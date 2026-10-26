"""Build the stakeholder demo: one self-contained HTML file (no server, no internet connection, no install).

Runs every computation on the engine (tpp.service.Platform), then embeds the results, web/app.js and
web/styles.css into web/template.html:
  - each group's status quo, optimized plan (its objective under every house limit), certified out of sample;
  - every stress for the status quo and each plan, with per-path results so the page recomputes P(hurdle), the
    distribution and the tails live when the reader moves the world probabilities or the hurdle;
  - Strategy: the risk frontier and what each lever buys (re-optimized with one lever switched off);
  - Balance Sheet: the debt-capacity frontier and the whole-fund NAV sensitivity;
  - Liquidity: owner-distribution policies under the prolonged DPI decline;
  - Asset Allocation: the return basis (strategy / blend / underwritten / actual), PE-program variants, holding
    cards with live return preferences, and swap tests;
  - IC: every plan, the consensus plan and the 10% target alone on one view, under every stress;
  - every case (plan x stress) carries each group's objective as a pass/fail test per path (tpp.metrics), so the page
    reports P(10%), P(each group's objective) and P(both) live;
  - leverage on the hedge-fund allocation: the borrowing needed for 10% (status quo and consensus plan);
  - the five years, year by year: growth against the target path and representative paths;
  - doing nothing (no sales, no new commitments, no rebalancing, no new debt) beside every plan, and the Strategy
    group's north star (10% a year) as the reference path;
  - the Yale model (Takahashi-Alexander) as a benchmark on ADIC's book.

Output: out/ADIC_TPP_Demo.html plus one copy per group that opens on its view. The files contain holding-level
data from the MSIP-labelled inputs: out/ is git-ignored; share them only inside ADIC.

usage: python build_demo.py [--fund-file PATH] [--er-file PATH] [--out DIR] [--quick]
"""
from __future__ import annotations

import argparse
import base64
import copy
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402

from tpp import metrics, paths, plan as planmod, service, sim, stakeholders as sh, substitution, yale  # noqa: E402
from tpp.legacy import quantile_w  # noqa: E402
from tpp.buckets import BY_ID, CATALOG  # noqa: E402
from tpp.returns import WORLDS  # noqa: E402

T0 = time.time()


def say(msg: str):
    print(f"[{time.time() - T0:6.1f}s] {msg}", flush=True)


def enc_twr(o: dict) -> str:
    """Per-path five-year TWR as int16 basis points, base64 (little-endian). Rounded down, so the page's test
    'TWR >= hurdle' is exact for any hurdle on the basis-point grid (it then matches the engine's own count)."""
    bp = np.clip(np.floor(np.asarray(o["twr"]) * 1e4 + 1e-9), -32767, 32767).astype("<i2")
    return base64.b64encode(bp.tobytes()).decode("ascii")


def enc_flags(flags: np.ndarray) -> str:
    """Per-path objective bits (tpp.metrics.OBJ_*), one byte a path, base64."""
    return base64.b64encode(np.asarray(flags, np.uint8).tobytes()).decode("ascii")


def flags_for(o: dict, o_sq: dict | None, house: dict) -> np.ndarray:
    return metrics.objective_flags(o, o_sq, float(house["lev_cap"]), float(house["overcommit"]), float(house["goal_rate"]))


def owner_meta(pf) -> dict:
    """The owner's distribution rule as the page needs it: the expected draw rate by year (base case, certification
    paths) for the north star's fund-size path, and the band."""
    v = pf.view("ic")
    house = pf.house()
    bkey, B, R = pf.book_for(v["prefs"], house)
    S = pf.paths_for(bkey, B, "oos", "base", pf._pi(v["prefs"]), house)
    w = S.prob / S.prob.sum()
    return {"draw_mean": [float(w @ S.draw[:, t]) for t in range(5)],
            "floor": float(pf.P.get("owner_distribution.rule_floor")), "cap": float(pf.P.get("owner_distribution.rule_cap"))}


def brief(s: dict) -> dict:
    return service._brief(s)


def lean(s: dict) -> dict:
    """A summary without the heavy histogram edges (kept once at the top)."""
    out = {k: v for k, v in s.items() if k not in ("hist",)}
    out["hist_p"] = s["hist"]["p"]
    return out


def sim_do_nothing(pf, role, stress, house=None, prefs=None):
    """Doing nothing on the same paths as sim_pair."""
    v = pf._variant_view(role, prefs)
    house = house or pf.house()
    bkey, B, R = pf.book_for(v["prefs"], house)
    S = pf.paths_for(bkey, B, "oos", stress, pf._pi(v["prefs"]), house)
    return sim.simulate(S, planmod.do_nothing(B, pf.P, house), pf.P, {**pf._sim_settings(house), **planmod.DO_NOTHING_SIM})


