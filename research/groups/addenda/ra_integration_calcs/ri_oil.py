"""
ri_oil (item 4): oil sensitivity - the change in the oil-crisis-state shortfall from the Real Assets oil loadings,
with and without the oil-linked natural-resource (ENR) exposure. SYNTHETIC - NOT ADIC DATA.

A. Deterministic named state OC ("Tier-1 oil-crisis state", G12 dossier s6.9; RA synthesis s6.3), on the local
   ladder (ra_ladder.gl_ladder with the inert-by-default `paths` / `ra_override` hooks):
     Brent -45% from the curve over six months, then $40-50 for 18 months; equities flat (-5% sensitivity); exits as
     today (PE / Secondaries / Co-investment at the ladder's drought rates); fund calls unchanged (28%, x1.0);
     Private Credit / Capital Solutions at drought cash rates (no credit crisis); draws at the 10% cap for two fiscal
     years on opening NAV, then 7.5%; no private marks; no VM, IM 4% (no crisis); no equity-tail monetisation; no
     opportunistic loss (trend and carry are right-way in a glut, RA s9.3) [I]; hedge funds noticed at t0, no gate;
     canonical T+P haircuts; revolver credit 0.80 (0.50 sensitivity).
   Real Assets OC leg (monthly, G15 sleeve mechanics; 'off' = every sleeve in G15's drought state, which reproduces
   the published RA drought row exactly):
     ENR sub-sleeves (RA s9.3 / G12 split; ENR_CE = levered upstream 0.80 + fee midstream 0.40 + other 0.40;
     ENR_DIR = levered upstream 0.27 + royalties 0.18 + fee midstream 0.45):
       cash multipliers on normal-state income (G12 s6.9, SG column): levered upstream 0 (RBL cash sweep; its cure is
       booked separately), royalties 0.63, fee midstream 0.95, other 0.90 [I]; ENR exits x0.30 of drought (G15 SG),
       levered upstream exits 0; true equity marks (G12 OC) levered upstream -65%, royalties -30%, midstream -10%,
       other -20% [I] over six months, reported through RAME (lambda 0.5, one-quarter lag);
       RBL cure on levered upstream at the SG/DB tail used for the Tier-1 reserve (RA s9.3 item 5): CVaR95 = 41% of
       levered equity (P90 32%; conditional-on-call mean floor $0.20bn total as variants); fund-held cures are
       protective calls capped at $0.26bn of unfunded; timing 70% in months 6-11 and 30% in months 12-17 [I];
       direct non-upstream ENR debt refinances at LTV^max 0.40 (0.55 - 5pp - 10pp in SG/DB, RA s5).
     GCC real estate: G15's supply-glut state (income x0.95 then x0.85; exits x0.5; marks -3/-4/-4/-3% at months
       6/12/18/24; true value -10% then -15%; normal lender terms).
     Infrastructure midstream (energy_link): 10% of each infrastructure sleeve; income x0.95, mark -10%.
   Variants: RA oil loadings off; on (ENR + GCC + midstream = 'with ENR'); on without the ENR exposure (ENR sleeves
   oil-neutral in the drought state; GCC + midstream on); ENR only. Shortfall measures: 24-month net cash outflow
   that Treasury + Public Markets must fund (NCO24), the T+P funding gap G*_OC (max_h [NCO + floor - CBC_TP]),
   24-month headroom and facility need. Also v1 (no RA) and the joint OCxDB reading (T4' at theta* plus the RA
   oil increments), and a closed-form first-order estimate of the delta for cross-checking.
B. Stochastic cross-check: the playbook-free engine (ri_mc 't1'), 50,000 paths, with the RA oil channels on / ENR
   oil-neutral / all RA oil channels off (ra_module switches): P(red), G* (24-month action-free gap) on wrong-way
   paths (supply glut or demand bust within 8 quarters).
Run: <venv>/python.exe -I -B ri_oil.py  -> ri_oil_results.json
"""
from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ri_common as C  # noqa: E402
import ra_book as B  # noqa: E402
import ra_ladder as RL  # noqa: E402

E = RL.E
T = 36
OC_SUB = {"ENR_CE": {"lev_up": 0.80, "mid": 0.40, "other": 0.40},
          "ENR_DIR": {"lev_up": 0.27, "roy": 0.18, "mid": 0.45}}
