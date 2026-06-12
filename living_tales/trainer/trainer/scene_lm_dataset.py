"""Trajectory JSON -> flat symbolic token sequences + Dataset for SceneLM (v3).

A play session is one string:

  <bos>
  <card>   {card}          <scene> {N dim tokens}     # normal turn
  <accuse> {accused token} <scene> {N dim tokens}     # accusation turn
  ...
  <outcome:cls> <eos>

Accusations are in-stream turns (the hand-authored data encodes them as
ACCUSE:* player cards with full confrontation scenes; near_miss trajectories
continue playing after a wrong accusation). The outcome token terminates every
trajectory — at runtime the model's own boundary choice between continuing and
an <outcome:*> token decides whether an accusation ends the story.
Conversion is fully mechanical from the trajectory files.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from trainer.scene_lm_vocab import GRAMMAR_ORDER, SceneVocab

TRAINER_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = TRAINER_ROOT / "cases"


def turn_marker_and_token(player_card: str) -> List[str]:
    """Map a trajectory player_card to its (marker, token) pair."""
    if player_card.startswith("ACCUSE:"):
        stripped = player_card.removeprefix("ACCUSE:")
        return ["<accuse>", "accuse:none" if stripped == "none" else stripped]
    return ["<card>", player_card]


def trajectory_to_tokens(
    traj: Dict,
    case_id: str,
    vocab: SceneVocab,
    parent: Optional[Dict] = None,
    universal_only: bool = False,
) -> List[str]:
    """Flatten one trajectory (optionally a cf-branch with its parent anchor)."""
    slots = vocab.slot_dims(case_id)
    if universal_only:
        slots = [d for d in slots if d in GRAMMAR_ORDER]
    toks: List[str] = ["<bos>"]

    def emit_turn(turn: Dict) -> None:
        toks.extend(turn_marker_and_token(turn["player_card"]))
        toks.append("<scene>")
        for dim in slots:
            toks.append(vocab.normalize(dim, turn["scene"][dim], case_id))

    if parent is not None:  # counterfactual: anchor = parent turns before branch
        branch_turn = traj["branch_turn"]
        for t in parent["turns"]:
            if t["turn"] >= branch_turn:
                break
            emit_turn(t)
    for t in traj["turns"]:
        emit_turn(t)

    toks.append(f"<outcome:{traj['outcome']}>")
    toks.append("<eos>")
    return toks


def load_case_token_sequences(
    case_id: str,
    cases_dir: Path,
    vocab: SceneVocab,
    universal_only: bool = False,
) -> List[List[str]]:
    tdir = cases_dir / case_id / "trajectories"
    by_id: Dict[str, Dict] = {}
    for f in sorted(tdir.glob("*.json")):
        if f.name == "manifest.json":
            continue
        traj = json.loads(f.read_text())
        by_id[traj["trajectory_id"]] = traj
    seqs = []
    for tid, traj in by_id.items():
        parent = by_id.get(traj["branch_of"]) if traj.get("branch_of") else None
        seqs.append(trajectory_to_tokens(traj, case_id, vocab, parent=parent,
                                         universal_only=universal_only))
    return seqs
