"""G10 stream (Real Assets: real estate). Part A: public-data timing/desmoothing; Part B: decision arithmetic.

Part A uses PUBLIC data only (not ADIC data):
  * NFI-ODCE gross quarterly total returns 1Q2022-2Q2026 as printed on NCREIF's 2Q2026 ODCE attribution
    webinar slides (16 Sep 2026), plus the 3Q2026 preliminary 1.71% from ncreif.org (index-returns page).
  * FTSE Nareit All Equity REITs total-return index (g10_reit_series_results.json, from Nareit's monthly file).
Part B is illustrative arithmetic on stated assumptions; every output is labelled ILLUSTRATIVE / SYNTHETIC.

Usage: python -I g10_public_and_arith.py <calc_dir>
"""
import json
import math
import sys

import numpy as np

CALC = sys.argv[1]
reit = json.load(open(f"{CALC}/g10_reit_series_results.json", encoding="utf-8"))

# ----------------------------------------------------------------------------------------------------------
# Part A1: quarterly series 2022Q1 .. 2026Q3
# ----------------------------------------------------------------------------------------------------------
odce_q = [7.4, 4.8, 0.5, -5.0, -3.2, -2.7, -1.9, -4.8, -2.4, -0.4, 0.2, 1.2, 1.1, 1.0, 0.7, 0.9, 1.2, 1.5, 1.71]
labels = [f"{y}Q{q}" for y in range(2022, 2027) for q in range(1, 5)][: len(odce_q)]
tri = {d: v for d, v in reit["quarterly_tri_1999_on"]}
qd = sorted(tri)
reit_q = []
for i, d in enumerate(qd):
    if d >= "2022-03-01" and d <= "2026-09-30":
        prev = tri[qd[i - 1]]
        reit_q.append(100 * (tri[d] / prev - 1))
assert len(reit_q) == len(odce_q), (len(reit_q), len(odce_q))
odce = np.array(odce_q) / 100
reitr = np.array(reit_q) / 100


def cum(x):
    return np.cumprod(1 + x)


def max_dd(x):
    c = np.concatenate([[1.0], cum(x)])
    peak = np.maximum.accumulate(c)
    dd = c / peak - 1
    j = int(np.argmin(dd))
    i = int(np.argmax(c[: j + 1]))
    return float(dd[j]), i, j  # index in level series (0 = end-2021)


# Unlever REITs (L_R = 0.33, cost of debt 4.5%/yr) and relever to ODCE leverage (L_O = 0.25, 4.5%/yr).
L_R, L_O, rd = 0.33, 0.25, 0.045 / 4
reit_unlev = (reitr - L_R * rd) / (1 - L_R) * (1 - L_R) + 0  # placeholder replaced below
reit_unlev = (1 - L_R) * reitr + L_R * rd            # asset return = E-weighted equity + D-weighted debt
reit_as_odce = (reit_unlev - L_O * rd) / (1 - L_O)  # relevered to ODCE-like leverage

# Geltner reverse filter on ODCE: r_T = (r_A - a r_A[-1])/(1-a), first obs uses r_A[-1] = r_A[0]
desm = {}
for a in (0.5, 0.6, 0.7, 0.8):
    rA = odce
    rT = (rA - a * np.concatenate([[rA[0]], rA[:-1]])) / (1 - a)
    dd, i, j = max_dd(rT)
    desm[str(a)] = {"max_dd_pct": round(100 * dd, 1), "peak_end_of": labels[i - 1] if i > 0 else "2021Q4",
                    "trough_end_of": labels[j - 1], "quarterly_sd_pct": round(100 * float(np.std(rT, ddof=1)), 2)}

dd_o, io, jo = max_dd(odce)
dd_r, ir, jr = max_dd(reitr)
dd_ro, iro, jro = max_dd(reit_as_odce)
# Approximate ODCE appreciation-only decline: subtract 0.9%/qtr income over the drawdown window (approximation).
n_q = jo - io
odce_value_dd_approx = (1 + dd_o) / (1.009 ** n_q) - 1

# Lead-lag: correlation of ODCE return at t with REIT return at t-k
xc = {}
for k in range(0, 5):
    a_ = odce[k:]
    b_ = reitr[: len(reitr) - k]
    xc[str(k)] = round(float(np.corrcoef(a_, b_)[0, 1]), 2)

# Stale-NAV gap: ln(cum ODCE) - ln(cum REIT-as-ODCE), both from end-2021 (gross, total-return basis)
gap = np.log(cum(odce)) - np.log(cum(reit_as_odce))

