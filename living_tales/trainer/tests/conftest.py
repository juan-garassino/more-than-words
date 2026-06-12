from __future__ import annotations

import sys
from pathlib import Path

import pytest

TRAINER_ROOT = Path(__file__).resolve().parents[1]   # living_tales/trainer
REPO_ROOT = TRAINER_ROOT.parents[1]
sys.path.insert(0, str(TRAINER_ROOT))


@pytest.fixture(scope="session")
def cases_dir() -> Path:
    return TRAINER_ROOT / "cases"


@pytest.fixture(scope="session")
def production_cases() -> list[str]:
    return ["amber_cipher", "attended_hour", "venetian_mirror"]
