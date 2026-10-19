"""Quick diagnostics of the integrated engine (SYNTHETIC - NOT ADIC DATA)."""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g04_engine as G  # noqa: E402

E = G.E
POL = {"off": E.Policy("off"),
       "mixA": E.Policy("mixA", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
       "mixB": E.Policy("mixB", rcf=10.0, pace=12.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0)}
mk = sys.argv[1] if len(sys.argv) > 1 else "M1"
for pk, pol in POL.items():
    cfg = G.Cfg(track=True, players=(frozenset() if pk == "off" else frozenset(G.PLAYERS)), trigger="current")
    t0 = time.time()
    r = G.simulate(E.MODELS[mk], pol, cfg, n=10000)
    rec = r["_rec"]
    print(f"\n=== {mk} {pk}  ({time.time()-t0:.1f}s)  P(red) {r['p_red']*100:.2f}%  E[W~] {r['mean_wtilde']:.1f}  "
          f"CE {G.ce_wealth(r['_w']):.1f}  forgone {r['mean_commit_forgone']:.1f}  withheld {r['mean_withheld']:.2f}")
    print("  year-1 mean group cash ($bn):", {g: round(float(rec['cash'][g][:, 0].mean()), 2) for g in G.ACC})
    print("  year-1 P(group cash<0):", {g: round(float((rec['cash'][g][:, 0] < 0).mean()), 2) for g in G.ACC})
    print("  NAV end-y1 / y5:", {g: (round(float(rec['nav'][g][:, 0].mean()), 1), round(float(rec['nav'][g][:, 4].mean()), 1))
                                 for g in G.ACC})
    sc = rec["stage_cfp"]
    print("  CFP stage at t0:", np.bincount(sc[:, 0], minlength=4) / sc.shape[0], " t1 stage at t0:",
          np.bincount(rec["stage_t1"][:, 0], minlength=4) / sc.shape[0])
    print("  CFP occupancy all quarters:", np.bincount(sc.ravel(), minlength=4) / sc.size)
    print("  SH_TP t0 quantiles:", np.quantile(rec["sh"][:, 0], [0.05, 0.5, 0.95]), " SH_TPF t0:",
          np.quantile(rec["shf"][:, 0], [0.05, 0.5, 0.95]), " LCR t0:", np.quantile(rec["lcr"][:, 0], [0.05, 0.5]))
    print("  Tier1 green share (quarters):", rec["tier1"].mean(), " T2/T3/T4:", rec["t2"].mean(), rec["t3"].mean(),
          rec["t4"].mean())
    d = rec["disc"]
    print("  discount quantiles (all q):", np.quantile(d, [0.05, 0.5, 0.95, 0.99]), " P(d>20%) per q:",
          (d > 0.20).mean(), " in crisis:", (d[rec['crisis']] > 0.2).mean() if rec['crisis'].any() else None,
          " outside crisis:", (d[~rec['crisis']] > 0.2).mean())
    hot = rec["dhat"] > 0.20
    print("  P(dhat>20% & CFP<=Amber & Tier1) per q:", (hot & (sc <= 1) & rec["tier1"]).mean(),
          " ever 5y:", (hot & (sc <= 1) & rec["tier1"]).any(1).mean())
    cr = rec["crisis"]
    print("  | crisis: P(CFP<=Amber)", (sc[cr] <= 1).mean(), " P(Tier1)", rec["tier1"][cr].mean(),
          " P(trigger)", (hot & (sc <= 1) & rec["tier1"])[cr].mean(), " P(debt>0)", (rec["debt"][cr] > 0).mean())
    sn = rec["stage_net"]
    trig_net = hot & (sn <= 1) & rec["tier1_net"]
    print("  NET convention: CFP occupancy", np.bincount(sn.ravel(), minlength=4) / sn.size,
          " P(trigger)/q", trig_net.mean(), " ever", trig_net.any(1).mean(), " | crisis", trig_net[cr].mean())
    dep = rec["deploy"] > 1e-9
    print("  deployment quarters with revolver drawn:", (dep & (rec["debt"] > 1e-6)).sum() / max(dep.sum(), 1))
    mon = rec["mon"] > 1e-6
    exq = rec["expiry"] > 1e-6
    print("  monetization quarters:", mon.mean(), " of which CFP<=Amber:", (mon & (sc <= 1)).sum() / max(mon.sum(), 1),
          " NET<=Amber:", (mon & (sn <= 1)).sum() / max(mon.sum(), 1),
          " mean mon cash:", float(rec['mon'][mon].mean()) if mon.any() else 0,
          " | expiry-pay quarters:", exq.mean(), " mean:", float(rec['expiry'][exq].mean()) if exq.any() else 0)
    print("  tail cash total 5y mean:", (rec["mon"] + rec["expiry"]).sum(1).mean(), " premium 5y:", rec["prem"].sum(1).mean())
    print("  red by year:", [float(rec['red_q'][:, 4 * y:4 * y + 4].any(1).mean()) for y in range(5)])
    print("  mean cash by year:", {g: [round(float(rec['cash'][g][:, y].mean()), 2) for y in range(5)] for g in G.ACC})
    print("  deployment: P(any)", (rec["deploy"].sum(1) > 0).mean(), " mean total", rec["deploy"].sum(1).mean())
    print("  co deploy mean/q:", rec["co_deploy"].mean(), " accepted flow mean/q:", np.nanmean(rec["coflow_acc"]),
          " recap gross y-avg:", rec["recap_gross"].sum(1).mean() / 5, " recap PC:", rec["recap_pc"].sum(1).mean() / 5)
    print("  crisis share of quarters:", rec["crisis"].mean())
