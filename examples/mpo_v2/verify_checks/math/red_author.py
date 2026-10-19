"""SYNTHETIC - NOT ADIC DATA. Reduced instance, AUTHOR side: the author's pipeline (read-only import) on the reduced
params: B0 readings, Phase I, GBO (every solve captured), exact max-P(goal) MILP by HiGHS branch and bound (gap 1e-6),
the 'round' comparison, and CRRA+L2. Dumps everything for the independent side."""
import json
import os
import pickle
import sys
import time

import numpy as np

SRC = r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2"
OUT = os.path.dirname(os.path.abspath(__file__))
RED = os.path.join(OUT, "reduced")
sys.path.insert(0, SRC)
sys.dont_write_bytecode = True
logf = open(os.path.join(RED, "red_author.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


class Lg:
    def __call__(self, msg=""):
        L(msg)

    def solve(self, rec):
        L(f"  solve {rec['name']}: {rec['status']} t={rec['time_s']:.2f}s obj={rec.get('obj')} gap={rec.get('mip_gap')} nodes={rec.get('mip_nodes')} bound={rec.get('dual_bound')}")


try:
    from common import Params
    import world
    import optim

    P = Params(os.path.join(RED, "params.json"))
    lg = Lg()
    w = world.build(P, log=lg)
    D, m, m0, x0, b0 = w["D"], w["m"], w["m0"], w["x0"], w["b0"]
    L(f"W0 {D['W0']:.4f} W* {D['Wstar']:.4f} T {D['T']} ND {D['ND']} leaves {len(D['leaves'])} nvar {m.nvar} nrow {m.nrow}"
      f" rank_rule {D['tr']['checks']['rank_rule']}")
    base = {"lb": m._cur_lb.copy(), "ub": m._cur_ub.copy(), "rlb": m._cur_rlb.copy(), "rub": m._cur_rub.copy()}
    caps = []
    orig_run = m.run

    def run2(name, *a, **k):
        x, y, rec = orig_run(name, *a, **k)
        caps.append({"name": name, "x": None if x is None else x.copy(), "rec": rec})
        return x, y, rec

    m.run = run2
    o1 = optim.gbo(m, lg, tag="R-O1 GBO")
    st = optim.tree_stats(m, o1["x"])
    L(f"O1 label {o1['label']} phi {o1['phi']} hist {o1.get('phi_history')} E* {o1['E_star']} tie {o1.get('tie')}")
    L("O1 stats " + json.dumps({k: (float(v) if not isinstance(v, bool) else v) for k, v in st.items()}))
    m.run = orig_run
    # exact MILP (HiGHS branch and bound), started from O1 as the author does
    t0 = time.time()
    mx = optim.milp(m, lg, o1["x"], time_limit=1500.0, node_limit=10 ** 9, tag="R-O2 exact", heuristics=True)
    L(f"exact MILP done in {time.time() - t0:.1f}s: {mx['rec']}")
    milp_x = mx["x"]
    stm = optim.tree_stats(m, milp_x) if milp_x is not None else None
    if stm:
        L("MILP stats " + json.dumps({k: (float(v) if not isinstance(v, bool) else v) for k, v in stm.items()}))
    # the 'round' comparison the run actually used
    mr = optim.milp_round(m, lg, o1["x"], tag="R-O2 round")
    L(f"round: {json.dumps({k: v for k, v in mr['rec'].items() if k != 'rounding'}, default=float)}")
    L(f"round tries: {mr['rec']['rounding']}")
    str_ = optim.tree_stats(m, mr["x"])
    # CRRA + L2
    o3 = optim.crra(m, lg)
    st3 = optim.tree_stats(m, o3["x"]) if o3["x"] is not None else None
    dump = {"D": {k: v for k, v in D.items() if k != "P"}, "b0": b0, "x0": x0, "base": base, "blocks": {k: np.asarray(v) for k, v in m.B.blocks.items()},
            "A": m.A_mat.tocsr(), "rtag": list(m.B.rtag), "caps": caps, "o1": o1, "o1_stats": st, "milp": mx, "milp_stats": stm,
            "round": mr, "round_stats": str_, "o3": o3, "o3_stats": st3, "p_leaf": m.p_leaf.copy(), "phase1": w["phase1"],
            "m0_blocks": {k: np.asarray(v) for k, v in m0.B.blocks.items()}, "m0_A": m0.A_mat.tocsr(), "m0_rtag": list(m0.B.rtag),
            "m0_lb": m0.lb.copy(), "m0_ub": m0.ub.copy(), "m0_rlb": m0.rlb.copy(), "m0_rub": m0.rub.copy(), "m0_cost": m0.obj_b0(),
            "nvar": m.nvar, "nrow": m.nrow}
    with open(os.path.join(RED, "red_dump.pkl"), "wb") as f:
        pickle.dump(dump, f, protocol=4)
    L("dump written")
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
