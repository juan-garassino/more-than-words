from __future__ import annotations

import pytest

from generator.scene_lm_runtime import AttractorMeter, SceneLMEngine
from trainer.scene_lm import SceneLM, SceneLMConfig
from trainer.scene_lm_vocab import SceneVocab

CASE = "amber_cipher"


@pytest.fixture(scope="module")
def ckpt(production_cases, tmp_path_factory):
    vocab = SceneVocab.build(production_cases)
    model = SceneLM(SceneLMConfig(vocab_size=len(vocab), n_layers=1,
                                  hidden_dim=32, n_heads=4, max_seq_len=512))
    p = tmp_path_factory.mktemp("ckpt") / "scene_lm_full.pt"
    model.save(p, vocab, case_id=CASE)
    return p


@pytest.fixture()
def engine(ckpt, tmp_path):
    eng = SceneLMEngine.load(ckpt, seed=1)
    eng.ledger_path = tmp_path / "ledger.json"
    return eng


def test_step_returns_full_scene_and_convergence(engine):
    scene, conv = engine.step("object:initialed_cufflink")
    assert set(scene) == set(engine.vocab.slot_dims(CASE))
    assert len(conv) == 3 and all(0.0 <= c <= 1.0 for c in conv)


def test_convergence_monotone_nondecreasing(engine):
    _, c1 = engine.step("witness:porter")
    _, c2 = engine.step("object:torn_ticket")
    assert all(b >= a for a, b in zip(c1, c2))


def test_scene_respects_constraints_first_turn(engine):
    # constraints.json: transition:returned requires a visited location —
    # impossible on turn 1, so the mask must exclude it.
    scene, _ = engine.step("object:initialed_cufflink")
    assert scene["TRANSITION"] != "transition:returned"


def test_accuse_returns_confrontation_and_model_decides_ending(engine):
    engine.step("object:initialed_cufflink")
    res = engine.accuse("suspect:renard_voss")
    assert set(res["scene"]) == set(engine.vocab.slot_dims(CASE))
    assert isinstance(res["ended"], bool)
    if res["ended"]:
        assert res["outcome"] in engine.vocab.outcome_classes(CASE)
        assert isinstance(res["ending"], dict)
    else:                                   # near-miss: story continues
        assert res["outcome"] is None


def test_resolve_forces_an_outcome(engine):
    engine.step("witness:porter")
    outcome, ending = engine.resolve()
    assert outcome in engine.vocab.outcome_classes(CASE)
    assert isinstance(ending, dict) and "type" in ending


def test_attractor_meter_maps_presence_to_suspect(production_cases, cases_dir):
    vocab = SceneVocab.build(production_cases)
    m = AttractorMeter(CASE, cases_dir / CASE)
    w = m.weights_for("presence:with_renard_voss")
    assert w is not None and len(w) == 3      # resolved via suspect:renard_voss


def test_ledger_records_outcome(engine):
    engine.step("object:initialed_cufflink")
    outcome, _ = engine.resolve()
    found, total = engine.ledger_progress()
    assert found >= 1
    assert total == len(engine.vocab.outcome_classes(CASE))


def test_game_state_tracks_locations(engine):
    scene, _ = engine.step("object:initialed_cufflink")
    gs = engine.game_state()
    if scene["LOCATION"] != "location:none":
        assert scene["LOCATION"] in gs["visited_locations"]
    assert gs["game_turn"] == 1
    assert gs["last_player_card"] == "object:initialed_cufflink"
