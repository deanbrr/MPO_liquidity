"""
G4 Co-investment stream: calibration and analytics behind
research/groups/dossiers/G4_coinvest.md  (as of 2026-10-18)

EVERYTHING PRODUCED HERE IS SYNTHETIC / ILLUSTRATIVE ([I]) except the sourced
calibration targets in the TARGETS block, which are copied from the cited papers.
No ADIC data is used.  Seeded and deterministic.

Run:  <venv>/python -I G4_coinvest_calcs.py
Writes G4_coinvest_calcs_results.json next to this file.

Sections
  1. Structural (levered-equity) fit of the deal-level gross multiple distribution
     to Braun, Jenkinson & Schemmerl (2020) Table 4 (buyout co-investments).
  2. Portfolio diversification: N deals, one-factor correlation.
  3. Fee and carry drag: 0/0, 1/10, 0/20 deal-by-deal vs fund-style 2/20 pooled.
  4. Exit hazard: Weibull fit to Kaplan & Stromberg (2008/2009) cumulative exits,
     regime scaling.
  5. Concentration analytics for an illustrative $18bn co-investment book.
  6. Decision economics: SELL / HOLD / REFINANCE / LEVER on one position.
"""
from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy import optimize, stats

SEED = 20261018
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "G4_coinvest_calcs_results.json")

# ---------------------------------------------------------------------------
# TARGETS (sourced)
# ---------------------------------------------------------------------------
# Braun, Jenkinson & Schemmerl (2020) JFE 136(1):44-62, Table 4 Panel A,
# gross PME of 365 buyout co-investments (winsorized at the 99th percentile).
BJS = dict(p25=0.26, p50=1.16, p75=2.45, p99=8.43, mean=1.76, sd=2.10, skew=2.50)
# Same paper: buyout "other" deals (5,399) and buyout funds (246), for reference.
BJS_OTHER = dict(p25=0.41, p50=1.13, p75=2.15, p99=11.35, mean=1.70, sd=2.15)
BJS_FUND_NET_PME = 1.36          # Table 7, weighted net PME of buyout funds
BJS_SIM_MEDIANS_NOFEE = {1: 1.16, 5: 1.48, 10: 1.63, 50: 1.65}  # Table 8 (net-net, 0/0)
# Kaplan & Stromberg (2008) NBER w14207 Table 2: share of LBOs exited within t years.
KS_EXIT = {2.0: 0.12, 5.0: 0.42, 6.0: 0.51, 7.0: 0.58, 10.0: 0.76}

Z = {q: stats.norm.ppf(q) for q in (0.25, 0.50, 0.75, 0.99)}


# ---------------------------------------------------------------------------
# 1. Structural fit:  M = max(G - L, 0) / (1 - L),  ln G ~ N(mu, s^2)
#    G = enterprise value relative to entry (PME space), L = entry debt / EV.
# ---------------------------------------------------------------------------
def m_quantile(q: float, mu: float, s: float, L: float) -> float:
    g = math.exp(mu + s * stats.norm.ppf(q))
    return max(g - L, 0.0) / (1.0 - L)


def lognorm_partial(mu: float, s: float, a: float, b: float) -> float:
    """E[G ; a < G < b] for ln G ~ N(mu, s^2)."""
    ea = (math.log(a) - mu - s * s) / s if a > 0 else -np.inf
    eb = (math.log(b) - mu - s * s) / s if np.isfinite(b) else np.inf
    return math.exp(mu + 0.5 * s * s) * (stats.norm.cdf(eb) - stats.norm.cdf(ea))


def m_mean_winsorized(mu: float, s: float, L: float, q: float = 0.99) -> float:
    g99 = math.exp(mu + s * stats.norm.ppf(q))
    m99 = max(g99 - L, 0.0) / (1 - L)
    pa = stats.norm.cdf((math.log(L) - mu) / s)
    body = (lognorm_partial(mu, s, L, g99) - L * (q - pa)) / (1 - L)
    return body + (1 - q) * m99


def m_moments_mc(mu: float, s: float, L: float, n: int = 400_000, seed: int = SEED):
    rng = np.random.default_rng(seed)
    g = np.exp(mu + s * rng.standard_normal(n))
    m = np.maximum(g - L, 0.0) / (1 - L)
    m99 = np.quantile(m, 0.99)
    mw = np.minimum(m, m99)
    return dict(
        mean_w=float(mw.mean()), sd_w=float(mw.std()), skew_w=float(stats.skew(mw)),
        p_zero=float((m <= 1e-12).mean()), p_lt_050=float((m < 0.5).mean()),
        p_lt_1=float((m < 1.0).mean()), p_gt_3=float((m > 3.0).mean()),
        p10=float(np.quantile(m, 0.10)), p90=float(np.quantile(m, 0.90)),
    )


