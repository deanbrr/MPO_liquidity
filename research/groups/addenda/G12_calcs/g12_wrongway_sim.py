"""G12 wrong-way-risk simulation: owner draw vs oil-linked real-asset segments.

ALL OUTPUTS ARE SYNTHETIC [I-MC]. Not ADIC data, not forecasts.

Re-uses stream-03 defaults (dossier 03 sections 6.3-6.6) for the annual oil / shock-type /
owner-draw model, and adds stylised per-$1 segment cash-flow models:
  upstream PDP (unlevered and RBL-levered), oil-weighted mineral & royalty interests,
  fee-based midstream with volume linkage, timberland with harvest deferral, row-crop farmland.

Outputs (JSON):
  - liability oil delta: P(draw rate strictly inside the band), dd/dlnP, $ per $1/bbl
  - segment value elasticities to a spot oil shock (barrel-equivalent deltas per $1bn)
  - owner beta  beta_own = Cov(r_j, d)/Var(d)
  - owner-weighted return haircut H_j = -Cov(m_own, r_j)/E[m_own]  (dossier 03 sec 6.9 weight)
  - conditional mean return and distribution yield by shock type Z
  - RBL equity-cure calls (REFINANCE capacity wrong-way) by Z
  - today's-state conditional 2-year expected returns

Usage: python -I g12_wrongway_sim.py <out_json>
"""
from __future__ import annotations

import json
import sys

import numpy as np

STATES = ["N", "B", "SG", "DB", "SS", "GW"]
ZI = {z: i for i, z in enumerate(STATES)}
# Stream-03 annual transition prior (Table 6.3); rows = current state
PZ = np.array([
    [0.62, 0.15, 0.10, 0.05, 0.04, 0.04],
    [0.40, 0.40, 0.05, 0.06, 0.07, 0.02],
    [0.38, 0.12, 0.42, 0.04, 0.02, 0.02],
    [0.35, 0.30, 0.20, 0.10, 0.03, 0.02],
    [0.30, 0.05, 0.10, 0.35, 0.15, 0.05],
    [0.30, 0.05, 0.35, 0.05, 0.05, 0.20],
])
PZ = PZ / PZ.sum(axis=1, keepdims=True)
MU_O = np.array([0.0, 0.20, -0.35, -0.45, 0.30, 0.10])
SIG_O = np.array([0.20, 0.20, 0.20, 0.25, 0.25, 0.30])
RHO_EQ = np.array([0.0, 0.2, 0.1, 0.6, -0.4, -0.5])
MU_EQ = np.array([0.07, 0.15, 0.05, -0.25, -0.10, -0.05])
SIG_EQ = np.array([0.15, 0.14, 0.16, 0.25, 0.22, 0.20])
W_Z = np.array([0.0, 0.0, -0.5, -1.5, -0.5, -6.0])  # fiscal wedge, pp of GDP
KAPPA, PLR = 0.40, 70.0
PHI = 1.0 - KAPPA
K_HORIZON = 30


def stationary(P):
    w, v = np.linalg.eig(P.T)
    s = np.real(v[:, np.argmin(np.abs(w - 1))])
    return s / s.sum()


def expected_log_path_offsets():
    """A[z, k-1] = sum_{i=1..k} phi^{k-i} (P^i mu)_z, k = 1..K."""
    A = np.zeros((6, K_HORIZON))
    Pi = np.eye(6)
    pm = []
    for i in range(1, K_HORIZON + 1):
        Pi = Pi @ PZ
        pm.append(Pi @ MU_O)
    pm = np.array(pm)  # (K, 6)
    for k in range(1, K_HORIZON + 1):
        acc = np.zeros(6)
        for i in range(1, k + 1):
            acc += PHI ** (k - i) * pm[i - 1]
        A[:, k - 1] = acc
    return A


A_OFF = expected_log_path_offsets()
KS = np.arange(1, K_HORIZON + 1)


