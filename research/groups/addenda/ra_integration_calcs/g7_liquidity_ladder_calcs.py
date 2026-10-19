"""
G7 - Total-portfolio liquidity ladder: illustrative calculations for the ADIC TPA lab.

EVERYTHING PRODUCED HERE IS SYNTHETIC / ILLUSTRATIVE [I]. Balances are the working synthetic
allocation in inputs/00_CONTEXT_AND_PRIOR_WORK.md section 1A, split further by G7 assumptions.
They are NOT ADIC data and must be labelled synthetic wherever shown.

Sourced anchors used as parameter defaults (see dossier G7_liquidity_ladder.md, sections 4 and 6):
  * Hedge-fund investor liquidity buckets <=7d / 8-90d / >90d = 8.4% / 27.3% / 64.4% of NAV
    (OFR Hedge Fund Monitor, SEC Form PF, qualifying hedge funds, 2026-06-30).
  * PE contribution rate ~28-31%/yr of unfunded; distribution rate 9-11% (drought) vs ~20-27% normal
    (MSCI Private Capital Benchmarks Summary Q2-2026).
  * Secondary pricing: buyout ~90-91% of NAV (H1-2026); H2-2008 average high bid 61% (Cogent, via dossier 05).
  * Basel LCR haircuts: Level 2A 15%, Level 2B equities/corporates 50% (LCR30.43-30.45); inflow cap 75%.
  * Credit-line draw spike: US C&I loans +$482bn between 11 Mar and 1 Apr 2020 (Li, Strahan & Zhang 2020).
  * SPX 21-day p1 move -11.7% (stream 09, Cboe data).

Run (isolated mode):  python -I g7_liquidity_ladder_calcs.py
Writes g7_liquidity_ladder_results.json next to this script. Fixed seeds.
"""
from __future__ import annotations

import json
import os

import numpy as np
from scipy.stats import beta as beta_dist

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "g7_liquidity_ladder_results.json")

NAV0 = 177.0  # USD bn (client brief)

# --------------------------------------------------------------------------------------------
# 1. Synthetic balance sheet (USD bn). Group tags follow the seven-group organisation + Treasury.
# --------------------------------------------------------------------------------------------
HF_TOTAL = 20.0
_HF_RAW = {"hf_le7d": 0.084, "hf_8_90d": 0.273, "hf_91_365d": 0.644 * 2 / 3, "hf_gt365d": 0.644 / 3}
HF_SHARES = {k: v / sum(_HF_RAW.values()) for k, v in _HF_RAW.items()}  # OFR shares sum to 100.1% (rounding)

BAL0 = {
    "cash": 6.0, "ust": 4.0, "ig": 5.0,                      # Treasury (central)
    "lo_dm": 22.0, "lo_em": 6.0, "lo_fi": 8.0,               # Public Markets: long-only
    **{k: HF_TOTAL * v for k, v in HF_SHARES.items()},       # Public Markets: hedge funds
    "pc": 14.0, "cs": 8.0, "sec": 14.0, "pe": 52.0, "co": 18.0,  # private groups
}
GROUP = {
    "cash": "Treasury", "ust": "Treasury", "ig": "Treasury",
    "lo_dm": "PublicMkts-LO", "lo_em": "PublicMkts-LO", "lo_fi": "PublicMkts-LO",
    "hf_le7d": "PublicMkts-HF", "hf_8_90d": "PublicMkts-HF", "hf_91_365d": "PublicMkts-HF", "hf_gt365d": "PublicMkts-HF",
    "pc": "PrivateCredit", "cs": "CapitalSolutions", "sec": "Secondaries", "pe": "PE", "co": "CoInvestment",
}
UNF0 = {"pe": 26.0, "sec_def": 1.5, "sec": 2.5, "pc_rev": 1.5, "pc": 2.5, "cs": 3.0, "co": 1.0}  # total 38

SYN_NOTIONAL = 15.0            # long equity-index futures already in place (synthetic beta)
IM_RATE_N, IM_RATE_S = 0.04, 0.10
HEDGE_NOTIONAL = 20.0          # 90/70 put-spread ladder notional (~11% of NAV)
HEDGE_PREMIUM_PA = 0.004 * NAV0  # 0.4% of NAV per year
OPP_IM = 1.0
RCF_COMMITTED = 5.0            # ASSUMPTION; ADIC to supply actual facilities
NEW_COMMIT_PA = 12.0           # ASSUMPTION; commitment pacing USD bn per year

assert abs(sum(BAL0.values()) - NAV0) < 1e-9, sum(BAL0.values())
assert abs(sum(UNF0.values()) - 38.0) < 1e-9

PRIVATE = ["pc", "cs", "sec", "pe", "co"]
LIQ_KEYS = ["cash", "ust", "ig", "lo_dm", "lo_em", "lo_fi"]

