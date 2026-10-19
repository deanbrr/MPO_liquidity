"""G10 stream: prototype real-estate engine for the Real Assets group (SYNTHETIC - NOT ADIC DATA).

Implements, on a synthetic $9.0bn real-estate sleeve of the $18bn Real Assets working NAV (sub-book totals aligned
with the G15 synthetic book; position-level detail is G10's):
  1. factor paths (10y yield, short rate, inflation, growth gap, credit spread, regime S, shock type Z,
     real-estate transaction window eRE) from the October-2026 state, plus named scenarios;
  2. sector x region property engines: market rent, lease roll, occupancy, sticky opex -> NOI; cap-rate process
     loaded on the 10y yield and credit spread; true value V = NOI_fwd / c; Geltner-smoothed appraisal value;
  3. position wrappers: open-end core funds (queue machine calibrated on ODCE 2022-26), closed-end VA/opportunistic
     fund interests (RFT-TA-style calls/distributions on an effective-age clock), JVs, direct assets, co-investments;
  4. asset-level debt with fixed/floating legs, a maturity ladder and refinancing under LTV and DSCR caps, with
     extension, equity cure or non-recourse hand-back;
  5. cash-map and risk outputs by scenario (P5/P50/P95), on common random numbers across scenarios.
Every number produced here is SYNTHETIC. Parameters marked [I] are design defaults to be calibrated.

Usage: python -I g10_re_engine.py <calc_dir> [n_paths]
"""
import json
import sys

import numpy as np

CALC = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
T = 20                      # quarters
SEED = 20261018

SECT = ["LOG", "RES", "OFF", "RET", "DC", "HOT", "ALT"]
EXP, LATE, CRIS, RECV = 0, 1, 2, 3
ZN, ZGW, ZDB = 0, 1, 2
eO, eN, eD, eF = 0, 1, 2, 3

# Sector parameters [I unless noted]; see dossier section 6 table.
# Recalibrated so that sleeve NOI growth at ~3.5% CPI is ~1-2%/yr, near NCREIF's 0.78% trailing same-store NOI
# growth (2Q2026 webinar) rather than CPI: real market-rent drift is negative outside logistics/data centres.
SP = {
    "LOG": dict(c_app=0.041, walt=5.0, esc=0.03, bpi=0.5, mu=-0.010, bg=1.0, occ=0.94, bo=0.5, phi=0.10, capex=0.008, sm=0.04, m2m=0.10, drift=0),
    "RES": dict(c_app=0.043, walt=1.0, esc=0.00, bpi=0.6, mu=-0.015, bg=0.8, occ=0.94, bo=0.5, phi=0.38, capex=0.012, sm=0.035, m2m=0.00, drift=0),
    "OFF": dict(c_app=0.062, walt=6.0, esc=0.025, bpi=0.3, mu=-0.020, bg=1.5, occ=0.82, bo=1.5, phi=0.40, capex=0.025, sm=0.06, m2m=-0.10, drift=10),
    "RET": dict(c_app=0.054, walt=5.0, esc=0.02, bpi=0.4, mu=-0.005, bg=1.2, occ=0.93, bo=0.8, phi=0.15, capex=0.012, sm=0.04, m2m=0.00, drift=0),
    "DC":  dict(c_app=0.048, walt=8.0, esc=0.03, bpi=0.3, mu=0.010, bg=0.6, occ=0.95, bo=0.3, phi=0.20, capex=0.015, sm=0.05, m2m=0.08, drift=0),
    "HOT": dict(c_app=0.075, walt=0.05, esc=0.00, bpi=0.8, mu=-0.005, bg=2.5, occ=0.70, bo=3.0, phi=0.70, capex=0.040, sm=0.10, m2m=0.00, drift=0),
    "ALT": dict(c_app=0.053, walt=1.5, esc=0.01, bpi=0.6, mu=0.000, bg=1.0, occ=0.88, bo=0.8, phi=0.45, capex=0.015, sm=0.05, m2m=0.00, drift=0),
}
REGADJ = {"US": 0.0, "EU": 0.0025, "AS": 0.0, "GCC": 0.015}
BETA_Y, BETA_S = 0.45, 0.50
LIQ_ADD = [0.0, 0.0010, 0.0075, 0.0025]   # credit-availability cap-rate premium by regime (debt-flow channel) [I]
KAPPA_C, SIG_C = 0.15, 0.0012
NU_RHO, NU_SIG = 0.70, 0.06                # listed-market sentiment wedge (REIT-implied minus true value), quarterly [I]
NU_MEAN = [0.0, -0.02, -0.12, 0.03]        # wedge mean by regime [I]
G0 = {"OE": 0.05, "CE": 0.08, "JV": 0.06, "DIR": 0.06, "CO": 0.07}
ALPHA = {"OE": 0.55, "CE": 0.65, "JV": 0.65, "DIR": 0.70, "CO": 0.65}
LTVMAX = np.array([0.65, 0.60, 0.50, 0.60])
SPRD_ADD = np.array([0.0, 0.0025, 0.0150, 0.0050])
PEXT = np.array([0.35, 0.50, 0.50, 0.40])
DSCR_MIN = {"OE": 1.25, "CE": 1.20, "JV": 1.20, "DIR": 1.25, "CO": 1.20}
SPREAD = {"OE": 0.016, "CE": 0.025, "JV": 0.022, "DIR": 0.018, "CO": 0.025}


def mix(**kw):
    v = np.array([kw.get(s, 0.0) for s in SECT], dtype=float)
    return v / v.sum()


