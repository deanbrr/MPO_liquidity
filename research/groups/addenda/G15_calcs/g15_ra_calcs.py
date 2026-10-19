"""
Stream G15 - Real Assets in the total portfolio: cash map row, liquidity ladder, open-end queue machine,
desmoothing and public-data checks.

*** ALL BOOK-LEVEL OUTPUTS ARE SYNTHETIC / ILLUSTRATIVE. NEVER ADIC DATA. ***

What it computes
  A. A synthetic Real Assets book (working allocation v2: NAV $18bn, unfunded $4bn; sectors confirmed by the
     user: real estate, infrastructure, energy & natural resources; vehicles: open-end and closed-end funds,
     co-investments, JVs and direct assets). Sleeve parameters are [I] defaults anchored on sourced data
     (see PARAMETER NOTES below and the G15 dossier).
  B. The Real Assets row of the cross-group cash map, monthly steps, first 12 and 24 months, in the groups
     report's states (normal, drought, S1 demand bust, T4' = s*(0.76) canonical) plus two oil-fiscal states
     (SG supply glut, GW Gulf war / export-volume shock).  Equity cures on maturing asset-level debt are
     modelled for the directly held sleeves.
  C. A PE-relabel comparison: the same NAV and unfunded run through the stream-G7 PE rates (what the v1 map
     implicitly assumed when the $18bn sat inside "PE funds").
  D. Liquidity-ladder entries by sleeve and state (SELL routes, JV sell-down, cash-out refinancing) and the
     counterbalancing capacity they add at 3 / 12 / 24 months, with a market-depth cap.
  E. An open-end redemption-queue state machine (quarterly, pro-rata) calibrated to NFI-ODCE 2023-26.
  F. Public-data checks (not synthetic): Geltner unsmoothing of NFI-ODCE quarterly returns 2022Q1-2026Q2;
     real returns of private real-asset indices vs US CPI 2022-2025; UAE residential property cycles (BIS via
     FRED) and their lead-lag with Brent.

Run:  <venv>/python.exe -I g15_ra_calcs.py     (writes g15_ra_results.json next to this file)
"""
from __future__ import annotations

import csv
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "g15_ra_results.json")
NOTE = "SYNTHETIC / ILLUSTRATIVE ONLY - not ADIC data (sections A-E). Section F uses public data."

# ------------------------------------------------------------------------------------------------
# Canonical conventions shared with the groups report (stream-G7 module and gap_02 s*(theta))
# ------------------------------------------------------------------------------------------------
THETA = 0.76
T4P_REAL_FACTOR = 0.45 * (1.0 - THETA)     # 0.108 x drought rates for exit-driven distributions
T4P_CALL_MULT = 1.0 + 0.5 * THETA          # 1.38 x calls
CALL = {"boom": 0.39, "normal": 0.29, "drought": 0.28, "crisis": 0.30}   # stream-G7 CALL table
PE_DIST = {"normal": 0.20, "drought": 0.11, "crisis": 0.035}             # stream-G7 DIST (PE)
S1_REAL_FACTOR = PE_DIST["crisis"] / PE_DIST["drought"]                  # 0.318, G7's crisis/drought ratio
MATURITY_PA = 0.17      # share of asset-level debt maturing per year (MBA: 17% of CRE balances mature in 2026)
NEW_COMMIT_PA = 1.2     # [I] RA closed-end commitments per year in the do-nothing book (~steady state: U* = pace /
                        #     call rate = 1.2 / 0.28-0.29 = $4.1-4.3bn, close to the working $4bn unfunded)


def monthly_rate(annual: float) -> float:
    return 1.0 - (1.0 - min(max(annual, 0.0), 0.99)) ** (1.0 / 12.0)


