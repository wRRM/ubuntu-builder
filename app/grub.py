from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


class GrubValidationError(ValueError):
    pass


class GrubValidator:
    def __init__(self, executable: str = "grub-script-check") -> None:
        self.executable = executable

    def validate(self, content: str) -> str:
        path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".cfg",
                delete=False,
            ) as source:
                source.write(content)
                path = Path(source.name)
            result = subprocess.run(
                [self.executable, str(path)],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except FileNotFoundError as exc:
            raise GrubValidationError("GRUB validator is unavailable in this container") from exc
        except subprocess.TimeoutExpired as exc:
            raise GrubValidationError("GRUB validation timed out") from exc
        finally:
            if path is not None:
                path.unlink(missing_ok=True)

        if result.returncode:
            detail = (result.stderr or result.stdout or "Syntax error").strip()
            detail = detail.replace(str(path), "GRUB configuration")
            raise GrubValidationError(detail[-2000:])
        return "GRUB syntax valid · Changes saved"
