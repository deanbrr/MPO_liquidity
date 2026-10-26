"""The four stakeholder lenses and the house constraints they own (one platform, many objectives).

Each lens is a preference profile (which return evidence to trust, how likely each ER world is, how risk-averse),
a default objective, a default stress, and the house limits it OWNS. Every optimization, whoever runs it, carries
every group's current limits as constraints (the epsilon-constraint method), so the four objectives meet in one
feasible set: the Strategy group cannot reach for 10% by breaching the Liquidity group's appetite, and the Liquidity
group cannot hoard cash below the return the Strategy group needs. The IC view prices the conflicts: it compares each
lens's plan, the status quo and the consensus plan (the Strategy objective under every limit) on one common view.
"""
from __future__ import annotations

import copy

from .buckets import LIQUID_RISK

ROLES = ["strategy", "balance_sheet", "liquidity", "asset_allocation"]

LENSES = {
    "strategy": {
        "title": "Strategy",
        "subtitle": "Owns the 10% hurdle: the probability of reaching it over five years, and what each lever buys",
        "objective": "gbo",
        "prefs": {"basis": "strategy", "scenario_probs": {"Downside": 0.25, "Base": 0.50, "Upside": 0.25},
                  "risk_aversion": 2.0, "weights": {"underwritten": 0.15, "actual": 0.25}, "persistence": 0.30,
                  "uw_debias": True},
        "stress": "base",
        "owns": ["goal_rate", "depth_guard", "depth_delta", "p_goal_min"],
    },
    "balance_sheet": {
        "title": "Balance Sheet",
        "subtitle": "Owns assets and liabilities: total NAV, the sleeves outside the fund file, debt, leverage and LTV",
        "objective": "utility",
        "prefs": {"basis": "strategy", "scenario_probs": {"Downside": 0.35, "Base": 0.50, "Upside": 0.15},
                  "risk_aversion": 4.0, "weights": {"underwritten": 0.15, "actual": 0.25}, "persistence": 0.30,
                  "uw_debias": True},
        "stress": "base",
        "owns": ["total_nav_bn", "sleeve_split", "lev_cap", "recourse_cap", "new_term_max_bn", "navf_ltv_max",
                 "allow_debt", "allow_beta", "beta_max", "overcommit", "bs_guard_prob", "revolver_signed_bn", "revolver_drawn0_bn",
                 "term_debt0_bn"],
    },
    "liquidity": {
        "title": "Liquidity",
        "subtitle": "Owns calls and the owner's annual distribution: reserve floor, waterfall, forced-sale appetite",
        "objective": "liquidity",
        "prefs": {"basis": "strategy", "scenario_probs": {"Downside": 0.40, "Base": 0.45, "Upside": 0.15},
                  "risk_aversion": 6.0, "weights": {"underwritten": 0.15, "actual": 0.25}, "persistence": 0.30,
                  "uw_debias": True},
        "stress": "prolonged_drought",
        "owns": ["floor_target", "floor_hard", "forced_eps", "ret_min", "waterfall", "draw_mode", "draw_rate",
                 "hf_quarterly_liquidity"],
    },
    "asset_allocation": {
        "title": "Asset Allocation",
        "subtitle": "Owns substitution: SELL / HOLD / REFINANCE / LEVER per holding, the PE program and what replaces it",
        "objective": "utility",
        "prefs": {"basis": "blend", "scenario_probs": {"Downside": 0.25, "Base": 0.50, "Upside": 0.25},
                  "risk_aversion": 3.0, "weights": {"underwritten": 0.15, "actual": 0.25}, "persistence": 0.30,
                  "uw_debias": True},
        "stress": "base",
        "owns": ["range_band", "pace_mult", "commit_agg_mult", "coinvest_extra_bn", "new_strategy_entry_bn",
                 "allow_other_sales", "pe_program_enabled", "pe_program_total_bn", "pe_program_years",
                 "pe_program_basis", "pe_program_selection", "even_program"],
    },
}

