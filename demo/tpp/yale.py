"""The Yale model as a benchmark: Takahashi and Alexander (2002), "Illiquid Alternative Asset Fund Modeling".

Per fund, by fund year k (deterministic, one path):
  contributions   C_k = RC_k x (commitment - paid-in to date)          RC: e.g. 25%, 33%, then 50% a year
  distributions   D_k = RD_k x NAV_{k-1} x (1 + G),  RD_k = max(Y, (k / L)^B)   bow B, life L, yield Y
  NAV             NAV_k = NAV_{k-1} x (1 + G) + C_k - D_k
The engine's private cash flows follow the same structure (call and distribution intensities by fund age) but make
them depend on the exit window, the market factors and the ER world, on thousands of paths. Here G is each bucket's
ER base return, so the two differ only in what the Yale model leaves out. Parameters: config/assumptions.json yale,
used as given ("textbook") and fitted to ADIC's own DPI by vintage (life and bow scaled, fit_to_vintages).
"""
from __future__ import annotations

import copy

import numpy as np
import pandas as pd

from .buckets import BY_ID, PRIVATE

FAMILY = {"PE_EU_F": "buyout", "PE_US_F": "buyout", "PE_VC_F": "venture", "SEC_LP_F": "secondaries",
          "SEC_GP_F": "secondaries", "CS_CR_F": "credit", "CS_INS_F": "credit", "INF_EU_F": "infrastructure",
          "INF_NA_F": "infrastructure", "RE_F": "real_estate"}


def family(bucket: str) -> str:
    if bucket in FAMILY:
        return FAMILY[bucket]
    return "coinvest_income" if bucket[:2] in ("CS", "IN", "RE") else "coinvest_equity"


def families(P, life_mult: float = 1.0, bow_mult: float = 1.0) -> dict:
    fam = copy.deepcopy(P.get("yale.families"))
    for f in fam.values():
        f["life"] = float(f["life"]) * life_mult
        f["bow"] = float(f["bow"]) * bow_mult
    return fam


def params(fam: dict, bucket: str, growth: float) -> dict:
    f = dict(fam[family(bucket)])
    f["G"] = float(growth)
    return f


def _rc(f: dict, k: int) -> float:
    rc = f["rc"]
    return float(rc[min(k, len(rc)) - 1])


def _rd(f: dict, k: float) -> float:
    return float(min(1.0, max(f["yield"], (max(k, 0.0) / f["life"]) ** f["bow"])))


def fund_curve(f: dict, years: int = 15) -> dict:
    """Cumulative paid-in, distributions and NAV per $1 committed, by fund year 0..years."""
    pic, dist, nav, unf = [0.0], [0.0], [0.0], 1.0
    for k in range(1, years + 1):
        c = _rc(f, k) * unf
        grown = nav[-1] * (1 + f["G"])
        d = _rd(f, k) * grown
        unf -= c
        pic.append(pic[-1] + c)
        dist.append(dist[-1] + d)
        nav.append(grown + c - d)
    return {"pic": pic, "dist": dist, "nav": nav}


def dpi_at(f: dict, age: float) -> float:
    """DPI at a fractional fund age (linear between fund-year ends)."""
    cv = fund_curve(f, int(np.ceil(max(age, 0.0))) + 1)
    k0 = int(np.floor(age))
    t = age - k0
    pic = cv["pic"][k0] * (1 - t) + cv["pic"][k0 + 1] * t
    dist = cv["dist"][k0] * (1 - t) + cv["dist"][k0 + 1] * t
    return dist / pic if pic > 1e-12 else 0.0


def _vintage_weights(holdings: pd.DataFrame) -> dict:
    d = holdings[(holdings["commit_bn"] > 0) & holdings["vintage"].notna()
                 & holdings["bucket"].map(lambda b: BY_ID[b].private)]
    return {int(v): g.groupby("bucket")["commit_bn"].sum() for v, g in d.groupby("vintage")}


def vintage_dpi(holdings: pd.DataFrame, bucket_ret: pd.DataFrame, fam: dict, as_of_year: float) -> list[dict]:
    """The Yale model's DPI for each vintage of the live book, commitment-weighted by strategy exactly like the
    actual figure (vintage funds start mid-year on average)."""
    out = []
    for v, w in _vintage_weights(holdings).items():
        age = as_of_year - (v + 0.5)
        if w.sum() <= 0 or age <= 0:
            continue
        dpi = sum(wb * dpi_at(params(fam, b, bucket_ret.loc[b, "new_Base"]), age) for b, wb in w.items()) / w.sum()
        out.append({"vintage": v, "age": age, "dpi_yale": float(dpi)})
    return out