POS = [
    dict(id="SYN-RE-OE1", veh="OE", reg="US", nav=0.55, unf=0, mix=mix(LOG=35, RES=30, OFF=15, RET=10, ALT=10), ltv=0.27, fx=0.78, term=4.5, cpn=0.045, share=0.04),
    dict(id="SYN-RE-OE2", veh="OE", reg="US", nav=0.50, unf=0, mix=mix(LOG=30, RES=35, OFF=15, RET=10, ALT=10), ltv=0.26, fx=0.75, term=4.5, cpn=0.045, share=0.05),
    dict(id="SYN-RE-OE3", veh="OE", reg="US", nav=0.40, unf=0, mix=mix(LOG=40, RES=25, OFF=12, RET=13, ALT=10), ltv=0.29, fx=0.75, term=4.0, cpn=0.046, share=0.03),
    dict(id="SYN-RE-OE4", veh="OE", reg="US", nav=0.35, unf=0, mix=mix(LOG=30, RES=30, OFF=20, RET=10, ALT=10), ltv=0.28, fx=0.80, term=4.5, cpn=0.044, share=0.06),
    dict(id="SYN-RE-OE5", veh="OE", reg="EU", nav=0.35, unf=0, mix=mix(LOG=35, RES=30, OFF=25, RET=10), ltv=0.25, fx=0.70, term=4.0, cpn=0.035, share=0.07),
    dict(id="SYN-RE-OE6", veh="OE", reg="EU", nav=0.25, unf=0, mix=mix(LOG=30, RES=35, OFF=25, RET=10), ltv=0.24, fx=0.70, term=4.0, cpn=0.035, share=0.08),
    *[dict(id=f"SYN-RE-VA{i+1}", veh="CE", style="VA", reg=r, nav=n, unf=u, mix=m, ltv=0.55, fx=0.40, term=2.5, cpn=0.050, share=0.10, age=a)
      for i, (r, n, u, m, a) in enumerate([
          ("US", 0.30, 0.00, mix(OFF=35, RES=30, LOG=20, RET=15), 7), ("US", 0.25, 0.05, mix(RES=40, LOG=30, ALT=30), 5),
          ("US", 0.25, 0.15, mix(LOG=40, RES=30, OFF=10, ALT=20), 3), ("US", 0.20, 0.25, mix(RES=40, LOG=30, DC=10, ALT=20), 1),
          ("EU", 0.25, 0.05, mix(OFF=30, LOG=30, RES=30, RET=10), 5), ("EU", 0.20, 0.20, mix(LOG=40, RES=40, OFF=20), 2),
          ("US", 0.20, 0.10, mix(OFF=50, RES=25, RET=25), 6), ("AS", 0.15, 0.10, mix(LOG=50, RES=30, OFF=20), 3)])],
    *[dict(id=f"SYN-RE-OP{i+1}", veh="CE", style="OP", reg=r, nav=n, unf=u, mix=m, ltv=0.62, fx=0.30, term=2.0, cpn=0.055, share=0.08, age=a)
      for i, (r, n, u, m, a) in enumerate([
          ("US", 0.30, 0.00, mix(OFF=30, HOT=20, RES=25, RET=25), 8), ("US", 0.30, 0.20, mix(RES=30, LOG=20, DC=20, HOT=10, ALT=20), 3),
          ("EU", 0.25, 0.10, mix(OFF=35, HOT=20, RES=25, LOG=20), 5), ("AS", 0.25, 0.15, mix(OFF=30, RES=30, LOG=20, HOT=20), 4),
          ("US", 0.20, 0.20, mix(RES=35, LOG=25, ALT=40), 2), ("AS", 0.10, 0.05, mix(OFF=40, RET=30, HOT=30), 6)])],
    dict(id="SYN-RE-JV1", veh="JV", reg="US", nav=0.80, unf=0.05, mix=mix(LOG=100), ltv=0.40, fx=0.65, term=3.5, cpn=0.045, share=0.90),
    dict(id="SYN-RE-JV2", veh="JV", reg="US", nav=0.70, unf=0.05, mix=mix(RES=100), ltv=0.50, fx=0.55, term=3.0, cpn=0.047, share=0.85),
    dict(id="SYN-RE-JV3", veh="JV", reg="EU", nav=0.40, unf=0.05, mix=mix(RES=100), ltv=0.45, fx=0.70, term=4.0, cpn=0.036, share=0.80),
    dict(id="SYN-RE-JV4", veh="JV", reg="US", nav=0.50, unf=0.40, mix=mix(DC=100), ltv=0.45, fx=0.40, term=3.0, cpn=0.055, share=0.80, dev=True),
    dict(id="SYN-RE-JV5", veh="JV", reg="AS", nav=0.20, unf=0.05, mix=mix(LOG=100), ltv=0.40, fx=0.60, term=3.5, cpn=0.030, share=0.80),
    dict(id="SYN-RE-DIR1", veh="DIR", reg="GCC", nav=0.60, unf=0, mix=mix(OFF=50, RET=30, RES=20), ltv=0.35, fx=0.50, term=4.0, cpn=0.055, share=1.0),
    dict(id="SYN-RE-DIR2", veh="DIR", reg="GCC", nav=0.30, unf=0, mix=mix(HOT=100), ltv=0.40, fx=0.40, term=3.5, cpn=0.058, share=1.0),
    dict(id="SYN-RE-DIR3", veh="DIR", reg="EU", nav=0.30, unf=0, mix=mix(OFF=100), ltv=0.40, fx=0.80, term=5.0, cpn=0.040, share=1.0),
    dict(id="SYN-RE-CO1", veh="CO", reg="US", nav=0.20, unf=0, mix=mix(OFF=100), ltv=0.60, fx=0.30, term=1.5, cpn=0.060, share=1.0),
    dict(id="SYN-RE-CO2", veh="CO", reg="EU", nav=0.20, unf=0, mix=mix(LOG=100), ltv=0.50, fx=0.60, term=3.0, cpn=0.042, share=1.0),
    dict(id="SYN-RE-CO3", veh="CO", reg="US", nav=0.20, unf=0, mix=mix(ALT=100), ltv=0.60, fx=0.40, term=2.5, cpn=0.055, share=1.0),
]
# ---- Align sub-book totals with the G15 Real Assets synthetic book (g15_ra_results.json, 'book'): RE NAV $9.0bn =
# RE_OE 2.7, RE_CE 2.6 (unfunded 1.2), RE_DIR_GL 1.7 (0.2), RE_DIR_GCC 1.2 (0.2, LTV 0.45), RE_COI 0.8. ----
G15_NAV = {"RE_OE": 2.7, "RE_CE": 2.6, "RE_DIR_GL": 1.7, "RE_DIR_GCC": 1.2, "RE_COI": 0.8}
G15_UNF = {"RE_OE": 0.0, "RE_CE": 1.2, "RE_DIR_GL": 0.2, "RE_DIR_GCC": 0.2, "RE_COI": 0.0}


