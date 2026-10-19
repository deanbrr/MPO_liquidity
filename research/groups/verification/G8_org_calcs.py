"""
G8 organizational-economics worked examples (ALL NUMBERS SYNTHETIC / ILLUSTRATIVE, NOT ADIC DATA).

Reproduces every [I-calc] number in research/groups/dossiers/G8_org_tpa_economics.md:
  E1  Group budgets as optimizer outputs and dual-based transfer prices (concave QP, cvxpy/Clarabel)
  E2  Decentralization check: groups facing the dual prices choose the central optimum
  E3  Baumol-Fabian non-uniqueness when the problem is linear (LP, HiGHS)
  E4  Forecast inflation by one group: own-budget gain and crowding-out of other groups,
      with and without credibility weighting Z
  E5  Misreport incentive when budget depends on the forecast (quadratic score), delta* = b*Z*B'/(2s)
  E6  Weitzman/Gonik plan-bonus scheme elicits the (beta-alpha)/(gamma-alpha) quantile
  E7  Interval/WIS scoring of a P10/P50/P90 forecast; implied dispersion inflation from 36% coverage
  E8  Internal transfer neutrality (PE -> Secondaries fund-stake sale) and attribution adjustment
  E9  Tail-hedge break-even: liquidity-provider and risk-capital credits vs expected carry
  E10 No-regret budget bands: effective curvature of the total-portfolio objective per group (re-solves)
Run:  python -I G8_org_calcs.py   (writes G8_org_calcs_results.json next to this file)
"""
import json
import math
import os

import cvxpy as cp
import numpy as np
from scipy import integrate, optimize, stats

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "G8_org_calcs_results.json")
res = {"note": "SYNTHETIC/ILLUSTRATIVE. Units: $bn of incremental 12-month deployment; alpha in decimal p.a. "
               "vs risk-matched funding basket; liquidity rows = stressed liquidity consumption per $ deployed "
               "(net of the liquid funding basket); risk row = linearised Euler CVaR contribution per $."}

# ---------------------------------------------------------------- E1 data (synthetic)
groups = ["PE", "SEC", "COI", "CAP", "PCR", "HF", "OVL_OPP", "TAIL"]
# fused forward alpha* before transfer charges (decimal p.a.); TAIL = expected carry per $ of premium budget
alpha = np.array([0.015, 0.030, 0.025, 0.035, 0.010, 0.010, 0.010, -0.45])
# diminishing returns (decimal per $bn): alpha_marginal = alpha - q x
q = np.array([0.0025, 0.0060, 0.0040, 0.0100, 0.0030, 0.0030, 0.0050, 0.30])
lo = np.zeros(8)
hi = np.array([8.0, 5.0, 4.0, 3.0, 5.0, 4.0, 3.0, 0.6])
# coupling rows (per $ deployed): L12 drought, L12 crisis, L24 crisis, CVaR contribution
A = np.array([
    #  PE    SEC   COI   CAP   PCR   HF    OVL   TAIL
    [0.40, 0.70, 0.95, 0.80, 0.60, 0.30, 0.10, 1.00],   # L12_drought (premium paid, no payoff)
    [0.55, 0.85, 1.00, 0.85, 0.70, 0.50, 0.25, -4.00],  # L12_crisis (hedge pays ~5x premium)
    [0.75, 0.65, 0.95, 0.70, 0.50, 0.25, 0.20, -3.50],  # L24_crisis
    [0.30, 0.25, 0.35, 0.18, 0.15, 0.10, 0.15, -2.00],  # CVaR contribution
])
rows = ["L12_drought", "L12_crisis", "L24_crisis", "CVaR"]
cap = np.array([6.0, 5.0, 7.0, 1.6])  # incremental headroom ($bn) per row

