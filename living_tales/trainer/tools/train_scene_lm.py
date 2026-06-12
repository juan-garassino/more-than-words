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


def _run(model, ds, args, device):
    class_w = ds.class_balance_weights().to(device)
    dl = DataLoader(ds, batch_size=args.batch_size, shuffle=True,
                    collate_fn=ds.collate)
    opt = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),
                            lr=args.lr, weight_decay=0.01)
    model.train().to(device)
    step = 0
    while step < args.steps:
        for batch in dl:
            batch = {k: v.to(device) for k, v in batch.items()}
            loss = _loss(model(batch["ids"]), batch, class_w)
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            step += 1
            if step % 50 == 0 or step == args.steps:
                print(f"step {step}/{args.steps} loss {loss.item():.4f}", flush=True)
            if step >= args.steps:
                break


def cmd_base(args):
    vocab = SceneVocab.build(PRODUCTION_CASES)
    ds = SceneLMDataset(PRODUCTION_CASES, vocab, universal_only=True, seed=args.seed)
    cfg = SceneLMConfig(vocab_size=len(vocab), n_layers=args.n_layers,
                        hidden_dim=args.hidden_dim, n_heads=args.n_heads)
    model = SceneLM(cfg)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"base: {len(ds)} sequences, {model.num_parameters():,} params, {device}")
    _run(model, ds, args, device)
    out = Path(args.output_dir) / "_base"
    out.mkdir(parents=True, exist_ok=True)
    model.save(out / "scene_lm_base.pt", vocab)
    print(f"saved -> {out / 'scene_lm_base.pt'}")


def cmd_adapter(args):
    base_path = Path(args.output_dir) / "_base" / "scene_lm_base.pt"
    model, vocab, _ = SceneLM.load(base_path)
    model.freeze_base_for_adapter_stage()
    ds = SceneLMDataset([args.case], vocab, universal_only=False, seed=args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"adapter[{args.case}]: {len(ds)} sequences, "
          f"{model.num_parameters(trainable_only=True):,} trainable, {device}")
    _run(model, ds, args, device)
    out = Path(args.output_dir) / args.case
    out.mkdir(parents=True, exist_ok=True)
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
    sub.choices["adapter"].add_argument("--case", required=True)
    args = p.parse_args()
    {"base": cmd_base, "adapter": cmd_adapter}[args.cmd](args)


if __name__ == "__main__":
    main()