def g15_key(P):
    if P["veh"] == "OE":
        return "RE_OE"
    if P["veh"] == "CE":
        return "RE_CE"
    if P["veh"] == "CO":
        return "RE_COI"
    return "RE_DIR_GCC" if P["reg"] == "GCC" else "RE_DIR_GL"


for key in G15_NAV:
    grp = [P for P in POS if g15_key(P) == key]
    sn = G15_NAV[key] / sum(P["nav"] for P in grp)
    su = sum(P["unf"] for P in grp)
    for P in grp:
        P["nav"] = P["nav"] * sn
        if key == "RE_DIR_GCC":
            P["ltv"] = 0.45
            P["unf"] = G15_UNF[key] if P["id"] == "SYN-RE-DIR1" else 0.0
        elif su > 0:
            P["unf"] = P["unf"] * G15_UNF[key] / su
NAV0 = sum(p["nav"] for p in POS)
UNF0 = sum(p["unf"] for p in POS)
OE_NAV0 = sum(p["nav"] for p in POS if p["veh"] == "OE")


def own(P):
    """ADIC's fraction of the simulated vehicle economics. JV/DIR/CO are simulated at vehicle level."""
    return P["share"] if P["veh"] in ("JV", "DIR", "CO") else 1.0


PS = np.array([[0.90, 0.07, 0.02, 0.01], [0.05, 0.87, 0.06, 0.02], [0.00, 0.05, 0.75, 0.20], [0.20, 0.03, 0.02, 0.75]])
YBAR = np.array([4.25, 5.00, 3.50, 4.00]); FBAR = np.array([3.50, 4.25, 1.50, 2.75])
PIBAR = np.array([2.5, 3.8, 1.5, 2.3]); GBAR = np.array([0.5, 0.0, -3.0, 1.5]); SBAR = np.array([1.6, 2.0, 3.5, 2.2])

SCEN = {
    "base_mc": dict(force_S=None, desc="Markov regimes from LATE x GW x D (October 2026 state)"),
    "higher_for_longer": dict(force_S=[LATE] * 8, y_add=0.40, s_add=0.40, gw_q=4,
                              desc="10y held near 5.4%, spreads +40bp, LATE for 8 quarters; Gulf war ends after 4"),
    "demand_bust": dict(force_S=[LATE] + [CRIS] * 6 + [RECV] * 6, z_crisis=ZDB, s_add=0.8,
                        desc="Oil demand bust and recession: CRISIS 6 quarters, then RECOVERY 6"),
    "stagflation_gulf": dict(force_S=[LATE] * 8, y_add=1.0, pi_add=1.2, s_add=1.0, gw_q=8, gcc_extra=True,
                             desc="10y ~6%, CPI ~5%, spreads +100bp, Gulf war persists 8 quarters"),
    "benign": dict(force_S=[LATE] + [EXP] * 19, y_add=-0.6, s_add=-0.3, gw_q=1,
                   desc="Disinflation, 10y toward ~3.7%, Gulf war ends next quarter"),
    "credit_crunch": dict(force_S=[LATE] + [CRIS] * 6 + [RECV] * 6, z_crisis=ZDB, s_add=2.5, nu_add=-0.10,
                          desc="GFC-type: Baa spread toward ~6%, CRISIS 6 quarters, listed wedge -22%, then RECOVERY"),
}


def sim_factors(sc, rng):
    S = np.full((N, T + 1), LATE); Z = np.full((N, T + 1), ZGW)
    y = np.full((N, T + 1), 5.10); f = np.full((N, T + 1), 3.90); pi = np.full((N, T + 1), 3.70)
    g = np.zeros((N, T + 1)); s = np.full((N, T + 1), 2.00); nu = np.zeros((N, T + 1))
    gw_q, fs, zc = sc.get("gw_q"), sc.get("force_S"), sc.get("z_crisis")
    for t in range(T):
        u = rng.random(N); e = rng.standard_normal((N, 6)); u2 = rng.random(N); u3 = rng.random(N)
        if fs is not None and t < len(fs):
            S[:, t + 1] = fs[t]
        else:
            cp = np.cumsum(PS[S[:, t]], axis=1)
            S[:, t + 1] = np.minimum((u[:, None] > cp).sum(axis=1), 3)
        if gw_q is not None:
            Z[:, t + 1] = np.where(t + 1 <= gw_q, ZGW, ZN)
        else:
            Z[:, t + 1] = np.where((Z[:, t] == ZGW) & (u2 < 0.75), ZGW, ZN)
        if zc is not None:
            Z[:, t + 1] = np.where(S[:, t + 1] == CRIS, zc, Z[:, t + 1])
        else:
            enter = (S[:, t + 1] == CRIS) & (S[:, t] != CRIS)
            Z[:, t + 1] = np.where((enter & (u3 < 0.30)) | ((Z[:, t] == ZDB) & (S[:, t + 1] == CRIS)), ZDB, Z[:, t + 1])
        St = S[:, t + 1]
        inside = fs is None or t < len(fs)
        ya = sc.get("y_add", 0.0) if inside else 0.0
        pa = sc.get("pi_add", 0.0) if inside else 0.0
        sa = sc.get("s_add", 0.0) if inside else 0.0
        y[:, t + 1] = y[:, t] + 0.15 * (YBAR[St] + ya - y[:, t]) + 0.22 * e[:, 0]
        f[:, t + 1] = np.maximum(0.0, f[:, t] + 0.30 * (FBAR[St] + 0.5 * ya - f[:, t]) + 0.15 * e[:, 1])
        pi[:, t + 1] = pi[:, t] + 0.25 * (PIBAR[St] + pa + 0.8 * (Z[:, t + 1] == ZGW) - pi[:, t]) + 0.35 * e[:, 2]
        g[:, t + 1] = g[:, t] + 0.40 * (GBAR[St] - g[:, t]) + 0.60 * e[:, 3]
        s[:, t + 1] = np.maximum(0.8, s[:, t] + 0.30 * (SBAR[St] + sa - s[:, t]) + 0.15 * e[:, 4])
        na = sc.get("nu_add", 0.0) if inside else 0.0
        nu[:, t + 1] = (np.array(NU_MEAN)[St] + na) + NU_RHO * (nu[:, t] - (np.array(NU_MEAN)[St] + na)) + NU_SIG * e[:, 5]
    eRE = np.where(S == CRIS, eF, np.where(((S == LATE) & (y > 4.75)) | (Z == ZGW), eD, np.where(s < 1.6, eO, eN)))
    eRE[:, 0] = eD
    return dict(S=S, Z=Z, y=y / 100, f=f / 100, pi=pi / 100, g=g / 100, s=s / 100, eRE=eRE, nu=nu)


