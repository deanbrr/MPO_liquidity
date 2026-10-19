"""
ra_integration_calcs COPY of ra_gap_01's ra_book.py (original untouched). ri: the only change is that the sealed
census v1.1 PE history is read from the local copy in this folder (sealed_pe_history_v1_1.csv, hash-checked by
ri_validate.py against groups gap_02's file).

ra_gap_01: shared book and parameter definitions for the integrated v2 re-run (eight groups).

SYNTHETIC - NOT ADIC DATA. Every balance, rate and parameter here is a working assumption (context s1A allocation
v2), a G10-G15 synthetic default or a design default [I]. Nothing here is ADIC data.

Contents
  BOOKS            v1 (seven groups, census v1.0 split, PE 52 / 27.4) and the two v2 books (PE 34 with unfunded
                   16.4 or 10.9; Real Assets 18 / 4.0; everything else unchanged).
  SLEEVES          the ten Real Assets census sleeves of record (RA synthesis s11 = G15's book), with the extra
                   fields the Monte Carlo needs (desmoothed equity betas, premia, RAME smoothing, oil elasticities,
                   control shares). G15 fields are copied verbatim so the G15 cash row can be reproduced.
  ra_theta()       theta-indexed Real Assets components of s*(theta): income multipliers, true-value shock,
                   LTV^max, lender availability, call multiplier, exit factor, stress months.
  pe_vintages_v2() PE vintage book for v2 from the sealed census v1.1 history (groups gap_02), rescaled.
  l8()             private NAV + unfunded <= 0.80 W.
"""
from __future__ import annotations

import csv
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS_ADD = os.path.normpath(os.path.join(HERE, ".."))
SEALED_CSV = os.path.join(HERE, "sealed_pe_history_v1_1.csv")   # local copy of groups gap_02's sealed history
NAV0 = 177.0
THETA0 = 0.76            # published canonical theta* (v1 book); anchor of the RA theta family

# ------------------------------------------------------------------------------------------------ books
# census v1.0 non-PE split (groups synthesis s6): Sec 3.5 + 0.4 deferred, Co 1.5, CS 1.2, PC 3.0 + 1.0 DDTL
NONPE_UNF = dict(sec=3.5, co=1.5, cs=1.2, pc=3.0)
SEC_DEF_V1, PC_REV_V1 = 0.4, 1.0
BOOKS = {
    "v1":    dict(label="v1: seven groups, census v1.0 split (PE 52 / 27.4)", pe_nav=52.0, pe_unf=27.4, ra=False),
    "v1s":   dict(label="v1 with sealed census v1.1 PE unfunded (PE 52 / 16.4)", pe_nav=52.0, pe_unf=16.4, ra=False),
    "v2u16": dict(label="v2: PE 34 / 16.4 (user's census v1.1 figure) + Real Assets 18 / 4.0", pe_nav=34.0,
                  pe_unf=16.4, ra=True),
    "v2u11": dict(label="v2: PE 34 / 10.9 (v1.1 U/NAV 0.32 rescaled) + Real Assets 18 / 4.0", pe_nav=34.0,
                  pe_unf=10.9, ra=True),
}


def book_priv(book: str, ra_scale: float = 1.0) -> dict:
    """Private NAV by group ($bn). Real Assets NAV = 18 * ra_scale, carved from PE so private stays 106."""
    b = BOOKS[book]
    ra_nav = 18.0 * ra_scale if b["ra"] else 0.0
    pe = b["pe_nav"] - (ra_nav - (18.0 if b["ra"] else 0.0))
    return dict(pe=pe, sec=14.0, co=18.0, cs=8.0, pc=14.0, ra=ra_nav)


def book_unf(book: str, ra_scale: float = 1.0) -> dict:
    b = BOOKS[book]
    priv = book_priv(book, ra_scale)
    pe_u = b["pe_unf"] * priv["pe"] / b["pe_nav"]          # PE unfunded scales with PE NAV in size scans
    return dict(pe=pe_u, **NONPE_UNF, ra=(4.0 * ra_scale if b["ra"] else 0.0))


def l8(book: str, ra_scale: float = 1.0, W: float = NAV0, priv_nav: float | None = None,
       unf: float | None = None) -> dict:
    """L8: private NAV + unfunded <= 0.80 W (groups s2.4). Unfunded includes deferred and DDTL commitments."""
    p = book_priv(book, ra_scale)
    u = book_unf(book, ra_scale)
    pn = sum(p.values()) if priv_nav is None else priv_nav
    un = (sum(u.values()) + SEC_DEF_V1 + PC_REV_V1) if unf is None else unf
    return dict(private_nav=pn, unfunded=un, ratio=(pn + un) / W, headroom=0.80 * W - pn - un)


