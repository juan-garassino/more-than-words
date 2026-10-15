import numpy as np
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "living_tales" / "trainer"))

from core.casebook import CasebookState
from core.game_mode import default_initial_dimension_value


def test_converging_mode_never_decreases_dimensions():
    state = CasebookState.create(n_dims=2, mode="converging", convergence_rate=0.5)
    state.apply_delta(np.array([0.4, 0.2], dtype=np.float32))
    after_positive = state.convergence_dimensions.copy()
    state.apply_delta(np.array([-0.5, -0.5], dtype=np.float32))
    assert np.allclose(state.convergence_dimensions, after_positive)


def test_oscillating_mode_uses_needy_start_and_supports_drop():
    # Oscillating (creature) mode deliberately starts "needy" (game_mode.py),
    # not at the midpoint; it must still move both down and up from there.
    start = default_initial_dimension_value("oscillating")
    state = CasebookState.create(n_dims=2, mode="oscillating", convergence_rate=0.5)
    assert np.allclose(state.convergence_dimensions, np.array([start, start], dtype=np.float32))
    state.apply_delta(np.array([-0.1, 0.2], dtype=np.float32))
    assert state.convergence_dimensions[0] < start
    assert state.convergence_dimensions[1] > start
    # Score is the weakest dimension (min) in both modes (game_mode.score_dimensions).
    assert abs(state.convergence_score - float(state.convergence_dimensions.min())) < 1e-6
