"""Independent re-check of G4 dossier section 6.5 decision examples (SELL bid, REFI breach).

*** EXTENDED COPY (research/groups/addenda/G4_barrier_rerun, 2026-10-18) ***
Copied from the G4 verifier's scratchpad script g4v_scripts/check_decisions.py; run() below is
unchanged and reproduces the published quarterly-tested figures (49.6/62.5% trigger, 32.7/47.9%
default level).  Added: barrier-monitoring analysis for every path statistic of the example.
  1. Closed-form CONTINUOUS-monitoring probabilities (exact for this model: EV is a GBM and net
     debt is constant, so every barrier is a constant level for ln V):
        P(min_{t<=T} X_t <= b) = N((b - nu T)/(s sqrt T)) + exp(2 nu b / s^2) N((b + nu T)/(s sqrt T))
        P(min X <= b, X_T > a) = exp(2 nu b / s^2) N((2b + nu T - a)/(s sqrt T)),  a >= b
     with X_t = ln(V_t/V_0), nu = mu - s^2/2, b = ln(B/V_0) < 0.
  2. Broadie-Glasserman-Kou (1997) continuity correction in both directions:
        discrete(B) ~ continuous(B * exp(-beta s sqrt(dt)))   [BGK's own use: price a discrete barrier]
        continuous(B) ~ discrete(B * exp(+beta s sqrt(dt)))   [the fix: make a quarterly check mimic
                                                               continuous monitoring]
  3. Fine-grid simulation (312 steps a year) with quarterly, monthly, weekly and 312/yr checks on
     the same paths, plus the BGK-shifted quarterly check and the dossier's wrong-sign shift.
  4. Wipe-out sensitivity: calc section 6 measures wipe-out only at exit; the dossier's own E3
     default rule (write-off when V <= 0.75 D at any time) adds paths that touch the barrier and
     recover.  Reported as a definitional sensitivity, not as a correction.
All inputs are the dossier's illustrative [I] values; nothing here is ADIC data.  SYNTHETIC.
Run:  <venv>/python.exe -I check_decisions_bgk.py   (writes check_decisions_bgk_results.json here)
"""
import json
import math
import os

import numpy as np
from scipy.stats import norm

SEED = 20261018 + 6
NAV = 400.0
NOWCAST = 0.97 * NAV
L_NOW = 6.0 / 14.0
EV0 = NOWCAST / (1 - L_NOW)
DEBT = EV0 * L_NOW
H = 0.09

BGK_BETA = 0.5825971579390106      # -zeta(1/2)/sqrt(2*pi); BGK (1997) abstract: beta ~ 0.5826
KAPPA_E3 = 0.75                     # dossier E3 / calc BOOK default_kappa
PIK_RATE, PIK_LTV = 0.12, 0.25      # calc section 6 LEVER example
SCEN = {"normal": (2.5, 0.06, 0.28), "drought": (3.5, 0.04, 0.30)}
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "check_decisions_bgk_results.json")


def run(tau, mu_a, s_a, n=400_000, dt=0.25, seed=SEED):
    rng = np.random.default_rng(seed)
    steps = int(round(tau / dt))
    ln_ev = np.full(n, math.log(EV0))
    min_eq = np.full(n, np.inf)
    for _ in range(steps):
        ln_ev += (mu_a - 0.5 * s_a ** 2) * dt + s_a * math.sqrt(dt) * rng.standard_normal(n)
        eq = np.maximum(np.exp(ln_ev) - DEBT, 0.0)
        min_eq = np.minimum(min_eq, eq)
    eq_T = np.maximum(np.exp(ln_ev) - DEBT, 0.0)
    out = dict(
        tau=tau,
        E_exit_equity=float(eq_T.mean()),
        p_trigger_terminal=float((eq_T < NAV * (2 / 3)).mean()),
        p_trigger_pathwise_quarterly=float((min_eq < NAV * (2 / 3)).mean()),
        p_default_terminal=float((eq_T < NAV * 0.5).mean()),
        p_default_pathwise_quarterly=float((min_eq < NAV * 0.5).mean()),
    )
    for yb in (0.20, 0.25):
        bid = out["E_exit_equity"] / (1 + yb) ** tau
        out[f"implied_bid_pct_nav_yb{int(yb*100)}"] = bid / NAV
    out["buyer_irr_at_95pct_bid"] = (out["E_exit_equity"] / (0.95 * NAV)) ** (1 / tau) - 1
    return out


# --------------------------------------------------------------------------- added analysis
def levels(tau):
    """EV levels of every event in the example (net debt is constant in calc section 6)."""
    pik_due = PIK_LTV * NAV * (1 + PIK_RATE) ** tau
    return dict(trigger=DEBT + NAV * 2 / 3,          # equity < 2/3 NAV  <=>  LTV >= 1.5 x 15%
                default_level=DEBT + NAV * 0.5,      # equity < 1/2 NAV  <=>  LTV >= 2 x 15%
                e3_barrier=KAPPA_E3 * DEBT,          # dossier E3 write-off barrier
                wipe_terminal=DEBT,                  # calc p_wipeout: equity = 0 at exit
                pik_terminal=DEBT + pik_due)         # calc p_residual_zero: equity <= PIK due at exit


def p_hit_cont(B, tau, mu, s):
    b, nu, sd = math.log(B / EV0), mu - 0.5 * s * s, s * math.sqrt(tau)
    return float(norm.cdf((b - nu * tau) / sd) + math.exp(2 * nu * b / s ** 2) * norm.cdf((b + nu * tau) / sd))


