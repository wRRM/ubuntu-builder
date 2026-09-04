from __future__ import annotations

import io
import shutil
from pathlib import Path

from app import create_app


class FakeIsoService:
    def validate(self, _iso_path: Path) -> None:
        pass

    def discover_grub(self, _iso_path: Path) -> dict[str, str]:
        return {"/boot/grub/grub.cfg": "set timeout=30\n"}

    def build(self, base_iso: Path, output_iso: Path, mappings, log=None) -> None:
        shutil.copyfile(base_iso, output_iso)


def test_health_and_initial_state(tmp_path):
    app = create_app(data_dir=tmp_path, iso_service=FakeIsoService())
    client = app.test_client()
    assert client.get("/health").json == {"status": "ok"}
    assert client.get("/api/state").json["baseIso"] is None
    assert client.get("/").status_code == 200


def test_upload_edit_and_stage_routes(tmp_path):
    app = create_app(data_dir=tmp_path, iso_service=FakeIsoService())
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

    response = client.post(
        "/api/files",
        data={"files": (io.BytesIO(b"payload"), "payload.txt"), "destinations": "/payload.txt"},
        content_type="multipart/form-data",
    )
    assert response.status_code == 201
    file_id = response.json["files"][0]["id"]
    assert client.delete(f"/api/files/{file_id}").status_code == 204


def test_rejects_bad_iso_extension(tmp_path):
    app = create_app(data_dir=tmp_path, iso_service=FakeIsoService())
    response = app.test_client().post(
        "/api/base-iso",
        data={"iso": (io.BytesIO(b"not an iso"), "notes.txt")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400

