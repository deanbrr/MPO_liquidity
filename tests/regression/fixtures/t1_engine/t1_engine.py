"""
gap_02 engine: joint Tier-1 (T1-T9) feasibility study on the SYNTHETIC ADIC book.

SYNTHETIC - NOT ADIC DATA.
- Census: GC2 v1.0 (context s1A working allocation; stream-G7 splits; GC2 D10, D14, D20-D24).
- Six models M1-M6 are STYLISED PROXIES of the report's CMA ensemble (C1 s5.10). Their means are anchored
  on the provider CMAs quoted in dossier 10 s4.1 (JPM 2027, BlackRock fee-adjusted, AQR nominal); their
  structures (drought persistence, stagflation, risk-premia repricing, overlay stress) are design
  assumptions [I]. They are NOT the production scenario engine E and must never be shown as ADIC results.
- Corrections relative to the stream-G7 Monte Carlo (G7 verifier R3, R5, R8; GC2 D3, D10, D12, D19, D21, D22):
  draw on opening-of-fiscal-year reported NAV with annual reset; standby (commitment) and upfront fees;
  regime-dependent facility availability; LTV-cut forced paydowns on the NAV facility; owner deferral cost
  carried outside NAV; P2S keeps exposure through futures (contingent VM); hedge-fund cash arrives through
  a notice/lag/gate queue instead of a capacity bucket; IM is encumbered and excluded from the 8% row.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.stats import beta as beta_dist

NAV0 = 177.0
SOFR = 0.0389                 # 15 Oct 2026 [S] (synthesis s7.1)
CASH_Q = SOFR / 4.0
T_Q = 20                      # 5 years, quarterly

# ----------------------------------------------------------------------------------------------
# 1. Synthetic balance sheet (US$bn).  All SYNTHETIC.
# ----------------------------------------------------------------------------------------------
TRE0 = 15.0                   # cash 6 + UST 4 + IG 5 (Corporate Finance)
LO0 = dict(dm=22.0, em=6.0, fi=8.0)
HF0 = 20.0
PRIV0 = dict(pe=52.0, sec=14.0, co=18.0, cs=8.0, pc=14.0)
UNF0 = dict(pe=27.4, sec=2.4, co=1.5, cs=1.2, pc=2.5)   # regular unfunded (GC2 D21)
SEC_DEF0 = 1.5                # deferred consideration on secondary purchases (paid over 4 quarters)
PC_REV0 = 1.5                 # private-credit revolver/DDTL commitments
assert abs(sum(UNF0.values()) + SEC_DEF0 + PC_REV0 - 38.0) < 1e-9
assert abs(TRE0 + sum(LO0.values()) + HF0 + sum(PRIV0.values()) - NAV0) < 1e-9

N_SYN0 = 10.0                 # synthetic-beta futures notional at t0 (GC2 D22)
N_TAIL = 22.5                 # tail-hedge notional (GC2 D22: 20-25)
TAIL_PREM = 0.0020            # premium, share of NAV0 per year (IC floor 0.15%; G7 used 0.4%)
OPP_IM0 = 1.0                 # opportunistic-book initial margin
IM_N, IM_S = 0.04, 0.10       # futures IM rate normal / stress [S->09 via G7]
FUT_SPREAD_N, FUT_SPREAD_S = 0.0040, 0.0140   # futures financing over SOFR, quarterly roll [S/I, GC2 D25]

# Hedge-fund investor liquidity (OFR Form PF, qualifying hedge funds, 30 Jun 2026) [S]; notice-based,
# gates assumed (GC2 D1). Cash = notice + 30-day payment lag; 5% audit holdback.
_hf = np.array([0.084, 0.273, 0.644 * 2 / 3, 0.644 / 3])
HF_SHARE = _hf / _hf.sum()
HOLDBACK = 0.05
HF_SCHED = np.zeros(10)       # share of a request paid at quarter offset q after the notice quarter
HF_SCHED[0] += HF_SHARE[0] * (1 - HOLDBACK)
HF_SCHED[2] += HF_SHARE[0] * HOLDBACK
HF_SCHED[0] += HF_SHARE[1] * 0.63 * (1 - HOLDBACK)
HF_SCHED[1] += HF_SHARE[1] * 0.37 * (1 - HOLDBACK)
HF_SCHED[3] += HF_SHARE[1] * HOLDBACK
for _q in (1, 2, 3, 4):
    HF_SCHED[_q] += HF_SHARE[2] * 0.25 * (1 - HOLDBACK)
HF_SCHED[6] += HF_SHARE[2] * HOLDBACK
for _q in (4, 5, 6, 7):
    HF_SCHED[_q] += HF_SHARE[3] * 0.25 * (1 - HOLDBACK)
HF_SCHED[9] += HF_SHARE[3] * HOLDBACK
assert abs(HF_SCHED.sum() - 1.0) < 1e-12
HF_CASH90 = float(HF_SCHED[0])  # ~24% of NAV within 90 days (GC2: ~$4.9bn of $20bn)

# Private cash-flow parameters (annual rates)
DIST_NORMAL = dict(pe=0.20, sec=0.25, co=0.18, cs=0.13, pc=0.17)      # stream G7, normal regime
BETA = dict(pe=1.1, sec=0.9, co=1.3, cs=0.5, pc=0.3)                  # stream G7
CALL_BASE = 0.29
PRICE_N = dict(pe=0.90, sec=0.88, co=0.82, pc=0.89, cs=0.85)          # LP-sale price, share of reported NAV
PRICE_C = dict(pe=0.65, sec=0.62, co=0.55, pc=0.75, cs=0.70)          # crisis (G7; H2-2008 anchor 61%)
P_SUCC_N, P_SUCC_C = 0.80, 0.45                                         # C2 success probabilities (GC2 D24)

# Shock-type chain (C3 s5.1 annual prior), states N, B, SG, DB, SS, GW
Z_NAMES = ["N", "B", "SG", "DB", "SS", "GW"]
PZ_A = np.array([[.62, .15, .10, .05, .04, .04],
                 [.40, .40, .05, .06, .07, .02],
                 [.38, .12, .42, .04, .02, .02],
                 [.35, .30, .20, .10, .03, .02],
                 [.30, .05, .10, .35, .15, .05],
                 [.30, .05, .35, .05, .05, .20]])
PZ_Q = np.eye(6) + (PZ_A - np.eye(6)) / 4.0
Z0_PROB = np.array([0.15, 0.0, 0.15, 0.0, 0.0, 0.70])      # C3: Z0 = GW with p >= 0.7 [I]
D_TGT = np.array([0.0675, 0.055, 0.0875, 0.10, 0.0575, 0.080])   # owner draw target by Z [I, C3 kinks]
P_OV = np.array([0.0025, 0.0025, 0.01, 0.01, 0.0025, 0.02])       # override probability per year (C3)
KAPPA_CRISIS = np.array([1.0, 0.5, 1.5, 4.0, 2.0, 1.5])            # crisis-entry multiplier by Z [I]


@dataclass(frozen=True)
class Model:
    key: str
    label: str
    eq_g: float          # ACWI 10y geometric
    cash_lr: float
    fi_g: float
    hf_g: float
    pe_g: float          # PE, net of fees
    pc_g: float
    cs_g: float
    crisis_entry: float  # base quarterly crisis-entry probability (Z = N)
    d_stay: float        # quarterly persistence of the exit drought (non-crisis)
    phi: float           # structural scalar on PE-type distributions
    md_f: float          # distribution multiplier in frozen exits (F)
    mc_f: float          # call multiplier in F
    fi_crisis_q: float   # long-only FI return per crisis quarter
    ust_crisis_q: float  # UST component of the Treasury pool per crisis quarter
    vm_mult: float = 1.0
    opp_mult: float = 1.0
    repricing_q: int = 0
    repricing_drift: float = 0.0


MODELS = {
    "M1": Model("M1", "JPM 2027 base", 0.075, 0.031, 0.053, 0.067, 0.096, 0.077, 0.085,
                0.020, 0.88, 1.00, 0.30, 0.80, +0.005, +0.015),
    "M2": Model("M2", "BlackRock fee-adjusted base", 0.0902, 0.0366, 0.0488, 0.068, 0.124, 0.0931, 0.100,
                0.015, 0.88, 1.00, 0.30, 0.80, +0.005, +0.015),
    "M3": Model("M3", "AQR nominal base", 0.066, 0.030, 0.049, 0.055, 0.066, 0.050, 0.060,
                0.025, 0.88, 1.00, 0.30, 0.80, +0.005, +0.015),
    "M4": Model("M4", "JPM persistent drought", 0.075, 0.031, 0.053, 0.067, 0.096, 0.077, 0.085,
                0.025, 0.95, 0.75, 0.20, 0.80, +0.005, +0.015),
    "M5": Model("M5", "JPM stagflation-heavy", 0.060, 0.031, 0.040, 0.060, 0.080, 0.070, 0.080,
                0.035, 0.90, 0.90, 0.25, 0.90, -0.025, -0.010),
    "M6": Model("M6", "BlackRock risk-premia-rise + drought + overlay stress", 0.030, 0.0366, 0.045, 0.050,
                0.059, 0.060, 0.070, 0.030, 0.93, 0.85, 0.20, 1.00, -0.010, +0.010,
                vm_mult=1.5, opp_mult=1.5, repricing_q=6, repricing_drift=-0.025),
}

EQ_CALM_SD = 0.07
# Crisis equity profile by quarters-in-crisis (front-loaded falls, grinding tail) and a post-crisis rebound [I].
# A typical 4-quarter crisis loses ~30% (2008-09: ~-55% peak-to-trough over ~6 quarters is a 1-in-50 path here).
CRISIS_MU = {1: -0.12, 2: -0.12, 3: -0.04, 4: -0.04}     # d >= 5: +0.01
CRISIS_SD = {1: 0.14, 2: 0.14, 3: 0.10, 4: 0.10}         # d >= 5: 0.08
CRISIS_MU_LONG, CRISIS_SD_LONG = 0.01, 0.08
REBOUND_Q, REBOUND_ADD = 4, 0.03


def crisis_mu_sd(dur):
    mu = np.where(dur <= 2, -0.12, np.where(dur <= 4, -0.04, CRISIS_MU_LONG))
    sd = np.where(dur <= 2, 0.14, np.where(dur <= 4, 0.10, CRISIS_SD_LONG))
    return mu, sd


@dataclass(frozen=True)
class Policy:
    """Levers of the minimum-cost mix. Defaults = do nothing beyond the CFP's HF-notice playbook."""
    name: str = "A"
    rcf: float = 0.0              # committed unsecured revolver, $bn
    navf: float = 0.0             # committed LP-portfolio NAV facility, $bn
    pace: float = 12.0            # base commitments, $bn/yr
    pace_cut: bool = False        # stage-triggered cut to 25% (Amber+ or crisis)
    band: bool = False            # owner-agreed draw of 5% of basis in Red/Black stage or crisis
    reserve: float = 0.08         # unencumbered Treasury (cash+UST+IG) target, share of NAV
    amber_t0: float = 0.0         # pre-emptive Private Credit / Capital Solutions sale at t0, $bn
    hf_t0: float = 0.0            # pre-emptive hedge-fund redemption notice at t0, $bn
    hf_amber: bool = True         # CFP Amber playbook: notices for 50% of unqueued HF per quarter
    floor_hard: float = 0.04      # hard IG+cash floor (GC2 D10)
    rcf_undrawn_fee: float = 0.0015
    rcf_upfront: float = 0.0015   # per 3-year tenor
    rcf_margin: float = 0.0085
    navf_undrawn_fee: float = 0.0050
    navf_upfront: float = 0.0100
    navf_margin: float = 0.0300
    navf_stress_add: float = 0.0140
    debt_cap: float = 0.15        # T5 hard: no new draws above 15% of current NAV
    rcf_covenant: float = 0.25    # lender maintenance covenant, debt / NAV [I]
    p2s_cap: float = 15.0         # synthetic-beta notional cap after P2S conversions (GC2 D22 stress level)