# ------------------------------------------------------------------------------------------------
# A. Synthetic Real Assets book (USD bn).  [I] unless noted.  Sum NAV = 18.0, unfunded = 4.0.
#   inc     : net cash income yield to ADIC on NAV (after fees, interest, capex reserves), normal state
#   real_n/d: exit-driven (realization) distribution rate on NAV, normal / drought
#   ltv     : look-through asset-level LTV (non-recourse debt / gross asset value)
#   g_n     : annual NAV appreciation in normal/drought states (marks)
#   direct  : True if ADIC itself funds equity cures on maturing asset-level debt
#   sector  : RE (global real estate), RE_GCC, INF (infrastructure), ENR (energy & natural resources)
#   commit  : share of NEW_COMMIT_PA flowing to this sleeve
# PARAMETER NOTES (sources in the dossier):
#   RE open-end core: NFI-ODCE income return 4.08% gross TTM 2Q26, leverage 27.1% (4Q25) -> 3.25% net cash.
#   RE closed-end VA/opp: real-estate fund distributions 7% of NAV (rolling year to 3Q25), ~1/3 of the 10-year
#     average (Ares, Feb 2026) -> total 7% drought, 19% normal (1% income + realizations).
#   Infra open-end core: bfinance target yield >= 6% (Infralogic, Jun 2026) -> 5.5% net cash.
#   Infra closed-end core-plus/VA: bfinance yields 4-5% (core/core-plus), 3-4% (VA) -> 4.0% income.
#   Energy & NR: oil-elastic income and realizations; private energy benchmark -20.5% in 2015 (Cambridge Assoc.).
# ------------------------------------------------------------------------------------------------
SLEEVES = [
    dict(id="RE_OE",      sector="RE",     vehicle="open-end core fund",           nav=2.7, unf=0.0, ltv=0.27,
         inc=0.0325, real_n=0.00, real_d=0.00, g_n=0.010, direct=False, commit=0.0),
    dict(id="RE_CE",      sector="RE",     vehicle="closed-end VA/opp fund",       nav=2.6, unf=1.2, ltv=0.60,
         inc=0.010, real_n=0.18, real_d=0.06, g_n=0.020, direct=False, commit=0.375),
    # ADIC-controlled JV/direct assets: no exogenous realizations in the HOLD baseline (sales are SELL actions)
    dict(id="RE_DIR_GL",  sector="RE",     vehicle="JV / direct (global)",         nav=1.7, unf=0.2, ltv=0.45,
         inc=0.030, real_n=0.00, real_d=0.00, g_n=0.010, direct=True,  commit=0.0),
    dict(id="RE_DIR_GCC", sector="RE_GCC", vehicle="JV / direct (GCC)",            nav=1.2, unf=0.2, ltv=0.45,
         inc=0.045, real_n=0.00, real_d=0.00, g_n=0.020, direct=True,  commit=0.0),
    dict(id="RE_COI",     sector="RE",     vehicle="co-investment",                nav=0.8, unf=0.0, ltv=0.60,
         inc=0.015, real_n=0.12, real_d=0.04, g_n=0.020, direct=True,  commit=0.0),
    dict(id="INF_OE",     sector="INF",    vehicle="open-end core fund",           nav=2.0, unf=0.0, ltv=0.50,
         inc=0.055, real_n=0.00, real_d=0.00, g_n=0.025, direct=False, commit=0.0),
    dict(id="INF_CE",     sector="INF",    vehicle="closed-end core-plus/VA fund", nav=2.5, unf=1.3, ltv=0.55,
         inc=0.040, real_n=0.08, real_d=0.04, g_n=0.040, direct=False, commit=0.4375),
    dict(id="INF_DIR",    sector="INF",    vehicle="direct / co-investment",       nav=2.0, unf=0.3, ltv=0.55,
         inc=0.050, real_n=0.02, real_d=0.01, g_n=0.030, direct=True,  commit=0.0),
    dict(id="ENR_CE",     sector="ENR",    vehicle="closed-end fund",              nav=1.6, unf=0.6, ltv=0.35,
         inc=0.040, real_n=0.10, real_d=0.06, g_n=0.030, direct=False, commit=0.1875),
    dict(id="ENR_DIR",    sector="ENR",    vehicle="direct / co-investment",       nav=0.9, unf=0.2, ltv=0.40,
         inc=0.070, real_n=0.00, real_d=0.00, g_n=0.020, direct=True,  commit=0.0),
]
assert abs(sum(s["nav"] for s in SLEEVES) - 18.0) < 1e-9
assert abs(sum(s["unf"] for s in SLEEVES) - 4.0) < 1e-9
assert abs(sum(s["commit"] for s in SLEEVES) - 1.0) < 1e-9

LTV_MAX = {"normal": {"RE": 0.60, "RE_GCC": 0.60, "INF": 0.65, "ENR": 0.55},
           "stress": {"RE": 0.50, "RE_GCC": 0.45, "INF": 0.55, "ENR": 0.45}}


# ------------------------------------------------------------------------------------------------
# B. States.  Each returns, per month t and sector, the drivers of the cash map.
#   regime(t)       -> call regime ('normal'|'drought'|'crisis')
#   call_mult(t)
#   inc_f(sec, t)   -> multiplier on the income yield
#   real(sl, t)     -> annual realization rate for the sleeve
#   mark(sec, t)    -> monthly reported mark change (appraisal-lagged)
#   true_v(sec, t)  -> cumulative TRUE value change since t0 (used by lenders at refinancing)
#   ltv_state(t)    -> 'normal' | 'stress' lender regime
# ------------------------------------------------------------------------------------------------
def _ramp(total: float, months: int, t: int) -> float:
    return total * min(1.0, (t + 1) / months)


def _quarterly_marks(t: int, schedule: dict) -> float:
    return schedule.get(t, 0.0)


STATES = {}


def st_normal():
    return dict(
        name="normal", regime=lambda t: "normal", call_mult=lambda t: 1.0,
        inc_f=lambda sec, t: 1.0,
        real=lambda sl, t: sl["real_n"],
        mark=lambda sec, t: 0.0, true_v=lambda sec, t: 0.0, ltv_state=lambda t: "normal")


def st_drought():
    return dict(
        name="drought", regime=lambda t: "drought", call_mult=lambda t: 1.0,
        inc_f=lambda sec, t: 1.0,
        real=lambda sl, t: sl["real_d"],
        mark=lambda sec, t: 0.0, true_v=lambda sec, t: 0.0, ltv_state=lambda t: "normal")


S1_MARKS = {"RE": {3: -0.05, 6: -0.05, 9: -0.03}, "RE_GCC": {3: -0.05, 6: -0.05, 9: -0.03},
            "INF": {3: -0.03, 6: -0.02}, "ENR": {3: -0.12, 6: -0.06}}
S1_TRUE = {"RE": -0.20, "RE_GCC": -0.22, "INF": -0.10, "ENR": -0.30}
S1_INC = {"RE": 0.92, "RE_GCC": 0.90, "INF": 0.97, "ENR": 0.65}


def st_s1():
    return dict(
        name="S1", regime=lambda t: "crisis" if t < 18 else "drought",
        call_mult=lambda t: 1.25 if t < 12 else 1.0,
        inc_f=lambda sec, t: S1_INC[sec] if t < 18 else 1.0,
        real=lambda sl, t: (S1_REAL_FACTOR * sl["real_d"]) if t < 18 else sl["real_d"],
        mark=lambda sec, t: _quarterly_marks(t, S1_MARKS[sec]),
        true_v=lambda sec, t: _ramp(S1_TRUE[sec], 9, t),
        ltv_state=lambda t: "stress" if t < 18 else "normal")


