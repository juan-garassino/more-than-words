"""Runtime engine for SceneLM (v3): the engine renders, measures, and reads.

No convergence boosts, no card forcing, no beat injection, no per-dim
temperatures, no runtime vocab wrapper. Grammar + constraints.json masks are
syntax; everything else is the model:

- ``step(card)``      — one investigation turn; returns (scene, convergence).
- ``accuse(token)``   — an accusation turn; the model narrates the
  confrontation scene, then its own boundary choice (continue vs <outcome:*>)
  decides whether the story ends. Near-misses are real: a wrong accusation can
  keep the story going, exactly as the near_miss trajectories teach.
- ``resolve()``       — force an outcome now (player quits / turn budget up).

Convergence is *measured*: cumulative authored attractor weight
(cases/<case>/tokens.json) of the tokens the model emits and the player plays.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch

from generator.constraints_compiler import ConstraintMask

TRAINER_ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = TRAINER_ROOT / "cases"
TEMPERATURE = 0.7


class AttractorMeter:
    """Measured convergence: cumulative authored attractor weight of tokens."""

    def __init__(self, case_id: str, case_dir: Path, scale: float = 1.0):
        self.scale = scale
        cards = json.loads((case_dir / "tokens.json").read_text())
        self._w = {t["id"]: t["attractor_weights"] for t in cards}
        self._conv = [0.0, 0.0, 0.0]

    def weights_for(self, token: str) -> Optional[List[float]]:
        if token in self._w:
            return self._w[token]
        if token.startswith("presence:with_"):
            name = token.removeprefix("presence:with_")
            for prefix in ("suspect:", "witness:"):
                if prefix + name in self._w:
                    return self._w[prefix + name]
        return None

    def observe(self, tokens: List[str]) -> List[float]:
        for t in tokens:
            w = self.weights_for(t)
            if w:
                self._conv = [c + self.scale * wi for c, wi in zip(self._conv, w)]
        return self.convergence

    @property
    def convergence(self) -> List[float]:
        return [max(0.0, min(1.0, c)) for c in self._conv]


class SceneLMEngine:
    def __init__(self, model, vocab, case_id: str, case_dir: Path,
                 seed: int = 0, conv_scale: float = 1.0):
        self.model, self.vocab, self.case_id = model.eval(), vocab, case_id
        self.case_dir = case_dir
        self.meter = AttractorMeter(case_id, case_dir, scale=conv_scale)
        self.gen = torch.Generator().manual_seed(seed)
        self.run_salt = str(seed)                  # composer per-run variant salt
        self.ids = torch.tensor([[vocab.encode("<bos>")]], dtype=torch.long)
        cjson = json.loads((case_dir / "constraints.json").read_text())
        token_classes = {t["id"]: t["token_class"]
                         for t in json.loads((case_dir / "tokens.json").read_text())}
        self.cmask = ConstraintMask(cjson, vocab.case_dim_vocab[case_id],
                                    token_class_map=token_classes)
        # game state (shape per constraints_compiler module docstring)
        self.prev_locations: List[str] = []
        self.visited: set = set()
        self.turn = 0
        self.last_card: Optional[str] = None
        self.ledger_path = TRAINER_ROOT / "outputs" / case_id / "ledger.json"

    @classmethod
    def load(cls, ckpt_path, seed: int = 0) -> "SceneLMEngine":
        from trainer.scene_lm import SceneLM
        model, vocab, ckpt = SceneLM.load(ckpt_path)
        case_id = ckpt["case_id"]
        scale = ckpt.get("extra", {}).get("conv_scale", 1.0)
        return cls(model, vocab, case_id, CASES_DIR / case_id, seed=seed,
                   conv_scale=scale)

    # ── state ────────────────────────────────────────────────────────────────
    def game_state(self) -> Dict:
        return {
            "previous_locations": list(self.prev_locations),
            "visited_locations": set(self.visited),
            "scene_index": self.turn - 1,
            "convergence_dims": self.meter.convergence,
            "game_turn": self.turn,
            "last_player_card": self.last_card,
        }

    def _observe_scene(self, played: str, scene: Dict[str, str]) -> List[float]:
        loc = scene.get("LOCATION")
        if loc and loc != "location:none":
            self.prev_locations.append(loc)
            self.visited.add(loc)
        return self.meter.observe([played] + list(scene.values()))

    # ── turns ────────────────────────────────────────────────────────────────
    def _append(self, tokens: List[str]) -> None:
        ids = torch.tensor([[self.vocab.encode(t) for t in tokens]], dtype=torch.long)
        self.ids = torch.cat([self.ids, ids], dim=1)

    def _generate_scene(self) -> Dict[str, str]:
        gs = self.game_state()
        return self.model.generate_scene(
            self.ids, self.case_id, self.vocab, temperature=TEMPERATURE,
            constraint_fn=lambda dim, partial:
                {self.vocab.encode(t)
                 for t in self.cmask.applicable_for_dim(dim, partial, gs)},
            generator=self.gen)

    def step(self, card: str) -> Tuple[Dict[str, str], List[float]]:
        self.turn += 1
        self.last_card = card
        self._append(["<card>", card, "<scene>"])
        scene = self._generate_scene()
        self._append([scene[d] for d in self.vocab.slot_dims(self.case_id)])
        conv = self._observe_scene(card, scene)
        return scene, conv

    def accuse(self, accused: str) -> Dict:
        """Accusation turn. The model narrates the confrontation, then decides
        at the boundary whether the story ends (outcome token) or continues."""
        self.turn += 1
        self.last_card = accused
        self._append(["<accuse>", accused, "<scene>"])
        scene = self._generate_scene()
        self._append([scene[d] for d in self.vocab.slot_dims(self.case_id)])
        conv = self._observe_scene(accused, scene)
        boundary = self.model.boundary_choice(self.ids, self.case_id, self.vocab,
                                              temperature=TEMPERATURE,
                                              generator=self.gen)
        if boundary.startswith("<outcome:"):
            outcome = boundary.removeprefix("<outcome:").removesuffix(">")
            ending = self._finish(outcome)
            return {"scene": scene, "conv": conv, "ended": True,
                    "outcome": outcome, "ending": ending}
        return {"scene": scene, "conv": conv, "ended": False,
                "outcome": None, "ending": None}

    def resolve(self) -> Tuple[str, Dict]:
        """Force an outcome now (player quits or the turn budget runs out)."""
        outcome = self.model.predict_outcome(self.ids, self.case_id, self.vocab)
        return outcome, self._finish(outcome)

    # ── endings + ledger ─────────────────────────────────────────────────────
    def _finish(self, outcome: str) -> Dict:
        self._append([f"<outcome:{outcome}>", "<eos>"])
        self._record_ledger(outcome)
        return self._pick_ending(outcome)

    def _pick_ending(self, outcome: str) -> Dict:
        """Hash-stable pick of an authored ending block matching the outcome."""
        candidates = []
        for f in sorted((self.case_dir / "trajectories").glob("*.json")):
            if f.name == "manifest.json":
                continue
            t = json.loads(f.read_text())
            if t.get("outcome") == outcome and t.get("ending"):
                candidates.append(t["ending"])
        if not candidates:
            return {"type": outcome}
        pick = hash(self.run_salt + outcome) % len(candidates)
        ending = dict(candidates[pick])
        ending.setdefault("type", outcome)
        return ending

    def _record_ledger(self, outcome: str) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        if self.ledger_path.exists():
            data = json.loads(self.ledger_path.read_text())
        data[outcome] = data.get(outcome, 0) + 1
        self.ledger_path.write_text(json.dumps(data, indent=1))

    def ledger_progress(self) -> Tuple[int, int]:
        data = (json.loads(self.ledger_path.read_text())
                if self.ledger_path.exists() else {})
        return len(data), len(self.vocab.outcome_classes(self.case_id))
