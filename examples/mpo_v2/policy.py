"""Policies from LP solutions, lens labels (R1) and decision cards (SYNTHETIC - NOT ADIC DATA).

- extract_policy: the root decision in dollars (applied exactly) and every stage-1/stage-2 node's decisions in
  relative form (sell / redeem as a share of the holding, adds and purchases as a share of W, commitments as a
  multiple of plan, financing as a share of the node's capacity, overlay as a share of W) for the playbook.
- r1_labels: DSGO section 1.2 R1, LEVER_n = min(dB+, dE_disc+), REFINANCE_n = dB+ - LEVER_n.
- cards: reservation price p* = nu_i / (lambda_0 N_i) from the solved LP's duals (x-balance and root cash row), the
  goal-basis hurdle h_i = mu_i - ln(p*/theta)/D, the break-even return, the liquidity premium from the cash-row
  duals, binding rows - every card quantity is read from the LP that made the decision (RV-08).
"""
from __future__ import annotations

import numpy as np

from model import FIN, FIN_FAMILY, MPOModel


def extract_policy(m: MPOModel, x: np.ndarray) -> dict:
    D, P = m.D, m.P
    ND = m.ND
    V = D["V"]
    plan = np.array([t.get("plan", 0.0) for t in D["tpl"]])
    is_commit = D["tpl_is_commit"]
    cf = lambda k: P.get(f"corporate_finance.{k}")
    navf, pref, csbl, smabl, raco = cf("navf"), cf("pref"), cf("csbl"), cf("smabl"), cf("raco")
    Ls = cf("revolver_signed")
    Lup = float(x[m.LUP[0]])
    root = {"sell": np.clip(x[m.S[0]], 0, None), "redeem": np.clip(x[m.R[0]], 0, None),
            "add": np.clip(x[m.A[0]], 0, None), "tpl": np.clip(x[m.Y[0]], 0, None), "p2s": float(x[m.PI[0]]),
            "beta": float(x[m.BETA[0]]), "trs": np.clip(x[m.TRS[0]], 0, None), "hed": float(x[m.HED[0]]),
            "opp": float(x[m.OPP[0]]), "fin": np.clip(x[m.FB[0]], 0, None), "Lup": Lup}
    feats = D["tr"]["features"]
    mu, sd = D["tr"]["feat_mu"], D["tr"]["feat_sd"]
    nodes = {}
    for n in range(1, ND):
        p = m.par[n]
        xp = x[m.X[p]]
        W = x[m.W[n]]
        c = m.cls[n]
        safe = np.where(xp > 1e-9, xp, 1.0)
        PP = x[m.PP[n]]
        CSV = float((x[m.X[n]] * V[n] * D["is_cs"]).sum())
        SMV = float((x[m.X[n]] * V[n] * D["is_sma"]).sum())
        RAV = float((x[m.X[n]] * V[n] * D["is_ra_ctrl"]).sum())
        caps = np.array([Ls + Lup, W, navf["ltv"][c] * PP, pref["advance"] * PP, csbl["debt_to_value"] * CSV,
                         smabl["ltv"] * SMV, min(raco["ltv"] * RAV, raco["cap"])])
        Bn = x[m.FB[n]]
        ratio = np.where(caps > 1e-9, Bn / np.maximum(caps, 1e-9), 0.0)
        nodes[n] = {"cls": int(c), "fz": (feats[n] - mu) / sd,
                    "sell_rel": np.where(xp > 1e-9, np.clip(x[m.S[n]], 0, None) / safe, 0.0),
                    "red_rel": np.where(xp > 1e-9, np.clip(x[m.R[n]], 0, None) / safe, 0.0),
                    "add_pct": np.clip(x[m.A[n]], 0, None) * V[n] / W,
                    "tpl_pct": np.where(is_commit, 0.0, np.clip(x[m.Y[n]], 0, None) / W),
                    "mult": np.where(is_commit, x[m.Y[n]] / np.maximum(plan, 1e-12), 0.0),
                    "fin_ratio": np.clip(ratio, 0, None), "p2s_pct": float(x[m.PI[n]] / W),
                    "beta_pct": float(x[m.BETA[n]] / W), "trs_pct": np.clip(x[m.TRS[n]], 0, None) / W,
                    "hed_pct": float(x[m.HED[n]] / W), "opp": float(x[m.OPP[n]])}
    stage1 = [int(n) for n in range(1, ND) if m.lvl[n] == 1]
    children = {int(n): [int(c) for c in D["tr"]["children"][n]] for n in stage1}
    return {"kind": "plan", "root": root, "nodes": nodes, "stage1": stage1, "children": children,
            "feat_mu": mu, "feat_sd": sd, "restore8": True,
            "playbook_years": (1,) if getattr(m, "rec2", False) else (1, 2)}