LADDER = {  # ttc months; cap = fraction of t0 balance per month; hc = haircut normal/stress; tier
    "cash":       dict(ttc=0, cap=1.00, hc_n=0.000, hc_s=0.000, path="cash", tier="T"),
    "ust":        dict(ttc=0, cap=1.00, hc_n=0.005, hc_s=0.020, path="ust", tier="T"),
    "ig":         dict(ttc=0, cap=0.50, hc_n=0.010, hc_s=0.100, path="ig", tier="T"),
    "lo_dm":      dict(ttc=0, cap=0.50, hc_n=0.002, hc_s=0.015, path="eq", tier="P"),
    "lo_fi":      dict(ttc=0, cap=0.50, hc_n=0.005, hc_s=0.050, path="fi", tier="P"),
    "lo_em":      dict(ttc=1, cap=0.50, hc_n=0.010, hc_s=0.050, path="em", tier="P"),
    "hf_le7d":    dict(ttc=1, cap=0.80, hc_n=0.000, hc_s=0.000, path="hf", tier="P"),
    "hf_8_90d":   dict(ttc=4, cap=0.25, hc_n=0.000, hc_s=0.000, path="hf", tier="P"),
    "hf_91_365d": dict(ttc=12, cap=0.10, hc_n=0.000, hc_s=0.000, path="hf", tier="P"),
    "hf_gt365d":  dict(ttc=24, cap=0.10, hc_n=0.000, hc_s=0.000, path="hf", tier="P"),
    "pc":         dict(ttc=4, cap=0.10, hc_n=0.11, hc_s=0.25, path="priv", tier="A"),
    "cs":         dict(ttc=6, cap=0.08, hc_n=0.10, hc_s=0.30, path="priv", tier="A"),
    "sec":        dict(ttc=6, cap=0.06, hc_n=0.10, hc_s=0.35, path="priv", tier="R"),
    "pe":         dict(ttc=6, cap=0.02, hc_n=0.09, hc_s=0.35, path="priv", tier="R"),
    "co":         dict(ttc=9, cap=0.03, hc_n=0.15, hc_s=0.45, path="priv", tier="R"),
}

DIST = {
    "boom":    {"pe": 0.25, "sec": 0.30, "co": 0.22, "cs": 0.14, "pc": 0.18},
    "normal":  {"pe": 0.20, "sec": 0.25, "co": 0.18, "cs": 0.13, "pc": 0.17},
    "drought": {"pe": 0.11, "sec": 0.18, "co": 0.09, "cs": 0.12, "pc": 0.16},
    "crisis":  {"pe": 0.035, "sec": 0.07, "co": 0.025, "cs": 0.07, "pc": 0.10},
}
CALL = {"boom": 0.39, "normal": 0.29, "drought": 0.28, "crisis": 0.30}


def monthly_rate(annual: float) -> float:
    return 1.0 - (1.0 - annual) ** (1.0 / 12.0)


# --------------------------------------------------------------------------------------------
# 2. Deterministic named stresses (monthly, 36 months) and the counterbalancing-capacity ladder
# --------------------------------------------------------------------------------------------
def build_paths(name: str, T: int = 36) -> dict:
    eq = np.zeros(T); fi = np.zeros(T); ig = np.zeros(T); ust = np.zeros(T); hf = np.zeros(T)
    priv_mark = np.zeros(T)
    regime = ["drought"] * T
    draw_rate = np.full(T, 0.075)
    call_mult = np.ones(T)
    rev_draw = np.zeros(T)
    hedge_months = []
    opp_loss = np.zeros(T)
    if name == "B0_drought":
        eq[:] = 0.0049; fi[:] = 0.0035; ig[:] = 0.0038; ust[:] = 0.0034; hf[:] = 0.004
        priv_mark[2::3] = 0.015
    elif name == "S1_demand_bust_24m":
        eq[:6] = [-0.15, -0.12, -0.08, -0.05, -0.04, -0.03]; eq[12:24] = 0.02; eq[24:] = 0.008
        fi[:3] = -0.02; fi[3:] = 0.005
        ig[:2] = -0.015; ig[2:] = 0.004
        ust[0] = 0.01; ust[1] = 0.005
        hf[:4] = -0.03; hf[12:] = 0.008
        priv_mark[3] = -0.08; priv_mark[6] = -0.08; priv_mark[9] = -0.04; priv_mark[14::3] = 0.01
        regime = ["crisis" if t < 18 else "drought" for t in range(T)]
        draw_rate[:24] = 0.10
        call_mult[:12] = 1.25
        rev_draw[:3] = 0.5 / 3
        hedge_months = [1, 5]
        opp_loss[:3] = 0.015 * NAV0 / 3
    elif name == "S2_owner_draw_cap_36m":
        eq[:3] = -0.053; eq[3:] = 0.004
        fi[:] = 0.003; ig[:] = 0.003; ust[:] = 0.003; hf[:3] = -0.01; hf[3:] = 0.004
        priv_mark[3] = -0.04; priv_mark[8::3] = 0.01
        draw_rate[:] = 0.10
        hedge_months = [2]
    elif name == "S3_rates_collateral_2022":
        eq[:9] = -0.0315; eq[9:] = 0.006
        fi[:9] = -0.014; fi[9:] = 0.004
        ig[:9] = -0.017; ig[9:] = 0.004
        ust[:9] = -0.011; ust[9:] = 0.003
        hf[:9] = -0.005; hf[9:] = 0.004
        priv_mark[3] = -0.03; priv_mark[6] = -0.04; priv_mark[9] = -0.03; priv_mark[12::3] = 0.01
        draw_rate[:] = 0.05      # stream 03 state SS: owner flush, draw at the floor
        call_mult[:12] = 31 / 28
        hedge_months = [8]
    else:
        raise ValueError(name)
    return dict(eq=eq, fi=fi, ig=ig, ust=ust, hf=hf, priv_mark=priv_mark, regime=regime, draw_rate=draw_rate,
                call_mult=call_mult, rev_draw=rev_draw, hedge_months=hedge_months, opp_loss=opp_loss)


