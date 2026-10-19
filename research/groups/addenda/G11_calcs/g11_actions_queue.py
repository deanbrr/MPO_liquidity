"""G11 (Real Assets: infrastructure) - Parts C/D: action economics and open-end queue.

SYNTHETIC - NOT ADIC DATA.

Part C: SELL / HOLD / REFINANCE / LEVER for a core-plus infrastructure stake under the main
synthesis rules (one kernel, flat or term-structured liquidity premium l):
   ADD    iff alpha* - l - lamR*m > 0
   REFI   iff l > s + f/T + lamLev + cov
   LEVER  iff ADD and REFI (LEVER = ADD + REFI)
   SELL   iff bid > LAPV(HOLD + best REFI) per $ NAV
LAPV is computed on explicit cash flows (cash yield + terminal value) discounted at r_h + l.
Two input sets: (A) the prior worked example (stream 08 sec. 6.12), (B) G11 evidence-based.

Part D: open-end (evergreen) infrastructure fund redemption queue with Stonepeak-Plus-type
terms (quarterly cap 5% of NAV, pro rata, no automatic carry-over -> ADIC resubmits each
quarter, optional suspension), versus selling the interest on the secondary market.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).with_name("g11_actions_queue_results.json")


# ---------------------------------------------------------------- Part C
def lapv_hold(mu, yc, rh, l_path, T=5):
    """PV per $ NAV of holding T years: annual cash yield yc on growing NAV, exit at NAV_T,
    discounted at rh + l_t (l_path: per-year liquidity premia)."""
    g = mu - yc
    v, df, nav = 0.0, 1.0, 1.0
    for t in range(T):
        df /= (1 + rh + l_path[t])
        v += yc * nav * df
        nav *= (1 + g)
    v += nav * df
    return v


def refi_value(b, s, f, l_path, rh, lamLev, cov, T=5):
    """Value per $ NAV of borrowing b (bullet, T years) at rf+s with upfront fee f;
    cash raised is worth par; debt service discounted on the kernel at rf+l (relative to rf).
    Using spreads over rf (rh and rf cancel to first order): PV = b - sum b*(s)/(1+l)^t ... """
    v, df = b * (1 - f), 1.0
    for t in range(T):
        df /= (1 + l_path[t])
        v -= b * (s + lamLev + cov) * df
    v -= b * df          # principal repaid at T, discounted at l (excess over rf)
    return v


def actions(inp: dict, l_path):
    T = 5
    mu, yc, rh = inp["mu"], inp["yc"], inp["rh"]
    alpha = mu - rh
    hold = lapv_hold(mu, yc, rh, l_path, T)
    ref = refi_value(inp["ltv"], inp["s"], inp["fee"], l_path, rh, inp["lamLev"], inp["cov"], T)
    best_refi = max(ref, 0.0)
    sell = inp["bid"]
    # ADD: buy +x of NAV at par, value = x*(hold - 1) - risk charge
    risk = inp["lamRm"] * sum(1 / (1 + rh + l) ** (t + 1) for t, l in enumerate(l_path[:T]))
    add = inp["add_x"] * (hold - 1.0) - inp["add_x"] * risk
    # LEVER = ADD financed by borrowing add_x on the same terms (identity LEVER = ADD + REFI(add_x))
    ref_add = refi_value(inp["add_x"], inp["s"], inp["fee"], l_path, rh, inp["lamLev"], inp["cov"], T)
    lever = add + ref_add
    # all values per $ of current NAV, relative to HOLD
    vals = {"HOLD": 0.0, "SELL": sell - hold, "REFI": ref, "ADD": add, "LEVER": lever}
    best = max(vals, key=vals.get)
    return {"alpha_star": round(alpha, 4), "LAPV_hold_per_NAV": round(hold, 4), **{k: round(v, 4) for k, v in vals.items()},
            "best": best, "sell_beats_hold_plus_refi": bool(sell > hold + best_refi)}


def region_map(inp: dict):
    rows = []
    for l in np.round(np.arange(0.0, 0.1201, 0.005), 4):
        rows.append({"l": float(l), **actions(inp, [l] * 5)})
    # boundaries
    bounds, prev = [], None
    for r in rows:
        if r["best"] != prev:
            bounds.append({"from_l": r["l"], "best": r["best"]})
            prev = r["best"]
    ts = actions(inp, [0.09, 0.09, 0.04, 0.04, 0.04])
    return {"rows": rows, "boundaries": bounds, "term_structure_9_9_4_4_4": ts}


SET_A = {"label": "A: prior worked example (stream 08 sec 6.12)", "mu": 0.11, "yc": 0.065, "rh": 0.06,
         "ltv": 0.23, "s": 0.025, "fee": 0.0075, "lamLev": 0.0025, "cov": 0.0, "lamRm": 0.0045,
         "bid": 0.91, "add_x": 0.30}
SET_B = {"label": "B: G11 evidence-based core-plus stake", "mu": 0.085, "yc": 0.05, "rh": 0.059,
         "ltv": 0.25, "s": 0.030, "fee": 0.010, "lamLev": 0.0025, "cov": 0.002, "lamRm": 0.0045,
         "bid": 0.91, "add_x": 0.30}
SET_B_STRESS = {**SET_B, "label": "B-stress: same asset, stress bid 0.83 (2020/2022 infra LP pricing), holdco S+450",
                "bid": 0.83, "s": 0.045}


def break_even_sell_vs_borrow(g_fwd_list, d, c, T=5):
    """Risk-neutral shortcut (stream 06): SELL beats HOLD+borrow iff g_fwd < (1+c)(1-d)^(1/T) - 1."""
    gstar = (1 + c) * (1 - d) ** (1 / T) - 1
    return {"d": d, "c": c, "T": T, "g_star": round(gstar, 4),
            "sell_better_for": [g for g in g_fwd_list if g < gstar]}


# ---------------------------------------------------------------- Part D
def queue_sim(others_req, adic_share=0.08, cap=0.05, nq=12, susp_prob=0.0, susp_len=2, nav_drift=0.0,
              npath=20000, seed=7, noise=0.3):
    """Fraction of ADIC's (initial) holding paid out by quarter. ADIC requests its whole remaining
    holding every quarter (no carry-over -> resubmission). Others request others_req[t] of NAV
    (lognormal noise). Pro-rata fill = min(1, cap / total_requests). Optional suspension."""
    rng = np.random.default_rng(seed)
    held = np.ones(npath)                    # ADIC holding in units of initial holding
    paid = np.zeros((npath, nq))
    nav = np.ones(npath)
    susp = np.zeros(npath)
    for t in range(nq):
        nav *= (1 + nav_drift)
        start_s = (susp == 0) & (rng.random(npath) < susp_prob)
        susp[start_s] = susp_len
        req_oth = others_req[min(t, len(others_req) - 1)] * np.exp(noise * rng.standard_normal(npath) - 0.5 * noise ** 2)
        adic_req = adic_share * held          # as share of fund NAV
        tot = req_oth * (1 - adic_share) + adic_req
        fill = np.minimum(1.0, cap / np.maximum(tot, 1e-12))
        fill = np.where(susp > 0, 0.0, fill)
        out_units = held * fill
        paid[:, t] = out_units * nav
        held = held - out_units
        susp = np.maximum(susp - 1, 0)
    cum = paid.cumsum(axis=1)
    return {f"q{h}": {"mean": round(float(cum[:, h - 1].mean()), 3), "p05": round(float(np.quantile(cum[:, h - 1], 0.05)), 3)}
            for h in (1, 2, 4, 8, 12)}


def run():
    res = {"label": "SYNTHETIC - NOT ADIC DATA"}
    res["partC_actions"] = {s["label"]: region_map(s) for s in (SET_A, SET_B, SET_B_STRESS)}
    res["partC_sell_vs_borrow_shortcut"] = {
        "direct stake sell-down at 0.97 vs holdco at SOFR+300 (6.89%)": break_even_sell_vs_borrow([0.04, 0.06, 0.08, 0.10], 0.03, 0.0689),
        "fund LP interest at 0.91 vs holdco/NAV loan at 8.4%": break_even_sell_vs_borrow([0.04, 0.06, 0.08, 0.10], 0.09, 0.084),
        "fund LP interest at 0.83 (stress) vs NAV loan at 9.9%": break_even_sell_vs_borrow([0.04, 0.06, 0.08, 0.10], 0.17, 0.099),
    }
    res["partD_queue"] = {
        "normal: others request 1.5%/q": queue_sim([0.015]),
        "stress: others 8%/q for 6q then 3%": queue_sim([0.08] * 6 + [0.03] * 6, nav_drift=-0.01),
        "severe: others 15%/q for 8q, 25% suspension chance/q (2q)": queue_sim([0.15] * 8 + [0.05] * 4, nav_drift=-0.015, susp_prob=0.25),
        "ADIC is 20% of fund, stress": queue_sim([0.08] * 6 + [0.03] * 6, adic_share=0.20, nav_drift=-0.01),
    }
    OUT.write_text(json.dumps(res, indent=2))
    for lab, rm in res["partC_actions"].items():
        print(lab)
        print("  boundaries:", rm["boundaries"])
        print("  term structure 9/9/4/4/4:", rm["term_structure_9_9_4_4_4"])
        for r in rm["rows"]:
            if r["l"] in (0.0, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10):
                print("   ", {k: r[k] for k in ("l", "alpha_star", "LAPV_hold_per_NAV", "SELL", "REFI", "ADD", "LEVER", "best")})
    print(json.dumps(res["partC_sell_vs_borrow_shortcut"], indent=1))
    print(json.dumps(res["partD_queue"], indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    run()
