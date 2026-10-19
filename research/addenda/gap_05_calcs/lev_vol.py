"""Volatility of the ADIC working book at economic leverage 1.00 / 1.05 / 1.30 (JPM-2026 risk), for the addendum."""
import sys

import numpy as np

D = np.load(sys.argv[1], allow_pickle=False)
names = [str(x) for x in D["names"]]
vol, C = D["vol"], D["corr"]
ix = {n: i for i, n in enumerate(names)}
K = ["Private Equity", "Direct Lending", "Diversified Hedge Funds", "AC World Equity", "U.S. Aggregate Bonds", "U.S. Cash"]
kk = [ix[k] for k in K]
w = np.array([88, 18, 20, 28, 8, 15]) / 177
# nearest-PSD repair (same routine as bridge.py)
Y = C.copy(); dS = np.zeros_like(Y)
for _ in range(5000):
    R = Y - dS
    ev, V = np.linalg.eigh((R + R.T) / 2)
    X = (V * np.clip(ev, 0, None)) @ V.T
    dS = X - R
    Yn = X.copy(); np.fill_diagonal(Yn, 1.0)
    if np.abs(Yn - Y).max() < 1e-12:
        Y = Yn
        break
    Y = Yn
S = Y[np.ix_(kk, kk)] * np.outer(vol[kk], vol[kk])
for L in (1.0, 1.05, 1.30):
    var = w @ S @ w + 2 * (L - 1) * (S @ w)[3] + (L - 1) ** 2 * S[3, 3] + 0.0125 ** 2
    print(f"L={L:.2f}: vol {np.sqrt(var):.4f}")
print("beta of book to ACWI:", round(float((S @ w)[3] / S[3, 3]), 3))