def property_engine(k, r, veh, F, rng, sc):
    p = SP[k]
    c_app = p["c_app"] + REGADJ[r]
    VT0 = np.exp(-G0[veh]); noi0 = c_app; c0 = noi0 / VT0
    O = np.full(N, p["occ"]); GR = noi0 / (1 - p["phi"]); E = p["phi"] * GR; R = GR / O; M = R * (1 + p["m2m"])
    rho = min(1.0, 0.25 / p["walt"]); c = np.full(N, c0)
    VT = np.zeros((N, T + 1)); VT[:, 0] = VT0
    NOI = np.zeros((N, T + 1)); NOI[:, 0] = noi0
    CAPX = np.zeros((N, T + 1))
    y, s, pi, g, Z = F["y"], F["s"], F["pi"], F["g"], F["Z"]
    gcc = r == "GCC"
    for t in range(T):
        e = rng.standard_normal((N, 3))
        M = M * np.exp((p["mu"] + p["bpi"] * pi[:, t + 1] + p["bg"] * g[:, t + 1]) / 4 + p["sm"] / 2 * e[:, 0])
        R = R * (1 + p["esc"] / 4) + rho * (M - R * (1 + p["esc"] / 4))
        O = np.clip(O + 0.15 * (p["occ"] + p["bo"] * g[:, t + 1] - O) + 0.005 * e[:, 1], 0.40, 0.99)
        E = E * (1 + pi[:, t + 1] / 4)
        noi = R * O - E
        if gcc:
            hit = {"HOT": 0.25, "RET": 0.10, "OFF": 0.06}.get(k, 0.04) * (1.6 if sc.get("gcc_extra") else 1.0)
            noi = noi * (1 - np.where(Z[:, t + 1] == ZGW, hit, np.where(Z[:, t + 1] == ZDB, 1.5 * hit + 0.05, 0.0)))
        noi = np.maximum(noi, 0.1 * noi0)
        cstar = (c0 + BETA_Y * (y[:, t + 1] - 0.051) + BETA_S * (s[:, t + 1] - 0.020) + p["drift"] / 1e4 * (t + 1) / 4
                 + np.array(LIQ_ADD)[F["S"][:, t + 1]] - LIQ_ADD[LATE])
        if gcc:
            cstar = cstar + np.where(Z[:, t + 1] == ZGW, 0.0075, np.where(Z[:, t + 1] == ZDB, 0.015, 0.0))
        c = np.maximum(0.025, c + KAPPA_C * (cstar - c) + SIG_C * e[:, 2])
        gfwd = 0.5 * (p["mu"] + p["bpi"] * pi[:, t + 1])
        VT[:, t + 1] = noi * (1 + gfwd) / c
        NOI[:, t + 1] = noi
        CAPX[:, t + 1] = p["capex"] / 4 * VT[:, t + 1]
    return VT, NOI, CAPX


def appraise(VT, veh, rng):
    a = ALPHA[veh]
    VA = np.zeros_like(VT); VA[:, 0] = 1.0
    for t in range(T):
        VA[:, t + 1] = np.exp(a * np.log(VA[:, t]) + (1 - a) * np.log(VT[:, t]) + 0.004 * rng.standard_normal(N))
    return VA


CE_CALL = np.array([0.25, 0.30, 0.35, 0.40]); MC = np.array([1.2, 1.0, 0.75, 0.6])
MD = np.array([1.3, 1.0, 0.45, 0.25]); KAP = np.array([1.2, 1.0, 0.6, 0.5])
DISP_OE = np.array([0.010, 0.006, 0.004, 0.002])


def exit_rate(age_e):
    return np.select([age_e < 3, age_e < 5, age_e < 7, age_e < 9], [0.03, 0.12, 0.22, 0.30], 0.35)


