"""gap_03 worked example: why SIMM-netted vega cannot govern the hedge/short-vol offset.

ILLUSTRATIVE and SYNTHETIC. Two delta-hedged books on one equity index (SIMM equity
bucket 11, "Indexes, Funds, ETFs"):
  tail sleeve : long 6-month puts,       vega +V per vol point
  opportunistic: short 1-month straddles, vega -V per vol point
SIMM parameters are ISDA SIMM v2.8+2512 (effective 11 Jul 2026), sections B, G, J:
  equity index delta RW 15; HVR_equity 0.56; VRW_equity 0.29; vega concentration
  threshold (indexes) USD 3,800mm; SF(t) = 0.5*min(1, 14/t days); 12m = 365 days.
Post-mode convention: sensitivities multiplied by -1 when computing IM to post
(vendor documentation, ActiveViam SIMM 3.0 "Post and Collect modes").
Term-structure betas come from gap03_greek_layer_results.json (Cboe data).

Usage: python -I simm_offset_example.py <results.json> <out.json>
"""
import json
import math
import sys
from pathlib import Path

from scipy.stats import norm

res = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
A = res["A_term_structure_betas"]

V = 10.0e6  # USD per vol point (illustrative)
RW, HVR, VRW, VT = 15.0, 0.56, 0.29, 3800e6
alpha = norm.ppf(0.99)
sigma = RW * math.sqrt(365.0 / 14.0) / alpha  # SIMM para 10(b)
lam0 = norm.ppf(0.995) ** 2 - 1.0             # SIMM para 11(d)


def sf(days: float) -> float:
    return 0.5 * min(1.0, 14.0 / days)


T6M, T1M = 365.0 / 2, 365.0 / 12
book = {"tail_6m_long": (T6M, +V), "opp_1m_short": (T1M, -V)}


def vega_margin(vegas):
    vr_i = [HVR * sigma * v for v in vegas]
    net = sum(vr_i)
    vcr = max(1.0, math.sqrt(abs(net) / VT))
    return abs(VRW * net * vcr)  # single risk factor, single bucket


def curvature_margin(items, post=True):
    s = -1.0 if post else 1.0
    cvr = sum(s * sf(t) * sigma * v for t, v in items)  # netted to one risk factor
    gross = abs(cvr)
    theta = min(cvr / gross, 0.0) if gross > 0 else 0.0
    lam = lam0 * (1 + theta) - theta
    kb = abs(cvr)
    return max(cvr + lam * kb, 0.0), cvr


out = {"assumptions": {"vega_per_volpt_usd": V, "simm_version": "2.8+2512",
                       "equity_index_RW": RW, "HVR": HVR, "VRW": VRW,
                       "sigma_simm_equity_index": round(sigma, 3), "lambda_theta0": round(lam0, 4),
                       "SF_6m": round(sf(T6M), 5), "SF_1m": round(sf(T1M), 5),
                       "note": "delta-hedged; equity risk class only; IM to POST; illustrative"}}
sep = {}
for k, (t, v) in book.items():
    vm = vega_margin([v])
    cm, cvr = curvature_margin([(t, v)])
    sep[k] = {"vega_margin": round(vm / 1e6, 1), "curvature_margin": round(cm / 1e6, 1),
              "cvr_post": round(cvr / 1e6, 2), "total": round((vm + cm) / 1e6, 1)}
vm_c = vega_margin([v for _, v in book.values()])
cm_c, cvr_c = curvature_margin(list(book.values()))
same = {"vega_margin": round(vm_c / 1e6, 1), "curvature_margin": round(cm_c / 1e6, 1),
        "cvr_post": round(cvr_c / 1e6, 2), "total": round((vm_c + cm_c) / 1e6, 1)}
sum_sep = sum(x["total"] for x in sep.values())
out["IM_post_usd_m"] = {"separate_CSAs": sep, "separate_total": round(sum_sep, 1),
                        "same_CSA": same, "saving_from_colocation": round(sum_sep - same["total"], 1),
                        "saving_pct": round(100 * (sum_sep - same["total"]) / sum_sep, 1)}

# VIX-equivalent vega and a COVID-type spike (14 Feb -> 16 Mar 2020)
b6_daily = A["pairwise"]["VIX6M"]["vix_up_ge3"]["coef"][1]
ep = A["episodes"]["2020_COVID"]
b6_ep = ep["ratio_dVIX6M_dVIX"]
dvix = ep["VIX_peak"] - ep["VIX_low"]
dv6 = ep["VIX6M_peak"] - ep["VIX6M_low"]
out["vix_equivalent_vega_usd_m_per_vixpt"] = {
    "tail": [round(V * b6_daily / 1e6, 2), round(V * b6_ep / 1e6, 2)],
    "opp": -V / 1e6,
    "net": [round((V * b6_daily - V) / 1e6, 2), round((V * b6_ep - V) / 1e6, 2)],
    "beta_6m_used": [b6_daily, b6_ep]}
gain_tail = V * dv6
loss_opp = -V * dvix
out["covid_spike_vega_only_usd_m"] = {
    "dVIX": round(dvix, 2), "dVIX6M": round(dv6, 2),
    "tail_gain": round(gain_tail / 1e6, 0), "opp_loss": round(loss_opp / 1e6, 0),
    "net": round((gain_tail + loss_opp) / 1e6, 0),
    "offset_ratio_opp_loss_over_tail_gain": round(-loss_opp / gain_tail, 2),
    "note": "first-order vega only; VIX indices proxy ATM vol at matching tenor; gamma/vanna/volga ignored"}

# Power-law fit beta(T) = (T/30)^(-g) on all-days betas
import numpy as np
tenor_days = {"VIX9D": 9, "VIX3M": 91, "VIX6M": 182, "VIX1Y": 365}
xs, ys = [], []
for k, d in tenor_days.items():
    b = A["pairwise"][k]["all_days"]["coef"][1]
    xs.append(math.log(d / 30.0)); ys.append(math.log(b))
g = -np.polyfit(xs, ys, 1)[0]
out["beta_power_law"] = {"fit": "ln beta = c - g ln(T/30d), all-days betas",
                         "g": round(float(g), 3),
                         "intercept": round(float(np.polyfit(xs, ys, 1)[1]), 3),
                         "betas_all_days": {k: A["pairwise"][k]["all_days"]["coef"][1] for k in tenor_days}}
Path(sys.argv[2]).write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
