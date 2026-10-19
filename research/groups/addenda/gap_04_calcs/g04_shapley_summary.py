"""Summarise the 9-player Shapley results (SYNTHETIC - NOT ADIC DATA).
Reads g04_shapley_mixB_results.json and the per-model coalition tables (npz); writes
g04_shapley_summary.json with exact values, CRN path SEs, the MC error of the group-off baseline itself,
a stand-alone-vs-Shapley interaction index and the permutation-sampling accuracy."""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "g04_shapley_mixB_results.json")))
P = S["players"]
out = {"players": P, "policy": S["policy"], "trigger": S["trigger"], "models": {}}
for mk, d in S["models"].items():
    a = d["analysis"]
    z = np.load(os.path.join(HERE, f"g04_shapley_{mk}_mixB.npz"))
    W, R = z["W"].astype(float), z["R"].astype(float)
    n = W.shape[1]
    ce = lambda w: float(np.mean(w ** -2.0) ** -0.5)  # noqa: E731
    # MC error of the baseline and the full policy themselves (not paired)
    base = dict(W=(float(W[0].mean()), float(W[0].std(ddof=1) / math.sqrt(n))),
                R=(float(100 * R[0].mean()), float(100 * math.sqrt(R[0].mean() * (1 - R[0].mean()) / n))),
                full_W=(float(W[-1].mean()), float(W[-1].std(ddof=1) / math.sqrt(n))),
                paired_total_W_se=float((W[-1] - W[0]).std(ddof=1) / math.sqrt(n)))
    # bootstrap SE of CE(baseline)
    rng = np.random.default_rng(3)
    bs = [ce(W[0][rng.integers(0, n, n)]) for _ in range(200)]
    base["CE"] = (ce(W[0]), float(np.std(bs, ddof=1)))
    row = {"baseline": base}
    for key in ("W", "R", "CE"):
        phi = np.array([a["exact"][key][p] for p in P])
        v = a["v"][key]
        alone = np.array([v["singles"][p] - v["empty"] for p in P])
        idx = float(np.abs(phi - alone).sum() / max(np.abs(phi).sum(), 1e-12))
        perm = {k: dict(max_rmse=max(x["rmse"].values()), mean_rmse=float(np.mean(list(x["rmse"].values()))),
                        min_cov=min(x["coverage_95"].values()), mean_cov=float(np.mean(list(x["coverage_95"].values()))),
                        mean_se=float(np.mean(list(x["mean_se_perm"].values()))), evals=x["coalitions_per_estimate"])
                for k, x in a["perm"][key].items()}
        row[key] = dict(total=v["full"] - v["empty"], empty=v["empty"], full=v["full"],
                        phi={p: float(x) for p, x in zip(P, phi)}, path_se=a["path_se"][key],
                        alone={p: float(x) for p, x in zip(P, alone)}, interaction_index=idx, perm=perm,
                        efficiency_check=float(phi.sum() - (v["full"] - v["empty"])))
    out["models"][mk] = row
with open(os.path.join(HERE, "g04_shapley_summary.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
for mk, row in out["models"].items():
    b = row["baseline"]
    print(f"== {mk} baseline W {b['W'][0]:.1f}+-{b['W'][1]:.2f}  P(red) {b['R'][0]:.2f}+-{b['R'][1]:.2f}pp  "
          f"CE {b['CE'][0]:.1f}+-{b['CE'][1]:.2f}  paired total W se {b['paired_total_W_se']:.3f}")
    for key in ("W", "R", "CE"):
        r = row[key]
        print(f"  {key} total {r['total']:+.2f} (eff chk {r['efficiency_check']:+.1e}) interaction idx {r['interaction_index']:.2f} | " +
              " ".join(f"{p}:{r['phi'][p]:+.2f}({r['path_se'][p]:.2f})" for p in P))
        print("      perm:", {k: (round(x["max_rmse"], 3), round(x["min_cov"], 2), x["evals"]) for k, x in r["perm"].items()})
