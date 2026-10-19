"""Ledger data for the optimizer (SYNTHETIC - NOT ADIC DATA).

Turns the book, the fused beliefs and the tree into the per-node arrays the LP reads (DSGO section 1.3, the action
ledger): hold trajectories of every holding (full original position; positions only scale them, by positive
homogeneity), per-$ trajectories of every opportunity template from every start node, bids by node class, stressed
flow rates for the red margin, sleeve aggregates for need-based funding, and the static-SAA accrual factors that
turn draws into distribution-inclusive wealth W~ (DSGO section 4.1).
"""
from __future__ import annotations

import numpy as np

from common import GROUPS, Params
from scenarios import UnitEngine
from tree import propagate

SLEEVES = ["LIQ", "HF", "AMB", "RED"]
PACE_GROUPS = ["PE", "SEC", "RA", "PC", "CS"]
PURCHASES = ["SEC_BUY", "CO_DEAL", "CS_NEW", "PC_NEW", "INFRA_LEV", "SMA_LEV"]


def _spec_arrays(segs: list[dict]) -> dict:
    return {"B": np.array([s["B"] for s in segs], float), "yield": np.array([s["yield"] for s in segs], float),
            "dist": np.array([s["dist"] for s in segs], float), "call": np.array([s["call"] for s in segs], float),
            "edges": np.array([s["edges"] for s in segs], float), "phi": np.array([s["phi"] for s in segs], float),
            "liquid": np.array([s["tier"] == "liquid" for s in segs], bool)}


def _rates(spec: dict, age: np.ndarray, V: np.ndarray, U: np.ndarray, P: Params, years: float = 1.0,
           call_mult: float | None = None, dist_mult: float | None = None):
    """Stressed calls and low (P10-type) distributions over the next `years` for states (n, I)."""
    mC = P.arr("private_engine.exit_call_mult")
    mD = P.arr("private_engine.exit_dist_mult")
    stress = P.get("private_engine.crisis_call_stress") if call_mult is None else call_mult
    dm = mD[3] if dist_mult is None else dist_mult
    b = (age[..., None] >= spec["edges"]).sum(-1)
    cols = np.arange(spec["B"].shape[0])
    c_int = spec["call"][cols, b]
    e_int = spec["dist"][cols, b]
    calls = U * (1 - np.exp(-c_int * mC[2] * stress * years))
    dist = V * (spec["yield"] * years + (1 - np.exp(-e_int * dm * years)))
    return calls, dist


