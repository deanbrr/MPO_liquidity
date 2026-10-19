"""
gap_02: penalty-pinned duals, Phase-I feasibility restoration and the decision-card guard.
SYNTHETIC - NOT ADIC DATA.

A one-row-per-constraint linearisation of the H program's t0 liquidity block. The T4 row's coefficients are
finite differences of the deterministic ladder (t1_engine.ladder) on the synthetic book, so the LP is a faithful
local model of the named-stress row. Lever costs are design assumptions [I] stated below.

Cases, for each reading of the named stress
 1. ELASTIC: Mode B, elastic rows at the report's penalty tiers (synthesis s4.8). If the row cannot be met inside
    T5 and lever capacities, its dual is pinned at M_S = 1e2 and every SELL card says "sell at almost any bid".
 2. PHASE I: lexicographic minimisation of violations subject to all non-relaxable rows -> u*.
 3. RESTORED: the violated row's RHS relaxed by u* (a recovery target), no slack in pricing rows; duals are the
    marginal cost of the marginal lever -> finite reservation prices; invariant to the penalty scale.
 4. MODE H: as 3, with the owner-agreed band available.
"""
from __future__ import annotations

import json
import os
import sys

import cvxpy as cp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import t1_engine as E  # noqa: E402
from gap02_study import s_star, t4_literal  # noqa: E402

M_TIERS = {"M": 1e4, "crit": 1e3, "S": 1e2, "red": 50.0, "IG": 10.0}   # synthesis s4.8 penalty tiers
# lever capacities [A/I]: RCF market capacity anchored on a large sovereign RCF (PIF $15bn, Aug 2024)
CAP = dict(rcf=15.0, reserve=0.06 * E.NAV0, amber=6.0, pace=6.0, band=1.0)
COST = dict(rcf=0.0090,      # PV $ per $ committed: 15bp undrawn x 5y + 15bp upfront
            reserve=0.075,   # per $ of reserve: 1.5%/yr buffer carry x 5y (GC2 D17 default)
            amber=0.21,      # per $ sold: 11% discount (Jefferies H1-2026 credit 89%) + 2%/yr lost carry x 5y
            pace=0.16,       # per $bn/yr of base pacing cut held for 2 years: 8% per $ forgone (G1) x 2
            band=0.065)      # per $ withheld: (10% - ~7%) accrual for ~1.5y + 2% fiscal-stress premium
IG_SHORT_T0 = 0.08 * E.NAV0 - (E.TRE0 - E.IM_N * E.N_SYN0 - E.OPP_IM0)   # T2 at t0 excluding encumbered IM
TEST_FUNDS = [dict(name="2018 buyout fund (report s4.4 example)", nav=0.5, bid=0.88, hold=0.95),
              dict(name="late-life buyout fund", nav=0.5, bid=0.80, hold=0.95),
              dict(name="tail-end fund", nav=0.5, bid=0.70, hold=0.95)]


def t4_coefficients(stress: E.Stress) -> dict:
    """Finite-difference slopes of the stress headroom (min over 24 months, $bn) per unit of each lever."""
    h0 = E.ladder(stress, E.Policy("A"))["min_head_tpf_24"]
    d = {"rcf": (E.ladder(stress, E.Policy("x", rcf=5.0))["min_head_tpf_24"] - h0) / 5.0}
    r0 = E.ladder(stress, E.Policy("x", reserve=0.08))["min_head_tpf_24"]
    d["reserve"] = (E.ladder(stress, E.Policy("x", reserve=0.08 + 5.0 / E.NAV0))["min_head_tpf_24"] - r0) / 5.0
    d["amber"] = (E.ladder(stress, E.Policy("x", amber_t0=3.0))["min_head_tpf_24"] - h0) / 3.0
    d["pace"] = (E.ladder(stress, E.Policy("x", pace=9.0))["min_head_tpf_24"] - h0) / 3.0
    d["band"] = E.ladder(stress, E.Policy("x", band=True))["min_head_tpf_24"] - h0
    return dict(h0=h0, slope=d)