def run_named(name: str, T: int = 36, cfp_actions: bool = False, nav_facility_prearranged: bool = False) -> dict:
    p = build_paths(name, T)
    bal = dict(BAL0)
    unf = dict(UNF0)
    eq_idx = 1.0
    im = IM_RATE_N * SYN_NOTIONAL
    rows = []
    for t in range(T):
        reg = p["regime"][t]
        stress = reg == "crisis"
        for k, f in (("lo_dm", p["eq"][t]), ("lo_em", 1.2 * p["eq"][t]), ("lo_fi", p["fi"][t]),
                     ("ig", p["ig"][t]), ("ust", p["ust"][t]), ("cash", 0.039 / 12)):
            bal[k] *= 1 + f
        for k in HF_SHARES:
            bal[k] *= 1 + p["hf"][t]
        for g in PRIVATE:
            bal[g] *= 1 + p["priv_mark"][t]
        vm = SYN_NOTIONAL * eq_idx * p["eq"][t]
        eq_idx *= 1 + p["eq"][t]
        im_new = (IM_RATE_S if (stress and t < 12) else IM_RATE_N) * SYN_NOTIONAL * eq_idx
        d_im = im_new - im
        im = im_new
        hedge_cf = -HEDGE_PREMIUM_PA / 12
        if t in p["hedge_months"]:  # monetise 50% of the 90/70 put-spread ladder at each listed month
            hedge_cf += 0.5 * HEDGE_NOTIONAL * min(0.20, max(0.0, 0.90 - eq_idx))
        opp = -p["opp_loss"][t]
        dist = {g: monthly_rate(DIST[reg][g]) * bal[g] for g in PRIVATE}
        crate = monthly_rate(min(0.95, CALL[reg] * p["call_mult"][t]))
        calls = {k: crate * unf[k] for k in ("pe", "sec", "pc", "cs", "co")}
        calls["sec_def"] = (UNF0["sec_def"] / 4.0) if t in (2, 5, 8, 11) else 0.0
        spike = p["rev_draw"][t] * UNF0["pc_rev"]
        calls["pc_rev"] = min(unf["pc_rev"], spike if spike > 0 else crate * unf["pc_rev"])
        nc = NEW_COMMIT_PA / 12.0
        if cfp_actions and stress and t >= 2:
            nc *= 0.25
        for k, v in calls.items():
            unf[k] -= v
        for k, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1), ("co", 0.1)):
            unf[k] += w * nc
        for g in PRIVATE:
            add = calls[g] + (calls["sec_def"] if g == "sec" else 0.0) + (calls["pc_rev"] if g == "pc" else 0.0)
            bal[g] += add - dist[g]
        draw = p["draw_rate"][t] * NAV0 / 12.0  # no distribution flex in named tests (owner decision; see MC policy D)
        opex = 0.001 * NAV0 / 12.0
        uses = draw + sum(calls.values()) + max(0.0, -vm) + max(0.0, d_im) + max(0.0, -hedge_cf) + max(0.0, -opp) + opex
        inflows = sum(dist.values()) + max(0.0, vm) + max(0.0, -d_im) + max(0.0, hedge_cf) + max(0.0, opp)
        rows.append(dict(t=t + 1, regime=reg, uses=uses, inflows=inflows, net=uses - inflows, draw=draw,
                         calls=sum(calls.values()), dist=sum(dist.values()), vm=vm, d_im=d_im, hedge=hedge_cf, opp=opp,
                         gross_nav=sum(bal.values()), calls_by=dict(calls), dist_by=dict(dist)))
    # Counterbalancing capacity: cumulative proceeds if every bucket were liquidated from t=0 at max pace
    idx = {"cash": np.cumprod(np.full(T, 1 + 0.039 / 12)), "ust": np.cumprod(1 + p["ust"]),
           "ig": np.cumprod(1 + p["ig"]), "eq": np.cumprod(1 + p["eq"]), "fi": np.cumprod(1 + p["fi"]),
           "em": np.cumprod(1 + 1.2 * p["eq"]), "hf": np.cumprod(1 + p["hf"]), "priv": np.cumprod(1 + p["priv_mark"])}
    proceeds = {}
    stressed_scenario = name != "B0_drought"
    for k, prm in LADDER.items():
        mv = BAL0[k] * idx[prm["path"]]
        cum = np.zeros(T); remaining = 1.0; acc = 0.0
        if k == "cash":
            mv = mv - (IM_RATE_N * SYN_NOTIONAL + OPP_IM)  # encumbered margin excluded
        for t in range(T):
            crisis_t = p["regime"][t] == "crisis"
            hc = prm["hc_s"] if stressed_scenario else prm["hc_n"]
            ttc = prm["ttc"] + (2 if (crisis_t and prm["tier"] in ("A", "R")) else 0)
            if t >= ttc and remaining > 1e-12:
                frac = min(prm["cap"], remaining)
                if k.startswith("hf") and crisis_t:
                    frac *= 0.5
                remaining -= frac
                acc += frac * mv[t] * (1 - hc)
            cum[t] = acc
        proceeds[k] = cum
    rcf = np.array([0.0 if t < 1 else RCF_COMMITTED * (0.75 if p["regime"][t] == "crisis" else 1.0) for t in range(T)])
    pe_sec = (BAL0["pe"] + BAL0["sec"]) * idx["priv"]
    lead = 0 if nav_facility_prearranged else 3
    navf = np.array([0.0 if t < lead else (0.05 if p["regime"][t] == "crisis" else 0.10) * pe_sec[t] for t in range(T)])
    net = np.array([r["net"] for r in rows])
    nco = np.cumsum(net)
    tiers = {"T": ["cash", "ust", "ig"]}
    tiers["TP"] = tiers["T"] + ["lo_dm", "lo_fi", "lo_em", "hf_le7d", "hf_8_90d", "hf_91_365d", "hf_gt365d"]
    tiers["TPF"] = tiers["TP"]
    tiers["TPFA"] = tiers["TP"] + ["pc", "cs"]
    tiers["ALL"] = tiers["TPFA"] + ["sec", "pe", "co"]
    cbc = {}
    for tn, keys in tiers.items():
        c = sum(proceeds[k] for k in keys)
        if tn != "T" and tn != "TP":
            c = c + rcf + navf
        cbc[tn] = c
    true_nav = np.array([r["gross_nav"] for r in rows]) - nco
    cbc["TP_floor8"] = cbc["TP"] - 0.08 * true_nav       # treasury floor treated as unusable
    cbc["TPF_floor4"] = cbc["TPF"] - 0.04 * true_nav     # usable buffer down to 4% of NAV

    def surv(c):
        br = np.where(nco > c)[0]
        return int(br[0] + 1) if br.size else None

    sh = {k: surv(v) for k, v in cbc.items()}
    # trajectory of the liquid share if the whole net need is met from the liquid book (no private sales):
    # liquid book (Treasury + LO + all HF) marked to the path, minus cumulative net need
    liq_book = np.zeros(T)
    for t in range(T):
        mvsum = 0.0
        for k in LIQ_KEYS + list(HF_SHARES):
            mvsum += BAL0[k] * idx[LADDER[k]["path"]][t]
        liq_book[t] = mvsum - nco[t]
    priv_book = true_nav - liq_book
    agg = lambda n_: {k: float(sum(r[k] for r in rows[:n_])) for k in ("draw", "calls", "dist", "vm", "d_im", "hedge", "opp")}
    return dict(
        scenario=name, cfp_actions=cfp_actions, nav_facility_prearranged=nav_facility_prearranged,
        survival_months=sh,
        net_need_cum={"1m": float(nco[0]), "3m": float(nco[2]), "12m": float(nco[11]), "24m": float(nco[23]), "36m": float(nco[35])},
        cbc_TP={"1m": float(cbc["TP"][0]), "3m": float(cbc["TP"][2]), "12m": float(cbc["TP"][11]), "24m": float(cbc["TP"][23])},
        cbc_TPF={"1m": float(cbc["TPF"][0]), "3m": float(cbc["TPF"][2]), "12m": float(cbc["TPF"][11]), "24m": float(cbc["TPF"][23])},
        flows_12m=agg(12), flows_24m=agg(24),
        calls_by_group_12m={k: float(sum(r["calls_by"][k] for r in rows[:12])) for k in rows[0]["calls_by"]},
        dist_by_group_12m={k: float(sum(r["dist_by"][k] for r in rows[:12])) for k in rows[0]["dist_by"]},
        liquid_share={"t0": float((sum(BAL0[k] for k in LIQ_KEYS) + HF_TOTAL) / NAV0),
                      "12m": float(liq_book[11] / true_nav[11]), "24m": float(liq_book[23] / true_nav[23]),
                      "36m": float(liq_book[35] / true_nav[35])},
        nav_true={"12m": float(true_nav[11]), "24m": float(true_nav[23]), "36m": float(true_nav[35])},
    )


