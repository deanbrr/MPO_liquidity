"""Parallel tasks (SYNTHETIC - NOT ADIC DATA).

Each worker process builds the headline world once (deterministic), then runs independent tasks. Every LP task
starts from a fresh HiGHS instance with the base bounds and Phase I allowances, so results do not depend on which
worker ran which task before (determinism, DSGO A16). Tasks:
  gbo        GBO with modifications (family switch-off, red-event limit, depth delta, forced columns, relaxed rows)
             and optionally the MILP at the same point (frontier)
  milp       the exact max-P(goal) comparison from a given start
  crra       CRRA(3) + quadratic shortfall
  beliefs    GBO with the fused beliefs replaced by group priors (F10)
  book       a replication / placebo book: rebuild, re-fuse, re-solve, simulate on its own sealed truth
  sim        one chunk of out-of-sample paths for a set of policies
"""
from __future__ import annotations

import time

import numpy as np

import optim
import world
from common import HERE, Params
from model import FIN, INF
from policy import extract_policy
from sim import Sim

WORLD = None
P = None


def init_worker(params_path: str):
    global WORLD, P
    P = Params(params_path)
    WORLD = world.build(P, log=None)


def _apply(m, mods):
    ctxs = []
    for md in mods:
        kind = md[0]
        if kind == "switchoff":
            c = optim.SwitchOff(m, md[1])
            c.__enter__()
            ctxs.append(c)
        elif kind == "eps":
            optim.set_eps_red(m, md[1])
        elif kind == "delta":
            optim.set_delta(m, md[1])
        elif kind == "fix":
            idx = np.atleast_1d(np.asarray(md[1], int))
            m.set_col_bounds(idx, md[2], md[3])
        elif kind == "relax":
            what = md[1]
            h = m.highs()
            if what == "floor8":
                for n, r in m.rows.get("floor8", {}).items():
                    m.set_row_bounds(r, -INF, INF)
            elif what == "class_caps":
                for n, r in m.rows["lev"].items():
                    h.changeCoeff(int(r), int(m.W[n]), float(-P.get("constraints.lev_cap")))
            elif what == "H11":
                for n, r in m.rows.get("H11", {}).items():
                    m.set_row_bounds(r, -INF, INF)
    return ctxs


def _summary(m, x):
    D = m.D
    return {"sell": x[m.S[0]].copy(), "redeem": x[m.R[0]].copy(), "add": x[m.A[0]].copy(), "tpl": x[m.Y[0]].copy(),
            "fin": x[m.FB[0]].copy(), "beta": float(x[m.BETA[0]]), "p2s": float(x[m.PI[0]]),
            "trs": x[m.TRS[0]].copy(), "hed": float(x[m.HED[0]]), "opp": float(x[m.OPP[0]]),
            "Lup": float(x[m.LUP[0]]), "C0": float(x[m.C[0]]), "W0post": float(x[m.W[0]]),
            "E_W0": float(x[m.EX[0]] / x[m.W[0]]), "LQ_W0": float(x[m.LQ[0]] / x[m.W[0]])}


def run_gbo(w, task, log=None):
    m = world.reset_model(w)
    mods = task.get("mods", [])
    _apply(m, mods)
    m.solves = []
    t0 = time.time()
    cert = bool(task.get("certify", False))
    res = optim.gbo(m, log or (lambda s: None), tag=task["id"], certify=cert)
    ph = None
    if res.get("x") is None:
        # the variant violates a hard row the base book meets: Phase I for this variant (STRUCTURAL_RECOVERY),
        # prices and decisions only from the restored problem (DSGO section 4.3 step 1)
        ph = optim.phase1(m, log or (lambda s: None))
        res = optim.gbo(m, log or (lambda s: None), tag=task["id"] + " (after Phase I)", certify=cert)
    out = {"id": task["id"], "status": res.get("status"), "time_s": time.time() - t0,
           "phase1": ({k: v for k, v in ph.items() if k != "slack_ub"} if ph else None)}
    if res.get("x") is None:
        out["ok"] = False
        out["solves"] = m.solves
        return out
    x = res["x"]
    out.update({"ok": True, "label": res["label"], "phi": res["phi"], "E_star": res["E_star"],
                "phi_history": res.get("phi_history"), "stats": optim.tree_stats(m, x),
                "policy": extract_policy(m, x), "root": _summary(m, x), "leaf_Wt": x[m.WT].copy()})
    if task.get("milp"):
        r = _milp(m, task, x, task["id"] + " MILP", log)
        out["milp"] = {"rec": r["rec"]}
        if r["x"] is not None:
            out["milp"].update({"stats": optim.tree_stats(m, r["x"]), "policy": extract_policy(m, r["x"]),
                                "root": _summary(m, r["x"])})
    if task.get("return_x"):
        out["x"] = x
    out["solves"] = m.solves
    return out


def _milp(m, task, start, tag, log=None):
    """The max-P(goal) comparison: HiGHS branch and bound (objective.milp_method = 'highs') or the deterministic
    relaxation bound + LP rounding ('round', default: the exact MILP does not close within the budget)."""
    if P.get("objective.milp_method") == "highs":
        return optim.milp(m, log or (lambda s: None), start, task["milp_tl"], task["milp_nodes"], tag=tag,
                          heuristics=task.get("milp_heuristics", True))
    return optim.milp_round(m, log or (lambda s: None), start, tag=tag)


