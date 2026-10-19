"""
ri_cashmap (item 1): cross-group cash map, v1 (seven groups) versus v2 (eight groups, Real Assets carved from PE).

SYNTHETIC - NOT ADIC DATA.

Conventions (the published groups-report conventions, census v1.1 by default as recorded in context s1A):
  base (normal) and drought (today):
    * non-PE groups: the stream-G7 engine logic of GS_calcs/gs_group_cashmap.run on the census split (local copies),
      monthly steps; new commitments to Secondaries / Private Credit / Capital Solutions / Co-investment at 10% each
      of the $12bn plan, as published
    * PE funds: the RFT-TA v2 vintage engine (local copy of groups gap_02's rfta_v2_book.py) started from the sealed
      census v1.1 history (seal_history_results.json); for v2 the cohort NAVs are rescaled to $34bn and the cohort
      unfunded to $16.4bn (U16) or $10.9bn (U11); forward pace = the sealed 2026 pace x the unfunded scale (groups
      gap_02 convention: each history's own pace). A rate-leg variant (G7 rates on NAV, census rate leg) is kept
      for comparison and for the published v1.0 reproduction.
    * Real Assets (v2 only): G15's monthly sleeve engine (ra_ladder.ra_leg mode 'g15'), $1.2bn a year of new
      closed-end commitments (10% of the plan) - the published RA row (+0.40 normal, -0.16 drought at 12 months).
    * Overlay and Corporate Finance opex: unchanged between v1 and v2. Shown at the published reconciled 12-month
      values (+0.31 overlay; -0.18 opex; groups gap_03 s5), doubled for 24 months [I].
  T4' = s*(theta*): the deterministic ladder (local ra_ladder.gl_ladder, the exact replica of t1_engine.ladder,
    with the theta-indexed RA leg) at each book's own theta*; group flows over 12 and 24 months. Do-nothing book
    (8% Treasury top-up), canonical draws (10% of opening-fiscal-year NAV), canonical overlay conventions.
Run: <venv>/python.exe -I -B ri_cashmap.py  -> ri_cashmap_results.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ri_common as C  # noqa: E402
import gs_group_cashmap as gs  # noqa: E402  (local copy; loads the local unmodified stream-G7 module)
import rfta_v2_book as rb  # noqa: E402  (local byte-identical copy)
import ra_book as B  # noqa: E402
import ra_ladder as RL  # noqa: E402

g = gs.g
SEAL = json.load(open(os.path.join(HERE, "seal_history_results.json"), encoding="utf-8"))
REGMAP = {"normal": "N", "drought": "D", "crisis": "F", "boom": "O"}
UNF_CENSUS = dict(gs.UNF_CENSUS)                 # census v1.0 split; non-PE part unchanged in census v1.1
OVERLAY_RECON_12M = {"normal": 0.31, "drought": 0.31}   # groups synthesis s2.2 (reconciled, groups gap_03 s5)
CF_OPEX_12M = 0.001 * 177.0
PAYOUT = {"5%": 0.05, "7.5%": 0.075, "10%": 0.10}
LIQUID_BOOK = 71.0                                # Treasury 15 + Public Markets 56


# ------------------------------------------------------------------------------------------ vintage PE leg
def census_cohorts(commitments: dict, omega: dict) -> list:
    """Cohort objects at 2026-09-30 (copied from groups gap_02 gap02_rerun.census_cohorts)."""
    cohorts = []
    for s in rb.S_KEYS:
        for v in range(1998, 2027):
            c = commitments[2010] if v < 2010 else commitments[v]
            nq = 3 if v == 2026 else 4
            for qi in range(nq):
                qc = v * 4 + qi
                h = rb.unit_history(s, qc)
                U, V, age, ae = h["state"]
                amt = omega[s] * c * 0.25
                cohorts.append(rb.Cohort(s, qc, K=amt, U=U * amt, V=V * amt, age=age, ae=ae))
    return cohorts


class PEBook:
    """Sealed census v1.1 PE book (gap02_rerun.PEBook), with optional NAV / unfunded rescaling of every cohort."""

    def __init__(self, nav_scale: float = 1.0, unf_scale: float = 1.0):
        s = SEAL["sealed"]
        com = {int(k): v for k, v in s["commitments"].items()}
        self.omega = s["omega"]
        self.cohorts = census_cohorts(com, self.omega)
        for c in self.cohorts:
            c.V *= nav_scale
            c.U *= unf_scale
            c.K *= unf_scale
        self.pace = float(s["pace2026"]) * unf_scale

    @property
    def nav(self):
        return sum(c.V for c in self.cohorts)

    @property
    def unf(self):
        return sum(c.U for c in self.cohorts)

    def step_month(self, t: int, reg: str, call_mult: float, dist_zero: bool, mark: float, new_commit: float):
        r = REGMAP[reg]
        mC = (1.0 if r == "F" else rb.REG[r]["mC"])
        if new_commit > 0:
            for s in rb.S_KEYS:
                self.cohorts.append(rb.Cohort(s, 10_000 + t, K=self.omega[s] * new_commit))
        calls = dists = 0.0
        for c in self.cohorts:
            cl, d = c.step(r, 1.0 / 12.0, call_mult=call_mult, mC_override=mC, mD_override=None, dist_zero=dist_zero,
                           mark=mark)
            calls += cl
            dists += d
        return calls, dists


SEALED_NAV, SEALED_UNF = 52.0, float(SEAL["sealed"]["census"]["unf"])


def pe_scales(book: str, exact_unf: bool = True) -> tuple:
    rbk = B.BOOKS[C.BOOKS[book]["rb_book"]]
    sn = rbk["pe_nav"] / SEALED_NAV
    su = (rbk["pe_unf"] / SEALED_UNF) if exact_unf else 1.0
    return sn, su


# ------------------------------------------------------------------------------------------ normal / drought
def cashmap_run(scn: str, book: str, T: int = 12, pe_leg: str = "vintage", pe_pace: float | None = None,
                pe_nav: float | None = None, pe_unf: float | None = None, exact_unf: bool = True) -> dict:
    """gs_group_cashmap.run (census split) with the PE leg on the sealed vintage book (or G7 rates) and, for v2
    books, the Real Assets row from G15's engine. Returns $bn flows over the first T months."""
    rbk = B.BOOKS[C.BOOKS[book]["rb_book"]] if book != "v1pub" else B.BOOKS["v1"]
    has_ra = rbk["ra"]
    p = gs.paths(scn, 36)
    rates = gs.dist_table("census")
    bal = dict(g.BAL0)
    unf = dict(UNF_CENSUS)
    pe_nav = rbk["pe_nav"] if pe_nav is None else pe_nav
    pe_unf = rbk["pe_unf"] if pe_unf is None else pe_unf
    bal["pe"] = pe_nav
    unf["pe"] = pe_unf
    book_pe = None
    if pe_leg == "vintage":
        sn, su = (pe_nav / SEALED_NAV, (pe_unf / SEALED_UNF) if exact_unf else 1.0)
        book_pe = PEBook(sn, su)
        pace = book_pe.pace if pe_pace is None else pe_pace
        unf["pe"] = book_pe.unf
        bal["pe"] = book_pe.nav
        pe_state0 = dict(nav=float(book_pe.nav), unf=float(book_pe.unf))
    w_new = {"pe": (0.5 if has_ra else 0.6), "sec": 0.1, "pc": 0.1, "cs": 0.1, "co": 0.1}
    dist_g = {k: 0.0 for k in g.PRIVATE}
    calls_g = {k: 0.0 for k in g.PRIVATE}
    for t in range(T):
        reg = p["regime"][t]
        for gg in g.PRIVATE:
            bal[gg] *= 1 + p["priv_mark"][t]
        dist = {}
        for gg in g.PRIVATE:
            rate = rates[reg][gg]
            if p["dist_zero"][t] and gg in ("pe", "sec", "co"):
                rate = 0.0
            dist[gg] = g.monthly_rate(rate) * bal[gg]
        crate = g.monthly_rate(min(0.95, g.CALL[reg] * p["call_mult"][t]))
        calls = {k: crate * unf[k] for k in ("pe", "sec", "pc", "cs", "co")}
        calls["sec_def"] = (UNF_CENSUS["sec_def"] / 4.0) if t in (2, 5, 8, 11) else 0.0
        spike = p["rev_draw"][t] * UNF_CENSUS["pc_rev"]
        calls["pc_rev"] = min(unf["pc_rev"], spike if spike > 0 else crate * unf["pc_rev"])
        if book_pe is not None:
            c_pe, d_pe = book_pe.step_month(t, reg, p["call_mult"][t], bool(p["dist_zero"][t]), p["priv_mark"][t],
                                            pace / 12.0)
            calls["pe"], dist["pe"] = c_pe, d_pe
        nc = g.NEW_COMMIT_PA / 12.0
        for k, v in calls.items():
            unf[k] -= v
        for k, w in w_new.items():
            unf[k] += w * nc
        for gg in g.PRIVATE:
            add = calls[gg] + (calls["sec_def"] if gg == "sec" else 0.0) + (calls["pc_rev"] if gg == "pc" else 0.0)
            if gg == "pe" and book_pe is not None:
                bal["pe"] = book_pe.nav
            else:
                bal[gg] += add - dist[gg]
            calls_g[gg] += add
            dist_g[gg] += dist[gg]
    out = {"dist": dist_g, "calls": calls_g, "net": {k: dist_g[k] - calls_g[k] for k in g.PRIVATE}}
    if book_pe is not None:
        out["pe_pace"] = pace
        out["pe_t0"] = pe_state0
        out["pe_end"] = dict(nav=float(book_pe.nav), unf=float(book_pe.unf))
    if has_ra:
        ra = RL.ra_leg(None, T=max(T, 24), mode="g15", state=scn, commit_m=np.full(max(T, 24), 1.2 / 12.0))
        sm = RL.ra_summary(ra, T)
        out["dist"]["ra"] = sm["dist"]
        out["calls"]["ra"] = sm["calls"] + sm["cures"] + sm["prot_calls"]
        out["net"]["ra"] = sm["net"]
        out["ra_detail"] = sm
    out["private_net"] = float(sum(out["net"].values()))
    yrs = T / 12.0
    ovl = OVERLAY_RECON_12M[scn] * yrs
    opex = CF_OPEX_12M * yrs
    out["overlay_net"] = ovl
    out["cf_opex"] = -opex
    out["before_payout"] = out["private_net"] + ovl - opex
    out["liquid_funding"] = {k: v * 177.0 * yrs - out["before_payout"] for k, v in PAYOUT.items()}
    out["liquid_share"] = {k: v / LIQUID_BOOK for k, v in out["liquid_funding"].items()}
    return out


