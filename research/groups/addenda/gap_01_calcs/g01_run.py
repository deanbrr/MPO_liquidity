"""
Group gap_01 driver: re-based group tables under T4' = s*(0.76), group RECOVERY (Phase I / II), t0 envelope /
charge / hurdle table with SAA ranges. SYNTHETIC - NOT ADIC DATA.
Run: <venv>/python.exe g01_run.py   (writes g01_results.json next to this file; ~5 minutes)
"""
from __future__ import annotations

import json
import os
import time

import numpy as np

import g01_core as G
from g01_core import E, s_star, t4_literal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "g01_results.json")
THETA = 0.76
N_MC = 50000
SAA_SEEDS = [20261018 + 101 * i for i in range(10)]
LIQ_BOOK = 71.0
T_REC = 4            # quarters (gap_02 default)
RCF_LEAD_Q = 2       # quarters to sign a syndicated revolver [I]


def flows_table(r: dict) -> dict:
    out = {}
    for g in G.PRIV:
        d12, c12 = r["gf"][g]["dist"][:12].sum(), r["gf"][g]["calls"][:12].sum()
        d24, c24 = r["gf"][g]["dist"][:24].sum(), r["gf"][g]["calls"][:24].sum()
        out[g] = dict(dist12=d12, calls12=c12, net12=d12 - c12, dist24=d24, calls24=c24, net24=d24 - c24)
    ov = r["ovl"]
    ovl12 = float((ov["vm"] - ov["dim"] + ov["tail"] - ov["prem"] - ov["opp"] - ov["fut"])[:12].sum())
    ovl24 = float((ov["vm"] - ov["dim"] + ov["tail"] - ov["prem"] - ov["opp"] - ov["fut"])[:24].sum())
    priv12 = sum(v["net12"] for v in out.values())
    opex12 = float(r["cf"]["opex"][:12].sum())
    before = priv12 + ovl12 - opex12
    draw12 = float(r["cf"]["draw"][:12].sum())
    return dict(groups=out, private12=dict(dist=sum(v["dist12"] for v in out.values()),
                                           calls=sum(v["calls12"] for v in out.values()), net=priv12),
                overlay12=ovl12, overlay24=ovl24,
                overlay_parts12={k: float(v[:12].sum()) for k, v in ov.items()}, opex12=opex12,
                before_payout12=before, draw12_canonical=draw12,
                liquid_funding={"canonical (10% opening NAV)": draw12 - before,
                                **{f"{p:.1%}": p * E.NAV0 - before for p in (0.05, 0.075, 0.10)}},
                liquid_share={"canonical": (draw12 - before) / LIQ_BOOK,
                              **{f"{p:.1%}": (p * E.NAV0 - before) / LIQ_BOOK for p in (0.05, 0.075, 0.10)}})


def ladder_row(s, lev):
    r = G.gl_ladder(s, lev)
    return dict(SH_TP=r["SH_TP"], SH_TPF=r["SH_TPF"], min_head_24=r["min_head_tpf_24"], argmin=r["argmin_24"],
                fac_need_24=r["fac_need_24"], gstar=r["gstar"], cbc12=float(r["cbc"][11]), cbc24=float(r["cbc"][23]),
                nco12=float(r["nco"][11]), nco24=float(r["nco"][23]))


def lar99_by_model(n=N_MC):
    """12-month LaR99: P99 of the 4-quarter net need before management actions (gap_02 engine, Policy A)."""
    keep = E.T_Q
    E.T_Q = 4
    out = {}
    try:
        for mk, m in E.MODELS.items():
            r = E.simulate(m, E.Policy("A"), n=n)
            out[mk] = dict(lar95=r["netneed8_q"][1], lar99=r["netneed8_q"][2], p50=r["netneed8_q"][0])
    finally:
        E.T_Q = keep
    return out


def theta_from_gstar(target: float) -> float:
    thetas = np.linspace(0, 1.2, 121)
    g = [E.ladder(s_star(th), E.Policy("A"))["gstar"] for th in thetas]
    return float(np.interp(target, g, thetas))


