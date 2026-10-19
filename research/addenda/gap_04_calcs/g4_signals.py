"""gap_04: build daily fragility signals, a real-time regime filter and forward event labels.

Usage: python -I g4_signals.py <data_dir> <cboe_dir> <brent_html> <out_dir>

Outputs (out_dir):
  daily_signals.csv      turbulence (TURB6, TURBX), absorption ratio and standardized shift, daily
  monthly_panel.csv      monthly features and forward event labels
  hmm_filtered.csv       filtered P(crisis) series, one column per annual refit (real-time protocol)
  hmm_meta.json          per-refit state summaries
"""
from __future__ import annotations

import json
import logging
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import logsumexp
from scipy.stats import multivariate_normal

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g4_load as L  # noqa: E402

warnings.filterwarnings("ignore")
logging.getLogger("hmmlearn").setLevel(logging.CRITICAL)


# ----------------------------------------------------------------------------- turbulence
def turbulence(Y: pd.DataFrame, window: int = 1260, min_obs: int = 750) -> pd.Series:
    """Kritzman-Li (2010) turbulence d_t=(y_t-mu)' S^-1 (y_t-mu), mu,S from the trailing window [t-W,t-1]."""
    X = Y.to_numpy(dtype=float)
    T, k = X.shape
    ok = ~np.isnan(X).any(1)
    Xz = np.where(ok[:, None], X, 0.0)
    c1 = np.vstack([np.zeros((1, k)), np.cumsum(Xz, 0)])
    c2 = np.vstack([np.zeros((1, k, k)), np.cumsum(Xz[:, :, None] * Xz[:, None, :], 0)])
    cn = np.concatenate([[0], np.cumsum(ok.astype(int))])
    d = np.full(T, np.nan)
    for t in range(T):
        if not ok[t]:
            continue
        a = max(0, t - window)
        n = cn[t] - cn[a]
        if n < min_obs:
            continue
        s1 = c1[t] - c1[a]
        s2 = c2[t] - c2[a]
        mu = s1 / n
        S = (s2 - n * np.outer(mu, mu)) / (n - 1)
        e = X[t] - mu
        try:
            d[t] = float(e @ np.linalg.solve(S, e))
        except np.linalg.LinAlgError:
            pass
    return pd.Series(d, index=Y.index)


# ----------------------------------------------------------------------------- absorption ratio
def absorption_ratio(R: pd.DataFrame, window: int = 500, half_life: float = 250.0,
                     frac: float = 0.2) -> pd.Series:
    """Kritzman-Li-Page-Rigobon (2011) absorption ratio: share of EW-weighted variance in the top N/5 PCs."""
    X = R.to_numpy(dtype=float)
    T, N = X.shape
    n_eig = int(round(N * frac))
    w = 0.5 ** (np.arange(window)[::-1] / half_life)
    w = w / w.sum()
    out = np.full(T, np.nan)
    for t in range(window - 1, T):
        Z = X[t - window + 1: t + 1]
        if np.isnan(Z).any():
            continue
        m = w @ Z
        Zc = Z - m
        C = (Zc * w[:, None]).T @ Zc
        ev = np.linalg.eigvalsh(C)
        out[t] = ev[-n_eig:].sum() / ev.sum()
    return pd.Series(out, index=R.index)


def ar_shift(ar: pd.Series) -> pd.Series:
    """Standardized shift: (15-day mean AR - 1-year mean AR) / 1-year sd of AR."""
    a15 = ar.rolling(15, min_periods=15).mean()
    a1y = ar.rolling(252, min_periods=200).mean()
    s1y = ar.rolling(252, min_periods=200).std()
    return (a15 - a1y) / s1y


# ----------------------------------------------------------------------------- HMM filter
def fit_hmm(X: np.ndarray, k: int, restarts: int = 8, seed0: int = 0):
    from hmmlearn.hmm import GaussianHMM
    best, best_ll = None, -np.inf
    for s in range(restarts):
        m = GaussianHMM(n_components=k, covariance_type="full", n_iter=300, tol=1e-4,
                        random_state=seed0 + s, min_covar=1e-3, init_params="stmc")
        try:
            m.fit(X)
            ll = m.score(X)
        except Exception:  # noqa: BLE001
            continue
        if np.isfinite(ll) and ll > best_ll:
            best, best_ll = m, ll
    return best, best_ll


