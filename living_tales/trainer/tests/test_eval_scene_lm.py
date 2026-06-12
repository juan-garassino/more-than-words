from __future__ import annotations

import pytest

from tools.eval_scene_lm import (
    BINDING_CHECK,
    INTRANSITIVE_ACTIONS,
    probe_binding,
    probe_coherence,
    probe_diversity,
    spearman,
)

CASE = "amber_cipher"


def test_spearman_basics():
    assert spearman([1, 2, 3, 4], [1, 2, 3, 4]) == pytest.approx(1.0)
    assert spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)


def test_binding_check_table():
    assert BINDING_CHECK["object"]("object:satchel",
                                   {"OBJECT_FOCUS": "object:satchel"})
    assert not BINDING_CHECK["object"]("object:satchel",
                                       {"OBJECT_FOCUS": "object:telegram"})
    assert BINDING_CHECK["suspect"]("suspect:renard_voss",
                                    {"PRESENCE": "presence:with_renard_voss"})


def test_intransitive_set():
    assert "action:waits" in INTRANSITIVE_ACTIONS


@pytest.fixture(scope="module")
def make_engine(production_cases, tmp_path_factory):
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from generator.scene_lm_runtime import SceneLMEngine
    from trainer.scene_lm import SceneLM, SceneLMConfig
    from trainer.scene_lm_vocab import SceneVocab
    vocab = SceneVocab.build(production_cases)
    model = SceneLM(SceneLMConfig(vocab_size=len(vocab), n_layers=1,
                                  hidden_dim=32, n_heads=4, max_seq_len=512))
    p = tmp_path_factory.mktemp("ckpt") / "m.pt"
    model.save(p, vocab, case_id=CASE)

    def make(seed):
        eng = SceneLMEngine.load(p, seed=seed)
        eng.ledger_path = tmp_path_factory.mktemp("ledger") / "ledger.json"
        return eng
    return make


def test_probes_run_on_tiny_engine(make_engine):
    eng0 = make_engine(0)
    vocab = eng0.vocab
    r1 = probe_binding(make_engine, vocab, CASE, n_turns=4, n_seeds=1)
    assert 0.0 <= r1["score"] <= 1.0 and r1["n"] > 0
    r2 = probe_coherence(make_engine, CASE, n_turns=4, n_seeds=1)
    assert "violations" in r2
    r3 = probe_diversity(make_engine, vocab, CASE, n_turns=4, n_seeds=1)
    assert set(r3) >= {"REVELATION", "TRANSITION", "BEAT"}
