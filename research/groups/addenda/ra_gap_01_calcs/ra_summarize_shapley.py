"""Summarise the ten-player Shapley results (ra_shapley_<book>_results.json) for the addendum. SYNTHETIC - NOT ADIC DATA.
Run: <venv>/python.exe -I -B ra_summarize_shapley.py [book]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
book = sys.argv[1] if len(sys.argv) > 1 else "v2u16"
d = json.load(open(os.path.join(HERE, f"ra_shapley_{book}_results.json"), encoding="utf-8"))
P = d["players"]
M = list(d["models"])
print("book", d["book"], "theta", round(d["theta"], 4), "models", M)
for mk in M:
    a = d["models"][mk]["analysis"]
    print(f"\n== {mk}  ({d['models'][mk]['secs']:.0f}s)")
    for key in ("R", "CE", "W"):
        v = a["v"][key]
        tot = v["full"] - v["empty"]
        s = sum(a["exact"][key].values())
        print(f"  {key}: v(N) {v['full']:.4f}  v(empty) {v['empty']:.4f}  total {tot:.4f}  sum phi {s:.4f}  "
              f"efficiency err {abs(s - tot):.2e}  interaction idx {a['interaction_index'][key]:.2f}  "
              f"perm32 cover min {a['perm32'][key]['coverage_min']:.3f} rmse max {a['perm32'][key]['rmse_max']:.3f}")
        se = a["path_se"][key]
        print("     path SE range", round(min(se.values()), 3), "-", round(max(se.values()), 3), " RA SE", round(se["RA"], 3))
        ra_alone = v["singles"]["RA"] - v["empty"]
        print(f"     RA: phi {a['exact'][key]['RA']:.3f}  first-in (alone) {ra_alone:.3f}  share of total {a['exact'][key]['RA'] / tot if tot else float('nan'):.3f}")
    print("  RA cures24 full / empty:", d["models"][mk].get("ra_cures24_full"), d["models"][mk].get("ra_cures24_empty"))

print("\n| Player | dP(red), pp: " + " / ".join(M) + " | dCE, $bn: " + " / ".join(M) + " | dE[W~], $bn: " + " / ".join(M) + " |")
order = sorted(P, key=lambda p: d["models"][M[-1]]["analysis"]["exact"]["R"][p])
for p in order:
    r = " / ".join(f"{d['models'][mk]['analysis']['exact']['R'][p]:+.1f}" for mk in M)
    c = " / ".join(f"{d['models'][mk]['analysis']['exact']['CE'][p]:+.2f}" for mk in M)
    w = " / ".join(f"{d['models'][mk]['analysis']['exact']['W'][p]:+.2f}" for mk in M)
    print(f"| {p} | {r} | {c} | {w} |")
tr = " / ".join(f"{d['models'][mk]['analysis']['v']['R']['full'] - d['models'][mk]['analysis']['v']['R']['empty']:+.1f}" for mk in M)
tc = " / ".join(f"{d['models'][mk]['analysis']['v']['CE']['full'] - d['models'][mk]['analysis']['v']['CE']['empty']:+.2f}" for mk in M)
tw = " / ".join(f"{d['models'][mk]['analysis']['v']['W']['full'] - d['models'][mk]['analysis']['v']['W']['empty']:+.2f}" for mk in M)
print(f"| Total v(N) - v(empty) | {tr} | {tc} | {tw} |")
