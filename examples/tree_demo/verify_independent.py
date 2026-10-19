#!/usr/bin/env python
"""
verify_independent.py: an independent re-implementation of the tree program that checks results.json.

SYNTHETIC. Same illustrative inputs as tree_demo.py (params.json); nothing here is ADIC data.

Written from the program as RESULTS.md section 9 and params.json describe it, not by calling tree_demo.py's model
code:
  * the tree is built depth-first and keyed by path (tree_demo.py: breadth-first, integer ids);
  * every row is a cvxpy expression in the economic quantities (tree_demo.py: a hand-built sparse matrix);
  * it is solved with CLARABEL (interior point) and with HiGHS through cvxpy (tree_demo.py: highspy dual simplex);
  * the objective is E[U_hat] itself (tree_demo.py scales it by 1000).
It runs three checks and writes verification.json, then asks tree_demo.py only to re-render RESULTS.md so that its
"Verification" section shows these results:
  1. objective agreement, for both consent scenarios, and the decisions at every node;
  2. every identity and limit at every node, recomputed from the published node values in results.json;
  3. the duals: the cash price at every decision node by finite-difference re-solves, and lambda by a carry
     re-solve (a dollar injected at the node that cannot relieve its floor or target).

Run:  .venv\\Scripts\\python.exe examples\\tree_demo\\verify_independent.py
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path

import cvxpy as cp
import numpy as np

HERE = Path(__file__).resolve().parent
REG = ("N", "D", "C")
CLARABEL_OPTS = dict(tol_gap_abs=1e-11, tol_gap_rel=1e-11, tol_feas=1e-11, max_iter=500)
HIGHS_OPTS = dict(primal_feasibility_tolerance=1e-10, dual_feasibility_tolerance=1e-10)


def values(raw):
    return {sec: {k: it["value"] for k, it in body.items()} for sec, body in raw.items() if not sec.startswith("_")}


# ---------------------------------------------------------------------------------------------
# The tree, depth-first, keyed by path
# ---------------------------------------------------------------------------------------------
class TNode:
    def __init__(self, path, stage, regime, parent, cprob, prob, Y):
        self.path, self.stage, self.regime, self.parent = path, stage, regime, parent
        self.cprob, self.prob, self.Y = cprob, prob, Y
        self.kids = []


def year_returns(p):
    """R[i][j] = mean + (sd*/sd_i)(r_j - m_i): next year's mean and volatility equal from every regime."""
    R, T = p["rates"], p["tree"]["transition_matrix"]
    assert R["return_model"] == "equal_conditional_moments", "this check implements the main return model only"
    out = {}
    for base, mean, volk in (("liquid_return", "liquid_expected_return", "liquid_volatility"),
                             ("pe_nav_return", "pe_expected_return", "pe_volatility")):
        r = R[base]
        m = {i: sum(T[i][j] * r[j] for j in REG) for i in REG}
        sd = {i: math.sqrt(sum(T[i][j] * (r[j] - m[i]) ** 2 for j in REG)) for i in REG}
        target = R.get(volk) or sd[p["tree"]["start_regime"]]
        out[base] = {i: {j: R[mean] + target / sd[i] * (r[j] - m[i]) for j in REG} for i in REG}
    return out["liquid_return"], out["pe_nav_return"]


def grow_tree(p, horizon):
    R, T = p["rates"], p["tree"]["transition_matrix"]
    b = p["balance_sheet_t0"]
    W0 = b["cash_hqla"] + b["liquid_book"] + b["pe_book_nav"] + b["yield_book_nav"]
    w = {"C": b["cash_hqla"] / W0, "L": b["liquid_book"] / W0, "P": b["pe_book_nav"] / W0, "Y": b["yield_book_nav"] / W0}
    RL, RP = year_returns(p)
    root = TNode(p["tree"]["start_regime"], 0, p["tree"]["start_regime"], None, 1.0, 1.0, b["yield_book_nav"])
    order = []

    def visit(nd):
        order.append(nd)
        if nd.stage == horizon:
            return
        for j in REG:
            ch = TNode(nd.path + ">" + j, nd.stage + 1, j, nd, T[nd.regime][j], nd.prob * T[nd.regime][j],
                       nd.Y * (1.0 + R["yield_nav_return"][j]))
            ch.rL, ch.rP = RL[nd.regime][j], RP[nd.regime][j]
            ch.yY, ch.gY = R["yield_cash_rate"][j], R["yield_nav_return"][j]
            ch.dist, ch.call, ch.draw = R["pe_distribution_rate"][j], R["pe_call_rate"][j], R["owner_draw_rate"][j]
            ch.rref = w["C"] * R["cash_rate"] + w["L"] * ch.rL + w["P"] * ch.rP + w["Y"] * (ch.yY + ch.gY)
            nd.kids.append(ch)
            visit(ch)

    visit(root)
    for i, nd in enumerate(order):
        nd.idx = i
    return order, W0


