# Stories Index

Single ledger for the project-wide completeness goal. Every canonical story (and tracked experimental orphan) gets one row. When every row is green across all five review passes AND the pacing audit, the goal is done.

Last updated: 2026-06-05 (re-spec'd quality-first after drift detected)

## CRITICAL: Primary bar is hand-authored narrative pacing

Validator pass + outcome balance + counts are necessary but NOT sufficient. The 2026-06-05 first wave of dispatched agents produced ~150-200 script-generated trajectories that satisfy these surface metrics but violate the project invariant — uniform convergence across dims, 20+ consecutive alone-and-examining turns, uniform 42-turn length. **All Tier-1 +10 expansions and all Tier-2 wave-1/wave-2 trajectories are scaffolds, not hand-authored.**

The new primary bar enforces 6 hand-pacing rules:

1. **Early NPC contact** — first non-`alone` scene by turn 3-5. ≥3 distinct NPCs in first 15 turns. Max 2 consecutive `alone` turns unless explicitly narratively justified.
2. **Convergence-dim asymmetry** — suspect/evidence/motive dims NEVER advance at identical rates. Equal advancement = script signature.
3. **Location rotation** — max 4 consecutive turns in same LOCATION. ≥5 distinct locations per trajectory.
4. **Object-focus rotation** — max 3 consecutive turns on same OBJECT_FOCUS. ~10-15 distinct objects per trajectory.
5. **Real stance arcs** — revisited NPCs show stance progression tied to turn count AND convergence.
6. **Length/shape variance** — some 32-turn speedy, some 55-turn slow-burn. Uniform = script signature.

## Per-story bar (revised)

Each story must reach:

- **Foundation**: dimensions, tokens, attractor weights, scene_map, voices, phases, constraints, beats (all present, validated). *Unchanged — foundation files have no pacing dimension.*
- **Trajectories**: **20-25 hand-paced** (revised down from 50). Each must pass the 6 pacing rules + outcome balance (no single family >30%) + validator clean.
- **Counterfactual branches**: 10, each anchored on an existing trajectory, single-token divergence, lands on a different outcome class. *Unchanged.*
- **Phrases**: top-3 NPCs × 4 voice-stages × ≥4 variants each, full Spanish parity. *Unchanged.*
- **Art prompts**: per-location backdrops, suspect+witness portraits, briefing establishing shot, verdict ending cards, case-specific UI ornament. *Unchanged — already in good shape per agent reports.*
- **Review passes** (5 narrative + 1 pacing, each must pass twice — independent passes A and B):
  1. Coverage — every dimension & every outcome class represented ≥2× across the trajectory set.
  2. Consistency — voices match VOICES.md; phrases respect voice-stage arcs; no cross-case bleed.
  3. Constraint — every trajectory satisfies hard-mask constraints; chronology respects EARLY → MID → LATE phase order.
  4. Spanish parity — every en string has an es sibling.
  5. Art-narrative alignment — every location/NPC referenced in trajectories has a corresponding art prompt.
  6. **Pacing audit (NEW)** — every trajectory satisfies all 6 hand-pacing rules above.

## Recovery plan for existing scaffolds

The 50/case scaffolded trajectories are NOT scrapped — they get a quality-pass that hand-rewrites pacing per the 6 rules. Existing files become inputs to the rewrite. Final output: 20-25 hand-paced trajectories per case (subset selected from scaffold pool + filled in by hand-authoring). Remaining scaffolds get moved to `trajectories/_scaffolds/` for documentation, not training.

## Legend

- ⬜ not started · 🟡 scaffold (validator-clean but NOT hand-paced) · 🟢 hand-paced · ✅ hand-paced + review passes A+B both clean · ⚠️ blocked/needs review
- "Traj" = trajectory count vs target (20-25 hand-paced)
- "CF" = counterfactual branches vs target (10)
- "Phr" = phrase pool meets top-3×4-stage×≥4-variants bar
- "Art" = art prompt sheet meets B2 spec
- "Pace" = pacing audit (6 rules) passes
- "RA" / "RB" = review pass A / B

---

## Tier 1 — runtime cases

Pre-existing baseline (39-41 trajectories each) was hand-authored at project genesis — keep as-is. The +10 expansions per case (2026-06-05 batch) are scaffolds, need quality pass. CF branches (10/case) are also scaffolds.

| # | Story | Traj | CF | Phr | Art | Pace | RA | RB | Status |
|---|---|---|---|---|---|---|---|---|---|
| 01 | amber_cipher | 🟡 49 (39 hand + 10 scaffold) | 🟡 10 scaffold | 🟡 partial | ✅ 32 prompts | ⬜ | ⬜ | ⬜ | scaffold layer done; quality pass + phrase expand pending |
| 02 | venetian_mirror | 🟡 49 (39 hand + 10 scaffold) | 🟡 10 scaffold | 🟡 partial | ✅ 35 prompts | ⬜ | ⬜ | ⬜ | scaffold layer done; quality pass + phrase expand pending |
| 10 | attended_hour | 🟡 49 (40 hand + 9 scaffold) | 🟡 10 scaffold | 🟡 partial | ✅ 37 prompts ⚠️ | ⬜ | ⬜ | ⬜ | scaffold layer done; quality pass + phrase expand pending |

## Tier 2 — bootstrap (all trajectories scaffolds, need quality pass)

ALL Tier-2 trajectories are scaffolded (validator-clean but script-generated). Quality pass selects best 20-25 per case + hand-rewrites pacing.

| # | Story | Traj | CF | Phr | Art | Pace | RA | RB | Status |
|---|---|---|---|---|---|---|---|---|---|
| 03 | fog_over_brussels | 🟡 50 scaffold | 🟡 10 scaffold | ✅ foundation | ✅ 35 prompts | ⬜ | ⬜ | ⬜ | scaffold layer done; quality pass pending |
| 04 | hollow_season | 🟢 22 hand-paced + 28 scaffold | 🟢 20 hand-paced | ✅ foundation | ✅ 39 prompts | 🟢 self-audited | ⬜ | ⬜ | batches 1+2 + 20 CF complete; out of scope for current 3-case test design |
| 05 | resonance_test | 🟡 50 scaffold | 🟡 10 scaffold | ✅ foundation | ✅ 33 prompts | ⬜ | ⬜ | ⬜ | scaffold layer done; quality pass pending |
| 06 | tidal_interval | 🟢 12 hand-paced + 38 scaffold | 🟡 10 scaffold | ✅ foundation | ✅ 36 prompts | 🟡 partial ⚠️ alone-span soft violation | ⬜ | ⬜ | batch 1 done; alone-spans 4-7 flagged (isolated-station setting); batch 2 + CF dispatched |
| 07 | third_signature | 🟡 50 scaffold | 🟡 10 scaffold | ✅ foundation | ✅ 36 prompts | ⬜ | ⬜ | ⬜ | scaffold layer done; quality pass pending |
| 08 | sulphur_line | 🟡 25 scaffold (wave 2 in flight) | ⬜ pending | ✅ foundation | ⬜ pending | ⬜ | ⬜ | ⬜ | wave 2 in flight |
| 09 | orchard_at_dusk | 🟢 29 hand-paced (31 scaffolds quarantined) | 🟢 10 hand-paced | ✅ foundation | ✅ 31 prompts | 🟢 self-audited | ⬜ | ⬜ | first case fully complete under new bar; correct_thomas_crale 13/39=33% flag for review |

## Tier 3 — bootstrap from design doc only

Note on Adventure cases (A01–A03): per `docs/cases/index.md`, adventures "converge toward a chosen state rather than a fixed truth" and use 4 sequential basins instead of a single mystery. The 50-trajectory / outcome-class bar from mystery cases is replaced by an adventure-shaped bar: per-basin trajectory coverage of every basin-resolution variant + cross-basin chain coherence. Adventure-specific bar will be finalized when the first adventure case (A01) reaches the foundation stage.

| # | Story | Traj | CF | Phr | Art | RA | RB | Status |
|---|---|---|---|---|---|---|---|---|
| 11 | winter_station | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 12 | monsoon_ledger | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 13 | observatory_clock | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 14 | endgame | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 15 | amber_silence | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 16 | signal_fire | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 17 | covenant_garden | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 18 | mountain_exchange | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 19 | instrument_landing | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 2 files | ⬜ | ⬜ | pending |
| 20 | burning_glass | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 1 files | ⬜ | ⬜ | pending |
| 21 | dead_calm | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 1 files | ⬜ | ⬜ | pending |
| A01 | thirteenth_tide | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 1 files | ⬜ | ⬜ | pending |
| A02 | glass_cartographer | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 1 files | ⬜ | ⬜ | pending |
| A03 | iron_cartridge | ⬜ 0/50 | ⬜ 0/10 | ⬜ | ⬜ 1 files | ⬜ | ⬜ | pending |

## Tier 4 — experimental orphans (in trainer/cases, no docs/cases entry)

Triaged 2026-06-05. None in scope — `docs/cases/index.md` lists 24 canonical cases; none of these orphans appear there.

| Story | Decision | Reason |
|---|---|---|
| thornling | excluded | `cartridge_type: TAMAGOTCHI` per spec.json — different game type (infinite-runtime creature game). Mystery-case completeness bar doesn't apply. Tracked separately under "creature games infinite" memory. |
| little_creature | excluded | TAMAGOTCHI-family experiment; v1-engine artifacts (tokens/graph/attractor schema). Not a mystery case. |
| black_ledger | excluded | v1 Hopfield-engine experimental mystery prototype; no `docs/cases/` entry, no `art/` directory, no canonical index slot. v1 path is preserved on disk but not the runtime. |
| dust_and_verdict | excluded | Same as `black_ledger` — v1 experimental, not canonical. |
| neon_blackout | excluded | Same as `black_ledger` — v1 experimental, not canonical. |

### Scale variants (excluded from goal — not separate stories)

- `amber_cipher_L`, `amber_cipher_M` — training-scale variants of `amber_cipher`
- `little_creature_L`, `little_creature_M`, `little_creature_XL` — TAMAGOTCHI scale variants

## Open issues to resolve in cross-story sweep

- **attended_hour style spine conflict**: VOICES.md sketches Briar Clinic as a 1970s-fluorescent conversion; art agent rendered Victorian + gas-lamp for catalogue consistency with amber_cipher and venetian_mirror. Decide: Victorian uniform spine (keep current) OR per-era palette/lighting variation (re-prompt attended_hour to 1970s clinical-fluorescent).
- **attended_hour 1 trajectory short** (49/50): agent worked from manifest baseline of 40 (correct) not my pre-task survey of 41. One extra trajectory needs authoring — batch with the phrase-expansion / review pass for this case.
- **venetian_mirror 1 trajectory short** (49/50): same off-by-one as attended_hour — manifest baseline was 39, my pre-survey said 40. Also note: correct_countess_morvaine at 16/49 = 32.7% if you count only trajectories (over 30% cap), or 16/59 = 27.1% if you include CF branches in denominator. Goal language is ambiguous; review pass to scrutinize and re-balance if needed.
- **amber_cipher 1 trajectory short** (49/50): same off-by-one — manifest baseline was 39 (my pre-survey said 40). One more trajectory needed.
- **Validator extension**: amber_cipher agent added `pre_branch_state` support to `living_tales/trainer/tools/validate_trajectories.py` so CF files can declare initial-convergence state inherited from their source. Existing trajectories unaffected; CFs in other cases (venetian_mirror, attended_hour) used metadata-only schema without needing this — verify cross-case consistency in review.

## Done when

- Every Tier 1/2/3 row above is fully ✅ across Traj, CF, Phr, Art, RA, RB.
- Every Tier 4 row has a Decision != TBD.
- A final cross-story sweep confirms no bleed, consistent style spine, full Spanish parity.
