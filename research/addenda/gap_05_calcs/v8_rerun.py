"""Gap 05: re-run of deck v8's 3-year oil shock -> stagflation -> recovery scenario with exact Shapley
attribution on common random numbers (CRN). Prototype of the new engine's key mechanics. SYNTHETIC.

Usage: python -I v8_rerun.py <out.json> [N]

Players (6, 64 coalitions): STATE (fragility hedge), MR (mean-reversion amplification), ALPHA (opportunity-cost
alpha reallocation), QDD (memo-corpus filter on new commitments), OVL (overlay execution / opportunistic book),
DRAG (liquidity and carry costs: convex sleeve, facilities, reserve; in the v8 replica the stated -0.1pp).
Configurations:
  A  v8 replica: v8 book ($85bn-like, 55% liquid, no payout), named path, anticipative year-known positions,
     v8's claimed additive values for ALPHA/QDD/OVL/DRAG. Calibrated to v8's static-SAA outputs.
  A+x one new-engine feature switched on alone (x = filt, evid, ovl, drag).
  B  new engine on the v8 book: non-anticipative filtered signals, evidence-based priors, costs, Tier-1 filter.
  C  new engine on the ADIC working book ($177bn, ~60% private, 7.5% payout, DPI drought), named path.
  D  as C, but regime path stochastic (Markov chain starting in the oil-shock state), i.e. ex ante.
"""
import itertools
import json
import math
import sys

import numpy as np
from scipy import stats

OUT = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 50_000
T = 36
A_ = ["EQ", "FI", "PE", "RA", "PC", "HF", "OIL", "CR"]
iEQ, iFI, iPE, iRA, iPC, iHF, iOIL, iCR = range(8)
PLAYERS = ["STATE", "MR", "ALPHA", "QDD", "OVL", "DRAG"]
NP = len(PLAYERS)
CASH = 0.04

# ---------------------------------------------------------------- regimes: 0 OS (oil shock), 1 SF (stagflation),
# 2 RC (disinflation + recovery), 3 NM (normal). Means: v8 slide 6 for EQ..HF; OIL, CR and NM are [I].
MU = np.array([
    [-0.10, 0.08, -0.05, 0.09, -0.10, 0.05, 0.15, -0.08],
    [0.10, 0.04, 0.07, 0.08, 0.05, 0.07, 0.05, 0.05],
    [0.32, 0.10, 0.20, 0.12, 0.12, 0.06, -0.05, 0.12],
    [0.075, 0.053, 0.096, 0.079, 0.077, 0.067, 0.03, 0.061],
])
SIG1 = np.array([0.25, 0.10, 0.15, 0.12, 0.12, 0.08, 0.35, 0.12])
VMULT = np.array([1.0, 0.8, 0.7, 0.6])
RC_OS = [[1, -.2, .8, .3, .7, .7, -.3, .75], [-.2, 1, -.1, 0, -.1, -.1, -.2, -.1], [.8, -.1, 1, .3, .6, .6, -.2, .65],
         [.3, 0, .3, 1, .3, .3, .5, .3], [.7, -.1, .6, .3, 1, .6, -.2, .8], [.7, -.1, .6, .3, .6, 1, -.1, .65],
         [-.3, -.2, -.2, .5, -.2, -.1, 1, -.2], [.75, -.1, .65, .3, .8, .65, -.2, 1]]
RC_SF = [[1, .4, .75, .3, .6, .6, .1, .65], [.4, 1, .3, -.1, .3, .2, -.3, .4], [.75, .3, 1, .3, .5, .5, 0, .55],
         [.3, -.1, .3, 1, .2, .3, .5, .2], [.6, .3, .5, .2, 1, .5, 0, .75], [.6, .2, .5, .3, .5, 1, .1, .55],
         [.1, -.3, 0, .5, 0, .1, 1, 0], [.65, .4, .55, .2, .75, .55, 0, 1]]
