import json
import sys

from scipy import stats

d = json.load(open(sys.argv[1], encoding="utf-8"))
lev = {"PE": (52 / 177, -0.55, 2.05), "COI": (18 / 177, -1.0, 2.5), "SEC": (14 / 177, -0.5, 2.5),
       "CAP": (8 / 177, -1.5, 1.5), "PCR": (14 / 177, -1.5, 0.75), "HF": (20 / 177, -1.5, 1.5),
       "LO": (28 / 177, -0.6, 0.3), "P2S": (10 / 177, -0.5, 0.2)}
sd_c = sum(w * (hi - lo) / 2.563 for w, lo, hi in lev.values()) / 100 + 0.25 * 0.0125
print("comonotone sd pp", round(sd_c * 100, 3))
for m, r in d["models"].items():
    a = 1 - stats.norm.cdf((0.10 - r["central_geo"]) / sd_c)
    b = 1 - stats.norm.cdf((0.10 - r["central_geo_L130"]) / sd_c)
    print(f"{m:26s} indep L1.05 {r['p_mu_ge10_L105']*100:5.1f} L1.30 {r['p_mu_ge10_L130']*100:5.1f} | "
          f"comonotone L1.05 {a*100:5.1f} L1.30 {b*100:5.1f}")
