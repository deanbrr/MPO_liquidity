"""G12 check: sensitivity of L_eff to the owner's draw slope b (0.625 vs 1.25), P^BE $55. SYNTHETIC [I-MC].
Usage: python -I g12_slope_check.py <out_json>
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g12_wrongway_sim import KAPPA, PLR, PZ, analyse, simulate, stationary  # noqa: E402


def main():
    pi = stationary(PZ)
    ann = 1.0 / (1.0 - (1.0 - KAPPA) / 1.06)
    out = {"label": "SYNTHETIC [I-MC]"}
    for bb in (0.625, 1.25):
        sim = simulate(40000, 12, seed=77, z0_probs=pi, p0=PLR, PBE=55.0, b=bb)
        seg, draw = analyse(sim, burn=2)
        out[f"b{bb}"] = {"p_inband": draw["p_inband_dstar"],
                         "L_eff_pct_nav": round(100 * bb * 0.10 * draw["p_inband_dstar"] * ann, 2),
                         "Hd05_pdp": seg["pdp"]["Hd_kappa0.5"], "mean_draw": draw["mean_draw"]}
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
