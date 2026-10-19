"""
Worked examples for dossier 08 (SELL / HOLD / REFINANCE / LEVER in a common currency).

Inputs are (a) from the research brief, (b) sourced market data (SOFR 3.89% on
2026-10-15, FRED; Jefferies H1-2026 secondary pricing; Rede 2025 NAV-loan margins),
or (c) explicit illustrative assumptions flagged as such.

Valuation currency: liquidity-adjusted present value (LAPV) in today's dollars.
  risky fund cash flow at t : DF_h(t) = prod_{k<=t} 1/((1+r_h)(1+l_k))
  contractual cash flow at t: DF_f(t) = prod_{k<=t} 1/((1+r_f)(1+l_k))
where l_k is the portfolio liquidity shadow price (annualised, FTP-style term structure).
"""
import json
import numpy as np
from scipy.optimize import brentq, milp, LinearConstraint, Bounds, linprog

OUT = {}
SOFR = 0.0389          # FRED SOFR, 2026-10-15
RF = SOFR              # riskless proxy for a sovereign investor (assumption)
ERP = 0.0425           # equity risk premium over cash for the funding-basket hurdle (assumption)
TC_SALE = 0.0075       # secondary transaction cost, % of NAV (assumption)


def dfs(rate, ell):
    T = len(ell)
    df = np.ones(T + 1)
    for t in range(1, T + 1):
        df[t] = df[t - 1] / ((1 + rate) * (1 + ell[t - 1]))
    return df


def irr(cfs):
    f = lambda r: sum(cf / (1 + r) ** t for t, cf in enumerate(cfs))
    return brentq(f, -0.9, 2.0)


# ===========================================================================
# EXAMPLE 1: 2018-vintage buyout fund
# ===========================================================================
NAV0, UNF = 500.0, 50.0
G_MEAN, G_SD = 0.11, 0.06
PRICE = 0.88
LTV, SPREAD_NAV, NAV_FEE = 0.15, 0.06, 0.015
R_B = SOFR + SPREAD_NAV
BETA_BO = 1.2
R_H = RF + BETA_BO * ERP
RD = np.array([0.15, 0.20, 0.25, 0.30, 0.40, 1.00])   # DPI-drought calibrated distribution rates (assumption)
CALLS = np.array([15.0, 10.0, 5.0])                   # expected calls t=0,1,2 (60% of unfunded; assumption)
ELL = np.array([0.09, 0.09, 0.04, 0.04, 0.04, 0.04])  # brief
KAPPA_GP = 1.8                                        # expected GP-relationship cost of selling, $m (assumption)
T1 = len(RD)


def fund_cf(nav0, g, rd=RD, calls=CALLS):
    T = len(rd)
    gg = np.full(T, g) if np.isscalar(g) else np.asarray(g)
    D, C, NAV = np.zeros(T + 1), np.zeros(T + 1), np.zeros(T + 1)
    NAV[0] = nav0
    for t in range(1, T + 1):
        c = calls[t - 1] if t - 1 < len(calls) else 0.0
        C[t - 1] += c
        pre = (NAV[t - 1] + c) * (1 + gg[t - 1])
        D[t] = rd[t - 1] * pre
        NAV[t] = pre - D[t]
    return D, C, NAV


def lapv_hold(nav0, g, ell=ELL, r_h=R_H, r_f=RF, rd=RD, calls=CALLS):
    D, C, _ = fund_cf(nav0, g, rd, calls)
    return float(D @ dfs(r_h, ell) - C @ dfs(r_f, ell)), D, C


def lapv_sale(nav0, price, ell=ELL, r_f=RF, defer_frac=0.0, defer_years=1, tc=TC_SALE, kappa=KAPPA_GP):
    gross = price * nav0
    return float(gross * (1 - defer_frac) + gross * defer_frac * dfs(r_f, ell)[defer_years] - tc * nav0 - kappa)


def nav_loan(D, C, ell=ELL, r_f=RF, ltv=LTV, nav0=NAV0, r_b=R_B, fee=NAV_FEE, sweep=1.0, maturity=4):
    df = dfs(r_f, ell)
    L = ltv * nav0
    bal, pays = L, np.zeros(len(D))
    for t in range(1, len(D)):
        if bal <= 1e-9:
            break
        due = bal * (1 + r_b)
        avail = sweep * max(D[t] - (C[t] if t < len(C) else 0.0), 0.0)
        pay = due if t == maturity else min(due, max(avail, bal * r_b))
        pays[t] = pay
        bal = due - pay
    life = int(np.max(np.nonzero(pays)[0])) if pays.any() else 0
    return L * (1 - fee) - float(pays @ df), pays, life