RC_RC = [[1, 0, .7, .4, .5, .6, .2, .6], [0, 1, 0, .1, .1, 0, -.1, .2], [.7, 0, 1, .4, .5, .5, .1, .5],
         [.4, .1, .4, 1, .3, .3, .3, .3], [.5, .1, .5, .3, 1, .5, .1, .7], [.6, 0, .5, .3, .5, 1, .1, .5],
         [.2, -.1, .1, .3, .1, .1, 1, .1], [.6, .2, .5, .3, .7, .5, .1, 1]]


def higham(A, iters=3000, tol=1e-12):
    Y = np.array(A, float); dS = np.zeros_like(Y)
    for _ in range(iters):
        R = Y - dS
        w, V = np.linalg.eigh((R + R.T) / 2)
        X = (V * np.clip(w, 1e-8, None)) @ V.T
        dS = X - R
        Yn = X.copy(); np.fill_diagonal(Yn, 1.0)
        if np.abs(Yn - Y).max() < tol:
            return Yn
        Y = Yn
    return Y


CHOL = [np.linalg.cholesky(higham(m)) for m in (RC_OS, RC_SF, RC_RC, RC_RC)]
PM = np.array([[0.90, 0.06, 0.02, 0.02], [0.02, 0.92, 0.04, 0.02], [0.01, 0.01, 0.92, 0.06], [0.01, 0.01, 0.0, 0.98]])
DIST = np.array([0.06, 0.10, 0.15, 0.20])          # PE distribution rate by regime (C2: crisis 6, drought 10, normal 20)
DISC = np.array([0.25, 0.15, 0.10, 0.08])          # forced LP-secondary discount by regime [I, C2/stream 05 ranges]


def gen_market(seed, mode, vol_scale):
    rng = np.random.default_rng(seed)
    if mode == "named":
        reg = np.repeat(np.array([0, 1, 2]), 12)[None, :].repeat(N, 0)
    else:
        reg = np.zeros((N, T), int)
        u = rng.random((N, T))
        cum = PM.cumsum(1)
        for t in range(1, T):
            reg[:, t] = (u[:, t, None] > cum[reg[:, t - 1]]).sum(1)
    z = rng.standard_normal((T, N, 8))
    chi = rng.chisquare(5, (T, N)) / 5
    R = np.empty((T, N, 8))
    for t in range(T):
        e = np.empty((N, 8))
        for r in range(4):
            m = reg[:, t] == r
            if m.any():
                e[m] = z[t, m] @ CHOL[r].T
        e = e / np.sqrt(chi[t])[:, None] * math.sqrt(3 / 5)
        e = np.clip(e, -6, 6)
        mu = (1 + MU[reg[:, t]]) ** (1 / 12) - 1                 # monthly mean compounding to the annual mean
        sg = (SIG1[None, :] * VMULT[reg[:, t]][:, None]) * vol_scale / math.sqrt(12)
        R[t] = mu + sg * e
    eps_o = rng.standard_normal((T, N))
    par = dict(sr=rng.normal(0.30, 0.25, N), alpha=rng.normal(0.0075, 0.015, N), qdd=rng.normal(0.005, 0.005, N))
    return R, reg, eps_o, par


def hmm_filter(req):
    """2-state Gaussian filter on observed monthly EQ returns; p[t] uses returns up to t-1 (non-anticipative)."""
    m = np.array([0.008, -0.010]); s = np.array([0.035, 0.065])
    P = np.array([[0.97, 0.03], [0.08, 0.92]])
    p = np.empty((T, N)); ps = np.full(N, 0.35)
    for t in range(T):
        p[t] = ps
        pr_c, pr_s = (1 - ps) * P[0, 0] + ps * P[1, 0], (1 - ps) * P[0, 1] + ps * P[1, 1]
        lc = pr_c * stats.norm.pdf(req[t], m[0], s[0]); ls = pr_s * stats.norm.pdf(req[t], m[1], s[1])
        ps = ls / (lc + ls)
    return p


def bs_put(S, K, T_, r, q, v):
    d1 = (np.log(S / K) + (r - q + 0.5 * v * v) * T_) / (v * np.sqrt(T_)); d2 = d1 - v * np.sqrt(T_)
    return K * np.exp(-r * T_) * stats.norm.cdf(-d2) - S * np.exp(-q * T_) * stats.norm.cdf(-d1)


