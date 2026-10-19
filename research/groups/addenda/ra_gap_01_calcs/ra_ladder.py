"""
ra_gap_01: deterministic monthly T4' ladder for the eight-group v2 book, with a theta-indexed Real Assets leg,
group-tagged levers (Phase I), cards (Phase II) and dual-based group prices.

SYNTHETIC - NOT ADIC DATA.

It is a copy of groups gap_01's `g01_core.gl_ladder` (itself an exact replica of gap_02's `t1_engine.ladder`),
generalised to a book argument and extended with:
  * the Real Assets leg `ra_leg()` (G15's monthly sleeve engine; reproduction mode 'g15' and canonical mode),
  * Real Assets levers (pacing cut, pre-arranged JV sell-down, t0 cash-out at maturity) and cards (ENR SELL,
    real-estate LP sale),
  * group prices for Real Assets (FTP on holdings, hurdle, 12/24-month envelope = L4 budget B_RA).
With book='v1' and the RA leg off it reproduces g01_core.gl_ladder exactly (asserted in ra_run.py validate).
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import sys

import cvxpy as cp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra_book as B  # noqa: E402

GAP02 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "addenda", "gap_02_calcs"))
sys.path.insert(0, GAP02)
import t1_engine as E  # noqa: E402  (unmodified)
from gap02_study import s_star, t4_literal  # noqa: E402

PRIV = ("pe", "sec", "co", "cs", "pc")
GROUP_NAME = {"pe": "PE", "sec": "Secondaries", "co": "Co-investment", "cs": "Capital Solutions",
              "pc": "Private Credit", "ra": "Real Assets", "pm": "Public Markets", "ovl": "Overlay",
              "cf": "Corporate Finance", "own": "Owner (band)"}
M_TIERS = {"S": 1e2, "IG": 10.0}
H_ROWS = 24
ALPHA_D = {"pe": (0.015, 5.0), "sec": (0.030, 3.4), "co": (0.025, 4.5), "cs": (0.035, 4.0), "pc": (0.010, 3.0),
           "ra": (0.010, 5.2)}                        # RA: net premium ~1% (ra_book prem), closed-end duration [I]
SMA_SLEEVE = 0.40 * 14.0
RUNOFF_C, RUNOFF_T = 0.065, 0.14
P_SMA, P_CS, P_HF = 0.96, 0.90, 0.80
P_JV_T0, JV_CAP_SHARE = 0.92, 0.40                    # pre-arranged JV sell-down at t0 (G15 drought 0.92; 40%)
CALL_RA = {"normal": 0.29, "drought": 0.28, "crisis": 0.30}
CASHOUT_LTV = {"RE": 0.55, "RE_GCC": 0.55, "INF": 0.60, "ENR": 0.50}   # G15 refinance_capacity targets


def w_new(book: str) -> dict:
    """Plan pacing split of the canonical $12bn a year: v1 60/10/10/10/10; v2 RA takes 10% from PE (G15)."""
    if B.BOOKS[book]["ra"]:
        return {"pe": 0.5, "sec": 0.1, "pc": 0.1, "cs": 0.1, "co": 0.1, "ra": 0.1}
    return {"pe": 0.6, "sec": 0.1, "pc": 0.1, "cs": 0.1, "co": 0.1, "ra": 0.0}


BASE = dict(rcf=0.0, navf=0.0, reserve=0.0, reserve_add=0.0, band=0.0, pace=12.0,
            cut={g: 0.0 for g in ("pe", "sec", "pc", "cs", "co", "ra")}, cut_from=2, amber_t0=0.0, sma_sell=0.0,
            cs_synd=0.0, sma_ro=0.0, ovl_im=0.0, p2s=0.0, hf_sell=0.0, red={"pe": 0.0, "sec": 0.0, "co": 0.0},
            red_bid={"pe": 0.88, "sec": 0.87, "co": 0.75},
            new_commit={g: 0.0 for g in ("pe", "sec", "pc", "cs", "co", "ra")}, cash_t0=0.0, census="v1",
            book="v1", ra_jv=0.0, ra_cashout=0.0, enr_sell=0.0, enr_bid=0.80, ra_re_sell=0.0, ra_re_bid=0.68,
            ra_scale=1.0)


def lev_of(**kw) -> dict:
    lev = copy.deepcopy(BASE)
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(lev.get(k), dict):
            lev[k].update(v)
        else:
            lev[k] = v
    return lev


def lev_from_policy(pol: E.Policy, **kw) -> dict:
    cut = 0.75 if pol.pace_cut else 0.0
    return lev_of(rcf=pol.rcf, navf=pol.navf, reserve=pol.reserve, band=1.0 if pol.band else 0.0, pace=pol.pace,
                  cut={g: cut for g in ("pe", "sec", "pc", "cs", "co", "ra")}, amber_t0=pol.amber_t0, **kw)


def _monthly(r):
    return 1.0 - (1.0 - min(max(r, 0.0), 0.99)) ** (1.0 / 12.0)


def cashout_caps(sl_list=None, scale: float = 1.0) -> dict:
    """Cash-out at maturity capacity on Q4-2026 maturities of controlled direct debt: new loan at the G15 target
    LTV on the maturing tranche's value less the old balance (no early refinancing while lock-in > 0.5% GAV)."""
    out = {}
    for s in (sl_list or B.SLEEVES):
        if not (s["direct"] and s["ctrl"] > 0):
            continue
        nav = s["nav"] * scale
        debt = nav * s["ltv"] / (1 - s["ltv"]) * s["ctrl"]
        d_q = debt * B.MATURITY_PA / 4.0
        out[s["id"]] = max(0.0, CASHOUT_LTV[s["sector"]] * d_q / s["ltv"] - d_q)
    return out


