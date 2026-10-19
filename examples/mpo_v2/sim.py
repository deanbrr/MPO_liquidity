"""Component 4: the out-of-sample simulator (SYNTHETIC - NOT ADIC DATA).

Fresh quarterly paths from the same generator on a separate seed, with a SEALED truth that the beliefs did not
generate (book truth model, DSGO RV-02) plus idiosyncratic noise per holding. Every policy runs on the same paths
(common random numbers) through one quarterly ledger:
  - root decision applied exactly (optimized policies) or the rule's t0 action;
  - years 1-2: optimized policies follow the nearest-node playbook (nearest stage-1 node, then its nearest child, on
    standardized observable features within the node class), in relative form; rules apply their own logic;
  - years 3-5: the fan rule (H16): buy-and-hold, funding moves only, forced deleveraging of synthetic beta;
  - each quarter: draws paid quarterly; a common need-based waterfall restores the 4% hard floor (long-only pro rata,
    hedge funds, revolver, amber, red - a red-tier sale is a red event); year ends restore 8% where the policy does.
Outputs per path: 5-year TWR on economic NAV (and on reported NAV), red-event flag, max drawdown, leverage path.
"""
from __future__ import annotations

import numpy as np

from common import GROUPS
from scenarios import UnitEngine, node_class

FIN = ["REV", "TERM", "NAVF", "PREF", "CSBL", "SMABL", "RACO"]