def run_milp(w, task, log=None):
    m = world.reset_model(w)
    _apply(m, task.get("mods", []))
    m.solves = []
    r = _milp(m, task, task["start"], task["id"], log)
    out = {"id": task["id"], "rec": r["rec"], "solves": m.solves}
    if r["x"] is not None:
        out.update({"ok": True, "stats": optim.tree_stats(m, r["x"]), "policy": extract_policy(m, r["x"]),
                    "root": _summary(m, r["x"]), "leaf_Wt": r["x"][m.WT].copy()})
    else:
        out["ok"] = False
    return out


def run_crra(w, task, log=None):
    m = world.reset_model(w)
    m.solves = []
    r = optim.crra(m, log or (lambda s: None))
    out = {"id": task["id"], "solves": m.solves}
    if r["x"] is not None:
        x = r["x"]
        out.update({"ok": True, "stats": optim.tree_stats(m, x), "policy": extract_policy(m, x),
                    "root": _summary(m, x), "leaf_Wt": x[m.WT].copy()})
    else:
        out["ok"] = False
    return out


def run_beliefs(task, log=None):
    w2 = world.build(P, log=None, use_beliefs=False, phase1=False)
    pre = list(w2["m0"].solves) + list(w2["m"].solves)
    out = run_gbo(w2, {"id": task["id"], "mods": task.get("mods", [])}, log)
    out["solves"] = pre + out.get("solves", [])
    return out


def sim_policies(D, gen, truth, n, seed, chunk, policies, tpl_seed):
    s = Sim(D, gen, n, seed, truth, chunk, idio=True, tpl_truth_seed=tpl_seed)
    return s.evaluate(policies)


def run_book(task, log=None):
    """Replication or placebo book: rebuild (new marks, bids and sealed truth), re-fuse, re-solve B0 and GBO, then
    certify B0 and O1 (both recourse variants) and the risk-matched line on the book's own truth."""
    t0 = time.time()
    w2 = world.build(P, log=None, book_seed=task["seed"], variant=task["variant"], phase1=False)
    solves = list(w2["m0"].solves) + list(w2["m"].solves)
    o1 = run_gbo(w2, {"id": task["id"] + " GBO"}, log)
    solves += o1.get("solves", [])
    pols = {"B0": {"kind": "B0", "restore8": False}}
    for s_ in task["b4_scales"]:
        pols[f"B4_{s_}"] = {"kind": "B4", "restore8": False, "scale": s_}
    out = {"id": task["id"], "seed": task["seed"], "variant": task["variant"], "ok": o1.get("ok", False)}
    if o1.get("ok"):
        pols["O1_playbook"] = o1["policy"]
        pols["O1_rule"] = dict(o1["policy"], playbook=False)
        out["o1_stats"] = o1["stats"]
        out["o1_label"] = o1["label"]
    if task.get("with_f10"):
        w3 = world.build(P, log=None, book_seed=task["seed"], variant=task["variant"], use_beliefs=False, phase1=False)
        solves += list(w3["m0"].solves) + list(w3["m"].solves)
        f10 = run_gbo(w3, {"id": task["id"] + " GBO priors"}, log)
        solves += f10.get("solves", [])
        if f10.get("ok"):
            pols["F10_playbook"] = f10["policy"]
            pols["F10_rule"] = dict(f10["policy"], playbook=False)
    res = sim_policies(w2["D"], w2["gen"], w2["book"]["truth"], task["n_paths"], task["sim_seed"],
                       task["chunk"], pols, task["tpl_seed"])
    out["sim"] = {k: {kk: v[kk] for kk in ("twr", "red")} for k, v in res.items()}
    out["time_s"] = time.time() - t0
    out["solves"] = solves
    return out


def run_sim(task, log=None):
    w = WORLD
    truth = w["book"]["truth"] if task["truth"] == "sealed" else None
    s = Sim(w["D"], w["gen"], task["n_total"], task["seed"], truth, task["chunk"],
            idio=(task["truth"] == "sealed" and bool(P.get("simulation.idio"))), tpl_truth_seed=task["tpl_seed"])
    wd = s._chunk_world(task["ci"], task["n"])
    from sim import run_policy
    b0r = run_policy(w["D"], wd, {"kind": "B0", "restore8": False})
    green_ext = b0r["green_path"].astype(bool)
    out = {}
    keep = ("twr", "twr_rep", "red", "red_wf", "maxdd", "lev_max", "lev_path", "lev_pre", "capcls_path",
            "behind_path", "loss_path", "cap_path", "skipped_red")
    for name, pol in task["policies"].items():
        if pol["kind"] == "B0" and not pol.get("restore8", False):
            r = b0r
        else:
            pp = dict(pol, green_ext=green_ext) if pol["kind"] == "plan" else pol
            r = run_policy(w["D"], wd, pp)
        out[name] = {k: r[k] for k in keep}
    return {"ci": task["ci"], "res": out}


def run_task(task):
    t0 = time.time()
    try:
        tp = task["type"]
        if tp == "gbo":
            r = run_gbo(WORLD, task)
        elif tp == "milp":
            r = run_milp(WORLD, task)
        elif tp == "crra":
            r = run_crra(WORLD, task)
        elif tp == "beliefs":
            r = run_beliefs(task)
        elif tp == "book":
            r = run_book(task)
        elif tp == "sim":
            r = run_sim(task)
        else:
            raise ValueError(tp)
        r["wall_s"] = time.time() - t0
        r["type"] = tp
        r["params_used"] = sorted(P.used)
        return r
    except Exception as e:
        import traceback
        return {"id": task.get("id", task["type"]), "type": task["type"], "ok": False, "error": repr(e),
                "trace": traceback.format_exc(), "wall_s": time.time() - t0}
