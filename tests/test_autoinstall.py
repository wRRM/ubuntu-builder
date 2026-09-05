from __future__ import annotations

import pytest

from app.autoinstall import AutoinstallGrubError, enable_autoinstall


def test_adds_autoinstall_before_separator_on_every_linux_directive():
    content = """menuentry 'Install Ubuntu' {
  linux /casper/vmlinuz quiet splash ---
  initrd /casper/initrd
}
menuentry 'Safe graphics' {
  linuxefi /casper/vmlinuz nomodeset ---
}
"""

    updated, added, directives = enable_autoinstall(content)

    assert added == 2
    assert directives == 2
    assert "quiet splash autoinstall ---" in updated
    assert "nomodeset autoinstall ---" in updated


def test_is_idempotent_and_preserves_existing_autoinstall_argument():
    content = "  linux /casper/vmlinuz autoinstall quiet ---\n"

    updated, added, directives = enable_autoinstall(content)

    assert updated == content
    assert added == 0
    assert directives == 1


def test_adds_autoinstall_when_separator_is_absent_and_preserves_line_ending():
    content = "linux16 /casper/vmlinuz quiet  \r\n"

    updated, added, directives = enable_autoinstall(content)

    assert updated == "linux16 /casper/vmlinuz quiet autoinstall  \r\n"
    assert added == 1
    assert directives == 1


def test_rejects_config_without_linux_boot_directives():
    with pytest.raises(AutoinstallGrubError, match="No Linux boot directives"):
        enable_autoinstall("set timeout=5\n")
