"""Clopper–Pearson coverage (BUILD_SPEC v1.1 §4.4 tests; ARCH §5.10; §10.6 statistical suite). Owner WP-02.

Nominal ≥ 95% coverage of the one-sided upper bound on Bernoulli(p), p ∈ {0.005, 0.01, 0.02}, n = 50k: exactly (the
binomial probability that the bound reaches p) and by simulation on the lab's own Philox uniforms (400 replications;
basis: SE of a 95% coverage estimate = √(0.95·0.05/400) ≈ 0.011, tolerance 3 SE). At n = 50k, p̂ = 0.90% passes a
1% gate and 1.00% fails. SYNTHETIC draws only.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy import stats

from adic_tpa.contracts.enums import Plane
from adic_tpa.rng import base_entropy, bernoulli, uniforms
from adic_tpa.stats import clopper_pearson

N = 50_000
REPS = 400
PS = [0.005, 0.01, 0.02]


@pytest.mark.parametrize("p", PS)
def test_exact_coverage_is_at_least_nominal(p: float) -> None:
    ks = np.arange(0, int(2 * p * N) + 1)
    upper = np.array([clopper_pearson(int(k), N) for k in ks])
    assert (np.diff(upper) > 0).all()
    k_star = int(ks[np.argmax(upper >= p)])                   # smallest k whose bound reaches p
    coverage = float(stats.binom.sf(k_star - 1, N, p))        # P(K >= k*)
    assert coverage >= 0.95


@pytest.fixture(scope="module")
def replications() -> np.ndarray:
    """u[path, replication]: 50k Bernoulli trials for each of 400 replications (counter month = replication)."""
    base = base_entropy(31, Plane.CALIBRATION, "M1")
    return uniforms(base, "stat.cp_coverage", [None], np.arange(N), np.arange(REPS), 1)[:, :, 0, 0]


@pytest.mark.parametrize("p", PS)
def test_simulated_coverage_on_bernoulli_draws(p: float, replications: np.ndarray) -> None:
    k = bernoulli(replications, p).sum(axis=0)
    covered = np.mean([clopper_pearson(int(x), N) >= p for x in k])
    assert covered >= 0.95 - 3.0 * math.sqrt(0.95 * 0.05 / REPS)
    assert abs(k.mean() / N - p) < 4.0 * math.sqrt(p * (1 - p) / N / REPS)


def test_the_one_percent_gate() -> None:
    assert clopper_pearson(450, N) <= 0.01 < clopper_pearson(500, N)
