"""Component 3b: the solve flow on the tree (SYNTHETIC - NOT ADIC DATA).

- b0_info: the status quo's exogenous node readings (event stage, behind, loss year, liquidity cushion, depth-guard
  reference distribution) used by G4, G5, H9 (ADR-39) and H10 (DSGO sections 1.1, 4.6-4.7).
- phase1: minimum hard-row violation over the soft-able rows; any residual is an allowance (STRUCTURAL_RECOVERY).
- gbo: the Goal-Buffered Objective (section 4.3): mean LP -> label STRETCH or PLAN -> bisection in PLAN ->
  mandatory CRRA(3) tie-break within the per-case tolerance.
- milp: exact max P(goal) with goal binaries only, big-M with L = 0, MIP start from GBO (section 4.4).
- crra: CRRA(3) + quadratic shortfall, the current design (section 4.5).
Every solve is logged with status and size.
"""
from __future__ import annotations

import time

import highspy
import numpy as np

from common import GROUPS, cvar_lower
from model import FIN, INF, MPOModel


# ---------------------------------------------------------------------------------------------- readings
def b0_info(m: MPOModel, x: np.ndarray) -> dict:
    D, P = m.D, m.P
    T, lvl, par, cls = m.T, m.lvl, m.par, m.cls
    W, LQ, M, NR = x[m.W], x[m.LQ], x[m.M], x[m.NR]
    d_year = D["tr"]["d_year"]
    b1, b2, b3 = P.get("constraints.stage_cash_bands")
    ratio = LQ / W
    cash_stage = np.where(ratio >= b1 - 1e-9, 0, np.where(ratio >= b2, 1, np.where(ratio >= b3 - 1e-9, 2, 3)))
    stage = np.maximum(cash_stage, cls)
    logtwr = np.zeros(T)
    loss = np.zeros(T, bool)
    for n in range(1, T):
        p = par[n]
        r = (W[n] + d_year[n] * NR[p]) / W[p]
        logtwr[n] = logtwr[p] + np.log(max(r, 1e-9))
        loss[n] = r < 1.0
    gap = logtwr - lvl * np.log(1 + P.get("goal.rate"))
    behind = gap < -P.get("constraints.behind_gap")
    Wt = x[m.WT]
    X = (D["Wstar"] - Wt) / D["W0"]
    lev = P.get("constraints.depth_levels")
    cvar_X = [-cvar_lower(-X, 1 - a, m.p_leaf) for a in lev]
    w_grp = {g: np.array([m.group_value(x, n, g) / W[n] for n in range(m.ND)]) for g in GROUPS}
    return {"W": W, "LQ": LQ, "M": M, "NR": NR, "stage": stage, "green": stage == 0, "black": stage == 3,
            "behind": behind, "loss": loss, "gap": gap, "cvar_X": cvar_X, "w_grp_b0": w_grp, "Wt": Wt,
            "lev_b0": x[m.EX] / W}


# ---------------------------------------------------------------------------------------------- statistics
def gbo_value(X: np.ndarray, p: np.ndarray, a_min: float) -> float:
    """Phi = min_{a >= a_min} E[(aX + 1)+], exact on a finite distribution (minimum at a breakpoint or a_min)."""
    cand = [a_min] + [-1.0 / xv for xv in X if xv < 0 and -1.0 / xv >= a_min]
    best = np.inf
    for a in cand:
        best = min(best, float(np.dot(p, np.maximum(a * X + 1.0, 0.0))))
    return best


def bpoe(X: np.ndarray, p: np.ndarray) -> float:
    return gbo_value(X, p, 0.0)