def fwd_curve(x, z):
    """Median expected price path F_k (k = 1..K) for arrays x (log price) and z (state index)."""
    xb = np.log(PLR)
    m = xb + (PHI ** KS)[None, :] * (x[:, None] - xb) + A_OFF[z, :]
    return np.exp(m)


# ---------------- segment parameters (SYNTHETIC defaults) ----------------
PDP = dict(nri=0.80, tax=0.07, loe=14.0, ga=3.0, diff=3.0, decline=0.12, disc=0.10)
ROY = dict(nri=1.0, tax=0.07, decline=0.08, act=0.10, disc=0.085)
MID = dict(decline=0.0, act=0.15, mvc=0.60, disc=0.09, capex=0.15)
RBL = dict(adv=0.60, deck=0.85, rate=0.075, ltv0=0.40)


def pdp_value(x, z, age):
    """PV of remaining PDP cash flows per unit of initial annual production, from year age onward."""
    F = fwd_curve(x, z)
    q = np.exp(-PDP["decline"] * (age[:, None] + KS[None, :] - 0.5))
    nb = np.maximum(F * PDP["nri"] * (1 - PDP["tax"]) - PDP["loe"] - PDP["ga"] - PDP["diff"], 0.0)
    disc = (1 + PDP["disc"]) ** -(KS - 0.5)
    return (q * nb * disc[None, :]).sum(axis=1)


def pdp_cash(P, age):
    q = np.exp(-PDP["decline"] * (age - 0.5))
    nb = np.maximum(P * PDP["nri"] * (1 - PDP["tax"]) - PDP["loe"] - PDP["ga"] - PDP["diff"], 0.0)
    return q * nb


def roy_value(x, z, vol):
    F = fwd_curve(x, z)
    # expected volume path: decline plus activity response to expected price gap
    gap = np.log(F) - np.log(PLR)
    g = -ROY["decline"] + ROY["act"] * gap
    q = vol[:, None] * np.exp(np.cumsum(g, axis=1) - 0.5 * g)
    disc = (1 + ROY["disc"]) ** -(KS - 0.5)
    return (q * F * ROY["nri"] * (1 - ROY["tax"]) * disc[None, :]).sum(axis=1)


def mid_value(x, z, vol):
    F = fwd_curve(x, z)
    gap = np.log(F) - np.log(PLR)
    g = MID["act"] * gap * 0.5
    q = vol[:, None] * np.exp(np.cumsum(g, axis=1))
    q = np.maximum(q, MID["mvc"])
    disc = (1 + MID["disc"]) ** -(KS - 0.5)
    return (q * (1 - MID["capex"]) * disc[None, :]).sum(axis=1)