T4_MARKS = {"RE": {3: -0.06, 6: -0.06, 9: -0.04, 12: -0.03}, "RE_GCC": {3: -0.06, 6: -0.07, 9: -0.05, 12: -0.04},
            "INF": {3: -0.03, 6: -0.03, 9: -0.02}, "ENR": {3: -0.10, 6: -0.08, 9: -0.05}}
T4_TRUE = {"RE": -0.25, "RE_GCC": -0.30, "INF": -0.12, "ENR": -0.30}
T4_INC = {"RE": 0.85, "RE_GCC": 0.80, "INF": 0.92, "ENR": 0.60}


def st_t4p():
    return dict(
        name="T4prime", regime=lambda t: "drought",          # canonical: calls = (1+0.5 theta) x 28%
        call_mult=lambda t: T4P_CALL_MULT if t < 24 else 1.0,
        inc_f=lambda sec, t: T4_INC[sec] if t < 23 else 1.0,
        real=lambda sl, t: (T4P_REAL_FACTOR * sl["real_d"]) if t < 23 else sl["real_d"],
        mark=lambda sec, t: _quarterly_marks(t, T4_MARKS[sec]),
        true_v=lambda sec, t: _ramp(T4_TRUE[sec], 12, t),
        ltv_state=lambda t: "stress" if t < 24 else "normal")


def st_sg():
    """Oil supply glut / price war (stream 03 state SG): owner draw toward the cap; global markets fine;
    exits as today (drought); GCC real estate follows the fiscal cycle with a lag; energy assets fall."""
    def inc_f(sec, t):
        if sec == "RE_GCC":
            return 0.95 if t < 12 else 0.85
        if sec == "ENR":
            return 0.68              # 1 + 0.8 x (-40% oil)
        return 1.0

    def real(sl, t):
        if sl["sector"] == "RE_GCC":
            return 0.5 * sl["real_d"]
        if sl["sector"] == "ENR":
            return 0.3 * sl["real_d"]   # bid-ask gap: energy exits stall (CA 2016: dry powder +20%)
        return sl["real_d"]

    def mark(sec, t):
        if sec == "RE_GCC":
            return {5: -0.03, 11: -0.04, 17: -0.04, 23: -0.03}.get(t, 0.0)
        if sec == "ENR":
            return {2: -0.10, 5: -0.06, 8: -0.04}.get(t, 0.0)
        return 0.0

    def true_v(sec, t):
        if sec == "RE_GCC":
            return _ramp(-0.10, 12, t) + (_ramp(-0.05, 12, t - 12) if t >= 12 else 0.0)
        if sec == "ENR":
            return _ramp(-0.20, 6, t)
        return 0.0

    return dict(name="SG_supply_glut", regime=lambda t: "drought", call_mult=lambda t: 1.0, inc_f=inc_f,
                real=real, mark=mark, true_v=true_v,
                ltv_state=lambda t: "normal")


def st_gw():
    """Gulf war / export-volume shock (stream 03 state GW; 2026 analogue): oil up, Gulf transaction volumes
    collapse (Dubai Q3-2026 transactions -38% y/y, prices -5 to -15% since end-2025), global exits as today."""
    def inc_f(sec, t):
        if sec == "RE_GCC":
            return 0.90
        if sec == "ENR":
            return 1.25
        return 1.0

    def real(sl, t):
        if sl["sector"] == "RE_GCC":
            return 0.5 * sl["real_d"]
        return sl["real_d"]

    def mark(sec, t):
        if sec == "RE_GCC":
            return {5: -0.04, 11: -0.03}.get(t, 0.0)
        if sec == "ENR":
            return {2: 0.05, 5: 0.03}.get(t, 0.0)
        return 0.0

    def true_v(sec, t):
        if sec == "RE_GCC":
            return _ramp(-0.10, 9, t)
        return 0.0

    return dict(name="GW_gulf_war", regime=lambda t: "drought", call_mult=lambda t: 1.0, inc_f=inc_f, real=real,
                mark=mark, true_v=true_v,
                ltv_state=lambda t: "normal")   # GCC lenders assumed to keep normal LTVs in GW [I]


def get_state(name: str) -> dict:
    return {"normal": st_normal, "drought": st_drought, "S1": st_s1, "T4prime": st_t4p,
            "SG_supply_glut": st_sg, "GW_gulf_war": st_gw}[name]()


