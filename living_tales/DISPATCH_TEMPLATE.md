# Trajectory Authoring Dispatch Template

Read this before authoring (or before dispatching a subagent to author) any Living Tales trajectory. Every trajectory authoring task — bootstrap, expansion, quality-pass, refinement — must conform to the rules here.

This template exists because on 2026-06-05 the project produced ~200 trajectories that passed the validator and outcome-balance checks but failed the project's core invariant: **trajectories must be hand-authored**, meaning **each turn is reasoned through by a human (or an LLM reasoning turn-by-turn) — not emitted by a builder script.** The fingerprints of the bug were clear: uniform convergence across dims (`[0.024, 0.024, 0.024]→[0.048, 0.048, 0.048]`), 20+ consecutive turns of detective-alone-in-one-location, uniform 42-turn length, agent-written `/tmp/build_*.py` scripts.

The rules below are designed to make that bug impossible to reproduce.

---

## Hard constraints — these are MUST checks

### 1. No builder scripts

You may NOT write a Python script that emits trajectories by combining template parts. No `gen_wave2_*.py`. No `build_*.py`. No `_author_*.py`. No `_sanitize_*.py`. If a script would let you produce 25 trajectories quickly, that's evidence you're not actually authoring them — you're generating them.

Author each trajectory by *reasoning* through the case turn-by-turn:
- What does the detective do in turn N given turns 1..N-1?
- What location, NPC, object, tell, stance, revelation, beat fits this turn?
- What player card is the detective playing here, and what scene does that card surface?

This is slow. That's the point. **20 well-reasoned trajectories beat 50 scripted ones.**

### 2. The 6 pacing rules

Every trajectory must satisfy all 6:

**P1. Early NPC contact.** First non-`alone` PRESENCE by turn 3-5 at the latest. ≥3 distinct NPCs appear in the first 15 turns. Max 2 consecutive `alone` turns anywhere unless explicitly narratively justified (stake-out scene, deliberate solitary breakthrough — and you must say so in the trajectory `description`).

**P2. Convergence-dim asymmetry.** The 3-vector `convergence_after = [suspect_dim, evidence_dim, motive_dim]` MUST advance non-uniformly. The 3 dims advance from different signals:
- suspect_dim spikes when a name surfaces, a stance shifts to defensive/hostile, or a presence pattern clicks
- evidence_dim spikes when an object is examined that yields a tell, or a contradiction is noticed
- motive_dim spikes when a motive token surfaces or a backstory hook lands

You should NEVER see two consecutive turns where all 3 dims advanced by the same delta. If you find yourself writing `0.024 → 0.048 → 0.072 → 0.096` across all three, STOP — you're scripting, not authoring.

Realistic example: suspect-dim jumps `0.45 → 0.62` on a name-uncovered turn while evidence-dim and motive-dim move `0.50 → 0.51` and `0.40 → 0.41` (small organic drift). Next turn: evidence-dim jumps `0.51 → 0.68` on an object examination while suspect-dim drifts `0.62 → 0.63` and motive-dim sits at `0.41`.

**P3. Location rotation.** Max 4 consecutive turns in the same LOCATION (except stake-out scenes — must be noted in description). ≥5 distinct locations visited per trajectory. A detective who spends 20 turns in `research_lab` examining objects is doing TV-procedural-montage authoring; that's not the bar.

**P4. Object-focus rotation.** Max 3 consecutive turns on the same OBJECT_FOCUS. ~10-15 distinct objects examined per trajectory. Same principle: you don't stare at the same satchel for 5 turns.

**P5. Real stance arcs.** When you revisit an NPC, their STANCE progression must be visible and tied to BOTH turn count AND convergence. A standard arc: `unaware → cooperative → defensive → hostile` over multiple encounters as the detective closes in. STANCE doesn't reset between encounters with the same NPC. If an NPC's first encounter is `defensive` and their second encounter (5 turns later) is also `defensive` with no provocation, you're not tracking their state.

**P6. Length and shape variance.** Across a portfolio of 20 trajectories, length should vary:
- 3-5 speedy trajectories (28-35 turns) — early lock, lucky breaks, modal speedrun
- 8-12 standard (40-47 turns) — main bell curve
- 3-5 slow-burn (48-55 turns) — cold trails, false plateaus, complex motive chains

