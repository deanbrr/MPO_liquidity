"""RA gap 03, step 5: the barrel budget derived from marginal Tier-1 and Tier-2 costs, and RA's envelope.

SYNTHETIC - NOT ADIC DATA. Inputs: ra03_tier1_results.json and ra03_tier1_sens_results.json (marginal effects on
the canonical generator), ra03_ledger_results.json (the total-portfolio ledger), ra03_gen_results.json (L_eff).
Price per barrel (front-month-equivalent, a year):
  Tier 2:  -dCE per m bbl (bp of NAV a year; 1bp = $17.7m a year)
  Tier 1:  mu x dG*(P99.6) per m bbl / annuity(5y, 5%) + c_red x dP(red) per m bbl
           mu: restored-problem duals, R1 (revolver signed) 0.0113, R0 (group levers) 0.243 per $ of month-24 headroom
           c_red: slope of gap_02's M1-M5 CE-price frontier near the 1% gate, 4-8bp a year per pp of P(red)
  plus the lambda-weighted and draw-weighted haircuts (path versions) for reference.
Quantity: the Tier-1 backstop is the barrel count at which the binding gate's slack is exhausted under the adopted
funding mix (checked by direct large bumps); in RECOVERY no action may worsen a violated gate.

Usage: python -I ra03_budget_run.py <tier1_json> <sens_json> <ledger_json> <gen_json> <out_json>
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ra03_lib as L  # noqa: E402
import ra03_t1oil as T  # noqa: E402
from ra03_tier1_run import LEDGER_NOW, POLICIES  # noqa: E402

E = T.E
BP_USD_M = 17.7
MU = {"R1_revolver_signed": 0.0113, "R0_group_levers": 0.243}
C_RED = (4.0, 8.0)                      # bp a year per pp of P(red) [I-calc, gap_02 frontier slope near 1%]
ANNUITY5 = sum(1.05 ** -k for k in range(1, 6))
LEDGER_BBL = LEDGER_NOW["PRIV"] + LEDGER_NOW["LEV"] + LEDGER_NOW["PUB"]   # m bbl (GCC carried in $bn)


def main():
    t1 = json.load(open(sys.argv[1], encoding="utf-8"))
    sens = json.load(open(sys.argv[2], encoding="utf-8"))
    led = json.load(open(sys.argv[3], encoding="utf-8"))
    gen = json.load(open(sys.argv[4], encoding="utf-8"))
    out = {"label": L.LABEL, "constants": {"bp_usd_m": BP_USD_M, "mu": MU, "c_red_bp_per_pp": C_RED,
                                           "annuity_5y": round(ANNUITY5, 3), "ledger_bbl_engine": LEDGER_BBL}}
    # ---------------- per-barrel prices by channel
    chans = {"PRIV_lookthrough_10": 10.0, "PRIV_enr_fund_10": 10.0, "LEV_direct_10": 10.0, "PUB_10": 10.0,
             "ledger_now": LEDGER_BBL}
    price = {}
    for ch, size in chans.items():
        rows = []
        for key, r in t1["runs"].items():
            mk, pk = key.split("|")
            if ch not in r["bumps"]:
                continue
            b = r["bumps"][ch]
            rows.append({"model": mk, "policy": pk,
                         "t2_bp_per_mbbl": -b["dCE_bp_a_year"] / size,
                         "dG_bn_per_mbbl": b["dG*_q99.6_bn"] / size,
                         "dG_top1_bn_per_mbbl": b["dG*_pathwise_mean_top1pct_bn"] / size,
                         "dRed_pp_per_mbbl": b["dP_red_pp"] / size,
                         "dRed_se_pp_per_mbbl": b["dP_red_pp_se"] / size})
        agg = {}
        for pk in ("do_nothing", "mix_A", "mix_B"):
            for grp, models in (("M1-M5", ("M1", "M2", "M3", "M4", "M5")), ("M6", ("M6",))):
                sel = [x for x in rows if x["policy"] == pk and x["model"] in models]
                if not sel:
                    continue
                t2 = np.array([x["t2_bp_per_mbbl"] for x in sel])
                dg = np.array([x["dG_top1_bn_per_mbbl"] for x in sel])
                dr = np.array([x["dRed_pp_per_mbbl"] for x in sel])
                t2_usd = t2 * BP_USD_M
                t1_g = {k: (mu * np.maximum(dg, 0) * 1000 / ANNUITY5) for k, mu in MU.items()}   # $m a yr per m bbl
                t1_r = (np.maximum(dr, 0) * C_RED[0] * BP_USD_M, np.maximum(dr, 0) * C_RED[1] * BP_USD_M)
                agg[f"{pk}|{grp}"] = {
                    "tier2_usd_per_bbl_yr": [round(float(t2_usd.min()), 2), round(float(t2_usd.max()), 2)],
                    "tier1_G_usd_per_bbl_yr_R1": [round(float(t1_g["R1_revolver_signed"].min()), 3),
                                                  round(float(t1_g["R1_revolver_signed"].max()), 3)],
                    "tier1_G_usd_per_bbl_yr_R0": [round(float(t1_g["R0_group_levers"].min()), 3),
                                                  round(float(t1_g["R0_group_levers"].max()), 3)],
                    "tier1_red_usd_per_bbl_yr": [round(float(t1_r[0].min()), 3), round(float(t1_r[1].max()), 3)],
                    "dRed_pp_per_mbbl": [round(float(dr.min()), 5), round(float(dr.max()), 5)],
                    "dG_top1pct_bn_per_mbbl": [round(float(dg.min()), 5), round(float(dg.max()), 5)]}
        price[ch] = agg
    out["price_per_bbl"] = price
    # lambda / draw haircuts per barrel (path versions; unit elasticity x front month)
    hl = [r["H_unit_eps"]["H_lambda_path_pct"] for r in t1["runs"].values()]
    hd = [r["H_unit_eps"]["H_draw_path_kd1.0_pct"] for r in t1["runs"].values()]
    out["haircuts_per_bbl_usd_yr"] = {"H_lambda_path": [round(min(hl) / 100 * L.F1, 3), round(max(hl) / 100 * L.F1, 3)],
                                      "H_draw_path_kd1": [round(min(hd) / 100 * L.F1, 3),
                                                          round(max(hd) / 100 * L.F1, 3)]}
    # surplus-framing check (G12's draw-surplus hurdle restated on the canonical L_eff)
    le0 = gen["L_eff"]["canonical_t0"]["L_eff_t0_pv"]
    leh = gen["L_eff"]["holding_period_avg_years_0_3"]
    sig2 = 0.2354 ** 2
    nav = 177.0
    d_now = led["totals"]["total_incl_opportunistic_now"]
    out["surplus_framing_usd_per_bbl_yr"] = {
        f"gamma{g}": [round(g * sig2 * L.F1 * (le0 + d_now * L.F1 / (nav * 1000)), 2),
                      round(g * sig2 * L.F1 * (leh + d_now * L.F1 / (nav * 1000)), 2)] for g in (2, 3, 4)}
    out["surplus_framing_note"] = ("gamma x Var(annual slow-factor move) x F1 x (L_eff + asset delta share of NAV); "
                                   "L_eff canonical t0 and holding-period average")

    # ---------------- Tier-1 backstop: slack / marginal, then direct large-bump check
    back = {}
    for pk in ("mix_A", "mix_B"):
        rows = []
        for mk in ("M1", "M2", "M3", "M4", "M5"):
            r = t1["runs"][f"{mk}|{pk}"]
            base = r["base"]["p_red_pct"]
            slack = 1.0 - base
            led_m = r["bumps"]["ledger_now"]["dP_red_pp"] / LEDGER_BBL
            se_m = r["bumps"]["ledger_now"]["dP_red_pp_se"] / LEDGER_BBL
            marg = max(led_m + 2 * se_m, 1e-6)       # conservative: +2 s.e.
            rows.append({"model": mk, "p_red_pct": base, "slack_pp": round(slack, 3),
                         "marginal_pp_per_mbbl_plus2se": round(marg, 5), "implied_cap_mbbl": round(slack / marg, 0)})
        back[pk] = {"by_model": rows, "binding": min(rows, key=lambda x: x["implied_cap_mbbl"])}
    # direct check: large private bumps under Mix B and Mix A in the two tightest models
    direct = {}
    for pk in ("mix_A", "mix_B"):
        for mk in ("M4", "M5"):
            m = E.MODELS[mk]
            gp = T.gen_paths(m, 30000, 20261018 + 1000)
            base = T.simulate_oil(m, POLICIES[pk], None, n=30000, seed=20261018, gen=gp)
            pts = []
            for add in (50.0, 100.0, 200.0):
                spec = {"PRIV": LEDGER_NOW["PRIV"] + add, "eps_PRIV": 0.5, "LEV": LEDGER_NOW["LEV"],
                        "PUB": LEDGER_NOW["PUB"], "GCC": LEDGER_NOW["GCC"]}
                r = T.simulate_oil(m, POLICIES[pk], spec, n=30000, seed=20261018, gen=gp)
                pts.append({"total_mbbl": round(LEDGER_BBL + add, 1), "p_red_pct": round(100 * r["p_red"], 3),
                            "dG*_q99.6_bn": round(r["gstar_q"][0.996] - base["gstar_q"][0.996], 3)})
            direct[f"{pk}|{mk}"] = {"base_p_red_pct": round(100 * base["p_red"], 3), "points": pts}
            print(pk, mk, direct[f"{pk}|{mk}"], flush=True)
    back["direct_large_bumps"] = direct
    # do nothing: RECOVERY (T6 breached in M3-M6) -> no action may worsen a violated gate
    rec = {}
    for mk in ("M3", "M4", "M5", "M6"):
        r = t1["runs"][f"{mk}|do_nothing"]
        rec[mk] = {"p_red_pct": r["base"]["p_red_pct"], "ledger_dRed_pp": r["bumps"]["ledger_now"]["dP_red_pp"],
                   "ledger_dRed_se": r["bumps"]["ledger_now"]["dP_red_pp_se"]}
    back["recovery_do_nothing"] = rec
    out["tier1_backstop"] = back

    # ---------------- RA envelope
    tot = led["totals"]
    ra_now = tot["RA_total (ENR + infra midstream + GCC RE)"]
    lev = led["ledger"]["RA ENR levered upstream (funds 0.80 + direct 0.27)"]
    sell = {st: 0.7 * lev[f"delta_{st}"] / 1.07 for st in ("now", "SG", "DB", "SG24", "DB24")}
    out["ra_envelope"] = {
        "RA_delta_now_by_state": ra_now,
        "SELL_0.7bn_removes": {k: round(v, 2) for k, v in sell.items()},
        "RA_envelope_in_recovery (freeze at post-SELL level)": {k: round(ra_now[k] - sell[k], 2) for k in sell},
        "share_of_total_asset_delta_now": round(ra_now["now"] / tot["total_portfolio_assets_ex_overlay_derivatives"]
                                                ["now"], 3)}
    with open(sys.argv[5], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=float)
    print(json.dumps({k: out[k] for k in ("price_per_bbl", "haircuts_per_bbl_usd_yr", "surplus_framing_usd_per_bbl_yr",
                                          "ra_envelope")}, indent=1))
    print(json.dumps({k: v for k, v in out["tier1_backstop"].items() if k != "direct_large_bumps"}, indent=1))


if __name__ == "__main__":
    main()
