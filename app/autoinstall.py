from __future__ import annotations

import re


class AutoinstallGrubError(ValueError):
    pass


_LINUX_DIRECTIVE = re.compile(r"^(?P<prefix>\s*linux(?:efi|16)?)(?P<arguments>\s+.*)$")
_AUTOINSTALL_ARGUMENT = re.compile(r"(?:^|\s)autoinstall(?=\s|$)")
_GRUB_ARGUMENT_SEPARATOR = re.compile(r"(?<!\S)---(?=\s|$)")
_UBUNTU_INSTALLER_KERNEL = re.compile(r"(?:^|\s)/casper/vmlinuz(?=\s|$)")
_MENUENTRY = re.compile(r"^\s*menuentry\s+(?P<quote>['\"])(?P<title>.*?)(?P=quote)(?=\s)")
_INSTALL_UBUNTU = re.compile(r"\binstall\s+ubuntu\b", re.IGNORECASE)


def _split_line(line: str) -> tuple[str, str]:
    body = line.rstrip("\r\n")
    return body, line[len(body) :]


def _grub_quote(value: str) -> str:
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    raise AutoinstallGrubError("The Install Ubuntu menu entry title cannot be safely selected")


def _configure_direct_boot(content: str, entry_line: int, entry_title: str) -> tuple[str, bool]:
    lines = content.splitlines(keepends=True)
    newline = "\r\n" if any(line.endswith("\r\n") for line in lines) else "\n"
    desired = (
        ("default", _grub_quote(entry_title)),
        ("timeout_style", "hidden"),
        ("timeout", "0"),
    )
    additions: list[str] = []

    for name, value in desired:
        setting = re.compile(rf"^(?P<indent>\s*)set\s+{re.escape(name)}\s*=.*$")
        found = False
        for index in range(entry_line):
            body, ending = _split_line(lines[index])
            match = setting.match(body)
            if match:
                lines[index] = f"{match.group('indent')}set {name}={value}{ending}"
                found = True
        if not found:
            additions.append(f"set {name}={value}{newline}")

    if additions:
        lines[entry_line:entry_line] = additions

    updated = "".join(lines)
    return updated, updated != content


def enable_autoinstall(content: str) -> tuple[str, int, int, str, bool]:
    """Configure a hidden direct boot and add autoinstall to Linux directives."""
    install_entry: tuple[int, str] | None = None
    for index, line in enumerate(content.splitlines(keepends=True)):
        body, _ = _split_line(line)
        match = _MENUENTRY.match(body)
        if match and _INSTALL_UBUNTU.search(match.group("title")):
            install_entry = (index, match.group("title"))
            break

    if not install_entry:
        raise AutoinstallGrubError("No Install Ubuntu menu entry was found in this grub.cfg")

    content, boot_changed = _configure_direct_boot(content, *install_entry)
    updated_lines: list[str] = []
    directive_count = 0
    added_count = 0

    for line in content.splitlines(keepends=True):
        body, ending = _split_line(line)
        match = _LINUX_DIRECTIVE.match(body)
        if not match or not _UBUNTU_INSTALLER_KERNEL.search(match.group("arguments")):
            updated_lines.append(line)
            continue

        directive_count += 1
        arguments = match.group("arguments")
        if _AUTOINSTALL_ARGUMENT.search(arguments):
            updated_lines.append(line)
            continue

        separator = _GRUB_ARGUMENT_SEPARATOR.search(arguments)
        if separator:
            arguments = f"{arguments[:separator.start()]}autoinstall {arguments[separator.start():]}"
        else:
            trailing_start = len(arguments.rstrip())
            arguments = f"{arguments[:trailing_start]} autoinstall{arguments[trailing_start:]}"

        updated_lines.append(f"{match.group('prefix')}{arguments}{ending}")
        added_count += 1

    if directive_count == 0:
        raise AutoinstallGrubError("No Ubuntu installer boot directives were found in this grub.cfg")

    return "".join(updated_lines), added_count, directive_count, install_entry[1], boot_changed
