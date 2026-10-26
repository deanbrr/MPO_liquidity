"""Component 3: the multi-period optimizer (one LP on in-sample scenarios, every stakeholder objective).

Decisions are non-anticipative (one value for every path): secondary sales of each private unit at the start of
years 1-3, today's liquid-risk allocation and reserve, five years of commitments / deployments per private bucket,
new term debt and NAV-facility draw today, and a synthetic-beta notional. Recourse is need-based funding only, so
no path's future can be traded on (the prototype's verification found such leaks; examples/mpo_v2 verify_math):
  Kp[j,t]   reserve (cash + Treasury composite) at the end of year t, earning its world's expected return
  Km[j,t]   liquid-risk assets sold to fund needs, carried at their expected return plus a sale cost, so the
            choice of funding source never depends on a path's realized future
  phi[j,t]  forced secondary sale of a pro-rata slice of the private book at the stressed bid (a red event)
  u[j,t]    reserve-floor shortfall (heavily penalized safety valve)
Rows per scenario and year: the reserve ledger (private flows, calls, owner draw on opening NAV, interest, overlay
margin, planned-sale proceeds, deployments), the NAV identity, liquid-sale capacity, and the reserve floor
(floor_target x NAV plus initial margin). Today: the budget, leverage, recourse-debt, NAV-facility LTV and
overcommitment limits, IC ranges, secondary-market depth and the PE program (user, 2026-10-25).

Goal wealth: W~_j = NAV_j,5 + sum_t draw_j,t x A_j,t (draws accrued to year 5 at the status-quo return; FD 4.2).
Objectives (tpp.stakeholders picks the default per lens): GBO (minimum bPOE of the 10% miss, examples/mpo_v2
optim.gbo, with a CRRA tie-break), CRRA utility, mean-CVaR, liquidity risk at a return floor, maximum mean.
Epsilon constraints let every lens carry the others' limits: buffered P(goal) floor, forced-sale CVaR, return floor.
"""
from __future__ import annotations

import time

import highspy
import numpy as np
import scipy.sparse as sp

from .buckets import BY_ID, LIQUID_RISK
from .legacy import bpoe
from .plan import STATES, Plan

INF = highspy.kHighsInf


class Cols:
    def __init__(self):
        self.n = 0
        self.lb, self.ub, self.names = [], [], {}

    def add(self, name, shape, lb=0.0, ub=INF):
        shape = tuple(np.atleast_1d(shape).tolist()) if not isinstance(shape, tuple) else shape
        k = int(np.prod(shape)) if shape else 1
        idx = np.arange(self.n, self.n + k).reshape(shape) if shape else np.array(self.n)
        self.lb.append(np.broadcast_to(np.asarray(lb, float), shape).ravel().copy())
        self.ub.append(np.broadcast_to(np.asarray(ub, float), shape).ravel().copy())
        self.n += k
        self.names[name] = idx
        return idx


class Rows:
    def __init__(self):
        self.r, self.c, self.v = [], [], []
        self.lo, self.hi = [], []
        self.n = 0
        self.tags = {}

    def add(self, tag, cols, vals, lo, hi, nrows=1):
        """Add `nrows` rows; cols/vals are arrays (nrows, k) or lists of per-row arrays."""
        start = self.n
        if nrows == 1 and np.ndim(cols) == 1:
            cols = np.asarray(cols)[None, :]
            vals = np.asarray(vals, float)[None, :]
        cols = np.asarray(cols)
        vals = np.broadcast_to(np.asarray(vals, float), cols.shape)
        rr = np.repeat(np.arange(start, start + nrows), cols.shape[1])
        keep = vals.ravel() != 0
        self.r.append(rr[keep])
        self.c.append(cols.ravel()[keep])
        self.v.append(vals.ravel()[keep])
        self.lo.append(np.broadcast_to(np.asarray(lo, float), (nrows,)).copy())
        self.hi.append(np.broadcast_to(np.asarray(hi, float), (nrows,)).copy())
        self.n += nrows
        self.tags[tag] = np.arange(start, start + nrows)
        return self.tags[tag]

    def triplets(self, tag_rows, cols, vals):
        """Append extra coefficients to existing rows (same-length arrays)."""
        cols = np.asarray(cols).ravel()
        vals = np.asarray(vals, float).ravel()
        rows = np.asarray(tag_rows).ravel()
        keep = vals != 0
        self.r.append(rows[keep])
        self.c.append(cols[keep])
        self.v.append(vals[keep])