def _q(r_annual):
    return 1.0 - (1.0 - r_annual) ** 0.25


_PI_CACHE: dict = {}


def _crisis_stats(m: Model) -> dict:
    """Long-run shares of crisis quarters by duration bucket and of rebound quarters (simulated once)."""
    if m.key in _PI_CACHE:
        return _PI_CACHE[m.key]
    rng = np.random.default_rng(123)
    n, T = 20000, 220
    z = rng.choice(6, size=n, p=Z0_PROB)
    cr = np.zeros(n, dtype=bool)
    dur = np.zeros(n, dtype=int)
    since = np.full(n, 99)
    acc_log_crisis = 0.0
    n_rebound = 0.0
    n_calm = 0.0
    n_cr = 0.0
    cdf = np.cumsum(PZ_Q, axis=1)
    for t in range(T):
        z_prev = z
        z = (rng.random(n)[:, None] > cdf[z]).sum(axis=1)
        enter_db = (z == 3) & (z_prev != 3)
        stay = np.where(z == 3, 0.90, 0.75)
        p_enter = np.minimum(0.95, m.crisis_entry * KAPPA_CRISIS[z])
        u = rng.random(n)
        cr_prev = cr
        cr = np.where(enter_db, u < 0.85, np.where(cr, u < stay, u < p_enter))
        dur = np.where(cr, dur + 1, 0)
        since = np.where(cr, 0, np.where(cr_prev & ~cr, 1, since + 1))
        if t >= 60:
            mu, sd = crisis_mu_sd(dur)
            acc_log_crisis += float(np.sum(np.where(cr, mu - 0.5 * sd ** 2, 0.0)))
            n_cr += float(cr.sum())
            n_rebound += float((~cr & (since <= REBOUND_Q)).sum())
            n_calm += float((~cr).sum())
    tot = n * (T - 60)
    _PI_CACHE[m.key] = dict(pi_c=n_cr / tot, crisis_log_sum=acc_log_crisis / tot,
                            rebound_share=n_rebound / tot, calm_share=n_calm / tot)
    return _PI_CACHE[m.key]


