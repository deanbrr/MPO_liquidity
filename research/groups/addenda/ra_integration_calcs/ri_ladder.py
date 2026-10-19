"""
ri_ladder (item 2): committed-facility need under T4' = s*(theta*), survival on Treasury + Public Markets and the
T4' hard-row gap, v1 (seven groups) versus v2 (eight groups). SYNTHETIC - NOT ADIC DATA.

Engine: local ra_ladder.gl_ladder, the exact replica of gap_02's t1_engine.ladder (groups gap_01 g01_core), with the
theta-indexed Real Assets leg of ra_gap_01 (canonical mode: RAME marks, lender availability a(theta), extension
0.35(1 - theta), fund-level refinancing module). Canonical conventions (gap_02 s1.1): vertex shock, draws 10% of
opening-fiscal-year NAV with annual reset, revolver credited at 80% from month 2, 4% hard floor, hedge funds noticed
at t0 (crisis pass-through 0.83), overlay $10bn synthetic beta, tail monetisation, opportunistic loss 1.5% of NAV.
Readings per book at its own theta* (ri_calib) and at the common theta 0.76:
  do-nothing (8% top-up); stage-triggered pacing rule (new commitments cut to 25% from month 3 in crisis, every
  group incl. Real Assets); owner band (5% draws in crisis); rule + band; Mix A; Mix B; revolver sized to the need.
  SH_TP / SH_TPF = first month the T+P (+F) headroom turns negative; facility = max 24-month gap / 0.80.
  d0 (hard-row gap) = max(0, -min_h headroom_TPF(h)), h <= 24, with nothing signed and no top-up.
  u* = Phase-I structural deficit over group-tagged reversible levers (R0: no revolver, no band).
Run: <venv>/python.exe -I -B ri_ladder.py  -> ri_ladder_results.json
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ri_common as C  # noqa: E402
import ra_book as B  # noqa: E402
import ra_ladder as RL  # noqa: E402

E = RL.E


def lev_for(book, policy="dn", **extra):
    bk = C.BOOKS[book]
    if policy == "dn":
        return RL.lev_of(reserve=0.08, book=bk["rb_book"], census=bk["census"], **extra)
    if policy == "none_no_topup":
        return RL.lev_of(reserve=0.0, book=bk["rb_book"], census=bk["census"], **extra)
    return RL.lev_from_policy(E.Policy("x", **C.POLICY_KW[policy]), book=bk["rb_book"], census=bk["census"], **extra)


def reading(book, theta, ra_opts=None):
    s = RL.s_star(theta)
    rows = {}
    for pk in ("dn", "rule", "band", "rule_band", "mixA", "mixB"):
        r = RL.gl_ladder(s, lev_for(book, pk), theta=theta, ra_opts=dict(ra_opts or {}))
        rows[pk] = dict(SH_TP=r["SH_TP"], SH_TPF=r["SH_TPF"], min_head_tpf_24=r["min_head_tpf_24"],
                        fac_need_24=r["fac_need_24"], gstar=r["gstar"], nco24=r["nco24"], argmin=r["argmin_24"])
    fac = rows["dn"]["fac_need_24"]
    r = RL.gl_ladder(s, lev_for(book, "dn", rcf=fac), theta=theta, ra_opts=dict(ra_opts or {}))
    rows["revolver_sized"] = dict(rcf=fac, SH_TP=r["SH_TP"], SH_TPF=r["SH_TPF"], min_head_tpf_24=r["min_head_tpf_24"])
    r0 = RL.gl_ladder(s, lev_for(book, "none_no_topup"), theta=theta, ra_opts=dict(ra_opts or {}))
    rows["d0"] = max(0.0, -float(r0["head_tpf"][:24].min()))
    rows["d0_month"] = int(np.argmin(r0["head_tpf"][:24]) + 1)
    rows["SH_TP_no_topup"] = r0["SH_TP"]
    return rows


def phase1(book, theta):
    bk = C.BOOKS[book]
    s = RL.s_star(theta)
    base = RL.lev_of(reserve=0.0, book=bk["rb_book"], census=bk["census"])
    coef = RL.coefficients(s, base, theta)
    res = {"d0": float(max(0.0, -coef["h0"].min()))}
    for st in ("R0x", "R0", "R1"):
        p1 = RL.phase1(coef, st)
        res[st] = dict(u_star=p1["u_S_star"], levers={k: v for k, v in p1["levers"].items() if v > 1e-6})
    return res


def main():
    th = {b: C.theta_star(b) for b in ("v1pub",) + C.MAIN_BOOKS}
    cal = C.load("ri_calib_results.json") or {}
    th_pool = {b: cal.get("saa", {}).get(b, {}).get("pooled_theta") for b in th}
    out = {"note": C.LABEL, "conventions": __doc__, "theta_star": th, "theta_pooled": th_pool, "readings": {},
           "phase1": {}, "L8_t0": {}, "bridge": {}}
    for b in ("v1pub",) + C.MAIN_BOOKS:
        out["readings"][f"{b}@theta*"] = reading(b, th[b])
        out["readings"][f"{b}@0.76"] = reading(b, 0.76)
        if th_pool.get(b):
            out["readings"][f"{b}@pooled"] = reading(b, th_pool[b])
        out["phase1"][f"{b}@theta*"] = phase1(b, th[b])
        out["L8_t0"][b] = B.l8(C.BOOKS[b]["rb_book"])
    for b in ("v2u16", "v2u11"):
        out["readings"][f"{b}@theta*|RA leg G15 (reproduction mode)"] = reading(b, th[b], ra_opts=dict(mode="g15"))
        out["readings"][f"{b}@theta*|RA extension 0"] = reading(b, th[b], ra_opts=dict(ext=0.0))
        out["readings"][f"{b}@theta*|RA calls x1.0"] = reading(b, th[b], ra_opts=dict(call_axis=1.0))
    # ---------------- bridge: published v1 -> census v1.1 -> carve-out (U16) -> U11 rescale
    def g(key, pk="dn", f="fac_need_24"):
        return out["readings"][key][pk][f] if f != "d0" else out["readings"][key]["d0"]
    for f in ("fac_need_24", "gstar", "d0"):
        steps = [("v1 published (census v1.0 split, theta 0.76)", g("v1pub@theta*", f=f)),
                 ("v1 on census v1.1 at common theta 0.76", g("v1@0.76", f=f)),
                 ("v1 on census v1.1 at its own theta*", g("v1@theta*", f=f)),
                 ("v2 U16 at theta 0.76 (carve-out, same theta)", g("v2u16@0.76", f=f)),
                 ("v2 U16 at its own theta*", g("v2u16@theta*", f=f)),
                 ("v2 U11 at its own theta*", g("v2u11@theta*", f=f))]
        out["bridge"][f] = steps
    out["ra_carveout_effect"] = {
        f"{f}|{tn}": g(f"v2u16@{tn}", f=f) - g(f"v1@{tn}", f=f) for f in ("fac_need_24", "gstar", "d0")
        for tn in ("0.76", "theta*")}
    C.save("ri_ladder_results.json", out)
    print("theta*", {k: round(v, 4) for k, v in th.items()}, "pooled", th_pool)
    for k, v in out["readings"].items():
        d = v["dn"]
        print(f"{k:48s} G* {d['gstar']:6.2f} SH_TP {d['SH_TP']} fac {d['fac_need_24']:6.2f} | rule SH {v['rule']['SH_TP']} "
              f"fac {v['rule']['fac_need_24']:5.2f} | band SH {v['band']['SH_TP']} fac {v['band']['fac_need_24']:.2f} | "
              f"rule+band SH {v['rule_band']['SH_TP']} | MixA SHTPF {v['mixA']['SH_TPF']} head {v['mixA']['min_head_tpf_24']:.1f}"
              f" | MixB SHTPF {v['mixB']['SH_TPF']} head {v['mixB']['min_head_tpf_24']:.1f} | d0 {v['d0']:.2f}")
    for k, v in out["phase1"].items():
        print("phase1", k, {s: round(v[s]["u_star"], 3) for s in ("R0x", "R0", "R1")}, "d0", round(v["d0"], 2))
    print("L8", {k: (round(v["ratio"], 3), round(v["headroom"], 1)) for k, v in out["L8_t0"].items()})
    print("carve-out effect (v2u16 - v1)", {k: round(v, 2) for k, v in out["ra_carveout_effect"].items()})


if __name__ == "__main__":
    main()
