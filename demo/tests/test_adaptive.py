"""The adaptive plan and the owner's distribution: later decisions never see the future (two paths in the same
situation get the same decision), the PE-cycle effects are centred so only timing earns them, and the owner takes
about what the fund earns, so the status quo's fund keeps roughly its size."""
from pathlib import Path

import numpy as np
import pytest

DATA = Path(__file__).resolve().parents[1] / "data"
needs_data = pytest.mark.skipif(not ((DATA / "fund_returns.xlsx").exists() and (DATA / "er_strategy_returns.xlsx").exists()),
                                reason="the user's workbooks are not in demo/data")


def test_pe_cycle_effects_are_centred(P):
    mix = np.asarray(P.get("pe_cycle.class_mix"), float)
    assert abs(mix.sum() - 1.0) < 1e-9
    assert abs(mix @ np.asarray(P.get("pe_cycle.vintage_alpha"), float)) < 5e-4      # the average vintage is unchanged
    for fam, g in P.get("pe_cycle.secondary_entry").items():
        g = np.asarray(g, float)
        assert abs(mix @ g - 1.0) < 5e-3, fam                                         # the average purchase is unchanged
        assert g[0] < g[1] < g[2], fam                                                # cheaper the worse the market


def test_owner_rule_band(P):
    lo, hi = float(P.get("owner_distribution.rule_floor")), float(P.get("owner_distribution.rule_cap"))
    assert 0.0 < lo <= float(P.get("owner_distribution.rule_prior")) <= hi


@needs_data
def test_owner_takes_about_what_the_fund_earns(platform):
    from tpp import paths, plan as planmod, sim
    v = platform.view("strategy")
    house = platform.house()
    bkey, B, _ = platform.book_for(v["prefs"], house)
    S = platform.paths_for(bkey, B, "oos", "base", platform._pi(v["prefs"]), house)
    lo, hi = float(platform.P.get("owner_distribution.rule_floor")), float(platform.P.get("owner_distribution.rule_cap"))
    assert S.draw.min() >= lo - 1e-9 and S.draw.max() <= hi + 1e-9
    o = sim.simulate(S, planmod.status_quo(B, platform.P), platform.P, platform._sim_settings(house))
    w = S.prob / S.prob.sum()
    nav5 = o["r_nav"][:, 5]
    med = nav5[np.argsort(nav5)][np.searchsorted(np.cumsum(w[np.argsort(nav5)]), 0.5)]
    assert abs(med / B.W0 - 1.0) < 0.10                    # the fund keeps roughly its size after paying the owner
    assert isinstance(paths.STRESSES, dict)


@needs_data
def test_adaptive_rules_never_see_the_future(platform):
    from tpp import plan as planmod, sim
    op = platform.optimize("strategy", persist=False, progress=lambda m: None)
    p = planmod.Plan.from_dict(op["plan"])
    assert p.contingent and "beta" not in p.contingent    # the overlay has no state rule unless asked for
    assert "bs_guard" in op["eps"]                        # the balance-sheet guard binds every optimized plan
    last = op["calibration"][-1]
    assert last["bs_within"] is not None and last["bs_within"] >= 0.85    # quick mode: few paths, loose bound
    v = platform.view("strategy")
    house = platform.house()
    bkey, B, _ = platform.book_for(v["prefs"], house)
    S = platform.paths_for(bkey, B, "oos", "base", platform._pi(v["prefs"]), house)
    uid = [u.id for u in B.units]
    sell, amt, sched = planmod.schedule_paths(p, uid, list(S.tpl_buckets), S.cls_y)
    cls = S.cls_y
    for tau in range(1, 5):                              # commitments: same class when made -> same commitment
        for c in range(3):
            mk = cls[:, tau] == c
            if mk.sum() > 1:
                assert np.ptp(amt[tau][mk], axis=0).max() < 1e-9
    hist = cls[:, 1] * 3 + cls[:, 2]                     # year-3 sales and debt: same (year-1, year-2) classes
    for h in np.unique(hist):
        mk = hist == h
        if mk.sum() > 1:
            assert np.ptp(sell[2][mk], axis=0).max() < 1e-9 and np.ptp(sched[2][mk]) < 1e-9
    assert np.allclose(sell[0], sell[0][0]) and np.allclose(amt[0], amt[0][0])     # today's: one decision for all
    o = sim.simulate(S, p, platform.P, platform._sim_settings(house))
    assert np.isfinite(o["twr"]).all()
    fixed = platform.optimize("strategy", persist=False, house_override={"contingent": False}, progress=lambda m: None)
    assert planmod.Plan.from_dict(fixed["plan"]).contingent is None
