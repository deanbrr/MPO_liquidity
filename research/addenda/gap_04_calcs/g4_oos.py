"""gap_04: out-of-sample, purged and embargoed test of fragility candidates vs the regime posterior.

Usage: python -I g4_oos.py <out_dir>   (reads monthly_panel.csv and hmm_filtered.csv written by g4_signals.py)

Protocol (pre-registered in the addendum):
  * Origins m = 1990-01 .. last labelled month. Forecast P(event in (m, m+h]) from information at end of month m.
  * Training rows s satisfy s <= m - h - e (purge: label observed; embargo e = 3 months), expanding from a
    common start so nested models share identical training rows.
  * The regime posterior at every row comes from the HMM refit at the start of year(m) on data to Dec(year-1),
    filtered (forward recursion only). Turbulence and absorption ratio use trailing windows only.
  * Logistic regression (L2, C=1) on training-standardised features; refit every month.
  * Scores: Brier, log score, AUC. Paired log-score differences tested with HAC (Newey-West) t-stats;
    moving-block bootstrap (12m blocks) for Brier/AUC deltas; Holm over the primary family.
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


def nw_lrv(u: np.ndarray, lags: int) -> np.ndarray:
    """Newey-West (Bartlett) long-run covariance of the rows of u (T x k), demeaned."""
    u = np.atleast_2d(u.T).T
    u = u - u.mean(0)
    T = len(u)
    S = u.T @ u / T
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1)
        G = u[l:].T @ u[:-l] / T
        S += w * (G + G.T)
    return S

warnings.filterwarnings("ignore")
EMBARGO = 3
OOS_START = pd.Period("1990-01", "M")


def logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


def load(out_dir: Path):
    P = pd.read_csv(out_dir / "monthly_panel.csv", index_col=0)
    P.index = pd.PeriodIndex(P.index, freq="M")
    F = pd.read_csv(out_dir / "hmm_filtered.csv", index_col=0)
    F.index = pd.PeriodIndex(F.index, freq="M")
    return P, F


def targets(P: pd.DataFrame) -> dict:
    T = {}
    T["DD3"] = ((P["fmdd63"] >= 0.10).astype(float).where(P["fmdd63"].notna()), 3)
    T["DD6"] = ((P["fmdd126"] >= 0.15).astype(float).where(P["fmdd126"].notna()), 6)
    vm_eq = (P["min10_eq_21"] <= np.log(1 - 0.07))
    vm_rt = (P["max10_dy10_21"] >= 0.40)
    ok = P["min10_eq_21"].notna() & P["max10_dy10_21"].notna()
    T["VM1"] = ((vm_eq | vm_rt).astype(float).where(ok), 1)
    T["VMEQ1"] = (vm_eq.astype(float).where(ok), 1)
    T["VMRT1"] = (vm_rt.astype(float).where(ok), 1)
    T["CRED6"] = ((P["debp6"] >= 0.5).astype(float).where(P["debp6"].notna()), 6)
    ex = ((P["ipo_ratio_fmin6"] < 0.5).astype(float)).where(P["ipo_ratio_fmin6"].notna() & (P["exit_open"] == 1))
    T["EXIT6"] = (ex, 6)
    return T


MODELS = {
    "M0": [],
    "RV": ["log_rv"],
    "C": ["crisis"],
    "C+T": ["crisis", "turb6"],
    "C+A": ["crisis", "ar", "dar"],
    "C+T+A": ["crisis", "turb6", "ar", "dar"],
    "T": ["turb6"],
    "A": ["ar", "dar"],
    "C+RV": ["crisis", "log_rv"],
}
MODELS_X = {"C": ["crisis"], "C+TX": ["crisis", "turbx"], "M0": []}


def walk_forward(P, F, y: pd.Series, h: int, models: dict, hmm_prefix: str, start_train: str,
                 oos_start=OOS_START):
    idx = y.dropna().index
    origins = [m for m in idx if m >= oos_start]
    preds = {k: {} for k in models}
    for m in origins:
        yr = m.year
        col = f"{hmm_prefix}_{yr}" if f"{hmm_prefix}_{yr}" in F.columns else f"{hmm_prefix}_final"
        crisis = logit(F[col])
        X = P.copy()
        X["crisis"] = crisis.reindex(P.index)
        cutoff = m - h - EMBARGO
        tr_idx = [s for s in idx if pd.Period(start_train, "M") <= s <= cutoff]
        for name, feats in models.items():
            ytr = y.loc[tr_idx]
            if not feats:
                preds[name][m] = float(ytr.mean())
                continue
            Xtr = X.loc[tr_idx, feats]
            ok = Xtr.notna().all(1)
            Xtr, ytr2 = Xtr[ok], ytr[ok]
            xt = X.loc[[m], feats]
            if xt.isna().any(axis=None) or ytr2.nunique() < 2:
                preds[name][m] = np.nan
                continue
            mu, sd = Xtr.mean(), Xtr.std().replace(0, 1)
            clf = LogisticRegression(C=1.0, max_iter=2000)
            clf.fit(((Xtr - mu) / sd).to_numpy(), ytr2.to_numpy())
            preds[name][m] = float(clf.predict_proba(((xt - mu) / sd).to_numpy())[0, 1])
    out = pd.DataFrame({k: pd.Series(v) for k, v in preds.items()})
    out["y"] = y.reindex(out.index)
    return out.dropna()


def scores(df: pd.DataFrame, name: str) -> dict:
    y, p = df["y"].to_numpy(), np.clip(df[name].to_numpy(), 1e-4, 1 - 1e-4)
    brier = float(np.mean((p - y) ** 2))
    ll = float(np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
    auc = float(roc_auc_score(y, p)) if 0 < y.mean() < 1 else np.nan
    return {"brier": brier, "logscore": ll, "auc": auc}


def hac_t(d: np.ndarray, lags: int):
    T = len(d)
    lrv = float(nw_lrv(d.reshape(-1, 1), lags)[0, 0])
    se = np.sqrt(max(lrv, 1e-18) / T)
    m = float(d.mean())
    return m, float(se), float(m / se)


def block_boot(df, a, b, n=1000, block=12, seed=0):
    rng = np.random.default_rng(seed)
    T = len(df)
    y = df["y"].to_numpy()
    pa, pb = df[a].to_numpy(), df[b].to_numpy()
    dB, dA = [], []
    nb = int(np.ceil(T / block))
    for _ in range(n):
        st = rng.integers(0, T - block + 1, nb)
        ii = np.concatenate([np.arange(s, s + block) for s in st])[:T]
        yy = y[ii]
        dB.append(np.mean((pa[ii] - yy) ** 2) - np.mean((pb[ii] - yy) ** 2))
        if 0 < yy.mean() < 1:
            dA.append(roc_auc_score(yy, pa[ii]) - roc_auc_score(yy, pb[ii]))
    return (np.percentile(dB, [5, 95]).round(4).tolist(), np.percentile(dA, [5, 95]).round(3).tolist())


def compare(df, a, b, h):
    ya = df["y"].to_numpy()
    pa = np.clip(df[a].to_numpy(), 1e-4, 1 - 1e-4)
    pb = np.clip(df[b].to_numpy(), 1e-4, 1 - 1e-4)
    la = ya * np.log(pa) + (1 - ya) * np.log(1 - pa)
    lb = ya * np.log(pb) + (1 - ya) * np.log(1 - pb)
    d = la - lb
    mean, se, t = hac_t(d, lags=2 * h + EMBARGO)
    from scipy.stats import norm
    p_one = float(1 - norm.cdf(t))
    sub = {}
    for nm, (s0, s1) in {"1990-2007": ("1990-01", "2007-12"), "2008-2026": ("2008-01", "2026-12")}.items():
        sl = df.loc[s0:s1]
        if len(sl) > 24 and 0 < sl["y"].mean() < 1:
            sa, sb = scores(sl, a), scores(sl, b)
            sub[nm] = {"dlog": round(sa["logscore"] - sb["logscore"], 4), "dbrier": round(sa["brier"] - sb["brier"], 4),
                       "dauc": round(sa["auc"] - sb["auc"], 3), "n": len(sl), "events": int(sl["y"].sum())}
    ciB, ciA = block_boot(df, a, b)
    return {"dlog_mean": round(mean, 4), "dlog_hac_t": round(t, 2), "p_one_sided": round(p_one, 4),
            "dbrier_ci90": ciB, "dauc_ci90": ciA, "subperiods": sub}


def holm(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    adj, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        adj[k] = round(run, 4)
    return adj


def in_sample_hac(P, F, y, h, feats, hmm_col="K3_final", start="1975-01"):
    X = P.copy()
    X["crisis"] = logit(F[hmm_col]).reindex(P.index)
    d = pd.concat([y.rename("y"), X[feats]], axis=1).loc[start:].dropna()
    Z = ((d[feats] - d[feats].mean()) / d[feats].std()).to_numpy()
    yy = d["y"].to_numpy()
    clf = LogisticRegression(penalty=None, max_iter=5000).fit(Z, yy)
    Xc = np.column_stack([np.ones(len(Z)), Z])
    beta = np.concatenate([clf.intercept_, clf.coef_[0]])
    p = 1 / (1 + np.exp(-Xc @ beta))
    Hm = (Xc * (p * (1 - p))[:, None]).T @ Xc / len(yy)
    scores_ = Xc * (yy - p)[:, None]
    S = nw_lrv(scores_, 2 * h + 3)
    Hi = np.linalg.inv(Hm)
    V = Hi @ S @ Hi / len(yy)
    se = np.sqrt(np.diag(V))
    return {f: {"coef": round(float(beta[i + 1]), 3), "z": round(float(beta[i + 1] / se[i + 1]), 2)}
            for i, f in enumerate(feats)}


def main():
    out_dir = Path(sys.argv[1])
    P, F = load(out_dir)
    T = targets(P)
    res = {"protocol": {"embargo_months": EMBARGO, "oos_start": str(OOS_START), "train_start": "1975-01",
                        "logistic_C": 1.0, "hac_lags": "2h+3"}}
    primary = ["DD3", "VM1", "CRED6", "EXIT6"]
    secondary = ["DD6", "VMEQ1", "VMRT1"]
    preds_all = {}
    for hmm_prefix in ("K3", "K4"):
        R = {}
        for tname in primary + secondary:
            y, h = T[tname]
            df = walk_forward(P, F, y, h, MODELS, hmm_prefix, "1975-01")
            preds_all[(hmm_prefix, tname)] = df
            sc = {k: {kk: round(vv, 4) for kk, vv in scores(df, k).items()} for k in MODELS}
            clim = sc["M0"]["brier"]
            for k in sc:
                sc[k]["bss_vs_clim"] = round(1 - sc[k]["brier"] / clim, 4)
            comps = {}
            for a, b in (("C+T", "C"), ("C+A", "C"), ("C+T+A", "C"), ("C", "M0"), ("C", "RV"),
                         ("C+RV", "C"), ("T", "C"), ("A", "M0"), ("T", "M0"), ("RV", "M0")):
                comps[f"{a} vs {b}"] = compare(df, a, b, h)
            R[tname] = {"h": h, "n_oos": len(df), "events_oos": int(df["y"].sum()),
                        "base_rate_oos": round(float(df["y"].mean()), 3),
                        "oos_window": [str(df.index[0]), str(df.index[-1])], "scores": sc, "comparisons": comps}
        fam = {f"{t}:{c}": R[t]["comparisons"][c]["p_one_sided"] for t in primary
               for c in ("C+T vs C", "C+A vs C", "C+T+A vs C")}
        R["holm_primary_family"] = holm(fam)
        res[f"baseline_{hmm_prefix}"] = R
    # robustness: cross-asset turbulence incl. ex-US equity and Brent (available later)
    rob = {}
    for tname in primary:
        y, h = T[tname]
        df = walk_forward(P, F, y, h, MODELS_X, "K3", "1993-07", oos_start=pd.Period("1998-01", "M"))
        rob[tname] = {"n_oos": len(df), "events": int(df["y"].sum()),
                      "scores": {k: {kk: round(vv, 4) for kk, vv in scores(df, k).items()} for k in MODELS_X},
                      "C+TX vs C": compare(df, "C+TX", "C", h)}
    res["robustness_turbx_1998on"] = rob
    # in-sample HAC logit (encompassing) on the final filter
    ins = {}
    for tname in primary:
        y, h = T[tname]
        ins[tname] = in_sample_hac(P, F, y, h, ["crisis", "turb6", "ar", "dar"])
    res["in_sample_hac_logit_K3final_1975on"] = ins
    # episodes: OOS predictions (K3 baseline) at dates the IC would recognise
    ep_dates = ["2007-07", "2008-06", "2008-08", "2011-06", "2015-07", "2018-09", "2019-12", "2020-01",
                "2020-02", "2021-12", "2022-03", "2022-06", "2025-02", "2026-02", "2026-03", "2026-05"]
    eps = {}
    for tname in primary:
        df = preds_all[("K3", tname)]
        eps[tname] = {d: {k: round(float(df.loc[pd.Period(d, "M"), k]), 3) for k in ("M0", "C", "C+T", "C+A", "y")}
                      for d in ep_dates if pd.Period(d, "M") in df.index}
    res["episodes_K3"] = eps
    # save predictions
    for (hp, tname), df in preds_all.items():
        df.to_csv(out_dir / f"oos_pred_{hp}_{tname}.csv")
    (out_dir / "oos_results.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    # compact print
    for hp in ("K3", "K4"):
        R = res[f"baseline_{hp}"]
        print(f"===== baseline {hp} =====")
        for tname in primary + secondary:
            r = R[tname]
            line = {k: (r["scores"][k]["bss_vs_clim"], r["scores"][k]["auc"]) for k in ("RV", "C", "C+T", "C+A", "C+T+A", "T")}
            print(tname, "n", r["n_oos"], "ev", r["events_oos"], "base", r["base_rate_oos"], "BSS/AUC", line)
            for c in ("C+T vs C", "C+A vs C", "C+T+A vs C", "C vs M0", "C vs RV", "C+RV vs C"):
                cc = r["comparisons"][c]
                print("    ", c, "dlog", cc["dlog_mean"], "t", cc["dlog_hac_t"], "p", cc["p_one_sided"],
                      "dBrierCI", cc["dbrier_ci90"], "dAUCci", cc["dauc_ci90"], "sub", cc["subperiods"])
        print("Holm:", R["holm_primary_family"])
    print("robustness TURBX:", json.dumps(rob, indent=0)[:3000])
    print("in-sample:", json.dumps(ins))


if __name__ == "__main__":
    main()