def tree_stats(m: MPOModel, x: np.ndarray) -> dict:
    D, P = m.D, m.P
    Wt = x[m.WT]
    p = m.p_leaf
    W0, Ws = D["W0"], D["Wstar"]
    X = (Ws - Wt) / W0
    yrs = P.get("goal.years")
    twr = np.maximum(Wt / W0, 1e-9) ** (1 / yrs) - 1
    cmax = P.get("goal.c_max_factor") * Ws / W0
    thr = P.get("constraints.red_sale_threshold")
    red = np.zeros(len(p), bool)
    for li, leaf in enumerate(m.leaves):
        path = D["anc"][leaf]
        red[li] = bool(np.any(x[m.M[path]] > 1e-6) or np.any(x[m.RS[path]] > thr))
    o = np.argsort(twr)
    cw = np.cumsum(p[o])
    med = float(twr[o][min(int(np.searchsorted(cw, 0.5)), len(o) - 1)])
    return {"p_goal": float(p[Wt >= Ws * (1 - 1e-9)].sum()), "E_Wt_over_Wstar": float(np.dot(p, Wt) / Ws),
            "E_Wt_bn": float(np.dot(p, Wt)), "twr_mean": float(np.dot(p, twr)), "twr_median": med,
            "cvar10_twr": cvar_lower(twr, 0.10, p), "cvar5_twr": cvar_lower(twr, 0.05, p),
            "cvar1_twr": cvar_lower(twr, 0.01, p), "bpoe": bpoe(X, p), "phi": gbo_value(X, p, 1.0 / cmax),
            "p_red": float(p[red].sum()), "leaf_condition_ok": bool(Wt.max() <= Ws + cmax * W0),
            "pileup_mass": float(p[(Wt >= Ws) & (Wt < Ws + 0.01 * W0)].sum()),
            "deep_miss_mass": float(p[X > 0.2].sum()), "min_Wt_bn": float(Wt.min())}


# ---------------------------------------------------------------------------------------------- phase I
SLACKS = ("SL3", "SL4", "SL11", "SL15", "SL9")


def phase1(m: MPOModel, log) -> dict:
    c = np.zeros(m.nvar)
    idx = np.concatenate([np.atleast_1d(getattr(m, s)).ravel() for s in SLACKS])
    c[idx] = 1.0
    m.set_col_bounds(idx, 0.0, INF)
    m.set_cost(c)
    x, y, rec = m.run("Phase I (min hard-row violation)")
    if x is None:
        raise RuntimeError(f"Phase I failed: {rec['status']}")
    u = float(x[idx].sum())
    allow = {}
    slack_ub = {}
    for s in SLACKS:
        ii = np.atleast_1d(getattr(m, s)).ravel()
        v = x[ii]
        if v.sum() > 1e-7:
            allow[s] = {"total": float(v.sum()), "n_rows": int((v > 1e-7).sum())}
        slack_ub[s] = np.where(v > 1e-7, v * (1 + 1e-6) + 1e-7, 0.0)
        m.set_col_bounds(ii, 0.0, slack_ub[s])
    label = "STRUCTURAL_RECOVERY" if u > 1e-6 else "FEASIBLE"
    log(f"Phase I: u* = {u:.6f} -> {label} {allow}")
    return {"u_star": u, "label": label, "allowances": allow, "slack_ub": slack_ub}