OC_INC = {"lev_up": 0.0, "roy": 0.63, "mid": 0.95, "other": 0.90}
OC_TRUE = {"lev_up": -0.65, "roy": -0.30, "mid": -0.10, "other": -0.20}
OC_EXIT_ENR = 0.30
INF_MID_SHARE, INF_MID_INC, INF_MID_TRUE = 0.10, 0.95, -0.10
RBL_SHARE = {"cvar95": 0.41, "p90": 0.32}
RBL_FLOOR_TOTAL = 0.20
RBL_FUND_CAP = 0.26
ENR_LTV_OC = 0.40
GCC_SG_MARKS = {5: -0.03, 11: -0.04, 17: -0.04, 23: -0.03}
LAM_ENR, LAG_ENR_Q = 0.50, 1
LAM_INF, LAG_INF_Q = 0.85, 1


def _monthly(r):
    return 1.0 - (1.0 - min(max(r, 0.0), 0.99)) ** (1.0 / 12.0)


def _ramp(total, months, t):
    return total * min(1.0, (t + 1) / months)


def _rame_marks(v_total, months_ramp, lam, lag_q, T_=T):
    """Cumulative reported mark (fraction of t0 value) by month from a true ramp to v_total over months_ramp,
    observed quarterly through a Geltner filter (lambda, lag in quarters); booked at quarter ends."""
    nq = T_ // 3 + 1
    lv = [1.0 + v_total * min(1.0, (3 * q) / months_ramp) for q in range(nq + 1)]
    r_true = [lv[q] / lv[q - 1] - 1.0 for q in range(1, nq + 1)]
    r_l = [0.0] * lag_q + r_true
    prev, lvl = 0.0, 1.0
    cum = np.zeros(T_)
    for q in range(nq):
        prev = lam * prev + (1 - lam) * r_l[q]
        lvl *= 1 + prev
        m = 3 * (q + 1) - 1
        if m < T_:
            cum[m:] = lvl - 1.0
    return cum