# ------------------------------------------------------------------------------------------------ RA census
# G15 fields (verbatim from research/groups/addenda/G15_calcs/g15_ra_calcs.py SLEEVES) plus MC fields [I]:
#   beta_eq   desmoothed equity-level beta to ACWI (G15 s7: RE 0.6-0.8, INF 0.5-0.6; dossier 04: VA RE 0.77,
#             infrastructure 0.5-0.7) [I]
#   prem      premium over the beta-matched basket, geometric, net (calibrated so M1 sector returns sit near
#             J.P. Morgan 2027 LTCMA core RE 7.9% / infrastructure 7.1% less fees; RA weighted M1 return 6.8%
#             against PE 9.6%, i.e. ~28bp of NAV a year for $18bn, as G15's 26bp) [I]
#   lam, lag  RAME aggregate smoothing and lag (G13 s6.7; RA synthesis s5) [I]
#   g0        initial asset-level stale gap V^A/V^T - 1 (RA synthesis RA8: SYN default 2% for real estate) [I]
#   eps_oil   oil elasticity of equity value (G12: levered upstream 0.643, royalties ~0.30, fee midstream ~0.10,
#             other ~0.07; weighted on G12's sub-sleeve split) [I-calc]
#   ctrl      share of the sleeve under sole or joint control (synthesis s7.2: funds LP; mixed sleeves 50%) [I]
#   sig_a     sleeve-level idiosyncratic asset volatility per quarter [I]
SLEEVES = [
    dict(id="RE_OE", sector="RE", vehicle="OE", nav=2.7, unf=0.0, ltv=0.27, inc=0.0325, real_n=0.00, real_d=0.00,
         g_n=0.010, direct=False, commit=0.0, beta_eq=0.55, prem=0.010, lam=0.75, lag=1, g0=0.02, eps_oil=0.0,
         ctrl=0.0, sig_a=0.012, seg="CORE_RE"),
    dict(id="RE_CE", sector="RE", vehicle="CE", nav=2.6, unf=1.2, ltv=0.60, inc=0.010, real_n=0.18, real_d=0.06,
         g_n=0.020, direct=False, commit=0.375, beta_eq=0.85, prem=0.002, lam=0.70, lag=1, g0=0.02, eps_oil=0.0,
         ctrl=0.0, sig_a=0.015, seg="VA_RE"),
    dict(id="RE_DIR_GL", sector="RE", vehicle="JV/DIR", nav=1.7, unf=0.2, ltv=0.45, inc=0.030, real_n=0.00,
         real_d=0.00, g_n=0.010, direct=True, commit=0.0, beta_eq=0.65, prem=0.010, lam=0.725, lag=1, g0=0.02,
         eps_oil=0.0, ctrl=1.0, sig_a=0.018, seg="CORE_RE"),
    dict(id="RE_DIR_GCC", sector="RE_GCC", vehicle="JV/DIR", nav=1.2, unf=0.2, ltv=0.45, inc=0.045, real_n=0.00,
         real_d=0.00, g_n=0.020, direct=True, commit=0.0, beta_eq=0.60, prem=0.018, lam=0.80, lag=1, g0=0.02,
         eps_oil=0.0, ctrl=1.0, sig_a=0.020, seg="GCC_RE"),
    dict(id="RE_COI", sector="RE", vehicle="CO", nav=0.8, unf=0.0, ltv=0.60, inc=0.015, real_n=0.12, real_d=0.04,
         g_n=0.020, direct=True, commit=0.0, beta_eq=0.85, prem=0.007, lam=0.70, lag=1, g0=0.02, eps_oil=0.0,
         ctrl=0.0, sig_a=0.025, seg="VA_RE"),
    dict(id="INF_OE", sector="INF", vehicle="OE", nav=2.0, unf=0.0, ltv=0.50, inc=0.055, real_n=0.00, real_d=0.00,
         g_n=0.025, direct=False, commit=0.0, beta_eq=0.50, prem=0.012, lam=0.85, lag=1, g0=0.01, eps_oil=0.0,
         ctrl=0.0, sig_a=0.010, seg="CORE_INFRA"),
    dict(id="INF_CE", sector="INF", vehicle="CE", nav=2.5, unf=1.3, ltv=0.55, inc=0.040, real_n=0.08, real_d=0.04,
         g_n=0.040, direct=False, commit=0.4375, beta_eq=0.60, prem=0.013, lam=0.80, lag=1, g0=0.01, eps_oil=0.0,
         ctrl=0.0, sig_a=0.012, seg="VA_INFRA"),
    dict(id="INF_DIR", sector="INF", vehicle="DIR/CO", nav=2.0, unf=0.3, ltv=0.55, inc=0.050, real_n=0.02,
         real_d=0.01, g_n=0.030, direct=True, commit=0.0, beta_eq=0.55, prem=0.020, lam=0.825, lag=1, g0=0.01,
         eps_oil=0.0, ctrl=0.5, sig_a=0.014, seg="CORE_INFRA"),
    dict(id="ENR_CE", sector="ENR", vehicle="CE", nav=1.6, unf=0.6, ltv=0.35, inc=0.040, real_n=0.10, real_d=0.06,
         g_n=0.030, direct=False, commit=0.1875, beta_eq=0.50, prem=0.002, lam=0.50, lag=2, g0=0.0,
         eps_oil=(0.80 * 0.643 + 0.40 * 0.0988 + 0.40 * 0.07) / 1.6, ctrl=0.0, sig_a=0.025, seg="ENERGY",
         lev_upstream=0.80),
    dict(id="ENR_DIR", sector="ENR", vehicle="DIR/CO", nav=0.9, unf=0.2, ltv=0.40, inc=0.070, real_n=0.00,
         real_d=0.00, g_n=0.020, direct=True, commit=0.0, beta_eq=0.40, prem=0.011, lam=0.50, lag=2, g0=0.0,
         eps_oil=(0.27 * 0.643 + 0.18 * 0.303 + 0.45 * 0.0988) / 0.9, ctrl=0.5, sig_a=0.025, seg="ENERGY",
         lev_upstream=0.27),
]
assert abs(sum(s["nav"] for s in SLEEVES) - 18.0) < 1e-9
assert abs(sum(s["unf"] for s in SLEEVES) - 4.0) < 1e-9
SIDS = [s["id"] for s in SLEEVES]
NS = len(SLEEVES)
SEC = np.array([s["sector"] for s in SLEEVES])
LEV_UP_ELAST = 0.643        # G12: 40%-LTV upstream equity elasticity at the $70 state
OIL_REF_DELTA = 70.0        # spot-equivalent barrels quoted at the $70 normal state (V-RA-OIL)

