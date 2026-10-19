"""
groups/gap_04 experiment runner on the integrated prototype (g04_engine.py). SYNTHETIC - NOT ADIC DATA.

Stages (python -I g04_run.py <stage> [...]):
  bridge   reconciliation from gap_02's published engine to the integrated prototype, M1-M6, three policies
  main     tracked runs: per-group fans of cash / NAV / DVA, joint trigger frequencies, monetization,
           contingent-budget value under six trigger regimes (paired on common random numbers)
  rh       reduced H: per-path coefficients from year-1 commitment bumps, CVaR LP over 10 SAA replications,
           envelopes and dual-based FTP charges by group
  shapley  exact Shapley over all 512 coalitions of 9 players + permutation-sampling estimator with its
           Monte Carlo error (path blocks x permutations), group-off baseline = HOLD + plan pacing
  pace     group PACE cost per $ forgone; repricing of gap_02 Mix A / Mix B and of gap_02's lever grid
Writes g04_<stage>_results.json next to this file.
"""
from __future__ import annotations

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
import g04_engine as G  # noqa: E402

E = G.E
MODELS = ["M1", "M2", "M3", "M4", "M5", "M6"]
N = 10000
ALL = frozenset(G.PLAYERS)
WORKERS = 22
POLS = {
    "dn": E.Policy("dn"),
    "mixA": E.Policy("mixA", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
    "mixB": E.Policy("mixB", rcf=10.0, pace=12.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0),
}


def q5(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return None
    return [round(float(v), 4) for v in np.quantile(x, [0.05, 0.25, 0.5, 0.75, 0.95])]


def fr(x):
    return None if x is None else float(x)


# ======================================================================================= summaries
def summarize_rec(rec, r):
    S = {}
    fans = {}
    for g in G.ACC:
        c, nv, xs = rec["cash"][g], rec["nav"][g], rec["xs"][g]
        fans[g] = dict(cash=[q5(c[:, y]) for y in range(5)], cash_cum5=q5(c.sum(1)),
                       nav=[q5(nv[:, y]) for y in range(5)], dva=[q5(xs[:, y]) for y in range(5)],
                       dva_cum5=q5(xs.sum(1)), p_cash_neg=[float((c[:, y] < 0).mean()) for y in range(5)],
                       p_cash_cum_neg=float((c.sum(1) < 0).mean()),
                       p_dva_cum_neg=float((xs.sum(1) < 0).mean()),
                       mean_cash=[float(c[:, y].mean()) for y in range(5)],
                       mean_nav=[float(nv[:, y].mean()) for y in range(5)],
                       mean_dva=[float(xs[:, y].mean()) for y in range(5)],
                       mean_navavg=[float(rec["navavg"][g][:, y].mean()) for y in range(5)])
    S["fans"] = fans
    cr = rec["crisis"]
    hot = rec["dhat"] > 0.20
    hot_t = rec["disc"] > 0.20
    for conv in ("gross", "net"):
        st = rec["stage_" + conv]
        ti = rec["tier1_" + conv]
        trig = hot & (st <= 1) & ti
        S["joint_" + conv] = dict(
            p_q=float(trig.mean()), p_ever=float(trig.any(1).mean()),
            p_q_given_crisis=fr(trig[cr].mean()) if cr.any() else None,
            p_q_given_hot=fr(trig[hot].mean()) if hot.any() else None,
            p_le_amber_given_crisis=fr((st[cr] <= 1).mean()) if cr.any() else None,
            p_le_amber_given_hot=fr((st[hot] <= 1).mean()) if hot.any() else None,
            p_tier1_given_hot=fr(ti[hot].mean()) if hot.any() else None,
            p_hot_and_le_amber=float((hot & (st <= 1)).mean()), p_hot_and_tier1=float((hot & ti).mean()),
            occupancy=(np.bincount(st.ravel(), minlength=4) / st.size).tolist(),
            t0=(np.bincount(st[:, 0], minlength=4) / st.shape[0]).tolist(),
            occupancy_given_hot=(np.bincount(st[hot].ravel(), minlength=4) / max(hot.sum(), 1)).tolist())
    S["disc"] = dict(p_hot_q=float(hot.mean()), p_hot_true_q=float(hot_t.mean()),
                     p_hot_true_given_crisis=fr(hot_t[cr].mean()) if cr.any() else None,
                     p_hot_true_given_calm=float(hot_t[~cr].mean()), p_crisis_q=float(cr.mean()),
                     p_crisis_ever=float(cr.any(1).mean()), p_hot_ever=float(hot.any(1).mean()),
                     q=q5(rec["disc"].ravel()))
    mon = rec["mon"] > 1e-6
    stg, stn = rec["stage_gross"], rec["stage_net"]
    tail_cash = rec["mon"] + rec["expiry"]
    crisis_paths = cr.any(1)
    S["mon"] = dict(p_q=float(mon.mean()), p_ever=float(mon.any(1).mean()),
                    share_le_amber_gross=float((mon & (stg <= 1)).sum() / max(mon.sum(), 1)),
                    share_le_amber_net=float((mon & (stn <= 1)).sum() / max(mon.sum(), 1)),
                    share_hot=float((mon & hot).sum() / max(mon.sum(), 1)),
                    share_crisis=float((mon & cr).sum() / max(mon.sum(), 1)),
                    p_q_mon_le_amber=float((mon & (stg <= 1)).mean()),
                    p_q_mon_le_amber_hot=float((mon & (stg <= 1) & hot).mean()),
                    mean_mon_cash=float(rec["mon"][mon].mean()) if mon.any() else 0.0,
                    mon_5y=float(rec["mon"].sum(1).mean()), expiry_5y=float(rec["expiry"].sum(1).mean()),
                    tail_cash_5y=float(tail_cash.sum(1).mean()), premium_5y=float(rec["prem"].sum(1).mean()),
                    tail_cash_5y_crisis_paths=q5(tail_cash.sum(1)[crisis_paths]) if crisis_paths.any() else None,
                    tail_cash_crisis_quarters_per_crisis_path=float((tail_cash * cr).sum(1)[crisis_paths].mean())
                    if crisis_paths.any() else None)
    dep = rec["deploy"]
    tot = dep.sum(1)
    S["deploy"] = dict(p_any=float((tot > 0).mean()), mean_total=float(tot.mean()),
                       mean_total_if_any=float(tot[tot > 0].mean()) if (tot > 0).any() else 0.0,
                       by_year=[float(dep[:, 4 * y:4 * y + 4].sum(1).mean()) for y in range(5)],
                       share_in_crisis=float((dep * cr).sum() / max(dep.sum(), 1e-9)),
                       share_stage_red=float((dep * (rec["stage_pol"] >= 2)).sum() / max(dep.sum(), 1e-9)),
                       mean_disc_at_deploy=float((rec["disc"] * dep).sum() / max(dep.sum(), 1e-9)),
                       share_with_debt=float((dep * (rec["debt"] > 1e-6)).sum() / max(dep.sum(), 1e-9)),
                       sec=float(rec["cont_out_sec"].mean()), cs=float(rec["cont_out_cs"].mean()),
                       cont_nav_T=float(rec["cont_nav"][:, -1].mean()), q=q5(tot))
    acc = rec["coflow_acc"]
    S["co"] = dict(accepted_by_year=[float(np.nanmean(acc[:, 4 * y:4 * y + 4].sum(1))) for y in range(5)],
                   deploy_by_year=[float(rec["co_deploy"][:, 4 * y:4 * y + 4].sum(1).mean()) for y in range(5)],
                   p_flow_binding=float((rec["co_deploy"] >= acc - 1e-9).mean()) if np.isfinite(acc).all() else None,
                   recap_gross_5y=float(rec["recap_gross"].sum(1).mean()),
                   recap_pc_5y=float(rec["recap_pc"].sum(1).mean()))
    S["red_by_year"] = [float(rec["red_q"][:, :4 * (y + 1)].any(1).mean()) for y in range(5)]
    S["sh_t0"] = q5(rec["sh"][:, 0])
    S["slack_min_q"] = q5(rec["slack"].min(1))
    S["debt_max_q"] = q5(rec["debt"].max(1))
    return S


# ======================================================================================= workers
def w_t1(args):
    mk, pk, n, seed = args
    r = E.simulate(E.MODELS[mk], POLS[pk], n=n, seed=seed)
    return (mk, pk), r


def w_run(args):
    tag, mk, pk, cfg_kw, n, keep, summ = args
    cfg = G.Cfg(**cfg_kw)
    t0 = time.time()
    r = G.simulate(E.MODELS[mk], POLS[pk], cfg, n=n)
    out = {k: v for k, v in r.items() if not k.startswith("_")}
    out["ce"] = G.ce_wealth(r["_w"])
    out["secs"] = time.time() - t0
    if summ:
        out["summary"] = summarize_rec(r["_rec"], r)
    if keep == "paths":
        out["_w"] = r["_w"].astype(np.float64)
        out["_red"] = r["_red"]
    elif keep == "rh":
        rec = r["_rec"]
        out["_w"] = r["_w"]
        out["_cash"] = {g: rec["cash"][g] for g in ("PE", "SEC", "CS", "CO", "PC")}
        out["_xs"] = {g: rec["xs"][g] for g in ("PE", "SEC", "CS", "CO", "PC")}
        out["_navavg"] = {g: rec["navavg"][g] for g in ("PE", "SEC", "CS", "CO", "PC")}
        out["_nav"] = {g: rec["nav"][g][:, -1] for g in ("PE", "SEC", "CS", "CO", "PC")}
        out["_slack"] = rec["slack"]
        out["_red"] = r["_red"]
    return tag, out


def pool_map(fn, jobs):
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        return list(ex.map(fn, jobs, chunksize=1))


def save(name, obj):
    with open(os.path.join(HERE, f"g04_{name}_results.json"), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, default=float)


# ======================================================================================= stage: bridge
_B = dict(init="gap04", groups="cohort", overlay="L1", links=True, stage="cfp", census="v1", trigger="none",
          gp_new=True)
BRIDGE = [
    ("S1 +gap_04 initial state", _B | dict(groups="rate", overlay="t1", links=False, stage="t1", census="gc2",
                                           gp_new=False)),
    ("S2 +cohort group engines, census v1", _B | dict(overlay="t1", links=False, stage="t1", gp_new=False)),
    ("S3 +links (co-invest flow, shared GP, recap netting)", _B | dict(overlay="t1", stage="t1", gp_new=False)),
    ("S4 +Level-1 overlay templates (static book)", _B | dict(stage="t1", gp_new=False)),
    ("S5 +group playbooks (PC run-off, CO pause, OVL, TPA)", _B | dict(stage="t1")),
    ("S6 +CFP stage machine drives policy", dict(_B)),
    ("S7 +contingent budgets, current triggers", _B | dict(trigger="current")),
]


def stage_bridge():
    jobs0 = [(mk, pk, N, 20261018) for mk in MODELS for pk in POLS]
    res0 = dict(pool_map(w_t1, jobs0))
    jobs = []
    for si, (sname, kw) in enumerate(BRIDGE):
        for mk in MODELS:
            for pk in POLS:
                jobs.append(((si, mk, pk), mk, pk, kw, N, "none", False))
    res = dict(pool_map(w_run, jobs))
    keys = ("p_red", "cp_upper_red", "mean_wtilde", "ce", "w_inv2", "mean_commit_forgone", "mean_withheld",
            "mean_red_loss", "p_black_12m", "stage_occupancy_avg")
    out = {"S0 gap_02 t1_engine as published": {f"{mk}|{pk}": {k: res0[(mk, pk)].get(k) for k in keys if k != "ce"}
                                                | {"ce": float(np.mean((res0[(mk, pk)]["w_inv2"])) ** -0.5 * E.NAV0)}
                                                for mk in MODELS for pk in POLS}}
    for si, (sname, kw) in enumerate(BRIDGE):
        out[sname] = {f"{mk}|{pk}": {k: res[(si, mk, pk)].get(k) for k in keys} for mk in MODELS for pk in POLS}
    save("bridge", out)
    for sname, d in out.items():
        line = " ".join(f"{mk}:{100 * d[f'{mk}|mixB']['p_red']:.2f}/{100 * d[f'{mk}|dn']['p_red']:.1f}" for mk in MODELS)
        print(f"{sname[:48]:48s} P(red) mixB/dn  {line}")


# ======================================================================================= stage: main
TRIGGERS = ["none", "current", "current_net", "tier1only", "ring50", "ring100", "ring_t1", "ungated"]
MAIN_POLS = {"off": ("dn", frozenset()), "dn": ("dn", ALL), "franchise": ("dn", frozenset({"SEC", "CS", "OVL"})),
             "mixA": ("mixA", ALL), "mixB": ("mixB", ALL)}


def trig_kw(tr):
    if tr == "current_net":
        return dict(trigger="current", stage_conv="net")
    return dict(trigger=tr)


def stage_main():
    jobs = []
    for mk in MODELS:
        for pname, (pk, players) in MAIN_POLS.items():
            trs = ["none"] if pname == "off" else TRIGGERS
            for tr in trs:
                kw = dict(track=True, players=players) | trig_kw(tr)
                jobs.append(((mk, pname, tr, "base"), mk, pk, kw, N, "paths", True))
            if pname in ("mixA", "mixB"):
                for tr in ("current", "ring100"):
                    kw = dict(track=True, players=players, theta_q=0.75) | trig_kw(tr)
                    jobs.append(((mk, pname, tr, "theta75"), mk, pk, kw, N, "paths", True))
    t0 = time.time()
    res = dict(pool_map(w_run, jobs))
    print(f"main runs: {len(jobs)} in {time.time() - t0:.0f}s")
    out = {"runs": {}, "contingent_value": {}}
    for key, r in res.items():
        mk, pname, tr, var = key
        out["runs"][f"{mk}|{pname}|{tr}|{var}"] = {k: v for k, v in r.items() if not k.startswith("_")}
    # paired contingent-budget values (common random numbers)
    for mk in MODELS:
        for pname in ("dn", "franchise", "mixA", "mixB"):
            base = res[(mk, pname, "none", "base")]
            for tr in TRIGGERS[1:]:
                for var in ("base", "theta75"):
                    if (mk, pname, tr, var) not in res:
                        continue
                    rr = res[(mk, pname, tr, var)]
                    dw = rr["_w"] - base["_w"]
                    dep = rr["summary"]["deploy"]["mean_total"]
                    out["contingent_value"][f"{mk}|{pname}|{tr}|{var}"] = dict(
                        d_mean_w=float(dw.mean()), d_w_se=float(dw.std(ddof=1) / math.sqrt(dw.size)), d_w_q=q5(dw),
                        d_ce=float(G.ce_wealth(rr["_w"]) - G.ce_wealth(base["_w"])),
                        d_p_red=float(rr["_red"].mean() - base["_red"].mean()),
                        red_new=int((rr["_red"] & ~base["_red"]).sum()), red_avoided=int((base["_red"] & ~rr["_red"]).sum()),
                        mean_deployed=dep, value_per_dollar=float(dw.mean() / dep) if dep > 1e-9 else None,
                        p_any=rr["summary"]["deploy"]["p_any"])
    save("main", out)
    for k, v in out["contingent_value"].items():
        if k.endswith("|base"):
            print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items() if kk != "d_w_q"})


