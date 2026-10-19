import sys, json
import numpy as np
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
r = json.load(open(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\results.json", encoding="utf-8"))
print("== replication books")
for b in r["replication_books"]:
    print(json.dumps(b)[:1500])
print("== lens_r1")
for l in r["lens_r1"]:
    print(l)
print("== root")
print(json.dumps(r["root"], indent=0)[:3000])
print("== cvar table (OOS)")
pol = r["oos"]["policies"]
for k in ["B0","B1","B2","B3","B4_1.0","B4_1.1","B4_1.2","B4_1.3","B4_1.45","B4_1.6","O1_playbook","O1_rule","O2_playbook","O2_rule","O3_playbook","O3_rule","OFF_PACE","OFF_HEDGE","OFF_BETA","OFF_REBALANCE","OFF_REDEEM","OFF_ADD","OFF_SELL","OFF_FUND","OFF_LEVER","OFF_BELIEFS","FORCE_SYNTH_BETA","FORCE_TERM","FORCE_HF-01","FORCE_LO-01","FORCE_LO-04","FORCE_LO-03","A20_class_caps","FR_delta_0.04"]:
    m = pol[k]
    print(f"{k:18s} P={m['p_goal']:.4f} Prep={m['p_goal_reported_nav']:.4f} mean={m['twr_mean']:.4f} med={m['twr_median']:.4f} cv10={m['cvar_twr']['10']:.4f} cv5={m['cvar_twr']['5']:.4f} cv1={m['cvar_twr']['1']:.4f} bpoe={m['bpoe']['goal']:.4f} bpoe7={m['bpoe']['floor7']:.4f} bpoe0={m['bpoe']['zero']:.4f} EW={m['E_terminal_Wtilde_over_W0']:.4f} dd50={m['maxdd_median']:.3f} dd95={m['maxdd_p95']:.3f} lev={m['lev_max_median']:.3f} bim={m['bimodality']:.3f} pile={m['pileup_mass']:.4f} red={m['p_red']:.4f} veq={m.get('value_at_equal_tail')}")
print("== attribution")
for a in r["attribution"]["switch_off"]:
    print(json.dumps(a))
print("== frontier")
for f in r["frontier"]:
    print(json.dumps(f))
print("== frontier delta")
for f in r["frontier_delta"]:
    print(json.dumps(f))
print("== a20")
for a in r["a20_limit_sensitivity"]:
    aa = dict(a); rt = aa.pop("root", None)
    print(json.dumps(aa))
    if rt:
        print("   root keys", list(rt.keys()))
        print("   beta", rt.get("beta"), "opp", rt.get("opp"), "hed", rt.get("hed"), "fin", rt.get("fin"), "tpl", rt.get("tpl"))
print("== b0 readings")
print(json.dumps(r["b0_readings"]))
print("== tree stage1")
for s in r["tree"]["stage1"]:
    print(s)
print("== hypotheses")
print(json.dumps(r["hypotheses"], indent=0)[:3000])