def simulate(n, T, seed, z0_probs, p0, PBE, h0=0.113, h_end=0.091, b=0.625, c=0.075, rho_d=0.5,
             d0=0.06, form="log", Pref=62.2, gw_jump=True, kappa_own=(0.5, 1.0, 2.0)):
    rng = np.random.default_rng(seed)
    z = rng.choice(6, size=n, p=z0_probs)
    x = np.full(n, np.log(p0))
    d_prev = np.full(n, d0)
    # timber / farm latent states
    s_t = np.zeros(n)  # log stumpage deviation
    inv = np.ones(n)
    c_f = np.zeros(n)  # log crop-revenue deviation
    rent_hist = [np.ones(n), np.ones(n), np.ones(n)]
    # segment initial values
    age = np.zeros(n)
    V_pdp = pdp_value(x, z, age)
    vol_r = np.ones(n)
    V_roy = roy_value(x, z, vol_r)
    vol_m = np.ones(n)
    V_mid = mid_value(x, z, vol_m)
    # levered PDP: debt at ltv0 of value
    D_debt = RBL["ltv0"] * V_pdp
    E_lev = V_pdp - D_debt
    land = 0.35
    S_bar = 1.0
    V_tim = land + 0.65 * inv * np.exp(0.3 * s_t)
    V_farm = np.ones(n)
    # hedged PDP: 3-year rolling swap ladder on 70% of revenue volume, locked at the model forward
    HR = 0.70
    F0 = fwd_curve(x, z)
    H_lock = F0[:, :3].copy()  # locked prices for years t+1, t+2, t+3
    nf = PDP["nri"] * (1 - PDP["tax"])

    def hedge_mtm(xx, zz, ag, Hl):
        F = fwd_curve(xx, zz)[:, :3]
        q = np.exp(-PDP["decline"] * (ag[:, None] + np.arange(1, 4)[None, :] - 0.5))
        disc = (1 + PDP["disc"]) ** -(np.arange(1, 4) - 0.5)
        return (HR * q * nf * (Hl - F) * disc[None, :]).sum(axis=1)

    MTM = hedge_mtm(x, z, age, H_lock)
    V_hdg = V_pdp + MTM
    out = {k: [] for k in ["z", "P", "d", "FB", "req", "r_pdp", "y_pdp", "r_lev", "y_lev", "cure",
                           "r_roy", "y_roy", "r_mid", "y_mid", "r_tim", "y_tim", "r_farm", "y_farm", "inband",
                           "r_hdg", "y_hdg", "vm_hdg", "c_pdp", "c_lev", "c_roy", "c_mid", "c_tim", "c_farm", "c_hdg"]}
    for t in range(1, T + 1):
        h_t = h0 + (h_end - h0) * min(t, 4) / 4.0
        z_new = np.array([rng.choice(6, p=PZ[zz]) for zz in z]) if n <= 2000 else _vec_trans(rng, z)
        eps_o = rng.standard_normal(n)
        eps_e = rng.standard_normal(n)
        jump = np.where((z_new == ZI["GW"]) & (rng.random(n) < 0.25) & gw_jump,
                        np.where(rng.random(n) < 0.5, np.log(1.3), np.log(0.7)), 0.0)
        x_new = x + KAPPA * (np.log(PLR) - x) + MU_O[z_new] + SIG_O[z_new] * eps_o + jump
        P = np.exp(x_new)
        req = MU_EQ[z_new] + SIG_EQ[z_new] * (RHO_EQ[z_new] * eps_o + np.sqrt(1 - RHO_EQ[z_new] ** 2) * eps_e)
        # owner fiscal balance and draw
        if form == "log":
            FB = 100 * h_t * np.log(P / PBE)
        else:
            FB = 100 * h_t * (P - PBE) / Pref
        FB = FB + W_Z[z_new] + rng.standard_normal(n) * 1.0
        d_star = np.clip(c - b * FB / 100.0, 0.05, 0.10)
        d = np.clip(rho_d * d_prev + (1 - rho_d) * d_star, 0.05, 0.10)
        inband = (d_star > 0.05 + 1e-9) & (d_star < 0.10 - 1e-9)
        # --- upstream PDP (unlevered)
        cash_pdp = pdp_cash(P, age + 1)
        age = age + 1
        V_pdp_new = pdp_value(x_new, z_new, age)
        r_pdp = (V_pdp_new + cash_pdp) / np.maximum(V_pdp, 1e-9) - 1
        y_pdp = cash_pdp / np.maximum(V_pdp, 1e-9)
        # --- levered PDP with RBL redetermination (annualised)
        interest = RBL["rate"] * D_debt
        bb = RBL["adv"] * RBL["deck"] * V_pdp_new  # borrowing base on deck-discounted PV
        over = np.maximum(D_debt - bb, 0.0)
        cash_after_int = cash_pdp - interest
        cure_from_cash = np.minimum(np.maximum(cash_after_int, 0.0), over)
        cure_call = over - cure_from_cash  # equity injection required (cash call on ADIC)
        dist_lev = np.maximum(cash_after_int - cure_from_cash, 0.0)
        shortfall = np.maximum(-cash_after_int, 0.0)
        cure_call = cure_call + shortfall
        D_new = D_debt - over
        E_new = np.maximum(V_pdp_new - D_new, 0.0)
        r_lev = (E_new + dist_lev - cure_call) / np.maximum(E_lev, 1e-9) - 1
        y_lev = (dist_lev - cure_call) / np.maximum(E_lev, 1e-9)
        cure = cure_call / np.maximum(E_lev, 1e-9)
        D_debt, E_lev = D_new, E_new
        # --- royalty
        cash_roy = vol_r * P * ROY["nri"] * (1 - ROY["tax"])
        vol_r = vol_r * np.exp(-ROY["decline"] + ROY["act"] * (x_new - np.log(PLR)))
        V_roy_new = roy_value(x_new, z_new, vol_r)
        r_roy = (V_roy_new + cash_roy) / np.maximum(V_roy, 1e-9) - 1
        y_roy = cash_roy / np.maximum(V_roy, 1e-9)
        # --- midstream (fee-based, volume-linked, MVC floor)
        vol_m = np.maximum(vol_m * np.exp(MID["act"] * (x_new - np.log(PLR)) * 0.5), MID["mvc"])
        cash_mid = vol_m * (1 - MID["capex"])
        V_mid_new = mid_value(x_new, z_new, vol_m)
        r_mid = (V_mid_new + cash_mid) / np.maximum(V_mid, 1e-9) - 1
        y_mid = cash_mid / np.maximum(V_mid, 1e-9)
        # --- timberland: stumpage log-OU (0.3 reversion, 15% vol, corr 0.3 with equity, 0 with oil)
        e_s = 0.3 * eps_e + np.sqrt(1 - 0.09) * rng.standard_normal(n)
        s_t = s_t - 0.3 * s_t + 0.15 * e_s
        S = S_bar * np.exp(s_t)
        harv = np.where(S < 0.9, 0.025, np.where(S > 1.1, 0.07, 0.05))  # harvest deferral / acceleration
        cash_tim = 0.65 * harv * inv * S * 0.85  # stumpage net of management and property tax
        inv = inv * (1.05 - harv)  # ~5% biological growth
        land = land * 1.025
        V_tim_new = land + 0.65 * inv * S_bar * np.exp(0.3 * s_t)
        r_tim = (V_tim_new + cash_tim) / np.maximum(V_tim, 1e-9) - 1
        y_tim = cash_tim / np.maximum(V_tim, 1e-9)
        # --- farmland: crop revenue log-OU (0.4 reversion, 15% vol, corr 0.25 oil, 0.1 equity)
        e_c = 0.25 * eps_o + 0.10 * eps_e + np.sqrt(1 - 0.0625 - 0.01) * rng.standard_normal(n)
        c_f = c_f - 0.4 * c_f + 0.15 * e_c
        rent_hist = rent_hist[1:] + [np.exp(c_f)]
        rent = np.mean(rent_hist, axis=0)  # 3-year lagged reset
        cash_farm = 0.03 * rent * 1.02 ** t
        V_farm_new = rent * 1.02 ** t  # capitalised at constant 3% cap rate
        r_farm = (V_farm_new + cash_farm) / np.maximum(V_farm, 1e-9) - 1
        y_farm = cash_farm / np.maximum(V_farm, 1e-9)
        # --- hedged PDP (asset-level settlement; overlay route adds collateral flow = change in MTM)
        q_now = np.exp(-PDP["decline"] * (age - 0.5))  # age already incremented
        settle = HR * q_now * nf * (H_lock[:, 0] - P)
        F_new = fwd_curve(x_new, z_new)
        H_lock = np.column_stack([H_lock[:, 1], H_lock[:, 2], F_new[:, 2]])
        MTM_new = hedge_mtm(x_new, z_new, age, H_lock)
        cash_hdg = cash_pdp + settle
        V_hdg_new = V_pdp_new + MTM_new
        r_hdg = (V_hdg_new + cash_hdg) / np.maximum(V_hdg, 1e-9) - 1
        y_hdg = cash_hdg / np.maximum(V_hdg, 1e-9)
        vm_hdg = (MTM_new - MTM) / np.maximum(V_hdg, 1e-9)  # >0: collateral received via overlay route
        # store
        for k, v in [("z", z_new), ("P", P), ("d", d), ("FB", FB), ("req", req), ("r_pdp", r_pdp),
                     ("y_pdp", y_pdp), ("r_lev", r_lev), ("y_lev", y_lev), ("cure", cure), ("r_roy", r_roy),
                     ("y_roy", y_roy), ("r_mid", r_mid), ("y_mid", y_mid), ("r_tim", r_tim), ("y_tim", y_tim),
                     ("r_farm", r_farm), ("y_farm", y_farm), ("inband", inband), ("r_hdg", r_hdg),
                     ("y_hdg", y_hdg), ("vm_hdg", vm_hdg), ("c_pdp", cash_pdp), ("c_lev", dist_lev - cure_call),
                     ("c_roy", cash_roy), ("c_mid", cash_mid), ("c_tim", cash_tim), ("c_farm", cash_farm),
                     ("c_hdg", cash_hdg)]:
            out[k].append(np.asarray(v).copy())
        # roll
        x, z, d_prev = x_new, z_new, d
        V_pdp, V_roy, V_mid, V_tim, V_farm = V_pdp_new, V_roy_new, V_mid_new, V_tim_new, V_farm_new
        V_hdg, MTM = V_hdg_new, MTM_new
    return {k: np.array(v) for k, v in out.items()}  # shape (T, n)


