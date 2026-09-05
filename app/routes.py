from __future__ import annotations

import errno
from pathlib import PurePosixPath

from flask import Blueprint, current_app, jsonify, render_template, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge

from .autoinstall import AutoinstallGrubError, enable_autoinstall
from .grub import GrubValidationError
from .iso import IsoToolError
from .ubuntu import UbuntuReleaseError


api = Blueprint("api", __name__)


def store():
    return current_app.extensions["project_store"]


@api.get("/")
def index():
    return render_template("index.html")


@api.get("/health")
def health():
    return jsonify(status="ok")


@api.get("/api/state")
def state():
    return jsonify(store().snapshot())


@api.post("/api/base-iso")
def upload_base_iso():
    upload = request.files.get("iso")
    if not upload or not upload.filename:
        return jsonify(error="Choose an Ubuntu ISO to upload"), 400
    if not upload.filename.lower().endswith(".iso"):
        return jsonify(error="The base image must have an .iso extension"), 400
    try:
        return jsonify(store().set_base_iso(upload.stream, upload.filename))
    except (ValueError, IsoToolError) as exc:
        return jsonify(error=str(exc)), 400


@api.post("/api/base-iso/latest")
def download_latest_ubuntu():
    body = request.get_json(silent=True) or {}
    edition = body.get("edition", "desktop")
    if edition not in {"desktop", "server"}:
        return jsonify(error="Edition must be desktop or server"), 400
    try:
        return jsonify(
            current_app.extensions["ubuntu_release_service"].download_latest(
                store(),
                edition,
                max_bytes=current_app.config["MAX_CONTENT_LENGTH"],
            )
        )
    except (ValueError, IsoToolError) as exc:
        return jsonify(error=str(exc)), 400
    except UbuntuReleaseError as exc:
        return jsonify(error=str(exc)), 502


@api.post("/api/files")
def upload_files():
    files = request.files.getlist("files")
    destinations = request.form.getlist("destinations")
    if not files or len(files) != len(destinations):
        return jsonify(error="Each uploaded file needs an ISO destination"), 400
    try:
        entries = [(item.stream, item.filename or "file", destination) for item, destination in zip(files, destinations)]
        return jsonify(files=store().add_files(entries)), 201
    except ValueError as exc:
        return jsonify(error=str(exc)), 400


@api.delete("/api/files/<file_id>")
def delete_file(file_id: str):
    try:
        if not store().remove_file(file_id):
            return jsonify(error="Staged file not found"), 404
        return "", 204
    except ValueError as exc:
        return jsonify(error=str(exc)), 409


@api.put("/api/grub")
def save_grub():
    body = request.get_json(silent=True) or {}
    if not isinstance(body.get("path"), str) or not isinstance(body.get("content"), str):
        return jsonify(error="Path and content are required"), 400
    try:
        validation_message = current_app.extensions["grub_validator"].validate(body["content"])
        updated = store().update_grub(body["path"], body["content"])
        return jsonify(file=updated, validation={"valid": True, "message": validation_message})
    except GrubValidationError as exc:
        return jsonify(
            error="GRUB validation failed",
            validation={"valid": False, "message": str(exc)},
        ), 422
    except KeyError:
        return jsonify(error="GRUB file not found in the base ISO"), 404
    except ValueError as exc:
        return jsonify(error=str(exc)), 400


@api.post("/api/grub/autoinstall")
def add_grub_autoinstall():
    body = request.get_json(silent=True) or {}
    path = body.get("path")
    content = body.get("content")
    if not isinstance(path, str) or not isinstance(content, str):
        return jsonify(error="Path and content are required"), 400
    if PurePosixPath(path).name != "grub.cfg":
        return jsonify(error="Select a grub.cfg file to enable autoinstall"), 400

    try:
        updated_content, added_count, directive_count = enable_autoinstall(content)
        validation_message = current_app.extensions["grub_validator"].validate(updated_content)
        updated = store().update_grub(path, updated_content)
        return jsonify(
            file=updated,
            autoinstall={"added": added_count, "directives": directive_count},
            validation={"valid": True, "message": validation_message},
        )
    except AutoinstallGrubError as exc:
        return jsonify(error=str(exc)), 400
    except GrubValidationError as exc:
        return jsonify(
            error="GRUB validation failed",
            validation={"valid": False, "message": str(exc)},
        ), 422
    except KeyError:
        return jsonify(error="GRUB file not found in the base ISO"), 404
    except ValueError as exc:
        return jsonify(error=str(exc)), 400


@api.post("/api/build")
def build():
    body = request.get_json(silent=True) or {}
    try:
        return jsonify(store().start_build(str(body.get("name", "custom-ubuntu.iso")))), 202
    except ValueError as exc:
        return jsonify(error=str(exc)), 409


@api.get("/api/output/<name>")
def download(name: str):
    project_store = store()
    output = project_store.output_path(name)
    if not output:
        return jsonify(error="Output ISO not found"), 404
    response = send_file(
        output,
        as_attachment=True,
        download_name=name,
        mimetype="application/x-iso9660-image",
        conditional=False,
    )
    if request.method == "GET":
        source = response.response

        def stream_and_consume():
            completed = False
            try:
                yield from source
                completed = True
            finally:
                if hasattr(source, "close"):
                    source.close()
                if completed:
                    project_store.consume_output(name)

        response.response = stream_and_consume()
    return response


@api.app_errorhandler(RequestEntityTooLarge)
def too_large(_error):
    return jsonify(error="Upload exceeds MAX_UPLOAD_BYTES"), 413


@api.app_errorhandler(OSError)
def storage_error(error: OSError):
    if error.errno == errno.ENOSPC:
        return jsonify(error="Not enough Docker storage to receive this ISO"), 507
    current_app.logger.exception("Storage operation failed", exc_info=error)
    return jsonify(error="A storage error interrupted the upload"), 500
