"""
gap_02 (groups) - which 2010-2026 PE commitment histories reproduce census v1.0?  SYNTHETIC.

Builds on rfta_v2_book.py (imported read-only).  Three searches:
  A. Smoothest history (minimum squared second difference of log commitments) that hits NAV = 52,
     U = U_target and an H1-2026 distribution rate r (MSCI definition), for several U_target and r.
  B. 'Plan-consistent' grid: log-linear plan with growth g1 (2010-2020), a 2021-22 boom factor b and
     post-boom growth g2 (2023-2026); reports U, rates and diagnostics for every grid point.
  C. Features of each solution: trough year, peak growth, 2026 pace relative to 2019 pace, vintage NAV
     concentration (G1 limit: vintage <= 15% of PE NAV), contribution rate (MSCI definition).

Run:  .venv\\Scripts\\python.exe -I -B history_search.py   -> history_search_results.json
"""
from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rfta_v2_book as rb  # noqa: E402

OUT = os.path.join(HERE, "history_search_results.json")


def features(cv: np.ndarray, om: dict, lm: dict) -> dict:
    v = np.array(lm["vint"])
    ev = rb.evaluate(cv, om, lm)
    lg = np.diff(np.log(np.maximum(cv, 1e-9)))
    # vintage NAV shares at census
    vnav = np.zeros(len(v))
    for s in rb.S_KEYS:
        vnav += lm["coef"][s]["nav"] * om[s] * cv
    shares = vnav / vnav.sum()
    return dict(
        commitments={int(y): round(float(x), 3) for y, x in zip(v, cv)},
        unf=round(ev["unf"], 3), u_over_nav=round(ev["u_over_nav"], 4),
        dist_rate=round(ev["dist_rate_h1_2026"], 4), contrib_rate=round(ev["contrib_rate_h1_2026"], 4),
        trough_year=int(v[int(np.argmin(cv))]), peak_year=int(v[int(np.argmax(cv))]),
        max_yoy_growth=round(float(np.exp(lg.max()) - 1), 4), min_yoy_growth=round(float(np.exp(lg.min()) - 1), 4),
        pace2026_over_pace2019=round(float(cv[-1] / cv[v == 2019][0]), 3),
        pace2026_over_mean_2010_19=round(float(cv[-1] / cv[(v >= 2010) & (v <= 2019)].mean()), 3),
        growth_2022_26_pa=round(float((cv[-1] / cv[v == 2022][0]) ** 0.25 - 1), 4),
        max_vintage_nav_share=round(float(shares.max()), 4), max_vintage_nav_year=int(v[int(np.argmax(shares))]),
        vintage_nav_hhi=round(float((shares ** 2).sum()), 4),
        pre2010_legacy_nav_share=None,
    )


def smoothest(lm: dict, om: dict, u_target: float, r: float, x0: np.ndarray | None = None) -> dict:
    cp = rb.composite(om, lm)
    n = len(lm["vint"])

    def c_of(z):
        return np.exp(z)

    def obj(z):
        d2 = np.diff(z, 2)
        return float(d2 @ d2)

    cons = [
        {"type": "eq", "fun": lambda z: float(cp["nav"] @ c_of(z)) - rb.NAV_TARGET},
        {"type": "eq", "fun": lambda z: float(cp["unf"] @ c_of(z)) - u_target},
        {"type": "eq", "fun": lambda z: float(2 * cp["d_h1"] @ c_of(z) - r * cp["nav_2025"] @ c_of(z))},
    ]
    best = None
    starts = [np.log(np.full(n, 5.0))] if x0 is None else [x0]
    starts += [np.log(np.linspace(8, 4, n)), np.log(np.linspace(3, 12, n)), np.log(4 + 3 * np.cos(np.linspace(0, 2 * np.pi, n)) ** 2)]
    for z0 in starts:
        res = minimize(obj, z0, constraints=cons, method="SLSQP", options=dict(maxiter=2000, ftol=1e-12))
        if res.success and (best is None or res.fun < best.fun):
            best = res
    if best is None:
        return dict(feasible=False)
    cv = c_of(best.x)
    f = features(cv, om, lm)
    f.update(feasible=True, roughness=round(float(best.fun), 5), u_target=u_target, r_target=r)
    return f