def _vec_trans(rng, z):
    u = rng.random(len(z))
    cdf = np.cumsum(PZ, axis=1)[z]
    return (u[:, None] > cdf).sum(axis=1).clip(0, 5)


SEGS = [("pdp", "Upstream PDP, unlevered"), ("lev", "Upstream PDP, 40% LTV RBL"),
        ("hdg", "Upstream PDP, 70% 3-yr swap ladder"), ("roy", "Oil mineral & royalty"),
        ("mid", "Fee-based midstream"), ("tim", "Timberland"), ("farm", "Row-crop farmland"), ("eq", "Global equity (ref)")]


def analyse(sim, burn=1, kappa_own=(0.5, 1.0, 2.0), kappa_d=(0.25, 0.5, 1.0)):
    sl = slice(burn, None)
    d = sim["d"][sl].ravel()
    FB = sim["FB"][sl].ravel()
    z = sim["z"][sl].ravel()
    lnP = np.log(sim["P"][sl].ravel())
    res = {}
    sigFB = FB.std()
    zz_t = sim["z"][sl]
    for key, name in SEGS:
        r = (sim["req"] if key == "eq" else sim[f"r_{key}"])[sl].ravel()
        y = None if key == "eq" else sim[f"y_{key}"][sl].ravel()
        r = np.clip(r, -0.99, 5.0)
        row = {"name": name,
               "mean_ret": round(float(r.mean()), 4), "vol": round(float(r.std()), 4),
               "beta_own": round(float(np.cov(r, d)[0, 1] / d.var()), 3),
               "corr_draw": round(float(np.corrcoef(r, d)[0, 1]), 3),
               "corr_dlnP": None}
        for ko in kappa_own:
            m = 1 + ko * np.maximum(2.0 - FB, 0.0) / sigFB
            row[f"H_kappa{ko}"] = round(float(-np.cov(m, r)[0, 1] / m.mean()), 4)
        for kd in kappa_d:  # draw-utilisation weight: 1 at the 5% floor, 1+kd at the 10% cap
            m = 1 + kd * (d - 0.05) / 0.05
            row[f"Hd_kappa{kd}"] = round(float(-np.cov(m, r)[0, 1] / m.mean()), 4)
        if key != "eq":
            # distributions by state relative to the N-state mean at the same date (removes depletion drift)
            cash = sim[f"c_{key}"][sl]
            ratios = {}
            for zz in STATES:
                vals = []
                for t in range(cash.shape[0]):
                    selN = zz_t[t] == ZI["N"]
                    selZ = zz_t[t] == ZI[zz]
                    if selN.sum() > 200 and selZ.sum() > 50:
                        base = cash[t][selN].mean()
                        if abs(base) > 1e-12:
                            vals.append(cash[t][selZ].mean() / base)
                if vals:
                    ratios[zz] = round(float(np.mean(vals)), 3)
            row["cash_vs_N"] = ratios
        if y is not None:
            y = np.clip(y, -2, 2)
            row["mean_yield"] = round(float(y.mean()), 4)
            row["corr_yield_draw"] = round(float(np.corrcoef(y, d)[0, 1]), 3)
        byz = {}
        for zz in STATES:
            sel = z == ZI[zz]
            if sel.sum() > 100:
                byz[zz] = {"ret": round(float(r[sel].mean()), 4), "share": round(float(sel.mean()), 4)}
                if y is not None:
                    byz[zz]["yield"] = round(float(y[sel].mean()), 4)
        row["by_Z"] = byz
        res[key] = row
    # oil-return correlation (annual log change)
    dl = np.diff(np.log(sim["P"]), axis=0)[burn - 1:].ravel() if burn >= 1 else None
    if dl is not None and len(dl) == len(d):
        for key, _ in SEGS:
            r = (sim["req"] if key == "eq" else sim[f"r_{key}"])[sl].ravel()
            res[key]["corr_dlnP"] = round(float(np.corrcoef(np.clip(r, -0.99, 5), dl)[0, 1]), 3)
    vm = sim["vm_hdg"][sl].ravel()
    res["hdg"]["overlay_route_collateral_flow_by_Z"] = {zz: round(float(vm[z == ZI[zz]].mean()), 4) for zz in STATES}
    res["hdg"]["overlay_route_collateral_P05_by_Z"] = {zz: round(float(np.percentile(vm[z == ZI[zz]], 5)), 4)
                                                      for zz in STATES}
    cure = sim["cure"][sl].ravel()
    res["lev"]["cure_call_prob_by_Z"] = {zz: round(float((cure[z == ZI[zz]] > 1e-6).mean()), 4) for zz in STATES}
    res["lev"]["cure_call_mean_if_any_by_Z"] = {
        zz: round(float(cure[(z == ZI[zz]) & (cure > 1e-6)].mean()), 4) if ((z == ZI[zz]) & (cure > 1e-6)).sum() > 50 else None
        for zz in STATES}
    draw = {"mean_draw": round(float(d.mean()), 4), "p_inband_dstar": round(float(sim["inband"][sl].mean()), 4),
            "draw_by_Z": {zz: round(float(d[z == ZI[zz]].mean()), 4) for zz in STATES},
            "sigma_FB_pp": round(float(sigFB), 3),
            "median_brent": round(float(np.exp(np.median(lnP))), 1)}
    return res, draw


