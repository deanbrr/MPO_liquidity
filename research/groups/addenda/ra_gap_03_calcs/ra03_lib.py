"""RA gap 03 library: the canonical monthly oil/fiscal generator, the owner-draw engine, ENR segment valuation
on the futures strip, and option helpers.

SYNTHETIC - NOT ADIC DATA. Every balance, path and probability produced with this module is a synthetic draw from
design defaults ([I]) anchored on the public inputs listed in MARKET below ([S]). Nothing here is an ADIC figure or
a forecast.

What "canonical" means here (main synthesis s4.1 and s4.7; gap_04 s6.1; ARCHITECTURE s4.1; BUILD_SPEC s4.10):
  * shock type Z in {N, B, SG, DB, SS, GW} evolves MONTHLY on the principal 12th root of stream 03's annual prior
    (ARCHITECTURE s4.1 / QUANT-29; the I + (P-I)/12 linearisation is kept only as a comparison);
  * Z is coupled to the macro regime S in {EXP, LATE, CRIS, RECV} through
        P(Z' = j | Z = i, S' = s) proportional to Pm[i, j] * kappa[s, j],
    with kappa calibrated so that P(S = CRIS | Z = DB) >= 0.8 and P(S = CRIS | Z = SG) ~ 0.15;
  * the Gulf-war (GW) dwell is semi-Markov: its exit hazard depends on elapsed duration (discrete Weibull), started
    at the war's elapsed duration on the as-of date;
  * oil is two-factor and starts from the futures curve, never from spot: chi0 = ln spot - ln front month (a
    transient physical premium that decays at Schwartz-Smith's kappa), x0 = ln front month (the slow factor with
    stream 03's kappa = 0.40 a year, state drifts, vols and GW jumps), xi = the back of the curve (~$70);
  * the owner draw uses main s4.7's linear fiscal map (revenue = price x volume), the IMF-fused 2027 fiscal balance
    (gap_04 s6.1 step 7), d_2026 = 5.8%, smoothing rho = 0.5, the 5-10% band and override probabilities.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import fractional_matrix_power
from scipy.special import ndtr

LABEL = "SYNTHETIC - NOT ADIC DATA [I-calc / I-MC on public inputs]"

# ------------------------------------------------------------------------------------------------ public inputs [S]
MARKET = {
    "asof": "2026-10-15",
    # NYMEX BZ (Brent last-day financial) settlements, Thu 15 Oct 2026, CME Daily Bulletin #199, as relayed by
    # baratelliinstitute.com/oil-futures-curve (page dated 17 Oct 2026) [S-sec]. Dec-26 $105.92 also reported by
    # HDFCSky (17 Oct 2026) as the ICE December settle [S-sec].
    "strip": {  # contract month -> $/bbl
        "2026-12": 105.92, "2027-01": 103.17, "2027-02": 100.60, "2027-03": 98.46, "2027-04": 96.58,
        "2027-05": 94.85, "2027-06": 93.20, "2027-07": 91.62, "2027-08": 90.13, "2027-09": 88.72,
        "2027-10": 87.40, "2027-11": 86.19, "2027-12": 85.08, "2028-01": 84.03, "2028-02": 83.07,
        "2028-03": 82.20, "2028-04": 81.43, "2028-05": 80.75, "2028-06": 80.12, "2028-07": 79.52,
        "2028-08": 78.94, "2028-09": 78.37, "2028-12": 76.83, "2029-06": 74.47, "2029-12": 72.32,
        "2030-12": 69.16},
    "spot_eia_2026_10_14": 126.55,          # EIA RBRTE via FRED DCOILBRENTEU [S]
    "ovx_2026_10_15": 49.13,                # Cboe OVX via FRED OVXCLS [S]
    "war_onset": "2026-02-28",              # EIA STEO (Jun 2026) via stream 03 s4.4 [S]
    "steo_oct26_brent_q": {"4Q26": 104.69, "1Q27": 94.90, "2Q27": 87.00, "3Q27": 80.03, "4Q27": 73.94,
                           "2026": 96.32, "2027": 83.74},   # EIA STEO Oct 2026, Table 2 [S]
    "steo_oct26_shutins_kbd": {"Mar-Jul26": 8512, "Aug26": 5760, "Sep26": 4770, "4Q26": 4470, "1Q27": 2683},
    "steo_oct26_uae_liquids_mbd": {"2025": 4.34, "2026": 4.12, "2027": 5.20, "4Q27": 5.29},
    "imf_fb_2027_pp": 4.4,                  # IMF DataMapper net lending 2027, via stream 03 s4.5 [S]
}
F1 = MARKET["strip"]["2026-12"]             # front month on the as-of date: the barrel unit of the ledger
SPOT = MARKET["spot_eia_2026_10_14"]
LN70 = math.log(70.0)
ELAPSED_GW_MONTHS = 7.5                     # 28 Feb -> mid-Oct 2026

# ------------------------------------------------------------------------------------------------ stream 03 priors
ZN = ("N", "B", "SG", "DB", "SS", "GW")
iN, iB, iSG, iDB, iSS, iGW = range(6)
SN = ("EXP", "LATE", "CRIS", "RECV")
sEXP, sLATE, sCRIS, sRECV = range(4)
PZ_A = np.array([[.62, .15, .10, .05, .04, .04],      # stream 03 Table 6.3 (annual, rows = from) [I]
                 [.40, .40, .05, .06, .07, .02],
                 [.38, .12, .42, .04, .02, .02],
                 [.35, .30, .20, .10, .03, .02],
                 [.30, .05, .10, .35, .15, .05],
                 [.30, .05, .35, .05, .05, .20]])
MU_Z = np.array([0.0, 0.20, -0.35, -0.45, 0.30, 0.10])    # annual log drift by state [I, stream 03 s6.4]
SIG_Z = np.array([0.20, 0.20, 0.20, 0.25, 0.25, 0.30])    # annual vol by state [I]
KAPPA_X = 0.40                                            # slow-factor reversion, a year [I, stream 03]
KM = 1.0 - (1.0 - KAPPA_X) ** (1.0 / 12.0)                # monthly
KAPPA_CHI_SS = 1.49                                       # Schwartz & Smith (2000) Table 2, futures data [S]
# The physical spot premium over the front month (chi0 = ln 126.55/105.92 = 0.178) is priced by the strip to vanish
# within about a month: at the Schwartz-Smith half-life (5.6 months) the model's expected spot one month out would sit
# ~15% above the Dec-26 contract. Its half-life is therefore fitted to the front of the curve [I]: 0.4 months.
CHI_HALF_LIFE_MONTHS = 0.4
KAPPA_CHI = 12.0 * math.log(2.0) / CHI_HALF_LIFE_MONTHS
GW_JUMP, GW_JUMP_P = 0.26, 0.25 / 12.0                    # +-ln(1.3) w.p. 0.25 a year, monthly (gap_04 code) [I]
W_Z = np.array([0.0, 0.0, -0.5, -1.5, -0.5, np.nan])      # fiscal wedge, pp of GDP; GW drawn N(-5, 2^2) [I]
P_OV = np.array([0.0025, 0.0025, 0.01, 0.01, 0.0025, 0.02])   # override probability by dominant state [I]
EQ_RHO = np.array([0.0, 0.2, 0.1, 0.6, -0.4, -0.5])       # oil-equity correlation by state [I, stream 03]


def stationary(P: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eig(P.T)
    s = np.real(v[:, np.argmin(np.abs(w - 1.0))])
    return s / s.sum()


def monthly_root(P: np.ndarray) -> tuple[np.ndarray, float]:
    """Principal 12th root with clipping and row renormalisation (BUILD_SPEC monthly_shock_matrix)."""
    R = np.real(fractional_matrix_power(P, 1.0 / 12.0))
    R = np.clip(R, 0.0, None)
    R = R / R.sum(axis=1, keepdims=True)
    err = float(np.abs(np.linalg.matrix_power(R, 12) - P).max())
    return R, err


def monthly_linear(P: np.ndarray) -> np.ndarray:
    return np.eye(P.shape[0]) + (P - np.eye(P.shape[0])) / 12.0


def monthly_lsq(P: np.ndarray, R0: np.ndarray | None = None) -> tuple[np.ndarray, float]:
    """Closest monthly stochastic matrix: min ||R^12 - P||_F over row-softmax parameterised R (R >= 0, rows sum
    to 1), started from the clipped principal root. Used when the principal root is not non-negative (the
    embedding problem), where clipping alone leaves a large repair error."""
    from scipy.optimize import minimize

    n = P.shape[0]
    if R0 is None:
        R0, _ = monthly_root(P)
    th0 = np.log(np.clip(R0, 1e-8, None)).ravel()

    def mat(th):
        Th = th.reshape(n, n)
        Th = Th - Th.max(axis=1, keepdims=True)
        E = np.exp(Th)
        return E / E.sum(axis=1, keepdims=True)

    def obj(th):
        D = np.linalg.matrix_power(mat(th), 12) - P
        return float((D ** 2).sum())

    sol = minimize(obj, th0, method="L-BFGS-B", options={"maxiter": 20000, "maxfun": 200000})
    R = mat(sol.x)
    return R, float(np.abs(np.linalg.matrix_power(R, 12) - P).max())


# ------------------------------------------------------------------------------------------------ macro regime S
def s_chain(dwell=(48.0, 24.0, 12.0, 12.0), c_exp=0.20, c_late=0.60, c_recv=0.10) -> np.ndarray:
    """Monthly 4-state chain. dwell = mean months in EXP, LATE, CRIS, RECV (main s4.1 targets: crisis 6-18,
    expansion 36-60). c_* = share of exits that go to CRIS. [I]"""
    dE, dL, dC, dR = dwell
    P = np.zeros((4, 4))
    P[sEXP, sEXP] = 1 - 1 / dE
    P[sEXP, sLATE] = (1 / dE) * (1 - c_exp)
    P[sEXP, sCRIS] = (1 / dE) * c_exp
    P[sLATE, sLATE] = 1 - 1 / dL
    P[sLATE, sCRIS] = (1 / dL) * c_late
    P[sLATE, sEXP] = (1 / dL) * (1 - c_late)
    P[sCRIS, sCRIS] = 1 - 1 / dC
    P[sCRIS, sRECV] = 1 / dC
    P[sRECV, sRECV] = 1 - 1 / dR
    P[sRECV, sEXP] = (1 / dR) * (1 - c_recv)
    P[sRECV, sCRIS] = (1 / dR) * c_recv
    return P


def s_chain_for_share(target_cris: float) -> np.ndarray:
    """Scale the EXP and LATE dwell (time between crises) so that the stationary crisis share hits target."""
    lo, hi = 0.2, 5.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        P = s_chain(dwell=(48.0 * mid, 24.0 * mid, 12.0, 12.0))
        if stationary(P)[sCRIS] > target_cris:
            lo = mid
        else:
            hi = mid
    return s_chain(dwell=(48.0 * mid, 24.0 * mid, 12.0, 12.0))


# ------------------------------------------------------------------------------------------------ coupling kappa
def kappa_matrix(a: float, b: float, c: float, boom_cris: float = 0.3, ss_noncris: float = 1.0) -> np.ndarray:
    """kappa[s, j] = 1 except DB (a in CRIS, b elsewhere), SG in CRIS (c), B in CRIS (boom_cris) and SS outside
    CRIS (ss_noncris). [I]"""
    K = np.ones((4, 6))
    K[:, iDB] = b
    K[sCRIS, iDB] = a
    K[sCRIS, iSG] = c
    K[sCRIS, iB] = boom_cris
    for s in (sEXP, sLATE, sRECV):
        K[s, iSS] = ss_noncris
    return K


def joint_chain(PS: np.ndarray, PZm: np.ndarray, K: np.ndarray) -> np.ndarray:
    """24-state (S, Z) chain with S' drawn first, then Z' | Z, S' ~ PZm[Z, :] * K[S', :] (normalised)."""
    n = 4 * 6
    J = np.zeros((n, n))
    for s in range(4):
        for z in range(6):
            for s2 in range(4):
                w = PZm[z] * K[s2]
                w = w / w.sum()
                J[s * 6 + z, s2 * 6:(s2 + 1) * 6] += PS[s, s2] * w
    return J


def joint_stats(PS, PZm, K) -> dict:
    pi = stationary(joint_chain(PS, PZm, K)).reshape(4, 6)
    pz = pi.sum(axis=0)
    ps = pi.sum(axis=1)
    return {"pz": pz, "ps": ps, "p_cris_given_z": pi[sCRIS] / np.maximum(pz, 1e-12), "pi": pi}


def calibrate_kappa(PS, PZm, target_db=0.060, target_cris_db=0.85, target_cris_sg=0.15) -> tuple[np.ndarray, dict]:
    """Fit kappa so that P(CRIS | DB) = 0.85, P(CRIS | SG) = 0.15 (stream 03 s6.3; main s4.1) while the stationary
    shock-type shares stay close to the annual prior's (DB set to 0.06, inside the elicited 0.02-0.06)."""
    from scipy.optimize import least_squares

    tgt = stationary(PZ_A).copy()
    tgt[iDB] = target_db
    tgt = tgt / tgt.sum()

    def res(th):
        a, b, c, g, e = np.exp(th)
        st = joint_stats(PS, PZm, kappa_matrix(a, b, c, boom_cris=g, ss_noncris=e))
        r = [(st["p_cris_given_z"][iDB] - target_cris_db) * 10, (st["p_cris_given_z"][iSG] - target_cris_sg) * 10]
        r += list((st["pz"] - tgt) * 20)
        return r

    sol = least_squares(res, x0=np.log([4.0, 0.2, 1.0, 0.3, 1.0]), bounds=(np.log(1e-3), np.log(1e3)))
    a, b, c, g, e = np.exp(sol.x)
    K = kappa_matrix(a, b, c, boom_cris=g, ss_noncris=e)
    return K, {"a_cris_db": a, "b_noncris_db": b, "c_cris_sg": c, "g_cris_boom": g, "e_noncris_ss": e,
               "target_pz": tgt, **{k: v for k, v in joint_stats(PS, PZm, K).items() if k != "pi"}}


