"""SYNTHETIC - NOT ADIC DATA. Verification helpers written for this check (independent of the author's code)."""
import time

import numpy as np
import scipy.sparse as sp

BIG = 1e20


def finite(v):
    return np.isfinite(v) & (np.abs(v) < 1e19)


# ------------------------------------------------------------------ distribution statistics (own code)
def cvar_upper(X, p, tail):
    """Mean of the worst (largest) `tail` probability mass of X (Rockafellar-Uryasev, exact on atoms)."""
    X = np.asarray(X, float)
    p = np.asarray(p, float) / np.sum(p)
    o = np.argsort(-X, kind="stable")
    xs, ps = X[o], p[o]
    cum = np.cumsum(ps)
    take = np.minimum(ps, np.maximum(tail - (cum - ps), 0.0))
    return float(np.dot(take, xs) / tail)


def cvar_upper_ru(X, p, tail):
    """Same quantity by the RU minimization over eta (scan of all atoms): min_eta eta + E[(X-eta)+]/tail."""
    X = np.asarray(X, float)
    p = np.asarray(p, float) / np.sum(p)
    best = np.inf
    for eta in np.unique(X):
        best = min(best, eta + float(np.dot(p, np.maximum(X - eta, 0.0))) / tail)
    return best


def bpoe0(X, p, a_min=0.0):
    """min_{a >= a_min} E[(aX+1)+] by exhaustive breakpoint enumeration (own implementation)."""
    X = np.asarray(X, float)
    p = np.asarray(p, float) / np.sum(p)
    cands = [a_min] + [-1.0 / v for v in X if v < 0 and -1.0 / v >= a_min]
    vals = [float(np.dot(p, np.maximum(a * X + 1.0, 0.0))) for a in cands]
    k = int(np.argmin(vals))
    return vals[k], cands[k]


def bpoe_by_cvar(X, p, tol=1e-12):
    """bPOE as the tail mass q at which CVaR_q(X) = 0 (bisection on q; CVaR_q decreasing in q)."""
    if np.dot(p, X) / np.sum(p) >= 0:
        return 1.0
    lo, hi = 1e-12, 1.0
    if cvar_upper(X, p, lo) <= 0:
        return 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if cvar_upper(X, p, mid) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


# ------------------------------------------------------------------ LP utilities
def row_report(A, x, rlb, rub, tags, skip=()):
    ax = A @ x
    out = {}
    for r in range(A.shape[0]):
        t = tags[r][0] if isinstance(tags[r], tuple) else tags[r]
        if t in skip:
            continue
        lo, hi = rlb[r], rub[r]
        v = 0.0
        if finite(np.array([lo]))[0]:
            v = max(v, lo - ax[r])
        if finite(np.array([hi]))[0]:
            v = max(v, ax[r] - hi)
        sl = np.inf
        if finite(np.array([lo]))[0]:
            sl = min(sl, ax[r] - lo)
        if finite(np.array([hi]))[0]:
            sl = min(sl, hi - ax[r])
        d = out.setdefault(t, {"rows": 0, "max_viol": 0.0, "binding": 0, "min_slack": np.inf, "worst": None})
        d["rows"] += 1
        if v > d["max_viol"]:
            d["max_viol"] = float(v)
            d["worst"] = tags[r]
        if np.isfinite(sl):
            d["min_slack"] = float(min(d["min_slack"], sl))
            if abs(sl) <= 1e-7 * max(1.0, abs(hi if finite(np.array([hi]))[0] else lo)):
                d["binding"] += 1
    return out


