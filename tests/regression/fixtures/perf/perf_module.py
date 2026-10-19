"""
gap_02 (groups) - deterministic performance module for observation layer O3 ("actuals").  Reference implementation.

Replaces "computed with ADIC's own code" (sec. 6, O3) with one versioned, deterministic module that computes the
'current actual' series a_{i,t} from OBSERVATION-layer data only (dated cash flows, reported NAV, index levels,
loan tapes, overlay trade marks).  It never reads truth tables, so a inherits every reporting bias in N (O1).
The same code will later run on ADIC data; outputs are hashed with the input snapshot (bitemporal registry).

Metric map by holding type (group):
  fund interests (PE funds, Secondaries S1/S3, closed-end credit funds; Co-investment and CV stakes on deal flows):
      XIRR, TVPI, DPI, RVPI, KS-PME, direct alpha (residual NAV treated as a terminal cash flow at the as-of date)
  hedge funds and long-only:  TWR (geometric linking; Modified Dietz between valuation dates; revalue on large flows)
  private credit and Capital Solutions debt/preferred: realized cash yield, PIK share, realized loss rate,
      loss-adjusted realized yield, and fund-level XIRR where the wrapper is a fund
  overlay: P&L = change in MTM + realized cash (premia, coupons, settlements) - funding charge on posted IM,
      split by book (tail, opportunistic, synthetic beta)
Conventions: ACT/365F year fractions; IRR by bracketed Brent root-finding on NPV(r) with a sign-change check
(returns None when no root, never an extrapolation); all amounts in one currency; contributions negative.
Run tests:  .venv\\Scripts\\python.exe -I -B perf_module.py
"""
from __future__ import annotations

import datetime as dt
import math
from typing import Iterable, Sequence

DAYS = 365.0
VERSION = "perf-0.1.0"


def yf(d0: dt.date, d1: dt.date) -> float:
    return (d1 - d0).days / DAYS


