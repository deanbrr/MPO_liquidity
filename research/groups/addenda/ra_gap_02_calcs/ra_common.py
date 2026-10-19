"""
RA gap 02 - shared module: canonical quarterly generator, explicit financing-window state, regime map.

*** SYNTHETIC / ILLUSTRATIVE. Every path, balance and outcome is synthetic. NOT ADIC DATA. ***

What is canonical here (and where it comes from)
  Z_t  oil/fiscal shock type {N,B,SG,DB,SS,GW}: C3 s5.1 annual prior P^Z_a, quarterly principal root
       (ARCHITECTURE s4.1 retires the linearisation I+(P-I)/k), Z0 = gap_04 posterior.
  crisis / S_t: crisis entry p = min(0.95, crisis_entry * KAPPA_CRISIS[Z]); DB entry -> crisis w.p. 0.85;
       persistence 0.90 in DB, 0.75 otherwise (gap_02 t1_engine, imported unmodified by groups gap_04).
       RECV = the 4 quarters after a crisis ends (t1 REBOUND_Q). EXP vs LATE splits the remaining quarters
       with a 2-state sub-chain [I] (the HSMM replaces it); start LATE (CPI 3.7%, 10y 5.10%).
  e_t  exit window {O,N,D,F}: t1 rows (model M1, d_stay 0.88); crisis -> F (or D); e0 = gap_04 filter.
  Factors y (10y), r (short), pi (CPI y/y), g (growth gap), s (Baa-10y spread), oil: [I] means by S with
       Z adjustments (G10 means for continuity); the canonical 20-factor model replaces them.
New here: the FINANCING WINDOW f_t in {N (open), T (tight), C (closed)}, driven by a SLOOS-type lending-
       standards index L_t (net % of banks tightening CRE standards) calibrated on FRED DRTSCREL/SUBLPDRCSN
       1990-2026, with f = N if L < 20, T if 20 <= L < 50, C if L >= 50. L0 = -11.3 (2026Q3 survey) -> f0 = N.
"""
from __future__ import annotations

import csv
import os
from dataclasses import dataclass, field

import numpy as np
from scipy.linalg import fractional_matrix_power

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
LABEL = "SYNTHETIC - NOT ADIC DATA"

# ------------------------------------------------------------------------------------------------ states
EXP, LATE, CRIS, RECV = 0, 1, 2, 3
S_NAMES = ["EXP", "LATE", "CRIS", "RECV"]
Z_NAMES = ["N", "B", "SG", "DB", "SS", "GW"]
ZN, ZB, ZSG, ZDB, ZSS, ZGW = range(6)
E_NAMES = ["O", "N", "D", "F"]
eO, eN, eD, eF = range(4)
F_NAMES = ["N", "T", "C"]
fN, fT, fC = range(3)
G11_NAMES = ["N", "I", "C", "G"]

PZ_A = np.array([[.62, .15, .10, .05, .04, .04],
                 [.40, .40, .05, .06, .07, .02],
                 [.38, .12, .42, .04, .02, .02],
                 [.35, .30, .20, .10, .03, .02],
                 [.30, .05, .10, .35, .15, .05],
                 [.30, .05, .35, .05, .05, .20]])
KAPPA_CRISIS = np.array([1.0, 0.5, 1.5, 4.0, 2.0, 1.5])     # t1_engine [I]
Z0_G4 = np.array([0.03, 0.0, 0.0, 0.02, 0.10, 0.85])          # gap_04 s6.2 (elicited)
E0_G4 = np.array([0.0, 0.08, 0.874, 0.046])                   # gap_04 exit-window filter
M1_CRISIS_ENTRY, M1_D_STAY = 0.020, 0.88                      # t1 MODELS["M1"]
REBOUND_Q = 4


