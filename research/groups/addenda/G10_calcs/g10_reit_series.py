"""G10 stream: public-data computations on the FTSE Nareit All Equity REITs total-return index.

Input: Nareit 'MonthlyHistoricalReturns.xls' (Dec 1971 - Sep 2026), downloaded 2026-10-18 into a scratch
folder (untrusted input; parsed with xlrd only). Output: g10_reit_series_results.json with annual returns,
drawdowns and monthly 2026 returns. These are PUBLIC-DATA computations, not ADIC data and not synthetic.

Usage: python -I g10_reit_series.py <pylibs_dir> <xls_path> <out_json>
"""
import json
import sys
import datetime as dt

sys.path.insert(0, sys.argv[1])
import xlrd  # noqa: E402

XLS, OUT = sys.argv[2], sys.argv[3]
book = xlrd.open_workbook(XLS)
sh = book.sheet_by_name("Index Data")

# Locate the 'All Equity REITs' block from the header row (row 5) to avoid hard-coding.
hdr = [str(sh.cell_value(5, c)) for c in range(sh.ncols)]
col0 = hdr.index("All Equity REITs")          # Total Return column
COL_TR, COL_TRI, COL_PR, COL_PRI, COL_INC, COL_DY = col0, col0 + 1, col0 + 2, col0 + 3, col0 + 4, col0 + 5

rows = []
for r in range(9, sh.nrows):
    d = sh.cell_value(r, 0)
    if not isinstance(d, float) or d <= 0:
        continue
    date = dt.datetime(1899, 12, 30) + dt.timedelta(days=d)
    tri = sh.cell_value(r, COL_TRI)
    if tri in ("", None):
        continue
    dy = sh.cell_value(r, COL_DY)
    rows.append((date.date(), float(tri), float(dy) if dy not in ("", None) else None))

dates = [x[0] for x in rows]
tri = [x[1] for x in rows]
dy = {x[0]: x[2] for x in rows}


def idx_at(y, m):
    for d, v in zip(dates, tri):
        if d.year == y and d.month == m:
            return v
    return None


res = {"label": "PUBLIC DATA (FTSE Nareit All Equity REITs, total return) - not ADIC data",
       "last_month": str(dates[-1]), "annual_total_return_pct": {}, "monthly_2026_pct": {}}
for y in range(2005, dates[-1].year + 1):
    a, b = idx_at(y - 1, 12), idx_at(y, 12) if y < dates[-1].year else tri[-1]
    if a and b:
        key = str(y) if y < dates[-1].year else f"{y} YTD to {dates[-1]}"
        res["annual_total_return_pct"][key] = round(100 * (b / a - 1), 2)
for d, v, prev in zip(dates[1:], tri[1:], tri[:-1]):
    if d.year == 2026:
        res["monthly_2026_pct"][str(d)] = round(100 * (v / prev - 1), 2)


def drawdown(start, end):
    """Peak-to-trough on month-end total-return index within [start, end]."""
    seg = [(d, v) for d, v in zip(dates, tri) if start <= d <= end]
    peak_d, peak_v, best = seg[0][0], seg[0][1], (0.0, None, None)
    for d, v in seg:
        if v > peak_v:
            peak_d, peak_v = d, v
        dd = v / peak_v - 1
        if dd < best[0]:
            best = (dd, peak_d, d)
    return {"max_drawdown_pct": round(100 * best[0], 1), "peak": str(best[1]), "trough": str(best[2])}


res["drawdowns"] = {
    "GFC 2007-2010": drawdown(dt.date(2006, 12, 1), dt.date(2010, 12, 31)),
    "COVID 2020": drawdown(dt.date(2019, 12, 1), dt.date(2020, 12, 31)),
    "Rates 2022-2023": drawdown(dt.date(2021, 12, 1), dt.date(2023, 12, 31)),
    "2026 to date": drawdown(dt.date(2025, 12, 1), dates[-1]),
}
res["dividend_yield_pct_latest"] = dy.get(dates[-1])
res["dividend_yield_pct_dec2021"] = next((dy[d] for d in dates if d.year == 2021 and d.month == 12), None)

# Quarterly total-return series 2000Q1-latest for desmoothing comparisons (used by g10_desmooth.py).
q = []
for d, v in zip(dates, tri):
    if d.month in (3, 6, 9, 12) and d.year >= 1999:
        q.append((str(d), v))
res["quarterly_tri_1999_on"] = q

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "quarterly_tri_1999_on"}, indent=1))