# ================================================================================================= RA leg
def ra_leg(theta: float | None, T: int = 36, mode: str = "canonical", state: str = "T4prime", commit_m=None,
           opts: dict | None = None, sleeves=None) -> dict:
    """Monthly Real Assets cash engine (G15 mechanics). Returns per-month aggregates and per-sleeve detail.

    mode 'g15'      : exactly G15's run_book (state in normal / drought / T4prime): hard-coded T4' marks, cures on
                      direct sleeves only, no availability, no fund-level module (V-RA-CF reproduction).
    mode 'canonical': theta-indexed components (ra_book.ra_theta), RAME reported marks (Geltner lambda_agg with
                      the segment lag on the true-value ramp), lender availability and extension axis, the
                      fund-level refinancing module (shortfall -> protective call up to unfunded -> distribution
                      stop -> NAV loss at a 20% fire-sale discount), state 'T4prime' only.
    commit_m        : array (T,) of new RA closed-end commitments per month ($bn), split by census commit shares.
    opts            : availability (bool), ext (float), call_axis (float|None), fund_module ('waterfall' |
                      'upper' | 'off'), marks ('rame' | 'g15'), nav_scale (float), sell (dict id -> $bn reported
                      NAV sold at t0, buyer assumes pro-rata unfunded), cashout_t0 ($bn, controlled share).
    """
    o = dict(availability=True, ext=None, call_axis=None, fund_module="waterfall", marks="rame", nav_scale=1.0,
             sell={}, cashout_t0=0.0)
    o.update(opts or {})
    sl_list = sleeves or B.SLEEVES
    if commit_m is None:
        commit_m = np.full(T, 1.2 / 12.0)
    if mode == "g15":
        o.update(availability=False, fund_module="off", marks="g15")
    comp = B.ra_theta(theta if theta is not None else B.THETA0, availability=o["availability"], ext=o["ext"],
                      call_axis=o["call_axis"]) if (mode == "canonical" or state == "T4prime") else None
    agg = {k: np.zeros(T) for k in ("income", "realiz", "calls", "prot_calls", "cures", "dist_stop", "nav_loss",
                                    "nav_rep", "nav_true", "debt", "unf", "shortfall_fund", "cashout")}
    per = {}
    for sl in sl_list:
        sec = sl["sector"]
        scale = o["nav_scale"]
        nav = sl["nav"] * scale
        unf = sl["unf"] * scale
        ltv0 = sl["ltv"]
        debt = nav * ltv0 / (1.0 - ltv0)
        gav0 = nav + debt
        sold = o["sell"].get(sl["id"], 0.0)
        if sold > 0:                                     # t0 sale: equity, debt and unfunded leave pro rata
            f = min(1.0, sold / nav)
            nav, debt, unf, gav0 = nav * (1 - f), debt * (1 - f), unf * (1 - f), gav0 * (1 - f)
        # collateral value per $ of maturing debt: G15 uses origination LTV; canonical uses true value (gap g0)
        coll = (1.0 / ltv0) if (mode == "g15" or state != "T4prime") else (gav0 / (1.0 + sl["g0"])) / max(debt, 1e-12)
        cash_out = 0.0
        if o["cashout_t0"] > 0 and sl["direct"] and sl["ctrl"] > 0:
            # cash-out at maturity on the controlled share of the debt maturing in the first quarter (pre-stress),
            # allocated pro rata to each sleeve's capacity
            caps = cashout_caps(sl_list, scale)
            tot_cap = sum(caps.values())
            cash_out = min(o["cashout_t0"], tot_cap) * caps.get(sl["id"], 0.0) / max(tot_cap, 1e-12)
            debt += cash_out
        vt = gav0 / (1.0 + sl["g0"]) - debt                 # true equity: reported asset value carries gap g0
        rows = {k: np.zeros(T) for k in agg}
        # reported marks: RAME quarterly Geltner on the true-asset ramp (lag in quarters)
        rep_q = {}
        if state == "T4prime" and o["marks"] == "rame":
            v = comp["true"][sec]
            lv = [1.0 + v * min(q, 4) / 4.0 for q in range(0, 13)]
            r_true = [lv[q] / lv[q - 1] - 1.0 for q in range(1, 13)]
            lag = sl["lag"]
            r_l = [0.0] * lag + r_true
            prev = 0.0
            lvl = 1.0
            for q in range(12):
                prev = sl["lam"] * prev + (1.0 - sl["lam"]) * r_l[q]
                new = lvl * (1 + prev)
                rep_q[3 * (q + 1)] = (new - lvl)           # change in reported asset index at month 3(q+1)
                lvl = new
        for t in range(T):
            if mode == "g15" or state != "T4prime":
                mark = 0.0
                if state == "T4prime":
                    mark = B.T4_MARKS[sec].get(t, 0.0)
                nav *= 1.0 + sl["g_n"] / 12.0 * (1.0 if state in ("normal", "drought") else 0.0)
                nav *= 1.0 + mark
            else:
                if o["marks"] == "g15":
                    nav *= 1.0 + B.T4_MARKS[sec].get(t, 0.0)
                else:
                    nav += gav0 * rep_q.get(t, 0.0)          # $ change on the original asset base, debt fixed
            # state drivers
            if state == "T4prime":
                in_cr = t < (comp["crisis_months"] if mode == "canonical" else 23)
                inc_f = (comp["inc"][sec] if mode == "canonical" else B.T4_INC[sec]) if in_cr else 1.0
                real = (comp["exit_factor"] if mode == "canonical" else 0.45 * (1 - B.THETA0)) * sl["real_d"] \
                    if in_cr else sl["real_d"]
                cmult = (comp["call_mult"] if mode == "canonical" else
                         (o["call_axis"] if o["call_axis"] is not None else 1.0 + 0.5 * B.THETA0)) if t < 24 else 1.0
                crate = _monthly(CALL_RA["drought"] * cmult)
                tv = (comp["true"][sec] if mode == "canonical" else B.T4_TRUE[sec]) * min(1.0, (t + 1) / 12.0)
                stressed = t < 24
                ltvmax = (comp["ltv"][sec] if mode == "canonical" else B.LTV_S[sec]) if stressed else B.LTV_N[sec]
                avail = (comp["avail"] if stressed else B.AVAIL_N) if (mode == "canonical" and o["availability"]) \
                    else 1.0
                ext = (comp["ext"] if stressed else B.EXT_N) if o["ext"] is None else o["ext"]
            else:
                inc_f = 1.0
                real = sl["real_n"] if state == "normal" else sl["real_d"]
                crate = _monthly(CALL_RA["normal" if state == "normal" else "drought"])
                tv = 0.0
                ltvmax = B.LTV_N[sec]
                avail, ext = 1.0, 0.0
            inc = sl["inc"] * inc_f * nav / 12.0
            rea = _monthly(real) * nav
            call = crate * unf
            unf -= call
            unf += sl["commit"] * commit_m[t] * (1.0 if sold <= 0 else 1.0)
            cure = prot = stop = loss = sf = 0.0
            if debt > 0:
                d_m = debt * B.MATURITY_PA / 12.0
                v_m = d_m * coll * (1.0 + tv)
                refi = avail * min(d_m, ltvmax * v_m) + (1.0 - avail) * ext * d_m
                gap = max(0.0, d_m - refi)
                if sl["direct"]:
                    cure = gap
                    debt -= cure
                elif o["fund_module"] != "off" and gap > 0:
                    sf = gap
                    if o["fund_module"] == "upper":
                        cure = gap                           # upper bound: every fund shortfall is cash
                        debt -= gap
                    else:
                        prot = min(gap, unf)
                        unf -= prot
                        rem = gap - prot
                        stop = min(rem, inc + rea)
                        rem -= stop
                        loss = 0.25 * rem                    # assets sold at a 20% discount repay the rest
                        debt -= gap
            nav += call + cure + prot - rea - loss
            vt += call + cure + prot - rea * (vt / max(nav + rea, 1e-9)) - loss \
                + (gav0 * ((tv - (rows_tv_prev if t > 0 else 0.0))) if state == "T4prime" else 0.0)
            rows_tv_prev = tv
            rows["income"][t], rows["realiz"][t], rows["calls"][t] = inc, rea, call
            rows["prot_calls"][t], rows["cures"][t], rows["dist_stop"][t], rows["nav_loss"][t] = prot, cure, stop, loss
            rows["nav_rep"][t], rows["nav_true"][t], rows["debt"][t], rows["unf"][t] = nav, vt, debt, unf
            rows["shortfall_fund"][t] = sf
            rows["cashout"][t] = cash_out if t == 0 else 0.0
        per[sl["id"]] = rows
        for k in agg:
            agg[k] += rows[k]
    agg["net"] = agg["income"] + agg["realiz"] - agg["dist_stop"] + agg["cashout"] - agg["calls"] \
        - agg["prot_calls"] - agg["cures"]
    agg["per"] = per
    agg["comp"] = comp
    return agg


