"""G5 Public Markets dossier: reproducible worked examples (SYNTHETIC / ILLUSTRATIVE inputs).
All inputs are labelled assumptions unless stated as sourced in the dossier. Run: python -I g5_examples.py
"""
import json
import math

import numpy as np

out = {}

# ---------------------------------------------------------------------------
# 1. Square-root market impact for USD 1-5bn baskets (Toth et al. 2011: Delta = Y*sigma*sqrt(Q/V))
# ---------------------------------------------------------------------------
markets = {
    # name: (daily dollar volume V in USD bn [assumption], daily vol sigma [assumption],
    #        half-spread + commission bps [assumption], taxes/levies on SELL bps [assumption])
    "US large cap (S&P 500 basket)": (400.0, 0.010, 1.5, 0.0),
    "Developed ex-US large cap": (150.0, 0.010, 3.0, 2.0),
    "EM equity (MSCI EM basket)": (150.0, 0.012, 6.0, 12.0),
    "US small cap (Russell 2000 basket)": (40.0, 0.016, 8.0, 0.0),
}
impact = {}
for name, (V, sig, spread_bps, tax_bps) in markets.items():
    row = {}
    for Q in (1.0, 2.0, 5.0):
        part = Q / V
        for Y in (0.5, 0.7, 1.0):
            imp_bps = Y * sig * math.sqrt(part) * 1e4
            row[f"Q={Q:.0f}bn,Y={Y}"] = {
                "participation_pct_of_ADV": round(100 * part, 2),
                "impact_bps": round(imp_bps, 1),
                "all_in_sell_bps": round(imp_bps + spread_bps + tax_bps, 1),
            }
    impact[name] = row
out["sqrt_impact"] = impact

# ---------------------------------------------------------------------------
# 2. GLM smoothing: reported vol, beta and Sharpe distortion
# ---------------------------------------------------------------------------
glm = {}
for label, theta in {
    "liquid (macro/CTA)": (1.0, 0.0, 0.0),
    "equity L/S": (0.85, 0.15, 0.0),
    "event/credit": (0.70, 0.20, 0.10),
    "illiquid credit/RV": (0.55, 0.30, 0.15),
}.items():
    th = np.array(theta)
    vol_ratio = float(np.sqrt((th ** 2).sum()))
    # lag-1 autocorrelation of reported returns under MA(2) smoothing of iid true returns
    rho1 = float((th[0] * th[1] + th[1] * th[2]) / (th ** 2).sum())
    glm[label] = {
        "theta": theta,
        "reported_vol_over_true": round(vol_ratio, 3),
        "sharpe_inflation_x": round(1 / vol_ratio, 3),
        "contemporaneous_beta_over_true": theta[0],
        "lag1_autocorr_reported": round(rho1, 3),
    }
out["glm_smoothing"] = glm

# ---------------------------------------------------------------------------
# 3. Redemption queue under a fund-level gate vs investor-level gate
# ---------------------------------------------------------------------------
def fund_gate_queue(adic_share, other_requests, gate, quarters=12):
    """Pro-rata fund-level gate. ADIC redeems its whole stake at q0.
    other_requests: list of new requests by others each quarter as fraction of current NAV.
    NAV units: fund NAV normalised to 1 at q0 (no returns, for clarity)."""
    nav = 1.0
    adic_rem = adic_share
    others_queue = 0.0
    paid_adic = []
    for q in range(quarters):
        new_other = other_requests[q] * (nav - adic_rem - others_queue) if q < len(other_requests) else 0.0
        others_queue += max(new_other, 0.0)
        total_req = adic_rem + others_queue
        capacity = gate * nav
        ratio = 1.0 if total_req <= capacity else capacity / total_req
        pay_adic = adic_rem * ratio
        pay_oth = others_queue * ratio
        adic_rem -= pay_adic
        others_queue -= pay_oth
        nav -= pay_adic + pay_oth
        paid_adic.append(round(pay_adic / adic_share, 4))
        if adic_rem < 1e-9:
            break
    return paid_adic