STATE_POS = {0: {iEQ: -.08, iFI: .08, iCR: -.04, iOIL: .02}, 1: {iEQ: -.02, iFI: .04, iOIL: .01}}
MR_POS = {iEQ: .18, iFI: .04, iCR: .04}


def run_config(cfg, R, reg, eps_o, par):
    """Returns per-coalition per-path annualized TWR (64 x N) plus metrics for empty and full coalitions."""
    book = cfg["book"]
    ant = cfg["anticipative"]
    kS, kM = cfg["kS"], cfg["kM"]
    # ---- market-only signals (coalition-independent)
    req = R[:, :, iEQ]
    pf = hmm_filter(req)
    hedge_sig = np.zeros((T, N), bool); hs = np.zeros(N, bool)
    amp_sig = np.zeros((T, N), bool); amp_left = np.zeros(N, int)
    cum12 = np.zeros((T, N))
    logeq = np.cumsum(np.log1p(req), 0)
    for t in range(T):
        hs = np.where(pf[t] > 0.6, True, np.where(pf[t] < 0.4, False, hs))
        hedge_sig[t] = hs
        if t >= 1:
            back = logeq[t - 1] - (logeq[t - 13] if t >= 13 else 0.0)
        else:
            back = np.zeros(N)
        cum12[t] = back
        trig = (back <= np.log(0.95)) & (pf[t] < 0.4) & (t >= 3)
        amp_left = np.where(trig & (amp_left == 0), 12, amp_left)
        amp_left = np.where(pf[t] > 0.6, 0, amp_left)
        amp_sig[t] = amp_left > 0
        amp_left = np.maximum(amp_left - 1, 0)
    yr = np.arange(T) // 12
    res = np.empty((2 ** NP, N)); extra = {}
    for mask in range(2 ** NP):
        on = {p: bool(mask >> i & 1) for i, p in enumerate(PLAYERS)}
        r_path, nav_path, aux = simulate(cfg, on, R, reg, eps_o, par, hedge_sig, amp_sig, yr)
        res[mask] = r_path
        if mask in (0, 2 ** NP - 1):
            extra[mask] = dict(nav=nav_path, aux=aux)
    return res, extra, dict(hedge_on_share=float(hedge_sig.mean()), amp_on_share=float(amp_sig.mean()),
                            hedge_on_by_year=[float(hedge_sig[yr == y].mean()) for y in range(3)],
                            amp_on_by_year=[float(amp_sig[yr == y].mean()) for y in range(3)])