def _brent(fn, lo: float, hi: float, tol: float = 1e-12, maxit: int = 300) -> float | None:
    flo, fhi = fn(lo), fn(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        return None
    a, b, fa, fb = lo, hi, flo, fhi
    c, fc, d = a, fa, b - a
    e = d
    for _ in range(maxit):
        if fb * fc > 0:
            c, fc = a, fa
            d = e = b - a
        if abs(fc) < abs(fb):
            a, b, c = b, c, b
            fa, fb, fc = fb, fc, fb
        tol1 = 2 * 1e-16 * abs(b) + 0.5 * tol
        xm = 0.5 * (c - b)
        if abs(xm) <= tol1 or fb == 0:
            return b
        if abs(e) >= tol1 and abs(fa) > abs(fb):
            s = fb / fa
            if a == c:
                p, q = 2 * xm * s, 1 - s
            else:
                q, r = fa / fc, fb / fc
                p = s * (2 * xm * q * (q - r) - (b - a) * (r - 1))
                q = (q - 1) * (r - 1) * (s - 1)
            if p > 0:
                q = -q
            p = abs(p)
            if 2 * p < min(3 * xm * q - abs(tol1 * q), abs(e * q)):
                e, d = d, p / q
            else:
                d = e = xm
        else:
            d = e = xm
        a, fa = b, fb
        b += d if abs(d) > tol1 else (tol1 if xm > 0 else -tol1)
        fb = fn(b)
    return b


def xirr(flows: Sequence[tuple[dt.date, float]]) -> float | None:
    """Annual IRR of dated flows (ACT/365F). None if NPV has no sign change on (-0.99, 10)."""
    d0 = min(d for d, _ in flows)
    t = [(yf(d0, d), x) for d, x in flows]

    def npv(r):
        return sum(x / (1 + r) ** ti for ti, x in t)
    return _brent(npv, -0.99, 10.0)


def multiples(flows: Sequence[tuple[dt.date, float]], nav: float) -> dict:
    paid = -sum(x for _, x in flows if x < 0)
    dist = sum(x for _, x in flows if x > 0)
    return dict(paid_in=paid, distributed=dist, nav=nav, dpi=dist / paid, rvpi=nav / paid, tvpi=(dist + nav) / paid)


def ks_pme(flows: Sequence[tuple[dt.date, float]], nav: float, asof: dt.date, index: dict) -> float:
    """Kaplan-Schoar PME: sum(D_t / I_t) + NAV / I_T over sum(C_t / I_t); index: {date: level}."""
    num = sum(x / index[d] for d, x in flows if x > 0) + nav / index[asof]
    den = sum(-x / index[d] for d, x in flows if x < 0)
    return num / den


def direct_alpha(flows: Sequence[tuple[dt.date, float]], nav: float, asof: dt.date, index: dict) -> float | None:
    """Gredil-Griffiths-Stucke direct alpha: compound each flow to the as-of date at the index return,
    take the IRR of the compounded flows (NAV terminal), report the continuously compounded rate ln(1 + IRR)."""
    fv = [(d, x * index[asof] / index[d]) for d, x in flows] + [(asof, nav)]
    r = xirr(fv)
    return None if r is None else math.log1p(r)


def twr(vals: Sequence[tuple[dt.date, float]], flows: Sequence[tuple[dt.date, float]], large: float = 0.10) -> float:
    """Time-weighted return over [first, last valuation date]. vals: dated valuations (end of day, after flows
    on that date); flows: external flows (+ in).  Between valuation dates use Modified Dietz; a flow larger than
    `large` x start value must coincide with a valuation date (raises otherwise)."""
    vals = sorted(vals)
    g = 1.0
    for (d0, v0), (d1, v1) in zip(vals[:-1], vals[1:]):
        sub = [(d, x) for d, x in flows if d0 < d <= d1]
        T = (d1 - d0).days
        for d, x in sub:
            if abs(x) > large * v0 and d != d1:
                raise ValueError(f"large flow {x} on {d} needs a valuation date (revalue on large flows)")
        net = sum(x for _, x in sub)
        wsum = sum(x * (d1 - d).days / T for d, x in sub)
        g *= 1 + (v1 - v0 - net) / (v0 + wsum)
    return g - 1


def credit_realized(periods: Iterable[dict]) -> dict:
    """periods: dicts with avg_par, cash_interest, pik_interest, fees, charge_offs, recoveries (one per period,
    period length in years 'len').  Returns annualized realized yield, PIK share, loss rate and loss-adjusted yield."""
    P = list(periods)
    par_yrs = sum(p["avg_par"] * p["len"] for p in P)
    cash = sum(p["cash_interest"] + p.get("fees", 0.0) for p in P)
    pik = sum(p["pik_interest"] for p in P)
    loss = sum(p["charge_offs"] - p["recoveries"] for p in P)
    return dict(cash_yield=cash / par_yrs, pik_share=pik / (cash + pik) if cash + pik else 0.0,
                total_yield=(cash + pik) / par_yrs, loss_rate=loss / par_yrs,
                loss_adj_cash_yield=(cash - loss) / par_yrs)


def overlay_pnl(trades: Iterable[dict], ftp_rate: float) -> dict:
    """trades: dicts with book, mtm0, mtm1, cash (premia paid negative, coupons/settlements positive),
    im_posted (average over the period), len (years). Funding charge = ftp_rate x IM x len (CF's FTP curve)."""
    out: dict = {}
    for tr in trades:
        b = out.setdefault(tr["book"], dict(mtm_change=0.0, cash=0.0, funding=0.0, pnl=0.0))
        f = ftp_rate * tr["im_posted"] * tr["len"]
        b["mtm_change"] += tr["mtm1"] - tr["mtm0"]
        b["cash"] += tr["cash"]
        b["funding"] -= f
        b["pnl"] += tr["mtm1"] - tr["mtm0"] + tr["cash"] - f
    out["total"] = {k: sum(v[k] for kk, v in out.items() if kk != "total") for k in ("mtm_change", "cash", "funding", "pnl")}
    return out


# ------------------------------------------------------------------------------------------------ golden tests
def _tests() -> list:
    D = dt.date
    res = []

    def check(name, got, exp, tol=1e-9):
        ok = got is not None and abs(got - exp) <= tol
        res.append((name, ok, got, exp))
    # T1 XIRR: -100 then +121 after exactly 730 days (ACT/365F, 2 years) -> 10%
    check("xirr_2y_10pct", xirr([(D(2020, 1, 1), -100.0), (D(2021, 12, 31), 121.0)]), 0.10, 1e-9)
    # T2 XIRR: no sign change -> None
    res.append(("xirr_no_root_is_None", xirr([(D(2020, 1, 1), 100.0), (D(2021, 1, 1), 5.0)]) is None, None, None))
    # T3 multiples
    fl = [(D(2015, 1, 1), -50.0), (D(2016, 1, 1), -50.0), (D(2020, 1, 1), 60.0)]
    m = multiples(fl, 80.0)
    check("tvpi", m["tvpi"], 1.4)
    check("dpi", m["dpi"], 0.6)
    # T4 KS-PME equals TVPI when the index is flat
    flat = {d: 100.0 for d, _ in fl}
    flat[D(2024, 1, 1)] = 100.0
    check("kspme_flat_index_equals_tvpi", ks_pme(fl, 80.0, D(2024, 1, 1), flat), 1.4)
    # T5 direct alpha equals ln(1 + IRR) when the index is flat
    irr_ = xirr(fl + [(D(2024, 1, 1), 80.0)])
    check("direct_alpha_flat_index", direct_alpha(fl, 80.0, D(2024, 1, 1), flat), math.log1p(irr_), 1e-9)
    # T6 direct alpha is zero when the fund exactly tracks the index (buy 100 at I=100, NAV = 100 x I_T / 100)
    idx = {D(2018, 1, 1): 100.0, D(2023, 1, 1): 161.051}
    check("direct_alpha_index_tracker_zero", direct_alpha([(D(2018, 1, 1), -100.0)], 161.051, D(2023, 1, 1), idx), 0.0, 1e-9)
    check("kspme_index_tracker_one", ks_pme([(D(2018, 1, 1), -100.0)], 161.051, D(2023, 1, 1), idx), 1.0, 1e-12)
    # T7 TWR is invariant to an external flow made on a valuation date
    v = [(D(2025, 1, 1), 100.0), (D(2025, 7, 1), 110.0 + 50.0), (D(2026, 1, 1), 176.0)]
    check("twr_flow_on_valuation_date", twr(v, [(D(2025, 7, 1), 50.0)]), 1.10 * 1.10 - 1, 1e-12)
    # T8 large intra-period flow without a valuation raises
    try:
        twr([(D(2025, 1, 1), 100.0), (D(2025, 12, 31), 130.0)], [(D(2025, 6, 30), 20.0)])
        res.append(("twr_large_flow_requires_revaluation", False, None, None))
    except ValueError:
        res.append(("twr_large_flow_requires_revaluation", True, None, None))
    # T9 credit: par 100 for 1y, cash 8, PIK 2, charge-offs 1.5, recoveries 0.5
    c = credit_realized([dict(avg_par=100.0, len=1.0, cash_interest=8.0, pik_interest=2.0, fees=0.0,
                              charge_offs=1.5, recoveries=0.5)])
    check("credit_cash_yield", c["cash_yield"], 0.08)
    check("credit_pik_share", c["pik_share"], 0.2)
    check("credit_loss_rate", c["loss_rate"], 0.01)
    check("credit_loss_adj_cash_yield", c["loss_adj_cash_yield"], 0.07)
    # T10 overlay: tail put bought for 4, MTM 0 -> 10; opportunistic MTM 5 -> 3 with coupon 1; IM 20 at FTP 4.5%
    o = overlay_pnl([dict(book="tail", mtm0=0.0, mtm1=10.0, cash=-4.0, im_posted=0.0, len=1.0),
                     dict(book="opportunistic", mtm0=5.0, mtm1=3.0, cash=1.0, im_posted=20.0, len=1.0)], 0.045)
    check("overlay_tail_pnl", o["tail"]["pnl"], 6.0)
    check("overlay_opp_pnl", o["opportunistic"]["pnl"], -1.9)
    check("overlay_total_pnl", o["total"]["pnl"], 4.1)
    return res


if __name__ == "__main__":
    results = _tests()
    for name, ok, got, exp in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name:40s} got={got} exp={exp}")
    print(f"{sum(ok for _, ok, _, _ in results)}/{len(results)} golden tests passed ({VERSION})")