def plan_grid(lm: dict) -> list:
    v = np.array(lm["vint"])
    out = []
    for g1, b, g2 in itertools.product(np.arange(-0.10, 0.251, 0.025), (1.0, 1.15, 1.3, 1.5),
                                       np.arange(-0.20, 0.301, 0.05)):
        base = (1 + g1) ** (np.minimum(v, 2020) - 2010)
        lvl20 = base[v == 2020][0]
        sh = base.copy()
        sh[v == 2021] = lvl20 * (1 + g1) * b
        sh[v == 2022] = lvl20 * (1 + g1) ** 2 * b
        l22 = sh[v == 2022][0]
        for i, yy in enumerate(v):
            if yy >= 2023:
                sh[i] = l22 * (1 + g2) ** (yy - 2022)
        om = rb.solve_omega(sh, lm, iters=15)
        cv = rb.scale_to_nav(sh, om, lm)
        ev = rb.evaluate(cv, om, lm)
        out.append(dict(g1=round(float(g1), 3), boom=b, g2=round(float(g2), 3), pace2026=round(float(cv[-1]), 3),
                        unf=round(ev["unf"], 3), u_over_nav=round(ev["u_over_nav"], 4),
                        dist_rate=round(ev["dist_rate_h1_2026"], 4), contrib_rate=round(ev["contrib_rate_h1_2026"], 4)))
    return out


def main() -> None:
    lm = rb.build_linear_map()
    om = rb.solve_omega(rb.named_shapes()["industry_boom_retrench"], lm)
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "omega": om}
    sm = {}
    for u in (14.0, 18.0, 22.0, 27.4, 30.0):
        for r in (0.07, 0.09, 0.11):
            sm[f"U={u}|r={r}"] = smoothest(lm, om, u, r)
    res["smoothest"] = sm
    grid = plan_grid(lm)
    res["plan_grid_n"] = len(grid)
    ok = [g for g in grid if 0.07 <= g["dist_rate"] <= 0.11]
    res["plan_grid_max_u_dist_7_11"] = max(ok, key=lambda g: g["unf"]) if ok else None
    ok9 = [g for g in grid if 0.085 <= g["dist_rate"] <= 0.095]
    res["plan_grid_max_u_dist_8p5_9p5"] = max(ok9, key=lambda g: g["unf"]) if ok9 else None
    # restricted plan class: g2 <= g1 + 0.05 (no acceleration into the drought beyond trend) and boom <= 1.5
    okr = [g for g in ok if g["g2"] <= g["g1"] + 0.05 + 1e-9]
    res["plan_grid_max_u_dist_7_11_no_drought_acceleration"] = max(okr, key=lambda g: g["unf"]) if okr else None
    hit = [g for g in grid if abs(g["unf"] - 27.4) <= 1.0]
    res["plan_grid_points_with_U_27p4_pm1"] = sorted(hit, key=lambda g: -g["dist_rate"])[:12]
    res["plan_grid"] = grid
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    for k, f in sm.items():
        if not f.get("feasible"):
            print(k, "infeasible")
            continue
        print(f"{k:16s} rough {f['roughness']:.4f} trough {f['trough_year']} 26/19 {f['pace2026_over_pace2019']:.2f} "
              f"g22-26 {f['growth_2022_26_pa']:+.3f} maxyoy {f['max_yoy_growth']:+.3f} minyoy {f['min_yoy_growth']:+.3f} "
              f"contrib {f['contrib_rate']:.3f} maxvint {f['max_vintage_nav_share']:.3f}({f['max_vintage_nav_year']})")
        print("    ", " ".join(f"{y}:{c:.1f}" for y, c in f["commitments"].items()))
    print("plan max U (dist 7-11%):", res["plan_grid_max_u_dist_7_11"])
    print("plan max U (dist 8.5-9.5%):", res["plan_grid_max_u_dist_8p5_9p5"])
    print("plan max U (dist 7-11%, g2<=g1+5%):", res["plan_grid_max_u_dist_7_11_no_drought_acceleration"])
    print("plan points with U ~27.4:")
    for g in res["plan_grid_points_with_U_27p4_pm1"]:
        print("   ", g)


if __name__ == "__main__":
    main()