# ---------------------------------------------------------------------------------------------- GBO
def gbo(m: MPOModel, log, tag="GBO", certify: bool = True) -> dict:
    P, D = m.P, m.D
    W0, Ws = D["W0"], D["Wstar"]
    cmax = P.get("goal.c_max_factor") * Ws / W0
    m.set_row_bounds(m.rows["meanrow"], -INF, INF)
    m.set_row_bounds(m.rows["cvarrow"], -INF, INF)
    m.set_cost(m.obj_mean())
    xm, ym, rec = m.run(f"{tag}: mean LP", sense_max=True)
    if xm is None:
        return {"status": rec["status"], "x": None}
    Estar = float(np.dot(m.p_leaf, xm[m.WT]))
    out = {"E_star": Estar, "x_mean": xm}
    if Estar <= Ws:
        out["label"] = "STRETCH"
        out["phi"] = 1.0 + (Ws - Estar) / W0 / cmax
        tol = P.get("objective.tiebreak_tol") * cmax * W0
        m.set_row_bounds(m.rows["meanrow"], Estar - tol, INF)
        out["tie_tol_bn"] = tol
        out["tie"] = {"label": "STRETCH", "lo": Estar - tol}
    else:
        # PLAN: minimize bPOE. Fixed-point form of the bisection (same optimum, fewer LPs): p_{k+1} =
        # bPOE(X(x_k)) with x_k = argmin_x CVaR_{1-p_k}(X(x)). CVaR_{1-p_k}(X(x_k)) <= 0, so p_{k+1} <= p_k: the
        # sequence decreases to p*. A certificate LP at p* - tol must have min CVaR > 0 (else continue).
        out["label"] = "PLAN"
        tolb = P.get("objective.bisection_tol")
        h = m.highs()
        c = np.zeros(m.nvar)
        X = lambda xx: (Ws - xx[m.WT]) / W0
        pk = bpoe(X(xm), m.p_leaf)
        hist = [pk]
        it = 0
        best_x = xm
        while it < 12:
            it += 1
            c[:] = 0.0
            c[m.ETA_B] = 1.0
            c[m.UB] = m.p_leaf / pk
            m.set_cost(c)
            xb, _, r = m.run(f"{tag}: min CVaR at p={pk:.4f}")
            if xb is None:
                break
            pn = bpoe(X(xb), m.p_leaf)
            best_x = xb if pn <= pk else best_x
            hist.append(pn)
            if pk - pn < tolb and not certify:
                pk = min(pk, pn)
                break
            if pk - pn < tolb:
                pt = max(pn - tolb, 1e-6)       # certificate: no plan reaches bPOE pn - tol
                c[m.UB] = m.p_leaf / pt
                m.set_cost(c)
                xc, _, rc = m.run(f"{tag}: certificate p={pt:.4f}")
                if xc is not None and rc["obj"] <= 1e-9:
                    pk = bpoe(X(xc), m.p_leaf)
                    hist.append(pk)
                    best_x = xc
                    continue
                pk = min(pk, pn)
                break
            pk = pn
        best_p = pk
        out["phi"] = best_p
        out["phi_history"] = hist
        pt = min(best_p + P.get("objective.tiebreak_tol"), 1.0)
        h.changeCoeff(int(m.rows["cvarrow"]), int(m.ETA_B[0]), float(pt))
        m.set_row_bounds(m.rows["cvarrow"], -INF, 0.0)
        out["tie"] = {"label": "PLAN", "pt": pt}
    m.set_cost(m.obj_util())
    x, y, rec = m.run(f"{tag}: CRRA(3) tie-break", sense_max=True)
    out["rc"] = m.last_rc
    if x is None:          # tie-break failed: fall back to the goal-value solution
        log(f"  tie-break status {rec['status']}; using the goal-value LP solution")
        x, y = xm, ym
        out["rc"] = None
    m.set_row_bounds(m.rows["meanrow"], -INF, INF)
    m.set_row_bounds(m.rows["cvarrow"], -INF, INF)
    out.update({"x": x, "y": y, "status": rec["status"]})
    return out


def apply_tie(m: MPOModel, tie: dict | None):
    """Re-impose GBO's tie-break constraint (goal value held within its tolerance)."""
    if not tie:
        return
    if tie["label"] == "STRETCH":
        m.set_row_bounds(m.rows["meanrow"], tie["lo"], INF)
    else:
        m.highs().changeCoeff(int(m.rows["cvarrow"]), int(m.ETA_B[0]), float(tie["pt"]))
        m.set_row_bounds(m.rows["cvarrow"], -INF, 0.0)


def clear_tie(m: MPOModel):
    m.set_row_bounds(m.rows["meanrow"], -INF, INF)
    m.set_row_bounds(m.rows["cvarrow"], -INF, INF)


def crra(m: MPOModel, log, tag="CRRA+L2") -> dict:
    m.set_row_bounds(m.rows["meanrow"], -INF, INF)
    m.set_row_bounds(m.rows["cvarrow"], -INF, INF)
    m.set_cost(m.obj_util(lam_l2=m.P.get("objective.lambda_T")))
    x, y, rec = m.run(f"{tag}: CRRA(3) - lambda_T x squared shortfall", sense_max=True)
    return {"x": x, "y": y, "status": rec["status"]}