# defaults for every house setting (the assumption file supplies the rest)
HOUSE_DEFAULTS = {
    "goal_rate": 0.10, "depth_guard": True, "depth_delta": 0.0, "p_goal_min": 0.0,
    "total_nav_bn": 177.0, "sleeve_split": {}, "lev_cap": 1.15, "recourse_cap": 0.15, "new_term_max_bn": 10.0,
    "navf_ltv_max": 0.10, "allow_debt": True, "allow_beta": True, "beta_max": 25.0, "overcommit": 0.80, "bs_guard_prob": 0.95,
    "revolver_signed_bn": 10.0, "revolver_drawn0_bn": 0.0, "term_debt0_bn": 0.0,
    "floor_target": 0.08, "floor_hard": 0.04, "forced_eps": 0.01, "ret_min": 0.085,
    "waterfall": ["AGG", "GE_DM", "GE_GLOBAL", "GE_EM", "HF", "MAO_EXT", "MAO_INT", "REVOLVER", "FORCED"],
    "draw_mode": "rule", "draw_rate": 0.07, "hf_quarterly_liquidity": [0.25, 0.20, 0.10],
    "range_band": [0.5, 1.5], "pace_mult": [0.0, 1.5], "commit_agg_mult": 1.25, "coinvest_extra_bn": 1.5,
    "new_strategy_entry_bn": 0.3, "allow_other_sales": True, "pe_program_enabled": True, "pe_program_total_bn": 20.0,
    "pe_program_years": 3, "pe_program_basis": "exposure", "pe_program_selection": "underperformers",
    "even_program": False,
}

OBJECTIVES = {
    "gbo": "Maximize the buffered probability of reaching the hurdle (GBO), CRRA tie-break",
    "utility": "Maximize CRRA utility of five-year wealth (risk-adjusted net worth)",
    "liquidity": "Minimize forced-sale and liquidity cost subject to the return floor",
    "mean_cvar": "Maximize mean wealth minus the CVaR of the worst 10%",
    "mean": "Maximize mean five-year wealth (no risk penalty; for reference)",
}

SETTING_OWNER = {k: role for role, lens in LENSES.items() for k in lens["owns"]}


def target_only(lev_cap: float = 1.0, liquid_caps: dict | None = None) -> dict:
    """House overrides for the 10% target alone: every group's policy limit removed (leverage, recourse, LTV and
    term-debt caps beyond lev_cap; the reserve floor and target; the forced-sale appetite; the depth guard; the
    return floor; IC ranges; pacing bands; overcommitment; the PE program). What stays is fact, not policy: the
    budget and ownership, the owner's distribution and capital calls (paid through the waterfall), secondary-market
    depth, co-invest deal flow, margin for synthetic beta, and fund commitments up to 5x today's pace (market access).
    liquid_caps: optional capacity per liquid sleeve in $bn (e.g. {"HF": 45.6})."""
    caps = {b: [0.0, 1e4] for b in LIQUID_RISK}
    caps.update({b: [0.0, float(v)] for b, v in (liquid_caps or {}).items()})
    return {"depth_guard": False, "forced_eps": 0.0, "p_goal_min": 0.0, "ret_min": 0.0, "lev_cap": float(lev_cap),
            "recourse_cap": 1.0, "new_term_max_bn": 1e6, "navf_ltv_max": 0.5, "beta_max": 1e4, "overcommit": 50.0,
            "floor_target": 0.0, "floor_hard": 0.0, "range_band": [0.0, 1e3], "pace_mult": [0.0, 5.0],
            "commit_agg_mult": 5.0, "pe_program_enabled": False, "x_bounds": caps, "bs_guard_prob": 0.0}


def default_state(role: str) -> dict:
    lens = LENSES[role]
    return {"prefs": copy.deepcopy(lens["prefs"]), "objective": lens["objective"], "stress": lens["stress"],
            "settings": {k: copy.deepcopy(HOUSE_DEFAULTS[k]) for k in lens["owns"]}}


def house(states: dict) -> dict:
    """Every group's owned settings, merged (each key comes from its owner's state)."""
    out = copy.deepcopy(HOUSE_DEFAULTS)
    for role, st in states.items():
        for k in LENSES[role]["owns"]:
            if k in st.get("settings", {}):
                out[k] = copy.deepcopy(st["settings"][k])
    return out


def lp_settings(house_settings: dict, prefs: dict, use_house: bool = True, own: dict | None = None) -> dict:
    """Settings dict for TPPModel / sim from the house limits (or only the role's own when use_house=False)."""
    s = copy.deepcopy(house_settings if use_house else {**HOUSE_DEFAULTS, **(own or {})})
    s["risk_aversion"] = float(prefs.get("risk_aversion", 3.0))
    return s
