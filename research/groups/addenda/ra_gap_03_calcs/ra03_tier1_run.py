"""RA gap 03, step 3 runner: marginal Tier-1 (G*, P(red)) and Tier-2 (CE) cost per barrel; lambda-weighted H_j.

SYNTHETIC - NOT ADIC DATA. Six stylised models (gap_02 proxies), three funding mixes (do nothing; Mix A; Mix B),
common random numbers throughout. Bumps add pure-risk oil exposure (zero expected excess return), so every cost
reported is a risk or liquidity cost, before any alpha.

Usage: python -I ra03_tier1_run.py <out_json> [n_paths]
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra03_lib as L  # noqa: E402
import ra03_t1oil as T  # noqa: E402

E = T.E
N = int(sys.argv[2]) if (__name__ == "__main__" and len(sys.argv) > 2) else 30000
SEED = 20261018
POLICIES = {
    "do_nothing": E.Policy(name="0"),
    "mix_A": E.Policy(name="A", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
    "mix_B": E.Policy(name="B", rcf=10.0, pace=12.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0),
}
# current ledger mapped to engine channels (ra03_ledger_results.json, canonical current state)
LEDGER_NOW = {"PRIV": 14.8, "eps_PRIV": 0.32, "LEV": 2.13, "PUB": 4.24 + 5.54, "GCC": 1.2}
BUMPS = {"PRIV_lookthrough_10": {"PRIV": 10.0, "eps_PRIV": 0.38},
         "PRIV_lookthrough_20": {"PRIV": 20.0, "eps_PRIV": 0.38},
         "PRIV_enr_fund_10": {"PRIV": 10.0, "eps_PRIV": 0.835},
         "LEV_direct_10": {"LEV": 10.0},
         "PUB_10": {"PUB": 10.0},
         "PUT_protection_3": {"PUT": -3.0},
         "GCC_1.2bn": {"GCC": 1.2},
         "ledger_now": LEDGER_NOW}


def h_lambda(lam, r):
    """-Cov(1 + lambda, r) / E[1 + lambda], pooled over path-quarters, annualised (x4)."""
    w = 1.0 + lam
    return float(-4.0 * np.mean((w - w.mean()) * (r - r.mean())) / w.mean())


def h_draw(dq, r, kd):
    w = 1.0 + kd * (dq - 0.05) / 0.05
    return float(-4.0 * np.mean((w - w.mean()) * (r - r.mean())) / w.mean())


def h_path(weight_tq, r_tq, years=5.0):
    """Horizon version: -Cov(path-mean weight, cumulative return) / E[weight] / years. Captures the lagged,
    smoothed response of the draw and of liquidity states to an oil move, which a contemporaneous quarterly
    covariance misses."""
    w = weight_tq.mean(axis=0)
    R = r_tq.sum(axis=0)
    return float(-np.mean((w - w.mean()) * (R - R.mean())) / w.mean() / years)


def main():
    t0 = time.time()
    out = {"label": L.LABEL, "n_paths": N, "policies": {k: vars(v) for k, v in POLICIES.items()},
           "ledger_now_channels": LEDGER_NOW, "lambda_stage": T.LAMBDA_STAGE.tolist(), "runs": {}}
    for mk, m in E.MODELS.items():
        gp = T.gen_paths(m, N, SEED + 1000)
        gp_blind = dict(gp)
        gp_blind["rates"] = np.repeat(gp["rates"].mean(axis=1, keepdims=True), N, axis=1)   # oil-blind draws
        for pk, pol in POLICIES.items():
            base = T.simulate_oil(m, pol, None, n=N, seed=SEED, gen=gp)
            res = {"base": {"p_red_pct": round(100 * base["p_red"], 3), "cp_upper_pct": round(100 * base["cp_upper_red"], 3),
                            "gstar_q": {str(k): round(v, 3) for k, v in base["gstar_q"].items()},
                            "stage_occ": [round(x, 3) for x in base["stage_occ"]],
                            "mean_lambda": round(float(base["lam"].mean()), 4)}}
            # lambda-weighted and draw-weighted haircuts per unit elasticity (r = dx de-meaned)
            dx = base["r_oil"]["PRIV"] / 0.38     # PRIV default eps 0.38 -> unit-elasticity oil return
            dq = base["draw_rate_q"]
            res["H_unit_eps"] = {"H_lambda_pct": round(100 * h_lambda(base["lam"], dx), 3),
                                 **{f"H_draw_kd{kd}_pct": round(100 * h_draw(dq, dx, kd), 3) for kd in (0.25, 0.5, 1.0)},
                                 "H_lambda_GCC_state_pct": round(100 * h_lambda(base["lam"], base["r_oil"]["GCC"]), 3),
                                 "H_lambda_path_pct": round(100 * h_path(1.0 + base["lam"], dx), 3),
                                 "H_draw_path_kd0.5_pct": round(100 * h_path(1.0 + 0.5 * (dq - 0.05) / 0.05, dx), 3),
                                 "H_draw_path_kd1.0_pct": round(100 * h_path(1.0 + 1.0 * (dq - 0.05) / 0.05, dx), 3),
                                 "H_lambda_path_GCC_state_pct": round(100 * h_path(1.0 + base["lam"],
                                                                                   base["r_oil"]["GCC"]), 3),
                                 "corr_path_oil_vs_mean_draw": round(float(np.corrcoef(dx.sum(axis=0),
                                                                                      dq.mean(axis=0))[0, 1]), 3),
                                 "corr_path_oil_vs_mean_lambda": round(float(np.corrcoef(dx.sum(axis=0),
                                                                                        base["lam"].mean(axis=0))[0, 1]), 3),
                                 "sd_dx_annual": round(float(dx.std() * 2.0), 4),
                                 "corr_dx_draw": round(float(np.corrcoef(dx.ravel(), dq.ravel())[0, 1]), 3)}
            res["H_per_bbl_usd_a_year"] = {"H_lambda": round(res["H_unit_eps"]["H_lambda_pct"] / 100 * L.F1, 3),
                                           "H_draw_kd0.5": round(res["H_unit_eps"]["H_draw_kd0.5_pct"] / 100 * L.F1, 3)}
            bumps = {}
            for bk, spec in BUMPS.items():
                if pk != "do_nothing" and bk in ("PRIV_lookthrough_20", "PRIV_enr_fund_10"):
                    continue
                r = T.simulate_oil(m, pol, spec, n=N, seed=SEED, gen=gp)
                size = spec.get("PRIV", spec.get("LEV", spec.get("PUB", spec.get("PUT", spec.get("GCC", 1.0)))))
                if bk == "ledger_now":
                    size = 1.0
                d_red = 100 * (r["p_red"] - base["p_red"])
                n_flip = int((r["red"] != base["red"]).sum())
                bumps[bk] = {"size": size,
                             "dP_red_pp": round(d_red, 4), "paths_flipped": n_flip,
                             "dP_red_pp_se": round(100 * np.sqrt(n_flip) / N, 4),
                             "dG*_q99.6_bn": round(r["gstar_q"][0.996] - base["gstar_q"][0.996], 4),
                             "dG*_q99_bn": round(r["gstar_q"][0.99] - base["gstar_q"][0.99], 4),
                             "dG*_q95_bn": round(r["gstar_q"][0.95] - base["gstar_q"][0.95], 4),
                             "dG*_pathwise_mean_top1pct_bn": round(float(
                                 (r["gstar"] - base["gstar"])[base["gstar"] >= np.quantile(base["gstar"], 0.99)].mean()), 4),
                             "dCE_bp_a_year": round(T.ce_bp(base["w_inv2"], r["w_inv2"]), 4),
                             "put_premium_5y_bn": round(r["put_prem"], 3), "put_payoff_5y_bn": round(r["put_cash"], 3)}
                if pk == "do_nothing" and bk in ("PRIV_lookthrough_10", "PRIV_enr_fund_10", "LEV_direct_10", "PUB_10"):
                    bb = T.simulate_oil(m, pol, None, n=N, seed=SEED, gen=gp_blind)
                    rb = T.simulate_oil(m, pol, spec, n=N, seed=SEED, gen=gp_blind)
                    bumps[bk]["dCE_bp_a_year_oil_blind_draws"] = round(T.ce_bp(bb["w_inv2"], rb["w_inv2"]), 4)
                    bumps[bk]["dP_red_pp_oil_blind_draws"] = round(100 * (rb["p_red"] - bb["p_red"]), 4)
            res["bumps"] = bumps
            out["runs"][f"{mk}|{pk}"] = res
            print(f"[{time.time() - t0:5.0f}s] {mk} {pk}: P(red) {res['base']['p_red_pct']:.2f}% "
                  f"G*99.6 {res['base']['gstar_q']['0.996']:.2f}  H_lam(unit) {res['H_unit_eps']['H_lambda_pct']:.2f}% "
                  f"| PRIV10 dRed {bumps['PRIV_lookthrough_10']['dP_red_pp']:+.3f} dG {bumps['PRIV_lookthrough_10']['dG*_q99.6_bn']:+.3f} "
                  f"dCE {bumps['PRIV_lookthrough_10']['dCE_bp_a_year']:+.3f} | ledger dRed {bumps['ledger_now']['dP_red_pp']:+.3f} "
                  f"dCE {bumps['ledger_now']['dCE_bp_a_year']:+.3f}", flush=True)
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == "__main__":
    main()
