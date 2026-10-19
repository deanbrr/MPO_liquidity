"""
ra_integration_calcs COPY of ra_gap_01's ra_module.py (original untouched). ri: adds the switches oil_enr / oil_gcc
(defaults True reproduce ra_gap_01 exactly): oil_enr=False zeroes the ENR oil elasticity and the oil-elastic ENR
income / exit factors (an oil-neutral sleeve with the same normal-state cash profile); oil_gcc=False removes the GCC
real-estate fiscal channels (Z-state value drag, income and exit multipliers). Expected returns are re-centred so
that switching a channel off removes the co-movement, not the mean.

ra_gap_01: quarterly Real Assets state machine for the integrated Monte Carlo (ra_engine.py).

SYNTHETIC - NOT ADIC DATA. All parameters are [I] defaults from the RA synthesis (s4-s9, s11) and ra_book.

Per path and sleeve (arrays of shape (n, S)) it carries:
  GT   true gross asset value          GR   reported (appraisal) gross asset value (RAME observation model)
  D    look-through asset-level debt   U    unfunded commitments
  rr   last reported asset return      lag buffer of true asset returns (segment lag 1q, ENR 2q)
  es   nowcast error by sector (V* = GT exp(es) - D; RMSE 5.5% asset level, AR(1) 0.5) [I; G13 R2 middle band]
  open-end queue state for RE_OE / INF_OE (G10 machine: others' queue Q, ADIC request share f_req)
Equity values: V^T = GT - D, V^A = GR - D, V* = GT exp(es) - D.

Quarterly order (called by the engine): returns() -> flows() [income, realisations, calls, maturities with cures
and the fund-level module, open-end payments] -> actions (notices, JV sell-down, cash-out, sales) -> commitments.
Every random draw comes from the engine's dedicated RA stream, so common random numbers hold for everything else.
"""
from __future__ import annotations

import math

import numpy as np

import ra_book as B

KQ = 1.0 - 0.6 ** 0.25                     # oil mean-reversion per quarter in the engine's oil process
R_DEBT = 0.050                             # average cost of the existing look-through debt [I]
CRISIS_DRAG = {"RE": -0.020, "RE_GCC": -0.020, "INF": -0.010, "ENR": -0.010}   # asset, per crisis quarter [I]
GCC_DRAG_Z = np.array([0.0, 0.0, -0.020, -0.025, 0.0, 0.0])                    # N B SG DB SS GW (value) [I]
GCC_INC_Z = np.array([1.0, 1.0, 0.90, 0.88, 1.0, 0.90])                        # G15 SG / GW income
GCC_EXIT_Z = np.array([1.0, 1.0, 0.5, 0.5, 1.0, 0.5])
INC_CRISIS = {"RE": 0.92, "RE_GCC": 0.90, "INF": 0.97, "ENR": 1.0}             # G15 S1 multipliers
EXIT_PREM = np.array([1.06, 1.03, 0.98, 0.90])                                 # O N D F, of economic NAV (G11)
LTV_MAX = {"N": {"RE": 0.625, "RE_GCC": 0.625, "INF": 0.725, "ENR": 0.55},
           "T": {"RE": 0.575, "RE_GCC": 0.575, "INF": 0.675, "ENR": 0.50},
           "C": {"RE": 0.525, "RE_GCC": 0.45, "INF": 0.625, "ENR": 0.45}}    # synthesis s5 (INF +10pp; GCC 45%)
AVAIL = {"N": 0.97, "T": 0.825, "C": 0.55}                                     # synthesis s5 [I]
SALE_PX = {  # proceeds per $ of reported NAV: normal / drought / crisis (G15 ladder, T4' column for crisis)
    "RE_OE": (0.96, 0.94, 0.82), "RE_CE": (0.71, 0.68, 0.475), "RE_DIR_GL": (0.95, 0.90, 0.73),
    "RE_DIR_GCC": (0.93, 0.90, 0.70), "RE_COI": (0.88, 0.82, 0.60), "INF_OE": (0.97, 0.96, 0.86),
    "INF_CE": (0.91, 0.90, 0.72), "INF_DIR": (0.96, 0.94, 0.82), "ENR_CE": (0.82, 0.80, 0.55),
    "ENR_DIR": (0.90, 0.88, 0.62)}
