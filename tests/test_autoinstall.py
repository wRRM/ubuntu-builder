from __future__ import annotations

import pytest

from app.autoinstall import AutoinstallGrubError, enable_autoinstall


def test_adds_autoinstall_before_separator_on_every_ubuntu_installer_directive():
    content = """menuentry 'Install Ubuntu' {
  linux /casper/vmlinuz quiet splash ---
  initrd /casper/initrd
}
menuentry 'Safe graphics' {
  linuxefi /casper/vmlinuz nomodeset ---
}
"""

    updated, added, directives, boot_entry, boot_changed = enable_autoinstall(content)

    assert added == 2
    assert directives == 2
    assert boot_entry == "Install Ubuntu"
    assert boot_changed is True
    assert updated.startswith("set default='Install Ubuntu'\nset timeout_style=hidden\nset timeout=0\n")
    assert "quiet splash autoinstall ---" in updated
    assert "nomodeset autoinstall ---" in updated


def test_is_idempotent_and_preserves_existing_autoinstall_argument():
    content = """set default='Try or Install Ubuntu'
set timeout_style=hidden
set timeout=0
menuentry 'Try or Install Ubuntu' {
  linux /casper/vmlinuz autoinstall quiet ---
}
"""

    updated, added, directives, boot_entry, boot_changed = enable_autoinstall(content)

    assert updated == content
    assert added == 0
    assert directives == 1
    assert boot_entry == "Try or Install Ubuntu"
    assert boot_changed is False


def test_adds_autoinstall_when_separator_is_absent_and_preserves_line_ending():
    content = "menuentry 'Install Ubuntu' {\r\nlinux16 /casper/vmlinuz quiet  \r\n}\r\n"

    updated, added, directives, _, _ = enable_autoinstall(content)

    assert "linux16 /casper/vmlinuz quiet autoinstall  \r\n" in updated
    assert added == 1
    assert directives == 1


def test_rejects_config_without_linux_boot_directives():
    with pytest.raises(AutoinstallGrubError, match="No Ubuntu installer boot directives"):
        enable_autoinstall("menuentry 'Install Ubuntu' {}\n")


def test_rejects_config_without_install_ubuntu_entry():
    with pytest.raises(AutoinstallGrubError, match="No Install Ubuntu menu entry"):
        enable_autoinstall("menuentry 'Safe graphics' {\n  linux /casper/vmlinuz ---\n}\n")


def test_replaces_existing_boot_settings_and_selects_server_install_entry():
    content = """set default=0
set timeout_style=menu
set timeout=30
menuentry 'Memory test' {
  linux /memtest ---
}
menuentry 'Try or Install Ubuntu Server' {
  linux /casper/vmlinuz ---
}
"""

    updated, _, _, boot_entry, boot_changed = enable_autoinstall(content)

    assert "set default='Try or Install Ubuntu Server'" in updated
    assert "set timeout_style=hidden" in updated
    assert "set timeout=0" in updated
    assert "set timeout=30" not in updated
    assert "linux /memtest ---" in updated
    assert "linux /memtest autoinstall" not in updated
    assert boot_entry == "Try or Install Ubuntu Server"
    assert boot_changed is True
