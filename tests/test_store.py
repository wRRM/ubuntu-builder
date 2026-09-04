from __future__ import annotations

import io
import shutil
import time
from pathlib import Path

import pytest

from app.store import ProjectStore, normalize_iso_path, safe_output_name


class FakeIsoService:
    def validate(self, iso_path: Path) -> None:
        if iso_path.read_bytes() == b"invalid":
            raise RuntimeError("invalid ISO")

    def discover_grub(self, _iso_path: Path) -> dict[str, str]:
        return {"/boot/grub/grub.cfg": "set timeout=30\nmenuentry 'Ubuntu' {}\n"}

    def build(self, base_iso: Path, output_iso: Path, mappings, log=None) -> None:
        assert base_iso.read_bytes() == b"iso-data"
        if log:
            log("fake build")
        shutil.copyfile(base_iso, output_iso)
        with output_iso.open("ab") as target:
            for source, destination in mappings:
                target.write(destination.encode())
                target.write(source.read_bytes())


def wait_for_build(store: ProjectStore) -> dict:
    for _ in range(100):
        build = store.snapshot()["build"]
        if build["status"] in {"complete", "failed"}:
            return build
        time.sleep(0.01)
    raise AssertionError("build did not finish")


def test_normalize_iso_path():
    assert normalize_iso_path("answer.txt") == "/answer.txt"
    assert normalize_iso_path(r"seed\user-data") == "/seed/user-data"
    with pytest.raises(ValueError):
        normalize_iso_path("../secret")
    with pytest.raises(ValueError):
        normalize_iso_path("/")


def test_safe_output_name():
    assert safe_output_name("My Ubuntu") == "My-Ubuntu.iso"
    assert safe_output_name("../../chosen.iso") == "chosen.iso"


def test_store_upload_edit_stage_and_build(tmp_path):
    store = ProjectStore(tmp_path, iso_service=FakeIsoService())
    store.set_base_iso(io.BytesIO(b"iso-data"), "ubuntu.iso")
    assert store.snapshot()["baseIso"]["name"] == "ubuntu.iso"
    assert store.snapshot()["grubFiles"][0]["path"] == "/boot/grub/grub.cfg"

    staged = store.add_files([(io.BytesIO(b"hello"), "hello.txt", "/hello.txt")])
    assert staged[0]["destination"] == "/hello.txt"
    store.update_grub("/boot/grub/grub.cfg", "set timeout=5\n")

    store.start_build("result.iso")
    build = wait_for_build(store)
    assert build["status"] == "complete"
    assert build["output"]["name"] == "result.iso"
    output = store.output_path("result.iso")
    assert output is not None
    assert b"/hello.txthello" in output.read_bytes()


def test_duplicate_and_traversal_destinations_are_rejected(tmp_path):
    store = ProjectStore(tmp_path, iso_service=FakeIsoService())
    store.set_base_iso(io.BytesIO(b"iso-data"), "ubuntu.iso")
    store.add_files([(io.BytesIO(b"one"), "one", "/same")])
    with pytest.raises(ValueError, match="already uses"):
        store.add_files([(io.BytesIO(b"two"), "two", "/same")])
    with pytest.raises(ValueError, match="cannot contain"):
        store.add_files([(io.BytesIO(b"bad"), "bad", "/a/../b")])


def test_files_require_a_base_iso(tmp_path):
    store = ProjectStore(tmp_path, iso_service=FakeIsoService())
    with pytest.raises(ValueError, match="base ISO"):
        store.add_files([(io.BytesIO(b"one"), "one", "/one")])


def test_uploaded_file_cannot_conflict_with_grub_editor(tmp_path):
    store = ProjectStore(tmp_path, iso_service=FakeIsoService())
    store.set_base_iso(io.BytesIO(b"iso-data"), "ubuntu.iso")
    with pytest.raises(ValueError, match="GRUB editor"):
        store.add_files([(io.BytesIO(b"bad"), "grub.cfg", "/boot/grub/grub.cfg")])
