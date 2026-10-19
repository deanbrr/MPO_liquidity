"""gap_04: do valuation, mean-reversion or momentum signals earn a place in the PolicySpec?

Usage: python -I g4_valuation.py <data_dir> <out_dir>
  data_dir: ff_monthly.zip, multpl_cape.html ; out_dir: monthly_panel.csv, hmm_filtered.csv (from g4_signals.py)

(1) Predictive regressions, expanding window from 1929, OOS 1990-01.., purged (train rows s <= m-h):
    Campbell-Thompson OOS R^2 (unrestricted and sign/positivity-restricted) and Clark-West t (Newey-West).
(2) Timing rules on US equity (w in [0.7,1.3], monthly), 1990-01..2026-08: Sharpe, CRRA(3) CE, max DD,
    block-bootstrap CI of the CE difference vs static exposure.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g4_load as L  # noqa: E402
from g4_oos import nw_lrv  # noqa: E402

OOS0 = pd.Period("1990-01", "M")


def cw_test(y, yhat, ybar, h):
    f = (y - ybar) ** 2 - ((y - yhat) ** 2 - (ybar - yhat) ** 2)
    lrv = float(nw_lrv(f.reshape(-1, 1), max(1, int(1.5 * h)))[0, 0])
    se = np.sqrt(max(lrv, 1e-18) / len(f))
    return float(f.mean() / se)


def predictive(M: pd.DataFrame, pred: str, h: int, sign: int):
    y = M["lx"].rolling(h).sum().shift(-h)  # sum over m+1..m+h
    x = M[pred]
    d = pd.concat([y.rename("y"), x.rename("x")], axis=1)
    rows = []
    for m in d.index:
        if m < OOS0 or pd.isna(d.at[m, "y"]) or pd.isna(d.at[m, "x"]):
            continue
        tr = d.loc[:m - h].dropna()
        tr = tr.loc[pd.Period("1929-07", "M"):]
        if len(tr) < 240:
            continue
        X = np.column_stack([np.ones(len(tr)), tr["x"].to_numpy()])
        b = np.linalg.lstsq(X, tr["y"].to_numpy(), rcond=None)[0]
        yhat = b[0] + b[1] * d.at[m, "x"]
        ybar = tr["y"].mean()
        yr = ybar if np.sign(b[1]) != sign else yhat
        yr = max(yr, 0.0)
        rows.append((m, d.at[m, "y"], yhat, yr, ybar, b[1]))
    R = pd.DataFrame(rows, columns=["m", "y", "yhat", "yrestr", "ybar", "slope"]).set_index("m")
    sse_b = ((R.y - R.ybar) ** 2).sum()
    out = {"n": len(R), "window": [str(R.index[0]), str(R.index[-1])],
           "R2os": round(float(1 - ((R.y - R.yhat) ** 2).sum() / sse_b), 4),
           "R2os_restricted": round(float(1 - ((R.y - R.yrestr) ** 2).sum() / sse_b), 4),
           "CW_t": round(cw_test(R.y.to_numpy(), R.yhat.to_numpy(), R.ybar.to_numpy(), h), 2),
           "slope_first_last": [round(float(R.slope.iloc[0]), 4), round(float(R.slope.iloc[-1]), 4)],
           "indep_obs_approx": int(len(R) / h)}
    for nm, (a, b2) in {"1990-2007": ("1990-01", "2007-12"), "2008-on": ("2008-01", "2030-12")}.items():
        s = R.loc[a:b2]
        if len(s) > 12:
            out[f"R2os_{nm}"] = round(float(1 - ((s.y - s.yhat) ** 2).sum() / ((s.y - s.ybar) ** 2).sum()), 4)
    return out


def zexp(s: pd.Series, min_n=120):
    m = s.expanding(min_n).mean()
    sd = s.expanding(min_n).std()
    return (s - m) / sd


def zroll(s: pd.Series, n=360):
    return (s - s.rolling(n, min_periods=240).mean()) / s.rolling(n, min_periods=240).std()


def perf(r_p: pd.Series, rf: pd.Series, gamma=3.0):
    ex = r_p - rf
    ce_m = np.mean((1 + r_p) ** (1 - gamma)) ** (1 / (1 - gamma)) - 1
    idx = (1 + r_p).cumprod()
    mdd = float((1 - idx / idx.cummax()).max())
    return {"ex_ret_ann": float(ex.mean() * 12), "vol_ann": float(ex.std() * np.sqrt(12)),
            "sharpe": float(ex.mean() / ex.std() * np.sqrt(12)), "ce_ann": float((1 + ce_m) ** 12 - 1), "maxdd": mdd}


def ce_boot(r_a, r_b, gamma=3.0, n=2000, block=12, seed=1):
    rng = np.random.default_rng(seed)
    a, b = r_a.to_numpy(), r_b.to_numpy()
    T = len(a)
    nb = int(np.ceil(T / block))
    out = []
    for _ in range(n):
        st = rng.integers(0, T - block + 1, nb)
        ii = np.concatenate([np.arange(s, s + block) for s in st])[:T]
        ca = np.mean((1 + a[ii]) ** (1 - gamma)) ** (1 / (1 - gamma))
        cb = np.mean((1 + b[ii]) ** (1 - gamma)) ** (1 / (1 - gamma))
        out.append((ca ** 12 - cb ** 12) * 1e4)
    return np.percentile(out, [5, 50, 95]).round(0).tolist(), float(np.mean(np.array(out) > 0))


def main():
    data_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    ffm = L.ff_monthly(data_dir / "ff_monthly.zip")
    cape = L.multpl_cape(data_dir / "multpl_cape.html")
    M = pd.DataFrame(index=ffm.index)
    M["mkt_ex"], M["rf"] = ffm["mkt_rf"], ffm["rf"]
    M["lx"] = np.log1p(M.mkt_ex + M.rf) - np.log1p(M.rf)
    M["logcape_l1"] = np.log(cape).shift(1).reindex(M.index)
    tr = (1 + M.mkt_ex + M.rf).cumprod()
    M["mr36"] = M["lx"].rolling(36).sum()
    M["dd36"] = 1 - tr / tr.rolling(36).max()
    M["mom12"] = M["lx"].rolling(12).sum()
    res = {"cape_latest_multpl": cape.attrs.get("latest"),
           "cape_percentile_since_1881_at_2026-09": round(float((cape.loc["1881-01":"2026-09"] <=
                                                                cape.loc["2026-09"]).mean()), 3)}
    # (1) predictive regressions
    P = {}
    for pred, sign in (("logcape_l1", -1), ("mr36", -1), ("dd36", +1), ("mom12", +1)):
        for h in (1, 12, 36, 60):
            P[f"{pred}_h{h}"] = predictive(M, pred, h, sign)
    res["predictive_oos"] = P
    # (2) timing rules
    panel = pd.read_csv(out_dir / "monthly_panel.csv", index_col=0)
    panel.index = pd.PeriodIndex(panel.index, freq="M")
    F = pd.read_csv(out_dir / "hmm_filtered.csv", index_col=0)
    F.index = pd.PeriodIndex(F.index, freq="M")
    crisis_rt = pd.Series({m: F.at[m, f"K3_{m.year}"] if f"K3_{m.year}" in F.columns else np.nan
                           for m in F.index if m >= OOS0})
    cape_full = np.log(cape).shift(1)
    zV = zexp(cape_full).reindex(M.index)
    zV30 = zroll(cape_full).reindex(M.index)
    zDD = zexp(M["dd36"])
    zMOM = zexp(M["mom12"])
    turb = panel["turb6"]
    zT = ((turb - turb.expanding(120).mean()) / turb.expanding(120).std()).reindex(M.index)
    c = lambda z, lo=-2, hi=2: z.clip(lo, hi)  # noqa: E731
    W = pd.DataFrame(index=M.index)
    W["static"] = 1.0
    W["VAL_exp"] = 1 - 0.15 * c(zV)
    W["VAL_30y"] = 1 - 0.15 * c(zV30)
    W["MR_dd"] = 1 + 0.15 * c(zDD)
    W["MOM12"] = 1 + 0.15 * c(zMOM)
    W["VAL+MOM"] = 1 + 0.075 * (c(-zV) + c(zMOM))
    W["CRISIS_derisk"] = 1 - 0.30 * crisis_rt.reindex(M.index)
    W["TURB_derisk"] = 1 - 0.15 * c(zT, 0, 2)
    W = W.clip(0.7, 1.3)
    sl = slice(OOS0, M.index[-1])
    nxt = M[["mkt_ex", "rf"]].shift(-1)  # weight set at end of m applies to month m+1
    perfs, rets = {}, {}
    for k in W.columns:
        w = W[k].loc[sl]
        rr = (nxt["rf"] + w * nxt["mkt_ex"]).loc[sl].dropna()
        rets[k] = rr
        perfs[k] = {kk: round(v, 4) for kk, v in perf(rr, nxt["rf"].loc[rr.index]).items()}
        perfs[k]["avg_w"] = round(float(w.loc[rr.index].mean()), 3)
    for k in W.columns:
        if k == "static":
            continue
        ci, pg = ce_boot(rets[k], rets["static"].loc[rets[k].index])
        perfs[k]["dCE_bp_vs_static_ci90"] = ci
        perfs[k]["P(dCE>0)_boot"] = round(pg, 3)
        perfs[k]["dCE_bp_point"] = round((perfs[k]["ce_ann"] - perfs["static"]["ce_ann"]) * 1e4, 0)
        perfs[k]["dSharpe"] = round(perfs[k]["sharpe"] - perfs["static"]["sharpe"], 3)
    res["timing_rules_1990on"] = perfs
    res["timing_window"] = [str(rets["static"].index[0]), str(rets["static"].index[-1])]
    res["n_variants_tested"] = len(W.columns) - 1
    (out_dir / "valuation_results.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