# G15 T4' values (RA synthesis s6.3) at theta = 0.76 and normal / stressed lender terms (G15 LTV_MAX)
T4_INC = {"RE": 0.85, "RE_GCC": 0.80, "INF": 0.92, "ENR": 0.60}
T4_TRUE = {"RE": -0.25, "RE_GCC": -0.30, "INF": -0.12, "ENR": -0.30}
LTV_N = {"RE": 0.60, "RE_GCC": 0.60, "INF": 0.65, "ENR": 0.55}
LTV_S = {"RE": 0.50, "RE_GCC": 0.45, "INF": 0.55, "ENR": 0.45}
T4_MARKS = {"RE": {3: -0.06, 6: -0.06, 9: -0.04, 12: -0.03}, "RE_GCC": {3: -0.06, 6: -0.07, 9: -0.05, 12: -0.04},
            "INF": {3: -0.03, 6: -0.03, 9: -0.02}, "ENR": {3: -0.10, 6: -0.08, 9: -0.05}}
MATURITY_PA = 0.17          # MBA: 17% of CRE balances mature in 2026 (G15)
AVAIL_N, AVAIL_LIT = 0.97, 0.45   # lender availability: normal 0.97; literal-T4 end 0.45 -> 0.575 at theta 0.76
                                  # (RA synthesis s5: N / T / C = 0.97 / 0.80-0.85 / 0.50-0.60) [I]


EXT_N = 0.35                # P(extension | no lender) outside crisis: G10's lower value (Glancy 2026: banks extended
                            # about half of maturing loans in 2023-25 unconditionally; risky / non-recourse loans
                            # less often after 2022) -> 0 in crisis; in s*(theta): 0.35 (1 - theta) [I]