# ---------------------------------------------------------------------------------------------- MILP
def milp(m: MPOModel, log, start_x: np.ndarray, time_limit: float, node_limit: int, tag="MILP",
         heuristics: bool = True) -> dict:
    """Separate HiGHS instance: the same rows and current bounds + goal binaries g_l with
    W~_l - W* >= eps_g W0 - M_l (1 - g_l), M_l = W* + eps_g W0 - L_l, L_l = 0."""
    P, D = m.P, m.D
    W0, Ws = D["W0"], D["Wstar"]
    eps_g = P.get("goal.eps_g")
    L = len(m.leaves)
    A = m.A_mat.tocsc()
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", int(P.get("solver.threads")))
    h.setOptionValue("mip_rel_gap", float(P.get("objective.milp_gap")))
    h.setOptionValue("time_limit", float(time_limit))
    h.setOptionValue("mip_max_nodes", int(node_limit))
    h.setOptionValue("random_seed", 0)
    h.setOptionValue("primal_feasibility_tolerance", float(P.get("solver.feas_tol")))
    h.setOptionValue("mip_lp_solver", "ipm")              # the simplex root solve never finishes at this size
    if heuristics:
        h.setOptionValue("mip_heuristic_effort", float(P.get("objective.milp_heuristic_effort")))
    else:
        h.setOptionValue("mip_heuristic_run_rins", False)
        h.setOptionValue("mip_heuristic_run_rens", False)
        h.setOptionValue("mip_heuristic_run_feasibility_jump", False)
    lp = highspy.HighsLp()
    nv = m.nvar + L
    lp.num_col_ = nv
    cost = np.zeros(nv)
    cost[m.nvar:] = -m.p_leaf
    lp.col_cost_ = cost
    lp.col_lower_ = np.r_[m._cur_lb, np.zeros(L)]
    lp.col_upper_ = np.r_[m._cur_ub, np.ones(L)]
    Mbig = Ws + eps_g * W0 - 0.0
    rows_i = np.r_[np.arange(L), np.arange(L)]
    cols_i = np.r_[m.WT, m.nvar + np.arange(L)]
    vals = np.r_[np.ones(L), -Mbig * np.ones(L)]
    import scipy.sparse as sp
    G = sp.csr_matrix((vals, (rows_i, cols_i)), shape=(L, nv))
    Afull = sp.vstack([sp.hstack([A, sp.csc_matrix((m.nrow, L))]), G]).tocsc()
    lp.num_row_ = m.nrow + L
    lp.row_lower_ = np.r_[m._cur_rlb, np.full(L, Ws + eps_g * W0 - Mbig)]
    lp.row_upper_ = np.r_[m._cur_rub, np.full(L, INF)]
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = Afull.indptr
    lp.a_matrix_.index_ = Afull.indices
    lp.a_matrix_.value_ = Afull.data
    lp.integrality_ = [highspy.HighsVarType.kContinuous] * m.nvar + [highspy.HighsVarType.kInteger] * L
    h.passModel(lp)
    g0 = (start_x[m.WT] >= Ws + eps_g * W0).astype(float)
    sol = highspy.HighsSolution()
    sol.col_value = list(np.r_[start_x, g0])
    sol.value_valid = True
    h.setSolution(sol)
    t0 = time.time()
    h.run()
    dt = time.time() - t0
    st = h.getModelStatus()
    info = h.getInfo()
    status = h.modelStatusToString(st)
    x = np.array(h.getSolution().col_value) if info.primal_solution_status >= 2 else None
    rec = {"name": f"{tag}: max P(goal)", "kind": "MIP", "status": status, "cols": int(nv), "rows": int(m.nrow + L),
           "nnz": int(Afull.nnz), "ints": int(L), "time_s": dt, "mip_gap": float(info.mip_gap),
           "mip_nodes": int(info.mip_node_count), "obj": (-info.objective_function_value if x is not None else None),
           "dual_bound": float(-info.mip_dual_bound), "start_p_goal": float(np.dot(m.p_leaf, g0)),
           "time_limited": status == "Time limit reached", "node_limit": int(node_limit), "heuristics": heuristics}
    m.solves.append(rec)
    if hasattr(log, "solve"):
        log.solve(rec)
    gfree = None
    if x is not None:
        gfree = int(L)
        x = x[:m.nvar]
    return {"x": x, "rec": rec, "free_binaries": gfree}