x = cp.Variable(8)
obj = cp.Maximize(alpha @ x - 0.5 * cp.sum(cp.multiply(q, cp.square(x))))
cons = [A @ x <= cap, x >= lo, x <= hi]
prob = cp.Problem(obj, cons)
prob.solve(solver=cp.CLARABEL)
xs = np.array(x.value)
duals = np.array(cons[0].dual_value)
charge = A.T @ duals  # transfer charge per $ deployed (decimal p.a.)
net = alpha - charge
res["E1"] = {
    "status": prob.status,
    "objective_bn_per_yr": float(prob.value),
    "x_star_bn": dict(zip(groups, np.round(xs, 3).tolist())),
    "row_usage_bn": dict(zip(rows, np.round(A @ xs, 3).tolist())),
    "row_cap_bn": dict(zip(rows, cap.tolist())),
    "duals_decimal": dict(zip(rows, np.round(duals, 5).tolist())),
    "charge_bp": dict(zip(groups, np.round(charge * 1e4, 1).tolist())),
    "alpha_bp": dict(zip(groups, np.round(alpha * 1e4, 1).tolist())),
    "net_alpha_after_charges_bp": dict(zip(groups, np.round(net * 1e4, 1).tolist())),
    "group_liquidity_budget_L12_crisis_bn": dict(zip(groups, np.round(A[1] * xs, 3).tolist())),
    "group_risk_budget_CVaR_bn": dict(zip(groups, np.round(A[3] * xs, 3).tolist())),
}

# ---------------------------------------------------------------- E2 decentralization check
x_dec = np.clip(net / q, lo, hi)
res["E2"] = {
    "x_decentralized_bn": dict(zip(groups, np.round(x_dec, 3).tolist())),
    "max_abs_diff_vs_central_bn": float(np.max(np.abs(x_dec - xs))),
}

# ---------------------------------------------------------------- E3 LP non-uniqueness (Baumol-Fabian)
# Two groups with identical net economics in a linear problem: prices cannot pick the split.
c = np.array([0.03, 0.03])           # alpha per $ for SEC-like and CAP-like strategies
A_lp = np.array([[0.8, 0.8]])        # same liquidity use
b_lp = np.array([4.0])
lp = optimize.linprog(-c, A_ub=A_lp, b_ub=b_lp, bounds=[(0, 5), (0, 5)], method="highs")
mu_lp = -lp.ineqlin.marginals[0]
reduced = c - A_lp[0] * mu_lp
res["E3"] = {
    "lp_solution_bn": lp.x.round(3).tolist(),
    "dual_liquidity": round(float(mu_lp), 5),
    "reduced_costs_at_dual": reduced.round(8).tolist(),
    "comment": "Both reduced costs are zero at the dual price: every split summing to 5bn is optimal, "
               "so prices alone cannot decentralize; the centre must also issue quantity envelopes.",
}

# ---------------------------------------------------------------- E4 inflation and crowding-out
def solve_with(alpha_vec):
    xv = cp.Variable(8)
    pr = cp.Problem(cp.Maximize(alpha_vec @ xv - 0.5 * cp.sum(cp.multiply(q, cp.square(xv)))),
                    [A @ xv <= cap, xv >= lo, xv <= hi])
    pr.solve(solver=cp.CLARABEL)
    return np.array(xv.value), np.array(pr.constraints[0].dual_value)

delta = 0.02  # PE inflates its forecast alpha by 200bp
e4 = {}
for label, Z in [("raw_forecast_used_Z1", 1.0), ("credibility_Z0.4", 0.4), ("credibility_Z0.2", 0.2)]:
    a2 = alpha.copy()
    a2[0] += Z * delta
    x2, d2 = solve_with(a2)
    true_val = float(alpha @ x2 - 0.5 * np.sum(q * x2 ** 2))  # value under TRUE alpha
    e4[label] = {
        "x_bn": dict(zip(groups, np.round(x2, 3).tolist())),
        "dPE_bn": round(float(x2[0] - xs[0]), 3),
        "d_others_bn": round(float(np.sum(x2[1:7] - xs[1:7])), 3),
        "duals": dict(zip(rows, np.round(d2, 5).tolist())),
        "true_value_loss_mn_per_yr": round(1000 * (float(prob.value) - true_val), 2),
    }
