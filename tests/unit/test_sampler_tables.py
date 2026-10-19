"""Tabulated inverse CDFs (BUILD_SPEC v1.1 §4.2 tests; S-ADR-38). Owner WP-02.

The tabulated Student t and gamma quantiles are within 1e-7 (absolute) of scipy's ``stdtrit``/``gammaincinv`` on a
dense grid that includes both extreme tails of the generator's 2^-53 grid; the standardized t₅ has variance 1 ±
0.005 on 1e6 draws. Sampling-error basis for the variance check: SE of the sample variance of a unit-variance t₅ is
√((E[X⁴] − 1)/n) = √(8/n) ≈ 0.0028 at n = 1e6 (fixed seed). SYNTHETIC seeds only.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy import special

from adic_tpa.contracts.enums import Plane
from adic_tpa.rng import U_MIN, base_entropy, gamma, student_t, uniforms

TOL = 1e-7


def _dense_grid() -> np.ndarray:
    k = np.arange(1, 1001, dtype=np.float64)
    parts = [k * 2.0 ** -53, np.logspace(-16, math.log10(0.5), 12000), np.linspace(0.0, 1.0, 12001)[:-1],
             1.0 - np.logspace(-15.9, math.log10(0.5), 12000), 1.0 - k * 2.0 ** -53, np.array([0.5])]
    g = np.unique(np.concatenate(parts))
    return g[(g >= 0.0) & (g < 1.0)]


GRID = _dense_grid()
GRID_CLAMPED = np.maximum(GRID, U_MIN)


@pytest.mark.parametrize("df", [2.5, 3.0, 4.0, 5.0, 8.0, 30.0, 100.0])
def test_student_t_table_within_1e7_of_stdtrit(df: float) -> None:
    got = student_t(GRID, df, standardize=False)
    ref = special.stdtrit(df, GRID_CLAMPED)
    err = np.abs(got - ref)
    assert err.max() < TOL, f"df={df}: max abs error {err.max():.3e} at u={GRID[np.argmax(err)]:.3e}"
    assert np.isfinite(got).all()


@pytest.mark.parametrize("shape", [0.05, 0.3, 1.0, 2.5, 7.5, 50.0, 500.0])
def test_gamma_table_within_1e7_of_gammaincinv(shape: float) -> None:
    got = gamma(GRID, shape)
    ref = special.gammaincinv(shape, GRID_CLAMPED)
    err = np.abs(got - ref)
    assert err.max() < TOL, f"shape={shape}: max abs error {err.max():.3e} at u={GRID[np.argmax(err)]:.3e}"


def test_tails_reach_the_generator_extremes() -> None:
    k = np.arange(1, 50, dtype=np.float64)
    lo, hi = k * 2.0 ** -53, 1.0 - k * 2.0 ** -53
    # t5 at u = 2^-53 is about -2434: the absolute bound there needs ~4e-11 relative accuracy (the tail expansion)
    assert np.abs(student_t(lo, 5.0, standardize=False) - special.stdtrit(5.0, lo)).max() < TOL
    assert np.abs(student_t(hi, 5.0, standardize=False) - special.stdtrit(5.0, hi)).max() < TOL
    assert np.abs(gamma(hi, 2.5) - special.gammaincinv(2.5, hi)).max() < TOL


def test_symmetry_on_the_generator_grid_is_exact() -> None:
    u = np.arange(1, 2 ** 12, dtype=np.float64) * 2.0 ** -13          # k·2^-13: 1 − u is exact
    assert np.array_equal(student_t(1.0 - u, 5.0), -student_t(u, 5.0))


def test_quantiles_are_monotone_and_scaled() -> None:
    assert (np.diff(student_t(GRID, 5.0)) >= 0).all()
    assert (np.diff(gamma(GRID, 2.5)) >= 0).all()
    raw = student_t(GRID, 5.0, standardize=False)
    assert np.allclose(student_t(GRID, 5.0), math.sqrt(3.0 / 5.0) * raw, rtol=1e-15, atol=0.0)
    assert np.allclose(gamma(GRID, 2.5, 3.0), 3.0 * gamma(GRID, 2.5), rtol=1e-15, atol=0.0)


def test_u_zero_maps_to_the_half_grid_step() -> None:
    assert student_t(np.array([0.0]), 5.0, standardize=False)[0] == pytest.approx(special.stdtrit(5.0, U_MIN),
                                                                                  rel=1e-12)
    assert np.isfinite(gamma(np.array([0.0]), 0.3)).all()


def test_standardized_t5_has_unit_variance_on_1e6_draws() -> None:
    base = base_entropy(5, Plane.CALIBRATION, "M1")
    u = uniforms(base, "scen.eps", [None], np.arange(62_500), np.arange(4), 4).reshape(-1)
    assert u.size == 1_000_000
    x = student_t(u, 5.0)
    assert abs(float(np.var(x)) - 1.0) < 0.005
    assert abs(float(np.mean(x))) < 0.005                               # SE of the mean 0.001
