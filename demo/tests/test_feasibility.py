"""The research-driven changes (2026-10-28): the reconciled opening balance sheet (private share of NAV, private NAV
outside the fund file derived from the current strategies, the reserve at its target), the target account and the
dollar shortfall, the two exit models, and the shortfall objective. Structural checks only: no figure from the
(MSIP-labelled) inputs is written here. Skipped without the workbooks."""
from pathlib import Path

import numpy as np
import pytest

DATA = Path(__file__).resolve().parents[1] / "data"
FUND, ER = DATA / "fund_returns.xlsx", DATA / "er_strategy_returns.xlsx"
pytestmark = pytest.mark.skipif(not (FUND.exists() and ER.exists()), reason="the user's workbooks are not in demo/data")


def _book(platform):
    v = platform.view("strategy")
    house = platform.house()
    bkey, B, _ = platform.book_for(v["prefs"], house)
    return v, house, bkey, B


def test_private_share_reconciles_from_the_current_strategies(platform):
    v, house, _, B = _book(platform)
    share = float(house["private_share"])
    file_priv = sum(u.nav0 for u in B.units if u.part != "ext")
    ext = [u for u in B.units if u.part == "ext"]
    if share * B.total_nav <= file_priv:
        assert not ext
        return
    assert B.private_nav == pytest.approx(share * B.total_nav, rel=1e-9)
    assert B.private_nav + sum(B.liquid.values()) == pytest.approx(B.total_nav, rel=1e-9)
    k = B.outside_nav / file_priv
    for u in ext:                                   # each bucket scaled by the same factor, unfunded included
        file_units = [x for x in B.units if x.bucket == u.bucket and x.part != "ext"]
        assert u.nav0 == pytest.approx(k * sum(x.nav0 for x in file_units), rel=1e-6)
        assert u.unf0 == pytest.approx(k * sum(x.unf0 for x in file_units), rel=1e-6)
        assert not u.pe_program and not u.codes
    assert B.pace_scale == pytest.approx(1.0 + k)
    res = B.liquid["CASH"] + B.liquid["TREASURY"]
    assert res >= float(platform.P.get("liquidity.floor_target")) * B.W0 - 1e-6   # the reserve starts at its target
    # a variant without the Liquidity group's limits starts from the same balance sheet
    from tpp import stakeholders as sh
    _, B2, _ = platform.book_for(v["prefs"], {**house, **sh.target_only(1.0)})
    assert B2.liquid == B.liquid and B2.private_nav == pytest.approx(B.private_nav)


def test_plans_never_sell_the_derived_private_assets(platform):
    from tpp import lp, stakeholders as sh
    v, house, bkey, B = _book(platform)
    S = platform.paths_for(bkey, B, "lp", "base", platform._pi(v["prefs"]), house)
    M = lp.TPPModel(S, platform.P, sh.lp_settings(house, v["prefs"]))
    for k, u in enumerate(B.units):
        if u.part == "ext":
            assert M.ub[int(M.Sx[k, 0])] == 0.0


def test_target_account_identity(platform):
    from tpp import plan as planmod, sim
    v, house, bkey, B = _book(platform)
    S = platform.paths_for(bkey, B, "oos", "base", platform._pi(v["prefs"]), house)
    o = sim.simulate(S, planmod.status_quo(B, platform.P, house), platform.P, platform._sim_settings(house))
    g = float(house["goal_rate"])
    # each year's draw is paid in four equal quarterly instalments, each growing at g to the end of year 5
    acc = np.array([np.mean([(1 + g) ** (5 - t - k / 4) for k in range(1, 5)]) for t in range(5)])
    B5 = B.W0 * (1 + g) ** 5 - o["y_draw"] @ acc
    assert np.allclose(o["r_target"][:, 5], B5, rtol=1e-9, atol=1e-6)
    assert np.allclose(o["short"], np.maximum(B5 - o["r_nav"][:, 5], 0.0), atol=1e-6)


def test_exit_models_split_and_mean_matched(P):
    from tpp import paths
    n = 200
    n_p = paths.exit_split(P, "base", n)
    assert n_p == int(np.floor(float(P.get("exits.persistent_share")) * n + 0.5))
    assert paths.exit_split(P, "prolonged_drought", n) == n
    assert paths.persistent_variant("base") == "prolonged_drought"
    assert paths.persistent_variant("crisis_y1") == "prolonged_drought+crisis_y1"
    F = paths.factors(P, "base", n, 5)
    assert F.persistent.sum() == n_p and not F.persistent[: n - n_p].any()
    # each block's mean factor return equals its own model's population mean
    cyc = F.f[: n - n_p].mean(axis=(0, 1)) * 4
    per = F.f[n - n_p:].mean(axis=(0, 1)) * 4
    assert np.allclose(cyc, paths.pop_factor_mean(P, "base"), atol=1e-9)
    assert np.allclose(per, paths.pop_factor_mean(P, "prolonged_drought"), atol=1e-9)
    # the slowdown keeps exits in drought longer
    drought = lambda E: (np.asarray(E)[:, 1:] == 2).mean()
    assert drought(F.E[n - n_p:]) > drought(F.E[: n - n_p])


def test_shortfall_objective_and_robust_views(platform):
    from tpp import lp, plan as planmod, stakeholders as sh
    v, house, bkey, B = _book(platform)
    S = platform.paths_for(bkey, B, "lp", "base", platform._pi(v["prefs"]), house)
    st = {**sh.lp_settings(house, v["prefs"]), "shortfall": True, "robust_pis": platform.robust_pis()}
    M = lp.TPPModel(S, platform.P, st)
    assert M.K_sf == len(platform.robust_pis()) >= 1
    assert M.evaluate_plan(planmod.status_quo(B, platform.P, house)) is not None
    res = lp.solve(M, "shortfall")
    x = res["x"]
    assert x is not None and res["label"] == "SHORTFALL"
    ins = M.in_sample(x)
    sh_ = np.maximum(M.Wstar - x[M.WB], 0.0)
    assert np.all(x[M.SH] >= sh_ / M.W0 - 1e-6)                 # S is at least the shortfall on every scenario
    # TT bounds every view's E[S] + CVaR(S) (in W0 units), within the tie-break tolerance of its optimum
    worst = max(ins["short_views"]) / M.W0
    assert worst <= float(x[int(M.TT)]) + 1e-5
    assert float(x[int(M.TT)]) <= res["phi"] * (1 + float(platform.P.get("objective.shortfall_tiebreak_rel"))) + 1e-5