def elasticities(p0, z0):
    """Value elasticity to a +1% spot shock, holding state; and barrel-equivalent delta per $1bn."""
    x = np.array([np.log(p0)])
    z = np.array([ZI[z0]])
    age = np.zeros(1)
    out = {}
    for name, f in [("pdp", lambda xx: pdp_value(xx, z, age)), ("roy", lambda xx: roy_value(xx, z, np.ones(1))),
                    ("mid", lambda xx: mid_value(xx, z, np.ones(1)))]:
        v0, v1 = f(x)[0], f(x + 0.01)[0]
        el = (v1 / v0 - 1) / 0.01
        out[name] = {"elasticity_to_spot": round(float(el), 3),
                     "bbl_equiv_per_usd1bn_mm": round(float(el * 1000 / p0), 2)}
    # levered equity at 40% LTV
    v0 = pdp_value(x, z, age)[0]
    v1 = pdp_value(x + 0.01, z, age)[0]
    e0 = v0 * (1 - RBL["ltv0"])
    e1 = v1 - v0 * RBL["ltv0"]
    el = (e1 / e0 - 1) / 0.01
    out["lev"] = {"elasticity_to_spot": round(float(el), 3), "bbl_equiv_per_usd1bn_mm": round(float(el * 1000 / p0), 2)}
    # hedged: 70% of years 1-3 revenue volume swapped at the current forward (MTM = 0 at inception)
    nf = PDP["nri"] * (1 - PDP["tax"])
    q = np.exp(-PDP["decline"] * (np.arange(1, 4) - 0.5))
    disc = (1 + PDP["disc"]) ** -(np.arange(1, 4) - 0.5)
    F0 = fwd_curve(x, z)[0, :3]
    F1 = fwd_curve(x + 0.01, z)[0, :3]
    dmtm = -(0.70 * q * nf * (F1 - F0) * disc).sum()
    el_h = ((v1 + dmtm) / v0 - 1) / 0.01
    out["hdg"] = {"elasticity_to_spot": round(float(el_h), 3), "bbl_equiv_per_usd1bn_mm": round(float(el_h * 1000 / p0), 2),
                  "share_of_unhedged_elasticity_removed": round(float(1 - el_h / out["pdp"]["elasticity_to_spot"]), 3)}
    return out


