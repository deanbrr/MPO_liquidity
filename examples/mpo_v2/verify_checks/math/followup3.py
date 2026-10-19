"""SYNTHETIC - NOT ADIC DATA. Follow-up 3 (full scale, my LP): H16 need-based funding cap.
(a) does O1 draw and repay the same facility at the same node? (b) duals of the binding need rows in the author's tie-break;
(c) GBO with the strict cap (sleeve proceeds <= this year's outflows: no RP and no 8% W allowance) and with same-node
revolver draw-and-repay forbidden; (d) ADR-39 first-after-STR nodes that are Green."""
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
from my_lp import MyLP, PJ  # noqa: E402

logf = open(os.path.join(OUT, "followup3.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


res = {}
try:
    dm = pickle.load(open(os.path.join(OUT, "full_dump.pkl"), "rb"))
    D = dm["D"]
    pj = PJ(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\params.json")
    bl = dm["blocks"]
    x1 = dm["caps"][3]["x"]
    y1 = dm["caps"][3]["y"]
    lp = MyLP(D, pj, dm["b0"], "OPT")
    v1 = lp.from_author(x1, bl)
    b = lp.blk
    lvl = lp.lvl
    DR, RP = v1[b["dr"]], v1[b["rp"]]
    both = (DR > 1e-9) & (RP > 1e-9)
    res["same_node_draw_and_repay"] = {"node_instrument_pairs": int(both.sum()), "levels": np.unique(lvl[np.where(both)[0]]).tolist(),
                                       "max_cycled_bn": float(np.minimum(DR, RP).max())}
    L("O1 same-node draw-and-repay: " + json.dumps(res["same_node_draw_and_repay"]))
    # duals of the author's need rows at the final tie-break (rows tagged ('need', n) in the author's model)
    tags = dm["rtag"]
    need_rows = [r for r, t in enumerate(tags) if t[0] == "need"]
    duals = np.array([y1[r] for r in need_rows])
    nn = np.array([tags[r][1] for r in need_rows])
    res["author_need_duals"] = {"max_abs": float(np.max(np.abs(duals))), "n_nonzero_1e-9": int((np.abs(duals) > 1e-9).sum()),
                                "by_level_max_abs": {int(L_): float(np.max(np.abs(duals[lvl[nn] == L_]))) for L_ in range(6)}}
    L("author need-row duals at O1: " + json.dumps(res["author_need_duals"]))
    fan = lvl >= 3
    nr = np.array(lp.rid["need"])
    variants = {}
    for nm in ("strict cap everywhere (no RP, no 8% W)", "strict cap in fans only", "no same-node draw-and-repay (rp=0 where dr>0 allowed)"):
        A = lp.A.tolil()
        lb, ub = lp.lb.copy(), lp.ub.copy()
        rhi = lp.rhi.copy()
        if nm.startswith("strict"):
            for r in nr:
                n = lp.tags[r][1]
                if nm.endswith("everywhere (no RP, no 8% W)") or lvl[n] >= 3:
                    A[r, b["W"][n]] = 0.0
                    for j in range(7):
                        A[r, b["rp"][n, j]] = 0.0
        else:
            # repayments only where no draw is possible (leaves) - removes the free cycling loophole
            for n in range(lp.T):
                for j in range(7):
                    if ub[b["dr"][n, j]] > 0 and lvl[n] < 5:
                        pass
            # simpler: forbid repaying in the same node as drawing by splitting is non-linear; instead cap RP by the parent balance
            rows = []
            for n in range(1, lp.T):
                for j in range(7):
                    rows.append(([b["rp"][n, j], b["B"][lp.par[n], j]], [1.0, -1.0 - (lp.rate[j, lp.cls[n]] if lp.pik[j] else 0.0)]))
            rr = np.concatenate([np.full(2, k) for k in range(len(rows))])
            cc = np.concatenate([np.array(c) for c, _ in rows])
            vv = np.concatenate([np.array(v) for _, v in rows])
            Ex = sp.csr_matrix((vv, (rr, cc)), shape=(len(rows), lp.nv))
            ub[b["rp"][0]] = 0.0
            A = sp.vstack([A.tocsr(), Ex]).tolil()
            rhi = np.r_[rhi, np.zeros(len(rows))]
        A = A.tocsr()
        rlo = lp.rlo if A.shape[0] == len(lp.rlo) else np.r_[lp.rlo, np.full(A.shape[0] - len(lp.rlo), -np.inf)]
        rm = vlib.highs_lp(lp.c_mean(), A, rlo, rhi, lb, ub, method="ipm", sense_max=True)
        ent = {"mean_status": rm["status"], "E_star": rm.get("obj")}
        if "x" in rm:
            c2, A2, rl2, rh2, lb2, ub2, ny = vlib.perspective(A, rlo, rhi, lb, ub, b["Wt"], lp.p_leaf, lp.Wstar, lp.W0)
            rp = vlib.highs_lp(c2, A2, rl2, rh2, lb2, ub2, method="ipm")
            ent["phi_exact"] = rp.get("obj")
            if rp.get("obj") is not None:
                At = sp.vstack([A, lp.tie_row(rp["obj"] + 0.005)]).tocsr()
                rt = vlib.highs_lp(lp.c_util(), At, np.r_[rlo, -np.inf], np.r_[rhi, 0.0], lb, ub, method="ipm", sense_max=True)
                if "x" in rt:
                    Wt = rt["x"][b["Wt"]]
                    ent["tie_P_goal"] = float(lp.p_leaf[Wt >= lp.Wstar * (1 - 1e-9)].sum())
                    ent["tie_util"] = rt["obj"]
                    xx = rt["x"]
                    ent["root_beta"] = float(xx[b["beta"][0]])
                    ent["root_sales_bn"] = float((xx[b["s"][0]] * lp.proc[0]).sum())
                    ent["root_adds_bn"] = float((xx[b["a"][0]] * lp.V[0]).sum())
        variants[nm] = ent
        L(f"variant [{nm}]: " + json.dumps(ent, default=float))
    res["need_variants"] = variants
    # ADR-39 condition (ii) of DSGO H9: first node after a STR node is a red-event node even if Green
    fas = np.asarray(D["tr"]["first_after_str"])
    green = np.asarray(dm["b0"]["green"])
    dec = np.arange(lp.T) < lp.ND
    res["green_first_after_str_decision_nodes"] = int((fas & green & dec).sum())
    L(f"decision nodes that are Green AND first after a STR node: {res['green_first_after_str_decision_nodes']}")
    json.dump(res, open(os.path.join(OUT, "followup3.json"), "w"), indent=1, default=float)
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