def quarterly_root(Pa: np.ndarray) -> tuple[np.ndarray, dict]:
    """Quarterly chain for the annual prior. The principal 4th root has negative entries (min -0.16): P^Z_a is not
    embeddable at quarterly (or monthly) frequency, so clipping misses P^Z_a by up to 0.16 and the linearisation
    by 0.28. Use the least-squares stochastic 4th root (softmax parameterisation), cached to data/."""
    import json
    from scipy.optimize import minimize
    cache = os.path.join(DATA, "pz_quarterly_lsq.json")
    if os.path.exists(cache):
        d = json.load(open(cache, encoding="utf-8"))
        return np.array(d["PZ_Q"]), d["diag"]
    R = np.real(fractional_matrix_power(Pa, 0.25))
    Lin = np.eye(6) + (Pa - np.eye(6)) / 4

    def unpack(th):
        M = th.reshape(6, 6)
        M = np.exp(M - M.max(1, keepdims=True))
        return M / M.sum(1, keepdims=True)

    def obj(th):
        return float(((np.linalg.matrix_power(unpack(th), 4) - Pa) ** 2).sum())

    th0 = np.log(np.clip(Lin, 1e-6, None)).ravel()
    best = None
    for k in range(6):
        r = minimize(obj, th0 + 0.3 * np.random.default_rng(k).standard_normal(36), method="L-BFGS-B",
                     options={"maxiter": 20000, "maxfun": 200000})
        best = r if best is None or r.fun < best.fun else best
    Pq = unpack(best.x)
    Pc = np.clip(R, 0, None); Pc = Pc / Pc.sum(1, keepdims=True)
    diag = {"principal_root_min_entry": float(R.min()),
            "max_abs_err_lsq": float(np.abs(np.linalg.matrix_power(Pq, 4) - Pa).max()),
            "max_abs_err_clipped_root": float(np.abs(np.linalg.matrix_power(Pc, 4) - Pa).max()),
            "max_abs_err_linearisation": float(np.abs(np.linalg.matrix_power(Lin, 4) - Pa).max())}
    json.dump({"PZ_Q": Pq.tolist(), "diag": diag, "note": "least-squares stochastic 4th root of C3 P^Z_a"},
              open(cache, "w", encoding="utf-8"), indent=1)
    return Pq, diag


PZ_Q, PZ_Q_DIAG = quarterly_root(PZ_A)

# ------------------------------------------------------------------------------------------------ start state
Y0, R0, PI0, S0_BAA, G0_GAP = 5.10, 3.89, 3.74, 1.44, 0.0     # 10y 15-Oct-26; SOFR; CPI Sep y/y; BAA10Y 15-Oct-26
L0_SLOOS = -11.3                                              # SUBLPDRCSN 2026Q3
OIL0 = 105.0                                                  # futures-curve start (gap_04 s6.1 step 6), not spot

# factor means by S (EXP, LATE, CRIS, RECV) - G10 values [I]; Z adjustments [I]
YBAR = np.array([4.25, 5.00, 3.50, 4.00]); YZ = np.array([0.0, 0.10, -0.15, -0.40, 0.30, 0.15])
RBAR = np.array([3.50, 4.25, 1.50, 2.75]); RZ = np.array([0.0, 0.0, 0.0, -0.50, 0.25, 0.10])
PIBAR = np.array([2.5, 3.8, 1.5, 2.3]); PIZ = np.array([0.0, 0.3, -0.6, -1.0, 1.5, 0.8])
GBAR = np.array([0.5, 0.0, -3.0, 1.5]); GZ = np.array([0.0, 0.3, 0.0, -1.0, -0.5, -0.3])
SBAR = np.array([1.55, 1.80, 3.50, 2.20]); SZ = np.array([0.0, 0.0, 0.0, 0.50, 0.25, 0.10])
K_Y, K_R, K_PI, K_G, K_S = 0.15, 0.30, 0.25, 0.40, 0.30
V_Y, V_R, V_PI, V_G, V_S = 0.22, 0.15, 0.35, 0.60, 0.15
# oil (C3 s5.1, quarterly aggregation of the monthly reduced form)
MU_OIL = np.array([0.0, 0.20, -0.35, -0.45, 0.30, 0.10]); SIG_OIL = np.array([0.20, 0.20, 0.20, 0.25, 0.25, 0.30])
KQ_OIL = 1.0 - 0.6 ** 0.25
P_LR = 70.0


