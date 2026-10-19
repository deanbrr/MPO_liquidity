"""
RA gap 02 - external-target gates for the Real Assets engine (replace V-RA-CF).

Public data in, synthetic engine out. Each gate states its target, source, tolerance and what was fitted.

  G-ODCE   Historical replay 2021Q4-2026Q2 of the engine's RE property layer (re_market, unchanged) on FRED factors
           (10y, Baa-10y, CPI y/y, real-GDP growth gap, SLOOS -> f). ODCE-like mix at 25% leverage, debt cost 4.5%.
           Targets: appraisal-based levered total-return drawdown -18.8% (NCREIF ODCE, 2022Q3-2024Q2; tolerance
           +/-3pp); true (unsmoothed) levered drawdown -25.7% (FTSE Nareit All Equity REITs relevered to 25%,
           2021Q4-2023Q3; +/-5pp, the V-RE3 tolerance); trough lag 3 quarters (+/-1).
           Cross-check: unlevered true value change Mar-2022 -> Dec-2023 vs Green Street CPPI -22% all-property.
           Fitted: ONE office demand shock (log market rent, 2022Q1-2023Q4) to Green Street office -35%.
  G-JIANG  CMBS-replica population outstanding in 2023Q4 (Jiang, Matvos, Piskorski & Seru, NBER w31970: 35,253 loans,
           $825bn; initial LTV 61.0% all / 54.4% office; current LTV 66.2% / 86.0%; LTV>80% 29.0% / 56.0%;
           LTV>100% 14.3% / 44.6%). Property values indexed from origination by the engine's own replayed sector
           paths 2013Q1-2023Q4 plus asset idiosyncratic dispersion SIG_ID_RE; origination-LTV dispersion is a tape
           parameter. Tolerances: shares +/-4pp; mean current LTV +/-4pp.
  G-CHEN   Mechanism test of decide_maturity (the engine's s4.5 rule) on a CMBS-like maturing population with
           quarter fixed effects: LPM slope of 1(refinance | transaction) on the rate gap. Target -0.111 (SE 0.019;
           Chen & Chen 2025, Table 9, full sample, 2003Q1-2019Q2, MSCI RCA) - pass inside the 95% CI [-0.148, -0.074].
           Held-out check: matched-sample -0.128 (SE 0.024).
Run:  .venv\\Scripts\\python.exe -B ra_gates.py
"""
from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy.optimize import brentq

import ra_common as C
import ra_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ra_gates_results.json")


class ZeroRNG:
    """Deterministic replay: the property layer's shocks are switched off."""
    def standard_normal(self, size):
        return np.zeros(size)

    def random(self, size):
        return np.full(size, 0.5)


def panel_slice(q0, q1):
    P = {r["quarter"]: r for r in C.load_panel()}
    qs = sorted(q for q in P if q0 <= q <= q1)
    return qs, P


def hist_F(q0, q1, office_shock=None):
    qs, P = panel_slice(q0, q1)
    y = np.array([[P[q]["y10"] for q in qs]])
    s = np.array([[P[q]["baa10y"] for q in qs]])
    pi = np.array([[P[q]["cpi_yoy"] for q in qs]])
    g = np.array([[P[q]["gdp_yoy"] - 2.0 if isinstance(P[q].get("gdp_yoy"), float) else 0.0 for q in qs]])
    L = np.array([[P[q]["sloos"] if isinstance(P[q].get("sloos"), float) else 0.0 for q in qs]])
    f = C.f_of_L(L)
    z = np.zeros_like(f)
    F = dict(y=y, s=s, pi=pi, g=g, f=f, fGCC=f, z=z)
    if office_shock is not None:
        F["office_shock"] = office_shock
    return qs, F


ODCE_MIX = {"LOG": 0.33, "RES": 0.31, "OFF": 0.185, "RET": 0.105, "ALT": 0.07}   # G10 OE fund mixes (average) [I]