def milp_round(m: MPOModel, log, start_x: np.ndarray, tag="MILP-R") -> dict:
    """Deterministic comparison for max P(goal) when the exact MILP cannot close in the budget.
    1. Relaxation: the MILP with g_l in [0, 1] continuous (same big-M rows, M = W* + eps_g W0, L = 0), solved by IPM:
       a valid UPPER bound on max P(goal) in the tree.
    2. Rounding: success sets S_tau = {l: g_l >= tau} united with the start's successes, tau = 0.5, 0.75, 0.9, 0.99
       (largest set first); fix g = 1 on S_tau (rows force W~_l >= W* + eps_g W0 there) and maximize CRRA(3) as
       the tie-break; the first feasible set gives the incumbent. Every LP is reported."""
    P, D = m.P, m.D
    W0, Ws = D["W0"], D["Wstar"]
    eps_g = P.get("goal.eps_g")
    L = len(m.leaves)
    import scipy.sparse as sp
    A = m.A_mat.tocsc()
    nv = m.nvar + L
    Mbig = Ws + eps_g * W0
    G = sp.csr_matrix((np.r_[np.ones(L), -Mbig * np.ones(L)],
                       (np.r_[np.arange(L), np.arange(L)], np.r_[m.WT, m.nvar + np.arange(L)])), shape=(L, nv))
    Af = sp.vstack([sp.hstack([A, sp.csc_matrix((m.nrow, L))]), G]).tocsc()
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", int(P.get("solver.threads")))
    h.setOptionValue("random_seed", 0)
    h.setOptionValue("solver", "ipm")
    h.setOptionValue("run_crossover", "on")
    lp = highspy.HighsLp()
    lp.num_col_ = nv
    lp.num_row_ = m.nrow + L
    cost = np.zeros(nv)
    cost[m.nvar:] = -m.p_leaf
    lp.col_cost_ = cost
    lo = np.r_[m._cur_lb, np.zeros(L)]
    hi = np.r_[m._cur_ub, np.ones(L)]
    lp.col_lower_ = lo
    lp.col_upper_ = hi
    lp.row_lower_ = np.r_[m._cur_rlb, np.full(L, Ws + eps_g * W0 - Mbig)]
    lp.row_upper_ = np.r_[m._cur_rub, np.full(L, INF)]
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = Af.indptr
    lp.a_matrix_.index_ = Af.indices
    lp.a_matrix_.value_ = Af.data
    h.passModel(lp)
    recs = []

    def run(name):
        t0 = time.time()
        h.run()
        st = h.getModelStatus()
        ok = st == highspy.HighsModelStatus.kOptimal
        rec = {"name": f"{tag}: {name}", "kind": "LP", "status": h.modelStatusToString(st), "cols": int(nv),
               "rows": int(m.nrow + L), "nnz": int(Af.nnz), "time_s": time.time() - t0,
               "obj": float(h.getInfo().objective_function_value) if ok else None}
        recs.append(rec)
        m.solves.append(rec)
        if hasattr(log, "solve"):
            log.solve(rec)
        return (np.array(h.getSolution().col_value) if ok else None), rec

    xr, rr = run("MILP relaxation (g continuous): upper bound on max P(goal)")
    ub = -rr["obj"] if xr is not None else np.nan
    best_x = start_x
    Wt0 = start_x[m.WT]
    best_p = float(m.p_leaf[Wt0 >= Ws * (1 - 1e-9)].sum())
    start_p = best_p
    S0 = Wt0 >= Ws + eps_g * W0 - 1e-9
    tried = []
    if xr is not None:
        g = xr[m.nvar:]
        gam, defl, Uf = m.crra
        c2 = np.zeros(nv)
        c2[m.UTIL] = -m.p_leaf
        h.changeColsCost(nv, np.arange(nv, dtype=np.int32), c2)
        idx = (m.nvar + np.arange(L)).astype(np.int32)
        taus = (0.5, 0.75, 0.9, 0.99)
        last_bad, feas_tau = None, None

        def attempt(S, label):
            nonlocal best_p, best_x
            h.changeColsBounds(L, idx, np.where(S, 1.0, 0.0), np.where(S, 1.0, 0.0))
            xs, rs = run(f"rounding {label}: fix {int(S.sum())} successes (P >= {float(m.p_leaf[S].sum()):.4f})")
            if xs is not None:
                Wt = xs[m.WT]
                pg = float(m.p_leaf[Wt >= Ws * (1 - 1e-9)].sum())
                if pg > best_p:
                    best_p, best_x = pg, xs[:m.nvar]
            return xs is not None, rs["status"]

        for tau in taus:
            S = (g >= tau) | S0
            pS = float(m.p_leaf[S].sum())
            if pS <= best_p + 1e-9:
                tried.append({"tau": tau, "p_set": pS, "status": "skipped (no gain)"})
                continue
            ok, stt = attempt(S, f"tau={tau}")
            tried.append({"tau": tau, "p_set": pS, "status": stt})
            if ok:
                feas_tau = tau
                break
            last_bad = tau
        # bisection on the relaxation's ranking between the last infeasible and the first feasible threshold
        if last_bad is not None:
            base = ((g >= feas_tau) | S0) if feas_tau is not None else S0.copy()
            cand = [l for l in np.argsort(-g, kind="stable") if (g[l] >= last_bad) and not base[l]]
            lo_k, hi_k = 0, len(cand)
            for _ in range(3):
                if hi_k - lo_k <= 1:
                    break
                mid = (lo_k + hi_k) // 2
                S = base.copy()
                S[cand[:mid]] = True
                ok, stt = attempt(S, f"bisection +{mid} leaves")
                tried.append({"tau": f"bisection +{mid}", "p_set": float(m.p_leaf[S].sum()), "status": stt})
                if ok:
                    lo_k = mid
                else:
                    hi_k = mid
    rec = {"name": f"{tag}: max P(goal) (relaxation bound + LP rounding)", "kind": "MIP-R", "status":
           ("Improved" if best_p > start_p + 1e-12 else "Start kept"), "cols": int(nv), "rows": int(m.nrow + L),
           "nnz": int(Af.nnz), "ints": int(L), "time_s": float(sum(r["time_s"] for r in recs)),
           "mip_gap": float((ub - best_p) / max(best_p, 1e-9)) if np.isfinite(ub) else np.nan, "mip_nodes": 0,
           "obj": best_p, "dual_bound": ub, "start_p_goal": start_p, "rounding": tried}
    return {"x": best_x, "rec": rec}


