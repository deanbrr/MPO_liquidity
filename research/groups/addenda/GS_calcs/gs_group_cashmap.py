"""
Group cash-generation map for 01_GROUPS_SYNTHESIS.md (ALL SYNTHETIC / ILLUSTRATIVE, never ADIC data).

What it does
  Re-uses the unmodified stream-G7 ladder module (loaded from ../G7_calcs/, as GC2 does) to produce
  12-month sources and uses BY GROUP in four states:
    normal  : benign market path (G7 B0), exit regime "normal" throughout
    drought : G7 B0_drought (today's state)
    S1      : G7 S1 demand bust (crisis 18m, calls x1.25 for 12m, cap draws)
    T14     : C1 T1.4-aligned vertex as built by GC2 (S1 market path; PE, Secondaries and Co-investment
              distributions = 0; calls x1.5 for 24m; cap draws)
  under two configurations:
    g7      : G7's own unfunded split and distribution rates (reproduces gap_01's group table exactly)
    census  : GC2/GC1 census v1.0 unfunded split (PE 27.4, Sec 3.5 + 0.4 deferred, Co 1.5, CapSol 1.2,
              PC 3.0 + 1.0 DDTL/revolver) and GC1's production co-investment distribution yields
              (19.3% normal, 12.4% drought; G4 engine via GC1 §1 item 3)
  plus a PE drought-rate sensitivity at MSCI's H1-2026 9% (vs G7's 11%).

Overlay and Corporate Finance flows (VM on synthetic beta, IM change, tail premium and monetisation,
opportunistic loss, opex) are reported separately; the owner payout is shown at 5 / 7.5 / 10% of $177bn.

Run:  <venv>/python.exe -I gs_group_cashmap.py   (writes gs_group_cashmap_results.json next to this file)
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_G7_PATH = os.path.normpath(os.path.join(HERE, "..", "G7_calcs", "g7_liquidity_ladder_calcs.py"))
_spec = importlib.util.spec_from_file_location("g7mod", _G7_PATH)
g = importlib.util.module_from_spec(_spec)
sys.modules["g7mod"] = g
_spec.loader.exec_module(g)  # unmodified

OUT = os.path.join(HERE, "gs_group_cashmap_results.json")

UNF_CENSUS = {"pe": 27.4, "sec_def": 0.4, "sec": 3.5, "pc_rev": 1.0, "pc": 3.0, "cs": 1.2, "co": 1.5}
assert abs(sum(UNF_CENSUS.values()) - 38.0) < 1e-9


def dist_table(config: str, pe_drought: float | None = None) -> dict:
    d = {r: dict(v) for r, v in g.DIST.items()}
    if config == "census":
        d["normal"]["co"] = 0.193
        d["drought"]["co"] = 0.124
    if pe_drought is not None:
        d["drought"]["pe"] = pe_drought
    return d


def paths(scn: str, T: int = 36) -> dict:
    if scn in ("normal", "drought"):
        p = g.build_paths("B0_drought", T)
        if scn == "normal":
            p["regime"] = ["normal"] * T
    else:
        p = g.build_paths("S1_demand_bust_24m", T)
    p["dist_zero"] = np.zeros(T, dtype=bool)
    if scn == "T14":  # GC2's T1.4-aligned construction
        p["call_mult"] = np.ones(T)
        p["call_mult"][:24] = 1.5
        p["draw_rate"] = np.full(T, 0.075)
        p["draw_rate"][:24] = 0.10
        p["dist_zero"][:24] = True
    return p


def run(scn: str, unf0: dict, rates: dict, T: int = 12) -> dict:
    p = paths(scn, 36)
    bal = dict(g.BAL0)
    unf = dict(unf0)
    eq_idx = 1.0
    im = g.IM_RATE_N * g.SYN_NOTIONAL
    acc = {k: 0.0 for k in ("vm", "d_im", "hedge", "opp", "opex", "draw_at_path_rate")}
    dist_g = {k: 0.0 for k in g.PRIVATE}
    calls_g = {k: 0.0 for k in g.PRIVATE}
    for t in range(T):
        reg = p["regime"][t]
        stress = reg == "crisis"
        for k, f in (("lo_dm", p["eq"][t]), ("lo_em", 1.2 * p["eq"][t]), ("lo_fi", p["fi"][t]),
                     ("ig", p["ig"][t]), ("ust", p["ust"][t]), ("cash", 0.039 / 12)):
            bal[k] *= 1 + f
        for k in g.HF_SHARES:
            bal[k] *= 1 + p["hf"][t]
        for gg in g.PRIVATE:
            bal[gg] *= 1 + p["priv_mark"][t]
        vm = g.SYN_NOTIONAL * eq_idx * p["eq"][t]
        eq_idx *= 1 + p["eq"][t]
        im_new = (g.IM_RATE_S if (stress and t < 12) else g.IM_RATE_N) * g.SYN_NOTIONAL * eq_idx
        d_im = im_new - im
        im = im_new
        hedge_cf = -g.HEDGE_PREMIUM_PA / 12
        if t in p["hedge_months"]:
            hedge_cf += 0.5 * g.HEDGE_NOTIONAL * min(0.20, max(0.0, 0.90 - eq_idx))
        opp = -p["opp_loss"][t]
        dist = {}
        for gg in g.PRIVATE:
            rate = rates[reg][gg]
            if p["dist_zero"][t] and gg in ("pe", "sec", "co"):
                rate = 0.0
            dist[gg] = g.monthly_rate(rate) * bal[gg]
        crate = g.monthly_rate(min(0.95, g.CALL[reg] * p["call_mult"][t]))
        calls = {k: crate * unf[k] for k in ("pe", "sec", "pc", "cs", "co")}
        calls["sec_def"] = (unf0["sec_def"] / 4.0) if t in (2, 5, 8, 11) else 0.0
        spike = p["rev_draw"][t] * unf0["pc_rev"]
        calls["pc_rev"] = min(unf["pc_rev"], spike if spike > 0 else crate * unf["pc_rev"])
        nc = g.NEW_COMMIT_PA / 12.0
        for k, v in calls.items():
            unf[k] -= v
        for k, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1), ("co", 0.1)):
            unf[k] += w * nc
        for gg in g.PRIVATE:
            add = calls[gg] + (calls["sec_def"] if gg == "sec" else 0.0) + (calls["pc_rev"] if gg == "pc" else 0.0)
            bal[gg] += add - dist[gg]
            calls_g[gg] += add
            dist_g[gg] += dist[gg]
        acc["vm"] += vm
        acc["d_im"] += d_im
        acc["hedge"] += hedge_cf
        acc["opp"] += opp
        acc["opex"] += 0.001 * g.NAV0 / 12.0
        acc["draw_at_path_rate"] += p["draw_rate"][t] * g.NAV0 / 12.0
    net_g = {k: dist_g[k] - calls_g[k] for k in g.PRIVATE}
    priv_net = sum(net_g.values())
    overlay_net = acc["vm"] - acc["d_im"] + acc["hedge"] + acc["opp"]
    before_payout = priv_net + overlay_net - acc["opex"]
    payout = {"5%": 0.05 * g.NAV0, "7.5%": 0.075 * g.NAV0, "10%": 0.10 * g.NAV0}
    liquid_funding = {k: v - before_payout for k, v in payout.items()}
    liquid_book0 = sum(g.BAL0[k] for k in g.LIQ_KEYS) + g.HF_TOTAL
    return dict(
        scenario=scn,
        dist_by_group=dist_g, calls_by_group=calls_g, net_by_group=net_g,
        private_dist=sum(dist_g.values()), private_calls=sum(calls_g.values()), private_net=priv_net,
        overlay=dict(vm=acc["vm"], d_im=acc["d_im"], tail_premium_and_monetisation=acc["hedge"],
                     opportunistic=acc["opp"], net=overlay_net),
        cf_opex=acc["opex"], before_payout=before_payout,
        draw_at_path_rate=acc["draw_at_path_rate"],
        liquid_book_funding_at_payout=liquid_funding,
        liquid_book_share=({k: v / liquid_book0 for k, v in liquid_funding.items()}),
    )


def pc_loss_pairs() -> dict:
    """Regime-weighted long-run private-credit loss (PD x LGD) for the competing calibrations.
    G6 4-state credit chain stationary weights B/N/T/C = 19.8/42.7/28.2/9.2% (G6 verifier check_math.py);
    GC2 / gap_01 3-state convention N/D/C = 70/20/10% with PD multipliers 1 / 1.5 / 3."""
    w4 = (0.198, 0.427, 0.282, 0.092)
    w3 = (0.70, 0.20, 0.10)
    m3 = (1.0, 1.5, 3.0)
    out = {}
    # A. GC2 T6: PD_N 1.8%, LGD 0.40 (+15pp in crisis)
    out["A_gc2_pd1.8_lgd0.40"] = sum(w * 0.018 * m * l for w, m, l in zip(w3, m3, (0.40, 0.40, 0.55)))
    # B. GC1 D16: PD 1.1/1.5/2.4/6.0%, recovery 55/50/45/35%
    out["B_gc1_incidence"] = sum(w * p * (1 - r) for w, p, r in zip(w4, (0.011, 0.015, 0.024, 0.060),
                                                                   (0.55, 0.50, 0.45, 0.35)))
    # C. gap_01: LGD 0.67, PD_N 1.1%, crisis recovery x0.7
    lgd_c = 1 - 0.33 * 0.7
    out["C_gap01_severity"] = sum(w * 0.011 * m * l for w, m, l in zip(w3, m3, (0.67, 0.67, lgd_c)))
    # D. Cross: GC1's incidence PDs with the observed direct-loan LGD 0.67 (crisis x0.7 recovery)
    out["D_gc1_pd_with_lgd0.67"] = sum(w * p * l for w, p, l in zip(w4, (0.011, 0.015, 0.024, 0.060),
                                                                   (0.67, 0.67, 0.67, lgd_c)))
    out["D_gc1_pd_with_lgd0.67_flat"] = sum(w * p * 0.67 for w, p in zip(w4, (0.011, 0.015, 0.024, 0.060)))
    return out


def coinvest_flow() -> dict:
    """G4 offered-flow model in steady state: accepted = theta * C * a (sum of lag weights d_k = 1).
    theta = 0.33 (Bain GP-level median, used at LP level [I]); acceptance a in [0.3, 0.6] [I]."""
    theta = 0.33
    out = {}
    for label, c in (("G1 mature PE pace 5.1", 5.1), ("G7 PE share of $12bn/yr = 7.2", 7.2), ("G4 assumption 10.0", 10.0)):
        out[label] = {"offered": theta * c, "accepted_a0.3": theta * c * 0.3, "accepted_a0.5": theta * c * 0.5,
                      "accepted_a0.6": theta * c * 0.6}
    out["sustain_18bn_book_per_G4"] = 3.0
    return out


def main() -> None:
    res = {"note": "SYNTHETIC / ILLUSTRATIVE ONLY - not ADIC data",
           "unfunded_g7": g.UNF0, "unfunded_census_v1": UNF_CENSUS,
           "rates_note": "Annual distribution rates by exit regime and group from G7 DIST; census config replaces "
                         "co-investment normal/drought with GC1 production yields 19.3%/12.4%. Calls: G7 CALL "
                         "(normal 29%, drought 28%, crisis 30%) x scenario multiplier; new commitments $12bn/yr "
                         "allocated 60/10/10/10/10 (PE/Sec/PC/CapSol/Co)."}
    out = {}
    for cfg, unf0 in (("g7", g.UNF0), ("census", UNF_CENSUS)):
        rates = dist_table(cfg)
        for scn in ("normal", "drought", "S1", "T14"):
            out[f"{cfg}|{scn}"] = run(scn, unf0, rates)
    # PE drought-rate sensitivity (MSCI H1-2026 9%)
    out["census|drought|pe9"] = run("drought", UNF_CENSUS, dist_table("census", pe_drought=0.09))
    res["runs"] = out
    # reproduction check vs gap_01's group table (drought and S1, G7 split)
    gap01 = {"drought": {"pe": -1.95, "sec": 0.41, "co": 1.24, "cs": 0.04, "pc": 1.12, "total": 0.86},
             "S1": {"pe": -9.29, "sec": -1.71, "co": -0.19, "cs": -0.81, "pc": -0.76, "total": -12.76}}
    chk = {}
    for scn, ref in gap01.items():
        r = out[f"g7|{scn}"]
        mine = {k: round(v, 2) for k, v in r["net_by_group"].items()}
        mine["total"] = round(r["private_net"], 2)
        chk[scn] = {"gap01": ref, "reproduced": mine,
                    "max_abs_diff": max(abs(mine[k] - ref[k]) for k in ref)}
    res["repro_check_gap01"] = chk
    res["pc_loss_pairs"] = pc_loss_pairs()
    res["coinvest_flow"] = coinvest_flow()
    t14 = out["census|T14"]["net_by_group"]
    s1 = out["census|S1"]["net_by_group"]
    res["pe_share_of_private_drain"] = {"T14": t14["pe"] / sum(t14.values()), "S1": s1["pe"] / sum(s1.values())}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    # compact console summary
    for key, r in out.items():
        ng = {k: round(v, 2) for k, v in r["net_by_group"].items()}
        print(key, "| dist", round(r["private_dist"], 2), "calls", round(r["private_calls"], 2),
              "net", round(r["private_net"], 2), "| by group", ng, "| overlay", round(r["overlay"]["net"], 2),
              "| before payout", round(r["before_payout"], 2),
              "| liquid funding @5/7.5/10", {k: round(v, 1) for k, v in r["liquid_book_funding_at_payout"].items()})
    print("repro:", json.dumps(chk))
    print("pc_loss_pairs:", json.dumps({k: round(v, 5) for k, v in res["pc_loss_pairs"].items()}))
    print("coinvest_flow:", json.dumps(res["coinvest_flow"]))
    print("pe_share_of_private_drain:", json.dumps(res["pe_share_of_private_drain"]))


if __name__ == "__main__":
    main()