def best_refi(D, C, ell=ELL):
    vals = {s: nav_loan(D, C, ell=ell, sweep=s)[0] for s in (1.0, 0.5, 0.25)}
    s = max(vals, key=vals.get)
    return vals[s], s


ex1 = {}
VH, D, C = lapv_hold(NAV0, G_MEAN)
ex1["inputs"] = dict(NAV0=NAV0, UNF=UNF, g_mean=G_MEAN, g_sd=G_SD, price=PRICE, ltv=LTV, r_b=round(R_B, 4),
                     sofr=SOFR, r_h=round(R_H, 4), r_f=RF, ell=ELL.tolist(), rd=RD.tolist(),
                     calls=CALLS.tolist(), tc=TC_SALE, kappa_gp=KAPPA_GP, nav_fee=NAV_FEE)
ex1["cashflows"] = dict(D=np.round(D, 1).tolist(), C=np.round(C, 1).tolist(),
                        total_D=round(float(D.sum()), 1), total_C=round(float(C.sum()), 1),
                        check_irr=round(irr([-NAV0 - C[0]] + [D[t] - C[t] for t in range(1, len(D))]), 4))
net = np.clip(D - C, 0, None)
ex1["cash_weighted_life_yrs"] = round(float((np.arange(len(net)) * net).sum() / net.sum()), 2)
VH0, _, _ = lapv_hold(NAV0, G_MEAN, ell=np.zeros(T1))
VS = lapv_sale(NAV0, PRICE)
refi = {}
for sw in (1.0, 0.5, 0.25):
    v, pays, life = nav_loan(D, C, sweep=sw)
    refi[f"sweep_{int(sw*100)}"] = dict(value=round(v, 2), life_years=life, pays=np.round(pays, 1).tolist())
VR, SW = best_refi(D, C)
ex1["values"] = dict(
    hold=round(VH, 2), hold_pct_nav=round(VH / NAV0, 4),
    hold_if_no_liquidity_premium=round(VH0, 2), hold_if_no_liq_pct_nav=round(VH0 / NAV0, 4),
    sell_cash=round(VS, 2),
    sell_88_50pct_deferred_12m=round(lapv_sale(NAV0, PRICE, defer_frac=0.5), 2),
    sell_92_50pct_deferred_12m=round(lapv_sale(NAV0, 0.92, defer_frac=0.5), 2),
    refi=refi, best_refi=round(VR, 2), best_refi_sweep=SW,
    refi_if_no_liquidity_premium=round(nav_loan(D, C, ell=np.zeros(T1), sweep=0.5)[0], 2),
    hold_plus_refi=round(VH + VR, 2),
    sell_minus_hold_plus_refi=round(VS - VH - VR, 2),
)
ex1["reservation_price_cash_vs_hold"] = round((VH + TC_SALE * NAV0 + KAPPA_GP) / NAV0, 4)
ex1["reservation_price_cash_vs_hold_refi"] = round((VH + VR + TC_SALE * NAV0 + KAPPA_GP) / NAV0, 4)
ex1["reservation_price_if_no_liquidity_premium"] = round((VH0 + TC_SALE * NAV0 + KAPPA_GP) / NAV0, 4)
# deferred-structure equivalent: headline price needed with 50% deferred 12m to match cash 88%
ex1["headline_needed_50pct_deferred_to_match_cash88"] = round(
    brentq(lambda p: lapv_sale(NAV0, p, defer_frac=0.5) - VS, 0.5, 1.5), 4)


def gap_ell12(x):
    ell = ELL.copy(); ell[:2] = x
    vh, d, c = lapv_hold(NAV0, G_MEAN, ell=ell)
    return lapv_sale(NAV0, PRICE, ell=ell) - (vh + max(0.0, best_refi(d, c, ell)[0]))


ex1["breakeven_ell_y1y2"] = round(brentq(gap_ell12, -0.05, 0.40), 4)


def gap_g(g):
    vh, d, c = lapv_hold(NAV0, g)
    return (vh + max(0.0, best_refi(d, c)[0])) - VS


