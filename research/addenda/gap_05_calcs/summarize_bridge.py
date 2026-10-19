import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
ms = list(d["models"])


def f(x):
    return f"{x * 100:6.2f}"


def p(x):
    return f"{x * 100:6.1f}"


print("model".ljust(18), " ".join(m[:6].rjust(6) for m in ms))
for key in ["beta_geo", "alpha_total", "overlay", "central_geo", "gap_to_10", "central_geo_L130", "allp90_geo", "allp10_geo"]:
    print(key.ljust(18), " ".join(f(d["models"][m][key]) for m in ms))
print("lev1.05".ljust(18), " ".join(f(d["models"][m]["contrib"]["Economic leverage (1.05x)"]) for m in ms))
print("drags".ljust(18), " ".join(f(-d["models"][m]["drags"]["total"]) for m in ms))
for k in ["convex", "reserve", "facilities", "pacing", "forced_sales"]:
    print(("  " + k).ljust(18), " ".join(f(-d["models"][m]["drags"][k]) for m in ms))
print("drags low/high".ljust(18), " ".join(f"{-d['models'][m]['drags_low']*100:.2f}/{-d['models'][m]['drags_high']*100:.2f}" for m in ms))
for key in ["p10y_beta", "p5y_beta", "p10y_central", "p10y_central_L130", "p5y_central", "allp90_p10y", "allp10_p10y",
            "p_mu_ge10_L105", "p_mu_ge10_L130"]:
    print(key.ljust(18), " ".join(p(d["models"][m][key]) for m in ms))
for h in ["0.079", "0.100", "0.108", "0.139"]:
    print(("P10y>=" + h).ljust(18), " ".join(p(d["models"][m]["p10y_hurdles"][h]) for m in ms))
print("\ncontrib (pp) M1:")
for k, v in d["models"][ms[0]]["contrib"].items():
    print("  ", k.ljust(50), f(v))
print("\nbreakevens (alpha_be | p_reach | P10y@P90 | P10y@0) for M1, M4, M3:")
for k in d["models"][ms[0]]["breakeven"]:
    row = []
    for m in (ms[0], ms[3], ms[2]):
        b = d["models"][m]["breakeven"][k]
        row.append(f"{b['alpha_be']:7.2f} {b['p_reach']*100:5.1f}% {b['p10y_at_p90']*100:5.1f} {b['p10y_at_zero']*100:5.1f}")
    print("  ", k[:46].ljust(46), " | ".join(row))
print("\nmixture:", {k: {kk: round(vv * 100, 2) for kk, vv in v.items()} for k, v in d["mixture"].items()})
print("sd levers pp:", round(d["sd_levers_pp"], 3))
print("weights:", {k: round(v, 4) for k, v in d["weights"].items()})