def forward_filter(model, X: np.ndarray) -> np.ndarray:
    """Filtered state probabilities P(S_t | x_1..x_t) (forward algorithm only; no smoothing)."""
    k = model.n_components
    logb = np.column_stack([multivariate_normal(model.means_[j], model.covars_[j], allow_singular=True).logpdf(X)
                            for j in range(k)])
    logA = np.log(np.clip(model.transmat_, 1e-300, None))
    la = np.log(np.clip(model.startprob_, 1e-300, None)) + logb[0]
    la -= logsumexp(la)
    out = np.empty((len(X), k))
    out[0] = np.exp(la)
    for t in range(1, len(X)):
        la = logsumexp(la[:, None] + logA, axis=0) + logb[t]
        la -= logsumexp(la)
        out[t] = np.exp(la)
    return out


# ----------------------------------------------------------------------------- labels
def fwd_max_drawdown(level: pd.Series, origins: pd.DatetimeIndex, ndays: int) -> pd.Series:
    """Max drawdown over the next ndays trading days, starting from the close at each origin date."""
    lv = level.to_numpy()
    idx = level.index
    pos = idx.get_indexer(origins, method="pad")
    out = np.full(len(origins), np.nan)
    for i, p in enumerate(pos):
        if p < 0 or p + ndays >= len(lv):
            continue
        path = lv[p: p + ndays + 1]
        peak = np.maximum.accumulate(path)
        out[i] = float(np.max(1 - path / peak))
    return pd.Series(out, index=origins)


def fwd_window_extreme(x: pd.Series, origins: pd.DatetimeIndex, ndays: int, win: int, how: str) -> pd.Series:
    """Extreme (min or max) of the win-day sum of x over windows lying fully inside (origin, origin+ndays]."""
    arr = x.to_numpy()
    idx = x.index
    cs = np.concatenate([[0.0], np.nancumsum(arr)])
    pos = idx.get_indexer(origins, method="pad")
    out = np.full(len(origins), np.nan)
    for i, p in enumerate(pos):
        if p < 0 or p + ndays >= len(arr):
            continue
        starts = np.arange(p + 1, p + ndays - win + 2)
        sums = cs[starts + win] - cs[starts]
        out[i] = float(sums.min() if how == "min" else sums.max())
    return pd.Series(out, index=origins)


