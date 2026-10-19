"""RA gap 03, step 4b: how the deployment of SELL proceeds moves the full-engine reservation price.

SYNTHETIC - NOT ADIC DATA. For M1, M4, M5 under do nothing and Mix B (alpha 0, k = 1.3), the SELL leg is run
four ways: proceeds held as cash (de-risks) or with the sleeve's 0.6 beta rebuilt in futures; proceeds landing
before or after the t0 reserve top-up (before: the top-up sells less DM equity, so SELL keeps more equity beta).
Reports p* and the expected terminal-wealth gap E[W_SELL - W_HOLD] at a 0.85 bid.

Usage: python -I ra03_card_deploy_check.py <card_json> <out_json> [n_paths]
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra03_lib as L  # noqa: E402
import ra03_t1oil as T  # noqa: E402
from ra03_tier1_run import POLICIES  # noqa: E402

E = T.E
N = int(sys.argv[3]) if len(sys.argv) > 3 else 30000
SEED = 20261018
V0, UNF, TAU, BETA_EQ, COST = 0.70, 0.70 * 0.6 / 1.6, 0.0025, 0.6, 0.01
BIDS = np.round(np.arange(0.60, 1.101, 0.05), 3)


def ce_growth(ws):
    return (float(np.mean(ws)) ** -0.5) ** 0.2 - 1.0


def main():
    card = json.load(open(sys.argv[1], encoding="utf-8"))
    g_pq = card["g_pq"]["1.3"]["g_pq_a_year"]
    eps = 0.835
    out = {"label": L.LABEL, "n_paths": N, "variants": {}}
    variants = {"cash_before_topup": (False, False), "rebuild_before_topup": (True, False),
                "cash_after_topup": (False, True), "rebuild_after_topup": (True, True)}
    keys = ("M1", "M4", "M5")
    for pk in ("do_nothing", "mix_B"):
        pol = POLICIES[pk]
        holds, sells = {}, {vk: {} for vk in variants}
        for mk in keys:
            m = E.MODELS[mk]
            gp = T.gen_paths(m, N, SEED + 1000)
            h = T.simulate_oil(m, pol, {"SLEEVE": {"V0": V0, "unf": UNF, "eps": eps, "beta_eq": BETA_EQ,
                                                   "alpha": -TAU, "g_pq": g_pq, "sell": False}},
                               n=N, seed=SEED, gen=gp)
            holds[mk] = h
            for vk, (rb, at) in variants.items():
                sells[vk][mk] = {}
                for b in BIDS:
                    s = T.simulate_oil(m, pol, {"SLEEVE": {"V0": V0, "unf": UNF, "eps": eps, "beta_eq": BETA_EQ,
                                                           "alpha": 0.0, "g_pq": 0.0, "sell": True, "bid": float(b),
                                                           "theta": 1.0, "cost": COST, "rebuild_beta": rb,
                                                           "after_topup": at}}, n=N, seed=SEED, gen=gp)
                    sells[vk][mk][str(b)] = (s["w_inv2"], float((s["w_tilde"] - h["w_tilde"]).mean()))
        ce_h = ce_growth([holds[mk]["w_inv2"] for mk in keys])
        for vk in variants:
            diff = np.array([ce_growth([sells[vk][mk][str(b)][0] for mk in keys]) - ce_h for b in BIDS])
            if diff[0] > 0:
                ps = float(BIDS[0])
            elif diff[-1] < 0:
                ps = float("nan")
            else:
                i = int(np.argmax(diff >= 0))
                ps = float(BIDS[i - 1] + (BIDS[i] - BIDS[i - 1]) * (-diff[i - 1]) / (diff[i] - diff[i - 1]))
            ew = float(np.mean([sells[vk][mk]["0.85"][1] for mk in keys]))
            out["variants"][f"{pk}|{vk}"] = {"p_star_M1M4M5": round(ps, 4), "E_dW_at_0.85_bn": round(ew, 4)}
            print(pk, vk, out["variants"][f"{pk}|{vk}"], flush=True)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
