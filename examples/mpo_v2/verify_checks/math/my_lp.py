"""SYNTHETIC - NOT ADIC DATA. Independent re-implementation of the MPO v2 tree LP, for verification only.

Written from the economic definitions (DSGO sections 1.3, 4.1, 4.6, 4.7 and the rationales in params.json), with its
own row builder and NO aggregate state variables: holding values, template values, unfunded, pledge pools and stressed
flows are inline linear expressions of the decision columns. Parameters are read straight from params.json. The tree
data (per-node trajectories of every holding and per-$ template, bids, draws, classes) is taken from the prepared ledger
arrays D, because the verification target is the optimizer, not the data generator; the accrual factors, sleeve
aggregates and trade caps are recomputed here from their definitions and compared.

Column names and shapes follow the author's so that solutions can be compared column by column.
"""
from __future__ import annotations

import json

import numpy as np
import scipy.sparse as sp

GROUPS = ["PE", "SEC", "CO", "CS", "PC", "HF", "LO", "RA"]
FINS = ["REV", "TERM", "NAVF", "PREF", "CSBL", "SMABL", "RACO"]


class PJ:
    def __init__(self, path):
        self.raw = json.load(open(path, encoding="utf-8"))

    def __call__(self, key):
        node = self.raw
        for part in key.split("."):
            node = node[part]
        return node["value"]


