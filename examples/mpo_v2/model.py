"""Component 3: the multi-period optimizer (SYNTHETIC - NOT ADIC DATA).

One LP on the scenario tree, built from the action ledger (DSGO section 1.3). Columns (per node unless stated):
  SELL       s[n,i]      fraction of holding i sold at the node's bid (per holding at decision nodes)
  ADD        a[n,i]      liquid holdings bought;  y[n,k] purchase templates (secondaries, co-invest, CS, loans)
  REDEEM     r[n,i]      hedge-fund / open-end notices: cash arrives next year at the class pass-through
  PACE       y[n,k]      commitment budgets (PE, Secondaries, RA, PC, CS); fans inherit the stage-2 level
  REFINANCE  NAV facility, LP preferred, CS back-leverage, SMA back-leverage, RA cash-out, P2S
  LEVER      HF TRS;  INFRA_LEV and SMA_LEV templates (asset debt);  BETA: synthetic beta (risk budget)
  HEDGE      tail-ladder notional, opportunistic IM
  FUND       revolver draws / repayments and upsizing, term debt
  funding    q[n,s]      need-based pro-rata sleeve sales (LIQ, HF, AMB, RED) - the waterfall, not a SELL
Decision nodes are t = 0, 1, 2 (per holding); fan years t = 3, 4, 5 are constraint nodes with funding moves only
(H16, buy-and-hold). Every hard row of DSGO section 4.6 and guard of section 4.7 is a row here, identical under the
three objectives (GBO, exact max-P(goal) MILP, CRRA + L2). Labels follow R1: a node's net new financing is LEVER up
to its discretionary exposure increase and REFINANCE beyond (computed on the solution).
"""
from __future__ import annotations

import time

import highspy
import numpy as np
import scipy.sparse as sp

from common import GROUPS

INF = highspy.kHighsInf
FIN = ["REV", "TERM", "NAVF", "PREF", "CSBL", "SMABL", "RACO"]
FIN_FAMILY = {"REV": "FUND", "TERM": "FUND", "NAVF": "REFINANCE", "PREF": "REFINANCE", "CSBL": "REFINANCE",
              "SMABL": "REFINANCE", "RACO": "REFINANCE"}
FAMILIES = ["SELL", "ADD", "REFINANCE", "BETA", "LEVER", "PACE", "REDEEM", "HEDGE", "FUND", "REBALANCE"]


class Builder:
    def __init__(self):
        self.nv = 0
        self.blocks = {}
        self._lb, self._ub = [], []
        self.ri, self.ci, self.vv = [], [], []
        self.rlb, self.rub, self.rtag = [], [], []
        self.nr = 0

    def block(self, name, shape, lb=0.0, ub=INF):
        shape = tuple(shape) if isinstance(shape, (tuple, list)) else (int(shape),)
        n = int(np.prod(shape))
        idx = np.arange(self.nv, self.nv + n).reshape(shape)
        self._lb.append(np.broadcast_to(np.asarray(lb, float), shape).ravel().copy())
        self._ub.append(np.broadcast_to(np.asarray(ub, float), shape).ravel().copy())
        self.nv += n
        self.blocks[name] = idx
        return idx

    def freeze(self):
        self.lb = np.concatenate(self._lb)
        self.ub = np.concatenate(self._ub)

    def row(self, cols, vals, lb, ub, tag):
        cols = np.asarray(cols, dtype=np.int64)
        vals = np.asarray(vals, dtype=float)
        keep = vals != 0.0
        r = self.nr
        self.nr += 1
        self.ri.append(np.full(int(keep.sum()), r, dtype=np.int64))
        self.ci.append(cols[keep])
        self.vv.append(vals[keep])
        self.rlb.append(float(lb))
        self.rub.append(float(ub))
        self.rtag.append(tag)
        return r

    def matrix(self):
        ri = np.concatenate(self.ri)
        ci = np.concatenate(self.ci)
        vv = np.concatenate(self.vv)
        A = sp.csr_matrix((vv, (ri, ci)), shape=(self.nr, self.nv))
        A.sum_duplicates()
        return A


class E:
    """Linear expression accumulator: cols / vals lists plus a constant."""
    __slots__ = ("c", "v", "k")

    def __init__(self):
        self.c, self.v, self.k = [], [], 0.0

    def add(self, cols, vals, scale=1.0):
        cols = np.atleast_1d(cols)
        vals = np.broadcast_to(np.asarray(vals, float), cols.shape)
        self.c.extend(cols.tolist())
        self.v.extend((vals * scale).tolist())
        return self

    def const(self, x):
        self.k += x
        return self

    def merged(self):
        if not self.c:
            return np.zeros(0, np.int64), np.zeros(0)
        c = np.asarray(self.c, np.int64)
        v = np.asarray(self.v, float)
        u, inv = np.unique(c, return_inverse=True)
        out = np.zeros(len(u))
        np.add.at(out, inv, v)
        return u, out