def replay(q0, q1, shock_q=None, shock_size=0.0, sectors=("LOG", "RES", "OFF", "RET", "ALT", "HOT", "DC")):
    qs, F0 = hist_F(q0, q1)
    T_ = len(qs) - 1
    shock = np.zeros(T_)
    if shock_q is not None:
        for i, q in enumerate(qs[1:]):
            if shock_q[0] <= q <= shock_q[1]:
                shock[i] = shock_size
    F0["office_shock"] = shock
    out = {}
    for k in sectors:
        m = E.re_market(k, "US", F0, ZeroRNG(), 1, T_=T_)
        out[k] = {"V": m["V"][0], "NOI": m["NOI"][0]}
    return qs, out, F0


def fit_office_shock():
    """One parameter: constant quarterly log market-rent shock to office over 2022Q1-2023Q4 so that office true
    value 2022Q1 -> 2023Q4 = -35% (Green Street CPPI office vs its March-2022 peak, release of 5 Jan 2024)."""
    def gap(sz):
        qs, out, _ = replay("2021Q4", "2023Q4", ("2022Q1", "2023Q4"), sz, sectors=("OFF",))
        V = out["OFF"]["V"]
        i0, i1 = qs.index("2022Q1"), qs.index("2023Q4")
        return V[i1] / V[i0] - 1 - (-0.35)
    sz = brentq(gap, -0.30, 0.05)
    return sz


def gate_odce(office_sz, lam=None):
    qs, out, F0 = replay("2021Q4", "2026Q2", ("2022Q1", "2023Q4"), office_sz)
    T_ = len(qs) - 1
    lev, rd = 0.25, 0.045
    V = sum(w * out[k]["V"] / out[k]["V"][0] for k, w in ODCE_MIX.items())
    NOI = sum(w * out[k]["NOI"] / out[k]["V"][0] for k, w in ODCE_MIX.items())
    capex = 0.010
    lam = E.LAM_APP["RE_OE"] if lam is None else lam
    VA = np.zeros_like(V); VA[0] = V[0]
    for t in range(T_):
        VA[t + 1] = math.exp(lam * math.log(VA[t]) + (1 - lam) * math.log(V[t]))     # lambda_agg 0.75, 1q lag
    D = lev * V[0]

    def lev_tr(Vs):
        r = []
        for t in range(1, T_ + 1):
            E0 = Vs[t - 1] - D
            r.append((Vs[t] - Vs[t - 1] + NOI[t] / 4 - capex / 4 * Vs[t] - rd / 4 * D) / E0)
        return np.array(r)

    def max_dd(r):
        c = np.concatenate([[1.0], np.cumprod(1 + r)])
        peak = np.maximum.accumulate(c)
        dd = c / peak - 1
        j = int(np.argmin(dd)); i = int(np.argmax(c[: j + 1]))
        return float(dd[j]), qs[i], qs[j]
    rT, rA = lev_tr(V), lev_tr(VA)
    ddT, pT, tT = max_dd(rT)
    ddA, pA, tA = max_dd(rA)
    i0, i1 = qs.index("2022Q1"), qs.index("2023Q4")
    unlev_all = float(V[i1] / V[i0] - 1)
    unlev_by = {k: round(float(out[k]["V"][i1] / out[k]["V"][i0] - 1), 3) for k in out}
    # Green Street all-property cross-check uses a broader mix (incl. hotels, data centres) [I]
    gs_mix = {"LOG": 0.22, "RES": 0.25, "OFF": 0.15, "RET": 0.15, "HOT": 0.05, "DC": 0.03, "ALT": 0.15}
    Vgs = sum(w * out[k]["V"] / out[k]["V"][0] for k, w in gs_mix.items())
    lag = qs.index(tA) - qs.index(tT)
    res = {"window": [qs[0], qs[-1]], "office_shock_fitted_qtr_log": round(office_sz, 4), "lambda_agg": lam,
           "appraisal_levered_dd": round(ddA, 4), "appraisal_dd_window": [pA, tA],
           "true_levered_dd": round(ddT, 4), "true_dd_window": [pT, tT], "trough_lag_q": lag,
           "unlevered_true_2022Q1_2023Q4_odce_mix": round(unlev_all, 4),
           "unlevered_true_2022Q1_2023Q4_greenstreet_mix": round(float(Vgs[i1] / Vgs[i0] - 1), 4),
           "unlevered_true_by_sector_2022Q1_2023Q4": unlev_by,
           "targets": {"appraisal_dd": -0.188, "true_dd": -0.257, "lag_q": 3, "greenstreet_all_property": -0.22,
                       "greenstreet_office (fitted)": -0.35}}
    res["pass"] = {"appraisal_dd_within_3pp": abs(ddA + 0.188) <= 0.03, "true_dd_within_5pp": abs(ddT + 0.257) <= 0.05,
                   "lag_within_1q": abs(lag - 3) <= 1,
                   "greenstreet_all_within_4pp": abs(float(Vgs[i1] / Vgs[i0] - 1) + 0.22) <= 0.04}
    res["factor_path"] = {q: [round(float(F0[k][0, i]), 2) for k in ("y", "s", "pi", "g")] + [int(F0["f"][0, i])]
                          for i, q in enumerate(qs)}
    return res