partA = {
    "label": "PUBLIC DATA computations (NCREIF NFI-ODCE gross quarterly returns as printed; FTSE Nareit All Equity REITs). Not ADIC data.",
    "quarters": labels,
    "odce_q_pct": odce_q,
    "reit_q_pct": [round(x, 2) for x in reit_q],
    "odce_max_dd_total_return_pct": round(100 * dd_o, 1),
    "odce_dd_window": [labels[io - 1] if io > 0 else "2021Q4", labels[jo - 1]],
    "odce_value_only_dd_approx_pct": round(100 * odce_value_dd_approx, 1),
    "reit_max_dd_quarterly_pct": round(100 * dd_r, 1),
    "reit_dd_window": [labels[ir - 1] if ir > 0 else "2021Q4", labels[jr - 1]],
    "reit_relevered_to_odce_max_dd_pct": round(100 * dd_ro, 1),
    "reit_relevered_dd_window": [labels[iro - 1] if iro > 0 else "2021Q4", labels[jro - 1]],
    "trough_lag_quarters_odce_vs_reit": int(jo - jr),
    "corr_odce_t_with_reit_t_minus_k": xc,
    "geltner_desmoothed_odce": desm,
    "stale_nav_gap_ln_pct_by_quarter": dict(zip(labels, [round(100 * x, 1) for x in gap])),
    "cum_2022Q1_2026Q3_pct": {"odce": round(100 * (cum(odce)[-1] - 1), 1), "reit": round(100 * (cum(reitr)[-1] - 1), 1),
                              "reit_relevered": round(100 * (cum(reit_as_odce)[-1] - 1), 1)},
    "assumptions": {"REIT leverage": L_R, "ODCE leverage": L_O, "cost of debt (annual)": 0.045},
}

# ----------------------------------------------------------------------------------------------------------
# Part A2: queue calibration replay. Others' redemption requests r = r0 + b*max(0, gap_{t-1}); payouts limited
# by liquidity L = l0 (income/cash) + dispositions d (share of NAV) + contributions c (lower when gap>0 or queue>5%).
# Target (Callan 4Q24 blog; Accordant Q1-2026): ODCE queue peak 19.3% of NAV in 1Q24; ~12% mid-2025; ~10% 1Q26.
# ----------------------------------------------------------------------------------------------------------
# Transaction window for the replay [I]: N in 2022H1, D from 2022Q3 to 2024Q2, N from 2024Q3 (volumes recovering).
E_REPLAY = ["N", "N"] + ["D"] * 8 + ["N"] * 9
# Dispositions, share of GAV per quarter [I]; sized so that N-state payout capacity (~1.5% of NAV a quarter) is
# consistent with ODCE's year to June 2026: distributions + redemptions $19.1bn = 8.5% of $223.7bn NAV, of which
# roughly 3-4 points are income distributions (NCREIF 2Q2026 press release; split is an inference).
DISP = {"O": 0.010, "N": 0.006, "D": 0.004, "F": 0.002}
GAV_NAV = 1 / (1 - 0.27)                                  # ODCE leverage 27.1% (NCREIF 2Q2026)


def queue_replay(b, w, r0=0.006, l0=0.0025, c_hi=0.012, c_lo=0.004, gap_series=gap, e_path=E_REPLAY):
    Q, out, paid = 0.0, [], []
    for t in range(len(gap_series)):
        g_prev = gap_series[t - 1] if t > 0 else 0.0
        req = r0 + b * max(0.0, g_prev)
        withdraw = w * Q if g_prev <= 0.03 else 0.0          # cancellations once the stale-NAV premium is gone
        contrib = c_lo if (g_prev > 0.03 or Q > 0.05) else c_hi
        L = l0 + DISP[e_path[t]] * GAV_NAV + contrib
        Q = max(0.0, Q + req - withdraw)
        pay = min(Q, L)
        Q -= pay
        out.append(Q)
        paid.append(pay)
    return out, paid


best = None
for b in np.linspace(0.02, 0.40, 77):
    for w in np.linspace(0.0, 0.30, 31):
        path, paid = queue_replay(b, w)
        err = ((path[labels.index("2024Q1")] - 0.193) ** 2 + (path[labels.index("2025Q2")] - 0.12) ** 2
               + (path[labels.index("2026Q1")] - 0.105) ** 2)
        if best is None or err < best[0]:
            best = (err, b, w, path, paid)