def ra_summary(agg: dict, h: int) -> dict:
    keys = ("income", "realiz", "calls", "prot_calls", "cures", "dist_stop", "nav_loss", "shortfall_fund", "cashout")
    out = {k: float(agg[k][:h].sum()) for k in keys}
    out["dist"] = out["income"] + out["realiz"] - out["dist_stop"]
    out["net"] = float(agg["net"][:h].sum())
    out["nav_rep_end"] = float(agg["nav_rep"][h - 1])
    out["nav_true_end"] = float(agg["nav_true"][h - 1])
    return out


# ================================================================================================= ladder
def gl_ladder(s: E.Stress, lev: dict | None = None, T: int = 36, pol: E.Policy | None = None,
              theta: float | None = None, ra_opts: dict | None = None) -> dict:
    """Monthly survival ladder on the t0 synthetic book, group-resolved (g01_core.gl_ladder generalised).
    theta: the s* parameter of `s` (needed for the theta-indexed RA leg; defaults to 0.76)."""
    if lev is None:
        lev = lev_from_policy(pol if pol is not None else E.Policy("A"))
    book = lev.get("book", "v1")
    has_ra = B.BOOKS[book]["ra"]
    WN = w_new(book)
    P = E.Policy("x", rcf=lev["rcf"], navf=lev["navf"])
    eq = np.zeros(T)
    if s.instant:
        eq[0] = -s.eq_drawdown
    else:
        shape = np.array([0.15, 0.12, 0.08, 0.05, 0.04, 0.03])
        shape = shape / shape.sum()
        eq[:6] = np.exp(shape * math.log(1 - s.eq_drawdown)) - 1
    eq[12:24] = 0.02
    eq[24:] = 0.008
    fi = np.zeros(T)
    fi[:3] = -0.02
    fi[3:] = 0.005
    hf_r = np.zeros(T)
    if s.instant:
        hf_r[0] = 0.3 * (-s.eq_drawdown) - 0.06
    else:
        hf_r[:4] = -0.03
    hf_r[12:] = 0.008
    pm = np.zeros(T)
    for mth, v in s.priv_marks:
        pm[mth] = v
    pm[14::3] = 0.01
    crisis = np.arange(T) < s.crisis_months

    def mult_at(table, t, default):
        acc = 0
        for months, mlt in table:
            if t < acc + months:
                return mlt
            acc += months
        return default

    priv0 = B.book_priv(book, lev.get("ra_scale", 1.0))
    unf_b = B.book_unf(book, lev.get("ra_scale", 1.0))
    if lev.get("census", "v1") == "gap02" and book == "v1":
        unf0, sec_def0, pc_rev0 = dict(E.UNF0), E.SEC_DEF0, E.PC_REV0
    else:
        unf0 = {g: unf_b[g] for g in PRIV}
        sec_def0, pc_rev0 = B.SEC_DEF_V1, B.PC_REV_V1
    priv_t0 = {g: priv0[g] for g in PRIV}

    tre = E.TRE0 + lev["cash_t0"]
    dm, em, fi_b = E.LO0["dm"], E.LO0["em"], E.LO0["fi"]
    hf0 = E.HF0
    priv = dict(priv_t0)
    unf = dict(unf0)
    proceeds = {g: 0.0 for g in ("pe", "sec", "co", "cs", "pc", "pm", "ra")}
    if lev["amber_t0"] > 0:
        tot = priv_t0["pc"] + priv_t0["cs"]
        for g in ("pc", "cs"):
            amt = lev["amber_t0"] * priv_t0[g] / tot
            tre += amt * E.PRICE_N[g]
            proceeds[g] += amt * E.PRICE_N[g]
            unf[g] *= 1 - amt / priv_t0[g]
            priv[g] -= amt
    if lev["sma_sell"] > 0:
        tre += lev["sma_sell"] * P_SMA
        proceeds["pc"] += lev["sma_sell"] * P_SMA
        priv["pc"] -= lev["sma_sell"]
    if lev["cs_synd"] > 0:
        tre += lev["cs_synd"] * P_CS
        proceeds["cs"] += lev["cs_synd"] * P_CS
        unf["cs"] *= 1 - lev["cs_synd"] / priv_t0["cs"]
        priv["cs"] -= lev["cs_synd"]
    for g in ("pe", "sec", "co"):
        amt = lev["red"][g]
        if amt > 0:
            tre += amt * lev["red_bid"][g]
            proceeds[g] += amt * lev["red_bid"][g]
            unf[g] *= 1 - amt / priv_t0[g]
            priv[g] -= amt
    if lev["hf_sell"] > 0:
        tre += lev["hf_sell"] * P_HF
        proceeds["pm"] += lev["hf_sell"] * P_HF
        hf0 -= lev["hf_sell"]
    for g in PRIV:
        if g == "co":
            tre -= lev["new_commit"]["co"]
            priv["co"] += lev["new_commit"]["co"]
        else:
            unf[g] += lev["new_commit"][g]
    # ---------------- Real Assets t0 actions (JV sell-down, ENR SELL, RE LP sale, cash-out)
    ra = None
    ra_sell = {}
    if has_ra:
        if lev["ra_jv"] > 0:                       # partial SELL of controlled equity, pro rata across controlled
            ctrl = {sl["id"]: sl["nav"] * lev.get("ra_scale", 1.0) * sl["ctrl"] for sl in B.SLEEVES if sl["ctrl"] > 0}
            tot = sum(ctrl.values())
            for k, v in ctrl.items():
                ra_sell[k] = ra_sell.get(k, 0.0) + lev["ra_jv"] * v / tot
            tre += lev["ra_jv"] * P_JV_T0
            proceeds["ra"] += lev["ra_jv"] * P_JV_T0
        if lev["enr_sell"] > 0:
            ra_sell["ENR_CE"] = ra_sell.get("ENR_CE", 0.0) + lev["enr_sell"]
            tre += lev["enr_sell"] * lev["enr_bid"]
            proceeds["ra"] += lev["enr_sell"] * lev["enr_bid"]
        if lev["ra_re_sell"] > 0:
            ra_sell["RE_CE"] = ra_sell.get("RE_CE", 0.0) + lev["ra_re_sell"]
            tre += lev["ra_re_sell"] * lev["ra_re_bid"]
            proceeds["ra"] += lev["ra_re_sell"] * lev["ra_re_bid"]
    n_syn = E.N_SYN0 + lev["p2s"]
    if lev["p2s"] > 0:
        dm -= lev["p2s"]
        tre += lev["p2s"] * 0.998
    enc0 = E.IM_N * n_syn + E.OPP_IM0 - lev["ovl_im"]
    top = max(0.0, lev["reserve"] * E.NAV0 - (tre - enc0)) + lev["reserve_add"]
    a = min(top / 0.998, dm)
    dm -= a
    tre += a * 0.998
    tre -= lev["rcf"] * P.rcf_upfront + lev["navf"] * P.navf_upfront

    # ---------------- RA leg (monthly), with plan pacing and stage-cut levers
    if has_ra:
        commit_m = np.zeros(T)
        for t in range(T):
            k = lev["pace"] / 12 * WN["ra"]
            active = t >= lev["cut_from"] and crisis[t]
            commit_m[t] = k * (1 - (lev["cut"]["ra"] if active else 0.0)) + (lev["new_commit"]["ra"] if t == 0 else 0.0)
        ro = dict(ra_opts or {})
        ro.setdefault("nav_scale", lev.get("ra_scale", 1.0))
        ro["sell"] = ra_sell
        ro["cashout_t0"] = lev["ra_cashout"]
        ra = ra_leg(theta if theta is not None else B.THETA0, T=T, mode=ro.pop("mode", "canonical"),
                    state="T4prime", commit_m=commit_m, opts=ro)   # cash-out cash enters the month-0 flow row

    eq_idx = 1.0
    im = E.IM_N * n_syn
    sec_def, pc_rev = sec_def0, pc_rev0
    ro_book = lev["sma_ro"]
    priv_m = dict(priv)
    basis = E.NAV0
    nco = 0.0
    liq_bh = dict(tre=tre, dm=dm, em=em, fi=fi_b, hf=hf0)
    rows = []
    gf = {g: dict(dist=np.zeros(T), calls=np.zeros(T)) for g in PRIV + ("ra",)}
    ovl = dict(vm=np.zeros(T), dim=np.zeros(T), tail=np.zeros(T), prem=np.zeros(T), opp=np.zeros(T),
               fut=np.zeros(T))
    cfv = dict(draw=np.zeros(T), opex=np.zeros(T), fee=np.zeros(T))
    withheld = 0.0
    for t in range(T):
        for g in priv_m:
            priv_m[g] *= 1 + pm[t]
        ro_book *= 1 + pm[t]
        dist = 0.0
        for g in ("pe", "sec", "co"):
            r = E.DROUGHT_DIST[g] * mult_at(s.dist_mult_pe, t, 1.0)
            d = _monthly(min(0.95, r)) * priv_m[g]
            priv_m[g] -= d
            dist += d
            gf[g]["dist"][t] += d
        for g, r in (("pc", s.pc_cs_rates[0]), ("cs", s.pc_cs_rates[1])):
            r_eff = r if crisis[t] else E.DIST_NORMAL[g] * 0.92
            d = _monthly(r_eff) * priv_m[g]
            priv_m[g] -= d
            dist += d
            gf[g]["dist"][t] += d
        if ro_book > 0:
            d = _monthly(RUNOFF_C if crisis[t] else RUNOFF_T) * ro_book
            ro_book -= d
            priv_m["pc"] -= d
            dist += d
            gf["pc"]["dist"][t] += d
        crate = _monthly(min(0.95, 0.28 * mult_at(s.call_mult, t, 1.0)))
        calls = 0.0
        for g in unf:
            c = crate * unf[g]
            unf[g] -= c
            priv_m[g] += c
            calls += c
            gf[g]["calls"][t] += c
        if t in (2, 5, 8, 11):
            calls += sec_def0 / 4
            gf["sec"]["calls"][t] += sec_def0 / 4
        rev = min(pc_rev, 0.5 * pc_rev0 / 3 if t < 3 else _monthly(0.15) * pc_rev)
        pc_rev -= rev
        calls += rev
        gf["pc"]["calls"][t] += rev
        k = lev["pace"] / 12
        active = t >= lev["cut_from"] and crisis[t]
        for g in ("pe", "sec", "pc", "cs"):
            unf[g] += WN[g] * k * (1 - (lev["cut"][g] if active else 0.0))
        c_co = WN["co"] * k * (1 - (lev["cut"]["co"] if active else 0.0))
        calls += c_co
        gf["co"]["calls"][t] += c_co
        if ra is not None:                                  # RA: distributions net of stops; calls incl. cures
            d_ra = ra["income"][t] + ra["realiz"][t] - ra["dist_stop"][t] + ra["cashout"][t]
            c_ra = ra["calls"][t] + ra["prot_calls"][t] + ra["cures"][t]
            dist += d_ra
            calls += c_ra
            gf["ra"]["dist"][t] += d_ra
            gf["ra"]["calls"][t] += c_ra
        fy = t // 12
        rate = s.draw_rates[min(fy, len(s.draw_rates) - 1)]
        rate0 = rate
        if crisis[t] and lev["band"] > 0:
            rate = lev["band"] * 0.05 + (1 - lev["band"]) * rate
        if fy == 1:
            rate += s.override_y2
            rate0 += s.override_y2
        ra_nav_rep = float(ra["nav_rep"][t]) if ra is not None else 0.0
        nav_now_est = sum(liq_bh.values()) + sum(priv_m.values()) + ra_nav_rep - nco
        if s.draw_basis == "fixed_usd":
            base = E.NAV0
        elif s.draw_basis == "current":
            base = max(nav_now_est, 1e-9)
        else:
            if t % 12 == 0:
                lag_priv = sum(priv_m.values()) / (1 + (pm[max(t - 1, 0)] + pm[max(t - 2, 0)] + pm[max(t - 3, 0)]))
                basis = (nav_now_est - sum(priv_m.values()) + lag_priv) if t > 0 else E.NAV0
            base = basis
        draw = rate * base / 12
        withheld += (rate0 - rate) * base / 12
        vm = n_syn * eq_idx * eq[t]
        eq_idx *= 1 + eq[t]
        im_new = (E.IM_S if (crisis[t] and t < s.im_months) else E.IM_N) * n_syn * eq_idx
        d_im = im_new - im
        im = im_new
        prem = E.TAIL_PREM * E.NAV0 / 12
        tail = 0.0
        if t in (1, 5):
            tail = 0.5 * E.N_TAIL * min(0.18, max(0.0, 0.90 - eq_idx))
        opp = 0.015 * E.NAV0 / 3 if t < 3 else 0.0
        fut = lev["p2s"] * eq_idx * (E.FUT_SPREAD_S if crisis[t] else E.FUT_SPREAD_N) / 12
        fee = lev["rcf"] * P.rcf_undrawn_fee / 12 + lev["navf"] * P.navf_undrawn_fee / 12
        opex = 0.001 * E.NAV0 / 12
        net = draw + calls + prem + opp + fee + opex + fut + max(0.0, d_im) - dist - vm - tail - max(0.0, -d_im)
        nco += net
        ovl["vm"][t], ovl["dim"][t], ovl["tail"][t], ovl["prem"][t], ovl["opp"][t], ovl["fut"][t] = \
            vm, d_im, tail, prem, opp, fut
        cfv["draw"][t], cfv["opex"][t], cfv["fee"][t] = draw, opex, fee
        sec_def_left = sec_def0 * (1 - sum(1 for m_ in (2, 5, 8, 11) if m_ <= t) / 4)
        rows.append(dict(net=net, nco=nco, draw=draw, calls=calls, dist=dist, vm=vm, tail=tail, nav=nav_now_est,
                         ra_nav_rep=ra_nav_rep, ra_nav_true=float(ra["nav_true"][t]) if ra is not None else 0.0,
                         priv_rep=sum(priv_m.values()),
                         unf=sum(unf.values()) + sec_def_left + pc_rev + (float(ra["unf"][t]) if ra is not None else 0.0)))
        for kk, f in (("tre", 0.0), ("dm", eq[t]), ("em", 1.2 * eq[t]), ("fi", fi[t]), ("hf", hf_r[t])):
            liq_bh[kk] *= 1 + f

    idx_eq = np.cumprod(1 + eq)
    idx_em = np.cumprod(1 + 1.2 * eq)
    idx_fi = np.cumprod(1 + fi)
    idx_hf = np.cumprod(1 + hf_r)
    cbc = np.zeros(T)
    hf_monthly = np.zeros(T + 40)
    for q, share in enumerate(E.HF_SCHED):
        for mm in range(3):
            hf_monthly[3 * q + mm] += share / 3
    hf_cash = np.zeros(T)
    backlog = 0.0
    for t in range(T):
        due = hf_monthly[t] * hf0 * idx_hf[t] + backlog
        paid = s.hf_pass * due if crisis[t] else due
        backlog = due - paid
        hf_cash[t] = paid
    cum_hf = np.cumsum(hf_cash)
    acc_dm = acc_fi = acc_em = 0.0
    rem_dm = rem_fi = rem_em = 1.0
    tre_cap = tre - enc0
    tre_haircut = 0.4 * 0.0 + 0.27 * 0.02 + 0.33 * 0.10
    comp = dict(tre=np.zeros(T), lo=np.zeros(T), hf=np.zeros(T))
    for t in range(T):
        f = min(0.5, rem_dm)
        rem_dm -= f
        acc_dm += f * dm * idx_eq[t] * (1 - 0.015)
        f = min(0.5, rem_fi)
        rem_fi -= f
        acc_fi += f * fi_b * idx_fi[t] * (1 - 0.05)
        if t >= 1:
            f = min(0.5, rem_em)
            rem_em -= f
            acc_em += f * em * idx_em[t] * (1 - 0.05)
        cbc[t] = tre_cap * (1 - tre_haircut) + acc_dm + acc_fi + acc_em + cum_hf[t]
        comp["tre"][t], comp["lo"][t], comp["hf"][t] = tre_cap * (1 - tre_haircut), acc_dm + acc_fi + acc_em, cum_hf[t]
    nco_arr = np.array([r["nco"] for r in rows])
    nav_arr = np.array([r["nav"] for r in rows])
    floor_arr = s.floor * nav_arr
    fac = np.array([0.0 if t < 1 else lev["rcf"] * s.fac_credit for t in range(T)])
    pool = min(0.20 * sum(priv_t0.values()), priv_t0["pe"] + priv_t0["sec"])
    navf_cap = np.array([0.0 if t < 1 else min(lev["navf"], s.navf_ltv * pool) for t in range(T)])
    head_tp = cbc - floor_arr - nco_arr
    head_tpf = head_tp + fac + navf_cap

    def first_breach(head):
        br = np.where(head < 0)[0]
        return int(br[0] + 1) if br.size else None

    gap = np.maximum(0.0, -(head_tp[1:24] + navf_cap[1:24]))
    return dict(head_tp=head_tp, head_tpf=head_tpf, cbc=cbc, nco=nco_arr, nav=nav_arr, floor=floor_arr, fac=fac,
                navf=navf_cap, gf=gf, ovl=ovl, cf=cfv, proceeds=proceeds, comp=comp, withheld24=withheld,
                SH_TP=first_breach(head_tp), SH_TPF=first_breach(head_tpf),
                min_head_tpf_24=float(head_tpf[:24].min()), argmin_24=int(np.argmin(head_tpf[:24]) + 1),
                fac_need_24=float(gap.max() / s.fac_credit) if gap.size else 0.0,
                gstar=float((-head_tp[:24]).max()), nco24=float(nco_arr[23]), tre_t0=tre, enc0=enc0,
                usable_t0=tre - enc0, ra=ra, rows=rows, priv_t0=priv_t0, unf0=unf0, book=book)


