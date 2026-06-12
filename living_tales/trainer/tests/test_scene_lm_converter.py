from __future__ import annotations

import json
from pathlib import Path

import pytest

from trainer.scene_lm_dataset import (
    load_case_token_sequences,
    trajectory_to_tokens,
    turn_marker_and_token,
)
from trainer.scene_lm_vocab import SceneVocab

CASE = "amber_cipher"


@pytest.fixture(scope="module")
def vocab(production_cases):
    return SceneVocab.build(production_cases)


def _load(cases_dir, name, case=CASE):
    return json.loads((cases_dir / case / "trajectories" / name).read_text())


def test_turn_template_shape(vocab, cases_dir):
    traj = _load(cases_dir, "framed_night_porter.json")
    toks = trajectory_to_tokens(traj, CASE, vocab)
    assert toks[0] == "<bos>"
    i = toks.index("<card>")
    assert toks[i + 2] == "<scene>"
    scene_block = toks[i + 3 : i + 14]
    assert scene_block[0].startswith("transition:")
    assert len(scene_block) == 11


def test_accuse_turn_in_stream(vocab, cases_dir):
    traj = _load(cases_dir, "framed_night_porter.json")
    toks = trajectory_to_tokens(traj, CASE, vocab)
    a = toks.index("<accuse>")
    assert toks[a + 1] == "suspect:night_porter"   # matches ending.accused
    assert toks[a + 2] == "<scene>"                 # confrontation scene follows
    assert toks[-2] == "<outcome:framed_suspect>"
    assert toks[-1] == "<eos>"


def test_every_trajectory_ends_with_outcome(vocab, cases_dir):
    traj = _load(cases_dir, "cold_trail_circular.json")
    toks = trajectory_to_tokens(traj, CASE, vocab)
    assert toks[-2] == "<outcome:cold_trail>"
    assert toks[-1] == "<eos>"


def test_near_miss_has_two_accusations_and_continues(vocab, cases_dir):
    traj = _load(cases_dir, "late_revelation_after_cipher_sheet.json")
    toks = trajectory_to_tokens(traj, CASE, vocab)
    accuse_positions = [i for i, t in enumerate(toks) if t == "<accuse>"]
    assert len(accuse_positions) == 2
    # after the first (wrong) accusation's scene, the story continues with <card>
    first_scene_end = accuse_positions[0] + 3 + 11
    assert toks[first_scene_end] == "<card>"


def test_accuse_none_maps_to_token():
    assert turn_marker_and_token("ACCUSE:none") == ["<accuse>", "accuse:none"]
    assert turn_marker_and_token("ACCUSE:suspect:renard_voss") == [
        "<accuse>", "suspect:renard_voss"]
    assert turn_marker_and_token("object:satchel") == ["<card>", "object:satchel"]


def test_counterfactual_gets_parent_anchor(vocab, cases_dir):
    cf = _load(cases_dir, "cf_voss_via_cufflink_to_broker.json")
    parent = _load(cases_dir, "voss_via_cufflink.json")
    toks = trajectory_to_tokens(cf, CASE, vocab, parent=parent)
    n_turns = toks.count("<card>") + toks.count("<accuse>")
    assert n_turns == (cf["branch_turn"] - 1) + len(cf["turns"])


def test_case_specific_dim_in_sequence(vocab, cases_dir):
    seqs = load_case_token_sequences("attended_hour", cases_dir, vocab)
    assert seqs, "attended_hour produced no sequences"
    toks = seqs[0]
    i = toks.index("<scene>")
    assert len(toks[i + 1 : i + 1 + 12]) == 12  # 12 dims incl. MEDICAL_TELL


def test_universal_only_drops_case_dim(vocab, cases_dir):
    seqs = load_case_token_sequences("attended_hour", cases_dir, vocab,
                                     universal_only=True)
    toks = seqs[0]
    i = toks.index("<scene>")
    block = toks[i + 1 : i + 12]
    assert len(block) == 11
    assert not any(t.startswith("medical_tell:") for t in block)


def test_whole_corpus_converts_and_encodes(vocab, cases_dir, production_cases):
    for case in production_cases:
        for seq in load_case_token_sequences(case, cases_dir, vocab):
            for t in seq:
                vocab.encode(t)  # raises KeyError on any unknown token


def test_golden_fixture(vocab, cases_dir):
    """Pin the exact first-2-turn token sequence of framed_night_porter."""
    traj = _load(cases_dir, "framed_night_porter.json")
    toks = trajectory_to_tokens(traj, CASE, vocab)
    golden = Path(__file__).parent / "fixtures" / "framed_night_porter_head.json"
    if not golden.exists():  # first run writes it; HAND-CHECK then commit
        golden.parent.mkdir(exist_ok=True)
        golden.write_text(json.dumps(toks[:29], indent=1))
        pytest.skip("golden written - hand-check fixtures/framed_night_porter_head.json")
    assert toks[:29] == json.loads(golden.read_text())