def simulate(cfg, on, R, reg, eps_o, par, hedge_sig, amp_sig, yr):
    book, ant = cfg["book"], cfg["anticipative"]
    kS, kM = cfg["kS"], cfg["kM"]
    evid_alpha, evid_qdd, evid_ovl, new_drag = cfg["alpha"] == "evid", cfg["qdd"] == "evid", cfg["ovl"] == "evid", cfg["drag"] == "new"
    costs = cfg.get("costs", False)
    asc = cfg.get("add_scale", {})
    sfin = 0.005; tc = 0.0003
    gate_applied = np.zeros(N); gate_wanted = np.zeros(N)
    if book == "v8":
        w_t = np.array([.33, .15, .22, .10, .10, .10, 0, 0])          # EQ FI PE RA PC HF
    else:
        w_t = None
    nav = np.ones(N); navs = np.empty((T + 1, N)); navs[0] = 1.0
    nav_rep = np.ones(N); navs_rep = np.empty((T + 1, N)); navs_rep[0] = 1.0
    prev_pos = np.zeros((N, 8))
    # ADIC book state ($bn scaled to NAV=1)
    if book == "adic":
        h = np.zeros((N, 8))
        h[:, iEQ] = 28 / 177; h[:, iFI] = 8 / 177; h[:, iHF] = 20 / 177; h[:, iPE] = 88 / 177; h[:, iPC] = 18 / 177
        cash = np.full(N, 15 / 177); U = np.full(N, 38 / 177); debt = np.zeros(N)
        cash_tgt = 15 / 177 + (0.05 if (on["DRAG"] and new_drag) else 0.0)
        if on["DRAG"] and new_drag:
            h[:, iEQ] -= 0.05; cash += 0.05
        eq_tgt0, fi_tgt0 = h[0, iEQ], h[0, iFI]
        payout_m = np.zeros(N); forced_loss = np.zeros(N); n_forced = np.zeros(N, bool); fac_used = np.zeros(N)
    convex_N = np.zeros(N); eq_px0 = np.ones(N); eqpx = np.ones(N)
    for t in range(T):
        y = yr[t]; rg = reg[:, t]
        Rt = R[t]
        # -------- overlay positions (fraction of NAV)
        pos = np.zeros((N, 8))
        if on["STATE"]:
            if ant:
                for k, v in STATE_POS.get(y, {}).items():
                    pos[:, k] += kS * v
            else:
                hsig = hedge_sig[t]
                for k, v in STATE_POS[0].items():
                    pos[hsig, k] += kS * v
        if on["MR"]:
            if ant:
                if y == 2:
                    for k, v in MR_POS.items():
                        pos[:, k] += kM * v
            else:
                a = amp_sig[t].copy()
                gate_wanted += a
                if book == "adic":                                 # Tier-1 gate (liquidity) on amplification
                    navb = h.sum(1) + cash - debt
                    liq = (cash + h[:, iEQ] + h[:, iFI] + 0.5 * h[:, iHF]) / navb
                    a &= (liq >= 0.25) & (cash / navb >= 0.06)
                gate_applied += a
                for k, v in MR_POS.items():
                    pos[a, k] += kM * v
        if not ant:                                                # safety filter: economic exposure <= 1.30
            if book == "v8":
                base_exp = 1.0 - 0.15 * 0                          # FI counted as risky (duration) -> ~1.0
                expo = base_exp + pos[:, iEQ] + pos[:, iCR]
            else:
                navb = h.sum(1) + cash - debt
                expo = (h.sum(1)) / navb + pos[:, iEQ] + pos[:, iCR]
            scale = np.where(expo > 1.30, np.clip((1.30 - (expo - pos[:, iEQ] - pos[:, iCR])) /
                                                  np.maximum(pos[:, iEQ] + pos[:, iCR], 1e-9), 0, 1), 1.0)
            pos[:, iEQ] *= scale; pos[:, iCR] *= scale
        ovl_pnl = (pos * (Rt - CASH / 12)).sum(1)
        if costs:                                                  # trading + futures financing over cash
            ovl_pnl -= tc * np.abs(pos - prev_pos).sum(1)
            ovl_pnl -= sfin / 12 * (np.clip(pos[:, iEQ], 0, None) + np.clip(pos[:, iCR], 0, None))
        prev_pos = pos
        # -------- additive components
        add = np.zeros(N)
        if on["ALPHA"]:
            if evid_alpha:
                wa = min(0.03 * (t + 1) / 12, 0.09)
                a_rate = par["alpha"]
                if book == "adic":
                    navb = h.sum(1) + cash - debt
                    liq = (cash + h[:, iEQ] + h[:, iFI] + 0.5 * h[:, iHF]) / navb
                    a_rate = a_rate - np.where(liq < 0.30, 0.01, 0.0)
                add += wa * a_rate / 12
            else:
                add += asc.get("ALPHA", 1.0) * 0.008 / 12
        if on["QDD"]:
            if evid_qdd:
                wq = min(0.02 * (t + 1) / 12, 0.06)
                add += wq * par["qdd"] / 12
            else:
                add += asc.get("QDD", 1.0) * 0.005 / 12
        add_ovl = np.zeros(N)
        if on["OVL"]:
            if evid_ovl:
                so = 0.0125
                add_ovl += par["sr"] * so / 12 + so / math.sqrt(12) * (0.2 * (Rt[:, iEQ] - Rt[:, iEQ].mean()) /
                                                                      max(Rt[:, iEQ].std(), 1e-9) * 1.0 +
                                                                      math.sqrt(1 - 0.04) * eps_o[t])
            else:
                add_ovl += asc.get("OVL", 1.0) * 0.010 / 12
        drag_m = np.zeros(N)
        if on["DRAG"]:
            if new_drag:
                drag_m += 0.0003 / 12                               # facility standby (10% NAV x 30bp)
                if t % 12 == 0:                                     # buy 12m 90/72 put spread, budget 0.20% NAV
                    v_impl = SIG1[iEQ] * VMULT[rg] * cfg["vs"] * 1.15
                    unit = bs_put(1.0, 0.90, 1.0, CASH, 0.02, v_impl) - bs_put(1.0, 0.72, 1.0, CASH, 0.02, v_impl)
                    convex_N = 0.0020 / unit
                    eq_px0 = eqpx.copy()
                    drag_m += 0.0020                                # premium (fraction of current NAV)
            else:
                drag_m += asc.get("DRAG", 1.0) * 0.001 / 12
        eqpx = eqpx * (1 + Rt[:, iEQ] - 0.02 / 12)
        payoff = np.zeros(N)
        if on["DRAG"] and new_drag and t % 12 == 11:
            X = eqpx / eq_px0
            payoff = convex_N * (np.clip(0.90 - X, 0, None) - np.clip(0.72 - X, 0, None))
        # -------- portfolio update
        if book == "v8":
            r_core = Rt @ w_t
            r = r_core + ovl_pnl + add + add_ovl - drag_m + payoff
            nav = nav * (1 + r)
            # reported basis (v8 'private-asset lag'): privates marked at the trailing 3-month average, lagged 1 month
            Rrep = Rt.copy()
            for k in (iPE, iRA, iPC):
                lags = [R[t - j, :, k] if t - j >= 0 else np.full(N, (1 + MU[0, k]) ** (1 / 12) - 1) for j in (1, 2, 3)]
                Rrep[:, k] = sum(lags) / 3
            nav_rep = nav_rep * (1 + Rrep @ w_t + ovl_pnl + add + add_ovl - drag_m + payoff)
            navs_rep[t + 1] = nav_rep
        else:
            navb = h.sum(1) + cash - debt
            # returns on holdings
            h = h * (1 + Rt)
            h[:, iRA] = 0; h[:, iOIL] = 0; h[:, iCR] = 0
            cash = cash * (1 + CASH / 12) + navb * (ovl_pnl + add_ovl - drag_m + payoff)  # VM, premia, payoffs
            h[:, iPE] += navb * add                                  # alpha / QDD accrue in private NAV
            debt = debt * (1 + (CASH + 0.015) / 12)
            # private flows
            calls = U * 0.28 / 12; U = U + (11 / 177) / 12 * 1.0 - calls
            dist = h[:, iPE] * DIST[rg] / 12
            h[:, iPE] += calls - dist; cash += dist - calls
            pc_cash = h[:, iPC] * 0.04 / 12; h[:, iPC] -= pc_cash; cash += pc_cash
            # payout (7.5% of NAV at start of each year, paid monthly)
            if t % 12 == 0:
                payout_m = 0.075 * (h.sum(1) + cash - debt) / 12
            cash -= payout_m
            navn = h.sum(1) + cash - debt
            im = 0.08 * np.abs(pos).sum(1) * navn + (0.0056 if on["OVL"] else 0.0)
            avail = cash - im
            tgt = cash_tgt * navn
            need = np.clip(tgt - avail, 0, None)
            # 1) sell FI/EQ pro rata
            liq_ = h[:, iEQ] + h[:, iFI]
            sell = np.minimum(need, liq_)
            fr = np.where(liq_ > 0, sell / np.maximum(liq_, 1e-12), 0)
            h[:, iEQ] *= 1 - fr; h[:, iFI] *= 1 - fr; cash += sell; need -= sell
            # 2) redeem HF up to monthly limit
            lim = h[:, iHF] * np.where(rg == 0, 0.05 / 3, 0.10 / 3)
            red = np.minimum(need, lim); h[:, iHF] -= red; cash += red; need -= red
            avail = cash - im
            floor = 0.04 * navn
            short = np.clip(floor - avail, 0, None)
            if on["DRAG"] and new_drag:                              # committed facility (10% NAV, 50% avail in stress)
                cap = 0.10 * navn * np.where(rg <= 1, 0.5, 1.0) - debt
                draw = np.minimum(short, np.clip(cap, 0, None)); debt += draw; cash += draw; short -= draw
                fac_used = np.maximum(fac_used, debt / navn)
            # 3) forced PE secondary sale to restore avail to floor + 2%
            restore = np.where(short > 0, short + 0.02 * navn, 0.0)
            d = DISC[rg]
            sale_nav = np.minimum(restore / (1 - d), h[:, iPE] * 0.5)
            h[:, iPE] -= sale_nav; cash += sale_nav * (1 - d)
            forced_loss += sale_nav * d / navn; n_forced |= sale_nav > 0
            # rebalance excess cash back to FI/EQ targets; repay debt first
            navn = h.sum(1) + cash - debt
            excess = np.clip(cash - im - (cash_tgt + 0.03) * navn, 0, None)
            rep = np.minimum(excess, debt); debt -= rep; cash -= rep; excess -= rep
            gap_eq = np.clip(eq_tgt0 * navn - h[:, iEQ], 0, None); gap_fi = np.clip(fi_tgt0 * navn - h[:, iFI], 0, None)
            gtot = gap_eq + gap_fi
            buy = np.minimum(excess, gtot)
            h[:, iEQ] += np.where(gtot > 0, buy * gap_eq / np.maximum(gtot, 1e-12), 0)
            h[:, iFI] += np.where(gtot > 0, buy * gap_fi / np.maximum(gtot, 1e-12), 0)
            cash -= buy
            navn = h.sum(1) + cash - debt
            r = (navn + payout_m) / navb - 1
            nav = nav * (1 + r)
        navs[t + 1] = nav
    ann = nav ** (1 / 3) - 1
    aux = {}
    if book == "v8":
        ddr = 1 - navs_rep / np.maximum.accumulate(navs_rep, 0)
        aux = dict(p_dd15_reported=float((ddr.max(0) > 0.15).mean()),
                   p10_reported=float(np.quantile(nav_rep ** (1 / 3) - 1, 0.10)))
    if book == "adic":
        aux = dict(p_forced=float(n_forced.mean()), forced_loss_mean=float(forced_loss.mean()),
                   private_share_end=float(np.mean((h[:, iPE] + h[:, iPC]) / (h.sum(1) + cash - debt))),
                   liquid_share_end=float(np.mean((cash + h[:, iEQ] + h[:, iFI] + 0.5 * h[:, iHF]) /
                                                  (h.sum(1) + cash - debt))),
                   fac_used_p90=float(np.quantile(fac_used, 0.9)))
    if gate_wanted.sum() > 0:
        aux["amp_months_wanted"] = float(gate_wanted.mean()); aux["amp_months_applied"] = float(gate_applied.mean())
    return ann, navs, aux


