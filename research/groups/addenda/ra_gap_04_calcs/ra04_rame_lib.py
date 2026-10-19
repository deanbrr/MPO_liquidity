"""
ra_gap_04 - RAME misspecification library.   ALL OUTPUTS SYNTHETIC - NOT ADIC DATA.

Builds on the G13 Real-Assets mark engine (G13_calcs/g13_ra_marks_sim.py, imported read-only): its segment
defaults, factor generator and seven-state appraisal Kalman model are reused unchanged. This module adds:
  1. a variant-aware world generator (canonical M1-M6/MALL mapped onto the appraisal/observation layer, the
     pre-registered tau axes, strategic marks, starting gaps G0 and a secondary-bid channel);
  2. a production RAME fit (G13 MLE, optionally with a lagged-tau loading for the detection test);
  3. a time-varying Kalman filter (sequential univariate updates) used for the variant-aware ORACLE and for
     the bid channel with a pre-bid ("leave-one-out") and post-bid state;
  4. metrics on the canonical gate scale (excess CRPS vs the oracle, 80% coverage, SELL bias, SELL regret)
     plus R2 (nowcast RMSE / appraisal RMSE) and the annual-return error of the nowcast index.

Canonical mapping onto RAME (only the generator changes; the production estimator stays fixed):
  M1  regime-dependent smoothing: lambda + 0.10 in the down regime (valuers smooth more in downturns)
  M2  nonlinear anchoring: lambda + 0.15 whenever true value is below the prior mark (valuers resist markdowns)
  M3  t3 tails in true shocks and in every observation noise, rescaled to the Gaussian 80% width
  M4  correlated errors: the transaction index is contaminated by appraisals, tau = (1-c) v + c a, c = 0.3
  M5  strategic marks (designed pay): appraisal level +0.8pp, +2pp on the 30% of holdings flagged SELL
  M5s strategic marks (status-quo pay): +3.2pp, +2pp on flagged holdings
  M6  prior shift: external appraisals less frequent than assumed (index noise AR 0.90 vs the filter's
      fixed 0.75) and appraisal noise x1.5
  MALL M1+M2+M3+M4+M5+M6
Pre-registered RA axes (synthesis sec. 11): tau lagged 1-2 quarters (TL1, TL2), AR-smoothed 0.3/0.5 (TA3, TA5),
level-biased (+3% constant, TB; +4% in the down regime only, TBC), worst case TW = TL1+TA5+TBC, MALL_T = MALL+TW.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

try:
    import numba as nb
    NUMBA = True
except Exception:  # noqa: BLE001
    NUMBA = False

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "G13_calcs"))
import g13_ra_marks_sim as g  # noqa: E402  (read-only import of the G13 engine)

SYN = "SYNTHETIC - NOT ADIC DATA"
Z80 = 1.2815516
T3_SCALE = Z80 / 1.6377444           # t3 rescaled to the Gaussian 80% width (canonical M3)
T3_VAR = T3_SCALE ** 2 * 3.0         # variance of the rescaled t3 relative to the Gaussian (1.837)
D_BID = 3.0                          # bid duration (G13: ln q = v - a - D (y_P - y_V) + eps)
PREM_N, PREM_DOWN = 0.05, 0.09       # buyer premium y_P - y_V: normal / down regime (truth)
SIG_Q = 0.05                         # bid noise
H_SELL = math.exp(-D_BID * PREM_N)   # SELL iff q >= H_SELL * theta_hat  (0.861)

MALL = dict(lam_regime=0.10, lam_asym=0.15, t3=True, tau_contam=0.30, strat=0.008, phi_e=0.90, sig_e_mult=1.5)
TW = dict(tau_lag=1, tau_ar=0.5, tau_bias_down=0.04)
VARIANTS = {
    "M0": {}, "M1": dict(lam_regime=0.10), "M2": dict(lam_asym=0.15), "M3": dict(t3=True),
    "M4": dict(tau_contam=0.30), "M5": dict(strat=0.008), "M5s": dict(strat=0.032),
    "M6": dict(phi_e=0.90, sig_e_mult=1.5), "MALL": MALL,
    "TL1": dict(tau_lag=1), "TL2": dict(tau_lag=2), "TA3": dict(tau_ar=0.3), "TA5": dict(tau_ar=0.5),
    "TB": dict(tau_bias=0.03), "TBC": dict(tau_bias_down=0.04), "TW": TW, "MALL_T": {**MALL, **TW},
}


# ------------------------------------------------------------------------------------------------------------
# 1. Generator
# ------------------------------------------------------------------------------------------------------------
def sim_world(rng, T: int, seg: str, var: dict, n_assets: int = 60) -> dict:
    """One segment world, index 0..T. Same truth equations and defaults as G13 sim_segment, plus variant hooks."""
    S = g.SEGMENTS[seg]
    F = g.FACTORS
    Fz = g.sim_factors(rng, T)
    r, pi, o, z = Fz["r"], Fz["pi"], Fz["o"], Fz["z"]
    t3 = bool(var.get("t3", False))

    def shk(size=None):
        if t3:
            return rng.standard_t(3, size) * T3_SCALE
        return rng.standard_normal(size)

    Tp = T + 1
    x = np.empty(Tp)
    nn = np.empty(Tp)
    x[0] = S["x0"]
    nn[0] = 0.0
    for t in range(1, Tp):
        down = z[t] == 1
        sx = S["sig_x"] * (F["sigx_mult_down"] if down else 1.0)
        x[t] = (S["phi_x"] * x[t - 1] + S["b_r"] * (r[t] - r[t - 1]) + (F["mu_x_down"] if down else 0.0)
                + sx * shk())
        nn[t] = (nn[t - 1] + (S["g"] + S["pass_pi"] * (pi[t] - F["pibar"])) / 4.0
                 + S["beta_oil"] * (o[t] - o[t - 1]) + (F["mu_n_down"] if down else 0.0) + S["sig_n"] * shk())
    vbar = nn - x
    w = np.zeros((n_assets, Tp))
    w[:, 1:] = np.cumsum(S["sig_i"] * shk((n_assets, T)), axis=1)
    # appraisal: two-component smoothing with variant lambda path
    lam0 = S["lam_agg"]
    lam_i = S["lam_idio"]
    lag = S["lag"]
    lam_used = np.full(Tp, lam0)
    abar = np.empty(Tp)
    arel = np.zeros((n_assets, Tp))
    abar[0] = vbar[0]
    for t in range(1, Tp):
        lt = lam0 + (var.get("lam_regime", 0.0) if z[t] == 1 else 0.0)
        src = vbar[max(t - lag, 0)]
        if var.get("lam_asym", 0.0) and src < abar[t - 1]:
            lt = lt + var["lam_asym"]
        lt = min(0.95, lt)
        lam_used[t] = lt
        abar[t] = (1 - lt) * src + lt * abar[t - 1]
        arel[:, t] = (1 - lam_i) * w[:, max(t - lag, 0)] + lam_i * arel[:, t - 1]
    # calendar noise: each asset re-appraised externally with prob p per quarter (p = 1 - phi_e; G13: yearly)
    phi_e = var.get("phi_e", 0.75)
    sig_e = S["sig_e"] * var.get("sig_e_mult", 1.0)
    e = np.zeros((n_assets, Tp))
    cur = sig_e * shk(n_assets)
    if phi_e == 0.75:                      # G13 calendar: one external appraisal a year in a fixed quarter
        appr_q = rng.integers(0, 4, size=n_assets)
        for t in range(Tp):
            redraw = (t % 4) == appr_q
            cur = np.where(redraw, sig_e * shk(n_assets), cur)
            e[:, t] = cur
    else:
        for t in range(Tp):
            redraw = rng.random(n_assets) < (1.0 - phi_e)
            cur = np.where(redraw, sig_e * shk(n_assets), cur)
            e[:, t] = cur
    a_index = (abar[None, :] + arel + e).mean(axis=0)
    # strategic marks (M5/M5s): previous-period SELL screen on true staleness, defend-the-holding uplift
    flag = np.zeros(Tp)
    strat_bias = np.zeros(Tp)
    if var.get("strat", 0.0):
        for t in range(1, Tp):
            flag[t] = float((vbar[t - 1] - (a_index[t - 1] - strat_bias[t - 1]) + 0.02 * rng.standard_normal())
                            < -0.04)
            strat_bias[t] = var["strat"] + 0.30 * 0.02 * flag[t]
        a_index = a_index + strat_bias
    # listed proxy (unlevered), AR(1) premium
    p = np.empty(Tp)
    p[0] = S["sig_p"] / math.sqrt(1 - S["phi_p"] ** 2) * shk()
    for t in range(1, Tp):
        p[t] = S["phi_p"] * p[t - 1] + S["sig_p"] * shk()
    L = S["beta_L"] * vbar + p + S["sig_L"] * shk(Tp)
    # transaction index tau with the pre-registered axes
    tl = int(var.get("tau_lag", 0))
    base = np.concatenate([np.repeat(vbar[0], tl), vbar[:Tp - tl]]) if tl > 0 else vbar.copy()
    rho = var.get("tau_ar", 0.0)
    if rho:
        ts = np.empty(Tp)
        ts[0] = base[0]
        for t in range(1, Tp):
            ts[t] = rho * ts[t - 1] + (1 - rho) * base[t]
        base = ts
    c = var.get("tau_contam", 0.0)
    if c:
        base = (1 - c) * base + c * a_index
    tau_bias = var.get("tau_bias", 0.0) + var.get("tau_bias_down", 0.0) * (z == 1)
    tau = base + tau_bias + S["sig_tau"] * shk(Tp)
    # secondary bid on a representative fund interest, every quarter
    prem = np.where(z == 1, PREM_DOWN, PREM_N)
    lnq = vbar - a_index - D_BID * prem + SIG_Q * shk(Tp)
    bid_seen = rng.random(Tp) < 0.5
    return dict(seg=seg, vbar=vbar, a=a_index, L=L, tau=tau, z=z, lam_used=lam_used, flag=flag,
                strat_bias=strat_bias, tau_bias=tau_bias, lnq=lnq, prem=prem, bid_seen=bid_seen, x=x, nn=nn)


def ss_params(seg: str, n_worlds: int = 200, T: int = 80, seed: int = 4242) -> tuple:
    """Index-level parameters of RAME's own state-space model implied by the G13 segment calibration:
    drift and volatility of the true index from G13 worlds (pooled moments), lambda/lag/listed/tau from the
    G13 defaults, calendar-noise innovation for a 60-asset index with yearly external appraisals."""
    S = g.SEGMENTS[seg]
    rng = default_rng_local(seed)
    dv = []
    for _ in range(n_worlds):
        Fz = g.sim_factors(rng, T)
        d = g.sim_segment(rng, T, seg, Fz, 2)
        dv.append(np.diff(d["vbar"]))
    dv = np.concatenate(dv)
    sxi = math.sqrt(S["sig_e"] ** 2 / 60 * (1 - 0.75 ** 2))
    return (S["lam_agg"], float(dv.mean()), float(dv.std()), sxi, S["beta_L"], S["phi_p"], S["sig_p"],
            S["sig_L"], S["sig_tau"], 0.0)


def default_rng_local(seed):
    return np.random.default_rng(seed)


def regime_path(rng, Tp):
    F = g.FACTORS
    z = np.zeros(Tp, dtype=np.int64)
    for t in range(1, Tp):
        u = rng.random()
        z[t] = (1 if u < F["p_nd"] else 0) if z[t - 1] == 0 else (0 if u < F["p_dn"] else 1)
    return z


def sim_ss_world(rng, T: int, seg: str, var: dict, P: tuple) -> dict:
    """Canonical layer: data drawn from RAME's own state-space model (the SBC case under M0), with the
    canonical M1-M6 mechanisms and the tau axes applied on top. P = (lam, mu, sv, sxi, beta, phip, sp, sL, st, cL)."""
    S = g.SEGMENTS[seg]
    lam0, mu, sv, sxi, beta, phip, sp, sL, st, cL = P
    t3 = bool(var.get("t3", False))

    def shk(size=None):
        if t3:
            return rng.standard_t(3, size) * T3_SCALE
        return rng.standard_normal(size)

    Tp = T + 1
    z = regime_path(rng, Tp)
    lag = S["lag"]
    v = np.empty(Tp)
    v[0] = 0.0
    for t in range(1, Tp):
        v[t] = mu + v[t - 1] + sv * shk()
    lam_used = np.full(Tp, lam0)
    s = np.empty(Tp)
    s[0] = v[0]
    for t in range(1, Tp):
        lt = lam0 + (var.get("lam_regime", 0.0) if z[t] == 1 else 0.0)
        src = v[max(t - lag, 0)]
        if var.get("lam_asym", 0.0) and src < s[t - 1]:
            lt = lt + var["lam_asym"]
        lt = min(0.95, lt)
        lam_used[t] = lt
        s[t] = (1 - lt) * src + lt * s[t - 1]
    phi_e = var.get("phi_e", 0.75)
    sxi_v = sxi * math.sqrt(var.get("sig_e_mult", 1.0) ** 2 * (1 - phi_e ** 2) / (1 - 0.75 ** 2))
    e = np.empty(Tp)
    e[0] = sxi_v / math.sqrt(1 - phi_e ** 2) * shk()
    for t in range(1, Tp):
        e[t] = phi_e * e[t - 1] + sxi_v * shk()
    a = s + e
    flag = np.zeros(Tp)
    strat_bias = np.zeros(Tp)
    if var.get("strat", 0.0):
        for t in range(1, Tp):
            flag[t] = float((v[t - 1] - (a[t - 1]) + 0.02 * rng.standard_normal()) < -0.04)
            strat_bias[t] = var["strat"] + 0.30 * 0.02 * flag[t]
        a = a + strat_bias
    p = np.empty(Tp)
    p[0] = sp / math.sqrt(1 - phip ** 2) * shk()
    for t in range(1, Tp):
        p[t] = phip * p[t - 1] + sp * shk()
    L = cL + beta * v + p + sL * shk(Tp)
    tl = int(var.get("tau_lag", 0))
    base = np.concatenate([np.repeat(v[0], tl), v[:Tp - tl]]) if tl > 0 else v.copy()
    rho = var.get("tau_ar", 0.0)
    if rho:
        ts = np.empty(Tp)
        ts[0] = base[0]
        for t in range(1, Tp):
            ts[t] = rho * ts[t - 1] + (1 - rho) * base[t]
        base = ts
    c = var.get("tau_contam", 0.0)
    if c:
        base = (1 - c) * base + c * a
    tau_bias = var.get("tau_bias", 0.0) + var.get("tau_bias_down", 0.0) * (z == 1)
    tau = base + tau_bias + st * shk(Tp)
    prem = np.where(z == 1, PREM_DOWN, PREM_N)
    lnq = v - a - D_BID * prem + SIG_Q * shk(Tp)
    bid_seen = rng.random(Tp) < 0.5
    return dict(seg=seg, vbar=v, a=a, L=L, tau=tau, z=z, lam_used=lam_used, flag=flag, strat_bias=strat_bias,
                tau_bias=tau_bias, lnq=lnq, prem=prem, bid_seen=bid_seen)


def shock_last(d: dict, seg: str, S_shock: float) -> dict:
    """G0 experiment: a true value shock of size S over the last two quarters (half at T-1, half at T) that
    appraisals have not absorbed; listed and tau react at once. Returns a modified copy."""
    S = g.SEGMENTS[seg]
    out = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in d.items()}
    Tn = len(d["vbar"]) - 1
    dv = np.zeros(Tn + 1)
    dv[Tn - 1] = -S_shock / 2
    dv[Tn] = -S_shock
    out["vbar"] = d["vbar"] + dv
    lam, lag = S["lam_agg"], S["lag"]
    a = out["a"]
    for t in (Tn - 1, Tn):              # appraisal responds through the smoothing recursion only
        a[t] = a[t] + (1 - lam) * dv[t - lag] + lam * (a[t - 1] - d["a"][t - 1])
    out["a"] = a
    out["L"] = d["L"] + S["beta_L"] * dv
    out["tau"] = d["tau"] + dv
    return out


# ------------------------------------------------------------------------------------------------------------
# 2. Production RAME fit (G13 model; optional lagged-tau loading)
# ------------------------------------------------------------------------------------------------------------
def build_prod(th, lag, use_L, use_tau, tau_lag=0):
    params = g.unpack(th, use_L, use_tau)
    Tm, cvec, Q, Z, Hd = g.ss_matrices(params, lag)
    if tau_lag:
        Z = Z.copy()
        Z[2, 0] = 0.0
        Z[2, tau_lag] = 1.0
    return params, Tm, cvec, Q, Z, Hd


def _init(y, params):
    lam, mu, sv, sxi, beta, phip, sp, sL, st, cL = params
    a0v = y[0, 0]
    a0 = np.array([a0v, a0v, a0v, a0v, 0.0, a0v, 0.0])
    P0 = np.diag(np.array([0.05 ** 2] * 4 + [(sp ** 2) / max(1e-6, 1 - phip ** 2), 0.02 ** 2,
                                              (sxi ** 2) / (1 - g.PHI_E ** 2)]))
    return a0, P0


def _negll(th, y, mask, lag, use_L, use_tau, tau_lag):
    params, Tm, cvec, Q, Z, Hd = build_prod(th, lag, use_L, use_tau, tau_lag)
    yy = y.copy()
    yy[:, 1] = yy[:, 1] - params[9]
    a0, P0 = _init(y, params)
    try:
        ll, _, _ = g._kf(yy, mask, Tm, cvec, Q, Z, Hd, a0, P0, False)
    except Exception:  # noqa: BLE001  (non-PD innovation covariance at an extreme trial point: infeasible)
        return 1e10
    return -ll if np.isfinite(ll) else 1e10


def fit_prod(a_idx, L, tau, lag, use_L=True, use_tau=True, tau_every=1, tau_lag=0):
    """MLE as in G13 kf_fit (three L-BFGS-B starts, same bounds); returns params, theta vector, nll."""
    y, mask = g.kf_build(a_idx, L, tau, use_L, use_tau, tau_every)
    ra = np.diff(a_idx)
    lam0 = min(max(g.acf1(ra), 0.10), 0.92)
    sv0 = max(np.std(ra) * math.sqrt((1 + lam0) / (1 - lam0)), 0.01)
    cL0 = float(np.mean(L - a_idx)) if use_L else 0.0
    th0 = np.array([math.log(lam0 / (0.98 - lam0)), np.mean(ra) / 0.01, math.log(sv0), math.log(0.005),
                    1.0, 1.5, math.log(0.05), math.log(0.01), math.log(0.03), cL0])
    B = g.TH_BOUNDS
    clip = lambda v: np.array([min(max(q, lo + 1e-6), hi - 1e-6) for q, (lo, hi) in zip(v, B)])
    th0 = clip(th0)
    best = None
    for dlt in (np.zeros(10), np.array([1.2, 0, 0.3, 0, 0, 0, 0, 0, 0, 0]), np.array([-1.0, 0, -0.2, 0, 0, 0, 0, 0, 0, 0])):
        st = clip(np.clip(th0 + dlt, -5.9, 5.9))
        res = optimize.minimize(_negll, st, args=(y, mask, lag, use_L, use_tau, tau_lag), method="L-BFGS-B", bounds=B)
        if best is None or res.fun < best.fun:
            best = res
    return dict(th=best.x, nll=float(best.fun), params=g.unpack(best.x, use_L, use_tau), use_L=use_L,
                use_tau=use_tau, tau_every=tau_every, tau_lag=tau_lag)


# ------------------------------------------------------------------------------------------------------------
# 3. Time-varying Kalman filter (sequential univariate updates; optional second-stage bid column)
# ------------------------------------------------------------------------------------------------------------
def _kf_tv_core(y, mask, Tt, ct, Q, Z, dt, Hd, a0, P0, bid_col, diag_col):
    T, k = y.shape
    a = a0.copy()
    P = P0.copy()
    ll = 0.0
    v_pre = np.zeros(T)
    P_pre = np.zeros(T)
    v_post = np.zeros(T)
    P_post = np.zeros(T)
    innov = np.full(T, np.nan)
    innov_var = np.full(T, np.nan)
    for t in range(T):
        a = ct[t] + Tt[t] @ a
        P = Tt[t] @ P @ Tt[t].T + Q
        for j in range(k):
            if j == bid_col or not mask[t, j]:
                continue
            zj = Z[j]
            vj = y[t, j] - dt[t, j] - zj @ a
            Pz = P @ zj
            Fv = zj @ Pz + Hd[j]
            K = Pz / Fv
            a = a + K * vj
            P = P - np.outer(K, Pz)
            ll += -0.5 * (math.log(2 * math.pi * Fv) + vj * vj / Fv)
            if j == diag_col:
                innov[t] = vj
                innov_var[t] = Fv
        P = 0.5 * (P + P.T)
        v_pre[t] = a[0]
        P_pre[t] = P[0, 0]
        if bid_col >= 0 and mask[t, bid_col]:
            zj = Z[bid_col]
            vj = y[t, bid_col] - dt[t, bid_col] - zj @ a
            Pz = P @ zj
            Fv = zj @ Pz + Hd[bid_col]
            K = Pz / Fv
            a = a + K * vj
            P = P - np.outer(K, Pz)
            P = 0.5 * (P + P.T)
            ll += -0.5 * (math.log(2 * math.pi * Fv) + vj * vj / Fv)
        v_post[t] = a[0]
        P_post[t] = P[0, 0]
    return ll, v_pre, P_pre, v_post, P_post, innov, innov_var


kf_tv = nb.njit(cache=False)(_kf_tv_core) if NUMBA else _kf_tv_core


def run_filter(system: dict):
    s = system
    return kf_tv(s["y"], s["mask"], s["Tt"], s["ct"], s["Q"], s["Z"], s["dt"], s["Hd"], s["a0"], s["P0"],
                 s["bid_col"], s["diag_col"])


def prod_system(d: dict, fit: dict, lag: int, use_bid=False, bid_prem=PREM_N, tau_every=1):
    """Production RAME as a time-varying system (8 states incl. an unused tau* slot) with optional bid row."""
    params = fit["params"]
    lam, mu, sv, sxi, beta, phip, sp, sL, st, cL = params
    _, Tm7, c7, Q7, Z7, H7 = build_prod(fit["th"], lag, fit["use_L"], fit["use_tau"], fit.get("tau_lag", 0))
    Tn = len(d["a"])
    m = 8
    Tm = np.zeros((m, m))
    Tm[:7, :7] = Tm7
    Q = np.zeros((m, m))
    Q[:7, :7] = Q7
    c = np.zeros(m)
    c[:7] = c7
    Z = np.zeros((4, m))
    Z[:3, :7] = Z7
    Z[3, 0] = 1.0
    Hd = np.array([H7[0], H7[1], H7[2], SIG_Q ** 2])
    y = np.zeros((Tn, 4))
    y[:, 0] = d["a"]
    y[:, 1] = d["L"]
    y[:, 2] = d["tau"]
    y[:, 3] = d["lnq"] + d["a"]
    mask = np.zeros((Tn, 4), dtype=np.bool_)
    mask[:, 0] = True
    if fit["use_L"]:
        mask[:, 1] = True
    if fit["use_tau"]:
        mask[::tau_every, 2] = True
    if use_bid:
        mask[:, 3] = d["bid_seen"]
    dt = np.zeros((Tn, 4))
    dt[:, 1] = cL
    dt[:, 3] = -D_BID * bid_prem
    a0v = d["a"][0]
    a0 = np.array([a0v, a0v, a0v, a0v, 0.0, a0v, 0.0, a0v])
    P0 = np.diag(np.array([0.05 ** 2] * 4 + [(sp ** 2) / max(1e-6, 1 - phip ** 2), 0.02 ** 2,
                                              (sxi ** 2) / (1 - g.PHI_E ** 2), 0.05 ** 2]))
    return dict(y=y, mask=mask, Tt=np.repeat(Tm[None], Tn, axis=0), ct=np.repeat(c[None], Tn, axis=0), Q=Q,
                Z=Z, dt=dt, Hd=Hd, a0=a0, P0=P0, bid_col=3 if use_bid else -1, diag_col=2)


def oracle_system(d: dict, seg: str, var: dict, pt: tuple, use_bid=False, use_tau=True, use_L=True,
                  tau_every=1):
    """Variant-aware oracle: knows the generator's mechanism (lambda path, tau lag/AR/contamination/bias,
    strategic mark bias, calendar persistence, t3 variances, bid premium path). Nuisance parameters are the
    pseudo-true production parameters pt from a long M0 world of the same segment."""
    S = g.SEGMENTS[seg]
    lam_p, mu, sv, sxi, beta, phip, sp, sL, st, cL = pt
    t3v = T3_VAR if var.get("t3", False) else 1.0
    phi_e = var.get("phi_e", 0.75)
    sxi_o = sxi * math.sqrt(var.get("sig_e_mult", 1.0) ** 2 * (1 - phi_e ** 2) / (1 - 0.75 ** 2))
    lag = S["lag"]
    tl = int(var.get("tau_lag", 0))
    rho = var.get("tau_ar", 0.0)
    cc = var.get("tau_contam", 0.0)
    Tn = len(d["a"])
    m = 8
    Tt = np.zeros((Tn, m, m))
    ct = np.zeros((Tn, m))
    for t in range(Tn):
        Tm = Tt[t]
        Tm[0, 0] = 1.0
        Tm[1, 0] = 1.0
        Tm[2, 1] = 1.0
        Tm[3, 2] = 1.0
        Tm[4, 4] = phip
        lt = d["lam_used"][t]
        Tm[5, 5] = lt
        Tm[5, lag - 1] += 1 - lt
        Tm[6, 6] = phi_e
        if rho:
            Tm[7, 7] = rho
            if tl == 0:
                Tm[7, 0] += 1 - rho
                ct[t, 7] = (1 - rho) * mu
            else:
                Tm[7, tl - 1] += 1 - rho
        ct[t, 0] = mu
    Q = np.zeros((m, m))
    Q[0, 0] = sv * sv * t3v
    Q[4, 4] = sp * sp * t3v
    Q[6, 6] = sxi_o * sxi_o * t3v
    if rho and tl == 0:                  # tau* loads on the current value shock
        Q[7, 7] = (1 - rho) ** 2 * sv * sv * t3v
        Q[0, 7] = Q[7, 0] = (1 - rho) * sv * sv * t3v
    Z = np.zeros((4, m))
    Z[0, 5] = 1.0
    Z[0, 6] = 1.0
    Z[1, 0] = beta
    Z[1, 4] = 1.0
    if rho:
        Z[2, 7] = 1.0 - cc
    else:
        Z[2, tl] = 1.0 - cc
    if cc:
        Z[2, 5] += cc
        Z[2, 6] += cc
    Z[3, 0] = 1.0
    Hd = np.array([1e-8, sL * sL * t3v, st * st * t3v, SIG_Q ** 2 * t3v])
    y = np.zeros((Tn, 4))
    y[:, 0] = d["a"]
    y[:, 1] = d["L"]
    y[:, 2] = d["tau"]
    y[:, 3] = d["lnq"] + d["a"]
    mask = np.zeros((Tn, 4), dtype=np.bool_)
    mask[:, 0] = True
    if use_L:
        mask[:, 1] = True
    if use_tau:
        mask[::tau_every, 2] = True
    if use_bid:
        mask[:, 3] = d["bid_seen"]
    dt = np.zeros((Tn, 4))
    dt[:, 0] = d["strat_bias"]
    dt[:, 1] = cL
    dt[:, 2] = d["tau_bias"] + cc * d["strat_bias"]
    dt[:, 3] = -D_BID * d["prem"]
    a0v = d["a"][0]
    a0 = np.array([a0v, a0v, a0v, a0v, 0.0, a0v, 0.0, a0v])
    P0 = np.diag(np.array([0.05 ** 2] * 4 + [(sp ** 2) * t3v / max(1e-6, 1 - phip ** 2), 0.02 ** 2,
                                              (sxi_o ** 2) * t3v / (1 - phi_e ** 2), 0.05 ** 2]))
    return dict(y=y, mask=mask, Tt=Tt, ct=ct, Q=Q, Z=Z, dt=dt, Hd=Hd, a0=a0, P0=P0,
                bid_col=3 if use_bid else -1, diag_col=2)


# ------------------------------------------------------------------------------------------------------------
# 4. Metrics
# ------------------------------------------------------------------------------------------------------------
def crps_gauss(yv, m, s):
    zz = (yv - m) / s
    Phi = 0.5 * (1 + np.vectorize(math.erf)(zz / math.sqrt(2)))
    return s * (zz * (2 * Phi - 1) + 2 * np.exp(-0.5 * zz * zz) / math.sqrt(2 * math.pi) - 1 / math.sqrt(math.pi))


def nowcast_metrics(d: dict, v_hat: np.ndarray, P: np.ndarray, burn: int = 12, use_theta_from=None) -> dict:
    """Per-world sums for nowcast quality and the SELL rule (SELL iff q >= H_SELL * theta_hat)."""
    v = d["vbar"]
    a = d["a"]
    sl = slice(burn, len(v))
    err = v_hat[sl] - v[sl]
    sd = np.sqrt(np.maximum(P[sl], 1e-12))
    th_true = np.exp(v[sl] - a[sl])
    th_hat = np.exp(v_hat[sl] - a[sl])
    q = np.exp(d["lnq"][sl])
    sell_true = q >= H_SELL * th_true
    sell_hat = q >= H_SELL * th_hat
    regret = np.abs(q - H_SELL * th_true) * (sell_true != sell_hat)
    e4_hat = v_hat[sl][4:] - v_hat[sl][:-4]
    e4_true = v[sl][4:] - v[sl][:-4]
    return dict(n=int(err.size), sse=float((err ** 2).sum()), sse_appr=float(((a[sl] - v[sl]) ** 2).sum()),
                crps=float(crps_gauss(v[sl], v_hat[sl], sd).sum()), cov80=float((np.abs(err) <= Z80 * sd).sum()),
                n_sell=int(sell_true.sum()), sell_bias=float(((th_hat - th_true)[sell_true]).sum()),
                regret=float(regret.sum()), dec_err=int((sell_true != sell_hat).sum()),
                down_n=int((d["z"][sl] == 1).sum()), down_bias=float(err[d["z"][sl] == 1].sum()),
                e4_n=int(e4_hat.size), e4_sum=float((e4_hat - e4_true).sum()),
                e4_sse=float(((e4_hat - e4_true) ** 2).sum()), e4_xy=float((e4_hat * e4_true).sum()),
                e4_xx=float((e4_true ** 2).sum()), e4_yy=float((e4_hat ** 2).sum()),
                e4_x=float(e4_true.sum()), e4_y=float(e4_hat.sum()))


def summarize(rows: list) -> dict:
    """Aggregate per-world sums into rates (pp where natural)."""
    tot = {}
    for r in rows:
        for k, v in r.items():
            tot[k] = tot.get(k, 0.0) + v
    n = max(tot.get("n", 0), 1)
    out = dict(rmse_pp=100 * math.sqrt(tot["sse"] / n), rmse_appr_pp=100 * math.sqrt(tot["sse_appr"] / n),
               crps_pp=100 * tot["crps"] / n, cov80=tot["cov80"] / n,
               sell_bias_pp=100 * tot["sell_bias"] / max(tot["n_sell"], 1), regret_pp=100 * tot["regret"] / n,
               dec_err_rate=tot["dec_err"] / n,
               down_level_bias_pp=100 * tot["down_bias"] / max(tot["down_n"], 1))
    out["r2_ratio"] = out["rmse_pp"] / out["rmse_appr_pp"]
    ne = max(tot.get("e4_n", 0), 1)
    mx, my = tot["e4_x"] / ne, tot["e4_y"] / ne
    vx = tot["e4_xx"] / ne - mx * mx
    cxy = tot["e4_xy"] / ne - mx * my
    out["e4_bias_pp"] = 100 * tot["e4_sum"] / ne
    out["e4_rmse_pp"] = 100 * math.sqrt(tot["e4_sse"] / ne)
    out["e4_slope"] = cxy / vx if vx > 0 else float("nan")
    out["e4_true_sd_pp"] = 100 * math.sqrt(max(vx, 0.0))
    return out
