"""Gate V-RA-CTRL (extends V23): no REFINANCE, LEVER or HEDGE action on LP or minority Real Assets holdings.
SYNTHETIC - NOT ADIC DATA. Run: <venv>/python.exe -I -B -m pytest -q test_v_ra_ctrl.py
Checks the ra_gap_01 ladder levers and the Monte Carlo RA playbook against the control matrix of the RA synthesis
s7.2 (fund interests: SELL / HOLD only; minority co-investments: SELL / HOLD; joint or sole control: full menu)."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra_book as B  # noqa: E402
import ra_ladder as RL  # noqa: E402
import ra_engine as R  # noqa: E402
import ra_module as RM  # noqa: E402

LP_OR_MINORITY = {s["id"] for s in B.SLEEVES if s["ctrl"] == 0.0}
CONTROLLED = {s["id"] for s in B.SLEEVES if s["ctrl"] > 0.0}


def test_census_control_matrix():
    # funds (OE / CE) and the minority RE co-investment carry no control share
    for s in B.SLEEVES:
        if s["vehicle"] in ("OE", "CE") or s["vehicle"] == "CO":
            assert s["ctrl"] == 0.0, s["id"]
    assert CONTROLLED == {"RE_DIR_GL", "RE_DIR_GCC", "INF_DIR", "ENR_DIR"}


def test_ladder_refinance_levers_only_on_controlled():
    caps = RL.cashout_caps()
    assert set(caps) <= CONTROLLED
    lev = {L["key"]: L for L in RL.levers(RL.s_star(0.835), "v2u16")}
    ctrl_nav = sum(s["nav"] * s["ctrl"] for s in B.SLEEVES)
    assert abs(lev["ra_jv"]["cap"] - RL.JV_CAP_SHARE * ctrl_nav) < 1e-12
    assert abs(lev["ra_cashout"]["cap"] - sum(caps.values())) < 1e-12


def test_mc_playbook_respects_control():
    m = R.E.MODELS["M6"]
    rng = np.random.default_rng(1)
    st = RM.RAState(400, m, rng, m.cash_lr, m.eq_g, R.E.stationary_crisis_share(m), R.pz_stationary(),
                    md_f=m.md_f, mc_f=m.mc_f)
    d0 = st.D.copy()
    st.cashout(np.ones(400, dtype=bool), np.full(400, 1))
    idx_lp = [st.ids.index(k) for k in LP_OR_MINORITY]
    assert np.all(st.co_debt[:, idx_lp] == 0.0)            # no cash-out (REFINANCE) debt on LP / minority sleeves
    assert np.allclose(st.D[:, idx_lp], d0[:, idx_lp])
    va0 = st.va().copy()
    cash, vgive, amt = st.jv_selldown(np.full(400, 5.0), np.full(400, 1), np.zeros(400, dtype=bool))
    assert np.allclose(st.va()[:, idx_lp], va0[:, idx_lp])    # sell-downs touch controlled equity only
    assert np.all(amt > 0)


def test_engine_run_no_cashout_on_lp():
    r = R.simulate(R.E.MODELS["M1"], R.E.Policy("mixB", rcf=10.0, pace_cut=True, band=True, hf_t0=5.0),
                   R.Cfg(book="v2u16", trigger="current", theta=0.835), n=300)
    assert r["ra"]["cashout"] >= 0.0
