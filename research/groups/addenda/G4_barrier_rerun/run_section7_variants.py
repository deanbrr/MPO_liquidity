"""
G4 barrier re-run, step A: section 7 (synthetic $18bn co-investment book) under alternative
treatments of the quarterly-checked default barrier.  SYNTHETIC - NOT ADIC DATA.

Imports, by file path, the verbatim copy orig/G4_coinvest_calcs.py and the corrected copy
G4_coinvest_calcs_bgk.py (both in this folder) and runs only section 7 (the only section of
that script with a monitored barrier; sections 1-6 contain no barrier monitoring).

Section 7 draws every random number with a state-independent shape, so all variants below use
exactly the same random numbers as the published run (common random numbers): every difference
is caused by the barrier rule alone.

Variants
  orig_script      verbatim original (no correction)  -> must reproduce the published JSON
  none             corrected copy with BARRIER_MODE="none" -> must equal orig_script
  bgk              kappa*D*exp(+0.5826*sigma_V*sqrt(0.25)), sigma_V diffusive (beta_A*sig_m, sig_id)  [FIX]
  bgk_total_sigma  same, sigma_V also including Kou jump variance (sensitivity)
  bgk_wrong_sign   kappa*D*exp(-0.5826*sigma_V*sqrt(0.25)), the formula printed in the dossier, section 7

Run:  <venv>/python.exe -I run_section7_variants.py   (writes section7_variants_results.json here)
"""
from __future__ import annotations

import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLISHED = os.path.normpath(os.path.join(HERE, "..", "..", "verification", "G4_coinvest_calcs_results.json"))
OUT = os.path.join(HERE, "section7_variants_results.json")


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def both_starts(mod) -> dict:
    return dict(start_drought=mod.section7(start_regime=2),
                start_normal=mod.section7(start_regime=1, seed_off=8))


def main():
    orig = load("g4_orig", os.path.join(HERE, "orig", "G4_coinvest_calcs.py"))
    bgk = load("g4_bgk", os.path.join(HERE, "G4_coinvest_calcs_bgk.py"))
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "variants": {}}
    res["variants"]["orig_script"] = both_starts(orig)
    for mode, sig in (("none", "diffusive"), ("bgk", "diffusive"), ("bgk", "total"), ("bgk_wrong_sign", "diffusive")):
        bgk.BARRIER_MODE, bgk.BGK_SIGMA = mode, sig
        key = {("none", "diffusive"): "none", ("bgk", "diffusive"): "bgk", ("bgk", "total"): "bgk_total_sigma",
               ("bgk_wrong_sign", "diffusive"): "bgk_wrong_sign"}[(mode, sig)]
        res["variants"][key] = both_starts(bgk)
    bgk.BARRIER_MODE, bgk.BGK_SIGMA = "bgk", "diffusive"

    # reproducibility check against the published results JSON
    with open(PUBLISHED, encoding="utf-8") as fh:
        pub = json.load(fh)
    chk = {}
    for start, pkey in (("start_drought", "section7_book_sim_start_drought"),
                        ("start_normal", "section7_book_sim_start_normal")):
        mine, theirs = res["variants"]["orig_script"][start], pub[pkey]
        diffs = []
        for k, v in theirs.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    if isinstance(vv, dict):
                        for k3, v3 in vv.items():
                            if abs(mine[k][kk][k3] - v3) > 1e-9:
                                diffs.append(f"{k}.{kk}.{k3}")
                    elif isinstance(vv, (int, float)) and abs(mine[k][kk] - vv) > 1e-9:
                        diffs.append(f"{k}.{kk}")
            elif isinstance(v, (int, float)) and abs(mine[k] - v) > 1e-9:
                diffs.append(k)
        same_none = res["variants"]["none"][start] == {**res["variants"]["orig_script"][start],
                                                       "barrier_mode": "none", "bgk_sigma": "diffusive",
                                                       "bgk_beta": bgk.BGK_BETA}
        chk[start] = dict(orig_vs_published_mismatches=diffs, none_equals_orig=bool(same_none))
    res["reproducibility"] = chk

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, default=float)

    # compact console table
    rows = [("annual_writeoff_rate_per_position", None), ("writeoffs_3y", "mean"), ("writeoff_cost_share", None),
            ("dist_3y", "mean"), ("dist_3y", "p10"), ("net_cf_3y", "mean"), ("net_cf_3y", "p10"),
            ("net_cf_3y", "p90"), ("calls_3y", "mean")]
    for start in ("start_drought", "start_normal"):
        print(f"--- {start}")
        for k, sub in rows:
            vals = []
            for var in ("orig_script", "bgk", "bgk_total_sigma", "bgk_wrong_sign"):
                v = res["variants"][var][start][k]
                vals.append(v[sub] if sub else v)
            print(f"{k + ('.' + sub if sub else ''):45s}", "  ".join(f"{x:9.4f}" for x in vals))
        y1 = [res["variants"][var][start]["annual_dist_yield_on_nav0"]["Y1"]["mean"]
              for var in ("orig_script", "bgk", "bgk_total_sigma", "bgk_wrong_sign")]
        print(f"{'Y1 yield mean':45s}", "  ".join(f"{x:9.4f}" for x in y1))
    print("reproducibility:", json.dumps(chk))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
