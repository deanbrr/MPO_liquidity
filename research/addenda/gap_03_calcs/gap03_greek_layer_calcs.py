"""gap_03 calcs: public-data calibration facts for the overlay factor/Greek layer.

All outputs are [I-calc] on public data (Cboe, ICE MOVE via Yahoo, Fed GSW, EIA).
Nothing here is ADIC data.

A. VIX term-structure betas: dX_T = a + b * dVIX for X in {VIX9D, VIX3M, VIX6M, VIX1Y},
   on all days, on vol-spike days and on SPX <= -2% days, plus episode ratios
   (change in X / change in VIX from pre-spike low to VIX peak).
   Use: converts tenor vega into "VIX-equivalent" vega for net-vega netting.
B. Short-variance proxy P&L by regime conditioning. Non-overlapping 21-trading-day
   blocks; strike K = VIX at block start; RV from the next 21 SPX log returns;
   P&L per unit vega notional = (K^2 - RV^2) / (2K) vol points. Grouped by the
   V-label (C3 thresholds 14.3 / 18.4 / 24.4 / 45) at entry, at exit and by the
   maximum label inside the block. Averaged over the 21 block offsets.
   Use: tests the C3 short-vol Sharpe template (0.9 / 0.6 / 0.0 / -2.0).
C. Rates spot-vol: d ln MOVE on d y10 (GSW par yield, bp) by episode and year.
D. Oil spot-vol: d OVX on Brent daily log return, split into up and down days,
   by episode.

Usage (paths as arguments; run with python -I):
  python -I gap03_greek_layer_calcs.py --vix .. --vix9d .. --vix3m .. --vix6m ..
      --vix1y .. --spx .. --move .. --gsw .. --ovx .. --brent .. --out ..
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

V_THRESH = [14.3, 18.4, 24.4, 45.0]  # C3 V-label thresholds (V0..V4)
V_NAMES = ["V0", "V1", "V2", "V3", "V4"]
TEMPLATE_SHORT_VOL = {"V0": 0.9, "V1": 0.6, "V2": 0.0, "V3": -2.0}  # C3 §5.3f [I]


def read_cboe(path: str, col: str | None = None) -> pd.Series:
    df = pd.read_csv(path)
    df.columns = [c.strip().upper() for c in df.columns]
    date = pd.to_datetime(df["DATE"], format="%m/%d/%Y")
    use = col.upper() if col else ("CLOSE" if "CLOSE" in df.columns else df.columns[1])
    s = pd.Series(df[use].astype(float).values, index=date).sort_index()
    s = s[~s.index.duplicated(keep="last")]
    return s[s > 0]


def read_move(path: str) -> pd.Series:
    js = json.loads(Path(path).read_text(encoding="utf-8"))
    res = js["chart"]["result"][0]
    ts = pd.to_datetime(res["timestamp"], unit="s", utc=True).tz_convert("America/New_York")
    idx = ts.normalize().tz_localize(None)
    close = res["indicators"]["quote"][0]["close"]
    s = pd.Series(close, index=idx, dtype="float64").dropna()
    s = s[~s.index.duplicated(keep="last")].sort_index()
    return s[s > 0]


def read_gsw(path: str, col: str = "SVENPY10") -> pd.Series:
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("Date,"))
    from io import StringIO
    df = pd.read_csv(StringIO("\n".join(lines[start:])), na_values=["NA"])
    s = pd.Series(df[col].values, index=pd.to_datetime(df["Date"])).astype(float).dropna()
    return s.sort_index()


MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


def read_eia_daily(path: str) -> pd.Series:
    """Same parser as research/addenda/03_sovereign_alm_calcs/oil_equity_regimes.py."""
    html = Path(path).read_text(encoding="utf-8", errors="replace")
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
                out[pd.Timestamp(start + dt.timedelta(days=i))] = float(v)
    return pd.Series(out).sort_index()


def ols(y: np.ndarray, x: np.ndarray) -> dict:
    """OLS of y on [1, x] (x may be 2-D). Returns coefficients, R2, n."""
    y = np.asarray(y, float)
    X = np.asarray(x, float)
    if X.ndim == 1:
        X = X[:, None]
    ok = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    y, X = y[ok], X[ok]
    n = len(y)
    if n < 8:
        return {"n": int(n)}
    A = np.column_stack([np.ones(n), X])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    r2 = 1 - resid.var() / y.var() if y.var() > 0 else float("nan")
    # HC0 robust standard errors
    xtx_inv = np.linalg.inv(A.T @ A)
    meat = (A * resid[:, None]).T @ (A * resid[:, None])
    se = np.sqrt(np.diag(xtx_inv @ meat @ xtx_inv))
    return {"n": int(n), "coef": [round(float(c), 4) for c in coef],
            "se_hc0": [round(float(s), 4) for s in se], "r2": round(float(r2), 3)}


def vlabel(v: float) -> str:
    for th, name in zip(V_THRESH, V_NAMES):
        if v < th:
            return name
    return V_NAMES[-1]


# ----------------------------------------------------------------------------- A
def part_a(vix, vix9d, vix3m, vix6m, vix1y, spx) -> dict:
    out = {"pairwise": {}, "episodes": {}}
    r_spx = np.log(spx).diff()
    tenors = {"VIX9D": vix9d, "VIX3M": vix3m, "VIX6M": vix6m, "VIX1Y": vix1y}
    for name, x in tenors.items():
        df = pd.concat({"vix": vix, "x": x, "r": r_spx}, axis=1).dropna()
        d = df[["vix", "x"]].diff()
        d["r"] = df["r"]
        d["lab"] = df["vix"].shift(1).map(lambda v: vlabel(v) if pd.notna(v) else None)
        d = d.dropna()
        res = {"sample": [str(d.index[0].date()), str(d.index[-1].date())],
               "all_days": ols(d["x"].values, d["vix"].values),
               "vix_up_ge3": ols(d.loc[d["vix"] >= 3, "x"].values, d.loc[d["vix"] >= 3, "vix"].values),
               "spx_le_m2pct": ols(d.loc[d["r"] <= np.log(0.98), "x"].values,
                                   d.loc[d["r"] <= np.log(0.98), "vix"].values)}
        by_lab = {}
        for lab in V_NAMES:
            sub = d[d["lab"] == lab]
            if len(sub) >= 30:
                by_lab[lab] = ols(sub["x"].values, sub["vix"].values)
        res["by_prior_vlabel"] = by_lab
        out["pairwise"][name] = res

    # Episode ratios: change from pre-peak low (30 trading days) to VIX peak
    episodes = {
        "2008_GFC": ("2008-09-01", "2008-12-31"),
        "2018_Feb_shortvol_unwind": ("2018-01-25", "2018-02-12"),
        "2020_COVID": ("2020-02-10", "2020-04-15"),
        "2022_grind_H1": ("2022-01-03", "2022-03-31"),
        "2024_Aug_carry_unwind": ("2024-07-20", "2024-08-15"),
        "2025_Apr_tariff": ("2025-03-25", "2025-04-30"),
        "2026_Mar": ("2026-02-15", "2026-04-15"),
    }
    full = pd.concat({"VIX": vix, **tenors}, axis=1)
    for ep, (a, b) in episodes.items():
        w = full.loc[a:b, "VIX"].dropna()
        if w.empty:
            continue
        peak_d = w.idxmax()
        pre = full.loc[:peak_d, "VIX"].dropna().iloc[-31:]
        low_d = pre.idxmin()
        rec = {"low_date": str(low_d.date()), "peak_date": str(peak_d.date()),
               "VIX_low": round(float(full.at[low_d, "VIX"]), 2),
               "VIX_peak": round(float(full.at[peak_d, "VIX"]), 2)}
        dv = full.at[peak_d, "VIX"] - full.at[low_d, "VIX"]
        for name in tenors:
            x0, x1 = full.at[low_d, name], full.at[peak_d, name]
            if pd.notna(x0) and pd.notna(x1) and dv != 0:
                rec[f"{name}_low"] = round(float(x0), 2)
                rec[f"{name}_peak"] = round(float(x1), 2)
                rec[f"ratio_d{name}_dVIX"] = round(float((x1 - x0) / dv), 3)
        out["episodes"][ep] = rec
    return out


# ----------------------------------------------------------------------------- B
def part_b(vix, spx, block=21) -> dict:
    df = pd.concat({"vix": vix, "spx": spx}, axis=1).dropna()
    r = np.log(df["spx"]).diff().values
    v = df["vix"].values
    n = len(df)
    recs = []
    for off in range(block):
        for s in range(off, n - block - 1, block):
            k = v[s]
            rets = r[s + 1: s + 1 + block]
            if np.any(~np.isfinite(rets)):
                continue
            rv = np.sqrt(252.0 / block * np.sum(rets ** 2)) * 100.0
            pnl = (k * k - rv * rv) / (2.0 * k)
            recs.append({"off": off, "date": df.index[s], "K": k, "RV": rv, "pnl": pnl,
                         "entry": vlabel(k), "exit": vlabel(v[s + block]),
                         "max": vlabel(np.max(v[s: s + block + 1]))})
    R = pd.DataFrame(recs)

    def stats(sub: pd.DataFrame) -> dict:
        # statistics per offset, then averaged across offsets (each offset = non-overlapping)
        per = []
        for _, g in sub.groupby("off"):
            if len(g) < 6:
                continue
            m, sd = g["pnl"].mean(), g["pnl"].std(ddof=1)
            per.append((len(g), m, sd, m / sd * np.sqrt(12) if sd > 0 else np.nan,
                        float(pd.Series(g["pnl"]).skew())))
        if not per:
            return {}
        P = np.array(per, float)
        return {"n_blocks_per_offset": round(float(P[:, 0].mean()), 1),
                "mean_volpts": round(float(np.nanmean(P[:, 1])), 2),
                "sd_volpts": round(float(np.nanmean(P[:, 2])), 2),
                "sharpe_ann": round(float(np.nanmean(P[:, 3])), 2),
                "skew": round(float(np.nanmean(P[:, 4])), 2)}

    out = {"sample": [str(df.index[0].date()), str(df.index[-1].date())],
           "unconditional": stats(R),
           "template_C3": TEMPLATE_SHORT_VOL}
    for cond in ["entry", "exit", "max"]:
        out[f"by_{cond}_label"] = {lab: stats(R[R[cond] == lab]) for lab in V_NAMES
                                   if (R[cond] == lab).sum() >= 6 * block}
    # Transition decomposition: entered <= V2 and touched >= V3 inside block
    trans = R[(R["entry"].isin(["V0", "V1", "V2"])) & (R["max"].isin(["V3", "V4"]))]
    stay3 = R[(R["entry"].isin(["V3", "V4"]))]
    out["entered_calm_touched_V3plus"] = stats(trans)
    out["entered_V3plus"] = stats(stay3)
    out["share_blocks_entered_calm_touched_V3plus"] = round(float(len(trans) / len(R)), 4)
    worst = R.sort_values("pnl").drop_duplicates("date").head(6)
    out["worst_blocks"] = [{"start": str(d.date()), "K": round(float(k), 2), "RV": round(float(rv), 1),
                            "pnl_volpts": round(float(p), 1)}
                           for d, k, rv, p in zip(worst["date"], worst["K"], worst["RV"], worst["pnl"])]
    return out


# ----------------------------------------------------------------------------- C
def part_c(move: pd.Series, y10: pd.Series) -> dict:
    df = pd.concat({"move": move, "y": y10}, axis=1).dropna()
    d = pd.DataFrame({"dlnm": np.log(df["move"]).diff(), "dy_bp": df["y"].diff() * 100.0}).dropna()
    # guard against bad prints (Yahoo occasionally has zero/garbage)
    d = d[d["dlnm"].abs() < 0.5]
    out = {"sample": [str(d.index[0].date()), str(d.index[-1].date())],
           "note": "slope = change in ln MOVE per +1bp in GSW 10y par yield; x1000 gives % per 10bp"}
    windows = {"full": (None, None), "2008_GFC_Sep_Dec": ("2008-09-01", "2008-12-31"),
               "2020_COVID_Feb19_Apr30": ("2020-02-19", "2020-04-30"),
               "2022_Jan_Oct": ("2022-01-03", "2022-10-31"),
               "2023_Mar_SVB": ("2023-03-01", "2023-03-31")}
    for k, (a, b) in windows.items():
        sub = d.loc[a:b] if a else d
        o = ols(sub["dlnm"].values, sub["dy_bp"].values)
        o["corr"] = round(float(sub["dlnm"].corr(sub["dy_bp"])), 3)
        o["pct_move_per_10bp"] = round(o["coef"][1] * 1000, 2) if "coef" in o else None
        out[k] = o
    yearly = {}
    for yr, g in d.groupby(d.index.year):
        if len(g) > 100:
            yearly[int(yr)] = round(float(g["dlnm"].corr(g["dy_bp"])), 3)
    out["corr_by_year"] = yearly
    out["share_years_positive_corr"] = round(float(np.mean([c > 0 for c in yearly.values()])), 3)
    peaks = {}
    for k, (a, b) in list(windows.items())[1:]:
        w = df.loc[a:b, "move"]
        peaks[k] = {"peak": round(float(w.max()), 1), "date": str(w.idxmax().date()),
                    "start": round(float(w.iloc[0]), 1)}
    out["move_peaks"] = peaks
    out["move_last"] = {"date": str(df.index[-1].date()), "value": round(float(df["move"].iloc[-1]), 1)}
    return out


# ----------------------------------------------------------------------------- D
def part_d(ovx: pd.Series, brent: pd.Series, vix: pd.Series) -> dict:
    df = pd.concat({"ovx": ovx, "b": brent}, axis=1).dropna()
    df = df[df["b"] > 0]
    d = pd.DataFrame({"dovx": df["ovx"].diff(), "r": np.log(df["b"]).diff() * 100.0}).dropna()
    d = d[d["r"].abs() < 40]
    d["rp"] = d["r"].clip(lower=0)
    d["rn"] = d["r"].clip(upper=0)
    out = {"sample": [str(d.index[0].date()), str(d.index[-1].date())],
           "note": ("piecewise OLS dOVX = a + s_up*max(r,0) + s_dn*min(r,0); r = Brent daily log return in %. "
                    "s_dn < 0 means vol rises on down days (put-skew dynamics); s_up > 0 means vol rises on "
                    "up days (call-skew dynamics). OVX is on USO (WTI) options; Brent is a proxy underlying.")}
    windows = {"full": (None, None), "2014_16_glut": ("2014-07-01", "2016-02-29"),
               "2020_demand_bust": ("2020-02-19", "2020-05-29"),
               "2022_supply_shock": ("2022-02-24", "2022-06-30"),
               "2026_YTD": ("2026-01-01", "2026-10-16")}
    for k, (a, b) in windows.items():
        sub = d.loc[a:b] if a else d
        o = ols(sub["dovx"].values, sub[["rp", "rn"]].values)
        if "coef" in o:
            o["s_up"], o["s_dn"] = o["coef"][1], o["coef"][2]
        out[k] = o
    lv = ovx.dropna()
    out["ovx_stats"] = {"median": round(float(lv.median()), 1), "p95": round(float(lv.quantile(0.95)), 1),
                        "max": round(float(lv.max()), 1), "max_date": str(lv.idxmax().date()),
                        "last": round(float(lv.iloc[-1]), 1), "last_date": str(lv.index[-1].date())}
    ratio = pd.concat({"ovx": ovx, "vix": vix}, axis=1).dropna()
    rr = ratio["ovx"] / ratio["vix"]
    out["ovx_over_vix"] = {"median": round(float(rr.median()), 2), "p10": round(float(rr.quantile(0.1)), 2),
                           "p90": round(float(rr.quantile(0.9)), 2),
                           "2026_YTD_median": round(float(rr.loc["2026-01-01":].median()), 2)}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    for k in ["vix", "vix9d", "vix3m", "vix6m", "vix1y", "spx", "move", "gsw", "ovx", "brent", "out"]:
        ap.add_argument(f"--{k}", required=True)
    a = ap.parse_args()
    vix = read_cboe(a.vix)
    spx = read_cboe(a.spx, "SPX")
    res = {"generated": "2026-10-18", "is_synthetic": False, "data_note": "public market data; not ADIC data"}
    res["A_term_structure_betas"] = part_a(vix, read_cboe(a.vix9d), read_cboe(a.vix3m),
                                           read_cboe(a.vix6m), read_cboe(a.vix1y), spx)
    res["B_short_variance_by_regime"] = part_b(vix, spx)
    res["C_rates_spot_vol"] = part_c(read_move(a.move), read_gsw(a.gsw))
    res["D_oil_spot_vol"] = part_d(read_cboe(a.ovx, "OVX"), read_eia_daily(a.brent), vix)
    Path(a.out).write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
