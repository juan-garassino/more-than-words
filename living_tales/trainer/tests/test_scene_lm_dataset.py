from __future__ import annotations

import torch

from trainer.scene_lm_dataset import SceneLMDataset
from trainer.scene_lm_vocab import SceneVocab


def _ds(production_cases, **kw):
    vocab = SceneVocab.build(production_cases)
    return SceneLMDataset(["amber_cipher"], vocab, augment_truncate=False, **kw), vocab


def test_loss_masked_on_player_tokens(production_cases):
    ds, vocab = _ds(production_cases)
    ex = ds[0]
    ids, mask = ex["ids"].tolist(), ex["loss_mask"]
    card_m, accuse_m = vocab.encode("<card>"), vocab.encode("<accuse>")
    saw_card = saw_accuse = False
    for i, t in enumerate(ids[:-1]):
        if t == card_m:
            assert mask[i + 1].item() == 0      # the played card: input-only
            saw_card = True
        if t == accuse_m:
            assert mask[i + 1].item() == 0      # the accused token: input-only
            saw_accuse = True
    assert saw_card
    # boundary markers themselves stay supervised (story-state signal)
    first_card = ids.index(card_m)
    assert mask[first_card].item() == 1


def test_outcome_token_supervised(production_cases):
    ds, vocab = _ds(production_cases)
    for i in range(len(ds)):
        ex = ds[i]
        ids = ex["ids"].tolist()
        out_pos = [j for j, t in enumerate(ids)
                   if vocab.decode(t).startswith("<outcome:")]
        assert len(out_pos) == 1
        assert ex["loss_mask"][out_pos[0]].item() == 1


def test_binding_weight_doubles_controlled_dim(production_cases):
    ds, vocab = _ds(production_cases)
    obj_cards = {i for i in vocab.card_ids("amber_cipher")
                 if vocab.decode(i).startswith("object:")}
    marker = vocab.encode("<card>")
    obj_slot_off = 3 + ds.slot_index("amber_cipher", "OBJECT_FOCUS")
    found = False
    for n in range(len(ds)):
        ex = ds[n]
        ids, w = ex["ids"].tolist(), ex["loss_weight"]
        for i, t in enumerate(ids):
            if t == marker and i + 1 < len(ids) and ids[i + 1] in obj_cards:
                assert w[i + obj_slot_off].item() >= 2.0
                found = True
        if found:
            break
    assert found


def test_class_balance_weights_cover_collapsed_dims(production_cases):
    ds, vocab = _ds(production_cases)
    cb = ds.class_balance_weights()
    rev_ids = vocab.legal_ids("amber_cipher", "REVELATION")
    assert all(cb[i] >= 1.0 for i in rev_ids)
    assert max(cb[i] for i in rev_ids) <= 5.0


def test_collate_pads_and_aligns(production_cases):
    ds, vocab = _ds(production_cases)
    batch = ds.collate([ds[0], ds[1]])
    assert batch["ids"].shape == batch["loss_mask"].shape == batch["loss_weight"].shape
    assert batch["ids"].dtype == torch.long


def test_truncation_augmentation_respects_turn_boundary(production_cases):
    vocab = SceneVocab.build(production_cases)
    ds = SceneLMDataset(["amber_cipher"], vocab, augment_truncate=True, seed=7)
    turn_len = 3 + len(vocab.slot_dims("amber_cipher"))   # marker+token+<scene>+dims
    eos = vocab.encode("<eos>")
    truncated = 0
    for i in range(len(ds)):
        ids = ds[i]["ids"].tolist()
        if ids[-1] != eos:
            truncated += 1
            assert (len(ids) - 1) % turn_len == 0          # <bos> + whole turns
    assert truncated > 0


def test_universal_only_mode(production_cases):
    vocab = SceneVocab.build(production_cases)
    ds = SceneLMDataset(["attended_hour"], vocab, universal_only=True,
                        augment_truncate=False)
    ids = ds[0]["ids"].tolist()
    med = [vocab.encode(t) for t in vocab.case_dim_vocab["attended_hour"]["MEDICAL_TELL"]]
    assert not any(t in set(med) for t in ids)


def test_stratified_holdout_split(production_cases):
    from collections import Counter
    vocab = SceneVocab.build(production_cases)

    def outcome_counts(ds):
        return Counter(next(t for t in seq if t.startswith("<outcome:"))
                       for _, seq in ds.examples)

    ds_all = SceneLMDataset(["amber_cipher"], vocab, augment_truncate=False)
    tr = SceneLMDataset(["amber_cipher"], vocab, augment_truncate=False,
                        split="train")
    ho = SceneLMDataset(["amber_cipher"], vocab, augment_truncate=False,
                        split="holdout")
    assert len(tr) + len(ho) == len(ds_all)
    assert 0 < len(ho) < len(tr)
    all_c, ho_c = outcome_counts(ds_all), outcome_counts(ho)
    for cls, n in all_c.items():
        if n < 3:
            assert cls not in ho_c          # tiny classes never leave train
        else:
            assert 0 < ho_c.get(cls, 0) < n  # bigger classes represented in both
    # deterministic across constructions
    ho2 = SceneLMDataset(["amber_cipher"], vocab, augment_truncate=False,
                         split="holdout")
    assert [s[:20] for _, s in ho.examples] == [s[:20] for _, s in ho2.examples]