def ra_oc_leg(enr_on=True, gcc_on=True, mid_on=True, rbl="cvar95", commit_pa=1.2, scale=1.0) -> dict:
    """Monthly Real Assets cash in the OC state ('on' channels) or in G15's drought state (all off)."""
    keys = ("income", "realiz", "calls", "prot_calls", "cures", "dist_stop", "nav_loss", "nav_rep", "nav_true",
            "debt", "unf", "shortfall_fund", "cashout", "rbl")
    agg = {k: np.zeros(T) for k in keys}
    per = {}
    for sl in B.SLEEVES:
        sid, sec = sl["id"], sl["sector"]
        nav = sl["nav"] * scale
        unf = sl["unf"] * scale
        ltv0 = sl["ltv"]
        debt = nav * ltv0 / (1 - ltv0)
        is_enr, is_gcc, is_inf = sec == "ENR", sec == "RE_GCC", sec == "INF"
        on_enr, on_gcc, on_mid = is_enr and enr_on, is_gcc and gcc_on, is_inf and mid_on
        sub = OC_SUB.get(sid, {})
        nav0 = nav
        # income multiplier, exit factor and true / reported marks for the oil-exposed part
        if on_enr:
            m_inc = sum(v * OC_INC[k] for k, v in sub.items()) / sum(sub.values())
            up_share = sub.get("lev_up", 0.0) / sum(sub.values())
            x_exit = OC_EXIT_ENR * (1 - up_share)
            v_true = sum(v * OC_TRUE[k] for k, v in sub.items()) / sum(sub.values())
            rep_cum = _rame_marks(v_true, 6, LAM_ENR, LAG_ENR_Q)
            # direct non-upstream debt goes through the maturity module at the OC LTV^max
            nonup_debt_share = (1 - up_share) if sl["direct"] else 0.0
            tv_nonup = (sum(v * OC_TRUE[k] for k, v in sub.items() if k != "lev_up")
                        / max(sum(v for k, v in sub.items() if k != "lev_up"), 1e-12))
        else:
            m_inc, x_exit, v_true, up_share, rep_cum, nonup_debt_share, tv_nonup = 1.0, 1.0, 0.0, 0.0, np.zeros(T), 0.0, 0.0
        if on_mid:
            m_inc = 1 - INF_MID_SHARE * (1 - INF_MID_INC)
            rep_cum = INF_MID_SHARE * _rame_marks(INF_MID_TRUE, 6, LAM_INF, LAG_INF_Q)
        # RBL cure schedule (levered upstream; on only)
        rbl_m = np.zeros(T)
        prot_m = np.zeros(T)
        if on_enr and sub.get("lev_up", 0.0) > 0:
            lev_eq = sub["lev_up"] * scale
            if rbl == "floor":
                tot_lev = sum(OC_SUB[k].get("lev_up", 0.0) for k in OC_SUB)
                amt = RBL_FLOOR_TOTAL * sub["lev_up"] / tot_lev * scale
            else:
                amt = RBL_SHARE[rbl] * lev_eq
            if not sl["direct"]:
                amt = min(amt, RBL_FUND_CAP * scale)
            sched = np.zeros(T)
            sched[6:12] = 0.70 / 6
            sched[12:18] = 0.30 / 6
            if sl["direct"]:
                rbl_m = amt * sched
            else:
                prot_m = amt * sched
        rows = {k: np.zeros(T) for k in keys}
        mark_dollars = np.zeros(T)
        for t in range(T):
            # reported NAV: G15 drought appreciation on the cash base; marks tracked separately (reported overlay)
            nav *= 1.0 + sl["g_n"] / 12.0
            if on_gcc:
                inc_f = 0.95 if t < 12 else 0.85
                real = 0.5 * sl["real_d"]
                mark_dollars[t] = (mark_dollars[t - 1] if t > 0 else 0.0) + nav0 * GCC_SG_MARKS.get(t, 0.0)
                tv = _ramp(-0.10, 12, t) + (_ramp(-0.05, 12, t - 12) if t >= 12 else 0.0)
            else:
                inc_f = m_inc if t < 24 else 1.0
                real = sl["real_d"] * (x_exit if t < 24 else 1.0)
                mark_dollars[t] = nav0 * rep_cum[t] if (on_enr or on_mid) else 0.0
                tv = 0.0
            inc = sl["inc"] * inc_f * nav / 12.0
            rea = _monthly(real) * nav
            call = _monthly(0.28) * unf
            unf -= call
            unf += sl["commit"] * commit_pa / 12.0
            prot = min(prot_m[t], unf)
            unf -= prot
            cure = 0.0
            if sl["direct"] and debt > 0:
                d_m = debt * B.MATURITY_PA / 12.0
                if on_enr:
                    d_nonup = d_m * nonup_debt_share
                    v_m = d_nonup / ltv0 * (1.0 + tv_nonup * min(1.0, (t + 1) / 6.0))
                    cure = max(0.0, d_nonup - ENR_LTV_OC * v_m) if t < 24 else 0.0
                    cure += rbl_m[t]
                else:
                    v_m = d_m / ltv0 * (1.0 + tv)
                    cure = max(0.0, d_m - B.LTV_N[sec] * v_m)
                debt -= cure
            nav += call + cure + prot - rea
            rows["income"][t], rows["realiz"][t], rows["calls"][t] = inc, rea, call
            rows["prot_calls"][t], rows["cures"][t] = prot, cure
            rows["rbl"][t] = rbl_m[t] + prot
            rows["nav_rep"][t] = nav + mark_dollars[t]
            rows["nav_true"][t] = nav + nav0 * (v_true * min(1.0, (t + 1) / 6.0) if on_enr else 0.0)
            rows["debt"][t], rows["unf"][t] = debt, unf
        per[sid] = rows
        for k in keys:
            agg[k] += rows[k]
    agg["net"] = agg["income"] + agg["realiz"] - agg["dist_stop"] + agg["cashout"] - agg["calls"] \
        - agg["prot_calls"] - agg["cures"]
    agg["per"] = per
    agg["comp"] = None
    return agg


def oc_stress(eq_vertex=0.0, fac_credit=0.80):
    s = E.Stress(name="OC (Tier-1 oil-crisis state)", eq_drawdown=-eq_vertex if eq_vertex < 0 else 0.0,
                 dist_mult_pe=((24, 1.0),), pc_cs_rates=(0.10, 0.07), call_mult=((24, 1.0),),
                 draw_rates=(0.10, 0.10, 0.075), draw_basis="opening_reset", override_y2=0.0, fac_credit=fac_credit,
                 navf_ltv=0.05, hf_pass=0.83, floor=0.04, crisis_months=0, priv_marks=(), im_months=12,
                 instant=True)
    eq = np.zeros(T)
    eq[0] = eq_vertex
    paths = dict(eq=eq, fi=np.zeros(T), hf=np.r_[0.3 * eq_vertex, np.zeros(T - 1)], pm=np.zeros(T),
                 opp=np.zeros(T))
    return s, paths