class TPPModel:
    """settings keys (all optional; defaults from config/assumptions.json):
    floor_target, lev_cap, recourse_cap, navf_ltv_max, overcommit, range_band, pace_mult, allow_other_sales,
    pe_program_enabled / total / years / basis / selection, even_program, beta_max, allow_debt, allow_beta,
    p_goal_min, forced_eps, ret_min, liquid_sale_cost, treasury_share."""

    def __init__(self, S, P, settings: dict | None = None, log=None):
        self.S, self.P = S, P
        self.st = dict(settings or {})
        self.log = log or (lambda s: None)
        t0 = time.time()
        self._data()
        self._build()
        self.build_time = time.time() - t0
        self.h = None

    # ------------------------------------------------------------------ data
    def _g(self, key, default):
        return self.st.get(key, default)

    def _data(self):
        S, P, bk = self.S, self.P, self.S.book
        m, K = S.m, len(bk.units)
        self.m, self.K = m, K
        self.W0, self.Wstar = bk.W0, bk.Wstar
        self.p = S.prob / S.prob.sum()
        lev = lambda X: X[:, ::4]                                                   # (m, 21, k) -> (m, 6, k)
        yf = lambda X: X.reshape(X.shape[0], 5, 4, X.shape[-1]).sum(2)              # (m, 20, k) -> (m, 5, k)
        self.uV = lev(S.uV)                                                         # (m, 6, K)
        self.uNF = yf(S.uD) - yf(S.uC)                                              # (m, 5, K)
        self.ubid = S.ubid                                                          # (m, 6, K)
        self.nav0 = np.array([u.nav0 for u in bk.units]) * (1 - S.shock["private_markdown"])
        self.unf0 = np.array([u.unf0 for u in bk.units])
        self.expo0 = np.array([u.exposure0 for u in bk.units])
        self.is_fund_u = np.array([BY_ID[u.bucket].is_fund for u in bk.units])
        self.tb = S.tpl_buckets
        self.Tb = len(self.tb)
        self.tV = S.tV.astype(float)                                                # (5, m, 6, Tb)
        self.tNF = np.stack([yf(S.tD[k].astype(float)) - yf(S.tC[k].astype(float)) for k in range(5)])
        self.tU = S.tU.astype(float)
        self.is_fund_t = S.tpl_is_fund
        self.LR = [b for b in LIQUID_RISK]
        self.x0 = np.array([bk.liquid.get(b, 0.0) for b in self.LR])
        self.G = np.stack([S.G[b][:, ::4] for b in self.LR], -1)                   # (m, 6, nLR)
        self.res0 = float(bk.liquid.get("CASH", 0.0) + bk.liquid.get("TREASURY", 0.0))
        # reserve composite: expected return per world (deterministic: no funding choice depends on a path)
        ts = float(self._g("treasury_share", bk.liquid.get("TREASURY", 0.0) / max(self.res0, 1e-9)))
        self.treasury_share = min(max(ts, 0.0), 1.0)
        ann = lambda g: g[:, 4::4] / g[:, :-4:4] - 1.0                              # (m, 5) annual returns
        rr = self.treasury_share * ann(S.G["TREASURY"]) + (1 - self.treasury_share) * ann(S.G["CASH"])
        self.r_res = np.zeros((m, 5))
        lr_w = self.x0 / max(self.x0.sum(), 1e-9)
        r_lr = np.einsum("mtk,k->mt", self.G[:, 1:, :] / self.G[:, :-1, :] - 1.0, lr_w)
        self.c_neg = np.zeros((m, 5))
        sale_cost = float(self._g("liquid_sale_cost", P.get("objective.liquid_sale_cost")))
        for w in range(3):
            mk = S.world == w
            self.r_res[mk] = rr[mk].mean()
            self.c_neg[mk] = r_lr[mk].mean() + sale_cost
        self.d = S.draw                                                             # (m, 5)
        self.A = S.accrual()                                                        # (m, 6)
        bsp = np.asarray(P.get("overlay.beta_fin_spread"), float)
        imr = np.asarray(P.get("overlay.im_rate"), float)
        eq = S.eq_excess_q.reshape(m, 5, 4)
        self.beta_pl = eq.sum(2) - bsp[S.cls_q].reshape(m, 5, 4).mean(2)          # per $ notional per year
        self.im = np.concatenate([imr[S.cls_y[:, :1]], imr[S.cls_y[:, 1:]]], 1)     # (m, 6)
        self.rf_fin = S.rf_fin
        self.term_rate = S.rf_fin + float(P.get("corporate_finance.term_spread"))
        self.navf_rate = S.rf_fin + float(P.get("corporate_finance.navf_spread"))
        self.oid = float(P.get("corporate_finance.navf_oid"))
        self.tc = float(P.get("trading.tc_liquid"))
        # status-quo private book continuation (for the forced-sale slice): value and net flow of the book as held
        # at the end of year t' (units + status-quo commitments made by t'), for later years s >= t'
        pace = np.array([bk.pacing_sq.get(b, 0.0) for b in self.tb])
        cont_v = np.zeros((6, m, 6))
        cont_f = np.zeros((6, m, 6))
        for tp in range(6):
            v = self.uV.sum(2).copy()
            f = np.zeros((m, 6))
            f[:, 1:] = self.uNF.sum(2)
            for tau in range(min(tp, 4) + 1):
                v += (self.tV[tau] * pace[None, None, :]).sum(2)
                f[:, 1:] += (self.tNF[tau] * pace[None, None, :]).sum(2)
            cont_v[tp], cont_f[tp] = v, f
        self.cont_v, self.cont_f = cont_v, cont_f
        rho_px = np.einsum("mk,mk->m", self.uV[:, 0, :], self.ubid[:, 0, :]) / np.maximum(self.uV[:, 0, :].sum(1), 1e-9)
        disc = float(P.get("liquidity.forced_sale_extra_discount"))
        self.pf = np.zeros((m, 6))
        for t in range(6):
            w = self.uV[:, t, :]
            self.pf[:, t] = (w * self.ubid[:, t, :]).sum(1) / np.maximum(w.sum(1), 1e-9) * (1 - disc)
        self.pf[:, 0] = rho_px * (1 - disc)
        self.depth = np.asarray(P.get("trading.lp_depth_year_bn"), float)
        rev_av = np.asarray(self._g("revolver_avail", P.get("corporate_finance.revolver_avail")), float)
        rev_cap = float(self._g("revolver_signed_bn", P.get("corporate_finance.revolver_signed_bn")))
        self.rev_rate = S.rf_fin + float(P.get("corporate_finance.revolver_spread"))
        self.rev_cap = rev_cap * rev_av[S.cls_y[:, 1:]]                             # (m, 5) at each year end
        self.rev0 = float(bk.revolver_drawn0)

    # ------------------------------------------------------------------ build
    def _build(self):
        st, P = self.st, self.P
        m, K, Tb = self.m, self.K, self.Tb
        nLR = len(self.LR)
        bk = self.S.book
        cl = Cols()
        # ---- first stage
        sell_ub = np.ones((K, 3))
        prog_on = bool(self._g("pe_program_enabled", P.get("pe_program.enabled")))
        prog_sel = self._g("pe_program_selection", P.get("pe_program.selection"))
        allow_other = bool(self._g("allow_other_sales", True))
        for k, u in enumerate(bk.units):
            if u.pe_program and prog_on and prog_sel == "underperformers" and u.part == "core":
                sell_ub[k] = 0.0
            if not u.pe_program and not allow_other:
                sell_ub[k] = 0.0
        if not prog_on and not bool(self._g("allow_pe_sales", True)):
            for k, u in enumerate(bk.units):
                if u.pe_program:
                    sell_ub[k] = 0.0
        self.Sx = cl.add("sell", (K, 3), 0.0, sell_ub)
        band = list(self._g("range_band", P.get("constraints.range_band")))
        tot0 = float(self.x0.sum() + self.res0)
        x_lo = np.where(self.x0 > 0, band[0] * self.x0, 0.0)
        x_hi = np.where(self.x0 > 0, band[1] * self.x0, 0.05 * tot0)
        for b, (lo, hi) in (self._g("x_bounds", {}) or {}).items():
            if b in self.LR:
                x_lo[self.LR.index(b)], x_hi[self.LR.index(b)] = lo, hi
        self.X = cl.add("x", (nLR,), x_lo, x_hi)
        self.XP = cl.add("xp", (nLR,))
        self.XM = cl.add("xm", (nLR,))
        self.R0 = cl.add("r0", ())
        pace = np.array([bk.pacing_sq.get(b, 0.0) for b in self.tb])
        self.pace = pace
        mult = list(self._g("pace_mult", P.get("pacing.mult_range")))
        entry = float(self._g("new_strategy_entry_bn", 0.3))            # a strategy with little or no pacing today
        c_lo = np.repeat((mult[0] * pace)[:, None], 5, 1)
        c_hi = np.repeat((mult[1] * pace + entry)[:, None], 5, 1)
        self.Cc = cl.add("commit", (Tb, 5), c_lo, c_hi)
        lev_cap = float(self._g("lev_cap", P.get("constraints.lev_cap")))
        allow_debt = bool(self._g("allow_debt", True))
        allow_beta = bool(self._g("allow_beta", True))
        self.DT = cl.add("term", (3,), 0.0, INF if allow_debt else 0.0)          # term draws at the start of years 1-3
        self.DN = cl.add("navf", (), 0.0, INF if allow_debt else 0.0)
        self.BETA = cl.add("beta", (), 0.0, float(self._g("beta_max", P.get("overlay.beta_max_bn"))) if allow_beta else 0.0)
        self.NAV0 = cl.add("nav0", (), -INF, INF)
        # ---- state-contingent copies of the later dated decisions. A decision taken at the start of a later year
        # follows what has been observed by then (the year-end market class: benign / exit drought / stress):
        # commitments the state at that year end; the year-2 sale and debt draw the year-1 state; the year-3 ones the
        # year-1 and year-2 states together, so the year-3 tranche can make up what year 2 did and the PE program's
        # total and the debt cap hold on every path. Each scenario uses its context's copy: the plan adapts without
        # seeing the future. A context seen in fewer than n_min scenarios shares the most populous related context's
        # copy; contingent=False gives one schedule for every path (the fixed-schedule LP).
        NS = 3
        self.contingent_on = cont = bool(self._g("contingent", True))
        n_min = int(self._g("contingent_min_scenarios", 24))
        cls = np.asarray(self.S.cls_y, int)
        ctx_sd = [np.zeros(m, int), cls[:, 1], cls[:, 1] * NS + cls[:, 2]]            # sales and debt, tau = 0, 1, 2
        ctx_c = [np.zeros(m, int)] + [cls[:, tau] for tau in range(1, 5)]           # commitments, tau = 0..4
        n_sd = [1, NS, NS * NS]

        def ctx_map(ctx, n, parent=None):
            cnt = np.bincount(ctx, minlength=n)
            mp = np.arange(n)
            if not cont:
                return np.zeros(n, int)
            for k_ in range(n):
                if cnt[k_] < n_min:
                    group = [j for j in range(n) if parent is None or parent[j] == parent[k_]]
                    mp[k_] = max(group, key=lambda j: cnt[j])
            return mp

        map_sd = [np.zeros(1, int), ctx_map(ctx_sd[1], NS), ctx_map(ctx_sd[2], NS * NS, np.repeat(np.arange(NS), NS))]
        map_c = [np.zeros(1, int)] + [ctx_map(ctx_c[tau], NS) for tau in range(1, 5)]
        freq_sd = [np.ones(1)] + [np.bincount(ctx_sd[tau], weights=self.p, minlength=n_sd[tau]) for tau in (1, 2)]
        freq_c = [np.ones(1)] + [np.bincount(ctx_c[tau], weights=self.p, minlength=NS) for tau in range(1, 5)]
        ex_S1 = cl.add("sell_s1", (K, NS - 1), 0.0, np.repeat(sell_ub[:, 1:2], NS - 1, 1))
        ex_S2 = cl.add("sell_s2", (K, NS * NS - 1), 0.0, np.repeat(sell_ub[:, 2:3], NS * NS - 1, 1))
        ex_D1 = cl.add("term_s1", (NS - 1,), 0.0, INF if allow_debt else 0.0)
        ex_D2 = cl.add("term_s2", (NS * NS - 1,), 0.0, INF if allow_debt else 0.0)
        ex_C = cl.add("commit_s", (Tb, 4, NS - 1), np.repeat(c_lo[:, 1:, None], NS - 1, 2),
                      np.repeat(c_hi[:, 1:, None], NS - 1, 2))
        S_col = lambda tau, c: self.Sx[:, tau] if c == 0 else (ex_S1 if tau == 1 else ex_S2)[:, c - 1]
        D_col = lambda tau, c: self.DT[tau] if c == 0 else (ex_D1 if tau == 1 else ex_D2)[c - 1]
        C_col = lambda tau, c: self.Cc[:, tau] if c == 0 else ex_C[:, tau - 1, c - 1]
        # per context: the column of the copy it uses
        self.SxI = [np.stack([S_col(tau, int(map_sd[tau][k_])) for k_ in range(n_sd[tau])], 1) for tau in range(3)]
        self.DTI = [np.array([D_col(tau, int(map_sd[tau][k_])) for k_ in range(n_sd[tau])]) for tau in range(3)]
        self.CcI = [np.stack([C_col(tau, int(map_c[tau][k_])) for k_ in range(len(map_c[tau]))], 1) for tau in range(5)]
        self.ctx_sd, self.ctx_c, self.map_sd, self.map_c = ctx_sd, ctx_c, map_sd, map_c
        self.freq_sd, self.freq_c = freq_sd, freq_c
        copies_sd = [sorted(set(int(c) for c in map_sd[tau])) for tau in range(3)]
        copies_c = [sorted(set(int(c) for c in map_c[tau])) for tau in range(5)]
        # the synthetic beta held in years 2-5 follows the market class at the start of the year, like the other
        # later decisions (equity volatility is higher in stress at the same expected return); fixed schedule: one
        # beta for all five years
        ctx_b = [np.zeros(m, int)] + [cls[:, t] for t in range(1, 5)]
        map_b = [np.zeros(1, int)] + [ctx_map(ctx_b[t], NS) for t in range(1, 5)]
        freq_b = [np.ones(1)] + [np.bincount(ctx_b[t], weights=self.p, minlength=NS) for t in range(1, 5)]
        beta_ub = float(self._g("beta_max", P.get("overlay.beta_max_bn"))) if allow_beta else 0.0
        self.cont_b = cont_b = cont and bool(self._g("contingent_beta", False))   # off by default: fits noise
        ex_B = cl.add("beta_s", (4, NS), 0.0, beta_ub) if cont_b else None
        B_col = lambda t, c: self.BETA if (t == 0 or not cont_b) else ex_B[t - 1, c]
        self.BI = [np.array([self.BETA])] + [np.array([B_col(t, int(map_b[t][k_])) for k_ in range(NS)]) for t in range(1, 5)]
        self.ctx_b, self.map_b, self.freq_b = ctx_b, map_b, freq_b
        copies_b = [[0]] + [sorted(set(int(c) for c in map_b[t])) for t in range(1, 5)]
        beta_cols = sorted({int(self.BETA)} | {int(B_col(t, c)) for t in range(1, 5) for c in copies_b[t]})
        # ---- recourse
        self.KP = cl.add("kp", (m, 5))
        self.KM = cl.add("km", (m, 5))
        self.PHI = cl.add("phi", (m, 5), 0.0, 1.0)
        use_rev = "REVOLVER" in list(self._g("waterfall", P.get("liquidity.waterfall")))
        self.RV = cl.add("rv", (m, 5), 0.0, self.rev_cap if use_rev else 0.0)        # revolver balance, year end
        self.U = cl.add("u", (m, 5))                                             # below the reserve target
        self.UH = cl.add("uh", (m, 5))                                           # below the hard floor (safety valve)
        self.NAV = cl.add("nav", (m, 5), -INF, INF)
        self.WT = cl.add("wt", (m,), -INF, INF)
        # objective auxiliaries
        self.ETA = cl.add("eta", (), -INF, INF)
        self.Z = cl.add("z", (m,))
        self.UT = cl.add("ut", (m,), -INF, INF)
        self.ETAF = cl.add("etaf", (), -INF, INF)
        self.ZF = cl.add("zf", (m,))
        self.ETAL = cl.add("etal", (), -INF, INF)
        self.ZL = cl.add("zl", (m,))
        self.cols = cl
        lb = np.concatenate(cl.lb)
        ub = np.concatenate(cl.ub)
        for tau in (1, 2):                                                         # copies no context uses stay at zero
            for c in range(n_sd[tau]):
                if c not in copies_sd[tau]:
                    idx = np.r_[np.ravel(S_col(tau, c)), np.atleast_1d(D_col(tau, c))]
                    lb[idx] = 0.0
                    ub[idx] = 0.0
        for tau in range(1, 5):
            for c in range(NS):
                if c not in copies_c[tau]:
                    lb[C_col(tau, c)] = 0.0
                    ub[C_col(tau, c)] = 0.0
                if cont_b and c not in copies_b[tau]:
                    lb[B_col(tau, c)] = 0.0
                    ub[B_col(tau, c)] = 0.0
        # opportunistic secondaries (a countercyclical mandate): in a stress year, when sellers need liquidity and
        # prices are low, LP-led and GP-led purchases may go up to the market's capacity, outside the program's
        # pacing range and yearly caps (rows below). Only a plan that sees the stress can use it: the fixed schedule
        # has one copy for every state and keeps the program's limits
        opp = bool(self._g("opportunistic_secondaries", P.get("pe_cycle.opportunistic_secondaries")))
        buy_cap = P.get("trading.buy_cap_year_bn")
        sec_fam = {f_: np.array([b.startswith(f_) for b in self.tb]) for f_ in ("SEC_LP", "SEC_GP")}
        is_sec = sec_fam["SEC_LP"] | sec_fam["SEC_GP"]
        opp_copy = lambda tau, c: opp and cont and tau >= 1 and c == 2 and int(map_c[tau][2]) == 2
        for tau in range(1, 5):
            if opp_copy(tau, 2) and 2 in copies_c[tau]:
                for f_, msk in sec_fam.items():
                    ub[np.asarray(C_col(tau, 2))[msk]] = float(buy_cap[f_])
        self.opp_secondaries = opp
        # every path's pair of later copies (year-2 by its year-1 state, year-3 by both): path-wise rows hold on each
        paths_sd = sorted({(int(map_sd[1][s1]), int(map_sd[2][s1 * NS + s2])) for s1 in range(NS) for s2 in range(NS)})
        nC = len(paths_sd)
        colS = lambda tau: self.SxI[tau][:, self.ctx_sd[tau]].T                    # (m, K): each scenario's copy

        def colC(tau, mask=None):
            A_ = self.CcI[tau] if mask is None else self.CcI[tau][mask]
            return A_[:, self.ctx_c[tau]].T

        colD = lambda tau: self.DTI[tau][self.ctx_sd[tau]]
        colB = lambda t: np.full(m, self.BETA) if t == 1 else self.BI[t - 1][self.ctx_b[t - 1]]   # beta held in year t
        R = Rows()
        Sx = self.Sx
        # ---- today
        bid0 = self.ubid[0, 0, :]                                                   # deterministic today
        coinv = ~self.is_fund_t
        # budget: r0 + sum x + deploy0 + tc (xp + xm) - sum s0 V0 bid0 - term - (1 - oid) navf = res0 + sum x0
        cols = np.r_[self.R0, self.X, self.Cc[coinv, 0], self.XP, self.XM, Sx[:, 0], self.DT[0], self.DN]
        vals = np.r_[1.0, np.ones(nLR), np.ones(coinv.sum()), self.tc * np.ones(2 * nLR), -self.nav0 * bid0, -1.0,
                     -(1 - self.oid)]
        R.add("budget", cols, vals, self.res0 + self.x0.sum(), self.res0 + self.x0.sum())
        R.add("xsplit", np.c_[self.X, self.XP, self.XM], np.array([1.0, -1.0, 1.0]), self.x0, self.x0, nrows=nLR)
        # NAV0 = r0 + sum x + sum (1 - s0) V0 + deploy0 - term_0 - navf - term0 - rev0
        debt0 = bk.term0 + bk.revolver_drawn0
        cols = np.r_[self.NAV0, self.R0, self.X, Sx[:, 0], self.Cc[coinv, 0], self.DT[0], self.DN]
        vals = np.r_[1.0, -1.0, -np.ones(nLR), self.nav0, -np.ones(coinv.sum()), 1.0, 1.0]
        R.add("nav0", cols, vals, self.nav0.sum() - debt0, self.nav0.sum() - debt0)
        # leverage: all planned term debt + navf + beta + debt0 <= (L - 1) NAV0 (planned draws count in full today)
        dt_c = np.array([[self.DT[0], D_col(1, c1), D_col(2, c2)] for c1, c2 in paths_sd])   # (nC, 3): every path's draws
        lev_rows = np.array([np.r_[d_, self.DN, bc, self.NAV0] for d_ in dt_c for bc in beta_cols])  # every path, every year's beta
        R.add("lev0", lev_rows, np.r_[1.0, 1.0, 1.0, 1.0, 1.0, -(lev_cap - 1.0)], -INF, -debt0, nrows=len(lev_rows))
        rc = float(self._g("recourse_cap", P.get("corporate_finance.recourse_cap")))
        R.add("recourse0", np.c_[dt_c, np.full(nC, self.NAV0)], np.r_[1.0, 1.0, 1.0, -rc], -INF, -debt0, nrows=nC)
        new_term_max = float(self._g("new_term_max_bn", INF))
        if new_term_max < INF:
            R.add("term_max", dt_c, np.ones(3), -INF, new_term_max, nrows=nC)
        # private capacity: fund commitments and co-invest / secondary deployments per year
        fund_t = self.is_fund_t
        agg = float(self._g("commit_agg_mult", 1.25))
        co_extra = float(self._g("coinvest_extra_bn", P.get("trading.buy_cap_year_bn")["COINVEST"]))
        for tau in range(5):
            for c in copies_c[tau]:
                ex = is_sec if opp_copy(tau, c) else np.zeros(Tb, bool)            # stress copy: secondaries apart
                fm, dm, col = fund_t & ~ex, ~fund_t & ~ex, np.asarray(C_col(tau, c))
                R.add(f"commit_cap{tau}_{c}", col[fm], np.ones(int(fm.sum())), -INF, agg * pace[fund_t].sum())
                R.add(f"deploy_cap{tau}_{c}", col[dm], np.ones(int(dm.sum())), -INF, pace[~fund_t].sum() + co_extra)
                for f_, msk in (sec_fam.items() if ex.any() else ()):
                    R.add(f"opp_cap{tau}_{c}_{f_}", col[msk], np.ones(int(msk.sum())), -INF, float(buy_cap[f_]))
        ltv = float(self._g("navf_ltv_max", P.get("corporate_finance.navf_ltv_max")))
        fund_v0 = self.nav0 * self.is_fund_u
        R.add("navf_ltv0", np.r_[self.DN, Sx[:, 0]], np.r_[1.0, ltv * fund_v0], -INF, ltv * fund_v0.sum())
        ovc = float(self._g("overcommit", P.get("constraints.overcommit")))
        cols = np.r_[Sx[:, 0], self.Cc[:, 0], self.NAV0]
        vals = np.r_[-(self.nav0 + self.unf0), np.ones(Tb), -ovc]
        R.add("overcommit0", cols, vals, -INF, -(self.nav0 + self.unf0).sum())
        ft = float(self._g("floor_target", P.get("liquidity.floor_target")))
        fh = float(self._g("floor_hard", P.get("liquidity.floor_hard")))
        self.floor, self.floor_hard = ft, fh
        R.add("reserve0", np.r_[self.R0, self.NAV0, self.BETA], np.r_[1.0, -ft, -self.im[0, 0]], 0.0, INF)
        R.add("sell_total", np.concatenate([np.c_[self.Sx[:, 0], S_col(1, c1), S_col(2, c2)] for c1, c2 in paths_sd]),
              np.ones(3), 0.0, 1.0, nrows=K * nC)
        depth = self.depth[1] * float(self._g("depth_mult", 1.0))
        for tau in range(3):
            cps = copies_sd[tau]
            R.add(f"depth{tau}", np.stack([S_col(tau, c) for c in cps]), self.nav0, -INF, depth, nrows=len(cps))
        # PE program: sum over PE units and tranches of the sold size = total (exposure or NAV basis)
        if prog_on:
            total = float(self._g("pe_program_total_bn", P.get("pe_program.total_bn")))
            years = int(min(self._g("pe_program_years", P.get("pe_program.years")), 3))
            basis = self._g("pe_program_basis", P.get("pe_program.basis"))
            size = self.expo0 if basis == "exposure" else self.nav0
            pe = np.array([u.pe_program for u in bk.units])
            # the program total holds on every path: one row per combination of later states
            cols = np.stack([np.concatenate([S_col(tau, (0, c1, c2)[tau])[pe] for tau in range(years)])
                             for c1, c2 in paths_sd])
            vals = np.concatenate([size[pe]] * years)
            R.add("program", cols, vals, total, total, nrows=nC)
            for tau in range(years, 3):
                lb[self.SxI[tau][pe].ravel()] = 0.0
                ub[self.SxI[tau][pe].ravel()] = 0.0
            if bool(self._g("even_program", False)):
                for tau in range(years):
                    cps = copies_sd[tau]
                    R.add(f"program{tau}", np.stack([S_col(tau, c)[pe] for c in cps]), size[pe], total / years,
                          total / years, nrows=len(cps))
        # ---- per scenario and year
        rows_nav, rows_res = [], []
        for t in range(1, 6):
            ti = t - 1
            # NAV[j,t] - Kp + Km - sum x G + sum_k V s(tau<=min(t,2)) - sum C TV + sum phi contV + DT + DN (1+r)^t = sum_k V
            taus = list(range(min(t, 2) + 1))
            Vt = self.uV[:, t, :]                                                   # (m, K)
            cols = [self.NAV[:, ti][:, None], self.KP[:, ti][:, None], self.KM[:, ti][:, None],
                    self.RV[:, ti][:, None], np.broadcast_to(self.X, (m, nLR))]
            vals = [np.ones((m, 1)), -np.ones((m, 1)), np.ones((m, 1)), np.ones((m, 1)), -self.G[:, t, :]]
            for tau in taus:
                cols.append(colS(tau))
                vals.append(Vt)
            for tau in range(min(t, 4) + 1):
                cols.append(colC(tau))
                vals.append(-self.tV[tau][:, t, :])
            for tp in range(1, t + 1):
                cols.append(self.PHI[:, tp - 1][:, None])
                vals.append(self.cont_v[tp][:, t][:, None])
            dts = np.stack([colD(k) for k in range(min(t, 2) + 1)], 1)             # term draws made by end of year t
            cols.append(np.c_[dts, np.full(m, self.DN)])
            vals.append(np.broadcast_to(np.r_[np.ones(dts.shape[1]), (1 + self.navf_rate) ** t], (m, dts.shape[1] + 1)))
            rows_nav.append(R.add(f"nav{t}", np.concatenate(cols, 1), np.concatenate(vals, 1), Vt.sum(1), Vt.sum(1),
                                  nrows=m))
            # reserve ledger
            NFt = self.uNF[:, ti, :]                                                # (m, K) flows in year t
            cols = [self.KP[:, ti][:, None], self.KM[:, ti][:, None], self.RV[:, ti][:, None]]
            vals = [np.ones((m, 1)), -np.ones((m, 1)), -np.ones((m, 1))]
            if t > 1:
                cols.append(self.RV[:, ti - 1][:, None])
                vals.append(np.full((m, 1), 1.0 + self.rev_rate))
            if t == 1:
                cols.append(np.broadcast_to(self.R0, (m, 1)))
                vals.append(-(1 + self.r_res[:, 0:1]))
                cols.append(np.broadcast_to(self.NAV0, (m, 1)))
                vals.append(self.d[:, 0:1])
            else:
                cols += [self.KP[:, ti - 1][:, None], self.KM[:, ti - 1][:, None], self.NAV[:, ti - 1][:, None]]
                vals += [-(1 + self.r_res[:, ti:ti + 1]), (1 + self.c_neg[:, ti:ti + 1]), self.d[:, ti:ti + 1]]
            for tau in range(min(t - 1, 2) + 1):                                    # units sold before year t
                cols.append(colS(tau))
                vals.append(NFt)
            if t <= 2:                                                              # planned sale at end of year t
                cols.append(colS(t))
                vals.append(-self.uV[:, t, :] * self.ubid[:, t, :])
            for tau in range(min(t - 1, 4) + 1):                                    # templates started before year t
                cols.append(colC(tau))
                vals.append(-self.tNF[tau][:, ti, :])
            if t <= 4:                                                              # deployments for year t + 1
                cols.append(colC(t, coinv))
                vals.append(np.ones((m, int(coinv.sum()))))
            # interest on term draws outstanding during year t; a draw at the end of year t brings cash in
            dts = np.stack([colD(k) for k in range(min(t - 1, 2) + 1)], 1)
            cols.append(dts)
            vals.append(np.full(dts.shape, self.term_rate))
            if t <= 2:
                cols.append(colD(t)[:, None])
                vals.append(-np.ones((m, 1)))
            cols.append(colB(t)[:, None])
            vals.append(-self.beta_pl[:, ti][:, None])
            cols.append(self.PHI[:, ti][:, None])
            vals.append(-(self.cont_v[t][:, t] * self.pf[:, t])[:, None])
            for tp in range(1, t):
                cols.append(self.PHI[:, tp - 1][:, None])
                vals.append(self.cont_f[tp][:, t][:, None])
            rhs = NFt.sum(1) - (self.rev0 * (1.0 + self.rev_rate) if t == 1 else 0.0)
            rows_res.append(R.add(f"res{t}", np.concatenate(cols, 1), np.concatenate(vals, 1), rhs, rhs, nrows=m))
            # liquid-sale capacity and the reserve floor
            R.add(f"cap{t}", np.c_[self.KM[:, ti][:, None], np.broadcast_to(self.X, (m, nLR))],
                  np.c_[np.ones((m, 1)), -self.G[:, t, :]], -INF, 0.0, nrows=m)
            # hard floor (as the simulator: restored by liquid sales, then forced sales) and the soft target
            # (as the simulator's year-end top-up from liquid sales: costly to miss, never a forced sale)
            R.add(f"floorh{t}", np.c_[self.KP[:, ti], self.NAV[:, ti], colB(t), self.UH[:, ti]],
                  np.c_[np.ones(m), -np.full(m, fh), -self.im[:, t], np.ones(m)], 0.0, INF, nrows=m)
            R.add(f"floor{t}", np.c_[self.KP[:, ti], self.NAV[:, ti], colB(t), self.U[:, ti]],
                  np.c_[np.ones(m), -np.full(m, ft), -self.im[:, t], np.ones(m)], 0.0, INF, nrows=m)
        self.rows_nav, self.rows_res = rows_nav, rows_res
        # goal wealth: WT - NAV5 - sum_t d_t A_t NAV_{t-1} = 0
        cols = [self.WT[:, None], self.NAV[:, 4][:, None], np.full((m, 1), self.NAV0)]
        vals = [np.ones((m, 1)), -np.ones((m, 1)), -(self.d[:, 0] * self.A[:, 1])[:, None]]
        for t in range(2, 6):
            cols.append(self.NAV[:, t - 2][:, None])
            vals.append(-(self.d[:, t - 1] * self.A[:, t])[:, None])
        R.add("wt", np.concatenate(cols, 1), np.concatenate(vals, 1), 0.0, 0.0, nrows=m)
        # CVaR of the goal miss X = (W* - WT)/W0:  z_j >= X_j - eta  ->  z_j + WT_j/W0 + eta >= W*/W0
        R.add("zrow", np.c_[self.Z, self.WT, np.full(m, self.ETA)], np.c_[np.ones(m), np.full(m, 1 / self.W0),
              np.ones(m)], self.Wstar / self.W0, INF, nrows=m)
        self.row_cvar = R.add("cvar", np.r_[self.ETA, self.Z], np.r_[1.0, self.p], -INF, INF)
        # forced-sale CVaR (liquidity appetite): zf_j >= sum_t phi_j,t contV_t - etaf
        cols = [self.ZF[:, None], np.full((m, 1), self.ETAF)] + [self.PHI[:, t - 1][:, None] for t in range(1, 6)]
        vals = [np.ones((m, 1)), np.ones((m, 1))] + [-self.cont_v[t][:, t][:, None] for t in range(1, 6)]
        R.add("zfrow", np.concatenate(cols, 1), np.concatenate(vals, 1), 0.0, INF, nrows=m)
        self.row_fcvar = R.add("fcvar", np.r_[self.ETAF, self.ZF], np.r_[1.0, self.p], -INF, INF)
        # mean wealth row (return floor / STRETCH tie-break)
        self.row_mean = R.add("mean", self.WT, self.p, -INF, INF)
        # lower-tail CVaR of wealth (mean-CVaR objective): zl_j >= etal - WT_j/W0
        R.add("zlrow", np.c_[self.ZL, self.WT, np.full(m, self.ETAL)], np.c_[np.ones(m), np.full(m, 1 / self.W0),
              -np.ones(m)], 0.0, INF, nrows=m)
        # depth guard (examples/mpo_v2 H10a): CVaR10 of WT/W0 no worse than the status quo's minus delta; inactive
        # until apply_depth_guard sets its bound
        self.depth_alpha = 0.10
        self.row_depth = R.add("depth", np.r_[self.ETAL, self.ZL], np.r_[1.0, -self.p / self.depth_alpha], -INF, INF)
        # CRRA tangents on WT/W0
        self.gamma = float(self._g("risk_aversion", 3.0))
        lo_w, hi_w = P.get("objective.crra_w_range")
        wk = np.geomspace(lo_w, hi_w, int(P.get("objective.crra_tangents")))
        g = self.gamma
        Uf = (lambda w: np.log(w)) if abs(g - 1) < 1e-9 else (lambda w: w ** (1 - g) / (1 - g))
        Ud = lambda w: w ** (-g)
        for i, w in enumerate(wk):
            R.add(f"util{i}", np.c_[self.UT, self.WT], np.c_[np.ones(m), np.full(m, -Ud(w) / self.W0)], -INF,
                  Uf(w) - Ud(w) * w, nrows=m)
        self.Uf = Uf
        self.rows = R
        A = sp.csr_matrix((np.concatenate(R.v), (np.concatenate(R.r), np.concatenate(R.c))), shape=(R.n, cl.n))
        A.sum_duplicates()
        self.A_mat = A
        self.lb, self.ub = lb, ub
        self.rlb, self.rub = np.concatenate(R.lo), np.concatenate(R.hi)
        self.nvar, self.nrow = cl.n, R.n
        # epsilon constraints from the settings
        self.eps = {}

    # ------------------------------------------------------------------ solve plumbing
    def highs(self):
        if self.h is not None:
            return self.h
        h = highspy.Highs()
        h.setOptionValue("output_flag", False)
        h.setOptionValue("threads", 1)
        h.setOptionValue("random_seed", 0)
        h.setOptionValue("primal_feasibility_tolerance", 1e-7)
        h.setOptionValue("dual_feasibility_tolerance", 1e-7)
        A = self.A_mat.tocsc()
        lp = highspy.HighsLp()
        lp.num_col_, lp.num_row_ = self.nvar, self.nrow
        lp.col_cost_ = np.zeros(self.nvar)
        lp.col_lower_, lp.col_upper_ = self.lb, self.ub
        lp.row_lower_, lp.row_upper_ = self.rlb, self.rub
        lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
        lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = A.indptr, A.indices, A.data
        h.passModel(lp)
        self.h = h
        self.cost = np.zeros(self.nvar)
        return h

    def set_cost(self, c):
        h = self.highs()
        idx = np.flatnonzero(c != self.cost)
        if len(idx):
            h.changeColsCost(len(idx), idx.astype(np.int32), c[idx].astype(float))
            self.cost = c.copy()

    def set_row(self, r, lo, hi):
        self.highs().changeRowBounds(int(np.atleast_1d(r)[0]), float(lo), float(hi))

    def run(self, name):
        h = self.highs()
        h.setOptionValue("solver", "ipm")
        h.setOptionValue("run_crossover", "on")
        t0 = time.time()
        h.run()
        st = h.getModelStatus()
        ok = st == highspy.HighsModelStatus.kOptimal
        sol = h.getSolution()
        x = np.array(sol.col_value) if ok else None
        y = np.array(sol.row_dual) if ok else None
        rc = np.array(sol.col_dual) if ok else None
        rec = {"name": name, "status": h.modelStatusToString(st), "time_s": time.time() - t0, "cols": self.nvar,
               "rows": self.nrow, "nnz": int(self.A_mat.nnz),
               "obj": float(h.getInfo().objective_function_value) if ok else None}
        self.log(f"  LP {name}: {rec['status']} {rec['time_s']:.2f}s")
        return x, y, rc, rec

    # ------------------------------------------------------------------ objectives
    def _penalty(self):
        c = np.zeros(self.nvar)
        pen = float(self.P.get("objective.floor_breach_cost"))
        c[self.U.ravel()] = pen * np.repeat(self.p, 5) / self.W0                 # below target: costly, not fatal
        c[self.UH.ravel()] = 100.0 * np.repeat(self.p, 5) / self.W0              # below the hard floor: never
        # revolver after liquid sales (the Liquidity group's waterfall): an ordering charge, not a wealth cost
        order = np.maximum(self.c_neg - self.rev_rate, 0.0) + 0.01
        c[self.RV.ravel()] = (order * self.p[:, None]).ravel() / self.W0
        # forced sales are a last resort, never a trade: without this charge the LP would "force-sell" private
        # holdings on paths where their marks later fall by more than the discount (a look-ahead leak)
        for t in range(1, 6):
            c[self.PHI[:, t - 1]] += 2.0 * self.p * self.cont_v[t][:, t] / self.W0
        return c

    def obj_mean(self):
        c = self._penalty()
        c[self.WT] = -self.p / self.W0
        return c

    def obj_util(self):
        c = self._penalty()
        c[self.UT] = -self.p
        return c

    def obj_liquidity(self):
        c = self._penalty()
        for t in range(1, 6):
            c[self.PHI[:, t - 1]] += self.p * self.cont_v[t][:, t] / self.W0
        c[self.KM.ravel()] += 0.02 * np.repeat(self.p, 5) / self.W0
        c[self.WT] = -1e-3 * self.p / self.W0
        return c

    def obj_mean_cvar(self, lam=1.0, alpha=0.10):
        c = self._penalty()
        c[self.WT] = -self.p / self.W0
        c[self.ETAL] = -lam
        c[self.ZL] = lam * self.p / alpha
        return c

    def apply_eps(self, p_goal_min=None, forced_eps=None, ret_min=None):
        """Epsilon constraints that carry other stakeholders' limits."""
        h = self.highs()
        if p_goal_min:
            # buffered P(goal) >= p_min  <=>  bPOE(X) <= 1 - p_min  <=>  CVaR_{p_min}(X) <= 0
            self._set_cvar_level(max(1.0 - float(p_goal_min), 1e-4))
            self.set_row(self.row_cvar, -INF, 0.0)
            self.eps["p_goal_min"] = p_goal_min
        if forced_eps:
            thr = float(self.P.get("liquidity.red_event_threshold_bn"))
            eps = float(forced_eps)
            h.changeCoeff(int(self.row_fcvar[0]), int(self.ETAF), 1.0)
            for j, zj in enumerate(self.ZF):
                h.changeCoeff(int(self.row_fcvar[0]), int(zj), float(self.p[j] / eps))
            self.set_row(self.row_fcvar, -INF, thr)
            self.eps["forced_eps"] = eps
        if ret_min is not None:
            self.set_row(self.row_mean, self.W0 * (1 + float(ret_min)) ** 5, INF)
            self.eps["ret_min"] = ret_min

    def apply_depth_guard(self, cvar_ref: float, delta: float = 0.0):
        """CVaR10 of WT/W0 >= cvar_ref - delta (cvar_ref from the status quo on the same scenarios)."""
        self.set_row(self.row_depth, float(cvar_ref) - float(delta), INF)
        self.eps["depth_guard"] = {"cvar_ref": cvar_ref, "delta": delta}

    def first_stage(self) -> dict:
        return {"sell": self.Sx, "x": self.X, "commit": self.Cc, "term": self.DT, "navf": self.DN, "beta": self.BETA}

    def fix_plan(self, plan: Plan):
        """Fix every first-stage decision to a plan's values (the reserve follows from the budget)."""
        h = self.highs()
        lo, hi = self.lb.copy(), self.ub.copy()
        bk = self.S.book
        vals = {}
        cont = plan.contingent or {}
        osd = [np.argsort(f) for f in self.freq_sd]                          # the most frequent context's value wins
        oc = [np.argsort(f) for f in self.freq_c]
        ctx_val = lambda arr, tau, k_: arr[k_] if len(arr) > k_ else arr[k_ % len(arr)]   # a 3-state plan on 9 histories
        for k, u in enumerate(bk.units):
            fr = plan.sell.get(u.id, [0.0, 0.0, 0.0])
            cs = (cont.get("sell") or {}).get(u.id)
            for tau in range(3):
                for k_ in osd[tau]:
                    v = fr[tau] if (tau == 0 or cs is None) else ctx_val(cs[tau - 1], tau, k_)
                    vals[int(self.SxI[tau][k, k_])] = float(v)
        for i, b in enumerate(self.LR):
            vals[int(self.X[i])] = float(plan.liquid.get(b, self.x0[i]))
        for j, b in enumerate(self.tb):
            cm = plan.commit.get(b, [0.0] * 5)
            cc = (cont.get("commit") or {}).get(b)
            for tau in range(5):
                for k_ in oc[tau]:
                    v = cm[tau] if (tau == 0 or cc is None) else cc[tau - 1][k_]
                    vals[int(self.CcI[tau][j, k_])] = float(v)
        sched = list(getattr(plan, "term_sched", None) or [plan.term_bn, 0.0, 0.0])
        for tau in range(3):
            for k_ in osd[tau]:
                v = sched[tau] if (tau == 0 or not cont.get("term")) else ctx_val(cont["term"][tau - 1], tau, k_)
                vals[int(self.DTI[tau][k_])] = float(v)
        vals[int(self.DN)] = float(plan.navf_bn)
        cb = cont.get("beta")
        ob = [np.argsort(f) for f in self.freq_b]
        for t in range(5):
            for k_ in ob[t]:
                v = plan.beta_bn if (t == 0 or not cb) else cb[t - 1][k_]
                vals[int(self.BI[t][k_])] = float(v)
        vals[int(self.BETA)] = float(plan.beta_bn)
        idx = np.array(list(vals.keys()), np.int32)
        v = np.array(list(vals.values()), float)
        h.changeColsBounds(len(idx), idx, v, v)
        self._fixed = (idx, lo[idx], hi[idx])

    def release(self):
        if getattr(self, "_fixed", None) is not None:
            idx, lo, hi = self._fixed
            self.highs().changeColsBounds(len(idx), idx, lo, hi)
            self._fixed = None

    def evaluate_plan(self, plan: Plan) -> dict | None:
        """In-sample evaluation of a fixed plan (recourse still optimized): WT and its CVaR10 on these scenarios."""
        self.fix_plan(plan)
        self.set_cost(self.obj_mean())
        x, _, _, rec = self.run(f"evaluate {plan.name}")
        self.release()
        if x is None:
            return None
        from .legacy import cvar_lower
        wt = x[self.WT] / self.W0
        return {"x": x, "cvar10": float(cvar_lower(wt, self.depth_alpha, self.p)), "in_sample": self.in_sample(x)}

    def _set_cvar_level(self, pk):
        h = self.highs()
        r = int(self.row_cvar[0])
        idx = np.asarray(self.Z, np.int64)
        for j, zj in enumerate(idx):
            h.changeCoeff(r, int(zj), float(self.p[j] / pk))

    # ------------------------------------------------------------------ results
    def X_miss(self, x):
        return (self.Wstar - x[self.WT]) / self.W0

    def _by_state(self, x, idx) -> list:
        """Values of a decision's copies for each observed state."""
        return [float(max(x[int(i)], 0.0)) for i in idx]

    def extract(self, x, name) -> Plan:
        """The plan: today's decisions, the later ones by observed state (plan.contingent) and their state-weighted
        averages in sell / commit / term_sched (in-sample state frequencies)."""
        bk = self.S.book
        fsd, fc = self.freq_sd, self.freq_c
        sell, c_sell = {}, {}
        for k, u in enumerate(bk.units):
            v0 = float(max(x[self.SxI[0][k, 0]], 0.0))
            vs = [self._by_state(x, self.SxI[tau][k]) for tau in (1, 2)]
            if v0 + sum(map(sum, vs)) > 1e-7:
                sell[u.id] = [v0] + [float(np.dot(fsd[tau], vs[tau - 1])) for tau in (1, 2)]
                c_sell[u.id] = vs
        liquid = {b: float(x[self.X[i]]) for i, b in enumerate(self.LR)}
        r0 = float(x[self.R0])
        commit, c_commit = {}, {}
        for j, b in enumerate(self.tb):
            vs = [self._by_state(x, self.CcI[tau][j]) for tau in range(1, 5)]
            commit[b] = [float(max(x[self.CcI[0][j, 0]], 0.0))] + [float(np.dot(fc[tau], vs[tau - 1])) for tau in range(1, 5)]
            c_commit[b] = vs
        ts = [self._by_state(x, self.DTI[tau]) for tau in (1, 2)]
        sched = [float(max(x[self.DTI[0][0]], 0.0))] + [float(np.dot(fsd[tau], ts[tau - 1])) for tau in (1, 2)]
        contingent = None
        if self.contingent_on:
            contingent = {"sell": c_sell, "commit": c_commit, "term": ts, "states": STATES,
                          "freq_commit": [f.tolist() for f in fc[1:]], "freq_sale": [f.tolist() for f in fsd[1:]],
                          "map_commit": [m_.tolist() for m_ in self.map_c[1:]],
                          "map_sale": [m_.tolist() for m_ in self.map_sd[1:]]}
            if self.cont_b:
                contingent.update({"beta": [self._by_state(x, self.BI[t]) for t in range(1, 5)],
                                   "freq_beta": [f.tolist() for f in self.freq_b[1:]],
                                   "map_beta": [m_.tolist() for m_ in self.map_b[1:]]})
        return Plan(name=name, sell=sell, liquid=liquid, cash=r0 * (1 - self.treasury_share),
                    treasury=r0 * self.treasury_share, commit=commit, term_bn=sum(sched), term_sched=sched,
                    navf_bn=float(x[self.DN]), beta_bn=float(x[self.BETA]),
                    meta={"kind": "optimized", "contingent": bool(self.contingent_on)}, contingent=contingent)

    def in_sample(self, x) -> dict:
        Wt = x[self.WT]
        twr = np.maximum(Wt / self.W0, 1e-9) ** 0.2 - 1
        Xm = self.X_miss(x)
        forced = sum(x[self.PHI[:, t - 1]] * self.cont_v[t][:, t] for t in range(1, 6))
        return {"p_goal": float(self.p @ (Wt >= self.Wstar * (1 - 1e-9))), "E_W": float(self.p @ Wt),
                "twr_mean": float(self.p @ twr), "bpoe": float(bpoe(Xm, self.p)),
                "p_forced": float(self.p @ (forced > 1e-6)), "below_target": float(self.p @ (x[self.U].sum(1) > 1e-6)),
                "floor_breach": float(self.p @ (x[self.UH].sum(1) > 1e-6))}

    def duals(self, x, y, rc) -> dict:
        """Shadow prices read from the LP that made the decision (sign-normalized to 'value of $1 more')."""
        lam0 = -y[self.rows.tags["budget"][0]]
        out = {"lambda0": float(lam0)}
        bk = self.S.book
        bid0 = self.ubid[0, 0, :]
        tags = self.rows.tags
        # reduced cost d_k = lam0 V (p* - bid) - (permission rows' share): the PE program, market-depth and
        # sale-total rows price PERMISSION to sell, not the economics of holding, so they are added back
        A = self.A_mat.tocsc()
        perm = np.zeros(self.nrow, bool)
        for name in ("program", "program0", "program1", "program2", "depth0", "sell_total"):
            if name in tags:
                perm[tags[name]] = True
        res = []
        for k, u in enumerate(bk.units):
            col = int(self.Sx[k, 0])
            r = rc[col] if rc is not None else 0.0
            a = A.getcol(col)
            r_perm = float(sum(v * y[i] for i, v in zip(a.indices, a.data) if perm[i]))
            V = max(self.nav0[k], 1e-12)
            # p_star: the decision threshold (finite-difference validated: the LP sells today iff bid > p_star,
            # given the PE program, market depth and sale limits); p_star_econ: the hold value with those
            # permission rows' shadow prices added back (what $1 of the unit is worth to the plan, unconstrained)
            p_raw = bid0[k] + r / (lam0 * V) if abs(lam0) > 1e-14 else np.nan
            p_econ = bid0[k] + (r + r_perm) / (lam0 * V) if abs(lam0) > 1e-14 else np.nan
            res.append({"unit": u.id, "bid0": float(bid0[k]), "p_star": float(p_raw), "p_star_econ": float(p_econ),
                        "sold0": float(x[col]),
                        "sold_total": float(x[col] + sum(np.dot(self.freq_sd[t], [x[int(i)] for i in self.SxI[t][k]])
                                                         for t in (1, 2))),
                        "sell_ub": float(self.ub[col])})
        out["units"] = res
        # liquid buckets: reduced cost of x (value of $1 more in the bucket vs cash, per $)
        out["liquid"] = {b: float(-rc[self.X[i]] / lam0) if abs(lam0) > 1e-14 else 0.0 for i, b in enumerate(self.LR)}
        out["commit"] = {b: float(-rc[self.Cc[j, 0]] / lam0) if abs(lam0) > 1e-14 else 0.0 for j, b in enumerate(self.tb)}
        tags = self.rows.tags
        for name in ("lev0", "recourse0", "navf_ltv0", "overcommit0", "reserve0", "program"):
            if name in tags:
                out[f"row_{name}"] = float(-y[tags[name][0]] / lam0) if abs(lam0) > 1e-14 else 0.0
        fl = np.concatenate([tags[f"floor{t}"] for t in range(1, 6)])
        out["floor_value"] = float(np.sum(y[fl]) / lam0) if abs(lam0) > 1e-14 else 0.0
        return out


