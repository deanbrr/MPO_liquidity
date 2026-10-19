"""Sleeve-level 24-month breakdown (cures, protective calls, distribution stops, LTV, queue) from ra_engine_results.json.
SYNTHETIC - NOT ADIC DATA.  Usage: python -B ra_sleeve_table.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "ra_engine_results.json"), encoding="utf-8"))
D = "ext=g10|varpi=1.0|calls=canonical|fund=True|coinv=True|gccGW=T|roll=0.111|recal=True"
out = {}
for sc in ("base_mc", "t4p_struct", "normal"):
    r = R["runs"][sc + "|" + D]
    print("==", sc)
    out[sc] = {}
    for sl, v in r["sleeves"].items():
        m = v["mean_24m"]
        row = {k: m[k] for k in ("cures", "shortfall", "prot_calls", "dist_stop", "gap", "matured", "handback_eq",
                                 "fund_loss", "sale_direct")}
        row["ltv_P50_t0_t4_t8"] = v["ltv_econ_P50_t0_t4_t8"]
        row["ltv_t8_P95"] = v["ltv_econ_t8_P95"]
        row["net24_P5_P50_P95"] = v["net_24m_P5_P50_P95"]
        if "queue_others_end_P50" in v:
            row["queue_end_P50"] = v["queue_others_end_P50"]
            row["adic_redeem_paid_q4_q8_P50"] = v["adic_full_redemption_paid_by_q4_q8_P50"]
            row["adic_redeem_paid_q4_P5"] = v["adic_full_redemption_paid_by_q4_P5"]
        out[sc][sl] = row
        print("  %-11s cures %.3f short %.3f prot %.3f stop %.3f gap %.3f matured %.3f hb %.3f loss %.3f sale %.3f "
              "ltv %s p95 %.3f net24 %s %s" % (sl, m["cures"], m["shortfall"], m["prot_calls"], m["dist_stop"], m["gap"],
                                              m["matured"], m["handback_eq"], m["fund_loss"], m["sale_direct"],
                                              v["ltv_econ_P50_t0_t4_t8"], v["ltv_econ_t8_P95"], v["net_24m_P5_P50_P95"],
                                              ("queue %s paid %s P5 %s" % (v["queue_others_end_P50"],
                                                                         v["adic_full_redemption_paid_by_q4_q8_P50"],
                                                                         v["adic_full_redemption_paid_by_q4_P5"])
                                               if "queue_others_end_P50" in v else "")))
json.dump(out, open(os.path.join(HERE, "ra_sleeve_table.json"), "w", encoding="utf-8"), indent=1)
