"""ra_gap_01 ladder validation (SYNTHETIC - NOT ADIC DATA).
1. book='v1', census gap02, RA off: ra_ladder.gl_ladder == groups gap_01 g01_core.gl_ladder (== t1_engine.ladder)
   on six readings x eight policies (head_TPF, SH_TP, G*, NCO).
2. RA leg, mode 'g15': reproduces G15's cash row (normal +0.40, drought -0.16, T4' -1.32 / -2.46; pacing stop
   24m -1.65; calls x1.0 -0.84 / -1.70) - gate V-RA-CF.
3. RA leg, canonical at theta 0.76: true T4' loss after 12 months (~7.35bn) and RAME reported capture (~32%).
Run: <venv>/python.exe -I -B ra_validate_ladder.py  (writes ra_validate_ladder_results.json)
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra_book as B  # noqa: E402
import ra_ladder as RL  # noqa: E402

G01 = os.path.normpath(os.path.join(HERE, "..", "gap_01_calcs"))
sys.path.insert(0, G01)
import g01_core as G1  # noqa: E402

E = RL.E
out = {}
# ------------------------------------------------------------------ 1. reproduction of g01 / t1 ladder
readings = {"s*(0.76)": RL.s_star(0.76), "s*(0.0)": RL.s_star(0.0), "s*(1.0)": RL.s_star(1.0),
            "T4 literal": RL.t4_literal(), "T4 8% floor": RL.t4_literal(floor=0.08),
            "critic": RL.t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0))}
pols = {"A": E.Policy("A"), "rcf15": E.Policy("r", rcf=15.0), "cut": E.Policy("c", pace_cut=True),
        "band": E.Policy("b", band=True), "mixA": E.Policy("mA", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
        "mixB": E.Policy("mB", rcf=10.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0),
        "navf": E.Policy("n", navf=2.0), "amber": E.Policy("am", amber_t0=3.0)}
maxdiff = 0.0
mism = []
for rn, s in readings.items():
    for pn, pol in pols.items():
        a = G1.gl_ladder(s, pol=pol)
        lv = RL.lev_from_policy(pol, census="gap02", book="v1")
        b = RL.gl_ladder(s, lv)
        t = E.ladder(s, pol)
        d = float(np.max(np.abs(a["head_tpf"] - b["head_tpf"])))
        maxdiff = max(maxdiff, d, abs(t["gstar"] - b["gstar"]))
        if d > 1e-9 or a["SH_TP"] != b["SH_TP"] or t["SH_TP"] != b["SH_TP"]:
            mism.append((rn, pn, d, a["SH_TP"], b["SH_TP"], t["SH_TP"]))
out["reproduction_g01_t1"] = dict(max_abs_diff=maxdiff, mismatches=mism, cases=len(readings) * len(pols))
print("1. reproduction max diff", maxdiff, "mismatches", mism)

# ------------------------------------------------------------------ 2. G15 cash row (V-RA-CF)
g15 = {}
for st in ("normal", "drought", "T4prime"):
    r = RL.ra_leg(0.76, T=24, mode="g15", state=st)
    g15[st] = {"12m": RL.ra_summary(r, 12), "24m": RL.ra_summary(r, 24)}
r = RL.ra_leg(0.76, T=24, mode="g15", state="T4prime", commit_m=np.zeros(24))
g15["T4prime_no_new"] = {"24m": RL.ra_summary(r, 24)}
r = RL.ra_leg(0.76, T=24, mode="g15", state="T4prime", opts=dict(call_axis=1.0))
g15["T4prime_calls_x1"] = {"12m": RL.ra_summary(r, 12), "24m": RL.ra_summary(r, 24)}
tgt = {"normal 12m": (g15["normal"]["12m"]["net"], 0.40), "drought 12m": (g15["drought"]["12m"]["net"], -0.16),
       "T4' 12m": (g15["T4prime"]["12m"]["net"], -1.32), "T4' 24m": (g15["T4prime"]["24m"]["net"], -2.46),
       "T4' no new 24m": (g15["T4prime_no_new"]["24m"]["net"], -1.65)}
out["g15_cash_row"] = g15
out["V-RA-CF"] = {k: dict(engine=round(v[0], 3), g15=v[1], pass_=abs(round(v[0], 2) - v[1]) < 0.0051)
                  for k, v in tgt.items()}
print("2. V-RA-CF:", out["V-RA-CF"])
print("   calls x1:", round(g15["T4prime_calls_x1"]["12m"]["net"], 3), round(g15["T4prime_calls_x1"]["24m"]["net"], 3))
print("   T4' cures 24m (direct):", round(g15["T4prime"]["24m"]["cures"], 3))

# ------------------------------------------------------------------ 3. canonical RA leg at theta 0.76
canon = {}
for name, opts in {"g15 marks, no avail, no fund module": dict(marks="g15", availability=False, fund_module="off"),
                   "RAME marks, no avail, no fund module": dict(availability=False, fund_module="off"),
                   "RAME + fund module (waterfall), no avail": dict(availability=False),
                   "RAME + fund module (upper bound), no avail": dict(availability=False, fund_module="upper"),
                   "RAME + fund module + availability (canonical)": dict(),
                   "canonical + extension 0.35": dict(ext=0.35),
                   "canonical, calls x1.0": dict(call_axis=1.0)}.items():
    r = RL.ra_leg(0.76, T=24, mode="canonical", state="T4prime", opts=opts)
    nav_rep0 = 18.0
    true0 = float(sum(r["per"][k]["nav_true"][0] for k in r["per"]))
    canon[name] = {"12m": RL.ra_summary(r, 12), "24m": RL.ra_summary(r, 24),
                   "reported_change_12m": float(r["nav_rep"][12] - r["nav_rep"][0]),
                   "true_change_12m": float(r["nav_true"][11] - r["nav_true"][0]),
                   "true0": true0}
    print(f"3. {name:48s} 12m net {canon[name]['12m']['net']:+.3f} 24m net {canon[name]['24m']['net']:+.3f} "
          f"cures24 {canon[name]['24m']['cures']:.3f} fundSF24 {canon[name]['24m']['shortfall_fund']:.3f} "
          f"prot24 {canon[name]['24m']['prot_calls']:.3f} stop24 {canon[name]['24m']['dist_stop']:.3f}")
out["canonical_T4prime"] = canon
# RAME capture: reported vs true equity change by month 12 using the per-sleeve paths (gross of flows)
r = RL.ra_leg(0.76, T=24, mode="canonical", state="T4prime", opts=dict(availability=False, fund_module="off"))
true_loss = sum(sl["nav"] / (1 - sl["ltv"]) * B.T4_TRUE[sl["sector"]] for sl in B.SLEEVES)
rep_loss = 0.0
for sl in B.SLEEVES:
    gav = sl["nav"] / (1 - sl["ltv"])
    v = B.T4_TRUE[sl["sector"]]
    lv = [1 + v * min(q, 4) / 4 for q in range(5)]
    rt = [lv[q] / lv[q - 1] - 1 for q in range(1, 5)]
    rl = [0.0] * sl["lag"] + rt
    prev, cum = 0.0, 1.0
    for q in range(4):
        prev = sl["lam"] * prev + (1 - sl["lam"]) * rl[q]
        cum *= 1 + prev
    rep_loss += gav * (cum - 1)
out["rame_capture_12m"] = dict(true_loss=true_loss, reported=rep_loss, share=rep_loss / true_loss)
print("   RAME capture 12m:", out["rame_capture_12m"])
with open(os.path.join(HERE, "ra_validate_ladder_results.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, default=float)