def simulate(sc_name):
    sc = SCEN[sc_name]
    rng = np.random.default_rng(SEED)        # common random numbers across scenarios (same seed)
    F = sim_factors(sc, rng)
    S, eRE = F["S"], F["eRE"]
    cache = {}
    keys = ["navA", "navT", "debt", "gavA", "gavT", "inc", "dist", "call", "cure", "short", "dev", "lost", "gap",
            "mature", "noi", "hbdebt"]
    o = {k: np.zeros((N, T + 1)) for k in keys}
    oeq = np.zeros((N, T + 1)); adic_red = np.zeros((N, T + 1)); handback_any = np.zeros(N, dtype=bool)
    ss_num = np.zeros((N, T + 1)); ss_den = 0.0               # same-store NOI index (NAV-weighted, no acquisitions)
    for P in POS:
        veh, reg, w_own = P["veh"], P["reg"], own(P)
        VTp = np.zeros((N, T + 1)); VAp = np.zeros((N, T + 1)); NOIp = np.zeros((N, T + 1)); CXp = np.zeros((N, T + 1))
        for j, k in enumerate(SECT):
            w = P["mix"][j]
            if w == 0:
                continue
            key = (k, reg, veh)
            if key not in cache:
                VT, NOI, CX = property_engine(k, reg, veh, F, rng, sc)
                cache[key] = (VT, appraise(VT, veh, rng), NOI, CX)
            VT, VA, NOI, CX = cache[key]
            VTp += w * VT; VAp += w * VA; NOIp += w * NOI; CXp += w * CX
        idio = np.exp(np.cumsum(np.concatenate([np.zeros((N, 1)), 0.02 * rng.standard_normal((N, T))], axis=1), axis=1))
        VTp *= idio; NOIp *= idio; CXp *= idio
        ss_num += P["nav"] * NOIp / NOIp[:, :1]; ss_den += P["nav"]
        gav0 = P["nav"] / w_own / (1 - P["ltv"])            # vehicle (or ADIC look-through) appraised GAV
        units = np.full(N, gav0)
        D_fix = np.full(N, P["ltv"] * gav0 * P["fx"]); D_flt = np.full(N, P["ltv"] * gav0 * (1 - P["fx"]))
        cpn_fix = P["cpn"]; D_new = np.zeros(N); cpn_new = np.zeros(N)
        nq = max(1, int(round(2 * P["term"] * 4)))
        haz = np.array([1.0 / (nq - q + 1) if q <= nq else 0.0 for q in range(T + 1)])  # share of remaining legacy maturing
        ext_due = np.zeros((N, T + 6))
        U = np.full(N, float(P["unf"])); age_e = np.full(N, float(P.get("age", 0)))
        # OE queues (others' requests, share of fund NAV): start from today's standing queue. ODCE was "just above 10%"
        # in Q1-2026 (Accordant) and the replay gives 6.8% for Q3-2026; use 8% (US) and 5% (Europe) [I].
        q0 = 0.08 if reg == "US" else 0.05
        Qh = np.full(N, q0); Qr = np.full(N, q0); Qadic = np.ones(N)   # HOLD world and ADIC-redeems world
        for t in range(T):
            St = S[:, t + 1]; et = eRE[:, t + 1]
            noi = units * NOIp[:, t + 1]; capex = units * CXp[:, t + 1]
            gavT = units * VTp[:, t + 1]
            r_flt = F["f"][:, t + 1] + SPREAD[veh]
            interest = (D_fix * cpn_fix + D_flt * r_flt + D_new * cpn_new) / 4
            # ---- maturities: legacy hazard plus extended loans falling due ----
            M_leg = (D_fix + D_flt) * haz[t + 1]
            M_ext = np.minimum(ext_due[:, t + 1], D_new)
            M_amt = M_leg + M_ext
            Dtot = D_fix + D_flt + D_new
            mat_frac = np.clip(M_amt / np.maximum(Dtot, 1e-12), 0, 1)
            r_new = F["y"][:, t + 1] + SPREAD[veh] + SPRD_ADD[St]
            cap = np.minimum(LTVMAX[St] * gavT, noi / (DSCR_MIN[veh] * r_new))
            gapamt = np.maximum(0.0, M_amt - mat_frac * cap)
            has_gap = gapamt > 1e-9
            ext = has_gap & (M_ext <= 1e-12) & (rng.random(N) < PEXT[St])
            paydown = np.where(ext, 0.05 * M_amt, 0.0)
            eq_after = gavT - (Dtot - gapamt)
            cure = has_gap & ~ext & (eq_after > 1.1 * gapamt)
            hand = has_gap & ~ext & ~cure
            handback_any |= hand
            cure_amt = np.where(cure, gapamt, 0.0) + paydown
            lost = np.where(hand, np.maximum(mat_frac * (gavT - Dtot), 0.0), 0.0)
            units = np.where(hand, units * (1 - mat_frac), units)
            # remove maturing pieces
            fr_leg = np.where(D_fix + D_flt > 0, M_leg / np.maximum(D_fix + D_flt, 1e-12), 0.0)
            D_fix = D_fix * (1 - fr_leg); D_flt = D_flt * (1 - fr_leg); D_new = D_new - M_ext
            # refinance the non-defaulted remainder into new fixed debt (extensions at +25bp)
            add = np.where(hand, 0.0, M_amt - np.where(cure, gapamt, 0.0) - paydown)
            rate_add = r_new + np.where(ext, 0.0025, 0.0)
            cpn_new = np.where(D_new + add > 0, (D_new * cpn_new + add * rate_add) / np.maximum(D_new + add, 1e-12), cpn_new)
            D_new = D_new + add
            ext_due[:, t + 5] += np.where(ext, add, 0.0)
            Dtot = D_fix + D_flt + D_new
            cfe = noi / 4 - capex - interest
            short = np.maximum(-cfe, 0.0)                     # operating/debt-service shortfall to be funded
            if veh in ("JV", "DIR", "CO"):
                dscr_ok = noi / np.maximum(4 * interest, 1e-12) >= 1.10
                dist = np.where(dscr_ok, np.maximum(cfe, 0.0), 0.0)
                trapped = np.where(dscr_ok, 0.0, np.maximum(cfe, 0.0))
                D_new = np.maximum(0.0, D_new - trapped)
                o["inc"][:, t + 1] += w_own * dist
                o["cure"][:, t + 1] += w_own * cure_amt
                o["short"][:, t + 1] += w_own * short
                if veh == "CO":
                    # co-investment exits on the sponsor's clock: 12%/yr of NAV in N, scaled by eRE (G15: 12% / 4%)
                    xco = 1 - np.exp(-0.12 * MD[et] / 4)
                    eqT = np.maximum(units * VTp[:, t + 1] - (D_fix + D_flt + D_new), 0.0)
                    o["dist"][:, t + 1] += w_own * xco * eqT
                    units = units * (1 - xco); D_fix = D_fix * (1 - xco); D_flt = D_flt * (1 - xco); D_new = D_new * (1 - xco)
                if P.get("dev"):
                    base = np.minimum(U, P["unf"] / 8.0)
                    draw = base * np.where(St == CRIS, 1.15, 1.0)          # cost overrun in crisis [I]
                    U = U - base
                    units = units + base / np.maximum(VTp[:, t + 1], 1e-9) * 1.25   # yield-on-cost premium [I]
                    o["dev"][:, t + 1] += w_own * draw
                elif P["unf"] > 0:
                    base = (1 - np.exp(-0.20 / 4)) * U                   # capex / add-on commitments, 20%/yr [I]
                    U = U - base
                    units = units + base / np.maximum(VTp[:, t + 1], 1e-9)
                    o["dev"][:, t + 1] += w_own * base
            elif veh == "OE":
                gavA = units * VAp[:, t + 1]
                navA_pos = np.maximum(gavA - Dtot, 1e-9)
                fee = 0.0085 / 4 * navA_pos
                # Distributions on the income-return basis (before capex), as ODCE funds pay (~3% of NAV); capex is
                # funded at fund level by borrowing, so fund leverage drifts up (ODCE: 22.4% average -> 27.1%) [I]
                income = np.maximum(noi / 4 - interest - fee, 0.0)
                o["inc"][:, t + 1] += 0.90 * income
                D_new = np.maximum(0.0, D_new - 0.10 * income + capex + np.minimum(cfe, 0.0) * 0.0)
                # perceived stale-NAV premium: appraisal over the REIT-implied (market) value = true value x exp(nu)
                gapA = (np.log(np.maximum(VAp[:, t + 1], 1e-9)) - np.log(np.maximum(VTp[:, t + 1], 1e-9))
                        - F["nu"][:, t + 1] + 0.02 * rng.standard_normal(N))
                req = 0.006 + 0.12 * np.maximum(0.0, gapA)
                contrib = lambda Q: np.where((gapA > 0.03) | (Q > 0.05), 0.004, 0.012)
                short_oe = np.maximum(-(noi / 4 - interest), 0.0)        # capex is debt-funded in OE funds
                L = lambda Q: np.maximum(0.0, 0.0025 + DISP_OE[et] * gavA / navA_pos + contrib(Q)
                                         - (cure_amt + short_oe) / navA_pos)
                # HOLD world (others only)
                Qh = np.maximum(0.0, Qh + req - np.where(gapA <= 0.03, 0.08 * Qh, 0.0))
                Qh = Qh - np.minimum(Qh, L(Qh))
                oeq[:, t + 1] += Qh * P["nav"]
                # ADIC-redeems world: ADIC's full request (share of fund NAV) joins the queue pro rata at t0
                sh = P["share"]
                Qr = np.maximum(0.0, Qr + req - np.where(gapA <= 0.03, 0.08 * Qr, 0.0))
                tot = Qr + sh * Qadic
                pay = np.minimum(tot, L(tot))
                frac = np.where(tot > 0, pay / np.maximum(tot, 1e-12), 0.0)
                adic_paid = np.minimum(Qadic, frac * Qadic)
                Qadic = Qadic - adic_paid
                Qr = Qr * (1 - frac)
                adic_red[:, t + 1] += adic_paid * P["nav"]
            else:  # closed-end fund interest
                a_b = np.clip(age_e.astype(int), 0, 3)
                call = (1 - np.exp(-CE_CALL[a_b] * MC[et] / 4)) * U
                U = U - call
                units = units + call / (1 - P["ltv"]) / np.maximum(VTp[:, t + 1], 1e-9)
                add2 = call * P["ltv"] / (1 - P["ltv"])
                cpn_new = np.where(D_new + add2 > 0, (D_new * cpn_new + add2 * r_new) / np.maximum(D_new + add2, 1e-12), cpn_new)
                D_new = D_new + add2
                Dtot = D_fix + D_flt + D_new
                gavT = units * VTp[:, t + 1]; gavA = units * VAp[:, t + 1]
                navT_pos = np.maximum(gavT - Dtot, 0.0); navA_pos = np.maximum(gavA - Dtot, 0.0)
                x = 1 - np.exp(-exit_rate(age_e) * MD[et] / 4)
                proceeds = x * navT_pos
                fee = 0.015 / 4 * navA_pos
                inc = 0.8 * np.maximum(cfe - fee, 0.0)
                D_new = np.maximum(0.0, D_new - 0.2 * np.maximum(cfe - fee, 0.0))
                units = units * (1 - x); D_fix = D_fix * (1 - x); D_flt = D_flt * (1 - x); D_new = D_new * (1 - x)
                need = cure_amt + short + np.maximum(fee - np.maximum(cfe, 0.0), 0.0)
                lp_call = np.minimum(U, need)                 # funded from unfunded commitments first
                U = U - lp_call
                fund_borrow = need - lp_call                  # remainder: fund-level borrowing or reduced distributions
                take = np.minimum(fund_borrow, proceeds + inc)
                D_new = D_new + (fund_borrow - take)
                o["dist"][:, t + 1] += proceeds + inc - take
                o["call"][:, t + 1] += call + lp_call
                age_e = age_e + KAP[et] / 4
            Dtot = D_fix + D_flt + D_new
            gavT = units * VTp[:, t + 1]; gavA = units * VAp[:, t + 1]
            o["navT"][:, t + 1] += w_own * np.maximum(gavT - Dtot, 0.0)
            o["navA"][:, t + 1] += w_own * np.maximum(gavA - Dtot, 0.0)
            o["debt"][:, t + 1] += w_own * Dtot
            o["gavA"][:, t + 1] += w_own * gavA
            o["gavT"][:, t + 1] += w_own * gavT
            o["gap"][:, t + 1] += w_own * gapamt
            o["mature"][:, t + 1] += w_own * M_amt
            o["lost"][:, t + 1] += w_own * lost
            o["noi"][:, t + 1] += w_own * noi
            o["hbdebt"][:, t + 1] += w_own * np.where(hand, M_amt, 0.0)
        o["navA"][:, 0] += P["nav"]
        o["navT"][:, 0] += w_own * (gav0 * np.exp(-G0[veh]) - P["ltv"] * gav0)
        o["debt"][:, 0] += w_own * P["ltv"] * gav0
        o["gavA"][:, 0] += w_own * gav0
        o["gavT"][:, 0] += w_own * gav0 * np.exp(-G0[veh])
        o["noi"][:, 0] += w_own * gav0 * float(np.dot(P["mix"], [SP[k]["c_app"] for k in SECT]))
    o["ss_noi"] = ss_num / ss_den
    return F, o, oeq, adic_red, handback_any


