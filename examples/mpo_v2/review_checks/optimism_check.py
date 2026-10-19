"""SYNTHETIC optimism check for the DSGO spec review (not ADIC data).

Uses the milp_pilot tree (10 x 5 x 4 fans, 40 cohort assets, 5 factors, no idiosyncratic
risk in the tree). Takes the ROOT decision of (a) status quo, (b) the mean LP (GBO in
STRETCH) and (c) the goal MILP (short time limit, loose big-M, MIP start from the mean
LP), freezes it (buy-and-hold, draws from cash then pro-rata liquid sales then debt),
and evaluates the same rule on the tree's own 200 leaves and on 20,000 fresh paths:
  truth = belief (alphas as believed, no idiosyncratic noise)        -> tree-sampling optimism only
  truth != belief (alpha_true = alpha_hat + N(0, 1.5%), idio 5/12%) -> plus belief and idiosyncratic risk
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0]]
import milp_pilot as M

NP = 20000


def frozen_rule(h, c, d, R, idio=None, alpha_shift=None):
    """h (NA,), R (n, T, NA) arithmetic returns. Returns W~ per path (draws accrued at SQ return)."""
    n = R.shape[0]
    H = np.tile(h, (n, 1)); C = np.full(n, c); D = np.full(n, d)
    Hs = np.tile(M.h0, (n, 1)); Cs = np.full(n, M.c0)
    acc = np.zeros(n)
    for t in range(M.T):
        r = R[:, t, :].copy()
        if alpha_shift is not None:
            r = r + alpha_shift
        if idio is not None:
            r = r + idio[:, t, :]
        Ws_prev = Hs.sum(1) + Cs
        draw = M.DRAW * Ws_prev
        # SQ path (for the draw basis and the static accrual)
        Hs = Hs * (1 + r); Cs = Cs * (1 + M.RF) - draw
        neg = Cs < 0.04 * (Hs.sum(1) + Cs)
        need = np.where(neg, 0.04 * (Hs.sum(1) + Cs) - Cs, 0.0)
        liq = Hs[:, :M.NLIQ].sum(1)
        frac = np.minimum(1.0, need / np.maximum(liq, 1e-12))
        Hs[:, :M.NLIQ] *= (1 - frac)[:, None]; Cs = Cs + frac * liq * (1 - M.TC)
        Ws_now = Hs.sum(1) + Cs
        gross_sq = (Ws_now + draw) / Ws_prev
        acc = acc * gross_sq + draw
        # policy path
        H = H * (1 + r); C = C * (1 + M.RF) - draw; D = D * (1 + M.RD)
        W = H.sum(1) + C - D
        need = np.maximum(0.0, 0.04 * W - C)
        liq = H[:, :M.NLIQ].sum(1)
        frac = np.minimum(1.0, need / np.maximum(liq, 1e-12))
        sold = frac * liq
        H[:, :M.NLIQ] *= (1 - frac)[:, None]; C = C + sold * (1 - M.TC)
        short = np.maximum(0.0, 0.04 * (H.sum(1) + C - D) - C)
        C = C + short; D = D + short
    return H.sum(1) + C - D + acc


def tree_paths():
    """The tree's leaf paths as (NL, T, NA) returns with leaf probabilities."""
    R = np.zeros((M.NL, M.T, M.NA)); p = np.zeros(M.NL)
    for l, L in enumerate(M.leaves):
        n2 = L["node"]; n1 = M.nodes[n2]["parent"]
        R[l, 0] = M.nodes[n1]["r"]; R[l, 1] = M.nodes[n2]["r"]; R[l, 2:] = L["r"]
        p[l] = L["prob"]
    return R, p


