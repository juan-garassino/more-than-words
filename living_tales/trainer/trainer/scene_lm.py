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
    """Hyper-parameters for :class:`SceneLM`.

    Attributes
    ----------
    vocab_size : int
        Size of the union token vocabulary (``len(SceneVocab)``).
    n_layers, hidden_dim, n_heads : int
        Transformer depth, model width and attention heads
        (``hidden_dim`` must be divisible by ``n_heads``).
    ffn_mult : int
        Feed-forward width as a multiple of ``hidden_dim``.
    dropout : float
        Dropout on attention and residual branches.
    max_seq_len : int
        Length of the precomputed RoPE cache; longer inputs are not supported.
    lora_rank : int
        Rank of the LoRA branch on every linear layer.
    """

    vocab_size: int
    n_layers: int = 5
    hidden_dim: int = 256
    n_heads: int = 8
    ffn_mult: int = 4
    dropout: float = 0.1
    max_seq_len: int = 2048
    lora_rank: int = 8


class _CausalBlock(nn.Module):
    """Pre-LayerNorm decoder block: RoPE causal self-attention + GELU FFN."""

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
        """Apply the block to ``x`` of shape ``(B, T, hidden_dim)`` (float).

        ``cos``/``sin`` are RoPE caches of shape ``(>=T, head_dim)``. Returns a
        tensor with the same shape as ``x``.
        """
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
    """Decoder-only transformer predicting the next symbolic token.

    Token ids come from :class:`trainer.scene_lm_vocab.SceneVocab`. The model
    itself is grammar-agnostic; the generation helpers below apply the
    per-case grammar (and optional constraints) as a logit mask.
    """

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
        """Return next-token logits.

        Parameters
        ----------
        ids : torch.Tensor
            ``(B, T)`` int64 token ids, ``T <= cfg.max_seq_len``.

        Returns
        -------
        torch.Tensor
            ``(B, T, vocab_size)`` float logits.
        """
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
        """Sample one token id from ``logits`` ``(vocab_size,)`` restricted to ``legal_ids``."""
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
        """Generate one full scene, slot by slot, grammar- and constraint-masked.

        ``ctx`` is a ``(1, T)`` int64 id tensor ending in ``<scene>``. For each
        slot in ``vocab.slot_dims(case_id)`` the legal ids are the grammar set,
        intersected with ``constraint_fn(dim, scene_so_far)`` when that returns
        a non-empty set that overlaps the grammar set (otherwise the grammar
        set alone is used). Returns ``{dim: token_string}``.
        """
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
        """Freeze everything except LoRA branches and the token embedding."""
        for n, p in self.named_parameters():
            p.requires_grad = ("lora" in n) or n.startswith("embed.")

    def num_parameters(self, trainable_only: bool = False) -> int:
        """Count parameters, optionally only those with ``requires_grad``."""
        return sum(p.numel() for p in self.parameters()
                   if p.requires_grad or not trainable_only)

    def save(self, path, vocab, case_id: Optional[str] = None,
             extra: Optional[Dict] = None) -> None:
        """Write config, weights and the baked-in vocab/grammar to ``path``."""
        torch.save({
            "config": asdict(self.cfg),
            "state_dict": self.state_dict(),
            "vocab": vocab.to_dict(),          # grammar + vocab baked in
            "case_id": case_id,
            "extra": extra or {},
        }, path)

    @classmethod
    def load(cls, path, map_location="cpu"):
        """Load a checkpoint written by :meth:`save`.

        Returns ``(model, vocab, ckpt)`` where ``ckpt`` is the raw dict
        (``case_id``, ``extra`` ...). Uses ``weights_only=False``, so only load
        checkpoints you trust.
        """
        from trainer.scene_lm_vocab import SceneVocab
        ckpt = torch.load(path, map_location=map_location, weights_only=False)
        model = cls(SceneLMConfig(**ckpt["config"]))
        model.load_state_dict(ckpt["state_dict"])
        return model, SceneVocab.from_dict(ckpt["vocab"]), ckpt
