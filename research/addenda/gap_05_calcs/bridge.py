"""Gap 05: expected-return bridge per CMA model for the ADIC working (SYNTHETIC) allocation.

Usage: python -I bridge.py <jpm2026.npz> <out.json>

All ADIC weights are the working (synthetic) allocation of context section 1A, not ADIC data.
Conventions: 10-year nominal USD, geometric (compound) returns; consistent lognormal conversion
(verifier 10-R7): portfolio geometric = exp(ln(1+m) - 0.5*ln(1+s^2/(1+m)^2)) - 1.
Lever alphas are per $ of sleeve NAV, net of fees, relative to that sleeve's CMA beta.
"""
import json
import sys

import numpy as np
from scipy import optimize, stats

D = np.load(sys.argv[1], allow_pickle=False)
names = [str(x) for x in D["names"]]
comp, arith, vol, C = D["comp"], D["arith"], D["vol"], D["corr"]


def higham(A, iters=5000, tol=1e-12):
    Y = A.copy(); dS = np.zeros_like(A)
    for _ in range(iters):
        R = Y - dS
        w, V = np.linalg.eigh((R + R.T) / 2)
        X = (V * np.clip(w, 0, None)) @ V.T
        dS = X - R
        Yn = X.copy(); np.fill_diagonal(Yn, 1.0)
        if np.abs(Yn - Y).max() < tol:
            return Yn
        Y = Yn
    return Y


Cp = higham(C)
ix = {n: i for i, n in enumerate(names)}

# ------------------------------------------------------------------ 0. regression test vs verifier 10 (stylised book)
w_sty = {"Private Equity": .38, "Venture Capital": .04, "Direct Lending": .07, "U.S. Core Real Estate": .04,
         "U.S. Value-Added Real Estate": .02, "Global Core Infrastructure": .05, "AC World Equity": .22,
         "U.S. Aggregate Bonds": .06, "U.S. Inv Grade Corporate Bonds": .02, "Diversified Hedge Funds": .06,
         "U.S. Cash": .04}
ii = [ix[k] for k in w_sty]; wv = np.array(list(w_sty.values()))
S_ = Cp[np.ix_(ii, ii)] * np.outer(vol[ii], vol[ii])
m_ = wv @ arith[ii]; s_ = np.sqrt(wv @ S_ @ wv)
sl_ = np.sqrt(np.log1p(s_ ** 2 / (1 + m_) ** 2)); g_ = np.expm1(np.log1p(m_) - 0.5 * sl_ ** 2)
p10_5 = 1 - stats.norm.cdf((np.log1p(.10) - np.log1p(g_)) / (sl_ / np.sqrt(5)))
p7_5 = stats.norm.cdf((np.log1p(.07) - np.log1p(g_)) / (sl_ / np.sqrt(5)))
regtest = dict(arith=m_, vol=s_, geo=g_, p5_ge10=p10_5, p5_lt7=p7_5)

# ------------------------------------------------------------------ 1. ADIC working allocation -> 6 CMA classes
K = ["PE", "DL", "HF", "EQ", "FI", "CASH"]
jn = {"PE": "Private Equity", "DL": "Direct Lending", "HF": "Diversified Hedge Funds", "EQ": "AC World Equity",
      "FI": "U.S. Aggregate Bonds", "CASH": "U.S. Cash"}
kk = [ix[jn[k]] for k in K]
VOL0 = vol[kk].copy(); R0 = Cp[np.ix_(kk, kk)].copy()
CONV = (arith - comp)[kk]          # JPM-2026 arithmetic-minus-compound spread per class (vol-implied)
NAV = 177.0
alloc = dict(PE=52, SEC=14, COI=18, CAP=8, PCR=14, HF=20, LOEQ=28, LOFI=8, TRE=15)   # $bn [A]
w = np.array([(52 + 14 + 18 + 4) / NAV, (14 + 4) / NAV, 20 / NAV, 28 / NAV, 8 / NAV, 15 / NAV])
assert abs(w.sum() - 1) < 1e-12

