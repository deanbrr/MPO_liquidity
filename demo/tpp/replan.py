"""Re-planning each year (model predictive control): the closed-loop rung of the benchmark ladder.

The fixed-schedule plan is solved once today and today's decisions are carried out. At the start of each later year
the engine observes the history so far (the market class at each year end: benign / exit drought / stress), takes
the in-sample scenarios that share that history, fixes every decision already made, and re-solves the same objective
under the same house limits for the rest of the five years with one schedule for the remaining years (open-loop
feedback). Only the coming year's decisions are kept; the next year re-plans again (external research shared
2026-10-27: a closed-loop benchmark). A limit is never relaxed to make a re-plan feasible.

What re-planning can change: the secondary sales and term-debt draws still to come (years 2 and 3), and the
commitments of years 2-5. Today's liquid allocation, NAV facility and synthetic beta stay as decided, as in every
other plan. The balance-sheet guard covers the year ends still ahead, at the buffered probability the fixed plan was
validated at; the forced-sale appetite stays. The depth guard (the tail no worse than the status quo's) is not
re-imposed: conditional on a bad history no plan may meet it, and it never binds the shortfall objective (the
feasibility tab's cost of limits).

The information state is the history of market classes, not each path's exact position: the re-plan for a history
sees the spread of positions its in-sample scenarios reached. A history seen in fewer than min_scenarios in-sample
scenarios keeps the plan in force (no re-plan on too little evidence), as does one whose re-plan is infeasible. The
result is a table of decisions by history (3, 9, 27 and 81 histories at the starts of years 2-5) that
tpp.plan.schedule_paths applies to any path set, so the simulator certifies it like any other plan.
"""
from __future__ import annotations

import copy
import time

import numpy as np

from . import lp
from .plan import STATES, Plan, history_code

NS = len(STATES)


def _decisions(p: Plan, tau: int, unit_ids: list, buckets: list) -> dict:
    """The decisions a one-schedule plan takes at the start of year tau + 1."""
    out = {"commit": {b: float(list(p.commit.get(b, [0.0] * 5))[tau]) for b in buckets}}
    if tau <= 2:
        out["sell"] = {u: float((list(p.sell.get(u, [0.0, 0.0, 0.0])) + [0.0] * 3)[tau]) for u in unit_ids}
        out["term"] = float(list(p.term_sched or [p.term_bn, 0.0, 0.0])[tau])
    return out