def sim_pair(pf, role, stress, plan_obj, house=None, prefs=None):
    v = pf._variant_view(role, prefs)
    house = house or pf.house()
    bkey, B, R = pf.book_for(v["prefs"], house)
    S = pf.paths_for(bkey, B, "oos", stress, pf._pi(v["prefs"]), house)
    sset = pf._sim_settings(house)
    sq = planmod.status_quo(B, pf.P, house, program=True)
    np_ = planmod.status_quo(B, pf.P, house, program=False)
    o_sq = sim.simulate(S, sq, pf.P, sset)
    o_np = sim.simulate(S, np_, pf.P, sset)
    o_pl = sim.simulate(S, plan_obj, pf.P, sset) if plan_obj is not None else None
    return B, S, o_sq, o_np, o_pl


def role_block(pf, role: str) -> dict:
    lens = sh.LENSES[role]
    v = pf.view(role)
    house = pf.house()
    g = float(house["goal_rate"])
    say(f"{lens['title']}: optimizing ({v['objective']}, {v['prefs']['basis']} basis, stress '{v['stress']}')")
    op = pf.optimize(role, progress=lambda m: None)
    plan_obj = planmod.Plan.from_dict(op["plan"])
    block = {"lens": lens, "prefs": v["prefs"], "objective": v["objective"], "objective_text": op["objective_text"],
             "stress": v["stress"], "label": op["label"], "plan": op["plan"], "summary": op["summary"],
             "change_list": op["change_list"], "duals": op["duals"], "in_sample": op["in_sample"],
             "solve_log": op["solve_log"], "lp_size": op["lp_size"], "eps": op["eps"], "phi": op.get("phi"),
             "alternatives": op["alternatives"], "card_counts": op["card_counts"], "stresses": {}}
    say(f"{lens['title']}: stresses")
    for st in paths.STRESSES:
        B, S, o_sq, o_np, o_pl = sim_pair(pf, role, st, plan_obj)
        o_dn = sim_do_nothing(pf, role, st)
        s_sq, s_np, s_pl, s_dn = (metrics.summarize(o, g) for o in (o_sq, o_np, o_pl, o_dn))
        fl = {"sq": flags_for(o_sq, None, house), "np": flags_for(o_np, o_sq, house), "plan": flags_for(o_pl, o_sq, house),
              "dn": flags_for(o_dn, o_sq, house)}
        entry = {"twr": {"sq": enc_twr(o_sq), "np": enc_twr(o_np), "plan": enc_twr(o_pl), "dn": enc_twr(o_dn)},
                 "flags": {k: enc_flags(v_) for k, v_ in fl.items()},
                 "objectives": {k: metrics.objective_rates(o, fl[k], g)
                                for k, o in (("sq", o_sq), ("np", o_np), ("plan", o_pl), ("dn", o_dn))},
                 "brief": {"sq": brief(s_sq), "np": brief(s_np), "plan": brief(s_pl), "dn": brief(s_dn)},
                 "delta": metrics.paired_delta(o_pl, o_sq), "program_effect": metrics.paired_delta(o_sq, o_np),
                 # fans and cash flows for every stress, so each view's charts follow its stress control
                 "full": {"sq": lean(s_sq), "plan": lean(s_pl), "dn": lean(s_dn)}}
        if st in (v["stress"], "base"):
            entry["full"]["np"] = lean(s_np)
            entry["program"] = op["change_list"]["pe_program"] if st == v["stress"] else None
        block["stresses"][st] = entry
    return block


def adaptivity_extras(pf) -> dict:
    """What adaptivity adds: the Strategy plan as built (later decisions by the market class observed by then)
    against the same objective with one fixed schedule for every path, both with validated guards, paired on the same
    paths under every stress; and the adaptive plan without the countercyclical secondaries mandate (where the gain
    comes from)."""
    v = pf.view("strategy")
    house = pf.house()
    g = float(house["goal_rate"])
    bkey, B, R = pf.book_for(v["prefs"], house)
    sset = pf._sim_settings(house)
    say("Strategy: what adaptivity adds")
    adaptive = planmod.Plan.from_dict(pf.plans["strategy"]["plan"])
    quiet = lambda m: None
    fixed = planmod.Plan.from_dict(pf.optimize("strategy", persist=False, house_override={"contingent": False}, progress=quiet)["plan"])
    no_mand = planmod.Plan.from_dict(pf.optimize("strategy", persist=False, house_override={"opportunistic_secondaries": False},
                                                 progress=quiet)["plan"])
    pick = lambda s_: {k: s_[k] for k in ("p_goal", "p_goal_ci", "twr_mean", "cvar10", "p_red", "p_revolver", "p_preserve")}
    rows, nm = [], None
    for st in paths.STRESSES:
        S = pf.paths_for(bkey, B, "oos", st, pf._pi(v["prefs"]), house)
        o_f, o_a = sim.simulate(S, fixed, pf.P, sset), sim.simulate(S, adaptive, pf.P, sset)
        d = metrics.paired_delta(o_a, o_f)
        rows.append({"stress": st, "fixed": pick(metrics.summarize(o_f, g)), "adaptive": pick(metrics.summarize(o_a, g)),
                     "d_p_goal": d["d_p_goal"], "d_p_goal_ci": d["d_p_goal_ci"]})
        if st == v["stress"]:
            o_n = sim.simulate(S, no_mand, pf.P, sset)
            dn = metrics.paired_delta(o_n, o_f)
            nm = {"adaptive": pick(metrics.summarize(o_n, g)), "d_p_goal": dn["d_p_goal"], "d_p_goal_ci": dn["d_p_goal_ci"]}
    base = next(r for r in rows if r["stress"] == v["stress"])
    say(f"   adaptive minus fixed: {base['d_p_goal']:+.4f} {np.round(base['d_p_goal_ci'], 4).tolist()}; "
        f"without the mandate {nm['d_p_goal']:+.4f}")
    return {"stresses": rows, "no_mandate": nm, "fixed_plan": fixed.to_dict()}


