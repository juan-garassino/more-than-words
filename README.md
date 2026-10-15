# Living Tales

Living Tales is a symbolic mystery game. A small transformer, overfitted per case,
co-narrates with the player: the player plays a card, the model emits a scene as
a tuple of symbolic tokens, and a template composer turns the tokens into
third-person past-tense prose. There is no LLM at runtime and the model never
sees or emits natural language.

## Status

| Part | State |
|---|---|
| v3 engine (`SceneLM`, runtime, composer, eval gate) | code complete, covered by `pytest` |
| First v3 training run (Colab) | **pending**; no trained v3 checkpoint exists in this repo and there are no v3 results to report |
| Authored data | 3 production cases, 190 hand-authored trajectories (see below) |
| v2 structured-scene engine | kept for A/B comparison, last trained runtime |
| Hopfield / KD / REINFORCE pipeline | legacy, preserved on disk, not the runtime |

Source of truth for current status and invariants: [`CLAUDE.md`](CLAUDE.md).

## How it works (v3)

- A play session is one flat token string:
  `<bos> <card> {card} <scene> {dim tokens} ... <accuse> {accused} <scene> {...} <outcome:class> <eos>`.
- `SceneLM` (`living_tales/trainer/trainer/scene_lm.py`) is a decoder-only transformer
  with RoPE and LoRA on all linear layers. With the default config (5 layers, width 256,
  8 heads) and the 436-token union vocabulary it has 4,336,384 parameters.
- Within a scene, dims are generated one token at a time in a fixed grammar order
  (TRANSITION, LOCATION, PRESENCE, STANCE, CAUSE, ACTION, OBJECT_FOCUS, TELL,
  ATMOSPHERE, REVELATION, BEAT; case-specific dims are inserted after TELL).
  The legal vocabulary per position is a logit mask, intersected with the case's
  hard constraints (`constraints.json`, compiled in `generator/constraints_compiler.py`).
- Convergence is measured, not scripted: `AttractorMeter` sums the authored attractor
  weights (`tokens.json`) of the tokens played and emitted.
- Accusations are in-stream turns. After the confrontation scene the model chooses
  between continuing and an `<outcome:*>` token, so a wrong accusation can leave the
  story running.
- Training is two-stage (`tools/train_scene_lm.py`): `base` on the union corpus
  (universal dims), then a per-case `adapter` (LoRA + token embedding trainable).
- `tools/eval_scene_lm.py` is the pass/fail gate: six probes (binding >= 0.95,
  coherence violations = 0, closing arc >= 2/3 runs, diversity max-share <= 0.40,
  outcome accuracy >= 0.90, convergence Spearman >= 0.70).
  `tools/error_analysis_scene_lm.py` reports where a failing checkpoint goes wrong.

Design: [`docs/superpowers/specs/2026-06-12-scene-language-model-design.md`](docs/superpowers/specs/2026-06-12-scene-language-model-design.md),
plan: [`docs/superpowers/plans/2026-06-12-scene-lm-v3.md`](docs/superpowers/plans/2026-06-12-scene-lm-v3.md).

## Data

Packed case data lives in `living_tales/trainer/cases/<case>/`
(`dimensions.json`, `constraints.json`, `tokens.json`, `phrases.json`, `trajectories/`, ...).

| Case | Trajectories | Case-specific dim |
|---|---|---|
| `amber_cipher` | 65 | none |
| `attended_hour` | 64 | MEDICAL_TELL |
| `venetian_mirror` | 61 | ART_TELL |

Trajectory counts are the number of files in each `trajectories/` directory (excluding
`manifest.json`). `cases/` at the repo root holds 19 source case specs and
[`docs/cases/`](docs/cases/) holds narrative specs for 24 cases; only the three above
have v3 trajectory data. Every trajectory in `amber_cipher` passes
`validate_trajectories.py` (65 trajectories, 0 rule violations, 0 vocab violations).

## Quick start

Requires Python 3.10+ and `numpy torch rich` (`pytest` for tests).

```bash
pip install -r living_tales/trainer/requirements.txt pytest

# Tests (CPU, includes short smoke tests of the training harness)
cd living_tales/trainer && python3 -m pytest tests -q

# Validate hand-authored trajectories against the hard-mask constraints
python3 living_tales/trainer/tools/validate_trajectories.py amber_cipher --all
```

Training is meant for a GPU runtime (Colab; see `notebooks/scene_lm_colab.ipynb`),
with checkpoints written straight to `OUTPUT_DIR`:

```bash
make train-scene-lm-all  OUTPUT_DIR=/content/drive/MyDrive/living_tales_outputs
make eval-gate-scene-lm  OUTPUT_DIR=/content/drive/MyDrive/living_tales_outputs
make error-analysis-scene-lm OUTPUT_DIR=/content/drive/MyDrive/living_tales_outputs
```

After a checkpoint exists, play it with
`cd living_tales/trainer && python3 tools/pygame_play.py <case> --engine scene_lm --lang en`
(needs `pygame`, which is not in `requirements.txt`; not verified in this sweep).

## Repository layout

```
Makefile                      v3 targets plus legacy pipelines
cases/                        source case specs (JSON)
docs/                         architecture.md, training.md, creature.md (legacy Hopfield-era),
                              cases/ (narrative specs), superpowers/ (v3 design + plan)
evals/                        separate pytest harness (convergence, diversity, chronology, ...)
notebooks/                    Colab notebooks
living_tales/ios/             Swift app consuming packed cartridges
living_tales/trainer/
  trainer/                    models: scene_lm*.py (v3), structured_scene_model_v2.py, legacy
  generator/                  scene_lm_runtime.py, constraints_compiler.py, composer, samplers
  tools/                      train/eval/error-analysis CLIs, validators, play and simulate tools
  cases/<case>/               packed data per case
  tests/                      pytest suite
```

`docs/architecture.md`, `docs/training.md` and `docs/creature.md` describe the earlier
Hopfield/KD/REINFORCE design and the creature track; they predate v3.

## Invariants

- Tokens are symbolic; the engine never reads surface text.
- Trajectories are hand-authored or hand-reviewed, never generated from attractor walks.
- Vocabulary and grammar are baked into each checkpoint; no cross-case bleed.
- Grammar and constraint masks apply at inference.
- Every `phrases.json` entry has English and Spanish.
- Real training runs on Colab, not on a local machine.
