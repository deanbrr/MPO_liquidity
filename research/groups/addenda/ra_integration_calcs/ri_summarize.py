"""
ri_summarize: collects the stage results into ra_integration_results.json (the results file of record for the Real
Assets integration re-run) and prints the Markdown tables used in RESULTS.md. SYNTHETIC - NOT ADIC DATA.
Run after ri_validate, ri_calib, ri_cashmap, ri_ladder, ri_mc and ri_oil:
  <venv>/python.exe -I -B ri_summarize.py
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ri_common as C  # noqa: E402

BK = ("v1", "v2u16", "v2u11")
NAMES = {"v1pub": "v1 published (census v1.0)", "v1": "v1 (7 groups, census v1.1)", "v2u16": "v2 U16",
         "v2u11": "v2 U11"}
GRP = (("pe", "PE funds"), ("sec", "Secondaries"), ("co", "Co-investment"), ("cs", "Capital Solutions"),
       ("pc", "Private Credit"), ("ra", "Real Assets"))


def f(x, nd=2, sign=True):
    if x is None:
        return "n/a"
    return (f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}")


def main():
    val = C.load("ri_validate_results.json")
    cal = C.load("ri_calib_results.json")
    cm = C.load("ri_cashmap_results.json")
    lad = C.load("ri_ladder_results.json")
    mc = C.load("ri_mc_results.json")
    oil = C.load("ri_oil_results.json")
    res = {"label": C.LABEL,
           "what": "Real Assets integration re-run: v1 (seven groups) vs v2 (eight groups, Real Assets $18bn carved "
                   "from PE funds), canonical conventions (T4' = s*(theta*), census v1.1 as chosen by the user; "
                   "U16 and U11 both reported). All figures SYNTHETIC - NOT ADIC DATA.",
           "books": {k: C.BOOKS[k]["label"] for k in C.BOOKS},
           "validation": dict(byte_identical={k: v["identical_to_original"] for k, v in
                                              val["copies"]["byte_identical"].items()},
                              ladder_max_abs_diff=val["ladder_reproduction"]["max_abs_diff"],
                              published_v1_T4prime=val["published_v1_T4prime"],
                              ra_gap_01_ladder={k: v["identical"] for k, v in val["ra_gap_01_ladder"].items()},
                              V_RA_CF={k: v["pass_"] for k, v in val["V-RA-CF"].items()},
                              mc_t1_identical=val["mc_t1_reproduction_identical"]["all"],
                              mc_ra_gap_01_identical={k: v["identical"] for k, v in
                                                      val["mc_ra_gap_01_reproduction"].items()},
                              cashmap=cm["reproduction"],
                              oil_off_leg_equals_G15_drought=oil["validate_off_equals_G15_drought"],
                              dcr_t0_reproduction=oil["dcr_sgps"]["v1pub|repro"],
                              mc_gap02_certified_mixes=dict(
                                  mixA_maxCP_M1_M5_pct=mc["summary"]["t1|v1pub|mixA"]["max_cp_M1_M5_pct"],
                                  mixA_M6_pct=mc["summary"]["t1|v1pub|mixA"]["p_red_pct"]["M6"],
                                  mixB_maxCP_M1_M5_pct=mc["summary"]["t1|v1pub|mixB"]["max_cp_M1_M5_pct"],
                                  mixB_M6_pct=mc["summary"]["t1|v1pub|mixB"]["p_red_pct"]["M6"],
                                  published="Mix A 0.98% / 5.8%; Mix B 0.79% / 6.5% (gap_02 s2.3)"))}
    # ---------------- theta*
    res["theta_star"] = {b: dict(theta=cal["theta_star"][b]["theta"], worst_model=cal["theta_star"][b]["worst_model"],
                                 gstar_p996=cal["theta_star"][b]["gstar_p996"],
                                 saa_range=[min(cal["saa"][b]["theta"]), max(cal["saa"][b]["theta"])],
                                 pooled=cal["saa"][b]["pooled_theta"],
                                 october_2026_state=cal.get("gap04_init", {}).get(b, {}).get("theta"))
                         for b in ("v1pub",) + BK}
    # ---------------- item 1: cash map
    cmap = {}
    for b in BK:
        d = cm["cashmap"][b]
        row = {}
        for gk, gname in GRP:
            if gk == "ra" and b == "v1":
                continue
            row[gname] = {
                "base_12m": d["normal|12m"]["net"][gk], "base_24m": d["normal|24m"]["net"][gk],
                "drought_12m": d["drought|12m"]["net"][gk], "drought_24m": d["drought|24m"]["net"][gk],
                "T4prime_12m": d["T4prime@theta*"]["12m"]["groups"][gk]["net"],
                "T4prime_24m": d["T4prime@theta*"]["24m"]["groups"][gk]["net"],
                "detail_12m": {"base": [d["normal|12m"]["dist"][gk], d["normal|12m"]["calls"][gk]],
                               "drought": [d["drought|12m"]["dist"][gk], d["drought|12m"]["calls"][gk]],
                               "T4prime": [d["T4prime@theta*"]["12m"]["groups"][gk]["dist"],
                                           d["T4prime@theta*"]["12m"]["groups"][gk]["calls"]]}}
        row["Private book"] = {"base_12m": d["normal|12m"]["private_net"], "base_24m": d["normal|24m"]["private_net"],
                               "drought_12m": d["drought|12m"]["private_net"],
                               "drought_24m": d["drought|24m"]["private_net"],
                               "T4prime_12m": d["T4prime@theta*"]["12m"]["private_net"],
                               "T4prime_24m": d["T4prime@theta*"]["24m"]["private_net"]}
        row["Overlay (unchanged v1 to v2)"] = {"base_12m": d["normal|12m"]["overlay_net"],
                                               "base_24m": d["normal|24m"]["overlay_net"],
                                               "drought_12m": d["drought|12m"]["overlay_net"],
                                               "drought_24m": d["drought|24m"]["overlay_net"],
                                               "T4prime_12m": d["T4prime@theta*"]["12m"]["overlay_net"],
                                               "T4prime_24m": d["T4prime@theta*"]["24m"]["overlay_net"]}
        row["Before payout"] = {"base_12m": d["normal|12m"]["before_payout"],
                                "base_24m": d["normal|24m"]["before_payout"],
                                "drought_12m": d["drought|12m"]["before_payout"],
                                "drought_24m": d["drought|24m"]["before_payout"],
                                "T4prime_12m": d["T4prime@theta*"]["12m"]["before_payout"],
                                "T4prime_24m": d["T4prime@theta*"]["24m"]["before_payout"]}
        row["Liquid-book funding (7.5% payout; T4': canonical draws)"] = {
            "base_12m": d["normal|12m"]["liquid_funding"]["7.5%"], "base_24m": d["normal|24m"]["liquid_funding"]["7.5%"],
            "drought_12m": d["drought|12m"]["liquid_funding"]["7.5%"],
            "drought_24m": d["drought|24m"]["liquid_funding"]["7.5%"],
            "T4prime_12m": d["T4prime@theta*"]["12m"]["liquid_funding_canonical_draws"],
            "T4prime_24m": d["T4prime@theta*"]["24m"]["liquid_funding_canonical_draws"]}
        cmap[b] = dict(theta=d["T4prime@theta*"]["theta"], rows=row,
                       pe_vintage_pace=d["drought|12m"].get("pe_pace"),
                       rate_leg_private_net={k: d[f"{k}|rate_leg"]["private_net"] for k in
                                             ("normal|12m", "drought|12m", "normal|24m", "drought|24m")},
                       T4prime_at_076_private_net={h: d["T4prime@0.76"][h]["private_net"] for h in ("12m", "24m")})
    res["item1_cash_map"] = cmap
    res["item1_deltas_v2_minus_v1"] = cm["deltas"]
    # ---------------- item 2: facility, survival, hard-row gap
    t = {}
    for key in ("v1pub@theta*",) + tuple(f"{b}@theta*" for b in BK) + tuple(f"{b}@0.76" for b in ("v1pub",) + BK) \
            + tuple(f"{b}@pooled" for b in BK):
        r = lad["readings"].get(key)
        if r is None:
            continue
        t[key] = dict(gstar=r["dn"]["gstar"], SH_TP=r["dn"]["SH_TP"], SH_TPF=r["dn"]["SH_TPF"],
                      facility_do_nothing=r["dn"]["fac_need_24"], facility_pacing_rule=r["rule"]["fac_need_24"],
                      SH_TP_pacing_rule=r["rule"]["SH_TP"], facility_band=r["band"]["fac_need_24"],
                      SH_TP_band=r["band"]["SH_TP"], SH_TP_rule_band=r["rule_band"]["SH_TP"],
                      mixA_head24=r["mixA"]["min_head_tpf_24"], mixB_head24=r["mixB"]["min_head_tpf_24"],
                      hard_row_gap_d0=r["d0"], d0_month=r["d0_month"])
    for key in ("v2u16@theta*|RA leg G15 (reproduction mode)", "v2u16@theta*|RA extension 0",
                "v2u16@theta*|RA calls x1.0", "v2u11@theta*|RA leg G15 (reproduction mode)",
                "v2u11@theta*|RA calls x1.0"):
        r = lad["readings"][key]
        t[key] = dict(gstar=r["dn"]["gstar"], SH_TP=r["dn"]["SH_TP"], facility_do_nothing=r["dn"]["fac_need_24"],
                      facility_pacing_rule=r["rule"]["fac_need_24"], hard_row_gap_d0=r["d0"])
    res["item2_T4prime"] = dict(readings=t, phase1_u_star={k: {s: v[s]["u_star"] for s in ("R0x", "R0", "R1")}
                                                           for k, v in lad["phase1"].items()},
                                L8_t0={k: dict(ratio=v["ratio"], headroom=v["headroom"]) for k, v in lad["L8_t0"].items()},
                                ra_carveout_effect_v2u16_minus_v1=lad["ra_carveout_effect"],
                                carveout_at_constant_PE_U_over_NAV_v2u11_minus_v1={
                                    "facility@0.76": t["v2u11@0.76"]["facility_do_nothing"] - t["v1@0.76"]["facility_do_nothing"],
                                    "facility@theta*": t["v2u11@theta*"]["facility_do_nothing"] - t["v1@theta*"]["facility_do_nothing"],
                                    "gstar@0.76": t["v2u11@0.76"]["gstar"] - t["v1@0.76"]["gstar"],
                                    "gstar@theta*": t["v2u11@theta*"]["gstar"] - t["v1@theta*"]["gstar"]})
    # ---------------- item 3: P(red)
    p = {}
    for eng in ("t1", "integrated", "integrated_raoff"):
        for b in ("v1pub",) + BK:
            for pk in ("dn", "mixA", "mixB"):
                s = mc["summary"].get(f"{eng}|{b}|{pk}")
                if s is None:
                    continue
                p[f"{eng}|{b}|{pk}"] = dict(M1=s["p_red_pct"]["M1"], M6=s["p_red_pct"]["M6"],
                                            all=s["p_red_pct"], cp_M6=s["cp_upper_pct"]["M6"],
                                            max_cp_M1_M5=s["max_cp_M1_M5_pct"])
    res["item3_P_red_pct"] = dict(table=p, n_paths=dict(t1=mc["n_t1"], integrated=mc["n_integrated"]),
                                  note="M6 = the stressed class; gap_02's M6-class capacity level is 5%; one-sided "
                                       "95% Clopper-Pearson bounds")
    # ---------------- item 4: oil
    res["item4_oil"] = dict(
        oc_state_ladder={k: {kk: v[kk] for kk in ("nco12", "nco24", "gstar", "min_head_tpf_24", "head_m24",
                                                   "fac_need_24", "SH_TP", "draws24")} for k, v in oil["oc_ladder"].items()},
        oc_deltas_from_RA_oil_loadings=oil["oc_deltas"], ra_leg_24m={k: {kk: v[kk] for kk in ("net12", "net24", "rbl24",
                                                                                             "income24", "realiz24")}
                                                                    for k, v in oil["ra_leg_24m"].items()},
        first_order_estimate=oil["first_order"], dcr_sgps={k: (v.get("dcr") if isinstance(v, dict) and "dcr" in v else v)
                                                           for k, v in oil["dcr_sgps"].items()},
        oc_x_db=oil["oc_x_db"], stochastic_deltas=oil["stochastic_deltas"])
    path = C.save("ra_integration_results.json", res)
    print("wrote", path)

    # ---------------- Markdown helpers (console)
    print("\n## theta*")
    for b in ("v1pub",) + BK:
        x = res["theta_star"][b]
        print(f"| {NAMES[b]} | {x['theta']:.3f} | {x['worst_model']} {x['gstar_p996']:.2f} | "
              f"{x['saa_range'][0]:.3f}-{x['saa_range'][1]:.3f} ({x['pooled']:.3f}) | {x['october_2026_state']} |")
    print("\n## cash map (net $bn): base 12/24 | drought 12/24 | T4' 12/24")
    for b in BK:
        print(f"### {NAMES[b]} (theta* {cmap[b]['theta']:.3f})")
        for g, r in cmap[b]["rows"].items():
            print(f"| {g} | {f(r['base_12m'])} / {f(r['base_24m'])} | {f(r['drought_12m'])} / {f(r['drought_24m'])} | "
                  f"{f(r['T4prime_12m'])} / {f(r['T4prime_24m'])} |")
    print("\n## T4' readings")
    for k, r in t.items():
        print(k, {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in r.items()})
    print("\n## P(red) %")
    for k, r in p.items():
        print(f"| {k} | M1 {r['M1']:.2f} | M6 {r['M6']:.2f} (CP {r['cp_M6']:.2f}) | max CP M1-M5 {r['max_cp_M1_M5']:.2f} |")


if __name__ == "__main__":
    main()
