"""Tree architecture preview for the goal-seeking optimizer (v2 layout).

A real, solved multistage stochastic LP on a 10 x 5 x 4 scenario tree (1 + 10 + 50 + 200 nodes),
with 24 holdings across ADIC's eight groups. At every decision node (t0, t1, t2) the optimizer
chooses, per holding, SELL / ADD / REFINANCE (cash-out borrowing against the holding), and at
portfolio level the revolver (FUND), synthetic exposure (LEVER), and PE pacing (PACE). The owner's
draw is an exogenous liability paid at every node.

SYNTHETIC: illustrative parameters loosely anchored on the research; not ADIC data, not a forecast.
The full, verified prototype is examples/mpo_v2 (in progress).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import cvxpy as cp
import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
OUT = HERE / "results.json"
W0 = 177.0
YEARS = 3
GOAL = 1.10 ** YEARS          # 10% a year, gross of distributions (draws accrued)
R_CASH = 0.04
REGIMES = ["N", "D", "C"]
TRANS = {"N": [0.70, 0.20, 0.10], "D": [0.30, 0.55, 0.15], "C": [0.25, 0.35, 0.40]}
# equity factor by regime: mean, vol (annual); long-run mean used to centre holding means
F_MEAN = {"N": 0.09, "D": 0.04, "C": -0.22}
F_VOL = {"N": 0.12, "D": 0.10, "C": 0.16}
F_LR = 0.054
DRAW = {"N": 0.06, "D": 0.075, "C": 0.10}          # owner draw, % of NAV (oil weak -> higher)
REV_LIMIT, REV_AVAIL, REV_SPREAD = 15.0, {"N": 1.0, "D": 1.0, "C": 0.5}, 0.015
SYN_FIN = {"N": 0.005, "D": 0.008, "C": 0.0175}    # synthetic beta financing spread
SYN_IM = 0.10                                       # initial margin held in cash
PE_PLAN, PACE_COST = 4.0, 0.086                     # planned new PE commitments a year; franchise cost per $ cut
LEV_CAP, CASH_FLOOR = 1.30, 0.04

# group economics: bid (1 - discount) by regime, depth cap (share of value sellable per year),
# LTV for holding-secured borrowing (REFINANCE), borrowing spread by regime, add cap, distribution rate,
# call rate on unfunded, unfunded passed per $ of NAV sold handled per holding.
G = {
    "PE":        dict(bid=(0.92, 0.86, 0.68), depth=(0.25, 0.15, 0.08), ltv=0.15, spr=(0.05, 0.07, 0.10), addcap=0.15, dist=(0.18, 0.09, 0.04), call=(0.30, 0.29, 0.35)),
    "SECONDARIES": dict(bid=(0.90, 0.85, 0.70), depth=(0.25, 0.20, 0.10), ltv=0.15, spr=(0.05, 0.07, 0.10), addcap=0.20, dist=(0.22, 0.14, 0.06), call=(0.35, 0.30, 0.35)),
    "CAPSOL":    dict(bid=(0.95, 0.90, 0.75), depth=(0.30, 0.20, 0.10), ltv=0.40, spr=(0.03, 0.04, 0.07), addcap=0.20, dist=(0.12, 0.10, 0.06), call=(0.0, 0.0, 0.0)),
    "COINVEST":  dict(bid=(0.85, 0.78, 0.60), depth=(0.20, 0.15, 0.05), ltv=0.10, spr=(0.05, 0.07, 0.10), addcap=0.15, dist=(0.15, 0.08, 0.03), call=(0.0, 0.0, 0.0)),
    "PUBLIC_HF": dict(bid=(0.99, 0.98, 0.95), depth=(0.25, 0.25, 0.10), ltv=0.20, spr=(0.03, 0.04, 0.08), addcap=0.25, dist=(0.0, 0.0, 0.0), call=(0.0, 0.0, 0.0)),
    "PUBLIC_LO": dict(bid=(0.998, 0.997, 0.99), depth=(1.0, 1.0, 1.0), ltv=0.0, spr=(0.0, 0.0, 0.0), addcap=1.0, dist=(0.0, 0.0, 0.0), call=(0.0, 0.0, 0.0)),
    "PRIVCREDIT": dict(bid=(0.98, 0.96, 0.85), depth=(0.30, 0.25, 0.10), ltv=0.50, spr=(0.03, 0.04, 0.07), addcap=0.20, dist=(0.10, 0.09, 0.07), call=(0.0, 0.0, 0.0)),
    "REALASSETS": dict(bid=(0.95, 0.90, 0.78), depth=(0.20, 0.15, 0.08), ltv=0.50, spr=(0.025, 0.035, 0.06), addcap=0.15, dist=(0.07, 0.06, 0.04), call=(0.25, 0.25, 0.30)),
    "OVERLAY":   dict(bid=(0.99, 0.99, 0.98), depth=(1.0, 1.0, 1.0), ltv=0.0, spr=(0.0, 0.0, 0.0), addcap=1.0, dist=(0.0, 0.0, 0.0), call=(0.0, 0.0, 0.0)),
}
GROUP_LABEL = {"PE": "PE funds", "SECONDARIES": "Secondaries", "CAPSOL": "Capital Solutions", "COINVEST": "Co-investment",
               "PUBLIC_HF": "Public Markets (HF)", "PUBLIC_LO": "Public Markets (LO)", "PRIVCREDIT": "Private Credit",
               "REALASSETS": "Real Assets", "OVERLAY": "Overlay"}

# 24 holdings: name, group, value $bn, unfunded $bn, beta to equity factor, three marks as IRR
# (underwritten, actual since inception, group forecast base with low/high), age in years.
H = [
    ("PE Buyout 2016", "PE", 14.0, 1.0, 0.9, 0.18, 0.11, (0.07, 0.10, 0.13), 10),
    ("PE Buyout 2019", "PE", 12.0, 3.0, 1.0, 0.20, 0.08, (0.08, 0.13, 0.17), 7),
    ("PE Growth 2021", "PE", 8.0, 6.0, 1.3, 0.25, 0.02, (0.06, 0.15, 0.22), 5),
    ("Secondary Fund 2018", "SECONDARIES", 6.0, 0.6, 0.7, 0.16, 0.12, (0.08, 0.11, 0.14), 8),
    ("LP Portfolio 2022", "SECONDARIES", 5.0, 1.2, 0.8, 0.17, 0.13, (0.09, 0.12, 0.15), 4),
    ("GP-led CV 2023", "SECONDARIES", 3.0, 0.4, 1.1, 0.22, 0.10, (0.05, 0.14, 0.20), 3),
    ("Pref Equity 1", "CAPSOL", 3.0, 0.0, 0.4, 0.13, 0.11, (0.09, 0.11, 0.12), 3),
    ("NAV Lending 2", "CAPSOL", 3.0, 0.0, 0.3, 0.12, 0.11, (0.09, 0.10, 0.11), 2),
    ("Special Sits 3", "CAPSOL", 2.0, 0.0, 0.8, 0.18, 0.07, (0.03, 0.10, 0.16), 4),
    ("Co-inv Industrial", "COINVEST", 7.0, 0.0, 1.0, 0.20, 0.12, (0.06, 0.12, 0.18), 5),
    ("Co-inv Software", "COINVEST", 6.0, 0.0, 1.4, 0.24, 0.03, (0.02, 0.14, 0.22), 4),
    ("Co-inv Healthcare", "COINVEST", 5.0, 0.0, 0.9, 0.19, 0.14, (0.07, 0.11, 0.15), 6),
    ("HF Multi-strategy", "PUBLIC_HF", 12.0, 0.0, 0.3, 0.09, 0.06, (0.04, 0.07, 0.09), 6),
    ("HF Macro", "PUBLIC_HF", 8.0, 0.0, -0.1, 0.08, 0.05, (0.02, 0.06, 0.10), 5),
    ("Long-only Global Equity", "PUBLIC_LO", 36.0, 0.0, 1.0, 0.075, 0.08, (0.04, 0.07, 0.10), 8),
    ("Direct Lending A", "PRIVCREDIT", 6.0, 0.0, 0.3, 0.10, 0.09, (0.07, 0.09, 0.10), 4),
    ("Direct Lending B", "PRIVCREDIT", 5.0, 0.0, 0.35, 0.11, 0.07, (0.05, 0.08, 0.10), 3),
    ("Asset-Based Finance", "PRIVCREDIT", 3.0, 0.0, 0.25, 0.10, 0.09, (0.07, 0.09, 0.11), 2),
    ("Core Real Estate", "REALASSETS", 8.0, 0.5, 0.5, 0.09, 0.04, (0.04, 0.07, 0.09), 7),
    ("Infrastructure Core+", "REALASSETS", 6.0, 1.0, 0.4, 0.11, 0.09, (0.07, 0.09, 0.11), 5),
    ("Energy & Resources", "REALASSETS", 4.0, 0.5, 0.8, 0.15, 0.10, (0.03, 0.10, 0.16), 4),
    ("Tail-hedge ladder", "OVERLAY", 0.5, 0.0, -2.5, 0.0, 0.0, (0.0, 0.0, 0.0), 1),
    ("Opportunistic book", "OVERLAY", 2.0, 0.0, 0.1, 0.06, 0.05, (0.02, 0.05, 0.08), 3),
    ("Synthetic equity beta", "OVERLAY", 0.0, 0.0, 1.0, 0.0, 0.0, (0.0, 0.0, 0.0), 0),
]
# group forecast optimism (subtracted) and underwriting optimism, from the research's bias priors (illustrative)
BIAS_F = {"PE": 0.03, "SECONDARIES": 0.02, "CAPSOL": 0.01, "COINVEST": 0.04, "PUBLIC_HF": 0.02, "PUBLIC_LO": 0.0,
          "PRIVCREDIT": 0.01, "REALASSETS": 0.02, "OVERLAY": 0.01}
BIAS_U = {"PE": 0.05, "SECONDARIES": 0.03, "CAPSOL": 0.02, "COINVEST": 0.06, "PUBLIC_HF": 0.03, "PUBLIC_LO": 0.0,
          "PRIVCREDIT": 0.015, "REALASSETS": 0.03, "OVERLAY": 0.02}


def fuse(h) -> tuple[float, dict]:
    """Credibility-weighted fusion of the three marks, after group bias correction (SYNTHETIC rule)."""
    name, g, v, u, beta, mu_u, mu_a, (f_lo, f_base, f_hi), age = h
    if name == "Tail-hedge ladder":
        return -0.70, {"note": "insurance: loses its premium unless a crisis hits"}
    if name == "Synthetic equity beta":
        return F_LR, {"note": "futures exposure: equity return minus financing"}
    w_a = min(age / 10.0, 0.5)               # actuals earn credibility with age
    w_u = 0.25 * (1 - w_a)                   # underwriting fades
    w_f = 1 - w_a - w_u
    spread = (f_hi - f_lo) / 2.563          # stated P10-P90 band -> sigma
    mu = w_u * (mu_u - BIAS_U[g]) + w_a * mu_a + w_f * (f_base - BIAS_F[g])
    return mu, {"w_underwritten": round(w_u, 3), "w_actual": round(w_a, 3), "w_forecast": round(w_f, 3),
                "forecast_sigma": round(spread, 4)}


def build_tree(seed: int = 7):
    rng = np.random.default_rng(seed)
    nodes = [dict(id=0, stage=0, regime="D", parent=None, p=1.0, bp=1.0, f=0.0, path="D")]
    plan = {1: 10, 2: 5, 3: 4}
    frontier = [0]
    for stage in (1, 2, 3):
        nxt = []
        for pid in frontier:
            par = nodes[pid]
            probs = TRANS[par["regime"]]
            k = plan[stage]
            # stratified regime counts (largest remainder, at least one child per regime with prob >= 0.1)
            raw = np.array(probs) * k
            cnt = np.floor(raw).astype(int)
            for r in range(3):
                if probs[r] >= 0.1 and cnt[r] == 0:
                    cnt[r] = 1
            while cnt.sum() > k:
                i = int(np.argmax(cnt - raw))
                cnt[i] -= 1
            while cnt.sum() < k:
                i = int(np.argmax(raw - cnt))
                cnt[i] += 1
            for r, reg in enumerate(REGIMES):
                if cnt[r] == 0:
                    continue
                qs = (np.arange(cnt[r]) + 0.5) / cnt[r]          # stratified factor shocks
                z = norm.ppf(qs)
                rng.shuffle(z)
                for zz in z:
                    nid = len(nodes)
                    fac = F_MEAN[reg] + F_VOL[reg] * float(zz)
                    bp = probs[r] / cnt[r]
                    nodes.append(dict(id=nid, stage=stage, regime=reg, parent=pid, p=par["p"] * bp, bp=bp, f=fac,
                                      path=par["path"] + ">" + reg))
                    nxt.append(nid)
        frontier = nxt
    for n in nodes:
        n["children"] = [m["id"] for m in nodes if m["parent"] == n["id"]]
    return nodes


def holding_return(i: int, n: dict, mu: np.ndarray) -> float:
    name, g, v, u, beta = H[i][:5]
    reg, fac = n["regime"], n["f"]
    if name == "Tail-hedge ladder":
        return 3.0 if reg == "C" and fac < -0.15 else (1.0 if reg == "C" else -0.70)
    if name == "Synthetic equity beta":
        return fac
    extra = -0.12 if (name == "Energy & Resources" and reg == "C") else 0.0      # oil wrong-way
    return float(mu[i] + beta * (fac - F_LR) + extra)


def solve(nodes, mu, mode: str, allow: set[str], cvar_floor: float | None):
    """mode: 'crra' (risk-averse utility) or 'max_ew' (goal-seeking: max expected wealth within the tail limit)."""
    n_h = len(H)
    dec = [n for n in nodes if n["stage"] < YEARS]
    leaves = [n for n in nodes if n["stage"] == YEARS]
    idx = {n["id"]: k for k, n in enumerate(nodes)}
    N = len(nodes)
    V = cp.Variable((N, n_h), nonneg=True)    # post-decision value (pre-decision at leaves)
    L = cp.Variable((N, n_h), nonneg=True)    # holding-secured loans (REFINANCE)
    S = cp.Variable((N, n_h), nonneg=True)    # SELL
    A = cp.Variable((N, n_h), nonneg=True)    # ADD
    RB = cp.Variable((N, n_h), nonneg=True)   # REFINANCE draw
    RR = cp.Variable((N, n_h), nonneg=True)   # loan repay
    C = cp.Variable(N)                        # cash
    B = cp.Variable(N, nonneg=True)           # revolver balance
    PC = cp.Variable(N, nonneg=True)          # pacing cut
    U = cp.Variable(N, nonneg=True)           # PE unfunded (group level, youngest fund receives commitments)
    cons = []
    lev_i = [k for k, h in enumerate(H) if h[0] == "Synthetic equity beta"][0]
    pe_young = [k for k, h in enumerate(H) if h[0] == "PE Growth 2021"][0]
    draws = {}
    nav_ref = {}
    # reference NAV path for the exogenous draw: status-quo growth at the fused means (computed once)
    w_mu = float(np.dot(mu[:lev_i] * 0 + 1, [h[2] for h in H][:lev_i]))  # placeholder (unused)
    for n in nodes:
        if n["parent"] is None:
            nav_ref[n["id"]] = W0
        else:
            par = nav_ref[n["parent"]]
            port_r = 0.55 * (n["f"]) + 0.45 * 0.07   # crude book return for the reference path
            nav_ref[n["id"]] = par * (1 + port_r) - DRAW[nodes[n["parent"]]["regime"]] * par
        draws[n["id"]] = DRAW[n["regime"]] * nav_ref[n["id"]] if n["parent"] is not None else 0.0
    unf0 = sum(h[3] for h in H)
    for n in nodes:
        k = idx[n["id"]]
        reg = n["regime"]
        ri = REGIMES.index(reg)
        if n["parent"] is None:
            Vpre = np.array([h[2] for h in H])
            cons += [C[k] == 12.5 + cp.sum(cp.multiply(np.array([G[h[1]]["bid"][ri] for h in H]), S[k]))
                     - cp.sum(A[k]) + cp.sum(RB[k]) - cp.sum(RR[k]) - SYN_IM * (A[k, lev_i] - S[k, lev_i])
                     + B[k] - 0.0]
            cons += [L[k] == RB[k] - RR[k]]
            cons += [U[k] == unf0 + PE_PLAN - PC[k]]
            Vpre_expr = Vpre
        else:
            p = idx[n["parent"]]
            R = np.array([holding_return(i, n, mu) for i in range(n_h)])
            dist = np.array([G[h[1]]["dist"][ri] for h in H])
            callr = np.array([G[h[1]]["call"][ri] for h in H])
            unf_share = np.array([h[3] for h in H]) / max(unf0, 1e-9)
            calls = cp.multiply(callr, unf_share) * U[p]                 # calls by holding (linear in U)
            Vpre_expr = cp.multiply(V[p], 1 + R) - cp.multiply(dist, V[p]) + calls
            spr = np.array([G[h[1]]["spr"][ri] for h in H])
            syn_pnl = V[p, lev_i] * (n["f"] - SYN_FIN[reg]) - V[p, lev_i] * 0.0   # VM on synthetic exposure
            cash_in = (C[p] * (1 + R_CASH) + cp.sum(cp.multiply(dist, V[p])) - cp.sum(calls) - draws[n["id"]]
                       - cp.sum(cp.multiply(R_CASH + spr, L[p])) - (R_CASH + REV_SPREAD) * B[p] + syn_pnl)
            if n["stage"] < YEARS:
                cons += [C[k] == cash_in + cp.sum(cp.multiply(np.array([G[h[1]]["bid"][ri] for h in H]), S[k]))
                         - cp.sum(A[k]) + cp.sum(RB[k]) - cp.sum(RR[k]) - SYN_IM * (A[k, lev_i] - S[k, lev_i])
                         + (B[k] - B[p])]
                cons += [L[k] == L[p] + RB[k] - RR[k]]
                cons += [U[k] == U[p] - cp.sum(calls) + PE_PLAN - PC[k]]
            else:
                cons += [C[k] == cash_in, L[k] == L[p], B[k] == B[p], U[k] == U[p] - cp.sum(calls)]
                cons += [S[k] == 0, A[k] == 0, RB[k] == 0, RR[k] == 0, PC[k] == 0]
        if n["stage"] < YEARS:
            cons += [V[k] == Vpre_expr - S[k] + A[k]]
            bid = np.array([G[h[1]]["bid"][ri] for h in H])
            depth = np.array([G[h[1]]["depth"][ri] for h in H])
            addcap = np.array([G[h[1]]["addcap"] for h in H])
            ltv = np.array([G[h[1]]["ltv"] for h in H])
            cons += [S[k] <= cp.multiply(depth, Vpre_expr), A[k] <= cp.multiply(addcap, Vpre_expr) + (np.arange(n_h) == lev_i) * 60.0,
                     L[k] <= cp.multiply(ltv, V[k]), PC[k] <= PE_PLAN]
            cons += [B[k] <= REV_AVAIL[reg] * REV_LIMIT]
            nav = cp.sum(V[k]) - V[k, lev_i] + C[k] - cp.sum(L[k]) - B[k]
            cons += [C[k] - SYN_IM * V[k, lev_i] >= CASH_FLOOR * nav_ref[n["id"]]]
            cons += [cp.sum(V[k]) <= LEV_CAP * nav]
            cons += [U[k] >= 0]
            # action families switched off
            if "SELL" not in allow:
                cons += [S[k, :lev_i] == 0] if True else []
                cons += [S[k, lev_i + 1:] == 0]
            if "ADD" not in allow:
                cons += [A[k, :lev_i] == 0, A[k, lev_i + 1:] == 0]
            if "REFI" not in allow:
                cons += [RB[k] == 0]
            if "LEVER" not in allow:
                cons += [A[k, lev_i] == 0]
            if "FUND" not in allow:
                cons += [B[k] == 0]
            if "PACE" not in allow:
                cons += [PC[k] == 0]
            if "SELL_LIQUID_ONLY" in allow:
                liq = {k2 for k2, h in enumerate(H) if h[1] in ("PUBLIC_LO", "PUBLIC_HF")}
                for i2 in range(n_h):
                    if i2 not in liq:
                        cons += [S[k, i2] == 0]
        else:
            cons += [V[k] == Vpre_expr]
    # terminal wealth with draws accrued (gross-of-distribution goal) and pacing franchise cost
    accr = {}
    for n in nodes:
        if n["parent"] is None:
            accr[n["id"]] = 0.0
    def path_draws(n):
        tot, m = 0.0, n
        while m["parent"] is not None:
            tot += draws[m["id"]] * (1.07 ** (YEARS - m["stage"]))
            m = nodes[m["parent"]]
        return tot
    def path_pace(n):
        terms, m = [], n
        while m is not None:
            if m["stage"] < YEARS:
                terms.append(PC[idx[m["id"]]])
            m = nodes[m["parent"]] if m["parent"] is not None else None
        return cp.sum(cp.hstack(terms)) if terms else 0
    Wt = []
    for lf in leaves:
        k = idx[lf["id"]]
        w = cp.sum(V[k]) - V[k, lev_i] + C[k] - cp.sum(L[k]) - B[k] + 0.9 * 0 - PACE_COST * path_pace(lf) - 0.02 * U[k]
        Wt.append((w + path_draws(lf)) / W0)
    Wt = cp.hstack(Wt)
    pl = np.array([lf["p"] for lf in leaves])
    pl = pl / pl.sum()
    # PWL CRRA(3) utility via tangents
    tang = np.linspace(0.75, 1.60, 12)
    u = cp.Variable(len(leaves))
    for x0 in tang:
        f0 = (x0 ** -2) / -2.0
        d0 = x0 ** -3
        cons += [u <= f0 + d0 * (Wt - x0)]
    eta = cp.Variable()
    z = cp.Variable(len(leaves), nonneg=True)
    if cvar_floor is not None:
        # CVaR10 of Wt >= floor: eta - (1/0.1) E[(eta - Wt)+] >= floor
        cons += [z >= eta - Wt, eta - (1 / 0.10) * (pl @ z) >= cvar_floor]
    obj = cp.Maximize(pl @ u) if mode == "crra" else cp.Maximize(pl @ Wt)
    prob = cp.Problem(obj, cons)
    t = time.time()
    prob.solve(solver=cp.HIGHS)
    return prob, dict(V=V, L=L, S=S, A=A, RB=RB, RR=RR, C=C, B=B, PC=PC, U=U, Wt=Wt, pl=pl, leaves=leaves,
                      draws=draws, nav_ref=nav_ref, time=time.time() - t, idx=idx, lev_i=lev_i)


def summarize(nodes, prob, v):
    if prob.status not in ("optimal", "optimal_inaccurate") or v["Wt"].value is None:
        return dict(status=prob.status, expected_ann=None, median_ann=None, p_goal=None, p_loss=None,
                    cvar10_ann=None, expected_w=None)
    Wt = np.asarray(v["Wt"].value).ravel()
    pl = v["pl"]
    order = np.argsort(Wt)
    cum = np.cumsum(pl[order])
    cvar_n = np.searchsorted(cum, 0.10) + 1
    tail = order[:cvar_n]
    ann = Wt ** (1 / YEARS) - 1
    return dict(status=prob.status, expected_ann=float(pl @ ann), median_ann=float(np.interp(0.5, cum, ann[order])),
                p_goal=float(pl[Wt >= GOAL].sum()), p_loss=float(pl[Wt < 1.0].sum()),
                cvar10_ann=float((np.average(Wt[tail], weights=pl[tail])) ** (1 / YEARS) - 1),
                expected_w=float(pl @ Wt))


def node_actions(nodes, v):
    out = {}
    lev_i = v["lev_i"]
    for n in nodes:
        if n["stage"] >= YEARS:
            continue
        k = v["idx"][n["id"]]
        acts = []
        borrowed = float(np.sum(v["RB"].value[k])) + max(0.0, float(v["B"].value[k] - (v["B"].value[v["idx"][n["parent"]]] if n["parent"] is not None else 0.0)))
        for i, h in enumerate(H):
            s, a, rb, rr = (float(v[x].value[k, i]) for x in ("S", "A", "RB", "RR"))
            if i == lev_i:
                if a > 0.05:
                    acts.append(dict(h=h[0], g=h[1], lens="LEVER", amt=a, why="adds equity exposure via futures (margin only)"))
                elif s > 0.05:
                    acts.append(dict(h=h[0], g=h[1], lens="SELL", amt=s, why="cuts synthetic exposure"))
                continue
            if s > 0.05:
                acts.append(dict(h=h[0], g=h[1], lens="SELL", amt=s, why=""))
            if a > 0.05:
                lens = "LEVER" if borrowed > 0.05 and h[1] not in ("PUBLIC_LO",) and a > 0.05 and borrowed > 0.05 else "ADD"
                acts.append(dict(h=h[0], g=h[1], lens="ADD" if lens == "ADD" else "ADD (debt-funded = LEVER)", amt=a, why=""))
            if rb > 0.05:
                acts.append(dict(h=h[0], g=h[1], lens="REFINANCE", amt=rb, why="cash-out borrowing against the holding"))
            if rr > 0.05:
                acts.append(dict(h=h[0], g=h[1], lens="REPAY", amt=rr, why=""))
        b_now = float(v["B"].value[k])
        b_prev = float(v["B"].value[v["idx"][n["parent"]]]) if n["parent"] is not None else 0.0
        if b_now - b_prev > 0.05:
            acts.append(dict(h="Revolver", g="CF", lens="FUND", amt=b_now - b_prev, why="Corporate Finance draws the committed line"))
        if b_prev - b_now > 0.05:
            acts.append(dict(h="Revolver", g="CF", lens="REPAY", amt=b_prev - b_now, why=""))
        pc = float(v["PC"].value[k])
        if pc > 0.05:
            acts.append(dict(h="PE commitments", g="PE", lens="PACE", amt=pc, why="cut planned new commitments"))
        out[n["id"]] = acts
    return out


def main():
    t0 = time.time()
    nodes = build_tree()
    mus, fusion = [], []
    for h in H:
        m, info = fuse(h)
        mus.append(m)
        fusion.append(dict(holding=h[0], group=h[1], value=h[2], underwritten=h[5], actual=h[6], forecast=h[7][1],
                           forecast_low=h[7][0], forecast_high=h[7][2], fused=round(m, 4), **info))
    mu = np.array(mus)
    floor = (0.97) ** YEARS      # CVaR10 floor: worst 10% average no worse than -3% a year (gross of draws)
    ALL = {"SELL", "ADD", "REFI", "LEVER", "FUND", "PACE"}
    runs = {}
    p_main, v_main = solve(nodes, mu, "crra", ALL, floor)
    runs["optimized_crra"] = summarize(nodes, p_main, v_main)
    p_goal, v_goal = solve(nodes, mu, "max_ew", ALL, floor)
    runs["goal_seeking"] = summarize(nodes, p_goal, v_goal)
    p_sq, v_sq = solve(nodes, mu, "crra", {"SELL_LIQUID_ONLY", "SELL"}, None)
    runs["status_quo_sell_liquid_only"] = summarize(nodes, p_sq, v_sq)
    ablation = {}
    for fam in ("SELL", "ADD", "REFI", "LEVER", "FUND", "PACE"):
        pa, va = solve(nodes, mu, "max_ew", ALL - {fam}, floor)
        ablation[fam] = summarize(nodes, pa, va)
    acts_goal = node_actions(nodes, v_goal)
    acts_main = node_actions(nodes, v_main)
    out_nodes = []
    for n in nodes:
        k = v_goal["idx"][n["id"]]
        rec = dict(id=n["id"], stage=n["stage"], regime=n["regime"], path=n["path"], parent=n["parent"],
                   children=n["children"], p=n["p"], bp=n["bp"], factor_return=n["f"],
                   owner_draw=v_goal["draws"][n["id"]],
                   cash=float(v_goal["C"].value[k]), revolver=float(v_goal["B"].value[k]),
                   loans=float(np.sum(v_goal["L"].value[k])),
                   nav=float(np.sum(v_goal["V"].value[k]) - v_goal["V"].value[k, v_goal["lev_i"]] + v_goal["C"].value[k]
                             - np.sum(v_goal["L"].value[k]) - v_goal["B"].value[k]),
                   synthetic=float(v_goal["V"].value[k, v_goal["lev_i"]]),
                   actions_goal=acts_goal.get(n["id"], []), actions_crra=acts_main.get(n["id"], []))
        if n["stage"] == YEARS:
            li = [lf["id"] for lf in v_goal["leaves"]].index(n["id"])
            rec["wealth_multiple_goal"] = float(np.asarray(v_goal["Wt"].value).ravel()[li])
            rec["wealth_multiple_crra"] = float(np.asarray(v_main["Wt"].value).ravel()[li])
        out_nodes.append(rec)
    res = dict(meta=dict(label="SYNTHETIC preview: illustrative parameters, not ADIC data, not a forecast",
                         tree="10 x 5 x 4 = 200 end-states; decisions at t0, t1, t2 (61 decision nodes); annual steps",
                         holdings=len(H), goal=f"10% a year for {YEARS} years, gross of distributions (draws accrued at 7%)",
                         cvar_floor="worst-10% average no worse than -3% a year", solver="HiGHS via cvxpy",
                         runtime_s=round(time.time() - t0, 1)),
               fusion=fusion, runs=runs, ablation_goal_seeking=ablation, nodes=out_nodes,
               groups=GROUP_LABEL)
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(dict(runs=runs, ablation={k: v["p_goal"] for k, v in ablation.items()},
                          runtime=res["meta"]["runtime_s"]), indent=1))


if __name__ == "__main__":
    main()
