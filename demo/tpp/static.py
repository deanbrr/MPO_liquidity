"""The static benchmark: a policy portfolio chosen once, then reached through Yale-model commitment pacing.

The first rung of the benchmark ladder (external research shared 2026-10-27): how a one-period framework sets the
plan. It sees five-year scenario returns per asset class and treats private assets as if they traded at NAV (an
index per strategy at its ER new-money return on the same factor paths: no calls, distributions, bids or J-curve,
tpp.paths.PathSet.private_index). The weights are held for five years with the owner's distribution taken pro rata
(the dollar draw on opening NAV, paid mid-year), so wealth is linear in the weights. On the same in-sample scenarios,
objective and world weights as the group's multi-period plan, it minimizes the expected plus the worst-10% dollar
shortfall against the target account (CRRA tie-break within the same tolerance), inside the limits a one-period model
can express: the reserve at least at its target, the IC ranges for the liquid sleeves (as in the multi-period model) and the
same band around today's weight of each private strategy, the overcommitment ceiling at today's unfunded per $ of
private NAV, and new term debt within today's leverage, recourse and term-debt caps. Nothing is dated and nothing
depends on the path; the balance-sheet guard at every year end, the forced-sale appetite and the depth guard have no
one-period form.

Implementation (what the framework does next): every liquid sleeve, the reserve included, takes its policy weight
pro rata on the liquid money there is (private assets cannot move to their weights today), within the IC ranges like
every plan's trades, the reserve never below its target; the annual rebalancing then works as for every plan. The PE
program runs as decided; each private strategy
commits a level amount a year, from the Yale model (tpp.yale, fitted to ADIC's DPI by vintage when a fit is given),
sized so that its projected NAV reaches its policy weight of the projected fund in year 5, within the pacing bands
and yearly caps. The simulator then certifies the plan on the same paths as every other plan.
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

from . import plan as planmod, yale
from .buckets import BY_ID, LIQUID_RISK, PRIVATE
from .lp import cvar_upper

RESERVE = "RESERVE"


def _views(S, settings: dict) -> np.ndarray:
    pis = settings.get("robust_pis")
    if not pis:
        return (S.prob / S.prob.sum())[None, :]
    out = []
    for pi in pis:
        pi = np.asarray(pi, float) / float(np.sum(pi))
        pk = pi[S.world] / S.n
        out.append(pk / pk.sum())
    return np.array(out)


def policy_portfolio(S, P, settings: dict, log=None) -> dict:
    """The one-period LP on the in-sample scenarios S (base case). settings: the house limits (lp_settings) plus
    risk_aversion and optional robust_pis, as for the multi-period model."""
    log = log or (lambda s: None)
    bk = S.book
    W0, g = float(bk.W0), float(bk.goal_rate)
    m = S.m
    p = S.prob / S.prob.sum()
    # ---- assets: liquid-risk sleeves, the reserve (cash + Treasury at today's split), private strategies held today
    priv0 = {b: 0.0 for b in PRIVATE}
    unf0 = 0.0
    for u in bk.units:
        priv0[u.bucket] += u.nav0
        unf0 += u.unf0
    res0 = float(bk.liquid.get("CASH", 0.0) + bk.liquid.get("TREASURY", 0.0))
    ts = float(bk.liquid.get("TREASURY", 0.0)) / max(res0, 1e-9)
    PR = [b for b in PRIVATE if priv0[b] > 1e-9]
    ids = list(LIQUID_RISK) + [RESERVE] + PR
    n = len(ids)
    w0 = np.array([bk.liquid.get(b, 0.0) / W0 for b in LIQUID_RISK] + [res0 / W0] + [priv0[b] / W0 for b in PR])
    ann = lambda G_: G_[:, 4::4] / G_[:, :-4:4]                                        # (m, 5) gross annual
    pidx = S.private_index()
    R = np.stack([ann(S.G[b]) for b in LIQUID_RISK]
                 + [ts * ann(S.G["TREASURY"]) + (1 - ts) * ann(S.G["CASH"])]
                 + [ann(pidx[b]) for b in PR], -1)                                     # (m, 5, n)
    r_term = float(S.rf_fin + float(P.get("corporate_finance.term_spread")))
    R = np.concatenate([R, np.full((m, 5, 1), 1.0 + r_term)], -1)                     # last column: new term debt
    d = np.asarray(S.draw, float)[:, :, None]
    c = R - d * np.sqrt(R)                                                             # pro-rata draw, mid-year
    cum = np.concatenate([np.ones((m, 1, n + 1)), np.cumprod(c, 1)], 1)                # (m, 6, n + 1) per $ today
    A10 = np.array([0.0] + [float(np.mean([(1 + g) ** (5 - (t - 1) - k / 4) for k in range(1, 5)])) for t in range(1, 6)])
    Aq = S.accrual()
    a = cum[:, 5] + sum(np.asarray(S.draw)[:, t - 1:t] * cum[:, t - 1] * A10[t] for t in range(1, 6))  # target acct
    bw = cum[:, 5] + sum(np.asarray(S.draw)[:, t - 1:t] * cum[:, t - 1] * Aq[:, t:t + 1] for t in range(1, 6))
    a[:, -1] *= -1.0                                                                   # debt enters with a minus
    bw[:, -1] *= -1.0
    # ---- limits a one-period model can express
    band = list(settings.get("range_band", P.get("constraints.range_band")))
    lo = np.zeros(n + 1)
    hi = np.zeros(n + 1)
    tot0 = float(sum(bk.liquid.get(b, 0.0) for b in LIQUID_RISK) + res0)
    xb = settings.get("x_bounds") or {}
    for i, b in enumerate(LIQUID_RISK):
        x0 = float(bk.liquid.get(b, 0.0))
        lo[i], hi[i] = (band[0] * x0, band[1] * x0) if x0 > 0 else (0.0, 0.05 * tot0)
        if b in xb:
            lo[i], hi[i] = xb[b]
        lo[i], hi[i] = lo[i] / W0, hi[i] / W0
    ft = float(settings.get("floor_target", P.get("liquidity.floor_target")))
    iR = len(LIQUID_RISK)
    lo[iR], hi[iR] = ft, 1.0
    for k, b in enumerate(PR):
        lo[iR + 1 + k], hi[iR + 1 + k] = band[0] * w0[iR + 1 + k], band[1] * w0[iR + 1 + k]
    lev_cap = float(settings.get("lev_cap", P.get("constraints.lev_cap")))
    rc = float(settings.get("recourse_cap", P.get("corporate_finance.recourse_cap")))
    beta0 = float(settings.get("beta0_bn", P.get("overlay.beta0_bn")))
    debt0 = float(bk.term0 + bk.revolver_drawn0)
    dmax = min((lev_cap - 1.0) * W0 - beta0 - debt0, rc * W0 - debt0, float(settings.get("new_term_max_bn", np.inf)))
    hi[n] = max(dmax, 0.0) / W0 if settings.get("allow_debt", True) else 0.0
    ovc = float(settings.get("overcommit", P.get("constraints.overcommit")))
    pnav0 = float(sum(priv0.values()))
    priv_cap = ovc * pnav0 / max(pnav0 + unf0, 1e-9)                                   # at today's unfunded per $ NAV
    # ---- variables: x = [w (n), delta, S (m), TT, eta (K), z (K m)]; then UT (m) for the tie-break
    V = _views(S, settings)
    K = len(V)
    alpha = float(P.get("objective.shortfall_alpha"))
    nw = n + 1
    iS, iT, iE, iZ = nw, nw + m, nw + m + 1, nw + m + 1 + K
    nx = iZ + K * m
    rows, rhs = [], []                                       # A_ub x <= b_ub, as (coo triplets)
    ri, ci, vi = [], [], []

    def add(cols, vals, b):
        r = len(rhs)
        ri.extend([r] * len(cols))
        ci.extend(cols)
        vi.extend(vals)
        rhs.append(b)

    target = (1.0 + g) ** 5
    W_idx = list(range(nw))
    for j in range(m):                                       # S_j >= target - a_j . w   <=>  -S_j - a_j . w <= -target
        add([iS + j] + W_idx, [-1.0] + (-a[j]).tolist(), -target)
    for k in range(K):
        for j in range(m):                                   # z_kj >= S_j - eta_k
            add([iZ + k * m + j, iS + j, iE + k], [-1.0, 1.0, -1.0], 0.0)
        cols = [iT, iE + k] + [iS + j for j in range(m)] + [iZ + k * m + j for j in range(m)]
        vals = [-1.0, 1.0] + V[k].tolist() + (V[k] / alpha).tolist()
        add(cols, vals, 0.0)                                 # TT >= E_k S + eta_k + E_k z_k / alpha
    priv_cols = list(range(iR + 1, n))
    add(priv_cols, [1.0] * len(priv_cols), priv_cap)
    A_ub = sp.csr_matrix((vi, (ri, ci)), shape=(len(rhs), nx))
    b_ub = np.array(rhs)
    A_eq = sp.csr_matrix(([1.0] * n + [-1.0], ([0] * nw, list(range(nw)))), shape=(1, nx))
    b_eq = np.array([1.0])
    bounds = [(lo[i], hi[i]) for i in range(nw)] + [(0, None)] * m + [(None, None)] * (1 + K) + [(0, None)] * (K * m)
    cost = np.zeros(nx)
    cost[iT] = 1.0
    r1 = linprog(cost, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if r1.status != 0:
        return {"ok": False, "message": r1.message}
    tstar = float(r1.x[iT])
    # ---- CRRA tie-break among policies within the tolerance of the minimum
    gam = float(settings.get("risk_aversion", 3.0))
    wk = np.geomspace(*P.get("objective.crra_w_range"), int(P.get("objective.crra_tangents")))
    Uf = (lambda w_: np.log(w_)) if abs(gam - 1) < 1e-9 else (lambda w_: w_ ** (1 - gam) / (1 - gam))
    Ud = lambda w_: w_ ** (-gam)
    nx2 = nx + m
    ri2, ci2, vi2 = list(ri), list(ci), list(vi)
    rhs2 = list(rhs)
    for wv in wk:                                            # UT_j <= U(w) + U'(w) (WT_j / W0 - w)
        base = len(rhs2)
        for j in range(m):
            ri2.extend([base + j] * (nw + 1))
            ci2.extend([nx + j] + W_idx)
            vi2.extend([1.0] + (-Ud(wv) * bw[j]).tolist())
            rhs2.append(Uf(wv) - Ud(wv) * wv)
    A2 = sp.csr_matrix((vi2, (ri2, ci2)), shape=(len(rhs2), nx2))
    rel = float(P.get("objective.shortfall_tiebreak_rel"))
    bounds2 = list(bounds)
    bounds2[iT] = (None, tstar * (1 + rel) + 1e-9)
    bounds2 += [(None, None)] * m
    cost2 = np.zeros(nx2)
    cost2[nx:] = -p
    A_eq2 = sp.hstack([A_eq, sp.csr_matrix((1, m))]).tocsr()
    r2 = linprog(cost2, A_ub=A2, b_ub=np.array(rhs2), A_eq=A_eq2, b_eq=b_eq, bounds=bounds2, method="highs")
    x = r2.x[:nx] if r2.status == 0 else r1.x
    w = x[:nw]
    sh = np.maximum(target - a @ w, 0.0) * W0                                          # $bn per scenario
    nav = np.einsum("mtk,k->mt", cum, w * np.r_[np.ones(n), -1.0]) * W0                # (m, 6)
    # what the one-period model believes: its own five-year TWR (modified Dietz, gross of the draws, as the simulator)
    D = np.asarray(S.draw, float) * nav[:, :5]
    r_y = (nav[:, 1:] - nav[:, :-1] + D) / np.maximum(nav[:, :-1] - 0.5 * D, 1e-9)
    twr = np.exp(np.log1p(np.maximum(r_y, -0.99)).mean(1)) - 1.0
    log(f"   static policy portfolio: shortfall measure {tstar * W0:.1f}bn in sample, private weight "
        f"{w[iR + 1:n].sum():.3f} (today {w0[iR + 1:].sum():.3f}), reserve {w[iR]:.3f}, new debt {w[n] * W0:.1f}bn")
    return {"ok": True, "ids": ids, "w": {b: float(w[i]) for i, b in enumerate(ids)}, "debt_bn": float(w[n] * W0),
            "w0": {b: float(w0[i]) for i, b in enumerate(ids)}, "lo": lo[:n].tolist(), "hi": hi[:n].tolist(),
            "priv_cap": float(priv_cap), "private_w": float(w[iR + 1:n].sum()), "private_w0": float(w0[iR + 1:].sum()),
            "reserve_w": float(w[iR]), "treasury_share": ts,
            "nav_mean_bn": [float(p @ nav[:, t]) for t in range(6)],
            "in_sample": {"short_mean_bn": float(p @ sh), "short_cvar10_bn": float(cvar_upper(sh, alpha, p)),
                          "measure_bn": tstar * W0, "p_target_acct": float(p @ (sh <= 1e-9)),
                          "twr_mean": float(p @ twr), "p_goal": float(p @ (twr >= g - 1e-12))},
            "tiebreak": r2.status == 0}


def yale_pacing(book, P, pol: dict, program: dict, fam: dict, settings: dict) -> dict:
    """Level annual commitments per private strategy so that the Yale model's projected NAV in year 5 (existing
    cohorts less the PE program's sales, plus five years of commitments) reaches the policy weight of the projected
    fund (the static model's own expected NAV in year 5); within the pacing bands and the yearly caps."""
    br = book.bucket_ret
    nav5 = float(pol["nav_mean_bn"][5])
    ex5 = {b: 0.0 for b in PRIVATE}
    for u in book.units:
        f = yale.params(fam, u.bucket, br.loc[u.bucket, "new_Base"])
        keep = 1.0 - float(sum(program.get(u.id, [0.0, 0.0, 0.0])))
        ex5[u.bucket] += keep * sum(yale.cohort_nav(f, c["nav"], c["unf"], c["age"], 5) for c in u.cohorts)
    mult = list(settings.get("pace_mult", P.get("pacing.mult_range")))
    entry = float(settings.get("new_strategy_entry_bn", 0.3))
    out, rows = {}, []
    for b in PRIVATE:
        f = yale.params(fam, b, br.loc[b, "new_Base"])
        nav_curve = yale.fund_curve(f, 5)["nav"]
        per_dollar = sum(nav_curve[5 - tau] for tau in range(5))                       # $1 a year for five years
        tgt = float(pol["w"].get(b, 0.0)) * nav5
        pace = float(book.pacing_sq.get(b, 0.0))
        raw = max(tgt - ex5[b], 0.0) / max(per_dollar, 1e-9)
        c_ = float(np.clip(raw, mult[0] * pace, mult[1] * pace + (entry if tgt > 0 else 0.0)))
        out[b] = c_
        rows.append({"bucket": b, "label": BY_ID[b].label, "fund": BY_ID[b].is_fund, "target_nav5_bn": tgt,
                     "existing_nav5_bn": ex5[b], "per_dollar_nav5": per_dollar, "raw_bn": raw, "commit_bn": c_,
                     "pace_sq_bn": pace})
    # yearly caps (as the multi-period model): fund commitments and co-invest deployments, scaled pro rata
    agg = float(settings.get("commit_agg_mult", 1.25))
    co_extra = float(settings.get("coinvest_extra_bn", P.get("trading.buy_cap_year_bn")["COINVEST"]))
    for is_fund, cap in ((True, agg * sum(book.pacing_sq.get(b, 0.0) for b in PRIVATE if BY_ID[b].is_fund)),
                         (False, sum(book.pacing_sq.get(b, 0.0) for b in PRIVATE if not BY_ID[b].is_fund) + co_extra)):
        tot = sum(v for b, v in out.items() if BY_ID[b].is_fund == is_fund)
        if tot > cap > 0:
            for b in out:
                if BY_ID[b].is_fund == is_fund:
                    out[b] *= cap / tot
    for r in rows:
        r["commit_bn"] = out[r["bucket"]]
    return {"commit": {b: [v] * 5 for b, v in out.items()}, "rows": rows, "nav5_bn": nav5}


def static_plan(S, P, settings: dict, fam: dict, name: str = "Static: policy portfolio + Yale pacing", log=None) -> dict:
    """The static benchmark plan on the in-sample scenarios S: the policy portfolio, the Yale pacing, and the plan
    the simulator certifies (today's trades to the policy weights, the PE program as decided, level commitments)."""
    bk = S.book
    pol = policy_portfolio(S, P, settings, log)
    if not pol["ok"]:
        return {"ok": False, "message": pol["message"]}
    program = planmod.program_fractions(bk, P, settings)
    pace = yale_pacing(bk, P, pol, program, fam, settings)
    W0 = float(bk.W0)
    uid = [u.id for u in bk.units]
    p0 = sum(float(fr[0]) * bk.units[uid.index(u_)].nav0 * float(S.ubid[0, 0, uid.index(u_)]) for u_, fr in program.items())
    deploy0 = sum(v[0] for b, v in pace["commit"].items() if not BY_ID[b].is_fund)
    # private assets cannot move to their policy weights today, so every liquid sleeve (the reserve included) takes
    # its policy weight pro rata on the liquid money there is (the usual treatment of an illiquid over- or
    # underweight), the reserve never below its target and every sleeve inside its IC range
    liquid_now = float(sum(bk.liquid.get(b, 0.0) for b in LIQUID_RISK) + bk.liquid.get("CASH", 0.0)
                       + bk.liquid.get("TREASURY", 0.0))
    avail = max(liquid_now + p0 + pol["debt_bn"] - deploy0, 0.0)
    wl = {b: pol["w"][b] for b in LIQUID_RISK}
    sw = max(sum(wl.values()), 1e-12)
    ft = float(settings.get("floor_target", P.get("liquidity.floor_target")))
    res_t = min(max(avail * pol["reserve_w"] / max(sw + pol["reserve_w"], 1e-12), ft * W0), avail)
    # the trades today stay inside the IC ranges, as for every plan; the reserve takes what is left
    rng = {b: (pol["lo"][i] * W0, pol["hi"][i] * W0) for i, b in enumerate(pol["ids"]) if b in wl}
    liquid = {b: float(np.clip((avail - res_t) * wl[b] / sw, *rng[b])) for b in LIQUID_RISK}
    short = ft * W0 - (avail - sum(liquid.values()))
    room = sum(liquid[b] - rng[b][0] for b in liquid)
    if short > 0 and room > 0:                                # the reserve's target first, then the ranges' floors
        f = min(short / room, 1.0)
        liquid = {b: x - f * (x - rng[b][0]) for b, x in liquid.items()}
    res_t = avail - sum(liquid.values())
    ts = pol["treasury_share"]
    plan = planmod.Plan(name=name, sell=program, liquid=liquid,
                        cash=res_t * (1 - ts), treasury=res_t * ts, commit=pace["commit"], term_bn=pol["debt_bn"],
                        term_sched=[pol["debt_bn"], 0.0, 0.0], navf_bn=0.0, rev_upsize_bn=0.0,
                        beta_bn=float(settings.get("beta0_bn", P.get("overlay.beta0_bn"))),
                        meta={"kind": "static", "program": bool(program)})
    return {"ok": True, "plan": plan, "policy": pol, "pacing": pace, "program_proceeds0_bn": p0, "deploy0_bn": deploy0}
