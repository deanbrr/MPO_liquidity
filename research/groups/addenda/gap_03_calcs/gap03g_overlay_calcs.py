"""
Group 7 (Overlay) addendum calculations for research/groups/addenda/gap_03.md.

EVERYTHING BELOW IS SYNTHETIC / ILLUSTRATIVE [I-calc] AND IS NOT ADIC DATA, except the public inputs:
  * Cboe daily index files SPX, VIX, VIX3M, VIX6M, VIX1Y, SKEW (last observation 2026-10-16),
    https://cdn.cboe.com/api/global/us_indices/daily_prices/<NAME>_History.csv
  * Fama-French 1-month T-bill (RF) monthly series, CRSP 202608 release.

Sections
  A  VIX-anchored option pricer. ATM vol = c_ATM x VIX_tau (C3 default c_ATM = 0.90); implied vol linear in
     strike, slope b calibrated so that the replicated variance-swap strike equals VIX_tau^2 (the Cboe VIX
     identity). 90/72%-of-forward put spreads on a 3/6/12-month ladder weighted 25/50/25 (C3 5.3e).
  B  Premium budget -> ladder notional -> S1 payoff -> VIX-equivalent vega -> L1/L2 capacity -> tail IM.
  C  Recomputed groups-synthesis 2.2 overlay row on the unmodified stream-G7 market paths.
  D  Transfer-pricing ledger for overlay services and the gate-V2 zero-sum test (plus the naive double count).
  E  Tail-book DVA: ex-post convention vs ex-ante kernel credit with an IC policy line.
  F  Empirical ladder replay, monthly purchases 2009-10 .. 2025-09 (SPX payoffs exact; premiums model-priced).

Run (project venv, isolated mode):
  python -I gap03g_overlay_calcs.py <cboe_dir_spx_vix_vix3m_skew> <cboe_dir_vix6m_vix1y> <ff_factors_csv> <out_json>
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
from datetime import date

import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import brentq
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
NAV = 177.0  # USD bn, client working figure [A]

# ------------------------------------------------------------------------------------------------ inputs
CBOE1, CBOE2, FF_CSV, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]


def load_close(path: str, col: str | None = None) -> pd.Series:
    df = pd.read_csv(path)
    df["DATE"] = pd.to_datetime(df["DATE"], format="%m/%d/%Y")
    c = col if col else ("CLOSE" if "CLOSE" in df.columns else df.columns[1])
    return df.set_index("DATE")[c].astype(float).sort_index()


SPX = load_close(os.path.join(CBOE1, "SPX_History.csv"), "SPX")
VIX = load_close(os.path.join(CBOE1, "VIX_History.csv"))
VIX3M = load_close(os.path.join(CBOE1, "VIX3M_History.csv"))
SKEW = load_close(os.path.join(CBOE1, "SKEW_History.csv"), "SKEW")
VIX6M = load_close(os.path.join(CBOE2, "VIX6M_History.csv"))
VIX1Y = load_close(os.path.join(CBOE2, "VIX1Y_History.csv"))


def load_ff_rf(path: str) -> pd.Series:
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 5 and len(parts[0]) == 6 and parts[0].isdigit():
                rows.append((pd.Timestamp(int(parts[0][:4]), int(parts[0][4:]), 1), float(parts[4])))
    s = pd.Series(dict(rows)).sort_index()
    return np.log1p(s / 100.0) * 12.0  # continuous annual rate


RF = load_ff_rf(FF_CSV)

C_ATM = 0.90          # C3 5.3(c) default, to be calibrated
Q_DIV = 0.015         # dividend yield assumption [I]; forward-moneyness strikes make prices insensitive to it
K1F, K2F = 0.90, 0.72  # put-spread strikes, % of forward (C3 5.3e)
LADDER = ((3, 0.25), (6, 0.50), (12, 0.25))  # (months, weight)
SOFR = 0.0389          # 15 Oct 2026 (NY Fed via synthesis 7.1)

# ------------------------------------------------------------------------------------------------ A. pricer
XG = np.geomspace(0.02, 4.0, 2401)


def put_u(F, K, s, T):
    sq = np.maximum(s * np.sqrt(T), 1e-12)
    d1 = (np.log(F / K) + 0.5 * sq ** 2) / sq
    return K * norm.cdf(-(d1 - sq)) - F * norm.cdf(-d1)


def smile(x, s_atm, b, floor=0.4):
    return np.maximum(s_atm - b * (x - 1.0), floor * s_atm)


def kvar(s_atm, b, T):
    v = smile(XG, s_atm, b)
    p = put_u(1.0, XG, v, T)
    c = p + 1.0 - XG
    q = np.where(XG < 1.0, p, c)
    return 2.0 / T * np.trapezoid(q / XG ** 2, XG)


def calib_b(s_atm, T, c=C_ATM):
    target = s_atm / c
    f = lambda b: math.sqrt(max(kvar(s_atm, b, T), 0.0)) - target  # noqa: E731
    if f(0.0) >= 0:
        return 0.0
    hi = 1.0
    while f(hi) < 0 and hi < 64:
        hi *= 2.0
    return brentq(f, 0.0, hi, xtol=1e-7)


# b depends (weakly) on the ATM level through the vol floor; tabulate b(T, s_atm) once and interpolate.
T_GRID = np.array([7, 14, 30, 45, 61, 91, 122, 152, 182, 243, 304, 365, 400]) / 365.0
S_GRID = np.array([0.06, 0.10, 0.14, 0.18, 0.22, 0.28, 0.36, 0.48, 0.64, 0.85])
B_TAB = np.array([[calib_b(s, t) for s in S_GRID] for t in T_GRID])
B_INTERP = RegularGridInterpolator((np.log(T_GRID), S_GRID), B_TAB, bounds_error=False, fill_value=None)


def b_of(T, s_atm):
    t = np.clip(T, T_GRID[0], T_GRID[-1])
    s = np.clip(s_atm, S_GRID[0], S_GRID[-1])
    return float(B_INTERP([[math.log(t), s]])[0])


def atm_vol(T_days, v30, v91, v182, v365, c=C_ATM):
    """ATM vol from the VIX term structure, linear in total variance between tenor nodes."""
    nodes = np.array([30.0, 91.0, 182.0, 365.0])
    vals = np.array([v30, v91, v182, v365]) / 100.0
    w = vals ** 2 * nodes / 365.0
    td = max(float(T_days), 1.0)
    if td <= 30.0:
        return c * vals[0]
    wi = np.interp(td, nodes, w, right=None) if td <= 365.0 else w[-1] * td / 365.0
    return c * math.sqrt(wi / (td / 365.0))


def spread_px(S, K1, K2, T, r, s_atm, b):
    """Discounted 90/72 put-spread value per index unit (Black-76 on the forward, sticky-moneyness smile)."""
    if T <= 1e-6:
        return max(K1 - S, 0.0) - max(K2 - S, 0.0)
    F = S * math.exp((r - Q_DIV) * T)
    v1, v2 = smile(K1 / F, s_atm, b), smile(K2 / F, s_atm, b)
    return math.exp(-r * T) * (float(put_u(F, K1, v1, T)) - float(put_u(F, K2, v2, T)))


# validation of the closed-form intuition 1 + 3 T b^2 = 1/c^2 (Demeterfi-Derman-Kamal-Zou linear-skew result)
val_rows = []
for T in (0.25, 0.5, 1.0):
    b_num = calib_b(0.19, T)
    val_rows.append({"T": T, "b_numeric": round(b_num, 4),
                     "b_closed_form": round(math.sqrt((1 / C_ATM ** 2 - 1) / (3 * T)), 4)})

# ---- today's ladder (16 Oct 2026)
d0 = pd.Timestamp("2026-10-16")
S0 = float(SPX.loc[d0])
mkt0 = {"SPX": S0, "VIX": float(VIX.loc[d0]), "VIX3M": float(VIX3M.loc[d0]), "VIX6M": float(VIX6M.loc[d0]),
        "VIX1Y": float(VIX1Y.loc[d0]), "SKEW": float(SKEW.loc[d0]),
        "SKEW_mean_1990_2026": float(SKEW.loc[:d0].mean()), "SKEW_max": float(SKEW.loc[:d0].max()),
        "SKEW_max_date": str(SKEW.loc[:d0].idxmax().date())}
BETA_ALL = {3: 0.6388, 6: 0.4539, 12: 0.3013}   # gap_03 A_term_structure_betas, all days
BETA_UP3 = {3: 0.6383, 6: 0.4243, 12: 0.2649}   # days with VIX up >= 3 points


def ladder_today(c=C_ATM):
    out = {}
    for m, w in LADDER:
        T = m / 12.0
        s_atm = atm_vol(m * 365 / 12, mkt0["VIX"], mkt0["VIX3M"], mkt0["VIX6M"], mkt0["VIX1Y"], c)
        b = calib_b(s_atm, T, c)
        F = S0 * math.exp((SOFR - Q_DIV) * T)
        K1, K2 = K1F * F, K2F * F
        px = spread_px(S0, K1, K2, T, SOFR, s_atm, b) / S0
        vega = (spread_px(S0, K1, K2, T, SOFR, s_atm + 0.005, b) - spread_px(S0, K1, K2, T, SOFR, s_atm - 0.005, b)) / S0
        dl = (spread_px(S0 * 1.005, K1, K2, T, SOFR, s_atm, b) - spread_px(S0 * 0.995, K1, K2, T, SOFR, s_atm, b)) / (0.01 * S0)
        out[m] = {"weight": w, "atm_vol": s_atm, "b": b, "vol_90": float(smile(K1F, s_atm, b)),
                  "vol_72": float(smile(K2F, s_atm, b)), "premium_per_notional": px,
                  "vega_per_volpt_per_notional": vega, "delta_per_notional": dl}
    return out


LAD = ladder_today()
LAD_LO = ladder_today(0.95)   # flatter skew sensitivity
LAD_HI = ladder_today(0.85)   # steeper skew sensitivity


def ladder_cost(lad):
    """Annual premium per $ of outstanding notional for monthly purchases split 25/50/25 by tenor."""
    k = sum(lad[m]["weight"] * m / (12.0 * lad[m]["premium_per_notional"]) for m, _ in LADDER)
    return 1.0 / k


c_N = ladder_cost(LAD)
c_N_lo, c_N_hi = ladder_cost(LAD_LO), ladder_cost(LAD_HI)

# ------------------------------------------------------------------------------------------------ B. sizing
_G7 = os.path.normpath(os.path.join(HERE, "..", "G7_calcs", "g7_liquidity_ladder_calcs.py"))
_spec = importlib.util.spec_from_file_location("g7mod", _G7)
g7 = importlib.util.module_from_spec(_spec)
sys.modules["g7mod"] = g7
_spec.loader.exec_module(g7)  # unmodified; main() not executed

p_s1 = g7.build_paths("S1_demand_bust_24m", 36)
eq_idx_path = np.cumprod(1 + p_s1["eq"])
mon_months = p_s1["hedge_months"]  # [1, 5] -> 2nd and 6th month


def payoff_per_notional(k2f=K2F):
    width = K1F - k2f
    return sum(0.5 * min(width, max(0.0, K1F - eq_idx_path[t])) for t in mon_months)


PAY_9072 = payoff_per_notional()
PAY_9070 = payoff_per_notional(0.70)
L1_SHARE, L2_SHARE = 0.25, 0.25  # opportunistic short-vega and stress-loss capacity as share of tail (gap_03 L1, L2)
SIMM_VEGA_RATIO = 0.29 * 0.56 * 15.0 * math.sqrt(365 / 14) / norm.ppf(0.99)  # VRW*HVR*sigma_kj (gap_03 7.2)
SIMM_DELTA_RW = 0.15  # equity index delta RW 15 applied to the 1% sensitivity


def size_budget(bud_pct, lad=LAD, cn=None):
    B = bud_pct / 100.0 * NAV
    cn = cn if cn is not None else ladder_cost(lad)
    by_m = {m: lad[m]["weight"] * (B / 12.0) * m / lad[m]["premium_per_notional"] for m, _ in LADDER}
    N = sum(by_m.values())
    vega = sum(by_m[m] * lad[m]["vega_per_volpt_per_notional"] for m in by_m)            # $bn per vol pt
    nv_all = sum(by_m[m] * lad[m]["vega_per_volpt_per_notional"] * BETA_ALL[m] for m in by_m)
    nv_up = sum(by_m[m] * lad[m]["vega_per_volpt_per_notional"] * BETA_UP3[m] for m in by_m)
    delta = sum(by_m[m] * lad[m]["delta_per_notional"] for m in by_m)                     # $bn delta
    pay = N * PAY_9072
    im_otc = SIMM_VEGA_RATIO * abs(vega) + SIMM_DELTA_RW * abs(delta)
    return {"budget_pct_nav": bud_pct, "premium_bn_yr": B, "notional_bn": N, "notional_by_tenor_bn": by_m,
            "cost_per_notional_yr": B / N, "s1_payoff_bn": pay, "payoff_multiple_of_annual_premium": pay / B,
            "vega_bn_per_volpt": vega, "vix_equiv_vega_bn_per_vixpt_alldays": nv_all,
            "vix_equiv_vega_bn_per_vixpt_spikes": nv_up, "dollar_delta_bn": delta,
            "L1_opp_short_vix_vega_cap_bn_per_vixpt": L1_SHARE * nv_up,
            "L2_opp_named_stress_loss_cap_bn": L2_SHARE * pay,
            "tail_IM_if_OTC_under_UMR_bn": im_otc, "tail_IM_if_listed_bn": 0.0}


BUDGETS = (0.15, 0.25, 0.40, 0.50)
SIZING = {f"{b:.2f}%": size_budget(b) for b in BUDGETS}
SIZING_RANGE = {f"{b:.2f}%": {"notional_flat_skew_cATM0.95": size_budget(b, LAD_LO)["notional_bn"],
                               "notional_steep_skew_cATM0.85": size_budget(b, LAD_HI)["notional_bn"]}
                for b in BUDGETS}
# implied budget of G7's $20bn ladder at this cost, and the notional G9's $25bn stack would need
G7_EQUIV_BUDGET_PCT = 100 * 20.0 * c_N / NAV

# opportunistic IM vs vol budget: 10-day 99% (SIMM horizon) on annual P&L vol, fragmentation k in [1, 1.5]
IM_PER_VOL = norm.ppf(0.99) * math.sqrt(10 / 252)
OPP = {f"vol_{v:.2f}%": {"vol_bn": v / 100 * NAV, "IM_k1.0_bn": IM_PER_VOL * v / 100 * NAV,
                         "IM_k1.5_bn": 1.5 * IM_PER_VOL * v / 100 * NAV,
                         "DD_stop_2x_bn": 2 * v / 100 * NAV} for v in (1.0, 1.25, 1.5)}

# ------------------------------------------------------------------------------------------------ C. cash map
with open(os.path.normpath(os.path.join(HERE, "..", "GS_calcs", "gs_group_cashmap_results.json")), encoding="utf-8") as fh:
    GS = json.load(fh)


def overlay_row(scn, syn, tail_N, tail_prem, k2f, opp_rule, opp_im_step):
    if scn in ("normal", "drought"):
        p = g7.build_paths("B0_drought", 36)
        regime = ["normal" if scn == "normal" else "drought"] * 36
    else:
        p = g7.build_paths("S1_demand_bust_24m", 36)
        regime = p["regime"]
    eq_idx, im = 1.0, g7.IM_RATE_N * syn
    acc = dict(vm=0.0, d_im=0.0, prem=0.0, mon=0.0, opp=0.0, opp_im=0.0)
    width = K1F - k2f
    tail_pay_total = 0.0
    for t in range(12):
        stress = regime[t] == "crisis"
        vm = syn * eq_idx * p["eq"][t]
        eq_idx *= 1 + p["eq"][t]
        im_new = (g7.IM_RATE_S if (stress and t < 12) else g7.IM_RATE_N) * syn * eq_idx
        acc["d_im"] += im_new - im
        im = im_new
        acc["vm"] += vm
        acc["prem"] -= tail_prem / 12.0
        if t in p["hedge_months"]:
            pay = 0.5 * tail_N * min(width, max(0.0, K1F - eq_idx))
            acc["mon"] += pay
            tail_pay_total += pay
    if scn in ("S1", "T4"):
        if opp_rule == "old":
            acc["opp"] = -0.015 * NAV
        else:  # L2-compliant named-stress loss: <= 25% of the tail's stressed P&L, never above the old 1.5%
            acc["opp"] = -min(0.015 * NAV, L2_SHARE * tail_pay_total)
        acc["opp_im"] = -opp_im_step
    services = acc["vm"] - acc["d_im"]
    own = acc["prem"] + acc["mon"] + acc["opp"] + acc["opp_im"]
    return {k: round(v, 3) for k, v in acc.items()} | {"services_synthetic_beta": round(services, 3),
                                                       "own_books_tail_opp": round(own, 3),
                                                       "net": round(services + own, 3)}


SCNS = ("normal", "drought", "S1", "T4")
GS_KEY = {"normal": "census|normal", "drought": "census|drought", "S1": "census|S1", "T4": "census|T14"}
CFG = {
    "old_2.2": dict(syn=15.0, tail_N=20.0, tail_prem=0.004 * NAV, k2f=0.70, opp_rule="old", opp_im_step=0.0),
    "recon_floor_0.15": dict(syn=10.0, tail_N=SIZING["0.15%"]["notional_bn"], tail_prem=0.0015 * NAV, k2f=K2F,
                             opp_rule="L2", opp_im_step=0.5),
    "recon_mid_0.25": dict(syn=10.0, tail_N=SIZING["0.25%"]["notional_bn"], tail_prem=0.0025 * NAV, k2f=K2F,
                           opp_rule="L2", opp_im_step=0.5),
    "recon_cap_0.50": dict(syn=10.0, tail_N=SIZING["0.50%"]["notional_bn"], tail_prem=0.0050 * NAV, k2f=K2F,
                           opp_rule="L2", opp_im_step=0.5),
}
CASHMAP = {}
for name, cfg in CFG.items():
    CASHMAP[name] = {}
    for scn in SCNS:
        row = overlay_row(scn, **cfg)
        priv = GS["runs"][GS_KEY[scn]]["private_net"]
        opex = GS["runs"][GS_KEY[scn]]["cf_opex"]
        before = priv + row["net"] - opex
        row["private_net_census"] = round(priv, 3)
        row["before_payout"] = round(before, 3)
        row["liquid_funding_5_7.5_10"] = [round(d * NAV - before, 2) for d in (0.05, 0.075, 0.10)]
        CASHMAP[name][scn] = row

# P2S Red-stage lever memo on the S1 path: $5bn executed at t0 of the stress (client: Public Markets)
def p2s_memo(n=5.0):
    p = g7.build_paths("S1_demand_bust_24m", 36)
    eq_idx, im0 = 1.0, g7.IM_RATE_N * n
    vm = 0.0
    for t in range(12):
        vm += n * eq_idx * p["eq"][t]
        eq_idx *= 1 + p["eq"][t]
    im12 = (g7.IM_RATE_S if p["regime"][11] == "crisis" else g7.IM_RATE_N) * n * eq_idx
    return {"cash_from_physical_sale": n, "IM_at_execution": -im0, "VM_12m": round(vm, 3),
            "IM_change_to_month12": round(-(im12 - im0), 3),
            "net_12m_cash": round(n - im0 + vm - (im12 - im0), 3),
            "note": "booked to Public Markets as client: physical sale proceeds and contingent VM/IM; "
                    "excluded from the Overlay row"}


P2S = p2s_memo()

# ------------------------------------------------------------------------------------------------ D. ledger + V2
rng = np.random.default_rng(20261018)
C_BUF = 0.015          # groups 4.3 contingent-liquidity charge rate (range 1-3%)
L_FTP = 0.005          # illustrative term liquidity premium credited on cash released [I]
SERVICES = [  # id, client, signed notional ($bn), funded?, liquidity credit on release?
    ("TPA_completion", "TPA", 10.0, True, False),
    ("P2S_public_markets", "PUB", 5.0, True, True),
    ("PE_beta_rebuild", "TPA", 1.0, True, False),
    ("COI_beta_hedge", "COI", -1.0, False, False),
]
STRESS_OUT_PER_N = 0.117 + (0.10 - 0.04)  # VM P99 30d (G7) + IM step 4% -> 10%


def ledger(eq_path, rf_m=SOFR / 12, s_lock=0.0050, basis_sd=0.0004, cdx=True):
    """Monthly double-entry books for overlay services. Returns per-entity totals, external total, max errors."""
    T = len(eq_path)
    ent = {}
    ext_total, max_int, max_id = 0.0, 0.0, 0.0
    naive_err = 0.0

    def book(e, x):
        ent[e] = ent.get(e, 0.0) + x

    for t in range(T):
        r_b = eq_path[t]
        internal_sum, ent_sum, ext_t = 0.0, 0.0, 0.0
        for sid, cl, n, funded, lpc_on in SERVICES:
            b_t = s_lock / 12 + rng.normal(0.0, basis_sd)           # realized financing spread (monthly)
            tc = abs(n) * 0.00005 if t % 3 == 0 else 0.0               # roll/execution cost every quarter
            vm = n * (r_b - rf_m - b_t)                                 # futures P&L (external)
            coll = rf_m * n if funded else 0.0                          # CF interest on the cash backing (external)
            ext = vm - tc + coll
            # internal transfers (each appears twice with opposite signs)
            tr = [("OVL", -n * r_b), (cl, +n * r_b),                    # exposure pass-through
                  (cl, -n * (rf_m + s_lock / 12)), ("OVL", +n * (rf_m + s_lock / 12))]  # locked financing
            if funded:
                tr += [("CF", -rf_m * n), (cl, +rf_m * n)]              # deposit interest on cash moved to CF
            clc = C_BUF / 12 * abs(n) * STRESS_OUT_PER_N               # contingent VM/IM liquidity charge
            tr += [(cl, -clc), ("CF", +clc)]
            if lpc_on:
                lpc = L_FTP / 12 * n * (1 - 0.04 - 0.117)              # credit on cash released (1-m-b)
                tr += [(cl, +lpc), ("CF", -lpc)]
            exts = [("OVL", vm - tc), ("CF", coll)]
            for e, x in tr + exts:
                book(e, x)
            internal_sum += sum(x for _, x in tr)
            ent_sum += sum(x for _, x in tr + exts)
            ext_t += ext
            # naive convention (2.2 row + 'as if physical' client benchmark, no pass-through or financing legs)
            naive = (n * r_b) + (vm - tc) + coll
            naive_err += naive - ext
        if cdx:  # Private Credit buys CDX HY protection on $1bn: reference index P&L vs on-the-run implementation
            n, dur, s_run = 1.0, 4.5, 0.035
            ds_ref = -0.25 * r_b                                         # spread change vs equity move [I]
            ref = -n * dur * ds_ref - n * s_run / 12
            act = ref + rng.normal(0.0, 0.0003) - (0.0002 if t % 6 == 0 else 0.0)  # roll basis + cost
            tr = [("OVL", -ref), ("PCR", +ref)]
            clc = C_BUF / 12 * n * 0.05
            tr += [("PCR", -clc), ("CF", +clc)]
            for e, x in tr + [("OVL", act)]:
                book(e, x)
            internal_sum += sum(x for _, x in tr)
            ent_sum += sum(x for _, x in tr) + act
            ext_t += act
        ext_total += ext_t
        max_int = max(max_int, abs(internal_sum))
        max_id = max(max_id, abs(ent_sum - ext_t))
    return ent, ext_total, max_int, max_id, naive_err


eq_benign = np.array(g7.build_paths("B0_drought", 36)["eq"][:12])
eq_s1 = np.array(p_s1["eq"][:12])
LED = {}
for nm, path in (("benign_B0", eq_benign), ("S1", eq_s1)):
    e, x, mi, md, ne = ledger(path)
    LED[nm] = {"entity_pnl_bn": {k: round(v, 4) for k, v in e.items()}, "external_bn": round(x, 4),
               "sum_entities_bn": round(sum(e.values()), 4), "max_abs_internal_sum": mi,
               "max_abs_identity_error": md, "naive_convention_double_count_bn": round(ne, 3)}
mc_int, mc_id = 0.0, 0.0
for _ in range(2000):
    path = rng.standard_t(5, 12) * 0.045 / math.sqrt(5 / 3) + 0.006
    _, _, mi, md, _ = ledger(path)
    mc_int, mc_id = max(mc_int, mi), max(mc_id, md)
LED["monte_carlo_2000_paths"] = {"max_abs_internal_sum": mc_int, "max_abs_identity_error": mc_id}

# ------------------------------------------------------------------------------------------------ F. replay
def build_replay(c=C_ATM, monetize=True, ba=0.02, trig_mult=3.0, vix_trig=35.0):
    days = SPX.index
    common = days[(days >= pd.Timestamp("2009-10-01")) & (days <= pd.Timestamp("2026-10-16"))]
    vix_f = {k: s.reindex(common).ffill() for k, s in (("v30", VIX), ("v91", VIX3M), ("v182", VIX6M), ("v365", VIX1Y))}
    spx = SPX.reindex(common).ffill()
    starts = []
    for y in range(2009, 2026):
        for mth in range(1, 13):
            if (y == 2009 and mth < 10) or (y == 2025 and mth > 9):
                continue
            dd = common[common >= pd.Timestamp(y, mth, 1)]
            starts.append(dd[0])
    cash = {}
    rungs = []
    for d in starts:
        r = float(RF.asof(pd.Timestamp(d.year, d.month, 1))) if not np.isnan(RF.asof(pd.Timestamp(d.year, d.month, 1))) else SOFR
        S0d = float(spx.loc[d])
        for m, w in LADDER:
            exp_target = (d + pd.DateOffset(months=m))
            later = common[common >= exp_target]
            if len(later) == 0:
                continue
            e = later[0]
            T = (e - d).days / 365.0
            s_atm = atm_vol((e - d).days, *(float(vix_f[k].loc[d]) for k in ("v30", "v91", "v182", "v365")), c=c)
            b = b_of(T, s_atm)
            F = S0d * math.exp((r - Q_DIV) * T)
            K1, K2 = K1F * F, K2F * F
            px = spread_px(S0d, K1, K2, T, r, s_atm, b)
            prem = w / 12.0                       # $ of a $1/yr budget spent on this rung
            units = prem / px
            cash[d.year] = cash.get(d.year, 0.0) - prem
            proceeds, when = 0.0, e
            window = common[(common > d) & (common <= e)]
            for dt in window:
                Trem = (e - dt).days / 365.0
                St = float(spx.loc[dt])
                if dt == e:
                    val = units * (max(K1 - St, 0.0) - max(K2 - St, 0.0))
                    proceeds, when = val, dt
                    break
                if not monetize:
                    continue
                s_t = atm_vol((e - dt).days, *(float(vix_f[k].loc[dt]) for k in ("v30", "v91", "v182", "v365")), c=c)
                val = units * spread_px(St, K1, K2, Trem, r, s_t, b_of(Trem, s_t))
                if val >= trig_mult * prem or (float(vix_f["v30"].loc[dt]) >= vix_trig and val > prem):
                    proceeds, when = val * (1 - ba), dt
                    break
            cash[when.year] = cash.get(when.year, 0.0) + proceeds
            rungs.append({"buy": str(d.date()), "tenor_m": m, "premium": prem, "proceeds": proceeds,
                          "exit": str(when.date())})
    return cash, rungs


def replay_stats(cash, rungs):
    years = list(range(2010, 2026))
    net = {y: round(cash.get(y, 0.0), 4) for y in years}   # per $1/yr budget; -1.0 = premium with no payoff
    neg = [y for y in years if net[y] < 0]
    run, best = 0, 0
    for y in years:
        run = run + 1 if net[y] < 0 else 0
        best = max(best, run)
    tot_prem = sum(r["premium"] for r in rungs)
    tot_proc = sum(r["proceeds"] for r in rungs)
    by_year_proc = {}
    for r_ in rungs:
        yy = int(r_["exit"][:4])
        by_year_proc[yy] = by_year_proc.get(yy, 0.0) + r_["proceeds"]
    top = sorted(by_year_proc.items(), key=lambda kv: -kv[1])[:3]
    hit = sum(1 for r_ in rungs if r_["proceeds"] > 0) / len(rungs)
    cum, peak, mdd = 0.0, 0.0, 0.0
    for y in years:
        cum += net[y]
        peak = max(peak, cum)
        mdd = min(mdd, cum - peak)
    return {"net_by_year_per_1usd_budget": net, "years_negative": len(neg), "years": len(years),
            "longest_negative_run_years": best, "realized_payoff_to_premium": round(tot_proc / tot_prem, 3),
            "share_of_rungs_paying": round(hit, 3),
            "top3_payoff_years": [(y, round(v / tot_proc, 3)) for y, v in top],
            "max_cumulative_drawdown_years_of_budget": round(mdd, 3), "rungs": len(rungs)}


REPLAY = {}
for nm, kw in (("monetize_cATM0.90", dict(c=0.90, monetize=True)),
               ("expiry_only_cATM0.90", dict(c=0.90, monetize=False)),
               ("monetize_cATM0.85", dict(c=0.85, monetize=True)),
               ("monetize_cATM0.95", dict(c=0.95, monetize=True)),
               ("monetize_5x_vix45_cATM0.90", dict(c=0.90, monetize=True, trig_mult=5.0, vix_trig=45.0))):
    cash, rungs = build_replay(**kw)
    REPLAY[nm] = replay_stats(cash, rungs)

# ------------------------------------------------------------------------------------------------ E. DVA
P_FLOOR = 0.0015 * NAV
CARRY = -0.45                     # stream 09 / G8 E1 convention: E^P[X]/(1+r) = 0.55 P
E1_CREDIT = 0.0895                # G8 E1: 895bp per $ of premium at duals 1.83% (crisis row) and 0.81% (CVaR)
pay_mult = SIZING["0.15%"]["payoff_multiple_of_annual_premium"]
CBUF_CREDIT = C_BUF * pay_mult    # parity with Private Credit / Capital Solutions: c_buf x stressed inflow
rep = REPLAY["monetize_cATM0.90"]
DVA = {
    "premium_floor_bn": P_FLOOR,
    "old_convention_calm_year_desk_dva_bn": -P_FLOOR,
    "old_convention_s1_year_desk_dva_bn": SIZING["0.15%"]["s1_payoff_bn"] - P_FLOOR,
    "ex_ante_value_per_usd_premium": {"KV": 1 + CARRY, "LV_EV_E1_duals": E1_CREDIT,
                                      "LV_cbuf_parity": round(CBUF_CREDIT, 4)},
    "policy_residual_per_usd_premium_E1": round(1 + CARRY + E1_CREDIT - 1, 4),
    "policy_residual_bn_yr_floor": round((CARRY + E1_CREDIT) * P_FLOOR, 4),
    "policy_residual_bn_yr_cap": round((CARRY + E1_CREDIT) * 0.005 * NAV, 4),
    "unmodelled_EV_needed_to_break_even_bn_yr_floor": round(-(CARRY + E1_CREDIT) * P_FLOOR, 4),
    "replay_years_negative": rep["years_negative"], "replay_longest_negative_run": rep["longest_negative_run_years"],
    "old_convention_5yr_calm_stretch_bn_floor": -5 * P_FLOOR,
    "old_convention_5yr_calm_stretch_bn_cap": -5 * 0.005 * NAV,
}

# ------------------------------------------------------------------------------------------------ output
res = {
    "note": "SYNTHETIC / ILLUSTRATIVE [I-calc]; not ADIC data. Public inputs: Cboe index files to 2026-10-16; "
            "Fama-French RF (CRSP 202608).",
    "A_market_2026_10_16": mkt0,
    "A_pricer": {"c_ATM": C_ATM, "q_div": Q_DIV, "r": SOFR, "strikes_pct_fwd": [K1F, K2F],
                 "skew_slope_validation": val_rows,
                 "ladder_today": {str(m): {k: (round(v, 5) if isinstance(v, float) else v) for k, v in d.items()}
                                  for m, d in LAD.items()},
                 "cost_per_notional_yr": {"cATM0.90": round(c_N, 5), "cATM0.95": round(c_N_lo, 5),
                                          "cATM0.85": round(c_N_hi, 5), "G7_assumption": round(0.004 * NAV / 20.0, 5)}},
    "B_sizing": {k: {kk: (round(vv, 4) if isinstance(vv, float) else
                          ({str(a): round(b_, 3) for a, b_ in vv.items()} if isinstance(vv, dict) else vv))
                     for kk, vv in v.items()} for k, v in SIZING.items()},
    "B_sizing_notional_range": {k: {kk: round(vv, 2) for kk, vv in v.items()} for k, v in SIZING_RANGE.items()},
    "B_G7_ladder_equivalent_budget_pct_nav": round(G7_EQUIV_BUDGET_PCT, 3),
    "B_s1_payoff_per_notional": {"90/72": round(PAY_9072, 4), "90/70": round(PAY_9070, 4)},
    "B_simm_vega_ratio": round(SIMM_VEGA_RATIO, 3),
    "B_opportunistic_IM": {k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in OPP.items()},
    "C_cashmap_overlay_row": CASHMAP,
    "C_p2s_red_lever_memo_S1": P2S,
    "D_ledger_v2": LED,
    "E_dva": DVA,
    "F_replay": REPLAY,
}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1, default=float)

# console summary
print("market", json.dumps(mkt0))
print("ladder today", {m: (round(d["premium_per_notional"], 4), round(d["vol_90"], 3), round(d["vol_72"], 3))
                       for m, d in LAD.items()})
print("c_N", round(c_N, 4), "range", round(c_N_lo, 4), round(c_N_hi, 4), "G7", round(0.004 * NAV / 20, 4))
for k, v in SIZING.items():
    print("sizing", k, {kk: (round(vv, 3) if isinstance(vv, float) else None) for kk, vv in v.items()
                        if not isinstance(vv, dict)})
print("G7 $20bn ladder equivalent budget % NAV", round(G7_EQUIV_BUDGET_PCT, 3))
for k, v in CASHMAP.items():
    print("cashmap", k, {s: (v[s]["net"], v[s]["services_synthetic_beta"], v[s]["own_books_tail_opp"],
                             v[s]["before_payout"]) for s in SCNS})
print("p2s", P2S)
print("ledger", json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "entity_pnl_bn"} for k, v in LED.items()}))
print("dva", json.dumps(DVA))
for k, v in REPLAY.items():
    print("replay", k, {kk: vv for kk, vv in v.items() if kk != "net_by_year_per_1usd_budget"})
    print("   net by year", v["net_by_year_per_1usd_budget"])
print("validation", val_rows)
