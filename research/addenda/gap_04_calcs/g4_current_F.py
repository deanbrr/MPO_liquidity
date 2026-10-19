"""gap_04: current F_t (Aug/Sep 2026), calibration of the selected model, and light thresholds.

Usage: python -I g4_current_F.py <out_dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g4_oos import load, targets, logit, EMBARGO  # noqa: E402


def fwd_crisis_prob(pi, A, crisis, h):
    k = len(pi)
    keep = [j for j in range(k) if j != crisis]
    v = np.ones(len(keep))
    Ann = A[np.ix_(keep, keep)]
    for _ in range(h - 1):
        v = Ann @ v
    return float(1 - sum(pi[i] * (A[i, keep] @ v) for i in range(k)))


def main():
    out_dir = Path(sys.argv[1])
    P, F = load(out_dir)
    T = targets(P)
    z = np.load(out_dir / "hmm_final_params_K3.npz", allow_pickle=True)
    order = list(z["order"])
    A = z["transmat"][np.ix_(order, order)]
    res = {}
    # model-internal forward crisis probability, real-time series (annual refits) -> use the refit-year transition
    # matrices is heavy; here: final-parameter series for distribution/thresholds and current value
    pc = F["K3_final"]
    pel = F["K3_final_elevated"] if "K3_final_elevated" in F.columns else None
    pcalm = F["K3_final_calm"]
    Fm = pd.Series([fwd_crisis_prob(np.array([pcalm[m], pel[m], pc[m]]), A, 2, 3) for m in pc.index], index=pc.index)
    res["F_model_h3_percentiles_1990on"] = {f"p{q}": round(float(np.percentile(Fm.loc['1990-01':], q)), 3)
                                            for q in (10, 25, 50, 75, 90, 95, 99)}
    res["F_model_h3_latest"] = {str(m): round(float(Fm[m]), 4) for m in Fm.index[-8:]}
    init = json.loads((out_dir / "initial_state_results.json").read_text())
    pis = init["pi0"]["K3"]["pi0_2026-09"]
    pi_sep = np.array([pis["calm"], pis["elevated"], pis["crisis"]])
    res["F_model_h3_2026-09"] = round(fwd_crisis_prob(pi_sep, A, 2, 3), 4)
    # calibrated probabilities from the C model (logistic on logit crisis posterior), trained on all labelled rows
    X = logit(pc).reindex(P.index)
    cur = {}
    for tname in ("DD3", "VM1", "CRED6", "EXIT6"):
        y, h = T[tname]
        lab = y.dropna()
        tr = lab.loc["1975-01":lab.index[-1]]
        xtr = X.reindex(tr.index)
        ok = xtr.notna()
        mu, sd = xtr[ok].mean(), xtr[ok].std()
        clf = LogisticRegression(C=1.0, max_iter=2000).fit(((xtr[ok] - mu) / sd).to_numpy().reshape(-1, 1), tr[ok].to_numpy())
        def prob(xv):
            return float(clf.predict_proba(np.array([[(xv - mu) / sd]]))[0, 1])
        cur[tname] = {"base_rate_1975on": round(float(tr.mean()), 3), "P_2026-08": round(prob(float(X.loc[pd.Period('2026-08', 'M')])), 3),
                      "P_2026-09_ext": round(prob(float(logit(pd.Series([pis['crisis']])).iloc[0])), 3),
                      "P_if_crisis_posterior=0.5": round(prob(0.0), 3), "P_if_crisis_posterior=0.9": round(prob(float(np.log(9))), 3)}
    res["calibrated_C_model_current"] = cur
    # reliability of OOS C-model predictions (K3 baseline) for DD3 and VM1, by bins
    rel = {}
    for tname in ("DD3", "VM1", "CRED6", "EXIT6"):
        df = pd.read_csv(out_dir / f"oos_pred_K3_{tname}.csv", index_col=0)
        bins = [0, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0]
        df["bin"] = pd.cut(df["C"], bins)
        g = df.groupby("bin", observed=True).agg(n=("y", "size"), mean_p=("C", "mean"), freq=("y", "mean"))
        rel[tname] = {str(k): {"n": int(r.n), "mean_p": round(float(r.mean_p), 3), "obs_freq": round(float(r.freq), 3)}
                      for k, r in g.iterrows()}
        # light shares with thresholds relative to base rate
        b = float(df["M0"].iloc[-1])
        green = (df["C"] < 1.25 * b).mean()
        red = (df["C"] >= 2.0 * b).mean()
        rel[tname]["light_shares(green<1.25x base, red>=2x base)"] = {"green": round(float(green), 3),
                                                                      "amber": round(float(1 - green - red), 3),
                                                                      "red": round(float(red), 3)}
        rel[tname]["event_rate_by_light"] = {
            "green": round(float(df.loc[df["C"] < 1.25 * b, "y"].mean()), 3),
            "amber": round(float(df.loc[(df["C"] >= 1.25 * b) & (df["C"] < 2 * b), "y"].mean()), 3) if ((df["C"] >= 1.25 * b) & (df["C"] < 2 * b)).any() else None,
            "red": round(float(df.loc[df["C"] >= 2 * b, "y"].mean()), 3) if (df["C"] >= 2 * b).any() else None}
    res["reliability_oos_K3_C"] = rel
    (out_dir / "current_F_results.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
