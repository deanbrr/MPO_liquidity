"""
gap_01: swap the hedge-fund treatment inside the GC2 / stream-G7 ladder for the state machine.

GC2 (research/groups/clusters/GC2_liquidity_org_data.md, sec. 4.4) computed survival on the canonical C1
T1.4-aligned stress with stream G7's bucket ladder for hedge funds (buckets <=7d / 8-90d / 91-365d / >365d,
time-to-cash 1 / 4 / 12 / 24 months, monthly capacity 80 / 25 / 10 / 10%, halved in crisis months).
This script re-runs GC2's run_v2 logic unchanged EXCEPT that hedge-fund counterbalancing capacity is the
state machine's P5 cash ladder phi(h) from hf_ladder.py (equity -40% variant, matching the S1/T1.4 equity
path of about -39%), i.e. the 5th-percentile share of t0 HF NAV received as cash by month h.

SYNTHETIC - NOT ADIC DATA.  GC2's script (research/groups/addenda/GC2_calcs/gc2_reconcile.py, which loads the
unmodified stream-G7 module from research/groups/addenda/G7_calcs/) is imported read-only; nothing in it is edited.

Run:  .venv\\Scripts\\python.exe -I -B t14_hf_swap.py      (-B: write no .pyc files into other streams' folders)
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE0 = os.path.dirname(os.path.abspath(__file__))
GC2_DIR = os.path.normpath(os.path.join(HERE0, "..", "..", "groups", "addenda", "GC2_calcs"))
sys.path.insert(0, GC2_DIR)
import gc2_reconcile as r2  # noqa: E402  (loads the unmodified stream-G7 ladder module)

g = r2.g
HERE = os.path.dirname(os.path.abspath(__file__))
HFRES = json.load(open(os.path.join(HERE, "hf_ladder_results.json"), encoding="utf-8"))
HF_KEYS = ["hf_le7d", "hf_8_90d", "hf_91_365d", "hf_gt365d"]
HF_TOTAL = sum(g.BAL0[k] for k in HF_KEYS)


def run_swap(scn: str, draw_basis: str, hf_phi: list | None, T: int = 36, cfp_actions: bool = False,
             nav_prearranged: bool = False) -> dict:
    p = r2.scenario_paths(scn, T)
    bal = dict(g.BAL0)
    unf = dict(g.UNF0)
    eq_idx = 1.0
    im = g.IM_RATE_N * g.SYN_NOTIONAL
    rows = []
    nco_prev = 0.0
    for t in range(T):                       # flows: identical to gc2_reconcile.run_v2
        reg = p["regime"][t]
        stress = reg == "crisis"
        for k, f in (("lo_dm", p["eq"][t]), ("lo_em", 1.2 * p["eq"][t]), ("lo_fi", p["fi"][t]),
                     ("ig", p["ig"][t]), ("ust", p["ust"][t]), ("cash", 0.039 / 12)):
            bal[k] *= 1 + f
        for k in g.HF_SHARES:
            bal[k] *= 1 + p["hf"][t]
        for gg in g.PRIVATE:
            bal[gg] *= 1 + p["priv_mark"][t]
        nav_start = sum(bal.values()) - nco_prev
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
            rate = g.DIST[reg][gg]
            if p["dist_zero"][t] and gg in ("pe", "sec", "co"):
                rate = 0.0
            dist[gg] = g.monthly_rate(rate) * bal[gg]
        crate = g.monthly_rate(min(0.95, g.CALL[reg] * p["call_mult"][t]))
        calls = {k: crate * unf[k] for k in ("pe", "sec", "pc", "cs", "co")}
        calls["sec_def"] = (g.UNF0["sec_def"] / 4.0) if t in (2, 5, 8, 11) else 0.0
        spike = p["rev_draw"][t] * g.UNF0["pc_rev"]
        calls["pc_rev"] = min(unf["pc_rev"], spike if spike > 0 else crate * unf["pc_rev"])
        nc = g.NEW_COMMIT_PA / 12.0
        if cfp_actions and stress and t >= 2:
            nc *= 0.25
        for k, v in calls.items():
            unf[k] -= v
        for k, w in (("pe", 0.6), ("sec", 0.1), ("pc", 0.1), ("cs", 0.1), ("co", 0.1)):
            unf[k] += w * nc
        for gg in g.PRIVATE:
            add = calls[gg] + (calls["sec_def"] if gg == "sec" else 0.0) + (calls["pc_rev"] if gg == "pc" else 0.0)
            bal[gg] += add - dist[gg]
        base = g.NAV0 if draw_basis == "opening" else nav_start
        draw = p["draw_rate"][t] * base / 12.0
        opex = 0.001 * g.NAV0 / 12.0
        uses = draw + sum(calls.values()) + max(0.0, -vm) + max(0.0, d_im) + max(0.0, -hedge_cf) + max(0.0, -opp) + opex
        inflows = sum(dist.values()) + max(0.0, vm) + max(0.0, -d_im) + max(0.0, hedge_cf) + max(0.0, opp)
        net = uses - inflows
        nco_prev += net
        rows.append(dict(net=net, gross_nav=sum(bal.values())))
    idx = {"cash": np.cumprod(np.full(T, 1 + 0.039 / 12)), "ust": np.cumprod(1 + p["ust"]),
           "ig": np.cumprod(1 + p["ig"]), "eq": np.cumprod(1 + p["eq"]), "fi": np.cumprod(1 + p["fi"]),
           "em": np.cumprod(1 + 1.2 * p["eq"]), "hf": np.cumprod(1 + p["hf"]), "priv": np.cumprod(1 + p["priv_mark"])}
    proceeds = {}
    for k, prm in g.LADDER.items():
        if hf_phi is not None and k in HF_KEYS:
            continue
        mv = g.BAL0[k] * idx[prm["path"]]
        cum = np.zeros(T)
        remaining, acc = 1.0, 0.0
        if k == "cash":
            mv = mv - (g.IM_RATE_N * g.SYN_NOTIONAL + g.OPP_IM)
        for t in range(T):
            crisis_t = p["regime"][t] == "crisis"
            hc = prm["hc_s"]
            ttc = prm["ttc"] + (2 if (crisis_t and prm["tier"] in ("A", "R")) else 0)
            if t >= ttc and remaining > 1e-12:
                frac = min(prm["cap"], remaining)
                if k.startswith("hf") and crisis_t:
                    frac *= 0.5
                remaining -= frac
                acc += frac * mv[t] * (1 - hc)
            cum[t] = acc
        proceeds[k] = cum
    if hf_phi is not None:                    # state-machine cash received by end of month t+1
        proceeds["hf_sm"] = HF_TOTAL * np.asarray(hf_phi[:T])
        hf_keys = ["hf_sm"]
    else:
        hf_keys = HF_KEYS
    fa = p["fac_avail"]
    rcf = np.array([0.0 if t < 1 else g.RCF_COMMITTED * fa[t] for t in range(T)])
    pe_sec = (g.BAL0["pe"] + g.BAL0["sec"]) * idx["priv"]
    lead = 0 if nav_prearranged else 3
    navf = np.array([0.0 if t < lead else p["navf_ltv"][t] * pe_sec[t] for t in range(T)])
    net = np.array([r["net"] for r in rows])
    nco = np.cumsum(net)
    tp_keys = ["cash", "ust", "ig", "lo_dm", "lo_fi", "lo_em"] + hf_keys
    cbc_tp = sum(proceeds[k] for k in tp_keys)
    true_nav = np.array([r["gross_nav"] for r in rows]) - nco
    cbc_tp4 = cbc_tp - 0.04 * true_nav
    cbc_tp8 = cbc_tp - 0.08 * true_nav

    def surv(c):
        br = np.where(nco > c)[0]
        return int(br[0] + 1) if br.size else None

    gap = np.maximum(0.0, nco[:24] - cbc_tp4[:24])
    fac_needed = float((gap[1:] / fa[1:24]).max()) if gap[1:].size else 0.0
    hf_cbc = {f"hf_cbc_{m}m": round(float(sum(proceeds[k][m - 1] for k in hf_keys)), 2) for m in (3, 6, 12, 24)}
    return dict(SH_TP_floor0=surv(cbc_tp), SH_TP_floor4=surv(cbc_tp4), SH_TP_floor8=surv(cbc_tp8),
                SH_TPF_floor4_rcf_navf=surv(cbc_tp4 + rcf + navf),
                facility_needed_24m_bn=round(fac_needed, 1), cover24_tp_floor4=round(float(cbc_tp4[23] / nco[23]), 3),
                need_12m=round(float(nco[11]), 1), need_24m=round(float(nco[23]), 1), **hf_cbc)


def main() -> None:
    phis = {"G7_buckets (as GC2)": None,
            "state_machine_P5_eq40": HFRES["equity_minus40"]["phi_monthly_p5"],
            "state_machine_P50_eq40": HFRES["equity_minus40"]["phi_monthly_p50"],
            "adverse_terms_P5": HFRES["adverse_terms_gate_x2"]["phi_monthly_p5"]}
    out = {"label": "SYNTHETIC - NOT ADIC DATA"}
    for scn, basis, cfp in (("S1", "opening", False), ("T14", "opening", False), ("T14", "current", False),
                            ("T14", "opening", True), ("T14", "current", True), ("T14_draw5", "current", False)):
        key = f"{scn}|{basis}" + ("|cfp" if cfp else "")
        out[key] = {name: run_swap(scn, basis, phi, cfp_actions=cfp, nav_prearranged=cfp) for name, phi in phis.items()}
    path = os.path.join(HERE, "t14_hf_swap_results.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    for key, v in out.items():
        if key == "label":
            continue
        for name, rr in v.items():
            print(f"{key:20s} {name:26s} SH_TP0 {rr['SH_TP_floor0']} SH_TP4 {rr['SH_TP_floor4']} SH_TP8 {rr['SH_TP_floor8']} "
                  f"SH_TPF4 {rr['SH_TPF_floor4_rcf_navf']} fac24 {rr['facility_needed_24m_bn']} cover24 {rr['cover24_tp_floor4']} "
                  f"HF cbc 3/6/12/24m {rr['hf_cbc_3m']}/{rr['hf_cbc_6m']}/{rr['hf_cbc_12m']}/{rr['hf_cbc_24m']}")


if __name__ == "__main__":
    main()
