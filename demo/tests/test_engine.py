"""Engine invariants on the user's book (skipped without the workbooks): data, calibration, the simulator's
ledger, the LP's limits and duals, determinism. Uses the platform's quick mode (fewer paths)."""
import base64
from pathlib import Path

import numpy as np
import pytest

DATA = Path(__file__).resolve().parents[1] / "data"
FUND, ER = DATA / "fund_returns.xlsx", DATA / "er_strategy_returns.xlsx"
pytestmark = pytest.mark.skipif(not (FUND.exists() and ER.exists()), reason="the user's workbooks are not in demo/data")


def test_er_grid_and_live_book(P, er):
    # structural checks only: no figure from the (MSIP-labelled) inputs is written into the repository
    from tpp import ingest
    from tpp.buckets import BY_KEY
    assert len(er) == 29 and set(er["key"]) == set(BY_KEY)
    assert er[["Downside", "Base", "Upside"]].notna().all().all()
    funds = ingest.load_funds(FUND)
    live, rep = ingest.live_book(funds, P)
    assert rep["as_of"] and 0 < rep["nav_live_bn"] <= funds["nav_bn"].clip(lower=0).sum() + 1e-9
    q = ingest.quality_report(funds, live, P)
    assert q["excluded"], "rows outside the live book are reported, never dropped silently"


def test_book_reconciles_to_total_nav(platform):
    _, B, _ = platform.book_for(platform.view("strategy")["prefs"], platform.house())
    assert abs(B.total_nav - platform.house()["total_nav_bn"]) < 1e-9
    assert abs(B.private_nav + sum(B.liquid.values()) - B.total_nav) < 1e-6
    pe_pool = sum(u.exposure0 for u in B.units if u.pe_program and u.part == "tail")
    assert pe_pool >= platform.house()["pe_program_total_bn"]     # the program can be met from underperformers


def test_units_earn_their_target_returns(platform):
    from tpp import paths
    v = platform.view("strategy")
    bkey, B, _ = platform.book_for(v["prefs"], platform.house())
    S = paths.PathSet(B, platform.P, 400, 5, "base", [0.25, 0.5, 0.25])
    for k, u in enumerate(B.units[:12]):
        V, D, Cc = S.uV[:, :, k], S.uD[:, :, k], S.uC[:, :, k]
        ok = V[:, :-1].min(1) > 1e-6
        rq = np.log(np.maximum((V[:, 1:] + D - Cc) / np.maximum(V[:, :-1], 1e-12), 1e-9))
        for w in range(3):
            m = (S.world == w) & ok
            assert abs(rq[m].mean() * 4 - np.log1p(u.r_world[w])) < 0.004, (u.id, w)


def test_simulator_ledger_and_program(platform):
    from tpp import plan as planmod, sim
    v = platform.view("strategy")
    house = platform.house()
    bkey, B, _ = platform.book_for(v["prefs"], house)
    S = platform.paths_for(bkey, B, "oos", "base", platform._pi(v["prefs"]), house)
    sq = planmod.status_quo(B, platform.P, house)
    prog = planmod.program_summary(B, sq)
    assert abs(prog["pe_exposure_bn"] - house["pe_program_total_bn"]) < 1e-6
    o = sim.simulate(S, sq, platform.P, platform._sim_settings(house))
    assert np.all(np.isfinite(o["twr"])) and o["r_nav"][:, 0].min() == pytest.approx(B.W0)
    assert (o["r_reserve"][:, 1:] >= -1e-6).all()                  # the waterfall keeps the reserve non-negative
    # same paths, same plan: identical results (determinism)
    o2 = sim.simulate(S, sq, platform.P, platform._sim_settings(house))
    assert np.array_equal(o["twr"], o2["twr"])


def test_optimizer_respects_house_limits_and_duals_match_finite_differences(platform):
    from tpp import lp, plan as planmod, stakeholders as sh
    v = platform.view("asset_allocation")
    house = platform.house()
    bkey, B, _ = platform.book_for(v["prefs"], house)
    S = platform.paths_for(bkey, B, "lp", "base", platform._pi(v["prefs"]), house)
    st = sh.lp_settings(house, v["prefs"])
    M = lp.TPPModel(S, platform.P, st)
    ev = M.evaluate_plan(planmod.status_quo(B, platform.P, house))
    assert ev is not None and ev["in_sample"]["p_forced"] < 0.01   # no look-ahead forced sales for the status quo
    res = lp.solve(M, "utility")
    x = res["x"]
    plan = M.extract(x, "t")
    assert abs(planmod.program_summary(B, plan)["pe_exposure_bn"] - house["pe_program_total_bn"]) < 1e-5
    assert plan.term_bn + plan.navf_bn + plan.beta_bn <= (house["lev_cap"] - 1) * float(x[M.NAV0]) + 1e-6
    du = M.duals(x, res["y"], res["rc"])
    # finite-difference check of the decision threshold p* on unsold units that may be sold today
    cand = [i for i, u in enumerate(B.units) if u.nav0 > 0.5 and M.ub[int(M.Sx[i, 0])] > 0.01
            and x[int(M.Sx[i, 0])] < 1e-9]
    if not cand:
        pytest.skip("the plan sells part of every sizeable unit today: no column at its bound to perturb")
    obj0 = float(M.cost @ x)
    h = M.highs()
    for k in cand[:3]:
        col = int(M.Sx[k, 0])
        h.changeColBounds(col, 0.002, 0.002)
        x2, *_ = M.run("fd")
        h.changeColBounds(col, M.lb[col], M.ub[col])
        assert x2 is not None
        p_fd = du["units"][k]["bid0"] + (float(M.cost @ x2) - obj0) / (du["lambda0"] * 0.002 * M.nav0[k])
        assert abs(p_fd - du["units"][k]["p_star"]) < 0.01, (B.units[k].id, p_fd, du["units"][k]["p_star"])


def test_twr_encoding_round_trip():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("build_demo", Path(__file__).resolve().parents[1] / "build_demo.py")
    bd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bd)
    t = np.array([-0.2, 0.0, 0.09996, 0.1, 0.10004, 0.12345, 0.5])
    raw = base64.b64decode(bd.enc_twr({"twr": t}))
    back = np.frombuffer(raw, dtype="<i2") / 1e4
    assert np.allclose(back, np.floor(t * 1e4 + 1e-9) / 1e4)
    for h in (0.085, 0.095, 0.1, 0.105):                         # the page's hurdle test agrees with the engine's
        assert np.array_equal(back >= h - 1e-9, t >= h)