def solve_states(s, states=("R0x", "R0", "R1", "R2"), role="pricing"):
    coef = G.coefficients_for(s, role=role)
    d0 = float(max(0.0, -coef["h0"].min()))
    res = {"h0_min": float(coef["h0"].min()), "d0": d0, "states": {}}
    for st in states:
        rr = G.restore_and_solve(coef, st)
        p1, h = rr["phase1"], rr["restored"]
        el = G.solve(coef, st, elastic=True)
        priced_on = "restored_problem" if (p1["u_S_star"] > 1e-9 or d0 > 1e-9) else "original_problem"
        hsh = G.recovery_hash(s.name, h) if priced_on == "restored_problem" else None
        gp = G.group_prices(coef, h, priced_on, hsh, d0) if role == "pricing" else None
        res["states"][st] = dict(
            label=G.STATES[st]["label"], u_star=p1["u_S_star"], u_IG_star=p1["u_IG_star"], iis=p1["iis"],
            phase1_levers=p1["levers"], x=h["x"], sell=h["sell"], mu_sum=float(h["mu"].sum()),
            mu_months=[int(i + 1) for i in np.where(h["mu"] > 1e-9)[0]], y_IG=h["y_IG"], y_cash=h["y_cash"],
            mu_sum_x10=float(rr["restored_elastic_x10"]["mu"].sum()), cards=h["cards"],
            elastic_original=dict(u_S=el["u_S"], mu_sum=float(el["mu"].sum()), pinned=G.pinned_rows(el),
                                  cards=el["cards"]),
            prices=gp, cost_5y=-h["obj"])
    lev_tab = {k: dict(owner=G.GROUP_NAME[v["owner"]], cap=v["cap"], cost=v["cost"], slope24=float(v["slope"][23]),
                       cost_per_relief=(v["cost"] / v["slope"][23]) if v["slope"][23] > 1e-9 else None,
                       ig=v["ig"], unit=v["unit"], note=v["note"])
               for k, v in coef["lever"].items()}
    res["levers"] = lev_tab
    res["cash_slope24"] = float(coef["cash"][23])
    res["commit_slope24"] = {g: float(v[23]) for g, v in coef["commit"].items()}
    return res, coef


def interim_path(coef, d0):
    """Glide path g_t = d0 (1 - t/T_rec)^+; before the revolver signs, the execution gap d0 - g_t is closed with
    reversible group levers only (state I); afterwards by the revolver (state R1 terminal plan)."""
    path = []
    for t in range(T_REC + 1):
        g_t = d0 * max(0.0, 1 - t / T_REC)
        need = d0 - g_t
        if t < RCF_LEAD_Q:
            st = "I"
            sol = G.solve(coef, st, elastic=False, relax=(g_t, 0.0))
            x = {k: v for k, v in sol["x"].items() if v > 1e-6}
            rel = {}
            for k, v in sol["x"].items():
                o = coef["lever"][k]["owner"]
                rel[o] = rel.get(o, 0.0) + float(coef["lever"][k]["slope"][23] * v)
            tot = sum(max(0, v) for v in rel.values())
            share = {G.GROUP_NAME[o]: max(0, v) / tot for o, v in rel.items() if tot > 1e-9 and v > 1e-9}
            path.append(dict(t=t, g_t=g_t, need=need, state=st, mu_interim=float(sol["mu"].sum()), x=x,
                             relief_by_owner={G.GROUP_NAME[o]: v for o, v in rel.items() if abs(v) > 1e-9},
                             share=share))
        else:
            path.append(dict(t=t, g_t=g_t, need=need, state="R1 (revolver signed)",
                             note="terminal plan: revolver carries the deficit; interim group levers released"))
    return path


