# GUARDIAN

Automated security / bug-hygiene ledger for this repo, maintained on the `claude/guardian` branch.

## Checks

All run from the repo root unless noted. Throwaway venv at `/tmp/guardian-mtw/venv` (numpy, rich, pytest, ruff, torch from PyPI; CPU only, no training).

| Area | Command |
|---|---|
| Deps | `pip-audit -r living_tales/trainer/requirements.txt` |
| Deps (lockfiles) | `osv-scanner -r .` (no lockfiles; API blocked from sandbox in run 1) |
| Code (SAST) | `bandit -q -r . -ll -x ./living_tales/trainer/tests,./evals/tests,./legacy` |
| Code (grep) | `grep -rnE "\beval\(\|\bexec\(\|pickle\.load\|torch\.load\(\|yaml\.load\(\|shell=True\|verify=False\|allow_origins\|0\.0\.0\.0\|os\.system\(" --include=*.py .` |
| Secrets | `gitleaks detect --source . --redact -v` (full history) and `gitleaks dir . --redact` |
| CI / Docker | `.github/workflows/` and `Dockerfile*`: none present |
| Tests | `cd living_tales/trainer && python -m pytest tests -q`; `cd evals && PYTHONPATH=../living_tales/trainer python -m pytest tests/ -q` |
| Lint | `cd living_tales/trainer && ruff check --isolated --select E9,F63,F7,F82 .` (syntax errors + undefined names; no ruff config in repo) |

## Findings ledger

| id | severity | type | file | status | date |
|---|---|---|---|---|---|
| G-001 | medium | unsafe deserialization (`torch.load(weights_only=False)`), v3 runtime checkpoint loader | living_tales/trainer/trainer/scene_lm.py | fixed | 2026-10-15 |
| G-002 | low | implicit `weights_only` on resume / v2 base checkpoint loads (relied on torch>=2.6 default) | living_tales/trainer/tools/train_scene_lm.py, tools/train_structured_v2.py | fixed | 2026-10-15 |
| G-003 | medium | bug: SyntaxError on Python 3.10/3.11 (backslash in f-string expression), CLI cannot start | living_tales/trainer/tools/playtest_judge.py | fixed | 2026-10-15 |
| G-004 | low | API key sent in URL query string (leaks into logs/tracebacks) | living_tales/trainer/tools/playtest_judge.py | fixed | 2026-10-15 |
| G-005 | low | lint: undefined `Dict`/`Any` in annotations (lazy via `__future__`, not a crash) | living_tales/trainer/tools/pygame_play.py | fixed | 2026-10-15 |
| G-006 | low | bandit B324: SHA1 used for variant picking (not security) | living_tales/trainer/generator/structured_scene_composer.py | fixed (`usedforsecurity=False`) | 2026-10-15 |
| G-007 | low | failing stale test: casebook oscillating mode (start 0.15 + min score are intentional in `core/game_mode.py`) | evals/tests/test_casebook_modes.py | fixed | 2026-10-15 |
| G-008 | medium | unsafe deserialization: 13 legacy/v2 tool `torch.load(..., weights_only=False)` / implicit calls | living_tales/trainer/tools/{play_dialogue,playtest_simulate,pygame_play,visualize,export_onnx,fit_play_report,probe_universal_transfer,train_all_cases,benchmark_models,load_trained_model}.py, trainer/train_policy.py, evals/conftest.py | open | 2026-10-15 |
| G-009 | low | predictable path in shared `/tmp` for sim ledger (bandit B108) | living_tales/trainer/tools/playtest_simulate.py | open | 2026-10-15 |
| G-010 | low | lint: undefined forward-ref names in legacy Hopfield annotations; dead `spec_path` lookup | living_tales/trainer/core/hopfield.py, tools/play_dialogue.py | open | 2026-10-15 |
| G-011 | info | bandit B310 urlopen on hard-coded https API URLs (false positive) | living_tales/trainer/tools/playtest_judge.py | wontfix | 2026-10-15 |

Secrets: gitleaks found nothing in history (51 commits) or the working tree.

## Metrics

| metric | before | after |
|---|---|---|
| open vulns crit / high / med / low (security items only) | 0 / 0 / 2 / 4 | 0 / 0 / 1 / 1 |
| bandit -ll issues (high / med) | 1 / 17 | 0 / 16 (2 newly visible B310 FPs now that playtest_judge parses) |
| dependency vulns (pip-audit) | 0 | 0 |
| failing tests (trainer / evals) | 0 / 1 | 0 / 0 |
| tests passing (trainer / evals) | 50 / 4 (8 skipped) | 111 / 5 (8 skipped) |
| lint errors (E9,F63,F7,F82) | 20 | 5 |
| coverage | not measured | not measured |

## Backlog

- G-008: migrate the remaining v2/legacy loaders to `weights_only=True` after verifying each checkpoint format is plain dicts/tensors/primitives (v2 `config` is `cfg.__dict__`, likely fine; legacy Hopfield/KD checkpoints unverified). Needs a real v2 checkpoint to confirm.
- G-009: use `tempfile` or the case `outputs/` dir for the simulate ledger.
- G-010: add `TYPE_CHECKING` imports in `core/hopfield.py`; drop the dead `spec_path` lookup.
- Pin dependency versions (requirements are unpinned; no lockfile, so audits only cover latest releases).

## Learnings

- `requires-python >=3.10` but the dev box apparently runs 3.12+, so PEP 701 f-strings slipped in; the compile-all-sources test now guards this on whatever interpreter CI/Colab uses.
- v3 `SceneLM` checkpoints are already safe-unpickler-compatible (round-trip test passes with `weights_only=True`).
- download.pytorch.org is unreachable from the sandbox; PyPI torch works (heavier, CUDA wheel, still CPU-only use).

## Ideas

1. Add a minimal CI workflow (SHA-pinned actions, `permissions: contents: read`) running the trainer pytest suite on Python 3.10 and 3.12.
2. Add a shared `safe_load_checkpoint(path)` helper and route every loader through it.
3. Add a repo `ruff.toml` with a small rule set (E9, F) so lint results are reproducible.

## Log

- Run 1 — 2026-10-15 — Initial scan (pip-audit, osv-scanner, bandit, grep, gitleaks history + dir). Fixed unsafe v3 checkpoint loading, a py3.10/3.11 SyntaxError in playtest_judge, API key in URL, stale evals test, lint nits. Trainer tests 50 → 111 passing; evals failures 1 → 0; lint 20 → 5.
