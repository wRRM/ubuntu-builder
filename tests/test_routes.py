from __future__ import annotations

import errno
import io
import shutil
import tempfile
from pathlib import Path

from app import create_app
from app.grub import GrubValidationError


class FakeIsoService:
    def validate(self, _iso_path: Path) -> None:
        pass

    def discover_grub(self, _iso_path: Path) -> dict[str, str]:
        return {"/boot/grub/grub.cfg": "set timeout=30\n"}

    def build(self, base_iso: Path, output_iso: Path, mappings, log=None) -> None:
        shutil.copyfile(base_iso, output_iso)


class FakeGrubValidator:
    def validate(self, _content: str) -> str:
        return "GRUB syntax valid · Changes saved"


class RejectingGrubValidator:
    def validate(self, _content: str) -> str:
        raise GrubValidationError("GRUB configuration:2: syntax error")


def make_app(tmp_path, *, grub_validator=None):
    return create_app(
        data_dir=tmp_path,
        iso_service=FakeIsoService(),
        grub_validator=grub_validator or FakeGrubValidator(),
    )


def test_health_and_initial_state(tmp_path):
    app = make_app(tmp_path)
    client = app.test_client()
    assert tempfile.tempdir == str(tmp_path / "tmp")
    assert client.get("/health").json == {"status": "ok"}
    assert client.get("/api/state").json["baseIso"] is None
    assert client.get("/").status_code == 200


def test_upload_edit_and_stage_routes(tmp_path):
    app = make_app(tmp_path)
    client = app.test_client()
    response = client.post(
        "/api/base-iso",
        data={"iso": (io.BytesIO(b"iso"), "ubuntu.iso")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert response.json["grubFiles"][0]["content"] == "set timeout=30\n"

    response = client.put(
        "/api/grub",
        json={"path": "/boot/grub/grub.cfg", "content": "set timeout=5\n"},
    )
    assert response.status_code == 200
    assert response.json["validation"] == {
        "valid": True,
        "message": "GRUB syntax valid · Changes saved",
    }

    response = client.post(
        "/api/files",
        data={"files": (io.BytesIO(b"payload"), "payload.txt"), "destinations": "/payload.txt"},
        content_type="multipart/form-data",
    )
    assert response.status_code == 201
    file_id = response.json["files"][0]["id"]
    assert client.delete(f"/api/files/{file_id}").status_code == 204


def test_rejects_bad_iso_extension(tmp_path):
    app = make_app(tmp_path)
    response = app.test_client().post(
        "/api/base-iso",
        data={"iso": (io.BytesIO(b"not an iso"), "notes.txt")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


def test_storage_full_returns_json_error(tmp_path):
    app = make_app(tmp_path)

    def fail_upload(*_args, **_kwargs):
        raise OSError(errno.ENOSPC, "No space left on device")

    app.extensions["project_store"].set_base_iso = fail_upload
    response = app.test_client().post(
        "/api/base-iso",
        data={"iso": (io.BytesIO(b"iso"), "ubuntu.iso")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 507
    assert response.is_json
    assert response.json == {"error": "Not enough Docker storage to receive this ISO"}


def test_invalid_grub_is_not_saved(tmp_path):
    app = make_app(tmp_path, grub_validator=RejectingGrubValidator())
    client = app.test_client()
    client.post(
        "/api/base-iso",
        data={"iso": (io.BytesIO(b"iso"), "ubuntu.iso")},
        content_type="multipart/form-data",
    )

    response = client.put(
        "/api/grub",
        json={"path": "/boot/grub/grub.cfg", "content": "if broken"},
    )

    assert response.status_code == 422
    assert response.json["validation"]["valid"] is False
    assert client.get("/api/state").json["grubFiles"][0]["content"] == "set timeout=30\n"