class MPOModel:
    """mode: 'B0' (status-quo funding LP that defines the exogenous readings) or 'OPT' (needs b0info)."""

    def __init__(self, D: dict, mode: str = "OPT", b0info: dict | None = None, log=print):
        self.D, self.mode, self.b0, self.log = D, mode, b0info, log
        self.P = D["P"]
        self.solves = []
        t0 = time.time()
        self._build()
        self.build_time = time.time() - t0
        self.h = None

    # ------------------------------------------------------------------ helpers
    def g(self, k):
        return self.P.get(k)

    def _dec(self, n):
        return n if n < self.ND else self.D["a2"][n]

    def _hold(self, ex: E, n: int, field: np.ndarray, mask=None, scale=1.0):
        """Sum_i X_{i,n} field[n,i] (holdings after decisions at n; fans: stage-2 holdings minus sleeve cuts)."""
        vals = field[n] if mask is None else field[n] * mask
        if n < self.ND:
            nz = vals != 0
            ex.add(self.X[n][nz], vals[nz], scale)
        else:
            a = self.D["a2"][n]
            nz = vals != 0
            ex.add(self.X[a][nz], vals[nz], scale)
            sl = self.D["sleeve_of"]
            for s in range(4):
                tot = vals[sl == s].sum()
                if tot != 0:
                    ex.add(self.CQ[n, s], -tot, scale)
        return ex

    def _flow(self, ex: E, n: int, field: np.ndarray, mask=None, scale=1.0):
        """Sum_i X_{i,p} field[n,i]: flows in the year into n from holdings at the parent p."""
        p = self.par[n]
        vals = field[n] if mask is None else field[n] * mask
        nz = vals != 0
        if p < self.ND:
            ex.add(self.X[p][nz], vals[nz], scale)
        else:
            a = self.D["a2"][p]
            ex.add(self.X[a][nz], vals[nz], scale)
            sl = self.D["sleeve_of"]
            for s in range(4):
                tot = vals[sl == s].sum()
                if tot != 0:
                    ex.add(self.CQ[p, s], -tot, scale)
        return ex

    def _tpl_state(self, ex: E, n: int, field: str, kmask=None, scale=1.0, init_field=None):
        """Templates held at n (bought at decision ancestors incl. n; fan commitments at levels 3-4 incl. n)."""
        D = self.D
        arr = D["tpl_arr"][field] if field in D["tpl_arr"] else D[field]
        ini = D["tpl_init"][init_field or field] if (init_field or field) in D["tpl_init"] else D[init_field]
        K = len(D["tpl"])
        km = np.ones(K, bool) if kmask is None else kmask
        for m in D["anc"][n]:
            if self.lvl[m] <= 2:
                vals = (ini[m] if m == n else arr[D["pair_index"][(m, n)]]) * km
                ex.add(self.Y[m], vals, scale)
            elif self.lvl[m] in (3, 4):
                vals = (ini[m] if m == n else arr[D["pair_index"][(m, n)]]) * km * D["tpl_is_commit"]
                ex.add(self.Y[D["a2"][n]], vals, scale)
        return ex

    def _tpl_flow(self, ex: E, n: int, field: str, kmask=None, scale=1.0):
        D = self.D
        p = self.par[n]
        arr = D["tpl_arr"][field]
        K = len(D["tpl"])
        km = np.ones(K, bool) if kmask is None else kmask
        for m in D["anc"][p]:
            if self.lvl[m] <= 2:
                ex.add(self.Y[m], arr[D["pair_index"][(m, n)]] * km, scale)
            elif self.lvl[m] in (3, 4):
                ex.add(self.Y[D["a2"][n]], arr[D["pair_index"][(m, n)]] * km * D["tpl_is_commit"], scale)
        return ex

    def _tpl_debt(self, ex: E, n: int, scale=1.0, through_parent=False):
        """Template asset debt outstanding (bullet, per $ of equity)."""
        D = self.D
        base = self.par[n] if through_parent else n
        for m in D["anc"][base]:
            if self.lvl[m] <= 2:
                ex.add(self.Y[m], D["tpl_debt"], scale)
        return ex

    # ------------------------------------------------------------------ build
    def _build(self):
        D, P, g = self.D, self.P, self.g
        tr = D["tr"]
        T, I, ND = D["T"], D["I"], D["ND"]
        self.T, self.I, self.ND = T, I, ND
        self.lvl, self.par, self.cls = tr["level"], tr["parent"], tr["cls"]
        self.prob = tr["prob"]
        self.leaves = D["leaves"]
        L = len(self.leaves)
        K = len(D["tpl"])
        opt = self.mode == "OPT"
        rf = D["rf"]
        erf = np.exp(rf)
        b0 = self.b0 or {}
        B = Builder()
        self.B = B
        # ---------------- variables
        self.X = B.block("x", (ND, I), 0.0, INF)
        self.S = B.block("s", (ND, I))
        self.A = B.block("a", (ND, I))
        self.R = B.block("r", (ND, I))
        self.Y = B.block("y", (ND, K))
        self.PU = B.block("pu", ND)
        self.PD = B.block("pd", ND)
        self.PI = B.block("pi", ND, 0.0, g("overlay.p2s_cap"))
        hf_units = np.flatnonzero(D["is_hf"])
        self.hf_units = hf_units
        self.TRS = B.block("trs", (ND, len(hf_units)))
        self.HED = B.block("hed", ND)
        self.OPP = B.block("opp", ND, 0.0, g("overlay.opp_im_max"))
        self.BRK = B.block("brk", (ND, len(GROUPS)))
        self.C = B.block("C", T)
        self.IM = B.block("IM", T)
        self.Q = B.block("Q", T)
        self.W = B.block("W", T, -INF, INF)
        self.NR = B.block("NR", T, -INF, INF)
        self.EX = B.block("E", T)
        self.LQ = B.block("LQ", T, -INF, INF)
        self.M = B.block("M", T, -INF, INF)
        self.LB = B.block("LB", T)
        self.RS = B.block("RS", T)
        self.BETA = B.block("beta", T)
        self.QS = B.block("q", (T, 4))
        self.CQ = B.block("cq", (T, 4))
        self.HV = B.block("HV", T, -INF, INF)
        self.HN = B.block("HN", T, -INF, INF)
        self.TV = B.block("TV", T, -INF, INF)
        self.TN = B.block("TN", T, -INF, INF)
        self.PV = B.block("PV", T, -INF, INF)
        self.PP = B.block("PP", T, -INF, INF)
        self.HM = B.block("HM", T, -INF, INF)      # holdings' stressed calls - P10 distributions (next year)
        self.TM = B.block("TM", T, -INF, INF)      # templates' stressed calls - P10 distributions
        self.HU = B.block("HU", T, -INF, INF)      # holdings' unfunded
        self.TU = B.block("TU", T, -INF, INF)      # templates' unfunded
        self.FB = B.block("B", (T, len(FIN)))
        self.DR = B.block("dr", (T, len(FIN)))
        self.RP = B.block("rp", (T, len(FIN)))
        self.LUP = B.block("Lup", 1, 0.0, g("corporate_finance.revolver_upsize_max"))
        self.WT = B.block("Wt", L, -INF, INF)
        self.Z = B.block("z", L)
        self.ETA_R = B.block("eta_R", 1, -INF, INF)
        lev = g("constraints.depth_levels")
        self.UU = B.block("uu", (L, len(lev)))
        self.ETA_A = B.block("eta_a", len(lev), -INF, INF)
        self.UTIL = B.block("util", L, -INF, INF)
        self.SH = B.block("sh", L)
        self.V2 = B.block("v2", L)
        self.UB = B.block("ub", L)
        self.ETA_B = B.block("eta_b", 1, -INF, INF)
        self.SL3 = B.block("sl3", ND)
        self.SL4 = B.block("sl4", 1)
        self.SL11 = B.block("sl11", T)
        self.SL15 = B.block("sl15", L)
        self.SL9 = B.block("sl9", 1)
        B.freeze()
        lb, ub = B.lb, B.ub
        # ---------------- data
        cls = self.cls
        V, Nr, Uf, Dl, Cl = D["V"], D["N"], D["U"], D["D"], D["C"]
        proc = D["proc"]
        sl = D["sleeve_of"]
        S_sl, bid_sl = D["S_sl"], D["bid_sl"]
        W0 = D["W0"]
        Wstar = D["Wstar"]
        cf = lambda k: g(f"corporate_finance.{k}")
        ov = lambda k: g(f"overlay.{k}")
        cn = lambda k: g(f"constraints.{k}")
        im_rate = np.array(ov("im_rate"))
        fb = np.array(ov("beta_fin_spread"))
        fp = np.array(ov("p2s_fin_spread"))
        navf, pref, csbl, smabl, raco = cf("navf"), cf("pref"), cf("csbl"), cf("smabl"), cf("raco")
        rev_av = np.array(cf("revolver_avail"))
        Ls = cf("revolver_signed")
        fee_u = cf("revolver_undrawn_fee")
        # per-instrument rates by class of the year (cash-pay vs PIK)
        rate = np.zeros((len(FIN), 3))
        rate[0] = rf + cf("revolver_spread")
        rate[1] = rf + cf("term_spread")
        rate[2] = rf + np.array(navf["spread"])
        rate[3] = np.array(pref["rate"])
        rate[4] = rf + csbl["spread"]
        rate[5] = rf + smabl["spread"]
        rate[6] = rf + np.array(raco["spread"])
        pik = np.array([False, False, True, True, False, False, False])
        oid = np.array([0, 0, navf["oid"], pref["fee"], 0, 0, 0])
        self.rate, self.pik = rate, pik
        avail = np.zeros((len(FIN), 3))
        avail[0] = 1.0
        avail[1] = cf("term_avail")
        avail[2] = navf["avail"]
        avail[3] = pref["avail"]
        avail[4] = csbl["avail"]
        avail[5] = smabl["avail"]
        avail[6] = raco["avail"]
        green = b0.get("green", np.zeros(T, bool))
        behind = b0.get("behind", np.zeros(T, bool))
        loss = b0.get("loss", np.zeros(T, bool))
        black = b0.get("black", np.zeros(T, bool))
        stage = b0.get("stage", np.ones(T, int))
        self.green = green
        # ---------------- variable bounds (admissibility, H14)
        liq = D["liquid"]
        red = D["red"]
        capt = D["cap_trade"]
        tpls = D["tpl"]
        plan = np.array([t.get("plan", 0.0) for t in tpls])
        mr = g("pacing.mult_range")
        is_commit = D["tpl_is_commit"]
        xmax = g("trading.xmax_liquid")
        rec2 = opt and bool(g("tree.stage2_recourse_only"))
        self.rec2 = rec2
        for n in range(ND):
            ub[self.X[n]] = np.where(liq, xmax, 1.0)
            Vn = np.maximum(V[n], 1e-9)
            su = np.minimum(capt / Vn, 1.0)
            if n == 0:
                su = np.where(red, 0.0, su)            # ADR-39: today is Amber, so root red-tier SELL is held at zero
            ub[self.S[n]] = su
            ub[self.A[n]] = np.where(liq, capt / Vn, 0.0)
            ub[self.R[n]] = np.where(D["is_hf"] | D["is_re_open"], 1.0, 0.0)
            if rec2 and self.lvl[n] == 2:             # stage-2 recourse only: funding moves, as in the fans
                ub[self.S[n]] = 0.0
                ub[self.A[n]] = 0.0
                ub[self.R[n]] = 0.0
                ub[self.PU[n]] = 0.0
                ub[self.PD[n]] = 0.0
            for k, t in enumerate(tpls):
                if t["kind"] == "commit":
                    lb[self.Y[n, k]] = mr[0] * plan[k]
                    ub[self.Y[n, k]] = mr[1] * plan[k]
                else:
                    ok = cls[n] in t["classes"]
                    if D["tpl_names"][k] == "SEC_BUY":
                        price = np.array(g("bids.rho")["fund"])[cls[n]] * D["theta_fund"][n]
                        ok = ok and (1 - price) > t["discount_gate"] and not black[n]
                    if t["green_only"]:
                        ok = ok and bool(green[n])
                    if rec2 and self.lvl[n] == 2:
                        ok = False
                    ub[self.Y[n, k]] = t["cap_year"] if ok else 0.0
            ub[self.TRS[n]] = INF
            ub[self.HED[n]] = INF
        ub[self.Q[D["leaves"]]] = INF
        for n in range(T):
            if n >= ND:
                ub[self.QS[n]] = [INF, INF, INF, INF]
            if self.lvl[n] >= 4:
                ub[self.Q[n]] = 0.0
            for j, nm in enumerate(FIN):
                c = cls[n]
                allow = avail[j, c] > 0
                if n >= ND or (rec2 and self.lvl[n] == 2):
                    allow = allow and nm == "REV"
                if self.lvl[n] == 5:
                    allow = False                       # H15: no new borrowing at leaves
                ub[self.DR[n, j]] = INF if allow else 0.0
        ub[self.FB[:, 6]] = raco["cap"]
        ub[self.CQ[:ND]] = 0.0
        ub[self.QS[:, 3]] = np.where(np.arange(T) < 1, 0.0, INF)  # no forced red sleeve sale at the root
        # ---------------- B0 mode: status-quo decisions fixed
        if not opt:
            ub[self.S.ravel()] = 0.0
            ub[self.A.ravel()] = 0.0
            ub[self.R.ravel()] = 0.0
            for k in range(K):
                if is_commit[k]:
                    lb[self.Y[:, k]] = plan[k]
                    ub[self.Y[:, k]] = plan[k]
                else:
                    ub[self.Y[:, k]] = 0.0
            ub[self.PU] = 0.0
            ub[self.PD] = 0.0
            ub[self.TRS.ravel()] = 0.0
            lb[self.OPP] = ov("opp_im_sq")
            ub[self.OPP] = ov("opp_im_sq")
            # the status quo holds its $10bn of synthetic beta at every node, fan years included (its funding-penalty
            # objective would otherwise be indifferent to beta in the fans and leave it at an arbitrary level)
            lb[self.BETA] = ov("beta_sq")
            ub[self.BETA] = ov("beta_sq")
            for j, nm in enumerate(FIN):
                if nm != "REV":
                    ub[self.DR[:, j]] = 0.0
            ub[self.LUP] = 0.0
        # slacks are only for Phase I (bounded by the Phase I solution later)
        ub[self.SL3] = INF
        ub[self.SL4] = INF
        ub[self.SL11] = INF
        ub[self.SL15] = INF
        ub[self.SL9] = INF
        # ---------------- rows
        rows = {}
        self.rows = rows
        R = B.row
        x0 = np.ones(I)
        C0 = g("treasury.cash0")
        hfi = g("treasury.fi_liquidity_weight")
        cpace = g("pacing.c_pace")
        psi = g("valuation.psi_unfunded")
        hmin = g("overlay.tail_budget")[0] / ov("tail_premium")
        hmax = g("overlay.tail_budget")[1] / ov("tail_premium")
        prem = ov("tail_premium")
        tc_lo = g("trading.tc")["lo_dm"]
        lo1 = D["lo1"]
        fi = D["fi"]
        d_year, d_next = D["tr"]["d_year"], D["tr"]["d_next"]
        Geq, tailpay, oppret = D["Geq"], D["tailpay"], D["oppret"]
        Gu = D["G"]
        first_str = D["tr"]["first_after_str"]
        caps_cls = np.array(cn("class_caps"))
        bshare = cn("behind_cap_share")
        rho_amber_str = 0.80
        phi_hf = np.array(g("trading.redeem_phi")["hf"])
        phi_re = np.array(g("trading.redeem_phi")["re_open_end"])
        phi_u = np.where(D["is_hf"][:, None], phi_hf[None, :], np.where(D["is_re_open"][:, None], phi_re[None, :], 0.0))
        pledge, priv = D["is_pledge"].astype(float), D["is_private"].astype(float)
        lo_eq, hfm = D["is_lo_eq"].astype(float), D["is_hf"].astype(float)
        amb = D["amber"].astype(float)
        gi = {gname: (D["group"] == gname).astype(float) for gname in GROUPS}
        tgi = {gname: (D["tpl_group"] == gname) for gname in GROUPS}
        w_grp = {gname: float((V[0] * gi[gname]).sum() / W0) for gname in GROUPS}
        self.w_grp = w_grp
        rows["cash"] = np.zeros(T, int)
        rows["xbal"] = np.full((ND, I), -1)
        for n in range(T):
            p = self.par[n]
            dn = self._dec(n)
            c = cls[n]
            isdec = n < ND
            # --- x balance (decision nodes)
            if isdec:
                for i in range(I):
                    ex = E().add([self.X[n, i], self.S[n, i], self.A[n, i], self.R[n, i]], [1.0, 1.0, -1.0, 1.0])
                    if p >= 0:
                        ex.add(self.X[p, i], -1.0)
                    s_ = sl[i]
                    ex.add(self.QS[n, s_], 1.0 / max(S_sl[n, s_], 1e-9))
                    if i == lo1:
                        ex.add([self.PU[n], self.PD[n]], [1.0 / V[n, lo1], -1.0 / V[n, lo1]])
                    cc, vv = ex.merged()
                    rhs = 1.0 if p < 0 else 0.0
                    rows["xbal"][n, i] = R(cc, vv, rhs, rhs, ("xbal", n, i))
                # P2S balance
                ex = E().add([self.PI[n], self.PU[n], self.PD[n]], [1.0, -1.0, 1.0])
                if p >= 0:
                    ex.add(self.PI[p], -1.0)
                R(*ex.merged(), 0.0, 0.0, ("p2s", n))
                if rec2 and self.lvl[n] == 2:
                    # stage-2 recourse only: pacing, TRS, tail ladder and opportunistic book carried from stage 1;
                    # synthetic beta can only be cut (forced deleveraging)
                    for k in np.flatnonzero(is_commit):
                        R([self.Y[n, k], self.Y[p, k]], [1.0, -1.0], 0.0, 0.0, ("pace2", n, k))
                    for h in range(len(hf_units)):
                        R([self.TRS[n, h], self.TRS[p, h]], [1.0, -1.0], 0.0, 0.0, ("trs2", n, h))
                    R([self.HED[n], self.HED[p]], [1.0, -1.0], 0.0, 0.0, ("hed2", n))
                    R([self.OPP[n], self.OPP[p]], [1.0, -1.0], 0.0, 0.0, ("opp2", n))
                    R([self.BETA[n], self.BETA[p]], [1.0, -1.0], -INF, 0.0, ("betacut2", n))
            else:
                # sleeve cumulative cut in fans: cq[n,s] = cq[p,s] + q[n,s] / S[n,s]
                for s_ in range(4):
                    ex = E().add([self.CQ[n, s_], self.QS[n, s_]], [1.0, -1.0 / max(S_sl[n, s_], 1e-9)])
                    if p >= ND:
                        ex.add(self.CQ[p, s_], -1.0)
                    R(*ex.merged(), 0.0, 0.0, ("cq", n, s_))
                # synthetic beta can only be cut in fans (forced deleveraging, H16)
                R([self.BETA[n], self.BETA[p]], [1.0, -1.0], -INF, 0.0, ("betacut", n))
            # --- aggregates
            ex = self._hold(E().add(self.HV[n], 1.0), n, V, scale=-1.0)
            R(*ex.merged(), 0.0, 0.0, ("HV", n))
            ex = self._hold(E().add(self.HN[n], 1.0), n, Nr, scale=-1.0)
            R(*ex.merged(), 0.0, 0.0, ("HN", n))
            ex = self._tpl_state(E().add(self.TV[n], 1.0), n, "V", scale=-1.0)
            R(*ex.merged(), 0.0, 0.0, ("TV", n))
            ex = self._tpl_state(E().add(self.TN[n], 1.0), n, "N", scale=-1.0)
            R(*ex.merged(), 0.0, 0.0, ("TN", n))
            # private NAV = holdings - liquid holdings + templates (all templates are private)
            ex = E().add([self.PV[n], self.HV[n], self.TV[n]], [1.0, -1.0, -1.0])
            self._hold(ex, n, V, mask=(~D["is_private"]).astype(float), scale=1.0)
            R(*ex.merged(), 0.0, 0.0, ("PV", n))
            ex = self._hold(E().add(self.PP[n], 1.0), n, V, mask=pledge, scale=-1.0)
            R(*ex.merged(), 0.0, 0.0, ("PP", n))
            ex = self._hold(E().add(self.HM[n], 1.0), n, D["callS"] - D["distL"], scale=-1.0)
            R(*ex.merged(), 0.0, 0.0, ("HM", n))
            ex = self._tpl_state(E().add(self.TM[n], 1.0), n, "tpl_callS", scale=-1.0, init_field="tpl_init_callS")
            self._tpl_state(ex, n, "tpl_distL", scale=1.0, init_field="tpl_init_distL")
            R(*ex.merged(), 0.0, 0.0, ("TM", n))
            ex = self._hold(E().add(self.HU[n], 1.0), n, Uf, scale=-1.0)
            R(*ex.merged(), 0.0, 0.0, ("HU", n))
            ex = self._tpl_state(E().add(self.TU[n], 1.0), n, "U", scale=-1.0)
            R(*ex.merged(), 0.0, 0.0, ("TU", n))
            # --- IM
            ex = E().add([self.IM[n], self.BETA[n]], [1.0, -im_rate[c]])
            ex.add(self.PI[dn], -im_rate[c]).add(self.TRS[dn], -ov("trs_ia")).add(self.OPP[dn], -1.0)
            R(*ex.merged(), 0.0, 0.0, ("IM", n))
            # --- W (economic NAV, after decisions; every financing claim at face; template debt)
            ex = E().add([self.W[n], self.C[n], self.IM[n], self.Q[n], self.HV[n], self.TV[n]],
                         [1.0, -1.0, -1.0, -1.0, -1.0, -1.0])
            ex.add(self.FB[n], 1.0)
            self._tpl_debt(ex, n, 1.0)
            R(*ex.merged(), 0.0, 0.0, ("W", n))
            ex = E().add([self.NR[n], self.C[n], self.IM[n], self.Q[n], self.HN[n], self.TN[n]],
                         [1.0, -1.0, -1.0, -1.0, -1.0, -1.0])
            ex.add(self.FB[n], 1.0)
            self._tpl_debt(ex, n, 1.0)
            R(*ex.merged(), 0.0, 0.0, ("NR", n))
            # --- exposure (delta-adjusted, incl. synthetic, P2S futures, TRS)
            ex = E().add([self.EX[n], self.HV[n], self.TV[n], self.BETA[n], self.PI[dn]], [1.0, -1.0, -1.0, -1.0, -1.0])
            ex.add(self.TRS[dn], -1.0)
            R(*ex.merged(), 0.0, 0.0, ("E", n))
            # --- IG + cash
            ex = E().add([self.LQ[n], self.C[n]], [1.0, -1.0])
            self._hold(ex, n, V, mask=(np.arange(I) == fi).astype(float), scale=-hfi)
            R(*ex.merged(), 0.0, 0.0, ("LQ", n))
            # --- cash row: C[n] = e^rf C[p] + flows + decisions
            ex = E().add([self.C[n], self.IM[n]], [1.0, 1.0])
            rhs = 0.0
            if p < 0:
                rhs = C0
            else:
                pd_ = self._dec(p)
                ex.add([self.C[p], self.IM[p]], [-erf, -erf])         # cash and posted margin earn SOFR
                self._flow(ex, n, Dl - Cl, scale=-1.0)
                self._tpl_flow(ex, n, "D", scale=-1.0)
                self._tpl_flow(ex, n, "C", scale=1.0)
                for m in D["anc"][p]:
                    if self.lvl[m] <= 2:
                        ex.add(self.Y[m], D["tpl_debt"] * (rf + D["tpl_spread"]), 1.0)   # asset-debt interest
                ex.add(self.NR[p], d_year[n])                                         # owner draw (H1)
                for j in range(len(FIN)):
                    if not pik[j]:
                        ex.add(self.FB[p, j], rate[j, c])
                # revolver undrawn fee on (signed + upsized - drawn)
                ex.add(self.FB[p, 0], -fee_u)
                ex.add(self.LUP, fee_u)
                rhs -= fee_u * Ls
                # futures variation margin (P2S and synthetic beta), TRS, tail payoff, opportunistic P&L
                ex.add(self.PI[pd_], -(Geq[n] - erf - fp[c]))
                ex.add(self.BETA[p], -(Geq[n] - erf - fb[c]))
                for h, iu in enumerate(hf_units):
                    ex.add(self.TRS[pd_, h], -(Gu[n, iu] - erf - ov("trs_fin_spread")))
                ex.add(self.HED[pd_], -tailpay[n])
                ex.add(self.OPP[pd_], -oppret[n])
                # redemption cash (notices at the parent) and queued claims
                if p < ND:
                    nzr = phi_u[:, c] > 0
                    ex.add(self.R[p][nzr], -(phi_u[nzr, c] * V[n, nzr]))
                ex.add(self.Q[p], -erf)
            if self.lvl[n] < 5:
                ex.add(self.HED[dn], prem)                         # premium for the next year's ladder
            if isdec:
                ex.add(self.S[n], -proc[n])
                ex.add(self.A[n], V[n] * (1 + D["tc_add"]))
                ex.add(self.Y[n], np.where(is_commit, 0.0, 1.0))
                ex.add(self.PU[n], -(1 - tc_lo))
                ex.add(self.PD[n], (1 + tc_lo))
                if n == 0:
                    ex.add(self.LUP, cf("revolver_upfront_fee") * 3)
            ex.add(self.QS[n], -bid_sl[n])
            ex.add(self.DR[n], -(1 - oid))
            ex.add(self.RP[n], 1.0)
            rows["cash"][n] = R(*ex.merged(), rhs, rhs, ("cash", n))
            # --- redemption queue
            if self.lvl[n] <= 3 and p >= 0 and p < ND:
                ex = E().add(self.Q[n], 1.0)
                nzr = phi_u[:, c] > 0
                ex.add(self.R[p][nzr], -((1 - phi_u[nzr, c]) * V[n, nzr]))
                R(*ex.merged(), 0.0, 0.0, ("Q", n))
            elif self.lvl[n] <= 3:
                R([self.Q[n]], [1.0], 0.0, 0.0, ("Q0", n))
            # --- debt balances and caps
            for j in range(len(FIN)):
                ex = E().add([self.FB[n, j], self.DR[n, j], self.RP[n, j]], [1.0, -1.0, 1.0])
                if p >= 0:
                    ex.add(self.FB[p, j], -(1.0 + (rate[j, c] if pik[j] else 0.0)))
                R(*ex.merged(), 0.0, 0.0, ("bal", n, j))
            Lcap_on = 1.0 if self.lvl[n] >= 1 else 0.0
            R([self.FB[n, 0], self.LUP[0]], [1.0, -rev_av[c] * Lcap_on], -INF, rev_av[c] * Ls, ("revcap", n))
            R([self.FB[n, 0], self.FB[n, 1], self.W[n]], [1.0, 1.0, -cf("recourse_cap")], -INF, 0.0, ("recourse", n))
            R([self.FB[n, 2], self.PP[n]], [1.0, -navf["ltv"][c]], -INF, 0.0, ("navf_ltv", n))
            R([self.FB[n, 2], self.PV[n]], [1.0, -navf["ltv"][c] * navf["pool_cap_share"]], -INF, 0.0, ("navf_pool", n))
            R([self.FB[n, 3], self.PP[n]], [1.0, -pref["advance"]], -INF, 0.0, ("pref_cap", n))
            ex = self._hold(E().add(self.FB[n, 4], 1.0), n, V, mask=D["is_cs"].astype(float), scale=-csbl["debt_to_value"])
            R(*ex.merged(), -INF, 0.0, ("csbl", n))
            ex = self._hold(E().add(self.FB[n, 5], 1.0), n, V, mask=D["is_sma"].astype(float), scale=-smabl["ltv"])
            R(*ex.merged(), -INF, 0.0, ("smabl", n))
            ex = self._hold(E().add(self.FB[n, 6], 1.0), n, V, mask=D["is_ra_ctrl"].astype(float), scale=-raco["ltv"])
            R(*ex.merged(), -INF, 0.0, ("raco", n))
            # encumbrance: pledged collateral <= 20% of total assets
            enc = [1.0 / navf["ltv"][0], 1.0 / pref["advance"], 1.0 / csbl["debt_to_value"], 1.0 / smabl["ltv"],
                   1.0 / raco["ltv"]]
            ex = E().add(self.FB[n, 2:7], np.array(enc) - cf("encumbrance_cap"))
            ex.add(self.W[n], -cf("encumbrance_cap"))
            ex.add(self.FB[n, 0:2], -cf("encumbrance_cap"))
            R(*ex.merged(), -INF, 0.0, ("encumb", n))
            # --- floors (H2)
            R([self.LQ[n], self.W[n]], [1.0, -cn("floor_hard")], 0.0, INF, ("floor4", n))
            if c in (0, 1) and not first_str[n] and opt:     # B0 keeps only the 4% floor (B1 restores 8%)
                rows.setdefault("floor8", {})[n] = R([self.LQ[n], self.W[n]], [1.0, -cn("floor_target")], 0.0, INF,
                                                     ("floor8", n))
            # --- leverage (H5 and G5 class / behind caps)
            capn = cn("lev_cap")
            if opt:
                # STR class caps are met within four quarters, not at the bottom: the first STR node keeps the
                # parent's class cap, so the cap never forces deleveraging sales in the crisis year itself
                cc_ = cls[p] if (c == 2 and n > 0 and cls[p] != 2) else c
                capn = min(capn, caps_cls[cc_])
                if behind[n]:
                    capn = 1.0 + bshare * (caps_cls[cc_] - 1.0)
            self.levcap = getattr(self, "levcap", np.zeros(T))
            self.levcap[n] = capn
            rows.setdefault("lev", {})[n] = R([self.EX[n], self.W[n]], [1.0, -capn], -INF, 0.0, ("lev", n))
            # gross overlay (H13)
            ex = E().add([self.BETA[n], self.PI[dn]], [1.0, 1.0]).add(self.TRS[dn], 1.0).add(self.W[n], -ov("gross_max"))
            R(*ex.merged(), -INF, 0.0, ("gross", n))
            # --- G5 cushion and G4 no-doubling-down (OPT only; exogenous B0 readings)
            if opt:
                R([self.LB[n], self.EX[n], self.W[n]], [1.0, -1.0, 1.0], 0.0, INF, ("lbor", n))
                ub[self.LB[n]] = cn("kappa_c") * max(0.0, -b0["M"][n])
                if n > 0 and (behind[n] or loss[n]):
                    ratio = b0["W"][n] / max(b0["W"][p], 1e-9)
                    rows.setdefault("g4", {})[n] = R([self.EX[n], self.EX[p]], [1.0, -ratio], -INF, 0.0, ("g4", n))
                    if isdec:
                        ex = E().add(self.BETA[n], 1.0).add(self.TRS[n], 1.0).add(self.BETA[p], -1.0).add(self.TRS[p], -1.0)
                        R(*ex.merged(), -INF, 0.0, ("g4lev", n))
                        pm = ~is_commit
                        ex = E().add(self.Y[n][pm], 1.0).add(self.Y[p][pm], -1.0)
                        R(*ex.merged(), -INF, 0.0, ("g4add", n))
            # --- red sales (ADR-39) and the signed red margin (H9)
            ex = E().add(self.RS[n], 1.0)
            if isdec:
                ratio_bid = proc[n] / np.maximum(D["proc_norm"][n], 1e-12)
                is_red_evt = red & ((not green[n]) | (ratio_bid < cn("red_bid_ratio")))
                ex.add(self.S[n][is_red_evt], -proc[n][is_red_evt])
            ex.add(self.QS[n, 3], -bid_sl[n, 3])
            R(*ex.merged(), 0.0, 0.0, ("RS", n))
            ex = E().add(self.M[n], 1.0)
            ex.add(self.NR[n], -d_next[n])
            ex.add([self.HM[n], self.TM[n]], [-1.0, -1.0])
            for j in range(len(FIN)):
                ex.add(self.FB[n, j], -rate[j, 2])
            for m in D["anc"][n]:
                if self.lvl[m] <= 2:
                    ex.add(self.Y[m], -D["tpl_debt"] * (rf + D["tpl_spread"]))
            vm = cn("margin_vm_drop") + (im_rate[2] - im_rate[c])
            ex.add([self.BETA[n], self.PI[dn]], [-vm, -vm])
            # capacity: cash above the hard floor, stressed liquid book, HF pass-through, revolver headroom, amber
            ex.add([self.LQ[n], self.W[n]], [1.0, -cn("floor_hard")])
            self._hold(ex, n, V, mask=lo_eq, scale=(1 - cn("margin_lo_haircut")))
            self._hold(ex, n, V, mask=hfm, scale=cn("margin_hf_phi"))
            self._hold(ex, n, V, mask=amb, scale=cn("margin_amber_share") * rho_amber_str)
            ex.add([self.LUP[0], self.FB[n, 0]], [rev_av[2] * (1.0 if self.lvl[n] >= 1 else 0.0), -1.0])
            ex.add(self.Q[n], 1.0)
            rows.setdefault("margin", {})[n] = R(*ex.merged(), -rev_av[2] * Ls, -rev_av[2] * Ls, ("M", n))
            # --- H3 six-month coverage at decision nodes
            if isdec and opt:
                ex = E()
                ex.add([self.LQ[n], self.W[n]], [1.0, -cn("floor_hard")])
                self._hold(ex, n, V, mask=lo_eq, scale=(1 - cn("margin_lo_haircut")))
                self._hold(ex, n, V, mask=hfm, scale=cn("h3_hf_phi"))
                ex.add([self.LUP[0], self.FB[n, 0]], [rev_av[c] * (1.0 if self.lvl[n] >= 1 else 0.0), -1.0])
                hs = cn("h3_share")
                ex.add(self.NR[n], -hs * d_next[n])
                ex.add([self.HM[n], self.TM[n]], [-hs, -hs])
                ex.add(self.SL3[n], 1.0)
                R(*ex.merged(), -rev_av[c] * Ls, INF, ("H3", n))
            # --- H11 overcommitment (STR nodes exempt)
            if opt and c != 2:
                ex = E().add([self.PV[n], self.HU[n], self.TU[n]], [1.0, 1.0, 1.0])
                ex.add(self.W[n], -cn("overcommit")).add(self.SL11[n], -1.0)
                rows.setdefault("H11", {})[n] = R(*ex.merged(), -INF, 0.0, ("H11", n))
            # --- need-based sleeve funding (H16): sleeve sales <= this year's outflows + floor restoration
            # (calls enter as a constant upper bound: every original holding fully held plus commitments at the
            #  top of the pacing range, so the row only caps funding sales and never binds on discretionary moves)
            ex = E().add(self.QS[n], bid_sl[n])
            calls_ub = 0.0
            if p >= 0:
                ex.add(self.NR[p], -d_year[n])
                calls_ub = float(Cl[n].sum())
                for mm in D["anc"][p]:
                    key = (mm, n)
                    if key in D["pair_index"]:
                        calls_ub += float((D["tpl_arr"]["C"][D["pair_index"][key]] * plan * mr[1]).sum())
                for j in range(len(FIN)):
                    ex.add(self.FB[p, j], -rate[j, c])
                ex.add(self.HED[self._dec(p)], -prem)
            ex.add(self.W[n], -cn("floor_target"))
            ex.add(self.RP[n], -1.0)
            R(*ex.merged(), -INF, calls_ub, ("need", n))
            # sleeve depth per year
            for s_, share in ((1, g("trading.hf_secondary_share")), (2, cn("margin_amber_share")),
                              (3, g("trading.co_sale_share"))):
                ex = E().add(self.QS[n, s_], 1.0)
                if n < ND and p >= 0:
                    self._flow(ex, n, V, mask=(sl == s_).astype(float), scale=-share)
                    R(*ex.merged(), -INF, 0.0, ("sdepth", n, s_))
                else:
                    R([self.QS[n, s_]], [1.0], -INF, share * S_sl[n, s_], ("sdepth", n, s_))
            # --- decision-node rows: depth caps (H7), TRS cap, hedge range, IC ranges, SEC group cap
            if isdec:
                lpm = (np.isin(D["group"], ["PE", "SEC"])).astype(float)
                ex = E().add(self.S[n], proc[n] * lpm)
                R(*ex.merged(), -INF, g("trading.lp_depth_year")[c], ("depth_lp", n))
                for gname, share in (("CO", g("trading.co_sale_share")), ("RA", g("trading.ra_sale_share")[c]),
                                     ("CS", g("trading.amber_sale_share")["CS"][c]),
                                     ("PC", g("trading.amber_sale_share")["PC"][c]),
                                     ("HF", g("trading.hf_secondary_share"))):
                    mk = gi[gname]
                    ex = E().add(self.S[n], V[n] * mk)
                    if p >= 0:
                        ex.add(self.X[p], -share * V[n] * mk)
                        rhs_d = 0.0
                    else:
                        rhs_d = share * (V[n] * mk).sum()
                    R(*ex.merged(), -INF, rhs_d, ("depth", n, gname))
                if not (rec2 and self.lvl[n] == 2):
                    for h, iu in enumerate(hf_units):
                        R([self.TRS[n, h], self.X[n, iu]], [1.0, -ov("trs_cap_share") * V[n, iu]], -INF, 0.0,
                          ("trscap", n, h))
                    rows.setdefault("hedlo", {})[n] = R([self.HED[n], self.W[n]], [1.0, -hmin], 0.0, INF, ("hedlo", n))
                    rows.setdefault("hedhi", {})[n] = R([self.HED[n], self.W[n]], [1.0, -(hmax if opt else hmin)],
                                                        -INF, 0.0, ("hedhi", n))
                if c != 2:
                    for gk, gname in enumerate(GROUPS):
                        exg = self._hold(E(), n, V, mask=gi[gname])
                        self._tpl_state(exg, n, "V", kmask=tgi[gname])
                        ce, ve = exg.merged()
                        lo_b, hi_b = g("constraints.range_band")
                        R(np.r_[ce, self.BRK[n, gk], self.W[n]], np.r_[-ve, 1.0, hi_b * w_grp[gname]], 0.0, INF,
                          ("brk_hi", n, gname))
                        R(np.r_[ce, self.BRK[n, gk], self.W[n]], np.r_[ve, 1.0, -lo_b * w_grp[gname]], 0.0, INF,
                          ("brk_lo", n, gname))
                if ub[self.Y[n, D["tpl_names"].index("SEC_BUY")]] > 0:
                    exg = self._hold(E(), n, V, mask=gi["SEC"])
                    self._tpl_state(exg, n, "V", kmask=tgi["SEC"])
                    exg.add(self.W[n], -P.get("templates.SEC_BUY")["group_cap_share"])
                    R(*exg.merged(), -INF, 0.0, ("seccap", n))
        # --- H4: 24-month named stress at the root (T4')
        if opt:
            h4 = cn("h4")
            ex = E().add([self.LQ[0], self.W[0]], [1.0, -cn("floor_hard")])
            self._hold(ex, 0, V, mask=lo_eq, scale=1 - h4["equity_drop"])
            self._hold(ex, 0, V, mask=hfm, scale=h4["hf_pass"])
            ex.add(self.PP[0], h4["navf_ltv"]).add(self.FB[0, 2], -1.0)
            ex.add(self.NR[0], -2 * h4["draw_rate"])
            self._hold(ex, 0, D["calls24"][None, :].repeat(T, 0) - D["dist24"][None, :].repeat(T, 0), scale=-1.0)
            ex.add(self.Y[0], -(D["tpl_init_calls24"] - D["tpl_init_dist24"]))
            for j in range(len(FIN)):
                ex.add(self.FB[0, j], -2 * rate[j, 2])
            ex.add([self.BETA[0], self.PI[0]], [-(h4["equity_drop"] + im_rate[2] - im_rate[1])] * 2)
            ex.add(self.SL4, 1.0)
            rows["H4"] = R(*ex.merged(), -h4["revolver_credit"] * Ls, INF, ("H4", 0))
        # ---------------- leaves: W~, H15, H9, H10, utility, shortfall, bisection auxiliaries
        p_leaf = self.prob[self.leaves]
        self.p_leaf = p_leaf
        rng_ch = g("constraints.range_charge")
        rows["Wt"] = np.zeros(L, int)
        pace_k = [k for k in range(K) if is_commit[k]]
        cp = np.array([cpace[D["tpl"][k]["group"]] for k in pace_k])
        for li, leaf in enumerate(self.leaves):
            path = D["anc"][leaf]
            # W~ = W - psi U + c_pace (commitments - plan) - range charges + draws accrued at the static-SAA return
            ex = E().add([self.WT[li], self.W[leaf], self.HU[leaf], self.TU[leaf]], [1.0, -1.0, psi, psi])
            rhs_w = 0.0
            a2l = D["a2"][leaf]
            for m in path:
                if self.lvl[m] <= 2:
                    ex.add(self.Y[m][pace_k], -cp)
                    rhs_w -= float((cp * plan[pace_k]).sum())
                    if cls[m] != 2:
                        ex.add(self.BRK[m], rng_ch)
            ex.add(self.Y[a2l][pace_k], -2 * cp)              # fan years 3 and 4 repeat the stage-2 commitments
            rhs_w -= 2 * float((cp * plan[pace_k]).sum())
            for nn in path[1:]:
                ex.add(self.NR[self.par[nn]], -d_year[nn] * D["acc"][(li, nn)])
            rows["Wt"][li] = R(*ex.merged(), rhs_w, rhs_w, ("Wt", li))
            # H15 at leaves: non-red liquidity covers next year's needs (margin <= 0)
            R([self.M[leaf], self.SL15[li]], [1.0, -1.0], -INF, 0.0, ("H15", li))
            # fan sleeve sales cannot cut a holding below zero (cq is cumulative, so the leaf row suffices):
            # per holding for the liquid sleeves, in aggregate for the amber and red emergency sleeves
            for i in np.flatnonzero(sl <= 1):
                R([self.X[a2l, i], self.CQ[leaf, sl[i]]], [1.0, -1.0], 0.0, INF, ("cqpos", li, i))
            for s_ in (2, 3):
                mem = np.flatnonzero(sl == s_)
                R(np.r_[self.X[a2l, mem], self.CQ[leaf, s_]], np.r_[V[leaf, mem], -V[leaf, mem].sum()], 0.0, INF,
                  ("cqpos_agg", li, s_))
        # H9 red-event CVaR surrogate over each path's decision nodes AND fan years
        thr = cn("red_sale_threshold")
        if opt:
            for li, leaf in enumerate(self.leaves):
                for nn in D["anc"][leaf]:
                    R([self.Z[li], self.M[nn], self.ETA_R[0]], [1.0, -1.0, 1.0], 0.0, INF, ("H9m", li, nn))
                    R([self.Z[li], self.RS[nn], self.ETA_R[0]], [1.0, -1.0, 1.0], -thr, INF, ("H9s", li, nn))
            eps = cn("red_eps_tree")
            ex = E().add(self.ETA_R, eps).add(self.Z, p_leaf).add(self.SL9, -1.0)
            rows["H9"] = R(*ex.merged(), -INF, 0.0, ("H9", 0))
            # H10 multi-level relative depth guard
            rows["H10"] = []
            for k_, a_ in enumerate(lev):
                for li in range(L):
                    R([self.UU[li, k_], self.WT[li], self.ETA_A[k_]], [1.0, 1.0 / W0, 1.0], Wstar / W0, INF, ("H10u", li, k_))
                ex = E().add(self.ETA_A[k_], 1 - a_).add(self.UU[:, k_], p_leaf)
                rhs_ = (1 - a_) * (b0["cvar_X"][k_] + cn("depth_delta"))
                rows["H10"].append(R(*ex.merged(), -INF, rhs_, ("H10", k_)))
        # utility tangents (CRRA on real W~/W0), squared-shortfall secants, bisection auxiliaries
        gam = g("objective.crra_gamma")
        defl = (1 + g("goal.inflation")) ** g("goal.years")
        wlo, whi = g("objective.crra_w_range")
        wk = np.geomspace(wlo, whi, g("objective.crra_tangents"))
        Ufun = lambda w: w ** (1 - gam) / (1 - gam)
        Ud = lambda w: w ** (-gam)
        self.crra = (gam, defl, Ufun)
        segs = g("objective.l2_segments")
        brk = np.linspace(0, 1, segs + 1)
        for li in range(L):
            for w_ in wk:
                R([self.UTIL[li], self.WT[li]], [1.0, -Ud(w_) / (W0 * defl)], -INF, Ufun(w_) - Ud(w_) * w_, ("util", li))
            R([self.SH[li], self.WT[li]], [1.0, 1.0 / Wstar], 1.0, INF, ("sh", li))
            for j in range(segs):
                a_, b_ = brk[j], brk[j + 1]
                slope = a_ + b_
                icpt = -a_ * b_
                R([self.V2[li], self.SH[li]], [1.0, -slope], icpt, INF, ("v2", li))
            R([self.UB[li], self.WT[li], self.ETA_B[0]], [1.0, 1.0 / W0, 1.0], Wstar / W0, INF, ("bis", li))
        # tie-break / goal rows (inactive until used)
        ex = E().add(self.WT, p_leaf)
        rows["meanrow"] = R(*ex.merged(), -INF, INF, ("meanrow", 0))
        ex = E().add(self.ETA_B, 1.0).add(self.UB, p_leaf)     # scaled CVaR row: eta + (1/pb) sum p ub <= 0
        rows["cvarrow"] = R(*ex.merged(), -INF, INF, ("cvarrow", 0))
        # REBALANCE switch-off rows (inactive): group exposure share within +-1% of W of the status quo's
        rows["rebal"] = []
        if opt and "w_grp_b0" in b0:
            for n in range(ND):
                for gname in GROUPS:
                    exg = self._hold(E(), n, V, mask=gi[gname])
                    self._tpl_state(exg, n, "V", kmask=tgi[gname])
                    ce, ve = exg.merged()
                    wb = b0["w_grp_b0"][gname][n]
                    r1 = R(np.r_[ce, self.W[n]], np.r_[ve, -(wb + 0.01)], -INF, INF, ("rebal_hi", n, gname))
                    r2 = R(np.r_[ce, self.W[n]], np.r_[ve, -(wb - 0.01)], -INF, INF, ("rebal_lo", n, gname))
                    rows["rebal"].append((r1, r2))
        self.A_mat = B.matrix()
        self.lb, self.ub = lb, ub
        self.rlb = np.array(B.rlb)
        self.rub = np.array(B.rub)
        self.nvar, self.nrow = B.nv, B.nr
        self.cost = np.zeros(B.nv)

    # ------------------------------------------------------------------ solving
    def highs(self):
        if self.h is not None:
            return self.h
        h = highspy.Highs()
        h.setOptionValue("output_flag", False)
        h.setOptionValue("threads", int(self.g("solver.threads")))
        h.setOptionValue("primal_feasibility_tolerance", float(self.g("solver.feas_tol")))
        h.setOptionValue("dual_feasibility_tolerance", float(self.g("solver.feas_tol")))
        h.setOptionValue("random_seed", 0)
        A = self.A_mat.tocsc()
        lp = highspy.HighsLp()
        lp.num_col_ = self.nvar
        lp.num_row_ = self.nrow
        lp.col_cost_ = self.cost
        lp.col_lower_ = self.lb
        lp.col_upper_ = self.ub
        lp.row_lower_ = self.rlb
        lp.row_upper_ = self.rub
        lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
        lp.a_matrix_.start_ = A.indptr
        lp.a_matrix_.index_ = A.indices
        lp.a_matrix_.value_ = A.data
        h.passModel(lp)
        self.h = h
        self._cur_lb = self.lb.copy()
        self._cur_ub = self.ub.copy()
        self._cur_rlb = self.rlb.copy()
        self._cur_rub = self.rub.copy()
        self._cur_cost = self.cost.copy()
        return h

    def set_cost(self, cost):
        h = self.highs()
        idx = np.flatnonzero(cost != self._cur_cost)
        if len(idx):
            h.changeColsCost(len(idx), idx.astype(np.int32), cost[idx].astype(float))
            self._cur_cost = cost.copy()

    def set_col_bounds(self, idx, lo, hi):
        h = self.highs()
        idx = np.atleast_1d(np.asarray(idx, np.int32))
        lo = np.broadcast_to(np.asarray(lo, float), idx.shape).copy()
        hi = np.broadcast_to(np.asarray(hi, float), idx.shape).copy()
        h.changeColsBounds(len(idx), idx, lo, hi)
        self._cur_lb[idx] = lo
        self._cur_ub[idx] = hi

    def set_row_bounds(self, r, lo, hi):
        h = self.highs()
        h.changeRowBounds(int(r), float(lo), float(hi))
        self._cur_rlb[r] = lo
        self._cur_rub[r] = hi

    def clear(self):
        """Forget the basis (deterministic restarts for independent tasks)."""
        if self.h is not None:
            self.h.clearSolver()

    def run(self, name, kind="LP", sense_max=False, method="ipm"):
        h = self.highs()
        h.setOptionValue("solver", "ipm" if method == "ipm" else "simplex")
        h.setOptionValue("run_crossover", "on")
        t0 = time.time()
        h.run()
        dt = time.time() - t0
        st = h.getModelStatus()
        status = h.modelStatusToString(st)
        info = h.getInfo()
        sol = h.getSolution()
        ok = st == highspy.HighsModelStatus.kOptimal
        x = np.array(sol.col_value) if ok else None
        y = np.array(sol.row_dual) if ok else None
        self.last_rc = np.array(sol.col_dual) if ok else None
        obj = info.objective_function_value if ok else None
        rec = {"name": name, "kind": kind, "status": status, "cols": int(self.nvar), "rows": int(self.nrow),
               "nnz": int(self.A_mat.nnz), "time_s": dt, "obj": (-obj if (sense_max and obj is not None) else obj),
               "iters": int(info.simplex_iteration_count), "ipm_iters": int(info.ipm_iteration_count),
               "method": method}
        self.solves.append(rec)
        if self.log is not None and hasattr(self.log, "solve"):
            self.log.solve(rec)
        return x, y, rec

    # ------------------------------------------------------------------ objectives
    def obj_mean(self):
        c = np.zeros(self.nvar)
        c[self.WT] = -self.p_leaf
        return c

    def obj_util(self, lam_l2=0.0):
        c = np.zeros(self.nvar)
        c[self.UTIL] = -self.p_leaf
        if lam_l2:
            c[self.V2] = lam_l2 * self.p_leaf
        return c

    def obj_b0(self):
        """Status-quo funding waterfall in the tree: Treasury first (free), then long-only, hedge funds, revolver,
        amber, red; revolver balances carry a small cost so they are repaid when cash allows."""
        pen = self.g("baselines.b0_penalties")
        c = np.zeros(self.nvar)
        pn = self.prob
        for s_, k in enumerate(["LIQ", "HF", "AMB", "RED"]):
            c[self.QS[:, s_]] = pen[k] * pn
        c[self.DR[:, 0]] = pen["REV"] * pn
        c[self.FB[:, 0]] = pen["REV_BAL"] * pn
        return c

    def eval_expr(self, ex: E, x):
        cc, vv = ex.merged()
        return float(np.dot(vv, x[cc]) + ex.k)

    def group_value(self, x, n, gname):
        D = self.D
        ex = self._hold(E(), n, D["V"], mask=(D["group"] == gname).astype(float))
        self._tpl_state(ex, n, "V", kmask=(D["tpl_group"] == gname))
        return self.eval_expr(ex, x)

    def leaf_values(self, x):
        return x[self.WT]