def replan_policy(S, P, settings: dict, objective: str, base: Plan, bs_alpha: float | None = None,
                  forced_eps: float | None = None, min_scenarios: int = 60, name: str = "Re-planned each year",
                  log=None) -> tuple[Plan, dict]:
    """Re-plan at the start of years 2-5 on the in-sample scenarios S, from the fixed-schedule plan base (its
    today's decisions are kept). Returns the plan (a table by history) and a record of every re-plan."""
    log = log or (lambda s: None)
    st = {**settings, "contingent": False}
    units = [u.id for u in S.book.units]
    buckets = list(S.tpl_buckets)
    p = S.prob / S.prob.sum()
    cont = {0: {0: base}}                                     # the one-schedule plan in force after each history
    pol = {t: {} for t in range(1, 5)}
    rec = []
    t_all = time.time()
    for t in range(1, 5):
        code = history_code(S.cls_y, t)
        cont[t] = {}
        for h in range(NS ** t):
            parent = cont[t - 1][h // NS]
            idx = np.flatnonzero(code == h)
            r = {"year": t + 1, "history": [STATES[(h // NS ** (t - 1 - s)) % NS] for s in range(t)],
                 "n": int(len(idx)), "p": float(p[idx].sum()), "status": "kept (too few scenarios)"}
            new = None
            if len(idx) >= min_scenarios:
                t0 = time.time()
                M = lp.TPPModel(S.subset(idx), P, {**st, "bs_from_year": t + 1})
                M.fix_through(parent, t)
                if forced_eps:
                    M.apply_eps(forced_eps=forced_eps)
                if bs_alpha:
                    M.apply_bs_guard(bs_alpha)
                res = lp.solve(M, objective)                  # never relaxed: an infeasible re-plan keeps the plan
                r["time_s"] = time.time() - t0
                if res.get("x") is not None:
                    new = M.extract(res["x"], name)
                    new.meta = {"kind": "replan", "year": t + 1}
                    r["status"] = "re-planned"
                    r["bs_alpha"] = M.bs_alpha
                    if M.sf_on:
                        ins = M.in_sample(res["x"])
                        r["short_mean_bn"], r["short_cvar_bn"] = ins["short_mean_bn"], ins["short_cvar_bn"]
                else:
                    r["status"] = "kept (re-plan infeasible)"
            cont[t][h] = new if new is not None else parent
            pol[t][h] = _decisions(cont[t][h], t, units, buckets)
            rec.append(r)
        log(f"   re-plans at the start of year {t + 1}: "
            f"{sum(1 for x in rec if x['year'] == t + 1 and x['status'] == 're-planned')} of {NS ** t} histories")
    plan = assemble(base, pol, S, units, buckets, name)
    info = {"replans": rec, "min_scenarios": int(min_scenarios), "time_s": time.time() - t_all,
            "n_replanned": sum(1 for x in rec if x["status"] == "re-planned"),
            "p_replanned": {t + 1: float(sum(x["p"] for x in rec if x["year"] == t + 1 and x["status"] == "re-planned"))
                            for t in range(1, 5)},
            "n_infeasible": sum(1 for x in rec if x["status"].startswith("kept (re-plan"))}
    return plan, info


def assemble(base: Plan, pol: dict, S, units: list, buckets: list, name: str) -> Plan:
    """The re-planned plan: today's decisions from base; the later ones as tables by history (plan.contingent, 3^tau
    values at tau); sell / commit / term_sched hold today's decisions and the in-sample probability-weighted averages
    of the later ones (for summaries and change lists)."""
    p = S.prob / S.prob.sum()
    freq = {t: np.bincount(history_code(S.cls_y, t), weights=p, minlength=NS ** t) for t in range(1, 5)}
    avg = lambda t, f: float(np.dot(freq[t], [f(pol[t][h]) for h in range(NS ** t)]))
    c_sell, sell = {}, {}
    for u in units:
        tabs = [[pol[t][h]["sell"][u] for h in range(NS ** t)] for t in (1, 2)]
        s0 = float((list(base.sell.get(u, [0.0, 0.0, 0.0])) + [0.0] * 3)[0])
        if s0 + sum(map(sum, tabs)) > 1e-7:
            sell[u] = [s0] + [avg(t, lambda d, u=u: d["sell"][u]) for t in (1, 2)]
            c_sell[u] = tabs
    c_commit, commit = {}, {}
    for b in buckets:
        c_commit[b] = [[pol[t][h]["commit"][b] for h in range(NS ** t)] for t in range(1, 5)]
        commit[b] = [float(list(base.commit.get(b, [0.0] * 5))[0])] + [avg(t, lambda d, b=b: d["commit"][b])
                                                                         for t in range(1, 5)]
    c_term = [[pol[t][h]["term"] for h in range(NS ** t)] for t in (1, 2)]
    sched = [float(list(base.term_sched or [base.term_bn, 0.0, 0.0])[0])] + [avg(t, lambda d: d["term"]) for t in (1, 2)]
    contingent = {"sell": c_sell, "commit": c_commit, "term": c_term, "states": STATES, "history": True,
                  "freq": {str(t + 0): freq[t].tolist() for t in range(1, 5)}}
    return Plan(name=name, sell=sell, liquid=dict(base.liquid), cash=base.cash, treasury=base.treasury, commit=commit,
                term_bn=float(sum(sched)), term_sched=sched, navf_bn=base.navf_bn, rev_upsize_bn=base.rev_upsize_bn,
                beta_bn=base.beta_bn, meta={**copy.deepcopy(base.meta), "kind": "replan"}, contingent=contingent)
