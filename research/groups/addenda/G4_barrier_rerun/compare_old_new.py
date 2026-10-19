"""
G4 barrier re-run, step C: old vs new values at the precision the reports quote them.
SYNTHETIC - NOT ADIC DATA.

Reads
  ../../verification/G4_coinvest_calcs_results.json   published run (old)
  G4_coinvest_calcs_bgk_results.json                   corrected run, same seeds (new)
  section7_variants_results.json                       total-sigma and wrong-sign sensitivities
  fine_grid_book_results.json                          independent fine-grid check
  check_decisions_bgk_results.json                     decision example (covenant, wipe-out)
Writes old_vs_new.json and prints markdown tables.
Run:  <venv>/python.exe -I compare_old_new.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def jload(*p):
    with open(os.path.join(HERE, *p), encoding="utf-8") as fh:
        return json.load(fh)


OLD = jload("..", "..", "verification", "G4_coinvest_calcs_results.json")
NEW = jload("G4_coinvest_calcs_bgk_results.json")
VAR = jload("section7_variants_results.json")
FG = jload("fine_grid_book_results.json")
CD = jload("check_decisions_bgk_results.json")

S7 = {"drought": "section7_book_sim_start_drought", "normal": "section7_book_sim_start_normal"}


def g(d, path):
    for k in path.split("."):
        d = d[k]
    return d


# (label, json path inside section 7, scale, decimals, unit)
ROWS = [
    ("Distributions 3y, mean ($bn)", "dist_3y.mean", 1, 1, ""),
    ("Distributions 3y, P10", "dist_3y.p10", 1, 1, ""),
    ("Distributions 3y, P50", "dist_3y.p50", 1, 1, ""),
    ("Distributions 3y, P90", "dist_3y.p90", 1, 1, ""),
    ("Calls 3y, mean ($bn)", "calls_3y.mean", 1, 1, ""),
    ("Net cash flow 3y, mean ($bn)", "net_cf_3y.mean", 1, 1, ""),
    ("Net cash flow 3y, P10", "net_cf_3y.p10", 1, 1, ""),
    ("Net cash flow 3y, P90", "net_cf_3y.p90", 1, 1, ""),
    ("Net CF 3y if drought all 12q, mean", "net_cf_3y_if_drought_throughout.mean", 1, 1, ""),
    ("Net CF 3y if drought all 12q, P10", "net_cf_3y_if_drought_throughout.p10", 1, 1, ""),
    ("Year-1 distribution yield, mean (%)", "annual_dist_yield_on_nav0.Y1.mean", 100, 1, "%"),
    ("Year-1 distribution yield, P10 (%)", "annual_dist_yield_on_nav0.Y1.p10", 100, 1, "%"),
    ("Year-1 distribution yield, P90 (%)", "annual_dist_yield_on_nav0.Y1.p90", 100, 1, "%"),
    ("Write-off rate per position-year (%)", "annual_writeoff_rate_per_position", 100, 1, "%"),
    ("Write-offs over 3y, mean (count)", "writeoffs_3y.mean", 1, 2, ""),
    ("Write-offs over 3y, P10 / P50 / P90", None, 1, 0, ""),
    ("Written-off cost / (initial NAV + new calls) (%)", "writeoff_cost_share", 100, 1, "%"),
    ("Exits over 3y, mean (count)", "exits_3y.mean", 1, 1, ""),
    ("Exit rate per position-year (%)", "annual_exit_rate_per_position", 100, 1, "%"),
    ("Recap dividends / exit proceeds (%)", "recap_dist_over_exit_proceeds", 100, 1, "%"),
    ("P(exit > next-to-last mark)", "p_exit_above_next_to_last_mark", 1, 2, ""),
    ("Reported vs economic NAV gap, P10 (%)", "reported_vs_economic_nav_gap.p10", 100, 1, "%"),
    ("Reported vs economic NAV gap, P50 (%)", "reported_vs_economic_nav_gap.p50", 100, 1, "%"),
    ("Reported vs economic NAV gap, P90 (%)", "reported_vs_economic_nav_gap.p90", 100, 1, "%"),
    ("Economic NAV at 3y, mean ($bn)", "nav_end_economic.mean", 1, 2, ""),
    ("Reported NAV at 3y, mean ($bn)", "nav_end_reported.mean", 1, 2, ""),
]


def fmt(x, scale, dec):
    return f"{x * scale:.{dec}f}"


def main():
    out = {"label": "SYNTHETIC - NOT ADIC DATA", "section7": {}, "decision_example": {}}
    for start, key in S7.items():
        rows = []
        for label, path, scale, dec, _ in ROWS:
            if path is None:
                o = "/".join(f"{OLD[key]['writeoffs_3y'][q]:.0f}" for q in ("p10", "p50", "p90"))
                n = "/".join(f"{NEW[key]['writeoffs_3y'][q]:.0f}" for q in ("p10", "p50", "p90"))
                rows.append(dict(metric=label, old=o, new=n, changes_at_display=o != n))
                continue
            o, n = g(OLD[key], path), g(NEW[key], path)
            tot = g(VAR["variants"]["bgk_total_sigma"][f"start_{start}"], path)
            wrong = g(VAR["variants"]["bgk_wrong_sign"][f"start_{start}"], path)
            rows.append(dict(metric=label, old=fmt(o, scale, dec), new=fmt(n, scale, dec),
                             new_total_sigma=fmt(tot, scale, dec), dossier_wrong_sign=fmt(wrong, scale, dec),
                             old_raw=o, new_raw=n, changes_at_display=fmt(o, scale, dec) != fmt(n, scale, dec)))
        fg = FG[f"start_{start}"]
        fgrow = {v: fg[v]["annual_writeoff_rate_per_position"] for v in
                 ("Q", "Q_bgk", "Q_bgk_wrong_sign", "M", "M_bgk", "W", "F")}
        fgrow["continuous_limit_lsq_MWF"] = fg["continuous_limit"]["annual_writeoff_rate_per_position"]["lsq_MWF"]
        fgrow["continuous_limit_two_point_WF"] = fg["continuous_limit"]["annual_writeoff_rate_per_position"]["two_point_WF"]
        fgrow["se_level"] = fg["Q_bgk"]["annual_writeoff_rate_se"]
        fgrow["paired_Q_bgk_minus_F"] = fg["paired_vs_F"]["Q_bgk"]
        out["section7"][start] = dict(rows=rows, fine_grid_writeoff_rate=fgrow,
                                      fine_grid_cost_share={v: fg[v]["writeoff_cost_share"] for v in
                                                            ("Q", "Q_bgk", "M", "W", "F")} |
                                      {"continuous_limit": fg["continuous_limit"]["writeoff_cost_share"]["lsq_MWF"]},
                                      fine_grid_writeoffs_3y_mean={v: fg[v]["writeoffs_3y"]["mean"] for v in
                                                                   ("Q", "Q_bgk", "M", "W", "F")} |
                                      {"continuous_limit": fg["continuous_limit"]["writeoffs_3y_mean"]["lsq_MWF"]})
        print(f"\n### Section 7, start {start}\n")
        print("| Metric | Old (published) | New (BGK fix) | changes at shown precision | sigma incl. jumps | dossier sign |")
        print("|---|---|---|---|---|---|")
        for r in rows:
            print(f"| {r['metric']} | {r['old']} | {r['new']} | {'YES' if r['changes_at_display'] else 'no'} | "
                  f"{r.get('new_total_sigma', '')} | {r.get('dossier_wrong_sign', '')} |")
        print("fine-grid write-off rate:", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in fgrow.items()})

    for scen in ("normal", "drought"):
        a = CD[scen]["analysis"]
        o = CD[scen]["original_run"]
        out["decision_example"][scen] = dict(
            trigger=dict(published_quarterly=o["p_trigger_pathwise_quarterly"], **a["trigger"]),
            default_level=dict(published_quarterly=o["p_default_pathwise_quarterly"], **a["default_level"]),
            e3_barrier=a["e3_barrier"],
            wipeout_unlevered=dict(published_terminal=OLD["section6_decision"]["scenarios"][scen]["p_wipeout"],
                                   **a["wipeout_unlevered"]),
            wipeout_levered_pik=dict(published_terminal=OLD["section6_decision"]["scenarios"][scen]["lever_pik"]["p_residual_zero"],
                                     **a["wipeout_levered_pik"]),
        )
    print("\n### Decision example (calc section 6 inputs)\n")
    for scen, d in out["decision_example"].items():
        for k, v in d.items():
            print(scen, k, {kk: round(vv, 4) for kk, vv in v.items()})
    with open(os.path.join(HERE, "old_vs_new.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote", os.path.join(HERE, "old_vs_new.json"))


if __name__ == "__main__":
    main()