def lcr30_t0() -> dict:
    hqla = {
        "L1_cash_unencumbered": BAL0["cash"] - IM_RATE_N * SYN_NOTIONAL - OPP_IM,
        "L1_ust": BAL0["ust"] * (1 - 0.02),
        "L2A_ig": BAL0["ig"] * (1 - 0.15),
        "L2B_dm_equity": BAL0["lo_dm"] * (1 - 0.50),
        "L2_lo_fixed_income": BAL0["lo_fi"] * (1 - 0.25),
    }
    out = {
        "owner_draw_at_cap": 0.10 * NAV0 / 12,
        "calls_stressed": monthly_rate(min(0.95, 0.30 * 1.25)) * (38.0 - UNF0["sec_def"] - UNF0["pc_rev"]),
        "revolver_ddtl_draw": UNF0["pc_rev"] * 0.5 / 3,
        "vm_p99_30d_synthetic_beta": SYN_NOTIONAL * 0.117,
        "im_spike": (IM_RATE_S - IM_RATE_N) * SYN_NOTIONAL,
        "opportunistic_loss": 0.005 * NAV0,
        "secondary_deferred_payment": UNF0["sec_def"] / 4,
        "hedge_premium": HEDGE_PREMIUM_PA / 12,
    }
    inflow = {"distributions_crisis": sum(monthly_rate(DIST["crisis"][g]) * BAL0[g] for g in PRIVATE)}
    tot_out = sum(out.values())
    tot_in = min(sum(inflow.values()), 0.75 * tot_out)
    num_all = sum(hqla.values())
    num_l1 = hqla["L1_cash_unencumbered"] + hqla["L1_ust"] + hqla["L2A_ig"]
    return dict(hqla=hqla, outflows=out, inflows=inflow, total_outflow=tot_out, net_outflow=tot_out - tot_in,
                lcr30_all=num_all / (tot_out - tot_in), lcr30_L1_L2A=num_l1 / (tot_out - tot_in))


