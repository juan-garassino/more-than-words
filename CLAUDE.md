# Living Tales

> **GCP migration note (2026-06-07):** When deployed as a user-facing product, cloud target is **`garassino-ai`** / `europe-west1` (apps tier, multi-user). Future deploys piggyback on the GAR repo `garassino-ai/app-images`. See workspace root `CLAUDE.md` § "GCP architecture".

Living Tales is a symbolic mystery game where a per-case overfitted transformer co-narrates with the player through token dialogue. The new engine is **v3 (SceneLM)** — a ~4.3M-param decoder-only transformer doing next-token prediction over the case's symbolic language (code shipped 2026-06-12; first Colab training run pending). v2 (structured-scene, parallel dim decoding) remains the last *trained* runtime; the legacy Hopfield/KD/REINFORCE path is preserved on disk but is not the runtime.

There is **no LLM at runtime.** The engine emits token IDs over a per-dim vocabulary; the composer slot-fills hand-authored phrases (`phrases.json`) into Obra-Dinn third-person past prose. Tokens are symbolic; the model never sees or emits natural language.

## Game Loop

Player plays a symbolic card → model emits a complete 11-12-dim scene tuple (TRANSITION, LOCATION, PRESENCE, STANCE, CAUSE, ACTION, OBJECT_FOCUS, TELL, ATMOSPHERE, REVELATION, BEAT, plus case-specific MEDICAL_TELL / ART_TELL) → composer renders prose → repeat. Convergence is *measured* from authored attractor weights of emitted tokens; phase/beats come from the model's own BEAT dim; player accuses via the verdict sheet — the model narrates the confrontation and its boundary choice decides whether the accusation ends the story (near-misses are real). 16 authored outcome classes per case are reachable endings, tracked in a casebook ledger.

## V3 Architecture (SceneLM)

