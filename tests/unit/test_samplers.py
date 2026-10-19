"""Closed-form samplers and the truncated t (BUILD_SPEC v1.1 §4.2: vectorized inverse CDF, one uniform per
variate). Owner WP-02. SYNTHETIC values only."""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy import special

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.rng import (
    U_MIN, bernoulli, categorical, exponential, gamma, kou_jump, normal, student_t, truncated_t,
)

U = (np.arange(1, 4001, dtype=np.float64) - 0.5) / 4000.0          # stratified uniforms in (0, 1)


def test_normal_is_ndtri_and_finite_at_zero() -> None:
    assert np.array_equal(normal(U), special.ndtri(U))
    z = normal(np.array([0.0, 1.0 - 2.0 ** -53]))
    assert np.isfinite(z).all() and z[0] == special.ndtri(U_MIN)


def test_exponential() -> None:
    assert np.allclose(exponential(U, 2.0), -np.log1p(-U) / 2.0, rtol=1e-15)
    assert exponential(np.array([0.0]), 1.0)[0] == 0.0
    rates = np.array([1.0, 4.0])
    assert exponential(np.array([0.5, 0.5]), rates).tolist() == pytest.approx([math.log(2), math.log(2) / 4])
    with pytest.raises(SchemaError):
        exponential(U, 0.0)


def test_bernoulli() -> None:
    assert bernoulli(np.array([0.1, 0.3, 0.5]), 0.3).tolist() == [True, False, False]
    assert not bernoulli(U, 0.0).any() and bernoulli(U, 1.0).all()
    assert bernoulli(U, 0.25).mean() == pytest.approx(0.25)
    assert bernoulli(np.array([0.2, 0.2]), np.array([0.1, 0.3])).tolist() == [False, True]
    with pytest.raises(SchemaError):
        bernoulli(U, 1.5)


def test_categorical_boundaries_and_broadcasting() -> None:
    cum = np.array([0.2, 0.5, 1.0])
    got = categorical(np.array([0.0, 0.1999, 0.2, 0.49, 0.5, 0.99]), cum)
    assert got.dtype == np.int8 and got.tolist() == [0, 0, 1, 1, 2, 2]
    rows = np.array([[0.5, 1.0], [0.1, 1.0]])
    assert categorical(np.array([0.3, 0.3]), rows).tolist() == [0, 1]
    assert np.bincount(categorical(U, cum)).tolist() == [800, 1200, 2000]
    with pytest.raises(SchemaError):
        categorical(U, np.array([0.2, 0.9]))            # last != 1
    with pytest.raises(SchemaError):
        categorical(U, np.array([0.5, 0.4, 1.0]))       # decreasing
    with pytest.raises(SchemaError):
        categorical(U, np.linspace(0.0, 1.0, 200))      # > 127 categories


def test_kou_jump_mechanics() -> None:
    zeros = kou_jump(U, U, U, lam=0.0, eta_up=10.0, eta_dn=5.0, p_up=0.4)
    assert not zeros.any()
    always = kou_jump(np.zeros_like(U), U, U[::-1], lam=50.0, eta_up=10.0, eta_dn=5.0, p_up=0.4)
    up = U[::-1] < 0.4
    assert np.allclose(always[up], -np.log1p(-U[up]) / 10.0) and (always[up] > 0).all()
    assert np.allclose(always[~up], np.log1p(-U[~up]) / 5.0) and (always[~up] < 0).all()
    # occurrence probability 1 − e^{−λ}
    lam = 0.05
    occurred = kou_jump(U, np.full_like(U, 0.5), np.full_like(U, 0.1), lam, 10.0, 5.0, 0.4) != 0
    assert occurred.mean() == pytest.approx(-math.expm1(-lam), abs=1.0 / U.size)
    with pytest.raises(SchemaError):
        kou_jump(U, U, U, lam=-1.0, eta_up=1.0, eta_dn=1.0, p_up=0.5)