# --------------------------------------------------------------------------------------------
# 3. Quarterly Monte Carlo with a pecking-order (waterfall) policy
# --------------------------------------------------------------------------------------------
REG_NAMES = ["boom", "normal", "drought", "crisis"]
P_Q = np.array([[0.85, 0.12, 0.02, 0.01],
                [0.04, 0.88, 0.06, 0.02],
                [0.03, 0.06, 0.88, 0.03],
                [0.02, 0.08, 0.15, 0.75]])
EQ_MU = np.array([0.030, 0.020, 0.015, -0.090]); EQ_SD = np.array([0.06, 0.07, 0.08, 0.14])
FI_MU = np.array([0.013, 0.012, 0.011, -0.010]); FI_SD = np.array([0.02, 0.02, 0.02, 0.03])
HF_MU = np.array([0.020, 0.016, 0.014, -0.030]); HF_SD = np.array([0.03, 0.03, 0.03, 0.05])
CASH_Q = 0.039 / 4
DRAW_REG = np.array([0.05, 0.075, 0.075, 0.10])
DIST_Q = {g: np.array([1 - (1 - DIST[r][g]) ** 0.25 for r in REG_NAMES]) for g in PRIVATE}
CALL_Q = np.array([1 - (1 - CALL[r]) ** 0.25 for r in REG_NAMES])
BETA = {"pe": 1.1, "sec": 0.9, "co": 1.3, "cs": 0.5, "pc": 0.3}
ALPHA = {"pe": 0.010, "sec": 0.012, "co": 0.008, "cs": 0.020, "pc": 0.022}
PRICE_N = {"pe": 0.90, "sec": 0.88, "co": 0.82, "pc": 0.88, "cs": 0.85}
PRICE_C = {"pe": 0.65, "sec": 0.62, "co": 0.55, "pc": 0.75, "cs": 0.70}
HF_CAP = {"hf_le7d": (1.0, 0.8), "hf_8_90d": (0.6, 0.3), "hf_91_365d": (0.2, 0.1), "hf_gt365d": (0.08, 0.04)}


def clopper_pearson(k: int, n: int, alpha: float = 0.05):
    lo = 0.0 if k == 0 else float(beta_dist.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta_dist.ppf(1 - alpha / 2, k + 1, n - k))
    return [lo, hi]


