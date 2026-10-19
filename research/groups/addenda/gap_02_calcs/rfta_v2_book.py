"""
gap_02 (groups) - RFT-TA v2 vintage engine for the SYN-ADIC-177 PE-funds book.  ALL OUTPUT IS SYNTHETIC.

What it does
  1. Implements the deterministic (mean-path) RFT-TA v2 cohort engine of cluster C2 sec. 4.1 on a quarterly
     grid: calls C = (1 - exp(-lambda*dt)) U with lambda = -ln(1 - RC_s(age)) * m^C(e); distributions
     D = (1 - exp(-delta*dt)) V (1+g)^dt with delta = dbar_s(a^e) * m^D(e),
     dbar_s(a) = -ln[1 - min(0.95, max(Y_s, (a/L_s)^B_s))], a liquidation hazard of 35%/yr once a^e >= L_s,
     and the effective-age clock a^e += kappa(e) dt.  Unfunded expires at the end of age-year 8.
     Strategy parameters: stream 04 sec. 6.4 (buyout, growth, VC); special situations [I].
     Regime multipliers: C2 / stream 04 exit-window table (O, N, D, F), mid-points of the published ranges.
  2. Builds the linear map from a vintage commitment vector c_v (2010-2026; pre-2010 legacy tied to c_2010)
     to the census quantities at 2026-09-30 (NAV, unfunded) and to MSCI-definition H1-2026 rates:
       distribution rate = 2 x (D_Q1 + D_Q2) / NAV_end-2025          (MSCI: "period distributions /
       contribution rate = 2 x (C_Q1 + C_Q2) / (U_end-2025 + new H1    previous valuation, annualized";
                           commitments)                                 "period contributions / (starting dry
                                                                         powder + newly raised), annualized")
  3. Solves LPs (HiGHS) for the maximum census unfunded consistent with NAV = $52bn, the V6 distribution-rate
     band and a pacing-corridor admissibility condition (year-on-year commitment ratio within [1/k, k]).
  4. Evaluates named histories (G1 truth variants and the proposed sealed history) and writes the sealed
     vintage x strategy table.

Run:  .venv\\Scripts\\python.exe -I -B rfta_v2_book.py     (writes rfta_v2_book_results.json + sealed CSV)
SYNTHETIC - NOT ADIC DATA.
"""
from __future__ import annotations

import csv
import json
import math
import os

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "rfta_v2_book_results.json")
OUT_CSV = os.path.join(HERE, "sealed_pe_history_v1_1.csv")

DT = 0.25
BUYOUT_RC = [0.20, 0.25, 0.30, 0.35, 0.40, 0.40, 0.40, 0.40]
STRAT = {  # stream 04 sec. 6.4 defaults; SSI is [I]
    "LBO": dict(rc=BUYOUT_RC, L=16.0, B=2.0, Y=0.0, G=0.11, mix=0.40),
    "MBO": dict(rc=BUYOUT_RC, L=16.0, B=2.0, Y=0.0, G=0.11, mix=0.25),
    "GRO": dict(rc=BUYOUT_RC, L=15.0, B=2.0, Y=0.0, G=0.11, mix=0.12),
    "VC": dict(rc=[0.15, 0.20, 0.25, 0.30, 0.35, 0.35, 0.35, 0.35], L=18.0, B=2.5, Y=0.0, G=0.12, mix=0.08),
    "SEC": dict(rc=BUYOUT_RC, L=16.0, B=2.0, Y=0.0, G=0.11, mix=0.10),
    "SSI": dict(rc=[0.25, 0.30, 0.35, 0.40, 0.40, 0.40, 0.40, 0.40], L=12.0, B=2.0, Y=0.0, G=0.11, mix=0.05),
}
S_KEYS = list(STRAT)
# exit-window regimes (C2 sec. 4.1 table; mid-points of ranges).  g: annual net NAV growth override (None = strategy G)
REG = {
    "O": dict(mD=1.25, mC=1.30, kap=1.2, g=None),
    "N": dict(mD=1.00, mC=1.00, kap=1.0, g=None),
    "D": dict(mD=0.475, mC=0.975, kap=0.6, g=0.07),   # G1 drought growth 7%
    "F": dict(mD=0.325, mC=0.80, kap=0.5, g=-0.10),
}
LIQ_HAZ = -math.log(1 - 0.35)
EXPIRY_YEARS = 8
Q0 = 1998 * 4          # first quarter index (1998Q1)
QCENSUS = 2026 * 4 + 2  # 2026Q3 (0-based quarter within year: Q1=0)
NAV_TARGET = 52.0
U_CENSUS_V10 = 27.4
MSCI_H1_2026 = dict(dist=0.09, contrib=0.31)  # MSCI Private Capital Benchmarks Summary Q2 2026, p.13 / p.16


