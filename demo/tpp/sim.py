"""Component 4: the exact quarterly simulator (out-of-sample certification of any plan).

Every plan (status quo, each stakeholder's optimized plan, an IC amendment) runs on the same paths (common random
numbers) through one ledger. Each quarter:
  1. liquid buckets, the reserve and every private unit and template earn that path's returns;
  2. private distributions come in; capital calls (on today's unfunded and on new commitments) go out; the owner
     draw is paid quarterly at the year's rate on the opening NAV; debt interest, the revolver's undrawn fee, the
     overlay's variation margin and any change in initial margin settle; the NAV facility accrues PIK;
  3. if cash is negative the Treasury sleeve covers it; if the reserve (cash + Treasury) is below the hard floor,
     the Liquidity group's waterfall restores it: liquid sales in order (hedge funds only up to the quarterly gate
     for the state), then the revolver (availability by state), then forced secondary sales of private holdings
     pro rata at the stressed bid less a distressed-seller discount (a red event above the threshold).
At the start of each year: planned private sales execute at that year's realized bid (the buyer takes the
unfunded), the year's commitments are made (co-investments deploy at once), the NAV-facility LTV covenant is
tested (a breach forces repayment), surplus reserve repays the revolver and is rebalanced into the liquid-risk
targets, and a reserve below its target is topped up from liquid sales (never by borrowing).
Returns are annual modified-Dietz time-weighted returns, gross of owner distributions; the goal is met when the
five-year annualized TWR reaches the hurdle.
"""
from __future__ import annotations

import numpy as np

from .buckets import BY_ID, LIQUID_RISK
from .plan import Plan, beta_paths, schedule_paths

NQ = 20


def _settings(P, st: dict | None) -> dict:
    st = dict(st or {})
    g = lambda k, d: st.get(k, d)
    return {
        "floor_hard": float(g("floor_hard", P.get("liquidity.floor_hard"))),
        "floor_target": float(g("floor_target", P.get("liquidity.floor_target"))),
        "waterfall": list(g("waterfall", P.get("liquidity.waterfall"))),
        "hf_liq": list(g("hf_quarterly_liquidity", P.get("liquidity.hf_quarterly_liquidity"))),
        "forced_disc": float(g("forced_sale_extra_discount", P.get("liquidity.forced_sale_extra_discount"))),
        "red_thr": float(P.get("liquidity.red_event_threshold_bn")),
        "rev_signed": float(g("revolver_signed_bn", P.get("corporate_finance.revolver_signed_bn"))),
        "rev_drawn0": float(g("revolver_drawn0_bn", P.get("corporate_finance.revolver_drawn0_bn"))),
        "rev_avail": list(g("revolver_avail", P.get("corporate_finance.revolver_avail"))),
        "rev_spread": float(P.get("corporate_finance.revolver_spread")),
        "rev_fee": float(P.get("corporate_finance.revolver_undrawn_fee")),
        "term0": float(g("term_debt0_bn", P.get("corporate_finance.term_debt0_bn"))),
        "term_spread": float(P.get("corporate_finance.term_spread")),
        "navf_spread": float(P.get("corporate_finance.navf_spread")),
        "navf_oid": float(P.get("corporate_finance.navf_oid")),
        "navf_ltv_max": float(g("navf_ltv_max", P.get("corporate_finance.navf_ltv_max"))),
        "navf_ltv_stress": float(g("navf_ltv_stress", P.get("corporate_finance.navf_ltv_stress"))),
        "beta_spread": list(P.get("overlay.beta_fin_spread")),
        "im_rate": list(P.get("overlay.im_rate")),
        "tc": float(P.get("trading.tc_liquid")),
        "maintain_target": bool(g("maintain_target", True)),
        "rebalance": bool(g("rebalance", True)),
        "goal": float(g("goal_rate", P.get("goal.rate"))),
    }


