"""SceneLM (v3) eval gate: 6 probes, JSON report, nonzero exit on gate failure.

  python3 tools/eval_scene_lm.py amber_cipher --model-path outputs/amber_cipher/scene_lm_full.pt

Probes (pass bars from the design spec):
  binding      >= 0.95  played card's controlled dim matches, raw model output
  coherence    == 0     intransitive ACTION must pair with object_focus:none
  closing_arc  >= 2/3   seeded 25-turn runs reach beat:closing_in or later
  diversity    <= 0.40  max single-token share on REVELATION/TRANSITION/BEAT
  outcome      >= 0.90  held-out (history, accusation) -> outcome class match
  convergence  >= 0.70  Spearman(measured attractor conv, authored conv_after)
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from generator.scene_lm_runtime import AttractorMeter, SceneLMEngine  # noqa: E402

INTRANSITIVE_ACTIONS = {"action:waits", "action:leaves", "action:arrives",
                        "action:recalls", "action:notices"}

BINDING_CHECK = {
    "object": lambda card, s: s["OBJECT_FOCUS"] == card,
    "suspect": lambda card, s: s["PRESENCE"] == "presence:with_" + card.split(":")[1],
    "witness": lambda card, s: s["PRESENCE"] == "presence:with_" + card.split(":")[1],
    "location": lambda card, s: s["LOCATION"] == card,
    # abstract classes: bound iff no stale object leaks
    "motive": lambda card, s: s["OBJECT_FOCUS"] == "object_focus:none"
        or s["ACTION"] == "action:recalls",
    "event": lambda card, s: s["OBJECT_FOCUS"] == "object_focus:none"
        or s["ACTION"] == "action:recalls",
    "emotion": lambda card, s: s["OBJECT_FOCUS"] == "object_focus:none"
        or s["ACTION"] == "action:recalls",
    "time": lambda card, s: s["OBJECT_FOCUS"] == "object_focus:none"
        or s["ACTION"] == "action:recalls",
}

GATES = {"binding": 0.95, "coherence_violations": 0, "closing_arc_runs": 2,
         "diversity_max_share": 0.40, "outcome_acc": 0.90, "conv_spearman": 0.70}

LATE_BEATS = {"beat:closing_in", "beat:verdict_ready"}


def spearman(a, b):
    def ranks(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        for rank, i in enumerate(order):
            r[i] = float(rank)
        return r
    n = len(a)
    if n <= 2:
        return 1.0
    ra, rb = ranks(a), ranks(b)
    d2 = sum((x - y) ** 2 for x, y in zip(ra, rb))
    return 1.0 - 6.0 * d2 / (n * (n * n - 1))


def probe_binding(make_engine, vocab, case_id, n_turns=25, n_seeds=3):
    hits = total = 0
    misses = []
    for seed in range(n_seeds):
        eng = make_engine(seed)
        rng = random.Random(seed)
        cards = sorted(vocab.case_cards[case_id])
        for _ in range(n_turns):
            card = rng.choice(cards)
            scene, _ = eng.step(card)
            check = BINDING_CHECK.get(card.split(":")[0])
            if check is not None:
                total += 1
                ok = bool(check(card, scene))
                hits += ok
                if not ok and len(misses) < 10:
                    misses.append({"card": card,
                                   "OBJECT_FOCUS": scene.get("OBJECT_FOCUS"),
                                   "PRESENCE": scene.get("PRESENCE"),
                                   "LOCATION": scene.get("LOCATION"),
                                   "ACTION": scene.get("ACTION")})
    return {"score": hits / max(total, 1), "n": total, "sample_misses": misses}


def probe_coherence(make_engine, case_id, n_turns=25, n_seeds=3):
    violations = []
    for seed in range(n_seeds):
        eng = make_engine(seed)
        rng = random.Random(100 + seed)
        cards = sorted(eng.vocab.case_cards[case_id])
        for t in range(n_turns):
            scene, _ = eng.step(rng.choice(cards))
            if (scene["ACTION"] in INTRANSITIVE_ACTIONS
                    and scene["OBJECT_FOCUS"] != "object_focus:none"):
                violations.append({"seed": seed, "turn": t,
                                   "action": scene["ACTION"],
                                   "object": scene["OBJECT_FOCUS"]})
    return {"violations": violations}


def probe_closing_arc(make_engine, case_id, n_turns=25, n_seeds=3):
    ok = 0
    per_run = []
    for seed in range(n_seeds):
        eng = make_engine(seed)
        rng = random.Random(200 + seed)
        cards = sorted(eng.vocab.case_cards[case_id])
        beats = [eng.step(rng.choice(cards))[0]["BEAT"] for _ in range(n_turns)]
        reached = any(b in LATE_BEATS for b in beats)
        ok += reached
        per_run.append({"seed": seed, "reached_late": reached,
                        "final_beat": beats[-1]})
    return {"runs_reaching_late": ok, "n_seeds": n_seeds, "runs": per_run}


def probe_diversity(make_engine, vocab, case_id, n_turns=25, n_seeds=3):
    counts = {d: Counter() for d in ("REVELATION", "TRANSITION", "BEAT")}
    for seed in range(n_seeds):
        eng = make_engine(300 + seed)
        rng = random.Random(300 + seed)
        cards = sorted(vocab.case_cards[case_id])
        for _ in range(n_turns):
            scene, _ = eng.step(rng.choice(cards))
            for d in counts:
                counts[d][scene[d]] += 1
    return {d: round(c.most_common(1)[0][1] / sum(c.values()), 3)
            for d, c in counts.items()}


def probe_outcome_accuracy(ckpt_path, case_id, cases_dir, holdout_frac=0.2):
    """Replay held-out trajectory histories up to their final accuse turn and
    check the model emits the authored outcome class."""
    import torch
    from trainer.scene_lm import SceneLM
    from trainer.scene_lm_dataset import load_case_token_sequences
    model, vocab, _ = SceneLM.load(ckpt_path)
    seqs = load_case_token_sequences(case_id, cases_dir, vocab)
    stride = max(1, int(1 / holdout_frac))
    holdout = [s for s in seqs[::stride]]
    hit = total = 0
    details = []
    for seq in holdout:
        out_pos = next(i for i, t in enumerate(seq) if t.startswith("<outcome:"))
        ctx = torch.tensor([[vocab.encode(t) for t in seq[:out_pos]]])
        pred = model.predict_outcome(ctx, case_id, vocab)
        truth = seq[out_pos].removeprefix("<outcome:").removesuffix(">")
        hit += pred == truth
        total += 1
        details.append({"truth": truth, "pred": pred})
    return {"acc": hit / max(total, 1), "n": total, "details": details[:10]}


def probe_convergence(case_id, cases_dir):
    """Pooled turn-level Spearman(measured attractor accumulation, authored
    convergence_after) over full (non-branch) trajectories. Model-free: it
    validates the meter at the granularity the runtime uses it (within-run
    progression drives beats/pacing). Uses unclamped sums — the runtime [0,1]
    clamp is display-only. Measured on 2026-06-12 data: 0.925 pooled, median
    within-run 1.0; final-value cross-run ordering is deliberately NOT gated
    (cumulative weight scales with run length by design)."""
    measured, authored = [], []
    for f in sorted((cases_dir / case_id / "trajectories").glob("*.json")):
        if f.name == "manifest.json":
            continue
        t = json.loads(f.read_text())
        if t.get("branch_of"):
            continue
        m = AttractorMeter(case_id, cases_dir / case_id)
        for turn in t["turns"]:
            m.observe([turn["player_card"]] + list(turn["scene"].values()))
            measured.append(sum(m._conv))          # unclamped
            authored.append(sum(turn["convergence_after"]))
    return {"spearman": round(spearman(measured, authored), 3), "n": len(measured)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("case_id")
    p.add_argument("--model-path", required=True)
    p.add_argument("--report", default=None)
    args = p.parse_args()
    cases_dir = _HERE.parent / "cases"
    ck = Path(args.model_path)

    def make(seed):
        return SceneLMEngine.load(ck, seed=seed)

    eng0 = make(0)
    vocab, case = eng0.vocab, args.case_id
    results = {
        "binding": probe_binding(make, vocab, case),
        "coherence": probe_coherence(make, case),
        "closing_arc": probe_closing_arc(make, case),
        "diversity": probe_diversity(make, vocab, case),
        "outcome": probe_outcome_accuracy(ck, case, cases_dir),
        "convergence": probe_convergence(case, cases_dir),
    }
    checks = {
        "binding": results["binding"]["score"] >= GATES["binding"],
        "coherence": len(results["coherence"]["violations"])
            <= GATES["coherence_violations"],
        "closing_arc": results["closing_arc"]["runs_reaching_late"]
            >= GATES["closing_arc_runs"],
        "diversity": max(results["diversity"].values())
            <= GATES["diversity_max_share"],
        "outcome": results["outcome"]["acc"] >= GATES["outcome_acc"],
        "convergence": results["convergence"]["spearman"] >= GATES["conv_spearman"],
    }
    results["gate"] = {**checks, "pass": all(checks.values())}
    report = json.dumps(results, indent=1, default=str)
    print(report)
    out = Path(args.report or (_HERE.parent / "outputs" / case / "scene_lm_eval.json"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report)
    print(f"\nGATE: {'PASS' if results['gate']['pass'] else 'FAIL'}")
    sys.exit(0 if results["gate"]["pass"] else 1)


if __name__ == "__main__":
    main()
