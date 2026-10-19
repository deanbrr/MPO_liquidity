import sys
import numpy as np
from scipy.stats import t
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
sets = {"published 4k paths, own draw (headline + 4 books)": [2.85, 1.108, 0.982, 1.285, -0.297],
        "10k paths, own draw": [2.85, 1.34, 1.36, 1.53, -0.05],
        "10k paths, opp Sharpe 0.30": [1.65, 1.20, 1.67, 1.20, 0.46],
        "10k paths, opp Sharpe 0": [1.02, 0.30, 0.90, 0.17, -0.39],
        "10k paths, O1 with opp IM 1.0, Sharpe 0.30": [1.43, 0.86, 1.35, 0.79, 0.20],
        "10k paths, playbook own draw": [-0.17, -0.43, 0.56, -0.23, -0.71]}
for k, v in sets.items():
    a = np.array(v)
    m, s = a.mean(), a.std(ddof=1)
    se = s / np.sqrt(len(a))
    for margin in (1.0, 0.0):
        tt = (m - margin) / se
        p = 1 - t.cdf(tt, len(a) - 1)
        print(f"{k}: mean {m:+.2f}pp sd {s:.2f} se {se:.2f}; vs +{margin:.0f}pp: t {tt:.2f}, one-sided p {p:.3f}")
x = np.array([0.672, 0.417, 0.181, 0.558, 0.150, 0.672]); y = np.array([2.85, 1.34, 1.36, 1.53, -0.05, 2.39])
b = np.polyfit(x, y, 1); r = np.corrcoef(x, y)[0, 1]
print(f"veq (own draw, 10k) on opp Sharpe across 6 books: slope {b[0]:.2f}pp per unit Sharpe, intercept {b[1]:.2f}, r {r:.2f}")
x4 = np.array([0.672, 0.417, 0.181, 0.558, 0.150, 0.672]); y4 = np.array([2.85, 1.108, 0.982, 1.285, -0.297, 2.129])
print("published 4k: rank corr", np.corrcoef(np.argsort(np.argsort(x4)), np.argsort(np.argsort(y4)))[0, 1])