def fresh_paths(seed):
    rng = np.random.default_rng(seed)
    f = M.mu_f + rng.standard_normal((NP, M.T, M.nf)) @ M.Lf.T
    R = M.RF + M.ALPHA + f @ M.B.T
    idio_sd = np.where(np.arange(M.NA) >= M.NLIQ, 0.12, 0.05)
    idio = rng.standard_normal((NP, M.T, M.NA)) * idio_sd
    shift = rng.normal(0.0, 0.015, M.NA)          # one truth draw: true alpha - believed alpha
    return R, idio, shift


def root_of(x):
    h = x[M.idx[("h", 0)]]; c = x[M.idx[("c", 0)]][0]; d = x[M.idx[("d", 0)]][0]
    return h, c, d


def main():
    t0 = time.time()
    # status quo LP (for the CVaR reference) and the mean LP, as in the pilot
    clo, cup = M.col_lo.copy(), M.col_up.copy()
    for n in range(M.NN):
        cup[M.idx[("b", n)]] = 0; cup[M.idx[("s", n)][M.NLIQ:]] = 0
    lo2, up2 = M.lo.copy(), M.up.copy()
    lo2[M.cvar_main], up2[M.cvar_main] = -np.inf, np.inf
    cup[M.Gb] = 0.0
    obj = np.zeros(M.NVAR)
    for n in range(M.NN):
        obj[M.idx[("d", n)]] = M.nodes[n]["prob"]; obj[M.idx[("s", n)][:M.NLIQ]] = 0.5 * M.nodes[n]["prob"]
    for l in range(M.NL):
        obj[M.idx[("dl", l)]] = M.p[l]; obj[M.idx[("ql", l)]] = 0.5 * M.p[l]
    rsq = M.solve(obj, M.A, lo2, up2, clo, cup)
    Wsq = M.leaf_values(rsq["x"]); Xsq = M.GOAL - Wsq
    order = np.argsort(-Xsq); cum = np.cumsum(M.p[order]); k = np.searchsorted(cum, 0.10)
    tail = order[:k + 1]; w = M.p[tail].copy(); w[-1] -= cum[k] - 0.10
    cvar_sq = np.sum(w * Xsq[tail]) / 0.10
    up = M.up.copy(); up[M.cvar_main] = cvar_sq + M.DELTA
    obj = np.zeros(M.NVAR)
    for l in range(M.NL):
        for j, v in M.leaf_coef[l][0].items():
            obj[j] += M.p[l] * v
    clo, cup = M.col_lo.copy(), M.col_up.copy(); cup[M.Gb] = 0.0
    rm = M.solve(obj, M.A, M.lo, up, clo, cup, sense_max=True)
    Wm = M.leaf_values(rm["x"])
    # goal MILP with loose valid big-M (L = -1), MIP start from the mean LP
    A2 = M.A.tolil(copy=True); lo3, up3 = M.lo.copy(), up.copy()
    Mbig = M.GOAL + M.EPS_G + 1.0
    for l in range(M.NL):
        A2[M.goal_rows[l], M.Gb[l]] = -Mbig
        lo3[M.goal_rows[l]] = M.GOAL + M.EPS_G - M.leaf_coef[l][1] - Mbig
        up3[M.goal_rows[l]] = np.inf
    clo3, cup3 = M.col_lo.copy(), M.col_up.copy()
    o = np.zeros(M.NVAR); o[M.Gb] = M.p
    start = rm["x"].copy(); start[M.Gb] = (Wm >= M.GOAL + M.EPS_G).astype(float)
    tl = 240.0
    rq = M.solve(o, A2.tocsr(), lo3, up3, clo3, cup3, integer=True, time_limit=tl, start=start, sense_max=True)
    Wq = M.leaf_values(rq["x"])
    print(f"solves done in {time.time() - t0:.0f}s; MILP {rq['status']} gap {rq['gap']:.3f}")
    print(f"in-tree (full contingent plan): P(goal) SQ {np.sum(M.p[Wsq >= M.GOAL]):.3f}  "
          f"meanLP {np.sum(M.p[Wm >= M.GOAL]):.3f}  MILP {np.sum(M.p[Wq >= M.GOAL]):.3f}")
    Rt, pt = tree_paths()
    Rf, idio, shift = fresh_paths(4242)
    pols = {"SQ": (M.h0, M.c0, 0.0), "meanLP": root_of(rm["x"]), "MILP": root_of(rq["x"])}
    print("root decision frozen (buy-and-hold + funding rule); P(goal) and E[W~]/W*:")
    base = {}
    for name, (h, c, d) in pols.items():
        lev = h.sum() / (h.sum() + c - d)
        Wt = frozen_rule(h, c, d, Rt)
        Wa = frozen_rule(h, c, d, Rf)
        Wb = frozen_rule(h, c, d, Rf, idio=idio, alpha_shift=shift)
        res = (np.sum(pt[Wt >= M.GOAL]), np.mean(Wa >= M.GOAL), np.mean(Wb >= M.GOAL))
        base[name] = res
        print(f"  {name:6s} exposure/W {lev:.2f}  illiquid share {h[M.NLIQ:].sum()/h.sum():.2f}  "
              f"tree {res[0]:.3f}  fresh(truth=belief) {res[1]:.3f}  fresh(truth!=belief, idio) {res[2]:.3f}  "
              f"E/W* tree {np.sum(pt*Wt)/M.GOAL:.3f} fresh {np.mean(Wa)/M.GOAL:.3f} {np.mean(Wb)/M.GOAL:.3f}")
    se = np.sqrt(0.25 / NP)
    for name in ("meanLP", "MILP"):
        d = [base[name][i] - base["SQ"][i] for i in range(3)]
        print(f"  uplift vs SQ, {name}: tree {100*d[0]:+.1f}pp  fresh(t=b) {100*d[1]:+.1f}pp  "
              f"fresh(t!=b) {100*d[2]:+.1f}pp   (MC se per estimate ~{100*se:.1f}pp)")

    # ---- risk-matched leverage control B4: SQ + debt-financed scaling of the liquid book,
    # sized so the fresh-path worst-decile mean of W~ equals the policy's (truth != belief).
    def w10(W):
        return np.sort(W)[: len(W) // 10].mean()
    def b4(x):
        h = M.h0.copy(); extra = x * h[:M.NLIQ].sum()
        h[:M.NLIQ] *= (1 + x)
        return h, M.c0, extra
    for name in ("meanLP", "MILP"):
        h, c, d = pols[name]
        Wp = frozen_rule(h, c, d, Rf, idio=idio, alpha_shift=shift)
        target = w10(Wp)
        lo_, hi_ = 0.0, 3.0
        for _ in range(40):
            mid = 0.5 * (lo_ + hi_)
            hb, cb, db = b4(mid)
            Wb4 = frozen_rule(hb, cb, db, Rf, idio=idio, alpha_shift=shift)
            if w10(Wb4) > target:
                lo_ = mid
            else:
                hi_ = mid
        hb, cb, db = b4(0.5 * (lo_ + hi_))
        Wb4 = frozen_rule(hb, cb, db, Rf, idio=idio, alpha_shift=shift)
        Wsq_f = frozen_rule(M.h0, M.c0, 0.0, Rf, idio=idio, alpha_shift=shift)
        print(f"  {name}: worst-decile mean W~/W0 {w10(Wp):.3f} (SQ {w10(Wsq_f):.3f}); "
              f"B4 matched at liquid scale {1 + 0.5*(lo_+hi_):.2f}, exposure/W {hb.sum()/(hb.sum()+cb-db):.2f}: "
              f"P(goal) B4 {np.mean(Wb4 >= M.GOAL):.3f} vs {name} {np.mean(Wp >= M.GOAL):.3f} "
              f"-> value at equal tail {100*(np.mean(Wp >= M.GOAL) - np.mean(Wb4 >= M.GOAL)):+.1f}pp")


if __name__ == "__main__":
    import builtins, functools
    builtins.print = functools.partial(builtins.print, flush=True)
    main()
