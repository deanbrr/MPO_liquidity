"""G12 check: L_eff and draw statistics at low effective breakevens (P^BE 35 and 40). SYNTHETIC [I-MC].
Usage: python -I g12_low_breakeven_check.py <out_json>
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g12_wrongway_sim import KAPPA, PLR, PZ, analyse, simulate, stationary  # noqa: E402


def main():
    pi = stationary(PZ)
    phi, r, b = 1 - KAPPA, 0.06, 0.625
    ann = 1.0 / (1.0 - phi / (1 + r))
    out = {"label": "SYNTHETIC [I-MC]"}
    for pbe in (35.0, 40.0):
        sim = simulate(40000, 12, seed=12 + int(pbe), z0_probs=pi, p0=PLR, PBE=pbe)
        seg, draw = analyse(sim, burn=2)
        pin = draw["p_inband_dstar"]
        out[f"PBE{pbe}"] = {"mean_draw": draw["mean_draw"], "p_inband": pin,
                            "L_eff_pct_nav_h0.10": round(100 * b * 0.10 * pin * ann, 2),
                            "Hd_kappa0.5_pdp": seg["pdp"]["Hd_kappa0.5"], "Hd_kappa0.5_lev": seg["lev"]["Hd_kappa0.5"]}
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
