"""SYNTHETIC MILP sizing pilot for the DSGO spec review (not ADIC data).

A 10 x 5 x 4-fan tree (61 decision nodes, 200 leaves), 40 cohort assets (16 liquid,
24 illiquid with sale caps), cash floor 4%, leverage cap 1.30, owner draw 6% a year,
relative CVaR90 depth guard (delta = 0.01 W0) and 200 goal binaries. Measures
how HiGHS MIP behaves: plain big-M vs presolve-fixed big-M (per-leaf L/U bounds).
"""
import sys, time
import numpy as np
import scipy.sparse as sp
import highspy

RNG = np.random.default_rng(20261019)
NA, NLIQ = 40, 16
RF, RD, TC = 0.0389, 0.0389 + 0.0085, 0.002
DRAW = 0.06
T = 5
GOAL = 1.10 ** T
DELTA = 0.01
EPS_G = 0.001

# ---------------------------------------------------------------- scenario data
nf = 5
mu_f = np.array([0.040, 0.000, 0.000, 0.000, 0.000])
vol_f = np.array([0.16, 0.05, 0.04, 0.25, 0.10])
Cf = np.array([[1, -.6, .1, .3, .6], [-.6, 1, -.2, -.2, -.5], [.1, -.2, 1, .2, 0],
               [.3, -.2, .2, 1, .15], [.6, -.5, 0, .15, 1]])
Lf = np.linalg.cholesky(Cf * np.outer(vol_f, vol_f))
B = np.zeros((NA, nf))
B[:NLIQ, 0] = RNG.uniform(0.2, 1.1, NLIQ)
B[:NLIQ, 1] = RNG.uniform(-0.5, 0.0, NLIQ)
B[:NLIQ, 2] = RNG.uniform(-0.6, 0.2, NLIQ)
B[NLIQ:, 0] = RNG.uniform(0.8, 1.4, NA - NLIQ)
B[NLIQ:, 4] = RNG.uniform(0.4, 1.0, NA - NLIQ)
B[NLIQ:, 3] = RNG.uniform(-0.2, 0.6, NA - NLIQ)
ALPHA = RNG.normal(0.0, 0.01, NA) + np.where(np.arange(NA) >= NLIQ, 0.01, 0.0)


def draw_returns(n):
    f = mu_f + RNG.standard_normal((n, nf)) @ Lf.T
    return RF + ALPHA + f @ B.T               # arithmetic, (n, NA)


# tree: node list with parent, prob, returns on arrival
nodes = [dict(parent=None, stage=0, prob=1.0, r=None)]
for a in range(10):
    nodes.append(dict(parent=0, stage=1, prob=0.1, r=draw_returns(1)[0]))
st1 = [i for i, n in enumerate(nodes) if n["stage"] == 1]
for p in st1:
    for b in range(5):
        nodes.append(dict(parent=p, stage=2, prob=nodes[p]["prob"] / 5, r=draw_returns(1)[0]))
st2 = [i for i, n in enumerate(nodes) if n["stage"] == 2]
leaves = []
for p in st2:
    for k in range(4):
        leaves.append(dict(node=p, prob=nodes[p]["prob"] / 4, r=draw_returns(3)))   # (3, NA)
NN, NL = len(nodes), len(leaves)
h0 = np.full(NA, 0.92 / NA)                   # initial positions (W0 = 1), cash 8%
c0 = 0.08

# ---------------------------------------------------------------- variable layout
idx = {}
nv = 0
def add(name, n):
    global nv
    idx[name] = np.arange(nv, nv + n); nv += n
for n in range(NN):
    add(("h", n), NA); add(("b", n), NA); add(("s", n), NA); add(("c", n), 1); add(("d", n), 1)
for l in range(NL):
    add(("cl", l), 3); add(("dl", l), 3); add(("ql", l), 3)
add("eta", 1); add("u", NL)
NCONT = nv
add("g", NL)
NVAR = nv

rows, cols, vals, lo, up = [], [], [], [], []
nr = 0
def row(entries, l, u):
    global nr
    for c_, v_ in entries:
        rows.append(nr); cols.append(int(c_)); vals.append(float(v_))
    lo.append(l); up.append(u); nr += 1


