"""Holm controls FWER and α-investing controls mFDR on 2,000 synthetic null campaigns (BUILD_SPEC v1.1 §4.4 tests,
§7.7; §10.6 statistical suite). Owner WP-02.

p-values are the lab's own Philox uniforms (exact nulls). Basis: FWER and mFDR estimates are compared with the
nominal 0.05 plus 2 Monte Carlo SE (binomial SE for FWER; delta-method SE for the ratio mFDR_η = E[V]/(E[R] + η),
η = W₀/payout = 1). A mixed campaign with 30% strong true effects checks that discoveries do not let false ones
through. SYNTHETIC campaigns only.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import special

from adic_tpa.contracts.enums import Plane
from adic_tpa.rng import base_entropy, normal, uniforms
from adic_tpa.stats import AlphaInvesting, holm

BASE = base_entropy(77, Plane.EXPLORATION, "M1")
CAMPAIGNS = 2000
ALPHA = 0.05


def _uniform_rows(source: str, m: int) -> np.ndarray:
    return uniforms(BASE, source, [None], np.arange(CAMPAIGNS), np.array([0]), m)[:, 0, 0, :]


def _ratio_se(v: np.ndarray, r: np.ndarray, eta: float) -> float:
    b = r.mean() + eta
    ratio = v.mean() / b
    var = (v.var(ddof=1) - 2 * ratio * np.cov(v, r)[0, 1] + ratio ** 2 * r.var(ddof=1)) / (v.size * b * b)
    return math.sqrt(max(var, 0.0))


def test_holm_controls_fwer_on_independent_nulls() -> None:
    p = _uniform_rows("stat.holm.null", 10)
    fwer = np.mean([any(holm(row, ALPHA)) for row in p])
    assert fwer <= ALPHA + 2 * math.sqrt(ALPHA * (1 - ALPHA) / CAMPAIGNS)


def test_holm_controls_fwer_under_positive_dependence() -> None:
    z = normal(_uniform_rows("stat.holm.dep", 11))
    rho = 0.5
    stat = math.sqrt(rho) * z[:, :1] + math.sqrt(1 - rho) * z[:, 1:]     # equicorrelated one-sided z-tests
    p = special.ndtr(-stat)
    fwer = np.mean([any(holm(row, ALPHA)) for row in p])
    assert fwer <= ALPHA + 2 * math.sqrt(ALPHA * (1 - ALPHA) / CAMPAIGNS)


def _run_ledgers(p: np.ndarray, null: np.ndarray, decay: float) -> tuple[np.ndarray, np.ndarray, float]:
    v = np.zeros(p.shape[0])
    r = np.zeros(p.shape[0])
    eta = 1.0
    for i, row in enumerate(p):
        ai = AlphaInvesting(decay=decay)
        eta = ai.eta
        rejected = np.array([ai.test(float(x)) for x in row])
        r[i] = rejected.sum()
        v[i] = (rejected & null[i]).sum()
    return v, r, eta


def test_alpha_investing_controls_mfdr_on_null_campaigns() -> None:
    for decay in (0.9, 0.0):                                  # the default and the research's all-in rule
        p = _uniform_rows(f"stat.alpha_investing.null.{decay}", 24)
        v, r, eta = _run_ledgers(p, np.ones(p.shape, dtype=bool), decay)
        mfdr = v.mean() / (r.mean() + eta)
        assert mfdr <= ALPHA + 2 * _ratio_se(v, r, eta), (decay, mfdr)
        assert v.mean() > 0                                   # the ledger does spend its wealth


def test_alpha_investing_controls_mfdr_with_true_discoveries() -> None:
    u = uniforms(BASE, "stat.alpha_investing.mixed", [None], np.arange(CAMPAIGNS), np.array([0]), 48)[:, 0, 0, :]
    null = u[:, 24:] >= 0.3                                   # 70% nulls
    p = np.where(null, u[:, :24], u[:, :24] ** (1 / 0.05))   # non-nulls: p ~ Beta(0.05, 1), strong evidence
    v, r, eta = _run_ledgers(p, null, 0.9)
    mfdr = v.mean() / (r.mean() + eta)
    assert r.mean() > 3 * v.mean()                            # real discoveries dominate
    assert mfdr <= ALPHA + 2 * _ratio_se(v, r, eta)
