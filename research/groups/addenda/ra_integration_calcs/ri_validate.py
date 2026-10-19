"""
ri_validate: reproduction checks for the ra_integration_calcs copies. SYNTHETIC - NOT ADIC DATA.

1. Byte-identical copies: SHA-256 of the local copies against the originals (nothing was edited in the originals).
2. Ladder: local ra_ladder.gl_ladder (book v1, gap_02 split, RA off) == local g01_core.gl_ladder == local
   t1_engine.ladder on six readings x eight policies; published v1 T4' figures (SH_TP 17, G* 11.1, facility 13.9,
   pacing rule 6.1 / 20 months, band 0 / 29 months, d0 11.3).
3. ra_gap_01 v2 ladder figures from its stored results (v2u16 / v2u11 at their theta*; v1s at 0.76; d0).
4. G15 Real Assets row (V-RA-CF as a regression test): +0.40 / -0.16 / -1.32 / -2.46.
5. Monte Carlo: local ra_engine with Cfg.t1() == local t1_engine.simulate (3 policies x 3 models); local ra_engine
   (oil switches at their defaults) == ra_gap_01's stored integrated v2u16 results (M1 / M6, do-nothing / Mix B).
Run: <venv>/python.exe -I -B ri_validate.py  -> ri_validate_results.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ri_common as C  # noqa: E402
import ra_book as B  # noqa: E402
import ra_ladder as RL  # noqa: E402
import g01_core as G1  # noqa: E402
import ra_engine as R  # noqa: E402

E = RL.E
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))          # .../research
out = {"label": C.LABEL}

# ------------------------------------------------------------------ 1. hashes
pairs = {
    "t1_engine.py": os.path.join(ROOT, "addenda", "gap_02_calcs", "t1_engine.py"),
    "gap02_study.py": os.path.join(ROOT, "addenda", "gap_02_calcs", "gap02_study.py"),
    "phase1_demo.py": os.path.join(ROOT, "addenda", "gap_02_calcs", "phase1_demo.py"),
    "g7_liquidity_ladder_calcs.py": os.path.join(ROOT, "groups", "addenda", "G7_calcs", "g7_liquidity_ladder_calcs.py"),
    "rfta_v2_book.py": os.path.join(ROOT, "groups", "addenda", "gap_02_calcs", "rfta_v2_book.py"),
    "seal_history_results.json": os.path.join(ROOT, "groups", "addenda", "gap_02_calcs", "seal_history_results.json"),
    "sealed_pe_history_v1_1.csv": os.path.join(ROOT, "groups", "addenda", "gap_02_calcs", "sealed_pe_history_v1_1.csv"),
}
hashes = {}
for k, orig in pairs.items():
    a, b = C.sha256_file(os.path.join(HERE, k)), C.sha256_file(orig)
    hashes[k] = dict(sha256=a, identical_to_original=(a == b))
adapted = {k: C.sha256_file(os.path.join(HERE, k)) for k in ("g01_core.py", "gs_group_cashmap.py", "ra_book.py",
                                                            "ra_ladder.py", "ra_module.py", "ra_engine.py")}
out["copies"] = dict(byte_identical=hashes, adapted_sha256=adapted)
print("1. byte-identical copies:", {k: v["identical_to_original"] for k, v in hashes.items()})

# ------------------------------------------------------------------ 2. ladder reproduction
readings = {"s*(0.76)": RL.s_star(0.76), "s*(0.0)": RL.s_star(0.0), "s*(1.0)": RL.s_star(1.0),
            "T4 literal": RL.t4_literal(), "T4 8% floor": RL.t4_literal(floor=0.08),
            "critic": RL.t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0))}
pols = {"A": E.Policy("A"), "rcf15": E.Policy("r", rcf=15.0), "cut": E.Policy("c", pace_cut=True),
        "band": E.Policy("b", band=True), "mixA": E.Policy("mA", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
        "mixB": E.Policy("mB", rcf=10.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0),
        "navf": E.Policy("n", navf=2.0), "amber": E.Policy("am", amber_t0=3.0)}
maxdiff, mism = 0.0, []
for rn, s in readings.items():
    for pn, pol in pols.items():
        a = G1.gl_ladder(s, pol=pol)
        b = RL.gl_ladder(s, RL.lev_from_policy(pol, census="gap02", book="v1"))
        t = E.ladder(s, pol)
        d = float(np.max(np.abs(a["head_tpf"] - b["head_tpf"])))
        maxdiff = max(maxdiff, d, abs(t["gstar"] - b["gstar"]))
        if d > 1e-9 or a["SH_TP"] != b["SH_TP"] or t["SH_TP"] != b["SH_TP"]:
            mism.append((rn, pn, d, a["SH_TP"], b["SH_TP"], t["SH_TP"]))
out["ladder_reproduction"] = dict(max_abs_diff=maxdiff, mismatches=mism, cases=len(readings) * len(pols))
print("2a. ladder reproduction: max diff", maxdiff, "mismatches", mism)


def lad(book_key, theta, **pol_kw):
    bk = C.BOOKS[book_key]
    if pol_kw:
        lev = RL.lev_from_policy(E.Policy("x", **pol_kw), book=bk["rb_book"], census=bk["census"])
    else:
        lev = RL.lev_of(reserve=0.08, book=bk["rb_book"], census=bk["census"])
    return RL.gl_ladder(RL.s_star(theta), lev, theta=theta)


pub = {}
r = lad("v1pub", 0.76)
pub["do-nothing"] = dict(SH_TP=r["SH_TP"], gstar=round(r["gstar"], 2), fac=round(r["fac_need_24"], 2),
                         published=dict(SH_TP=17, gstar=11.1, fac=13.9))
r = lad("v1pub", 0.76, pace_cut=True)
pub["rule"] = dict(SH_TP=r["SH_TP"], fac=round(r["fac_need_24"], 2), published=dict(SH_TP=20, fac=6.1))
r = lad("v1pub", 0.76, band=True)
pub["band"] = dict(SH_TP=r["SH_TP"], fac=round(r["fac_need_24"], 2), published=dict(SH_TP=29, fac=0.0))
lv0 = RL.lev_of(reserve=0.0, book="v1", census="gap02")
d0 = max(0.0, -float(RL.gl_ladder(RL.s_star(0.76), lv0, theta=0.76)["head_tpf"][:24].min()))
pub["d0"] = dict(value=round(d0, 2), published=11.3)
out["published_v1_T4prime"] = pub
print("2b. published v1 T4':", pub)

# ------------------------------------------------------------------ 3. ra_gap_01 stored ladder values
ref_path = os.path.join(ROOT, "groups", "addenda", "ra_gap_01_calcs", "ra_ladder_results.json")
ref = json.load(open(ref_path, encoding="utf-8"))
cal_ref = json.load(open(os.path.join(ROOT, "groups", "addenda", "ra_gap_01_calcs", "ra_calib_results.json"),
                         encoding="utf-8"))
th16 = cal_ref["theta_star"]["v2u16"]["theta"]
th11 = cal_ref["theta_star"]["v2u11"]["theta"]
chk = {}
for name, bk, th, refkey in (("v2u16@theta*", "v2u16", th16, "v2u16 @theta*"), ("v2u11@theta*", "v2u11", th11,
                                                                                  "v2u11 @theta*"),
                             ("v1s@0.76", "v1", 0.76, "v1s (PE 52/16.4, no RA) @0.76")):
    rr = lad(bk, th)
    rf = ref["ladder"][refkey]["do-nothing"]
    chk[name] = dict(gstar=(rr["gstar"], rf["gstar"]), fac=(rr["fac_need_24"], rf["fac_need_24"]),
                     SH_TP=(rr["SH_TP"], rf["SH_TP"]),
                     identical=bool(abs(rr["gstar"] - rf["gstar"]) < 1e-9 and rr["SH_TP"] == rf["SH_TP"]))
for bk, th, rk in (("v2u16", th16, "v2u16|theta*"), ("v2u11", th11, "v2u11|theta*")):
    lv = RL.lev_of(reserve=0.0, book=bk, census="v1")
    d0v = max(0.0, -float(RL.gl_ladder(RL.s_star(th), lv, theta=th)["head_tpf"][:24].min()))
    chk[f"d0 {bk}"] = dict(value=d0v, ra_gap_01=ref["recovery"][rk]["d0"],
                           identical=bool(abs(d0v - ref["recovery"][rk]["d0"]) < 1e-6))
out["ra_gap_01_ladder"] = chk
print("3. ra_gap_01 ladder:", {k: v["identical"] for k, v in chk.items()})

# ------------------------------------------------------------------ 4. G15 RA row
g15 = {}
for st in ("normal", "drought", "T4prime"):
    rr = RL.ra_leg(0.76, T=24, mode="g15", state=st)
    g15[st] = {"12m": RL.ra_summary(rr, 12)["net"], "24m": RL.ra_summary(rr, 24)["net"]}
tgt = {"normal 12m": (g15["normal"]["12m"], 0.40), "drought 12m": (g15["drought"]["12m"], -0.16),
       "T4' 12m": (g15["T4prime"]["12m"], -1.32), "T4' 24m": (g15["T4prime"]["24m"], -2.46)}
out["V-RA-CF"] = {k: dict(engine=round(v[0], 3), g15=v[1], pass_=abs(round(v[0], 2) - v[1]) < 0.0051)
                  for k, v in tgt.items()}
print("4. V-RA-CF:", {k: (v["engine"], v["pass_"]) for k, v in out["V-RA-CF"].items()})

# ------------------------------------------------------------------ 5. Monte Carlo reproduction
keys = ("p_red", "mean_wtilde", "mean_commit_forgone", "mean_withheld", "w_inv2", "mean_fees")
mcp = {"dn": E.Policy("dn"), "mixA": E.Policy("mixA", **C.POLICY_KW["mixA"]),
       "mixB": E.Policy("mixB", **C.POLICY_KW["mixB"])}
rep = {}
for pk, pol in mcp.items():
    for mk in ("M1", "M4", "M6"):
        a = E.simulate(E.MODELS[mk], pol, n=3000)
        b = R.simulate(E.MODELS[mk], pol, R.Cfg.t1(), n=3000)
        rep[f"{pk}|{mk}"] = all(abs(a[k] - b[k]) < 1e-9 for k in keys)
out["mc_t1_reproduction_identical"] = dict(all=all(rep.values()), cases=rep)
print("5a. ra_engine Cfg.t1() == t1_engine.simulate:", all(rep.values()))
main_ref = json.load(open(os.path.join(ROOT, "groups", "addenda", "ra_gap_01_calcs", "ra_main_results.json"),
                          encoding="utf-8"))
rep2 = {}
for mk in ("M1", "M6"):
    for pk in ("dn", "mixB"):
        cfg = R.Cfg(track=True, players=frozenset(R.PLAYERS), trigger="current", book="v2u16", theta=th16)
        rr = R.simulate(E.MODELS[mk], mcp[pk], cfg, n=10000, seed=C.SEED)
        rf = main_ref["runs"][f"v2u16|{mk}|{pk}"]
        rep2[f"v2u16|{mk}|{pk}"] = dict(p_red=(rr["p_red"], rf["p_red"]), mean_w=(rr["mean_wtilde"], rf["mean_wtilde"]),
                                        identical=bool(abs(rr["p_red"] - rf["p_red"]) < 1e-12
                                                       and abs(rr["mean_wtilde"] - rf["mean_wtilde"]) < 1e-9))
out["mc_ra_gap_01_reproduction"] = rep2
print("5b. ra_engine copy == ra_gap_01 stored v2u16 runs:", {k: v["identical"] for k, v in rep2.items()})
C.save("ri_validate_results.json", out)