Uniform 42-turn length across all 20 = script signature.

### 3. Outcome balance

No single outcome class >30% of the trajectory portfolio (counting only trajectories, not CF branches). Use the design doc's outcome list — favor under-represented classes when adding.

### 4. Validator clean

Every trajectory passes `tools/validate_trajectories.py <case_id> --traj <id>` with zero rule violations and zero vocab violations.

---

## Per-case targets (revised 2026-06-05)

| Category | Target |
|---|---|
| Trajectories per case | **20-25** (was 50) |
| Counterfactual branches per case | 10 |
| Phrase pool (top-3 NPCs × 4 stages) | ≥4 variants per cell (en + es) |
| Art prompt sheet | 5 categories covered (per the goal spec) |

Why 20-25 not 50: a single subagent reasoning turn-by-turn through a case can plausibly hand-author ~5-8 trajectories in one run. 4-5 such runs per case gets us to 20-25. 50 forces scripting.

---

## Subagent prompt skeleton

When dispatching a subagent to author trajectories for a case, include the following in the prompt:

```
You are authoring N trajectories for Living Tales case `<case_id>`.

ABSOLUTE CONSTRAINTS:
- You may NOT write a Python script or builder file to generate these trajectories.
  No /tmp/build_*.py, no _author_*.py, no gen_*.py. Author each turn by reasoning,
  not by running code.
- Each trajectory's convergence_after vector must show dim-asymmetry: suspect/evidence/motive
  dims advance from different signals, not uniformly. Equal-rate advancement is a bug.
- First non-`alone` PRESENCE by turn 3-5. ≥3 distinct NPCs in first 15 turns. Max 2
  consecutive `alone` turns.
- Max 4 consecutive turns in same LOCATION. Max 3 on same OBJECT_FOCUS.
- Length must vary: include speedy (~32t), standard (~42t), and slow-burn (~50t) shapes.
- Outcome balance: no class >30%.

WORKFLOW PER TRAJECTORY:
1. Open the design doc and the foundation files. Identify the evidence chain you're going to render.
2. Write the trajectory turn-by-turn. For each turn, ask: where is the detective, who's
   with them, what player card is in play, what scene emerges, and HOW DOES CONVERGENCE
   MOVE (which dim, by how much, driven by what signal in this turn).
3. Validate via `python3 tools/validate_trajectories.py <case_id> --traj <id>`.
4. Self-audit against the 6 pacing rules — if any fail, rewrite the offending turn(s).

REQUIRED READING (in order): living_tales/SCHEMA.md, living_tales/DISPATCH_TEMPLATE.md
(THIS FILE), living_tales/AUTHORING_TRAJECTORIES.md, the case's dimensions.json /
constraints.json / scene_map.json / VOICES.md / phrases.json / beats.json, and 2 example
hand-authored flagship trajectories from amber_cipher (its 39-trajectory baseline IS hand-authored).
```

---

## Quality-pass workflow (for inheriting scaffolded trajectories)

When inheriting scaffolds (script-generated trajectories that pass the validator but fail the pacing rules):

1. Read each existing scaffold's structure: outcome, evidence chain, anchor NPCs, key objects.
2. Throw away the turn-level scene tuples. Keep the high-level shape (outcome, chain, anchors).
3. Re-author the turn-level content by hand-reasoning, following the 6 pacing rules.
4. Select 20-25 from the scaffold pool to refurbish. Move the rest to `trajectories/_scaffolds/` for documentation; they're not used in training.
5. Validate every refurbished trajectory.
6. Run a pacing audit (the 6 rules) on every refurbished trajectory.

---

## When this template does NOT apply

- Foundation files (dimensions, constraints, scene_map, VOICES.md, snippets, phrases, beats) — no pacing dimension. Foundation subagents can be dispatched without this template.
- Art prompt sheets — handled by the `lt-art` skill; no pacing dimension.
- Counterfactual branches — the 6 pacing rules still apply but are scaled down to 5-8 turns. P1 (early NPC contact) may not apply since CFs start mid-case. P2 (dim asymmetry) absolutely does apply. P6 (length variance) doesn't — CF length is what it is.
