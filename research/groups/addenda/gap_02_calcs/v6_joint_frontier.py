"""
gap_02 (groups) - joint V6 frontier: maximum census PE unfunded consistent with NAV = $52bn and BOTH halves of
gate V6 (distribution AND contribution rate vs MSCI), plus the plan-consistent sealed-history candidates.
SYNTHETIC - NOT ADIC DATA.

Bands tested (MSCI Private Capital Benchmarks Summary Q2 2026, PE: distribution 9% / contribution 31% in H1-2026;
2022-2025 distribution 11/9/11/11%, contribution 31/27/28/29%):
  H1:   distribution 9% +/- 2pp, contribution 31% +/- 2pp           (V6 read point-by-point)
  AVG:  distribution 9% +/- 2pp, contribution 29.2% +/- 2pp         (contribution vs the 2022-H1 2026 mean)
LPs maximize unfunded under a year-on-year pacing corridor k (1.25 = G1 normal corridor; 1.5 = IC override).
Run:  .venv\\Scripts\\python.exe -I -B v6_joint_frontier.py  -> v6_joint_frontier_results.json
"""
from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rfta_v2_book as rb  # noqa: E402

OUT = os.path.join(HERE, "v6_joint_frontier_results.json")
BANDS = {"H1": dict(d=(0.07, 0.11), c=(0.29, 0.33)), "AVG": dict(d=(0.07, 0.11), c=(0.272, 0.312))}


def lp_joint(lm, om, band, corridor, d_point=None):
    cp = rb.composite(om, lm)
    n = len(lm["vint"])
    A, b = [], []
    dlo, dhi = band["d"] if d_point is None else (d_point, d_point)
    clo, chi = band["c"]
    A.append(-(2 * cp["d_h1"] - dlo * cp["nav_2025"])); b.append(0.0)
    A.append(2 * cp["d_h1"] - dhi * cp["nav_2025"]); b.append(0.0)
    den = cp["unf_2025"] + cp["new_h1"]
    A.append(-(2 * cp["c_h1"] - clo * den)); b.append(0.0)
    A.append(2 * cp["c_h1"] - chi * den); b.append(0.0)
    if corridor is not None:
        for i in range(n - 1):
            r = np.zeros(n); r[i + 1] = 1; r[i] = -corridor; A.append(r); b.append(0.0)
            r = np.zeros(n); r[i + 1] = -1; r[i] = 1 / corridor; A.append(r); b.append(0.0)
    res = linprog(-cp["unf"], A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array([cp["nav"]]), b_eq=[rb.NAV_TARGET],
                  bounds=[(0, None)] * n, method="highs")
    if not res.success:
        return dict(feasible=False, status=res.message)
    ev = rb.evaluate(res.x, om, lm)
    return dict(feasible=True, unf=round(ev["unf"], 2), u_over_nav=round(ev["u_over_nav"], 3),
                dist=round(ev["dist_rate_h1_2026"], 4), contrib=round(ev["contrib_rate_h1_2026"], 4),
                pace2026=round(float(res.x[-1]), 2), commitments={y: round(float(x), 2) for y, x in zip(lm["vint"], res.x)})


def shape_industry(v, g1, boom, drop23, g2):
    base = (1 + g1) ** (np.minimum(v, 2020) - 2010)
    sh = base.copy()
    l20 = base[v == 2020][0]
    sh[v == 2021] = l20 * (1 + g1) * boom
    sh[v == 2022] = l20 * (1 + g1) ** 2 * boom
    l23 = sh[v == 2022][0] * drop23
    for i, y in enumerate(v):
        if y >= 2023:
            sh[i] = l23 * (1 + g2) ** (y - 2023)
    return sh


def main():
    lm = rb.build_linear_map()
    v = np.array(lm["vint"])
    om = rb.solve_omega(rb.named_shapes()["industry_boom_retrench"], lm)
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "bands": BANDS}
    lp = {}
    for bname, band in BANDS.items():
        for corr in (1.25, 1.5, None):
            lp[f"{bname}|corridor={corr}"] = lp_joint(lm, om, band, corr)
            lp[f"{bname}|corridor={corr}|dist=9.0%"] = lp_joint(lm, om, band, corr, d_point=0.09)
    res["lp_joint_v6"] = lp
    # plan-consistent industry-shaped family: g1 2010-20, boom 2021-22, 2023 step drop23, g2 2023-26
    fam = []
    for g1, boom, drop23, g2 in itertools.product(np.arange(0.0, 0.151, 0.01), (1.0, 1.2, 1.35, 1.5),
                                                  (0.7, 0.8, 0.9, 1.0), np.arange(-0.10, 0.101, 0.025)):
        sh = shape_industry(v, g1, boom, drop23, g2)
        o = rb.solve_omega(sh, lm, iters=12)
        cv = rb.scale_to_nav(sh, o, lm)
        ev = rb.evaluate(cv, o, lm)
        fam.append(dict(g1=round(float(g1), 3), boom=boom, drop23=drop23, g2=round(float(g2), 3),
                        pace2026=round(float(cv[-1]), 3), unf=round(ev["unf"], 3), u_over_nav=round(ev["u_over_nav"], 4),
                        dist=round(ev["dist_rate_h1_2026"], 4), contrib=round(ev["contrib_rate_h1_2026"], 4)))
    res["industry_family_n"] = len(fam)
    for bname, band in BANDS.items():
        ok = [f for f in fam if band["d"][0] <= f["dist"] <= band["d"][1] and band["c"][0] <= f["contrib"] <= band["c"][1]]
        res[f"industry_family_maxU_{bname}"] = max(ok, key=lambda f: f["unf"]) if ok else None
        ok9 = [f for f in ok if abs(f["dist"] - 0.09) <= 0.0025]
        res[f"industry_family_maxU_{bname}_dist9"] = max(ok9, key=lambda f: f["unf"]) if ok9 else None
        res[f"industry_family_count_{bname}"] = len(ok)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    for k, r in lp.items():
        if r["feasible"]:
            print(f"{k:34s} maxU {r['unf']:6.2f} U/NAV {r['u_over_nav']:.3f} dist {r['dist']:.3f} contrib {r['contrib']:.3f} pace26 {r['pace2026']:.2f}")
            print("      ", " ".join(f"{y}:{c:.1f}" for y, c in r["commitments"].items()))
        else:
            print(k, "infeasible")
    for bname in BANDS:
        print(bname, "industry max U:", res[f"industry_family_maxU_{bname}"], "count", res[f"industry_family_count_{bname}"])
        print(bname, "industry max U at dist~9%:", res[f"industry_family_maxU_{bname}_dist9"])


if __name__ == "__main__":
    main()