# ------------------------------------------------------------------------------------------ T4' (ladder)
def t4_groups(book: str, theta: float, T: int = 36, policy: str = "dn") -> dict:
    """Group flows of the canonical T4' ladder at theta (do-nothing book, 8% top-up)."""
    bk = C.BOOKS[book]
    pol_kw = C.POLICY_KW[policy]
    if policy == "dn":
        lev = RL.lev_of(reserve=0.08, book=bk["rb_book"], census=bk["census"])
    else:
        lev = RL.lev_from_policy(RL.E.Policy("x", **pol_kw), book=bk["rb_book"], census=bk["census"])
    r = RL.gl_ladder(RL.s_star(theta), lev, T=T, theta=theta)
    out = {}
    for h in (12, 24):
        grp = {}
        for gname, f in r["gf"].items():
            if gname == "ra" and not B.BOOKS[bk["rb_book"]]["ra"]:
                continue
            d, c = float(f["dist"][:h].sum()), float(f["calls"][:h].sum())
            grp[gname] = dict(dist=d, calls=c, net=d - c)
        ov = r["ovl"]
        ovl_net = float((ov["vm"] - np.maximum(ov["dim"], 0.0) + np.maximum(-ov["dim"], 0.0) + ov["tail"] - ov["prem"]
                         - ov["opp"] - ov["fut"])[:h].sum())
        draws = float(r["cf"]["draw"][:h].sum())
        opex = float(r["cf"]["opex"][:h].sum() + r["cf"]["fee"][:h].sum())
        priv = sum(v["net"] for v in grp.values())
        out[f"{h}m"] = dict(groups=grp, private_net=priv, overlay_net=ovl_net, cf_opex_fees=-opex,
                            before_payout=priv + ovl_net - opex, draws=draws,
                            liquid_funding_canonical_draws=draws - (priv + ovl_net - opex),
                            liquid_share=(draws - (priv + ovl_net - opex)) / LIQUID_BOOK,
                            overlay_detail={k: float(v[:h].sum()) for k, v in ov.items()})
    if r.get("ra") is not None:
        out["ra_24m_detail"] = RL.ra_summary(r["ra"], 24)
        out["ra_12m_detail"] = RL.ra_summary(r["ra"], 12)
    out["theta"] = theta
    out["SH_TP"], out["gstar"], out["fac_need_24"] = r["SH_TP"], r["gstar"], r["fac_need_24"]
    return out