def stationary_crisis_share(m: Model) -> float:
    return _crisis_stats(m)["pi_c"]


def calm_drift(m: Model, pi_c: float | None = None) -> float:
    """Calm-quarter arithmetic equity mean such that unconditional log growth matches the model CMA."""
    st = _crisis_stats(m)
    target = math.log1p(m.eq_g) / 4.0
    mu_n_log = (target - st["crisis_log_sum"] - st["rebound_share"] * REBOUND_ADD) / st["calm_share"]
    return mu_n_log + 0.5 * EQ_CALM_SD ** 2


def clopper_pearson_upper(k: int, n: int, alpha: float = 0.05) -> float:
    """One-sided (1 - alpha) Clopper-Pearson upper bound."""
    if k >= n:
        return 1.0
    return float(beta_dist.ppf(1 - alpha, k + 1, n - k))


def simulate(m: Model, pol: Policy, n: int = 10000, seed: int = 20261018, hf_gate_pass: float = 0.83,
             overrides: bool = True, kappa_own: float = 0.05, return_paths: bool = False) -> dict:
    """Quarterly Monte Carlo over 20 quarters from today's drought (exit window D) and Gulf-war (Z0) state.

    Red event (T6): any liquidity-driven sale (or failed attempt) of PE / Secondaries / Co-investment, or a
    payout below the owner's call. Common random numbers: the same seed gives the same exogenous paths for
    every policy (policy-dependent draws use a separate stream).
    """
    pi_c = stationary_crisis_share(m)
    mu_calm = calm_drift(m, pi_c)
    rng = np.random.default_rng(seed)                 # exogenous stream
    rng_p = np.random.default_rng(seed + 7)           # sale-execution stream
    cdfZ = np.cumsum(PZ_Q, axis=1)

    eq_arith = math.log1p(m.eq_g) + 0.5 * 0.165 ** 2

    def alpha_for(g_target, beta):
        return (g_target + 0.5 * (beta * 0.165) ** 2) - (m.cash_lr + beta * (eq_arith - m.cash_lr))

    tgt = {"pe": m.pe_g, "sec": m.pe_g + 0.005, "co": m.pe_g, "cs": m.cs_g, "pc": m.pc_g}
    alpha = {g: alpha_for(tgt[g], BETA[g]) for g in PRIV0}
    alpha["pc"] += pi_c * 0.08
    alpha_hf = alpha_for(m.hf_g, 0.3) + pi_c * 0.08

    tre = np.full(n, TRE0)
    lo = {k: np.full(n, v) for k, v in LO0.items()}
    hf = np.full(n, HF0)
    hf_q = np.zeros((n, 10))
    priv = {k: np.full(n, v) for k, v in PRIV0.items()}
    econ_prev = {k: np.zeros(n) for k in PRIV0}
    rep = {k: np.full(n, v) for k, v in PRIV0.items()}
    unf = {k: np.full(n, v) for k, v in UNF0.items()}
    sec_def = np.full(n, SEC_DEF0)
    pc_rev = np.full(n, PC_REV0)
    n_syn = np.full(n, N_SYN0)
    b_r = np.zeros(n)
    b_n = np.zeros(n)
    z = rng.choice(6, size=n, p=Z0_PROB)
    crisis = np.zeros(n, dtype=bool)
    cdur = np.zeros(n, dtype=int)
    since_exit = np.full(n, 99)
    e = np.full(n, 2)
    d_prev = np.full(n, 0.075)
    d_year = np.full(n, 0.075)
    basis = np.full(n, NAV0)
    override_year = np.zeros(n, dtype=bool)
    im_prev = IM_N * n_syn

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
    stage_hist = np.zeros((T_Q, 4))
    netneed8 = np.zeros(n)
    # buy-and-hold mark of the t0 Treasury + Public Markets book (for the 24-month gap metric)
    bh = dict(tre=np.full(n, TRE0), dm=np.full(n, LO0["dm"]), em=np.full(n, LO0["em"]),
              fi=np.full(n, LO0["fi"]), hf=np.full(n, HF0))
    tp0 = TRE0 + sum(LO0.values()) + HF0
    tp_bh8 = np.full(n, tp0)
    # survival-ladder replica on each path (no management actions): G* = max_t [NCO + floor - CBC_TP]
    hf_bh_q = np.tile(HF0 * HF_SCHED, (n, 1))     # whole HF book noticed at t0
    hf_bh_cash = np.zeros(n)
    nco_bh = np.zeros(n)
    gstar = np.full(n, -np.inf)
    nav_min = np.full(n, NAV0)

    # ---------------- t0 actions
    if pol.amber_t0 > 0:
        tot = PRIV0["pc"] + PRIV0["cs"]
        for g in ("pc", "cs"):
            sell_amt = pol.amber_t0 * PRIV0[g] / tot
            frac = sell_amt / PRIV0[g]
            tre += sell_amt * PRICE_N[g]
            amber_loss += sell_amt * (1 - PRICE_N[g])
            amber_sales += sell_amt
            priv[g] -= sell_amt
            rep[g] -= sell_amt
            unf[g] *= (1 - frac)
    if pol.hf_t0 > 0:
        amt = min(pol.hf_t0, HF0)
        hf -= amt
        hf_q += amt * HF_SCHED[None, :]
    enc0 = IM_N * N_SYN0 + OPP_IM0
    top_up = max(0.0, pol.reserve * NAV0 - (float(tre[0]) - enc0))
    if top_up > 0:
        a = min(top_up / 0.998, LO0["dm"])
        lo["dm"] -= a
        tre += a * 0.998
    up = pol.rcf * pol.rcf_upfront + pol.navf * pol.navf_upfront
    fees += up
    tre -= up

    def nav_of():
        return tre + sum(lo.values()) + hf + hf_q.sum(axis=1) + sum(priv.values()) - b_r - b_n

    for t in range(T_Q):
        # ---------------- fiscal-year basis (opening reported NAV, annual reset)
        if t % 4 == 0:
            basis = sum(rep.values()) + tre + sum(lo.values()) + hf + hf_q.sum(axis=1) - b_r - b_n
        # ---------------- regimes
        z_prev = z
        z = (rng.random(n)[:, None] > cdfZ[z]).sum(axis=1)
        enter_db = (z == 3) & (z_prev != 3)
        stay = np.where(z == 3, 0.90, 0.75)
        p_enter = np.minimum(0.95, m.crisis_entry * KAPPA_CRISIS[z])
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

        # ---------------- market returns
        zz = rng.standard_normal(n)
        drift = mu_calm + (m.repricing_drift if t < m.repricing_q else 0.0) \
            + np.where(since_exit <= REBOUND_Q, REBOUND_ADD, 0.0)
        c_mu, c_sd = crisis_mu_sd(cdur)
        r_eq = np.where(crisis, c_mu + c_sd * zz, drift + EQ_CALM_SD * zz)
        r_eq = np.maximum(r_eq, -0.6)
        r_em = 1.2 * r_eq + 0.04 * rng.standard_normal(n)
        r_fi = np.where(crisis, m.fi_crisis_q, m.fi_g / 4) + 0.02 * (0.3 * zz + 0.95 * rng.standard_normal(n))
        r_tre = np.where(crisis, 0.4 * CASH_Q + 0.27 * m.ust_crisis_q + 0.33 * (-0.005), 0.0100)
        r_hf = CASH_Q + 0.3 * (r_eq - CASH_Q) + alpha_hf / 4 + np.where(crisis, -0.02, 0.0) \
            + 0.025 * rng.standard_normal(n)
        nav_start = nav_of()
        tre *= 1 + r_tre
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
        for g in PRIV0:
            econ = CASH_Q + BETA[g] * (r_eq - CASH_Q) + alpha[g] / 4 + np.where(crisis & (g == "pc"), -0.02, 0.0)
            priv[g] *= 1 + econ
            rep[g] *= 1 + (0.5 * econ + 0.5 * econ_prev[g])
            econ_prev[g] = econ

        # ---------------- private cash flows
        mD = np.array([1.25, 1.0, 0.50, m.md_f])[e]
        mC = np.array([1.3, 1.0, 0.97, m.mc_f])[e]
        dist = np.zeros(n)
        for g in ("pe", "sec", "co"):
            d = _q(np.minimum(0.95, DIST_NORMAL[g] * mD * m.phi)) * priv[g]
            priv[g] -= d
            rep[g] -= d
            dist += d
        mDc = np.array([1.05, 1.0, 0.92, 0.57])[e]
        for g in ("cs", "pc"):
            d = _q(DIST_NORMAL[g] * mDc) * priv[g]
            priv[g] -= d
            rep[g] -= d
            dist += d
        cq = _q(np.minimum(0.95, CALL_BASE * mC))
        calls = np.zeros(n)
        for g in UNF0:
            c = cq * unf[g]
            if g == "pe":
                c = c + np.where(onset, 0.05 * unf[g], 0.0)   # subscription-line clean-up at crisis onset [I]
            c = np.minimum(c, unf[g])
            unf[g] -= c
            priv[g] += c
            rep[g] += c
            calls += c
        c = np.full(n, SEC_DEF0 / 4 if t < 4 else 0.0)
        sec_def -= c
        priv["sec"] += c
        rep["sec"] += c
        calls += c
        c = np.minimum(pc_rev, np.where(onset, 0.5 * pc_rev, _q(0.15) * pc_rev))
        pc_rev -= c
        priv["pc"] += c
        rep["pc"] += c
        calls += c

        # ---------------- stage (CFP thresholds, GC2 D14)
        nav_now = nav_of()
        im_req = np.where(crisis, IM_S, IM_N) * n_syn
        opp_im = np.where(crisis & (m.opp_mult > 1), 2.0, 1.0) * OPP_IM0
        enc = im_req + opp_im
        usable = tre - enc
        liq_share = (usable + sum(lo.values()) + HF_CASH90 * hf + hf_q[:, 0]) / nav_now
        tre_share = usable / nav_now
        stage = np.zeros(n, dtype=int)
        stage = np.maximum(stage, np.where(liq_share < 0.28, 1, 0))
        stage = np.maximum(stage, np.where(liq_share < 0.24, 2, 0))
        stage = np.maximum(stage, np.where(liq_share < 0.20, 3, 0))
        stage = np.maximum(stage, np.where(tre_share < 0.06, 1, 0))
        stage = np.maximum(stage, np.where(tre_share < 0.04, 2, 0))
        stage = np.maximum(stage, np.where(crisis, 1, 0))
        for s in range(4):
            stage_hist[t, s] += float((stage == s).mean())
        amber_up = stage >= 1
        red_up = (stage >= 2) | crisis

        # ---------------- new commitments
        k = np.full(n, pol.pace / 4)
        if pol.pace_cut:
            k = np.where(amber_up, 0.25 * k, k)
        commit_forgone += np.maximum(0.0, 12.0 / 4 - k)
        for g, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1)):
            unf[g] += w * k
        co_deal = 0.1 * k
        priv["co"] += co_deal
        rep["co"] += co_deal

        # ---------------- owner draw (Mode B), opening reported NAV basis, quarterly instalments
        if t % 4 == 0:
            tgt_d = D_TGT[z] + 0.005 * rng.standard_normal(n)
            d_year = np.clip(0.5 * d_prev + 0.5 * tgt_d, 0.05, 0.10)
            ov = rng.random(n) < P_OV[z]
            if overrides:
                d_year = np.where(ov, 0.10 + rng.uniform(0.02, 0.035, n), d_year)
                override_year = ov
            d_prev = np.minimum(d_year, 0.10)
        inst = d_year * basis / 4
        inst_mode_b = inst
        if pol.band:
            cut = ((stage >= 2) | crisis) & ~override_year
            new_inst = np.where(cut, 0.05 * basis / 4, inst)
            withheld += inst - new_inst
            if t < 4:
                band_active_12m |= cut & (new_inst < inst - 1e-12)
            inst = new_inst

        # ---------------- overlay
        spread = np.where(crisis, FUT_SPREAD_S, FUT_SPREAD_N)
        vm = n_syn * (r_eq - CASH_Q - spread / 4)
        vm = np.where(crisis & (vm < 0), vm * m.vm_mult, vm)      # overlay stress: margin outflows amplified
        prem = TAIL_PREM * NAV0 / 4
        tail = N_TAIL * np.clip(-r_eq - 0.10, 0.0, 0.18)
        opp = 0.0125 / 2 * NAV0 * rng.standard_normal(n) + np.where(crisis, -0.005, 0.001) * NAV0
        opp = np.where(crisis, opp * m.opp_mult, opp)
        d_im = im_req - im_prev
        im_prev = im_req

        # ---------------- facility costs
        f_cost = np.maximum(pol.rcf - b_r, 0.0) * pol.rcf_undrawn_fee / 4 \
            + np.maximum(pol.navf - b_n, 0.0) * pol.navf_undrawn_fee / 4
        if t == 12:
            f_cost = f_cost + pol.rcf * pol.rcf_upfront
        i_cost = b_r * (SOFR + pol.rcf_margin) / 4 \
            + b_n * (SOFR + pol.navf_margin + np.where(crisis, pol.navf_stress_add, 0.0)) / 4
        fees += f_cost
        interest += i_cost
        opex = 0.001 / 4 * nav_start

        net = inst + calls + co_deal + prem + f_cost + i_cost + opex - dist - vm - tail - opp
        tre -= net
        if t < 8:
            step = net - f_cost - i_cost + np.maximum(d_im, 0.0)
            netneed8 += step
            # ladder replica (action-free): t0 overlay only, Mode-B draws, CBC = t0 Treasury + Public Markets
            # book held until needed at current marks and stress haircuts; HF through the gated queue;
            # floor 4% of an action-free NAV estimate
            vm0 = N_SYN0 * (r_eq - CASH_Q - spread / 4)
            vm0 = np.where(crisis & (vm0 < 0), vm0 * m.vm_mult, vm0)
            d_im0 = (np.where(crisis, IM_S, IM_N) - np.where(crisis_prev, IM_S, IM_N)) * N_SYN0
            nco_bh += (inst_mode_b + calls + co_deal + prem + opex - dist - vm0 - tail - opp
                       + np.maximum(d_im0, 0.0))
            due_bh = hf_bh_q[:, 0].copy()
            paid_bh = np.where(crisis, hf_gate_pass * due_bh, due_bh)
            hf_bh_q[:, :-1] = hf_bh_q[:, 1:]
            hf_bh_q[:, -1] = 0.0
            hf_bh_q[:, 0] += due_bh - paid_bh
            hf_bh_q *= (1 + r_hf)[:, None]
            hf_bh_cash += paid_bh
            cbc_t = ((bh["tre"] - IM_N * N_SYN0 - OPP_IM0) * (1 - 0.038) + bh["dm"] * 0.985
                     + bh["fi"] * 0.95 + bh["em"] * 0.95 + hf_bh_cash)
            nav_bh = sum(bh.values()) + sum(priv.values()) - nco_bh
            gap_t = nco_bh + 0.04 * nav_bh - cbc_t
            gstar = np.maximum(gstar, gap_t)
        if t == 7:
            tp_bh8 = sum(bh.values())

        # ---------------- hedge-fund queue: cash due this quarter, gated in crisis
        due = hf_q[:, 0].copy()
        paid_hf = np.where(crisis, hf_gate_pass * due, due)
        rolled = due - paid_hf
        hf_q[:, :-1] = hf_q[:, 1:]
        hf_q[:, -1] = 0.0
        hf_q[:, 0] += rolled
        tre += paid_hf
        if pol.hf_amber:
            file = np.where(amber_up, 0.5 * hf, 0.0)
            hf -= file
            hf_q += file[:, None] * HF_SCHED[None, :]

        # ---------------- NAV facility: LTV cut -> forced paydown (lender-imposed)
        pool = np.maximum(np.minimum(0.20 * sum(priv.values()), rep["pe"] + rep["sec"]), 1e-9)
        ltv_cap = np.where(crisis, 0.05, 0.10)
        if t < 4:
            navf_trig_12m |= (b_n > 1e-9) & (b_n / pool > 0.15)
        fp = np.maximum(0.0, b_n - ltv_cap * pool)
        b_n -= fp
        tre -= fp
        forced_paydown += fp

        # ---------------- waterfall
        nav_now = nav_of()
        usable = tre - enc
        target = pol.reserve * nav_now
        floor = pol.floor_hard * nav_now
        need = np.maximum(0.0, target - usable)
        # (1) long-only: P2S in calm quarters (keeps exposure, cap 30% NAV), outright in crisis
        room = np.maximum(0.0, np.minimum(0.30 * nav_now, pol.p2s_cap) - n_syn)
        p2s_net = 0.998 - IM_N
        a = np.where(~crisis, np.minimum(np.minimum(0.5 * lo["dm"], room), need / p2s_net), 0.0)
        lo["dm"] -= a
        n_syn = n_syn + a
        tre += a * 0.998
        enc = enc + a * IM_N
        im_prev = im_prev + a * IM_N
        need = need - a * p2s_net
        for key, cap, pn, pc_ in (("dm", 0.5, 0.998, 0.985), ("fi", 0.5, 0.995, 0.95), ("em", 0.5, 0.99, 0.95)):
            capf = cap
            price = np.where(crisis, pc_, pn)
            a = np.minimum(np.maximum(capf * lo[key], 0.0), need / price)
            lo[key] -= a
            tre += a * price
            need = need - a * price
        # (2) Red / crisis (or Treasury below 6%): committed facilities toward the target,
        #     then amber sales to defend 6% of NAV
        use_fac = red_up | ((tre - enc) < 0.06 * nav_now)
        if pol.rcf > 0:
            avail_f = np.where(crisis, np.where((z == 3) | (z == 5), 0.80, 0.90), 1.0)
            cap_debt = np.maximum(0.0, pol.debt_cap * nav_now - b_r - b_n)
            avail = np.maximum(0.0, np.minimum(pol.rcf * avail_f - b_r, cap_debt))
            dr = np.where(use_fac, np.minimum(avail, need), 0.0)
            b_r += dr
            tre += dr
            need = need - dr
        if pol.navf > 0:
            cap_debt = np.maximum(0.0, pol.debt_cap * nav_now - b_r - b_n)
            avail = np.maximum(0.0, np.minimum(np.minimum(pol.navf, ltv_cap * pool) - b_n, cap_debt))
            dr = np.where(use_fac, np.minimum(avail, need / 0.985), 0.0)
            b_n += dr
            tre += dr * 0.985
            fees += dr * 0.015
            need = need - dr * 0.985
        usable = tre - enc
        need_amber = np.maximum(0.0, np.where(red_up, 0.06, pol.floor_hard + 0.01) * nav_now - usable)
        for g in ("pc", "cs"):
            pr = np.where(crisis, PRICE_C[g], PRICE_N[g])
            amt = np.minimum(0.10 * priv[g], need_amber / pr)
            frac = amt / np.maximum(priv[g], 1e-9)
            priv[g] -= amt
            rep[g] -= amt
            unf[g] *= 1 - frac
            tre += amt * pr
            need_amber = need_amber - amt * pr
            amber_sales += amt
            amber_loss += amt * (1 - pr)
        # (3) defend the hard floor: red sales (Secondaries, PE, Co-investment)
        usable = tre - enc
        need_floor = np.maximum(0.0, floor - usable)
        depth = np.where(crisis, 2.5, 4.0)
        ok = rng_p.random(n) < np.where(crisis, P_SUCC_C, P_SUCC_N)
        for g in ("sec", "pe", "co"):
            pr = np.where(crisis, PRICE_C[g], PRICE_N[g])
            amt = np.where(ok, np.minimum(np.minimum(priv[g], depth), need_floor / pr), 0.0)
            frac = amt / np.maximum(priv[g], 1e-9)
            priv[g] -= amt
            rep[g] -= amt
            unf[g] *= 1 - frac
            tre += amt * pr
            need_floor = need_floor - amt * pr
            depth = depth - amt
            red_sales += amt
            red_loss += amt * (1 - pr)
        attempted = np.maximum(0.0, floor - usable) > 1e-6
        first_red = np.where(attempted & (first_red < 0), t + 1, first_red)
        red |= attempted
        floor4_breach |= (tre - enc) < floor - 1e-6
        # (4) payout shortfall if usable cash is negative (capped at this quarter's instalment); any residual
        #     deficit (e.g. variation margin) is met by an emergency pro-rata private sale at 50% of NAV
        usable = tre - enc
        short = np.maximum(0.0, -usable)
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
            tot_priv = np.maximum(sum(priv.values()), 1e-9)
            sold = np.minimum(resid / 0.5, tot_priv)
            for g in PRIV0:
                share = priv[g] / tot_priv
                priv[g] -= sold * share
                rep[g] -= sold * share
                unf[g] *= 1 - np.minimum(1.0, sold / tot_priv)
            tre += sold * 0.5
            red_sales += sold
            red_loss += sold * 0.5
        paid_fv += (inst - short_pay) * 1.10 ** ((T_Q - t - 1) / 4)

        # ---------------- repayments in calm Green quarters
        nav_now = nav_of()
        usable = tre - enc
        excess = np.where(~crisis & (stage == 0), np.maximum(0.0, usable - (pol.reserve + 0.02) * nav_now), 0.0)
        rp = np.minimum(b_n, excess)
        b_n -= rp
        tre -= rp
        excess = excess - rp
        rp = np.minimum(b_r, excess)
        b_r -= rp
        tre -= rp

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

    nav_T = nav_of()
    w_tilde = nav_T + paid_fv
    k_red = int(red.sum())
    k_b12 = int(black_12m.sum())
    gap8 = netneed8 + (tp0 - tp_bh8)      # 24-month need including the asset shock to the T+P book
    out = dict(
        model=m.key, policy=pol.name, n=n,
        p_red=float(red.mean()), k_red=k_red, cp_upper_red=clopper_pearson_upper(k_red, n),
        p_black=float(black.mean()), p_black_12m=float(black_12m.mean()),
        cp_upper_black_12m=clopper_pearson_upper(k_b12, n),
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
        median_first_red=(float(np.median(first_red[first_red > 0])) if (first_red > 0).any() else None),
        mean_wtilde=float(w_tilde.mean()), mean_navT=float(nav_T.mean()),
        crisis_share_lr=float(pi_c),
        stage_occupancy_avg=stage_hist.mean(axis=0).tolist(),
        w_inv2=float(np.mean((w_tilde / NAV0) ** -2.0)),
        netneed8_q=[float(x) for x in np.quantile(netneed8, [0.5, 0.95, 0.99, 0.995, 0.999])],
        gap8_q=[float(x) for x in np.quantile(gap8, [0.5, 0.95, 0.99, 0.995, 0.999])],
        gstar_q=[float(x) for x in np.quantile(gstar, [0.5, 0.90, 0.95, 0.99, 0.995, 0.999])],
        nav_min_q=[float(x) for x in np.quantile(nav_min, [0.001, 0.01, 0.05, 0.5])],
        navT_q=[float(x) for x in np.quantile(nav_T, [0.001, 0.01, 0.05, 0.5])],
    )
    if return_paths:
        out["_gap8"] = gap8
        out["_netneed8"] = netneed8
        out["_gstar"] = gstar
    return out