def hist_regime(qidx: int) -> str:
    y = qidx // 4
    if y <= 2020:
        return "N"
    if y == 2021:
        return "O"
    return "D"


def dbar(s: str, ae: float) -> float:
    p = STRAT[s]
    if ae >= p["L"]:
        return LIQ_HAZ
    rate = min(0.95, max(p["Y"], (ae / p["L"]) ** p["B"]))
    return -math.log(1.0 - rate)


class Cohort:
    """One commitment cohort (strategy s, commitment quarter qc), unit commitment unless scaled.
    age and ae are in years; calls use the age-year index floor(age - delay)."""
    __slots__ = ("s", "qc", "U", "V", "age", "ae", "K", "delay")

    def __init__(self, s: str, qc: int, K: float = 1.0, U=None, V=0.0, age=0.0, ae=0.0, delay=0.0):
        self.s, self.qc, self.K = s, qc, K
        self.U = K if U is None else U
        self.V, self.age, self.ae, self.delay = V, age, ae, delay

    def scaled(self, x: float) -> "Cohort":
        return Cohort(self.s, self.qc, self.K * x, self.U * x, self.V * x, self.age, self.ae, self.delay)

    def step(self, reg: str, dt: float, call_mult: float = 1.0, mC_override: float | None = None,
             mD_override: float | None = None, dist_zero: bool = False, mark: float | None = None) -> tuple[float, float]:
        """Advance one step of length dt (years). Returns (call, distribution).
        mark: if given, the period NAV return (replaces regime growth), e.g. a scenario's private-mark path."""
        r = REG[reg]
        p = STRAT[self.s]
        k = int(math.floor(self.age - self.delay + 1e-9))
        call = 0.0
        if self.U > 0 and 0 <= k < len(p["rc"]):
            mC = r["mC"] if mC_override is None else mC_override
            lam = -math.log(1.0 - p["rc"][k]) * mC * call_mult
            call = (1.0 - math.exp(-lam * dt)) * self.U
            self.U -= call
        if mark is None:
            g = p["G"] if r["g"] is None else r["g"]
            grown = self.V * (1.0 + g) ** dt
        else:
            grown = self.V * (1.0 + mark)
        if dist_zero:
            dist = 0.0
        else:
            mD = r["mD"] if mD_override is None else mD_override
            delta = dbar(self.s, self.ae) * mD
            dist = (1.0 - math.exp(-delta * dt)) * grown
        self.V = grown + call - dist
        self.age += dt
        self.ae += r["kap"] * dt
        if self.age >= EXPIRY_YEARS + self.delay - 1e-9:
            self.U = 0.0
        return call, dist


def unit_history(s: str, qc: int, q_end: int = QCENSUS) -> dict:
    """Quarterly path of a unit cohort committed in quarter qc, to q_end inclusive."""
    c = Cohort(s, qc)
    rows = {}
    for q in range(qc, q_end + 1):
        call, dist = c.step(hist_regime(q), DT)
        rows[q] = (call, dist, c.V, c.U)
    return dict(rows=rows, state=(c.U, c.V, c.age, c.ae))


