"""
Extension of gap_02's test_no_pinned_duals.py to GROUP decision cards and GROUP envelopes / charges / hurdles.
SYNTHETIC - NOT ADIC DATA. Run from this folder:  <venv>/python.exe -m pytest -q test_no_pinned_duals_groups.py
(gap_02's original 8 tests are unchanged and still run from research/addenda/gap_02_calcs/.)

Fixture: g01_core's group-resolved linearisation of the H liquidity block - monthly T4' rows h = 1..24 (T + P + F
headroom under s*(0.76)), the t0 T2 row (IG + cash 8% target), 13 group-tagged levers and four group SELL cards.
"""
import math

import numpy as np
import pytest

import g01_core as G
from g01_core import s_star, t4_literal

READ = {"canonical": (s_star(0.76), "pricing"),
        "t4_literal": (t4_literal(), "reverse"),
        "critic": (t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0)), "reverse")}


@pytest.fixture(scope="module")
def coefs():
    return {k: G.coefficients_for(s, role) for k, (s, role) in READ.items()}


def test_group_cards_pinned_when_infeasible_row_is_elastic(coefs):
    """An infeasible row priced elastically pins mu at the tier; every group card fires; the guards refuse it."""
    c = coefs["critic"]
    as_pricing = dict(c, role="pricing")                      # isolate the pinned-dual guard from the role guard
    for st in ("R0", "R1"):
        sol = G.solve(c, st, elastic=True)
        assert sol["u_S"] > 0.0
        assert math.isclose(float(sol["mu"].sum()), G.M_TIERS["S"], rel_tol=1e-6)
        sol10 = G.solve(c, st, elastic=True, penalty_scale=10.0)
        assert math.isclose(float(sol10["mu"].sum()), 10 * G.M_TIERS["S"], rel_tol=1e-6)   # scales with M: pinned
        with pytest.raises(AssertionError):
            G.assert_no_penalty_pinned_duals(sol)
        assert all(card["action"] == "SELL" for card in sol["cards"])                       # PE, Sec, Co, HF
        assert max(card["reservation_price"] for card in sol["cards"]) < 0.02
        with pytest.raises(AssertionError):                                                  # no envelopes either
            G.group_prices(as_pricing, sol, "restored_problem", "x")


@pytest.mark.parametrize("reading", ["canonical", "t4_literal", "critic"])
@pytest.mark.parametrize("state", ["R0", "R1", "R2"])
def test_restored_group_prices_finite_and_penalty_invariant(coefs, reading, state):
    c = coefs[reading]
    r = G.restore_and_solve(c, state)
    hard, e1, e10 = r["restored"], r["restored_elastic_x1"], r["restored_elastic_x10"]
    G.assert_no_penalty_pinned_duals(e1)
    G.assert_no_penalty_pinned_duals(e10)
    assert np.allclose(e1["mu"], e10["mu"], atol=1e-9) and np.allclose(hard["mu"], e1["mu"], atol=1e-9)
    assert math.isclose(e1["y_IG"], e10["y_IG"], abs_tol=1e-9)
    assert [x["action"] for x in e1["cards"]] == [x["action"] for x in e10["cards"]]
    assert min(x["reservation_price"] for x in hard["cards"]) > 0.60      # no "sell at almost any bid"
    if c["role"] == "pricing":
        g1 = G.group_prices(c, e1, "restored_problem", "h")
        g10 = G.group_prices(c, e10, "restored_problem", "h")
        for g in G.PRIV:
            for k in ("envelope_12m", "envelope_24m", "pacing_bn_yr", "ftp_new_bp_yr", "hurdle_bp_yr",
                      "ftp_hold_bp_yr", "glide_share"):
                assert math.isclose(g1["groups"][g][k], g10["groups"][g][k], rel_tol=1e-6, abs_tol=1e-9)
    else:                                                                  # reverse stresses never price
        with pytest.raises(AssertionError):
            G.group_prices(c, hard, "restored_problem", "h")