# CMA compound returns (10y nominal, net of fees; % -> decimal). Sources in the addendum.
CMA = {
    "M1 JPM-2027": dict(PE=9.6, DL=7.7, HF=6.7, EQ=7.5, FI=5.3, CASH=3.1),
    "M2 BlackRock fee-adj": dict(PE=15.888 - 3.5, DL=9.307 - 2.0, HF=9.291 - 2.5, EQ=9.015, FI=4.879, CASH=3.665),
    "M3 AQR nominal": dict(PE=4.2 + 2.4, DL=2.6 + 2.4, HF=5.3, EQ=4.2 + 2.4, FI=2.5 + 2.4, CASH=1.3 + 2.4),
    "M4 JPM drought": dict(PE=9.6, DL=7.7, HF=6.7, EQ=7.5, FI=5.3, CASH=3.1),
    "M5 JPM stagflation": dict(PE=9.6, DL=7.7, HF=6.7, EQ=7.5, FI=5.3, CASH=3.1),
    "M6 BlackRock RPR fee-adj": dict(PE=9.355 - 3.5, DL=8.960 - 2.0, HF=7.660 - 2.5, EQ=4.570, FI=5.110, CASH=4.046),
}


def risk(model):
    """Vol vector and correlation matrix by model (JPM-2026 risk for all; M5 stagflation stress)."""
    v = VOL0.copy(); R = R0.copy()
    if model.startswith("M5"):
        v = v * 1.15
        risky = [0, 1, 2, 3]                     # PE, DL, HF, EQ
        for a in risky:
            for b in risky:
                if a != b:
                    R[a, b] = R[a, b] + 0.5 * (0.9 - R[a, b])
        for a in risky:                           # stock-bond correlation positive (2022-like)
            R[a, 4] = R[4, a] = 0.4
        R = higham(R)
    return v, R


def portfolio(model, extra_mu=0.0, extra_var=0.0, L=1.0, s_fin=0.005):
    v, R = risk(model)
    g = np.array([CMA[model][k] for k in K]) / 100
    conv = CONV * (1.15 ** 2 if model.startswith("M5") else 1.0)
    a = g + conv                                   # asset arithmetic means
    S = R * np.outer(v, v)
    m = w @ a; var = w @ S @ w
    if L != 1.0:                                   # (L-1) x ACWI futures, financed at cash + s_fin
        e = 3
        m += (L - 1) * (a[e] - g[5] - s_fin)
        var += 2 * (L - 1) * (S @ w)[e] + (L - 1) ** 2 * S[e, e]
    m += extra_mu; var += extra_var
    sl = np.sqrt(np.log1p(var / (1 + m) ** 2))
    geo = np.expm1(np.log1p(m) - 0.5 * sl ** 2)
    return dict(arith=m, vol=np.sqrt(var), geo=geo, sl=sl)


# ------------------------------------------------------------------ 2. lever priors (per $ of sleeve, pp/yr)
# (P10, central, P90); normal with sd=(P90-P10)/2.563. Weights = share of NAV the alpha applies to.
LEVERS = {
    "PE primaries: selection + fee scale": dict(w=52 / NAV, p=(-0.55, 0.75, 2.05)),
    "Co-investment (fee saving net of timing/size)": dict(w=18 / NAV, p=(-1.0, 1.0, 2.5)),
    "Secondaries (discount capture, net)": dict(w=14 / NAV, p=(-0.5, 1.0, 2.5)),
    "Capital Solutions": dict(w=8 / NAV, p=(-1.5, 0.0, 1.5)),
    "Private Credit": dict(w=14 / NAV, p=(-1.5, 0.0, 0.75)),
    "Hedge-fund selection vs median": dict(w=20 / NAV, p=(-1.5, 0.0, 1.5)),
    "Long-only active vs index": dict(w=28 / NAV, p=(-0.6, -0.15, 0.3)),
    "Physical-to-synthetic ($10bn, per $ converted)": dict(w=10 / NAV, p=(-0.5, -0.1, 0.2)),
}
SR_PRIOR = (0.30, 0.25); SIG_O = 0.0125           # opportunistic overlay: Sharpe prior N(0.3,0.25^2), vol 1.25% NAV
LEV = (1.00, 1.05, 1.30)                            # economic exposure (P10, central, P90=cap)
S_FIN = {"normal": 0.003, "jun2026": 0.0081, "stress": 0.0175}

