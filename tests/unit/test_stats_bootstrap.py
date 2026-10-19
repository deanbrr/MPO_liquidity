"""Paired bootstrap mechanics (BUILD_SPEC v1.1 §4.4). Owner WP-02.

Calibration on synthetic data is in tests/statistical/test_paired_bootstrap.py. SYNTHETIC values only.
"""

from __future__ import annotations

import dataclasses

import numpy as np
import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.stats import BootstrapResult, paired_bootstrap

GEN = np.random.Generator(np.random.Philox(17))
DIFF = GEN.normal(0.2, 1.0, 3000)


def test_result_fields_and_seed_determinism() -> None:
    r = paired_bootstrap(DIFF, n_boot=1000, seed=3)
    assert isinstance(r, BootstrapResult)
    assert r == paired_bootstrap(DIFF, n_boot=1000, seed=3)
    assert r != paired_bootstrap(DIFF, n_boot=1000, seed=4)
    assert r.mean == pytest.approx(DIFF.mean(), rel=1e-15)
    assert r.lcb < r.mean < r.ucb
    with pytest.raises(dataclasses.FrozenInstanceError):
        r.mean = 0.0  # type: ignore[misc]


def test_iid_se_matches_the_analytic_value() -> None:
    r = paired_bootstrap(DIFF, n_boot=2000)
    assert r.se == pytest.approx(DIFF.std(ddof=1) / np.sqrt(DIFF.size), rel=0.08)   # MC error of the SE ≈ 1.6%


def test_level_controls_the_one_sided_bounds() -> None:
    r95 = paired_bootstrap(DIFF, n_boot=2000, level=0.95)
    r99 = paired_bootstrap(DIFF, n_boot=2000, level=0.99)
    assert r99.lcb < r95.lcb < r95.mean < r95.ucb < r99.ucb
    assert r95.mean - r95.lcb == pytest.approx(1.645 * r95.se, rel=0.1)


def test_block_bootstrap_widens_for_autocorrelated_differences() -> None:
    n, phi = 4000, 0.8
    eps = GEN.normal(size=n)
    ar = np.empty(n)
    ar[0] = eps[0]
    for t in range(1, n):
        ar[t] = phi * ar[t - 1] + eps[t]
    iid = paired_bootstrap(ar, n_boot=1000)
    blk = paired_bootstrap(ar, n_boot=1000, block=50)
    assert blk.se > 1.8 * iid.se                       # long-run sd is (1+φ)/(1−φ) = 9× the variance here
    assert paired_bootstrap(ar, n_boot=200, block=1) == paired_bootstrap(ar, n_boot=200)


def test_large_inputs_are_chunked() -> None:
    big = GEN.normal(size=10_000)
    r = paired_bootstrap(big, n_boot=300, seed=1)
    assert np.isfinite([r.mean, r.se, r.lcb, r.ucb]).all()


@pytest.mark.parametrize(("diff", "kw"), [
    (np.array([1.0]), {}), (np.array([[1.0, 2.0]]), {}), (np.array([1.0, np.nan]), {}),
    (np.arange(10.0), {"n_boot": 1}), (np.arange(10.0), {"level": 0.5}), (np.arange(10.0), {"block": 11}),
    (np.arange(10.0), {"seed": -1}), (np.arange(10.0), {"seed": 1.5}),
])
def test_validation(diff: np.ndarray, kw: dict) -> None:
    with pytest.raises(SchemaError):
        paired_bootstrap(diff, **kw)
