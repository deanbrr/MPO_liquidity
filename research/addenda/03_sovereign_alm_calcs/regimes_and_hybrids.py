"""Illustrative calibration helpers for the ADIC sovereign-ALM dossier.

1) Shock-type regime shares from overlapping 12m oil/equity windows (EIA Brent, Ken French US mkt).
2) 3-state Gaussian HMM on monthly (oil, equity) log returns: means, vols, correlations, transitions.
3) Monte Carlo prices (risk-neutral, bivariate GBM) of joint-state hedges vs correlation:
   oil put, equity put, worst-of put, best-of ("dual-down") put, dual digital, oil-conditional equity put.

Usage: python -I regimes_and_hybrids.py <data_dir> <out_dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oil_equity_regimes import parse_eia_daily, parse_ff  # noqa: E402


def shock_regimes(M: pd.DataFrame) -> dict:
    o12 = np.exp(M["oil"].rolling(12).sum()) - 1
    e12 = np.exp(M["us"].rolling(12).sum()) - 1
    J = pd.concat([o12.rename("o"), e12.rename("e")], axis=1).dropna()
    lab = pd.Series("normal", index=J.index)
    lab[(J.o <= -0.20) & (J.e <= -0.10)] = "demand_bust(oil<=-20%,eq<=-10%)"
    lab[(J.o <= -0.20) & (J.e > 0.0)] = "supply_glut(oil<=-20%,eq>0)"
    lab[(J.o >= 0.30) & (J.e < 0.0)] = "supply_spike(oil>=+30%,eq<0)"
    lab[(J.o >= 0.30) & (J.e >= 0.10)] = "demand_boom(oil>=+30%,eq>=+10%)"
    share = lab.value_counts(normalize=True).round(3).to_dict()
    # episodes (first month of each run) per label
    runs = {}
    prev = None
    for per, l in lab.items():
        if l != prev:
            runs.setdefault(l, []).append(str(per))
        prev = l
    return {"share_of_12m_windows": share,
            "episode_starts": {k: v for k, v in runs.items() if k != "normal"},
            "window_range": [str(J.index[0]), str(J.index[-1])]}


def fit_hmm(X: np.ndarray, n_states: int = 3, n_restarts: int = 30) -> dict:
    from hmmlearn.hmm import GaussianHMM
    best, best_ll = None, -np.inf
    for seed in range(n_restarts):
        m = GaussianHMM(n_components=n_states, covariance_type="full", n_iter=500,
                        random_state=seed, tol=1e-5, min_covar=1e-4)
        try:
            m.fit(X)
            ll = m.score(X)
        except Exception:  # noqa: BLE001
            continue
        if ll > best_ll:
            best, best_ll = m, ll
    m = best
    order = np.argsort([np.sqrt(c[0, 0]) for c in m.covars_])  # sort by oil vol
    states = []
    post = m.predict_proba(X)
    for k in order:
        c = m.covars_[k]
        states.append({
            "oil_mean_ann": round(float(m.means_[k][0] * 12), 3),
            "eq_mean_ann": round(float(m.means_[k][1] * 12), 3),
            "oil_vol_ann": round(float(np.sqrt(c[0, 0] * 12)), 3),
            "eq_vol_ann": round(float(np.sqrt(c[1, 1] * 12)), 3),
            "corr": round(float(c[0, 1] / np.sqrt(c[0, 0] * c[1, 1])), 3),
            "stationary_prob": round(float(post[:, k].mean()), 3),
            "expected_duration_months": round(float(1.0 / (1.0 - m.transmat_[k, k])), 1),
        })
    T = m.transmat_[np.ix_(order, order)]
    return {"loglik": round(float(best_ll), 2), "states_sorted_by_oil_vol": states,
            "transmat_monthly": np.round(T, 3).tolist()}


def hybrid_prices(rhos=(-0.4, -0.2, 0.0, 0.3, 0.6), sig_o=0.40, sig_e=0.18, r=0.04, T=1.0,
                  k_o=0.80, k_e=0.90, n=400_000, seed=7) -> dict:
    rng = np.random.default_rng(seed)
    z1 = rng.standard_normal(n)
    z2i = rng.standard_normal(n)
    out = {}
    disc = np.exp(-r * T)
    for rho in rhos:
        z2 = rho * z1 + np.sqrt(1 - rho ** 2) * z2i
        so = np.exp((r - 0.5 * sig_o ** 2) * T + sig_o * np.sqrt(T) * z1)
        se = np.exp((r - 0.5 * sig_e ** 2) * T + sig_e * np.sqrt(T) * z2)
        xo, xe = so / k_o, se / k_e
        pay = {
            "oil_put_80": np.maximum(k_o - so, 0) / k_o,
            "eq_put_90": np.maximum(k_e - se, 0) / k_e,
            "worst_of_put": np.maximum(1 - np.minimum(xo, xe), 0),
            "best_of_put_dual_down": np.maximum(1 - np.maximum(xo, xe), 0),
            "dual_digital": ((so < k_o) & (se < k_e)).astype(float),
            "eq_put_90_if_oil_below_80": (so < k_o) * np.maximum(k_e - se, 0) / k_e,
        }
        out[f"rho={rho:+.1f}"] = {k: round(float(disc * v.mean()), 4) for k, v in pay.items()}
        out[f"rho={rho:+.1f}"]["Q_prob_joint_down"] = round(float(((so < k_o) & (se < k_e)).mean()), 4)
    return {"assumptions": {"sig_oil": sig_o, "sig_eq": sig_e, "r": r, "T_years": T,
                            "oil_strike_pct_spot": k_o, "eq_strike_pct_spot": k_e,
                            "units": "premium as fraction of notional (puts normalised by strike)"},
            "prices": out}


def main() -> None:
    data_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    brent_d = parse_eia_daily(data_dir / "eia_brent_daily.html")
    us = parse_ff(next((data_dir / "ff_us").glob("*.csv"))).sort_index()
    b_me = brent_d.resample("ME").last()
    b_me.index = b_me.index.to_period("M")
    M = pd.concat([np.log(b_me).diff().rename("oil"), np.log1p(us["ret"]).rename("us")], axis=1)
    M = M.sort_index().dropna()
    res = {"sample": [str(M.index[0]), str(M.index[-1])], "n": int(len(M))}
    res["shock_regimes_12m"] = shock_regimes(M)
    W = M[["oil", "us"]].copy()
    lo, hi = W["oil"].quantile([0.01, 0.99])
    W["oil"] = W["oil"].clip(lo, hi)
    res["winsor_oil_bounds_monthly_logret"] = [round(float(lo), 3), round(float(hi), 3)]
    import logging
    logging.getLogger("hmmlearn").setLevel(logging.ERROR)
    res["hmm_2state_winsor"] = fit_hmm(W.to_numpy(), n_states=2)
    res["hmm_3state_winsor"] = fit_hmm(W.to_numpy(), n_states=3)
    if "--skip-hybrids" not in sys.argv:
        res["hybrid_prices_calm_vol"] = hybrid_prices(sig_o=0.35, sig_e=0.16)
        res["hybrid_prices_2026_vol"] = hybrid_prices(sig_o=0.70, sig_e=0.20)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "regimes_and_hybrids.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