def p_union_cont(B_bar, B_term, tau, mu, s):
    """P(min V <= B_bar or V_tau <= B_term), B_bar <= B_term (continuous barrier, terminal test)."""
    b, a = math.log(B_bar / EV0), math.log(B_term / EV0)
    nu, sd = mu - 0.5 * s * s, s * math.sqrt(tau)
    return float(norm.cdf((a - nu * tau) / sd) + math.exp(2 * nu * b / s ** 2) * norm.cdf((2 * b + nu * tau - a) / sd))


def p_term(B, tau, mu, s):
    nu, sd = mu - 0.5 * s * s, s * math.sqrt(tau)
    return float(norm.cdf((math.log(B / EV0) - nu * tau) / sd))


def fine_grid(tau, mu, s, n=400_000, per_year=312, seed=SEED + 1000):
    """Running minima of ln V at quarterly / monthly / weekly / per-step checkpoints, same paths."""
    rng = np.random.default_rng(seed)
    dts = 1.0 / per_year
    steps = int(round(tau * per_year))
    every = {"Q": per_year // 4, "M": per_year // 12, "W": per_year // 52, "F": 1}
    x = np.zeros(n)
    mins = {k: np.full(n, np.inf) for k in every}
    drift, vol = (mu - 0.5 * s * s) * dts, s * math.sqrt(dts)
    for k in range(steps):
        x += drift + vol * rng.standard_normal(n)
        for f, m in every.items():
            if (k + 1) % m == 0:
                np.minimum(mins[f], x, out=mins[f])
    return x, mins


def analyse(name, tau, mu, s):
    lv = levels(tau)
    shift_q = BGK_BETA * s * math.sqrt(0.25)
    shift_m = BGK_BETA * s * math.sqrt(1 / 12)
    xT, mins = fine_grid(tau, mu, s)
    lb = {k: math.log(v / EV0) for k, v in lv.items()}
    out = {"levels_EV": lv, "bgk_shift_quarterly_log": shift_q, "bgk_factor_quarterly": math.exp(shift_q)}
    for ev_name in ("trigger", "default_level", "e3_barrier"):
        b = lb[ev_name]
        B = lv[ev_name]
        out[ev_name] = dict(
            terminal_closed_form=p_term(B, tau, mu, s),
            continuous_closed_form=p_hit_cont(B, tau, mu, s),
            quarterly_bgk_predicted_from_continuous=p_hit_cont(B * math.exp(-shift_q), tau, mu, s),
            sim_terminal=float((xT <= b).mean()),
            sim_quarterly=float((mins["Q"] <= b).mean()),
            sim_quarterly_bgk_fix=float((mins["Q"] <= b + shift_q).mean()),
            sim_quarterly_bgk_wrong_sign=float((mins["Q"] <= b - shift_q).mean()),
            sim_monthly=float((mins["M"] <= b).mean()),
            sim_monthly_bgk_fix=float((mins["M"] <= b + shift_m).mean()),
            sim_weekly=float((mins["W"] <= b).mean()),
            sim_312_per_year=float((mins["F"] <= b).mean()),
        )
        sq = np.array([math.sqrt(1 / 12), math.sqrt(1 / 52), math.sqrt(1 / 312)])
        ys = np.array([out[ev_name]["sim_monthly"], out[ev_name]["sim_weekly"], out[ev_name]["sim_312_per_year"]])
        out[ev_name]["sim_continuous_extrapolated"] = float(np.polyfit(sq, ys, 1)[1])
    # wipe-out: published = terminal only; sensitivity = dossier E3 barrier (any time) OR terminal test
    be3 = lb["e3_barrier"]
    for tag, term in (("wipeout_unlevered", "wipe_terminal"), ("wipeout_levered_pik", "pik_terminal")):
        a = lb[term]
        out[tag] = dict(
            terminal_only_closed_form=p_term(lv[term], tau, mu, s),
            terminal_only_sim=float((xT <= a).mean()),
            with_E3_continuous_closed_form=p_union_cont(lv["e3_barrier"], lv[term], tau, mu, s),
            with_E3_quarterly_sim=float(((mins["Q"] <= be3) | (xT <= a)).mean()),
            with_E3_quarterly_bgk_fix_sim=float(((mins["Q"] <= be3 + shift_q) | (xT <= a)).mean()),
            with_E3_monthly_sim=float(((mins["M"] <= be3) | (xT <= a)).mean()),
            with_E3_312_per_year_sim=float(((mins["F"] <= be3) | (xT <= a)).mean()),
        )
    return out


if __name__ == "__main__":
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "bgk_beta": BGK_BETA, "kappa_E3": KAPPA_E3,
           "inputs": dict(NAV=NAV, nowcast=NOWCAST, EV0=EV0, debt=DEBT, scenarios=SCEN)}
    for name, (tau, mu, s) in SCEN.items():
        r = run(tau, mu, s)
        print(name, "ORIGINAL run():", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
        res[name] = {"original_run": r, "analysis": analyse(name, tau, mu, s)}
        a = res[name]["analysis"]
        for ev_name in ("trigger", "default_level", "e3_barrier"):
            print(f"  {ev_name:14s}", {k: round(v, 4) for k, v in a[ev_name].items()})
        for tag in ("wipeout_unlevered", "wipeout_levered_pik"):
            print(f"  {tag:20s}", {k: round(v, 4) for k, v in a[tag].items()})
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print("wrote", OUT)
