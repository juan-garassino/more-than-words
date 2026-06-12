# Scene Language Model (v3) — design

**Date:** 2026-06-12
**Status:** draft for review
**Supersedes:** `StructuredSceneTransformerV2` as the runtime engine (v2 stays on disk, untouched)

## 1. Why

A four-part audit (game loop, ML engine, content, replayability) found one root problem: **the network does not carry the game; scaffolds do.** Concretely:

- Played cards reach the scene via a runtime forcing table ("fix #4"), not the model. Abstract cards (EVENT/MOTIVE/EMOTION/TELL/STANCE) leak stale objects ("questioned the coal dust", "waited the torn ticket").
- Convergence is a flat +0.06/turn placeholder — player choice is mechanically invisible; 0/3 simulated runs ever reach the LATE phase or an accusation.
- Beats are injected from `beats.json` on convergence thresholds that, given the flat boost, are turn timers.
- Modal collapse ("Silence held between them" 19×/25 turns) is fought with per-dim runtime temperatures (0.3–0.8).
- 16 hand-authored outcome classes per case (59 trajectories in amber_cipher) collapse to 4 runtime ending buckets; the richest replay content is unreachable.

V2's architecture invites this: dims are decoded in parallel from cross-head dim queries, so dims are conditionally near-independent given the hidden state — scene incoherence and weak card binding are structural, and every scaffold above is a compensation for it.

