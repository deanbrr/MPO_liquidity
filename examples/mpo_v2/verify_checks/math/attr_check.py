"""SYNTHETIC - NOT ADIC DATA. Verification step 5: switch-off attribution.
Part 1: what each author SwitchOff changes in the live model (columns, rows, coefficients), restoration, overlaps.
Part 2: every switch-off re-solved with MY independent restriction (DSGO 6.3) on MY LP, against results.json/run_log."""
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
logf = open(os.path.join(OUT, "attr_check.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


res = {}
try:
    from common import Params
    import world
    import optim
    from model import FAMILIES
    import vlib
    from my_lp import MyLP, PJ, GROUPS

    P = Params(os.path.join(SRC, "params.json"))
    w = world.build(P, log=None)
    m = world.reset_model(w)
    h = m.highs()

    def mat():
        lp = h.getLp()
        A = sp.csc_matrix((np.array(lp.a_matrix_.value_), np.array(lp.a_matrix_.index_), np.array(lp.a_matrix_.start_)),
                          shape=(lp.num_row_, lp.num_col_))
        return A

    base = {"lb": m._cur_lb.copy(), "ub": m._cur_ub.copy(), "rlb": m._cur_rlb.copy(), "rub": m._cur_rub.copy(), "A": mat()}
    inv = np.empty(m.nvar, dtype=object)
    for k, v in m.B.blocks.items():
        inv[np.asarray(v).ravel()] = k
    lvl_of_col = np.full(m.nvar, -1)
    for k, v in m.B.blocks.items():
        v = np.asarray(v)
        if v.ndim >= 1 and v.shape[0] in (m.ND, m.T) and k not in ("Wt", "z", "uu", "util", "sh", "v2", "ub", "sl15"):
            for n in range(v.shape[0]):
                lvl_of_col[np.asarray(v[n]).ravel()] = m.lvl[n]
    changed = {}
    for f in FAMILIES:
        c = optim.SwitchOff(m, f)
        c.__enter__()
        dlb = np.flatnonzero(m._cur_lb != base["lb"])
        dub = np.flatnonzero(m._cur_ub != base["ub"])
        drow = np.flatnonzero((m._cur_rlb != base["rlb"]) | (m._cur_rub != base["rub"]))
        dA = (mat() - base["A"]).tocoo()
        cols = np.union1d(dlb, dub)
        blocks = {}
        for j in cols:
            key = f"{inv[j]}@lvl{lvl_of_col[j]}"
            blocks[key] = blocks.get(key, 0) + 1
        rowtags = sorted({m.B.rtag[r][0] for r in drow})
        coef = sorted({(m.B.rtag[r][0], inv[cc]) for r, cc in zip(dA.row, dA.col)})
        # columns whose bound change is a no-op (already at that value)
        noop = int(np.sum((m._cur_lb[cols] == base["lb"][cols]) & (m._cur_ub[cols] == base["ub"][cols])))
        changed[f] = set(cols.tolist())
        res.setdefault("part1", {})[f] = {"cols_changed": int(len(cols)), "by_block_level": blocks, "rows_changed": int(len(drow)),
                                          "row_tags": rowtags, "coef_changes": int(dA.nnz), "coef_rows_cols": [list(map(str, x)) for x in coef]}
        c.__exit__()
        restored = bool(np.array_equal(m._cur_lb, base["lb"]) and np.array_equal(m._cur_ub, base["ub"]) and
                        np.array_equal(m._cur_rlb, base["rlb"]) and np.array_equal(m._cur_rub, base["rub"]) and
                        (mat() - base["A"]).nnz == 0)
        res["part1"][f]["restored_after_exit"] = restored
        L(f"P1 {f:10s} cols {len(cols):5d} {blocks} rows {len(drow)} {rowtags} coef {dA.nnz} {coef[:3]} restored {restored}")
    ov = {}
    fl = list(changed)
    for i in range(len(fl)):
        for j in range(i + 1, len(fl)):
            k = len(changed[fl[i]] & changed[fl[j]])
            if k:
                ov[f"{fl[i]}&{fl[j]}"] = k
    res["part1_overlaps_columns"] = ov
    L(f"P1 column overlaps between families: {ov}")
    # discretionary decision columns not covered by any family
    allc = set().union(*changed.values())
    dec_blocks = ["s", "a", "r", "y", "pu", "pd", "trs", "hed", "opp", "beta", "dr", "Lup"]
    uncovered = {}
    for k in dec_blocks:
        idx = np.asarray(m.B.blocks[k]).ravel()
        free = [j for j in idx if j not in allc and base["ub"][j] > base["lb"][j]]
        if free:
            lv = {}
            for j in free:
                lv[int(lvl_of_col[j])] = lv.get(int(lvl_of_col[j]), 0) + 1
            uncovered[k] = lv
    res["part1_uncovered_free_decision_cols"] = uncovered
    L(f"P1 free decision columns in no family (block: {{level: count}}): {uncovered}")
    # ------------------------------------------------------------------ part 2
    R = json.load(open(os.path.join(SRC, "results.json"), encoding="utf-8"))
    att = {a["family"]: a for a in R["attribution"]["switch_off"]}
    o1t = R["solutions"]["GBO"]["tree"]
    run_log = open(os.path.join(SRC, "run_log.txt"), encoding="utf-8").read()
    dm = pickle.load(open(os.path.join(OUT, "full_dump.pkl"), "rb"))
    pj = PJ(os.path.join(SRC, "params.json"))

    def gbo_mine(lp, extra_A=None, extra_lo=None, extra_hi=None, lb=None, ub=None, pt=None, stretch_tol=None, phase1=False):
        A = lp.A if extra_A is None else sp.vstack([lp.A, extra_A]).tocsr()
        rlo = lp.rlo if extra_A is None else np.r_[lp.rlo, extra_lo]
        rhi = lp.rhi if extra_A is None else np.r_[lp.rhi, extra_hi]
        lb = lp.lb if lb is None else lb
        ub = lp.ub if ub is None else ub
        out = {}
        rm = vlib.highs_lp(lp.c_mean(), A, rlo, rhi, lb, ub, method="ipm", sense_max=True)
        out["mean_status"] = rm["status"]
        if "x" not in rm:
            return out, None, (A, rlo, rhi, lb, ub)
        Es = rm["obj"]
        out["E_star"] = Es
        Ws, W0 = lp.Wstar, lp.W0
        if Es > Ws:
            out["label"] = "PLAN"
            c2, A2, rl2, rh2, lb2, ub2, ny = vlib.perspective(A, rlo, rhi, lb, ub, lp.blk["Wt"], lp.p_leaf, Ws, W0)
            rp = vlib.highs_lp(c2, A2, rl2, rh2, lb2, ub2, method="ipm")
            out["phi_exact"] = rp.get("obj")
            ptt = pt if pt is not None else rp["obj"] + 0.005
            At = sp.vstack([A, lp.tie_row(ptt)]).tocsr()
            rt = vlib.highs_lp(lp.c_util(), At, np.r_[rlo, -np.inf], np.r_[rhi, 0.0], lb, ub, method="ipm", sense_max=True)
        else:
            out["label"] = "STRETCH"
            cmax = pj("goal.c_max_factor") * Ws / W0
            out["phi_exact"] = 1.0 + (Ws - Es) / W0 / cmax
            tol = pj("objective.tiebreak_tol") * cmax * W0
            mrow = sp.csr_matrix((lp.p_leaf, (np.zeros(len(lp.p_leaf), int), lp.blk["Wt"])), shape=(1, lp.nv))
            At = sp.vstack([A, mrow]).tocsr()
            rt = vlib.highs_lp(lp.c_util(), At, np.r_[rlo, Es - tol], np.r_[rhi, np.inf], lb, ub, method="ipm", sense_max=True)
        out["tie_status"] = rt["status"]
        x = rt.get("x")
        if x is not None:
            Wt = x[lp.blk["Wt"]]
            out["tie_util"] = rt["obj"]
            out["p_goal"] = float(lp.p_leaf[Wt >= lp.Wstar * (1 - 1e-9)].sum())
            out["E_Wt"] = float(lp.p_leaf @ Wt)
        return out, x, (A, rlo, rhi, lb, ub)

    lp = MyLP(dm["D"], pj, dm["b0"], "OPT")
    b = lp.blk
    tn = lp.tnames
    pur = [tn.index(k) for k in ("SEC_BUY", "CO_DEAL", "CS_NEW", "PC_NEW")]
    levt = [tn.index(k) for k in ("INFRA_LEV", "SMA_LEV")]
    com = [k for k, nm in enumerate(tn) if nm.startswith("COMMIT_")]
    hmin = pj("overlay.tail_budget")[0] / pj("overlay.tail_premium")

    def grp_rows(n, g, wb, sign):
        gm = (lp.group == g).astype(float)
        terms = lp.hold(n, lp.V[n], gm) + lp.tstate(n, "V", kmask=(lp.tgroup == g))
        terms = terms + [(b["W"][n], -(wb + 0.01 * sign))]
        return terms

    def rows_from_terms(rowlist):
        rr, cc, vv, lo, hi = [], [], [], [], []
        for k, (terms, l_, h_) in enumerate(rowlist):
            for c_, v_ in terms:
                c_ = np.atleast_1d(np.asarray(c_)).ravel()
                v_ = np.broadcast_to(np.asarray(v_, float), c_.shape).ravel()
                rr.append(np.full(len(c_), k)); cc.append(c_); vv.append(v_)
            lo.append(l_); hi.append(h_)
        A = sp.csr_matrix((np.concatenate(vv), (np.concatenate(rr), np.concatenate(cc))), shape=(len(rowlist), lp.nv))
        return A, np.array(lo, float), np.array(hi, float)

    for f in FAMILIES + ["BELIEFS"]:
        a_ = att[f]
        lb, ub = lp.lb.copy(), lp.ub.copy()
        ex = None
        lpf = lp
        if f == "SELL":
            ub[b["s"]] = 0.0
        elif f == "ADD":
            ub[b["a"]] = 0.0
            ub[b["y"][:, pur]] = 0.0
        elif f == "REFINANCE":
            ub[b["dr"][:, 2:7]] = 0.0
            ub[b["pu"]] = 0.0
        elif f == "BETA":
            lb[b["beta"][:lp.ND]] = ub[b["beta"][:lp.ND]] = pj("overlay.beta_sq")
        elif f == "LEVER":
            ub[b["trs"]] = 0.0
            ub[b["y"][:, levt]] = 0.0
        elif f == "PACE":
            lb[b["y"][:, com]] = ub[b["y"][:, com]] = lp.plan[com]
        elif f == "REDEEM":
            ub[b["r"]] = 0.0
        elif f == "HEDGE":
            lb[b["opp"]] = ub[b["opp"]] = pj("overlay.opp_im_sq")
            rl = [([(b["hed"][t[1]], 1.0), (b["W"][t[1]], -hmin)], -np.inf, 0.0) for t in lp.tags if t[0] == "hedhi"]
            ex = rows_from_terms(rl)
        elif f == "FUND":
            ub[b["dr"][:, 0:2]] = 0.0
            ub[b["Lup"]] = 0.0
        elif f == "REBALANCE":
            wg = dm["b0"]["w_grp_b0"]
            rl = []
            for n in range(lp.ND):
                for g in GROUPS:
                    rl.append((grp_rows(n, g, wg[g][n], +1), -np.inf, 0.0))
                    rl.append((grp_rows(n, g, wg[g][n], -1), 0.0, np.inf))
            ex = rows_from_terms(rl)
        elif f == "BELIEFS":
            w2 = world.build(P, log=None, use_beliefs=False, phase1=False)
            lpf = MyLP({k: v for k, v in w2["D"].items() if k != "P"}, pj, w2["b0"], "OPT")
            lb, ub = lpf.lb.copy(), lpf.ub.copy()
        pt = (a_["phi"] + 0.005) if a_.get("phi") is not None and a_.get("label") == "PLAN" else None
        t0 = time.time()
        if ex is None:
            out, x, mats = gbo_mine(lpf, lb=lb, ub=ub, pt=pt)
        else:
            out, x, mats = gbo_mine(lpf, ex[0], ex[1], ex[2], lb=lb, ub=ub, pt=pt)
        if f == "PACE" and out.get("mean_status") != "Optimal":
            # Phase I on my rows: slacks on H3 (>=), H4 (>=), H11 (<=), H15 (<=), H9 (<=); min total violation
            A, rlo, rhi, lbb, ubb = mats
            tags = lpf.tags
            sl_rows = [(r, +1.0) for r, t in enumerate(tags) if t[0] in ("H3", "H4")] + \
                      [(r, -1.0) for r, t in enumerate(tags) if t[0] in ("H11", "H15", "H9")]
            ns = len(sl_rows)
            S = sp.csr_matrix(([s for _, s in sl_rows], ([r for r, _ in sl_rows], np.arange(ns))), shape=(A.shape[0], ns))
            Aph = sp.hstack([A, S]).tocsr()
            cph = np.r_[np.zeros(lpf.nv), np.ones(ns)]
            rph = vlib.highs_lp(cph, Aph, rlo, rhi, np.r_[lbb, np.zeros(ns)], np.r_[ubb, np.full(ns, np.inf)], method="ipm")
            sv = rph["x"][lpf.nv:]
            nzs = [(tags[sl_rows[k][0]], float(sv[k])) for k in np.flatnonzero(sv > 1e-7)]
            out["phase1_u_star"] = rph["obj"]
            out["phase1_rows"] = [(str(t), v) for t, v in nzs]
            # mean LP with the slacks capped at the Phase I values (as the author), then STRETCH tie-break
            ubs = np.where(sv > 1e-7, sv * (1 + 1e-6) + 1e-7, 0.0)
            rm = vlib.highs_lp(np.r_[lpf.c_mean(), np.zeros(ns)], Aph, rlo, rhi, np.r_[lbb, np.zeros(ns)], np.r_[ubb, ubs], method="ipm", sense_max=True)
            out["E_star_after_phase1"] = rm.get("obj")
        out["time_s"] = time.time() - t0
        # author's numbers
        import re
        mm = re.search(rf"solve OFF_{f}(?: \(after Phase I\))?: mean LP: LP status=Optimal .*? obj=([0-9.]+)", run_log)
        auth = {"label": a_.get("label"), "phi": a_.get("phi"), "E_star_runlog": float(mm.group(1)) if mm else None,
                "p_goal_tree": o1t["p_goal"] + a_["tree_dp_goal"], "E_Wt_tree": o1t["E_Wt_bn"] + a_["tree_dE_Wt_bn"],
                "phase1": a_.get("phase1")}
        res.setdefault("part2", {})[f] = {"mine": out, "author": auth}
        L(f"P2 {f:10s} mine {json.dumps(out, default=float)}")
        L(f"   {'':10s} author {json.dumps(auth, default=float)}")
    json.dump(res, open(os.path.join(OUT, "attr_check.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
