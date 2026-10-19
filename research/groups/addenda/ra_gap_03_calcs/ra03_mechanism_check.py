"""RA gap 03, step 3c: where does the Tier-2 cost of oil delta come from?

SYNTHETIC - NOT ADIC DATA. Compares the CE cost of +10m bbl of private oil exposure (eps 0.38) under
  (a) the canonical coupling (kappa calibrated: P(CRIS | DB) = 0.85),
  (b) no coupling (kappa = 1: demand busts no longer cluster in crises),
  (c) the canonical coupling with oil-blind draws (draw rates replaced by their cross-path mean),
for M1, M4 and M6, do nothing. If (b) is much cheaper than (a) while (c) ~ (a), the cost is oil's co-movement with
ADIC's crisis risk, not the owner draw.

Usage: python -I ra03_mechanism_check.py <out_json> [n_paths]
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra03_lib as L  # noqa: E402
import ra03_t1oil as T  # noqa: E402

E = T.E
N = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
SEED = 20261018


def gen_paths_kappa1(m, n, seed):
    PZm = T._pzm()
    PS = L.s_chain_for_share(E.stationary_crisis_share(m))
    K = np.ones((4, 6))
    g = L.Gen(PS, PZm, K, gw_mode="weibull", gw_k=1.3)
    sim = g.simulate(n=n, T=63, seed=seed, S0=L.sLATE, Z0=T.Z0, x0=math.log(L.F1), chi0=math.log(L.SPOT / L.F1))
    dr = L.owner_draws(sim, 6, seed + 1)
    q_end = np.array([3 * (t + 1) for t in range(E.T_Q)])
    x = sim["x"][q_end]
    d = dr["d"]
    rates = [(5.8 + 3 * d[0]) / 4] + [(d[k - 1] + 3 * d[k]) / 4 for k in range(1, 5)]
    return {"crisis": sim["S"][q_end] == L.sCRIS, "z": sim["Z"][q_end].astype(int), "x": x,
            "x_prev": np.vstack([sim["x"][0][None, :], x[:-1]]),
            "P_q": np.stack([sim["P"][3 * t + 1:3 * t + 4].mean(axis=0) for t in range(E.T_Q)]),
            "rates": np.array(rates) / 100.0, "d_annual": d, "Z_month": sim["Z"], "S_month": sim["S"]}


def main():
    out = {"label": L.LABEL, "n_paths": N, "runs": {}}
    spec = {"PRIV": 10.0, "eps_PRIV": 0.38}
    pol = E.Policy()
    for mk in ("M1", "M4", "M6"):
        m = E.MODELS[mk]
        gp = T.gen_paths(m, N, SEED + 1000)
        gb = dict(gp)
        gb["rates"] = np.repeat(gp["rates"].mean(axis=1, keepdims=True), N, axis=1)
        g1 = gen_paths_kappa1(m, N, SEED + 1000)
        row = {}
        for nm, g in (("canonical", gp), ("oil_blind_draws", gb), ("kappa_1_no_coupling", g1)):
            b = T.simulate_oil(m, pol, None, n=N, seed=SEED, gen=g)
            r = T.simulate_oil(m, pol, spec, n=N, seed=SEED, gen=g)
            corr = float(np.corrcoef((g["x"] - g["x_prev"]).ravel(), g["crisis"].astype(float).ravel())[0, 1])
            row[nm] = {"dCE_bp_per_10mbbl": round(T.ce_bp(b["w_inv2"], r["w_inv2"]), 3),
                       "p_red_base_pct": round(100 * b["p_red"], 2),
                       "share_DB_in_crisis": round(float((g["z"][g["crisis"]] == L.iDB).mean()), 3),
                       "corr_quarterly_dx_crisis": round(corr, 3)}
        out["runs"][mk] = row
        print(mk, row, flush=True)
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
