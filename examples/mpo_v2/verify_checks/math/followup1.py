"""SYNTHETIC - NOT ADIC DATA. Follow-ups: red-tier sales at exactly the red-event threshold (knife edge), the tie row on
the author's solutions, the reduced tie-break with HiGHS IPM, and where W~ < 0 comes from in the min-W~ LP."""
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

logf = open(os.path.join(OUT, "followup1.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


res = {}
try:
    thr = 0.05
    for tag, dpath, ppath in (("reduced", os.path.join(RED, "red_dump.pkl"), os.path.join(RED, "params.json")),
                              ("full", os.path.join(OUT, "full_dump.pkl"), r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\params.json")):
        dm = pickle.load(open(dpath, "rb"))
        bl = dm["blocks"]
        D = dm["D"]
        lvl = np.asarray(D["tr"]["level"])
        prob = np.asarray(D["tr"]["prob"])
        cands = {"O1": dm["caps"][3]["x"]}
        if tag == "reduced":
            cands["exact MILP"] = dm["milp"]["x"]
            cands["round MILP"] = dm["round"]["x"]
        for nm, x in cands.items():
            RS = x[bl["RS"]]
            S = x[bl["s"]]
            red = np.array([u["tier"] == "red" for u in D["units"]])
            pos = RS > 1e-9
            at_thr = np.abs(RS - thr) < 1e-9
            above = RS > thr
            # leaves flagged by the author's tree_stats rule (M > 1e-6 or RS > thr on the path)
            flagged = []
            for li, leaf in enumerate(D["leaves"]):
                path = D["anc"][leaf]
                if np.any(x[bl["M"][path]] > 1e-6) or np.any(x[bl["RS"][path]] > thr):
                    flagged.append(li)
            pl = dm["p_leaf"]
            ent = {"nodes_with_red_sales": int(pos.sum()), "nodes_at_threshold": int(at_thr.sum()), "nodes_strictly_above_thr_float": int(above.sum()),
                   "max_RS_minus_thr": float((RS - thr).max()), "levels_of_red_sales": np.unique(lvl[pos]).tolist(),
                   "prob_mass_of_nodes_at_thr": float(prob[at_thr].sum()), "tree_stats_flagged_leaf_prob": float(pl[flagged].sum()),
                   "red_tier_sell_frac_max_at_decision_nodes": float((S[:, red]).max()) if red.any() else 0.0}
            res[f"{tag}:{nm}"] = ent
            L(f"{tag} {nm}: {json.dumps(ent)}")
    # ---------------- tie row and my IPM tie-break on the reduced instance
    dm = pickle.load(open(os.path.join(RED, "red_dump.pkl"), "rb"))
    pj = PJ(os.path.join(RED, "params.json"))
    lp = MyLP(dm["D"], pj, dm["b0"], "OPT")
    bl = dm["blocks"]
    pt = dm["o1"]["tie"]["pt"]
    xa = lp.from_author(dm["caps"][3]["x"], bl)
    trow = lp.tie_row(pt)
    res["reduced_author_tie_row_value"] = float((trow @ xa)[0])
    At = sp.vstack([lp.A, trow]).tocsr()
    rl, rh = np.r_[lp.rlo, -np.inf], np.r_[lp.rhi, 0.0]
    ti = vlib.highs_lp(lp.c_util(), At, rl, rh, lp.lb, lp.ub, method="ipm", sense_max=True)
    res["reduced_tie_mine_ipm"] = ti["obj"]
    res["reduced_tie_author"] = dm["caps"][3]["rec"]["obj"]
    res["reduced_tie_author_util_in_mine"] = float(lp.c_util() @ xa)
    # dual simplex again with tight tolerances
    ts = vlib.highs_lp(lp.c_util(), At, rl, rh, lp.lb, lp.ub, method="simplex", sense_max=True, feas_tol=1e-9)
    res["reduced_tie_mine_simplex_tol1e-9"] = ts["obj"]
    L("reduced tie-break: " + json.dumps({k: v for k, v in res.items() if k.startswith("reduced_tie") or k.startswith("reduced_author")}, default=float))
    # ---------------- where does W~ < 0 come from? minimise W~ at the worst leaf, then with BRK capped at the breach
    li = 27
    c = np.zeros(lp.nv)
    c[lp.blk["Wt"][li]] = 1.0
    r1 = vlib.highs_lp(c, lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="simplex")
    x = r1["x"]
    b = lp.blk
    leaf = lp.leaves[li]
    path = lp.anc[leaf]
    comp = {"Wt": float(x[b["Wt"][li]]), "W_leaf": float(x[b["W"][leaf]]),
            "range_charge": float(sum(pj("constraints.range_charge") * x[b["brk"][m]].sum() for m in path if lp.lvl[m] <= 2 and lp.cls[m] != 2)),
            "brk_total_on_path": float(sum(x[b["brk"][m]].sum() for m in path if lp.lvl[m] <= 2))}
    res["minWt_leaf27_components"] = comp
    # cap BRK at the actual breach: add BRK <= breach rows is not linear; instead bound BRK by a generous 200 $bn and re-run
    ub2 = lp.ub.copy()
    ub2[b["brk"]] = 0.0
    lb2 = lp.lb.copy()
    # with BRK fixed at zero the IC-range rows become hard: use them only as a lower bound check on W_leaf
    rW = np.zeros(lp.nv)
    rW[b["W"][leaf]] = 1.0
    r2 = vlib.highs_lp(rW, lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="simplex")
    res["min_W_leaf27"] = r2.get("obj")
    L("min W~ components at leaf 27: " + json.dumps(comp, default=float) + f"; min W at that leaf node {r2.get('obj')}")
    # minimise W~ at leaf 27 with the range charge at its minimum: two-stage (min W~ s.t. BRK penalised heavily)
    c3 = c.copy()
    c3[b["brk"].ravel()] = 1e3
    r3 = vlib.highs_lp(c3, lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="simplex")
    res["minWt_leaf27_minimal_brk"] = float(r3["x"][b["Wt"][li]])
    L(f"min W~ at leaf 27 with BRK kept minimal: {res['minWt_leaf27_minimal_brk']:.3f}")
    json.dump(res, open(os.path.join(OUT, "followup1.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
