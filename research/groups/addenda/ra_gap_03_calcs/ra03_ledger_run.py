"""RA gap 03, step 2: total-portfolio oil-delta ledger at spot-equivalent (front-month-equivalent) delta.

SYNTHETIC - NOT ADIC DATA. The book is working allocation v2 (context s1A) with the G15 RA census; sector shares
are public-index anchors ([S]) or design defaults ([I]). Every delta is the dollar value change for a +1% shock to
the generator's slow oil factor x (the curve moving by the generator's impulse response 0.6^(m/12)), divided by
the as-of front month (Dec-26 Brent, $105.92). Barrels are reported at:
  * the canonical current state: the 15-Oct-2026 strip (NYMEX BZ settlements) and today's NAVs;
  * the SG and DB states: the generator's month-12 state-conditional curves (median slow factor of paths in that
    state at Oct-2027, the E1 curve with the state's expected drifts, plus the as-of tenor premium), with NAVs
    re-marked to those curves.

Usage: python -I ra03_ledger_run.py <gen_results_json> <g15_data_dir> <out_json>
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra03_lib as L  # noqa: E402

NAV_TOTAL = 177.0
M = 360
BETA_M = L.impulse_x(M)


# ------------------------------------------------------------------------------------------------ curves
def e1_curve(x: float, z: int, PZm: np.ndarray, M: int = M) -> np.ndarray:
    """Median curve ln F(m) = ln70 + phi^m (x - ln70) + sum_i phi^(m-i) (P^i mu)_z / 12 (G12 E1, monthly)."""
    phi = 1.0 - L.KM
    out = np.empty(M + 1)
    Pi = np.eye(6)
    acc = 0.0
    out[0] = x
    for m in range(1, M + 1):
        Pi = Pi @ PZm
        acc = phi * acc + (Pi @ L.MU_Z)[z] / 12.0
        out[m] = L.LN70 + phi ** m * (x - L.LN70) + acc
    return np.exp(out)


def gcc_regression(g15_dir: str) -> dict:
    """UAE residential property prices (BIS via FRED QAEN628BIS) on Brent (FRED DCOILBRENTEU quarterly averages):
    4-quarter log changes, Brent at lags 0-2 quarters, Newey-West (4) errors."""
    def load(fn, col):
        out = {}
        with open(os.path.join(g15_dir, fn), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    out[row["observation_date"]] = float(row[col])
                except (ValueError, KeyError):
                    pass
        return out
    uae = load("fred_QAEN628BIS_uae_resi_prices.csv", "QAEN628BIS")
    br = load("fred_DCOILBRENTEU_quarterly_avg.csv", "DCOILBRENTEU")
    dates = sorted(set(uae) & set(br))
    lu = np.log([uae[d] for d in dates])
    lb = np.log([br[d] for d in dates])
    res = {}
    dy_all = lu[4:] - lu[:-4]
    dx_all = lb[4:] - lb[:-4]
    for lag in (0, 1, 2):
        y = dy_all[lag:]
        x = dx_all[:len(dx_all) - lag]
        X = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        # Newey-West, 4 lags
        Xe = X * e[:, None]
        S = Xe.T @ Xe
        for l in range(1, 5):
            w = 1 - l / 5
            G = Xe[l:].T @ Xe[:-l]
            S += w * (G + G.T)
        XtXi = np.linalg.inv(X.T @ X)
        V = XtXi @ S @ XtXi
        res[f"lag{lag}q"] = {"beta": round(float(b[1]), 3), "nw_se": round(float(math.sqrt(V[1, 1])), 3),
                             "corr": round(float(np.corrcoef(x, y)[0, 1]), 3), "n": int(len(y))}
    res["sample"] = f"{dates[0]}..{dates[-1]} (BIS series ends here)"
    return res


# ------------------------------------------------------------------------------------------------ main
def main():
    gen = json.load(open(sys.argv[1], encoding="utf-8"))
    g15_dir, out_path = sys.argv[2], sys.argv[3]
    out = {"label": L.LABEL, "asof": L.MARKET["asof"], "unit": "m bbl front-month-equivalent (Dec-26 Brent "
           "$105.92) per the generator's slow-factor impulse; positive = long oil"}

    # ---------------- curves: current (observed strip) and state curves at month 12
    Fobs = L.observed_curve_monthly(M)
    PZm, _ = L.monthly_lsq(L.PZ_A)
    PS = L.s_chain_for_share(0.1433)
    K, _ = L.calibrate_kappa(PS, PZm)
    g = L.Gen(PS, PZm, K, gw_mode="weibull", gw_k=1.3)
    Z0 = np.array([0.03, 0.0, 0.0, 0.02, 0.10, 0.85])
    sim = g.simulate(n=40000, T=24, seed=20261019, S0=L.sLATE, Z0=Z0, x0=math.log(L.F1),
                     chi0=math.log(L.SPOT / L.F1))
    # as-of tenor premium (strip vs generator E1 curve from the Z0 mixture)
    e1_now = sum(Z0[z] * np.log(e1_curve(math.log(L.F1), z, PZm)) for z in range(6))
    prem = np.log(Fobs) - e1_now
    states = {}
    for nm, zi, mm in (("SG", L.iSG, 12), ("DB", L.iDB, 12), ("GW", L.iGW, 12), ("N", L.iN, 12),
                       ("SG24", L.iSG, 24), ("DB24", L.iDB, 24)):
        sel = sim["Z"][mm] == zi
        xs = float(np.median(sim["x"][mm][sel]))
        curve = e1_curve(xs, zi, PZm) * np.exp(prem)      # P-median plus the as-of tenor premium
        states[nm] = {"share_of_paths_at_m12": round(float(sel.mean()), 4), "front": float(curve[0]),
                      "curve": curve}
    out["state_curves_m12"] = {k: {"share": v["share_of_paths_at_m12"], "front_month": round(v["front"], 2),
                                   "1y_fwd": round(float(v["curve"][12]), 2), "3y_avg": round(float(
                                       v["curve"][1:37].mean()), 2)} for k, v in states.items()}
    out["current_curve"] = {"front_month": L.F1, "1y_fwd": round(float(Fobs[12]), 2),
                            "3y_avg": round(float(Fobs[1:37].mean()), 2)}

    # ---------------- ENR segment elasticities and values on each curve
    def seg_on(curve, ltv=0.40):
        el = L.segment_elasticities(curve, BETA_M, ltv=ltv)
        Fk = L.annual_avg(curve)
        Fk1 = L.annual_avg(curve * np.exp(0.01 * BETA_M))
        v = {"pdp": L.pdp_value(Fk), "roy": L.roy_value(Fk), "mid": L.mid_value(Fk)}
        debt = ltv * v_now_pdp                    # debt fixed at today's 40% of PDP value
        v["lev"] = max(v["pdp"] - debt, 1e-9)
        el["lev"] = (L.pdp_value(Fk1) - v["pdp"]) / 0.01 / v["lev"]
        return el, v

    Fk_now = L.annual_avg(Fobs)
    v_now_pdp = L.pdp_value(Fk_now)
    el_now, val_now = seg_on(Fobs)
    seg_state = {nm: seg_on(st["curve"]) for nm, st in states.items()}
    # G12 reference: elasticities at $70 N state and $95 GW state from its own one-factor curve
    out["enr_elasticities"] = {"canonical_now": {k: round(v, 3) for k, v in el_now.items()},
                               **{f"{nm}_m12": {k: round(v, 3) for k, v in seg_state[nm][0].items()}
                                  for nm in states},
                               "G12_N_at_70": {"pdp": 0.386, "roy": 0.305, "mid": 0.099, "lev": 0.643},
                               "G12_GW_at_95": {"pdp": 0.395, "roy": 0.311, "mid": 0.099, "lev": 0.659}}

    # ---------------- holdings (SYNTHETIC v2 book)
    gcc = gcc_regression(g15_dir)
    out["gcc_regression"] = gcc
    beta_gcc_asset = max(gcc["lag1q"]["beta"], gcc["lag0q"]["beta"])
    eps_gcc_now = 0.0                       # today: GW wedge dominates; fiscal channel shown in SG/DB
    eps_gcc_fiscal = beta_gcc_asset / (1 - 0.45) * 0.70      # equity, year-ahead average response 0.70 [I]
    eps_gcc_g15 = (0.15 / abs(math.log(0.60))) / (1 - 0.45)  # G15 SG stress: -15% asset value for Brent -40%
    eps_gcc_gw = -(0.10 / math.log(1.40)) / (1 - 0.45)        # G15 GW: -10% asset value while oil +40%

    def lin(nav, eps, note, eps_sg=None, eps_db=None, group="", tag="[I]"):
        return {"nav": nav, "eps": eps, "eps_SG": eps if eps_sg is None else eps_sg,
                "eps_DB": eps if eps_db is None else eps_db, "note": note, "group": group, "tag": tag, "kind": "lin"}

    w_energy_acwi = 0.0396                   # MSCI ACWI (net) factsheet, 30 Sep 2026 [S]
    w_energy_pe = 0.020                      # Pantheon International factsheet, 31 Aug 2026 [S-sec]
    beta12_listed = 0.40                     # Norges Bank (2017): global oil & gas relative beta to 12m futures [S]
    beta12_credit = 0.08                     # Norges Bank (2017): energy bonds, since 2008 [S]
    resp12 = float(BETA_M[12])               # 12m-future response to a slow-factor shock (0.60)
    eps_listed = beta12_listed * resp12
    eps_pe = 0.45 * 1.4 * resp12             # PE energy: listed-mix beta 0.45 x buyout leverage 1.4 [I]
    book = {
        # Real Assets (G15 census; G12 sub-split)
        "RA ENR levered upstream (funds 0.80 + direct 0.27)": {"nav": 1.07, "seg": "lev", "group": "RA",
                                                              "kind": "seg", "tag": "[I] G12 split"},
        "RA ENR royalties": {"nav": 0.18, "seg": "roy", "group": "RA", "kind": "seg", "tag": "[I] G12 split"},
        "RA ENR fee midstream (funds 0.40 + JV 0.45)": {"nav": 0.85, "seg": "mid", "group": "RA", "kind": "seg",
                                                       "tag": "[I] G12 split"},
        "RA ENR other (services, metals, transition)": lin(0.40, 0.07, "G12's 1m bbl per $bn at $70", group="RA"),
        "RA infrastructure midstream (10% of $6.5bn, energy_link)": {"nav": 0.65, "seg": "mid", "group": "RA",
                                                                    "kind": "seg",
                                                                    "tag": "[I] G11 weights; RA s2.1 rule"},
        "RA GCC real estate (fiscal/oil channel)": lin(1.20, eps_gcc_now, "today GW wedge offsets the fiscal "
                                                       "channel; SG/DB use the fiscal loading", eps_sg=eps_gcc_fiscal,
                                                       eps_db=eps_gcc_fiscal, group="RA",
                                                       tag="[I-calc] BIS/FRED regression; G15 stress"),
        # other private groups (look-through energy)
        "PE funds energy look-through (2.0% of $34bn)": lin(34.0 * w_energy_pe, eps_pe, "PIN 2.0% energy",
                                                           group="PE", tag="[S-sec]/[I]"),
        "Co-investment energy look-through (3% of $18bn)": lin(18.0 * 0.03, eps_pe, "share [I]", group="CO"),
        "Secondaries energy look-through (2% of $14bn)": lin(14.0 * 0.02, eps_pe, "share [I]", group="SEC"),
        "Capital Solutions energy (3% of $8bn)": lin(8.0 * 0.03, 0.20 * resp12, "pref/structured beta 0.2 [I]",
                                                     eps_sg=0.35 * resp12, eps_db=0.35 * resp12, group="CS"),
        "Private Credit energy loans (2% of $14bn)": lin(14.0 * 0.02, beta12_credit * resp12,
                                                         "CCLFX energy ~1% [S]; NB credit beta [S]; stressed 0.25 [I]",
                                                         eps_sg=0.25 * resp12, eps_db=0.25 * resp12, group="PC",
                                                         tag="[S]/[I]"),
        # Public Markets
        "Long-only equity energy (3.96% of $28bn)": lin(28.0 * w_energy_acwi, eps_listed, "MSCI ACWI 3.96%; NB "
                                                        "beta 0.40 to 12m futures", group="PUB", tag="[S]"),
        "Long-only fixed income energy (8% of $8bn)": lin(8.0 * 0.08, beta12_credit * resp12, "share [I]",
                                                          eps_sg=0.20 * resp12, eps_db=0.20 * resp12, group="PUB"),
        "Hedge funds energy (net beta 0.3 x 3.96% of $20bn)": lin(20.0 * 0.3 * w_energy_acwi, eps_listed,
                                                                  "macro/commodity books unknown, set 0 [I]",
                                                                  group="PUB"),
        # Overlay
        "Overlay completion beta energy (3.96% of $10bn)": lin(10.0 * w_energy_acwi, eps_listed, "", group="OVL",
                                                               tag="[S]/[I]"),
    }
    rows = {}
    STS = ("now", "SG", "DB", "SG24", "DB24")
    tot = {s: 0.0 for s in STS}
    ra = {s: 0.0 for s in STS}
    enr = {s: 0.0 for s in STS}
    for name, h in book.items():
        r = {"group": h["group"], "tag": h["tag"], "nav_now": round(h["nav"], 3)}
        if h["kind"] == "seg":
            s = h["seg"]
            for st in STS:
                el, val = (el_now, val_now) if st == "now" else seg_state[st]
                f1 = L.F1 if st == "now" else states[st]["front"]
                nav = h["nav"] * (val[s] / val_now[s] if st != "now" else 1.0)
                nav = max(nav, 0.0)
                d = el[s] * nav * 1000.0 / f1
                r[f"eps_{st}"] = round(el[s], 3)
                r[f"nav_{st}"] = round(nav, 3)
                r[f"delta_{st}"] = round(d, 2)
        else:
            for st in STS:
                eps = h["eps"] if st == "now" else h[f"eps_{st[:2]}"]
                if st == "now":
                    nav, f1 = h["nav"], L.F1
                else:
                    dx = math.log(states[st]["front"] / L.F1)
                    nav, f1 = h["nav"] * math.exp(eps * dx), states[st]["front"]
                d = eps * nav * 1000.0 / f1
                r[f"eps_{st}"] = round(eps, 3)
                r[f"nav_{st}"] = round(nav, 3)
                r[f"delta_{st}"] = round(d, 2)
        for st in STS:
            tot[st] += r[f"delta_{st}"]
            if h["group"] == "RA":
                ra[st] += r[f"delta_{st}"]
                if name.startswith("RA ENR"):
                    enr[st] += r[f"delta_{st}"]
        rows[name] = r
    out["ledger"] = rows

    # ---------------- overlay derivatives: opportunistic templates and (if permitted) kink put spreads
    vol_budget = 0.011 * NAV_TOTAL           # opportunistic vol ~1.0-1.2% of NAV (groups s3.7)
    trend_share, carry_share = 0.35, 0.25    # [I] split of the opportunistic risk budget
    sig_crude = L.term_vol(0.25)             # 3-month crude vol from OVX decay
    trend_crude_vol = trend_share * vol_budget / math.sqrt(40) * 2 * math.sqrt((1 + 0.95) / 2)
    carry_crude_vol = carry_share * vol_budget / 4 / math.sqrt(10) * 2 * math.sqrt((1 + 0.95) / 2)
    trend_bbl = trend_crude_vol / sig_crude / L.F1 * 1000 * BETA_M[2]
    carry_bbl = carry_crude_vol / sig_crude / L.F1 * 1000 * BETA_M[2]
    out["overlay_opportunistic_templates"] = {
        "assumptions": {"vol_budget_usd_bn": round(vol_budget, 2), "trend_share": trend_share,
                        "carry_share": carry_share, "crude_vol_3m": round(sig_crude, 3),
                        "markets": "trend 40 futures equal risk; carry 4 asset buckets x ~10 markets; Brent+WTI "
                                   "rho 0.95 [I]"},
        "trend_m_bbl_now": round(trend_bbl, 2), "carry_m_bbl_now": round(carry_bbl, 2),
        "sign_now": "long: 12-month Brent return strongly positive (4Q25 avg $63.65 -> Oct-26 front $105.92) and "
                    "the curve is in steep backwardation (Dec-26 to Dec-27 -$20.84)",
        "sign_SG_DB": "short: trend flips after a sustained fall; carry flips if the curve moves to contango"}
    opp = trend_bbl + carry_bbl

    def put_spread_delta(n_mbbl, k_hi, k_lo, m_exp, curve, skew=0.15, vol_scale=1.0):
        """Spot-equivalent delta of a long put spread on the m_exp-month future: n x option delta x dlnF/dx x F,
        divided by that state's front month. Vol: OVX-anchored term structure [I] with a linear put skew [I]."""
        T = m_exp / 12.0
        F = float(curve[m_exp])
        atm = L.term_vol(T) * vol_scale
        s_hi = atm * (1 + skew * max(0.0, 1 - k_hi / F))
        s_lo = atm * (1 + skew * max(0.0, 1 - k_lo / F))
        dlt = L.b76_put_delta(F, k_hi, s_hi, T) - L.b76_put_delta(F, k_lo, s_lo, T)
        prem = L.b76_put(F, k_hi, s_hi, T) - L.b76_put(F, k_lo, s_lo, T)
        bbl = n_mbbl * float(dlt) * float(BETA_M[m_exp]) * F / float(curve[0])
        return {"forward": round(F, 2), "atm_vol": round(atm, 3), "option_delta_per_bbl": round(float(dlt), 3),
                "spot_equiv_m_bbl": round(float(bbl), 2), "premium_usd_per_bbl": round(float(prem), 2),
                "premium_usd_bn": round(float(prem) * n_mbbl / 1000, 3)}

    ps = {}
    for label, (khi, klo) in {"log kinks 64/31": (64.0, 31.0), "linear kinks 67/23": (67.0, 23.0),
                              "canonical linear kinks 65/26 (P_BE 55, 2027 volumes)": (65.3, 26.5)}.items():
        for tenor_label, m_exp in (("1y (Dec-27)", 13), ("2y (Dec-28)", 25)):
            for n in (20.0, 40.0):
                key = f"{label} | {tenor_label} | {int(n)}m bbl notional"
                ps[key] = {"now": put_spread_delta(n, khi, klo, m_exp, Fobs),
                           "now_vol_x0.8": put_spread_delta(n, khi, klo, m_exp, Fobs, vol_scale=0.8),
                           "now_vol_x1.3": put_spread_delta(n, khi, klo, m_exp, Fobs, vol_scale=1.3)}
                for st in ("SG", "DB", "SG24", "DB24"):
                    c = states[st]["curve"]
                    ps[key][st] = put_spread_delta(n, khi, klo, m_exp, c)   # same programme, rolled, at state
    out["kink_put_spreads"] = ps
    # groups gap_04 integrated-engine Level-1 Brent ladder: 20% of a 0.15%-of-NAV tail budget in 12m 85/65 spreads
    prem_bud = 0.20 * 0.0015 * NAV_TOTAL
    F12 = float(Fobs[12])
    lad = put_spread_delta(1.0, 0.85 * F12, 0.65 * F12, 12, Fobs)
    lad_n = prem_bud / (lad["premium_usd_bn"])
    out["groups_gap04_brent_ladder"] = {"premium_usd_bn_a_year": round(prem_bud, 3),
                                        "notional_m_bbl": round(lad_n, 1),
                                        "spot_equiv_m_bbl": round(lad_n * lad["spot_equiv_m_bbl"], 2)}

    # ---------------- totals
    out["totals"] = {
        "RA_ENR_only": {k: round(v, 2) for k, v in enr.items()},
        "RA_total (ENR + infra midstream + GCC RE)": {k: round(v, 2) for k, v in ra.items()},
        "total_portfolio_assets_ex_overlay_derivatives": {k: round(v, 2) for k, v in tot.items()},
        "overlay_opportunistic_templates_now": round(opp, 2),
        "total_incl_opportunistic_now": round(tot["now"] + opp, 2),
        "G12_reference_ENR": {"$70 N basis": 12.22, "$95 GW basis": 9.2}}
    out["liability_in_barrels"] = {
        "L_eff_t0_pct_nav": round(100 * gen["L_eff"]["canonical_t0"]["L_eff_t0_pv"], 2),
        "PV_draw_delta_m_bbl": round(gen["L_eff"]["canonical_t0"]["L_eff_t0_pv"] * NAV_TOTAL * 1000 / L.F1, 1),
        "first_year_2027_draw_delta_m_bbl": round(gen["L_eff"]["canonical_t0"][
            "draw_sensitivity_by_year_pct_nav_per_unit_log"][0] / 100 * NAV_TOTAL * 1000 / L.F1, 1),
        "first_year_conditional_on_in_band_m_bbl": round(gen["L_eff"]["canonical_t0"][
            "draw_sensitivity_by_year_pct_nav_per_unit_log"][0] / 100 / max(gen["L_eff"]["canonical_t0"][
                "p_inband_by_year"][0], 1e-9) * NAV_TOTAL * 1000 / L.F1, 1),
        "stream03_reference_first_year_m_bbl": 100}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=float)
    print(json.dumps({k: out[k] for k in ("state_curves_m12", "current_curve", "enr_elasticities", "gcc_regression",
                                          "totals", "liability_in_barrels", "overlay_opportunistic_templates",
                                          "groups_gap04_brent_ladder")}, indent=1, default=float))
    for k, v in rows.items():
        print(f"{k[:62]:62s} nav {v['nav_now']:6.2f} eps {v['eps_now']:6.3f} d_now {v['delta_now']:6.2f} "
              f"d_SG {v['delta_SG']:6.2f} d_DB {v['delta_DB']:6.2f} d_SG24 {v['delta_SG24']:6.2f} "
              f"d_DB24 {v['delta_DB24']:6.2f}")
    for k, v in ps.items():
        print(k, v["now"]["spot_equiv_m_bbl"], v["now"]["option_delta_per_bbl"], v["now"]["premium_usd_per_bbl"],
              "| SG", v["SG"]["spot_equiv_m_bbl"], "| DB", v["DB"]["spot_equiv_m_bbl"],
              "| SG24", v["SG24"]["spot_equiv_m_bbl"], "| DB24", v["DB24"]["spot_equiv_m_bbl"])


if __name__ == "__main__":
    main()