def fit_structural(L: float):
    def loss(x):
        mu, s = x[0], abs(x[1]) + 1e-6
        err = []
        for key, q in (("p25", 0.25), ("p50", 0.50), ("p75", 0.75), ("p99", 0.99)):
            mq = max(m_quantile(q, mu, s, L), 1e-3)
            err.append(math.log(mq / BJS[key]))
        err.append(math.log(m_mean_winsorized(mu, s, L) / BJS["mean"]))
        return float(np.sum(np.square(err)))

    res = optimize.minimize(loss, x0=[0.05, 0.65], method="Nelder-Mead",
                            options=dict(xatol=1e-7, fatol=1e-10, maxiter=4000))
    mu, s = res.x[0], abs(res.x[1])
    fitted = {k: m_quantile(q, mu, s, L) for k, q in
              (("p25", 0.25), ("p50", 0.50), ("p75", 0.75), ("p99", 0.99))}
    fitted["mean_w"] = m_mean_winsorized(mu, s, L)
    mc = m_moments_mc(mu, s, L)
    return dict(L=L, mu=mu, sigma=s, loss=res.fun, fitted=fitted, mc=mc)


def section1():
    fits = [fit_structural(L) for L in (0.45, 0.50, 0.55, 0.60, 0.65)]
    best = min(fits, key=lambda d: d["loss"])
    hold_years = 4.5  # approx. BJS/BJSt holding periods (3.8 incl. unrealized, 4.3 realized)
    for f in fits:
        f["sigma_annual_if_T4.5"] = f["sigma"] / math.sqrt(hold_years)
        f["mu_annual_if_T4.5"] = f["mu"] / hold_years
    return dict(fits=fits, best_L=best["L"], hold_years_assumed=hold_years)


# ---------------------------------------------------------------------------
# 1b. Extended static model used as the house calibration:
#     ln G = mu + s*eps + J*B,  B ~ Bern(p_u), J ~ Exp(mean m_u)   (upside jumps)
#     M = max(G - L, 0)/(1 - L)          if G >= L   (going concern)
#     M = R * U, U ~ U(0,1)              if G <  L   (distress: restructuring residual,
#                                                     interim distributions already received)
#     Targets: BJS quartiles, p99, winsorized mean and sd; LPG (2015): ~1 in 10 deals
#     returns no money  ->  P(M < 0.05) ~ 0.10 (soft target).
# ---------------------------------------------------------------------------
N_CRN = 300_000
_rng_crn = np.random.default_rng(SEED + 11)
CRN = dict(eps=_rng_crn.standard_normal(N_CRN), u_jump=_rng_crn.random(N_CRN),
           e_jump=_rng_crn.exponential(1.0, N_CRN), u_rec=_rng_crn.random(N_CRN))


def ext_draw(theta, L, crn=CRN, eps=None):
    mu, s, p_u, m_u, R = theta
    e = crn["eps"] if eps is None else eps
    lng = mu + s * e + (crn["u_jump"] < p_u) * crn["e_jump"] * m_u
    g = np.exp(lng)
    m = np.where(g >= L, (g - L) / (1 - L), R * crn["u_rec"])
    return m


def ext_stats(m):
    m99 = np.quantile(m, 0.99)
    mw = np.minimum(m, m99)
    q = np.quantile(m, [0.10, 0.25, 0.50, 0.75, 0.90, 0.99])
    return dict(p10=float(q[0]), p25=float(q[1]), p50=float(q[2]), p75=float(q[3]),
                p90=float(q[4]), p99=float(q[5]), mean_w=float(mw.mean()), sd_w=float(mw.std()),
                skew_w=float(stats.skew(mw)), p_lt_005=float((m < 0.05).mean()),
                p_lt_050=float((m < 0.5).mean()), p_lt_1=float((m < 1.0).mean()),
                p_gt_3=float((m > 3.0).mean()), p_gt_5=float((m > 5.0).mean()))


def fit_extended(L: float, p_max: float = 0.30):
    """Rare upside jumps: jump probability per deal life capped at p_max (interpretability)."""
    def unpack(x):
        return (x[0], math.exp(x[1]), p_max / (1 + math.exp(-x[2])), math.exp(x[3]),
                1 / (1 + math.exp(-x[4])))

    def loss(x):
        th = unpack(x)
        st = ext_stats(ext_draw(th, L))
        err = [math.log(max(st[k], 1e-3) / BJS[k]) for k in ("p25", "p50", "p75", "p99")]
        err += [math.log(st["mean_w"] / BJS["mean"]), math.log(st["sd_w"] / BJS["sd"])]
        err += [0.3 * math.log(max(st["skew_w"], 0.1) / BJS["skew"])]
        err += [0.5 * (st["p_lt_005"] - 0.10) / 0.10]
        return float(np.sum(np.square(err)))

    res = None
    for x0 in ([-0.1, math.log(0.45), 0.0, math.log(0.8), -2.0],
               [-0.2, math.log(0.40), 1.0, math.log(1.0), -2.0],
               [0.0, math.log(0.50), -1.0, math.log(0.6), -2.0]):
        r = optimize.minimize(loss, x0, method="Nelder-Mead",
                              options=dict(maxiter=6000, xatol=1e-6, fatol=1e-9))
        if res is None or r.fun < res.fun:
            res = r
    th = unpack(res.x)
    st = ext_stats(ext_draw(th, L))
    return dict(L=L, mu=th[0], sigma=th[1], p_jump=th[2], mean_jump=th[3], R_max=th[4],
                loss=float(res.fun), stats=st)


