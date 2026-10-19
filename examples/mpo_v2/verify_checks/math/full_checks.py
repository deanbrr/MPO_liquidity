"""SYNTHETIC - NOT ADIC DATA. Verification step 2 (full scale): bPOE / CVaR numerics, every row and bound of O1 at
every node, exact perspective-LP bPOE minimum (HiGHS), MILP relaxation without the eps margin, L=0 checks."""
import json
import os
import pickle
import sys
import time

import numpy as np
import scipy.sparse as sp

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, OUT)
import vlib  # noqa: E402

logf = open(os.path.join(OUT, "full_checks.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


res = {}
try:
    dm = pickle.load(open(os.path.join(OUT, "full_dump.pkl"), "rb"))
    D = dm["D"]
    W0, Ws = D["W0"], D["Wstar"]
    p = dm["p_leaf"]
    bl = dm["blocks"]
    WT = bl["Wt"]
    caps = dm["caps"]
    names = [c["name"] for c in caps]
    L(f"captured solves: {names}")
    xm = caps[0]["x"]; xb = caps[1]["x"]; xc = caps[2]["x"]; x1 = caps[3]["x"]
    X = lambda x: (Ws - x[WT]) / W0
    # ---------------------------------------------------------------- A. bPOE / CVaR
    A_ = {}
    for nm, x in (("mean LP", xm), ("min-CVaR (p=0.9573)", xb), ("certificate (p=0.9557)", xc), ("O1 tie-break", x1)):
        Xv = X(x)
        b, a = vlib.bpoe0(Xv, p)
        bc = vlib.bpoe_by_cvar(Xv, p)
        A_[nm] = {"bpoe_enum": b, "a_star": a, "buffer_c_star_W0": (1 / a if a > 0 else None), "bpoe_by_cvar_root": bc,
                  "P_goal": float(p[x[WT] >= Ws * (1 - 1e-9)].sum()), "E_Wt": float(p @ x[WT]),
                  "max_Wt_minus_Wstar_W0": float((x[WT].max() - Ws) / W0)}
    pk0 = A_["mean LP"]["bpoe_enum"]
    # the LP objective of the min-CVaR solve equals CVaR_{1-pk0}(X(xb))
    obj_b = caps[1]["rec"]["obj"]
    cv_sort = vlib.cvar_upper(X(xb), p, pk0)
    cv_ru = vlib.cvar_upper_ru(X(xb), p, pk0)
    eta_b = float(xb[bl["eta_b"]][0]); ub_b = xb[bl["ub"]]
    A_["minCVaR_LP_obj"] = obj_b
    A_["minCVaR_direct_sort"] = cv_sort
    A_["minCVaR_direct_RU_scan"] = cv_ru
    A_["minCVaR_LP_eta"] = eta_b
    A_["minCVaR_ub_minus_hinge_maxabs"] = float(np.max(np.abs(ub_b - np.maximum(X(xb) - eta_b, 0.0))))
    pc = A_["min-CVaR (p=0.9573)"]["bpoe_enum"] - 1e-3
    A_["certificate_p"] = pc
    A_["certificate_LP_obj"] = caps[2]["rec"]["obj"]
    A_["certificate_direct_CVaR_of_its_solution"] = vlib.cvar_upper(X(xc), p, pc)
    # O1: the tie-break row  pt*eta + sum p ub <= 0  (pt = phi + 0.005)
    pt = dm["o1"]["tie"]["pt"]
    eta1 = float(x1[bl["eta_b"]][0]); ub1 = x1[bl["ub"]]
    A_["O1_tie_pt"] = pt
    A_["O1_tie_row_value"] = float(pt * eta1 + p @ ub1)
    A_["O1_CVaR_at_pt_direct"] = vlib.cvar_upper(X(x1), p, pt)
    A_["O1_CVaR_at_phi_direct"] = vlib.cvar_upper(X(x1), p, dm["o1"]["phi"])
    A_["O1_ub_ge_hinge_min"] = float(np.min(ub1 - np.maximum(X(x1) - eta1, 0.0)))
    res["A_bpoe_cvar"] = A_
    L("A " + json.dumps(A_, indent=1, default=float))
    # ---------------------------------------------------------------- B. every row and bound of O1
    A = dm["A"]
    base = dm["base"]
    tags = dm["rtag"]
    rep = vlib.row_report(A, x1, base["rlb"], base["rub"], tags)
    lbv, ubv = base["lb"], base["ub"]
    bviol_lo = np.maximum(lbv - x1, 0.0)
    bviol_hi = np.maximum(x1 - ubv, 0.0)
    inv = {}
    for k, v in bl.items():
        for j in np.asarray(v).ravel():
            inv[int(j)] = k
    worst_lo = int(np.argmax(bviol_lo)); worst_hi = int(np.argmax(bviol_hi))
    B_ = {"rows": rep, "bound_viol_lo": float(bviol_lo.max()), "bound_viol_lo_block": inv[worst_lo],
          "bound_viol_hi": float(bviol_hi.max()), "bound_viol_hi_block": inv[worst_hi],
          "slacks_sum": float(sum(x1[bl[s]].sum() for s in ("sl3", "sl4", "sl11", "sl15", "sl9")))}
    res["B_rows"] = B_
    L("B rows: max violation by row family")
    for t, d in sorted(rep.items()):
        L(f"   {t:10s} rows {d['rows']:6d} max_viol {d['max_viol']:.3e} binding {d['binding']:5d} min_slack {d['min_slack']:.3e} worst {d['worst']}")
    L(f"   bounds: lo viol {B_['bound_viol_lo']:.3e} ({B_['bound_viol_lo_block']}), hi viol {B_['bound_viol_hi']:.3e} ({B_['bound_viol_hi_block']}); slacks {B_['slacks_sum']:.3e}")
    # B0 readings: BRK in the status-quo LP (no cost in the B0 objective) vs the minimal breach
    x0 = dm["x0"]
    b0b = dm["m0_blocks"]
    m0A, m0tags = dm["m0_A"], dm["m0_rtag"]
    ax0 = m0A @ x0
    brk_rows = {}
    for r, t in enumerate(m0tags):
        if t[0] in ("brk_hi", "brk_lo"):
            brk_rows.setdefault((t[1], t[2]), []).append((t[0], r))
    from_rows = []
    GR = ["PE", "SEC", "CO", "CS", "PC", "HF", "LO", "RA"]
    for (n, g), lst in brk_rows.items():
        gk = GR.index(g)
        col = b0b["brk"][n, gk]
        v = x0[col]
        need = 0.0
        for kind, r in lst:
            # row: (+-)group + BRK (+-) w W >= 0  -> BRK >= -(rest)
            rest = ax0[r] - m0A[r, col] * v
            need = max(need, -rest / m0A[r, col])
        from_rows.append((n, g, v, max(need, 0.0)))
    excess = [(n, g, v, need) for n, g, v, need in from_rows if v > need + 1e-7]
    res["B0_brk_excess"] = {"n_cells": len(from_rows), "n_excess": len(excess), "max_excess": float(max([v - nd for _, _, v, nd in excess], default=0.0)),
                            "examples": excess[:5]}
    L(f"B0 BRK cells {len(from_rows)}, with BRK above the minimal breach: {len(excess)}; max excess {res['B0_brk_excess']['max_excess']:.3e}")
    # ---------------------------------------------------------------- C. perspective LP (exact min bPOE, one LP)
    for amin_name, amin in (("bPOE (a>=0)", 0.0), ("GBO Phi (a>=a_min)", 1.0 / (2.0 * Ws / W0))):
        c2, A2, rlb2, rub2, lb2, ub2, ny = vlib.perspective(A, base["rlb"], base["rub"], base["lb"], base["ub"],
                                                            WT, p, Ws, W0, a_min=amin)
        L(f"perspective LP [{amin_name}]: {A2.shape[0]} rows x {A2.shape[1]} cols, nnz {A2.nnz}")
        r = vlib.highs_lp(c2, A2, rlb2, rub2, lb2, ub2, method="ipm")
        L(f"   HiGHS IPM status {r['status']} time {r['time']:.1f}s obj {r.get('obj')}")
        if "x" in r:
            tau = r["x"][ny]
            xs = r["x"][:ny] / tau
            Xv = X(xs)
            b, a = vlib.bpoe0(Xv, p, amin)
            ax = A @ xs
            fl = vlib.finite(base["rlb"]); fu = vlib.finite(base["rub"])
            viol = max(np.max(np.where(fl, base["rlb"] - ax, -np.inf)), np.max(np.where(fu, ax - base["rub"], -np.inf)))
            res[f"C_persp_{amin}"] = {"obj": r["obj"], "tau": float(tau), "buffer_W0": float(1 / tau), "bpoe_of_x": b,
                                     "a_star_of_x": a, "max_row_viol_of_x": float(viol), "P_goal": float(p[xs[WT] >= Ws * (1 - 1e-9)].sum()),
                                     "E_Wt": float(p @ xs[WT])}
            L("   " + json.dumps(res[f"C_persp_{amin}"], default=float))
            if amin == 0.0:
                np.save(os.path.join(OUT, "full_persp_x.npy"), xs)
    # ---------------------------------------------------------------- D. MILP relaxation: with and without the eps margin
    eps_g = 0.001
    Lf = len(WT)
    nv = A.shape[1]
    for eps in (eps_g, 0.0):
        Mb = Ws + eps * W0
        G = sp.csr_matrix((np.r_[np.ones(Lf), -Mb * np.ones(Lf)], (np.r_[np.arange(Lf), np.arange(Lf)], np.r_[WT, nv + np.arange(Lf)])),
                          shape=(Lf, nv + Lf))
        Af = sp.vstack([sp.hstack([A, sp.csr_matrix((A.shape[0], Lf))]), G]).tocsr()
        c = np.r_[np.zeros(nv), p]
        r = vlib.highs_lp(c, Af, np.r_[base["rlb"], np.zeros(Lf)], np.r_[base["rub"], np.full(Lf, np.inf)],
                          np.r_[base["lb"], np.zeros(Lf)], np.r_[base["ub"], np.ones(Lf)], method="ipm", sense_max=True)
        L(f"MILP relaxation eps={eps}: {r['status']} obj {r.get('obj')} time {r['time']:.1f}s")
        res[f"D_relax_eps_{eps}"] = r.get("obj")
        if "x" in r:
            xr = r["x"]
            g = xr[nv:]
            frac = np.minimum(1.0, xr[WT] / Mb)
            res[f"D_relax_eps_{eps}_check_g_eq_min1_Wt_over_M"] = float(np.max(np.abs(g - np.clip(frac, 0, 1))))
            res[f"D_relax_eps_{eps}_E_min1_Wt_over_M"] = float(p @ np.clip(frac, 0, 1))
    json.dump(res, open(os.path.join(OUT, "full_checks.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
