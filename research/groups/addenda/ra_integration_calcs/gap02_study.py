"""
gap_02 study driver: joint T1-T9 feasibility on the SYNTHETIC ADIC book, six stylised models.
SYNTHETIC - NOT ADIC DATA.

Steps (this script)
 1. Calibrate the canonical named stress s*(theta) against the six-model distribution of the 24-month
    funding gap G* (action-free ladder replica on every path, from today's drought + Gulf-war state).
 2. Grid over the levers (committed RCF, NAV facility, pacing level, stage-triggered pacing cut, owner-agreed
    band use, reserve size, pre-emptive amber sales, pre-emptive HF notices), 10k paths per model (screening),
    with the deterministic ladder heads (s*(theta), T4 readings), t0 DCR (T8) and capped LCR30 (T3) per mix.
Downstream: gap02_frontier.py (joint feasibility, CE price, frontier, 50k certification),
gap02_premium_frontier.py (exposure-neutral frontier), gap02_certify_extra.py (50k certification).
Run: <venv>/python.exe gap02_study.py   (writes gap02_grid_raw.json next to this file, ~4 minutes on 20 workers)
"""
from __future__ import annotations

import itertools
import json
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import t1_engine as E  # noqa: E402

OUT = os.path.join(HERE, "gap02_results.json")
N_SCREEN = 10000
N_CERT = 50000
KAPPA_OWN = 0.02          # fiscal-stress premium per $ of draw withheld, on top of the 10% accrual in W~ [I]
C_PACE_TV = {"M1": 0.064, "M2": 0.096, "M3": 0.022, "M4": 0.064, "M5": 0.050, "M6": 0.048}  # 2 x (PE - liquid CMA) [I]
KAPPA_GP = 0.02           # relationship / signalling cost per $ of red sale (C2 kappa^GP) [I]


def s_star(theta: float, **kw) -> E.Stress:
    """Canonical named stress family: DB -> SG in drought, vertex convention, canonical conventions.
    theta = 0: C3-type path (equity -30%, PE-type distributions 45% of drought, calls x1.0);
    theta = 1: C1 T1.4 literal severity (equity -40%, distributions 0, calls x1.5, 24 months)."""
    base = dict(name=f"s*(theta={theta:.2f})", eq_drawdown=0.30 + 0.10 * theta,
                dist_mult_pe=((24, 0.45 * (1 - theta)),), pc_cs_rates=(0.10, 0.07),
                call_mult=((24, 1.0 + 0.5 * theta),), draw_rates=(0.10, 0.10, 0.075),
                draw_basis="opening_reset", override_y2=0.0, fac_credit=0.80, navf_ltv=0.05,
                hf_pass=0.83, floor=0.04, crisis_months=int(round(18 + 6 * theta)))
    base.update(kw)
    return E.Stress(**base)


def t4_literal(**kw) -> E.Stress:
    base = dict(name="T4 literal (C1 T1.4)", eq_drawdown=0.40, dist_mult_pe=((24, 0.0),), pc_cs_rates=(0.10, 0.07),
                call_mult=((24, 1.5),), draw_rates=(0.10, 0.10, 0.075), draw_basis="opening_reset",
                fac_credit=0.50, navf_ltv=0.05, hf_pass=0.83, floor=0.04, crisis_months=24)
    base.update(kw)
    return E.Stress(**base)


def dcr_t0(pol: E.Policy, shock: str, hf_haircut: float = 0.5) -> float:
    """C3 H3b 12-month stressed coverage ratio at t0 for Z in {DB, GW, SG+PS} (hard >= 1.0, green >= 1.25)."""
    nav = E.NAV0
    enc = E.IM_N * E.N_SYN0 + E.OPP_IM0
    top = max(0.0, pol.reserve * nav - (E.TRE0 + 0.89 * pol.amber_t0 * 14 / 22 + 0.85 * pol.amber_t0 * 8 / 22 - enc))
    dm = E.LO0["dm"] - top / 0.998
    cash_extra = top + 0.89 * pol.amber_t0 * 14 / 22 + 0.85 * pol.amber_t0 * 8 / 22
    eq_h = 0.30 if shock == "DB" else 0.20
    num = (6.0 + cash_extra) + 4.0 * 0.97 + 5.0 * 0.90 - enc + dm * (1 - eq_h) + E.LO0["em"] * 0.65 \
        + E.LO0["fi"] * 0.90 + E.HF0 * (1 - hf_haircut)
    h_cpty = 0.20 if shock in ("DB", "GW", "SG+PS") else 0.10
    num += (1 - h_cpty) * pol.rcf
    pe_dist = {"DB": 0.30, "GW": 0.45, "SG+PS": 0.45}[shock] * 0.10 * 84.0 + 0.10 * 14 + 0.07 * 8
    hedge = {"DB": 3.0, "GW": 0.5, "SG+PS": 0.5}[shock]
    num += pe_dist + hedge
    calls = 0.28 * 1.25 * 38.0 + 0.10 * pol.pace + 0.28 * 0.5 * 0.9 * pol.pace
    cn = {"DB": 0.117 * E.N_SYN0 * 1.0 + 0.6, "GW": 0.05 * E.N_SYN0 + 0.6, "SG+PS": 0.08 * E.N_SYN0 + 0.6}[shock]
    draw = (0.05 if pol.band else 0.10) * nav
    ov = 0.035 * nav if shock == "GW" else 0.0
    den = draw + calls + cn + 0.0 + ov
    return num / den