def strategy_extras(pf) -> dict:
    """Risk frontier (depth-guard allowance and leverage cap) and what each lever buys (switch-offs)."""
    out = {"frontier": [], "levers": []}
    base = pf.house()

    def run(name, house_patch, key):
        r = pf.optimize("strategy", persist=False, house_override={**SWEEP, **house_patch}, progress=lambda m: None)
        s = r["metrics"]
        row = {"name": name, "key": key, "p_goal": s["p_goal"], "p_goal_ci": s["p_goal_ci"], "twr_mean": s["twr_mean"],
               "cvar10": s["cvar10"], "cvar1": s["cvar1"], "p_red": s["p_red"], "p_revolver": s["p_revolver"],
               "lev_max_p95": max(s["fans"]["lev"]["p95"]), "d_p_goal": r["delta"]["d_p_goal"],
               "d_p_goal_ci": r["delta"]["d_p_goal_ci"], "label": r["label"],
               "financing": r["change_list"]["financing"], "r1": r["change_list"]["r1"]}
        say(f"   {name}: P(goal) {s['p_goal']:.3f} CVaR10 {s['cvar10']:.4f}")
        return row

    say("Strategy: risk frontier")
    for d in (0.0, 0.02, 0.05):
        out["frontier"].append(run(f"Tail allowance {d:.0%} of NAV", {"depth_guard": True, "depth_delta": d}, f"delta{d}"))
    out["frontier"].append(run("No depth guard", {"depth_guard": False}, "noguard"))
    for L in (1.0, 1.30):
        out["frontier"].append(run(f"Leverage cap {L:.2f}x", {"lev_cap": L}, f"lev{L}"))
    say("Strategy: what each lever buys")
    levers = [("All levers (the plan)", {}),
              ("No new debt", {"allow_debt": False}),
              ("No synthetic beta", {"allow_beta": False}),
              ("No liquid reallocation", {"range_band": [1.0, 1.0]}),
              ("Pacing held at status quo", {"pace_mult": [1.0, 1.0], "new_strategy_entry_bn": 0.0,
                                             "coinvest_extra_bn": 0.0}),
              ("PE program sold evenly (no timing)", {"even_program": True}),
              ("No other secondary sales", {"allow_other_sales": False})]
    for name, patch in levers:
        out["levers"].append(run(name, patch, name))
    return out


TARGET_ONLY = [("to_none", "Target only, no borrowing", 1.0, None),
               ("to_hfcap", "Target only, no borrowing, hedge funds at most 2x today's program", 1.0, 2.0),
               ("to_115", "Target only, leverage up to 1.15x", 1.15, None),
               ("to_150", "Target only, leverage up to 1.5x", 1.5, None),
               ("to_200", "Target only, leverage up to 2.0x", 2.0, None)]


