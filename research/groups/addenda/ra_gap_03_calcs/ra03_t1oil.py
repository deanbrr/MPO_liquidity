"""RA gap 03, step 3 engine: gap_02's Tier-1 Monte Carlo on the canonical generator, with oil-linked blocks.

SYNTHETIC - NOT ADIC DATA. Census, models M1-M6 and policies are gap_02's stylised proxies
(research/addenda/gap_02_calcs/t1_engine.py, imported unmodified for constants, models, policies and helpers).
`simulate_oil` is a copy of t1_engine.simulate with these changes only (each marked "RA03" in the code):

  1. Regimes. The macro crisis indicator and the shock type Z come from the canonical monthly generator
     (ra03_lib.Gen: least-squares monthly root of stream 03's prior, kappa coupling Z | S, Weibull Gulf-war dwell
     conditioned on 7.5 months elapsed, oil from the futures curve), sampled at quarter ends. The S chain is scaled
     per model to t1_engine's stationary crisis share, so t1's calm-drift calibration still applies (approximation).
  2. Owner draw. The annual rate comes from the canonical owner-draw engine on each path's own oil (linear fiscal
     map, frozen IMF fusion for 2027, d_2026 = 5.8%, smoothing, band, overrides), replacing t1's D_TGT[z].
  3. Oil blocks. Incremental oil-linked positions, specified in m bbl of front-month-equivalent delta at t0, carry
     a de-meaned oil P&L (zero expected excess return: a pure risk position) through the channel each block uses:
        PRIV  private fund-type exposure: value in private NAV; distributions scale with (F3/F3_mean)^eta;
        LEV   direct levered upstream (40% LTV RBL): value; distributions; equity cures when 0.6 x 0.85 x PV < debt
              (semi-annual redeterminations; cure = over-advance, owner policy varpi = 1);
        PUB   public energy equity: value in long-only DM equity, so it enters CBC_TP;
        PUT   overlay kink put spreads (rolling 1-year tranches, Black-76 premia on the model curve, cash payoff at
              expiry): negative delta, premium cash out;
        GCC   GCC real estate: a state exposure (G15 SG and GW multipliers on value and income), sized in $bn.
  4. Liquidity-state weights. Each path-quarter carries lambda_t mapped from t1's CFP stage (Green 0.0113 =
     revolver carry; Amber 0.05 = SMA run-off / sales; Red 0.243 = restored-problem dual on group levers; Black or a
     red-event quarter 0.54 = selling private NAV at 0.65) [I, anchored on groups synthesis s2.3 / s4.8 duals].
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra03_lib as L  # noqa: E402

_T1 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "addenda", "gap_02_calcs", "t1_engine.py"))
_spec = importlib.util.spec_from_file_location("t1_engine", _T1)
E = importlib.util.module_from_spec(_spec)
sys.modules["t1_engine"] = E
_spec.loader.exec_module(E)  # unmodified gap_02 engine

LAMBDA_STAGE = np.array([0.0113, 0.05, 0.243, 0.54])   # RA03 change 4 [I]
Z0 = np.array([0.03, 0.0, 0.0, 0.02, 0.10, 0.85])
_GEN_CACHE: dict = {}
_PZM = None


def _pzm():
    global _PZM
    if _PZM is None:
        _PZM = L.monthly_lsq(L.PZ_A)[0]
    return _PZM


def gen_paths(m: "E.Model", n: int, seed: int, k_gw: float = 1.3, imf: bool | str = True,
              pbe_median: float = 55.0) -> dict:
    """Canonical generator paths for model m, aggregated to t1's quarters, with annual draw rates."""
    key = (m.key, n, seed, k_gw, imf, pbe_median)
    if key in _GEN_CACHE:
        return _GEN_CACHE[key]
    PZm = _pzm()
    PS = L.s_chain_for_share(E.stationary_crisis_share(m))
    K, _ = L.calibrate_kappa(PS, PZm)
    g = L.Gen(PS, PZm, K, gw_mode="weibull", gw_k=k_gw)
    sim = g.simulate(n=n, T=63, seed=seed, S0=L.sLATE, Z0=Z0, x0=math.log(L.F1), chi0=math.log(L.SPOT / L.F1))
    dr = L.owner_draws(sim, 6, seed + 1, imf_fuse=imf, pbe_median=pbe_median)
    T = E.T_Q
    q_end = np.array([3 * (t + 1) for t in range(T)])
    crisis = (sim["S"][q_end] == L.sCRIS)
    z = sim["Z"][q_end].astype(int)
    x = sim["x"][q_end]
    x_prev = np.vstack([sim["x"][0][None, :], x[:-1]])
    P_q = np.stack([sim["P"][3 * t + 1:3 * t + 4].mean(axis=0) for t in range(T)])
    d = dr["d"]
    rates = [(5.8 + 3 * d[0]) / 4] + [(d[k - 1] + 3 * d[k]) / 4 for k in range(1, 5)]
    out = {"crisis": crisis, "z": z, "x": x, "x_prev": x_prev, "P_q": P_q, "rates": np.array(rates) / 100.0,
           "d_annual": d, "Z_month": sim["Z"], "S_month": sim["S"]}
    _GEN_CACHE[key] = out
    return out