def r1_labels(m: MPOModel, x: np.ndarray) -> list:
    """Per decision node: net new financing dB (total B incl. embedded futures/TRS financing net of margin) split by
    R1 into LEVER (funds discretionary new exposure) and REFINANCE (cash raised against holdings)."""
    D = m.D
    V = D["V"]
    out = []
    pur = ~D["tpl_is_commit"]
    for n in range(m.ND):
        p = m.par[n]
        fin_now = float(x[m.FB[n]].sum())
        fin_prev = float(x[m.FB[p]].sum()) if p >= 0 else 0.0
        if p >= 0:
            fin_prev *= 1.0
        syn_now = float(x[m.BETA[n]] + x[m.PI[n]] + x[m.TRS[n]].sum() - x[m.IM[n]] + x[m.OPP[n]])
        syn_prev = (float(x[m.BETA[p]] + x[m.PI[p]] + x[m.TRS[p]].sum() - x[m.IM[p]] + x[m.OPP[p]]) if p >= 0
                    else float(m.P.get("overlay.beta_sq")))
        tdebt_new = float((x[m.Y[n]] * D["tpl_debt"]).sum())
        dB = (fin_now - fin_prev) + (syn_now - syn_prev) + tdebt_new
        adds = float((x[m.A[n]] * V[n]).sum()) + float((x[m.Y[n]][pur] * D["tpl_init"]["V"][n][pur]).sum())
        syn_add = float(x[m.BETA[n]] + x[m.TRS[n]].sum()) - (float(x[m.BETA[p]] + x[m.TRS[p]].sum()) if p >= 0
                                                           else float(m.P.get("overlay.beta_sq")))
        sales = float((x[m.S[n]] * V[n]).sum())
        dE = adds + syn_add - sales
        lever = min(max(dB, 0.0), max(dE, 0.0))
        out.append({"node": int(n), "level": int(m.lvl[n]), "dB_bn": dB, "dE_disc_bn": dE, "LEVER_bn": lever,
                    "REFINANCE_bn": max(dB, 0.0) - lever})
    return out


def liquidity_premia(m: MPOModel, y: np.ndarray) -> np.ndarray:
    """ell_n = lambda_n / (e^rf sum_c lambda_c) - 1 from the cash-row duals (one-year liquidity premium)."""
    lam = y[m.rows["cash"]]
    erf = np.exp(m.D["rf"])
    ell = np.full(m.T, np.nan)
    for n in range(m.ND):
        ch = m.D["tr"]["children"][n]
        den = erf * lam[ch].sum()
        if abs(den) > 1e-14:
            ell[n] = lam[n] / den - 1.0
    return ell


