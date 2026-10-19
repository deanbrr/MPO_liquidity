"""
Regression test (gap_02 item 5): no decision card may be driven by penalty-pinned duals.
SYNTHETIC - NOT ADIC DATA. Run: <venv>/python.exe -m pytest -q test_no_pinned_duals.py

The production version runs on H's full dual set; this fixture uses the linearised t0 liquidity block in
phase1_demo.py, whose T4 coefficients come from the deterministic ladder on the synthetic book.
"""
import math

import pytest

import phase1_demo as P
from gap02_study import s_star, t4_literal

READINGS = {
    "critic": t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0)),
    "as_written": t4_literal(floor=0.08),
    "canonical": s_star(0.76),
}


@pytest.fixture(scope="module")
def coefs():
    return {k: P.t4_coefficients(s) for k, s in READINGS.items()}


def test_infeasible_reading_pins_the_dual_and_is_caught(coefs):
    """An infeasible hard row priced elastically pins its dual at the penalty; the guard must fire."""
    sol = P.solve(coefs["critic"], mode_h=False, elastic=True)
    assert sol["u_S"] > 0.0
    assert math.isclose(sol["duals"]["T4"], P.M_TIERS["S"], rel_tol=1e-6)
    scaled = P.solve(coefs["critic"], mode_h=False, elastic=True, penalty_scale=10.0)
    assert math.isclose(scaled["duals"]["T4"], 10 * P.M_TIERS["S"], rel_tol=1e-6)   # scales with M: pinned
    with pytest.raises(AssertionError):
        P.assert_no_penalty_pinned_duals(sol)
    # the pathology the guard prevents: every test fund is a SELL at a reservation price near zero
    assert all(c["action"] == "SELL" for c in sol["cards"])
    assert max(c["reservation_price"] for c in sol["cards"]) < 0.02


@pytest.mark.parametrize("reading", ["critic", "as_written", "canonical"])
@pytest.mark.parametrize("mode_h", [False, True])
def test_restored_problem_prices_are_finite_and_penalty_invariant(coefs, reading, mode_h):
    r = P.restore_and_solve(coefs[reading], mode_h=mode_h)
    hard, e1, e10 = r["restored"], r["restored_elastic_x1"], r["restored_elastic_x10"]
    P.assert_no_penalty_pinned_duals(e1)
    P.assert_no_penalty_pinned_duals(e10)
    for row in ("T4", "IG"):
        assert math.isclose(e1["duals"][row], e10["duals"][row], rel_tol=1e-6, abs_tol=1e-9)
        assert math.isclose(hard["duals"][row], e1["duals"][row], rel_tol=1e-6, abs_tol=1e-9)
    # decision cards identical whatever the penalty scale
    assert [c["action"] for c in e1["cards"]] == [c["action"] for c in e10["cards"]]
    # no card says "sell at almost any bid": reservation prices stay above a crisis-bid floor
    assert min(c["reservation_price"] for c in hard["cards"]) > 0.60
    # the policy cushion is measured against the glide path and is non-negative after restoration
    assert r["cushion_on_glide_path"] >= -1e-9


def test_phase1_minimal_violation_matches_closed_form(coefs):
    """With every reversible lever at capacity (no PE sales in Phase I), u* is the residual gap."""
    c = coefs["critic"]
    p1 = P.phase1(c, mode_h=False)
    max_relief = sum(c["slope"][k] * (P.CAP[k] if k != "band" else 0.0) for k in P.CAP if c["slope"][k] > 0)
    assert math.isclose(p1["u_S_star"], max(0.0, -(c["h0"] + max_relief)), rel_tol=1e-6, abs_tol=1e-6)
    assert "T4 row" in p1["iis"]
