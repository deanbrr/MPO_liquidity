"""Print compact tables from g04_main_results.json (SYNTHETIC - NOT ADIC DATA)."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "g04_main_results.json")))
R = M["runs"]
CV = M["contingent_value"]
MODELS = ["M1", "M2", "M3", "M4", "M5", "M6"]
what = sys.argv[1] if len(sys.argv) > 1 else "joint"

if what == "joint":
    for pol in ("off", "dn", "franchise", "mixA", "mixB"):
        print(f"\n== {pol}: trigger frequencies (policy run with trigger 'current' where applicable)")
        for mk in MODELS:
            key = f"{mk}|{pol}|{'none' if pol == 'off' else 'current'}|base"
            S = R[key]["summary"]
            jg, jn, d = S["joint_gross"], S["joint_net"], S["disc"]
            print(f" {mk} P(crisis q) {d['p_crisis_q']:.3f} ever {d['p_crisis_ever']:.2f} | P(dhat>20% q) {d['p_hot_q']:.3f} "
                  f"ever {d['p_hot_ever']:.2f} P(d>20|crisis) {d['p_hot_true_given_crisis']:.3f} P(d>20|calm) {d['p_hot_true_given_calm']:.3f}"
                  f" | t0 stage {np.round(jg['t0'], 2).tolist()} occ {np.round(jg['occupancy'], 2).tolist()}"
                  f" | trig q {jg['p_q']:.4f} ever {jg['p_ever']:.3f} |crisis {jg['p_q_given_crisis']:.3f} |hot {jg['p_q_given_hot']:.3f}"
                  f" <=Amber|hot {jg['p_le_amber_given_hot']:.3f} T1|hot {jg['p_tier1_given_hot']:.3f}"
                  f" | NET trig q {jn['p_q']:.4f} ever {jn['p_ever']:.3f}")
elif what == "mon":
    for pol in ("off", "dn", "franchise", "mixA", "mixB"):
        print(f"\n== {pol}: tail cash and monetization")
        for mk in MODELS:
            key = f"{mk}|{pol}|{'none' if pol == 'off' else 'current'}|base"
            S = R[key]["summary"]["mon"]
            print(f" {mk} mon q {S['p_q']:.3f} ever {S['p_ever']:.2f} share<=Amber {S['share_le_amber_gross']:.2f} "
                  f"(net {S['share_le_amber_net']:.2f}) share hot {S['share_hot']:.2f} share crisis {S['share_crisis']:.2f}"
                  f" P(mon&<=Amber&hot) {S['p_q_mon_le_amber_hot']:.4f} | mon5y {S['mon_5y']:.2f} expiry5y {S['expiry_5y']:.2f}"
                  f" tail5y {S['tail_cash_5y']:.2f} prem5y {S['premium_5y']:.2f} | tail cash per crisis path (crisis q) "
                  f"{S['tail_cash_crisis_quarters_per_crisis_path']}")
elif what == "deploy":
    for pol in ("dn", "franchise", "mixA", "mixB"):
        print(f"\n== {pol}: contingent deployment and value (paired vs trigger 'none')")
        for mk in MODELS:
            for tr in ("current", "current_net", "tier1only", "ring50", "ring100", "ring_t1", "ungated"):
                S = R[f"{mk}|{pol}|{tr}|base"]["summary"]["deploy"]
                c = CV[f"{mk}|{pol}|{tr}|base"]
                print(f" {mk} {tr:11s} P(any) {S['p_any']:.2f} mean {S['mean_total']:.2f} (if any {S['mean_total_if_any']:.2f}) "
                      f"crisis share {S['share_in_crisis']:.2f} Red share {S['share_stage_red']:.2f} disc@dep {S['mean_disc_at_deploy']:.3f}"
                      f" debt share {S['share_with_debt']:.2f} | dE[W] {c['d_mean_w']:+.3f}+-{c['d_w_se']:.3f} dCE {c['d_ce']:+.3f}"
                      f" dP(red) {100 * c['d_p_red']:+.2f}pp value/$ {c['value_per_dollar']}")
            for tr in ("current", "ring100"):
                k = f"{mk}|{pol}|{tr}|theta75"
                if k in CV:
                    c = CV[k]
                    print(f"    theta 0.75 {tr:8s}: dE[W] {c['d_mean_w']:+.3f} dCE {c['d_ce']:+.3f} value/$ {c['value_per_dollar']}")
elif what == "fans":
    pol = sys.argv[2] if len(sys.argv) > 2 else "mixB"
    tr = "none" if pol == "off" else "current"
    for mk in MODELS:
        S = R[f"{mk}|{pol}|{tr}|base"]["summary"]
        print(f"\n== {mk} {pol}  red by year {np.round(np.array(S['red_by_year']) * 100, 2).tolist()}")
        for g, F in S["fans"].items():
            print(f"  {g:4s} P(cash<0) y1-5 {np.round(F['p_cash_neg'], 2).tolist()} cum {F['p_cash_cum_neg']:.2f} | "
                  f"cash y1 {F['cash'][0]} y5 {F['cash'][4]} | cum5 {F['cash_cum5']} | NAV y5 {F['nav'][4]} | "
                  f"DVA cum5 {F['dva_cum5']} P(DVA<0) {F['p_dva_cum_neg']:.2f}")
elif what == "co":
    for pol in ("off", "mixA", "mixB"):
        tr = "none" if pol == "off" else "current"
        for mk in MODELS:
            S = R[f"{mk}|{pol}|{tr}|base"]["summary"]["co"]
            print(pol, mk, {k: (np.round(v, 2).tolist() if isinstance(v, list) else (round(v, 3) if v is not None else None))
                            for k, v in S.items()})
elif what == "runs":
    for pol in ("off", "dn", "franchise", "mixA", "mixB"):
        for mk in MODELS:
            key = f"{mk}|{pol}|{'none' if pol == 'off' else 'current'}|base"
            r = R[key]
            print(pol, mk, f"P(red) {100 * r['p_red']:.2f}% E[W] {r['mean_wtilde']:.1f} CE {r['ce']:.1f} forgone {r['mean_commit_forgone']:.1f}"
                  f" withheld {r['mean_withheld']:.2f} forgone_g {dict((k, round(v, 1)) for k, v in r['mean_forgone_g'].items())}")