# ------------------------------------------------------------------------------------------------
# Engine: monthly sources and uses by sleeve
# ------------------------------------------------------------------------------------------------
def run_book(state_name: str, T: int = 24, new_commit_pa: float = NEW_COMMIT_PA, sleeves=None,
             call_mult_override: float | None = None) -> dict:
    st = get_state(state_name)
    if call_mult_override is not None:
        st["call_mult"] = lambda t: call_mult_override
    sleeves = sleeves or SLEEVES
    res = {}
    for sl in sleeves:
        nav = sl["nav"]
        unf = sl["unf"]
        debt = nav * sl["ltv"] / (1.0 - sl["ltv"])          # look-through asset-level debt
        ltv0 = sl["ltv"]
        acc = {k: np.zeros(T) for k in ("income", "realiz", "calls", "cures")}
        for t in range(T):
            sec = sl["sector"]
            # reported marks and appreciation
            nav *= 1.0 + sl["g_n"] / 12.0 * (1.0 if state_name in ("normal", "drought", "GW_gulf_war") else 0.0)
            nav *= 1.0 + st["mark"](sec, t)
            inc = sl["inc"] * st["inc_f"](sec, t) * nav / 12.0
            rea = monthly_rate(st["real"](sl, t)) * nav
            crate = monthly_rate(CALL[st["regime"](t)] * st["call_mult"](t))
            call = crate * unf
            unf -= call
            unf += sl["commit"] * new_commit_pa / 12.0
            # equity cures on maturing debt (only where ADIC funds the equity directly)
            cure = 0.0
            if sl["direct"] and debt > 0:
                d_m = debt * MATURITY_PA / 12.0
                v_m = d_m / ltv0 * (1.0 + st["true_v"](sec, t))
                cap = LTV_MAX[st["ltv_state"](t)][sec] * v_m
                cure = max(0.0, d_m - cap)
                debt -= cure
            nav += call + cure - rea
            acc["income"][t] = inc
            acc["realiz"][t] = rea
            acc["calls"][t] = call
            acc["cures"][t] = cure
        res[sl["id"]] = {k: v for k, v in acc.items()}
        res[sl["id"]]["nav_end"] = nav
        res[sl["id"]]["unf_end"] = unf
    return res


def summarize(res: dict, h: int) -> dict:
    out = {}
    tot = {"income": 0.0, "realiz": 0.0, "dist": 0.0, "calls": 0.0, "cures": 0.0, "net": 0.0}
    for sid, a in res.items():
        inc = float(a["income"][:h].sum())
        rea = float(a["realiz"][:h].sum())
        cal = float(a["calls"][:h].sum())
        cur = float(a["cures"][:h].sum())
        row = {"income": inc, "realiz": rea, "dist": inc + rea, "calls": cal, "cures": cur,
               "net": inc + rea - cal - cur}
        out[sid] = {k: round(v, 3) for k, v in row.items()}
        for k in tot:
            tot[k] += row[k]
    out["TOTAL"] = {k: round(v, 3) for k, v in tot.items()}
    by_sector = {}
    for sl in SLEEVES:
        s = sl["sector"].replace("_GCC", "")
        by_sector.setdefault(s, 0.0)
        by_sector[s] += out[sl["id"]]["net"]
    out["NET_BY_SECTOR"] = {k: round(v, 3) for k, v in by_sector.items()}
    return out


# ------------------------------------------------------------------------------------------------
# C. PE-relabel comparison (stream-G7 PE rates on the same NAV and unfunded)
# ------------------------------------------------------------------------------------------------
def pe_relabel(state_name: str, nav0: float, unf0: float, T: int, new_commit_pa: float = NEW_COMMIT_PA) -> dict:
    nav, unf = nav0, unf0
    dist = calls = 0.0
    for t in range(T):
        if state_name == "normal":
            d, reg, mult = PE_DIST["normal"], "normal", 1.0
        elif state_name in ("drought", "SG_supply_glut", "GW_gulf_war"):
            d, reg, mult = PE_DIST["drought"], "drought", 1.0
        elif state_name == "S1":
            d = PE_DIST["crisis"] if t < 18 else PE_DIST["drought"]
            reg = "crisis" if t < 18 else "drought"
            mult = 1.25 if t < 12 else 1.0
        elif state_name == "T4prime":
            d = T4P_REAL_FACTOR * PE_DIST["drought"] if t < 23 else PE_DIST["drought"]
            reg, mult = "drought", T4P_CALL_MULT
        else:
            raise ValueError(state_name)
        dd = monthly_rate(d) * nav
        cc = monthly_rate(CALL[reg] * mult) * unf
        unf -= cc
        unf += new_commit_pa / 12.0
        nav += cc - dd
        dist += dd
        calls += cc
    return {"dist": round(dist, 3), "calls": round(calls, 3), "net": round(dist - calls, 3)}


# ------------------------------------------------------------------------------------------------
# E. Open-end redemption-queue state machine (quarterly, pro-rata)
# ------------------------------------------------------------------------------------------------
QUEUE_STATES = {
    # Q0: other investors' queue (share of fund NAV); new: new requests per quarter; resc: rescission share of
    # queue per quarter; cap: redemption capacity per quarter (share of NAV); mark: quarterly NAV change path
    "normal":  dict(Q0=0.02, new=[0.010] * 8, resc=[0.05] * 8, cap=[0.030] * 8, mark=[0.003] * 8),
    "drought": dict(Q0=0.10, new=[0.015] * 8, resc=[0.08] * 8, cap=[0.012] * 8, mark=[0.001] * 8),
    "T4prime": dict(Q0=0.12, new=[0.035, 0.035, 0.030, 0.025, 0.015, 0.010, 0.010, 0.010],
                    resc=[0.01, 0.01, 0.02, 0.03, 0.05, 0.08, 0.10, 0.10],
                    cap=[0.006, 0.006, 0.008, 0.010, 0.012, 0.014, 0.015, 0.015],
                    mark=[-0.05, -0.05, -0.04, -0.03, -0.01, 0.0, 0.005, 0.005]),
    "SG_supply_glut": dict(Q0=0.10, new=[0.015] * 8, resc=[0.08] * 8, cap=[0.012] * 8, mark=[0.001] * 8),
}