# ======================================================================================= stage: reduced H
RH_GROUPS = ("pe", "sec", "cs", "co", "pc")
RH_UB = {"pe": 9.0, "sec": 2.4, "cs": 2.4, "co": 1.35, "pc": 2.4}
RH_LB = {"pe": 1.8, "sec": 0.0, "cs": 0.0, "co": 0.0, "pc": 0.0}
RH_PLAN = {"pe": 7.2, "sec": 1.2, "cs": 1.2, "co": 1.2, "pc": 1.2}
RH_T4C = {"pe": 0.62, "sec": 0.62, "cs": 0.62, "co": 1.0, "pc": 0.62}   # s*(0.76) 24-month calls per $ committed
RH_DREM = {"pe": 3.0, "sec": 2.0, "cs": 2.0, "co": 3.0, "pc": 1.5}      # NAV-years per $ of NAV left at T [I]
TRANCHE = (1.0, 0.75, 0.5, 0.25)
BUMP = 1.0


def rh_coeffs(base, bumps):
    """Per-path coefficients per $1bn of extra year-1 commitment, from paired (CRN) tracked runs."""
    up = {"pe": "PE", "sec": "SEC", "cs": "CS", "co": "CO", "pc": "PC"}
    C = {}
    for g in RH_GROUPS:
        b = bumps[g]
        G_ = up[g]
        dcash = (b["_cash"][G_] - base["_cash"][G_]) / BUMP
        C[g] = dict(a12=-dcash[:, 0], a24=-(dcash[:, 0] + dcash[:, 1]),
                    xs=(b["_xs"][G_] - base["_xs"][G_]).sum(1) / BUMP,
                    navyrs=(b["_navavg"][G_] - base["_navavg"][G_]).sum(1) / BUMP,
                    navT=(b["_nav"][G_] - base["_nav"][G_]) / BUMP,
                    dW=(b["_w"] - base["_w"]) / BUMP)
    H12 = base["_slack"][:, :4].min(1)
    H24 = base["_slack"][:, :8].min(1)
    return C, H12, H24