def highs_lp(c, A, rlb, rub, lb, ub, method="ipm", sense_max=False, integrality=None, time_limit=None,
             mip_gap=None, feas_tol=1e-7, start=None, threads=1):
    import highspy
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", threads)
    h.setOptionValue("random_seed", 0)
    h.setOptionValue("primal_feasibility_tolerance", feas_tol)
    h.setOptionValue("dual_feasibility_tolerance", feas_tol)
    if integrality is None:
        h.setOptionValue("solver", method)
        if method == "ipm":
            h.setOptionValue("run_crossover", "on")
    else:
        if mip_gap is not None:
            h.setOptionValue("mip_rel_gap", mip_gap)
        h.setOptionValue("mip_feasibility_tolerance", 1e-7)
    if time_limit is not None:
        h.setOptionValue("time_limit", float(time_limit))
    inf = highspy.kHighsInf
    conv = lambda v: np.where(finite(v), v, np.where(v > 0, inf, -inf)).astype(float)
    Ac = sp.csc_matrix(A)
    lp = highspy.HighsLp()
    lp.num_col_ = A.shape[1]
    lp.num_row_ = A.shape[0]
    lp.col_cost_ = (-c if sense_max else c).astype(float)
    lp.col_lower_ = conv(np.asarray(lb, float))
    lp.col_upper_ = conv(np.asarray(ub, float))
    lp.row_lower_ = conv(np.asarray(rlb, float))
    lp.row_upper_ = conv(np.asarray(rub, float))
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = Ac.indptr
    lp.a_matrix_.index_ = Ac.indices
    lp.a_matrix_.value_ = Ac.data
    if integrality is not None:
        lp.integrality_ = [highspy.HighsVarType.kInteger if f else highspy.HighsVarType.kContinuous for f in integrality]
    h.passModel(lp)
    if start is not None:
        sol = highspy.HighsSolution()
        sol.col_value = list(start)
        sol.value_valid = True
        h.setSolution(sol)
    t0 = time.time()
    h.run()
    dt = time.time() - t0
    st = h.getModelStatus()
    info = h.getInfo()
    out = {"status": h.modelStatusToString(st), "time": dt}
    ok = st == highspy.HighsModelStatus.kOptimal
    if integrality is not None:
        ok = info.primal_solution_status >= 2
        out["mip_gap"] = float(info.mip_gap)
        out["dual_bound"] = float(info.mip_dual_bound) * (-1 if sense_max else 1)
        out["nodes"] = int(info.mip_node_count)
    if ok:
        sol = h.getSolution()
        out["x"] = np.array(sol.col_value)
        if integrality is None:
            out["y"] = np.array(sol.row_dual)
        out["obj"] = float(info.objective_function_value) * (-1 if sense_max else 1)
    return out


def clarabel_lp(c, A, rlb, rub, lb, ub, sense_max=False, tol=1e-9, max_iter=400, verbose=False):
    """LP through Clarabel (interior point, conic): min c'x, rlb <= Ax <= rub, lb <= x <= ub."""
    import clarabel
    A = sp.csr_matrix(A)
    n = A.shape[1]
    rlb = np.asarray(rlb, float)
    rub = np.asarray(rub, float)
    lb = np.asarray(lb, float)
    ub = np.asarray(ub, float)
    fl, fu = finite(rlb), finite(rub)
    eq = fl & fu & (np.abs(rlb - rub) <= 0)
    blocks_eq, b_eq = [A[eq]], [rlb[eq]]
    I = sp.identity(n, format="csr")
    bl, bu = finite(lb), finite(ub)
    beq = bl & bu & (lb == ub)
    blocks_eq.append(I[beq])
    b_eq.append(lb[beq])
    ineq_hi = fu & ~eq
    ineq_lo = fl & ~eq
    bhi = bu & ~beq
    blo = bl & ~beq
    Aeq = sp.vstack(blocks_eq)
    beqv = np.concatenate(b_eq)
    Ain = sp.vstack([A[ineq_hi], -A[ineq_lo], I[bhi], -I[blo]])
    bin_ = np.concatenate([rub[ineq_hi], -rlb[ineq_lo], ub[bhi], -lb[blo]])
    Aall = sp.vstack([Aeq, Ain]).tocsc()
    ball = np.concatenate([beqv, bin_])
    cones = [clarabel.ZeroConeT(Aeq.shape[0]), clarabel.NonnegativeConeT(Ain.shape[0])]
    st = clarabel.DefaultSettings()
    st.verbose = verbose
    st.max_iter = max_iter
    st.tol_gap_abs = tol
    st.tol_gap_rel = tol
    st.tol_feas = tol
    st.tol_ktratio = 1e-7
    Pm = sp.csc_matrix((n, n))
    q = (-c if sense_max else c).astype(float)
    t0 = time.time()
    solver = clarabel.DefaultSolver(Pm, q, Aall, ball, cones, st)
    sol = solver.solve()
    dt = time.time() - t0
    out = {"status": str(sol.status), "time": dt, "iters": int(sol.iterations)}
    x = np.array(sol.x)
    out["x"] = x
    out["obj"] = float(c @ x)
    return out