def section1b():
    fits = [fit_extended(L) for L in (0.55, 0.60, 0.65, 0.70)]
    best = min(fits, key=lambda d: d["loss"])
    return dict(fits=fits, best_L=best["L"])


def section1c(theta, L_hist):
    """Translate the historically calibrated EV process to other leverage levels.
    Same EV distribution (theta), different L.  [I] - ignores selection of
    lower-volatility firms into lower leverage and entry-multiple effects."""
    out = {}
    for label, L in (("hist_fit", L_hist), ("today_~36-40%_debt/EV", 0.40),
                     ("6.0x_debt_at_12x_EV", 0.50), ("7.0x_debt_at_12x_EV", 7 / 12),
                     ("6.0x_debt_at_10x_EV", 0.60)):
        out[label] = dict(L=L, **ext_stats(ext_draw(theta, L)))
    # entry-multiple compression sensitivity: shift ln G by -0.07 (14x -> 13x exit) [I]
    th2 = (theta[0] - math.log(14 / 13),) + tuple(theta[1:])
    out["today_L0.40_with_14x_to_13x_compression"] = dict(L=0.40, **ext_stats(ext_draw(th2, 0.40)))
    return out


# ---------------------------------------------------------------------------
# 2. Portfolio diversification (equal weights, one-factor Gaussian in ln G)
# ---------------------------------------------------------------------------
def simulate_deals(n_port: int, n_deals: int, theta, L: float, rho: float,
                   rng: np.random.Generator, n_vintages: int = 1, rho_v: float = 0.0):
    """Deal multiples under the extended model with a one- or two-level Gaussian factor.
    rho: global factor loading^2; rho_v: vintage factor loading^2 (deals split evenly
    across n_vintages)."""
    mu, s, p_u, m_u, R = theta
    zc = rng.standard_normal((n_port, 1))
    zv = rng.standard_normal((n_port, n_vintages))
    vint = np.arange(n_deals) % n_vintages
    ze = rng.standard_normal((n_port, n_deals))
    z = (math.sqrt(rho) * zc + math.sqrt(rho_v) * zv[:, vint]
         + math.sqrt(1 - rho - rho_v) * ze)
    jump = (rng.random((n_port, n_deals)) < p_u) * rng.exponential(m_u, (n_port, n_deals))
    g = np.exp(mu + s * z + jump)
    rec = R * rng.random((n_port, n_deals))
    return np.where(g >= L, (g - L) / (1 - L), rec)


def section2(theta, L: float):
    rng = np.random.default_rng(SEED + 2)
    out = {}
    for rho in (0.0, 0.10, 0.20, 0.30):
        rows = {}
        for n in (1, 5, 10, 20, 30, 50, 100):
            m = simulate_deals(20_000, n, theta, L, rho, rng).mean(axis=1)
            q05 = np.quantile(m, 0.05)
            rows[n] = dict(
                mean=float(m.mean()), median=float(np.median(m)), p05=float(q05),
                p10=float(np.quantile(m, 0.10)), p_lt_1=float((m < 1.0).mean()),
                p_lt_fund_net=float((m < BJS_FUND_NET_PME).mean()),
                cvar05=float(m[m <= q05].mean()),
            )
        out[f"rho={rho:.2f}"] = rows
    # deals needed so that P(portfolio multiple < 1) <= 5% and the
    # idiosyncratic variance share <= 10% (closed form for the latter)
    need = {}
    for rho_key, rows in out.items():
        n_ok = [n for n, r in rows.items() if r["p_lt_1"] <= 0.05]
        need[rho_key] = min(n_ok) if n_ok else None
    idio_share = {}
    for rho in (0.10, 0.20, 0.30):
        # share of variance that is idiosyncratic = (1-rho)/N / (rho + (1-rho)/N)
        n10 = math.ceil((1 - rho) * 9 / rho)   # solve share <= 10%
        idio_share[f"rho={rho:.2f}"] = n10
    # time (vintage) diversification: 60 deals, global rho 0.05, vintage rho 0.20
    vint = {}
    for v in (1, 2, 4, 6, 8):
        m = simulate_deals(20_000, 60, theta, L, 0.05, rng, n_vintages=v, rho_v=0.20).mean(axis=1)
        q05 = np.quantile(m, 0.05)
        vint[v] = dict(mean=float(m.mean()), median=float(np.median(m)), p05=float(q05),
                       p_lt_1=float((m < 1.0).mean()),
                       p_lt_fund_net=float((m < BJS_FUND_NET_PME).mean()),
                       cvar05=float(m[m <= q05].mean()))
    return dict(table=out, n_for_p_lt1_le5pct=need, n_for_idio_share_le10pct=idio_share,
                vintage_diversification_60deals=vint,
                bjs_sim_medians_nofee=BJS_SIM_MEDIANS_NOFEE)