# ---------------------------------------------------------------------------------------------- families
def family_cols(m: MPOModel) -> dict:
    """Column sets each switch-off fixes (DSGO section 6.3)."""
    D = m.D
    names = D["tpl_names"]
    pur = [names.index(k) for k in ("SEC_BUY", "CO_DEAL", "CS_NEW", "PC_NEW")]
    lev = [names.index(k) for k in ("INFRA_LEV", "SMA_LEV")]
    com = [k for k, nm in enumerate(names) if nm.startswith("COMMIT_")]
    fin_ref = [FIN.index(k) for k in ("NAVF", "PREF", "CSBL", "SMABL", "RACO")]
    return {"SELL": {"zero": [m.S.ravel()]},
            "ADD": {"zero": [m.A.ravel(), m.Y[:, pur].ravel()]},
            "REFINANCE": {"zero": [m.DR[:, fin_ref].ravel(), m.PU]},
            "BETA": {"fix_beta": True},
            "LEVER": {"zero": [m.TRS.ravel(), m.Y[:, lev].ravel()]},
            "PACE": {"plan": com},
            "REDEEM": {"zero": [m.R.ravel()]},
            "HEDGE": {"hedge": True},
            "FUND": {"zero": [m.DR[:, [0, 1]].ravel(), m.LUP]},
            "REBALANCE": {"rebal": True}}