def main() -> None:
    data_dir, cboe_dir, brent_html, out_dir = (Path(a) for a in sys.argv[1:5])
    out_dir.mkdir(parents=True, exist_ok=True)
    meta: dict = {}

    ffd = L.ff_daily(data_dir / "ff_daily.zip")
    ffm = L.ff_monthly(data_dir / "ff_monthly.zip")
    ind = L.ff49_daily(data_dir / "ind49_daily.zip")
    gy = L.gsw_yields(data_dir / "feds200628.csv")
    zr = L.zero_returns(gy)
    eb = L.ebp(data_dir / "ebp.csv")
    ipo = L.ipo_monthly(data_dir / "IPOALL.xlsx")
    wti = L.eia_daily(data_dir / "eia_wti_daily.html")
    dev = None
    try:
        import zipfile, re  # noqa: E401
        txt = zipfile.ZipFile(data_dir / "devexus_daily.zip").read(
            zipfile.ZipFile(data_dir / "devexus_daily.zip").namelist()[0]).decode("latin-1")
        recs = []
        for ln in txt.splitlines():
            m = re.match(r"^\s*(\d{8})\s*,(.*)$", ln)
            if m:
                v = [float(x) for x in m.group(2).split(",")[:4]]
                recs.append((pd.Timestamp(m.group(1)), v[0] + v[3]))
        dev = pd.Series(dict(recs)).sort_index() / 100.0
    except Exception as e:  # noqa: BLE001
        meta["devexus_error"] = str(e)

    meta["data_ranges"] = {
        "ff_daily": [str(ffd.index[0].date()), str(ffd.index[-1].date())],
        "ff_monthly": [str(ffm.index[0]), str(ffm.index[-1])],
        "ff49_daily": [str(ind.index[0].date()), str(ind.index[-1].date())],
        "gsw": [str(gy.index[0].date()), str(gy.index[-1].date())],
        "ebp": [str(eb.index[0]), str(eb.index[-1])],
        "ipo": [str(ipo.index[0]), str(ipo.index[-1])],
        "wti": [str(wti.index[0].date()), str(wti.index[-1].date())],
    }

    # ---------------- daily signals
    Y6 = pd.concat([ffd[["mkt_rf", "smb", "hml"]], zr[["z2", "z5", "z10"]]], axis=1, join="inner").dropna()
    turb6 = turbulence(Y6)
    brent = L.eia_daily(brent_html)
    brent = brent[brent > 0]
    oil_r = np.log(brent).diff()
    meta["data_ranges"]["brent"] = [str(brent.index[0].date()), str(brent.index[-1].date())]
    if dev is not None:
        YX = pd.concat([Y6, dev.rename("dev"), oil_r.rename("oil")], axis=1, join="inner").dropna()
        turbx = turbulence(YX)
    else:
        turbx = pd.Series(dtype=float)
    # industries: keep those complete from 1965 onward
    ind65 = ind.loc["1965-01-01":]
    keep = [c for c in ind65.columns if ind65[c].notna().all()]
    meta["ar_industries_kept"] = len(keep)
    meta["ar_industries_dropped"] = [c for c in ind65.columns if c not in keep]
    ar = absorption_ratio(ind65[keep])
    dar = ar_shift(ar)
    daily = pd.concat([turb6.rename("turb6"), turbx.rename("turbx"), ar.rename("ar"), dar.rename("dar")], axis=1)
    daily.to_csv(out_dir / "daily_signals.csv")

    # ---------------- monthly panel
    months = pd.period_range("1963-07", ffm.index[-1], freq="M")
    P = pd.DataFrame(index=months)
    P["mkt_ex"] = ffm["mkt_rf"]
    P["rf"] = ffm["rf"]
    dm = ffd.copy()
    dm["m"] = dm.index.to_period("M")
    rv = dm.groupby("m")["mkt_rf"].apply(lambda s: np.sqrt(252 * np.mean(s.to_numpy() ** 2)))
    P["log_rv"] = np.log(rv)
    y10m = gy["y10"].dropna().groupby(gy["y10"].dropna().index.to_period("M")).last()
    P["y10"] = y10m
    P["dy10"] = y10m.diff()
    P["ebp"] = eb["ebp"]
    P["ebp_l1"] = eb["ebp"].shift(1)
    # month-end daily signals
    def month_end_stat(s: pd.Series, n: int, how: str) -> pd.Series:
        s = s.dropna()
        g = s.groupby(s.index.to_period("M"))
        if how == "logmean":
            return g.apply(lambda x: np.log(x.iloc[-n:].mean()))
        if how == "mean":
            return g.apply(lambda x: x.iloc[-n:].mean())
        return g.last()
    P["turb6"] = month_end_stat(turb6, 21, "logmean")
    P["turbx"] = month_end_stat(turbx, 21, "logmean") if len(turbx) else np.nan
    P["ar"] = month_end_stat(ar, 15, "mean")
    P["dar"] = month_end_stat(dar, 1, "last")
    cpi = L.multpl_cape(data_dir.parent / "data_multpl" / "cpi_by_month.html")
    meta["data_ranges"]["cpi_multpl"] = [str(cpi.index[0]), str(cpi.index[-1])]
    infl = (cpi / cpi.shift(12) - 1.0)
    P["infl_l1"] = infl.shift(1).reindex(months)  # CPI for m-1 is published during month m
    cape = L.multpl_cape(data_dir / "multpl_cape.html")
    P["cape_l1"] = cape.shift(1).reindex(months)
    P["ipo_net"] = ipo["net"]
    P["ipo3"] = P["ipo_net"].rolling(3).sum()
    P["ipo_ratio"] = P["ipo3"] / P["ipo3"].shift(1).rolling(36, min_periods=36).mean()

    # ---------------- forward labels
    origins = pd.DatetimeIndex([dm.index[dm["m"] == m][-1] if (dm["m"] == m).any() else pd.NaT for m in months])
    eq_tr = (1 + ffd["mkt_rf"] + ffd["rf"]).cumprod()
    ex_log = np.log1p(ffd["mkt_rf"])
    valid = ~origins.isna()
    o = origins[valid]
    lab = pd.DataFrame(index=months[valid])
    lab["fmdd63"] = fwd_max_drawdown(eq_tr, o, 63).to_numpy()
    lab["fmdd126"] = fwd_max_drawdown(eq_tr, o, 126).to_numpy()
    lab["min10_eq_21"] = fwd_window_extreme(ex_log, o, 21, 10, "min").to_numpy()
    y10_ff = gy["y10"].dropna().reindex(ffd.index, method="ffill")  # last bond close on/before each equity day
    dy_d = y10_ff.diff().fillna(0.0)
    lab["max10_dy10_21"] = fwd_window_extreme(dy_d, o, 21, 10, "max").to_numpy()
    P = P.join(lab)
    # credit-widening proxy: max(EBP_{m..m+5}) - EBP_{m-1}
    e = eb["ebp"].reindex(months)
    fwdmax = pd.concat([e.shift(-k) for k in range(0, 6)], axis=1).max(axis=1, skipna=False)
    P["debp6"] = fwdmax - e.shift(1)
    # exit-window closure proxy: ipo_ratio falls below 0.5 within the next 6 months, given >=0.5 now
    r = P["ipo_ratio"]
    fwdmin = pd.concat([r.shift(-k) for k in range(1, 7)], axis=1).min(axis=1, skipna=False)
    P["exit_open"] = (r >= 0.5).astype(float).where(r.notna())
    P["ipo_ratio_fmin6"] = fwdmin

    # ---------------- real-time HMM filter (annual refits, expanding window)
    feats3 = ["mkt_ex", "log_rv", "ebp_l1", "dy10"]
    feats4 = feats3 + ["infl_l1"]
    filt_cols, refit_meta = {}, {}
    for K, feats in ((3, feats3), (4, feats4)):
        H = P[feats].dropna()
        meta[f"hmm_sample_K{K}"] = [str(H.index[0]), str(H.index[-1])]
        last_year = int(str(H.index[-1])[:4])
        for Yr in list(range(1990, last_year + 1)) + ["final"]:
            if Yr == "final":
                train = H
                tag = f"K{K}_final"
            else:
                train = H.loc[:f"{Yr - 1}-12"]
                tag = f"K{K}_{Yr}"
            mu, sd = train.mean(), train.std()
            Xtr = ((train - mu) / sd).to_numpy()
            model, ll = fit_hmm(Xtr, K, restarts=10, seed0=0)
            Xall = ((H - mu) / sd).to_numpy()
            fp = forward_filter(model, Xall)
            rv_means = model.means_[:, feats.index("log_rv")]
            order = list(np.argsort(rv_means))  # ascending vol; crisis = last
            crisis = order[-1]
            labels = {crisis: "crisis"}
            if K == 3:
                labels[order[0]], labels[order[1]] = "calm", "elevated"
            else:
                rest = order[:-1]
                infl_j = max(rest, key=lambda j: model.means_[j, feats.index("infl_l1")])
                labels[infl_j] = "inflationary"
                rest2 = [j for j in rest if j != infl_j]
                rec_j = max(rest2, key=lambda j: model.means_[j, feats.index("log_rv")])  # post-stress, elevated vol
                labels[rec_j] = "recovery/elevated"
                labels[[j for j in rest2 if j != rec_j][0]] = "expansion/calm"
            order_lab = sorted(labels, key=lambda j: ["calm", "expansion/calm", "elevated", "recovery/elevated",
                                                      "inflationary", "crisis"].index(labels[j]))
            filt_cols[tag] = pd.Series(fp[:, crisis], index=H.index)
            st = []
            for j in order_lab:
                mj = model.means_[j] * sd.to_numpy() + mu.to_numpy()
                row = {"label": labels[j], "mkt_ex_ann": round(float(mj[0] * 12), 3),
                       "rv_ann": round(float(np.exp(mj[1])), 3), "ebp": round(float(mj[2]), 3),
                       "dy10_pp": round(float(mj[3]), 3), "dur_m": round(float(1 / (1 - model.transmat_[j, j])), 1)}
                if K == 4:
                    row["infl"] = round(float(mj[4]), 3)
                st.append(row)
            refit_meta[tag] = {"loglik": round(float(ll), 1), "states": st,
                               "transmat_ordered": np.round(model.transmat_[np.ix_(order_lab, order_lab)], 4).tolist(),
                               "train_end": str(train.index[-1])}
            if Yr == "final":
                refit_meta[tag]["filtered_last9"] = {str(i): np.round(fp[-9:][n][order_lab], 4).tolist()
                                                     for n, i in enumerate(H.index[-9:])}
                refit_meta[tag]["state_order"] = [labels[j] for j in order_lab]
                refit_meta[tag]["mu"] = mu.round(5).to_dict()
                refit_meta[tag]["sd"] = sd.round(5).to_dict()
                np.savez(out_dir / f"hmm_final_params_K{K}.npz", startprob=model.startprob_,
                         transmat=model.transmat_, means=model.means_, covars=model.covars_,
                         order=np.array(order_lab), mu=mu.to_numpy(), sd=sd.to_numpy(),
                         feats=np.array(feats))
                for j in order_lab:
                    filt_cols[f"{tag}_{labels[j]}"] = pd.Series(fp[:, j], index=H.index)
    pd.DataFrame(filt_cols).to_csv(out_dir / "hmm_filtered.csv")
    meta["hmm_refits"] = refit_meta

    P.to_csv(out_dir / "monthly_panel.csv")
    # basic descriptive stats of labels (full sample and OOS window)
    desc = {}
    oos = P.loc["1990-01":]
    desc["P(fmdd63>=10%)"] = round(float((oos["fmdd63"] >= 0.10).mean()), 3)
    desc["P(fmdd126>=15%)"] = round(float((oos["fmdd126"] >= 0.15).mean()), 3)
    for th in (0.05, 0.06, 0.07):
        desc[f"P(10d eq loss>={th:.0%} in next month)"] = round(float((oos["min10_eq_21"] <= np.log(1 - th)).mean()), 3)
    for th in (0.30, 0.40, 0.50):
        desc[f"P(10d dy10>=+{int(th*100)}bp in next month)"] = round(float((oos["max10_dy10_21"] >= th).mean()), 3)
    for th in (0.3, 0.4, 0.5):
        desc[f"P(dEBP6>={th})"] = round(float((oos["debp6"] >= th).mean()), 3)
    op = oos[oos["exit_open"] == 1]
    desc["exit: share of months open"] = round(float((oos["exit_open"] == 1).mean()), 3)
    desc["P(close within 6m | open)"] = round(float((op["ipo_ratio_fmin6"] < 0.5).mean()), 3)
    meta["label_base_rates_1990on"] = desc
    meta["signal_corr_1990on"] = P.loc["1990-01":, ["log_rv", "turb6", "turbx", "ar", "dar", "ebp_l1"]].corr().round(2).to_dict()
    (out_dir / "signals_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in meta.items() if k != "hmm_refits"}, indent=1))
    print(json.dumps({k: refit_meta.get(k) for k in ("K3_final", "K4_final", "K3_1990", "K4_1990")}, indent=1))


if __name__ == "__main__":
    main()