def target_only_extras(pf) -> dict:
    """The 10% target alone: the Strategy objective (GBO) with every group's policy limit removed
    (tpp.stakeholders.target_only), swept over borrowing; each plan runs under its own operating rules (no reserve
    floor) and is judged against every group's objective with the house limits."""
    v = pf.view("strategy")
    house = pf.house()
    g = float(house["goal_rate"])
    bkey, B, R = pf.book_for(v["prefs"], house)
    units = {u.id: u for u in B.units}
    rows, plans = [], {}
    say("Strategy: the 10% target alone")
    sq_house = {st: sim_pair(pf, "strategy", st, None)[2] for st in ("base", "crisis_y1", "hf_gates")}
    for key, name, lev, hf_mult in TARGET_ONLY:
        ov = sh.target_only(lev, {"HF": hf_mult * float(B.liquid["HF"])} if hf_mult else None)
        r = pf.optimize("strategy", objective="gbo", persist=False, house_override={**SWEEP, **ov}, progress=lambda m: None)
        p = planmod.Plan.from_dict(r["plan"])
        p.name = name
        plans[key] = (p, ov)
        o_pl = sim_pair(pf, "strategy", "base", p, house={**house, **ov})[4]
        rates = metrics.objective_rates(o_pl, flags_for(o_pl, sq_house["base"], house), g)
        s = r["metrics"]
        stressed = {}
        for st in ("crisis_y1", "hf_gates"):
            c_pl = sim_pair(pf, "strategy", st, p, house={**house, **ov})[4]
            cs = metrics.summarize(c_pl, g)
            cr = metrics.objective_rates(c_pl, flags_for(c_pl, sq_house[st], house), g)
            stressed[st] = {"p_goal": cs["p_goal"], "cvar10": cs["cvar10"], "p_red": cs["p_red"],
                            "p_bs": cr["p_bs"], "p_liq": cr["p_liq"], "p_aa": cr["p_aa"], "p_all": cr["p_all"]}
        sold = {u: float(sum(fr)) for u, fr in r["plan"]["sell"].items() if sum(fr) > 1e-4}
        rows.append({"key": key, "name": name, "lev_cap": lev,
                     "hf_cap_bn": hf_mult * float(B.liquid["HF"]) if hf_mult else None,
                     "p_goal": s["p_goal"], "p_goal_ci": s["p_goal_ci"], "by_world": s["by_world"],
                     "twr_mean": s["twr_mean"], "cvar10": s["cvar10"], "cvar1": s["cvar1"], "p_red": s["p_red"],
                     "p_revolver": s["p_revolver"], "objectives": rates, "stresses": stressed,
                     "liquid": dict(r["plan"]["liquid"]),
                     "liquid_sq": {b: float(B.liquid.get(b, 0.0)) for b in r["plan"]["liquid"]},
                     "reserve_bn": r["plan"]["cash"] + r["plan"]["treasury"],
                     "reserve_sq_bn": float(B.liquid.get("CASH", 0.0) + B.liquid.get("TREASURY", 0.0)),
                     "borrowing_bn": float(sum(r["plan"]["term_sched"]) + r["plan"]["navf_bn"]),
                     "beta_bn": r["plan"]["beta_bn"],
                     "commit_by_year": [float(sum(c[t] for c in r["plan"]["commit"].values())) for t in range(5)],
                     "commit_sq_bn": float(sum(B.pacing_sq.values())),
                     "sold_nav_bn": float(sum(units[u].nav0 * f for u, f in sold.items())),
                     "sold": [{"label": BY_ID[units[u].bucket].label, "part": units[u].part, "fraction": f}
                              for u, f in sold.items()],
                     "pe_program_sold": any(units[u].pe_program and units[u].part == "tail" for u in sold),
                     "ovc_t5_mean": s["fans"]["ovc"]["mean"][-1]})
        say(f"   {name}: P(goal) {s['p_goal']:.3f} CVaR10 {s['cvar10']:.4f} forced {s['p_red']:.3f} "
            f"objectives BS {rates['p_bs']:.2f} liquidity {rates['p_liq']:.2f} ahead {rates['p_aa']:.2f}")
    return {"rows": rows, "plans": plans}


def ic_cases(pf, plans: list) -> dict:
    """Every plan on the IC view under every stress: per-path TWR and objective flags (judged against the status
    quo under the same stress and the house limits), so the page shows any plan x stress cell live."""
    v = pf.view("ic")
    house = pf.house()
    g = float(house["goal_rate"])
    bkey, B, R = pf.book_for(v["prefs"], house)
    ids = {u.id for u in B.units}
    out = {key: {} for key, _, _ in plans}
    for st in paths.STRESSES:
        S = pf.paths_for(bkey, B, "oos", st, pf._pi(v["prefs"]), house)
        o_sq = None
        for key, p, ov in plans:
            p = copy.deepcopy(p)
            p.sell = {k: v_ for k, v_ in p.sell.items() if k in ids}
            o = sim.simulate(S, p, pf.P, pf._sim_settings({**house, **(ov or {})}))
            if key == "status_quo":
                o_sq = o
            fl = flags_for(o, None if key == "status_quo" else o_sq, house)
            out[key][st] = {"twr": enc_twr(o), "flags": enc_flags(fl), "rates": metrics.objective_rates(o, fl, g)}
        say(f"   IC cases: {st}")
    return out


HF_GRID = [0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100]
# sensitivity sweeps compare levers with each other: the fixed-schedule optimizer on fewer in-sample scenarios keeps
# the build quick (the groups' plans and the adaptivity comparison use the full adaptive optimizer)
SWEEP = {"contingent": False, "n_lp_paths": 120}


def _cross(rows, key, target, x="borrow_bn"):
    """First x at which rows[key] reaches target (linear between grid points), or None."""
    for a, b in zip(rows, rows[1:]):
        if a[key] < target <= b[key]:
            return a[x] + (b[x] - a[x]) * (target - a[key]) / (b[key] - a[key])
    return rows[0][x] if rows and rows[0][key] >= target else None