partA["queue_replay"] = {
    "label": "Calibration replay of the open-end queue machine on PUBLIC gap data (illustrative fit, 2 parameters)",
    "b_fit": round(float(best[1]), 3), "withdraw_fit": round(float(best[2]), 3),
    "queue_pct_nav": dict(zip(labels, [round(100 * q, 1) for q in best[3]])),
    "paid_pct_nav": dict(zip(labels, [round(100 * q, 2) for q in best[4]])),
    "targets": {"2024Q1": 19.3, "2025Q2": "about 12", "2026Q1": "just above 10"},
    "fixed_inputs": {"r0": 0.006, "l0": 0.0025, "contrib_hi/lo": [0.012, 0.004], "disp": DISP, "e_path": E_REPLAY},
}

# ----------------------------------------------------------------------------------------------------------
# Part B: decision arithmetic (ILLUSTRATIVE)
# ----------------------------------------------------------------------------------------------------------
B = {"label": "ILLUSTRATIVE arithmetic on stated assumptions; SYNTHETIC where applied to ADIC-like positions"}

# B1: cap-rate shock grid: value change = (NOI growth factor) * c0/(c0+dc) - 1
grid = {}
for c0 in (0.045, 0.055, 0.065, 0.075):
    for dc in (0.0025, 0.005, 0.0075, 0.01, 0.015):
        for gN in (0.0, 0.03):
            grid[f"c0={c0:.3f} dc=+{int(dc*1e4)}bp g_NOI={gN:.0%}"] = round(100 * ((1 + gN) * c0 / (c0 + dc) - 1), 1)
B["cap_rate_shock_value_change_pct"] = grid

# B2: required cap rate for a target risk premium over the 10y: c_req = y10 + RP + capex - g
y10 = 0.051
B["required_cap_rate_pct"] = {}
for RP in (0.015, 0.025, 0.035):
    for g in (0.02, 0.03):
        for capex in (0.012, 0.018):
            c_req = y10 + RP + capex - g
            B["required_cap_rate_pct"][f"RP={RP:.1%} g={g:.0%} capex={capex:.1%}"] = round(100 * c_req, 2)
# implied expected return at today's appraisal yield 4.7% (NPI income return, RCLCO Q2-2026)
for g in (0.02, 0.025, 0.03):
    B.setdefault("implied_premium_at_appraisal_yield_4.7pct", {})[f"g={g:.1%}"] = round(100 * (0.047 + g - 0.013 - y10), 2)

# B3: refinancing gap on a 2021-vintage loan maturing late-2026
V0, LTV0, c_entry = 100.0, 0.65, 0.045
D = V0 * LTV0
rows = {}
for c_now in (0.055, 0.06, 0.065):
    for gN in (0.0, 0.10):
        NOI0 = c_entry * V0
        NOI = NOI0 * (1 + gN)
        V = NOI / c_now
        r_new = 0.051 + 0.0200          # 10y + 200bp
        cap_ltv = 0.60 * V
        cap_dscr = NOI / (1.25 * r_new)
        Dmax = min(cap_ltv, cap_dscr)
        rows[f"exit/refi cap {c_now:.1%}, NOI growth {gN:.0%}"] = {
            "value": round(V, 1), "LTV_now_pct": round(100 * D / V, 1), "Dmax": round(Dmax, 1),
            "binding": "LTV" if cap_ltv < cap_dscr else "DSCR", "gap": round(max(0.0, D - Dmax), 1),
            "gap_pct_of_value": round(100 * max(0.0, D - Dmax) / V, 1),
            "equity_before_pct_of_entry_equity": round(100 * (V - D) / (V0 - D), 1)}
B["refi_gap_2021_vintage"] = {"assumptions": "V0=100 at 4.5% cap, 65% LTV, IO; new loan 10y(5.1%)+200bp, LTV<=60%, DSCR>=1.25x",
                              "rows": rows}

# B4: negative leverage check: levered cash yield = (c - LTV*r_d)/(1-LTV)
lev = {}
for c in (0.05, 0.056, 0.064, 0.07):
    for r_d in (0.062, 0.068, 0.075):
        lev[f"cap {c:.1%} debt {r_d:.1%}"] = {f"LTV {L:.0%}": round(100 * (c - L * r_d) / (1 - L), 2) for L in (0.0, 0.5, 0.6)}
B["levered_cash_yield_pct"] = lev
# break-even NOI growth for LEVER to add expected return: levered return > unlevered iff unlevered total return > r_d
B["lever_rule"] = "LEVER adds expected return iff E[r_unlevered] = c - capex + g > r_d (plus risk and liquidity charges)"