def solve_rh(C, H12, H24, idx, alpha_g, hr_t4, beta_l=0.99, beta_r=0.95):
    from scipy.optimize import linprog
    S = idx.size
    gs = RH_GROUPS
    nx = len(gs) * len(TRANCHE)
    # value per $: expected realised 5-year excess (per path) + beyond-horizon alpha on NAV left at T
    v = {g: float(C[g]["xs"][idx].mean() + alpha_g[g] * C[g]["navT"][idx].mean() * RH_DREM[g]) for g in gs}
    # variable layout: x (nx) | eta12, eta24, etaR | z12 (S) | z24 (S) | zR (S)
    nv = nx + 3 + 3 * S
    c = np.zeros(nv)
    bounds = []
    for gi, g in enumerate(gs):
        w = RH_UB[g] / len(TRANCHE)
        for j, mlt in enumerate(TRANCHE):
            c[gi * 4 + j] = -mlt * v[g]
            lb = min(w, max(0.0, RH_LB[g] - j * w))
            bounds.append((lb, w))
    bounds += [(None, None)] * 3 + [(0, None)] * (3 * S)
    xs_dm = {g: C[g]["xs"][idx] - C[g]["xs"][idx].mean() for g in gs}
    # risk budget: CVaR_95 of the demeaned 5-year loss at the plan allocation (the plan is just risk-feasible)
    loss_plan = -sum(xs_dm[g] * RH_PLAN[g] for g in gs)
    k = int(math.ceil((1 - beta_r) * S))
    R_budget = float(np.sort(loss_plan)[-k:].mean())
    from scipy.sparse import coo_matrix
    ri, ci, vv = [], [], []
    b = np.zeros(3 * S + 4)
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
        b[r0:r0 + S] = Hh
    rows_cvar = {}
    r = 3 * S
    for name, ei, zoff, beta, rhs_v in (("L12", nx, nx + 3, beta_l, 0.0), ("L24", nx + 1, nx + 3 + S, beta_l, 0.0),
                                        ("R", nx + 2, nx + 3 + 2 * S, beta_r, R_budget)):
        ri.append(np.array([r])); ci.append(np.array([ei])); vv.append(np.array([1.0]))
        ri.append(np.full(S, r)); ci.append(zoff + srange); vv.append(np.full(S, 1.0 / ((1 - beta) * S)))
        b[r] = rhs_v
        rows_cvar[name] = r
        r += 1
    for gi, g in enumerate(gs):
        ri.append(np.full(4, r)); ci.append(gi * 4 + np.arange(4)); vv.append(np.full(4, RH_T4C[g]))
    b[r] = hr_t4
    rows_cvar["T4"] = r
    M = coo_matrix((np.concatenate(vv), (np.concatenate(ri), np.concatenate(ci))), shape=(3 * S + 4, nv)).tocsr()
    res = linprog(c, A_ub=M, b_ub=b, bounds=bounds, method="highs")
    if res.status != 0:
        return dict(status=int(res.status), message=res.message)
    x = res.x
    xg = {g: float(x[gi * 4:(gi + 1) * 4].sum()) for gi, g in enumerate(gs)}
    duals = {k_: float(-res.ineqlin.marginals[rw]) for k_, rw in rows_cvar.items()}
    # tail sets for Euler-style envelope contributions
    out = dict(status=0, x=xg, duals=duals, v=v, R_budget=R_budget, obj=float(-res.fun))
    env, charge = {}, {}
    for name, coef, Hh, beta in (("L12", "a12", H12[idx], beta_l), ("L24", "a24", H24[idx], beta_l)):
        tot = sum(C[g][coef][idx] * xg[g] for g in gs) - Hh
        kk = int(math.ceil((1 - beta) * S))
        tail = np.argsort(tot)[-kk:]
        env[name] = {g: float(C[g][coef][idx][tail].mean() * xg[g]) for g in gs}
        for g in gs:
            charge.setdefault(g, 0.0)
            charge[g] += duals[name] * float(C[g][coef][idx][tail].mean())
    lossx = -sum(xs_dm[g] * xg[g] for g in gs)
    tail = np.argsort(lossx)[-k:]
    env["R"] = {g: float(-xs_dm[g][tail].mean() * xg[g]) for g in gs}
    env["T4"] = {g: RH_T4C[g] * xg[g] for g in gs}
    for g in gs:
        charge[g] += duals["R"] * float(-xs_dm[g][tail].mean()) + duals["T4"] * RH_T4C[g]
    navyrs = {g: float(C[g]["navyrs"][idx].mean()) for g in gs}
    out["envelopes"] = env
    out["charge_per_dollar"] = charge
    out["navyrs_5y_per_dollar"] = navyrs
    out["charge_bp_per_navyear"] = {g: (1e4 * charge[g] / navyrs[g] if navyrs[g] > 1e-6 else None) for g in gs}
    out["alpha_bp_per_navyear"] = {g: (1e4 * v[g] / (navyrs[g] + C[g]["navT"][idx].mean() * RH_DREM[g])
                                       if navyrs[g] > 1e-6 else None) for g in gs}
    return out