def ce_growth(w_inv2_by_model: dict, weights: dict | None = None) -> float:
    """Annualised CRRA(3) certainty-equivalent growth of distribution-inclusive wealth over 5 years."""
    keys = list(w_inv2_by_model)
    if weights is None:
        weights = {k: 1.0 / len(keys) for k in keys}
    m2 = sum(weights[k] * w_inv2_by_model[k] for k in keys)
    ce = m2 ** (-0.5)
    return ce ** (1 / 5) - 1


# ----------------------------------------------------------------------------------------------
# 2. Deterministic named-stress ladder (monthly), for T4 / s* / C3 / G7-S1 comparisons
# ----------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Stress:
    name: str
    eq_drawdown: float = 0.40          # peak-to-trough over months 1-6 (G7 S1 shape, rescaled)
    dist_mult_pe: tuple = ((24, 0.0),)  # (months, multiplier on drought rates) for PE / Sec / Co
    pc_cs_rates: tuple = (0.10, 0.07)  # contractual cash yields in stress (PC, CS), annual
    call_mult: tuple = ((24, 1.5),)    # (months, multiplier) on the drought call rate (28%)
    draw_rates: tuple = (0.10, 0.10, 0.075)   # by fiscal year
    draw_basis: str = "opening_reset"  # opening_reset | fixed_usd | current
    override_y2: float = 0.0           # extra draw in fiscal year 2, share of basis
    fac_credit: float = 0.80           # unsecured committed RCF credit
    navf_ltv: float = 0.05             # stressed LTV on the pledge pool
    hf_pass: float = 0.83              # HF gate pass-through in crisis months
    floor: float = 0.04                # usable IG+cash floor, share of NAV
    crisis_months: int = 18
    priv_marks: tuple = ((3, -0.08), (6, -0.08), (9, -0.04))
    im_months: int = 12
    instant: bool = True               # vertex convention: the equity shock hits marketable assets at t0