- **Sequence format**: a play session is one string — `<bos>` … `<card> {card} <scene> {dim tokens in grammar order}` … `<accuse> {accused} <scene> {…}` … `<outcome:class> <eos>`. Accusations are in-stream turns with confrontation scenes (matches how trajectories are authored: `ACCUSE:*` player cards, incl. mid-game near-misses and `ACCUSE:none`).
- **Grammar order** (within-turn causal dim order): TRANSITION → LOCATION → PRESENCE → STANCE → CAUSE → ACTION → OBJECT_FOCUS → TELL → [MEDICAL/ART_TELL] → ATMOSPHERE → REVELATION → BEAT. Position determines the legal sub-vocab (logit mask = syntax, not scaffold).
- **`SceneLM`** (`trainer/scene_lm.py`): 5 layers, d256, 8 heads, RoPE, ctx 2048, LoRA on all linears (reuses v2's `LoraLinear`/RoPE helpers). `generate_scene` (grammar ∩ constraints mask, single temp 0.7), `boundary_choice` (continue vs outcome), `predict_outcome`. Vocab + grammar baked into every checkpoint.
- **`SceneVocab`** (`trainer/scene_lm_vocab.py`): union vocab across cases (~436 tokens); per-case slot template + legal-id sets; cards = tokens.json ∪ trajectory-played cards.
- **Converter + dataset** (`trainer/scene_lm_dataset.py`): mechanical trajectory→sequence conversion (golden fixture in `tests/fixtures/`); loss masks (player's card/accused input-only; boundary markers + outcome supervised), ×2 binding weights on card-controlled dims, class-balanced CE weights on REVELATION/TRANSITION/BEAT, turn-boundary truncation augmentation, cf-branch anchoring.
- **Two-stage training** (`tools/train_scene_lm.py`): `base` (union corpus, universal dims) → `outputs/_base/scene_lm_base.pt`; `adapter` (frozen base + LoRA + embedding) → `outputs/<case>/scene_lm_full.pt`.
- **Runtime** (`generator/scene_lm_runtime.py`): `SceneLMEngine.step/accuse/resolve`; `AttractorMeter` measures convergence (validated: turn-level Spearman 0.925 vs authored `convergence_after`); endings picked hash-stably from authored trajectory `ending` blocks; ledger at `outputs/<case>/ledger.json`. **Zero scaffolds**: no convergence boosts, no card forcing, no per-dim temperatures, no beat injection, no vocab wrapper.
- **Composer** (`generator/structured_scene_composer.py`): variant picker hash-stable on `(turn_idx, token_id)` plus optional per-run `run_salt` (set by the v3 loop so replays read fresh); voice-arc stages (cold/warming/breaking/broken); v3 pygame loop tracks NPC interview counts so stages actually advance.
- **Eval gate** (`tools/eval_scene_lm.py`): 6 probes — binding ≥0.95, coherence violations 0, closing-arc ≥2/3, diversity max-share ≤0.40, outcome accuracy ≥0.90, convergence Spearman ≥0.70. Design docs: `docs/superpowers/specs/2026-06-12-scene-language-model-design.md` + `docs/superpowers/plans/2026-06-12-scene-lm-v3.md`.
- **v2 reference** (`trainer/structured_scene_model_v2.py`, `tools/train_structured_v2.py`, `trainer/trajectory_dataset_v2.py`, `generator/discovery_beats.py` + `beats.json`): preserved untouched for A/B; beats.json is demoted to an eval reference in v3.

## Cases

| Case | Trajectories | Case-specific dims |
|---|---|---|
| amber_cipher | 59 (49 full + 10 cf branches) | none |
| attended_hour | 59 | MEDICAL_TELL |
| venetian_mirror | 59 | ART_TELL |

Total: 177 trajectories across ~16 outcome classes per case (correct_*, partial_correct, accomplice_found, framed_suspect, motive_only_confession, late_revelation, near_miss, red_herring_trap, cold_trail, per-suspect wrong_*). Accusations are authored as in-stream `ACCUSE:*` turns with confrontation scenes; `ending.accused` names the accused.

## Key Commands

```bash
# Author + validate
python3 living_tales/trainer/tools/validate_trajectories.py <case> --all
python3 living_tales/trainer/tools/author_live.py <case> <traj_id>      # live composer preview

# Train v3 (Colab only — never local)
make train-scene-lm-all  OUTPUT_DIR=/content/drive/MyDrive/living_tales_outputs
make eval-gate-scene-lm  # 6-probe gate per case (binding/coherence/arc/diversity/outcome/convergence)

# Train v2 (legacy reference)
make train-v2-all    OUTPUT_DIR=/content/drive/MyDrive/living_tales_outputs
make eval-gate       # v2 probe + 5-seed × 3-case judge sweep

# Play (v3)
cd living_tales/trainer && python3 tools/pygame_play.py <case> --engine scene_lm --lang en

# Simulate (v3; v2 default; judges: claude_subagent / openai / gemini)
python3 tools/playtest_simulate.py <case> --engine scene_lm --n 3 --max-turns 25 --seed 1

# Tests (local, fast)
cd living_tales/trainer && python3 -m pytest tests -q
```

## Invariants (Non-Negotiable)

- Engine never reads surface expressions; tokens are symbolic.
- All trajectories are hand-authored (or hand-reviewed); no programmatic generation from attractor walks.
- Cross-case bleed is forbidden: v3 bakes per-case vocab + grammar into each checkpoint.
- Convergence is player-guided, driven only from token attractor weights — in v3 this is literally the implementation (`AttractorMeter`), no boosts.
- Hard-mask constraints apply at inference (v3: grammar mask is also applied to the training loss).
- Spanish parity: every phrases.json entry has en + es.
- Train on Colab, never local (a ≤10-step CPU smoke test in pytest is testing, not training).

## Known Issues / Roadmap

Resolved by v3 *by construction* (verify after the first trained checkpoint passes the gate): modal-token collapse (class-balanced CE replaces lambda_div), convergence placeholder (+0.06/turn deleted — measured accumulator), per-case vocab runtime wrapper (baked into checkpoints), card-binding force tables (binding learned via weighted loss + in-stream card context), beat injection (model's BEAT dim drives the arc), NPC interview-stage tracking (v3 pygame loop counts interviews).

Still open:

- **First v3 training run** (Colab) + eval gate pass on amber_cipher; v2 judge baseline to beat: 13/25.
- **Journal `_phrase` predates list-variant phrases** — `tools/journal.py` crashes (caught) on variant lists; affects v2 and v3 equally.
- **Phrase pool thin per token** — many top-NPC phrases have 1 cold-stage variant; need 4-6 variants × 4 stages.
- **CAUSE phrase poverty** — "Tracing the evidence" dominates transcripts; widen composer banks.

## What to Optimize

- First v3 checkpoint through the 6-probe gate, then judge sweep ≥18/25.
- More trajectories per case (50 → 65 → 90 in three thresholds).
- Phrase variant richness, especially top-NPC voice-arc stages.
- Outcome-class coverage for rare classes (wrong_<suspect> singletons strain the outcome head).