queue = {
    "calm: others request 5%/q, gate 25%": fund_gate_queue(0.05, [0.05] * 12, 0.25),
    "crisis: others request 40% then 20%,10%, gate 25%": fund_gate_queue(0.05, [0.40, 0.20, 0.10, 0.05], 0.25),
    "crisis: others request 40% then 20%,10%, gate 10%": fund_gate_queue(0.05, [0.40, 0.20, 0.10, 0.05], 0.10),
}
cum = {k: [round(float(x), 3) for x in np.cumsum(v)] for k, v in queue.items()}
out["fund_gate_queue_cumulative_fraction_paid_to_ADIC_by_quarter"] = cum
# investor-level gates: fraction of stake receivable per quarter
out["investor_level_gate_quarters_to_full_exit"] = {
    "1/4 per quarter (e.g. 25%)": 4,
    "1/8 per quarter": 8,
    "1/16 per quarter (6.25%)": 16,
    "1/20 per quarter (5%)": 20,
}

# ---------------------------------------------------------------------------
# 4. Physical-to-synthetic (REFINANCE) economics for a USD 5bn long-only US large-cap mandate
# ---------------------------------------------------------------------------
N = 5000.0  # USD m notional
cases = {
    "normal": {"fin_spread": 0.0050, "im": 0.06, "vm_buffer": 0.117},   # 21d p1 SPX move -11.7% (Stream 09, Cboe)
    "tight (Jun-2026-like)": {"fin_spread": 0.0081, "im": 0.08, "vm_buffer": 0.117},
    "stress": {"fin_spread": 0.0175, "im": 0.12, "vm_buffer": 0.33},     # worst 21d SPX -33% (Stream 09, Cboe)
}
mgr_fee = 0.0025  # assumption: institutional SMA fee 25 bp
# Relative carry of synthetic vs physical-with-manager = -(f + alpha_net), alpha_net = alpha_gross - fee.
# Bounds: alpha_net = -fee (gross alpha zero, Fama-French reading) .. alpha_net = 0 (Barras et al. reading).
tc_oneway_bps = 8.0  # from sqrt-impact table, US large cap Q=5bn, Y~0.7 incl. spread (rounded)
p2s = {}
for k, c in cases.items():
    freed = N * (1 - c["im"] - c["vm_buffer"])
    tc_amort = N * 2 * tc_oneway_bps / 1e4 / 2.0  # round trip amortised over 2 years
    res = {
        "cash_freed_usd_m": round(freed, 0),
        "freed_pct_notional": round(100 * freed / N, 1),
        "tc_amortised_usd_m_per_yr": round(tc_amort, 1),
    }
    for lab, a_net in (("alpha_net=-fee", -mgr_fee), ("alpha_net=0", 0.0)):
        annual_cost = N * (c["fin_spread"] + a_net)
        total = annual_cost + tc_amort
        res[f"annual_carry_cost_usd_m[{lab}]"] = round(annual_cost, 1)
        res[f"cost_pct_per_yr_of_cash_freed[{lab}]"] = round(100 * total / freed, 2)
    p2s[k] = res
out["physical_to_synthetic"] = p2s

# Credibility (Buhlmann) of a manager's realised alpha: Z = n/(n+k), k = (sigma_eps/tau)^2
cred = {}
for lab, s_eps, tau in (("LO: TE 3%, tau 1%", 0.03, 0.01), ("HF: idio 6%, tau 2.5%", 0.06, 0.025)):
    k_years = (s_eps / tau) ** 2
    cred[lab] = {"k_years": round(k_years, 2), **{f"Z({n}y)": round(n / (n + k_years), 3) for n in (3, 5, 10)}}
out["credibility"] = cred

# Barclay CTA Index arithmetic mean 2009-2025 (annual returns as published by BarclayHedge, fetched 2026-10-18)
cta = [-0.10, 7.05, -3.09, -1.70, -1.42, 7.61, -1.50, -1.23, 0.70, -3.17, 5.17, 5.43, 5.03, 7.13, -0.39, 3.45, 3.10]
out["barclay_cta_2009_2025"] = {"mean_pct": round(float(np.mean(cta)), 2), "stdev_pct": round(float(np.std(cta, ddof=1)), 2)}
# Comparators (annualised cost of liquidity, % of cash raised), simple:
# NAV loan spread (Stream 06/08: SOFR+480-610bp + 1-1.5% fee over 4y) -> ~5.5% + 0.3% = ~5.8%/yr
# Secondary sale at 12% discount, forgone excess return ~ d/(1-d) one-off; amortised over 3y ~ 4.5%/yr
out["comparators_pct_per_yr"] = {
    "NAV loan (SOFR+5.45% mid + 1.25% fee/4y)": round(5.45 + 1.25 / 4, 2),
    "LP secondary at 12% discount amortised 3y": round(100 * (0.12 / 0.88) / 3, 2),
}