# ================================================================================================= levers, cards
def _cut_months(s: E.Stress) -> int:
    return sum(1 for t in range(H_ROWS) if t >= 2 and t < s.crisis_months)


def levers(s: E.Stress, book: str) -> list:
    nm = _cut_months(s) / 12.0
    WN = w_new(book)
    L = []
    groups = [("pe", 0.75), ("co", 1.0), ("sec", 1.0), ("pc", 1.0), ("cs", 1.0)]
    if B.BOOKS[book]["ra"]:
        groups.append(("ra", 1.0))
    for g, cap in groups:
        a, d = ALPHA_D[g]
        forgone = 12.0 * WN[g] * nm
        L.append(dict(key=f"pace_{g}", owner=g, unit="share of group flow cut (stage rule)", cap=cap,
                      cost=a * d * forgone, ig=0.0,
                      apply=(lambda lev, x, g=g: lev["cut"].__setitem__(g, x)), step=0.5,
                      note="PE: protected core 25%; RA: pacing stop (no new closed-end commitments)"))
    L += [
        dict(key="sma_sell", owner="pc", unit="$bn SMA loans sold at 0.96", cap=SMA_SLEEVE, cost=1 - P_SMA,
             ig=P_SMA, apply=lambda lev, x: lev.__setitem__("sma_sell", x), step=2.0, note="alpha* ~0 (G6)"),
        dict(key="sma_ro", owner="pc", unit="$bn SMA book in run-off", cap=SMA_SLEEVE, cost=0.005, ig=0.0,
             apply=lambda lev, x: lev.__setitem__("sma_ro", x), step=2.0, note="C 5-8%/yr principal (G6)"),
        dict(key="cs_synd", owner="cs", unit="$bn sold down at 0.90", cap=0.25 * 8.0,
             cost=(1 - P_CS) + 0.10, ig=P_CS, apply=lambda lev, x: lev.__setitem__("cs_synd", x), step=1.0,
             note="discount + 2%/yr carry x 5y"),
        dict(key="ovl_im", owner="ovl", unit="$bn opportunistic IM released", cap=E.OPP_IM0,
             cost=0.15 * 0.0125 * E.NAV0 * 2 / E.OPP_IM0, ig=1.0,
             apply=lambda lev, x: lev.__setitem__("ovl_im", x), step=0.5, note="Sharpe 0.15 x 1.25% NAV vol x 2y"),
        dict(key="p2s", owner="pm", unit="$bn DM converted to futures", cap=0.5 * E.LO0["dm"],
             cost=0.0055 * 5 * (0.998 - E.IM_N), ig=0.998 - E.IM_S - 0.117,
             apply=lambda lev, x: lev.__setitem__("p2s", x), step=2.0, slope_cap0=True,
             note="no T4' credit for exposure kept through the s* rebound"),
        dict(key="reserve_add", owner="cf", unit="$bn Treasury top-up from DM", cap=0.06 * E.NAV0, cost=0.075,
             ig=1.0, apply=lambda lev, x: lev.__setitem__("reserve_add", x), step=2.0, note="1.5%/yr carry x 5y"),
        dict(key="rcf", owner="cf", unit="$bn committed revolver", cap=15.0, cost=0.009, ig=0.0,
             apply=lambda lev, x: lev.__setitem__("rcf", x), step=5.0, note="PIF $15bn precedent; SOFR+85bp"),
        dict(key="band", owner="own", unit="share of band (5% draw in crisis)", cap=1.0, cost=None, ig=0.0,
             apply=lambda lev, x: lev.__setitem__("band", x), step=1.0, note="0.065 per $ withheld (gap_02)"),
    ]
    if B.BOOKS[book]["ra"]:
        ctrl_nav = sum(sl["nav"] * sl["ctrl"] for sl in B.SLEEVES)
        L += [
            dict(key="ra_jv", owner="ra", unit="$bn controlled RA equity sold down at t0 (pre-arranged) at 0.92",
                 cap=JV_CAP_SHARE * ctrl_nav, cost=(1 - P_JV_T0) + 0.05, ig=P_JV_T0,
                 apply=lambda lev, x: lev.__setitem__("ra_jv", x), step=0.5,
                 note="partial SELL (RA2); controlled holdings only (V-RA-CTRL); discount + 1%/yr x 5y forgone"),
            dict(key="ra_cashout", owner="ra", unit="$bn cash-out at maturity, Q4-2026 maturities, controlled",
                 cap=sum(cashout_caps().values()), cost=0.044 * 5.0 * 0.5, ig=1.0,
                 apply=lambda lev, x: lev.__setitem__("ra_cashout", x), step=max(sum(cashout_caps().values()), 1e-6),
                 note="spread 4.4% (T regime) x ~2.5y average life; capacity = first-quarter maturities only"),
        ]
    return L