CMBS_MIX = {"RET": 0.25, "OFF": 0.192, "HOT": 0.15, "RES": 0.15, "LOG": 0.10, "ALT": 0.158}   # [I] CMBS universe
_JIANG_CACHE = {}


def _jiang_replay(office_sz):
    if office_sz not in _JIANG_CACHE:
        _JIANG_CACHE[office_sz] = replay("2012Q4", "2023Q4", ("2022Q1", "2023Q4"), office_sz, sectors=tuple(CMBS_MIX))
    return _JIANG_CACHE[office_sz]


def gate_jiang(office_sz, sig_id=None, ltv_sd=0.09, n=200_000, seed=7, delta_off=0.0, delta_non=0.0, sig_shock=0.0):
    """CMBS-replica outstanding at 2023Q4: 10-year loans, 39% originated 2013-2015 and 61% 2016-2023Q3 (Jiang App. A5:
    39% of loans mature in 2023-25); balance amortises 30-year after a 3-year IO period on half the loans; origination
    LTV ~ N(mean_s, ltv_sd) clipped [0.30, 0.85] with means 54.4% office / 62.6% others (all-loan mean 61.0%).
    Value at 2023Q4 = V0 x engine sector index ratio x exp(delta_s x years to 2022Q1) [pre-shock drift correction]
    x lognormal(sig_shock) [dispersion of the 2022-23 repricing across MSAs and quality] x lognormal(sig_id sqrt(yrs))
    [property noise]. Jiang marks values with Green Street MSA x type indices, i.e. without property noise."""
    sig_id = E.SIG_ID_RE if sig_id is None else sig_id
    qs, out, _ = _jiang_replay(office_sz)
    rng = np.random.default_rng(seed)
    sec = rng.choice(list(CMBS_MIX), size=n, p=np.array(list(CMBS_MIX.values())) / sum(CMBS_MIX.values()))
    early = [q for q in qs[1:-1] if q <= "2015Q4"]
    late = [q for q in qs[1:-1] if q > "2015Q4"]
    vint = np.where(rng.random(n) < 0.39, rng.choice(early, size=n), rng.choice(late, size=n))
    mean_ltv = np.where(sec == "OFF", 0.544, (0.610 - 0.192 * 0.544) / (1 - 0.192))
    ltv0 = np.clip(rng.normal(mean_ltv, ltv_sd), 0.30, 0.85)
    iq = {q: i for i, q in enumerate(qs)}
    vi = np.array([iq[v] for v in vint])
    yrs = (iq["2023Q4"] - vi) / 4
    pre = np.maximum(iq["2022Q1"] - vi, 0) / 4
    io = rng.random(n) < 0.5
    c0 = 0.045
    amort_yrs = np.where(io, np.maximum(yrs - 3, 0), yrs)
    bal_ratio = ((1 + c0) ** 30 - (1 + c0) ** amort_yrs) / ((1 + c0) ** 30 - 1)
    Vend = {s: out[s]["V"][iq["2023Q4"]] for s in CMBS_MIX}
    idx = np.array([Vend[s] / out[s]["V"][i] for s, i in zip(sec, vi)])
    off = sec == "OFF"
    drift = np.exp(np.where(off, delta_off, delta_non) * pre)
    shock_disp = np.exp(sig_shock * rng.standard_normal(n) - 0.5 * sig_shock ** 2)
    idio = np.exp(sig_id * np.sqrt(yrs) * rng.standard_normal(n) - 0.5 * sig_id ** 2 * yrs)
    ltv_now = ltv0 * bal_ratio / (idx * drift * shock_disp * idio)
    res = {"sig_id": sig_id, "ltv_sd": ltv_sd, "delta_off": delta_off, "delta_non": delta_non, "sig_shock": sig_shock,
           "all": {"mean_init_ltv": round(float(ltv0.mean()), 4), "mean_current_ltv": round(float(ltv_now.mean()), 4),
                   "share_gt_80": round(float((ltv_now > 0.80).mean()), 4), "share_gt_100": round(float((ltv_now > 1.0).mean()), 4)},
           "office": {"mean_init_ltv": round(float(ltv0[off].mean()), 4), "mean_current_ltv": round(float(ltv_now[off].mean()), 4),
                      "share_gt_80": round(float((ltv_now[off] > 0.80).mean()), 4),
                      "share_gt_100": round(float((ltv_now[off] > 1.0).mean()), 4)},
           "sector_index_2013Q1_to_2023Q4": {s: round(float(out[s]["V"][-1] / out[s]["V"][1]), 3) for s in CMBS_MIX},
           "sector_index_2022Q1_to_2023Q4": {s: round(float(out[s]["V"][-1] / out[s]["V"][qs.index("2022Q1")]), 3) for s in CMBS_MIX},
           "targets": {"all": {"mean_current_ltv": 0.662, "share_gt_80": 0.290, "share_gt_100": 0.143},
                       "office": {"mean_current_ltv": 0.860, "share_gt_80": 0.560, "share_gt_100": 0.446}}}
    tg = res["targets"]
    res["pass"] = {f"{g}_{k}": abs(res[g][k] - tg[g][k]) <= 0.04 for g in ("all", "office") for k in tg[g]}
    return res


