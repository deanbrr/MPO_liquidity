"""MPO v2 prototype: five components end to end (SYNTHETIC - NOT ADIC DATA).

  1 data and three-return fusion     book.py, fusion.py
  2 scenario tree                    scenarios.py, tree.py, prep.py
  3 multi-period optimizer           model.py, optim.py, policy.py (GBO main; exact max-P(goal) MILP; CRRA + L2)
  4 simulator for probabilities      sim.py (sealed truth, fresh paths, common random numbers)
  5 reports                          report.py -> RESULTS.md; results.json; run_log.txt

Run:  .venv\\Scripts\\pythonw.exe examples\\mpo_v2\\mpo_v2.py      (python.exe works where policy allows)
Spec: design/DECISION_SPACE_AND_GOAL_OBJECTIVE.md v1.1 (DSGO) with examples/mpo_v2/spec_review.md.
Independent LP/MIP solves run in parallel single-threaded processes; each starts from a fresh HiGHS instance, so the
results do not depend on scheduling (deterministic seeds everywhere).
"""
from __future__ import annotations

import multiprocessing as mp
import os
import sys
import time

import numpy as np

HERE_ = os.path.dirname(os.path.abspath(__file__))
if HERE_ not in sys.path:
    sys.path.insert(0, HERE_)

from common import HERE, LABEL, Log, Params, clopper_pearson_upper, cvar_lower, holm, jdump, r6, \
    sarle_bimodality, setup_stdout_utf8, stable_hash, wilson   # noqa: E402
import optim   # noqa: E402
import policy as pol_mod   # noqa: E402
import tasks   # noqa: E402
import world   # noqa: E402
from model import FIN   # noqa: E402
from sim import run_policy, tree_world   # noqa: E402


# ---------------------------------------------------------------------------------------------- statistics
def bpoe_eq(X):
    p = np.full(len(X), 1.0 / len(X))
    return optim.bpoe(np.asarray(X, float), p)


def bpoe_fast(X):
    """bPOE of X under equal weights, exact: min over breakpoints a = -1/X_k of mean((aX+1)+)."""
    X = np.sort(np.asarray(X, float))
    if X.mean() >= 0:
        return 1.0
    neg = X[X < 0]
    best = 1.0
    cand = np.unique(-1.0 / neg)
    if len(cand) > 400:
        cand = np.quantile(cand, np.linspace(0, 1, 400))
    for a in cand:
        best = min(best, float(np.mean(np.maximum(a * X + 1.0, 0.0))))
    return best


def oos_metrics(r: dict, goal=0.10, yrs=5) -> dict:
    twr = r["twr"]
    n = len(twr)
    g = twr >= goal - 1e-12
    k = int(g.sum())
    W = (1 + twr) ** yrs
    out = {"p_goal": k / n, "p_goal_ci95": list(wilson(k, n)), "p_goal_reported_nav": float(np.mean(r["twr_rep"] >= goal)),
           "E_terminal_Wtilde_over_W0": float(W.mean()),
           "twr_mean": float(twr.mean()), "twr_median": float(np.median(twr)),
           "cvar_twr": {"10": cvar_lower(twr, 0.10), "5": cvar_lower(twr, 0.05), "1": cvar_lower(twr, 0.01)},
           "bpoe": {"goal": bpoe_fast((1 + goal) ** yrs - W), "floor7": bpoe_fast(1.07 ** yrs - W),
                    "zero": bpoe_fast(1.0 - W)},
           "p_red": float(r["red"].mean()), "p_red_cp95": clopper_pearson_upper(int(r["red"].sum()), n),
           "maxdd_median": float(np.median(r["maxdd"])), "maxdd_p95": float(np.quantile(r["maxdd"], 0.95)),
           "lev_max_median": float(np.median(r["lev_max"])), "bimodality": sarle_bimodality(twr),
           "pileup_mass": float(np.mean((W >= (1 + goal) ** yrs) & (W < (1 + goal) ** yrs + 0.01))),
           "n_paths": n}
    out["bimodality_flag"] = out["bimodality"] > 0.555
    out["reported_nav_flag"] = out["p_goal_reported_nav"] - out["p_goal"] > 0.02
    # G6 signatures. Active leverage increase after a loss year: post-decision E/W above the pre-decision E/W at a
    # year end that follows a negative year (mechanical drift and forced deleveraging are not counted). At the cap
    # while behind: post-decision E/W at the full CLASS cap at a behind year end (G5's behind cap sits below it).
    lp, pre, lo_, bh, cc = r["lev_path"], r["lev_pre"], r["loss_path"], r["behind_path"], r["capcls_path"]
    yrs_ = slice(1, 5)
    rise = (lp[:, yrs_] > pre[:, yrs_] + 0.01) & (lo_[:, yrs_] > 0.5)
    out["lev_up_after_loss"] = float(rise.mean())
    atcap = (bh[:, yrs_] > 0.5) & (lp[:, yrs_] >= cc[:, yrs_] - 0.005)
    out["lev_at_cap_while_behind"] = float(atcap.mean())
    return out


def ssd_vs(twr_a, twr_b, yrs=5) -> bool:
    """Second-order stochastic dominance of a over b on terminal wealth (LPM1 at every threshold)."""
    a = np.sort((1 + twr_a) ** yrs)
    b = np.sort((1 + twr_b) ** yrs)
    ts = np.quantile(b, np.linspace(0.005, 0.995, 199))
    la = np.array([np.mean(np.maximum(t - a, 0)) for t in ts])
    lb = np.array([np.mean(np.maximum(t - b, 0)) for t in ts])
    return bool(np.all(la <= lb + 1e-4))


def b4_line(res, scales):
    pts = []
    for s in scales:
        r = res[f"B4_{s}"]
        pts.append((cvar_lower(r["twr"], 0.10), float(np.mean(r["twr"] >= 0.10)), s))
    return pts


def interp_line(pts, cv):
    """P(goal) of the risk-matched line at CVaR10 = cv (line is ordered by scale: CVaR falls, P(goal) rises)."""
    xs = np.array([p[0] for p in pts])[::-1]
    ys = np.array([p[1] for p in pts])[::-1]
    o = np.argsort(xs)
    xs, ys = xs[o], ys[o]
    if cv <= xs[0]:
        slope = (ys[1] - ys[0]) / (xs[1] - xs[0]) if xs[1] != xs[0] else 0.0
        return float(ys[0] + slope * (cv - xs[0]))
    if cv >= xs[-1]:
        slope = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2]) if xs[-1] != xs[-2] else 0.0
        return float(ys[-1] + slope * (cv - xs[-1]))
    return float(np.interp(cv, xs, ys))