# ------------------------------------------------------------------ 3. drags (pp of NAV per year, positive = drag)


def drags(model, case="central"):
    c = CMA[model]
    erp = (c["EQ"] - c["CASH"]) / 100
    prem_pe = max((c["PE"] - c["EQ"]) / 100, 0.0)
    drought = model.startswith("M4") or model.startswith("M6")
    stag = model.startswith("M5")
    lo, ce, hi = 0, 1, 2
    k = {"low": lo, "central": ce, "high": hi}[case]
    convex_prem = (0.0015, 0.0020, 0.0050)[k]
    pq = (0.70, 0.55, 0.40)[k]                       # E^P[payoff]/premium
    d_convex = convex_prem * (1 - pq)
    reserve = (0.03, 0.05, 0.07)[k] + (0.01 if (drought or stag) else 0.0)
    carry = 0.5 * erp + 0.5 * 0.0125                 # half funded by selling risk assets, half by term debt
    d_reserve = reserve * carry
    fac = (0.05, 0.10, 0.20)[k] + (0.05 if drought else 0.0)
    d_fac = fac * (0.0015, 0.0030, 0.0040)[k]
    dpriv = (0.0, 0.03, 0.06)[k] + (0.03 if drought else 0.0)
    d_pacing = dpriv * (prem_pe + 0.0075)            # forgone private premium + central PE alpha
    d_forced = (0.0003, 0.0006, 0.0025)[k] + (0.0010 if drought else 0.0)
    out = dict(convex=d_convex, reserve=d_reserve, facilities=d_fac, pacing=d_pacing, forced_sales=d_forced)
    out["total"] = sum(out.values())
    return out


def bridge(model, lever_vals=None, L=LEV[1], SR=SR_PRIOR[0], sig_o=SIG_O, drag_case="central", s_fin=S_FIN["normal"],
           tau=True):
    lv = {k: v["p"][1] for k, v in LEVERS.items()}
    if lever_vals:
        lv.update(lever_vals)
    alpha = sum(LEVERS[k]["w"] * lv[k] / 100 for k in LEVERS)
    dg = drags(model, drag_case)
    extra_mu = alpha + SR * sig_o - dg["total"]
    pf = portfolio(model, extra_mu=extra_mu, extra_var=sig_o ** 2, L=L, s_fin=s_fin)
    # parameter (lever) uncertainty: persistent, does not diversify over time
    t2 = 0.0
    if tau:
        for k, v in LEVERS.items():
            sd = (v["p"][2] - v["p"][0]) / 2.563 / 100
            t2 += (v["w"] * sd) ** 2
        t2 += (SR_PRIOR[1] * sig_o) ** 2
        t2 = t2 / (1 + pf["arith"]) ** 2
    pf["tau2"] = t2
    pf["alpha"] = alpha; pf["overlay"] = SR * sig_o; pf["drags"] = dg
    return pf


def p_ge(pf, H, thr=0.10):
    sd = np.sqrt(pf["sl"] ** 2 / H + pf["tau2"])
    return 1 - stats.norm.cdf((np.log1p(thr) - np.log1p(pf["geo"])) / sd)