def ra_theta(theta: float, availability: bool = True, ext: float | None = None,
             call_axis: float | None = None) -> dict:
    """theta-indexed Real Assets components of s*(theta) [I].

    Each component c is affine in theta, anchored at the drought ('today', theta = 0 for income and lender terms)
    value and passing exactly through G15's T4' value at theta0 = 0.76, so the published canonical point is
    unchanged when theta* = 0.76:
      income multiplier   m_s(theta) = 1 - (theta / 0.76) (1 - m_s^T4')
      true-value shock    v_s(theta) = v_s^T4' (0.30 + 0.10 theta) / 0.376     (scales with the equity vertex)
      LTV^max             L_s(theta) = L_N - (theta / 0.76) (L_N - L_S)
      availability        a(theta)   = 0.97 - 0.52 theta  (0.575 at 0.76: mid of the crisis range 0.50-0.60)
      calls               (1 + 0.5 theta) x 28% of unfunded (the family's own, as for PE); axis x1.0
      exits               0.45 (1 - theta) x drought realisation rates (the family's own)
      stress months       round(18 + 6 theta) income months; lender stress 24 months (G15)
    ext is P(extension | no lender): canonical 0.35 (1 - theta) (0.084 at 0.76); axis 0 / 0.35 fixed."""
    k = theta / THETA0
    eqv = (0.30 + 0.10 * theta) / (0.30 + 0.10 * THETA0)
    out = dict(theta=theta,
               inc={s: 1.0 - k * (1.0 - T4_INC[s]) for s in T4_INC},
               true={s: T4_TRUE[s] * eqv for s in T4_TRUE},
               ltv={s: LTV_N[s] - k * (LTV_N[s] - LTV_S[s]) for s in LTV_N},
               avail=(AVAIL_N - (AVAIL_N - AVAIL_LIT) * theta) if availability else 1.0,
               ext=(max(0.0, EXT_N * (1.0 - theta)) if ext is None else ext),
               call_mult=(1.0 + 0.5 * theta) if call_axis is None else call_axis,
               exit_factor=0.45 * (1.0 - theta),
               crisis_months=int(round(18 + 6 * theta)), lender_months=24)
    return out


def oil_delta_bbl(nav_by_sleeve: dict, price: float = OIL_REF_DELTA, elast_scale: float = 1.0) -> float:
    """Spot-equivalent barrels (millions) of the ENR sleeves: sum V_s * eps_s / P (G12 convention)."""
    tot = 0.0
    for s in SLEEVES:
        if s["sector"] != "ENR":
            continue
        tot += nav_by_sleeve[s["id"]] * s["eps_oil"] * elast_scale / price * 1000.0
    return tot


# ------------------------------------------------------------------------------------------------ PE vintages
def pe_vintages_v2(pe_nav: float, pe_unf: float, first: int = 2012, last: int = 2026):
    """NAV and unfunded by vintage for the v2 PE book from the sealed census v1.1 history (groups gap_02), with
    NAV rescaled to pe_nav and unfunded rescaled to pe_unf. Vintages before `first` are folded into `first`.
    Also returns the quarterly commitment history for the last 20 quarters (2021Q4..2026Q3), scaled like the
    unfunded (it drives the co-investment flow)."""
    rows = []
    with open(SEALED_CSV, encoding="utf-8") as fh:
        rd = csv.reader(l for l in fh if not l.startswith("#"))
        hdr = next(rd)
        for r in rd:
            rows.append({h: float(x) for h, x in zip(hdr, r)})
    vint = np.arange(first, last + 1)
    N = np.zeros(vint.size)
    U = np.zeros(vint.size)
    K = np.zeros(vint.size)
    for r in rows:
        v = int(r["vintage"])
        i = max(0, min(v, last) - first)
        N[i] += r["nav_total"]
        U[i] += r["unf_total"]
        if v >= first:
            K[v - first] += r["commit_pace_annual"]
    sN, sU = pe_nav / N.sum(), pe_unf / U.sum()
    N, U = N * sN, U * sU
    # quarterly commitments 2021Q4..2026Q3 (20 quarters), each vintage's annual pace / 4, scaled like U
    hist = []
    for q in range(20):
        tau = 2021.75 + 0.25 * q
        v = int(math.floor(tau + 1e-9))
        hist.append(K[v - first] / 4.0 * sU)
    return dict(vint=vint, N0=N, U0=U, hist_c=np.array(hist), scale_nav=sN, scale_unf=sU,
                pace_2026=float(K[-1] * sU))


if __name__ == "__main__":
    import json
    out = {"books": {}, "l8": {}, "theta_family": {}, "oil_delta": {}}
    for b in BOOKS:
        out["books"][b] = dict(priv=book_priv(b), unf=book_unf(b))
        out["l8"][b] = l8(b)
    for th in (0.0, 0.5, 0.76, 0.8, 1.0):
        out["theta_family"][f"{th:.2f}"] = ra_theta(th)
    out["oil_delta"]["census_$70"] = oil_delta_bbl({s["id"]: s["nav"] for s in SLEEVES})
    v = pe_vintages_v2(34.0, 16.4)
    out["pe_v2_u16"] = dict(N=v["N0"].round(2).tolist(), U=v["U0"].round(2).tolist(), pace=v["pace_2026"])
    v = pe_vintages_v2(34.0, 10.9)
    out["pe_v2_u11"] = dict(N=v["N0"].round(2).tolist(), U=v["U0"].round(2).tolist(), pace=v["pace_2026"])
    print(json.dumps(out, indent=1, default=float))
