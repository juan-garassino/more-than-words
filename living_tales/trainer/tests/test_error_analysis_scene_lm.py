from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

CASE = "amber_cipher"


@pytest.fixture(scope="module")
def tiny_ckpt(production_cases, tmp_path_factory):
    from trainer.scene_lm import SceneLM, SceneLMConfig
    from trainer.scene_lm_vocab import SceneVocab
    vocab = SceneVocab.build(production_cases)
    model = SceneLM(SceneLMConfig(vocab_size=len(vocab), n_layers=1,
                                  hidden_dim=32, n_heads=4, max_seq_len=2048))
    p = tmp_path_factory.mktemp("ckpt") / "m.pt"
    model.save(p, vocab, case_id=CASE)
    return p


def test_analyze_report_shape(tiny_ckpt):
    from tools.error_analysis_scene_lm import analyze
    rep = analyze(tiny_ckpt, CASE, n_turns=2, n_seeds=1, max_sequences=4)
    tf = rep["teacher_forced"]
    for split in ("train", "holdout"):
        assert tf[split]["per_dim"], split
        for dim, cell in tf[split]["per_dim"].items():
            assert set(cell) >= {"acc", "n"}, dim
    assert rep["confusion"], "per-dim confusion pairs missing"
    dim, pairs = next(iter(rep["confusion"].items()))
    assert pairs and set(pairs[0]) >= {"truth", "pred", "count"}
    oc = rep["outcome"]
    assert oc["classes"] and len(oc["matrix"]) == len(oc["classes"])
    assert set(oc["per_class_recall"]) == set(oc["classes"])
    fr = rep["free_run"]
    assert fr["histograms"] and "binding_misses" in fr and "coherence_violations" in fr


def test_analyze_writes_reports(tiny_ckpt, tmp_path):
    from tools.error_analysis_scene_lm import analyze, write_reports
    rep = analyze(tiny_ckpt, CASE, n_turns=2, n_seeds=1, max_sequences=4)
    write_reports(rep, tmp_path)
    assert (tmp_path / "error_analysis.json").exists()
    md = (tmp_path / "error_analysis.md").read_text()
    assert "Error → lever map" in md and "BEAT" in md