def simulate(policy: str, n: int = 20000, Tq: int = 20, seed: int = 7, start_reg: int = 2,
             draw_nd: float = 0.075, pacing: float = NEW_COMMIT_PA) -> dict:
    """Policies: A base; B + committed RCF and pre-arranged NAV facility; C = B + stage-based pacing cut
    and early HF redemptions; D = C + owner-agreed distribution flex to 5% in Red/crisis;
    E = D + treasury target 12% of NAV (reserve funded from DM equities).
    start_reg: 0 boom, 1 normal, 2 drought (default), 3 crisis. draw_nd: owner draw in normal/drought."""
    rng = np.random.default_rng(seed)
    draw_reg = np.array([0.05, draw_nd, draw_nd, 0.10])
    first_red_reg = np.full(n, -1)
    rcf_on = policy in "BCDE"
    navf_on = policy in "BCDE"
    pacing_cut = policy in "CDE"
    early_hf = policy in "CDE"
    draw_flex = policy in "DE"
    t_min_normal = 0.12 if policy == "E" else 0.08
    b = {k: np.full(n, v) for k, v in BAL0.items()}
    u = {k: np.full(n, v) for k, v in UNF0.items()}
    if policy == "E":
        shift = 0.04 * NAV0
        b["lo_dm"] -= shift; b["cash"] += shift / 2; b["ust"] += shift / 2
    rep_prev = {g: np.zeros(n) for g in PRIVATE}
    reg = np.full(n, start_reg)
    fiscal = np.zeros(n, dtype=int)
    rcf = np.zeros(n); navf = np.zeros(n)
    im = np.full(n, IM_RATE_N * SYN_NOTIONAL)
    red = np.zeros(n, dtype=bool); black = np.zeros(n, dtype=bool); floor_breach = np.zeros(n, dtype=bool)
    first_red = np.full(n, -1)
    net_need_hist = []
    min_head = np.full(n, np.inf)
    illiq_max = np.zeros(n)
    cum_draw = np.zeros(n)
    sold_red = np.zeros(n); sold_amber = np.zeros(n); shortfall = np.zeros(n)
    crisis_q = np.zeros(n)
    hf_keys = list(HF_SHARES)
    for t in range(Tq):
        cdf = np.cumsum(P_Q[reg], axis=1)
        reg = (rng.random(n)[:, None] > cdf).sum(axis=1)
        crisis = reg == 3
        crisis_q += crisis
        onset = (rng.random(n) < 0.03) & (fiscal == 0)
        fiscal = np.where(onset, 8, np.maximum(fiscal - 1, 0))
        z = rng.standard_normal(n)
        r_eq = EQ_MU[reg] + EQ_SD[reg] * z
        r_em = 1.2 * r_eq + 0.04 * rng.standard_normal(n)
        r_fi = FI_MU[reg] + FI_SD[reg] * (0.3 * z + 0.95 * rng.standard_normal(n))
        r_hf = HF_MU[reg] + HF_SD[reg] * (0.5 * z + 0.87 * rng.standard_normal(n))
        nav_start = sum(b.values()) - rcf - navf
        b["lo_dm"] *= 1 + r_eq; b["lo_em"] *= 1 + r_em; b["lo_fi"] *= 1 + r_fi
        b["ig"] *= 1 + np.where(crisis, -0.005, 0.011); b["ust"] *= 1 + np.where(crisis, 0.015, 0.010)
        b["cash"] *= 1 + CASH_Q
        for k in hf_keys:
            b[k] *= 1 + r_hf
        for g in PRIVATE:
            econ = BETA[g] * (r_eq - CASH_Q) + CASH_Q + ALPHA[g] + np.where(crisis & (g == "pc"), -0.02, 0.0)
            rep = 0.5 * econ + 0.5 * rep_prev[g]
            rep_prev[g] = econ
            b[g] *= 1 + rep
        dist = np.zeros(n)
        for g in PRIVATE:
            d = DIST_Q[g][reg] * b[g]
            b[g] -= d; dist += d
        cq = CALL_Q[reg]
        calls = np.zeros(n)
        for k in ("pe", "sec", "pc", "cs", "co", "pc_rev"):
            c = cq * u[k]
            if k == "pc_rev":
                c = np.minimum(c + np.where(crisis, 0.25 * u[k], 0.0), u[k])
            if k == "pe":
                c = c + np.where(crisis, 0.02 * u[k], 0.0)
            u[k] -= c
            b["pc" if k == "pc_rev" else k] += c
            calls += c
        if t < 4:
            c = np.full(n, UNF0["sec_def"] / 4)
            u["sec_def"] -= c; b["sec"] += c; calls += c
        liq_share = (b["cash"] + b["ust"] + b["ig"] + b["lo_dm"] + b["lo_em"] + b["lo_fi"] + b["hf_le7d"] + b["hf_8_90d"]) / nav_start
        amber = liq_share < 0.26
        red_stage = liq_share < 0.20
        nc = np.full(n, pacing / 4)
        if pacing_cut:
            nc = np.where(amber | crisis, 0.25 * pacing / 4, nc)
        for k, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1)):
            u[k] += w * nc
        co_deal = np.full(n, 0.3)
        if pacing_cut:
            co_deal = np.where(amber | crisis, 0.0, co_deal)
        b["co"] += co_deal
        dr = np.where(fiscal > 0, 0.10, draw_reg[reg])
        if draw_flex:
            dr = np.where(crisis | red_stage, 0.05, dr)
        draw = dr / 4 * nav_start
        vm = SYN_NOTIONAL * r_eq
        im_new = np.where(crisis, IM_RATE_S, IM_RATE_N) * SYN_NOTIONAL
        d_im = im_new - im; im = im_new
        hedge = -HEDGE_PREMIUM_PA / 4 + HEDGE_NOTIONAL * np.clip(-r_eq - 0.10, 0.0, 0.20)
        opp = 0.0125 / 2 * NAV0 * rng.standard_normal(n) + np.where(crisis, -0.005, 0.001) * NAV0
        interest = (0.039 + 0.010) / 4 * rcf + (0.039 + 0.055) / 4 * navf
        opex = 0.001 / 4 * nav_start
        net_need = draw + calls + co_deal + interest + opex - dist - vm - hedge - opp + d_im
        net_need_hist.append(net_need)
        b["cash"] -= net_need
        cum_draw += draw
        if early_hf:
            for k in hf_keys:
                capn, caps = HF_CAP[k]
                take = np.where(amber | crisis, np.where(crisis, caps, capn) * b[k], 0.0)
                b[k] -= take; b["cash"] += take
        # --- waterfall: restore Treasury (cash+UST+IG) to its target; usable down to 4% NAV in crisis
        nav_now = sum(b.values()) - rcf - navf
        t_min = np.where(crisis, 0.04, t_min_normal)
        need = np.maximum(0.0, t_min * nav_now - (b["cash"] + b["ust"] + b["ig"]))
        need = np.maximum(need, -(b["cash"] + b["ust"] + b["ig"]))

        def take(avail, price):
            nonlocal need
            amt = np.minimum(np.maximum(avail, 0.0), need / price)
            need = need - amt * price
            return amt

        p_dm = np.where(crisis, 0.985, 0.998 - IM_RATE_N)
        a = take(0.5 * b["lo_dm"], p_dm); b["lo_dm"] -= a; b["cash"] += a * p_dm
        p_fi = np.where(crisis, 0.95, 0.995)
        a = take(0.5 * b["lo_fi"], p_fi); b["lo_fi"] -= a; b["cash"] += a * p_fi
        p_em = np.where(crisis, 0.95, 0.99)
        a = take(0.5 * b["lo_em"], p_em); b["lo_em"] -= a; b["cash"] += a * p_em
        if rcf_on:
            a = take(RCF_COMMITTED * np.where(crisis, 0.75, 1.0) - rcf, 1.0); rcf += a; b["cash"] += a
        for k in hf_keys:
            capn, caps = HF_CAP[k]
            a = take(np.where(crisis, caps, capn) * b[k], 1.0); b[k] -= a; b["cash"] += a
        if navf_on:
            ltv = np.where(crisis, 0.05, 0.10)
            a = take(ltv * (b["pe"] + b["sec"]) - navf, 0.985); navf += a; b["cash"] += a * 0.985
        for g in ("pc", "cs"):
            pr = np.where(crisis, PRICE_C[g], PRICE_N[g])
            a = take(0.10 * b[g], pr); b[g] -= a; b["cash"] += a * pr; sold_amber += a
        depth = np.where(crisis, 2.5, 4.0)
        for g in ("pe", "sec", "co"):
            pr = np.where(crisis, PRICE_C[g], PRICE_N[g])
            a = take(np.minimum(b[g], depth), pr)
            frac = a / np.maximum(b[g], 1e-9)
            if g in ("pe", "sec", "co"):
                u[g] *= 1 - frac
            b[g] -= a; b["cash"] += a * pr; sold_red += a; depth = depth - a
            hit = a > 1e-9
            new_hit = hit & (first_red < 0)
            first_red_reg = np.where(new_hit, reg, first_red_reg)
            first_red = np.where(new_hit, t + 1, first_red)
            red |= hit
        # remaining need only matters if Treasury is negative -> payout shortfall (critical)
        treas = b["cash"] + b["ust"] + b["ig"]
        short = np.maximum(0.0, -treas)
        is_short = short > 1e-6
        black |= is_short; red |= is_short
        new_hit = is_short & (first_red < 0)
        first_red_reg = np.where(new_hit, reg, first_red_reg)
        first_red = np.where(new_hit, t + 1, first_red)
        b["cash"] += short; cum_draw -= short; shortfall += short
        # repay facilities in non-crisis quarters from Treasury above target
        excess = np.maximum(0.0, b["cash"] + b["ust"] + b["ig"] - (t_min_normal + 0.02) * nav_now)
        rep_nav = np.where(~crisis, np.minimum(navf, excess), 0.0); navf -= rep_nav; b["cash"] -= rep_nav; excess -= rep_nav
        rep_rcf = np.where(~crisis, np.minimum(rcf, excess), 0.0); rcf -= rep_rcf; b["cash"] -= rep_rcf
        nav_now = sum(b.values()) - rcf - navf
        treas = b["cash"] + b["ust"] + b["ig"]
        floor_breach |= treas < 0.08 * nav_now - 1e-9
        liquid = treas + b["lo_dm"] + b["lo_em"] + b["lo_fi"] + b["hf_le7d"]
        min_head = np.minimum(min_head, liquid - 0.04 * nav_now)
        illiq = (sum(b[g] for g in PRIVATE) + b["hf_91_365d"] + b["hf_gt365d"]) / nav_now
        illiq_max = np.maximum(illiq_max, illiq)
    nnh = np.array(net_need_hist)
    need_4q = nnh[:4].sum(axis=0)
    nav_T = sum(b.values()) - rcf - navf
    wealth = nav_T + cum_draw
    k_red = int(red.sum())
    return dict(
        policy=policy, n_paths=n, quarters=Tq,
        p_red_5y=float(red.mean()), p_red_ci95=clopper_pearson(k_red, n),
        p_black_5y=float(black.mean()),
        p_treasury_below_8pct_any_q=float(floor_breach.mean()),
        median_first_red_q=float(np.median(first_red[first_red > 0])) if (first_red > 0).any() else None,
        mean_4q_net_need=float(need_4q.mean()),
        lar95_4q_net_need=float(np.quantile(need_4q, 0.95)),
        lar99_4q_net_need=float(np.quantile(need_4q, 0.99)),
        mean_annual_net_need_5y=float(nnh.sum(axis=0).mean() / (Tq / 4)),
        min_headroom_median=float(np.median(min_head)), min_headroom_p05=float(np.quantile(min_head, 0.05)),
        max_illiquid_share_median=float(np.median(illiq_max)), max_illiquid_share_p95=float(np.quantile(illiq_max, 0.95)),
        mean_red_sales_bn=float(sold_red.mean()), mean_amber_sales_bn=float(sold_amber.mean()),
        mean_shortfall_bn=float(shortfall.mean()),
        mean_terminal_nav=float(nav_T.mean()), median_terminal_nav=float(np.median(nav_T)),
        mean_distribution_inclusive_wealth=float(wealth.mean()), mean_cum_draw=float(cum_draw.mean()),
        mean_crisis_quarters=float(crisis_q.mean()),
        first_red_regime_share={REG_NAMES[i]: float(((first_red_reg == i).sum()) / max(1, (first_red > 0).sum()))
                                for i in range(4)},
        first_red_quarter_quartiles=([float(x) for x in np.quantile(first_red[first_red > 0], [0.25, 0.5, 0.75])]
                                     if (first_red > 0).any() else None),
        start_regime=REG_NAMES[start_reg], draw_normal_drought=draw_nd, pacing_pa=pacing,
    )


