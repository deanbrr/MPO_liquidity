"""groups/gap_04 validation checks (SYNTHETIC - NOT ADIC DATA).
1. PE vintage calibration (census unfunded 27.4, NAV 52, 20% pooled normal distribution rate).
2. T4' survival proxy at t0 equals gap_02's deterministic ladder for s*(0.76) (17 months, gap_02 s1.3).
3. Cfg.t1() reproduces t1_engine.simulate path for path (do-nothing, Mix A, Mix B; M1, M4, M6).
4. Timing of one integrated run.
Run: <venv>/python.exe -I g04_validate.py
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g04_engine as G  # noqa: E402

E = G.E
sys.path.insert(0, os.path.dirname(G._T1))
import gap02_study as S  # noqa: E402

out = {}
cal = G.pe_calibration()
out["pe_calibration"] = {k: cal[k] for k in ("L", "K26", "g", "pooled_dist_normal", "pooled_call", "U_tot", "N_tot")}
out["pe_vintages"] = {int(v): (round(u, 2), round(nv, 2)) for v, u, nv in zip(range(2012, 2027), cal["U0"], cal["N0"])}
cc = G.company_census()
out["co_census"] = dict(n_eff=cc["n_eff"], largest=cc["largest"], share_overlap=float(cc["overlap"].mean()),
                        share_shared_gp=float((cc["gp"] < 70).mean()))
print(json.dumps(out, indent=1))

# 2. T4' proxy at t0 versus gap_02 ladder (do-nothing, gc2 census, t1 overlay)
A = E.Policy("A")
lad = E.ladder(S.s_star(0.76), A)
n = 3
st = dict(tre=np.full(n, E.TRE0), enc=np.full(n, E.IM_N * E.N_SYN0 + E.OPP_IM0), dm=np.full(n, 22.0),
          em=np.full(n, 6.0), fi=np.full(n, 8.0), hf=np.full(n, 20.0), hf_q=np.zeros((n, 10)),
          priv={g: np.full(n, E.PRIV0[g]) for g in G.GKEYS}, unf=np.full(n, sum(E.UNF0.values())),
          sec_def=np.full(n, E.SEC_DEF0), sec_def0=E.SEC_DEF0, pc_rev=np.full(n, E.PC_REV0),
          basis=np.full(n, E.NAV0), n_syn=np.full(n, E.N_SYN0), pace=12.0, pace_cut=False, band=False,
          tail_stress=np.full(n, E.N_TAIL * 0.18), prem_m=E.TAIL_PREM * E.NAV0 / 12, nav=np.full(n, E.NAV0),
          fee_m=np.zeros(n), fac=np.zeros(n))
sh, shf = G.sh_tp_proxy(st, T=36)
out["t4prime_t0"] = dict(ladder_SH_TP=lad["SH_TP"], proxy_SH_TP=int(sh[0]), ladder_gstar=lad["gstar"])
print("T4' proxy check:", out["t4prime_t0"])
# census v1.0 variants of the t0 survival horizon (do-nothing book)
var = {}
top = 0.08 * E.NAV0 - (E.TRE0 - (E.IM_N * E.N_SYN0 + E.OPP_IM0))
for name, kw in {"gc2 split, no reserve top-up (gap_02)": {},
                 "census v1 split": dict(unf=np.full(n, 36.6), sec_def=np.full(n, 0.4), sec_def0=0.4,
                                         pc_rev=np.full(n, 1.0)),
                 "census v1 + 8% reserve top-up": dict(unf=np.full(n, 36.6), sec_def=np.full(n, 0.4), sec_def0=0.4,
                                                       pc_rev=np.full(n, 1.0), tre=np.full(n, E.TRE0 + top * 0.998),
                                                       dm=np.full(n, 22.0 - top)),
                 "census v1 + top-up + L1 tail ladder (3.2bn stress payoff)":
                     dict(unf=np.full(n, 36.6), sec_def=np.full(n, 0.4), sec_def0=0.4, pc_rev=np.full(n, 1.0),
                          tre=np.full(n, E.TRE0 + top * 0.998), dm=np.full(n, 22.0 - top),
                          tail_stress=np.full(n, 3.2))}.items():
    s2 = dict(st)
    s2.update(kw)
    var[name] = int(G.sh_tp_proxy(s2, T=36)[0][0])
out["t4prime_t0_variants"] = var
print("T4' t0 variants:", var)
# with a $10bn revolver (Mix B facility): SH_TPF
lad_b = E.ladder(S.s_star(0.76), E.Policy("B", rcf=10.0, band=True, pace_cut=True, hf_t0=5.0))
out["t4prime_t0_mixB_ladder"] = dict(SH_TP=lad_b["SH_TP"], SH_TPF=lad_b["SH_TPF"], min_head_tpf_24=lad_b["min_head_tpf_24"])
print("Mix B ladder:", out["t4prime_t0_mixB_ladder"])

# 3. exact reproduction of t1_engine in compatibility mode
pols = {"do_nothing": E.Policy("A"),
        "mixA": E.Policy("mixA", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
        "mixB": E.Policy("mixB", rcf=10.0, pace=12.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0)}
rep = {}
for pk, pol in pols.items():
    for mk in ("M1", "M4", "M6"):
        a = E.simulate(E.MODELS[mk], pol, n=4000)
        b = G.simulate(E.MODELS[mk], pol, G.Cfg.t1(), n=4000)
        keys = ("p_red", "mean_wtilde", "mean_commit_forgone", "mean_withheld", "w_inv2", "mean_fees")
        rep[f"{pk}|{mk}"] = {k: (a[k], b[k]) for k in keys}
        rep[f"{pk}|{mk}"]["identical"] = all(abs(a[k] - b[k]) < 1e-9 for k in keys)
out["t1_reproduction"] = rep
print("t1 reproduction identical:", all(v["identical"] for v in rep.values()))
for k, v in rep.items():
    if not v["identical"]:
        print("  MISMATCH", k, v)

# 4. timing of one integrated run
t0 = time.time()
r = G.simulate(E.MODELS["M1"], pols["mixB"], G.Cfg(track=True), n=10000)
out["timing_integrated_10k_s"] = time.time() - t0
out["integrated_M1_mixB"] = {k: r[k] for k in ("p_red", "mean_wtilde", "mean_commit_forgone", "mean_withheld",
                                               "stage_occupancy_avg", "p_black_12m")}
print("integrated run:", out["timing_integrated_10k_s"], out["integrated_M1_mixB"])
with open(os.path.join(HERE, "g04_validate_results.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, default=float)
