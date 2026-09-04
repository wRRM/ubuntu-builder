from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
import shutil
import threading
import uuid
from copy import deepcopy
from pathlib import Path
from typing import BinaryIO

from .iso import IsoService


DEFAULT_STATE = {
    "baseIso": None,
    "files": [],
    "grubFiles": [],
    "build": {"status": "idle", "output": None, "error": None, "log": []},
}


def normalize_iso_path(value: str) -> str:
    value = (value or "").replace("\\", "/").strip()
    if "\x00" in value:
        raise ValueError("Destination contains an invalid character")
    if not value.startswith("/"):
        value = "/" + value
    parts = value.split("/")
    if any(part == ".." for part in parts):
        raise ValueError("Destination cannot contain '..'")
    normalized = posixpath.normpath(value)
    if normalized == "/" or value.endswith("/"):
        raise ValueError("Destination must include a file name")
    if len(normalized) > 1024:
        raise ValueError("Destination is too long")
    return normalized


def safe_output_name(value: str) -> str:
    name = Path(value or "custom-ubuntu.iso").name
    if not name.lower().endswith(".iso"):
        name += ".iso"
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name)
    return name[:120] or "custom-ubuntu.iso"


class ProjectStore:
    def __init__(self, root: Path, iso_service=None) -> None:
        self.root = root
        self.input_dir = root / "input"
        self.staged_dir = root / "staged"
        self.output_dir = root / "output"
        self.work_dir = root / "work"
        self.upload_tmp_dir = root / "tmp"
        self.state_path = root / "state.json"
        for directory in (
            root,
            self.input_dir,
            self.staged_dir,
            self.output_dir,
            self.work_dir,
            self.upload_tmp_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        self.iso = iso_service or IsoService()
        self.lock = threading.RLock()
        self.build_lock = threading.Lock()
        self.state = self._load()
        if self.state["build"]["status"] in {"queued", "running"}:
            self.state["build"].update(status="failed", error="The container stopped during the previous build")
            self._save()

    def _load(self) -> dict:
        if not self.state_path.exists():
            return deepcopy(DEFAULT_STATE)
        try:
            loaded = json.loads(self.state_path.read_text(encoding="utf-8"))
            return {**deepcopy(DEFAULT_STATE), **loaded}
        except (OSError, json.JSONDecodeError):
            return deepcopy(DEFAULT_STATE)

    def _save(self) -> None:
        temporary = self.state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.state, indent=2), encoding="utf-8")
        os.replace(temporary, self.state_path)

    def snapshot(self) -> dict:
        with self.lock:
            return deepcopy(self.state)

    @staticmethod
    def _copy_stream(stream: BinaryIO, destination: Path) -> tuple[int, str]:
        digest = hashlib.sha256()
        size = 0
        try:
            with destination.open("wb") as target:
                while chunk := stream.read(1024 * 1024):
                    target.write(chunk)
                    digest.update(chunk)
                    size += len(chunk)
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        return size, digest.hexdigest()

    def set_base_iso(self, stream: BinaryIO, original_name: str) -> dict:
        with self.lock:
            if self.state["build"]["status"] in {"queued", "running"}:
                raise ValueError("Wait for the current build before replacing the base ISO")
        temporary = self.input_dir / f"upload-{uuid.uuid4().hex}.iso"
        try:
            size, sha256 = self._copy_stream(stream, temporary)
            if size == 0:
                raise ValueError("The uploaded ISO is empty")
            self.iso.validate(temporary)
            grub = self.iso.discover_grub(temporary)
            final_path = self.input_dir / "base.iso"
            with self.lock:
                if self.state["build"]["status"] in {"queued", "running"}:
                    raise ValueError("A build started while the ISO was uploading; please try again when it finishes")
                conflicting_paths = sorted(
                    {item["destination"] for item in self.state["files"]}.intersection(grub)
                )
                if conflicting_paths:
                    raise ValueError(
                        "Remove the staged GRUB path before replacing the ISO: " + ", ".join(conflicting_paths)
                    )
                os.replace(temporary, final_path)
                self.state["baseIso"] = {
                    "name": Path(original_name).name or "base.iso",
                    "size": size,
                    "sha256": sha256,
                }
                self.state["grubFiles"] = [
                    {"path": path, "content": content, "originalContent": content}
                    for path, content in grub.items()
                ]
                self.state["build"] = deepcopy(DEFAULT_STATE["build"])
                self._save()
                return self.snapshot()
        finally:
            temporary.unlink(missing_ok=True)

    def add_files(self, uploads: list[tuple[BinaryIO, str, str]]) -> list[dict]:
        created: list[tuple[Path, dict]] = []
        with self.lock:
            if not self.state["baseIso"]:
                raise ValueError("Upload a base ISO before staging files")
            if self.state["build"]["status"] in {"queued", "running"}:
                raise ValueError("Wait for the current build before changing staged files")
            existing = {item["destination"] for item in self.state["files"]}
            grub_paths = {item["path"] for item in self.state["grubFiles"]}
            normalized_uploads = []
            batch_paths: set[str] = set()
            for stream, filename, destination in uploads:
                normalized = normalize_iso_path(destination)
                if normalized in existing or normalized in batch_paths:
                    raise ValueError(f"A staged file already uses {normalized}")
                if normalized in grub_paths:
                    raise ValueError(f"Edit {normalized} in the GRUB editor instead")
                batch_paths.add(normalized)
                normalized_uploads.append((stream, Path(filename).name, normalized))

            try:
                for stream, filename, destination in normalized_uploads:
                    file_id = uuid.uuid4().hex
                    disk_path = self.staged_dir / file_id
                    size, sha256 = self._copy_stream(stream, disk_path)
                    item = {
                        "id": file_id,
                        "name": filename or Path(destination).name,
                        "destination": destination,
                        "size": size,
                        "sha256": sha256,
                    }
                    created.append((disk_path, item))
                self.state["files"].extend(item for _, item in created)
                self._save()
                return [deepcopy(item) for _, item in created]
            except Exception:
                for disk_path, _ in created:
                    disk_path.unlink(missing_ok=True)
                raise

    def remove_file(self, file_id: str) -> bool:
        with self.lock:
            if self.state["build"]["status"] in {"queued", "running"}:
                raise ValueError("Wait for the current build before changing staged files")
            found = next((item for item in self.state["files"] if item["id"] == file_id), None)
            if not found:
                return False
            self.state["files"] = [item for item in self.state["files"] if item["id"] != file_id]
            self._save()
        (self.staged_dir / file_id).unlink(missing_ok=True)
        return True

    def update_grub(self, path: str, content: str) -> dict:
        if len(content.encode("utf-8")) > 2 * 1024**2:
            raise ValueError("GRUB configuration cannot exceed 2 MiB")
        with self.lock:
            if self.state["build"]["status"] in {"queued", "running"}:
                raise ValueError("Wait for the current build before changing GRUB")
            item = next((item for item in self.state["grubFiles"] if item["path"] == path), None)
            if not item:
                raise KeyError(path)
            item["content"] = content
            self._save()
            return deepcopy(item)

    def start_build(self, requested_name: str) -> dict:
        with self.lock:
            if not self.state["baseIso"]:
                raise ValueError("Upload a base ISO before building")
            if self.state["build"]["status"] in {"queued", "running"}:
                raise ValueError("A build is already running")
            output_name = safe_output_name(requested_name)
            self.state["build"] = {"status": "queued", "output": None, "error": None, "log": []}
            self._save()
        thread = threading.Thread(target=self._build, args=(output_name,), daemon=True, name="iso-builder")
        thread.start()
        return self.snapshot()["build"]

    def _append_log(self, message: str) -> None:
        if not message:
            return
        with self.lock:
            self.state["build"]["log"] = (self.state["build"]["log"] + [message])[-200:]

    def _build(self, output_name: str) -> None:
        with self.build_lock:
            temporary_output = self.work_dir / f"{uuid.uuid4().hex}.iso"
            grub_work = self.work_dir / f"grub-{uuid.uuid4().hex}"
            grub_work.mkdir()
            try:
                with self.lock:
                    snapshot = deepcopy(self.state)
                    self.state["build"]["status"] = "running"
                    self._save()
                mappings: list[tuple[Path, str]] = []
                for item in snapshot["files"]:
                    source = self.staged_dir / item["id"]
                    if not source.is_file():
                        raise RuntimeError(f"Staged source is missing: {item['destination']}")
                    mappings.append((source, item["destination"]))
                for index, item in enumerate(snapshot["grubFiles"]):
                    source = grub_work / str(index)
                    source.write_text(item["content"], encoding="utf-8")
                    mappings.append((source, item["path"]))
                self._append_log(f"Building from {snapshot['baseIso']['name']}")
                self.iso.build(self.input_dir / "base.iso", temporary_output, mappings, self._append_log)
                final_output = self.output_dir / output_name
                os.replace(temporary_output, final_output)
                with self.lock:
                    self.state["build"].update(
                        status="complete",
                        output={"name": output_name, "size": final_output.stat().st_size},
                        error=None,
                    )
                    self._save()
            except Exception as exc:
                with self.lock:
                    self.state["build"].update(status="failed", output=None, error=str(exc))
                    self._save()
            finally:
                temporary_output.unlink(missing_ok=True)
                shutil.rmtree(grub_work, ignore_errors=True)

    def output_path(self, name: str) -> Path | None:
        safe_name = safe_output_name(name)
        candidate = self.output_dir / safe_name
        return candidate if safe_name == name and candidate.is_file() else None