ex1["breakeven_forward_irr"] = round(brentq(gap_g, -0.2, 0.6), 4)
sale_cfs = [PRICE * NAV0 - TC_SALE * NAV0 - KAPPA_GP + C[0]] + [-(D[t] - C[t]) for t in range(1, len(D))]
ex1["implied_cost_of_sale_irr"] = round(irr(sale_cfs), 4)
ex1["implied_cost_of_sale_spread_over_r_h"] = round((1 + irr(sale_cfs)) / (1 + R_H) - 1, 4)
_, p50, _ = nav_loan(D, C, sweep=0.5)
loan_cfs = [LTV * NAV0 * (1 - NAV_FEE)] + [-p for p in p50[1:]]
ex1["implied_cost_of_navloan_irr"] = round(irr(loan_cfs), 4)
ex1["implied_cost_of_navloan_spread_over_rf"] = round((1 + irr(loan_cfs)) / (1 + RF) - 1, 4)

grid = {}
for p in (0.80, 0.84, 0.86, 0.88, 0.91, 0.94):
    row = {}
    for e in (0.0, 0.04, 0.06, 0.09, 0.12):
        ell = ELL.copy(); ell[:2] = e
        vh, d, c = lapv_hold(NAV0, G_MEAN, ell=ell)
        row[f"ell{int(e*100)}"] = round(lapv_sale(NAV0, p, ell=ell) - (vh + max(0.0, best_refi(d, c, ell)[0])), 1)
    grid[f"p{int(round(p*100))}"] = row
ex1["grid_sell_minus_best_keep"] = grid

rng = np.random.default_rng(20261018)
g_draw = rng.normal(G_MEAN, G_SD, 50_000)
dh, dff = dfs(R_H, ELL), dfs(RF, ELL)
vh_draw = np.empty_like(g_draw)
for i, g in enumerate(g_draw):
    d, c, _ = fund_cf(NAV0, g)
    vh_draw[i] = d @ dh - c @ dff
keep = vh_draw + VR
ex1["mc"] = dict(p_keep_beats_sell=round(float((keep > VS).mean()), 3),
                 hold_lapv_p10=round(float(np.percentile(vh_draw, 10)), 1),
                 hold_lapv_p50=round(float(np.percentile(vh_draw, 50)), 1),
                 hold_lapv_p90=round(float(np.percentile(vh_draw, 90)), 1),
                 expected_regret_if_sell=round(float(np.clip(keep - VS, 0, None).mean()), 2),
                 expected_regret_if_keep=round(float(np.clip(VS - keep, 0, None).mean()), 2),
                 evpi=round(float(np.maximum(keep, VS).mean() - max(keep.mean(), VS)), 2))


def wait_one_year(n=100_000, p_stress=0.15, seed=7):
    """Hold for one year, learn g perfectly, then sell or hold. Stress (15%): year-1 mark-down
    of 15%, exits stall (RD halved), secondary price 72%, liquidity premium spikes to 15%/8%."""
    rng = np.random.default_rng(seed)
    g = rng.normal(G_MEAN, G_SD, n)
    stress = rng.random(n) < p_stress
    v_opt, v_hold, sold = np.empty(n), np.empty(n), np.empty(n, dtype=bool)
    for i in range(n):
        s = stress[i]
        pre = (NAV0 + CALLS[0]) * (1 + g[i] - (0.15 if s else 0.0))
        d1 = RD[0] * (0.5 if s else 1.0) * pre
        nav1 = pre - d1
        ell_after = np.array([0.15, 0.08, 0.04, 0.04, 0.04]) if s else ELL[1:].copy()
        d, c, _ = fund_cf(nav1, g[i], rd=RD[1:], calls=CALLS[1:])
        cont = d @ dfs(R_H, ell_after) - c @ dfs(RF, ell_after)
        p1 = min(max((0.72 if s else PRICE) + 0.6 * (g[i] - G_MEAN), 0.5), 1.0)
        sale1 = p1 * nav1 - TC_SALE * nav1 - KAPPA_GP
        sold[i] = sale1 > cont
        disc = (1 + R_H) * (1 + ELL[0])
        v_opt[i] = (d1 + max(sale1, cont)) / disc
        v_hold[i] = (d1 + cont) / disc
    return (float(v_opt.mean()) - CALLS[0], float(v_hold.mean()) - CALLS[0], float(sold.mean()),
            float(sold[stress].mean()), float(sold[~stress].mean()))