def oc_ladder(book, ra_leg=None, eq_vertex=0.0, fac_credit=0.80, policy="dn"):
    bk = C.BOOKS[book]
    s, paths = oc_stress(eq_vertex, fac_credit)
    if policy == "dn":
        lev = RL.lev_of(reserve=0.08, book=bk["rb_book"], census=bk["census"])
    else:
        lev = RL.lev_from_policy(E.Policy("x", **C.POLICY_KW[policy]), book=bk["rb_book"], census=bk["census"])
    r = RL.gl_ladder(s, lev, T=T, theta=None, paths=paths, ra_override=ra_leg)
    head = r["head_tpf"][:24]
    out = dict(nco12=float(r["nco"][11]), nco24=float(r["nco"][23]), gstar=float(r["gstar"]),
               min_head_tpf_24=float(head.min()), head_m12=float(head[11]), head_m24=float(head[23]),
               fac_need_24=float(r["fac_need_24"]), SH_TP=r["SH_TP"],
               draws24=float(r["cf"]["draw"][:24].sum()), nav24=float(r["nav"][23]), floor24=float(r["floor"][23]))
    if ra_leg is not None:
        out["ra_net12"] = float(ra_leg["net"][:12].sum())
        out["ra_net24"] = float(ra_leg["net"][:24].sum())
        out["ra_rbl24"] = float(ra_leg["rbl"][:24].sum())
        out["ra_nav_rep24"] = float(ra_leg["nav_rep"][23])
    out["groups_net24"] = {g: float(f["dist"][:24].sum() - f["calls"][:24].sum()) for g, f in r["gf"].items()}
    return out


def dcr_sgps(book, ra_leg=None, pol=None):
    """T8's 12-month stressed distribution-coverage ratio in the supply-glut-with-peg-stress state (SG+PS), adapted
    from gap02_study.dcr_t0 (local byte-identical copy) to any book [I]: the PE / Secondaries / Co-investment
    distribution term uses the book's NAV, the call term the book's non-RA unfunded (x0.28 x1.25), fund
    commitments 90% (v1) or 80% (v2) of the plan; for v2 the Real Assets 12-month OC distributions, calls (x1.25,
    as the DCR convention) and cures (incl. RBL) come from the RA leg. With book 'v1pub' it reproduces dcr_t0."""
    pol = pol or E.Policy("A")
    bk = C.BOOKS[book]
    rbk = B.BOOKS[bk["rb_book"]]
    nav = E.NAV0
    enc = E.IM_N * E.N_SYN0 + E.OPP_IM0
    top = max(0.0, pol.reserve * nav - (E.TRE0 - enc))
    dm = E.LO0["dm"] - top / 0.998
    num = (6.0 + top) + 4.0 * 0.97 + 5.0 * 0.90 - enc + dm * (1 - 0.20) + E.LO0["em"] * 0.65 + E.LO0["fi"] * 0.90 \
        + E.HF0 * 0.5 + 0.80 * pol.rcf
    priv = B.book_priv(bk["rb_book"])
    if book == "v1pub":
        u_nonra = sum(E.UNF0.values()) + E.SEC_DEF0 + E.PC_REV0
    else:
        ub = B.book_unf(bk["rb_book"])
        u_nonra = sum(ub[g] for g in ("pe", "sec", "co", "cs", "pc")) + B.SEC_DEF_V1 + B.PC_REV_V1
    num += 0.45 * 0.10 * (priv["pe"] + priv["sec"] + priv["co"]) + 0.10 * priv["pc"] + 0.07 * priv["cs"] + 0.5
    fund_share = 0.8 if rbk["ra"] else 0.9
    den = (0.05 if pol.band else 0.10) * nav + 0.28 * 1.25 * u_nonra + 0.10 * pol.pace \
        + 0.28 * 0.5 * fund_share * pol.pace + (0.08 * E.N_SYN0 + 0.6)
    ra_terms = {}
    if rbk["ra"] and ra_leg is not None:
        ra_d = float((ra_leg["income"] + ra_leg["realiz"] - ra_leg["dist_stop"])[:12].sum())
        ra_c = 1.25 * float(ra_leg["calls"][:12].sum())
        ra_k = float((ra_leg["cures"] + ra_leg["prot_calls"])[:12].sum())
        num += ra_d
        den += ra_c + ra_k
        ra_terms = dict(dist12=ra_d, calls12_x125=ra_c, cures12=ra_k)
    return dict(dcr=num / den, resources=num, needs=den, shortfall=max(0.0, den - num), ra=ra_terms,
                u_nonra=u_nonra)


