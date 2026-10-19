"""
RA gap 02 - Real Assets engine prototype on the census of record, under the canonical (S_t, e_t, Z_t) generator plus
the explicit financing window f_t.

*** SYNTHETIC - NOT ADIC DATA. Every balance, path, cure and cash figure is synthetic. ***

Components (quarterly, 20 quarters from 2026Q4; common random numbers on exogenous paths across scenarios):
  RE property layer   G10 equations (lease roll, sticky opex, partial-adjustment cap rate on 10y and Baa) re-keyed to the
                      canonical factors; credit-availability premium keyed to f_t; GCC hits keyed to Z_t (differenced
                      against the initial Gulf-war state); asset-level idiosyncratic value paths.
  Infrastructure      G11 structural archetypes: revenue indexed to lagged CPI with pass-through theta_k, fixed escalators,
                      GDP-elastic volume, regime-entry jumps with half-lives, power price; regulated RAB indexed to CPI with
                      allowed-return resets every 20 quarters; V^A = PV of CFADS on the current curve + ERP_k + beta_q q_t,
                      with q_t's mean keyed to the G11 state derived from (S, Z).
  ENR                 G12 curve (C3 dynamics, Z-dependent expected path); PDP / royalty / midstream / other assets; RBL
                      borrowing base = advance x PV at 0.85 x strip, semiannual + interim (|dln P| >= 0.20) redeterminations,
                      deficiency cured over two quarters (3-6 monthly instalments, Latham 2015).
  Debt module (s4.5)  per tranche of the sealed tape (decide_maturity): L^max = a min(LTV^max_f V^mat, NOI/(DSCR^min_f k),
                      NOI/DY^min_f); clean refinance; contractual extension if its tests pass; discretionary extension
                      (axis 0 vs G10); forbearance for up to two no-lender quarters; then cure (varpi = 1, or the ruthless
                      rule V - D - ell S > max(0, V(1-d) - D)), sale or hand-back. DSCR traps/lock-ups, maintenance LTV.
  Fund-level module   GP needs -> distribution stop -> protective calls up to unfunded (closed-end) or asset sales
                      (open-end) -> residual NAV loss.
  Vehicles            closed-end calls (canonical CALL table keyed to e; 0.28 x 1.38 under T4'; structural m^C(e) axis),
                      exits by effective age and window, income; open-end income and the G10 queue machine; direct
                      income, cures, shortfalls, development draws; co-investments on the sponsor's exit clock.
Run:  .venv\\Scripts\\python.exe -B ra_engine.py [n_paths]
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import os
import sys
import time

import numpy as np
from scipy.special import ndtri

import ra_common as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ra_engine_results.json")
T = 20
SEED = 20261019
G0_GAP = 0.02                      # RA s11 SYN default stale gap at t0
RHO_LENDER = 0.5                   # lender-availability copula with CF facilities (RA s4.5) [I]
SPREAD_FIX = {"RE": 0.0200, "INF": 0.0175, "ENR": 0.0250}   # N-state new-loan spreads (CBRE 204bp; G14) [S/I]
BRIDGE_SPREAD = 0.0300
NEW_TERM_Q = {"RE": 20, "INF": 28, "ENR": 20, "bridge": 12}
CAP_FWD_VOL = 0.004                # cap cost per year above intrinsic (3y 4.5% cap ~1.2% of notional, RA s9.2)
ELL_GP = np.array([0.05, 0.10, 0.20])   # GP / sponsor liquidity premium by f [I]
FEES = {"RE_OE": 0.0085, "INF_OE": 0.010, "RE_CE": 0.015, "INF_CE": 0.0125, "ENR_CE": 0.015,
        "RE_DIR_GL": 0.005, "RE_DIR_GCC": 0.005, "RE_COI": 0.005, "INF_DIR": 0.005, "ENR_DIR": 0.005}
LAM_APP = {"RE_OE": 0.75, "RE_DIR_GL": 0.75, "RE_CE": 0.70, "RE_COI": 0.70, "RE_DIR_GCC": 0.80, "INF_OE": 0.85,
           "INF_CE": 0.80, "INF_DIR": 0.80, "ENR_CE": 0.50, "ENR_DIR": 0.50}   # G13 lambda_agg
CANON_CALL = np.array([0.39, 0.29, 0.28, 0.30])    # groups-report CALL table, keyed to e (O/N/D/F)
PACE = {"RE_CE": 0.375, "INF_CE": 0.4375, "ENR_CE": 0.1875}   # G15 commit shares of $1.2bn a year
PACE_TOTAL = 1.2
C_SLEEVES = ["RE_OE", "RE_CE", "RE_DIR_GL", "RE_DIR_GCC", "RE_COI", "INF_OE", "INF_CE", "INF_DIR", "ENR_CE", "ENR_DIR"]

# ------------------------------------------------------------------------------------------------ tape
NUM = {"gav_adic", "noi_yield", "capex_rate", "adic_share", "decline", "hedge_share", "unfunded_adic", "balance_adic",
       "commit_adic", "ltv_t0_app", "coupon", "spread", "swap_share", "cap_strike", "amort_years", "ext_dscr", "ext_dy",
       "ext_ltv", "ext_paydown", "cov_trap_dscr", "cov_default_dscr", "cov_ltv_max", "cov_dy_min", "guarantee_share",
       "rbl_adv", "rbl_deck", "dev_ltc"}
INT = {"gcc_flag", "dev_flag", "age_q", "reset_phase_q", "energy_link", "orig_year", "maturity_q", "cap_expiry_q",
       "ext_options", "ext_len_q", "rbl_redet_q", "controllable"}


def load_tape():
    man = json.load(open(os.path.join(HERE, "ra_tape_manifest.json"), encoding="utf-8"))
    out = {}
    for fn, h in man["files"].items():
        with open(os.path.join(HERE, fn), encoding="utf-8", newline="") as fh:
            txt = fh.read()
        if hashlib.sha256(txt.encode("utf-8")).hexdigest() != h:
            raise RuntimeError(f"tape seal broken: {fn}")
        rows = list(csv.DictReader(io.StringIO("\n".join(txt.splitlines()[1:]))))
        for r in rows:
            for k in list(r):
                if k in NUM:
                    r[k] = float(r[k])
                elif k in INT:
                    r[k] = int(float(r[k]))
        out[fn] = rows
    return out["ra_tape_assets_v1.csv"], out["ra_tape_tranches_v1.csv"], man


# ------------------------------------------------------------------------------------------------ s4.5 decision (pure)
BETA_ROLLOVER = 0.111  # sponsor (non-ADIC) RE sale hazard per +1pp of positive rate gap at maturity = Chen & Chen's
                       # marginal effect (Table 9); the s4.5 capacity channel alone explains <= 1/8 of it (G-CHEN)
ROLL_DAMP = np.array([1.0, 0.6, 0.2])   # the 2003-19 estimate is damped when the financing window tightens/closes [I]


def decide_maturity(D, sib, Vm, NOIa, VAj, lmax, dmin, dymin, k_new, lender, due, ext_left, ext_dscr, ext_dy, ext_ltv,
                    dscr_now, p_ext, u_ext, disc_left, forb_left, nonrec, owner_ctl, varpi, ell, dsc, cov_gap=None,
                    rbl_cap=None, gap_pp=None, u_sale=None, beta_sale=0.0):
    """One tranche across paths. V^mat = Vm (own collateral, economic). Returns masks and the gap.
    Optional behavioural channel (sponsor/GP owners only): at maturity, with probability beta_sale x (rate gap in pp)^+,
    the owner sells instead of refinancing (Chen & Chen 2025 rollover effect), if equity after the sale is positive."""
    cap_ltv = lmax * Vm - sib
    cap_dscr = NOIa / (dmin * k_new) - sib
    cap_dy = np.where(dymin > 0, NOIa / np.maximum(dymin, 1e-6) - sib, np.inf)
    Lmax = np.maximum(np.minimum(np.minimum(cap_ltv, cap_dscr), cap_dy), 0.0)
    if rbl_cap is not None:
        Lmax = np.maximum(rbl_cap, 0.0)
    gap = np.where(lender, np.maximum(D - Lmax, 0.0), D)
    if cov_gap is not None:
        gap = np.where(due, gap, cov_gap)
        act = due | (cov_gap > 1e-9)
    else:
        act = due.copy()
    refi = due & lender & (gap <= 1e-12)
    dy_now = NOIa / np.maximum(D + sib, 1e-12)
    ltv_now = (D + sib) / np.maximum(VAj, 1e-12)
    ext_ok = (due & ~refi & (ext_left > 0) & (dscr_now >= ext_dscr) & ((ext_dy == 0) | (dy_now >= ext_dy)) &
              ((ext_ltv == 0) | (ltv_now <= ext_ltv)))
    pe = p_ext - 0.05 * nonrec - 0.07 * (dy_now < 0.08)          # Glancy (2026): non-recourse -5pp, DY<8% -7pp
    dext = due & ~refi & ~ext_ok & (gap > 0) & (disc_left > 0) & (u_ext < np.maximum(pe, 0.0))
    forbear = due & ~refi & ~ext_ok & ~dext & ~lender & (forb_left > 0)
    decide = act & ~refi & ~ext_ok & ~dext & ~forbear
    V_eq = Vm - D - sib
    sale_val = Vm * (1 - dsc) - D - sib
    if owner_ctl and varpi >= 1.0:
        cure = decide & ~(~lender & (sale_val > 0))              # reputation-bound; no lender -> sell if equity > 0
    else:
        cure = decide & ((V_eq - ell * gap) > np.maximum(0.0, sale_val))
    sell = decide & ~cure & (sale_val > 0)
    hand = decide & ~cure & ~sell
    if beta_sale > 0 and gap_pp is not None and not owner_ctl:
        roll = (refi | cure) & due & (sale_val > 0) & (u_sale < np.clip(beta_sale * np.maximum(gap_pp, 0.0), 0.0, 0.9))
        refi = refi & ~roll
        cure = cure & ~roll
        sell = sell | roll
    return dict(Lmax=Lmax, gap=gap, act=act, refi=refi, ext_ok=ext_ok, dext=dext, forbear=forbear, cure=cure,
                sell=sell, hand=hand, V_eq=V_eq, sale_val=sale_val)


# ------------------------------------------------------------------------------------------------ RE property layer
SP = {   # G10 sector parameters [I]; c_app is the appraisal cap rate
    "LOG": dict(c_app=0.041, walt=5.0, esc=0.03, bpi=0.5, mu=-0.010, bg=1.0, occ=0.94, bo=0.5, phi=0.10, sm=0.04, m2m=0.10, drift=0),
    "RES": dict(c_app=0.043, walt=1.0, esc=0.00, bpi=0.6, mu=-0.015, bg=0.8, occ=0.94, bo=0.5, phi=0.38, sm=0.035, m2m=0.00, drift=0),
    "OFF": dict(c_app=0.062, walt=6.0, esc=0.025, bpi=0.3, mu=-0.020, bg=1.5, occ=0.82, bo=1.5, phi=0.40, sm=0.06, m2m=-0.10, drift=10),
    "RET": dict(c_app=0.054, walt=5.0, esc=0.02, bpi=0.4, mu=-0.005, bg=1.2, occ=0.93, bo=0.8, phi=0.15, sm=0.04, m2m=0.00, drift=0),
    "DC": dict(c_app=0.048, walt=8.0, esc=0.03, bpi=0.3, mu=0.010, bg=0.6, occ=0.95, bo=0.3, phi=0.20, sm=0.05, m2m=0.08, drift=0),
    "HOT": dict(c_app=0.075, walt=0.05, esc=0.00, bpi=0.8, mu=-0.005, bg=2.5, occ=0.70, bo=3.0, phi=0.70, sm=0.10, m2m=0.00, drift=0),
    "ALT": dict(c_app=0.053, walt=1.5, esc=0.01, bpi=0.6, mu=0.000, bg=1.0, occ=0.88, bo=0.8, phi=0.45, sm=0.05, m2m=0.00, drift=0),
}
REGADJ = {"US": 0.0, "EU": 0.0025, "AS": 0.0, "GCC": 0.015}
BETA_Y, BETA_S, KAPPA_C, SIG_C = 0.45, 0.50, 0.15, 0.0012
SIG_ID_RE = 0.08                   # asset idiosyncratic value vol, annual [I]; disciplined by the Jiang gate
GCC_CAP = np.array([0.0, 0.0, 0.0050, 0.0150, 0.0, 0.0075])


def gcc_hit(k, z):
    h = {"HOT": 0.25, "RET": 0.10, "OFF": 0.06}.get(k, 0.04)
    return np.select([z == C.ZGW, z == C.ZDB, z == C.ZSG], [h, 1.5 * h + 0.05, 0.5 * h + 0.05], 0.0)


def re_market(k, reg, F, rng, n, T_=None):
    """Market path per $1 of t0 appraisal value: economic value V (V0 = e^-G0), NOI (annual), cap rate c, gfwd.
    F needs y, s, pi, g (percent), z, f, fGCC arrays of shape (n, T+1)."""
    T_ = T_ or (F["y"].shape[1] - 1)
    p = SP[k]
    gcc = reg == "GCC"
    y, s, pi, g, z = F["y"] / 100, F["s"] / 100, F["pi"] / 100, F["g"] / 100, F["z"]
    fe = F["fGCC"] if gcc else F["f"]
    liq = C.TERMS["liq_cap_add"]
    c_app = p["c_app"] + REGADJ[reg]
    noi0 = c_app
    gf0 = 0.5 * (p["mu"] + p["bpi"] * pi[:, 0])
    V0 = math.exp(-G0_GAP)
    c0 = noi0 * (1 + gf0) / V0
    O = np.full(n, p["occ"]); GR = noi0 / (1 - p["phi"]); E = p["phi"] * GR; R = GR / O; M = R * (1 + p["m2m"])
    rho = min(1.0, 0.25 / p["walt"])
    c = c0.copy()
    V = np.zeros((n, T_ + 1)); NOI = np.zeros((n, T_ + 1)); CC = np.zeros((n, T_ + 1)); GF = np.zeros((n, T_ + 1))
    V[:, 0] = V0; NOI[:, 0] = noi0; CC[:, 0] = c0; GF[:, 0] = gf0
    hit0 = gcc_hit(k, z[:, 0]) if gcc else 0.0
    shock = F.get("office_shock")             # optional structural office demand shock (gate replays only)
    for t in range(T_):
        e = rng.standard_normal((n, 3))
        M = M * np.exp((p["mu"] + p["bpi"] * pi[:, t + 1] + p["bg"] * g[:, t + 1]) / 4 + p["sm"] / 2 * e[:, 0])
        if shock is not None and k == "OFF":
            M = M * np.exp(shock[t])
        R = R * (1 + p["esc"] / 4) + rho * (M - R * (1 + p["esc"] / 4))
        O = np.clip(O + 0.15 * (p["occ"] + p["bo"] * g[:, t + 1] - O) + 0.005 * e[:, 1], 0.40, 0.99)
        E = E * (1 + pi[:, t + 1] / 4)
        noi = R * O - E
        if gcc:
            noi = noi * (1 - gcc_hit(k, z[:, t + 1])) / (1 - hit0)
        noi = np.maximum(noi, 0.1 * noi0)
        cstar = (c0 + BETA_Y * (y[:, t + 1] - y[:, 0]) + BETA_S * (s[:, t + 1] - s[:, 0]) + p["drift"] / 1e4 * (t + 1) / 4
                 + liq[fe[:, t + 1]] - liq[fe[:, 0]])
        if gcc:
            cstar = cstar + GCC_CAP[z[:, t + 1]] - GCC_CAP[z[:, 0]]
        c = np.maximum(0.025, c + KAPPA_C * (cstar - c) + SIG_C * e[:, 2])
        gf = 0.5 * (p["mu"] + p["bpi"] * pi[:, t + 1])
        V[:, t + 1] = noi * (1 + gf) / c
        NOI[:, t + 1] = noi; CC[:, t + 1] = c; GF[:, t + 1] = gf
    return dict(V=V, NOI=NOI, c=CC, gf=GF, c_app=c_app)


SIG_ID_REGIME = np.array([0.08, 0.15, 0.28])   # gate-informed (G-JIANG): sigma_id by f; 8 C quarters -> ~0.40 dispersion
OFFICE_DISP = 1.5                              # office repricing is more heterogeneous (G-JIANG office tail) [I]


def re_asset_paths(a, mk, rng, n, lam, f_path=None):
    """Asset economic value V*, NOI (annual), capex (quarterly) and appraisal V^A at ADIC share ($bn).
    f_path (n, T+1) switches on regime-dependent idiosyncratic dispersion (recalibrated engine)."""
    gav = a["gav_adic"]
    ci0 = a["noi_yield"] * (1 + mk["gf"][:, 0]) / math.exp(-G0_GAP)
    ci = np.maximum(ci0[:, None] + (mk["c"] - mk["c"][:, :1]), 0.02)     # asset cap rate moves with the market
    eps = rng.standard_normal((n, T))
    if f_path is None:
        sig = np.full((n, T), SIG_ID_RE)
    else:
        sig = SIG_ID_REGIME[f_path[:, 1:]] * (OFFICE_DISP if a["segment"] == "OFF" else 1.0)
    io_ = np.exp(np.cumsum(np.concatenate([np.zeros((n, 1)), sig / 2 * eps - 0.5 * (sig / 2) ** 2], axis=1), axis=1))
    noi = gav * a["noi_yield"] * mk["NOI"] / mk["NOI"][:, :1] * io_
    V = noi * (1 + mk["gf"]) / ci
    capex = a["capex_rate"] / 4 * V
    VA = np.zeros_like(V); VA[:, 0] = gav
    for t in range(T):
        VA[:, t + 1] = np.exp(lam * np.log(VA[:, t]) + (1 - lam) * np.log(np.maximum(V[:, t], 1e-9))
                              + 0.004 * rng.standard_normal(n))
    return dict(V=V, NOI=noi, capex=capex, VA=VA)


# ------------------------------------------------------------------------------------------------ infrastructure
ARCH_P = {  # G11 s6.10 table and durations archetypes [I]
    "REG": dict(theta=1.0, lag=2, esc=0.0, bg=0.0, m=0.0, opex=0.0, greal=0.010, life=60, bq=0.6),
    "CON_IDX": dict(theta=0.9, lag=2, esc=0.0, bg=0.0, m=0.0, opex=0.25, greal=0.0, life=25, bq=0.5),
    "CON_FIX": dict(theta=0.1, lag=4, esc=0.01, bg=0.0, m=0.10, opex=0.20, greal=0.0, life=25, bq=0.6),
    "TOLL": dict(theta=0.8, lag=2, esc=0.0, bg=0.8, m=0.0, opex=0.25, greal=0.015, life=35, bq=1.0),
    "AIR": dict(theta=0.6, lag=2, esc=0.0, bg=1.8, m=0.0, opex=0.45, greal=0.020, life=40, bq=1.4),
    "MID": dict(theta=0.5, lag=4, esc=0.02, bg=0.6, m=0.15, opex=0.35, greal=0.0, life=30, bq=1.0),
    "TOW": dict(theta=0.0, lag=0, esc=0.03, bg=0.3, m=0.0, opex=0.25, greal=0.020, life=40, bq=1.2),
    "DC": dict(theta=0.2, lag=0, esc=0.02, bg=0.5, m=0.0, opex=0.40, greal=0.030, life=40, bq=1.6),
    "MER": dict(theta=0.8, lag=1, esc=0.0, bg=0.3, m=0.80, opex=0.30, greal=0.0, life=25, bq=1.3),
}
JUMPS = {"AIR": (-0.55, 0.25, 3.0), "TOLL": (-0.18, 0.25, 1.0), "DC": (-0.10, 0.50, 8.0), "MID": (-0.08, 1.0, 4.0)}
GW_AIR = -(0.25 * 0.20 + 0.03)
# CFADS idiosyncratic vol, annual: about half of G11's equity sigma_id for contracted/regulated, G11's for others [I]
SIG_ID_INF = {"REG": 0.015, "CON_IDX": 0.010, "CON_FIX": 0.020, "TOLL": 0.040, "AIR": 0.050, "MID": 0.040,
              "TOW": 0.030, "DC": 0.050, "MER": 0.060}


def annuity(x, n):
    x = np.where(np.abs(x) < 1e-6, 1e-6, x)
    return (1 - (1 + x) ** (-n)) / x


def infra_paths(a, F, rng, n, lam):
    P = ARCH_P[a["segment"]]
    gav = a["gav_adic"]
    cf0 = a["noi_yield"] * gav
    pi = F["pi"] / 100
    pie = 0.5 * pi + 0.5 * 0.025
    rreal = F["y"] / 100 - pie
    g11 = F["g11"]
    qbar = C.Q_RISK[g11]
    pbar = np.where(F["z"] == C.ZSG, -0.15, C.P_POWER[g11])
    q = qbar[:, 0].copy(); xp = pbar[:, 0].copy()
    life0 = P["life"] - (a["age_q"] / 4 if P["life"] < 40 else 0)
    r0 = float(rreal[0, 0] + pie[0, 0] + P["bq"] * q[0])
    gnom0 = float(P["theta"] * pie[0, 0] + (1 - P["theta"]) * P["esc"] + P["greal"])
    regulated = P["life"] == 60
    erp_reg = 0.030                    # G11 durations archetype: regulated asset ERP 3.0%
    d_op = 0.0
    if regulated:
        # EV/RAB premium = pre-reset excess return + persistent outperformance d_op (totex / financing), solved so
        # V^A_0 = gav; post-reset value = RAB * (x + d_op) / x with x = real required return less real RAB growth.
        rab0 = gav / 1.10
        om0 = cf0 / rab0
        tau0 = a["reset_phase_q"] / 4
        x0 = max(float(rreal[0, 0] + erp_reg + P["bq"] * q[0] - P["greal"]), 0.005)

        def v_reg(dop):
            return rab0 * (om0 * float(annuity(np.array(x0), tau0)) + (x0 + dop) / x0 * (1 + x0) ** (-tau0))
        lo, hi = -0.03, 0.08
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if v_reg(mid) < gav else (lo, mid)
        d_op = 0.5 * (lo + hi)
        erp = erp_reg
    else:
        lo, hi = -0.02, 0.20
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            v = cf0 * (1 + gnom0) * float(annuity(np.array(r0 + mid - gnom0), life0))
            lo, hi = (mid, hi) if v > gav else (lo, mid)
        erp = 0.5 * (lo + hi)
    R = np.full(n, 1 / (1 - P["opex"])); O = np.full(n, P["opex"] / (1 - P["opex"]))
    Rp = R.copy()                      # revenue for value: power-price moves 35% persistent (G11 MC), jumps 1/4
    J = np.zeros(n)
    rab = np.full(n, gav / 1.10); om = np.full(n, cf0 / (gav / 1.10))
    idio = np.zeros(n)
    CF = np.zeros((n, T + 1)); V = np.zeros((n, T + 1)); CF[:, 0] = cf0; V[:, 0] = gav
    jspec = JUMPS.get(a["segment"])
    oil = F["x"]
    for t in range(T):
        e = rng.standard_normal((n, 3))
        q = q + 0.25 * (qbar[:, t + 1] - q) + 0.00125 * e[:, 0]
        dxp = 0.30 * (pbar[:, t + 1] - xp) + 0.15 * e[:, 1]
        xp = xp + dxp
        lagpi = pi[:, max(0, t + 1 - P["lag"])]
        dJ = np.zeros(n)
        if jspec is not None:
            size, prob, hl = jspec
            dJ = -J * (1 - 0.5 ** (1 / hl)) + np.where(F["onset"][:, t + 1] & (rng.random(n) < prob), size, 0.0)
        if a["segment"] == "AIR":
            dJ = dJ + np.where(F["gw_entry"][:, t + 1], GW_AIR, 0.0)
        J = J + dJ
        idio = idio + SIG_ID_INF[a["segment"]] / 2 * e[:, 2]
        if regulated:
            rab = rab * (1 + pi[:, t + 1] / 4) * (1 + P["greal"] / 4)
            x = np.maximum(rreal[:, t + 1] + erp + P["bq"] * q - P["greal"], 0.005)
            if (t + 1 >= a["reset_phase_q"]) and ((t + 1 - a["reset_phase_q"]) % 20 == 0):
                # reset: allowed real return = market real rate + regulatory premium (half the risk-premium move)
                om = np.maximum(0.005, rreal[:, t + 1] + erp - P["greal"] + 0.5 * P["bq"] * q + d_op)
            cf = om * rab * np.exp(idio)
            tau = ((a["reset_phase_q"] - (t + 1)) % 20) / 4
            tau = 5.0 if tau == 0 else tau
            V[:, t + 1] = rab * np.exp(idio) * (om * annuity(x, tau) + (x + d_op) / x * (1 + x) ** (-tau))
        else:
            dlnR = (P["theta"] * lagpi / 4 + (1 - P["theta"]) * P["esc"] / 4 + P["greal"] / 4
                    + P["bg"] * F["g"][:, t + 1] / 400 + P["m"] * dxp)
            if a["segment"] == "MID":
                dlnR = dlnR + 0.075 * (oil[:, t + 1] - oil[:, t])
            R = R * np.exp(dlnR)
            Rp = Rp * np.exp(dlnR - 0.65 * P["m"] * dxp)
            O = O * (1 + pi[:, t + 1] / 4)
            cf = cf0 * np.maximum(R * np.exp(J) - O, 0.05) * np.exp(idio)
            life = max(1.0, life0 - (t + 1) / 4)
            r = rreal[:, t + 1] + pie[:, t + 1] + erp + P["bq"] * q
            gn = P["theta"] * pie[:, t + 1] + (1 - P["theta"]) * P["esc"] + P["greal"]
            cf_perm = cf0 * np.maximum(Rp * np.exp(J / 4) - O, 0.05) * np.exp(idio)  # value sees ~1/4 of a jump
            V[:, t + 1] = cf_perm * (1 + gn) * annuity(r - gn, life)
        CF[:, t + 1] = cf
    VA = np.zeros_like(V); VA[:, 0] = gav
    for t in range(T):
        VA[:, t + 1] = lam * VA[:, t] + (1 - lam) * V[:, t]
    return dict(V=V, NOI=CF, capex=np.zeros_like(V), VA=VA, erp=erp)


# ------------------------------------------------------------------------------------------------ ENR
PHI_OIL = 0.6
KS = np.arange(1, 31)


def a_off():
    A = np.zeros((6, 30)); Pi = np.eye(6); pm = []
    for _ in range(30):
        Pi = Pi @ C.PZ_A
        pm.append(Pi @ C.MU_OIL)
    pm = np.array(pm)
    for k in range(1, 31):
        A[:, k - 1] = sum(PHI_OIL ** (k - i) * pm[i - 1] for i in range(1, k + 1))
    return A


A_OFF = a_off()


def curve(x, z):
    return np.exp(np.log(C.P_LR) + (PHI_OIL ** KS)[None, :] * (x[:, None] - np.log(C.P_LR)) + A_OFF[z, :])


PDP = dict(nri=0.80, tax=0.07, cost=20.0, disc=0.10)


def pdp_pv(x, z, age, decline, deck=1.0):
    Fk = curve(x, z) * deck
    qk = np.exp(-decline * (age[:, None] + KS[None, :] - 0.5))
    nb = np.maximum(Fk * PDP["nri"] * (1 - PDP["tax"]) - PDP["cost"], 0.0)
    return (qk * nb * (1 + PDP["disc"]) ** -(KS - 0.5)).sum(axis=1)


def roy_pv(x, z, vol, deck=1.0):
    Fk = curve(x, z) * deck
    gk = -0.08 + 0.10 * (np.log(Fk) - np.log(C.P_LR))
    qk = vol[:, None] * np.exp(np.cumsum(gk, axis=1) - 0.5 * gk)
    return (qk * Fk * 0.93 * 1.085 ** -(KS - 0.5)).sum(axis=1)


def enr_paths(a, F, rng, n):
    x, z = F["x"], F["z"]
    gav = a["gav_adic"]
    typ = a["enr_type"]
    V = np.zeros((n, T + 1)); CF = np.zeros((n, T + 1)); VD = np.zeros((n, T + 1))
    if typ == "PDP":
        # reserves valued on a 12%-decline PDP profile (what RBL lenders value), with maintenance drilling replacing
        # reserves so the portfolio's net decline is 3% a year (the FCF yield is after maintenance capex) [I]
        age = np.full(n, a["age_q"] / 4)
        net_dec = 0.03
        pv0 = pdp_pv(x[:, 0], z[:, 0], age, a["decline"])
        F1 = curve(x[:, 0], z[:, 0])[:, 0]
        h = a["hedge_share"]
        for t in range(T + 1):
            P = np.exp(x[:, t])
            qn = np.exp(-net_dec * t / 4)
            cash = qn * np.maximum(P * PDP["nri"] * (1 - PDP["tax"]) - PDP["cost"], 0.0)
            hedge = qn * h * PDP["nri"] * (1 - PDP["tax"]) * (F1 - P) if t <= 8 else 0.0
            CF[:, t] = cash + hedge
            V[:, t] = gav * qn * pdp_pv(x[:, t], z[:, t], age, a["decline"]) / pv0
            VD[:, t] = gav * qn * pdp_pv(x[:, t], z[:, t], age, a["decline"], deck=0.85) / pv0
        CF = CF / CF[:, :1] * (a["noi_yield"] * gav)
    elif typ == "ROY":
        vol = np.ones(n)
        sc = gav / roy_pv(x[:, 0], z[:, 0], vol)
        for t in range(T + 1):
            if t > 0:
                vol = vol * np.exp((-0.08 + 0.10 * (x[:, t] - np.log(C.P_LR))) / 4)
            CF[:, t] = vol * np.exp(x[:, t])
            V[:, t] = sc * roy_pv(x[:, t], z[:, t], vol)
            VD[:, t] = sc * roy_pv(x[:, t], z[:, t], vol, deck=0.85)
        CF = CF / CF[:, :1] * (a["noi_yield"] * gav)
    elif typ == "MID":
        v = np.ones(n)
        y = F["y"] / 100
        for t in range(T + 1):
            if t > 0:
                F1 = curve(x[:, t], z[:, t])[:, 0]
                v = np.maximum(v * np.exp(0.15 * 0.5 * (np.log(F1) - np.log(C.P_LR)) / 4), 0.6)
            CF[:, t] = a["noi_yield"] * gav * v
            V[:, t] = CF[:, t] / np.maximum(a["noi_yield"] + 0.6 * (y[:, t] - y[:, 0]), 0.03)
        VD[:] = V
    else:
        for t in range(T + 1):
            V[:, t] = gav * np.exp(0.10 * (x[:, t] - x[:, 0])) * 1.02 ** (t / 4)
            CF[:, t] = 0.06 * V[:, t]
        VD[:] = V
    VA = np.zeros_like(V); VA[:, 0] = gav
    for t in range(T):
        VA[:, t + 1] = 0.5 * VA[:, t] + 0.5 * V[:, max(0, t - 1)]          # lambda 0.5 + 2-quarter deck lag (G13)
    return dict(V=V, NOI=CF, capex=np.zeros_like(V), VA=VA, VD=VD)


# ------------------------------------------------------------------------------------------------ engine
LAM_RECAL = {"RE_OE": 0.60, "RE_DIR_GL": 0.60, "RE_CE": 0.55, "RE_COI": 0.55, "RE_DIR_GCC": 0.65}   # G-ODCE lag


class Opts:
    def __init__(self, ext="g10", varpi=1.0, calls="canonical", fund_module=True, coinv_participate=True,
                 gcc_gw_floor=C.fT, beta_roll=BETA_ROLLOVER, recal=True):
        self.ext, self.varpi, self.calls, self.fund_module = ext, varpi, calls, fund_module
        self.coinv_participate, self.gcc_gw_floor, self.beta_roll = coinv_participate, gcc_gw_floor, beta_roll
        self.recal = recal

    def key(self):
        return (f"ext={self.ext}|varpi={self.varpi}|calls={self.calls}|fund={self.fund_module}"
                f"|coinv={self.coinv_participate}|gccGW={C.F_NAMES[self.gcc_gw_floor]}|roll={self.beta_roll}"
                f"|recal={self.recal}")


AGG_KEYS = ("income", "exits", "calls", "prot_calls", "dist_stop", "cures_direct", "cures_coinv", "fund_need",
            "fund_loss", "shortfall_direct", "dev_draws", "debt", "V", "VA", "matured", "gap", "handback_equity",
            "sale_proceeds_direct", "ext_paydown", "rbl_cures", "debt_ctl", "V_ctl", "matured_ctl", "oe_sales", "Vidx")
OUTC = ("refi", "ext_contract", "ext_discretionary", "cure", "sale", "handback", "forbear")


def run(scen: str, n: int = 4000, seed: int = SEED, opts: Opts | None = None, keep=False):
    opts = opts or Opts()
    sc = C.SCENARIOS[scen]
    F = C.simulate_states(n, T, seed, sc)
    if opts.gcc_gw_floor != C.fT:
        floor = C.GCC_FLOOR.copy(); floor[C.ZGW] = opts.gcc_gw_floor
        F["fGCC"] = np.maximum(F["f"], floor[F["z"]])
    assets, tranches, man = load_tape()
    rng_m = np.random.default_rng(seed + 11)
    rng_d = np.random.default_rng(seed + 23)
    mk_cache, AP = {}, {}
    for a in assets:
        lam = LAM_RECAL.get(a["sleeve"], LAM_APP[a["sleeve"]]) if opts.recal else LAM_APP[a["sleeve"]]
        if a["strategy"] == "RE":
            key = (a["segment"], a["region"])
            if key not in mk_cache:
                mk_cache[key] = re_market(a["segment"], a["region"], F, rng_m, n)
            fp = (F["fGCC"] if a["gcc_flag"] else F["f"]) if opts.recal else None
            AP[a["asset_id"]] = re_asset_paths(a, mk_cache[key], rng_m, n, lam, f_path=fp)
        elif a["strategy"] == "INF":
            AP[a["asset_id"]] = infra_paths(a, F, rng_m, n, lam)
        else:
            AP[a["asset_id"]] = enr_paths(a, F, rng_m, n)
    Xl = rng_d.standard_normal((n, T + 1))           # common lender factor per path-quarter
    agg = {k: np.zeros((n, T + 1)) for k in AGG_KEYS}
    outc = {k: np.zeros(n) for k in OUTC}
    diag = {"ladder": np.zeros(T + 1), "ladder_ctl": np.zeros(T + 1), "pfail": np.zeros((4, 2)),
            "trig_loans": [], "sleeve_net": {}}
    res = {"scenario": scen, "desc": sc.desc, "opts": opts.key(), "n": n, "sleeves": {}}
    for sl in C_SLEEVES:
        A_sl = [a for a in assets if a["sleeve"] == sl]
        T_sl = [t for t in tranches if t["sleeve"] == sl]
        res["sleeves"][sl] = simulate_sleeve(sl, A_sl, T_sl, AP, F, opts, rng_d, Xl, n, agg, outc, diag, sc)
    res["summary"] = summarize(agg, outc, diag, F, n)
    if keep:
        res["_agg"], res["_F"], res["_diag"] = agg, F, diag
    return res


def cap_cost(sofr, strike, years):
    return (np.maximum(sofr - strike, 0.0) + CAP_FWD_VOL) * years


def simulate_sleeve(sl, A_sl, T_sl, AP, F, opts, rng, Xl, n, agg, outc, diag, sc):
    strat = sl.split("_")[0]
    vehicle = "OE" if sl.endswith("_OE") else ("CE" if sl.endswith("_CE") else "DIR")
    nA, nT = len(A_sl), len(T_sl)
    aidx = {a["asset_id"]: j for j, a in enumerate(A_sl)}
    Vp = np.stack([AP[a["asset_id"]]["V"] for a in A_sl], axis=1).copy()
    NOIp = np.stack([AP[a["asset_id"]]["NOI"] for a in A_sl], axis=1).copy()
    CXp = np.stack([AP[a["asset_id"]]["capex"] for a in A_sl], axis=1)
    VAp = np.stack([AP[a["asset_id"]]["VA"] for a in A_sl], axis=1)
    VDp = np.stack([AP[a["asset_id"]].get("VD", AP[a["asset_id"]]["V"]) for a in A_sl], axis=1)
    frac = np.ones((n, nA))
    ctl_a = np.array([a["control"] in ("sole", "joint") for a in A_sl])
    gcc_a = np.array([a["gcc_flag"] == 1 for a in A_sl])
    pos = sorted({a["position_id"] for a in A_sl})
    pidx = np.array([pos.index(a["position_id"]) for a in A_sl])
    U = np.zeros((n, len(pos))); U0 = np.zeros(len(pos)); age_e = np.zeros((n, len(pos)))
    devpos = np.zeros(len(pos), dtype=bool)
    for a in A_sl:
        jp = pos.index(a["position_id"])
        U[:, jp] += a["unfunded_adic"]; U0[jp] += a["unfunded_adic"]
        age_e[:, jp] = a["age_q"] / 4
        devpos[jp] |= bool(a["dev_flag"])
    newpool = np.zeros(n)
    bal = np.tile(np.array([t["balance_adic"] for t in T_sl], float), (n, 1))
    mat = np.tile(np.array([t["maturity_q"] for t in T_sl], int), (n, 1))
    ext_left = np.tile(np.array([t["ext_options"] for t in T_sl], int), (n, 1))
    disc_left = np.full((n, nT), 2, dtype=int)
    forb_left = np.full((n, nT), 2, dtype=int)
    fixed_sh = np.tile(np.array([1.0 if t["rate_type"] == "fixed" else t["swap_share"] for t in T_sl]), (n, 1))
    cpn = np.tile(np.array([t["coupon"] if t["coupon"] > 0 else (C.R0 / 100 + t["spread"]) for t in T_sl]), (n, 1))
    spr = np.tile(np.array([t["spread"] for t in T_sl]), (n, 1))
    capk = np.tile(np.array([t["cap_strike"] for t in T_sl]), (n, 1))
    capx = np.tile(np.array([t["cap_expiry_q"] for t in T_sl], int), (n, 1))
    alive = np.ones((n, nT), dtype=bool)
    t_asset = np.array([aidx.get(t["asset_id"], -1) for t in T_sl])
    t_ctl = np.array([t["controllable"] == 1 for t in T_sl])
    t_rbl = np.array([t["lender"] == "rbl_syndicate" for t in T_sl])
    t_bridge = np.array([t["lender"] in ("debt_fund_clo", "cmbs_sasb", "mezz_fund") for t in T_sl])
    t_constr = np.array([t["dev_ltc"] > 0 for t in T_sl])
    t_nonrec = np.array(["nonrecourse" in t["recourse"] for t in T_sl]).astype(float)
    t_amort = [t["amort"] for t in T_sl]
    t_amyrs = np.array([max(t["amort_years"], 1.0) for t in T_sl])
    # project-finance debt service is sculpted to the plan CFADS at the archetype DSCR (G11 s6.10) [I]
    DSCR0 = {"CON_IDX": 1.25, "CON_FIX": 1.35, "REG": 1.45, "TOLL": 1.70, "AIR": 1.80, "MID": 2.50, "TOW": 2.00,
             "DC": 1.90, "MER": 1.80}
    sculpt_ds = np.zeros(nT)
    for j, t_ in enumerate(T_sl):
        if t_["amort"] == "sculpted" and t_asset[j] >= 0:
            a_ = A_sl[t_asset[j]]
            sculpt_ds[j] = a_["noi_yield"] * a_["gav_adic"] / 4 / DSCR0.get(a_["segment"], 1.3)
    rbl_last_x = np.tile(F["x"][:, :1], (1, nT))
    rbl_def = np.zeros((n, nT))
    trig = np.zeros((n, nT), dtype=bool)          # any covenant trigger within 4 quarters (per loan)
    keys = ("income", "exits", "calls", "prot_calls", "dist_stop", "cures", "shortfall", "dev", "debt", "V", "VA",
            "matured", "gap", "handback_eq", "sale_direct", "ext_paydown", "rbl_cures", "matured_ctl", "fund_loss",
            "oe_sales", "Vidx")
    o = {k: np.zeros((n, T + 1)) for k in keys}
    o["debt"][:, 0] = bal.sum(axis=1); o["V"][:, 0] = Vp[:, :, 0].sum(axis=1); o["VA"][:, 0] = VAp[:, :, 0].sum(axis=1)
    o["Vidx"][:, 0] = Vp[:, :, 0].sum(axis=1)
    fee = FEES[sl]
    y, r_s, f_all, fG, e_all, eRE = F["y"] / 100, F["r"] / 100, F["f"], F["fGCC"], F["e"], F["eRE"]
    T_ = C.TERMS
    p_ext_axis = T_["p_ext_g10"] if opts.ext == "g10" else np.zeros(3)
    Q = np.full(n, 0.10 if sl == "RE_OE" else 0.05)
    Qr = Q.copy(); Qadic = np.ones(n); adic_paid = np.zeros((n, T + 1))
    tr_gcc = np.array([(t_asset[j] >= 0) and bool(gcc_a[t_asset[j]]) for j in range(nT)])
    for t in range(1, T + 1):
        f_tr = np.where(tr_gcc[None, :], fG[:, t][:, None], f_all[:, t][:, None])     # (n, nT)
        noi_q = NOIp[:, :, t] / 4 * frac
        cap_q = CXp[:, :, t] * frac
        V_t = Vp[:, :, t] * frac
        VA_t = VAp[:, :, t] * frac
        sofr = r_s[:, t]
        # ---- interest and amortisation
        flo = sofr[:, None] + spr
        capped = (capk > 0) & (t <= capx)
        flo = np.where(capped, np.minimum(sofr[:, None], capk) + spr, flo)
        intr = bal * (fixed_sh * cpn + (1 - fixed_sh) * flo) / 4 * alive
        cap_int = np.where(t_constr[None, :], intr, 0.0)      # construction interest is capitalised (interest reserve)
        intr = intr - cap_int
        am = np.zeros((n, nT))
        for j in range(nT):
            if t_amort[j] in ("annuity30", "annuity"):
                c_ = np.maximum(cpn[:, j], 0.01)
                nyr = 30.0 if t_amort[j] == "annuity30" else t_amyrs[j]
                am[:, j] = bal[:, j] * (c_ / (1 - (1 + c_) ** -nyr) - c_) / 4
            elif t_amort[j] == "sculpted":
                am[:, j] = np.maximum(sculpt_ds[j] * 1.02 ** (t / 4) - intr[:, j], 0.0)
        am = np.minimum(am, bal) * alive
        ds_a = np.zeros((n, nA)); bal_a = np.zeros((n, nA))
        for j in range(nT):
            if t_asset[j] >= 0:
                ds_a[:, t_asset[j]] += intr[:, j] + am[:, j]
                bal_a[:, t_asset[j]] += bal[:, j]
        pool_int = sum((intr[:, j] for j in range(nT) if t_asset[j] < 0), np.zeros(n))
        # closed-end and open-end funds fund capex from calls / the line; direct owners fund it from cash
        cash_a = noi_q - ds_a - (cap_q if vehicle == "DIR" else 0.0)
        dscr_a = np.where(ds_a > 1e-12, noi_q / np.maximum(ds_a, 1e-12), 9.9)
        trap_lvl = np.zeros(nA)
        for j in range(nT):
            if t_asset[j] >= 0 and not A_sl[t_asset[j]]["dev_flag"]:      # no DSCR test during construction
                trap_lvl[t_asset[j]] = max(trap_lvl[t_asset[j]], T_sl[j]["cov_trap_dscr"])
        trapped = (dscr_a < trap_lvl[None, :]) & (ds_a > 0) & (frac > 0)
        for j in range(nT):
            if t_asset[j] >= 0 and t <= 4:
                trig[:, j] |= trapped[:, t_asset[j]] & alive[:, j]
        short = np.maximum(-cash_a, 0.0) * (frac > 0)
        sweep_a = np.where(trapped, np.maximum(cash_a, 0.0), 0.0)
        dist_a = np.where(trapped, 0.0, np.maximum(cash_a, 0.0))
        for j in range(nT):
            if t_asset[j] >= 0:
                ja = t_asset[j]
                share = np.where(bal_a[:, ja] > 0, bal[:, j] / np.maximum(bal_a[:, ja], 1e-12), 0.0)
                bal[:, j] = np.maximum(0.0, bal[:, j] - am[:, j] - sweep_a[:, ja] * share) + cap_int[:, j]
            else:
                bal[:, j] = np.maximum(0.0, bal[:, j] - am[:, j])
        cure_cash = np.zeros(n); coinv_cash = np.zeros(n); fund_need = np.zeros(n); short_cash = np.zeros(n)
        eq_a = V_t - bal_a
        if vehicle == "DIR":
            pay_short = np.where(ctl_a[None, :], (opts.varpi >= 1.0) | (eq_a > 0), eq_a > 0)
            short_cash += (short * pay_short * ctl_a[None, :]).sum(axis=1)
            coinv_cash += (short * pay_short * (~ctl_a)[None, :]).sum(axis=1) * (1.0 if opts.coinv_participate else 0.0)
            hb = (short > 1e-9) & ~pay_short
        else:
            fund_need += (short * (eq_a > 0)).sum(axis=1)
            hb = (short > 1e-9) & (eq_a <= 0)
        if hb.any():
            for j in range(nT):
                if t_asset[j] >= 0:
                    kill = hb[:, t_asset[j]]
                    bal[kill, j] = 0.0; alive[kill, j] = False
            o["handback_eq"][:, t] += (np.maximum(eq_a, 0) * hb).sum(axis=1)
            frac = np.where(hb, 0.0, frac)
        # ---- maintenance LTV covenants (appraisal basis)
        cov_need = np.zeros((n, nT))
        for j in range(nT):
            lim = T_sl[j]["cov_ltv_max"]
            if lim <= 0:
                continue
            if t_asset[j] >= 0:
                ja = t_asset[j]
                ex = np.maximum(bal_a[:, ja] - lim * VA_t[:, ja], 0.0) * (bal_a[:, ja] > 0)
                share = np.where(bal_a[:, ja] > 0, bal[:, j] / np.maximum(bal_a[:, ja], 1e-12), 0.0)
                cov_need[:, j] = ex * share * alive[:, j]
            else:
                tot_b = bal.sum(axis=1); tot_v = VA_t.sum(axis=1) + newpool
                cov_need[:, j] = np.maximum(tot_b - lim * tot_v, 0.0) * alive[:, j]
            if t <= 4:
                trig[:, j] |= cov_need[:, j] > 1e-9
        # ---- RBL redeterminations
        for j in np.where(t_rbl)[0]:
            ja = t_asset[j]
            redet = (t >= T_sl[j]["rbl_redet_q"]) and ((t - T_sl[j]["rbl_redet_q"]) % 2 == 0)
            jumpx = np.abs(F["x"][:, t] - rbl_last_x[:, j]) >= 0.20
            do = (redet | jumpx) & alive[:, j]
            adv = T_sl[j]["rbl_adv"] - 0.10 * np.isin(F["z"][:, t], [C.ZSG, C.ZDB])
            bb = adv * VDp[:, ja, t] * frac[:, ja]
            rbl_def[:, j] = np.where(do, np.maximum(bal[:, j] - bb, 0.0), rbl_def[:, j])
            rbl_last_x[:, j] = np.where(do, F["x"][:, t], rbl_last_x[:, j])
            if t <= 4:
                trig[:, j] |= do & (rbl_def[:, j] > 1e-9)
            pay = rbl_def[:, j] / 2
            from_cash = np.minimum(pay, dist_a[:, ja])
            dist_a[:, ja] -= from_cash
            eq_need = pay - from_cash
            if vehicle == "DIR" and t_ctl[j]:
                ok = (opts.varpi >= 1.0) | (eq_a[:, ja] > eq_need)
                cure_cash += np.where(ok, eq_need, 0.0)
                o["rbl_cures"][:, t] += np.where(ok, eq_need, 0.0)
            else:
                ok = eq_a[:, ja] > eq_need
                if vehicle == "DIR":
                    part = 1.0 if opts.coinv_participate else 0.0
                    coinv_cash += np.where(ok, eq_need, 0.0) * part
                    o["rbl_cures"][:, t] += np.where(ok, eq_need, 0.0) * part
                else:
                    fund_need += np.where(ok, eq_need, 0.0)
            fail = ~ok & (eq_need > 1e-12)
            bal[:, j] = np.maximum(0.0, bal[:, j] - np.where(ok, pay, 0.0))
            rbl_def[:, j] = np.where(ok, np.maximum(rbl_def[:, j] - pay, 0.0), rbl_def[:, j])
            if fail.any():
                bal[fail, j] = 0.0; alive[fail, j] = False
                o["handback_eq"][:, t] += np.where(fail, np.maximum(eq_a[:, ja], 0), 0.0)
                frac[fail, ja] = 0.0
        # ---- maturities and covenant cures (s4.5)
        for j in range(nT):
            due = (mat[:, j] == t) & alive[:, j] & (bal[:, j] > 1e-12)
            cov = cov_need[:, j] > 1e-9
            if not (due.any() or cov.any()):
                continue
            ja = t_asset[j]
            if ja >= 0:
                Vm, NOIa, VAj = V_t[:, ja], noi_q[:, ja] * 4, VA_t[:, ja]
                sib = np.maximum(bal_a[:, ja] - bal[:, j], 0.0)
            else:
                Vm, NOIa, VAj = V_t.sum(axis=1) + newpool, noi_q.sum(axis=1) * 4, VA_t.sum(axis=1) + newpool
                sib = bal.sum(axis=1) - bal[:, j]
            fj = f_tr[:, j]
            Dj = bal[:, j].copy()
            lmax = T_["ltv_max"][fj].copy(); dmin = T_["dscr_min"][fj].copy(); dymin = T_["dy_min"][fj].copy()
            av = T_["avail"][fj].copy(); sadd = T_["spread_add"][fj].copy()
            if strat == "INF":
                lmax += C.INFRA_ADJ["ltv"]; dmin += C.INFRA_ADJ["dscr"]; av = np.minimum(av + C.INFRA_ADJ["avail"], 0.99)
                dymin = np.zeros(n); sadd = sadd + C.INFRA_ADJ["spread"]
            if strat == "ENR":
                cut = 0.10 * np.isin(F["z"][:, t], [C.ZSG, C.ZDB])
                lmax = np.maximum(lmax - 0.05 - cut, 0.30); dmin = dmin - 0.10; dymin = np.zeros(n)
            r_new = np.where(t_bridge[j], sofr + BRIDGE_SPREAD + sadd, y[:, t] + SPREAD_FIX[strat] + sadd)
            k_new = r_new + 0.01
            lender = (math.sqrt(RHO_LENDER) * Xl[:, t] + math.sqrt(1 - RHO_LENDER) * rng.standard_normal(n)) < ndtri(av)
            rbl_cap = None
            if t_rbl[j]:
                rbl_cap = (T_sl[j]["rbl_adv"] - 0.10 * np.isin(F["z"][:, t], [C.ZSG, C.ZDB])) * VDp[:, ja, t] * frac[:, ja]
            dscr_now = NOIa / np.maximum(4 * (intr[:, j] + am[:, j]) + (4 * (ds_a[:, ja] - intr[:, j] - am[:, j]) if ja >= 0 else 0), 1e-12)
            ell = T_["ell"][fj] if (t_ctl[j] and vehicle == "DIR") else ELL_GP[fj]
            cur_rate = fixed_sh[:, j] * cpn[:, j] + (1 - fixed_sh[:, j]) * flo[:, j]
            gap_pp = (r_new - cur_rate) * 100
            dec = decide_maturity(Dj, sib, Vm, NOIa, VAj, lmax, dmin, dymin, k_new, lender, due, ext_left[:, j],
                                  T_sl[j]["ext_dscr"], T_sl[j]["ext_dy"], T_sl[j]["ext_ltv"], dscr_now,
                                  p_ext_axis[fj], rng.random(n), disc_left[:, j], forb_left[:, j], t_nonrec[j],
                                  bool(t_ctl[j] and vehicle == "DIR"), opts.varpi, ell, T_["sale_disc"][fj],
                                  cov_gap=cov_need[:, j], rbl_cap=rbl_cap, gap_pp=gap_pp * ROLL_DAMP[fj],
                                  u_sale=rng.random(n), beta_sale=(opts.beta_roll if strat == "RE" else 0.0))
            if t_constr[j]:
                pass   # construction facility: same capacity test on completion value (V^mat includes drawn value)
            gapj, refi, ext_ok, dext, forbear = dec["gap"], dec["refi"], dec["ext_ok"], dec["dext"], dec["forbear"]
            cure, sell, hand, act = dec["cure"], dec["sell"], dec["hand"], dec["act"]
            o["matured"][:, t] += np.where(due, Dj, 0.0)
            diag["ladder"][t] += float(np.where(due, Dj, 0.0).mean())
            if t_ctl[j]:
                o["matured_ctl"][:, t] += np.where(due, Dj, 0.0)
                diag["ladder_ctl"][t] += float(np.where(due, Dj, 0.0).mean())
            o["gap"][:, t] += np.where(act, gapj, 0.0)
            paydown = np.where(ext_ok, T_sl[j]["ext_paydown"] * Dj, 0.0) + np.where(dext, 0.05 * Dj, 0.0)
            capbuy = np.where((ext_ok | dext) & (capk[:, j] > 0), cap_cost(sofr, capk[:, j], T_sl[j]["ext_len_q"] / 4) * Dj, 0.0)
            pen = np.where(forbear, 0.02 / 4 * Dj, 0.0)                      # default interest while forborne
            need = np.where(cure, gapj, 0.0) + paydown + capbuy + pen
            if vehicle == "DIR":
                if t_ctl[j]:
                    cure_cash += need
                elif opts.coinv_participate:
                    coinv_cash += need
                else:
                    frac[:, ja] = np.where(need > 0, frac[:, ja] * np.clip(1 - need / np.maximum(dec["V_eq"], 1e-9), 0, 1), frac[:, ja])
            else:
                fund_need += need
            o["ext_paydown"][:, t] += paydown + capbuy
            newbal = np.where(cure, Dj - gapj, Dj) - paydown
            bal[:, j] = np.where(act & ~(sell | hand), np.maximum(newbal, 0.0), bal[:, j])
            nrefi = refi | (cure & due)
            cpn[:, j] = np.where(nrefi, r_new, np.where(dext, cpn[:, j] + 0.005, cpn[:, j]))
            spr[:, j] = np.where(nrefi & t_bridge[j], BRIDGE_SPREAD + sadd, np.where(dext, spr[:, j] + 0.005, spr[:, j]))
            fixed_sh[:, j] = np.where(nrefi, 0.0 if t_bridge[j] else 1.0, fixed_sh[:, j])
            term = NEW_TERM_Q["bridge"] if t_bridge[j] else NEW_TERM_Q[strat]
            mat[:, j] = np.where(nrefi, t + term, np.where(ext_ok, mat[:, j] + T_sl[j]["ext_len_q"],
                                 np.where(dext, mat[:, j] + 4, np.where(forbear, mat[:, j] + 1, mat[:, j]))))
            capx[:, j] = np.where(nrefi & t_bridge[j], t + 12, np.where(ext_ok | dext, mat[:, j], capx[:, j]))
            capk[:, j] = np.where(nrefi & t_bridge[j], sofr + 0.01, capk[:, j])
            ext_left[:, j] -= ext_ok.astype(int)
            disc_left[:, j] -= dext.astype(int)
            forb_left[:, j] -= forbear.astype(int)
            exit_mask = sell | hand
            if exit_mask.any():
                if ja >= 0:
                    proceeds = np.where(sell, np.maximum(dec["sale_val"], 0.0), 0.0)
                    if vehicle == "DIR":
                        o["sale_direct"][:, t] += proceeds
                    elif vehicle == "CE":
                        o["exits"][:, t] += proceeds
                    o["handback_eq"][:, t] += np.where(hand, np.maximum(dec["V_eq"], 0.0), 0.0)
                    for jj in range(nT):
                        if t_asset[jj] == ja:
                            bal[exit_mask, jj] = 0.0; alive[exit_mask, jj] = False
                    frac[exit_mask, ja] = 0.0
                else:                                   # fund line not refinanced: repay the gap from the fund
                    fund_need += np.where(exit_mask, gapj, 0.0)
                    bal[:, j] = np.where(exit_mask, Dj - gapj, bal[:, j])
            for k_, m_ in (("refi", refi), ("ext_contract", ext_ok), ("ext_discretionary", dext), ("cure", cure & due),
                           ("sale", sell), ("handback", hand), ("forbear", forbear)):
                outc[k_] += m_.astype(float)
            if strat == "INF" and ja >= 0:
                failed = due & ~(refi | (cure & due) | ext_ok | dext)
                for s_ in range(4):
                    m_ = F["g11"][:, t] == s_
                    diag["pfail"][s_, 0] += float((Dj * (due & m_)).sum())
                    diag["pfail"][s_, 1] += float((Dj * (failed & m_)).sum())
        # recompute asset debt after maturities
        bal_a = np.zeros((n, nA))
        for j in range(nT):
            if t_asset[j] >= 0:
                bal_a[:, t_asset[j]] += bal[:, j]
        # ---- vehicle layer
        e_use = eRE[:, t] if strat == "RE" else e_all[:, t]
        dsc_t = T_["sale_disc"][f_all[:, t]]
        if vehicle == "CE":
            if sc.calls_t4p and t <= 8 and opts.calls != "structural":
                calls = (1 - (1 - 0.28 * 1.38) ** 0.25) * U
            elif opts.calls == "structural":
                base = {"RE": np.array([0.25, 0.30, 0.35, 0.40]), "INF": np.array([0.20, 0.25, 0.30, 0.35]),
                        "ENR": np.array([0.25, 0.25, 0.25, 0.25])}[strat]
                ab = np.clip(age_e.astype(int), 0, 3)
                calls = (1 - np.exp(-base[ab] * np.array([1.2, 1.0, 0.75, 0.6])[e_use][:, None] / 4)) * U
            else:
                calls = (1 - (1 - CANON_CALL[e_use])[:, None] ** 0.25) * U
            U = U - calls + PACE.get(sl, 0.0) * PACE_TOTAL / 4 / len(pos)
            newpool = newpool + calls.sum(axis=1)
            o["calls"][:, t] += calls.sum(axis=1)
            kap = np.array([1.2, 1.0, 0.6, 0.5])[e_use]
            if strat == "RE":
                d_bar = np.select([age_e < 3, age_e < 5, age_e < 7, age_e < 9], [0.03, 0.12, 0.22, 0.30], 0.35)
                x_rate = d_bar * np.array([1.3, 1.0, 0.45, 0.25])[e_use][:, None]
            elif strat == "INF":
                x_rate = np.tile(np.array([0.14, 0.10, 0.04, 0.015])[e_use][:, None], (1, len(pos)))
            else:
                F3 = curve(F["x"][:, t], F["z"][:, t])[:, 2]
                x_rate = np.tile((0.10 * np.array([1.3, 1.0, 0.6, 0.3])[e_use] * np.exp(1.2 * np.log(F3 / C.P_LR)))[:, None],
                                 (1, len(pos)))
            xq = 1 - np.exp(-x_rate / 4)
            xa = xq[:, pidx]
            eq_sold = xa * np.maximum(V_t * (1 - dsc_t[:, None]) - bal_a, 0.0)
            mD_young = np.array([1.3, 1.0, 0.45, 0.25])[e_use]
            npx = (1 - np.exp(-0.03 * mD_young / 4)) * newpool          # new investments exit at the young-fund rate
            o["exits"][:, t] += eq_sold.sum(axis=1) + npx
            newpool = newpool - npx
            for j in range(nT):
                if t_asset[j] >= 0:
                    bal[:, j] *= (1 - xa[:, t_asset[j]])
            frac = frac * (1 - xa)
            age_e = age_e + kap[:, None] / 4
            fee_q = fee / 4 * np.maximum(VA_t.sum(axis=1) + newpool - bal.sum(axis=1), 0.0)
            np_inc = newpool * {"RE": 0.035, "INF": 0.05, "ENR": 0.06}[strat] / 4
            inc = 0.8 * np.maximum(dist_a.sum(axis=1) + np_inc - fee_q, 0.0)
            need = fund_need if opts.fund_module else np.zeros(n)
            stop = np.minimum(need, inc)
            rem = need - stop
            Usum = U.sum(axis=1)
            prot = np.minimum(rem, Usum)
            U = U * np.where(Usum[:, None] > 0, (1 - prot / np.maximum(Usum, 1e-12))[:, None], 1.0)
            o["income"][:, t] += inc - stop
            o["dist_stop"][:, t] += stop
            o["prot_calls"][:, t] += prot
            o["cures"][:, t] += need
            o["fund_loss"][:, t] += rem - prot
        elif vehicle == "OE":
            fee_q = fee / 4 * np.maximum(VA_t.sum(axis=1) - bal.sum(axis=1), 0.0)
            inc = 0.9 * np.maximum(dist_a.sum(axis=1) - pool_int - fee_q, 0.0)
            need = fund_need if opts.fund_module else np.zeros(n)
            stop = np.minimum(need, inc)
            rem = need - stop
            # remainder met by pro-rata asset sales at the stressed discount (NAV loss = discount on sold assets)
            eqv = np.maximum(V_t * (1 - dsc_t[:, None]) - bal_a, 0.0)
            sfrac = np.clip(rem / np.maximum(eqv.sum(axis=1), 1e-9), 0.0, 1.0)
            o["fund_loss"][:, t] += sfrac * (V_t.sum(axis=1) * dsc_t)
            o["oe_sales"][:, t] += rem
            frac = frac * (1 - sfrac[:, None])
            for j in range(nT):
                bal[:, j] *= (1 - sfrac)
            line = [j for j in range(nT) if t_asset[j] < 0]
            if line:
                bal[:, line[0]] += cap_q.sum(axis=1)          # capex on the fund line (G10)
            o["income"][:, t] += inc - stop
            o["dist_stop"][:, t] += stop
            o["cures"][:, t] += need
            navA = np.maximum(VA_t.sum(axis=1) - bal.sum(axis=1), 1e-9)
            gapA = np.log(np.maximum(VA_t.sum(axis=1), 1e-9)) - np.log(np.maximum(V_t.sum(axis=1), 1e-9))
            req = 0.006 + 0.12 * np.maximum(0.0, gapA)
            disp = np.array([0.010, 0.006, 0.004, 0.002])[e_use]

            def Lcap(q_):
                contrib = np.where((gapA > 0.03) | (q_ > 0.05), 0.004, 0.012)
                return np.maximum(0.0, 0.0025 + disp * VA_t.sum(axis=1) / navA + contrib - need / navA)
            Q = np.maximum(0.0, Q + req - np.where(gapA <= 0.03, 0.08 * Q, 0.0))
            Q = Q - np.minimum(Q, Lcap(Q))
            Qr = np.maximum(0.0, Qr + req - np.where(gapA <= 0.03, 0.08 * Qr, 0.0))
            tot = Qr + 0.05 * Qadic
            pay = np.minimum(tot, Lcap(tot))
            frc = np.where(tot > 0, pay / np.maximum(tot, 1e-12), 0.0)
            paid = np.minimum(Qadic, frc * Qadic)
            Qadic = Qadic - paid
            Qr = Qr * (1 - frc)
            adic_paid[:, t] = paid
        else:
            fee_q = fee / 4 * np.maximum(VA_t.sum(axis=1) - bal.sum(axis=1), 0.0)
            inc = np.maximum(dist_a.sum(axis=1) - fee_q, 0.0)
            if not ctl_a.all():          # minority co-investments exit on the sponsor's clock (G15: 12% / 4%)
                rate_co = np.array([0.156, 0.12, 0.054, 0.03])[e_use]
                xco = (1 - np.exp(-rate_co / 4))[:, None] * (~ctl_a)[None, :]
                o["exits"][:, t] += (xco * np.maximum(V_t * (1 - dsc_t[:, None]) - bal_a, 0.0)).sum(axis=1)
                for j in range(nT):
                    if t_asset[j] >= 0:
                        bal[:, j] *= (1 - xco[:, t_asset[j]])
                frac = frac * (1 - xco)
            dev = np.zeros(n)
            for jp in range(len(pos)):
                if U0[jp] <= 0:
                    continue
                base_draw = np.minimum(U[:, jp], U0[jp] / 8.0) if devpos[jp] else (1 - np.exp(-0.20 / 4)) * U[:, jp]
                draw = base_draw * np.where(F["S"][:, t] == C.CRIS, 1.15, 1.0) if devpos[jp] else base_draw
                U[:, jp] -= base_draw
                dev += draw
                ja0 = [jj for jj, a in enumerate(A_sl) if a["position_id"] == pos[jp]][0]
                add = base_draw * (1.25 if devpos[jp] else 1.0) / np.maximum(frac[:, ja0], 1e-6)
                Vp[:, ja0, t:] += add[:, None]
                NOIp[:, ja0, t:] += (add * A_sl[ja0]["noi_yield"])[:, None]
            o["dev"][:, t] += dev
            o["income"][:, t] += inc
            o["cures"][:, t] += cure_cash + coinv_cash
            o["shortfall"][:, t] += short_cash
            agg["cures_coinv"][:, t] += coinv_cash
            agg["cures_direct"][:, t] += cure_cash
            agg["shortfall_direct"][:, t] += short_cash
        o["debt"][:, t] = bal.sum(axis=1)
        o["Vidx"][:, t] = Vp[:, :, t].sum(axis=1)
        o["V"][:, t] = (Vp[:, :, t] * frac).sum(axis=1) + (newpool if vehicle == "CE" else 0.0)
        o["VA"][:, t] = (VAp[:, :, t] * frac).sum(axis=1) + (newpool if vehicle == "CE" else 0.0)
        if vehicle != "DIR":
            agg["fund_need"][:, t] += o["cures"][:, t]
        if t_ctl.any():
            agg["debt_ctl"][:, t] += (bal * t_ctl[None, :]).sum(axis=1)
            agg["V_ctl"][:, t] += (Vp[:, :, t] * frac * ctl_a[None, :]).sum(axis=1)
    if t_ctl.any():
        agg["debt_ctl"][:, 0] += float((np.array([t["balance_adic"] for t in T_sl]) * t_ctl).sum())
        agg["V_ctl"][:, 0] += (Vp[:, :, 0] * ctl_a[None, :]).sum(axis=1)
    for k_src, k_dst in (("income", "income"), ("exits", "exits"), ("calls", "calls"), ("prot_calls", "prot_calls"),
                         ("dist_stop", "dist_stop"), ("dev", "dev_draws"), ("debt", "debt"), ("V", "V"), ("VA", "VA"),
                         ("matured", "matured"), ("gap", "gap"), ("handback_eq", "handback_equity"),
                         ("sale_direct", "sale_proceeds_direct"), ("ext_paydown", "ext_paydown"),
                         ("rbl_cures", "rbl_cures"), ("matured_ctl", "matured_ctl"), ("fund_loss", "fund_loss"),
                         ("oe_sales", "oe_sales"), ("Vidx", "Vidx")):
        agg[k_dst] += o[k_src]
    diag.setdefault("Vidx_by_sleeve", {})[sl] = o["Vidx"]
    diag["trig_loans"].extend([(sl, bool(t_ctl[j]), float(trig[:, j].mean())) for j in range(nT)])
    net = o["income"] + o["exits"] + o["sale_direct"] - o["calls"] - o["prot_calls"] - o["dev"]
    if vehicle == "DIR":
        net = net - o["cures"] - o["shortfall"]
    diag["sleeve_net"][sl] = net

    def pct(x):
        return [round(float(np.percentile(x, p)), 3) for p in (5, 50, 95)]
    row = {"net_12m_P5_P50_P95": pct(net[:, 1:5].sum(axis=1)), "net_24m_P5_P50_P95": pct(net[:, 1:9].sum(axis=1)),
           "net_12m_mean": round(float(net[:, 1:5].sum(axis=1).mean()), 3),
           "net_24m_mean": round(float(net[:, 1:9].sum(axis=1).mean()), 3),
           "mean_24m": {k: round(float(o[k][:, 1:9].sum(axis=1).mean()), 4) for k in
                        ("income", "exits", "calls", "prot_calls", "dist_stop", "cures", "shortfall", "dev",
                         "sale_direct", "handback_eq", "gap", "matured", "fund_loss")},
           "mean_12m": {k: round(float(o[k][:, 1:5].sum(axis=1).mean()), 4) for k in
                        ("income", "exits", "calls", "prot_calls", "dist_stop", "cures", "shortfall", "dev", "sale_direct")},
           "ltv_econ_P50_t0_t4_t8": [round(float(np.median(o["debt"][:, k] / np.maximum(o["V"][:, k], 1e-9))), 3) for k in (0, 4, 8)],
           "ltv_econ_t8_P95": round(float(np.percentile(o["debt"][:, 8] / np.maximum(o["V"][:, 8], 1e-9), 95)), 3),
           "value_true_change_t4_P50": round(float(np.median(o["V"][:, 4] / o["V"][:, 0] - 1)), 3)}
    if vehicle == "OE":
        row["queue_others_end_P50"] = round(float(np.median(Q)), 3)
        row["adic_full_redemption_paid_by_q4_q8_P50"] = [round(float(np.median(adic_paid[:, 1:5].sum(axis=1))), 3),
                                                         round(float(np.median(adic_paid[:, 1:9].sum(axis=1))), 3)]
        row["adic_full_redemption_paid_by_q4_P5"] = round(float(np.percentile(adic_paid[:, 1:5].sum(axis=1), 5)), 3)
    return row


def cvar(x, a=0.95):
    q = np.percentile(x, 100 * a)
    tail = x[x >= q]
    return float(tail.mean()) if tail.size else float(q)


def summarize(agg, outc, diag, F, n):
    def p3(x):
        return [round(float(np.percentile(x, p)), 3) for p in (5, 50, 95)]
    inflow = agg["income"] + agg["exits"] + agg["sale_proceeds_direct"]
    outflow = (agg["calls"] + agg["prot_calls"] + agg["dev_draws"] + agg["cures_direct"] + agg["cures_coinv"]
               + agg["shortfall_direct"])
    net = inflow - outflow
    adic_cures = agg["cures_direct"] + agg["shortfall_direct"] + agg["cures_coinv"]
    s = {}
    ctl_cures = agg["cures_direct"] + agg["shortfall_direct"]
    for h, lab in ((4, "12m"), (8, "24m"), (20, "60m")):
        w = slice(1, h + 1)
        m = lambda k: round(float(agg[k][:, w].sum(axis=1).mean()), 3)
        s[lab] = {"income": m("income"), "exits": m("exits"), "sale_proceeds_direct": m("sale_proceeds_direct"),
                  "calls": m("calls"), "protective_calls": m("prot_calls"), "distribution_stop": m("dist_stop"),
                  "dev_draws": m("dev_draws"), "cures_direct_controlled": m("cures_direct"),
                  "shortfalls_direct": m("shortfall_direct"), "cures_coinvest": m("cures_coinv"),
                  "fund_level_need": m("fund_need"), "fund_level_unfunded_loss": m("fund_loss"),
                  "matured": m("matured"), "gap": m("gap"), "handback_equity": m("handback_equity"),
                  "net_mean": round(float(net[:, w].sum(axis=1).mean()), 3), "net_P5_P50_P95": p3(net[:, w].sum(axis=1)),
                  "adic_direct_cures_mean": round(float(adic_cures[:, w].sum(axis=1).mean()), 3),
                  "adic_direct_cures_CVaR95": round(cvar(adic_cures[:, w].sum(axis=1)), 3),
                  "controlled_cures_mean": round(float(ctl_cures[:, w].sum(axis=1).mean()), 3),
                  "controlled_cures_CVaR95": round(cvar(ctl_cures[:, w].sum(axis=1)), 3),
                  "adic_cure_cash_incl_protective_calls_CVaR95": round(cvar((adic_cures + agg["prot_calls"])[:, w].sum(axis=1)), 3),
                  "fund_level_need_CVaR95": round(cvar(agg["fund_need"][:, w].sum(axis=1)), 3)}
    ltv = agg["debt"] / np.maximum(agg["V"], 1e-9)
    ltvA = agg["debt"] / np.maximum(agg["VA"], 1e-9)
    s["ltv_lookthrough_econ"] = {"t0": round(float(ltv[:, 0].mean()), 3), "t4_P5_P50_P95": p3(ltv[:, 4]),
                                 "t8_P5_P50_P95": p3(ltv[:, 8]), "peak_8q_P50_P95": p3(ltv[:, 1:9].max(axis=1))[1:]}
    s["ltv_lookthrough_appraisal_P50_t4_t8"] = [round(float(np.median(ltvA[:, 4])), 3), round(float(np.median(ltvA[:, 8])), 3)]
    ltvc = agg["debt_ctl"] / np.maximum(agg["V_ctl"], 1e-9)
    s["ltv_controllable_econ"] = {"t0": round(float(ltvc[:, 0].mean()), 3), "t8_P50_P95": p3(ltvc[:, 8])[1:]}
    s["value_change_true_P50_t4_t8"] = [round(float(np.median(agg["V"][:, k] / agg["V"][:, 0] - 1)), 3) for k in (4, 8)]
    s["market_value_index_change_P50_t4_t8"] = [round(float(np.median(agg["Vidx"][:, k] / agg["Vidx"][:, 0] - 1)), 3) for k in (4, 8)]
    s["market_value_index_change_P5_t4_t8"] = [round(float(np.percentile(agg["Vidx"][:, k] / agg["Vidx"][:, 0] - 1, 5)), 3) for k in (4, 8)]
    by = {}
    for sl_, arr in diag.get("Vidx_by_sleeve", {}).items():
        by[sl_] = [round(float(np.median(arr[:, k] / arr[:, 0] - 1)), 3) for k in (4, 8)]
    s["market_value_index_change_by_sleeve_P50_t4_t8"] = by
    # LTV with debt held at t0 and the market value index (comparable to G15's 'debt fixed' stressed LTV)
    s["ltv_debt_fixed_on_value_index_P50_t4_t8"] = [round(float(np.median(agg["debt"][:, 0] / agg["Vidx"][:, k])), 3) for k in (4, 8)]
    s["ltv_debt_fixed_on_value_index_P95_t4_t8"] = [round(float(np.percentile(agg["debt"][:, 0] / agg["Vidx"][:, k], 95)), 3) for k in (4, 8)]
    s["value_change_appraisal_P50_t4_t8"] = [round(float(np.median(agg["VA"][:, k] / agg["VA"][:, 0] - 1)), 3) for k in (4, 8)]
    s["ladder_mean_bn_by_quarter"] = [round(float(x), 3) for x in diag["ladder"][1:]]
    s["ladder_controllable_mean_bn_by_quarter"] = [round(float(x), 3) for x in diag["ladder_ctl"][1:]]
    tot = sum(float(v.sum()) for v in outc.values())
    s["maturity_outcomes_share_of_events"] = {k: round(float(v.sum()) / max(tot, 1e-9), 4) for k, v in outc.items()}
    pf = diag["pfail"]
    s["infra_unrefinanced_share_by_G11_state"] = {C.G11_NAMES[k]: (round(pf[k, 1] / pf[k, 0], 4) if pf[k, 0] > 0 else None)
                                                  for k in range(4)}
    ctl_trig = [p for sl, c, p in diag["trig_loans"] if c]
    s["covenant_trigger_12m_controllable"] = {"mean_share_of_loans": round(float(np.mean(ctl_trig)), 4) if ctl_trig else None,
                                              "max_per_loan": round(float(np.max(ctl_trig)), 4) if ctl_trig else None,
                                              "loans_above_2pct": int(sum(p > 0.02 for p in ctl_trig))}
    s["state_shares_q4"] = {"crisis": round(float((F["S"][:, 4] == C.CRIS).mean()), 3),
                            "f_N_T_C": [round(float((F["f"][:, 4] == k).mean()), 3) for k in range(3)]}
    s["sleeve_net_24m_mean"] = {k: round(float(v[:, 1:9].sum(axis=1).mean()), 3) for k, v in diag["sleeve_net"].items()}
    return s


PLAN = [("normal", {}), ("drought", {}), ("base_mc", {}), ("t4p_struct", {}), ("t4p_ratesflat", {}), ("rate_shock", {}),
        ("gulf_persist", {}), ("sg_glut", {}),
        ("base_mc", {"recal": False}), ("t4p_struct", {"recal": False}),
        ("base_mc", {"ext": "zero"}), ("base_mc", {"varpi": 0.0}), ("base_mc", {"beta_roll": 0.0}),
        ("t4p_struct", {"ext": "zero"}), ("t4p_struct", {"varpi": 0.0}), ("t4p_struct", {"ext": "zero", "varpi": 0.0}),
        ("t4p_struct", {"fund_module": False}), ("t4p_struct", {"calls": "structural"}),
        ("t4p_struct", {"coinv_participate": False}), ("t4p_struct", {"beta_roll": 0.0}),
        ("base_mc", {"gcc_gw_floor": C.fC})]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    t0 = time.time()
    results = {"label": C.LABEL, "n_paths": n, "T_quarters": T, "seed": SEED, "runs": {},
               "regime_table": C.regime_table(), "sloos_calibration": C.SLOOS, "pz_quarterly": C.PZ_Q_DIAG,
               "tape_manifest_files": load_tape()[2]["files"]}
    for scen, kw in PLAN:
        op = Opts(**kw)
        r = run(scen, n=n, opts=op)
        key = f"{scen}|{op.key()}"
        results["runs"][key] = r
        s = r["summary"]
        print(f"{key:88s} net12 {s['12m']['net_mean']:+.2f} net24 {s['24m']['net_mean']:+.2f} "
              f"cureCVaR24 {s['24m']['adic_cure_cash_incl_protective_calls_CVaR95']:.2f} "
              f"LTVt8 {s['ltv_lookthrough_econ']['t8_P5_P50_P95']} [{time.time() - t0:.0f}s]", flush=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, default=float)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
