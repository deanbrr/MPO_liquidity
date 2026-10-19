import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
print("calibration:", d["calibration"])
for name, r in d.items():
    if name == "calibration":
        continue
    s, f = r["static"], r["full"]
    sh = r["shapley"]
    print(f"\n{name}: uplift {r['uplift']*100:.2f}pp")
    print("  static", {k: round(v * 100, 2) for k, v in s.items()}, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r["aux_static"].items()})
    print("  full  ", {k: round(v * 100, 2) for k, v in f.items()}, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r["aux_full"].items()})
    print("  shapley pp (mean, 1.96se):", {k: (round(v[0] * 100, 3), round(1.96 * v[1] * 100, 3)) for k, v in sh.items()})
    print("  sum shapley:", round(sum(v[0] for v in sh.values()) * 100, 3))