# ------------------------------------------------------------------------------------------------ SLOOS calibration
def load_panel():
    rows = []
    with open(os.path.join(DATA, "fred_quarterly_panel.csv"), encoding="utf-8") as fh:
        lines = [ln for ln in fh if not ln.startswith("#")]
    rd = csv.DictReader(lines)
    for r in rd:
        rows.append({k: (float(v) if v not in ("", None) and k != "quarter" else v) for k, v in r.items()})
    return rows


NBER_REC = {"1990Q3", "1990Q4", "1991Q1", "2001Q1", "2001Q2", "2001Q3", "2001Q4",
            "2008Q1", "2008Q2", "2008Q3", "2008Q4", "2009Q1", "2009Q2", "2020Q1", "2020Q2"}


def calibrate_sloos() -> dict:
    """OLS: L_t = c + phi L_{t-1} + b_rec REC_t + b_dy (y_t - y_{t-4})^+ + b_ds (s_t - s_{t-4}) + e.
    Public data (FRED). NBER recession quarters proxy the crisis state."""
    P = [r for r in load_panel() if isinstance(r.get("sloos"), float)]
    idx = {r["quarter"]: i for i, r in enumerate(P)}
    allp = load_panel()
    aidx = {r["quarter"]: i for i, r in enumerate(allp)}
    X, Yv, qs = [], [], []
    for i in range(1, len(P)):
        q = P[i]["quarter"]
        ai = aidx[q]
        if ai < 4:
            continue
        y_now, y_4 = allp[ai].get("y10"), allp[ai - 4].get("y10")
        s_now, s_4 = allp[ai].get("baa10y"), allp[ai - 4].get("baa10y")
        if not all(isinstance(v, float) for v in (y_now, y_4, s_now, s_4)):
            continue
        X.append([1.0, P[i - 1]["sloos"], 1.0 if q in NBER_REC else 0.0, max(0.0, y_now - y_4), s_now - s_4])
        Yv.append(P[i]["sloos"])
        qs.append(q)
    X, Yv = np.array(X), np.array(Yv)
    beta, *_ = np.linalg.lstsq(X, Yv, rcond=None)
    res = Yv - X @ beta
    sig = float(np.sqrt(res @ res / (len(Yv) - X.shape[1])))
    cov = sig ** 2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    Lvals = np.array([r["sloos"] for r in P])
    share = {"N": float((Lvals < 20).mean()), "T": float(((Lvals >= 20) & (Lvals < 50)).mean()),
             "C": float((Lvals >= 50).mean())}
    c_quarters = [r["quarter"] for r in P if r["sloos"] >= 50]
    return {"coef": dict(zip(["c", "phi", "b_rec", "b_dy_pos", "b_ds"], [float(b) for b in beta])),
            "se": dict(zip(["c", "phi", "b_rec", "b_dy_pos", "b_ds"], [float(s) for s in se])),
            "sigma": sig, "n": int(len(Yv)), "sample": [qs[0], qs[-1]], "share_quarters_by_f": share,
            "C_quarters": c_quarters, "note": "public data; spliced DRTSCREL (to 2013Q3) / SUBLPDRCSN (from 2013Q4)"}


SLOOS = calibrate_sloos()
_C = SLOOS["coef"]
F_THRESH = (20.0, 50.0)
L_Z = np.array([0.0, -3.0, 0.0, 5.0, 5.0, 5.0])     # [I] shock-type add-ons (no history for GW)


def f_of_L(L):
    return np.where(L >= F_THRESH[1], fC, np.where(L >= F_THRESH[0], fT, fN))