def model_alphas(mk):
    m = E.MODELS[mk]
    eq_arith = math.log1p(m.eq_g) + 0.5 * 0.165 ** 2

    def af(g, b):
        return (g + 0.5 * (b * 0.165) ** 2) - (m.cash_lr + b * (eq_arith - m.cash_lr))
    pi_c = E.stationary_crisis_share(m)
    return {"pe": af(m.pe_g, 1.1), "sec": af(m.pe_g + 0.005, 0.9), "cs": af(m.cs_g, 0.5),
            "co": af(m.pe_g, 1.3) + G.CO_FEE_EDGE, "pc": af(m.pc_g, 0.3) + pi_c * 0.08}


def stage_rh():
    sys.path.insert(0, os.path.dirname(G._T1))
    import gap02_study as S2
    jobs = []
    for mk in MODELS:
        for pk in ("mixB", "mixA"):
            base_kw = dict(track=True, players=ALL, trigger="none")
            jobs.append(((mk, pk, "base"), mk, pk, base_kw, N, "rh", False))
            for g in RH_GROUPS:
                jobs.append(((mk, pk, g), mk, pk, base_kw | dict(bump=(g, BUMP)), N, "rh", False))
    t0 = time.time()
    res = dict(pool_map(w_run, jobs))
    print(f"rh runs {len(jobs)} in {time.time() - t0:.0f}s")
    hr_tol = {pk: float(E.ladder(S2.s_star(0.76), POLS[pk])["min_head_tpf_24"]) for pk in ("mixB", "mixA")}
    hr_app = {pk: float(-E.ladder(S2.s_star(0.76), POLS[pk])["gstar"]) for pk in ("mixB", "mixA")}
    out = {"t4prime_headroom_tolerance_TPF": hr_tol, "t4prime_headroom_appetite_TP": hr_app, "models": {}}
    rng = np.random.default_rng(11)
    for pk, variant in (("mixB", "tol"), ("mixA", "tol"), ("mixB", "app"), ("mixA", "app")):
        hr = {pk: (hr_tol[pk] if variant == "tol" else hr_app[pk])}
        pooled = {}
        for mk in MODELS:
            C, H12, H24 = rh_coeffs(res[(mk, pk, "base")], {g: res[(mk, pk, g)] for g in RH_GROUPS})
            al = model_alphas(mk)
            reps = []
            for rep in range(10):
                idx = rng.choice(N, 1000, replace=False)
                reps.append(solve_rh(C, H12, H24, idx, al, hr[pk]))
            ok = [r_ for r_ in reps if r_.get("status") == 0]
            summ = dict(n_ok=len(ok), alphas=al,
                        coef_means={g: {k_: float(np.mean(C[g][k_])) for k_ in ("a12", "a24", "xs", "navyrs", "navT", "dW")}
                                    for g in RH_GROUPS},
                        H12_q=q5(H12), H24_q=q5(H24))
            if ok:
                for key in ("x", "charge_bp_per_navyear", "alpha_bp_per_navyear", "charge_per_dollar"):
                    summ[key] = {g: [float(np.min([r_[key][g] for r_ in ok if r_[key][g] is not None])),
                                     float(np.median([r_[key][g] for r_ in ok if r_[key][g] is not None])),
                                     float(np.max([r_[key][g] for r_ in ok if r_[key][g] is not None]))]
                                 for g in RH_GROUPS}
                summ["duals"] = {d: [float(np.min([r_["duals"][d] for r_ in ok])), float(np.median([r_["duals"][d] for r_ in ok])),
                                     float(np.max([r_["duals"][d] for r_ in ok]))] for d in ok[0]["duals"]}
                summ["envelopes"] = {row: {g: [float(np.min([r_["envelopes"][row][g] for r_ in ok])),
                                               float(np.median([r_["envelopes"][row][g] for r_ in ok])),
                                               float(np.max([r_["envelopes"][row][g] for r_ in ok]))] for g in RH_GROUPS}
                                     for row in ok[0]["envelopes"]}
            out["models"][f"{mk}|{pk}|{variant}"] = summ
            pooled[mk] = (C, H12, H24, al)
        # pooled M1-M5 mixture (equal weights, 200 paths per model per replication)
        reps = []
        for rep in range(10):
            idxs = {mk: rng.choice(N, 200, replace=False) for mk in MODELS[:5]}   # aligned across coefficients
            Cm = {g: {k_: np.concatenate([pooled[mk][0][g][k_][idxs[mk]] for mk in MODELS[:5]])
                      for k_ in ("a12", "a24", "xs", "navyrs", "navT", "dW")} for g in RH_GROUPS}
            H12m = np.concatenate([pooled[mk][1][idxs[mk]] for mk in MODELS[:5]])
            H24m = np.concatenate([pooled[mk][2][idxs[mk]] for mk in MODELS[:5]])
            alm = {g: float(np.mean([pooled[mk][3][g] for mk in MODELS[:5]])) for g in RH_GROUPS}
            reps.append(solve_rh(Cm, H12m, H24m, np.arange(1000), alm, hr[pk]))
        ok = [r_ for r_ in reps if r_.get("status") == 0]
        summ = dict(n_ok=len(ok))
        if ok:
            for key in ("x", "charge_bp_per_navyear", "alpha_bp_per_navyear"):
                summ[key] = {g: [float(np.min([r_[key][g] for r_ in ok if r_[key][g] is not None])),
                                 float(np.median([r_[key][g] for r_ in ok if r_[key][g] is not None])),
                                 float(np.max([r_[key][g] for r_ in ok if r_[key][g] is not None]))] for g in RH_GROUPS}
            summ["duals"] = {d: [float(np.min([r_["duals"][d] for r_ in ok])), float(np.median([r_["duals"][d] for r_ in ok])),
                                 float(np.max([r_["duals"][d] for r_ in ok]))] for d in ok[0]["duals"]}
            summ["envelopes"] = {row: {g: [float(np.min([r_["envelopes"][row][g] for r_ in ok])),
                                           float(np.median([r_["envelopes"][row][g] for r_ in ok])),
                                           float(np.max([r_["envelopes"][row][g] for r_ in ok]))] for g in RH_GROUPS}
                                 for row in ok[0]["envelopes"]}
        out["models"][f"pooledM1-M5|{pk}|{variant}"] = summ
    save("rh", out)
    for k, v in out["models"].items():
        print(k, "x:", {g: [round(a, 2) for a in v.get("x", {}).get(g, [])] for g in RH_GROUPS},
              "duals:", {d: [round(a, 4) for a in vv] for d, vv in v.get("duals", {}).items()})