def main():
    out_path = sys.argv[1]
    pi = stationary(PZ)
    res = {"label": "SYNTHETIC [I-MC] - stylised segment models on stream-03 oil/draw defaults; not ADIC data",
           "stationary_Z": {s: round(float(p), 4) for s, p in zip(STATES, pi)}, "runs": {}}
    n, T = 40000, 12
    for PBE in [44.8, 55.0, 65.0]:
        for form in ["log", "linear"]:
            sim = simulate(n, T, seed=12 + int(PBE), z0_probs=pi, p0=PLR, PBE=PBE, form=form)
            seg, draw = analyse(sim, burn=2)
            res["runs"][f"stationary_PBE{PBE}_{form}"] = {"segments": seg, "draw": draw}
    # hydrocarbon share sensitivity (owner's oil dependence), PBE 55, log form
    for h in [0.06, 0.091, 0.113, 0.15]:
        sim = simulate(n, T, seed=99, z0_probs=pi, p0=PLR, PBE=55.0, h0=h, h_end=h)
        seg, draw = analyse(sim, burn=2)
        res["runs"][f"stationary_PBE55_h{h}"] = {"segments": {k: {kk: v[kk] for kk in ["beta_own", "H_kappa1.0", "Hd_kappa0.5", "corr_draw"]}
                                                             for k, v in seg.items()}, "draw": draw}
    # today's state: GW 0.85 / N 0.15, 1-year-forward Brent ~ $95 (between spot 126.55 and EIA 2027 avg 84)
    z0 = np.zeros(6)
    z0[ZI["GW"]], z0[ZI["N"]] = 0.85, 0.15
    sim = simulate(n, 3, seed=7, z0_probs=z0, p0=95.0, PBE=55.0)
    today = {}
    for key, _ in SEGS:
        r = sim["req"] if key == "eq" else sim[f"r_{key}"]
        cum2 = np.prod(1 + np.clip(r[:2], -0.99, 5), axis=0) - 1
        today[key] = {"E_2y_cum": round(float(cum2.mean()), 4), "P10_2y": round(float(np.percentile(cum2, 10)), 4)}
    today["z_share_year2"] = {s: round(float((sim["z"][1] == ZI[s]).mean()), 3) for s in STATES}
    today["brent_median_y1_y2_y3"] = [round(float(np.median(sim["P"][i])), 1) for i in range(3)]
    res["today_GW_start"] = today
    res["elasticities"] = {"N_at_70": elasticities(70.0, "N"), "GW_at_95": elasticities(95.0, "GW"),
                           "SG_at_55": elasticities(55.0, "SG")}
    # liability delta (log form): dd/dlnP = -b*100h/100 of NAV when d* in band
    nav = 177.0
    liab = {}
    for h in [0.113, 0.091]:
        dd = 0.625 * 100 * h / 100.0  # fraction of NAV per unit log price
        liab[f"h{h}"] = {"dd_dlnP_pct_nav": round(dd * 100, 2),
                         "usd_bn_per_1usd_bbl_at_50": round(dd * nav / 50.0, 3),
                         "usd_bn_per_1usd_bbl_at_64": round(dd * nav / 64.0, 3)}
    liab["linear_map_usd_bn_per_1usd_bbl"] = round(0.00625 * 11.3 / 62.2 * nav, 3)
    res["liability_delta"] = liab
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
