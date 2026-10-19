"""GC2 variant (SYNTHETIC / illustrative only): re-split the Form PF >90-day hedge-fund bucket to the SEC Q3-2025
cumulative curve (35.0% within 90d, 58.2% within 365d) instead of G7's 2/3 : 1/3 assumption, and re-run the
G7-module ladder under S1 and the C1 T1.4-aligned stress. Uses gc2_reconcile.run_v2 unchanged."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gc2_reconcile as r  # noqa: E402  (imports lib/g7mod.py as r.g)

g = r.g
base = {}
for scn in ("S1", "T14", "T14_draw5"):
    for basis in ("opening", "current"):
        base[f"{scn}|{basis}"] = r.run_v2(scn, basis)

# SEC Q3-2025: share of the >90d bucket redeemable within 365 days = (58.2-35.0)/(100-35.0)
frac_91_365 = (58.2 - 35.0) / (100.0 - 35.0)
gt90 = g.HF_TOTAL * (g.BAL0["hf_91_365d"] + g.BAL0["hf_gt365d"]) / g.HF_TOTAL
orig = {k: g.BAL0[k] for k in ("hf_91_365d", "hf_gt365d")}
g.BAL0["hf_91_365d"] = gt90 * frac_91_365
g.BAL0["hf_gt365d"] = gt90 * (1 - frac_91_365)
variant = {}
for scn in ("S1", "T14", "T14_draw5"):
    for basis in ("opening", "current"):
        variant[f"{scn}|{basis}"] = r.run_v2(scn, basis)
cfp = {}
for scn in ("S1", "T14", "T14_draw5", "T14_call125"):
    for basis in ("opening", "current"):
        cfp[f"{scn}|{basis}|cfp"] = {m: r.run_v2(scn, basis, cfp_actions=True, nav_prearranged=True)[m]
                                     for m in ("SH_TP_floor4", "SH_TPF_floor4_rcf_navf", "committed_facility_needed_for_24m", "cover24_tp")}
        if scn == "T14_call125":
            cfp[f"{scn}|{basis}"] = {m: r.run_v2(scn, basis)[m]
                                     for m in ("SH_TP_floor4", "SH_TPF_floor4_rcf_navf", "committed_facility_needed_for_24m", "cover24_tp")}

keys = ("SH_TP_floor0", "SH_TP_floor4", "cbc_tp_24m", "cover24_tp", "committed_facility_needed_for_24m")
out = {"note": "SYNTHETIC / ILLUSTRATIVE ONLY", "frac_of_gt90_within_365d_SEC": frac_91_365,
       "orig_split_bn": orig, "variant_split_bn": {k: g.BAL0[k] for k in ("hf_91_365d", "hf_gt365d")},
       "compare": {k: {"G7_split": {m: base[k][m] for m in keys}, "SEC_split": {m: variant[k][m] for m in keys}} for k in base},
       "SEC_split_cfp_and_call125": cfp}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "gc2_hf_split_variant_results.json"), "w"), indent=1)
