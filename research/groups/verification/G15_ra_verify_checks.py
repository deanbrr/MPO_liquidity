"""Independent checks on the G15 dossier (fact-check harness; synthetic book values are the dossier's own).
Usage: python -I indep_checks.py <orig_results.json> <rerun_results.json> <data_dir>
"""
import csv
import json
import math
import sys

import numpy as np

orig = json.load(open(sys.argv[1], encoding="utf-8"))
rer = json.load(open(sys.argv[2], encoding="utf-8"))
data = sys.argv[3]


# 1. Diff original vs rerun JSON
def walk(a, b, path, diffs):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                diffs.append((path + "/" + str(k), "missing"))
            else:
                walk(a[k], b[k], path + "/" + str(k), diffs)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append((path, "len"))
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", diffs)
    else:
        if isinstance(a, float) or isinstance(b, float):
            if not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) < 1e-12):
                diffs.append((path, (a, b)))
        elif a != b:
            diffs.append((path, (a, b)))


diffs = []
walk(orig, rer, "", diffs)
print("JSON diffs:", len(diffs), diffs[:10])


# 2. Lead-lag UAE vs Brent, independent implementation
def rd(p):
    out = {}
    with open(p, encoding="utf-8") as fh:
        r = csv.reader(fh)
        next(r)
        for d, v in r:
            if v.strip() not in ("", "."):
                out[d] = float(v)
    return out


uae = rd(data + "/fred_QAEN628BIS_uae_resi_prices.csv")
br = rd(data + "/fred_DCOILBRENTEU_quarterly_avg.csv")
dates = sorted(d for d in uae if d in br)
u = np.log([uae[d] for d in dates])
b = np.log([br[d] for d in dates])
du = u[4:] - u[:-4]
db = b[4:] - b[:-4]
print("sample", dates[0], dates[-1], "n quarters", len(dates), "n 4q changes", len(du))
for L in (0, 1, 2, 3, 4, 6, 8):
    x = db if L == 0 else db[:-L]
    y = du if L == 0 else du[L:]
    rho = np.corrcoef(x, y)[0, 1]
    # Bartlett-ish effective n for overlapping 4q windows: n/4
    n_eff = len(x) / 4.0
    t = rho * math.sqrt((n_eff - 2) / (1 - rho ** 2))
    print(f"L={L} corr={rho:.3f} n={len(x)} n_eff~{n_eff:.0f} t(n_eff)~{t:.2f}")
print("UAE peak/trough checks:",
      round(uae["2010-10-01"] / uae["2008-04-01"] - 1, 4), round(uae["2020-07-01"] / uae["2014-10-01"] - 1, 4),
      round(uae["2024-01-01"] / uae["2020-07-01"] - 1, 4))

# 3. Geltner-consistent reported marks under T4' vs the hard-coded marks in the script
SLEEVES = orig["book"]
T4_TRUE = {"RE": -0.25, "RE_GCC": -0.30, "INF": -0.12, "ENR": -0.30}
PHI = {"RE": 0.65, "RE_GCC": 0.65, "INF": 0.60, "ENR": 0.50}
T4_MARKS = {"RE": [-0.06, -0.06, -0.04, -0.03], "RE_GCC": [-0.06, -0.07, -0.05, -0.04],
            "INF": [-0.03, -0.03, -0.02], "ENR": [-0.10, -0.08, -0.05]}
tot_true = tot_rep_geltner = tot_rep_script4 = tot_rep_script3 = 0.0
for s in SLEEVES:
    sec, nav, ltv = s["sector"], s["nav"], s["ltv"]
    gav = nav / (1 - ltv)
    # true gross value path, linear ramp to T4_TRUE over 4 quarters (dossier: ramped over 12 months)
    lv = [1 + T4_TRUE[sec] * q / 4 for q in range(5)]
    r_true = [lv[q] / lv[q - 1] - 1 for q in range(1, 5)]
    phi = PHI[sec]
    rs, prev = [], 0.0
    for r in r_true:
        prev = phi * prev + (1 - phi) * r
        rs.append(prev)
    rep_gross = float(np.prod([1 + x for x in rs]) - 1)
    d_true = gav * T4_TRUE[sec]
    d_rep_g = gav * rep_gross              # appraisal smoothing at asset level, debt fixed -> same $ on equity
    m = T4_MARKS[sec]
    d_rep_s4 = nav * (float(np.prod([1 + x for x in m])) - 1)
    d_rep_s3 = nav * (float(np.prod([1 + x for x in m[:3]])) - 1)
    tot_true += d_true
    tot_rep_geltner += d_rep_g
    tot_rep_script4 += d_rep_s4
    tot_rep_script3 += d_rep_s3
print(f"T4' 12m true equity loss {tot_true:.2f}; Geltner-consistent reported {tot_rep_geltner:.2f} "
      f"({tot_rep_geltner / tot_true:.0%} of true); script marks incl. m12 {tot_rep_script4:.2f} "
      f"({tot_rep_script4 / tot_true:.0%}); script marks t<=11 {tot_rep_script3:.2f} ({tot_rep_script3 / tot_true:.0%})")

# 4. Look-through LTV after the T4' true-value shock (12m), and per-sleeve LTVs vs the proposed limits
gav0 = sum(s["nav"] / (1 - s["ltv"]) for s in SLEEVES)
debt0 = gav0 - 18.0
cures12 = orig["cash_map"]["T4prime"]["12m"]["TOTAL"]["cures"]
gav1 = gav0 + tot_true
print(f"look-through LTV t0 {debt0 / gav0:.3f}; after T4' 12m {(debt0 - cures12) / gav1:.3f} (debt {debt0 - cures12:.2f}, GAV {gav1:.2f})")
for s in SLEEVES:
    l1 = s["ltv"] / (1 + T4_TRUE[s["sector"]])
    print(f"  {s['id']:11s} LTV0 {s['ltv']:.2f} -> stressed {l1:.2f} direct={s['direct']}")

# 5. Return-cost arithmetic (J.P. Morgan figures cited in dossier) - implied ENR return
for enr in (0.06, 0.07, 0.08, 0.09):
    ra = 0.50 * 0.079 + 0.36 * 0.071 + 0.14 * enr
    cost = 18.0 * (0.102 - ra)
    print(f"ENR {enr:.0%}: RA blended {ra:.3%}; cost ${cost:.2f}bn = {cost / 177 * 1e4:.0f}bp of NAV")

# 6. Queue calibration arithmetic: 2025 ODCE flows
print("ODCE D&R/NAV", round(19.9 / 227.3, 4), "less 4% income ->", round(19.9 / 227.3 - 0.04, 4), "per q", round((19.9 / 227.3 - 0.04) / 4, 4))
# steady state of the drought queue: Q = Q(1-rho) + n - cap  -> Q* = (n - cap)/rho (no ADIC)
print("drought queue steady state Q* =", round((0.015 - 0.012) / 0.08, 4))
