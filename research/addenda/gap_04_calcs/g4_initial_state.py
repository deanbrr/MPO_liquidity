"""gap_04: initial state as of October 2026 - filtered pi0 (macro regime), e0 (exit window), Z0 evidence
(oil shock decomposition) and the 12-month owner-draw expectation.

Usage: python -I g4_initial_state.py <data_dir> <cboe_dir> <brent_html> <out_dir>
All outputs are illustrative [I-calc]: public data, simplified filters, design-default parameters.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import logsumexp
from scipy.stats import multivariate_normal

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g4_load as L  # noqa: E402


def filt(params, X):
    k = len(params["startprob"])
    logb = np.column_stack([multivariate_normal(params["means"][j], params["covars"][j], allow_singular=True).logpdf(X)
                            for j in range(k)])
    logA = np.log(np.clip(params["transmat"], 1e-300, None))
    la = np.log(np.clip(params["startprob"], 1e-300, None)) + logb[0]
    la -= logsumexp(la)
    out = [np.exp(la)]
    for t in range(1, len(X)):
        la = logsumexp(la[:, None] + logA, axis=0) + logb[t]
        la -= logsumexp(la)
        out.append(np.exp(la))
    return np.array(out)


def p_visit_within(pi, A, target, n):
    """P(state 'target' is visited at least once in steps 1..n | current distribution pi)."""
    k = len(pi)
    keep = [j for j in range(k) if j != target]
    Ann = A[np.ix_(keep, keep)]
    v = np.ones(len(keep))
    for _ in range(n - 1):
        v = Ann @ v
    # first step: from any state (incl. target) into non-target, then avoid
    p_avoid = sum(pi[i] * (A[i, keep] @ v) for i in range(k))
    return float(1 - p_avoid)


def main():
    data_dir, cboe_dir, brent_html, out_dir = (Path(a) for a in sys.argv[1:5])
    res: dict = {}
    P = pd.read_csv(out_dir / "monthly_panel.csv", index_col=0)
    P.index = pd.PeriodIndex(P.index, freq="M")
    spx = L.cboe_close(cboe_dir / "SPX.csv", "SPX")
    vix = L.cboe_close(cboe_dir / "VIX.csv")
    gy = L.gsw_yields(data_dir / "feds200628.csv")
    eb = L.ebp(data_dir / "ebp.csv")
    cpi = L.multpl_cape(data_dir.parent / "data_multpl" / "cpi_by_month.html")
    infl = cpi / cpi.shift(12) - 1

    # --- extend monthly features to Sep-2026 (complete) and Oct-2026 (to date: 16 Oct equity, 9 Oct yields)
    ext = {}
    rf_m = float(P["rf"].dropna().iloc[-1])
    for m, (a, b) in {"2026-09": ("2026-08-31", "2026-09-30"), "2026-10": ("2026-09-30", "2026-10-16")}.items():
        s = spx.loc[a:b]
        r = np.log(s).diff().dropna()
        mret = float(s.iloc[-1] / s.iloc[0] - 1) + 0.0010 * (len(r) / 21)  # ~1.2%/yr dividend yield
        y10 = gy["y10"].dropna()
        dy = float(y10.loc[:b].iloc[-1] - y10.loc[:a].iloc[-1])
        per = pd.Period(m, "M")
        ext[m] = {"mkt_ex": mret - rf_m * (len(r) / 21), "log_rv": float(np.log(np.sqrt(252 * np.mean(r.to_numpy() ** 2)))),
                  "ebp_l1": float(eb["ebp"].loc[per - 1]), "dy10": dy, "infl_l1": float(infl.loc[per - 1]),
                  "n_days": int(len(r)), "spx_ret": round(float(s.iloc[-1] / s.iloc[0] - 1), 4),
                  "y10_end": round(float(y10.loc[:b].iloc[-1]), 3), "vix_end": float(vix.loc[:b].iloc[-1])}
    res["extension_inputs"] = ext
    res["latest_market"] = {"vix_2026-10-16": float(vix.loc["2026-10-16"]), "spx_2026-10-16": float(spx.loc["2026-10-16"]),
                            "gsw_y10_last": [str(gy["y10"].dropna().index[-1].date()), round(float(gy["y10"].dropna().iloc[-1]), 3)],
                            "ebp_2026-09": round(float(eb["ebp"].iloc[-1]), 3), "cpi_yoy_2026-09": round(float(infl.iloc[-1]), 4),
                            "cpi_yoy_2026-01": round(float(infl.loc[pd.Period("2026-01", "M")]), 4)}

    # --- pi0 under both filters
    pi = {}
    for K in (3, 4):
        z = np.load(out_dir / f"hmm_final_params_K{K}.npz", allow_pickle=True)
        params = {k: z[k] for k in ("startprob", "transmat", "means", "covars")}
        feats = [str(f) for f in z["feats"]]
        order = list(z["order"])
        mu, sd = z["mu"], z["sd"]
        H = P[feats].dropna()
        Xe = pd.concat([H, pd.DataFrame({m: {f: ext[m][f] for f in feats} for m in ext}).T.set_index(
            pd.PeriodIndex(list(ext), freq="M"))])
        X = ((Xe - mu) / sd).to_numpy()
        fp = filt(params, X)[:, order]
        A = params["transmat"][np.ix_(order, order)]
        labels = (["calm", "elevated", "crisis"] if K == 3 else
                  ["S1 moderate-infl. expansion", "S2 low-infl. calm", "S3 high-inflation", "S4 stress"])
        last = {str(i): dict(zip(labels, np.round(fp[n], 4).tolist())) for n, i in
                zip(range(len(Xe) - 4, len(Xe)), Xe.index[-4:])}
        pi_sep = fp[-2]
        crisis_idx = len(labels) - 1
        pi[f"K{K}"] = {"filtered_last4": last,
                       "pi0_2026-09": dict(zip(labels, np.round(pi_sep, 4).tolist())),
                       "pi_12m_ahead": dict(zip(labels, np.round(pi_sep @ np.linalg.matrix_power(A, 12), 4).tolist())),
                       "P(stress state visited within 12m)": round(p_visit_within(pi_sep, A, crisis_idx, 12), 4),
                       "P(stress within 12m | stationary start)": None,
                       "stationary": None}
        w, v = np.linalg.eig(A.T)
        st = np.real(v[:, np.argmin(abs(w - 1))])
        st = st / st.sum()
        pi[f"K{K}"]["stationary"] = dict(zip(labels, np.round(st, 4).tolist()))
        pi[f"K{K}"]["P(stress within 12m | stationary start)"] = round(p_visit_within(st, A, crisis_idx, 12), 4)
        # stress-state share of months 1990-2026 under the final filter (for context)
    res["pi0"] = pi

    # --- e0: exit-window filter on MSCI PE distribution rates (annualised, distributions / prior NAV)
    states = ["O", "N", "D", "F"]
    mD = np.array([1.25, 1.0, 0.475, 0.325])     # synthesis 4.2 multipliers (D, F at band midpoints)
    base = 0.20                                    # normal-state distribution rate (synthesis 2.3)
    Aq = np.array([[0.85, 0.15, 0.00, 0.00],       # quarterly; diagonal from synthesis 4.2, off-diagonals [I]
                   [0.06, 0.88, 0.06, 0.00],
                   [0.00, 0.08, 0.88, 0.04],
                   [0.00, 0.05, 0.20, 0.75]])
    w, v = np.linalg.eig(Aq.T)
    st = np.real(v[:, np.argmin(abs(w - 1))])
    st = st / st.sum()
    obs = [("2017", 0.24, 4), ("2018", 0.21, 4), ("2019", 0.18, 4), ("2020", 0.17, 4), ("2021", 0.27, 4),
           ("2022", 0.11, 4), ("2023", 0.09, 4), ("2024", 0.11, 4), ("2025", 0.11, 4), ("H1-2026", 0.09, 2)]
    sig = 0.15
    post = st.copy()
    trace = {}
    for lab, y, q in obs:
        post = post @ np.linalg.matrix_power(Aq, q)
        lik = np.exp(-0.5 * ((np.log(y) - np.log(base * mD)) / sig) ** 2)
        post = post * lik
        post = post / post.sum()
        trace[lab] = dict(zip(states, np.round(post, 3).tolist()))
    e_oct = post @ Aq  # one quarter forward (end-Q2 -> Q3/Oct)
    e_4q = e_oct @ np.linalg.matrix_power(Aq, 4)
    exp_dist_rate_12m = float(np.mean([(e_oct @ np.linalg.matrix_power(Aq, k)) @ (base * mD) for k in range(4)]))
    res["e0"] = {"prior_stationary": dict(zip(states, np.round(st, 3).tolist())), "trace": trace,
                 "e0_2026-10": dict(zip(states, np.round(e_oct, 3).tolist())),
                 "e_12m_ahead": dict(zip(states, np.round(e_4q, 3).tolist())),
                 "expected_dist_rate_next_12m": round(exp_dist_rate_12m, 4),
                 "expected_distributions_next_12m_usd_bn_on_106bn": round(exp_dist_rate_12m * 106, 1),
                 "same_if_starting_N_usd_bn": round(float(np.mean([(np.array([0, 1, 0, 0]) @ np.linalg.matrix_power(Aq, k)) @ (base * mD)
                                                                   for k in range(4)])) * 106, 1),
                 "ipo_ratio_last": {str(i): round(float(v), 2) for i, v in P["ipo_ratio"].dropna().iloc[-6:].items()},
                 "ipo_net_2025_total": float(P.loc["2025-01":"2025-12", "ipo_net"].sum()),
                 "ipo_net_2021_total": float(P.loc["2021-01":"2021-12", "ipo_net"].sum()),
                 "ipo_net_2022_total": float(P.loc["2022-01":"2022-12", "ipo_net"].sum()),
                 "ipo_net_2024_total": float(P.loc["2024-01":"2024-12", "ipo_net"].sum())}

    # --- Z0 evidence: Ready (2018)-style decomposition of Brent moves (producer stocks = FF49 'Oil')
    ind = L.ff49_daily(data_dir / "ind49_daily.zip")
    brent = L.eia_daily(brent_html)
    dpx = np.log(brent[brent > 0]).diff()
    dvix = vix.diff()
    D = pd.concat([dpx.rename("dp"), ind["Oil"].rename("rprod"), dvix.rename("dvix")], axis=1, join="inner").dropna()
    est = D.loc["1990-01-02":"2025-12-31"]
    X1 = np.column_stack([np.ones(len(est)), est["dvix"]])
    b1 = np.linalg.lstsq(X1, est["rprod"], rcond=None)[0]
    d_sh = est["rprod"] - X1 @ b1
    X2 = np.column_stack([np.ones(len(est)), d_sh, est["dvix"]])
    b2 = np.linalg.lstsq(X2, est["dp"], rcond=None)[0]
    s_sh = est["dp"] - X2 @ b2
    r2_dp = 1 - s_sh.var() / est["dp"].var()
    def decompose(a, b):
        w = D.loc[a:b]
        dd = w["rprod"] - (b1[0] + b1[1] * w["dvix"])
        ss = w["dp"] - (b2[0] + b2[1] * dd + b2[2] * w["dvix"])
        return {"window": [str(w.index[0].date()), str(w.index[-1].date())], "n_days": len(w),
                "cum_dlogp": round(float(w["dp"].sum()), 3),
                "demand": round(float((b2[1] * dd).sum()), 3), "risk": round(float((b2[2] * w["dvix"]).sum()), 3),
                "supply": round(float(ss.sum()), 3), "drift": round(float(b2[0] * len(w)), 3)}
    res["Z0_ready_decomposition"] = {
        "estimation": "1990-01-02..2025-12-31 daily; rprod = FF49 Oil (US-listed oil & gas, VW); dvix = daily VIX change",
        "beta_rprod_on_dvix": round(float(b1[1]), 5), "beta_dp_on_demand": round(float(b2[1]), 3),
        "beta_dp_on_dvix": round(float(b2[2]), 5), "R2_dp_explained_by_demand_risk": round(float(r2_dp), 3),
        "war_onset_to_Aug": decompose("2026-02-27", "2026-08-31"),
        "Mar_2026": decompose("2026-03-01", "2026-03-31"),
        "Apr_Aug_2026": decompose("2026-04-01", "2026-08-31"),
        "comparison_2014H2_2015": decompose("2014-07-01", "2015-12-31"),
        "comparison_2008H2": decompose("2008-07-01", "2008-12-31"),
        "comparison_2020Q1": decompose("2020-01-01", "2020-04-30"),
        "comparison_2022H1": decompose("2022-01-01", "2022-06-30")}

    # --- 12-month owner-draw expectation (C3 5.1-5.2 defaults; linear fiscal map)
    rng = np.random.default_rng(20261018)
    N = 200_000
    Zs = ["N", "B", "SG", "DB", "SS", "GW"]
    Pa = np.array([[.62, .15, .10, .05, .04, .04], [.40, .40, .05, .06, .07, .02], [.38, .12, .42, .04, .02, .02],
                   [.35, .30, .20, .10, .03, .02], [.30, .05, .10, .35, .15, .05], [.30, .05, .35, .05, .05, .20]])
    Pm = np.eye(6) + (Pa - np.eye(6)) / 12
    mu_z = np.array([0, .20, -.35, -.45, .30, .10])
    sg_z = np.array([.20, .20, .20, .25, .25, .30])
    w_fix = np.array([0, 0, -.5, -1.5, -.5, np.nan])
    p_ov = np.array([.0025, .0025, .01, .01, .0025, .02])
    km = 1 - 0.6 ** (1 / 12)
    h27, Pref = 11.3 - (11.3 - 9.1) / 4, 62.5
    q_norm, q_gw = 5.20 / 4.34, 4.12 / 4.34   # EIA STEO Oct-2026 UAE liquids 2027F and 2026 vs 2025
    sig_be = (np.log(70) - np.log(45)) / (2 * 1.645)

    def simulate(z0_probs, d2026, p0=126.55, imf_fuse=False):
        z = rng.choice(6, size=N, p=z0_probs)
        lp = np.full(N, np.log(p0))
        cum = np.cumsum(Pm, 1)
        months_2027 = np.zeros((N, 6))
        p27 = np.zeros(N)
        for t in range(14):  # Nov-2026 .. Dec-2027
            u = rng.random(N)
            z = (u[:, None] > cum[z]).sum(1)
            jump = (z == 5) & (rng.random(N) < 0.25 / 12)
            lp = lp + km * (np.log(70) - lp) + mu_z[z] / 12 + sg_z[z] / np.sqrt(12) * rng.standard_normal(N) \
                + jump * np.where(rng.random(N) < 0.5, 0.26, -0.26)
            if t >= 2:
                months_2027[np.arange(N), z] += 1
                p27 += np.exp(lp)
        p27 /= 12
        frac = months_2027 / 12
        pbe = np.exp(np.log(55) + sig_be * rng.standard_normal(N))
        wgw = np.clip(rng.normal(-5, 2, N), -9, -1)
        wz = frac[:, :5] @ w_fix[:5] + frac[:, 5] * wgw
        q = q_norm * (1 - frac[:, 5]) + q_gw * frac[:, 5]
        peff = p27 + rng.normal(0, 2, N)
        fb = 100 * h27 / 100 * (peff * q - pbe) / Pref * 1.0 + wz + rng.standard_normal(N)
        if imf_fuse:  # precision-weighted fusion with the IMF Oct-2026 projection for 2027 (+4.4pp, sd 2.5 [I])
            sm2 = fb.var()
            fb = (fb / sm2 + 4.4 / 2.5 ** 2) / (1 / sm2 + 1 / 2.5 ** 2)
        dstar = np.clip(7.5 - 0.625 * fb, 5, 10)
        d27 = np.clip(0.5 * d2026 + 0.5 * dstar, 5, 10)
        zdom = frac.argmax(1)
        ov = rng.random(N) < p_ov[zdom]
        d27 = np.where(ov, 10 + rng.uniform(2, 5, N), d27)
        d12 = d2026 / 4 + 3 * d27 / 4
        return {"E_brent_2027avg": round(float(p27.mean()), 1),
                "brent_2027avg_p10_p50_p90": np.round(np.percentile(p27, [10, 50, 90]), 1).tolist(),
                "E_frac_2027_in_state": dict(zip(Zs, np.round(frac.mean(0), 3).tolist())),
                "E_FB_2027_pp": round(float(fb.mean()), 2), "FB_p10_p50_p90": np.round(np.percentile(fb, [10, 50, 90]), 2).tolist(),
                "E_d2027_pct": round(float(d27.mean()), 2), "d2027_p10_p50_p90": np.round(np.percentile(d27, [10, 50, 90]), 2).tolist(),
                "P(d2027>=9.5%)": round(float((d27 >= 9.5).mean()), 4), "P(override)": round(float(ov.mean()), 4),
                "E_12m_draw_pct_NAV": round(float(d12.mean()), 2),
                "E_12m_draw_usd_bn_on_177": round(float(d12.mean()) / 100 * 177, 2),
                "12m_draw_p90_usd_bn": round(float(np.percentile(d12, 90)) / 100 * 177, 2)}

    z0_gw = np.array([0.03, 0.0, 0.0, 0.02, 0.10, 0.85])
    stat = np.real(np.linalg.eig(Pa.T)[1][:, np.argmin(abs(np.linalg.eig(Pa.T)[0] - 1))])
    stat = stat / stat.sum()
    draws = {}
    for d26 in (5.0, 5.8, 6.6):
        draws[f"d2026={d26}"] = {"Z0=GW-posterior(0.85 GW,0.10 SS,0.03 N,0.02 DB)": simulate(z0_gw, d26),
                                 "Z0=N": simulate(np.eye(6)[0], d26),
                                 "Z0=stationary": simulate(stat, d26)}
    draws["d2026=5.8_variants"] = {
        "GW-posterior, oil start 105 (EIA 4Q26 avg; ~ICE front month mid-Oct)": simulate(z0_gw, 5.8, p0=105.0),
        "GW-posterior, oil start 105 + IMF fusion": simulate(z0_gw, 5.8, p0=105.0, imf_fuse=True),
        "N, oil start 105 + IMF fusion": simulate(np.eye(6)[0], 5.8, p0=105.0, imf_fuse=True),
        "GW-posterior, oil start 84 (EIA 2027 avg)": simulate(z0_gw, 5.8, p0=84.0),
    }
    res["draw_12m"] = draws
    res["draw_12m_assumptions"] = {
        "fiscal_map": "FB = 100 h (P_eff q - P_BE)/P_ref + sum_z frac_z w_z + eps (C3 linear default)",
        "h_2027_pct": h27, "P_ref": Pref, "q_norm": round(q_norm, 3), "q_gw": round(q_gw, 3),
        "P_BE": "lognormal median 55, 90% 45-70", "w_GW": "N(-5,2^2) trunc [-9,-1]",
        "draw": "d* = clip(7.5 - 0.625 FB, 5, 10); d = clip(0.5 d_2026 + 0.5 d*, 5, 10); override by dominant state",
        "oil": "C3 monthly: kappa_m=1-0.6^(1/12), P_LR=70, (mu,sigma)_Z annual/12, GW jumps +-0.26 w.p. 0.25/12; start 126.55 (EIA spot 14-Oct-2026)",
        "window": "Nov-2026..Oct-2027: Q4-2026 instalment at d_2026, three 2027 instalments at d_2027",
        "d_2026_note": "client data; 5.8% is the reduced form's smoothed value on IMF net-lending 2024-26 (6.2, 3.9, 1.5)"}
    (out_dir / "initial_state_results.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