# ======================================================================================= stage: Shapley
NP = len(G.PLAYERS)


def coalition(mask):
    return frozenset(p for i, p in enumerate(G.PLAYERS) if mask >> i & 1)


def stage_shapley(models=None, pk="mixB", trigger="current"):
    models = models or MODELS
    out = {"players": list(G.PLAYERS), "policy": pk, "trigger": trigger, "models": {}}
    for mk in models:
        t0 = time.time()
        jobs = [((mask,), mk, pk, dict(players=coalition(mask), trigger=trigger), N, "paths", False)
                for mask in range(2 ** NP)]
        res = dict(pool_map(w_run, jobs))
        W = np.stack([res[(mask,)]["_w"] for mask in range(2 ** NP)])           # (512, N)
        R = np.stack([res[(mask,)]["_red"] for mask in range(2 ** NP)]).astype(float)
        scal = {mask: dict(forgone=res[(mask,)]["mean_forgone_g"], withheld=res[(mask,)]["mean_withheld"],
                           red_sales=res[(mask,)]["mean_red_sales"], p_red=res[(mask,)]["p_red"])
                for mask in range(2 ** NP)}
        np.savez_compressed(os.path.join(HERE, f"g04_shapley_{mk}_{pk}.npz"), W=W.astype(np.float32),
                            R=R.astype(np.bool_))
        out["models"][mk] = dict(secs=time.time() - t0, analysis=shapley_analysis(W, R), scalars=scal)
        a = out["models"][mk]["analysis"]
        print(mk, f"{time.time() - t0:.0f}s", "v(full)-v(empty) W:", round(a["v"]["W"]["full"] - a["v"]["W"]["empty"], 2),
              "phi_W:", {p: round(v, 2) for p, v in a["exact"]["W"].items()})
        save(f"shapley_{pk}", out)
    return out