def stationary(P):
    w, v = np.linalg.eig(P.T)
    s = np.real(v[:, np.argmin(np.abs(w - 1))])
    return s / s.sum()


def reverse_stress_grid() -> list:
    """12- and 24-month closed-form ladders across stress severities (no red recourse, no facilities)."""
    out = []
    unf_regular = 38.0 - UNF0["sec_def"] - UNF0["pc_rev"]
    for eq_shock in (-0.20, -0.30, -0.40, -0.50):
        for dist_mult in (1.0, 0.6, 0.3, 0.0):
            for draw in (0.075, 0.10):
                for call_mult in (1.0, 1.25, 1.5):
                    priv_dist = sum(DIST["drought"][g] * dist_mult * BAL0[g] for g in PRIVATE)
                    c_rate = min(0.95, CALL["drought"] * call_mult)
                    calls12 = c_rate * unf_regular + UNF0["sec_def"] + 0.5 * UNF0["pc_rev"] + 0.25 * NEW_COMMIT_PA * 0.5
                    calls24 = calls12 + c_rate * unf_regular * (1 - c_rate) + 0.25 * NEW_COMMIT_PA * 1.5
                    vm = SYN_NOTIONAL * (-eq_shock)
                    hedge = HEDGE_NOTIONAL * min(0.20, max(0.0, -eq_shock - 0.10))
                    one_off = vm + (IM_RATE_S - IM_RATE_N) * SYN_NOTIONAL - hedge
                    need12 = draw * NAV0 + calls12 + one_off - priv_dist + HEDGE_PREMIUM_PA
                    need24 = 2 * draw * NAV0 + calls24 + one_off - 2 * priv_dist + 2 * HEDGE_PREMIUM_PA
                    cap12 = (BAL0["cash"] - IM_RATE_N * SYN_NOTIONAL - OPP_IM) + BAL0["ust"] * 0.98 + BAL0["ig"] * 0.90 \
                        + BAL0["lo_dm"] * (1 + eq_shock) * 0.985 + BAL0["lo_fi"] * 0.93 \
                        + BAL0["lo_em"] * (1 + 1.2 * eq_shock) * 0.95 \
                        + HF_TOTAL * (1 + 0.3 * eq_shock) * (0.084 * 0.8 + 0.273 * 0.5)
                    cap24 = cap12 + HF_TOTAL * (1 + 0.3 * eq_shock) * (0.273 * 0.5 + 0.644 * (2 / 3) * 0.6)
                    out.append(dict(eq_shock=eq_shock, dist_mult=dist_mult, draw=draw, call_mult=call_mult,
                                    need12=round(need12, 2), cap12=round(cap12, 2), cover12=round(cap12 / need12, 2),
                                    need24=round(need24, 2), cap24=round(cap24, 2), cover24=round(cap24 / need24, 2),
                                    breach12=bool(need12 > cap12), breach24=bool(need24 > cap24),
                                    residual_liquid_share_24m=round((cap24 - need24) / (NAV0 * (1 + 0.4 * eq_shock) - need24), 3)))
    return out