# ------------------------------------------------------------------------------------------------ GW duration law
def weibull_hazard(d: np.ndarray, lam: float, k: float) -> np.ndarray:
    """Monthly exit probability from GW after d months elapsed (discrete Weibull)."""
    return 1.0 - np.exp(-(((d + 1.0) / lam) ** k) + ((d / lam) ** k))


def weibull_lambda_for_mean(mean_months: float, k: float) -> float:
    return mean_months / math.gamma(1.0 + 1.0 / k)


# ------------------------------------------------------------------------------------------------ the generator
class Gen:
    """Monthly canonical generator. Index t = 0 is the as-of date (mid-Oct 2026); t = 1 is mid-Nov 2026; months
    t = 3 + 12k .. 14 + 12k are calendar year 2027 + k."""

    def __init__(self, PS: np.ndarray, PZm: np.ndarray, K: np.ndarray, gw_mode: str = "weibull", gw_k: float = 1.6,
                 gw_mean: float | None = None):
        self.PS, self.PZm, self.K = PS, PZm, K
        self.gw_mode, self.gw_k = gw_mode, gw_k
        mean_mem = 1.0 / (1.0 - PZm[iGW, iGW])
        self.gw_mean = gw_mean if gw_mean is not None else mean_mem
        self.gw_lam = weibull_lambda_for_mean(self.gw_mean, gw_k)
        # exit row from GW (j != GW) and the per-S conditional transition rows
        self.rows = np.zeros((4, 6, 6))
        for s in range(4):
            w = PZm * K[s][None, :]
            self.rows[s] = w / w.sum(axis=1, keepdims=True)
        self.exit_rows = np.zeros((4, 6))
        for s in range(4):
            w = PZm[iGW] * K[s]
            w[iGW] = 0.0
            self.exit_rows[s] = w / w.sum()

    def simulate(self, n: int, T: int, seed: int, S0, Z0, x0: float, chi0: float, d0: float = ELAPSED_GW_MONTHS,
                 x_bump_at: dict | None = None, chi_kappa: float | None = None) -> dict:
        """x_bump_at = {month: dlog} adds a deterministic shock to the slow factor at that month (CRN bumps)."""
        rng = np.random.default_rng(seed)
        S = np.empty((T + 1, n), dtype=np.int8)
        Z = np.empty((T + 1, n), dtype=np.int8)
        x = np.empty((T + 1, n))
        chi = np.empty(T + 1)
        S[0] = rng.choice(4, size=n, p=np.asarray(S0, float)) if np.ndim(S0) else S0
        Z[0] = rng.choice(6, size=n, p=np.asarray(Z0, float))
        x[0] = x0 + (x_bump_at.get(0, 0.0) if x_bump_at else 0.0)
        chi[0] = chi0
        d = np.where(Z[0] == iGW, d0, 0.0)
        cumS = np.cumsum(self.PS, axis=1)
        dec = math.exp(-(KAPPA_CHI if chi_kappa is None else chi_kappa) / 12.0)
        for t in range(T):
            u1, u2, u3 = rng.random(n), rng.random(n), rng.random(n)
            eps = rng.standard_normal(n)
            uj, us = rng.random(n), rng.random(n)
            s_new = (u1[:, None] > cumS[S[t]]).sum(axis=1).clip(0, 3)
            z_old = Z[t]
            # ordinary rows (memoryless for all states; GW handled below for the semi-Markov modes)
            cum = np.cumsum(self.rows[s_new, z_old], axis=1)
            z_new = (u2[:, None] > cum).sum(axis=1).clip(0, 5)
            ingw = z_old == iGW
            if self.gw_mode == "weibull" and ingw.any():
                h = weibull_hazard(d[ingw], self.gw_lam, self.gw_k)
                leave = u3[ingw] < h
                cumx = np.cumsum(self.exit_rows[s_new[ingw]], axis=1)
                dest = (u2[ingw][:, None] > cumx).sum(axis=1).clip(0, 5)
                z_new[ingw] = np.where(leave, dest, iGW)
            S[t + 1] = s_new
            Z[t + 1] = z_new
            d = np.where(z_new == iGW, np.where(z_old == iGW, d + 1.0, 1.0), 0.0)
            jump = (z_new == iGW) & (uj < GW_JUMP_P)
            xx = x[t] + KM * (LN70 - x[t]) + MU_Z[z_new] / 12.0 + SIG_Z[z_new] / math.sqrt(12.0) * eps \
                + jump * np.where(us < 0.5, GW_JUMP, -GW_JUMP)
            if x_bump_at and (t + 1) in x_bump_at:
                xx = xx + x_bump_at[t + 1]
            x[t + 1] = xx
            chi[t + 1] = chi[t] * dec
        P = np.exp(x + chi[:, None])
        return {"S": S, "Z": Z, "x": x, "chi": chi, "P": P}


