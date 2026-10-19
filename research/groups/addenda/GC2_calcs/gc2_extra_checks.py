"""GC2 extra checks (SYNTHETIC / illustrative only; never ADIC data)."""
import json
from math import erf, sqrt

def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))

out = {}

# (a) Two-quarter CRIS gate probability by strategy (G5 per-quarter CRIS hazards) and book share gated
q = {"credit": 0.20, "rv": 0.20, "event": 0.10, "eqls": 0.04, "multi": 0.03, "macro": 0.01, "trend": 0.01}
two_q = {k: 1 - (1 - v) ** 2 for k, v in q.items()}
mix_d20 = {"multi": 0.30, "eqls": 0.15, "event": 0.10, "credit": 0.15, "rv": 0.10, "macro": 0.10, "trend": 0.10}
mix_g9 = {"multi": 0.30, "eqls": 0.20, "macro": 0.15, "credit": 0.15, "rv": 0.10, "event": 0.10}
mix_g5 = {"credit": 0.40, "eqls": 0.15, "multi": 0.15, "macro": 0.30}  # G5 sanity: 40% illiquid as credit/RV, 30% EqLS+multi, 30% macro/CTA
out["two_quarter_gate_prob"] = {k: round(v, 4) for k, v in two_q.items()}
for name, mix in (("D20", mix_d20), ("G9", mix_g9), ("G5_sanity", mix_g5)):
    out[f"share_gated_{name}"] = round(sum(w * two_q[k] for k, w in mix.items()), 4)

# (b) Overconfidence: coverage of a stated 80% interval when stated width = (1/kappa) x calibrated width, unbiased normal errors
def coverage(kappa, bias_sd=0.0):
    z = 1.2815516 / kappa
    if bias_sd == 0:
        return 2 * Phi(z) - 1
    # bias expressed in units of true sd: coverage = Phi(z - b) - Phi(-z - b)
    return Phi(z - bias_sd) - Phi(-z - bias_sd)
out["coverage_unbiased"] = {str(k): round(coverage(k), 3) for k in (1.0, 1.2, 1.75, 2.0, 2.7, 2.74)}
out["coverage_kappa1.75_bias0.5sd"] = round(coverage(1.75, 0.5), 3)
out["coverage_kappa1.75_bias0.75sd"] = round(coverage(1.75, 0.75), 3)
out["kappa_conf_for_36pct"] = round(1 / 2.74, 3)

# (c) Contingent liquidity charge (performance FTP) order of magnitude
U = 38.0
out["CLC_bn"] = {f"draw{d}_cbuf{c}": round(U * d * c, 3) for d in (0.25, 0.30, 0.35, 0.45) for c in (0.01, 0.015, 0.03)}

# (d) PE unfunded / PE NAV under different censuses vs TA steady state (0.37 normal, 0.24 drought)
for name, u in (("G9_census", 24.0), ("G7", 26.0), ("v1_residual", 38 - 3.9 - 1.5 - 1.2 - 4.0), ("G1_working", 25.0), ("G1_exec", 29.0), ("G1_mature", 12.0)):
    out[f"PE_U_over_NAV_{name}"] = round(u / 52.0, 3)
out["PE_residual_bn"] = round(38 - 3.9 - 1.5 - 1.2 - 4.0, 2)
out["overcommit_ratio"] = round((106 + 38) / 177, 3)
out["unfunded_over_liquid_G7"] = round(38 / (15 + 36 + 7.14), 3)
out["liquid_share_notice90"] = round((15 + 36 + 7.14) / 177, 4)
out["liquid_share_cash90"] = round((15 + 36 + 4.885) / 177, 4)

# (e) Private-credit expected loss check: regime shares 70/20/10, PD mult 1/1.5/3, LGD 0.40/0.40/0.55
w = 0.70 * 1.0 * 0.40 + 0.20 * 1.5 * 0.40 + 0.10 * 3.0 * 0.55
out["pc_EL_pd2.5"] = round(0.025 * w, 5)
out["pc_pd_for_1pct"] = round(0.01 / w, 5)
out["pc_EL_pd1.8"] = round(0.018 * w, 5)

# (f) Vintage-alpha term: SD of a_v = coef * SD(z), SD(z) ~ 0.2
out["vintage_alpha_sd_coef0.5"] = 0.5 * 0.2
out["vintage_alpha_sd_coef0.05"] = 0.05 * 0.2

# (g) T1.4 vs C3 year-1 net private flow (from gc2_reconcile_results.json, T14|opening)
res = json.load(open(__file__.replace("gc2_extra_checks.py", "gc2_reconcile_results.json")))
t = res["named"]["T14|opening"]
out["T14_year1_net_private_flow"] = round(t["dist_12m"] - t["calls_12m"], 2)
s = res["named"]["S1|opening"]
out["S1_year1_net_private_flow"] = round(s["dist_12m"] - s["calls_12m"], 2)

print(json.dumps(out, indent=1))
json.dump(out, open(__file__.replace(".py", "_results.json"), "w"), indent=1)
