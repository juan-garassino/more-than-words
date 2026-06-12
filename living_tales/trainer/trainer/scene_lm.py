"""SceneLM (v3): decoder-only causal transformer over the symbolic case language.

Replaces StructuredSceneTransformerV2's parallel dim decoding with flat
next-token prediction. The grammar (slot order, per-dim legal vocab) is applied
as a logit mask at generation time — syntax, not scaffold. Vocab + grammar are
baked into every checkpoint.

Adapter stage note: `freeze_base_for_adapter_stage` keeps LoRA branches AND the
token embedding trainable. Per-case checkpoints ship the full model, so slight
base-token embedding drift per adapter cannot cause cross-case bleed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Dict, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from trainer.structured_scene_model_v2 import (
    LoraLinear,
    _apply_rope,
    _build_rope_cache,
)


@dataclass
class SceneLMConfig:
    vocab_size: int
    n_layers: int = 5
    hidden_dim: int = 256
    n_heads: int = 8
    ffn_mult: int = 4
    dropout: float = 0.1
    max_seq_len: int = 2048
    lora_rank: int = 8


class _CausalBlock(nn.Module):
    def __init__(self, cfg: SceneLMConfig):
        super().__init__()
        d, h = cfg.hidden_dim, cfg.n_heads
        self.n_heads, self.head_dim = h, d // h
        self.qkv = LoraLinear(d, 3 * d, lora_rank=cfg.lora_rank)
        self.proj = LoraLinear(d, d, lora_rank=cfg.lora_rank)
        self.ffn_in = LoraLinear(d, cfg.ffn_mult * d, lora_rank=cfg.lora_rank)
        self.ffn_out = LoraLinear(cfg.ffn_mult * d, d, lora_rank=cfg.lora_rank)
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.drop = nn.Dropout(cfg.dropout)

    def forward(self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
        B, T, D = x.shape
        q, k, v = self.qkv(self.ln1(x)).chunk(3, dim=-1)
        shp = (B, T, self.n_heads, self.head_dim)
        q, k, v = (t.view(shp).transpose(1, 2) for t in (q, k, v))
        q, k = _apply_rope(q, cos[:T], sin[:T]), _apply_rope(k, cos[:T], sin[:T])
        attn = F.scaled_dot_product_attention(
            q, k, v, is_causal=True,
            dropout_p=self.drop.p if self.training else 0.0)
        x = x + self.drop(self.proj(attn.transpose(1, 2).reshape(B, T, D)))
        x = x + self.drop(self.ffn_out(F.gelu(self.ffn_in(self.ln2(x)))))
        return x


class SceneLM(nn.Module):
    def __init__(self, cfg: SceneLMConfig):
        super().__init__()
        self.cfg = cfg
        self.embed = nn.Embedding(cfg.vocab_size, cfg.hidden_dim)
        self.blocks = nn.ModuleList(_CausalBlock(cfg) for _ in range(cfg.n_layers))
        self.ln_f = nn.LayerNorm(cfg.hidden_dim)
        self.head = nn.Linear(cfg.hidden_dim, cfg.vocab_size, bias=False)
        cos, sin = _build_rope_cache(cfg.max_seq_len, cfg.hidden_dim // cfg.n_heads,
                                     device="cpu")
        self.register_buffer("rope_cos", cos, persistent=False)
        self.register_buffer("rope_sin", sin, persistent=False)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        x = self.embed(ids)
        cos = self.rope_cos.to(x.device)
        sin = self.rope_sin.to(x.device)
        for blk in self.blocks:
            x = blk(x, cos, sin)
        return self.head(self.ln_f(x))

    # ── generation ──────────────────────────────────────────────────────────
    @staticmethod
    def _sample_masked(
        logits: torch.Tensor,
        legal_ids: set,
        temperature: float,
        generator: Optional[torch.Generator],
    ) -> int:
        mask = torch.full_like(logits, float("-inf"))
        idx = torch.tensor(sorted(legal_ids), device=logits.device, dtype=torch.long)
        mask[idx] = 0.0
        probs = F.softmax((logits + mask) / max(temperature, 1e-4), dim=-1)
        return int(torch.multinomial(probs, 1, generator=generator))

    @torch.no_grad()
    def generate_scene(
        self,
        ctx: torch.Tensor,                       # (1, T) ending in <scene>
        case_id: str,
        vocab,
        temperature: float = 0.7,
        constraint_fn: Optional[Callable[[str, Dict[str, str]], Optional[set]]] = None,
        generator: Optional[torch.Generator] = None,
    ) -> Dict[str, str]:
        """Generate one full scene, slot by slot, grammar- and constraint-masked."""
        scene: Dict[str, str] = {}
        ids = ctx
        for dim in vocab.slot_dims(case_id):
            logits = self(ids)[0, -1]
            legal = set(vocab.legal_ids(case_id, dim))
            if constraint_fn is not None:
                allowed = constraint_fn(dim, scene)
                if allowed:
                    narrowed = legal & allowed
                    if narrowed:
                        legal = narrowed
            nxt = self._sample_masked(logits, legal, temperature, generator)
            scene[dim] = vocab.decode(nxt)
            ids = torch.cat([ids, torch.tensor([[nxt]], device=ids.device)], dim=1)
        return scene

    @torch.no_grad()
    def boundary_choice(
        self,
        ctx: torch.Tensor,
        case_id: str,
        vocab,
        temperature: float = 0.7,
        generator: Optional[torch.Generator] = None,
    ) -> str:
        """At a turn boundary: does the story continue or end, per the model?

        Restricted to {<card>, <accuse>} ∪ outcome tokens. The engine uses the
        outcome-vs-continue decision; <card>/<accuse> both mean 'continues'.
        """
        logits = self(ctx)[0, -1]
        legal = {vocab.encode("<card>"), vocab.encode("<accuse>")}
        legal.update(vocab.outcome_ids(case_id))
        return vocab.decode(self._sample_masked(logits, legal, temperature, generator))

    @torch.no_grad()
    def predict_outcome(self, ctx: torch.Tensor, case_id: str, vocab) -> str:
        """Greedy over outcome tokens (used when the run must resolve now)."""
        logits = self(ctx)[0, -1]
        oids = vocab.outcome_ids(case_id)
        best = oids[int(torch.argmax(logits[torch.tensor(oids)]))]
        return vocab.decode(best).removeprefix("<outcome:").removesuffix(">")

    # ── staging / persistence ────────────────────────────────────────────────
    def freeze_base_for_adapter_stage(self) -> None:
        for n, p in self.named_parameters():
            p.requires_grad = ("lora" in n) or n.startswith("embed.")

    def num_parameters(self, trainable_only: bool = False) -> int:
        return sum(p.numel() for p in self.parameters()
                   if p.requires_grad or not trainable_only)

    def save(self, path, vocab, case_id: Optional[str] = None,
             extra: Optional[Dict] = None) -> None:
        torch.save({
            "config": asdict(self.cfg),
            "state_dict": self.state_dict(),
            "vocab": vocab.to_dict(),          # grammar + vocab baked in
            "case_id": case_id,
            "extra": extra or {},
        }, path)

    @classmethod
    def load(cls, path, map_location="cpu"):
        from trainer.scene_lm_vocab import SceneVocab
        ckpt = torch.load(path, map_location=map_location, weights_only=False)
        model = cls(SceneLMConfig(**ckpt["config"]))
        model.load_state_dict(ckpt["state_dict"])
        return model, SceneVocab.from_dict(ckpt["vocab"]), ckpt
