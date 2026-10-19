"""Component 2b: the decision tree (SYNTHETIC - NOT ADIC DATA).

Shape K1 x K2 x F (default 10 x 7 x 3 = 210 leaves; decisions at t = 0, 1, 2; fan years t = 3, 4, 5 are constraint
nodes). The computed task asks for about 200 leaves; DSGO's 640-leaf 10 x 8 x 8 tree does not fit the 15-minute
budget, so the rank rule (children >= matched drivers + 1) is kept at both decision branchings by matching:
  stage 1: 6 factor drivers + the belief-error driver (d = 7 <= K1 - 1 = 9)
  stage 2: 6 factor drivers                            (d = 6 <= K2 - 1 = 6)
  fans:    the status-quo portfolio's 3-year return    (d = 1 <= F - 1 = 2)
The draw rate is a deterministic function of the matched Brent path, so it is not matched separately.

Construction (DSGO section 5.2, scaled): simulate N1 one-year paths from today; stratify by node class and shock type
(at least one demand-bust branch, one other STR branch and a Gulf-war continuation branch); k-means inside strata on
observable features; the medoid path represents each cluster with the cluster's probability mass; an affine map then
matches the branch drivers' conditional mean and covariance exactly (Hoyland-Wallace style). Stage 2 repeats from
each stage-1 node with N2 continuations (worlds drawn from the cluster's world mix, so recourse cannot learn the
world). Fans take one medoid path per tercile of the status-quo 3-year return.
Every holding and every per-$ template (opportunity purchases and new commitments started at t = 0, 1, 2) is then
propagated through the shared quarterly engine along the tree.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import norm

from common import Params
from scenarios import Generator, UnitEngine, node_class


def kmeans(X, k, rng, iters=60):
    n = len(X)
    if n <= k:
        return np.arange(n), X.copy()
    C = [X[rng.integers(n)]]
    d2 = ((X - C[0]) ** 2).sum(1)
    for _ in range(1, k):
        p = d2 / max(d2.sum(), 1e-300)
        j = rng.choice(n, p=p)
        C.append(X[j])
        d2 = np.minimum(d2, ((X - X[j]) ** 2).sum(1))
    C = np.array(C)
    lab = np.zeros(n, int)
    for _ in range(iters):
        D = ((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)
        lab = D.argmin(1)
        newC = np.array([X[lab == j].mean(0) if np.any(lab == j) else C[j] for j in range(k)])
        if np.allclose(newC, C, atol=1e-12):
            break
        C = newC
    return lab, C


def _sqrtm(S, floor=0.0, inverse=False):
    w, V = np.linalg.eigh((S + S.T) / 2)
    w = np.clip(w, floor, None)
    return (V / np.sqrt(w)) @ V.T if inverse else (V * np.sqrt(w)) @ V.T


def moment_match(Xc, p, m, S):
    """Minimum-distortion affine map (the Gaussian optimal-transport map) so the p-weighted mean and covariance of
    the branch values equal (m, S) exactly: A = S^1/2 (S^1/2 Sc S^1/2)^-1/2 S^1/2 is symmetric, so A Sc A' = S.
    Unlike a Cholesky map it does not rotate the branches, so a demand-bust branch stays a demand bust."""
    xbar = p @ Xc
    Dv = Xc - xbar
    Sc = (Dv * p[:, None]).T @ Dv
    ridge = 1e-14 * max(np.trace(S), 1e-300)
    St = _sqrtm(S)
    A = St @ _sqrtm(St @ Sc @ St, floor=ridge, inverse=True) @ St
    return m + Dv @ A.T


def moment_report(Xc, p, m, S):
    xbar = p @ Xc
    Dv = Xc - xbar
    Sc = (Dv * p[:, None]).T @ Dv
    sd_t, sd_c = np.sqrt(np.diag(S)), np.sqrt(np.maximum(np.diag(Sc), 1e-300))
    Ct, Cc = S / np.outer(sd_t, sd_t), Sc / np.outer(sd_c, sd_c)
    return {"max_abs_mean_err": float(np.max(np.abs(xbar - m))),
            "max_rel_vol_err": float(np.max(np.abs(sd_c / sd_t - 1))),
            "max_abs_corr_err": float(np.max(np.abs(Cc - Ct)))}


def _allocate(masses, total, mins):
    """Largest-remainder allocation of `total` branches over strata with minimum counts where mass > 0."""
    masses = np.asarray(masses, float)
    alloc = np.array([mins[i] if masses[i] > 0 else 0 for i in range(len(masses))], int)
    rest = total - alloc.sum()
    if rest < 0:
        raise ValueError("minimum branch counts exceed the branch total")
    if rest > 0 and masses.sum() > 0:
        raw = masses / masses.sum() * total - alloc
        raw = np.clip(raw, 0, None)
        if raw.sum() <= 0:
            raw = masses.copy()
        share = raw / raw.sum() * rest
        add = np.floor(share).astype(int)
        while add.sum() < rest:
            add[int(np.argmax(share - add))] += 1
        alloc = alloc + add
    return alloc


class Tree:
    """Time-nodes: levels 0 (root), 1, 2 (decision nodes) and 3, 4, 5 (fan years of each leaf path)."""

    def __init__(self):
        self.parent, self.level, self.prob = [], [], []
        self.seg = []                      # per node: dict with the 4-quarter segment into the node


def _segment(sim, j, q0, q1):
    """Extract quarters [q0, q1) of simulated path j as a node segment (states at the end of each quarter)."""
    return {"f": sim["f"][j, q0:q1].copy(),
            "S": sim["S"][j, q0 + 1:q1 + 1].copy(), "E": sim["E"][j, q0 + 1:q1 + 1].copy(),
            "Z": sim["Z"][j, q0 + 1:q1 + 1].copy(),
            "end": {k: float(sim[k][j, q1]) for k in ("cs", "y", "lb", "X", "vix")},
            "S_end": int(sim["S"][j, q1]), "E_end": int(sim["E"][j, q1]), "Z_end": int(sim["Z"][j, q1]),
            "d": float(sim["draw"][j, q0 // 4]), "w": int(sim["w"][j])}


def _apply_shift(seg, dx, gen):
    """Spread an annual driver adjustment dx (6,) evenly over the segment's quarters; adjust levels consistently."""
    nq = len(seg["f"])
    seg["f"] = seg["f"] + dx[None, :] / nq
    seg["end"]["cs"] = max(seg["end"]["cs"] - dx[1] / gen.cs_D, 0.005)
    seg["end"]["y"] = max(seg["end"]["y"] - dx[2] / gen.y_D, 0.0)
    seg["end"]["lb"] = seg["end"]["lb"] + dx[3]
    seg["end"]["X"] = seg["end"]["X"] + dx[4]
    seg["end"]["vix"] = max(seg["end"]["vix"] + 100 * dx[5], gen.v_floor)