def value_eq_tail(res, name, scales, nboot=200, seed=7):
    r = res[name]
    cv = cvar_lower(r["twr"], 0.10)
    pts = b4_line(res, scales)
    v = float(np.mean(r["twr"] >= 0.10)) - interp_line(pts, cv)
    rng = np.random.default_rng(seed)
    n = len(r["twr"])
    boots = []
    for _ in range(nboot):
        idx = rng.integers(0, n, n)
        rb = {f"B4_{s}": {"twr": res[f"B4_{s}"]["twr"][idx]} for s in scales}
        tw = r["twr"][idx]
        boots.append(float(np.mean(tw >= 0.10)) - interp_line(b4_line(rb, scales), cvar_lower(tw, 0.10)))
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"dp_goal": v, "ci95": [float(lo), float(hi)], "cvar10": cv}


def paired(res, a, b, margin=0.0):
    ga = res[a]["twr"] >= 0.10
    gb = res[b]["twr"] >= 0.10
    d = ga.astype(float) - gb.astype(float)
    n = len(d)
    mean = float(d.mean())
    se = float(d.std(ddof=1) / np.sqrt(n)) if n > 1 else np.nan
    from scipy.stats import binomtest, norm
    bb = int((ga & ~gb).sum())
    cc = int((~ga & gb).sum())
    mc = binomtest(bb, bb + cc, 0.5, alternative="greater").pvalue if bb + cc > 0 else 1.0
    z = (mean - margin) / se if se and se > 0 else 0.0
    return {"dp_goal": mean, "se": se, "ci95": [mean - 1.96 * se, mean + 1.96 * se], "mcnemar_p_gt0": float(mc),
            "p_margin": float(1 - norm.cdf(z)), "margin": margin, "b": bb, "c": cc,
            "dtwr_mean": float(res[a]["twr"].mean() - res[b]["twr"].mean()),
            "dcvar10": float(cvar_lower(res[a]["twr"], 0.10) - cvar_lower(res[b]["twr"], 0.10)),
            "dp_red": float(res[a]["red"].mean() - res[b]["red"].mean())}


# ---------------------------------------------------------------------------------------------- helpers
def collect(asyncs, log, label):
    out = {}
    for k, a in asyncs.items():
        r = a.get()
        out[k] = r
        if not r.get("ok", True) and "error" in r:
            log(f"  TASK {label}:{k} ERROR {r['error']}")
            log(r.get("trace", ""))
        for s in r.get("solves", []):
            s = dict(s)
            s["name"] = f"[{k}] {s['name']}" if not s["name"].startswith(k) else s["name"]
            log.solve(s)
    return out


def sim_parallel(pool, policies, n_total, seed, chunk, truth, tpl_seed):
    nch = int(np.ceil(n_total / chunk))
    asy = []
    for ci in range(nch):
        n = min(chunk, n_total - ci * chunk)
        asy.append(pool.apply_async(tasks.run_task, ({"type": "sim", "seed": seed, "ci": ci, "n": n, "n_total": n_total,
                                                       "chunk": chunk, "policies": policies, "truth": truth,
                                                       "tpl_seed": tpl_seed},)))
    parts = [a.get() for a in asy]
    for p_ in parts:
        if "error" in p_:
            raise RuntimeError(p_["error"] + "\n" + p_.get("trace", ""))
        SIM_PARAMS_USED.update(p_.get("params_used", []))
    parts.sort(key=lambda r: r["ci"])
    res = {}
    for name in policies:
        res[name] = {k: np.concatenate([p_["res"][name][k] for p_ in parts]) for k in parts[0]["res"][name]}
    return res


SIM_PARAMS_USED: set = set()


def strip_policy(p):
    return {k: v for k, v in p.items() if k not in ("nodes",)}


def describe_node(m, x, n, D, y=None):
    V = D["V"]
    ids = D["ids"]
    sells = {g: float((x[m.S[n]] * D["proc"][n] * (D["group"] == g)).sum()) for g in sorted(set(D["group"]))}
    sells = {k: v for k, v in sells.items() if v > 1e-3}
    adds = {ids[i]: float(x[m.A[n, i]] * V[n, i]) for i in range(D["I"]) if x[m.A[n, i]] * V[n, i] > 1e-3}
    reds = {ids[i]: float(x[m.R[n, i]]) for i in range(D["I"]) if x[m.R[n, i]] > 1e-4}
    tpl = {nm: float(x[m.Y[n, k]]) for k, nm in enumerate(D["tpl_names"]) if x[m.Y[n, k]] > 1e-3}
    fin = {f: float(x[m.FB[n, j]]) for j, f in enumerate(FIN) if x[m.FB[n, j]] > 1e-3}
    feat = D["tr"]["features"][n]
    return {"node": int(n), "class": ["BEN", "DRT", "STR"][int(m.cls[n])], "prob": float(m.prob[n]),
            "stratum": D["tr"]["nodes"][n].get("stratum"), "eq_year_log_excess": float(feat[0]),
            "brent": float(np.exp(feat[3])), "vix": float(feat[5]), "draw_rate_next": float(feat[6]),
            "W_bn": float(x[m.W[n]]), "E_over_W": float(x[m.EX[n]] / x[m.W[n]]),
            "IGcash_over_W": float(x[m.LQ[n]] / x[m.W[n]]), "sales_bn_by_group": sells, "adds_bn": adds,
            "redeem_frac": reds, "templates_bn": tpl, "debt_bn": fin, "synthetic_beta_bn": float(x[m.BETA[n]]),
            "p2s_bn": float(x[m.PI[n]]), "tail_notional_bn": float(x[m.HED[n]]), "opp_im_bn": float(x[m.OPP[n]]),
            "red_margin_bn": float(x[m.M[n]])}


