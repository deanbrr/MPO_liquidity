"""Compact tables from ra_engine_results.json and ra_gates_results.json for the ra_gap_02 addendum.
SYNTHETIC - NOT ADIC DATA (engine outputs); gate targets are public data.
Usage: python -B ra_summarize.py  (writes ra_summary.json and prints tables)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "ra_engine_results.json"), encoding="utf-8"))
G = json.load(open(os.path.join(HERE, "ra_gates_results.json"), encoding="utf-8"))
DEF = "ext=g10|varpi=1.0|calls=canonical|fund=True|coinv=True|gccGW=T|roll=0.111|recal=True"


def key(scen, **chg):
    parts = dict(p.split("=") for p in DEF.split("|"))
    for k, v in chg.items():
        parts[k] = str(v)
    return scen + "|" + "|".join(f"{k}={v}" for k, v in parts.items())


out = {"label": "SYNTHETIC - NOT ADIC DATA", "cash_rows": {}, "axes": {}, "gates": {}}
print("CASH ROW ($bn, mean; 12m | 24m)")
for scen in ("normal", "drought", "base_mc", "rate_shock", "gulf_persist", "sg_glut", "t4p_struct", "t4p_ratesflat"):
    s = R["runs"][key(scen)]["summary"]
    row = {}
    for h in ("12m", "24m"):
        d = s[h]
        row[h] = {k: d[k] for k in ("income", "exits", "sale_proceeds_direct", "calls", "protective_calls",
                                    "distribution_stop", "dev_draws", "cures_direct_controlled", "shortfalls_direct",
                                    "cures_coinvest", "fund_level_need", "fund_level_unfunded_loss", "matured", "gap",
                                    "handback_equity", "net_mean", "net_P5_P50_P95", "adic_direct_cures_mean",
                                    "adic_direct_cures_CVaR95", "adic_cure_cash_incl_protective_calls_CVaR95",
                                    "fund_level_need_CVaR95")}
    row["ltv"] = s["ltv_lookthrough_econ"]
    row["ltv_debt_fixed_on_value_index_P50_P95_t4_t8"] = [s["ltv_debt_fixed_on_value_index_P50_t4_t8"],
                                                         s["ltv_debt_fixed_on_value_index_P95_t4_t8"]]
    row["ltv_controllable"] = s["ltv_controllable_econ"]
    row["value_index_P50_t4_t8"] = s["market_value_index_change_P50_t4_t8"]
    row["value_index_P5_t4_t8"] = s["market_value_index_change_P5_t4_t8"]
    row["value_index_by_sleeve"] = s["market_value_index_change_by_sleeve_P50_t4_t8"]
    row["appraisal_change_P50_t4_t8"] = s["value_change_appraisal_P50_t4_t8"]
    row["outcomes"] = s["maturity_outcomes_share_of_events"]
    row["infra_unrefinanced_by_G11"] = s["infra_unrefinanced_share_by_G11_state"]
    row["cov_kpi"] = s["covenant_trigger_12m_controllable"]
    row["ladder"] = s["ladder_mean_bn_by_quarter"]
    row["ladder_ctl"] = s["ladder_controllable_mean_bn_by_quarter"]
    row["sleeve_net_24m"] = s["sleeve_net_24m_mean"]
    row["states_q4"] = s["state_shares_q4"]
    out["cash_rows"][scen] = row
    a, b = row["12m"], row["24m"]
    print(f"{scen:14s} dist {a['income'] + a['exits'] + a['sale_proceeds_direct']:.2f} calls {a['calls'] + a['dev_draws']:.2f} "
          f"prot {a['protective_calls']:.2f} cures {a['adic_direct_cures_mean']:.2f} net {a['net_mean']:+.2f} {a['net_P5_P50_P95']} | "
          f"24m net {b['net_mean']:+.2f} {b['net_P5_P50_P95']} cures {b['adic_direct_cures_mean']:.2f} prot {b['protective_calls']:.2f} "
          f"fundneed {b['fund_level_need']:.2f} CVaR(direct) {b['adic_direct_cures_CVaR95']:.2f} CVaR(+prot) "
          f"{b['adic_cure_cash_incl_protective_calls_CVaR95']:.2f} CVaR(fund) {b['fund_level_need_CVaR95']:.2f}")
    print(f"{'':14s} LTV econ t4 {row['ltv']['t4_P5_P50_P95']} t8 {row['ltv']['t8_P5_P50_P95']} peak {row['ltv']['peak_8q_P50_P95']} "
          f"| debt-fixed/idx {row['ltv_debt_fixed_on_value_index_P50_P95_t4_t8']} | idx dV {row['value_index_P50_t4_t8']} P5 "
          f"{row['value_index_P5_t4_t8']} | ctl {row['ltv_controllable']}")
print("\nAXES (24m net, 24m direct-cure mean, CVaR95 direct, CVaR95 incl. protective calls, fund-level need)")
for scen in ("base_mc", "t4p_struct"):
    for lab, chg in (("default", {}), ("ext=zero", {"ext": "zero"}), ("varpi=0", {"varpi": 0.0}),
                     ("ext=zero,varpi=0", {"ext": "zero", "varpi": 0.0}), ("fund module off", {"fund": False}),
                     ("structural calls", {"calls": "structural"}), ("co-inv no participation", {"coinv": False}),
                     ("rollover hazard off", {"roll": 0.0}), ("as specified (no recal)", {"recal": False}),
                     ("GCC GW floor = C", {"gccGW": "C"})):
        k = key(scen, **chg)
        if k not in R["runs"]:
            continue
        s = R["runs"][k]["summary"]["24m"]
        s12 = R["runs"][k]["summary"]["12m"]
        out["axes"][f"{scen}|{lab}"] = {"net12": s12["net_mean"], "net24": s["net_mean"],
                                        "cures_direct_mean24": s["adic_direct_cures_mean"],
                                        "cvar_direct24": s["adic_direct_cures_CVaR95"],
                                        "cvar_incl_prot24": s["adic_cure_cash_incl_protective_calls_CVaR95"],
                                        "fund_need24": s["fund_level_need"], "prot24": s["protective_calls"],
                                        "ltv_t8": R["runs"][k]["summary"]["ltv_lookthrough_econ"]["t8_P5_P50_P95"]}
        print(f"{scen:11s} {lab:26s} net12 {s12['net_mean']:+.2f} net24 {s['net_mean']:+.2f} cures {s['adic_direct_cures_mean']:.3f} "
              f"CVaR {s['adic_direct_cures_CVaR95']:.3f} CVaR+prot {s['adic_cure_cash_incl_protective_calls_CVaR95']:.3f} "
              f"fundneed {s['fund_level_need']:.3f} prot {s['protective_calls']:.3f}")
out["gates"] = {
    "G_ODCE": {k: G["G_ODCE"][k] for k in ("appraisal_levered_dd", "appraisal_dd_window", "true_levered_dd", "true_dd_window",
                                           "trough_lag_q", "unlevered_true_2022Q1_2023Q4_greenstreet_mix",
                                           "unlevered_true_by_sector_2022Q1_2023Q4", "pass", "office_shock_fitted_qtr_log")},
    "G_ODCE_lambda_variants": G["G_ODCE_lambda_variants"],
    "G_JIANG_engine_as_specified": {k: G["G_JIANG_engine_as_specified"][k] for k in ("all", "office", "pass")},
    "G_JIANG_measurement_matched_uncalibrated": {k: G["G_JIANG_measurement_matched_uncalibrated"][k] for k in ("all", "office", "pass")},
    "G_JIANG_calibrated": {k: G["G_JIANG_calibrated"][k] for k in ("all", "office", "pass", "fitted", "held_out")},
    "G_CHEN": {k: {kk: G[k][kk] for kk in ("slope_refi_on_gap_pp", "se_cluster", "refi_share", "pass", "gap_range_pp",
                                          "beta_sale", "ell_sponsor", "p_sale0")}
               for k in ("G_CHEN_mechanism_default", "G_CHEN_mechanism_max", "G_CHEN_with_hazard_forward_range",
                         "G_CHEN_with_hazard_2003_2019_range")},
}
print("\nGATES")
print(json.dumps(out["gates"], indent=1)[:6000])
print("\nREGIME / SLOOS", json.dumps(R["sloos_calibration"]["coef"]), R["sloos_calibration"]["share_quarters_by_f"])
print("PZ quarterly", R["pz_quarterly"])
json.dump(out, open(os.path.join(HERE, "ra_summary.json"), "w", encoding="utf-8"), indent=1)
