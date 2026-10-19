"""G12: oil delta and supply-glut loss of the SYNTHETIC energy & natural-resources (ENR) sleeve, versus the
overlay's oil put-spread programme. ALL OUTPUTS SYNTHETIC [I-calc]. Not ADIC data.

Sleeve sizes follow stream G15's synthetic book (ENR_CE $1.6bn closed-end funds, ENR_DIR $0.9bn direct/co-invest,
working allocation v2). The sub-segment split below is a G12 [I] assumption.

Usage: python -I g12_enr_book.py <sim_json> <episodes_json> <out_json>
"""
from __future__ import annotations

import json
import math
import sys


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def black76_put(F, K, vol, T, r=0.04):
    if K <= 0:
        return 0.0
    s = vol * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * s * s) / s
    d2 = d1 - s
    return math.exp(-r * T) * (K * ncdf(-d2) - F * ncdf(-d1))


def main():
    sim = json.load(open(sys.argv[1], encoding="utf-8"))
    eps = json.load(open(sys.argv[2], encoding="utf-8"))
    out_path = sys.argv[3]
    el = sim["elasticities"]["N_at_70"]
    seg = sim["runs"]["stationary_PBE55.0_log"]["segments"]
    # [I] split of the $2.5bn ENR sleeve into model segments
    split = {  # USD bn
        "lev": 0.80 + 0.27,   # upstream oil-weighted equity with RBL-type leverage (funds 0.80, direct non-op 0.27)
        "roy": 0.18,          # mineral & royalty interests (direct)
        "mid": 0.40 + 0.45,   # fee-based midstream / gas infrastructure (funds 0.40, JV 0.45)
        "other": 0.40,        # services, metals/mining and transition assets (oil beta ~0.1 assumed)
    }
    other_bbl_per_bn = 1.0   # [I] ~0.07 elasticity at $70
    delta = {k: v * (el[k]["bbl_equiv_per_usd1bn_mm"] if k in el else other_bbl_per_bn) for k, v in split.items()}
    total_delta = sum(delta.values())
    # supply-glut (SG) one-year loss relative to the N state, from the stationary simulation by-Z means
    sg_rel = {}
    for k, v in split.items():
        if k in seg:
            sg_rel[k] = v * (seg[k]["by_Z"]["SG"]["ret"] - seg[k]["by_Z"]["N"]["ret"])
        else:
            sg_rel[k] = v * (-0.05)  # [I]
    # listed analogue: 2014-06..2016-01, Oil industry -38.5% vs market -0.6%
    ep = eps["episodes"]["oil_bust_2014-06_2016-01"]
    listed_loss = 2.5 * ep["Oil"]
    # put-spread programme payoff in a glut at Brent $45 (kinks: long 64 / short 31, log-form draw rule)
    payoff = {f"{n}m_bbl": round(n * 1e6 * (64 - max(45, 31)) / 1e9, 3) for n in (20, 40)}
    # Black-76 cost per bbl of a 1-year 64/31 put spread for forwards 84 (EIA 2027 avg proxy) and 70
    cost = {}
    for F in (84.0, 70.0):
        for vol in (0.35, 0.55, 0.70):
            c = black76_put(F, 64, vol, 1.0) - black76_put(F, 31, vol, 1.0)
            cost[f"F{F:.0f}_vol{vol}"] = round(c, 2)
    # cost of carrying the sleeve's delta through linear swaps is ~0 premium but VM in oil-up states;
    # options-equivalent illustrative carry: delta (m bbl) x put-spread cost / sleeve NAV
    carry = {k: round(total_delta * 1e6 * v / 2.5e9, 4) for k, v in cost.items()}
    res = {"label": "SYNTHETIC [I-calc]", "sleeve_split_usd_bn": split,
           "oil_delta_m_bbl_by_segment": {k: round(v, 2) for k, v in delta.items()},
           "oil_delta_total_m_bbl": round(total_delta, 2),
           "share_of_inband_draw_delta_201m_bbl": round(total_delta / 201.0, 3),
           "share_of_put_spread_programme_20_40m_bbl": [round(total_delta / 20, 2), round(total_delta / 40, 2)],
           "sg_one_year_loss_vs_N_usd_bn": {k: round(v, 3) for k, v in sg_rel.items()},
           "sg_one_year_loss_vs_N_total_usd_bn": round(sum(sg_rel.values()), 3),
           "listed_2014_16_analogue_loss_usd_bn": round(listed_loss, 3),
           "put_spread_payoff_at_brent45_usd_bn": payoff,
           "put_spread_64_31_cost_usd_per_bbl": cost,
           "options_equivalent_carry_pct_of_sleeve_nav": carry}
    json.dump(res, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