def _f3_dev(x_t: np.ndarray, x_bar: float) -> np.ndarray:
    """log(F3 / mean F3) for a slow-factor deviation: average impulse over 36 months (~0.49)."""
    b3 = float(L.impulse_x(36)[1:37].mean())
    return b3 * (x_t - x_bar)


def simulate_oil(m: "E.Model", pol: "E.Policy", oil: dict | None = None, n: int = 10000, seed: int = 20261018,
                 hf_gate_pass: float = 0.83, gen: dict | None = None) -> dict:
    """t1_engine.simulate with the RA03 changes. oil = {block: size} with sizes in m bbl (PRIV, LEV, PUB, PUT;
    PUT negative = protection) and $bn for GCC; optional eps overrides 'eps_PRIV', 'eps_LEV', 'eps_PUB'."""
    oil = dict(oil or {})
    pi_c = E.stationary_crisis_share(m)
    mu_calm = E.calm_drift(m, pi_c)
    rng = np.random.default_rng(seed)                 # exogenous stream (returns, exits)
    rng_p = np.random.default_rng(seed + 7)           # sale-execution stream
    gp = gen if gen is not None else gen_paths(m, n, seed + 1000)   # RA03 change 1
    T_Q, NAV0 = E.T_Q, E.NAV0
    CASH_Q = E.CASH_Q

    eq_arith = math.log1p(m.eq_g) + 0.5 * 0.165 ** 2

    def alpha_for(g_target, beta):
        return (g_target + 0.5 * (beta * 0.165) ** 2) - (m.cash_lr + beta * (eq_arith - m.cash_lr))

    tgt = {"pe": m.pe_g, "sec": m.pe_g + 0.005, "co": m.pe_g, "cs": m.cs_g, "pc": m.pc_g}
    alpha = {g: alpha_for(tgt[g], E.BETA[g]) for g in E.PRIV0}
    alpha["pc"] += pi_c * 0.08
    alpha_hf = alpha_for(m.hf_g, 0.3) + pi_c * 0.08

    tre = np.full(n, E.TRE0)
    lo = {k: np.full(n, v) for k, v in E.LO0.items()}
    hf = np.full(n, E.HF0)
    hf_q = np.zeros((n, 10))
    priv = {k: np.full(n, v) for k, v in E.PRIV0.items()}
    econ_prev = {k: np.zeros(n) for k in E.PRIV0}
    rep = {k: np.full(n, v) for k, v in E.PRIV0.items()}
    unf = {k: np.full(n, v) for k, v in E.UNF0.items()}
    sec_def = np.full(n, E.SEC_DEF0)
    pc_rev = np.full(n, E.PC_REV0)
    n_syn = np.full(n, E.N_SYN0)
    b_r = np.zeros(n)
    b_n = np.zeros(n)
    crisis = np.zeros(n, dtype=bool)
    cdur = np.zeros(n, dtype=int)
    since_exit = np.full(n, 99)
    e = np.full(n, 2)
    basis = np.full(n, NAV0)
    im_prev = E.IM_N * n_syn

    red = np.zeros(n, dtype=bool)
    black_12m = np.zeros(n, dtype=bool)
    shortfall = np.zeros(n)
    withheld = np.zeros(n)
    paid_fv = np.zeros(n)
    red_sales = np.zeros(n)
    red_loss = np.zeros(n)
    amber_sales = np.zeros(n)
    amber_loss = np.zeros(n)
    floor4_breach = np.zeros(n, dtype=bool)
    stage_hist = np.zeros((T_Q, 4))
    lam = np.zeros((T_Q, n))                          # RA03 change 4
    draw_rate_q = np.zeros((T_Q, n))
    bh = dict(tre=np.full(n, E.TRE0), dm=np.full(n, E.LO0["dm"]), em=np.full(n, E.LO0["em"]),
              fi=np.full(n, E.LO0["fi"]), hf=np.full(n, E.HF0))
    hf_bh_q = np.tile(E.HF0 * E.HF_SCHED, (n, 1))
    hf_bh_cash = np.zeros(n)
    nco_bh = np.zeros(n)
    gstar = np.full(n, -np.inf)

    # ---------------- RA03 change 3: oil blocks (sizes at t0)
    F1 = L.F1
    eps = {"PRIV": oil.get("eps_PRIV", 0.38), "LEV": oil.get("eps_LEV", 0.835), "PUB": oil.get("eps_PUB", 0.24)}
    v_priv = np.full(n, oil.get("PRIV", 0.0) * F1 / eps["PRIV"] / 1000.0)      # $bn
    v_lev = np.full(n, oil.get("LEV", 0.0) * F1 / eps["LEV"] / 1000.0)
    v_pub0 = oil.get("PUB", 0.0) * F1 / eps["PUB"] / 1000.0
    pv_lev = v_lev / 0.6                                # PV of PDP behind the levered equity (LTV 40%)
    debt_lev = 0.4 * pv_lev
    eps_pdp = 0.501                                     # canonical PDP value elasticity (ledger)
    gcc = np.full(n, oil.get("GCC", 0.0))               # $bn of GCC RE NAV
    y_priv = {0: 0.04 + 0.13, 1: 0.04 + 0.10, 2: 0.04 + 0.06, 3: 0.04 + 0.03}  # ENR income + exits by e [G15]
    eta = 1.2                                           # G12 E6
    put_n = -oil.get("PUT", 0.0)                        # requested protection, m bbl of delta (positive)
    put_tr = []                                          # live tranches: dict(notional_mbbl, k_hi, k_lo, t_exp)
    put_cash = np.zeros(n)
    put_prem = np.zeros(n)
    oil_cash_cum = np.zeros(n)
    x_all = gp["x"]
    x_bar = x_all.mean(axis=1)                           # expected path (cross-path mean)
    dx_bar = (gp["x"] - gp["x_prev"]).mean(axis=1)
    r_oil = {"PRIV": np.zeros((T_Q, n)), "PUB": np.zeros((T_Q, n)), "LEV": np.zeros((T_Q, n)),
             "GCC": np.zeros((T_Q, n))}

    def put_tranche_size():
        """Notional (m bbl) of a fresh 1-year 64/31 tranche that delivers put_n/4 m bbl of spot-equivalent delta
        on the as-of curve (four quarterly tranches)."""
        Fobs = L.observed_curve_monthly(16)
        F, T = float(Fobs[13]), 13 / 12
        s = L.term_vol(T)
        dl = float(L.b76_put_delta(F, 64.0, s * 1.03, T) - L.b76_put_delta(F, 31.0, s * 1.08, T))
        return (put_n / 4.0) / max(abs(dl) * float(L.impulse_x(13)[13]) * F / F1, 1e-9)

    put_size = put_tranche_size() if put_n > 0 else 0.0

    # ---------------- RA03: optional full sleeve for SELL/HOLD cards (fund-held levered upstream)
    sl = oil.get("SLEEVE")
    if sl is not None:
        sv = np.full(n, sl["V0"] if not sl["sell"] else 0.0)        # economic NAV V* held
        su = np.full(n, sl["unf"] if not sl["sell"] else 0.0)       # unfunded attached to the interest
        if sl["sell"]:
            proceeds = sl["bid"] * sl["theta"] * sl["V0"] * (1.0 - sl.get("cost", 0.01))
            if not sl.get("after_topup", False):
                tre += proceeds
            bh["tre"] = bh["tre"] + proceeds          # the action-free ladder replica sees the cash too
            if sl.get("rebuild_beta", False):         # TPA rebuilds the forgone beta with index futures
                n_syn = n_syn + sl["beta_eq"] * proceeds
                im_prev = E.IM_N * n_syn
    else:
        sv = np.zeros(n)
        su = np.zeros(n)

    # ---------------- t0 actions (as t1)
    if pol.amber_t0 > 0:
        tot = E.PRIV0["pc"] + E.PRIV0["cs"]
        for g in ("pc", "cs"):
            sell_amt = pol.amber_t0 * E.PRIV0[g] / tot
            frac = sell_amt / E.PRIV0[g]
            tre += sell_amt * E.PRICE_N[g]
            amber_loss += sell_amt * (1 - E.PRICE_N[g])
            amber_sales += sell_amt
            priv[g] -= sell_amt
            rep[g] -= sell_amt
            unf[g] *= (1 - frac)
    if pol.hf_t0 > 0:
        amt = min(pol.hf_t0, E.HF0)
        hf -= amt
        hf_q += amt * E.HF_SCHED[None, :]
    enc0 = E.IM_N * E.N_SYN0 + E.OPP_IM0
    top_up = max(0.0, pol.reserve * NAV0 - (float(tre[0]) - enc0))
    if top_up > 0:
        a = min(top_up / 0.998, E.LO0["dm"])
        lo["dm"] -= a
        tre += a * 0.998
    up = pol.rcf * pol.rcf_upfront + pol.navf * pol.navf_upfront
    tre -= up
    if sl is not None and sl["sell"] and sl.get("after_topup", False):
        tre += proceeds          # RA03: proceeds land after the t0 reserve top-up, so both legs sell the same DM
    # RA03: the PUB block is a swap of DM equity into energy equity (same $), PRIV/LEV swaps inside private NAV
    # (carried in the PE bucket so the waterfall treats them as red-sale assets), GCC inside private NAV too.

    def nav_of():
        return (tre + sum(lo.values()) + hf + hf_q.sum(axis=1) + sum(priv.values()) + sv - b_r - b_n)

    for t in range(T_Q):
        if t % 4 == 0:
            basis = sum(rep.values()) + tre + sum(lo.values()) + hf + hf_q.sum(axis=1) + sv - b_r - b_n
        # ---------------- RA03 change 1: regimes from the canonical generator
        crisis_prev = crisis
        crisis = gp["crisis"][t]
        z = gp["z"][t]
        onset = crisis & ~crisis_prev
        cdur = np.where(crisis, cdur + 1, 0)
        since_exit = np.where(crisis, 0, np.where(crisis_prev & ~crisis, 1, since_exit + 1))
        ue = rng.random(n)
        o_row = np.where(ue < 0.85, 0, np.where(ue < 0.98, 1, 2))
        n_row = np.where(ue < 0.05, 0, np.where(ue < 0.89, 1, 2))
        d_up = 1 - m.d_stay
        d_row = np.where(ue < 0.1 * d_up, 0, np.where(ue < d_up, 1, 2))
        f_row = np.where(ue < 0.6, 2, 1)
        e_new = np.where(e == 0, o_row, np.where(e == 1, n_row, np.where(e == 2, d_row, f_row)))
        uf = rng.random(n)
        e = np.where(crisis, np.where((e == 3) | (uf < 0.8), 3, 2), e_new)

        # ---------------- market returns (as t1)
        zz = rng.standard_normal(n)
        drift = mu_calm + (m.repricing_drift if t < m.repricing_q else 0.0) \
            + np.where(since_exit <= E.REBOUND_Q, E.REBOUND_ADD, 0.0)
        c_mu, c_sd = E.crisis_mu_sd(cdur)
        r_eq = np.where(crisis, c_mu + c_sd * zz, drift + E.EQ_CALM_SD * zz)
        r_eq = np.maximum(r_eq, -0.6)
        r_em = 1.2 * r_eq + 0.04 * rng.standard_normal(n)
        r_fi = np.where(crisis, m.fi_crisis_q, m.fi_g / 4) + 0.02 * (0.3 * zz + 0.95 * rng.standard_normal(n))
        r_tre = np.where(crisis, 0.4 * CASH_Q + 0.27 * m.ust_crisis_q + 0.33 * (-0.005), 0.0100)
        r_hf = CASH_Q + 0.3 * (r_eq - CASH_Q) + alpha_hf / 4 + np.where(crisis, -0.02, 0.0) \
            + 0.025 * rng.standard_normal(n)
        tre *= 1 + r_tre
        lo["dm"] *= 1 + r_eq
        lo["em"] *= 1 + r_em
        lo["fi"] *= 1 + r_fi
        hf *= 1 + r_hf
        hf_q *= (1 + r_hf)[:, None]
        bh["tre"] *= 1 + r_tre
        bh["dm"] *= 1 + r_eq
        bh["em"] *= 1 + r_em
        bh["fi"] *= 1 + r_fi
        bh["hf"] *= 1 + r_hf
        for g in E.PRIV0:
            econ = CASH_Q + E.BETA[g] * (r_eq - CASH_Q) + alpha[g] / 4 + np.where(crisis & (g == "pc"), -0.02, 0.0)
            priv[g] *= 1 + econ
            rep[g] *= 1 + (0.5 * econ + 0.5 * econ_prev[g])
            econ_prev[g] = econ

        # ---------------- RA03 change 3: oil P&L (de-meaned) and oil cash flows
        dx = (gp["x"][t] - gp["x_prev"][t]) - dx_bar[t]
        xdev = gp["x"][t] - x_bar[t]
        r_priv_oil = eps["PRIV"] * dx
        r_pub_oil = eps["PUB"] * dx
        r_oil["PRIV"][t] = r_priv_oil
        r_oil["PUB"][t] = r_pub_oil
        pnl_priv = v_priv * r_priv_oil
        v_priv = v_priv + pnl_priv
        f3 = np.exp(eta * _f3_dev(gp["x"][t], x_bar[t]))
        y_e = np.array([y_priv[k] for k in range(4)])[e]
        cf_priv = v_priv * y_e / 4 * (f3 - 1.0)
        # levered upstream: PV follows the curve; equity = PV - debt; RBL over-advance cured by the owner
        pv_new = pv_lev * np.exp(eps_pdp * dx)
        cf_lev = (v_lev * 0.07 / 4) * (f3 - 1.0)        # direct ENR income 7% (G15 ENR_DIR) x oil elasticity
        cure = np.zeros(n)
        if t % 2 == 1:                                   # semi-annual redetermination
            bb = 0.6 * 0.85 * pv_new
            over = np.maximum(debt_lev - bb, 0.0)
            cure = over
            debt_lev = debt_lev - over
        r_oil["LEV"][t] = np.where(v_lev > 1e-12, (pv_new - pv_lev) / np.maximum(pv_lev - 0.4 * pv_lev, 1e-12),
                                   0.0)
        pv_lev = pv_new
        v_lev_new = np.maximum(pv_lev - debt_lev, 0.0)
        pnl_lev = v_lev_new - v_lev                       # NAV change; includes the cure injected (paid in cash)
        v_lev = v_lev_new
        # GCC real estate (state exposure, G15): SG value -2.5%/q (yr1) then -1.25%/q; GW -3.3%/q; income 4.5%
        g_r = np.where(z == L.iSG, -0.025, np.where(z == L.iGW, -0.033, np.where(z == L.iDB, -0.03, 0.0)))
        g_r = g_r + np.where((z == L.iN) | (z == L.iB), 0.005, 0.0)     # recovery drift outside stress [I]
        g_r = g_r - (g_r * (gcc > 0)).mean() if gcc.any() else g_r      # de-mean: pure state exposure
        r_oil["GCC"][t] = g_r
        pnl_gcc = gcc * g_r
        gcc = gcc + pnl_gcc
        inc_mult = np.where(z == L.iSG, 0.90, np.where(z == L.iGW, 0.90, np.where(z == L.iDB, 0.85, 1.0)))
        cf_gcc = gcc * 0.045 / 4 * (inc_mult - 1.0)
        # cash not distributed (or paid out in excess) stays in (leaves) the vehicle's NAV: the oil block's cash
        # channel is a timing effect on top of its value P&L, not a second loss
        v_priv = v_priv - cf_priv
        v_lev = v_lev - cf_lev
        gcc = gcc - cf_gcc
        # value effects: private blocks sit in the PE bucket's economic and reported NAV (reported smoothed)
        dv_priv_tot = pnl_priv + pnl_lev + pnl_gcc - cf_priv - cf_lev - cf_gcc
        priv["pe"] = priv["pe"] + dv_priv_tot
        rep["pe"] = rep["pe"] + 0.5 * dv_priv_tot
        # public energy equity: a DM-equity swap; its oil P&L moves the DM book and the buy-and-hold CBC replica
        if v_pub0 > 0:
            pnl_pub = (lo["dm"] / np.maximum(E.LO0["dm"], 1e-9)) * v_pub0 * r_pub_oil
            lo["dm"] = lo["dm"] + pnl_pub
            bh["dm"] = bh["dm"] + (bh["dm"] / E.LO0["dm"]) * v_pub0 * r_pub_oil
        # overlay put spreads: expiry payoffs, then buy a fresh tranche each quarter
        pay = np.zeros(n)
        prem = np.zeros(n)
        if put_size > 0:
            live = []
            for tr in put_tr:
                if tr["t_exp"] == t:
                    px = gp["P_q"][t]
                    pay = pay + tr["n"] * np.clip(tr["k_hi"] - px, 0.0, tr["k_hi"] - tr["k_lo"]) / 1000.0
                else:
                    live.append(tr)
            put_tr = live
            # fresh 1-year tranche, premium on each path's own model curve (forward ~ E1 at 12 months)
            Fp = np.exp(L.LN70 + (1 - L.KM) ** 12 * (gp["x"][t] - L.LN70) + 12 * float(L.MU_Z[L.iN]))
            s = L.term_vol(1.0)
            unit = (L.b76_put(Fp, 64.0, s * 1.03, 1.0) - L.b76_put(Fp, 31.0, s * 1.08, 1.0))
            prem = put_size * unit / 1000.0
            put_tr.append({"n": put_size, "k_hi": 64.0, "k_lo": 31.0, "t_exp": t + 4})
        put_cash += pay
        put_prem += prem
        # sleeve (HOLD case): value return, oil P&L, oil-elastic distributions, calls on its unfunded
        cf_sl = np.zeros(n)
        if sl is not None and not sl["sell"]:
            # alpha is measured against the implementable beta-matched basket (index futures at the engine's
            # financing spread), so the sleeve's beta leg carries the same spread as the SELL leg's rebuild
            spr = np.where(crisis, E.FUT_SPREAD_S, E.FUT_SPREAD_N) if sl.get("basket_spread", True) else 0.0
            r_sl = (CASH_Q + sl["beta_eq"] * (r_eq - CASH_Q - spr / 4.0) + (sl["alpha"] + sl["g_pq"]) / 4.0
                    + sl["eps"] * dx)
            sv = sv * (1.0 + r_sl)
            dist_sl = sv * y_e / 4.0 * f3
            call_sl = su * E._q(0.28)
            sv = sv - dist_sl + call_sl
            su = su - call_sl
            cf_sl = dist_sl - call_sl
            priv["pe"] = priv["pe"] + 0.0      # sleeve tracked separately; NAV added in nav_of via sv
        oil_cf = cf_priv + cf_lev + cf_gcc - cure + pay - prem + cf_sl
        oil_cash_cum += oil_cf

        # ---------------- private cash flows (as t1)
        mD = np.array([1.25, 1.0, 0.50, m.md_f])[e]
        mC = np.array([1.3, 1.0, 0.97, m.mc_f])[e]
        dist = np.zeros(n)
        for g in ("pe", "sec", "co"):
            d = E._q(np.minimum(0.95, E.DIST_NORMAL[g] * mD * m.phi)) * priv[g]
            priv[g] -= d
            rep[g] -= d
            dist += d
        mDc = np.array([1.05, 1.0, 0.92, 0.57])[e]
        for g in ("cs", "pc"):
            d = E._q(E.DIST_NORMAL[g] * mDc) * priv[g]
            priv[g] -= d
            rep[g] -= d
            dist += d
        cq = E._q(np.minimum(0.95, E.CALL_BASE * mC))
        calls = np.zeros(n)
        for g in E.UNF0:
            c = cq * unf[g]
            if g == "pe":
                c = c + np.where(onset, 0.05 * unf[g], 0.0)
            c = np.minimum(c, unf[g])
            unf[g] -= c
            priv[g] += c
            rep[g] += c
            calls += c
        c = np.full(n, E.SEC_DEF0 / 4 if t < 4 else 0.0)
        sec_def -= c
        priv["sec"] += c
        rep["sec"] += c
        calls += c
        c = np.minimum(pc_rev, np.where(onset, 0.5 * pc_rev, E._q(0.15) * pc_rev))
        pc_rev -= c
        priv["pc"] += c
        rep["pc"] += c
        calls += c

        # ---------------- stage (as t1)
        nav_now = nav_of()
        im_req = np.where(crisis, E.IM_S, E.IM_N) * n_syn
        opp_im = np.where(crisis & (m.opp_mult > 1), 2.0, 1.0) * E.OPP_IM0
        enc = im_req + opp_im
        usable = tre - enc
        liq_share = (usable + sum(lo.values()) + E.HF_CASH90 * hf + hf_q[:, 0]) / nav_now
        tre_share = usable / nav_now
        stage = np.zeros(n, dtype=int)
        stage = np.maximum(stage, np.where(liq_share < 0.28, 1, 0))
        stage = np.maximum(stage, np.where(liq_share < 0.24, 2, 0))
        stage = np.maximum(stage, np.where(liq_share < 0.20, 3, 0))
        stage = np.maximum(stage, np.where(tre_share < 0.06, 1, 0))
        stage = np.maximum(stage, np.where(tre_share < 0.04, 2, 0))
        stage = np.maximum(stage, np.where(crisis, 1, 0))
        for s_ in range(4):
            stage_hist[t, s_] += float((stage == s_).mean())
        amber_up = stage >= 1
        red_up = (stage >= 2) | crisis

        # ---------------- new commitments (as t1)
        k = np.full(n, pol.pace / 4)
        if pol.pace_cut:
            k = np.where(amber_up, 0.25 * k, k)
        for g, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1)):
            unf[g] += w * k
        co_deal = 0.1 * k
        priv["co"] += co_deal
        rep["co"] += co_deal

        # ---------------- RA03 change 2: owner draw from the canonical owner-draw engine
        d_year = gp["rates"][t // 4]
        draw_rate_q[t] = d_year
        inst = d_year * basis / 4
        inst_mode_b = inst
        if pol.band:
            cut = ((stage >= 2) | crisis) & (d_year <= 0.10 + 1e-9)
            new_inst = np.where(cut, 0.05 * basis / 4, inst)
            withheld += inst - new_inst
            inst = new_inst

        # ---------------- overlay (as t1)
        spread = np.where(crisis, E.FUT_SPREAD_S, E.FUT_SPREAD_N)
        vm = n_syn * (r_eq - CASH_Q - spread / 4)
        vm = np.where(crisis & (vm < 0), vm * m.vm_mult, vm)
        prem_t = E.TAIL_PREM * NAV0 / 4
        tail = E.N_TAIL * np.clip(-r_eq - 0.10, 0.0, 0.18)
        opp = 0.0125 / 2 * NAV0 * rng.standard_normal(n) + np.where(crisis, -0.005, 0.001) * NAV0
        opp = np.where(crisis, opp * m.opp_mult, opp)
        d_im = im_req - im_prev
        im_prev = im_req

        f_cost = np.maximum(pol.rcf - b_r, 0.0) * pol.rcf_undrawn_fee / 4 \
            + np.maximum(pol.navf - b_n, 0.0) * pol.navf_undrawn_fee / 4
        if t == 12:
            f_cost = f_cost + pol.rcf * pol.rcf_upfront
        i_cost = b_r * (E.SOFR + pol.rcf_margin) / 4 \
            + b_n * (E.SOFR + pol.navf_margin + np.where(crisis, pol.navf_stress_add, 0.0)) / 4
        opex = 0.001 / 4 * nav_now

        net = inst + calls + co_deal + prem_t + f_cost + i_cost + opex - dist - vm - tail - opp - oil_cf
        tre -= net
        if t < 8:
            vm0 = E.N_SYN0 * (r_eq - CASH_Q - spread / 4)
            vm0 = np.where(crisis & (vm0 < 0), vm0 * m.vm_mult, vm0)
            d_im0 = (np.where(crisis, E.IM_S, E.IM_N) - np.where(crisis_prev, E.IM_S, E.IM_N)) * E.N_SYN0
            nco_bh += (inst_mode_b + calls + co_deal + prem_t + opex - dist - vm0 - tail - opp
                       + np.maximum(d_im0, 0.0) - oil_cf)
            due_bh = hf_bh_q[:, 0].copy()
            paid_bh = np.where(crisis, hf_gate_pass * due_bh, due_bh)
            hf_bh_q[:, :-1] = hf_bh_q[:, 1:]
            hf_bh_q[:, -1] = 0.0
            hf_bh_q[:, 0] += due_bh - paid_bh
            hf_bh_q *= (1 + r_hf)[:, None]
            hf_bh_cash += paid_bh
            cbc_t = ((bh["tre"] - E.IM_N * E.N_SYN0 - E.OPP_IM0) * (1 - 0.038) + bh["dm"] * 0.985
                     + bh["fi"] * 0.95 + bh["em"] * 0.95 + hf_bh_cash)
            nav_bh = sum(bh.values()) + sum(priv.values()) - nco_bh
            gap_t = nco_bh + 0.04 * nav_bh - cbc_t
            gstar = np.maximum(gstar, gap_t)

        # ---------------- hedge-fund queue (as t1)
        due = hf_q[:, 0].copy()
        paid_hf = np.where(crisis, hf_gate_pass * due, due)
        rolled = due - paid_hf
        hf_q[:, :-1] = hf_q[:, 1:]
        hf_q[:, -1] = 0.0
        hf_q[:, 0] += rolled
        tre += paid_hf
        if pol.hf_amber:
            file = np.where(amber_up, 0.5 * hf, 0.0)
            hf -= file
            hf_q += file[:, None] * E.HF_SCHED[None, :]

        # ---------------- NAV facility forced paydown (as t1)
        pool = np.maximum(np.minimum(0.20 * sum(priv.values()), rep["pe"] + rep["sec"]), 1e-9)
        ltv_cap = np.where(crisis, 0.05, 0.10)
        fp = np.maximum(0.0, b_n - ltv_cap * pool)
        b_n -= fp
        tre -= fp

        # ---------------- waterfall (as t1)
        nav_now = nav_of()
        usable = tre - enc
        target = pol.reserve * nav_now
        floor = pol.floor_hard * nav_now
        need = np.maximum(0.0, target - usable)
        room = np.maximum(0.0, np.minimum(0.30 * nav_now, pol.p2s_cap) - n_syn)
        p2s_net = 0.998 - E.IM_N
        a = np.where(~crisis, np.minimum(np.minimum(0.5 * lo["dm"], room), need / p2s_net), 0.0)
        lo["dm"] -= a
        n_syn = n_syn + a
        tre += a * 0.998
        enc = enc + a * E.IM_N
        im_prev = im_prev + a * E.IM_N
        need = need - a * p2s_net
        for key, cap, pn, pc_ in (("dm", 0.5, 0.998, 0.985), ("fi", 0.5, 0.995, 0.95), ("em", 0.5, 0.99, 0.95)):
            price = np.where(crisis, pc_, pn)
            a = np.minimum(np.maximum(cap * lo[key], 0.0), need / price)
            lo[key] -= a
            tre += a * price
            need = need - a * price
        use_fac = red_up | ((tre - enc) < 0.06 * nav_now)
        if pol.rcf > 0:
            avail_f = np.where(crisis, np.where((z == 3) | (z == 5), 0.80, 0.90), 1.0)
            cap_debt = np.maximum(0.0, pol.debt_cap * nav_now - b_r - b_n)
            avail = np.maximum(0.0, np.minimum(pol.rcf * avail_f - b_r, cap_debt))
            dr = np.where(use_fac, np.minimum(avail, need), 0.0)
            b_r += dr
            tre += dr
            need = need - dr
        if pol.navf > 0:
            cap_debt = np.maximum(0.0, pol.debt_cap * nav_now - b_r - b_n)
            avail = np.maximum(0.0, np.minimum(np.minimum(pol.navf, ltv_cap * pool) - b_n, cap_debt))
            dr = np.where(use_fac, np.minimum(avail, need / 0.985), 0.0)
            b_n += dr
            tre += dr * 0.985
            need = need - dr * 0.985
        usable = tre - enc
        need_amber = np.maximum(0.0, np.where(red_up, 0.06, pol.floor_hard + 0.01) * nav_now - usable)
        for g in ("pc", "cs"):
            pr = np.where(crisis, E.PRICE_C[g], E.PRICE_N[g])
            amt = np.minimum(0.10 * priv[g], need_amber / pr)
            frac = amt / np.maximum(priv[g], 1e-9)
            priv[g] -= amt
            rep[g] -= amt
            unf[g] *= 1 - frac
            tre += amt * pr
            need_amber = need_amber - amt * pr
            amber_sales += amt
            amber_loss += amt * (1 - pr)
        usable = tre - enc
        need_floor = np.maximum(0.0, floor - usable)
        depth = np.where(crisis, 2.5, 4.0)
        ok = rng_p.random(n) < np.where(crisis, E.P_SUCC_C, E.P_SUCC_N)
        for g in ("sec", "pe", "co"):
            pr = np.where(crisis, E.PRICE_C[g], E.PRICE_N[g])
            amt = np.where(ok, np.minimum(np.minimum(np.maximum(priv[g], 0.0), depth), need_floor / pr), 0.0)
            frac = amt / np.maximum(priv[g], 1e-9)
            priv[g] -= amt
            rep[g] -= amt
            unf[g] *= 1 - frac
            tre += amt * pr
            need_floor = need_floor - amt * pr
            depth = depth - amt
            red_sales += amt
            red_loss += amt * (1 - pr)
        attempted = np.maximum(0.0, floor - usable) > 1e-6
        red |= attempted
        floor4_breach |= (tre - enc) < floor - 1e-6
        usable = tre - enc
        short = np.maximum(0.0, -usable)
        short_pay = np.minimum(short, inst)
        resid = short - short_pay
        is_short = short > 1e-6
        red |= is_short
        if t < 4:
            black_12m |= is_short
        tre += short_pay
        shortfall += short_pay
        if np.any(resid > 1e-9):
            tot_priv = np.maximum(sum(priv.values()), 1e-9)
            sold = np.minimum(resid / 0.5, tot_priv)
            for g in E.PRIV0:
                share = priv[g] / tot_priv
                priv[g] -= sold * share
                rep[g] -= sold * share
                unf[g] *= 1 - np.minimum(1.0, sold / tot_priv)
            tre += sold * 0.5
            red_sales += sold
            red_loss += sold * 0.5
        paid_fv += (inst - short_pay) * 1.10 ** ((T_Q - t - 1) / 4)
        # RA03 change 4: liquidity-state weight for this path-quarter
        lam[t] = np.where(attempted | is_short, LAMBDA_STAGE[3], LAMBDA_STAGE[stage])

        # ---------------- repayments in calm Green quarters (as t1)
        nav_now = nav_of()
        usable = tre - enc
        excess = np.where(~crisis & (stage == 0), np.maximum(0.0, usable - (pol.reserve + 0.02) * nav_now), 0.0)
        rp = np.minimum(b_n, excess)
        b_n -= rp
        tre -= rp
        excess = excess - rp
        rp = np.minimum(b_r, excess)
        b_r -= rp
        tre -= rp

    nav_T = nav_of()
    w_tilde = nav_T + paid_fv
    k_red = int(red.sum())
    return dict(model=m.key, n=n, p_red=float(red.mean()), k_red=k_red, w_tilde=w_tilde,
                cp_upper_red=E.clopper_pearson_upper(k_red, n), red=red,
                gstar=gstar, gstar_q={q: float(np.quantile(gstar, q)) for q in (0.5, 0.9, 0.95, 0.99, 0.996)},
                w_inv2=float(np.mean((w_tilde / NAV0) ** -2.0)), mean_wtilde=float(w_tilde.mean()),
                lam=lam, r_oil=r_oil, stage_occ=stage_hist.mean(axis=0).tolist(),
                mean_red_loss=float(red_loss.mean()), mean_withheld=float(withheld.mean()),
                put_cash=float(put_cash.mean()), put_prem=float(put_prem.mean()),
                oil_cash_cum_mean=float(oil_cash_cum.mean()), draw_rate_q=draw_rate_q, gp=gp)


def ce_bp(w_inv2_a: float, w_inv2_b: float) -> float:
    """Difference in annualised CRRA(3) certainty-equivalent growth over 5 years, bp a year (b minus a)."""
    ga = w_inv2_a ** (-0.5)
    gb = w_inv2_b ** (-0.5)
    return 1e4 * ((gb ** 0.2 - 1) - (ga ** 0.2 - 1))