def hf_leverage_extras(pf) -> dict:
    """Fund-level term debt drawn today (SOFR + term spread, held to the horizon) and invested in the hedge-fund
    allocation, on the status quo and on the consensus plan: how much borrowing reaches 10%. IC view; every group's
    objective tested against the house limits."""
    v = pf.view("ic")
    house = pf.house()
    g = float(house["goal_rate"])
    bkey, B, R = pf.book_for(v["prefs"], house)
    sset = pf._sim_settings(house)
    bases = {"status_quo": planmod.status_quo(B, pf.P, house, program=True)}
    if "consensus" in pf.plans:
        bases["consensus"] = planmod.Plan.from_dict(pf.plans["consensus"]["plan"])

    def levered(p0, b):
        q = copy.deepcopy(p0)
        q.liquid = dict(q.liquid)
        q.liquid["HF"] = float(q.liquid.get("HF", 0.0)) + b
        sched = list(q.term_sched or [q.term_bn, 0.0, 0.0])
        sched[0] += b
        q.term_sched, q.term_bn = sched, float(sum(sched))
        return q

    out = {"W0_bn": B.W0, "hf_today_bn": float(B.liquid["HF"]), "grid": HF_GRID,
           "rate": float(pf.P.get("rates.sofr")) + float(pf.P.get("corporate_finance.term_spread")),
           "lev_cap": float(house["lev_cap"]), "bases": {}, "cross": {}}
    say("IC: leverage on the hedge-fund allocation")
    for stress in ("base", "crisis_y1", "hf_gates"):
        S = pf.paths_for(bkey, B, "oos", stress, pf._pi(v["prefs"]), house)
        w = S.prob / S.prob.sum()
        o_sq = sim.simulate(S, bases["status_quo"], pf.P, sset)
        for name, p0 in bases.items():
            rows = out["bases"].setdefault(name, {}).setdefault(stress, [])
            for b in HF_GRID:
                o = o_sq if (name == "status_quo" and b == 0) else sim.simulate(S, levered(p0, b), pf.P, sset)
                s_ = metrics.summarize(o, g)
                rr = metrics.objective_rates(o, flags_for(o, None if (name == "status_quo" and b == 0) else o_sq, house), g)
                rows.append({"borrow_bn": b, "lev0": float(o["r_lev"][:, 0].mean()), "p_goal": s_["p_goal"],
                             "twr_mean": s_["twr_mean"], "twr_p50": float(quantile_w(o["twr"], 0.5, w)),
                             "cvar10": s_["cvar10"], "cvar1": s_["cvar1"], "p_red": s_["p_red"],
                             "p_revolver": s_["p_revolver"],
                             "lev_p95": float(max(quantile_w(o["r_lev"][:, t], 0.95, w) for t in range(6))),
                             "p_bs": rr["p_bs"], "p_liq": rr["p_liq"], "p_all": rr["p_all"],
                             "by_world": {k: x["p_goal"] for k, x in s_["by_world"].items()}})
    for name in bases:
        rows = out["bases"][name]["base"]
        out["cross"][name] = {"mean_10": _cross(rows, "twr_mean", g), "median_10": _cross(rows, "twr_p50", g),
                              "p_55": _cross(rows, "p_goal", 0.55), "p_60": _cross(rows, "p_goal", 0.60)}
        say(f"   {name}: mean reaches {g:.0%} at {out['cross'][name]['mean_10']}, median at {out['cross'][name]['median_10']}")
    return out


def yale_extras(pf) -> dict:
    """The Yale model (Takahashi-Alexander) on ADIC's book: its deterministic projection of private calls,
    distributions and NAV against the engine's distribution (status quo without the program, base case and with the
    exit window reopening), and its implied DPI by vintage against the actual."""
    v = pf.view("strategy")
    house = pf.house()
    g = float(house["goal_rate"])
    bkey, B, R = pf.book_for(v["prefs"], house)
    sq0 = planmod.status_quo(B, pf.P, house, program=False)
    as_of = float(pf.quality["as_of"][:4]) + float(pf.quality["as_of"][5:7]) / 12
    actual = {r["vintage"]: r["dpi"] for r in pf.dpi}
    fit = yale.fit_to_vintages(R["holdings"], B.bucket_ret, pf.P, as_of, actual)
    fam0, fam1 = yale.families(pf.P), yale.families(pf.P, fit["life_mult"], fit["bow_mult"])
    out = {"ta": yale.project(B, sq0, fam0), "ta_fit": yale.project(B, sq0, fam1), "fit": fit, "engine": {}}
    for st in ("base", "exit_window_opens"):
        o = sim_pair(pf, "strategy", st, None)[3]
        s_ = metrics.summarize(o, g)
        out["engine"][st] = {"calls": s_["flows"]["calls"], "dist": s_["flows"]["dist"], "net": s_["net_private_fan"],
                             "priv": s_["fans"]["priv"], "p_goal": s_["p_goal"], "twr_q": s_["twr_q"]}
    dfit = {r["vintage"]: r["dpi_yale"] for r in yale.vintage_dpi(R["holdings"], B.bucket_ret, fam1, as_of)}
    out["dpi"] = [{**r, "dpi_fit": dfit.get(r["vintage"]), "dpi_actual": actual.get(r["vintage"])}
                  for r in yale.vintage_dpi(R["holdings"], B.bucket_ret, fam0, as_of)]
    out["paid_in"] = yale.vintage_paid_in(R["holdings"], B.bucket_ret, fam0, as_of)
    out["families"] = fam0
    say("Yale model benchmark")
    return out


