"""Summaries of ra_main_results.json for the addendum (SYNTHETIC - NOT ADIC DATA)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "ra_main_results.json"), encoding="utf-8"))
runs = d["runs"]
print("theta*", d["theta_star"])
print("\nP(red) % / CE / E[W] by book, model, policy")
for book in ("v1", "v2u16", "v2u11"):
    for pname in ("off", "dn", "mixA", "mixB", "mixB_raoff"):
        row = []
        for mk in ("M1", "M2", "M3", "M4", "M5", "M6"):
            k = f"{book}|{mk}|{pname}"
            if k in runs:
                r = runs[k]
                row.append(f"{mk}:{100 * r['p_red']:.2f}/{r['ce']:.1f}/{r['mean_wtilde']:.1f}")
        if row:
            print(book, pname, " ".join(row))
print("\nPer-group fans, Mix B (P(cash<0) y1..y5 | 5y cash P5/P50/P95 | NAV y5 P50 | 5y DVA P5/P50/P95)")
for book in ("v2u16",):
    for mk in ("M1", "M6"):
        f = runs[f"{book}|{mk}|mixB"]["fans"]
        for g in ("PE", "SEC", "CS", "CO", "PC", "RA", "PM", "OVL", "TPA"):
            x = f[g]
            print(book, mk, g, [round(v, 2) for v in x["p_cash_neg"]], [x["cash5"][0], x["cash5"][2], x["cash5"][4]],
                  x["nav5"][2] if x["nav5"] else None, [x["dva5"][0], x["dva5"][2], x["dva5"][4]])
print("\nRA DVA by basis (Mix B): year-1 mean and 5-year P50 ($bn); gap reported(obs beta) - V*(desm beta)")
for book in ("v2u16", "v2u11"):
    for mk in ("M1", "M4", "M6"):
        for pname in ("off", "mixB"):
            r = runs[f"{book}|{mk}|{pname}"]
            dv = r["ra"]["dva"]
            gap = r["ra_dva_gap_rep_minus_star"]
            print(book, mk, pname, {k: (round(v["mean_y"][0], 2), round(v["cum5_q"][2], 2)) for k, v in dv.items()},
                  "gap y1 P5/P50/P95", [round(x, 2) for x in (gap["y1"][0], gap["y1"][2], gap["y1"][4])],
                  "cum5 mean", round(gap["cum5_mean"], 2))
print("\nRA cash and cures (Mix B vs off)")
for book in ("v2u16", "v2u11"):
    for mk in ("M1", "M6"):
        for pname in ("off", "dn", "mixB"):
            ra = runs[f"{book}|{mk}|{pname}"]["ra"]
            print(book, mk, pname, "cash/yr", [round(v, 2) for v in ra["cash_y_mean"]], "P(cash<0)",
                  [round(v, 2) for v in ra["p_cash_neg_y"]], "cures24", {k: round(v, 2) for k, v in ra["cures24"].items()},
                  "OE red", round(ra["oe_redemptions"], 2), "JV", round(ra["jv_cash"], 2), "cash-out", round(ra["cashout"], 2),
                  "forced", round(ra["forced_sale_cash"], 2), "oil t0/post", round(ra["oil_delta_t0"], 1), round(ra["oil_delta_post_sale"], 1))
print("\nCLC inputs", json.dumps(d["clc"], indent=0)[:2000])
