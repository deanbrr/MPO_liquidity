"""
gap_02 frontier: joint feasibility, certainty-equivalent price of safety, frontier and 50k certification.
SYNTHETIC - NOT ADIC DATA. Reads gap02_grid_raw.json (written by gap02_study.py).

Cost measures (bp of NAV per year, averaged over the models in scope)
- CE price  = annualised CRRA(3) certainty-equivalent growth of distribution-inclusive wealth of the CE-best mix
              in the grid (same band permission, no Tier-1 gates) minus that of the mix, plus outside-NAV costs.
              This is the 'price of safety' of synthesis s4.11: what the gates cost relative to the best policy
              without them.
- CE vs do-nothing = the same against the do-nothing reference (negative = the mix improves CE).
- Premium   = expected gross outlay: facility fees and interest, reserve carry (extra reserve x model ERP),
              pre-emptive amber-sale discount, pacing beyond-horizon cost, owner cost of band use.
Outside-NAV costs: owner fiscal-stress premium KAPPA_OWN per $ withheld (the 10% accrual is inside W~), pacing
beyond-horizon C_PACE_TV per $ of commitments forgone, relationship cost KAPPA_GP per $ of red sale.
"""
from __future__ import annotations

import json
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import t1_engine as E  # noqa: E402
from gap02_study import C_PACE_TV, KAPPA_GP, KAPPA_OWN, N_CERT, run_policy  # noqa: E402

SCOPES = {"all6": ["M1", "M2", "M3", "M4", "M5", "M6"], "M1-M5": ["M1", "M2", "M3", "M4", "M5"],
          "M1-M3": ["M1", "M2", "M3"]}
EPS = (0.0025, 0.005, 0.0075, 0.01, 0.015, 0.02, 0.025, 0.03, 0.05, 0.075, 0.10)
THETA_KEYS = ("0.42", "0.76", "1.00")
OWNER_PREMIUM = 0.065      # per $ withheld: (10% - ~7%) accrual for ~1.5y + 2% fiscal-stress premium [I]


def erp(mk):
    m = E.MODELS[mk]
    return math.log1p(m.eq_g) + 0.5 * 0.165 ** 2 - m.cash_lr


def g_ce(row, models):
    return E.ce_growth({k: row["models"][k]["w_inv2"] for k in models})


def outside_bp(row, models):
    return float(np.mean([(KAPPA_OWN * row["models"][k]["mean_withheld"]
                           + C_PACE_TV[k] * row["models"][k]["mean_commit_forgone"]
                           + KAPPA_GP * row["models"][k]["mean_red_sales"]) / E.NAV0 / 5 * 1e4 for k in models]))


def premium_bp(row, models):
    kw = row["kw"]
    out = {}
    out["fees_interest"] = float(np.mean([(row["models"][k]["mean_fees"] + row["models"][k]["mean_interest"])
                                          / E.NAV0 / 5 * 1e4 for k in models]))
    extra_res = max(0.0, kw["reserve"] - 0.0768)      # t0 usable Treasury is 7.68% of NAV
    out["reserve_carry"] = float(np.mean([extra_res * erp(k) * 1e4 for k in models]))
    out["amber_t0_discount"] = kw["amber_t0"] * (1 - (0.89 * 14 + 0.85 * 8) / 22) / E.NAV0 / 5 * 1e4
    out["pacing_tv"] = float(np.mean([C_PACE_TV[k] * row["models"][k]["mean_commit_forgone"] / E.NAV0 / 5 * 1e4
                                      for k in models]))
    out["owner"] = float(np.mean([OWNER_PREMIUM * row["models"][k]["mean_withheld"] / E.NAV0 / 5 * 1e4
                                  for k in models]))
    out["total"] = sum(out.values())
    return out