def vintage_paid_in(holdings: pd.DataFrame, bucket_ret: pd.DataFrame, fam: dict, as_of_year: float) -> list[dict]:
    """Paid-in share of commitments by vintage: the actual (1 - unfunded / commitment, live funds) against the Yale
    model's contribution schedule at the same age."""
    d = holdings[(holdings["commit_bn"] > 0) & holdings["vintage"].notna()
                 & holdings["bucket"].map(lambda b: BY_ID[b].private)]
    out = []
    for v, g in d.groupby("vintage"):
        age = as_of_year - (float(v) + 0.5)
        c = float(g["commit_bn"].sum())
        if c <= 0 or age <= 0:
            continue
        w = g.groupby("bucket")["commit_bn"].sum()
        model = 0.0
        for b, wb in w.items():
            cv = fund_curve(params(fam, b, bucket_ret.loc[b, "new_Base"]), int(np.ceil(age)) + 1)
            k0, t = int(np.floor(age)), age - np.floor(age)
            model += wb * (cv["pic"][k0] * (1 - t) + cv["pic"][k0 + 1] * t)
        out.append({"vintage": int(v), "age": age, "paid_in_actual": 1.0 - float(g["unfunded_bn"].sum()) / c,
                    "paid_in_yale": model / c})
    return out


def fit_to_vintages(holdings, bucket_ret, P, as_of_year: float, actual: dict, vintages=range(2012, 2025)) -> dict:
    """Scale every family's life and bow to fit ADIC's actual DPI by vintage (commitment-weighted least squares):
    the Yale model at its best on this book."""
    wts = _vintage_weights(holdings)
    vs = [v for v in vintages if v in actual and v in wts]
    best = None
    for lm in np.round(np.arange(0.8, 3.01, 0.1), 2):
        for bm in np.round(np.arange(0.5, 2.01, 0.1), 2):
            rows = {r["vintage"]: r["dpi_yale"] for r in vintage_dpi(holdings, bucket_ret, families(P, lm, bm), as_of_year)}
            sse = sum(float(wts[v].sum()) * (rows[v] - actual[v]) ** 2 for v in vs if v in rows)
            if best is None or sse < best["sse"]:
                best = {"life_mult": float(lm), "bow_mult": float(bm), "sse": sse}
    base = sum(float(wts[r["vintage"]].sum()) * (r["dpi_yale"] - actual[r["vintage"]]) ** 2
               for r in vintage_dpi(holdings, bucket_ret, families(P), as_of_year) if r["vintage"] in vs)
    best["sse_textbook"] = base
    best["vintages"] = [int(v) for v in vs]
    return best


def project(book, plan, fam: dict, years: int = 5) -> dict:
    """The Yale model's deterministic projection of the private book under a plan's commitments (no secondary
    sales: the status quo without the program): calls, distributions and private NAV by year."""
    calls, dist, nav = np.zeros(years), np.zeros(years), np.zeros(years + 1)
    br = book.bucket_ret

    def run(f, v, unf, k0, t_start):
        for t in range(t_start, years):
            k = k0 + t - t_start
            cc = _rc(f, k) * unf
            grown = v * (1 + f["G"])
            dd = _rd(f, k) * grown
            unf -= cc
            v = grown + cc - dd
            calls[t] += cc
            dist[t] += dd
            nav[t + 1] += v

    for u in book.units:
        f = params(fam, u.bucket, br.loc[u.bucket, "new_Base"])
        for c in u.cohorts:
            nav[0] += float(c["nav"])
            run(f, float(c["nav"]), float(c["unf"]), int(np.floor(float(c["age"]))) + 1, 0)
    for b in PRIVATE:
        f = params(fam, b, br.loc[b, "new_Base"])
        for t0, amount in enumerate(plan.commit.get(b, [0.0] * years)[:years]):
            run(f, 0.0, float(amount), 1, t0)
    return {"calls": calls.tolist(), "dist": dist.tolist(), "net": (dist - calls).tolist(), "nav": nav.tolist()}