def q(x, p):
    return float(np.percentile(x, p))


def pct3(x, nd=3):
    return [round(q(x, 5), nd), round(q(x, 50), nd), round(q(x, 95), nd)]


results = {"label": "SYNTHETIC - NOT ADIC DATA. Prototype real-estate engine, G10 stream, run 2026-10-18.",
           "n_paths": N, "quarters": T, "seed": SEED, "nav0_bn": round(NAV0, 2), "unfunded0_bn": round(UNF0, 2),
           "positions": len(POS), "scenarios": {}}
for name in SCEN:
    F, o, oeq, adic_red, hb = simulate(name)
    yr = lambda arr, a, b: arr[:, a:b].sum(axis=1)
    cin1 = yr(o["inc"], 1, 5) + yr(o["dist"], 1, 5)
    cout1 = yr(o["call"], 1, 5) + yr(o["cure"], 1, 5) + yr(o["short"], 1, 5) + yr(o["dev"], 1, 5)
    cin2 = yr(o["inc"], 5, 9) + yr(o["dist"], 5, 9)
    cout2 = yr(o["call"], 5, 9) + yr(o["cure"], 5, 9) + yr(o["short"], 5, 9) + yr(o["dev"], 5, 9)
    navA, navT = o["navA"], o["navT"]
    ddT = navT[:, :13].min(axis=1) / navT[:, 0] - 1
    ddA = navA[:, :13].min(axis=1) / navA[:, 0] - 1
    gapNAV = np.log(navA[:, 1:] / np.maximum(navT[:, 1:], 1e-9))
    sel = (navT[:, 1:13].min(axis=1) / navT[:, 0] - 1) < -0.10
    lags = []
    for pth in np.where(sel)[0][:3000]:
        tT = int(np.argmin(navT[pth, :]))
        tA = int(np.argmin(navA[pth, :]))
        lags.append(tA - tT)                     # trough-to-trough lag of reported vs true NAV (quarters)
    lev_A = o["debt"][:, 1:13] / np.maximum(o["gavA"][:, 1:13], 1e-9)
    lev_T = o["debt"][:, 1:13] / np.maximum(o["gavT"][:, 1:13], 1e-9)
    mat24 = yr(o["mature"], 1, 9); gap24 = yr(o["gap"], 1, 9)
    noi_g = o["ss_noi"][:, 8] ** 0.5 - 1          # same-store NOI growth, annualised over 2 years
    res = {
        "desc": SCEN[name]["desc"],
        "factor_medians_q4_q8": {"y10_pct": [round(100 * q(F["y"][:, 4], 50), 2), round(100 * q(F["y"][:, 8], 50), 2)],
                                 "baa_spread_pct": [round(100 * q(F["s"][:, 4], 50), 2), round(100 * q(F["s"][:, 8], 50), 2)],
                                 "cpi_pct": [round(100 * q(F["pi"][:, 4], 50), 2), round(100 * q(F["pi"][:, 8], 50), 2)],
                                 "share_crisis_by_q8": round(float((F["S"][:, 1:9] == CRIS).any(axis=1).mean()), 3),
                                 "share_eRE_drought_or_frozen_q4": round(float((F["eRE"][:, 4] >= eD).mean()), 3)},
        "cash_y1_bn": {"in": pct3(cin1), "out": pct3(cout1), "net": pct3(cin1 - cout1)},
        "cash_y2_bn": {"in": pct3(cin2), "out": pct3(cout2), "net": pct3(cin2 - cout2)},
        "p_net_cash_negative": [round(float((cin1 - cout1 < 0).mean()), 3), round(float((cin2 - cout2 < 0).mean()), 3)],
        "components_y1_median_bn": {k: round(q(yr(o[k], 1, 5), 50), 3) for k in ["inc", "dist", "call", "cure", "short", "dev"]},
        "noi_growth_2y_annualised_pct": pct3(100 * noi_g, 2),
        "nav_reported_end_y1_y2_y3_bn": [pct3(navA[:, 4]), pct3(navA[:, 8]), pct3(navA[:, 12])],
        "nav_true_end_y1_y2_y3_bn": [pct3(navT[:, 4]), pct3(navT[:, 8]), pct3(navT[:, 12])],
        "max_dd_3y_true_pct_P5_P50": [round(100 * q(ddT, 5), 1), round(100 * q(ddT, 50), 1)],
        "max_dd_3y_reported_pct_P5_P50": [round(100 * q(ddA, 5), 1), round(100 * q(ddA, 50), 1)],
        "p_true_dd_gt_15pct_3y": round(float((ddT < -0.15).mean()), 3),
        "p_reported_dd_gt_15pct_3y": round(float((ddA < -0.15).mean()), 3),
        "stale_gap_ln_navA_over_navT_q4_pct": pct3(100 * gapNAV[:, 3], 1),
        "trough_lag_reported_vs_true_q_median": (float(np.median(lags)) if lags else None),
        "share_paths_true_dd_gt_10pct": round(float(sel.mean()), 3),
        "refi_gap_share_of_maturing_24m_pct_P50": round(100 * q(gap24 / np.maximum(mat24, 1e-9), 50), 1),
        "lookthrough_ltv_appraised_q1_pct": round(100 * q(lev_A[:, 0], 50), 1),
        "lookthrough_ltv_true_peak_3y_P50_P95_pct": [round(100 * q(lev_T.max(axis=1), 50), 1), round(100 * q(lev_T.max(axis=1), 95), 1)],
        "debt_maturing_24m_bn": pct3(mat24),
        "refi_gap_24m_bn": pct3(gap24),
        "p_any_handback_5y": round(float(hb.mean()), 3),
        "handback_debt_share_of_initial_debt_5y_pct": pct3(100 * o["hbdebt"].sum(axis=1) / o["debt"][:, 0], 2),
        "nav_total_return_3y_ann_pct": {
            "true": pct3(100 * (((navT[:, 12] + yr(o["inc"], 1, 13) + yr(o["dist"], 1, 13) - yr(o["call"], 1, 13)
                                  - yr(o["cure"], 1, 13) - yr(o["short"], 1, 13) - yr(o["dev"], 1, 13))
                                 / navT[:, 0]) ** (1 / 3) - 1), 2),
            "reported": pct3(100 * (((navA[:, 12] + yr(o["inc"], 1, 13) + yr(o["dist"], 1, 13) - yr(o["call"], 1, 13)
                                      - yr(o["cure"], 1, 13) - yr(o["short"], 1, 13) - yr(o["dev"], 1, 13))
                                     / navA[:, 0]) ** (1 / 3) - 1), 2)},
        "equity_lost_handback_5y_bn": pct3(o["lost"].sum(axis=1)),
        "oe_queue_peak_pct_nav_P50_P95": [round(100 * q((oeq[:, 1:] / OE_NAV0).max(axis=1), 50), 1),
                                          round(100 * q((oeq[:, 1:] / OE_NAV0).max(axis=1), 95), 1)],
        "adic_full_oe_redemption_cum_paid_share_P5_P50": {
            f"q{h}": [round(q(adic_red[:, 1:h + 1].sum(axis=1) / OE_NAV0, 5), 3),
                      round(q(adic_red[:, 1:h + 1].sum(axis=1) / OE_NAV0, 50), 3)] for h in (4, 8, 12, 20)},
    }
    results["scenarios"][name] = res
    print(f"== {name}")
    for k in ("cash_y1_bn", "cash_y2_bn", "components_y1_median_bn", "max_dd_3y_true_pct_P5_P50",
              "max_dd_3y_reported_pct_P5_P50", "trough_lag_reported_vs_true_q_median", "share_paths_true_dd_gt_10pct",
              "debt_maturing_24m_bn", "refi_gap_24m_bn", "refi_gap_share_of_maturing_24m_pct_P50",
              "p_true_dd_gt_15pct_3y", "p_reported_dd_gt_15pct_3y", "lookthrough_ltv_true_peak_3y_P50_P95_pct",
              "oe_queue_peak_pct_nav_P50_P95", "adic_full_oe_redemption_cum_paid_share_P5_P50", "p_any_handback_5y",
              "handback_debt_share_of_initial_debt_5y_pct", "nav_total_return_3y_ann_pct", "lookthrough_ltv_appraised_q1_pct",
              "noi_growth_2y_annualised_pct", "stale_gap_ln_navA_over_navT_q4_pct", "factor_medians_q4_q8"):
        print(" ", k, json.dumps(res[k]))