def fit_jiang(office_sz, n=120_000):
    """Calibration split: fit (delta_off, delta_non, sig_shock) to the two mean current LTVs and the all-loan >100%
    share; hold out the office >100%, office >80% and all >80% shares. Measurement-matched (no property noise)."""
    best = None
    for d_off in np.arange(-0.01, 0.061, 0.005):
        for d_non in np.arange(-0.02, 0.031, 0.005):
            for sg in np.arange(0.10, 0.61, 0.05):
                g = gate_jiang(office_sz, sig_id=0.0, n=n, delta_off=d_off, delta_non=d_non, sig_shock=sg)
                r = [g["all"]["mean_current_ltv"] - 0.662, g["office"]["mean_current_ltv"] - 0.860,
                     g["all"]["share_gt_100"] - 0.143]
                sse = sum(x * x for x in r)
                if best is None or sse < best[0]:
                    best = (sse, d_off, d_non, sg, r)
    _, d_off, d_non, sg, r = best
    g = gate_jiang(office_sz, sig_id=0.0, n=200_000, delta_off=d_off, delta_non=d_non, sig_shock=sg)
    g["fitted"] = {"delta_off_per_year": round(float(d_off), 4), "delta_non_per_year": round(float(d_non), 4),
                   "sig_shock": round(float(sg), 4), "fit_residuals": [round(float(x), 4) for x in r],
                   "method": "grid search, 3 parameters on 3 moments"}
    g["held_out"] = {k: g["pass"][k] for k in ("office_share_gt_100", "office_share_gt_80", "all_share_gt_80")}
    return g


