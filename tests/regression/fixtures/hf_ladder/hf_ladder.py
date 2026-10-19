"""
gap_01: hedge-fund liquidity-term state machine (G5 sec. 6.5 / GC2 sec. 4.1, verifier corrections applied).

Purpose
    Replace the static hedge-fund haircuts (22% / 50% / 100%) in 00_SYNTHESIS sec. 2.3(d) with a
    time-phased cash ladder from a notice-date queue with gate, suspension, side-pocket and
    liquidation hazards, then recompute survival months on the same named path (C3: demand bust ->
    supply glut -> supply glut, cap draws, exits shut; consumption 25.7 / 18.7 / 18.7 $bn a year).

SYNTHETIC - NOT ADIC DATA.  Every parameter is a G5 sec. 6.5 / 6.11 or GC2 sec. 4.1 synthetic default [I]
unless noted.  Strategy mix = GC2 D20 census v1.0 (multi 30, equity L/S 15, event 10, credit 15,
RV 10, macro 10, systematic trend 10).
Verifier corrections applied:
  * G5 R1   - Form PF buckets are notice capacity, not cash: cash is counted when RECEIVED
              (notice + dealing date + payment lag + holdback + gate state).
  * G5 R8   - notices are irrevocable (no rescission); all notices lodged at t = notice_month.
  * G5 R11  - payout ratio pi = min(1, g NAV / R) applies only when a gate is imposed; quarterly
              others' request rate converted per dealing date.
  * G5 table "gate/suspension probability per quarter" is a COMBINED hazard: split 80% gate /
              20% suspension here (so the sum equals the published row).
  * others' backlog is capped so total requests never exceed 100% of fund NAV.
Assumptions [I]: seasoned book (no lot inside a hard lock-up); payment lag 1 month; 5% holdback
released after 6 months; ADIC share of each fund U(2%, 10%) (G5 C-PM2 cap 10-20%); equity path
-30% over months 1-6 then flat (consistent with the 30% long-only haircut in sec. 2.3(d)); CRIS
hazards for the first two quarters, LATE thereafter (G5 sec. 6.5).

Run:  .venv\\Scripts\\python.exe -I hf_ladder.py   (writes hf_ladder_results.json next to this file)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

SEED = 20261018
N = 20_000            # Monte Carlo paths
T = 36                # months simulated
HF0 = 20.0            # $bn synthetic hedge-fund NAV (context sec. 1A)
N_FUNDS = 40          # GC2 census v1.0
K_MAX = 4             # times an investor can be gated before full payment (G5: 2-4)
LAG = 1               # payment lag, months
HOLDBACK = 0.05       # share of each payment held until audit
HOLDBACK_LAG = 6      # months until the holdback is released
GATE_SHARE = 0.80     # share of the published combined gate/suspension hazard that is a gate
SUSP_SHARE = 0.20     # ... and the share that is a suspension
SUSP_MEAN_Q = 3       # mean suspension length, quarters (G5)
SUSP_TO_LIQ = 0.30    # share of suspensions ending in liquidation [I]
LIQ_SCHED = [(3, 0.50), (12, 0.30), (36, 0.20)]   # G5 sec. 6.5 liquidation cash schedule
LIQ_REC = 0.90        # recovery on liquidation, share of last NAV (G5: 0.85-1.0)
PREEMPT = 0.25        # extra others' requests on the date a fund gates (run on the fund) [I]
SP_P_Q = 0.10         # side-pocket creation per quarter in CRIS (credit/event/RV) (G5)
SP_SIZE = (0.10, 0.30)
SP_PAY_Q = 0.05       # quarterly hazard that a side pocket pays out [I]
SP_REC = 0.80         # recovery on side-pocket payout [I]
RHO_Q = {"CRIS": 0.15, "LATE": 0.04}   # others' requests, share of fund NAV per quarter (G5)

# share, dealing frequency (months), first eligible dealing month after notice at t=0, fund gate g
# (None = no fund-level gate; a gate event then halves the payout), investor gate per dealing date
# (fraction of initial units), combined gate/suspension probability per quarter (CRIS, LATE),
# crisis equity beta, residual vol (annual), side-pocket eligible.   Source: G5 sec. 6.11 / GC2 4.1 [I].
BASE_STRATS = {
    "multi":  dict(share=0.30, freq=3, first=3, g=None, inv_gate=1 / 16, pq=(0.03, 0.002), beta=0.30, sig=0.04, sp=False),
    "eq_ls":  dict(share=0.15, freq=3, first=3, g=0.25, inv_gate=None,   pq=(0.04, 0.004), beta=0.65, sig=0.07, sp=False),
    "event":  dict(share=0.10, freq=3, first=3, g=0.20, inv_gate=None,   pq=(0.10, 0.006), beta=0.75, sig=0.06, sp=True),
    "credit": dict(share=0.15, freq=3, first=3, g=0.15, inv_gate=None,   pq=(0.20, 0.010), beta=0.55, sig=0.06, sp=True),
    "rv":     dict(share=0.10, freq=3, first=3, g=0.25, inv_gate=None,   pq=(0.20, 0.010), beta=0.30, sig=0.04, sp=True),
    "macro":  dict(share=0.10, freq=1, first=1, g=0.25, inv_gate=None,   pq=(0.01, 0.002), beta=0.00, sig=0.07, sp=False),
    "trend":  dict(share=0.10, freq=1, first=1, g=0.25, inv_gate=None,   pq=(0.01, 0.002), beta=-0.20, sig=0.11, sp=False),
}

# 00_SYNTHESIS sec. 2.3(d) named path (C3): demand bust -> supply glut -> supply glut, cap draws, exits shut.
CONS_M = np.r_[np.full(12, 25.7 / 12), np.full(24, 18.7 / 12)]   # $bn consumed per month
TREAS, LO = 15.0, 36.0
FLOOR8 = 14.2                       # 8% IG + cash floor treated as unusable (as in sec. 2.3(d))
FLOOR4 = 0.04 * 177.0               # usable down to 4% of NAV (G7 verifier R2 / GC2 D10 metric)


def eq_path(total_fall: float) -> np.ndarray:
    return np.r_[np.full(6, np.log(1.0 - total_fall) / 6), np.zeros(T - 6)]


REGIME = np.array(["CRIS"] * 6 + ["LATE"] * (T - 6))


def simulate(strats: dict, notice_month: int = 0, pq_mult: float = 1.0, fall: float = 0.30,
             seed: int = SEED) -> np.ndarray:
    """Return an (N, T+40) array of monthly cash received ($bn) from a full redemption of the HF book."""
    rng = np.random.default_rng(seed)
    EQ = eq_path(fall)
    names = list(strats)
    shares = np.array([strats[s]["share"] for s in names])
    shares = shares / shares.sum()
    counts = np.maximum(1, np.round(shares * N_FUNDS).astype(int))
    fund_strat = np.repeat(np.arange(len(names)), counts)
    F = fund_strat.size
    size = np.exp(0.6 * rng.standard_normal(F))      # lognormal sizes (sigma 0.6, G9/GC2)
    for j in range(len(names)):
        m = fund_strat == j
        size[m] *= shares[j] * HF0 / size[m].sum()
    omega = rng.uniform(0.02, 0.10, F)                # ADIC share of each fund

    H = T + 40
    cash = np.zeros((N, H))
    units = np.tile(size, (N, 1))
    init_units = units.copy()
    price = np.ones((N, F))
    sp_val = np.zeros((N, F))
    gated_k = np.zeros((N, F), dtype=int)
    others_backlog = np.zeros((N, F))
    susp_left = np.zeros((N, F), dtype=int)
    liquidating = np.zeros((N, F), dtype=bool)

    par = {k: np.array([strats[names[j]][k] for j in fund_strat]) for k in ("freq", "first", "beta", "sig")}
    g_arr = np.array([np.nan if strats[names[j]]["g"] is None else strats[names[j]]["g"] for j in fund_strat])
    invg = np.array([np.nan if strats[names[j]]["inv_gate"] is None else strats[names[j]]["inv_gate"] for j in fund_strat])
    sp_ok = np.array([strats[names[j]]["sp"] for j in fund_strat])
    pq_cris = np.minimum(0.40, pq_mult * np.array([strats[names[j]]["pq"][0] for j in fund_strat]))
    pq_late = np.array([strats[names[j]]["pq"][1] for j in fund_strat])

    for t in range(1, T + 1):
        reg = REGIME[t - 1]
        r = (par["beta"] * EQ[t - 1] + par["sig"] / np.sqrt(12) * rng.standard_normal((N, F))
             - 0.5 * par["sig"] ** 2 / 12)
        price *= np.exp(r)
        dealing = (t % par["freq"] == 0)
        eligible = dealing & (t >= notice_month + par["first"])
        pq = pq_cris if reg == "CRIS" else pq_late
        p_date = 1 - (1 - pq) ** (par["freq"] / 3)             # combined hazard per dealing date
        # side pockets (quarterly; created in CRIS for eligible strategies; paid out at a hazard)
        if t % 3 == 0:
            if reg == "CRIS":
                hit = (rng.random((N, F)) < SP_P_Q) & sp_ok & ~liquidating
                frac = rng.uniform(*SP_SIZE, (N, F)) * hit
                sp_val += frac * units * price
                units *= 1 - frac
            pay = (rng.random((N, F)) < SP_PAY_Q) & (sp_val > 0)
            cash[:, t + LAG] += (pay * sp_val * SP_REC).sum(axis=1)
            sp_val[pay] = 0.0
        # suspension dynamics
        active = susp_left > 0
        susp_left[active] -= 1
        ending = active & (susp_left == 0)
        to_liq = ending & (rng.random((N, F)) < SUSP_TO_LIQ)
        if to_liq.any():
            val = units * price * LIQ_REC * to_liq
            for dm, w in LIQ_SCHED:
                if t + dm < H:
                    cash[:, t + dm] += (w * val).sum(axis=1)
            units[to_liq] = 0.0
            liquidating |= to_liq
        new_susp = (eligible & (susp_left == 0) & ~ending & ~liquidating
                    & (rng.random((N, F)) < SUSP_SHARE * p_date))
        dur_q = rng.geometric(1 / SUSP_MEAN_Q, (N, F))
        susp_left = np.where(new_susp, 3 * dur_q, susp_left)
        # dealing: ADIC requests all remaining units (irrevocable full redemption)
        can = eligible & (susp_left == 0) & ~liquidating & (units > 1e-12)
        if can.any():
            req = units.copy()
            cap = np.where(np.isnan(invg), np.inf, invg * init_units)   # investor-level gate
            req = np.minimum(req, cap)
            gate_evt = rng.random((N, F)) < GATE_SHARE * p_date
            rho = RHO_Q[reg] * par["freq"] / 3
            adic_frac = omega * (req / np.maximum(init_units, 1e-12))
            others = np.minimum(rho + others_backlog + PREEMPT * gate_evt, 1.0 - adic_frac)
            R = adic_frac + others
            g_eff = np.where(np.isnan(g_arr), 0.5 * R, g_arr)            # no fund gate: a gate halves payout
            pi = np.where(gate_evt, np.minimum(1.0, g_eff / np.maximum(R, 1e-12)), 1.0)
            pi = np.where(gated_k >= K_MAX, 1.0, pi)
            gated_k += (gate_evt & (pi < 1.0) & can).astype(int)
            others_backlog = np.where(can, others * (1 - pi), others_backlog)
            paid_units = np.where(can, req * pi, 0.0)
            val = paid_units * price
            cash[:, t + LAG] += ((1 - HOLDBACK) * val).sum(axis=1)
            cash[:, t + HOLDBACK_LAG] += (HOLDBACK * val).sum(axis=1)
            units -= paid_units
        if reg == "LATE":
            others_backlog *= 0.5          # backlog decays once the crisis passes [I]
    return cash


def ladder(cash: np.ndarray, months=(1, 3, 6, 12, 24, 36)) -> dict:
    cum = np.cumsum(cash, axis=1)
    out = {}
    for m in months:
        x = cum[:, m] / HF0
        out[f"m{m}"] = {"mean": round(float(x.mean()), 4), "p50": round(float(np.median(x)), 4),
                        "p10": round(float(np.quantile(x, 0.10)), 4), "p5": round(float(np.quantile(x, 0.05)), 4),
                        "p1": round(float(np.quantile(x, 0.01)), 4)}
    return out


def survival(cash: np.ndarray, floor: float, extra_static: float = 0.0, extra_cons: np.ndarray | None = None) -> dict:
    """Fractional months until cumulative consumption exceeds usable liquidity plus HF cash received.

    Usable static liquidity = Treasury at a 5% haircut + long-only at a 30% haircut - floor (as sec. 2.3(d)).
    HF cash received by end of month k is added; consumption is linear within a month.
    """
    cons = CONS_M.copy() if extra_cons is None else CONS_M + extra_cons
    usable0 = TREAS * 0.95 + LO * 0.70 - floor - extra_static
    cum_hf = np.cumsum(cash[:, : T + 1], axis=1)              # index k = cash received by end of month k
    cum_c = np.r_[0.0, np.cumsum(cons)]                         # consumed by end of month k
    surplus = usable0 + cum_hf - cum_c[None, :]                 # (N, T+1); k = 0..T
    neg = surplus[:, 1:] < 0
    first = np.where(neg.any(axis=1), neg.argmax(axis=1) + 1, T + 1)   # first month-end in deficit
    months = np.full(N, float(T) + 1.0)
    hit = first <= T
    k = first[hit]
    s_prev = surplus[hit, k - 1] + 0.0
    # HF cash for month k arrives at month-end; consumption is spread within the month.
    s_prev_no_cash = s_prev
    months[hit] = (k - 1) + np.clip(s_prev_no_cash / cons[k - 1], 0.0, 1.0)
    q = {name: round(float(np.quantile(months, val)), 1) for name, val in
         (("p50", 0.5), ("p10", 0.10), ("p5", 0.05), ("p1", 0.01))}
    q["share_gt36"] = round(float((months > T).mean()), 4)
    q["usable_static_bn"] = round(usable0, 2)
    return q


def static_months(usable: float, cons: np.ndarray = CONS_M) -> float:
    cum_c = np.cumsum(cons)
    i = int(np.searchsorted(cum_c, usable))
    if i >= T:
        return float("inf")
    prev = cum_c[i - 1] if i > 0 else 0.0
    return i + (usable - prev) / cons[i]


def main() -> None:
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "seed": SEED, "paths": N,
           "static_reference_months": {
               "hf_gated_100pct": round(static_months(TREAS * 0.95 + LO * 0.70 - FLOOR8), 1),
               "hf_50pct": round(static_months(TREAS * 0.95 + LO * 0.70 + 0.5 * HF0 - FLOOR8), 1),
               "blended_22pct": round(static_months(0.78 * 71.0 - FLOOR8), 1),
               "hf_gated_100pct_floor4": round(static_months(TREAS * 0.95 + LO * 0.70 - FLOOR4), 1),
               "hf_50pct_floor4": round(static_months(TREAS * 0.95 + LO * 0.70 + 0.5 * HF0 - FLOOR4), 1)}}
    multi_heavy = {**BASE_STRATS,
                   "multi": {**BASE_STRATS["multi"], "share": 0.55},
                   "eq_ls": {**BASE_STRATS["eq_ls"], "share": 0.10},
                   "event": {**BASE_STRATS["event"], "share": 0.05},
                   "credit": {**BASE_STRATS["credit"], "share": 0.10},
                   "rv": {**BASE_STRATS["rv"], "share": 0.05},
                   "macro": {**BASE_STRATS["macro"], "share": 0.10},
                   "trend": {**BASE_STRATS["trend"], "share": 0.05}}
    # Reverse-stress terms [I]: what ADIC's documents would have to look like for the static
    # "all gated" 12-month case to become plausible.  Multi-strategy investor gate 1/20; credit, event
    # and RV semi-annual dealing (first date month 6) with 25%-a-date investor gates; equity L/S
    # investor gate 25%; combined gate/suspension hazards doubled.
    adverse = {**BASE_STRATS,
               "multi": {**BASE_STRATS["multi"], "inv_gate": 1 / 20},
               "eq_ls": {**BASE_STRATS["eq_ls"], "inv_gate": 0.25},
               "event": {**BASE_STRATS["event"], "freq": 6, "first": 6, "inv_gate": 0.25},
               "credit": {**BASE_STRATS["credit"], "freq": 6, "first": 6, "inv_gate": 0.25},
               "rv": {**BASE_STRATS["rv"], "freq": 6, "first": 6, "inv_gate": 0.25}}
    runs = {
        "base": dict(strats=BASE_STRATS),
        "adverse_terms_gate_x2": dict(strats=adverse, pq_mult=2.0),
        "gate_x2": dict(strats=BASE_STRATS, pq_mult=2.0),
        "gate_x0.5": dict(strats=BASE_STRATS, pq_mult=0.5),
        "equity_minus40": dict(strats=BASE_STRATS, fall=0.40),
        "multi_heavy": dict(strats=multi_heavy),
        "notice_at_m6": dict(strats=BASE_STRATS, notice_month=6),
    }
    for name, kw in runs.items():
        c = simulate(kw["strats"], notice_month=kw.get("notice_month", 0), pq_mult=kw.get("pq_mult", 1.0),
                     fall=kw.get("fall", 0.30))
        res[name] = {"cash_share_of_initial_hf_nav": ladder(c),
                     "survival_floor8": survival(c, FLOOR8),
                     "survival_floor4": survival(c, FLOOR4)}
        if name in ("base", "equity_minus40", "adverse_terms_gate_x2"):
            cum = np.cumsum(c, axis=1)[:, 1: T + 1] / HF0          # cash share received by end of month 1..T
            res[name]["phi_monthly_p5"] = [round(float(v), 4) for v in np.quantile(cum, 0.05, axis=0)]
            res[name]["phi_monthly_p50"] = [round(float(v), 4) for v in np.quantile(cum, 0.50, axis=0)]
        if name == "base":
            # Press-reported HF-TRS sleeve (Hedgeweek, 12 Jun 2026, citing Bloomberg: up to $15bn,
            # UNDER CONSIDERATION; TRS with local banks on mainly large multi-strategy funds).
            # Modelled [I]: independent amount 10% of notional posted at inception (encumbered);
            # VM on reference-NAV moves with multi-strategy crisis beta 0.30 during the equity fall;
            # the sleeve adds no redemption liquidity (ADIC owns no units).
            n_trs, ia, beta = 15.0, 0.10, 0.30
            eqp = eq_path(0.30)
            vm = np.r_[n_trs * beta * (1 - np.exp(eqp[:6])), np.zeros(T - 6)]
            res["base_plus_hf_trs_15bn"] = {"survival_floor8": survival(c, FLOOR8, extra_static=ia * n_trs, extra_cons=vm),
                                            "survival_floor4": survival(c, FLOOR4, extra_static=ia * n_trs, extra_cons=vm),
                                            "vm_outflow_bn": round(float(vm.sum()), 2), "ia_bn": ia * n_trs}
    out = Path(__file__).with_name("hf_ladder_results.json")
    out.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