# ---------------------------------------------------------------------------
# 5. Portable alpha stress: USD 2bn HF + USD 2bn futures beta
# ---------------------------------------------------------------------------
hf = 2000.0
beta_notional = 2000.0
eq_crash_21d = -0.33  # worst 21d SPX (Stream 09)
hf_crisis_beta = 0.30
hf_loss = hf * hf_crisis_beta * eq_crash_21d
vm_call = beta_notional * eq_crash_21d  # negative = cash out
im_increase = beta_notional * (0.12 - 0.06)
for_gate_p = [0.0, 0.2, 0.5]
pa = {
    "hf_mark_change_usd_m": round(hf_loss, 0),
    "vm_outflow_usd_m": round(vm_call, 0),
    "im_increase_usd_m": round(im_increase, 0),
    "cash_needed_within_days_usd_m": round(-vm_call + im_increase, 0),
    "expected_hf_cash_available_within_90d_if_gated_with_p": {
        str(p): round(hf * (1 + hf_crisis_beta * eq_crash_21d) * 0.36 * (1 - p), 0) for p in for_gate_p
    },
}
out["portable_alpha_stress"] = pa

# ---------------------------------------------------------------------------
# 6. Industry investor-liquidity profile applied to a USD 20bn HF book (OFR Form PF, 2026-06-30)
# ---------------------------------------------------------------------------
book = 20.0
prof = {"<=7d": 0.084, "8-90d": 0.273, ">90d": 0.644}
out["hf_book_contractual_liquidity_usd_bn"] = {k: round(book * v, 2) for k, v in prof.items()}
# crisis overlay: 25% of the 8-90d bucket gated/deferred one quarter, 5% of book side-pocketed
crisis_90d = book * (prof["<=7d"] + prof["8-90d"] * 0.75)
out["hf_book_crisis_within_90d_usd_bn"] = round(crisis_90d, 2)

# ---------------------------------------------------------------------------
# 7. Crisis-beta ratios (HF composite loss / equity loss)
# ---------------------------------------------------------------------------
ratios = {
    "2008 HFRI FWC -19.03% vs S&P 500 TR -37.0% [nrv]": round(-19.03 / -37.0, 2),
    "Q1-2020 HFRI FWC -9.4% vs S&P 500 -19.6%": round(-9.4 / -19.6, 2),
    "Q1-2020 HFRI EH -12.9% vs S&P 500 -19.6%": round(-12.9 / -19.6, 2),
    "Q1-2020 HFRI ED -15.3% vs S&P 500 -19.6%": round(-15.3 / -19.6, 2),
    "2022 HFRI FWC -4.2% vs S&P 500 TR -18.1% [nrv]": round(-4.2 / -18.1, 2),
    "2022 HFRI EH -10.2% vs S&P 500 TR -18.1% [nrv]": round(-10.2 / -18.1, 2),
}
out["crisis_beta_ratios"] = ratios

# ---------------------------------------------------------------------------
# 8. Monte Carlo of a synthetic HF manager: factor + alpha + skew-t + smoothing, regime crisis jumps
# ---------------------------------------------------------------------------
rng = np.random.default_rng(20261018)
T = 12 * 30
n_paths = 2000
p_crisis = 0.06  # monthly prob of entering crisis month (assumption)
mkt_mu, mkt_sig = 0.006, 0.045
beta_n, beta_c = 0.40, 0.65
alpha_m = 0.02 / 12
idio = 0.025
nu = 5.0
theta = np.array([0.85, 0.15])
ann_true, ann_rep, ac1 = [], [], []
for _ in range(n_paths):
    crisis = rng.random(T) < p_crisis
    m = rng.normal(mkt_mu, mkt_sig, T)
    m[crisis] += rng.normal(-0.08, 0.04, crisis.sum())
    b = np.where(crisis, beta_c, beta_n)
    t_draw = rng.standard_t(nu, T) * math.sqrt((nu - 2) / nu)
    r = alpha_m + b * m + idio * t_draw
    rep = theta[0] * r + theta[1] * np.concatenate([[r[0]], r[:-1]])
    ann_true.append(r.std() * math.sqrt(12))
    ann_rep.append(rep.std() * math.sqrt(12))
    ac1.append(np.corrcoef(rep[1:], rep[:-1])[0, 1])
out["synthetic_manager_mc"] = {
    "true_ann_vol_mean": round(float(np.mean(ann_true)), 4),
    "reported_ann_vol_mean": round(float(np.mean(ann_rep)), 4),
    "reported_lag1_ac_mean": round(float(np.mean(ac1)), 3),
}

print(json.dumps(out, indent=1))