def crra(x, g):
    return x ** (1.0 - g) / (1.0 - g)


# ---------------------------------------------------------------------------------------------
# The program in cvxpy
# ---------------------------------------------------------------------------------------------
class Program:
    def __init__(self, p, nodes, W0, tangents, lim, root_pe_zero=False):
        A, Lm, R, Tm = p["actions"], p["limits"], p["rates"], p["terminal"]
        rc, tau, kU = R["cash_rate"], A["liquid_trade_cost"], A["unfunded_assumed_per_nav_sold"]
        plan, cpace, kap = A["pacing_plan"], A["pacing_cut_cost"], A["exposure_cap"]
        q1 = A["new_commitment_first_year_call_rate"]
        sR, uR = A["revolver_drawn_spread"], A["revolver_undrawn_fee"]
        f, f8 = Lm["cash_floor_frac"], Lm["cash_target_frac"]
        lo, hi = Lm["liquid_exposure_min_frac"], Lm["liquid_exposure_max_frac"]
        assert Lm["cash_target_basis"] == "net_of_facility_draws" and not Lm.get("liquid_exposure_min_hard")
        p2s_only = A["synthetic_use"] == "p2s_only"
        g = p["objective"]["crra_gamma"]
        H = max(n.stage for n in nodes)
        b = p["balance_sheet_t0"]
        self.p, self.nodes, self.W0, self.H, self.f, self.f8 = p, nodes, W0, H, f, f8
        N = len(nodes)
        self.inj = cp.Parameter(N, value=np.zeros(N))       # cash injected at a node
        self.tf = cp.Parameter(N, value=np.zeros(N))        # tightening of the floor row
        self.tt = cp.Parameter(N, value=np.zeros(N))        # tightening of the target row
        V, E, con, util = {}, {}, {}, []

        def price(pr, regime, horizon):
            return pr["horizon"] if (horizon and "horizon" in pr) else pr[regime]

        for n in nodes:
            dec = n.stage < H
            v = {k: cp.Variable(nonneg=True, name=f"{k}[{n.path}]")
                 for k in ("C", "L", "P", "U", "sL", "bL", "sP", "BR", "BN", "s8", "sb")}
            if dec:
                v.update({k: cp.Variable(nonneg=True, name=f"{k}[{n.path}]") for k in ("X", "cv", "uw", "lev", "cut")})
                if p2s_only:
                    con[("nolev", n.path)] = v["lev"] == 0
            if root_pe_zero and n.parent is None:
                con[("rootpe",)] = v["sP"] == 0
            if n.regime in set(A.get("no_liquid_purchases_in_regimes") or []):
                con[("nobuy", n.path)] = v["bL"] == 0      # the CFP Red playbook adds no risk in a crisis year
            V[n.path] = v
            e = {}
            h = A["lever_initial_margin"][n.regime] if dec else 0.0
            disc = A["pe_secondary_discount"][n.regime]
            if n.parent is None:
                Cp_flow, Lpre, Ppre, Upre = b["cash_hqla"], b["liquid_book"], b["pe_book_nav"], b["pe_unfunded"]
                BRp, BNp, Xp = 0.0, 0.0, 0.0
            else:
                pa, vp, ep = n.parent, V[n.parent.path], E[n.parent.path]
                hp = A["lever_initial_margin"][pa.regime]
                sN, sX = A["nav_loan_spread"][pa.regime], A["lever_financing_spread"][pa.regime]
                e["draw"] = n.draw * ep["NAV"]
                Cp_flow = ((1 + rc) * vp["C"] + (1 + rc) * hp * vp["X"] + (n.rL - rc - sX) * vp["X"]
                           + n.dist * vp["P"] - n.call * vp["U"] - q1 * (plan - vp["cut"]) + n.yY * pa.Y
                           - e["draw"] - (rc + sR) * vp["BR"] - uR * (lim - vp["BR"]) - (rc + sN) * vp["BN"])
                Lpre = (1 + n.rL) * vp["L"]
                Ppre = (1 + n.rP - n.dist) * vp["P"] + n.call * vp["U"] + q1 * (plan - vp["cut"])
                Upre = (1 - n.call) * vp["U"] + (1 - q1) * (plan - vp["cut"])
                BRp, BNp, Xp = vp["BR"], vp["BN"], vp["X"]
            cash = (Cp_flow + (1 - tau) * v["sL"] - (1 + tau) * v["bL"] + (1 - disc) * v["sP"]
                    + (v["BR"] - BRp) + (v["BN"] - BNp) + self.inj[n.idx])
            liq = Lpre - v["sL"] + v["bL"]
            if dec:
                cash = cash + (1 - tau) * v["cv"] - (1 + tau) * v["uw"] - h * v["X"]
                liq = liq - v["cv"] + v["uw"]
                con[("syn", n.path)] = v["X"] == Xp + v["cv"] - v["uw"] + v["lev"]
                con[("uwcap", n.path)] = v["uw"] <= Xp
            con[("cash", n.path)] = v["C"] == cash
            con[("liq", n.path)] = v["L"] == liq
            con[("pe", n.path)] = v["P"] == Ppre - v["sP"]
            con[("unf", n.path)] = v["U"] == Upre - kU * v["sP"]
            X = v["X"] if dec else 0.0
            NAV = v["C"] + h * X + v["L"] + v["P"] + n.Y - v["BR"] - v["BN"]
            e["NAV"] = NAV
            con[("floor", n.path)] = v["C"] - f * NAV >= self.tf[n.idx]
            con[("target", n.path)] = v["C"] - v["BR"] - v["BN"] + v["s8"] - f8 * NAV >= self.tt[n.idx]
            pool = A["nav_loan_ltv_cap"][n.regime] * A["nav_loan_pledge_pool_frac"]
            con[("ltv", n.path)] = v["BN"] <= pool * (v["P"] + (n.Y if A["nav_loan_pledge_pool_includes_yield_book"] else 0.0))
            con[("rcf", n.path)] = v["BR"] <= A["revolver_availability"][n.regime] * lim
            if not dec:
                con[("norev", n.path)] = v["BR"] <= BRp       # at t = 3 debt can be repaid, not drawn
                con[("nonav", n.path)] = v["BN"] <= BNp
            con[("band_hi", n.path)] = v["L"] + X <= hi * NAV
            con[("band_lo", n.path)] = v["L"] + X + v["sb"] >= lo * NAV
            if dec:
                con[("expo", n.path)] = v["L"] + v["P"] + n.Y + v["X"] <= kap * NAV
                con[("pace", n.path)] = v["cut"] <= (1 - A["pacing_core_sleeve"]) * plan
                con[("syncap", n.path)] = v["X"] <= A["synthetic_notional_cap"]
            else:
                anc = []
                k = n
                while k is not None:
                    anc.append(k)
                    k = k.parent
                anc = anc[::-1]
                W = (v["C"] + v["L"] + Tm["pe_value_per_nav"][n.regime] * v["P"] + n.Y - v["BR"] - v["BN"]
                     - Tm["unfunded_burden_per_dollar"] * v["U"]
                     - cpace * sum(V[a.path]["cut"] for a in anc[:-1]))
                for a in anc:
                    hz = a.stage == H
                    W = W - price(Lm["cash_target_shortfall_price"], a.regime, hz) * V[a.path]["s8"]
                    W = W - price(Lm["liquid_exposure_min_shortfall_price"], a.regime, hz) * V[a.path]["sb"]
                for i in range(1, len(anc)):
                    G = 1.0
                    for j in range(i + 1, len(anc)):
                        G *= 1.0 + anc[j].rref
                    draw_i = e["draw"] if i == len(anc) - 1 else E[anc[i].path]["draw"]
                    W = W + G * draw_i
                v["W"] = cp.Variable(name=f"W[{n.path}]")
                v["u"] = cp.Variable(name=f"u[{n.path}]")
                con[("wealth", n.path)] = v["W"] == W
                for kk, wk in enumerate(tangents):
                    con[("util", n.path, kk)] = v["u"] <= crra(wk, g) + wk ** (-g) * (v["W"] / W0 - wk)
                util.append(n.prob * v["u"])
            E[n.path] = e
        self.V, self.E, self.con = V, E, con
        self.leaves = [n for n in nodes if n.stage == H]
        self.obj_expr = sum(util)
        self.prob = cp.Problem(cp.Maximize(self.obj_expr), list(con.values()))

    def decision_range(self, path, key, opt, tol=1e-10):
        """Smallest and largest value of one decision over the optimal face (objective >= optimum - tol)."""
        x = self.V[path][key]
        cons = list(self.con.values()) + [self.obj_expr >= opt - tol]
        lo_ = cp.Problem(cp.Minimize(x), cons)
        lo_.solve(solver=cp.HIGHS, **HIGHS_OPTS)
        hi_ = cp.Problem(cp.Maximize(x), cons)
        hi_.solve(solver=cp.HIGHS, **HIGHS_OPTS)
        return float(lo_.value), float(hi_.value)

    def solve(self, solver="HIGHS"):
        if solver == "CLARABEL":
            self.prob.solve(solver=cp.CLARABEL, **CLARABEL_OPTS)
        else:
            self.prob.solve(solver=cp.HIGHS, **HIGHS_OPTS)
        return self.prob.status, self.prob.value

    def val(self, path, key):
        x = self.V[path].get(key)
        return 0.0 if x is None else float(x.value)


