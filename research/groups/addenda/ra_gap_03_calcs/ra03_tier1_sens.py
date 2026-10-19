"""RA gap 03, step 3b: sensitivity of the marginal Tier-1 cost per barrel to the owner model and the war law.

SYNTHETIC - NOT ADIC DATA. Variants: fiscal breakeven median $65 (more draws in band), no IMF fusion, a longer
war (Weibull k = 0.8) and a shorter one (k = 2.2). Bumps: +10m bbl private look-through (eps 0.38), +10m bbl
public energy equity, and the current ledger.

Usage: python -I ra03_tier1_sens.py <out_json> [n_paths]
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra03_lib as L  # noqa: E402
import ra03_t1oil as T  # noqa: E402
from ra03_tier1_run import LEDGER_NOW, POLICIES  # noqa: E402

E = T.E
N = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
SEED = 20261018
VARIANTS = {"base": {}, "pbe65": {"pbe_median": 65.0}, "no_imf_fusion": {"imf": False},
            "war_long_k0.8": {"k_gw": 0.8}, "war_short_k2.2": {"k_gw": 2.2}}
BUMPS = {"PRIV10": {"PRIV": 10.0, "eps_PRIV": 0.38}, "PUB10": {"PUB": 10.0}, "ledger_now": LEDGER_NOW}


def main():
    t0 = time.time()
    out = {"label": L.LABEL, "n_paths": N, "runs": {}}
    for vk, vkw in VARIANTS.items():
        for mk in ("M1", "M4", "M5", "M6"):
            m = E.MODELS[mk]
            gp = T.gen_paths(m, N, SEED + 1000, **vkw)
            for pk in ("do_nothing", "mix_B"):
                pol = POLICIES[pk]
                base = T.simulate_oil(m, pol, None, n=N, seed=SEED, gen=gp)
                row = {"p_red_pct": round(100 * base["p_red"], 3), "gstar_q99.6": round(base["gstar_q"][0.996], 3),
                       "mean_draw_rate_y1_y2": [round(float(gp["rates"][k].mean() * 100), 2) for k in (0, 1)],
                       "bumps": {}}
                for bk, spec in BUMPS.items():
                    r = T.simulate_oil(m, pol, spec, n=N, seed=SEED, gen=gp)
                    nf = int((r["red"] != base["red"]).sum())
                    row["bumps"][bk] = {"dP_red_pp": round(100 * (r["p_red"] - base["p_red"]), 4),
                                        "se_pp": round(100 * np.sqrt(nf) / N, 4),
                                        "dG*_q99.6_bn": round(r["gstar_q"][0.996] - base["gstar_q"][0.996], 4),
                                        "dCE_bp": round(T.ce_bp(base["w_inv2"], r["w_inv2"]), 4)}
                out["runs"][f"{vk}|{mk}|{pk}"] = row
                b = row["bumps"]
                print(f"[{time.time() - t0:5.0f}s] {vk:15s} {mk} {pk:10s} P(red) {row['p_red_pct']:6.2f}% draws "
                      f"{row['mean_draw_rate_y1_y2']} | PRIV10 dRed {b['PRIV10']['dP_red_pp']:+.3f}"
                      f"(se {b['PRIV10']['se_pp']:.3f}) dCE {b['PRIV10']['dCE_bp']:+.2f} | ledger dRed "
                      f"{b['ledger_now']['dP_red_pp']:+.3f}(se {b['ledger_now']['se_pp']:.3f}) dG* "
                      f"{b['ledger_now']['dG*_q99.6_bn']:+.3f} dCE {b['ledger_now']['dCE_bp']:+.2f}", flush=True)
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == "__main__":
    main()