# ------------------------------------------------------------------------------------------------ regime map
# Every RA parameter set is a function of the canonical (S, e, Z) and the financing window f.
TERMS = {   # G14 lending STANDARDS keyed to f; base yields retired (the rate level comes from y_t / SOFR)
    "ltv_max": np.array([0.625, 0.575, 0.525]),
    "dscr_min": np.array([1.25, 1.35, 1.40]),
    "dy_min": np.array([0.085, 0.095, 0.105]),
    "avail": np.array([0.97, 0.85, 0.60]),
    "spread_add": np.array([0.0, 0.0075, 0.0175]),      # over the N spread (G14 2.00 / 2.75 / 3.75%)
    "p_ext_g10": np.array([0.35, 0.50, 0.50]),          # P(lender extension | gap), G10 values on the f axis
    "sale_disc": np.array([0.03, 0.08, 0.15]),          # G14 forced-sale discount vs economic value
    "ell": np.array([0.01, 0.03, 0.10]),                # ADIC liquidity shadow price at a cure (G14 by regime)
    "liq_cap_add": np.array([0.0, 0.0010, 0.0075]),     # G10 credit-availability cap-rate premium, keyed to f
}
INFRA_ADJ = dict(ltv=0.10, dscr=-0.05, avail=0.05, spread=-0.0025)   # G14 infra_terms
GCC_FLOOR = np.array([fN, fN, fT, fC, fT, fT])     # f^GCC = max(f, floor(Z)); GW -> T (C as sensitivity)
Q_RISK = np.array([0.0, 0.0020, 0.0100, 0.0040])   # G11 infra risk-premium regime means N/I/C/G (C an upper bound)
P_POWER = np.array([0.0, 0.15, -0.30, 0.35])        # G11 power-price means N/I/C/G; SG handled below
G11_PFAIL_RETIRED = np.array([0.0, 0.01, 0.15, 0.03])   # kept only as a diagnostic target


def g11_state(S, z):
    """G11 N/I/C/G from canonical states, precedence C > G > I > N (G11 s6.2 script-regime definitions)."""
    return np.where(S == CRIS, 2, np.where((z == ZGW) | (z == ZSS), 3, np.where(S == LATE, 1, 0)))


def e_re(f, S, y, s):
    """Real-estate transaction window (G10 rule re-keyed): F if f=C; D if f=T or (LATE and 10y>4.75%);
    O if f=N, EXP and Baa spread < 1.6%; else N. The Gulf-war -> D clause now applies to GCC assets only."""
    return np.where(f == fC, eF, np.where((f == fT) | ((S == LATE) & (y > 4.75)), eD,
                                          np.where((f == fN) & (S == EXP) & (s < 1.6), eO, eN)))


def ra12_amber(f, S):
    """RA12 re-keyed: RA sales may be amber in P only while the financing window is N or T and S != CRIS."""
    return (f <= fT) & (S != CRIS)


# ------------------------------------------------------------------------------------------------ scenarios
@dataclass
class Scenario:
    name: str
    desc: str
    force_S: list | None = None          # per quarter t=1..; None = generator
    force_e: list | None = None
    force_z: list | None = None
    y_add: float = 0.0
    s_add: float = 0.0
    pi_add: float = 0.0
    add_q: int = 0                       # quarters over which the adds apply (0 = while forced)
    force_f: list | None = None
    force_eRE: list | None = None
    calls_t4p: bool = False              # Tier-1 convention: closed-end calls at 0.28 x 1.38 a year
    frozen_factors: bool = False         # hold y, r, pi, g, s, oil at the start values (steady-state rows)
    freeze_z: bool = False               # hold Z at its starting draw (steady-state rows)