def cards(m: MPOModel, x: np.ndarray, y: np.ndarray, beliefs: list, book: dict, Ef: np.ndarray,
          rc: np.ndarray | None = None) -> list:
    """One card per holding at the root, read from the LP's duals. The hold value of holding i is the marginal value
    of one more unit of it held: nu_i (dual of its balance row) plus the reduced cost of x_i (non-zero when x_i sits
    at a bound, e.g. a private holding that cannot be added to), so p*_i = (nu_i + rc_xi) / (lambda_0 N_i)."""
    D, P = m.D, m.P
    rf = D["rf"]
    V, Nr = D["V"], D["N"]
    lam0 = y[m.rows["cash"][0]]
    ell = liquidity_premia(m, y)
    ell0 = float(ell[0])
    ell_bar = float(np.nanmean([ell[n] for n in range(1, 11)]) * 0.5 + ell0 * 0.5)
    out = []
    for i, u in enumerate(D["units"]):
        b = beliefs[i]
        nu = y[m.rows["xbal"][0, i]] + (rc[m.X[0, i]] if rc is not None else 0.0)
        pstar = float(nu / (lam0 * Nr[0, i])) if abs(lam0) > 1e-14 else np.nan
        theta = float(V[0, i] / Nr[0, i])
        pce = float(D["proc"][0, i] / Nr[0, i])
        Dd = max(u["D"], 0.5)
        h_goal = float(b["mu_hat"] - np.log(max(pstar, 1e-9) / theta) / Dd) if pstar > 0 else np.nan
        mu_be = float(h_goal + np.log(pce / theta) / Dd) if np.isfinite(h_goal) else np.nan
        rp = float(np.asarray(u["B"]) @ Ef)
        h_util = rf + rp + max(ell_bar, 0.0)
        s0, a0, r0 = float(x[m.S[0, i]]), float(x[m.A[0, i]]), float(x[m.R[0, i]])
        su = float(m._cur_ub[m.S[0, i]])
        act = "SELL" if s0 > 1e-6 else "REDEEM" if r0 > 1e-6 else "ADD" if a0 > 1e-6 else "HOLD"
        admissible_sell = su > 1e-12
        # A23: card-LP sign consistency (sell iff bid >= reservation, unless a cap binds or the column is held at 0)
        tol = 2e-3
        at_cap = s0 >= su - 1e-7 if admissible_sell else False
        if not admissible_sell:
            ok = True
        elif s0 > 1e-6:
            ok = pce >= pstar - tol or at_cap
        else:
            ok = pce <= pstar + tol
        out.append({"unit_id": u["id"], "group": u["group"], "segment": u["segment"], "name": u["name"],
                    "tier": u["tier"], "action": act, "sell_frac": s0, "redeem_frac": r0, "add_frac": a0,
                    "size_bn": float((s0 + r0) * V[0, i] if act in ("SELL", "REDEEM") else a0 * V[0, i]),
                    "p_ce": pce, "p_star": pstar, "theta": theta, "mu_hat": float(b["mu_hat"]),
                    "mu_p10": float(b["p10"]), "mu_p90": float(b["p90"]), "hurdle_goal": h_goal,
                    "hurdle_utility": h_util, "mu_be": mu_be, "ell_root": ell0, "duration_y": Dd,
                    "goal_driven": bool(np.isfinite(h_goal) and b["mu_hat"] >= h_goal and b["mu_hat"] < h_util
                                        and act in ("HOLD", "ADD")),
                    "red_event_if_sold_today": u["tier"] == "red", "sell_admissible": admissible_sell,
                    "a23_ok": bool(ok)})
    return out


