from __future__ import annotations

import re


class AutoinstallGrubError(ValueError):
    pass


_LINUX_DIRECTIVE = re.compile(r"^(?P<prefix>\s*linux(?:efi|16)?)(?P<arguments>\s+.*)$")
_AUTOINSTALL_ARGUMENT = re.compile(r"(?:^|\s)autoinstall(?=\s|$)")
_GRUB_ARGUMENT_SEPARATOR = re.compile(r"(?<!\S)---(?=\s|$)")


def enable_autoinstall(content: str) -> tuple[str, int, int]:
    """Add the autoinstall kernel argument to every Linux boot directive."""
    updated_lines: list[str] = []
    directive_count = 0
    added_count = 0

    for line in content.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        ending = line[len(body) :]
        match = _LINUX_DIRECTIVE.match(body)
        if not match:
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
        raise AutoinstallGrubError("No Linux boot directives were found in this grub.cfg")

    return "".join(updated_lines), added_count, directive_count
