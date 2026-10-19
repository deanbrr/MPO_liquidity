"""G11 (Real Assets: infrastructure) - Part A: archetype DCF durations.

SYNTHETIC - NOT ADIC DATA. Illustrative archetypes only.

Each archetype has annual nominal asset cash flows (CFADS = revenue - opex - maintenance capex),
a debt policy and a forward-curve valuation. Equity value V_E = V_A - V_D (asset and debt each
discounted on their own forward curves). Reported sensitivities, all as -dlnV_E per +100bp
(so a positive number means equity LOSES value when the shocked rate rises):

  D_eq_y    'EDHEC-style' duration: equity cash flows held FIXED, equity discount rate +100bp.
            This is what infraMetrics reports (7.4-11.6 across segments, Q1 2021).
  D_real_P  +100bp PERMANENT parallel real-rate shock: asset discount rates, debt market values,
            refinancing coupons and (regulated assets) allowed-return resets all respond.
  D_real_MR +100bp real-rate shock that mean-reverts with a 5-year half-life along the forward curve.
  D_infl    +100bp permanent expected-inflation shock (nominal rates +100bp; revenues escalate by
            theta; opex/capex by full inflation; fixed coupons erode; RAB indexed).
  D_erp     +100bp asset risk premium (asset discount rate only; allowed returns do not reset).

Debt policies: 'amort' = level annuity over tenor (project finance);
               'regear' = interest-only, debt re-sized each year to gearing x asset cash-flow
               index (constant-leverage corporate/holdco policy), original tranche at a locked
               coupon until its tenor, refinanced and increments at the then-forward market rate.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

OUT = Path(__file__).with_name("g11_durations_results.json")

R_REAL = 0.023   # 10y real rate proxy (10y UST 5.09% nominal, Oct-2026, less ~2.8% breakeven)
PI_E = 0.028     # expected inflation
HL_MR = 5.0      # half-life (years) of the mean-reverting real-rate shock
N_MAX = 80


@dataclass
class Archetype:
    key: str
    name: str
    life: int
    terminal_mult: float      # terminal value as multiple of final-year CFADS (0 = finite life)
    g_real: float
    theta: float              # revenue inflation pass-through
    opex_share: float         # opex / revenue at t0
    capex_share: float        # maintenance capex / revenue at t0
    erp_asset: float
    gearing: float
    debt_spread: float
    debt_policy: str          # 'amort' or 'regear'
    debt_tenor: int           # amortisation tenor, or tenor of the locked original tranche
    fixed_share: float
    regulated: bool = False
    reset_every: int = 5
    notes: str = ""


ARCHETYPES = [
    Archetype("REG", "Regulated utility (RAB CPI-indexed, 5y resets)", 60, 0.0, 0.010, 1.0, 0.0, 0.0,
              0.030, 0.65, 0.010, "regear", 10, 0.85, regulated=True,
              notes="Cash = allowed real return x indexed RAB - net growth capex; terminal RAB at par; "
                    "allowed real return resets to market real rate + premium every 5y."),
    Archetype("CON-IDX", "Availability PPP (90% CPI-indexed, 25y)", 25, 0.0, 0.0, 0.90, 0.25, 0.05,
              0.030, 0.80, 0.012, "amort", 22, 0.95, notes="Finite concession; nominal amortising debt."),
    Archetype("CON-FIX", "Contracted renewables (fixed PPA, 25y)", 25, 0.0, 0.0, 0.10, 0.20, 0.05,
              0.035, 0.75, 0.014, "amort", 18, 0.90, notes="Fixed-price PPA; opex indexed."),
    Archetype("TOLL", "Toll road (CPI escalator, 40y)", 40, 0.0, 0.015, 0.80, 0.25, 0.08,
              0.040, 0.60, 0.018, "regear", 8, 0.80, notes="Traffic +1.5% real; tolls theta 0.8."),
    Archetype("AIR", "Airport (50y, partly regulated)", 50, 0.0, 0.020, 0.80, 0.45, 0.10,
              0.045, 0.55, 0.018, "regear", 8, 0.85, notes="High operating leverage."),
    Archetype("TOW", "Tower/fibre (fixed 3% escalators)", 30, 15.0, 0.020, 0.30, 0.25, 0.05,
              0.045, 0.55, 0.020, "regear", 7, 0.80, notes="Fixed escalators ~ theta 0.3."),
    Archetype("DC", "Stabilised data centre (re-lease at market)", 30, 12.0, 0.030, 0.40, 0.40, 0.08,
              0.055, 0.50, 0.022, "regear", 5, 0.60, notes="Equity-like ERP; obsolescence capex."),
    Archetype("MID", "Midstream (take-or-pay, half-indexed tariffs)", 30, 7.0, 0.0, 0.50, 0.35, 0.06,
              0.050, 0.50, 0.020, "regear", 7, 0.90, notes="Contracted volumes."),
]


def curves(shock_r: float = 0.0, shock_pi: float = 0.0, mr: bool = False):
    s = np.arange(1, N_MAX + 1, dtype=float)
    k = math.log(2) / HL_MR
    fr = R_REAL + (shock_r * np.exp(-k * (s - 1)) if mr else shock_r)
    fpi = np.full(N_MAX, PI_E + shock_pi)
    return np.asarray(fr, dtype=float) * np.ones(N_MAX), fpi


def disc_factors(fwd: np.ndarray) -> np.ndarray:
    return np.exp(-np.cumsum(np.log1p(fwd)))


def asset_cfs(a: Archetype, fr: np.ndarray, fpi: np.ndarray, erp_shift: float = 0.0) -> np.ndarray:
    n = a.life
    idx = np.cumprod(1 + fpi[:n])                 # price index at end of each year
    if a.regulated:
        cfs = np.zeros(n)
        allowed = R_REAL + a.erp_asset            # current control set at base rates
        for yr in range(1, n + 1):
            if (yr - 1) % a.reset_every == 0 and yr > 1:
                # regulator resets to the market real rate and passes through half of any
                # change in the required risk premium (cost-of-equity evidence is partial)
                allowed = fr[yr - 1] + a.erp_asset + 0.5 * erp_shift
            rab_open = (idx[yr - 2] if yr > 1 else 1.0) * (1 + a.g_real) ** (yr - 1)
            cfs[yr - 1] = rab_open * (1 + fpi[yr - 1]) * (allowed - a.g_real)
        cfs[-1] += idx[n - 1] * (1 + a.g_real) ** n
        return cfs
    t = np.arange(1, n + 1)
    rev_idx = np.cumprod(1 + a.theta * fpi[:n]) * (1 + a.g_real) ** t
    cf = rev_idx - (a.opex_share + a.capex_share) * idx
    if a.terminal_mult > 0:
        cf = cf.copy()
        cf[-1] += a.terminal_mult * cf[-1]
    return cf


def value(a: Archetype, fr, fpi, erp_shift=0.0, base=None):
    n = a.life
    fnom = fr[:n] + fpi[:n]
    cf = asset_cfs(a, fr, fpi, erp_shift)
    dfa = disc_factors(fnom + a.erp_asset + erp_shift)
    VA = float(np.sum(cf * dfa))
    dfd = disc_factors(fnom + a.debt_spread)
    if base is None:
        D0 = a.gearing * VA
        i_lock = R_REAL + PI_E + a.debt_spread
        cf_index = cf / cf[0] if cf[0] > 0 else np.ones(n)
        if a.terminal_mult == 0 and not a.regulated:
            # finite concession: constant-leverage until 15y before expiry, then taper to zero
            tail = 15
            taper = np.ones(n)
            start = max(n - tail, 1)
            taper[start:] = np.linspace(1.0, 0.0, n - start)
            cf_index = cf_index * taper
    else:
        D0, i_lock = base["D0"], base["i_lock"]
        cf_index = base["cf_index"]                # debt sizing follows the base-case plan
    interest = np.zeros(n)
    principal = np.zeros(n)
    if a.debt_policy == "amort":
        bal_f, bal_v = D0 * a.fixed_share, D0 * (1 - a.fixed_share)
        nT = min(a.debt_tenor, n)
        pay_f = bal_f * i_lock / (1 - (1 + i_lock) ** (-nT))
        for k in range(nT):
            i_f = bal_f * i_lock
            i_v = bal_v * (fnom[k] + a.debt_spread)
            p_f = pay_f - i_f
            p_v = (D0 * (1 - a.fixed_share)) / nT
            interest[k] = i_f + i_v
            principal[k] = p_f + p_v
            bal_f -= p_f
            bal_v -= p_v
    else:  # regear: balance_t = D0 * cf_index_t (base plan); original tranche locked to tenor
        bal = D0 * cf_index
        prev = D0
        for k in range(n):
            orig = D0
            mkt = fnom[k] + a.debt_spread
            if k < a.debt_tenor:
                cost_orig = orig * (a.fixed_share * i_lock + (1 - a.fixed_share) * mkt)
            else:
                cost_orig = orig * mkt
            incr = max(bal[k - 1] if k > 0 else D0, 0.0) - orig
            interest[k] = cost_orig + incr * mkt
            principal[k] = -(bal[k] - prev) if k < n - 1 else prev
            prev = bal[k]
    ds = interest + principal
    VD = float(np.sum(ds * dfd))
    ecf = cf - ds
    return {"VA": VA, "VD": VD, "VE": VA - VD, "ecf": ecf, "cf": cf, "ds": ds,
            "base": {"D0": D0, "i_lock": i_lock, "cf_index": cf_index}}


def irr(cfs, price):
    lo, hi = -0.9, 2.0
    t = np.arange(1, len(cfs) + 1)
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if np.sum(cfs / (1 + mid) ** t) > price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def pv_flat(cfs, y):
    t = np.arange(1, len(cfs) + 1)
    return float(np.sum(cfs / (1 + y) ** t))


def sens(a: Archetype, debt_tenor_override: int | None = None, fixed_override: float | None = None):
    if debt_tenor_override is not None or fixed_override is not None:
        a = Archetype(**{**asdict(a), **({"debt_tenor": debt_tenor_override} if debt_tenor_override else {}),
                         **({"fixed_share": fixed_override} if fixed_override is not None else {})})
    fr0, fpi0 = curves()
    b = value(a, fr0, fpi0)
    VE0 = b["VE"]
    ye = irr(b["ecf"], VE0)
    d_eq_y = -(math.log(pv_flat(b["ecf"], ye + 0.01)) - math.log(pv_flat(b["ecf"], ye))) / 0.01
    out = {"equity_irr": ye, "cash_yield_y1": float(b["ecf"][0] / VE0),
           "cash_yield_avg_y1_10": float(np.mean(b["ecf"][:10]) / VE0), "D_eq_y": d_eq_y}
    for lab, (sr, sp, mr, se) in {"D_real_P": (0.01, 0, False, 0), "D_real_MR": (0.01, 0, True, 0),
                                  "D_infl": (0, 0.01, False, 0), "D_erp": (0, 0, False, 0.01)}.items():
        fr, fpi = curves(sr, sp, mr)
        v = value(a, fr, fpi, erp_shift=se, base=b["base"])
        out[lab] = -(math.log(max(v["VE"], 1e-9)) - math.log(VE0)) / 0.01
    dscr = b["cf"][:20] / np.where(np.abs(b["ds"][:20]) > 1e-9, b["ds"][:20], np.nan)
    out["min_DSCR_or_ICR_20y"] = float(np.nanmin(dscr)) if np.isfinite(np.nanmin(dscr)) else None
    # unlevered asset duration (flat yield at asset IRR)
    ya = irr(b["cf"], b["VA"])
    out["D_asset"] = -(math.log(pv_flat(b["cf"], ya + 0.01)) - math.log(pv_flat(b["cf"], ya))) / 0.01
    return out


def run():
    rows = []
    for a in ARCHETYPES:
        s = sens(a)
        rows.append({"key": a.key, "archetype": a.name, **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items()},
                     "gearing": a.gearing, "theta": a.theta, "debt_policy": a.debt_policy, "debt_tenor": a.debt_tenor,
                     "fixed_share": a.fixed_share})
    # debt-tenor sensitivity for the refinancing channel (regear archetypes)
    tenor_tab = []
    for a in ARCHETYPES:
        if a.debt_policy != "regear":
            continue
        for ten in (3, 8, 15, 25):
            s = sens(a, debt_tenor_override=ten, fixed_override=1.0)
            tenor_tab.append({"key": a.key, "locked_tenor": ten, "D_real_P": round(s["D_real_P"], 2),
                              "D_real_MR": round(s["D_real_MR"], 2), "D_infl": round(s["D_infl"], 2),
                              "D_eq_y": round(s["D_eq_y"], 2)})
    out = {"label": "SYNTHETIC - NOT ADIC DATA (illustrative archetypes)",
           "base_rates": {"real": R_REAL, "expected_inflation": PI_E, "mean_reversion_half_life_y": HL_MR},
           "definition": "-dlnV_E per +100bp; positive = equity loses value when the shocked rate rises",
           "rows": rows, "tenor_sensitivity_fixed_share_1": tenor_tab,
           "archetype_inputs": [asdict(a) for a in ARCHETYPES]}
    OUT.write_text(json.dumps(out, indent=2))
    print(f"{'key':8s} {'IRR':>6s} {'yld1':>6s} {'yld10':>6s} {'D_A':>6s} {'Deq_y':>6s} {'DrP':>6s} {'DrMR':>6s} {'Dinfl':>6s} {'Derp':>6s} {'minCov':>6s}")
    for r in rows:
        print(f"{r['key']:8s} {r['equity_irr']*100:6.2f} {r['cash_yield_y1']*100:6.2f} {r['cash_yield_avg_y1_10']*100:6.2f} {r['D_asset']:6.2f} {r['D_eq_y']:6.2f} "
              f"{r['D_real_P']:6.2f} {r['D_real_MR']:6.2f} {r['D_infl']:6.2f} {r['D_erp']:6.2f} {r['min_DSCR_or_ICR_20y'] or float('nan'):6.2f}")
    print("\nLocked-tenor sensitivity (fixed share 100%):")
    for r in tenor_tab:
        print(r)
    print("wrote", OUT)


if __name__ == "__main__":
    run()