# ---------------------------------------------------------------------------
# 3. Fee / carry drag (absolute multiples; single entry and exit cash flow)
# ---------------------------------------------------------------------------
def carry_with_catchup(proceeds: np.ndarray, T: float, rate: float, hurdle: float = 0.08):
    """Deal-level carry with an 8% compounded hurdle and full GP catch-up."""
    profit = proceeds - 1.0
    hurdle_profit = (1 + hurdle) ** T - 1.0
    excess = np.maximum(profit - hurdle_profit, 0.0)
    return np.minimum(excess, rate * np.maximum(profit, 0.0))


def section3(theta, L: float):
    rng = np.random.default_rng(SEED + 3)
    res = {}
    for T in (5.0, 7.0):
        mkt = 1.07 ** T  # PME -> absolute multiple conversion at 7%/yr market return [I]
        m_abs = simulate_deals(1, 400_000, theta, L, 0.0, rng).ravel() * mkt
        gross_profit = np.maximum(m_abs - 1.0, 0.0).mean()
        scen = {}
        # co-investment terms, deal by deal
        for name, fee, crate in (("0/0", 0.0, 0.0), ("1/10", 0.01, 0.10), ("0/20", 0.0, 0.20)):
            proceeds = m_abs - fee * T              # fee on invested capital, paid from proceeds
            carry = carry_with_catchup(proceeds, T, crate) if crate > 0 else 0.0
            net = proceeds - carry
            scen[name] = dict(E_net=float(np.mean(net)), median_net=float(np.median(net)),
                              E_carry=float(np.mean(carry)),
                              carry_share_of_gross_profit=float(np.mean(carry) / gross_profit),
                              irr_of_mean=float(np.mean(net) ** (1 / T) - 1))
        # fund style, pooled over 20 deals: 2% on commitments for 5y then 1.5% on invested
        n_f = 20
        m_pool = m_abs[: (len(m_abs) // n_f) * n_f].reshape(-1, n_f).mean(axis=1)
        fee_f = 0.02 * 5 + 0.015 * max(T - 5, 0)
        proceeds_f = m_pool - fee_f
        carry_f = carry_with_catchup(proceeds_f, T, 0.20)
        net_f = proceeds_f - carry_f
        scen["fund_2/20_pooled20"] = dict(E_net=float(net_f.mean()), median_net=float(np.median(net_f)),
                                          E_carry=float(carry_f.mean()),
                                          irr_of_mean=float(net_f.mean() ** (1 / T) - 1))
        # carry netting value: same 0/20 terms charged pooled instead of deal by deal
        proceeds_p = m_pool
        carry_p = carry_with_catchup(proceeds_p, T, 0.20)
        scen["0/20_pooled20_counterfactual"] = dict(E_net=float((proceeds_p - carry_p).mean()),
                                                    E_carry=float(carry_p.mean()))
        res[f"T={T:.0f}"] = dict(E_gross=float(m_abs.mean()), median_gross=float(np.median(m_abs)),
                                 E_gross_profit_pos=float(gross_profit), scenarios=scen)
    # program cost per FIL (2015) as used by BJS (2020): 0.91% (co-invest) vs 0.11% (funds)
    res["program_cost_pp_of_capital_5y"] = dict(coinvest=0.91 * 5, fund=0.11 * 5)
    return res


# ---------------------------------------------------------------------------
# 4. Exit hazard: Weibull fit to Kaplan & Stromberg cumulative exits
# ---------------------------------------------------------------------------
def section4():
    ts = np.array(sorted(KS_EXIT))
    fs = np.array([KS_EXIT[t] for t in ts])

    def loss(x):
        k, eta = x
        f = 1 - np.exp(-(ts / eta) ** k)
        return float(np.sum((f - fs) ** 2))

    r = optimize.minimize(loss, x0=[1.4, 7.7], method="Nelder-Mead")
    k, eta = r.x
    fit = {float(t): float(1 - math.exp(-(t / eta) ** k)) for t in ts}
    H = lambda t: (t / eta) ** k  # cumulative hazard
    mult = {"open (B)": 1.3, "normal (N)": 1.0, "drought (D)": 0.5, "crisis (C)": 0.3}
    cond = {}
    for name, m in mult.items():
        cond[name] = {a: float(1 - math.exp(-m * (H(a + 1) - H(a)))) for a in (2, 3, 4, 5, 6, 7, 8)}
    # book-level annual exit fraction for a uniform age mix over 0..9 years
    ages = np.arange(0, 10)
    book = {name: float(np.mean([1 - math.exp(-m * (H(a + 1) - H(a))) for a in ages]))
            for name, m in mult.items()}
    median_hold = float(eta * math.log(2) ** (1 / k))
    return dict(k=float(k), eta=float(eta), median_years=median_hold, fit=fit,
                conditional_1y_exit_prob=cond, book_annual_exit_fraction_uniform_age=book,
                regime_multipliers=mult)


# ---------------------------------------------------------------------------
# 5. Concentration analytics: illustrative $18bn book
# ---------------------------------------------------------------------------
def section5():
    rng = np.random.default_rng(SEED + 5)
    out = {}
    for n_pos, size_sigma in ((60, 0.8), (90, 0.8), (90, 1.1), (150, 0.8)):
        w = np.exp(size_sigma * rng.standard_normal(n_pos))
        w = np.sort(w / w.sum())[::-1]
        n_eff = 1.0 / np.sum(w ** 2)
        sig_id, beta_e, sig_m = 0.40, 1.4, 0.16   # [I] annual idiosyncratic vol, equity beta, market vol
        idio = sig_id * math.sqrt(float(np.sum(w ** 2)))
        syst = beta_e * sig_m
        out[f"N={n_pos},size_sigma={size_sigma}"] = dict(
            n_eff=float(n_eff), top1_share=float(w[0]), top10_share=float(w[:10].sum()),
            largest_position_usd_bn=float(18 * w[0]),
            book_idio_vol=float(idio), book_syst_vol=float(syst),
            book_total_vol=float(math.sqrt(idio ** 2 + syst ** 2)),
            idio_1sigma_usd_bn=float(18 * idio),
        )
    return out


# ---------------------------------------------------------------------------
# 6. Decision economics on one illustrative position (all inputs [I])
# ---------------------------------------------------------------------------
def section6():
    rng = np.random.default_rng(SEED + 6)
    nav = 400.0          # $m, GP mark (lagged one quarter)
    nowcast = 0.97 * nav # [I] nowcast after a weak quarter for comparables
    L_now = 6.0 / 14.0   # net debt 6.0x EBITDA, EV 14x EBITDA
    ev0 = nowcast / (1 - L_now)
    debt = ev0 * L_now
    sofr = 0.0389        # FRED, 2026-10-15 (via sibling dossier 01)
    h = 0.09             # [I] ADIC opportunity-cost hurdle for this risk
    scenarios = {}
    for regime, (tau, mu_a, s_a) in {
        "normal": (2.5, 0.06, 0.28),     # remaining hold, EV drift, EV vol (annual)
        "drought": (3.5, 0.04, 0.30),
    }.items():
        n = 400_000
        g = np.exp((mu_a - 0.5 * s_a ** 2) * tau + s_a * math.sqrt(tau) * rng.standard_normal(n))
        equity = np.maximum(ev0 * g - debt, 0.0)
        pv_hold = float(np.mean(equity) / (1 + h) ** tau)
        e_eq = float(np.mean(equity))
        res = dict(tau=tau, E_exit_equity=e_eq, p_loss_vs_nav=float((equity < nav).mean()),
                   p_wipeout=float((equity <= 1e-9).mean()), PV_hold_at_h=pv_hold)
        # SELL: strip sale of 100% at price_pct of the (lagged) NAV
        for price_pct in (0.80, 0.88, 0.95, 1.00):
            p = price_pct * nav
            res[f"sell_{int(price_pct*100)}"] = dict(
                price=p,
                buyer_expected_irr_under_our_beliefs=float((e_eq / p) ** (1 / tau) - 1),
                breakeven_liquidity_premium_total=float(pv_hold / p - 1),
            )
        # REFINANCE: concentrated co-invest pool facility, 15% LTV, SOFR+650, 1.5% OID, bullet
        ltv, spread, oid = 0.15, 0.065, 0.015
        loan = ltv * nav
        rate = sofr + spread
        cost_annual = rate + oid / tau
        res["refi"] = dict(loan=loan, all_in_rate=float(cost_annual),
                           spread_over_rf=float(cost_annual - sofr))
        # covenant: LTV doubles (1.5x trigger at 22.5%, 2x default at 30%) when NAV falls
        # 33% (trigger) / 50% (default). Probability that the exit equity value is below these.
        res["refi"]["p_nav_down_33pct_at_exit"] = float((equity < nav * (1 - 1 / 3)).mean())
        res["refi"]["p_nav_down_50pct_at_exit"] = float((equity < nav * 0.5).mean())
        # LEVER: holdco PIK at 12% on 25% LTV; equity-on-equity leverage
        pik_rate, pik_ltv = 0.12, 0.25
        pik = pik_ltv * nav
        pik_due = pik * (1 + pik_rate) ** tau
        resid = np.maximum(equity - pik_due, 0.0)
        res["lever_pik"] = dict(
            pik_principal=pik, pik_due_at_exit=float(pik_due),
            E_residual=float(resid.mean()),
            p_residual_zero=float((resid <= 1e-9).mean()),
            levered_equity_expected_irr=float((resid.mean() / (nav - pik)) ** (1 / tau) - 1),
            unlevered_expected_irr_on_nav=float((e_eq / nav) ** (1 / tau) - 1),
        )
        scenarios[regime] = res
    return dict(inputs=dict(nav=nav, nowcast=nowcast, L_now=L_now, sofr=sofr, hurdle=h),
                scenarios=scenarios)


# ---------------------------------------------------------------------------
# 7. Dynamic deal-level book simulation (SYNTHETIC $18bn co-investment book)
#    Quarterly; regime-switching market; EV jump-diffusion; debt with amortization
#    and recaps; default barrier; Weibull exit hazard x regime x performance tilt;
#    exit uplift over fair value; smoothed, lagged GP marks; follow-ons; pacing.
# ---------------------------------------------------------------------------
REG = ("B_open", "N_normal", "D_drought", "C_crisis")
P_REG = np.array([[0.85, 0.12, 0.02, 0.01],    # quarterly transition matrix (dossier 04 default)
                  [0.04, 0.88, 0.06, 0.02],
                  [0.03, 0.06, 0.88, 0.03],
                  [0.02, 0.08, 0.15, 0.75]])
BOOK = dict(
    mu_m=np.array([0.10, 0.07, 0.04, -0.20]),     # listed-equity drift by regime [I]
    sig_m=np.array([0.14, 0.16, 0.18, 0.30]),     # listed-equity vol by regime [I]
    exit_mult=np.array([1.3, 1.0, 0.5, 0.3]),     # exit-hazard multipliers [I], cf. dossier 04 m^D
    recap_p=np.array([0.15, 0.10, 0.05, 0.0]),    # annual recap probability if eligible [I]
    deploy_q=np.array([0.75, 0.75, 0.50, 0.25]),  # $bn deployed per quarter by regime [I]
    beta_A=0.9, alpha_A=0.01, sig_id=0.25,        # EV beta, EV alpha, idiosyncratic EV vol [I]
    lam_J=0.15, p_up=0.4, eta_up=0.20, eta_dn=0.30,  # Kou jumps (annual intensity) [I]
    L_entry=0.45, amort=0.01,                     # entry debt/EV (today), amortization [I]
    k=1.447, eta=7.70, gamma=0.50,                # Weibull (fit to KS) and performance tilt [I]
    uplift_mu=0.15, uplift_sd=0.10,               # exit price over fair value [I]; tuned so that
                                                  # ~75% of exits beat the next-to-last mark (Bain/MSCI)
    default_kappa=0.75,                           # write-off when EV < kappa * debt (cov-lite) [I]
    lam_mark=0.5,                                 # quarterly smoothing, 1q lag (dossier 04)
    fo_p=0.05, fo_size=0.10,                      # follow-on probability / size [I]
    recap_debt_up=0.25, recap_elig_L=0.50,        # recap: +25% debt (~+1 turn), if D/EV < 50%
    ticket=0.20, n_init=90, slots=320,            # $bn ticket, initial positions
)


def section7(start_regime: int = 2, n_paths: int = 2000, quarters: int = 12, seed_off: int = 7):
    b = BOOK
    rng = np.random.default_rng(SEED + seed_off)
    dt = 0.25
    S = b["slots"]
    act = np.zeros((n_paths, S), bool)
    ev = np.zeros((n_paths, S)); debt = np.zeros((n_paths, S)); cost = np.zeros((n_paths, S))
    age = np.zeros((n_paths, S)); mark = np.zeros((n_paths, S)); mark_prev = np.zeros((n_paths, S))
    eq_lag = np.zeros((n_paths, S))
    # initial book: 90 positions, ages U(0,7), equity drawn around cost with drift
    n0 = b["n_init"]
    act[:, :n0] = True
    age[:, :n0] = rng.uniform(0, 7, (n_paths, n0))
    cost[:, :n0] = b["ticket"]
    growth = np.exp(rng.normal(0.05 * age[:, :n0], 0.25 * np.sqrt(np.maximum(age[:, :n0], 0.25))))
    eq0 = cost[:, :n0] * growth
    eq0 *= 18.0 / eq0.sum(axis=1, keepdims=True)          # normalise NAV to $18bn
    debt[:, :n0] = cost[:, :n0] * b["L_entry"] / (1 - b["L_entry"]) * (1 - b["amort"] * age[:, :n0])
    ev[:, :n0] = eq0 + debt[:, :n0]
    mark[:, :n0] = eq0; mark_prev[:, :n0] = eq0; eq_lag[:, :n0] = eq0
    reg = np.full(n_paths, start_regime)
    H = lambda t: (np.maximum(t, 0) / b["eta"]) ** b["k"]
    cum = dict(dist_exit=np.zeros(n_paths), dist_recap=np.zeros(n_paths), calls_new=np.zeros(n_paths),
               calls_fo=np.zeros(n_paths), writeoff_cost=np.zeros(n_paths), n_exit=np.zeros(n_paths),
               n_wo=np.zeros(n_paths))
    nav0 = (np.maximum(ev - debt, 0) * act).sum(axis=1)
    exit_above_prev = []; yearly_dist = np.zeros((n_paths, quarters // 4))
    regime_path = np.zeros((n_paths, quarters), int)
    for q in range(quarters):
        # 1. regime transition
        u = rng.random(n_paths)
        cp = np.cumsum(P_REG[reg], axis=1)
        reg = (u[:, None] > cp).sum(axis=1)
        regime_path[:, q] = reg
        mu_m, sg_m = b["mu_m"][reg], b["sig_m"][reg]
        r_m = (mu_m - 0.5 * sg_m ** 2) * dt + sg_m * math.sqrt(dt) * rng.standard_normal(n_paths)
        # 2. EV evolution with jumps
        nj = rng.poisson(b["lam_J"] * dt, (n_paths, S))
        up = rng.random((n_paths, S)) < b["p_up"]
        jsize = np.where(up, rng.exponential(b["eta_up"], (n_paths, S)),
                         -rng.exponential(b["eta_dn"], (n_paths, S))) * (nj > 0)
        r_ev = (b["alpha_A"] - 0.5 * b["sig_id"] ** 2) * dt + b["beta_A"] * r_m[:, None] \
            + b["sig_id"] * math.sqrt(dt) * rng.standard_normal((n_paths, S)) + jsize
        ev = np.where(act, ev * np.exp(r_ev), ev)
        debt = np.where(act, debt * (1 - b["amort"] * dt), debt)
        eq = np.maximum(ev - debt, 0.0)
        # 3. default / write-off (barrier below face value: cov-lite survival)
        active_count_q = act.sum(axis=1)
        cum.setdefault("pos_q", np.zeros(n_paths))
        cum["pos_q"] += active_count_q
        wo = act & (ev <= b["default_kappa"] * debt)
        cum["writeoff_cost"] += (cost * wo).sum(axis=1); cum["n_wo"] += wo.sum(axis=1)
        act &= ~wo
        # 4. recaps (interim distributions)
        elig = act & (age >= 2.0) & (debt / np.maximum(ev, 1e-12) < b["recap_elig_L"])
        rc = elig & (rng.random((n_paths, S)) < b["recap_p"][reg][:, None] * dt)
        d_up = b["recap_debt_up"] * debt * rc
        debt = debt + d_up
        dist_rc = (0.98 * d_up).sum(axis=1)
        cum["dist_recap"] += dist_rc
        eq = np.maximum(ev - debt, 0.0)
        # 5. follow-ons
        fo = act & (rng.random((n_paths, S)) < b["fo_p"] * dt)
        call_fo = b["fo_size"] * eq * fo
        ev = ev + call_fo; cost = cost + call_fo
        cum["calls_fo"] += call_fo.sum(axis=1)
        eq = np.maximum(ev - debt, 0.0)
        # 6. exits
        perf = np.log(np.maximum(eq, 1e-9) / np.maximum(cost, 1e-9))
        haz = b["exit_mult"][reg][:, None] * (H(age + dt) - H(age)) * np.exp(b["gamma"] * np.clip(perf, -3, 3))
        ex = act & (rng.random((n_paths, S)) < 1 - np.exp(-haz))
        upl = np.maximum(rng.normal(b["uplift_mu"], b["uplift_sd"], (n_paths, S)), -0.5)
        proceeds = eq * (1 + upl) * ex
        if ex.any():
            live = ex & (proceeds > 0) & (mark_prev > 0)   # realised exits, excluding zero-value exits
            exit_above_prev.append(((proceeds > mark_prev) & live).sum() / max(live.sum(), 1))
            cum.setdefault("zero_exits", np.zeros(n_paths))
            cum["zero_exits"] += (ex & (proceeds <= 0)).sum(axis=1)
        cum["dist_exit"] += proceeds.sum(axis=1); cum["n_exit"] += ex.sum(axis=1)
        yearly_dist[:, q // 4] += proceeds.sum(axis=1) + dist_rc
        act &= ~ex
        # 7. marks: smoothed, one-quarter lag
        mark_prev = np.where(act, mark, 0.0)
        mark = np.where(act, b["lam_mark"] * mark + (1 - b["lam_mark"]) * eq_lag, 0.0)
        eq_lag = np.where(act, eq, 0.0)
        # 8. new deployment into free slots
        n_new = np.floor(b["deploy_q"][reg] / b["ticket"]).astype(int)
        free = ~act
        rank = np.cumsum(free, axis=1)
        newm = free & (rank <= n_new[:, None])
        tk = b["ticket"]
        ev = np.where(newm, tk / (1 - b["L_entry"]), ev)
        debt = np.where(newm, tk / (1 - b["L_entry"]) * b["L_entry"], debt)
        cost = np.where(newm, tk, np.where(act, cost, 0.0))
        age = np.where(newm, 0.0, age)
        mark = np.where(newm, tk, mark); mark_prev = np.where(newm, tk, mark_prev)
        eq_lag = np.where(newm, tk, eq_lag)
        cum["calls_new"] += (newm * tk).sum(axis=1)
        act |= newm
        age = np.where(act, age + dt, age)
    eq_end = (np.maximum(ev - debt, 0) * act).sum(axis=1)
    mark_end = (mark * act).sum(axis=1)
    dist = cum["dist_exit"] + cum["dist_recap"]
    calls = cum["calls_new"] + cum["calls_fo"]
    net = dist - calls

    def pct(x):
        return dict(mean=float(np.mean(x)), p10=float(np.quantile(x, 0.10)),
                    p50=float(np.median(x)), p90=float(np.quantile(x, 0.90)))

    stayed_d = (regime_path == 2).all(axis=1)
    return dict(
        start_regime=REG[start_regime], quarters=quarters, n_paths=n_paths,
        nav0=pct(nav0), dist_3y=pct(dist), recap_share_of_dist=float(cum["dist_recap"].sum() / dist.sum()),
        calls_3y=pct(calls), net_cf_3y=pct(net), nav_end_economic=pct(eq_end), nav_end_reported=pct(mark_end),
        annual_dist_yield_on_nav0={f"Y{y+1}": pct(yearly_dist[:, y] / nav0) for y in range(quarters // 4)},
        exits_3y=pct(cum["n_exit"]), writeoffs_3y=pct(cum["n_wo"]),
        writeoff_cost_share=float(cum["writeoff_cost"].sum() / max((cum["calls_new"] + 18.0).sum(), 1e-9)),
        annual_writeoff_rate_per_position=float(cum["n_wo"].sum() / (cum["pos_q"].sum() * dt)),
        share_of_exits_at_zero=float(cum.get("zero_exits", np.zeros(1)).sum() / max(cum["n_exit"].sum(), 1)),
        annual_exit_rate_per_position=float(cum["n_exit"].sum() / (cum["pos_q"].sum() * dt)),
        recap_dist_over_exit_proceeds=float(cum["dist_recap"].sum() / max(cum["dist_exit"].sum(), 1e-9)),
        p_exit_above_next_to_last_mark=float(np.mean(exit_above_prev)) if exit_above_prev else None,
        net_cf_3y_if_drought_throughout=pct(net[stayed_d]) if stayed_d.any() else None,
        share_paths_drought_throughout=float(stayed_d.mean()),
        reported_vs_economic_nav_gap=pct(mark_end / np.maximum(eq_end, 1e-9) - 1),
    )


def main():
    s1 = section1()
    s1b = section1b()
    # house calibration: extended model at L = 0.60 (historical debt/total capital ~60-70%:
    # GKM 2016 survey target 60%; AJSW 2013 median 70%, as cited by GKM)
    house = next(f for f in s1b["fits"] if abs(f["L"] - 0.60) < 1e-9)
    theta = (house["mu"], house["sigma"], house["p_jump"], house["mean_jump"], house["R_max"])
    L = house["L"]
    results = dict(
        note="SYNTHETIC/ILLUSTRATIVE outputs; targets from BJS (2020), LPG (2015), Kaplan & Stromberg (2008).",
        targets=dict(BJS_buyout_coinvest=BJS, BJS_buyout_other=BJS_OTHER, KS_exit=KS_EXIT),
        section1_fit_lognormal=s1,
        section1b_fit_extended=s1b,
        house_params=dict(mu=theta[0], sigma=theta[1], p_jump=theta[2], mean_jump=theta[3],
                          R_max=theta[4], L=L),
        section1c_leverage_translation=section1c(theta, L),
        section1d_abs_moic=dict(
            note="PME -> absolute MOIC at 1.36x (BJSt realised medians MOIC 1.9 / PME 1.4) [I]",
            p_moic_lt1_hist_L060=float((ext_draw(theta, L) * 1.36 < 1.0).mean()),
            median_moic_hist_L060=float(np.median(ext_draw(theta, L) * 1.36)),
            p_moic_lt1_today_L040=float((ext_draw(theta, 0.40) * 1.36 < 1.0).mean()),
            median_moic_today_L040=float(np.median(ext_draw(theta, 0.40) * 1.36)),
        ),
        section2_diversification=section2(theta, L),
        section3_fees=section3(theta, L),
        section4_exit_hazard=section4(),
        section5_concentration=section5(),
        section6_decision=section6(),
        section7_book_sim_start_drought=section7(start_regime=2),
        section7_book_sim_start_normal=section7(start_regime=1, seed_off=8),
        book_params={k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in BOOK.items()},
    )
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("lognormal best L:", s1["best_L"], "| extended best L:", s1b["best_L"])
    print("house:", {k: round(v, 4) for k, v in results["house_params"].items()})
    print("wrote", OUT)


if __name__ == "__main__":
    main()