models = list(CMA)
out = dict(regtest=regtest, weights=dict(zip(K, w.tolist())), models={})
for m in models:
    beta = portfolio(m)
    lev_only = {}
    rows = {}
    base = bridge(m)
    # contribution by lever (difference in geometric return vs all-else-central with lever at zero)
    contrib = {}
    for k in LEVERS:
        z = bridge(m, {k: 0.0})
        contrib[k] = base["geo"] - z["geo"]
    contrib["Opportunistic overlay"] = base["geo"] - bridge(m, SR=0.0, sig_o=0.0)["geo"]
    contrib["Economic leverage (1.05x)"] = base["geo"] - bridge(m, L=1.0)["geo"]
    # break-evens to reach 10% (others central)
    be = {}
    for k, v in LEVERS.items():
        f = lambda a: bridge(m, {k: a})["geo"] - 0.10
        try:
            a_be = optimize.brentq(f, -50, 200)
        except ValueError:
            a_be = float("nan")
        sd = (v["p"][2] - v["p"][0]) / 2.563
        be[k] = dict(alpha_be=a_be, p_reach=float(1 - stats.norm.cdf((a_be - v["p"][1]) / sd)),
                     p10y_at_p90=float(p_ge(bridge(m, {k: v["p"][2]}), 10)),
                     p10y_at_zero=float(p_ge(bridge(m, {k: 0.0}), 10)))
    f = lambda s: bridge(m, SR=s, sig_o=0.015)["geo"] - 0.10
    try:
        sr_be = optimize.brentq(f, -5, 50)
    except ValueError:
        sr_be = float("nan")
    be["Opportunistic overlay (SR at 1.5% vol)"] = dict(
        alpha_be=sr_be, p_reach=float(1 - stats.norm.cdf((sr_be - SR_PRIOR[0]) / SR_PRIOR[1])),
        p10y_at_p90=float(p_ge(bridge(m, SR=SR_PRIOR[0] + 1.2816 * SR_PRIOR[1]), 10)),
        p10y_at_zero=float(p_ge(bridge(m, SR=0.0, sig_o=0.0), 10)))
    f = lambda L: bridge(m, L=L)["geo"] - 0.10
    try:
        L_be = optimize.brentq(f, 1.0, 5.0)
    except ValueError:
        L_be = float("nan")
    be["Economic leverage (x)"] = dict(alpha_be=L_be, p_reach=float("nan"),
                                       p10y_at_p90=float(p_ge(bridge(m, L=1.30), 10)),
                                       p10y_at_zero=float(p_ge(bridge(m, L=1.0), 10)))
    for nm, sf in S_FIN.items():
        be["Economic leverage (x)"][f"geo_at_1.30_{nm}"] = float(bridge(m, L=1.30, s_fin=sf)["geo"])
    allp90 = bridge(m, {k: v["p"][2] for k, v in LEVERS.items()}, L=1.30, SR=SR_PRIOR[0] + 1.2816 * SR_PRIOR[1],
                    drag_case="low")
    allp10 = bridge(m, {k: v["p"][0] for k, v in LEVERS.items()}, L=1.0, SR=SR_PRIOR[0] - 1.2816 * SR_PRIOR[1],
                    drag_case="high")
    out["models"][m] = dict(
        beta_geo=beta["geo"], beta_arith=beta["arith"], beta_vol=beta["vol"],
        central_geo=base["geo"], central_vol=base["vol"], alpha_total=base["alpha"], overlay=base["overlay"],
        drags=base["drags"], contrib=contrib,
        p10y_beta=float(p_ge(dict(beta, tau2=0.0), 10)), p5y_beta=float(p_ge(dict(beta, tau2=0.0), 5)),
        p10y_central=float(p_ge(base, 10)), p5y_central=float(p_ge(base, 5)),
        gap_to_10=0.10 - base["geo"], breakeven=be,
        allp90_geo=allp90["geo"], allp90_p10y=float(p_ge(allp90, 10)),
        allp10_geo=allp10["geo"], allp10_p10y=float(p_ge(allp10, 10)),
        drags_low=drags(m, "low")["total"], drags_high=drags(m, "high")["total"])

# ------------------------------------------------------------------ 4. plan / stretch / aspiration statistics
# P(true expected geometric return >= 10%) under lever-parameter uncertainty only (market noise excluded)
sd_lev = np.sqrt(sum((v["w"] * (v["p"][2] - v["p"][0]) / 2.563 / 100) ** 2 for v in LEVERS.values())
                 + (SR_PRIOR[1] * SIG_O) ** 2)
