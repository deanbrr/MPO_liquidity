"""G12: liability oil exposure, Gintschel-Scherer-style hurdles and an oil-delta budget. SYNTHETIC [I-calc/I-MC].

Inputs: g12_wrongway_sim_results.json (same folder). Re-simulates only the stream-03 oil process to get
sigma(dlnP) under the shock-type chain.

Hurdle (surplus mean-variance FOC with liability L = -L_eff * dlnP per unit NAV):
    mu_j - r = gamma * [Cov(r_j, r_p) + L_eff * Cov(r_j, dlnP)]
so the extra required return for asset j is  dmu_j = gamma * L_eff * Cov(r_j, dlnP).
L_eff = (b*h) * P(d* in band) * sum_k phi^k (1+r)^-k  (impulse of a log-oil shock on PV of draws, % of NAV)

Usage: python -I g12_hedging_demand.py <sim_json> <out_json>
"""
from __future__ import annotations

import json
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from g12_wrongway_sim import KAPPA, MU_O, PLR, PZ, SIG_O, ZI, _vec_trans, stationary  # noqa: E402


def sigma_dlnP(n=200000, T=12, seed=5):
    rng = np.random.default_rng(seed)
    z = rng.choice(6, size=n, p=stationary(PZ))
    x = np.full(n, np.log(PLR))
    dl = []
    for _ in range(T):
        zn = _vec_trans(rng, z)
        jump = np.where((zn == ZI["GW"]) & (rng.random(n) < 0.25), np.where(rng.random(n) < 0.5, np.log(1.3), np.log(0.7)), 0)
        xn = x + KAPPA * (np.log(PLR) - x) + MU_O[zn] + SIG_O[zn] * rng.standard_normal(n) + jump
        dl.append(xn - x)
        x, z = xn, zn
    dl = np.array(dl[2:]).ravel()
    return float(dl.std())


def main():
    sim = json.load(open(sys.argv[1], encoding="utf-8"))
    out_path = sys.argv[2]
    s_o = sigma_dlnP()
    phi, r, b = 1 - KAPPA, 0.06, 0.625
    annuity = 1.0 / (1.0 - phi / (1 + r))
    res = {"label": "SYNTHETIC [I-calc]", "sigma_dlnP_annual": round(s_o, 3), "annuity_factor": round(annuity, 3),
           "L_eff": {}, "hurdles": {}, "oil_delta_budget": {}}
    # L_eff by PBE (h path 11.3 -> 9.1) and by h (PBE 55)
    cases = {f"PBE{p}": (sim["runs"][f"stationary_PBE{p}_log"]["draw"]["p_inband_dstar"], 0.10) for p in ["44.8", "55.0", "65.0"]}
    for h in ["0.06", "0.091", "0.113", "0.15"]:
        cases[f"PBE55_h{h}"] = (sim["runs"][f"stationary_PBE55_h{h}"]["draw"]["p_inband_dstar"], float(h))
    for k, (pin, h) in cases.items():
        L = b * h * pin * annuity  # fraction of NAV per unit log oil
        res["L_eff"][k] = {"p_inband": pin, "h": h, "L_eff_pct_nav": round(100 * L, 2)}
    base = sim["runs"]["stationary_PBE55.0_log"]["segments"]
    for key, v in base.items():
        cov = v["corr_dlnP"] * v["vol"] * s_o
        row = {"name": v["name"], "corr_dlnP": v["corr_dlnP"], "vol": v["vol"], "cov_with_dlnP": round(cov, 4)}
        for case in ["PBE44.8", "PBE55.0", "PBE65.0", "PBE55_h0.06", "PBE55_h0.15"]:
            L = res["L_eff"][case]["L_eff_pct_nav"] / 100
            for g in [2, 4]:
                row[f"hurdle_{case}_gamma{g}"] = round(g * L * cov, 4)
        # GS min-variance hedge ratio (per unit NAV): -L_eff * Cov(r_j, dlnP)/Var(r_j)
        L55 = res["L_eff"]["PBE55.0"]["L_eff_pct_nav"] / 100
        row["mv_hedge_weight_PBE55"] = round(-L55 * cov / max(v["vol"] ** 2, 1e-9), 3)
        res["hurdles"][key] = row
    # oil-delta budget: barrel-equivalent deltas per $1bn from elasticities at $70 (N state)
    el = sim["elasticities"]["N_at_70"]
    liab_bbl_m = sim["liability_delta"]["linear_map_usd_bn_per_1usd_bbl"] * 1000  # m bbl equivalent
    for B in [5.0, 10.0, 20.0]:
        res["oil_delta_budget"][f"B{B:.0f}m_bbl"] = {
            "share_of_inband_draw_delta": round(B / liab_bbl_m, 3),
            **{f"max_usd_bn_{k}": round(B / v["bbl_equiv_per_usd1bn_mm"], 2) for k, v in el.items()}}
    res["context"] = {"inband_draw_delta_m_bbl_linear_map": round(liab_bbl_m, 1),
                      "smoothed_first_year_draw_delta_m_bbl_main_report": 100,
                      "overlay_put_spread_programme_m_bbl_main_report": [20, 40]}
    json.dump(res, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
