"""SYNTHETIC - NOT ADIC DATA. Reduced instance, INDEPENDENT side: my formulation (my_lp.py) solved with HiGHS and
Clarabel; GBO by mean LP + exact perspective LP + bisection + tie-break; exact max-P(goal) MILP with explicit
indicators; big-M lower-bound validity (min W~ per leaf); my own status-quo LP and its readings."""
import json
import os
import pickle
import sys
import time

import numpy as np
import scipy.sparse as sp

OUT = os.path.dirname(os.path.abspath(__file__))
RED = os.path.join(OUT, "reduced")
sys.path.insert(0, OUT)
import vlib  # noqa: E402
from my_lp import MyLP, PJ  # noqa: E402

logf = open(os.path.join(RED, "red_mine.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


def viol(lp, v):
    ax = lp.A @ v
    fl, fu = vlib.finite(lp.rlo), vlib.finite(lp.rhi)
    vv = np.maximum(np.maximum(np.where(fl, lp.rlo - ax, -np.inf), np.where(fu, ax - lp.rhi, -np.inf)), 0.0)
    worst = int(np.argmax(vv))
    bnd = max(np.maximum(lp.lb - v, 0).max(), np.maximum(v - lp.ub, 0).max())
    return float(vv.max()), lp.tags[worst], float(bnd)


res = {}
try:
    dm = pickle.load(open(os.path.join(RED, "red_dump.pkl"), "rb"))
    D, b0 = dm["D"], dm["b0"]
    pj = PJ(os.path.join(RED, "params.json"))
    lp = MyLP(D, pj, b0, "OPT")
    L(f"my LP: {lp.A.shape[0]} rows x {lp.nv} cols (author {dm['nrow']} x {dm['nvar']}); data checks {json.dumps(lp.chk, default=float)}")
    bl = dm["blocks"]
    W0, Ws, p = lp.W0, lp.Wstar, lp.p_leaf
    WT = lp.blk["Wt"]
    Xof = lambda v: (Ws - v[WT]) / W0
    caps = dm["caps"]
    # ---------------- author's solutions in my rows
    sols = {c["name"]: c["x"] for c in caps if c["x"] is not None}
    sols["author exact MILP"] = dm["milp"]["x"]
    sols["author round MILP"] = dm["round"]["x"]
    sols["author CRRA+L2"] = dm["o3"]["x"]
    for nm, xa in sols.items():
        v = lp.from_author(xa, bl)
        mv, t, mb = viol(lp, v)
        L(f"author '{nm}' in my rows: worst row viol {mv:.2e} at {t}; bounds {mb:.2e}")
        res.setdefault("author_in_mine", {})[nm] = [mv, str(t), mb]
    # ---------------- 1. mean LP
    r = vlib.highs_lp(lp.c_mean(), lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="simplex", sense_max=True)
    rc = vlib.clarabel_lp(lp.c_mean(), lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, sense_max=True, tol=1e-10, max_iter=500)
    Ea = caps[0]["rec"]["obj"]
    res["mean"] = {"author": Ea, "mine_highs_simplex": r["obj"], "mine_clarabel": rc["obj"], "clarabel_status": rc["status"],
                   "clarabel_viol": viol(lp, rc["x"])[0]}
    L(f"1 mean LP: author {Ea:.12f}  mine/HiGHS dual simplex {r['obj']:.12f}  mine/Clarabel {rc['obj']:.12f} ({rc['status']}, viol {res['mean']['clarabel_viol']:.1e})")
    label = "PLAN" if r["obj"] > Ws else "STRETCH"
    L(f"   label {label} (W* {Ws:.6f})")
    # ---------------- 2. exact min bPOE: perspective LP (both solvers) and bisection on min CVaR
    c2, A2, rlb2, rub2, lb2, ub2, ny = vlib.perspective(lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, WT, p, Ws, W0)
    rp_h = vlib.highs_lp(c2, A2, rlb2, rub2, lb2, ub2, method="ipm")
    rp_c = vlib.clarabel_lp(c2, A2, rlb2, rub2, lb2, ub2, tol=1e-10, max_iter=500)
    xs = rp_h["x"][:ny] / rp_h["x"][ny]
    b_h, a_h = vlib.bpoe0(Xof(xs), p)
    xs_c = rp_c["x"][:ny] / rp_c["x"][ny]
    b_c, _ = vlib.bpoe0(Xof(xs_c), p)
    lo, hi = 0.5, 1.0
    nlp = 0
    while hi - lo > 1e-7:
        mid = 0.5 * (lo + hi)
        rr = vlib.highs_lp(lp.c_cvar(mid), lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="simplex")
        nlp += 1
        if rr["obj"] <= 0:
            hi = mid
        else:
            lo = mid
    phi_a = dm["o1"]["phi"]
    res["phi"] = {"author_fixed_point": phi_a, "author_hist": dm["o1"]["phi_history"], "mine_persp_highs_obj": rp_h["obj"],
                  "mine_persp_highs_bpoe_of_x": b_h, "mine_persp_clarabel_obj": rp_c["obj"], "mine_persp_clarabel_bpoe_of_x": b_c,
                  "mine_bisection": [lo, hi], "bisection_lps": nlp, "author_x_bpoe": vlib.bpoe0(Xof(lp.from_author(caps[1]["x"], bl)), p)[0]}
    L("2 Phi: " + json.dumps(res["phi"], default=float))
    # ---------------- 3. tie-break at the author's pt (and at my own Phi + 0.005)
    pt_a = dm["o1"]["tie"]["pt"]
    for nm, pt in (("author pt", pt_a), ("my Phi + 0.005", rp_h["obj"] + 0.005)):
        At = sp.vstack([lp.A, lp.tie_row(pt)]).tocsr()
        rl, rh = np.r_[lp.rlo, -np.inf], np.r_[lp.rhi, 0.0]
        th = vlib.highs_lp(lp.c_util(), At, rl, rh, lp.lb, lp.ub, method="simplex", sense_max=True)
        tc = vlib.clarabel_lp(lp.c_util(), At, rl, rh, lp.lb, lp.ub, sense_max=True, tol=1e-10, max_iter=500)
        ent = {"pt": pt, "mine_highs": th["obj"], "mine_clarabel": tc["obj"], "clarabel_status": tc["status"]}
        if nm == "author pt":
            ent["author"] = caps[3]["rec"]["obj"]
            xa = lp.from_author(caps[3]["x"], bl)
            b = lp.blk
            V0 = D["V"][0]
            diff = {}
            for sol_nm, xm in (("highs", th["x"]), ("clarabel", tc["x"])):
                d = {}
                for k in ("s", "r", "a"):
                    d[k] = float(np.max(np.abs((xm[b[k][0]] - xa[b[k][0]]) * V0)))
                for k in ("y", "beta", "trs", "hed", "opp", "pi", "B", "Lup"):
                    d[k] = float(np.max(np.abs(np.atleast_1d(xm[b[k][0]] if k not in ("Lup",) else xm[b[k]]) - np.atleast_1d(xa[b[k][0]] if k not in ("Lup",) else xa[b[k]]))))
                d["leaf_Wt"] = float(np.max(np.abs(xm[WT] - xa[WT])))
                d["stage1_all_decisions_max_bn"] = float(max(np.max(np.abs((xm[b[k][1:6]] - xa[b[k][1:6]]) * D["V"][1:6])) for k in ("s", "r", "a")))
                diff[sol_nm] = d
            ent["decision_diffs"] = diff
            ent["clarabel_viol"] = viol(lp, tc["x"])[0]
            ent["bpoe_mine_highs"] = vlib.bpoe0(Xof(th["x"]), p)[0]
            ent["P_goal_mine_highs"] = float(p[th["x"][WT] >= Ws * (1 - 1e-9)].sum())
            ent["P_goal_author"] = dm["o1_stats"]["p_goal"]
            np.save(os.path.join(RED, "my_o1.npy"), th["x"])
        res.setdefault("tie", {})[nm] = ent
        L(f"3 tie-break [{nm}]: " + json.dumps(ent, default=float))
    # ---------------- 4. CRRA + L2 (O3)
    r3 = vlib.highs_lp(lp.c_util(pj("objective.lambda_T")), lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="simplex", sense_max=True)
    res["crra_l2"] = {"author": dm["o3"]["rec"]["obj"] if "rec" in dm["o3"] else None, "mine": r3["obj"]}
    L(f"4 CRRA+L2: mine {r3['obj']:.12f}  author {dm['o3'].get('status')} (author obj in log: -0.4208237440)")
    # ---------------- 5. exact MILP with explicit indicators
    eps_g = pj("goal.eps_g")
    Lf = len(WT)
    nv = lp.nv

    def milp(eps, Mvec=None, gap=1e-9, tl=1200):
        Mb = (Ws + eps * W0) * np.ones(Lf) if Mvec is None else Mvec
        rhs = Ws + eps * W0 - Mb
        G = sp.csr_matrix((np.r_[np.ones(Lf), -Mb], (np.r_[np.arange(Lf), np.arange(Lf)], np.r_[WT, nv + np.arange(Lf)])), shape=(Lf, nv + Lf))
        Af = sp.vstack([sp.hstack([lp.A, sp.csr_matrix((lp.A.shape[0], Lf))]), G]).tocsr()
        c = np.r_[np.zeros(nv), p]
        integ = np.r_[np.zeros(nv, bool), np.ones(Lf, bool)]
        return vlib.highs_lp(c, Af, np.r_[lp.rlo, rhs], np.r_[lp.rhi, np.full(Lf, np.inf)], np.r_[lp.lb, np.zeros(Lf)],
                             np.r_[lp.ub, np.ones(Lf)], sense_max=True, integrality=integ, mip_gap=gap, time_limit=tl)

    t0 = time.time()
    mm = milp(eps_g)
    L(f"5 my MILP (eps {eps_g}, L=0): {mm['status']} obj {mm.get('obj')} bound {mm.get('dual_bound')} gap {mm.get('mip_gap')} nodes {mm.get('nodes')} in {time.time()-t0:.1f}s; author exact {dm['milp']['rec']['obj']}")
    xg = mm["x"]
    g = xg[nv:]
    Wt = xg[WT]
    meets_margin = Wt >= Ws + eps_g * W0 - 1e-6
    meets_goal = Wt >= Ws * (1 - 1e-9)
    gi = g > 0.5
    ind = {"obj": mm["obj"], "n_g1": int(gi.sum()), "n_meets_margin": int(meets_margin.sum()), "n_meets_goal": int(meets_goal.sum()),
           "g1_but_below_margin": int((gi & ~meets_margin).sum()), "g0_but_meets_margin": int((~gi & meets_margin).sum()),
           "g0_but_meets_goal_in_eps_band": int((~gi & meets_goal).sum()), "max_frac_g": float(np.max(np.minimum(g, 1 - g))),
           "P_goal_noeps": float(p[meets_goal].sum()), "min_Wt_given_g0": float(Wt[~gi].min()) if (~gi).any() else None}
    res["milp_mine"] = ind
    L("   indicator logic: " + json.dumps(ind, default=float))
    xa_m = lp.from_author(dm["milp"]["x"], bl)
    Wa = xa_m[WT]
    res["milp_author"] = {"obj": dm["milp"]["rec"]["obj"], "P_meets_margin": float(p[Wa >= Ws + eps_g * W0 - 1e-6].sum()),
                          "P_meets_goal": float(p[Wa >= Ws * (1 - 1e-9)].sum()),
                          "n_in_eps_band": int(((Wa >= Ws * (1 - 1e-9)) & (Wa < Ws + eps_g * W0 - 1e-6)).sum())}
    L("   author's exact MILP solution: " + json.dumps(res["milp_author"], default=float))
    # red margin on the MILP solutions: is P(red) > eps an H9 violation or a tolerance artefact?
    Mcols = lp.blk["M"]
    RScols = lp.blk["RS"]
    for nm, xx in (("author exact MILP", xa_m), ("my MILP", xg[:nv]), ("author O1", lp.from_author(caps[3]["x"], bl))):
        Rl = np.array([max(np.max(xx[Mcols[lp.anc[f]]]), np.max(xx[RScols[lp.anc[f]]] - pj("constraints.red_sale_threshold"))) for f in lp.leaves])
        res.setdefault("red_margin", {})[nm] = {"max_R": float(Rl.max()), "P(R>1e-6)": float(p[Rl > 1e-6].sum()), "P(R>1e-4)": float(p[Rl > 1e-4].sum()),
                                                "CVaR_0.006(R)": vlib.cvar_upper(Rl, p, 0.006)}
    L("   red-event statistic R_l = max over the path of (M, RS - thr): " + json.dumps(res["red_margin"], default=float))
    # same MILP without the eps margin
    mm0 = milp(0.0)
    res["milp_mine_eps0"] = {"obj": mm0.get("obj"), "status": mm0["status"]}
    L(f"   my MILP without the eps margin: {mm0['status']} obj {mm0.get('obj')}")
    # ---------------- 6. big-M validity: L_l = min W~_l over the feasible set
    Lmin = np.zeros(Lf)
    for li in range(Lf):
        c = np.zeros(nv)
        c[WT[li]] = 1.0
        rr = vlib.highs_lp(c, lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="simplex")
        Lmin[li] = rr["obj"]
    res["bigM_L"] = {"min_over_leaves": float(Lmin.min()), "argmin_leaf": int(np.argmin(Lmin)), "n_negative": int((Lmin < 0).sum()),
                     "quantiles": np.quantile(Lmin, [0, 0.1, 0.5, 0.9, 1]).tolist()}
    L("6 big-M lower bounds L_l = min W~_l: " + json.dumps(res["bigM_L"], default=float))
    Mt = Ws + eps_g * W0 - np.minimum(Lmin, 0.0)
    mmt = milp(eps_g, Mvec=Mt)
    res["milp_mine_tight_M"] = mmt.get("obj")
    L(f"   MILP with LP-tightened valid M (L_l = min(0, min W~_l)): obj {mmt.get('obj')}")
    # ---------------- 7. my status-quo LP and its readings vs the author's
    lp0 = MyLP(D, pj, {}, "B0")
    r0 = vlib.highs_lp(lp0.c_b0(), lp0.A, lp0.rlo, lp0.rhi, lp0.lb, lp0.ub, method="ipm")
    x0m = r0["x"]
    x0a = lp0.from_author(dm["x0"], dm["m0_blocks"])
    b = lp0.blk
    Wm, Wa0 = x0m[b["W"]], x0a[b["W"]]
    Xm, Xa = (Ws - x0m[b["Wt"]]) / W0, (Ws - x0a[b["Wt"]]) / W0
    cv = lambda X, a: vlib.cvar_upper(X, p, 1 - a)
    res["b0"] = {"obj_mine": r0["obj"], "obj_author": float(dm["m0_cost"] @ dm["x0"]), "author_x0_in_my_B0_rows": viol(lp0, x0a)[0],
                 "max_W_diff": float(np.max(np.abs(Wm - Wa0))), "max_Wt_diff": float(np.max(np.abs(x0m[b["Wt"]] - x0a[b["Wt"]]))),
                 "cvar_X_mine": [cv(Xm, a) for a in (0.9, 0.95, 0.99)], "cvar_X_author": list(map(float, b0["cvar_X"])),
                 "max_M_diff": float(np.max(np.abs(x0m[b["M"]] - x0a[b["M"]])))}
    L("7 status-quo LP: " + json.dumps(res["b0"], default=float))
    json.dump(res, open(os.path.join(RED, "red_mine.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