out["sd_levers_pp"] = float(sd_lev * 100)
for m in models:
    r = out["models"][m]
    g105 = r["central_geo"]; g130 = bridge(m, L=1.30)["geo"]
    r["p_mu_ge10_L105"] = float(1 - stats.norm.cdf((0.10 - g105) / sd_lev))
    r["p_mu_ge10_L130"] = float(1 - stats.norm.cdf((0.10 - g130) / sd_lev))
    r["central_geo_L130"] = float(g130)
    base = bridge(m)
    r["p10y_hurdles"] = {f"{h:.3f}": float(p_ge(base, 10, h)) for h in (0.0789, 0.10, 0.1081, 0.1389)}
    r["p10y_central_L130"] = float(p_ge(bridge(m, L=1.30), 10))

# mixture summaries (equal weights)
mix = {}
for key in ["beta_geo", "central_geo", "p10y_beta", "p10y_central", "p5y_central", "allp90_p10y", "allp10_p10y"]:
    vals = [out["models"][m][key] for m in models]
    mix[key] = dict(mean=float(np.mean(vals)), min=float(np.min(vals)), max=float(np.max(vals)))
out["mixture"] = mix
out["payout_hurdles_real_preserving"] = {d: (1.025 / (1 - d) - 1) for d in (0.05, 0.075, 0.10)}


def conv(o):
    if isinstance(o, dict):
        return {k: conv(v) for k, v in o.items()}
    if isinstance(o, (np.floating, float)):
        return float(o)
    return o


with open(sys.argv[2], "w", encoding="utf-8") as fh:
    json.dump(conv(out), fh, indent=1)

# ------------------------------------------------------------------ console summary
print("regression test (stylised book, JPM 2026):", {k: round(float(v), 4) for k, v in regtest.items()})
print("weights:", dict(zip(K, np.round(w, 4))))
for m in models:
    r = out["models"][m]
    print(f"\n== {m}: beta geo {r['beta_geo']:.4f} (arith {r['beta_arith']:.4f}, vol {r['beta_vol']:.4f}); "
          f"central {r['central_geo']:.4f}; gap {r['gap_to_10']:+.4f}; alpha {r['alpha_total']:.4f}; "
          f"overlay {r['overlay']:.4f}; drags {r['drags']['total']:.4f} [{r['drags_low']:.4f}-{r['drags_high']:.4f}]")
    print("   drags:", {k: round(v, 4) for k, v in r["drags"].items()})
    print("   contrib:", {k[:28]: round(v, 4) for k, v in r["contrib"].items()})
    print(f"   P10y>=10%: beta {r['p10y_beta']:.3f} central {r['p10y_central']:.3f} | P5y central {r['p5y_central']:.3f}"
          f" | all-P90 geo {r['allp90_geo']:.4f} P10y {r['allp90_p10y']:.3f} | all-P10 geo {r['allp10_geo']:.4f}"
          f" P10y {r['allp10_p10y']:.3f}")
    for k, b in r["breakeven"].items():
        extra = {kk: round(vv, 4) for kk, vv in b.items() if kk.startswith("geo_at")}
        print(f"   BE {k[:44]:44s} {b['alpha_be']:8.3f}  P(reach) {b['p_reach']:.3f}  P10y@P90 {b['p10y_at_p90']:.3f}"
              f"  P10y@0 {b['p10y_at_zero']:.3f} {extra if extra else ''}")
print("\nsd of lever uncertainty (pp):", round(out["sd_levers_pp"], 3))
for m in models:
    r = out["models"][m]
    print(f"{m:26s} P(mu>=10%) L1.05 {r['p_mu_ge10_L105']:.3f} L1.30 {r['p_mu_ge10_L130']:.3f} "
          f"(geo@1.30 {r['central_geo_L130']:.4f}; P10y@1.30 {r['p10y_central_L130']:.3f}) "
          f"P10y>=hurdles {({k: round(v, 3) for k, v in r['p10y_hurdles'].items()})}")
print("\nmixture:", json.dumps(conv(mix), indent=0))
print("payout hurdles:", {k: round(v, 4) for k, v in out["payout_hurdles_real_preserving"].items()})
