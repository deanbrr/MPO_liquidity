"""Asset substitution: the plan's change list, LEVER / REFINANCE labels, and holding-level cards.

Change list: every difference between a plan and the status quo, dated (secondary sales by unit and tranche with
NAV, unfunded transferred and expected proceeds; liquid trades; reserve; commitments by strategy and year; term
debt, NAV facility and synthetic beta). R1 (examples/mpo_v2, user definitions): new financing dB is LEVER up to the
discretionary exposure it adds, dE, and REFINANCE beyond (cash raised against holdings without adding exposure):
    LEVER = min(dB+, dE+),  REFINANCE = dB+ - LEVER.

Holding cards. The LP prices each unit: p*_k, the value of holding $1 of the unit's NAV in today's dollars, read
from the LP's own duals (tpp.lp.TPPModel.duals), so a card agrees with the optimizer in sign. A holding's own value
adjusts for its forward return against its unit's over its remaining duration:
    p*_i = p*_k x exp((CE_i - CE_k) x min(D_i, 6))
    SELL       bid_i > p*_i (the secondary bid beats the hold value)
    REFINANCE  hold, fund interest aged 3-10 with NAV >= $50m, CE_i above the NAV facility's all-in cost: raise
               liquidity against it instead of selling it
    LEVER      hold, co-investment / direct or GP-led, CE_i at least 2pp above the hurdle and 4pp above asset-level
               financing: a candidate to add exposure financed with debt
    HOLD       otherwise
Alternatives: new-money ER buckets ranked by the stakeholder's certainty-equivalent return.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .buckets import BY_ID, LIQUID_RISK, PRIVATE
from .returns import WORLDS, ce


def change_list(book, plan, sq, S=None) -> dict:
    units = {u.id: u for u in book.units}
    sells = []
    for uid, fr in plan.sell.items():
        u = units[uid]
        k = [x.id for x in book.units].index(uid)
        for tau, f in enumerate(fr):
            if f <= 1e-6:
                continue
            if S is not None:
                p = S.prob / S.prob.sum()
                proceeds = float(p @ (f * S.uV[:, 4 * tau, k] * S.ubid[:, tau, k]))
                navv = float(p @ (f * S.uV[:, 4 * tau, k]))
            else:
                proceeds, navv = f * u.nav0 * u.bidfac[tau], f * u.nav0
            sells.append({"unit": uid, "bucket": u.bucket, "label": BY_ID[u.bucket].label, "part": u.part,
                          "department": BY_ID[u.bucket].department, "tranche": tau + 1, "fraction": f,
                          "nav_bn": f * u.nav0, "unfunded_bn": f * u.unf0, "exposure_bn": f * u.exposure0,
                          "expected_nav_at_sale_bn": navv, "expected_proceeds_bn": proceeds,
                          "discount_bn": navv - proceeds, "pe_program": u.pe_program})
    liquid = []
    for b in LIQUID_RISK:
        a, z = float(sq.liquid.get(b, 0.0)), float(plan.liquid.get(b, 0.0))
        if abs(z - a) > 1e-3:
            liquid.append({"bucket": b, "label": BY_ID[b].label, "from_bn": a, "to_bn": z, "change_bn": z - a,
                           "lens": "ADD" if z > a else "SELL"})
    res_sq, res_pl = sq.cash + sq.treasury, plan.cash + plan.treasury
    commits = []
    for b in PRIVATE:
        a = np.asarray(sq.commit.get(b, [0.0] * 5), float)
        z = np.asarray(plan.commit.get(b, [0.0] * 5), float)
        if np.abs(z - a).sum() > 1e-3:
            commits.append({"bucket": b, "label": BY_ID[b].label, "fund": BY_ID[b].is_fund,
                            "sq_by_year": a.tolist(), "plan_by_year": z.tolist(), "change_5y_bn": float((z - a).sum()),
                            "lens": (("PACE UP" if (z - a).sum() >= 0 else "PACE DOWN") if BY_ID[b].is_fund
                                     else ("ADD" if (z - a).sum() >= 0 else "CUT"))})
    sched = list(getattr(plan, "term_sched", None) or [plan.term_bn, 0, 0])
    fin = {"term_sched_bn": sched, "term_total_bn": float(sum(sched)), "navf_bn": float(plan.navf_bn),
           "beta_bn": float(plan.beta_bn), "beta_sq_bn": float(sq.beta_bn), "rev_upsize_bn": float(plan.rev_upsize_bn)}
    # R1 over the plan's horizon of decisions (today and the dated schedule)
    dB = fin["term_total_bn"] + fin["navf_bn"] + max(fin["beta_bn"] - fin["beta_sq_bn"], 0.0)
    adds = sum(max(r["change_bn"], 0.0) for r in liquid) + sum(max(c["change_5y_bn"], 0.0) for c in commits)
    dE = adds + (fin["beta_bn"] - fin["beta_sq_bn"]) - sum(max(-r["change_bn"], 0.0) for r in liquid) \
        - sum(s["nav_bn"] for s in sells if not s["pe_program"])
    lever = min(max(dB, 0.0), max(dE, 0.0))
    r1 = {"dB_bn": dB, "dE_disc_bn": dE, "LEVER_bn": lever, "REFINANCE_bn": max(dB, 0.0) - lever}
    return {"sells": sells, "liquid": liquid, "reserve": {"from_bn": res_sq, "to_bn": res_pl},
            "commits": commits, "financing": fin, "r1": r1,
            "pe_program": {"exposure_bn": sum(s["exposure_bn"] for s in sells if s["pe_program"]),
                           "nav_bn": sum(s["nav_bn"] for s in sells if s["pe_program"]),
                           "unfunded_bn": sum(s["unfunded_bn"] for s in sells if s["pe_program"]),
                           "proceeds_bn": sum(s["expected_proceeds_bn"] for s in sells if s["pe_program"]),
                           "by_tranche_bn": [sum(s["exposure_bn"] for s in sells if s["pe_program"] and s["tranche"] == k)
                                             for k in (1, 2, 3)]}}


def holding_cards(book, duals: dict | None, prefs: dict, P, settings: dict, plan=None) -> pd.DataFrame:
    """Cards consistent with the plan. Within each unit the plan sells, holdings are sold in order of their margin
    bid_i - p*_i until the plan's fraction of the unit's NAV is reached (SELL, with its tranche); a holding whose bid
    beats its hold value but does not fit is a SELL candidate (the market-depth, program or sale limits bind)."""
    h = book.holdings
    pi = np.array([prefs["scenario_probs"][w] for w in WORLDS])
    gam = float(prefs.get("risk_aversion", 3.0))
    H = float(P.get("returns.horizon_years"))
    R = h[["r_down", "r_base", "r_up"]].to_numpy()
    h = h.assign(ce_pref=ce(R, pi, gam, H), exp_pref=R @ pi)
    thr, econ = {}, {}
    for d in (duals or {}).get("units", []):
        if np.isfinite(d.get("p_star", np.nan)):
            thr[d["unit"]] = d["p_star"]
            econ[d["unit"]] = d.get("p_star_econ", d["p_star"])
    unit_ce = {}
    for uid, g in h[h["unit"] != ""].groupby("unit"):
        unit_ce[uid] = float(np.average(g["ce_pref"], weights=np.maximum(g["nav_bn"], 1e-9)))
    sofr = float(P.get("rates.sofr"))
    navf_cost = sofr + float(P.get("corporate_finance.navf_spread")) + float(P.get("corporate_finance.navf_oid")) / 3
    asset_fin = sofr + 0.025
    goal = float(settings.get("goal_rate", 0.10))
    adj = np.exp((h["ce_pref"].to_numpy() - h["unit"].map(unit_ce).fillna(h["ce_pref"]).to_numpy())
                 * np.minimum(h["duration"].to_numpy(dtype=float), 6.0))
    h["p_star"] = h["unit"].map(thr).to_numpy(dtype=float) * adj
    h["p_hold"] = h["unit"].map(econ).to_numpy(dtype=float) * adj
    h["margin"] = h["bid0"] - h["p_star"]
    card = np.array(["HOLD"] * len(h), dtype=object)
    why = np.array([""] * len(h), dtype=object)
    tranche = np.zeros(len(h), int)
    sold = set()
    if plan is not None:
        for uid, fr in plan.sell.items():
            g = h[h["unit"] == uid]
            if g.empty:
                continue
            target = float(sum(fr)) * float(g["nav_bn"].sum())
            order = g.sort_values("margin", ascending=False, na_position="last")
            acc = 0.0
            cum = np.cumsum([max(f, 0.0) for f in fr])
            for idx, r in order.iterrows():
                if acc >= target - 1e-9:
                    break
                pos = h.index.get_loc(idx)
                share = (acc + 0.5 * r["nav_bn"]) / max(float(g["nav_bn"].sum()), 1e-12)
                tranche[pos] = int(np.searchsorted(cum, share - 1e-12)) + 1
                card[pos] = "SELL"
                why[pos] = (f"plan sells {sum(fr):.0%} of {uid} (tranche {tranche[pos]}); bid {r['bid0']:.2f} vs "
                            f"hold threshold {r['p_star']:.2f}")
                acc += r["nav_bn"]
                sold.add(idx)
    for pos, (idx, r) in enumerate(h.iterrows()):
        bk = BY_ID[r["bucket"]]
        if not bk.private:
            card[pos], why[pos] = "LIQUID", "liquid sleeve: sized by the plan's allocation"
            continue
        if idx in sold:
            continue
        if np.isfinite(r["p_star"]) and r["bid0"] > r["p_star"] * 1.02:
            card[pos] = "SELL?"
            why[pos] = f"bid {r['bid0']:.2f} beats hold threshold {r['p_star']:.2f}, but the plan's sale limits bind"
        elif bk.is_fund and 3 <= r["age"] <= 10 and r["nav_bn"] >= 0.05 and r["ce_pref"] > navf_cost:
            card[pos] = "REFINANCE"
            why[pos] = (f"CE {r['ce_pref']:.1%} above the NAV facility's all-in {navf_cost:.1%}: raise cash against it "
                        f"rather than sell it")
        elif (not bk.is_fund or bk.vertical == "GP Led") and r["ce_pref"] >= goal + 0.02 and r["ce_pref"] >= asset_fin + 0.04:
            card[pos] = "LEVER"
            why[pos] = f"CE {r['ce_pref']:.1%} clears the {goal:.0%} hurdle +2pp and asset-level financing +4pp"
        else:
            why[pos] = (f"hold threshold {r['p_star']:.2f} vs bid {r['bid0']:.2f}" if np.isfinite(r["p_star"])
                        else "no plan yet")
    h["card"], h["why"], h["tranche"] = card, why, tranche
    return h


def holdings_payload(cards: pd.DataFrame, limit: int | None = None) -> list[dict]:
    cols = ["FUND_CODE", "FUND_NAME", "bucket", "department", "vertical", "vehicle", "INVESTMENT_CLASS",
            "INVESTMENT_STYLE", "vintage", "age", "nav_bn", "unfunded_bn", "uw_irr", "act_irr", "ACTUAL_TVPI",
            "ACTUAL_DPI", "shortfall_vs_uw", "act_excess", "perf", "S_base", "r_down", "r_base", "r_up", "exp_pref",
            "ce_pref", "tilt_uw", "tilt_act", "bid0", "p_star", "p_hold", "margin", "card", "why", "tranche", "unit",
            "confidence", "rule", "duration"]
    d = cards[[c for c in cols if c in cards.columns]].copy()
    d = d.sort_values("nav_bn", ascending=False)
    if limit:
        d = d.head(limit)
    d = d.replace({np.nan: None})
    out = []
    for rec in d.to_dict(orient="records"):
        for k, v in rec.items():
            if isinstance(v, (np.floating, float)) and v is not None:
                rec[k] = float(v)
            elif isinstance(v, (np.integer,)):
                rec[k] = int(v)
            elif v is pd.NA:
                rec[k] = None
        out.append(rec)
    return out


def alternatives(book, prefs: dict, P, duals: dict | None = None) -> list[dict]:
    pi = np.array([prefs["scenario_probs"][w] for w in WORLDS])
    gam = float(prefs.get("risk_aversion", 3.0))
    H = float(P.get("returns.horizon_years"))
    br = book.bucket_ret
    out = []
    for b in PRIVATE + [x for x in LIQUID_RISK]:
        R = np.array([[br.loc[b, f"new_{w}"] for w in WORLDS]])
        out.append({"bucket": b, "label": BY_ID[b].label, "department": BY_ID[b].department,
                    "er": [float(br.loc[b, f"new_{w}"]) for w in WORLDS], "exp": float((R @ pi)[0]),
                    "ce": float(ce(R, pi, gam, H)[0]),
                    "lp_value": (duals or {}).get("commit", {}).get(b, (duals or {}).get("liquid", {}).get(b))})
    return sorted(out, key=lambda r: -r["ce"])
