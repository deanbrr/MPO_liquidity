"""Oil / equity regime statistics for the ADIC sovereign-ALM dossier.

Inputs (downloaded public data, treated as untrusted and parsed defensively):
  - EIA Europe Brent spot FOB, daily (RBRTE, HTML table)
  - Ken French US Research Factors (Mkt-RF, RF) monthly CSV
  - Ken French Developed Markets 3 factors monthly CSV
  - CBOE VIX daily history CSV

Usage: python -I oil_equity_regimes.py <data_dir> <out_dir>
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


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
                out[pd.Timestamp(start + dt.timedelta(days=i))] = float(v)
    s = pd.Series(out).sort_index()
    s.name = "brent"
    return s


def parse_ff(path: Path) -> pd.DataFrame:
    recs = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 5 and re.fullmatch(r"\d{6}", parts[0]):
            try:
                mkt_rf, rf = float(parts[1]), float(parts[4])
            except ValueError:
                continue
            if mkt_rf <= -99 or rf <= -99:
                continue
            recs.append((pd.Period(parts[0][:4] + "-" + parts[0][4:], "M"), mkt_rf, rf))
        elif recs and len(parts) >= 1 and parts[0] and re.fullmatch(r"\d{4}", parts[0]):
            break  # annual block starts: stop after monthly block
    df = pd.DataFrame(recs, columns=["m", "mkt_rf", "rf"]).drop_duplicates("m").set_index("m")
    df["ret"] = (df["mkt_rf"] + df["rf"]) / 100.0
    return df


def parse_vix(path: Path) -> pd.Series:
    df = pd.read_csv(path)
    df["DATE"] = pd.to_datetime(df["DATE"], format="%m/%d/%Y")
    return df.set_index("DATE")["CLOSE"].astype(float)


def corr(a: pd.Series, b: pd.Series) -> float:
    j = pd.concat([a, b], axis=1).dropna()
    return float(j.corr().iloc[0, 1]) if len(j) > 5 else float("nan")


def tail_dep(a: pd.Series, b: pd.Series, q: float = 0.10) -> float:
    j = pd.concat([a, b], axis=1).dropna()
    qa, qb = j.iloc[:, 0].quantile(q), j.iloc[:, 1].quantile(q)
    both = ((j.iloc[:, 0] <= qa) & (j.iloc[:, 1] <= qb)).sum()
    return float(both / max(1, (j.iloc[:, 0] <= qa).sum()))


def main() -> None:
    data_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    brent_d = parse_eia_daily(data_dir / "eia_brent_daily.html")
    us = parse_ff(next((data_dir / "ff_us").glob("*.csv")))
    dev = parse_ff(next((data_dir / "ff_dev").glob("*.csv")))
    vix_d = parse_vix(data_dir / "vix_history.csv")

    res: dict = {"as_of": {
        "brent_last_date": str(brent_d.index[-1].date()), "brent_last": float(brent_d.iloc[-1]),
        "ff_us_last": str(us.index[-1]), "ff_dev_last": str(dev.index[-1]),
        "vix_last_date": str(vix_d.index[-1].date()), "vix_last": float(vix_d.iloc[-1])}}

    # Month-end Brent and monthly log returns
    b_me = brent_d.resample("ME").last()
    b_me.index = b_me.index.to_period("M")
    b_avg = brent_d.resample("ME").mean()
    b_avg.index = b_avg.index.to_period("M")
    r_oil = np.log(b_me).diff().rename("oil")
    r_us = np.log1p(us["ret"]).rename("us")
    r_dev = np.log1p(dev["ret"]).rename("dev")
    v_me = vix_d.resample("ME").last()
    v_me.index = v_me.index.to_period("M")
    dv = v_me.diff().rename("dvix")
    M = pd.concat([r_oil, r_us, r_dev, dv], axis=1).sort_index()
    us = us.sort_index()
    dev = dev.sort_index()
    b_me = b_me.sort_index()
    b_avg = b_avg.sort_index()
    v_me = v_me.sort_index()

    periods = {
        "1988-2007": ("1988-01", "2007-12"), "2008-2019": ("2008-01", "2019-12"),
        "2020-2026": ("2020-01", "2026-12"), "full_1988-2026": ("1988-01", "2026-12"),
        "GFC_2008-07_2009-03": ("2008-07", "2009-03"), "OilBust_2014-07_2016-02": ("2014-07", "2016-02"),
        "Covid_2020-01_2020-06": ("2020-01", "2020-06"), "Infl_2022-01_2022-12": ("2022-01", "2022-12"),
        "War_2026-03_2026-08": ("2026-03", "2026-08"), "2023-2025": ("2023-01", "2025-12"),
    }
    pstats = {}
    for name, (a, b) in periods.items():
        sl = M.loc[a:b]
        pstats[name] = {
            "n_months": int(sl["oil"].notna().sum()),
            "corr_oil_us": round(corr(sl["oil"], sl["us"]), 3),
            "corr_oil_dev": round(corr(sl["oil"], sl["dev"]), 3),
            "corr_oil_dvix": round(corr(sl["oil"], sl["dvix"]), 3),
            "oil_vol_ann": round(float(sl["oil"].std() * np.sqrt(12)), 3),
            "us_vol_ann": round(float(sl["us"].std() * np.sqrt(12)), 3),
            "oil_cum_logret": round(float(sl["oil"].sum()), 3),
            "us_cum_logret": round(float(sl["us"].sum()), 3),
        }
    res["period_stats"] = pstats

    # Lower-tail dependence (monthly) by era
    res["lower_tail_dep_q10"] = {
        k: round(tail_dep(M.loc[a:b, "oil"], M.loc[a:b, "us"], 0.10), 3)
        for k, (a, b) in {"1988-2007": ("1988-01", "2007-12"), "2008-2026": ("2008-01", "2026-12"),
                          "full": ("1988-01", "2026-12")}.items()}

    # Rolling 36m correlation summary
    roll = M["oil"].rolling(36).corr(M["us"])
    res["rolling36_corr_oil_us"] = {
        "min": round(float(roll.min()), 3), "min_at": str(roll.idxmin()),
        "max": round(float(roll.max()), 3), "max_at": str(roll.idxmax()),
        "last": round(float(roll.dropna().iloc[-1]), 3), "last_at": str(roll.dropna().index[-1]),
        "share_positive_pre2008": round(float((roll.loc[:"2007-12"].dropna() > 0).mean()), 3),
        "share_positive_post2008": round(float((roll.loc["2008-01":].dropna() > 0).mean()), 3)}

    # Calendar-year table: Brent (Dec-to-Dec month-end) vs US equity total return
    yb = b_me[b_me.index.month == 12]
    years = {}
    for y in range(1988, 2026):
        try:
            oil_y = float(yb.loc[pd.Period(f"{y}-12", "M")] / yb.loc[pd.Period(f"{y-1}-12", "M")] - 1)
        except KeyError:
            continue
        us_y = float(np.prod(1 + us.loc[f"{y}-01":f"{y}-12", "ret"]) - 1)
        years[y] = {"brent_chg": round(oil_y, 3), "us_eq_ret": round(us_y, 3),
                    "brent_avg": round(float(b_avg.loc[f"{y}-01":f"{y}-12"].mean()), 2)}
    res["calendar_years"] = years
    yy = pd.DataFrame(years).T
    q = {
        "oil_down_eq_down": int(((yy.brent_chg < 0) & (yy.us_eq_ret < 0)).sum()),
        "oil_down_eq_up": int(((yy.brent_chg < 0) & (yy.us_eq_ret >= 0)).sum()),
        "oil_up_eq_down": int(((yy.brent_chg >= 0) & (yy.us_eq_ret < 0)).sum()),
        "oil_up_eq_up": int(((yy.brent_chg >= 0) & (yy.us_eq_ret >= 0)).sum()),
        "n_years": int(len(yy)),
        "years_brent_drop_ge30pct": [int(y) for y in yy.index[yy.brent_chg <= -0.30]],
        "years_brent_drop_ge20pct": [int(y) for y in yy.index[yy.brent_chg <= -0.20]],
        "years_brent_rise_ge40pct": [int(y) for y in yy.index[yy.brent_chg >= 0.40]],
    }
    res["calendar_year_quadrants"] = q

    # Overlapping 12m windows: conditional probabilities
    oil12 = np.exp(M["oil"].rolling(12).sum()) - 1
    us12 = np.exp(M["us"].rolling(12).sum()) - 1
    J = pd.concat([oil12.rename("o"), us12.rename("e")], axis=1).dropna()
    def cp(cond, event):
        c = J[cond(J)]
        return {"n_cond": int(len(c)), "p": round(float(event(c).mean()), 3) if len(c) else None}
    res["overlapping_12m"] = {
        "P(oil12<-30%)": round(float((J.o < -0.30).mean()), 3),
        "P(oil12<-40%)": round(float((J.o < -0.40).mean()), 3),
        "P(oil12>+50%)": round(float((J.o > 0.50).mean()), 3),
        "P(eq12<-10%)": round(float((J.e < -0.10).mean()), 3),
        "P(eq12<-10% | oil12<-30%)": cp(lambda d: d.o < -0.30, lambda c: c.e < -0.10),
        "P(eq12<-20% | oil12<-30%)": cp(lambda d: d.o < -0.30, lambda c: c.e < -0.20),
        "P(oil12<-30% | eq12<-20%)": cp(lambda d: d.e < -0.20, lambda c: c.o < -0.30),
        "P(eq12<-10% | oil12>+50%)": cp(lambda d: d.o > 0.50, lambda c: c.e < -0.10),
    }
    # Same split by era
    for era, (a, b) in {"pre2008": ("1988-01", "2007-12"), "post2008": ("2008-01", "2026-12")}.items():
        Je = J.loc[a:b]
        c = Je[Je.o < -0.30]
        res["overlapping_12m"][f"{era}: P(eq12<-10% | oil12<-30%)"] = {
            "n_cond": int(len(c)), "p": round(float((c.e < -0.10).mean()), 3) if len(c) else None}

    # Low-price regime durations: Brent month-avg below 0.70 x trailing 36m mean
    trail = b_avg.rolling(36).mean().shift(1)
    low = (b_avg < 0.70 * trail).astype(int)
    spells, cur, start = [], 0, None
    for per, flag in low.items():
        if flag and not cur:
            start, cur = per, 1
        elif flag:
            cur += 1
        elif cur:
            spells.append({"start": str(start), "months": cur})
            cur = 0
    if cur:
        spells.append({"start": str(start), "months": cur, "ongoing": True})
    res["low_price_spells_lt70pct_of_trailing36m"] = spells

    # 2026 monthly path
    res["brent_2026_monthly_avg"] = {str(k): round(float(v), 2) for k, v in b_avg.loc["2025-10":].items()}
    res["brent_2026_month_end"] = {str(k): round(float(v), 2) for k, v in b_me.loc["2025-12":].items()}
    res["us_eq_2026_monthly_ret"] = {str(k): round(float(v), 4) for k, v in us.loc["2025-12":, "ret"].items()}
    res["dev_eq_2026_monthly_ret"] = {str(k): round(float(v), 4) for k, v in dev.loc["2025-12":, "ret"].items()}
    res["vix_2026_month_end"] = {str(k): round(float(v), 2) for k, v in v_me.loc["2025-12":].items()}
    # Daily realized vol of Brent in 2026 vs 2015-2019
    rd = np.log(brent_d).diff()
    res["brent_daily_realized_vol_ann"] = {
        "2015-2019": round(float(rd.loc["2015":"2019"].std() * np.sqrt(252)), 3),
        "2026-03-01_to_last": round(float(rd.loc["2026-03-01":].std() * np.sqrt(252)), 3),
        "2025": round(float(rd.loc["2025"].std() * np.sqrt(252)), 3)}

    (out_dir / "oil_equity_regimes.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
