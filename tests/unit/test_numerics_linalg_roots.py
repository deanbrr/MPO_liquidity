"""Nearest correlation matrix and bracketed root finding (BUILD_SPEC v1.1 §4.3 tests). Owner WP-02.

``nearest_correlation`` returns a PSD matrix with unit diagonal (Higham 2002, with its published 3×3 example);
``brentq`` raises ``SolverError`` on every failure. SYNTHETIC values only.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from adic_tpa.contracts.errors import SchemaError, SolverError
from adic_tpa.numerics import brentq, nearest_correlation


def _random_symmetric(n: int, seed: int) -> np.ndarray:
    gen = np.random.Generator(np.random.Philox(seed))
    a = gen.uniform(-1.0, 1.0, (n, n))
    a = 0.5 * (a + a.T)
    np.fill_diagonal(a, 1.0)
    return a


def test_higham_2002_example() -> None:
    a = np.array([[1.0, 1.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0]])
    x = nearest_correlation(a)
    expected = np.array([[1.0, 0.7607, 0.1573], [0.7607, 1.0, 0.7607], [0.1573, 0.7607, 1.0]])
    assert np.allclose(x, expected, atol=1e-4)
    assert np.linalg.norm(x - a) == pytest.approx(0.5278, abs=1e-4)


@pytest.mark.parametrize(("n", "seed"), [(4, 2), (12, 2), (20, 3), (40, 4)])
def test_output_is_psd_symmetric_with_unit_diagonal(n: int, seed: int) -> None:
    a = _random_symmetric(n, seed)
    assert np.linalg.eigvalsh(a)[0] < 0                             # the input really is indefinite
    x = nearest_correlation(a)
    assert np.array_equal(x, x.T)
    assert np.array_equal(np.diag(x), np.ones(n))
    assert np.linalg.eigvalsh(x)[0] >= -1e-12
    assert (np.abs(x) <= 1.0 + 1e-12).all()


def test_a_valid_correlation_matrix_is_returned_unchanged() -> None:
    gen = np.random.Generator(np.random.Philox(5))
    f = gen.normal(size=(6, 3))
    c = f @ f.T + np.diag(np.full(6, 0.5))
    d = np.sqrt(np.diag(c))
    c = c / np.outer(d, d)
    np.fill_diagonal(c, 1.0)
    c = 0.5 * (c + c.T)
    assert np.array_equal(nearest_correlation(c), c)


def test_blend_repair_as_engine_e_uses_it() -> None:
    r0 = np.array([[1.0, 0.3], [0.3, 1.0]])
    r_crisis = np.array([[1.0, 0.9], [0.9, 1.0]])
    blend = 0.6 * r0 + 0.4 * r_crisis                                 # already a correlation matrix
    assert np.array_equal(nearest_correlation(blend), blend)


def test_errors() -> None:
    with pytest.raises(SchemaError):
        nearest_correlation(np.ones((2, 3)))
    with pytest.raises(SchemaError):
        nearest_correlation(np.array([[1.0, math.nan], [math.nan, 1.0]]))
    with pytest.raises(SolverError) as exc:
        nearest_correlation(_random_symmetric(20, 3), maxiter=2)
    assert exc.value.code == "SOLVER_NONOPTIMAL"


def test_brentq_finds_roots_to_tolerance() -> None:
    assert brentq(lambda x: x * x - 2.0, 0.0, 2.0) == pytest.approx(math.sqrt(2.0), abs=1e-12)
    assert brentq(lambda x: math.exp(x) - 3.0, -5.0, 5.0, xtol=1e-14) == pytest.approx(math.log(3.0), abs=1e-13)
    assert brentq(lambda x: x, 0.0, 1.0) == 0.0                     # exact zero at an end
    assert brentq(lambda x: x - 1.0, 0.0, 1.0) == 1.0


@pytest.mark.parametrize(("f", "lo", "hi"), [
    (lambda x: x * x + 1.0, -1.0, 1.0),                            # no sign change
    (lambda x: math.inf if x > 0.5 else -1.0, 0.0, 1.0),            # non-finite end value
    (lambda x: x, 1.0, 0.0),                                        # empty bracket
    (lambda x: x, -math.inf, 1.0),
])
def test_brentq_raises_solver_error(f, lo: float, hi: float) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(SolverError):
        brentq(f, lo, hi)


def test_brentq_reports_non_convergence() -> None:
    with pytest.raises(SolverError):
        brentq(lambda x: x ** 3 - 0.123456789, 0.0, 1.0, xtol=1e-300, maxiter=2)