**Design principle (the user's invariant):** the symbiosis between engine and network is everything. The network does the work; the engine renders, measures, and grades — it never overrides.

## 2. Core idea

Replace per-dim parallel decoding with a **decoder-only transformer doing next-token prediction over a symbolic language**. The case is the language. A play session is one string. The player's card is a token in the stream; the scene is 11–12 tokens generated after it; the accusation and outcome are tokens too.

Card binding, scene coherence, pacing, and outcome narration all become properties of one autoregressive distribution, learned from the existing hand-authored trajectories. No fix #4, no convergence boost, no beat injection, no per-dim temperatures, no runtime vocab wrapper.

## 3. The symbolic language

One vocabulary per case (~200 tokens), three families:

| Family | Examples | Source |
|---|---|---|
| Card tokens | `object:initialed_cufflink`, `witness:porter`, `travel:to_platform_two` | `tokens.json` (cards reuse the same symbol ids as scene tokens where they overlap — shared embeddings deliberately tie their semantics) |
| Scene tokens | `location:signal_box`, `presence:with_signalman`, `action:questions`, `beat:orientation` | `dimensions.json` per-dim vocabs |
| Control tokens | `<bos>`, `<card>`, `<scene>`, `<accuse>`, `<eos>`, `<outcome:correct_voss>`, `<outcome:partial_correct>`, … (one per outcome class, 16 in amber_cipher) | new |

- **Universal core**: the union of universal-dim vocabs + control tokens, shared across cases with stable ids (same id table the base model is pretrained on).
- **Case-specific extension**: case-only tokens (case cards, MEDICAL_TELL / ART_TELL vocabs, case outcome tokens) appended after the core; their embedding rows train in the adapter stage.

## 4. Sequence format

```
<bos>
<card> object:initialed_cufflink
<scene> location:thornfield_crossing transition:stayed cause:examining_evidence
        presence:alone stance:none action:examines object:initialed_cufflink
        tell:none atmosphere:fog_thickens revelation:partial_match beat:orientation
<card> witness:porter
<scene> …
…
<accuse> suspect:renard_voss
<outcome:correct_voss>
<eos>
```

- One turn = `<card>` + card token + `<scene>` + exactly N scene tokens (N = 11 universal, 12 for cases with a case-specific dim).
- Budget: 120 turns × 14 tokens ≈ 1,700 → **max context 2,048** (RoPE; no architectural issue).
- The accusation segment is **suspect-only**: `<accuse>` + the accused token. **Implementation amendment (2026-06-12, data-driven):** trajectories author accusations as *in-stream turns* (`ACCUSE:*` player cards with full confrontation scenes, including mid-game wrong accusations in near_miss/late_revelation arcs and `ACCUSE:none`). The shipped format therefore makes an accuse turn `<accuse> {token} <scene> {dims}`, every trajectory terminates with its `<outcome:*>` token, and at runtime the model's boundary choice (continue vs outcome) after a confrontation decides whether the accusation ends the story. The outcome class remains f(history, accused); motive/evidence picks in the verdict UI stay deferred (YAGNI).

## 5. Within-turn grammar — where coherence comes from

Scene tokens are generated in a **fixed causal dim order**:

```
TRANSITION → LOCATION → PRESENCE → STANCE → CAUSE → ACTION → OBJECT_FOCUS
→ TELL → [MEDICAL_TELL | ART_TELL] → ATMOSPHERE → REVELATION → BEAT
```

(TRANSITION precedes LOCATION because `constraints.json` rules condition LOCATION on the
already-emitted TRANSITION — e.g. `transition:stayed ⇒ LOCATION = previous location` —
matching the existing rule-evaluation direction in `generator/constraints_compiler.py`.)

Rationale (each dim conditions on everything before it):

- ACTION is predicted after PRESENCE → "questioned" cannot pair with `presence:alone` + an object unless the data shows it. Kills the verb-slot bugs at the source.
- OBJECT_FOCUS conditions on ACTION → `action:recalls` learns to be followed by `object:none`; the stale-object leak class disappears without a routing table.
- REVELATION and BEAT come last, conditioned on the entire scene and full history → pacing decisions see everything. This is what lets the model's own BEAT head drive phase progression.

**Grammar mask:** the position within a turn determines which dim's sub-vocab is legal; illegal logits are −inf at both train (loss restricted to legal vocab) and inference. This has the status of syntax — same category as a tokenizer — not a behavioral scaffold. Hard constraints from `constraints.json` (forbidden combinations) also apply inside the mask, satisfying the "hard-mask at train time" roadmap item.

## 6. Architecture — `SceneLM`

Deliberately boring decoder-only transformer:

| Component | Spec |
|---|---|
| Layers | 5 |
| d_model | 256, 8 heads, FFN ×4, dropout 0.1 |
| Positions | RoPE over the flat stream, max 2,048 |
| Vocab | ~200/case (core + extension) |
| Params | ≈ 4–5M (same class as v2's 5.3M) |
| Adaptation | unchanged two-stage: universal base on union corpus → frozen base + per-case LoRA (all linears) + case-specific embedding rows |

**Deleted from v2** (each existed to compensate for parallel dim decoding):

- cross-head decoder over dim queries — dims now interact through ordinary causal attention;
- dedicated played-card KV slot — the card is first-class context in the stream;
- latent scene-type z (8 modes) — multimodality comes from sampling at branch points the counterfactual trajectories already author.

New files (v2 untouched): `trainer/scene_lm.py` (model), `trainer/scene_lm_dataset.py` (converter + dataset), `trainer/tools/train_scene_lm.py` (two-stage trainer), `generator/scene_lm_runtime.py` (turn loop used by pygame).

## 7. Data pipeline — mechanical conversion, no re-authoring

Trajectory JSON already contains everything: per-turn `player_card`, full `scene` dict, `convergence_after`, top-level `outcome`, `opening`, `ending`.

`scene_lm_dataset.py` converts each trajectory to one token sequence:

1. **Normalize** token ids against `dimensions.json` vocab (the files contain prefix drift, e.g. `object:none` vs `object_focus:none`, `emotion:steady_hands` in the TELL slot — normalization table derived from the validator's rules, and the validator gains a check for it).
2. Emit `<card> {player_card} <scene> {11–12 dim tokens in grammar order}` per turn.
3. Terminal segment from `outcome` + `ending`: `<accuse> {suspect} {motive} {evidence}` + `<outcome:{class}>`. A small per-case mapping table (outcome class → accusation tokens) covers the 16 classes; for `cold_trail`/no-accusation trajectories the sequence ends `<eos>` without an accuse segment.
4. **Counterfactual branches** (`cf_*`): anchor history (cached from the parent trajectory up to `branch_turn`) + divergent continuation — exactly as `trajectory_dataset_v2.py` does today, producing genuinely multimodal next-token distributions at decision points.
5. **Augmentation kept from v2**: history truncation (random prefix crops respecting turn boundaries).
6. **Loss mask**: card tokens and `<card>`/`<scene>`/`<accuse>` markers and the player's accusation tokens are input-only (no loss) — the model never learns to predict the player, only to respond.

Stage-1 (base) uses universal dims only: case-specific dim positions are dropped from the turn template (`active_mask` equivalent), and only core-vocab sequences are used.

## 8. Training

- **Loss**: next-token CE restricted to the grammar-legal vocab per position.
- **Binding weight**: ×2 loss on the dims a card class controls, on the scene immediately after that card (OBJECT→OBJECT_FOCUS, SUSPECT/WITNESS→PRESENCE, TRAVEL→LOCATION+TRANSITION, EVENT/MOTIVE/EMOTION/TELL→ACTION+OBJECT_FOCUS). A nudge — the mechanism is attention.
- **Anti-collapse**: class-balanced CE (inverse-√-frequency weights, capped at 5×) on the historically collapsed dims: REVELATION, TRANSITION, BEAT. Replaces λ_div and runtime temperature hacks.
- **Outcome supervision**: the `<outcome:*>` token trains like any other target token; wrong-accusation and partial-outcome trajectories (16 classes) are its training signal.
- Two-stage schedule, optimizer, and Colab-only execution unchanged from v2 (`OUTPUT_DIR` on Drive, per the standing rule). Checkpoints: `outputs/_base/scene_lm_base.pt`, `outputs/<case>/scene_lm_full.pt` — **per-case vocab and grammar tables are baked into the checkpoint** (closes the runtime-vocab-wrapper roadmap item).

## 9. Runtime — the engine becomes a reader

Turn loop in `scene_lm_runtime.py`:

1. Append `<card>` + the player's card token to the running context.
2. Generate exactly N scene tokens, grammar-masked, **one global temperature 0.7** (no per-dim schedules), greedy fallback below a confidence floor is *not* applied — what the model says is what renders.
3. Composer renders the scene (unchanged, except a per-run salt mixed into the hash-stable variant picker so replays read fresh — one line).
4. **Convergence is measured, never boosted**: the engine sums the attractor weights (`attractor.json`) of the emitted scene tokens per convergence dim, normalized. The authored `convergence_after` vectors in trajectories become *eval references* (measured-vs-authored correlation), not runtime inputs.
5. **Beats come from the model**: phase progression and discovery beats key off the emitted BEAT/REVELATION tokens. `beats.json` is demoted from injector to eval assertion ("a healthy seeded run reaches `beat:verdict_ready` territory by turn ~24").
6. **Accusation**: the verdict-sheet UI (WHO pick; motive/evidence picks deferred per §4) composes the `<accuse>` segment; the model emits the outcome token; the engine renders the authored ending for that class. The engine grades nothing — it reads the outcome the model narrated. All 16 authored outcome classes become reachable, named endings.
7. **Outcome ledger**: a per-case "endings found: k/16" screen across runs (local JSON). Pure UI over model output; the replay hook.

**Scaffolds removed from `pygame_play.py`'s structured path**: +0.06/turn convergence boost, fix-#4 card forcing, per-dim temperatures/top-k, beat injection, runtime vocab restriction, dead `fake_dialogue`/ending-fragments path.

## 10. Eval gate (extends `make eval-gate`)

The retrain is verifiable **before** scaffolds are stripped; v2 stays runnable for A/B:

| Probe | Pass bar |
|---|---|
| **Binding probe** | ≥95% of probe turns: played card's controlled dim matches the card (all card classes, including abstract — measured on the model's raw output, no forcing) |
| **Coherence probe** | 0 verb-object agreement violations over a 75-turn sweep (intransitive ACTION ⇒ `object:none`) |
| **Closing-arc probe** | ≥2/3 seeded 25-turn runs reach LATE-phase BEAT tokens; accusation reachable |
| **Diversity floor** | no single token >40% of emissions on REVELATION/TRANSITION/BEAT across a sweep |
| **Outcome accuracy** | held-out (history, accusation) pairs: emitted outcome class matches authored class ≥90% |
| **Convergence sanity** | measured attractor convergence vs authored `convergence_after`: Spearman ≥0.7 on held-out trajectories |
| **Judge sweep** | existing 5-seed × 3-case `playtest_judge.py`; target ≥18/25 (current v2: 13/25) |

**Fallback policy:** if the outcome-accuracy probe fails the bar, the engine-side outcome grader is the contingency — explicitly logged as a temporary scaffold with a removal condition, per the minimal-post-processing rule.

## 11. Testing

- Unit: converter round-trip (trajectory → sequence → trajectory), grammar-mask legality, loss-mask placement, vocab id stability between base and adapter stages.
- Golden: one hand-checked trajectory's exact token sequence committed as a fixture.
- Integration: `playtest_simulate.py` gains a `--engine scene_lm` path; judge pipeline unchanged.
- All validation runs locally; training runs on Colab only.

## 12. Risks

- **Outcome head reliability** (16-way, thin data for rare classes) — mitigated by the probe + contingency grader.
- **AR error cascade within a turn** (one bad early token skews the scene) — mitigated by grammar mask + constraints; monitored by the coherence probe.
- **Class-balanced CE over-rotating** rare tokens into noise — capped weights; diversity floor is two-sided in spirit (judge sweep catches nonsense).
- Authored-pacing drift: converter is mechanical, but the per-outcome accusation mapping table is hand-written — it gets validator coverage.

## 13. Docs to update (with implementation, same commits)

- **`010-more-than-words/CLAUDE.md`**: replace "V2 Architecture" section with SceneLM (v3) — files, sequence format, grammar order; update Key Commands (`train_scene_lm.py`, eval gate probes); move resolved Known Issues (collapse, convergence placeholder, vocab wrapper, hard-mask) to a "resolved in v3" note; update Invariants (convergence-measured wording unchanged — now true).
- **`living_tales/DISPATCH_TEMPLATE.md` / `STORIES_INDEX.md`**: no change (authoring format untouched).
- **README.md / DOCS.md**: none exist at project level — no doc impact beyond CLAUDE.md.