# exogenous SQ wealth path for the draw (computed from a no-trade buy-and-hold sim)
def sq_wealth_node(n):
    path = []
    while n is not None:
        path.append(n); n = nodes[n]["parent"]
    path = path[::-1]
    h = h0.copy(); c = c0; w = h.sum() + c
    for k in path[1:]:
        h = h * (1 + nodes[k]["r"]); c = c * (1 + RF) - DRAW * w
        w = h.sum() + c
    return w, h, c
W_SQ = {n: sq_wealth_node(n)[0] for n in range(NN)}

# decision nodes
for n in range(NN):
    par = nodes[n]["parent"]
    H, Bv, S = idx[("h", n)], idx[("b", n)], idx[("s", n)]
    cn, dn = idx[("c", n)][0], idx[("d", n)][0]
    if par is None:
        grown_const = h0
        for i in range(NA):   # h = h0 + b - s
            row([(H[i], 1), (Bv[i], -1), (S[i], 1)], h0[i], h0[i])
        # cash: c = c0 + sum s(1-tc) - sum b(1+tc) + d
        ent = [(cn, 1)] + [(S[i], -(1 - TC)) for i in range(NA)] + [(Bv[i], 1 + TC) for i in range(NA)] + [(dn, -1)]
        row(ent, c0, c0)
        draw = 0.0
    else:
        r = nodes[n]["r"]
        Hp, cp, dp = idx[("h", par)], idx[("c", par)][0], idx[("d", par)][0]
        for i in range(NA):   # h = hp(1+r) + b - s
            row([(H[i], 1), (Hp[i], -(1 + r[i])), (Bv[i], -1), (S[i], 1)], 0.0, 0.0)
        draw = DRAW * W_SQ[par]
        ent = [(cn, 1), (cp, -(1 + RF)), (dn, -1), (dp, 1 + RD)] + \
              [(S[i], -(1 - TC)) for i in range(NA)] + [(Bv[i], 1 + TC) for i in range(NA)]
        row(ent, -draw, -draw)
        # illiquid sale cap: s_i <= 0.10 * hp_i (1+r_i)
        for i in range(NLIQ, NA):
            row([(S[i], 1), (Hp[i], -0.10 * (1 + r[i]))], -np.inf, 0.0)
    # cash floor c >= 0.04 W ; W = sum h + c - d
    row([(cn, 1 - 0.04)] + [(H[i], -0.04) for i in range(NA)] + [(dn, 0.04)], 0.0, np.inf)
    # leverage sum h <= 1.3 W  -> -0.3 sum h - 1.3 c + 1.3 d <= 0
    row([(H[i], -0.3) for i in range(NA)] + [(cn, -1.3), (dn, 1.3)], -np.inf, 0.0)
    # illiquid purchases capped at 2% of W0 per asset per node
    for i in range(NLIQ, NA):
        row([(Bv[i], 1)], -np.inf, 0.02)