def queue_machine(state: str, adic_share: float = 0.06) -> dict:
    """ADIC requests redemption of its whole stake (adic_share of fund NAV) at t0.  Returns cumulative fraction
    of the t0 stake value received by quarter (at the NAV prevailing when paid)."""
    p = QUEUE_STATES[state]
    q_other = p["Q0"]
    r_adic = adic_share
    nav_idx = 1.0
    received = []
    cum = 0.0
    for k in range(8):
        q_other = q_other * (1.0 - p["resc"][k]) + p["new"][k]
        nav_idx *= 1.0 + p["mark"][k]
        total = q_other + r_adic
        paid_total = min(p["cap"][k], total)
        share = r_adic / total if total > 0 else 0.0
        paid_adic = paid_total * share
        paid_other = paid_total - paid_adic
        q_other = max(0.0, q_other - paid_other)
        r_adic = max(0.0, r_adic - paid_adic)
        cum += paid_adic / adic_share * nav_idx      # value received relative to the t0 stake value
        received.append(round(cum, 4))
    return {"cum_value_received_by_quarter": received,
            "by_3m": received[0], "by_12m": received[3], "by_24m": received[7],
            "share_of_units_redeemed_24m": round(1.0 - r_adic / adic_share, 4)}


# ------------------------------------------------------------------------------------------------
# D. Liquidity-ladder entries (SELL / partial SELL / REFINANCE routes) by sleeve and state
#   ttc: months to first cash; cap_m: share of the t0 position that can be sold per month after ttc
#   (market depth); price: proceeds per $ of reported NAV (1 - haircut); p_succ: execution probability
# ------------------------------------------------------------------------------------------------
LADDER = {
    # sleeve: {state: (ttc, cap_m, price, p_succ)}
    "RE_OE_secondary":   {"normal": (3, 0.10, 0.96, 0.95), "drought": (3, 0.08, 0.94, 0.90),
                          "T4prime": (4, 0.04, 0.82, 0.60), "SG_supply_glut": (3, 0.08, 0.94, 0.90)},
    "RE_CE":             {"normal": (5, 0.06, 0.71, 0.85), "drought": (5, 0.05, 0.68, 0.80),
                          "T4prime": (7, 0.03, 0.475, 0.50), "SG_supply_glut": (5, 0.05, 0.68, 0.80)},
    "RE_DIR_GL":         {"normal": (6, 0.08, 0.95, 0.90), "drought": (7, 0.06, 0.90, 0.80),
                          "T4prime": (12, 0.03, 0.73, 0.50), "SG_supply_glut": (7, 0.06, 0.90, 0.80)},
    "RE_DIR_GCC":        {"normal": (6, 0.08, 0.93, 0.90), "drought": (7, 0.06, 0.90, 0.80),
                          "T4prime": (12, 0.03, 0.70, 0.45), "SG_supply_glut": (12, 0.03, 0.75, 0.50)},
    "RE_COI":            {"normal": (6, 0.06, 0.88, 0.85), "drought": (7, 0.05, 0.82, 0.75),
                          "T4prime": (12, 0.02, 0.60, 0.45), "SG_supply_glut": (7, 0.05, 0.82, 0.75)},
    "INF_OE_secondary":  {"normal": (3, 0.10, 0.97, 0.95), "drought": (3, 0.08, 0.96, 0.90),
                          "T4prime": (4, 0.05, 0.86, 0.65), "SG_supply_glut": (3, 0.08, 0.96, 0.90)},
    "INF_CE":            {"normal": (4, 0.08, 0.91, 0.90), "drought": (4, 0.07, 0.90, 0.85),
                          "T4prime": (7, 0.04, 0.72, 0.55), "SG_supply_glut": (4, 0.07, 0.90, 0.85)},
    "INF_DIR":           {"normal": (6, 0.08, 0.96, 0.90), "drought": (7, 0.06, 0.94, 0.85),
                          "T4prime": (12, 0.03, 0.82, 0.55), "SG_supply_glut": (7, 0.06, 0.94, 0.85)},
    "ENR_CE":            {"normal": (5, 0.06, 0.82, 0.85), "drought": (5, 0.06, 0.80, 0.80),
                          "T4prime": (8, 0.03, 0.55, 0.45), "SG_supply_glut": (8, 0.03, 0.60, 0.50)},
    "ENR_DIR":           {"normal": (6, 0.06, 0.90, 0.85), "drought": (6, 0.06, 0.88, 0.80),
                          "T4prime": (12, 0.02, 0.62, 0.45), "SG_supply_glut": (12, 0.02, 0.65, 0.45)},
}
LADDER_NAV = {"RE_OE_secondary": 2.7, "RE_CE": 2.6, "RE_DIR_GL": 1.7, "RE_DIR_GCC": 1.2, "RE_COI": 0.8,
              "INF_OE_secondary": 2.0, "INF_CE": 2.5, "INF_DIR": 2.0, "ENR_CE": 1.6, "ENR_DIR": 0.9}
# Market-depth caps per year on LP-led secondary sales by ADIC (share of 2025 global LP-led volume) [I]:
# core open-end RE LP-led volume $2.65bn and VA/opp $3.1bn in 2025 (Ares, Feb 2026).  ADIC <= 20% of a market.
DEPTH_CAP_PA = {"RE_OE_secondary": 0.20 * 2.65, "RE_CE": 0.20 * 3.1,
                "INF_OE_secondary": 0.5, "INF_CE": 1.5, "ENR_CE": 0.5}     # infra / energy caps are [I]
OE_QUEUE_MAP = {"RE_OE_secondary": 2.7, "INF_OE_secondary": 2.0}


