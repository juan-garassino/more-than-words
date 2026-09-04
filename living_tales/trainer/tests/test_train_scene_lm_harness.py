"""Checkpoint/resume/logging/mid-eval harness around train_scene_lm.py.
Tiny CPU runs only — training happens on Colab."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

TRAINER = Path(__file__).resolve().parents[1]

TINY = ["--batch-size", "2", "--hidden-dim", "32", "--n-layers", "1",
        "--n-heads", "4"]


def _run(args, timeout=900):
    return subprocess.run(
        [sys.executable, str(TRAINER / "tools" / "train_scene_lm.py"), *args],
        capture_output=True, text=True, timeout=timeout, cwd=str(TRAINER))


def _rows(p):
    return [json.loads(line) for line in p.read_text().splitlines()]


def test_checkpoint_log_resume_and_mid_eval(tmp_path):
    out = str(tmp_path)
    r = _run(["base", "--steps", "6", "--checkpoint-every", "2",
              "--log-every", "2", *TINY, "--output-dir", out])
    assert r.returncode == 0, r.stderr[-2000:]
    base_dir = tmp_path / "_base"
    assert (base_dir / "scene_lm_base.pt").exists()
    assert (base_dir / "scene_lm_base.train_state.pt").exists()
    rows = _rows(base_dir / "train.jsonl")
    assert rows and rows[0]["stage"] == "base"
    assert {"step", "loss", "val_loss"} <= set(rows[-1])

    # resume continues from saved step instead of restarting
    r = _run(["base", "--steps", "8", "--checkpoint-every", "2",
              "--log-every", "2", *TINY, "--output-dir", out, "--resume"])
    assert r.returncode == 0, r.stderr[-2000:]
    assert "resumed at step 6" in r.stdout
    assert _rows(base_dir / "train.jsonl")[-1]["step"] == 8

    # adapter with mid-training eval writes eval.jsonl probe rows
    r = _run(["adapter", "--case", "amber_cipher", "--steps", "4",
              "--checkpoint-every", "2", "--log-every", "2",
              "--eval-every", "2", "--eval-turns", "2", "--eval-seeds", "1",
              "--batch-size", "2", "--output-dir", out])
    assert r.returncode == 0, r.stderr[-2000:]
    case_dir = tmp_path / "amber_cipher"
    assert (case_dir / "scene_lm_full.pt").exists()
    erows = _rows(case_dir / "eval.jsonl")
    assert erows and {"step", "binding", "outcome_acc", "gate_pass"} <= set(erows[-1])