@pytest.mark.parametrize("state", ["R0", "R1", "R2", "I"])
def test_kkt_cap_cheapest_spare_lever(coefs, state):
    """For every lever below its cap: sum_h mu_h slope_h + y_IG ig <= cost. The dual is capped by the cheapest spare
    lever per unit of headroom - not by buffer carry as such - and only once the row is restorable."""
    c = coefs["canonical"]
    relax = (max(0.0, -c["h0"].min()) * 0.75, 0.0) if state == "I" else (0.0, 0.0)
    h = G.solve(c, state, elastic=False, relax=relax)
    allow = G.STATES[state]["allow"]
    sleeve_full = h["x"]["sma_sell"] + h["x"]["sma_ro"] >= G.SMA_SLEEVE - 1e-6
    for k, v in c["lever"].items():
        cap = allow.get(k, v["cap"])
        if cap <= 0 or h["x"][k] >= cap - 1e-6 or (sleeve_full and k in ("sma_sell", "sma_ro")):
            continue
        assert float(h["mu"] @ v["slope"]) + h["y_IG"] * v["ig"] <= v["cost"] + 1e-7, k
    if state in ("R1", "R2"):                     # FTP flat at revolver carry while the revolver has spare capacity
        assert math.isclose(float(h["mu"].sum()), c["lever"]["rcf"]["cost"] / c["lever"]["rcf"]["slope"][23],
                            rel_tol=1e-6)


def test_phase1_group_closed_form(coefs):
    """With every reversible group lever at capacity (no sales of PE / Secondaries / Co-investment / HF lots in
    Phase I), u* is the residual gap; the IIS names the row and the levers at capacity by owning group."""
    c = coefs["critic"]
    assert np.all(c["lever"]["sma_sell"]["slope"] >= c["lever"]["sma_ro"]["slope"] - 1e-12)   # sale dominates
    for st in ("R0x", "R0", "R1", "R2"):
        p1 = G.phase1(c, st)
        allow = G.STATES[st]["allow"]
        head = c["h0"].copy()
        for k, v in c["lever"].items():
            if k == "sma_ro":
                continue
            head = head + np.maximum(v["slope"], 0.0) * allow.get(k, v["cap"])
        assert math.isclose(p1["u_S_star"], max(0.0, -float(head.min())), rel_tol=1e-6, abs_tol=1e-6)
        assert p1["iis"] and p1["iis"][0].startswith("T4' row")
        assert any("(PE)" in x for x in p1["iis"]) and any("(Private Credit)" in x for x in p1["iis"])


def test_canonical_restorable_without_band_or_fire_sales(coefs):
    """T4' = s*(0.76): Phase I over the task's group lever list alone returns u* = 0 (no structural RECOVERY)."""
    c = coefs["canonical"]
    for st in ("R0x", "R0", "R1", "R2"):
        assert G.phase1(c, st)["u_S_star"] == pytest.approx(0.0, abs=1e-7)


def test_envelope_accounting_and_glide_shares(coefs):
    c = coefs["canonical"]
    d0 = max(0.0, -float(c["h0"].min()))
    assert G.priced_on_flag(d0, 0.0) == "restored_problem"       # current book fails T4': price on the plan
    assert G.priced_on_flag(0.0, 0.0) == "original_problem"
    for st in ("R0", "R1"):
        h = G.restore_and_solve(c, st)["restored"]
        gp = G.group_prices(c, h, G.priced_on_flag(d0, 0.0), G.recovery_hash("s*", h), d0)
        assert gp["priced_on"] == "restored_problem" and gp["recovery_target_hash"]
        assert math.isclose(sum(v.get("glide_share", 0.0) for v in gp["groups"].values()), 1.0, rel_tol=1e-9)
        r = G.gl_ladder(c["stress"], G.plan_lev(c, h))
        used = sum(gp["groups"][g]["envelope_24m"] for g in G.PRIV) + gp["groups"]["ovl"]["envelope_24m"] \
            + float(r["cf"]["draw"][:24].sum() + r["cf"]["opex"][:24].sum() + r["cf"]["fee"][:24].sum())
        assert math.isclose(used, float(r["nco"][23]), rel_tol=1e-9)          # envelopes add up to NCO(24)
        assert float(r["head_tpf"][:24].min()) >= -1e-6                         # plan restores T4'
        if st == "R1":
            assert gp["groups"]["cf"]["glide_share"] > 0.9                      # revolver carries the deficit


def test_interim_glide_path_feasible_with_reversible_group_levers(coefs):
    c = coefs["canonical"]
    d0 = max(0.0, -float(c["h0"].min()))
    for t in range(5):
        g_t = d0 * max(0.0, 1 - t / 4)
        sol = G.solve(c, "I", elastic=False, relax=(g_t, 0.0))
        assert sol["status"] == "optimal"
        head = c["h0"] + sum(c["lever"][k]["slope"] * v for k, v in sol["x"].items())
        assert float(head.min()) >= -g_t - 1e-6
        assert all(v < 1e-9 for k, v in sol["sell"].items())                   # no sales on the interim path