class SwitchOff:
    """Context manager: apply a family switch-off on the live HiGHS model, restore afterwards."""

    def __init__(self, m: MPOModel, fam: str):
        self.m, self.fam = m, fam
        self.spec = family_cols(m)[fam]

    def __enter__(self):
        m, s = self.m, self.spec
        self.saved_cols = []
        self.saved_rows = []
        self.saved_coef = []
        P = m.P
        if "zero" in s:
            for idx in s["zero"]:
                idx = np.atleast_1d(idx)
                self.saved_cols.append((idx, m._cur_lb[idx].copy(), m._cur_ub[idx].copy()))
                m.set_col_bounds(idx, 0.0, 0.0)
        if s.get("fix_beta"):
            idx = m.BETA[:m.ND]
            self.saved_cols.append((idx, m._cur_lb[idx].copy(), m._cur_ub[idx].copy()))
            v = P.get("overlay.beta_sq")
            m.set_col_bounds(idx, v, v)
        if "plan" in s:
            plan = np.array([t.get("plan", 0.0) for t in m.D["tpl"]])
            for k in s["plan"]:
                idx = m.Y[:, k]
                self.saved_cols.append((idx, m._cur_lb[idx].copy(), m._cur_ub[idx].copy()))
                m.set_col_bounds(idx, plan[k], plan[k])
        if s.get("hedge"):
            idx = m.OPP
            self.saved_cols.append((idx, m._cur_lb[idx].copy(), m._cur_ub[idx].copy()))
            v = P.get("overlay.opp_im_sq")
            m.set_col_bounds(idx, v, v)
            hmin = P.get("overlay.tail_budget")[0] / P.get("overlay.tail_premium")
            hmax = P.get("overlay.tail_budget")[1] / P.get("overlay.tail_premium")
            h = m.highs()
            for n, r in m.rows["hedhi"].items():
                h.changeCoeff(int(r), int(m.W[n]), float(-hmin))
                self.saved_coef.append((int(r), int(m.W[n]), float(-hmax)))
        if s.get("rebal"):
            for (r1, r2) in m.rows["rebal"]:
                self.saved_rows.append((r1, m._cur_rlb[r1], m._cur_rub[r1]))
                self.saved_rows.append((r2, m._cur_rlb[r2], m._cur_rub[r2]))
                m.set_row_bounds(r1, -INF, 0.0)
                m.set_row_bounds(r2, 0.0, INF)
        return self

    def __exit__(self, *a):
        m = self.m
        for idx, lo, hi in self.saved_cols[::-1]:
            m.set_col_bounds(idx, lo, hi)
        for r, lo, hi in self.saved_rows:
            m.set_row_bounds(r, lo, hi)
        h = m.highs()
        for r, c, v in self.saved_coef:
            h.changeCoeff(r, c, v)
        return False


def set_eps_red(m: MPOModel, eps: float):
    h = m.highs()
    if eps >= 1.0:
        m.set_row_bounds(m.rows["H9"], -INF, INF)
    else:
        h.changeCoeff(int(m.rows["H9"]), int(m.ETA_R[0]), float(eps))
        m.set_row_bounds(m.rows["H9"], -INF, 0.0)


def set_delta(m: MPOModel, delta: float | None):
    lev = m.P.get("constraints.depth_levels")
    for k, a in enumerate(lev):
        r = m.rows["H10"][k]
        if delta is None:
            m.set_row_bounds(r, -INF, INF)
        else:
            m.set_row_bounds(r, -INF, (1 - a) * (m.b0["cvar_X"][k] + delta))