SCENARIOS = {
    "base_mc": Scenario("base_mc", "Canonical generator (M1) from the October-2026 initial state"),
    "normal": Scenario("normal", "Steady state: LATE, e=N, e^RE=N, f=N, Z and factors frozen at Oct-2026 (G15 'normal')",
                       force_S=[LATE] * 20, force_e=[eN] * 20, force_f=[fN] * 20,
                       force_eRE=[eN] * 20, frozen_factors=True, freeze_z=True),
    "drought": Scenario("drought", "Steady state with exits in drought: e=D, e^RE=D, f=N (G15 'drought')",
                        force_S=[LATE] * 20, force_e=[eD] * 20, force_f=[fN] * 20,
                        force_eRE=[eD] * 20, frozen_factors=True, freeze_z=True),
    "t4p_struct": Scenario("t4p_struct", "Structural T4': crisis q1-q8 (23 crisis months), demand bust q1-q4, "
                           "exits F q1-q4 then D, financing closed q1-q6 and tight q7-q8, Baa +2.0pp (GFC-type), "
                           "calls 0.28 x 1.38",
                           force_S=[CRIS] * 8 + [RECV] * 4 + [EXP] * 8, force_e=[eF] * 4 + [eD] * 8 + [eN] * 8,
                           force_z=[ZDB] * 4 + [ZN] * 16, force_f=[fC] * 6 + [fT] * 2, s_add=2.0, add_q=8,
                           calls_t4p=True),
    "t4p_ratesflat": Scenario("t4p_ratesflat", "Structural T4' without the flight-to-quality rate fall: as t4p_struct "
                              "with 10y +1.5pp against the crisis mean (10y stays near 5%)",
                              force_S=[CRIS] * 8 + [RECV] * 4 + [EXP] * 8, force_e=[eF] * 4 + [eD] * 8 + [eN] * 8,
                              force_z=[ZDB] * 4 + [ZN] * 16, force_f=[fC] * 6 + [fT] * 2, s_add=2.0, y_add=1.5,
                              add_q=8, calls_t4p=True),
    "rate_shock": Scenario("rate_shock", "2022-type: LATE for 8 quarters, 10y +1.0pp, Baa +0.5pp, CPI +1.0pp",
                           force_S=[LATE] * 8, y_add=1.0, s_add=0.5, pi_add=1.0),
    "gulf_persist": Scenario("gulf_persist", "Gulf war persists 8 quarters (Z=GW), macro from the generator",
                             force_z=[ZGW] * 8),
    "sg_glut": Scenario("sg_glut", "Supply glut for 8 quarters (Z=SG), macro from the generator",
                        force_z=[ZSG] * 8),
}