# ------------------------------------------------------------------------------------------------ owner-draw engine
H_PATH = {2026: 11.3, 2027: 10.75, 2028: 10.2, 2029: 9.65, 2030: 9.1}   # hydrocarbon revenue % GDP [S IMF, interp]
P_REF = 62.5                                                         # gap_04 code [I]
Q_NORM = {2027: 5.20 / 4.34}                                         # EIA STEO Oct 2026 [S]; 2028+ held at 4Q27
Q_NORM_LATER = 5.29 / 4.34
Q_GW = 4.12 / 4.34                                                   # 2026 average with the war [S]
SIG_BE = (math.log(70.0) - math.log(45.0)) / (2 * 1.645)             # P_BE lognormal, median 55, 90% 45-70 [I]


def owner_draws(gen_out: dict, years: int, seed: int, d2026: float = 5.8, imf_fuse: bool | str = True,
                form: str = "linear", pbe_median: float = 55.0, b: float = 0.625, overrides: bool = True,
                fusion_ref: dict | None = None) -> dict:
    """Annual draw rates (% of opening NAV) for calendar years 2027 .. 2027+years-1 on each path.

    imf_fuse: True / "shift" moves the 2027 fiscal-balance distribution's MEAN to the precision-weighted fusion of
    the model mean and the IMF projection (+4.4pp, sd 2.5), keeping each path's deviation (base); "shrink" applies
    gap_04's per-path precision weighting, which also shrinks every path's oil-driven deviation by the model weight
    (kept as a variant: it compresses the oil sensitivity of the 2027 draw); False skips fusion.

    fusion_ref: the fusion is an initial-state step (gap_04 s6.1 step 7), fitted ONCE on the base run. Pass the base
    run's output["fusion"] when evaluating bumped or stressed runs, so that the fusion does not re-centre them (a
    re-fitted fusion absorbs most of any common oil shock and makes the draw look oil-insensitive)."""
    rng = np.random.default_rng(seed)
    P, Z = gen_out["P"], gen_out["Z"]
    n = P.shape[1]
    pbe = np.exp(math.log(pbe_median) + SIG_BE * rng.standard_normal(n))
    d_prev = np.full(n, d2026)
    out_d, out_ds, out_fb, out_inband, out_pbar = [], [], [], [], []
    fusion = None
    for k in range(years):
        y = 2027 + k
        sl = slice(3 + 12 * k, 15 + 12 * k)
        pbar = P[sl].mean(axis=0)
        frac = np.stack([(Z[sl] == j).mean(axis=0) for j in range(6)], axis=1)
        h = H_PATH.get(y, 9.1)
        qn = Q_NORM.get(y, Q_NORM_LATER)
        q = qn * (1 - frac[:, iGW]) + Q_GW * frac[:, iGW]
        wgw = np.clip(rng.normal(-5.0, 2.0, n), -9.0, -1.0)
        wz = frac[:, :5] @ W_Z[:5] + frac[:, iGW] * wgw
        peff = pbar + rng.normal(0.0, 2.0, n)
        if form == "linear":
            fb = 100 * h / 100 * (peff * q - pbe) / P_REF * 1.0 + wz + rng.standard_normal(n)
        else:  # log form (stream 03 s6.5 reduced form)
            fb = h * np.log(np.maximum(peff * q, 1.0) / pbe) + wz + rng.standard_normal(n)
        if imf_fuse and y == 2027:
            if fusion_ref is None:
                sm2 = float(fb.var())
                w_model = (1 / sm2) / (1 / sm2 + 1 / 2.5 ** 2)
                fusion = {"sm2": sm2, "w_model": w_model,
                          "shift": (1 - w_model) * (MARKET["imf_fb_2027_pp"] - float(fb.mean()))}
            else:
                fusion = fusion_ref
            if imf_fuse == "shrink":     # gap_04 code: per-path precision weighting (frozen weights)
                sm2 = fusion["sm2"]
                fb = (fb / sm2 + MARKET["imf_fb_2027_pp"] / 2.5 ** 2) / (1 / sm2 + 1 / 2.5 ** 2)
            else:                        # frozen mean shift to the fused mean; path deviations kept
                fb = fb + fusion["shift"]
        dstar_raw = 7.5 - b * fb
        dstar = np.clip(dstar_raw, 5.0, 10.0)
        d = np.clip(0.5 * d_prev + 0.5 * dstar, 5.0, 10.0)
        if overrides:
            zdom = frac.argmax(axis=1)
            ov = rng.random(n) < P_OV[zdom]
            d = np.where(ov, 10.0 + rng.uniform(2.0, 5.0, n), d)
        out_d.append(d)
        out_ds.append(dstar)
        out_fb.append(fb)
        out_inband.append((dstar_raw > 5.0) & (dstar_raw < 10.0))
        out_pbar.append(pbar)
        d_prev = np.minimum(d, 10.0)
    return {"d": np.array(out_d), "dstar": np.array(out_ds), "fb": np.array(out_fb),
            "inband": np.array(out_inband), "pbar": np.array(out_pbar), "pbe": pbe, "fusion": fusion}