vw, vw0, fs, fss, fsn = wait_one_year()
ex1["wait_one_year"] = dict(value_with_option=round(vw, 2), value_never_sell_same_scenarios=round(vw0, 2),
                            option_value_of_waiting=round(vw - vw0, 2), frac_sell_t1=round(fs, 3),
                            frac_sell_t1_stress=round(fss, 3), frac_sell_t1_normal=round(fsn, 3),
                            sell_now=round(VS, 2))
ann4 = dfs(RF, ELL)[1:5].sum()
ex1["sell_risk_relief"] = {f"lambdaR_{lam}": round(lam * 0.25 * NAV0 * ann4, 2) for lam in (0.0, 0.01, 0.03)}
ex1["sell_minus_keep_vs_kappa_gp"] = {f"kappa_{k}": round(VS + KAPPA_GP - k - VH - VR, 2) for k in (0.0, 1.8, 5.0, 10.0)}
OUT["example1"] = ex1

# ===========================================================================
# EXAMPLE 2: same asset, five actions, across portfolio liquidity states
#   LEVER = ADD (buy increment) + REFI (borrow) - leverage-capacity charge
# ===========================================================================
NAVB, MU, MU_SD, YIELD, BETA_B, T2 = 400.0, 0.11, 0.04, 0.065, 0.5, 5
R_HB = RF + BETA_B * ERP
DX = 120.0                        # increment / borrowing capacity (30% of NAV)
R_BB, FEE_B = SOFR + 0.025, 0.0075   # asset-backed facility, SOFR+250, 0.75% fee, 5y bullet (illustrative)
LAMBDA_R, M_CVAR, LAMBDA_LEV = 0.03, 0.15, 0.0025   # illustrative portfolio duals
SALE_B = 0.91                     # Jefferies H1-2026 infrastructure LP pricing (% NAV)


def asset_cf(nav0, mu, y=YIELD, T=T2):
    D, NAV = np.zeros(T + 1), nav0
    for t in range(1, T + 1):
        d = y * NAV
        NAV = NAV * (1 + mu) - d
        D[t] = d + (NAV if t == T else 0.0)
    return D


def actions_B(ell, mu=MU, lam_r=LAMBDA_R, lam_lev=LAMBDA_LEV):
    dh, df = dfs(R_HB, ell), dfs(RF, ell)
    ann = df[1:].sum()
    v_hold = float(asset_cf(NAVB, mu) @ dh)
    pays = np.zeros(T2 + 1); pays[1:] = DX * R_BB; pays[T2] += DX
    refi = DX * (1 - FEE_B) - float(pays @ df) - lam_lev * DX * ann
    add = float(asset_cf(DX, mu) @ dh) - DX - lam_r * M_CVAR * DX * ann
    sell = SALE_B * NAVB - TC_SALE * NAVB - v_hold + lam_r * M_CVAR * NAVB * ann
    lever = add + refi
    return dict(HOLD=0.0, SELL=round(sell, 2), REFI=round(refi, 2), ADD=round(add, 2), LEVER=round(lever, 2)), v_hold


ex2 = dict(inputs=dict(NAVB=NAVB, mu=MU, mu_sd=MU_SD, cash_yield=YIELD, beta=BETA_B, r_h=round(R_HB, 4),
                       dx=DX, r_b=round(R_BB, 4), fee=FEE_B, lambda_R=LAMBDA_R, m_cvar=M_CVAR,
                       lambda_lev=LAMBDA_LEV, sale_price=SALE_B))
states = {f"flat_{int(e*100)}pct": np.full(T2, e) for e in (0.0, 0.02, 0.03, 0.04, 0.05, 0.06, 0.09)}
states["example1_term_structure"] = ELL[:T2].copy()
smap = {}
for k, ell in states.items():
    a, vh = actions_B(ell)
    smap[k] = dict(actions=a, best=max(a, key=a.get), hold_lapv=round(vh, 1))
ex2["state_map"] = smap
# LEVER region in flat-ell space
lev_region = [round(e, 3) for e in np.arange(0.0, 0.12, 0.0025) if
              (lambda a: max(a, key=a.get))(actions_B(np.full(T2, e))[0]) == "LEVER"]