def _features(eq_year, end, d_next):
    return np.array([eq_year, end["cs"], end["y"], end["lb"], end["X"], end["vix"], d_next])


def _start_from(seg_end, S, E, Z, d, w, n, gen):
    return {"S": np.full(n, S), "E": np.full(n, E), "Z": np.full(n, Z),
            "cs": np.full(n, seg_end["cs"]), "y": np.full(n, seg_end["y"]), "lb": np.full(n, seg_end["lb"]),
            "X": np.full(n, seg_end["X"]), "vix": np.full(n, seg_end["vix"]), "d_prev": np.full(n, d), "w": w}


def build_tree(P: Params, gen: Generator, rng, b_sq: np.ndarray, a_sq: float, log=print, seed_tag=0) -> dict:
    """b_sq (6,), a_sq: status-quo portfolio loadings and alpha for the fan stratification statistic."""
    K1, K2 = P.get("tree.branches")
    F = P.get("tree.fan_paths")
    N1, N2, NF = P.get("tree.n_stage1_paths"), P.get("tree.n_stage2_paths"), P.get("tree.n_fan_candidates")
    alloc1 = P.get("tree.stage1_strata")
    min_paths = P.get("tree.min_stratum_paths")
    rf = gen.rf
    nodes = []   # list of dicts

    def add_node(parent, level, prob, seg, extra=None):
        nd = {"id": len(nodes), "parent": parent, "level": level, "prob": prob, "seg": seg, "children": []}
        if extra:
            nd.update(extra)
        if parent is not None:
            nodes[parent]["children"].append(nd["id"])
        nodes.append(nd)
        return nd["id"]

    st0 = gen.start_state(1, rng)
    root_seg = {"f": np.zeros((0, 6)), "S": np.zeros(0, int), "E": np.zeros(0, int), "Z": np.zeros(0, int),
                "end": {"cs": gen.cs0, "y": gen.y0, "lb": gen.lb0, "X": gen.x0, "vix": gen.v0},
                "S_end": int(np.argmax(gen.s0p)), "E_end": int(np.argmax(gen.e0p)), "Z_end": int(np.argmax(gen.z0p)),
                "d": gen.d_prior, "w": -1}
    add_node(None, 0, 1.0, root_seg, {"world_mix": gen.w_prob.copy()})
    checks = {"moments": [], "rank_rule": True}

    # ------------------------------------------------------------- stage 1
    st = gen.start_state(N1, rng)
    sim = gen.simulate(st, 4, rng)
    drv = sim["f"].sum(1)                                   # annual drivers (N1, 6)
    end_d = gen.expected_next_draw(np.exp(sim["lb"][:, 4]), sim["draw"][:, 0], sim["Z"][:, 4])
    cls = node_class(sim["S"][:, 4], sim["E"][:, 4], sim["Z"][:, 4], end_d, P)
    Z4 = sim["Z"][:, 4]
    strata = {"STR_DB": (cls == 2) & (Z4 == 3), "STR_other": (cls == 2) & (Z4 != 3),
              "DRT_GW": (cls == 1) & (Z4 == 5), "DRT": (cls == 1) & (Z4 != 5), "BEN": cls == 0}
    names = list(strata)
    masses = np.array([strata[k].sum() for k in names], float)
    want = np.array([alloc1[k] for k in names])
    # merge strata too small to support their branches into the nearest compatible stratum
    merge_to = {"STR_DB": "STR_other", "STR_other": "DRT", "DRT_GW": "DRT", "DRT": "BEN", "BEN": "DRT"}
    for i, k in enumerate(names):
        if masses[i] < max(min_paths, want[i]):
            tgt = names.index(merge_to[k])
            strata[merge_to[k]] = strata[merge_to[k]] | strata[k]
            strata[k] = np.zeros(N1, bool)
            want[tgt] += want[i]
            want[i] = 0
    masses = np.array([strata[k].sum() for k in names], float)
    feats = np.column_stack([drv[:, 0], sim["cs"][:, 4], sim["y"][:, 4], sim["lb"][:, 4], sim["X"][:, 4],
                             sim["vix"][:, 4], end_d])
    fmu, fsd = feats.mean(0), feats.std(0) + 1e-12
    Xs = (feats - fmu) / fsd
    reps, probs, strat_of, wmix = [], [], [], []
    for i, k in enumerate(names):
        if want[i] == 0 or masses[i] == 0:
            continue
        idx = np.flatnonzero(strata[k])
        lab, C = kmeans(Xs[idx], int(want[i]), rng)
        for j in range(int(want[i])):
            mem = idx[lab == j]
            if len(mem) == 0:
                continue
            med = mem[np.argmin(((Xs[mem] - C[j]) ** 2).sum(1))]
            reps.append(med)
            probs.append(len(mem) / N1)
            strat_of.append(k)
            wmix.append(np.bincount(sim["w"][mem], minlength=len(gen.w_prob)) / len(mem))
    probs = np.array(probs)
    K1_eff = len(reps)
    # Stage 1 matches the six factor drivers. The belief-error driver (RV-01) is NOT drawn here: drawn at stage 1 it
    # is known to every stage-1 decision in the tree but invisible to the executed playbook (which maps paths on
    # observables), a look-ahead leak measured out of sample. It is drawn at the fan branching instead (below).
    Xc = drv[reps]
    m_t = drv.mean(0)
    S_t = np.cov(drv.T, bias=True)
    before = moment_report(Xc, probs, m_t, S_t)
    Xm = moment_match(Xc, probs, m_t, S_t)
    after = moment_report(Xm, probs, m_t, S_t)
    checks["moments"].append({"branching": "root", "children": K1_eff, "drivers": 6, "before": before, "after": after})
    checks["rank_rule"] &= K1_eff >= 6 + 1
    for c in range(K1_eff):
        seg = _segment(sim, reps[c], 0, 4)
        _apply_shift(seg, Xm[c] - drv[reps[c]], gen)
        add_node(0, 1, float(probs[c]), seg, {"stratum": strat_of[c], "belief_e": 0.0, "world_mix": wmix[c]})

    # ------------------------------------------------------------- stage 2
    st1 = [n for n in nodes if n["level"] == 1]
    for nd in st1:
        sg = nd["seg"]
        w = rng.choice(len(gen.w_prob), size=N2, p=nd["world_mix"])
        st = _start_from(sg["end"], sg["S_end"], sg["E_end"], sg["Z_end"], sg["d"], w, N2, gen)
        sim2 = gen.simulate(st, 4, rng)
        drv2 = sim2["f"].sum(1)
        d2n = gen.expected_next_draw(np.exp(sim2["lb"][:, 4]), sim2["draw"][:, 0], sim2["Z"][:, 4])
        cls2 = node_class(sim2["S"][:, 4], sim2["E"][:, 4], sim2["Z"][:, 4], d2n, P)
        ms = np.array([(cls2 == c).sum() for c in range(3)], float) / N2
        mins = [1 if ms[c] >= P.get("tree.stage2_min_class_mass") else 0 for c in range(3)]
        al = _allocate(ms * (ms >= P.get("tree.stage2_min_class_mass")), K2, mins)
        f2 = np.column_stack([drv2[:, 0], sim2["cs"][:, 4], sim2["y"][:, 4], sim2["lb"][:, 4], sim2["X"][:, 4],
                              sim2["vix"][:, 4], d2n])
        X2 = (f2 - fmu) / fsd
        reps2, members, cents = [], [], []
        for c in range(3):
            if al[c] == 0:
                continue
            idx = np.flatnonzero(cls2 == c)
            lab, C = kmeans(X2[idx], int(al[c]), rng)
            for j in range(int(al[c])):
                mem = idx[lab == j]
                if len(mem) == 0:
                    continue
                reps2.append(mem[np.argmin(((X2[mem] - C[j]) ** 2).sum(1))])
                members.append(list(mem))
                cents.append(C[j])
        # paths of classes too rare for their own branch join the nearest cluster: no probability mass is dropped
        orphan = np.flatnonzero(np.isin(cls2, [c for c in range(3) if al[c] == 0]))
        if len(orphan):
            Cm = np.array(cents)
            near = ((X2[orphan][:, None, :] - Cm[None, :, :]) ** 2).sum(-1).argmin(1)
            for o, k in zip(orphan, near):
                members[k].append(o)
        pr2 = np.array([len(m) for m in members], float) / N2
        wm2 = [np.bincount(sim2["w"][np.array(m)], minlength=len(gen.w_prob)) / len(m) for m in members]
        Xc2 = drv2[reps2]
        m2, S2 = drv2.mean(0), np.cov(drv2.T, bias=True)
        b2 = moment_report(Xc2, pr2, m2, S2)
        Xm2 = moment_match(Xc2, pr2, m2, S2)
        a2 = moment_report(Xm2, pr2, m2, S2)
        checks["moments"].append({"branching": f"node{nd['id']}", "children": len(reps2), "drivers": 6,
                                  "before": b2, "after": a2})
        checks["rank_rule"] &= len(reps2) >= 6 + 1
        for c in range(len(reps2)):
            seg = _segment(sim2, reps2[c], 0, 4)
            _apply_shift(seg, Xm2[c] - drv2[reps2[c]], gen)
            add_node(nd["id"], 2, nd["prob"] * float(pr2[c]), seg, {"belief_e": 0.0, "world_mix": wm2[c]})

    # ------------------------------------------------------------- fans
    st2 = [n for n in nodes if n["level"] == 2]
    leaves = []
    for nd in st2:
        sg = nd["seg"]
        w = rng.choice(len(gen.w_prob), size=NF, p=nd["world_mix"])
        st = _start_from(sg["end"], sg["S_end"], sg["E_end"], sg["Z_end"], sg["d"], w, NF, gen)
        simf = gen.simulate(st, 12, rng)
        r_sq = (rf / 4 + simf["f"] @ b_sq + a_sq / 4).sum(1)       # status-quo 3-year log return
        order = np.argsort(r_sq, kind="stable")
        groups = np.array_split(order, F)
        dsum = simf["draw"].sum(1)
        Zf = np.column_stack([r_sq, dsum, simf["f"][:, :, 0].sum(1)])
        Zs = (Zf - Zf.mean(0)) / (Zf.std(0) + 1e-12)
        reps_f = [g[np.argmin(((Zs[g] - Zs[g].mean(0)) ** 2).sum(1))] for g in groups]
        xr = r_sq[reps_f]
        m_f, v_f = r_sq.mean(), r_sq.var()
        x_bar, v_r = xr.mean(), xr.var()
        s = np.sqrt(v_f / max(v_r, 1e-12))
        x_new = m_f + s * (xr - x_bar)
        # belief-error driver e (RV-01), drawn here so no decision node can condition on it: zero mean, unit
        # variance and zero correlation with the matched fan return (with F = 3, e is the unit vector orthogonal
        # to 1 and to the centred fan returns; its sign is random). Rank rule at the fans: d = 2 <= F - 1.
        dvec = x_new - x_new.mean()
        if F == 3 and np.linalg.norm(dvec) > 1e-12:
            e_f = np.cross(np.ones(3), dvec)
        else:
            e_f = rng.standard_normal(F)
            e_f -= e_f.mean()
            e_f -= dvec * (e_f @ dvec) / max(dvec @ dvec, 1e-300)
        e_f = e_f / np.sqrt(np.mean(e_f ** 2)) * (1.0 if rng.random() < 0.5 else -1.0)
        checks["moments"].append({"branching": f"fan{nd['id']}", "children": F, "drivers": 2,
                                  "before": {"max_abs_mean_err": float(abs(x_bar - m_f)),
                                             "max_rel_vol_err": float(abs(np.sqrt(v_r / v_f) - 1)),
                                             "max_abs_corr_err": 0.0},
                                  "after": {"max_abs_mean_err": float(max(abs(x_new.mean() - m_f), abs(e_f.mean()))),
                                            "max_rel_vol_err": float(max(abs(np.sqrt(x_new.var() / v_f) - 1),
                                                                         abs(np.sqrt(np.mean(e_f ** 2)) - 1))),
                                            "max_abs_corr_err": float(abs(np.mean(e_f * dvec)) /
                                                                      max(np.sqrt(np.mean(dvec ** 2)), 1e-300))}})
        checks["rank_rule"] &= F >= 2 + 1
        for k, j in enumerate(reps_f):
            delta_eq = (x_new[k] - xr[k]) / max(b_sq[0], 1e-6)          # shift carried by the equity factor
            par = nd["id"]
            for yr in range(3):
                seg = _segment(simf, j, 4 * yr, 4 * yr + 4)
                dx = np.zeros(6)
                dx[0] = delta_eq / 3
                _apply_shift(seg, dx, gen)
                par = add_node(par, 3 + yr, nd["prob"] / F, seg, {"belief_e": float(e_f[k]),
                                                                  "world_mix": nd["world_mix"],
                                                                  "leaf": len(leaves)})
            leaves.append(par)
    checks["leaves"] = len(leaves)
    checks["decision_nodes"] = sum(1 for n in nodes if n["level"] <= 2)
    return {"nodes": nodes, "leaves": leaves, "checks": checks, "feat_mu": fmu, "feat_sd": fsd}