def cards(book: str, enr_hold: float = 0.84) -> list:
    C = [
        dict(key="sell_pe", owner="pe", bid=0.88, hold=0.95, size=0.5,
             apply=lambda lev, x: lev["red"].__setitem__("pe", x), name="PE: 2018 buyout fund (s4.4 example)"),
        dict(key="sell_sec", owner="sec", bid=0.87, hold=0.95, size=0.5,
             apply=lambda lev, x: lev["red"].__setitem__("sec", x), name="Secondaries: S3 LP interest"),
        dict(key="sell_co", owner="co", bid=0.75, hold=0.95, size=0.5,
             apply=lambda lev, x: lev["red"].__setitem__("co", x), name="Co-investment: strip"),
        dict(key="sell_hf", owner="pm", bid=P_HF, hold=0.95, size=0.5,
             apply=lambda lev, x: lev.__setitem__("hf_sell", x), name="Public Markets: HF secondary"),
    ]
    if B.BOOKS[book]["ra"]:
        C += [
            dict(key="sell_enr", owner="ra", bid=0.80, hold=enr_hold, size=0.7,
                 apply=lambda lev, x: lev.__setitem__("enr_sell", x),
                 name="RA: ENR fund-held levered upstream into the Gulf-war bid ($0.7bn)"),
            dict(key="sell_ra_re", owner="ra", bid=0.68, hold=0.70, size=0.5,
                 apply=lambda lev, x: lev.__setitem__("ra_re_sell", x),
                 name="RA: closed-end value-add RE LP interest at 68% (hold 69.4-70% per synthesis s7.4)"),
        ]
    return C