def ladder_cbc(state: str, horizons=(3, 12, 24)) -> dict:
    """SELL-route counterbalancing capacity.  For open-end holdings the route is the better of (a) secondary sale
    and (b) redemption through the queue machine, never the sum."""
    out = {}
    qm = queue_machine(state) if state in QUEUE_STATES else None
    for k, table in LADDER.items():
        ttc, cap_m, price, ps = table[state]
        nav = LADDER_NAV[k]
        sold = np.zeros(25)
        cum_q = 0.0
        for m in range(1, 25):
            if m >= ttc:
                q = min(cap_m * nav, nav - cum_q)
                if k in DEPTH_CAP_PA:
                    q = min(q, DEPTH_CAP_PA[k] / 12.0)
                cum_q += q
            sold[m] = cum_q
        out[k] = {f"{h}m": round(float(sold[h] * price * ps), 3) for h in horizons}
        out[k]["price"] = price
        out[k]["ttc_m"] = ttc
        if k in OE_QUEUE_MAP and qm is not None:
            red = {f"{h}m": round(OE_QUEUE_MAP[k] * qm[f"by_{h}m"], 3) for h in horizons}
            out[k]["redemption_route"] = red
            out[k]["secondary_route"] = {f"{h}m": out[k][f"{h}m"] for h in horizons}
            for h in horizons:
                out[k][f"{h}m"] = max(out[k][f"{h}m"], red[f"{h}m"])
    tot = {f"{h}m": round(sum(v[f"{h}m"] for v in out.values()), 3) for h in horizons}
    out["TOTAL_SELL_ROUTES"] = tot
    return out


def true_nav_impact(state_name: str, month: int = 12) -> dict:
    """Change in TRUE (transaction-based) value by sector at `month`, $bn and % of RA NAV."""
    st = get_state(state_name)
    by = {}
    for sl in SLEEVES:
        dv = st["true_v"](sl["sector"], month - 1) * sl["nav"] / (1.0 - sl["ltv"])   # on gross asset value
        # equity absorbs the gross-value change (debt fixed), floored at -NAV
        de = max(dv, -sl["nav"])
        by.setdefault(sl["sector"], 0.0)
        by[sl["sector"]] += de
    tot = sum(by.values())
    return {"by_sector_bn": {k: round(v, 3) for k, v in by.items()}, "total_bn": round(tot, 3),
            "total_pct_of_RA_NAV": round(tot / 18.0, 4)}


def refinance_capacity(state: str) -> dict:
    """Cash-out refinancing and JV sell-down capacity on the directly held sleeves."""
    target = {"RE": 0.55, "RE_GCC": 0.55, "INF": 0.60, "ENR": 0.50}
    out = {}
    tot_cashout = tot_jv = 0.0
    for sl in SLEEVES:
        if not sl["direct"]:
            continue
        v = sl["nav"] / (1.0 - sl["ltv"])
        d = v - sl["nav"]
        sec = sl["sector"]
        if state in ("normal", "drought"):
            cashout = max(0.0, target[sec] * v - d)
            jv = 0.40 * sl["nav"] * (0.95 if state == "normal" else 0.92)
        elif state == "SG_supply_glut":
            ok = sec not in ("RE_GCC", "ENR")
            cashout = max(0.0, target[sec] * v - d) if ok else 0.0
            jv = 0.40 * sl["nav"] * (0.92 if ok else 0.75) * (1.0 if ok else 0.5)
        else:  # T4prime: lenders cut LTV; cash-out impossible; JV sell-down slow and discounted
            cashout = 0.0
            jv = 0.20 * sl["nav"] * 0.80
        out[sl["id"]] = {"cash_out_refi": round(cashout, 3), "jv_selldown_40pct": round(jv, 3)}
        tot_cashout += cashout
        tot_jv += jv
    out["TOTAL"] = {"cash_out_refi": round(tot_cashout, 3), "jv_selldown": round(tot_jv, 3)}
    return out


def leverage_metrics() -> dict:
    gav = sum(s["nav"] / (1.0 - s["ltv"]) for s in SLEEVES)
    debt = gav - 18.0
    direct_debt = sum(s["nav"] * s["ltv"] / (1.0 - s["ltv"]) for s in SLEEVES if s["direct"])
    return {"look_through_gross_asset_value": round(gav, 2), "look_through_debt": round(debt, 2),
            "look_through_LTV": round(debt / gav, 3), "debt_on_directly_held_sleeves": round(direct_debt, 2),
            "annual_maturities_direct": round(direct_debt * MATURITY_PA, 2),
            "annual_maturities_all": round(debt * MATURITY_PA, 2)}


# ------------------------------------------------------------------------------------------------
# F. Public-data checks
# ------------------------------------------------------------------------------------------------
ODCE_Q = [7.4, 4.8, 0.5, -5.0, -3.2, -2.7, -1.9, -4.8, -2.4, -0.4, 0.2, 1.2, 1.1, 1.0, 0.7, 0.9, 1.2, 1.5]
ODCE_LABELS = [f"{y}Q{q}" for y in range(2022, 2027) for q in range(1, 5)][:18]


def geltner(series_pct, phi):
    r = np.array(series_pct) / 100.0
    u = np.empty_like(r)
    u[0] = r[0]
    for t in range(1, len(r)):
        u[t] = (r[t] - phi * r[t - 1]) / (1.0 - phi)
    return u


def drawdown(r):
    idx = np.cumprod(1.0 + np.asarray(r))
    peak = np.maximum.accumulate(np.concatenate([[1.0], idx]))[1:]
    return float((idx / peak - 1.0).min())


def read_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        next(rd)
        for d, v in rd:
            if v.strip() in ("", "."):
                continue
            rows.append((d, float(v)))
    return rows