def _model(coef, mode_h, elastic, relax, penalty_scale, ig_short):
    x = {k: cp.Variable(nonneg=True, name=k) for k in CAP}
    s = cp.Variable(len(TEST_FUNDS), nonneg=True, name="sell")
    uS = cp.Variable(nonneg=True, name="u_S")
    uIG = cp.Variable(nonneg=True, name="u_IG")
    bid = np.array([f["bid"] for f in TEST_FUNDS])
    hold = np.array([f["hold"] for f in TEST_FUNDS])
    navs = np.array([f["nav"] for f in TEST_FUNDS])
    sl = coef["slope"]
    t4 = coef["h0"] + sum(sl[k] * x[k] for k in CAP) + bid @ s
    ig = bid @ s + x["reserve"] + 0.89 * x["amber"]
    c_t4 = (t4 + uS >= -relax[0]) if elastic else (t4 >= -relax[0])
    c_ig = (ig + uIG >= ig_short - relax[1]) if elastic else (ig >= ig_short - relax[1])
    cons = [c_t4, c_ig, s <= navs] + [x[k] <= (CAP[k] if (k != "band" or mode_h) else 0.0) for k in CAP]
    cost = (COST["rcf"] * x["rcf"] + COST["reserve"] * x["reserve"] + COST["amber"] * x["amber"]
            + COST["pace"] * x["pace"] + COST["band"] * max(sl["band"], 1e-9) * x["band"])
    obj = (bid - hold) @ s - cost
    if elastic:
        obj = obj - penalty_scale * (M_TIERS["S"] * uS + M_TIERS["IG"] * uIG)
    return cp.Problem(cp.Maximize(obj), cons), x, s, uS, uIG, c_t4, c_ig


def solve(coef: dict, mode_h: bool, elastic: bool, relax=(0.0, 0.0), penalty_scale: float = 1.0,
          ig_short: float = IG_SHORT_T0) -> dict:
    prob, x, s, uS, uIG, c_t4, c_ig = _model(coef, mode_h, elastic, relax, penalty_scale, ig_short)
    prob.solve(solver=cp.HIGHS)
    sol = dict(status=prob.status, obj=float(prob.value),
               duals=dict(T4=float(c_t4.dual_value), IG=float(c_ig.dual_value)),
               x={k: float(v.value) for k, v in x.items()}, sell=[float(v) for v in s.value],
               u_S=float(uS.value) if elastic else 0.0, u_IG=float(uIG.value) if elastic else 0.0,
               penalty_scale=penalty_scale, relax=list(relax), elastic=elastic)
    sol["cards"] = decision_cards(sol)
    return sol


def phase1(coef: dict, mode_h: bool, ig_short: float = IG_SHORT_T0) -> dict:
    """Lexicographic Phase I (tier order: T4 at M_S, then IG at M_IG), all other rows non-relaxable.
    Only reversible, non-red recovery levers enter Phase I; red-tier (PE) sales are excluded so that the
    structural deficit u* never presumes a fire sale. They re-enter in Phase II at the restored prices."""
    x = {k: cp.Variable(nonneg=True) for k in CAP}
    s = cp.Variable(len(TEST_FUNDS), nonneg=True)
    uS = cp.Variable(nonneg=True)
    uIG = cp.Variable(nonneg=True)
    bid = np.array([f["bid"] for f in TEST_FUNDS])
    sl = coef["slope"]
    cons = [coef["h0"] + sum(sl[k] * x[k] for k in CAP) + bid @ s + uS >= 0,
            bid @ s + x["reserve"] + 0.89 * x["amber"] + uIG >= ig_short, s == 0]
    cons += [x[k] <= (CAP[k] if (k != "band" or mode_h) else 0.0) for k in CAP]
    cp.Problem(cp.Minimize(uS), cons).solve(solver=cp.HIGHS)
    u_s = max(0.0, float(uS.value))
    cp.Problem(cp.Minimize(uIG), cons + [uS <= u_s + 1e-9]).solve(solver=cp.HIGHS)
    u_ig = max(0.0, float(uIG.value))
    at_cap = [k for k in CAP if sl[k] > 0 and (k != "band" or mode_h) and abs(float(x[k].value) - CAP[k]) < 1e-6]
    return dict(u_S_star=u_s, u_IG_star=u_ig, levers={k: float(v.value) for k, v in x.items()},
                iis=(["T4 row"] + [f"cap:{k}" for k in at_cap] + (["Mode B (no band)"] if not mode_h else [])
                     if u_s > 1e-9 else []))


def decision_cards(sol: dict) -> list:
    """Reservation price implied by the cash-row duals: SELL iff bid x (1 + y) >= hold,
    y = shadow value of $1 of cash today in the pricing rows (T4 + IG, coefficient 1 on sale proceeds)."""
    y = sol["duals"]["T4"] + sol["duals"]["IG"]
    return [dict(fund=f["name"], bid=f["bid"], hold=f["hold"], y_cash=y, reservation_price=f["hold"] / (1 + y),
                 action="SELL" if sv > 1e-9 else "HOLD") for f, sv in zip(TEST_FUNDS, sol["sell"])]