@pytest.mark.parametrize(("lo", "hi"), [(-1.0, 2.0), (-math.inf, -3.0), (0.5, math.inf), (4.0, 9.0), (-9.0, -4.0)])
def test_truncated_t_matches_the_mapped_quantile(lo: float, hi: float) -> None:
    df = 5.0
    got = truncated_t(U, df, lo, hi)
    assert (got >= lo).all() and (got <= hi).all()
    if lo >= 0:      # upper intervals: reference through survival probabilities
        s_lo, s_hi = special.stdtr(df, -lo), special.stdtr(df, -hi)
        ref = -special.stdtrit(df, s_lo - U * (s_lo - s_hi))
    else:
        f_lo, f_hi = special.stdtr(df, lo), special.stdtr(df, hi)
        ref = special.stdtrit(df, f_lo + U * (f_hi - f_lo))
    assert np.abs(got - ref).max() < 1e-7


def test_truncated_t_standardized_bounds_and_errors() -> None:
    x = truncated_t(U, 5.0, -0.5, 0.5, standardize=True)
    assert (np.abs(x) <= 0.5).all()
    raw = truncated_t(U, 5.0, -0.5 / math.sqrt(0.6), 0.5 / math.sqrt(0.6))
    assert np.allclose(x, math.sqrt(0.6) * raw, rtol=1e-12, atol=1e-15)
    with pytest.raises(SchemaError):
        truncated_t(U, 5.0, 1.0, 1.0)
    with pytest.raises(SchemaError):
        truncated_t(U, 5.0, 1e300, math.inf)            # no mass
    with pytest.raises(SchemaError):
        student_t(U, 2.0)                               # standardize needs df > 2


@pytest.mark.parametrize("bad", [np.array([1.0]), np.array([-0.1]), np.array([np.nan]), np.array([0.2, 1.5])])
def test_every_sampler_rejects_values_outside_the_unit_interval(bad: np.ndarray) -> None:
    calls = [lambda u: normal(u), lambda u: student_t(u, 5.0), lambda u: truncated_t(u, 5.0, -1.0, 1.0),
             lambda u: gamma(u, 2.0), lambda u: exponential(u, 1.0), lambda u: bernoulli(u, 0.5),
             lambda u: categorical(u, np.array([0.5, 1.0])), lambda u: kou_jump(u, u, u, 0.1, 5.0, 5.0, 0.5)]
    for call in calls:
        with pytest.raises(SchemaError):
            call(bad)


def test_one_uniform_per_variate_shapes() -> None:
    u = U.reshape(40, 10, 10)
    for out in (normal(u), student_t(u, 5.0), truncated_t(u, 5.0, -2.0, 2.0), gamma(u, 2.0), exponential(u, 1.0),
                bernoulli(u, 0.5), categorical(u, np.array([0.5, 1.0])), kou_jump(u, u, u, 0.1, 5.0, 5.0, 0.5)):
        assert out.shape == u.shape


def test_parameter_validation() -> None:
    for call in (lambda: gamma(U, 0.0), lambda: gamma(U, 2.0, scale=-1.0), lambda: student_t(U, math.nan),
                 lambda: kou_jump(U, U, U, 0.1, 0.0, 1.0, 0.5), lambda: kou_jump(U, U, U, 0.1, 1.0, 1.0, 1.5)):
        with pytest.raises(SchemaError):
            call()


def test_a_table_that_cannot_reach_its_tolerance_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    from adic_tpa.contracts.errors import SolverError
    from adic_tpa.rng import samplers

    monkeypatch.setattr(samplers, "_TABLE_N_MAX", samplers._TABLE_N0)       # no refinement allowed
    with pytest.raises(SolverError):
        samplers._gamma_table(1.2345678)                                      # an uncached shape


def test_read_only_inputs_are_accepted() -> None:
    ro = U.copy()
    ro.flags.writeable = False
    assert np.array_equal(student_t(ro, 5.0), student_t(U, 5.0))
    assert np.array_equal(gamma(ro, 3.0), gamma(U, 3.0))
