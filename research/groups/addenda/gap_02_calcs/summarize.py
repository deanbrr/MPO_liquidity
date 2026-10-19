"""Print the figures quoted in gap_02.md from the result JSONs (no new computation except ratios).  SYNTHETIC."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import rfta_v2_book as rb  # noqa: E402

R = json.load(open(os.path.join(HERE, "gap02_rerun_results.json"), encoding="utf-8"))
S = json.load(open(os.path.join(HERE, "seal_history_results.json"), encoding="utf-8"))
cm = R["cashmap"]
print("CASH MAP (12m): key | PE d/c/net | private net | before payout | liquid funding 5/7.5/10 (share)")
for k in ("v1.0_rate", "sealed", "sealed_gs_pace7.2", "mature_flat", "g10_to_2022_then_flat", "g20pct",
          "v1_0_reproduction", "v1_0_reproduction_gs_pace7.2"):
    for scn in ("drought", "S1", "T14", "normal"):
        r = cm[f"{k}|{scn}"]
        lf = r["liquid_funding"]
        ls = r["liquid_share"]
        print(f"{k:30s} {scn:7s} PE {r['dist_by_group']['pe']:5.2f}/{r['calls_by_group']['pe']:5.2f}/{r['net_by_group']['pe']:+6.2f}"
              f"  priv {r['private_net']:+6.2f}  before {r['before_payout']:+6.2f}  fund {lf['5%']:5.1f}/{lf['7.5%']:5.1f}/{lf['10%']:5.1f}"
              f" ({ls['5%']:.0%}/{ls['7.5%']:.0%}/{ls['10%']:.0%})  PE share of drain {r['net_by_group']['pe'] / r['private_net']:.0%}")
r = cm["sealed_g7_crisis_dist|S1"]
print("sealed S1 at G7 crisis distribution:", round(r["dist_by_group"]["pe"], 2), round(r["net_by_group"]["pe"], 2), round(r["private_net"], 2), "mD", round(r["crisis_mD"], 3))
others = {k: sum(cm[f"sealed|drought"]["net_by_group"][g] for g in ("sec", "co", "cs", "pc")) for k in ["x"]}
print("four non-PE groups drought net:", round(others["x"], 2))
print("\nLADDERS:")
for k, v in R["ladders"].items():
    print(f"{k:46s} SH4 {v['SH_TP_floor4']}  fac24 {v['facility_24m']:5.1f}  cover24 {v['cover24_tp_floor4']:.2f} need12 {v['need_12m']:.1f} need24 {v['need_24m']:.1f}")
print("\nPACE:")
for b, v in R["pace_levers"].items():
    for lev in ("pause_2027", "pause_2027_28", "halve_2027_28"):
        x = v[lev]
        print(f"{b:12s} {lev:14s} forgone {x['forgone']:5.2f} y1 {x['d_ncf_2027']:+.2f} ({x['d_ncf_2027']/x['forgone']:.1%}) 4y {x['d_ncf_2027_30']:+.2f} ({x['share_4y']:.0%}) "
              f"2027-40 {x['d_ncf_2027_40']:+.2f} irr {x['implied_irr']:.1%} dNAV31 {x['d_nav_2031_pct']:+.1%}")
print("\nCO-INVEST FLOW:")
for b, v in R["coinvest_flow"].items():
    h = v["hold_pace"]
    p = v["pause_2027"]
    print(f"{b:20s} 2026 offered {h['2026']['offered']:.2f} acc {h['2026']['accepted_lo']:.2f}-{h['2026']['accepted_hi']:.2f}; "
          f"2027 hold {h['2027']['accepted_lo']:.2f}-{h['2027']['accepted_hi']:.2f}; pause {p['2027']['accepted_lo']:.2f}-{p['2027']['accepted_hi']:.2f}; "
          f"2028 pause {p['2028']['accepted_lo']:.2f}-{p['2028']['accepted_hi']:.2f}; steady {v['steady_state_at_pace']['accepted_lo']:.2f}-{v['steady_state_at_pace']['accepted_hi']:.2f}; "
          f"pace for 3bn {v['pace_needed_for_3bn_accepted']['at_a0_6']:.1f}-{v['pace_needed_for_3bn_accepted']['at_a0_3']:.1f}")
print("\nL8:", {k: (round(v["ratio"], 3), round(v["headroom_bn"], 1)) for k, v in R["L8_0p80W"].items()})
# industry ratio and book ratios
print("\nMSCI-implied industry (dry powder + new)/(prior valuation), H1-2026:", round((2 * 228 / 0.31) / (2 * 211 / 0.09), 3))
lm = rb.build_linear_map()
for name, vv in [("sealed", None)] + [(k, S["variants"][k]) for k in S["variants"]]:
    if name == "sealed":
        com = np.array([S["sealed"]["commitments"][str(y)] for y in range(2010, 2027)])
        om = S["sealed"]["omega"]
    else:
        com = np.array(vv["commitments"])
        om = vv["omega"]
    ev = rb.evaluate(com, om, lm)
    print(f"{name:24s} U {ev['unf']:.2f} (dry powder+new)/NAV_2025 {(ev['unf_2025'] + ev['new_h1']) / ev['nav_2025']:.3f}  U_2025/NAV_2025 {ev['unf_2025'] / ev['nav_2025']:.3f}")
ann = S["sealed"]["annual"]
print("sealed annual dist rates:", {y: (round(d["dist_rate"], 3) if d["dist_rate"] else None) for y, d in ann.items()})
print("sealed commitments:", {y: round(x, 2) for y, x in S["sealed"]["commitments"].items()})
print("omega:", {k: round(x, 3) for k, x in S["sealed"]["omega"].items()})
rows = S["sealed"]["vintage_rows"]
print("NAV by vintage band: 2010-15 %.1f, 2016-20 %.1f, 2021-22 %.1f, 2023-26 %.1f" % tuple(
    sum(r["nav_total"] for r in rows if lo <= r["vintage"] <= hi) for lo, hi in ((2010, 2015), (2016, 2020), (2021, 2022), (2023, 2026))))
print("U by vintage band: 2019-20 %.2f, 2021-22 %.2f, 2023-24 %.2f, 2025-26 %.2f" % tuple(
    sum(r["unf_total"] for r in rows if lo <= r["vintage"] <= hi) for lo, hi in ((2019, 2020), (2021, 2022), (2023, 2024), (2025, 2026))))
print("max vintage NAV share:", max((r["nav_total"] / 52.0, r["vintage"]) for r in rows))