# fans (buy-and-hold positions from stage-2 node; cash/debt funding only)
leaf_coef = []          # W~_l = sum_j coef_j x_j + const
for l, L in enumerate(leaves):
    n2 = L["node"]; H2 = idx[("h", n2)]; c2, d2 = idx[("c", n2)][0], idx[("d", n2)][0]
    CL, DL = idx[("cl", l)], idx[("dl", l)]
    growth = np.ones(NA)
    w_sq = W_SQ[n2]
    accr_draw = 0.0
    # SQ path wealth in the fan for the exogenous draw basis and static accrual
    _, hsq, csq = sq_wealth_node(n2)
    sq_vals = []
    hs, cs = hsq.copy(), csq
    for k in range(3):
        wprev = hs.sum() + cs
        hs = hs * (1 + L["r"][k]); cs = cs * (1 + RF) - DRAW * wprev
        sq_vals.append((wprev, hs.sum() + cs, hs.sum() / max(hs.sum(), 1e-12)))
    sq_ret = []   # static SAA (SQ) gross return per fan year
    for k in range(3):
        wprev, wnow, _ = sq_vals[k]
        sq_ret.append((wnow + DRAW * wprev) / wprev)
    QL = idx[("ql", l)]
    wl = h0[:NLIQ] / h0[:NLIQ].sum()
    rs = L["r"][:, :NLIQ] @ wl                      # pro-rata liquid slice return per fan year
    def gs(j, k):                                   # slice growth from end of year j to end of year k
        return float(np.prod(1 + rs[j + 1:k + 1])) if k > j else 1.0
    growths = []
    for k in range(3):
        growth = growth * (1 + L["r"][k])
        growths.append(growth.copy())
        draw = DRAW * sq_vals[k][0]
        prev_c = c2 if k == 0 else CL[k - 1]
        prev_d = d2 if k == 0 else DL[k - 1]
        row([(CL[k], 1), (prev_c, -(1 + RF)), (DL[k], -1), (prev_d, 1 + RD), (QL[k], -(1 - TC))], -draw, -draw)
        sold = [(QL[j], gs(j, k)) for j in range(k + 1)]
        # floor: c >= 0.04 (positions + c - d)
        row([(CL[k], 1 - 0.04)] + [(H2[i], -0.04 * growth[i]) for i in range(NA)] + [(DL[k], 0.04)]
            + [(q_, 0.04 * g_) for q_, g_ in sold], 0.0, np.inf)
        # leverage: positions <= 1.3 W
        row([(H2[i], -0.3 * growth[i]) for i in range(NA)] + [(CL[k], -1.3), (DL[k], 1.3)]
            + [(q_, 0.3 * g_) for q_, g_ in sold], -np.inf, 0.0)
        # cannot sell more liquid than held
        row([(H2[i], growth[i]) for i in range(NLIQ)] + [(q_, -g_) for q_, g_ in sold], 0.0, np.inf)
    # draws paid inside the tree accrue at the SQ static return (exogenous)
    # (approximate: accrue all draws on the path at SQ returns to T)
    path = []
    n = n2
    while n is not None:
        path.append(n); n = nodes[n]["parent"]
    path = path[::-1]
    draws = []
    for k in path[1:]:
        draws.append(DRAW * W_SQ[nodes[k]["parent"]])
    for k in range(3):
        draws.append(DRAW * sq_vals[k][0])
    # accrual factors: product of later SQ gross returns
    gross = []
    for k in path[1:]:
        par = nodes[k]["parent"]
        gross.append((W_SQ[k] + DRAW * W_SQ[par]) / W_SQ[par])
    gross += sq_ret
    acc = 0.0
    for t_, dv in enumerate(draws):
        acc += dv * np.prod(gross[t_ + 1:])
    coef = {}
    for i in range(NA):
        coef[H2[i]] = growth[i]
    coef[CL[2]] = 1.0; coef[DL[2]] = -1.0
    for j in range(3):
        coef[QL[j]] = -gs(j, 2)
    leaf_coef.append((coef, acc))

# CVaR90 depth guard on X = (W* - W~)/W0 relative to SQ
def leaf_expr(l):
    return leaf_coef[l]

# SQ leaf values (no trades: solve later by fixing b=s=0) -> computed after model built
eta, U, Gb = idx["eta"][0], idx["u"], idx["g"]
p = np.array([L["prob"] for L in leaves])

# placeholders: rows for u_l >= X_l - eta  ->  u_l + sum coef x + eta >= GOAL - acc
cvar_rows = []
for l in range(NL):
    coef, acc = leaf_coef[l]
    ent = [(U[l], 1), (eta, 1)] + [(j, v) for j, v in coef.items()]
    cvar_rows.append(nr)
    row(ent, GOAL - acc, np.inf)
cvar_main = nr
row([(eta, 1)] + [(U[l], p[l] / 0.10) for l in range(NL)], -np.inf, 0.0)   # rhs set later

goal_rows = []
for l in range(NL):
    coef, acc = leaf_coef[l]
    goal_rows.append(nr)
    row([(j, v) for j, v in coef.items()] + [(Gb[l], 0.0)], -np.inf, np.inf)  # set later