def pv_draws(dr: dict, r: float = 0.06, d2026: float = 5.8) -> np.ndarray:
    """PV at t0 (fraction of NAV, NAV held at 1) of the Q4-2026 instalment plus calendar-year draws, mid-year."""
    years = dr["d"].shape[0]
    pv = np.full(dr["d"].shape[1], d2026 / 100 / 4 * (1 + r) ** (-1.5 / 12))
    for k in range(years):
        pv = pv + dr["d"][k] / 100 * (1 + r) ** (-(8.5 + 12 * k) / 12)
    return pv


# ------------------------------------------------------------------------------------------------ curves
def strip_months() -> tuple[np.ndarray, np.ndarray]:
    """Observed strip as (model month index m, price). Contract month M maps to m = months from Nov-2026, so the
    Dec-26 contract is m = 1 (delivery roughly a month out)."""
    ms, ps = [], []
    for key, px in MARKET["strip"].items():
        yy, mm = map(int, key.split("-"))
        ms.append((yy - 2026) * 12 + (mm - 11))
        ps.append(px)
    return np.array(ms), np.array(ps)


def observed_curve_monthly(M: int = 360) -> np.ndarray:
    """Monthly forward curve F_obs(m), m = 0..M: log-linear interpolation of the strip, flat-forward at the last
    quoted point (Dec-2030 $69.16, about the $70 anchor) beyond; m = 0 is set to the front month."""
    ms, ps = strip_months()
    grid = np.arange(M + 1)
    lp = np.interp(grid, np.concatenate([[0], ms]), np.log(np.concatenate([[ps[0]], ps])))
    return np.exp(lp)