def shapley_weights():
    w = np.zeros(NP)
    for s in range(NP):
        w[s] = math.factorial(s) * math.factorial(NP - s - 1) / math.factorial(NP)
    return w


def exact_shapley(v):
    """v: array over 512 masks -> exact Shapley values (9 players)."""
    w = shapley_weights()
    phi = np.zeros(NP)
    for i in range(NP):
        for mask in range(2 ** NP):
            if mask >> i & 1:
                continue
            s = bin(mask).count("1")
            phi[i] += w[s] * (v[mask | (1 << i)] - v[mask])
    return phi


def perm_estimate(v, P, rng, antithetic=True):
    """Permutation-sampling Shapley estimate with its sampling SE (pairs of a permutation and its reverse)."""
    contrib = []
    npairs = P // 2 if antithetic else P
    for _ in range(npairs):
        perm = rng.permutation(NP)
        orders = [perm, perm[::-1]] if antithetic else [perm]
        acc = np.zeros(NP)
        for order in orders:
            mask = 0
            for i in order:
                acc[i] += v[mask | (1 << i)] - v[mask]
                mask |= 1 << i
        contrib.append(acc / len(orders))
    contrib = np.array(contrib)
    return contrib.mean(0), contrib.std(0, ddof=1) / math.sqrt(contrib.shape[0])


def shapley_analysis(W, R, B=20, reps=200):
    n = W.shape[1]
    full, empty = 2 ** NP - 1, 0
    ce = lambda w: float(np.mean(w ** -2.0) ** -0.5)  # noqa: E731
    vals = {"W": W.mean(1), "R": R.mean(1) * 100, "CE": np.array([ce(W[k]) for k in range(2 ** NP)])}
    out = {"v": {k: dict(full=float(v[full]), empty=float(v[empty]),
                         singles={p: float(v[1 << i]) for i, p in enumerate(G.PLAYERS)}) for k, v in vals.items()},
           "exact": {}, "path_se": {}, "perm": {}, "interaction_share": {}}
    blocks = np.array_split(np.arange(n), B)
    for key, v in vals.items():
        phi = exact_shapley(v)
        out["exact"][key] = {p: float(phi[i]) for i, p in enumerate(G.PLAYERS)}
        # path-sampling error: Shapley on block-level coalition values
        phib = []
        for bl in blocks:
            if key == "W":
                vb = W[:, bl].mean(1)
            elif key == "R":
                vb = R[:, bl].mean(1) * 100
            else:
                vb = np.array([ce(W[k, bl]) for k in range(2 ** NP)])
            phib.append(exact_shapley(vb))
        phib = np.array(phib)
        se = phib.std(0, ddof=1) / math.sqrt(B)
        out["path_se"][key] = {p: float(se[i]) for i, p in enumerate(G.PLAYERS)}
        # interaction share: 1 - sum of stand-alone effects / total
        tot = v[full] - v[empty]
        alone = sum(v[1 << i] - v[empty] for i in range(NP))
        out["interaction_share"][key] = float(1 - alone / tot) if abs(tot) > 1e-12 else None
        # permutation sampling: estimator quality against exact, for several budgets
        rng = np.random.default_rng(5)
        perm = {}
        for P in (8, 16, 32, 64, 128):
            ests, ses = [], []
            for _ in range(reps):
                e_, s_ = perm_estimate(v, P, rng)
                ests.append(e_)
                ses.append(s_)
            ests, ses = np.array(ests), np.array(ses)
            tot_se = np.sqrt(ses ** 2 + se[None, :] ** 2)
            cover = (np.abs(ests - phi[None, :]) <= 1.96 * tot_se).mean(0)
            rmse = np.sqrt(((ests - phi[None, :]) ** 2).mean(0))
            perm[P] = dict(rmse={p: float(rmse[i]) for i, p in enumerate(G.PLAYERS)},
                           mean_se_perm={p: float(ses[:, i].mean()) for i, p in enumerate(G.PLAYERS)},
                           coverage_95={p: float(cover[i]) for i, p in enumerate(G.PLAYERS)},
                           coalitions_per_estimate=int(P * (NP - 1) + 2))
        out["perm"][key] = perm
    return out