res["E4"] = e4

# ---------------------------------------------------------------- E5 misreport incentive (analytic + check)
# Group utility U(f) = b*Budget(mu_post(f)) - s*E[(f-y)^2],  mu_post = Z f + (1-Z) m,
# Budget'(mu) = B'.  FOC: b*Z*B' - 2 s (f - E y) = 0  =>  delta* = b Z B' / (2 s).
Bprime = 1.0 / q[0]   # $bn of budget per unit (decimal) of fused alpha, interior PE optimum
e5 = []
for b, s, Z in [(0.02, 50.0, 1.0), (0.02, 50.0, 0.4), (0.02, 200.0, 0.4), (0.005, 50.0, 0.4)]:
    e5.append({"b": b, "s": s, "Z": Z, "Bprime_bn_per_unit": round(Bprime, 1),
               "delta_star_bp": round(1e4 * b * Z * Bprime / (2 * s), 1)})
res["E5"] = e5

# ---------------------------------------------------------------- E6 Weitzman quantile result
# Bonus = B0 + beta*(yhat - ybar) + alpha_w*(y - yhat)^+ - gamma*(yhat - y)^+, alpha_w < beta < gamma
alpha_w, beta_w, gamma_w = 0.2, 0.6, 1.0
dist = stats.lognorm(s=0.5, scale=1.0)
def neg_exp_bonus(yh):
    # E[(y-yh)^+] and E[(yh-y)^+] via numerical integration
    up = integrate.quad(lambda y: (y - yh) * dist.pdf(y), yh, np.inf)[0]
    dn = integrate.quad(lambda y: (yh - y) * dist.pdf(y), 0, yh)[0]
    return -(beta_w * yh + alpha_w * up - gamma_w * dn)
opt = optimize.minimize_scalar(neg_exp_bonus, bounds=(0.05, 5.0), method="bounded")
res["E6"] = {
    "alpha_beta_gamma": [alpha_w, beta_w, gamma_w],
    "theory_quantile_level": (beta_w - alpha_w) / (gamma_w - alpha_w),
    "numerical_cdf_at_optimum": round(float(dist.cdf(opt.x)), 4),
}

# ---------------------------------------------------------------- E7 scoring
def interval_score(l, u, y, a):
    return (u - l) + (2 / a) * (l - y) * (y < l) + (2 / a) * (y - u) * (y > u)
def wis_p10_p50_p90(p10, p50, p90, y):
    # K = 1 interval at alpha = 0.2 plus the median; w0 = 1/2, w1 = alpha/2 (Bracher et al. 2021)
    return (0.5 * abs(y - p50) + 0.1 * interval_score(p10, p90, y, 0.2)) / 1.5
cases = {
    "group_forecast_hockey_stick": (0.12, 0.20, 0.26),   # forward IRR forecast for a co-invest
    "reference_class": (0.00, 0.10, 0.20),
}
y_real = 0.07
res["E7"] = {
    "realized": y_real,
    "WIS": {k: round(wis_p10_p50_p90(*v, y_real), 4) for k, v in cases.items()},
}
res["E7"]["WIS_skill_vs_reference"] = round(
    1 - res["E7"]["WIS"]["group_forecast_hockey_stick"] / res["E7"]["WIS"]["reference_class"], 3)
# implied dispersion inflation: stated 80% intervals covering only 36% (Ben-David et al. 2013)
kappa = stats.norm.ppf(0.9) / stats.norm.ppf((1 + 0.36) / 2)
res["E7"]["kappa_for_36pct_coverage_of_80pct_interval"] = round(float(kappa), 2)
# coverage needed before credibility is shown: binomial SE of 80% coverage with n forecasts
res["E7"]["coverage_se_n20_n50_n100"] = [round(math.sqrt(0.8 * 0.2 / n), 3) for n in (20, 50, 100)]

