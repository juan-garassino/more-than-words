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
) -> List[List[str]]:  # noqa: D103 — see module docstring
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


# ── Dataset ──────────────────────────────────────────────────────────────────

import math
import random
from collections import Counter

import torch
from torch.utils.data import Dataset

# card-id prefix -> dims whose loss is doubled on the following scene
BINDING_MAP = {
    "object": ["OBJECT_FOCUS"],
    "suspect": ["PRESENCE"],
    "witness": ["PRESENCE"],
    "location": ["TRANSITION", "LOCATION"],
    "travel": ["TRANSITION", "LOCATION"],
    "motive": ["ACTION", "OBJECT_FOCUS"],
    "event": ["ACTION", "OBJECT_FOCUS"],
    "emotion": ["ACTION", "OBJECT_FOCUS"],
    "time": ["ACTION", "OBJECT_FOCUS"],
    "modifier": ["ACTION", "OBJECT_FOCUS"],
    "action": ["ACTION"],
}
BINDING_WEIGHT = 2.0
COLLAPSED_DIMS = ["REVELATION", "TRANSITION", "BEAT"]
CLASS_BALANCE_CAP = 5.0


def _stratified_split(examples, split, holdout_frac):
    """Deterministic train/holdout split stratified by (case, outcome class).
    Classes with <3 sequences stay whole in train — the outcome head barely
    sees them as it is; load order (sorted filenames) makes this stable."""
    by_class: Dict[tuple, list] = {}
    for ex in examples:
        outcome = next((t for t in ex[1] if t.startswith("<outcome:")),
                       "<outcome:none>")
        by_class.setdefault((ex[0], outcome), []).append(ex)
    train, hold = [], []
    for key in sorted(by_class):
        group = by_class[key]
        if len(group) < 3:
            train.extend(group)
            continue
        k = max(1, round(len(group) * holdout_frac))
        hold.extend(group[:k])
        train.extend(group[k:])
    return hold if split == "holdout" else train


class SceneLMDataset(Dataset):
    """Flat next-token examples with loss masks, binding weights, augmentation.

    Loss policy: the player's tokens (card after <card>, accused token after
    <accuse>) are input-only. Boundary markers themselves stay supervised —
    the model's calibrated choice between <card>/<accuse>/<outcome:*> at turn
    boundaries is what lets an accusation end (or not end) the story at runtime.
    """

    def __init__(self, case_ids, vocab, universal_only=False,
                 augment_truncate=True, seed=0, cases_dir=None,
                 split="all", holdout_frac=0.1):
        self.vocab = vocab
        self.universal_only = universal_only
        self.augment_truncate = augment_truncate
        self.rng = random.Random(seed)
        self.examples = []           # (case_id, token_strs)
        for cid in case_ids:
            for seq in load_case_token_sequences(cid, cases_dir or CASES_DIR,
                                                 vocab, universal_only=universal_only):
                self.examples.append((cid, seq))
        if split != "all":
            self.examples = _stratified_split(self.examples, split, holdout_frac)

    def slot_index(self, case_id: str, dim: str) -> int:
        return self._slots(case_id).index(dim)

    def _slots(self, case_id: str) -> List[str]:
        slots = self.vocab.slot_dims(case_id)
        if self.universal_only:
            slots = [d for d in slots if d in GRAMMAR_ORDER]
        return slots

    def _turn_len(self, case_id: str) -> int:
        return 3 + len(self._slots(case_id))   # marker + token + <scene> + dims

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        case_id, toks = self.examples[i]
        toks = list(toks)
        tl = self._turn_len(case_id)
        if self.augment_truncate and self.rng.random() < 0.5:
            n_turns = sum(1 for t in toks if t in ("<card>", "<accuse>"))
            if n_turns > 4:
                keep = self.rng.randint(3, n_turns - 1)
                toks = toks[: 1 + keep * tl]            # <bos> + whole turns
        ids = torch.tensor([self.vocab.encode(t) for t in toks], dtype=torch.long)
        loss_mask = torch.ones_like(ids)
        loss_weight = torch.ones(ids.shape, dtype=torch.float)
        loss_mask[0] = 0                                # <bos> never a target
        slots = self._slots(case_id)
        j = 1
        while j < len(toks):
            if toks[j] in ("<card>", "<accuse>"):
                loss_mask[j + 1] = 0                     # player's token: input-only
                if toks[j] == "<card>":
                    card = toks[j + 1]
                    bound = BINDING_MAP.get(card.split(":")[0], [])
                    for k, dim in enumerate(slots):
                        if dim in bound and j + 3 + k < len(toks):
                            loss_weight[j + 3 + k] = BINDING_WEIGHT
                j += tl
            else:
                j += 1
        return {"ids": ids, "loss_mask": loss_mask, "loss_weight": loss_weight}

    def class_balance_weights(self) -> torch.Tensor:
        """Inverse-sqrt frequency weights (capped) for collapsed-dim tokens."""
        counts: Counter = Counter()
        collapsed_ids = set()
        for cid in {c for c, _ in self.examples}:
            for dim in COLLAPSED_DIMS:
                collapsed_ids.update(self.vocab.legal_ids(cid, dim))
        for _, toks in self.examples:
            for t in toks:
                tid = self.vocab.encode(t)
                if tid in collapsed_ids:
                    counts[tid] += 1
        w = torch.ones(len(self.vocab))
        if counts:
            med = sorted(counts.values())[len(counts) // 2]
            for tid in collapsed_ids:
                c = max(1, counts.get(tid, 1))
                w[tid] = min(CLASS_BALANCE_CAP, max(1.0, math.sqrt(med / c)))
        return w

    def collate(self, batch):
        n = max(len(b["ids"]) for b in batch)
        pad = self.vocab.encode("<pad>")
        out = {
            "ids": torch.full((len(batch), n), pad, dtype=torch.long),
            "loss_mask": torch.zeros((len(batch), n), dtype=torch.long),
            "loss_weight": torch.ones((len(batch), n), dtype=torch.float),
        }
        for i, b in enumerate(batch):
            L = len(b["ids"])
            out["ids"][i, :L] = b["ids"]
            out["loss_mask"][i, :L] = b["loss_mask"]
            out["loss_weight"][i, :L] = b["loss_weight"]
        return out