ex2["lever_optimal_flat_ell_range"] = [min(lev_region), max(lev_region)] if lev_region else None
# Focus state: flat 4% (Example 1's state from year 3 onward)
ell4 = np.full(T2, 0.04)
a4, vh4 = actions_B(ell4)
ex2["focus_state_flat4"] = dict(actions=a4, best=max(a4, key=a4.get))
ex2["breakeven_mu_lever_vs_hold_flat4"] = round(brentq(lambda m: actions_B(ell4, mu=m)[0]["LEVER"], -0.2, 0.5), 4)
ex2["breakeven_mu_lever_vs_refi_flat4"] = round(brentq(lambda m: actions_B(ell4, mu=m)[0]["ADD"], -0.2, 0.5), 4)
pays = np.zeros(T2 + 1); pays[1:] = DX * R_BB; pays[T2] += DX
ex2["lever_net_liquidity_profile"] = np.round((asset_cf(DX, MU) - pays)[1:], 2).tolist()
ex2["spread_decomposition_pa"] = dict(alpha_star=round(MU - R_HB, 4), credit_spread=round(R_BB - RF, 4),
                                      fee_amortised=round(FEE_B / T2, 4),
                                      risk_budget_charge=round(LAMBDA_R * M_CVAR, 4),
                                      leverage_capacity_charge=LAMBDA_LEV)
rng = np.random.default_rng(11)
mu_draw = rng.normal(MU, MU_SD, 20_000)
lv = np.array([actions_B(ell4, mu=m)[0]["LEVER"] for m in mu_draw])
ad = np.array([actions_B(ell4, mu=m)[0]["ADD"] for m in mu_draw])
vol, n = 0.09, 50_000
mu2 = rng.normal(MU, MU_SD, n)
paths = rng.normal(0, vol, (n, T2))
nav_tot = (NAVB + DX) * np.cumprod(1 + (mu2[:, None] - YIELD) + paths - 0.5 * vol ** 2, axis=1)
breach = ((DX / nav_tot) > 0.40).any(axis=1)
ex2["mc_flat4"] = dict(p_lever_beats_hold=round(float((lv > 0).mean()), 3),
                       p_lever_beats_refi=round(float((ad > 0).mean()), 3),
                       lever_p10=round(float(np.percentile(lv, 10)), 1),
                       lever_p50=round(float(np.percentile(lv, 50)), 1),
                       lever_p90=round(float(np.percentile(lv, 90)), 1),
                       p_ltv_above_40pct=round(float(breach.mean()), 4),
                       initial_ltv=round(DX / (NAVB + DX), 3))
OUT["example2"] = ex2

# ===========================================================================
# EXAMPLE 3: price decomposition, 40 assets x {HOLD, SELL, REFI, LEVER}, 4 coupling constraints
# ===========================================================================
rng = np.random.default_rng(42)
N = 40
nav = np.round(rng.lognormal(np.log(300), 0.6, N), 1)
age = rng.integers(2, 13, N)
fwd = np.clip(rng.normal(0.10, 0.03, N), 0.02, 0.18)
beta = np.clip(rng.normal(1.0, 0.3, N), 0.3, 1.6)
hurdle = RF + beta * ERP
dur = np.clip(7 - 0.45 * age, 1.5, 5.5)
yld = np.clip(0.06 + 0.02 * age, 0.06, 0.35)
price = np.clip(0.97 - 0.012 * age - rng.normal(0, 0.03, N), 0.55, 1.0)
unf = nav * np.clip(0.35 - 0.03 * age, 0.0, 0.3)
lever_ok = (beta < 0.9) & (fwd > 0.09)
hold_pv = nav * ((1 + fwd) / (1 + hurdle)) ** dur
dV, dL1, dL2, dR, dLev = (np.zeros((N, 4)) for _ in range(5))
K_RISK = 0.20
# SELL
dV[:, 1] = price * nav - TC_SALE * nav - hold_pv
dL1[:, 1] = price * nav - yld * nav + 0.5 * unf
dL2[:, 1] = -yld * nav * (1 + fwd) + 0.3 * unf
dR[:, 1] = -K_RISK * beta * nav
# REFI: 15% LTV, SOFR+600, 2-year bullet
L = 0.15 * nav
dV[:, 2] = -(R_B - RF) * L * 1.9 - NAV_FEE * L
dL1[:, 2] = L * (1 - NAV_FEE) - R_B * L
dL2[:, 2] = -L * (1 + R_B)
dR[:, 2] = 0.02 * L
dLev[:, 2] = L
# LEVER: +30% exposure funded with debt at SOFR+300, 1% fee, 5y
R_BB3, FEE_B3 = SOFR + 0.03, 0.01
X = 0.30 * nav
dV[:, 3] = np.where(lever_ok, X * (((1 + fwd) / (1 + hurdle)) ** 5 - 1) - X * ((R_BB3 - RF) * 4.4 + FEE_B3), -1e3)
dL1[:, 3] = np.where(lever_ok, X * (yld - R_BB3), 0.0)
dL2[:, 3] = np.where(lever_ok, X * (yld - R_BB3), 0.0)
dR[:, 3] = np.where(lever_ok, K_RISK * beta * X, 0.0)
dLev[:, 3] = np.where(lever_ok, X, 0.0)
NEED1, NEED2 = 3800.0, -900.0     # yr-1 need; yr-2 baseline surplus that increments may draw down ($m)
RISK_CAP = -800.0                 # book must cut CVaR usage by $800m
LEV_CAP = 1200.0                  # leverage capacity ($m)