def lcr30_t0(pol: E.Policy) -> float:
    """ADIC-LCR(30d) with Basel L2 (40%) / L2B (15%) caps and Treasury-controlled assets (GC2 D13)."""
    enc = E.IM_N * E.N_SYN0 + E.OPP_IM0
    top = max(0.0, pol.reserve * E.NAV0 - (E.TRE0 - enc))
    l1 = (6.0 - enc + top) + 4.0 * 0.98
    l2a = 5.0 * 0.85
    l2b = (E.LO0["dm"] - top) * 0.5
    adj15 = max(l2b - 15 / 85 * (l1 + l2a), l2b - 15 / 60 * l1, 0.0)
    adj40 = max((l2a + l2b - adj15) - 2 / 3 * l1, 0.0)
    num = l1 + l2a + l2b - adj15 - adj40
    out = (0.10 if not pol.band else 0.10) * E.NAV0 / 12 + 1.34 + 0.25 + 0.117 * E.N_SYN0 + 0.06 * E.N_SYN0 \
        + 0.005 * E.NAV0 + 0.375 + 0.0020 * E.NAV0 / 12
    inflow = min(0.45, 0.75 * out)
    return num / (out - inflow)


def run_policy(args):
    pol_kw, n = args
    pol = E.Policy(**pol_kw)
    res = {}
    for mk, m in E.MODELS.items():
        r = E.simulate(m, pol, n=n)
        res[mk] = {k: r[k] for k in ("p_red", "k_red", "cp_upper_red", "p_black", "p_black_12m",
                                     "cp_upper_black_12m", "p_band_12m", "p_floor4_breach", "p_restore_fail",
                                     "p_covenant", "p_navf_trig_12m", "max_debt_ratio_p99", "p_debt_gt10",
                                     "p_debt_gt15", "max_enc_p99", "mean_red_sales", "mean_red_loss",
                                     "mean_amber_loss", "mean_withheld", "mean_fees", "mean_interest",
                                     "mean_forced_paydown", "mean_commit_forgone", "mean_wtilde", "w_inv2",
                                     "median_first_red", "mean_shortfall", "p_restore_fail")}
    return pol_kw, res


def cost_bp(res: dict, ref: dict, models=None) -> dict:
    models = models or list(E.MODELS)
    g_ref = E.ce_growth({k: ref[k]["w_inv2"] for k in models})
    g_pol = E.ce_growth({k: res[k]["w_inv2"] for k in models})
    sim = (g_ref - g_pol) * 1e4
    outside = np.mean([(KAPPA_OWN * res[k]["mean_withheld"] + C_PACE_TV[k] * res[k]["mean_commit_forgone"]
                        + KAPPA_GP * res[k]["mean_red_sales"]) / E.NAV0 / 5 * 1e4 for k in models])
    owner = np.mean([KAPPA_OWN * res[k]["mean_withheld"] / E.NAV0 / 5 * 1e4 for k in models])
    pace = np.mean([C_PACE_TV[k] * res[k]["mean_commit_forgone"] / E.NAV0 / 5 * 1e4 for k in models])
    fees = np.mean([(res[k]["mean_fees"] + res[k]["mean_interest"]) / E.NAV0 / 5 * 1e4 for k in models])
    return dict(total=float(sim + outside), sim=float(sim), outside=float(outside), owner=float(owner),
                pace_tv=float(pace), fees_interest=float(fees))