def finalize_tree(P: Params, gen: Generator, tr: dict):
    """Per-node annual quantities: class, draw rates, equity total return, tail payoff, features, SAA return later."""
    nodes = tr["nodes"]
    rf = gen.rf
    T = len(nodes)
    lvl = np.array([n["level"] for n in nodes])
    par = np.array([-1 if n["parent"] is None else n["parent"] for n in nodes])
    prob = np.array([n["prob"] for n in nodes])
    S_end = np.array([n["seg"]["S_end"] for n in nodes])
    E_end = np.array([n["seg"]["E_end"] for n in nodes])
    Z_end = np.array([n["seg"]["Z_end"] for n in nodes])
    lb_end = np.array([n["seg"]["end"]["lb"] for n in nodes])
    d_year = np.array([n["seg"]["d"] for n in nodes])              # draw rate of the year INTO the node
    d_next = gen.expected_next_draw(np.exp(lb_end), d_year, Z_end)
    cls = node_class(S_end, E_end, Z_end, d_next, P)
    cls[0] = 1                                                      # today: exit drought, no crisis -> DRT
    f_year = np.array([n["seg"]["f"].sum(0) if len(n["seg"]["f"]) else np.zeros(6) for n in nodes])
    eq_tot = np.array([np.exp((n["seg"]["f"][:, 0] + rf / 4).sum()) - 1 if len(n["seg"]["f"]) else 0.0 for n in nodes])
    lo, width, mult = P.get("overlay.tail_strike_lo"), P.get("overlay.tail_width"), P.get("overlay.tail_rung_factor")
    tail = mult * np.clip(-eq_tot - lo, 0, width)
    vix = np.array([n["seg"]["end"]["vix"] for n in nodes])
    feats = np.array([_features(f_year[i, 0], nodes[i]["seg"]["end"], d_next[i]) for i in range(T)])
    leaf_of = np.full(T, -1)
    for k, li in enumerate(tr["leaves"]):
        j = li
        while j >= 0 and lvl[j] >= 3:
            leaf_of[j] = k
            j = par[j]
    first_after_str = np.zeros(T, bool)
    for i in range(1, T):
        first_after_str[i] = cls[par[i]] == 2 and cls[i] != 2
    tr.update(T=T, level=lvl, parent=par, prob=prob, S_end=S_end, E_end=E_end, Z_end=Z_end, lb_end=lb_end,
              d_year=d_year, d_next=d_next, cls=cls, f_year=f_year, eq_tot=eq_tot, tail_pay=tail, vix=vix,
              features=feats, leaf_of=leaf_of, first_after_str=first_after_str,
              belief_e=np.array([n.get("belief_e", 0.0) for n in nodes]))
    tr["children"] = [n["children"] for n in nodes]
    return tr


