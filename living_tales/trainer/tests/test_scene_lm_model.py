from __future__ import annotations

import torch

from trainer.scene_lm import SceneLM, SceneLMConfig
from trainer.scene_lm_vocab import SceneVocab


def _tiny(production_cases):
    vocab = SceneVocab.build(production_cases)
    cfg = SceneLMConfig(vocab_size=len(vocab), n_layers=2, hidden_dim=64,
                        n_heads=4, max_seq_len=256)
    return SceneLM(cfg), vocab


def test_forward_shape(production_cases):
    model, vocab = _tiny(production_cases)
    ids = torch.randint(0, len(vocab), (2, 30))
    logits = model(ids)
    assert logits.shape == (2, 30, len(vocab))


def test_causality(production_cases):
    """Changing a future token must not change past logits."""
    model, vocab = _tiny(production_cases)
    model.eval()
    ids = torch.randint(0, len(vocab), (1, 20))
    with torch.no_grad():
        a = model(ids)[0, 9]
        ids2 = ids.clone()
        ids2[0, 15] = (ids2[0, 15] + 1) % len(vocab)
        b = model(ids2)[0, 9]
    assert torch.allclose(a, b, atol=1e-5)


def test_generate_scene_respects_grammar(production_cases):
    model, vocab = _tiny(production_cases)
    model.eval()
    ctx = torch.tensor([[vocab.encode("<bos>"), vocab.encode("<card>"),
                         vocab.encode("object:initialed_cufflink"),
                         vocab.encode("<scene>")]])
    scene = model.generate_scene(ctx, "amber_cipher", vocab, temperature=0.7,
                                 constraint_fn=None,
                                 generator=torch.Generator().manual_seed(0))
    assert list(scene.keys()) == vocab.slot_dims("amber_cipher")
    for dim, tok in scene.items():
        assert vocab.encode(tok) in set(vocab.legal_ids("amber_cipher", dim))


def test_generate_scene_respects_constraint_fn(production_cases):
    model, vocab = _tiny(production_cases)
    model.eval()
    ctx = torch.tensor([[vocab.encode("<bos>"), vocab.encode("<card>"),
                         vocab.encode("witness:porter"),
                         vocab.encode("<scene>")]])
    forced = {vocab.encode("transition:stayed")}
    scene = model.generate_scene(
        ctx, "amber_cipher", vocab,
        constraint_fn=lambda dim, partial: forced if dim == "TRANSITION" else None,
        generator=torch.Generator().manual_seed(0))
    assert scene["TRANSITION"] == "transition:stayed"


def test_boundary_choice_restricted(production_cases):
    model, vocab = _tiny(production_cases)
    model.eval()
    ctx = torch.tensor([[vocab.encode("<bos>")]])
    tok = model.boundary_choice(ctx, "amber_cipher", vocab,
                                generator=torch.Generator().manual_seed(0))
    legal = {"<card>", "<accuse>"} | {
        f"<outcome:{o}>" for o in vocab.outcome_classes("amber_cipher")}
    assert tok in legal


def test_lora_freeze(production_cases):
    model, _ = _tiny(production_cases)
    model.freeze_base_for_adapter_stage()
    trainable = [n for n, p in model.named_parameters() if p.requires_grad]
    assert trainable
    assert all("lora" in n or "embed" in n for n in trainable)


def test_save_load_round_trip(production_cases, tmp_path):
    model, vocab = _tiny(production_cases)
    p = tmp_path / "m.pt"
    model.save(p, vocab, case_id="amber_cipher", extra={"conv_scale": 2.0})
    m2, v2, ckpt = SceneLM.load(p)
    assert ckpt["case_id"] == "amber_cipher"
    assert ckpt["extra"]["conv_scale"] == 2.0
    assert v2.encode("<accuse>") == vocab.encode("<accuse>")
    ids = torch.randint(0, len(vocab), (1, 10))
    with torch.no_grad():
        assert torch.allclose(model.eval()(ids), m2.eval()(ids), atol=1e-6)