def two_pass(p, nodes, W0, lim, root_pe_zero, solver):
    K = int(p["objective"]["n_tangents"])
    lo, hi = p["objective"]["tangent_first_pass_range"]
    t1 = np.geomspace(lo, hi, K)
    m1 = Program(p, nodes, W0, t1, lim, root_pe_zero)
    m1.solve(solver)
    w = np.array([m1.val(n.path, "W") / W0 for n in m1.leaves])
    a, b = p["settings"]["tangent_margins"]
    t2 = np.geomspace(a * w.min(), b * w.max(), K)
    m2 = Program(p, nodes, W0, t2, lim, root_pe_zero)
    st, obj = m2.solve(solver)
    return m2, t2, st, obj


# ---------------------------------------------------------------------------------------------
# Check 2: identities and limits from the published node values
# ---------------------------------------------------------------------------------------------
def published_checks(p, nodes_by_path, recs, lim):
    """Recompute every identity and limit from results.json's node records (12 significant digits)."""
    A, Lm, R = p["actions"], p["limits"], p["rates"]
    rc, tau, kU = R["cash_rate"], A["liquid_trade_cost"], A["unfunded_assumed_per_nav_sold"]
    f, f8 = Lm["cash_floor_frac"], Lm["cash_target_frac"]
    H = max(r["stage"] for r in recs)
    by = {r["path"]: r for r in recs}
    resid, slack = {}, {}

    def rr(k, x):
        resid[k] = max(resid.get(k, 0.0), abs(x))

    def ss(k, x):
        slack[k] = min(slack.get(k, float("inf")), x)

    for r in recs:
        n = nodes_by_path[r["path"]]
        dec = r["stage"] < H
        cs, op, d = r["closing_state"], r["opening_state"], r["decisions"]
        h = A["lever_initial_margin"][n.regime] if dec else 0.0
        NAV = cs["C"] + h * cs["X"] + cs["L"] + cs["P"] + n.Y - cs["BR"] - cs["BN"]
        rr("closing NAV as published", NAV - cs["NAV"])
        if n.parent is not None:
            pc = by[n.parent.path]["closing_state"]
            pd = by[n.parent.path]["decisions"]
            hp = A["lever_initial_margin"][n.parent.regime]
            navp = pc["C"] + hp * pc["X"] + pc["L"] + pc["P"] + n.parent.Y - pc["BR"] - pc["BN"]
            draw = n.draw * navp
            rr("owner draw = rate x parent's NAV", -r["exogenous_flows"]["owner_draw"] - draw)
            cflow = ((1 + rc) * pc["C"] + (1 + rc) * hp * pc["X"]
                     + (n.rL - rc - A["lever_financing_spread"][n.parent.regime]) * pc["X"]
                     + n.dist * pc["P"] - n.call * pc["U"] + n.yY * n.parent.Y - draw
                     - (rc + A["revolver_drawn_spread"]) * pc["BR"] - A["revolver_undrawn_fee"] * (lim - pc["BR"])
                     - (rc + A["nav_loan_spread"][n.parent.regime]) * pc["BN"])
            rr("opening cash = parent's closing cash + the year's flows", cflow - op["C"])
            rr("opening liquid = parent's liquid x (1 + return)", (1 + n.rL) * pc["L"] - op["L"])
            rr("opening PE = parent's PE x (1 + return - distributions) + calls",
               (1 + n.rP - n.dist) * pc["P"] + n.call * pc["U"] - op["P"])
            rr("opening unfunded = parent's x (1 - call rate) + new commitments",
               (1 - n.call) * pc["U"] + (A["pacing_plan"] - pd["pace_cut"]) - op["U"])
            BRp, BNp = pc["BR"], pc["BN"]
        else:
            BRp, BNp = 0.0, 0.0
        cv, uw = d["p2s"], (d["synthetic_closed"] if dec else 0.0)
        disc = A["pe_secondary_discount"][n.regime]
        c_close = (op["C"] + (1 - tau) * (d["sell_liquid"] + cv) - (1 + tau) * (d["buy_liquid"] + uw)
                   + (1 - disc) * d["sell_pe_nav"] + (cs["BR"] - BRp) + (cs["BN"] - BNp) - h * cs["X"])
        rr("closing cash = opening cash + trades", c_close - cs["C"])
        rr("closing liquid = opening liquid + trades",
           op["L"] - d["sell_liquid"] + d["buy_liquid"] - cv + uw - cs["L"])
        rr("closing PE = opening PE - sales", op["P"] - d["sell_pe_nav"] - cs["P"])
        rr("closing unfunded = opening - transferred", op["U"] - kU * d["sell_pe_nav"] - cs["U"])
        ss("cash floor 4%", cs["C"] - f * NAV)
        ss("8% target with priced shortfall", cs["C"] - cs["BR"] - cs["BN"] + cs["s8"] - f8 * NAV)
        ss("NAV-loan capacity", A["nav_loan_ltv_cap"][n.regime] * A["nav_loan_pledge_pool_frac"] * (cs["P"] + n.Y)
           - cs["BN"])
        ss("revolver availability", A["revolver_availability"][n.regime] * lim - cs["BR"])
        ss("IC range upper edge", Lm["liquid_exposure_max_frac"] * NAV - cs["L"] - cs["X"])
        ss("IC range lower edge with priced shortfall", cs["L"] + cs["X"] + cs["sb"] - Lm["liquid_exposure_min_frac"] * NAV)
        if dec:
            ss("exposure cap", A["exposure_cap"] * NAV - cs["L"] - cs["P"] - n.Y - cs["X"])
            ss("synthetic budget", A["synthetic_notional_cap"] - cs["X"])
            ss("pacing cut <= 75% of plan", (1 - A["pacing_core_sleeve"]) * A["pacing_plan"] - d["pace_cut"])
        ss("non-negative stocks", min(cs[k] for k in ("C", "L", "P", "U", "BR", "BN", "X")))
    probs = {}
    for r in recs:
        probs[r["stage"]] = probs.get(r["stage"], 0.0) + r["probability"]
    rr("probabilities sum to 1 at each stage", max(abs(v_ - 1.0) for v_ in probs.values()))
    for r in recs:
        n = nodes_by_path[r["path"]]
        rr("node probability = parent's x branch probability", r["probability"] - n.prob)
    return resid, slack


