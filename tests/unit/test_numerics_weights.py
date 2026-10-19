"""Weight utilities: log-sum-exp, Kish ESS and weighted quantiles (BUILD_SPEC v1.1 §4.3 tests). Owner WP-02.

``weighted_quantile`` equals ``numpy.quantile`` for equal weights. SYNTHETIC values only.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.numerics import kish_ess, logsumexp_weights, weighted_quantile

Q = np.linspace(0.0, 1.0, 101)


def test_logsumexp_weights_normalize_stably() -> None:
    lw = np.array([0.0, math.log(2.0), math.log(3.0)])
    assert np.allclose(logsumexp_weights(lw), [1 / 6, 2 / 6, 3 / 6], rtol=1e-15)
    big = logsumexp_weights(np.array([1000.0, 1001.0]))
    assert np.allclose(big, [1 / (1 + math.e), math.e / (1 + math.e)])
    assert logsumexp_weights(np.array([-np.inf, 0.0])).tolist() == [0.0, 1.0]
    for bad in (np.array([np.nan, 0.0]), np.array([np.inf, 0.0]), np.array([-np.inf, -np.inf]), np.array([])):
        with pytest.raises(SchemaError):
            logsumexp_weights(bad)


def test_kish_ess() -> None:
    assert kish_ess(np.ones(500)) == 500.0
    assert kish_ess(np.array([0.0, 3.0, 0.0])) == 1.0
    w = np.array([1.0, 2.0, 3.0, 4.0])
    assert kish_ess(w) == pytest.approx(100.0 / 30.0)
    assert kish_ess(7.0 * w) == pytest.approx(kish_ess(w))
    for bad in (np.array([-1.0, 2.0]), np.zeros(3), np.array([[1.0]])):
        with pytest.raises(SchemaError):
            kish_ess(bad)


@pytest.mark.parametrize("n", [1, 2, 3, 10, 577])
def test_equal_weights_reproduce_numpy_quantile(n: int) -> None:
    gen = np.random.Generator(np.random.Philox(n))
    x = gen.normal(size=n)
    assert np.allclose(weighted_quantile(x, np.ones(n), Q), np.quantile(x, Q), rtol=1e-12, atol=1e-14)


def test_ties_scalars_and_zero_weights() -> None:
    x = np.array([3.0, 1.0, 2.0, 2.0, 2.0, 5.0])
    assert np.allclose(weighted_quantile(x, np.full(6, 0.3), Q), np.quantile(x, Q), rtol=1e-12)
    out = weighted_quantile(x, np.ones(6), 0.5)
    assert isinstance(out, np.floating) and out == np.quantile(x, 0.5)
    w = np.array([1.0, 1.0, 0.0, 1.0, 1.0, 0.0])
    keep = w > 0
    assert np.allclose(weighted_quantile(x, w, Q), np.quantile(x[keep], Q), rtol=1e-12)


def test_weights_shift_the_quantile_and_bounds_hold() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    heavy_top = weighted_quantile(x, np.array([1.0, 1.0, 1.0, 10.0]), 0.5)
    assert heavy_top > np.quantile(x, 0.5)
    assert weighted_quantile(x, np.array([1.0, 2.0, 3.0, 4.0]), 0.0) == 0.0
    assert weighted_quantile(x, np.array([1.0, 2.0, 3.0, 4.0]), 1.0) == 3.0


def test_validation() -> None:
    x = np.arange(4.0)
    with pytest.raises(SchemaError):
        weighted_quantile(x, np.ones(3), 0.5)
    with pytest.raises(SchemaError):
        weighted_quantile(x, np.ones(4), 1.5)
    with pytest.raises(SchemaError):
        weighted_quantile(x, np.zeros(4), 0.5)
    with pytest.raises(SchemaError):
        weighted_quantile(np.array([0.0, np.nan]), np.ones(2), 0.5)
