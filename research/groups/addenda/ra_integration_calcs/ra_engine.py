"""
ra_integration_calcs COPY of ra_gap_01's ra_engine.py (original untouched). Adaptations, all marked "ri:":
  * t1_engine is loaded from the local byte-identical copy in this folder;
  * book 'v1s' (seven groups, PE 52 / 16.4 = census v1.1, the user's choice) uses the sealed census v1.1 vintage
    profile in cohort mode, like the v2 books (the original fell back to gap_04's U 27.4 history rescaled);
  * Cfg.ra_oil_enr / Cfg.ra_oil_gcc switch the Real Assets oil channels (ENR oil elasticity and oil-elastic
    income / exits; GCC fiscal drag, income and exit links) for the oil-sensitivity runs. Defaults (True) give
    the ra_gap_01 engine exactly.

ra_gap_01: integrated EIGHT-group + Corporate Finance + overlay prototype on SYN-ADIC-177 (allocation v2).

A copy of groups gap_04's g04_engine.py (research/groups/addenda/gap_04_calcs/, left untouched), extended with:
  book       'v1' (as gap_04) or 'v2u16' / 'v2u11' (PE $34bn with $16.4bn or $10.9bn unfunded from the sealed
             census v1.1 vintage profile; Real Assets $18bn / $4.0bn; plan pacing 50/10/10/10/10/10 incl. RA)
  RA module  ra_module.RAState: ten census sleeves, true / reported (RAME) / nowcast values, asset-level debt with
             lender availability and cures (varpi = 1), the fund-level refinancing module, the open-end queue
             machine, oil and GCC links; drawn from a dedicated RNG stream (seed + 505) so CRN holds elsewhere
  RA player  the tenth Shapley player: pacing corridor, open-end notices at Amber, pre-arranged JV sell-downs
             (controlled holdings), cash-out at maturity (controlled, Green/Amber), the t0 ENR SELL.
             Group-off baseline: HOLD + plan pacing, no notices / sell-downs / cash-outs / ENR SELL; cures paid
  proxy      the CFP survival proxy carries the theta-indexed RA leg at the recalibrated theta (cfg.theta)
  gstar      the rate-mode action-free G* replica carries RA flows and RA NAV (theta* recalibration)
With book='v1' and no RA it reproduces g04_engine (and Cfg.t1() reproduces t1_engine.simulate) path for path.

SYNTHETIC - NOT ADIC DATA. Every balance, rate and outcome here is a design default or a synthetic draw.

What it is
  An extension of gap_02's quarterly Monte Carlo (research/addenda/gap_02_calcs/t1_engine.py, imported
  UNMODIFIED). With every extension switched off (Cfg.t1()), `simulate` reproduces t1_engine.simulate path for
  path (same RNG streams); every new random draw comes from separate streams so that switching an extension on
  or off keeps common random numbers for everything else.

Extensions (each a switch in Cfg)
  init='gap04'     October-2026 initial state of research/addenda/gap_04.md s6: exit window e0 ~ (N .08, D .874,
                   F .046); shock type Z0 ~ (N .03, DB .02, SS .10, GW .85); market calm; Q4-2026 draw at
                   d_2026 = 5.8%, 2027 draws from gap_04's reduced form (oil start $105 + IMF fusion).
  groups='cohort'  cohort-level versions of the groups-synthesis s3 engines: PE vintages (RFT-TA call schedule,
                   TA-style distributions on age), Secondaries (S1 funds / LP interests / CVs / contingent
                   purchases), Capital Solutions (cash-pay and PIK-capable claims, PD/LGD, PIK switch,
                   wrong-way repayments), Co-investment (90 companies on an EV engine with Weibull exits, recaps,
                   write-offs; new deals in yearly cohorts), Private Credit (SMA/CEF/evergreen/BDC wrappers, CPR,
                   PIK, defaults, DDTL draws).
  links=True       s4.7 lagged co-investment flow O_t = theta*sum d_k C_(t-k) from simulated PE commitments;
                   GP effects drawn once per path and SHARED by PE funds and co-investments (rho_GP ~0.6);
                   company overlap with Private Credit: recap netting and shared default draws.
  overlay='L1'     Level-1 templates (gap_03 s4): 12-month equity and Brent put-spread ladders priced on
                   regime vols with skew, market-based monetization; opportunistic families as factor exposures
                   (trend, carry, RV, short vol) with the L1 vega floor; synthetic beta split into TPA and P2S.
  stage='cfp'      the groups-synthesis s2.4 CFP stage machine (SH_TP under T4' = s*(0.76), ADIC-LCR(30d),
                   Treasury/NAV, liquid share; hysteresis) instead of t1's three-indicator stage.
  players          which of the nine players (7 groups + TPA + CF) run their discretionary policy; the
                   others run the group-off baseline: HOLD plus plan pacing.
  trigger          contingent budgets of Secondaries and Capital Solutions: 'none', 'current' (discount > 20%
                   AND Tier 1 green AND stage <= Amber), 'tier1only' (discount > 20% AND Tier 1 green, any stage
                   but Black), 'ring50' / 'ring100' (a ring-fenced account fed by 50% / 100% of tail-hedge cash,
                   deployable at discount > 20% in any stage but Black), 'ring_t1' (ring100 AND Tier 1 green),
                   'ungated' (discount > 20% only). Deployment under 'current'/'tier1only' is capped at usable
                   IG + cash above 8% of NAV; ring-fenced cash is excluded from the waterfall for four quarters.
  stage_conv       CFP indicators on gross Treasury ('gross') or net of drawn facilities ('net').
  gp_new           switches the new group playbooks (PC run-off, co-investment pause, overlay monetization and
                   de-risking, TPA beta rule) independently of the player flags, for the bridge.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import brentq, least_squares
from scipy.special import ndtr

HERE = os.path.dirname(os.path.abspath(__file__))
_T1 = os.path.join(HERE, "t1_engine.py")   # ra_integration_calcs: local byte-identical copy of gap_02's engine
_spec = importlib.util.spec_from_file_location("t1_engine", _T1)
E = importlib.util.module_from_spec(_spec)
sys.modules["t1_engine"] = E
_spec.loader.exec_module(E)  # unmodified gap_02 engine
sys.path.insert(0, HERE)
import ra_book as RB  # noqa: E402
import ra_module as RM  # noqa: E402

PLAYERS9 = ("PE", "SEC", "CS", "CO", "PM", "PC", "OVL", "TPA", "CF")
PLAYERS = PLAYERS9 + ("RA",)
GKEYS = ("pe", "sec", "co", "cs", "pc")
OWNER = {"pe": "PE", "sec": "SEC", "co": "CO", "cs": "CS", "pc": "PC", "ra": "RA"}
SHARE_V1 = {"pe": 0.6, "sec": 0.1, "pc": 0.1, "cs": 0.1, "co": 0.1}
SHARE_V2 = {"pe": 0.5, "sec": 0.1, "pc": 0.1, "cs": 0.1, "co": 0.1, "ra": 0.1}
SHARE = SHARE_V1
ACC = ("PE", "SEC", "CS", "CO", "PC", "PM", "OVL", "TPA", "CF", "RA")
BETA_G = {"PE": 1.1, "SEC": 0.9, "CS": 0.5, "CO": 1.3, "PC": 0.3}
ENR_BID_GW = 0.80          # ENR fund-held levered upstream: G15 drought ladder price; GW bid sensitivity 0.75-0.85


def share_of(book: str) -> dict:
    return SHARE_V2 if RB.BOOKS[book]["ra"] else SHARE_V1


def pz_stationary() -> np.ndarray:
    w, v = np.linalg.eig(E.PZ_Q.T)
    p = np.real(v[:, np.argmin(np.abs(w - 1))])
    return p / p.sum()

# ---------------------------------------------------------------- gap_04 (main) October-2026 initial state
Z0_G4 = np.array([0.03, 0.0, 0.0, 0.02, 0.10, 0.85])     # N, B, SG, DB, SS, GW  [gap_04 s6.2, elicited]
E0_G4 = np.array([0.0, 0.08, 0.874, 0.046])               # O, N, D, F            [gap_04 s6.2 filter]
D2026 = 0.058                                             # reduced-form smoothed d_2026 [gap_04 s6.2]
FB27_MU, FB27_SD = 4.66, 0.98                             # 2027 fiscal balance, oil start 105 + IMF fusion
P_OV27 = 0.0123                                           # P(owner override) in 2027 [gap_04 results]
OIL0 = 105.0                                              # futures-curve start, not spot [gap_04 s6.1 step 6]

# ---------------------------------------------------------------- census v1.0 (groups synthesis s6)
UNF_V1 = dict(pe=27.4, sec=3.5, co=1.5, cs=1.2, pc=3.0)
SEC_DEF_V1, PC_REV_V1 = 0.4, 1.0
assert abs(sum(UNF_V1.values()) + SEC_DEF_V1 + PC_REV_V1 - 38.0) < 1e-9

# ---------------------------------------------------------------- group-engine defaults (all [I] unless noted)
VINT = np.arange(2012, 2032)          # PE vintages carried (2012..2031)
PE_B = 2.0                            # TA bow (stream 04 / G1)
PE_CALL = (0.20, 0.25, 0.30, 0.35, 0.40)   # of remaining unfunded by age [S: Ljungqvist-Richardson via G1]
SIG_GP, SIG_VINT, SIG_FUND = 0.03, 0.01, 0.025   # G9 truth: GP 3%, vintage ~1%, idiosyncratic 2.5%
SIG_CO_ETA = 0.024                    # company-level alpha error -> rho_GP(fund, co-invest) ~ 0.6
CO_N, CO_SIGMA_SIZE, CO_L0 = 90, 0.8, 0.40
CO_BETA_A, CO_SIG_ID = 0.9, 0.25
CO_WEIB_K, CO_WEIB_ETA = 1.447, 7.70  # Kaplan-Stromberg fit (G4)
MX = np.array([1.3, 1.0, 0.5, 0.3])   # exit multipliers O/N/D/F (G4)
CO_FEE_EDGE = 0.02                    # co-investment edge over fund net (avoided fees less costs) [I]
CO_RECAP_Q = np.array([0.03, 0.025, 0.0125, 0.0])   # recap probability per quarter by e (0 in crisis)
CO_RECAP_DD = 0.30                    # recap adds 30% to debt (~ +1 turn)  [S: LCD via G4, ~+1 turn]
CO_OVERLAP_P, CO_OVERLAP_S = 0.25, 0.50   # share of companies also borrowing from ADIC PC; PC share of recap debt
CO_OVERLAP_T0 = 0.25                  # t0 PC loans to overlap companies, per $ of ADIC look-through debt
COFLOW_THETA, COFLOW_A = 0.33, 0.45   # s4.7: Bain median 33c offered per $ (GP level, used at LP level); accept
COFLOW_D = (0.15, 0.25, 0.25, 0.20, 0.15)
PC_SPLIT = dict(sma=0.40, cef=0.45, evg=0.10, bdc=0.05)
PC_COUPON = 0.090                     # SOFR + ~5.1% blended
PC_PD_N, PC_LGD = 0.011, 0.67         # FBE severity-anchored pair (gap_01 / groups R1)
PC_CPR = np.array([0.32, 0.24, 0.18, 0.10])   # O/N/D/F; crisis 6.5%
PC_PIK = np.array([0.07, 0.07, 0.11, 0.14])   # share of income PIK; crisis 18% [S: Lincoln 11.3% Q2-26]
PC_DDTL = np.array([0.15, 0.15, 0.20, 0.30])  # annual draw of undrawn; crisis 60%, onset 50%
CS_SPLIT_CP = 0.55                    # families A+F+B cash-pay; C+D+E PIK-capable
CS_Y = (0.095, 0.125)
CS_PD = np.array([0.010, 0.010, 0.025, 0.050])   # O,N,D,F; crisis 7%; RECV 1.5%
CS_LGD = (0.40, 0.70)
CS_RR = np.array([0.20, 0.20, 0.08, 0.05])       # repayment rates; crisis 3%; RECV 15%
SEC_THETA_Q = 0.92                    # quality / winner's-curse haircut on contingent purchases [I; G2 curse ~5%]
TAIL_EQ_SHARE = 0.80                  # tail budget split equity / Brent ladders [I]
DISC_BAR = np.array([0.05, 0.08, 0.13, 0.20])    # LP-portfolio discount by exit window O/N/D/F
#   anchors: D, no drawdown 13% = Jefferies H1-2026 87% [S]; 2022 81% [S]; H2-2008 61% [S: Cogent]; 2009 54% [S]


@dataclass(frozen=True)
class Cfg:
    init: str = "gap04"
    groups: str = "cohort"
    overlay: str = "L1"
    links: bool = True
    stage: str = "cfp"
    census: str = "v1"
    players: frozenset = frozenset(PLAYERS)
    trigger: str = "current"
    budget: float = 3.9                # contingent budget per 12 months [I-calc G8 E1: SEC 2.07 + CAP 1.80]
    desk_sd: float = 0.03              # Secondaries desk forecast error on the external clearing discount
    track: bool = False
    tracers: bool = False
    bump: object = None                # (group key, $bn) extra year-1 commitment, for reduced-H coefficients
    stage_conv: str = "gross"          # CFP indicators on gross Treasury ('gross', as the groups table) or
                                       # net of drawn facilities ('net', proposed)
    theta_q: float = SEC_THETA_Q       # economic value per $ of staleness-adjusted reference NAV bought
    gp_new: bool = True                # new group playbook actions (PC SMA run-off, co-investment pause,
                                       # overlay monetization / de-risking / vega floor, TPA beta rule)
    # ---------------- ra_gap_01 additions
    book: str = "v1"                   # 'v1' | 'v2u16' | 'v2u11'
    theta: float = 0.76                # s*(theta) used by the CFP survival proxy (recalibrated theta*)
    ra_scale: float = 1.0              # Real Assets NAV scale (size scans; PE absorbs the difference)
    ra_split: tuple = None             # RA closed-end commitment split (RE_CE, INF_CE, ENR_CE); None = census
    ra_ext: float = None               # P(extension | no lender): None = 0.35 outside crisis, 0 in crisis (and
                                       # 0.35 (1 - theta) in the proxy); a float fixes it (axis 0 / 0.35)
    ra_avail: bool = True              # lender availability by state (N 0.97 / T 0.825 / C 0.55)
    ra_fund: str = "waterfall"         # fund-level refinancing module: 'waterfall' | 'upper' | 'off'
    enr_sell: float = 0.70             # ENR SELL at t0 ($bn reported NAV) when the RA player is on
    enr_bid: float = ENR_BID_GW
    ra_cashout: bool = True            # cash-out at maturity in the RA playbook (controlled, Amber, not crisis)
    ra_jv: bool = True                 # pre-arranged JV sell-downs in the RA playbook
    ra_notices: bool = True            # open-end notices at Amber in the RA playbook
    pe_pace_override: float = None     # PE plan pace ($bn a year) override, e.g. scaled sealed pace
    # ---------------- ri: oil-sensitivity switches (defaults reproduce ra_gap_01)
    ra_oil_enr: bool = True            # ENR oil channels (oil elasticity of value; oil-elastic income and exits)
    ra_oil_gcc: bool = True            # GCC real-estate fiscal channels (Z-state drag, income and exit links)

    @staticmethod
    def t1():
        return Cfg(init="gap02", groups="rate", overlay="t1", links=False, stage="t1", census="gc2",
                   players=frozenset(PLAYERS), trigger="none")


def qr(r):
    """Quarterly rate from an annual rate (vectorised)."""
    return 1.0 - (1.0 - np.minimum(0.95, r)) ** 0.25


# ======================================================================================== calibrations
_CACHE: dict = {}


def pe_rates(age, L):
    age = np.maximum(age, 0.0)
    rd = np.minimum(0.95, (age / L) ** PE_B)
    c = np.select([age < 1, age < 2, age < 3, age < 4], list(PE_CALL[:4]), PE_CALL[4])
    return rd, c


def pe_history(K26, g, L):
    """Deterministic 2012-2026Q3 history: normal to 2021 (growth 11%), drought 2022-26 (7%, m^D 0.5)
    (G1 s4.2). Returns unfunded and NAV by vintage at 2026.75 and quarterly PE commitments 2021Q4..2026Q3."""
    vint = np.arange(2012, 2027)
    K = K26 * (1 + g) ** (vint - 2026)
    U = np.zeros(vint.size)
    N = np.zeros(vint.size)
    hist_c = []
    nq = int(round((2026.75 - 2012) * 4))
    for q in range(nq):
        tau = 2012 + q / 4
        vi = int(math.floor(tau + 1e-9)) - 2012
        U[vi] += K[vi] / 4
        hist_c.append(K[vi] / 4)
        drought = tau >= 2022
        G, mD, mC = (0.07, 0.5, 0.97) if drought else (0.11, 1.0, 1.0)
        rd, c = pe_rates(tau - (vint + 0.5), L)
        active = vint <= math.floor(tau + 1e-9)
        call = qr(c * mC) * U * active
        N *= (1 + G) ** 0.25
        dist = qr(rd * mD) * N
        N += call - dist
        U -= call
    return vint, K, U, N, np.array(hist_c[-20:])


def pe_calibration():
    """Solve the commitment level and growth (K26, g) that give census unfunded 27.4 and NAV 52, and the TA
    life L that gives a 20% pooled normal-regime distribution rate on the t0 book (t1/G7 normal rate)."""
    if "pe" in _CACHE:
        return _CACHE["pe"]

    def solve_kg(L):
        def f(x):
            _, _, U, N, _ = pe_history(x[0], x[1], L)
            return [U.sum() / 27.4 - 1, N.sum() / 52.0 - 1]
        r = least_squares(f, x0=[9.0, 0.10], bounds=([1.0, -0.2], [40.0, 0.6]))
        return r.x

    def pooled_rate(L):
        K26, g = solve_kg(L)
        vint, _, U, N, _ = pe_history(K26, g, L)
        rd, _ = pe_rates(2026.75 - (vint + 0.5), L)
        return float((rd * N).sum() / N.sum()) - 0.20

    L = brentq(pooled_rate, 6.0, 30.0, xtol=1e-4)
    K26, g = solve_kg(L)
    vint, K, U, N, hist_c = pe_history(K26, g, L)
    rd, c = pe_rates(2026.75 - (vint + 0.5), L)
    out = dict(L=float(L), K26=float(K26), g=float(g), K=K.tolist(), U0=U.tolist(), N0=N.tolist(),
               hist_c=hist_c.tolist(), pooled_dist_normal=float((rd * N).sum() / N.sum()),
               pooled_call=float((c * U).sum() / U.sum()), U_tot=float(U.sum()), N_tot=float(N.sum()))
    _CACHE["pe"] = out
    return out


def pe_calibration_book(book: str, ra_scale: float = 1.0):
    """v1: gap_04's calibration (U 27.4 / N 52). v2: the sealed census v1.1 vintage profile (groups gap_02)
    rescaled to PE NAV and unfunded of the book; TA life L solved for a 20% pooled normal distribution rate on
    that vintage mix (the t1 / G7 normal rate, as gap_04)."""
    if book == "v1":           # ri: only the census v1.0 book keeps gap_04's U 27.4 history; 'v1s' uses the seal
        return pe_calibration()
    key = f"pe_{book}_{ra_scale:.4f}"
    if key in _CACHE:
        return _CACHE[key]
    priv = RB.book_priv(book, ra_scale)
    unf = RB.book_unf(book, ra_scale)
    v = RB.pe_vintages_v2(priv["pe"], unf["pe"])
    vint = v["vint"]

    def pooled(L):
        rd, _ = pe_rates(2026.75 - (vint + 0.5), L)
        return float((rd * v["N0"]).sum() / v["N0"].sum()) - 0.20
    L = brentq(pooled, 4.0, 40.0, xtol=1e-4)
    rd, c = pe_rates(2026.75 - (vint + 0.5), L)
    out = dict(L=float(L), K26=float(v["pace_2026"]), g=None, K=None, U0=v["U0"].tolist(), N0=v["N0"].tolist(),
               hist_c=v["hist_c"].tolist(), pooled_dist_normal=float((rd * v["N0"]).sum() / v["N0"].sum()),
               pooled_call=float((c * v["U0"]).sum() / max(v["U0"].sum(), 1e-9)), U_tot=float(v["U0"].sum()),
               N_tot=float(v["N0"].sum()))
    _CACHE[key] = out
    return out


def company_census():
    """Fixed synthetic census of the 90 co-investments (SYN-), the 70 PE GPs (tier weights) and overlaps."""
    if "co" in _CACHE:
        return _CACHE["co"]
    r = np.random.default_rng(336)   # seed chosen so the draw matches census v1.0: effective N ~46, largest ~$1.1bn
    w = np.concatenate([np.full(7, 0.20 / 7), np.full(35, 0.60 / 35), np.full(28, 0.20 / 28)])
    size = np.exp(CO_SIGMA_SIZE * r.standard_normal(CO_N))
    e0 = size / size.sum() * 18.0
    age0 = r.uniform(0.0, 7.0, CO_N)
    shared = r.random(CO_N) < 0.70                         # ~70% share a GP with a PE fund [groups s3.4]
    gp = np.where(shared, r.choice(70, CO_N, p=w), 70 + r.integers(0, 30, CO_N))
    overlap = r.random(CO_N) < CO_OVERLAP_P
    v0 = e0 / (1 - CO_L0)
    d0 = CO_L0 * v0
    out = dict(w=w, e0=e0, v0=v0, d0=d0, age0=age0, gp=gp, overlap=overlap,
               n_eff=float(1 / ((e0 / e0.sum()) ** 2).sum()), largest=float(e0.max()))
    _CACHE["co"] = out
    return out


# ======================================================================================== T4' survival proxy
_TS = 25                               # months evaluated (thresholds are 12 / 18 / 24)
_PROXY_CACHE: dict = {}


def proxy_consts(theta: float = 0.76) -> dict:
    """Stress-path constants of s*(theta) for the survival proxy (gap_04 hard-coded theta = 0.76)."""
    key = round(float(theta), 6)
    if key in _PROXY_CACHE:
        return _PROXY_CACHE[key]
    eq = np.zeros(36); eq[0] = -(0.30 + 0.10 * theta); eq[12:24] = 0.02; eq[24:] = 0.008
    fi = np.zeros(36); fi[:3] = -0.02; fi[3:] = 0.005
    hfr = np.zeros(36); hfr[0] = 0.3 * eq[0] - 0.06; hfr[12:] = 0.008
    pm = np.zeros(36); pm[3] = -0.08; pm[6] = -0.08; pm[9] = -0.04; pm[14::3] = 0.01
    crm = np.arange(36) < int(round(18 + 6 * theta))
    idx_eq = np.cumprod(1 + eq); idx_em = np.cumprod(1 + 1.2 * eq)
    idx_fi = np.cumprod(1 + fi); idx_hf = np.cumprod(1 + hfr)
    k_dm = np.zeros(36); k_fi = np.zeros(36); k_em = np.zeros(36)
    rem_dm = rem_fi = rem_em = 1.0
    a_dm = a_fi = a_em = 0.0
    for t in range(36):
        f = min(0.5, rem_dm); rem_dm -= f; a_dm += f * idx_eq[t] * 0.985
        f = min(0.5, rem_fi); rem_fi -= f; a_fi += f * idx_fi[t] * 0.95
        if t >= 1:
            f = min(0.5, rem_em); rem_em -= f; a_em += f * idx_em[t] * 0.95
        k_dm[t], k_fi[t], k_em[t] = a_dm, a_fi, a_em

    def hf_cum(sched_m):
        cum = np.zeros(36); backlog = 0.0; acc = 0.0
        for t in range(36):
            due = sched_m[t] * idx_hf[t] + backlog
            paid = 0.83 * due if crm[t] else due
            backlog = due - paid
            acc += paid
            cum[t] = acc
        return cum
    sch = np.zeros(76)
    for q, s in enumerate(E.HF_SCHED):
        sch[3 * q:3 * q + 3] += s / 3
    k_hf = hf_cum(sch[:36])
    k_q = np.zeros((10, 36))
    for q in range(10):
        s = np.zeros(76); s[3 * q:3 * q + 3] = 1 / 3
        k_q[q] = hf_cum(s[:36])
    out = dict(theta=theta, eq=eq, fi=fi, hfr=hfr, pm=pm, crm=crm, dmult=0.45 * (1 - theta),
               cmult=1.0 + 0.5 * theta, k_dm=k_dm, k_fi=k_fi, k_em=k_em, k_hf=k_hf, k_q=k_q)
    _PROXY_CACHE[key] = out
    return out


_C076 = proxy_consts(0.76)
K_DM, K_FI, K_EM, K_HF, K_Q = _C076["k_dm"], _C076["k_fi"], _C076["k_em"], _C076["k_hf"], _C076["k_q"]
TRE_HC = 0.27 * 0.02 + 0.33 * 0.10


def mo(r):
    return 1.0 - (1.0 - np.minimum(0.95, r)) ** (1.0 / 12.0)


def sh_tp_proxy(st: dict, T: int = _TS, theta: float = 0.76):
    """Months of survival on Treasury + Public Markets (SH_TP) and with committed facilities (SH_TPF) under
    T4' = s*(theta), canonical conventions (gap_02 s1.1), from the current state of every path. Mirrors
    the ladder month by month (vertex shock; PE/Sec/Co distributions at 0.45(1-theta) x drought; calls
    x(1+0.5 theta); PC 10% / CS 7% cash; cap draws on opening NAV with annual reset; IM 4->10%; tail paid at
    months 1 and 5; opportunistic loss 1.5% of NAV over 3 months; 4% hard floor). ra_gap_01: optional keys
    'share' (plan pacing split; v1 default 60/10/10/10/10) and the RA state (ra_va, ra_gt, ra_d, ra_u), whose
    theta-indexed leg (ra_module.ra_proxy_paths) adds RA flows and RA reported NAV."""
    C = proxy_consts(theta)
    _EQ, _FI, _HFR, _PM, _CRM = C["eq"], C["fi"], C["hfr"], C["pm"], C["crm"]
    _DMULT, _CMULT = C["dmult"], C["cmult"]
    k_dm, k_fi, k_em, k_hf, k_q = C["k_dm"], C["k_fi"], C["k_em"], C["k_hf"], C["k_q"]
    n = st["tre"].shape[0]
    usable = st["tre"] - st["enc"]
    cbc_base = usable * (1 - TRE_HC)
    priv = {g: st["priv"][g].copy() for g in GKEYS}
    unf = st["unf"].copy()
    sec_def = st["sec_def"].copy()
    rev0 = st["pc_rev"].copy(); rev = rev0.copy()
    liq = st["tre"] + st["dm"] + st["em"] + st["fi"] + st["hf"] + st["hf_q"].sum(axis=1)
    liq_parts = [st["tre"], st["dm"], st["em"], st["fi"], st["hf"] + st["hf_q"].sum(axis=1)]
    basis = st["basis"].copy()
    n_syn = st["n_syn"]
    im = 0.04 * n_syn
    nco = np.zeros(n)
    eq_idx = 1.0
    sh = np.full(n, T + 12, dtype=np.int16)
    shf = np.full(n, T + 12, dtype=np.int16)
    pace_m = st["pace"] / 12.0
    share = st.get("share", SHARE_V1)
    sh_unf = share["pe"] + share["sec"] + share["pc"] + share["cs"]
    tail_stress = st["tail_stress"]          # total stress payoff of the tail book at the vertex
    ra_net = ra_nav = None
    if "ra_va" in st:
        pm_arr = np.broadcast_to(np.asarray(pace_m, dtype=float), (n,)).copy()
        cut_arr = np.broadcast_to(np.asarray(st.get("ra_cut", False)), (n,)).copy()
        ra_net, ra_nav = RM.ra_proxy_paths(st, theta, T, _CRM, pm_arr, cut_arr,
                                           availability=st.get("ra_avail", True), ext=st.get("ra_ext", None),
                                           fund_module=st.get("ra_fund", "waterfall"))
    for t in range(T):
        pm = _PM[t]
        for g in GKEYS:
            priv[g] *= 1 + pm
        dist = np.zeros(n)
        for g, r in (("pe", 0.10), ("sec", 0.125), ("co", 0.09)):
            d = mo(r * (_DMULT if t < 24 else 1.0)) * priv[g]
            priv[g] -= d
            dist += d
        for g, rc, rn in (("pc", 0.10, E.DIST_NORMAL["pc"] * 0.92), ("cs", 0.07, E.DIST_NORMAL["cs"] * 0.92)):
            d = mo(rc if _CRM[t] else rn) * priv[g]
            priv[g] -= d
            dist += d
        crate = mo(0.28 * (_CMULT if t < 24 else 1.0))
        calls = crate * unf
        unf = unf - calls
        priv["pe"] += calls
        if t in (2, 5, 8, 11):
            sd = np.minimum(sec_def, st["sec_def0"] / 4)
            sec_def = sec_def - sd
            calls = calls + sd
        rv = np.minimum(rev, 0.5 * rev0 / 3 if t < 3 else mo(0.15) * rev)
        rev = rev - rv
        calls = calls + rv
        k = pace_m * (0.25 if (st["pace_cut"] and t >= 2 and _CRM[t]) else 1.0)
        unf = unf + sh_unf * k
        calls = calls + share["co"] * k
        rate = (0.10, 0.10, 0.075)[min(t // 12, 2)]
        if st["band"] and _CRM[t]:
            rate = 0.05
        priv_sum = sum(priv.values())
        ra_now = ra_nav[:, t] if ra_nav is not None else 0.0
        nav_est = liq + priv_sum + ra_now - nco
        if t % 12 == 0 and t > 0:
            lag = 1 + _PM[t - 1] + _PM[t - 2] + _PM[t - 3]
            basis = nav_est - priv_sum + priv_sum / lag
        draw = rate * basis / 12
        vm = n_syn * eq_idx * _EQ[t]
        eq_idx *= 1 + _EQ[t]
        im_new = (0.10 if (_CRM[t] and t < 12) else 0.04) * n_syn * eq_idx
        d_im = im_new - im
        im = im_new
        prem = st["prem_m"]
        tail = 0.5 * tail_stress if t in (1, 5) else 0.0
        opp = 0.015 * st["nav"] / 3 if t < 3 else 0.0
        fee = st["fee_m"]
        opex = 0.001 * st["nav"] / 12
        net = draw + calls + prem + opp + fee + opex + np.maximum(0.0, d_im) - dist - vm - tail \
            - np.maximum(0.0, -d_im)
        if ra_net is not None:
            net = net + ra_net[:, t]
        nco = nco + net
        # liquid book marked on the stress path
        liq_parts = [liq_parts[0], liq_parts[1] * (1 + _EQ[t]), liq_parts[2] * (1 + 1.2 * _EQ[t]),
                     liq_parts[3] * (1 + _FI[t]), liq_parts[4] * (1 + _HFR[t])]
        liq = sum(liq_parts)
        cbc = cbc_base + st["dm"] * k_dm[t] + st["fi"] * k_fi[t] + st["em"] * k_em[t] + st["hf"] * k_hf[t] \
            + st["hf_q"] @ k_q[:, t]
        head = cbc - 0.04 * nav_est - nco
        headf = head + (st["fac"] if t >= 1 else 0.0)
        sh = np.where((head < 0) & (sh > T), t + 1, sh)
        shf = np.where((headf < 0) & (shf > T), t + 1, shf)
    return sh, shf


def lcr30_proxy(tre, enc, dm, nav, unf_tot, n_syn, d_rate):
    """ADIC-LCR(30d) with Basel L2 / L2B caps on Treasury-controlled assets (gap_02 lcr30_t0, generalised)."""
    l1 = np.maximum(0.40 * tre - enc, 0.0) + 0.27 * tre * 0.98
    l2a = 0.33 * tre * 0.85
    l2b = dm * 0.5
    adj15 = np.maximum(np.maximum(l2b - 15 / 85 * (l1 + l2a), l2b - 15 / 60 * l1), 0.0)
    adj40 = np.maximum((l2a + l2b - adj15) - 2 / 3 * l1, 0.0)
    num = l1 + l2a + l2b - adj15 - adj40
    out = d_rate * nav / 12 + 1.34 * unf_tot / 38.0 + 0.25 + 0.117 * n_syn + 0.06 * n_syn + 0.005 * nav \
        + 0.375 + 0.0020 * E.NAV0 / 12
    inflow = np.minimum(0.45, 0.75 * out)
    return num / np.maximum(out - inflow, 1e-6)


def band_of(x, edges, higher_is_better=True):
    """Stage 0..3 from a metric and three edges (Green/Amber/Red/Black)."""
    a, b, c = edges
    if higher_is_better:
        return np.where(x >= a, 0, np.where(x >= b, 1, np.where(x >= c, 2, 3)))
    return np.where(x <= a, 0, np.where(x <= b, 1, np.where(x <= c, 2, 3)))


# ======================================================================================== option helpers
def bs_put(x, k, tau, sig, r=E.SOFR):
    """Black-Scholes put on spot x (relative units), strike k, tenor tau (years), vol sig."""
    tau = np.maximum(tau, 1e-6)
    sd = sig * np.sqrt(tau)
    d1 = (np.log(np.maximum(x, 1e-9) / k) + (r + 0.5 * sig ** 2) * tau) / sd
    d2 = d1 - sd
    return k * np.exp(-r * tau) * ndtr(-d2) - x * ndtr(-d1)


def put_spread(x, k1, k2, tau, sig_atm, skew=1.5, r=E.SOFR):
    s1 = sig_atm * (1 + skew * (1 - k1))
    s2 = sig_atm * (1 + skew * (1 - k2))
    return np.maximum(bs_put(x, k1, tau, s1, r) - bs_put(x, k2, tau, s2, r), 0.0)


def oil_fwd(s, tau):
    """Oil forward consistent with the scenario dynamics (mean reversion to $70, kappa 0.4 a year), so that
    oil puts are struck and priced on the curve, not on spot (gap_04 s6.1 step 6)."""
    return s * np.exp((1 - 0.6 ** tau) * (np.log(70.0) - np.log(s)))


# ======================================================================================== simulation
def simulate(m, pol, cfg: Cfg = Cfg(), n: int = 10000, seed: int = 20261018, hf_gate_pass: float = 0.83,
             overrides: bool = True) -> dict:
    on = lambda p: p in cfg.players  # noqa: E731
    rate_mode = cfg.groups == "rate"
    pi_c = E.stationary_crisis_share(m)
    mu_calm = E.calm_drift(m, pi_c)
    rng = np.random.default_rng(seed)           # exogenous stream (identical to t1_engine)
    rng_p = np.random.default_rng(seed + 7)     # sale execution (identical to t1_engine)
    rng_s = np.random.default_rng(seed + 101)   # initial-state extras
    rng_f = np.random.default_rng(seed + 202)   # discount, desk, oil, GP / vintage truth
    rng_c = np.random.default_rng(seed + 303)   # company shocks
    rng_o = np.random.default_rng(seed + 404)   # overlay templates
    cdfZ = np.cumsum(E.PZ_Q, axis=1)
    eq_arith = math.log1p(m.eq_g) + 0.5 * 0.165 ** 2

    def alpha_for(g_target, beta):
        return (g_target + 0.5 * (beta * 0.165) ** 2) - (m.cash_lr + beta * (eq_arith - m.cash_lr))

    tgt = {"pe": m.pe_g, "sec": m.pe_g + 0.005, "co": m.pe_g, "cs": m.cs_g, "pc": m.pc_g}
    alpha = {g: alpha_for(tgt[g], E.BETA[g]) for g in E.PRIV0}
    alpha["pc"] += pi_c * 0.08
    alpha_hf = alpha_for(m.hf_g, 0.3) + pi_c * 0.08

    # ------------------------------------------------ effective levers (player gating)
    rcf = pol.rcf if on("CF") else 0.0
    navf = pol.navf if on("CF") else 0.0
    band = pol.band and on("CF")
    reserve = pol.reserve if on("CF") else 0.08
    hf_t0 = pol.hf_t0 if on("PM") else 0.0
    hf_amber = pol.hf_amber and on("PM")
    p2s_on = on("PM")
    amber_on = {"pc": on("PC"), "cs": on("CS")}
    amber_t0 = pol.amber_t0 if (on("PC") and on("CS")) else 0.0
    repay_on = on("CF")
    SH = share_of(cfg.book)
    ra_book = RB.BOOKS[cfg.book]["ra"]
    ra_on = on("RA") and ra_book
    pace_g = {g: (pol.pace if on(OWNER[g]) else 12.0) * SH[g] for g in SH}
    plan_g = {g: 12.0 * SH[g] for g in SH}
    if cfg.pe_pace_override is not None:
        plan_g["pe"] = cfg.pe_pace_override
        pace_g["pe"] = cfg.pe_pace_override * (pol.pace / 12.0 if on("PE") else 1.0)
    cut_g = {g: bool(pol.pace_cut and on(OWNER[g])) for g in SH}
    pace_tot = sum(pace_g.values())
    ovl_on = on("OVL") and cfg.gp_new
    tpa_on = on("TPA") and cfg.gp_new
    co_pause = on("CO") and cfg.gp_new
    pc_runoff = on("PC") and cfg.gp_new
    sec_cont = on("SEC") and cfg.trigger != "none"
    cs_cont = on("CS") and cfg.trigger != "none"
    cont_share = {"sec": (2.07 / 3.87 if sec_cont else 0.0), "cs": (1.80 / 3.87 if cs_cont else 0.0)}

    if ra_book or cfg.book != "v1":
        ub = RB.book_unf(cfg.book, cfg.ra_scale)
        unf0 = {g: ub[g] for g in ("pe", "sec", "co", "cs", "pc")}
        sec_def0, pc_rev0 = RB.SEC_DEF_V1, RB.PC_REV_V1
    elif cfg.census == "v1":
        unf0, sec_def0, pc_rev0 = dict(UNF_V1), SEC_DEF_V1, PC_REV_V1
    else:
        unf0, sec_def0, pc_rev0 = dict(E.UNF0), E.SEC_DEF0, E.PC_REV0
    PRIVB = {g: v for g, v in RB.book_priv(cfg.book, cfg.ra_scale).items() if g != "ra"}

    # ------------------------------------------------ balances (t1)
    tre = np.full(n, E.TRE0)
    lo = {k: np.full(n, v) for k, v in E.LO0.items()}
    hf = np.full(n, E.HF0)
    hf_q = np.zeros((n, 10))
    priv = {k: np.full(n, v) for k, v in PRIVB.items()}
    econ_prev = {k: np.zeros(n) for k in E.PRIV0}
    rep = {k: np.full(n, v) for k, v in PRIVB.items()}
    unf = {k: np.full(n, v) for k, v in unf0.items()}
    sec_def = np.full(n, sec_def0)
    pc_rev = np.full(n, pc_rev0)
    n_tpa = np.full(n, E.N_SYN0)
    n_p2s = np.zeros(n)
    n_syn = n_tpa + n_p2s
    b_r = np.zeros(n)
    b_n = np.zeros(n)
    z = rng.choice(6, size=n, p=(Z0_G4 if cfg.init == "gap04" else E.Z0_PROB))
    crisis = np.zeros(n, dtype=bool)
    cdur = np.zeros(n, dtype=int)
    since_exit = np.full(n, 99)
    e = rng_s.choice(4, size=n, p=E0_G4) if cfg.init == "gap04" else np.full(n, 2)
    d_prev = np.full(n, 0.075)
    d_year = np.full(n, 0.075)
    basis = np.full(n, E.NAV0)
    override_year = np.zeros(n, dtype=bool)
    im_prev = E.IM_N * n_syn
    if cfg.init == "gap04":
        fb27 = FB27_MU + FB27_SD * rng_s.standard_normal(n)
        dstar = np.clip(7.5 - 0.625 * fb27, 5, 10)
        d27 = np.clip(0.5 * D2026 * 100 + 0.5 * dstar, 5, 10) / 100
        ov27 = rng_s.random(n) < P_OV27
        d27 = np.where(ov27, 0.10 + rng_s.uniform(0.02, 0.05, n), d27)

    red = np.zeros(n, dtype=bool)
    black = np.zeros(n, dtype=bool)
    black_12m = np.zeros(n, dtype=bool)
    first_red = np.full(n, -1)
    red_sales = np.zeros(n)
    red_loss = np.zeros(n)
    amber_sales = np.zeros(n)
    amber_loss = np.zeros(n)
    shortfall = np.zeros(n)
    withheld = np.zeros(n)
    band_active_12m = np.zeros(n, dtype=bool)
    paid_fv = np.zeros(n)
    fees = np.zeros(n)
    interest = np.zeros(n)
    max_debt_ratio = np.zeros(n)
    covenant_trig = np.zeros(n, dtype=bool)
    navf_trig_12m = np.zeros(n, dtype=bool)
    floor4_breach = np.zeros(n, dtype=bool)
    below8_streak = np.zeros(n, dtype=int)
    restore_fail = np.zeros(n, dtype=bool)
    forced_paydown = np.zeros(n)
    max_enc = np.zeros(n)
    commit_forgone = np.zeros(n)
    forgone_g = {g: np.zeros(n) for g in SH}
    forgone_t = np.zeros((n, E.T_Q))
    stage_hist = np.zeros((E.T_Q, 4))
    netneed8 = np.zeros(n)
    nav_min = np.full(n, E.NAV0)
    bh = dict(tre=np.full(n, E.TRE0), dm=np.full(n, E.LO0["dm"]), em=np.full(n, E.LO0["em"]),
              fi=np.full(n, E.LO0["fi"]), hf=np.full(n, E.HF0))
    tp0 = E.TRE0 + sum(E.LO0.values()) + E.HF0
    tp_bh8 = np.full(n, tp0)
    hf_bh_q = np.tile(E.HF0 * E.HF_SCHED, (n, 1))
    hf_bh_cash = np.zeros(n)
    nco_bh = np.zeros(n)
    gstar = np.full(n, -np.inf)

    # ------------------------------------------------ cohort engines
    if not rate_mode:
        cal = pe_calibration_book(cfg.book, cfg.ra_scale)
        cc = company_census()
        V = VINT.size
        PE_N = np.zeros((n, V)); PE_U = np.zeros((n, V))
        PE_N[:, :15] = np.array(cal["N0"]) * (PRIVB["pe"] / cal["N_tot"])
        PE_U[:, :15] = np.array(cal["U0"]) * (unf0["pe"] / cal["U_tot"])
        PE_R = PE_N.copy()
        PE_eprev = np.zeros((n, V))
        L_pe = cal["L"]
        gam = SIG_GP * rng_f.standard_normal((n, 100))            # GP effects (annual alpha), 70 PE + 30 outside
        u_v = SIG_VINT * rng_f.standard_normal((n, V))            # vintage effects
        pe_gp_alpha = gam[:, :70] @ cc["w"]
        gam_co = gam if cfg.links else SIG_GP * rng_f.standard_normal((n, 100))
        # Secondaries: S1 funds (5.6 NAV, all regular unfunded), LP interests S3+S6 (5.0), CVs S4+S5 (3.4)
        SN1 = np.full(n, 5.6); SR1 = SN1.copy(); SU1 = np.full(n, unf0["sec"])
        SN3 = np.full(n, 5.0); SR3 = SN3.copy()
        SN4 = np.full(n, 3.4); SR4 = SN4.copy()
        SNc = np.zeros(n); SRc = np.zeros(n); SUc = np.zeros(n)
        s_eprev = np.zeros(n); s_eprev_cv = np.zeros(n); s_eprev_c = np.zeros(n)
        alpha_cv = alpha_for(tgt["sec"], 1.5)
        # Capital Solutions: cash-pay and PIK-capable claims, contingent cohort
        CC = np.full(n, 8.0 * CS_SPLIT_CP); CK = np.full(n, 8.0 * (1 - CS_SPLIT_CP)); CN = np.zeros(n)
        CN_age = np.zeros(n)
        CU = np.full(n, unf0["cs"])
        cs_mark = np.ones(n); cs_rep = np.full(n, 8.0)
        # Co-investment: 90 companies (ADIC look-through units) + yearly new-deal cohorts
        co_v = np.tile(cc["v0"], (n, 1)); co_d = np.tile(cc["d0"], (n, 1))
        co_alive = np.ones((n, CO_N), dtype=bool)
        co_age = np.tile(cc["age0"], (n, 1))
        co_M = np.tile(cc["e0"], (n, 1))
        co_eta = SIG_CO_ETA * rng_f.standard_normal((n, CO_N))
        co_gam = gam_co[:, cc["gp"]]
        alpha_E = alpha_for(tgt["co"], E.BETA["co"]) + CO_FEE_EDGE
        alpha_A = alpha_E * (1 - CO_L0)
        co_ovl = cc["overlap"][None, :] & cfg.links
        pc_loan = np.where(co_ovl, CO_OVERLAP_T0 * co_d, 0.0)    # within the PC SMA par
        CO_U = np.full(n, unf0["co"])
        NEWN = np.zeros((n, 6)); NEWR = np.zeros((n, 6)); NEW_age = np.zeros(6)
        new_gam = gam_co[:, :70] @ cc["w"]
        # PE commitment history for the co-investment flow: the calibrated program's own quarterly
        # commitments over the last 20 quarters (2021Q4..2026Q3), scaled to the census unfunded
        pe_hist = list(np.array(cal["hist_c"]) * (unf0["pe"] / cal["U_tot"]))
        pe_hist_arr = [np.full(n, c) for c in pe_hist]
        dq = np.repeat(np.array(COFLOW_D) / 4.0, 4)                # quarterly lag weights, sum = 1
        # Private Credit wrappers (par) and marks
        PSMA = np.full(n, 14.0 * PC_SPLIT["sma"]); PCEF = np.full(n, 14.0 * PC_SPLIT["cef"])
        PEVG = np.full(n, 14.0 * PC_SPLIT["evg"]); PBDC = np.full(n, 14.0 * PC_SPLIT["bdc"])
        PSMA = PSMA + 0.0  # overlap loans are part of SMA par
        PU = np.full(n, unf0["pc"])
        pc_price = np.ones(n); pc_rep = np.full(n, 14.0)

    # ------------------------------------------------ Real Assets (ra_gap_01)
    ra = None
    if ra_book:
        rng_ra = np.random.default_rng(seed + 505)   # dedicated stream: CRN preserved for everything else
        ra = RM.RAState(n, m, rng_ra, m.cash_lr, m.eq_g, pi_c, pz_stationary(), scale=cfg.ra_scale,
                        split=cfg.ra_split, ext=cfg.ra_ext, fund_module=cfg.ra_fund, availability=cfg.ra_avail,
                        md_f=m.md_f, mc_f=m.mc_f, oil_enr=cfg.ra_oil_enr, oil_gcc=cfg.ra_oil_gcc)  # ri: switches
        beta_desm = RM.BETA_RECOVERY_DESM * ra.beta_eq
        beta_obs = RM.BETA_RECOVERY_OBS * ra.beta_eq
    ra_cash_t0 = np.zeros(n)
    enr_vgive = np.zeros(n)
    ra_cure_q = np.zeros((n, E.T_Q))
    ra_flow_q = np.zeros((n, E.T_Q))
    ra_jv_tot = np.zeros(n)
    ra_red_tot = np.zeros(n)
    ra_co_tot = np.zeros(n)
    ra_forced = np.zeros(n)
    ra_navT_y = np.zeros((n, 5)); ra_navA_y = np.zeros((n, 5)); ra_navS_y = np.zeros((n, 5))
    ra_dva = {k: np.zeros((n, 5)) for k in ("star_desm", "rep_obs", "rep_desm", "true_desm", "star_obs", "true_b1")}
    ra_cash_y = np.zeros((n, 5))
    ra_oil0 = None
    wrongway = np.zeros(n, dtype=bool)           # oil-down fiscal states (SG or DB) within 8 quarters

    # ------------------------------------------------ overlay L1 state
    if cfg.overlay == "L1":
        eq_lvl = np.ones(n)
        eq_hist = [np.ones(n) for _ in range(4)]
        oil = np.full(n, OIL0)
        prem_eq_q = TAIL_EQ_SHARE * E.TAIL_PREM * E.NAV0 / 4
        prem_oil_q = (1 - TAIL_EQ_SHARE) * E.TAIL_PREM * E.NAV0 / 4
        # 4 tranches each (rolling quarterly, 12-month tenor); ages 0..3 at t0, struck at today's levels
        TE_N = np.zeros((n, 4)); TE_S = np.ones((n, 4)); TE_age = np.array([0, 1, 2, 3])
        TO_N = np.zeros((n, 4)); TO_S = np.zeros((n, 4))      # TO_S = forward to expiry at strike date
        for j in range(4):
            px = put_spread(1.0, 0.90, 0.70, (4 - TE_age[j]) / 4, 0.16)
            TE_N[:, j] = prem_eq_q / px
            TO_S[:, j] = oil_fwd(OIL0, (4 - TE_age[j]) / 4)
            pxo = put_spread(1.0, 0.85, 0.65, (4 - TE_age[j]) / 4, 0.35, skew=0.5, r=0.0)
            TO_N[:, j] = prem_oil_q / pxo
        TE_live = np.ones((n, 4), dtype=bool); TO_live = np.ones((n, 4), dtype=bool)
        opp_scale = np.ones(n)
        trend_sig_prev = np.ones(n)
        disc_x = np.zeros(n)
    else:
        eq_lvl = np.ones(n)
        eq_hist = [np.ones(n) for _ in range(4)]
        disc_x = np.zeros(n)
        oil = np.full(n, OIL0)

    ring = np.zeros(n)                       # ring-fenced tail-hedge cash (trigger ring50 / ring100)
    ring_age = np.zeros((n, 4))              # FIFO buckets by quarter of receipt
    budget_rem = np.full(n, cfg.budget)
    stage_cfp = None
    stage_g = stage_n = None
    cfp_cnt = np.zeros(n, dtype=int)
    cfp_cnt_n = np.zeros(n, dtype=int)

    # ------------------------------------------------ tracking (per path, per year / quarter)
    T_Q = E.T_Q
    rec = {}
    if cfg.track:
        for kk in ("cash", "nav", "xs", "navavg"):
            rec[kk] = {g: np.zeros((n, 5)) for g in ACC}
        for kk in ("stage_cfp", "stage_t1", "stage_pol", "stage_gross", "stage_net"):
            rec[kk] = np.zeros((n, T_Q), dtype=np.int8)
        for kk in ("tier1", "crisis", "t2", "t3", "t4", "tier1_gross", "tier1_net", "red_q"):
            rec[kk] = np.zeros((n, T_Q), dtype=bool)
        rec["debt"] = np.zeros((n, T_Q), dtype=np.float32)
        for kk in ("disc", "dhat", "mon", "expiry", "deploy", "sh", "shf", "lcr", "oil", "cont_nav",
                   "coflow_acc", "co_deploy", "recap_gross", "recap_pc", "tail_mtm", "slack", "prem"):
            rec[kk] = np.zeros((n, T_Q), dtype=np.float32)
        rec["cont_out"] = np.zeros(n); rec["cont_in"] = np.zeros(n)
        rec["cont_out_sec"] = np.zeros(n); rec["cont_out_cs"] = np.zeros(n)

    # ------------------------------------------------ t0 actions
    def priv_nav_tot():
        if rate_mode:
            return sum(priv.values())
        return PE_N.sum(1) + SN1 + SN3 + SN4 + SNc + (CC + CK + CN) * cs_mark + co_equity_nav() \
            + NEWN.sum(1) + (PSMA + PCEF + PEVG + PBDC) * pc_price

    def priv_rep_tot():
        ra_rep = ra.nav_rep() if ra is not None else 0.0
        if rate_mode:
            return sum(rep.values()) + ra_rep
        return PE_R.sum(1) + SR1 + SR3 + SR4 + SRc + cs_rep + co_M.sum(1) * 1.0 + NEWR.sum(1) + pc_rep + ra_rep

    def co_equity_nav():
        return np.where(co_alive, np.maximum(co_v - co_d, 0.0), 0.0).sum(1)

    def group_nav(g):
        if rate_mode:
            return priv[g]
        if g == "pe":
            return PE_N.sum(1)
        if g == "sec":
            return SN1 + SN3 + SN4 + SNc
        if g == "cs":
            return (CC + CK + CN) * cs_mark
        if g == "co":
            return co_equity_nav() + NEWN.sum(1)
        return (PSMA + PCEF + PEVG + PBDC) * pc_price

    def group_rep(g):
        if rate_mode:
            return rep[g]
        if g == "pe":
            return PE_R.sum(1)
        if g == "sec":
            return SR1 + SR3 + SR4 + SRc
        if g == "cs":
            return cs_rep
        if g == "co":
            return co_M.sum(1) + NEWR.sum(1)
        return pc_rep

    def group_unf(g):
        if rate_mode:
            return unf[g]
        return {"pe": PE_U.sum(1), "sec": SU1 + SUc, "cs": CU, "co": CO_U, "pc": PU}[g]

    def sell_group(g, amt_rep):
        """Sell a reported-NAV amount of group g pro rata (buyer assumes the unfunded). Returns econ removed."""
        nonlocal PE_N, PE_R, PE_U, SN1, SR1, SU1, SN3, SR3, SN4, SR4, SNc, SRc, SUc, CC, CK, CN, CU, cs_rep
        nonlocal co_v, co_d, co_M, NEWN, NEWR, CO_U, PSMA, PCEF, PEVG, PBDC, PU, pc_rep, pc_loan
        rp = group_rep(g)
        frac = np.clip(amt_rep / np.maximum(rp, 1e-9), 0.0, 1.0)
        keep = 1 - frac
        econ_before = group_nav(g)
        if g == "pe":
            PE_N = PE_N * keep[:, None]; PE_R = PE_R * keep[:, None]; PE_U = PE_U * keep[:, None]
        elif g == "sec":
            SN1, SR1, SU1, SN3, SR3, SN4, SR4, SNc, SRc, SUc = (x * keep for x in
                                                                (SN1, SR1, SU1, SN3, SR3, SN4, SR4, SNc, SRc, SUc))
        elif g == "cs":
            CC, CK, CN, CU, cs_rep = CC * keep, CK * keep, CN * keep, CU * keep, cs_rep * keep
        elif g == "co":
            co_v = co_v * keep[:, None]; co_d = co_d * keep[:, None]; co_M = co_M * keep[:, None]
            NEWN = NEWN * keep[:, None]; NEWR = NEWR * keep[:, None]; CO_U = CO_U * keep
        else:
            PSMA, PCEF, PEVG, PBDC, PU, pc_rep = (x * keep for x in (PSMA, PCEF, PEVG, PBDC, PU, pc_rep))
            pc_loan = pc_loan * keep[:, None]
        return econ_before * frac

    if amber_t0 > 0:
        tot = E.PRIV0["pc"] + E.PRIV0["cs"]
        for g in ("pc", "cs"):
            sell_amt = amber_t0 * E.PRIV0[g] / tot
            if rate_mode:
                frac = sell_amt / E.PRIV0[g]
                priv[g] -= sell_amt
                rep[g] -= sell_amt
                unf[g] *= (1 - frac)
            else:
                sell_group(g, np.full(n, sell_amt))
            tre += sell_amt * E.PRICE_N[g]
            amber_loss += sell_amt * (1 - E.PRICE_N[g])
            amber_sales += sell_amt
    if hf_t0 > 0:
        amt = min(hf_t0, E.HF0)
        hf -= amt
        hf_q += amt * E.HF_SCHED[None, :]
    if ra is not None:
        ra_oil0 = ra.oil_delta(np.full(n, 70.0))
        if ra_on and cfg.enr_sell > 0:                  # ENR SELL into the Gulf-war bid at t0 (RA playbook)
            c_, v_ = ra.enr_sell(cfg.enr_sell, cfg.enr_bid)
            tre += c_
            ra_cash_t0 += c_
            enr_vgive += v_
        ra_oil_post = ra.oil_delta(np.full(n, 70.0))
    enc0 = E.IM_N * E.N_SYN0 + E.OPP_IM0
    top_up = max(0.0, reserve * E.NAV0 - (float(tre[0]) - enc0))
    if top_up > 0:
        a = min(top_up / 0.998, E.LO0["dm"])
        lo["dm"] -= a
        tre += a * 0.998
    up = rcf * pol.rcf_upfront + navf * pol.navf_upfront
    fees += up
    tre -= up

    def nav_of():
        return tre + sum(lo.values()) + hf + hf_q.sum(axis=1) + priv_nav_tot() - b_r - b_n \
            + (tail_mtm if cfg.overlay == "L1" else 0.0) + (ra.nav_true() if ra is not None else 0.0)

    tail_mtm = np.zeros(n)
    if cfg.overlay == "L1":
        tail_mtm = (TE_N * put_spread(1.0, 0.90, 0.70, (4 - TE_age[None, :]) / 4, 0.16)).sum(1) \
            + (TO_N * put_spread(1.0, 0.85, 0.65, (4 - TE_age[None, :]) / 4, 0.35, skew=0.5, r=0.0)).sum(1)

    bump = getattr(cfg, "bump", None)       # (group, $bn per year in year 1) for reduced-H finite differences
    tau0 = 2026.75
    for t in range(T_Q):
        tau = tau0 + 0.25 * t
        yr = t // 4
        # ---------------- fiscal-year basis (opening reported NAV, annual reset)
        if t % 4 == 0:
            basis = priv_rep_tot() + tre + sum(lo.values()) + hf + hf_q.sum(axis=1) - b_r - b_n
            budget_rem = np.full(n, cfg.budget)
        # ---------------- regimes
        z_prev = z
        z = (rng.random(n)[:, None] > cdfZ[z]).sum(axis=1)
        enter_db = (z == 3) & (z_prev != 3)
        stay = np.where(z == 3, 0.90, 0.75)
        p_enter = np.minimum(0.95, m.crisis_entry * E.KAPPA_CRISIS[z])
        u = rng.random(n)
        crisis_prev = crisis
        crisis = np.where(enter_db, u < 0.85, np.where(crisis, u < stay, u < p_enter))
        onset = crisis & ~crisis_prev
        cdur = np.where(crisis, cdur + 1, 0)
        since_exit = np.where(crisis, 0, np.where(crisis_prev & ~crisis, 1, since_exit + 1))
        ue = rng.random(n)
        o_row = np.where(ue < 0.85, 0, np.where(ue < 0.98, 1, 2))
        n_row = np.where(ue < 0.05, 0, np.where(ue < 0.89, 1, 2))
        d_up = 1 - m.d_stay
        d_row = np.where(ue < 0.1 * d_up, 0, np.where(ue < d_up, 1, 2))
        f_row = np.where(ue < 0.6, 2, 1)
        e_new = np.where(e == 0, o_row, np.where(e == 1, n_row, np.where(e == 2, d_row, f_row)))
        uf = rng.random(n)
        e = np.where(crisis, np.where((e == 3) | (uf < 0.8), 3, 2), e_new)
        recv = (~crisis) & (since_exit <= 4)
        if t < 8:
            wrongway |= (z == 2) | (z == 3)

        # ---------------- market returns
        zz = rng.standard_normal(n)
        drift = mu_calm + (m.repricing_drift if t < m.repricing_q else 0.0) \
            + np.where(since_exit <= E.REBOUND_Q, E.REBOUND_ADD, 0.0)
        c_mu, c_sd = E.crisis_mu_sd(cdur)
        r_eq = np.where(crisis, c_mu + c_sd * zz, drift + E.EQ_CALM_SD * zz)
        r_eq = np.maximum(r_eq, -0.6)
        r_em = 1.2 * r_eq + 0.04 * rng.standard_normal(n)
        r_fi = np.where(crisis, m.fi_crisis_q, m.fi_g / 4) + 0.02 * (0.3 * zz + 0.95 * rng.standard_normal(n))
        r_tre = np.where(crisis, 0.4 * E.CASH_Q + 0.27 * m.ust_crisis_q + 0.33 * (-0.005), 0.0100)
        r_hf = E.CASH_Q + 0.3 * (r_eq - E.CASH_Q) + alpha_hf / 4 + np.where(crisis, -0.02, 0.0) \
            + 0.025 * rng.standard_normal(n)
        nav_start = nav_of()
        if ra is not None:
            ra_vt0, ra_va0, ra_vs0 = ra.vt().copy(), ra.va().copy(), ra.vs().copy()
        if cfg.track:
            nav_start_g = {"PE": group_nav("pe"), "SEC": group_nav("sec"), "CS": group_nav("cs"),
                           "CO": group_nav("co"), "PC": group_nav("pc"),
                           "PM": sum(lo.values()) + hf + hf_q.sum(1), "OVL": tail_mtm.copy(),
                           "TPA": np.zeros(n), "CF": tre - b_r - b_n,
                           "RA": (ra.nav_true() if ra is not None else np.zeros(n))}
            cash_q = {g: np.zeros(n) for g in ACC}
        tre *= 1 + r_tre
        lo_prev = {k: v.copy() for k, v in lo.items()}
        lo["dm"] *= 1 + r_eq
        lo["em"] *= 1 + r_em
        lo["fi"] *= 1 + r_fi
        hf *= 1 + r_hf
        hf_q *= (1 + r_hf)[:, None]
        bh["tre"] *= 1 + r_tre
        bh["dm"] *= 1 + r_eq
        bh["em"] *= 1 + r_em
        bh["fi"] *= 1 + r_fi
        bh["hf"] *= 1 + r_hf
        eq_lvl = eq_lvl * (1 + r_eq)
        eq_hist = eq_hist[1:] + [eq_lvl.copy()]
        dd = 1 - eq_lvl / np.maximum.reduce(eq_hist)
        # discount and desk quote (separate stream)
        disc_x = 0.5 * disc_x + math.sqrt(0.75) * rng_f.standard_normal(n)
        disc = np.clip(DISC_BAR[e] + 0.25 * dd + 0.10 * crisis + 0.03 * disc_x, 0.02, 0.60)
        dhat = disc + cfg.desk_sd * rng_f.standard_normal(n)
        # oil (gap_04 / C3 dynamics, quarterly)
        zo = rng_f.standard_normal(n)
        mu_z = np.array([0, .20, -.35, -.45, .30, .10])[z]
        sg_z = np.array([.20, .20, .20, .25, .25, .30])[z]
        jump = (z == 5) & (rng_f.random(n) < 0.25 / 4)
        jsign = np.where(rng_f.random(n) < 0.5, 0.26, -0.26)
        oil_prev = oil
        oil = np.exp(np.log(oil) + (1 - 0.6 ** 0.25) * (np.log(70) - np.log(oil)) + mu_z / 4
                     + sg_z / 2 * zo + jump * jsign)
        if ra is not None:
            ra.returns(r_eq, E.CASH_Q, crisis, z, oil, oil_prev)
        base_r = {b: E.CASH_Q + b * (r_eq - E.CASH_Q) for b in (0.3, 0.5, 0.9, 1.0, 1.1, 1.3, 1.5)}
        if rate_mode:
            for g in E.PRIV0:
                econ = E.CASH_Q + E.BETA[g] * (r_eq - E.CASH_Q) + alpha[g] / 4 + np.where(crisis & (g == "pc"),
                                                                                          -0.02, 0.0)
                priv[g] *= 1 + econ
                rep[g] *= 1 + (0.5 * econ + 0.5 * econ_prev[g])
                econ_prev[g] = econ
        else:
            # PE vintages (book-level idiosyncratic noise 3% a year beyond GP and vintage effects [I])
            pe_eps = rng_c.standard_normal(n)
            sec_eps = rng_c.standard_normal(n)
            econ = base_r[1.1][:, None] + (alpha["pe"] + pe_gp_alpha[:, None] + u_v) / 4 + 0.015 * pe_eps[:, None]
            PE_N *= 1 + econ
            PE_R *= 1 + 0.5 * econ + 0.5 * PE_eprev
            PE_eprev = econ
            # Secondaries
            ec = base_r[0.9] + alpha["sec"] / 4 + 0.015 * sec_eps
            SN1 *= 1 + ec; SN3 *= 1 + ec
            SR1 *= 1 + 0.5 * ec + 0.5 * s_eprev; SR3 *= 1 + 0.5 * ec + 0.5 * s_eprev
            s_eprev = ec
            ecv = base_r[1.5] + alpha_cv / 4 + 0.03 * sec_eps
            SN4 *= 1 + ecv
            SR4 *= 1 + 0.5 * ecv + 0.5 * s_eprev_cv
            s_eprev_cv = ecv
            ecc = base_r[1.1] + (alpha["pe"] + pe_gp_alpha) / 4
            SNc *= 1 + ecc
            SRc *= 1 + 0.5 * ecc + 0.5 * s_eprev_c
            s_eprev_c = ecc
            # Co-investment companies (EV engine) and new-deal cohorts
            eps = rng_c.standard_normal((n, CO_N))
            jmp = rng_c.random((n, CO_N)) < (0.02 + 0.04 * crisis[:, None])
            jsz = np.where(jmp, -0.25 + 0.15 * rng_c.standard_normal((n, CO_N)), 0.0)
            lr = (E.CASH_Q + CO_BETA_A * (r_eq - E.CASH_Q))[:, None] + (alpha_A + co_gam + co_eta) / 4 \
                - 0.5 * CO_SIG_ID ** 2 / 4 + CO_SIG_ID / 2 * eps + jsz
            co_v = co_v * np.exp(lr)
            co_age = co_age + 0.25
            NEW_age = np.maximum(0.0, (t + 1) * 0.25 - np.arange(6) * 1.0 - 0.375)
            enew = base_r[1.3][:, None] + (alpha_E + new_gam[:, None]) / 4 \
                + 0.12 / 2 * rng_c.standard_normal((n, 6))
            NEWN *= 1 + enew
            NEWR *= 1 + 0.5 * enew
            # Capital Solutions marks
            cs_mark_prev = cs_mark
            cs_mark = 1 - 0.10 * crisis - 0.03 * ((e == 3) & ~crisis)
            pc_price_prev = pc_price
            pc_price = 1 - 0.12 * crisis - 0.04 * ((e == 3) & ~crisis) - 0.01 * (e == 2)

        # ---------------- private cash flows
        mD = np.array([1.25, 1.0, 0.50, m.md_f])[e]
        mC = np.array([1.3, 1.0, 0.97, m.mc_f])[e]
        dist = np.zeros(n)
        calls = np.zeros(n)
        dist_g = {g: np.zeros(n) for g in GKEYS}
        calls_g = {g: np.zeros(n) for g in GKEYS}
        recap_div = np.zeros(n)
        recap_pc = np.zeros(n)
        if rate_mode:
            for g in ("pe", "sec", "co"):
                d = E._q(np.minimum(0.95, E.DIST_NORMAL[g] * mD * m.phi)) * priv[g]
                priv[g] -= d
                rep[g] -= d
                dist += d
                dist_g[g] += d
            mDc = np.array([1.05, 1.0, 0.92, 0.57])[e]
            for g in ("cs", "pc"):
                d = E._q(E.DIST_NORMAL[g] * mDc) * priv[g]
                priv[g] -= d
                rep[g] -= d
                dist += d
                dist_g[g] += d
            cq = E._q(np.minimum(0.95, E.CALL_BASE * mC))
            for g in unf0:
                c = cq * unf[g]
                if g == "pe":
                    c = c + np.where(onset, 0.05 * unf[g], 0.0)
                c = np.minimum(c, unf[g])
                unf[g] -= c
                priv[g] += c
                rep[g] += c
                calls += c
                calls_g[g] += c
            c = np.full(n, sec_def0 / 4 if t < 4 else 0.0)
            sec_def -= c
            priv["sec"] += c
            rep["sec"] += c
            calls += c
            calls_g["sec"] += c
            c = np.minimum(pc_rev, np.where(onset, 0.5 * pc_rev, E._q(0.15) * pc_rev))
            pc_rev -= c
            priv["pc"] += c
            rep["pc"] += c
            calls += c
            calls_g["pc"] += c
        else:
            # PE vintages
            age = tau - (VINT + 0.5)
            rd, cr = pe_rates(age, L_pe)
            qd = qr(rd[None, :] * (mD * m.phi)[:, None])
            qc = qr(cr[None, :] * mC[:, None])
            dpe = qd * PE_N
            cpe = np.minimum(qc * PE_U + np.where(onset, 0.05, 0.0)[:, None] * PE_U, PE_U)
            PE_N += cpe - dpe
            PE_R = np.maximum(PE_R + cpe - dpe, 0.0)
            PE_U -= cpe
            dist_g["pe"] += dpe.sum(1); calls_g["pe"] += cpe.sum(1)
            pe_dist_rate = dpe.sum(1) / np.maximum(PE_N.sum(1) + dpe.sum(1) - cpe.sum(1), 1e-9) * 4
            # Secondaries
            d1 = qr(0.25 * mD * m.phi) * SN1; d3 = qr(0.30 * mD * m.phi) * SN3
            dcv = qr(0.154 * MX[e]) * SN4
            dc = qr(0.30 * mD * m.phi) * SNc
            c1 = qr(0.45 * mC) * SU1; ccn = qr(0.30 * mC) * SUc
            SN1 += c1 - d1; SR1 = np.maximum(SR1 + c1 - d1, 0); SU1 -= c1
            SN3 -= d3; SR3 = np.maximum(SR3 - d3, 0)
            SN4 -= dcv; SR4 = np.maximum(SR4 - dcv, 0)
            SNc += ccn - dc; SRc = np.maximum(SRc + ccn - dc, 0); SUc -= ccn
            sdef = np.minimum(sec_def, sec_def0 / 4) if t < 4 else np.zeros(n)
            sec_def = sec_def - sdef
            SN1 += sdef; SR1 += sdef
            dist_g["sec"] += d1 + d3 + dcv + dc
            calls_g["sec"] += c1 + ccn + sdef
            cont_in_q = dc - ccn
            # Capital Solutions
            pik_k = np.where(crisis, 0.70, np.where(recv, 0.20, np.array([0.15, 0.15, 0.30, 0.50])[e]))
            pik_c = np.where(crisis, 0.15, 0.0)
            pik_n = np.where(crisis, 0.70, np.where(e == 3, 0.50, 0.30))
            pd_base = np.where(crisis, 0.07, np.where(recv, 0.015, CS_PD[e]))
            lgd_cr = lambda L: np.where(crisis, 1 - 0.7 * (1 - L), L)  # noqa: E731
            inc_c = CC * CS_Y[0] / 4; inc_k = CK * CS_Y[1] / 4; inc_n = CN * 0.13 / 4
            cash_inc = inc_c * (1 - pik_c) + inc_k * (1 - pik_k) + inc_n * (1 - pik_n)
            CC += inc_c * pik_c; CK += inc_k * pik_k; CN += inc_n * pik_n
            dfc = qr(pd_base * 0.6) * CC; dfk = qr(pd_base * 1.4) * CK
            dfn = qr(np.where(crisis, 0.07, 0.03)) * CN
            rec_cs = dfc * (1 - lgd_cr(CS_LGD[0])) + dfk * (1 - lgd_cr(CS_LGD[1])) + dfn * (1 - lgd_cr(0.55))
            CC -= dfc; CK -= dfk; CN -= dfn
            rr = np.where(crisis, 0.03, np.where(recv, 0.15, CS_RR[e]))
            rr_c = rr * np.clip(pe_dist_rate / 0.20, 0.2, 1.5)       # NAV loans repay from PE distributions
            rpc = qr(rr_c) * CC; rpk = qr(rr) * CK
            CN_age = CN_age + 0.25
            rpn = np.where(CN_age > 1.0, qr(0.25), 0.0) * CN
            CC -= rpc; CK -= rpk; CN -= rpn
            ccs = qr(0.30 * mC) * CU
            CU -= ccs
            CC += CS_SPLIT_CP * ccs; CK += (1 - CS_SPLIT_CP) * ccs
            dist_g["cs"] += cash_inc + rec_cs + rpc + rpk + rpn
            calls_g["cs"] += ccs
            cs_cont_in_q = inc_n * (1 - pik_n) + dfn * (1 - lgd_cr(0.55)) + rpn
            cs_rep = 0.5 * cs_rep + 0.5 * (CC + CK + CN) * cs_mark_prev
            # Co-investment: write-offs, exits, recaps, follow-ons, new-deal exits
            eq_co = np.maximum(co_v - co_d, 0.0)
            wo = co_alive & (co_v < 0.85 * co_d)
            pc_loss = np.where(wo, pc_loan, 0.0)
            co_alive = co_alive & ~wo
            H = lambda a: (np.maximum(a, 0) / CO_WEIB_ETA) ** CO_WEIB_K  # noqa: E731
            hz = (H(co_age) - H(co_age - 0.25)) * np.where(crisis, 0.3, MX[e])[:, None]
            ex = co_alive & (rng_c.random((n, CO_N)) < 1 - np.exp(-hz))
            proceeds = np.where(ex, eq_co * np.exp(0.10 * rng_c.standard_normal((n, CO_N)) - 0.005), 0.0)
            co_alive = co_alive & ~ex
            pc_repaid = np.where(ex, pc_loan, 0.0)                    # loans refinanced at exit
            pr_q = np.where(crisis, 0.0, CO_RECAP_Q[e])[:, None]
            rc = co_alive & (co_age >= 2.0) & (co_d < 0.5 * co_v) & (rng_c.random((n, CO_N)) < pr_q)
            dd_ = np.where(rc, CO_RECAP_DD * co_d, 0.0)
            div = 0.98 * dd_
            co_d = co_d + dd_
            loan_new = np.where(rc & co_ovl, CO_OVERLAP_S * dd_, 0.0)
            pc_loan = np.where(wo | ex, 0.0, pc_loan + loan_new)
            recap_div = div.sum(1)
            recap_pc = loan_new.sum(1)
            fo = qr(0.25 * mC) * CO_U
            CO_U -= fo
            alive_eq = np.where(co_alive, np.maximum(co_v - co_d, 0.0), 0.0)
            tot_eq = np.maximum(alive_eq.sum(1), 1e-9)
            co_v = co_v + np.where(co_alive, (fo / tot_eq)[:, None] * alive_eq, 0.0)
            co_M = np.where(co_alive, 0.5 * co_M + 0.5 * np.maximum(co_v - co_d, 0.0), 0.0)
            hzn = (H(NEW_age) - H(NEW_age - 0.25))[None, :] * np.where(crisis, 0.3, MX[e])[:, None]
            exn = (1 - np.exp(-hzn)) * NEWN
            NEWR = np.maximum(NEWR - exn * NEWR / np.maximum(NEWN, 1e-9), 0.0)
            NEWN = NEWN - exn
            dist_g["co"] += proceeds.sum(1) + recap_div + exn.sum(1)
            calls_g["co"] += fo
            # Private Credit wrappers
            ss = np.where(crisis, 4, e)
            pik = np.where(crisis, 0.18, PC_PIK[e])
            pdv = PC_PD_N * np.where(crisis, 3.0, np.array([1.0, 1.0, 1.5, 2.0])[e])
            lgd = np.where(crisis, 1 - 0.7 * (1 - PC_LGD), PC_LGD)
            cpr = np.where(crisis, 0.065, PC_CPR[e])
            ovl_par = pc_loan.sum(1)
            pc_rec_cash = np.zeros(n)
            principal_ret = np.zeros(n)
            inc_cash = np.zeros(n)
            for w in ("sma", "cef", "evg", "bdc"):
                P = {"sma": PSMA, "cef": PCEF, "evg": PEVG, "bdc": PBDC}[w]
                base_par = np.maximum(P - (ovl_par if w == "sma" else 0.0), 0.0)
                inc = P * PC_COUPON / 4
                inc_cash += inc * (1 - pik)
                P = P + inc * pik
                dfl = qr(pdv) * base_par
                pc_rec_cash += dfl * (1 - lgd)
                P = P - dfl
                rp = qr(cpr) * np.maximum(P - (ovl_par if w == "sma" else 0.0), 0.0)
                if w == "sma":
                    sma_rp = rp      # SMA principal: run-off or reinvest, decided below with the stage
                elif w == "cef":
                    principal_ret += 0.5 * rp
                    P = P - 0.5 * rp
                if w == "sma":
                    PSMA = P
                elif w == "cef":
                    PCEF = P
                elif w == "evg":
                    PEVG = P
                else:
                    PBDC = P
            # overlap loans: shared defaults with co-investment write-offs; repaid at exits; new recap loans
            pc_rec_cash += 0.33 * pc_loss.sum(1)
            PSMA = PSMA - pc_loss.sum(1) - pc_repaid.sum(1) + recap_pc
            principal_ret += pc_repaid.sum(1)
            cpc = qr(np.where(crisis, 0.40, E.CALL_BASE * mC)) * PU
            PU -= cpc
            PCEF += cpc
            ddtl = np.minimum(pc_rev, np.where(onset, 0.5 * pc_rev, qr(np.where(crisis, 0.60, PC_DDTL[e])) * pc_rev))
            pc_rev = pc_rev - ddtl
            PSMA = PSMA + ddtl
            dist_g["pc"] += inc_cash + pc_rec_cash + principal_ret
            calls_g["pc"] += cpc + ddtl + recap_pc
            pc_rep = 0.5 * pc_rep + 0.5 * (PSMA + PCEF + PEVG + PBDC) * pc_price_prev
            dist = sum(dist_g.values())
            calls = sum(calls_g.values())

        # ---------------- Real Assets flows (ra_gap_01): income, exits, calls, maturities / cures, OE payments
        ra_q_cash = np.zeros(n)
        if ra is not None:
            ra_fl = ra.flows(e, crisis, z, oil, None, None)
            ra_in = ra_fl["dist"] + ra_fl["red"]
            ra_out = ra_fl["calls"] + ra_fl["cures"] + ra_fl["prot"] + ra_fl["co_cost"]
            dist = dist + ra_in
            calls = calls + ra_out
            ra_q_cash = ra_in - ra_out + (ra_cash_t0 if t == 0 else 0.0)
            ra_cure_q[:, t] = ra_fl["cure_cash"]
            ra_flow_q[:, t] = ra_fl["dist"] - ra_fl["calls"] - ra_fl["cures"] - ra_fl["prot"]
            ra_red_tot += ra_fl["red"]

        # ---------------- stage: t1 indicators and the CFP stage machine
        nav_now = nav_of()
        im_req = np.where(crisis, E.IM_S, E.IM_N) * n_syn
        opp_im = np.where(crisis & (m.opp_mult > 1), 2.0, 1.0) * E.OPP_IM0 * (opp_scale if cfg.overlay == "L1"
                                                                            else 1.0)
        enc = im_req + opp_im
        usable = tre - enc - (ring if cfg.trigger.startswith("ring") else 0.0)
        liq_share = (tre - enc + sum(lo.values()) + E.HF_CASH90 * hf + hf_q[:, 0]) / nav_now
        tre_share = (tre - enc) / nav_now
        stage = np.zeros(n, dtype=int)
        stage = np.maximum(stage, np.where(liq_share < 0.28, 1, 0))
        stage = np.maximum(stage, np.where(liq_share < 0.24, 2, 0))
        stage = np.maximum(stage, np.where(liq_share < 0.20, 3, 0))
        stage = np.maximum(stage, np.where(tre_share < 0.06, 1, 0))
        stage = np.maximum(stage, np.where(tre_share < 0.04, 2, 0))
        stage = np.maximum(stage, np.where(crisis, 1, 0))
        stage_t1 = stage
        need_cfp = (cfg.stage == "cfp") or cfg.track or cfg.trigger in ("current", "tier1only", "ring_t1")
        if need_cfp:
            ra_u_now = ra.unf_tot() if ra is not None else 0.0
            unf_tot = sum(group_unf(g) for g in GKEYS) + sec_def + pc_rev + ra_u_now
            pace_now = sum(pace_g.values())
            ra_pst = ra.proxy_state() if ra is not None else {}
            if cfg.overlay == "L1":
                xj = eq_lvl[:, None] / TE_S
                tail_stress = (TE_N * TE_live * np.clip(0.90 - xj * 0.624, 0, 0.20)).sum(1)
            else:
                tail_stress = np.full(n, E.N_TAIL * 0.18)
            navf_cap_now = np.minimum(navf, 0.05 * np.minimum(0.20 * priv_nav_tot(), group_rep("pe")
                                                              + group_rep("sec")))
            debt = b_r + b_n

            def cfp_eval(tre_eff, fac_eff):
                st = dict(tre=tre_eff, enc=enc, dm=lo["dm"], em=lo["em"], fi=lo["fi"], hf=hf, hf_q=hf_q,
                          priv={g: group_nav(g) for g in GKEYS}, unf=unf_tot - ra_u_now - sec_def - pc_rev,
                          sec_def=sec_def, sec_def0=sec_def0, pc_rev=pc_rev, basis=basis, n_syn=n_syn,
                          pace=pace_now, pace_cut=pol.pace_cut and on("PE"), band=band, tail_stress=tail_stress,
                          prem_m=E.TAIL_PREM * E.NAV0 / 12, nav=nav_now,
                          fee_m=np.maximum(rcf - b_r, 0) * pol.rcf_undrawn_fee / 12, fac=fac_eff, share=SH)
                if ra is not None:
                    st.update(ra_pst)
                    st.update(ra_cut=bool(cut_g.get("ra", False)), ra_avail=cfg.ra_avail, ra_ext=cfg.ra_ext,
                              ra_fund=cfg.ra_fund)
                sh_, shf_ = sh_tp_proxy(st, theta=cfg.theta)
                lcr_ = lcr30_proxy(tre_eff, enc, lo["dm"], nav_now, unf_tot, n_syn, np.where(band, 0.05, 0.10))
                ts_ = (tre_eff - enc) / nav_now
                ls_ = (tre_eff - enc + sum(lo.values()) + E.HF_CASH90 * hf + hf_q[:, 0]) / nav_now
                raw_ = np.maximum.reduce([band_of(sh_, (24, 18, 12)), band_of(lcr_, (2.0, 1.5, 1.0)),
                                          band_of(ts_, (0.08, 0.06, 0.04)), band_of(ls_, (0.28, 0.24, 0.20))])
                tier_ = (ts_ >= 0.08) & (lcr_ >= 1.0) & (shf_ >= 24)
                return raw_, tier_, sh_, shf_, lcr_, ts_

            def hyst(cur, cnt, raw_):
                if cur is None:
                    return raw_.copy(), np.zeros(n, dtype=int)
                up_ = raw_ > cur
                down = raw_ < cur
                cnt = np.where(down, cnt + 1, 0)
                new = np.where(up_, raw_, np.where(down & (cnt >= 2), cur - 1, cur))
                cnt = np.where(down & (cnt >= 2), 0, cnt)
                return new, cnt

            raw_g, tier_g, sh, shf, lcr, ts_g = cfp_eval(tre, np.maximum(rcf - b_r, 0.0) * 0.80 + navf_cap_now)
            stage_g, cfp_cnt = hyst(stage_g if t > 0 else None, cfp_cnt, raw_g)
            if cfg.track or cfg.stage_conv == "net":
                raw_n, tier_n, sh_n, shf_n, lcr_n, ts_n = cfp_eval(tre - debt, rcf * 0.80 + navf_cap_now)
                stage_n, cfp_cnt_n = hyst(stage_n if t > 0 else None, cfp_cnt_n if t > 0 else None, raw_n)
            else:
                stage_n, tier_n = stage_g, tier_g
            if cfg.stage_conv == "net":
                stage_cfp, tier1 = stage_n, tier_n
                t2 = ts_n >= 0.08
                t3 = lcr_n >= 1.0
                t4 = shf_n >= 24
            else:
                stage_cfp, tier1 = stage_g, tier_g
                t2 = ts_g >= 0.08
                t3 = lcr >= 1.0
                t4 = shf >= 24
        if cfg.stage == "cfp":
            stage_pol = stage_cfp
            amber_up = stage_cfp >= 1
            red_up = (stage_cfp >= 2) | crisis
        else:
            stage_pol = stage_t1
            amber_up = stage_t1 >= 1
            red_up = (stage_t1 >= 2) | crisis
        for s in range(4):
            stage_hist[t, s] += float((stage_pol == s).mean())
        # ---------------- RA playbook: open-end notices at Amber (paid through the queue from next quarter)
        if ra is not None and ra_on and cfg.ra_notices:
            ra.lodge_notices(amber_up)

        # ---------------- SMA principal: run-off (PC on, Amber+) or reinvest
        if not rate_mode:
            runoff = pc_runoff & amber_up
            sret = np.where(runoff, sma_rp, 0.0)
            PSMA = PSMA - sret
            dist_g["pc"] += sret
            dist = dist + sret

        # ---------------- new commitments (group pacing)
        k_g = {}
        for g in SH:
            k = np.full(n, pace_g[g] / 4)
            if cut_g[g]:
                if cfg.stage == "cfp":
                    k = np.where(stage_cfp >= 2, 0.25 * k, np.where(stage_cfp == 1, 0.375 * k, k))
                else:
                    k = np.where(amber_up, 0.25 * k, k)
            if g == "co" and co_pause and not rate_mode:
                k = np.where(amber_up, 0.0, k)
            fg = np.maximum(0.0, plan_g[g] / 4 - k)
            forgone_g[g] += fg
            commit_forgone += fg
            forgone_t[:, t] += fg
            if bump is not None and t < 4 and bump[0] == g and g not in ("co", "ra"):
                k = k + bump[1] / 4
            k_g[g] = k
        if ra is not None:
            ra.add_commitments(k_g["ra"])
            if bump is not None and t < 4 and str(bump[0]).startswith("ra_"):
                sid = {"ra_re": "RE_CE", "ra_inf": "INF_CE", "ra_enr": "ENR_CE"}[bump[0]]
                ra.U[:, ra.ids.index(sid)] += bump[1] / 4
        if rate_mode:
            for g in ("pe", "sec", "pc", "cs"):
                unf[g] += k_g[g]
            co_deal = k_g["co"]
            priv["co"] += co_deal
            rep["co"] += co_deal
        else:
            vi = int(math.floor(tau + 1e-9)) - 2012
            PE_U[:, vi] += k_g["pe"]
            pe_hist_arr = pe_hist_arr[1:] + [k_g["pe"]]
            SU1 += k_g["sec"]; CU += k_g["cs"]; PU += k_g["pc"]
            if cfg.links:
                offered = COFLOW_THETA * sum(dq[19 - j] * pe_hist_arr[j] for j in range(20)) * 1.0
                accepted = COFLOW_A * offered
                co_deal = np.minimum(k_g["co"], accepted)
            else:
                accepted = np.full(n, np.inf)
                co_deal = k_g["co"]
            if bump is not None and t < 4 and bump[0] == "co":
                co_deal = co_deal + bump[1] / 4
            NEWN[:, yr] += co_deal
            NEWR[:, yr] += co_deal
            calls_g["co"] = calls_g["co"] + co_deal      # group accounting; the net adds co_deal as t1 does

        # ---------------- owner draw (Mode B), opening reported NAV basis, quarterly instalments
        if t % 4 == 0:
            tgt_d = E.D_TGT[z] + 0.005 * rng.standard_normal(n)
            d_year = np.clip(0.5 * d_prev + 0.5 * tgt_d, 0.05, 0.10)
            ov = rng.random(n) < E.P_OV[z]
            if overrides:
                d_year = np.where(ov, 0.10 + rng.uniform(0.02, 0.035, n), d_year)
                override_year = ov
            d_prev = np.minimum(d_year, 0.10)
            if cfg.init == "gap04" and t == 0:
                d_year = np.full(n, D2026)
                override_year = np.zeros(n, dtype=bool)
                d_prev = np.minimum(d27, 0.10)
        if cfg.init == "gap04" and t == 1:
            d_year = d27
            override_year = ov27
        inst = d_year * basis / 4
        inst_mode_b = inst
        if band:
            cut = ((stage_pol >= 2) | crisis) & ~override_year
            new_inst = np.where(cut, 0.05 * basis / 4, inst)
            withheld += inst - new_inst
            if t < 4:
                band_active_12m |= cut & (new_inst < inst - 1e-12)
            inst = new_inst

        # ---------------- overlay
        spread = np.where(crisis, E.FUT_SPREAD_S, E.FUT_SPREAD_N)
        unit_vm = r_eq - E.CASH_Q - spread / 4
        vm = n_syn * unit_vm
        vm = np.where(crisis & (vm < 0), vm * m.vm_mult, vm)
        vm_mult_eff = np.where(crisis & (unit_vm < 0), m.vm_mult, 1.0)
        vm_tpa = n_tpa * unit_vm * vm_mult_eff
        vm_p2s = n_p2s * unit_vm * vm_mult_eff
        if cfg.overlay == "t1":
            prem = E.TAIL_PREM * E.NAV0 / 4
            tail = E.N_TAIL * np.clip(-r_eq - 0.10, 0.0, 0.18)
            opp = 0.0125 / 2 * E.NAV0 * rng.standard_normal(n) + np.where(crisis, -0.005, 0.001) * E.NAV0
            opp = np.where(crisis, opp * m.opp_mult, opp)
            mon_cash = tail
            exp_cash = np.zeros(n)
        else:
            z_opp = rng.standard_normal(n)        # keeps t1's stream aligned; used as residual noise
            sig_eq = np.where(crisis, 0.40, np.where(since_exit <= 4, 0.24, 0.16))
            sig_oil = np.where(crisis | (z == 2) | (z == 3), 0.55, 0.35)
            prem = np.zeros(n)
            mon_cash = np.zeros(n)
            exp_cash = np.zeros(n)
            # equity ladder
            for j in range(4):
                age_j = (TE_age[j] + t + 1) % 4          # quarters since strike after this quarter
                x = eq_lvl / TE_S[:, j]
                if age_j == 0:                           # expiry this quarter: intrinsic, then re-strike
                    pay = TE_N[:, j] * TE_live[:, j] * np.clip(0.90 - x, 0.0, 0.20)
                    exp_cash += pay
                    px = put_spread(1.0, 0.90, 0.70, 1.0, sig_eq)
                    TE_N[:, j] = prem_eq_q / px
                    TE_S[:, j] = eq_lvl
                    TE_live[:, j] = True
                    prem += prem_eq_q
                else:
                    if ovl_on:
                        mtm = TE_N[:, j] * put_spread(x, 0.90, 0.70, (4 - age_j) / 4, sig_eq)
                        mx = TE_N[:, j] * 0.20
                        sell = TE_live[:, j] & ((mtm >= 0.5 * mx) | ((stage_pol >= 2) & (mtm >= 0.25 * mx)))
                        mon_cash += np.where(sell, 0.99 * mtm, 0.0)
                        TE_live[:, j] &= ~sell
            # Brent ladder (oil liability hedge)
            for j in range(4):
                age_j = (TE_age[j] + t + 1) % 4
                if age_j == 0:
                    pay = TO_N[:, j] * TO_live[:, j] * np.clip(0.85 - oil / TO_S[:, j], 0.0, 0.20)
                    exp_cash += pay
                    px = put_spread(1.0, 0.85, 0.65, 1.0, sig_oil, skew=0.5, r=0.0)
                    TO_N[:, j] = prem_oil_q / px
                    TO_S[:, j] = oil_fwd(oil, 1.0)
                    TO_live[:, j] = True
                    prem += prem_oil_q
                else:
                    if ovl_on:
                        x = oil_fwd(oil, (4 - age_j) / 4) / TO_S[:, j]
                        mtm = TO_N[:, j] * put_spread(x, 0.85, 0.65, (4 - age_j) / 4, sig_oil, skew=0.5, r=0.0)
                        mx = TO_N[:, j] * 0.20
                        sell = TO_live[:, j] & ((mtm >= 0.5 * mx) | ((stage_pol >= 2) & (mtm >= 0.25 * mx)))
                        mon_cash += np.where(sell, 0.99 * mtm, 0.0)
                        TO_live[:, j] &= ~sell
            tail = mon_cash + exp_cash
            # opportunistic families (Level-1 exposures on the simulated factors)
            sv_scale = 0.15 if ovl_on else 1.0               # L1 vega floor caps short vol
            if ovl_on:
                opp_scale = np.where(stage_pol >= 2, 0.5, 1.0)
            else:
                opp_scale = np.ones(n)
            trend_sig = np.sign(eq_hist[-1] / np.maximum(eq_hist[0], 1e-9) - 1 + 1e-12)
            # signal uses the trailing four quarters known at the start of the quarter
            trend = 6.0 * trend_sig_prev * (r_eq - E.CASH_Q) + 6.0 * trend_sig_prev * (r_fi - E.CASH_Q) * 0.5
            trend_sig_prev = np.where(t >= 0, trend_sig, trend_sig_prev)
            carry = np.where(crisis, np.where(onset, -0.06, -0.02), 0.03 / 4) * 10.0
            rv = np.where(crisis, np.where(onset, -0.03, 0.0), 0.01 / 4) * 15.0
            svol = np.where(crisis, np.where(onset, -0.010, -0.002), 0.0025 / 4) * E.NAV0 * sv_scale
            resid = 0.0005 / 4 * E.NAV0 + 0.5 * z_opp
            opp = (trend + carry + rv + svol + resid) * opp_scale
            opp = np.where(crisis & (opp < 0), opp * m.opp_mult, opp)
            # tail book MTM (for NAV)
            tail_mtm_new = np.zeros(n)
            for j in range(4):
                age_j = (TE_age[j] + t + 1) % 4
                tail_mtm_new += TE_N[:, j] * TE_live[:, j] * put_spread(eq_lvl / TE_S[:, j], 0.90, 0.70,
                                                                        (4 - age_j) / 4, sig_eq)
                tail_mtm_new += TO_N[:, j] * TO_live[:, j] * put_spread(
                    oil_fwd(oil, (4 - age_j) / 4) / TO_S[:, j], 0.85, 0.65, (4 - age_j) / 4, sig_oil, skew=0.5,
                    r=0.0)
        d_im = im_req - im_prev
        im_prev = im_req

        # ---------------- facility costs
        f_cost = np.maximum(rcf - b_r, 0.0) * pol.rcf_undrawn_fee / 4 + np.maximum(navf - b_n, 0.0) \
            * pol.navf_undrawn_fee / 4
        if t == 12:
            f_cost = f_cost + rcf * pol.rcf_upfront
        i_cost = b_r * (E.SOFR + pol.rcf_margin) / 4 + b_n * (E.SOFR + pol.navf_margin
                                                              + np.where(crisis, pol.navf_stress_add, 0.0)) / 4
        fees += f_cost
        interest += i_cost
        opex = 0.001 / 4 * nav_start

        net = inst + calls + co_deal + prem + f_cost + i_cost + opex - dist - vm - tail - opp
        tre -= net
        tail_cash_q = tail - prem
        if cfg.overlay == "L1":
            tail_mtm = tail_mtm_new
        if cfg.trigger.startswith("ring"):
            share_rf = 0.5 if cfg.trigger == "ring50" else 1.0      # ring100 and ring_t1 take all tail cash
            add = share_rf * np.maximum(tail, 0.0)
            ring_age = np.concatenate([ring_age[:, 1:], add[:, None]], axis=1)
            ring = ring_age.sum(1)
        if t < 8 and rate_mode:
            step = net - f_cost - i_cost + np.maximum(d_im, 0.0)
            netneed8 += step
            vm0 = E.N_SYN0 * (r_eq - E.CASH_Q - spread / 4)
            vm0 = np.where(crisis & (vm0 < 0), vm0 * m.vm_mult, vm0)
            d_im0 = (np.where(crisis, E.IM_S, E.IM_N) - np.where(crisis_prev, E.IM_S, E.IM_N)) * E.N_SYN0
            nco_bh += (inst_mode_b + calls + co_deal + prem + opex - dist - vm0 - tail - opp
                       + np.maximum(d_im0, 0.0))
            due_bh = hf_bh_q[:, 0].copy()
            paid_bh = np.where(crisis, hf_gate_pass * due_bh, due_bh)
            hf_bh_q[:, :-1] = hf_bh_q[:, 1:]
            hf_bh_q[:, -1] = 0.0
            hf_bh_q[:, 0] += due_bh - paid_bh
            hf_bh_q *= (1 + r_hf)[:, None]
            hf_bh_cash += paid_bh
            cbc_t = ((bh["tre"] - E.IM_N * E.N_SYN0 - E.OPP_IM0) * (1 - 0.038) + bh["dm"] * 0.985
                     + bh["fi"] * 0.95 + bh["em"] * 0.95 + hf_bh_cash)
            nav_bh = sum(bh.values()) + sum(priv.values()) - nco_bh \
                + (ra.nav_true() if ra is not None else 0.0)
            gap_t = nco_bh + 0.04 * nav_bh - cbc_t
            gstar = np.maximum(gstar, gap_t)
        if t == 7:
            tp_bh8 = sum(bh.values())

        # ---------------- hedge-fund queue
        due = hf_q[:, 0].copy()
        paid_hf = np.where(crisis, hf_gate_pass * due, due)
        rolled = due - paid_hf
        hf_q[:, :-1] = hf_q[:, 1:]
        hf_q[:, -1] = 0.0
        hf_q[:, 0] += rolled
        tre += paid_hf
        if hf_amber:
            file = np.where(amber_up, 0.5 * hf, 0.0)
            hf -= file
            hf_q += file[:, None] * E.HF_SCHED[None, :]

        # ---------------- NAV facility: LTV cut -> forced paydown
        pool = np.maximum(np.minimum(0.20 * priv_nav_tot(), group_rep("pe") + group_rep("sec")), 1e-9)
        ltv_cap = np.where(crisis, 0.05, 0.10)
        if t < 4:
            navf_trig_12m |= (b_n > 1e-9) & (b_n / pool > 0.15)
        fp = np.maximum(0.0, b_n - ltv_cap * pool)
        b_n -= fp
        tre -= fp
        forced_paydown += fp

        # ---------------- RA playbook: cash-out at maturity on controlled debt (Amber, not crisis)
        if ra is not None and ra_on and cfg.ra_cashout:
            co_cash = ra.cashout((stage_pol == 1) & ~crisis, e)
            tre += co_cash
            ra_q_cash = ra_q_cash + co_cash
            ra_co_tot += co_cash

        # ---------------- waterfall
        rf = ring if cfg.trigger.startswith("ring") else 0.0
        nav_now = nav_of()
        usable = tre - enc - rf
        target = reserve * nav_now
        floor = pol.floor_hard * nav_now
        need = np.maximum(0.0, target - usable)
        lo_sold = np.zeros(n)
        room = np.maximum(0.0, np.minimum(0.30 * nav_now, pol.p2s_cap) - n_syn)
        p2s_net = 0.998 - E.IM_N
        if p2s_on:
            a = np.where(~crisis, np.minimum(np.minimum(0.5 * lo["dm"], room), need / p2s_net), 0.0)
        else:
            a = np.zeros(n)
        lo["dm"] -= a
        n_p2s = n_p2s + a
        n_syn = n_tpa + n_p2s
        tre += a * 0.998
        enc = enc + a * E.IM_N
        im_prev = im_prev + a * E.IM_N
        need = need - a * p2s_net
        lo_sold += a * 0.998
        for key, cap, pn, pc_ in (("dm", 0.5, 0.998, 0.985), ("fi", 0.5, 0.995, 0.95), ("em", 0.5, 0.99, 0.95)):
            price = np.where(crisis, pc_, pn)
            a = np.minimum(np.maximum(cap * lo[key], 0.0), need / price)
            lo[key] -= a
            tre += a * price
            need = need - a * price
            lo_sold += a * price
        use_fac = red_up | ((tre - enc - rf) < 0.06 * nav_now)
        if rcf > 0:
            avail_f = np.where(crisis, np.where((z == 3) | (z == 5), 0.80, 0.90), 1.0)
            cap_debt = np.maximum(0.0, pol.debt_cap * nav_now - b_r - b_n)
            avail = np.maximum(0.0, np.minimum(rcf * avail_f - b_r, cap_debt))
            dr = np.where(use_fac, np.minimum(avail, need), 0.0)
            b_r += dr
            tre += dr
            need = need - dr
        if navf > 0:
            cap_debt = np.maximum(0.0, pol.debt_cap * nav_now - b_r - b_n)
            avail = np.maximum(0.0, np.minimum(np.minimum(navf, ltv_cap * pool) - b_n, cap_debt))
            dr = np.where(use_fac, np.minimum(avail, need / 0.985), 0.0)
            b_n += dr
            tre += dr * 0.985
            fees += dr * 0.015
            need = need - dr * 0.985
        usable = tre - enc - rf
        need_amber = np.maximum(0.0, np.where(red_up, 0.06, pol.floor_hard + 0.01) * nav_now - usable)
        sale_cash = {g: np.zeros(n) for g in GKEYS}
        for g in ("pc", "cs"):
            if not amber_on[g]:
                continue
            if rate_mode:
                pr = np.where(crisis, E.PRICE_C[g], E.PRICE_N[g])
                amt = np.minimum(0.10 * priv[g], need_amber / pr)
                frac = amt / np.maximum(priv[g], 1e-9)
                priv[g] -= amt
                rep[g] -= amt
                unf[g] *= 1 - frac
            else:
                if g == "pc":       # SMA performing loans near par (groups s3.6)
                    pr = np.where(crisis, 0.85, np.where(e == 3, 0.96, 0.99))
                    amt = np.minimum(0.10 * PSMA * pc_price, need_amber / pr)
                    frac = amt / np.maximum(PSMA * pc_price, 1e-9)
                    PSMA = PSMA * (1 - frac)
                    pc_loan = pc_loan * (1 - frac)[:, None]
                    pc_rep = pc_rep - amt
                else:
                    pr = np.where(crisis, E.PRICE_C[g], E.PRICE_N[g])
                    amt = np.minimum(0.10 * group_rep(g), need_amber / pr)
                    sell_group(g, amt)
            tre += amt * pr
            need_amber = need_amber - amt * pr
            amber_sales += amt
            amber_loss += amt * (1 - pr)
            sale_cash[g] += amt * pr
        if ra is not None and ra_on and cfg.ra_jv:           # pre-arranged JV sell-down (partial SELL)
            jv_cash, jv_v, jv_amt = ra.jv_selldown(np.maximum(need_amber, 0.0), e, crisis)
            tre += jv_cash
            need_amber = need_amber - jv_cash
            amber_sales += jv_amt
            amber_loss += jv_amt - jv_cash
            ra_q_cash = ra_q_cash + jv_cash
            ra_jv_tot += jv_cash
        usable = tre - enc - rf
        need_floor = np.maximum(0.0, floor - usable)
        depth = np.where(crisis, 2.5, 4.0)
        ok = rng_p.random(n) < np.where(crisis, E.P_SUCC_C, E.P_SUCC_N)
        for g in ("sec", "pe", "co"):
            pr = np.where(crisis, E.PRICE_C[g], E.PRICE_N[g])
            if rate_mode:
                amt = np.where(ok, np.minimum(np.minimum(priv[g], depth), need_floor / pr), 0.0)
                frac = amt / np.maximum(priv[g], 1e-9)
                priv[g] -= amt
                rep[g] -= amt
                unf[g] *= 1 - frac
            else:
                amt = np.where(ok, np.minimum(np.minimum(group_rep(g), depth), need_floor / pr), 0.0)
                sell_group(g, amt)
            tre += amt * pr
            need_floor = need_floor - amt * pr
            depth = depth - amt
            red_sales += amt
            red_loss += amt * (1 - pr)
            sale_cash[g] += amt * pr
        if ra is not None:                                    # forced RA stake / asset sales (remain in baseline)
            rc_, ramt, _ = ra.red_sale(np.maximum(need_floor, 0.0), e, crisis, depth, ok)
            tre += rc_
            need_floor = need_floor - rc_
            depth = depth - ramt
            red_sales += ramt
            red_loss += ramt - rc_
            ra_q_cash = ra_q_cash + rc_
            ra_forced += rc_
        attempted = np.maximum(0.0, floor - usable) > 1e-6
        first_red = np.where(attempted & (first_red < 0), t + 1, first_red)
        red |= attempted
        floor4_breach |= (tre - enc - rf) < floor - 1e-6
        usable = tre - enc - rf
        short = np.maximum(0.0, -usable)
        if cfg.trigger.startswith("ring"):          # the ring-fence yields before a payout shortfall
            rel = np.minimum(short, ring)
            ring_age = ring_age * (1 - rel / np.maximum(ring, 1e-9))[:, None]
            ring = ring_age.sum(1)
            short = short - rel
        short_pay = np.minimum(short, inst)
        resid = short - short_pay
        is_short = short > 1e-6
        black |= is_short
        red |= is_short
        if t < 4:
            black_12m |= is_short
        first_red = np.where(is_short & (first_red < 0), t + 1, first_red)
        tre += short_pay
        shortfall += short_pay
        if np.any(resid > 1e-9):
            ra_tot = np.maximum(ra.nav_true(), 0.0) if ra is not None else 0.0
            if rate_mode:
                tot_priv = np.maximum(sum(priv.values()) + ra_tot, 1e-9)
                sold = np.minimum(resid / 0.5, tot_priv)
                for g in E.PRIV0:
                    share = priv[g] / tot_priv
                    priv[g] -= sold * share
                    rep[g] -= sold * share
                    unf[g] *= 1 - np.minimum(1.0, sold / tot_priv)
            else:
                tot_priv = np.maximum(priv_nav_tot() + ra_tot, 1e-9)
                sold = np.minimum(resid / 0.5, tot_priv)
                for g in GKEYS:
                    share = group_nav(g) / tot_priv
                    rp = group_rep(g)
                    gnav = np.maximum(group_nav(g), 1e-9)
                    sell_group(g, sold * share * rp / gnav)
                    sale_cash[g] += sold * share * 0.5
            if ra is not None:
                ra.emergency(np.minimum(1.0, np.where(resid > 1e-9, sold / tot_priv, 0.0)))
                ra_q_cash = ra_q_cash + sold * (ra_tot / tot_priv) * 0.5
                ra_forced += sold * (ra_tot / tot_priv) * 0.5
            tre += sold * 0.5
            red_sales += sold
            red_loss += sold * 0.5
        paid_fv += (inst - short_pay) * 1.10 ** ((E.T_Q - t - 1) / 4)

        # ---------------- contingent budgets (Secondaries buying + Capital Solutions new money)
        deploy = np.zeros(n)
        if cfg.trigger != "none" and (sec_cont or cs_cont) and not rate_mode:
            nav_now = nav_of()
            usable_g = tre - enc - (ring if cfg.trigger.startswith("ring") else 0.0)
            hot = dhat > 0.20
            if cfg.trigger == "current":
                cond = hot & tier1 & (stage_cfp <= 1)
                cap = np.maximum(0.0, usable_g - 0.08 * nav_now)
            elif cfg.trigger == "tier1only":          # drop the stage condition, keep Tier 1 green
                cond = hot & tier1 & (stage_cfp <= 2)
                cap = np.maximum(0.0, usable_g - 0.08 * nav_now)
            elif cfg.trigger == "ring_t1":            # ring-fenced tail cash, deployable in Red if Tier 1 green
                cond = hot & tier1 & (stage_pol <= 2) & ~is_short
                cap = np.minimum(ring, np.maximum(0.0, tre - enc - 0.05 * nav_now))
            elif cfg.trigger.startswith("ring"):
                cond = hot & (stage_pol <= 2) & ~is_short
                cap = np.minimum(ring, np.maximum(0.0, tre - enc - 0.05 * nav_now))
            else:   # ungated
                cond = hot & ~is_short
                cap = np.maximum(0.0, tre - enc - 0.05 * nav_now)
            amt_tot = np.where(cond, np.minimum(np.minimum(budget_rem, cfg.budget / 2), cap), 0.0)
            amt_tot = amt_tot * (cont_share["sec"] + cont_share["cs"])
            budget_rem = budget_rem - amt_tot
            a_sec = amt_tot * cont_share["sec"] / max(cont_share["sec"] + cont_share["cs"], 1e-9)
            a_cs = amt_tot - a_sec
            # Secondaries: buy reference NAV at the clearing price 1 - disc; economic value acquired is the
            # market staleness ratio (PE econ / reported) times the quality haircut
            pr = 1 - disc
            stale = np.clip(PE_N.sum(1) / np.maximum(PE_R.sum(1), 1e-9), 0.5, 1.2)
            nref = a_sec / pr
            SNc += cfg.theta_q * stale * nref
            SRc += nref
            SUc += 0.08 * nref
            # Capital Solutions: new money at crisis terms, 2% OID
            CN_age = np.where(a_cs > 0, (CN_age * CN + 0.0 * a_cs) / np.maximum(CN + a_cs, 1e-9), CN_age)
            CN += a_cs / 0.98
            tre -= amt_tot
            deploy = amt_tot
            calls_g["sec"] = calls_g["sec"] + a_sec
            calls_g["cs"] = calls_g["cs"] + a_cs
            if cfg.trigger.startswith("ring"):
                used = np.minimum(amt_tot, ring)
                ring_age = ring_age * (1 - used / np.maximum(ring, 1e-9))[:, None]
                ring = ring_age.sum(1)
            if cfg.track:
                rec["cont_out"] += amt_tot * (1 + E.CASH_Q) ** (E.T_Q - t - 1)
                rec["cont_out_sec"] += a_sec
                rec["cont_out_cs"] += a_cs

        # ---------------- repayments in calm Green quarters
        nav_now = nav_of()
        usable = tre - enc
        if repay_on:
            excess = np.where(~crisis & (stage_pol == 0), np.maximum(0.0, usable - (reserve + 0.02) * nav_now), 0.0)
            rp_ = np.minimum(b_n, excess)
            b_n -= rp_
            tre -= rp_
            excess = excess - rp_
            rp_ = np.minimum(b_r, excess)
            b_r -= rp_
            tre -= rp_

        # ---------------- TPA synthetic-beta rule for next quarter (economic leverage monotone in the cushion)
        if tpa_on and cfg.overlay == "L1":
            n_tpa = np.select([stage_pol == 0, stage_pol == 1, stage_pol == 2], [12.5, 10.0, 5.0], 0.0)
        n_syn = n_tpa + n_p2s

        # ---------------- monitoring
        nav_now = nav_of()
        nav_min = np.minimum(nav_min, nav_now)
        debt_ratio = (b_r + b_n) / np.maximum(nav_now, 1e-9)
        max_debt_ratio = np.maximum(max_debt_ratio, debt_ratio)
        covenant_trig |= debt_ratio > pol.rcf_covenant
        enc_share = (enc + np.where(b_n > 1e-9, pool, 0.0)) / np.maximum(nav_now + b_r + b_n, 1e-9)
        max_enc = np.maximum(max_enc, enc_share)
        below8 = (tre - enc) < 0.08 * nav_now
        below8_streak = np.where(below8 & ~crisis, below8_streak + 1, 0)
        restore_fail |= below8_streak > 4

        # ---------------- Real Assets attribution ledger (ra_gap_01): DVA on V*, V^A and V^T
        if ra is not None:
            vT1, vA1, vS1 = ra.vt(), ra.va(), ra.vs()
            q_dva = ra_q_cash - (ra_cash_t0 if t == 0 else 0.0)    # the t0 ENR SELL is booked as a sale P&L below
            fb_desm = E.CASH_Q + beta_desm[None, :] * (r_eq - E.CASH_Q)[:, None]
            fb_obs = E.CASH_Q + beta_obs[None, :] * (r_eq - E.CASH_Q)[:, None]
            sale_T = (ra_cash_t0 - enr_vgive) if t == 0 else 0.0
            sale_A = (ra_cash_t0 - (cfg.enr_sell if (ra_on and cfg.enr_sell > 0) else 0.0)) if t == 0 else 0.0
            dT = vT1.sum(1) - ra_vt0.sum(1) + q_dva + sale_T
            dA = vA1.sum(1) - ra_va0.sum(1) + q_dva + sale_A
            dS = vS1.sum(1) - ra_vs0.sum(1) + q_dva + sale_T
            ra_dva["true_desm"][:, yr] += dT - (ra_vt0 * fb_desm).sum(1)
            ra_dva["star_desm"][:, yr] += dS - (ra_vs0 * fb_desm).sum(1)
            ra_dva["star_obs"][:, yr] += dS - (ra_vs0 * fb_obs).sum(1)
            ra_dva["rep_obs"][:, yr] += dA - (ra_va0 * fb_obs).sum(1)
            ra_dva["rep_desm"][:, yr] += dA - (ra_va0 * fb_desm).sum(1)
            fb_true = E.CASH_Q + ra.beta_eq[None, :] * (r_eq - E.CASH_Q)[:, None]
            ra_dva["true_b1"][:, yr] += dT - (ra_vt0 * fb_true).sum(1)
            ra_cash_y[:, yr] += ra_q_cash
            if t % 4 == 3:
                ra_navT_y[:, yr], ra_navA_y[:, yr], ra_navS_y[:, yr] = vT1.sum(1), vA1.sum(1), vS1.sum(1)

        if cfg.track:
            rec["stage_cfp"][:, t] = stage_cfp
            rec["stage_t1"][:, t] = stage_t1
            rec["stage_pol"][:, t] = stage_pol
            rec["stage_gross"][:, t] = stage_g
            rec["stage_net"][:, t] = stage_n
            rec["tier1"][:, t] = tier1
            rec["tier1_gross"][:, t] = tier_g
            rec["tier1_net"][:, t] = tier_n
            rec["red_q"][:, t] = attempted | is_short
            rec["debt"][:, t] = b_r + b_n
            rec["t2"][:, t] = t2
            rec["t3"][:, t] = t3
            rec["t4"][:, t] = t4
            rec["crisis"][:, t] = crisis
            rec["disc"][:, t] = disc
            rec["dhat"][:, t] = dhat
            rec["mon"][:, t] = mon_cash
            rec["expiry"][:, t] = exp_cash
            rec["deploy"][:, t] = deploy
            rec["sh"][:, t] = sh
            rec["shf"][:, t] = shf
            rec["lcr"][:, t] = lcr
            rec["oil"][:, t] = oil
            rec["tail_mtm"][:, t] = tail_mtm
            rec["prem"][:, t] = prem
            rec["slack"][:, t] = (tre - enc - 0.04 * nav_now + 0.95 * sum(lo.values())
                                  + 0.8 * np.maximum(rcf - b_r, 0.0))
            if not rate_mode:
                rec["cont_nav"][:, t] = SNc + CN * cs_mark
                rec["coflow_acc"][:, t] = accepted if cfg.links else np.nan
                rec["co_deploy"][:, t] = co_deal
                rec["recap_gross"][:, t] = recap_div
                rec["recap_pc"][:, t] = recap_pc
            # group accounting (external cash: + = to CF's pool)
            gcash = {"PE": dist_g["pe"] - calls_g["pe"] + sale_cash["pe"],
                     "SEC": dist_g["sec"] - calls_g["sec"] + sale_cash["sec"],
                     "CS": dist_g["cs"] - calls_g["cs"] + sale_cash["cs"],
                     "CO": dist_g["co"] - calls_g["co"] + sale_cash["co"],
                     "PC": dist_g["pc"] - calls_g["pc"] + sale_cash["pc"],
                     "PM": lo_sold + paid_hf + vm_p2s,
                     "OVL": tail - prem + opp,
                     "TPA": vm_tpa,
                     "CF": -inst - f_cost - i_cost - opex,
                     "RA": ra_q_cash}
            gnav = {"PE": group_nav("pe"), "SEC": group_nav("sec"), "CS": group_nav("cs"), "CO": group_nav("co"),
                    "PC": group_nav("pc"), "PM": sum(lo.values()) + hf + hf_q.sum(1),
                    "OVL": tail_mtm.copy(), "TPA": np.zeros(n), "CF": tre - b_r - b_n,
                    "RA": (ra.nav_true() if ra is not None else np.zeros(n))}
            beta_fb = {"PE": 1.1, "SEC": 0.9, "CS": 0.5, "CO": 1.3, "PC": 0.3}
            for g in ACC:
                rec["cash"][g][:, yr] += gcash[g]
                rec["nav"][g][:, yr] = gnav[g]
                rec["navavg"][g][:, yr] += nav_start_g[g] / 4
                if g in beta_fb:
                    # total return incl. sale proceeds (a sale below economic NAV shows as a loss) minus the
                    # beta-matched funding-basket return on opening NAV
                    ret_d = gnav[g] - nav_start_g[g] + gcash[g]
                    xs = ret_d - nav_start_g[g] * base_r[beta_fb[g]]
                elif g == "PM":
                    # long-only FB = its own index (no alpha modelled); hedge funds vs cash + 0.3 beta
                    xs = (hf + hf_q.sum(1)) - (hf + hf_q.sum(1)) / (1 + r_hf) * (1 + base_r[0.3])
                elif g == "OVL":
                    xs = gnav[g] - nav_start_g[g] + gcash[g]
                elif g == "TPA":
                    xs = (n_tpa - 10.0) * 0 + vm_tpa - E.N_SYN0 * unit_vm * vm_mult_eff
                elif g == "RA":
                    xs = (dS - (ra_vs0 * fb_desm).sum(1)) if ra is not None else np.zeros(n)   # canonical: V*
                else:
                    xs = -f_cost - i_cost
                rec["xs"][g][:, yr] += xs

    nav_T = nav_of()
    w_tilde = nav_T + paid_fv
    k_red = int(red.sum())
    k_b12 = int(black_12m.sum())
    out = dict(
        model=m.key, policy=pol.name, n=n,
        p_red=float(red.mean()), k_red=k_red, cp_upper_red=E.clopper_pearson_upper(k_red, n),
        p_black=float(black.mean()), p_black_12m=float(black_12m.mean()),
        cp_upper_black_12m=E.clopper_pearson_upper(k_b12, n),
        p_band_12m=float(band_active_12m.mean()),
        p_floor4_breach=float(floor4_breach.mean()), p_restore_fail=float(restore_fail.mean()),
        p_covenant=float(covenant_trig.mean()), p_navf_trig_12m=float(navf_trig_12m.mean()),
        max_debt_ratio_p99=float(np.quantile(max_debt_ratio, 0.99)),
        p_debt_gt10=float((max_debt_ratio > 0.10).mean()), p_debt_gt15=float((max_debt_ratio > 0.15).mean()),
        max_enc_p99=float(np.quantile(max_enc, 0.99)),
        mean_red_sales=float(red_sales.mean()), mean_red_loss=float(red_loss.mean()),
        mean_amber_loss=float(amber_loss.mean()), mean_shortfall=float(shortfall.mean()),
        mean_withheld=float(withheld.mean()), mean_fees=float(fees.mean()),
        mean_interest=float(interest.mean()), mean_forced_paydown=float(forced_paydown.mean()),
        mean_commit_forgone=float(commit_forgone.mean()),
        mean_forgone_g={g: float(v.mean()) for g, v in forgone_g.items()},
        forgone_by_q=forgone_t.mean(0).tolist(),
        median_first_red=(float(np.median(first_red[first_red > 0])) if (first_red > 0).any() else None),
        mean_wtilde=float(w_tilde.mean()), mean_navT=float(nav_T.mean()),
        crisis_share_lr=float(pi_c),
        stage_occupancy_avg=stage_hist.mean(axis=0).tolist(),
        w_inv2=float(np.mean((w_tilde / E.NAV0) ** -2.0)),
        gstar_q=[float(x) for x in np.quantile(gstar, [0.5, 0.90, 0.95, 0.99, 0.995, 0.999])] if rate_mode else None,
    )
    out["_w"] = w_tilde
    out["_red"] = red
    out["_wrongway"] = wrongway
    if rate_mode:
        out["_gstar"] = gstar
    if cfg.track:
        out["_rec"] = rec
    if ra is not None:
        def cvar(x, a=0.95):
            k = max(1, int(math.ceil((1 - a) * x.size)))
            return float(np.sort(x)[-k:].mean())

        def qq(x):
            return [float(v) for v in np.quantile(x, [0.05, 0.25, 0.5, 0.75, 0.95])]
        c12, c24 = ra_cure_q[:, :4].sum(1), ra_cure_q[:, :8].sum(1)
        out["ra"] = dict(
            cures12=dict(mean=float(c12.mean()), p95=float(np.quantile(c12, 0.95)), cvar95=cvar(c12)),
            cures24=dict(mean=float(c24.mean()), p95=float(np.quantile(c24, 0.95)), cvar95=cvar(c24)),
            cash_y_mean=ra_cash_y.mean(0).tolist(), p_cash_neg_y=(ra_cash_y < 0).mean(0).tolist(),
            cash5_q=qq(ra_cash_y.sum(1)), navT_y_mean=ra_navT_y.mean(0).tolist(),
            navA_y_mean=ra_navA_y.mean(0).tolist(), navS_y_mean=ra_navS_y.mean(0).tolist(),
            navT5_q=qq(ra_navT_y[:, -1]),
            dva={k: dict(y1_q=qq(v[:, 0]), cum5_q=qq(v.sum(1)), mean_y=v.mean(0).tolist(),
                         p_cum5_neg=float((v.sum(1) < 0).mean())) for k, v in ra_dva.items()},
            jv_cash=float(ra_jv_tot.mean()), oe_redemptions=float(ra_red_tot.mean()),
            cashout=float(ra_co_tot.mean()), forced_sale_cash=float(ra_forced.mean()),
            oil_delta_t0=float(ra_oil0.mean()), oil_delta_post_sale=float(ra_oil_post.mean()),
            enr_cash_t0=float(ra_cash_t0.mean()), enr_value_given=float(enr_vgive.mean()))
        out["_ra"] = dict(cure_q=ra_cure_q, dva=ra_dva, cash_y=ra_cash_y, navT_y=ra_navT_y, navA_y=ra_navA_y,
                          navS_y=ra_navS_y, flow_q=ra_flow_q)
    return out


def ce_wealth(w: np.ndarray) -> float:
    """CRRA(3) certainty-equivalent of distribution-inclusive terminal wealth ($bn)."""
    return float(np.mean(w ** -2.0) ** -0.5)
