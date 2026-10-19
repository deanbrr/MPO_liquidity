"""
ra_gap_04 - how much resolved history is needed to score a SEGMENT kappa?   ALL OUTPUTS SYNTHETIC - NOT ADIC DATA.

kappa := w80(true) / w80(stated) (groups gap_02 sec. 5). Scored on realized outcomes: z = (y - f) / sd_stated with
sd_stated = (P90 - P10) / 2.563 from the archived cases (brief sec. 9). Realized errors share a segment-date common
component, so standardized errors have intra-cluster correlation rho; squared errors have rho^2 (Gaussian).
Census: 115 positions in 8 segments (CORE_RE 9, VA_RE 17, RE_DEV 2, GCC_RE 3, CORE_INF 16, VA_INF 38, GF_INF 6,
ENR 24); one resolved annual forecast per position per year.
1. Power to detect kappa_s != kappa_g (the sec. 8.4 table differences: x1.20 = 1.67 -> 2.00, x1.33 = 1.67 -> 2.22,
   x0.83 = 2.00 -> 1.67) with a date-clustered log-ratio t test (t_{D-1}, 5% two-sided), by segment, rho, years D.
2. Years needed for 80% power.
3. n_eff accrual per segment per year for bias (rho) and for kappa (rho^2); years to n_eff = 20.
4. Estimator comparison when truth has segment heterogeneity tau in {0, 0.10, 0.25} (log scale): raw segment
   kappa, one group kappa_g, empirical-Bayes random effects (DL tau), fixed-tau random effects (tau = 0.10);
   RMSE of ln kappa_s and the resulting coverage error of segment 80% bands.
Run:  .venv\\Scripts\\python.exe -I -B ra04_kappa_power.py  -> ra04_kappa_power_results.json
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
OUT = HERE / "ra04_kappa_power_results.json"
SYN = "SYNTHETIC - NOT ADIC DATA"
SEGS = ["CORE_RE", "VA_RE", "RE_DEV", "GCC_RE", "CORE_INF", "VA_INF", "GF_INF", "ENR"]
NS = np.array([9, 17, 2, 3, 16, 38, 6, 24])
KG = 1.75
R = 4000
rng = np.random.default_rng(20261019)


def sim_z(D, rho, kap):
    """z[s] arrays (R, D, n_s): kappa_s x (sqrt(rho) c_sd + sqrt(1-rho) e)."""
    out = []
    for s, n in enumerate(NS):
        c = rng.standard_normal((R, D, 1))
        e = rng.standard_normal((R, D, n))
        out.append(kap[s] * (math.sqrt(rho) * c + math.sqrt(1 - rho) * e))
    return out


def log_kappa_and_var(zlist):
    """Date-clustered estimate of ln kappa from squared standardized errors: kappa^2 = mean_d q_d."""
    q = np.concatenate([(z ** 2).mean(2, keepdims=True) if z.ndim == 3 else z for z in zlist], axis=2).mean(2) \
        if len(zlist) > 1 else (zlist[0] ** 2).mean(2)
    D = q.shape[1]
    k2 = q.mean(1)
    v_k2 = q.var(1, ddof=1) / D
    return 0.5 * np.log(k2), v_k2 / (4 * k2 ** 2)


def seg_q(z):
    return (z ** 2).mean(2)                               # (R, D)


def power_table():
    res = {}
    for rho in (0.1, 0.3, 0.5):
        for D in (4, 8, 12, 20, 40):
            for ratio in (1.20, 1.33, 0.83, 1.00):
                row = {}
                for s in range(8):
                    kap = np.full(8, KG)
                    kap[s] = KG * ratio
                    z = sim_z(D, rho, kap)
                    qs = seg_q(z[s])
                    # rest of the group: equal-weighted pooled squared errors of the other segments by date
                    qr = np.mean([seg_q(z[j]) * NS[j] for j in range(8) if j != s], axis=0) / \
                         np.mean([NS[j] for j in range(8) if j != s])
                    ks, kr = qs.mean(1), qr.mean(1)
                    vs = qs.var(1, ddof=1) / D / (4 * ks ** 2)
                    vr = qr.var(1, ddof=1) / D / (4 * kr ** 2)
                    t = (0.5 * np.log(ks) - 0.5 * np.log(kr)) / np.sqrt(vs + vr)
                    crit = stats.t.ppf(0.975, D - 1)
                    row[SEGS[s]] = float(np.mean(np.abs(t) > crit))
                res[f"rho={rho}|D={D}|ratio={ratio}"] = row
    return res


def years_for_power(pt, target=0.80):
    out = {}
    for rho in (0.1, 0.3, 0.5):
        for ratio in (1.20, 1.33, 0.83):
            row = {}
            for s in SEGS:
                yrs = None
                for D in (4, 8, 12, 20, 40):
                    if pt[f"rho={rho}|D={D}|ratio={ratio}"][s] >= target:
                        yrs = D
                        break
                row[s] = yrs if yrs is not None else ">40"
            out[f"rho={rho}|ratio={ratio}"] = row
    return out


def neff_table():
    out = {}
    for rho in (0.1, 0.3, 0.5):
        nb = NS / (1 + (NS - 1) * rho)
        nk = NS / (1 + (NS - 1) * rho ** 2)
        out[f"rho={rho}"] = dict(
            bias_neff_per_year={s: round(float(x), 2) for s, x in zip(SEGS, nb)},
            kappa_neff_per_year={s: round(float(x), 2) for s, x in zip(SEGS, nk)},
            years_to_neff20_bias={s: round(float(20 / x), 1) for s, x in zip(SEGS, nb)},
            group_bias_neff_per_year=round(float(nb.sum()), 1), group_kappa_neff_per_year=round(float(nk.sum()), 1))
    return out


def estimator_comparison():
    out = {}
    for tau in (0.0, 0.10, 0.25):
        for D in (4, 8, 20):
            for rho in (0.3,):
                u = rng.standard_normal((R, 8)) * tau
                lk_true = math.log(KG) + u                                     # (R, 8)
                qs = []
                for s, n in enumerate(NS):
                    c = rng.standard_normal((R, D, 1))
                    e = rng.standard_normal((R, D, n))
                    z = np.exp(lk_true[:, s])[:, None, None] * (math.sqrt(rho) * c + math.sqrt(1 - rho) * e)
                    qs.append((z ** 2).mean(2))
                q = np.stack(qs, 1)                                             # (R, 8, D)
                k2 = q.mean(2)
                lk = 0.5 * np.log(k2)
                v = q.var(2, ddof=1) / D / (4 * k2 ** 2)
                w = NS / NS.sum()
                lkg = 0.5 * np.log((k2 * w[None, :]).sum(1))                   # one group kappa (position-weighted)
                wt = 1 / v
                mu = (wt * lk).sum(1) / wt.sum(1)
                Q = (wt * (lk - mu[:, None]) ** 2).sum(1)
                cden = wt.sum(1) - (wt ** 2).sum(1) / wt.sum(1)
                t2 = np.maximum(0, (Q - 7) / cden)
                eb = mu[:, None] + t2[:, None] / (t2[:, None] + v) * (lk - mu[:, None])
                fx = mu[:, None] + 0.01 / (0.01 + v) * (lk - mu[:, None])
                ests = dict(raw_segment=lk, one_group=np.repeat(lkg[:, None], 8, 1), eb_dl=eb, fixed_tau_0p10=fx)
                row = {}
                for k, est in ests.items():
                    err = est - lk_true
                    cov = 2 * stats.norm.cdf(Z80 * np.exp(est - lk_true)) - 1       # realized coverage of the 80% band
                    row[k] = dict(rmse_lnkappa=float(np.sqrt((err ** 2).mean())),
                                  mean_abs_cov_err=float(np.abs(cov - 0.80).mean()),
                                  worst_seg_cov_mean=float(cov.mean(0).min()),
                                  group_cov=float((cov * w[None, :]).sum(1).mean()))
                out[f"tau={tau}|D={D}|rho={rho}"] = row
    return out


Z80 = 1.2815516


def main():
    pt = power_table()
    res = dict(label=SYN, R=R, kappa_g=KG, census=dict(zip(SEGS, NS.tolist())), power=pt,
               years_for_80pct_power=years_for_power(pt), neff=neff_table(), estimators=estimator_comparison())
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    for k, v in res["years_for_80pct_power"].items():
        print(k, v)
    print("size (ratio 1.00), rho 0.3, D 8:", pt["rho=0.3|D=8|ratio=1.0"])
    for k, v in res["neff"].items():
        print(k, "group bias/kappa neff per year", v["group_bias_neff_per_year"], v["group_kappa_neff_per_year"],
              "years to 20 (bias):", v["years_to_neff20_bias"])
    for k, v in res["estimators"].items():
        print(k, {e: (round(x["rmse_lnkappa"], 3), round(x["mean_abs_cov_err"], 3)) for e, x in v.items()})
    print("wrote", OUT, SYN)


if __name__ == "__main__":
    main()
