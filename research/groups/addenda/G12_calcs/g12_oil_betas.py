"""G12 (Real Assets: energy, natural resources, agriculture, timber) - listed-proxy oil loadings.

[I-calc] on public data. Outputs are illustrative estimates on LISTED US industry portfolios,
used only as priors for the SYNTHETIC Real Assets book. Not ADIC data.

Inputs (downloaded public data, treated as untrusted and parsed defensively):
  - EIA Europe Brent spot FOB, daily (RBRTE, HTML table)        -> eia_brent_daily.html
  - Ken French 49 Industry Portfolios, monthly, value-weighted  -> ind49.zip
  - Ken French F-F Research Data Factors, monthly               -> ff3.zip

Usage: python -I g12_oil_betas.py <data_dir> <out_json>
"""
from __future__ import annotations

import datetime as dt
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}

INDUSTRIES = ["Oil", "Coal", "Mines", "Gold", "Agric", "Paper", "Util", "Trans", "RlEst", "Chems", "Steel"]


def parse_eia_daily(path: Path) -> pd.Series:
    html = path.read_text(encoding="utf-8", errors="replace")
    rows = re.findall(r"<tr>(.*?)</tr>", html, flags=re.S)
    out = {}
    for row in rows:
        lab = re.search(r"class='B6'>(?:&nbsp;)*\s*(\d{4})\s+([A-Za-z]{3})-\s*(\d{1,2})\s+to", row)
        if not lab:
            continue
        year, mon, day = int(lab.group(1)), MONTHS[lab.group(2)], int(lab.group(3))
        start = dt.date(year, mon, day)
        vals = re.findall(r"class='B3'>([^<]*)</td>", row)
        for i, v in enumerate(vals[:5]):
            v = v.strip()
            if v:
                try:
                    out[pd.Timestamp(start + dt.timedelta(days=i))] = float(v)
                except ValueError:
                    continue
    s = pd.Series(out).sort_index()
    s.name = "brent"
    return s


def read_zip_csv(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if not names:
            raise ValueError("no csv in zip")
        raw = z.read(names[0])
    return raw.decode("utf-8", errors="replace")


def parse_ff_first_monthly_block(text: str) -> pd.DataFrame:
    """Return the first monthly block (YYYYMM rows) with its header."""
    lines = text.splitlines()
    header = None
    recs = []
    started = False
    for i, line in enumerate(lines):
        parts = [p.strip() for p in line.split(",")]
        if not started:
            if len(parts) > 3 and re.fullmatch(r"\d{6}", parts[0] or ""):
                # header is the closest previous non-empty line with names
                j = i - 1
                while j >= 0 and not lines[j].strip():
                    j -= 1
                header = [h.strip() for h in lines[j].split(",")]
                started = True
            else:
                continue
        if started:
            if len(parts) > 1 and re.fullmatch(r"\d{6}", parts[0] or ""):
                recs.append(parts)
            else:
                break
    cols = ["m"] + header[1:len(recs[0])]
    df = pd.DataFrame(recs, columns=cols[:len(recs[0])])
    df["m"] = df["m"].map(lambda x: pd.Period(x[:4] + "-" + x[4:], "M"))
    df = df.set_index("m")
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.mask(df <= -99)
    return df / 100.0


def ols_nw(y: np.ndarray, X: np.ndarray, lags: int = 3):
    """OLS with Newey-West standard errors. X must include a constant column."""
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        w = 1.0 - L / (lags + 1.0)
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None])
        S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.diag(V))
    r2 = 1.0 - (e @ e) / np.sum((y - y.mean()) ** 2)
    return b, se, r2


def window_stats(M: pd.DataFrame, start: str, end: str) -> dict:
    W = M.loc[pd.Period(start, "M"):pd.Period(end, "M")].dropna(subset=["oil", "mkt_ex"])
    out = {"n_months": int(len(W)), "start": start, "end": end}
    for ind in INDUSTRIES:
        col = f"{ind}_ex"
        J = W[["oil", "mkt_ex", col]].dropna()
        if len(J) < 24:
            continue
        y = J[col].values
        X1 = np.column_stack([np.ones(len(J)), J["oil"].values])
        X2 = np.column_stack([np.ones(len(J)), J["mkt_ex"].values, J["oil"].values])
        b1, se1, r21 = ols_nw(y, X1)
        b2, se2, r22 = ols_nw(y, X2)
        down = J[J["oil"] <= -0.10]
        up = J[J["oil"] >= 0.10]
        out[ind] = {
            "corr_oil": round(float(np.corrcoef(J["oil"], J[col])[0, 1]), 3),
            "beta_oil_univ": round(float(b1[1]), 3), "se_univ": round(float(se1[1]), 3),
            "beta_mkt": round(float(b2[1]), 3), "beta_oil_partial": round(float(b2[2]), 3),
            "se_oil_partial": round(float(se2[2]), 3), "r2_two_factor": round(float(r22), 3),
            "ann_vol": round(float(J[col].std() * np.sqrt(12)), 3),
            "mean_ret_oil_down10_months": round(float(down[col].mean()), 4) if len(down) else None,
            "n_oil_down10": int(len(down)),
            "mean_ret_oil_up10_months": round(float(up[col].mean()), 4) if len(up) else None,
            "n_oil_up10": int(len(up)),
        }
    return out


