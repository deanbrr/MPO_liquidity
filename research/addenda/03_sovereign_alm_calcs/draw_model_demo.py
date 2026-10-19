"""Illustrative regime chain + clipped distribution-demand model (defaults for the dossier).

All parameters are *priors for discussion*, derived from public data where noted
(IMF UAE Article IV Dec-2025: breakeven 44.8 USD/bbl for 2026, hydrocarbon revenue ~11.3% GDP;
IMF DataMapper fiscal balance history; EIA Brent), not ADIC data.

Usage: python -I draw_model_demo.py <out_dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

STATES = ["N", "B", "SG", "DB", "SS", "GW"]
# Annual transition prior (rows = from, cols = to). Expert-set; see dossier section 6.3.
P = np.array([
    # N     B     SG    DB    SS    GW
    [0.62, 0.15, 0.10, 0.05, 0.04, 0.04],  # N  normal
    [0.40, 0.40, 0.05, 0.06, 0.07, 0.02],  # B  demand boom
    [0.38, 0.12, 0.42, 0.04, 0.02, 0.02],  # SG supply glut / price war
    [0.35, 0.30, 0.20, 0.10, 0.03, 0.02],  # DB demand bust (oil down, equities down, exits shut)
    [0.30, 0.05, 0.10, 0.35, 0.15, 0.05],  # SS global supply spike / stagflation
    [0.30, 0.05, 0.35, 0.05, 0.05, 0.20],  # GW Gulf war / export-volume shock
])
assert np.allclose(P.sum(1), 1.0)

# Regime-conditional annual oil log-change mean / sd and owner fiscal add-on (pp of GDP)
OIL = {"N": (0.00, 0.20), "B": (0.20, 0.20), "SG": (-0.35, 0.20), "DB": (-0.45, 0.25),
       "SS": (0.30, 0.25), "GW": (0.10, 0.30)}
KAPPA = 0.40  # annual mean-reversion speed of log price toward the long-run anchor
P_LR = 70.0   # long-run anchor (USD/bbl, nominal) - prior, to be replaced by curve/ET overlay
FISCAL_ADDON = {"N": 0.0, "B": 0.0, "SG": -0.5, "DB": -1.5, "SS": -0.5, "GW": -6.0}
P_BE, H_SHARE = 44.8, 11.0          # IMF consolidated UAE breakeven (2026) and hydrocarbon rev % GDP
D_CENTER, D_SLOPE, RHO = 7.5, 0.625, 0.5  # draw rate (% NAV) = clip(center - slope*FB, 5, 10), smoothed
D_MIN, D_MAX = 5.0, 10.0


def stationary(T: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eig(T.T)
    s = np.real(v[:, np.argmin(np.abs(w - 1))])
    return s / s.sum()


def simulate(n_paths=200_000, years=10, p0=126.0, s0="GW", d0=6.5, seed=11,
             p_be=None, slope=None):
    p_be = P_BE if p_be is None else p_be
    slope = D_SLOPE if slope is None else slope
    rng = np.random.default_rng(seed)
    idx = {s: i for i, s in enumerate(STATES)}
    s = np.full(n_paths, idx[s0])
    logp = np.full(n_paths, np.log(p0))
    d_prev = np.full(n_paths, d0)
    cum = np.cumsum(P, axis=1)
    out_d = np.empty((years, n_paths))
    out_s = np.empty((years, n_paths), dtype=int)
    out_p = np.empty((years, n_paths))
    for t in range(years):
        u = rng.random(n_paths)
        s = (u[:, None] > cum[s]).sum(1)
        mu = np.array([OIL[x][0] for x in STATES])[s]
        sd = np.array([OIL[x][1] for x in STATES])[s]
        # mean reversion of log price toward log(70) in long run (equilibrium prior)
        logp = logp + KAPPA * (np.log(P_LR) - logp) + mu + sd * rng.standard_normal(n_paths)
        price = np.exp(logp)
        fb = H_SHARE * np.log(price / p_be) + np.array([FISCAL_ADDON[x] for x in STATES])[s]
        d_star = np.clip(D_CENTER - slope * fb, D_MIN, D_MAX)
        d = np.clip(RHO * d_prev + (1 - RHO) * d_star, D_MIN, D_MAX)
        out_d[t], out_s[t], out_p[t] = d, s, price
        d_prev = d
    return out_d, out_s, out_p


def main() -> None:
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    st = stationary(P)
    dur = 1 / (1 - np.diag(P))
    d, s, p = simulate()
    res = {
        "stationary": dict(zip(STATES, np.round(st, 3).tolist())),
        "expected_duration_years": dict(zip(STATES, np.round(dur, 2).tolist())),
        "kinks_usd_bbl": {"draw_at_floor_if_P_ge": round(P_BE * np.exp((D_CENTER - D_MIN) / D_SLOPE / H_SHARE), 1),
                          "draw_at_cap_if_P_le": round(P_BE * np.exp(-(D_MAX - D_CENTER) / D_SLOPE / H_SHARE), 1)},
        "draw_rate_by_regime_pctNAV": {},
        "P(draw>=9.5%) by year": [round(float((d[t] >= 9.5).mean()), 3) for t in range(d.shape[0])],
        "P(>=3 consecutive years with draw>=9.5%) within 10y": None,
        "mean_draw_by_year": [round(float(d[t].mean()), 2) for t in range(d.shape[0])],
        "p10_p50_p90_price_y1_y3": {f"y{t+1}": np.round(np.percentile(p[t], [10, 50, 90]), 1).tolist()
                                    for t in (0, 2)},
    }
    for i, name in enumerate(STATES):
        m = s == i
        if m.any():
            res["draw_rate_by_regime_pctNAV"][name] = {
                "mean": round(float(d[m].mean()), 2),
                "p90": round(float(np.percentile(d[m], 90)), 2),
                "share_at_or_above_9.5": round(float((d[m] >= 9.5).mean()), 3)}
    hi = d >= 9.5
    run = np.zeros(d.shape[1], dtype=int)
    best = np.zeros(d.shape[1], dtype=int)
    for t in range(d.shape[0]):
        run = np.where(hi[t], run + 1, 0)
        best = np.maximum(best, run)
    res["P(>=3 consecutive years with draw>=9.5%) within 10y"] = round(float((best >= 3).mean()), 3)
    # put-spread equivalence: dollars of extra draw per $1/bbl between kinks, per $1bn NAV
    k_hi, k_lo = res["kinks_usd_bbl"]["draw_at_floor_if_P_ge"], res["kinks_usd_bbl"]["draw_at_cap_if_P_le"]
    res["put_spread_equivalent"] = {
        "note": "linear-in-price approximation between kinks; draw is linear in log price in the model",
        "extra_draw_per_usd_bbl_per_1bn_NAV_musd": round(1000 * (D_MAX - D_MIN) / 100 / (k_hi - k_lo), 2),
        "barrels_equiv_for_177bn_NAV_million": round(177e9 * (D_MAX - D_MIN) / 100 / (k_hi - k_lo) / 1e6, 0)}
    # Sensitivity grid: owner breakeven and draw slope (the two least-known, most important inputs)
    grid = {}
    for p_be in (44.8, 55.0, 65.0):
        for slope in (0.625, 1.0):
            dd, ss, _ = simulate(n_paths=100_000, p_be=p_be, slope=slope, seed=5)
            hi2 = dd >= 9.5
            r2 = np.zeros(dd.shape[1], dtype=int)
            b2 = np.zeros(dd.shape[1], dtype=int)
            for t in range(dd.shape[0]):
                r2 = np.where(hi2[t], r2 + 1, 0)
                b2 = np.maximum(b2, r2)
            db = ss == STATES.index("DB")
            sg = ss == STATES.index("SG")
            grid[f"P_BE={p_be},slope={slope}"] = {
                "mean_draw_10y": round(float(dd.mean()), 2),
                "P(draw>=9.5%) avg yrs4-10": round(float(hi2[3:].mean()), 3),
                "P(>=3 consec yrs >=9.5%) in 10y": round(float((b2 >= 3).mean()), 3),
                "mean_draw_in_DB": round(float(dd[db].mean()), 2),
                "mean_draw_in_SG": round(float(dd[sg].mean()), 2)}
    res["sensitivity_grid"] = grid
    (out_dir / "draw_model_demo.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
