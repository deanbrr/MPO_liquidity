"""SYNTHETIC - NOT ADIC DATA. Verification step 1: reproduce O1 at full scale with the author's code (read-only import),
capture every intermediate GBO solve, dump model + solutions for the independent checks."""
import json
import os
import pickle
import sys
import time

import numpy as np

SRC = r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2"
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
sys.dont_write_bytecode = True
logf = open(os.path.join(OUT, "full_o1.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


class Lg:
    def __call__(self, msg=""):
        L(msg)

    def solve(self, rec):
        L(f"  solve {rec['name']}: {rec['status']} t={rec['time_s']:.1f}s obj={rec.get('obj')}")


try:
    from common import Params
    import world
    import optim

    P = Params(os.path.join(SRC, "params.json"))
    lg = Lg()
    w = world.build(P, log=lg)
    D, m, m0, x0, b0 = w["D"], w["m"], w["m0"], w["x0"], w["b0"]
    L(f"W0 {D['W0']:.4f} W* {D['Wstar']:.4f} T {D['T']} ND {D['ND']} leaves {len(D['leaves'])} nvar {m.nvar} nrow {m.nrow}")
    base = {"lb": m._cur_lb.copy(), "ub": m._cur_ub.copy(), "rlb": m._cur_rlb.copy(), "rub": m._cur_rub.copy()}
    caps = []
    orig_run = m.run

    def run2(name, *a, **k):
        x, y, rec = orig_run(name, *a, **k)
        caps.append({"name": name, "x": None if x is None else x.copy(), "y": None if y is None else y.copy(),
                     "rc": None if m.last_rc is None else m.last_rc.copy(), "rec": rec,
                     "cost": m._cur_cost.copy(), "rlb": m._cur_rlb.copy(), "rub": m._cur_rub.copy()})
        return x, y, rec

    m.run = run2
    o1 = optim.gbo(m, lg, tag="O1 GBO")
    L(f"O1 label {o1['label']} phi {o1['phi']} hist {o1.get('phi_history')} E* {o1['E_star']} tie {o1.get('tie')}")
    st = optim.tree_stats(m, o1["x"])
    L("O1 tree stats " + json.dumps({k: (float(v) if not isinstance(v, bool) else v) for k, v in st.items()}))
    # model blocks and rows
    blocks = {k: np.asarray(v) for k, v in m.B.blocks.items()}
    dump = {"base": base, "A": m.A_mat.tocsr(), "rtag": list(m.B.rtag), "blocks": blocks,
            "rows": {k: (v if not isinstance(v, np.ndarray) else v.copy()) for k, v in m.rows.items()},
            "p_leaf": m.p_leaf.copy(), "levcap": m.levcap.copy(), "caps": caps, "o1": {k: v for k, v in o1.items()},
            "x0": x0, "b0": b0, "m0_blocks": {k: np.asarray(v) for k, v in m0.B.blocks.items()},
            "m0_A": m0.A_mat.tocsr(), "m0_lb": m0.lb.copy(), "m0_ub": m0.ub.copy(), "m0_rlb": m0.rlb.copy(),
            "m0_rub": m0.rub.copy(), "m0_rtag": list(m0.B.rtag), "m0_cost": m0.obj_b0(),
            "obj_util": m.obj_util(), "obj_mean": m.obj_mean(), "crra": (m.crra[0], m.crra[1]),
            "hf_units": m.hf_units.copy(), "nvar": m.nvar, "nrow": m.nrow, "phase1": w["phase1"]}
    Dd = {k: v for k, v in D.items() if k not in ("P",)}
    dump["D"] = Dd
    with open(os.path.join(OUT, "full_dump.pkl"), "wb") as f:
        pickle.dump(dump, f, protocol=4)
    L("dump written")
    # compare with results.json
    R = json.load(open(os.path.join(SRC, "results.json"), encoding="utf-8"))
    g = R["solutions"]["GBO"]
    L(f"results.json GBO phi {g['phi']} E* {g['E_star_bn']} p_goal {g['tree']['p_goal']} bpoe {g['tree']['bpoe']}")
    L(f"repro      GBO phi {o1['phi']:.6g} E* {o1['E_star']:.6g} p_goal {st['p_goal']:.6g} bpoe {st['bpoe']:.6g}")
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
