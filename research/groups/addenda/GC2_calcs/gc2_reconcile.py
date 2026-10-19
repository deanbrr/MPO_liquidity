"""
GC2 cluster reconciliation calculations (ALL SYNTHETIC / ILLUSTRATIVE, never ADIC data).

Purpose
  1. Re-run the G7 liquidity ladder (the unmodified stream-G7 module, loaded from ../G7_calcs/) under
     (a) G7's own S1 demand bust and (b) a stress aligned with C1's canonical T1.4 named stress
         (equity ~-40%, PE-type distributions 0 for 24m, calls x1.5, cap draws, 50% facility availability,
          no private sales), each with two owner-draw conventions (fixed USD of opening NAV vs % of current NAV).
  2. Report survival on the IC-defined metric SH_TP(s*) (Treasury usable down to 4% of NAV), the 24m cover
     ratio and the committed facility needed to clear 24 months.
  3. Recompute ADIC-LCR(30d) with Basel L2/L2B composition caps and an operational-control variant.
  4. Convert Form PF notice-based hedge-fund liquidity into an illustrative cash-timing ladder.
  5. Corrected credibility weights (G5 R4) and private-credit PD calibration (G9 R2).

Run:  <venv>/python.exe -I gc2_reconcile.py   (writes gc2_reconcile_results.json next to this file)
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
_spec.loader.exec_module(g)  # stream-G7 ladder module, loaded unmodified from its project location

OUT = os.path.join(HERE, "gc2_reconcile_results.json")


def scenario_paths(scn: str, T: int = 36) -> dict:
    p = g.build_paths("S1_demand_bust_24m", T)
    p["dist_zero"] = np.zeros(T, dtype=bool)
    crisis = np.array([r == "crisis" for r in p["regime"]])
    p["fac_avail"] = np.where(crisis, 0.75, 1.0)      # G7 convention: committed RCF at 75% in crisis months
    p["navf_ltv"] = np.where(crisis, 0.05, 0.10)      # G7 convention: NAV-facility LTV 5% in crisis, 10% otherwise
    if scn == "S1":
        return p
    if scn.startswith("T14"):             # C1 T1.4-aligned
        p["call_mult"] = np.ones(T)
        p["call_mult"][:24] = 1.25 if scn == "T14_call125" else 1.5
        p["draw_rate"] = np.full(T, 0.075)
        p["draw_rate"][:24] = 0.05 if scn == "T14_draw5" else 0.10
        p["dist_zero"][:24] = True        # PE funds, Secondaries, Co-investment distribute nothing for 24 months
        p["fac_avail"] = np.where(np.arange(T) < 24, 0.50, 1.0)   # T1.4: 50% facility availability for 24 months
        p["navf_ltv"] = np.where(np.arange(T) < 24, 0.05, 0.10)   # i.e. half of the 10% normal LTV
        return p
    raise ValueError(scn)


def run_v2(scn: str, draw_basis: str = "opening", T: int = 36, cfp_actions: bool = False,
           nav_prearranged: bool = False) -> dict:
    p = scenario_paths(scn, T)
    bal = dict(g.BAL0)
    unf = dict(g.UNF0)
    eq_idx = 1.0
    im = g.IM_RATE_N * g.SYN_NOTIONAL
    rows = []
    nco_prev = 0.0
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
        rows.append(dict(net=net, draw=draw, gross_nav=sum(bal.values()), calls=sum(calls.values()),
                         dist=sum(dist.values()), vm=vm, d_im=d_im, hedge=hedge_cf))
    # counterbalancing capacity (same mechanics as the G7 module)
    idx = {"cash": np.cumprod(np.full(T, 1 + 0.039 / 12)), "ust": np.cumprod(1 + p["ust"]),
           "ig": np.cumprod(1 + p["ig"]), "eq": np.cumprod(1 + p["eq"]), "fi": np.cumprod(1 + p["fi"]),
           "em": np.cumprod(1 + 1.2 * p["eq"]), "hf": np.cumprod(1 + p["hf"]), "priv": np.cumprod(1 + p["priv_mark"])}
    proceeds = {}
    for k, prm in g.LADDER.items():
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
    fa = p["fac_avail"]
    rcf = np.array([0.0 if t < 1 else g.RCF_COMMITTED * fa[t] for t in range(T)])
    pe_sec = (g.BAL0["pe"] + g.BAL0["sec"]) * idx["priv"]
    lead = 0 if nav_prearranged else 3
    navf = np.array([0.0 if t < lead else p["navf_ltv"][t] * pe_sec[t] for t in range(T)])
    net = np.array([r["net"] for r in rows])
    nco = np.cumsum(net)
    tp_keys = ["cash", "ust", "ig", "lo_dm", "lo_fi", "lo_em", "hf_le7d", "hf_8_90d", "hf_91_365d", "hf_gt365d"]
    cbc_t = sum(proceeds[k] for k in ("cash", "ust", "ig"))
    cbc_tp = sum(proceeds[k] for k in tp_keys)
    true_nav = np.array([r["gross_nav"] for r in rows]) - nco
    cbc_tp4 = cbc_tp - 0.04 * true_nav
    cbc_tp8 = cbc_tp - 0.08 * true_nav
    cbc_tpf4_rcf = cbc_tp4 + rcf
    cbc_tpf4_all = cbc_tp4 + rcf + navf

    def surv(c):
        br = np.where(nco > c)[0]
        return int(br[0] + 1) if br.size else None

    # committed facility needed (counted from month 2, at availability fa) so that SH_TP_floor4 >= 24 months
    gap = np.maximum(0.0, nco[:24] - cbc_tp4[:24])
    month1_gap = float(gap[0])
    fac_needed = float((gap[1:] / fa[1:24]).max()) if gap[1:].size else 0.0
    return dict(
        scenario=scn, draw_basis=draw_basis, cfp_actions=cfp_actions, nav_prearranged=nav_prearranged,
        need_12m=float(nco[11]), need_24m=float(nco[23]),
        draws_12m=float(sum(r["draw"] for r in rows[:12])), draws_24m=float(sum(r["draw"] for r in rows[:24])),
        calls_12m=float(sum(r["calls"] for r in rows[:12])), dist_12m=float(sum(r["dist"] for r in rows[:12])),
        cbc_tp_24m=float(cbc_tp[23]), cover24_tp=float(cbc_tp[23] / nco[23]),
        cover24_tp_floor4=float(cbc_tp4[23] / nco[23]),
        SH_T=surv(cbc_t), SH_TP_floor0=surv(cbc_tp), SH_TP_floor4=surv(cbc_tp4), SH_TP_floor8=surv(cbc_tp8),
        SH_TPF_floor4_rcf=surv(cbc_tpf4_rcf), SH_TPF_floor4_rcf_navf=surv(cbc_tpf4_all),
        month1_gap_floor4=month1_gap, committed_facility_needed_for_24m=fac_needed,
        facility_availability_min=float(fa[:24].min()),
        true_nav_12m=float(true_nav[11]), true_nav_24m=float(true_nav[23]),
    )


def lcr30_variants() -> dict:
    base = g.lcr30_t0()
    net_out = base["net_outflow"]
    l1 = base["hqla"]["L1_cash_unencumbered"] + base["hqla"]["L1_ust"]
    l2a = base["hqla"]["L2A_ig"]

    def capped(L1, L2A, L2B):
        adj15 = max(L2B - 15 / 85 * (L1 + L2A), L2B - 15 / 60 * L1, 0.0)
        adj40 = max((L2A + L2B - adj15) - 2 / 3 * L1, 0.0)
        return L1 + L2A + L2B - adj15 - adj40

    dm_l2b = base["hqla"]["L2B_dm_equity"]
    lofi_25 = base["hqla"]["L2_lo_fixed_income"]
    out = dict(
        net_outflow=net_out,
        uncapped=sum(base["hqla"].values()) / net_out,
        capped_lofi_as_L2B=capped(l1, l2a, dm_l2b + lofi_25) / net_out,
        capped_lofi_as_L1=capped(l1 + g.BAL0["lo_fi"], l2a, dm_l2b) / net_out,
        treasury_controlled_only=(l1 + l2a) / net_out,
    )
    # R6: Basel LCR40.64 40% 30-day drawdown on regular unfunded instead of ~3.8%/month
    regular_unf = 38.0 - g.UNF0["sec_def"] - g.UNF0["pc_rev"]
    extra = 0.40 * regular_unf - base["outflows"]["calls_stressed"]
    tot_out = base["total_outflow"] + extra
    net_r6 = tot_out - min(sum(base["inflows"].values()), 0.75 * tot_out)
    out["basel40_unfunded_extra_outflow"] = extra
    out["basel40_capped_lofi_as_L2B"] = capped(l1, l2a, dm_l2b + lofi_25) / net_r6
    out["basel40_uncapped"] = sum(base["hqla"].values()) / net_r6
    return out


def hf_cash_timing(nav_hf: float = 20.0, le7: float = 0.084, b8_90: float = 0.273,
                   pay_lag_days: float = 30.0, holdback: float = 0.05) -> dict:
    """Convert Form PF notice-based buckets (<=7d, 8-90d) into cash received by day h, assuming effective
    dates uniform within the 8-90d bucket, a payment lag after the dealing date and an audit holdback.
    Gates are already assumed in Form PF; suspensions, side pockets and ADIC's own queue effect are excluded."""
    res = {}
    for h in (30, 90, 120, 180):
        lim = h - pay_lag_days
        f_le7 = 1.0 if lim >= 7 else max(0.0, lim / 7.0)
        f_mid = min(1.0, max(0.0, (lim - 8.0) / (90.0 - 8.0)))
        share = (le7 * f_le7 + b8_90 * f_mid) * (1 - holdback)
        res[f"cash_by_{h}d_share"] = share
        res[f"cash_by_{h}d_bn"] = share * nav_hf
    res["notice_based_le90d_bn"] = (le7 + b8_90) * nav_hf
    res["notice_based_le7d_bn"] = le7 * nav_hf
    return res


