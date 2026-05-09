# Living Tales

Living Tales is a symbolic mystery game where a per-case overfitted transformer co-narrates with the player through token dialogue. The current production engine is **v2** — a 5.3M-param multidimensional structured-scene transformer with a shared base + per-case LoRA adapters. The legacy Hopfield/KD/REINFORCE path is preserved on disk but is no longer the runtime.

There is **no LLM at runtime.** The engine emits token IDs over a per-dim vocabulary; the composer slot-fills hand-authored phrases (`phrases.json`) into Obra-Dinn third-person past prose. Tokens are symbolic; the model never sees or emits natural language.

## Game Loop

Player plays a symbolic card → model emits a complete 11-13-dim scene tuple (LOCATION, TRANSITION, CAUSE, PRESENCE, STANCE, ACTION, OBJECT_FOCUS, TELL, ATMOSPHERE, REVELATION, BEAT, plus case-specific MEDICAL_TELL / ART_TELL) → composer renders prose → repeat. Convergence accumulates from token attractor weights; discovery beats fire at authored thresholds; player accuses to solve.

## V2 Architecture

- **`StructuredSceneTransformerV2`** (`trainer/structured_scene_model_v2.py`): 4 layers, hidden_dim=256, 8 heads, RoPE, max_history=160. Cross-head decoder over dim queries; played-card dedicated KV slot; latent scene-type z (8 modes); LoRA hooks on every linear.
- **Two-stage training** (`tools/train_structured_v2.py`):
  - Stage 1 (`base`): pretrain on union universal-core corpus across all cases. Only universal dims get supervision (case-specific dims masked via `active_mask`). Saves `outputs/_base/base_universal.pt`.
  - Stage 2 (`adapter`): freeze base, train LoRA branches + case-specific heads. Saves `outputs/<case>/v2_full.pt`.
- **TrajectoryDatasetV2** (`trainer/trajectory_dataset_v2.py`): supports universal-only mode, history-truncation augmentation, counterfactual-branch sampling, scene_type / forbidden_dims / active_mask.
- **Discovery beats** (`generator/discovery_beats.py` + `cases/<case>/beats.json`): convergence-threshold scaffolding fires REVELATION/BEAT injections (closing-arc rescue while training data is thin).
- **Composer** (`generator/structured_scene_composer.py`): variant picker (hash-stable on `(turn_idx, token_id)`); voice-arc stages (cold/warming/breaking/broken) for top-3 NPCs per case.

## Cases

| Case | Trajectories | Case-specific dims |
|---|---|---|
| amber_cipher | 39 | none |
| attended_hour | 40 | MEDICAL_TELL |
| venetian_mirror | 39 | ART_TELL |

Total: 118 trajectories (target was 50/case = 150). New outcome classes added: partial_correct, accomplice_found, framed_suspect, motive_only_confession, late_revelation, near_miss.

## Key Commands

```bash
# Author + validate
python3 living_tales/trainer/tools/validate_trajectories.py <case> --all
python3 living_tales/trainer/tools/author_live.py <case> <traj_id>      # live composer preview

# Train (Colab only — never local)
make train-v2-base   OUTPUT_DIR=/content/drive/MyDrive/living_tales_outputs
make train-v2-all    OUTPUT_DIR=/content/drive/MyDrive/living_tales_outputs
make eval-gate       # probe + 5-seed × 3-case judge sweep

# Play
cd living_tales/trainer && python3 tools/pygame_play.py <case> --lang en

# Simulate (with claude_subagent / openai / gemini judge)
python3 tools/playtest_simulate.py <case> --n 3 --max-turns 25 --seed 1
```

## Invariants (Non-Negotiable)

- Engine never reads surface expressions; tokens are symbolic.
- All trajectories are hand-authored (or hand-reviewed); no programmatic generation from attractor walks.
- Cross-case bleed is forbidden: per-case vocab restriction at inference (will move to per-case checkpoint baking).
- Convergence is player-guided (driven by token attractor weights), not automatic time-based — runtime placeholders are scaffolding to remove.
- Hard-mask constraints apply at inference; soft penalty at training is on the roadmap.
- Spanish parity: every phrases.json entry has en + es.
- Train on Colab, never local.

## Known Issues / Roadmap

- **Modal-token collapse** on REVELATION (`confirmation`) and TRANSITION (`stayed`) — `lambda_div=0.05` was too weak; bump to 0.20 next retrain.
- **NPC interview-stage tracking** absent in runtime — voice-arcs stay at "cold" stage forever. Easy fix.
- **Convergence accumulator placeholder** (+0.04/turn) bypasses real attractor-weight signal — restore proper accumulator.
- **Per-case vocab restriction** is a runtime wrapper; should be baked into adapter checkpoints.
- **Hard-mask only at inference** — train-time soft penalty would harden constraint coverage.
- **Phrase pool thin per token** — many top-NPC phrases have 1 cold-stage variant; need 4-6 variants × 4 stages.

## What to Optimize

- Diversity-loss weight + counterfactual-branch density (cures head collapse).
- More trajectories per case (50 → 65 → 90 in three thresholds).
- Phrase variant richness, especially top-NPC voice-arc stages.
- Train-time hard-mask penalty (kills inference-time slips).
- Convergence purity — drive only from attractor weights, no constant boosts.