# ---------------------------------------------------------------- E8 internal transfer neutrality
fair = 0.90      # independent fair value as % of NAV (e.g., external bid evidence)
p_tr = 0.85      # internal transfer price agreed between groups
nav = 1.0        # $bn NAV transferred
fees = 0.004     # transfer/legal/GP-consent costs, $bn
res["E8"] = {
    "total_portfolio_liquidity_change_bn": -fees,
    "total_portfolio_value_change_bn": -fees,
    "PE_group_pnl_vs_fair_bn": round((p_tr - fair) * nav, 3),
    "SEC_group_pnl_vs_fair_bn": round((fair - p_tr) * nav, 3),
    "attribution_adjustment": "book both legs at fair value 0.90; the 0.05bn wedge is a centre item, not group DVA",
}

# ---------------------------------------------------------------- E9 tail-hedge break-even (liquidity provider credit)
# Hedge enters when  -carry + lambda_R * r + k * p * d >= 0  (per $ of premium, annual expected terms)
# carry c (expected loss as fraction of premium), r = CVaR reduction per $ premium, k = net crisis cash per $ premium,
# p = annual crisis probability, d = forced-sale discount avoided per $ of crisis cash.
e9 = []
for c_carry in (0.20, 0.45):
    lam_R, r_red, k_mult, p_c = 0.0475, 2.0, 4.0, 0.08
    d_star = (c_carry - lam_R * r_red) / (k_mult * p_c)
    e9.append({"carry": c_carry, "lambda_R": lam_R, "r": r_red, "k": k_mult, "p": p_c,
               "break_even_forced_sale_discount": round(d_star, 3)})
# crisis-liquidity dual at which the hedge would enter the E1 programme (other rows at their E1 duals)
mu = res["E1"]["duals_decimal"]
mu_star = (-alpha[7] - (-A[3, 7]) * mu["CVaR"] + A[0, 7] * mu["L12_drought"]
           - (-A[2, 7]) * mu["L24_crisis"]) / (-A[1, 7])
res["E9"] = {"break_even": e9, "E1_crisis_dual_needed_for_hedge_entry": round(float(mu_star), 4),
             "E1_crisis_dual_actual": mu["L12_crisis"]}

# ---------------------------------------------------------------- E10 no-regret budget bands from re-solves
# Fix group g at x*_g + d (others re-optimise); effective curvature H_g = 2*loss/d^2; band = sqrt(2*eps/H_g).
def value_with_fixed(gi, xval):
    xv = cp.Variable(8)
    cs = [A @ xv <= cap, xv >= lo, xv <= hi, xv[gi] == xval]
    pr = cp.Problem(cp.Maximize(alpha @ xv - 0.5 * cp.sum(cp.multiply(q, cp.square(xv)))), cs)
    pr.solve(solver=cp.CLARABEL)
    return float(pr.value) if pr.status == "optimal" else float("nan")

eps = 0.005  # $5m per year tolerated loss per group envelope
e10 = {}
for gi, g in enumerate(groups):
    if xs[gi] < 0.05:
        continue
    d = 0.25
    losses = []
    for sgn in (+1, -1):
        xv = min(max(xs[gi] + sgn * d, lo[gi]), hi[gi])
        losses.append(float(prob.value) - value_with_fixed(gi, xv))
    H = 2 * np.mean(losses) / d ** 2
    e10[g] = {"x_star_bn": round(float(xs[gi]), 3), "loss_at_pm0.25bn_mn": [round(1000 * l, 3) for l in losses],
              "effective_curvature": round(float(H), 5), "own_q": float(q[gi]),
              "band_pm_bn_for_5mn": round(float(math.sqrt(2 * eps / H)), 2)}
res["E10"] = e10

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=2)
print(json.dumps(res, indent=2))