# ---------------------------------------------------------------------------------------------- solve flows
def solve(model: TPPModel, objective: str, gamma: float | None = None, tol=None) -> dict:
    """objective: gbo | utility | mean | liquidity | mean_cvar. Returns x, y, rc, label and the solve log."""
    P = model.P
    log = []
    if objective == "mean":
        model.set_cost(model.obj_mean())
        x, y, rc, rec = model.run("max mean wealth")
        log.append(rec)
        return {"x": x, "y": y, "rc": rc, "label": "MEAN", "log": log}
    if objective == "utility":
        model.set_cost(model.obj_util())
        x, y, rc, rec = model.run(f"max CRRA({model.gamma:g}) utility")
        log.append(rec)
        return {"x": x, "y": y, "rc": rc, "label": "UTILITY", "log": log}
    if objective == "liquidity":
        model.set_cost(model.obj_liquidity())
        x, y, rc, rec = model.run("min liquidity risk at the return floor")
        log.append(rec)
        return {"x": x, "y": y, "rc": rc, "label": "LIQUIDITY", "log": log}
    if objective == "mean_cvar":
        model.set_cost(model.obj_mean_cvar())
        x, y, rc, rec = model.run("max mean - CVaR10")
        log.append(rec)
        return {"x": x, "y": y, "rc": rc, "label": "MEAN_CVAR", "log": log}
    # ---- GBO (examples/mpo_v2 optim.gbo, on this model)
    cmax = float(P.get("goal.c_max_factor")) * model.Wstar / model.W0
    model.set_cost(model.obj_mean())
    xm, ym, rcm, rec = model.run("GBO: mean LP")
    log.append(rec)
    if xm is None:
        return {"x": None, "label": "INFEASIBLE", "log": log}
    Estar = float(model.p @ xm[model.WT])
    out = {"E_star": Estar}
    tolb = float(P.get("objective.bisection_tol"))
    if Estar <= model.Wstar:
        out["label"] = "STRETCH"
        tie = float(P.get("objective.tiebreak_tol")) * cmax * model.W0
        model.set_row(model.row_mean, Estar - tie, INF)
        out["phi"] = 1.0 + (model.Wstar - Estar) / model.W0 / cmax
    else:
        out["label"] = "PLAN"
        pk = float(bpoe(model.X_miss(xm), model.p))
        hist = [pk]
        best = xm
        for it in range(10):
            c = model._penalty()
            c[model.ETA] = 1.0
            c[model.Z] = model.p / pk
            model.set_cost(c)
            xb, _, _, rec = model.run(f"GBO: min CVaR at p={pk:.4f}")
            log.append(rec)
            if xb is None:
                break
            pn = float(bpoe(model.X_miss(xb), model.p))
            hist.append(pn)
            if pn <= pk:
                best = xb
            if pk - pn < tolb:
                pk = min(pk, pn)
                break
            pk = pn
        out["phi"] = pk
        out["phi_history"] = hist
        pt = min(pk + float(P.get("objective.tiebreak_tol")), 1.0)
        model._set_cvar_level(pt)
        model.set_row(model.row_cvar, -INF, 0.0)
    model.set_cost(model.obj_util())
    x, y, rc, rec = model.run(f"GBO: CRRA({model.gamma:g}) tie-break")
    log.append(rec)
    if x is None:
        x, y, rc = xm, ym, rcm
    out.update({"x": x, "y": y, "rc": rc, "log": log})
    return out
