"""
gap_02: exposure-neutral frontier. Minimise the expected gross premium (fees + interest + reserve carry at the
model ERP + pre-emptive amber discount + pacing beyond-horizon cost + owner cost of band use) subject to the same
joint gates as gap02_frontier.py. Complements the CE frontier, whose CRRA(3) metric also rewards de-risking.
SYNTHETIC - NOT ADIC DATA. Reads gap02_grid_raw.json; writes gap02_premium_frontier.json.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gap02_frontier import SCOPES, feasible, g_ce, outside_bp, premium_bp  # noqa: E402

EPS = (0.0025, 0.005, 0.01, 0.015, 0.02, 0.03, 0.05, 0.10)


def main():
    raw = json.load(open(os.path.join(HERE, "gap02_grid_raw.json")))
    rows = raw["grid"]
    by = {r["kw"]["name"]: r for r in rows}
    ref = by[raw["reference"]]
    out = {}
    for band_ok in (False, True):
        for scope in ("all6", "M1-M5", "mixture"):
            models = SCOPES.get(scope, SCOPES["all6"])
            pool = [r for r in rows if band_ok or not r["kw"]["band"]]
            pts = []
            for eps in EPS:
                c = [r for r in pool if feasible(r, eps, scope, "0.76")[0]]
                if not c:
                    pts.append(dict(eps=eps, feasible=False))
                    continue
                b = min(c, key=lambda r: premium_bp(r, models)["total"])
                pts.append(dict(eps=eps, feasible=True, mix=b["kw"]["name"], premium=premium_bp(b, models),
                                ce_vs_ref=(g_ce(ref, models) - g_ce(b, models)) * 1e4 + outside_bp(b, models)
                                - outside_bp(ref, models),
                                p_red={k: b["models"][k]["p_red"] for k in models},
                                p_band12={k: b["models"][k]["p_band_12m"] for k in models},
                                withheld={k: b["models"][k]["mean_withheld"] for k in models}))
            out[f"band={band_ok}|scope={scope}"] = pts
    with open(os.path.join(HERE, "gap02_premium_frontier.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    for k, pts in out.items():
        print(k)
        for p in pts:
            if p["feasible"]:
                print(f"   {p['eps']*100:.3g}%: premium {p['premium']['total']:.1f}bp "
                      f"(fees {p['premium']['fees_interest']:.1f}, reserve {p['premium']['reserve_carry']:.1f}, "
                      f"pace {p['premium']['pacing_tv']:.1f}, owner {p['premium']['owner']:.1f}, amber {p['premium']['amber_t0_discount']:.1f}) "
                      f"CEvsRef {p['ce_vs_ref']:.1f} [{p['mix']}] maxP {max(p['p_red'].values())*100:.2f}% "
                      f"band12 max {max(p['p_band12'].values())*100:.0f}%")
            else:
                print(f"   {p['eps']*100:.3g}%: infeasible")


if __name__ == "__main__":
    main()