JV_PX = (0.95, 0.92, 0.80)                 # partial SELL of controlled equity (G15 ladder)
CASHOUT_LTV = {"RE": 0.55, "RE_GCC": 0.55, "INF": 0.60, "ENR": 0.50}
CASHOUT_SPREAD = 0.02                      # extra annual cost of cash-out debt over the book's debt cost [I]
QUEUE = dict(r0=0.006, b=0.12, w=0.08, l0=0.0025, d=np.array([0.010, 0.006, 0.004, 0.002]), cin=0.012,
             cin_low=0.004, h=0.06, q0={"RE_OE": 0.10, "INF_OE": 0.05}, cap={"RE_OE": 1.0, "INF_OE": 0.05})
BETA_RECOVERY_DESM, BETA_RECOVERY_OBS = 0.80, 0.35   # RAME: 3-step recovers 75-85% of true beta, appraisals 25-48%
RAME_SD, RAME_PHI = 0.055, 0.5


class RAState:
    def __init__(self, n: int, m, rng, cash_lr: float, eq_g: float, pi_c: float, pz_stat: np.ndarray,
                 scale: float = 1.0, split=None, ext: float = 0.0, fund_module: str = "waterfall",
                 availability: bool = True, md_f: float = 0.30, mc_f: float = 0.80, oil_enr: bool = True,
                 oil_gcc: bool = True):
        self.n = n
        self.oil_enr, self.oil_gcc = bool(oil_enr), bool(oil_gcc)      # ri: oil-sensitivity switches
        self.rng = rng
        self.S = B.NS
        sl = B.SLEEVES
        self.ids = B.SIDS
        self.sec = [s["sector"] for s in sl]
        self.ltv0 = np.array([s["ltv"] for s in sl])
        self.beta_eq = np.array([s["beta_eq"] for s in sl])
        self.beta_a = self.beta_eq * (1 - self.ltv0)
        self.eps_eq = np.array([s["eps_oil"] for s in sl])
        self.eps_a = self.eps_eq * (1 - self.ltv0)
        self.sig = np.array([s["sig_a"] for s in sl])
        self.lam = np.array([s["lam"] for s in sl])
        self.lag = np.array([s["lag"] for s in sl], dtype=int)
        self.inc = np.array([s["inc"] for s in sl])
        self.real_n = np.array([s["real_n"] for s in sl])
        self.real_d = np.array([s["real_d"] for s in sl])
        self.direct = np.array([s["direct"] for s in sl])
        self.ctrl = np.array([s["ctrl"] for s in sl])
        self.is_enr = np.array([s["sector"] == "ENR" for s in sl])
        self.is_gcc = np.array([s["sector"] == "RE_GCC" for s in sl])
        self.is_oe = np.array([s["vehicle"] == "OE" for s in sl])
        if not self.oil_enr:                           # ri: oil-neutral ENR (no value elasticity to oil)
            self.eps_eq = np.where(self.is_enr, 0.0, self.eps_eq)
            self.eps_a = self.eps_eq * (1 - self.ltv0)
        self.cdrag = np.array([CRISIS_DRAG[s] for s in self.sec])
        self.inc_cr = np.array([INC_CRISIS[s] for s in self.sec])
        if split is None:
            commit = np.array([s["commit"] for s in sl])
        else:                                          # (RE_CE, INF_CE, ENR_CE) shares of new closed-end commitments
            commit = np.zeros(len(sl))
            for sid, w in zip(("RE_CE", "INF_CE", "ENR_CE"), split):
                commit[[s["id"] for s in sl].index(sid)] = w
        self.commit = commit / commit.sum()
        self.ext = ext
        self.fund_module = fund_module
        self.availability = availability
        self.md_f, self.mc_f = md_f, mc_f
        nav = np.array([s["nav"] for s in sl]) * scale
        unf = np.array([s["unf"] for s in sl]) * scale
        g0 = np.array([s["g0"] for s in sl])
        D = nav * self.ltv0 / (1 - self.ltv0)
        GR = nav + D
        GT = GR / (1 + g0)
        self.D = np.tile(D, (n, 1))
        self.GR = np.tile(GR, (n, 1))
        self.GT = np.tile(GT, (n, 1))
        self.U = np.tile(unf, (n, 1))
        self.rr = np.zeros((n, self.S))
        self.buf = np.zeros((n, self.S, 3))          # true asset returns, most recent first
        self.sec_names = ["RE", "RE_GCC", "INF", "ENR"]
        self.sec_idx = np.array([self.sec_names.index(s) for s in self.sec])
        self.es = RAME_SD * rng.standard_normal((n, 4))
        self.co_debt = np.zeros((n, self.S))
        # open-end queue machine
        self.Qo = np.zeros((n, self.S))
        for k, q in QUEUE["q0"].items():
            self.Qo[:, self.ids.index(k)] = q
        self.freq = np.zeros((n, self.S))             # ADIC outstanding request, share of its units
        self.lodged = np.zeros(n, dtype=bool)
        self.jv_sold = np.zeros(n)                     # cumulative controlled equity sold down ($ reported)
        self.ctrl_nav0 = float((nav * self.ctrl).sum())
        # expected-return calibration: asset drift a_s so that E[equity geometric return] = target (model m)
        sig_m = 0.165
        g_e = cash_lr + self.beta_eq * (eq_g - cash_lr) + np.array([s["prem"] for s in sl])
        sig_e2 = (self.beta_eq * sig_m) ** 2 + (2 * self.sig / (1 - self.ltv0)) ** 2
        mu_e = g_e + 0.5 * sig_e2
        mu_a = (1 - self.ltv0) * mu_e + self.ltv0 * R_DEBT
        eq_arith = math.log1p(eq_g) + 0.5 * sig_m ** 2
        e_gcc = float(pz_stat @ GCC_DRAG_Z) * 4.0 * (1.0 if self.oil_gcc else 0.0)   # ri: switch
        mu_z = np.array([0, .20, -.35, -.45, .30, .10])
        e_oil = float(pz_stat @ mu_z)                  # annual expected oil innovation (regime drifts)
        self.a = mu_a - cash_lr - self.beta_a * (eq_arith - cash_lr) - 4 * pi_c * self.cdrag \
            - self.is_gcc * e_gcc - self.eps_a * e_oil
        self.g_e_target = g_e
        # appraisal filter starts in its steady state (expected quarterly asset return), not cold
        self.rr = np.tile(mu_a / 4.0, (n, 1))
        self.buf = np.tile((mu_a / 4.0)[None, :, None], (n, 1, 3))

    # ------------------------------------------------------------------ views
    def vt(self):
        return self.GT - self.D

    def va(self):
        return self.GR - self.D

    def vs(self):
        return self.GT * np.exp(self.es[:, self.sec_idx]) - self.D

    def nav_true(self):
        return self.vt().sum(1)

    def nav_rep(self):
        return self.va().sum(1)

    def nav_star(self):
        return self.vs().sum(1)

    def unf_tot(self):
        return self.U.sum(1)

    def oil_delta(self, oil):
        """Spot-equivalent barrels (m) at the path's oil price: sum V^T eps / P."""
        return (self.vt() * self.eps_eq[None, :]).sum(1) / np.maximum(oil, 1.0) * 1000.0

    # ------------------------------------------------------------------ dynamics
    def returns(self, r_eq, cash_q, crisis, z, oil, oil_prev):
        n = self.n
        innov = np.log(oil / oil_prev) - KQ * (np.log(70.0) - np.log(oil_prev))
        eps = self.rng.standard_normal((n, self.S))
        r_a = cash_q + self.beta_a[None, :] * (r_eq - cash_q)[:, None] + self.a[None, :] / 4 \
            + self.cdrag[None, :] * crisis[:, None] \
            + (self.is_gcc[None, :] * GCC_DRAG_Z[z][:, None] if self.oil_gcc else 0.0) \
            + self.eps_a[None, :] * innov[:, None] + self.sig[None, :] * eps
        r_a = np.maximum(r_a, -0.5)
        self.buf = np.concatenate([r_a[:, :, None], self.buf[:, :, :-1]], axis=2)
        lagged = np.take_along_axis(self.buf, np.broadcast_to(self.lag[None, :, None], (n, self.S, 1)), axis=2)[:, :, 0]
        self.rr = self.lam[None, :] * self.rr + (1 - self.lam[None, :]) * lagged
        interest = self.D * R_DEBT / 4                  # paid by the assets to lenders (not ADIC cash)
        self.GT = self.GT * (1 + r_a) - interest
        self.GR = self.GR * (1 + self.rr) - interest
        self.es = RAME_PHI * self.es + RAME_SD * math.sqrt(1 - RAME_PHI ** 2) * self.rng.standard_normal((n, 4))
        # cash-out debt carries an extra spread (charged as a cash cost in flows)
        return r_a

    def _remove(self, frac, unfunded: bool = True):
        """Remove a fraction (n, S) of every sleeve's balance sheet. Sales and redemptions transfer the unfunded
        too (buyer assumes it); realisations (exits) do not."""
        keep = 1 - frac
        self.GT, self.GR, self.D, self.co_debt = self.GT * keep, self.GR * keep, self.D * keep, self.co_debt * keep
        if unfunded:
            self.U = self.U * keep

    def flows(self, e, crisis, z, oil, stage, notices_on):
        """Cash to / from ADIC this quarter. Returns dict of (n,) arrays and per-sleeve cure cash."""
        n, S = self.n, self.S
        va = np.maximum(self.va(), 0.0)
        vt = np.maximum(self.vt(), 0.0)
        # income
        m_inc = np.where(crisis[:, None], self.inc_cr[None, :], 1.0)
        if self.oil_gcc:                                   # ri: switch
            m_inc = np.where(self.is_gcc[None, :], m_inc * GCC_INC_Z[z][:, None], m_inc)
        if self.oil_enr:                                   # ri: switch
            oilf = np.clip((oil / 80.0) ** 0.8, 0.3, 2.0)
            m_inc = np.where(self.is_enr[None, :], oilf[:, None], m_inc)
        inc = self.inc[None, :] * m_inc * va / 4
        # realisations (closed-end and co-investment exits)
        ec = e[:, None]
        rate = np.select([ec == 0, ec == 1, ec == 2],
                         [np.broadcast_to(1.25 * self.real_n, (n, S)), np.broadcast_to(self.real_n, (n, S)),
                          np.broadcast_to(self.real_d, (n, S))],
                         np.broadcast_to(self.real_d * (self.md_f / 0.5), (n, S)))
        if self.oil_enr:                                   # ri: switch
            oil_x = np.clip((oil / 80.0) ** 1.2, 0.3, 2.0)
            rate = np.where(self.is_enr[None, :], rate * oil_x[:, None], rate)
        if self.oil_gcc:                                   # ri: switch
            rate = np.where(self.is_gcc[None, :], rate * GCC_EXIT_Z[z][:, None], rate)
        q = 1 - (1 - np.minimum(rate, 0.95)) ** 0.25
        proceeds = q * vt * EXIT_PREM[e][:, None]
        # pay out income from both value bases, then remove the realised fraction (unfunded stays)
        self.GT = self.GT - inc
        self.GR = self.GR - inc
        self._remove(q, unfunded=False)
        # calls (new assets carry debt at origination LTV)
        mC = np.array([1.3, 1.0, 0.97, self.mc_f])[e]
        cq = 1 - (1 - np.minimum(0.29 * mC, 0.95)) ** 0.25
        calls = cq[:, None] * self.U
        self.U = self.U - calls
        add_gav = calls / (1 - self.ltv0[None, :])
        self.GT = self.GT + add_gav
        self.GR = self.GR + add_gav
        self.D = self.D + add_gav - calls
        # maturities: refinance at LTV^max(state) x availability; gaps cured (direct, varpi = 1) or fund module
        lstate = np.where(crisis, 2, np.where((e >= 2), 1, 0))
        ltvmax = np.stack([np.array([LTV_MAX[k][s] for s in self.sec]) for k in ("N", "T", "C")])[lstate]
        av = np.array([AVAIL["N"], AVAIL["T"], AVAIL["C"]])[lstate] if self.availability else np.ones(n)
        Dm = self.D * B.MATURITY_PA / 4
        Vm = self.GT * np.where(self.D > 1e-12, Dm / np.maximum(self.D, 1e-12), 0.0)
        ext = np.where(crisis, 0.0, B.EXT_N) if self.ext is None else np.full(n, self.ext)
        refi = av[:, None] * np.minimum(Dm, ltvmax * Vm) + (1 - av[:, None]) * ext[:, None] * Dm
        gap = np.maximum(Dm - refi, 0.0)
        cure = np.where(self.direct[None, :], gap, 0.0)
        self.D = self.D - cure
        fgap = np.where(self.direct[None, :], 0.0, gap)
        prot = np.zeros((n, S))
        stop = np.zeros((n, S))
        loss = np.zeros((n, S))
        if self.fund_module == "upper":
            cure = cure + fgap
            self.D = self.D - fgap
        elif self.fund_module == "waterfall":
            prot = np.minimum(fgap, self.U)
            self.U = self.U - prot
            rem = fgap - prot
            stop = np.minimum(rem, inc + proceeds)
            rem = rem - stop
            self.D = self.D - prot - stop - rem
            self.GT = self.GT - rem / 0.8
            self.GR = self.GR - rem / 0.8
            loss = 0.25 * rem
        dist_cash = inc + proceeds - stop
        # open-end queue payments (G10 machine); ADIC notices only if lodged
        red_cash = np.zeros(n)
        if self.is_oe.any():
            for j in np.where(self.is_oe)[0]:
                vaj = np.maximum(self.va()[:, j], 1e-9)
                vtj = np.maximum(self.vt()[:, j], 1e-9)
                gmi = vaj / vtj - 1
                R = QUEUE["r0"] + QUEUE["b"] * np.maximum(gmi, 0.0)
                W = QUEUE["w"] * self.Qo[:, j] * (gmi <= 0.03)
                cin = np.where((gmi <= 0.03) & (self.Qo[:, j] <= 0.05), QUEUE["cin"], QUEUE["cin_low"])
                L = QUEUE["l0"] + QUEUE["d"][e] * (self.GR[:, j] / vaj) + cin \
                    - (fgap[:, j] / vaj)
                L = np.clip(np.minimum(L, QUEUE["cap"][self.ids[j]]), 0.0, None)
                adic = QUEUE["h"] * self.freq[:, j]
                pool = np.maximum(self.Qo[:, j] + R - W, 0.0) + adic
                P = np.minimum(pool, L)
                paid_adic = np.where(pool > 1e-12, P * adic / np.maximum(pool, 1e-12), 0.0)
                frac = np.clip(paid_adic / QUEUE["h"], 0.0, 1.0)      # share of ADIC units redeemed
                cash_j = frac * self.va()[:, j]
                red_cash += cash_j
                f = np.zeros((n, S))
                f[:, j] = frac
                self._remove(f)
                self.freq[:, j] = np.clip(np.where(1 - frac > 1e-9, (self.freq[:, j] - frac)
                                                   / np.maximum(1 - frac, 1e-9), 0.0), 0.0, 1.0)
                others = np.maximum(self.Qo[:, j] + R - W, 0.0)
                self.Qo[:, j] = others - np.where(pool > 1e-12, P * others / np.maximum(pool, 1e-12), 0.0)
        co_cost = (self.co_debt.sum(1)) * CASHOUT_SPREAD / 4
        return dict(income=inc.sum(1), realiz=proceeds.sum(1), stop=stop.sum(1), dist=dist_cash.sum(1),
                    calls=calls.sum(1), cures=cure.sum(1), prot=prot.sum(1), loss=loss.sum(1), red=red_cash,
                    co_cost=co_cost, gap_fund=fgap.sum(1), cure_cash=(cure + prot + stop).sum(1))

    # ------------------------------------------------------------------ actions
    def lodge_notices(self, mask):
        """Lodge redemption notices for all open-end units on paths in mask (once)."""
        new = mask & ~self.lodged
        for j in np.where(self.is_oe)[0]:
            self.freq[:, j] = np.where(new, 1.0, self.freq[:, j])
        self.lodged |= new

    def price_state(self, e, crisis):
        return np.where(crisis, 2, np.where(e >= 2, 1, 0))

    def jv_selldown(self, need, e, crisis, cap_share_q=0.10):
        """Partial SELL of controlled equity (pre-arranged): up to 40% of t0 controlled NAV (20% in crisis),
        10% of it a quarter, at 0.95 / 0.92 / 0.80 of reported NAV. Returns cash (n,) and value given up (n,)."""
        ps = self.price_state(e, crisis)
        px = np.array(JV_PX)[ps]
        cap_tot = np.where(crisis, 0.20, 0.40) * self.ctrl_nav0
        room = np.maximum(cap_tot - self.jv_sold, 0.0)
        ctrl_va = (np.maximum(self.va(), 0) * self.ctrl[None, :]).sum(1)
        amt = np.minimum(np.minimum(room, cap_share_q * self.ctrl_nav0), np.minimum(need / px, ctrl_va))
        amt = np.maximum(amt, 0.0)
        frac_c = np.where(ctrl_va > 1e-9, amt / np.maximum(ctrl_va, 1e-9), 0.0)
        frac = frac_c[:, None] * self.ctrl[None, :]
        vt_before = self.vt()
        self._remove(frac)
        self.jv_sold += amt
        return amt * px, (frac * vt_before).sum(1), amt

    def cashout(self, mask, e):
        """Cash-out at maturity on controlled direct debt (Green / Amber, not crisis): new loan at the G15
        target LTV on the maturing tranche's true value less the old balance."""
        lstate = np.where(e >= 2, 1, 0)
        av = np.array([AVAIL["N"], AVAIL["T"]])[lstate]
        tgt = np.array([CASHOUT_LTV[s] for s in self.sec])
        Dm = self.D * B.MATURITY_PA / 4 * self.ctrl[None, :] * self.direct[None, :]
        Vm = self.GT * np.where(self.D > 1e-12, Dm / np.maximum(self.D, 1e-12), 0.0)
        extra = np.maximum(av[:, None] * tgt[None, :] * Vm - Dm, 0.0) * mask[:, None]
        self.D = self.D + extra
        self.co_debt = self.co_debt + extra
        return extra.sum(1)

    def sell_sleeve(self, sid, amt_rep, px):
        """Sell amt_rep of reported NAV of sleeve sid at px (buyer assumes pro-rata unfunded)."""
        j = self.ids.index(sid)
        va = np.maximum(self.va()[:, j], 1e-9)
        frac = np.clip(amt_rep / va, 0.0, 1.0)
        f = np.zeros((self.n, self.S))
        f[:, j] = frac
        vt_before = self.vt()[:, j]
        self._remove(f)
        return frac * va * px, frac * vt_before

    def enr_sell(self, amt_rep, px):
        """ENR SELL: fund-held levered upstream out of ENR_CE; the remaining sleeve's oil elasticity falls."""
        j = self.ids.index("ENR_CE")
        va0 = float(B.SLEEVES[j]["nav"])
        eps_before = self.eps_eq[j]
        cash, vgive = self.sell_sleeve("ENR_CE", np.full(self.n, amt_rep), px)
        rem = max(va0 - amt_rep, 1e-9)
        self.eps_eq = self.eps_eq.copy()
        self.eps_eq[j] = max((eps_before * va0 - B.LEV_UP_ELAST * amt_rep) / rem, 0.0)
        self.eps_a = self.eps_eq * (1 - self.ltv0)
        return cash, vgive

    def red_sale(self, need, e, crisis, depth, ok):
        """Forced (red) sale of RA stakes pro rata to reported NAV at state prices, within remaining depth."""
        ps = self.price_state(e, crisis)
        px = np.stack([np.array([SALE_PX[s][k] for s in self.ids]) for k in range(3)])[ps]   # (n, S)
        va = np.maximum(self.va(), 0.0)
        tot = va.sum(1)
        avg_px = np.where(tot > 1e-9, (px * va).sum(1) / np.maximum(tot, 1e-9), 0.5)
        amt = np.where(ok, np.minimum(np.minimum(tot, np.maximum(depth, 0.0)), need / np.maximum(avg_px, 1e-9)), 0.0)
        frac = np.where(tot > 1e-9, amt / np.maximum(tot, 1e-9), 0.0)
        cash = (frac[:, None] * va * px).sum(1)
        vt_before = self.vt().sum(1)
        self._remove(np.broadcast_to(frac[:, None], (self.n, self.S)))
        return cash, amt, frac * vt_before

    def emergency(self, frac):
        """Emergency pro-rata private sale at 50% (engine convention)."""
        va = np.maximum(self.va(), 0.0).sum(1)
        self._remove(np.broadcast_to(frac[:, None], (self.n, self.S)))
        return frac * va

    def add_commitments(self, k_ra):
        self.U = self.U + k_ra[:, None] * self.commit[None, :]

    # ------------------------------------------------------------------ stress proxy state
    def proxy_state(self):
        return dict(ra_va=np.maximum(self.va(), 0.0), ra_gt=self.GT.copy(), ra_d=self.D.copy(), ra_u=self.U.copy())


