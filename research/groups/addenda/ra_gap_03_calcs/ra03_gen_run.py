"""RA gap 03, step 1: the canonical generator and owner-draw engine from today's state.

SYNTHETIC - NOT ADIC DATA. Outputs: monthly-matrix diagnostics, kappa coupling, Gulf-war duration law, state
occupancy from today against G12's stationary annual chain, the oil path against the 15-Oct-2026 strip, the
12-month draw, and the state-conditional effective liability oil exposure L_eff,t (with draw smoothing, the band,
the linear fiscal map and the IMF-fused 2027 balance), with comparisons that isolate each correction.

Usage: python -I ra03_gen_run.py <out_json>
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra03_lib as L  # noqa: E402

N = 40000
T = 12 * 11            # Oct-2026 .. Oct-2037 (10 calendar years of draws: 2027-2036)
YEARS = 10
SEED = 20261019
Z0 = np.array([0.03, 0.0, 0.0, 0.02, 0.10, 0.85])      # gap_04 s6.2 elicited posterior [I]
X0 = math.log(L.F1)
CHI0 = math.log(L.SPOT / L.F1)
R_DISC = 0.06                                         # G12's discount rate for L_eff


def build(k_gw=1.3, monthly="lsq", target_cris=0.1433):
    PZm, err = (L.monthly_lsq(L.PZ_A) if monthly == "lsq" else
                (L.monthly_root(L.PZ_A) if monthly == "root" else (L.monthly_linear(L.PZ_A), 0.0)))
    PS = L.s_chain_for_share(target_cris)
    K, kinfo = L.calibrate_kappa(PS, PZm)
    mode = "weibull" if k_gw is not None else "memoryless"
    g = L.Gen(PS, PZm, K, gw_mode=mode, gw_k=(k_gw or 1.0))
    return g, PZm, err, PS, K, kinfo


def occupancy(Z, months):
    sl = slice(months[0], months[1])
    return {z: round(float((Z[sl] == j).mean()), 4) for j, z in enumerate(L.ZN)}


def leff(g, seed, bump_month=0, x0=X0, chi0=CHI0, Z0p=Z0, S0=L.sLATE, form="linear", imf=True, n=N, d0=None,
         pbe_median=55.0, b=0.625):
    """L_eff for a +/-1% shock to the slow factor at bump_month: PV(draws) sensitivity, fraction of NAV per unit
    log oil, discounted to t0 and also restated at the shock date."""
    kw = dict(n=n, T=T, seed=seed, S0=S0, Z0=Z0p, x0=x0, chi0=chi0)
    if d0 is not None:
        kw["d0"] = d0
    base = g.simulate(**kw)
    db = L.owner_draws(base, YEARS, seed + 1, imf_fuse=imf, form=form, pbe_median=pbe_median, b=b)
    up = g.simulate(**kw, x_bump_at={bump_month: +0.01})
    dn = g.simulate(**kw, x_bump_at={bump_month: -0.01})
    du = L.owner_draws(up, YEARS, seed + 1, imf_fuse=imf, form=form, pbe_median=pbe_median, b=b,
                       fusion_ref=db["fusion"])
    dd = L.owner_draws(dn, YEARS, seed + 1, imf_fuse=imf, form=form, pbe_median=pbe_median, b=b,
                       fusion_ref=db["fusion"])
    pv_u, pv_d = L.pv_draws(du, R_DISC), L.pv_draws(dd, R_DISC)
    le = -(pv_u - pv_d) / 0.02
    by_year = [-(du["d"][k] - dd["d"][k]).mean() / 100 / 0.02 for k in range(YEARS)]
    return {"L_eff_t0_pv": float(le.mean()),
            "L_eff_at_shock_date": float(le.mean() * (1 + R_DISC) ** (bump_month / 12)),
            "draw_sensitivity_by_year_pct_nav_per_unit_log": [round(100 * v, 2) for v in by_year],
            "p_inband_by_year": [round(float(((du["inband"][k]) | (dd["inband"][k])).mean()), 3)
                                 for k in range(YEARS)]}


def main():
    out = {"label": L.LABEL, "asof": L.MARKET["asof"], "inputs": {
        "front_month": L.F1, "spot": L.SPOT, "chi0": round(CHI0, 4), "Z0": dict(zip(L.ZN, Z0.tolist())),
        "elapsed_gw_months": L.ELAPSED_GW_MONTHS, "paths": N}}

    # ---------------------------------------------------------------- monthly matrices
    R_root, e_root = L.monthly_root(L.PZ_A)
    R_lsq, e_lsq = L.monthly_lsq(L.PZ_A, R_root)
    R_lin = L.monthly_linear(L.PZ_A)
    out["monthly_matrix"] = {
        "clipped_principal_root_max_repair_error": round(e_root, 4),
        "least_squares_monthly_max_error": round(e_lsq, 4),
        "lsq_error_by_row_max": dict(zip(L.ZN, np.round(np.abs(np.linalg.matrix_power(R_lsq, 12) - L.PZ_A)
                                                       .max(axis=1), 4).tolist())),
        "twelve_month_persistence": {
            "annual_prior": dict(zip(L.ZN, np.diag(L.PZ_A).round(3).tolist())),
            "linearised_I_plus_(P-I)/12": dict(zip(L.ZN, np.diag(np.linalg.matrix_power(R_lin, 12)).round(3)
                                                   .tolist())),
            "least_squares_root": dict(zip(L.ZN, np.diag(np.linalg.matrix_power(R_lsq, 12)).round(3).tolist()))},
        "monthly_gw_stay": {"linearised": round(float(R_lin[L.iGW, L.iGW]), 4),
                            "least_squares_root": round(float(R_lsq[L.iGW, L.iGW]), 4)},
        "mean_gw_dwell_months": {"linearised": round(1 / (1 - R_lin[L.iGW, L.iGW]), 2),
                                 "least_squares_root": round(1 / (1 - R_lsq[L.iGW, L.iGW]), 2)},
        "gw_row_lsq": dict(zip(L.ZN, R_lsq[L.iGW].round(4).tolist())),
        "stationary": {"annual_prior": dict(zip(L.ZN, L.stationary(L.PZ_A).round(4).tolist())),
                       "lsq_root": dict(zip(L.ZN, L.stationary(R_lsq).round(4).tolist()))}}

    # ---------------------------------------------------------------- coupling (base: M1 crisis share)
    g, PZm, _, PS, K, kinfo = build(k_gw=1.3)
    out["coupling"] = {"kappa": {s: dict(zip(L.ZN, K[i].round(3).tolist())) for i, s in enumerate(L.SN)},
                       "a_cris_db": round(kinfo["a_cris_db"], 3), "b_noncris_db": round(kinfo["b_noncris_db"], 3),
                       "c_cris_sg": round(kinfo["c_cris_sg"], 3), "g_cris_boom": round(kinfo["g_cris_boom"], 3),
                       "e_noncris_ss": round(kinfo["e_noncris_ss"], 3),
                       "target_Z": dict(zip(L.ZN, kinfo["target_pz"].round(4).tolist())),
                       "stationary_Z": dict(zip(L.ZN, kinfo["pz"].round(4).tolist())),
                       "stationary_S": dict(zip(L.SN, kinfo["ps"].round(4).tolist())),
                       "P(CRIS|Z)": dict(zip(L.ZN, kinfo["p_cris_given_z"].round(3).tolist())),
                       "S_chain_monthly_diag": dict(zip(L.SN, np.diag(PS).round(4).tolist()))}

    # ---------------------------------------------------------------- GW duration law from today
    gw = {}
    variants = [("memoryless_linearised", None, "lin"), ("memoryless_lsq_root", None, "lsq")] + \
        [(f"weibull_k{k}", k, "lsq") for k in (0.8, 1.3, 1.6, 2.2)]
    for name, k, mm in variants:
        gg, *_ = build(k_gw=k, monthly=mm)
        sim = gg.simulate(n=N, T=40, seed=SEED, S0=L.sLATE, Z0=np.eye(6)[L.iGW], x0=X0, chi0=CHI0)
        Zs = sim["Z"]
        first_exit = np.argmax(Zs != L.iGW, axis=0).astype(float)
        never = (Zs == L.iGW).all(axis=0)
        first_exit[never] = np.nan
        gw[name] = {"P(GW) Jan-27 / Apr-27 / Jul-27 / Oct-27": [round(float((Zs[m] == L.iGW).mean()), 3)
                                                                for m in (3, 6, 9, 12)],
                    "share_of_2027_in_GW": round(float((Zs[3:15] == L.iGW).mean()), 3),
                    "median_months_to_first_exit": float(np.nanmedian(first_exit)),
                    "mean_months_to_first_exit": round(float(np.nanmean(first_exit)), 2),
                    "share_of_exits_to_SG": round(float((Zs[np.minimum(np.nan_to_num(first_exit, nan=0).astype(int),
                                                                       40), np.arange(N)] == L.iSG).mean()), 3)}
    out["gw_duration_from_today"] = gw
    out["gw_reference_points"] = {"gap_04_memoryless_linearised_share_2027": 0.49,
                                  "imf_hormuz_reopening_march_2027_share_2027": 0.17}

    # ---------------------------------------------------------------- state occupancy and oil from today
    sim = g.simulate(n=N, T=T, seed=SEED, S0=L.sLATE, Z0=Z0, x0=X0, chi0=CHI0)
    occ = {f"{2027 + k}": occupancy(sim["Z"], (3 + 12 * k, 15 + 12 * k)) for k in range(5)}
    occ["2027-2031"] = occupancy(sim["Z"], (3, 63))
    wrong = {k: round(v["SG"] + v["DB"], 4) for k, v in occ.items()}
    out["occupancy_from_today"] = {"by_year": occ, "SG+DB": wrong,
                                   "GW": {k: v["GW"] for k, v in occ.items()},
                                   "G12_stationary_annual_chain": {"SG+DB": 0.2248, "GW": 0.0382},
                                   "canonical_stationary": {"SG+DB": round(float(kinfo["pz"][L.iSG] +
                                                                               kinfo["pz"][L.iDB]), 4),
                                                            "GW": round(float(kinfo["pz"][L.iGW]), 4)},
                                   "P(S=CRIS) 2027-2031": round(float((sim["S"][3:63] == L.sCRIS).mean()), 4)}
    P = sim["P"]
    ms, ps = L.strip_months()
    sim_ss = g.simulate(n=N, T=60, seed=SEED, S0=L.sLATE, Z0=Z0, x0=X0, chi0=CHI0, chi_kappa=L.KAPPA_CHI_SS)
    sim_spot = g.simulate(n=N, T=60, seed=SEED, S0=L.sLATE, Z0=Z0, x0=math.log(L.SPOT), chi0=0.0)
    out["oil_vs_strip"] = {
        "contract_months": list(L.MARKET["strip"].keys()),
        "strip": ps.tolist(),
        "model_median": [round(float(np.median(P[m])), 2) for m in ms],
        "model_mean": [round(float(P[m].mean()), 2) for m in ms],
        "model_median_with_schwartz_smith_chi_halflife": [round(float(np.median(sim_ss["P"][m])), 2)
                                                          for m in ms if m <= 60],
        "model_median_spot_start": [round(float(np.median(sim_spot["P"][m])), 2) for m in ms if m <= 60],
        "spot_start_2027_avg_mean": round(float(sim_spot["P"][3:15].mean()), 1),
        "brent_2027_avg_mean_p10_p50_p90": [round(float(P[3:15].mean()), 1)] +
                                          np.percentile(P[3:15].mean(axis=0), [10, 50, 90]).round(1).tolist(),
        "strip_2027_avg": round(float(np.mean([L.MARKET["strip"][f"2027-{m:02d}"] for m in range(1, 13)])), 2),
        "eia_steo_2027": L.MARKET["steo_oct26_brent_q"]["2027"],
        "P(annual avg < 64) by year 2027-2031": [round(float((P[3 + 12 * k:15 + 12 * k].mean(axis=0) < 64).mean()),
                                                       3) for k in range(5)]}

    dr = L.owner_draws(sim, YEARS, SEED + 1)
    d12 = (5.8 / 4 + 3 * dr["d"][0] / 4)
    out["draws"] = {"12m_draw_usd_bn_mean_p90": [round(float(d12.mean() / 100 * 177), 2),
                                                 round(float(np.percentile(d12, 90) / 100 * 177), 2)],
                    "mean_rate_by_year": [round(float(dr["d"][k].mean()), 2) for k in range(YEARS)],
                    "P(rate>=9.5%) by year": [round(float((dr["d"][k] >= 9.5).mean()), 4) for k in range(5)],
                    "P(d* in band) by year": [round(float(dr["inband"][k].mean()), 3) for k in range(YEARS)],
                    "gap_04_reference_12m_usd_bn": "9.9-10.8"}

    # ---------------------------------------------------------------- L_eff,t
    le = {}
    le["canonical_t0"] = leff(g, SEED + 11, 0)
    for mth in (12, 24, 36):
        le[f"canonical_forward_start_{mth}m"] = leff(g, SEED + 11, mth)
    hp = [le["canonical_t0"]["L_eff_at_shock_date"]] + \
        [le[f"canonical_forward_start_{m}m"]["L_eff_at_shock_date"] for m in (12, 24, 36)]
    le["holding_period_avg_years_0_3"] = float(np.mean(hp))
    # comparisons that isolate each correction (all from the same seed)
    g_lin, *_ = build(k_gw=None, monthly="lin")
    g_mem, *_ = build(k_gw=None, monthly="lsq")
    stat = L.stationary(L.joint_chain(PS, PZm, K)).reshape(4, 6)
    le["memoryless_linearised_chain_t0"] = leff(g_lin, SEED + 11, 0)
    le["memoryless_lsq_chain_t0"] = leff(g_mem, SEED + 11, 0)
    le["spot_start_t0"] = leff(g, SEED + 11, 0, x0=math.log(L.SPOT), chi0=0.0)
    le["no_imf_fusion_t0"] = leff(g, SEED + 11, 0, imf=False)
    le["gap04_per_path_shrink_fusion_t0"] = leff(g, SEED + 11, 0, imf="shrink")
    le["log_fiscal_map_t0"] = leff(g, SEED + 11, 0, form="log")
    le["stationary_start_normal_oil_70"] = leff(g, SEED + 11, 0, x0=L.LN70, chi0=0.0,
                                                Z0p=stat.sum(axis=0), S0=stat.sum(axis=1), d0=0.0, imf=False)
    le["stationary_start_log_map_no_smoothing_check"] = "see G12 formula: b*h*P(in band)*annuity = 9.25%"
    le["pbe_45_t0"] = leff(g, SEED + 11, 0, pbe_median=45.0)
    le["pbe_65_t0"] = leff(g, SEED + 11, 0, pbe_median=65.0)
    le["G12_reference"] = {"L_eff_pct_nav_stationary_log_map_pbe55": 9.25, "budget_scaling_reference": 9.3}
    out["L_eff"] = le
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=float)
    print(json.dumps({k: out[k] for k in ("monthly_matrix", "coupling")}, indent=1, default=float)[:3000])
    print(json.dumps(out["gw_duration_from_today"], indent=1))
    print(json.dumps(out["occupancy_from_today"]["SG+DB"]), json.dumps(out["occupancy_from_today"]["GW"]))
    print(json.dumps(out["oil_vs_strip"], default=float))
    print(json.dumps(out["draws"]))
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items()
                                                             if kk in ("L_eff_t0_pv", "L_eff_at_shock_date")})
                      for k, v in le.items()}, indent=1, default=float))


if __name__ == "__main__":
    main()