def credibility() -> dict:
    def Z(n, sig, tau):
        k = (sig / tau) ** 2
        return n / (n + k)
    cases = {"LO_DM (TE 3%, IR sd 0.15)": (0.03, 0.15 * 0.03), "LO_EM/small (TE 5%, IR sd 0.20)": (0.05, 0.20 * 0.05),
             "HF event/credit (6%, 2.5%)": (0.06, 0.025), "HF multi-strategy (4%, 2.5%)": (0.04, 0.025),
             "HF trend (11%, 2.0%)": (0.11, 0.02),
             "HF event/credit de-smoothed (6%/0.74, 2.5%)": (0.06 / 0.735, 0.025)}
    return {name: {f"Z_{n}y": round(Z(n, s, t), 3) for n in (3, 5, 10)} for name, (s, t) in cases.items()}


def pc_pd_calibration(shares=(0.70, 0.20, 0.10), mult=(1.0, 1.5, 3.0), lgd=(0.40, 0.40, 0.55), target=0.01) -> dict:
    w = sum(s * m * l for s, m, l in zip(shares, mult, lgd))
    return dict(el_at_pd_2p5=0.025 * w, pd_normal_for_1pct=target / w)


def refi_cost_table() -> dict:
    """G5 worked REFINANCE example re-expressed per $ of cash freed per year (R7-consistent)."""
    out = {}
    for name, f, im, buf in (("normal", 0.0050, 0.06, 0.117), ("jun2026_like", 0.0081, 0.08, 0.117),
                             ("stress_175bp_assumption", 0.0175, 0.12, 0.33),
                             ("stress_140bp_documented_quarterly_max", 0.0140, 0.12, 0.33)):
        freed = 1 - im - buf
        lo = (f - 0.0025 + 0.0008) / freed
        hi = (f + 0.0008) / freed
        out[name] = dict(cash_freed_per_5bn=5.0 * freed, cost_lo=lo, cost_hi=hi)
    return out


