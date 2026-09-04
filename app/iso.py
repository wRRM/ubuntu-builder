from __future__ import annotations

import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Callable


class IsoToolError(RuntimeError):
    pass


class IsoService:
    def __init__(self, executable: str = "xorriso") -> None:
        self.executable = executable

    def _run(self, arguments: list[str], *, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                [self.executable, *arguments],
                check=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except FileNotFoundError as exc:
            raise IsoToolError("xorriso is not installed in the container") from exc
        except subprocess.TimeoutExpired as exc:
            raise IsoToolError("ISO operation timed out") from exc
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or exc.stdout or "xorriso failed").strip()
            raise IsoToolError(detail[-4000:]) from exc

    def validate(self, iso_path: Path) -> None:
        self._run(["-report_about", "SORRY", "-indev", str(iso_path), "-toc"], timeout=60)

    def discover_grub(self, iso_path: Path) -> dict[str, str]:
        paths: set[str] = set()
        for filename in ("grub.cfg", "loopback.cfg"):
            result = self._run(
                [
                    "-report_about",
                    "SORRY",
                    "-indev",
                    str(iso_path),
                    "-find",
                    "/",
                    "-type",
                    "f",
                    "-name",
                    filename,
                    "-exec",
                    "echo",
                ],
                timeout=60,
            )
            for line in result.stdout.splitlines():
                try:
                    fields = shlex.split(line)
                except ValueError:
                    continue
                if len(fields) == 1 and fields[0].startswith("/"):
                    paths.add(fields[0])

        configs: dict[str, str] = {}
        with tempfile.TemporaryDirectory(prefix="grub-inspect-") as temp_dir:
            for index, iso_file in enumerate(sorted(paths)):
                destination = Path(temp_dir) / str(index)
                self._run(
                    [
                        "-report_about",
                        "SORRY",
                        "-osirrox",
                        "on",
                        "-indev",
                        str(iso_path),
                        "-extract",
                        iso_file,
                        str(destination),
                    ],
                    timeout=60,
                )
                if destination.stat().st_size > 2 * 1024**2:
                    raise IsoToolError(f"GRUB configuration is unexpectedly large: {iso_file}")
                configs[iso_file] = destination.read_text(encoding="utf-8", errors="replace")
        return configs

    def build(
        self,
        base_iso: Path,
        output_iso: Path,
        mappings: list[tuple[Path, str]],
        log: Callable[[str], None] | None = None,
    ) -> None:
        arguments = [
            "-report_about",
            "NOTE",
            "-indev",
            str(base_iso),
            "-outdev",
            str(output_iso),
            "-boot_image",
            "any",
            "replay",
            "-overwrite",
            "on",
        ]
        for source, destination in mappings:
            arguments.extend(["-map", str(source), destination])
        arguments.extend(["-commit", "-end"])

        try:
            process = subprocess.Popen(
                [self.executable, *arguments],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except FileNotFoundError as exc:
            raise IsoToolError("xorriso is not installed in the container") from exc

        assert process.stdout is not None
        for line in process.stdout:
            if log:
                log(line.rstrip())
        return_code = process.wait()
        if return_code:
            raise IsoToolError(f"xorriso exited with status {return_code}")
        if not output_iso.is_file() or output_iso.stat().st_size == 0:
            raise IsoToolError("xorriso did not create an output ISO")
        os.chmod(output_iso, 0o640)