def shapley(res):
    n = NP; phi = np.zeros((n, res.shape[1]))
    for i in range(n):
        for mask in range(2 ** n):
            if mask >> i & 1:
                continue
            s = bin(mask).count("1")
            wgt = math.factorial(s) * math.factorial(n - s - 1) / math.factorial(n)
            phi[i] += wgt * (res[mask | (1 << i)] - res[mask])
    return phi


def metrics(ann, navs):
    dd = 1 - navs / np.maximum.accumulate(navs, 0)
    return dict(mean=float(ann.mean()), p_ge10=float((ann >= 0.10).mean()), p10=float(np.quantile(ann, 0.10)),
                p_dd15=float((dd.max(0) > 0.15).mean()))


CFGS = {
    "A_v8_replica": dict(book="v8", mode="named", anticipative=True, alpha="v8", qdd="v8", ovl="v8", drag="v8"),
    "A+filter": dict(book="v8", mode="named", anticipative=False, alpha="v8", qdd="v8", ovl="v8", drag="v8"),
    "A+costs": dict(book="v8", mode="named", anticipative=True, alpha="v8", qdd="v8", ovl="v8", drag="v8", costs=True),
    "A+evidence_alpha_qdd": dict(book="v8", mode="named", anticipative=True, alpha="evid", qdd="evid", ovl="v8", drag="v8"),
    "A+evidence_overlay": dict(book="v8", mode="named", anticipative=True, alpha="v8", qdd="v8", ovl="evid", drag="v8"),
    "A+new_drags": dict(book="v8", mode="named", anticipative=True, alpha="v8", qdd="v8", ovl="v8", drag="new"),
    "B_new_engine_v8book": dict(book="v8", mode="named", anticipative=False, alpha="evid", qdd="evid", ovl="evid",
                                drag="new", costs=True),
    "B_exante_v8book": dict(book="v8", mode="markov", anticipative=False, alpha="evid", qdd="evid", ovl="evid",
                            drag="new", costs=True),
    "C_new_engine_ADIC_named": dict(book="adic", mode="named", anticipative=False, alpha="evid", qdd="evid", ovl="evid",
                                    drag="new", costs=True),
    "D_new_engine_ADIC_exante": dict(book="adic", mode="markov", anticipative=False, alpha="evid", qdd="evid",
                                     ovl="evid", drag="new", costs=True),
}