def build_linear_map(legacy_growth: float = 0.0, first_v: int = 1998) -> dict:
    """Coefficients per vintage v (2010..2026) and strategy s for a unit annual commitment of vintage v,
    spread evenly over the vintage's quarters (2026: Q1-Q3 only, i.e. 3/4 of the annual pace by the census).
    Vintages before 2010 are folded into the 2010 column at c_v = c_2010 (1+legacy_growth)^(v-2010)."""
    vint = list(range(2010, 2027))
    keys = ("nav", "unf", "d_h1", "c_h1", "nav_2025", "unf_2025", "new_h1")
    coef = {s: {k: np.zeros(len(vint)) for k in keys} for s in S_KEYS}
    annual = {s: {} for s in S_KEYS}   # per vintage column: yearly calls, dists, end-NAV, end-U (2010..2026Q3)
    for s in S_KEYS:
        cache = {}
        for v in range(first_v, 2027):
            col = max(0, v - 2010)
            w = 1.0 if v >= 2010 else (1.0 + legacy_growth) ** (v - 2010)
            nq = 3 if v == 2026 else 4
            for qi in range(nq):
                qc = v * 4 + qi
                if qc not in cache:
                    cache[qc] = unit_history(s, qc)
                h = cache[qc]["rows"]
                amt = w * 0.25  # annual pace / 4 per quarter
                cf = coef[s]
                cf["nav"][col] += amt * h[QCENSUS][2]
                cf["unf"][col] += amt * h[QCENSUS][3]
                cf["d_h1"][col] += amt * sum(h[q][1] for q in (2026 * 4, 2026 * 4 + 1) if q in h)
                cf["c_h1"][col] += amt * sum(h[q][0] for q in (2026 * 4, 2026 * 4 + 1) if q in h)
                q25 = 2025 * 4 + 3
                if q25 in h:
                    cf["nav_2025"][col] += amt * h[q25][2]
                    cf["unf_2025"][col] += amt * h[q25][3]
                if v == 2026 and qi in (0, 1):
                    cf["new_h1"][col] += amt
                yr = annual[s].setdefault(col, {})
                for q, (call, dist, V, U) in h.items():
                    y = q // 4
                    if y < 2010:
                        continue
                    a = yr.setdefault(y, [0.0, 0.0, 0.0, 0.0])
                    a[0] += amt * call
                    a[1] += amt * dist
                    if q % 4 == 3 or q == QCENSUS:
                        a[2] += amt * V
                        a[3] += amt * U
    return dict(vint=vint, coef=coef, annual=annual)


def evaluate(cv: np.ndarray, omega: dict, lm: dict) -> dict:
    """cv: annual commitments by vintage 2010..2026 (total, $bn); omega: strategy commitment shares."""
    tot = {k: 0.0 for k in ("nav", "unf", "d_h1", "c_h1", "nav_2025", "unf_2025", "new_h1")}
    by_s = {}
    for s in S_KEYS:
        x = omega[s] * cv
        r = {k: float(lm["coef"][s][k] @ x) for k in tot}
        by_s[s] = r
        for k in tot:
            tot[k] += r[k]
    out = dict(tot)
    out["u_over_nav"] = tot["unf"] / tot["nav"]
    out["dist_rate_h1_2026"] = 2 * tot["d_h1"] / tot["nav_2025"]
    out["contrib_rate_h1_2026"] = 2 * tot["c_h1"] / (tot["unf_2025"] + tot["new_h1"])
    out["nav_mix"] = {s: by_s[s]["nav"] / tot["nav"] for s in S_KEYS}
    return out


def annual_series(cv: np.ndarray, omega: dict, lm: dict) -> dict:
    years = range(2010, 2027)
    res = {y: [0.0, 0.0, 0.0, 0.0] for y in years}
    for s in S_KEYS:
        for col, yr in lm["annual"][s].items():
            x = omega[s] * cv[col]
            for y, a in yr.items():
                for i in range(4):
                    res[y][i] += x * a[i]
    out = {}
    prev_nav = None
    prev_unf = None
    for y in years:
        calls, dists, nav, unf = res[y]
        newc = float(cv[y - 2010]) * (0.75 if y == 2026 else 1.0)
        dr = (dists / prev_nav) if prev_nav else None
        cr = (calls / (prev_unf + newc)) if prev_unf is not None else None
        if y == 2026 and prev_nav:   # Q1-Q3 only: annualize
            dr = dists / prev_nav * 4 / 3
            cr = calls / (prev_unf + newc) * 4 / 3
        out[y] = dict(calls=calls, dists=dists, nav=nav, unf=unf, ncf=dists - calls,
                      dist_rate=dr, contrib_rate=cr)
        prev_nav, prev_unf = nav, unf
    return out


