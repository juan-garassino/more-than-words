from __future__ import annotations

import pytest

from trainer.scene_lm_vocab import GRAMMAR_ORDER, SceneVocab


@pytest.fixture(scope="module")
def vocab(production_cases):
    return SceneVocab.build(production_cases)


def test_specials_have_stable_low_ids(vocab):
    assert vocab.encode("<pad>") == 0
    assert vocab.encode("<bos>") == 1
    for s in ["<eos>", "<card>", "<scene>", "<accuse>"]:
        assert vocab.encode(s) < 6


def test_grammar_order_starts_transition_location():
    assert GRAMMAR_ORDER[:2] == ["TRANSITION", "LOCATION"]
    assert GRAMMAR_ORDER[-2:] == ["REVELATION", "BEAT"]


def test_case_slot_template(vocab):
    assert len(vocab.slot_dims("amber_cipher")) == 11          # universal only
    assert len(vocab.slot_dims("attended_hour")) == 12         # + MEDICAL_TELL
    assert "MEDICAL_TELL" in vocab.slot_dims("attended_hour")


def test_legal_ids_are_case_and_dim_scoped(vocab):
    loc = vocab.legal_ids("amber_cipher", "LOCATION")
    assert vocab.encode("location:signal_box") in loc
    for tid in loc:
        assert vocab.decode(tid).startswith("location:")


def test_normalize_passes_canonical_and_rejects_unknown(vocab):
    # corpus has zero drift today (verified); normalize is a guard, not a fixer
    assert vocab.normalize("OBJECT_FOCUS", "object_focus:none") == "object_focus:none"
    assert vocab.normalize("TELL", "emotion:steady_hands") == "emotion:steady_hands"
    with pytest.raises(ValueError):
        vocab.normalize("LOCATION", "location:not_a_place")


def test_outcome_and_card_tokens(vocab):
    assert vocab.encode("<outcome:correct_voss>") >= 0
    assert vocab.encode("object:initialed_cufflink") in vocab.card_ids("amber_cipher")
    assert "correct_voss" in vocab.outcome_classes("amber_cipher")


def test_round_trip_dict(vocab):
    v2 = SceneVocab.from_dict(vocab.to_dict())
    assert v2.encode("<accuse>") == vocab.encode("<accuse>")
    assert v2.legal_ids("amber_cipher", "BEAT") == vocab.legal_ids("amber_cipher", "BEAT")
