"""G14 - Real Assets actions and financing: illustrative calculations.

ALL OUTPUTS ARE SYNTHETIC - NOT ADIC DATA. Every parameter below is a design default
([I]) anchored, where noted, on dated public sources cited in
research/groups/dossiers/G14_ra_actions_financing.md.

Sections
  A. Instrument economics: proceeds, one-off value cost per $ raised (kappa), break-even
     per-period liquidity premium (ell*), all-in REFINANCE spread (s_hat), encumbrance per $.
  B. Open-end redemption-queue machine: cash share by horizon and value cost at ell.
  C. Refinancing-wall Monte Carlo: calibration of the stress regime to the Jiang-Matvos-
     Piskorski-Seru negative-equity shares, then hidden capital calls (cash-in refinancing)
     on a synthetic Real Assets book by regime, under 'ruthless' and 'reputation-bound'
     default policies.
  D. Decision example: liquidity menu for one core logistics asset, merit order by regime.
  E. Look-through and delta-adjusted leverage of the synthetic Real Assets book.
  F. Interest-rate cap price (Bachelier) for the lender-required hedge.

Run:  .venv/Scripts/python.exe -I g14_ra_actions.py   (writes g14_ra_actions_results.json)
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

OUT = Path(__file__).with_name("g14_ra_actions_results.json")
LABEL = "SYNTHETIC - NOT ADIC DATA"

# ----------------------------------------------------------------------------------------
# Market anchors (sourced in the dossier; dated)
# ----------------------------------------------------------------------------------------
SOFR = 0.0389          # 15 Oct 2026, main report section 2.1 [S]
SWAP5_OVER_SOFR = 0.0070  # CBRE Q2-2026 release quotes a ~70bp gap SOFR vs 5y fixed [S, indicative]
CRE_SPREAD_N = 0.0204  # CBRE Q2-2026 commercial mortgage spread, 5-10y fixed [S]
MF_SPREAD_N = 0.0162   # CBRE Q2-2026 multifamily spread [S]

REGIMES = ["N", "T", "C", "GW", "OD"]  # normal, tight (LATE x D), crisis, Gulf war, oil-down (SG/DB)


# ----------------------------------------------------------------------------------------
# A. Instrument economics
# ----------------------------------------------------------------------------------------
def hold_cashflows(V: float, y: float, r_h: float, T: int) -> np.ndarray:
    """Annual unlevered HOLD cash flows whose PV at r_h equals V: income y*V_t, exit at T."""
    g = (1 + r_h) / (1 + y) - 1.0  # value growth so that total return = r_h exactly
    cfs = np.zeros(T)
    v = V
    for t in range(T):
        cfs[t] = y * v          # income on opening value
        v = v * (1 + g)
    cfs[-1] += v
    # rescale so PV at r_h is exactly V (numerical guard)
    pv = sum(cf / (1 + r_h) ** (t + 1) for t, cf in enumerate(cfs))
    return cfs * (V / pv)


def lapv(cfs: np.ndarray, r_h: float, ell: float) -> float:
    return float(sum(cf / ((1 + r_h) * (1 + ell)) ** (t + 1) for t, cf in enumerate(cfs)))


def breakeven_ell(cfs: np.ndarray, r_h: float, proceeds: float) -> float:
    """ell* such that LAPV(HOLD; ell*) = proceeds (SELL ties HOLD). Returns nan if none."""
    f = lambda ell: lapv(cfs, r_h, ell) - proceeds
    if f(0.0) <= 0:
        return 0.0  # SELL already at least as good at ell = 0
    try:
        return brentq(f, 0.0, 5.0)
    except ValueError:
        return float("nan")


def cash_weighted_life(cfs: np.ndarray) -> float:
    t = np.arange(1, len(cfs) + 1)
    return float((t * cfs).sum() / cfs.sum())


@dataclass
class SellCase:
    name: str
    regime: str
    theta: float      # economic value / reported NAV
    price: float      # gross price as fraction of reported NAV (before seller costs)
    seller_costs: float  # broker/legal + seller-borne transfer tax, fraction of price
    months_to_cash: float
    p_success: float

    def evaluate(self, y=0.045, r_h=0.07, T=5) -> dict:
        V = self.theta  # economic value per $1 of NAV
        net = self.price * (1 - self.seller_costs)
        cfs = hold_cashflows(V, y, r_h, T)
        kappa = V / net - 1.0
        # delay: proceeds arrive after months_to_cash; discount at r_f for the wait
        net_pv = net / (1 + SOFR) ** (self.months_to_cash / 12)
        ell_star = breakeven_ell(cfs, r_h, net_pv)
        return {
            "instrument": self.name, "regime": self.regime, "theta": self.theta,
            "price_pct_nav": round(100 * self.price, 1),
            "net_proceeds_pct_nav": round(100 * net, 2),
            "kappa_value_cost_per_usd_raised": round(kappa, 4),
            "breakeven_ell_annual": None if math.isnan(ell_star) else round(ell_star, 4),
            "months_to_cash": self.months_to_cash, "p_success": self.p_success,
            "hold_cash_weighted_life_y": round(cash_weighted_life(cfs), 2),
        }


def sell_library() -> list[dict]:
    """SELL instruments by regime. theta from G13-type staleness priors [I];
    prices anchored: RE LP 68% (Jefferies H1-2026), infra LP 91% (Jefferies) / 95% (CL 5.0% disc.),
    open-end secondary -8%..+3% (Alliance 2020) and -25% bid (DTZ Nov-2022) [S]."""
    cases = [
        # direct core asset sale, US asset deal, seller costs 1.25% fees + 0% tax (seller pays none)
        SellCase("direct_asset_sale_US_lowtax", "N", 1.00, 0.98, 0.0125, 4.5, 0.85),
        SellCase("direct_asset_sale_US_lowtax", "T", 0.95, 0.90, 0.0125, 7.0, 0.70),
        SellCase("direct_asset_sale_US_lowtax", "C", 0.90, 0.80, 0.0125, 10.0, 0.50),
        # NYC-type: seller pays 2.625% city + 0.65% state transfer tax
        SellCase("direct_asset_sale_NYC_seller_tax", "N", 1.00, 0.98, 0.0125 + 0.03275, 4.5, 0.85),
        SellCase("direct_asset_sale_NYC_seller_tax", "C", 0.90, 0.80, 0.0125 + 0.03275, 10.0, 0.50),
        # same sale when the exposure will be rebuilt later: add a UK-type re-entry charge
        # (SDLT 5% + ~1.8% purchaser fees) as kappa_re [I]
        SellCase("direct_asset_sale_with_UKtype_reentry", "N", 1.00, 0.98, 0.0125 + 0.068, 4.5, 0.85),
        # Saudi RETT 5% (seller generally pays)
        SellCase("direct_asset_sale_KSA_RETT5", "N", 1.00, 0.98, 0.0125 + 0.05, 5.0, 0.80),
        SellCase("direct_asset_sale_KSA_RETT5", "OD", 0.90, 0.82, 0.0125 + 0.05, 10.0, 0.45),
        # JV 50% stake sale with ROFR; minority discount on top of asset discount
        SellCase("jv_stake_sale_50pct", "N", 1.00, 0.98 * 0.95, 0.010, 6.0, 0.80),
        SellCase("jv_stake_sale_50pct", "C", 0.90, 0.80 * 0.80, 0.010, 12.0, 0.40),
        # closed-end RE fund LP interest
        SellCase("lp_secondary_real_estate", "N", 0.88, 0.68, 0.010, 4.0, 0.75),
        SellCase("lp_secondary_real_estate", "C", 0.82, 0.57, 0.010, 6.0, 0.45),
        # closed-end infra fund LP interest
        SellCase("lp_secondary_infrastructure", "N", 0.97, 0.93, 0.010, 4.0, 0.85),
        SellCase("lp_secondary_infrastructure", "C", 0.93, 0.82, 0.010, 6.0, 0.55),
        # open-end core unit secondary
        SellCase("open_end_unit_secondary", "N", 0.98, 0.98, 0.005, 1.0, 0.95),
        SellCase("open_end_unit_secondary", "C", 0.90, 0.78, 0.005, 2.0, 0.70),
    ]
    return [c.evaluate() for c in cases]


def refi_spread(s_B: float, fee: float, T_eff: float, cap_cost: float = 0.0,
                cov_charge: float = 0.0, lam_lev: float = 0.0) -> float:
    """Main report REFINANCE metric: s_B + f/T + lambda_Lev + covenant charge (+ hedge cost/T)."""
    return s_B + (fee + cap_cost) / T_eff + lam_lev + cov_charge


def cashout_marginal_rate(D_old: float, L_new: float, r_old: float, r_new: float) -> float:
    """Marginal cost of the incremental cash when cheap old debt is replaced early."""
    dL = L_new - D_old
    return r_new + (D_old / dL) * (r_new - r_old)


def lockin_value(D_old: float, r_old: float, r_new: float, years_left: float) -> float:
    """PV (at r_new) of the coupon saving on below-market debt; lost on early refi or sale."""
    ann = (1 - (1 + r_new) ** (-years_left)) / r_new
    return D_old * (r_new - r_old) * ann


def refi_library() -> list[dict]:
    base_fixed = SOFR + SWAP5_OVER_SOFR  # ~4.59% 5y fixed benchmark [I]
    rows = []
    # (name, regime, borrowing rate, upfront fee, T_eff, cap cost (upfront), covenant charge,
    #  proceeds per $ GAV, encumbrance per $ raised, months to cash, availability)
    spec = [
        ("cashout_refi_unlevered_to_50LTV", "N", base_fixed + CRE_SPREAD_N, 0.015, 5, 0.0, 0.0015, 0.50, 1 / 0.50, 3.0, 0.97),
        ("cashout_refi_unlevered_to_50LTV", "T", base_fixed + CRE_SPREAD_N + 0.010, 0.0175, 5, 0.0, 0.0030, 0.45, 1 / 0.45, 4.5, 0.80),
        ("cashout_refi_unlevered_to_50LTV", "C", base_fixed + 0.0150 + CRE_SPREAD_N + 0.020, 0.020, 5, 0.0, 0.0060, 0.40, 1 / 0.40, 6.0, 0.50),
        ("cashout_refi_unlevered_to_50LTV", "GW", base_fixed + CRE_SPREAD_N + 0.015, 0.020, 5, 0.0, 0.0050, 0.40, 1 / 0.40, 6.0, 0.50),
        ("floating_refi_with_cap_3y", "N", SOFR + 0.0250, 0.0125, 3, 0.0080, 0.0020, 0.55, 1 / 0.55, 2.5, 0.95),
        ("mezz_or_pref_on_cheap_senior", "N", 0.130, 0.015, 4, 0.0, 0.0050, 0.15, 0.0, 2.0, 0.90),
        ("mezz_or_pref_on_cheap_senior", "C", 0.160, 0.020, 4, 0.0, 0.0100, 0.10, 0.0, 3.0, 0.50),
        ("ground_lease_sale", "N", 0.073, 0.020, 30, 0.0, 0.0, 0.35, 0.0, 4.0, 0.80),
        ("sale_leaseback_operating_asset", "N", 0.0725 + 0.012, 0.020, 15, 0.0, 0.0, 0.95, 0.0, 4.0, 0.80),
        ("nav_facility_RE_fund_interests", "N", SOFR + 0.0550, 0.015, 3, 0.0, 0.0050, 0.10, 1 / 0.10, 2.5, 0.70),
        ("nav_facility_infra_fund_interests", "N", SOFR + 0.0375, 0.0125, 4, 0.0, 0.0030, 0.20, 1 / 0.20, 2.5, 0.90),
        ("nav_facility_RE_fund_interests", "C", SOFR + 0.0550 + 0.020, 0.020, 3, 0.0, 0.0150, 0.05, 1 / 0.05, 4.0, 0.30),
        ("infra_holdco_debt_pik_toggle", "N", SOFR + 0.0450, 0.020, 5, 0.0, 0.0060, 0.15, 0.0, 3.0, 0.85),
    ]
    for name, reg, rB, fee, T, cap, cov, proceeds, enc, months, avail in spec:
        s_B = rB - SOFR
        s_hat = refi_spread(s_B, fee, T, cap, cov)
        rows.append({
            "instrument": name, "regime": reg, "borrowing_rate": round(rB, 4),
            "s_B_over_SOFR": round(s_B, 4), "s_hat_all_in": round(s_hat, 4),
            "proceeds_per_usd_GAV": proceeds, "encumbrance_per_usd_raised": round(enc, 2),
            "months_to_cash": months, "availability": avail,
        })
    # cash-out before maturity on cheap legacy debt (lock-in destruction)
    D_old, L_new, r_old = 0.40, 0.55, 0.0375
    r_new = base_fixed + CRE_SPREAD_N
    marg = cashout_marginal_rate(D_old, L_new, r_old, r_new)
    lock2 = lockin_value(D_old, r_old, r_new, 2)
    lock5 = lockin_value(D_old, r_old, r_new, 5)
    extra = {
        "early_cashout_40_to_55LTV_marginal_rate_on_new_cash": round(marg, 4),
        "early_cashout_marginal_spread_over_SOFR": round(marg - SOFR, 4),
        "lockin_value_pct_GAV_2y_left": round(100 * lock2, 2),
        "lockin_value_pct_GAV_5y_left": round(100 * lock5, 2),
        "r_old": r_old, "r_new": round(r_new, 4),
    }
    return rows, extra


# ----------------------------------------------------------------------------------------
# B. Open-end redemption-queue machine
# ----------------------------------------------------------------------------------------
def queue_machine(seed: int = 7, n_paths: int = 20000, quarters: int = 16) -> dict:
    """Pro-rata queue. Each quarter the fund pays a fraction q_z of the outstanding queue.
    q anchored on PREA/Townsend: since 2007 ODCE paid ~71% of queues per quarter on average,
    but only ~5% per quarter in 2023 [S]. Regime chain over {N, T, C} [I]."""
    rng = np.random.default_rng(seed)
    q = {"N": 0.71, "T": 0.20, "C": 0.05}
    states = ["N", "T", "C"]
    P = np.array([[0.90, 0.08, 0.02],
                  [0.10, 0.80, 0.10],
                  [0.03, 0.12, 0.85]])  # quarterly [I]
    results = {}
    for start in states:
        s0 = states.index(start)
        paid_share = np.zeros((n_paths, quarters))
        s = np.full(n_paths, s0)
        outstanding = np.ones(n_paths)
        cum = np.zeros(n_paths)
        for t in range(quarters):
            # first dealing date after notice: payment at end of quarter t
            frac = np.array([q[states[k]] for k in s])
            # payout noise: beta around the regime mean
            a = 8.0
            frac = rng.beta(frac * a + 1e-6, (1 - frac) * a + 1e-6)
            pay = outstanding * frac
            outstanding -= pay
            cum += pay
            paid_share[:, t] = cum
            # transition
            u = rng.random(n_paths)
            cdf = np.cumsum(P[s], axis=1)
            s = (u[:, None] > cdf).sum(axis=1)
        p5 = np.percentile(paid_share, 5, axis=0)
        p50 = np.percentile(paid_share, 50, axis=0)
        mean = paid_share.mean(axis=0)
        # value cost at ell: 1 - E[sum payments discounted at (1+r_f)(1+ell)] (NAV = economic)
        out = {}
        for ell in (0.0, 0.02, 0.05, 0.10, 0.20):
            disc = np.array([((1 + SOFR) * (1 + ell)) ** (-(t + 1) / 4) for t in range(quarters)])
            incr = np.diff(np.concatenate([np.zeros((n_paths, 1)), paid_share], axis=1), axis=1)
            pv = (incr * disc).sum(axis=1) + (1 - paid_share[:, -1]) * disc[-1]
            out[f"value_cost_at_ell_{ell:.2f}"] = round(float(1 - pv.mean()), 4)
        results[start] = {
            "cash_share_P5_by_quarter": [round(x, 3) for x in p5],
            "cash_share_P50_by_quarter": [round(x, 3) for x in p50],
            "cash_share_mean_by_quarter": [round(x, 3) for x in mean],
            **out,
        }
    return {"q_by_regime": q, "transition_quarterly": P.tolist(), "by_start_regime": results}


# ----------------------------------------------------------------------------------------
# C. Refinancing-wall Monte Carlo
# ----------------------------------------------------------------------------------------
@dataclass
class LendTerms:
    base_yield: float    # 5y benchmark at maturity
    spread: float
    ltv_max: float
    dscr_min: float
    dy_min: float
    avail: float         # P(a lender is available at all)
    p_extend: float      # P(extension | no lender)
    sale_disc: float     # forced-sale discount vs economic value


TERMS = {  # [I]; N anchored on CBRE Q2-2026 (LTV 59.6%, DSCR 1.43 avg, DY 10.2% avg, spread 204bp)
    "N":  LendTerms(0.0459, 0.0200, 0.625, 1.25, 0.085, 0.97, 0.70, 0.03),
    "T":  LendTerms(0.0500, 0.0275, 0.575, 1.35, 0.095, 0.85, 0.65, 0.08),
    "C":  LendTerms(0.0475, 0.0375, 0.525, 1.40, 0.105, 0.60, 0.55, 0.15),
    "GW": LendTerms(0.0500, 0.0350, 0.525, 1.40, 0.100, 0.55, 0.50, 0.15),   # Gulf-located assets
    "OD": LendTerms(0.0450, 0.0325, 0.550, 1.35, 0.100, 0.65, 0.55, 0.12),   # Gulf-located, oil-down
}


@dataclass
class Cohort:
    name: str
    gav_bn: float        # gross asset value at ADIC share
    ltv_mean: float
    ltv_sd: float
    cap0: float          # entry cap rate / cash yield on value
    coupon0: float       # legacy coupon
    noi_g: dict          # annual NOI growth by regime
    dcap: dict           # cap-rate change (abs) by regime over the horizon
    vol: float           # idiosyncratic value vol (annual)
    gulf: bool = False


SOFR_SHIFT = {"N": 0.0, "T": 0.0075, "C": 0.0100, "GW": 0.0050, "OD": -0.0025}  # 2y path shift [I]
FLOAT_SPREAD = 0.0300   # value-add / bridge floating loans [I]
CAP_EXPIRES_EARLY = 0.40  # share of floating loans whose cap expires before maturity (CRED iQ 2023) [S]


def infra_terms(t: LendTerms) -> LendTerms:
    """Infrastructure refinances against gearing and DSCR (no debt-yield test), with higher
    gearing tolerance (NBIM per-investment cap 70%; Ofwat PR24 notional gearing 55%) [S anchors, I values]."""
    return LendTerms(t.base_yield, t.spread - 0.0025, min(t.ltv_max + 0.10, 0.75), t.dscr_min - 0.05,
                     0.0, min(t.avail + 0.05, 0.99), t.p_extend, t.sale_disc)


def energy_terms(t: LendTerms, regime: str) -> LendTerms:
    """Reserve-based / project lending for energy and natural resources: the borrowing base is
    an advance rate on PV of reserves at the bank price deck, redetermined semi-annually; no
    debt-yield test. Advance rates fall in oil-down and crisis states (spring-2020 survey: most
    respondents expected borrowing-base cuts of at least 20% [S: Haynes Boone]) [I values]."""
    cut = 0.10 if regime in ("OD", "C") else 0.0
    return LendTerms(t.base_yield, t.spread + 0.0050, max(t.ltv_max - 0.05 - cut, 0.30),
                     t.dscr_min - 0.10, 0.0, t.avail, t.p_extend, t.sale_disc + 0.05)


def simulate_cohort(c: Cohort, regime: str, years: float, n: int, rng, policy: str,
                    ell: float, terms: dict = TERMS) -> dict:
    """Loans maturing at 'years'. Outputs shortfall, cash-in, walk, extension, cash trap."""
    reg_terms = terms[regime]
    if c.name.startswith("infrastructure"):
        reg_terms = infra_terms(reg_terms)
    elif c.name.startswith("energy"):
        reg_terms = energy_terms(reg_terms, regime)
    # Gulf assets use GW/OD terms in those regimes, others use C/T analogues
    ltv0 = np.clip(rng.normal(c.ltv_mean, c.ltv_sd, n), 0.05, 0.90)
    D = ltv0  # V0 = 1
    noi0 = c.cap0
    g = c.noi_g[regime]
    dcap = c.dcap[regime]
    eps_noi = rng.normal(0, 0.06 * math.sqrt(years), n)
    noiT = noi0 * np.exp(g * years + eps_noi)
    capT = np.maximum(c.cap0 + dcap + rng.normal(0, 0.0035, n), 0.03)
    eps_v = rng.normal(0, c.vol * math.sqrt(years), n)
    VT = (noiT / capT) * np.exp(eps_v - 0.5 * (c.vol ** 2) * years)
    r_new = reg_terms.base_yield + reg_terms.spread
    k_new = r_new  # interest-only constant (conservative alternative: amortizing)
    dy_cap = noiT / reg_terms.dy_min if reg_terms.dy_min > 0 else np.full(n, np.inf)
    Lmax = np.minimum.reduce([reg_terms.ltv_max * VT,
                              noiT / (reg_terms.dscr_min * k_new),
                              dy_cap])
    lender = rng.random(n) < reg_terms.avail
    extend = (~lender) & (rng.random(n) < reg_terms.p_extend)
    no_option = (~lender) & (~extend)
    shortfall = np.where(lender, np.maximum(D - Lmax, 0.0), 0.0)
    underwater = VT < D
    # equity decision at a refinancing gap: cure iff V - D - ell*S > max(0, V(1-d) - D)
    sale_val = VT * (1 - reg_terms.sale_disc) - D
    cure_val = VT - D - ell * shortfall
    if policy == "ruthless":
        cure = lender & (shortfall > 0) & (cure_val > np.maximum(0.0, sale_val))
        walk_on_gap = lender & (shortfall > 0) & ~cure & (sale_val <= 0)
        sell_on_gap = lender & (shortfall > 0) & ~cure & (sale_val > 0)
        # no lender and no extension: sell if equity positive, else walk
        walk_forced = no_option & (sale_val <= 0)
        sell_forced = no_option & (sale_val > 0)
    else:  # reputation-bound: never defaults. Gaps are always cured; with no lender and no
        # extension it sells if equity is positive, otherwise repays the loan in full from its
        # own liquidity (the asset becomes unlevered) - the worst case for ADIC's liquidity.
        cure = lender & (shortfall > 0)
        walk_on_gap = np.zeros(n, bool)
        sell_on_gap = np.zeros(n, bool)
        walk_forced = np.zeros(n, bool)
        sell_forced = no_option & (sale_val > 0)
    cash_in = np.where(cure, shortfall, 0.0)
    if policy != "ruthless":
        cash_in = cash_in + np.where(no_option & (sale_val <= 0), D, 0.0)  # full take-out
    # cash trap on a FLOATING-rate sub-book before maturity (value-add / bridge loans, LTV +10pp):
    # DSCR on SOFR path (+ shift) + spread, capped at the strike unless the cap expired early.
    noi_mid = noi0 * np.exp(g * years / 2 + eps_noi / 2)
    D_f = np.clip(D + 0.10, 0.05, 0.95)
    sofr_path = SOFR + SOFR_SHIFT[regime] + rng.normal(0, 0.0075, n)
    strike = SOFR + 0.0050
    capped = rng.random(n) > CAP_EXPIRES_EARLY
    rate_f = np.where(capped, np.minimum(sofr_path, strike), sofr_path) + FLOAT_SPREAD
    dscr_float = noi_mid / (D_f * rate_f)
    trap = dscr_float < 1.15
    return {
        "P_shortfall": float((shortfall > 0).mean()),
        "mean_shortfall_given_gap_pct_D": float((shortfall[shortfall > 0] / D[shortfall > 0]).mean()) if (shortfall > 0).any() else 0.0,
        "P_underwater": float(underwater.mean()),
        "P_cure": float(cure.mean()),
        "P_extend": float(extend.mean()),
        "P_walk": float((walk_on_gap | walk_forced).mean()),
        "P_forced_sale": float((sell_on_gap | sell_forced).mean()),
        "cash_in_per_usd_GAV_mean": float(cash_in.mean()),
        "cash_in_per_usd_GAV_p95": float(np.percentile(cash_in, 95)),
        "P_cash_trap_floating_subbook": float(trap.mean()),
        "mean_value_change": float(VT.mean() - 1.0),
    }


def calibrate_office_stress(rng_seed: int = 11) -> dict:
    """Bank-loan-like book (LTV ~ 62% +/- 12%): find the office cap-rate shock so that ~44% of
    office loans are underwater, and the all-CRE shock so that ~14% are (Jiang et al., NBER w31970,
    loan-level data) [S target]. Horizon 3 years."""
    targets = {"office": 0.44, "all_cre": 0.14}
    out = {}
    for key, tgt, g in (("office", targets["office"], -0.03), ("all_cre", targets["all_cre"], 0.0)):
        def gap(dcap):
            rng = np.random.default_rng(rng_seed)
            c = Cohort(key, 1.0, 0.62, 0.12, 0.060, 0.040, {"C": g}, {"C": dcap}, 0.10)
            r = simulate_cohort(c, "C", 3.0, 40000, rng, "ruthless", 0.0)
            return r["P_underwater"] - tgt
        dcap = brentq(gap, 0.0, 0.06)
        out[key] = {"target_P_underwater": tgt, "calibrated_cap_rate_shock_abs": round(dcap, 4),
                    "noi_growth_assumed": g}
    return out


def synthetic_ra_book() -> list[Cohort]:
    """G14 synthetic Real Assets book with asset-level debt (ADIC share), $bn GAV.
    Direct/JV sleeves carry ~$12.0bn of equity (GAV $22.8bn); fund interests ($6bn NAV) are
    handled through look-through in section E; together $18.0bn = working allocation v2.
    Sectors follow the user's confirmed scope (real estate, infrastructure, energy & natural
    resources; no agriculture or timber). [I]"""
    return [
        # office C-regime shock = the Jiang-et-al. calibration (+242bp, NOI -3%/yr), see section C
        Cohort("office_US_EU", 2.4, 0.50, 0.10, 0.065, 0.040,
               {"N": 0.01, "T": -0.01, "C": -0.03, "GW": 0.0, "OD": 0.0},
               {"N": 0.000, "T": 0.0075, "C": 0.0242, "GW": 0.0025, "OD": 0.0025}, 0.10),
        Cohort("logistics", 4.2, 0.42, 0.08, 0.050, 0.035,
               {"N": 0.035, "T": 0.025, "C": 0.0, "GW": 0.03, "OD": 0.03},
               {"N": 0.000, "T": 0.0050, "C": 0.0125, "GW": 0.0, "OD": 0.0}, 0.08),
        Cohort("residential", 3.6, 0.48, 0.08, 0.048, 0.037,
               {"N": 0.03, "T": 0.02, "C": 0.0, "GW": 0.025, "OD": 0.025},
               {"N": 0.000, "T": 0.0050, "C": 0.0100, "GW": 0.0, "OD": 0.0}, 0.08),
        Cohort("retail_hotel", 1.6, 0.50, 0.10, 0.070, 0.045,
               {"N": 0.02, "T": 0.0, "C": -0.06, "GW": -0.02, "OD": -0.02},
               {"N": 0.000, "T": 0.0075, "C": 0.0150, "GW": 0.0050, "OD": 0.0050}, 0.12),
        Cohort("gulf_mixed_use", 2.0, 0.45, 0.10, 0.070, 0.050,
               {"N": 0.03, "T": 0.01, "C": -0.05, "GW": -0.08, "OD": -0.06},
               {"N": 0.000, "T": 0.0050, "C": 0.0150, "GW": 0.0200, "OD": 0.0175}, 0.12, gulf=True),
        Cohort("infrastructure_core", 6.2, 0.55, 0.08, 0.060, 0.040,
               {"N": 0.03, "T": 0.025, "C": 0.0, "GW": 0.02, "OD": 0.0},
               {"N": 0.000, "T": 0.0050, "C": 0.0100, "GW": 0.0025, "OD": 0.0050}, 0.07),
        # energy & natural resources (confirmed in scope by the user): co-investments and direct
        # assets with reserve-based / project debt; cash flow strongly oil-linked [I]. Equity
        # $1.8bn closes the $18bn working allocation. Its borrowing base is redetermined
        # semi-annually, so all of its debt faces a 'maturity' event within 24 months.
        Cohort("energy_natural_resources", 2.77, 0.35, 0.10, 0.100, 0.060,
               {"N": 0.02, "T": 0.0, "C": -0.12, "GW": 0.10, "OD": -0.15},
               {"N": 0.000, "T": 0.0050, "C": 0.0150, "GW": -0.0050, "OD": 0.0200}, 0.25),
    ]


def refinancing_wall(seed: int = 2026) -> dict:
    rng = np.random.default_rng(seed)
    book = synthetic_ra_book()
    share_maturing_24m = 0.40  # staggered 5-year loans [I]
    years = 2.0
    out = {"share_of_asset_level_debt_maturing_within_24m": share_maturing_24m, "regimes": {}}
    for regime in REGIMES:
        reg_rows = {}
        tot = {"ruthless": {"cash_in_mean": 0.0, "cash_in_p95": 0.0, "walk_gav": 0.0},
               "reputation_bound": {"cash_in_mean": 0.0, "cash_in_p95": 0.0}}
        for c in book:
            # Gulf-located assets face GW/OD lending terms; non-Gulf assets face the T terms in
            # the GW and OD regimes (global markets tight but open) [I]. Value/NOI dynamics
            # always follow the scenario regime; only the lending terms are remapped.
            reg_for_terms = regime
            if regime in ("GW", "OD") and not c.gulf:
                reg_for_terms = "T"
            ell = {"N": 0.01, "T": 0.03, "C": 0.10, "GW": 0.05, "OD": 0.06}[regime]
            if c.name.startswith("energy"):
                # reserve-based lending reacts to the oil state directly: generous price decks in
                # an oil-up Gulf-war state (normal terms), tight decks in oil-down (OD terms)
                reg_for_terms = {"GW": "N"}.get(regime, regime)
            r_ruth = simulate_cohort_mixed(c, regime, reg_for_terms, years, 20000, rng, "ruthless", ell)
            r_rep = simulate_cohort_mixed(c, regime, reg_for_terms, years, 20000, rng, "reputation", ell)
            share = 1.0 if c.name.startswith("energy") else share_maturing_24m
            mat_gav = c.gav_bn * share
            reg_rows[c.name] = {
                "gav_bn": c.gav_bn, "maturing_gav_bn_24m": round(mat_gav, 2),
                "ruthless": {k: round(v, 4) for k, v in r_ruth.items()},
                "reputation_bound": {k: round(v, 4) for k, v in r_rep.items()},
                "cash_in_bn_mean_ruthless": round(mat_gav * r_ruth["cash_in_per_usd_GAV_mean"], 3),
                "cash_in_bn_mean_reputation": round(mat_gav * r_rep["cash_in_per_usd_GAV_mean"], 3),
            }
            tot["ruthless"]["cash_in_mean"] += mat_gav * r_ruth["cash_in_per_usd_GAV_mean"]
            tot["ruthless"]["walk_gav"] += mat_gav * r_ruth["P_walk"]
            tot["reputation_bound"]["cash_in_mean"] += mat_gav * r_rep["cash_in_per_usd_GAV_mean"]
            # comonotone upper bound for P95 of the book (sum of cohort P95s)
            tot["ruthless"]["cash_in_p95"] += mat_gav * r_ruth["cash_in_per_usd_GAV_p95"]
            tot["reputation_bound"]["cash_in_p95"] += mat_gav * r_rep["cash_in_per_usd_GAV_p95"]
        out["regimes"][regime] = {"cohorts": reg_rows,
                                  "book_totals_bn": {p: {k: round(v, 3) for k, v in d.items()} for p, d in tot.items()}}
    return out


def simulate_cohort_mixed(c: Cohort, value_regime: str, terms_regime: str, years: float, n: int,
                          rng, policy: str, ell: float) -> dict:
    """Value/NOI follow value_regime; lending terms follow terms_regime."""
    if value_regime == terms_regime:
        return simulate_cohort(c, value_regime, years, n, rng, policy, ell)
    # build a temporary terms dict mapping value_regime -> terms of terms_regime
    tmp = dict(TERMS)
    tmp[value_regime] = TERMS[terms_regime]
    return simulate_cohort(c, value_regime, years, n, rng, policy, ell, tmp)


# ----------------------------------------------------------------------------------------
# D. Decision example: one core logistics asset needing liquidity
# ----------------------------------------------------------------------------------------
def annuity(r: float, T: float) -> float:
    return (1 - (1 + r) ** (-T)) / r


def decision_example() -> dict:
    """GAV $500m, debt $200m (40% LTV, 3.75% fixed, 2 years left), NOI yield 5.0%, fused
    unlevered expected return 7.0%. Raise cash; compare menus by regime in common units:
      kappa_oneoff = one-off value given up per $ raised (sales: discount + costs + lost lock-in);
      s_hat        = per-period cost of borrowed cash over SOFR (main report REFINANCE metric);
      kappa(T)     = kappa_oneoff + s_hat * annuity(T) : total cost per $ if the cash is needed
                     for T years. SELL has no running cost (fair-value exit), so kappa(T) = kappa_oneoff.
    A REFINANCE beats a SELL for a need of T years iff kappa_REFI(T) < kappa_SELL."""
    V, D, r_h, y = 500.0, 200.0, 0.07, 0.05
    r_old, years_left = 0.0375, 2
    base_fixed = SOFR + SWAP5_OVER_SOFR
    r_new = base_fixed + CRE_SPREAD_N
    menus = {}
    for regime, d_sale, months_sale, p_ok in (("N", 0.02, 4.5, 0.85), ("T", 0.08, 7, 0.7), ("C", 0.15, 10, 0.5)):
        spread_add = {"N": 0.0, "T": 0.010, "C": 0.030}[regime]
        r_reg = r_new + spread_add
        lock = lockin_value(D, r_old, r_reg, years_left)
        rows = []
        # 1. SELL 100%: asset deal, seller costs 1.25%; legacy loan repaid at par (not assumable)
        gross = V * (1 - d_sale) * (1 - 0.0125)
        cash = gross - D
        k1 = (V - gross + lock) / cash
        rows.append({"action": "SELL_100pct", "cash_m": round(cash, 1), "kappa_oneoff": round(k1, 4),
                     "s_hat": 0.0, "months": months_sale, "p_success": p_ok})
        # 2. JV sell-down of 49% of the equity (control retained); minority discount 3/8/15%
        mdisc = {"N": 0.03, "T": 0.08, "C": 0.15}[regime]
        E = V - D
        px = 0.49 * E * (1 - d_sale) * (1 - mdisc) * (1 - 0.01)
        k2 = (0.49 * E - px) / px
        rows.append({"action": "JV_selldown_49pct", "cash_m": round(px, 1), "kappa_oneoff": round(k2, 4),
                     "s_hat": 0.0, "months": months_sale + 1.5, "p_success": p_ok})
        # 3. Early cash-out refi 40% -> LTV_new; destroys the lock-in; fees 1.5% of the new loan
        ltv_new = {"N": 0.55, "T": 0.50, "C": 0.45}[regime]
        L_new = ltv_new * V
        cash3 = L_new - D - 0.015 * L_new
        k3 = (0.015 * L_new + lock) / cash3
        s3 = (r_reg - SOFR) * (L_new - D) / cash3
        rows.append({"action": "cashout_refi_early", "cash_m": round(cash3, 1), "kappa_oneoff": round(k3, 4),
                     "s_hat": round(s3, 4), "months": {"N": 3, "T": 4.5, "C": 6}[regime],
                     "p_success": {"N": 0.97, "T": 0.8, "C": 0.5}[regime],
                     "marginal_rate_on_new_cash": round(cashout_marginal_rate(D, L_new, r_old, r_reg), 4)})
        # 3b. Same cash-out at the loan's maturity (no lock-in lost): the main report's REFINANCE
        cash3b = L_new - D - 0.015 * (L_new - D)
        rows.append({"action": "cashout_refi_at_maturity", "cash_m": round(cash3b, 1),
                     "kappa_oneoff": round(0.015 * (L_new - D) / cash3b, 4),
                     "s_hat": round((r_reg - SOFR) * (L_new - D) / cash3b, 4),
                     "months": {"N": 3, "T": 4.5, "C": 6}[regime],
                     "p_success": {"N": 0.97, "T": 0.8, "C": 0.5}[regime]})
        # 4. Mezzanine / preferred equity on top of the cheap senior (stack to 55%; 50% in C)
        rp = {"N": 0.13, "T": 0.145, "C": 0.16}[regime]
        amt = (0.55 - 0.40) * V if regime != "C" else 0.10 * V
        cash4 = amt * (1 - 0.015)
        rows.append({"action": "mezz_pref_on_senior", "cash_m": round(cash4, 1),
                     "kappa_oneoff": round(0.015 * amt / cash4, 4), "s_hat": round((rp - SOFR) * amt / cash4, 4),
                     "months": {"N": 2, "T": 3, "C": 3}[regime], "p_success": {"N": 0.9, "T": 0.75, "C": 0.5}[regime]})
        for r in rows:
            for T in (1, 2, 5):
                r[f"kappa_T{T}"] = round(r["kappa_oneoff"] + r["s_hat"] * annuity(SOFR, T), 4)
        menus[regime] = {"lockin_value_m": round(lock, 2), "r_new": round(r_reg, 4),
                         "rows": sorted(rows, key=lambda r: r["kappa_T2"])}
    return {"asset": {"GAV_m": V, "debt_m": D, "legacy_coupon": r_old, "years_left": years_left,
                      "unlevered_expected_return": r_h, "noi_yield": y},
            "menus": menus}


# ----------------------------------------------------------------------------------------
# E. Look-through and delta-adjusted leverage of the synthetic RA book
# ----------------------------------------------------------------------------------------
def merton_delta(V: float, D: float, sigma: float, T: float, r: float) -> float:
    if D <= 0:
        return 1.0
    d1 = (math.log(V / D) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return float(norm.cdf(d1))


def lookthrough(book: list[Cohort]) -> dict:
    rows = []
    tot_gav = tot_debt = tot_eq = tot_delta_exp = 0.0
    for c in book:
        debt = c.gav_bn * c.ltv_mean
        eq = c.gav_bn - debt
        sig = c.vol + 0.08  # total asset vol incl. systematic [I]
        delta = merton_delta(1.0, c.ltv_mean, sig, 3.0, SOFR)
        rows.append({"cohort": c.name, "gav_bn": c.gav_bn, "debt_bn": round(debt, 2),
                     "equity_bn": round(eq, 2), "ltv": c.ltv_mean, "delta_equity_wrt_V": round(delta, 3),
                     "delta_adj_exposure_bn": round(delta * c.gav_bn, 2)})
        tot_gav += c.gav_bn; tot_debt += debt; tot_eq += eq; tot_delta_exp += delta * c.gav_bn
    # fund interests (closed-end RE/infra $4bn NAV at fund LTV 50%; open-end core $2bn at 27.1%)
    funds = [("closed_end_RE_infra_funds", 4.0, 0.50), ("open_end_core_RE", 2.0, 0.271)]
    for name, nav, ltv in funds:
        gav = nav / (1 - ltv)
        debt = gav - nav
        rows.append({"cohort": name, "gav_bn": round(gav, 2), "debt_bn": round(debt, 2),
                     "equity_bn": nav, "ltv": ltv})
        tot_gav += gav; tot_debt += debt; tot_eq += nav; tot_delta_exp += gav  # delta ~1 (fund level)
    return {
        "rows": rows,
        "totals_bn": {"gav": round(tot_gav, 2), "lookthrough_debt": round(tot_debt, 2),
                      "equity_nav": round(tot_eq, 2), "portfolio_ltv": round(tot_debt / tot_gav, 3),
                      "delta_adjusted_exposure": round(tot_delta_exp, 2)},
        "comparison": {"T5_recourse_target_bn_at_177": 17.7, "T5_recourse_hard_bn_at_177": 26.6,
                       "lookthrough_debt_as_pct_fund_NAV_177": round(100 * tot_debt / 177.0, 1)},
    }


# ----------------------------------------------------------------------------------------
# F. Lender-required interest-rate cap (Bachelier caplets on 3M SOFR)
# ----------------------------------------------------------------------------------------
def cap_price(notional: float, strike: float, fwd: float, normal_vol: float, years: float,
              r_disc: float) -> float:
    pv = 0.0
    dt = 0.25
    for i in range(1, int(round(years / dt)) + 1):
        T = i * dt - dt  # fixing time
        if T <= 0:
            continue
        sd = normal_vol * math.sqrt(T)
        d = (fwd - strike) / sd
        caplet = (fwd - strike) * norm.cdf(d) + sd * norm.pdf(d)
        pv += caplet * dt * math.exp(-r_disc * (T + dt))
    return notional * pv


def cap_examples() -> dict:
    ex = {}
    for vol_bp in (80, 110, 150):
        for strike in (0.045, 0.050, 0.055):
            p = cap_price(1.0, strike, SOFR, vol_bp / 1e4, 3.0, SOFR)
            ex[f"3y_strike_{strike:.3f}_vol_{vol_bp}bp_pct_notional"] = round(100 * p, 3)
    return ex


def delta_table() -> dict:
    """Equity delta dE/dV of a non-recourse-levered asset (Merton call, 3y, sigma 18%) by LTV.
    Under a ruthless (walk-away) policy ADIC's economic exposure is delta*GAV; a
    reputation-bound sponsor has delta = 1 (debt is economically recourse)."""
    return {f"LTV_{ltv:.2f}": round(merton_delta(1.0, ltv, 0.18, 3.0, SOFR), 3)
            for ltv in (0.40, 0.55, 0.70, 0.85, 1.00, 1.15)}


def sell_vs_refi_threshold(menus: dict) -> dict:
    """T* (years) at which kappa_REFI(T) = kappa_SELL-type action: borrowing beats selling only
    if the cash is repaid within T*. Compares cash-out-at-maturity and mezz/pref against the
    cheapest sale-type action (JV sell-down or SELL 100%)."""
    out = {}
    for regime, m in menus.items():
        rows = {r["action"]: r for r in m["rows"]}
        k_sell = min(rows["JV_selldown_49pct"]["kappa_oneoff"], rows["SELL_100pct"]["kappa_oneoff"])
        res = {}
        for refi in ("cashout_refi_at_maturity", "mezz_pref_on_senior"):
            r = rows[refi]
            target = (k_sell - r["kappa_oneoff"]) / r["s_hat"] if r["s_hat"] > 0 else float("inf")
            # invert annuity at SOFR
            if target <= 0:
                T = 0.0
            elif target >= 1 / SOFR:
                T = float("inf")
            else:
                T = -math.log(1 - target * SOFR) / math.log(1 + SOFR)
            res[refi] = round(T, 2)
        out[regime] = {"kappa_cheapest_sale": k_sell, "T_star_years": res}
    return out


def headroom_cost(sell_rows: list[dict], refi_rows: list[dict], menus: dict) -> dict:
    """Approximate conversion to the groups report's lever units: PV cost per $ of month-24
    T4' headroom ~ cost per $ raised / kappa_24, kappa_24 = 0.825 (groups report section 4.8),
    with no alpha-carry term (fused alpha* of core real assets ~ 0). Not a ladder run."""
    k24 = 0.825
    out = {"kappa_24": k24, "levers": {}}
    for r in sell_rows:
        key = f"{r['instrument']}|{r['regime']}"
        out["levers"][key] = round(r["kappa_value_cost_per_usd_raised"] / k24, 3)
    for regime, m in menus.items():
        for r in m["rows"]:
            key = f"decision_{r['action']}|{regime}"
            out["levers"][key] = round(r["kappa_T2"] / k24, 3)
    for r in refi_rows:
        key = f"{r['instrument']}|{r['regime']}"
        out["levers"][key] = round(r["s_hat_all_in"] * annuity(SOFR, 2) / k24, 3)
    return out


def main() -> None:
    rows_refi, refi_extra = refi_library()
    sells = sell_library()
    dec = decision_example()
    results = {
        "label": LABEL,
        "anchors": {"SOFR": SOFR, "five_year_fixed_benchmark": round(SOFR + SWAP5_OVER_SOFR, 4),
                    "CRE_spread_N": CRE_SPREAD_N, "MF_spread_N": MF_SPREAD_N},
        "A_sell_library": sells,
        "A_refi_library": rows_refi,
        "A_refi_lockin": refi_extra,
        "A_headroom_cost_conversion": headroom_cost(sells, rows_refi, dec["menus"]),
        "B_queue_machine": queue_machine(),
        "C_calibration_jiang_targets": calibrate_office_stress(),
        "C_refinancing_wall": refinancing_wall(),
        "D_decision_example": dec,
        "D_sell_vs_refi_threshold": sell_vs_refi_threshold(dec["menus"]),
        "E_lookthrough": lookthrough(synthetic_ra_book()),
        "E_delta_by_ltv": delta_table(),
        "F_cap_prices": cap_examples(),
    }
    OUT.write_text(json.dumps(results, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