def public_checks() -> dict:
    out = {}
    # 1. Geltner unsmoothing of NFI-ODCE quarterly gross total returns (NCREIF, 2Q26 webinar chart labels)
    g = {"reported": {"drawdown": round(drawdown(np.array(ODCE_Q) / 100), 4),
                      "vol_q": round(float(np.std(np.array(ODCE_Q) / 100, ddof=1)), 4),
                      "ac1": round(float(np.corrcoef(ODCE_Q[:-1], ODCE_Q[1:])[0, 1]), 3)}}
    for phi in (0.5, 0.6, 0.7):
        u = geltner(ODCE_Q, phi)
        g[f"phi_{phi}"] = {"drawdown": round(drawdown(u), 4), "vol_q": round(float(np.std(u, ddof=1)), 4),
                           "min_q": round(float(u.min()), 4),
                           "min_q_label": ODCE_LABELS[int(np.argmin(u))]}
    out["odce_geltner"] = g
    # 2. Real returns vs US CPI (Dec/Dec)
    cpi = dict(read_csv(os.path.join(DATA, "fred_CPIAUCNS_monthly.csv")))
    dec = {y: cpi[f"{y}-12-01"] for y in range(2020, 2026)}
    infl = {y: dec[y] / dec[y - 1] - 1.0 for y in range(2021, 2026)}
    odce_cy = {}
    for y in (2022, 2023, 2024, 2025):
        qs = [ODCE_Q[i] for i, lab in enumerate(ODCE_LABELS) if lab.startswith(str(y))]
        odce_cy[y] = float(np.prod(1 + np.array(qs) / 100) - 1)
    odce_cy[2025] = 0.0379          # NCREIF 4Q25 release (exact)
    msci = {"private_RE": {2023: -0.060, 2024: -0.026, 2025: 0.023},
            "private_infra": {2023: 0.085, 2024: 0.064, 2025: 0.126},
            "private_NR": {2023: 0.016, 2024: 0.037, 2025: 0.049},
            "ACWI_RE": {2023: 0.095, 2024: 0.031, 2025: 0.073},
            "ACWI_infra": {2023: 0.048, 2024: 0.155, 2025: 0.221}}
    real = {"ODCE": {y: round((1 + r) / (1 + infl[y]) - 1, 4) for y, r in odce_cy.items()}}
    for k, v in msci.items():
        real[k] = {y: round((1 + r) / (1 + infl[y]) - 1, 4) for y, r in v.items()}
    cum_odce_22_24 = np.prod([1 + odce_cy[y] for y in (2022, 2023, 2024)]) / np.prod([1 + infl[y] for y in (2022, 2023, 2024)]) - 1
    cum_infra_23_25 = np.prod([1 + msci["private_infra"][y] for y in (2023, 2024, 2025)]) / np.prod([1 + infl[y] for y in (2023, 2024, 2025)]) - 1
    cum_re_23_25 = np.prod([1 + msci["private_RE"][y] for y in (2023, 2024, 2025)]) / np.prod([1 + infl[y] for y in (2023, 2024, 2025)]) - 1
    sep26 = cpi.get("2026-09-01")
    sep25 = cpi.get("2025-09-01")
    out["inflation"] = {"cpi_dec_dec": {y: round(v, 4) for y, v in infl.items()},
                        "cpi_2026_ytd_sep": round(sep26 / dec[2025] - 1, 4) if sep26 else None,
                        "cpi_yoy_sep2026": round(sep26 / sep25 - 1, 4) if (sep26 and sep25) else None,
                        "odce_calendar_nominal": {y: round(v, 4) for y, v in odce_cy.items()},
                        "real_returns": real,
                        "odce_cum_real_2022_24": round(float(cum_odce_22_24), 4),
                        "msci_private_infra_cum_real_2023_25": round(float(cum_infra_23_25), 4),
                        "msci_private_RE_cum_real_2023_25": round(float(cum_re_23_25), 4)}
    # 3. UAE residential property cycles (BIS via FRED) and Brent lead-lag
    uae = read_csv(os.path.join(DATA, "fred_QAEN628BIS_uae_resi_prices.csv"))
    brent = dict(read_csv(os.path.join(DATA, "fred_DCOILBRENTEU_quarterly_avg.csv")))
    dates = [d for d, _ in uae]
    vals = np.array([v for _, v in uae])

    def episode(d0, d1):
        sub = [(d, v) for d, v in uae if d0 <= d <= d1]
        pk = max(sub, key=lambda x: x[1])
        after = [(d, v) for d, v in sub if d >= pk[0]]
        tr = min(after, key=lambda x: x[1])
        return {"peak": pk, "trough": tr, "change": round(tr[1] / pk[1] - 1, 4)}
    cyc = {"2008_2011": episode("2007-01-01", "2011-12-31"), "2014_2020": episode("2014-01-01", "2020-12-31"),
           "rise_2020Q3_2024Q1": round(vals[-1] / dict(uae)["2020-07-01"] - 1, 4)}
    # lead-lag: 4-quarter log change of UAE prices vs 4-quarter log change of Brent lagged L quarters
    common = [d for d in dates if d in brent]
    up = np.array([dict(uae)[d] for d in common])
    br = np.array([brent[d] for d in common])
    lu = np.log(up)
    lb = np.log(br)
    du = lu[4:] - lu[:-4]
    db = lb[4:] - lb[:-4]
    corr = {}
    for L in range(0, 9):
        if L == 0:
            x, y = db, du
        else:
            x, y = db[:-L], du[L:]
        corr[L] = round(float(np.corrcoef(x, y)[0, 1]), 3)
    out["uae_property"] = {"cycles": cyc, "corr_4q_change_uae_vs_brent_lagged_L_quarters": corr,
                           "sample": f"{common[0]}..{common[-1]}, n_quarters={len(common)} (overlapping 4q changes)"}
    return out