def propagate(P: Params, tr: dict, eng: UnitEngine, init: dict, alpha_rows, label="units"):
    """Run the engine along the tree. init: {'V','N','U','age'} arrays (I,) at the root.
    alpha_rows(node_ids) -> (n, I) annual alphas for the year into each node (belief error included by caller).
    Returns per node (T, I) arrays: V, N, U (end of year), D, C (flows in the year), G (gross return factor)."""
    T, I = tr["T"], eng.I
    out = {k: np.zeros((T, I)) for k in ("V", "N", "U", "D", "C", "G")}
    state = {}
    s0 = eng.init_state(1, init["V"], init["N"], init["U"], init["age"])
    state[0] = s0
    for k in ("V", "N", "U"):
        out[k][0] = s0[k][0]
    out["G"][0] = 1.0
    for L in range(1, 6):
        ids = np.flatnonzero(tr["level"] == L)
        if len(ids) == 0:
            continue
        pst = {k: np.concatenate([state[tr["parent"][i]][k] for i in ids]) for k in state[0]}
        a = alpha_rows(ids)
        Dsum = np.zeros((len(ids), I))
        Csum = np.zeros((len(ids), I))
        logg = np.zeros((len(ids), I))
        st = pst
        for q in range(4):
            f = np.array([tr["nodes"][i]["seg"]["f"][q] for i in ids])
            E = np.array([tr["nodes"][i]["seg"]["E"][q] for i in ids])
            S = np.array([tr["nodes"][i]["seg"]["S"][q] for i in ids])
            st, D, C, r = eng.step(st, f, E, S, a)
            Dsum += D
            Csum += C
            logg += r
        for j, i in enumerate(ids):
            state[i] = {k: st[k][j:j + 1] for k in st}
        out["V"][ids], out["N"][ids], out["U"][ids] = st["V"], st["N"], st["U"]
        out["D"][ids], out["C"][ids], out["G"][ids] = Dsum, Csum, np.exp(logg)
    return out


