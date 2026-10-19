"""SYNTHETIC - NOT ADIC DATA. Follow-up 2 (full scale, my LP): is H9 degenerate? R_l distribution of O1; GBO E* and exact
Phi* with H9 at eps 0.006 / 0.05, with H9 replaced by the hard per-node rule (M_n <= 0 and RS_n <= thr everywhere), and
without H9. Plus Clarabel with tight settings on the reduced tie-break."""
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

logf = open(os.path.join(OUT, "followup2.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


res = {}
try:
    # ---------------- reduced: Clarabel with tight settings on the tie-break
    dmr = pickle.load(open(os.path.join(RED, "red_dump.pkl"), "rb"))
    pjr = PJ(os.path.join(RED, "params.json"))
    lpr = MyLP(dmr["D"], pjr, dmr["b0"], "OPT")
    pt = dmr["o1"]["tie"]["pt"]
    At = sp.vstack([lpr.A, lpr.tie_row(pt)]).tocsr()
    rl, rh = np.r_[lpr.rlo, -np.inf], np.r_[lpr.rhi, 0.0]
    for scale in (1.0, 1000.0):
        rc = vlib.clarabel_lp(lpr.c_util() * scale, At, rl, rh, lpr.lb, lpr.ub, sense_max=True, tol=1e-12, max_iter=2000)
        res[f"reduced_tie_clarabel_tight_scale{scale:g}"] = {"obj": rc["obj"] / scale, "status": rc["status"], "iters": rc["iters"]}
        L(f"reduced tie-break Clarabel tol 1e-12, objective x{scale:g}: {rc['status']} obj {rc['obj']/scale:.14f} iters {rc['iters']} (author {dmr['caps'][3]['rec']['obj']:.14f})")
    rp = vlib.clarabel_lp(lpr.c_mean(), lpr.A, lpr.rlo, lpr.rhi, lpr.lb, lpr.ub, sense_max=True, tol=1e-12, max_iter=2000)
    L(f"reduced mean LP Clarabel tol 1e-12: {rp['status']} obj {rp['obj']:.12f} (author {dmr['caps'][0]['rec']['obj']:.12f})")
    res["reduced_mean_clarabel_tight"] = rp["obj"]
    # ---------------- full scale: H9 degeneracy
    dm = pickle.load(open(os.path.join(OUT, "full_dump.pkl"), "rb"))
    pj = PJ(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\params.json")
    bl = dm["blocks"]
    x1 = dm["caps"][3]["x"]
    D = dm["D"]
    thr = pj("constraints.red_sale_threshold")
    Rl = np.array([max(np.max(x1[bl["M"][D["anc"][f]]]), np.max(x1[bl["RS"][D["anc"][f]]] - thr)) for f in D["leaves"]])
    pl = dm["p_leaf"]
    res["O1_R_leaf"] = {"P(R=0)": float(pl[np.abs(Rl) < 1e-9].sum()), "P(R<0)": float(pl[Rl < -1e-9].sum()), "P(R>0)": float(pl[Rl > 1e-9].sum()),
                        "eta_R": float(x1[bl["eta_R"]][0]), "CVaR_eps(R)": vlib.cvar_upper(Rl, pl, 0.006)}
    L("O1 red statistic R_l: " + json.dumps(res["O1_R_leaf"], default=float))
    variants = {}
    for nm in ("eps 0.006 (as run)", "eps 0.05", "hard per-node rule", "no H9"):
        eps = {"eps 0.006 (as run)": 0.006, "eps 0.05": 0.05, "hard per-node rule": 0.006, "no H9": 1.0}[nm]
        lp = MyLP(D, pj, dm["b0"], "OPT", eps_red=eps)
        A, rlo, rhi = lp.A, lp.rlo.copy(), lp.rhi.copy()
        if nm == "hard per-node rule":
            # drop the CVaR row and impose M_n <= 0 and RS_n <= thr at every node of the tree
            r = lp.r_H9
            rlo[r], rhi[r] = -np.inf, np.inf
            T = lp.T
            ex = sp.vstack([sp.csr_matrix((np.ones(T), (np.arange(T), lp.blk["M"])), shape=(T, lp.nv)),
                            sp.csr_matrix((np.ones(T), (np.arange(T), lp.blk["RS"])), shape=(T, lp.nv))]).tocsr()
            A = sp.vstack([A, ex]).tocsr()
            rlo = np.r_[rlo, np.full(2 * T, -np.inf)]
            rhi = np.r_[rhi, np.zeros(T), np.full(T, thr)]
        rm = vlib.highs_lp(lp.c_mean(), A, rlo, rhi, lp.lb, lp.ub, method="ipm", sense_max=True)
        c2, A2, rl2, rh2, lb2, ub2, ny = vlib.perspective(A, rlo, rhi, lp.lb, lp.ub, lp.blk["Wt"], lp.p_leaf, lp.Wstar, lp.W0)
        rpp = vlib.highs_lp(c2, A2, rl2, rh2, lb2, ub2, method="ipm")
        variants[nm] = {"E_star": rm.get("obj"), "phi_exact": rpp.get("obj")}
        L(f"H9 variant [{nm}]: E* {rm.get('obj')}  exact Phi* {rpp.get('obj')}")
    res["H9_variants"] = variants
    json.dump(res, open(os.path.join(OUT, "followup2.json"), "w"), indent=1, default=float)
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