# B5: SELL a closed-end VA fund interest at 68% of reported NAV vs HOLD (no unfunded)
# Hold value: PV at hurdle h of forward cash flows from NAV_T (economic) growing at mu, liquidated evenly over T years.
def hold_value(mu, h, T, econ_to_rep):
    # cash flows: equal fractions of the (growing) NAV paid out at the end of years 1..T
    nav = econ_to_rep
    pv = 0.0
    for t in range(1, T + 1):
        nav *= (1 + mu)
        cf = nav / (T - t + 1)
        nav -= cf
        pv += cf / (1 + h) ** t
    return pv


sell = {}
for econ in (1.0, 0.92, 0.85):
    for mu in (0.04, 0.08, 0.12):
        for ell in (0.0, 0.02, 0.05):
            h = 0.08 + ell
            sell[f"econ/rep={econ:.2f} mu={mu:.0%} hurdle=8%+l={ell:.0%}"] = round(100 * hold_value(mu, h, 4, econ), 1)
B["fund_interest_hold_value_pct_of_reported_nav"] = {"note": "SELL iff bid (68% H1-2026, Jefferies) > value; 4-year run-off",
                                                     "values": sell}
# buyer-implied IRR at 68% with 4-year run-off, for given economic NAV/forward growth
def implied_irr(price, mu, T, econ):
    lo, hi = -0.5, 1.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if hold_value(mu, mid, T, econ) > price:
            lo = mid
        else:
            hi = mid
    return mid


B["buyer_irr_at_68pct"] = {f"econ/rep={e:.2f} mu={m:.0%}": round(100 * implied_irr(0.68, m, 4, e), 1)
                           for e in (1.0, 0.92, 0.85) for m in (0.04, 0.08)}

# B6: open-end redemption at stale NAV: value per $1 of current reported NAV of redeeming through a queue that pays
# a fraction p per quarter, when the appraisal gap G closes linearly over K quarters, vs holding (receives V_T path).
def redeem_value(p, G, K, h_q, drift_q):
    rem, val, nav = 1.0, 0.0, 1.0
    for t in range(1, 41):
        # reported NAV per unit drifts at true drift minus gap closure
        nav *= (1 + drift_q) * math.exp(-G / K if t <= K else 0.0)
        pay = rem * p
        val += pay * nav / (1 + h_q) ** t
        rem -= pay
    val += rem * nav / (1 + h_q) ** 40
    return val


red = {}
for G in (0.0, 0.05, 0.10, 0.15):
    for p in (0.05, 0.10, 0.25):
        # drift = hurdle, so HOLD is worth the true value exp(-G); the difference is the stale-NAV premium captured
        red[f"gap={G:.0%} payout/qtr={p:.0%}"] = round(100 * redeem_value(p, G, 6, 0.08 / 4, 0.08 / 4), 1)
hold = {f"gap={G:.0%}": round(100 * math.exp(-G), 1) for G in (0.0, 0.05, 0.10, 0.15)}
B["open_end_redeem_vs_hold"] = {"note": "value per $1 reported NAV, forward return = hurdle (8%); HOLD = exp(-gap). "
                                        "Liquidity value of earlier cash (l) is extra and not included.",
                                "redeem": red, "hold_true_value": hold}

# B7: cash-out refinance cost per $ raised vs liquidity premium (one period approx)
B["cash_out_refi"] = {
    "rule": "REFINANCE iff spread_over_ref + fees/T + lambda_Lev + covenant charge < l_bar (one-period: rho > s)",
    "example": {"asset value": 100, "LTV from": 0.40, "LTV to": 0.55, "cash raised": 15.0, "all-in rate": 0.068,
                "property cap rate": 0.056, "negative carry per $ raised (rate - cap)": round(0.068 - 0.056, 4),
                "fees (1% of new loan, 3-yr)": round(0.01 * 55 / 15 / 3, 4)},
}

out = {"partA": partA, "partB": B}
with open(f"{CALC}/g10_public_and_arith_results.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps({k: partA[k] for k in partA if k not in ("stale_nav_gap_ln_pct_by_quarter", "queue_replay")}, indent=1))
print(json.dumps(partA["queue_replay"], indent=1))
print(json.dumps(partA["stale_nav_gap_ln_pct_by_quarter"], indent=1))
print(json.dumps(B["refi_gap_2021_vintage"], indent=1))
print(json.dumps(B["buyer_irr_at_68pct"], indent=1))
print(json.dumps(B["open_end_redeem_vs_hold"], indent=1))
print(json.dumps(B["implied_premium_at_appraisal_yield_4.7pct"], indent=1))
