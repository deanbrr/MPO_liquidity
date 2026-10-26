"""The Return Preference Engine on a synthetic book (no data needed): each basis does what it says."""
import numpy as np
import pandas as pd
import pytest

from tpp import returns
from tpp.buckets import CATALOG


@pytest.fixture(scope="module")
def er_synth():
    rows = []
    for k, b in enumerate(CATALOG):
        base = 0.04 + 0.003 * k
        rows.append({"department": b.department, "vertical": b.vertical, "vehicle": b.vehicle, "key": b.er_key,
                     "Downside": base - 0.03, "Base": base, "Upside": base + 0.03, "flags": ""})
    return pd.DataFrame(rows)


@pytest.fixture(scope="module")
def book_synth():
    rng = np.random.default_rng(0)
    rows = []
    for i in range(240):
        b = ["PE_US_F", "PE_VC_F", "CS_CR_F", "RE_F"][i % 4]
        age = float(rng.uniform(1, 12))
        uw = float(rng.uniform(0.12, 0.25))
        act = uw - float(rng.normal(0.05, 0.06))
        rows.append({"FUND_CODE": f"F{i}", "bucket": b, "department": {"PE": "Private Equity", "CS": "Capital Solutions", "RE": "Real Estate"}[b[:2]],
                     "nav_bn": float(rng.uniform(0.05, 0.5)), "age": age, "vintage": 2026 - round(age),
                     "uw_irr": uw, "act_irr": act, "ACTUAL_DPI": min(age / 10, 1.2)})
    return pd.DataFrame(rows)


def test_strategy_basis_is_the_er_return(P, er_synth, book_synth):
    R = returns.holding_returns(book_synth, er_synth, P, {"basis": "strategy"})
    h = R["holdings"]
    assert np.allclose(h["r_base"], h["S_base"]) and np.allclose(h["r_down"], h["S_down"]) and np.allclose(h["r_up"], h["S_up"])


def test_measured_underwriting_bias_is_positive_when_underwriting_was_optimistic(P, er_synth, book_synth):
    bias = returns.underwriting_bias(book_synth, P)
    for b in ("PE_US_F", "PE_VC_F", "CS_CR_F", "RE_F"):
        assert 0.0 < bias.loc[b, "beta"] < 0.15


def test_blend_tilts_are_capped_and_scenario_spread_is_kept(P, er_synth, book_synth):
    R = returns.holding_returns(book_synth, er_synth, P, {"basis": "blend", "weights": {"underwritten": 1.0, "actual": 1.0}})
    h = R["holdings"]
    cap = float(P.get("returns.tilt_cap_pp")) / 100
    assert (h["r_base"] - h["S_base"]).abs().max() <= 2 * cap + 1e-12
    assert np.allclose(h["r_up"] - h["r_base"], h["S_up"] - h["S_base"])


def test_risk_aversion_lowers_the_certainty_equivalent_toward_the_downside(P, er_synth, book_synth):
    lo = returns.holding_returns(book_synth, er_synth, P, {"risk_aversion": 1.0})["holdings"]["r_ce"]
    hi = returns.holding_returns(book_synth, er_synth, P, {"risk_aversion": 8.0})["holdings"]["r_ce"]
    h = returns.holding_returns(book_synth, er_synth, P, {"risk_aversion": 8.0})["holdings"]
    assert (hi <= lo + 1e-12).all() and (hi >= h["r_down"] - 1e-12).all()


def test_scenario_probabilities_reweight_the_expected_return(P, er_synth, book_synth):
    a = returns.holding_returns(book_synth, er_synth, P, {"scenario_probs": {"Downside": 1, "Base": 0, "Upside": 0}})["holdings"]
    assert np.allclose(a["r_exp"], a["r_down"])


def test_ce_closed_forms():
    R = np.array([[0.0, 0.10, 0.20]])
    pi = np.array([0.25, 0.5, 0.25])
    assert abs(returns.ce(R, pi, 0.0, 5)[0] - ((pi @ (1 + R[0]) ** 5) ** 0.2 - 1)) < 1e-12
    assert abs(returns.ce(R, pi, 1.0, 5)[0] - (np.exp(pi @ np.log(1 + R[0])) - 1)) < 1e-12