def first_order(variant="with_enr", rbl="cvar95"):
    """Closed-form first-order delta of the 24-month RA cash drain (OC on minus drought), $bn [I]:
    dS = sum_j V_j y_s (1 - m_j) x 2 + V_CE real_d [1 - 0.3 (1 - up_CE)] x 2 + C_RBL
         + V_GCC y_GCC (0.05 + 0.15) + V_INF 0.10 y_INF 0.05 x 2  (+ small direct-ENR maturity cures, ignored)."""
    sl = {s["id"]: s for s in B.SLEEVES}
    d = 0.0
    if variant in ("with_enr", "enr_only"):
        for sid, sub in OC_SUB.items():
            y = sl[sid]["inc"]
            d += sum(v * y * (1 - OC_INC[k]) * 2 for k, v in sub.items())
        up_ce = OC_SUB["ENR_CE"]["lev_up"] / 1.6
        d += 1.6 * sl["ENR_CE"]["real_d"] * (1 - OC_EXIT_ENR * (1 - up_ce)) * 2
        if rbl == "floor":
            d += RBL_FLOOR_TOTAL
        else:
            d += RBL_SHARE[rbl] * OC_SUB["ENR_DIR"]["lev_up"] + min(RBL_SHARE[rbl] * OC_SUB["ENR_CE"]["lev_up"],
                                                                  RBL_FUND_CAP)
    if variant in ("with_enr", "without_enr"):
        d += sl["RE_DIR_GCC"]["nav"] * sl["RE_DIR_GCC"]["inc"] * (0.05 + 0.15)
        d += sum(sl[k]["nav"] for k in ("INF_OE", "INF_CE", "INF_DIR")) * INF_MID_SHARE * 0.05 * 2 \
            * np.mean([sl[k]["inc"] for k in ("INF_OE", "INF_CE", "INF_DIR")])
    return float(d)


# ------------------------------------------------------------------------------------------ B. stochastic
N_ST = 50000


def _st_job(args):
    book, mk, pk, oil_enr, oil_gcc = args
    import ra_engine as R
    bk = C.BOOKS[book]
    has_ra = R.RB.BOOKS[bk["rb_book"]]["ra"]
    cfg = R.Cfg(init="gap02", groups="rate", overlay="t1", links=False, stage="t1",
                census=("gc2" if bk["census"] == "gap02" else "v1"),
                players=(frozenset(R.PLAYERS) if has_ra else frozenset(R.PLAYERS9)), trigger="none",
                book=bk["rb_book"], theta=C.theta_star(book), ra_notices=False, ra_jv=False, ra_cashout=False,
                enr_sell=0.0, ra_oil_enr=oil_enr, ra_oil_gcc=oil_gcc)
    r = R.simulate(R.E.MODELS[mk], R.E.Policy(pk, **C.POLICY_KW[pk]), cfg, n=N_ST, seed=C.SEED)
    ww = r["_wrongway"]
    g = r["_gstar"]
    red = r["_red"]
    w = r["_w"]
    eps24 = 1 - (1 - 0.01) ** (8 / 20)
    return args, dict(p_red=float(red.mean()), p_ww=float(ww.mean()), p_red_ww=float(red[ww].mean()),
                      p_red_notww=float(red[~ww].mean()), gstar_p996=float(np.quantile(g, 1 - eps24)),
                      gstar_mean_ww=float(g[ww].mean()), gstar_p99_ww=float(np.quantile(g[ww], 0.99)),
                      gstar_mean_all=float(g.mean()), w_mean_ww=float(w[ww].mean()), w_mean=float(w.mean()),
                      oil_delta_t0=(float(r["ra"]["oil_delta_t0"]) if "ra" in r else 0.0))


