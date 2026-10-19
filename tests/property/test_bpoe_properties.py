"""bPOE and CVaR properties (BUILD_SPEC v1.1 §4.4 tests: bPOE ≥ POE and bPOE(CVaR_α threshold) = 1 − α; S-ADR-07).
Owner WP-02.

Samples are distinct multiples of 1/4 (exact, well separated) with optional positive weights; α keeps the tail
mass above the largest atom so CVaR_α lies strictly below the maximum. SYNTHETIC values only.
"""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from adic_tpa.stats import bpoe, cvar

samples = st.lists(st.integers(-4000, 4000), min_size=2, max_size=60, unique=True).map(
    lambda v: np.asarray(v, dtype=np.float64) / 4.0)


def _weights(n: int, data: st.DataObject, weighted: bool) -> np.ndarray | None:
    if not weighted:
        return None
    return np.asarray(data.draw(st.lists(st.floats(0.1, 10.0), min_size=n, max_size=n)), dtype=np.float64)


@settings(max_examples=100, deadline=None)
@given(samples, st.floats(-1100.0, 1100.0), st.booleans(), st.data())
def test_bpoe_dominates_poe(x: np.ndarray, z: float, weighted: bool, data: st.DataObject) -> None:
    w = _weights(x.size, data, weighted)
    p = np.ones(x.size) / x.size if w is None else w / w.sum()
    assert bpoe(x, z, w) >= float(p @ (x > z)) - 1e-12
    assert 0.0 <= bpoe(x, z, w) <= 1.0


@settings(max_examples=100, deadline=None)
@given(samples, st.floats(0.0, 0.99), st.booleans(), st.data())
def test_bpoe_at_the_cvar_threshold_is_one_minus_alpha(x: np.ndarray, alpha: float, weighted: bool,
                                                       data: st.DataObject) -> None:
    w = _weights(x.size, data, weighted)
    p = np.ones(x.size) / x.size if w is None else w / w.sum()
    assume(1.0 - alpha > p[np.argmax(x)] + 1e-9)        # CVaR_α strictly below the maximum
    z = cvar(x, alpha, w)
    assert bpoe(x, z, w) == pytest.approx(1.0 - alpha, abs=1e-9)


@settings(max_examples=100, deadline=None)
@given(samples, st.floats(-1100.0, 1100.0), st.floats(0.0, 50.0))
def test_bpoe_is_non_increasing_in_the_threshold(x: np.ndarray, z: float, dz: float) -> None:
    assert bpoe(x, z + dz) <= bpoe(x, z) + 1e-12


@settings(max_examples=100, deadline=None)
@given(samples, st.floats(0.0, 0.99), st.floats(0.0, 0.99))
def test_cvar_is_monotone_and_bounded(x: np.ndarray, a1: float, a2: float) -> None:
    lo, hi = sorted((a1, a2))
    assert cvar(x, lo) <= cvar(x, hi) + 1e-9
    assert np.quantile(x, hi, method="inverted_cdf") - 1e-9 <= cvar(x, hi) <= x.max() + 1e-9
    assert cvar(x, 0.0) == pytest.approx(float(x.mean()), abs=1e-9)