def propagate_templates(P: Params, tr: dict, eng: UnitEngine, init_fn, alpha_fn):
    """Per-$ template trajectories for purchases/commitments started at each decision node.
    init_fn(start_node) -> dict of (V, N, U, age) arrays (I_t,) per $ at the start node (after purchase).
    alpha_fn(start_node, node_ids) -> (n, I_t) alphas. Returns dict keyed by start node -> arrays over the subtree:
    {'nodes': descendant ids (incl. start), 'V','N','U','D','C' (len, I_t)}."""
    res = {}
    T = tr["T"]
    dec = np.flatnonzero(tr["level"] <= 2)
    # descendants of each decision node (BFS order by level)
    for m in dec:
        sub = [m]
        frontier = [m]
        while frontier:
            nxt = []
            for i in frontier:
                nxt.extend(tr["children"][i])
            sub.extend(nxt)
            frontier = nxt
        sub = np.array(sub)
        I = eng.I
        vals = {k: np.zeros((len(sub), I)) for k in ("V", "N", "U", "D", "C")}
        pos = {int(i): j for j, i in enumerate(sub)}
        ini = init_fn(m)
        s0 = eng.init_state(1, ini["V"], ini["N"], ini["U"], ini["age"])
        state = {int(m): s0}
        vals["V"][0], vals["N"][0], vals["U"][0] = s0["V"][0], s0["N"][0], s0["U"][0]
        for L in range(int(tr["level"][m]) + 1, 6):
            ids = np.array([i for i in sub if tr["level"][i] == L])
            if len(ids) == 0:
                continue
            st = {k: np.concatenate([state[int(tr["parent"][i])][k] for i in ids]) for k in s0}
            a = alpha_fn(m, ids)
            Dsum = np.zeros((len(ids), I))
            Csum = np.zeros((len(ids), I))
            for q in range(4):
                f = np.array([tr["nodes"][i]["seg"]["f"][q] for i in ids])
                E = np.array([tr["nodes"][i]["seg"]["E"][q] for i in ids])
                S = np.array([tr["nodes"][i]["seg"]["S"][q] for i in ids])
                st, D, C, r = eng.step(st, f, E, S, a)
                Dsum += D
                Csum += C
            for j, i in enumerate(ids):
                state[int(i)] = {k: st[k][j:j + 1] for k in st}
                p = pos[int(i)]
                vals["V"][p], vals["N"][p], vals["U"][p] = st["V"][j], st["N"][j], st["U"][j]
                vals["D"][p], vals["C"][p] = Dsum[j], Csum[j]
        res[int(m)] = {"nodes": sub, "pos": pos, **vals}
    return res


def leaf_paths(tr: dict):
    """For each leaf: the list of time-nodes from level 1 to level 5 (its full 5-year path)."""
    paths = []
    for li in tr["leaves"]:
        p, j = [], li
        while j > 0:
            p.append(j)
            j = tr["parent"][j]
        paths.append(p[::-1])
    return paths