class Sim:
    def __init__(self, D: dict, gen, n_paths: int, seed: int, truth: dict | None, chunk: int, idio: bool = True,
                 tpl_truth_seed: int = 0):
        self.D, self.gen, self.P = D, gen, D["P"]
        self.n, self.seed, self.chunk = n_paths, seed, chunk
        self.truth = truth
        self.idio = idio
        P = self.P
        I = D["I"]
        K = len(D["tpl"])
        # sealed truth: holdings' true alpha (book truth) or the beliefs (truth=None: in-tree check)
        if truth is None:
            self.alpha_u = D["alpha_hat"].copy()
            self.alpha_t_noise = np.zeros(K)
            self.opp_sr = P.get("overlay.opp_sr_prior")
        else:
            self.alpha_u = np.asarray(truth["alpha_true"], float)
            rng = np.random.default_rng(tpl_truth_seed)
            prior_sd = P.get("fusion.unit_prior_sd_pp")
            disp = truth["variant"]["alpha_dispersion"]
            self.alpha_t_noise = np.array([disp * prior_sd[t["group"]] / 100 for t in D["tpl"]]) * rng.standard_normal(K)
            self.opp_sr = truth["opp_sharpe_true"]
        self.sig_idio = np.array([u["sigma_idio"] for u in D["units"]]) if idio else np.zeros(I)
        self.sig_idio_t = np.array([t["seg"]["sigma_idio"] for t in D["tpl"]]) if idio else np.zeros(K)

    # ------------------------------------------------------------------ engine per chunk
    def _chunk_world(self, ci: int, n: int):
        D, P, gen = self.D, self.P, self.gen
        rng = np.random.default_rng([self.seed, ci])
        st0 = gen.start_state(n, rng)
        sim = gen.simulate(st0, 20, rng)
        I = D["I"]
        K = len(D["tpl"])
        units = D["units"]
        eng = UnitEngine(D["spec"], P)
        V0 = np.array([u["nav_econ"] for u in units])
        N0 = np.array([u["nav"] for u in units])
        U0 = np.array([u["unfunded"] for u in units])
        A0 = np.array([u["age"] for u in units], float)
        st = eng.init_state(n, V0, N0, U0, A0)
        Vq = np.zeros((n, 21, I)); Nq = np.zeros((n, 21, I)); Uq = np.zeros((n, 21, I))
        Dq = np.zeros((n, 20, I)); Cq = np.zeros((n, 20, I)); Gq = np.zeros((n, 20, I))
        Vq[:, 0], Nq[:, 0], Uq[:, 0] = st["V"], st["N"], st["U"]
        zr = np.random.default_rng([self.seed, ci, 1])
        for q in range(20):
            idio = self.sig_idio[None, :] / 2 * zr.standard_normal((n, I))
            st, Dd, Cc, r = eng.step(st, sim["f"][:, q], sim["E"][:, q + 1], sim["S"][:, q + 1], self.alpha_u, idio)
            Vq[:, q + 1], Nq[:, q + 1], Uq[:, q + 1] = st["V"], st["N"], st["U"]
            Dq[:, q], Cq[:, q], Gq[:, q] = Dd, Cc, np.exp(r)
        # classes and features at year ends t = 0..5
        cls_t = np.zeros((n, 6), int)
        feat = np.zeros((n, 6, 7))
        cls_t[:, 0] = 1
        for t in range(1, 6):
            q = 4 * t
            dprev = sim["draw"][:, t - 1]
            dn = gen.expected_next_draw(np.exp(sim["lb"][:, q]), dprev, sim["Z"][:, q])
            cls_t[:, t] = node_class(sim["S"][:, q], sim["E"][:, q], sim["Z"][:, q], dn, P)
            feat[:, t] = np.column_stack([sim["f"][:, q - 4:q, 0].sum(1), sim["cs"][:, q], sim["y"][:, q],
                                          sim["lb"][:, q], sim["X"][:, q], sim["vix"][:, q], dn])
        cls_q = np.zeros((n, 20), int)
        for q in range(20):
            dprev = sim["draw"][:, q // 4]
            dn = gen.expected_next_draw(np.exp(sim["lb"][:, q + 1]), dprev, sim["Z"][:, q + 1])
            cls_q[:, q] = node_class(sim["S"][:, q + 1], sim["E"][:, q + 1], sim["Z"][:, q + 1], dn, P)
        # templates: per start year t, per-$ trajectories from quarter 4t
        teng = UnitEngine(D["tspec"], P)
        rho_f = np.array(P.get("bids.rho")["fund"])
        fund = np.array([u["kind"] == "fund" and u["group"] in ("PE", "SEC") for u in units])
        TV = np.zeros((n, 5, 21, K)); TN = np.zeros((n, 5, 21, K)); TU = np.zeros((n, 5, 21, K))
        TD = np.zeros((n, 5, 20, K)); TC = np.zeros((n, 5, 20, K))
        t_alpha = np.array([[t["alpha_pp"][c] / 100 for c in range(3)] for t in D["tpl"]])
        names = D["tpl_names"]
        for t0 in range(5):
            q0 = 4 * t0
            c0 = cls_t[:, t0]
            th = Vq[:, q0][:, fund].sum(1) / np.maximum(Nq[:, q0][:, fund].sum(1), 1e-9)
            iV = np.zeros((n, K)); iN = np.zeros((n, K)); iU = np.zeros((n, K)); ia = np.zeros((n, K))
            for k, t in enumerate(D["tpl"]):
                if t["kind"] == "commit":
                    iU[:, k] = 1.0
                elif names[k] == "SEC_BUY":
                    price = rho_f[c0] * th
                    iN[:, k] = 1.0 / price
                    iV[:, k] = (1 - t["winners_curse"]) / rho_f[c0]
                    iU[:, k] = t["unfunded_per_nav"] / price
                    ia[:, k] = t["age"]
                else:
                    g = 1.0 + t["lever_debt"]
                    iV[:, k] = g
                    iN[:, k] = g
                    ia[:, k] = t["age"]
            s = teng.init_state(n, iV, iN, iU, ia)
            TV[:, t0, q0], TN[:, t0, q0], TU[:, t0, q0] = s["V"], s["N"], s["U"]
            alpha = t_alpha[:, c0].T + self.alpha_t_noise[None, :]
            for q in range(q0, 20):
                idio = self.sig_idio_t[None, :] / 2 * zr.standard_normal((n, K))
                s, Dd, Cc, r = teng.step(s, sim["f"][:, q], sim["E"][:, q + 1], sim["S"][:, q + 1], alpha, idio)
                TV[:, t0, q + 1], TN[:, t0, q + 1], TU[:, t0, q + 1] = s["V"], s["N"], s["U"]
                TD[:, t0, q], TC[:, t0, q] = Dd, Cc
        # market data per quarter
        rf = D["rf"]
        Geq = np.exp(rf / 4 + sim["f"][:, :, 0])
        ov = lambda k: P.get(f"overlay.{k}")
        z_eq = (sim["f"][:, :, 0] - gen.w_eq[sim["w"]][:, None] / 4) / (ov("eq_vol_ref") / 2)
        z_v = sim["f"][:, :, 5] / (ov("vix_vol_ref") / 2)
        lo, lv = ov("opp_load_eq"), ov("opp_load_vol")
        nrm = np.sqrt(lo ** 2 + lv ** 2)
        idshare = ov("opp_idio_share")
        zo = zr.standard_normal((n, 20)) if self.idio else np.zeros((n, 20))
        oppret = ov("opp_vol_per_im") * (self.opp_sr / 4 + (np.sqrt(1 - idshare) * (lo * z_eq + lv * z_v) / nrm
                                                         + np.sqrt(idshare) * zo) / 2)
        eq_year = np.stack([np.exp((rf / 4 + sim["f"][:, 4 * y:4 * y + 4, 0]).sum(1)) - 1 for y in range(5)], 1)
        tail = ov("tail_rung_factor") * np.clip(-eq_year - ov("tail_strike_lo"), 0, ov("tail_width"))
        return {"sim": sim, "n": n, "Vq": Vq, "Nq": Nq, "Uq": Uq, "Dq": Dq, "Cq": Cq, "Gq": Gq, "cls_t": cls_t,
                "cls_q": cls_q, "feat": feat, "TV": TV, "TN": TN, "TU": TU, "TD": TD, "TC": TC, "Geq": Geq,
                "oppret": oppret, "tail": tail, "draw": sim["draw"], "w": sim["w"]}

    # ------------------------------------------------------------------ evaluation
    def evaluate(self, policies: dict, paths_of_tree=None) -> dict:
        """Run every policy on the same paths. Returns {name: {metric arrays}}."""
        out = {k: [] for k in policies}
        nchunks = int(np.ceil(self.n / self.chunk))
        b0pol = {"kind": "B0", "restore8": False}
        for ci in range(nchunks):
            n = min(self.chunk, self.n - ci * self.chunk)
            wd = self._chunk_world(ci, n)
            # the status quo's path supplies the exogenous ADR-39 stage readings (as in the tree)
            b0r = run_policy(self.D, wd, b0pol)
            green_ext = b0r["green_path"].astype(bool)
            for name, pol in policies.items():
                if pol["kind"] == "B0" and not pol.get("restore8", False):
                    out[name].append(b0r)
                    continue
                pp = dict(pol, green_ext=green_ext) if pol["kind"] == "plan" else pol
                out[name].append(run_policy(self.D, wd, pp))
        res = {}
        for name in policies:
            res[name] = {k: np.concatenate([o[k] for o in out[name]]) for k in out[name][0]}
        return res


def tree_world(D: dict, gen) -> dict:
    """The tree's own leaf paths as a simulator world (belief alphas with the fan-year belief error, no idiosyncratic
    noise): in-tree probabilities for rules, and the E1 check of the LP's annual ledger on identical paths."""
    P = D["P"]
    tr = D["tr"]
    leaves = D["leaves"]
    n = len(leaves)
    I = D["I"]
    K = len(D["tpl"])
    paths = [D["anc"][lf][1:] for lf in leaves]           # nodes at levels 1..5
    nodes = tr["nodes"]
    f = np.zeros((n, 20, 6))
    S = np.zeros((n, 21), int); Ez = np.zeros((n, 21), int)
    S[:, 0] = nodes[0]["seg"]["S_end"]
    Ez[:, 0] = nodes[0]["seg"]["E_end"]
    for j, pth in enumerate(paths):
        for yv, nd in enumerate(pth):
            seg = nodes[nd]["seg"]
            f[j, 4 * yv:4 * yv + 4] = seg["f"]
            S[j, 4 * yv + 1:4 * yv + 5] = seg["S"]
            Ez[j, 4 * yv + 1:4 * yv + 5] = seg["E"]
    node_y = np.array(paths)                                # (n, 5)
    draw = tr["d_year"][node_y]
    cls_t = np.zeros((n, 6), int)
    cls_t[:, 0] = tr["cls"][0]
    cls_t[:, 1:] = tr["cls"][node_y]
    cls_q = np.repeat(tr["cls"][node_y], 4, axis=1)
    feat = np.zeros((n, 6, 7))
    feat[:, 1:] = tr["features"][node_y]
    e_scale = P.get("tree.belief_error_fan_scale")
    e_leaf = tr["belief_e"][leaves] * e_scale
    units = D["units"]
    eng = UnitEngine(D["spec"], P)
    V0 = np.array([u["nav_econ"] for u in units]); N0 = np.array([u["nav"] for u in units])
    U0 = np.array([u["unfunded"] for u in units]); A0 = np.array([u["age"] for u in units], float)
    st = eng.init_state(n, V0, N0, U0, A0)
    Vq = np.zeros((n, 21, I)); Nq = np.zeros((n, 21, I)); Uq = np.zeros((n, 21, I))
    Dq = np.zeros((n, 20, I)); Cq = np.zeros((n, 20, I)); Gq = np.zeros((n, 20, I))
    Vq[:, 0], Nq[:, 0], Uq[:, 0] = st["V"], st["N"], st["U"]
    a_hat, s_post = D["alpha_hat"], D["sigma_post"]
    for q in range(20):
        al = a_hat[None, :] + (e_leaf[:, None] * s_post[None, :] if q >= 8 else 0.0)
        st, Dd, Cc, r = eng.step(st, f[:, q], Ez[:, q + 1], S[:, q + 1], al)
        Vq[:, q + 1], Nq[:, q + 1], Uq[:, q + 1] = st["V"], st["N"], st["U"]
        Dq[:, q], Cq[:, q], Gq[:, q] = Dd, Cc, np.exp(r)
    teng = UnitEngine(D["tspec"], P)
    rho_f = np.array(P.get("bids.rho")["fund"])
    fund = np.array([u["kind"] == "fund" and u["group"] in ("PE", "SEC") for u in units])
    prior_sd = P.get("fusion.unit_prior_sd_pp")
    t_sd = np.array([prior_sd[t["group"]] / 100 for t in D["tpl"]])
    t_alpha = np.array([[t["alpha_pp"][c] / 100 for c in range(3)] for t in D["tpl"]])
    names = D["tpl_names"]
    TV = np.zeros((n, 5, 21, K)); TN = np.zeros((n, 5, 21, K)); TU = np.zeros((n, 5, 21, K))
    TD = np.zeros((n, 5, 20, K)); TC = np.zeros((n, 5, 20, K))
    for t0 in range(5):
        q0 = 4 * t0
        c0 = cls_t[:, t0]
        th = Vq[:, q0][:, fund].sum(1) / np.maximum(Nq[:, q0][:, fund].sum(1), 1e-9)
        iV = np.zeros((n, K)); iN = np.zeros((n, K)); iU = np.zeros((n, K)); ia = np.zeros((n, K))
        for k, t in enumerate(D["tpl"]):
            if t["kind"] == "commit":
                iU[:, k] = 1.0
            elif names[k] == "SEC_BUY":
                price = rho_f[c0] * th
                iN[:, k] = 1.0 / price
                iV[:, k] = (1 - t["winners_curse"]) / rho_f[c0]
                iU[:, k] = t["unfunded_per_nav"] / price
                ia[:, k] = t["age"]
            else:
                g = 1.0 + t["lever_debt"]
                iV[:, k] = g
                iN[:, k] = g
                ia[:, k] = t["age"]
        s = teng.init_state(n, iV, iN, iU, ia)
        TV[:, t0, q0], TN[:, t0, q0], TU[:, t0, q0] = s["V"], s["N"], s["U"]
        for q in range(q0, 20):
            al = t_alpha[:, c0].T + (e_leaf[:, None] * t_sd[None, :] if q >= 8 else 0.0)
            s, Dd, Cc, r = teng.step(s, f[:, q], Ez[:, q + 1], S[:, q + 1], al)
            TV[:, t0, q + 1], TN[:, t0, q + 1], TU[:, t0, q + 1] = s["V"], s["N"], s["U"]
            TD[:, t0, q], TC[:, t0, q] = Dd, Cc
    rf = D["rf"]
    Geq = np.exp(rf / 4 + f[:, :, 0])
    oppret = np.repeat(D["oppret"][node_y] / 4, 4, axis=1)
    tail = D["tailpay"][node_y]
    sim = {"vix": np.zeros((n, 21)), "w": np.zeros(n, int)}
    for t in range(1, 6):
        sim["vix"][:, 4 * t] = np.array([nodes[nd]["seg"]["end"]["vix"] for nd in node_y[:, t - 1]])
    sim["vix"][:, 0] = nodes[0]["seg"]["end"]["vix"]
    return {"sim": sim, "n": n, "Vq": Vq, "Nq": Nq, "Uq": Uq, "Dq": Dq, "Cq": Cq, "Gq": Gq, "cls_t": cls_t,
            "cls_q": cls_q, "feat": feat, "TV": TV, "TN": TN, "TU": TU, "TD": TD, "TC": TC, "Geq": Geq,
            "oppret": oppret, "tail": tail, "draw": draw, "w": sim["w"], "prob": tr["prob"][leaves]}


# ====================================================================================== the ledger
def run_policy(D: dict, wd: dict, pol: dict) -> dict:
    P = D["P"]
    n = wd["n"]
    I = D["I"]
    K = len(D["tpl"])
    rf = D["rf"]
    eq4 = np.exp(rf / 4)
    ov = lambda k: P.get(f"overlay.{k}")
    cf = lambda k: P.get(f"corporate_finance.{k}")
    cn = lambda k: P.get(f"constraints.{k}")
    units = D["units"]
    names = D["tpl_names"]
    is_commit = D["tpl_is_commit"]
    plan = np.array([t.get("plan", 0.0) for t in D["tpl"]])
    dpe = D["tpl_debt"]
    tsp = D["tpl_spread"]
    sl = D["sleeve_of"]
    lo_eq = D["is_lo_eq"]
    fi = D["fi"]
    hf = D["is_hf"]
    red = D["red"]
    amb = D["amber"]
    rho = P.get("bids.rho")
    agem = P.arr("bids.age_multiplier")
    tc = P.get("trading.tc")
    prem_u = D["bid_prem"]
    im_rate = np.array(ov("im_rate"))
    fb = np.array(ov("beta_fin_spread"))
    fp = np.array(ov("p2s_fin_spread"))
    navf, pref, csbl, smabl, raco = cf("navf"), cf("pref"), cf("csbl"), cf("smabl"), cf("raco")
    rate = np.zeros((7, 3))
    rate[0] = rf + cf("revolver_spread")
    rate[1] = rf + cf("term_spread")
    rate[2] = rf + np.array(navf["spread"])
    rate[3] = np.array(pref["rate"])
    rate[4] = rf + csbl["spread"]
    rate[5] = rf + smabl["spread"]
    rate[6] = rf + np.array(raco["spread"])
    pik = np.array([False, False, True, True, False, False, False])
    rev_av = np.array(cf("revolver_avail"))
    hmin = P.get("overlay.tail_budget")[0] / ov("tail_premium")
    hmax = P.get("overlay.tail_budget")[1] / ov("tail_premium")
    prem = ov("tail_premium")
    phi_hf = np.array(P.get("trading.redeem_phi")["hf"])
    phi_re = np.array(P.get("trading.redeem_phi")["re_open_end"])
    phi_u = np.where(D["is_hf"][:, None], phi_hf[None, :], np.where(D["is_re_open"][:, None], phi_re[None, :], 0.0))
    caps_cls = np.array(cn("class_caps"))
    bshare = cn("behind_cap_share")
    thr = cn("red_sale_threshold")
    psi = P.get("valuation.psi_unfunded")
    cpace = P.get("pacing.c_pace")
    cp_k = np.array([cpace[t["group"]] if t["kind"] == "commit" else 0.0 for t in D["tpl"]])
    W0 = D["W0"]
    Vq, Nq, Uq, Dq, Cq, Gq = wd["Vq"], wd["Nq"], wd["Uq"], wd["Dq"], wd["Cq"], wd["Gq"]
    TV, TN, TU, TD, TC = wd["TV"], wd["TN"], wd["TU"], wd["TD"], wd["TC"]
    cls_t, cls_q = wd["cls_t"], wd["cls_q"]
    restore8 = pol.get("restore8", True)
    kind = pol["kind"]
    # ---------------- state
    x = np.ones((n, I))
    y = np.zeros((n, K, 5))            # $ per template per start year
    C = np.full(n, P.get("treasury.cash0"))
    IM = np.zeros(n)
    B = np.zeros((n, 7))
    L = np.full(n, cf("revolver_signed"))
    Lup = 0.0
    beta = np.full(n, ov("beta_sq"))
    p2s = np.zeros(n)
    trs = np.zeros((n, int(hf.sum())))
    hed = np.zeros(n)
    opp = np.full(n, ov("opp_im_sq"))
    claim1 = np.zeros((n, I))
    claim2 = np.zeros(n)
    redflag = np.zeros(n, bool)
    red_wf = np.zeros(n, bool)         # forced red-tier sale in the waterfall
    red_plan = np.zeros(n, bool)       # planned red-tier sale outside Green BEN / at a fire-sale bid
    skipped_red = np.zeros(n)          # $ of planned red-tier sales skipped by the ADR-39 execution rule
    green_ext = pol.get("green_ext")   # exogenous Green flags (status quo's path), as in the tree
    cpace_acc = np.zeros(n)
    charges = np.zeros(n)
    mult_now = np.ones((n, K))         # commitment multiplier applied each year
    node1 = np.full(n, -1)
    node2 = np.full(n, -1)
    lev_path = np.zeros((n, 6))
    lev_pre = np.zeros((n, 6))
    capcls_path = np.zeros((n, 6))
    green_out = np.zeros((n, 6), bool)
    w_grp = {g: float(Vq[0, 0][D["group"] == g].sum() / W0) for g in GROUPS}
    rb_lo, rb_hi = P.get("constraints.range_band")
    rchg = P.get("constraints.range_charge")
    tgrp = D["tpl_group"]

    def range_charge(qi, ccls):
        """Elastic IC ranges (0.5-1.5x SAA weight), charged per $ of breach at decision years, waived in STR."""
        W, NR, E, LQ, HV, tv = values(qi)
        tot = np.zeros(n)
        for g in GROUPS:
            m_ = D["group"] == g
            eg = (x[:, m_] * Vq[:, qi][:, m_]).sum(1) + \
                (y[:, tgrp == g] * TV[:, :, qi][:, :, tgrp == g].transpose(0, 2, 1)).sum((1, 2))
            br = np.maximum(eg - rb_hi * w_grp[g] * W, 0) + np.maximum(rb_lo * w_grp[g] * W - eg, 0)
            tot += br
        return np.where(ccls == 2, 0.0, rchg * tot)
    behind_path = np.zeros((n, 6), bool)
    loss_path = np.zeros((n, 6), bool)
    cap_path = np.zeros((n, 6))

    def proc_unit(qi, ccls):
        """Proceeds per unit of fraction sold at quarter boundary qi, class ccls (n,)."""
        V = Vq[:, qi]
        out = np.zeros((n, I))
        for i, u in enumerate(units):
            if u["tier"] == "liquid":
                if u["group"] == "HF":
                    out[:, i] = np.array(rho["hf"])[ccls] * V[:, i]
                else:
                    out[:, i] = (1 - tc.get(u["bid_key"], 0.001)) * V[:, i]
            else:
                r = np.array(rho[u["bid_key"]])
                am = agem[min(int(np.searchsorted(np.asarray(u["edges"]), u["age"] + qi / 4, side="right")), 3)] \
                    if u["age_mult"] else 1.0
                out[:, i] = r[ccls] * am * prem_u[i] * V[:, i]
        return out

    def proc_norm(qi):
        return proc_unit(qi, np.zeros(n, int))

    def values(qi):
        HV = (x * Vq[:, qi]).sum(1)
        HN = (x * Nq[:, qi]).sum(1)
        tv = (y * TV[:, :, qi].transpose(0, 2, 1)).sum((1, 2))
        tn = (y * TN[:, :, qi].transpose(0, 2, 1)).sum((1, 2))
        tdebt = (y.sum(2) * dpe[None, :]).sum(1)
        cl = claim1.sum(1) + claim2
        W = C + IM + cl + HV + tv - B.sum(1) - tdebt
        NR = C + IM + cl + HN + tn - B.sum(1) - tdebt
        E = HV + tv + beta + p2s + trs.sum(1)
        LQ = C + P.get("treasury.fi_liquidity_weight") * x[:, fi] * Vq[:, qi, fi]
        return W, NR, E, LQ, HV, tv

    def waterfall(qi, target_lq, ccls, allow_rev=True, prorata=False):
        """Raise IG + cash to target_lq (n,) and cash to >= 0. Order: FI (cash only), long-only, hedge funds,
        revolver, amber, red (red event). prorata: B2 raises across long-only, HF and amber in proportion."""
        nonlocal C
        W, NR, E, LQ, HV, tv = values(qi)
        V = Vq[:, qi]
        pr = proc_unit(qi, ccls)
        # cash negative but IG available: sell FI for cash
        needc = np.maximum(-C, 0.0)
        if needc.any():
            avail = x[:, fi] * pr[:, fi]
            take = np.minimum(needc, avail)
            frac = np.where(avail > 0, take / np.maximum(avail, 1e-12), 0.0)
            x[:, fi] *= (1 - frac)
            C += take
        W, NR, E, LQ, HV, tv = values(qi)
        need = np.maximum(target_lq - LQ, 0.0)
        if not need.any():
            return
        if prorata:
            groups = [lo_eq, hf, amb]
            avail = np.stack([(x[:, g] * pr[:, g]).sum(1) for g in groups], 1)
            tot = avail.sum(1)
            take_tot = np.minimum(need, tot)
            for gi_, g in enumerate(groups):
                share = np.where(tot > 0, avail[:, gi_] / np.maximum(tot, 1e-12), 0.0)
                tk = take_tot * share
                frac = np.where(avail[:, gi_] > 0, tk / np.maximum(avail[:, gi_], 1e-12), 0.0)
                x[:, g] *= (1 - frac[:, None])
                C += tk
            need = need - take_tot
        order = [("LO", lo_eq), ("HF", hf), ("REV", None), ("AMB", amb), ("RED", red)]
        for nm, g in order:
            if not need.any():
                break
            if nm == "REV":
                if not allow_rev:
                    continue
                head = np.maximum(rev_av[ccls] * L - B[:, 0], 0.0)
                tk = np.minimum(need, head)
                B[:, 0] += tk
                C += tk
                need = need - tk
                continue
            avail = (x[:, g] * pr[:, g]).sum(1)
            tk = np.minimum(need, avail)
            frac = np.where(avail > 0, tk / np.maximum(avail, 1e-12), 0.0)
            x[:, g] *= (1 - frac[:, None])
            C += tk
            if nm == "RED":
                redflag[:] |= tk > thr
                red_wf[:] |= tk > thr
            need = need - tk

    def set_im(qi, ccls):
        nonlocal C, IM
        req = im_rate[ccls] * (beta + p2s) + ov("trs_ia") * trs.sum(1) + opp
        C -= (req - IM)
        IM = req

    def lev_cap(t, behind):
        c = cls_t[:, t]
        cap = np.minimum(caps_cls[c], cn("lev_cap"))
        cap = np.where(behind, 1.0 + bshare * (caps_cls[c] - 1.0), cap)
        return cap

    def deleverage(qi, cap):
        nonlocal beta
        W, NR, E, LQ, HV, tv = values(qi)
        excess = np.maximum(E - cap * W, 0.0)
        cut = np.minimum(excess, beta)
        beta = beta - cut
        excess = excess - cut
        tot = trs.sum(1)
        cut2 = np.minimum(excess, tot)
        trs[:] *= np.where(tot > 0, 1 - cut2 / np.maximum(tot, 1e-12), 1.0)[:, None]

    # ---------------- t = 0 decisions
    W, NR, E, LQ, HV, tv = values(0)
    ccls0 = np.ones(n, int)
    if kind == "plan":
        r0 = pol["root"]
        pr0 = proc_unit(0, ccls0)
        s0 = np.minimum(r0["sell"], 1.0)
        C += (s0[None, :] * pr0).sum(1)
        x -= s0[None, :]
        root_red = float((s0 * pr0[0] * red).sum())
        if root_red > thr:                    # ADR-39: today's stage is Amber, so a root red-tier sale is a red event
            redflag[:] = True
            red_plan[:] = True
        rd = r0["redeem"]
        claim1 += rd[None, :] * Vq[:, 0]
        x -= rd[None, :]
        ad = r0["add"]
        C -= (ad * Vq[0, 0] * (1 + D["tc_add"])).sum()
        x += ad[None, :]
        for k in range(K):
            y[:, k, 0] = r0["tpl"][k]
            if not is_commit[k]:
                C -= r0["tpl"][k]
        cpace_acc += (cp_k * (r0["tpl"] - plan) * is_commit).sum()
        dp = r0["p2s"]
        if dp > 0:
            frac = dp / Vq[0, 0, D["lo1"]]
            x[:, D["lo1"]] -= frac
            C += dp * (1 - tc["lo_dm"])
        p2s[:] = dp
        beta[:] = r0["beta"]
        trs[:] = r0["trs"][None, :]
        hed[:] = r0["hed"]
        opp[:] = r0["opp"]
        B[:] = r0["fin"][None, :]
        oid = np.array([0, 0, navf["oid"], pref["fee"], 0, 0, 0])
        C += (r0["fin"] * (1 - oid)).sum()
        Lup = r0["Lup"]
        C -= cf("revolver_upfront_fee") * 3 * Lup
        mult_now[:] = np.where(is_commit, r0["tpl"] / np.maximum(plan, 1e-12), 0.0)[None, :]
    else:
        y[:, :, 0] = np.where(is_commit, plan, 0.0)[None, :]
        mult_now[:] = np.where(is_commit, 1.0, 0.0)[None, :]
        hed[:] = hmin * W
        if kind == "B4":
            beta[:] = ov("beta_sq") + (pol["scale"] - 1.0) * E
        if kind == "B3":
            beta[:] = np.maximum(b3_target(P, wd, 0) * W - (E - beta), 0.0)
    set_im(0, ccls0)
    C -= prem * hed
    if kind == "plan" or restore8:
        waterfall(0, cn("floor_target") * values(0)[0], ccls0)
    charges += range_charge(0, ccls0)
    W, NR, E, LQ, HV, tv = values(0)
    W_prev = W.copy()
    N_prev = NR.copy()
    N_open = NR.copy()
    logtwr = np.zeros(n)
    logtwr_r = np.zeros(n)
    peak = np.zeros(n)
    maxdd = np.zeros(n)
    lev_path[:, 0] = E / W
    d_rate = wd["draw"][:, 0]
    Gh = wd["Gq"][:, :, hf]
    yr_ret = np.zeros(n)
    # ---------------- quarters
    for q in range(20):
        yi = q // 4
        ccls = cls_q[:, q]
        Gu = Gq[:, q]
        # flows
        C += (x * (Dq[:, q] - Cq[:, q])).sum(1)
        C += (y * (TD[:, :, q] - TC[:, :, q]).transpose(0, 2, 1)).sum((1, 2))
        C -= (y.sum(2) * (dpe * (rf + tsp))[None, :]).sum(1) / 4
        C += (C + IM) * (eq4 - 1)
        for j in range(7):
            if pik[j]:
                B[:, j] *= (1 + rate[j, ccls] / 4)
            else:
                C -= rate[j, ccls] * B[:, j] / 4
        C -= cf("revolver_undrawn_fee") * np.maximum(L - B[:, 0], 0.0) / 4
        C += p2s * (wd["Geq"][:, q] - eq4 - fp[ccls] / 4) + beta * (wd["Geq"][:, q] - eq4 - fb[ccls] / 4)
        C += (trs * (Gh[:, q] - eq4 - ov("trs_fin_spread") / 4)).sum(1)
        C += opp * wd["oppret"][:, q]
        draw_q = d_rate * N_open / 4
        C -= draw_q
        claim1 *= Gu
        claim2 *= eq4
        if q % 4 == 3:
            C += hed * wd["tail"][:, yi]
        set_im(q + 1, ccls)
        # hard floor
        W, NR, E, LQ, HV, tv = values(q + 1)
        if (LQ < cn("floor_hard") * W).any() or (C < 0).any():
            waterfall(q + 1, cn("floor_hard") * W, ccls, prorata=(kind == "B2"))
        W, NR, E, LQ, HV, tv = values(q + 1)
        if q % 4 != 3:
            r_ = np.maximum((W + draw_q) / W_prev, 1e-6)
            rr_ = np.maximum((NR + draw_q) / N_prev, 1e-6)
            logtwr += np.log(r_)
            logtwr_r += np.log(rr_)
            peak = np.maximum(peak, logtwr)
            maxdd = np.maximum(maxdd, peak - logtwr)
            W_prev, N_prev = W, NR
            continue
        # ---------------- year end t
        t = yi + 1
        ct = cls_t[:, t]
        # redemption claims: queued remainder paid fully, new notices paid at the class pass-through
        C += claim2
        claim2[:] = 0.0
        pay = claim1 * phi_u.T[ct]
        C += pay.sum(1)
        claim2 += (claim1 - pay).sum(1)
        claim1[:] = 0.0
        if t == 5:
            W, NR, E, LQ, HV, tv = values(20)
            Uend = (x * Uq[:, 20]).sum(1) + (y * TU[:, :, 20].transpose(0, 2, 1)).sum((1, 2))
            W_adj = W - psi * Uend + cpace_acc - charges
            r_ = np.maximum((W_adj + draw_q) / W_prev, 1e-6)
            rr_ = np.maximum((NR - psi * Uend + cpace_acc - charges + draw_q) / N_prev, 1e-6)
            logtwr += np.log(r_)
            logtwr_r += np.log(rr_)
            peak = np.maximum(peak, logtwr)
            maxdd = np.maximum(maxdd, peak - logtwr)
            break
        # pre-decision return of the year (loss year) and the goal-path gap (behind)
        W, NR, E, LQ, HV, tv = values(q + 1)
        lev_pre[:, t] = E / W
        capcls_path[:, t] = np.minimum(caps_cls[ct], cn("lev_cap"))
        r_ = np.maximum((W + draw_q) / W_prev, 1e-6)
        logtwr_pre = logtwr + np.log(r_)
        behind = logtwr_pre - t * np.log(1 + P.get("goal.rate")) < -cn("behind_gap")
        green = (ct == 0) & (LQ >= cn("floor_target") * W)
        if green_ext is not None:                     # ADR-39 stage read on the status quo's path (exogenous)
            green = green_ext[:, t]
        first_after_str = (cls_t[:, t - 1] == 2) & (ct != 2)
        stage_path = np.maximum(ct, np.where(LQ >= cn("floor_target") * W, 0, np.where(LQ >= 0.06 * W, 1, 2)))
        if kind == "B0":
            green_out[:, t] = (ct == 0) & (LQ >= cn("floor_target") * W)
        # ---------------- decisions
        if kind == "plan" and t in pol.get("playbook_years", (1, 2)) and pol.get("playbook", True):
            chosen = map_nodes(pol, wd["feat"][:, t], ct, node1 if t == 2 else None)
            if t == 1:
                node1[:] = chosen
            else:
                node2[:] = chosen
            ref = {"C": C, "B": B, "beta": beta, "p2s": p2s, "trs": trs, "hed": hed, "opp": opp, "claim1": claim1,
                   "redflag": redflag, "red_plan": red_plan, "skipped_red": skipped_red, "mult_now": mult_now, "L": L,
                   "Lup": Lup, "values": values,
                   "proc_unit": proc_unit, "proc_norm": proc_norm}
            apply_node(P, D, wd, pol, chosen, q + 1, ct, green, x, y, t, ref)
            C, beta, p2s, hed, opp = ref["C"], ref["beta"], ref["p2s"], ref["hed"], ref["opp"]
            if t == 1:
                L[:] = cf("revolver_signed") + Lup
        elif kind == "B2" and t <= 4:
            ref = {"C": C, "values": values}
            rebalance_liquid(P, D, wd, q + 1, x, ref, ct)
            C = ref["C"]
        if kind == "B3":
            W, NR, E, LQ, HV, tv = values(q + 1)
            tgt = b3_target(P, wd, t)
            ok = (LQ >= cn("floor_target") * W)
            newb = np.maximum(tgt * W - (E - beta), 0.0)
            beta = np.where(ok | (newb < beta), newb, beta)
        if kind == "B4":
            W, NR, E, LQ, HV, tv = values(q + 1)
            base = E - beta + ov("beta_sq")             # the status quo's exposure on this path
            beta = ov("beta_sq") + (pol["scale"] - 1.0) * base
        # B0-style hedge at the floor in decision years; fans hold the dollar notional
        if kind != "plan" and t <= 2:
            hed = hmin * values(q + 1)[0]
        # commitments for the coming year (fans: the stage-2 multiplier repeats)
        if t <= 4:
            y[:, :, t] = mult_now * plan[None, :] * is_commit[None, :]
            cpace_acc += ((mult_now - 1.0) * plan[None, :] * cp_k[None, :] * is_commit[None, :]).sum(1)
        # forced paydown of secured facilities whose LTV cap tightened
        W, NR, E, LQ, HV, tv = values(q + 1)
        PP = (x[:, D["is_pledge"]] * Vq[:, q + 1][:, D["is_pledge"]]).sum(1)
        capn = np.array(navf["ltv"])[ct] * PP
        pay_navf = np.maximum(B[:, 2] - capn, 0.0)
        B[:, 2] -= pay_navf
        C -= pay_navf
        caprev = rev_av[ct] * L
        pay_rev = np.maximum(B[:, 0] - caprev, 0.0)
        B[:, 0] -= pay_rev
        C -= pay_rev
        set_im(q + 1, ct)
        C -= prem * hed
        # floors: 8% target where the policy restores it, 4% always
        W, NR, E, LQ, HV, tv = values(q + 1)
        tgt = np.where(((ct <= 1) & ~first_after_str) & (restore8 or kind == "plan"),
                       cn("floor_target"), cn("floor_hard")) * W
        waterfall(q + 1, tgt, ct, prorata=(kind == "B2"))
        # leverage caps (forced deleveraging of synthetic beta; the measurement device B4 is uncapped)
        if kind != "B4":
            cap = lev_cap(t, behind) if kind == "plan" else np.full(n, cn("lev_cap"))
            deleverage(q + 1, cap)
            cap_path[:, t] = cap
        # repay the revolver from surplus cash above the target (all policies)
        W, NR, E, LQ, HV, tv = values(q + 1)
        surplus = np.maximum(LQ - (cn("floor_target") + 0.01) * W, 0.0)
        rp = np.minimum(np.minimum(surplus, B[:, 0]), np.maximum(C, 0.0))
        if kind == "plan" and t <= 2:
            rp = rp * 0.0       # playbook years keep the planned revolver balance
        B[:, 0] -= rp
        C -= rp
        set_im(q + 1, ct)
        if t <= 2:
            charges += range_charge(q + 1, ct)
        W, NR, E, LQ, HV, tv = values(q + 1)
        lev_path[:, t] = E / W
        behind_path[:, t] = behind
        loss_path[:, t] = r_ < 1.0
        r2 = np.maximum((W + draw_q) / W_prev, 1e-6)
        rr2 = np.maximum((NR + draw_q) / N_prev, 1e-6)
        logtwr += np.log(r2)
        logtwr_r += np.log(rr2)
        peak = np.maximum(peak, logtwr)
        maxdd = np.maximum(maxdd, peak - logtwr)
        W_prev, N_prev = W, NR
        N_open = NR.copy()
        d_rate = wd["draw"][:, t]
    yrs = 5
    return {"twr": np.exp(logtwr / yrs) - 1, "twr_rep": np.exp(logtwr_r / yrs) - 1, "red": redflag.astype(float),
            "red_wf": red_wf.astype(float), "red_plan": red_plan.astype(float), "skipped_red": skipped_red,
            "maxdd": 1 - np.exp(-maxdd), "lev_max": lev_path.max(1), "lev_path": lev_path, "lev_pre": lev_pre,
            "capcls_path": capcls_path,
            "behind_path": behind_path.astype(float), "loss_path": loss_path.astype(float), "cap_path": cap_path,
            "green_path": green_out.astype(float), "node1": node1.astype(float), "node2": node2.astype(float)}


def map_nodes(pol, feat, ct, parent_nodes=None):
    """Nearest node (squared distance on standardized features), preferring nodes of the path's class.
    t = 1: among the stage-1 nodes; t = 2: among the children of each path's stage-1 node."""
    fz = (feat - pol["feat_mu"]) / pol["feat_sd"]
    if parent_nodes is None:
        cand = np.tile(np.asarray(pol["stage1"]), (len(fz), 1))
    else:
        width = max(len(v) for v in pol["children"].values())
        tab = {k: (v + [v[-1]] * (width - len(v))) for k, v in pol["children"].items()}
        cand = np.array([tab[int(p)] for p in parent_nodes])
    nf = np.array([pol["nodes"][int(c)]["fz"] for c in cand.ravel()]).reshape(cand.shape + (-1,))
    ncl = np.array([pol["nodes"][int(c)]["cls"] for c in cand.ravel()]).reshape(cand.shape)
    d2 = ((nf - fz[:, None, :]) ** 2).sum(-1)
    same = ncl == ct[:, None]
    has = same.any(1)
    d2 = np.where(has[:, None] & ~same, np.inf, d2)
    return cand[np.arange(len(fz)), d2.argmin(1)]


def b3_target(P, wd, t):
    a, b = P.get("baselines.b3_vix_F")
    f1, f2 = P.get("baselines.b3_F_band")
    hi, lo = P.get("baselines.b3_lev")
    vix = wd["sim"]["vix"][:, 4 * t]
    F = (vix - a) / b
    w = np.clip((F - f1) / (f2 - f1), 0.0, 1.0)
    return hi + (lo - hi) * w


def rebalance_liquid(P, D, wd, qi, x, ref, ccls):
    """B2: bring long-only and hedge-fund holdings back to their t0 shares of W (cash to 8% first)."""
    values = ref["values"]
    W, NR, E, LQ, HV, tv = values(qi)
    V = wd["Vq"][:, qi]
    V0 = wd["Vq"][:, 0]
    W0 = D["W0"]
    tc_add = D["tc_add"]
    spare = np.maximum(LQ - P.get("constraints.floor_target") * W, 0.0)
    for g in ("LO", "HF"):
        m = (D["group"] == g) & ~D["is_fi"]
        tgt_share = V0[:, m].sum(1) / W0
        cur = (x[:, m] * V[:, m]).sum(1)
        delta = tgt_share * W - cur
        delta = np.where(delta > 0, np.minimum(delta, spare), delta)
        spare = spare - np.maximum(delta, 0.0)
        frac = delta / np.maximum(cur, 1e-9)
        x[:, m] *= (1 + frac)[:, None]
        cost = np.where(delta > 0, delta * (1 + tc_add[m].mean()), delta * (1 - tc_add[m].mean()))
        ref["C"] = ref["C"] - cost


def apply_node(P, D, wd, pol, chosen, qi, ct, green, x, y, t, ref):
    """Apply each path's mapped node decisions in relative form (DSGO section 5.5, RR1)."""
    nodes = pol["nodes"]
    values, proc_unit = ref["values"], ref["proc_unit"]
    n = len(chosen)
    I = D["I"]
    K = len(D["tpl"])
    is_commit = D["tpl_is_commit"]
    plan = np.array([tt.get("plan", 0.0) for tt in D["tpl"]])
    red = D["red"]
    thr = P.get("constraints.red_sale_threshold")
    cn = lambda k: P.get(f"constraints.{k}")
    cf = lambda k: P.get(f"corporate_finance.{k}")
    navf, pref, csbl, smabl, raco = cf("navf"), cf("pref"), cf("csbl"), cf("smabl"), cf("raco")
    rho_f = np.array(P.get("bids.rho")["fund"])
    tc_lo = P.get("trading.tc")["lo_dm"]
    V = wd["Vq"][:, qi]
    pr = proc_unit(qi, ct)
    prn = ref["proc_norm"](qi)
    sell = np.stack([nodes[c]["sell_rel"] for c in chosen])
    redm = np.stack([nodes[c]["red_rel"] for c in chosen])
    addp = np.stack([nodes[c]["add_pct"] for c in chosen])
    tplp = np.stack([nodes[c]["tpl_pct"] for c in chosen])
    mult = np.stack([nodes[c]["mult"] for c in chosen])
    W, NR, E, LQ, HV, tv = values(qi)
    C = ref["C"]
    # sells. Execution respects ADR-39: a planned red-tier sale is executed only on a Green BEN path at a bid of at
    # least 0.9 x normal; elsewhere it would be a red event, so it is skipped (logged), never executed as planned
    redok = green[:, None] & (pr / np.maximum(prn, 1e-12) >= cn("red_bid_ratio"))
    sell = np.where(red[None, :] & ~redok, 0.0, sell)
    ref["skipped_red"][:] += ((np.stack([nodes[c]["sell_rel"] for c in chosen]) - sell) * x * pr).sum(1)
    sold = sell * x
    proceeds = (sold * pr).sum(1)
    x -= sold
    C = C + proceeds
    # redemptions
    rd = redm * x
    ref["claim1"][:] += rd * V
    x -= rd
    # adds (liquid holdings, as a share of W)
    buy = addp * W[:, None]
    C = C - (buy * (1 + D["tc_add"][None, :])).sum(1)
    x += buy / np.maximum(V, 1e-12)
    # purchase templates (gated on the path's own state)
    names = D["tpl_names"]
    th = (wd["Vq"][:, qi][:, D["is_pledge"]].sum(1) / np.maximum(wd["Nq"][:, qi][:, D["is_pledge"]].sum(1), 1e-9))
    for k, tt in enumerate(D["tpl"]):
        if is_commit[k]:
            continue
        ok = np.isin(ct, tt["classes"])
        if names[k] == "SEC_BUY":
            ok &= (1 - rho_f[ct] * th) > tt["discount_gate"]
        if tt["green_only"]:
            ok &= green
        amt = np.where(ok, tplp[:, k] * W, 0.0)
        y[:, k, t] += amt
        C = C - amt
    ref["mult_now"][:] = np.where(is_commit[None, :], mult, 0.0)
    # financing targets (ratio of the node's capacity, applied to the path's capacity)
    B = ref["B"]
    PP = (x[:, D["is_pledge"]] * V[:, D["is_pledge"]]).sum(1)
    CSV = (x[:, D["is_cs"]] * V[:, D["is_cs"]]).sum(1)
    SMV = (x[:, D["is_sma"]] * V[:, D["is_sma"]]).sum(1)
    RAV = (x[:, D["is_ra_ctrl"]] * V[:, D["is_ra_ctrl"]]).sum(1)
    caps = np.stack([ref["L"] + ref["Lup"], np.full(n, D["W0"]), np.array(navf["ltv"])[ct] * PP, pref["advance"] * PP,
                     csbl["debt_to_value"] * CSV, smabl["ltv"] * SMV,
                     np.minimum(raco["ltv"] * RAV, raco["cap"])], 1)
    ratio = np.stack([nodes[c]["fin_ratio"] for c in chosen])
    avail = np.zeros((7, 3))
    avail[0] = 1.0
    avail[1] = cf("term_avail")
    avail[2] = navf["avail"]
    avail[3] = pref["avail"]
    avail[4] = csbl["avail"]
    avail[5] = smabl["avail"]
    avail[6] = raco["avail"]
    tgt = ratio * caps
    tgt[:, 1] = ratio[:, 1] * W                  # term debt as a share of W
    oid = np.array([0, 0, navf["oid"], pref["fee"], 0, 0, 0])
    for j in range(7):
        dlt = tgt[:, j] - B[:, j]
        can = avail[j, ct] > 0
        draw = np.where(can, np.maximum(dlt, 0.0), 0.0)
        rep = np.maximum(-dlt, 0.0)
        B[:, j] += draw - rep
        C = C + draw * (1 - oid[j]) - rep
    # overlay targets
    p2s_t = np.stack([nodes[c]["p2s_pct"] for c in chosen]) * W
    dp = p2s_t - ref["p2s"]
    lo1 = D["lo1"]
    frac = dp / np.maximum(V[:, lo1], 1e-9)
    frac = np.minimum(frac, x[:, lo1])
    x[:, lo1] -= frac
    C = C + frac * V[:, lo1] * np.where(frac > 0, 1 - tc_lo, 1 + tc_lo)
    ref["p2s"] = ref["p2s"] + frac * V[:, lo1]
    ref["beta"] = np.stack([nodes[c]["beta_pct"] for c in chosen]) * W
    ref["trs"][:] = np.stack([nodes[c]["trs_pct"] for c in chosen]) * W[:, None]
    hmin = P.get("overlay.tail_budget")[0] / P.get("overlay.tail_premium")
    ref["hed"] = np.maximum(np.stack([nodes[c]["hed_pct"] for c in chosen]), hmin) * W
    ref["opp"] = np.stack([nodes[c]["opp"] for c in chosen]).astype(float)
    ref["C"] = C