def solve_omega(shape: np.ndarray, lm: dict, iters: int = 30) -> dict:
    """Strategy commitment shares so that the census NAV mix equals STRAT mix for a given vintage shape."""
    om = {s: STRAT[s]["mix"] for s in S_KEYS}
    for _ in range(iters):
        nav_s = {s: float(lm["coef"][s]["nav"] @ (om[s] * shape)) for s in S_KEYS}
        tot = sum(nav_s.values())
        om = {s: om[s] * (STRAT[s]["mix"] / (nav_s[s] / tot)) for s in S_KEYS}
        z = sum(om.values())
        om = {s: om[s] / z for s in S_KEYS}
    return om


def scale_to_nav(shape: np.ndarray, omega: dict, lm: dict) -> np.ndarray:
    nav = sum(float(lm["coef"][s]["nav"] @ (omega[s] * shape)) for s in S_KEYS)
    return shape * NAV_TARGET / nav


def composite(omega: dict, lm: dict) -> dict:
    return {k: sum(omega[s] * lm["coef"][s][k] for s in S_KEYS) for k in lm["coef"][S_KEYS[0]]}


def lp_max_unfunded(omega: dict, lm: dict, rmin: float, rmax: float, corridor: float | None,
                    minimize: bool = False, nav: float = NAV_TARGET) -> dict:
    """max (or min) census unfunded over all vintage vectors with NAV = nav, H1-26 dist rate in [rmin, rmax],
    and c_{v+1}/c_v in [1/corridor, corridor] (2010..2026)."""
    cp = composite(omega, lm)
    n = len(lm["vint"])
    cobj = cp["unf"] if minimize else -cp["unf"]
    A_ub, b_ub = [], []
    A_ub.append(-(2 * cp["d_h1"] - rmin * cp["nav_2025"])); b_ub.append(0.0)
    A_ub.append(2 * cp["d_h1"] - rmax * cp["nav_2025"]); b_ub.append(0.0)
    if corridor is not None:
        for i in range(n - 1):
            row = np.zeros(n); row[i + 1] = 1.0; row[i] = -corridor; A_ub.append(row); b_ub.append(0.0)
            row = np.zeros(n); row[i + 1] = -1.0; row[i] = 1.0 / corridor; A_ub.append(row); b_ub.append(0.0)
    A_eq = [cp["nav"]]; b_eq = [nav]
    res = linprog(cobj, A_ub=np.array(A_ub), b_ub=np.array(b_ub), A_eq=np.array(A_eq), b_eq=np.array(b_eq),
                  bounds=[(0, None)] * n, method="highs")
    if not res.success:
        return dict(status=res.message, feasible=False)
    cv = res.x
    ev = evaluate(cv, omega, lm)
    return dict(feasible=True, unf=ev["unf"], u_over_nav=ev["u_over_nav"], dist_rate=ev["dist_rate_h1_2026"],
                contrib_rate=ev["contrib_rate_h1_2026"], commitments={v: round(float(x), 3) for v, x in zip(lm["vint"], cv)})


def named_shapes() -> dict:
    v = np.arange(2010, 2027)
    sh = {}
    sh["mature_flat"] = np.ones(len(v))
    sh["g7pct"] = 1.07 ** (v - 2010)
    sh["g10_to_2022_then_flat"] = 1.10 ** (np.minimum(v, 2022) - 2010)
    sh["g15pct"] = 1.15 ** (v - 2010)
    sh["g20pct"] = 1.20 ** (v - 2010)
    # industry-shaped: +8%/yr 2010-19, 2020 at trend, 2021-22 boom x1.35, 2023 x0.85 of 2022 then -5%/yr to 2026
    base = 1.08 ** (np.minimum(v, 2020) - 2010)
    ind = base.copy()
    ind[v == 2021] = base[v == 2020][0] * 1.08 * 1.35
    ind[v == 2022] = base[v == 2020][0] * 1.08 ** 2 * 1.35
    lvl23 = ind[v == 2022][0] * 0.80
    for i, yy in enumerate(v):
        if yy >= 2023:
            ind[i] = lvl23 * 0.95 ** (yy - 2023)
    sh["industry_boom_retrench"] = ind
    return sh