# ======================================================================================= stage: PACE
def cohort_navyears(kind, start_q, mD_path, T_q=20):
    """NAV-years after the 5-year horizon per $1 committed at quarter start_q (no growth: alpha accrues on the
    NAV that would have been held). Deterministic exit-window path mD_path (quarterly multipliers)."""
    cal = G.pe_calibration()
    L = cal["L"]
    U, N_ = 1.0, 0.0
    before, after = 0.0, 0.0
    for q in range(start_q, start_q + 80):
        a = (q - start_q) / 4.0 + 0.125
        mD = mD_path[min(q, len(mD_path) - 1)]
        if kind == "pe":
            rd, c = G.pe_rates(np.array([a]), L)
            rd, c = float(rd[0]), float(c[0])
            call = float(G.qr(c)) * U
            dist = float(G.qr(rd * mD)) * N_
        elif kind == "sec":
            call = float(G.qr(0.45)) * U
            dist = float(G.qr(0.25 * mD)) * N_
        elif kind == "co":
            H = lambda x: (max(x, 0.0) / G.CO_WEIB_ETA) ** G.CO_WEIB_K  # noqa: E731
            call = U
            dist = (1 - math.exp(-(H(a) - H(a - 0.25)) * (0.5 if mD < 0.75 else 1.0))) * N_
        elif kind == "cs":
            call = float(G.qr(0.30)) * U
            dist = float(G.qr(0.08 if mD < 0.75 else 0.20)) * N_
        else:  # pc
            call = float(G.qr(0.29)) * U
            dist = float(G.qr(0.5 * (0.18 if mD < 0.75 else 0.24))) * N_
        U -= call
        N_ += call - dist
        if q >= T_q:
            after += N_ / 4
        else:
            before += N_ / 4
    return before, after


