"""
ra_gap_01 experiment runner on the eight-group v2 book. SYNTHETIC - NOT ADIC DATA.

Stages (python -I -B ra_run.py <stage> [...]):
  calib    theta* recalibration: action-free G* replica on every path (rate mode, gap_02 conventions, Policy A,
           no RA actions), 50k paths per model, books v1 (gc2 and census-v1 splits), v2u16, v2u11; worst-model P99.6;
           SAA replications of the worst model; theta* by inverting the deterministic ladder G*(theta) of each book
  ladder   deterministic T4' tables at theta*: RA row bridge, SH_TP / SH_TPF, facility need, Phase I / II (R0x R0 R1
           R2), FTP / hurdles / envelopes incl. RA, ENR card, L4 pool row and budgets B_g, L8 (t0 and on the stress
           path, reported vs true), T4' DVA divergence (reported vs V*)
  main     tracked integrated runs (cohort mode, gap_04 initial state, CFP stage at theta*): per-group fans incl.
           RA, RA DVA on V* vs reported NAV, CVaR95 of joint-path RA cures (CLC_RA), P(red), CE
  shapley  ten players (seven groups + TPA + CF + RA), Mix B, exact over 1,024 coalitions per model, path SE,
           permutation-sampling coverage
  sizing   RA NAV scale scan (PE absorbs; private stays 106) and RA commitment split (census vs 45/45/10)
  rh       reduced H with RA sector columns (RE / INF / ENR) beside the five private groups: envelopes and FTP
  enr      confirmatory sealed run for the ENR SELL (pre-registered protocol hashed before the run)
Writes ra_<stage>_results.json next to this file.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra_engine as R  # noqa: E402
import ra_book as B  # noqa: E402

E = R.E
MODELS = ["M1", "M2", "M3", "M4", "M5", "M6"]
WORKERS = 23
N = 10000
POLS = {
    "dn": E.Policy("dn"),
    "mixA": E.Policy("mixA", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
    "mixB": E.Policy("mixB", rcf=10.0, pace=12.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0),
}
THETA_FILE = os.path.join(HERE, "ra_calib_results.json")


def q5(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return None
    return [round(float(v), 4) for v in np.quantile(x, [0.05, 0.25, 0.5, 0.75, 0.95])]


def save(name, obj):
    with open(os.path.join(HERE, f"ra_{name}_results.json"), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))


def pool_map(fn, jobs, workers=WORKERS):
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(fn, jobs, chunksize=1))


def theta_star(book: str) -> float:
    d = json.load(open(THETA_FILE, encoding="utf-8"))
    return float(d["theta_star"][book]["theta"])


# ============================================================================================ calib
CALIB_BOOKS = {"v1_gc2": dict(book="v1", census="gc2"), "v1_cv1": dict(book="v1", census="v1"),
               "v2u16": dict(book="v2u16", census="v1"), "v2u11": dict(book="v2u11", census="v1")}
CALIB_N = 50000


def w_calib(args):
    key, mk, seed, init = args
    kw = CALIB_BOOKS[key]
    cfg = R.Cfg(init=init, groups="rate", overlay="t1", links=False, stage="t1", census=kw["census"],
                players=frozenset(R.PLAYERS9), trigger="none", book=kw["book"])
    r = R.simulate(E.MODELS[mk], E.Policy("A"), cfg, n=CALIB_N, seed=seed)
    return (key, mk, seed, init), dict(gstar_q=r["gstar_q"], p_red=r["p_red"])


def _gstar_paths(args):
    key, mk, seed, init = args
    kw = CALIB_BOOKS[key]
    cfg = R.Cfg(init=init, groups="rate", overlay="t1", links=False, stage="t1", census=kw["census"],
                players=frozenset(R.PLAYERS9), trigger="none", book=kw["book"])
    r = R.simulate(E.MODELS[mk], E.Policy("A"), cfg, n=CALIB_N, seed=seed)
    return (key, mk, seed, init), r["_gstar"]


def ladder_gstar_curve(book: str, census: str, thetas, ra_opts=None):
    import ra_ladder as RL
    g = []
    for th in thetas:
        lev = RL.lev_of(reserve=0.08, book=book, census=("gap02" if census == "gc2" else "v1"))
        g.append(RL.gl_ladder(RL.s_star(th), lev, theta=th, ra_opts=dict(ra_opts or {}))["gstar"])
    return np.array(g)


def stage_calib():
    eps24 = 1 - (1 - 0.01) ** (8 / 20)
    seeds = [20261018]
    saa_seeds = [20261018 + 101 * i for i in range(1, 6)]
    jobs = [(k, mk, s, "gap02") for k in CALIB_BOOKS for mk in MODELS for s in seeds]
    jobs += [(k, "M6", s, "gap02") for k in ("v2u16", "v2u11", "v1_cv1") for s in saa_seeds]
    jobs += [(k, mk, 20261018, "gap04") for k in ("v2u16", "v2u11") for mk in MODELS]
    t0 = time.time()
    res = dict(pool_map(_gstar_paths, jobs))
    print(f"calib MC {len(jobs)} runs in {time.time() - t0:.0f}s")
    thetas = np.round(np.arange(0.0, 1.2001, 0.01), 4)
    curves = {k: ladder_gstar_curve(v["book"], v["census"], thetas) for k, v in CALIB_BOOKS.items()}
    out = {"eps24": eps24, "thetas": thetas.tolist(), "curves": {k: v.tolist() for k, v in curves.items()},
           "mc": {}, "theta_star": {}, "saa": {}}
    for (k, mk, s, init), g in res.items():
        out["mc"][f"{k}|{mk}|{s}|{init}"] = dict(q=[float(x) for x in np.quantile(g, [0.5, 0.9, 0.95, 0.99,
                                                                                         1 - eps24, 0.999])],
                                                  p996=float(np.quantile(g, 1 - eps24)))
    for k in CALIB_BOOKS:
        p = {mk: float(np.quantile(res[(k, mk, 20261018, "gap02")], 1 - eps24)) for mk in MODELS}
        worst = max(p, key=p.get)
        tgt = p[worst]
        th = float(np.interp(tgt, curves[k], thetas))
        mix = float(np.quantile(np.concatenate([res[(k, mk, 20261018, "gap02")] for mk in MODELS]), 1 - eps24))
        out["theta_star"][k] = dict(worst_model=worst, gstar_p996=tgt, theta=th, by_model=p,
                                    mixture_p996=mix, theta_mixture=float(np.interp(mix, curves[k], thetas)))
        if k in ("v2u16", "v2u11", "v1_cv1"):
            reps = [float(np.quantile(res[(k, "M6", s, "gap02")], 1 - eps24)) for s in saa_seeds] + [p["M6"]]
            pooled = float(np.quantile(np.concatenate([res[(k, "M6", s, "gap02")] for s in saa_seeds]
                                                      + [res[(k, "M6", 20261018, "gap02")]]), 1 - eps24))
            out["saa"][k] = dict(gstar=reps, theta=[float(np.interp(x, curves[k], thetas)) for x in reps],
                                 pooled_gstar=pooled, pooled_theta=float(np.interp(pooled, curves[k], thetas)))
        if k in ("v2u16", "v2u11"):
            p4 = {mk: float(np.quantile(res[(k, mk, 20261018, "gap04")], 1 - eps24)) for mk in MODELS}
            w4 = max(p4, key=p4.get)
            out["theta_star"][k]["gap04_init"] = dict(worst_model=w4, gstar_p996=p4[w4],
                                                      theta=float(np.interp(p4[w4], curves[k], thetas)), by_model=p4)
    save("calib", out)
    print(json.dumps(out["theta_star"], indent=1))
    print(json.dumps(out["saa"], indent=1))


# ============================================================================================ main
MAIN_POLS = {"off": ("dn", frozenset()), "dn": ("dn", frozenset(R.PLAYERS)), "mixA": ("mixA", frozenset(R.PLAYERS)),
             "mixB": ("mixB", frozenset(R.PLAYERS)),
             "mixB_raoff": ("mixB", frozenset(R.PLAYERS9))}


def w_run(args):
    tag, mk, pk, cfg_kw, n, keep, seed = args
    cfg = R.Cfg(**cfg_kw)
    t0 = time.time()
    r = R.simulate(E.MODELS[mk], POLS[pk], cfg, n=n, seed=seed)
    out = {k: v for k, v in r.items() if not k.startswith("_")}
    out["ce"] = R.ce_wealth(r["_w"])
    out["secs"] = time.time() - t0
    if keep in ("paths", "fans", "rh"):
        out["_w"] = r["_w"].astype(np.float64)
        out["_red"] = r["_red"]
    if keep in ("fans", "rh") and "_rec" in r:
        rec = r["_rec"]
        out["fans"] = {}
        for g in R.ACC:
            c, nv, xs = rec["cash"][g], rec["nav"][g], rec["xs"][g]
            out["fans"][g] = dict(p_cash_neg=[float((c[:, y] < 0).mean()) for y in range(5)], cash5=q5(c.sum(1)),
                                  nav5=q5(nv[:, -1]), dva5=q5(xs.sum(1)), mean_cash=[float(c[:, y].mean()) for y in range(5)])
        if keep == "rh":
            out["_cash"] = {g: rec["cash"][g] for g in ("PE", "SEC", "CS", "CO", "PC", "RA")}
            out["_xs"] = {g: rec["xs"][g] for g in ("PE", "SEC", "CS", "CO", "PC", "RA")}
            if "_ra" in r:            # RA increments valued against a true-beta funding basket (like other groups)
                out["_xs"]["RA"] = r["_ra"]["dva"]["true_b1"]
            out["_navavg"] = {g: rec["navavg"][g] for g in ("PE", "SEC", "CS", "CO", "PC", "RA")}
            out["_nav"] = {g: rec["nav"][g][:, -1] for g in ("PE", "SEC", "CS", "CO", "PC", "RA")}
            out["_slack"] = rec["slack"]
    if "_ra" in r and keep in ("fans", "paths"):
        out["_ra_dva"] = {k: v for k, v in r["_ra"]["dva"].items()}
        out["_ra_cure"] = r["_ra"]["cure_q"]
    return tag, out


def stage_main():
    th = {b: theta_star(b) for b in ("v2u16", "v2u11")}
    jobs = []
    for book in ("v2u16", "v2u11"):
        for mk in MODELS:
            for pname, (pk, players) in MAIN_POLS.items():
                kw = dict(track=True, players=players, trigger="current", book=book, theta=th[book])
                jobs.append(((book, mk, pname), mk, pk, kw, N, "fans", 20261018))
    # v1 bridge in this engine (theta 0.76, census v1.0): Mix B and do-nothing
    for mk in MODELS:
        for pname in ("dn", "mixB", "off"):
            pk, players = MAIN_POLS[pname]
            kw = dict(track=True, players=frozenset(p for p in players if p != "RA"), trigger="current", book="v1")
            jobs.append((("v1", mk, pname), mk, pk, kw, N, "fans", 20261018))
    t0 = time.time()
    res = dict(pool_map(w_run, jobs))
    print(f"main runs: {len(jobs)} in {time.time() - t0:.0f}s")
    out = {"theta_star": th, "runs": {}}
    for key, r in res.items():
        book, mk, pname = key
        d = {k: v for k, v in r.items() if not k.startswith("_")}
        if "_ra_cure" in r:
            cq = r["_ra_cure"]
            d["ra_cure_paths"] = dict(c12=q5(cq[:, :4].sum(1)), c24=q5(cq[:, :8].sum(1)))
            dv = r["_ra_dva"]
            gap = dv["rep_obs"] - dv["star_desm"]
            d["ra_dva_gap_rep_minus_star"] = dict(y1=q5(gap[:, 0]), cum5=q5(gap.sum(1)),
                                                  y1_mean=float(gap[:, 0].mean()), cum5_mean=float(gap.sum(1).mean()))
            gap2 = dv["rep_desm"] - dv["star_desm"]
            d["ra_dva_gap_repdesm_minus_star"] = dict(y1=q5(gap2[:, 0]), cum5=q5(gap2.sum(1)))
        out["runs"][f"{book}|{mk}|{pname}"] = d
    # pooled CVaR95 of joint-path cures (CLC_RA input) by book, policy
    out["clc"] = {}
    for book in ("v2u16", "v2u11"):
        for pname in ("off", "dn", "mixB"):
            c12 = np.concatenate([res[(book, mk, pname)]["_ra_cure"][:, :4].sum(1) for mk in MODELS])
            c24 = np.concatenate([res[(book, mk, pname)]["_ra_cure"][:, :8].sum(1) for mk in MODELS])

            def cvar(x, a=0.95):
                k = max(1, int(math.ceil((1 - a) * x.size)))
                return float(np.sort(x)[-k:].mean())
            worst24 = max(MODELS, key=lambda mk: cvar(res[(book, mk, pname)]["_ra_cure"][:, :8].sum(1)))
            out["clc"][f"{book}|{pname}"] = dict(
                cvar95_12_pooled=cvar(c12), cvar95_24_pooled=cvar(c24), mean24=float(c24.mean()),
                worst_model_24=worst24, cvar95_24_worst=cvar(res[(book, worst24, pname)]["_ra_cure"][:, :8].sum(1)),
                clc_bn_yr_15pct_pooled=0.015 * cvar(c24), clc_bn_yr_15pct_worst=0.015 * cvar(
                    res[(book, worst24, pname)]["_ra_cure"][:, :8].sum(1)))
    save("main", out)
    for k, v in out["runs"].items():
        if "|M1|" in k or "|M6|" in k:
            ra = v.get("ra", {})
            print(k, f"P(red) {100 * v['p_red']:.2f}% CE {v['ce']:.1f} W {v['mean_wtilde']:.1f}",
                  "RA cures24 cvar", ra.get("cures24", {}).get("cvar95"))
    print(json.dumps(out["clc"], indent=1))


# ============================================================================================ shapley
NP = len(R.PLAYERS)


def coalition(mask):
    return frozenset(p for i, p in enumerate(R.PLAYERS) if mask >> i & 1)


def w_shap(args):
    mask, mk, book, theta, n = args
    cfg = R.Cfg(players=coalition(mask), trigger="current", book=book, theta=theta)
    r = R.simulate(E.MODELS[mk], POLS["mixB"], cfg, n=n, seed=20261018)
    return mask, dict(w=r["_w"].astype(np.float32), red=r["_red"], p_red=r["p_red"],
                      forgone=r["mean_forgone_g"], ra=(r.get("ra", {}) or {}).get("cures24"))


def shapley_weights():
    w = np.zeros(NP)
    for s in range(NP):
        w[s] = math.factorial(s) * math.factorial(NP - s - 1) / math.factorial(NP)
    return w


def exact_shapley(v):
    w = shapley_weights()
    phi = np.zeros(NP)
    masks = np.arange(2 ** NP)
    sizes = np.array([bin(m).count("1") for m in masks])
    for i in range(NP):
        without = masks[(masks >> i & 1) == 0]
        phi[i] = float((w[sizes[without]] * (v[without | (1 << i)] - v[without])).sum())
    return phi


def perm_estimate(v, P, rng):
    contrib = []
    for _ in range(P // 2):
        perm = rng.permutation(NP)
        acc = np.zeros(NP)
        for order in (perm, perm[::-1]):
            mask = 0
            for i in order:
                acc[i] += v[mask | (1 << i)] - v[mask]
                mask |= 1 << i
        contrib.append(acc / 2)
    contrib = np.array(contrib)
    return contrib.mean(0), contrib.std(0, ddof=1) / math.sqrt(contrib.shape[0])


def shapley_analysis(W, R_, B_=20):
    n = W.shape[1]
    full, empty = 2 ** NP - 1, 0
    ce = lambda w: float(np.mean(np.asarray(w, dtype=np.float64) ** -2.0) ** -0.5)  # noqa: E731
    vals = {"W": W.mean(1).astype(np.float64), "R": R_.mean(1) * 100,
            "CE": np.array([ce(W[k]) for k in range(2 ** NP)])}
    out = {"v": {k: dict(full=float(v[full]), empty=float(v[empty]),
                         singles={p: float(v[1 << i]) for i, p in enumerate(R.PLAYERS)}) for k, v in vals.items()},
           "exact": {}, "path_se": {}, "perm32": {}, "interaction_index": {}}
    blocks = np.array_split(np.arange(n), B_)
    for key, v in vals.items():
        phi = exact_shapley(v)
        out["exact"][key] = {p: float(phi[i]) for i, p in enumerate(R.PLAYERS)}
        phib = []
        for bl in blocks:
            if key == "W":
                vb = W[:, bl].mean(1).astype(np.float64)
            elif key == "R":
                vb = R_[:, bl].mean(1) * 100
            else:
                vb = np.array([ce(W[k, bl]) for k in range(2 ** NP)])
            phib.append(exact_shapley(vb))
        se = np.array(phib).std(0, ddof=1) / math.sqrt(B_)
        out["path_se"][key] = {p: float(se[i]) for i, p in enumerate(R.PLAYERS)}
        alone = np.array([v[1 << i] - v[empty] for i in range(NP)])
        out["interaction_index"][key] = float(np.abs(phi - alone).sum() / max(np.abs(phi).sum(), 1e-12))
        rng = np.random.default_rng(5)
        ests, ses = [], []
        for _ in range(200):
            e_, s_ = perm_estimate(v, 32, rng)
            ests.append(e_)
            ses.append(s_)
        ests, ses = np.array(ests), np.array(ses)
        tot_se = np.sqrt(ses ** 2 + se[None, :] ** 2)
        cover = (np.abs(ests - phi[None, :]) <= 1.96 * tot_se).mean(0)
        out["perm32"][key] = dict(coverage_min=float(cover.min()), coverage={p: float(cover[i]) for i, p in
                                                                             enumerate(R.PLAYERS)},
                                  rmse_max=float(np.sqrt(((ests - phi[None, :]) ** 2).mean(0)).max()))
    return out


def stage_shapley(models=None, book="v2u16"):
    models = models or MODELS
    theta = theta_star(book)
    path = os.path.join(HERE, f"ra_shapley_{book}_results.json")
    out = json.load(open(path)) if os.path.exists(path) else {"players": list(R.PLAYERS), "book": book,
                                                                "theta": theta, "models": {}}
    for mk in models:
        if mk in out["models"]:
            continue
        t0 = time.time()
        res = dict(pool_map(w_shap, [(mask, mk, book, theta, N) for mask in range(2 ** NP)]))
        W = np.stack([res[m]["w"] for m in range(2 ** NP)])
        Rr = np.stack([res[m]["red"] for m in range(2 ** NP)]).astype(float)
        out["models"][mk] = dict(secs=time.time() - t0, analysis=shapley_analysis(W, Rr),
                                 ra_cures24_full=res[2 ** NP - 1]["ra"], ra_cures24_empty=res[0]["ra"])
        a = out["models"][mk]["analysis"]
        print(mk, f"{time.time() - t0:.0f}s", "R:", {p: round(v, 2) for p, v in a["exact"]["R"].items()},
              "CE:", {p: round(v, 2) for p, v in a["exact"]["CE"].items()}, flush=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, default=float)


# ============================================================================================ sizing
def stage_sizing():
    import ra_ladder as RL
    th = theta_star("v2u16")
    scales = (0.6, 0.8, 1.0, 1.2, 1.4)
    splits = {"census": None, "45/45/10": (0.45, 0.45, 0.10), "60/30/10": (0.60, 0.30, 0.10),
              "30/60/10": (0.30, 0.60, 0.10)}
    jobs = []
    for sc in scales:
        for mk in MODELS:
            for pk in ("dn", "mixB"):
                kw = dict(players=frozenset(R.PLAYERS), trigger="current", book="v2u16", theta=th, ra_scale=sc)
                jobs.append(((sc, "census", mk, pk), mk, pk, kw, N, "paths", 20261018))
    for sp, val in splits.items():
        if val is None:
            continue
        for mk in MODELS:
            kw = dict(players=frozenset(R.PLAYERS), trigger="current", book="v2u16", theta=th, ra_split=val)
            jobs.append(((1.0, sp, mk, "mixB"), mk, "mixB", kw, N, "paths", 20261018))
    t0 = time.time()
    res = dict(pool_map(w_run, jobs))
    print(f"sizing runs {len(jobs)} in {time.time() - t0:.0f}s")
    out = {"theta": th, "runs": {}, "ladder": {}, "paired": {}}
    for (sc, sp, mk, pk), r in res.items():
        out["runs"][f"{sc}|{sp}|{mk}|{pk}"] = dict(p_red=r["p_red"], ce=r["ce"], mean_w=r["mean_wtilde"],
                                                    ra_cures24=r.get("ra", {}).get("cures24"),
                                                    ra_cash_y=r.get("ra", {}).get("cash_y_mean"))
    for (sc, sp, mk, pk), r in res.items():
        base = res.get((1.0, "census", mk, pk))
        if base is None:
            continue
        dw = r["_w"] - base["_w"]
        out["paired"][f"{sc}|{sp}|{mk}|{pk}"] = dict(d_mean_w=float(dw.mean()), se=float(dw.std(ddof=1) / math.sqrt(dw.size)),
                                                      d_ce=float(R.ce_wealth(r["_w"]) - R.ce_wealth(base["_w"])),
                                                      d_p_red_pp=float(100 * (r["_red"].mean() - base["_red"].mean())))
    for sc in scales:
        for book in ("v2u16", "v2u11"):
            lev = RL.lev_of(reserve=0.08, book=book, census="v1", ra_scale=sc)
            lad = RL.gl_ladder(RL.s_star(th), lev, theta=th)
            out["ladder"][f"{book}|{sc}"] = dict(gstar=lad["gstar"], SH_TP=lad["SH_TP"], fac=lad["fac_need_24"],
                                                 l8=B.l8(book, sc), ra_nav=18 * sc,
                                                 ra_b24=float(np.sum(lad["gf"]["ra"]["calls"][:24] - lad["gf"]["ra"]["dist"][:24])))
    save("sizing", out)
    for k, v in out["paired"].items():
        print(k, {kk: round(vv, 3) for kk, vv in v.items()})
    print(json.dumps(out["ladder"], indent=1))


# ============================================================================================ reduced H
RH_GROUPS = ("pe", "sec", "cs", "co", "pc", "ra_re", "ra_inf", "ra_enr")
RH_UB = {"pe": 9.0, "sec": 2.4, "cs": 2.4, "co": 1.35, "pc": 2.4, "ra_re": 1.2, "ra_inf": 1.2, "ra_enr": 0.6}
RH_LB = {"pe": 1.8, "sec": 0.0, "cs": 0.0, "co": 0.0, "pc": 0.0, "ra_re": 0.0, "ra_inf": 0.0, "ra_enr": 0.0}
RH_PLAN = {"pe": 6.0, "sec": 1.2, "cs": 1.2, "co": 1.2, "pc": 1.2, "ra_re": 0.45, "ra_inf": 0.525, "ra_enr": 0.225}
RH_DREM = {"pe": 3.0, "sec": 2.0, "cs": 2.0, "co": 3.0, "pc": 1.5, "ra_re": 3.5, "ra_inf": 4.0, "ra_enr": 3.0}
TRANCHE = (1.0, 0.75, 0.5, 0.25)
ACCKEY = {"pe": "PE", "sec": "SEC", "cs": "CS", "co": "CO", "pc": "PC", "ra_re": "RA", "ra_inf": "RA", "ra_enr": "RA"}


def rh_t4c(theta):
    """24-month s*(theta) calls per $ committed (co-investment deploys at once); RA closed-end the same family."""
    c = 1 - (1 - min(0.95, 0.28 * (1 + 0.5 * theta))) ** 2
    return {g: (1.0 if g == "co" else c) for g in RH_GROUPS}


def stage_rh():
    sys.path.insert(0, os.path.dirname(R._T1))
    import gap02_study as S2
    import ra_ladder as RL
    th = theta_star("v2u16")
    jobs = []
    for mk in MODELS:
        base_kw = dict(track=True, players=frozenset(R.PLAYERS), trigger="none", book="v2u16", theta=th)
        jobs.append(((mk, "base"), mk, "mixB", base_kw, N, "rh", 20261018))
        for g in RH_GROUPS:
            jobs.append(((mk, g), mk, "mixB", base_kw | dict(bump=(g, 1.0)), N, "rh", 20261018))
    t0 = time.time()
    res = dict(pool_map(w_run, jobs))
    print(f"rh runs {len(jobs)} in {time.time() - t0:.0f}s")
    lev_b = RL.lev_from_policy(POLS["mixB"], book="v2u16", census="v1")
    lad = RL.gl_ladder(RL.s_star(th), lev_b, theta=th)
    hr = {"tol": float(lad["min_head_tpf_24"]), "app": float(-lad["gstar"])}
    t4c = rh_t4c(th)
    out = {"theta": th, "hr": hr, "models": {}}

    def coeffs(mk):
        base = res[(mk, "base")]
        C = {}
        for g in RH_GROUPS:
            b = res[(mk, g)]
            G_ = ACCKEY[g]
            dcash = (b["_cash"][G_] - base["_cash"][G_])
            C[g] = dict(a12=-dcash[:, 0], a24=-(dcash[:, 0] + dcash[:, 1]),
                        xs=(b["_xs"][G_] - base["_xs"][G_]).sum(1), navyrs=(b["_navavg"][G_] - base["_navavg"][G_]).sum(1),
                        navT=(b["_nav"][G_] - base["_nav"][G_]))
        return C, base["_slack"][:, :4].min(1), base["_slack"][:, :8].min(1)

    def alphas(mk):
        m = E.MODELS[mk]
        eq_arith = math.log1p(m.eq_g) + 0.5 * 0.165 ** 2

        def af(g, b):
            return (g + 0.5 * (b * 0.165) ** 2) - (m.cash_lr + b * (eq_arith - m.cash_lr))
        pi_c = E.stationary_crisis_share(m)
        prem = {s["id"]: s["prem"] for s in B.SLEEVES}
        # ENR carries the draw-surplus hurdle H_j (synthesis s9.3: 1.2-4.8%/yr by sub-sleeve; fund mix ~1.5%) [I]
        return {"pe": af(m.pe_g, 1.1), "sec": af(m.pe_g + 0.005, 0.9), "cs": af(m.cs_g, 0.5),
                "co": af(m.pe_g, 1.3) + R.CO_FEE_EDGE, "pc": af(m.pc_g, 0.3) + pi_c * 0.08,
                "ra_re": prem["RE_CE"], "ra_inf": prem["INF_CE"], "ra_enr": prem["ENR_CE"] - 0.015}

    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix

    def solve(C, H12, H24, idx, al, hr_t4, beta_l=0.99, beta_r=0.95):
        S = idx.size
        gs = RH_GROUPS
        nx = len(gs) * 4
        v = {g: float(C[g]["xs"][idx].mean() + al[g] * C[g]["navT"][idx].mean() * RH_DREM[g]) for g in gs}
        nv = nx + 3 + 3 * S
        c = np.zeros(nv)
        bounds = []
        for gi, g in enumerate(gs):
            w = RH_UB[g] / 4
            for j, mlt in enumerate(TRANCHE):
                c[gi * 4 + j] = -mlt * v[g]
                bounds.append((min(w, max(0.0, RH_LB[g] - j * w)), w))
        bounds += [(None, None)] * 3 + [(0, None)] * (3 * S)
        xs_dm = {g: C[g]["xs"][idx] - C[g]["xs"][idx].mean() for g in gs}
        loss_plan = -sum(xs_dm[g] * RH_PLAN[g] for g in gs)
        k = int(math.ceil((1 - beta_r) * S))
        R_budget = float(np.sort(loss_plan)[-k:].mean())
        ri, ci, vv = [], [], []
        bvec = np.zeros(3 * S + 4)
        srange = np.arange(S)
        blocks = (("a12", H12[idx], nx, nx + 3, 1.0), ("a24", H24[idx], nx + 1, nx + 3 + S, 1.0),
                  ("xs", np.zeros(S), nx + 2, nx + 3 + 2 * S, -1.0))
        for bi, (coef, Hh, ei, zoff, sign) in enumerate(blocks):
            r0 = bi * S
            for gi, g in enumerate(gs):
                col = C[g][coef][idx] if coef != "xs" else xs_dm[g]
                for j in range(4):
                    ri.append(r0 + srange); ci.append(np.full(S, gi * 4 + j)); vv.append(sign * col)
            ri.append(r0 + srange); ci.append(np.full(S, ei)); vv.append(np.full(S, -1.0))
            ri.append(r0 + srange); ci.append(zoff + srange); vv.append(np.full(S, -1.0))
            bvec[r0:r0 + S] = Hh
        rows = {}
        r = 3 * S
        for name, ei, zoff, beta, rhs in (("L12", nx, nx + 3, beta_l, 0.0), ("L24", nx + 1, nx + 3 + S, beta_l, 0.0),
                                          ("R", nx + 2, nx + 3 + 2 * S, beta_r, R_budget)):
            ri.append(np.array([r])); ci.append(np.array([ei])); vv.append(np.array([1.0]))
            ri.append(np.full(S, r)); ci.append(zoff + srange); vv.append(np.full(S, 1.0 / ((1 - beta) * S)))
            bvec[r] = rhs
            rows[name] = r
            r += 1
        for gi, g in enumerate(gs):
            ri.append(np.full(4, r)); ci.append(gi * 4 + np.arange(4)); vv.append(np.full(4, t4c[g]))
        bvec[r] = hr_t4
        rows["T4"] = r
        M = coo_matrix((np.concatenate(vv), (np.concatenate(ri), np.concatenate(ci))), shape=(3 * S + 4, nv)).tocsr()
        sol = linprog(c, A_ub=M, b_ub=bvec, bounds=bounds, method="highs")
        if sol.status != 0:
            return dict(status=int(sol.status))
        x = sol.x
        xg = {g: float(x[gi * 4:(gi + 1) * 4].sum()) for gi, g in enumerate(gs)}
        duals = {k_: float(-sol.ineqlin.marginals[rw]) for k_, rw in rows.items()}
        charge = {g: 0.0 for g in gs}
        for name, coef, Hh, beta in (("L12", "a12", H12[idx], beta_l), ("L24", "a24", H24[idx], beta_l)):
            tot = sum(C[g][coef][idx] * xg[g] for g in gs) - Hh
            kk = int(math.ceil((1 - beta) * S))
            tail = np.argsort(tot)[-kk:]
            for g in gs:
                charge[g] += duals[name] * float(C[g][coef][idx][tail].mean())
        lossx = -sum(xs_dm[g] * xg[g] for g in gs)
        tail = np.argsort(lossx)[-k:]
        for g in gs:
            charge[g] += duals["R"] * float(-xs_dm[g][tail].mean()) + duals["T4"] * t4c[g]
        navyrs = {g: float(C[g]["navyrs"][idx].mean()) for g in gs}
        return dict(status=0, x=xg, duals=duals, v=v,
                    charge_bp=({g: (1e4 * charge[g] / navyrs[g] if navyrs[g] > 1e-6 else None) for g in gs}),
                    alpha_bp=({g: (1e4 * v[g] / (navyrs[g] + C[g]["navT"][idx].mean() * RH_DREM[g])
                                   if navyrs[g] > 1e-6 else None) for g in gs}))

    rng = np.random.default_rng(11)
    pooled = {mk: (*coeffs(mk), alphas(mk)) for mk in MODELS}
    for variant in ("tol", "app"):
        reps = []
        for rep in range(10):
            idxs = {mk: rng.choice(N, 200, replace=False) for mk in MODELS[:5]}
            Cm = {g: {k_: np.concatenate([pooled[mk][0][g][k_][idxs[mk]] for mk in MODELS[:5]])
                      for k_ in ("a12", "a24", "xs", "navyrs", "navT")} for g in RH_GROUPS}
            H12m = np.concatenate([pooled[mk][1][idxs[mk]] for mk in MODELS[:5]])
            H24m = np.concatenate([pooled[mk][2][idxs[mk]] for mk in MODELS[:5]])
            alm = {g: float(np.mean([pooled[mk][3][g] for mk in MODELS[:5]])) for g in RH_GROUPS}
            reps.append(solve(Cm, H12m, H24m, np.arange(1000), alm, hr[variant]))
        ok = [r_ for r_ in reps if r_.get("status") == 0]
        summ = dict(n_ok=len(ok))
        if ok:
            for key in ("x", "charge_bp", "alpha_bp"):
                summ[key] = {g: [float(np.min([r_[key][g] for r_ in ok if r_[key][g] is not None])),
                                 float(np.median([r_[key][g] for r_ in ok if r_[key][g] is not None])),
                                 float(np.max([r_[key][g] for r_ in ok if r_[key][g] is not None]))] for g in RH_GROUPS}
            summ["duals"] = {d: [float(np.min([r_["duals"][d] for r_ in ok])), float(np.median([r_["duals"][d] for r_ in ok])),
                                 float(np.max([r_["duals"][d] for r_ in ok]))] for d in ok[0]["duals"]}
            xra = np.array([[r_["x"]["ra_re"], r_["x"]["ra_inf"], r_["x"]["ra_enr"]] for r_ in ok])
            tot = xra.sum(1, keepdims=True)
            summ["ra_split"] = q5(xra[:, 0] / np.maximum(tot[:, 0], 1e-9)) and \
                dict(re=[float(v) for v in np.quantile(xra[:, 0] / np.maximum(tot[:, 0], 1e-9), [0.0, 0.5, 1.0])],
                     inf=[float(v) for v in np.quantile(xra[:, 1] / np.maximum(tot[:, 0], 1e-9), [0.0, 0.5, 1.0])],
                     enr=[float(v) for v in np.quantile(xra[:, 2] / np.maximum(tot[:, 0], 1e-9), [0.0, 0.5, 1.0])],
                     total=[float(v) for v in np.quantile(tot[:, 0], [0.0, 0.5, 1.0])])
        out["models"][f"pooledM1-M5|mixB|{variant}"] = summ
        print(variant, json.dumps(summ, indent=1)[:4000])
    save("rh", out)


# ============================================================================================ ENR confirmatory
ENR_PROTOCOL = dict(
    action="SELL $0.70bn of fund-held levered upstream (ENR_CE) at t0 into the Gulf-war bid, price 0.80 of reported "
           "NAV; buyer assumes the pro-rata unfunded",
    control="HOLD (identical book, plan and every other RA playbook item; only the ENR SELL toggled)",
    plan="Mix B (revolver $10bn, pacing $12bn + stage cut, band, reserve 8%, $5bn HF notice), current triggers, "
         "all ten players on, book v2u16, CFP proxy at the recalibrated theta*",
    worlds=["M1", "M2", "M3", "M4", "M5", "M6"], paths_per_world=50000,
    seeds="fresh: 31337000 + 1000*k (k = world index); disjoint from every search / screening run (20261018 family)",
    metrics=["dCE ($bn and bp of NAV a year, CRRA 3 on distribution-inclusive W~)", "dE[W~]",
             "dP(red event, 5y)", "dE[W~ | wrong-way paths: SG or DB within 8 quarters]", "oil delta at $70"],
    decision_rule=("QUALIFIED iff, intersection-union across the six worlds: (i) non-inferiority on CE: the paired "
                   "lower 95% bound of dCE >= -0.5bp of NAV a year in every world; (ii) Tier-1 non-inferiority: "
                   "the paired upper 95% bound of dP(red) <= +0.10pp in every world; (iii) purpose: the oil delta at "
                   "$70 falls inside the 10m-bbl hard budget and dE[W~ | wrong-way] > 0 with a lower 95% bound > 0 "
                   "in at least two worlds. NOT ESTABLISHED if (i) or (ii) fails in any world; materiality for "
                   "return claims (15bp a year, main s5.4) is not applicable to a 0.4%-of-NAV action and is not "
                   "used"),
    sensitivities="bid 0.75 / 0.85; size 0.6 / 0.8; plan = do-nothing; extension axis 0; theta* SAA band",
    registered="2026-10-19, before the run")


def stage_enr():
    blob = json.dumps(ENR_PROTOCOL, sort_keys=True).encode()
    proto_hash = hashlib.sha256(blob).hexdigest()
    with open(os.path.join(HERE, "ra_enr_protocol.json"), "w", encoding="utf-8") as fh:
        json.dump(dict(protocol=ENR_PROTOCOL, sha256=proto_hash), fh, indent=1)
    th = theta_star("v2u16")
    variants = {"base": dict(enr_bid=0.80, size=0.70, pk="mixB"), "bid075": dict(enr_bid=0.75, size=0.70, pk="mixB"),
                "bid085": dict(enr_bid=0.85, size=0.70, pk="mixB"), "size06": dict(enr_bid=0.80, size=0.60, pk="mixB"),
                "size08": dict(enr_bid=0.80, size=0.80, pk="mixB"), "dn": dict(enr_bid=0.80, size=0.70, pk="dn"),
                "ext0": dict(enr_bid=0.80, size=0.70, pk="mixB", ra_ext=0.0)}
    jobs = []
    for vname, v in variants.items():
        for k, mk in enumerate(MODELS):
            seed = 31337000 + 1000 * k
            for arm in ("sell", "hold"):
                kw = dict(players=frozenset(R.PLAYERS), trigger="current", book="v2u16", theta=th,
                          enr_bid=v["enr_bid"], enr_sell=(v["size"] if arm == "sell" else 0.0), wrongway=True)
                if "ra_ext" in v:
                    kw["ra_ext"] = v["ra_ext"]
                jobs.append(((vname, mk, arm), mk, seed, kw, v["pk"]))
    t0 = time.time()
    res = dict(pool_map(w_enr_run, jobs, workers=12))
    print(f"enr runs {len(jobs)} in {time.time() - t0:.0f}s")
    out = {"protocol_sha256": proto_hash, "theta": th, "variants": {}}
    for vname in variants:
        rows = {}
        for mk in MODELS:
            s, h = res[(vname, mk, "sell")], res[(vname, mk, "hold")]
            dw = s["w"] - h["w"]
            n = dw.size
            ce_s, ce_h = R.ce_wealth(s["w"]), R.ce_wealth(h["w"])
            # paired bootstrap for dCE (block of paths)
            rng = np.random.default_rng(99)
            bs = []
            for _ in range(400):
                ix = rng.integers(0, n, n)
                bs.append(R.ce_wealth(s["w"][ix]) - R.ce_wealth(h["w"][ix]))
            bs = np.array(bs)
            dce = ce_s - ce_h
            dce_bp = dce / E.NAV0 / 5 * 1e4
            se_ce = float(bs.std(ddof=1))
            dred = s["red"].astype(float) - h["red"].astype(float)
            ww = s["ww"]
            dww = dw[ww] if ww is not None and ww.any() else np.array([0.0])
            rows[mk] = dict(d_mean_w=float(dw.mean()), se_w=float(dw.std(ddof=1) / math.sqrt(n)),
                            d_ce=float(dce), d_ce_bp_yr=float(dce_bp), ce_lb95_bp_yr=float((dce - 1.96 * se_ce) / E.NAV0 / 5 * 1e4),
                            d_p_red_pp=float(100 * dred.mean()), p_red_ub95_pp=float(100 * (dred.mean() + 1.96 * dred.std(ddof=1) / math.sqrt(n))),
                            wrongway_share=float(ww.mean()) if ww is not None else None,
                            d_w_wrongway=float(dww.mean()), d_w_wrongway_lb95=float(dww.mean() - 1.96 * dww.std(ddof=1) / math.sqrt(max(dww.size, 2))),
                            oil_delta_sell=s["ra"]["oil_delta_post_sale"], oil_delta_hold=h["ra"]["oil_delta_post_sale"])
        c1 = all(r_["ce_lb95_bp_yr"] >= -0.5 for r_ in rows.values())
        c2 = all(r_["p_red_ub95_pp"] <= 0.10 for r_ in rows.values())
        c3 = (rows["M1"]["oil_delta_sell"] <= 10.0) and sum(r_["d_w_wrongway_lb95"] > 0 for r_ in rows.values()) >= 2
        out["variants"][vname] = dict(rows=rows, criteria=dict(ce_noninferior=c1, tier1_noninferior=c2, purpose=c3),
                                      label=("QUALIFIED" if (c1 and c2 and c3) else "NOT ESTABLISHED"))
        print(vname, out["variants"][vname]["label"], {mk: (round(r_["d_ce_bp_yr"], 2), round(r_["ce_lb95_bp_yr"], 2),
                                                            round(r_["d_p_red_pp"], 3), round(r_["d_w_wrongway"], 3))
                                                       for mk, r_ in rows.items()})
    save("enr", out)


def w_enr_run(args):
    key, mk, seed, kw, pk = args
    ww = kw.pop("wrongway", False)
    cfg = R.Cfg(**kw)
    r = R.simulate(E.MODELS[mk], POLS[pk], cfg, n=50000, seed=seed)
    return key, dict(w=r["_w"].astype(np.float64), red=r["_red"], p_red=r["p_red"],
                     ra={k: r["ra"][k] for k in ("oil_delta_post_sale", "enr_cash_t0", "enr_value_given")},
                     ww=r.get("_wrongway"))


if __name__ == "__main__":
    stg = sys.argv[1] if len(sys.argv) > 1 else "calib"
    t0 = time.time()
    if stg == "calib":
        stage_calib()
    elif stg == "main":
        stage_main()
    elif stg == "shapley":
        ms = sys.argv[2].split(",") if len(sys.argv) > 2 else None
        bk = sys.argv[3] if len(sys.argv) > 3 else "v2u16"
        stage_shapley(ms, bk)
    elif stg == "sizing":
        stage_sizing()
    elif stg == "rh":
        stage_rh()
    elif stg == "enr":
        stage_enr()
    print(f"[{stg}] done in {time.time() - t0:.0f}s")