def ra_proxy_paths(st: dict, theta: float, T: int, crm: np.ndarray, pace_m: np.ndarray, cut: np.ndarray,
                   availability=True, ext=None, fund_module="waterfall"):
    """Monthly RA flows under s*(theta) from each path's current RA state (vectorised mirror of
    ra_ladder.ra_leg canonical mode). Returns net outflow (n, T) and reported NAV (n, T)."""
    comp = B.ra_theta(theta, availability=availability, ext=ext)
    ext_post = B.EXT_N if ext is None else ext
    va = st["ra_va"].copy()
    gt0 = st["ra_gt"].copy()
    D = st["ra_d"].copy()
    U = st["ra_u"].copy()
    n, S = va.shape
    sl = B.SLEEVES
    sec = [s["sector"] for s in sl]
    inc = np.array([s["inc"] for s in sl])
    real_d = np.array([s["real_d"] for s in sl])
    direct = np.array([s["direct"] for s in sl])
    ltv0 = np.array([s["ltv"] for s in sl])
    lam = np.array([s["lam"] for s in sl])
    lag = np.array([s["lag"] for s in sl], dtype=int)
    commit = np.array([s["commit"] for s in sl])
    commit = commit / commit.sum()
    m_inc = np.array([comp["inc"][s] for s in sec])
    v_tot = np.array([comp["true"][s] for s in sec])
    ltvS = np.array([comp["ltv"][s] for s in sec])
    ltvN = np.array([B.LTV_N[s] for s in sec])
    # reported quarterly changes on the ramp (RAME), per sleeve
    rep_q = np.zeros((13, S))
    for j in range(S):
        lv = [1.0 + v_tot[j] * min(q, 4) / 4.0 for q in range(0, 13)]
        rt = [lv[q] / lv[q - 1] - 1.0 for q in range(1, 13)]
        rl = [0.0] * lag[j] + rt
        prev, lvl = 0.0, 1.0
        for q in range(12):
            prev = lam[j] * prev + (1 - lam[j]) * rl[q]
            new = lvl * (1 + prev)
            rep_q[q + 1, j] = new - lvl
            lvl = new
    gr0 = va + D
    r0 = np.where(D > 1e-12, gt0 / np.maximum(D, 1e-12), 0.0)      # true collateral per $ of debt at proxy start
    net = np.zeros((n, T))
    navr = np.zeros((n, T))
    mo = lambda r: 1.0 - (1.0 - np.minimum(r, 0.95)) ** (1.0 / 12.0)  # noqa: E731
    tv_prev = 0.0
    for t in range(T):
        if t % 3 == 0 and t > 0 and t // 3 <= 12:
            va = va + gr0 * rep_q[t // 3][None, :]
        in_cr = t < comp["crisis_months"]
        incm = inc[None, :] * (m_inc[None, :] if in_cr else 1.0) * np.maximum(va, 0.0) / 12
        rea = mo((comp["exit_factor"] if in_cr else 1.0) * real_d)[None, :] * np.maximum(va, 0.0)
        crate = mo(0.28 * (comp["call_mult"] if t < 24 else 1.0))
        calls = crate * U
        U = U - calls
        k = pace_m * np.where(cut & (t >= 2) & crm[t], 0.25, 1.0) * 0.1
        U = U + k[:, None] * commit[None, :]
        tv = v_tot * min(1.0, (t + 1) / 12.0)
        stressed = t < 24
        ltvmax = ltvS if stressed else ltvN
        av = (comp["avail"] if stressed else B.AVAIL_N) if availability else 1.0
        ex = comp["ext"] if stressed else ext_post
        Dm = D * B.MATURITY_PA / 12
        Vm = Dm * r0 * (1 + tv[None, :])
        refi = av * np.minimum(Dm, ltvmax[None, :] * Vm) + (1 - av) * ex * Dm
        gap = np.maximum(Dm - refi, 0.0)
        cure = np.where(direct[None, :], gap, 0.0)
        fgap = np.where(direct[None, :], 0.0, gap)
        prot = stop = np.zeros_like(gap)
        rem = np.zeros_like(gap)
        if fund_module == "upper":
            cure = cure + fgap
        elif fund_module == "waterfall":
            prot = np.minimum(fgap, U)
            U = U - prot
            rem = fgap - prot
            stop = np.minimum(rem, incm + rea)
            rem = rem - stop
        D = D - cure - prot - stop - rem
        va = va + calls + cure + prot - rea - 0.25 * rem
        net[:, t] = (calls + cure + prot - incm - rea + stop).sum(1)
        navr[:, t] = np.maximum(va, 0.0).sum(1)
        tv_prev = tv
    return net, navr