# ------------------------------------------------------------------------------------------------
def main() -> None:
    res = {"note": NOTE,
           "conventions": {"theta": THETA, "t4p_realization_factor": T4P_REAL_FACTOR,
                           "t4p_call_mult": T4P_CALL_MULT, "s1_realization_factor": round(S1_REAL_FACTOR, 4),
                           "call_table": CALL, "maturity_pa": MATURITY_PA, "new_commit_pa": NEW_COMMIT_PA},
           "book": SLEEVES and [{k: v for k, v in s.items()} for s in SLEEVES],
           "leverage": leverage_metrics()}
    cash = {}
    for stn in ("normal", "drought", "S1", "T4prime", "SG_supply_glut", "GW_gulf_war"):
        r = run_book(stn, T=24)
        cash[stn] = {"12m": summarize(r, 12), "24m": summarize(r, 24)}
    res["cash_map"] = cash
    # pacing-cut variant (no new RA commitments) for T4'
    r0 = run_book("T4prime", T=24, new_commit_pa=0.0)
    res["cash_map_T4prime_no_new_commitments"] = {"12m": summarize(r0, 12)["TOTAL"], "24m": summarize(r0, 24)["TOTAL"]}
    # empirical-calls sensitivity: T4' with calls x1.0 (downturn calls historically fell, main report 2.3(d))
    r1 = run_book("T4prime", T=24, call_mult_override=1.0)
    res["cash_map_T4prime_calls_x1"] = {"12m": summarize(r1, 12)["TOTAL"], "24m": summarize(r1, 24)["TOTAL"]}
    res["true_value_impact_12m"] = {stn: true_nav_impact(stn, 12)
                                    for stn in ("S1", "T4prime", "SG_supply_glut", "GW_gulf_war")}
    res["true_value_impact_24m"] = {stn: true_nav_impact(stn, 24) for stn in ("SG_supply_glut",)}
    # PE-relabel comparisons
    rel = {}
    for stn in ("normal", "drought", "S1", "T4prime"):
        rel[stn] = {
            "PE_rates_U4.0": {"12m": pe_relabel(stn, 18.0, 4.0, 12), "24m": pe_relabel(stn, 18.0, 4.0, 24)},
            "PE_rates_U5.8_(0.32xNAV)": {"12m": pe_relabel(stn, 18.0, 0.32 * 18, 12),
                                         "24m": pe_relabel(stn, 18.0, 0.32 * 18, 24)},
            "PE_rates_U9.5_(0.53xNAV)": {"12m": pe_relabel(stn, 18.0, 0.53 * 18, 12),
                                         "24m": pe_relabel(stn, 18.0, 0.53 * 18, 24)},
        }
    res["pe_relabel"] = rel
    # ladder and refinancing
    res["ladder_sell_routes"] = {stn: ladder_cbc(stn) for stn in ("normal", "drought", "T4prime", "SG_supply_glut")}
    res["refinance_capacity"] = {stn: refinance_capacity(stn) for stn in ("normal", "drought", "T4prime", "SG_supply_glut")}
    res["queue_machine"] = {stn: queue_machine(stn) for stn in QUEUE_STATES}
    # open-end redemption cash by horizon on the synthetic OE holdings ($2.7bn RE + $2.0bn infra)
    oe = {}
    for stn in QUEUE_STATES:
        q = res["queue_machine"][stn]
        oe[stn] = {f"{h}": round((2.7 + 2.0) * q[f"by_{h}"], 3) for h in ("3m", "12m", "24m")}
    res["open_end_redemption_cash"] = oe
    res["public_checks"] = public_checks()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=str)
    # console summary
    print(NOTE)
    print("leverage:", res["leverage"])
    for stn, v in cash.items():
        t12, t24 = v["12m"]["TOTAL"], v["24m"]["TOTAL"]
        print(f"{stn:16s} 12m dist {t12['dist']:.2f} (inc {t12['income']:.2f}, real {t12['realiz']:.2f}) "
              f"calls {t12['calls']:.2f} cures {t12['cures']:.2f} net {t12['net']:+.2f} | 24m net {t24['net']:+.2f}"
              f" | by sector 12m {v['12m']['NET_BY_SECTOR']}")
    print("T4' without new commitments:", res["cash_map_T4prime_no_new_commitments"])
    print("T4' calls x1.0:", res["cash_map_T4prime_calls_x1"])
    print("true value impact 12m:", json.dumps(res["true_value_impact_12m"]))
    print("true value impact 24m:", json.dumps(res["true_value_impact_24m"]))
    for stn, v in rel.items():
        print("PE-relabel", stn, {k: (vv["12m"]["net"], vv["24m"]["net"]) for k, vv in v.items()})
    for stn, v in res["ladder_sell_routes"].items():
        print("ladder", stn, v["TOTAL_SELL_ROUTES"])
    for stn, v in res["refinance_capacity"].items():
        print("refi", stn, v["TOTAL"])
    for stn, v in res["queue_machine"].items():
        print("queue", stn, v["by_3m"], v["by_12m"], v["by_24m"], "units redeemed 24m", v["share_of_units_redeemed_24m"])
    print("OE redemption cash ($bn):", oe)
    print(json.dumps(res["public_checks"], indent=1, default=str))


if __name__ == "__main__":
    main()