DROUGHT_DIST = dict(pe=0.10, sec=0.125, co=0.09)     # PE-type drought rates (20/25/18% x 0.5)


def _monthly(r):
    return 1.0 - (1.0 - r) ** (1.0 / 12.0)


def ladder(s: Stress, pol: Policy, T: int = 36) -> dict:
    """Monthly survival ladder on the t0 synthetic book.

    CBC_TP(h): cumulative proceeds from liquidating Treasury + Public Markets at maximum pace (stress haircuts,
    path prices, hedge-fund notices filed at month 0 and paid through the queue), less the usable floor.
    NCO(h): cumulative net contractual and behavioural outflow. F(h): committed facilities x credit.
    No private-asset sales of any kind (T4 convention), so amber sales count only if made pre-emptively at t0.
    """
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

    # t0 balances after t0 policy actions
    tre = TRE0
    dm, em, fi_b = LO0["dm"], LO0["em"], LO0["fi"]
    priv = dict(PRIV0)
    unf = dict(UNF0)
    if pol.amber_t0 > 0:
        tot = PRIV0["pc"] + PRIV0["cs"]
        for g in ("pc", "cs"):
            amt = pol.amber_t0 * PRIV0[g] / tot
            tre += amt * PRICE_N[g]
            unf[g] *= 1 - amt / PRIV0[g]
            priv[g] -= amt
    enc0 = IM_N * N_SYN0 + OPP_IM0
    top = max(0.0, pol.reserve * NAV0 - (tre - enc0))
    a = min(top / 0.998, dm)
    dm -= a
    tre += a * 0.998
    tre -= pol.rcf * pol.rcf_upfront + pol.navf * pol.navf_upfront

    # --- outflow ladder
    eq_idx = 1.0
    im = IM_N * N_SYN0
    sec_def, pc_rev = SEC_DEF0, PC_REV0
    rows = []
    priv_m = dict(priv)
    basis = NAV0
    nav_rep_hist = []
    nco = 0.0
    liq_bh = dict(tre=tre, dm=dm, em=em, fi=fi_b, hf=HF0)
    year1_priv_net = 0.0
    for t in range(T):
        # marks
        for g in priv_m:
            priv_m[g] *= 1 + pm[t]
        dist = 0.0
        for g in ("pe", "sec", "co"):
            r = DROUGHT_DIST[g] * mult_at(s.dist_mult_pe, t, 1.0)
            d = _monthly(min(0.95, r)) * priv_m[g]
            priv_m[g] -= d
            dist += d
        for g, r in (("pc", s.pc_cs_rates[0]), ("cs", s.pc_cs_rates[1])):
            r_eff = r if crisis[t] else DIST_NORMAL[g] * 0.92
            d = _monthly(r_eff) * priv_m[g]
            priv_m[g] -= d
            dist += d
        crate = _monthly(min(0.95, 0.28 * mult_at(s.call_mult, t, 1.0)))
        calls = 0.0
        for g in unf:
            c = crate * unf[g]
            unf[g] -= c
            priv_m[g] += c
            calls += c
        if t in (2, 5, 8, 11):
            calls += SEC_DEF0 / 4
        rev = min(pc_rev, 0.5 * PC_REV0 / 3 if t < 3 else _monthly(0.15) * pc_rev)
        pc_rev -= rev
        calls += rev
        k = pol.pace / 12
        if pol.pace_cut and t >= 2 and crisis[t]:
            k *= 0.25
        for g, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1)):
            unf[g] += w * k
        calls += 0.1 * k          # direct co-investment deployment
        # draws
        fy = t // 12
        rate = s.draw_rates[min(fy, len(s.draw_rates) - 1)]
        if pol.band and crisis[t]:
            rate = 0.05
        if fy == 1:
            rate += s.override_y2
        nav_now_est = sum(liq_bh.values()) + sum(priv_m.values()) - nco
        if s.draw_basis == "fixed_usd":
            base = NAV0
        elif s.draw_basis == "current":
            base = max(nav_now_est, 1e-9)
        else:
            if t % 12 == 0:
                # reported NAV at fiscal-year start: private marks lag one quarter
                lag_priv = sum(priv_m.values()) / (1 + (pm[max(t - 1, 0)] + pm[max(t - 2, 0)] + pm[max(t - 3, 0)]))
                basis = (nav_now_est - sum(priv_m.values()) + lag_priv) if t > 0 else NAV0
            base = basis
        draw = rate * base / 12
        # overlay
        vm = N_SYN0 * eq_idx * eq[t]
        eq_idx *= 1 + eq[t]
        im_new = (IM_S if (crisis[t] and t < s.im_months) else IM_N) * N_SYN0 * eq_idx
        d_im = im_new - im
        im = im_new
        prem = TAIL_PREM * NAV0 / 12
        tail = 0.0
        if t in (1, 5):
            tail = 0.5 * N_TAIL * min(0.18, max(0.0, 0.90 - eq_idx))
        opp = 0.015 * NAV0 / 3 if t < 3 else 0.0
        fee = pol.rcf * pol.rcf_undrawn_fee / 12 + pol.navf * pol.navf_undrawn_fee / 12
        opex = 0.001 * NAV0 / 12
        net = draw + calls + prem + opp + fee + opex + max(0.0, d_im) - dist - vm - tail - max(0.0, -d_im)
        nco += net
        if t < 12:
            year1_priv_net += dist - calls
        rows.append(dict(net=net, nco=nco, draw=draw, calls=calls, dist=dist, vm=vm, tail=tail,
                         nav=nav_now_est))
        for kk, f in (("tre", 0.0), ("dm", eq[t]), ("em", 1.2 * eq[t]), ("fi", fi[t]), ("hf", hf_r[t])):
            liq_bh[kk] *= 1 + f

    # --- counterbalancing capacity
    idx_eq = np.cumprod(1 + eq)
    idx_em = np.cumprod(1 + 1.2 * eq)
    idx_fi = np.cumprod(1 + fi)
    idx_hf = np.cumprod(1 + hf_r)
    cbc = np.zeros(T)
    hf_monthly = np.zeros(T + 40)
    # monthly HF schedule from the quarterly one (spread evenly within each quarter after the notice)
    for q, share in enumerate(HF_SCHED):
        for mm in range(3):
            hf_monthly[3 * q + mm] += share / 3
    hf_cash = np.zeros(T)
    backlog = 0.0
    for t in range(T):
        due = hf_monthly[t] * HF0 * idx_hf[t] + backlog
        paid = s.hf_pass * due if crisis[t] else due
        backlog = due - paid
        hf_cash[t] = paid
    cum_hf = np.cumsum(hf_cash)
    acc_dm = acc_fi = acc_em = 0.0
    rem_dm = rem_fi = rem_em = 1.0
    tre_cap = tre - enc0
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
        # Treasury: cash / UST / IG at stress haircuts (UST 2%, IG 10%) on the t0 composition
        tre_haircut = 0.4 * 0.0 + 0.27 * 0.02 + 0.33 * 0.10
        cbc[t] = tre_cap * (1 - tre_haircut) + acc_dm + acc_fi + acc_em + cum_hf[t]
    nco_arr = np.array([r["nco"] for r in rows])
    nav_arr = np.array([r["nav"] for r in rows])
    floor_arr = s.floor * nav_arr
    fac = np.array([0.0 if t < 1 else pol.rcf * s.fac_credit for t in range(T)])
    pool = min(0.20 * sum(PRIV0.values()), PRIV0["pe"] + PRIV0["sec"])
    navf_cap = np.array([0.0 if t < 1 else min(pol.navf, s.navf_ltv * pool) for t in range(T)])
    head_tp = cbc - floor_arr - nco_arr
    head_tpf = head_tp + fac + navf_cap

    def first_breach(head):
        br = np.where(head < 0)[0]
        return int(br[0] + 1) if br.size else None

    sh_tp = first_breach(head_tp)
    sh_tpf = first_breach(head_tpf)
    gap = np.maximum(0.0, -(head_tp[1:24] + navf_cap[1:24]))
    fac_need = float(gap.max() / s.fac_credit) if gap.size else 0.0
    month1 = float(max(0.0, -head_tp[0]))
    tp0 = TRE0 + sum(LO0.values()) + HF0
    gap24 = float(nco_arr[23] + (tp0 - sum(liq_bh.values())))   # comparable with the Monte Carlo gap8
    return dict(stress=s.name, policy=pol.name,
                nco12=float(nco_arr[11]), nco24=float(nco_arr[23]),
                draws24=float(sum(r["draw"] for r in rows[:24])),
                calls24=float(sum(r["calls"] for r in rows[:24])),
                dist24=float(sum(r["dist"] for r in rows[:24])),
                year1_private_net=float(year1_priv_net),
                cbc24=float(cbc[23]), floor24=float(floor_arr[23]), nav24=float(nav_arr[23]),
                SH_TP=sh_tp, SH_TPF=sh_tpf, month1_gap=month1,
                min_head_tpf_24=float(head_tpf[:24].min()),
                cushion_24=float(head_tpf[:24].min() / NAV0),
                fac_need_24=fac_need, gap24=gap24,
                gstar=float((-head_tp[:24]).max()))
