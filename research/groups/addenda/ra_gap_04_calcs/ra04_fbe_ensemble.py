"""
ra_gap_04 - Real Assets forecast-engine (FBE) misspecification ensemble.   ALL OUTPUTS SYNTHETIC - NOT ADIC DATA.

Canonical ensemble (groups gap_02 sec. 3; misspec_ensemble_proto.py) applied to the RA forecast engine. Only the
generator changes; estimators stay fixed. Gate thresholds are the canonical ones (G-A..G-E).

RA world (annual units, decimals), per Monte Carlo world:
  * 115 test positions on the census of record mapped to 8 bias segments (CORE_RE 9, VA_RE 17, RE_DEV 2, GCC_RE 3,
    CORE_INF 16, VA_INF 38, GF_INF 6, ENR 24) [I mapping of synthesis sec. 11 sleeves];
  * expected return on V*: mu = m_s + c_{s,d} + e_i ; c ~ N(0, 1.5%), e ~ N(0, 2.5-3.5%) [I];
  * underwritten u = mu + b^u_s + gamma_s 1{late} + eta_u ; valuation view a = mu + eta_a ;
    forecast f = mu + b^f_s + w_a x_{s,d} + eta_f, with w_a = 0.30 anchoring on the appraisal lag x (sec. 8.4);
    b^u, b^f, late uplifts and component shares from synthesis sec. 8.4 [I];
  * resolved outcomes (training archive, D_TR annual dates x 115 positions): y = mu + eta_{s,d} + eps, with a COMMON
    segment-date shock eta (the RA-specific feature) and the desmoothed common-shock control
    C_hat = s_c eta + b_c + nu (quality from the RAME ensemble);
  * stated case width: sd_stated = 0.03 / kappa_s with segment kappa_s unknown to the estimators
    (truth K-RND: kappa_s ~ LN(ln 1.75, 0.25^2), the prior of record; sensitivity K-TAB: the sec. 8.4 table x LN(0, 0.15^2));
  * plan components (when archived): NOI-growth and exit-cap components of b^f are observed against fast-resolving
    outcomes (NOI, market-implied forward cap); the residual (capex/schedule/strategic) only through total returns.
Canonical variants M0..M6, MALL exactly as gap_02 (M1 regime x(1+1{D}) with training 30% D and test 100% D; M2
nonlinear anchoring on underwriting; M3 t3 tails; M4 corr(eta_u, eta_f) = 0.6; M5 / M5s strategic delta* 80 / 320bp +
u_def 2pp on SELL-flagged holdings; M6 true b^f = prior mean + 2 prior sd). RA variants: RAME quality (ideal tau,
listed-only AL, worst-case tau TW), starting gap G0 2 / 5 / 8% (V* level error), components absent (IRR/MOIC + cases
only, brief sec. 9), archive depth 8 years, kappa truth K-TAB.

Estimators:
  FBE-B-RA (production-style, synthesis sec. 8.4-8.5 as written): segment biases from the control-adjusted errors
    (control coefficient fixed at -1, w_a fixed at 0.30), shrunk to segment priors with date-clustered variance;
    segment kappa table; independent errors; precision weights shrunk 50% toward equal weights; uncertainty propagated.
  FBE-R-RA (robust; canonical FBE-R + RA terms): canonical regime / gap / flag terms pooled across the other seven
    groups (Huber; the regime term relative, since M1 multiplies b^f); RA Huber regression on [segment intercepts x
    pooled regime multiplier, x_hat, C_hat] with segment-date cluster-robust covariance; plan components (when archived)
    by pooled relative regressions with their own regime term (prior: the pooled relative regime effect); segment
    effects as random effects on the relative deviation from the sec. 8.4 priors (segment sd 1/3, group shift pooled
    across the eight segments ~ N(0, (1/3)^2)); one kappa_g = 1.75; u-f covariance estimated WITHIN segments from the
    test cross-section and used only in the predictive variance; fusion by the sec. 8.5 rule (precision weights shrunk
    50% toward equal) - chosen by the design ablation (ra04_fbe_ablation.py) because GLS with an estimated covariance
    amplifies the kappa misspecification; bias uncertainty propagated.
  FBE-R-RA-GLS: the same with canonical GLS fusion (comparator).
  FBE-R-RA-cap: FBE-R-RA with the forecast signal's precision set to zero (the G-E remedy path).
  ORACLE: knows the generator (biases incl. M1/M6, anchoring with true x, M2 inversion, M5 terms, true kappa_s,
    error covariance incl. M3/M4, V* level error); linear-Gaussian GLS with the true second moments.
Run:  .venv\\Scripts\\python.exe -I -B ra04_fbe_ensemble.py   -> ra04_fbe_ensemble_results.json
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "ra04_fbe_ensemble_results.json"
SYN = "SYNTHETIC - NOT ADIC DATA"
W = int(os.environ.get("RA04_W", "2000"))
Z80 = 1.2815516
T3_Q90 = 1.6377444
T3S = Z80 / T3_Q90
T3V = T3S ** 2 * 3.0
_erf = np.frompyfunc(math.erf, 1, 1)

# canonical constants (gap_02 prototype) for the pooled seven other groups
SDU, SDA, SDF = 0.03, 0.05, 0.03
NPOOL = 7 * 40
MU0, SD_V, SD_E = 0.10, 0.01, 0.04
BU_C, BF_C, SDY_C, H_C = 0.05, 0.03, 0.06, 0.08

# Real Assets segments [I]: sec. 8.4 priors (pp/yr), census mapping of the 115 positions
SEGS = ["CORE_RE", "VA_RE", "RE_DEV", "GCC_RE", "CORE_INF", "VA_INF", "GF_INF", "ENR"]
NTE = np.array([9, 17, 2, 3, 16, 38, 6, 24])
SEG_OF = np.repeat(np.arange(8), NTE)
NP = int(NTE.sum())
M_S = np.array([0.070, 0.090, 0.100, 0.080, 0.080, 0.095, 0.100, 0.100])
SD_C = 0.015
SD_I = np.array([0.025, 0.035, 0.035, 0.035, 0.025, 0.035, 0.035, 0.035])
BU = np.array([0.015, 0.040, 0.060, 0.020, 0.010, 0.030, 0.040, 0.030])
GU = np.array([0.015, 0.015, 0.000, 0.015, 0.010, 0.010, 0.000, 0.000])
BF = np.array([0.010, 0.025, 0.035, 0.015, 0.0075, 0.020, 0.030, 0.020])
KTAB = np.array([1.67, 2.00, 2.22, 2.00, 1.67, 2.00, 2.22, 2.22])
PHI_N = np.array([0.5, 0.4, 0.2, 0.4, 0.4, 0.3, 0.2, 0.3])
PHI_X = np.array([0.4, 0.3, 0.3, 0.4, 0.5, 0.3, 0.2, 0.2])
PHI_K = 1.0 - PHI_N - PHI_X
SIG_ETA = np.array([0.07, 0.09, 0.11, 0.09, 0.05, 0.07, 0.08, 0.14])
SIG_EPS = np.array([0.06, 0.09, 0.12, 0.09, 0.04, 0.08, 0.10, 0.14])
H_S = M_S - 0.015                      # SELL hurdle by segment
WA = 0.30
X_TEST = np.array([[0.01, 0.02], [0.01, 0.02], [0.01, 0.02], [0.03, 0.02], [0.0, 0.015], [0.0, 0.015],
                   [0.0, 0.015], [-0.01, 0.03]])          # (mean, sd) of today's appraisal-lag covariate [I]
OMEGA = 0.5                            # V* level error -> annual return error over a 2-year horizon

# RAME linkage (control C_hat and anchoring covariate x_hat): slope, bias, noise sd. Provisional values are
# replaced by the RAME ensemble's annual-return error statistics when rame_ens_g13_*.json exist.
RAME_Q = {"ideal": dict(s=0.95, b=0.0, sd=0.025), "AL": dict(s=0.85, b=0.0, sd=0.040),
          "TW": dict(s=0.55, b=0.0, sd=0.045)}
G0_ERR = {"ideal": 0.20, "AL": 0.40}  # share of an imposed starting gap left in V* (from the RAME G0 experiment)


def load_rame_linkage():
    import glob
    fs = sorted(glob.glob(str(HERE / "rame_ens_g13_*.json")))
    if not fs:
        return "provisional"
    acc = {"ideal": [], "AL": [], "TW": []}
    g0 = {"ideal": [], "AL": []}
    for f in fs:
        r = json.load(open(f, encoding="utf-8"))
        v = r.get("variants", {})
        if "M0" in v:
            acc["ideal"].append(v["M0"]["ALT"])
            acc["AL"].append(v["M0"]["AL"])
            if "G0" in v["M0"]:
                for k_src, k_dst in (("ALT", "ideal"), ("AL", "AL")):
                    for gv in ("0.05", "0.08"):
                        e = v["M0"]["G0"][gv][k_src]
                        base = v["M0"]["G0"]["0.0"][k_src]
                        imposed = e["G_true_mean_pp"] - base["G_true_mean_pp"]
                        if imposed > 0:
                            g0[k_dst].append(max(0.0, -(e["err_mean_pp"] - base["err_mean_pp"])) / imposed)
        if "TW" in v:
            acc["TW"].append(v["TW"]["ALT"])
    for k, lst in acc.items():
        if lst:
            # annual-return error: slope of nowcast on true 4q change, bias, residual noise around the slope
            s = float(np.mean([x["e4_slope"] for x in lst]))
            b = float(np.mean([x["e4_bias_pp"] for x in lst])) / 100
            rm = float(np.mean([x["e4_rmse_pp"] for x in lst])) / 100
            sdt = float(np.mean([x["e4_true_sd_pp"] for x in lst])) / 100
            resid = math.sqrt(max(rm ** 2 - ((s - 1) * sdt) ** 2 - b ** 2, 1e-6))
            RAME_Q[k] = dict(s=s, b=b, sd=resid)
    for k, lst in g0.items():
        if lst:
            G0_ERR[k] = float(np.clip(np.mean(lst), 0.0, 1.0))
    return f"from {len(fs)} RAME g13 files"


def tdraw(rng, shape, t3):
    if t3:
        return rng.standard_t(3, size=shape) * T3S
    return rng.standard_normal(shape)


def flags_of(variant):
    allv = variant == "MALL"
    return dict(m1=allv or variant == "M1", m2=allv or variant == "M2", m3=allv or variant == "M3",
                m4=allv or variant == "M4", m5=allv or variant in ("M5", "M5s"), m6=allv or variant == "M6",
                delta=0.032 if variant == "M5s" else 0.008)


def m2_w(u, a):
    return 0.15 + 0.45 * np.tanh(np.maximum(u - a - 0.05, 0) / 0.04)


# ------------------------------------------------------------------------------------------------------------
# Generator
# ------------------------------------------------------------------------------------------------------------
def generate(variant: str, seed: int, opt: dict) -> dict:
    rng = np.random.default_rng(seed)
    fl = flags_of(variant)
    DTR = opt.get("dtr", 4)
    rq = RAME_Q[opt.get("rame", "ideal")]
    t3 = fl["m3"]
    # --- pooled seven canonical groups (iid, PE-like; canonical generator) ---
    vint = rng.integers(0, 10, size=(W, NPOOL))
    av = rng.standard_normal((W, 10)) * SD_V
    mu_p = MU0 + np.take_along_axis(av, vint, axis=1) + rng.standard_normal((W, NPOOL)) * SD_E
    Dp = (rng.random((W, NPOOL)) < 0.30).astype(float)
    eu = tdraw(rng, (W, NPOOL), t3) * SDU
    ef = tdraw(rng, (W, NPOOL), t3) * SDF
    if fl["m4"]:
        ef = 0.6 * eu / SDU * SDF + 0.8 * ef
    bfc = 0.03 + 2 * 0.01 if fl["m6"] else BF_C
    up = mu_p + BU_C + eu
    ap = mu_p + rng.standard_normal((W, NPOOL)) * SDA
    fp = mu_p + bfc * ((1 + Dp) if fl["m1"] else 1.0) + ef
    if fl["m2"]:
        w = m2_w(up, ap)
        fp = (1 - w) * fp + w * up
    flp = np.zeros((W, NPOOL))
    if fl["m5"]:
        flp = ((mu_p + rng.standard_normal((W, NPOOL)) * 0.03) < H_C).astype(float)
        fp = fp + fl["delta"] + 0.02 * flp
    yp = mu_p + tdraw(rng, (W, NPOOL), t3) * SDY_C
    pool = dict(u=up, a=ap, f=fp, y=yp, D=Dp, flag=flp)
    # --- Real Assets world ---
    e_i = rng.standard_normal((W, NP)) * SD_I[SEG_OF]
    c = rng.standard_normal((W, 8, DTR + 1)) * SD_C
    if opt.get("ktruth", "RND") == "RND":
        kap = np.exp(np.log(1.75) + 0.25 * rng.standard_normal((W, 8)))
    else:
        kap = KTAB[None, :] * np.exp(0.15 * rng.standard_normal((W, 8)))
    sd_stated = SDF / kap[:, SEG_OF]                                     # (W, NP)
    bf_true = BF * ((1 + 2 / 3) if fl["m6"] else 1.0)
    Dd = (rng.random((W, DTR)) < 0.30).astype(float)
    late = (rng.random((W, DTR)) < 0.50).astype(float)
    xs = rng.standard_normal((W, 8, DTR)) * 0.03
    xs_te = X_TEST[:, 0][None, :] + X_TEST[:, 1][None, :] * rng.standard_normal((W, 8))
    eta = tdraw(rng, (W, 8, DTR), t3) * SIG_ETA[None, :, None]
    rows = []
    for dd in range(DTR + 1):
        test = dd == DTR
        mu = M_S[SEG_OF][None, :] + c[:, SEG_OF, dd] + e_i
        D = np.ones((W, 1)) if test else Dd[:, dd:dd + 1]
        lt = np.ones((W, 1)) if test else late[:, dd:dd + 1]
        eu = tdraw(rng, (W, NP), t3) * SDU
        ef = tdraw(rng, (W, NP), t3) * SDF
        if fl["m4"]:
            ef = 0.6 * eu / SDU * SDF + 0.8 * ef
        x_true = xs_te[:, SEG_OF] if test else xs[:, SEG_OF, dd]
        u = mu + BU[SEG_OF] + GU[SEG_OF] * lt + eu
        a = mu + rng.standard_normal((W, NP)) * SDA
        bft = np.broadcast_to(bf_true[SEG_OF][None, :] * ((1 + D) if fl["m1"] else 1.0), (W, NP)).copy()
        f = mu + bft + WA * x_true + ef
        if fl["m2"]:
            w = m2_w(u, a)
            f = (1 - w) * f + w * u
        flag = np.zeros((W, NP))
        if fl["m5"]:
            flag = ((mu + rng.standard_normal((W, NP)) * 0.03) < H_S[SEG_OF]).astype(float)
            f = f + fl["delta"] + 0.02 * flag
        x_hat_s = rq["s"] * (xs_te if test else xs[:, :, dd]) + rq["b"] + rq["sd"] * rng.standard_normal((W, 8))
        x_hat = x_hat_s[:, SEG_OF]
        r = dict(mu=mu, u=u, a=a, f=f, D=np.broadcast_to(D, (W, NP)).copy(), late=np.broadcast_to(lt, (W, NP)).copy(),
                 flag=flag, x_true=x_true, x_hat=x_hat, sd_stated=sd_stated, bft=bft)
        if test:
            g0 = opt.get("g0", 0.0)
            if g0:
                delta_s = G0_ERR[opt.get("rame", "ideal")] * g0 * np.where(np.isin(np.arange(8), [0, 1, 2, 3]), 1.0, 0.5)
                shift = -OMEGA * delta_s[SEG_OF]
                for k in ("u", "a", "f"):
                    r[k] = r[k] + shift[None, :]
                r["shift"] = np.broadcast_to(shift[None, :], (W, NP)).copy()
            else:
                r["shift"] = np.zeros((W, NP))
        else:
            r["y"] = mu + eta[:, SEG_OF, dd] + tdraw(rng, (W, NP), t3) * SIG_EPS[SEG_OF]
            chat_s = rq["s"] * eta[:, :, dd] + rq["b"] + rq["sd"] * rng.standard_normal((W, 8))
            r["C_hat"] = chat_s[:, SEG_OF]
            # components (fast-resolving): NOI-growth and exit-cap parts of b^f, return units
            cN = rng.standard_normal((W, 8)) * 0.010
            cX = rng.standard_normal((W, 8)) * 0.005
            r["eN"] = PHI_N[SEG_OF] * bft + cN[:, SEG_OF] + rng.standard_normal((W, NP)) * 0.020
            r["eX"] = PHI_X[SEG_OF] * bft + cX[:, SEG_OF] + rng.standard_normal((W, NP)) * 0.0075
            r["date"] = dd
        rows.append(r)
    tr = {k: np.concatenate([rr[k] for rr in rows[:-1]], axis=1) for k in rows[0] if k not in ("date",)}
    tr["seg"] = np.tile(SEG_OF, DTR)
    tr["cluster"] = np.concatenate([SEG_OF + 8 * dd for dd in range(DTR)])
    tr["ncl"] = 8 * DTR
    return dict(pool=pool, tr=tr, te=rows[-1], kap=kap, bf_true=bf_true, fl=fl, opt=opt)


# ------------------------------------------------------------------------------------------------------------
# Regression utilities (vectorized over worlds)
# ------------------------------------------------------------------------------------------------------------
def huber(X, y, cl=None, ncl=None, iters=10, c=1.345, prior=None):
    """Huber M-estimation, vectorized over worlds. prior: list of (col, mean (W,), sd (W,), sigma) normal priors
    on single coefficients, implemented as pseudo-observations (own cluster, weight fixed at 1)."""
    n_data = X.shape[1]
    if prior:
        Wn, _, k = X.shape
        rows_x, rows_y = [], []
        for col, pm, ps, sig in prior:
            sc_ = sig / np.maximum(np.broadcast_to(ps, (Wn,)), 1e-9)
            xr = np.zeros((Wn, 1, k))
            xr[:, 0, col] = sc_
            rows_x.append(xr)
            rows_y.append((sc_ * np.broadcast_to(pm, (Wn,)))[:, None])
        X = np.concatenate([X] + rows_x, axis=1)
        y = np.concatenate([y] + rows_y, axis=1)
        if cl is not None:
            cl = np.concatenate([cl, ncl + np.arange(len(prior))])
            ncl = ncl + len(prior)
    Wn, n, k = X.shape
    w = np.ones((Wn, n))
    for _ in range(iters):
        Xw = X * w[..., None]
        A = np.einsum("wnk,wnj->wkj", Xw, X) + 1e-10 * np.eye(k)
        beta = np.linalg.solve(A, np.einsum("wnk,wn->wk", Xw, y)[..., None])[..., 0]
        r = y - np.einsum("wnk,wk->wn", X, beta)
        rd = r[:, :n_data]
        sc = 1.4826 * np.median(np.abs(rd - np.median(rd, 1, keepdims=True)), 1, keepdims=True) + 1e-12
        z = np.abs(r) / sc
        w = np.where(z <= c, 1.0, c / z)
        w[:, n_data:] = 1.0
    Xw = X * w[..., None]
    A = np.einsum("wnk,wnj->wkj", Xw, X) + 1e-10 * np.eye(k)
    Ai = np.linalg.inv(A)
    if cl is None:
        s2 = (w * r ** 2).sum(1) / np.maximum(w.sum(1) - k, 1)
        cov = Ai * s2[:, None, None]
    else:
        G = np.zeros((n, ncl))
        G[np.arange(n), cl] = 1.0
        sc_ = np.einsum("nc,wnk->wck", G, X * (w * r)[..., None])
        meat = np.einsum("wck,wcj->wkj", sc_, sc_)
        if prior:                                         # prior pseudo-rows: add their information, not their score
            for j in range(len(prior)):
                xr = X[:, n_data + j, :]
                meat = meat - np.einsum("wk,wj->wkj", sc_[:, ncl - len(prior) + j, :], sc_[:, ncl - len(prior) + j, :])
                s2p = (w[:, :n_data] * r[:, :n_data] ** 2).sum(1) / np.maximum(w[:, :n_data].sum(1) - k, 1)
                meat = meat + np.einsum("wk,wj->wkj", xr, xr) * s2p[:, None, None]
        cov = np.einsum("wij,wjk,wkl->wil", Ai, meat, Ai) * ncl / max(ncl - 1, 1)
        # iid floor
        s2 = (w[:, :n_data] * r[:, :n_data] ** 2).sum(1) / np.maximum(w[:, :n_data].sum(1) - k, 1)
        cov_iid = Ai * s2[:, None, None]
        dg = np.maximum(np.diagonal(cov, axis1=1, axis2=2), np.diagonal(cov_iid, axis1=1, axis2=2))
        cov = cov.copy()
        idx = np.arange(k)
        cov[:, idx, idx] = dg
    return beta, cov, r


def gls(zs, cov, prior_m, prior_v):
    """zs: list of (W, n) signals; cov: (W, n, k, k); prior (W, n). Returns posterior mean/var and weights."""
    k = len(zs)
    Si = np.linalg.inv(cov)
    one = np.ones(k)
    p_obs = np.einsum("i,wnij,j->wn", one, Si, one)
    wts = np.einsum("wnij,j->wni", Si, one)
    p = p_obs + 1 / prior_v
    m = (np.einsum("wni,iwn->wn", wts, np.stack(zs)) + prior_m / prior_v) / p
    return m, 1 / p, wts / p[..., None]


def prior_of():
    return M_S[SEG_OF][None, :], (SD_C ** 2 + SD_I[SEG_OF] ** 2)[None, :]


# ------------------------------------------------------------------------------------------------------------
# Estimators
# ------------------------------------------------------------------------------------------------------------
def seg_means(val, seg, cluster, ncl):
    """Segment means with date-clustered variance (iid floor). val (W, n)."""
    out_m = np.zeros((val.shape[0], 8))
    out_v = np.zeros((val.shape[0], 8))
    for s in range(8):
        sel = seg == s
        v = val[:, sel]
        cls = cluster[sel]
        ucl = np.unique(cls)
        m = v.mean(1)
        cm = np.stack([v[:, cls == u_].mean(1) for u_ in ucl], 1)          # cluster means
        G = len(ucl)
        vc = cm.var(1, ddof=1) / G if G > 1 else v.var(1) / v.shape[1]
        vi = v.var(1, ddof=1) / v.shape[1]
        out_m[:, s] = m
        out_v[:, s] = np.maximum(vc, vi)
    return out_m, out_v


def shrink_to(m, v, pm, pv):
    post_v = 1 / (1 / v + 1 / pv)
    return (m / v + pm / pv) * post_v, post_v


def fbe_b(d, components=True):
    tr, te = d["tr"], d["te"]
    seg, cl = tr["seg"], tr["cluster"]
    pm_f, pv_f = BF[None, :], (BF / 3)[None, :] ** 2
    resid = tr["f"] - tr["y"] + tr["C_hat"] - WA * tr["x_hat"]          # control coef -1, w_a 0.30 fixed
    if components:
        mN, vN = seg_means(tr["eN"], seg, cl, tr["ncl"])
        mX, vX = seg_means(tr["eX"], seg, cl, tr["ncl"])
        bN, vbN = shrink_to(mN, vN, PHI_N * BF, (PHI_N * BF / 3) ** 2)
        bX, vbX = shrink_to(mX, vX, PHI_X * BF, (PHI_X * BF / 3) ** 2)
        mK, vK = seg_means(resid - (bN + bX)[:, seg], seg, cl, tr["ncl"])
        bK, vbK = shrink_to(mK, vK, PHI_K * BF, (PHI_K * BF / 3) ** 2)
        bf, vbf = bN + bX + bK, vbN + vbX + vbK
    else:
        mF, vF = seg_means(resid, seg, cl, tr["ncl"])
        bf, vbf = shrink_to(mF, vF, pm_f, pv_f)
    lt = tr["late"] > 0.5
    ures = np.where(lt, tr["u"] - tr["y"] + tr["C_hat"], np.nan)
    mU = np.zeros((ures.shape[0], 8))
    vU = np.zeros((ures.shape[0], 8))
    for s in range(8):
        v_ = ures[:, seg == s]
        n_ = np.maximum((~np.isnan(v_)).sum(1), 1)
        mU[:, s] = np.nan_to_num(np.nanmean(v_, 1), nan=0.0)
        vU[:, s] = np.nan_to_num(np.nanvar(v_, 1), nan=0.01) / n_ + 1e-6
    bu, vbu = shrink_to(mU, vU, (BU + GU)[None, :], ((BU + GU) / 3)[None, :] ** 2)
    S_ = SEG_OF
    zu = te["u"] - bu[:, S_]
    zf = te["f"] - bf[:, S_] - WA * te["x_hat"]
    za = te["a"]
    sf = KTAB[S_][None, :] * te["sd_stated"]
    var_k = np.stack([np.full_like(sf, SDU ** 2), np.full_like(sf, SDA ** 2), sf ** 2], -1)
    wprec = (1 / var_k) / (1 / var_k).sum(-1, keepdims=True)
    wts = 0.5 * wprec + 0.5 / 3
    md = wts[..., 0] * zu + wts[..., 1] * za + wts[..., 2] * zf
    vd = (wts ** 2 * var_k).sum(-1) + wts[..., 0] ** 2 * vbu[:, S_] + wts[..., 2] ** 2 * vbf[:, S_]
    pm, pv = prior_of()
    vpost = 1 / (1 / vd + 1 / pv)
    m = (md / vd + pm / pv) * vpost
    return m, np.sqrt(vpost)


def pooled_slopes(d):
    """Canonical pooled regression on the other seven groups: (f - y) on [1, D, gap, flag].
    Returns the RELATIVE regime effect (slope_D / intercept, since M1 multiplies b^f) with its delta-method
    variance, and the ABSOLUTE gap and flag slopes (M2 and M5 act in pp) with their covariance."""
    p = d["pool"]
    X = np.stack([np.ones_like(p["y"]), p["D"], np.maximum(p["u"] - p["a"] - 0.05, 0), p["flag"]], -1)
    b, cov, _ = huber(X, p["f"] - p["y"])
    b0 = np.maximum(b[:, 0], 0.005)
    relD = b[:, 1] / b0
    g = np.stack([-b[:, 1] / b0 ** 2, 1 / b0], -1)
    vrelD = np.einsum("wi,wij,wj->w", g, cov[:, :2, :2], g)
    return relD, vrelD, b[:, 2:], cov[:, 2:, 2:]


def re_pool(m, v, prior_mean, tau_seg=1 / 3, tau_grp=1 / 3):
    """Hierarchical shrinkage on the relative deviation from the segment priors:
         r_s = rbar + u_s + noise_s,  u_s ~ N(0, tau_seg^2) (segment random effect, prior sd 1/3 of the mean),
         rbar ~ N(0, tau_grp^2) (group-level shift pooled across the eight segments; canonical prior sd 1/3).
    Returns segment bias estimates, their variances, and the data-implied between-segment variance (diagnostic)."""
    r = m / prior_mean[None, :] - 1
    vr = v / prior_mean[None, :] ** 2
    wt = 1 / (vr + tau_seg ** 2)
    prec_g = 1 / tau_grp ** 2 + wt.sum(1)
    rbar = (wt * r).sum(1) / prec_g
    vrbar = 1 / prec_g
    lam = tau_seg ** 2 / (tau_seg ** 2 + vr)
    rs = rbar[:, None] + lam * (r - rbar[:, None])
    vrs = lam * vr + (1 - lam) ** 2 * vrbar[:, None]
    w0 = 1 / vr
    rb0 = (w0 * r).sum(1) / w0.sum(1)
    Q = (w0 * (r - rb0[:, None]) ** 2).sum(1)
    cden = w0.sum(1) - (w0 ** 2).sum(1) / w0.sum(1)
    tau2_dl = np.maximum(0.0, (Q - (r.shape[1] - 1)) / np.maximum(cden, 1e-9))
    return prior_mean[None, :] * (1 + rs), (prior_mean[None, :] ** 2) * vrs, tau2_dl


def fbe_r(d, components=True, cap_forecast=False, kappa_g=1.75, use_cuf=True, fixed_ra_coefs=False,
          fusion="gls"):
    tr, te = d["tr"], d["te"]
    seg, cl, ncl = tr["seg"], tr["cluster"], tr["ncl"]
    relD, vrelD, slopes, cov_s = pooled_slopes(d)
    Xc_tr = np.stack([np.maximum(tr["u"] - tr["a"] - 0.05, 0), tr["flag"]], -1)
    resid0 = (tr["f"] - tr["y"]) - np.einsum("wnk,wk->wn", Xc_tr, slopes)      # absolute pooled gap and flag terms
    Wn, n = resid0.shape
    dummies = np.zeros((n, 8))
    dummies[np.arange(n), seg] = 1.0
    regime = 1.0 + relD[:, None] * tr["D"]                                   # relative regime multiplier (pooled)
    if fixed_ra_coefs:                    # control coefficient -1 and w_a 0.30 imposed (as FBE-B-RA)
        resid0 = resid0 + tr["C_hat"] - WA * tr["x_hat"]
        X = np.concatenate([dummies[None, :, :] * regime[..., None], np.zeros((Wn, n, 2))], -1)
        prior_fix = [(8, np.zeros(Wn), np.full(Wn, 1e-6), 0.1), (9, np.zeros(Wn), np.full(Wn, 1e-6), 0.1)]
    else:
        X = np.concatenate([dummies[None, :, :] * regime[..., None], tr["x_hat"][..., None], tr["C_hat"][..., None]], -1)
        prior_fix = None
    if components:
        # fast components: pooled relative regressions with their own regime term (estimated within RA)
        def comp(eC, phi, sig):
            base = (phi * BF)[seg]
            Xn = np.stack([base[None, :] * np.ones((Wn, 1)), base[None, :] * tr["D"]], -1)
            pri = [(1, relD, np.sqrt(vrelD + 0.1 ** 2), sig)]  # regime effect: pooled relative prior
            bc, cc, _ = huber(Xn, eC, cl, ncl, prior=pri)
            return bc, cc                                 # coef on base (1 + r) and on base x D
        bN, cN = comp(tr["eN"], PHI_N, 0.022)
        bX, cX = comp(tr["eX"], PHI_X, 0.009)
        fitNX_tr = (PHI_N * BF)[seg][None, :] * (bN[:, 0:1] + bN[:, 1:2] * tr["D"]) + \
                   (PHI_X * BF)[seg][None, :] * (bX[:, 0:1] + bX[:, 1:2] * tr["D"])
        bK, covK, _ = huber(X, resid0 - fitNX_tr, cl, ncl, prior=prior_fix)
        mK, vK = bK[:, :8], np.diagonal(covK, axis1=1, axis2=2)[:, :8]
        bKs, vKs, tau2 = re_pool(mK, vK, PHI_K * BF)
        coef_x, var_x = (np.full(Wn, WA), np.zeros(Wn)) if fixed_ra_coefs else (bK[:, 8], covK[:, 8, 8])
        nx = (PHI_N * BF)[None, :] * (bN[:, 0:1] + bN[:, 1:2]) + (PHI_X * BF)[None, :] * (bX[:, 0:1] + bX[:, 1:2])
        vnx = (PHI_N * BF)[None, :] ** 2 * (cN[:, 0, 0] + cN[:, 1, 1] + 2 * cN[:, 0, 1])[:, None] + \
              (PHI_X * BF)[None, :] ** 2 * (cX[:, 0, 0] + cX[:, 1, 1] + 2 * cX[:, 0, 1])[:, None]
        # test date is D = 1: K part scaled by the pooled relative regime effect
        bias_seg = nx + bKs * (1 + relD[:, None])
        var_seg = vnx + vKs * (1 + relD[:, None]) ** 2 + bKs ** 2 * vrelD[:, None]
    else:
        bT, covT, _ = huber(X, resid0, cl, ncl, prior=prior_fix)
        mT, vT = bT[:, :8], np.diagonal(covT, axis1=1, axis2=2)[:, :8]
        bTs, vTs, tau2 = re_pool(mT, vT, BF)
        coef_x, var_x = (np.full(Wn, WA), np.zeros(Wn)) if fixed_ra_coefs else (bT[:, 8], covT[:, 8, 8])
        bias_seg = bTs * (1 + relD[:, None])
        var_seg = vTs * (1 + relD[:, None]) ** 2 + bTs ** 2 * vrelD[:, None]
    S_ = SEG_OF
    Xc_te = np.stack([np.maximum(te["u"] - te["a"] - 0.05, 0), te["flag"]], -1)
    bf_te = bias_seg[:, S_] + np.einsum("wnk,wk->wn", Xc_te, slopes) + coef_x[:, None] * te["x_hat"]
    vbf_te = var_seg[:, S_] + np.einsum("wnk,wkj,wnj->wn", Xc_te, cov_s, Xc_te) + var_x[:, None] * te["x_hat"] ** 2
    # underwriting bias: segment intercepts + late + control, RE-pooled relative to priors
    Xu = np.concatenate([np.broadcast_to(dummies, (Wn, n, 8)), tr["late"][..., None], tr["C_hat"][..., None]], -1)
    bu_, covu, _ = huber(Xu, tr["u"] - tr["y"], cl, ncl, prior=[(8, np.full(Wn, GU.mean()), np.full(Wn, 0.01), 0.12)])
    bus, vus, _ = re_pool(bu_[:, :8], np.diagonal(covu, axis1=1, axis2=2)[:, :8], BU)
    bu_te = bus[:, S_] + bu_[:, 8:9] * te["late"]
    vbu_te = vus[:, S_] + covu[:, 8, 8][:, None] * te["late"]
    du, df = te["u"] - te["a"], te["f"] - te["a"]
    # within-segment covariance (segment biases differ, so the raw cross-section would mix them in)
    du_c = du.copy()
    df_c = df.copy()
    for s_ in range(8):
        sel = S_ == s_
        du_c[:, sel] -= du[:, sel].mean(1, keepdims=True)
        df_c[:, sel] -= df[:, sel].mean(1, keepdims=True)
    dof = NP - 8
    cuf = (du_c * df_c).sum(1) / dof - SDA ** 2
    sf = kappa_g * te["sd_stated"]
    cuf = np.clip(cuf[:, None], 0.0, 0.95 * SDU * sf)
    pm, pv = prior_of()
    pm = np.broadcast_to(pm, te["u"].shape)
    pv = np.broadcast_to(pv, te["u"].shape)
    zs = [te["u"] - bu_te, te["a"], te["f"] - bf_te]
    if fusion == "shrink50" and not cap_forecast:
        # sec. 8.5 rule: precision weights shrunk 50% toward equal; covariances only in the predictive variance
        var_k = np.stack([np.full_like(sf, SDU ** 2), np.full_like(sf, SDA ** 2), sf ** 2], -1)
        wp = (1 / var_k) / (1 / var_k).sum(-1, keepdims=True)
        wts = 0.5 * wp + 0.5 / 3
        md = sum(wts[..., k] * zs[k] for k in range(3))
        vd = (wts ** 2 * var_k).sum(-1) + (2 * wts[..., 0] * wts[..., 2] * cuf if use_cuf else 0.0)
        vd = vd + wts[..., 0] ** 2 * vbu_te + wts[..., 2] ** 2 * vbf_te
        v = 1 / (1 / vd + 1 / pv)
        m = (md / vd + pm / pv) * v
        return m, np.sqrt(v), tau2
    cov = np.zeros(te["u"].shape + (3, 3))
    cov[..., 0, 0] = SDU ** 2
    cov[..., 1, 1] = SDA ** 2
    cov[..., 2, 2] = sf ** 2 if not cap_forecast else 1e6
    if (not cap_forecast) and use_cuf:
        cov[..., 0, 2] = cov[..., 2, 0] = cuf
    m, v, wn = gls(zs, cov, pm, pv)
    s = np.sqrt(v + wn[..., 0] ** 2 * vbu_te + wn[..., 2] ** 2 * vbf_te)
    return m, s, tau2


def oracle(d):
    te, fl = d["te"], d["fl"]
    S_ = SEG_OF
    f = te["f"] - te["shift"]
    u = te["u"] - te["shift"]
    a = te["a"] - te["shift"]
    if fl["m5"]:
        f = f - fl["delta"] - 0.02 * te["flag"]
    if fl["m2"]:
        w = m2_w(te["u"], te["a"])                          # the generator applied M2 to the unshifted signals
        f = (f - w * u) / (1 - w)
    zf = f - te["bft"] - WA * te["x_true"]
    zu = u - BU[S_] - GU[S_] * te["late"]
    t3v = T3V if fl["m3"] else 1.0
    sf2 = SDF ** 2 * t3v * np.ones_like(zf)
    cov = np.zeros(zf.shape + (3, 3))
    cov[..., 0, 0] = SDU ** 2 * t3v
    cov[..., 1, 1] = SDA ** 2
    cov[..., 2, 2] = sf2
    if fl["m4"]:
        cov[..., 0, 2] = cov[..., 2, 0] = 0.6 * SDU * SDF * t3v
    pm, pv = prior_of()
    pm = np.broadcast_to(pm, zf.shape)
    pv = np.broadcast_to(pv, zf.shape)
    m, v, _ = gls([zu, a, zf], cov, pm, pv)
    return m, np.sqrt(v)


def crps_gauss(y, m, s):
    z = (y - m) / s
    Phi = 0.5 * (1 + _erf(z / math.sqrt(2)).astype(float))
    return s * (z * (2 * Phi - 1) + 2 * np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi) - 1 / math.sqrt(math.pi))


def metrics(d, m, s):
    mu = d["te"]["mu"]
    h = H_S[SEG_OF][None, :]
    sell = mu < h
    out = dict(crps_pp=float(crps_gauss(mu, m, s).mean() * 100), cov80=float((np.abs(mu - m) <= Z80 * s).mean()),
               bias_sell_pp=float(((m - mu)[sell]).mean() * 100),
               regret_pp=float((np.abs(mu - h) * ((m < h) != sell)).mean() * 100),
               rmse_pp=float(np.sqrt(((m - mu) ** 2).mean()) * 100))
    cs = {}
    for s_, nm in enumerate(SEGS):
        sel = SEG_OF == s_
        cs[nm] = float((np.abs(mu[:, sel] - m[:, sel]) <= Z80 * s[:, sel]).mean())
    out["cov80_by_segment"] = cs
    return out


def detection(d):
    """RA-only and pooled power for the canonical terms; RA-only power for the anchoring term."""
    tr, p = d["tr"], d["pool"]
    seg, cl, ncl = tr["seg"], tr["cluster"], tr["ncl"]
    Wn, n = tr["y"].shape
    dummies = np.zeros((n, 8))
    dummies[np.arange(n), seg] = 1.0
    X = np.concatenate([np.broadcast_to(dummies, (Wn, n, 8)), tr["D"][..., None],
                        np.maximum(tr["u"] - tr["a"] - 0.05, 0)[..., None], tr["flag"][..., None],
                        tr["x_hat"][..., None], tr["C_hat"][..., None]], -1)
    hasD = (tr["D"].min(1) < 0.5) & (tr["D"].max(1) > 0.5)
    X[~hasD, :, 8] = 0.0
    pri = [(8, np.zeros(Wn), np.where(hasD, 1e3, 1e-6), 0.12)]       # absorbs the empty regime column only
    b, cov, _ = huber(X, tr["f"] - tr["y"], cl, ncl, prior=pri)
    se = np.sqrt(np.maximum(np.diagonal(cov, axis1=1, axis2=2), 1e-14))
    t = b / se
    t[~hasD, 8] = 0.0
    has_flag = tr["flag"].sum(1) > 0
    out = dict(ra_power_regime=float((t[:, 8] > 1.96).mean()), ra_power_gap=float((t[:, 9] > 1.96).mean()),
               ra_power_flag=float(np.where(has_flag, t[:, 10] > 1.96, False).mean()),
               ra_power_anchor=float((t[:, 11] > 1.96).mean()))
    Xp = np.stack([np.ones_like(p["y"]), p["D"], np.maximum(p["u"] - p["a"] - 0.05, 0), p["flag"]], -1)
    bp, covp, _ = huber(Xp, p["f"] - p["y"])
    tp = bp / np.sqrt(np.maximum(np.diagonal(covp, axis1=1, axis2=2), 1e-14))
    hf = p["flag"].sum(1) > 0
    out.update(pool_power_regime=float((tp[:, 1] > 1.96).mean()), pool_power_gap=float((tp[:, 2] > 1.96).mean()),
               pool_power_flag=float(np.where(hf, tp[:, 3] > 1.96, False).mean()))
    return out


def run(variant, seed, opt):
    d = generate(variant, seed, opt)
    comp = opt.get("components", True)
    res = dict(baseline=metrics(d, *fbe_b(d, components=comp)))
    mR, sR, tau2 = fbe_r(d, components=comp, fusion="shrink50")
    res["robust"] = metrics(d, mR, sR)
    res["robust"]["tau2_seg_rel_median_DL"] = float(np.median(tau2))
    mG, sG, _ = fbe_r(d, components=comp, fusion="gls")
    res["robust_gls"] = metrics(d, mG, sG)
    mC, sC, _ = fbe_r(d, components=comp, cap_forecast=True)
    res["robust_cap"] = metrics(d, mC, sC)
    res["oracle"] = metrics(d, *oracle(d))
    res["detection"] = detection(d)
    o = res["oracle"]
    for est in ("baseline", "robust", "robust_gls", "robust_cap"):
        r = res[est]
        r["crps_excess_vs_oracle"] = r["crps_pp"] / o["crps_pp"] - 1
        r["regret_excess_vs_oracle"] = r["regret_pp"] / o["regret_pp"] - 1
    return res


def gates(r, variant):
    """Canonical thresholds. Returns pass/fail per estimator."""
    out = {}
    for est in ("baseline", "robust", "robust_gls", "robust_cap"):
        x = r[est]
        if variant == "MALL":
            ok = dict(crps=x["crps_excess_vs_oracle"] <= 0.25, cov=x["cov80"] >= 0.70,
                      sell_bias=abs(x["bias_sell_pp"]) <= 2.0, regret=x["regret_excess_vs_oracle"] <= 0.50)
            gate = "G-C"
        elif variant == "M0":
            ok = dict(crps=x["crps_excess_vs_oracle"] <= 0.15, cov=0.75 <= x["cov80"] <= 0.85,
                      sell_bias=abs(x["bias_sell_pp"]) <= 1.5, regret=x["regret_excess_vs_oracle"] <= 0.35)
            gate = "G-A(+B metrics)"
        else:
            ok = dict(crps=x["crps_excess_vs_oracle"] <= 0.15, cov=0.72 <= x["cov80"] <= 0.88,
                      sell_bias=abs(x["bias_sell_pp"]) <= 1.5, regret=x["regret_excess_vs_oracle"] <= 0.35)
            gate = "G-B"
        out[est] = dict(gate=gate, **{k: bool(v) for k, v in ok.items()}, all=bool(all(ok.values())))
    return out


def main():
    src = load_rame_linkage()
    canon = ["M0", "M1", "M2", "M3", "M4", "M5", "M5s", "M6", "MALL"]
    plans = {}
    for i, v in enumerate(canon):
        plans[f"{v}"] = (v, 3000 + i, dict())
    plans.update({
        "M0|components_absent": ("M0", 3100, dict(components=False)),
        "M5s|components_absent": ("M5s", 3101, dict(components=False)),
        "MALL|components_absent": ("MALL", 3102, dict(components=False)),
        "M0|RAME_AL": ("M0", 3200, dict(rame="AL")),
        "M0|RAME_TW": ("M0", 3201, dict(rame="TW")),
        "MALL|RAME_TW": ("MALL", 3202, dict(rame="TW")),
        "M0|G0=2%": ("M0", 3300, dict(g0=0.02)),
        "M0|G0=5%": ("M0", 3301, dict(g0=0.05)),
        "M0|G0=8%": ("M0", 3302, dict(g0=0.08)),
        "M0|G0=8%|RAME_AL": ("M0", 3303, dict(g0=0.08, rame="AL")),
        "M0|archive_8y": ("M0", 3400, dict(dtr=8)),
        "MALL|archive_8y": ("MALL", 3401, dict(dtr=8)),
        "M0|kappa_truth_TAB": ("M0", 3500, dict(ktruth="TAB")),
        "MALL|kappa_truth_TAB": ("MALL", 3501, dict(ktruth="TAB")),
        "MALL|components_absent|RAME_TW": ("MALL", 3600, dict(components=False, rame="TW")),
    })
    res = dict(label=SYN, worlds=W, n_test=NP, segments=SEGS, n_test_by_segment=NTE.tolist(),
               rame_linkage_source=src, rame_linkage=RAME_Q, g0_residual_share=G0_ERR, table={}, gates={})
    for name, (v, seed, opt) in plans.items():
        r = run(v, seed, opt)
        res["table"][name] = r
        res["gates"][name] = gates(r, v)
        b, q, c_, dt = r["baseline"], r["robust"], r["robust_cap"], r["detection"]
        gq = r["robust_gls"]
        print(f"{name:34s} | B {b['crps_excess_vs_oracle']:+6.1%} {b['cov80']:.3f} {b['bias_sell_pp']:+5.2f} "
              f"{b['regret_excess_vs_oracle']:+6.1%} | R {q['crps_excess_vs_oracle']:+6.1%} {q['cov80']:.3f} "
              f"{q['bias_sell_pp']:+5.2f} {q['regret_excess_vs_oracle']:+6.1%} | Rgls {gq['crps_excess_vs_oracle']:+6.1%} "
              f"{gq['cov80']:.3f} | Rcap {c_['crps_excess_vs_oracle']:+6.1%} "
              f"{c_['cov80']:.3f} {c_['bias_sell_pp']:+5.2f} | RA pow D/gap/flag/anch {dt['ra_power_regime']:.2f}/"
              f"{dt['ra_power_gap']:.2f}/{dt['ra_power_flag']:.2f}/{dt['ra_power_anchor']:.2f} pool flag "
              f"{dt['pool_power_flag']:.2f}", flush=True)
        OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("wrote", OUT, SYN)


if __name__ == "__main__":
    main()