def main() -> None:
    res = {"note": "SYNTHETIC/ILLUSTRATIVE [I]; working allocation from context section 1A; not ADIC data."}
    res["balance_sheet_bn"] = BAL0
    res["unfunded_bn"] = UNF0
    res["groups"] = GROUP
    res["lcr30_t0"] = lcr30_t0()
    named = {}
    for s in ("B0_drought", "S1_demand_bust_24m", "S2_owner_draw_cap_36m", "S3_rates_collateral_2022"):
        named[s + "|gross"] = run_named(s)
        named[s + "|cfp"] = run_named(s, cfp_actions=True, nav_facility_prearranged=True)
    res["named"] = named
    res["regime_stationary_quarterly"] = dict(zip(REG_NAMES, [float(x) for x in stationary(P_Q)]))
    res["monte_carlo"] = {pol: simulate(pol) for pol in "ABCDE"}
    sens = {}
    for pol in ("A", "D"):
        sens[f"{pol}|start_normal"] = simulate(pol, start_reg=1)
        sens[f"{pol}|draw_5pct"] = simulate(pol, draw_nd=0.05)
        sens[f"{pol}|draw_10pct"] = simulate(pol, draw_nd=0.10)
        sens[f"{pol}|pacing_8bn"] = simulate(pol, pacing=8.0)
        sens[f"{pol}|pacing_16bn"] = simulate(pol, pacing=16.0)
    keep = ("p_red_5y", "p_red_ci95", "p_black_5y", "lar95_4q_net_need", "lar99_4q_net_need",
            "mean_distribution_inclusive_wealth", "max_illiquid_share_median", "first_red_regime_share")
    res["monte_carlo_sensitivity"] = {k: {kk: v[kk] for kk in keep} for k, v in sens.items()}
    rs = reverse_stress_grid()
    res["reverse_stress_n_cells"] = len(rs)
    res["reverse_stress_breach12"] = [r for r in rs if r["breach12"]]
    res["reverse_stress_breach24_mildest"] = sorted([r for r in rs if r["breach24"]],
                                                    key=lambda r: (r["need24"]))[:10]
    res["reverse_stress_share_breach24"] = sum(r["breach24"] for r in rs) / len(rs)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=float)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
