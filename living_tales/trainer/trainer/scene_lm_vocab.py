"""Symbolic vocabulary + per-case grammar for SceneLM (v3).

The union vocab spans all production cases (stable ids — the base model is
pretrained on it); each case gets a grammar: a slot template (dim order) and
per-dim legal-id sets used as logit masks at train and inference time.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

TRAINER_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = TRAINER_ROOT / "cases"

SPECIALS = ["<pad>", "<bos>", "<eos>", "<card>", "<scene>", "<accuse>"]

# TRANSITION precedes LOCATION: constraints.json rules condition LOCATION on
# the already-emitted TRANSITION (see constraints_compiler.py rule direction).
GRAMMAR_ORDER = [
    "TRANSITION", "LOCATION", "PRESENCE", "STANCE", "CAUSE", "ACTION",
    "OBJECT_FOCUS", "TELL", "ATMOSPHERE", "REVELATION", "BEAT",
]
CASE_DIM_SLOT_AFTER = "TELL"  # MEDICAL_TELL / ART_TELL insert here

# Known prefix drift in hand-authored trajectories -> canonical dim-vocab id.
# Corpus scan 2026-06-12: zero drift across all 3 production cases; this table
# exists so future drift gets one canonical fix-point (validator checks it too).
ALIASES: Dict[str, str] = {}


class SceneVocab:
    """Token <-> id mapping plus per-case grammar, cards and outcome classes.

    Parameters
    ----------
    id_to_token : list of str
        Token strings; the list index is the id.
    case_dims : dict
        ``case_id -> slot order`` (dim names in grammar order).
    case_dim_vocab : dict
        ``case_id -> {dim: [legal token strings]}``.
    case_cards : dict
        ``case_id -> sorted playable card tokens``.
    case_outcomes : dict
        ``case_id -> sorted outcome class names`` (without ``<outcome:>``).
    """

    def __init__(
        self,
        id_to_token: List[str],
        case_dims: Dict[str, List[str]],
        case_dim_vocab: Dict[str, Dict[str, List[str]]],
        case_cards: Dict[str, List[str]],
        case_outcomes: Dict[str, List[str]],
    ):
        self.id_to_token = id_to_token
        self.token_to_id = {t: i for i, t in enumerate(id_to_token)}
        self.case_dims = case_dims
        self.case_dim_vocab = case_dim_vocab
        self.case_cards = case_cards
        self.case_outcomes = case_outcomes

    # -- construction ----------------------------------------------------
    @classmethod
    def build(cls, case_ids: List[str], cases_dir: Optional[Path] = None) -> "SceneVocab":
        """Build the union vocab from packed case directories.

        Reads ``dimensions.json``, ``tokens.json`` and ``trajectories/*.json``
        under ``cases_dir/<case_id>`` (default: ``trainer/cases``). Cases are
        processed in sorted order so ids are stable for a given case set.
        """
        cases_dir = cases_dir or CASES_DIR
        tokens: List[str] = list(SPECIALS)
        seen = set(tokens)
        case_dims: Dict[str, List[str]] = {}
        case_dim_vocab: Dict[str, Dict[str, List[str]]] = {}
        case_cards: Dict[str, List[str]] = {}
        case_outcomes: Dict[str, List[str]] = {}

        def add(t: str) -> None:
            if t not in seen:
                seen.add(t)
                tokens.append(t)

        for cid in sorted(case_ids):
            cdir = cases_dir / cid
            dims_json = json.loads((cdir / "dimensions.json").read_text())
            dim_vocab: Dict[str, List[str]] = {}
            slots = list(GRAMMAR_ORDER)
            for dim in dims_json["dimensions"]:
                name, vocab = dim["name"], list(dim["vocab"])
                dim_vocab[name] = vocab
                for t in vocab:
                    add(t)
                if name not in GRAMMAR_ORDER:  # case-specific dim
                    slots.insert(slots.index(CASE_DIM_SLOT_AFTER) + 1, name)
            # cards = tokens.json union cards actually played in trajectories
            # (hand-authored data plays a handful of ids beyond tokens.json,
            # e.g. modifier:debt_pressure; ACCUSE:* turns map to <accuse> + the
            # stripped accused token, with ACCUSE:none -> accuse:none).
            cards = {t["id"] for t in json.loads((cdir / "tokens.json").read_text())}
            outcomes = set()
            for f in sorted((cdir / "trajectories").glob("*.json")):
                if f.name == "manifest.json":
                    continue
                traj = json.loads(f.read_text())
                outcomes.add(traj["outcome"])
                for turn in traj.get("turns", []):
                    pc = turn["player_card"]
                    if pc.startswith("ACCUSE:"):
                        stripped = pc.removeprefix("ACCUSE:")
                        add("accuse:none" if stripped == "none" else stripped)
                    else:
                        cards.add(pc)
            cards = sorted(cards)
            for c in cards:
                add(c)
            outcomes = sorted(outcomes)
            for o in outcomes:
                add(f"<outcome:{o}>")
            case_dims[cid] = slots
            case_dim_vocab[cid] = dim_vocab
            case_cards[cid] = cards
            case_outcomes[cid] = outcomes
        return cls(tokens, case_dims, case_dim_vocab, case_cards, case_outcomes)

    # -- core API ----------------------------------------------------------
    def encode(self, token: str) -> int:
        """Return the id of ``token`` (KeyError if unknown)."""
        return self.token_to_id[token]

    def decode(self, idx: int) -> str:
        """Return the token string for id ``idx``."""
        return self.id_to_token[idx]

    def __len__(self) -> int:
        return len(self.id_to_token)

    def slot_dims(self, case_id: str) -> List[str]:
        """Dim names of one scene, in emission order, for ``case_id``."""
        return self.case_dims[case_id]

    def legal_ids(self, case_id: str, dim: str) -> List[int]:
        """Sorted ids of the tokens legal in slot ``dim`` of ``case_id``."""
        return sorted(self.encode(t) for t in self.case_dim_vocab[case_id][dim])

    def card_ids(self, case_id: str) -> set:
        """Set of ids of the cards playable in ``case_id``."""
        return {self.encode(c) for c in self.case_cards[case_id]}

    def outcome_classes(self, case_id: str) -> List[str]:
        """Outcome class names for ``case_id`` (no ``<outcome:>`` wrapper)."""
        return self.case_outcomes[case_id]

    def outcome_ids(self, case_id: str) -> List[int]:
        """Ids of the ``<outcome:*>`` tokens for ``case_id``, in class order."""
        return [self.encode(f"<outcome:{o}>") for o in self.case_outcomes[case_id]]

    def normalize(self, dim: str, raw: str, case_id: str = "amber_cipher") -> str:
        """Map ``raw`` through ``ALIASES`` and check it is legal for ``dim``.

        Raises ValueError if the token is not in the case's vocab for ``dim``.
        """
        token = ALIASES.get(raw, raw)
        if token not in self.case_dim_vocab[case_id][dim]:
            raise ValueError(f"{raw!r} not in {case_id}/{dim} vocab")
        return token

    # -- checkpoint baking ---------------------------------------------------
    def to_dict(self) -> Dict:
        """JSON/pickle-friendly dict used to bake the vocab into checkpoints."""
        return {
            "id_to_token": self.id_to_token,
            "case_dims": self.case_dims,
            "case_dim_vocab": self.case_dim_vocab,
            "case_cards": self.case_cards,
            "case_outcomes": self.case_outcomes,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "SceneVocab":
        """Inverse of :meth:`to_dict`."""
        return cls(d["id_to_token"], d["case_dims"], d["case_dim_vocab"],
                   d["case_cards"], d["case_outcomes"])
