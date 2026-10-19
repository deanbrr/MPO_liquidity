#!/usr/bin/env python
"""
tree_demo.py (version 2): a worked multistage stochastic program on a 40-node scenario tree.

SYNTHETIC. Every number is illustrative (see params.json). Nothing here is ADIC data.

WHAT IT SHOWS
  The quant core of the design is one objective optimization. Given the inputs in params.json and the
  limits people set, ONE linear program computes
    * a decision at every node of a scenario tree (SELL / HOLD / REFINANCE / LEVER / PACE-CUT),
    * the shadow price of liquidity at every node (read from the LP duals), and
    * the probability of every outcome (products of the branch probabilities).
  No step inside the solve is a judgement call. People set the inputs and limits and approve the result.

THE MODEL IN ONE PARAGRAPH (RESULTS.md section 9 writes out every row)
  Annual stages: decisions at t = 0, 1, 2; horizon t = 3. Three regimes a year: N normal, D PE distribution
  drought, C crisis with an oil shock. Start in D. 1 + 3 + 9 + 27 = 40 nodes. Regimes decide the year's cash flows
  (PE calls and distributions, the owner's draw, the yield book's cash), bids and facility availability, and the
  shape of the year's returns; next year's expected return and volatility are the same from every regime (computed
  from params.json), so the program has nothing to time.
  At each decision node the program may sell or buy liquid assets; convert physical to synthetic exposure (P2S, a
  REFINANCE) or back; SELL PE interests at the regime's discount (the buyer takes the matching unfunded);
  REFINANCE with a NAV loan (pledge-pool capped) or the committed revolver (availability capped); cut up to 75% of
  the year's PE commitments (a protected core sleeve). Synthetic LEVER of the liquid book is off by the doctrine
  (beta has alpha* < 0); a facility draw that pays for purchases is labelled LEVER.
  Then the year happens under the child's regime, and the owner's draw (a share of NAV, higher when oil is weak)
  is paid in full: there is no variable that could skip it.
  Hard rows at every node, t = 3 included: unencumbered cash >= 4% of NAV, NAV-loan capacity, revolver
  availability (forced paydowns), the IC range's upper edge; at decision nodes exposure <= 1.30x and the synthetic
  budget; at t = 3 debt can be repaid, not drawn. Appetite rows, elastic and priced in terminal wealth: own
  liquidity (cash net of facility draws) >= 8% of NAV, and the IC range's lower edge (both free in a crisis year).
  Terminal wealth uses economic PE value and a burden on unfunded commitments.
  Objective (Tier 2): maximize E[U(W~/W0)], U = CRRA(3) approximated by tangent lines (an LP).
  Non-anticipativity holds by construction: one decision vector per node.

  Also computed: the tree without a signed revolver (consent scenario R0); Phase I with reversible levers only;
  three naive rules under the same limits; the rolling (closed-loop) policy, re-solved at all 12 nodes of
  t = 1 and t = 2; a horizon test (2, 3 and 4 years); one-at-a-time sensitivities with their owners; downside
  floors as a sensitivity; finite-difference, carry and kink checks of the duals; a 48-tangent decision test.
  Version 2 applies the corrections in verify_math.md and verify_finance.md (RESULTS.md section 10).

  Solved with HiGHS dual simplex, so the solution is basic and its duals are exact LP duals.
    m_n      = mu_n / (p_n * mu_0)       state price: today's value of $1 arriving at node n, per unit of
                                         probability (mu_n = dual of node n's cash-balance row)
    lambda_n = M_n / (mu_n - M_n)        liquidity premium (ARCHITECTURE.md section 5.6); M_n = dual mass of
                                         node n's liquidity rows (4% floor and 8% target) on its cash

Run:   .venv\\Scripts\\python.exe examples\\tree_demo\\tree_demo.py
Reads: params.json (same folder).  Writes: results.json and RESULTS.md (same folder).
Independent check: verify_independent.py (same folder) re-solves the main case with cvxpy and writes
verification.json and the Verification section of RESULTS.md.
Deterministic: single-threaded simplex, fixed seed, no random numbers; results.json carries no timings.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import highspy

HERE = Path(__file__).resolve().parent
INF = highspy.kHighsInf
REGIMES = ("N", "D", "C")
REGIME_NAME = {"N": "normal", "D": "PE distribution drought", "C": "crisis with oil shock"}
STAGES = ("Green", "Amber", "Red", "Black")
OBJ_SCALE = 1000.0   # solver setting: LP objective = OBJ_SCALE * E[U], keeps duals well above simplex tolerances
DEC_KEYS = ("sell_liquid", "buy_liquid", "sell_pe_nav", "nav_loan_change", "revolver_change",
            "synthetic_notional", "pace_cut")


# =============================================================================================
# 1. Parameters
# =============================================================================================
def load_params(path: Path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    val = {sec: {k: item["value"] for k, item in body.items()}
           for sec, body in raw.items() if not sec.startswith("_")}
    return raw, val


def apply_changes(v, changes: dict):
    """Return a deep copy of v with dotted-key changes applied, e.g. {'rates.owner_draw_rate.C': 0.10}."""
    vv = copy.deepcopy(v)
    for key, val in changes.items():
        parts = key.split(".")
        d = vv
        for p_ in parts[:-1]:
            d = d[p_]
        d[parts[-1]] = copy.deepcopy(val)
    return vv


def S(v, key):
    return v["settings"][key]


# =============================================================================================
# 2. The scenario tree
# =============================================================================================
@dataclass
class Node:
    id: int
    stage: int
    regime: str
    path: str
    parent: int | None
    cond_prob: float
    prob: float
    children: list = field(default_factory=list)
    # Rates of the year that ENDS at this node (unused at the root).
    rL: float = 0.0      # liquid book total return (regime shape + valuation adjustment)
    rP: float = 0.0      # PE reported-NAV total return (value created, before distributions)
    adjL: float = 0.0    # valuation adjustment from the previous year's regime (liquid)
    adjP: float = 0.0    # valuation adjustment from the previous year's regime (PE)
    gY: float = 0.0      # yield-book NAV change (excluding cash yield)
    yY: float = 0.0      # yield-book cash yield
    dist: float = 0.0    # PE distributions, share of opening PE NAV
    call: float = 0.0    # PE calls, share of opening unfunded
    draw: float = 0.0    # owner draw, share of opening NAV
    rRef: float = 0.0    # static-allocation return of the year (only used to accrue owner draws)
    Y: float = 0.0       # yield-book NAV at this node (exogenous: no decision is taken on it)


def return_matrix(v, base_key, mean_key, vol_key):
    """Return of a year in regime j that follows a year in regime i, R[i][j], under the chosen return model.

    'equal_conditional_moments': R[i][j] = mean + s_i (r_j - m_i), with m_i = sum_j T[i][j] r_j,
        sd_i = (sum_j T[i][j] (r_j - m_i)^2)^0.5 and s_i = sd* / sd_i: next year's expected return AND volatility
        are the same from every regime (sd* = the start regime's unless set). Regimes still decide which year
        happens (cash flows, bids, facility availability) and the shape of the year (a crisis after a calm year
        is a deeper loss than a crisis after a crisis), but give the program no mean or volatility to time.
    'equal_conditional_means': R[i][j] = r_j + (mean - m_i): same expected return, regime-dependent volatility.
    'regime_means' (v1): R[i][j] = r_j, plus a rebound in a year that follows a crisis and is not itself one."""
    R, T = v["rates"], v["tree"]["transition_matrix"]
    model = R.get("return_model", "equal_conditional_moments")
    r = R[base_key]
    m = {i: sum(T[i][j] * r[j] for j in REGIMES) for i in REGIMES}
    sd = {i: math.sqrt(sum(T[i][j] * (r[j] - m[i]) ** 2 for j in REGIMES)) for i in REGIMES}
    out = {}
    if model == "equal_conditional_moments":
        target_sd = R.get(vol_key) or sd[v["tree"]["start_regime"]]
        for i in REGIMES:
            out[i] = {j: R[mean_key] + target_sd / sd[i] * (r[j] - m[i]) for j in REGIMES}
    elif model == "equal_conditional_means":
        for i in REGIMES:
            out[i] = {j: r[j] + R[mean_key] - m[i] for j in REGIMES}
    else:
        reb = R.get("liquid_rebound_after_crisis" if base_key == "liquid_return" else "pe_rebound_after_crisis", 0.0)
        for i in REGIMES:
            out[i] = {j: r[j] + (reb if (i == "C" and j != "C") else 0.0) for j in REGIMES}
    return out, {"conditional_mean_before": m, "conditional_sd_before": sd}


def return_adjustments(v):
    """Both return matrices (liquid book, PE reported NAV)."""
    RL, _ = return_matrix(v, "liquid_return", "liquid_expected_return", "liquid_volatility")
    RP, _ = return_matrix(v, "pe_nav_return", "pe_expected_return", "pe_volatility")
    return RL, RP


def build_tree(v, root_regime: str, horizon: int, Y0: float, saa_w: dict) -> list[Node]:
    """Breadth-first tree: ids 0 | 1-3 | 4-12 | 13-39 for a 3-year horizon."""
    R, T = v["rates"], v["tree"]["transition_matrix"]
    RL, RP = return_adjustments(v)
    nodes = [Node(0, 0, root_regime, root_regime, None, 1.0, 1.0, Y=Y0)]
    frontier = [0]
    for t in range(1, horizon + 1):
        nxt = []
        for pid in frontier:
            par = nodes[pid]
            for r in REGIMES:
                cp = T[par.regime][r]
                n = Node(len(nodes), t, r, f"{par.path}>{r}", pid, cp, par.prob * cp)
                n.rL, n.rP = RL[par.regime][r], RP[par.regime][r]
                n.adjL, n.adjP = n.rL - R["liquid_return"][r], n.rP - R["pe_nav_return"][r]
                n.gY, n.yY = R["yield_nav_return"][r], R["yield_cash_rate"][r]
                n.dist, n.call, n.draw = (R["pe_distribution_rate"][r], R["pe_call_rate"][r],
                                          R["owner_draw_rate"][r])
                n.Y = par.Y * (1.0 + n.gY)
                n.rRef = (saa_w["C"] * R["cash_rate"] + saa_w["L"] * n.rL + saa_w["P"] * n.rP
                          + saa_w["Y"] * (n.yY + n.gY))
                nodes.append(n)
                par.children.append(n.id)
                nxt.append(n.id)
        frontier = nxt
    return nodes


def path_ids(nodes, n: Node) -> list[int]:
    out = [n.id]
    while nodes[out[-1]].parent is not None:
        out.append(nodes[out[-1]].parent)
    return out[::-1]


def accrual_factor(nodes, path: list[int], i: int) -> float:
    """Growth from the end of year path[i] to the horizon at the static-allocation return.
    Owner draws are added back to terminal wealth at this growth (ARCHITECTURE.md 5.2: W~ = W_T + sum d_t G)."""
    g = 1.0
    for j in path[i + 1:]:
        g *= 1.0 + nodes[j].rRef
    return g


def node_by_path(nodes, path):
    return next(n for n in nodes if n.path == path)


# =============================================================================================
# 3. One year of flows: the child's pre-decision state as an affine map of the parent's decisions
# =============================================================================================
def transition(v, par: Node, ch: Node, lim: float) -> dict:
    """Return {quantity: (coefficients over the parent's post-decision variables, constant)}.

    Timing: decisions at the parent (start of the year); then, under the CHILD's regime, returns accrue,
    PE calls and distributions arrive, the yield book pays cash, loans pay interest and the owner's draw is
    paid. The same map drives the LP rows, the reporting, the naive rules and the closed-loop simulation.
    """
    R, A = v["rates"], v["actions"]
    rc = R["cash_rate"]
    h = A["lever_initial_margin"][par.regime]
    d, q, dist = ch.draw, ch.call, ch.dist
    q1, plan = A["new_commitment_first_year_call_rate"], A["pacing_plan"]
    sR, uR = A["revolver_drawn_spread"], A["revolver_undrawn_fee"]
    sN = A["nav_loan_spread"][par.regime]           # spread set when the balance is carried forward
    sX = A["lever_financing_spread"][par.regime]    # synthetic financing locked when the position is put on
    # Owner draw = d x opening NAV, opening NAV = C + IM + L + P + Y - BR - BN with IM = h X.
    cash = {
        "C": 1.0 + rc - d,                        # cash earns SOFR; the draw scales with NAV
        "L": -d,
        "P": dist - d,                            # distributions on opening PE NAV
        "U": -q,                                  # calls on opening unfunded
        "BR": d - (rc + sR) + uR,                 # revolver interest; the undrawn fee falls as BR rises
        "BN": d - (rc + sN),                      # NAV-loan interest
        "X": (1.0 + rc) * h + (ch.rL - rc - sX) - d * h,   # margin returned with interest + variation margin
        "cut": q1,                                # first-year calls on new commitments (zero by default)
    }
    cash_const = (ch.yY - d) * par.Y - uR * lim - q1 * plan
    return {
        "cash": (cash, cash_const),
        "liq": ({"L": 1.0 + ch.rL}, 0.0),
        "pe": ({"P": 1.0 + ch.rP - dist, "U": q, "cut": -q1}, q1 * plan),
        "unf": ({"U": 1.0 - q, "cut": -(1.0 - q1)}, (1.0 - q1) * plan),   # new commitments join unfunded
    }


def pre_state(v, par: Node, ch: Node, post_par: dict, lim: float) -> dict:
    tr = transition(v, par, ch, lim)

    def ev(key):
        co, c0 = tr[key]
        return sum(a * post_par[k] for k, a in co.items()) + c0

    return dict(C=ev("cash"), L=ev("liq"), P=ev("pe"), U=ev("unf"), BR=post_par["BR"], BN=post_par["BN"],
                Y=ch.Y, Xprev=post_par["X"])


def nav_post(v, n: Node, p: dict) -> float:
    h = v["actions"]["lever_initial_margin"][n.regime]
    return p["C"] + h * p.get("X", 0.0) + p["L"] + p["P"] + n.Y - p["BR"] - p["BN"]


def year_flows(v, par: Node, ch: Node, post_par: dict, lim: float) -> dict:
    """The same year, broken into named cash flows for the report ($bn; + = into cash)."""
    R, A = v["rates"], v["actions"]
    rc = R["cash_rate"]
    h = A["lever_initial_margin"][par.regime]
    q1, plan = A["new_commitment_first_year_call_rate"], A["pacing_plan"]
    im = h * post_par["X"]
    out = {
        "owner_draw": -ch.draw * nav_post(v, par, post_par),
        "pe_distributions": ch.dist * post_par["P"],
        "pe_calls": -(ch.call * post_par["U"] + q1 * (plan - post_par["cut"])),
        "yield_cash": ch.yY * par.Y,
        "cash_interest": rc * (post_par["C"] + im),
        "margin_returned": im,
        "lever_variation_margin": (ch.rL - rc - A["lever_financing_spread"][par.regime]) * post_par["X"],
        "revolver_interest_and_fees": -((rc + A["revolver_drawn_spread"]) * post_par["BR"]
                                        + A["revolver_undrawn_fee"] * (lim - post_par["BR"])),
        "nav_loan_interest": -(rc + A["nav_loan_spread"][par.regime]) * post_par["BN"],
    }
    out["net_cash_flow_ex_returns"] = sum(val for k, val in out.items()
                                          if k not in ("cash_interest", "margin_returned",
                                                       "lever_variation_margin"))
    return out


# =============================================================================================
# 4. A thin LP layer on top of highspy (scipy.sparse assembly, named rows and columns)
# =============================================================================================
class LP:
    def __init__(self):
        self.vnames, self.lb, self.ub, self.cost, self.vidx = [], [], [], [], {}
        self.rnames, self.rlo, self.rhi, self.rnode, self.rkind, self.ridx = [], [], [], [], [], {}
        self._ri, self._ci, self._vv = [], [], []

    def var(self, name, lb=0.0, ub=INF, cost=0.0):
        self.vidx[name] = len(self.vnames)
        self.vnames.append(name)
        self.lb.append(lb)
        self.ub.append(ub)
        self.cost.append(cost)

    def row(self, name, terms, lo, hi, node=None, kind=None):
        i = len(self.rnames)
        self.ridx[name] = i
        self.rnames.append(name)
        self.rlo.append(lo)
        self.rhi.append(hi)
        self.rnode.append(node)
        self.rkind.append(kind)
        acc = {}
        for var, a in terms:
            acc[var] = acc.get(var, 0.0) + a
        for var, a in acc.items():
            if a != 0.0:
                self._ri.append(i)
                self._ci.append(self.vidx[var])
                self._vv.append(a)

    def set_row_bounds(self, name, lo, hi):
        i = self.ridx[name]
        self.rlo[i], self.rhi[i] = lo, hi

    def matrix(self):
        A = sp.csc_matrix((self._vv, (self._ri, self._ci)), shape=(len(self.rnames), len(self.vnames)))
        A.sum_duplicates()
        A.sort_indices()
        return A

    def solve(self) -> "Sol":
        A = self.matrix()
        lp = highspy.HighsLp()
        lp.num_col_, lp.num_row_ = A.shape[1], A.shape[0]
        lp.sense_ = highspy.ObjSense.kMaximize
        lp.col_cost_ = np.asarray(self.cost, float)
        lp.col_lower_ = np.asarray(self.lb, float)
        lp.col_upper_ = np.asarray(self.ub, float)
        lp.row_lower_ = np.asarray(self.rlo, float)
        lp.row_upper_ = np.asarray(self.rhi, float)
        lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
        lp.a_matrix_.start_ = A.indptr
        lp.a_matrix_.index_ = A.indices
        lp.a_matrix_.value_ = A.data
        h = highspy.Highs()
        for k, val in (("output_flag", False), ("solver", "simplex"), ("threads", 1),
                       ("random_seed", 0), ("primal_feasibility_tolerance", 1e-9),
                       ("dual_feasibility_tolerance", 1e-9)):
            h.setOptionValue(k, val)
        h.passModel(lp)
        h.run()
        status = h.modelStatusToString(h.getModelStatus())
        s = h.getSolution()
        info = h.getInfo()
        return Sol(self, status, info.objective_function_value, np.array(s.col_value),
                   np.array(s.row_value), np.array(s.row_dual), np.array(s.col_dual),
                   int(info.simplex_iteration_count), A.nnz)


@dataclass
class Sol:
    lp: LP
    status: str
    obj: float
    xv: np.ndarray
    rv: np.ndarray
    rd: np.ndarray        # row duals: d(objective)/d(row bound), HiGHS convention, maximize sense
    cd: np.ndarray
    iters: int
    nnz: int

    @property
    def ok(self):
        return self.status == "Optimal"

    def x(self, name):
        return float(self.xv[self.lp.vidx[name]])

    def has(self, name):
        return name in self.lp.vidx

    def dual(self, row):
        return float(self.rd[self.lp.ridx[row]])

    def act(self, row):
        return float(self.rv[self.lp.ridx[row]])


# =============================================================================================
# 5. The tree program
# =============================================================================================
def crra(w, g):
    return w ** (1.0 - g) / (1.0 - g)


def crra_prime(w, g):
    return w ** (-g)


def _price(pr, regime, horizon):
    if horizon and "horizon" in pr:
        return pr["horizon"]
    return pr[regime]


def target_price(v, regime, horizon=False):
    """$ charged per $ of own liquidity below the 8% target for one year at a node; horizon nodes use the
    'horizon' price, because a shortfall left at t = 3 still has to be restored after it."""
    return _price(v["limits"]["cash_target_shortfall_price"], regime, horizon)


def band_price(v, regime, horizon=False):
    """$ charged per $ of public-markets exposure below the IC range's lower edge for one year at a node."""
    pr = v["limits"].get("liquid_exposure_min_shortfall_price")
    return 0.0 if pr is None else _price(pr, regime, horizon)


def band_lo_value(v, regime, horizon=False):
    """Lower edge of the IC range at a node of this regime (None = not enforced there)."""
    Lm = v["limits"]
    lo = Lm.get("liquid_exposure_min_frac")
    if lo is None:
        return None
    val = lo.get(regime) if isinstance(lo, dict) else lo
    if val is None or regime in set(Lm.get("liquid_exposure_min_waived_in_regimes") or []):
        return None
    if horizon and not (Lm.get("liquid_exposure_min_enforced_at_horizon") or {}).get(regime, True):
        return None
    return val


def band_lo_applies(v, regime, horizon=False):
    return band_lo_value(v, regime, horizon) is not None


def nav_loan_capacity_terms(v, n):
    """NAV-loan capacity at node n = LTV_n x pool x (P + Y if the pool includes the yield book)."""
    A = v["actions"]
    k = A["nav_loan_ltv_cap"][n.regime] * A["nav_loan_pledge_pool_frac"]
    const = k * n.Y if A["nav_loan_pledge_pool_includes_yield_book"] else 0.0
    return k, const


def build_lp(v, nodes, root, W0, tangents, lim, *, cvar_floor=None, allow_pe_sales=True,
             root_pe_zero=False, offsets=None, mode="utility", phase1_tier=None, u_tier_a=None) -> LP:
    """Assemble the tree LP.

    mode 'utility'  : Tier 2 objective, max E[PWL CRRA(W~/W0)];
         'settle'   : one-node tree whose root is a horizon node: max W~ (closed-loop settlement at t = 3);
         'maxcvar'  : max CVaR10% of W~ (capacity check for a downside floor);
         'phase1'   : tier 'A' minimizes the probability-weighted shortfall below the 4% floor with reversible
                      levers only (the IC range is not a Tier-1A row); tier 'B' then minimizes the shortfall
                      below the IC range's lower edge while holding tier A at its optimum."""
    A, Lm, Tm = v["actions"], v["limits"], v["terminal"]
    f, f8 = Lm["cash_floor_frac"], Lm["cash_target_frac"]
    pi8 = Lm["cash_target_shortfall_price"]
    tau, kU = A["liquid_trade_cost"], A["unfunded_assumed_per_nav_sold"]
    plan, cpace, kap = A["pacing_plan"], A["pacing_cut_cost"], A["exposure_cap"]
    cut_max = (1.0 - A["pacing_core_sleeve"]) * plan
    om, psi = Tm["pe_value_per_nav"], Tm["unfunded_burden_per_dollar"]
    hi_b = Lm.get("liquid_exposure_max_frac")
    syn_cap = A.get("synthetic_notional_cap")
    p2s_only = A.get("synthetic_use", "p2s_and_lever") == "p2s_only"
    net_target = Lm.get("cash_target_basis", "gross") == "net_of_facility_draws"
    g, alpha = v["objective"]["crra_gamma"], Lm["cvar_alpha"]
    H = max(n.stage for n in nodes)
    offsets = offsets or {}
    want_cvar = cvar_floor is not None or mode == "maxcvar"
    include_band = mode != "phase1" or phase1_tier == "B"
    lp = LP()

    def nm(s_, n):
        return f"{s_}[{n.id}]"

    # ---- columns ----------------------------------------------------------------------------
    no_buy = set(A.get("no_liquid_purchases_in_regimes") or [])
    for n in nodes:
        dec = n.stage < H
        for s_ in ("C", "L", "P", "U", "sL", "bL", "BR", "BN", "s8"):
            lp.var(nm(s_, n), ub=0.0 if (s_ == "bL" and n.regime in no_buy) else INF)
        # Shortfall below the IC range's lower edge (elastic): priced in W~ in 'utility' and 'settle' modes,
        # the objective of Phase I tier B.
        lp.var(nm("sb", n), cost=(-OBJ_SCALE * n.prob if (mode == "phase1" and phase1_tier == "B") else 0.0))
        no_sale = (not allow_pe_sales) or (root_pe_zero and n.parent is None)
        lp.var(nm("sP", n), ub=0.0 if no_sale else INF)
        if dec:
            lp.var(nm("X", n))        # synthetic notional held after the node's decisions
            lp.var(nm("cv", n))       # P2S: physical converted to synthetic (exposure unchanged)
            lp.var(nm("uw", n))       # unwind: synthetic converted back to physical
            lp.var(nm("lev", n), ub=0.0 if p2s_only else INF)   # LEVER: synthetic exposure added
            lp.var(nm("cut", n))
        else:
            lp.var(nm("W", n), lb=-INF, cost=OBJ_SCALE if mode == "settle" else 0.0)
            if mode == "utility":
                lp.var(nm("u", n), lb=-INF, cost=OBJ_SCALE * n.prob)
            if want_cvar:
                lp.var(nm("z", n), cost=(-OBJ_SCALE * n.prob / alpha if mode == "maxcvar" else 0.0))
        if mode == "phase1":
            lp.var(nm("e", n), cost=(-OBJ_SCALE * n.prob if phase1_tier == "A" else 0.0))
    if want_cvar:
        lp.var("eta", lb=-INF, cost=(OBJ_SCALE if mode == "maxcvar" else 0.0))

    # ---- rows -------------------------------------------------------------------------------
    for n in nodes:
        dec = n.stage < H
        hn = A["lever_initial_margin"][n.regime] if dec else 0.0
        dl = A["pe_secondary_discount"][n.regime]
        C, L, P, U, sL, bL, sP, BR, BN, s8 = (nm(s_, n) for s_ in
                                              ("C", "L", "P", "U", "sL", "bL", "sP", "BR", "BN", "s8"))
        X = nm("X", n) if dec else None
        cv, uw, lev = (nm("cv", n), nm("uw", n), nm("lev", n)) if dec else (None, None, None)
        # Trades common to the cash and liquid rows. P2S sells physical at the trading cost and holds the same
        # exposure synthetically; an unwind buys the physical back. Margin h_n X_n is posted on the whole
        # synthetic position (the parent's margin came back in this year's flows).
        cash_trades = [(sL, -(1 - tau)), (bL, 1 + tau), (sP, -(1 - dl)), (BR, -1.0), (BN, -1.0)]
        liq_trades = [(sL, 1.0), (bL, -1.0)]
        if dec:
            cash_trades += [(cv, -(1 - tau)), (uw, 1 + tau), (X, hn)]
            liq_trades += [(cv, 1.0), (uw, -1.0)]
        if n.parent is None:
            # Root: the opening balance sheet is data.
            c0 = root["C"] - root["BR"] - root["BN"]
            lp.row(nm("cash", n), [(C, 1.0)] + cash_trades, c0, c0, n.id, "cash")
            lp.row(nm("liq", n), [(L, 1.0)] + liq_trades, root["L"], root["L"], n.id, "liq")
            lp.row(nm("pe", n), [(P, 1.0), (sP, 1.0)], root["P"], root["P"], n.id, "pe")
            lp.row(nm("unf", n), [(U, 1.0), (sP, kU)], root["U"], root["U"], n.id, "unf")
            if dec:
                xp = root.get("Xprev", 0.0)
                lp.row(nm("synflow", n), [(X, 1.0), (cv, -1.0), (uw, 1.0), (lev, -1.0)], xp, xp, n.id, "synflow")
                lp.row(nm("uwcap", n), [(uw, 1.0)], -INF, xp, n.id, "uwcap")
            else:
                lp.row(nm("norev", n), [(BR, 1.0)], -INF, root["BR"], n.id, "norev")
                lp.row(nm("nonav", n), [(BN, 1.0)], -INF, root["BN"], n.id, "nonav")
        else:
            par = nodes[n.parent]
            tr = transition(v, par, n, lim)
            # Cash balance: C_n = (year's flows from the parent's post-decision state) + this node's trades.
            co, c0 = tr["cash"]
            terms = [(C, 1.0)] + [(nm(k, par), -a) for k, a in co.items()] + cash_trades
            terms += [(nm("BR", par), 1.0), (nm("BN", par), 1.0)]
            lp.row(nm("cash", n), terms, c0, c0, n.id, "cash")
            co, c0 = tr["liq"]
            lp.row(nm("liq", n), [(L, 1.0)] + liq_trades + [(nm(k, par), -a) for k, a in co.items()],
                   c0, c0, n.id, "liq")
            if dec:
                # Synthetic notional carried from the parent, plus P2S and LEVER, less unwinds (of carried
                # positions only).
                lp.row(nm("synflow", n), [(X, 1.0), (nm("X", par), -1.0), (cv, -1.0), (uw, 1.0), (lev, -1.0)],
                       0.0, 0.0, n.id, "synflow")
                lp.row(nm("uwcap", n), [(uw, 1.0), (nm("X", par), -1.0)], -INF, 0.0, n.id, "uwcap")
            co, c0 = tr["pe"]
            lp.row(nm("pe", n), [(P, 1.0), (sP, 1.0)] + [(nm(k, par), -a) for k, a in co.items()],
                   c0, c0, n.id, "pe")
            co, c0 = tr["unf"]
            # A secondary buyer takes over kU of unfunded per $ of NAV bought.
            lp.row(nm("unf", n), [(U, 1.0), (sP, kU)] + [(nm(k, par), -a) for k, a in co.items()],
                   c0, c0, n.id, "unf")
            if not dec:
                # Horizon: debt can be repaid (and must be, where a cap has shrunk), never drawn. A draw at t = 3
                # would cost nothing inside the horizon, so it would be a free and arbitrary move.
                lp.row(nm("norev", n), [(BR, 1.0), (nm("BR", par), -1.0)], -INF, 0.0, n.id, "norev")
                lp.row(nm("nonav", n), [(BN, 1.0), (nm("BN", par), -1.0)], -INF, 0.0, n.id, "nonav")

        def nav_terms(scale):
            """scale x NAV_n as (column, coefficient) pairs; the constant part is scale x Y_n."""
            t_ = [(C, scale), (L, scale), (P, scale), (BR, -scale), (BN, -scale)]
            if dec:
                t_.append((X, scale * hn))
            return t_

        # Tier 1A cash floor: unencumbered cash - f * NAV >= 0 (posted margin is NAV but not cash).
        terms = [(C, 1.0)] + nav_terms(-f)
        if mode == "phase1":
            terms.append((nm("e", n), 1.0))
        lp.row(nm("floor", n), terms, f * n.Y, INF, n.id, "floor")
        # Elastic 8% target: cash (net of facility draws if so set) + shortfall >= f8 * NAV; the shortfall is
        # charged in W~ (below), so the target is never a hard row.
        tterms = [(C, 1.0), (s8, 1.0)] + nav_terms(-f8)
        if net_target:
            tterms += [(BR, -1.0), (BN, -1.0)]
        lp.row(nm("target", n), tterms, f8 * n.Y, INF, n.id, "target")
        # NAV-loan capacity (pledge pool x LTV of the node's regime) and revolver availability.
        k_ltv, c_ltv = nav_loan_capacity_terms(v, n)
        lp.row(nm("ltv", n), [(BN, 1.0), (P, -k_ltv)], -INF, c_ltv, n.id, "ltv")
        lp.row(nm("rcf", n), [(BR, 1.0)], -INF, A["revolver_availability"][n.regime] * lim, n.id, "rcf")
        if dec:
            # Gross exposure L + P + Y + X <= kap * NAV.
            lp.row(nm("expo", n), [(L, 1.0), (P, 1.0), (X, 1.0)] + nav_terms(-kap), -INF, (kap - 1) * n.Y,
                   n.id, "expo")
            lp.row(nm("pace", n), [(nm("cut", n), 1.0)], -INF, cut_max, n.id, "pace")
            if syn_cap is not None:
                lp.row(nm("syn", n), [(X, 1.0)], -INF, syn_cap, n.id, "syn")
        if include_band:
            # IC range on public-markets exposure (physical + synthetic): lo * NAV <= L + X <= hi * NAV.
            pm = [(L, 1.0)] + ([(X, 1.0)] if dec else [])
            if hi_b is not None:
                lp.row(nm("band_hi", n), pm + nav_terms(-hi_b), -INF, hi_b * n.Y, n.id, "band_hi")
            lo_n = band_lo_value(v, n.regime, horizon=not dec)
            if lo_n is not None:
                # Elastic lower edge: exposure + shortfall >= lo * NAV, the shortfall priced in W~ (zero price in a
                # crisis year, where the CFP Red playbook sells long-only and uses P2S before any PE sale).
                lp.row(nm("band_lo", n), pm + nav_terms(-lo_n) + [(nm("sb", n), 1.0)], lo_n * n.Y, INF,
                       n.id, "band_lo")
        if not dec:
            # Terminal wealth W~ = cash + liquid + omega x PE + yield - debt - psi x unfunded - charges
            #                      + owner draws paid, each grown to the horizon at the static-allocation return.
            pth = path_ids(nodes, n)
            terms = [(nm("W", n), 1.0), (C, -1.0), (L, -1.0), (P, -om[n.regime]), (U, psi),
                     (BR, 1.0), (BN, 1.0)]
            terms += [(f"cut[{k}]", cpace) for k in pth[:-1]]
            terms += [(f"s8[{k}]", target_price(v, nodes[k].regime, horizon=nodes[k].stage == H)) for k in pth]
            terms += [(f"sb[{k}]", band_price(v, nodes[k].regime, horizon=nodes[k].stage == H)) for k in pth]
            const = n.Y + offsets.get(n.id, 0.0)
            for i in range(1, len(pth)):
                k, kp = nodes[pth[i]], nodes[pth[i - 1]]
                gd = accrual_factor(nodes, pth, i) * k.draw
                hk = A["lever_initial_margin"][kp.regime]
                terms += [(nm("C", kp), -gd), (nm("X", kp), -gd * hk), (nm("L", kp), -gd),
                          (nm("P", kp), -gd), (nm("BR", kp), gd), (nm("BN", kp), gd)]
                const += gd * kp.Y
            lp.row(nm("wealth", n), terms, const, const, n.id, "wealth")
            if mode == "utility":
                # Concave PWL utility: u <= U(w_k) + U'(w_k) (W/W0 - w_k) for every tangent point w_k.
                for k, wk in enumerate(tangents):
                    slope = crra_prime(wk, g)
                    lp.row(f"util[{n.id},{k}]", [(nm("u", n), 1.0), (nm("W", n), -slope / W0)],
                           -INF, crra(wk, g) - slope * wk, n.id, "util")
            if want_cvar:
                lp.row(nm("cvz", n), [(nm("z", n), 1.0), (nm("W", n), 1.0), ("eta", -1.0)],
                       0.0, INF, n.id, "cvz")
    if cvar_floor is not None and mode != "maxcvar":
        # Rockafellar-Uryasev: CVaR_alpha(W) = max_eta { eta - E[(eta - W)+] / alpha } >= floor.
        leaves = [n for n in nodes if n.stage == H]
        lp.row("cvar", [("eta", 1.0)] + [(f"z[{n.id}]", -n.prob / alpha) for n in leaves],
               cvar_floor, INF, None, "cvar")
    if mode == "phase1" and phase1_tier == "B":
        lp.row("tierA_cap", [(f"e[{n.id}]", n.prob) for n in nodes], -INF, u_tier_a + 1e-9 * W0, None, "cap")
    if (mode == "phase1" and phase1_tier == "A") or (mode != "phase1" and Lm.get("liquid_exposure_min_hard")):
        # Tier A ignores the IC range; the v1 sensitivity makes the lower edge hard. Either way no shortfall.
        for n in nodes:
            lp.ub[lp.vidx[f"sb[{n.id}]"]] = 0.0
    return lp


def solve_case(v, nodes, root, W0, lim, *, cvar_floor=None, offsets=None, tangents=None,
               allow_pe_sales=True, root_pe_zero=False):
    """Two-pass adaptive tangents (ARCHITECTURE.md 5.4): solve on a wide grid, then re-place the tangents
    on that solve's leaf-wealth range and solve again. Returns (lp, sol, tangents)."""
    K = int(v["objective"]["n_tangents"])
    H = max(n.stage for n in nodes)
    leaves = [n for n in nodes if n.stage == H]
    kw = dict(cvar_floor=cvar_floor, allow_pe_sales=allow_pe_sales, root_pe_zero=root_pe_zero, offsets=offsets)
    if tangents is None:
        lo, hi = v["objective"]["tangent_first_pass_range"]
        t1 = np.geomspace(lo, hi, K)
        lp1 = build_lp(v, nodes, root, W0, t1, lim, **kw)
        s1 = lp1.solve()
        if not s1.ok:
            return lp1, s1, t1
        w = np.array([s1.x(f"W[{n.id}]") / W0 for n in leaves])
        m0, m1 = S(v, "tangent_margins")
        tangents = np.geomspace(m0 * w.min(), m1 * w.max(), K)
    lp = build_lp(v, nodes, root, W0, tangents, lim, **kw)
    return lp, lp.solve(), np.asarray(tangents)


# =============================================================================================
# 6. Reading the solution: states, flows, decisions, labels, CFP stage, red events, duals and lambda
# =============================================================================================
ROW_TEXT = {
    "floor": "cash floor: cash after the owner draw >= 4% of NAV",
    "target": "8% cash target (elastic, priced)",
    "ltv": "NAV-loan capacity (pledge pool x LTV)",
    "rcf": "revolver availability cap",
    "expo": "exposure cap 1.30x NAV",
    "pace": "pacing cut at its maximum (core sleeve protected)",
    "band_hi": "IC range: public-markets exposure <= upper edge",
    "band_lo": "IC range: public-markets exposure >= lower edge",
    "syn": "synthetic-beta budget",
    "norev": "no new revolver drawing at the horizon",
    "nonav": "no new NAV-loan drawing at the horizon",
}
SHORT = {"floor": "cash floor", "target": "8% target", "ltv": "NAV-loan cap", "rcf": "revolver cap",
         "expo": "exposure cap", "pace": "pacing cut max", "band_hi": "IC range (upper)",
         "band_lo": "IC range (lower)", "syn": "synthetic budget", "norev": "no new revolver",
         "nonav": "no new NAV loan"}


def rnd(x, sig=12):
    """12 significant digits: about 1e-9 $bn on a $200bn book, so published balances re-add to the cent."""
    if isinstance(x, bool) or x is None:
        return x
    if isinstance(x, float):
        if not math.isfinite(x):
            return None
        return float(f"{x:.{sig}g}") if x != 0 else 0.0
    if isinstance(x, dict):
        return {k: rnd(val, sig) for k, val in x.items()}
    if isinstance(x, (list, tuple)):
        return [rnd(val, sig) for val in x]
    if isinstance(x, np.floating):
        return rnd(float(x), sig)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.ndarray):
        return rnd(x.tolist(), sig)
    return x


def cfp_stage(v, treasury_share, liquid_share):
    th = v["red_event"]["cfp_event_thresholds"]

    def band(x, cuts):
        for i, c in enumerate(cuts):
            if x >= c - 1e-9:
                return i
        return 3

    return STAGES[max(band(treasury_share, th["treasury_to_nav"]), band(liquid_share, th["liquid_share"]))]


def red_reasons(v, regime, stage_post, below_target, forced=False):
    """ADR-39 economic-substance test for a red-tier (PE) sale, read after the node's actions."""
    re_, disc = v["red_event"], v["actions"]["pe_secondary_discount"]
    bid_ratio = (1 - disc[regime]) / (1 - disc[re_["normal_regime"]])
    out = []
    if forced:
        out.append("forced recourse sale")
    if stage_post != "Green":
        out.append(f"event stage {stage_post}")
    if below_target:
        out.append("Treasury below the 8% target")
    if bid_ratio < 1 - re_["delta_max"] - 1e-12:
        out.append(f"bid {100 * bid_ratio:.0f}% of the normal bid")
    return out


def decision_values(v, n, dec, pr, p, sL, bL, sP, cv=0.0, uw=0.0, lev=0.0):
    """Decisions at a node, with borrowing split into REFINANCE (cash-out) and LEVER (funds new exposure).

    User definitions (ARCHITECTURE.md 4.8): REFINANCE raises cash against a holding without selling it; LEVER
    borrows to add exposure. P2S (physical converted to synthetic, exposure unchanged) is a REFINANCE of the
    liquid book; synthetic exposure added on top is LEVER; both are separate columns, so a label never has to
    guess. A revolver or NAV-loan draw pays first for this node's purchases (physical buys and the margin on
    synthetic LEVER): that part is LEVER, the rest is REFINANCE."""
    A, tau = v["actions"], v["actions"]["liquid_trade_cost"]
    hn = A["lever_initial_margin"][n.regime] if dec else 0.0
    dl = A["pe_secondary_discount"][n.regime]
    dX = p["X"] - pr.get("Xprev", 0.0)
    p2s = cv if dec else 0.0
    xcut = uw if dec else max(-dX, 0.0)      # at the horizon open synthetic positions close with the year
    dBR, dBN = p["BR"] - pr["BR"], p["BN"] - pr["BN"]
    drawR, drawN = max(dBR, 0.0), max(dBN, 0.0)
    borrow = drawR + drawN
    outlay = (1 + tau) * bL + hn * lev
    bp = min(borrow, outlay)
    shR = drawR / borrow if borrow > 0 else 0.0
    return {
        "sell_liquid": sL, "buy_liquid": bL, "sell_pe_nav": sP,
        "pe_sale_cash_proceeds": (1 - dl) * sP, "pe_sale_discount_loss": dl * sP,
        "unfunded_passed_to_buyer": A["unfunded_assumed_per_nav_sold"] * sP,
        "nav_loan_change": dBN, "revolver_change": dBR,
        "synthetic_notional": p["X"], "synthetic_change": dX, "p2s": p2s, "lever_synthetic": lev,
        "synthetic_closed": xcut,
        "borrowed_for_purchases": bp,
        "revolver_lever": bp * shR, "nav_loan_lever": bp * (1 - shR),
        "revolver_refinance": drawR - bp * shR, "nav_loan_refinance": drawN - bp * (1 - shR),
        "initial_margin_posted": hn * p["X"],
        "pace_cut": p["cut"],
        "new_commitments": (A["pacing_plan"] - p["cut"]) if dec else None,
        "cash_target_shortfall": p.get("s8", 0.0),
    }


def labels_for(dv, dec, eps):
    liq = []
    if dv["sell_liquid"] > eps:
        liq.append(f"SELL {dv['sell_liquid']:.2f}")
    if dv["p2s"] > eps:
        liq.append(f"REFINANCE {dv['p2s']:.2f} (P2S)")
    if dv["buy_liquid"] > eps:
        liq.append(f"BUY {dv['buy_liquid']:.2f}")
    if dv["lever_synthetic"] > eps:
        liq.append(f"LEVER {dv['lever_synthetic']:.2f} (synthetic)")
    if dec and dv["synthetic_closed"] > eps:
        liq.append(f"UNWIND P2S {dv['synthetic_closed']:.2f}")
    pe = []
    if dv["sell_pe_nav"] > eps:
        pe.append(f"SELL {dv['sell_pe_nav']:.2f}")
    if dv["nav_loan_refinance"] > eps:
        pe.append(f"REFINANCE {dv['nav_loan_refinance']:.2f} (NAV loan)")
    if dv["nav_loan_lever"] > eps:
        pe.append(f"LEVER {dv['nav_loan_lever']:.2f} (NAV loan pays for purchases)")
    if dv["nav_loan_change"] < -eps:
        pe.append(f"REPAY NAV loan {-dv['nav_loan_change']:.2f}")
    if dv["pace_cut"] > eps:
        pe.append(f"PACE-CUT {dv['pace_cut']:.2f}")
    cf = []
    if dv["revolver_refinance"] > eps:
        cf.append(f"REFINANCE {dv['revolver_refinance']:.2f} (revolver)")
    if dv["revolver_lever"] > eps:
        cf.append(f"LEVER {dv['revolver_lever']:.2f} (revolver pays for purchases)")
    if dv["revolver_change"] < -eps:
        cf.append(f"REPAY revolver {-dv['revolver_change']:.2f}")
    return {
        "liquid_book": " + ".join(liq) if liq else "HOLD",
        "pe_book": " + ".join(pe) if pe else "HOLD",
        "yield_book": "HOLD",
        "corporate_finance": " + ".join(cf) if cf else "NONE",
    }


def terminal_record(v, nodes, n, p, post, W0, offsets):
    """Terminal wealth and the horizon balance sheet of leaf n (same formula as the LP's wealth row)."""
    A, Tm, Lm = v["actions"], v["terminal"], v["limits"]
    H = n.stage
    pth = path_ids(nodes, n)
    om = Tm["pe_value_per_nav"][n.regime]
    nav_rep = p["C"] + p["L"] + p["P"] + n.Y - p["BR"] - p["BN"]
    econ = p["C"] + p["L"] + om * p["P"] + n.Y - p["BR"] - p["BN"]
    charges_pace = A["pacing_cut_cost"] * sum(post[k]["cut"] for k in pth[:-1])
    charges_t8 = sum(target_price(v, nodes[k].regime, horizon=nodes[k].stage == H) * post[k]["s8"] for k in pth)
    charges_band = sum(band_price(v, nodes[k].regime, horizon=nodes[k].stage == H) * post[k].get("sb", 0.0)
                       for k in pth)
    psi_u = Tm["unfunded_burden_per_dollar"] * p["U"]
    draws_acc = sum(accrual_factor(nodes, pth, i) * nodes[pth[i]].draw
                    * nav_post(v, nodes[pth[i - 1]], post[pth[i - 1]]) for i in range(1, len(pth)))
    off = offsets.get(n.id, 0.0)
    w_tilde = econ - charges_pace - charges_t8 - charges_band - psi_u + draws_acc + off
    return {
        "balance_sheet_NAV_reported": nav_rep, "economic_value": econ, "pacing_charges": charges_pace,
        "cash_target_charges": charges_t8, "ic_range_charges": charges_band, "unfunded_burden": psi_u,
        "draws_paid_accrued": draws_acc, "offset_constant": off,
        "W_tilde": w_tilde, "annualized_return": (w_tilde / W0) ** (1.0 / max(H, 1)) - 1.0 if w_tilde > 0 else None,
        "horizon_balance_sheet": {
            "treasury_to_nav": p["C"] / nav_rep, "liquid_share": p["L"] / nav_rep,
            "LR8_private_plus_unfunded_to_nav": (p["P"] + n.Y + p["U"]) / nav_rep,
            "debt": p["BR"] + p["BN"], "nav_vs_W0": nav_rep / W0 - 1.0,
        },
    }


def extract(v, nodes, root, lp: LP, s: Sol, lim, W0, offsets=None, has_duals=True):
    """Per-node report plus the post-decision states (for the naive rules, MPC and checks)."""
    A, Lm = v["actions"], v["limits"]
    f, f8, tau = Lm["cash_floor_frac"], Lm["cash_target_frac"], A["liquid_trade_cost"]
    eps, btol = S(v, "action_threshold_bn"), S(v, "binding_tolerance_bn")
    H = max(n.stage for n in nodes)
    offsets = offsets or {}
    mu0 = s.dual("cash[0]") if has_duals else float("nan")
    leaves_under = {n.id: [] for n in nodes}
    for m in nodes:
        if m.stage == H:
            for k in path_ids(nodes, m):
                leaves_under[k].append(m.id)
    post, pre, out = {}, {}, []
    for n in nodes:
        dec = n.stage < H

        def x(name):
            return s.x(f"{name}[{n.id}]")

        if n.parent is None:
            pr = dict(root)
            pr.setdefault("Xprev", 0.0)
        else:
            pr = pre_state(v, nodes[n.parent], n, post[n.parent], lim)
        pre[n.id] = pr
        p = dict(C=x("C"), L=x("L"), P=x("P"), U=x("U"), BR=x("BR"), BN=x("BN"), s8=x("s8"), sb=x("sb"),
                 X=x("X") if dec else 0.0, cut=x("cut") if dec else 0.0)
        post[n.id] = p
        hn = A["lever_initial_margin"][n.regime] if dec else 0.0
        dl = A["pe_secondary_discount"][n.regime]
        cv, uw, lv = (x("cv"), x("uw"), x("lev")) if dec else (0.0, 0.0, 0.0)
        dv = decision_values(v, n, dec, pr, p, x("sL"), x("bL"), x("sP"), cv, uw, lv)
        navp = nav_post(v, n, p)
        treas, lsh = p["C"] / navp, p["L"] / navp
        stage = cfp_stage(v, treas, lsh)
        reds = red_reasons(v, n.regime, stage, p["s8"] > btol) if dv["sell_pe_nav"] > eps else []
        # Conservation: rebuild the post-decision stocks from the pre-decision stocks and the trades.
        c_rebuilt = (pr["C"] + (1 - tau) * (dv["sell_liquid"] + cv) - (1 + tau) * (dv["buy_liquid"] + uw)
                     + dv["pe_sale_cash_proceeds"] + dv["nav_loan_change"] + dv["revolver_change"]
                     - dv["initial_margin_posted"])
        resid = {"cash": c_rebuilt - p["C"],
                 "liquid": pr["L"] - dv["sell_liquid"] + dv["buy_liquid"] - cv + uw - p["L"],
                 "synthetic": (pr.get("Xprev", 0.0) + cv - uw + lv - p["X"]) if dec else 0.0,
                 "pe": pr["P"] - dv["sell_pe_nav"] - p["P"],
                 "unfunded": pr["U"] - dv["unfunded_passed_to_buyer"] - p["U"]}
        rec = {
            "id": n.id, "stage": n.stage, "regime": n.regime, "regime_name": REGIME_NAME[n.regime],
            "path": n.path, "parent": n.parent, "children": list(n.children),
            "branch_probability": n.cond_prob, "probability": n.prob,
            "node_type": "decision" if dec else "horizon (settlement: repay, rebalance, restore limits)",
            "opening_state": {**{k: pr[k] for k in ("C", "L", "P", "U", "BR", "BN")}, "Y": n.Y,
                              "NAV": pr["C"] + pr["L"] + pr["P"] + n.Y - pr["BR"] - pr["BN"]},
            "year_rates": None if n.parent is None else {
                "liquid_return": n.rL, "pe_nav_return": n.rP, "valuation_adjustment_liquid": n.adjL,
                "valuation_adjustment_pe": n.adjP, "yield_cash": n.yY, "yield_nav_return": n.gY,
                "pe_distribution_rate": n.dist, "pe_call_rate": n.call, "owner_draw_rate": n.draw},
            "exogenous_flows": None if n.parent is None else
            year_flows(v, nodes[n.parent], n, post[n.parent], lim),
            "decisions": dv,
            "closing_state": {**{k: p[k] for k in ("C", "L", "P", "U", "BR", "BN", "X")},
                              "IM": hn * p["X"], "Y": n.Y, "NAV": navp, "cash_floor": f * navp,
                              "cash_target": f8 * navp, "s8": p["s8"], "sb": p["sb"]},
            "treasury_to_nav": treas, "liquid_share": lsh, "public_markets_share": (p["L"] + p["X"]) / navp,
            "cfp_stage": stage, "red_event_reasons": reds,
            "labels": labels_for(dv, dec, eps),
            "residuals": resid,
        }
        if not dec:
            rec["terminal"] = terminal_record(v, nodes, n, p, post, W0, offsets)
            rec["terminal"]["W_tilde_lp"] = s.x(f"W[{n.id}]")
            rec["terminal"]["horizon_balance_sheet"]["cfp_stage"] = stage
        if has_duals:
            mu = s.dual(f"cash[{n.id}]")
            fl = -s.dual(f"floor[{n.id}]")            # >= 0: value of $1 less required cash
            tg = -s.dual(f"target[{n.id}]")           # >= 0
            M = (1 - f) * fl + (1 - f8) * tg
            rec["duals"] = {
                "mu_cash_utility_per_bn": mu / OBJ_SCALE,
                "state_price_m": mu / (n.prob * mu0),
                "liquidity_premium_lambda": M / (mu - M) if mu - M > 0 else None,
                "liquidity_dual_mass_M_utility": M / OBJ_SCALE,
                "M_from_floor": (1 - f) * fl / OBJ_SCALE, "M_from_target": (1 - f8) * tg / OBJ_SCALE,
            }
            binding = []
            for i, (rn, kind) in enumerate(zip(lp.rnode, lp.rkind)):
                if rn != n.id or kind not in ROW_TEXT:
                    continue
                act, lo, hi = s.rv[i], lp.rlo[i], lp.rhi[i]
                at_lo = lo > -INF and abs(act - lo) <= btol
                at_hi = hi < INF and abs(act - hi) <= btol
                if kind == "target":
                    at_lo = p["s8"] > btol or at_lo
                if kind == "band_lo":
                    at_lo = p["sb"] > btol or at_lo
                if not (at_lo or at_hi):
                    continue
                relax = -s.rd[i] if at_lo else s.rd[i]
                binding.append({
                    "row": lp.rnames[i], "kind": kind, "constraint": ROW_TEXT[kind],
                    "shadow_value_node_usd_per_usd": relax / mu,
                    "shadow_value_root_usd_per_usd": relax / mu0,
                })
            rec["binding_constraints"] = binding
            if dec:
                # The cut column's reduced cost = (liquidity and return value of cutting $1) - c_PACE x S,
                # with S the value of $1 of terminal wealth on the leaves below n. So the franchise cost at
                # which a cut would start to pay is c_PACE + reduced cost / S.
                Ssum = sum(s.dual(f"wealth[{m}]") for m in leaves_under[n.id])
                dcut = float(s.cd[lp.vidx[f"cut[{n.id}]"]])
                rec["duals"]["pacing_cut_break_even_cost_per_usd"] = (
                    A["pacing_cut_cost"] + dcut / Ssum if Ssum > 0 else None)
        out.append(rec)
    return out, post, pre


def tail_cvar(values, probs, alpha):
    """Lower-tail CVaR_alpha of a discrete distribution."""
    order = np.argsort(values)
    acc, tot = 0.0, 0.0
    for i in order:
        take = min(probs[i], alpha - acc)
        if take <= 0:
            break
        tot += take * float(values[i])
        acc += take
    return float(tot / alpha)


def summarize(v, nodes, rep, W0, cvar_floor=None):
    g, alpha = v["objective"]["crra_gamma"], v["limits"]["cvar_alpha"]
    eps = S(v, "action_threshold_bn")
    H = max(n.stage for n in nodes)
    leaves = [n for n in nodes if n.stage == H]
    byid = {r["id"]: r for r in rep}
    pr = np.array([n.prob for n in leaves])
    wt = np.array([byid[n.id]["terminal"]["W_tilde"] for n in leaves])
    nav = np.array([byid[n.id]["terminal"]["balance_sheet_NAV_reported"] for n in leaves])
    hb = [byid[n.id]["terminal"]["horizon_balance_sheet"] for n in leaves]
    ann = (wt / W0) ** (1.0 / H) - 1.0
    eu = float(np.sum(pr * crra(wt / W0, g)))
    w_ce = ((1.0 - g) * eu) ** (1.0 / (1.0 - g))
    cvar_w = tail_cvar(wt, pr, alpha)

    def on_path(leaf, test):
        return any(test(byid[k]) for k in path_ids(nodes, leaf))

    def p_path(test):
        return float(sum(n.prob for n in leaves if on_path(n, test)))

    d_ = lambda r: r["decisions"]
    fire = lambda r: r["regime"] == "C" and d_(r)["sell_pe_nav"] > eps
    anysale = lambda r: d_(r)["sell_pe_nav"] > eps
    red = lambda r: bool(r.get("red_event_reasons"))
    revd = lambda r: r["closing_state"]["BR"] > eps
    navl = lambda r: r["closing_state"]["BN"] > eps
    cut = lambda r: d_(r)["pace_cut"] > eps
    lev = lambda r: d_(r)["lever_synthetic"] > eps or d_(r)["borrowed_for_purchases"] > eps
    p2s = lambda r: d_(r)["p2s"] > eps
    below8 = lambda r: r["closing_state"]["s8"] > eps
    worse_amber = lambda r: r["cfp_stage"] in ("Red", "Black")
    lev_below_amber = lambda r: lev(r) and worse_amber(r)
    borrowed_buy = lambda r: d_(r)["borrowed_for_purchases"] > eps
    floorb = lambda r: r["stage"] >= 1 and any(b["kind"] == "floor" for b in r.get("binding_constraints", []))
    stage_dist = {}
    for t in range(0, H + 1):
        stage_dist[str(t)] = {st: float(sum(r["probability"] for r in rep if r["stage"] == t and r["cfp_stage"] == st))
                              for st in STAGES}
    exp_draws = float(sum(r["probability"] * -r["exogenous_flows"]["owner_draw"]
                          for r in rep if r["exogenous_flows"] is not None))
    dist_table = sorted(({"path": n.path, "probability": n.prob, "W_tilde": byid[n.id]["terminal"]["W_tilde"],
                          "annualized_return": byid[n.id]["terminal"]["annualized_return"],
                          **{k: byid[n.id]["terminal"]["horizon_balance_sheet"][k]
                             for k in ("treasury_to_nav", "liquid_share", "LR8_private_plus_unfunded_to_nav",
                                       "debt", "nav_vs_W0")},
                          "cfp_stage": byid[n.id]["cfp_stage"]} for n in leaves),
                        key=lambda d: d["W_tilde"])
    cum = 0.0
    for d in dist_table:
        cum += d["probability"]
        d["cumulative_probability"] = cum
    lo_b = band_lo_value(v, "N")          # the IC range's lower edge in a normal year
    out = {
        "expected_terminal_NAV_reported": float(np.sum(pr * nav)),
        "expected_W_tilde": float(np.sum(pr * wt)),
        "expected_annualized_return": float(np.sum(pr * ann)),
        "median_annualized_return": float(next(d["annualized_return"] for d in dist_table
                                               if d["cumulative_probability"] >= 0.5)),
        "certainty_equivalent_W_tilde": w_ce * W0,
        "certainty_equivalent_annualized_return": w_ce ** (1.0 / H) - 1.0,
        "expected_utility_exact_crra": eu,
        "cvar10_W_tilde": cvar_w,
        "cvar10_annualized_return": (cvar_w / W0) ** (1.0 / H) - 1.0,
        "cvar_floor_W_tilde": cvar_floor,
        "P_annualized_return_ge_10pct": float(np.sum(pr[ann >= 0.10 - 1e-12])),
        "P_annualized_return_ge_7pct": float(np.sum(pr[ann >= 0.07 - 1e-12])),
        "P_annualized_return_lt_0": float(np.sum(pr[ann < 0.0])),
        "P_any_pe_sale": p_path(anysale),
        "P_any_pe_fire_sale_at_crisis_discount": p_path(fire),
        "P_red_event": p_path(red),
        "P_revolver_drawn_somewhere": p_path(revd),
        "P_nav_loan_used_somewhere": p_path(navl),
        "P_pacing_cut_somewhere": p_path(cut),
        "P_lever_somewhere": p_path(lev),
        "P_borrowed_purchase_somewhere": p_path(borrowed_buy),
        "P_lever_while_red_or_black": p_path(lev_below_amber),
        "P_p2s_somewhere": p_path(p2s),
        "P_below_8pct_target_somewhere": p_path(below8),
        "P_cash_floor_binds_somewhere_t1_to_t3": p_path(floorb),
        "P_cfp_red_or_black_somewhere": p_path(worse_amber),
        "cfp_stage_probability_by_t": stage_dist,
        "expected_owner_draws_paid_total": exp_draws,
        "expected_pe_sale_discount_losses": float(sum(r["probability"] * d_(r)["pe_sale_discount_loss"] for r in rep)),
        "expected_pacing_cuts_total": float(sum(r["probability"] * d_(r)["pace_cut"] for r in rep)),
        "expected_liquid_turnover_decision_nodes": float(sum(r["probability"] * (d_(r)["sell_liquid"] + d_(r)["buy_liquid"])
                                                             for r in rep if r["stage"] < H)),
        "P_horizon_liquid_share_below_lower_edge": (float(sum(n.prob for n, h_ in zip(leaves, hb)
                                                               if h_["liquid_share"] < lo_b - 1e-9))
                                                     if lo_b is not None else None),
        "P_horizon_LR8_above_0p80": float(sum(n.prob for n, h_ in zip(leaves, hb)
                                              if h_["LR8_private_plus_unfunded_to_nav"] > 0.80 + 1e-12)),
        "P_horizon_NAV_below_80pct_of_W0": float(sum(n.prob for n, h_ in zip(leaves, hb) if h_["nav_vs_W0"] < -0.20)),
        "expected_horizon_debt": float(sum(n.prob * h_["debt"] for n, h_ in zip(leaves, hb))),
        "terminal_distribution": dist_table,
    }
    return out


def strip(summ):
    return {k: val for k, val in summ.items() if k != "terminal_distribution"}


def compact_node(r):
    """Short per-node view used in comparisons and RESULTS.md."""
    d = r["decisions"]
    return {"path": r["path"], "probability": r["probability"], "labels": r["labels"],
            **{k: d[k] for k in DEC_KEYS}, "borrowed_for_purchases": d["borrowed_for_purchases"],
            "closing_cash": r["closing_state"]["C"], "treasury_to_nav": r["treasury_to_nav"],
            "cfp_stage": r["cfp_stage"], "red_event_reasons": r.get("red_event_reasons", []),
            "lambda": r.get("duals", {}).get("liquidity_premium_lambda"),
            "state_price_m": r.get("duals", {}).get("state_price_m")}


# =============================================================================================
# 7. Cases: the root red-tier rule, Phase I, the naive rules, the closed loop
# =============================================================================================
def root_state_t0(v):
    b = v["balance_sheet_t0"]
    return dict(C=b["cash_hqla"], L=b["liquid_book"], P=b["pe_book_nav"], U=b["pe_unfunded"],
                BR=0.0, BN=0.0, Y=b["yield_book_nav"], Xprev=0.0)


def saa_weights(v):
    b = v["balance_sheet_t0"]
    tot = b["cash_hqla"] + b["liquid_book"] + b["pe_book_nav"] + b["yield_book_nav"]
    return {"C": b["cash_hqla"] / tot, "L": b["liquid_book"] / tot, "P": b["pe_book_nav"] / tot,
            "Y": b["yield_book_nav"] / tot}


def opening_stage(v, st):
    nav = st["C"] + st["L"] + st["P"] + st["Y"] - st["BR"] - st["BN"]
    return cfp_stage(v, st["C"] / nav, st["L"] / nav), nav


@dataclass
class Case:
    lp: LP
    s: Sol
    tan: np.ndarray
    rep: list
    post: dict
    pre: dict
    summ: dict
    root_pe_rule: str
    forced: "Case | None" = None


def run_case(v, nodes, root, W0, lim, *, cvar_floor=None, offsets=None, tangents=None, hold_root_pe=False):
    """Solve the tree and apply the root red-tier SELL rule (ADR-39; ARCHITECTURE.md 5.4): if today's event
    stage is Amber or worse, or the root's PE sale would be a red event, the root PE SELL is held at zero and
    the version that allows it is kept as the forced re-solve, so the IC sees what the sale would add.
    hold_root_pe=True holds it at zero in any case (used when a downside floor is set: a tail row is never met
    with a red-tier sale without the forced re-solve, verify_finance.md M7)."""
    eps = S(v, "action_threshold_bn")
    stage0, _ = opening_stage(v, root)
    if hold_root_pe and stage0 == "Green":
        stage0 = "Green (root PE sale held at zero because a downside floor is set)"

    def one(root_zero):
        lp, s, tan = solve_case(v, nodes, root, W0, lim, cvar_floor=cvar_floor, offsets=offsets,
                                tangents=tangents, root_pe_zero=root_zero)
        if not s.ok:
            return None, (lp, s, tan)
        rep, post, pre = extract(v, nodes, root, lp, s, lim, W0, offsets=offsets)
        return Case(lp, s, tan, rep, post, pre, summarize(v, nodes, rep, W0, cvar_floor), ""), (lp, s, tan)

    if stage0 != "Green":
        held, raw = one(True)
        forced, _ = one(False)
        if held is not None:
            held.root_pe_rule = (f"held at zero: today's event stage is {stage0}" if not stage0.startswith("Green")
                                 else "held at zero: a downside floor is set")
            held.forced = forced
        return held, raw
    free, raw = one(False)
    if free is None:
        return None, raw
    r0 = free.rep[0]
    if r0["decisions"]["sell_pe_nav"] > eps and r0["red_event_reasons"]:
        held, raw2 = one(True)
        if held is None:
            free.root_pe_rule = ("kept: the root PE sale is a red event (" + "; ".join(r0["red_event_reasons"])
                                 + ") but the tree is infeasible without it")
            return free, raw
        held.root_pe_rule = ("held at zero: the root PE sale would be a red event ("
                             + "; ".join(r0["red_event_reasons"]) + ")")
        held.forced = free
        return held, raw2
    free.root_pe_rule = ("allowed: no PE sale at the root" if r0["decisions"]["sell_pe_nav"] <= eps
                         else "allowed: the root PE sale passes the economic-substance test (planned, not red)")
    return free, raw


def run_phase1(v, nodes, root, W0, lim):
    """Phase I (ARCHITECTURE.md 5.5) with reversible levers only (no PE sale anywhere).
    Tier A: Tier-1A cash floor at every node. Tier B, reported separately: the IC range's lower edge, holding
    tier A at its optimum (the architecture's Phase I tiers carry no allocation range)."""
    lpA = build_lp(v, nodes, root, W0, [], lim, allow_pe_sales=False, mode="phase1", phase1_tier="A")
    sA = lpA.solve()
    if not sA.ok:
        return {"status": sA.status, "u_star_floor_bn": None, "u_star_ic_range_bn": None,
                "short_floor": {}, "short_ic_range": {}, "reading": f"Phase I LP {sA.status}"}
    uA = -sA.obj / OBJ_SCALE
    short_f = {n.path: sA.x(f"e[{n.id}]") for n in nodes if sA.x(f"e[{n.id}]") > 1e-7}
    lpB = build_lp(v, nodes, root, W0, [], lim, allow_pe_sales=False, mode="phase1", phase1_tier="B",
                   u_tier_a=uA)
    sB = lpB.solve()
    uB = -sB.obj / OBJ_SCALE if sB.ok else None
    short_b = ({n.path: sB.x(f"sb[{n.id}]") for n in nodes if sB.x(f"sb[{n.id}]") > 1e-7
                and band_price(v, n.regime, horizon=n.stage == max(m.stage for m in nodes)) > 0}
               if sB.ok else {})
    if not short_f and not short_b:
        reading = "every hard row can be met without any PE sale (u* = 0)"
    elif short_f:
        reading = "the cash floor cannot be met everywhere without a PE sale (structural deficit)"
    else:
        reading = "the cash floor can be met without PE sales, but the IC range's lower edge cannot everywhere"
    return {"status": sA.status, "u_star_floor_bn": uA, "u_star_ic_range_bn": uB,
            "short_floor": short_f, "short_ic_range": short_b, "reading": reading}


def simulate_naive(v, nodes, root, target, W0, lim=0.0, revolver_first=False):
    """Naive Treasury rule on the same tree, with the same flow equations, limits and charges as the program.

    At every node, in this order:
      (1) repay the revolver down to its availability if a crisis cut it (revolver variant);
      (2) trim the liquid book to the IC range's upper edge;
      (3) if own liquidity is below `target` x NAV, sell liquid assets, but only down to the IC range's lower
          edge (the edge is free in a crisis year, as for the program);
      (4) if the 4% hard floor still fails: draw the revolver (revolver variant; the CFP Red playbook's 'lines
          drawn'), then sell liquid below the range, and only then sell PE at the regime's discount (a forced,
          red sale);
      (5) if own liquidity is above target: repay the revolver first (variant), then sweep the surplus into the
          liquid book up to the upper edge (decision nodes only);
      (6) if the liquid book is below the lower edge where it is priced, buy it back with cash above the target.
    Shortfalls below the 8% target and the IC range are charged at the program's prices. The rule never uses a
    NAV loan, P2S, LEVER or a pacing cut, and it has no look-ahead."""
    A, Lm = v["actions"], v["limits"]
    f, f8, tau = Lm["cash_floor_frac"], Lm["cash_target_frac"], A["liquid_trade_cost"]
    hi_b = Lm.get("liquid_exposure_max_frac")
    net_target = Lm.get("cash_target_basis", "gross") == "net_of_facility_draws"
    eps = S(v, "action_threshold_bn")
    H = max(n.stage for n in nodes)
    post, rep, infeasible, breaches = {}, [], [], []
    for n in nodes:
        dec = n.stage < H
        if n.parent is None:
            pr = dict(root)
            pr.setdefault("Xprev", 0.0)
        else:
            pr = pre_state(v, nodes[n.parent], n, post[n.parent], lim)
        C, Lq, P, U, BR = pr["C"], pr["L"], pr["P"], pr["U"], pr["BR"]
        Y = n.Y
        dl = A["pe_secondary_discount"][n.regime]
        avail = A["revolver_availability"][n.regime] * lim
        lo_all = band_lo_value(v, n.regime, horizon=not dec)
        lo_n = lo_all if (lo_all is not None and band_price(v, n.regime, horizon=not dec) > 0) else None
        may_buy = n.regime not in set(A.get("no_liquid_purchases_in_regimes") or [])
        sL = bL = sP = 0.0
        nav = lambda: C + Lq + P + Y - BR
        own = lambda: C - BR if net_target else C
        # (1) forced paydown
        if BR > avail + 1e-12:
            C -= BR - avail
            BR = avail
        # (2) upper edge: L - s <= hi (NAV - tau s)
        if hi_b is not None and Lq > hi_b * nav() + 1e-12:
            s_ = (Lq - hi_b * nav()) / (1 - hi_b * tau)
            sL += s_
            C, Lq = C + (1 - tau) * s_, Lq - s_
        need = target * nav() - own()
        if need > 1e-12:
            # (3) liquid sales inside the range to restore the target: own + (1 - tau) s = target (NAV - tau s)
            room = Lq if lo_n is None else max(0.0, (Lq - lo_n * nav()) / (1 - lo_n * tau))
            s_ = min(need / (1 - tau + target * tau), room, Lq)
            sL += s_
            C, Lq = C + (1 - tau) * s_, Lq - s_
        # (4) the hard floor
        short = f * nav() - C
        if short > 1e-12 and revolver_first and dec and avail > BR:
            dr = min(short, avail - BR)
            C, BR = C + dr, BR + dr
            short = f * nav() - C
        if short > 1e-12 and Lq > 0:
            s_ = min(short / (1 - tau + f * tau), Lq)
            sL += s_
            C, Lq = C + (1 - tau) * s_, Lq - s_
            short = f * nav() - C
        if short > 1e-12:
            sp_ = short / (1 - dl + f * dl)
            if sp_ > P:
                infeasible.append(n.path)
                sp_ = P
            sP += sp_
            C, P, U = C + (1 - dl) * sp_, P - sp_, U - A["unfunded_assumed_per_nav_sold"] * sp_
        # (5) surplus
        surplus = own() - target * nav()
        if surplus > 1e-12:
            if revolver_first and BR > 0:
                rp = min(BR, max(0.0, C - target * nav()), C - f * nav())
                if rp > 0:
                    C, BR = C - rp, BR - rp
                surplus = own() - target * nav()
            if dec and may_buy and surplus > 1e-12 and C - f * nav() > 1e-12:
                room = INF if hi_b is None else max(0.0, (hi_b * nav() - Lq) / (1 + hi_b * tau))
                cash_room = (C - target * nav()) / (1 + tau - target * tau)
                b_ = max(0.0, min(surplus / (1 + tau - target * tau), room, cash_room))
                bL += b_
                C, Lq = C - (1 + tau) * b_, Lq + b_
        # (6) lower edge restore with cash above the target
        if may_buy and lo_n is not None and Lq < lo_n * nav() - 1e-12:
            want = (lo_n * nav() - Lq) / (1 + lo_n * tau)
            cash_room = max(0.0, (own() - target * nav()) / (1 + tau - target * tau))
            b_ = min(want, cash_room)
            bL += b_
            C, Lq = C - (1 + tau) * b_, Lq + b_
        # Net the two directions of liquid trading into one (no simultaneous buy and sell in the report).
        if sL > 0 and bL > 0:
            m = min(sL, bL)
            sL, bL = sL - m, bL - m
            C += 2 * tau * m          # the round trip did not happen, so its cost is not paid
        p = dict(C=C, L=Lq, P=P, U=U, BR=BR, BN=0.0, X=0.0, cut=0.0)
        navp = nav_post(v, n, p)
        p["s8"] = max(0.0, f8 * navp - (C - BR if net_target else C))
        p["sb"] = max(0.0, lo_all * navp - Lq) if lo_all is not None else 0.0
        post[n.id] = p
        share = (p["L"]) / navp
        if hi_b is not None and share > hi_b + 1e-9:
            breaches.append({"path": n.path, "probability": n.prob, "liquid_exposure_share": share})
        dv = decision_values(v, n, dec, pr, p, sL, bL, sP)
        treas, lsh = p["C"] / navp, p["L"] / navp
        stage = cfp_stage(v, treas, lsh)
        rec = {"id": n.id, "stage": n.stage, "regime": n.regime, "path": n.path, "probability": n.prob,
               "opening_state": {**{k: pr[k] for k in ("C", "L", "P", "U", "BR")},
                                 "NAV": pr["C"] + pr["L"] + pr["P"] + Y - pr["BR"]},
               "exogenous_flows": None if n.parent is None else
               year_flows(v, nodes[n.parent], n, post[n.parent], lim),
               "decisions": dv, "closing_state": {**p, "NAV": navp},
               "treasury_to_nav": treas, "liquid_share": lsh, "cfp_stage": stage,
               "red_event_reasons": (red_reasons(v, n.regime, stage, p["s8"] > 1e-9, forced=True)
                                     if sP > eps else []),
               "labels": labels_for(dv, dec, eps),
               "binding_constraints": ([{"row": f"floor[{n.id}]", "kind": "floor", "constraint": ROW_TEXT["floor"]}]
                                       if p["C"] <= f * navp + 1e-9 else [])}
        if not dec:
            rec["terminal"] = terminal_record(v, nodes, n, p, post, W0, {})
            rec["terminal"]["horizon_balance_sheet"]["cfp_stage"] = stage
        rep.append(rec)
    return rep, post, infeasible, breaches


def settle_leaf(v, leaf: Node, pre: dict, lim, offset):
    """Closed-loop settlement at t = 3: the same horizon rows as the tree's leaves, on a one-node program
    that maximizes W~ (any increasing utility picks the same settlement)."""
    node = Node(0, 0, leaf.regime, leaf.path, None, 1.0, 1.0, Y=leaf.Y)
    lp = build_lp(v, [node], pre, 1.0, [], lim, mode="settle", offsets={0: offset})
    s = lp.solve()
    return [node], lp, s


def closed_loop(v, nodes, root, W0, lim, main: Case, saa):
    """The rolling policy on the tree (ARCHITECTURE.md 5.9): execute the root decision; at every t = 1 and t = 2
    node re-solve a fresh tree of the same depth from the realized state, with the same rules (the root red-tier
    rule included), and execute only its first decision; at t = 3 settle with the horizon rows. Returns
    node records shaped like extract() and the re-solve details."""
    H = max(n.stage for n in nodes)
    hz = int(v["mpc"]["horizon"])
    A, Lm = v["actions"], v["limits"]
    post = {0: main.post[0]}
    recs = {0: main.rep[0]}
    details = []
    for t in range(1, H):
        for n in (m for m in nodes if m.stage == t):
            par = nodes[n.parent]
            st = pre_state(v, par, n, post[par.id], lim)
            stage0, W1 = opening_stage(v, st)
            sub = build_tree(v, n.regime, hz, st["Y"], saa)
            case, raw = run_case(v, sub, st, W1, lim)
            note = ""
            if case is None:
                # Re-solve infeasible: Phase I measures the deficit; the program then allows a root PE sale.
                ph = run_phase1(v, sub, st, W1, lim)
                note = f"infeasible as specified ({raw[1].status}); Phase I u* floor = {ph['u_star_floor_bn']}"
                lp_, s_, tan_ = solve_case(v, sub, st, W1, lim)
                rep_, post_, pre_ = extract(v, sub, st, lp_, s_, lim, W1)
                case = Case(lp_, s_, tan_, rep_, post_, pre_, summarize(v, sub, rep_, W1), "forced (infeasible)")
            r_new = copy.deepcopy(case.rep[0])
            # Re-key the record to the original tree's node.
            r_new.update({"id": n.id, "stage": n.stage, "path": n.path, "parent": n.parent,
                          "children": list(n.children), "branch_probability": n.cond_prob,
                          "probability": n.prob})
            r_new["exogenous_flows"] = year_flows(v, par, n, post[par.id], lim)
            r_new["opening_state"] = {**{k: st[k] for k in ("C", "L", "P", "U", "BR", "BN")}, "Y": n.Y, "NAV": W1}
            r_new.pop("terminal", None)
            p_new = dict(case.post[0])
            post[n.id] = p_new
            recs[n.id] = r_new
            plan = next(r for r in main.rep if r["id"] == n.id)
            details.append({
                "path": n.path, "stage": n.stage, "probability": n.prob, "opening_event_stage": stage0,
                "opening_state": r_new["opening_state"], "root_pe_rule": case.root_pe_rule, "note": note,
                "plan_made_at_t0_on_this_path": compact_node(plan) if t == 1 else None,
                "resolved_decision": compact_node(case.rep[0]) | {"path": n.path},
                "resolved_binding": case.rep[0].get("binding_constraints", []),
                "resolved_window_summary": strip(case.summ),
                "forced_resolve_root_pe": (None if case.forced is None else
                                           {"labels": case.forced.rep[0]["labels"],
                                            "ce_gain_bn": case.forced.summ["certainty_equivalent_W_tilde"]
                                            - case.summ["certainty_equivalent_W_tilde"]}),
            })
    # t = 3: settle each leaf with the horizon rows.
    for n in (m for m in nodes if m.stage == H):
        par = nodes[n.parent]
        st = pre_state(v, par, n, post[par.id], lim)
        pth = path_ids(nodes, n)
        draws_acc = sum(accrual_factor(nodes, pth, i) * nodes[pth[i]].draw
                        * nav_post(v, nodes[pth[i - 1]], post[pth[i - 1]]) for i in range(1, len(pth)))
        charges = sum(A["pacing_cut_cost"] * post[k]["cut"]
                      + target_price(v, nodes[k].regime) * post[k]["s8"]
                      + band_price(v, nodes[k].regime) * post[k].get("sb", 0.0) for k in pth[:-1])
        one, lp_, s_ = settle_leaf(v, n, st, lim, draws_acc - charges)
        assert s_.ok, f"closed-loop settlement at {n.path}: {s_.status}"
        rep1, post1, _ = extract(v, one, st, lp_, s_, lim, W0, offsets={0: draws_acc - charges}, has_duals=False)
        r = rep1[0]
        r.update({"id": n.id, "stage": n.stage, "path": n.path, "parent": n.parent, "children": [],
                  "branch_probability": n.cond_prob, "probability": n.prob,
                  "node_type": "horizon (settlement: repay, rebalance, restore limits)"})
        r["exogenous_flows"] = year_flows(v, par, n, post[par.id], lim)
        # Annualize over the full horizon (the one-node program sees a horizon of 0 years).
        r["terminal"]["annualized_return"] = (r["terminal"]["W_tilde"] / W0) ** (1.0 / H) - 1.0
        r["terminal"]["draws_paid_accrued"] = draws_acc
        r["terminal"]["path_charges"] = charges
        post[n.id] = post1[0]
        recs[n.id] = r
    rep = [recs[n.id] for n in nodes]
    return rep, details


# =============================================================================================
# 8. Checks on the duals: finite differences, the carry re-solve and kinks
# =============================================================================================
def row_fd(lp: LP, base_obj: float, row: str, step: float):
    i = lp.ridx[row]
    lo0, hi0 = lp.rlo[i], lp.rhi[i]
    vals = {}
    for sgn in (+1, -1):
        lo = lo0 + sgn * step if lo0 > -INF else lo0
        hi = hi0 + sgn * step if hi0 < INF else hi0
        lp.set_row_bounds(row, lo, hi)
        s = lp.solve()
        vals[sgn] = s.obj if s.ok else float("nan")
    lp.set_row_bounds(row, lo0, hi0)
    return (vals[1] - base_obj) / step, (base_obj - vals[-1]) / step


def dual_checks(v, nodes, case: Case):
    """(1) Finite differences on every decision node's cash row, on binding floor/target rows and on a few
    leaves; (2) lambda from a direct carry re-solve (inject $delta at the node and tighten the floor and the
    target by (1 - f) delta and (1 - f8) delta, so the dollar cannot relieve them); (3) kink probes at
    +/- kink_probe_bn of cash."""
    lp, s = case.lp, case.s
    f, f8 = v["limits"]["cash_floor_frac"], v["limits"]["cash_target_frac"]
    step, probe, ktol = S(v, "fd_step_bn"), S(v, "kink_probe_bn"), S(v, "kink_rel_tol")
    H = max(n.stage for n in nodes)
    fd, carry, kinks = [], [], []
    rows = [f"cash[{n.id}]" for n in nodes if n.stage < H]
    rows += [f"cash[{n.id}]" for n in nodes if n.stage == H][:: max(1, len([1 for n in nodes if n.stage == H]) // 5)]
    for r in case.rep:
        for b in r.get("binding_constraints", []):
            if b["kind"] in ("floor", "target", "band_lo", "rcf", "syn", "ltv") and r["stage"] < H:
                rows.append(b["row"])
    seen = set()
    for row in rows:
        if row in seen:
            continue
        seen.add(row)
        right, left = row_fd(lp, s.obj, row, step)
        du = s.dual(row)
        fd.append({"row": row, "lp_dual": du / OBJ_SCALE, "fd_right": right / OBJ_SCALE, "fd_left": left / OBJ_SCALE,
                   "rel_err_vs_nearest_side": min(abs(right - du), abs(left - du)) / max(abs(du), 1e-12)
                   if abs(du) > 1e-12 else min(abs(right), abs(left))})
    for r in case.rep:
        if r["stage"] >= H:
            continue
        nid = r["id"]
        cr, fr, tr_ = f"cash[{nid}]", f"floor[{nid}]", f"target[{nid}]"
        saved = {k: (lp.rlo[lp.ridx[k]], lp.rhi[lp.ridx[k]]) for k in (cr, fr, tr_)}
        lp.set_row_bounds(cr, saved[cr][0] + step, saved[cr][1] + step)
        lp.set_row_bounds(fr, saved[fr][0] + (1 - f) * step, saved[fr][1])
        lp.set_row_bounds(tr_, saved[tr_][0] + (1 - f8) * step, saved[tr_][1])
        s2 = lp.solve()
        for k, (lo, hi) in saved.items():
            lp.set_row_bounds(k, lo, hi)
        mu = s.dual(cr)
        c_val = (s2.obj - s.obj) / step
        lam_dual = r["duals"]["liquidity_premium_lambda"]
        lam_resolve = (mu - c_val) / c_val if c_val > 0 else None
        carry.append({"path": r["path"], "lambda_from_duals": lam_dual, "lambda_from_carry_resolve": lam_resolve,
                      "abs_diff": (abs(lam_dual - lam_resolve) if lam_dual is not None and lam_resolve is not None
                                   else None)})
        right, left = row_fd(lp, s.obj, cr, probe)
        rel = abs(left - right) / max(abs(mu), 1e-12)
        kinks.append({"path": r["path"], "mu": mu / OBJ_SCALE, "slope_plus_probe": right / OBJ_SCALE,
                      "slope_minus_probe": left / OBJ_SCALE, "relative_gap": rel, "near_kink": rel > ktol})
    return fd, carry, kinks


# =============================================================================================
# 9. Horizon test, sensitivities, downside floors, time consistency, limit checks
# =============================================================================================
def p_paths(nodes, rep, test, tmax=None):
    """Probability of the leaves whose path meets `test` at some node of stage <= tmax."""
    H = max(n.stage for n in nodes)
    byid = {r["id"]: r for r in rep}
    tot = 0.0
    for leaf in (n for n in nodes if n.stage == H):
        if any(test(byid[k]) and (tmax is None or nodes[k].stage <= tmax) for k in path_ids(nodes, leaf)):
            tot += leaf.prob
    return float(tot)


def case_brief(v, nodes, case, tmax=None):
    """The handful of numbers the comparison tables use."""
    if case is None:
        return None
    eps = S(v, "action_threshold_bn")
    rep = case.rep
    H = max(n.stage for n in nodes)
    lam = [r["duals"]["liquidity_premium_lambda"] for r in rep
           if r["stage"] < H and r["duals"]["liquidity_premium_lambda"] is not None]
    d_ = lambda r: r["decisions"]
    out = {
        "root_labels": rep[0]["labels"], "root_pe_rule": case.root_pe_rule,
        "root_lambda": rep[0]["duals"]["liquidity_premium_lambda"],
        "root_treasury_to_nav": rep[0]["treasury_to_nav"],
        "ce": case.summ["certainty_equivalent_W_tilde"],
        "ce_annualized": case.summ["certainty_equivalent_annualized_return"],
        "expected_annualized": case.summ["expected_annualized_return"],
        "cvar10_annualized": case.summ["cvar10_annualized_return"],
        "P_pe_sale": p_paths(nodes, rep, lambda r: d_(r)["sell_pe_nav"] > eps, tmax),
        "P_fire_sale": p_paths(nodes, rep, lambda r: r["regime"] == "C" and d_(r)["sell_pe_nav"] > eps, tmax),
        "P_red_event": p_paths(nodes, rep, lambda r: bool(r.get("red_event_reasons")), tmax),
        "P_revolver_drawn": p_paths(nodes, rep, lambda r: r["closing_state"]["BR"] > eps, tmax),
        "P_pacing_cut": p_paths(nodes, rep, lambda r: d_(r)["pace_cut"] > eps, tmax),
        "max_lambda_decision_nodes": max(lam) if lam else None,
        "forced_root_pe": (None if case.forced is None else {
            "labels": case.forced.rep[0]["labels"],
            "ce_gain_bn": case.forced.summ["certainty_equivalent_W_tilde"] - case.summ["certainty_equivalent_W_tilde"]}),
    }
    for pth in ("D>D", "D>C", "D>C>C"):
        r = next((x for x in rep if x["path"] == pth and x["stage"] < H), None)
        if r is not None:
            out[f"plan_{pth}"] = {"labels": r["labels"], "lambda": r["duals"]["liquidity_premium_lambda"],
                                  "treasury_to_nav": r["treasury_to_nav"], "cfp_stage": r["cfp_stage"]}
    return out


def run_horizon_test(v, root, W0, saa):
    """Same parameters and rules with the tree cut at 2, 3 and 4 years (ARCHITECTURE.md 5.2)."""
    lim = float(v["actions"]["revolver_limit"])
    out = []
    for Hh in v["horizon_test"]["horizons"]:
        nodes_h = build_tree(v, v["tree"]["start_regime"], Hh, root["Y"], saa)
        a, _ = run_case(v, nodes_h, root, W0, lim)
        b, _ = run_case(v, nodes_h, root, W0, 0.0)
        out.append({"horizon_years": Hh, "nodes": len(nodes_h),
                    "R1": case_brief(v, nodes_h, a), "R0": case_brief(v, nodes_h, b),
                    "R1_first_two_years": case_brief(v, nodes_h, a, tmax=2),
                    "R0_first_two_years": case_brief(v, nodes_h, b, tmax=2)})
    return out


def run_sensitivities(v, root, W0, saa, base_r1):
    """One change at a time from params.json, each re-solved with and without the revolver."""
    H = int(v["tree"]["decision_stages"])
    out = []
    for var in v["sensitivity"]["variants"]:
        vv = apply_changes(v, var["changes"])
        nodes_s = build_tree(vv, vv["tree"]["start_regime"], H, root["Y"], saa)
        lim_s = float(vv["actions"]["revolver_limit"])
        a, ra = run_case(vv, nodes_s, root, W0, lim_s)
        b, rb = run_case(vv, nodes_s, root, W0, 0.0)
        ba, bb = case_brief(vv, nodes_s, a), case_brief(vv, nodes_s, b)
        same_u = vv["objective"]["crra_gamma"] == v["objective"]["crra_gamma"]
        out.append({"id": var["id"], "label": var["label"], "owner": var["owner"], "changes": var["changes"],
                    "status_R1": "Optimal" if a is not None else ra[1].status,
                    "status_R0": "Optimal" if b is not None else rb[1].status,
                    "R1": ba, "R0": bb,
                    "revolver_value_bn": (ba["ce"] - bb["ce"]) if (ba and bb) else None,
                    "same_utility_as_base": same_u,
                    "ce_change_vs_base_bn": (ba["ce"] - base_r1["ce"]) if (ba and same_u) else None})
    return out


def run_floor_table(v, nodes, root, W0, lim, base: Case):
    """Downside floors as a sensitivity: CVaR10% of W~ >= floor, with the capacity check first."""
    H = max(n.stage for n in nodes)
    lpx = build_lp(v, nodes, root, W0, [], lim, mode="maxcvar")
    sx = lpx.solve()
    best = sx.obj / OBJ_SCALE if sx.ok else None
    out = {"no_floor": {"cvar10_W_tilde": base.summ["cvar10_W_tilde"],
                        "cvar10_annualized": base.summ["cvar10_annualized_return"],
                        "ce": base.summ["certainty_equivalent_W_tilde"]},
           "best_attainable_cvar10_W_tilde": best,
           "best_attainable_cvar10_annualized": (best / W0) ** (1 / H) - 1 if best and best > 0 else None,
           "rows": []}
    for fl in v["downside_floor_sensitivity"]["floors"]:
        F = W0 * (1.0 + fl) ** H
        a, raw_ = run_case(v, nodes, root, W0, lim, cvar_floor=F, hold_root_pe=True)
        if a is None:
            forced, _ = run_case(v, nodes, root, W0, lim, cvar_floor=F)
            out["rows"].append({"floor_annual": fl, "floor_W_tilde": F, "status": raw_[1].status,
                                "attainable": best is not None and F <= best,
                                "forced_root_pe": None if forced is None else {
                                    "labels": forced.rep[0]["labels"],
                                    "ce": forced.summ["certainty_equivalent_W_tilde"]}})
            continue
        b = case_brief(v, nodes, a)
        mu0 = a.s.dual("cash[0]")
        out["rows"].append({
            "floor_annual": fl, "floor_W_tilde": F, "status": "Optimal",
            "binding": abs(a.summ["cvar10_W_tilde"] - F) < 1e-6 * W0,
            "shadow_value_root_usd_per_usd": -a.s.dual("cvar") / mu0,
            "ce": a.summ["certainty_equivalent_W_tilde"],
            "ce_cost_bn": base.summ["certainty_equivalent_W_tilde"] - a.summ["certainty_equivalent_W_tilde"],
            "cvar10_annualized": a.summ["cvar10_annualized_return"],
            "root_labels": a.rep[0]["labels"], "root_pe_rule": a.root_pe_rule,
            "P_pe_sale": b["P_pe_sale"], "P_red_event": b["P_red_event"], "P_fire_sale": b["P_fire_sale"],
            "forced_root_pe": b["forced_root_pe"]})
    return out


def time_consistency(v, nodes, root, W0, lim, main: Case, saa):
    """Shrinking horizon: re-solve the remaining subtree from each stage-1 node with the same tangents and the
    year-1 draw and the root's charges as constants. Expected utility is time consistent, so the plan must
    come back unchanged."""
    H = max(n.stage for n in nodes)
    A = v["actions"]
    p0 = main.post[0]
    charges0 = (A["pacing_cut_cost"] * p0["cut"] + target_price(v, nodes[0].regime) * p0["s8"]
                + band_price(v, nodes[0].regime) * p0["sb"])
    out = []
    for n1 in (n for n in nodes if n.stage == 1):
        st = dict(main.pre[n1.id])
        sub = build_tree(v, n1.regime, H - 1, st["Y"], saa)
        d1 = n1.draw * nav_post(v, nodes[0], p0)
        offs = {}
        for leaf in (m for m in sub if m.stage == H - 1):
            g_acc = 1.0
            for j in path_ids(sub, leaf)[1:]:
                g_acc *= 1.0 + sub[j].rRef
            offs[leaf.id] = d1 * g_acc - charges0
        lp_t, s_t, _ = solve_case(v, sub, st, W0, lim, offsets=offs, tangents=main.tan)
        rep_t, _, _ = extract(v, sub, st, lp_t, s_t, lim, W0, offsets=offs)
        diffs = []
        for r in rep_t:
            if r["stage"] >= H - 1:
                continue
            full = next(x for x in main.rep if x["path"] == n1.path + r["path"][1:])
            diffs.append(max(abs(r["decisions"][k] - full["decisions"][k]) for k in DEC_KEYS))
        out.append({"from_path": n1.path, "max_abs_decision_difference_bn": max(diffs)})
    return out


def limit_slacks(v, nodes, rep, lim):
    """Every identity and limit at every node, recomputed from the reported states (not from the LP rows).
    Returns the smallest slack per row family (>= 0 means the row holds) and the largest identity residuals."""
    A, Lm = v["actions"], v["limits"]
    f, f8 = Lm["cash_floor_frac"], Lm["cash_target_frac"]
    net = Lm.get("cash_target_basis", "gross") == "net_of_facility_draws"
    hi = Lm.get("liquid_exposure_max_frac")
    kap, cap = A["exposure_cap"], A.get("synthetic_notional_cap")
    cut_max = (1.0 - A["pacing_core_sleeve"]) * A["pacing_plan"]
    H = max(n.stage for n in nodes)
    byid = {r["id"]: r for r in rep}
    slack, resid = {}, {}

    def s_(k, val):
        slack[k] = min(slack.get(k, INF), val)

    def r_(k, val):
        resid[k] = max(resid.get(k, 0.0), abs(val))

    for r in rep:
        n = nodes[r["id"]]
        dec = n.stage < H
        cs = r["closing_state"]
        nav = cs["C"] + A["lever_initial_margin"][n.regime] * cs["X"] + cs["L"] + cs["P"] + n.Y - cs["BR"] - cs["BN"]
        r_("closing NAV", nav - cs["NAV"])
        s_("cash floor (4%)", cs["C"] - f * nav)
        own = cs["C"] - ((cs["BR"] + cs["BN"]) if net else 0.0)
        s_("8% target incl. priced shortfall", own + cs["s8"] - f8 * nav)
        k_ltv, c_ltv = nav_loan_capacity_terms(v, n)
        s_("NAV-loan capacity", k_ltv * cs["P"] + c_ltv - cs["BN"])
        s_("revolver availability", A["revolver_availability"][n.regime] * lim - cs["BR"])
        pm = cs["L"] + cs["X"]
        if hi is not None:
            s_("IC range upper edge", hi * nav - pm)
        lo = band_lo_value(v, n.regime, horizon=not dec)
        if lo is not None:
            s_("IC range lower edge incl. priced shortfall", pm + cs["sb"] - lo * nav)
        if dec:
            s_("exposure cap", kap * nav - (cs["L"] + cs["P"] + n.Y + cs["X"]))
            if cap is not None:
                s_("synthetic budget", cap - cs["X"])
            s_("pacing cut <= 75% of plan", cut_max - r["decisions"]["pace_cut"])
        s_("non-negative stocks", min(cs["C"], cs["L"], cs["P"], cs["U"], cs["BR"], cs["BN"], cs["X"]))
        if n.parent is not None:
            par = nodes[n.parent]
            pc = byid[par.id]["closing_state"]
            post_par = {k: pc[k] for k in ("C", "L", "P", "U", "BR", "BN", "X")}
            post_par["cut"] = byid[par.id]["decisions"]["pace_cut"]
            pre = pre_state(v, par, n, post_par, lim)
            for k in ("C", "L", "P", "U"):
                r_(f"opening {k} from the parent's closing state and the year's rates", pre[k] - r["opening_state"][k])
            draw = -r["exogenous_flows"]["owner_draw"]
            r_("owner draw = draw rate x parent's closing NAV", draw - n.draw * pc["NAV"])
        for k, val in r.get("residuals", {}).items():
            r_(f"closing {k} = opening {k} + trades", val)
    return slack, resid


# =============================================================================================
# 10. RESULTS.md (every number is read from results.json; the Verification section from verification.json)
# =============================================================================================
def fm(x, nd=2):
    return "-" if x is None else f"{x:,.{nd}f}"


def pct(x, nd=1):
    if x is None:
        return "-"
    y = 100 * x
    if abs(y) < 0.5 * 10 ** (-nd):
        y = 0.0
    return f"{y:.{nd}f}%"


def acts_text(lab, horizon=False):
    a = []
    if lab["liquid_book"] != "HOLD":
        a.append("Liquid " + lab["liquid_book"])
    if lab["pe_book"] != "HOLD":
        a.append("PE " + lab["pe_book"])
    if lab["corporate_finance"] != "NONE":
        a.append("CF " + lab["corporate_finance"])
    return "; ".join(a) if a else ("no trade" if horizon else "HOLD everything")


def lam_text(r):
    lam = r.get("duals", {}).get("liquidity_premium_lambda") if "duals" in r else r.get("lambda")
    return pct(max(lam, 0.0) if lam is not None else None, 2)


def money(x, nd=3):
    """Signed $bn amount: +$0.044bn / −$0.065bn."""
    if x is None:
        return "-"
    return f"{'−' if x < 0 else '+'}${abs(x):.{nd}f}bn"


def shown_binding(r):
    """Binding rows worth showing: hard rows at their bound, and priced rows whose price is not zero."""
    return [b for b in r.get("binding_constraints", [])
            if b["kind"] not in ("target", "band_lo") or b["shadow_value_node_usd_per_usd"] > 5e-5]


def write_results_md(res, nodes, H):
    """Human-readable summary. Every number comes from `res` (results.json) or verification.json."""
    S_, cases = res["summary"], res["cases"]
    nb = cases["no_revolver"]
    nbs = nb["summary"]
    cl, clb = res["closed_loop"]["with_revolver"], res["closed_loop"]["no_revolver"]
    nv = res["naive_rules"]
    prm = res["meta"]["parameters"]
    eps = prm["settings"]["action_threshold_bn"]
    byid = {r["id"]: r for r in res["nodes"]}
    bypath = {r["path"]: r for r in res["nodes"]}
    nob = {r["path"]: r for r in nb["nodes"]}
    W0 = res["meta"]["W0"]
    L = []
    w = L.append

    w("# Multi-period tree: worked example (SYNTHETIC)")
    w("")
    w("> **SYNTHETIC. Not ADIC data and not a forecast.** Every number here is computed by `tree_demo.py` from the "
      "illustrative inputs in `params.json` and read from `results.json`. Version 2: the corrections from "
      "`verify_math.md` and `verify_finance.md` are applied (section 10 lists each one).")
    w("")
    w("## What this shows")
    w("")
    w("One linear program turns inputs and limits into decisions. People set the inputs (scenario probabilities, "
      "returns, bids, the owner's draw rule) and the limits (the 4% cash floor, facility and leverage caps, the IC "
      "range, the prices of the two appetite limits) and approve the result. Nothing inside the solve is a "
      "judgement call. For every node of a 40-node scenario tree the program returns:")
    w("")
    w("1. **what to do** with each book (SELL / HOLD / REFINANCE / LEVER / PACE-CUT, with amounts);")
    w("2. **the price of liquidity** at that node (λ, read from the LP duals);")
    w("3. **the probability** of reaching it, and so the probability of every outcome.")
    w("")
    w(f"Start: the $177bn book (allocation v2), today read as a PE distribution **drought (D)**. Each year moves to "
      f"N (normal), D (drought) or C (crisis with an oil shock, when the owner draws more). Decisions at t = 0, 1, 2; "
      f"outcomes at t = 3; 1 + 3 + 9 + 27 = {res['meta']['tree']['nodes']} nodes. The LP has "
      f"{res['meta']['lp_size_main_case']['columns']} columns and {res['meta']['lp_size_main_case']['rows']} rows "
      f"and solves in milliseconds with HiGHS. The whole run, with every check below, takes a few seconds.")
    w("")

    # ---- key results ----
    r0, rdc, rdd, rdcc = bypath[nodes[0].path], bypath.get("D>C"), bypath.get("D>D"), bypath.get("D>C>C")
    b0 = res["cases"]["with_revolver"]["brief"]
    dce_rev = nb["revolver_value_ce_bn"]
    dec = nv["decomposition"]
    hz = res["horizon_test"]
    root_same = len({json.dumps(h["R1"]["root_labels"], sort_keys=True) for h in hz}) == 1
    w("**Key results (revolver signed unless stated; SYNTHETIC):**")
    w("")
    w(f"- **Today (root, drought):** {acts_text(r0['labels'])}. Treasury closes at {pct(r0['treasury_to_nav'])} of "
      f"NAV (CFP {r0['cfp_stage']}); λ = {lam_text(r0)}. The program holds exactly the 8% own-liquidity target and "
      f"puts the cash above it into the liquid book. "
      + ("The same root decision comes out of a 2-, 3- and 4-year tree (section 6)." if root_same else
         "The root decision changes with the tree's depth (section 6)."))
    if rdc is not None:
        dcd = rdc["decisions"]
        calm = ("It sells no equities at the bottom and no PE." if dcd["sell_liquid"] < eps and dcd["sell_pe_nav"] < eps
                else ("It sells no PE." if dcd["sell_pe_nav"] < eps else "It sells PE."))
        w(f"- **First crisis year (D>C, p = {rdc['probability']:.2f}):** {acts_text(rdc['labels'])}; Treasury "
          f"{pct(rdc['treasury_to_nav'])} of NAV (CFP {rdc['cfp_stage']}); λ = {lam_text(rdc)}; state price "
          f"m = {rdc['duals']['state_price_m']:.2f}. {calm} Without the revolver: {acts_text(nob['D>C']['labels'])}.")
    if rdd is not None:
        w(f"- **Drought persists (D>D, p = {rdd['probability']:.2f}):** {acts_text(rdd['labels'])}, restoring the 8% "
          f"target; λ = {lam_text(rdd)}.")
    w(f"- **Outcomes of the plan:** expected return {pct(S_['expected_annualized_return'])} a year (owner draws "
      f"counted), P(≥ 10% a year) = {pct(S_['P_annualized_return_ge_10pct'])}, CVaR10% = "
      f"{pct(S_['cvar10_annualized_return'])} a year, P(any PE sale) = {pct(S_['P_any_pe_sale'])}, P(red event) = "
      f"{pct(S_['P_red_event'])}. **The rolling policy** (re-solved at all 12 nodes of years 1 and 2) reaches a "
      f"certainty equivalent within ${abs(cl['summary']['certainty_equivalent_W_tilde'] - S_['certainty_equivalent_W_tilde']):.3f}bn "
      f"of the static plan, with P(any PE sale) = {pct(cl['summary']['P_any_pe_sale'])}.")
    w(f"- **The signed revolver** is worth {money(dce_rev)} of certainty equivalent here, against "
      f"${nb['undrawn_fee_over_3_years_bn']:.3f}bn of undrawn fees over 3 years. With research-calibrated draws the "
      f"fund can meet its crisis needs by selling liquid assets, so the facility "
      + ("does not pay for itself in this example. " if dce_rev < 0 else "pays for itself. ")
      + "With v1's hard IC range it would be worth "
      + next((money(s["revolver_value_bn"], 2) for s in res["sensitivity"] if s["id"] == "ic_lo_hard"), "-")
      + " (section 7). v1's $0.75bn also reflected its larger crisis draws and its downside floor.")
    w(f"- **Against a simple rule** (hold 8% by selling liquid first and PE last, never borrow): the program beats it "
      f"by {money(dec['program_R0_minus_naive_8pct_ce_bn'])} when neither has a revolver (the program can also use "
      f"P2S and the NAV loan), and beats the same rule with the revolver by "
      f"{money(dec.get('program_R1_minus_naive_8pct_revolver_ce_bn'))}. The gaps are small because liquidity is "
      f"cheap in this calibration. Here the program's value is that it finds the plan without a hand-written rule "
      f"and prices liquidity at every node.")
    w("")

    # ---- 1. the tree ----
    w("## 1. The tree and the decision at every node (revolver signed)")
    w("")
    w("Each line: path (regime of each year), probability of reaching the node, opening cash / liquid / PE NAV "
      "($bn) after that year's flows, the owner's draw paid that year, the decision (amounts in $bn; CF = Corporate "
      "Finance), Treasury / NAV after the decision with its CFP stage, λ (liquidity premium) and m (state price: "
      "today's value of $1 at that node per unit of probability). Under each year-2 node: its three outcomes at "
      "t = 3 as annualized returns, with the settlement trade if there is one.")
    w("")
    w("```text")

    def line(r):
        o, d = r["opening_state"], r["exogenous_flows"]
        draw = "" if d is None else f" draw {-d['owner_draw']:4.1f} |"
        return (f"{r['path']:<8} p={r['probability']:.3f} | cash {o['C']:5.1f} liq {o['L']:5.1f} PE {o['P']:5.1f} |"
                f"{draw} {acts_text(r['labels'])} | T/NAV {pct(r['treasury_to_nav'])} {r['cfp_stage']} | "
                f"λ {lam_text(r)} m {r['duals']['state_price_m']:.2f}")

    for n in nodes:
        if n.stage >= H:
            continue
        r = byid[n.id]
        ind = "    " * n.stage
        w(ind + line(r))
        if n.stage == H - 1:
            parts = []
            for c in n.children:
                rc = byid[c]
                t = rc["terminal"]
                dd = rc["decisions"]
                extra = []
                if dd["sell_pe_nav"] > eps:
                    extra.append(f"PE-SALE {dd['sell_pe_nav']:.1f}")
                if dd["sell_liquid"] > eps:
                    extra.append(f"sells liq {dd['sell_liquid']:.1f}")
                if dd["buy_liquid"] > eps:
                    extra.append(f"buys liq {dd['buy_liquid']:.1f}")
                if dd["revolver_change"] > eps or dd["nav_loan_change"] > eps:
                    extra.append(f"draws {max(dd['revolver_change'], 0) + max(dd['nav_loan_change'], 0):.1f}")
                parts.append(f"{rc['regime']}: {pct(t['annualized_return'])}/yr p={rc['probability']:.3f}"
                             + (" " + ", ".join(extra) if extra else ""))
            w(ind + "    t=3 -> " + " | ".join(parts))
    w("```")
    w("")
    w("Read across a row: the program's plan for that state of the world. Only the root's decision is executed now; "
      "the rest are contingency plans, re-solved when the year's regime is known (section 5 runs that rolling "
      "policy). Opening cash can be negative: it is cash after the year's flows (draw, calls, distributions, yield, "
      "interest) and before the node's actions. With annual steps the sales and drawings a treasurer would make "
      "during the year are booked at the node, and after them every hard limit holds at every node.")
    w("")

    # ---- 2. decision table ----
    w("## 2. Decisions, binding limits and prices by node")
    w("")
    w("| Path | p | Draw paid | Liquid | PE book | Corporate Finance | Treasury / NAV (CFP) | Binding limits (¢ per $1 of relief, at the node) | λ | m |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for n in nodes:
        if n.stage >= H:
            continue
        r = byid[n.id]
        d = r["exogenous_flows"]
        draw = "-" if d is None else fm(-d["owner_draw"], 1)
        bind = "; ".join(f"{SHORT.get(b['kind'], b['kind'])} ({100 * max(b['shadow_value_node_usd_per_usd'], 0):.1f}¢)"
                         for b in shown_binding(r)) or "-"
        kink = " (near a kink)" if r["duals"].get("near_kink_within_probe") else ""
        w(f"| {r['path']} | {r['probability']:.3f} | {draw} | {r['labels']['liquid_book']} | {r['labels']['pe_book']} | "
          f"{r['labels']['corporate_finance']} | {pct(r['treasury_to_nav'])} ({r['cfp_stage']}) | {bind} | "
          f"{lam_text(r)}{kink} | {r['duals']['state_price_m']:.2f} |")
    w("")
    dnodes = [r for r in res["nodes"] if r["stage"] < H]
    lams = [(r["path"], max(r["duals"]["liquidity_premium_lambda"] or 0.0, 0.0)) for r in dnodes]
    top = max(lams, key=lambda t: t[1])
    crisis_lams = [l for p_, l in lams if p_.endswith("C")]
    tgt_lams = [max(r["duals"]["liquidity_premium_lambda"] or 0, 0) for r in dnodes
                if any(b["kind"] == "target" and b["shadow_value_node_usd_per_usd"] > 5e-5 for b in r["binding_constraints"])
                and r["decisions"]["revolver_change"] <= eps]
    rev_lams = [max(r["duals"]["liquidity_premium_lambda"] or 0, 0) for r in dnodes
                if any(b["kind"] == "floor" for b in r["binding_constraints"]) and r["decisions"]["revolver_change"] > eps]
    top_r = bypath[top[0]]
    top_bind = ", ".join(SHORT.get(b["kind"], b["kind"]) for b in shown_binding(top_r))
    tp = prm["limits"]["cash_target_shortfall_price"]["N"]
    w("**How to read λ and m.** λ = M/(μ − M): μ is the dual of the node's cash-balance row and M the part that comes "
      "from the node's liquidity rows (the 4% floor and the 8% target; ARCHITECTURE.md §5.6). It is the cost of the "
      "marginal dollar of liquidity at that node, roughly (1 − f)/(1 + r) × the net cost of the cheapest source still "
      "available."
      + (f" Where the 8% target binds and is met, the marginal dollar comes from a liquid sale: the 0.15% trading cost "
         f"plus the return given up by holding cash instead of the liquid book (λ {pct(min(tgt_lams), 2)}–"
         f"{pct(max(tgt_lams), 2)} here, capped by the target's {100 * tp:.0f}¢ price)." if tgt_lams else "")
      + (f" Where a crisis year draws the revolver, it is the revolver's 85bp spread less the 15bp undrawn fee the draw "
         f"saves (λ {pct(min(rev_lams), 2)}–{pct(max(rev_lams), 2)})." if rev_lams else "")
      + f" The highest λ in the tree is {pct(top[1], 2)} at {top[0]} (binding there: {top_bind}).")
    w("")
    w(f"So λ is **not** highest in the crisis branches (crisis nodes: {pct(min(crisis_lams), 2)}–"
      f"{pct(max(crisis_lams), 2)}): with a signed revolver, a crisis dollar is cheap at the margin. The stress shows "
      "in m instead. m is today's value of a dollar at that node, and it is highest where wealth is lowest "
      f"(D>C {byid[node_by_path(nodes, 'D>C').id]['duals']['state_price_m']:.2f}, D>C>C "
      f"{byid[node_by_path(nodes, 'D>C>C').id]['duals']['state_price_m']:.2f}). Without the revolver, crisis λ "
      "rises (section 4). Every decision node's cash price was also measured at ± "
      f"${prm['settings']['kink_probe_bn']}bn of cash. "
      + ("None sits within that distance of a kink, so each λ holds for at least that much cash."
         if not res["checks"]["nodes_near_a_kink"] else
         f"Nodes near a kink: {', '.join(res['checks']['nodes_near_a_kink'])}."))
    w("")
    be = [(r["path"], r["duals"].get("pacing_cut_break_even_cost_per_usd")) for r in res["nodes"]
          if r["stage"] < H and r["duals"].get("pacing_cut_break_even_cost_per_usd") is not None]
    if be:
        topb = max(be, key=lambda t: t[1])
        cp = prm["actions"]["pacing_cut_cost"]
        psi_var = next((s for s in res["sensitivity"] if s["id"] == "psi_10"), None)
        cut_txt = ""
        if psi_var and psi_var["R1"] and "plan_D>C>C" in psi_var["R1"] and "PACE-CUT" in psi_var["R1"]["plan_D>C>C"]["labels"]["pe_book"]:
            cut_txt = (f" With a terminal burden of 10¢ per $ of unfunded (section 7), the program cuts the maximum 75% "
                       f"of the plan in the second crisis year (D>C>C: {psi_var['R1']['plan_D>C>C']['labels']['pe_book']}).")
        w(f"**PACE-CUT** is available at every node, capped at 75% of the year's plan (a protected core sleeve), but it "
          f"is not chosen here. Its franchise cost is {100 * cp:.1f}¢ per $ cut, and its liquidity only arrives two "
          f"quarters later. The cut column's reduced cost gives the break-even cost: the most valuable cut in the tree "
          f"is at {topb[0]}, worth {100 * topb[1]:.1f}¢ per $. Unfunded commitments left at t = 3 carry a stated burden "
          f"of {100 * prm['terminal']['unfunded_burden_per_dollar']:.0f}¢ per $ (v1 used 0).{cut_txt}")
        w("")

    # ---- 3. outcomes ----
    w("## 3. Outcomes and their probabilities (SYNTHETIC)")
    w("")
    cols = [("Plan, revolver", S_), ("Rolling policy, revolver", cl["summary"]), ("Plan, no revolver", nbs),
            ("Rolling, no revolver", clb["summary"])]
    for k, lab_ in (("naive_8pct", "Naive 8%"), ("naive_8pct_revolver", "Naive 8% + revolver"),
                    ("naive_4pct", "Naive 4%")):
        if k in nv:
            cols.append((lab_, nv[k]["summary"]))
    w("| Metric | " + " | ".join(c for c, _ in cols) + " |")
    w("|---|" + "---|" * len(cols))
    rows = [
        ("Certainty equivalent of W~ ($bn, exact CRRA 3)", "certainty_equivalent_W_tilde", lambda x: fm(x, 2)),
        ("Expected W~ ($bn, draws counted)", "expected_W_tilde", lambda x: fm(x, 2)),
        ("Expected annualized return", "expected_annualized_return", pct),
        ("Median annualized return", "median_annualized_return", pct),
        ("CVaR10% as annualized return", "cvar10_annualized_return", pct),
        ("P(annualized return ≥ 10%)", "P_annualized_return_ge_10pct", pct),
        ("P(annualized return < 0)", "P_annualized_return_lt_0", pct),
        ("P(any PE sale)", "P_any_pe_sale", pct),
        ("P(PE fire sale at the crisis discount)", "P_any_pe_fire_sale_at_crisis_discount", pct),
        ("P(red event: ADR-39 test)", "P_red_event", pct),
        ("P(revolver drawn somewhere)", "P_revolver_drawn_somewhere", pct),
        ("P(NAV loan used somewhere)", "P_nav_loan_used_somewhere", pct),
        ("P(P2S used somewhere)", "P_p2s_somewhere", pct),
        ("P(LEVER: synthetic, or a draw that pays for purchases)", "P_lever_somewhere", pct),
        ("P(below the 8% target somewhere)", "P_below_8pct_target_somewhere", pct),
        ("P(CFP Red or Black somewhere)", "P_cfp_red_or_black_somewhere", pct),
        ("P(pacing cut somewhere)", "P_pacing_cut_somewhere", pct),
        ("At t = 3: P(liquid share < 27%)", "P_horizon_liquid_share_below_lower_edge", pct),
        ("At t = 3: P(private NAV + unfunded > 80% of NAV, LR8)", "P_horizon_LR8_above_0p80", pct),
        ("At t = 3: P(NAV < 80% of today's)", "P_horizon_NAV_below_80pct_of_W0", pct),
        ("Expected owner draws paid over 3 years ($bn)", "expected_owner_draws_paid_total", lambda x: fm(x, 2)),
    ]
    for label, key, f_ in rows:
        w(f"| {label} | " + " | ".join(f_(c.get(key)) if c.get(key) is not None else "-" for _, c in cols) + " |")
    w("")
    w("Columns: the **plan** is the static 3-year solution. The **rolling policy** executes only each node's first "
      "decision and re-solves a fresh 3-year tree at every node of years 1 and 2 (section 5); its probabilities are "
      "those of the policy that would actually run. The **naive rules** face the same flows, limits and charges: "
      "hold the target by selling liquid inside the IC range, sell liquid below the range before any PE if the 4% "
      "floor would fail, and never use a NAV loan, P2S, LEVER or a pacing cut. The revolver variant draws only for "
      "the floor ('lines drawn') and pays the undrawn fee. The owner's draw is paid in full at every node in every "
      "column: it is a fixed outflow in every cash row, not a choice.")
    w("")
    w(f"Decomposition of the program's lead in certainty equivalent ($bn): program with revolver minus naive 8% "
      f"{dec['program_R1_minus_naive_8pct_ce_bn']:+.3f} = value of the revolver to the program "
      f"{dec['revolver_value_for_the_program_ce_bn']:+.3f} + optimizing without it "
      f"{dec['program_R0_minus_naive_8pct_ce_bn']:+.3f}. With the revolver on both sides, the program leads by "
      f"{dec.get('program_R1_minus_naive_8pct_revolver_ce_bn', float('nan')):+.3f}. Probabilities are coarse: 27 "
      f"leaves whose masses run from {100 * min(d['probability'] for d in S_['terminal_distribution']):.2f}% to "
      f"{100 * max(d['probability'] for d in S_['terminal_distribution']):.1f}%, so P(≥ 10% a year) moves in "
      f"leaf-sized steps and is the same in every column (the regime path decides it).")
    w("")
    w("Terminal distribution of the plan (revolver signed), worst to best, with the horizon balance sheet:")
    w("")
    w("| Path | p | Cum. p | W~ ($bn) | Annualized | Treasury / NAV | Liquid share | LR8 | Debt ($bn) | NAV vs today | CFP |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for d in S_["terminal_distribution"]:
        w(f"| {d['path']} | {d['probability']:.4f} | {d['cumulative_probability']:.3f} | {d['W_tilde']:.1f} | "
          f"{pct(d['annualized_return'])} | {pct(d['treasury_to_nav'])} | {pct(d['liquid_share'])} | "
          f"{d['LR8_private_plus_unfunded_to_nav']:.2f} | {d['debt']:.1f} | {pct(d['nav_vs_W0'])} | {d['cfp_stage']} |")
    w("")
    w("At t = 3 every hard row still holds: the 4% floor, the NAV-loan cap and revolver availability of the leaf's "
      "regime (with forced paydowns). Debt can be repaid there but not drawn, because a draw at the horizon would cost "
      "nothing inside the tree. Shortfalls below the 8% target and the IC range are charged, so the plan cannot end "
      "in a state that the next year would have to repair for free. PE is valued at economic NAV (90% of the mark "
      "after a crisis year), and unfunded commitments carry a burden. LR8 is (private NAV + unfunded) / NAV; the "
      "architecture's default limit is 0.80.")
    w("")

    # ---- 4. revolver ----
    p1a, p1b = cases["with_revolver"]["phase1"], nb["phase1"]
    w("## 4. Revolver signed or not (consent scenarios R1 and R0) and Phase I")
    w("")

    def shorts(d_):
        return ", ".join(f"{k} (${val:.2f}bn)" for k, val in d_.items())

    w(f"Phase I asks whether every hard row can be met with reversible levers only, i.e. with no PE sale "
      f"(ARCHITECTURE.md §5.5). Tier A is the 4% cash floor at every node. The IC range is not a Tier-1A row, so its "
      f"shortfall is reported separately as tier B. With the revolver: {p1a['reading']}; tier A u* = "
      f"{fm(p1a['u_star_floor_bn'], 3)}bn"
      + (f", IC-range shortfall u* = {fm(p1a['u_star_ic_range_bn'], 3)}bn ({shorts(p1a['short_ic_range'])})"
         if p1a["short_ic_range"] else "") + ". "
      f"Without it: {p1b['reading']}; tier A u* = {fm(p1b['u_star_floor_bn'], 3)}bn"
      + (f", IC-range shortfall u* = {fm(p1b['u_star_ic_range_bn'], 3)}bn, all at t = 3 after crisis years "
         f"({shorts(p1b['short_ic_range'])})" if p1b["short_ic_range"] else "")
      + ". The IC range is elastic, so its shortfalls are priced, not forced, and they never trigger a PE sale.")
    w("")
    w("| Path | p | λ with revolver | λ without | m with / without | Closing cash with / without | What changes |")
    w("|---|---|---|---|---|---|---|")
    for c in nb["comparison_with_revolver"]:
        ch = "; ".join(f"{k.replace('_', ' ')}: {val['with_revolver']} -> {val['no_revolver']}"
                       for k, val in c["label_changes"].items()) or "same actions"
        lw = c["lambda_with_revolver"]
        lo_ = c["lambda_no_revolver"]
        w(f"| {c['path']} | {c['probability']:.3f} | {pct(max(lw, 0) if lw is not None else None, 2)} | "
          f"{pct(max(lo_, 0) if lo_ is not None else None, 2)} | {c['m_with_revolver']:.2f} / {c['m_no_revolver']:.2f} | "
          f"{c['closing_cash_with']:.1f} / {c['closing_cash_without']:.1f} | {ch} |")
    w("")
    root_flip = byid[0]["labels"] != nob[nodes[0].path]["labels"]
    w(f"Value of the signed revolver: {money(dce_rev)} of certainty equivalent against "
      f"${nb['undrawn_fee_over_3_years_bn']:.3f}bn of undrawn fees over 3 years. "
      + ("The root decision changes with the revolver, so the root card is consent-sensitive. " if root_flip else
         "No root decision changes between R1 and R0, so no card here is consent-sensitive. ")
      + "Section 7 shows when the facility becomes valuable: with v1's hard IC range it is worth "
      + next((money(s["revolver_value_bn"], 2) for s in res["sensitivity"] if s["id"] == "ic_lo_hard"), "-")
      + ", because without it the fund would have to sell PE.")
    w("")

    # ---- 5. rolling policy ----
    w("## 5. The rolling policy (MPC): re-solving at every node of years 1 and 2")
    w("")
    w("Only the root decision is executed. A year later the realized regime is known, the state is measured, and the "
      "same program is solved again on a fresh 3-year tree from there, with the same rules. A re-solve whose opening "
      "event stage is Amber or worse holds any PE sale at its own root at zero and prices it with a forced re-solve "
      "(ARCHITECTURE.md §5.4). The opening stage is read before the node's actions, on cash after the year's flows, "
      "which is why it is often Red or Black. At t = 3 each path settles with the same horizon rows as the plan. That "
      "is done at all 3 + 9 = 12 nodes, so every probability in the rolling columns of section 3 is that of the policy "
      "that would run.")
    w("")
    w("| Node | p | Opening event stage | Plan made at t = 0 | Re-solved | Treasury / NAV | λ |")
    w("|---|---|---|---|---|---|---|")
    for d in cl["resolves"]:
        plan = bypath[d["path"]]
        w(f"| {d['path']} | {d['probability']:.3f} | {d['opening_event_stage']} | {acts_text(plan['labels'])} | "
          f"{acts_text(d['resolved_decision']['labels'])} | {pct(d['resolved_decision']['treasury_to_nav'])} | "
          f"{pct(max(d['resolved_decision']['lambda'] or 0, 0), 2)} |")
    w("")
    tcs = res["time_consistency_check"]
    forced_gains = [d["forced_resolve_root_pe"]["ce_gain_bn"] for d in cl["resolves"] if d["forced_resolve_root_pe"]]
    w(f"The re-solved decisions differ from the plan only where the 3-year window has moved, so the horizon now sees "
      f"one more year. The rolling policy's certainty equivalent is "
      f"{fm(cl['summary']['certainty_equivalent_W_tilde'], 3)} against {fm(S_['certainty_equivalent_W_tilde'], 3)} for "
      f"the plan. Forced re-solves that allow a PE sale at a re-solve's root would add at most "
      f"${max(forced_gains) if forced_gains else 0:.3f}bn. Check: re-solving the remaining subtree with the same horizon "
      f"reproduces the plan exactly (max decision difference "
      + ", ".join(f"{t['from_path']}: ${t['max_abs_decision_difference_bn']:.0e}bn" for t in tcs)
      + "). The program is time consistent; only the moving window changes decisions. v1's rolling CVaR floor was not "
      "time consistent and made the rolling policy sell PE at D>D. There is no floor in the main case now (section 7).")
    w("")

    # ---- 6. horizon test ----
    w("## 6. Horizon test: does the answer depend on where the tree stops?")
    w("")
    w("Same inputs and rules, with the tree cut after 2, 3 and 4 years (ARCHITECTURE.md §5.2):")
    w("")
    w("| Tree | Nodes | Root decision | Root λ | Plan at D>C (first crisis year) | CE (annualized) | P(any PE sale) R1 / R0 | P(red event) R1 / R0 | P(revolver drawn, years 1-2) |")
    w("|---|---|---|---|---|---|---|---|---|")
    for h in hz:
        a, b = h["R1"], h["R0"]
        dc = a.get("plan_D>C")
        w(f"| {h['horizon_years']} years | {h['nodes']} | {acts_text(a['root_labels'])} | {pct(a['root_lambda'], 2)} | "
          f"{acts_text(dc['labels']) if dc else '-'} | {pct(a['ce_annualized'])} | {pct(a['P_pe_sale'])} / "
          f"{pct(b['P_pe_sale'])} | {pct(a['P_red_event'])} / {pct(b['P_red_event'])} | "
          f"{pct(h['R1_first_two_years']['P_revolver_drawn'])} |")
    w("")
    dc_same = len({json.dumps(h["R1"].get("plan_D>C", {}).get("labels"), sort_keys=True) for h in hz}) == 1
    w(("The root decision does not depend on the horizon" if root_same else "The root decision changes with the horizon")
      + (", and neither does the first-crisis-year response. " if dc_same else
         "; the first-crisis-year response keeps its main move but its details shift with the cut. ")
      + "Plans further out shift a little with the cut, because the last decision year always looks one year ahead, "
      "so they are contingency plans, not policy. In v1 the 0% fire-sale headline and the LEVER and REFINANCE plans at "
      "t = 2 came from the cut. Horizon rows now hold every limit at t = 3 and price what is left to repair.")
    w("")

    # ---- 7. sensitivity ----
    w("## 7. What moves the answer: the human-set inputs and their owners (SYNTHETIC)")
    w("")
    w("The solve is objective, but its answer moves with a handful of inputs that people own. Each row changes one "
      "input in `params.json` and re-solves with and without the revolver. CE change is against the main case "
      f"(${fm(b0['ce'], 2)}bn).")
    w("")
    w("| Input changed | Owner | Root decision (R1) | First crisis year D>C (R1) | CE change ($bn) | Revolver value ($bn) | P(PE sale) R1 / R0 | P(fire sale) R1 / R0 | P(red event) R1 / R0 | Max λ R1 / R0 |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    w(f"| Main case | - | {acts_text(b0['root_labels'])} | {acts_text(b0['plan_D>C']['labels'])} | - | {dce_rev:+.3f} | "
      f"{pct(b0['P_pe_sale'])} / {pct(res['cases']['no_revolver']['brief']['P_pe_sale'])} | "
      f"{pct(b0['P_fire_sale'])} / {pct(res['cases']['no_revolver']['brief']['P_fire_sale'])} | "
      f"{pct(b0['P_red_event'])} / {pct(res['cases']['no_revolver']['brief']['P_red_event'])} | "
      f"{pct(b0['max_lambda_decision_nodes'])} / {pct(res['cases']['no_revolver']['brief']['max_lambda_decision_nodes'])} |")
    for s in res["sensitivity"]:
        a, b = s["R1"], s["R0"]
        if a is None or b is None:
            w(f"| {s['label']} | {s['owner']} | {s['status_R1']} | - | - | - | - | - | - | - |")
            continue
        dce = "n/a (other utility)" if s["ce_change_vs_base_bn"] is None else f"{s['ce_change_vs_base_bn']:+.3f}"
        w(f"| {s['label']} | {s['owner']} | {acts_text(a['root_labels'])} | "
          f"{acts_text(a['plan_D>C']['labels']) if 'plan_D>C' in a else '-'} | {dce} | {s['revolver_value_bn']:+.3f} | "
          f"{pct(a['P_pe_sale'])} / {pct(b['P_pe_sale'])} | {pct(a['P_fire_sale'])} / {pct(b['P_fire_sale'])} | "
          f"{pct(a['P_red_event'])} / {pct(b['P_red_event'])} | {pct(a['max_lambda_decision_nodes'])} / "
          f"{pct(b['max_lambda_decision_nodes'])} |")
    w("")
    w("What the table says:")
    w("")
    sv = {s["id"]: s for s in res["sensitivity"]}
    if "ic_lo_hard" in sv and sv["ic_lo_hard"]["R1"]:
        s = sv["ic_lo_hard"]
        w(f"- **A hard IC range brings back every v1 problem.** If the lower edge also binds in crisis years, the "
          f"program fire-sells PE (P = {pct(s['R1']['P_fire_sale'])} with the revolver, {pct(s['R0']['P_fire_sale'])} "
          f"without), λ reaches {pct(s['R0']['max_lambda_decision_nodes'])} without the revolver, and the revolver "
          f"is worth {money(s['revolver_value_bn'], 2)}. A CIO would breach a soft range before selling PE at 35% "
          f"(verify_finance.md H3); the elastic range does exactly that.")
    if "returns_means_only" in sv and sv["returns_means_only"]["R1"]:
        s = sv["returns_means_only"]
        w(f"- **Regime-predictable volatility makes the program time the market.** With equal means only, the first "
          f"crisis year's plan becomes '{acts_text(s['R1']['plan_D>C']['labels'])}' with λ = "
          f"{pct(max(s['R1']['plan_D>C']['lambda'] or 0, 0), 2)}, and the revolver is never drawn: the sale pays for "
          f"itself through the risk it removes, so it sells at the bottom for risk, not for cash. With v1's regime "
          f"means, CE falls by ${-sv['returns_v1']['ce_change_vs_base_bn']:.2f}bn and D>C becomes "
          f"'{acts_text(sv['returns_v1']['R1']['plan_D>C']['labels'])}'. The main case gives the program nothing to time.")
    for key, txt in (("target_free", "Without a price on the 8% target"), ("target_gross", "With the target counted gross of facility draws")):
        if key in sv and sv[key]["R1"]:
            s = sv[key]
            borrows = "LEVER" in s["R1"]["root_labels"]["corporate_finance"] or "LEVER" in s["R1"]["root_labels"]["pe_book"]
            how = ("the fund borrows to buy equities" if borrows else
                   f"the fund spends its buffer on equities (Treasury {pct(s['R1']['root_treasury_to_nav'])} of NAV today) "
                   f"and leans on the revolver later")
            w(f"- **{txt}** the root becomes '{acts_text(s['R1']['root_labels'])}' and the revolver is drawn on "
              f"{pct(s['R1']['P_revolver_drawn'])} of paths: {how}. That is v1's 'Treasury at the floor, levering "
              f"there' (verify_finance.md H6).")
    if "prices_075pct" in sv and sv["prices_075pct"]["R1"] and "prices_1pct" in sv and sv["prices_1pct"]["R1"]:
        s75, s1 = sv["prices_075pct"]["R1"], sv["prices_1pct"]["R1"]
        w(f"- **The appetite prices need to clear about 1%.** At 1% today's decision is "
          f"'{acts_text(s1['root_labels'])}' (Treasury {pct(s1['root_treasury_to_nav'])}), as at 2%; at 0.75% it becomes "
          f"'{acts_text(s75['root_labels'])}' and Treasury falls to {pct(s75['root_treasury_to_nav'])} of NAV, because a "
          f"cheaper target is worth breaching for the return on equities. Any price above that threshold gives the same "
          f"plan, so the exact number matters less than the IC's choice to treat 8% as a target.")
    if "psi_10" in sv and sv["psi_10"]["R1"]:
        s = sv["psi_10"]
        w(f"- **The terminal burden on unfunded commitments (ψ) is the one input that turns PACE-CUT on**: at ψ = 0.10 "
          f"the second crisis year reads '{acts_text(s['R1']['plan_D>C>C']['labels'])}'. CE changes by "
          f"{money(s['ce_change_vs_base_bn'], 2)}, so ψ deserves the estimation the architecture plans for it (§5.12).")
    if "omega_1" in sv and sv["omega_1"]["R1"]:
        w(f"- **Valuing crisis-leaf PE at the reported mark** (v1) adds {money(sv['omega_1']['ce_change_vs_base_bn'], 2)} "
          f"of certainty equivalent that does not exist (verify_finance.md M5).")
    if "gamma_5" in sv and sv["gamma_5"]["R1"]:
        w(f"- **Risk aversion** is the input that moves today's decision most: at γ = 5 the root becomes "
          f"{acts_text(sv['gamma_5']['R1']['root_labels'])}.")
    quiet = [s["label"] for s in res["sensitivity"] if s["R1"] and s["R1"]["root_labels"] == b0["root_labels"]
             and s["R1"]["P_pe_sale"] < 1e-9 and s["R0"]["P_pe_sale"] < 1e-9]
    if quiet:
        w(f"- **Inputs that leave today's decision unchanged and cause no PE sale** (they still move the certainty "
          f"equivalent and the contingent plans): {'; '.join(quiet)}.")
    w("")
    fl = res["downside_floor"]
    w("**Downside floors (a sensitivity, not part of the main case).** The architecture's Tier-1B floors apply to "
      "10-year windows, which a 3-year tree that starts in a drought cannot test. A 3-year floor would be a new limit "
      f"for the IC to set. Without one, the plan's CVaR10% is {pct(fl['no_floor']['cvar10_annualized'])} a year, and "
      f"the best any policy can reach is {pct(fl['best_attainable_cvar10_annualized'])} a year. In every row a PE "
      "sale at the root is held at zero and priced by a forced re-solve, so a tail row is never met with a red-tier "
      "sale without the IC seeing it:")
    w("")
    w("| CVaR10% floor (a year) | Binds? | Price of $1 of floor (today's $) | CE cost ($bn) | Root decision | P(any PE sale) | P(red event) | Forced re-solve with a root PE sale |")
    w("|---|---|---|---|---|---|---|---|")
    for r in fl["rows"]:
        if r["status"] != "Optimal":
            fr = r.get("forced_root_pe")
            w(f"| {pct(r['floor_annual'])} | infeasible without a root PE sale | - | - | - | - | - | "
              f"{acts_text(fr['labels']) if fr else 'infeasible'} |")
            continue
        fr = r.get("forced_root_pe")
        if fr is None:
            forced_txt = "-"
        elif abs(fr["ce_gain_bn"]) < 5e-4:
            forced_txt = "adds nothing (no root PE sale wanted)"
        else:
            forced_txt = f"{acts_text(fr['labels'])}, {fr['ce_gain_bn']:+.3f}bn"
        w(f"| {pct(r['floor_annual'])} | {'yes' if r['binding'] else 'no'} | {r['shadow_value_root_usd_per_usd']:.3f} | "
          f"{r['ce_cost_bn']:.2f} | {acts_text(r['root_labels'])} | {pct(r['P_pe_sale'])} | {pct(r['P_red_event'])} | "
          f"{forced_txt} |")
    w("")
    w("v1's floor of −3.9% a year was set just above the unconstrained tail so that it would bind. Here it would be "
      "slack. A floor that binds is cheap at first and then expensive: near the best attainable tail the program sells "
      "the liquid book far below the IC range, and contingent PE sales (red events) appear.")
    w("")

    # ---- 8. who decides ----
    w("## 8. What people set, what the program computes")
    w("")
    w("| Set by people (inputs and limits, in params.json, each with an owner) | Computed by the program (no judgement) |")
    w("|---|---|")
    w("| Regime probabilities, regime returns and the CMA mean and volatility (scenario engine; CRO validates) | Every decision at every node |")
    w("| Secondary discounts, loan spreads, LTV and pledge caps, facility availability (market data; Corporate Finance) | λ and the state price at every node |")
    w("| Owner draw rule: 5-10% of NAV, higher when oil is weak (owner; Corporate Finance forecasts) | Which limits bind, and what each costs |")
    w("| Hard limits: 4% floor, 1.30x exposure, synthetic budget, IC range edges (IC) | Probabilities of every outcome, CE, CVaR, P(red event) |")
    w("| Appetite prices: 8% target and IC range shortfalls (IC); terminal PE value and unfunded burden (TPA) | The rolling policy, the horizon test and every sensitivity |")
    w("| Which facilities are signed (consent scenarios: Corporate Finance, banks, owner) | How decisions and prices change if a facility is not signed |")
    w("| Approval of the root decision, and of any red-tier sale (forced re-solve) | The forced re-solve that prices a held red-tier sale |")
    w("")

    # ---- 9. the LP ----
    rm = res["meta"]["return_matrices"]
    w("## 9. The program, written out")
    w("")
    w("Per decision node n (13 nodes): post-decision states C (unencumbered cash), L (physical liquid), P (PE NAV, "
      "reported), U (unfunded), BR (revolver), BN (NAV loan), X (synthetic notional); trades sL, bL (sell / buy "
      "liquid), cv (P2S: physical to synthetic), uw (unwind), lev (synthetic LEVER, fixed at 0 by the doctrine), sP "
      "(sell PE), cut (pacing cut); s8 and sb (priced shortfalls below the 8% target and the IC range). Per leaf ℓ "
      "(27): settlement trades sL, bL, sP, facility moves, s8, sb, and terminal wealth W~.")
    w("")
    w("```text")
    w("max  Σ_ℓ p_ℓ u_ℓ,   u_ℓ ≤ U(w_k) + U'(w_k)(W~_ℓ/W0 − w_k)              k = 1..10 tangents of CRRA(3)")
    w("cash  C_n = (1+r)C_p + (1+r)h_p X_p + (rL_n − r − s_X,p)X_p + δ_n P_p − q_n U_p + y_n Y_p − d_n·NAV_p")
    w("            − (r+s_R)BR_p − f_R(Lim−BR_p) − (r+s_N,p)BN_p")
    w("            + (1−τ)(sL_n + cv_n) − (1+τ)(bL_n + uw_n) + (1−disc_n)sP_n + (BR_n−BR_p) + (BN_n−BN_p) − h_n X_n")
    w("liq   L_n = (1+rL_n)L_p − sL_n + bL_n − cv_n + uw_n;      X_n = X_p + cv_n − uw_n + lev_n,  uw_n ≤ X_p")
    w("PE    P_n = (1+rP_n−δ_n)P_p + q_n U_p − sP_n;              U_n = (1−q_n)U_p + (plan − cut_p) − κ_U sP_n")
    w("hard  C_n ≥ 0.04·NAV_n   (NAV_n = C + hX + L + P + Y − BR − BN)                      every node, t = 3 too")
    w(f"      BN_n ≤ LTV_n·{prm['actions']['nav_loan_pledge_pool_frac']:.2f}·(P_n + Y_n);  BR_n ≤ avail_n·Lim;  "
      f"L+X ≤ {prm['limits']['liquid_exposure_max_frac']:.2f}·NAV_n                    every node, t = 3 too")
    w(f"      L+P+Y+X ≤ {prm['actions']['exposure_cap']:.2f}·NAV_n;  X_n ≤ {prm['actions']['synthetic_notional_cap']:g};  "
      f"cut_n ≤ {1 - prm['actions']['pacing_core_sleeve']:.2f}·plan                       decision nodes")
    w("      BR_ℓ ≤ BR_p;  BN_ℓ ≤ BN_p   (debt can be repaid at t = 3, not drawn)                  leaves")
    w("appetite  C_n − BR_n − BN_n + s8_n ≥ 0.08·NAV_n;   L_n + X_n + sb_n ≥ "
      f"{prm['limits']['liquid_exposure_min_frac']:.2f}·NAV_n          every node, priced in W~")
    w("W~_ℓ = C + L + ω_ℓ·P + Y − BR − BN − ψ·U − c_PACE·Σcut − Σ_k π_k(s8_k + sb_k) + Σ_t d_t·NAV_{t−1}·G_{t→3}")
    w("```")
    w("")
    w(f"p = parent node, n = the node (its regime sets the year's rates). π_k = 2¢ a year at N and D nodes and at "
      f"t = 3, 0 in a crisis year; ω = 1 except 0.90 after a crisis year; ψ = "
      f"{prm['terminal']['unfunded_burden_per_dollar']}. The owner draw d_n·NAV_p is a fixed liability of the year. "
      "No variable can skip it, so it is paid in full by construction.")
    w("")
    w("Returns by (previous regime → this year's regime), computed from params.json so that next year's mean and "
      "volatility are the same from every regime (liquid book CMA 7.2%, PE 9.6%):")
    w("")
    w("| Previous year | Liquid: to N | to D | to C | PE NAV: to N | to D | to C |")
    w("|---|---|---|---|---|---|---|")
    for i in REGIMES:
        w(f"| {i} | {pct(rm['liquid_R_prev_to_this_regime'][i]['N'])} | {pct(rm['liquid_R_prev_to_this_regime'][i]['D'])} | "
          f"{pct(rm['liquid_R_prev_to_this_regime'][i]['C'])} | {pct(rm['pe_R_prev_to_this_regime'][i]['N'])} | "
          f"{pct(rm['pe_R_prev_to_this_regime'][i]['D'])} | {pct(rm['pe_R_prev_to_this_regime'][i]['C'])} |")
    w("")
    w("So a crisis after a calm year is a deeper loss than a crisis after a crisis, and nothing in the tree lets the "
      "program forecast a better or calmer year from today's regime.")
    w("")

    # ---- 10. what changed ----
    w("## 10. What changed in version 2, and why")
    w("")
    w("Every critical and high finding of `verify_finance.md` and `verify_math.md` is addressed, and so are the "
      "medium ones. The low ones are addressed where the fix was cheap; the rest are listed as open.")
    w("")
    w("| Finding | Change in v2 | Where to see it |")
    w("|---|---|---|")
    for row in V2_CHANGES:
        w(f"| {row[0]} | {row[1]} | {row[2]} |")
    w("")
    w("**Still open (stated, not fixed):**")
    w("")
    for item in V2_OPEN:
        w(f"- {item}")
    w("")

    # ---- 11. checks ----
    ck = res["checks"]
    w("## 11. Checks run by tree_demo.py")
    w("")
    sla = ck["min_slack_by_row_family_with_revolver"]
    w(f"- Probabilities sum to 1 at every stage: {ck['probability_sum_by_stage']}.")
    w(f"- Every identity, recomputed from the reported states (not the LP rows): opening stocks from the parent's "
      f"closing stocks and the year's rates; closing stocks from the opening stocks and the trades; the owner draw "
      f"= draw rate × the parent's closing NAV. The largest residual is {ck['max_identity_residual_bn']:.1e}bn. "
      f"Terminal wealth: LP against recomputed {ck['max_wealth_lp_vs_recomputed_bn']:.1e}bn.")
    w(f"- Every limit at every node, both consent scenarios: all hold = {ck['all_limits_hold']} (smallest slack by "
      f"family, revolver case: " + "; ".join(f"{k} {v_:.1e}" for k, v_ in sla.items()) + ").")
    w(f"- Duals: finite-difference re-solves on {ck['dual_fd_rows_checked']} rows (every decision node's cash row, "
      f"binding limits, some leaves) agree with the LP duals to a relative {ck['dual_fd_max_rel_err']:.1e}. λ was "
      f"also recomputed with a direct carry re-solve at every decision node (inject $1 and tighten the floor and the "
      f"target so it cannot relieve them). That replaces v1's circular reduced-cost check, and it agrees to "
      f"{ck['lambda_carry_resolve_max_abs_diff']:.1e}. Kink probes at ± ${prm['settings']['kink_probe_bn']}bn: "
      f"{'none near a kink' if not ck['nodes_near_a_kink'] else ', '.join(ck['nodes_near_a_kink'])}.")
    pd_ = ck["pwl_decision_test_48_tangents"]
    w(f"- Piecewise-linear utility: largest error at the leaves {ck['pwl_utility_max_abs_error_at_leaves']:.1e} (a "
      f"level bias of ${ck['pwl_ce_bias_bn']:.2f}bn in certainty equivalent; every comparison uses the exact CRRA). "
      f"Re-solved with 48 tangents: certainty equivalent {pd_['exact_ce_48_tangents_bn']:.3f} against "
      f"{pd_['exact_ce_10_tangents_bn']:.3f}. The root decision moves by ${pd_['root_max_abs_decision_diff_bn']:.2f}bn. "
      f"The largest move anywhere is ${pd_['largest_decision_diff_bn']:.2f}bn at {pd_['largest_decision_diff_node']} "
      f"({acts_text(pd_['labels_10_at_that_node'])} against {acts_text(pd_['labels_48_at_that_node'])}), a node where "
      f"the two funding mixes are worth the same to within the certainty-equivalent difference above.")
    w(f"- Time consistency: re-solving each year-1 subtree reproduces the plan to "
      f"{ck['time_consistency_max_decision_diff_bn']:.1e}bn.")
    w(f"- Deterministic: single-threaded dual simplex, fixed seed, no sampling; results.json hash "
      f"`{res['meta']['content_sha256_before_this_field'][:16]}…`.")
    w("")

    # ---- Verification ----
    w("## Verification (independent re-implementation)")
    w("")
    vpath = HERE / "verification.json"
    ver = None
    if vpath.exists():
        try:
            ver = json.loads(vpath.read_text(encoding="utf-8"))
        except Exception:
            ver = None
    if ver is None or ver.get("results_sha256") != res["meta"]["content_sha256_before_this_field"]:
        w("Pending: run `verify_independent.py` to re-solve this results.json independently. "
          + ("(verification.json belongs to an earlier run.)" if ver is not None else ""))
    else:
        for line_ in ver.get("markdown_lines", []):
            w(line_)
    w("")
    (HERE / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")


V2_CHANGES = [
    ("Horizon effects drive the t = 2 plans and the 0% fire-sale headline (finance H1, math 1)",
     "Horizon nodes keep every hard row (4% floor, LTV and availability of the leaf's regime with forced paydowns), "
     "allow no new borrowing, and price what is left below the 8% target and the IC range; PE at economic value (ω), "
     "unfunded burden ψ > 0; horizon-node balance sheets reported; 2/3/4-year horizon test",
     "§§1, 3, 6"),
    ("Probabilities describe the static plan, not the rolling policy (H2)",
     "The rolling policy is simulated: re-solve at all 12 nodes of years 1-2, execute the first decision, settle at "
     "t = 3; its statistics sit beside the plan's", "§§3, 5"),
    ("A hard 27% IC edge drives fire sales, the Phase I deficit and the revolver value (H3)",
     "The IC lower edge is elastic (2¢ a year per $ below it, free in a crisis year); Phase I reports IC-range "
     "shortfalls apart from Tier 1A; the cause of the timing it masked is removed (M2); 27 / 24 / 20% and v1's hard "
     "edge in §7", "§§4, 7"),
    ("The naive-rule gap is caused by the band (H4)",
     "Naive rules face the same flows, limits and charges and sell liquid below the range before any PE; a revolver "
     "variant; the lead is decomposed into revolver access and optimization", "§3"),
    ("Revolver draws that fund purchases are labelled REFINANCE (H5)",
     "P2S, unwind and synthetic LEVER are separate columns; a draw that pays for purchases is labelled LEVER; the "
     "exposure change is read against the parent's position", "§§1, 2"),
    ("Treasury at the 4% floor in most t = 2 states, levering there; no 8% target or CFP stages (H6)",
     "8% own-liquidity target (net of facility draws), elastic and priced; CFP stage at every node; the doctrine "
     "(beta has α* < 0) keeps synthetic LEVER at zero; no liquid-book purchases in a crisis year (the CFP Red "
     "playbook adds no risk), and the target makes borrowed purchases costly elsewhere; P(LEVER while CFP Red or "
     "Black) is reported", "§§1-3, 7"),
    ("λ not highest in crisis, unexplained (M1)", "λ against m explained; λ uses the full liquidity dual mass (floor and "
     "target); one-sided prices probed at ± $0.5bn for kinks", "§2"),
    ("The liquid book times regimes and sells at the bottom (M2)",
     "Next year's expected return and volatility are the same from every regime (CMA mean, start-regime volatility); "
     "turnover and binding edges reported; the rebound rationale removed", "§§7, 9"),
    ("Owner draw far from the research (M3)", "N and D draw 5.8% ($10.3bn, inside the research's $9.9-10.8bn); a "
     "crisis with an oil shock 7.5%; the 10% cap and v1's draws as sensitivities", "§7"),
    ("NAV-loan capacity 2.5-3x the architecture's cap (M4)", "Pledge pool capped at 20% of private NAV: $2.1bn at 10% "
     "LTV, $1.1bn at 5%; v1's capacity as a sensitivity", "§7"),
    ("PE valued at stale marks in crisis leaves (M5)", "Economic value 90% of the mark after a crisis year; the 35% "
     "crisis discount labelled a stress case and 25% shown", "§§3, 7"),
    ("PACE-CUT never chosen because ψ = 0 (M6)", "ψ = 2¢ stated with a sensitivity (0 and 10¢); corridor with a 25% "
     "protected core sleeve; break-even printed", "§§2, 7"),
    ("CVaR floor tuned to bind (M7); root decision a corner of two tuned limits (math 4)",
     "No floor in the main case; floors from −4% to +0.5% a year as a sensitivity, with root PE sales held at zero and "
     "priced by forced re-solve; 'Tier 1B' label dropped; today's decision now sits at the 8% target, and §7 shows "
     "how it moves with every input", "§7"),
    ("Math 2 and 3: λ read as 'about the loan spread'; recovery mode drops the floor by a hard-coded rule",
     "λ ≈ (1 − f)/(1 + r) × net cost of the marginal source, with the ranges read from this run; no floor in the main "
     "case or the rolling policy, so no recovery mode is triggered, and an unattainable floor in §7 is reported with "
     "its forced re-solve", "§§2, 5, 7"),
    ("Red-event test (ADR-39) not applied (M8)", "P(red event) in every outcome column; the root red-tier SELL rule "
     "(today's stage is computed: Green); re-solves at Amber or worse hold root PE sales at zero", "§§3, 5"),
    ("No sensitivity table (M9)", "One-at-a-time table with the owner of each input", "§7"),
    ("Low: crisis persistence 40% (L1)", "30% (17-month mean spell); 40% as a sensitivity", "§7"),
    ("Low: terminal risk metrics missing (L3)", "LR8, NAV drawdown, Treasury, liquid share and debt per leaf", "§3"),
    ("Low: SYNTHETIC labels (L4); coarse probabilities (L5); naive breaches (L6, math 5)",
     "Tagged headings; coarseness stated; naive rules trim to the upper edge and report breaches", "§3"),
    ("Low: flat synthetic financing (L7)", "30 / 81 / 175bp by regime", "params.json"),
    ("Math: circular stationarity check (6); 8-digit rounding (7); hard-coded settings (8); LEVER label on the stock (9)",
     "Direct carry re-solve; 12 significant digits and per-node residuals; thresholds moved to params.json "
     "'settings'; labels read changes against the parent", "§11; results.json"),
]

V2_OPEN = [
    "The yield book ($40bn) still has no levers (verify_finance.md L2): amber sales of private credit and the SMA "
    "run-off are not modelled, so the waterfall goes from liquid assets and facilities straight to PE.",
    "Covenant risk on the revolver after a large NAV fall is not modelled (L7).",
    "Three branches a year are coarse: the tree's volatility is set to the start regime's (9.5% liquid, 7.6% reported "
    "PE), below a real blended book's. Results that depend on tails (CVaR, P(red event)) should be read as "
    "illustrations. More scenarios per node (M2's second fix) would cost the 40-node picture.",
    "ψ, ω and the two appetite prices are stated values with sensitivities. The architecture estimates terminal "
    "values by regression on simulated paths (§5.12), which this toy does not have.",
    "Contingent plans at t ≥ 1 are not unique where two funding mixes are worth the same (section 11). Only the root "
    "decision is executed, and it is unique and horizon-invariant here.",
]


# =============================================================================================
# 10. Main
# =============================================================================================
def main():
    t_start = time.perf_counter()
    raw, v = load_params(HERE / "params.json")
    H = int(v["tree"]["decision_stages"])
    root = root_state_t0(v)
    W0 = root["C"] + root["L"] + root["P"] + root["Y"]
    saa = saa_weights(v)
    nodes = build_tree(v, v["tree"]["start_regime"], H, root["Y"], saa)
    lim = float(v["actions"]["revolver_limit"])
    c_floor = v["limits"].get("cvar_floor_annual_return")
    F = None if c_floor is None else W0 * (1.0 + c_floor) ** H
    eps = S(v, "action_threshold_bn")
    checks = {}
    checks["probability_sum_by_stage"] = {str(t): sum(n.prob for n in nodes if n.stage == t) for t in range(H + 1)}
    assert all(abs(x - 1.0) < 1e-12 for x in checks["probability_sum_by_stage"].values())
    RL, RP = return_adjustments(v)
    _, mL = return_matrix(v, "liquid_return", "liquid_expected_return", "liquid_volatility")
    _, mP = return_matrix(v, "pe_nav_return", "pe_expected_return", "pe_volatility")
    stage0, _ = opening_stage(v, root)

    # ---- main case: revolver signed (consent scenario R1), and no signed revolver (R0) --------
    main_a, raw_a = run_case(v, nodes, root, W0, lim, cvar_floor=F)
    assert main_a is not None, f"main case: {raw_a[1].status}"
    main_b, raw_b = run_case(v, nodes, root, W0, 0.0, cvar_floor=F)
    assert main_b is not None, f"no-revolver case: {raw_b[1].status}"

    # ---- Phase I for both consent scenarios -------------------------------------------------
    ph1_a = run_phase1(v, nodes, root, W0, lim)
    ph1_b = run_phase1(v, nodes, root, W0, 0.0)

    # ---- naive rules -------------------------------------------------------------------------
    nv = v["naive_rule"]
    naive = {}
    for tag, tgt, lm, rf in (("naive_8pct", nv["cash_target_frac"], 0.0, False),
                             ("naive_8pct_revolver", nv["cash_target_frac"], lim, True),
                             ("naive_4pct", nv["variant_cash_target_frac"], 0.0, False)):
        if tag == "naive_8pct_revolver" and not nv.get("revolver_first_variant", True):
            continue
        rep_n, _, inf_n, br_n = simulate_naive(v, nodes, root, tgt, W0, lim=lm, revolver_first=rf)
        naive[tag] = {"rep": rep_n, "summ": summarize(v, nodes, rep_n, W0), "infeasible": inf_n,
                      "ic_upper_edge_breaches": br_n, "cash_target_frac": tgt, "revolver": lm > 0}

    # ---- closed loop: the rolling policy -----------------------------------------------------
    cl_rep, cl_details = closed_loop(v, nodes, root, W0, lim, main_a, saa)
    cl_summ = summarize(v, nodes, cl_rep, W0)
    cl_rep_b, cl_details_b = closed_loop(v, nodes, root, W0, 0.0, main_b, saa)
    cl_summ_b = summarize(v, nodes, cl_rep_b, W0)

    # ---- horizon test, sensitivities, downside floors -----------------------------------------
    horizon = run_horizon_test(v, root, W0, saa)
    base_brief_a, base_brief_b = case_brief(v, nodes, main_a), case_brief(v, nodes, main_b)
    sens = run_sensitivities(v, root, W0, saa, base_brief_a)
    floors = run_floor_table(v, nodes, root, W0, lim, main_a)

    # ---- duals: finite differences, carry re-solve, kinks ------------------------------------
    fd, carry, kinks = dual_checks(v, nodes, main_a)
    kink_by_path = {k["path"]: k for k in kinks}
    for r in main_a.rep:
        if r["path"] in kink_by_path:
            r["duals"]["near_kink_within_probe"] = kink_by_path[r["path"]]["near_kink"]
    tc = time_consistency(v, nodes, root, W0, lim, main_a, saa)

    # ---- consistency checks -------------------------------------------------------------------
    sl_a, rs_a = limit_slacks(v, nodes, main_a.rep, lim)
    sl_b, rs_b = limit_slacks(v, nodes, main_b.rep, 0.0)
    checks["min_slack_by_row_family_with_revolver"] = sl_a
    checks["max_identity_residual_with_revolver"] = rs_a
    checks["min_slack_by_row_family_no_revolver"] = sl_b
    checks["max_identity_residual_no_revolver"] = rs_b
    checks["all_limits_hold"] = min(min(sl_a.values()), min(sl_b.values())) >= -1e-9
    checks["max_identity_residual_bn"] = max(max(rs_a.values()), max(rs_b.values()))
    checks["max_wealth_lp_vs_recomputed_bn"] = max(abs(r["terminal"]["W_tilde"] - r["terminal"]["W_tilde_lp"])
                                                   for r in main_a.rep + main_b.rep if "terminal" in r)
    g = v["objective"]["crra_gamma"]
    leaves_a = [n for n in nodes if n.stage == H]
    pwl = []
    for n in leaves_a:
        w = main_a.rep[n.id]["terminal"]["W_tilde"] / W0
        pwl.append(min(crra(t, g) + crra_prime(t, g) * (w - t) for t in main_a.tan) - crra(w, g))
    checks["pwl_utility_max_abs_error_at_leaves"] = float(max(abs(e) for e in pwl))
    eu_pwl = sum(n.prob * (crra(main_a.rep[n.id]["terminal"]["W_tilde"] / W0, g) + e) for n, e in zip(leaves_a, pwl))
    checks["pwl_ce_bias_bn"] = float(W0 * ((1 - g) * eu_pwl) ** (1 / (1 - g))
                                     - main_a.summ["certainty_equivalent_W_tilde"])
    v48 = apply_changes(v, {"objective.n_tangents": 48})
    c48, _ = run_case(v48, nodes, root, W0, lim, cvar_floor=F)
    diffs48 = sorted(((max(abs(c48.rep[r["id"]]["decisions"][k] - r["decisions"][k]) for k in DEC_KEYS), r["path"])
                      for r in main_a.rep if r["stage"] < H), reverse=True)
    checks["pwl_decision_test_48_tangents"] = {
        "exact_ce_10_tangents_bn": main_a.summ["certainty_equivalent_W_tilde"],
        "exact_ce_48_tangents_bn": c48.summ["certainty_equivalent_W_tilde"],
        "root_labels_10": main_a.rep[0]["labels"], "root_labels_48": c48.rep[0]["labels"],
        "root_max_abs_decision_diff_bn": diffs48[[p_ for _, p_ in diffs48].index(nodes[0].path)][0],
        "largest_decision_diff_bn": diffs48[0][0], "largest_decision_diff_node": diffs48[0][1],
        "labels_10_at_that_node": main_a.rep[node_by_path(nodes, diffs48[0][1]).id]["labels"],
        "labels_48_at_that_node": c48.rep[node_by_path(nodes, diffs48[0][1]).id]["labels"]}
    checks["dual_fd_max_rel_err"] = max(d["rel_err_vs_nearest_side"] for d in fd)
    checks["dual_fd_rows_checked"] = len(fd)
    checks["lambda_carry_resolve_max_abs_diff"] = max((c["abs_diff"] or 0.0) for c in carry)
    checks["nodes_near_a_kink"] = [k["path"] for k in kinks if k["near_kink"]]
    checks["time_consistency_max_decision_diff_bn"] = max(t["max_abs_decision_difference_bn"] for t in tc)
    checks["naive_rule_infeasible_nodes"] = {k: x["infeasible"] for k, x in naive.items()}

    # ---- revolver comparison ------------------------------------------------------------------
    comparison = []
    for ra, rb in zip(main_a.rep, main_b.rep):
        if ra["stage"] == H:
            continue
        flips = {bk: {"with_revolver": ra["labels"][bk], "no_revolver": rb["labels"][bk]}
                 for bk in ("liquid_book", "pe_book", "corporate_finance") if ra["labels"][bk] != rb["labels"][bk]}
        comparison.append({"path": ra["path"], "probability": ra["probability"],
                           "lambda_with_revolver": ra["duals"]["liquidity_premium_lambda"],
                           "lambda_no_revolver": rb["duals"]["liquidity_premium_lambda"],
                           "m_with_revolver": ra["duals"]["state_price_m"], "m_no_revolver": rb["duals"]["state_price_m"],
                           "closing_cash_with": ra["closing_state"]["C"], "closing_cash_without": rb["closing_state"]["C"],
                           "label_changes": flips})

    # ---- assemble results.json ---------------------------------------------------------------
    edges = []
    for n in nodes[1:]:
        r = main_a.rep[n.id]
        edges.append({"from": n.parent, "to": n.id, "from_path": nodes[n.parent].path, "to_path": n.path,
                      "regime": n.regime, "transition_probability": n.cond_prob,
                      "liquid_return": n.rL, "pe_nav_return": n.rP, "yield_total_return": n.yY + n.gY,
                      "pe_distribution_rate": n.dist, "pe_call_rate": n.call, "owner_draw_rate": n.draw,
                      "flows_bn_with_revolver": {k: r["exogenous_flows"][k] for k in
                                                 ("owner_draw", "pe_calls", "pe_distributions", "yield_cash")}})
    mu0 = main_a.s.dual("cash[0]")
    sa, sb_, sn = main_a.summ, main_b.summ, {k: x["summ"] for k, x in naive.items()}
    decomposition = {
        "program_R1_minus_naive_8pct_ce_bn": sa["certainty_equivalent_W_tilde"] - sn["naive_8pct"]["certainty_equivalent_W_tilde"],
        "revolver_value_for_the_program_ce_bn": sa["certainty_equivalent_W_tilde"] - sb_["certainty_equivalent_W_tilde"],
        "program_R0_minus_naive_8pct_ce_bn": sb_["certainty_equivalent_W_tilde"] - sn["naive_8pct"]["certainty_equivalent_W_tilde"],
    }
    if "naive_8pct_revolver" in sn:
        decomposition["program_R1_minus_naive_8pct_revolver_ce_bn"] = (
            sa["certainty_equivalent_W_tilde"] - sn["naive_8pct_revolver"]["certainty_equivalent_W_tilde"])
        decomposition["revolver_value_for_the_naive_rule_ce_bn"] = (
            sn["naive_8pct_revolver"]["certainty_equivalent_W_tilde"] - sn["naive_8pct"]["certainty_equivalent_W_tilde"])
    undrawn_fee_3y = v["actions"]["revolver_undrawn_fee"] * lim * H
    results = {
        "meta": {
            "label": "SYNTHETIC. Illustrative teaching example; not ADIC data and not a forecast.",
            "title": "ADIC multi-period tree: worked example",
            "version": "2 (corrections from verify_math.md and verify_finance.md)",
            "generated_by": "examples/tree_demo/tree_demo.py",
            "units": "$bn; annual stages; decisions at t = 0, 1, 2; horizon t = 3",
            "solver": f"HiGHS {highspy.Highs().version()} dual simplex via highspy (basic solution, exact duals)",
            "tree": {"regimes": REGIME_NAME, "start_regime": v["tree"]["start_regime"], "nodes": len(nodes),
                     "decision_nodes": sum(1 for n in nodes if n.stage < H), "leaves": len(leaves_a),
                     "probability_sum_by_stage": checks["probability_sum_by_stage"]},
            "W0": W0,
            "lp_size_main_case": {"columns": len(main_a.lp.vnames), "rows": len(main_a.lp.rnames),
                                  "nonzeros": main_a.s.nnz, "simplex_iterations": main_a.s.iters},
            "lp_objective_expected_pwl_utility": main_a.s.obj / OBJ_SCALE,
            "utility_tangents_W_over_W0": list(main_a.tan),
            "return_matrices": {"liquid_R_prev_to_this_regime": RL, "pe_R_prev_to_this_regime": RP,
                                "liquid_row_mean_and_sd_before_mapping": mL, "pe_row_mean_and_sd_before_mapping": mP},
            "root_event_stage": stage0, "root_pe_rule": main_a.root_pe_rule,
            "root_pe_sell_held_at_zero": main_a.forced is not None,
            "parameters": v,
            "parameter_rationales": {sec: {k: {kk: it[kk] for kk in ("rationale", "source", "unit") if kk in it}
                                           for k, it in body.items()}
                                     for sec, body in raw.items() if not sec.startswith("_")},
            "definitions": {
                "W_tilde": "terminal wealth: cash + liquid + omega x PE NAV + yield NAV - debt - psi x unfunded - "
                           "pacing charges - appetite charges (8% target and IC range shortfalls) + owner draws paid, "
                           "each grown to t = 3 at the path's static-allocation return",
                "annualized_return": "(W_tilde / W0)^(1/3) - 1: the 3-year total return with draws counted",
                "mu_cash_utility_per_bn": "dual of node n's cash-balance row: expected utility per extra $1bn at n",
                "state_price_m": "mu_n / (p_n * mu_0): today's value of $1 arriving at node n, per unit of probability",
                "liquidity_premium_lambda": "M_n / (mu_n - M_n) with M_n the dual mass of n's liquidity rows (4% floor and "
                                            "8% target) on its cash (ARCHITECTURE.md 5.6): how much more $1 of cash "
                                            "is worth at n than the same dollar carried forward",
                "cfp_stage": "worse of Treasury / NAV (8 / 6 / 4%) and physical liquid share (28 / 24 / 20%), after "
                             "the node's actions",
                "red_event": "a PE sale while the CFP stage is Amber or worse, while own liquidity is below the 8% "
                             "target, or at a bid below 90% of the normal bid (ADR-39)",
                "labels": "SELL / BUY on the liquid book; REFINANCE (P2S) converts physical to synthetic, exposure "
                          "unchanged; LEVER adds exposure with borrowed or synthetic money; SELL / REFINANCE (NAV loan) "
                          "/ PACE-CUT on the PE book; REFINANCE (revolver) for Corporate Finance; a draw that pays for "
                          "purchases is LEVER; amounts in $bn",
                "certainty_equivalent": "W such that U(W/W0) = E[U(W_tilde/W0)] with the exact CRRA(3)",
            },
        },
        "nodes": main_a.rep,
        "edges": edges,
        "cases": {
            "with_revolver": {"consent_scenario": "R1: committed $15bn revolver signed", "status": main_a.s.status,
                              "root_pe_rule": main_a.root_pe_rule, "summary": strip(sa), "phase1": ph1_a,
                              "brief": base_brief_a, "nodes_compact": [compact_node(r) for r in main_a.rep]},
            "no_revolver": {"consent_scenario": "R0: no signed facility (revolver limit 0)", "status": main_b.s.status,
                            "root_pe_rule": main_b.root_pe_rule, "root_pe_sell_held_at_zero": main_b.forced is not None,
                            "lp_objective_expected_pwl_utility": main_b.s.obj / OBJ_SCALE,
                            "utility_tangents_W_over_W0": list(main_b.tan),
                            "summary": strip(sb_), "phase1": ph1_b,
                            "brief": base_brief_b, "nodes": main_b.rep,
                            "terminal_distribution": sb_["terminal_distribution"],
                            "comparison_with_revolver": comparison,
                            "revolver_value_ce_bn": decomposition["revolver_value_for_the_program_ce_bn"],
                            "undrawn_fee_over_3_years_bn": undrawn_fee_3y},
        },
        "closed_loop": {
            "what": "The rolling policy: the root decision is executed; every t = 1 and t = 2 node re-solves a fresh "
                    "3-year tree from its realized state with the same rules and executes only its first decision; "
                    "t = 3 settles with the horizon rows.",
            "with_revolver": {"summary": strip(cl_summ), "resolves": cl_details,
                              "nodes_compact": [compact_node(r) for r in cl_rep],
                              "terminal_distribution": cl_summ["terminal_distribution"]},
            "no_revolver": {"summary": strip(cl_summ_b), "resolves": cl_details_b},
        },
        "summary": strip(sa) | {"terminal_distribution": sa["terminal_distribution"]},
        "naive_rules": {
            "rule": raw["naive_rule"]["cash_target_frac"]["rationale"],
            **{k: {"cash_target_frac": x["cash_target_frac"], "revolver": x["revolver"], "summary": strip(x["summ"]),
                   "nodes_compact": [compact_node(r) for r in x["rep"]], "infeasible_nodes": x["infeasible"],
                   "ic_upper_edge_breaches": x["ic_upper_edge_breaches"]} for k, x in naive.items()},
            "decomposition": decomposition,
        },
        "horizon_test": horizon,
        "sensitivity": sens,
        "downside_floor": floors,
        "dual_checks": {"finite_differences": fd, "lambda_carry_resolve": carry, "kink_probes": kinks},
        "time_consistency_check": tc,
        "checks": checks,
    }
    results = rnd(results)
    body = json.dumps(results, indent=1, ensure_ascii=False, sort_keys=False)
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    results["meta"]["content_sha256_before_this_field"] = digest
    (HERE / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    write_results_md(results, nodes, H)
    elapsed = time.perf_counter() - t_start
    print(f"OK  status={main_a.s.status}  CE R1={sa['certainty_equivalent_W_tilde']:.3f}  "
          f"CE R0={sb_['certainty_equivalent_W_tilde']:.3f}  closed-loop CE={cl_summ['certainty_equivalent_W_tilde']:.3f}  "
          f"sha256={digest[:16]}  runtime={elapsed:.2f}s")
    return results, elapsed


if __name__ == "__main__":
    main()