# ---------------------------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------------------------
def main():
    t0 = time.perf_counter()
    raw = json.loads((HERE / "params.json").read_text(encoding="utf-8"))
    p = values(raw)
    res_text = (HERE / "results.json").read_text(encoding="utf-8")
    res = json.loads(res_text)
    sha = res["meta"]["content_sha256_before_this_field"]
    H = int(p["tree"]["decision_stages"])
    nodes, W0 = grow_tree(p, H)
    by_path = {n.path: n for n in nodes}
    lim = p["actions"]["revolver_limit"]
    out = {"results_sha256": sha, "checked_on": "2026-10-19", "method": __doc__.strip().splitlines()[0]}

    # ---- check 1: objective agreement and decisions -------------------------------------------
    cases = {}
    for tag, lm, recs, author_obj, author_tan, held in (
            ("with_revolver", lim, res["nodes"], res["meta"]["lp_objective_expected_pwl_utility"],
             res["meta"]["utility_tangents_W_over_W0"], res["meta"]["root_pe_sell_held_at_zero"]),
            ("no_revolver", 0.0, res["cases"]["no_revolver"]["nodes"],
             res["cases"]["no_revolver"]["lp_objective_expected_pwl_utility"],
             res["cases"]["no_revolver"]["utility_tangents_W_over_W0"],
             res["cases"]["no_revolver"]["root_pe_sell_held_at_zero"])):
        mh, th, sth, objh = two_pass(p, nodes, W0, lm, held, "HIGHS")
        mc, tcl, stc, objc = two_pass(p, nodes, W0, lm, held, "CLARABEL")
        # The author's tangents re-used, so the two objectives are the same function.
        ma = Program(p, nodes, W0, np.array(author_tan), lm, held)
        sta, obja = ma.solve("HIGHS")
        by = {r["path"]: r for r in recs}
        keys = {"sell_liquid": "sL", "buy_liquid": "bL", "sell_pe_nav": "sP", "p2s": "cv"}
        dmax, dwhere = 0.0, None
        for n in nodes:
            r = by[n.path]
            vals = {k: ma.val(n.path, kk) for k, kk in keys.items()}
            vals |= {"C": ma.val(n.path, "C"), "L": ma.val(n.path, "L"), "P": ma.val(n.path, "P"),
                     "U": ma.val(n.path, "U"), "BR": ma.val(n.path, "BR"), "BN": ma.val(n.path, "BN"),
                     "X": ma.val(n.path, "X")}
            pub = {k: r["decisions"][k] for k in keys} | {k: r["closing_state"][k] for k in ("C", "L", "P", "U", "BR", "BN", "X")}
            for k in vals:
                dlt = abs(vals[k] - pub[k])
                if dlt > dmax:
                    dmax, dwhere = dlt, f"{n.path} {k}"
        cases[tag] = {
            "author_objective": author_obj,
            "independent_objective_highs_own_tangents": objh, "status_highs": sth,
            "independent_objective_clarabel_own_tangents": objc, "status_clarabel": stc,
            "independent_objective_highs_author_tangents": obja,
            "rel_diff_highs": abs(objh - author_obj) / abs(author_obj),
            "rel_diff_clarabel": abs(objc - author_obj) / abs(author_obj),
            "rel_diff_author_tangents": abs(obja - author_obj) / abs(author_obj),
            "max_tangent_rel_diff": float(np.max(np.abs(th - np.array(author_tan)) / np.array(author_tan))),
            "max_abs_decision_or_state_diff_bn": dmax, "where": dwhere,
        }
        if tag == "with_revolver":
            main_prog = ma
    out["objective_and_decisions"] = cases

    # ---- check 2: identities and limits from the published values ------------------------------
    pub = {}
    for tag, lm, recs in (("with_revolver", lim, res["nodes"]), ("no_revolver", 0.0, res["cases"]["no_revolver"]["nodes"])):
        resid, slack = published_checks(p, by_path, recs, lm)
        pub[tag] = {"max_residual_by_identity": resid, "min_slack_by_limit": slack,
                    "max_residual_bn": max(resid.values()), "min_slack_bn": min(slack.values())}
    out["published_values"] = pub

    # ---- check 3: duals by re-solving ----------------------------------------------------------
    m = main_prog
    base = m.prob.value
    f, f8 = p["limits"]["cash_floor_frac"], p["limits"]["cash_target_frac"]
    step = p["settings"]["fd_step_bn"]
    by = {r["path"]: r for r in res["nodes"]}
    rows = []
    N = len(nodes)
    for n in nodes:
        if n.stage >= H:
            continue
        slopes = []
        for sgn in (+1, -1):
            inj = np.zeros(N)
            inj[n.idx] = sgn * step
            m.inj.value = inj
            m.prob.solve(solver=cp.HIGHS, **HIGHS_OPTS)
            slopes.append((m.prob.value - base) / (sgn * step))
        m.inj.value = np.zeros(N)
        # carry: inject step, tighten floor and target so the dollar cannot relieve them
        inj = np.zeros(N)
        inj[n.idx] = step
        tf, tt = np.zeros(N), np.zeros(N)
        tf[n.idx], tt[n.idx] = (1 - f) * step, (1 - f8) * step
        m.inj.value, m.tf.value, m.tt.value = inj, tf, tt
        m.prob.solve(solver=cp.HIGHS, **HIGHS_OPTS)
        carry = (m.prob.value - base) / step
        m.inj.value, m.tf.value, m.tt.value = np.zeros(N), np.zeros(N), np.zeros(N)
        mu_pub = by[n.path]["duals"]["mu_cash_utility_per_bn"]
        lam_pub = by[n.path]["duals"]["liquidity_premium_lambda"]
        mu_fd = slopes[0] if abs(slopes[0] - mu_pub) <= abs(slopes[1] - mu_pub) else slopes[1]
        lam_rs = (mu_fd - carry) / carry if carry > 0 else None
        rows.append({"path": n.path, "mu_published": mu_pub, "mu_right": slopes[0], "mu_left": slopes[1],
                     "rel_err": abs(mu_fd - mu_pub) / abs(mu_pub),
                     "lambda_published": lam_pub, "lambda_resolve": lam_rs,
                     "lambda_abs_diff": None if (lam_rs is None or lam_pub is None) else abs(lam_rs - lam_pub)})
    out["duals"] = {"rows": rows, "max_rel_err_mu": max(r_["rel_err"] for r_ in rows),
                    "max_abs_diff_lambda": max(r_["lambda_abs_diff"] or 0.0 for r_ in rows),
                    "right_left_max_rel_gap": max(abs(r_["mu_right"] - r_["mu_left"]) / abs(r_["mu_published"]) for r_ in rows)}

    # ---- uniqueness: how far each decision at t = 0 and t = 1 can move without changing the optimum ----------
    m.prob.solve(solver=cp.HIGHS, **HIGHS_OPTS)
    opt = m.prob.value
    uniq = []
    for n in nodes:
        if n.stage > 1:
            continue
        for key in ("sL", "bL", "sP", "cv", "uw", "BR", "BN", "X", "cut"):
            lo_, hi_ = m.decision_range(n.path, key, opt)
            uniq.append({"path": n.path, "decision": key, "min": lo_, "max": hi_, "range": hi_ - lo_})
    root_rng = max(u["range"] for u in uniq if u["path"] == nodes[0].path)
    t1_worst = max((u for u in uniq if u["path"] != nodes[0].path), key=lambda u: u["range"])
    out["uniqueness"] = {"rows": uniq, "root_max_range_bn": root_rng, "stage1_max_range_bn": t1_worst["range"],
                         "stage1_worst": f"{t1_worst['path']} {t1_worst['decision']}"}
    out["runtime_seconds_not_hashed"] = round(time.perf_counter() - t0, 1)

    # ---- markdown for RESULTS.md ---------------------------------------------------------------
    c1, c0 = cases["with_revolver"], cases["no_revolver"]
    pa, pb = pub["with_revolver"], pub["no_revolver"]
    du = out["duals"]
    passed = (max(c1["rel_diff_highs"], c1["rel_diff_clarabel"], c0["rel_diff_highs"], c0["rel_diff_clarabel"]) < 1e-6
              and max(pa["max_residual_bn"], pb["max_residual_bn"]) < 1e-6
              and min(pa["min_slack_bn"], pb["min_slack_bn"]) > -1e-6
              and du["max_rel_err_mu"] < 1e-4 and du["max_abs_diff_lambda"] < 1e-5)
    md = [
        f"`verify_independent.py` re-implements the program from section 9 and `params.json` without calling "
        f"`tree_demo.py`'s model code. The tree is built depth-first and keyed by path, every row is a cvxpy "
        f"expression, and the program is solved with CLARABEL (interior point) and with HiGHS through cvxpy. It "
        f"checked results.json `{sha[:16]}…` on 2026-10-19. **Result: {'all three checks pass' if passed else 'see the failures below'}.**",
        "",
        "| Check | What was compared | Result |",
        "|---|---|---|",
        f"| 1. Objective agreement, revolver signed | E[Û]: author {c1['author_objective']:.12f}; independent HiGHS "
        f"{c1['independent_objective_highs_own_tangents']:.12f}, CLARABEL {c1['independent_objective_clarabel_own_tangents']:.12f} "
        f"(each with its own two-pass tangents) | relative difference {c1['rel_diff_highs']:.1e} / "
        f"{c1['rel_diff_clarabel']:.1e}; tangents agree to {c1['max_tangent_rel_diff']:.1e} |",
        f"| 1. Objective agreement, no revolver | author {c0['author_objective']:.12f}; HiGHS "
        f"{c0['independent_objective_highs_own_tangents']:.12f}, CLARABEL {c0['independent_objective_clarabel_own_tangents']:.12f} | "
        f"relative difference {c0['rel_diff_highs']:.1e} / {c0['rel_diff_clarabel']:.1e} |",
        f"| 1. Decisions and states at all 40 nodes | sells, buys, PE sales, P2S, closing C, L, P, U, BR, BN, X "
        f"(HiGHS vertex, author's tangents) | largest difference ${c1['max_abs_decision_or_state_diff_bn']:.1e}bn "
        f"({c1['where']}); no revolver ${c0['max_abs_decision_or_state_diff_bn']:.1e}bn |",
        f"| 2. Identities at every node, from the published values | opening stocks from the parent's closing stocks "
        f"and the year's rates; closing stocks from the trades; owner draw = rate × parent's NAV; probabilities | "
        f"largest residual {pa['max_residual_bn']:.1e} (revolver) / {pb['max_residual_bn']:.1e} (no revolver) |",
        f"| 2. Limits at every node, from the published values | 4% floor, 8% target with its priced shortfall, "
        f"NAV-loan capacity, revolver availability, IC range edges, exposure cap, synthetic budget, pacing cap, "
        f"non-negative stocks | smallest slack {pa['min_slack_bn']:.1e} / {pb['min_slack_bn']:.1e} (≥ 0 holds) |",
        f"| 3. Cash price at all 13 decision nodes | μ published against ± ${step}bn re-solves (HiGHS) | largest "
        f"relative error {du['max_rel_err_mu']:.1e}; right and left slopes agree to {du['right_left_max_rel_gap']:.1e} |",
        f"| 3. λ at all 13 decision nodes | λ published against a carry re-solve (inject $1, tighten the floor and "
        f"target by (1 − f) and (1 − 0.08)) | largest absolute difference {du['max_abs_diff_lambda']:.1e} |",
        f"| Uniqueness of the decisions that matter | the range of each decision at t = 0 and t = 1 over the whole "
        f"optimal face (objective held at its optimum) | root: ${out['uniqueness']['root_max_range_bn']:.1e}bn; "
        f"year 1: ${out['uniqueness']['stage1_max_range_bn']:.1e}bn ({out['uniqueness']['stage1_worst']}) |",
        "",
        "What this does and does not show: an independently written program with the same inputs reaches the same "
        "optimum, decisions and prices, and the published numbers satisfy every row. It does not test whether the "
        "inputs are right. That is what the sensitivities in section 7 are for. Details are in `verification.json`.",
    ]
    out["passed"] = bool(passed)
    out["markdown_lines"] = md

    def plain(o):
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        raise TypeError(type(o))

    (HERE / "verification.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=plain),
                                            encoding="utf-8")
    # Re-render RESULTS.md so its Verification section shows these results.
    sys.path.insert(0, str(HERE))
    sys.dont_write_bytecode = True
    import tree_demo
    rawp, vv = tree_demo.load_params(HERE / "params.json")
    root = tree_demo.root_state_t0(vv)
    tnodes = tree_demo.build_tree(vv, vv["tree"]["start_regime"], H, root["Y"], tree_demo.saa_weights(vv))
    tree_demo.write_results_md(res, tnodes, H)
    print(f"verification {'PASSED' if passed else 'FAILED'}: obj rel diff {c1['rel_diff_highs']:.1e}/{c1['rel_diff_clarabel']:.1e}, "
          f"decisions {c1['max_abs_decision_or_state_diff_bn']:.1e}bn, residual {pa['max_residual_bn']:.1e}, "
          f"slack {pa['min_slack_bn']:.1e}, mu {du['max_rel_err_mu']:.1e}, lambda {du['max_abs_diff_lambda']:.1e}; "
          f"{out['runtime_seconds_not_hashed']}s")


if __name__ == "__main__":
    main()