comp = {"by_vehicle_nav_bn": {}, "by_region_nav_bn": {}, "by_sector_nav_bn": {}, "by_g15_subbook_nav_bn": {}}
for P in POS:
    comp["by_g15_subbook_nav_bn"][g15_key(P)] = round(comp["by_g15_subbook_nav_bn"].get(g15_key(P), 0) + P["nav"], 3)
    comp["by_vehicle_nav_bn"][P["veh"]] = round(comp["by_vehicle_nav_bn"].get(P["veh"], 0) + P["nav"], 3)
    comp["by_region_nav_bn"][P["reg"]] = round(comp["by_region_nav_bn"].get(P["reg"], 0) + P["nav"], 3)
    for j, k in enumerate(SECT):
        comp["by_sector_nav_bn"][k] = round(comp["by_sector_nav_bn"].get(k, 0) + P["nav"] * P["mix"][j], 3)
gav_lt = sum(P["nav"] / (1 - P["ltv"]) for P in POS)
debt_lt = sum(P["ltv"] * P["nav"] / (1 - P["ltv"]) for P in POS)
comp["lookthrough_gav_adic_share_bn"] = round(gav_lt, 2)
comp["lookthrough_debt_adic_share_bn"] = round(debt_lt, 2)
comp["lookthrough_ltv_pct"] = round(100 * debt_lt / gav_lt, 1)
comp["unfunded_by_vehicle_bn"] = {v: round(sum(P["unf"] for P in POS if P["veh"] == v), 3) for v in ("CE", "JV", "DIR")}
comp["positions"] = [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in P.items() if k != "mix"}
                     | {"mix": dict(zip(SECT, [round(float(x), 3) for x in P["mix"]]))} for P in POS]
results["composition"] = comp
print(json.dumps(comp, indent=1))
with open(f"{CALC}/g10_re_engine_results.json", "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=1)