def feasible(row, eps, scope, theta_key, need_t4=True):
    models = SCOPES.get(scope, SCOPES["all6"])
    m = row["models"]
    if scope == "mixture":
        ok_red = np.mean([m[k]["p_red"] for k in models]) <= eps
    else:
        ok_red = all(m[k]["p_red"] <= eps for k in models)
    checks = dict(
        T6=ok_red,
        T7=all(m[k]["cp_upper_black_12m"] <= 0.025 for k in models),
        T9=all(m[k]["p_navf_trig_12m"] <= 0.02 and m[k]["p_covenant"] <= 0.01 for k in models),
        # T5 is enforced at decision time inside the engine (no draws above 15% of current NAV, pledges
        # capped); passive drift from NAV falls is monitored, not gated: allow p99 up to the 20% encumbrance
        # hard limit and leave covenant risk to T9.
        T5=all(m[k]["max_enc_p99"] <= 0.20 for k in models),
        T8=all(v >= 1.0 for v in row["dcr"].values()),
        T3=row["lcr30"] >= 1.0,
        T4=(row["ladder_head"][theta_key] >= 0) if need_t4 else True,
    )
    return all(checks.values()), checks


def main():
    raw = json.load(open(os.path.join(HERE, "gap02_grid_raw.json")))
    rows = raw["grid"]
    by = {r["kw"]["name"]: r for r in rows}
    ref = by[raw["reference"]]
    res = dict(note=raw["note"], calibration=raw["calibration"], n_screen=raw["n_screen"])

    # lever-by-lever table (single levers on top of do-nothing), all six models and M1-M5
    single = {}
    for nm in ("R0_N0_P12_B0_Q8_A0_H0", "R5_N0_P12_B0_Q8_A0_H0", "R10_N0_P12_B0_Q8_A0_H0", "R15_N0_P12_B0_Q8_A0_H0",
               "R0_N2_P12_B0_Q8_A0_H0", "R0_N0_P9_B0_Q8_A0_H0", "R0_N0_P12c_B0_Q8_A0_H0", "R0_N0_P6c_B0_Q8_A0_H0",
               "R0_N0_P12_B1_Q8_A0_H0", "R0_N0_P12_B0_Q12_A0_H0", "R0_N0_P12_B0_Q14_A0_H0",
               "R0_N0_P12_B0_Q8_A6_H0", "R0_N0_P12_B0_Q8_A0_H5"):
        r = by[nm]
        single[nm] = dict(p_red={k: r["models"][k]["p_red"] for k in r["models"]},
                          ce_vs_ref_all6=(g_ce(ref, SCOPES["all6"]) - g_ce(r, SCOPES["all6"])) * 1e4 + outside_bp(r, SCOPES["all6"]),
                          ce_vs_ref_m15=(g_ce(ref, SCOPES["M1-M5"]) - g_ce(r, SCOPES["M1-M5"])) * 1e4 + outside_bp(r, SCOPES["M1-M5"]),
                          premium_all6=premium_bp(r, SCOPES["all6"]),
                          heads={k: r["ladder_head"][k] for k in ("0.42", "0.76", "1.00")},
                          t4_as_written=r["t4_as_written_head"], t4_critic=r["t4_critic_head"],
                          dcr=r["dcr"], lcr30=r["lcr30"])
    res["single_levers"] = single

    frontier = {}
    best_ce = {}
    for band_ok in (False, True):
        for scope in ("all6", "M1-M5", "M1-M3", "mixture"):
            models = SCOPES.get(scope, SCOPES["all6"])
            pool = [r for r in rows if band_ok or not r["kw"]["band"]]
            g_best_row = max(pool, key=lambda r: g_ce(r, models) * 1e4 - outside_bp(r, models))
            g_best = g_ce(g_best_row, models) * 1e4 - outside_bp(g_best_row, models)
            best_ce[f"band={band_ok}|scope={scope}"] = dict(mix=g_best_row["kw"]["name"],
                                                            p_red={k: g_best_row["models"][k]["p_red"] for k in models})
            for th in THETA_KEYS:
                pts = []
                for eps in EPS:
                    cands = []
                    for r in pool:
                        ok, _ = feasible(r, eps, scope, th)
                        if ok:
                            cands.append(r)
                    if not cands:
                        # best achievable red-event level under the other gates, for the record
                        others = [r for r in pool if all(v for kk, v in feasible(r, 1.0, scope, th)[1].items())]
                        if scope == "mixture":
                            best_eps = min((np.mean([r["models"][k]["p_red"] for k in models]) for r in others), default=None)
                        else:
                            best_eps = min((max(r["models"][k]["p_red"] for k in models) for r in others), default=None)
                        pts.append(dict(eps=eps, feasible=False, best_achievable=best_eps))
                        continue
                    best = min(cands, key=lambda r: g_best - (g_ce(r, models) * 1e4 - outside_bp(r, models)))
                    price = g_best - (g_ce(best, models) * 1e4 - outside_bp(best, models))
                    vs_ref = (g_ce(ref, models) - g_ce(best, models)) * 1e4 + outside_bp(best, models) - outside_bp(ref, models)
                    pts.append(dict(eps=eps, feasible=True, mix=best["kw"]["name"], kw=best["kw"],
                                    ce_price=price, ce_vs_ref=vs_ref, premium=premium_bp(best, models),
                                    p_red={k: best["models"][k]["p_red"] for k in models},
                                    p_band12={k: best["models"][k]["p_band_12m"] for k in models},
                                    t4_head=best["ladder_head"][th]))
                frontier[f"band={band_ok}|scope={scope}|theta={th}"] = pts
    res["best_ce_unconstrained"] = best_ce
    res["frontier"] = frontier

    # ---------------- certification at 50k paths per model
    chosen = {raw["reference"]: by[raw["reference"]]["kw"]}
    for key, pts in frontier.items():
        if "|theta=0.76" not in key:
            continue
        for p in pts:
            if p["feasible"] and p["eps"] in (0.005, 0.01, 0.02, 0.03, 0.05):
                chosen[p["mix"]] = p["kw"]
    for key, v in best_ce.items():
        chosen[v["mix"]] = by[v["mix"]]["kw"]
    with ProcessPoolExecutor(max_workers=min(20, len(chosen))) as ex:
        out_c = list(ex.map(run_policy, [(kw, N_CERT) for kw in chosen.values()]))
    cert = {}
    ref_c = [r for kw, r in out_c if kw["name"] == raw["reference"]][0]
    for kw, r in out_c:
        row = dict(kw=kw, models=r)
        cert[kw["name"]] = dict(
            kw=kw, p_red={k: r[k]["p_red"] for k in r}, cp_red={k: r[k]["cp_upper_red"] for k in r},
            cp_black12={k: r[k]["cp_upper_black_12m"] for k in r}, p_band12={k: r[k]["p_band_12m"] for k in r},
            debt_p99={k: r[k]["max_debt_ratio_p99"] for k in r}, p_debt10={k: r[k]["p_debt_gt10"] for k in r},
            p_cov={k: r[k]["p_covenant"] for k in r}, p_floor4={k: r[k]["p_floor4_breach"] for k in r},
            p_restore_fail={k: r[k]["p_restore_fail"] for k in r}, median_first_red={k: r[k]["median_first_red"] for k in r},
            mean_red_loss={k: r[k]["mean_red_loss"] for k in r}, mean_withheld={k: r[k]["mean_withheld"] for k in r},
            ce_vs_ref_all6=(g_ce(dict(models=ref_c), SCOPES["all6"]) - g_ce(row, SCOPES["all6"])) * 1e4
            + outside_bp(row, SCOPES["all6"]) - outside_bp(dict(models=ref_c), SCOPES["all6"]),
            ce_vs_ref_m15=(g_ce(dict(models=ref_c), SCOPES["M1-M5"]) - g_ce(row, SCOPES["M1-M5"])) * 1e4
            + outside_bp(row, SCOPES["M1-M5"]) - outside_bp(dict(models=ref_c), SCOPES["M1-M5"]),
            premium_all6=premium_bp(row, SCOPES["all6"]), premium_m15=premium_bp(row, SCOPES["M1-M5"]))
    res["certified_50k"] = cert
    with open(os.path.join(HERE, "gap02_results.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=float)
    print("wrote gap02_results.json;", len(cert), "certified mixes")


if __name__ == "__main__":
    main()