STATES = {
    "R0": dict(label="t0, group levers + reserve (no revolver, no band)", allow={"rcf": 0.0, "band": 0.0}),
    "R0x": dict(label="t0, group levers only (no reserve top-up)", allow={"rcf": 0.0, "band": 0.0, "reserve_add": 0.0}),
    "R1": dict(label="+ CF revolver signed (Mode B)", allow={"band": 0.0}),
    "R2": dict(label="+ owner band (Mode H)", allow={}),
    "I": dict(label="interim, reversible group levers only", allow={"rcf": 0.0, "band": 0.0, "sma_sell": 0.0,
                                                                     "cs_synd": 0.0, "ra_jv": 0.0}, cards=False),
}


def coefficients(s: E.Stress, base_lev: dict, theta: float, ra_opts: dict | None = None,
                 enr_hold: float = 0.84) -> dict:
    book = base_lev["book"]
    b = gl_ladder(s, base_lev, theta=theta, ra_opts=ra_opts)
    h0 = b["head_tpf"][:H_ROWS].copy()
    out = dict(h0=h0, base=b, lever={}, card={}, cash=None, commit={}, book=book, theta=theta,
               ra_opts=ra_opts, stress=s, enr_hold=enr_hold)
    for L in levers(s, book):
        lv = copy.deepcopy(base_lev)
        L["apply"](lv, L["step"])
        r = gl_ladder(s, lv, theta=theta, ra_opts=ra_opts)
        sl = (r["head_tpf"][:H_ROWS] - h0) / L["step"]
        if L.get("slope_cap0"):
            sl = np.minimum(sl, 0.0)
        cost = L["cost"]
        if L["key"] == "band":
            cost = 0.065 * r["withheld24"] / L["step"]
        out["lever"][L["key"]] = dict(slope=sl, cost=cost, cap=L["cap"], owner=L["owner"], ig=L["ig"],
                                      unit=L["unit"], note=L["note"])
    for C in cards(book, enr_hold):
        lv = copy.deepcopy(base_lev)
        C["apply"](lv, C["size"])
        r = gl_ladder(s, lv, theta=theta, ra_opts=ra_opts)
        out["card"][C["key"]] = dict(slope=(r["head_tpf"][:H_ROWS] - h0) / C["size"], bid=C["bid"], hold=C["hold"],
                                     size=C["size"], owner=C["owner"], name=C["name"], ig=C["bid"])
    lv = copy.deepcopy(base_lev)
    lv["cash_t0"] = 1.0
    out["cash"] = (gl_ladder(s, lv, theta=theta, ra_opts=ra_opts)["head_tpf"][:H_ROWS] - h0)
    for g in ("pe", "sec", "pc", "cs", "co") + (("ra",) if B.BOOKS[book]["ra"] else ()):
        lv = copy.deepcopy(base_lev)
        lv["new_commit"][g] = 1.0
        out["commit"][g] = -(gl_ladder(s, lv, theta=theta, ra_opts=ra_opts)["head_tpf"][:H_ROWS] - h0)
    return out