def aa_extras(pf) -> dict:
    out = {"basis": [], "program_variants": [], "swaps": []}
    house = pf.house()
    g = float(house["goal_rate"])
    say("Asset Allocation: return basis comparison")
    for basis in ("strategy", "blend", "underwritten", "actual"):
        ev = pf.evaluate("asset_allocation", prefs_override={"basis": basis}, progress=lambda m: None)
        r = pf.optimize("asset_allocation", persist=False, prefs_override={"basis": basis}, house_override=SWEEP,
                        progress=lambda m: None)
        _, B, R = pf.book_for(pf._variant_view("asset_allocation", {"basis": basis})["prefs"], house)
        h = R["holdings"]
        w = h["nav_bn"].to_numpy()
        out["basis"].append({"basis": basis, "book_return_base": float(np.average(h["r_base"], weights=w)),
                             "book_return_exp": float(np.average(h["r_exp"], weights=w)),
                             "book_return_ce": float(np.average(h["r_ce"], weights=w)),
                             "sq": brief(ev["status_quo"]), "np": brief(ev["no_program"]),
                             "program_effect": ev["program_effect"], "plan": brief(r["metrics"]),
                             "delta": r["delta"], "sells": r["change_list"]["sells"],
                             "pe_program": r["change_list"]["pe_program"]})
        say(f"   {basis}: book E {out['basis'][-1]['book_return_exp']:.4f}  SQ {ev['status_quo']['p_goal']:.3f} "
            f"program effect {ev['program_effect']['d_p_goal']:+.3f}  plan {r['metrics']['p_goal']:.3f}")
    say("Asset Allocation: PE program variants")
    v = pf.view("asset_allocation")
    bkey, B, R = pf.book_for(v["prefs"], house)
    S = pf.paths_for(bkey, B, "oos", v["stress"], pf._pi(v["prefs"]), house)
    sset = pf._sim_settings(house)
    o_np = sim.simulate(S, planmod.status_quo(B, pf.P, house, program=False), pf.P, sset)
    variants = [("No program", {"pe_program_enabled": False}),
                ("As decided: $20bn exposure, underperformers, 3 years", {}),
                ("Pro rata across all PE", {"pe_program_selection": "pro_rata"}),
                ("$20bn of NAV (not exposure)", {"pe_program_basis": "nav"}),
                ("Faster: 2 years", {"pe_program_years": 2}),
                ("Smaller: $10bn", {"pe_program_total_bn": 10.0})]
    for name, patch in variants:
        hs = {**house, **patch}
        if patch.get("pe_program_total_bn"):
            _, B2, _ = pf.book_for(v["prefs"], hs)
        else:
            B2 = B
        pl = planmod.status_quo(B2, pf.P, hs, program=hs.get("pe_program_enabled", True))
        S2 = S if B2 is B else pf.paths_for(pf.book_for(v["prefs"], hs)[0], B2, "oos", v["stress"], pf._pi(v["prefs"]), hs)
        o = sim.simulate(S2, pl, pf.P, sset)
        s = metrics.summarize(o, g)
        o_np2 = o_np if B2 is B else sim.simulate(S2, planmod.status_quo(B2, pf.P, hs, program=False), pf.P, sset)
        prog = planmod.program_summary(B2, pl)
        cl = substitution.change_list(B2, pl, planmod.status_quo(B2, pf.P, hs, program=False), S2)
        out["program_variants"].append({"name": name, "metrics": brief(s), "vs_no_program": metrics.paired_delta(o, o_np2),
                                         "exposure_bn": prog["pe_exposure_bn"], "nav_bn": prog["pe_nav_bn"],
                                         "proceeds_bn": cl["pe_program"]["proceeds_bn"],
                                         "unfunded_bn": cl["pe_program"]["unfunded_bn"],
                                         "by_tranche_bn": prog["by_tranche_bn"]})
    say("Asset Allocation: swap tests")
    cards = pf.holdings("asset_allocation")["rows"]
    winners = [r for r in cards if r["card"] == "SELL?"][:10]
    laggards = sorted([r for r in cards if r["card"] == "SELL" and r.get("ce_pref") is not None],
                      key=lambda r: r["ce_pref"])[:10]
    for name, rows, target in (("Sell the 10 largest bid-premium holdings, buy Secondaries LP-led co-invest", winners, "SEC_LP_C"),
                               ("Sell the 10 lowest-return program holdings now, buy hedge funds", laggards, "HF"),
                               ("Sell the 10 largest bid-premium holdings, buy Infra & NR N. America co-invest", winners, "INF_NA_C")):
        if not rows:
            continue
        sw = pf.swap("asset_allocation", [r["FUND_CODE"] for r in rows], target, progress=lambda m: None)
        sw["name"] = name
        sw["holdings"] = [{"name": r["FUND_NAME"], "nav_bn": r["nav_bn"], "bid": r["bid0"], "ce": r["ce_pref"]} for r in rows]
        out["swaps"].append(sw)
        say(f"   {name}: dP {sw['delta']['d_p_goal']:+.4f} dTWR {sw['delta']['d_twr']:+.5f}")
    return out


