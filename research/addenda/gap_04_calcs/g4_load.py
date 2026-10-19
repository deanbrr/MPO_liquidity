"""Loaders for gap_04 (state/fragility engine) analysis. All inputs are public downloads, parsed defensively.

Every function takes explicit paths; nothing is executed from the data directory.
"""
from __future__ import annotations

import datetime as dt
import io
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from xlsx_min import read_xlsx  # noqa: E402

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


def _zip_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        name = zf.namelist()[0]
        return zf.read(name).decode("latin-1", errors="replace")


def ff_daily(path: Path) -> pd.DataFrame:
    """Fama-French daily factors (Mkt-RF, SMB, HML, RF) in decimals, DatetimeIndex."""
    recs = []
    for ln in _zip_text(path).splitlines():
        m = re.match(r"^\s*(\d{8})\s*,(.*)$", ln)
        if not m:
            continue
        vals = [v.strip() for v in m.group(2).split(",")]
        if len(vals) < 4:
            continue
        try:
            x = [float(v) for v in vals[:4]]
        except ValueError:
            continue
        recs.append((pd.Timestamp(m.group(1)), *x))
    df = pd.DataFrame(recs, columns=["date", "mkt_rf", "smb", "hml", "rf"]).set_index("date")
    df = df[~df.index.duplicated()].sort_index() / 100.0
    return df


def ff_monthly(path: Path) -> pd.DataFrame:
    recs = []
    for ln in _zip_text(path).splitlines():
        m = re.match(r"^\s*(\d{6})\s*,(.*)$", ln)
        if not m:
            if recs and re.match(r"^\s*\d{4}\s*,", ln):
                break  # annual block
            continue
        vals = [v.strip() for v in m.group(2).split(",")]
        try:
            x = [float(v) for v in vals[:4]]
        except ValueError:
            continue
        recs.append((pd.Period(m.group(1)[:4] + "-" + m.group(1)[4:], "M"), *x))
    df = pd.DataFrame(recs, columns=["m", "mkt_rf", "smb", "hml", "rf"]).drop_duplicates("m").set_index("m")
    return df.sort_index() / 100.0


def ff49_daily(path: Path) -> pd.DataFrame:
    """Value-weighted daily returns of the 49 FF industries (decimals); -99.99/-999 -> NaN."""
    lines = _zip_text(path).splitlines()
    cols, recs, in_vw = None, [], False
    for ln in lines:
        if "Average Value Weighted Returns" in ln:
            in_vw = True
            continue
        if "Average Equal Weighted Returns" in ln:
            break
        if in_vw and cols is None and ln.startswith(","):
            cols = [c.strip() for c in ln.split(",")[1:]]
            continue
        if in_vw and cols is not None:
            m = re.match(r"^\s*(\d{8})\s*,(.*)$", ln)
            if m:
                vals = [float(v) for v in m.group(2).split(",")[: len(cols)]]
                recs.append([pd.Timestamp(m.group(1))] + vals)
    df = pd.DataFrame(recs, columns=["date"] + cols).set_index("date").sort_index()
    df = df.mask(df <= -99.0)
    return df / 100.0


def gsw_yields(path: Path, mats=(1, 2, 5, 7, 10, 30)) -> pd.DataFrame:
    """Gurkaynak-Sack-Wright zero-coupon yields SVENYnn (continuously compounded, %)."""
    txt = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = next(i for i, ln in enumerate(txt) if ln.startswith("Date,"))
    df = pd.read_csv(io.StringIO("\n".join(txt[start:])), na_values=["NA", ""], low_memory=False)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).set_index("Date").sort_index()
    keep = {f"SVENY{m:02d}": f"y{m}" for m in mats if f"SVENY{m:02d}" in df.columns}
    out = df[list(keep)].rename(columns=keep).apply(pd.to_numeric, errors="coerce")
    return out


def zero_returns(y: pd.DataFrame) -> pd.DataFrame:
    """Daily log returns of constant-maturity zero-coupon bonds from GSW zero yields (%).

    r_t = [y_{t-1}(n) n - y_t(n) (n - dt)] / 100, ignoring one-day roll-down; dt from calendar days.
    """
    out = {}
    days = y.index.to_series().diff().dt.days.fillna(1).to_numpy() / 365.25
    for c in y.columns:
        n = float(c[1:])
        yy = y[c].to_numpy()
        r = np.full(len(yy), np.nan)
        r[1:] = (yy[:-1] * n - yy[1:] * (n - days[1:])) / 100.0
        out[f"z{int(n)}"] = r
    return pd.DataFrame(out, index=y.index)


def ebp(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["m"] = pd.to_datetime(df["date"]).dt.to_period("M")
    return df.set_index("m")[["gz_spread", "ebp", "est_prob"]].astype(float)


def ipo_monthly(path: Path) -> pd.DataFrame:
    """Ritter IPOALL: month, 2-digit year, avg first-day return, gross count, net count, % above midpoint."""
    rows = read_xlsx(str(path))
    recs = []
    for r in rows:
        if len(r) < 4 or not isinstance(r[0], float) or not isinstance(r[1], float):
            continue
        mo, yy = int(r[0]), int(r[1])
        if not 1 <= mo <= 12:
            continue
        year = 1900 + yy if yy >= 60 else 2000 + yy
        gross = r[3] if isinstance(r[3], float) else np.nan
        net = r[4] if len(r) > 4 and isinstance(r[4], float) else np.nan
        recs.append((pd.Period(f"{year}-{mo:02d}", "M"), gross, net))
    df = pd.DataFrame(recs, columns=["m", "gross", "net"]).drop_duplicates("m", keep="last").set_index("m")
    return df.sort_index()


def multpl_cape(path: Path) -> pd.Series:
    """Generic multpl.com 'table/by-month' parser (CAPE, CPI, inflation %); month-start rows only."""
    h = path.read_text(encoding="utf-8", errors="replace")
    rows = re.findall(r"<tr[^>]*>\s*<td[^>]*>([^<]+)</td>\s*<td[^>]*>\s*(?:&#x2002;)?\s*([^<]+)</td>", h)
    out = {}
    for d, v in rows:
        try:
            ts = pd.Timestamp(dt.datetime.strptime(d.strip(), "%b %d, %Y"))
            out[ts] = float(v.strip().replace(",", "").replace("%", ""))
        except ValueError:
            continue
    s = pd.Series(out).sort_index()
    # keep month-start observations (one per month); the latest intra-month row is dropped for history
    s_m = s[s.index.day == 1]
    s_m.index = s_m.index.to_period("M")
    s_m.attrs["latest"] = (str(s.index[-1].date()), float(s.iloc[-1]))
    return s_m


def cboe_close(path: Path, col: str | None = None) -> pd.Series:
    df = pd.read_csv(path)
    df["DATE"] = pd.to_datetime(df["DATE"], format="%m/%d/%Y")
    c = col or ("CLOSE" if "CLOSE" in df.columns else df.columns[-1])
    return df.set_index("DATE")[c].astype(float).sort_index()


def eia_daily(path: Path) -> pd.Series:
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
                    pass
    return pd.Series(out).sort_index()