A = sp.csr_matrix((vals, (rows, cols)), shape=(nr, NVAR))
lo = np.array(lo, float); up = np.array(up, float)
col_lo = np.zeros(NVAR); col_up = np.full(NVAR, np.inf)
col_lo[eta] = -np.inf
col_up[Gb] = 1.0


def solve(obj, A_, lo_, up_, clo, cup, integer=False, time_limit=600, start=None, sense_max=False, quiet=True):
    h = highspy.Highs()
    h.setOptionValue("output_flag", not quiet)
    h.setOptionValue("time_limit", float(time_limit))
    h.setOptionValue("mip_rel_gap", 0.005)
    h.setOptionValue("threads", 1)
    Ac = A_.tocsc()
    lp = highspy.HighsLp()
    lp.num_col_ = A_.shape[1]; lp.num_row_ = A_.shape[0]
    lp.col_cost_ = (-obj if sense_max else obj).astype(float)
    lp.col_lower_ = clo; lp.col_upper_ = cup
    lp.row_lower_ = lo_; lp.row_upper_ = up_
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = Ac.indptr; lp.a_matrix_.index_ = Ac.indices; lp.a_matrix_.value_ = Ac.data
    if integer:
        integ = [highspy.HighsVarType.kContinuous] * A_.shape[1]
        for j in Gb:
            integ[j] = highspy.HighsVarType.kInteger
        lp.integrality_ = integ
    h.passModel(lp)
    if start is not None:
        sol = highspy.HighsSolution(); sol.col_value = list(start); sol.value_valid = True
        h.setSolution(sol)
    t0 = time.time(); h.run(); dt = time.time() - t0
    info = h.getInfo()
    x = np.array(h.getSolution().col_value) if h.getModelStatus() in (highspy.HighsModelStatus.kOptimal,
            highspy.HighsModelStatus.kTimeLimit, highspy.HighsModelStatus.kSolutionLimit) else None
    out = dict(status=h.modelStatusToString(h.getModelStatus()), time=dt, x=x,
               obj=info.objective_function_value)
    if integer:
        out.update(gap=info.mip_gap, bound=info.mip_dual_bound, nodes=info.mip_node_count)
    return out


def leaf_values(x):
    return np.array([sum(v * x[j] for j, v in leaf_coef[l][0].items()) + leaf_coef[l][1] for l in range(NL)])