class MyLP:
    def __init__(self, D, pj: PJ, b0: dict, mode="OPT", delta=None, eps_red=None, h4_net_revolver=False,
                 log=None):
        self.D, self.pj, self.b0, self.mode = D, pj, b0, mode
        self.opt = mode == "OPT"
        self.delta = pj("constraints.depth_delta") if delta is None else delta
        self.eps_red = pj("constraints.red_eps_tree") if eps_red is None else eps_red
        self.h4_net = h4_net_revolver
        self.log = log or (lambda s: None)
        self._setup()
        self._vars()
        self._rows()
        self._finish()

    # ------------------------------------------------------------------ data
    def _setup(self):
        D, pj = self.D, self.pj
        tr = D["tr"]
        self.T = int(tr["T"])
        self.lvl = np.asarray(tr["level"])
        self.par = np.asarray(tr["parent"])
        self.cls = np.asarray(tr["cls"])
        self.prob = np.asarray(tr["prob"])
        self.leaves = np.asarray(D["leaves"])
        self.ND = int((self.lvl <= 2).sum())
        self.I = len(D["units"])
        self.K = len(D["tpl"])
        self.rf = pj("rates.sofr")
        self.erf = np.exp(self.rf)
        # ancestors (root .. n) and stage-2 ancestor, recomputed from the parent pointers
        self.anc = []
        self.a2 = np.full(self.T, -1)
        for n in range(self.T):
            a, j = [], n
            while j >= 0:
                a.append(j)
                j = self.par[j]
            a = a[::-1]
            self.anc.append(a)
            if self.lvl[n] >= 2:
                self.a2[n] = a[2]
        assert all(list(self.anc[n]) == list(D["anc"][n]) for n in range(self.T))
        self.dec = np.array([n if n < self.ND else self.a2[n] for n in range(self.T)])
        units = D["units"]
        self.group = np.array([u["group"] for u in units])
        tier = np.array([u["tier"] for u in units])
        self.liquid = tier == "liquid"
        self.red = tier == "red"
        self.amber = tier == "amber"
        self.sl = np.array([0 if g == "LO" else 1 if g == "HF" else 2 if t == "amber" else 3
                            for g, t in zip(self.group, tier)])
        self.is_hf = self.group == "HF"
        self.hf_units = np.flatnonzero(self.is_hf)
        self.is_lo_eq = np.array([u["group"] == "LO" and u["segment"] != "lo_fi" for u in units])
        self.fi = int(np.flatnonzero([u["segment"] == "lo_fi" for u in units])[0])
        self.lo1 = [u["id"] for u in units].index("LO-01")
        self.is_pledge = np.array(["pledge_pool" in u["flags"] for u in units])
        self.is_private = np.isin(self.group, ["PE", "SEC", "CO", "CS", "PC", "RA"])
        self.is_cs = self.group == "CS"
        self.is_sma = np.array(["sma" in u["flags"] for u in units])
        self.is_ra_ctrl = np.array([u["group"] == "RA" and "controlled" in u["flags"] for u in units])
        self.is_re_open = np.array(["open_end" in u["flags"] for u in units])
        self.V, self.N, self.U = D["V"], D["N"], D["U"]
        self.Dist, self.Call, self.G = D["D"], D["C"], D["G"]
        self.proc, self.proc_norm = D["proc"], D["proc_norm"]
        tc = pj("trading.tc")
        self.tc_add = np.array([(tc["hf"] if u["group"] == "HF" else tc.get(u["bid_key"], 0.001)) if u["tier"] == "liquid"
                                else 0.0 for u in units])
        # sleeve aggregates recomputed: value at full original positions and value-weighted bid
        self.S_sl = np.stack([self.V[:, self.sl == s].sum(1) for s in range(4)], 1)
        self.bid_sl = np.stack([self.proc[:, self.sl == s].sum(1) / np.maximum(self.S_sl[:, s], 1e-9) for s in range(4)], 1)
        self.chk = {"S_sl": float(np.max(np.abs(self.S_sl - D["S_sl"]))), "bid_sl": float(np.max(np.abs(self.bid_sl - D["bid_sl"])))}
        V0 = np.array([u["nav_econ"] for u in units])
        self.W0 = float(V0.sum() + pj("treasury.cash0"))
        self.Wstar = self.W0 * (1 + pj("goal.rate")) ** pj("goal.years")
        self.chk["W0"] = abs(self.W0 - D["W0"])
        self.chk["Wstar"] = abs(self.Wstar - D["Wstar"])
        s_post = np.array([b["sigma_post"] for b in D["beliefs"]])
        self.cap_trade = pj("trading.k_sel") * self.W0 * float(np.median(s_post)) / s_post
        self.chk["cap_trade"] = float(np.max(np.abs(self.cap_trade - D["cap_trade"])))
        # static-SAA return and accrual factors recomputed
        fb = np.array(pj("overlay.beta_fin_spread"))
        w_u = V0 / self.W0
        w_c = pj("treasury.cash0") / self.W0
        r_saa = (self.G - 1.0) @ w_u + w_c * (self.erf - 1.0) + pj("overlay.beta_sq") / self.W0 * (D["Geq"] - self.erf - fb[self.cls])
        r_saa[0] = 0.0
        self.r_saa = r_saa
        self.chk["r_saa"] = float(np.max(np.abs(r_saa - D["r_saa"])))
        self.acc = {}
        for li, leaf in enumerate(self.leaves):
            path = self.anc[leaf]
            for k, nn in enumerate(path):
                self.acc[(li, nn)] = float(np.prod([1.0 + r_saa[m] for m in path[k + 1:]]))
        self.chk["acc"] = max(abs(self.acc[k] - D["acc"][k]) for k in self.acc)
        # stressed next-year calls and low distributions recomputed (drought call multiplier x crisis stress; frozen
        # distribution multiplier), as the margin rows define them
        mC = np.array(pj("private_engine.exit_call_mult"))
        mD = np.array(pj("private_engine.exit_dist_mult"))
        stress = pj("private_engine.crisis_call_stress")
        segs = [dict(pj(f"book.segments.{u['segment']}"), **{k: u[k] for k in ("B", "yield") if k in u}) for u in units]
        edges = np.array([s["edges"] for s in segs], float)
        calli = np.array([s["call"] for s in segs], float)
        disti = np.array([s["dist"] for s in segs], float)
        yld = np.array([u["yield"] for u in units], float)
        age = np.array([u["age"] for u in units], float)[None, :] + self.lvl[:, None]
        b = (age[..., None] >= edges[None]).sum(-1)
        ci = np.take_along_axis(calli[None].repeat(self.T, 0), b[..., None], 2)[..., 0]
        ei = np.take_along_axis(disti[None].repeat(self.T, 0), b[..., None], 2)[..., 0]
        callS = self.U * (1 - np.exp(-ci * mC[2] * stress))
        distL = self.V * (yld + (1 - np.exp(-ei * mD[3])))
        self.chk["callS"] = float(np.max(np.abs(callS - D["callS"])))
        self.chk["distL"] = float(np.max(np.abs(distL - D["distL"])))
        self.netS = callS - distL
        h4 = pj("constraints.h4")
        A0 = np.array([u["age"] for u in units], float)
        b0_ = (A0[:, None] >= edges).sum(-1)
        U0 = np.array([u["unfunded"] for u in units])
        c24 = U0 * (1 - np.exp(-calli[np.arange(self.I), b0_] * mC[2] * h4["call_mult"] * 2.0))
        d24 = V0 * (yld * 2.0 + (1 - np.exp(-disti[np.arange(self.I), b0_] * mD[2] * h4["dist_factor"] * 2.0)))
        self.chk["calls24"] = float(np.max(np.abs(c24 - D["calls24"])))
        self.chk["dist24"] = float(np.max(np.abs(d24 - D["dist24"])))
        self.net24 = c24 - d24
        # templates
        self.tnames = D["tpl_names"]
        self.tpl = D["tpl"]
        self.is_commit = np.array([t["kind"] == "commit" for t in self.tpl])
        self.plan = np.array([t.get("plan", 0.0) for t in self.tpl])
        self.tinit = D["tpl_init"]
        self.tarr = D["tpl_arr"]
        self.pair = D["pair_index"]
        self.tdebt = np.array([t["lever_debt"] for t in self.tpl])
        self.tspread = np.array([t["lever_spread"] for t in self.tpl])
        self.tgroup = np.array([t["group"] for t in self.tpl])
        self.tnetS_arr = D["tpl_callS"] - D["tpl_distL"]
        self.tnetS_init = D["tpl_init_callS"] - D["tpl_init_distL"]
        self.tnet24 = D["tpl_init_calls24"] - D["tpl_init_dist24"]
        # market
        self.Geq, self.tail, self.oppret = D["Geq"], D["tailpay"], D["oppret"]
        self.d_year, self.d_next = np.asarray(tr["d_year"]), np.asarray(tr["d_next"])
        self.first_str = np.asarray(tr["first_after_str"])
        b0 = self.b0
        T = self.T
        self.green = np.asarray(b0.get("green", np.zeros(T, bool)))
        self.behind = np.asarray(b0.get("behind", np.zeros(T, bool)))
        self.loss = np.asarray(b0.get("loss", np.zeros(T, bool)))
        self.black = np.asarray(b0.get("black", np.zeros(T, bool)))

    # ------------------------------------------------------------------ columns
    def _vars(self):
        pj, T, ND, I, K, L = self.pj, self.T, self.ND, self.I, self.K, len(self.leaves)
        self.blk, lbs, ubs = {}, [], []
        self.nv = 0

        def add(name, shape, lb=0.0, ub=np.inf):
            shape = tuple(np.atleast_1d(shape))
            n = int(np.prod(shape))
            self.blk[name] = np.arange(self.nv, self.nv + n).reshape(shape)
            lbs.append(np.broadcast_to(np.asarray(lb, float), shape).ravel().copy())
            ubs.append(np.broadcast_to(np.asarray(ub, float), shape).ravel().copy())
            self.nv += n

        H = len(self.hf_units)
        for nm, sh in (("x", (ND, I)), ("s", (ND, I)), ("a", (ND, I)), ("r", (ND, I)), ("y", (ND, K)), ("pu", ND),
                       ("pd", ND), ("pi", ND), ("trs", (ND, H)), ("hed", ND), ("opp", ND), ("brk", (ND, 8)), ("C", T),
                       ("IM", T), ("Q", T), ("E", T), ("LB", T), ("RS", T), ("beta", T), ("q", (T, 4)), ("cq", (T, 4)),
                       ("B", (T, 7)), ("dr", (T, 7)), ("rp", (T, 7)), ("Lup", 1), ("z", L), ("uu", (L, 3)), ("sh", L),
                       ("v2", L), ("ub", L)):
            add(nm, sh)
        for nm, sh in (("W", T), ("NR", T), ("LQ", T), ("M", T), ("Wt", L), ("eta_R", 1), ("eta_a", 3), ("util", L),
                       ("eta_b", 1)):
            add(nm, sh, -np.inf, np.inf)
        self.lb = np.concatenate(lbs)
        self.ub = np.concatenate(ubs)
        b = self.blk
        lb, ub = self.lb, self.ub
        opt = self.opt
        rec2 = opt and bool(pj("tree.stage2_recourse_only"))
        self.rec2 = rec2
        xmax = pj("trading.xmax_liquid")
        mr = pj("pacing.mult_range")
        rho_f = np.array(pj("bids.rho")["fund"])
        for n in range(ND):
            c = self.cls[n]
            st2 = rec2 and self.lvl[n] == 2
            ub[b["x"][n]] = np.where(self.liquid, xmax, 1.0)
            su = np.minimum(self.cap_trade / np.maximum(self.V[n], 1e-9), 1.0)
            if n == 0:
                su = np.where(self.red, 0.0, su)       # ADR-39: Amber today -> no planned red-tier sale at the root
            ub[b["s"][n]] = 0.0 if st2 else su
            ub[b["a"][n]] = 0.0 if st2 else np.where(self.liquid, self.cap_trade / np.maximum(self.V[n], 1e-9), 0.0)
            ub[b["r"][n]] = 0.0 if st2 else np.where(self.is_hf | self.is_re_open, 1.0, 0.0)
            if st2:
                ub[b["pu"][n]] = 0.0
                ub[b["pd"][n]] = 0.0
            for k, t in enumerate(self.tpl):
                col = b["y"][n, k]
                if t["kind"] == "commit":
                    lb[col], ub[col] = mr[0] * self.plan[k], mr[1] * self.plan[k]
                else:
                    ok = c in t["classes"]
                    if self.tnames[k] == "SEC_BUY":
                        ok = ok and (1 - rho_f[c] * self.D["theta_fund"][n]) > t["discount_gate"] and not self.black[n]
                    if t["green_only"]:
                        ok = ok and bool(self.green[n])
                    if st2:
                        ok = False
                    ub[col] = t["cap_year"] if ok else 0.0
        ub[b["pi"]] = pj("overlay.p2s_cap")
        ub[b["opp"]] = pj("overlay.opp_im_max")
        ub[b["Lup"]] = pj("corporate_finance.revolver_upsize_max")
        ub[b["cq"][:ND]] = 0.0
        ub[b["q"][0, 3]] = 0.0                      # no forced red-sleeve sale at the root
        ub[b["Q"][self.lvl >= 4]] = 0.0
        ub[b["B"][:, 6]] = pj("corporate_finance.raco")["cap"]
        cf = lambda k: pj(f"corporate_finance.{k}")
        avail = np.array([[1.0, 1.0, 1.0], cf("term_avail"), cf("navf")["avail"], cf("pref")["avail"], cf("csbl")["avail"],
                          cf("smabl")["avail"], cf("raco")["avail"]], float)
        for n in range(T):
            for j, f in enumerate(FINS):
                allow = avail[j, self.cls[n]] > 0
                if n >= ND or (rec2 and self.lvl[n] == 2):
                    allow = allow and f == "REV"
                if self.lvl[n] == 5:
                    allow = False
                ub[b["dr"][n, j]] = np.inf if allow else 0.0
        if opt:
            ub[b["LB"]] = pj("constraints.kappa_c") * np.maximum(0.0, -np.asarray(self.b0["M"]))
        else:
            ub[b["s"]] = 0.0
            ub[b["a"]] = 0.0
            ub[b["r"]] = 0.0
            for k in range(K):
                if self.is_commit[k]:
                    lb[b["y"][:, k]] = self.plan[k]
                    ub[b["y"][:, k]] = self.plan[k]
                else:
                    ub[b["y"][:, k]] = 0.0
            ub[b["pu"]] = 0.0
            ub[b["pd"]] = 0.0
            ub[b["trs"]] = 0.0
            lb[b["opp"]] = ub[b["opp"]] = pj("overlay.opp_im_sq")
            lb[b["beta"]] = ub[b["beta"]] = pj("overlay.beta_sq")
            ub[b["dr"][:, 1:]] = 0.0
            ub[b["Lup"]] = 0.0

    # ------------------------------------------------------------------ expressions
    def hold(self, at, field_row, mask=None):
        """sum_i holding_i(at) * field_row[i]; holdings at fan nodes are the stage-2 fractions minus sleeve cuts."""
        f = field_row if mask is None else field_row * mask
        X = self.blk["x"]
        if at < self.ND:
            return [(X[at], f)]
        out = [(X[self.a2[at]], f)]
        for s in range(4):
            tot = float(f[self.sl == s].sum())
            if tot != 0.0:
                out.append((self.blk["cq"][at, s], -tot))
        return out

    def _tval(self, m, n, key, init_key=None):
        if m == n:
            src = self.tinit[key] if init_key is None else init_key
            return src[m]
        return self.tarr[key][self.pair[(m, n)]]

    def tstate(self, n, key, kmask=None, init_key=None, arr_key=None):
        """sum over template positions held at n: purchases/commitments at decision ancestors (incl. n) and fan
        commitments at levels 3-4 (at the stage-2 level)."""
        km = np.ones(self.K) if kmask is None else kmask.astype(float)
        Y = self.blk["y"]
        out = []
        for m in self.anc[n]:
            if m == n:
                v = (self.tinit[key][m] if init_key is None else init_key[m])
            else:
                v = (self.tarr[key] if arr_key is None else arr_key)[self.pair[(m, n)]]
            if self.lvl[m] <= 2:
                out.append((Y[m], v * km))
            elif self.lvl[m] in (3, 4):
                out.append((Y[self.a2[n]], v * km * self.is_commit))
        return out

    def tflow(self, n, key):
        p = self.par[n]
        Y = self.blk["y"]
        out = []
        for m in self.anc[p]:
            v = self.tarr[key][self.pair[(m, n)]]
            if self.lvl[m] <= 2:
                out.append((Y[m], v))
            elif self.lvl[m] in (3, 4):
                out.append((Y[self.a2[n]], v * self.is_commit))
        return out

    def tdebt_terms(self, n, scale=1.0):
        Y = self.blk["y"]
        return [(Y[m], self.tdebt * scale) for m in self.anc[n] if self.lvl[m] <= 2]

    def tdebt_int(self, n):
        Y = self.blk["y"]
        return [(Y[m], self.tdebt * (self.rf + self.tspread)) for m in self.anc[n] if self.lvl[m] <= 2]

    @staticmethod
    def neg(terms, s=-1.0):
        return [(c, np.asarray(v, float) * s) for c, v in terms]

    # ------------------------------------------------------------------ rows
    def _rows(self):
        pj, D = self.pj, self.D
        b = self.blk
        T, ND, I, K = self.T, self.ND, self.I, self.K
        R_r, R_c, R_v, R_lo, R_hi, tags = [], [], [], [], [], []
        self.rid = {}

        def row(terms, lo, hi, tag):
            cs, vs = [], []
            for c, v in terms:
                c = np.atleast_1d(np.asarray(c)).ravel()
                v = np.broadcast_to(np.asarray(v, float), c.shape).ravel()
                cs.append(c)
                vs.append(v)
            c = np.concatenate(cs)
            v = np.concatenate(vs)
            r = len(R_lo)
            R_r.append(np.full(len(c), r))
            R_c.append(c)
            R_v.append(v)
            R_lo.append(lo)
            R_hi.append(hi)
            tags.append(tag)
            self.rid.setdefault(tag[0], []).append(r)
            return r

        self.row = row
        cf = lambda k: pj(f"corporate_finance.{k}")
        ov = lambda k: pj(f"overlay.{k}")
        cn = lambda k: pj(f"constraints.{k}")
        opt, rec2 = self.opt, self.rec2
        rf, erf = self.rf, self.erf
        imr = np.array(ov("im_rate"))
        fbs = np.array(ov("beta_fin_spread"))
        fps = np.array(ov("p2s_fin_spread"))
        navf, pref, csbl, smabl, raco = cf("navf"), cf("pref"), cf("csbl"), cf("smabl"), cf("raco")
        Ls = cf("revolver_signed")
        fee_u = cf("revolver_undrawn_fee")
        rate = np.zeros((7, 3))
        rate[0] = rf + cf("revolver_spread")
        rate[1] = rf + cf("term_spread")
        rate[2] = rf + np.array(navf["spread"])
        rate[3] = np.array(pref["rate"])
        rate[4] = rf + csbl["spread"]
        rate[5] = rf + smabl["spread"]
        rate[6] = rf + np.array(raco["spread"])
        pik = np.array([False, False, navf["pik"], True, False, False, False])
        oid = np.array([0.0, 0.0, navf["oid"], pref["fee"], 0.0, 0.0, 0.0])
        self.rate, self.pik = rate, pik
        rev_av = np.array(cf("revolver_avail"))
        phi_hf = np.array(pj("trading.redeem_phi")["hf"])
        phi_re = np.array(pj("trading.redeem_phi")["re_open_end"])
        phi = np.where(self.is_hf[:, None], phi_hf[None, :], np.where(self.is_re_open[:, None], phi_re[None, :], 0.0))
        hfi = pj("treasury.fi_liquidity_weight")
        prem = ov("tail_premium")
        hmin = ov("tail_budget")[0] / prem
        hmax = ov("tail_budget")[1] / prem
        tc_lo = pj("trading.tc")["lo_dm"]
        caps_cls = np.array(cn("class_caps"))
        gmask = {g: (self.group == g).astype(float) for g in GROUPS}
        tgm = {g: (self.tgroup == g) for g in GROUPS}
        V, Nn, U = self.V, self.N, self.U
        w_grp = {g: float((V[0] * gmask[g]).sum() / self.W0) for g in GROUPS}
        x, s_, a_, r_, y = b["x"], b["s"], b["a"], b["r"], b["y"]
        mr = pj("pacing.mult_range")
        self.vm_c = None
        for n in range(T):
            p = self.par[n]
            c = self.cls[n]
            lv = self.lvl[n]
            dn = self.dec[n]
            isdec = n < ND
            st2 = rec2 and lv == 2
            Hval = self.hold(n, V[n])
            Tval = self.tstate(n, "V")
            Tdeb = self.tdebt_terms(n)
            # ---- holdings balance and P2S position (decision nodes)
            if isdec:
                for i in range(I):
                    t = [(x[n, i], 1.0), (s_[n, i], 1.0), (a_[n, i], -1.0), (r_[n, i], 1.0),
                         (b["q"][n, self.sl[i]], 1.0 / max(self.S_sl[n, self.sl[i]], 1e-9))]
                    if p >= 0:
                        t.append((x[p, i], -1.0))
                    if i == self.lo1:
                        t += [(b["pu"][n], 1.0 / V[n, i]), (b["pd"][n], -1.0 / V[n, i])]
                    row(t, 1.0 if p < 0 else 0.0, 1.0 if p < 0 else 0.0, ("xbal", n, i))
                t = [(b["pi"][n], 1.0), (b["pu"][n], -1.0), (b["pd"][n], 1.0)]
                if p >= 0:
                    t.append((b["pi"][p], -1.0))
                row(t, 0.0, 0.0, ("p2s", n))
                if st2:
                    for k in np.flatnonzero(self.is_commit):
                        row([(y[n, k], 1.0), (y[p, k], -1.0)], 0.0, 0.0, ("carry_pace", n, k))
                    for h in range(len(self.hf_units)):
                        row([(b["trs"][n, h], 1.0), (b["trs"][p, h], -1.0)], 0.0, 0.0, ("carry_trs", n, h))
                    row([(b["hed"][n], 1.0), (b["hed"][p], -1.0)], 0.0, 0.0, ("carry_hed", n))
                    row([(b["opp"][n], 1.0), (b["opp"][p], -1.0)], 0.0, 0.0, ("carry_opp", n))
                    row([(b["beta"][n], 1.0), (b["beta"][p], -1.0)], -np.inf, 0.0, ("betacut", n))
            else:
                for s in range(4):
                    t = [(b["cq"][n, s], 1.0), (b["q"][n, s], -1.0 / max(self.S_sl[n, s], 1e-9))]
                    if p >= ND:
                        t.append((b["cq"][p, s], -1.0))
                    row(t, 0.0, 0.0, ("cq", n, s))
                row([(b["beta"][n], 1.0), (b["beta"][p], -1.0)], -np.inf, 0.0, ("betacut", n))
            # ---- initial margin
            row([(b["IM"][n], 1.0), (b["beta"][n], -imr[c]), (b["pi"][dn], -imr[c]), (b["trs"][dn], -ov("trs_ia")),
                 (b["opp"][dn], -1.0)], 0.0, 0.0, ("IM", n))
            # ---- economic NAV and reported NAV (every financing claim at face, template asset debt)
            t = [(b["W"][n], 1.0), (b["C"][n], -1.0), (b["IM"][n], -1.0), (b["Q"][n], -1.0), (b["B"][n], 1.0)]
            t += self.neg(Hval) + self.neg(Tval) + Tdeb
            row(t, 0.0, 0.0, ("W", n))
            t = [(b["NR"][n], 1.0), (b["C"][n], -1.0), (b["IM"][n], -1.0), (b["Q"][n], -1.0), (b["B"][n], 1.0)]
            t += self.neg(self.hold(n, Nn[n])) + self.neg(self.tstate(n, "N")) + Tdeb
            row(t, 0.0, 0.0, ("NR", n))
            # ---- exposure
            t = [(b["E"][n], 1.0), (b["beta"][n], -1.0), (b["pi"][dn], -1.0), (b["trs"][dn], -1.0)]
            t += self.neg(Hval) + self.neg(Tval)
            row(t, 0.0, 0.0, ("E", n))
            # ---- IG + cash
            fmask = np.zeros(I)
            fmask[self.fi] = 1.0
            t = [(b["LQ"][n], 1.0), (b["C"][n], -1.0)] + self.neg(self.hold(n, V[n], fmask), -hfi)
            row(t, 0.0, 0.0, ("LQ", n))
            # ---- cash and posted margin
            t = [(b["C"][n], 1.0), (b["IM"][n], 1.0)]
            rhs = 0.0
            if p < 0:
                rhs = pj("treasury.cash0")
                t.append((b["Lup"][0], cf("revolver_upfront_fee") * 3))
            else:
                pdn = self.dec[p]
                t += [(b["C"][p], -erf), (b["IM"][p], -erf), (b["Q"][p], -erf)]
                t += self.neg(self.hold(p, self.Dist[n] - self.Call[n]))       # holdings' flows (held at the parent)
                t += self.neg(self.tflow(n, "D")) + self.tflow(n, "C")
                t += self.tdebt_int(p)
                t.append((b["NR"][p], self.d_year[n]))                           # owner draw, no slack (H1)
                for j in range(7):
                    if not pik[j]:
                        t.append((b["B"][p, j], rate[j, c]))
                t += [(b["B"][p, 0], -fee_u), (b["Lup"][0], fee_u)]
                rhs = -fee_u * Ls
                t.append((b["pi"][pdn], -(self.Geq[n] - erf - fps[c])))
                t.append((b["beta"][p], -(self.Geq[n] - erf - fbs[c])))
                for h, iu in enumerate(self.hf_units):
                    t.append((b["trs"][pdn, h], -(self.G[n, iu] - erf - ov("trs_fin_spread"))))
                t.append((b["hed"][pdn], -self.tail[n]))
                t.append((b["opp"][pdn], -self.oppret[n]))
                if p < ND:
                    t.append((r_[p], -(phi[:, c] * V[n])))
            if lv < 5:
                t.append((b["hed"][dn], prem))
            if isdec:
                t += [(s_[n], -self.proc[n]), (a_[n], V[n] * (1 + self.tc_add)),
                      (y[n], np.where(self.is_commit, 0.0, 1.0)), (b["pu"][n], -(1 - tc_lo)), (b["pd"][n], 1 + tc_lo)]
            t += [(b["q"][n], -self.bid_sl[n]), (b["dr"][n], -(1 - oid)), (b["rp"][n], 1.0)]
            row(t, rhs, rhs, ("cash", n))
            # ---- redemption queue
            if 1 <= lv <= 3 and p < ND:
                row([(b["Q"][n], 1.0), (r_[p], -((1 - phi[:, c]) * V[n]))], 0.0, 0.0, ("Q", n))
            elif lv == 0:
                row([(b["Q"][n], 1.0)], 0.0, 0.0, ("Q", n))
            # ---- debt balances (PIK accrues) and caps
            for j in range(7):
                t = [(b["B"][n, j], 1.0), (b["dr"][n, j], -1.0), (b["rp"][n, j], 1.0)]
                if p >= 0:
                    t.append((b["B"][p, j], -(1.0 + (rate[j, c] if pik[j] else 0.0))))
                row(t, 0.0, 0.0, ("bal", n, j))
            row([(b["B"][n, 0], 1.0), (b["Lup"][0], -rev_av[c] * (1.0 if lv >= 1 else 0.0))], -np.inf, rev_av[c] * Ls,
                ("revcap", n))
            row([(b["B"][n, 0], 1.0), (b["B"][n, 1], 1.0), (b["W"][n], -cf("recourse_cap"))], -np.inf, 0.0, ("recourse", n))
            pool = self.hold(n, V[n], self.is_pledge.astype(float))
            pvt = self.hold(n, V[n], self.is_private.astype(float)) + Tval
            row([(b["B"][n, 2], 1.0)] + self.neg(pool, -navf["ltv"][c]), -np.inf, 0.0, ("navf_ltv", n))
            row([(b["B"][n, 2], 1.0)] + self.neg(pvt, -navf["ltv"][c] * navf["pool_cap_share"]), -np.inf, 0.0, ("navf_pool", n))
            row([(b["B"][n, 3], 1.0)] + self.neg(pool, -pref["advance"]), -np.inf, 0.0, ("pref_cap", n))
            row([(b["B"][n, 4], 1.0)] + self.neg(self.hold(n, V[n], self.is_cs.astype(float)), -csbl["debt_to_value"]),
                -np.inf, 0.0, ("csbl", n))
            row([(b["B"][n, 5], 1.0)] + self.neg(self.hold(n, V[n], self.is_sma.astype(float)), -smabl["ltv"]),
                -np.inf, 0.0, ("smabl", n))
            row([(b["B"][n, 6], 1.0)] + self.neg(self.hold(n, V[n], self.is_ra_ctrl.astype(float)), -raco["ltv"]),
                -np.inf, 0.0, ("raco", n))
            # encumbered collateral (debt / LTV) <= 20% of total assets (W + financing debt)
            ltv_j = np.array([navf["ltv"][0], pref["advance"], csbl["debt_to_value"], smabl["ltv"], raco["ltv"]])
            ec = cf("encumbrance_cap")
            row([(b["B"][n, 2:7], 1.0 / ltv_j), (b["B"][n], -ec), (b["W"][n], -ec)], -np.inf, 0.0, ("encumb", n))
            # ---- floors (H2)
            row([(b["LQ"][n], 1.0), (b["W"][n], -cn("floor_hard"))], 0.0, np.inf, ("floor4", n))
            if opt and c in (0, 1) and not self.first_str[n]:
                row([(b["LQ"][n], 1.0), (b["W"][n], -cn("floor_target"))], 0.0, np.inf, ("floor8", n))
            # ---- leverage (H5; G5 class / behind caps)
            cap = cn("lev_cap")
            if opt:
                cc = self.cls[p] if (c == 2 and n > 0 and self.cls[p] != 2) else c
                cap = min(cap, caps_cls[cc])
                if self.behind[n]:
                    cap = 1.0 + cn("behind_cap_share") * (caps_cls[cc] - 1.0)
            row([(b["E"][n], 1.0), (b["W"][n], -cap)], -np.inf, 0.0, ("lev", n))
            row([(b["beta"][n], 1.0), (b["pi"][dn], 1.0), (b["trs"][dn], 1.0), (b["W"][n], -ov("gross_max"))], -np.inf, 0.0,
                ("gross", n))
            # ---- G5 liquidity cushion, G4 no doubling down (exogenous status-quo readings)
            if opt:
                row([(b["LB"][n], 1.0), (b["E"][n], -1.0), (b["W"][n], 1.0)], 0.0, np.inf, ("lbor", n))
                if n > 0 and (self.behind[n] or self.loss[n]):
                    ratio = self.b0["W"][n] / max(self.b0["W"][p], 1e-9)
                    row([(b["E"][n], 1.0), (b["E"][p], -ratio)], -np.inf, 0.0, ("g4", n))
                    if isdec:
                        row([(b["beta"][n], 1.0), (b["trs"][n], 1.0), (b["beta"][p], -1.0), (b["trs"][p], -1.0)], -np.inf, 0.0,
                            ("g4lev", n))
                        pm = ~self.is_commit
                        row([(y[n][pm], 1.0), (y[p][pm], -1.0)], -np.inf, 0.0, ("g4add", n))
            # ---- red-tier sales (ADR-39) and the signed red margin (H9)
            t = [(b["RS"][n], 1.0), (b["q"][n, 3], -self.bid_sl[n, 3])]
            if isdec:
                evt = self.red & ((not self.green[n]) | (self.proc[n] / np.maximum(self.proc_norm[n], 1e-12) < cn("red_bid_ratio")))
                t.append((s_[n], -self.proc[n] * evt))
            row(t, 0.0, 0.0, ("RS", n))
            vm = cn("margin_vm_drop") + (imr[2] - imr[c])
            needs = [(b["NR"][n], self.d_next[n])] + self.hold(n, self.netS[n]) + \
                self.tstate(n, "V", init_key=self.tnetS_init, arr_key=self.tnetS_arr) + \
                [(b["B"][n], rate[:, 2])] + self.tdebt_int(n) + [(b["beta"][n], vm), (b["pi"][dn], vm)]
            capac = [(b["LQ"][n], 1.0), (b["W"][n], -cn("floor_hard"))] + \
                self.hold(n, V[n] * (1 - cn("margin_lo_haircut")), self.is_lo_eq.astype(float)) + \
                self.hold(n, V[n] * cn("margin_hf_phi"), self.is_hf.astype(float)) + \
                self.hold(n, V[n] * cn("margin_amber_share") * 0.80, self.amber.astype(float)) + \
                [(b["Lup"][0], rev_av[2] * (1.0 if lv >= 1 else 0.0)), (b["B"][n, 0], -1.0), (b["Q"][n], 1.0)]
            # M = needs - capacity - rev_av[STR] * Ls
            row([(b["M"][n], 1.0)] + self.neg(needs) + capac, -rev_av[2] * Ls, -rev_av[2] * Ls, ("M", n))
            # ---- H3 six-month coverage (decision nodes)
            if isdec and opt:
                hs = cn("h3_share")
                t = [(b["LQ"][n], 1.0), (b["W"][n], -cn("floor_hard"))] + \
                    self.hold(n, V[n] * (1 - cn("margin_lo_haircut")), self.is_lo_eq.astype(float)) + \
                    self.hold(n, V[n] * cn("h3_hf_phi"), self.is_hf.astype(float)) + \
                    [(b["Lup"][0], rev_av[c] * (1.0 if lv >= 1 else 0.0)), (b["B"][n, 0], -1.0)] + \
                    self.neg([(b["NR"][n], self.d_next[n])] + self.hold(n, self.netS[n]) +
                             self.tstate(n, "V", init_key=self.tnetS_init, arr_key=self.tnetS_arr), -hs)
                row(t, -rev_av[c] * Ls, np.inf, ("H3", n))
            # ---- H11 overcommitment (STR exempt)
            if opt and c != 2:
                t = pvt + self.hold(n, U[n]) + self.tstate(n, "U") + [(b["W"][n], -cn("overcommit"))]
                row(t, -np.inf, 0.0, ("H11", n))
            # ---- H16 need-based funding: sleeve proceeds <= this year's outflows + floor restoration (+ repayments)
            calls_ub = 0.0
            t = [(b["q"][n], self.bid_sl[n]), (b["W"][n], -cn("floor_target")), (b["rp"][n], -1.0)]
            if p >= 0:
                calls_ub = float(self.Call[n].sum())
                for m in self.anc[p]:
                    if (m, n) in self.pair:
                        calls_ub += float((self.tarr["C"][self.pair[(m, n)]] * self.plan * mr[1]).sum())
                t.append((b["NR"][p], -self.d_year[n]))
                t.append((b["B"][p], -rate[:, c]))
                t.append((b["hed"][self.dec[p]], -prem))
            row(t, -np.inf, calls_ub, ("need", n))
            # ---- sleeve depth per year
            for s, share in ((1, pj("trading.hf_secondary_share")), (2, cn("margin_amber_share")),
                             (3, pj("trading.co_sale_share"))):
                if isdec and p >= 0:
                    row([(b["q"][n, s], 1.0), (x[p], -share * V[n] * (self.sl == s))], -np.inf, 0.0, ("sdepth", n, s))
                else:
                    row([(b["q"][n, s], 1.0)], -np.inf, share * self.S_sl[n, s], ("sdepth", n, s))
            # ---- decision-node rows
            if isdec:
                lpm = np.isin(self.group, ["PE", "SEC"]).astype(float)
                row([(s_[n], self.proc[n] * lpm)], -np.inf, pj("trading.lp_depth_year")[c], ("depth_lp", n))
                for g, share in (("CO", pj("trading.co_sale_share")), ("RA", pj("trading.ra_sale_share")[c]),
                                 ("CS", pj("trading.amber_sale_share")["CS"][c]), ("PC", pj("trading.amber_sale_share")["PC"][c]),
                                 ("HF", pj("trading.hf_secondary_share"))):
                    mk = gmask[g]
                    if p >= 0:
                        row([(s_[n], V[n] * mk), (x[p], -share * V[n] * mk)], -np.inf, 0.0, ("depth", n, g))
                    else:
                        row([(s_[n], V[n] * mk)], -np.inf, share * float((V[n] * mk).sum()), ("depth", n, g))
                if not st2:
                    for h, iu in enumerate(self.hf_units):
                        row([(b["trs"][n, h], 1.0), (x[n, iu], -ov("trs_cap_share") * V[n, iu])], -np.inf, 0.0, ("trscap", n, h))
                    row([(b["hed"][n], 1.0), (b["W"][n], -hmin)], 0.0, np.inf, ("hedlo", n))
                    row([(b["hed"][n], 1.0), (b["W"][n], -(hmax if opt else hmin))], -np.inf, 0.0, ("hedhi", n))
                if c != 2:
                    lo_b, hi_b = cn("range_band")
                    for gk, g in enumerate(GROUPS):
                        gv = self.hold(n, V[n], gmask[g]) + self.tstate(n, "V", kmask=tgm[g])
                        row(self.neg(gv) + [(b["brk"][n, gk], 1.0), (b["W"][n], hi_b * w_grp[g])], 0.0, np.inf, ("brk_hi", n, g))
                        row(gv + [(b["brk"][n, gk], 1.0), (b["W"][n], -lo_b * w_grp[g])], 0.0, np.inf, ("brk_lo", n, g))
                ks = self.tnames.index("SEC_BUY")
                if self.ub[y[n, ks]] > 0:
                    gv = self.hold(n, V[n], gmask["SEC"]) + self.tstate(n, "V", kmask=tgm["SEC"])
                    row(gv + [(b["W"][n], -pj("templates.SEC_BUY")["group_cap_share"])], -np.inf, 0.0, ("seccap", n))
        # ---- H4: 24-month named stress at the root
        if opt:
            h4 = cn("h4")
            t = [(b["LQ"][0], 1.0), (b["W"][0], -cn("floor_hard"))]
            t += self.hold(0, V[0] * (1 - h4["equity_drop"]), self.is_lo_eq.astype(float))
            t += self.hold(0, V[0] * h4["hf_pass"], self.is_hf.astype(float))
            t += self.neg(self.hold(0, V[0], self.is_pledge.astype(float)), h4["navf_ltv"])
            t += [(b["B"][0, 2], -1.0), (b["NR"][0], -2 * h4["draw_rate"])]
            t += self.neg(self.hold(0, self.net24))
            t += [(y[0], -self.tnet24), (b["B"][0], -2 * rate[:, 2])]
            t += [(b["beta"][0], -(h4["equity_drop"] + imr[2] - imr[self.cls[0]])), (b["pi"][0], -(h4["equity_drop"] + imr[2] - imr[self.cls[0]]))]
            if self.h4_net:
                t.append((b["B"][0, 0], -1.0))
            row(t, -h4["revolver_credit"] * Ls, np.inf, ("H4", 0))
        # ---- leaves
        L = len(self.leaves)
        psi = pj("valuation.psi_unfunded")
        cpace = pj("pacing.c_pace")
        pace_k = np.flatnonzero(self.is_commit)
        cp = np.array([cpace[self.tpl[k]["group"]] for k in pace_k])
        rc = cn("range_charge")
        self.p_leaf = self.prob[self.leaves]
        for li, leaf in enumerate(self.leaves):
            path = self.anc[leaf]
            a2l = self.a2[leaf]
            t = [(b["Wt"][li], 1.0), (b["W"][leaf], -1.0)]
            t += self.neg(self.hold(leaf, U[leaf]), psi) + self.neg(self.tstate(leaf, "U"), psi)
            rhs = 0.0
            for m in path:
                if self.lvl[m] <= 2:
                    t.append((y[m][pace_k], -cp))
                    rhs -= float(cp @ self.plan[pace_k])
                    if self.cls[m] != 2:
                        t.append((b["brk"][m], rc))
            t.append((y[a2l][pace_k], -2 * cp))
            rhs -= 2 * float(cp @ self.plan[pace_k])
            for nn in path[1:]:
                t.append((b["NR"][self.par[nn]], -self.d_year[nn] * self.acc[(li, nn)]))
            row(t, rhs, rhs, ("Wt", li))
            if opt:
                row([(b["M"][leaf], 1.0)], -np.inf, 0.0, ("H15", li))
            for i in np.flatnonzero(self.sl <= 1):
                row([(x[a2l, i], 1.0), (b["cq"][leaf, self.sl[i]], -1.0)], 0.0, np.inf, ("cqpos", li, i))
            for s in (2, 3):
                mem = np.flatnonzero(self.sl == s)
                row([(x[a2l, mem], V[leaf, mem]), (b["cq"][leaf, s], -V[leaf, mem].sum())], 0.0, np.inf, ("cqpos_agg", li, s))
        if opt:
            thr = cn("red_sale_threshold")
            for li, leaf in enumerate(self.leaves):
                for nn in self.anc[leaf]:
                    row([(b["z"][li], 1.0), (b["M"][nn], -1.0), (b["eta_R"][0], 1.0)], 0.0, np.inf, ("H9m", li, nn))
                    row([(b["z"][li], 1.0), (b["RS"][nn], -1.0), (b["eta_R"][0], 1.0)], -thr, np.inf, ("H9s", li, nn))
            self.r_H9 = row([(b["eta_R"][0], self.eps_red), (b["z"], self.p_leaf)], -np.inf, 0.0 if self.eps_red < 1 else np.inf,
                            ("H9", 0))
            levs = cn("depth_levels")
            self.r_H10 = []
            for k, al in enumerate(levs):
                for li in range(L):
                    row([(b["uu"][li, k], 1.0), (b["Wt"][li], 1.0 / self.W0), (b["eta_a"][k], 1.0)], self.Wstar / self.W0, np.inf,
                        ("H10u", li, k))
                rhs = (1 - al) * (self.b0["cvar_X"][k] + self.delta) if self.delta is not None else np.inf
                self.r_H10.append(row([(b["eta_a"][k], 1 - al), (b["uu"][:, k], self.p_leaf)], -np.inf, rhs, ("H10", k)))
        # objective auxiliaries: CRRA(3) tangents on real W~/W0, squared shortfall secants, CVaR (bPOE) hinge
        gam = pj("objective.crra_gamma")
        defl = (1 + pj("goal.inflation")) ** pj("goal.years")
        wk = np.geomspace(*pj("objective.crra_w_range"), pj("objective.crra_tangents"))
        Uf = lambda w: w ** (1 - gam) / (1 - gam)
        Ud = lambda w: w ** (-gam)
        self.crra = (gam, defl, Uf)
        brks = np.linspace(0, 1, pj("objective.l2_segments") + 1)
        for li in range(L):
            for w_ in wk:
                row([(b["util"][li], 1.0), (b["Wt"][li], -Ud(w_) / (self.W0 * defl))], -np.inf, Uf(w_) - Ud(w_) * w_, ("util", li))
            row([(b["sh"][li], 1.0), (b["Wt"][li], 1.0 / self.Wstar)], 1.0, np.inf, ("sh", li))
            for j in range(len(brks) - 1):
                a0, b1 = brks[j], brks[j + 1]
                row([(b["v2"][li], 1.0), (b["sh"][li], -(a0 + b1))], -a0 * b1, np.inf, ("v2", li))
            row([(b["ub"][li], 1.0), (b["Wt"][li], 1.0 / self.W0), (b["eta_b"][0], 1.0)], self.Wstar / self.W0, np.inf, ("bis", li))
        self._R = (R_r, R_c, R_v)
        self.rlo = np.array(R_lo, float)
        self.rhi = np.array(R_hi, float)
        self.tags = tags

    def _finish(self):
        R_r, R_c, R_v = self._R
        A = sp.csr_matrix((np.concatenate(R_v), (np.concatenate(R_r), np.concatenate(R_c))), shape=(len(self.rlo), self.nv))
        A.sum_duplicates()
        A.eliminate_zeros()
        self.A = A
        del self._R

    # ------------------------------------------------------------------ objectives and helpers
    def c_mean(self):
        c = np.zeros(self.nv)
        c[self.blk["Wt"]] = self.p_leaf
        return c                                     # maximize

    def c_util(self, lam_l2=0.0):
        c = np.zeros(self.nv)
        c[self.blk["util"]] = self.p_leaf
        if lam_l2:
            c[self.blk["v2"]] = -lam_l2 * self.p_leaf
        return c                                     # maximize

    def c_cvar(self, tail):
        c = np.zeros(self.nv)
        c[self.blk["eta_b"]] = 1.0
        c[self.blk["ub"]] = self.p_leaf / tail
        return c                                     # minimize: CVaR_{1-tail}(X)

    def c_b0(self):
        pen = self.pj("baselines.b0_penalties")
        c = np.zeros(self.nv)
        for s, k in enumerate(["LIQ", "HF", "AMB", "RED"]):
            c[self.blk["q"][:, s]] = pen[k] * self.prob
        c[self.blk["dr"][:, 0]] = pen["REV"] * self.prob
        c[self.blk["B"][:, 0]] = pen["REV_BAL"] * self.prob
        return c                                     # minimize

    def tie_row(self, tail):
        """CVaR_{1-tail}(X) <= 0 written as tail*eta + sum p ub <= 0 (bPOE <= tail)."""
        b = self.blk
        cols = np.r_[b["eta_b"], b["ub"]]
        vals = np.r_[tail, self.p_leaf]
        row = sp.csr_matrix((vals, (np.zeros(len(cols), int), cols)), shape=(1, self.nv))
        return row

    def from_author(self, xa, ablocks):
        v = np.zeros(self.nv)
        for k, idx in self.blk.items():
            if k in ablocks:
                v[idx.ravel()] = xa[np.asarray(ablocks[k]).ravel()]
            else:
                raise KeyError(k)
        return v
