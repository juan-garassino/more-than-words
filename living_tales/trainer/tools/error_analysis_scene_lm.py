"""SceneLM (v3) error analysis: the diagnosis layer behind the eval gate.

  python3 tools/error_analysis_scene_lm.py amber_cipher --model-path outputs/amber_cipher/scene_lm_full.pt

Where the gate says pass/fail, this says *what to fix*:
  teacher_forced  per-dim / per-beat / per-depth next-token accuracy, train vs held-out
  confusion       per-dim (authored -> predicted) pairs, sorted by count
  outcome         full confusion matrix + per-class recall (exposes class starvation)
  free_run        untruncated binding misses, coherence violations, per-dim histograms

Writes outputs/<case>/error_analysis.{json,md}. The md opens with the
error -> lever map so a failing signal points at data vs hyperparams.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

import torch  # noqa: E402

from generator.scene_lm_runtime import SceneLMEngine                 # noqa: E402
from tools.eval_scene_lm import probe_binding, probe_coherence       # noqa: E402
from trainer.scene_lm import SceneLM                                 # noqa: E402
from trainer.scene_lm_dataset import load_case_token_sequences       # noqa: E402

LEVER_MAP = """\
## Error → lever map

| Signal | Likely cause | Lever |
|---|---|---|
| binding misses concentrated on one card class | seam authoring — card→dim links weak in data | fix trajectories, not hyperparams |
| dim accuracy low everywhere | undertrained | more steps / lower lr |
| dim accuracy low only late-turn | late-game data thin | more late-game trajectories / truncation-augment tuning |
| diversity max-share fail on a dim | class imbalance surviving CE weights | widen authored token variety |
| outcome recall 0 on specific classes | class has <2 trajectories or held-out singleton | add trajectories / cf branches for that class |
| val loss diverges from train | memorizing surface order | more augmentation, fewer adapter steps |
"""

DEPTH_BUCKETS = [(1, 10, "turns_1-10"), (11, 25, "turns_11-25"),
                 (26, 10**9, "turns_26+")]


def _depth(turn):
    return next(name for lo, hi, name in DEPTH_BUCKETS if lo <= turn <= hi)


def _annotate(seq, dims):
    """Per-position (dim, turn, beat_token) for supervised scene positions;
    ('OUTCOME', turn, None) at the outcome token; None elsewhere."""
    ann = [None] * len(seq)
    turn = 0
    i = 0
    while i < len(seq):
        if seq[i] == "<scene>":
            turn += 1
            span = [(i + 1 + k, d) for k, d in enumerate(dims)
                    if i + 1 + k < len(seq)]
            beat = next((seq[p] for p, d in span if d == "BEAT"), None)
            for p, d in span:
                ann[p] = (d, turn, beat)
            i += len(dims) + 1
        else:
            if seq[i].startswith("<outcome:"):
                ann[i] = ("OUTCOME", turn, None)
            i += 1
    return ann


def _acc_table(cells):
    return {k: {"acc": round(c / max(n, 1), 3), "n": n}
            for k, (c, n) in sorted(cells.items())}


def _teacher_forced(model, vocab, case_id, seqs):
    dims = vocab.slot_dims(case_id)
    legal = {d: torch.tensor(vocab.legal_ids(case_id, d)) for d in dims}
    per_dim = defaultdict(lambda: [0, 0])
    per_beat = defaultdict(lambda: [0, 0])
    per_depth = defaultdict(lambda: [0, 0])
    confusion = defaultdict(Counter)
    for seq in seqs:
        ids = torch.tensor([[vocab.encode(t) for t in seq]])
        with torch.no_grad():
            logits = model(ids)[0]
        ann = _annotate(seq, dims)
        for pos in range(1, len(seq)):
            a = ann[pos]
            if a is None or a[0] == "OUTCOME":
                continue
            dim, turn, beat = a
            cand = legal[dim]
            pred = vocab.decode(int(cand[int(torch.argmax(
                logits[pos - 1, cand]))]))
            truth = seq[pos]
            ok = pred == truth
            for acc_key, table in ((dim, per_dim), (beat, per_beat),
                                   ((dim, _depth(turn)), per_depth)):
                table[acc_key][0] += ok
                table[acc_key][1] += 1
            if not ok:
                confusion[dim][(truth, pred)] += 1
    return per_dim, per_beat, per_depth, confusion


def _outcome_matrix(model, vocab, case_id, seqs):
    classes = vocab.outcome_classes(case_id)
    matrix = {t: {p: 0 for p in classes} for t in classes}
    for seq in seqs:
        pos = next((i for i, t in enumerate(seq)
                    if t.startswith("<outcome:")), None)
        if pos is None:
            continue
        ctx = torch.tensor([[vocab.encode(t) for t in seq[:pos]]])
        pred = model.predict_outcome(ctx, case_id, vocab)
        truth = seq[pos].removeprefix("<outcome:").removesuffix(">")
        matrix.setdefault(truth, {p: 0 for p in classes})
        matrix[truth][pred] = matrix[truth].get(pred, 0) + 1
    recall = {t: round(row.get(t, 0) / max(sum(row.values()), 1), 3)
              for t, row in matrix.items()}
    return {"classes": sorted(matrix), "matrix": matrix,
            "per_class_recall": recall}


def _free_run(ckpt_path, case_id, n_turns, n_seeds):
    def make(seed):
        return SceneLMEngine.load(Path(ckpt_path), seed=seed)

    vocab = make(0).vocab
    hist = defaultdict(Counter)
    for seed in range(n_seeds):
        eng = make(400 + seed)
        rng = random.Random(400 + seed)
        cards = sorted(vocab.case_cards[case_id])
        for _ in range(n_turns):
            scene, _ = eng.step(rng.choice(cards))
            for d, t in scene.items():
                hist[d][t] += 1
    binding = probe_binding(make, vocab, case_id, n_turns, n_seeds,
                            max_misses=10**9)
    coherence = probe_coherence(make, case_id, n_turns, n_seeds)
    return {"histograms": {d: dict(c.most_common()) for d, c in hist.items()},
            "binding_misses": binding["sample_misses"],
            "binding_score": binding["score"],
            "coherence_violations": coherence["violations"]}


def analyze(ckpt_path, case_id, cases_dir=None, holdout_frac=0.2,
            n_turns=25, n_seeds=3, max_sequences=None):
    cases_dir = Path(cases_dir) if cases_dir else _HERE.parent / "cases"
    model, vocab, _ = SceneLM.load(Path(ckpt_path))
    model.eval()
    seqs = load_case_token_sequences(case_id, cases_dir, vocab)
    if max_sequences:
        seqs = seqs[:max_sequences]
    stride = max(1, int(1 / holdout_frac))
    holdout = seqs[::stride]
    train = [s for i, s in enumerate(seqs) if i % stride]
    if not train:                       # tiny max_sequences smoke contexts
        train = holdout
    report = {"case_id": case_id, "checkpoint": str(ckpt_path),
              "n_sequences": {"train": len(train), "holdout": len(holdout)},
              "teacher_forced": {}, "confusion": {}}
    all_confusion = defaultdict(Counter)
    for split, split_seqs in (("train", train), ("holdout", holdout)):
        per_dim, per_beat, per_depth, confusion = _teacher_forced(
            model, vocab, case_id, split_seqs)
        report["teacher_forced"][split] = {
            "per_dim": _acc_table(per_dim),
            "per_beat": _acc_table(per_beat),
            "per_depth": _acc_table(
                {f"{d}/{b}": v for (d, b), v in per_depth.items()}),
        }
        for d, c in confusion.items():
            all_confusion[d].update(c)
    report["confusion"] = {
        d: [{"truth": t, "pred": p, "count": n}
            for (t, p), n in c.most_common(15)]
        for d, c in all_confusion.items()}
    report["outcome"] = _outcome_matrix(model, vocab, case_id, seqs)
    report["free_run"] = _free_run(ckpt_path, case_id, n_turns, n_seeds)
    return report


def _md(report):
    lines = [f"# Error analysis — {report['case_id']}", "",
             f"Checkpoint: `{report['checkpoint']}`", "", LEVER_MAP, ""]
    for split in ("train", "holdout"):
        tf = report["teacher_forced"][split]
        lines += [f"## Teacher-forced accuracy ({split}, "
                  f"n={report['n_sequences'][split]} sequences)", "",
                  "| dim | acc | n |", "|---|---|---|"]
        lines += [f"| {d} | {v['acc']} | {v['n']} |"
                  for d, v in tf["per_dim"].items()]
        lines += ["", "| beat | acc | n |", "|---|---|---|"]
        lines += [f"| {b} | {v['acc']} | {v['n']} |"
                  for b, v in tf["per_beat"].items()]
        lines += ["", "| dim/depth | acc | n |", "|---|---|---|"]
        lines += [f"| {k} | {v['acc']} | {v['n']} |"
                  for k, v in tf["per_depth"].items()]
        lines.append("")
    lines += ["## Confusion pairs (top 15 per dim)", ""]
    for d, pairs in report["confusion"].items():
        lines += [f"### {d}", "", "| authored | predicted | count |",
                  "|---|---|---|"]
        lines += [f"| {p['truth']} | {p['pred']} | {p['count']} |"
                  for p in pairs]
        lines.append("")
    oc = report["outcome"]
    lines += ["## Outcome per-class recall", "", "| class | recall |",
              "|---|---|"]
    lines += [f"| {c} | {oc['per_class_recall'][c]} |" for c in oc["classes"]]
    fr = report["free_run"]
    lines += ["", "## Free-run", "",
              f"Binding score {fr['binding_score']:.3f} "
              f"({len(fr['binding_misses'])} misses), "
              f"{len(fr['coherence_violations'])} coherence violations.", ""]
    for d, h in fr["histograms"].items():
        top = ", ".join(f"{t.split(':', 1)[-1]}×{n}"
                        for t, n in list(h.items())[:5])
        lines.append(f"- **{d}**: {top}")
    return "\n".join(lines) + "\n"


def write_reports(report, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "error_analysis.json").write_text(
        json.dumps(report, indent=1, default=str))
    (out_dir / "error_analysis.md").write_text(_md(report))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("case_id")
    p.add_argument("--model-path", required=True)
    p.add_argument("--report-dir", default=None)
    p.add_argument("--holdout-frac", type=float, default=0.2)
    p.add_argument("--n-turns", type=int, default=25)
    p.add_argument("--n-seeds", type=int, default=3)
    args = p.parse_args()
    report = analyze(args.model_path, args.case_id,
                     holdout_frac=args.holdout_frac,
                     n_turns=args.n_turns, n_seeds=args.n_seeds)
    out = Path(args.report_dir or (_HERE.parent / "outputs" / args.case_id))
    write_reports(report, out)
    print(f"wrote {out / 'error_analysis.json'} + .md")


if __name__ == "__main__":
    main()
