"""Paired-bootstrap calibration (BUILD_SPEC v1.1 §4.4; §10.6 statistical suite). Owner WP-02.

The one-sided 95% bounds cover the true mean difference at ≈ the nominal rate on i.i.d. differences (400
replications; basis: SE of a 95% coverage estimate ≈ 0.011, tolerance 3 SE), and the circular block bootstrap
recovers the long-run standard error of autocorrelated differences (mean over 30 AR(1) samples, within 12%; the
per-sample relative error ≈ √(block/n) ≈ 0.16, so the mean's is ≈ 0.03). SYNTHETIC data only.
"""

from __future__ import annotations

import math

import numpy as np

from adic_tpa.contracts.enums import Plane
from adic_tpa.rng import base_entropy, normal, uniforms
from adic_tpa.stats import paired_bootstrap

BASE = base_entropy(13, Plane.EXPLORATION, "M1")


def test_one_sided_bounds_have_nominal_coverage() -> None:
    reps, n, mu = 400, 200, 0.3
    x = mu + normal(uniforms(BASE, "stat.boot.iid", [None], np.arange(n), np.arange(reps), 1)[:, :, 0, 0])
    lcb_cover = ucb_cover = 0
    for j in range(reps):
        r = paired_bootstrap(x[:, j], n_boot=500, level=0.95, seed=j)
        lcb_cover += r.lcb <= mu
        ucb_cover += r.ucb >= mu
    tol = 3 * math.sqrt(0.95 * 0.05 / reps)
    assert lcb_cover / reps >= 0.95 - tol
    assert ucb_cover / reps >= 0.95 - tol


def test_block_bootstrap_recovers_the_long_run_standard_error() -> None:
    n, phi, block, samples = 4000, 0.5, 100, 30
    eps = normal(uniforms(BASE, "stat.boot.ar1", [None], np.arange(n), np.arange(samples), 1)[:, :, 0, 0])
    ses = []
    for j in range(samples):
        x = np.empty(n)
        x[0] = eps[0, j] / math.sqrt(1 - phi * phi)            # stationary start
        for t in range(1, n):
            x[t] = phi * x[t - 1] + eps[t, j]
        ses.append(paired_bootstrap(x, n_boot=300, block=block, seed=j).se)
    true_se = 1.0 / (1.0 - phi) / math.sqrt(n)                 # long-run sd of an AR(1) mean
    assert abs(np.mean(ses) / true_se - 1.0) < 0.12