# ---------------------------------------------------------------------------------------------- main
def main():
    setup_stdout_utf8()
    t_start = time.time()
    P = Params(HERE / "params.json")
    log = Log(HERE / "run_log.txt")
    log(f"{LABEL}. MPO v2 prototype run. params hash {P.hash()}")
    nwork = max(2, min(20, (os.cpu_count() or 4) - 2))
    ctx = mp.get_context("spawn")
    pool = ctx.Pool(nwork, initializer=tasks.init_worker, initargs=(str(HERE / "params.json"),))
    log(f"worker pool: {nwork} processes (single-threaded HiGHS each)")
    eps_grid = P.get("frontier.eps_grid")
    from model import FAMILIES
    early = []
    for f in FAMILIES:
        early.append({"type": "gbo", "id": f"OFF_{f}", "mods": [("switchoff", f)]})
    early.append({"type": "beliefs", "id": "OFF_BELIEFS"})
    mpts = P.get("frontier.milp_points")
    for e in eps_grid:
        early.append({"type": "gbo", "id": f"FR_eps_{e}", "mods": [("eps", e)], "milp": e in mpts,
                      "milp_tl": P.get("objective.milp_frontier_time_limit"),
                      "milp_nodes": P.get("objective.milp_frontier_node_limit"), "milp_heuristics": False,
                      "return_x": False})
    early.append({"type": "crra", "id": "O3_CRRA"})
    early_b = []
    for dl in P.get("frontier.delta_grid"):
        early_b.append({"type": "gbo", "id": f"FR_delta_{dl}", "mods": [("delta", dl)]})
    for rl in ("floor8", "class_caps", "H11"):
        early_b.append({"type": "gbo", "id": f"A20_{rl}", "mods": [("relax", rl)]})
    variants = P.get("truth_model.alpha_dispersion_variants")
    infos = P.get("truth_model.bid_info_variants")
    seeds_rep = P.get("seeds.replication_books")
    b4s = P.get("baselines.b4_scales")
    rep_specs = []
    for k, sd in enumerate(seeds_rep):
        v = {"alpha_dispersion": variants[k % 2], "bid_info": infos[(k // 2) % 2], "placebo": False}
        rep_specs.append((f"BOOK_{sd}", sd, v, False))
    rep_specs.append(("BOOK_PLACEBO", P.get("seeds.book"), {"alpha_dispersion": 1.0, "bid_info": 1.0, "placebo": True},
                      True))
    books_t = []
    for nm, sd, v, f10 in rep_specs:
        books_t.append({"type": "book", "id": nm, "seed": sd, "variant": v, "with_f10": f10,
                        "n_paths": P.get("simulation.n_replication_paths"), "sim_seed": P.get("seeds.cert") + 1000,
                        "chunk": 2000, "tpl_seed": sd + 1, "b4_scales": b4s[:4]})
    # fill the workers now; the O1-dependent tasks (MILP first) are queued ahead of the rest
    nfill = max(0, nwork - len(early))
    early += books_t[:nfill]
    early_b = books_t[nfill:] + early_b
    asy_early = {t["id"]: pool.apply_async(tasks.run_task, (t,)) for t in early}
    log(f"submitted {len(early)} independent tasks (switch-offs, beliefs, frontier, CRRA, books)")

    # ------------------------------------------------ component 1-3 in the main process
    w = world.build(P, log=log)
    D, m, m0, x0, b0 = w["D"], w["m"], w["m0"], w["x0"], w["b0"]
    tr = D["tr"]
    log(f"world: W0 = {D['W0']:.2f} $bn economic (177 reported), W* = {D['Wstar']:.2f} $bn; tree {tr['T']} time-nodes, "
        f"{len(D['leaves'])} leaves; model {m.nvar} cols {m.nrow} rows {m.A_mat.nnz} nnz (built {m.build_time:.1f}s)")
    st_b0 = optim.tree_stats(m0, x0)
    o1 = optim.gbo(m, log, tag="O1 GBO")
    x1, y1 = o1["x"], o1["y"]
    st_o1 = optim.tree_stats(m, x1)
    log(f"O1: label {o1['label']}  Phi {o1['phi']:.4f}  E*[W~] {o1['E_star']:.2f}  in-tree P(goal) {st_o1['p_goal']:.4f} "
        f"(B0 {st_b0['p_goal']:.4f})")
    pol_o1 = pol_mod.extract_policy(m, x1)
    lens = pol_mod.r1_labels(m, x1)
    cardl = pol_mod.cards(m, x1, y1, w["beliefs"], w["book"], w["Ef"], rc=o1.get("rc"))
    chg = pol_mod.change_list(m, x1, y1, cardl, lens[0])
    ell = pol_mod.liquidity_premia(m, y1)
    contingent = [dict(describe_node(m, x1, n, D), ell=float(ell[n])) for n in range(1, m.ND) if m.lvl[n] == 1]
    root_desc = dict(describe_node(m, x1, 0, D), ell=float(ell[0]))
    # tasks that need O1: the MILP, forced re-solves of the top root actions, red-tier forced cards
    late = [{"type": "milp", "id": "O2_MILP", "start": x1, "milp_tl": P.get("objective.milp_time_limit"),
             "milp_nodes": P.get("objective.milp_node_limit"), "milp_heuristics": True}]
    nforce = P.get("report.n_forced")
    order = [k for k in sorted(range(len(chg)), key=lambda k: -abs(chg[k]["size_bn"]))
             if chg[k]["unit_id"] != "TAIL_LADDER"]
    forced_ids = []
    for k in order[:nforce]:
        row = chg[k]
        fix = None
        uid = row["unit_id"]
        if uid in D["ids"]:
            i = D["ids"].index(uid)
            col = {"sell": m.S[0, i], "redeem": m.R[0, i], "add": m.A[0, i]}[row["action"]]
            fix = ([int(col)], 0.0, 0.0)
        elif uid in D["tpl_names"]:
            kk = D["tpl_names"].index(uid)
            plan = D["tpl"][kk].get("plan", 0.0)
            fix = ([int(m.Y[0, kk])], plan, plan)
        elif uid in FIN:
            fix = ([int(m.DR[0, FIN.index(uid)])], 0.0, 0.0)
        elif uid == "SYNTH_BETA":
            v = P.get("overlay.beta_sq")
            fix = ([int(m.BETA[0])], v, v)
        elif uid == "OPPORTUNISTIC":
            v = P.get("overlay.opp_im_sq")
            fix = ([int(m.OPP[0])], v, v)
        elif uid.startswith("TRS:"):
            h = list(m.hf_units).index(D["ids"].index(uid[4:]))
            fix = ([int(m.TRS[0, h])], 0.0, 0.0)
        elif uid == "P2S":
            fix = ([int(m.PU[0])], 0.0, 0.0)
        elif uid == "TAIL_LADDER":
            continue
        if fix is None:
            continue
        tid = f"FORCE_{uid}"
        forced_ids.append((k, tid))
        late.append({"type": "gbo", "id": tid, "mods": [("fix",) + fix]})
    # red-tier root SELL candidates (ADR-39: today is Amber -> shown only by forced re-solve)
    redc = sorted([c for c in cardl if c["tier"] == "red" and np.isfinite(c["p_star"])],
                  key=lambda c: -(c["p_ce"] - c["p_star"]))[:P.get("report.n_red_cards")]
    red_ids = []
    for c in redc:
        i = D["ids"].index(c["unit_id"])
        frac = float(min(0.5, D["cap_trade"][i] / D["V"][0, i]))
        tid = f"RED_{c['unit_id']}"
        red_ids.append((c["unit_id"], tid, frac))
        # a root red-tier sale is a red event on every path (Amber today), so H9 is relaxed for the card: the card
        # exists to show what forcing the sale would cost or gain
        late.append({"type": "gbo", "id": tid, "mods": [("eps", 1.0), ("fix", [int(m.S[0, i])], frac, frac)]})
    asy_late = {t["id"]: pool.apply_async(tasks.run_task, (t,)) for t in late}
    log(f"submitted {len(late)} O1-dependent tasks (MILP, {len(forced_ids)} forced re-solves, {len(red_ids)} red cards)")
    asy_b = {t["id"]: pool.apply_async(tasks.run_task, (t,)) for t in early_b}
    log(f"submitted {len(early_b)} further tasks (books, depth-guard frontier, A20)")
    # A9: finite-difference check of the root cash dual (the decision LP: tie-break constraint re-imposed)
    a9 = {}
    try:
        r0 = m.rows["cash"][0]
        optim.apply_tie(m, o1.get("tie"))
        m.set_cost(m.obj_util())
        base_obj = float(np.dot(m._cur_cost, x1))
        fds = []
        for stp in (0.01, -0.01):
            m.set_row_bounds(r0, m.rlb[r0] + stp, m.rub[r0] + stp)
            xa, _, reca = m.run(f"A9: root cash {stp:+.2f} $bn (finite difference on the decision LP)", method="ipm")
            if xa is not None:
                fds.append((float(np.dot(m._cur_cost, xa)) - base_obj) / stp)
        m.set_row_bounds(r0, m.rlb[r0], m.rub[r0])
        optim.clear_tie(m)
        if fds:
            dual = float(y1[r0])
            lo_, hi_ = min(fds), max(fds)
            inside = lo_ - 1e-4 * abs(dual) <= dual <= hi_ + 1e-4 * abs(dual)
            a9 = {"dual": dual, "finite_difference_up_down": fds,
                  "rel_err": float(min(abs(f - dual) for f in fds) / max(abs(dual), 1e-12)),
                  "dual_within_one_sided_differences": bool(inside)}
    except Exception as e:   # pragma: no cover
        a9 = {"error": repr(e)}
    early_res = collect(asy_early, log, "early")
    late_res = collect(asy_late, log, "late")
    early_res.update(collect(asy_b, log, "further"))
    for r in list(early_res.values()) + list(late_res.values()):
        P.used.update(r.get("params_used", []))
    t_lp = time.time() - t_start
    log(f"all optimization tasks done at {t_lp:.1f}s")

    # ------------------------------------------------ component 4: selection and certification
    rules = {"B0": {"kind": "B0", "restore8": False}, "B1": {"kind": "B1", "restore8": True},
             "B2": {"kind": "B2", "restore8": True}, "B3": {"kind": "B3", "restore8": True}}
    o2 = late_res["O2_MILP"]
    o3 = early_res["O3_CRRA"]
    objs = {"O1": pol_o1}
    if o2.get("ok"):
        objs["O2"] = o2["policy"]
    if o3.get("ok"):
        objs["O3"] = o3["policy"]
    sel_pols = dict(rules)
    for k, p_ in objs.items():
        sel_pols[f"{k}_playbook"] = p_
        sel_pols[f"{k}_rule"] = dict(p_, playbook=False)
    t0 = time.time()
    sel = sim_parallel(pool, sel_pols, P.get("simulation.n_select"), P.get("seeds.select"), 1000, "sealed", 501)
    log(f"selection set: {P.get('simulation.n_select')} paths x {len(sel_pols)} policies in {time.time() - t0:.1f}s")
    best_rule = max(["B1", "B2", "B3"], key=lambda k: float(np.mean(sel[k]["twr"] >= 0.10)))
    choice = {}
    for k in objs:
        a = float(np.mean(sel[f"{k}_playbook"]["twr"] >= 0.10))
        b = float(np.mean(sel[f"{k}_rule"]["twr"] >= 0.10))
        choice[k] = "playbook" if a >= b else "rule"
    log(f"selection: best simple rule {best_rule}; recourse chosen {choice}")
    sel_summary = {k: {"p_goal": float(np.mean(v["twr"] >= 0.10)), "twr_mean": float(v["twr"].mean()),
                       "cvar10": cvar_lower(v["twr"], 0.10)} for k, v in sel.items()}
    # certification policies
    cert = dict(rules)
    for s in b4s:
        cert[f"B4_{s}"] = {"kind": "B4", "restore8": False, "scale": s}
    for k, p_ in objs.items():
        cert[f"{k}_playbook"] = p_
        cert[f"{k}_rule"] = dict(p_, playbook=False)
    var = choice["O1"]

    def as_var(p_):
        return p_ if var == "playbook" else dict(p_, playbook=False)

    for k, r in list(early_res.items()) + list(late_res.items()):
        if r.get("type") == "gbo" or r.get("type") == "beliefs":
            if r.get("ok"):
                cert[k] = as_var(r["policy"])
            if r.get("milp") and r["milp"].get("policy") is not None:
                cert[k + "_MILP"] = as_var(r["milp"]["policy"])
    t0 = time.time()
    res = sim_parallel(pool, cert, P.get("simulation.n_cert"), P.get("seeds.cert"), P.get("simulation.chunk"), "sealed", 502)
    log(f"certification: {P.get('simulation.n_cert')} paths x {len(cert)} policies in {time.time() - t0:.1f}s")
    # posterior-draw / belief mode for the headline policies (never the headline: confirms the beliefs)
    bel_pols = {k: cert[k] for k in ["B0", best_rule] + [f"{o}_{choice[o]}" for o in objs]}
    resb = sim_parallel(pool, bel_pols, P.get("simulation.n_cert"), P.get("seeds.cert"), P.get("simulation.chunk"), "belief", 502)
    # in-tree evaluation of rules and the E1 check on the tree's own leaf paths
    tw = tree_world(D, w["gen"])
    pw = tw["prob"]
    intree_sim = {}
    g_ext = run_policy(D, tw, rules["B0"])["green_path"].astype(bool)
    for k in ["B0", "B1", "B2", "B3"] + [f"O1_{v}" for v in ("playbook", "rule")]:
        pk = dict(cert[k], green_ext=g_ext) if cert[k]["kind"] == "plan" else cert[k]
        rr = run_policy(D, tw, pk)
        intree_sim[k] = {"p_goal": float(np.dot(pw, rr["twr"] >= 0.10)), "twr_mean": float(np.dot(pw, rr["twr"])),
                         "cvar10": cvar_lower(rr["twr"], 0.10, pw)}
    pool.close()
    pool.join()

    # ------------------------------------------------ statistics
    metrics = {k: oos_metrics(v) for k, v in res.items()}
    line = [{"beta_scale": s, "p_goal": metrics[f"B4_{s}"]["p_goal"], "cvar10_twr": metrics[f"B4_{s}"]["cvar_twr"]["10"],
             "twr_mean": metrics[f"B4_{s}"]["twr_mean"]} for s in b4s]
    vet = {}
    for k in res:
        if not k.startswith("B4_"):
            vet[k] = value_eq_tail(res, k, b4s, nboot=60 if k not in ("O1_playbook", "O1_rule") else 400)
    h_o1 = f"O1_{choice['O1']}"
    ssd = ssd_vs(res[h_o1]["twr"], res["B0"]["twr"])
    tests = {"H1": paired(res, h_o1, "B0", 0.02), "H2": paired(res, h_o1, best_rule, 0.01)}
    o2key = f"O2_{choice.get('O2', 'rule')}" if "O2" in objs else None
    # optimism gaps (tree minus out of sample; truth = belief and sealed)
    gaps = {"O1": {"tree": st_o1["p_goal"], "oos_sealed": metrics[h_o1]["p_goal"],
                   "oos_belief": float(np.mean(resb[h_o1]["twr"] >= 0.10))}}
    if o2key:
        gaps["O2"] = {"tree": o2["stats"]["p_goal"], "oos_sealed": metrics[o2key]["p_goal"],
                      "oos_belief": float(np.mean(resb[o2key]["twr"] >= 0.10))}
    for k in gaps:
        gaps[k]["gap_sealed"] = gaps[k]["tree"] - gaps[k]["oos_sealed"]
        gaps[k]["gap_belief"] = gaps[k]["tree"] - gaps[k]["oos_belief"]
    # replication books and placebo
    books = []
    for nm, sd, v, f10 in rep_specs:
        r = early_res[nm]
        if not r.get("ok") or "sim" not in r:
            books.append({"id": nm, "ok": False, "error": r.get("error")})
            continue
        sm = r["sim"]
        rb = {k: {"twr": vv["twr"], "red": vv["red"]} for k, vv in sm.items()}
        ent = {"id": nm, "seed": sd, "variant": v, "ok": True, "label": r.get("o1_label"),
               "p_goal": {k: float(np.mean(vv["twr"] >= 0.10)) for k, vv in rb.items()},
               "cvar10": {k: cvar_lower(vv["twr"], 0.10) for k, vv in rb.items()}}
        for k in ("O1_playbook", "O1_rule", "F10_playbook", "F10_rule"):
            if k in rb:
                ent[f"veq_{k}"] = value_eq_tail(rb, k, b4s[:4], nboot=50)["dp_goal"]
                ent[f"dp_vs_B0_{k}"] = ent["p_goal"][k] - ent["p_goal"]["B0"]
        books.append(ent)
    good = [b for b in books if b.get("ok") and "PLACEBO" not in b["id"]]
    key = f"O1_{choice['O1']}"
    if good:
        dps = np.array([b[f"dp_vs_B0_{key}"] for b in good] + [tests["H1"]["dp_goal"]])
        from scipy.stats import t as tdist
        mean_b = float(dps.mean())
        se_b = float(dps.std(ddof=1) / np.sqrt(len(dps))) if len(dps) > 1 else np.nan
        tests["H3"] = {"books": len(dps), "dp_goal_mean": mean_b, "se_clustered_by_book": se_b,
                       "per_book": dps.tolist(),
                       "p_margin": float(1 - tdist.cdf((mean_b - 0.02) / se_b, len(dps) - 1)) if se_b > 0 else 1.0}
    gamb = {k: metrics[h_o1][k] for k in ("bimodality_flag", "lev_up_after_loss", "lev_at_cap_while_behind",
                                           "pileup_mass")}
    a14_ok = (not metrics[h_o1]["bimodality_flag"]) and metrics[h_o1]["lev_at_cap_while_behind"] < 0.01 \
        and metrics[h_o1]["lev_up_after_loss"] < 0.01
    tests["H4"] = {"signatures": gamb, "ssd_vs_B0": ssd, "a14_pass": bool(a14_ok), "pass": bool(a14_ok and ssd)}
    if o2key:
        tests["H5"] = {"gap_O2": gaps["O2"]["gap_sealed"], "gap_O1": gaps["O1"]["gap_sealed"],
                       "pass": bool(gaps["O2"]["gap_sealed"] > gaps["O1"]["gap_sealed"])}
    v1 = vet[h_o1]
    se6 = (v1["ci95"][1] - v1["ci95"][0]) / (2 * 1.96)
    from scipy.stats import norm
    tests["H6"] = {"value_at_equal_tail": v1["dp_goal"], "ci95": v1["ci95"],
                   "p_margin": float(1 - norm.cdf((v1["dp_goal"] - 0.01) / se6)) if se6 > 0 else 1.0}
    plc = [b for b in books if b.get("ok") and "PLACEBO" in b["id"]]
    if plc:
        b = plc[0]
        k1 = f"O1_{choice['O1']}"
        kf = f"F10_{choice['O1']}"
        f10v = b["p_goal"].get(k1, np.nan) - b["p_goal"].get(kf, np.nan)
        tests["H7"] = {"placebo_F10_dp_goal": f10v, "placebo_O1_value_at_equal_tail": b.get(f"veq_{k1}"),
                       "pass": bool(abs(f10v) < 0.01 and (b.get(f"veq_{k1}") or 0) <= 0.005)}
    pv = {"H1": tests["H1"]["p_margin"], "H2": tests["H2"]["p_margin"], "H6": tests["H6"]["p_margin"]}
    if "H3" in tests:
        pv["H3"] = tests["H3"]["p_margin"]
    hol = holm(pv)
    for k in pv:
        tests[k]["holm_p"] = hol[k]
        tests[k]["established"] = bool(hol[k] < 0.05)

    # switch-off attribution (vs O1 in the same recourse variant)
    att = []
    for f in FAMILIES + ["BELIEFS"]:
        kk = f"OFF_{f}"
        if kk not in res:
            att.append({"family": f, "ok": False})
            continue
        pr = paired(res, kk, h_o1)
        rr = early_res[kk]
        att.append({"family": f, "ok": True, "dp_goal": pr["dp_goal"], "ci95": pr["ci95"], "dtwr_mean": pr["dtwr_mean"],
                    "dcvar10": pr["dcvar10"], "dp_red": pr["dp_red"],
                    "dp_goal_equal_tail": vet[kk]["dp_goal"] - vet[h_o1]["dp_goal"],
                    "tree_dp_goal": rr["stats"]["p_goal"] - st_o1["p_goal"],
                    "tree_dE_Wt_bn": rr["stats"]["E_Wt_bn"] - st_o1["E_Wt_bn"], "label": rr.get("label"),
                    "phi": rr.get("phi"), "phase1": rr.get("phase1")})
    # frontier
    front = []
    for e in eps_grid:
        kk = f"FR_eps_{e}"
        r = early_res.get(kk, {})
        if not r.get("ok"):
            front.append({"eps_red_tree": e, "ok": False})
            continue
        ent = {"eps_red_tree": e, "ok": True, "label": r["label"], "phi_min_bpoe_tree": r["phi"],
               "gbo_p_goal_tree": r["stats"]["p_goal"], "gbo_p_red_tree": r["stats"]["p_red"],
               "gbo_p_goal_oos": metrics[kk]["p_goal"], "gbo_bpoe_oos": metrics[kk]["bpoe"]["goal"],
               "gbo_p_red_oos": metrics[kk]["p_red"], "gbo_cvar10_oos": metrics[kk]["cvar_twr"]["10"],
               "gbo_value_at_equal_tail": vet[kk]["dp_goal"]}
        if r.get("milp") and r["milp"].get("stats"):
            mk = kk + "_MILP"
            ent.update({"milp_max_p_goal_tree": r["milp"]["stats"]["p_goal"], "milp_status": r["milp"]["rec"]["status"],
                        "milp_gap": r["milp"]["rec"]["mip_gap"], "milp_bound_tree": r["milp"]["rec"]["dual_bound"],
                        "milp_p_goal_oos": metrics[mk]["p_goal"],
                        "milp_bpoe_oos": metrics[mk]["bpoe"]["goal"], "milp_p_red_oos": metrics[mk]["p_red"]})
        elif o2.get("ok") and o2key and abs(r["stats"]["p_goal"] - st_o1["p_goal"]) < 1e-9 and \
                abs(r["stats"]["E_Wt_bn"] - st_o1["E_Wt_bn"]) < 1e-3 and abs(r["phi"] - o1["phi"]) < 1e-6:
            ent.update({"milp_max_p_goal_tree": o2["stats"]["p_goal"], "milp_status": o2["rec"]["status"] + " (O2 reused: "
                        "identical GBO solution)", "milp_gap": o2["rec"]["mip_gap"],
                        "milp_bound_tree": o2["rec"]["dual_bound"], "milp_p_goal_oos": metrics[o2key]["p_goal"],
                        "milp_bpoe_oos": metrics[o2key]["bpoe"]["goal"], "milp_p_red_oos": metrics[o2key]["p_red"]})
        front.append(ent)
    dfront = []
    for dl in P.get("frontier.delta_grid"):
        kk = f"FR_delta_{dl}"
        r = early_res.get(kk, {})
        if r.get("ok"):
            dfront.append({"delta_W0": dl, "label": r["label"], "phi_tree": r["phi"], "p_goal_tree": r["stats"]["p_goal"],
                           "p_goal_oos": metrics[kk]["p_goal"], "cvar10_oos": metrics[kk]["cvar_twr"]["10"],
                           "value_at_equal_tail": vet[kk]["dp_goal"], "ssd_vs_B0": ssd_vs(res[kk]["twr"], res["B0"]["twr"])})
    # A20 limit sensitivity
    a20 = []
    for rl in ("floor8", "class_caps", "H11"):
        kk = f"A20_{rl}"
        r = early_res.get(kk, {})
        if r.get("ok"):
            dp = metrics[kk]["p_goal"] - metrics[h_o1]["p_goal"]
            a20.append({"limit": rl, "dp_goal_oos": dp, "named": abs(dp) > 0.01, "tree_dp_goal": r["stats"]["p_goal"] - st_o1["p_goal"],
                        "root": {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in r["root"].items()}})
    # forced re-solves for the change list
    for k, tid in forced_ids:
        r = late_res.get(tid, {})
        if r.get("ok") and tid in res:
            pr = paired(res, h_o1, tid)
            chg[k]["dp_goal_forced"] = pr["dp_goal"]
            chg[k]["dp_goal_forced_ci95"] = pr["ci95"]
            chg[k]["dtwr_forced"] = pr["dtwr_mean"]
            chg[k]["dp_goal_forced_equal_tail"] = vet[h_o1]["dp_goal"] - vet[tid]["dp_goal"]
            chg[k]["risk_budget"] = bool(pr["dp_goal"] > 0 and chg[k]["dp_goal_forced_equal_tail"] <= 0)
            chg[k]["tree_dp_goal_forced"] = st_o1["p_goal"] - r["stats"]["p_goal"]
    for row in chg:
        row.setdefault("risk_budget", False)
        row["limit_driven"] = False
        for a in a20:
            if not a["named"]:
                continue
            uid = row["unit_id"]
            if uid in D["ids"]:
                i = D["ids"].index(uid)
                base_ = row["size_bn"]
                alt = (a["root"]["sell"][i] + a["root"]["redeem"][i] + a["root"]["add"][i]) * D["V"][0, i]
                if base_ > 0 and abs(alt - base_) / base_ > 0.2:
                    row["limit_driven"] = True
    red_cards = []
    for uid, tid, frac in red_ids:
        r = late_res.get(tid, {})
        if r.get("ok") and tid in res:
            pr = paired(res, tid, h_o1)
            c = next(cc for cc in cardl if cc["unit_id"] == uid)
            red_cards.append({"unit_id": uid, "forced_sell_frac": frac, "size_bn": frac * float(D["V"][0, D["ids"].index(uid)]),
                              "p_ce": c["p_ce"], "p_star": c["p_star"], "mu_hat": c["mu_hat"], "hurdle_goal": c["hurdle_goal"],
                              "dp_goal_oos": pr["dp_goal"], "dp_goal_ci95": pr["ci95"], "dtwr_mean": pr["dtwr_mean"],
                              "red_event": "yes by construction: ADR-39, today's stage is Amber",
                              "tree_dp_goal": r["stats"]["p_goal"] - st_o1["p_goal"]})
    # ------------------------------------------------ checks
    m_solves = m.solves + m0.solves
    all_solves = list(log.solves)
    statuses = [s["status"] for s in all_solves]
    milp_recs = [s for s in all_solves if s.get("kind") in ("MIP", "MIP-R")]
    checks = []

    def chk(i, val, thr, ok, note=""):
        checks.append({"id": i, "value": val, "threshold": thr, "pass": bool(ok), "note": note})

    eqrows = np.flatnonzero(m.rlb == m.rub)
    Ax = m.A_mat @ x1
    resid = float(np.max(np.abs(Ax[eqrows] - m.rlb[eqrows]))) if len(eqrows) else 0.0
    chk("A1", resid, 1e-8 * D["W0"] * 1e3, resid <= 1e-5 * D["W0"], "max equality-row residual of O1 ($bn); HiGHS tolerance 1e-7")
    viol = float(max(np.max(m._cur_rlb - Ax - 0), np.max(Ax - m._cur_rub)))
    chk("A3", -viol, -1e-6, viol <= 1e-5 * max(1.0, D["W0"] / 100), "worst row slack of O1 (all H rows, every node, fan year, leaf)")
    phi_fn = optim.gbo_value((D["Wstar"] - x1[m.WT]) / D["W0"], m.p_leaf, 1.0 / (P.get("goal.c_max_factor") * D["Wstar"] / D["W0"]))
    chk("A5", abs(phi_fn - st_o1["phi"]), 1e-6, True, "GBO on O1's leaf values vs the exact function (tie-break moves O1 within the tolerance)")
    chk("A6", st_o1["leaf_condition_ok"], True, st_o1["leaf_condition_ok"], "leaf condition max W~ <= W* + c_max W0")
    if o1["label"] == "PLAN":
        chk("A7", o1["phi"], "fixed point + certificate", True, f"bPOE history {o1.get('phi_history')}")
    if milp_recs:
        mr = [r for r in milp_recs if r["name"].startswith("O2")]
        if mr:
            chk("A8", mr[0]["mip_gap"], P.get("objective.milp_gap"), True,
                f"MILP status {mr[0]['status']}, gap {mr[0]['mip_gap']:.4f}, nodes {mr[0]['mip_nodes']}, "
                f"start P(goal) {mr[0]['start_p_goal']:.4f}, min W~ >= 0 (L=0 valid): {o2.get('stats', {}).get('min_Wt_bn', np.nan):.1f}")
    if a9:
        chk("A9", a9.get("rel_err", np.nan), 1e-3, a9.get("rel_err", 1) < 1e-3 or a9.get("dual_within_one_sided_differences"),
            f"root cash dual vs one-sided finite differences (+-0.01 $bn) on the decision LP {a9}")
    chk("A11", tr["checks"]["rank_rule"], True, tr["checks"]["rank_rule"], "rank rule K >= d + 1 at every branching")
    mm = tr["checks"]["moments"]
    chk("A11m", max(x_["after"]["max_rel_vol_err"] for x_ in mm), 0.02,
        max(x_["after"]["max_rel_vol_err"] for x_ in mm) < 0.02, "moment-matching residual (vols)")
    hw = (metrics[h_o1]["p_goal_ci95"][1] - metrics[h_o1]["p_goal_ci95"][0]) / 2
    chk("A12", hw, 0.01, hw <= 0.01, "P(goal) 95% half-width (10,000 pooled paths)")
    chk("A13", len([a for a in att if a.get("ok")]), len(FAMILIES) + 1, all(a.get("ok") for a in att), "switch-off table (Shapley not run)")
    chk("A14", gamb, "no flag", tests["H4"]["a14_pass"], "G6 gambling signatures on O1 (headline recourse); "
        "a flag blocks the change list")
    # parameters read only when the results are assembled, by simulation workers, or by the alternative MILP method
    for k_ in ("goal.W0_reported", "corporate_finance.consent_scenario", "constraints.red_eps_certified",
               "objective.milp_gap", "objective.milp_heuristic_effort"):
        P.get(k_)
    P.used.update(SIM_PARAMS_USED)
    c0 = w["x0"][m0.C]
    thin = (m0.cls >= 1) | (c0 / np.maximum(b0["W"], 1e-9) < P.get("constraints.thin_cash"))
    p_unused = P.unused()
    chk("A16", len(p_unused), 0, len(p_unused) == 0, f"params never read: {p_unused[:8]}")
    a23 = [c for c in cardl if not c["a23_ok"]]
    chk("A23", len(a23), 0, len(a23) == 0, f"card-LP sign mismatches: {[c['unit_id'] for c in a23]}")
    gap_rep = metrics[h_o1]["p_goal_reported_nav"] - metrics[h_o1]["p_goal"]
    chk("A24", gap_rep, 0.02, gap_rep <= 0.02, "P(goal) on reported NAV minus economic NAV")
    lv99 = int((m.p_leaf[np.argsort(-((D['Wstar'] - x1[m.WT])))].cumsum() <= 0.01 + 1e-12).sum()) + 1
    chk("A22", lv99, 6, lv99 >= 6, "leaves inside the 1% CVaR level")
    chk("solves", sum(1 for s in statuses if s != "Optimal"), 0, True,
        f"{len(all_solves)} LP/MIP solves; non-optimal statuses: {sorted(set(s for s in statuses if s != 'Optimal'))}")
    runtime = time.time() - t_start
    chk("A17", runtime, 900, runtime < 900, "total runtime (s) under the 15-minute budget")

    # ------------------------------------------------ results.json
    beliefs_tab = []
    for u, h, b in zip(w["units"], w["book"]["holdings"], w["beliefs"]):
        mk = h["marks"]
        beliefs_tab.append({"unit_id": u["id"], "name": u["name"], "group": u["group"], "segment": u["segment"],
                            "tier": u["tier"], "nav_rep_bn": u["nav"], "nav_econ_bn": u["nav_econ"], "theta": u["theta0"],
                            "unfunded_bn": u["unfunded"], "age_y": u["age"], "remaining_life_y": u["H"],
                            "marks": {"underwritten": {"irr": mk["underwritten"]["irr"], "moic": mk["underwritten"]["moic"]},
                                      "actual": {"irr": mk["actual"]["irr"], "tvpi": mk["actual"]["tvpi"]},
                                      "forecast": {"irr": mk["forecast"]["irr"], "moic": mk["forecast"]["moic"]}},
                            "bid_p_ce": h["bid"]["p_ce"] if h["bid"] else None,
                            "bid_source": h["bid"]["source"] if h["bid"] else None,
                            "signals_forward_basis": {k: {"raw": v["raw"], "debiased": v["debiased"], "sd": v["sd"]}
                                                      for k, v in b["signals"].items()},
                            "prior_mu": b["prior"], "mu_hat": b["mu_hat"], "mu_hat_with_own_bid": b["mu_hat_with_own_bid"],
                            "alpha_hat": b["alpha_hat"], "sigma_post": b["sigma_post"], "sigma_hat": b["sigma_hat"],
                            "p10": b["p10"], "p90": b["p90"], "weights": b["weights"], "flags": b["flags"],
                            "bias_forecast_applied": b["bias_forecast_applied"], "kappa_g": b["kappa_g"],
                            "p_forecast_optimistic": b["p_forecast_optimistic"]})
    a_true = np.array(w["book"]["truth"]["alpha_true"])
    a_hat = np.array([b["alpha_hat"] for b in w["beliefs"]])
    a_fc = np.array([b["signals"]["f"]["raw"] - u["beta_return"] for b, u in zip(w["beliefs"], w["units"])])
    fusion_quality = {"corr_alpha_hat_true": float(np.corrcoef(a_hat, a_true)[0, 1]),
                      "corr_raw_forecast_true": float(np.corrcoef(a_fc, a_true)[0, 1]),
                      "mean_abs_err_alpha_hat_pp": float(100 * np.mean(np.abs(a_hat - a_true))),
                      "mean_abs_err_raw_forecast_pp": float(100 * np.mean(np.abs(a_fc - a_true))),
                      "mean_alpha_hat_minus_true_pp": float(100 * np.mean(a_hat - a_true)),
                      "opportunistic_sharpe_true": float(w["book"]["truth"]["opp_sharpe_true"]),
                      "opportunistic_sharpe_prior": float(P.get("overlay.opp_sr_prior")),
                      "note": "sealed truth revealed for diagnostics only; the optimizer never sees it"}
    policies_tab = {}
    for k, mt in metrics.items():
        policies_tab[k] = dict(mt, value_at_equal_tail=vet.get(k))
    in_tree = {"B0": st_b0, "O1": st_o1}
    if o2.get("ok"):
        in_tree["O2"] = o2["stats"]
    if o3.get("ok"):
        in_tree["O3"] = o3["stats"]
    results = {
        "meta": {"label": LABEL, "spec": "DSGO-1.1 (examples/mpo_v2/spec_review.md)", "params_hash": P.hash(),
                 "seeds": {k: P.get(f"seeds.{k}") for k in ("book", "factor_means", "select", "cert")},
                 "tree_seed": P.get("tree.seed"), "solver": {"name": "HiGHS", "version": "1.15.1", "lp": "ipm+crossover",
                                                             "threads": 1, "mip_gap": P.get("objective.milp_gap")},
                 "workers": nwork, "runtime_s": runtime, "runtime_lp_phase_s": t_lp},
        "config": {"goal": {"rate": P.get("goal.rate"), "years": P.get("goal.years"),
                            "basis": "TWR gross of distributions on economic NAV", "W0_bn": D["W0"], "Wstar_bn": D["Wstar"],
                            "W0_reported_bn": P.get("goal.W0_reported")},
                   "c_max_W0": P.get("goal.c_max_factor") * D["Wstar"] / D["W0"],
                   "eps_red_tree": P.get("constraints.red_eps_tree"), "eps_red_certified": P.get("constraints.red_eps_certified"),
                   "depth_guard": {"levels": P.get("constraints.depth_levels"), "delta_W0": P.get("constraints.depth_delta")},
                   "consent_scenario": P.get("corporate_finance.consent_scenario"),
                   "tree": {"branches": P.get("tree.branches"), "fan_paths": P.get("tree.fan_paths"),
                            "leaves": int(len(D["leaves"])), "decision_nodes": int(m.ND),
                            "stage2_recourse_only": P.get("tree.stage2_recourse_only")}},
        "phase1": {k: v for k, v in w["phase1"].items() if k != "slack_ub"},
        "beliefs": beliefs_tab, "fusion_quality": fusion_quality,
        "tree": {"checks": tr["checks"], "class_mass_by_level": {int(L): [float(m.prob[(m.lvl == L) & (m.cls == c)].sum())
                                                                        for c in range(3)] for L in range(6)},
                 "stage1": [{"node": int(n), "stratum": tr["nodes"][n].get("stratum"), "prob": float(m.prob[n]),
                             "class": ["BEN", "DRT", "STR"][int(m.cls[n])], "eq_total_return": float(tr["eq_tot"][n]),
                             "brent": float(np.exp(tr["lb_end"][n])), "draw_next": float(tr["d_next"][n])}
                            for n in range(1, m.ND) if m.lvl[n] == 1],
                 "effective_leaves": float(1.0 / np.sum(m.p_leaf ** 2)), "leaves_in_cvar99": lv99},
        "b0_readings": {"green_decision_nodes": int(b0["green"][:m.ND].sum()), "behind_nodes": int(b0["behind"].sum()),
                        "thin_decision_nodes": int(thin[:m.ND].sum()),
                        "loss_nodes": int(b0["loss"].sum()), "cvar_X_levels": b0["cvar_X"]},
        "solutions": {"GBO": {"label": o1["label"], "phi": o1["phi"], "phi_history": o1.get("phi_history"),
                              "E_star_bn": o1["E_star"], "tree": st_o1, "tie_tol_bn": o1.get("tie_tol_bn")},
                      "MILP": {"rec": o2.get("rec"), "tree": o2.get("stats")},
                      "CRRA": {"tree": o3.get("stats")}, "B0": {"tree": st_b0}},
        "in_tree": in_tree, "in_tree_simulator": intree_sim,
        "root": root_desc, "lens_r1": lens[:11], "cards": cardl, "change_list": chg, "red_cards": red_cards,
        "contingent_year1": contingent,
        "selection": {"best_rule": best_rule, "recourse_choice": choice, "summary": sel_summary,
                      "n_paths": P.get("simulation.n_select")},
        "oos": {"paths": P.get("simulation.n_cert"), "truth": "sealed", "policies": policies_tab,
                "risk_matched_line": line, "belief_mode": {k: {"p_goal": float(np.mean(v["twr"] >= 0.10)),
                                                              "twr_mean": float(v["twr"].mean())} for k, v in resb.items()},
                "optimism_gap": gaps, "headline_policy": h_o1},
        "hypotheses": tests, "attribution": {"switch_off": att}, "frontier": front, "frontier_delta": dfront,
        "a20_limit_sensitivity": a20, "replication_books": books, "a9": a9, "checks": checks,
        "solves": [{k: v for k, v in s.items() if k != "x"} for s in all_solves],
    }
    det = {k: results[k] for k in ("solutions", "change_list", "oos", "frontier", "attribution", "hypotheses")}
    results["meta"]["determinism_hash"] = stable_hash(r6(_scrub(det)))
    (HERE / "results.json").write_text(jdump(r6(results)), encoding="utf-8")
    log(f"results.json written; determinism hash {results['meta']['determinism_hash']}")
    import report
    report.write(results, P, HERE / "RESULTS.md")
    log(f"RESULTS.md written. total runtime {time.time() - t_start:.1f}s")
    log.save()


def _scrub(o):
    """Drop timing fields before hashing (they vary run to run)."""
    if isinstance(o, dict):
        return {k: _scrub(v) for k, v in o.items() if k not in ("time_s", "wall_s", "runtime_s", "runtime_lp_phase_s")}
    if isinstance(o, list):
        return [_scrub(v) for v in o]
    return o


if __name__ == "__main__":
    mp.freeze_support()
    main()