def gate_chen(ell_sponsor=None, n_q=40, n_per=4000, seed=11, p_sale0=0.45, gap_lo=-3.0, gap_hi=1.5, beta_sale=0.0):
    """Maturing 10-year fixed CMBS loans in n_q transaction quarters (2003Q1-2019Q2 style), each quarter with its own
    market CRE rate r_T and cap rate; loans within a quarter differ by origination rate c0 (hence the rate gap), LTV,
    DSCR and NOI growth. Origination sizing: L0 = min(LTV0 V0, NOI0 / (DSCR0 k(c0))). At maturity the engine's
    decide_maturity applies with f = N (lender available) and sponsor-type (ruthless) owners with ell = ell_sponsor.
    A baseline share p_sale0 of owners sells regardless of financing (business-plan exits). Transactions = refinance
    (refi or cure) or sale; hand-backs are excluded (they are not RCA sale/refi transactions)."""
    rng = np.random.default_rng(seed)
    rows = []
    ellv = E.ELL_GP[C.fN] if ell_sponsor is None else ell_sponsor
    for qi in range(n_q):
        r_T = rng.uniform(0.045, 0.075)               # market CRE rate in the transaction quarter
        # cap rates load on rates with the engine's own beta_y (0.45), around 6.5% at a 5.7% loan rate
        cap_T = 0.065 + E.BETA_Y * (r_T - 0.057) + rng.normal(0, 0.003)
        n = n_per
        gap_pp = rng.uniform(gap_lo, gap_hi, n)       # rate gap r_T - c0 (pp); 2003-2019-type sample by default
        c0 = r_T - gap_pp / 100
        cap0 = np.clip(0.065 + E.BETA_Y * (c0 - 0.057) + rng.normal(0, 0.004, n), 0.035, 0.11)
        noi0 = cap0                                    # V0 = 1
        ltv_o = np.clip(rng.normal(0.66, 0.08, n), 0.40, 0.85)
        dscr_o = np.clip(rng.normal(1.40, 0.15, n), 1.15, 2.0)
        L0 = np.minimum(ltv_o, noi0 / (dscr_o * (c0 + 0.01)))
        bal = L0 * 0.86                                # 10 years of 30-year amortisation at ~5.7%
        noiT = noi0 * np.exp(0.02 * 10 + rng.normal(0, 0.15, n))
        VT = noiT / np.maximum(cap_T + rng.normal(0, 0.004, n), 0.03) * np.exp(rng.normal(0, 0.10, n))
        k_new = r_T + 0.01
        f = np.full(n, C.fN)
        dec = E.decide_maturity(bal, np.zeros(n), VT, noiT, VT, C.TERMS["ltv_max"][f], C.TERMS["dscr_min"][f],
                                C.TERMS["dy_min"][f], np.full(n, k_new), np.ones(n, bool), np.ones(n, bool),
                                np.zeros(n, int), 0.0, 0.0, 0.0, np.full(n, 9.9), np.zeros(n), np.ones(n),
                                np.zeros(n, int), np.zeros(n, int), 1.0, False, 0.0, np.full(n, ellv),
                                np.full(n, 0.12),   # Chen & Chen: rollover sales clear ~12% below refinance values
                                gap_pp=gap_pp, u_sale=rng.random(n), beta_sale=beta_sale)
        base_sale = rng.random(n) < p_sale0
        refi = (dec["refi"] | dec["cure"]) & ~base_sale
        sale = dec["sell"] | (base_sale & ~dec["hand"])
        tx = refi | sale
        for i in np.where(tx)[0]:
            rows.append((qi, gap_pp[i], 1.0 if refi[i] else 0.0, ltv_o[i], cap0[i] * 100, dscr_o[i], c0[i] * 100))
    A = np.array(rows)
    q = A[:, 0].astype(int)
    Y = A[:, 2]
    X = np.column_stack([A[:, 1], A[:, 3], A[:, 4], A[:, 5]])   # gap, orig LTV, cap rate, DSCR (c0 = r_T - gap)
    # within-quarter demeaning (quarter fixed effects)
    Xd = X.copy(); Yd = Y.copy()
    for qq in np.unique(q):
        m = q == qq
        Xd[m] -= X[m].mean(axis=0); Yd[m] -= Y[m].mean()
    beta, *_ = np.linalg.lstsq(Xd, Yd, rcond=None)
    resid = Yd - Xd @ beta
    # cluster-robust SE by quarter
    XtX_inv = np.linalg.inv(Xd.T @ Xd)
    meat = np.zeros((X.shape[1], X.shape[1]))
    for qq in np.unique(q):
        m = q == qq
        sg = Xd[m].T @ resid[m]
        meat += np.outer(sg, sg)
    V = XtX_inv @ meat @ XtX_inv
    se = float(np.sqrt(V[0, 0]))
    return {"ell_sponsor": float(ellv), "p_sale0": p_sale0, "gap_range_pp": [gap_lo, gap_hi], "beta_sale": beta_sale,
            "n_transactions": int(len(Y)),
            "refi_share": round(float(Y.mean()), 4), "slope_refi_on_gap_pp": round(float(beta[0]), 4),
            "se_cluster": round(se, 4), "target": -0.111, "ci95": [-0.148, -0.074],
            "pass": bool(-0.148 <= beta[0] <= -0.074),
            "heldout_matched_sample": {"target": -0.128, "ci95": [-0.175, -0.081],
                                       "pass": bool(-0.175 <= beta[0] <= -0.081)}}