def simulate_states(n: int, T: int, seed: int, sc: Scenario, crisis_entry=M1_CRISIS_ENTRY, d_stay=M1_D_STAY):
    """Quarterly canonical state and factor paths, index 0 = 2026Q4 start, 1..T = quarters ahead."""
    rng = np.random.default_rng(seed)
    sh = (n, T + 1)
    z = np.zeros(sh, int); S = np.zeros(sh, int); e = np.zeros(sh, int); crisis = np.zeros(sh, bool)
    y = np.zeros(sh); r = np.zeros(sh); pi = np.zeros(sh); g = np.zeros(sh); s = np.zeros(sh)
    L = np.zeros(sh); x = np.zeros(sh); late = np.zeros(sh, bool)
    onset = np.zeros(sh, bool); gw_entry = np.zeros(sh, bool); cdur = np.zeros(n, int); since_exit = np.full(n, 99)
    z[:, 0] = rng.choice(6, size=n, p=Z0_G4)
    e[:, 0] = rng.choice(4, size=n, p=E0_G4)
    S[:, 0] = LATE; late[:, 0] = True
    y[:, 0], r[:, 0], pi[:, 0], g[:, 0], s[:, 0], L[:, 0], x[:, 0] = Y0, R0, PI0, G0_GAP, S0_BAA, L0_SLOOS, np.log(OIL0)
    cdfZ = np.cumsum(PZ_Q, axis=1)
    for t in range(T):
        u = rng.random((n, 9)); eps = rng.standard_normal((n, 7))
        # --- Z
        zn = (u[:, 0][:, None] > cdfZ[z[:, t]]).sum(axis=1).clip(0, 5)
        if sc.force_z is not None and t < len(sc.force_z):
            zn = np.full(n, sc.force_z[t])
        if sc.freeze_z:
            zn = z[:, t].copy()
        gw_entry[:, t + 1] = (zn == ZGW) & (z[:, t] != ZGW)
        enter_db = (zn == ZDB) & (z[:, t] != ZDB)
        z[:, t + 1] = zn
        # --- crisis (t1 rule)
        stay = np.where(zn == ZDB, 0.90, 0.75)
        p_enter = np.minimum(0.95, crisis_entry * KAPPA_CRISIS[zn])
        cprev = crisis[:, t]
        cnew = np.where(enter_db, u[:, 1] < 0.85, np.where(cprev, u[:, 1] < stay, u[:, 1] < p_enter))
        if sc.force_S is not None and t < len(sc.force_S):
            cnew = np.full(n, sc.force_S[t] == CRIS)
        onset[:, t + 1] = cnew & ~cprev
        crisis[:, t + 1] = cnew
        cdur = np.where(cnew, cdur + 1, 0)
        since_exit = np.where(cnew, 0, np.where(cprev & ~cnew, 1, since_exit + 1))
        # --- EXP / LATE sub-chain [I]; a crisis resets to EXP afterwards
        lt = late[:, t]
        lt = np.where(lt, u[:, 2] >= 0.06, u[:, 2] < 0.05)
        lt = np.where(cnew, False, lt)
        late[:, t + 1] = lt
        Sn = np.where(cnew, CRIS, np.where((since_exit >= 1) & (since_exit <= REBOUND_Q), RECV,
                                           np.where(lt, LATE, EXP)))
        if sc.force_S is not None and t < len(sc.force_S):
            Sn = np.full(n, sc.force_S[t])
        S[:, t + 1] = Sn
        # --- exit window (t1 rows)
        ue = u[:, 3]
        o_row = np.where(ue < 0.85, 0, np.where(ue < 0.98, 1, 2))
        n_row = np.where(ue < 0.05, 0, np.where(ue < 0.89, 1, 2))
        d_up = 1 - d_stay
        d_row = np.where(ue < 0.1 * d_up, 0, np.where(ue < d_up, 1, 2))
        f_row = np.where(ue < 0.6, 2, 1)
        e_t = e[:, t]
        en = np.where(e_t == 0, o_row, np.where(e_t == 1, n_row, np.where(e_t == 2, d_row, f_row)))
        en = np.where(cnew, np.where((e_t == 3) | (u[:, 4] < 0.8), 3, 2), en)
        if sc.force_e is not None and t < len(sc.force_e):
            en = np.full(n, sc.force_e[t])
        e[:, t + 1] = en
        # --- factors
        inside = (sc.add_q == 0 and sc.force_S is not None and t < len(sc.force_S)) or (t < sc.add_q)
        ya, sa, pa = (sc.y_add, sc.s_add, sc.pi_add) if inside else (0.0, 0.0, 0.0)
        if sc.frozen_factors:
            y[:, t + 1], r[:, t + 1], pi[:, t + 1], g[:, t + 1], s[:, t + 1] = y[:, t], r[:, t], pi[:, t], g[:, t], s[:, t]
        else:
            y[:, t + 1] = y[:, t] + K_Y * (YBAR[Sn] + YZ[zn] + ya - y[:, t]) + V_Y * eps[:, 0]
            r[:, t + 1] = np.maximum(0.0, r[:, t] + K_R * (RBAR[Sn] + RZ[zn] + 0.5 * ya - r[:, t]) + V_R * eps[:, 1])
            pi[:, t + 1] = pi[:, t] + K_PI * (PIBAR[Sn] + PIZ[zn] + pa - pi[:, t]) + V_PI * eps[:, 2]
            g[:, t + 1] = g[:, t] + K_G * (GBAR[Sn] + GZ[zn] - g[:, t]) + V_G * eps[:, 3]
            s[:, t + 1] = np.maximum(0.8, s[:, t] + K_S * (SBAR[Sn] + SZ[zn] + sa - s[:, t]) + V_S * eps[:, 4])
        jump = (zn == ZGW) & (u[:, 5] < 0.25 / 4)
        x[:, t + 1] = (x[:, t] + KQ_OIL * (np.log(P_LR) - x[:, t]) + MU_OIL[zn] / 4 + SIG_OIL[zn] / 2 * eps[:, 5]
                       + jump * np.where(u[:, 6] < 0.5, 0.26, -0.26))
        if sc.frozen_factors:
            x[:, t + 1] = x[:, t]
        # --- financing window: SLOOS-type index (calibrated OLS), state-dependent
        y4 = y[:, max(0, t + 1 - 4)]
        s4 = s[:, max(0, t + 1 - 4)]
        L[:, t + 1] = (_C["c"] + _C["phi"] * L[:, t] + _C["b_rec"] * (Sn == CRIS)
                       + _C["b_dy_pos"] * np.maximum(0.0, y[:, t + 1] - y4) + _C["b_ds"] * (s[:, t + 1] - s4)
                       + L_Z[zn] + SLOOS["sigma"] * eps[:, 6])
        L[:, t + 1] = np.clip(L[:, t + 1], -40.0, 100.0)
    f = f_of_L(L)
    if sc.force_f is not None:
        for t, fv in enumerate(sc.force_f):
            f[:, t + 1] = fv
    out = dict(z=z, S=S, e=e, crisis=crisis, y=y, r=r, pi=pi, g=g, s=s, L=L, f=f, x=x, onset=onset,
               gw_entry=gw_entry, late=late)
    out["eRE"] = e_re(f, S, y, s)
    if sc.force_eRE is not None:
        for t, ev in enumerate(sc.force_eRE):
            out["eRE"][:, t + 1] = ev
    out["g11"] = g11_state(S, z)
    out["fGCC"] = np.maximum(f, GCC_FLOOR[z])
    out["amber"] = ra12_amber(f, S)
    return out