def main():
    t_start = time.time()
    results = {"note": "SYNTHETIC / ILLUSTRATIVE - not ADIC data. Six stylised proxy models; see t1_engine.py."}

    # ---------------- 1. calibration of s*(theta)
    A = E.Policy("A")
    gstars = {}
    calib = {}
    for mk, m in E.MODELS.items():
        r = E.simulate(m, A, n=N_CERT, return_paths=True)
        gstars[mk] = r.pop("_gstar")
        r.pop("_gap8"), r.pop("_netneed8")
        calib[mk] = dict(p_red=r["p_red"], gstar_q=r["gstar_q"], netneed8_q=r["netneed8_q"],
                         crisis_share=r["crisis_share_lr"])
    mix = np.concatenate(list(gstars.values()))
    eps24 = 1 - (1 - 0.01) ** (8 / 20)
    targets = {
        "mixture_P99.6 (eps_R 1%, 24m share)": float(np.quantile(mix, 1 - eps24)),
        "worst_model_P99": float(max(np.quantile(g, 0.99) for g in gstars.values())),
        "worst_model_P99.6": float(max(np.quantile(g, 1 - eps24) for g in gstars.values())),
        "M1-M5_worst_P99.6": float(max(np.quantile(gstars[k], 1 - eps24) for k in ("M1", "M2", "M3", "M4", "M5"))),
        "mixture_P99": float(np.quantile(mix, 0.99)),
    }
    thetas = np.linspace(0, 1.2, 61)
    g_theta = [E.ladder(s_star(th), A)["gstar"] for th in thetas]
    theta_for = {}
    for name, tg in targets.items():
        th = float(np.interp(tg, g_theta, thetas)) if tg <= max(g_theta) else float("nan")
        theta_for[name] = th
    named = {}
    for key, s in {"T4_literal": t4_literal(), "T4_literal_floor8": t4_literal(floor=0.08),
                   "T4_literal_fixedusd": t4_literal(draw_basis="fixed_usd"),
                   "T4_literal_current": t4_literal(draw_basis="current"),
                   "T4_literal_hf_gated": t4_literal(hf_pass=0.0),
                   "T4_literal_hf50": t4_literal(hf_pass=0.5),
                   "T4_literal_noPCCS": t4_literal(pc_cs_rates=(0.0, 0.0)),
                   "T4_literal_worst_conventions": t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0,
                                                              pc_cs_rates=(0.0, 0.0)),
                   "G7_S1_shape": E.Stress("G7 S1", 0.39, ((18, 0.30),), (0.10, 0.07), ((12, 1.25),),
                                           (0.10, 0.10, 0.075), "fixed_usd", 0.0, 0.75, 0.05, 0.50, 0.04,
                                           instant=False),
                   "G7_S1_vertex_canonical": E.Stress("G7 S1 canonical", 0.39, ((18, 0.30),), (0.10, 0.07),
                                                      ((12, 1.25),), (0.10, 0.10, 0.075), "opening_reset", 0.0,
                                                      0.80, 0.05, 0.83, 0.04),
                   "C3_like": s_star(0.0)}.items():
        L = E.ladder(s, A)
        L["percentile_by_model"] = {mk: float((g <= L["gstar"]).mean()) for mk, g in gstars.items()}
        L["percentile_mixture"] = float((mix <= L["gstar"]).mean())
        named[key] = L
    results["calibration"] = dict(models={mk: dict(label=m.label) for mk, m in E.MODELS.items()},
                                  mc=calib, eps24=eps24, targets=targets, theta_for=theta_for,
                                  theta_grid=thetas.tolist(), gstar_theta=g_theta, named=named)
    print(f"[{time.time()-t_start:.0f}s] calibration done", json.dumps(targets), json.dumps(theta_for))

    # ---------------- 2. lever grid
    grid = []
    for rcf, navf, pace, cut, band, res_, amb, hft in itertools.product(
            (0.0, 5.0, 10.0, 15.0, 20.0), (0.0, 2.0), (12.0, 9.0, 6.0), (False, True), (False, True),
            (0.08, 0.10, 0.12, 0.14), (0.0, 3.0, 6.0), (0.0, 5.0)):
        name = (f"R{rcf:g}_N{navf:g}_P{pace:g}{'c' if cut else ''}_B{int(band)}_Q{int(round(res_*100))}"
                f"_A{amb:g}_H{hft:g}")
        grid.append(dict(name=name, rcf=rcf, navf=navf, pace=pace, pace_cut=cut, band=band, reserve=res_,
                         amber_t0=amb, hf_t0=hft))
    with ProcessPoolExecutor(max_workers=20) as ex:
        out = list(ex.map(run_policy, [(g, N_SCREEN) for g in grid], chunksize=4))
    print(f"[{time.time()-t_start:.0f}s] grid done: {len(out)} mixes")
    rows = []
    for kw, r in out:
        pol = E.Policy(**kw)
        lad = {f"{th:.2f}": E.ladder(s_star(th), pol)["min_head_tpf_24"] for th in THETAS_STORED}
        row = dict(kw=kw, models=r, ladder_head=lad,
                   t4_literal_head=E.ladder(t4_literal(), pol)["min_head_tpf_24"],
                   t4_as_written_head=E.ladder(t4_literal(floor=0.08), pol)["min_head_tpf_24"],
                   t4_critic_head=E.ladder(t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0,
                                                      pc_cs_rates=(0.0, 0.0)), pol)["min_head_tpf_24"],
                   dcr={z: dcr_t0(pol, z) for z in ("DB", "GW", "SG+PS")},
                   dcr_hf_gated={z: dcr_t0(pol, z, 1.0) for z in ("DB", "GW", "SG+PS")},
                   lcr30=lcr30_t0(pol))
        rows.append(row)
    raw = dict(note=results["note"], calibration=results["calibration"], grid=rows,
               reference="R0_N0_P12_B0_Q8_A0_H0", n_screen=N_SCREEN)
    with open(os.path.join(HERE, "gap02_grid_raw.json"), "w", encoding="utf-8") as fh:
        json.dump(raw, fh, default=float)
    print(f"[{time.time()-t_start:.0f}s] wrote gap02_grid_raw.json")


THETAS_STORED = (0.0, 0.25, 0.35, 0.42, 0.5, 0.6, 0.7, 0.76, 0.8, 0.9, 1.0)


if __name__ == "__main__":
    main()