def main():
    res = {"label": "Gates on public targets; engine outputs are SYNTHETIC - NOT ADIC DATA"}
    sz = fit_office_shock()
    # G-ODCE: engine as specified (G13 lambda_agg 0.75), then the smoothing variants
    res["G_ODCE"] = gate_odce(sz)
    res["G_ODCE_lambda_variants"] = {str(l): {k: gate_odce(sz, lam=l)[k] for k in
                                              ("appraisal_levered_dd", "true_levered_dd", "trough_lag_q", "pass")}
                                     for l in (0.50, 0.55, 0.60, 0.65, 0.70, 0.75)}
    # G-JIANG: (a) engine as specified (property noise SIG_ID_RE, no drift correction, no shock dispersion)
    res["G_JIANG_engine_as_specified"] = gate_jiang(sz)
    # (b) measurement-matched (index marking, no property noise), uncalibrated
    res["G_JIANG_measurement_matched_uncalibrated"] = gate_jiang(sz, sig_id=0.0)
    # (c) calibration split: 3 parameters fitted, 3 moments held out
    res["G_JIANG_calibrated"] = fit_jiang(sz, n=30_000)
    # G-CHEN: (a) mechanism only on a 2003-2019-type gap range, engine default sponsor ell; (b) the most permissive
    # mechanism (no equity injections, no planned sales); (c) the calibrated hazard on the engine's forward gap range
    res["G_CHEN_mechanism_default"] = gate_chen()
    res["G_CHEN_mechanism_max"] = gate_chen(ell_sponsor=1e6, p_sale0=0.0)
    res["G_CHEN_with_hazard_forward_range"] = gate_chen(gap_lo=0.0, gap_hi=3.0, p_sale0=0.0, beta_sale=E.BETA_ROLLOVER)
    res["G_CHEN_with_hazard_2003_2019_range"] = gate_chen(beta_sale=E.BETA_ROLLOVER)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=float)
    print("written", OUT)


if __name__ == "__main__":
    main()