def stage_pace():
    sys.path.insert(0, os.path.dirname(G._T1))
    import gap02_study as S2
    import gap02_frontier as F
    out = {}
    # 1. deterministic exit-window path: drought persisting from the gap_04 start (e0 D 0.874), M1 transition
    #    probabilities (drought stays 0.88 a quarter); expected multiplier path
    mD = []
    pD = 0.874
    for q in range(120):
        mD.append(pD * 0.5 + (1 - pD) * 1.0)
        pD *= 0.88
    D = {k: [cohort_navyears(k, q, mD) for q in range(20)] for k in ("pe", "sec", "co", "cs", "pc")}
    out["navyears_per_dollar_by_quarter"] = {k: [[round(b, 3), round(a, 3)] for b, a in v] for k, v in D.items()}
    # 2. re-run gap_02 Mix A / Mix B in t1_engine at 50k (same seed as gap_02) for per-model forgone and timing
    jobs = [(mk, pk, 50000, 20261018) for mk in MODELS for pk in ("mixA", "mixB", "dn")]
    res = dict(pool_map(w_t1, jobs))
    # forgone timing is not returned by t1_engine; use the integrated engine's t1-mode replica for timing
    jobs2 = [((mk, pk), mk, pk, dict(init="gap02", groups="rate", overlay="t1", links=False, stage="t1",
                                     census="gc2", trigger="none"), 50000, "none", False)
             for mk in MODELS for pk in ("mixA", "mixB")]
    res2 = dict(pool_map(w_run, jobs2))
    # 3. group PACE cost per $ forgone (per model): forgone net alpha* beyond the horizon + kappa^GP (upper
    #    bound, PE only) + lost co-investment flow (PE only); gross and net of the reduced-H FTP charge
    rh_path = os.path.join(HERE, "g04_rh_results.json")
    rh = json.load(open(rh_path)) if os.path.exists(rh_path) else None
    KGP_UB = 0.92 * 0.04 + 0.08 * 0.18          # G1 s6.5 illustration: buyout skip 3-4% incl. later funds; elite VC 18%
    KGP_CENTRAL = 0.92 * 0.04 / 2.0 + 0.08 * 0.18 / 3.0   # deflated by the G1 verifier's x1.3-2.6 / x1.8-5.0 bias
    out["kappa_gp"] = dict(upper=KGP_UB, central=KGP_CENTRAL)
    cpace = {}

    def charges(mk, variant):
        key = f"{mk}|mixB|{variant}"
        if rh is not None and key in rh["models"] and "charge_bp_per_navyear" in rh["models"][key]:
            return {g: (rh["models"][key]["charge_bp_per_navyear"][g][1] or 0.0) / 1e4 for g in RH_GROUPS}
        return None

    for mk in MODELS:
        al = model_alphas(mk)
        fz = np.array(res2[(mk, "mixB")]["forgone_by_q"]) + np.array(res2[(mk, "mixA")]["forgone_by_q"])
        wq = fz / fz.sum() if fz.sum() > 0 else np.full(20, 1 / 20)
        Dafter = {k: float(sum(wq[q] * D[k][q][1] for q in range(20))) for k in D}
        Dbefore = {k: float(sum(wq[q] * D[k][q][0] for q in range(20))) for k in D}
        row = {}
        ch_sets = {"gross": {g: 0.0 for g in RH_GROUPS}, "net_tol": charges(mk, "tol"), "net_app": charges(mk, "app")}
        for var, charge in ch_sets.items():
            if charge is None:
                continue
            c_g = {g: max(al[g] - charge[g], 0.0) * Dafter[g] for g in RH_GROUPS}
            co_val = max(al["co"] - charge["co"], 0.0) * (Dbefore["co"] + Dafter["co"])
            lost_co = G.COFLOW_THETA * G.COFLOW_A * co_val           # per $ of PE commitment forgone
            pe_ub = c_g["pe"] + KGP_UB + lost_co
            pe_c = c_g["pe"] + KGP_CENTRAL + lost_co
            others = 0.1 * (c_g["sec"] + c_g["cs"] + c_g["pc"] + c_g["co"])
            row[var] = dict(charge=charge, per_group_alpha_cost=c_g, pe_alpha=c_g["pe"], kgp_ub=KGP_UB,
                            kgp_central=KGP_CENTRAL, lost_co_flow=lost_co, pe_total_ub=pe_ub, pe_total_central=pe_c,
                            blended_ub=0.6 * pe_ub + others, blended_central=0.6 * pe_c + others)
        cpace[mk] = dict(alphas=al, D_after=Dafter, D_before=Dbefore, gap02_C_PACE_TV=S2.C_PACE_TV[mk], **row)
    out["c_pace"] = cpace
    VARS = [("gap02 (2 x (PE - liquid CMA))", None), ("gross alpha*, kappa^GP UB", ("gross", "blended_ub")),
            ("net alpha* (tolerance H), kappa^GP UB", ("net_tol", "blended_ub")),
            ("net alpha* (appetite H), kappa^GP UB", ("net_app", "blended_ub")),
            ("net alpha* (appetite H), kappa^GP central", ("net_app", "blended_central"))]
    # 4. reprice gap_02's certified Mix A / Mix B (50k, t1 engine) - M1-M5 averages, bp of NAV a year
    rep = {}
    for pk in ("mixA", "mixB"):
        d = {}
        for var, key in VARS:
            vals = []
            for mk in MODELS[:5]:
                fg = res[(mk, pk)]["mean_commit_forgone"]
                c = S2.C_PACE_TV[mk] if key is None else cpace[mk][key[0]][key[1]]
                vals.append(c * fg / E.NAV0 / 5 * 1e4)
            d[var] = float(np.mean(vals))
        d["mean_forgone_M1-M5"] = float(np.mean([res[(mk, pk)]["mean_commit_forgone"] for mk in MODELS[:5]]))
        rep[pk] = d
    out["mix_pacing_bp"] = rep
    # 5. re-run gap_02's frontier logic on the stored 2,880-mix grid with the group PACE cost
    raw = json.load(open(os.path.join(os.path.dirname(G._T1), "gap02_grid_raw.json")))
    rows = raw["grid"]
    by = {r_["kw"]["name"]: r_ for r_ in rows}
    ref = by[raw["reference"]]
    models = F.SCOPES["M1-M5"]
    fr_out = {}
    for var, key in VARS:
        cmap = {mk: (S2.C_PACE_TV[mk] if key is None else cpace[mk][key[0]][key[1]]) for mk in MODELS}

        def outside(row_):
            return float(np.mean([(S2.KAPPA_OWN * row_["models"][k]["mean_withheld"] + cmap[k] * row_["models"][k]["mean_commit_forgone"]
                                   + S2.KAPPA_GP * row_["models"][k]["mean_red_sales"]) / E.NAV0 / 5 * 1e4 for k in models]))

        def premium(row_):
            p = F.premium_bp(row_, models)
            pace_old = p["pacing_tv"]
            pace_new = float(np.mean([cmap[k] * row_["models"][k]["mean_commit_forgone"] / E.NAV0 / 5 * 1e4 for k in models]))
            return p["total"] - pace_old + pace_new, pace_new
        res_v = {}
        for band_ok in (False, True):
            pool = [r_ for r_ in rows if band_ok or not r_["kw"]["band"]]
            g_best_row = max(pool, key=lambda r_: F.g_ce(r_, models) * 1e4 - outside(r_))
            g_best = F.g_ce(g_best_row, models) * 1e4 - outside(g_best_row)
            pts = {}
            for eps in (0.005, 0.01, 0.02):
                cands = [r_ for r_ in pool if F.feasible(r_, eps, "M1-M5", "0.76")[0]]
                if not cands:
                    pts[eps] = None
                    continue
                best_ce = min(cands, key=lambda r_: g_best - (F.g_ce(r_, models) * 1e4 - outside(r_)))
                best_pr = min(cands, key=lambda r_: premium(r_)[0])
                pts[eps] = dict(ce_mix=best_ce["kw"]["name"],
                                ce_price=float(g_best - (F.g_ce(best_ce, models) * 1e4 - outside(best_ce))),
                                prem_mix=best_pr["kw"]["name"], premium=premium(best_pr)[0], premium_pace=premium(best_pr)[1])
            for nm in ("R15_N0_P6c_B0_Q14_A0_H0", "R10_N0_P12c_B1_Q8_A0_H5"):
                if nm in by and (band_ok or not by[nm]["kw"]["band"]):
                    pts[nm] = dict(ce_vs_ref=float((F.g_ce(ref, models) - F.g_ce(by[nm], models)) * 1e4 + outside(by[nm]) - outside(ref)),
                                   premium=premium(by[nm])[0], premium_pace=premium(by[nm])[1],
                                   ce_price=float(g_best - (F.g_ce(by[nm], models) * 1e4 - outside(by[nm]))))
            res_v[f"band={band_ok}"] = dict(ce_best_unconstrained=g_best_row["kw"]["name"], points=pts)
        fr_out[var] = res_v
    out["frontier_repriced_10k_grid"] = fr_out
    save("pace", out)
    print(json.dumps(out["mix_pacing_bp"], indent=1))
    for mk, v in cpace.items():
        print(mk, "gap02", v["gap02_C_PACE_TV"], {var: {k: round(v[var][k], 4) for k in ("pe_alpha", "lost_co_flow",
                                                                                        "pe_total_ub", "blended_ub",
                                                                                        "blended_central")}
                                                  for var in ("gross", "net_tol", "net_app") if var in v},
              "D_after", {k: round(x, 2) for k, x in v["D_after"].items()})
    print(json.dumps(fr_out, indent=1)[:6000])


if __name__ == "__main__":
    stg = sys.argv[1] if len(sys.argv) > 1 else "bridge"
    t0 = time.time()
    if stg == "bridge":
        stage_bridge()
    elif stg == "main":
        stage_main()
    elif stg == "rh":
        stage_rh()
    elif stg == "shapley":
        ms = sys.argv[2].split(",") if len(sys.argv) > 2 else None
        stage_shapley(ms)
    elif stg == "pace":
        stage_pace()
    print(f"[{stg}] done in {time.time() - t0:.0f}s")