nv = N * 4
c = -dV.ravel()
A_eq = np.zeros((N, nv))
for i in range(N):
    A_eq[i, 4 * i:4 * i + 4] = 1
A_ub = np.vstack([-dL1.ravel(), -dL2.ravel(), dR.ravel(), dLev.ravel()])
b_ub = np.array([-NEED1, -NEED2, RISK_CAP, LEV_CAP])
res_mip = milp(c, constraints=[LinearConstraint(A_eq, 1, 1), LinearConstraint(A_ub, -np.inf, b_ub)],
               integrality=np.ones(nv), bounds=Bounds(0, 1))
assert res_mip.status == 0, res_mip.message
x_mip = np.round(res_mip.x).reshape(N, 4)
res_lp = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=np.ones(N), bounds=(0, 1), method="highs")
duals = -res_lp.ineqlin.marginals
x_lp = res_lp.x.reshape(N, 4)
fr = ((x_lp > 1e-6) & (x_lp < 1 - 1e-6)).any(axis=1)
priced = dV + duals[0] * dL1 + duals[1] * dL2 - duals[2] * dR - duals[3] * dLev
x_dec = np.zeros_like(x_mip); x_dec[np.arange(N), priced.argmax(axis=1)] = 1
names = ["HOLD", "SELL", "REFI", "LEVER"]
use = lambda x: dict(liq1=round(float((x * dL1).sum()), 1), liq2=round(float((x * dL2).sum()), 1),
                     risk=round(float((x * dR).sum()), 1), lev=round(float((x * dLev).sum()), 1))
OUT["example3"] = dict(
    book_nav=round(float(nav.sum()), 1), needs=dict(liq1=NEED1, liq2=NEED2, risk_cap=RISK_CAP, lev_cap=LEV_CAP),
    mip_objective=round(-res_mip.fun, 1), lp_objective=round(-res_lp.fun, 1),
    gap=round(-res_lp.fun + res_mip.fun, 2),
    shadow_prices=dict(liq_y1=round(duals[0], 4), liq_y2=round(duals[1], 4),
                       risk=round(duals[2], 4), leverage=round(duals[3], 4)),
    lp_fractional_assets=int(fr.sum()),
    mip_action_counts={names[a]: int(x_mip[:, a].sum()) for a in range(4)},
    decentralised_action_counts={names[a]: int(x_dec[:, a].sum()) for a in range(4)},
    decentralised_vs_mip_disagreements=int((x_dec.argmax(1) != x_mip.argmax(1)).sum()),
    decentralised_objective=round(float((x_dec * dV).sum()), 1),
    mip_usage=use(x_mip), decentralised_usage=use(x_dec),
    marginal_assets=[dict(i=int(i), nav=float(nav[i]), age=int(age[i]), price=round(float(price[i]), 3),
                          fwd=round(float(fwd[i]), 3), beta=round(float(beta[i]), 2), mip=names[int(x_mip[i].argmax())],
                          lp_mix={names[a]: round(float(x_lp[i, a]), 2) for a in range(4) if x_lp[i, a] > 1e-6})
                     for i in np.where(fr)[0]],
)

print(json.dumps(OUT, indent=1))
with open(__file__.replace(".py", "_results.json"), "w") as f:
    json.dump(OUT, f, indent=1)
