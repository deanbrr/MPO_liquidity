"""
gap_02 (groups) - misspecification ensemble prototype for the Forward Belief Engine (FBE).  SYNTHETIC.

Purpose: measure how far a production-style FBE degrades when the generator departs from the estimator's
assumptions, and check that pre-registered gates are attainable by a robustified FBE.  One group with PE-like
defaults (sec. 5 / G9 sec. 6.4), many worlds; numpy only.

Generator (truth and observation), annualized decimals:
  mu_i = 0.10 + a_v + e_i,  a_v ~ N(0, 0.01^2) (10 vintages), e_i ~ N(0, 0.04^2)
  u_i  = mu_i + b_u + eta_u,          b_u = 0.05, sd(eta_u) = 0.03
  a_i  = mu_i + eta_a,                sd(eta_a) = 0.05          (actual-to-date signal)
  f_i  = mu_i + b_f + eta_f,          b_f = 0.03, sd(eta_f) = 0.03; stated sd = 0.03 / kappa, kappa = 2.0
  resolved outcomes (training only): y_j = mu_j + eps_j, sd(eps) = 0.06; group training n = 40,
  pooled cross-group training n = 320 (8 groups sharing the misspecification coefficients)
Variants (generator only; estimators unchanged):
  M0  well specified (the SBC case: generator draws what the estimator assumes)
  M1  regime-dependent optimism: b_f x (1 + 1{D}); training 30% D, test 100% D (today is LATE x D)
  M2  nonlinear anchoring: f = (1-w) f0 + w u, w = 0.15 + 0.45 tanh((u - a - 0.05)^+ / 0.04)
  M3  t3 tails: eta_u, eta_f, eps ~ t3 rescaled to the Gaussian 80% width
  M4  correlated u-f errors: corr(eta_u, eta_f) = 0.6
  M5  strategic (designed pay): f += delta* + u_def 1{SELL flag}; delta* = bZB'/(2s) = 0.008, u_def = 0.02
  M5s strategic (status-quo pay): delta* = 0.032, u_def = 0.02
  M6  prior shift: true b_f = estimator prior mean + 2 prior sd = 0.05
  MALL M1 + M2 + M3 + M4 + M5 + M6
Estimators:
  FBE-B (production baseline): b_u = mean(u - y); b_f = mean(f - y) shrunk to the sec. 5 prior N(0.03, 0.01^2);
        known error scales (kappa = 2); independent errors; GLS with prior N(0.10, 0.04^2 + 0.01^2);
        bias-estimation uncertainty propagated into the predictive sd.
  FBE-R (robust): Huber bias regression for f - y on [1, D, gap, flag] with the slope coefficients pooled
        across groups (n = 320) and a local intercept (n = 40, same prior); u-f error covariance estimated from
        the test cross-section, cov(u - a, f - a) - sd_a^2; GLS with the full covariance; uncertainty propagated.
Metrics on test assets vs true mu: CRPS (Gaussian), 80% coverage, mean error on true SELL candidates (mu < h),
decision regret of SELL (posterior mean < h) vs the oracle (mu < h), h = 0.08, in pp of NAV a year per asset.
Run:  .venv\\Scripts\\python.exe -I -B misspec_ensemble_proto.py   -> misspec_ensemble_proto_results.json
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "misspec_ensemble_proto_results.json")
W, NTR, NPOOL, NTE = 2000, 40, 320, 120
MU0, SD_V, SD_E = 0.10, 0.01, 0.04
BU, SDU, SDA = 0.05, 0.03, 0.05
BF, SDF, KAPPA = 0.03, 0.03, 2.0
SDY, H = 0.06, 0.08
PRIOR_BF = (0.03, 0.01)
Z80 = 1.2815516
T3_Q90 = 1.6377444
_erf = np.frompyfunc(math.erf, 1, 1)


def crps_gauss(y, m, s):
    z = (y - m) / s
    Phi = 0.5 * (1 + _erf(z / math.sqrt(2)).astype(float))
    return s * (z * (2 * Phi - 1) + 2 * np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi) - 1 / math.sqrt(math.pi))


def errs(rng, shape, sd, t3):
    if t3:
        return rng.standard_t(3, size=shape) * sd * Z80 / T3_Q90
    return rng.standard_normal(shape) * sd


def generate(variant: str, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    allv = variant == "MALL"
    m1, m2, m3, m4 = (allv or variant == k for k in ("M1", "M2", "M3", "M4"))
    m5 = allv or variant in ("M5", "M5s")
    m6 = allv or variant == "M6"
    delta = 0.032 if variant == "M5s" else 0.008
    bf = PRIOR_BF[0] + 2 * PRIOR_BF[1] if m6 else BF
    out = {}
    for part, n in (("tr", NTR), ("pool", NPOOL), ("te", NTE)):
        vint = rng.integers(0, 10, size=(W, n))
        av = rng.standard_normal((W, 10)) * SD_V
        mu = MU0 + np.take_along_axis(av, vint, axis=1) + rng.standard_normal((W, n)) * SD_E
        D = (rng.random((W, n)) < 0.30).astype(float) if part != "te" else np.ones((W, n))
        eu = errs(rng, (W, n), SDU, m3)
        ef = errs(rng, (W, n), SDF, m3)
        if m4:
            ef = 0.6 * eu / SDU * SDF + 0.8 * ef
        u = mu + BU + eu
        a = mu + rng.standard_normal((W, n)) * SDA
        f = mu + bf * ((1 + D) if m1 else 1.0) + ef
        if m2:
            w = 0.15 + 0.45 * np.tanh(np.maximum(u - a - 0.05, 0) / 0.04)
            f = (1 - w) * f + w * u
        flag = np.zeros((W, n))
        if m5:
            flag = ((mu + rng.standard_normal((W, n)) * 0.03) < H).astype(float)   # previous-period screen
            f = f + delta + 0.02 * flag
        y = mu + errs(rng, (W, n), SDY, m3) if part != "te" else None
        out[part] = dict(mu=mu, u=u, a=a, f=f, D=D, flag=flag, y=y)
    return out


def gls(zs: list, cov: np.ndarray, prior_m: float, prior_v: float):
    """zs: list of (W, n) signals of mu; cov: (W, k, k) error covariance. Returns weights and posterior."""
    k = len(zs)
    Si = np.linalg.inv(cov)
    one = np.ones(k)
    p_obs = np.einsum("i,wij,j->w", one, Si, one)
    wts = np.einsum("wij,j->wi", Si, one)                       # unnormalized weights per signal
    p = p_obs + 1 / prior_v
    m = (np.einsum("wi,iwn->wn", wts, np.stack(zs)) + prior_m / prior_v) / p[:, None]
    return m, 1 / p, wts / p[:, None]


def fbe_baseline(d):
    tr, te = d["tr"], d["te"]
    n = NTR
    eu, ef = tr["u"] - tr["y"], tr["f"] - tr["y"]
    bu = eu.mean(1)
    vbu = eu.var(1, ddof=1) / n
    se2 = ef.var(1, ddof=1) / n
    pm, ps = PRIOR_BF
    bf = (ef.mean(1) / se2 + pm / ps ** 2) / (1 / se2 + 1 / ps ** 2)
    vbf = 1 / (1 / se2 + 1 / ps ** 2)
    cov = np.zeros((W, 3, 3))
    cov[:, 0, 0], cov[:, 1, 1], cov[:, 2, 2] = SDU ** 2, SDA ** 2, SDF ** 2
    m, v, wn = gls([te["u"] - bu[:, None], te["a"], te["f"] - bf[:, None]], cov, MU0, SD_E ** 2 + SD_V ** 2)
    s = np.sqrt(v + wn[:, 0] ** 2 * vbu + wn[:, 2] ** 2 * vbf)[:, None] * np.ones_like(m)
    return m, s


def huber(X, y, iters=10, c=1.345):
    Wn, n, k = X.shape
    w = np.ones((Wn, n))
    for _ in range(iters):
        Xw = X * w[..., None]
        A = np.einsum("wnk,wnj->wkj", Xw, X) + 1e-10 * np.eye(k)
        beta = np.linalg.solve(A, np.einsum("wnk,wn->wk", Xw, y)[..., None])[..., 0]
        r = y - np.einsum("wnk,wk->wn", X, beta)
        sc = 1.4826 * np.median(np.abs(r - np.median(r, 1, keepdims=True)), 1, keepdims=True) + 1e-12
        z = np.abs(r) / sc
        w = np.where(z <= c, 1.0, c / z)
    Xw = X * w[..., None]
    A = np.einsum("wnk,wnj->wkj", Xw, X) + 1e-10 * np.eye(k)
    s2 = (w * r ** 2).sum(1) / np.maximum(w.sum(1) - k, 1)
    covb = np.linalg.inv(A) * s2[:, None, None]
    return beta, covb


def gapc(part):
    return np.maximum(part["u"] - part["a"] - 0.05, 0)


def fbe_robust(d):
    tr, pool, te = d["tr"], d["pool"], d["te"]
    # pooled slopes on [1, D, gap, flag] (intercept absorbed per pool; slopes shared)
    Xp = np.stack([np.ones_like(pool["y"]), pool["D"], gapc(pool), pool["flag"]], -1)
    bp, covp = huber(Xp, pool["f"] - pool["y"])
    slopes, cov_s = bp[:, 1:], covp[:, 1:, 1:]
    # local intercept after removing pooled slope effects, shrunk to the sec. 5 prior
    xs_tr = np.stack([tr["D"], gapc(tr), tr["flag"]], -1)
    resid = (tr["f"] - tr["y"]) - np.einsum("wnk,wk->wn", xs_tr, slopes)
    b0r, cov0 = huber(np.ones((W, NTR, 1)), resid)
    se2 = cov0[:, 0, 0]
    pm, ps = PRIOR_BF
    b0 = (b0r[:, 0] / se2 + pm / ps ** 2) / (1 / se2 + 1 / ps ** 2)
    vb0 = 1 / (1 / se2 + 1 / ps ** 2)
    bur, covu = huber(np.stack([np.ones_like(tr["y"]), tr["D"]], -1), tr["u"] - tr["y"])
    xs_te = np.stack([te["D"], gapc(te), te["flag"]], -1)
    bf_te = b0[:, None] + np.einsum("wnk,wk->wn", xs_te, slopes)
    bu_te = bur[:, 0:1] + bur[:, 1:2] * te["D"]
    vbf_te = vb0[:, None] + np.einsum("wnk,wkj,wnj->wn", xs_te, cov_s, xs_te)
    vbu_te = covu[:, 0, 0][:, None] + covu[:, 1, 1][:, None] * te["D"] + 2 * covu[:, 0, 1][:, None] * te["D"]
    # u-f error covariance from the test cross-section (no outcomes needed)
    du, df = te["u"] - te["a"], te["f"] - te["a"]
    cuf = ((du - du.mean(1, keepdims=True)) * (df - df.mean(1, keepdims=True))).mean(1) - SDA ** 2
    cuf = np.clip(cuf, 0.0, 0.95 * SDU * SDF)
    cov = np.zeros((W, 3, 3))
    cov[:, 0, 0], cov[:, 1, 1], cov[:, 2, 2] = SDU ** 2, SDA ** 2, SDF ** 2
    cov[:, 0, 2] = cov[:, 2, 0] = cuf
    m, v, wn = gls([te["u"] - bu_te, te["a"], te["f"] - bf_te], cov, MU0, SD_E ** 2 + SD_V ** 2)
    s = np.sqrt(v[:, None] + wn[:, 0:1] ** 2 * vbu_te + wn[:, 2:3] ** 2 * vbf_te)
    return m, s


def flags_of(variant):
    allv = variant == "MALL"
    return dict(m1=allv or variant == "M1", m2=allv or variant == "M2", m3=allv or variant == "M3",
                m4=allv or variant == "M4", m5=allv or variant in ("M5", "M5s"), m6=allv or variant == "M6",
                delta=0.032 if variant == "M5s" else 0.008)


def fbe_oracle(d, variant):
    """Variant-aware benchmark: knows the generator's bias function, anchoring rule and error covariance
    (linear-Gaussian GLS with the true second moments; exact for M0, M1, M4, M5, M6; the best linear rule for M3)."""
    fl = flags_of(variant)
    te = d["te"]
    bf = PRIOR_BF[0] + 2 * PRIOR_BF[1] if fl["m6"] else BF
    f = te["f"].copy()
    if fl["m5"]:
        f = f - fl["delta"] - 0.02 * te["flag"]
    if fl["m2"]:
        w = 0.15 + 0.45 * np.tanh(np.maximum(te["u"] - te["a"] - 0.05, 0) / 0.04)
        f = (f - w * te["u"]) / (1 - w)
    zf = f - bf * ((1 + te["D"]) if fl["m1"] else 1.0)
    t3v = (Z80 / T3_Q90) ** 2 * 3.0 if fl["m3"] else 1.0      # variance of the rescaled t3 relative to sd^2
    cov = np.zeros((W, 3, 3))
    cov[:, 0, 0], cov[:, 1, 1], cov[:, 2, 2] = SDU ** 2 * t3v, SDA ** 2, SDF ** 2 * t3v
    if fl["m4"]:
        cov[:, 0, 2] = cov[:, 2, 0] = 0.6 * SDU * SDF * t3v
    m, v, _ = gls([te["u"] - BU, te["a"], zf], cov, MU0, SD_E ** 2 + SD_V ** 2)
    return m, np.sqrt(v)[:, None] * np.ones_like(m)


def detection(d):
    """Pooled Huber regression t-stats for the regime and SELL-flag coefficients."""
    pool = d["pool"]
    Xp = np.stack([np.ones_like(pool["y"]), pool["D"], gapc(pool), pool["flag"]], -1)
    bp, covp = huber(Xp, pool["f"] - pool["y"])
    tD = bp[:, 1] / np.sqrt(covp[:, 1, 1])
    has_flag = pool["flag"].sum(1) > 0
    tF = np.where(has_flag, bp[:, 3] / np.sqrt(np.maximum(covp[:, 3, 3], 1e-12)), 0.0)
    tG = bp[:, 2] / np.sqrt(covp[:, 2, 2])
    return dict(power_regime=float((tD > 1.96).mean()), power_flag=float((tF > 1.96).mean()),
                power_gap=float((tG > 1.96).mean()))


def metrics(d, m, s):
    mu = d["te"]["mu"]
    sell = mu < H
    return dict(crps_pp=float(crps_gauss(mu, m, s).mean() * 100),
                cov80=float((np.abs(mu - m) <= Z80 * s).mean()),
                bias_sell_pp=float(((m - mu)[sell]).mean() * 100),
                regret_pp=float((np.abs(mu - H) * ((m < H) != sell)).mean() * 100),
                rmse_pp=float(np.sqrt(((m - mu) ** 2).mean()) * 100))


def main():
    variants = ["M0", "M1", "M2", "M3", "M4", "M5", "M5s", "M6", "MALL"]
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "worlds": W, "n_train": NTR, "n_pool": NPOOL, "n_test": NTE}
    tab = {}
    for i, vname in enumerate(variants):
        d = generate(vname, 1000 + i)
        tab[vname] = dict(baseline=metrics(d, *fbe_baseline(d)), robust=metrics(d, *fbe_robust(d)),
                          oracle=metrics(d, *fbe_oracle(d, vname)), detection=detection(d))
    ref = tab["M0"]["baseline"]
    for r in tab.values():
        for est in ("baseline", "robust", "oracle"):
            r[est]["crps_vs_B0"] = r[est]["crps_pp"] / ref["crps_pp"] - 1
            r[est]["regret_vs_B0"] = r[est]["regret_pp"] / ref["regret_pp"] - 1
            r[est]["crps_excess_vs_oracle"] = r[est]["crps_pp"] / r["oracle"]["crps_pp"] - 1
            r[est]["regret_excess_vs_oracle"] = r[est]["regret_pp"] / r["oracle"]["regret_pp"] - 1
    res["table"] = tab
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(f"{'var':5s} | oracle dCRPS(vsB0) | B: xsCRPS  cov80  biasSELL xsRegret | R: xsCRPS  cov80  biasSELL xsRegret | power D/flag/gap")
    for k, r in tab.items():
        b, q, o, dt = r["baseline"], r["robust"], r["oracle"], r["detection"]
        print(f"{k:5s} | {o['crps_vs_B0']:+7.1%} | {b['crps_excess_vs_oracle']:+7.1%} {b['cov80']:6.3f} {b['bias_sell_pp']:+7.2f} "
              f"{b['regret_excess_vs_oracle']:+7.1%} | {q['crps_excess_vs_oracle']:+7.1%} {q['cov80']:6.3f} "
              f"{q['bias_sell_pp']:+7.2f} {q['regret_excess_vs_oracle']:+7.1%} | {dt['power_regime']:.2f}/{dt['power_flag']:.2f}/{dt['power_gap']:.2f}")
    print("reference B0: CRPS %.3fpp, regret %.3fpp, RMSE %.2fpp" % (ref["crps_pp"], ref["regret_pp"], ref["rmse_pp"]))


if __name__ == "__main__":
    main()
