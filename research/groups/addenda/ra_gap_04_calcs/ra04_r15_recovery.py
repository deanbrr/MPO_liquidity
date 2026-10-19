"""
ra_gap_04 - R15 recovery test of PACE and UNFUNDED by vintage for the sealed Real Assets closed-end book.
ALL OUTPUTS SYNTHETIC - NOT ADIC DATA.

Truth (per sector RE / INF / ENR): the sealed vintage commitments (seal_ra_ce_results.json) split into funds
(census position counts 14 / 25 / 16, at least one per vintage); fund call hazard
  lambda_{f,t} = -ln(1 - RC_s[age-year]) x m^C(regime_t) x exp(zeta_f) x M_t,  zeta_f ~ N(0, 0.30^2) [I],
  quarterly call = U (1 - exp(-lambda dt)) x xi,  xi ~ Gamma(4, 1/4) (lumpy calls, CV 0.5) [I], capped at U;
  unfunded lapses after age-year L_s (RE/ENR 6, INF 7); first close in a random quarter of the vintage year.
Observation layer (what ADIC holds): per fund commitment, vintage, quarterly calls and contractual unfunded to the
census date 2026-09-30, and the regime history.
Estimands: PACE = calls in the next 4 and next 8 quarters; UNFUNDED = callable unfunded (all future calls), for the
book and by vintage bucket (2012-19, 2020-22, 2023-24, 2025-26).
Estimator (what the lab would run): exposure-weighted call rates by age-year x regime factorised as lambda_k x m_e
(log-additive, iterative), fund effects by shrunken observed/expected call ratios, sigma_zeta by moments; projection by
simulation under the drought regime (or the stated scenario); parameter uncertainty by a fund-cluster bootstrap (B).
90% predictive intervals. Gate (V17, +/-5pp): coverage in [0.85, 0.95] and |bias| <= 5% for the book totals.
Variants (truth; the estimator is unchanged): sealed history; mature/flat, +10% and +20% commitment histories
(seal truth variants, same NAV); lapse two years later than the engine default (learned from old funds); recallable
distributions (estimator ignores future recycling); T4' call acceleration x1.38 for 8 quarters, scenario-conditional
(estimator applies x1.38) and unannounced (estimator assumes the drought regime).
Run:  .venv\\Scripts\\python.exe -I -B ra04_r15_recovery.py [R] [B]  -> ra04_r15_recovery_results.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "ra04_r15_recovery_results.json"
SYN = "SYNTHETIC - NOT ADIC DATA"
R = int(sys.argv[1]) if len(sys.argv) > 1 else 200
B = int(sys.argv[2]) if len(sys.argv) > 2 else 200
DT = 0.25
VINT = list(range(2012, 2027))
QC = 2026 * 4 + 2                          # census quarter 2026Q3
H = 40                                     # projection quarters
REG = {y: "N" for y in range(2012, 2020)}
REG.update({2020: "D", 2021: "O", 2022: "D", 2023: "D", 2024: "D", 2025: "D", 2026: "D"})
MC = dict(O=1.2, N=1.0, D=0.75, F=0.6)
E_IDX = {"N": 0, "O": 1, "D": 2}
SECT = {"RE": dict(rc=[0.25, 0.30, 0.35, 0.40, 0.40, 0.40], lapse=6, n_funds=14),
        "INF": dict(rc=[0.20, 0.25, 0.30, 0.35, 0.35, 0.35, 0.35], lapse=7, n_funds=25),
        "ENR": dict(rc=[0.25, 0.30, 0.35, 0.40, 0.40, 0.40], lapse=6, n_funds=16)}
SIG_Z = 0.30
KMAX = 10                                  # age-year cells 0..9 (9 = 9+)
BUCKETS = {"2012-19": (2012, 2019), "2020-22": (2020, 2022), "2023-24": (2023, 2024), "2025-26": (2025, 2026)}


def load_seal():
    return json.loads((HERE / "seal_ra_ce_results.json").read_text(encoding="utf-8"))


def funds_for(s, commitments):
    c = np.array([commitments[str(v)] if isinstance(commitments, dict) and str(v) in commitments
                  else commitments[i] if not isinstance(commitments, dict) else commitments[v]
                  for i, v in enumerate(VINT)], dtype=float)
    c_tot = c * np.array([0.75 if v == 2026 else 1.0 for v in VINT])
    n = np.maximum(1, np.round(SECT[s]["n_funds"] * c_tot / c_tot.sum())).astype(int)
    vint, comm = [], []
    for v, cv, nv in zip(VINT, c_tot, n):
        for _ in range(nv):
            vint.append(v)
            comm.append(cv / nv)
    return np.array(vint), np.array(comm)


def rate(s, k, lapse):
    rc = SECT[s]["rc"]
    lam = np.where(k < len(rc), -np.log(1 - np.array(rc + [rc[-1]] * 20)[np.minimum(k, 25)]), -math.log(1 - rc[-1]))
    return np.where(k < lapse, lam, 0.0)


def simulate_truth(rng, s, vint, comm, var):
    """History to the census quarter and future calls (truth). Returns observation arrays and truth outcomes."""
    nf = len(vint)
    q0 = vint * 4 + np.where(vint == 2026, rng.integers(0, 3, nf), rng.integers(0, 4, nf))
    zeta = rng.normal(0, SIG_Z, nf)
    lapse = SECT[s]["lapse"] + var.get("lapse_shift", 0)
    U = comm.copy()
    rows = []
    lapse_obs = np.full(nf, np.nan)          # age at which unfunded was released without a call (observable)
    paid = np.zeros(nf)
    for q in range(2012 * 4, QC + 1):
        e = REG[q // 4]
        active = q >= q0
        age = (q - q0) * DT
        k = np.floor(age + 1e-9).astype(int)
        lam = rate(s, k, lapse) * MC[e] * np.exp(zeta)
        p = 1 - np.exp(-lam * DT)
        xi = rng.gamma(4.0, 0.25, nf)
        call = np.where(active, np.minimum(U, U * p * xi), 0.0)
        for f in np.where(active & (U > 1e-12))[0]:
            rows.append((f, min(k[f], KMAX - 1), E_IDX[e], U[f], call[f]))
        U = U - call
        paid += call
        if var.get("recallable", 0.0):
            rec = np.where(active & (age < 4.0) & (rng.random(nf) < 0.5), var["recallable"] * paid * DT, 0.0)
            U = U + rec
        rel = active & (age + DT >= lapse) & (U > 1e-12) & np.isnan(lapse_obs)
        lapse_obs = np.where(rel, age + DT, lapse_obs)
        U = np.where(active & (age + DT >= lapse), 0.0, U)
    U_census = U.copy()
    # contractual unfunded as reported (lapsed commitments still show as unfunded until the fund term ends)
    fut = np.zeros((nf, H))
    Uf = U.copy()
    paid_f = paid.copy()
    for h in range(H):
        q = QC + 1 + h
        age = (q - q0) * DT
        k = np.floor(age + 1e-9).astype(int)
        mult = var.get("future_mult", 1.0) if h < 8 else 1.0
        lam = rate(s, k, lapse) * MC["D"] * np.exp(zeta) * mult
        p = 1 - np.exp(-lam * DT)
        xi = rng.gamma(4.0, 0.25, nf)
        call = np.minimum(Uf, Uf * p * xi)
        fut[:, h] = call
        Uf = Uf - call
        paid_f += call
        if var.get("recallable", 0.0):
            Uf = Uf + np.where((age < 4.0) & (rng.random(nf) < 0.5), var["recallable"] * paid_f * DT, 0.0)
        Uf = np.where(age + DT >= lapse, 0.0, Uf)
    obs = np.array(rows) if rows else np.zeros((0, 5))
    return dict(q0=q0, obs=obs, U_census=U_census, fut=fut, comm=comm, vint=vint, lapse_obs=lapse_obs)


def estimate(obs, nf, weights=None):
    """Exposure-weighted call rates by age-year x regime, factorised lambda_k x m_e (m_N = 1); fund effects."""
    if weights is None:
        weights = np.ones(nf)
    f = obs[:, 0].astype(int)
    k = obs[:, 1].astype(int)
    e = obs[:, 2].astype(int)
    U0 = obs[:, 3]
    c = obs[:, 4]
    w = weights[f]
    y = -np.log(np.maximum(1 - c / np.maximum(U0, 1e-12), 1e-6)) / DT       # implied quarterly hazard (annualised)
    num = np.zeros((KMAX, 3))
    den = np.zeros((KMAX, 3))
    np.add.at(num, (k, e), w * U0 * y)
    np.add.at(den, (k, e), w * U0)
    lam = np.full(KMAX, 0.2)
    m = np.ones(3)
    for _ in range(30):
        lam = (num.sum(1) + 1e-12) / ((den * m[None, :]).sum(1) + 1e-12)
        m = (num.sum(0) + 1e-12) / ((den * lam[:, None]).sum(0) + 1e-12)
        m = m / m[0]
    # unobserved high age cells inherit the last observed rate
    seen = den.sum(1) > 0
    for kk in range(1, KMAX):
        if not seen[kk]:
            lam[kk] = lam[kk - 1]
    # fund effects: observed vs expected calls, shrunk
    exp_c = U0 * (1 - np.exp(-lam[k] * m[e] * DT))
    oc = np.bincount(f, weights=c, minlength=nf)
    ec = np.bincount(f, weights=exp_c, minlength=nf)
    nq = np.bincount(f, minlength=nf)
    lr = np.log(np.maximum(oc, 1e-9) / np.maximum(ec, 1e-9))
    okf = (ec > 1e-6) & (nq >= 2)
    v_noise = 0.25 / np.maximum(nq, 1)                                          # Gamma(4) noise: var(log mean) ~ 0.25/n
    s2 = max(0.0, float(np.var(lr[okf]) - np.mean(v_noise[okf]))) if okf.sum() > 2 else SIG_Z ** 2
    wz = np.where(okf, s2 / (s2 + v_noise), 0.0)
    zhat = wz * np.where(okf, lr, 0.0)
    return dict(lam=lam, m=m, zhat=zhat, s2=s2, wz=wz)


def lapse_estimate(lapse_obs, weights, prior):
    """Lapse age from observed release events (unfunded released without a call); prior if none observed."""
    x = np.repeat(lapse_obs, weights.astype(int))
    x = x[~np.isnan(x)]
    return float(np.median(x)) if x.size else prior


def project(rng, est, q0, U, nB, var_est, lapse_hat=None):
    """Simulate future calls for each fund under estimated rates; returns (nB, nf, H). With lapse_hat, unfunded is
    released (no further calls) once a fund reaches the estimated lapse age; without it (naive), the last observed
    call rate is extrapolated."""
    nf = len(q0)
    out = np.zeros((nB, nf, H))
    Uc = np.repeat(U[None, :], nB, axis=0)
    resid_sd = np.sqrt(np.maximum(est["s2"] * (1 - est["wz"]), 0.0))
    z = est["zhat"][None, :] + resid_sd[None, :] * rng.standard_normal((nB, nf))
    mD = est["m"][E_IDX["D"]]
    for h in range(H):
        q = QC + 1 + h
        age = (q - q0) * DT
        k = np.minimum(np.floor(age + 1e-9).astype(int), KMAX - 1)
        mult = var_est.get("future_mult", 1.0) if h < 8 else 1.0
        lam = est["lam"][k][None, :] * mD * np.exp(z) * mult
        p = 1 - np.exp(-lam * DT)
        xi = rng.gamma(4.0, 0.25, (nB, nf))
        call = np.minimum(Uc, Uc * p * xi)
        if lapse_hat is not None:
            call = np.where((age < lapse_hat)[None, :], call, 0.0)
        out[:, :, h] = call
        Uc = Uc - call
        if lapse_hat is not None:
            Uc = np.where((age + DT >= lapse_hat)[None, :], 0.0, Uc)
    return out


def run_variant(s, vint, comm, var, var_est, seed, lapse_model=True):
    rng = np.random.default_rng(seed)
    nf = len(vint)
    hits = {k: [] for k in ("pace4", "pace8", "unf")}
    bias = {k: [] for k in ("pace4", "pace8", "unf")}
    bhits = {b: {k: [] for k in ("pace8", "unf")} for b in BUCKETS}
    contractual_ratio = []
    for _ in range(R):
        tr = simulate_truth(rng, s, vint, comm, var)
        truth = dict(pace4=tr["fut"][:, :4].sum(), pace8=tr["fut"][:, :8].sum(), unf=tr["fut"].sum())
        contractual_ratio.append(truth["unf"] / max(tr["U_census"].sum(), 1e-9))
        sims = []
        for b in range(B // 10):                       # bootstrap over funds; 10 process draws per resample
            wts = np.bincount(rng.integers(0, nf, nf), minlength=nf).astype(float)
            est = estimate(tr["obs"], nf, wts)
            lh = lapse_estimate(tr["lapse_obs"], wts, SECT[s]["lapse"]) if lapse_model else None
            sims.append(project(rng, est, tr["q0"], tr["U_census"], 10, var_est, lh))
        sims = np.concatenate(sims, axis=0)            # (B, nf, H)
        pred = dict(pace4=sims[:, :, :4].sum((1, 2)), pace8=sims[:, :, :8].sum((1, 2)), unf=sims.sum((1, 2)))
        for kq in hits:
            lo, hi = np.percentile(pred[kq], [5, 95])
            hits[kq].append(lo <= truth[kq] <= hi)
            bias[kq].append((np.median(pred[kq]) - truth[kq]) / max(truth[kq], 1e-9))
        for bname, (y0, y1) in BUCKETS.items():
            sel = (vint >= y0) & (vint <= y1)
            if not sel.any():
                continue
            for kq, (a, bq) in (("pace8", (0, 8)), ("unf", (0, H))):
                t_ = tr["fut"][sel, a:bq].sum()
                p_ = sims[:, sel, a:bq].sum((1, 2))
                lo, hi = np.percentile(p_, [5, 95])
                bhits[bname][kq].append(bool(lo <= t_ <= hi) if t_ > 1e-6 or hi > 1e-6 else True)
    res = {k: dict(coverage90=float(np.mean(v)), bias_median=float(np.median(bias[k])),
                   bias_mean=float(np.mean(bias[k]))) for k, v in hits.items()}
    res["gate_V17"] = bool(all(0.85 <= res[k]["coverage90"] <= 0.95 and abs(res[k]["bias_mean"]) <= 0.05
                              for k in ("pace4", "pace8", "unf")))
    res["callable_over_contractual_unfunded"] = float(np.mean(contractual_ratio))
    res["buckets"] = {b: {k: (float(np.mean(v)) if v else None) for k, v in d.items()} for b, d in bhits.items()}
    return res


def main():
    seal = load_seal()
    res = dict(label=SYN, R=R, B=B, sigma_zeta=SIG_Z, sectors={})
    for si, s in enumerate(SECT):
        sec = seal["sectors"][s]
        sealed_c = [sec["commitments"][str(v)] for v in VINT]
        vint, comm = funds_for(s, sealed_c)
        tv = sec["truth_variants"]
        plans = {
            "sealed": (vint, comm, {}, {}),
            "mature_flat": (*funds_for(s, tv["mature_flat"]["commitments"]), {}, {}),
            "growth_10pct": (*funds_for(s, tv["growth_10pct"]["commitments"]), {}, {}),
            "growth_20pct_stress": (*funds_for(s, tv["growth_20pct_stress"]["commitments"]), {}, {}),
            "lapse_plus2y": (vint, comm, dict(lapse_shift=2), {}),
            "recallable_10pct": (vint, comm, dict(recallable=0.10), {}),
            "T4prime_x1.38_scenario_conditional": (vint, comm, dict(future_mult=1.38), dict(future_mult=1.38)),
            "T4prime_x1.38_unannounced": (vint, comm, dict(future_mult=1.38), {}),
        }
        res["sectors"][s] = {"n_funds": int(len(vint))}
        rn = run_variant(s, vint, comm, {}, {}, seed=6900 + si, lapse_model=False)
        res["sectors"][s]["sealed|naive_no_lapse_model"] = rn
        print(f"{s:3s} {'sealed|naive_no_lapse_model':36s} cov90 pace4/pace8/unf {rn['pace4']['coverage90']:.3f}/"
              f"{rn['pace8']['coverage90']:.3f}/{rn['unf']['coverage90']:.3f} bias unf {rn['unf']['bias_mean']:+.3f}", flush=True)
        for j, (name, (vv, cc, var, ve)) in enumerate(plans.items()):
            r = run_variant(s, vv, cc, var, ve, seed=7000 + 100 * si + j)
            res["sectors"][s][name] = r
            print(f"{s:3s} {name:36s} cov90 pace4/pace8/unf {r['pace4']['coverage90']:.3f}/{r['pace8']['coverage90']:.3f}/"
                  f"{r['unf']['coverage90']:.3f} bias {r['pace4']['bias_mean']:+.3f}/{r['pace8']['bias_mean']:+.3f}/"
                  f"{r['unf']['bias_mean']:+.3f} V17 {'PASS' if r['gate_V17'] else 'FAIL'}", flush=True)
            OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("wrote", OUT, SYN)


if __name__ == "__main__":
    main()
