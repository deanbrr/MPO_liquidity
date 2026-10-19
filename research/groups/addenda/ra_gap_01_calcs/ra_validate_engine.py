"""ra_gap_01 engine validation (SYNTHETIC - NOT ADIC DATA).
1. book v1, Cfg.t1(): ra_engine.simulate == t1_engine.simulate (M1, M4, M6; do-nothing, Mix A, Mix B).
2. book v1, integrated config: ra_engine.simulate == g04_engine.simulate (M1 / M6, Mix B, current triggers).
3. T4' survival proxy at t0 vs the deterministic ladder: v1 (gap_04 check) and v2 (RA leg), theta 0.76 / 0.85.
4. v2 smoke run: RA ledger sanity (cash row, cures, NAV, DVA) and timing.
Run: <venv>/python.exe -I -B ra_validate_engine.py
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra_engine as R  # noqa: E402
import ra_ladder as RL  # noqa: E402
import ra_book as B  # noqa: E402

G04 = os.path.normpath(os.path.join(HERE, "..", "gap_04_calcs"))
sys.path.insert(0, G04)
import g04_engine as G  # noqa: E402

E = R.E
out = {}
pols = {"dn": E.Policy("dn"), "mixA": E.Policy("mixA", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
        "mixB": E.Policy("mixB", rcf=10.0, pace=12.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0)}
keys = ("p_red", "mean_wtilde", "mean_commit_forgone", "mean_withheld", "w_inv2", "mean_fees")
rep = {}
for pk, pol in pols.items():
    for mk in ("M1", "M4", "M6"):
        a = E.simulate(E.MODELS[mk], pol, n=3000)
        b = R.simulate(E.MODELS[mk], pol, R.Cfg.t1(), n=3000)
        rep[f"{pk}|{mk}"] = all(abs(a[k] - b[k]) < 1e-9 for k in keys)
out["t1_reproduction_identical"] = all(rep.values())
print("1. t1 reproduction identical:", out["t1_reproduction_identical"], rep)

rep2 = {}
for mk in ("M1", "M6"):
    a = G.simulate(E.MODELS[mk], pols["mixB"], G.Cfg(trigger="current"), n=2000)
    b = R.simulate(E.MODELS[mk], pols["mixB"], R.Cfg(trigger="current", players=frozenset(R.PLAYERS9)), n=2000)
    rep2[mk] = {k: (a[k], b[k]) for k in keys}
    rep2[mk]["identical"] = all(abs(a[k] - b[k]) < 1e-9 for k in keys)
    a2 = G.simulate(E.MODELS[mk], pols["dn"], G.Cfg(trigger="none", players=frozenset()), n=2000)
    b2 = R.simulate(E.MODELS[mk], pols["dn"], R.Cfg(trigger="none", players=frozenset()), n=2000)
    rep2[mk + "_off"] = all(abs(a2[k] - b2[k]) < 1e-9 for k in keys)
out["g04_reproduction"] = rep2
print("2. g04 reproduction:", {k: (v["identical"] if isinstance(v, dict) else v) for k, v in rep2.items()})


# ------------------------------------------------------------------ 3. proxy vs ladder at t0
def t0_state(book, n=2):
    priv = B.book_priv(book)
    unf = B.book_unf(book)
    st = dict(tre=np.full(n, E.TRE0), enc=np.full(n, E.IM_N * E.N_SYN0 + E.OPP_IM0), dm=np.full(n, 22.0),
              em=np.full(n, 6.0), fi=np.full(n, 8.0), hf=np.full(n, 20.0), hf_q=np.zeros((n, 10)),
              priv={g: np.full(n, priv[g]) for g in R.GKEYS},
              unf=np.full(n, sum(unf[g] for g in R.GKEYS)), sec_def=np.full(n, B.SEC_DEF_V1),
              sec_def0=B.SEC_DEF_V1, pc_rev=np.full(n, B.PC_REV_V1), basis=np.full(n, E.NAV0),
              n_syn=np.full(n, E.N_SYN0), pace=12.0, pace_cut=False, band=False,
              tail_stress=np.full(n, E.N_TAIL * 0.18), prem_m=E.TAIL_PREM * E.NAV0 / 12, nav=np.full(n, E.NAV0),
              fee_m=np.zeros(n), fac=np.zeros(n), share=R.share_of(book))
    if B.BOOKS[book]["ra"]:
        nav = np.array([s["nav"] for s in B.SLEEVES])
        ltv = np.array([s["ltv"] for s in B.SLEEVES])
        g0 = np.array([s["g0"] for s in B.SLEEVES])
        D = nav * ltv / (1 - ltv)
        st.update(ra_va=np.tile(nav, (n, 1)), ra_gt=np.tile((nav + D) / (1 + g0), (n, 1)), ra_d=np.tile(D, (n, 1)),
                  ra_u=np.tile(np.array([s["unf"] for s in B.SLEEVES]), (n, 1)), ra_cut=False)
    return st


prox = {}
for book in ("v1", "v2u16", "v2u11"):
    for th in (0.76, 0.85):
        st = t0_state(book)
        sh, shf = R.sh_tp_proxy(st, T=36, theta=th)
        lad = RL.gl_ladder(RL.s_star(th), RL.lev_of(reserve=0.0, book=book, census="v1"), theta=th)
        prox[f"{book}|{th}"] = dict(proxy_SH_TP=int(sh[0]), ladder_SH_TP=lad["SH_TP"], ladder_gstar=lad["gstar"])
out["proxy_vs_ladder_t0"] = prox
print("3. proxy vs ladder:", prox)

# ------------------------------------------------------------------ 4. v2 smoke run
for book in ("v2u16",):
    t0 = time.time()
    r = R.simulate(E.MODELS["M1"], pols["mixB"], R.Cfg(book=book, trigger="current", track=True), n=4000)
    dt = time.time() - t0
    ra = r["ra"]
    out[f"smoke_{book}"] = dict(secs=dt, p_red=r["p_red"], mean_w=r["mean_wtilde"], ra={k: ra[k] for k in (
        "cures12", "cures24", "cash_y_mean", "p_cash_neg_y", "navT_y_mean", "navA_y_mean", "navS_y_mean",
        "jv_cash", "oe_redemptions", "cashout", "forced_sale_cash", "oil_delta_t0", "oil_delta_post_sale",
        "enr_cash_t0", "enr_value_given")}, dva_mean_y={k: v["mean_y"] for k, v in ra["dva"].items()})
    print(f"4. smoke {book}: {dt:.1f}s", json.dumps(out[f"smoke_{book}"], indent=1)[:3000])
    rec = r["_rec"]
    print("   RA fan cash mean by year:", [float(rec["cash"]["RA"][:, y].mean()) for y in range(5)],
          "PE:", [float(rec["cash"]["PE"][:, y].mean()) for y in range(5)])
with open(os.path.join(HERE, "ra_validate_engine_results.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, default=float)
