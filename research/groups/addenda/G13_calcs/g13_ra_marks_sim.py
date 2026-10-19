"""
G13 - Real Assets marks: synthetic ground truth, desmoothing, bias/credibility, recovery tests.

ALL SIMULATED OUTPUTS ARE SYNTHETIC - NOT ADIC DATA.
Section P (public-data illustrations) uses dated public figures quoted in the G13 dossier;
those are labelled PUBLIC-DATA ILLUSTRATION, not ADIC data and not synthetic.

Run (project venv, isolated):
    .venv/Scripts/python.exe -I -B g13_ra_marks_sim.py            # full run
    .venv/Scripts/python.exe -I -B g13_ra_marks_sim.py --quick    # smoke test

Outputs: g13_ra_marks_results.json (same folder).

Model summary (quarterly, log units). For segment s, asset i:
  true value      v_it = vbar_st + w_it,  vbar_st = n_st - x_st  (log NOI minus log cap-rate deviation)
  cap-rate factor x_st = phi_x x_s,t-1 + b_r dr_t + mu_x(z_t) + sig_x(z_t) e_st
  NOI             n_st = n_s,t-1 + (g + pass*(pi_t - pibar))/4 + beta_oil d(oil)_t + mu_n(z_t) + sig_n e_st
  idiosyncratic   w_it = w_i,t-1 + sig_i e_it
  appraisal (CGR-type AR smoothing with lag l):
      abar_st = (1 - lam_agg_t) vbar_s,t-l + lam_agg_t abar_s,t-1
      arel_it = (1 - lam_idio) w_i,t-l + lam_idio arel_i,t-1
      a_it    = abar_st + arel_it + e_it  (e redrawn at the asset's annual external appraisal, carried otherwise)
  listed proxy    L_st = beta_L vbar_s,t+k + p_st + sig_L e,  p_st = phi_p p_s,t-1 + sig_p e  (premium/discount)
  transaction idx tau_st = vbar_st + sig_tau e
  underwriting    u_i  = mu*_i,t0 + b_u + gamma_u 1{late cycle at t0} + eta_u
  group forecast  f_it = mu*_it + b_f + w_a (trailing appraisal return - mu*_it) + eta_f
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
from numpy.random import SeedSequence, default_rng
from scipy import optimize, stats

try:
    import numba as nb
    NUMBA = True
except Exception:  # noqa: BLE001
    NUMBA = False

SYN = "SYNTHETIC - NOT ADIC DATA"
OUT = Path(__file__).with_name("g13_ra_marks_results.json")

# ----------------------------------------------------------------------------------------------
# 0. Segment defaults (SYNTHETIC; [I] unless noted in the dossier). Rates are decimals per year
#    unless marked /q (per quarter). b_r = d(log cap rate) per 1.00 change in the real rate
#    (b_r = 12 means +100bp real rate -> +0.12 in log cap rate, i.e. 5.0% -> 5.6%).
# ----------------------------------------------------------------------------------------------
SEGMENTS = {
    "CORE_RE": dict(cbar=0.050, x0=-0.10, phi_x=0.95, b_r=12.0, sig_x=0.040, g=0.025, pass_pi=0.5,
                    sig_n=0.015, beta_oil=0.0, sig_i=0.040, lam_agg=0.75, lam_idio=0.35, lag=1,
                    sig_e=0.05, capex=0.10, beta_L=1.0, phi_p=0.85, sig_p=0.05, sig_L=0.01,
                    sig_tau=0.025, b_u=0.015, gamma_u=0.015, b_f=0.010, w_a=0.30, kappa=1.67),
    "VA_RE": dict(cbar=0.0575, x0=-0.10, phi_x=0.95, b_r=12.0, sig_x=0.050, g=0.030, pass_pi=0.4,
                  sig_n=0.025, beta_oil=0.0, sig_i=0.070, lam_agg=0.70, lam_idio=0.35, lag=1,
                  sig_e=0.07, capex=0.15, beta_L=1.0, phi_p=0.85, sig_p=0.05, sig_L=0.01,
                  sig_tau=0.030, b_u=0.040, gamma_u=0.015, b_f=0.025, w_a=0.30, kappa=2.00),
    "CORE_INFRA": dict(cbar=0.060, x0=-0.08, phi_x=0.96, b_r=10.0, sig_x=0.035, g=0.025, pass_pi=0.8,
                       sig_n=0.010, beta_oil=0.0, sig_i=0.030, lam_agg=0.85, lam_idio=0.50, lag=1,
                       sig_e=0.03, capex=0.05, beta_L=1.0, phi_p=0.88, sig_p=0.06, sig_L=0.01,
                       sig_tau=0.035, b_u=0.010, gamma_u=0.010, b_f=0.0075, w_a=0.30, kappa=1.67),
    "VA_INFRA": dict(cbar=0.065, x0=-0.08, phi_x=0.95, b_r=10.0, sig_x=0.050, g=0.040, pass_pi=0.6,
                     sig_n=0.030, beta_oil=0.0, sig_i=0.080, lam_agg=0.80, lam_idio=0.45, lag=1,
                     sig_e=0.05, capex=0.10, beta_L=1.0, phi_p=0.88, sig_p=0.06, sig_L=0.01,
                     sig_tau=0.040, b_u=0.030, gamma_u=0.010, b_f=0.020, w_a=0.30, kappa=2.00),
    "ENERGY": dict(cbar=0.100, x0=0.00, phi_x=0.93, b_r=6.0, sig_x=0.060, g=0.000, pass_pi=0.3,
                   sig_n=0.020, beta_oil=0.70, sig_i=0.100, lam_agg=0.50, lam_idio=0.30, lag=1,
                   sig_e=0.08, capex=0.20, beta_L=1.0, phi_p=0.80, sig_p=0.07, sig_L=0.02,
                   sig_tau=0.060, b_u=0.030, gamma_u=0.010, b_f=0.020, w_a=0.30, kappa=2.22),
    # AGRI_TIMBER: template only. The user excluded agriculture and timber from Real Assets (context 1A,
    # 2026-10-18); no test or census sleeve uses this segment.
    "AGRI_TIMBER": dict(cbar=0.040, x0=-0.05, phi_x=0.96, b_r=10.0, sig_x=0.030, g=0.025, pass_pi=0.7,
                        sig_n=0.020, beta_oil=0.0, sig_i=0.040, lam_agg=0.85, lam_idio=0.50, lag=2,
                        sig_e=0.05, capex=0.05, beta_L=0.6, phi_p=0.85, sig_p=0.06, sig_L=0.04,
                        sig_tau=0.060, b_u=0.010, gamma_u=0.010, b_f=0.010, w_a=0.30, kappa=1.67),
}

FACTORS = dict(rbar=0.015, phi_r=0.95, sig_r=0.0025, pibar=0.025, phi_pi=0.80, sig_pi=0.005,
               o0=math.log(75.0), phi_o=0.97, sig_o=0.16,
               p_nd=0.04, p_dn=0.15,          # regime switching per quarter: normal->down, down->normal
               mu_x_down=0.015, sigx_mult_down=1.5, mu_n_down=-0.005)


# ----------------------------------------------------------------------------------------------
# 1. Generator
# ----------------------------------------------------------------------------------------------
def sim_factors(rng, T, burn=40):
    F = FACTORS
    n = T + burn + 1
    r = np.empty(n); pi = np.empty(n); o = np.empty(n); z = np.zeros(n, dtype=np.int64)
    r[0], pi[0], o[0] = F["rbar"], F["pibar"], F["o0"]
    for t in range(1, n):
        r[t] = F["rbar"] + F["phi_r"] * (r[t - 1] - F["rbar"]) + F["sig_r"] * rng.standard_normal()
        pi[t] = F["pibar"] + F["phi_pi"] * (pi[t - 1] - F["pibar"]) + F["sig_pi"] * rng.standard_normal()
        o[t] = F["o0"] + F["phi_o"] * (o[t - 1] - F["o0"]) + F["sig_o"] * rng.standard_normal()
        u = rng.random()
        z[t] = (1 if u < F["p_nd"] else 0) if z[t - 1] == 0 else (0 if u < F["p_dn"] else 1)
    sl = slice(burn, n)
    return dict(r=r[sl], pi=pi[sl], o=o[sl], z=z[sl])


def sim_segment(rng, T, seg, Fz, n_assets, variant="M0", k_lead=0):
    """Return dict with true and observed series for one segment. Index 0..T (T+1 points)."""
    S = SEGMENTS[seg]
    F = FACTORS
    r, pi, o, z = Fz["r"], Fz["pi"], Fz["o"], Fz["z"]
    Tp = T + 1
    x = np.empty(Tp); nn = np.empty(Tp)
    x[0] = S["x0"]; nn[0] = 0.0
    for t in range(1, Tp):
        down = z[t] == 1
        sx = S["sig_x"] * (F["sigx_mult_down"] if down else 1.0)
        x[t] = (S["phi_x"] * x[t - 1] + S["b_r"] * (r[t] - r[t - 1])
                + (F["mu_x_down"] if down else 0.0) + sx * rng.standard_normal())
        nn[t] = (nn[t - 1] + (S["g"] + S["pass_pi"] * (pi[t] - F["pibar"])) / 4.0
                 + S["beta_oil"] * (o[t] - o[t - 1]) + (F["mu_n_down"] if down else 0.0)
                 + S["sig_n"] * rng.standard_normal())
    vbar = nn - x                                   # log value index (up to a constant)
    cap = S["cbar"] * np.exp(x)                     # annual cap rate
    yld = cap * (1.0 - S["capex"]) / 4.0            # quarterly cash yield
    # conditional expected next-quarter total log return (Campbell-Shiller style)
    mu_star = yld + S["g"] / 4.0 + (1.0 - S["phi_x"]) * x - 0.5 * (S["sig_x"] ** 2 + S["sig_n"] ** 2)

    # idiosyncratic
    w = np.zeros((n_assets, Tp))
    w[:, 1:] = np.cumsum(S["sig_i"] * rng.standard_normal((n_assets, T)), axis=1)

    # appraisal smoothing parameters by quarter
    lam_agg_t = np.full(Tp, S["lam_agg"])
    if variant in ("M_regime", "M_all"):
        lam_agg_t = np.where(z == 1, np.minimum(0.95, S["lam_agg"] + 0.10), lam_agg_t)
    if variant in ("M_season", "M_all"):
        q4 = (np.arange(Tp) % 4) == 3
        lam_agg_t = np.where(q4, np.maximum(0.05, lam_agg_t - 0.20), lam_agg_t)
    lam_i = S["lam_idio"]
    lag = S["lag"]

    abar = np.empty(Tp); arel = np.zeros((n_assets, Tp))
    abar[0] = vbar[0]
    for t in range(1, Tp):
        src = vbar[max(t - lag, 0)]
        abar[t] = (1 - lam_agg_t[t]) * src + lam_agg_t[t] * abar[t - 1]
        arel[:, t] = (1 - lam_i) * w[:, max(t - lag, 0)] + lam_i * arel[:, t - 1]
    # appraisal level noise: redrawn at each asset's annual external appraisal quarter
    appr_q = rng.integers(0, 4, size=n_assets)
    e = np.zeros((n_assets, Tp)); cur = S["sig_e"] * rng.standard_normal(n_assets)
    for t in range(Tp):
        redraw = (t % 4) == appr_q
        cur = np.where(redraw, S["sig_e"] * rng.standard_normal(n_assets), cur)
        e[:, t] = cur
    a_asset = abar[None, :] + arel + e
    a_index = a_asset.mean(axis=0)

    # listed proxy (unlevered), premium/discount AR(1)
    p = np.empty(Tp); p[0] = S["sig_p"] / math.sqrt(1 - S["phi_p"] ** 2) * rng.standard_normal()
    for t in range(1, Tp):
        p[t] = S["phi_p"] * p[t - 1] + S["sig_p"] * rng.standard_normal()
    vlead = np.concatenate([vbar[k_lead:], np.repeat(vbar[-1], k_lead)]) if k_lead > 0 else vbar
    L = S["beta_L"] * vlead + p + S["sig_L"] * rng.standard_normal(Tp)
    tau = vbar + S["sig_tau"] * rng.standard_normal(Tp)
    return dict(seg=seg, x=x, n=nn, vbar=vbar, cap=cap, yld=yld, mu_star=mu_star, w=w,
                v_asset=vbar[None, :] + w, abar=abar, a_asset=a_asset, a_index=a_index,
                lam_agg_t=lam_agg_t, p=p, L=L, tau=tau, z=z, Fz=Fz)


def cond_exp(d, seg, t, h):
    """Exact conditional expectation (given time-t state) of the h-quarter true total log return
    (capital + income, income approximated at E[x]) under the generator's linear dynamics and the
    two-state regime chain. Used as the 'true mu' that unbiased forecasts would report."""
    S = SEGMENTS[seg]; F = FACTORS; Fz = d["Fz"]
    r_t, pi_t, o_t, z_t = Fz["r"][t], Fz["pi"][t], Fz["o"][t], Fz["z"][t]
    P = np.array([[1 - F["p_nd"], F["p_nd"]], [F["p_dn"], 1 - F["p_dn"]]])
    prob = np.array([1.0, 0.0]) if z_t == 0 else np.array([0.0, 1.0])
    Ex = d["x"][t]; cap_ret = 0.0; inc = 0.0
    for k in range(1, h + 1):
        inc += S["cbar"] * math.exp(Ex) * (1 - S["capex"]) / 4.0
        prob = prob @ P
        pdn = prob[1]
        dr = (F["phi_r"] - 1) * F["phi_r"] ** (k - 1) * (r_t - F["rbar"])
        Ex_new = S["phi_x"] * Ex + S["b_r"] * dr + F["mu_x_down"] * pdn
        dn = ((S["g"] + S["pass_pi"] * F["phi_pi"] ** k * (pi_t - F["pibar"])) / 4.0
              + S["beta_oil"] * (F["phi_o"] - 1) * F["phi_o"] ** (k - 1) * (o_t - F["o0"])
              + F["mu_n_down"] * pdn)
        cap_ret += dn - (Ex_new - Ex)
        Ex = Ex_new
    return cap_ret + inc


# ----------------------------------------------------------------------------------------------
# 2. One-step (Geltner) and three-step (Couts-Goncalves-Rossi) AR desmoothing
# ----------------------------------------------------------------------------------------------
def ar1_ols(y):
    """OLS of y_t on [1, y_{t-1}] -> (const, phi, resid)."""
    Y = y[1:]; X = np.column_stack([np.ones(len(Y)), y[:-1]])
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    return b[0], b[1], Y - X @ b


def geltner_1step(ret):
    c, lam, _ = ar1_ols(ret)
    lam = min(max(lam, 0.0), 0.97)
    rv = (ret[1:] - lam * ret[:-1]) / (1 - lam)
    return lam, np.concatenate([[np.nan], rv])


def cgr_3step(R):
    """R: (N, T) observed asset returns. AR(1) version of CGR (2024) eq. (21)-(23)."""
    N, T = R.shape
    Rbar = R.mean(axis=0)
    Rrel = R - Rbar[None, :]
    eps = np.full((N, T), np.nan); phi0 = np.empty(N); pi0 = np.empty(N); mu = R.mean(axis=1)
    for j in range(N):
        Y = R[j, 1:]
        X = np.column_stack([np.ones(T - 1), Rrel[j, :-1], Rbar[:-1]])
        b, *_ = np.linalg.lstsq(X, Y, rcond=None)
        phi1 = min(max(b[1], 0.0), 0.97); pi1 = min(max(b[2], 0.0), 0.97)
        phi0[j] = 1 - phi1; pi0[j] = 1 - pi1
        eps[j, 1:] = Y - X @ b
    eps_bar = np.nanmean(eps, axis=0)
    pi0_bar = pi0.mean()
    eta = eps_bar / pi0_bar
    eta_rel = (eps - pi0[:, None] * eta[None, :]) / phi0[:, None]
    Rhat = mu.mean() + eta[None, :] + eta_rel + (mu - mu.mean())[:, None]
    return dict(Rhat=Rhat, phi1=1 - phi0, pi1=1 - pi0, agg=np.nanmean(Rhat, axis=0))


def acf1(x):
    x = x[~np.isnan(x)]
    x = x - x.mean()
    return float((x[1:] * x[:-1]).sum() / (x * x).sum())


# ----------------------------------------------------------------------------------------------
# 3. Kalman state-space desmoothing (segment index): the appraisal model in state-space form.
#    State (m=7): [v_t, v_t-1, v_t-2, v_t-3, p_t, s_t, e_t]
#      v_t = mu + v_t-1 + eta                (true log value, random walk with drift)
#      p_t = phi_p p_t-1 + zeta              (listed premium/discount to private value)
#      s_t = lam s_t-1 + (1-lam) v_t-l       (smoothed appraisal, Geltner/Quan-Quigley partial adjustment)
#      e_t = phi_e e_t-1 + xi                (appraisal-calendar noise; phi_e = 0.75 for annual cycles)
#    Obs: a_t = s_t + e_t (+tiny);  L_t - cL = beta v_t + p_t + eL;  tau_t = v_t + e_tau
# ----------------------------------------------------------------------------------------------
M_STATE = 7
PHI_E = 0.75


def _kf_core(y, mask, Tm, cvec, Q, Z, Hd, a0, P0, want_states):
    T = y.shape[0]
    m = Tm.shape[0]
    a = a0.copy(); P = P0.copy()
    ll = 0.0
    filt = np.zeros((T, m)); Pf = np.zeros((T, m + 1))
    for t in range(T):
        a = cvec + Tm @ a
        P = Tm @ P @ Tm.T + Q
        idx = np.where(mask[t])[0]
        k = idx.shape[0]
        if k > 0:
            Zo = np.zeros((k, m)); yo = np.zeros(k); Ho = np.zeros((k, k))
            for jj in range(k):
                Zo[jj, :] = Z[idx[jj], :]
                yo[jj] = y[t, idx[jj]]
                Ho[jj, jj] = Hd[idx[jj]]
            v = yo - Zo @ a
            Fm = Zo @ P @ Zo.T + Ho
            Lc = np.linalg.cholesky(Fm)
            Finv = np.linalg.inv(Fm)
            K = P @ Zo.T @ Finv
            a = a + K @ v
            P = P - K @ Zo @ P
            P = 0.5 * (P + P.T)
            logdet = 2.0 * np.sum(np.log(np.diag(Lc)))
            llt = -0.5 * (logdet + v @ Finv @ v + k * math.log(2 * math.pi))
            ll += llt
            Pf[t, m] = llt                      # per-period log-likelihood contribution (for sandwich SEs)
        if want_states:
            filt[t, :] = a
            for jj in range(m):
                Pf[t, jj] = P[jj, jj]
    return ll, filt, Pf


if NUMBA:
    _kf = nb.njit(cache=False)(_kf_core)
else:
    _kf = _kf_core

# parameter vector th (unconstrained) and bounds
TH_BOUNDS = [(-6, 6), (-5, 5), (-9, 0), (-12, -1), (0.2, 2.5), (-6, 6), (-9, -0.5), (-12, -1), (-9, -0.5), (-5, 5)]


def unpack(th, use_L, use_tau):
    lam = 0.98 / (1 + math.exp(-th[0]))
    mu = th[1] * 0.01
    sv = math.exp(th[2]); sxi = math.exp(th[3])
    beta = th[4] if use_L else 1.0
    phip = 0.99 / (1 + math.exp(-th[5])) if use_L else 0.0
    sp = math.exp(th[6]) if use_L else 1e-4
    sL = math.exp(th[7]) if use_L else 1.0
    st = math.exp(th[8]) if use_tau else 1.0
    cL = th[9] if use_L else 0.0
    return lam, mu, sv, sxi, beta, phip, sp, sL, st, cL


def ss_matrices(params, lag):
    lam, mu, sv, sxi, beta, phip, sp, sL, st, cL = params
    m = M_STATE
    Tm = np.zeros((m, m)); cvec = np.zeros(m); Rm = np.zeros((m, 3))
    Tm[0, 0] = 1.0; cvec[0] = mu; Rm[0, 0] = 1.0
    Tm[1, 0] = 1.0; Tm[2, 1] = 1.0; Tm[3, 2] = 1.0
    Tm[4, 4] = phip; Rm[4, 1] = 1.0
    Tm[5, 5] = lam
    if lag == 0:
        Tm[5, 0] += 1 - lam; cvec[5] = (1 - lam) * mu; Rm[5, 0] = 1 - lam
    else:
        Tm[5, lag - 1] += 1 - lam
    Tm[6, 6] = PHI_E; Rm[6, 2] = 1.0
    Qs = np.diag(np.array([sv * sv, sp * sp, sxi * sxi]))
    Q = Rm @ Qs @ Rm.T
    Z = np.zeros((3, m)); Z[0, 5] = 1.0; Z[0, 6] = 1.0; Z[1, 0] = beta; Z[1, 4] = 1.0; Z[2, 0] = 1.0
    Hd = np.array([1e-8, sL * sL, st * st])
    return Tm, cvec, Q, Z, Hd


def kf_build(a_idx, L, tau, use_L, use_tau, tau_every=1):
    T = len(a_idx)
    y = np.zeros((T, 3)); mask = np.zeros((T, 3), dtype=np.bool_)
    y[:, 0] = a_idx; y[:, 1] = L; y[:, 2] = tau
    mask[:, 0] = True
    if use_L:
        mask[:, 1] = True
    if use_tau:
        mask[::tau_every, 2] = True
    return y, mask


def kf_negll(th, y, mask, lag, use_L, use_tau, want=False):
    params = unpack(th, use_L, use_tau)
    lam, mu, sv, sxi, beta, phip, sp, sL, st, cL = params
    Tm, cvec, Q, Z, Hd = ss_matrices(params, lag)
    yy = y.copy()
    yy[:, 1] = yy[:, 1] - cL
    a0v = y[0, 0]
    a0 = np.array([a0v, a0v, a0v, a0v, 0.0, a0v, 0.0])
    P0 = np.diag(np.array([0.05 ** 2, 0.05 ** 2, 0.05 ** 2, 0.05 ** 2, (sp ** 2) / max(1e-6, 1 - phip ** 2),
                           0.02 ** 2, (sxi ** 2) / (1 - PHI_E ** 2)]))
    ll, filt, Pf = _kf(yy, mask, Tm, cvec, Q, Z, Hd, a0, P0, want)
    if want:
        return -ll, filt, Pf
    if not np.isfinite(ll):
        return 1e10
    return -ll


def kf_fit(a_idx, L, tau, lag, use_L=True, use_tau=True, hess=False, tau_every=1):
    y, mask = kf_build(a_idx, L, tau, use_L, use_tau, tau_every)
    ra = np.diff(a_idx)
    lam0 = min(max(acf1(ra), 0.10), 0.92)
    sv0 = max(np.std(ra) * math.sqrt((1 + lam0) / (1 - lam0)), 0.01)
    cL0 = float(np.mean(L - a_idx)) if use_L else 0.0
    th0 = np.array([math.log(lam0 / (0.98 - lam0)), np.mean(ra) / 0.01, math.log(sv0), math.log(0.005),
                    1.0, 1.5, math.log(0.05), math.log(0.01), math.log(0.03), cL0])
    th0 = np.array([min(max(v_, lo + 1e-6), hi - 1e-6) for v_, (lo, hi) in zip(th0, TH_BOUNDS)])
    f = lambda th: kf_negll(th, y, mask, lag, use_L, use_tau)
    best = None
    for start in (th0, np.clip(th0 + np.array([1.2, 0, 0.3, 0, 0, 0, 0, 0, 0, 0]), -5.9, 5.9),
                  np.clip(th0 + np.array([-1.0, 0, -0.2, 0, 0, 0, 0, 0, 0, 0]), -5.9, 5.9)):
        start = np.array([min(max(v_, lo + 1e-6), hi - 1e-6) for v_, (lo, hi) in zip(start, TH_BOUNDS)])
        res = optimize.minimize(f, start, method="L-BFGS-B", bounds=TH_BOUNDS)
        if best is None or res.fun < best.fun:
            best = res
    th = best.x
    out = dict(th=th, nll=float(best.fun), params=unpack(th, use_L, use_tau))
    if hess:
        out["lam_se"] = lam_se_numhess(f, th)
        out["lam_se_sandwich"] = lam_se_sandwich(f, th, y, mask, lag, use_L, use_tau)
    _, filt, Pf = kf_negll(th, y, mask, lag, use_L, use_tau, want=True)
    out["v_filt"] = filt[:, 0]; out["v_sd"] = np.sqrt(Pf[:, 0])
    return out


def lam_se_sandwich(f, th, y, mask, lag, use_L, use_tau, h=1e-3, nw_lags=4):
    """QMLE sandwich SE of lam: H^-1 J H^-1 with J from per-period scores (Newey-West, 4 lags).
    Parameters at a bound are held fixed (dropped) to avoid singular directions."""
    k = len(th)
    free = [i for i in range(k) if (TH_BOUNDS[i][0] + 1e-3 < th[i] < TH_BOUNDS[i][1] - 1e-3)]
    if not use_L:
        free = [i for i in free if i in (0, 1, 2, 3, 8)]
    if not use_tau:
        free = [i for i in free if i != 8]
    if 0 not in free:
        return float("nan")

    def llt(thv):
        _, _, Pf = kf_negll(thv, y, mask, lag, use_L, use_tau, want=True)
        return Pf[:, -1]
    nT = y.shape[0]
    S = np.zeros((nT, len(free)))
    for jj, i in enumerate(free):
        e = np.zeros(k); e[i] = h
        S[:, jj] = (llt(th + e) - llt(th - e)) / (2 * h)
    H = np.zeros((len(free), len(free)))
    for a_, i in enumerate(free):
        for b_, j in enumerate(free):
            if b_ < a_:
                continue
            ei = np.zeros(k); ej = np.zeros(k); ei[i] = h; ej[j] = h
            H[a_, b_] = H[b_, a_] = (f(th + ei + ej) - f(th + ei - ej) - f(th - ei + ej) + f(th - ei - ej)) / (4 * h * h)
    Sc = S - S.mean(axis=0)
    J = Sc.T @ Sc
    for L_ in range(1, nw_lags + 1):
        w = 1 - L_ / (nw_lags + 1)
        G = Sc[L_:].T @ Sc[:-L_]
        J += w * (G + G.T)
    try:
        Hi = np.linalg.pinv(H)
        V = Hi @ J @ Hi
        i0 = free.index(0)
        s = 0.98 / (1 + math.exp(-th[0]))
        dlam = s * (1 - s / 0.98)
        var = dlam * dlam * V[i0, i0]
        return float(math.sqrt(var)) if var > 0 else float("nan")
    except Exception:  # noqa: BLE001
        return float("nan")


def lam_se_numhess(f, th, h=1e-3):
    """Delta-method SE of lam from a numerical Hessian (profiled over all params)."""
    k = len(th)
    H = np.zeros((k, k))
    f0 = f(th)
    for i in range(k):
        for j in range(i, k):
            ei = np.zeros(k); ej = np.zeros(k); ei[i] = h; ej[j] = h
            fpp = f(th + ei + ej); fpm = f(th + ei - ej); fmp = f(th - ei + ej); fmm = f(th - ei - ej)
            H[i, j] = H[j, i] = (fpp - fpm - fmp + fmm) / (4 * h * h)
    try:
        cov = np.linalg.pinv(H)
        s = 0.98 / (1 + math.exp(-th[0]))
        dlam = s * (1 - s / 0.98)
        var = dlam * dlam * cov[0, 0]
        return float(math.sqrt(var)) if var > 0 else float("nan")
    except Exception:  # noqa: BLE001
        return float("nan")


# ----------------------------------------------------------------------------------------------
# 4. Test R1-R3: desmoothing recovery
# ----------------------------------------------------------------------------------------------
def test_desmoothing(worlds, kworlds, T, n_assets, seed, segs=("CORE_RE", "VA_RE", "CORE_INFRA"),
                     variants=("M0", "M_regime", "M_season", "M_all")):
    out = {}
    ss = SeedSequence(seed)
    for variant in variants:
        for seg in segs:
            S = SEGMENTS[seg]
            rows = dict(lam_g=[], lam_cgr_pi=[], ac1_obs_asset=[], ac1_obs_fund=[], ac1_obs_agg=[],
                        ac1_1step_agg=[], ac1_3step_agg=[], vol_ratio_obs=[], vol_ratio_1s=[], vol_ratio_3s=[],
                        fvol_ratio_obs=[], fvol_ratio_1s=[], fvol_ratio_3s=[], f_ac1_1s_agg=[], f_ac1_3s_agg=[],
                        beta_obs=[], beta_1s=[], beta_3s=[], beta_true=[],
                        fbeta_obs=[], fbeta_1s=[], fbeta_3s=[], fbeta_true=[])
            krows = dict(lam_A=[], lam_AL=[], lam_ALT=[], lam_ALT4=[], cover_ALT=[], rmse_appr=[], rmse_A=[],
                         rmse_AL=[], rmse_ALT=[], rmse_ALT4=[], cov80_AL=[], cov80_ALT=[], lag_sel_ok=[],
                         turn_err_appr=[], turn_err_AL=[], turn_err_ALT=[], beta_L_hat=[])
            child = ss.spawn(worlds)
            nf, fs = 10, n_assets // 10                 # 10 'funds' of n_assets/10 assets each
            for wi, cs in enumerate(child):
                rng = default_rng(cs)
                Fz = sim_factors(rng, T)
                d = sim_segment(rng, T, seg, Fz, n_assets, variant=variant)
                RA = np.diff(d["a_asset"], axis=1)          # observed asset capital returns
                RV = np.diff(d["v_asset"], axis=1)          # true asset capital returns
                FA = RA.reshape(nf, fs, -1).mean(axis=1)    # fund-level (equal-weighted blocks)
                FV = RV.reshape(nf, fs, -1).mean(axis=1)
                ra_idx = RA.mean(axis=0)
                rL = np.diff(d["L"])
                lam_g, rv1 = geltner_1step(ra_idx)
                rows["lam_g"].append(lam_g)
                rows["ac1_obs_asset"].append(float(np.mean([acf1(RA[j]) for j in range(n_assets)])))
                rows["ac1_obs_fund"].append(float(np.mean([acf1(FA[j]) for j in range(nf)])))
                rows["ac1_obs_agg"].append(acf1(ra_idx))
                R1 = np.array([geltner_1step(RA[j])[1] for j in range(n_assets)])
                rows["ac1_1step_agg"].append(acf1(np.nanmean(R1[:, 1:], axis=0)))
                c3 = cgr_3step(RA)
                rows["lam_cgr_pi"].append(float(np.mean(c3["pi1"])))
                rows["ac1_3step_agg"].append(acf1(c3["agg"][1:]))
                sd_true = np.std(RV, axis=1).mean()
                rows["vol_ratio_obs"].append(float(np.std(RA, axis=1).mean() / sd_true))
                rows["vol_ratio_1s"].append(float(np.nanstd(R1, axis=1).mean() / sd_true))
                rows["vol_ratio_3s"].append(float(np.nanstd(c3["Rhat"], axis=1).mean() / sd_true))
                # fund level
                F1 = np.array([geltner_1step(FA[j])[1] for j in range(nf)])
                f3 = cgr_3step(FA)
                fsd_true = np.std(FV, axis=1).mean()
                rows["fvol_ratio_obs"].append(float(np.std(FA, axis=1).mean() / fsd_true))
                rows["fvol_ratio_1s"].append(float(np.nanstd(F1, axis=1).mean() / fsd_true))
                rows["fvol_ratio_3s"].append(float(np.nanstd(f3["Rhat"], axis=1).mean() / fsd_true))
                rows["f_ac1_1s_agg"].append(acf1(np.nanmean(F1[:, 1:], axis=0)))
                rows["f_ac1_3s_agg"].append(acf1(f3["agg"][1:]))

                def avg_beta(Rm, nlag=2):
                    """Dimson beta: sum of slopes on listed returns at lags 0..nlag (de-lagging check)."""
                    bs = []
                    for j in range(Rm.shape[0]):
                        yv = Rm[j, nlag:]
                        X = np.column_stack([np.ones(len(yv))] + [rL[nlag - k: len(rL) - k] for k in range(nlag + 1)])
                        ok = ~np.isnan(yv)
                        b, *_ = np.linalg.lstsq(X[ok], yv[ok], rcond=None)
                        bs.append(b[1:].sum())
                    return float(np.mean(bs))
                rows["beta_obs"].append(avg_beta(RA)); rows["beta_1s"].append(avg_beta(R1))
                rows["beta_3s"].append(avg_beta(c3["Rhat"])); rows["beta_true"].append(avg_beta(RV))
                rows["fbeta_obs"].append(avg_beta(FA)); rows["fbeta_1s"].append(avg_beta(F1))
                rows["fbeta_3s"].append(avg_beta(f3["Rhat"])); rows["fbeta_true"].append(avg_beta(FV))

                if wi < kworlds:
                    a_idx = d["a_index"]; L = d["L"]; tau = d["tau"]; v = d["vbar"]
                    fA = kf_fit(a_idx, L, tau, S["lag"], use_L=False, use_tau=False)
                    fAL = kf_fit(a_idx, L, tau, S["lag"], use_L=True, use_tau=False)
                    fALT = kf_fit(a_idx, L, tau, S["lag"], use_L=True, use_tau=True, hess=True)
                    fALT4 = kf_fit(a_idx, L, tau, S["lag"], use_L=True, use_tau=True, tau_every=4)
                    krows["lam_A"].append(fA["params"][0]); krows["lam_AL"].append(fAL["params"][0])
                    krows["lam_ALT4"].append(fALT4["params"][0]); krows["beta_L_hat"].append(fAL["params"][4])
                    lam_hat = fALT["params"][0]; krows["lam_ALT"].append(lam_hat)
                    se = fALT.get("lam_se", float("nan"))
                    se_s = fALT.get("lam_se_sandwich", float("nan"))
                    lam_true = S["lam_agg"]
                    krows["cover_ALT"].append(bool(abs(lam_hat - lam_true) <= 1.645 * se) if np.isfinite(se) else False)
                    krows.setdefault("cover_ALT_sandwich", []).append(
                        bool(abs(lam_hat - lam_true) <= 1.645 * se_s) if np.isfinite(se_s) else False)
                    krows.setdefault("se_hess", []).append(se if np.isfinite(se) else np.nan)
                    krows.setdefault("se_sandwich", []).append(se_s if np.isfinite(se_s) else np.nan)
                    burn = 8
                    err_appr = (a_idx - v)[burn:]
                    rm = lambda fv: float(np.sqrt(np.mean((fv[burn:] - v[burn:]) ** 2)))
                    krows["rmse_appr"].append(float(np.sqrt(np.mean(err_appr ** 2))))
                    krows["rmse_A"].append(rm(fA["v_filt"])); krows["rmse_AL"].append(rm(fAL["v_filt"]))
                    krows["rmse_ALT"].append(rm(fALT["v_filt"])); krows["rmse_ALT4"].append(rm(fALT4["v_filt"]))
                    for nm, ff in (("cov80_AL", fAL), ("cov80_ALT", fALT)):
                        zsc = (v[burn:] - ff["v_filt"][burn:]) / ff["v_sd"][burn:]
                        krows[nm].append(float(np.mean(np.abs(zsc) <= 1.2816)))
                    dn = (d["z"][burn:] == 1)
                    if dn.sum() > 0:
                        krows["turn_err_appr"].append(float(np.mean((a_idx - v)[burn:][dn])))
                        krows["turn_err_AL"].append(float(np.mean((fAL["v_filt"] - v)[burn:][dn])))
                        krows["turn_err_ALT"].append(float(np.mean((fALT["v_filt"] - v)[burn:][dn])))
                    if variant == "M0":
                        nlls = [kf_fit(a_idx, L, tau, lg, True, True)["nll"] for lg in (0, 1, 2)]
                        krows["lag_sel_ok"].append(int(np.argmin(nlls)) == S["lag"])
            summ = {k: (float(np.mean(vv)), float(np.std(vv))) for k, vv in rows.items() if len(vv)}
            ksumm = {}
            for k, vv in krows.items():
                if len(vv) == 0:
                    continue
                arr = np.array(vv, dtype=float)
                ksumm[k] = (float(np.nanmean(arr)), float(np.nanstd(arr)))
            lam_true = S["lam_agg"]
            ksumm["lam_true"] = lam_true
            for k in ("lam_A", "lam_AL", "lam_ALT", "lam_ALT4"):
                if k in krows and len(krows[k]):
                    arr = np.array(krows[k])
                    ksumm[k + "_bias"] = float(arr.mean() - lam_true)
                    ksumm[k + "_rmse"] = float(np.sqrt(np.mean((arr - lam_true) ** 2)))
            out[f"{variant}|{seg}"] = dict(onestep_threestep=summ, kalman=ksumm, worlds=worlds,
                                           kworlds=min(kworlds, worlds), T=T, n_assets=n_assets,
                                           label=SYN)
            print(f"  desmooth {variant:9s} {seg:10s} lam_g={summ['lam_g'][0]:.3f} "
                  f"ac1 asset/fund/agg obs={summ['ac1_obs_asset'][0]:.2f}/{summ['ac1_obs_fund'][0]:.2f}/"
                  f"{summ['ac1_obs_agg'][0]:.2f} aggAC1 1s={summ['ac1_1step_agg'][0]:.2f} 3s={summ['ac1_3step_agg'][0]:.2f}"
                  f" | lam A/AL/ALT/ALT4={ksumm.get('lam_A', (np.nan,))[0]:.3f}/{ksumm.get('lam_AL', (np.nan,))[0]:.3f}/"
                  f"{ksumm.get('lam_ALT', (np.nan,))[0]:.3f}/{ksumm.get('lam_ALT4', (np.nan,))[0]:.3f} (true {lam_true})"
                  f" rmse appr/A/AL/ALT={ksumm.get('rmse_appr', (np.nan,))[0]:.3f}/{ksumm.get('rmse_A', (np.nan,))[0]:.3f}/"
                  f"{ksumm.get('rmse_AL', (np.nan,))[0]:.3f}/{ksumm.get('rmse_ALT', (np.nan,))[0]:.3f}"
                  f" beta 1s/3s/true={summ['beta_1s'][0]:.2f}/{summ['beta_3s'][0]:.2f}/{summ['beta_true'][0]:.2f}"
                  f" fbeta obs/1s/3s/true={summ['fbeta_obs'][0]:.2f}/{summ['fbeta_1s'][0]:.2f}/{summ['fbeta_3s'][0]:.2f}/"
                  f"{summ['fbeta_true'][0]:.2f}", flush=True)
    return out


# ----------------------------------------------------------------------------------------------
# 4b. Calibration check V-RA1: sale price vs appraisal two quarters earlier (Cannon-Cole style)
# ----------------------------------------------------------------------------------------------
def test_sales_vs_appraisal(worlds, T, seed, segs=("CORE_RE", "VA_RE", "CORE_INFRA"), n_assets=60,
                            h0=0.02, alpha_sel=1.0, sig_bid=0.04, forced_down=0.02):
    """Each quarter an asset sells with probability h0*exp(alpha_sel*(v - a)) (discretionary sellers sell
    when bids beat book) plus, in the down regime, forced sales at rate forced_down with no selection;
    price = exp(v + bid noise). Statistic: (S - A_{t-2})/A_{t-2}, as in Cannon & Cole (2011)."""
    ss = SeedSequence(seed + 23)
    out = {}
    for seg in segs:
        diffs, absd, dn_d, up_d, above, crash, boom = [], [], [], [], [], [], []
        for cs in ss.spawn(worlds):
            rng = default_rng(cs)
            Fz = sim_factors(rng, T)
            d = sim_segment(rng, T, seg, Fz, n_assets)
            v, a, z = d["v_asset"], d["a_asset"], d["z"]
            for t in range(10, T + 1):
                pr = np.minimum(0.5, h0 * np.exp(alpha_sel * (v[:, t] - a[:, t])) + (forced_down if z[t] == 1 else 0.0))
                sold = rng.random(n_assets) < pr
                if not sold.any():
                    continue
                S_ = np.exp(v[sold, t] + sig_bid * rng.standard_normal(sold.sum()))
                A2 = np.exp(a[sold, t - 2])
                dd = S_ / A2 - 1
                diffs.extend(dd.tolist()); absd.extend(np.abs(dd).tolist()); above.extend((S_ > np.exp(a[sold, t - 1])).tolist())
                (dn_d if z[t] == 1 else up_d).extend(dd.tolist())
                if d["vbar"][t] - d["vbar"][t - 4] < -0.08:          # 'crash' quarters: true index -8% over 4q
                    crash.extend(dd.tolist())
                if d["vbar"][t] - d["vbar"][t - 4] > 0.08:           # 'boom' quarters
                    boom.extend(dd.tolist())
        out[seg] = dict(n_sales=len(diffs), mean_signed=float(np.mean(diffs)), median_signed=float(np.median(diffs)),
                        mean_abs=float(np.mean(absd)), median_abs=float(np.median(absd)),
                        mean_signed_down_regime=float(np.mean(dn_d)) if dn_d else None,
                        mean_signed_normal_regime=float(np.mean(up_d)) if up_d else None,
                        mean_signed_crash_quarters=float(np.mean(crash)) if crash else None,
                        mean_signed_boom_quarters=float(np.mean(boom)) if boom else None,
                        share_sold_above_prior_mark=float(np.mean(above)), label=SYN,
                        targets="Cannon-Cole 1984-2010 NPI: mean abs 12.5% (median 8.1%); signed mean +4.9% "
                                "(median 2.8%); 2008 -12.0%, 2009 -8.9%")
        o = out[seg]
        print(f"  sales-vs-appraisal {seg}: n={o['n_sales']} mean signed={o['mean_signed']:.3f} mean abs={o['mean_abs']:.3f} "
              f"median abs={o['median_abs']:.3f} down={o['mean_signed_down_regime']} normal={o['mean_signed_normal_regime']} "
              f"above-mark={o['share_sold_above_prior_mark']:.2f}", flush=True)
    return out


# ----------------------------------------------------------------------------------------------
# 5. Test R4-R5: underwriting/forecast bias and overconfidence recovery
# ----------------------------------------------------------------------------------------------
def test_bias(worlds, T, n_assets, seed, segs=("CORE_RE", "VA_RE", "CORE_INFRA", "VA_INFRA"), h=8,
              n_years=8):
    """Forecasts filed annually over the last n_years; 8-quarter horizon; errors on true outcomes.
    Estimators: (a) naive mean, iid SE; (b) date-clustered SE; (c) common-shock control using the
    desmoothed (true-proxy) index vs the appraisal index."""
    ss = SeedSequence(seed + 7)
    res = {}
    for seg in segs:
        S = SEGMENTS[seg]
        acc = dict(bf_naive=[], bf_ctrl_true=[], bf_ctrl_appr=[], wa_hat=[], cover_naive=[], cover_clu=[],
                   bu_hat=[], bu_cover_clu=[], kappa_hat=[], pit_ks_p=[])
        for cs in ss.spawn(worlds):
            rng = default_rng(cs)
            Fz = sim_factors(rng, T)
            d = sim_segment(rng, T, seg, Fz, n_assets)
            v = d["v_asset"]; a = d["a_asset"]; yl = d["yld"]
            dates = [T - h - 4 * k for k in range(n_years)][::-1]
            E_f, E_u, X_anchor, D_id, Rtrue, IDX_true, IDX_appr, STATED_SD = [], [], [], [], [], [], [], []
            sig_true = None
            for di, t in enumerate(dates):
                # realized 8q total log return per asset, true
                R = (v[:, t + h] - v[:, t]) + yl[t:t + h].sum()
                mu_star = cond_exp(d, seg, t, h)     # conditional expectation (segment-level)
                trail_appr = (a[:, t] - a[:, t - 4]) * (h / 4.0) + yl[t - 4:t].sum() * (h / 4.0)
                anchor_gap = trail_appr - mu_star
                b_f = S["b_f"] * h / 4.0
                eta_f = rng.standard_normal(n_assets) * 0.02 * math.sqrt(h / 4.0)
                f = mu_star + b_f + S["w_a"] * anchor_gap + eta_f
                late = d["x"][t] < -0.05
                b_u = (S["b_u"] + S["gamma_u"] * late) * h / 4.0
                u = mu_star + b_u + rng.standard_normal(n_assets) * 0.03 * math.sqrt(h / 4.0)
                E_f.append(R - f); E_u.append(R - u); X_anchor.append(anchor_gap)
                D_id.append(np.full(n_assets, di)); Rtrue.append(R)
                IDX_true.append(np.full(n_assets, (d["vbar"][t + h] - d["vbar"][t]) + yl[t:t + h].sum() - mu_star))
                IDX_appr.append(np.full(n_assets, (d["abar"][t + h] - d["abar"][t]) + yl[t:t + h].sum() - mu_star))
                # stated 80% interval half-width = 1.2816 * sigma_true / kappa
                if sig_true is None:
                    sig_true = math.sqrt(h) * math.sqrt(S["sig_x"] ** 2 + S["sig_n"] ** 2 + S["sig_i"] ** 2)
                STATED_SD.append(np.full(n_assets, sig_true / S["kappa"]))
            E_f = np.concatenate(E_f); E_u = np.concatenate(E_u); X_anchor = np.concatenate(X_anchor)
            D_id = np.concatenate(D_id); IDX_true = np.concatenate(IDX_true); IDX_appr = np.concatenate(IDX_appr)
            STATED_SD = np.concatenate(STATED_SD)
            target_f = -S["b_f"] * h / 4.0
            # (a) naive: E[R - f] = -b_f - w_a * E[anchor_gap]; regress on [1, anchor_gap]
            X = np.column_stack([np.ones_like(E_f), X_anchor])
            bhat, *_ = np.linalg.lstsq(X, E_f, rcond=None)
            resid = E_f - X @ bhat
            XtX_inv = np.linalg.inv(X.T @ X)
            se_iid = math.sqrt(XtX_inv[0, 0] * resid.var(ddof=2))
            # cluster-robust by forecast date
            meat = np.zeros((2, 2))
            for g in np.unique(D_id):
                sel = D_id == g
                sg = X[sel].T @ resid[sel]
                meat += np.outer(sg, sg)
            V = XtX_inv @ meat @ XtX_inv
            se_clu = math.sqrt(V[0, 0])
            acc["bf_naive"].append(bhat[0]); acc["wa_hat"].append(-bhat[1])
            acc["cover_naive"].append(abs(bhat[0] - target_f) <= 1.645 * se_iid)
            acc["cover_clu"].append(abs(bhat[0] - target_f) <= 1.645 * se_clu)
            # (c) control for the common segment shock: true index vs appraisal index vs a nowcast-quality
            #     estimate of the true index (true + N(0, 3%) per date, i.e. Kalman-type nowcast error)
            Xc = np.column_stack([np.ones_like(E_f), X_anchor, IDX_true])
            bc, *_ = np.linalg.lstsq(Xc, E_f, rcond=None)
            Xa = np.column_stack([np.ones_like(E_f), X_anchor, IDX_appr])
            ba, *_ = np.linalg.lstsq(Xa, E_f, rcond=None)
            acc["bf_ctrl_true"].append(bc[0]); acc["bf_ctrl_appr"].append(ba[0])
            noise_by_date = {g_: rng.normal(0, 0.03) for g_ in np.unique(D_id)}
            IDX_hat = IDX_true + np.array([noise_by_date[g_] for g_ in D_id])
            Xh = np.column_stack([np.ones_like(E_f), X_anchor, IDX_hat])
            bh, *_ = np.linalg.lstsq(Xh, E_f, rcond=None)
            rh = E_f - Xh @ bh
            XtXh = np.linalg.inv(Xh.T @ Xh)
            meat_h = np.zeros((3, 3))
            for g_ in np.unique(D_id):
                sel = D_id == g_
                sg = Xh[sel].T @ rh[sel]
                meat_h += np.outer(sg, sg)
            Vh = XtXh @ meat_h @ XtXh
            G_ = len(np.unique(D_id))
            tcrit = stats.t.ppf(0.95, G_ - 1)          # small-cluster t critical value
            se_h = math.sqrt(Vh[0, 0] * G_ / (G_ - 1))
            acc.setdefault("bf_ctrl_hat", []).append(bh[0])
            acc.setdefault("wa_ctrl_hat", []).append(-bh[1])
            acc.setdefault("cover_ctrl_hat_clu_t", []).append(abs(bh[0] - target_f) <= tcrit * se_h)
            # underwriting bias (mean over all; includes late-cycle uplift)
            acc["bu_hat"].append(-float(np.mean(E_u)))
            # cluster SE for mean underwriting error
            gm = np.array([E_u[D_id == g].mean() for g in np.unique(D_id)])
            se_u = gm.std(ddof=1) / math.sqrt(len(gm))
            late_share = None
            acc["bu_cover_clu"].append(se_u)
            # kappa via coverage of stated 80% interval after removing estimated bias
            centered = E_f - X @ bhat
            cov = float(np.mean(np.abs(centered) <= 1.2816 * STATED_SD))
            cov = min(max(cov, 0.02), 0.98)
            kap = 1.2816 / stats.norm.ppf((1 + cov) / 2)
            acc["kappa_hat"].append(kap)
            # PIT of stated (unwidened) forecast: should be non-uniform when kappa > 1
            pit = stats.norm.cdf(centered / STATED_SD)
            acc["pit_ks_p"].append(stats.kstest(pit, "uniform").pvalue)
        tf = -S["b_f"] * 8 / 4.0
        res[seg] = dict(
            b_f_true_8q=S["b_f"] * 2, w_a_true=S["w_a"], kappa_true=S["kappa"],
            b_f_hat_naive=(-float(np.mean(acc["bf_naive"])), float(np.std(acc["bf_naive"]))),
            b_f_hat_ctrl_true=(-float(np.mean(acc["bf_ctrl_true"])), float(np.std(acc["bf_ctrl_true"]))),
            b_f_hat_ctrl_appr=(-float(np.mean(acc["bf_ctrl_appr"])), float(np.std(acc["bf_ctrl_appr"]))),
            w_a_hat=(float(np.mean(acc["wa_hat"])), float(np.std(acc["wa_hat"]))),
            b_f_hat_ctrl_nowcast=(-float(np.mean(acc["bf_ctrl_hat"])), float(np.std(acc["bf_ctrl_hat"]))),
            w_a_hat_ctrl_nowcast=(float(np.mean(acc["wa_ctrl_hat"])), float(np.std(acc["wa_ctrl_hat"]))),
            coverage90_ctrl_nowcast_clustered_t=float(np.mean(acc["cover_ctrl_hat_clu_t"])),
            b_f_hat_ctrl_appr_sd=float(np.std(acc["bf_ctrl_appr"])),
            coverage90_iid=float(np.mean(acc["cover_naive"])), coverage90_clustered=float(np.mean(acc["cover_clu"])),
            b_u_hat_8q=(float(np.mean(acc["bu_hat"])), float(np.std(acc["bu_hat"]))),
            kappa_hat=(float(np.mean(acc["kappa_hat"])), float(np.std(acc["kappa_hat"]))),
            pit_ks_reject_share=float(np.mean(np.array(acc["pit_ks_p"]) < 0.05)),
            worlds=worlds, n_assets=n_assets, n_dates=n_years, horizon_q=h, label=SYN)
        r = res[seg]
        print(f"  bias {seg:10s} b_f(8q) true={r['b_f_true_8q']:.3f} naive={r['b_f_hat_naive'][0]:.3f}"
              f"±{r['b_f_hat_naive'][1]:.3f} ctrl_true={r['b_f_hat_ctrl_true'][0]:.3f}±{r['b_f_hat_ctrl_true'][1]:.3f}"
              f" ctrl_appr={r['b_f_hat_ctrl_appr'][0]:.3f}  cov iid/clu={r['coverage90_iid']:.2f}/"
              f"{r['coverage90_clustered']:.2f} w_a={r['w_a_hat'][0]:.2f} kappa={r['kappa_hat'][0]:.2f}", flush=True)
    return res


# ----------------------------------------------------------------------------------------------
# 6. Test R6: scoring against appraisal returns rewards appraisal-mimicking forecasts
# ----------------------------------------------------------------------------------------------
def test_scoring(worlds, T, seed, seg="CORE_RE", h=4):
    ss = SeedSequence(seed + 11)
    S = SEGMENTS[seg]
    mse = dict(H_vs_appr=[], S_vs_appr=[], H_vs_true=[], S_vs_true=[], H_vs_tau=[], S_vs_tau=[])
    for cs in ss.spawn(worlds):
        rng = default_rng(cs)
        Fz = sim_factors(rng, T)
        d = sim_segment(rng, T, seg, Fz, 30)
        v, ab, tau, yl = d["vbar"], d["abar"], d["tau"], d["yld"]
        for t in range(12, T - h):
            honest = cond_exp(d, seg, t, h)       # forecast of true h-quarter return
            # appraisal-mimic: forecast = expected appraisal return given smoothing (persistence)
            lam = S["lam_agg"]
            last_ra = ab[t] - ab[t - 1]
            sl = sum(lam ** k for k in range(1, h + 1))
            inc_h = yl[t] * h
            mimic = sl * last_ra + (h - sl) * (honest - inc_h) / h + inc_h
            R_true = v[t + h] - v[t] + yl[t:t + h].sum()
            R_appr = ab[t + h] - ab[t] + yl[t:t + h].sum()
            R_tau = tau[t + h] - tau[t] + yl[t:t + h].sum()
            mse["H_vs_appr"].append((R_appr - honest) ** 2); mse["S_vs_appr"].append((R_appr - mimic) ** 2)
            mse["H_vs_true"].append((R_true - honest) ** 2); mse["S_vs_true"].append((R_true - mimic) ** 2)
            mse["H_vs_tau"].append((R_tau - honest) ** 2); mse["S_vs_tau"].append((R_tau - mimic) ** 2)
    out = {k: float(np.mean(vv)) for k, vv in mse.items()}
    out["winner_vs_appraisal"] = "mimic" if out["S_vs_appr"] < out["H_vs_appr"] else "honest"
    out["winner_vs_true"] = "mimic" if out["S_vs_true"] < out["H_vs_true"] else "honest"
    out["winner_vs_transaction_index"] = "mimic" if out["S_vs_tau"] < out["H_vs_tau"] else "honest"
    out["label"] = SYN
    print(f"  scoring {seg}: vs appraisal H={out['H_vs_appr']:.5f} S={out['S_vs_appr']:.5f} | vs true "
          f"H={out['H_vs_true']:.5f} S={out['S_vs_true']:.5f} | vs tau H={out['H_vs_tau']:.5f} S={out['S_vs_tau']:.5f}",
          flush=True)
    return out


# ----------------------------------------------------------------------------------------------
# 7. Test R7: fusion weights (equal / inverse-MSE / GLS / shrink-to-equal) out of sample
# ----------------------------------------------------------------------------------------------
def test_fusion(worlds, T, seed, seg="VA_RE", n_assets=40, h=8):
    ss = SeedSequence(seed + 13)
    S = SEGMENTS[seg]
    rowsM, rowsR = [], []
    for cs in ss.spawn(worlds):
        rng = default_rng(cs)
        Fz = sim_factors(rng, T)
        d = sim_segment(rng, T, seg, Fz, n_assets)
        v, a, yl, x = d["v_asset"], d["a_asset"], d["yld"], d["x"]
        for t in range(T - h - 28, T - h, 4):
            R = (v[:, t + h] - v[:, t]) + yl[t:t + h].sum()
            mu = cond_exp(d, seg, t, h)
            # m1: debiased underwriting with residual bias uncertainty and noise
            m1 = mu + rng.normal(0, 0.006) + rng.standard_normal(n_assets) * 0.035
            # m2: yield-based outside view using APPRAISAL cap rate (stale): NOI/A = cap * V/A
            capA = S["cbar"] * np.exp(x[t]) * np.exp(v[:, t] - a[:, t])
            m2 = (capA * (1 - S["capex"]) / 4 + S["g"] / 4) * h + rng.standard_normal(n_assets) * 0.01
            # m3: yield-based using market-implied cap rate (listed-implied, noisy)
            capM = S["cbar"] * np.exp(x[t] + rng.normal(0, 0.03))
            m3 = (capM * (1 - S["capex"]) / 4 + S["g"] / 4 + (1 - S["phi_x"]) * x[t]) * h + \
                rng.standard_normal(n_assets) * 0.01
            # m4: debiased group forecast (anchoring corrected imperfectly)
            m4 = mu + 0.10 * ((a[:, t] - a[:, t - 4]) * 2 - mu) + rng.standard_normal(n_assets) * 0.03
            rowsM.append(np.column_stack([m1, m2, m3, m4])); rowsR.append(R)
    M = np.vstack(rowsM); R = np.concatenate(rowsR)
    n = len(R); half = n // 2
    Mtr, Rtr, Mte, Rte = M[:half], R[:half], M[half:], R[half:]
    E = Rtr[:, None] - Mtr
    bias = E.mean(axis=0)
    Ec = E - bias
    Sig = np.cov(Ec.T)
    K = M.shape[1]
    one = np.ones(K)
    w_eq = one / K
    w_imse = (1 / np.diag(Sig)) / (1 / np.diag(Sig)).sum()
    Si = np.linalg.inv(Sig)
    w_gls = Si @ one / (one @ Si @ one)
    # constrained GLS (w >= 0, sum 1) via NNLS-like projection
    cons = ({"type": "eq", "fun": lambda w: w.sum() - 1},)
    rr = optimize.minimize(lambda w: w @ Sig @ w, w_eq, bounds=[(0, 1)] * K, constraints=cons)
    w_cgls = rr.x
    w_shr = 0.5 * w_cgls + 0.5 * w_eq

    def evaluate(w, small_n=None):
        pred = (Mte + bias) @ w
        err = Rte - pred
        sd = math.sqrt(max(w @ Sig @ w, 1e-8))
        z = err / sd
        crps = sd * (z * (2 * stats.norm.cdf(z) - 1) + 2 * stats.norm.pdf(z) - 1 / math.sqrt(math.pi))
        cov80 = float(np.mean(np.abs(z) <= 1.2816))
        return dict(mse=float(np.mean(err ** 2)), crps=float(np.mean(crps)), cov80=cov80, w=[float(q) for q in w])

    out = dict(equal=evaluate(w_eq), inv_mse=evaluate(w_imse), gls=evaluate(w_gls), cgls=evaluate(w_cgls),
               shrink50=evaluate(w_shr))
    # small-sample instability: estimate weights on 40 forecast-outcome pairs, 500 resamples
    rngb = default_rng(seed + 99)
    small = dict(equal=[], gls=[], cgls=[], shrink50=[])
    for _ in range(300):
        idx = rngb.choice(half, size=40, replace=False)
        Es = Rtr[idx, None] - Mtr[idx]
        bs = Es.mean(axis=0)
        Ss = np.cov((Es - bs).T) + 1e-6 * np.eye(K)
        Sis = np.linalg.inv(Ss)
        wg = Sis @ one / (one @ Sis @ one)
        rr = optimize.minimize(lambda w: w @ Ss @ w, w_eq, bounds=[(0, 1)] * K, constraints=cons)
        wc = rr.x
        for name, w in (("equal", w_eq), ("gls", wg), ("cgls", wc), ("shrink50", 0.5 * wc + 0.5 * w_eq)):
            pred = (Mte + bs) @ w
            small[name].append(float(np.mean((Rte - pred) ** 2)))
    out["small_n40_mse"] = {k: (float(np.mean(vv)), float(np.percentile(vv, 90))) for k, vv in small.items()}
    out["marks"] = ["m1 debiased underwriting", "m2 yield view on appraisal cap rate",
                    "m3 yield view on market-implied cap rate", "m4 debiased group forecast"]
    out["label"] = SYN
    print("  fusion " + seg + ": " + ", ".join(f"{k} mse={v['mse']:.5f} crps={v['crps']:.4f} cov80={v['cov80']:.2f}"
                                             for k, v in out.items() if isinstance(v, dict) and "mse" in v), flush=True)
    print("  fusion small-n (n=40) mean/P90 mse: " + ", ".join(f"{k}={v[0]:.5f}/{v[1]:.5f}"
                                                         for k, v in out["small_n40_mse"].items()), flush=True)
    return out


# ----------------------------------------------------------------------------------------------
# 8. Test R8: closed-end real-asset fund ultimates (prior / reported TVPI / economic TVPI / BF / Benktander)
# ----------------------------------------------------------------------------------------------
def test_bf(worlds, seed, seg="VA_RE", n_funds=12, M=8, T_life=48):
    ss = SeedSequence(seed + 17)
    S = SEGMENTS[seg]
    ages = [8, 12, 16, 20, 24, 28, 32]
    keys = ("prior", "prior_biased", "tvpi_rep", "tvpi_econ", "bf_paid", "gb_paid", "gb_incurred_econ",
            "gb_incurred_econ_biasedprior")
    errs = {k: {a: [] for a in ages} for k in keys}
    errs_dn = {k: {a: [] for a in ages} for k in keys}     # dates in the down regime
    p_dev_curve = None
    for cs in ss.spawn(worlds):
        rng = default_rng(cs)
        Tw = T_life + 40
        Fz = sim_factors(rng, Tw)
        d = sim_segment(rng, Tw, seg, Fz, n_funds * M)
        v, a, yl = d["v_asset"], d["a_asset"], d["yld"]
        # vintages spread over the world; each fund invests in M assets in quarters 0..11 of its life
        DPI_paths, NAVr_paths, NAVe_paths, ULT, T0 = [], [], [], [], []
        for f in range(n_funds):
            t0 = int(rng.integers(4, Tw - T_life - 1))
            T0.append(t0)
            dist = np.zeros(T_life + 1); navr = np.zeros(T_life + 1); nave = np.zeros(T_life + 1)
            paid_in = 0.0
            for k in range(M):
                i = f * M + k
                ta = t0 + int(rng.integers(0, 8))
                hold = int(rng.integers(16, 29))
                te = min(ta + hold, t0 + T_life)
                entry = math.exp(v[i, ta])
                paid_in += entry
                units = 1.0 / entry
                for t in range(ta, t0 + T_life + 1):
                    age = t - t0
                    if t < te:
                        dist[age] += units * math.exp(v[i, t]) * yl[t] * 0.8
                        navr[age] += units * math.exp(a[i, t] - (a[i, ta] - v[i, ta]))  # appraisal starts at cost
                        nave[age] += units * math.exp(v[i, t])
                    elif t == te:
                        dist[age] += units * math.exp(v[i, t]) * (1 - 0.02)
                        break
            # per $ paid in (M units of 1$ each)
            dist /= M; navr /= M; nave /= M
            cum = np.cumsum(dist)
            DPI_paths.append(cum); NAVr_paths.append(navr); NAVe_paths.append(nave)
            ULT.append(cum[-1])
        DPI = np.array(DPI_paths); NAVr = np.array(NAVr_paths); NAVe = np.array(NAVe_paths); ULT = np.array(ULT)
        # development pattern p(age) = E[DPI_age]/E[ULT] estimated from THIS world's other funds (leave-one-out)
        U0_mean_true = ULT.mean()
        TVr = DPI + NAVr; TVe = DPI + NAVe
        for f in range(n_funds):
            others = [g for g in range(n_funds) if g != f]
            p_dev = DPI[others].mean(axis=0) / ULT[others].mean()          # paid development pattern
            ldf_rep = ULT[others].mean() / np.maximum(TVr[others].mean(axis=0), 1e-9)   # incurred LDFs
            ldf_eco = ULT[others].mean() / np.maximum(TVe[others].mean(axis=0), 1e-9)
            U0 = math.exp(math.log(np.mean(ULT[others])) + rng.normal(0, 0.10))   # outside-view prior with noise
            for age in ages:
                p = min(max(p_dev[age], 1e-3), 0.999)
                dpi = DPI[f, age]
                tv_rep = (dpi + NAVr[f, age]) * ldf_rep[age]                    # chain-ladder on reported TVPI
                # economic NAV: Kalman-type adjustment, imperfect: theta_hat = exp(v-a) with 4% error
                theta_true = NAVe[f, age] / NAVr[f, age] if NAVr[f, age] > 0 else 1.0
                theta_hat = theta_true * math.exp(rng.normal(0, 0.04))
                tv_eco = (dpi + NAVr[f, age] * theta_hat) * ldf_eco[age]         # chain-ladder on economic TVPI
                bf = dpi + (1 - p) * U0
                gb = dpi + (1 - p) * bf
                p_inc = min(max(1.0 / ldf_eco[age], 1e-3), 0.999)
                c_star = 1 - (1 - p_inc) ** 2                                   # Benktander weight, incurred
                gb_inc = c_star * tv_eco + (1 - c_star) * U0
                # frozen underwriting prior NOT debiased: b_u per year over a 5-year plan
                U0b = U0 * math.exp(S["b_u"] * 5.0)
                gb_inc_b = c_star * tv_eco + (1 - c_star) * U0b
                tr = ULT[f]
                down = d["z"][T0[f] + age] == 1
                for k2, val in (("prior", U0), ("prior_biased", U0b), ("tvpi_rep", tv_rep), ("tvpi_econ", tv_eco),
                                ("bf_paid", bf), ("gb_paid", gb), ("gb_incurred_econ", gb_inc),
                                ("gb_incurred_econ_biasedprior", gb_inc_b)):
                    e_ = math.log(max(val, 1e-6) / tr)
                    errs[k2][age].append(e_)
                    if down:
                        errs_dn[k2][age].append(e_)
            if p_dev_curve is None:
                p_dev_curve = [float(p_dev[a_]) for a_ in ages]
    out = {k: {str(a_): dict(bias=float(np.mean(vv[a_])), rmse=float(np.sqrt(np.mean(np.square(vv[a_])))))
               for a_ in ages} for k, vv in errs.items()}
    out["down_regime_dates"] = {k: {str(a_): dict(n=len(vv[a_]), bias=float(np.mean(vv[a_])) if vv[a_] else None,
                                                 rmse=float(np.sqrt(np.mean(np.square(vv[a_])))) if vv[a_] else None)
                                    for a_ in ages} for k, vv in errs_dn.items()}
    out["p_dev_example"] = dict(zip([str(a_) for a_ in ages], p_dev_curve))
    out["label"] = SYN
    best = {str(a_): min(errs.keys(), key=lambda k: np.sqrt(np.mean(np.square(errs[k][a_])))) for a_ in ages}
    out["best_by_age_q"] = best
    print("  BF/Benktander best estimator by age (quarters): " + str(best), flush=True)
    for k in errs:
        print(f"    {k:18s} " + " ".join(f"{a_}:{out[k][str(a_)]['rmse']:.3f}" for a_ in ages), flush=True)
    return out


# ----------------------------------------------------------------------------------------------
# 9. Test R9: open-end fund with stale NAV - wealth transfer under no queue / queue / queue+buffer
# ----------------------------------------------------------------------------------------------
def test_openend(worlds, T, seed, seg="CORE_RE"):
    """Investor redemption requests respond to lagged listed returns (Couts 2025 direction).
    Fund pays redemptions at appraisal NAV (stale); assets sold at true value to fund outflows beyond
    cash. Wealth transfer to redeemers = sum over t of paid_t * (NAV_t/V_t - 1) per unit of fund value."""
    ss = SeedSequence(seed + 19)
    S = SEGMENTS[seg]
    results = {}
    worlds_list = ss.spawn(worlds)
    for regime in ("no_queue", "queue_2pct", "queue_2pct_buffer5"):
        transfers, max_queue = [], []
        for cs in worlds_list:                                   # common random numbers across regimes
            rng = default_rng(cs)
            Fz = sim_factors(rng, T)
            d = sim_segment(rng, T, seg, Fz, 30)
            v, ab, Lr = d["vbar"], d["abar"], np.diff(d["L"])
            V = 1.0; queue = 0.0; cash = 0.05 if regime.endswith("buffer5") else 0.0
            transfer = 0.0; mq = 0.0
            for t in range(5, T):
                nav_ratio = math.exp(ab[t] - v[t])               # NAV / true value
                # redemption request (share of fund) responds to last 4q listed return
                lr4 = Lr[t - 4:t].sum()
                req = max(0.0, 0.008 - 0.12 * lr4) + 0.002 * rng.standard_normal() ** 2
                queue += req
                if regime == "no_queue":
                    paid = queue
                else:
                    cap = 0.02 + (cash if regime.endswith("buffer5") else 0.0)
                    paid = min(queue, cap)
                    if regime.endswith("buffer5"):
                        use_cash = min(cash, paid)
                        cash -= use_cash
                        cash = min(0.05, cash + 0.005)           # rebuild buffer slowly
                queue -= paid
                mq = max(mq, queue)
                transfer += paid * (nav_ratio - 1.0)             # gain to redeemers per unit of fund value
            transfers.append(transfer); max_queue.append(mq)
        yrs = (T - 5) / 4.0
        results[regime] = dict(mean_transfer_pct_of_fund_cum=float(100 * np.mean(transfers)),
                               mean_transfer_bp_per_year=float(1e4 * np.mean(transfers) / yrs),
                               p95_abs_transfer_pct_cum=float(100 * np.percentile(np.abs(transfers), 95)),
                               mean_max_queue_pct=float(100 * np.mean(max_queue)),
                               p90_max_queue_pct=float(100 * np.percentile(max_queue, 90)))
    results["label"] = SYN
    print("  open-end: " + str(results), flush=True)
    return results


# ----------------------------------------------------------------------------------------------
# P. Public-data illustrations (NOT synthetic; dated public figures cited in the dossier)
# ----------------------------------------------------------------------------------------------
def public_illustrations():
    out = {"label": "PUBLIC-DATA ILLUSTRATION (not ADIC data; figures as cited in G13 dossier)"}
    # P1. HICL (annual report 2026): NAV 160.2p; discount 24% at 31 Mar 2026; +/-0.5% DR -> -6.8p/+7.4p
    nav = 160.2; disc = 0.24; dr = 0.085
    price = nav * (1 - disc)
    gap = nav - price
    # local linear sensitivity per +1% DR (use the downside leg, 2 x 6.8p) and a convex variant
    sens_up_1pct = 2 * 6.8
    ddr_lin = gap / sens_up_1pct
    # convexity: fit NAV(dr) = A * (dr)^(-D) through (dr, nav) and (dr+0.005, nav-6.8)
    D = math.log(nav / (nav - 6.8)) / math.log((dr + 0.005) / dr)
    ddr_cvx = dr * ((nav / price) ** (1 / D)) - dr
    out["P1_HICL_implied_discount_rate"] = dict(nav_p=nav, discount=disc, appraisal_dr=dr,
                                                implied_dr_linear=dr + ddr_lin / 100.0, implied_dr_convex=dr + ddr_cvx,
                                                note="upper bound: the share discount also prices fees, gearing, "
                                                     "governance and sentiment, not only NAV staleness")
    # P2. Jefferies H1 2026 LP pricing: RE 68%, infrastructure 91%. theta = p * ((1+yP)/(1+yV))^D
    rows = {}
    for name, p, yP, yV, D_ in (("real_estate", 0.68, 0.14, 0.09, 3.0), ("real_estate_lowprem", 0.68, 0.12, 0.09, 3.0),
                                ("infrastructure", 0.91, 0.14, 0.10, 3.5), ("infrastructure_lowprem", 0.91, 0.13, 0.11, 3.5)):
        theta = p * ((1 + yP) / (1 + yV)) ** D_
        rows[name] = dict(price_pct_nav=p, buyer_target=yP, fund_expected=yV, duration=D_,
                          implied_econ_to_reported_nav=round(theta, 3))
    out["P2_secondary_implied_theta"] = rows
    # P3. NFI-ODCE vs FTSE Nareit All Equity REITs (calendar years). ODCE quarterly gross total returns read
    # from the NCREIF Q2-2026 webinar chart (2022Q1..2026Q2); REIT annual from Nareit fact sheets
    # (2022 -24.95%, 2025 +2.27%); 2023 +11.4% and 2024 +4.9% are secondary-source values.
    odce_q = [7.4, 4.8, 0.5, -5.0, -3.2, -2.7, -1.9, -4.8, -2.4, -0.4, 0.2, 1.2, 1.1, 1.0, 0.7, 0.9, 1.25, 1.49]
    yrs = {}
    for k, y in enumerate((2022, 2023, 2024, 2025)):
        q = odce_q[4 * k:4 * k + 4]
        yrs[y] = round(100 * (np.prod([1 + x / 100 for x in q]) - 1), 1)
    reit = {2022: -24.95, 2023: 11.4, 2024: 4.9, 2025: 2.27}
    # ODCE drawdown from 2022Q3 level to trough
    lvl = np.cumprod([1 + x / 100 for x in odce_q])
    peak_i = int(np.argmax(lvl[:4])); trough_i = int(np.argmin(lvl))
    dd = lvl[trough_i] / lvl[peak_i] - 1
    out["P3_ODCE_vs_REIT"] = dict(odce_calendar=yrs, reit_calendar=reit,
                                  odce_peak_quarter_index=peak_i, odce_trough_quarter_index=trough_i,
                                  odce_peak_to_trough_total_return=round(100 * dd, 1),
                                  quarters_peak_to_trough=trough_i - peak_i,
                                  note="ODCE is gross, levered (27.1% leverage at 2Q26); REITs levered and listed")
    # P4. BREIT 2022 illustration: NAV +8.5% YTD Oct-2022 vs similar public REITs ~-30% (FA magazine, 6 Dec 2022).
    # If true private value fell by half the REIT move after unlevering, NAV overstatement and transfer per 2% redemption:
    nav_ret = 0.085; reit_ret = -0.30; ltv_reit = 0.35
    unlev = reit_ret * (1 - ltv_reit)
    for share in (0.5, 1.0):
        true_ret = share * unlev
        over = (1 + nav_ret) / (1 + true_ret) - 1
        out[f"P4_stale_nav_illustration_share{share}"] = dict(assumed_true_return=round(true_ret, 3),
                                                             nav_overstatement=round(over, 3),
                                                             transfer_per_2pct_monthly_redemption_pct_nav=round(100 * 0.02 * over, 2),
                                                             note="illustrative only; BREIT's true NAV is contested")
    return out


# ----------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", type=int, default=200)
    ap.add_argument("--kworlds", type=int, default=60)
    ap.add_argument("--T", type=int, default=80)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--seed", type=int, default=20261018)
    args = ap.parse_args()
    if args.quick:
        args.worlds, args.kworlds = 12, 4
    t0 = time.time()
    res = dict(label=SYN, run=dict(worlds=args.worlds, kworlds=args.kworlds, T=args.T, seed=args.seed,
                                   numba=NUMBA, generated=time.strftime("%Y-%m-%d %H:%M:%S")),
               segments=SEGMENTS, factors=FACTORS)
    print("R1-R3 desmoothing ...", flush=True)
    res["desmoothing"] = test_desmoothing(args.worlds, args.kworlds, args.T, 60, args.seed)
    print("V-RA1 sales vs appraisal ...", flush=True)
    res["sales_vs_appraisal"] = test_sales_vs_appraisal(max(20, args.worlds // 2), args.T, args.seed)
    print("R4-R5 bias/kappa ...", flush=True)
    res["bias"] = test_bias(args.worlds, args.T, 40, args.seed)
    print("R6 scoring ...", flush=True)
    res["scoring"] = test_scoring(max(20, args.worlds // 4), args.T, args.seed)
    print("R7 fusion ...", flush=True)
    res["fusion"] = test_fusion(max(20, args.worlds // 2), args.T, args.seed)
    print("R8 BF/Benktander ...", flush=True)
    res["bf_benktander"] = test_bf(max(20, args.worlds // 2), args.seed)
    print("R9 open-end ...", flush=True)
    res["openend"] = test_openend(max(20, args.worlds), args.T, args.seed)
    print("P public illustrations ...", flush=True)
    res["public"] = public_illustrations()
    print(json.dumps(res["public"], indent=1))
    res["run"]["seconds"] = round(time.time() - t0, 1)

    def conv(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    OUT.write_text(json.dumps(res, indent=1, default=conv), encoding="utf-8")
    print(f"wrote {OUT} in {res['run']['seconds']}s  [{SYN}]")


if __name__ == "__main__":
    main()
