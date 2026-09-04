from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from app.iso import IsoService, IsoToolError


class DiscoveryIsoService(IsoService):
    def _run(self, arguments, *, timeout=None):
        if "-find" in arguments:
            filename = arguments[arguments.index("-name") + 1]
            output = "'/boot/grub/grub.cfg'\n" if filename == "grub.cfg" else ""
            assert arguments[-2:] == ["-exec", "echo"]
            return subprocess.CompletedProcess(arguments, 0, stdout=output, stderr="")
        destination = Path(arguments[-1])
        destination.write_text("set timeout=10\n", encoding="utf-8")
        return subprocess.CompletedProcess(arguments, 0, stdout="", stderr="")


def test_discovers_quoted_xorriso_find_output(tmp_path):
    service = DiscoveryIsoService()
    assert service.discover_grub(tmp_path / "base.iso") == {
        "/boot/grub/grub.cfg": "set timeout=10\n"
    }


def test_rejects_file_without_iso9660_signature(tmp_path):
    source = tmp_path / "renamed.iso"
    source.write_text("not an ISO", encoding="utf-8")
    with pytest.raises(IsoToolError, match="not an ISO 9660"):
        IsoService().validate(source)
