"""PWL proxies of the Tier-2 objective (BUILD_SPEC v1.1 §4.3 tests; §5.3 UTILITY/SHORTFALL; A8). Owner WP-02.

Tangent cuts lie above U and touch it at the points; ``adaptive_tangent_points`` puts ≥ 60% of its points inside
the weighted P10–P90 of the leaf wealth; ``exact_objective`` equals the CRRA/shortfall formula to 1e-12. Wealth in
W₀ units; SYNTHETIC values only.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.numerics import (
    adaptive_tangent_points, crra_tangents, crra_utility, exact_objective, pwl_power, tangent_error_bound,
    weighted_quantile,
)

CRITIQUE_POINTS = [0.60, 0.75, 0.90, 1.00, 1.15, 1.35, 1.60, 2.00]     # BUILD-19's eight points
DEFAULT_BREAKS = (0.0, 0.05, 0.10, 0.20, 0.35, 0.50)                  # ObjectiveSpec.h_shortfall_breaks


@pytest.mark.parametrize("gamma", [1.0, 2.0, 3.0, 6.0])
def test_tangent_cuts_lie_above_u_and_touch_at_the_points(gamma: float) -> None:
    pts = np.array(CRITIQUE_POINTS)
    a, b = crra_tangents(pts, gamma)
    assert np.allclose(a * pts + b, crra_utility(pts, gamma), rtol=0.0, atol=1e-14)
    x = np.linspace(0.2, 5.0, 20001)
    cuts = a[:, None] * x[None, :] + b[:, None]
    assert (cuts >= crra_utility(x, gamma)[None, :] - 1e-14).all()
    assert np.allclose(a, pts ** -gamma)


def test_tangents_keep_input_order_and_validate() -> None:
    a, _ = crra_tangents([2.0, 1.0], 3.0)
    assert a.tolist() == [2.0 ** -3, 1.0]
    for bad in ([0.0, 1.0], [-1.0], [], [math.nan]):
        with pytest.raises(SchemaError):
            crra_tangents(bad, 3.0)
    with pytest.raises(SchemaError):
        crra_tangents([1.0], 0.0)


def _leaves(seed: int) -> tuple[np.ndarray, np.ndarray]:
    gen = np.random.Generator(np.random.Philox(seed))
    wealth = np.exp(gen.normal(0.6, 0.45, 576))                      # leaf W̃/W0 (SYNTHETIC)
    weights = gen.dirichlet(np.full(576, 0.7))
    return wealth, weights


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_adaptive_points_concentrate_inside_weighted_p10_p90(seed: int) -> None:
    wealth, weights = _leaves(seed)
    pts = adaptive_tangent_points(wealth, weights)
    p10, p90 = weighted_quantile(wealth, weights, np.array([0.10, 0.90]))
    assert pts.shape == (48,) and (np.diff(pts) >= 0).all()
    assert np.mean((pts >= p10) & (pts <= p90)) >= 0.60
    assert pts[0] == pytest.approx(weighted_quantile(wealth, weights, 0.01))
    assert pts[-1] == pytest.approx(weighted_quantile(wealth, weights, 0.99))


def test_adaptive_points_validate() -> None:
    wealth, weights = _leaves(4)
    assert adaptive_tangent_points(wealth, weights, n=32).shape == (32,)
    with pytest.raises(SchemaError):
        adaptive_tangent_points(wealth - 10.0, weights)              # non-positive wealth
    with pytest.raises(SchemaError):
        adaptive_tangent_points(wealth, weights, lo_q=0.9, hi_q=0.1)
    with pytest.raises(SchemaError):
        adaptive_tangent_points(wealth, weights, n=0)


def test_pwl_power_has_one_piece_per_break_and_interpolates_the_shortfall() -> None:
    s, t = pwl_power(DEFAULT_BREAKS, 2.0)
    assert s.shape == t.shape == (6,)                                # §5.3: 6 SHORTFALL rows per leaf
    assert (s[0], t[0]) == (0.0, 0.0)
    b = np.array(DEFAULT_BREAKS)

    def psi(x: np.ndarray) -> np.ndarray:
        return np.max(s[:, None] * x[None, :] + t[:, None], axis=0)

    assert np.allclose(psi(b), b ** 2, rtol=0.0, atol=1e-15)
    x = np.linspace(0.0, 0.5, 5001)
    assert (psi(x) >= x ** 2 - 1e-15).all()                          # chords of a convex function lie above it
    assert np.allclose(psi(np.array([-0.3, -1e-9])), 0.0)            # the positive part
    assert (np.diff(s) > 0).all()                                    # convex: slopes increase


def test_pwl_power_validates() -> None:
    for bad in ((0.05, 0.10), (0.0, 0.1, 0.1), (0.0,), (0.0, math.inf)):
        with pytest.raises(SchemaError):
            pwl_power(bad, 2.0)
    with pytest.raises(SchemaError):
        pwl_power(DEFAULT_BREAKS, 0.5)


def test_tangent_error_bound_on_the_critique_points() -> None:
    bound = tangent_error_bound(CRITIQUE_POINTS, 3.0)
    assert bound == pytest.approx(0.15 ** 2 * 3.0 * 0.6 ** -4 / 8.0, rel=1e-12)      # 0.0651 on [0.60, 0.75]
    assert bound == pytest.approx(0.065, abs=5e-4)
    a, b = crra_tangents(CRITIQUE_POINTS, 3.0)
    x = np.linspace(0.6, 2.0, 140001)
    gap = np.min(a[:, None] * x[None, :] + b[:, None], axis=0) - crra_utility(x, 3.0)
    assert gap.max() == pytest.approx(0.041, abs=1e-3)               # the measured maximum gap (BUILD-19)
    assert x[np.argmax(gap)] == pytest.approx(0.66, abs=0.01)
    assert gap.max() <= bound
    assert tangent_error_bound([2.0, 1.0, 1.0], 3.0) == tangent_error_bound([1.0, 2.0], 3.0)   # sorted, unique
    with pytest.raises(SchemaError):
        tangent_error_bound([1.0], 3.0)


def test_exact_objective_equals_the_formula() -> None:
    gen = np.random.Generator(np.random.Philox(9))
    n = 400
    w = np.exp(gen.normal(0.8, 0.5, n))
    w_real = w / 1.28
    p = gen.dirichlet(np.ones(n))
    w_star = np.full(n, 1.1 ** 10)
    gamma, lam, p_exp = 3.0, 1.0, 2.0
    expected = math.fsum(p[i] * (w_real[i] ** (1 - gamma) / (1 - gamma)
                                 - lam * max(0.0, 1 - w[i] / w_star[i]) ** p_exp) for i in range(n))
    got = exact_objective(w, w_real, p, gamma, lam, w_star, p_exp)
    assert abs(got - expected) <= 1e-12
    assert exact_objective(w, w_real, p, gamma, lam, 1.1 ** 10, p_exp) == pytest.approx(got, abs=1e-15)
    log_case = exact_objective(w, w_real, p, 1.0, 0.0, w_star, p_exp)
    assert abs(log_case - math.fsum(p * np.log(w_real))) <= 1e-12


def test_exact_objective_validates() -> None:
    w = np.array([1.0, 2.0])
    p = np.array([0.5, 0.5])
    with pytest.raises(SchemaError):
        exact_objective(w, np.array([1.0, 0.0]), p, 3.0, 1.0, 2.0, 2.0)      # CRRA needs positive real wealth
    with pytest.raises(SchemaError):
        exact_objective(w, w, np.array([1.0]), 3.0, 1.0, 2.0, 2.0)
    with pytest.raises(SchemaError):
        exact_objective(w, w, p, 3.0, -1.0, 2.0, 2.0)
    with pytest.raises(SchemaError):
        exact_objective(np.array([1.0, math.inf]), w, p, 3.0, 1.0, 2.0, 2.0)
    with pytest.raises(SchemaError):
        exact_objective(w, w, np.array([1.5, -0.5]), 3.0, 1.0, 2.0, 2.0)
    with pytest.raises(SchemaError):
        exact_objective(w, w, p, 3.0, 1.0, 0.0, 2.0)                         # a target must be positive