def change_list(m: MPOModel, x: np.ndarray, y: np.ndarray, cardl: list, lens_root: dict) -> list:
    """Root actions with a nonzero size: per holding, templates, financing, overlay, pacing."""
    D, P = m.D, m.P
    rows = []
    phi_hf = P.get("trading.redeem_phi")["hf"]
    phi_re = P.get("trading.redeem_phi")["re_open_end"]
    for c in cardl:
        if c["action"] != "HOLD" and c["size_bn"] > 1e-4:
            lens = {"SELL": "SELL", "REDEEM": "REDEEM", "ADD": "ADD"}[c["action"]]
            phi = phi_hf if c["group"] == "HF" else phi_re
            rows.append({"unit_id": c["unit_id"], "group": c["group"], "action": c["action"].lower(), "lens": lens,
                         "family": lens, "size_bn": c["size_bn"],
                         "size_pct": 100 * (c["sell_frac"] + c["redeem_frac"] + c["add_frac"]),
                         "p_ce": c["p_ce"], "p_star": c["p_star"], "mu_hat": [c["mu_p10"], c["mu_hat"], c["mu_p90"]],
                         "hurdle_goal": c["hurdle_goal"], "hurdle_utility": c["hurdle_utility"], "mu_be": c["mu_be"],
                         "ell_root": c["ell_root"], "red_event": False, "goal_driven": c["goal_driven"],
                         "consent": "GP transfer consent" if c["tier"] == "red" else "none",
                         "lag_q": 4 if c["action"] == "REDEEM" else 0, "name": c["name"],
                         "redeem_phi": "/".join(f"{v:.2f}" for v in phi) if c["action"] == "REDEEM" else None})
    plan = np.array([t.get("plan", 0.0) for t in D["tpl"]])
    cpace = P.get("pacing.c_pace")
    psi = P.get("valuation.psi_unfunded")
    astar = P.get("fusion.alpha_star_pp")
    c0 = int(m.cls[0])
    for k, nm in enumerate(D["tpl_names"]):
        v = float(x[m.Y[0, k]])
        t = D["tpl"][k]
        if t["kind"] == "commit":
            if abs(v - plan[k]) > 1e-4:
                rows.append({"unit_id": nm, "group": t["group"], "action": "pace", "lens": "PACE", "family": "PACE",
                             "size_bn": v - plan[k], "size_pct": 100 * (v / plan[k] - 1), "note":
                             f"commitments {v:.2f} vs plan {plan[k]:.2f} $bn/yr; alpha prior {astar[t['group']]:+.2f}pp, "
                             f"post-horizon value {100 * cpace[t['group']]:.1f}c per $ vs leaf unfunded charge "
                             f"{100 * psi:.0f}c; cuts also free stressed-call margin (H9/H15)"})
        elif v > 1e-4:
            lens = "LEVER" if t["family"] == "LEVER" else "ADD"
            rows.append({"unit_id": nm, "group": t["group"], "action": "buy", "lens": lens, "family": t["family"],
                         "size_bn": v, "size_pct": None,
                         "note": f"{nm} template ($ of equity): alpha {t['alpha_pp'][c0]:+.2f}pp a year in today's class"
                                 + (f", asset debt {t['lever_debt']:.1f} per $" if t["lever_debt"] else "")})
    for j, f in enumerate(FIN):
        v = float(x[m.FB[0, j]])
        if v > 1e-4:
            rows.append({"unit_id": f, "group": "CF" if f in ("REV", "TERM", "NAVF", "PREF") else
                         {"CSBL": "CS", "SMABL": "PC", "RACO": "RA"}[f], "action": "borrow",
                         "lens": "LEVER" if lens_root["LEVER_bn"] >= v - 1e-6 else "REFINANCE",
                         "family": FIN_FAMILY[f], "size_bn": v, "size_pct": None,
                         "note": f"R1 at the root: LEVER {lens_root['LEVER_bn']:.2f} / REFINANCE "
                                 f"{lens_root['REFINANCE_bn']:.2f} $bn of {lens_root['dB_bn']:.2f} net new financing"})
    ov = lambda k: P.get(f"overlay.{k}")
    b = float(x[m.BETA[0]])
    if abs(b - ov("beta_sq")) > 1e-3:
        rows.append({"unit_id": "SYNTH_BETA", "group": "OV", "action": "resize", "lens": "LEVER", "family": "BETA",
                     "size_bn": b - ov("beta_sq"), "size_pct": 100 * (b / ov("beta_sq") - 1),
                     "note": f"synthetic beta {b:.2f} vs {ov('beta_sq'):.1f} $bn (risk budget, never alpha)"})
    if float(x[m.PI[0]]) > 1e-3:
        rows.append({"unit_id": "P2S", "group": "LO", "action": "convert", "lens": "REFINANCE", "family": "REFINANCE",
                     "size_bn": float(x[m.PI[0]]), "size_pct": None, "note": "physical DM core to futures"})
    for h, iu in enumerate(m.hf_units):
        v = float(x[m.TRS[0, h]])
        if v > 1e-3:
            rows.append({"unit_id": f"TRS:{D['ids'][iu]}", "group": "HF", "action": "trs", "lens": "LEVER",
                         "family": "LEVER", "size_bn": v, "size_pct": None, "note": "hedge-fund TRS (portable alpha)"})
    hmin = P.get("overlay.tail_budget")[0] / ov("tail_premium")
    hv = float(x[m.HED[0]])
    rows.append({"unit_id": "TAIL_LADDER", "group": "OV", "action": "size", "lens": "HEDGE", "family": "HEDGE",
                 "size_bn": hv, "size_pct": None,
                 "note": f"notional {hv:.2f} $bn (floor {hmin * float(x[m.W[0]]):.2f}); premium {hv * ov('tail_premium'):.3f} $bn/yr"})
    o = float(x[m.OPP[0]])
    if abs(o - ov("opp_im_sq")) > 1e-3:
        rows.append({"unit_id": "OPPORTUNISTIC", "group": "OV", "action": "resize", "lens": "HEDGE", "family": "HEDGE",
                     "size_bn": o - ov("opp_im_sq"), "size_pct": None, "note": f"IM {o:.2f} vs {ov('opp_im_sq'):.1f} $bn"})
    lu = float(x[m.LUP[0]])
    if lu > 1e-3:
        rows.append({"unit_id": "REVOLVER_UPSIZE", "group": "CF", "action": "arrange", "lens": "FUND", "family": "FUND",
                     "size_bn": lu, "size_pct": None, "note": "effective from year 1 (2-quarter lead)"})
    return rows