def impulse_x(M: int = 360) -> np.ndarray:
    """Response of ln F(m) to a unit shock to the slow factor x (generator impulse response)."""
    return (1.0 - KM) ** np.arange(M + 1)


def annual_avg(F_month: np.ndarray, K: int = 30, start: int = 1) -> np.ndarray:
    """Year-k average price (k = 1..K) from a monthly curve; year 1 = months start..start+11."""
    return np.array([F_month[start + 12 * (k - 1): start + 12 * k].mean() for k in range(1, K + 1)])


# ------------------------------------------------------------------------------------------------ ENR segment values
# G12 stylised segment parameters (research/groups/addenda/G12_calcs/g12_wrongway_sim.py) [I]
PDP = dict(nri=0.80, tax=0.07, loe=14.0, ga=3.0, diff=3.0, decline=0.12, disc=0.10)
ROY = dict(nri=1.0, tax=0.07, decline=0.08, act=0.10, disc=0.085)
MID = dict(act=0.15, mvc=0.60, disc=0.09, capex=0.15)
PLR = 70.0


def pdp_value(Fk: np.ndarray, age: float = 0.0) -> float:
    K = np.arange(1, len(Fk) + 1)
    q = np.exp(-PDP["decline"] * (age + K - 0.5))
    nb = np.maximum(Fk * PDP["nri"] * (1 - PDP["tax"]) - PDP["loe"] - PDP["ga"] - PDP["diff"], 0.0)
    return float((q * nb * (1 + PDP["disc"]) ** -(K - 0.5)).sum())


