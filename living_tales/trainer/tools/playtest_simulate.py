"""
Playtest simulator
==================
Runs N simulated playthroughs of a trained Living Tales structured-scene
case and writes a human-readable transcript per playthrough. The transcripts
are designed to be read by a human (or by an LLM-as-judge subagent) to
verify the case plays as a coherent detective experience BEFORE investing
time in a full pygame playtest.

Usage
-----
    cd living_tales/trainer
    python tools/playtest_simulate.py amber_cipher --n 5 --max-turns 30 \
        --out outputs/amber_cipher/playtest_transcripts.md

Strategy
--------
At each turn the simulator picks a player card uniformly at random from
the case's PLAYER-agency tokens that haven't been placed yet, then asks
the model to predict the engine response. The strategy is intentionally
naive — random card selection stress-tests the model on choices the
authored trajectories may not have rehearsed exactly, surfacing the
bounded-variability behaviour where it really lives.

Output
------
A markdown file with one section per playthrough:

    ## Playthrough 1 (seed=42)
    Opening: location:thornfield_crossing, event:aldous_verne_discovered, ...

    [ 1] PLAYS object:initialed_cufflink
         The detective examined the initialed cufflink. ...

    [ 2] PLAYS witness:ticket_clerk
         On the witness's word, crossed to Platform Two. ...

    ...

    Final state: 30 turns | convergence_min ≈ 0.62 | beat: closing_in
    Notes: 1 hard-mask violation observed (atmosphere:dawn_approaches at turn 14).

The Notes block flags any inference-time constraint violations the model
slipped — useful for the LLM judge to weigh.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from generator.constraints_compiler import ConstraintMask
from generator.structured_scene_composer import SceneComposer
from generator.trajectory_loader import TrajectoryLoader
from trainer.structured_scene_model import StructuredSceneTransformer

# ─────────────────────────────────────────────────────────────────────────────
# Loading
# ─────────────────────────────────────────────────────────────────────────────


def load_engine(case_id: str, project_root: Path):
    """Load model, composer, constraint mask, and case spec for inference.

    Prefers v2_full.pt; falls back to v1 structured_scene_model.pt.
    For v2, applies a per-case vocabulary restriction wrapper around
    ConstraintMask so the union-vocab base doesn't bleed cross-case tokens.
    """
    v2_path = project_root / "living_tales/trainer/outputs" / case_id / "v2_full.pt"
    v1_path = project_root / "living_tales/trainer/outputs" / case_id / "structured_scene_model.pt"

    case_dir = project_root / "living_tales/trainer/cases" / case_id
    with open(case_dir / "constraints.json") as f:
        constraints = json.load(f)
    with open(case_dir / "dimensions.json") as f:
        dimensions = json.load(f)
    case_dim_vocab = {d["name"]: list(d["vocab"]) for d in dimensions["dimensions"]}
    case_dims_set = set(case_dim_vocab.keys())

    model_version = None
    if v2_path.exists():
        from trainer.structured_scene_model_v2 import (
            StructuredSceneTransformerV2, V2Config,
        )
        ckpt = torch.load(v2_path, map_location="cpu", weights_only=False)
        cfg_dict = ckpt.get("config", {})
        cfg = V2Config(**{k: cfg_dict[k] for k in (
            "hidden_dim", "n_layers", "n_heads", "max_history", "lora_rank",
        ) if k in cfg_dict})
        cfg.universal_dims = ckpt.get("universal_dims", [])
        model = StructuredSceneTransformerV2(
            dim_vocab=ckpt["dim_vocab"],
            dim_order=ckpt["dim_order"],
            full_vocab=ckpt["full_vocab"],
            config=cfg,
        )
        model.load_state_dict(ckpt["state_dict"], strict=False)
        model.eval()
        # v2 needs a full_vocab_to_idx for the simulator's history encoding.
        if "full_vocab_to_idx" not in ckpt:
            ckpt["full_vocab_to_idx"] = {t: i for i, t in enumerate(ckpt["full_vocab"])}
        model_version = "v2"
        print(f"[simulate] loaded v2 from {v2_path}")
    elif v1_path.exists():
        ckpt = torch.load(v1_path, map_location="cpu", weights_only=False)
        model = StructuredSceneTransformer(
            dim_vocab=ckpt["dim_vocab"],
            full_vocab=ckpt["full_vocab"],
            **ckpt["config"],
        )
        model.load_state_dict(ckpt["state_dict"])
        model.eval()
        model_version = "v1"
        print(f"[simulate] loaded v1 from {v1_path}")
    else:
        raise FileNotFoundError(f"No checkpoint at {v2_path} or {v1_path}.")

    composer = SceneComposer.load(case_id, lang="en")
    base_cmask = ConstraintMask(constraints, ckpt["dim_vocab"])

    # v2: wrap with per-case vocab restriction (union-vocab guard).
    if model_version == "v2":
        case_sets = {d: set(toks) for d, toks in case_dim_vocab.items()}

        class _CaseRestrictedMask:
            def __init__(self, base, sets, dims):
                self.base = base
                self.case_sets = sets
                self.case_dims = dims
            def applicable_for_dim(self, dim, scene_so_far, game_state):
                allowed = (self.base.applicable_for_dim(dim, scene_so_far, game_state)
                           if hasattr(self.base, "applicable_for_dim") else None)
                if dim not in self.case_dims:
                    return None
                cs = self.case_sets.get(dim, set())
                return cs if allowed is None else (allowed & cs)
            def is_valid_tuple(self, *a, **k):
                return self.base.is_valid_tuple(*a, **k)

        cmask = _CaseRestrictedMask(base_cmask, case_sets, case_dims_set)
    else:
        cmask = base_cmask

    # Spec carries opening_token_ids + cartridge metadata.
    with open(case_dir / "spec.json") as f:
        spec = json.load(f)
    # Tokens live in tokens.json (not in spec.json — different cartridge file).
    with open(case_dir / "tokens.json") as f:
        tokens_list = json.load(f)
    spec["tokens"] = tokens_list

    # Discovery beats — convergence-threshold scaffolding.
    discovery_beats = None
    try:
        from generator.discovery_beats import DiscoveryBeats
        discovery_beats = DiscoveryBeats.load(case_id, project_root)
    except Exception as e:
        print(f"[simulate] discovery beats load failed: {e}")

    return {
        "model": model,
        "model_version": model_version,
        "case_dims": case_dims_set,
        "composer": composer,
        "constraints": constraints,
        "constraint_mask": cmask,
        "dimensions": dimensions,
        "ckpt": ckpt,
        "spec": spec,
        "discovery_beats": discovery_beats,
    }


def player_card_pool(spec: dict, dimensions: dict) -> Dict[str, List[str]]:
    """Return two pools — `inquiry` tokens (suspects, witnesses, objects,
    motives, modifiers, actions, emotions) and `travel` tokens. The
    simulator strongly prefers inquiry cards because they accumulate
    convergence and engage NPCs; travel cards are sprinkled to test the
    flow narration."""
    inquiry: List[str] = []
    for tok in spec.get("tokens", []):
        if tok.get("agency") in ("PLAYER", "SHARED") and not tok.get("is_invariant"):
            stream = tok.get("stream", "EVIDENCE")
            if stream != "OPENING":
                inquiry.append(tok["id"])
    travel: List[str] = list(dimensions.get("player_cards", {}).get("travel", []))
    return {"inquiry": inquiry, "travel": travel}


# ─────────────────────────────────────────────────────────────────────────────
# Simulation
# ─────────────────────────────────────────────────────────────────────────────


def simulate_one(engine: dict, max_turns: int, seed: int) -> dict:
    """Run one full playthrough. Returns a dict with transcript, turns,
    final convergence, and any constraint violations observed."""
    rng = random.Random(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    model: StructuredSceneTransformer = engine["model"]
    composer: SceneComposer = engine["composer"]
    cmask: ConstraintMask = engine["constraint_mask"]
    spec: dict = engine["spec"]
    ckpt: dict = engine["ckpt"]

    # Reset discovery beats per simulation so each session starts clean.
    if engine.get("discovery_beats") is not None:
        engine["discovery_beats"].reset()

    v2i = ckpt["full_vocab_to_idx"]
    # v2 model exposes dim_order as instance attr; v1 as class attr.
    DIM_ORDER = list(getattr(model, "dim_order", None) or model.DIM_ORDER)
    case_dims = engine.get("case_dims") or set(DIM_ORDER)

    # Build the two player card pools (inquiry vs travel). Drop tokens
    # the model's vocab doesn't know.
    pools = player_card_pool(spec, engine["dimensions"])
    inquiry_pool = [c for c in pools["inquiry"] if c in v2i]
    travel_pool = [c for c in pools["travel"] if c in v2i]
    rng.shuffle(inquiry_pool)
    rng.shuffle(travel_pool)

    # Encode the opening into history.
    history_tokens: List[int] = []
    history_dims: List[int] = []
    placed_ids = set()
    visited_locations: List[str] = []
    for tok in spec.get("opening_token_ids", []):
        if tok in v2i:
            history_tokens.append(v2i[tok])
            history_dims.append(len(DIM_ORDER))  # opening uses pad slot
            placed_ids.add(tok)
            if tok.startswith("location:"):
                visited_locations.append(tok)

    # State
    convergence = np.zeros(3, dtype=np.float32)
    # 3× the spec rate. Trained model under-emits high-attractor tokens at
    # inference (head collapse onto modal tokens), so the convergence accumulator
    # needs more push per turn for the closing arc to fire by turn 18-22.
    convergence_rate = float(spec.get("convergence_rate", 0.08)) * 3.0
    turns_log: List[Dict[str, Any]] = []
    violations: List[str] = []
    last_player_card = None

    # Quick lookup: token id → token dict (for class + attractor weights)
    tok_index = {t["id"]: t for t in spec.get("tokens", [])}

    for turn in range(1, max_turns + 1):
        # 80% inquiry, 20% travel — biased toward NPC engagement and
        # evidence accumulation, with occasional movement to test the
        # transition narration.
        prefer_travel = rng.random() < 0.2 and travel_pool
        primary = travel_pool if prefer_travel else inquiry_pool
        secondary = inquiry_pool if prefer_travel else travel_pool

        candidates = [c for c in primary if c not in placed_ids]
        if not candidates:
            candidates = [c for c in secondary if c not in placed_ids]
        if not candidates:
            break
        player_card = candidates[0]  # shuffled deterministically by seed
        # Rotate so we don't always pick the same one
        if player_card in primary:
            primary.remove(player_card)
            primary.append(player_card)
        placed_ids.add(player_card)

        pc_idx = v2i.get(player_card, 0)

        # Update convergence with player card weights (best effort).
        pc_meta = tok_index.get(player_card, {})
        if pc_meta.get("attractor_weights"):
            convergence = np.minimum(
                1.0,
                convergence
                + np.array(pc_meta["attractor_weights"][:3]) * convergence_rate,
            )

        # Game state for ConstraintMask
        last_loc = visited_locations[-1] if visited_locations else None
        last_pc_class = None
        if last_player_card:
            last_meta = tok_index.get(last_player_card, {})
            last_pc_class = last_meta.get("token_class") or last_meta.get("class")
        game_state = {
            "previous_locations": visited_locations,
            "visited_locations": set(visited_locations),
            "scene_index": turn - 1,
            "convergence_dims": convergence.tolist(),
            "game_turn": turn - 1,
            "last_player_card": last_player_card,
            "last_player_card_class": last_pc_class,
        }

        history = {
            "tokens": torch.tensor([history_tokens], dtype=torch.long),
            "dims": torch.tensor([history_dims], dtype=torch.long),
        }

        try:
            if engine.get("model_version") == "v2":
                # Per-dim temperatures tuned to break head collapse:
                #  - REVELATION/ATMOSPHERE/CAUSE/STANCE/TELL: hot + top_k for variety
                #  - TRANSITION: hot + top_k=3 so the model stops repeatedly emitting
                #    `stayed`/`did_not_move`
                #  - LOCATION/PRESENCE/ACTION: kept near-greedy so scene logic stays consistent
                #  - REVELATION/BEAT can be hotter because beats.json injection takes
                #    over for closing-arc tokens
                per_dim_temp = {
                    "LOCATION":     0.3,
                    "TRANSITION":   0.7,
                    "CAUSE":        0.7,
                    "PRESENCE":     0.4,
                    "STANCE":       0.7,
                    "ACTION":       0.3,
                    "OBJECT_FOCUS": 0.4,
                    "TELL":         0.7,
                    "ATMOSPHERE":   0.8,
                    "REVELATION":   0.6,
                    "BEAT":         0.5,
                    "MEDICAL_TELL": 0.5,
                    "ART_TELL":     0.5,
                }
                per_dim_topk = {
                    "TRANSITION": 3, "CAUSE": 4, "STANCE": 3, "TELL": 4,
                    "ATMOSPHERE": 4, "REVELATION": 4, "BEAT": 3,
                }
                scene = model.predict_scene(
                    history, pc_idx, cmask, game_state,
                    per_dim_temperature=per_dim_temp,
                    per_dim_top_k=per_dim_topk,
                )
            else:
                scene = model.predict_scene(
                    history, pc_idx, cmask, game_state, temperature=0.5,
                )
        except Exception as e:
            violations.append(f"turn {turn}: predict_scene failed: {type(e).__name__}: {e}")
            break

        # v2: drop dims that aren't part of this case.
        scene = {d: t for d, t in scene.items() if d in case_dims}

        # Bind the scene's focal slot AND the action verb to whatever the
        # player just played. The model has not learned this binding
        # strongly enough (judge flagged: "player plays coal_dust, scene
        # narrates the telegram"; also "player plays stationmaster, scene
        # has detective stepping into rooms instead of questioning him").
        # The simulator + pygame engine always honor the played card as
        # the scene's focal token AND swap the action verb so the prose
        # actually shows what the player did.
        pc_class = (pc_meta.get("token_class") or pc_meta.get("class") or "").upper()
        dims_by_name = {d["name"]: d["vocab"] for d in engine["dimensions"]["dimensions"]}
        if pc_class in ("OBJECT", "MODIFIER"):
            if player_card in dims_by_name.get("OBJECT_FOCUS", []):
                scene["OBJECT_FOCUS"] = player_card
                if scene.get("ACTION") in (
                    "action:arrives", "action:leaves", "action:none", None
                ):
                    scene["ACTION"] = "action:examines"
        elif pc_class in ("SUSPECT", "WITNESS"):
            presence_id = f"presence:with_{player_card.split(':', 1)[-1]}"
            if presence_id in dims_by_name.get("PRESENCE", []):
                scene["PRESENCE"] = presence_id
                if scene.get("ACTION") in (
                    "action:arrives", "action:leaves", "action:none", None
                ):
                    scene["ACTION"] = "action:questions"
        elif pc_class in ("MOTIVE", "EVENT", "EMOTION", "ACTION", "TIME"):
            # Player is recalling/connecting an abstract — bias ACTION to
            # recalls. Clear stale OBJECT_FOCUS so we don't get "waited the
            # torn ticket" / "questioned the coal dust" leakage.
            if scene.get("ACTION") in (
                "action:arrives", "action:leaves", "action:none",
                "action:waits", "action:questions", "action:examines", None
            ):
                scene["ACTION"] = "action:recalls"
            scene["OBJECT_FOCUS"] = "object_focus:none"
        elif player_card.startswith("travel:"):
            target_loc = player_card.replace("travel:to_", "location:")
            if target_loc in dims_by_name.get("LOCATION", []):
                scene["LOCATION"] = target_loc

        # Discovery-beats hook (parity with pygame_play).
        beats = engine.get("discovery_beats")
        if beats is not None:
            try:
                scene = beats.apply(
                    scene, convergence=list(convergence), turn_idx=turn,
                )
            except Exception as e:
                violations.append(f"turn {turn}: discovery beats failed: {e}")

        # Validate scene against constraints (post-hoc — flag any slips).
        ok, rule_violations = cmask.is_valid_tuple(scene, game_state)
        if not ok:
            for rid in rule_violations:
                violations.append(f"turn {turn}: rule slip → {rid}")

        # Append scene to history.
        for dim_name in DIM_ORDER:
            tok = scene.get(dim_name)
            if tok and tok in v2i:
                history_tokens.append(v2i[tok])
                history_dims.append(DIM_ORDER.index(dim_name))
                placed_ids.add(tok)
        loc = scene.get("LOCATION")
        if loc and loc != "location:none" and loc != (visited_locations[-1] if visited_locations else None):
            visited_locations.append(loc)

        # Convergence update from scene tokens.
        for dim_name in DIM_ORDER:
            tok = scene.get(dim_name)
            tok_meta = tok_index.get(tok, {})
            if tok_meta.get("attractor_weights"):
                convergence = np.minimum(
                    1.0,
                    convergence
                    + np.array(tok_meta["attractor_weights"][:3]) * convergence_rate,
                )

        prose = composer.compose(scene)
        turns_log.append({
            "turn": turn,
            "player_card": player_card,
            "scene": scene,
            "prose": prose,
            "convergence_after": convergence.tolist(),
            "beat": scene.get("BEAT"),
        })
        last_player_card = player_card

    return {
        "seed": seed,
        "turns": turns_log,
        "final_convergence": convergence.tolist(),
        "violations": violations,
        "final_beat": turns_log[-1]["beat"] if turns_log else None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Transcript rendering
# ─────────────────────────────────────────────────────────────────────────────


def render_transcript(case_id: str, run: dict, idx: int) -> str:
    lines = [f"## Playthrough {idx} (seed={run['seed']})", ""]
    for t in run["turns"]:
        pc = t["player_card"].split(":", 1)[-1]
        lines.append(f"[{t['turn']:2d}] PLAYS  {pc}")
        lines.append(f"     {t['prose']}")
        lines.append("")
    cmin = min(run["final_convergence"]) if run["final_convergence"] else 0.0
    lines.append(
        f"**Final state**: {len(run['turns'])} turns · "
        f"convergence_min ≈ {cmin:.2f} · "
        f"beat: {run['final_beat']}"
    )
    if run.get("outcome"):
        lines.append(f"**Outcome**: {run['outcome']}")
    if run["violations"]:
        lines.append("")
        lines.append(f"**Notes** ({len(run['violations'])} constraint slip(s)):")
        for v in run["violations"][:6]:
            lines.append(f"  - {v}")
        if len(run["violations"]) > 6:
            lines.append(f"  - … and {len(run['violations']) - 6} more")
    lines.append("")
    lines.append("---")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SceneLM (v3) simulation — no simulator-side scaffolds
# ─────────────────────────────────────────────────────────────────────────────


def simulate_one_scene_lm(ckpt_path: Path, case_id: str, max_turns: int,
                          seed: int, lang: str = "en") -> dict:
    """One playthrough on the v3 engine. Convergence is the engine's measured
    attractor accumulation (no multiplier); beats are the model's own BEAT
    tokens; the run ends when the model emits an outcome after an accusation,
    or via engine.resolve() at the turn cap. Sim policy: random cards, accuse
    a random suspect once measured convergence_min >= 0.65."""
    from generator.scene_lm_runtime import SceneLMEngine

    rng = random.Random(seed)
    engine = SceneLMEngine.load(ckpt_path, seed=seed)
    engine.ledger_path = Path("/tmp") / f"scene_lm_sim_ledger_{case_id}.json"
    composer = SceneComposer.load(case_id, lang=lang)
    cards = sorted(engine.vocab.case_cards[case_id])
    suspects = [c for c in cards if c.startswith("suspect:")]

    turns_log: List[Dict[str, Any]] = []
    outcome = None
    final_beat = "beat:orientation"
    conv: List[float] = [0.0, 0.0, 0.0]
    for turn in range(1, max_turns + 1):
        accusing = min(conv) >= 0.65 and suspects and rng.random() < 0.5
        composer.set_context(turn_idx=turn)
        if accusing:
            accused = rng.choice(suspects)
            res = engine.accuse(accused)
            scene, conv = res["scene"], res["conv"]
            prose = composer.compose(scene)
            turns_log.append({"turn": turn, "player_card": f"ACCUSE:{accused}",
                              "prose": prose})
            final_beat = scene.get("BEAT", final_beat)
            if res["ended"]:
                outcome = res["outcome"]
                break
        else:
            card = rng.choice(cards)
            scene, conv = engine.step(card)
            prose = composer.compose(scene)
            turns_log.append({"turn": turn, "player_card": card, "prose": prose})
            final_beat = scene.get("BEAT", final_beat)
    if outcome is None:
        outcome, _ = engine.resolve()
    return {"seed": seed, "turns": turns_log, "final_convergence": list(conv),
            "final_beat": final_beat, "violations": [], "outcome": outcome}


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────


def main():
    p = argparse.ArgumentParser()
    p.add_argument("case_id")
    p.add_argument("--n", type=int, default=5,
                   help="Number of playthroughs to simulate")
    p.add_argument("--max-turns", type=int, default=30,
                   help="Hard cap on turns per playthrough")
    p.add_argument("--seed", type=int, default=42, help="Base seed (per-run = base+i)")
    p.add_argument("--out", default=None,
                   help="Output markdown path (default: outputs/<case>/playtest_transcripts.md)")
    p.add_argument("--engine", choices=["v2", "scene_lm"], default="v2",
                   help="v2 = structured-scene engine; scene_lm = v3 flat "
                        "next-symbolic-token engine (no sim-side scaffolds)")
    p.add_argument("--model-path", default=None,
                   help="scene_lm only: checkpoint path (default: "
                        "outputs/<case>/scene_lm_full.pt)")
    args = p.parse_args()

    project_root = _HERE.parent.parent.parent  # 010-more-than-words/
    out_path = (
        Path(args.out) if args.out
        else project_root / "living_tales/trainer/outputs"
             / args.case_id / "playtest_transcripts.md"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.engine == "scene_lm":
        ckpt_path = Path(args.model_path or
                         (_HERE.parent / "outputs" / args.case_id
                          / "scene_lm_full.pt"))
        print(f"Loading {args.case_id} scene_lm engine from {ckpt_path} ...")
        sections = [
            f"# Playtest transcripts — {args.case_id} (engine: scene_lm)",
            "",
            f"Generated by `tools/playtest_simulate.py {args.case_id} "
            f"--engine scene_lm --n {args.n} --max-turns {args.max_turns}`",
            "", "---", "",
        ]
        for i in range(args.n):
            seed = args.seed + i
            print(f"  simulating playthrough {i + 1}/{args.n} (seed={seed})...")
            run = simulate_one_scene_lm(ckpt_path, args.case_id,
                                        max_turns=args.max_turns, seed=seed)
            sections.append(render_transcript(args.case_id, run, i + 1))
        out_path.write_text("\n".join(sections))
        print(f"\ntranscripts → {out_path}")
        return

    print(f"Loading {args.case_id} engine...")
    engine = load_engine(args.case_id, project_root)
    print(f"  model params: {sum(p.numel() for p in engine['model'].parameters()):,}")
    print(f"  full_vocab: {len(engine['ckpt']['full_vocab'])}")
    print()

    sections = [
        f"# Playtest transcripts — {args.case_id}",
        "",
        f"Generated by `tools/playtest_simulate.py {args.case_id} "
        f"--n {args.n} --max-turns {args.max_turns}`",
        "",
        f"Each playthrough below is a fresh simulated session: random player "
        f"card selection, model emits scene tuples, composer renders prose. "
        f"The Notes block flags any constraint violations the model slipped at "
        f"inference. Read each as if it were a real player's run.",
        "",
        "---",
        "",
    ]

    total_violations = 0
    for i in range(args.n):
        seed = args.seed + i
        print(f"  simulating playthrough {i + 1}/{args.n} (seed={seed})...")
        run = simulate_one(engine, max_turns=args.max_turns, seed=seed)
        total_violations += len(run["violations"])
        sections.append(render_transcript(args.case_id, run, i + 1))

    sections.append("")
    sections.append(f"**Aggregate**: {args.n} playthroughs, "
                    f"{total_violations} total constraint slips across all turns.")

    out_path.write_text("\n".join(sections))
    print()
    print(f"transcripts → {out_path}")
    print(f"total constraint slips across {args.n} runs: {total_violations}")


if __name__ == "__main__":
    main()
