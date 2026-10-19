"""
gap_02 (groups) - re-runs on the vintage-resolved PE book (census v1.1 and truth variants).  ALL SYNTHETIC.

Replaces ONLY the PE-funds leg of the existing group scripts with the RFT-TA v2 vintage engine
(rfta_v2_book.py; state at 2026-09-30 from seal_history_results.json) and re-runs:
  1. the sec. 2.2 group cash map (logic of GS_calcs/gs_group_cashmap.py.run, census split; normal, drought, S1, s*=T4)
  2. the S1 and s* (T4) ladders (logic of GC2_calcs/gc2_reconcile.run_v2 and gap_01 t14_hf_swap.run_swap):
     SH_TP with Treasury usable to 4% of NAV, 24-month cover, committed facility to clear 24 months;
     static hedge-fund buckets and the gap_01 state-machine P5 ladder
  3. the PACE lever table (pause 2027, pause 2027-28, halve 2027-28) on path L (drought to 2029, then normal)
  4. the sec. 4.7 co-investment flow O_t = theta * sum_k d_k C_{t-k} from the sealed commitment history
  5. the 0.80W row (L8): private NAV + unfunded <= 0.80 W
Reproduction checks: with the rate-based PE leg the cash map reproduces gs_group_cashmap_results.json and the
ladder reproduces gc2_reconcile_results.json / gap_01 t14_hf_swap_results.json.
Imported read-only (nothing edited): GS_calcs/gs_group_cashmap.py, GC2_calcs/gc2_reconcile.py (both load the
unmodified stream-G7 module), research/addenda/gap_01_calcs/hf_ladder_results.json.
Run:  .venv\\Scripts\\python.exe -I -B gap02_rerun.py   -> gap02_rerun_results.json
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ADD = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ADD, "GS_calcs"))
sys.path.insert(0, os.path.join(ADD, "GC2_calcs"))
import rfta_v2_book as rb  # noqa: E402
import gs_group_cashmap as gs  # noqa: E402
import gc2_reconcile as r2  # noqa: E402

g = gs.g
OUT = os.path.join(HERE, "gap02_rerun_results.json")
SEAL = json.load(open(os.path.join(HERE, "seal_history_results.json"), encoding="utf-8"))
GS_RES = json.load(open(os.path.join(ADD, "GS_calcs", "gs_group_cashmap_results.json"), encoding="utf-8"))
GC2_RES = json.load(open(os.path.join(ADD, "GC2_calcs", "gc2_reconcile_results.json"), encoding="utf-8"))
HF_SM = json.load(open(os.path.normpath(os.path.join(ADD, "..", "..", "addenda", "gap_01_calcs", "hf_ladder_results.json")),
                       encoding="utf-8"))
HF_KEYS = ["hf_le7d", "hf_8_90d", "hf_91_365d", "hf_gt365d"]
REGMAP = {"normal": "N", "drought": "D", "crisis": "F", "boom": "O"}
UNF_CENSUS = dict(gs.UNF_CENSUS)


# ------------------------------------------------------------------------------------------------ PE book state
def census_cohorts(commitments: dict, omega: dict) -> list:
    """Cohort objects at 2026-09-30 for annual commitments by vintage (2010..2026; legacy pre-2010 at c_2010)."""
    cohorts = []
    for s in rb.S_KEYS:
        for v in range(1998, 2027):
            c = commitments[2010] if v < 2010 else commitments[v]
            nq = 3 if v == 2026 else 4
            for qi in range(nq):
                qc = v * 4 + qi
                h = rb.unit_history(s, qc)
                U, V, age, ae = h["state"]
                amt = omega[s] * c * 0.25
                cohorts.append(rb.Cohort(s, qc, K=amt, U=U * amt, V=V * amt, age=age, ae=ae))
    return cohorts


class PEBook:
    def __init__(self, commitments: dict, omega: dict):
        self.omega = omega
        self.cohorts = census_cohorts(commitments, omega)

    @property
    def nav(self):
        return sum(c.V for c in self.cohorts)

    @property
    def unf(self):
        return sum(c.U for c in self.cohorts)

    crisis_mD = None  # None: RFT-TA v2 F multiplier (0.325); set to match another crisis-distribution convention

    def step_month(self, t: int, reg: str, call_mult: float, dist_zero: bool, mark: float, new_commit: float):
        r = REGMAP[reg]
        mC = (1.0 if r == "F" else rb.REG[r]["mC"])
        mD = self.crisis_mD if (r == "F" and self.crisis_mD is not None) else None
        if new_commit > 0:
            for s in rb.S_KEYS:
                self.cohorts.append(rb.Cohort(s, 10_000 + t, K=self.omega[s] * new_commit))
        calls = dists = 0.0
        for c in self.cohorts:
            cl, d = c.step(r, 1.0 / 12.0, call_mult=call_mult, mC_override=mC, mD_override=mD, dist_zero=dist_zero,
                           mark=mark)
            calls += cl
            dists += d
        return calls, dists


def sealed_inputs(name: str = "sealed"):
    if name == "sealed":
        s = SEAL["sealed"]
        return {int(k): v for k, v in s["commitments"].items()}, s["omega"], s["pace2026"]
    vv = SEAL["variants"][name]
    com = {y: x for y, x in zip(range(2010, 2027), vv["commitments"])}
    return com, vv["omega"], vv["pace2026"]


# ------------------------------------------------------------------------------------------------ 1. cash map
def cashmap_run(scn: str, pe: str | tuple, T: int = 12, pe_pace: float | None = None,
                crisis_mD: float | None = None) -> dict:
    """gs_group_cashmap.run (census split) with the PE leg replaced when pe != 'rate'.
    pe: 'rate' (GS logic) or (book_name,) ; pe_pace: annual PE commitments for the forward window."""
    p = gs.paths(scn, 36)
    rates = gs.dist_table("census")
    bal = dict(g.BAL0)
    unf = dict(UNF_CENSUS)
    book = None
    if pe != "rate":
        com, om, pace26 = sealed_inputs(pe[0])
        book = PEBook(com, om)
        book.crisis_mD = crisis_mD
        pace = pace26 if pe_pace is None else pe_pace
        unf["pe"] = book.unf
    eq_idx = 1.0
    im = g.IM_RATE_N * g.SYN_NOTIONAL
    acc = {k: 0.0 for k in ("vm", "d_im", "hedge", "opp", "opex")}
    dist_g = {k: 0.0 for k in g.PRIVATE}
    calls_g = {k: 0.0 for k in g.PRIVATE}
    for t in range(T):
        reg = p["regime"][t]
        stress = reg == "crisis"
        for k, f in (("lo_dm", p["eq"][t]), ("lo_em", 1.2 * p["eq"][t]), ("lo_fi", p["fi"][t]),
                     ("ig", p["ig"][t]), ("ust", p["ust"][t]), ("cash", 0.039 / 12)):
            bal[k] *= 1 + f
        for k in g.HF_SHARES:
            bal[k] *= 1 + p["hf"][t]
        for gg in g.PRIVATE:
            bal[gg] *= 1 + p["priv_mark"][t]
        vm = g.SYN_NOTIONAL * eq_idx * p["eq"][t]
        eq_idx *= 1 + p["eq"][t]
        im_new = (g.IM_RATE_S if (stress and t < 12) else g.IM_RATE_N) * g.SYN_NOTIONAL * eq_idx
        d_im = im_new - im
        im = im_new
        hedge_cf = -g.HEDGE_PREMIUM_PA / 12
        if t in p["hedge_months"]:
            hedge_cf += 0.5 * g.HEDGE_NOTIONAL * min(0.20, max(0.0, 0.90 - eq_idx))
        opp = -p["opp_loss"][t]
        dist = {}
        for gg in g.PRIVATE:
            rate = rates[reg][gg]
            if p["dist_zero"][t] and gg in ("pe", "sec", "co"):
                rate = 0.0
            dist[gg] = g.monthly_rate(rate) * bal[gg]
        crate = g.monthly_rate(min(0.95, g.CALL[reg] * p["call_mult"][t]))
        calls = {k: crate * unf[k] for k in ("pe", "sec", "pc", "cs", "co")}
        calls["sec_def"] = (UNF_CENSUS["sec_def"] / 4.0) if t in (2, 5, 8, 11) else 0.0
        spike = p["rev_draw"][t] * UNF_CENSUS["pc_rev"]
        calls["pc_rev"] = min(unf["pc_rev"], spike if spike > 0 else crate * unf["pc_rev"])
        if book is not None:
            c_pe, d_pe = book.step_month(t, reg, p["call_mult"][t], bool(p["dist_zero"][t]), p["priv_mark"][t], pace / 12.0)
            calls["pe"], dist["pe"] = c_pe, d_pe
        nc = g.NEW_COMMIT_PA / 12.0
        for k, v in calls.items():
            unf[k] -= v
        for k, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1), ("co", 0.1)):
            unf[k] += w * nc
        for gg in g.PRIVATE:
            add = calls[gg] + (calls["sec_def"] if gg == "sec" else 0.0) + (calls["pc_rev"] if gg == "pc" else 0.0)
            if gg == "pe" and book is not None:
                bal["pe"] = book.nav
            else:
                bal[gg] += add - dist[gg]
            calls_g[gg] += add
            dist_g[gg] += dist[gg]
        acc["vm"] += vm
        acc["d_im"] += d_im
        acc["hedge"] += hedge_cf
        acc["opp"] += opp
        acc["opex"] += 0.001 * g.NAV0 / 12.0
    net_g = {k: dist_g[k] - calls_g[k] for k in g.PRIVATE}
    priv_net = sum(net_g.values())
    overlay_net = acc["vm"] - acc["d_im"] + acc["hedge"] + acc["opp"]
    before = priv_net + overlay_net - acc["opex"]
    liquid0 = sum(g.BAL0[k] for k in g.LIQ_KEYS) + g.HF_TOTAL
    fund = {k: v * g.NAV0 - before for k, v in (("5%", 0.05), ("7.5%", 0.075), ("10%", 0.10))}
    out = dict(dist_by_group=dist_g, calls_by_group=calls_g, net_by_group=net_g, private_net=priv_net,
               overlay_net=overlay_net, before_payout=before, liquid_funding=fund,
               liquid_share={k: v / liquid0 for k, v in fund.items()})
    if book is not None:
        out["pe_nav_end"] = book.nav
        out["pe_unf_end"] = book.unf
        out["pe_pace"] = pace
    return out


# ------------------------------------------------------------------------------------------------ 2. ladders
def ladder_run(scn: str, basis: str, pe: str | tuple, unf_split: dict, hf_phi=None, T: int = 36,
               pe_pace: float | None = None) -> dict:
    """gc2_reconcile.run_v2 / t14_hf_swap.run_swap logic, PE leg pluggable, unfunded split as given."""
    p = r2.scenario_paths(scn, T)
    bal = dict(g.BAL0)
    unf = dict(unf_split)
    book = None
    if pe != "rate":
        com, om, pace26 = sealed_inputs(pe[0])
        book = PEBook(com, om)
        pace = pace26 if pe_pace is None else pe_pace
        unf["pe"] = book.unf
    eq_idx = 1.0
    im = g.IM_RATE_N * g.SYN_NOTIONAL
    rows = []
    nco_prev = 0.0
    for t in range(T):
        reg = p["regime"][t]
        stress = reg == "crisis"
        for k, f in (("lo_dm", p["eq"][t]), ("lo_em", 1.2 * p["eq"][t]), ("lo_fi", p["fi"][t]),
                     ("ig", p["ig"][t]), ("ust", p["ust"][t]), ("cash", 0.039 / 12)):
            bal[k] *= 1 + f
        for k in g.HF_SHARES:
            bal[k] *= 1 + p["hf"][t]
        for gg in g.PRIVATE:
            bal[gg] *= 1 + p["priv_mark"][t]
        nav_start = sum(bal.values()) - nco_prev
        vm = g.SYN_NOTIONAL * eq_idx * p["eq"][t]
        eq_idx *= 1 + p["eq"][t]
        im_new = (g.IM_RATE_S if (stress and t < 12) else g.IM_RATE_N) * g.SYN_NOTIONAL * eq_idx
        d_im = im_new - im
        im = im_new
        hedge_cf = -g.HEDGE_PREMIUM_PA / 12
        if t in p["hedge_months"]:
            hedge_cf += 0.5 * g.HEDGE_NOTIONAL * min(0.20, max(0.0, 0.90 - eq_idx))
        opp = -p["opp_loss"][t]
        dist = {}
        for gg in g.PRIVATE:
            rate = g.DIST[reg][gg]
            if p["dist_zero"][t] and gg in ("pe", "sec", "co"):
                rate = 0.0
            dist[gg] = g.monthly_rate(rate) * bal[gg]
        crate = g.monthly_rate(min(0.95, g.CALL[reg] * p["call_mult"][t]))
        calls = {k: crate * unf[k] for k in ("pe", "sec", "pc", "cs", "co")}
        calls["sec_def"] = (unf_split["sec_def"] / 4.0) if t in (2, 5, 8, 11) else 0.0
        spike = p["rev_draw"][t] * unf_split["pc_rev"]
        calls["pc_rev"] = min(unf["pc_rev"], spike if spike > 0 else crate * unf["pc_rev"])
        if book is not None:
            c_pe, d_pe = book.step_month(t, reg, p["call_mult"][t], bool(p["dist_zero"][t]), p["priv_mark"][t], pace / 12.0)
            calls["pe"], dist["pe"] = c_pe, d_pe
        nc = g.NEW_COMMIT_PA / 12.0
        for k, v in calls.items():
            unf[k] -= v
        for k, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1), ("co", 0.1)):
            unf[k] += w * nc
        for gg in g.PRIVATE:
            add = calls[gg] + (calls["sec_def"] if gg == "sec" else 0.0) + (calls["pc_rev"] if gg == "pc" else 0.0)
            if gg == "pe" and book is not None:
                bal["pe"] = book.nav
            else:
                bal[gg] += add - dist[gg]
        base = g.NAV0 if basis == "opening" else nav_start
        draw = p["draw_rate"][t] * base / 12.0
        opex = 0.001 * g.NAV0 / 12.0
        uses = draw + sum(calls.values()) + max(0.0, -vm) + max(0.0, d_im) + max(0.0, -hedge_cf) + max(0.0, -opp) + opex
        inflows = sum(dist.values()) + max(0.0, vm) + max(0.0, -d_im) + max(0.0, hedge_cf) + max(0.0, opp)
        net = uses - inflows
        nco_prev += net
        rows.append(dict(net=net, gross_nav=sum(bal.values()), calls=sum(calls.values()), dist=sum(dist.values()),
                         pe_calls=calls["pe"], pe_dist=dist["pe"]))
    idx = {"cash": np.cumprod(np.full(T, 1 + 0.039 / 12)), "ust": np.cumprod(1 + p["ust"]),
           "ig": np.cumprod(1 + p["ig"]), "eq": np.cumprod(1 + p["eq"]), "fi": np.cumprod(1 + p["fi"]),
           "em": np.cumprod(1 + 1.2 * p["eq"]), "hf": np.cumprod(1 + p["hf"]), "priv": np.cumprod(1 + p["priv_mark"])}
    proceeds = {}
    for k, prm in g.LADDER.items():
        if hf_phi is not None and k in HF_KEYS:
            continue
        mv = g.BAL0[k] * idx[prm["path"]]
        cum = np.zeros(T)
        remaining, accp = 1.0, 0.0
        if k == "cash":
            mv = mv - (g.IM_RATE_N * g.SYN_NOTIONAL + g.OPP_IM)
        for t in range(T):
            crisis_t = p["regime"][t] == "crisis"
            hc = prm["hc_s"]
            ttc = prm["ttc"] + (2 if (crisis_t and prm["tier"] in ("A", "R")) else 0)
            if t >= ttc and remaining > 1e-12:
                frac = min(prm["cap"], remaining)
                if k.startswith("hf") and crisis_t:
                    frac *= 0.5
                remaining -= frac
                accp += frac * mv[t] * (1 - hc)
            cum[t] = accp
        proceeds[k] = cum
    if hf_phi is not None:
        proceeds["hf_sm"] = sum(g.BAL0[k] for k in HF_KEYS) * np.asarray(hf_phi[:T])
        hfk = ["hf_sm"]
    else:
        hfk = HF_KEYS
    fa = p["fac_avail"]
    net = np.array([r["net"] for r in rows])
    nco = np.cumsum(net)
    cbc_tp = sum(proceeds[k] for k in ["cash", "ust", "ig", "lo_dm", "lo_fi", "lo_em"] + hfk)
    true_nav = np.array([r["gross_nav"] for r in rows]) - nco
    cbc_tp4 = cbc_tp - 0.04 * true_nav

    def surv(c):
        br = np.where(nco > c)[0]
        return int(br[0] + 1) if br.size else None
    gap = np.maximum(0.0, nco[:24] - cbc_tp4[:24])
    fac = float((gap[1:] / fa[1:24]).max()) if gap[1:].size else 0.0
    return dict(SH_TP_floor4=surv(cbc_tp4), SH_TP_floor0=surv(cbc_tp), need_12m=float(nco[11]), need_24m=float(nco[23]),
                cover24_tp_floor4=float(cbc_tp4[23] / nco[23]), facility_24m=fac,
                pe_calls_12m=float(sum(r["pe_calls"] for r in rows[:12])), pe_dist_12m=float(sum(r["pe_dist"] for r in rows[:12])),
                pe_calls_24m=float(sum(r["pe_calls"] for r in rows[:24])), pe_dist_24m=float(sum(r["pe_dist"] for r in rows[:24])))


# ------------------------------------------------------------------------------------------------ 3. PACE levers
def pace_levers(book_name: str = "sealed") -> dict:
    com, om, pace = sealed_inputs(book_name)

    def run(mult: dict):
        book = PEBook(com, om)
        ncf = {}
        nav = {}
        q = 0
        for y in range(2026, 2041):
            quarters = [3] if y == 2026 else [0, 1, 2, 3]
            for qi in quarters:
                reg = "D" if y <= 2029 else "N"
                c_new = pace * mult.get(y, 1.0) * 0.25
                if c_new > 0:
                    for s in rb.S_KEYS:
                        book.cohorts.append(rb.Cohort(s, 20_000 + q, K=om[s] * c_new))
                cl = ds = 0.0
                for c in book.cohorts:
                    a, b = c.step(reg, 0.25)
                    cl += a
                    ds += b
                ncf[y] = ncf.get(y, 0.0) + ds - cl
                q += 1
            nav[y] = book.nav
        return ncf, nav
    base_ncf, base_nav = run({})
    out = {"pace": pace}
    for name, mult in (("pause_2027", {2027: 0.0}), ("pause_2027_28", {2027: 0.0, 2028: 0.0}),
                       ("halve_2027_28", {2027: 0.5, 2028: 0.5})):
        ncf, nav = run(mult)
        d = [ncf[y] - base_ncf[y] for y in range(2027, 2041)]
        forgone = sum(pace * (1 - m) for m in mult.values())

        def npv(r):
            return sum(x / (1 + r) ** i for i, x in enumerate(d))
        try:
            irr = brentq(npv, -0.5, 1.0)
        except ValueError:
            irr = float("nan")
        out[name] = dict(forgone=forgone, d_ncf_2027=d[0], d_ncf_2027_30=sum(d[:4]), share_4y=sum(d[:4]) / forgone,
                         d_ncf_2027_40=sum(d), implied_irr=irr, d_nav_2031_pct=(nav[2031] - base_nav[2031]) / base_nav[2031])
    out["base_ncf_2027_30"] = {y: base_ncf[y] for y in range(2027, 2031)}
    return out


# ------------------------------------------------------------------------------------------------ 4. co-investment flow
def coinvest_flow(book_name: str = "sealed", theta: float = 0.33) -> dict:
    com, om, pace = sealed_inputs(book_name)
    d = (0.15, 0.25, 0.25, 0.20, 0.15)
    hist = dict(com)
    out = {}
    for label, fwd in (("hold_pace", {2027: pace, 2028: pace, 2029: pace, 2030: pace}),
                       ("pause_2027", {2027: 0.0, 2028: pace, 2029: pace, 2030: pace})):
        series = dict(hist)
        series.update(fwd)
        o = {t: theta * sum(d[k] * series[t - k] for k in range(5)) for t in (2026, 2027, 2028, 2029, 2030)}
        out[label] = {t: dict(offered=o[t], accepted_lo=0.3 * o[t], accepted_hi=0.6 * o[t]) for t in o}
    out["steady_state_at_pace"] = dict(offered=theta * pace, accepted_lo=0.3 * theta * pace, accepted_hi=0.6 * theta * pace)
    out["pace_needed_for_3bn_accepted"] = dict(at_a0_6=3.0 / (theta * 0.6), at_a0_3=3.0 / (theta * 0.3))
    return out


# ------------------------------------------------------------------------------------------------ main
def main():
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "sealed": {k: SEAL["sealed"][k] for k in ("g1", "g2", "boom", "pace2026")},
           "sealed_census": SEAL["sealed"]["census"]}
    # reproduction checks
    rep_cash = {}
    for scn in ("normal", "drought", "S1", "T14"):
        mine = cashmap_run(scn, "rate")
        ref = GS_RES["runs"][f"census|{scn}"]
        rep_cash[scn] = max(abs(mine["net_by_group"][k] - ref["net_by_group"][k]) for k in g.PRIVATE)
    res["repro_cashmap_max_abs_diff_bn"] = rep_cash
    rep_lad = {}
    for scn, basis in (("T14", "opening"), ("T14", "current"), ("S1", "opening")):
        mine = ladder_run(scn, basis, "rate", g.UNF0)
        ref = GC2_RES["named"][f"{scn}|{basis}"]
        rep_lad[f"{scn}|{basis}"] = dict(need12=(round(mine["need_12m"], 3), round(ref["need_12m"], 3)),
                                         SH=(mine["SH_TP_floor4"], ref["SH_TP_floor4"]),
                                         fac=(round(mine["facility_24m"], 2), round(ref["committed_facility_needed_for_24m"], 2)))
    sm = HF_SM["equity_minus40"]["phi_monthly_p5"]
    mine = ladder_run("T14", "opening", "rate", g.UNF0, hf_phi=sm)
    rep_lad["T14|opening|state_machine_P5"] = dict(SH=mine["SH_TP_floor4"], fac=round(mine["facility_24m"], 1),
                                                   gap01_reported=dict(SH=15, fac=40.6))
    res["repro_ladder"] = rep_lad
    # 1. cash map: census v1.0 (rate PE leg) vs vintage books
    books = ["sealed", "mature_flat", "g10_to_2022_then_flat", "g20pct", "v1_0_reproduction"]
    cm = {}
    for scn in ("normal", "drought", "S1", "T14"):
        cm[f"v1.0_rate|{scn}"] = cashmap_run(scn, "rate")
        for b in books:
            cm[f"{b}|{scn}"] = cashmap_run(scn, (b,))
        cm[f"sealed_gs_pace7.2|{scn}"] = cashmap_run(scn, ("sealed",), pe_pace=7.2)
        cm[f"v1_0_reproduction_gs_pace7.2|{scn}"] = cashmap_run(scn, ("v1_0_reproduction",), pe_pace=7.2)
    # S1 under the stream-G7 crisis-distribution convention (PE ~3.5%/yr) instead of the v2 F multiplier
    def s1_rate(mD):
        r = cashmap_run("S1", ("sealed",), crisis_mD=mD)
        return r["dist_by_group"]["pe"] / 52.0 - 0.035
    mD_g7 = brentq(s1_rate, 0.01, 0.325, xtol=1e-4)
    cm["sealed_g7_crisis_dist|S1"] = cashmap_run("S1", ("sealed",), crisis_mD=mD_g7)
    cm["sealed_g7_crisis_dist|S1"]["crisis_mD"] = mD_g7
    res["cashmap"] = cm
    # 2. ladders on census split with the vintage PE leg
    lad = {}
    split_v11 = dict(UNF_CENSUS)
    for b in ("rate", "sealed", "g20pct", "v1_0_reproduction"):
        for scn, basis in (("S1", "opening"), ("T14", "opening"), ("T14", "current")):
            key_pe = "rate" if b == "rate" else (b,)
            lad[f"{b}|{scn}|{basis}|buckets"] = ladder_run(scn, basis, key_pe, split_v11)
            lad[f"{b}|{scn}|{basis}|state_machine"] = ladder_run(scn, basis, key_pe, split_v11, hf_phi=sm)
    res["ladders"] = lad
    # 3. PACE levers
    res["pace_levers"] = {b: pace_levers(b) for b in ("sealed", "mature_flat", "g20pct")}
    # 4. co-investment flow
    res["coinvest_flow"] = {b: coinvest_flow(b) for b in ("sealed", "mature_flat", "g20pct", "v1_0_reproduction")}
    # 5. 0.80W row
    w = g.NAV0
    pe_u = {"v1.0": 27.4}
    pe_u.update({b: (SEAL["sealed"]["census"]["unf"] if b == "sealed" else SEAL["variants"][b]["unf"]) for b in books})
    res["L8_0p80W"] = {b: dict(pe_unfunded=u, total_unfunded=38.0 - 27.4 + u, ratio=(106.0 + 38.0 - 27.4 + u) / w,
                               headroom_bn=0.80 * w - (106.0 + 38.0 - 27.4 + u)) for b, u in pe_u.items()}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=float)
    # console summary
    print("repro cashmap:", rep_cash)
    print("repro ladder:", json.dumps(rep_lad))
    for k, r in cm.items():
        ng = {kk: round(v, 2) for kk, v in r["net_by_group"].items()}
        extra = f" PE d/c {r['dist_by_group']['pe']:.2f}/{r['calls_by_group']['pe']:.2f}"
        print(f"{k:34s} priv {r['private_net']:+7.2f} before {r['before_payout']:+7.2f} fund@7.5 {r['liquid_funding']['7.5%']:6.2f} "
              f"({r['liquid_share']['7.5%']:.0%}) {ng}{extra}")
    for k, r in lad.items():
        print(f"{k:44s} SH_TP4 {r['SH_TP_floor4']} fac24 {r['facility_24m']:6.2f} need12 {r['need_12m']:6.2f} "
              f"PE c/d 12m {r['pe_calls_12m']:.2f}/{r['pe_dist_12m']:.2f}")
    for b, r in res["pace_levers"].items():
        print(b, "pace", round(r["pace"], 2), {k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in r.items() if isinstance(v, dict) and "forgone" in v})
    for b, r in res["coinvest_flow"].items():
        print(b, {k: (round(v[2027]["accepted_lo"], 2), round(v[2027]["accepted_hi"], 2)) for k, v in r.items() if k in ("hold_pace", "pause_2027")},
              "2026", (round(r["hold_pace"][2026]["accepted_lo"], 2), round(r["hold_pace"][2026]["accepted_hi"], 2)))
    print("L8:", {k: round(v["ratio"], 3) for k, v in res["L8_0p80W"].items()})


if __name__ == "__main__":
    main()