def label_shock_types(M: pd.DataFrame) -> pd.Series:
    """Stream-03 sign rules on overlapping 12-month windows (log returns)."""
    o12 = M["oil"].rolling(12).sum()
    e12 = M["mkt_tot"].rolling(12).sum()
    lab = pd.Series("N", index=M.index)
    lab[(o12 <= np.log(0.8)) & (e12 <= np.log(0.9))] = "DB"
    lab[(o12 <= np.log(0.8)) & (e12 > 0)] = "SG"
    lab[(o12 >= np.log(1.3)) & (e12 < 0)] = "SS"
    lab[(o12 >= np.log(1.3)) & (e12 >= np.log(1.1))] = "B"
    lab[o12.isna() | e12.isna()] = np.nan
    return lab


def main() -> None:
    data_dir, out_json = Path(sys.argv[1]), Path(sys.argv[2])
    brent_d = parse_eia_daily(data_dir / "eia_brent_daily.html")
    ind = parse_ff_first_monthly_block(read_zip_csv(data_dir / "ind49.zip"))
    ff3 = parse_ff_first_monthly_block(read_zip_csv(data_dir / "ff3.zip"))

    b_me = brent_d.resample("ME").last()
    b_me.index = b_me.index.to_period("M")
    r_oil = np.log(b_me).diff().rename("oil")

    M = pd.DataFrame(index=ind.index)
    M["rf"] = ff3["RF"]
    M["mkt_ex"] = np.log1p(ff3["Mkt-RF"] + ff3["RF"]) - np.log1p(ff3["RF"])
    M["mkt_tot"] = np.log1p(ff3["Mkt-RF"] + ff3["RF"])
    for c in INDUSTRIES:
        if c not in ind.columns:
            raise KeyError(c)
        M[f"{c}_ex"] = np.log1p(ind[c]) - np.log1p(ff3["RF"])
        M[f"{c}_tot"] = np.log1p(ind[c])
    M = M.join(r_oil, how="left").sort_index()

    res: dict = {
        "label": "SYNTHETIC-ADJACENT [I-calc] on public data: listed US industry proxies; not ADIC data",
        "as_of": {"brent_last_date": str(brent_d.index[-1].date()), "brent_last": float(brent_d.iloc[-1]),
                  "ff_industry_last": str(ind.dropna(how="all").index[-1]), "ff3_last": str(ff3.index[-1])},
        "windows": {},
    }
    windows = {
        "1988-2007": ("1988-01", "2007-12"), "2008-2019": ("2008-01", "2019-12"),
        "2020-2026": ("2020-01", "2026-12"), "full_1988-2026": ("1988-01", "2026-12"),
        "oil_bust_2014-07_2016-02": ("2014-07", "2016-02"), "covid_2020-01_2020-06": ("2020-01", "2020-06"),
        "war_2026-03_latest": ("2026-03", "2026-12"),
    }
    for k, (a, b) in windows.items():
        res["windows"][k] = window_stats(M, a, b)

    # Shock-type conditional 12-month relative returns (industry minus market), overlapping windows
    lab = label_shock_types(M)
    rel = {}
    for c in INDUSTRIES:
        r12 = (M[f"{c}_tot"].rolling(12).sum() - M["mkt_tot"].rolling(12).sum())
        a12 = M[f"{c}_tot"].rolling(12).sum()
        d = {}
        for z in ["N", "B", "SG", "DB", "SS"]:
            sel = (lab == z) & r12.notna()
            if sel.sum() > 0:
                d[z] = {"n_windows": int(sel.sum()),
                        "mean_12m_rel_vs_mkt": round(float(np.expm1(r12[sel]).mean()), 4),
                        "mean_12m_abs": round(float(np.expm1(a12[sel]).mean()), 4)}
        rel[c] = d
    shares = lab.loc[pd.Period("1988-12", "M"):].value_counts(normalize=True).round(4).to_dict()
    res["shock_type_12m"] = {"label_shares_since_1988": shares, "industry_rel_returns": rel}

    # Drawdowns (total return index, log-cum) for oil-linked proxies since 1988
    dd = {}
    for c in ["Oil", "Coal", "Mines", "Gold", "Agric", "Paper", "Util"]:
        x = M.loc[pd.Period("1988-01", "M"):, f"{c}_tot"].dropna().cumsum()
        peak = x.cummax()
        ddser = np.expm1(x - peak)
        trough = ddser.idxmin()
        dd[c] = {"max_drawdown": round(float(ddser.min()), 3), "trough": str(trough)}
    x = M.loc[pd.Period("1988-01", "M"):, "oil"].dropna().cumsum()
    dd["Brent"] = {"max_drawdown": round(float(np.expm1(x - x.cummax()).min()), 3),
                   "trough": str(np.expm1(x - x.cummax()).idxmin())}
    res["max_drawdowns_since_1988"] = dd

    # Calendar-year returns for owner-beta analysis
    yr = M.loc[pd.Period("1988-01", "M"):].copy()
    yr["year"] = [p.year for p in yr.index]
    annual = yr.groupby("year").agg({**{f"{c}_tot": "sum" for c in INDUSTRIES}, "mkt_tot": "sum", "oil": "sum"})
    annual = annual[annual.index <= 2025]
    brent_avg = brent_d.groupby(brent_d.index.year).mean()
    annual["brent_avg"] = brent_avg.reindex(annual.index)
    res["annual_table"] = {int(y): {k: round(float(v), 4) for k, v in row.items()} for y, row in annual.iterrows()}
    out_json.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("wrote", out_json)


if __name__ == "__main__":
    main()
