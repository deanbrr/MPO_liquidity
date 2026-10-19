"""
ra_gap_01 ladder stage: deterministic T4' tables on the eight-group v2 book at the recalibrated theta*.
SYNTHETIC - NOT ADIC DATA.
Writes ra_ladder_results.json. Run: <venv>/python.exe -I -B ra_ladder_run.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra_book as B  # noqa: E402
import ra_ladder as RL  # noqa: E402

E = RL.E
CAL = json.load(open(os.path.join(HERE, "ra_calib_results.json"), encoding="utf-8"))
TH = {k: v["theta"] for k, v in CAL["theta_star"].items()}
TH_POOL = {k: v["pooled_theta"] for k, v in CAL["saa"].items()}
out = {"theta_star": TH, "theta_pooled": TH_POOL}


def pol(**kw):
    return E.Policy("x", **kw)


def ladder_rows(book, theta, census="v1", ra_opts=None):
    configs = {
        "do-nothing": RL.lev_of(reserve=0.08, book=book, census=census),
        "stage pacing rule": RL.lev_from_policy(pol(pace_cut=True), book=book, census=census),
        "owner band": RL.lev_from_policy(pol(band=True), book=book, census=census),
        "rule + band": RL.lev_from_policy(pol(pace_cut=True, band=True), book=book, census=census),
        "Mix A (rcf 15, pace 6 + rule, reserve 14%)": RL.lev_from_policy(pol(rcf=15.0, pace=6.0, pace_cut=True,
                                                                               reserve=0.14), book=book, census=census),
        "Mix B (rcf 10, rule, band, reserve 8%)": RL.lev_from_policy(pol(rcf=10.0, pace_cut=True, band=True,
                                                                         reserve=0.08), book=book, census=census),
    }
    rows = {}
    s = RL.s_star(theta)
    for k, lev in configs.items():
        r = RL.gl_ladder(s, lev, theta=theta, ra_opts=dict(ra_opts or {}))
        rows[k] = dict(SH_TP=r["SH_TP"], SH_TPF=r["SH_TPF"], min_head_24=r["min_head_tpf_24"], fac_need_24=r["fac_need_24"],
                       gstar=r["gstar"], nco24=r["nco24"])
    # revolver sized to the facility need
    fac = rows["do-nothing"]["fac_need_24"]
    r = RL.gl_ladder(s, RL.lev_of(reserve=0.08, book=book, census=census, rcf=fac), theta=theta, ra_opts=dict(ra_opts or {}))
    rows[f"revolver {fac:.1f}"] = dict(SH_TP=r["SH_TP"], SH_TPF=r["SH_TPF"], min_head_24=r["min_head_tpf_24"],
                                       fac_need_24=r["fac_need_24"], gstar=r["gstar"])
    return rows


# ---------------------------------------------------------------- 1. RA T4' row bridge
bridge = {}
for th_name, th in (("0.76", 0.76), ("theta*_v2u16", TH["v2u16"]), ("theta*_v2u11", TH["v2u11"])):
    rows = {}
    rows["G15 (published row)"] = RL.ra_leg(0.76, T=24, mode="g15", state="T4prime")
    rows["+ theta-indexed, RAME marks"] = RL.ra_leg(th, T=24, mode="canonical", state="T4prime",
                                                   opts=dict(availability=False, fund_module="off"))
    rows["+ fund-level module (waterfall)"] = RL.ra_leg(th, T=24, mode="canonical", state="T4prime",
                                                       opts=dict(availability=False))
    rows["+ lender availability, ext(theta) = canonical"] = RL.ra_leg(th, T=24, mode="canonical", state="T4prime")
    rows["axis: ext 0"] = RL.ra_leg(th, T=24, mode="canonical", state="T4prime", opts=dict(ext=0.0))
    rows["axis: ext 0.35"] = RL.ra_leg(th, T=24, mode="canonical", state="T4prime", opts=dict(ext=0.35))
    rows["axis: calls x1.0"] = RL.ra_leg(th, T=24, mode="canonical", state="T4prime", opts=dict(call_axis=1.0))
    rows["axis: fund module upper bound"] = RL.ra_leg(th, T=24, mode="canonical", state="T4prime",
                                                     opts=dict(fund_module="upper"))
    rows["canonical, no new RA commitments"] = RL.ra_leg(th, T=24, mode="canonical", state="T4prime",
                                                        commit_m=np.zeros(24))
    bridge[th_name] = {k: {"12m": RL.ra_summary(v, 12), "24m": RL.ra_summary(v, 24),
                           "true_change_12m": float(v["nav_true"][11] - v["nav_true"][0] + 0.0),
                           "rep_change_12m": float(v["nav_rep"][12] - 18.0)} for k, v in rows.items()}
    comp = B.ra_theta(th)
    bridge[th_name]["components"] = comp
out["ra_row_bridge"] = bridge
print("1. RA T4' row bridge (24m net):", {k: {kk: round(vv["24m"]["net"], 2) for kk, vv in v.items() if kk != "components"}
                                         for k, v in bridge.items()})

# ---------------------------------------------------------------- 2. ladder tables
tabs = {"v1 census v1.0 @0.76": ladder_rows("v1", 0.76), "v1 gc2 @0.76": ladder_rows("v1", 0.76, census="gap02")}
for book in ("v2u16", "v2u11"):
    tabs[f"{book} @0.76"] = ladder_rows(book, 0.76)
    tabs[f"{book} @theta*"] = ladder_rows(book, TH[book])
    tabs[f"{book} @pooled"] = ladder_rows(book, TH_POOL[book])
    tabs[f"{book} @theta* ext0"] = ladder_rows(book, TH[book], ra_opts=dict(ext=0.0))
    tabs[f"{book} @theta* G15 RA leg"] = ladder_rows(book, TH[book], ra_opts=dict(mode="g15"))
tabs["v1s (PE 52/16.4, no RA) @0.76"] = ladder_rows("v1s", 0.76)
out["ladder"] = tabs
for k, v in tabs.items():
    d = v["do-nothing"]
    print(f"2. {k:34s} SH_TP {d['SH_TP']} G* {d['gstar']:.2f} fac {d['fac_need_24']:.2f} | rule SH {v['stage pacing rule']['SH_TP']}"
          f" fac {v['stage pacing rule']['fac_need_24']:.2f} | band {v['owner band']['SH_TP']} | MixB SHTPF {v['Mix B (rcf 10, rule, band, reserve 8%)']['SH_TPF']}")


# ---------------------------------------------------------------- 3. Phase I / II and group prices
def recovery(book, theta, ra_opts=None, enr_hold=0.84):
    s = RL.s_star(theta)
    base = RL.lev_of(reserve=0.0, book=book, census="v1")
    coef = RL.coefficients(s, base, theta, ra_opts=ra_opts, enr_hold=enr_hold)
    d0 = float(max(0.0, -coef["h0"].min()))
    res = {"d0": d0, "states": {}, "levers": {}}
    for k, v in coef["lever"].items():
        sl24 = float(v["slope"][23])
        res["levers"][k] = dict(owner=RL.GROUP_NAME[v["owner"]], cap=v["cap"], cost=v["cost"], slope24=sl24,
                                cost_per_headroom=(v["cost"] / sl24 if (v["cost"] is not None and sl24 > 1e-9) else None))
    res["cash_slope24"] = float(coef["cash"][23])
    res["commit_slope24"] = {g: float(v[23]) for g, v in coef["commit"].items()}
    for st in ("R0x", "R0", "R1", "R2"):
        rr = RL.restore_and_solve(coef, st)
        h = rr["restored"]
        p1 = rr["phase1"]
        priced_on = "restored_problem" if (p1["u_S_star"] > 1e-9 or d0 > 1e-9) else "original_problem"
        gp = RL.group_prices(coef, h, base, priced_on, d0)
        res["states"][st] = dict(u_star=p1["u_S_star"], u_IG_star=p1["u_IG_star"], mu_sum=float(h["mu"].sum()),
                                 mu_months=[int(i + 1) for i in np.where(h["mu"] > 1e-9)[0]],
                                 mu_sum_x10=float(rr["restored_elastic_x10"]["mu"].sum()), y_IG=h["y_IG"],
                                 y_cash=h["y_cash"], x={k: v for k, v in h["x"].items() if v > 1e-6},
                                 sell={k: v for k, v in h["sell"].items() if v > 1e-6}, cards=h["cards"], prices=gp,
                                 cost_5y=-h["obj"])
    return res


rec = {}
for book in ("v2u16", "v2u11"):
    for tn, th in (("theta*", TH[book]), ("0.76", 0.76), ("pooled", TH_POOL[book])):
        rec[f"{book}|{tn}"] = recovery(book, th)
        r1, r0 = rec[f"{book}|{tn}"]["states"]["R1"], rec[f"{book}|{tn}"]["states"]["R0"]
        print(f"3. {book} {tn}: d0 {rec[f'{book}|{tn}']['d0']:.2f} | R1 mu {r1['mu_sum']:.4f} x {r1['x']} | "
              f"R0 mu {r0['mu_sum']:.4f} x {r0['x']} sell {r0['sell']}")
        for stn in ("R1", "R0"):
            g = rec[f"{book}|{tn}"]["states"][stn]["prices"]["groups"]
            print(f"   {stn}: FTP_hold RA {g['ra']['ftp_hold_bp_yr']:.1f}bp, hurdle RA {g['ra']['hurdle_bp_yr']:.0f}bp, "
                  f"B_RA24 {g['ra']['envelope_24m']:.2f}, B_RA12 {g['ra']['envelope_12m']:.2f}; PE FTP {g['pe']['ftp_hold_bp_yr']:.1f}")
            for c in rec[f"{book}|{tn}"]["states"][stn]["cards"]:
                if c["card"] in ("sell_enr", "sell_pe", "sell_ra_re"):
                    print(f"      card {c['card']}: res {c['reservation_price']:.3f} bid {c['bid']} -> {c['action']}")
rec["v2u16|theta*|ext0"] = recovery("v2u16", TH["v2u16"], ra_opts=dict(ext=0.0))
rec["v2u16|theta*|enr_hold0.95"] = recovery("v2u16", TH["v2u16"], enr_hold=0.95)
out["recovery"] = rec

# ---------------------------------------------------------------- 4. L4 pool row and budgets
l4 = {}
for book in ("v2u16", "v2u11"):
    th = TH[book]
    s = RL.s_star(th)
    r1 = rec[f"{book}|theta*"]["states"]["R1"]
    plan = RL.lev_of(book=book, census="v1")
    for k, v in r1["x"].items():
        L = next(L for L in RL.levers(s, book) if L["key"] == k)
        L["apply"](plan, v)
    for C in RL.cards(book):
        C["apply"](plan, r1["sell"].get(C["key"], 0.0))
    r0 = rec[f"{book}|theta*"]["states"]["R0"]
    plan0 = RL.lev_of(book=book, census="v1")
    for k, v in r0["x"].items():
        L = next(L for L in RL.levers(s, book) if L["key"] == k)
        L["apply"](plan0, v)
    for C in RL.cards(book):
        C["apply"](plan0, r0["sell"].get(C["key"], 0.0))
    cfgs = {"do-nothing": RL.lev_of(reserve=0.08, book=book, census="v1"),
            "minimum T4' plan R1 (revolver)": plan, "minimum T4' plan R0 (group levers)": plan0,
            "Mix A": RL.lev_from_policy(pol(rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14), book=book, census="v1"),
            "Mix B": RL.lev_from_policy(pol(rcf=10.0, pace_cut=True, band=True, reserve=0.08), book=book, census="v1")}
    l4[book] = {k: RL.pools_budgets(s, v, th) for k, v in cfgs.items()}
out["L4"] = l4
for book, d in l4.items():
    for k, v in d.items():
        print(f"4. {book} {k:32s} B_RA 24/12 {v['ra']['B24']:.2f}/{v['ra']['B12']:.2f}  B_PE {v['pe']['B24']:.2f}/{v['pe']['B12']:.2f}"
              f"  pool24 {v['pool']['24m']:.2f} slack24 {v['slack']['24m']:.2f}")

# ---------------------------------------------------------------- 5. L8 at t0 and on the T4' path
l8 = {}
for book in ("v1", "v1s", "v2u16", "v2u11"):
    l8[book] = B.l8(book)
for book in ("v2u16", "v2u11"):
    th = TH[book]
    r = RL.gl_ladder(RL.s_star(th), RL.lev_of(reserve=0.08, book=book, census="v1"), theta=th)
    ra = r["ra"]
    path = {}
    for mth in (0, 11, 23):
        row = r["rows"][mth]
        W_rep = row["nav"]
        W_true = row["nav"] - row["ra_nav_rep"] + row["ra_nav_true"]
        priv_rep = row["priv_rep"] + row["ra_nav_rep"]
        priv_true = row["priv_rep"] + row["ra_nav_true"]
        u = row["unf"]
        path[f"m{mth + 1}"] = dict(W_reported=W_rep, W_true_RA=W_true, private_reported=priv_rep,
                                   private_true_RA=priv_true, unfunded=u,
                                   ratio_reported=(priv_rep + u) / W_rep, ratio_true_RA=(priv_true + u) / W_true,
                                   headroom_reported=0.80 * W_rep - priv_rep - u,
                                   headroom_true_RA=0.80 * W_true - priv_true - u,
                                   ra_rep=row["ra_nav_rep"], ra_true=row["ra_nav_true"])
    l8[f"{book}|T4'path"] = path
    print(f"5. L8 on T4' path {book}:", {k: (round(v['ratio_reported'], 3), round(v['ratio_true_RA'], 3),
                                          round(v['headroom_reported'], 1)) for k, v in path.items()})
out["L8"] = l8

# ---------------------------------------------------------------- 6. T4' DVA divergence (deterministic)
dva = {}
for book in ("v2u16",):
    for th_name, th in (("theta*", TH[book]), ("0.76", 0.76)):
        r = RL.ra_leg(th, T=24, mode="canonical", state="T4prime")
        eq = np.zeros(24)
        eq[0] = -(0.30 + 0.10 * th)
        eq[12:24] = 0.02
        cash = r["net"]
        beta_true = float(sum(s["beta_eq"] * s["nav"] for s in B.SLEEVES) / 18.0)
        b_desm, b_obs = 0.80 * beta_true, 0.35 * beta_true
        res_ = {}
        for y, (a, b) in enumerate(((0, 12), (12, 24))):
            fb = lambda beta: float(np.prod(1 + beta * eq[a:b]) - 1)  # noqa: E731
            vT0 = float(r["nav_true"][a - 1]) if a > 0 else float(sum(r["per"][k]["nav_true"][0] for k in r["per"]))
            vA0 = float(r["nav_rep"][a - 1]) if a > 0 else 18.0
            vT1, vA1 = float(r["nav_true"][b - 1]), float(r["nav_rep"][b - 1])
            if a == 0:
                vT0 = sum(sl["nav"] / (1 - sl["ltv"]) / (1 + sl["g0"]) - sl["nav"] * sl["ltv"] / (1 - sl["ltv"])
                          for sl in B.SLEEVES)
            cy = float(cash[a:b].sum())
            res_[f"y{y + 1}"] = dict(
                dva_star_desm=vT1 - vT0 + cy - vT0 * fb(b_desm), dva_rep_obs=vA1 - vA0 + cy - vA0 * fb(b_obs),
                dva_rep_desm=vA1 - vA0 + cy - vA0 * fb(b_desm), dva_star_obs=vT1 - vT0 + cy - vT0 * fb(b_obs),
                true_change=vT1 - vT0, rep_change=vA1 - vA0, cash=cy, fb_desm=fb(b_desm), fb_obs=fb(b_obs))
        res_["beta"] = dict(true=beta_true, desm=b_desm, obs=b_obs)
        dva[f"{book}|{th_name}"] = res_
out["t4_dva_divergence"] = dva
print("6. T4' DVA divergence:", json.dumps(dva, indent=1)[:2500])

with open(os.path.join(HERE, "ra_ladder_results.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
