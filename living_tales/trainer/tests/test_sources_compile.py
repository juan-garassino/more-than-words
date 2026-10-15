"""Every trainer source must byte-compile on the supported interpreters
(requires-python >=3.10), e.g. no PEP 701 f-strings that need 3.12."""
from __future__ import annotations

import py_compile
from pathlib import Path

import pytest

TRAINER_ROOT = Path(__file__).resolve().parents[1]
SOURCES = sorted(p for d in ("trainer", "generator", "tools")
                 for p in (TRAINER_ROOT / d).rglob("*.py"))


@pytest.mark.parametrize("path", SOURCES, ids=lambda p: str(p.relative_to(TRAINER_ROOT)))
def test_source_compiles(path, tmp_path):
    py_compile.compile(str(path), cfile=str(tmp_path / "x.pyc"), doraise=True)