def regime_table() -> list[dict]:
    """The mapping table, rows = canonical conditions, for the addendum (also printed by ra_engine)."""
    return [
        {"RA parameter set": "G14 lending standards (LTV/DSCR/DY/availability/spread add-on)",
         "key": "f_t (N/T/C) from L_t", "values": {k: TERMS[k].tolist() for k in
                                                     ("ltv_max", "dscr_min", "dy_min", "avail", "spread_add")},
         "retired": "G14 N/T/C base yields (rate level now y_t / SOFR); GW and OD regimes -> GCC floor on f"},
        {"RA parameter set": "Infrastructure terms", "key": "f_t", "values": INFRA_ADJ,
         "retired": "G11 credit-spread regime means (0/25/200/50bp)"},
        {"RA parameter set": "GCC lending", "key": "max(f_t, floor(Z_t)), floor N/N/T/C/T/T",
         "values": GCC_FLOOR.tolist(), "retired": "G14 GW/OD term sets; G15 'GCC lenders normal in GW'"},
        {"RA parameter set": "G11 regime N/I/C/G", "key": "C if S=CRIS; G if Z in {GW,SS}; I if S=LATE; else N",
         "values": {"q_risk_premium": Q_RISK.tolist(), "power_price": P_POWER.tolist()},
         "retired": "G11 4x4 transition matrix; G11 real-rate/inflation/GDP means (now canonical factors); "
                    "p^fail 0/1/15/3% (now the s4.5 module; kept as a diagnostic)"},
        {"RA parameter set": "e^RE (RE transaction window)", "key": "F if f=C; D if f=T or (LATE and 10y>4.75%); "
         "O if f=N, EXP, Baa<1.6%; else N", "values": None,
         "retired": "G10 private S chain (PS) and its Z in {N,GW,DB}; GW->D for non-GCC assets"},
        {"RA parameter set": "G10 credit-availability cap-rate premium", "key": "f_t",
         "values": TERMS["liq_cap_add"].tolist(), "retired": "keyed to S (0/10/75/25bp)"},
        {"RA parameter set": "Extension probability (axis)", "key": "f_t", "values": TERMS["p_ext_g10"].tolist(),
         "retired": "G14 0.55-0.70"},
        {"RA parameter set": "RA12 sales tier", "key": "amber iff f in {N,T} and S != CRIS; red under T4'",
         "values": None, "retired": "'N or T' of an unmapped regime"},
        {"RA parameter set": "ENR RBL", "key": "oil curve x_t, Z_t", "values": {"advance": 0.60, "deck": 0.85,
         "advance_cut_SG_DB": 0.10, "redetermination": "semiannual + interim on |dln P| >= 0.20"},
         "retired": "G14 energy_terms regime remap"},
    ]


if __name__ == "__main__":
    import json
    print(json.dumps(SLOOS, indent=1))
    print("PZ_Q rows sum", PZ_Q.sum(axis=1).round(6).tolist())
    print("PZ_Q^4 vs PZ_A max abs diff", float(np.abs(np.linalg.matrix_power(PZ_Q, 4) - PZ_A).max()))
    st = simulate_states(4000, 20, 7, SCENARIOS["base_mc"])
    for t in (0, 1, 4, 8, 12, 20):
        print(t, "f share", np.bincount(st["f"][:, t], minlength=3) / 4000, "crisis", st["crisis"][:, t].mean().round(3),
              "S", np.bincount(st["S"][:, t], minlength=4) / 4000, "eRE", np.bincount(st["eRE"][:, t], minlength=4) / 4000)
