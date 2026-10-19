"""G12 check: oil delta of the SYNTHETIC ENR sleeve after a 70% 3-year asset-level hedge on the levered upstream.
SYNTHETIC [I-calc]. Usage: python -I g12_check_hedged_sleeve.py <enr_json> <out_json>
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g12_wrongway_sim import PDP, ZI, fwd_curve, pdp_value  # noqa: E402


def main():
    enr = json.load(open(sys.argv[1], encoding="utf-8"))
    p0 = 70.0
    x = np.array([np.log(p0)])
    z = np.array([ZI["N"]])
    age = np.zeros(1)
    v0, v1 = pdp_value(x, z, age)[0], pdp_value(x + 0.01, z, age)[0]
    nf = PDP["nri"] * (1 - PDP["tax"])
    q = np.exp(-PDP["decline"] * (np.arange(1, 4) - 0.5))
    disc = (1 + PDP["disc"]) ** -(np.arange(1, 4) - 0.5)
    dF = fwd_curve(x + 0.01, z)[0, :3] - fwd_curve(x, z)[0, :3]
    dmtm = -(0.70 * q * nf * dF * disc).sum()
    D = 0.40 * v0
    el_lev_unhedged = ((v1 - D) / (v0 - D) - 1) / 0.01
    el_lev_hedged = ((v1 + dmtm - D) / (v0 - D) - 1) / 0.01
    lev_bn = enr["sleeve_split_usd_bn"]["lev"]
    others = sum(v for k, v in enr["oil_delta_m_bbl_by_segment"].items() if k != "lev")
    d_unh = lev_bn * el_lev_unhedged * 1000 / p0 + others
    d_h = lev_bn * el_lev_hedged * 1000 / p0 + others
    res = {"label": "SYNTHETIC [I-calc]", "lev_equity_elasticity_unhedged": round(el_lev_unhedged, 3),
           "lev_equity_elasticity_hedged70_3y": round(el_lev_hedged, 3),
           "sleeve_delta_unhedged_m_bbl": round(d_unh, 2), "sleeve_delta_after_hedge_m_bbl": round(d_h, 2),
           "sleeve_delta_after_selling_0.6_0.8bn_lev_m_bbl": [round(d_unh - s * el_lev_unhedged * 1000 / p0, 2) for s in (0.6, 0.8)]}
    json.dump(res, open(sys.argv[2], "w", encoding="utf-8"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
