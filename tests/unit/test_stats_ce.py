"""Certainty-equivalent conversions (BUILD_SPEC v1.1 §1.2, §4.4, §5.11). Owner WP-02.

``j_to_ce_wealth`` inverts the objective to 1e-10 (the spec's acceptance), on both sides of the target and for
several risk aversions; the bp conversions follow their formulas; 1bp a year ≈ $17.7m a year at W₀ = $177bn.
SYNTHETIC values only.
"""

from __future__ import annotations

import datetime as dt
import math

import numpy as np
import pytest

from adic_tpa.contracts.contract import ObjectiveSpec
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.stats import delta_ce_bp, h_delta_ce_bp, j_to_ce_wealth, sure_objective, usd_m_per_bp_year

TARGET = 1.10 ** 10                                     # W̃*/W0 for 10% a year over 10 years
WEALTH = [0.05, 0.3, 0.8, 1.0, 1.7, 2.5, TARGET, 2.6, 3.5, 10.0]


def _objective_spec(**kw: object) -> ObjectiveSpec:
    return ObjectiveSpec(target_anchor_date=dt.date(2026, 9, 30), target_anchor_wealth_bn=177.0,
                         model_weights={"M1": 0.5, "M6": 0.5}, **kw)  # type: ignore[arg-type]


@pytest.mark.parametrize("gamma", [0.5, 1.0, 2.0, 3.0, 6.0])
@pytest.mark.parametrize("lam", [0.0, 1.0, 2.0])
def test_inverts_the_objective_to_1e_10(gamma: float, lam: float) -> None:
    for w in WEALTH:
        j = sure_objective(w, gamma, lam, 2.0, TARGET)
        assert abs(j_to_ce_wealth(j, gamma, lam, 2.0, TARGET) - w) <= 1e-10 * max(1.0, w), (gamma, lam, w)


def test_sure_objective_is_the_spec_formula() -> None:
    w = 1.5
    assert sure_objective(w, 3.0, 1.0, 2.0, TARGET) == pytest.approx(w ** -2 / -2 - (1 - w / TARGET), rel=1e-14)
    assert sure_objective(3.0, 3.0, 1.0, 2.0, TARGET) == pytest.approx(3.0 ** -2 / -2, rel=1e-14)
    # the shortfall exponent cancels for a sure outcome (the p-norm of a constant)
    assert sure_objective(w, 3.0, 1.0, 1.5, TARGET) == pytest.approx(sure_objective(w, 3.0, 1.0, 3.0, TARGET))


def test_ce_wealth_is_increasing_in_j() -> None:
    js = np.linspace(-5.0, -0.06, 50)
    ws = [j_to_ce_wealth(float(j), 3.0, 1.0, 2.0, TARGET) for j in js]
    assert (np.diff(ws) > 0).all()


def test_unreachable_objectives_raise() -> None:
    with pytest.raises(SchemaError):
        j_to_ce_wealth(0.0, 3.0, 1.0, 2.0, TARGET)              # CRRA(3) utility is negative
    with pytest.raises(SchemaError):
        j_to_ce_wealth(-1.5, 0.5, 1.0, 2.0, TARGET)             # below −λ at γ < 1
    with pytest.raises(SchemaError):
        j_to_ce_wealth(-0.5, 3.0, 1.0, 1.0, TARGET)             # shortfall exponent must exceed 1 (S-ADR-06)
    with pytest.raises(SchemaError):
        j_to_ce_wealth(math.nan, 3.0, 1.0, 2.0, TARGET)
    with pytest.raises(SchemaError):
        j_to_ce_wealth(-800.0, 1.0, 1.0, 2.0, TARGET)            # exp(-800) underflows: no representable wealth


@pytest.mark.parametrize("args", [(1.0, 0.0, 1.0, 2.0, TARGET), (1.0, 3.0, -1.0, 2.0, TARGET),
                                  (1.0, 3.0, 1.0, 2.0, 0.0), (0.0, 3.0, 1.0, 2.0, TARGET)])
def test_sure_objective_validation(args: tuple[float, ...]) -> None:
    with pytest.raises(SchemaError):
        sure_objective(*args)


def test_delta_ce_bp_needs_positive_years() -> None:
    with pytest.raises(SchemaError):
        delta_ce_bp(-0.2, -0.3, _objective_spec(), years=0)


def test_delta_ce_bp_is_the_annualized_ce_return_difference() -> None:
    obj = _objective_spec()
    target = (1 + obj.target_annual) ** obj.horizon_years
    for w0, w1 in ((1.8, 1.9), (2.7, 2.9), (0.9, 0.95)):
        j0 = sure_objective(w0, obj.gamma, obj.lambda_T, obj.shortfall_exponent, target)
        j1 = sure_objective(w1, obj.gamma, obj.lambda_T, obj.shortfall_exponent, target)
        assert delta_ce_bp(j1, j0, obj) == pytest.approx(1e4 * (w1 ** 0.1 - w0 ** 0.1), rel=1e-9)
        assert delta_ce_bp(j0, j1, obj) == pytest.approx(-delta_ce_bp(j1, j0, obj), rel=1e-12)
    assert delta_ce_bp(-0.2, -0.2, obj) == 0.0
    j0 = sure_objective(2.0, 3.0, 1.0, 2.0, target)
    j1 = sure_objective(2.0 * 1.01 ** 5, 3.0, 1.0, 2.0, target)
    assert delta_ce_bp(j1, j0, obj, years=5) == pytest.approx(1e4 * (2.0 ** 0.2) * 0.01, rel=1e-9)


def test_h_delta_ce_bp_formula() -> None:
    assert h_delta_ce_bp(0.003, 0.5) == pytest.approx(1e4 * 0.003 / (0.5 * 3.0))
    assert h_delta_ce_bp(-0.003, 0.5, years=2.0) == pytest.approx(-30.0)
    with pytest.raises(SchemaError):
        h_delta_ce_bp(0.003, 0.0)
    with pytest.raises(SchemaError):
        h_delta_ce_bp(0.003, 1.0, years=0.0)


def test_usd_per_bp_year() -> None:
    assert usd_m_per_bp_year(177.0) == pytest.approx(17.7, rel=1e-12)
    assert usd_m_per_bp_year(100.0) == pytest.approx(10.0, rel=1e-12)
    with pytest.raises(SchemaError):
        usd_m_per_bp_year(0.0)