def prepare(P: Params, units: list[dict], beliefs: list[dict], book: dict, gen, tr: dict,
            use_beliefs: bool = True) -> dict:
    T = tr["T"]
    lvl, par, cls = tr["level"], tr["parent"], tr["cls"]
    I = len(units)
    rf = P.get("rates.sofr")
    D = {"P": P, "tr": tr, "units": units, "beliefs": beliefs, "I": I, "T": T, "rf": rf}
    D["ids"] = [u["id"] for u in units]
    D["group"] = np.array([u["group"] for u in units])
    D["tier"] = np.array([u["tier"] for u in units])
    D["liquid"] = D["tier"] == "liquid"
    D["red"] = D["tier"] == "red"
    D["amber"] = D["tier"] == "amber"
    D["seg"] = [u["segment"] for u in units]
    spec = _spec_arrays(units)
    D["spec"] = spec
    # ---- beliefs in the tree: alpha_hat + sigma_post x belief error (held from stage 1 to the leaves; RV-01)
    if use_beliefs:
        a_hat = np.array([b["alpha_hat"] for b in beliefs])
    else:   # F10 switch-off: group prior only
        a_hat = np.array([u["alpha_star"] for u in units])
    s_post = np.array([b["sigma_post"] for b in beliefs])
    D["alpha_hat"], D["sigma_post"] = a_hat, s_post
    e = tr["belief_e"]
    eng = UnitEngine(spec, P)
    V0 = np.array([u["nav_econ"] for u in units])
    N0 = np.array([u["nav"] for u in units])
    U0 = np.array([u["unfunded"] for u in units])
    A0 = np.array([u["age"] for u in units], float)
    # the belief error lives in the fan years only (it is drawn at the fan branching); it is scaled so its total
    # effect on 5-year log wealth equals a 5-year alpha error: sigma_post x e x (5 / 3) a year for 3 years
    e_scale = P.get("tree.belief_error_fan_scale")
    e = e * np.where(lvl >= 3, e_scale, 0.0)
    out = propagate(P, tr, eng, {"V": V0, "N": N0, "U": U0, "age": A0},
                    lambda ids: a_hat[None, :] + e[ids][:, None] * s_post[None, :])
    for k in ("V", "N", "U", "D", "C", "G"):
        D[k] = out[k]
    D["age"] = A0[None, :] + lvl[:, None]
    # stressed next-year calls and P10 distributions per node (red margin), 6-month and 24-month variants
    D["callS"], D["distL"] = _rates(spec, D["age"], D["V"], D["U"], P)
    h4 = P.get("constraints.h4")
    mD = P.arr("private_engine.exit_dist_mult")
    D["calls24"], D["dist24"] = _rates(spec, A0, V0, U0, P, years=2.0, call_mult=h4["call_mult"],
                                       dist_mult=mD[2] * h4["dist_factor"])
    # ---- bids: proceeds per unit of fraction sold, by node class (one price primitive: rho on economic NAV)
    rho = P.get("bids.rho")
    agem = P.arr("bids.age_multiplier")
    tc = P.get("trading.tc")
    proc = np.zeros((T, I))
    proc_norm = np.zeros((T, I))
    prem = np.ones(I)
    for i, (u, h) in enumerate(zip(units, book["holdings"])):
        if u["tier"] == "liquid":
            c = tc["hf"] if u["group"] == "HF" else tc.get(u["bid_key"], 0.001)
            if u["group"] == "HF":      # hedge-fund secondary at a class discount
                r = np.array(rho["hf"])
                proc[:, i] = r[cls] * D["V"][:, i]
                proc_norm[:, i] = r[0] * D["V"][:, i]
            else:
                proc[:, i] = (1 - c) * D["V"][:, i]
                proc_norm[:, i] = proc[:, i]
            continue
        r = np.array(rho[u["bid_key"]])
        bucket = (D["age"][:, i][:, None] >= np.asarray(u["edges"])).sum(1)
        am = agem[bucket] if u["age_mult"] else np.ones(T)
        if h["bid"] is not None:   # the unit's own external bid carries its idiosyncratic premium (partly alpha)
            generic = u["theta0"] * r[1] * (agem[u["age_bucket"]] if u["age_mult"] else 1.0)
            prem[i] = h["bid"]["p_ce"] / generic
        proc[:, i] = r[cls] * am * prem[i] * D["V"][:, i]
        proc_norm[:, i] = r[0] * am * prem[i] * D["V"][:, i]
    D["proc"], D["proc_norm"], D["bid_prem"] = proc, proc_norm, prem
    D["tc_add"] = np.array([(tc["hf"] if u["group"] == "HF" else tc.get(u["bid_key"], 0.001)) if u["tier"] == "liquid"
                            else 0.0 for u in units])
    # ---- sleeves (need-based funding sells a sleeve pro rata: equal fractional cut of each member)
    sl = np.full(I, -1)
    for i, u in enumerate(units):
        sl[i] = 0 if u["group"] == "LO" else 1 if u["group"] == "HF" else 2 if u["tier"] == "amber" else 3
    D["sleeve_of"] = sl
    D["S_sl"] = np.stack([D["V"][:, sl == s].sum(1) for s in range(4)], 1)            # (T, 4)
    D["bid_sl"] = np.stack([proc[:, sl == s].sum(1) / np.maximum(D["S_sl"][:, s], 1e-9) for s in range(4)], 1)
    # ---- unit subsets
    D["is_lo_eq"] = np.array([u["group"] == "LO" and u["segment"] != "lo_fi" for u in units])
    D["is_fi"] = np.array([u["segment"] == "lo_fi" for u in units])
    D["is_hf"] = D["group"] == "HF"
    D["is_pledge"] = np.array(["pledge_pool" in u["flags"] for u in units])
    D["is_private"] = np.array([u["group"] in ("PE", "SEC", "CO", "CS", "PC", "RA") for u in units])
    D["is_cs"] = D["group"] == "CS"
    D["is_sma"] = np.array(["sma" in u["flags"] for u in units])
    D["is_ra_ctrl"] = np.array([u["group"] == "RA" and "controlled" in u["flags"] for u in units])
    D["is_re_open"] = np.array(["open_end" in u["flags"] for u in units])
    D["is_enr"] = np.array(["enr" in u["flags"] for u in units])
    D["lo1"] = D["ids"].index("LO-01")
    D["fi"] = int(np.flatnonzero(D["is_fi"])[0])
    # per-unit trade cap (belief risk): |dv| <= k_sel W0 sigma_ref / sigma_post
    sref = float(np.median(s_post))
    D["cap_trade"] = P.get("trading.k_sel") * (V0.sum() + P.get("treasury.cash0")) * sref / s_post
    # ---- tree topology helpers
    D["a2"] = np.full(T, -1)
    D["anc"] = []
    for n in range(T):
        a, j = [], n
        while j >= 0:
            a.append(j)
            j = par[j]
        a = a[::-1]
        D["anc"].append(a)
        if lvl[n] >= 2:
            D["a2"][n] = a[2]
    D["ND"] = int((lvl <= 2).sum())
    assert np.all(np.flatnonzero(lvl <= 2) == np.arange(D["ND"])), "decision nodes must come first"
    D["leaves"] = np.array(tr["leaves"])
    # ---- templates (purchases at decision nodes; commitments at decision nodes and fan years 3-4)
    tpl_specs, tnames = [], []
    for name in PURCHASES:
        t = dict(P.get(f"templates.{name}"))
        s = dict(P.get(f"book.segments.{t['segment']}"))
        s.update({"tier": "tpl"})
        t["seg"] = s
        t["kind"] = "purchase"
        tpl_specs.append(t)
        tnames.append(name)
    plan = P.get("pacing.plan")
    psegs = P.get("pacing.segments")
    astar = P.get("fusion.alpha_star_pp")
    for g in PACE_GROUPS:
        s = dict(P.get(f"book.segments.{psegs[g]}"))
        s.update({"tier": "tpl"})
        tpl_specs.append({"group": g, "family": "PACE", "segment": psegs[g], "age": 0, "seg": s, "kind": "commit",
                          "alpha_pp": [astar[g]] * 3, "plan": plan[g], "lever_debt": 0.0, "lever_spread": 0.0,
                          "unfunded_per_nav": 0.0, "winners_curse": 0.0})
        tnames.append("COMMIT_" + g)
    D["tpl_names"] = tnames
    D["tpl"] = tpl_specs
    K = len(tpl_specs)
    tspec = _spec_arrays([t["seg"] for t in tpl_specs])
    tspec["liquid"] = np.zeros(K, bool)
    teng = UnitEngine(tspec, P)
    D["tspec"] = tspec
    prior_sd = P.get("fusion.unit_prior_sd_pp")
    t_sd = np.array([prior_sd[t["group"]] / 100 for t in tpl_specs])
    # theta of the fund book at each node (prices secondary purchases on economic NAV)
    fund = np.array([u["kind"] == "fund" and u["group"] in ("PE", "SEC") for u in units])
    D["theta_fund"] = D["V"][:, fund].sum(1) / np.maximum(D["N"][:, fund].sum(1), 1e-9)
    starts = [n for n in range(T) if lvl[n] <= 4]
    # pairs (m, n): n strictly below m in m's subtree
    children = tr["children"]
    pair_m, pair_n = [], []
    sub = {}
    for m in starts:
        lst, fr = [], [m]
        while fr:
            nx = []
            for i in fr:
                nx.extend(children[i])
            lst.extend(nx)
            fr = nx
        sub[m] = lst
        for n in lst:
            pair_m.append(m)
            pair_n.append(n)
    pair_m, pair_n = np.array(pair_m), np.array(pair_n)
    D["pair_index"] = {(int(m), int(n)): k for k, (m, n) in enumerate(zip(pair_m, pair_n))}
    # initial per-$ state at each start node
    rho_f = np.array(rho["fund"])
    init = {k: np.zeros((T, K)) for k in ("V", "N", "U", "age")}
    for j, t in enumerate(tpl_specs):
        if t["kind"] == "commit":
            init["U"][:, j] = 1.0
        elif tnames[j] == "SEC_BUY":
            price = rho_f[cls] * D["theta_fund"]                # per $ of reported NAV
            init["N"][:, j] = 1.0 / price
            init["V"][:, j] = (1 - t["winners_curse"]) / rho_f[cls]
            init["U"][:, j] = t["unfunded_per_nav"] / price
            init["age"][:, j] = t["age"]
        else:
            g = 1.0 + t["lever_debt"]
            init["V"][:, j] = g
            init["N"][:, j] = g
            init["age"][:, j] = t["age"]
    D["tpl_init"] = init
    t_alpha = np.array([[t["alpha_pp"][c] / 100 for c in range(3)] for t in tpl_specs])   # (K, class)
    # propagate all pairs level by level
    npair = len(pair_m)
    arr = {k: np.zeros((npair, K)) for k in ("V", "N", "U", "D", "C", "G")}
    state = {}
    for L in range(1, 6):
        sel = np.flatnonzero(lvl[pair_n] == L)
        if len(sel) == 0:
            continue
        pm, pn = pair_m[sel], pair_n[sel]
        pp = par[pn]
        st = {k: np.zeros((len(sel), K)) for k in ("V", "N", "U", "age", "rl", "rr")}
        for r, (m, p) in enumerate(zip(pm, pp)):
            if p == m:
                st["V"][r], st["N"][r], st["U"][r], st["age"][r] = init["V"][m], init["N"][m], init["U"][m], init["age"][m]
            else:
                s0 = state[(int(m), int(p))]
                for k in st:
                    st[k][r] = s0[k]
        alpha = t_alpha[:, cls[pm]].T + e[pn][:, None] * t_sd[None, :]
        Ds = np.zeros((len(sel), K))
        Cs = np.zeros((len(sel), K))
        lg = np.zeros((len(sel), K))
        for q in range(4):
            f = np.array([tr["nodes"][i]["seg"]["f"][q] for i in pn])
            Eq = np.array([tr["nodes"][i]["seg"]["E"][q] for i in pn])
            Sq = np.array([tr["nodes"][i]["seg"]["S"][q] for i in pn])
            st, Dq, Cq, r_ = teng.step(st, f, Eq, Sq, alpha)
            Ds += Dq
            Cs += Cq
            lg += r_
        for r, k in enumerate(sel):
            state[(int(pair_m[k]), int(pair_n[k]))] = {kk: st[kk][r] for kk in st}
        arr["V"][sel], arr["N"][sel], arr["U"][sel] = st["V"], st["N"], st["U"]
        arr["D"][sel], arr["C"][sel], arr["G"][sel] = Ds, Cs, np.exp(lg)
        arr.setdefault("age", np.zeros((npair, K)))
        arr["age"][sel] = st["age"]
    D["tpl_arr"] = arr
    pc, pd = _rates(tspec, arr["age"], arr["V"], arr["U"], P)
    D["tpl_callS"], D["tpl_distL"] = pc, pd
    ic, idl = _rates(tspec, init["age"], init["V"], init["U"], P)
    D["tpl_init_callS"], D["tpl_init_distL"] = ic, idl
    c24, d24 = _rates(tspec, init["age"][0:1], init["V"][0:1], init["U"][0:1], P, years=2.0,
                      call_mult=h4["call_mult"], dist_mult=mD[2] * h4["dist_factor"])
    D["tpl_init_calls24"], D["tpl_init_dist24"] = c24[0], d24[0]
    D["tpl_debt"] = np.array([t["lever_debt"] for t in tpl_specs])
    D["tpl_spread"] = np.array([t["lever_spread"] for t in tpl_specs])
    D["tpl_group"] = np.array([t["group"] for t in tpl_specs])
    D["tpl_is_commit"] = np.array([t["kind"] == "commit" for t in tpl_specs])
    D["tpl_private"] = np.ones(K, bool)
    # ---- node market data
    rf_g = np.exp(rf)
    D["Geq"] = 1.0 + tr["eq_tot"]
    D["tailpay"] = tr["tail_pay"]
    ov = lambda k: P.get(f"overlay.{k}")
    f_year = tr["f_year"]
    z_eq = (f_year[:, 0] - gen.w_eq.mean()) / ov("eq_vol_ref")
    z_v = f_year[:, 5] / ov("vix_vol_ref")
    lo, lv = ov("opp_load_eq"), ov("opp_load_vol")
    norm_ = np.sqrt(lo ** 2 + lv ** 2)
    D["oppret"] = ov("opp_vol_per_im") * (ov("opp_sr_prior")
                                          + (lo * z_eq + lv * z_v) / norm_ * np.sqrt(1.0 - ov("opp_idio_share")))
    D["oppret"][0] = 0.0
    # ---- static-SAA return per node (accrues draws to the horizon in W~; error ledger E1)
    W0 = V0.sum() + P.get("treasury.cash0")
    D["W0"] = W0
    w_u = V0 / W0
    w_c = P.get("treasury.cash0") / W0
    fb = np.array(ov("beta_fin_spread"))
    r_saa = (D["G"] - 1.0) @ w_u + w_c * (rf_g - 1.0) + ov("beta_sq") / W0 * (D["Geq"] - rf_g - fb[cls])
    r_saa[0] = 0.0
    D["r_saa"] = r_saa
    # accrual factor G_{t(n) -> 5} along each leaf path for every node on it
    acc = {}
    for li, leaf in enumerate(D["leaves"]):
        path = D["anc"][leaf]       # root .. leaf
        g = 1.0
        for n in path[::-1]:
            acc[(li, n)] = g
            g *= (1.0 + r_saa[n]) if n > 0 else 1.0
    D["acc"] = acc
    D["Wstar"] = W0 * (1 + P.get("goal.rate")) ** P.get("goal.years")
    return D
