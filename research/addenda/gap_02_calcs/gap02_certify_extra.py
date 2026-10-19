"""gap_02: 50k-path certification of the exposure-neutral (premium) frontier mixes. SYNTHETIC - NOT ADIC DATA."""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gap02_frontier import SCOPES, g_ce, outside_bp, premium_bp  # noqa: E402
from gap02_study import N_CERT, run_policy  # noqa: E402

MIXES = ["R0_N0_P12_B0_Q8_A0_H0", "R10_N0_P12c_B1_Q8_A0_H5", "R20_N0_P6c_B0_Q12_A3_H0", "R20_N0_P9c_B0_Q8_A0_H0",
         "R15_N0_P9c_B1_Q8_A0_H5", "R15_N0_P12_B0_Q8_A0_H0", "R0_N0_P12_B1_Q8_A0_H0", "R0_N0_P12c_B0_Q8_A0_H0"]


def main():
    raw = json.load(open(os.path.join(HERE, "gap02_grid_raw.json")))
    by = {r["kw"]["name"]: r for r in raw["grid"]}
    with ProcessPoolExecutor(max_workers=len(MIXES)) as ex:
        out = list(ex.map(run_policy, [(by[m]["kw"], N_CERT) for m in MIXES]))
    ref = [r for kw, r in out if kw["name"] == MIXES[0]][0]
    res = {}
    for kw, r in out:
        row = dict(kw=kw, models=r)
        res[kw["name"]] = dict(
            p_red={k: r[k]["p_red"] for k in r}, cp_red={k: r[k]["cp_upper_red"] for k in r},
            cp_black12={k: r[k]["cp_upper_black_12m"] for k in r}, p_band12={k: r[k]["p_band_12m"] for k in r},
            withheld={k: r[k]["mean_withheld"] for k in r}, debt_p99={k: r[k]["max_debt_ratio_p99"] for k in r},
            p_cov={k: r[k]["p_covenant"] for k in r},
            ce_vs_ref_m15=(g_ce(dict(models=ref), SCOPES["M1-M5"]) - g_ce(row, SCOPES["M1-M5"])) * 1e4
            + outside_bp(row, SCOPES["M1-M5"]) - outside_bp(dict(models=ref), SCOPES["M1-M5"]),
            premium_m15=premium_bp(row, SCOPES["M1-M5"]))
        print(kw["name"], {k: round(v * 100, 2) for k, v in res[kw["name"]]["cp_red"].items()},
              "band12", {k: round(v * 100, 1) for k, v in res[kw["name"]]["p_band12"].items()},
              f"CE15 {res[kw['name']]['ce_vs_ref_m15']:.1f} prem15 {res[kw['name']]['premium_m15']['total']:.1f}",
              "cov", {k: round(v * 100, 2) for k, v in res[kw["name"]]["p_cov"].items()})
    with open(os.path.join(HERE, "gap02_certify_extra.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