def simulate(S, plan: Plan, P, settings: dict | None = None, keep_paths: bool = False) -> dict:
    cfg = _settings(P, settings)
    if S.shock["hf_liq"] is not None:
        cfg["hf_liq"] = list(S.shock["hf_liq"])
    book = S.book
    m, K = S.m, len(book.units)
    T = len(S.tpl_buckets)
    rf = S.rf_fin
    uid = [u.id for u in book.units]
    # per-path schedules: a state-contingent plan's later decisions follow each path's observed market state
    sell, amt, sched = schedule_paths(plan, uid, list(S.tpl_buckets), S.cls_y)
    is_fund = S.tpl_is_fund
    LR = [b for b in cfg["waterfall"] if b in LIQUID_RISK] + [b for b in LIQUID_RISK if b not in cfg["waterfall"]]
    pledge_u = np.array([BY_ID[u.bucket].is_fund for u in book.units], float)
    pledge_t = is_fund.astype(float)
    hf_liq = np.asarray(cfg["hf_liq"], float)
    rev_av = np.asarray(cfg["rev_avail"], float)
    im_rate = np.asarray(cfg["im_rate"], float)
    bsp = np.asarray(cfg["beta_spread"], float)
    # ---------------- state
    keep = np.ones((m, K))
    tkeep = np.ones((m, 5, T))
    L = {b: np.full(m, float(book.liquid.get(b, 0.0))) for b in LIQUID_RISK}
    cash = np.full(m, float(book.liquid.get("CASH", 0.0)))
    tre = np.full(m, float(book.liquid.get("TREASURY", 0.0)))
    rev = np.full(m, cfg["rev_drawn0"])
    term = cfg["term0"] + sched[0]
    navf = np.full(m, float(plan.navf_bn))
    rev_cap = cfg["rev_signed"] + float(plan.rev_upsize_bn)
    beta_y = beta_paths(plan, S.cls_y)                                              # (5, m): year t+1's beta
    beta = beta_y[0]
    IM = np.zeros(m)
    # ---------------- records
    rec = {k: np.zeros((m, 6)) for k in ("nav", "reserve", "lr", "priv", "unf", "debt", "lev", "ovc", "rev")}
    yr = {k: np.zeros((m, 5)) for k in ("draw", "dist", "calls", "interest", "forced", "lr_sold", "rev_draw",
                                         "sales", "vm", "lcr", "net_private", "deploy")}
    forced_q = np.zeros((m, NQ))
    rev_max = np.zeros(m)
    min_res_ratio = np.full(m, np.inf)
    nav_start = np.zeros(m)
    dq = np.zeros(m)

    def tpl_level(t_idx):
        """Value and unfunded of all templates at year end t_idx (sum over start years <= t_idx)."""
        v = np.zeros(m)
        uu = np.zeros(m)
        pv = np.zeros(m)
        for tau in range(min(t_idx, 4) + 1):
            w = tkeep[:, tau, :] * amt[tau]
            v += (w * S.tV[tau, :, t_idx, :]).sum(1)
            uu += (w * S.tU[tau, :, t_idx, :]).sum(1)
            pv += (w * S.tV[tau, :, t_idx, :] * pledge_t[None, :]).sum(1)
        return v, uu, pv

    def private_level(t_idx):
        v = (keep * S.uV[:, 4 * t_idx, :]).sum(1)
        uu = (keep * S.uU[:, 4 * t_idx, :]).sum(1)
        pv = (keep * S.uV[:, 4 * t_idx, :] * pledge_u[None, :]).sum(1)
        tv, tu, tpv = tpl_level(t_idx)
        return v + tv, uu + tu, pv + tpv

    def nav_now(t_idx):
        pv, _, _ = private_level(t_idx)
        lr = sum(L[b] for b in LIQUID_RISK)
        return cash + tre + lr + pv + IM - rev - term - navf

    def sell_lr(need, order, qidx, gate=True):
        """Sell liquid-risk buckets in order to raise `need` (m,), at 1 - tc. Returns cash raised (m,)."""
        raised = np.zeros(m)
        for b in order:
            if not np.any(need > 1e-12):
                break
            avail = L[b] * (1 - cfg["tc"])
            if b == "HF" and gate:
                avail = avail * hf_liq[S.cls_q[:, qidx]]
            take = np.clip(need, 0.0, avail)
            L[b] = L[b] - take / (1 - cfg["tc"])
            raised += take
            need = need - take
        return raised

    def forced_sale(need, qidx, t_idx):
        """Forced pro-rata sale of private units and templates at the stressed bid less the extra discount."""
        nonlocal keep, tkeep
        if not np.any(need > 1e-12):
            return np.zeros(m), np.zeros(m)
        st = S.cls_q[:, qidx]
        tau = min(t_idx, 2)
        uval = keep * S.uV[:, qidx + 1, :]
        upx = S.unit_bid_state[:, tau, :][:, st].T                                 # (m, K)
        tval = np.zeros((m, 5, T))
        for k in range(min(t_idx, 4) + 1):
            tval[:, k, :] = tkeep[:, k, :] * amt[k] * S.tV[k, :, min(t_idx, 5), :]
        tpx = S.tpl_bid_state[:, :][:, st].T                                       # (m, T)
        val_tot = uval.sum(1) + tval.sum((1, 2))
        proceeds_cap = ((uval * upx).sum(1) + (tval * tpx[:, None, :]).sum((1, 2))) * (1 - cfg["forced_disc"])
        share = np.clip(np.divide(np.minimum(need, proceeds_cap), np.maximum(proceeds_cap, 1e-12)), 0.0, 1.0)
        share = np.where(proceeds_cap > 1e-12, share, 0.0)
        keep = keep * (1 - share[:, None])
        tkeep = tkeep * (1 - share[:, None, None])
        return share * proceeds_cap, share * val_tot

    # ---------------- t0: planned sales at today's bid, trades to the plan's targets, new debt
    p0 = (sell[0] * S.uV[:, 0, :] * S.ubid[:, 0, :]).sum(1)
    yr["sales"][:, 0] += p0
    keep = keep - sell[0]
    budget = cash + tre + sum(L[b] for b in LIQUID_RISK) + p0 + term - cfg["term0"] + navf * (1 - cfg["navf_oid"])
    tc_cost = sum(abs(float(plan.liquid.get(b, 0.0)) - float(book.liquid.get(b, 0.0))) for b in LIQUID_RISK) * cfg["tc"]
    for b in LIQUID_RISK:
        L[b] = np.full(m, float(plan.liquid.get(b, 0.0)))
    tre = np.full(m, float(plan.treasury))
    cash = budget - tc_cost - tre - sum(L[b] for b in LIQUID_RISK)
    targets = {b: float(plan.liquid.get(b, 0.0)) for b in LIQUID_RISK}
    tsum = sum(targets.values())
    # ---------------- quarters
    for q in range(NQ):
        t = q // 4
        if q % 4 == 0:
            beta = beta_y[t]                                                        # this year's synthetic beta
            if t > 0:
                # year-end housekeeping for year t-1 (records at year end t)
                nv = nav_now(t)
                st_y = S.cls_y[:, t]
                # NAV-facility covenant
                _, _, pool = private_level(t)
                cap_ltv = np.where(st_y == 2, cfg["navf_ltv_stress"], cfg["navf_ltv_max"])
                excess = np.maximum(navf - cap_ltv * pool, 0.0)
                cash = cash - excess
                navf = navf - excess
                # revolver repayment from reserve above target
                surplus = cash + tre - cfg["floor_target"] * nv
                pay = np.clip(surplus, 0.0, rev)
                cash -= pay
                rev -= pay
                # rebalance surplus into the liquid-risk targets, or top up the reserve from liquid sales
                surplus = cash + tre - cfg["floor_target"] * nv
                if cfg["rebalance"] and tsum > 1e-9:
                    inv = np.maximum(surplus, 0.0) * (rev <= 1e-9)
                    for b in LIQUID_RISK:
                        L[b] = L[b] + inv * targets[b] / tsum * (1 - cfg["tc"])
                    cash -= inv
                if cfg["maintain_target"]:
                    need = np.maximum(-surplus, 0.0)
                    got = sell_lr(need, LR, q, gate=True)
                    cash += got
                    yr["lr_sold"][:, t - 1] += got
                # planned term-debt draw for this year
                if t <= 2 and sched[t].any():
                    term = term + sched[t]
                    cash = cash + sched[t]
                # planned sales at this year's bid
                if t <= 2 and sell[t].any():
                    frac = np.minimum(sell[t], keep)
                    proceeds = (frac * S.uV[:, 4 * t, :] * S.ubid[:, t, :]).sum(1)
                    keep = keep - frac
                    cash += proceeds
                    yr["sales"][:, t] += proceeds
            # this year's deployments (co-invest buckets pay at once; fund commitments create unfunded)
            dep = (amt[t] * (~is_fund)[None, :]).sum(1)
            cash = cash - dep
            yr["deploy"][:, t] += dep
            nav_start = nav_now(t)
            if t == 0:
                rec_t0 = nav_start.copy()
            dq = S.draw[:, t] * nav_start / 4
            # liquidity coverage at the start of the year
            lr_now = sum(L[b] * (hf_liq[S.cls_q[:, q]] * 4 if b == "HF" else 1.0) for b in LIQUID_RISK)
            src = cash + tre + lr_now + np.maximum(rev_cap * rev_av[S.cls_y[:, t]] - rev, 0.0)
            yr["lcr"][:, t] = src            # divided by the year's uses after the year
            # records at year start t
            pv, uu, _ = private_level(t)
            rec["nav"][:, t] = nav_start
            rec["reserve"][:, t] = cash + tre
            rec["lr"][:, t] = sum(L[b] for b in LIQUID_RISK)
            rec["priv"][:, t] = pv
            rec["unf"][:, t] = uu
            rec["debt"][:, t] = rev + term + navf
            rec["rev"][:, t] = rev
            rec["lev"][:, t] = (nav_start + rev + term + navf + beta) / np.maximum(nav_start, 1e-9)
            rec["ovc"][:, t] = (pv + uu) / np.maximum(nav_start, 1e-9)
        # -------- quarter flows
        for b in LIQUID_RISK:
            L[b] = L[b] * np.exp(S.rq[b][:, q])
        tre = tre * np.exp(S.rq["TREASURY"][:, q])
        cash = cash * np.exp(S.rq["CASH"][:, q])
        dist = (keep * S.uD[:, q, :]).sum(1)
        calls = (keep * S.uC[:, q, :]).sum(1)
        for tau in range(t + 1):
            w = tkeep[:, tau, :] * amt[tau]
            dist += (w * S.tD[tau, :, q, :]).sum(1)
            calls += (w * S.tC[tau, :, q, :]).sum(1)
        interest = (term * (rf + cfg["term_spread"]) + rev * (rf + cfg["rev_spread"])
                    + cfg["rev_fee"] * np.maximum(rev_cap - rev, 0.0)) / 4
        navf = navf * np.exp((rf + cfg["navf_spread"]) / 4)
        stq = S.cls_q[:, q]
        vm = beta * (S.eq_excess_q[:, q] - bsp[stq] / 4)
        im_new = im_rate[stq] * beta
        dIM = im_new - IM
        IM = im_new
        cash = cash + dist - calls - dq - interest + vm - dIM
        yr["draw"][:, t] += dq
        yr["dist"][:, t] += dist
        yr["calls"][:, t] += calls
        yr["interest"][:, t] += interest
        yr["vm"][:, t] += vm
        # Treasury covers negative cash
        cover = np.clip(-cash, 0.0, tre)
        tre -= cover
        cash += cover
        # waterfall to the hard floor
        need = np.maximum(cfg["floor_hard"] * nav_start - (cash + tre), 0.0)
        for src_name in cfg["waterfall"]:
            if not np.any(need > 1e-9):
                break
            if src_name in LIQUID_RISK:
                got = sell_lr(need, [src_name], q, gate=True)
                yr["lr_sold"][:, t] += got
            elif src_name == "REVOLVER":
                head = np.maximum(rev_cap * rev_av[stq] - rev, 0.0)
                got = np.clip(need, 0.0, head)
                rev = rev + got
                yr["rev_draw"][:, t] += got
            elif src_name == "FORCED":
                got, navsold = forced_sale(need, q, t)
                forced_q[:, q] += navsold
                yr["forced"][:, t] += navsold
            else:
                continue
            cash = cash + got
            need = need - got
        rev_max = np.maximum(rev_max, rev)
        min_res_ratio = np.minimum(min_res_ratio, (cash + tre) / np.maximum(nav_start, 1e-9))
    # ---------------- final year end
    nv5 = nav_now(5)
    pv, uu, _ = private_level(5)
    rec["nav"][:, 5] = nv5
    rec["reserve"][:, 5] = cash + tre
    rec["lr"][:, 5] = sum(L[b] for b in LIQUID_RISK)
    rec["priv"][:, 5] = pv
    rec["unf"][:, 5] = uu
    rec["debt"][:, 5] = rev + term + navf
    rec["rev"][:, 5] = rev
    rec["lev"][:, 5] = (nv5 + rev + term + navf + beta) / np.maximum(nv5, 1e-9)
    rec["ovc"][:, 5] = (pv + uu) / np.maximum(nv5, 1e-9)
    # ---------------- returns (modified Dietz per year, gross of owner draws). Year 1 starts from today's NAV
    # BEFORE the plan's trades, so t0 sale discounts, trading costs and fees count against the plan.
    rec["nav"][:, 0] = book.W0
    nav = rec["nav"]
    D = yr["draw"]
    r = (nav[:, 1:] - nav[:, :-1] + D) / np.maximum(nav[:, :-1] - 0.5 * D, 1e-9)
    r = np.maximum(r, -0.99)
    twr = np.exp(np.log1p(r).mean(1)) - 1.0
    uses = D + yr["calls"] + yr["interest"]
    lcr = yr["lcr"] / np.maximum(uses, 1e-9)
    W0 = book.W0
    out = {
        "plan": plan.name, "m": m, "prob": S.prob, "world": S.world,
        "twr": twr, "ret": r, "goal": twr >= cfg["goal"] - 1e-12,
        "red": forced_q.sum(1) * 1.0 > cfg["red_thr"], "forced_total": forced_q.sum(1),
        "rev_max": rev_max, "rev_used": rev_max > 1e-6, "min_reserve_ratio": min_res_ratio,
        "lcr": lcr, "nav0_post": rec_t0, "W0": W0, "macro_y": S.macro_y, "exit_y": S.exit_y,
        "cls_y": S.cls_y,
        "wealth": W0 * (1 + twr) ** 5,
        **{f"y_{k}": v for k, v in yr.items() if k != "lcr"},
        **{f"r_{k}": v for k, v in rec.items()},
    }
    return out
