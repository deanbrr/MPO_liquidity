"""numerics properties (BUILD_SPEC v1.1 §4.3 tests). Owner WP-02.

Tangent cuts lie above U; the tangent error bound dominates the measured gap; secants of (x⁺)^p lie above it and
meet it at the breaks; nearest_correlation returns PSD with unit diagonal; weighted_quantile equals numpy.quantile
under equal weights. SYNTHETIC values only.
"""

from __future__ import annotations

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from adic_tpa.numerics import (
    crra_tangents, crra_utility, nearest_correlation, pwl_power, tangent_error_bound, weighted_quantile,
)

points = st.lists(st.floats(0.05, 20.0), min_size=2, max_size=12, unique=True).map(lambda v: np.sort(np.asarray(v)))
gammas = st.floats(0.5, 8.0)


@settings(max_examples=100, deadline=None)
@given(points, gammas)
def test_tangent_cuts_lie_above_u(pts: np.ndarray, gamma: float) -> None:
    a, b = crra_tangents(pts, gamma)
    x = np.geomspace(pts[0] / 2.0, pts[-1] * 2.0, 2001)
    u = crra_utility(x, gamma)
    cuts = np.min(a[:, None] * x[None, :] + b[:, None], axis=0)
    assert (cuts >= u - 1e-10 * np.maximum(1.0, np.abs(u))).all()


@settings(max_examples=100, deadline=None)
@given(points, gammas)
def test_tangent_bound_dominates_the_gap(pts: np.ndarray, gamma: float) -> None:
    a, b = crra_tangents(pts, gamma)
    x = np.linspace(pts[0], pts[-1], 4001)
    u = crra_utility(x, gamma)
    gap = np.min(a[:, None] * x[None, :] + b[:, None], axis=0) - u
    assert gap.max() <= tangent_error_bound(pts, gamma) * (1 + 1e-9) + 1e-10 * np.abs(u).max()


@settings(max_examples=100, deadline=None)
@given(st.lists(st.floats(0.01, 2.0), min_size=1, max_size=8, unique=True), st.floats(1.0, 4.0))
def test_secants_lie_above_the_power_and_meet_it_at_the_breaks(inner: list[float], p: float) -> None:
    breaks = np.concatenate(([0.0], np.sort(np.asarray(inner))))
    s, t = pwl_power(breaks, p)
    assert s.size == breaks.size

    def psi(x: np.ndarray) -> np.ndarray:
        return np.max(s[:, None] * x[None, :] + t[:, None], axis=0)

    x = np.linspace(0.0, breaks[-1], 2001)
    assert (psi(x) >= x ** p - 1e-12).all()
    assert np.allclose(psi(breaks), breaks ** p, rtol=1e-12, atol=1e-12)
    assert np.allclose(psi(-x[1:]), 0.0)


@settings(max_examples=100, deadline=None)
@given(st.integers(2, 8), st.integers(0, 10 ** 6))
def test_nearest_correlation_is_a_correlation_matrix(n: int, seed: int) -> None:
    gen = np.random.Generator(np.random.Philox(seed))
    a = gen.uniform(-1.0, 1.0, (n, n))
    a = 0.5 * (a + a.T)
    np.fill_diagonal(a, 1.0)
    x = nearest_correlation(a)
    assert np.array_equal(x, x.T)
    assert np.array_equal(np.diag(x), np.ones(n))
    assert np.linalg.eigvalsh(x)[0] >= -1e-12


@settings(max_examples=100, deadline=None)
@given(st.lists(st.floats(-1e6, 1e6), min_size=1, max_size=50), st.lists(st.floats(0.0, 1.0), min_size=1, max_size=9))
def test_weighted_quantile_matches_numpy_under_equal_weights(xs: list[float], qs: list[float]) -> None:
    x = np.asarray(xs)
    q = np.asarray(qs)
    assert np.allclose(weighted_quantile(x, np.ones(x.size), q), np.quantile(x, q), rtol=1e-9, atol=1e-6)
