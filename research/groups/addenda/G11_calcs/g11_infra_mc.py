"""G11 (Real Assets: infrastructure) - Part B: segment Monte Carlo for a SYNTHETIC infra sleeve.

SYNTHETIC - NOT ADIC DATA. Illustrative engine and parameters ([I] unless sourced in the dossier).

Quarterly, 40 quarters, regime-switching macro {N normal, I inflationary late-cycle,
C crisis/demand bust, G Gulf-war supply shock}. Nine infrastructure segments.

Per segment k (equity level):
  NAV (mark-to-model, reduced form, EDHEC-style duration D_k):
    dlnV = (mu_k - y_k - 0.5 s_k^2) dt
           - D_k [ dr + (1 - thetaE_k) dpi_e + lam_k de ]          (discount-rate channel)
           + OL_k * d s_perm                                      (permanent revenue news)
           + dln ECF_ss(coupon)                                    (refinancing/floating channel)
           - (tau_k / D_k) * OL_k * jump_k                         (transitory jump value impact)
           + sig_id sqrt(dt) eps
  Equity cash flow (levered, with DSCR lock-up and refinancing sweeps):
    ECF = DS0 * G_t * [ DSCR0 * exp(OL*s_rev) - kappa_int * c_t/c_0 - (1 - kappa_int) ]
  Appraisal NAV: N_t = lam_app N_{t-1} + (1 - lam_app) V_{t-1}  (one-quarter lag)

Vehicle layer: direct/co-invest, closed-end funds (fees, regime-dependent exits, calls on
unfunded), open-end funds (fees). Outputs: calibration checks, 12-month cash map by starting
state, drawdowns (true vs appraisal), lock-up / refinancing-failure probabilities.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).with_name("g11_infra_mc_results.json")
RNG = np.random.default_rng(20261018)

NPATH = 20000
NQ = 40
DT = 0.25
REG = ["N", "I", "C", "G"]
P = np.array([  # quarterly regime transitions (rows: from)
    [0.92, 0.04, 0.025, 0.015],
    [0.06, 0.86, 0.05, 0.03],
    [0.15, 0.03, 0.80, 0.02],
    [0.08, 0.10, 0.05, 0.77],
])
# regime means
M_R = np.array([0.018, 0.024, 0.008, 0.024])     # 10y real rate
M_PI = np.array([0.023, 0.033, 0.016, 0.038])    # expected inflation
M_G = np.array([0.023, 0.013, -0.030, 0.003])    # real GDP growth
M_P = np.array([0.00, 0.15, -0.30, 0.35])        # log power-price factor
M_E = np.array([0.000, 0.0020, 0.0100, 0.004])   # common infra risk-premium shock (2020: ~+1pp, EDHECinfra attribution)
M_S = np.array([0.000, 0.0025, 0.0200, 0.005])   # credit-spread shock (refinancing)
P_REFI_FAIL = np.array([0.0, 0.01, 0.15, 0.03])  # share of maturing debt that cannot refinance
K_R, S_R = 0.30, 0.006
K_PI, S_PI = 0.60, 0.004
S_G = 0.015
K_P, S_P = 1.20, 0.30
K_E, S_E = 1.00, 0.0025
LAM_APP = 0.85

SEG = ["REG", "CONI", "CONF", "TOLL", "AIR", "MID", "TOW", "DC", "MER"]
W = np.array([0.18, 0.08, 0.14, 0.12, 0.08, 0.10, 0.10, 0.12, 0.08])
Y0 = np.array([0.050, 0.070, 0.080, 0.045, 0.035, 0.080, 0.030, 0.020, 0.080])  # equity cash yield
MU = np.array([0.085, 0.085, 0.085, 0.095, 0.100, 0.095, 0.100, 0.110, 0.100])  # gross total return (N)
D = np.array([9.0, 7.7, 7.4, 8.6, 11.6, 7.7, 10.0, 11.0, 7.7])                 # EDHEC-style duration
THE = np.array([1.3, 1.3, 0.1, 0.9, 0.6, 0.4, 0.0, 0.2, 0.8])                  # thetaE (levered)
LAM = np.array([0.6, 0.5, 0.6, 1.0, 1.4, 1.0, 1.2, 1.6, 1.3])                   # ERP loading
BG = np.array([0.0, 0.0, 0.0, 0.8, 1.8, 0.6, 0.3, 0.5, 0.3])                    # GDP elasticity
MP = np.array([0.0, 0.0, 0.10, 0.0, 0.0, 0.15, 0.0, 0.0, 0.8])                  # power-price share
OL = np.array([1.3, 1.2, 1.2, 1.4, 2.0, 1.5, 1.3, 1.6, 1.5])                    # operating leverage
LEV = np.array([0.65, 0.80, 0.75, 0.60, 0.55, 0.50, 0.55, 0.50, 0.40])
DSCR0 = np.array([1.45, 1.25, 1.35, 1.70, 1.80, 2.50, 2.00, 1.90, 1.80])
LOCK = np.array([1.15, 1.20, 1.20, 1.15, 1.15, 1.15, 1.15, 1.15, 1.20])
H = np.array([0.85, 0.95, 0.90, 0.80, 0.85, 0.90, 0.80, 0.60, 0.80])           # fixed/hedged share
MAT = np.array([9.0, 15.0, 12.0, 7.0, 7.0, 6.0, 6.0, 5.0, 8.0])                 # avg maturity (y)
KINT = np.array([1.0, 0.55, 0.55, 1.0, 1.0, 1.0, 1.0, 1.0, 0.6])                # interest share of DS
SPR = np.array([0.010, 0.012, 0.014, 0.018, 0.018, 0.020, 0.020, 0.022, 0.025])
SIGID = np.array([0.03, 0.03, 0.04, 0.05, 0.06, 0.05, 0.06, 0.08, 0.06])
GPLAN = np.array([0.035, 0.010, 0.000, 0.040, 0.045, 0.020, 0.050, 0.070, 0.010])  # planned nominal CF growth
TAU = np.array([0, 0, 0, 0.5, 1.5, 1.0, 0, 2.5, 0])   # years: transitory-shock persistence (value impact)
GULF_SHARE_AIR = 0.20  # share of airport NAV exposed to Gulf traffic (ADIC to confirm)

# vehicle mix (share of sleeve NAV) and fees
VEH = {"direct_coinvest": 0.35, "closed_end": 0.40, "open_end": 0.25}
FEE = {"direct_coinvest": 0.005, "closed_end": 0.020, "open_end": 0.010}   # all-in annual drag on NAV
# exit window e in {O, N, D, F} (open, normal, drought, frozen) drives closed-end-fund exits
EXIT_RATE = np.array([0.14, 0.10, 0.04, 0.015])     # CEF exit proceeds / CEF NAV per year, by e
EXIT_PX = np.array([1.06, 1.03, 0.98, 0.90])        # exit price / mark, by e
PE_EXIT = np.array([  # quarterly exit-window transitions (stream 04 default, rows O,N,D,F)
    [0.85, 0.12, 0.02, 0.01],
    [0.04, 0.88, 0.06, 0.02],
    [0.03, 0.06, 0.88, 0.03],
    [0.02, 0.08, 0.15, 0.75],
])
EW = ["O", "N", "D", "F"]
CALL_RATE = 0.25 * np.array([1.0, 0.95, 0.90, 1.0])  # calls / unfunded per year
DC_DEV_CALL = np.array([0.06, 0.06, 0.04, 0.05])    # development capex on direct DC NAV per year
SLEEVE_NAV = 7.2   # $bn = 40% of the $18bn Real Assets working allocation [I]
UNFUNDED0 = 1.6    # $bn = 40% of $4bn Real Assets unfunded [I]


def stationary(Pm: np.ndarray) -> np.ndarray:
    w, vecs = np.linalg.eig(Pm.T)
    v = np.real(vecs[:, np.argmin(np.abs(w - 1))])
    return v / v.sum()


PI_STAT = stationary(P)
G_BAR = float(PI_STAT @ M_G)    # unconditional mean real GDP growth: permanent news has zero mean


def simulate(start: int, npath: int = NPATH, nq: int = NQ, seed_shift: int = 0, e_start: int = 1):
    rng = np.random.default_rng(20261018 + 97 * start + 13 * e_start + seed_shift)
    K = len(SEG)
    s = np.full(npath, start)
    ew = np.full(npath, e_start)
    ew_path = np.zeros((npath, nq), dtype=int)
    r = np.full(npath, 0.023)
    pie = np.full(npath, 0.028 if start != 3 else 0.035)
    xp = np.full(npath, M_P[start])
    e = np.full(npath, M_E[start])
    i0 = 0.023 + 0.028 + SPR                      # base coupon per segment
    c_fix = np.tile(i0, (npath, 1))
    ln_v = np.zeros((npath, K))
    app = np.ones((npath, K))
    v_prev = np.ones((npath, K))
    s_perm = np.zeros((npath, K))
    jump = np.zeros((npath, K))
    sweep = np.zeros((npath, K))
    G = np.ones(K)
    DS0 = Y0 / (DSCR0 - 1.0)                       # per unit equity
    ecf_ss_prev = np.tile(DSCR0 - 1.0, (npath, 1))
    out = {k: np.zeros((npath, nq, K)) for k in ("v", "app", "ecf", "dscr")}
    reg_path = np.zeros((npath, nq), dtype=int)
    lock_flag = np.zeros((npath, nq, K), dtype=bool)
    refi_fail = np.zeros((npath, nq, K), dtype=bool)
    hl = {3: 1.0, 4: 3.0, 5: 4.0, 7: 8.0}         # jump half-lives (quarters)
    for t in range(nq):
        # regime transition
        u = rng.random(npath)
        cum = np.cumsum(P[s], axis=1)
        s_new = (u[:, None] > cum).sum(axis=1)
        entered_c = (s_new == 2) & (s != 2)
        entered_g = (s_new == 3) & (s != 3)
        s = s_new
        reg_path[:, t] = s
        # exit window: own Markov chain; entering a macro crisis freezes exits with prob 0.7
        ue = rng.random(npath)
        cume = np.cumsum(PE_EXIT[ew], axis=1)
        ew = (ue[:, None] > cume).sum(axis=1)
        frz = entered_c & (rng.random(npath) < 0.7)
        ew[frz] = 3
        ew_path[:, t] = ew
        # factors
        er, ep, eg, epp, ee = rng.standard_normal((5, npath))
        ee = -0.5 * eg + np.sqrt(1 - 0.25) * ee
        ep = 0.3 * er + np.sqrt(1 - 0.09) * ep
        dr = K_R * (M_R[s] - r) * DT + S_R * np.sqrt(DT) * er
        dpi = K_PI * (M_PI[s] - pie) * DT + S_PI * np.sqrt(DT) * ep
        r = r + dr
        pie = pie + dpi
        g = M_G[s] + S_G * eg
        dxp = K_P * (M_P[s] - xp) * DT + S_P * np.sqrt(DT) * epp
        xp = xp + dxp
        de = K_E * (M_E[s] - e) * DT + S_E * np.sqrt(DT) * ee
        e = e + de
        i_mkt = (r + pie)[:, None] + SPR[None, :] + M_S[s][:, None]
        # jumps (transitory revenue shocks), decaying
        for k_idx, h_q in hl.items():
            jump[:, k_idx] *= 0.5 ** (1.0 / h_q)
        mob = entered_c & (rng.random(npath) < 0.25)
        jump[mob, 4] += -0.55
        jump[mob, 3] += -0.18
        dcb = entered_c & (rng.random(npath) < 0.5)
        jump[dcb, 7] += -0.10
        jump[entered_c, 5] += -0.08
        jump[entered_g, 4] += -0.25 * GULF_SHARE_AIR - 0.03
        # permanent revenue news: GDP surprise (vs unconditional mean) and power price deviation
        ds_perm = BG[None, :] * ((g - G_BAR)[:, None]) * DT
        s_perm += ds_perm
        s_rev = s_perm + jump + MP[None, :] * xp[:, None]
        # debt repricing: floating share each quarter; fixed share rolls at DT/MAT per quarter
        roll = DT / MAT
        fail = (rng.random((npath, len(SEG))) < (P_REFI_FAIL[s][:, None] * np.minimum(1.0, roll * 4)))
        c_fix = c_fix * (1 - roll) + i_mkt * roll
        c = H * c_fix + (1 - H) * i_mkt
        # cash flows
        G = G * (1 + GPLAN * DT)
        cover = DSCR0 * np.exp(OL * s_rev)
        ds_ratio = KINT * c / i0 + (1 - KINT)
        dscr = cover / ds_ratio
        ecf_unit = DS0 * (cover - ds_ratio)               # per unit equity at t0, annual rate
        sweep = np.maximum(sweep - 1, 0)
        sweep[fail] = 4
        refi_fail[:, t, :] = fail
        locked = dscr < LOCK
        lock_flag[:, t, :] = locked
        pay = (~locked) & (sweep == 0)
        ecf = np.where(pay, np.maximum(ecf_unit, 0.0), 0.0) * G * DT
        # NAV dynamics
        ecf_ss = np.maximum(DSCR0 - ds_ratio, 0.02)
        dln_fin = np.log(ecf_ss / ecf_ss_prev)
        ecf_ss_prev = ecf_ss
        # refinancing/floating channel: proportional change in steady-state equity cash flow,
        # half treated as persistent (debt rolls again later at then-market, mean-reverting rates)
        dlnv = ((MU - Y0 - 0.5 * (0.08 ** 2)) * DT
                - D * (dr[:, None] + (1 - THE) * dpi[:, None] + LAM * de[:, None])
                + OL * ds_perm + 0.5 * dln_fin
                + SIGID * np.sqrt(DT) * rng.standard_normal((npath, len(SEG))))
        dlnv += np.where(fail, np.log(0.97), 0.0)       # distress costs on a failed refinancing
        # transitory jump value impact: when a jump arrives its PV loss = tau/D * size (levered by OL)
        new_jump = np.zeros_like(jump)
        new_jump[mob, 4] = -0.55
        new_jump[mob, 3] = -0.18
        new_jump[dcb, 7] = -0.10
        new_jump[entered_c, 5] = -0.08
        new_jump[entered_g, 4] = -0.25 * GULF_SHARE_AIR - 0.03
        dlnv += (TAU / D) * OL * new_jump
        # power price moves have mostly transitory value impact (mean-reverting factor)
        dlnv += MP * (dxp[:, None]) * 0.35
        ln_v += dlnv
        v = np.exp(ln_v)
        app = LAM_APP * app + (1 - LAM_APP) * v_prev
        v_prev = v
        out["v"][:, t, :] = v
        out["app"][:, t, :] = app
        out["ecf"][:, t, :] = ecf
        out["dscr"][:, t, :] = dscr
    out["ew"] = ew_path
    return out, reg_path, lock_flag, refi_fail


def max_drawdown(x: np.ndarray) -> np.ndarray:
    peak = np.maximum.accumulate(x, axis=1)
    return (1 - x / peak).max(axis=1)


def summarize():
    res = {"label": "SYNTHETIC - NOT ADIC DATA", "segments": SEG, "weights": W.tolist(),
           "sleeve_nav_bn": SLEEVE_NAV, "unfunded_bn": UNFUNDED0, "by_start": {}}
    # --- calibration run from N (unconditional-ish) ---
    out, regp, lockf, refif = simulate(0)
    v = out["v"]
    qret = np.diff(np.log(np.concatenate([np.ones((NPATH, 1, len(SEG))), v], axis=1)), axis=1)
    # add cash yield to total return
    tot = qret + out["ecf"] / np.concatenate([np.ones((NPATH, 1, len(SEG))), v[:, :-1, :]], axis=1)
    vol_true = tot.std(axis=1).mean(axis=0) * 2
    app = out["app"]
    aret = np.diff(np.log(np.concatenate([np.ones((NPATH, 1, len(SEG))), app], axis=1)), axis=1)
    vol_app = aret[:, 4:, :].std(axis=1).mean(axis=0) * 2
    mean_tot = tot.mean(axis=(0, 1)) * 4
    cash_y = (out["ecf"] / np.concatenate([np.ones((NPATH, 1, len(SEG))), v[:, :-1, :]], axis=1)).mean(axis=(0, 1)) * 4
    mdd_true = np.stack([max_drawdown(v[:, :, k]) for k in range(len(SEG))], axis=1)
    mdd_app = np.stack([max_drawdown(app[:, :, k]) for k in range(len(SEG))], axis=1)
    p_lock3 = lockf[:, :12, :].any(axis=1).mean(axis=0)
    p_refi5 = refif[:, :20, :].any(axis=1).mean(axis=0)
    calib = []
    for k, name in enumerate(SEG):
        calib.append({"segment": name, "mean_total_return_ann": round(float(mean_tot[k]), 4),
                      "cash_yield_ann": round(float(cash_y[k]), 4),
                      "vol_true_ann": round(float(vol_true[k]), 4), "vol_appraisal_ann": round(float(vol_app[k]), 4),
                      "mdd10y_true_p50": round(float(np.median(mdd_true[:, k])), 4),
                      "mdd10y_true_p95": round(float(np.quantile(mdd_true[:, k], 0.95)), 4),
                      "mdd10y_app_p95": round(float(np.quantile(mdd_app[:, k], 0.95)), 4),
                      "p_lockup_3y": round(float(p_lock3[k]), 4), "p_refi_fail_5y": round(float(p_refi5[k]), 4)})
    res["calibration_from_N"] = calib
    # --- sleeve cash map by starting state (macro regime, exit window) ---
    scen = {"Normal (N macro, N exits)": (0, 1),
            "Drought (N macro, D exits)": (0, 2),
            "Today: Gulf war + drought (G macro, D exits)": (3, 2),
            "Inflationary late-cycle + drought (I, D)": (1, 2),
            "S1-like demand bust (C macro, F exits)": (2, 3)}
    for lab, (st, e0) in scen.items():
        out, regp, lockf, refif = simulate(st, seed_shift=11, e_start=e0)
        v = out["v"]
        ewp = out["ew"]
        nav_k0 = SLEEVE_NAV * W                   # $bn by segment
        ecf_bn = out["ecf"] * nav_k0[None, None, :]
        v_bn = v * nav_k0[None, None, :]
        sleeve_v = v_bn.sum(axis=2)
        sleeve_app = (out["app"] * nav_k0[None, None, :]).sum(axis=2)
        # vehicle layer (applied pro rata across segments)
        fee_drag = sum(VEH[x] * FEE[x] for x in VEH)                       # share of NAV per year
        q_fee = fee_drag * DT * np.concatenate([np.full((NPATH, 1), SLEEVE_NAV), sleeve_v[:, :-1]], axis=1)
        dist_ops = ecf_bn.sum(axis=2) - q_fee
        regs = regp
        cef_nav = VEH["closed_end"] * np.concatenate([np.full((NPATH, 1), SLEEVE_NAV), sleeve_v[:, :-1]], axis=1)
        exits = cef_nav * EXIT_RATE[ewp] * DT * EXIT_PX[ewp]
        unf = np.full(NPATH, UNFUNDED0)
        calls = np.zeros((NPATH, NQ))
        dc_dev = VEH["direct_coinvest"] * v_bn[:, :, 7] * DC_DEV_CALL[regs] * DT
        for t in range(NQ):
            cq = unf * (1 - (1 - CALL_RATE[regs[:, t]]) ** DT)
            calls[:, t] = cq + dc_dev[:, t]
            unf = unf - cq
        dist_total = dist_ops + exits
        net = dist_total - calls
        y1 = lambda a: a[:, :4].sum(axis=1)
        y5 = lambda a: a[:, :20].sum(axis=1)
        sv = np.concatenate([np.full((NPATH, 1), SLEEVE_NAV), sleeve_v], axis=1)
        sa = np.concatenate([np.full((NPATH, 1), SLEEVE_NAV), sleeve_app], axis=1)
        tr_true = np.diff(np.log(sv), axis=1) + ecf_bn.sum(axis=2) / sv[:, :-1]
        tr_app = np.diff(np.log(sa), axis=1) + ecf_bn.sum(axis=2) / sa[:, :-1]
        sleeve_vol_true = float(tr_true.std(axis=1).mean() * 2)
        sleeve_vol_app = float(tr_app[:, 4:].std(axis=1).mean() * 2)
        nav_dd_true = max_drawdown(np.concatenate([np.full((NPATH, 1), SLEEVE_NAV), sleeve_v], axis=1))
        nav_dd_app = max_drawdown(np.concatenate([np.full((NPATH, 1), SLEEVE_NAV), sleeve_app], axis=1))
        q = lambda a, p: round(float(np.quantile(a, p)), 3)
        res["by_start"][lab] = {
            "y1_distributions_bn": {"p10": q(y1(dist_total), .1), "p50": q(y1(dist_total), .5), "p90": q(y1(dist_total), .9), "mean": round(float(y1(dist_total).mean()), 3)},
            "y1_operating_cash_bn_mean": round(float(y1(dist_ops).mean()), 3),
            "y1_exit_proceeds_bn_mean": round(float(y1(exits).mean()), 3),
            "y1_calls_bn_mean": round(float(y1(calls).mean()), 3),
            "y1_net_bn": {"p10": q(y1(net), .1), "p50": q(y1(net), .5), "p90": q(y1(net), .9), "mean": round(float(y1(net).mean()), 3)},
            "y5_cum_net_bn": {"p10": q(y5(net), .1), "p50": q(y5(net), .5), "p90": q(y5(net), .9)},
            "y1_dist_pct_nav_mean": round(float(y1(dist_total).mean() / SLEEVE_NAV), 4),
            "y1_operating_yield_pct_nav_mean": round(float(y1(dist_ops).mean() / SLEEVE_NAV), 4),
            "nav_maxdd_10y_true": {"p50": q(nav_dd_true, .5), "p95": q(nav_dd_true, .95)},
            "nav_maxdd_10y_appraisal": {"p50": q(nav_dd_app, .5), "p95": q(nav_dd_app, .95)},
            "nav_y1_change_true_p05": q(sleeve_v[:, 3] / SLEEVE_NAV - 1, .05),
            "nav_y1_change_app_p05": q(sleeve_app[:, 3] / SLEEVE_NAV - 1, .05),
            "p_any_lockup_y1_by_segment": dict(zip(SEG, [round(float(x), 3) for x in lockf[:, :4, :].any(axis=1).mean(axis=0)])),
            "share_of_paths_in_C_y1": round(float((regs[:, :4] == 2).any(axis=1).mean()), 3),
            "sleeve_vol_true_ann": round(sleeve_vol_true, 4), "sleeve_vol_appraisal_ann": round(sleeve_vol_app, 4),
            "sleeve_mean_total_return_ann_gross": round(float(tr_true.mean() * 4), 4),
        }
    OUT.write_text(json.dumps(res, indent=2))
    print("Calibration (start N, 10y, quarterly; gross of fees):")
    for c in calib:
        print(c)
    print("\nSleeve cash map by start state ($bn):")
    for st, d in res["by_start"].items():
        print(st, json.dumps(d))
    print("wrote", OUT)


if __name__ == "__main__":
    summarize()