def pe_relabel_rates(nav: float, unf: float, scn: str, T: int, commit_pa: float = 1.2) -> dict:
    """The same NAV and unfunded run through stream-G7 PE rates (what v1 implicitly assumed for the $18bn)."""
    nav_, unf_ = nav, unf
    d_ = c_ = 0.0
    rate = {"normal": 0.20, "drought": 0.11}[scn]
    cr = {"normal": 0.29, "drought": 0.28}[scn]
    for t in range(T):
        dd = g.monthly_rate(rate) * nav_
        cc = g.monthly_rate(cr) * unf_
        unf_ += commit_pa / 12.0 - cc
        nav_ += cc - dd
        d_ += dd
        c_ += cc
    return dict(dist=d_, calls=c_, net=d_ - c_)


def main():
    res = {"note": C.LABEL, "conventions": __doc__}
    theta = {b: C.theta_star(b) for b in ("v1pub",) + C.MAIN_BOOKS}
    res["theta_star"] = theta
    # ---------------- reproduction anchors (published v1)
    rep = {}
    gsr = json.load(open(os.path.normpath(os.path.join(HERE, "..", "GS_calcs", "gs_group_cashmap_results.json")),
                         encoding="utf-8"))
    for scn in ("normal", "drought"):
        mine = cashmap_run(scn, "v1pub", 12, pe_leg="rate", pe_nav=52.0, pe_unf=27.4)
        ref = gsr["runs"][f"census|{scn}"]["net_by_group"]
        rep[f"census_v1.0_rate|{scn}"] = dict(max_abs_diff=max(abs(mine["net"][k] - ref[k]) for k in ref),
                                              private_net=mine["private_net"])
        mine = cashmap_run(scn, "v1", 12, pe_leg="vintage", exact_unf=False)
        rr = json.load(open(os.path.normpath(os.path.join(HERE, "..", "gap_02_calcs", "gap02_rerun_results.json")),
                            encoding="utf-8"))["cashmap"][f"sealed|{scn}"]["net_by_group"]
        rep[f"sealed_v1.1_vintage|{scn}"] = dict(max_abs_diff=max(abs(mine["net"][k] - rr[k]) for k in rr),
                                                 pe_net=mine["net"]["pe"], private_net=mine["private_net"])
    t4p = t4_groups("v1pub", 0.76)
    rep["T4prime_v1pub_0.76_12m"] = {k: round(v["net"], 2) for k, v in t4p["12m"]["groups"].items()}
    rep["T4prime_v1pub_0.76_24m_private"] = round(t4p["24m"]["private_net"], 2)
    rep["T4prime_v1pub_0.76_overlay_12m_24m"] = (round(t4p["12m"]["overlay_net"], 2), round(t4p["24m"]["overlay_net"], 2))
    res["reproduction"] = rep
    # ---------------- main cash map
    cm = {}
    for book in C.MAIN_BOOKS:
        cm[book] = {}
        for scn in ("normal", "drought"):
            for T in (12, 24):
                cm[book][f"{scn}|{T}m"] = cashmap_run(scn, book, T, pe_leg="vintage")
                cm[book][f"{scn}|{T}m|rate_leg"] = cashmap_run(scn, book, T, pe_leg="rate")
                rbk = B.BOOKS[C.BOOKS[book]["rb_book"]]
                plan_pe = 12.0 * (0.5 if rbk["ra"] else 0.6)
                cm[book][f"{scn}|{T}m|vintage_plan_pace"] = cashmap_run(scn, book, T, pe_leg="vintage",
                                                                        pe_pace=plan_pe)
        cm[book]["T4prime@theta*"] = t4_groups(book, theta[book])
        cm[book]["T4prime@0.76"] = t4_groups(book, 0.76)
    res["cashmap"] = cm
    # relabel comparison: the RA NAV and unfunded at PE rates (v1's implicit assumption)
    res["ra_at_pe_rates"] = {f"{scn}|{T}m": pe_relabel_rates(18.0, 4.0, scn, T) for scn in ("normal", "drought")
                             for T in (12, 24)}
    # ---------------- deltas v2 - v1 (12 / 24 months)
    dl = {}
    for b2 in ("v2u16", "v2u11"):
        for key in ("normal|12m", "normal|24m", "drought|12m", "drought|24m"):
            a, b = cm["v1"][key], cm[b2][key]
            dl[f"{b2}-v1|{key}"] = dict(private_net=b["private_net"] - a["private_net"],
                                        pe=b["net"]["pe"] - a["net"]["pe"], ra=b["net"].get("ra", 0.0))
        for th in ("T4prime@theta*", "T4prime@0.76"):
            for h in ("12m", "24m"):
                a, b = cm["v1"][th][h], cm[b2][th][h]
                dl[f"{b2}-v1|{th}|{h}"] = dict(private_net=b["private_net"] - a["private_net"],
                                               pe=b["groups"]["pe"]["net"] - a["groups"]["pe"]["net"],
                                               ra=b["groups"].get("ra", {}).get("net", 0.0),
                                               before_payout=b["before_payout"] - a["before_payout"])
    res["deltas"] = dl
    C.save("ri_cashmap_results.json", res)
    # ---------------- console
    print("theta*", {k: round(v, 4) for k, v in theta.items()})
    print("reproduction", json.dumps(rep, default=float))
    for book in C.MAIN_BOOKS:
        for key in ("normal|12m", "drought|12m", "normal|24m", "drought|24m"):
            r = cm[book][key]
            print(book, key, {k: round(v, 2) for k, v in r["net"].items()}, "private", round(r["private_net"], 2),
                  "liquid@7.5%", round(r["liquid_funding"]["7.5%"], 2))
        for th in ("T4prime@theta*", "T4prime@0.76"):
            for h in ("12m", "24m"):
                r = cm[book][th][h]
                print(book, th, h, {k: round(v["net"], 2) for k, v in r["groups"].items()}, "private",
                      round(r["private_net"], 2), "ovl", round(r["overlay_net"], 2), "before", round(r["before_payout"], 2),
                      "liquid", round(r["liquid_funding_canonical_draws"], 2))


if __name__ == "__main__":
    main()