def liquidity_extras(pf) -> dict:
    out = {"draw_policies": []}
    plan_d = pf.plans.get("liquidity", {}).get("plan")
    pl = planmod.Plan.from_dict(plan_d) if plan_d else None
    v = pf.view("liquidity")
    g = float(pf.house()["goal_rate"])
    say("Liquidity: owner-distribution policies")
    lo, hi = float(pf.P.get("owner_distribution.rule_floor")), float(pf.P.get("owner_distribution.rule_cap"))
    for name, patch in ((f"Oil-linked rule ({lo:.0%}-{hi:.0%})", {"draw_mode": "rule"}),
                        ("Fixed 7% of NAV", {"draw_mode": "fixed_rate", "draw_rate": 0.07}),
                        ("Fixed 10% of NAV", {"draw_mode": "fixed_rate", "draw_rate": 0.10})):
        hs = {**pf.house(), **patch}
        B, S, o_sq, o_np, o_pl = sim_pair(pf, "liquidity", v["stress"], pl, house=hs)
        s_sq = metrics.summarize(o_sq, g)
        s_pl = metrics.summarize(o_pl, g) if o_pl is not None else None
        out["draw_policies"].append({"name": name, "sq": brief(s_sq), "plan": brief(s_pl) if s_pl else None,
                                     "draws_sq": s_sq["flows"]["draw"], "lcr_sq": s_sq["lcr_fan"],
                                     "lcr_plan": s_pl["lcr_fan"] if s_pl else None,
                                     "reserve_sq": s_sq["fans"]["reserve"],
                                     "reserve_plan": s_pl["fans"]["reserve"] if s_pl else None})
        say(f"   {name}: SQ P(revolver) {s_sq['p_revolver']:.3f} P(red) {s_sq['p_red']:.4f} LCR p5 {s_sq['lcr_min_p5']:.2f}")
    return out


def bs_extras(pf) -> dict:
    out = {"debt_frontier": [], "nav_sensitivity": []}
    say("Balance Sheet: debt-capacity frontier (the hurdle objective under this group's view)")
    for cap, beta in ((0.0, False), (5.0, False), (10.0, False), (10.0, True), (20.0, True)):
        r = pf.optimize("balance_sheet", objective="gbo", persist=False,
                        house_override={**SWEEP, "new_term_max_bn": cap, "allow_beta": beta, "allow_debt": cap > 0},
                        progress=lambda m: None)
        s = r["metrics"]
        out["debt_frontier"].append({"name": f"New term debt up to ${cap:.0f}bn" + (", synthetic beta allowed" if beta else ""),
                                     "cap": cap, "beta": beta, "p_goal": s["p_goal"], "twr_mean": s["twr_mean"],
                                     "cvar10": s["cvar10"], "lev_max_p95": max(s["fans"]["lev"]["p95"]),
                                     "debt_p95_bn": max(s["fans"]["debt"]["p95"]), "financing": r["change_list"]["financing"],
                                     "r1": r["change_list"]["r1"], "d_p_goal": r["delta"]["d_p_goal"]})
        say(f"   cap {cap} beta {beta}: P(goal) {s['p_goal']:.3f}")
    say("Balance Sheet: whole-fund NAV sensitivity")
    for nav in (170.0, 177.0, 185.0):
        ev = pf.evaluate("balance_sheet", house_override={"total_nav_bn": nav}, progress=lambda m: None)
        out["nav_sensitivity"].append({"total_nav_bn": nav, "sq": brief(ev["status_quo"]),
                                       "np": brief(ev["no_program"])})
    return out


def holdings_block(pf) -> dict:
    """Holdings with the AA cards and the raw return components the page needs to recompute returns live."""
    hd = pf.holdings("asset_allocation")
    rows = hd["rows"]
    v = pf.view("asset_allocation")
    _, B, R = pf.book_for(v["prefs"], pf.house())
    h = R["holdings"].set_index("FUND_CODE")
    cols = ["FUND_CODE", "FUND_NAME", "bucket", "department", "vehicle", "INVESTMENT_CLASS", "INVESTMENT_STYLE",
            "vintage", "age", "nav_bn", "unfunded_bn", "uw_irr", "act_irr", "ACTUAL_TVPI", "ACTUAL_DPI", "S_down",
            "S_base", "S_up", "uw_beta", "uw_youth", "act_excess", "act_cred", "bid0", "p_star", "p_hold", "card",
            "why", "tranche", "unit", "confidence", "rule", "perf"]
    data = []
    for r in rows:
        code = r["FUND_CODE"]
        hr = h.loc[code]
        rec = []
        for c in cols:
            val = r.get(c) if c in r else (hr[c] if c in hr.index else None)
            if isinstance(val, (np.floating, float)):
                val = None if not np.isfinite(val) else round(float(val), 5)
            elif isinstance(val, (np.integer,)):
                val = int(val)
            elif val is not None and not isinstance(val, (str, int, bool)):
                try:
                    val = None if val != val else str(val)
                except Exception:
                    val = str(val)
            rec.append(val)
        data.append(rec)
    roles_cards = {}
    for role in sh.ROLES:
        hr_ = pf.holdings(role)["rows"]
        roles_cards[role] = {r["FUND_CODE"]: [r["card"], r.get("p_star"), r.get("why")] for r in hr_}
    return {"columns": cols, "rows": data, "cards": roles_cards, "alternatives": hd["alternatives"]}