def ig_short_t0() -> float:
    return 0.08 * E.NAV0 - (E.TRE0 - E.IM_N * E.N_SYN0 - E.OPP_IM0)


def _build(coef, state, elastic, relax=(0.0, 0.0), penalty_scale=1.0, phase1=False, cards_on=True):
    allow = STATES[state]["allow"]
    cards_on = cards_on and STATES[state].get("cards", True)
    keys = list(coef["lever"])
    x = {k: cp.Variable(nonneg=True, name=k) for k in keys}
    cks = list(coef["card"])
    sv = {k: cp.Variable(nonneg=True, name=k) for k in cks}
    uS = cp.Variable(nonneg=True)
    uIG = cp.Variable(nonneg=True)
    head = [coef["h0"][h] + sum(coef["lever"][k]["slope"][h] * x[k] for k in keys)
            + sum(coef["card"][c]["slope"][h] * sv[c] for c in cks) for h in range(H_ROWS)]
    ig = sum(coef["lever"][k]["ig"] * x[k] for k in keys) + sum(coef["card"][c]["ig"] * sv[c] for c in cks)
    rows_h = [(head[h] + (uS if (elastic or phase1) else 0) >= -relax[0]) for h in range(H_ROWS)]
    row_ig = (ig + (uIG if (elastic or phase1) else 0) >= ig_short_t0() - relax[1])
    cons = rows_h + [row_ig]
    for k in keys:
        cap = allow.get(k, coef["lever"][k]["cap"])
        cons.append(x[k] <= cap)
    cons.append(x["sma_sell"] + x["sma_ro"] <= SMA_SLEEVE)
    if "ra_jv" in x and "sell_enr" in sv:
        pass
    for c in cks:
        cons.append(sv[c] <= (coef["card"][c]["size"] if (cards_on and not phase1) else 0.0))
    cost = sum(coef["lever"][k]["cost"] * x[k] for k in keys)
    obj = sum((coef["card"][c]["bid"] - coef["card"][c]["hold"]) * sv[c] for c in cks) - cost
    if elastic:
        obj = obj - penalty_scale * (M_TIERS["S"] * uS + M_TIERS["IG"] * uIG)
    return x, sv, uS, uIG, rows_h, row_ig, cons, obj


def phase1(coef, state):
    x, sv, uS, uIG, rows_h, row_ig, cons, _ = _build(coef, state, elastic=False, phase1=True)
    cp.Problem(cp.Minimize(uS), cons).solve(solver=cp.HIGHS)
    u_s = max(0.0, float(uS.value))
    cp.Problem(cp.Minimize(uIG), cons + [uS <= u_s + 1e-9]).solve(solver=cp.HIGHS)
    u_ig = max(0.0, float(uIG.value))
    return dict(u_S_star=u_s, u_IG_star=u_ig, levers={k: float(v.value) for k, v in x.items()})


def solve(coef, state, elastic, relax=(0.0, 0.0), penalty_scale=1.0):
    x, sv, uS, uIG, rows_h, row_ig, cons, obj = _build(coef, state, elastic, relax, penalty_scale)
    prob = cp.Problem(cp.Maximize(obj), cons)
    prob.solve(solver=cp.HIGHS)
    mu = np.array([float(r.dual_value) for r in rows_h])
    sol = dict(status=prob.status, obj=float(prob.value), mu=mu, y_IG=float(row_ig.dual_value),
               x={k: float(v.value) for k, v in x.items()}, sell={k: float(v.value) for k, v in sv.items()},
               u_S=float(uS.value) if elastic else 0.0, u_IG=float(uIG.value) if elastic else 0.0,
               penalty_scale=penalty_scale, relax=list(relax), elastic=elastic, state=state)
    sol["y_cash"] = float(mu @ coef["cash"]) + sol["y_IG"]
    sol["cards"] = card_prices(coef, sol)
    return sol


def card_prices(coef, sol):
    out = []
    for c, d in coef["card"].items():
        rel = d["slope"] - d["bid"] * coef["cash"]
        y_rel = float(sol["mu"] @ rel)
        res = (d["hold"] - y_rel) / (1.0 + sol["y_cash"])
        out.append(dict(card=c, group=GROUP_NAME[d["owner"]], name=d["name"], bid=d["bid"], hold=d["hold"],
                        y_cash=sol["y_cash"], y_rel=y_rel, reservation_price=res,
                        action="SELL" if sol["sell"][c] > 1e-9 else "HOLD"))
    return out


