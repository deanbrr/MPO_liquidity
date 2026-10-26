"""Data layer: the ER strategy-return grid and the fund-level actual-vs-underwritten file (DATA).

ER file ("Strategy Returns"): one row per Department x Vertical x vehicle (Fund / Co-Invest / Derivatives) with
Base, Upside and Downside forward returns. Departments are forward-filled; names are trimmed. Rows whose Upside is
below Base or whose Downside is above Base are kept and flagged: for Treasury and Cash the inversion is economic
(rates fall in the downside world), so the three columns are read as joint macro worlds, not per-asset ranges.

Fund file: one row per position with underwritten base IRR / MOIC, since-inception actual IRR, TVPI / DPI / RVPI,
latest NAV, commitments and unfunded, vintage. Amounts stored as long decimal strings are parsed; Excel serial dates
are converted. Zero underwritten IRR / MOIC means missing.

Live book: rows whose latest performance date is within `max_stale_months` of the file's as-of date, with NAV or
unfunded exposure. Everything else is reported, never silently dropped (quality_report).
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd

from . import xlsx

ER_WORLDS = ["Downside", "Base", "Upside"]
FUND_NUMERIC = ["UNDERWRITTEN_BASE_IRR", "UNDERWRITTEN_BASE_MOIC", "ACTUAL_IRR_SINCE_INCEPTION", "ACTUAL_TVPI",
                "ACTUAL_DPI", "ACTUAL_RVPI", "LATEST_NAV_USD", "ORIGINAL_COMMITMENT_USD", "CURRENT_COMMITMENT_USD",
                "UNFUNDED_COMMITMENT_USD", "IRR_ACTUAL_MINUS_UNDERWRITTEN", "TVPI_ACTUAL_VS_UNDERWRITTEN",
                "IC_APPROVED_DATE", "LATEST_PERFORMANCE_DATE"]


def _xl_date(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return pd.NaT
    try:
        return pd.Timestamp(dt.date(1899, 12, 30) + dt.timedelta(days=int(float(v))))
    except (TypeError, ValueError):
        return pd.NaT


# ---------------------------------------------------------------------------------------------- ER grid
def load_er(path: str | Path) -> pd.DataFrame:
    rows = xlsx.read_sheet(path, 0)
    hdr_i = next(i for i, r in enumerate(rows) if r and any(str(c).strip() == "Base" for c in r if c is not None))
    hdr = [str(c).strip() if c is not None else "" for c in rows[hdr_i]]
    col = {name: hdr.index(name) for name in ("Department", "Vertical", "Base", "Upside", "Downside")}
    veh_col = next(i for i, h in enumerate(hdr) if h.lower().startswith("fund"))
    out, dept, vert = [], None, None
    for r in rows[hdr_i + 1:]:
        r = r + [None] * (len(hdr) - len(r))
        if all(v is None for v in r):
            continue
        d = r[col["Department"]]
        v = r[col["Vertical"]]
        if d is not None and str(d).strip():
            dept, vert = str(d).strip(), None
        if v is not None and str(v).strip():
            vert = str(v).strip()
        base, up, dn = r[col["Base"]], r[col["Upside"]], r[col["Downside"]]
        if not all(isinstance(x, float) for x in (base, up, dn)):
            continue
        veh = str(r[veh_col]).strip() if r[veh_col] is not None else ""
        out.append({"department": dept, "vertical": vert or dept, "vehicle": veh or "Fund",
                    "Base": base, "Upside": up, "Downside": dn})
    er = pd.DataFrame(out)
    er["key"] = er["department"] + " | " + er["vertical"] + " | " + er["vehicle"]
    flags = []
    for _, r in er.iterrows():
        f = []
        if r.Upside < r.Base:
            f.append("upside below base")
        if r.Downside > r.Base:
            f.append("downside above base")
        flags.append("; ".join(f))
    er["flags"] = flags
    return er.reset_index(drop=True)


# ---------------------------------------------------------------------------------------------- fund file
def load_funds(path: str | Path) -> pd.DataFrame:
    rows = xlsx.read_sheet(path, 0)
    hdr = [str(c).strip() for c in rows[0]]
    data = [r + [None] * (len(hdr) - len(r)) for r in rows[1:]]
    df = pd.DataFrame(data, columns=hdr)
    for c in FUND_NUMERIC:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["perf_date"] = df["LATEST_PERFORMANCE_DATE"].map(_xl_date)
    df["ic_date"] = df["IC_APPROVED_DATE"].map(_xl_date)
    df["vintage"] = pd.to_numeric(df["VINTAGE_YEAR"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")
    for c in ("FUND_NAME", "INVESTMENT_CLASS", "INVESTMENT_STYLE"):
        df[c] = df[c].astype("string").str.strip()
    # zero underwritten IRR / MOIC = not underwritten (legacy, secondaries bought in, liquid sleeves)
    df["uw_irr"] = df["UNDERWRITTEN_BASE_IRR"].where(df["UNDERWRITTEN_BASE_IRR"] > 0)
    df["uw_moic"] = df["UNDERWRITTEN_BASE_MOIC"].where(df["UNDERWRITTEN_BASE_MOIC"] > 0)
    df["act_irr"] = df["ACTUAL_IRR_SINCE_INCEPTION"]
    df["nav_bn"] = df["LATEST_NAV_USD"].fillna(0.0) / 1e9
    df["unfunded_bn"] = df["UNFUNDED_COMMITMENT_USD"].fillna(0.0).clip(lower=0.0) / 1e9
    df["commit_bn"] = df["ORIGINAL_COMMITMENT_USD"].fillna(0.0) / 1e9
    return df


def as_of(funds: pd.DataFrame) -> pd.Timestamp:
    return funds["perf_date"].max()


def live_book(funds: pd.DataFrame, P) -> tuple[pd.DataFrame, dict]:
    """Live holdings and the reasons every other row was left out."""
    asof = as_of(funds)
    cutoff = asof - pd.DateOffset(months=int(P.get("fund.max_stale_months")))
    min_nav = float(P.get("fund.min_live_nav_usd")) / 1e9
    marked = funds["perf_date"].notna() & (funds["perf_date"] > cutoff)
    legacy = funds["perf_date"].notna() & ~marked
    has_exposure = (funds["nav_bn"] > min_nav) | (funds["unfunded_bn"] > 1e-5)   # unfunded below $10k is rounding
    live_mask = marked & has_exposure & (funds["nav_bn"] >= 0)
    if P.get("fund.include_legacy_rows"):
        live_mask |= legacy & (funds["nav_bn"] > min_nav)
    live = funds[live_mask].copy()
    live["legacy"] = legacy[live_mask]
    yr = asof.year + (asof.dayofyear - 0.5) / 365.25
    live["age"] = np.clip(yr - (live["vintage"].fillna(asof.year) + 0.5), 0.0, 40.0)
    live = live.reset_index(drop=True)
    reasons = {
        "as_of": asof.date().isoformat(),
        "cutoff": cutoff.date().isoformat(),
        "rows_total": int(len(funds)),
        "rows_live": int(len(live)),
        "nav_live_bn": float(live["nav_bn"].sum()),
        "unfunded_live_bn": float(live["unfunded_bn"].sum()),
    }
    return live, reasons


def quality_report(funds: pd.DataFrame, live: pd.DataFrame, P) -> dict:
    asof = as_of(funds)
    cutoff = asof - pd.DateOffset(months=int(P.get("fund.max_stale_months")))
    nav = funds["nav_bn"]
    excl = []

    def add(label, mask, note):
        m = mask & ~funds["FUND_CODE"].isin(live["FUND_CODE"])
        excl.append({"reason": label, "rows": int(m.sum()), "nav_pos_bn": float(nav[m & (nav > 0)].sum()),
                     "nav_neg_bn": float(nav[m & (nav < 0)].sum()), "note": note})

    stale = funds["perf_date"].notna() & (funds["perf_date"] <= cutoff)
    add("Last valued before the staleness window", stale,
        "Legacy marks (2017-2023): pre-restructuring strategic stakes, 2021 cash deposits, old futures and swaps, 2017 loans")
    add("No performance date (never marked or pipeline)", funds["perf_date"].isna(),
        "Approved or pipeline commitments with no NAV and no unfunded in the file")
    add("Negative NAV (liabilities, hedges, swaps)", (nav < 0) & ~stale,
        "Synthetic hedges and swap MTM; balance-sheet liabilities are entered as assumptions")
    add("Fully realized (no NAV, no unfunded)", funds["perf_date"].notna() & ~stale & (nav <= 0)
        & (funds["unfunded_bn"] <= 0), "Exited positions")
    top_legacy = funds[stale & (nav.abs() > 0.25)].sort_values("nav_bn", key=np.abs, ascending=False)
    oddities = []
    for _, r in live.iterrows():
        if pd.notna(r.act_irr) and abs(r.act_irr) > 1.5:
            oddities.append({"code": r.FUND_CODE, "name": r.FUND_NAME, "issue": f"actual IRR {r.act_irr:.0%}",
                             "nav_bn": r.nav_bn})
        if pd.notna(r.ACTUAL_TVPI) and r.ACTUAL_TVPI > 8:
            oddities.append({"code": r.FUND_CODE, "name": r.FUND_NAME, "issue": f"TVPI {r.ACTUAL_TVPI:.1f}x",
                             "nav_bn": r.nav_bn})
    oddities = sorted(oddities, key=lambda o: -o["nav_bn"])[:25]
    miss = {
        "no underwritten IRR (NAV $bn)": float(live.loc[live["uw_irr"].isna(), "nav_bn"].sum()),
        "no actual IRR (NAV $bn)": float(live.loc[live["act_irr"].isna(), "nav_bn"].sum()),
        "no vintage (NAV $bn)": float(live.loc[live["vintage"].isna(), "nav_bn"].sum()),
        "no investment class (NAV $bn)": float(live.loc[live["INVESTMENT_CLASS"].isna(), "nav_bn"].sum()),
    }
    return {
        "as_of": asof.date().isoformat(),
        "file_rows": int(len(funds)),
        "file_nav_gross_bn": float(nav[nav > 0].sum()),
        "file_nav_net_bn": float(nav.sum()),
        "live_rows": int(len(live)),
        "live_nav_bn": float(live["nav_bn"].sum()),
        "live_unfunded_bn": float(live["unfunded_bn"].sum()),
        "excluded": excl,
        "top_legacy_rows": [{"code": r.FUND_CODE, "name": r.FUND_NAME, "nav_bn": float(r.nav_bn),
                             "last_valued": r.perf_date.date().isoformat()} for _, r in top_legacy.head(20).iterrows()],
        "field_gaps": miss,
        "oddities": oddities,
    }


def dpi_by_vintage(live: pd.DataFrame) -> list[dict]:
    """Commitment-weighted DPI, TVPI and the share of NAV by vintage (private holdings with commitments)."""
    d = live[(live["commit_bn"] > 0) & live["vintage"].notna() & live["ACTUAL_DPI"].notna()].copy()
    d["w"] = d["commit_bn"]
    out = []
    for v, g in d.groupby("vintage"):
        w = g["w"].sum()
        if w <= 0:
            continue
        out.append({"vintage": int(v), "dpi": float((g["ACTUAL_DPI"] * g["w"]).sum() / w),
                    "tvpi": float((g["ACTUAL_TVPI"].fillna(0) * g["w"]).sum() / w),
                    "commit_bn": float(w), "nav_bn": float(g["nav_bn"].sum()), "n": int(len(g))})
    return out
