"""The benchmark ladder: the static framework (one policy portfolio, Yale pacing) and the yearly re-plan. A re-planned
decision depends only on the history observed when it is taken; the static policy respects the limits a one-period
model can express; and a scenario subset is the same scenarios, renormalized."""
from pathlib import Path

import numpy as np
import pytest

DATA = Path(__file__).resolve().parents[1] / "data"
needs_data = pytest.mark.skipif(not ((DATA / "fund_returns.xlsx").exists() and (DATA / "er_strategy_returns.xlsx").exists()),
                                reason="the user's workbooks are not in demo/data")


def test_history_tables_follow_the_whole_history():
    from tpp import plan as planmod
    cls = np.array([[1, 0, 0, 0, 0, 0], [1, 0, 0, 2, 1, 0], [1, 2, 1, 0, 2, 0], [1, 0, 0, 2, 2, 0]])
    assert planmod.history_code(cls, 2).tolist() == [0, 0, 7, 0]
    assert planmod.history_code(cls, 3).tolist() == [0, 2, 21, 2]
    tab = [list(range(3)), list(range(9)), [10.0 * h for h in range(27)], [100.0 * h for h in range(81)]]
    p = planmod.Plan(name="t", commit={"PE_US_F": [1.0, 0, 0, 0, 0]}, contingent={"commit": {"PE_US_F": tab}})
    _, amt, _ = planmod.schedule_paths(p, [], ["PE_US_F"], cls)
    assert amt[1, :, 0].tolist() == cls[:, 1].tolist()                     # year 2: the year-1 state
    assert amt[3, :, 0].tolist() == [0.0, 20.0, 210.0, 20.0]                # year 4: the history of three year ends
    assert amt[4, 1, 0] != amt[4, 3, 0]                                     # same history to year 3, not to year 4
    assert amt[4, :, 0].tolist() == [100.0 * h for h in planmod.history_code(cls, 4)]


@needs_data
def test_subset_is_the_same_scenarios(platform):
    v = platform.view("strategy")
    house = platform.house()
    bkey, B, _ = platform.book_for(v["prefs"], house)
    S = platform.paths_for(bkey, B, "lp", "base", platform._pi(v["prefs"]), house)
    idx = np.flatnonzero(S.cls_y[:, 1] == 0)
    sub = S.subset(idx)
    assert sub.m == len(idx) and np.array_equal(sub.uV, S.uV[idx]) and np.array_equal(sub.tV, S.tV[:, idx])
    assert np.array_equal(sub.G["HF"], S.G["HF"][idx]) and np.array_equal(sub.cls_y, S.cls_y[idx])
    assert np.allclose(sub.accrual(), S.accrual()[idx])


@needs_data
def test_static_policy_respects_one_period_limits(platform):
    from tpp import sim
    from tpp.buckets import LIQUID_RISK
    sb = platform.static_benchmark("strategy", progress=lambda m: None)
    assert sb["ok"]
    pol, plan = sb["policy"], sb["plan"]
    w = pol["w"]
    v = platform.view("strategy")
    house = platform.house()
    bkey, B, _ = platform.book_for(v["prefs"], house)
    assert abs(sum(w.values()) - pol["debt_bn"] / B.W0 - 1.0) < 1e-6                 # weights on NAV, debt netted
    assert w["RESERVE"] >= float(house["floor_target"]) - 1e-9
    assert pol["private_w"] <= pol["priv_cap"] + 1e-9
    for i, b in enumerate(pol["ids"]):
        assert pol["lo"][i] - 1e-9 <= w[b] <= pol["hi"][i] + 1e-9, b
    mult = platform.house()["pace_mult"]
    for r in sb["pacing"]["rows"]:
        assert r["commit_bn"] <= mult[1] * r["pace_sq_bn"] + 0.3 + 1e-9, r["bucket"]
    assert all(len(set(c)) == 1 for c in plan.commit.values())             # level commitments: nothing dated
    assert not plan.contingent                                              # nothing depends on the path
    S = platform.paths_for(bkey, B, "oos", "base", platform._pi(v["prefs"]), house)
    o = sim.simulate(S, plan, platform.P, platform._sim_settings(house))
    # today's trades spend what there is: the reserve after today's trades is at least the target less trading costs
    assert o["r_reserve"][:, 0].min() >= float(house["floor_target"]) * B.W0 * 0.98
    assert sum(plan.liquid[b] for b in LIQUID_RISK) > 0


@needs_data
def test_replan_keeps_today_and_never_sees_the_future(platform):
    from tpp import plan as planmod
    fixed = platform.optimize("strategy", persist=False, house_override={"contingent": False}, progress=lambda m: None)
    rp, info = platform.replan("strategy", fixed, progress=lambda m: None, min_scenarios=20)
    base = planmod.Plan.from_dict(fixed["plan"])
    assert rp.liquid == base.liquid and rp.beta_bn == base.beta_bn and rp.navf_bn == base.navf_bn
    assert all(abs(rp.commit[b][0] - base.commit[b][0]) < 1e-12 for b in base.commit)
    assert info["n_replanned"] >= 1
    v = platform.view("strategy")
    house = platform.house()
    bkey, B, _ = platform.book_for(v["prefs"], house)
    S = platform.paths_for(bkey, B, "oos", "base", platform._pi(v["prefs"]), house)
    uid = [u.id for u in B.units]
    sell, amt, sched = planmod.schedule_paths(rp, uid, list(S.tpl_buckets), S.cls_y)
    for t in range(1, 5):
        code = planmod.history_code(S.cls_y, t)
        for h in np.unique(code):
            mk = code == h
            assert np.allclose(amt[t][mk], amt[t][mk][0]), (t, h)            # same history, same decision
            if t <= 2:
                assert np.allclose(sell[t][mk], sell[t][mk][0]) and np.allclose(sched[t][mk], sched[t][mk][0])