def main():
    out = {"note": C.LABEL, "conventions": __doc__}
    # ---------------- validation: the 'off' leg reproduces G15's drought row
    off = ra_oc_leg(enr_on=False, gcc_on=False, mid_on=False)
    g15d = RL.ra_leg(None, T=24, mode="g15", state="drought", commit_m=np.full(24, 1.2 / 12))
    out["validate_off_equals_G15_drought"] = dict(off12=float(off["net"][:12].sum()), g15_12=RL.ra_summary(g15d, 12)["net"],
                                                  off24=float(off["net"][:24].sum()), g15_24=RL.ra_summary(g15d, 24)["net"])
    legs = {"off": off,
            "with_enr": ra_oc_leg(True, True, True),
            "without_enr": ra_oc_leg(False, True, True),
            "enr_only": ra_oc_leg(True, False, False),
            "with_enr|rbl_p90": ra_oc_leg(True, True, True, rbl="p90"),
            "with_enr|rbl_floor": ra_oc_leg(True, True, True, rbl="floor")}
    out["ra_leg_24m"] = {k: dict(net12=float(v["net"][:12].sum()), net24=float(v["net"][:24].sum()),
                                 income24=float(v["income"][:24].sum()), realiz24=float(v["realiz"][:24].sum()),
                                 calls24=float(v["calls"][:24].sum()), prot24=float(v["prot_calls"][:24].sum()),
                                 cures24=float(v["cures"][:24].sum()), rbl24=float(v["rbl"][:24].sum()),
                                 nav_rep12=float(v["nav_rep"][11]), nav_rep24=float(v["nav_rep"][23]),
                                 by_sleeve_net24={s: float((p["income"] + p["realiz"] - p["calls"] - p["prot_calls"]
                                                            - p["cures"])[:24].sum()) for s, p in v["per"].items()})
                         for k, v in legs.items()}
    # ---------------- A. deterministic OC ladder
    oc = {}
    for book in C.MAIN_BOOKS:
        has_ra = B.BOOKS[C.BOOKS[book]["rb_book"]]["ra"]
        if not has_ra:
            oc[f"{book}|no RA"] = oc_ladder(book)
            oc[f"{book}|no RA|eq-5%"] = oc_ladder(book, eq_vertex=-0.05)
            continue
        for k, leg in legs.items():
            oc[f"{book}|{k}"] = oc_ladder(book, leg)
        oc[f"{book}|off|eq-5%"] = oc_ladder(book, legs["off"], eq_vertex=-0.05)
        oc[f"{book}|with_enr|eq-5%"] = oc_ladder(book, legs["with_enr"], eq_vertex=-0.05)
        oc[f"{book}|without_enr|eq-5%"] = oc_ladder(book, legs["without_enr"], eq_vertex=-0.05)
    out["oc_ladder"] = oc
    dl = {}
    for book in ("v2u16", "v2u11"):
        for v in ("with_enr", "without_enr", "enr_only", "with_enr|rbl_p90", "with_enr|rbl_floor"):
            a, b = oc[f"{book}|off"], oc[f"{book}|{v}"]
            dl[f"{book}|{v}"] = dict(d_nco12=b["nco12"] - a["nco12"], d_nco24=b["nco24"] - a["nco24"],
                                     d_gstar=b["gstar"] - a["gstar"], d_head24=b["min_head_tpf_24"] - a["min_head_tpf_24"],
                                     d_ra_net24=b["ra_net24"] - a["ra_net24"],
                                     d_draws24=b["draws24"] - a["draws24"], d_floor24=b["floor24"] - a["floor24"])
        for v in ("with_enr", "without_enr"):
            a, b = oc[f"{book}|off|eq-5%"], oc[f"{book}|{v}|eq-5%"]
            dl[f"{book}|{v}|eq-5%"] = dict(d_nco24=b["nco24"] - a["nco24"], d_gstar=b["gstar"] - a["gstar"])
        dl[f"{book}-v1|off"] = dict(d_nco24=oc[f"{book}|off"]["nco24"] - oc["v1|no RA"]["nco24"],
                                    d_gstar=oc[f"{book}|off"]["gstar"] - oc["v1|no RA"]["gstar"])
        dl[f"{book}-v1|with_enr"] = dict(d_nco24=oc[f"{book}|with_enr"]["nco24"] - oc["v1|no RA"]["nco24"],
                                         d_gstar=oc[f"{book}|with_enr"]["gstar"] - oc["v1|no RA"]["gstar"])
    for book in ("v2u16", "v2u11"):
        for v in ("with_enr", "without_enr", "enr_only"):
            a, b = oc[f"{book}|off"], oc[f"{book}|{v}"]
            dl[f"{book}|{v}"].update(d_head_m12=b["head_m12"] - a["head_m12"], d_head_m24=b["head_m24"] - a["head_m24"])
    out["oc_deltas"] = dl
    # T8 DCR in SG+PS (12 months): reproduction of gap02_study.dcr_t0 on the published book, then v1 / v2
    import gap02_study as S2
    dcr = {"v1pub|repro": dict(mine=dcr_sgps("v1pub")["dcr"], gap02=S2.dcr_t0(E.Policy("A"), "SG+PS"))}
    for pk in ("dn", "mixB"):
        pol = E.Policy(pk, **C.POLICY_KW[pk])
        dcr[f"v1|{pk}"] = dcr_sgps("v1", None, pol)
        for book in ("v2u16", "v2u11"):
            for v in ("off", "with_enr", "without_enr", "enr_only"):
                dcr[f"{book}|{v}|{pk}"] = dcr_sgps(book, legs[v], pol)
    out["dcr_sgps"] = dcr
    out["first_order"] = {f"{v}|{rb}": first_order(v, rb) for v in ("with_enr", "without_enr", "enr_only")
                          for rb in ("cvar95", "p90", "floor")}
    # facility-credit 0.50 sensitivity on the facility need (only matters if the OC row breaches)
    out["oc_fac_credit_050"] = {b: oc_ladder(b, legs["with_enr"] if B.BOOKS[C.BOOKS[b]["rb_book"]]["ra"] else None,
                                             fac_credit=0.50)["fac_need_24"] for b in C.MAIN_BOOKS}
    # ---------------- OCxDB: T4' at theta* plus the RA oil increments (v2), ladder
    ocdb = {}
    for book in ("v2u16", "v2u11"):
        th = C.theta_star(book)
        bk = C.BOOKS[book]
        lev = RL.lev_of(reserve=0.08, book=bk["rb_book"], census=bk["census"])
        base = RL.gl_ladder(RL.s_star(th), lev, theta=th)
        ra_t4 = base["ra"]
        for v in ("with_enr", "without_enr"):
            inc_leg = {k: (ra_t4[k] if not isinstance(ra_t4[k], np.ndarray) else ra_t4[k].copy())
                       for k in ra_t4 if k not in ("per", "comp")}
            on, off_ = legs[v], legs["off"]
            # add the OC-minus-drought RA increments that T4' does not already carry: RBL cures (protective calls
            # and direct cures) and the ENR / GCC distribution cut beyond T4''s own sector multipliers
            comp = base["ra"]["comp"]
            t4_enr_inc = comp["inc"]["ENR"]
            if v == "with_enr":      # RBL cures only (direct ENR cure; fund-held cure as a protective call)
                extra_cures = on["per"]["ENR_DIR"]["rbl"].copy()
                extra_prot = on["per"]["ENR_CE"]["prot_calls"].copy()
            else:
                extra_cures, extra_prot = np.zeros(T), np.zeros(T)
            d_inc = np.zeros(T)
            for sid in ("ENR_CE", "ENR_DIR"):
                po, pf = on["per"][sid], off_["per"][sid]
                if v == "with_enr":
                    # OC cash multiplier over the 24 stressed months; T4' already cuts ENR income to comp["inc"] and
                    # exits to 0.45(1 - theta) of drought (below OC's), and GCC income below OC's, so only the
                    # further ENR income cut and the RBL cures are added
                    m_oc = po["income"][:24].sum() / max(pf["income"][:24].sum(), 1e-12)
                    m_extra = max(0.0, t4_enr_inc - m_oc) / max(t4_enr_inc, 1e-12)
                    d_inc[:24] += m_extra * ra_t4["per"][sid]["income"][:24]
            inc_leg["income"] = ra_t4["income"] - d_inc
            inc_leg["cures"] = ra_t4["cures"] + extra_cures
            inc_leg["prot_calls"] = ra_t4["prot_calls"] + extra_prot
            inc_leg["net"] = inc_leg["income"] + inc_leg["realiz"] - inc_leg["dist_stop"] + inc_leg["cashout"] \
                - inc_leg["calls"] - inc_leg["prot_calls"] - inc_leg["cures"]
            r = RL.gl_ladder(RL.s_star(th), lev, theta=th, ra_override=inc_leg)
            ocdb[f"{book}|{v}"] = dict(gstar=float(r["gstar"]), fac_need_24=float(r["fac_need_24"]), SH_TP=r["SH_TP"],
                                       d_gstar_vs_T4prime=float(r["gstar"] - base["gstar"]),
                                       d_fac_vs_T4prime=float(r["fac_need_24"] - base["fac_need_24"]),
                                       T4prime_gstar=float(base["gstar"]), T4prime_fac=float(base["fac_need_24"]))
    out["oc_x_db"] = ocdb
    # ---------------- B. stochastic cross-check
    jobs = []
    for book in ("v1", "v2u16", "v2u11"):
        has_ra = B.BOOKS[C.BOOKS[book]["rb_book"]]["ra"]
        variants = [(True, True), (False, True), (False, False)] if has_ra else [(True, True)]
        for mk in C.MODELS:
            for pk in ("dn", "mixB"):
                for oe, og in variants:
                    jobs.append((book, mk, pk, oe, og))
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=23) as ex:
        st = dict(ex.map(_st_job, jobs, chunksize=1))
    out["stochastic_secs"] = time.time() - t0
    out["stochastic"] = {f"{b}|{mk}|{pk}|enr{int(oe)}|gcc{int(og)}": v for (b, mk, pk, oe, og), v in st.items()}
    sd = {}
    for book in ("v2u16", "v2u11"):
        for mk in C.MODELS:
            for pk in ("dn", "mixB"):
                on = st[(book, mk, pk, True, True)]
                ne = st[(book, mk, pk, False, True)]
                no = st[(book, mk, pk, False, False)]
                sd[f"{book}|{mk}|{pk}"] = dict(
                    d_p_red_pp_all_oil=100 * (on["p_red"] - no["p_red"]),
                    d_p_red_pp_enr=100 * (on["p_red"] - ne["p_red"]),
                    d_p_red_ww_pp_all_oil=100 * (on["p_red_ww"] - no["p_red_ww"]),
                    d_gstar_mean_ww_all_oil=on["gstar_mean_ww"] - no["gstar_mean_ww"],
                    d_gstar_mean_ww_enr=on["gstar_mean_ww"] - ne["gstar_mean_ww"],
                    d_gstar_p99_ww_all_oil=on["gstar_p99_ww"] - no["gstar_p99_ww"],
                    d_gstar_p996_all_oil=on["gstar_p996"] - no["gstar_p996"],
                    d_w_mean_ww_all_oil=on["w_mean_ww"] - no["w_mean_ww"], p_ww=on["p_ww"])
    out["stochastic_deltas"] = sd
    C.save("ri_oil_results.json", out)
    # ---------------- console
    print("validate off == G15 drought:", out["validate_off_equals_G15_drought"])
    for k, v in out["ra_leg_24m"].items():
        print(f"RA leg {k:22s} net12 {v['net12']:+.3f} net24 {v['net24']:+.3f} rbl24 {v['rbl24']:.3f} "
              f"income24 {v['income24']:.3f} realiz24 {v['realiz24']:.3f} navrep24 {v['nav_rep24']:.2f}")
    for k, v in oc.items():
        print(f"OC {k:32s} NCO12 {v['nco12']:6.2f} NCO24 {v['nco24']:6.2f} G* {v['gstar']:7.2f} head24 "
              f"{v['min_head_tpf_24']:6.2f} fac {v['fac_need_24']:.2f} SH_TP {v['SH_TP']}")
    for k, v in dl.items():
        print("delta", k, {kk: round(vv, 3) for kk, vv in v.items()})
    print("first order", {k: round(v, 3) for k, v in out["first_order"].items()})
    print("DCR SG+PS", {k: (round(v["dcr"], 4) if "dcr" in v else v) for k, v in dcr.items()})
    print("OCxDB", ocdb)
    for k, v in sd.items():
        if "|M1|" in k or "|M6|" in k:
            print("stoch", k, {kk: round(vv, 4) for kk, vv in v.items()})


if __name__ == "__main__":
    main()
