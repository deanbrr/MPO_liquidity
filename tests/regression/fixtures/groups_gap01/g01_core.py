"""
Group gap_01 (groups workflow): re-base the group layer on gap_02's canonical stress T4' = s*(0.76) and add a
group-level RECOVERY mode (Phase I over group-tagged reversible levers, Phase II restored problem, duals,
FTP charges, hurdles and envelopes).

SYNTHETIC - NOT ADIC DATA. Working allocation of context s1A; GC2 census as used by gap_02's t1_engine.
Lever capacities and costs are design assumptions [I] stated next to each lever below.

Core pieces
  gl_ladder()     group-resolved replica of t1_engine.ladder() (asserted to reproduce it exactly on the
                  readings and policies used by gap_02), extended with group levers.
  LEVERS / CARDS  group-tagged reversible levers (Phase I) and group decision cards (Phase II only for
                  red-tier and secondary sales).
  coefficients()  finite-difference slopes of the monthly T+P+F headroom rows h = 1..24 per lever and card.
  phase1(), solve()  lexicographic minimum violation; elastic or hard (restored) LP; duals by month row.
  group_prices()  FTP charges, hurdles, envelopes and glide-path allocation from a restored solution only.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import sys

import cvxpy as cp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GAP02 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "addenda", "gap_02_calcs"))
sys.path.insert(0, GAP02)
import t1_engine as E  # noqa: E402
from gap02_study import s_star, t4_literal  # noqa: E402

PRIV = ("pe", "sec", "co", "cs", "pc")
GROUP_NAME = {"pe": "PE", "sec": "Secondaries", "co": "Co-investment", "cs": "Capital Solutions",
              "pc": "Private Credit", "pm": "Public Markets", "ovl": "Overlay", "cf": "Corporate Finance",
              "own": "Owner (band)"}
W_NEW = {"pe": 0.6, "sec": 0.1, "pc": 0.1, "cs": 0.1, "co": 0.1}        # $12bn/yr split (GC2 census)
M_TIERS = {"S": 1e2, "IG": 10.0}                                          # synthesis s4.8 tiers (as gap_02)
H_ROWS = 24                                                               # monthly rows h = 1..24
ALPHA_D = {"pe": (0.015, 5.0), "sec": (0.030, 3.4), "co": (0.025, 4.5),   # (alpha*, duration): G8 E1 alpha*
           "cs": (0.035, 4.0), "pc": (0.010, 3.0)}                        # [I]; durations from s3 examples [I]
SMA_SLEEVE = 0.40 * E.PRIV0["pc"]                                         # SMA wrapper 40% (s3.6 default) = 5.6
RUNOFF_C, RUNOFF_T = 0.065, 0.14                                          # SMA principal run-off, C / T (G6)
P_SMA, P_CS, P_HF = 0.96, 0.90, 0.80                                      # t0 prices [I]: G6 T 0.95-0.97;
#                                                                           G3 yield mark -8-12%; G5 15-25%

BASE = dict(rcf=0.0, navf=0.0, reserve=0.0, reserve_add=0.0, band=0.0, pace=12.0,
            cut={g: 0.0 for g in W_NEW}, cut_from=2, amber_t0=0.0, sma_sell=0.0, cs_synd=0.0, sma_ro=0.0,
            ovl_im=0.0, p2s=0.0, hf_sell=0.0, red={"pe": 0.0, "sec": 0.0, "co": 0.0},
            red_bid={"pe": 0.88, "sec": 0.87, "co": 0.75}, new_commit={g: 0.0 for g in W_NEW}, cash_t0=0.0,
            census="gap02")


def lev_of(**kw) -> dict:
    lev = copy.deepcopy(BASE)
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(lev.get(k), dict):
            lev[k].update(v)
        else:
            lev[k] = v
    return lev


def lev_from_policy(pol: E.Policy) -> dict:
    """Map a gap_02 Policy onto the lever dict (used to assert exact reproduction of t1_engine.ladder)."""
    cut = 0.75 if pol.pace_cut else 0.0
    return lev_of(rcf=pol.rcf, navf=pol.navf, reserve=pol.reserve, band=1.0 if pol.band else 0.0, pace=pol.pace,
                  cut={g: cut for g in W_NEW}, amber_t0=pol.amber_t0)


def _monthly(r):
    return 1.0 - (1.0 - r) ** (1.0 / 12.0)


def gl_ladder(s: E.Stress, lev: dict | None = None, T: int = 36, pol: E.Policy | None = None) -> dict:
    """Monthly survival ladder on the t0 synthetic book, group-resolved. Mirrors t1_engine.ladder line by line;
    additions (group levers) are inert at their defaults."""
    if lev is None:
        lev = lev_from_policy(pol if pol is not None else E.Policy("A"))
    P = E.Policy("x", rcf=lev["rcf"], navf=lev["navf"])         # fee schedule only
    eq = np.zeros(T)
    if s.instant:
        eq[0] = -s.eq_drawdown
    else:
        shape = np.array([0.15, 0.12, 0.08, 0.05, 0.04, 0.03])
        shape = shape / shape.sum()
        eq[:6] = np.exp(shape * math.log(1 - s.eq_drawdown)) - 1
    eq[12:24] = 0.02
    eq[24:] = 0.008
    fi = np.zeros(T)
    fi[:3] = -0.02
    fi[3:] = 0.005
    hf_r = np.zeros(T)
    if s.instant:
        hf_r[0] = 0.3 * (-s.eq_drawdown) - 0.06
    else:
        hf_r[:4] = -0.03
    hf_r[12:] = 0.008
    pm = np.zeros(T)
    for mth, v in s.priv_marks:
        pm[mth] = v
    pm[14::3] = 0.01
    crisis = np.arange(T) < s.crisis_months

    def mult_at(table, t, default):
        acc = 0
        for months, mlt in table:
            if t < acc + months:
                return mlt
            acc += months
        return default

    if lev.get("census", "gap02") == "v1":            # census v1.0 split (groups report s6): Sec 3.5+0.4, PC 3.0+1.0
        unf0 = dict(pe=27.4, sec=3.5, co=1.5, cs=1.2, pc=3.0)
        sec_def0, pc_rev0 = 0.4, 1.0
    else:
        unf0, sec_def0, pc_rev0 = dict(E.UNF0), E.SEC_DEF0, E.PC_REV0

    # ---------------- t0 balances after t0 actions
    tre = E.TRE0 + lev["cash_t0"]
    dm, em, fi_b = E.LO0["dm"], E.LO0["em"], E.LO0["fi"]
    hf0 = E.HF0
    priv = dict(E.PRIV0)
    unf = dict(unf0)
    proceeds = {g: 0.0 for g in ("pe", "sec", "co", "cs", "pc", "pm")}
    if lev["amber_t0"] > 0:                                  # gap_02 pro-rata PC/CS sale at PRICE_N
        tot = E.PRIV0["pc"] + E.PRIV0["cs"]
        for g in ("pc", "cs"):
            amt = lev["amber_t0"] * E.PRIV0[g] / tot
            tre += amt * E.PRICE_N[g]
            proceeds[g] += amt * E.PRICE_N[g]
            unf[g] *= 1 - amt / E.PRIV0[g]
            priv[g] -= amt
    if lev["sma_sell"] > 0:                                  # PC SMA performing loans (funded; no unfunded attached)
        tre += lev["sma_sell"] * P_SMA
        proceeds["pc"] += lev["sma_sell"] * P_SMA
        priv["pc"] -= lev["sma_sell"]
    if lev["cs_synd"] > 0:                                   # CS sell-down; buyer assumes pro-rata unfunded
        tre += lev["cs_synd"] * P_CS
        proceeds["cs"] += lev["cs_synd"] * P_CS
        unf["cs"] *= 1 - lev["cs_synd"] / E.PRIV0["cs"]
        priv["cs"] -= lev["cs_synd"]
    for g in ("pe", "sec", "co"):                            # red-tier test sales; buyer assumes pro-rata unfunded
        amt = lev["red"][g]
        if amt > 0:
            tre += amt * lev["red_bid"][g]
            proceeds[g] += amt * lev["red_bid"][g]
            unf[g] *= 1 - amt / E.PRIV0[g]
            priv[g] -= amt
    if lev["hf_sell"] > 0:                                   # HF secondary sale (removes the lot from the queue)
        tre += lev["hf_sell"] * P_HF
        proceeds["pm"] += lev["hf_sell"] * P_HF
        hf0 -= lev["hf_sell"]
    for g in W_NEW:                                          # extra $1 commitments (for hurdle slopes)
        if g == "co":
            tre -= lev["new_commit"]["co"]
            priv["co"] += lev["new_commit"]["co"]
        else:
            unf[g] += lev["new_commit"][g]
    n_syn = E.N_SYN0 + lev["p2s"]
    if lev["p2s"] > 0:                                       # P2S: sell DM, keep exposure in futures
        dm -= lev["p2s"]
        tre += lev["p2s"] * 0.998
    enc0 = E.IM_N * n_syn + E.OPP_IM0 - lev["ovl_im"]
    top = max(0.0, lev["reserve"] * E.NAV0 - (tre - enc0)) + lev["reserve_add"]
    a = min(top / 0.998, dm)
    dm -= a
    tre += a * 0.998
    tre -= lev["rcf"] * P.rcf_upfront + lev["navf"] * P.navf_upfront

    eq_idx = 1.0
    im = E.IM_N * n_syn
    sec_def, pc_rev = sec_def0, pc_rev0
    ro_book = lev["sma_ro"]
    priv_m = dict(priv)
    basis = E.NAV0
    nco = 0.0
    liq_bh = dict(tre=tre, dm=dm, em=em, fi=fi_b, hf=hf0)
    rows = []
    gf = {g: dict(dist=np.zeros(T), calls=np.zeros(T)) for g in PRIV}
    ovl = dict(vm=np.zeros(T), dim=np.zeros(T), tail=np.zeros(T), prem=np.zeros(T), opp=np.zeros(T),
               fut=np.zeros(T))
    cfv = dict(draw=np.zeros(T), opex=np.zeros(T), fee=np.zeros(T))
    withheld = 0.0
    for t in range(T):
        for g in priv_m:
            priv_m[g] *= 1 + pm[t]
        ro_book *= 1 + pm[t]
        dist = 0.0
        for g in ("pe", "sec", "co"):
            r = E.DROUGHT_DIST[g] * mult_at(s.dist_mult_pe, t, 1.0)
            d = _monthly(min(0.95, r)) * priv_m[g]
            priv_m[g] -= d
            dist += d
            gf[g]["dist"][t] += d
        for g, r in (("pc", s.pc_cs_rates[0]), ("cs", s.pc_cs_rates[1])):
            r_eff = r if crisis[t] else E.DIST_NORMAL[g] * 0.92
            d = _monthly(r_eff) * priv_m[g]
            priv_m[g] -= d
            dist += d
            gf[g]["dist"][t] += d
        if ro_book > 0:                                      # SMA run-off: principal no longer reinvested
            d = _monthly(RUNOFF_C if crisis[t] else RUNOFF_T) * ro_book
            ro_book -= d
            priv_m["pc"] -= d
            dist += d
            gf["pc"]["dist"][t] += d
        crate = _monthly(min(0.95, 0.28 * mult_at(s.call_mult, t, 1.0)))
        calls = 0.0
        for g in unf:
            c = crate * unf[g]
            unf[g] -= c
            priv_m[g] += c
            calls += c
            gf[g]["calls"][t] += c
        if t in (2, 5, 8, 11):
            calls += sec_def0 / 4
            gf["sec"]["calls"][t] += sec_def0 / 4
        rev = min(pc_rev, 0.5 * pc_rev0 / 3 if t < 3 else _monthly(0.15) * pc_rev)
        pc_rev -= rev
        calls += rev
        gf["pc"]["calls"][t] += rev
        k = lev["pace"] / 12
        active = t >= lev["cut_from"] and crisis[t]
        for g in ("pe", "sec", "pc", "cs"):
            unf[g] += W_NEW[g] * k * (1 - (lev["cut"][g] if active else 0.0))
        c_co = 0.1 * k * (1 - (lev["cut"]["co"] if active else 0.0))
        calls += c_co
        gf["co"]["calls"][t] += c_co
        fy = t // 12
        rate = s.draw_rates[min(fy, len(s.draw_rates) - 1)]
        rate0 = rate
        if crisis[t] and lev["band"] > 0:
            rate = lev["band"] * 0.05 + (1 - lev["band"]) * rate
        if fy == 1:
            rate += s.override_y2
            rate0 += s.override_y2
        nav_now_est = sum(liq_bh.values()) + sum(priv_m.values()) - nco
        if s.draw_basis == "fixed_usd":
            base = E.NAV0
        elif s.draw_basis == "current":
            base = max(nav_now_est, 1e-9)
        else:
            if t % 12 == 0:
                lag_priv = sum(priv_m.values()) / (1 + (pm[max(t - 1, 0)] + pm[max(t - 2, 0)] + pm[max(t - 3, 0)]))
                basis = (nav_now_est - sum(priv_m.values()) + lag_priv) if t > 0 else E.NAV0
            base = basis
        draw = rate * base / 12
        withheld += (rate0 - rate) * base / 12
        vm = n_syn * eq_idx * eq[t]
        eq_idx *= 1 + eq[t]
        im_new = (E.IM_S if (crisis[t] and t < s.im_months) else E.IM_N) * n_syn * eq_idx
        d_im = im_new - im
        im = im_new
        prem = E.TAIL_PREM * E.NAV0 / 12
        tail = 0.0
        if t in (1, 5):
            tail = 0.5 * E.N_TAIL * min(0.18, max(0.0, 0.90 - eq_idx))
        opp = 0.015 * E.NAV0 / 3 if t < 3 else 0.0
        fut = lev["p2s"] * eq_idx * (E.FUT_SPREAD_S if crisis[t] else E.FUT_SPREAD_N) / 12   # P2S roll spread
        fee = lev["rcf"] * P.rcf_undrawn_fee / 12 + lev["navf"] * P.navf_undrawn_fee / 12
        opex = 0.001 * E.NAV0 / 12
        net = draw + calls + prem + opp + fee + opex + fut + max(0.0, d_im) - dist - vm - tail - max(0.0, -d_im)
        nco += net
        ovl["vm"][t], ovl["dim"][t], ovl["tail"][t], ovl["prem"][t], ovl["opp"][t], ovl["fut"][t] = \
            vm, d_im, tail, prem, opp, fut
        cfv["draw"][t], cfv["opex"][t], cfv["fee"][t] = draw, opex, fee
        rows.append(dict(net=net, nco=nco, draw=draw, calls=calls, dist=dist, vm=vm, tail=tail, nav=nav_now_est))
        for kk, f in (("tre", 0.0), ("dm", eq[t]), ("em", 1.2 * eq[t]), ("fi", fi[t]), ("hf", hf_r[t])):
            liq_bh[kk] *= 1 + f

    # ---------------- counterbalancing capacity (as t1_engine.ladder)
    idx_eq = np.cumprod(1 + eq)
    idx_em = np.cumprod(1 + 1.2 * eq)
    idx_fi = np.cumprod(1 + fi)
    idx_hf = np.cumprod(1 + hf_r)
    cbc = np.zeros(T)
    hf_monthly = np.zeros(T + 40)
    for q, share in enumerate(E.HF_SCHED):
        for mm in range(3):
            hf_monthly[3 * q + mm] += share / 3
    hf_cash = np.zeros(T)
    backlog = 0.0
    for t in range(T):
        due = hf_monthly[t] * hf0 * idx_hf[t] + backlog
        paid = s.hf_pass * due if crisis[t] else due
        backlog = due - paid
        hf_cash[t] = paid
    cum_hf = np.cumsum(hf_cash)
    acc_dm = acc_fi = acc_em = 0.0
    rem_dm = rem_fi = rem_em = 1.0
    tre_cap = tre - enc0
    tre_haircut = 0.4 * 0.0 + 0.27 * 0.02 + 0.33 * 0.10
    comp = dict(tre=np.zeros(T), lo=np.zeros(T), hf=np.zeros(T))
    for t in range(T):
        f = min(0.5, rem_dm)
        rem_dm -= f
        acc_dm += f * dm * idx_eq[t] * (1 - 0.015)
        f = min(0.5, rem_fi)
        rem_fi -= f
        acc_fi += f * fi_b * idx_fi[t] * (1 - 0.05)
        if t >= 1:
            f = min(0.5, rem_em)
            rem_em -= f
            acc_em += f * em * idx_em[t] * (1 - 0.05)
        cbc[t] = tre_cap * (1 - tre_haircut) + acc_dm + acc_fi + acc_em + cum_hf[t]
        comp["tre"][t], comp["lo"][t], comp["hf"][t] = tre_cap * (1 - tre_haircut), acc_dm + acc_fi + acc_em, cum_hf[t]
    nco_arr = np.array([r["nco"] for r in rows])
    nav_arr = np.array([r["nav"] for r in rows])
    floor_arr = s.floor * nav_arr
    fac = np.array([0.0 if t < 1 else lev["rcf"] * s.fac_credit for t in range(T)])
    pool = min(0.20 * sum(E.PRIV0.values()), E.PRIV0["pe"] + E.PRIV0["sec"])
    navf_cap = np.array([0.0 if t < 1 else min(lev["navf"], s.navf_ltv * pool) for t in range(T)])
    head_tp = cbc - floor_arr - nco_arr
    head_tpf = head_tp + fac + navf_cap

    def first_breach(head):
        br = np.where(head < 0)[0]
        return int(br[0] + 1) if br.size else None

    gap = np.maximum(0.0, -(head_tp[1:24] + navf_cap[1:24]))
    return dict(head_tp=head_tp, head_tpf=head_tpf, cbc=cbc, nco=nco_arr, nav=nav_arr, floor=floor_arr, fac=fac,
                navf=navf_cap, gf=gf, ovl=ovl, cf=cfv, proceeds=proceeds, comp=comp, withheld24=withheld,
                SH_TP=first_breach(head_tp), SH_TPF=first_breach(head_tpf),
                min_head_tpf_24=float(head_tpf[:24].min()), argmin_24=int(np.argmin(head_tpf[:24]) + 1),
                fac_need_24=float(gap.max() / s.fac_credit) if gap.size else 0.0,
                gstar=float((-head_tp[:24]).max()), nco24=float(nco_arr[23]), tre_t0=tre, enc0=enc0,
                usable_t0=tre - enc0)


# ------------------------------------------------------------------------------------------------------------
# Levers (Phase I set = reversible, non-red) and cards (Phase II only). cost = 5-year PV $ per unit [I].
# ------------------------------------------------------------------------------------------------------------
def _cut_months(s: E.Stress) -> int:
    return sum(1 for t in range(H_ROWS) if t >= 2 and t < s.crisis_months)


def levers(s: E.Stress) -> list:
    nm = _cut_months(s) / 12.0                     # years of stage-triggered cuts inside the 24-month window
    L = []
    for g, cap in (("pe", 0.75), ("co", 1.0), ("sec", 1.0), ("pc", 1.0), ("cs", 1.0)):
        a, d = ALPHA_D[g]
        forgone = 12.0 * W_NEW[g] * nm             # $bn of commitments forgone per unit of cut
        L.append(dict(key=f"pace_{g}", owner=g, unit="share of group flow cut (stage rule)", cap=cap,
                      cost=a * d * forgone, ig=0.0,
                      apply=(lambda lev, x, g=g: lev["cut"].__setitem__(g, x)), step=0.5,
                      note="PE: protected core 25%; others: contingent budget / pause"))
    L += [
        dict(key="sma_sell", owner="pc", unit="$bn SMA loans sold at 0.96", cap=SMA_SLEEVE, cost=1 - P_SMA,
             ig=P_SMA, apply=lambda lev, x: lev.__setitem__("sma_sell", x), step=2.0, note="alpha* ~0 (G6)"),
        dict(key="sma_ro", owner="pc", unit="$bn SMA book in run-off", cap=SMA_SLEEVE, cost=0.005, ig=0.0,
             apply=lambda lev, x: lev.__setitem__("sma_ro", x), step=2.0, note="C 5-8%/yr principal (G6)"),
        dict(key="cs_synd", owner="cs", unit="$bn sold down at 0.90", cap=0.25 * E.PRIV0["cs"],
             cost=(1 - P_CS) + 0.10, ig=P_CS, apply=lambda lev, x: lev.__setitem__("cs_synd", x), step=1.0,
             note="discount + 2%/yr carry x 5y (gap_02 amber convention)"),
        dict(key="ovl_im", owner="ovl", unit="$bn opportunistic IM released", cap=E.OPP_IM0,
             cost=0.15 * 0.0125 * E.NAV0 * 2 / E.OPP_IM0, ig=1.0,
             apply=lambda lev, x: lev.__setitem__("ovl_im", x), step=0.5,
             note="Sharpe 0.15 x 1.25% NAV vol x 2y forgone"),
        dict(key="p2s", owner="pm", unit="$bn DM converted to futures", cap=0.5 * E.LO0["dm"],
             cost=0.0055 * 5 * (0.998 - E.IM_N), ig=0.998 - E.IM_S - 0.117,
             apply=lambda lev, x: lev.__setitem__("p2s", x), step=2.0, slope_cap0=True,
             note="0.40-0.70%/yr per $ freed (GC2); counts in T2 net of stressed IM and P99 30d VM; "
                  "no T4' credit for exposure kept through the s* rebound"),
        dict(key="reserve_add", owner="cf", unit="$bn Treasury top-up from DM", cap=0.06 * E.NAV0, cost=0.075,
             ig=1.0, apply=lambda lev, x: lev.__setitem__("reserve_add", x), step=2.0,
             note="1.5%/yr buffer carry x 5y (gap_02)"),
        dict(key="rcf", owner="cf", unit="$bn committed revolver", cap=15.0, cost=0.009, ig=0.0,
             apply=lambda lev, x: lev.__setitem__("rcf", x), step=5.0, note="PIF $15bn precedent; SOFR+85bp"),
        dict(key="band", owner="own", unit="share of band (5% draw in crisis)", cap=1.0, cost=None, ig=0.0,
             apply=lambda lev, x: lev.__setitem__("band", x), step=1.0, note="0.065 per $ withheld (gap_02)"),
    ]
    return L


CARDS = [  # group decision cards priced in Phase II (sales excluded from Phase I)
    dict(key="sell_pe", owner="pe", bid=0.88, hold=0.95, size=0.5,
         apply=lambda lev, x: lev["red"].__setitem__("pe", x), name="PE: 2018 buyout fund (s4.4 example)"),
    dict(key="sell_sec", owner="sec", bid=0.87, hold=0.95, size=0.5,
         apply=lambda lev, x: lev["red"].__setitem__("sec", x), name="Secondaries: S3 LP interest"),
    dict(key="sell_co", owner="co", bid=0.75, hold=0.95, size=0.5,
         apply=lambda lev, x: lev["red"].__setitem__("co", x), name="Co-investment: strip"),
    dict(key="sell_hf", owner="pm", bid=P_HF, hold=0.95, size=0.5,
         apply=lambda lev, x: lev.__setitem__("hf_sell", x), name="Public Markets: HF secondary"),
]

STATES = {
    "R0": dict(label="t0, group levers + reserve (no revolver, no band)", allow={"rcf": 0.0, "band": 0.0}),
    "R0x": dict(label="t0, task lever list only (no reserve top-up)", allow={"rcf": 0.0, "band": 0.0,
                                                                           "reserve_add": 0.0}),
    "R1": dict(label="+ CF revolver signed (Mode B)", allow={"band": 0.0}),
    "R2": dict(label="+ owner band (Mode H)", allow={}),
    "I": dict(label="interim, reversible group levers only (before the revolver signs)",
              allow={"rcf": 0.0, "band": 0.0, "sma_sell": 0.0, "cs_synd": 0.0}, cards=False),
}


def coefficients(s: E.Stress, base_lev: dict | None = None) -> dict:
    """Finite-difference slopes of head_TPF(h), h = 1..24, per unit of each lever / card; t0 IG coefficients."""
    base_lev = base_lev or lev_of()
    b = gl_ladder(s, base_lev)
    h0 = b["head_tpf"][:H_ROWS].copy()
    out = dict(h0=h0, base=b, lever={}, card={}, cash=None, commit={})
    for L in levers(s):
        lv = copy.deepcopy(base_lev)
        L["apply"](lv, L["step"])
        r = gl_ladder(s, lv)
        sl = (r["head_tpf"][:H_ROWS] - h0) / L["step"]
        if L.get("slope_cap0"):
            sl = np.minimum(sl, 0.0)
        cost = L["cost"]
        if L["key"] == "band":
            cost = 0.065 * r["withheld24"] / L["step"]
        out["lever"][L["key"]] = dict(slope=sl, cost=cost, cap=L["cap"], owner=L["owner"], ig=L["ig"],
                                      unit=L["unit"], note=L["note"])
    for C in CARDS:
        lv = copy.deepcopy(base_lev)
        C["apply"](lv, C["size"])
        r = gl_ladder(s, lv)
        out["card"][C["key"]] = dict(slope=(r["head_tpf"][:H_ROWS] - h0) / C["size"], bid=C["bid"], hold=C["hold"],
                                     size=C["size"], owner=C["owner"], name=C["name"], ig=C["bid"])
    lv = copy.deepcopy(base_lev)
    lv["cash_t0"] = 1.0
    out["cash"] = (gl_ladder(s, lv)["head_tpf"][:H_ROWS] - h0)
    for g in W_NEW:
        lv = copy.deepcopy(base_lev)
        lv["new_commit"][g] = 1.0
        out["commit"][g] = -(gl_ladder(s, lv)["head_tpf"][:H_ROWS] - h0)   # headroom consumed per $1bn
    return out


IG_SHORT_T0 = 0.08 * E.NAV0 - (E.TRE0 - E.IM_N * E.N_SYN0 - E.OPP_IM0)   # 0.56: T2 8% target at t0


def _build(coef, state, elastic, relax=(0.0, 0.0), penalty_scale=1.0, phase1=False, cards_on=True):
    allow = STATES[state]["allow"]
    cards_on = cards_on and STATES[state].get("cards", True)
    keys = list(coef["lever"])
    x = {k: cp.Variable(nonneg=True, name=k) for k in keys}
    cks = list(coef["card"])
    s = {k: cp.Variable(nonneg=True, name=k) for k in cks}
    uS = cp.Variable(nonneg=True)
    uIG = cp.Variable(nonneg=True)
    head = [coef["h0"][h] + sum(coef["lever"][k]["slope"][h] * x[k] for k in keys)
            + sum(coef["card"][c]["slope"][h] * s[c] for c in cks) for h in range(H_ROWS)]
    ig = sum(coef["lever"][k]["ig"] * x[k] for k in keys) + sum(coef["card"][c]["ig"] * s[c] for c in cks)
    rows_h = [(head[h] + (uS if (elastic or phase1) else 0) >= -relax[0]) for h in range(H_ROWS)]
    row_ig = (ig + (uIG if (elastic or phase1) else 0) >= IG_SHORT_T0 - relax[1])
    cons = rows_h + [row_ig]
    for k in keys:
        cap = allow.get(k, coef["lever"][k]["cap"])
        cons.append(x[k] <= cap)
    cons.append(x["sma_sell"] + x["sma_ro"] <= SMA_SLEEVE)
    for c in cks:
        cons.append(s[c] <= (coef["card"][c]["size"] if (cards_on and not phase1) else 0.0))
    cost = sum(coef["lever"][k]["cost"] * x[k] for k in keys)
    obj = sum((coef["card"][c]["bid"] - coef["card"][c]["hold"]) * s[c] for c in cks) - cost
    if elastic:
        obj = obj - penalty_scale * (M_TIERS["S"] * uS + M_TIERS["IG"] * uIG)
    return x, s, uS, uIG, rows_h, row_ig, cons, obj


def phase1(coef, state):
    x, s, uS, uIG, rows_h, row_ig, cons, _ = _build(coef, state, elastic=False, phase1=True)
    cp.Problem(cp.Minimize(uS), cons).solve(solver=cp.HIGHS)
    u_s = max(0.0, float(uS.value))
    cp.Problem(cp.Minimize(uIG), cons + [uS <= u_s + 1e-9]).solve(solver=cp.HIGHS)
    u_ig = max(0.0, float(uIG.value))
    allow = STATES[state]["allow"]
    hstar = int(np.argmin([coef["h0"][h] + sum(coef["lever"][k]["slope"][h] * float(x[k].value) for k in x)
                           for h in range(H_ROWS)]))
    at_cap = [k for k in x if coef["lever"][k]["slope"][hstar] > 1e-9
              and abs(float(x[k].value) - allow.get(k, coef["lever"][k]["cap"])) < 1e-6
              and allow.get(k, coef["lever"][k]["cap"]) > 0]
    zero_by_convention = [k for k in x if coef["lever"][k]["slope"][hstar] <= 1e-9]
    iis = []
    if u_s > 1e-9:
        iis = [f"T4' row (binding month {hstar + 1})"] + [f"cap:{k} ({GROUP_NAME[coef['lever'][k]['owner']]})"
                                                           for k in at_cap]
        iis += [f"unavailable:{k}" for k, v in allow.items() if v == 0.0]
    return dict(u_S_star=u_s, u_IG_star=u_ig, hstar=hstar + 1, levers={k: float(v.value) for k, v in x.items()},
                iis=iis, no_relief=zero_by_convention)


def solve(coef, state, elastic, relax=(0.0, 0.0), penalty_scale=1.0):
    x, s, uS, uIG, rows_h, row_ig, cons, obj = _build(coef, state, elastic, relax, penalty_scale)
    prob = cp.Problem(cp.Maximize(obj), cons)
    prob.solve(solver=cp.HIGHS)
    mu = np.array([float(r.dual_value) for r in rows_h])
    sol = dict(status=prob.status, obj=float(prob.value), mu=mu, y_IG=float(row_ig.dual_value),
               x={k: float(v.value) for k, v in x.items()}, sell={k: float(v.value) for k, v in s.items()},
               u_S=float(uS.value) if elastic else 0.0, u_IG=float(uIG.value) if elastic else 0.0,
               penalty_scale=penalty_scale, relax=list(relax), elastic=elastic, state=state)
    sol["y_cash"] = float(mu @ coef["cash"]) + sol["y_IG"]
    sol["cards"] = cards(coef, sol)
    return sol


def cards(coef, sol):
    """Reservation price: SELL iff (bid - hold) + sum_h mu_h * slope_h + y_IG * bid >= 0. The slope contains
    bid * cash-relief plus the group-specific relief (e.g. unfunded assumed by the buyer)."""
    out = []
    for c, d in coef["card"].items():
        rel = d["slope"] - d["bid"] * coef["cash"]                      # per $ NAV, beyond proceeds
        y_rel = float(sol["mu"] @ rel)
        res = (d["hold"] - y_rel) / (1.0 + sol["y_cash"])
        out.append(dict(card=c, group=GROUP_NAME[d["owner"]], name=d["name"], bid=d["bid"], hold=d["hold"],
                        y_cash=sol["y_cash"], y_rel=y_rel, reservation_price=res,
                        action="SELL" if sol["sell"][c] > 1e-9 else "HOLD"))
    return out


def pinned_rows(sol, tol=1e-3):
    bad = []
    sc = sol["penalty_scale"]
    if sol["u_S"] > 1e-7 or float(sol["mu"].sum()) >= (1 - tol) * M_TIERS["S"] * sc:
        bad.append("T4'")
    if sol["u_IG"] > 1e-7 or sol["y_IG"] >= (1 - tol) * M_TIERS["IG"] * sc:
        bad.append("IG")
    return bad


def assert_no_penalty_pinned_duals(sol, tol=1e-3):
    bad = pinned_rows(sol, tol)
    if bad:
        raise AssertionError(f"group cards/envelopes priced off penalty-pinned rows: {bad}")


def restore_and_solve(coef, state):
    p1 = phase1(coef, state)
    relax = (p1["u_S_star"] + 1e-6 if p1["u_S_star"] > 0 else 0.0,
             p1["u_IG_star"] + 1e-6 if p1["u_IG_star"] > 0 else 0.0)
    hard = solve(coef, state, elastic=False, relax=relax)
    el1 = solve(coef, state, elastic=True, relax=relax, penalty_scale=1.0)
    el10 = solve(coef, state, elastic=True, relax=relax, penalty_scale=10.0)
    return dict(phase1=p1, restored=hard, restored_elastic_x1=el1, restored_elastic_x10=el10)


# ------------------------------------------------------------------------------------------------------------
# Group prices and envelopes - computed ONLY from a restored (or feasible original) solution
# ------------------------------------------------------------------------------------------------------------
def plan_lev(coef, sol, include_cards=True):
    lv = lev_of()
    for k, v in sol["x"].items():
        L = next(L for L in levers(coef["stress"]) if L["key"] == k)
        L["apply"](lv, v)
    if include_cards:
        for C in CARDS:
            C["apply"](lv, sol["sell"][C["key"]])
    return lv


def coefficients_for(s, role: str = "pricing"):
    """role = 'pricing' for the Tier-1 row that may price cards (T4' = s*(theta*)); 'reverse' for literal T4, the
    critic reading and other reverse stresses, which are reported but never written to cards or envelopes."""
    c = coefficients(s)
    c["stress"] = s
    c["role"] = role
    return c


def group_prices(coef, sol, priced_on: str, recovery_hash: str | None = None, d0: float | None = None) -> dict:
    """FTP charges, hurdles, envelopes and glide-path shares by group from a restored / feasible solution.
    Refuses to price off a pinned solution."""
    assert_no_penalty_pinned_duals(sol)
    if coef.get("role", "pricing") != "pricing":
        raise AssertionError("reverse stresses are reported, never used to price group cards or envelopes")
    if sol["elastic"] and (sol["u_S"] > 1e-7 or sol["u_IG"] > 1e-7):
        raise AssertionError("elastic slack in a pricing row: price only on the restored problem")
    s = coef["stress"]
    mu = sol["mu"]
    lv = plan_lev(coef, sol)
    r = gl_ladder(s, lv)
    hstar = int(np.argmin(r["head_tpf"][:H_ROWS]))
    out = {"priced_on": priced_on, "recovery_target_hash": recovery_hash, "binding_months": [
        int(h + 1) for h in np.where(mu > 1e-9)[0]], "y_cash_5y": sol["y_cash"], "y_IG_5y": sol["y_IG"],
        "mu_sum_5y": float(mu.sum()), "groups": {}}
    # relief delivered at the binding month by each owner's levers (for the glide-path allocation)
    relief = {}
    for k, v in sol["x"].items():
        o = coef["lever"][k]["owner"]
        relief[o] = relief.get(o, 0.0) + float(coef["lever"][k]["slope"][hstar] * v)
    for c, v in sol["sell"].items():
        o = coef["card"][c]["owner"]
        relief[o] = relief.get(o, 0.0) + float(coef["card"][c]["slope"][hstar] * v)
    tot_rel = sum(max(0.0, v) for v in relief.values())
    for g in PRIV:
        a, d = ALPHA_D[g]
        charge_new = float(mu @ coef["commit"][g]) + (sol["y_IG"] if g == "co" else 0.0)   # 5y PV per $
        nco_g = np.cumsum(r["gf"][g]["calls"] - r["gf"][g]["dist"])[:H_ROWS]
        charge_hold = float(mu @ nco_g) / E.PRIV0[g]                                        # 5y PV per $ NAV
        out["groups"][g] = dict(
            name=GROUP_NAME[g],
            envelope_12m=float(np.sum(r["gf"][g]["calls"][:12] - r["gf"][g]["dist"][:12])),
            envelope_24m=float(np.sum(r["gf"][g]["calls"][:24] - r["gf"][g]["dist"][:24])),
            pacing_bn_yr=12.0 * W_NEW[g] * (1 - lv["cut"][g]),
            ftp_new_bp_yr=1e4 * charge_new / 5.0, hurdle_bp_yr=1e4 * charge_new / d,
            ftp_hold_bp_yr=1e4 * charge_hold / 5.0,
            glide_share=(max(0.0, relief.get(g, 0.0)) / tot_rel) if tot_rel > 1e-9 else 0.0)
    ov = r["ovl"]
    out["groups"]["ovl"] = dict(name="Overlay", envelope_12m=float(np.sum((-ov["vm"] + ov["dim"] - ov["tail"] + ov["prem"]
                                                                          + ov["opp"] + ov["fut"])[:12])),
                                envelope_24m=float(np.sum((-ov["vm"] + ov["dim"] - ov["tail"] + ov["prem"]
                                                           + ov["opp"] + ov["fut"])[:24])),
                                glide_share=(max(0.0, relief.get("ovl", 0.0)) / tot_rel) if tot_rel > 1e-9 else 0.0)
    out["groups"]["pm"] = dict(name="Public Markets", cbc_tp_12m=float(r["comp"]["lo"][11] + r["comp"]["hf"][11]),
                               cbc_tp_24m=float(r["comp"]["lo"][23] + r["comp"]["hf"][23]),
                               glide_share=(max(0.0, relief.get("pm", 0.0)) / tot_rel) if tot_rel > 1e-9 else 0.0)
    out["groups"]["cf"] = dict(name="Corporate Finance", glide_share=(max(0.0, relief.get("cf", 0.0)) / tot_rel)
                               if tot_rel > 1e-9 else 0.0)
    out["groups"]["own"] = dict(name="Owner (band)", glide_share=(max(0.0, relief.get("own", 0.0)) / tot_rel)
                                if tot_rel > 1e-9 else 0.0)
    out["plan_ladder"] = dict(SH_TP=r["SH_TP"], SH_TPF=r["SH_TPF"], min_head=r["min_head_tpf_24"],
                              argmin=r["argmin_24"])
    out["relief_by_owner"] = relief
    out["d0"] = d0
    return out


def priced_on_flag(d0: float, u_star: float) -> str:
    """'restored_problem' whenever the current book fails a hard pricing row (execution deficit d0 > 0) or Phase I
    leaves a structural deficit u* > 0; prices then refer to the post-plan book named by the recovery hash."""
    return "restored_problem" if (u_star > 1e-9 or d0 > 1e-9) else "original_problem"


def recovery_hash(stress_name: str, sol: dict) -> str:
    blob = json.dumps({"stress": stress_name, "x": {k: round(v, 6) for k, v in sol["x"].items()},
                       "sell": {k: round(v, 6) for k, v in sol["sell"].items()}, "relax": sol["relax"]},
                      sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]