def perspective(A, rlb, rub, lb, ub, wt_idx, p_leaf, Wstar, W0, a_min=0.0):
    """Charnes-Cooper / Mafusalov-Uryasev LP for min_{x feasible, a >= a_min} E[(a X(x) + 1)+], y = a x, tau = a.
    Returns (c, A2, rlb2, rub2, lb2, ub2, n_y)."""
    A = sp.csr_matrix(A)
    m, n = A.shape
    L = len(wt_idx)
    rlb = np.asarray(rlb, float)
    rub = np.asarray(rub, float)
    lb = np.asarray(lb, float)
    ub = np.asarray(ub, float)
    fl, fu = finite(rlb), finite(rub)
    rows, lo, hi = [], [], []
    tau_col = []
    # original rows: equality, >= and <= parts (both parts for ranged rows)
    eq = fl & fu & (rlb == rub)
    sel = np.flatnonzero(eq)
    rows.append(A[sel]); tau_col.append(-rlb[sel]); lo.append(np.zeros(len(sel))); hi.append(np.zeros(len(sel)))
    sel = np.flatnonzero(fl & ~eq)
    rows.append(A[sel]); tau_col.append(-rlb[sel]); lo.append(np.zeros(len(sel))); hi.append(np.full(len(sel), np.inf))
    sel = np.flatnonzero(fu & ~eq)
    rows.append(A[sel]); tau_col.append(-rub[sel]); lo.append(np.full(len(sel), -np.inf)); hi.append(np.zeros(len(sel)))
    # bounds: nonzero finite bounds become tau rows; zero bounds stay bounds
    I = sp.identity(n, format="csr")
    bl, bu = finite(lb), finite(ub)
    lb2 = np.where(bl & (lb == 0), 0.0, -np.inf)
    ub2 = np.where(bu & (ub == 0), 0.0, np.inf)
    sel = np.flatnonzero(bl & (lb != 0))
    rows.append(I[sel]); tau_col.append(-lb[sel]); lo.append(np.zeros(len(sel))); hi.append(np.full(len(sel), np.inf))
    sel = np.flatnonzero(bu & (ub != 0))
    rows.append(I[sel]); tau_col.append(-ub[sel]); lo.append(np.full(len(sel), -np.inf)); hi.append(np.zeros(len(sel)))
    # sign of y where the bound is nonzero but implies a sign
    lb2 = np.where(bl & (lb > 0), 0.0, lb2)
    ub2 = np.where(bu & (ub < 0), 0.0, ub2)
    Ay = sp.vstack(rows).tocsr()
    tcol = np.concatenate(tau_col)
    nr = Ay.shape[0]
    # hinge rows: z_l - (W*/W0) tau + y_WT_l / W0 >= 1
    Hy = sp.csr_matrix((np.full(L, 1.0 / W0), (np.arange(L), wt_idx)), shape=(L, n))
    top = sp.hstack([Ay, sp.csr_matrix(tcol.reshape(-1, 1)), sp.csr_matrix((nr, L))])
    bot = sp.hstack([Hy, sp.csr_matrix(np.full((L, 1), -Wstar / W0)), sp.identity(L, format="csr")])
    A2 = sp.vstack([top, bot]).tocsr()
    rlb2 = np.concatenate(lo + [np.ones(L)])
    rub2 = np.concatenate(hi + [np.full(L, np.inf)])
    lbv = np.concatenate([lb2, [a_min], np.zeros(L)])
    ubv = np.concatenate([ub2, [np.inf], np.full(L, np.inf)])
    c = np.concatenate([np.zeros(n), [0.0], np.asarray(p_leaf, float)])
    return c, A2, rlb2, rub2, lbv, ubv, n
