"""Clopper–Pearson bounds (BUILD_SPEC v1.1 §4.4; ARCH §5.10). Owner WP-02.

At n = 50k, p̂ = 0.90% passes a 1% gate and 1.00% fails; bounds agree with scipy's exact binomial interval; the
importance-sampled bound equals the plain one under equal weights. SYNTHETIC counts only.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.stats import clopper_pearson, is_cp_upper


def test_the_one_percent_gate_at_50k_paths() -> None:
    assert clopper_pearson(450, 50_000) <= 0.01            # p̂ = 0.90% passes
    assert clopper_pearson(500, 50_000) > 0.01             # p̂ = 1.00% fails


def test_closed_forms_at_the_edges() -> None:
    n, alpha = 200, 0.05
    assert clopper_pearson(0, n, alpha) == pytest.approx(1.0 - alpha ** (1.0 / n), rel=1e-12)
    assert clopper_pearson(n, n) == 1.0
    assert clopper_pearson(0, n, side="two") == (0.0, pytest.approx(1.0 - (alpha / 2) ** (1.0 / n), rel=1e-12))
    lo, hi = clopper_pearson(n, n, side="two")
    assert hi == 1.0 and lo == pytest.approx((alpha / 2) ** (1.0 / n), rel=1e-12)


@pytest.mark.parametrize(("k", "n"), [(1, 10), (7, 1000), (450, 50_000), (999, 1000)])
def test_two_sided_matches_scipy_exact_interval(k: int, n: int) -> None:
    ci = stats.binomtest(k, n).proportion_ci(confidence_level=0.95, method="exact")
    lo, hi = clopper_pearson(k, n, side="two")
    assert lo == pytest.approx(ci.low, rel=1e-10) and hi == pytest.approx(ci.high, rel=1e-10)


def test_upper_bound_is_monotone_in_k_and_alpha() -> None:
    ups = [clopper_pearson(k, 1000) for k in range(0, 50)]
    assert (np.diff(ups) > 0).all()
    assert clopper_pearson(5, 1000, alpha=0.01) > clopper_pearson(5, 1000, alpha=0.05)


@pytest.mark.parametrize(("k", "n", "kw"), [(-1, 10, {}), (11, 10, {}), (1, 0, {}), (1.5, 10, {}),
                                            (1, 10, {"alpha": 0.0}), (1, 10, {"side": "lower"})])
def test_validation(k: object, n: object, kw: dict) -> None:
    with pytest.raises(SchemaError):
        clopper_pearson(k, n, **kw)  # type: ignore[arg-type]


def test_importance_sampled_bound_reduces_to_the_plain_one() -> None:
    events = np.zeros(5000, dtype=bool)
    events[:37] = True
    assert is_cp_upper(np.ones(5000), events) == pytest.approx(clopper_pearson(37, 5000), rel=1e-12)
    assert is_cp_upper(np.full(5000, 0.2), events) == pytest.approx(clopper_pearson(37, 5000), rel=1e-12)


def test_importance_sampled_bound_uses_the_kish_effective_n() -> None:
    gen = np.random.Generator(np.random.Philox(11))
    w = gen.lognormal(0.0, 1.0, 20_000)
    events = gen.uniform(size=20_000) < 0.004
    n_eff = w.sum() ** 2 / (w ** 2).sum()
    p_hat = w[events].sum() / w.sum()
    expected = stats.beta.ppf(0.95, p_hat * n_eff + 1, n_eff - p_hat * n_eff)
    assert is_cp_upper(w, events) == pytest.approx(expected, rel=1e-9)
    assert is_cp_upper(w, events) > clopper_pearson(int(events.sum()), 20_000) * 0.5
    assert is_cp_upper(w, np.ones(20_000, dtype=bool)) == 1.0


def test_importance_sampled_validation() -> None:
    with pytest.raises(SchemaError):
        is_cp_upper(np.ones(3), np.array([0, 1, 0]))          # events must be boolean
    with pytest.raises(SchemaError):
        is_cp_upper(np.ones(3), np.zeros(4, dtype=bool))
    with pytest.raises(SchemaError):
        is_cp_upper(np.array([1.0, -1.0]), np.zeros(2, dtype=bool))