def pinned_rows(sol: dict, tol: float = 1e-3) -> list:
    """Rows whose elastic slack is positive or whose dual sits within tol of its (scaled) penalty tier."""
    bad = []
    sc = sol["penalty_scale"]
    if sol["u_S"] > 1e-7 or sol["duals"]["T4"] >= (1 - tol) * M_TIERS["S"] * sc:
        bad.append("T4")
    if sol["u_IG"] > 1e-7 or sol["duals"]["IG"] >= (1 - tol) * M_TIERS["IG"] * sc:
        bad.append("IG")
    return bad


def assert_no_penalty_pinned_duals(sol: dict, tol: float = 1e-3) -> None:
    bad = pinned_rows(sol, tol)
    if bad:
        raise AssertionError(f"decision cards priced off penalty-pinned rows: {bad}")


def restore_and_solve(coef: dict, mode_h: bool) -> dict:
    p1 = phase1(coef, mode_h)
    relax = (p1["u_S_star"] + 1e-6 if p1["u_S_star"] > 0 else 0.0, p1["u_IG_star"] + 1e-6 if p1["u_IG_star"] > 0 else 0.0)
    hard = solve(coef, mode_h, elastic=False, relax=relax)
    el1 = solve(coef, mode_h, elastic=True, relax=relax, penalty_scale=1.0)
    el10 = solve(coef, mode_h, elastic=True, relax=relax, penalty_scale=10.0)
    return dict(phase1=p1, restored=hard, restored_elastic_x1=el1, restored_elastic_x10=el10,
                cushion_on_glide_path=(coef["h0"] + sum(coef["slope"][k] * hard["x"][k] for k in CAP)
                                       + sum(f["bid"] * v for f, v in zip(TEST_FUNDS, hard["sell"]))
                                       + relax[0]) / E.NAV0)


def run(theta_star: float = 0.76) -> dict:
    out = {"note": "SYNTHETIC - NOT ADIC DATA; linearised H liquidity block; lever costs [I]",
           "ig_short_t0": IG_SHORT_T0, "caps": CAP, "costs": COST}
    readings = {
        "T4_as_written": t4_literal(floor=0.08),                      # synthesis s4.9 T2 8% hard, 50% credit
        "T4_critic_reading": t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0)),
        "s_star_canonical": s_star(theta_star),
    }
    for key, st in readings.items():
        coef = t4_coefficients(st)
        blk = dict(stress=st.name, coef=coef)
        blk["case1_elastic_modeB"] = solve(coef, mode_h=False, elastic=True)
        blk["case1_pinned_rows"] = pinned_rows(blk["case1_elastic_modeB"])
        blk["case1_dual_T4_penalty_x10"] = solve(coef, False, True, penalty_scale=10.0)["duals"]["T4"]
        blk["modeB"] = restore_and_solve(coef, mode_h=False)
        blk["modeH"] = restore_and_solve(coef, mode_h=True)
        out[key] = blk
    return out


if __name__ == "__main__":
    th = float(sys.argv[1]) if len(sys.argv) > 1 else 0.76
    res = run(th)
    with open(os.path.join(HERE, "phase1_demo_results.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=float)
    for key in ("T4_as_written", "T4_critic_reading", "s_star_canonical"):
        b = res[key]
        c1 = b["case1_elastic_modeB"]
        print(f"== {key}: h0={b['coef']['h0']:.2f} slopes={ {k: round(v, 3) for k, v in b['coef']['slope'].items()} }")
        print(f"   case1 elastic: u_S={c1['u_S']:.2f} y_T4={c1['duals']['T4']:.3f} (x10 -> {b['case1_dual_T4_penalty_x10']:.3f}) "
              f"pinned={b['case1_pinned_rows']} levers={ {k: round(v, 2) for k, v in c1['x'].items()} } "
              f"cards={[ (c['bid'], round(c['reservation_price'], 3), c['action']) for c in c1['cards']]}")
        for mode in ("modeB", "modeH"):
            r = b[mode]
            h = r["restored"]
            print(f"   {mode}: u*={r['phase1']['u_S_star']:.2f} iis={r['phase1']['iis']} y_T4={h['duals']['T4']:.3f} "
                  f"y_IG={h['duals']['IG']:.3f} x10={r['restored_elastic_x10']['duals']['T4']:.3f} "
                  f"levers={ {k: round(v, 2) for k, v in h['x'].items()} } cushion={r['cushion_on_glide_path']:.4f} "
                  f"cards={[ (c['bid'], round(c['reservation_price'], 3), c['action']) for c in h['cards']]}")
