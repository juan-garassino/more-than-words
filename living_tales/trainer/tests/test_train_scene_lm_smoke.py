from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TRAINER = Path(__file__).resolve().parents[1]


def _run(args, timeout=600):
    return subprocess.run(
        [sys.executable, str(TRAINER / "tools" / "train_scene_lm.py"), *args],
        capture_output=True, text=True, timeout=timeout, cwd=str(TRAINER))


def test_base_then_adapter_smoke(tmp_path):
    r = _run(["base", "--steps", "8", "--batch-size", "2", "--hidden-dim", "32",
              "--n-layers", "1", "--n-heads", "4", "--output-dir", str(tmp_path)])
    assert r.returncode == 0, r.stderr[-2000:]
    assert (tmp_path / "_base" / "scene_lm_base.pt").exists()

    r = _run(["adapter", "--case", "amber_cipher", "--steps", "5",
              "--batch-size", "2", "--output-dir", str(tmp_path)])
    assert r.returncode == 0, r.stderr[-2000:]
    assert (tmp_path / "amber_cipher" / "scene_lm_full.pt").exists()
