"""
gap_02 (groups) - select and seal the census v1.1 PE commitment history and the truth variants.  SYNTHETIC.

Selection rule (pre-stated):
  family    = plan-consistent industry shape: growth g1 (2010-2020), 2021-22 boom x1.5 (cap), no 2023 step,
              post-boom growth g2 (2023-2026), strategy commitment shares solved so the census NAV mix equals
              the sec. 3.1 strategy mix;
  targets   = NAV $52bn at 2026-09-30; H1-2026 distribution rate = 9.0% (MSCI point); H1-2026 contribution
              rate >= 29.0% (MSCI 31% - 2pp);
  choice    = the member with the largest census unfunded (the liquidity-conservative choice).
Truth variants (G1 sec. 4.2 histories re-run on RFT-TA v2): mature (flat), 10%/yr to 2022 then flat,
20%/yr growth; plus 'v1.0 reproduction' (smoothest history hitting U = 27.4, 9.0%) for continuity.
Writes sealed_pe_history_v1_1.csv (vintage x strategy commitments, census U and NAV by vintage),
seal_history_results.json and the SHA-256 of the CSV (the seal).
Run:  .venv\\Scripts\\python.exe -I -B seal_history.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rfta_v2_book as rb  # noqa: E402
import history_search as hs  # noqa: E402

OUT_JSON = os.path.join(HERE, "seal_history_results.json")
OUT_CSV = os.path.join(HERE, "sealed_pe_history_v1_1.csv")
BOOM = 1.5


def industry_shape(v, g1, g2, boom=BOOM):
    base = (1 + g1) ** (np.minimum(v, 2020) - 2010)
    sh = base.copy()
    l20 = base[v == 2020][0]
    sh[v == 2021] = l20 * (1 + g1) * boom
    sh[v == 2022] = l20 * (1 + g1) ** 2 * boom
    for i, y in enumerate(v):
        if y >= 2023:
            sh[i] = sh[v == 2022][0] * (1 + g2) ** (y - 2022)
    return sh


def build(lm, shape):
    om = rb.solve_omega(shape, lm, iters=40)
    cv = rb.scale_to_nav(shape, om, lm)
    return om, cv, rb.evaluate(cv, om, lm)


def vintage_tables(lm, om, cv):
    """census NAV and unfunded by vintage and strategy."""
    rows = []
    for i, y in enumerate(lm["vint"]):
        row = {"vintage": y}
        for s in rb.S_KEYS:
            x = om[s] * cv[i]
            row[f"commit_{s}"] = x
            row[f"nav_{s}"] = lm["coef"][s]["nav"][i] * om[s] * cv[i]
            row[f"unf_{s}"] = lm["coef"][s]["unf"][i] * om[s] * cv[i]
        row["commit_total"] = float(cv[i]) * (0.75 if y == 2026 else 1.0)
        row["commit_pace_annual"] = float(cv[i])
        row["nav_total"] = sum(row[f"nav_{s}"] for s in rb.S_KEYS)
        row["unf_total"] = sum(row[f"unf_{s}"] for s in rb.S_KEYS)
        rows.append(row)
    return rows


def main():
    lm = rb.build_linear_map()
    v = np.array(lm["vint"])
    cands = []
    for g1 in np.arange(-0.02, 0.121, 0.01):
        def f(g2):
            _, _, ev = build(lm, industry_shape(v, g1, g2))
            return ev["dist_rate_h1_2026"] - 0.09
        try:
            g2 = brentq(f, -0.30, 0.30, xtol=1e-5)
        except ValueError:
            continue
        om, cv, ev = build(lm, industry_shape(v, g1, g2))
        cands.append(dict(g1=round(float(g1), 3), g2=round(float(g2), 4), unf=ev["unf"], dist=ev["dist_rate_h1_2026"],
                          contrib=ev["contrib_rate_h1_2026"], pace2026=float(cv[-1])))
    ok = [c for c in cands if c["contrib"] >= 0.29]
    pick = max(ok, key=lambda c: c["unf"])
    # refine: along the dist = 9.0% curve, U falls and the contribution rate rises with g1, so the largest-U
    # admissible member sits where the contribution rate equals 29.0%; bracket it between grid points.
    lo = max((c for c in cands if c["contrib"] < 0.29), key=lambda c: c["g1"], default=None)
    if lo is not None and lo["g1"] < pick["g1"]:
        def g2_of(g1):
            return brentq(lambda g2: build(lm, industry_shape(v, g1, g2))[2]["dist_rate_h1_2026"] - 0.09,
                          -0.30, 0.30, xtol=1e-6)

        def h(g1):
            return build(lm, industry_shape(v, g1, g2_of(g1)))[2]["contrib_rate_h1_2026"] - 0.29
        g1s = brentq(h, lo["g1"], pick["g1"], xtol=1e-5)
        g1s = float(np.ceil(g1s * 1e4) / 1e4)        # round up so the contribution floor holds
        g2s = g2_of(g1s)
        _, cvr, evr = build(lm, industry_shape(v, g1s, g2s))
        pick = dict(g1=round(g1s, 4), g2=round(float(g2s), 4), unf=evr["unf"], dist=evr["dist_rate_h1_2026"],
                    contrib=evr["contrib_rate_h1_2026"], pace2026=float(cvr[-1]))
    om, cv, ev = build(lm, industry_shape(v, pick["g1"], pick["g2"]))
    rows = vintage_tables(lm, om, cv)
    # CSV (the sealed table) and its hash
    buf = io.StringIO()
    fields = ["vintage", "commit_pace_annual", "commit_total"] + [f"commit_{s}" for s in rb.S_KEYS] + \
             ["nav_total", "unf_total"] + [f"nav_{s}" for s in rb.S_KEYS] + [f"unf_{s}" for s in rb.S_KEYS]
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: (f"{r[k]:.4f}" if isinstance(r[k], float) else r[k]) for k in fields})
    text = "# SYN-ADIC-177 census v1.1 PE-funds commitment history (USD bn). SYNTHETIC - NOT ADIC DATA.\n" + buf.getvalue()
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    ann = rb.annual_series(cv, om, lm)
    # truth variants
    variants = {}
    for name in ("mature_flat", "g10_to_2022_then_flat", "g20pct"):
        sh = rb.named_shapes()[name]
        o, c, e = build(lm, sh)
        variants[name] = dict(omega=o, commitments=[float(x) for x in c], pace2026=float(c[-1]), unf=e["unf"],
                              u_over_nav=e["u_over_nav"], dist=e["dist_rate_h1_2026"], contrib=e["contrib_rate_h1_2026"])
    rep = hs.smoothest(lm, om, 27.4, 0.09)
    variants["v1_0_reproduction"] = dict(commitments=[rep["commitments"][y] for y in lm["vint"]],
                                         pace2026=rep["commitments"][2026], unf=rep["unf"], u_over_nav=rep["u_over_nav"],
                                         dist=rep["dist_rate"], contrib=rep["contrib_rate"],
                                         growth_2022_26_pa=rep["growth_2022_26_pa"], omega=om)
    out = dict(label="SYNTHETIC - NOT ADIC DATA", rule=__doc__.split("Selection rule (pre-stated):")[1].split("Truth variants")[0].strip(),
               candidates=cands, sealed=dict(g1=pick["g1"], g2=pick["g2"], boom=BOOM, omega=om,
                                             commitments={int(y): float(x) for y, x in zip(v, cv)},
                                             pace2026=float(cv[-1]), census=dict(nav=ev["nav"], unf=ev["unf"],
                                             u_over_nav=ev["u_over_nav"], dist_h1_2026=ev["dist_rate_h1_2026"],
                                             contrib_h1_2026=ev["contrib_rate_h1_2026"], nav_mix=ev["nav_mix"],
                                             nav_2025=ev["nav_2025"], unf_2025=ev["unf_2025"]),
                                             vintage_rows=rows, annual={int(k): d for k, d in ann.items()},
                                             csv=os.path.basename(OUT_CSV), sha256=sha),
               variants=variants)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=float)
    print("candidates (g1, g2, U, dist, contrib, pace26):")
    for c in cands:
        print(f"   {c['g1']:+.2f} {c['g2']:+.4f} U {c['unf']:.2f} d {c['dist']:.4f} c {c['contrib']:.4f} pace {c['pace2026']:.2f}")
    print("SEALED:", pick, "sha256", sha)
    print("omega:", {s: round(x, 4) for s, x in om.items()})
    print("vintage rows (commit pace, NAV, U):")
    for r in rows:
        print(f"   {r['vintage']}: pace {r['commit_pace_annual']:.2f}  NAV {r['nav_total']:.2f}  U {r['unf_total']:.2f}")
    print("annual book rates:")
    for y, d in ann.items():
        print(f"   {y}: calls {d['calls']:.2f} dists {d['dists']:.2f} NAV {d['nav']:.2f} U {d['unf']:.2f} "
              f"dr {d['dist_rate'] if d['dist_rate'] is None else round(d['dist_rate'], 3)} cr {d['contrib_rate'] if d['contrib_rate'] is None else round(d['contrib_rate'], 3)}")
    for k, x in variants.items():
        print(k, {kk: (round(vv, 4) if isinstance(vv, float) else None) for kk, vv in x.items() if kk in ("pace2026", "unf", "u_over_nav", "dist", "contrib", "growth_2022_26_pa")})


if __name__ == "__main__":
    main()
