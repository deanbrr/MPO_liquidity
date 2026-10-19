"""SYNTHETIC - NOT ADIC DATA. Follow-up 4: does the H16 loophole change the recommendation out of sample?
GBO tie-break root decisions under (a) the model as run, (b) no same-node draw-and-repay, (c) strict H16 in fans,
(d) strict H16 everywhere, each certified with rule recourse on the author's certification paths (seed 31, 10,000)."""
import json
import os
import pickle
import sys
import time

import numpy as np
import scipy.sparse as sp

SRC = r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2"
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
sys.path.insert(1, OUT)
sys.dont_write_bytecode = True
logf = open(os.path.join(OUT, "followup4.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


res = {}
try:
    import vlib
    from my_lp import MyLP, PJ
    from common import Params, cvar_lower
    import world
    import sim as simmod

    dm = pickle.load(open(os.path.join(OUT, "full_dump.pkl"), "rb"))
    D = dm["D"]
    pj = PJ(os.path.join(SRC, "params.json"))
    lp = MyLP(D, pj, dm["b0"], "OPT")
    b = lp.blk
    lvl = lp.lvl
    nr = np.array(lp.rid["need"])

    def solve(variant):
        A = lp.A.tolil()
        lb, ub = lp.lb.copy(), lp.ub.copy()
        rlo, rhi = lp.rlo.copy(), lp.rhi.copy()
        if variant in ("strict fans", "strict all"):
            for r in nr:
                n = lp.tags[r][1]
                if variant == "strict all" or lvl[n] >= 3:
                    A[r, b["W"][n]] = 0.0
                    for j in range(7):
                        A[r, b["rp"][n, j]] = 0.0
        A = A.tocsr()
        if variant == "no cycling":
            rows = []
            for n in range(1, lp.T):
                for j in range(7):
                    rows.append(([b["rp"][n, j], b["B"][lp.par[n], j]], [1.0, -1.0 - (lp.rate[j, lp.cls[n]] if lp.pik[j] else 0.0)]))
            rr = np.concatenate([np.full(2, k) for k in range(len(rows))])
            cc = np.concatenate([np.array(c) for c, _ in rows])
            vv = np.concatenate([np.array(v) for _, v in rows])
            A = sp.vstack([A, sp.csr_matrix((vv, (rr, cc)), shape=(len(rows), lp.nv))]).tocsr()
            rlo = np.r_[rlo, np.full(len(rows), -np.inf)]
            rhi = np.r_[rhi, np.zeros(len(rows))]
            ub[b["rp"][0]] = 0.0
        c2, A2, rl2, rh2, lb2, ub2, ny = vlib.perspective(A, rlo, rhi, lb, ub, b["Wt"], lp.p_leaf, lp.Wstar, lp.W0)
        rp = vlib.highs_lp(c2, A2, rl2, rh2, lb2, ub2, method="ipm")
        phi = rp["obj"] if variant != "as run" else dm["o1"]["phi"]
        At = sp.vstack([A, lp.tie_row(phi + 0.005)]).tocsr()
        rt = vlib.highs_lp(lp.c_util(), At, np.r_[rlo, -np.inf], np.r_[rhi, 0.0], lb, ub, method="ipm", sense_max=True)
        return rp["obj"], rt["x"]

    P = Params(os.path.join(SRC, "params.json"))
    w = world.build(P, log=None, phase1=False)
    truth = w["book"]["truth"]
    pols = {"B0": {"kind": "B0", "restore8": False}}
    tree_stats = {}
    for v in ("as run", "no cycling", "strict fans", "strict all"):
        t0 = time.time()
        phi, x = solve(v)
        root = {"sell": np.clip(x[b["s"][0]], 0, None), "redeem": np.clip(x[b["r"][0]], 0, None), "add": np.clip(x[b["a"][0]], 0, None),
                "tpl": np.clip(x[b["y"][0]], 0, None), "p2s": float(x[b["pi"][0]]), "beta": float(x[b["beta"][0]]),
                "trs": np.clip(x[b["trs"][0]], 0, None), "hed": float(x[b["hed"][0]]), "opp": float(x[b["opp"][0]]),
                "fin": np.clip(x[b["B"][0]], 0, None), "Lup": float(x[b["Lup"][0]])}
        pols[v] = {"kind": "plan", "root": root, "playbook": False, "restore8": True, "nodes": {}, "stage1": [], "children": {},
                   "playbook_years": (1,)}
        Wt = x[b["Wt"]]
        tree_stats[v] = {"phi_exact": phi, "P_goal_tree": float(lp.p_leaf[Wt >= lp.Wstar * (1 - 1e-9)].sum()),
                         "root_beta": root["beta"], "root_E_over_W": float(x[b["E"][0]] / x[b["W"][0]]),
                         "root_LQ_over_W": float(x[b["LQ"][0]] / x[b["W"][0]]), "root_term_debt": float(root["fin"][1]),
                         "root_redeem_bn": float((root["redeem"] * lp.V[0]).sum()), "root_adds_bn": float((root["add"] * lp.V[0]).sum()),
                         "root_commit": root["tpl"][lp.is_commit].round(3).tolist(), "time_s": time.time() - t0}
        L(f"[{v}] " + json.dumps(tree_stats[v], default=float))
    s = simmod.Sim(w["D"], w["gen"], 10000, P.get("seeds.cert"), truth, P.get("simulation.chunk"), idio=True, tpl_truth_seed=502)
    out = s.evaluate(pols)
    oos = {}
    for k in pols:
        tw = out[k]["twr"]
        oos[k] = {"P_goal": float(np.mean(tw >= 0.10)), "twr_mean": float(tw.mean()), "cvar10": cvar_lower(tw, 0.10), "P_red": float(out[k]["red"].mean())}
        if k != "B0":
            d = (tw >= 0.10).astype(float) - (out["as run"]["twr"] >= 0.10).astype(float)
            oos[k]["dP_vs_as_run"] = float(d.mean())
            oos[k]["dP_se"] = float(d.std(ddof=1) / np.sqrt(len(d)))
        L(f"OOS rule recourse [{k}]: " + json.dumps(oos[k], default=float))
    res = {"tree": tree_stats, "oos": oos}
    json.dump(res, open(os.path.join(OUT, "followup4.json"), "w"), indent=1, default=float)
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
