"""SYNTHETIC - NOT ADIC DATA. Verification step 3 (full scale): the author's O1 checked against MY independent rows
(every node, fan year and leaf); my LP re-solved (mean LP, min CVaR, tie-break) with HiGHS and, where it fits, Clarabel."""
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

logf = open(os.path.join(OUT, "my_full.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


def viol_report(lp, v, label):
    ax = lp.A @ v
    fl, fu = vlib.finite(lp.rlo), vlib.finite(lp.rhi)
    lo_v = np.where(fl, lp.rlo - ax, -np.inf)
    hi_v = np.where(fu, ax - lp.rhi, -np.inf)
    viol = np.maximum(np.maximum(lo_v, hi_v), 0.0)
    fams = {}
    for r, t in enumerate(lp.tags):
        d = fams.setdefault(t[0], [0, 0.0, None])
        d[0] += 1
        if viol[r] > d[1]:
            d[1], d[2] = float(viol[r]), t
    bl = np.maximum(lp.lb - v, 0.0).max()
    bu = np.maximum(v - lp.ub, 0.0).max()
    L(f"{label}: worst row violation {viol.max():.3e}; bounds lo {bl:.3e} hi {bu:.3e}")
    for k, (nr, mv, t) in sorted(fams.items()):
        if mv > 1e-9:
            L(f"    VIOLATED {k:10s} rows {nr:6d} max {mv:.3e} at {t}")
    return fams, float(viol.max()), float(max(bl, bu))


try:
    dm = pickle.load(open(os.path.join(OUT, "full_dump.pkl"), "rb"))
    D = dm["D"]
    pj = PJ(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\params.json")
    t0 = time.time()
    lp = MyLP(D, pj, dm["b0"], "OPT")
    L(f"my LP built in {time.time() - t0:.1f}s: {lp.A.shape[0]} rows x {lp.nv} cols, nnz {lp.A.nnz} (author: {dm['nrow']} x {dm['nvar']})")
    L("data recomputed vs prepared arrays (max abs diff): " + json.dumps(lp.chk, default=float))
    bl = dm["blocks"]
    caps = dm["caps"]
    out = {"chk": lp.chk, "size": [int(lp.A.shape[0]), int(lp.nv), int(lp.A.nnz)]}
    for nm, k in (("O1 (tie-break)", 3), ("mean LP", 0), ("min-CVaR", 1)):
        v = lp.from_author(caps[k]["x"], bl)
        fams, mv, mb = viol_report(lp, v, f"author's {nm} in my rows")
        out[f"author_{k}_in_mine"] = {"max_row_viol": mv, "max_bound_viol": mb}
    v1 = lp.from_author(caps[3]["x"], bl)
    out["author_O1_my_util"] = float(lp.c_util() @ v1)
    out["author_O1_my_mean"] = float(lp.c_mean() @ v1)
    L(f"author O1 objective values in my model: E[util] {out['author_O1_my_util']:.12f} (author LP {-caps[3]['rec']['obj']:.12f}); E[Wt] {out['author_O1_my_mean']:.9f}")
    # ---------------- my LP re-solved with HiGHS (dual simplex: a different algorithm path from the author's IPM)
    r = vlib.highs_lp(lp.c_mean(), lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="ipm", sense_max=True)
    L(f"MY mean LP (HiGHS ipm): {r['status']} obj {r.get('obj')} time {r['time']:.1f}s  (author {caps[0]['rec']['obj']})")
    out["my_mean_highs"] = r.get("obj")
    if "x" in r:
        np.save(os.path.join(OUT, "my_full_mean_x.npy"), r["x"])
    pk = 0.9572695202620741
    r2 = vlib.highs_lp(lp.c_cvar(pk), lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, method="ipm")
    L(f"MY min CVaR at p={pk}: {r2['status']} obj {r2.get('obj')} time {r2['time']:.1f}s (author {caps[1]['rec']['obj']})")
    out["my_mincvar_highs"] = r2.get("obj")
    if "x" in r2:
        b, a = vlib.bpoe0((lp.Wstar - r2["x"][lp.blk["Wt"]]) / lp.W0, lp.p_leaf)
        out["my_mincvar_bpoe"] = b
        L(f"   bPOE of my min-CVaR solution {b:.10f}")
    # perspective LP on my formulation (exact min bPOE)
    c2, A2, rlb2, rub2, lb2, ub2, ny = vlib.perspective(lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, lp.blk["Wt"], lp.p_leaf, lp.Wstar, lp.W0)
    r3 = vlib.highs_lp(c2, A2, rlb2, rub2, lb2, ub2, method="ipm")
    L(f"MY perspective LP (exact min bPOE): {r3['status']} obj {r3.get('obj')} time {r3['time']:.1f}s")
    out["my_persp_highs"] = r3.get("obj")
    # tie-break at the author's pt
    pt = dm["o1"]["tie"]["pt"]
    At = sp.vstack([lp.A, lp.tie_row(pt)]).tocsr()
    r4 = vlib.highs_lp(lp.c_util(), At, np.r_[lp.rlo, -np.inf], np.r_[lp.rhi, 0.0], lp.lb, lp.ub, method="ipm", sense_max=True)
    L(f"MY tie-break (bPOE <= {pt:.6f}): {r4['status']} obj {r4.get('obj')} time {r4['time']:.1f}s (author {-caps[3]['rec']['obj']})")
    out["my_tie_highs"] = r4.get("obj")
    if "x" in r4:
        np.save(os.path.join(OUT, "my_full_tie_x.npy"), r4["x"])
        xm = r4["x"]
        b = lp.blk
        root = {"sell": xm[b["s"][0]], "redeem": xm[b["r"][0]], "add": xm[b["a"][0]], "tpl": xm[b["y"][0]], "beta": xm[b["beta"][0]],
                "trs": xm[b["trs"][0]], "hed": xm[b["hed"][0]], "opp": xm[b["opp"][0]], "fin": xm[b["B"][0]], "pi": xm[b["pi"][0]]}
        xa = caps[3]["x"]
        roota = {"sell": xa[bl["s"][0]], "redeem": xa[bl["r"][0]], "add": xa[bl["a"][0]], "tpl": xa[bl["y"][0]], "beta": xa[bl["beta"][0]],
                 "trs": xa[bl["trs"][0]], "hed": xa[bl["hed"][0]], "opp": xa[bl["opp"][0]], "fin": xa[bl["B"][0]], "pi": xa[bl["pi"][0]]}
        V0 = D["V"][0]
        diffs = {}
        for k in root:
            dd = np.atleast_1d(root[k]) - np.atleast_1d(roota[k])
            if k in ("sell", "redeem", "add"):
                dd = dd * V0
            diffs[k] = float(np.max(np.abs(dd)))
        out["root_decision_maxdiff_bn"] = diffs
        L("root decision max |mine - author| ($bn): " + json.dumps(diffs))
        Wt_m, Wt_a = xm[b["Wt"]], xa[bl["Wt"]]
        out["leaf_Wt_maxdiff"] = float(np.max(np.abs(Wt_m - Wt_a)))
        L(f"leaf W~ max |mine - author| {out['leaf_Wt_maxdiff']:.3e} $bn; P(goal) mine {lp.p_leaf[Wt_m >= lp.Wstar*(1-1e-9)].sum():.6f} author {lp.p_leaf[Wt_a >= lp.Wstar*(1-1e-9)].sum():.6f}")
    json.dump(out, open(os.path.join(OUT, "my_full.json"), "w"), indent=1, default=float)
    # ---------------- Clarabel (second solver) on my mean LP at full scale
    rc = vlib.clarabel_lp(lp.c_mean(), lp.A, lp.rlo, lp.rhi, lp.lb, lp.ub, sense_max=True, tol=1e-8, max_iter=300)
    L(f"MY mean LP (Clarabel): {rc['status']} obj {rc['obj']} iters {rc['iters']} time {rc['time']:.1f}s")
    out["my_mean_clarabel"] = rc["obj"]
    out["my_mean_clarabel_status"] = rc["status"]
    json.dump(out, open(os.path.join(OUT, "my_full.json"), "w"), indent=1, default=float)
    rc2 = vlib.clarabel_lp(lp.c_util(), At, np.r_[lp.rlo, -np.inf], np.r_[lp.rhi, 0.0], lp.lb, lp.ub, sense_max=True, tol=1e-8, max_iter=300)
    L(f"MY tie-break (Clarabel): {rc2['status']} obj {rc2['obj']} iters {rc2['iters']} time {rc2['time']:.1f}s")
    out["my_tie_clarabel"] = rc2["obj"]
    out["my_tie_clarabel_status"] = rc2["status"]
    json.dump(out, open(os.path.join(OUT, "my_full.json"), "w"), indent=1, default=float)
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
