"""SYNTHETIC - NOT ADIC DATA. Final full-scale checks: second solver (Clarabel, scaled objective) on the tie-break;
O1 against limits the model does not implement (H8 oil, H12 concentration); TRS cap where it is not imposed; fan-year
sleeve sales (H16 allowance, red-sleeve sales at the threshold) and how much of the in-tree result rests on them."""
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

logf = open(os.path.join(OUT, "final_full.log"), "w", encoding="utf-8", buffering=1)
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
    lp = MyLP(D, pj, dm["b0"], "OPT")
    v1 = lp.from_author(x1, bl)
    b = lp.blk
    T, ND = lp.T, lp.ND
    lvl, cls = lp.lvl, lp.cls
    V = lp.V
    # ---------------- O1 stats
    W = v1[b["W"]]
    hold = np.zeros((T, lp.I))
    for n in range(T):
        if n < ND:
            hold[n] = v1[b["x"][n]]
        else:
            a = lp.a2[n]
            hold[n] = v1[b["x"][a]] - v1[b["cq"][n]][lp.sl]
    val = hold * V
    units = D["units"]
    enr = np.array(["enr" in u["flags"] for u in units])
    gcc = np.array(["gcc" in u["flags"] for u in units])
    co = lp.group == "CO"
    sh_enr = val[:, enr].sum(1) / W
    sh_gcc = val[:, gcc].sum(1) / W
    sh_co = (val[:, co] / W[:, None]).max(1)
    res["H8_H12"] = {"ENR_share_max": float(sh_enr.max()), "ENR_nodes_above_1.5pct": int((sh_enr > 0.015).sum()),
                     "ENR_prob_mass_above": float(lp.prob[sh_enr > 0.015].sum()), "ENR_share_t0": float(sh_enr[0]),
                     "GCC_share_max": float(sh_gcc.max()), "GCC_nodes_above_1pct": int((sh_gcc > 0.01).sum()),
                     "max_single_coinvest_share": float(sh_co.max()), "coinvest_nodes_above_4pct": int((sh_co > 0.04).sum())}
    # B0 for reference
    x0 = dm["x0"]
    lp0 = MyLP(D, pj, {}, "B0")
    v0 = lp0.from_author(x0, dm["m0_blocks"])
    W0n = v0[b["W"]]
    hold0 = np.zeros((T, lp.I))
    for n in range(T):
        hold0[n] = v0[b["x"][n]] if n < ND else v0[b["x"][lp.a2[n]]] - v0[b["cq"][n]][lp.sl]
    sh_enr0 = (hold0 * V)[:, enr].sum(1) / W0n
    res["H8_H12"]["B0_ENR_share_max"] = float(sh_enr0.max())
    res["H8_H12"]["B0_ENR_nodes_above_1.5pct"] = int((sh_enr0 > 0.015).sum())
    L("H8/H12 (not implemented) on O1: " + json.dumps(res["H8_H12"], default=float))
    res["root_revolver_drawn"] = float(v1[b["B"][0, 0]])
    L(f"root revolver balance in O1 (H4 omits it): {res['root_revolver_drawn']}")
    # TRS cap where not imposed (stage-2 nodes and fans): TRS <= 0.5 x HF lot value
    hfu = lp.hf_units
    worst = 0.0
    cnt = 0
    for n in range(T):
        if n < ND and not (lvl[n] == 2):
            continue
        dn = lp.dec[n]
        trs = v1[b["trs"][dn]]
        cap = 0.5 * V[n, hfu] * hold[n, hfu]
        ex = trs - cap
        worst = max(worst, float(ex.max()))
        cnt += int((ex > 1e-7).sum())
    res["TRS_cap_unimposed"] = {"max_excess_bn": worst, "node_lot_pairs_above": cnt}
    L(f"TRS cap at stage-2 / fan nodes (not imposed): max excess {worst:.4f} $bn, pairs above {cnt}")
    # fan sleeve sales and the need row
    q = v1[b["q"]]
    fan = lvl >= 3
    res["fan_sales"] = {"q_by_sleeve_fans_prob_weighted_bn": (lp.prob[fan] @ (q[fan] * lp.bid_sl[fan])).tolist(),
                        "q_by_sleeve_decision_prob_weighted_bn": (lp.prob[~fan] @ (q[~fan] * lp.bid_sl[~fan])).tolist()}
    ax = lp.A @ v1
    nr = np.array(lp.rid["need"])
    nl = np.array([lp.tags[r][1] for r in nr])
    bind = np.abs(ax[nr] - lp.rhi[nr]) <= 1e-7 * np.maximum(1, np.abs(lp.rhi[nr]))
    res["need_binding_by_level"] = {int(L_): int(bind[lvl[nl] == L_].sum()) for L_ in range(6)}
    RS = v1[b["RS"]]
    at = np.abs(RS - pj("constraints.red_sale_threshold")) < 1e-9
    red_s = np.zeros(T)
    for n in range(ND):
        evt = lp.red & ((not lp.green[n]) | (lp.proc[n] / np.maximum(lp.proc_norm[n], 1e-12) < pj("constraints.red_bid_ratio")))
        red_s[n] = float((v1[b["s"][n]] * lp.proc[n] * evt).sum())
    res["red_at_threshold_by_level"] = {int(L_): int(at[lvl == L_].sum()) for L_ in range(6)}
    res["red_at_threshold_source"] = {"planned_sales_nodes": int((at & (red_s > 1e-9)).sum()),
                                      "red_sleeve_funding_nodes": int((at & (q[:, 3] > 1e-9)).sum())}
    L("fan sales: " + json.dumps({k: res[k] for k in ("fan_sales", "need_binding_by_level", "red_at_threshold_by_level", "red_at_threshold_source")}, default=float))
    # ---------------- how much rests on fan-year funding sales: GBO variants on my LP
    var = {}
    for nm in ("as run", "no red-sleeve sales in fans", "fan sleeve sales capped at outflows (no 8% W allowance)"):
        A, rlo, rhi, lb, ub = lp.A, lp.rlo.copy(), lp.rhi.copy(), lp.lb.copy(), lp.ub.copy()
        if nm == "no red-sleeve sales in fans":
            ub[b["q"][fan, 3]] = 0.0
        if nm.startswith("fan sleeve"):
            A = lp.A.tolil()
            for r in nr:
                n = lp.tags[r][1]
                if lvl[n] >= 3:
                    A[r, b["W"][n]] = 0.0
            A = A.tocsr()
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
                    ent["root_beta"] = float(rt["x"][b["beta"][0]])
                    ent["root_E_over_W"] = float(rt["x"][b["E"][0]] / rt["x"][b["W"][0]])
        var[nm] = ent
        L(f"variant [{nm}]: " + json.dumps(ent, default=float))
    res["fan_variants"] = var
    json.dump(res, open(os.path.join(OUT, "final_full.json"), "w"), indent=1, default=float)
    # ---------------- second solver at full scale on the tie-break, objective scaled x1000
    pt = dm["o1"]["tie"]["pt"]
    At = sp.vstack([lp.A, lp.tie_row(pt)]).tocsr()
    rc = vlib.clarabel_lp(lp.c_util() * 1000.0, At, np.r_[lp.rlo, -np.inf], np.r_[lp.rhi, 0.0], lp.lb, lp.ub, sense_max=True,
                          tol=1e-10, max_iter=1500)
    res["clarabel_tie_scaled"] = {"obj": rc["obj"] / 1000.0, "status": rc["status"], "iters": rc["iters"], "time": rc["time"],
                                  "author": dm["caps"][3]["rec"]["obj"]}
    xc = rc["x"]
    res["clarabel_tie_scaled"]["root_beta"] = float(xc[b["beta"][0]])
    res["clarabel_tie_scaled"]["author_root_beta"] = float(v1[b["beta"][0]])
    res["clarabel_tie_scaled"]["root_adds_maxdiff_bn"] = float(np.max(np.abs((xc[b["a"][0]] - v1[b["a"][0]]) * V[0])))
    res["clarabel_tie_scaled"]["root_redeem_maxdiff_bn"] = float(np.max(np.abs((xc[b["r"][0]] - v1[b["r"][0]]) * V[0])))
    res["clarabel_tie_scaled"]["root_commit_maxdiff_bn"] = float(np.max(np.abs(xc[b["y"][0]] - v1[b["y"][0]])))
    L("Clarabel tie-break (objective x1000, tol 1e-10): " + json.dumps(res["clarabel_tie_scaled"], default=float))
    json.dump(res, open(os.path.join(OUT, "final_full.json"), "w"), indent=1, default=float)
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