def main() -> None:
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "engine": "RFT-TA v2 deterministic mean path, quarterly",
           "msci_h1_2026": MSCI_H1_2026, "census_v1_0": {"nav": NAV_TARGET, "unf": U_CENSUS_V10}}
    lm = build_linear_map(legacy_growth=0.0)
    # 1. named histories
    named = {}
    for name, shape in named_shapes().items():
        om = solve_omega(shape, lm)
        cv = scale_to_nav(shape, om, lm)
        ev = evaluate(cv, om, lm)
        ann = annual_series(cv, om, lm)
        named[name] = dict(omega={s: round(om[s], 4) for s in S_KEYS},
                           commitments={y: round(float(x), 3) for y, x in zip(lm["vint"], cv)},
                           pace_2026=round(float(cv[-1]), 3), unf=round(ev["unf"], 3), u_over_nav=round(ev["u_over_nav"], 4),
                           dist_rate_h1_2026=round(ev["dist_rate_h1_2026"], 4),
                           contrib_rate_h1_2026=round(ev["contrib_rate_h1_2026"], 4),
                           nav_2025=round(ev["nav_2025"], 3),
                           v6_dist_pass=bool(abs(ev["dist_rate_h1_2026"] - 0.09) <= 0.02),
                           v6_contrib_pass=bool(abs(ev["contrib_rate_h1_2026"] - 0.31) <= 0.02),
                           annual={y: {k: (round(val, 4) if isinstance(val, float) else val) for k, val in d.items()}
                                   for y, d in ann.items()})
    res["named"] = named
    # 2. LP frontier (omega from the industry-shaped history; check sensitivity to omega from flat/20%)
    frontier = {}
    for om_name in ("industry_boom_retrench", "mature_flat", "g20pct"):
        om = solve_omega(named_shapes()[om_name], lm)
        for corr in (1.25, 1.5, 2.0, None):
            for rmin in (0.07, 0.08, 0.09):
                key = f"omega={om_name}|corridor={corr}|rmin={rmin}"
                frontier[key] = lp_max_unfunded(om, lm, rmin, 0.11, corr)
    res["lp_frontier_max_unfunded"] = frontier
    # minimum unfunded at the same constraints (feasible band)
    om_ind = solve_omega(named_shapes()["industry_boom_retrench"], lm)
    res["lp_min_unfunded"] = {f"corridor={c}|rmin={r}": lp_max_unfunded(om_ind, lm, r, 0.11, c, minimize=True)
                              for c in (1.5,) for r in (0.07, 0.09)}
    # 3. legacy-growth sensitivity for the LP bound
    lm5 = build_linear_map(legacy_growth=0.05)
    res["lp_legacy_growth_5pct"] = lp_max_unfunded(solve_omega(named_shapes()["industry_boom_retrench"], lm5), lm5,
                                                   0.07, 0.11, 1.5)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    for name, r in named.items():
        print(f"{name:26s} pace26 {r['pace_2026']:6.2f}  U {r['unf']:6.2f}  U/NAV {r['u_over_nav']:.3f}  "
              f"dist_H1 {r['dist_rate_h1_2026']:.3f}  contrib_H1 {r['contrib_rate_h1_2026']:.3f}  "
              f"V6d {r['v6_dist_pass']}  V6c {r['v6_contrib_pass']}")
    for k, v in frontier.items():
        if v.get("feasible"):
            print(f"{k:60s} maxU {v['unf']:6.2f} U/NAV {v['u_over_nav']:.3f} dist {v['dist_rate']:.3f} contrib {v['contrib_rate']:.3f}")
        else:
            print(f"{k:60s} infeasible: {v.get('status')}")
    print("min U:", json.dumps({k: (round(v['unf'], 2) if v.get('feasible') else None) for k, v in res['lp_min_unfunded'].items()}))
    print("legacy 5%:", round(res["lp_legacy_growth_5pct"].get("unf", float('nan')), 2))


if __name__ == "__main__":
    main()