def main() -> None:
    res = {"note": "SYNTHETIC / ILLUSTRATIVE ONLY - not ADIC data"}
    named = {}
    for scn in ("S1", "T14", "T14_draw5", "T14_call125"):
        for basis in ("opening", "current"):
            named[f"{scn}|{basis}"] = run_v2(scn, basis)
            named[f"{scn}|{basis}|cfp"] = run_v2(scn, basis, cfp_actions=True, nav_prearranged=True)
    res["named"] = named
    # reproduction checks against the G7 module / verifier harness
    mod = g.run_named("S1_demand_bust_24m")
    res["repro_check"] = dict(module_need12=mod["net_need_cum"]["12m"], module_need24=mod["net_need_cum"]["24m"],
                              module_SH_TP=mod["survival_months"]["TP"],
                              v2_need12=named["S1|opening"]["need_12m"], v2_need24=named["S1|opening"]["need_24m"],
                              v2_SH_TP=named["S1|opening"]["SH_TP_floor0"],
                              v2_SH_TP_floor4=named["S1|opening"]["SH_TP_floor4"])
    res["lcr30"] = lcr30_variants()
    res["hf_cash_timing"] = hf_cash_timing()
    res["credibility"] = credibility()
    res["pc_pd"] = pc_pd_calibration()
    res["refi_cost"] = refi_cost_table()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