if __name__ == "__main__":
    out = {}
    VS = 0.90            # vol scale calibrated so the v8 static SAA matches v8's mean, P(>=10%) and P10 (calib_v8.py)
    cache = {}
    for mode in ("named", "markov"):
        cache[mode] = gen_market(20261018 if mode == "named" else 20261019, mode, VS)
    # ---- calibration of kS, kM on the replica so STATE ~ +0.5pp and MR ~ +0.8pp (v8 slide 6)
    R, reg, eps, par = cache["named"]
    kS, kM = 1.0, 1.0
    asc = dict(ALPHA=1.0, QDD=1.0, OVL=1.0, DRAG=1.0)
    target = dict(STATE=0.005, MR=0.008, ALPHA=0.008, QDD=0.005, OVL=0.010, DRAG=-0.001)
    for it in range(4):
        cfg = dict(CFGS["A_v8_replica"], kS=kS, kM=kM, vs=VS, add_scale=asc)
        res, extra, sig = run_config(cfg, R, reg, eps, par)
        phi = dict(zip(PLAYERS, shapley(res).mean(1)))
        kS *= target["STATE"] / phi["STATE"]; kM *= target["MR"] / phi["MR"]
        for p in ("ALPHA", "QDD", "OVL", "DRAG"):
            asc[p] *= target[p] / phi[p]
    out["calibration"] = dict(vol_scale=VS, kS=kS, kM=kM, add_scale=asc)
    for name, c in CFGS.items():
        R, reg, eps, par = cache[c["mode"]]
        cfg = dict(c, kS=kS, kM=kM, vs=VS, add_scale=asc)
        res, extra, sig = run_config(cfg, R, reg, eps, par)
        phi_p = shapley(res)
        phi = phi_p.mean(1); se = phi_p.std(1) / math.sqrt(N)
        m0 = metrics(res[0], extra[0]["nav"]); m1 = metrics(res[-1], extra[2 ** NP - 1]["nav"])
        out[name] = dict(static=m0, full=m1, uplift=m1["mean"] - m0["mean"],
                         shapley={p: [float(phi[i]), float(se[i])] for i, p in enumerate(PLAYERS)},
                         signals=sig, aux_static=extra[0]["aux"], aux_full=extra[2 ** NP - 1]["aux"])
        print(f"\n== {name}  (N={N})")
        print("   static:", {k: round(v, 4) for k, v in m0.items()}, extra[0]["aux"])
        print("   full  :", {k: round(v, 4) for k, v in m1.items()}, extra[2 ** NP - 1]["aux"])
        print("   uplift: %.4f" % (m1["mean"] - m0["mean"]))
        print("   shapley:", {p: (round(phi[i] * 100, 2), round(1.96 * se[i] * 100, 2)) for i, p in enumerate(PLAYERS)})
        print("   signals:", sig)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("\ncalibration:", out["calibration"])