def main():
    t0 = time.time()
    res = {"note": "SYNTHETIC / ILLUSTRATIVE - not ADIC data. Engine: gap_02 t1_engine via a group-resolved replica.",
           "theta_star": THETA}
    s = s_star(THETA)
    base = G.lev_of(reserve=0.08)                       # gap_02 canonical do-nothing (8% top-up at t0)
    r0 = G.gl_ladder(s, base)
    res["s22_column"] = flows_table(r0)
    res["s22_census_v1"] = ladder_row(s, G.lev_of(reserve=0.08, census="v1"))
    t4 = t4_literal()
    res["s22_T4_literal_reverse"] = flows_table(G.gl_ladder(t4, base))

    pol = lambda **kw: G.lev_from_policy(E.Policy("x", **kw))
    configs = {
        "do-nothing": base,
        "stage pacing rule": pol(pace_cut=True),
        "owner band": pol(band=True),
        "rule + band": pol(pace_cut=True, band=True),
        "revolver 13.9": G.lev_of(reserve=0.08, rcf=13.9),
        "revolver 6.1 + rule": pol(pace_cut=True, rcf=6.1),
        "Mix A (rcf 15, pace 6 + rule, reserve 14%)": pol(rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
        "Mix B (rcf 10, rule, band, reserve 8%)": pol(rcf=10.0, pace_cut=True, band=True, reserve=0.08),
        "NAV facility 2.12 (10% LTV on 21.2 pool)": G.lev_of(reserve=0.08, navf=2.12),
    }
    res["s24_ladder"] = {k: ladder_row(s, v) for k, v in configs.items()}
    res["s24_reverse"] = {"T4 literal canonical, do-nothing": ladder_row(t4, base),
                          "T4 literal canonical, Mix A": ladder_row(t4, configs["Mix A (rcf 15, pace 6 + rule, reserve 14%)"]),
                          "T4 as written (8% floor)": ladder_row(t4_literal(floor=0.08), base),
                          "critic reading": ladder_row(t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0,
                                                                  pc_cs_rates=(0.0, 0.0)), base)}
    print(f"[{time.time() - t0:.0f}s] tables done")

    # ---------------- CFP indicators at t0
    lar = lar99_by_model()
    mix_lar99 = float(np.mean([v["lar99"] for v in lar.values()]))
    usable_pre = E.TRE0 - E.IM_N * E.N_SYN0 - E.OPP_IM0
    res["cfp"] = dict(
        SH_TP={"do-nothing": r0["SH_TP"], "stage rule adopted": res["s24_ladder"]["stage pacing rule"]["SH_TP"],
               "band agreed": res["s24_ladder"]["owner band"]["SH_TP"],
               "census v1 split": res["s22_census_v1"]["SH_TP"]},
        lcr30_gc2=2.10, lcr30_gap02_engine=__import__("gap02_study").lcr30_t0(E.Policy("A")),
        treasury_share={"before 8% top-up": usable_pre / E.NAV0, "after top-up": 0.08},
        liquid_share=(usable_pre + sum(E.LO0.values()) + E.HF_CASH90 * E.HF0) / E.NAV0,
        lar_by_model=lar, lar99_mean_of_models=mix_lar99, lar99_worst=max(v["lar99"] for v in lar.values()),
        cbc_tp12=float(r0["cbc"][11]),
        lar99_over_cbc={"mean of models": mix_lar99 / float(r0["cbc"][11]),
                        "worst model": max(v["lar99"] for v in lar.values()) / float(r0["cbc"][11])})
    print(f"[{time.time() - t0:.0f}s] CFP done")

    # ---------------- L4 pools
    def pools(lev):
        r = G.gl_ladder(s, lev)
        out = {}
        for h in (12, 24):
            i = h - 1
            out[f"{h}m"] = dict(cbc_tp=float(r["cbc"][i]), fac=float(r["fac"][i] + r["navf"][i]),
                                draw=float(r["cf"]["draw"][:h].sum()), opex=float(r["cf"]["opex"][:h].sum()),
                                fees=float(r["cf"]["fee"][:h].sum()), floor=float(r["floor"][i]),
                                pool_tpf=float(r["cbc"][i] + r["fac"][i] + r["navf"][i] - r["cf"]["draw"][:h].sum()
                                               - r["cf"]["opex"][:h].sum() - r["cf"]["fee"][:h].sum() - r["floor"][i]),
                                head_tpf=float(r["head_tpf"][i]))
        return out
    res["L4_pools"] = {"do-nothing": pools(base), "revolver 14.2": pools(G.lev_of(reserve=0.08, rcf=14.2))}

    def budgets(lev):
        r = G.gl_ladder(s, lev)
        ov = r["ovl"]
        use = (-ov["vm"] + ov["dim"] - ov["tail"] + ov["prem"] + ov["opp"] + ov["fut"])
        out = {g: dict(B12=float(np.sum(r["gf"][g]["calls"][:12] - r["gf"][g]["dist"][:12])),
                       B24=float(np.sum(r["gf"][g]["calls"][:24] - r["gf"][g]["dist"][:24]))) for g in G.PRIV}
        out["ovl"] = dict(B12=float(use[:12].sum()), B24=float(use[:24].sum()))
        p = pools(lev)
        out["pool"] = {h: p[h]["pool_tpf"] for h in p}
        out["slack"] = {h: p[h]["head_tpf"] for h in p}
        return out
    res["L4_budgets"] = {
        "do-nothing": budgets(base),
        "R1 plan (revolver 13.6 + SMA sale 0.58)": budgets(G.lev_of(rcf=13.64, sma_sell=0.58)),
        "Mix A (rcf 15, pace 6 + rule, reserve 14%)": budgets(configs["Mix A (rcf 15, pace 6 + rule, reserve 14%)"]),
        "Mix B (rcf 10, rule, band, reserve 8%)": budgets(configs["Mix B (rcf 10, rule, band, reserve 8%)"]),
        "Mix A without revolver": budgets(pol(pace=6.0, pace_cut=True, reserve=0.14)),
    }

    # ---------------- Phase I / II by state
    main_res, coef = solve_states(s)
    res["recovery_T4prime"] = main_res
    res["interim_glide_path"] = interim_path(coef, main_res["d0"])
    rev = {}
    for name, st in (("T4 literal canonical", t4),
                     ("critic reading", t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0,
                                                    pc_cs_rates=(0.0, 0.0)))):
        rr, _ = solve_states(st, role="reverse")
        rev[name] = {k: dict(u_star=v["u_star"], iis=v["iis"], mu_sum=v["mu_sum"],
                             elastic_mu_sum=v["elastic_original"]["mu_sum"],
                             elastic_pinned=v["elastic_original"]["pinned"],
                             elastic_cards=[(c["card"], c["reservation_price"], c["action"])
                                            for c in v["elastic_original"]["cards"]],
                             restored_cards=[(c["card"], c["reservation_price"], c["action"]) for c in v["cards"]])
                     for k, v in rr["states"].items()}
    res["recovery_reverse"] = rev
    print(f"[{time.time() - t0:.0f}s] recovery done")

    # ---------------- SAA replications of theta* (worst model M6, 50k paths each)
    eps24 = 1 - (1 - 0.01) ** (8 / 20)
    saa = []
    pooled = []
    for seed in SAA_SEEDS:
        r = E.simulate(E.MODELS["M6"], E.Policy("A"), n=N_MC, seed=seed, return_paths=True)
        pooled.append(r["_gstar"])
        gq = float(np.quantile(r["_gstar"], 1 - eps24))
        th = theta_from_gstar(gq)
        rr, _ = solve_states(s_star(th), states=("R0", "R1"))
        row = dict(seed=seed, gstar_q=gq, theta=th, fac_need=E.ladder(s_star(th), E.Policy("A"))["fac_need_24"])
        for st in ("R0", "R1"):
            v = rr["states"][st]
            row[st] = dict(u_star=v["u_star"], mu_sum=v["mu_sum"], y_IG=v["y_IG"], y_cash=v["y_cash"],
                           groups={g: {k: v["prices"]["groups"][g].get(k) for k in
                                       ("envelope_12m", "envelope_24m", "pacing_bn_yr", "ftp_new_bp_yr",
                                        "hurdle_bp_yr", "ftp_hold_bp_yr")} for g in G.PRIV},
                           cards=[(c["card"], c["reservation_price"], c["action"]) for c in v["cards"]],
                           x={k: x for k, x in v["x"].items() if x > 1e-6})
        saa.append(row)
        print(f"[{time.time() - t0:.0f}s] SAA seed {seed}: G*q={gq:.2f} theta={th:.3f}")
    res["saa"] = saa
    th = np.array([r["theta"] for r in saa])
    gq_pool = float(np.quantile(np.concatenate(pooled), 1 - eps24))
    th_pool = theta_from_gstar(gq_pool)
    res["saa_pooled"] = dict(n_paths=N_MC * len(SAA_SEEDS), gstar_q=gq_pool, theta=th_pool,
                             fac_need=E.ladder(s_star(th_pool), E.Policy("A"))["fac_need_24"])
    res["saa_summary"] = dict(theta_min=float(th.min()), theta_median=float(np.median(th)), theta_max=float(th.max()),
                              gstar_q=[r["gstar_q"] for r in saa], fac_need=[r["fac_need"] for r in saa],
                              rcf_R1=[r["R1"]["x"].get("rcf", 0.0) for r in saa])
    # revolver-cap threshold: R1 dual as theta rises
    cap_scan = {}
    for thv in (0.79, 0.81, 0.82, 0.85, 0.90):
        rr, _ = solve_states(s_star(thv), states=("R1",))
        v = rr["states"]["R1"]
        cap_scan[f"{thv:.2f}"] = dict(mu_sum=v["mu_sum"], x={k: x for k, x in v["x"].items() if x > 1e-6},
                                      cards=[(c["card"], c["reservation_price"], c["action"]) for c in v["cards"]])
    res["revolver_cap_scan"] = cap_scan

    # ---------------- NAV facility vs pledge cap
    pool = min(0.20 * sum(E.PRIV0.values()), E.PRIV0["pe"] + E.PRIV0["sec"])
    nav_rel = ladder_row(s, G.lev_of(reserve=0.08, navf=0.10 * pool))["min_head_24"] - ladder_row(s, base)["min_head_24"]
    navf_cost_per_committed = 0.005 * 5 + 0.010                  # undrawn 50bp/yr x 5y + 1% upfront [t1_engine]
    res["nav_facility_check"] = dict(
        pledge_pool=pool, capacity_10pct=0.10 * pool, capacity_5pct=0.05 * pool, s_star_relief=nav_rel,
        share_of_need=[0.05 * pool / 13.9, 0.10 * pool / 13.9],
        cost_per_credited_dollar=navf_cost_per_committed / 0.5,     # sized at 10% LTV, credited at 5% stressed LTV
        revolver_cost_per_credited_dollar=0.009 / 0.80)             # gap_02: 15bp undrawn x 5y + 15bp upfront
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
    print(f"[{time.time() - t0:.0f}s] wrote {OUT}")


if __name__ == "__main__":
    main()
