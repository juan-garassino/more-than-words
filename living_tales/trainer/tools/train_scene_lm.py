"""Two-stage SceneLM (v3) trainer. Real runs on Colab only (OUTPUT_DIR on Drive).

  python3 tools/train_scene_lm.py base    --output-dir <dir> [--steps N]
  python3 tools/train_scene_lm.py adapter --case amber_cipher --output-dir <dir>

Stage `base` pretrains on the union universal-dim corpus across all production
cases. Stage `adapter` loads the base, freezes everything except LoRA branches
and the token embedding (per-case checkpoints ship the full model, so embedding
drift cannot bleed across cases), and trains on one case's full-dim corpus.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from trainer.scene_lm import SceneLM, SceneLMConfig                 # noqa: E402
from trainer.scene_lm_dataset import SceneLMDataset                 # noqa: E402
from trainer.scene_lm_vocab import SceneVocab                       # noqa: E402

PRODUCTION_CASES = ["amber_cipher", "attended_hour", "venetian_mirror"]


def _loss(logits, batch, class_w):
    tgt = batch["ids"][:, 1:]
    lm = batch["loss_mask"][:, 1:].float()
    lw = batch["loss_weight"][:, 1:]
    ce = F.cross_entropy(logits[:, :-1].transpose(1, 2), tgt,
                         weight=class_w, reduction="none")
    return (ce * lm * lw).sum() / lm.sum().clamp(min=1.0)


def _val_loss(model, val_ds, class_w, device, batch_size):
    if val_ds is None or not len(val_ds):
        return None
    dl = DataLoader(val_ds, batch_size=batch_size, collate_fn=val_ds.collate)
    model.eval()
    tot = n = 0
    with torch.no_grad():
        for batch in dl:
            batch = {k: v.to(device) for k, v in batch.items()}
            tot += _loss(model(batch["ids"]), batch, class_w).item()
            n += 1
    model.train()
    return round(tot / max(n, 1), 4)


def _run(model, ds, args, device, out_dir, artifact, vocab, case_id=None,
         val_ds=None):
    """Drive-safe loop: JSONL logs flushed per row, artifact + optimizer
    state overwritten in place every checkpoint, resume picks up mid-run."""
    class_w = ds.class_balance_weights().to(device)
    dl = DataLoader(ds, batch_size=args.batch_size, shuffle=True,
                    collate_fn=ds.collate)
    opt = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),
                            lr=args.lr, weight_decay=0.01)
    model.train().to(device)
    out_dir.mkdir(parents=True, exist_ok=True)
    state_path = out_dir / f"{artifact.removesuffix('.pt')}.train_state.pt"
    step = 0
    if args.resume and state_path.exists():
        state = torch.load(state_path, map_location=device)
        model.load_state_dict(state["model"])
        opt.load_state_dict(state["opt"])
        step = state["step"]
        print(f"resumed at step {step}", flush=True)
    stage = "adapter" if case_id else "base"
    eval_every = getattr(args, "eval_every", 0)

    def checkpoint():
        model.save(out_dir / artifact, vocab, case_id=case_id)
        torch.save({"model": model.state_dict(), "opt": opt.state_dict(),
                    "step": step}, state_path)
        if eval_every and case_id and step % eval_every == 0:
            from tools.eval_scene_lm import run_probes
            r = run_probes(out_dir / artifact, case_id,
                           n_turns=args.eval_turns, n_seeds=args.eval_seeds)
            row = {"step": step, "case": case_id,
                   "binding": r["binding"]["score"],
                   "coherence_violations": len(r["coherence"]["violations"]),
                   "closing_arc": r["closing_arc"]["runs_reaching_late"],
                   "diversity_max": max(r["diversity"].values()),
                   "outcome_acc": r["outcome"]["acc"],
                   "conv_spearman": r["convergence"]["spearman"],
                   "gate_pass": r["gate"]["pass"]}
            with (out_dir / "eval.jsonl").open("a") as f:
                f.write(json.dumps(row) + "\n")
            model.train().to(device)

    with (out_dir / "train.jsonl").open("a") as log:
        while step < args.steps:
            for batch in dl:
                batch = {k: v.to(device) for k, v in batch.items()}
                loss = _loss(model(batch["ids"]), batch, class_w)
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
                step += 1
                if step % args.log_every == 0 or step == args.steps:
                    row = {"stage": stage, "case": case_id, "step": step,
                           "loss": round(loss.item(), 4),
                           "val_loss": _val_loss(model, val_ds, class_w,
                                                 device, args.batch_size)}
                    print(f"step {step}/{args.steps} loss {row['loss']} "
                          f"val {row['val_loss']}", flush=True)
                    log.write(json.dumps(row) + "\n")
                    log.flush()
                if step % args.checkpoint_every == 0 or step == args.steps:
                    checkpoint()
                if step >= args.steps:
                    break


def _splits(case_ids, vocab, universal_only, args):
    if args.holdout_frac <= 0:
        return (SceneLMDataset(case_ids, vocab, universal_only=universal_only,
                               seed=args.seed), None)
    common = dict(universal_only=universal_only, seed=args.seed,
                  holdout_frac=args.holdout_frac)
    return (SceneLMDataset(case_ids, vocab, split="train", **common),
            SceneLMDataset(case_ids, vocab, split="holdout",
                           augment_truncate=False, **common))


def cmd_base(args):
    vocab = SceneVocab.build(PRODUCTION_CASES)
    ds, val_ds = _splits(PRODUCTION_CASES, vocab, True, args)
    cfg = SceneLMConfig(vocab_size=len(vocab), n_layers=args.n_layers,
                        hidden_dim=args.hidden_dim, n_heads=args.n_heads)
    model = SceneLM(cfg)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"base: {len(ds)} sequences, {model.num_parameters():,} params, {device}")
    out = Path(args.output_dir) / "_base"
    _run(model, ds, args, device, out, "scene_lm_base.pt", vocab,
         val_ds=val_ds)
    model.save(out / "scene_lm_base.pt", vocab)
    print(f"saved -> {out / 'scene_lm_base.pt'}")


def cmd_adapter(args):
    base_path = Path(args.output_dir) / "_base" / "scene_lm_base.pt"
    model, vocab, _ = SceneLM.load(base_path)
    model.freeze_base_for_adapter_stage()
    ds, val_ds = _splits([args.case], vocab, False, args)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"adapter[{args.case}]: {len(ds)} sequences, "
          f"{model.num_parameters(trainable_only=True):,} trainable, {device}")
    out = Path(args.output_dir) / args.case
    _run(model, ds, args, device, out, "scene_lm_full.pt", vocab,
         case_id=args.case, val_ds=val_ds)
    model.save(out / "scene_lm_full.pt", vocab, case_id=args.case)
    print(f"saved -> {out / 'scene_lm_full.pt'}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("base", "adapter"):
        s = sub.add_parser(name)
        s.add_argument("--output-dir", required=True)   # Colab: Drive path
        s.add_argument("--steps", type=int, default=3000 if name == "base" else 1500)
        s.add_argument("--batch-size", type=int, default=16)
        s.add_argument("--lr", type=float, default=3e-4)
        s.add_argument("--seed", type=int, default=0)
        s.add_argument("--hidden-dim", type=int, default=256)
        s.add_argument("--n-layers", type=int, default=5)
        s.add_argument("--n-heads", type=int, default=8)
        s.add_argument("--checkpoint-every", type=int, default=250)
        s.add_argument("--log-every", type=int, default=50)
        s.add_argument("--resume", action="store_true")
        s.add_argument("--holdout-frac", type=float, default=0.1)  # 0 = train on all
    sub.choices["adapter"].add_argument("--case", required=True)
    sub.choices["adapter"].add_argument("--eval-every", type=int, default=500)
    sub.choices["adapter"].add_argument("--eval-turns", type=int, default=25)
    sub.choices["adapter"].add_argument("--eval-seeds", type=int, default=3)
    args = p.parse_args()
    {"base": cmd_base, "adapter": cmd_adapter}[args.cmd](args)


if __name__ == "__main__":
    main()