def pinned_rows(sol, tol=1e-3):
    bad = []
    sc = sol["penalty_scale"]
    if sol["u_S"] > 1e-7 or float(sol["mu"].sum()) >= (1 - tol) * M_TIERS["S"] * sc:
        bad.append("T4'")
    if sol["u_IG"] > 1e-7 or sol["y_IG"] >= (1 - tol) * M_TIERS["IG"] * sc:
        bad.append("IG")
    return bad


def restore_and_solve(coef, state):
    p1 = phase1(coef, state)
    relax = (p1["u_S_star"] + 1e-6 if p1["u_S_star"] > 0 else 0.0,
             p1["u_IG_star"] + 1e-6 if p1["u_IG_star"] > 0 else 0.0)
    hard = solve(coef, state, elastic=False, relax=relax)
    el10 = solve(coef, state, elastic=True, relax=relax, penalty_scale=10.0)
    return dict(phase1=p1, restored=hard, restored_elastic_x10=el10)


def plan_lev(coef, sol, base_lev):
    lv = copy.deepcopy(base_lev)
    for k, v in sol["x"].items():
        L = next(L for L in levers(coef["stress"], coef["book"]) if L["key"] == k)
        L["apply"](lv, v)
    for C in cards(coef["book"], coef["enr_hold"]):
        C["apply"](lv, sol["sell"][C["key"]])
    return lv


def group_prices(coef, sol, base_lev, priced_on: str, d0: float) -> dict:
    """FTP, hurdles, envelopes (L4 budgets) and glide shares from a restored solution only (never pinned)."""
    if pinned_rows(sol):
        raise AssertionError("pinned dual: refuse to price")
    s = coef["stress"]
    mu = sol["mu"]
    lv = plan_lev(coef, sol, base_lev)
    r = gl_ladder(s, lv, theta=coef["theta"], ra_opts=coef["ra_opts"])
    hstar = int(np.argmin(r["head_tpf"][:H_ROWS]))
    out = {"priced_on": priced_on, "binding_months": [int(h + 1) for h in np.where(mu > 1e-9)[0]],
           "y_cash_5y": sol["y_cash"], "y_IG_5y": sol["y_IG"], "mu_sum_5y": float(mu.sum()), "groups": {}}
    relief = {}
    for k, v in sol["x"].items():
        o = coef["lever"][k]["owner"]
        relief[o] = relief.get(o, 0.0) + float(coef["lever"][k]["slope"][hstar] * v)
    for c, v in sol["sell"].items():
        o = coef["card"][c]["owner"]
        relief[o] = relief.get(o, 0.0) + float(coef["card"][c]["slope"][hstar] * v)
    tot_rel = sum(max(0.0, v) for v in relief.values())
    WN = w_new(coef["book"])
    grs = PRIV + (("ra",) if B.BOOKS[coef["book"]]["ra"] else ())
    for g in grs:
        a, d = ALPHA_D[g]
        charge_new = float(mu @ coef["commit"][g]) + (sol["y_IG"] if g == "co" else 0.0)
        nco_g = np.cumsum(r["gf"][g]["calls"] - r["gf"][g]["dist"])[:H_ROWS]
        nav_g = r["priv_t0"][g] if g != "ra" else B.book_priv(coef["book"], base_lev.get("ra_scale", 1.0))["ra"]
        charge_hold = float(mu @ nco_g) / nav_g
        out["groups"][g] = dict(
            name=GROUP_NAME[g],
            envelope_12m=float(np.sum(r["gf"][g]["calls"][:12] - r["gf"][g]["dist"][:12])),
            envelope_24m=float(np.sum(r["gf"][g]["calls"][:24] - r["gf"][g]["dist"][:24])),
            pacing_bn_yr=12.0 * WN[g] * (1 - lv["cut"][g]),
            ftp_new_bp_yr=1e4 * charge_new / 5.0, hurdle_bp_yr=1e4 * charge_new / d,
            ftp_hold_bp_yr=1e4 * charge_hold / 5.0,
            glide_share=(max(0.0, relief.get(g, 0.0)) / tot_rel) if tot_rel > 1e-9 else 0.0)
    ov = r["ovl"]
    use = (-ov["vm"] + ov["dim"] - ov["tail"] + ov["prem"] + ov["opp"] + ov["fut"])
    out["groups"]["ovl"] = dict(name="Overlay", envelope_12m=float(use[:12].sum()), envelope_24m=float(use[:24].sum()))
    out["plan_ladder"] = dict(SH_TP=r["SH_TP"], SH_TPF=r["SH_TPF"], min_head=r["min_head_tpf_24"],
                              argmin=r["argmin_24"])
    out["relief_by_owner"] = relief
    out["d0"] = d0
    out["plan_x"] = {k: v for k, v in sol["x"].items() if v > 1e-6}
    out["plan_sell"] = {k: v for k, v in sol["sell"].items() if v > 1e-6}
    out["recovery_hash"] = hashlib.sha256(json.dumps({"x": {k: round(v, 6) for k, v in sol["x"].items()},
                                                      "sell": {k: round(v, 6) for k, v in sol["sell"].items()},
                                                      "book": coef["book"], "theta": round(coef["theta"], 4)},
                                                     sort_keys=True).encode()).hexdigest()[:16]
    return out


def pools_budgets(s, lev, theta, ra_opts=None) -> dict:
    """L4 pool row (groups s2.4): sum_g B_g + B_OVL <= Pool_h = CBC_TP(h) + F(h) - D(h) - opex - fees - 0.04 W(h)."""
    r = gl_ladder(s, lev, theta=theta, ra_opts=ra_opts)
    ov = r["ovl"]
    use = (-ov["vm"] + ov["dim"] - ov["tail"] + ov["prem"] + ov["opp"] + ov["fut"])
    grs = PRIV + (("ra",) if B.BOOKS[lev["book"]]["ra"] else ())
    out = {g: dict(B12=float(np.sum(r["gf"][g]["calls"][:12] - r["gf"][g]["dist"][:12])),
                   B24=float(np.sum(r["gf"][g]["calls"][:24] - r["gf"][g]["dist"][:24]))) for g in grs}
    out["ovl"] = dict(B12=float(use[:12].sum()), B24=float(use[:24].sum()))
    for h in (12, 24):
        i = h - 1
        pool = float(r["cbc"][i] + r["fac"][i] + r["navf"][i] - r["cf"]["draw"][:h].sum() - r["cf"]["opex"][:h].sum()
                     - r["cf"]["fee"][:h].sum() - r["floor"][i])
        out.setdefault("pool", {})[f"{h}m"] = pool
        out.setdefault("slack", {})[f"{h}m"] = float(r["head_tpf"][i])
    out["SH_TP"], out["SH_TPF"] = r["SH_TP"], r["SH_TPF"]
    return out
