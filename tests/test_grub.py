from __future__ import annotations

import pytest

from app.grub import GrubValidationError, GrubValidator


def test_accepts_valid_grub_syntax():
    assert GrubValidator().validate("set timeout=5\n") == "GRUB syntax valid · Changes saved"


def test_rejects_invalid_grub_syntax_without_exposing_temp_path():
    with pytest.raises(GrubValidationError) as failure:
        GrubValidator().validate("if [ x = y ]; then\n  echo broken\n")
    assert "syntax error" in str(failure.value).lower()
    assert "/data/tmp/" not in str(failure.value)