def roy_value(Fk: np.ndarray) -> float:
    K = np.arange(1, len(Fk) + 1)
    g = -ROY["decline"] + ROY["act"] * (np.log(Fk) - math.log(PLR))
    q = np.exp(np.cumsum(g) - 0.5 * g)
    return float((q * Fk * ROY["nri"] * (1 - ROY["tax"]) * (1 + ROY["disc"]) ** -(K - 0.5)).sum())


def mid_value(Fk: np.ndarray) -> float:
    K = np.arange(1, len(Fk) + 1)
    g = MID["act"] * (np.log(Fk) - math.log(PLR)) * 0.5
    q = np.maximum(np.exp(np.cumsum(g)), MID["mvc"])
    return float((q * (1 - MID["capex"]) * (1 + MID["disc"]) ** -(K - 0.5)).sum())


def segment_elasticities(F_month: np.ndarray, beta_m: np.ndarray, bump: float = 0.01, ltv: float = 0.40) -> dict:
    """Value elasticity of each ENR segment to a +bump shock to the slow factor, the curve moving by beta_m."""
    Fk0 = annual_avg(F_month)
    Fk1 = annual_avg(F_month * np.exp(bump * beta_m))
    out = {}
    for name, f in (("pdp", pdp_value), ("roy", roy_value), ("mid", mid_value)):
        v0, v1 = f(Fk0), f(Fk1)
        out[name] = (v1 / v0 - 1) / bump
    v0, v1 = pdp_value(Fk0), pdp_value(Fk1)
    out["lev"] = ((v1 - ltv * v0) / (v0 - ltv * v0) - 1) / bump
    return out


# ------------------------------------------------------------------------------------------------ options
def b76_put(F, K, sig, T, r=0.0389):
    F, K = np.asarray(F, float), np.asarray(K, float)
    sd = sig * np.sqrt(T)
    d1 = (np.log(F / K) + 0.5 * sd ** 2) / sd
    d2 = d1 - sd
    return math.exp(-r * T) * (K * ndtr(-d2) - F * ndtr(-d1))


def b76_put_delta(F, K, sig, T, r=0.0389):
    sd = sig * np.sqrt(T)
    d1 = (np.log(np.asarray(F, float) / K) + 0.5 * sd ** 2) / sd
    return -math.exp(-r * T) * ndtr(-d1)


def term_vol(T_years: float, short_vol: float = 0.4913, long_vol: float = 0.30, half_life: float = 0.75) -> float:
    """ATM vol for tenor T: 30-day OVX decaying toward a long-dated level (Samuelson effect) [I]."""
    w = 2 ** (-T_years / half_life)
    return long_vol + (short_vol - long_vol) * w