def assumptions_list(pf) -> list:
    out = []
    P = pf.P
    for key in P.leaves():
        leaf = P._leaf(key)
        out.append({"key": key, "value": leaf["value"], "unit": leaf.get("unit"), "rationale": leaf.get("rationale"),
                    "source": leaf.get("source")})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fund-file")
    ap.add_argument("--er-file")
    ap.add_argument("--out", default=str(HERE / "out"))
    ap.add_argument("--quick", action="store_true", help="fewer paths (for a fast preview)")
    ap.add_argument("--from-payload", action="store_true",
                    help="re-render the HTML from out/payload.json without recomputing (front-end changes)")
    a = ap.parse_args()
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    if a.from_payload:
        render(out_dir, (out_dir / "payload.json").read_text(encoding="utf-8"))
        return
    say("loading data and classifying holdings")
    pf = service.Platform(state_dir=HERE / "state", fund_file=a.fund_file, er_file=a.er_file, quick=a.quick)
    # each group's settings file, a template to edit before the next build (written once, never overwritten)
    for role in sh.ROLES:
        if not (pf.state_dir / f"{role}.json").exists():
            pf._save_json(f"{role}.json", pf.states[role])
    if not (pf.state_dir / "ic.json").exists():
        pf._save_json("ic.json", pf.ic)
    ov = pf.overview("strategy")
    data = {"meta": {"built": time.strftime("%Y-%m-%d %H:%M"), "files": pf.files, "n_oos": pf.n_oos, "n_lp": pf.n_lp,
                     "worlds": WORLDS, "hist_edges": None, "goal_rate": float(pf.house()["goal_rate"]),
                     "W0": ov["book"]["W0_bn"], "Wstar": ov["book"]["Wstar_bn"], "quick": bool(a.quick),
                     "n_val": pf.n_val, "owner": owner_meta(pf)},
            "overview": ov, "stresses": paths.STRESSES, "objectives": sh.OBJECTIVES, "house": pf.house(),
            "owner": sh.SETTING_OWNER, "roles": {}}
    for role in sh.ROLES:
        data["roles"][role] = role_block(pf, role)
    data["meta"]["hist_edges"] = np.linspace(-0.10, 0.25, 36).tolist()
    data["roles"]["strategy"]["extras"] = strategy_extras(pf)
    data["roles"]["strategy"]["extras"]["adaptivity"] = adaptivity_extras(pf)
    to = target_only_extras(pf)
    data["roles"]["strategy"]["extras"]["target_only"] = to["rows"]
    data["roles"]["asset_allocation"]["extras"] = aa_extras(pf)
    data["roles"]["liquidity"]["extras"] = liquidity_extras(pf)
    data["roles"]["balance_sheet"]["extras"] = bs_extras(pf)
    say("IC: every plan and the consensus plan on one view")
    extra = [(k, *to["plans"][k]) for k in ("to_none", "to_150")]
    _, B_ic, _ = pf.book_for(pf.view("ic")["prefs"], pf.house())
    extra = [("do_nothing", planmod.do_nothing(B_ic, pf.P, pf.house()), dict(planmod.DO_NOTHING_SIM))] + extra
    data["ic"] = pf.compare(include_consensus=True, progress=lambda m: None, extra_plans=extra)
    v = pf.view("ic")
    house = pf.house()
    bkey, B, R = pf.book_for(v["prefs"], house)
    plans = [("status_quo", planmod.status_quo(B, pf.P, house, program=True), None),
             ("no_program", planmod.status_quo(B, pf.P, house, program=False), None)]
    plans += [(k, planmod.Plan.from_dict(pf.plans[k]["plan"]), None) for k in sh.ROLES + ["consensus"] if k in pf.plans]
    plans += extra
    say("IC: every plan under every stress")
    cases = ic_cases(pf, plans)
    data["ic"]["cases"] = cases
    data["ic"]["twr"] = {key: cases[key][v["stress"]]["twr"] for key, _, _ in plans}
    data["ic"]["hf_leverage"] = hf_leverage_extras(pf)
    data["yale"] = yale_extras(pf)
    data["ic"]["consensus_plan"] = pf.plans.get("consensus", {}).get("plan")
    say("holdings and cards")
    data["holdings"] = holdings_block(pf)
    data["assumptions"] = assumptions_list(pf)
    payload = json.dumps(service.jsonable(data), separators=(",", ":"))
    say(f"payload {len(payload) / 1e6:.2f} MB")
    (out_dir / "payload.json").write_text(payload, encoding="utf-8")
    render(out_dir, payload)


def render(out_dir: Path, payload: str):
    web = HERE / "web"
    tpl = (web / "template.html").read_text(encoding="utf-8")
    html = (tpl.replace("/*__STYLES__*/", (web / "styles.css").read_text(encoding="utf-8"))
               .replace("/*__APP__*/", (web / "app.js").read_text(encoding="utf-8"))
               .replace("__DATA__", payload.replace("</", "<\\/")))
    main_file = out_dir / "ADIC_TPP_Demo.html"
    main_file.write_text(html, encoding="utf-8")
    for role in sh.ROLES + ["ic"]:
        (out_dir / f"ADIC_TPP_{role}.html").write_text(html.replace('data-default-role="strategy"',
                                                                    f'data-default-role="{role}"'), encoding="utf-8")
    say(f"wrote {main_file} ({main_file.stat().st_size / 1e6:.2f} MB) and one copy per group")


if __name__ == "__main__":
    main()