def run():
    print(f"model: {NVAR} columns ({NL} binaries), {nr} rows, {A.nnz} nonzeros")
    # 1. SQ: fix b = s = 0 ; minimise total debt use (feasibility)
    clo, cup = col_lo.copy(), col_up.copy()
    for n in range(NN):
        cup[idx[("b", n)]] = 0; cup[idx[("s", n)][NLIQ:]] = 0
    lo2, up2 = lo.copy(), up.copy()
    lo2[cvar_main], up2[cvar_main] = -np.inf, np.inf
    cup[Gb] = 0.0
    obj = np.zeros(NVAR)
    for n in range(NN):
        obj[idx[("d", n)]] = nodes[n]["prob"]
        obj[idx[("s", n)][:NLIQ]] = 0.5 * nodes[n]["prob"]
    for l in range(NL):
        obj[idx[("dl", l)]] = p[l]
        obj[idx[("ql", l)]] = 0.5 * p[l]
    r = solve(obj, A, lo2, up2, clo, cup)
    print("SQ LP:", r["status"], f"{r['time']:.1f}s")
    Wsq = leaf_values(r["x"])
    Xsq = GOAL - Wsq
    order = np.argsort(-Xsq); cum = np.cumsum(p[order]); k = np.searchsorted(cum, 0.10)
    tail = order[:k + 1]; w = p[tail].copy(); w[-1] -= cum[k] - 0.10
    cvar_sq = np.sum(w * Xsq[tail]) / 0.10
    print(f"SQ: P(goal) in tree {np.sum(p[Wsq >= GOAL]):.3f}, E[W~]/W* {np.sum(p*Wsq)/GOAL:.3f}, CVaR90(X) {cvar_sq:.4f}")
    up[cvar_main] = cvar_sq + DELTA
    # 2. mean LP (STRETCH GBO proxy)
    obj = np.zeros(NVAR)
    for l in range(NL):
        for j, v in leaf_coef[l][0].items():
            obj[j] += p[l] * v
    clo, cup = col_lo.copy(), col_up.copy(); cup[Gb] = 0.0
    r = solve(obj, A, lo, up, clo, cup, sense_max=True)
    Wm = leaf_values(r["x"])
    print(f"mean LP: {r['status']} {r['time']:.1f}s  E[W~]/W* {np.sum(p*Wm)/GOAL:.3f}  P(goal) tree {np.sum(p[Wm >= GOAL + EPS_G]):.3f}")
    xm = r["x"]
    # 3. per-leaf bounds L_l, U_l (2 LPs per leaf, one warm-started HiGHS instance)
    t0 = time.time(); Lb = np.zeros(NL); Ub = np.zeros(NL)
    h = highspy.Highs(); h.setOptionValue("output_flag", False); h.setOptionValue("threads", 1)
    Ac = A.tocsc(); lp = highspy.HighsLp()
    lp.num_col_ = NVAR; lp.num_row_ = A.shape[0]
    lp.col_cost_ = np.zeros(NVAR); lp.col_lower_ = clo; lp.col_upper_ = cup
    lp.row_lower_ = lo; lp.row_upper_ = up
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = Ac.indptr; lp.a_matrix_.index_ = Ac.indices; lp.a_matrix_.value_ = Ac.data
    h.passModel(lp)
    allc = np.arange(NVAR, dtype=np.int32)
    for l in range(NL):
        o = np.zeros(NVAR)
        for j, v in leaf_coef[l][0].items():
            o[j] = v
        for sgn in (1.0, -1.0):
            h.changeColsCost(NVAR, allc, sgn * o)
            h.run()
            val = h.getInfo().objective_function_value
            if sgn > 0:
                Lb[l] = val + leaf_coef[l][1]
            else:
                Ub[l] = -val + leaf_coef[l][1]
        if l % 50 == 0:
            print(f"  bounds leaf {l}: {time.time() - t0:.1f}s", flush=True)
    tb = time.time() - t0
    fix1 = Lb >= GOAL + EPS_G; fix0 = Ub < GOAL + EPS_G
    print(f"leaf bounds: {2*NL} LPs in {tb:.1f}s; fixed to 1: {fix1.sum()}, fixed to 0: {fix0.sum()}, free: {NL - fix1.sum() - fix0.sum()}")
    # 4. MILP: set goal rows  sum coef x + acc - W* >= eps - M(1-g)  ->  sum coef x - M g >= W* + eps - acc - M
    def milp(fix, tl):
        A2 = A.tolil(copy=True)
        lo3, up3 = lo.copy(), up.copy()
        M = GOAL + EPS_G - Lb
        for l in range(NL):
            A2[goal_rows[l], Gb[l]] = -M[l]
            lo3[goal_rows[l]] = GOAL + EPS_G - leaf_coef[l][1] - M[l]
            up3[goal_rows[l]] = np.inf
        clo3, cup3 = col_lo.copy(), col_up.copy()
        if fix:
            clo3[Gb[fix1]] = 1.0; cup3[Gb[fix0]] = 0.0
        obj = np.zeros(NVAR); obj[Gb] = p
        start = xm.copy(); start[Gb] = (Wm >= GOAL + EPS_G).astype(float)
        return solve(obj, A2.tocsr(), lo3, up3, clo3, cup3, integer=True, time_limit=tl,
                     start=start, sense_max=True)
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
    for fix in (False, True):
        r = milp(fix, tl)
        Wx = leaf_values(r["x"]) if r["x"] is not None else None
        pg = np.sum(p[Wx >= GOAL + EPS_G - 1e-7]) if Wx is not None else float("nan")
        print(f"MILP fix={fix}: {r['status']} {r['time']:.1f}s  P(goal) {pg:.3f}  bound {-r['bound']:.3f}  gap {r['gap']:.4f}  nodes {r['nodes']}")


if __name__ == "__main__":
    import builtins, functools
    builtins.print = functools.partial(builtins.print, flush=True)
    run()
