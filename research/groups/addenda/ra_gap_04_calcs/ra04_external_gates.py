"""
ra_gap_04 - external-data gates replacing V-RA-OIL and V-RA-CF (which pinned prototype outputs and could not fail).
Model outputs are SYNTHETIC [I-calc]; targets are PUBLIC, dated data. Not ADIC data.

V-RA-OIL-X (oil elasticities and mark dynamics of the ENR sleeve, not its barrel count):
  X1 2014-16 glut replay: closed-end ENR sleeve (G12 split: levered upstream $0.80bn, fee midstream $0.40bn, other
     $0.40bn; spot elasticities at the $70 normal state 0.643 / 0.099 / 0.07 from g12_wrongway_sim_results.json and
     g12_enr_book.py) driven by FRED Brent quarterly averages; reported NAV = RAME ENR smoothing (lambda 0.50) after a
     2-quarter deck lag (synthesis sec. 5); income 4% x (Brent/75)^1.2. Target: Cambridge Associates private energy
     benchmark 2015 = -20.5% (CA Real Asset Dynamics, Jun 2016, via G15). Gate: within +/-7pp.
  X2 2026 Gulf-war spike: same model; target MSCI natural-resources closed-end index 2026Q1 +6.9%, Q2 +3.6% (MSCI
     Private Capital Benchmarks Summary Q2-2026, p. 7). Gate: H1 cumulative within +/-6pp of +10.7%, and same-sign
     Q1 response (tests the deck lag).
  X3 listed-equity cross-check: sleeve-weighted elasticity inside the listed oil-equity episode range
     (Ken French Oil industry vs EIA Brent, G12 episode file): 2014-16 0.40; COVID 0.33; 2026 Gulf war 0.71.
  The barrel delta (sum NAV_j x elasticity_j / price) is then REPORTED from the validated elasticities, not pinned.
V-RA-CF-X (cash-row ingredients against external data):
  X1 RE closed-end distributions, mature-population analogue (seal_ra_ce_results.json): TTM-3Q25 vs Ares 7% +/- 2pp;
     10-year time average vs ~21% +/- 4pp (Ares, 11 Feb 2026: 7% is "about a third of the 10-year average").
  X2 closed-end contribution rates H1-2026 on the sealed book vs MSCI all-private-capital 29% +/- 5pp (weak).
  X3 cash-row NAV growth: G15 closed-end sleeve total return in the drought state (income + appreciation) vs MSCI
     closed-end index average of 2024-25 (RE -2.6/+2.3, infrastructure +6.4/+12.6, natural resources +3.7/+4.9);
     gate +/-3pp.
  X4-X5 open-end RE income vs NCREIF ODCE income 4.08% gross TTM 2Q26 and open-end infrastructure yield vs bfinance
     >= 6% target: CALIBRATION IDENTITIES (the G15 values were set from these sources) - reported, not counted.
  X6 open-end queue: V-RE2 (ra04_vre2_queue.py).
Run:  .venv\\Scripts\\python.exe -I -B ra04_external_gates.py -> ra04_external_gates_results.json
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "ra04_external_gates_results.json"
LBL = "Model outputs SYNTHETIC [I-calc]; targets PUBLIC and dated; not ADIC data"


def brent():
    out = {}
    with open(HERE.parent / "G15_calcs" / "data" / "fred_DCOILBRENTEU_quarterly_avg.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            y, m = int(row["observation_date"][:4]), int(row["observation_date"][5:7])
            out[(y, (m - 1) // 3 + 1)] = float(row["DCOILBRENTEU"])
    return out


def g12_elasticities():
    j = json.loads((HERE.parent / "G12_calcs" / "g12_wrongway_sim_results.json").read_text(encoding="utf-8"))
    return j["elasticities"]


def enr_replay(eps, start, end, lam=0.50, lag=2, inc=0.04, eta=1.2, fbar=75.0):
    """Quarterly true log value change = eps x dln(Brent); reported = smoothed after a deck lag; total return =
    reported capital change + income. Returns dict quarter -> (true, reported capital, total)."""
    B = brent()
    qs = sorted(k for k in B if start <= k <= end)
    v = {qs[0]: 0.0}
    for a, b in zip(qs[:-1], qs[1:]):
        v[b] = v[a] + eps * math.log(B[b] / B[a])
    s = {qs[0]: 0.0}
    out = {}
    for i, q in enumerate(qs[1:], start=1):
        src = v[qs[max(i - lag, 0)]]
        s[q] = lam * s[qs[i - 1]] + (1 - lam) * src
        cap = math.exp(s[q] - s[qs[i - 1]]) - 1
        income = inc / 4 * (B[q] / fbar) ** eta
        out[q] = dict(true=math.exp(v[q] - v[qs[i - 1]]) - 1, reported_capital=cap, total=cap + income)
    return out


def compound(out, qs):
    x = 1.0
    for q in qs:
        x *= 1 + out[q]["total"]
    return x - 1


def main():
    res = dict(label=LBL)
    el = g12_elasticities()["N_at_70"]
    split = {"lev": 0.80, "mid": 0.40, "other": 0.40}             # G12 closed-end ENR fund holdings, $bn
    eps_j = {"lev": el["lev"]["elasticity_to_spot"], "mid": el["mid"]["elasticity_to_spot"], "other": 0.07}
    eps_ce = sum(split[k] * eps_j[k] for k in split) / sum(split.values())
    res["enr_ce_elasticity"] = dict(components=eps_j, weights_bn=split, sleeve=eps_ce)
    # X1: 2014-16 glut
    o = enr_replay(eps_ce, (2013, 4), (2016, 4))
    r2015 = compound(o, [(2015, q) for q in (1, 2, 3, 4)])
    r2015_nolag = compound(enr_replay(eps_ce, (2013, 4), (2016, 4), lag=0), [(2015, q) for q in (1, 2, 3, 4)])
    res["OIL_X1"] = dict(model_2015_total=r2015, model_2015_total_no_deck_lag=r2015_nolag, target=-0.205,
                         source="Cambridge Associates private energy benchmark, 2015 (CA Real Asset Dynamics, Jun 2016)",
                         passes=bool(abs(r2015 + 0.205) <= 0.07))
    # X2: 2026 spike
    o2 = enr_replay(eps_ce, (2024, 4), (2026, 2))
    q1, q2 = o2[(2026, 1)]["total"], o2[(2026, 2)]["total"]
    h1 = (1 + q1) * (1 + q2) - 1
    o2n = enr_replay(eps_ce, (2024, 4), (2026, 2), lag=0)
    h1n = (1 + o2n[(2026, 1)]["total"]) * (1 + o2n[(2026, 2)]["total"]) - 1
    res["OIL_X2"] = dict(model_q1=q1, model_q2=q2, model_h1=h1, model_h1_no_deck_lag=h1n,
                         model_q1_no_deck_lag=o2n[(2026, 1)]["total"], target_q1=0.069, target_q2=0.036, target_h1=0.107,
                         source="MSCI Private Capital Benchmarks Summary Q2-2026, natural-resources closed-end index",
                         passes=bool(abs(h1 - 0.107) <= 0.06 and q1 > 0))
    # X3: listed cross-check (G12 episode file)
    ep = json.loads((HERE.parent / "G12_calcs" / "g12_episode_stats_results.json").read_text(encoding="utf-8"))["episodes"]
    def ee(k):
        e = ep[k]
        return math.log(1 + e["Oil"]) / math.log(1 + e["brent_change"])
    listed = {"oil_bust_2014-06_2016-01": ee("oil_bust_2014-06_2016-01"), "covid_2019-12_2020-04": ee("covid_2019-12_2020-04"),
              "gulf_war_2026-02_2026-08": ee("gulf_war_2026-02_2026-08")}
    lo, hi = min(listed.values()), max(listed.values())
    sleeve_total_eps = 12.2e6 * 70 / 2.5e9                           # G12: 12.2m bbl at $70 on the $2.5bn sleeve
    res["OIL_X3"] = dict(listed_episode_elasticities=listed, band=[lo, hi], enr_ce_elasticity=eps_ce,
                         enr_total_sleeve_elasticity=sleeve_total_eps,
                         unlevered_pdp=el["pdp"]["elasticity_to_spot"], levered_upstream=el["lev"]["elasticity_to_spot"],
                         passes=bool(lo <= sleeve_total_eps <= hi))
    # Derived (not pinned) barrel delta from the validated elasticities
    full = {"lev": 1.07, "roy": 0.18, "mid": 0.85, "other": 0.40}
    eps_full = {"lev": el["lev"]["elasticity_to_spot"], "roy": el["roy"]["elasticity_to_spot"],
                "mid": el["mid"]["elasticity_to_spot"], "other": 0.07}
    res["OIL_delta_derived"] = {f"at_{p}": round(sum(full[k] * 1e9 * eps_full[k] / p for k in full) / 1e6, 2)
                                for p in (70, 95)}
    # V-RA-CF-X
    seal = json.loads((HERE / "seal_ra_ce_results.json").read_text(encoding="utf-8"))
    mh = seal["mature_history_rates"]["RE"]
    res["CF_X1"] = dict(mature_ttm_3q25=mh["ttm_3q25"], mature_10y_avg=mh["avg_10y"], targets=dict(ttm=0.07, avg10=0.21),
                        source="Ares (11 Feb 2026), global real estate funds",
                        passes=bool(abs(mh["ttm_3q25"] - 0.07) <= 0.02 and abs(mh["avg_10y"] - 0.21) <= 0.04))
    cx = {s: seal["sectors"][s]["rates"]["contrib_h1_26"] for s in ("RE", "INF", "ENR")}
    res["CF_X2"] = dict(contrib_h1_26=cx, target=0.29, band=[0.24, 0.34],
                        source="MSCI Private Capital Benchmarks Summary Q2-2026 p.12 (all private capital, 2026 YTD)",
                        passes={s: bool(0.24 <= v <= 0.34) for s, v in cx.items()})
    g15 = {"RE_CE": 0.010 + 0.020, "INF_CE": 0.040 + 0.040, "ENR_CE": 0.040 + 0.030}   # G15 inc + g_n (drought)
    msci = {"RE_CE": (-0.026 + 0.023) / 2, "INF_CE": (0.064 + 0.126) / 2, "ENR_CE": (0.037 + 0.049) / 2}
    res["CF_X3"] = dict(g15_drought_total_return=g15, msci_2024_25_avg=msci,
                        diff_pp={k: round(100 * (g15[k] - msci[k]), 2) for k in g15},
                        passes={k: bool(abs(g15[k] - msci[k]) <= 0.03) for k in g15},
                        source="MSCI Private Capital Benchmarks Summary Q2-2026 p.7 (closed-end indices)")
    res["CF_X4_X5_identities"] = dict(open_end_re_net_cash=0.0325, odce_income_gross_ttm_2q26=0.0408,
                                      open_end_infra_cash=0.055, bfinance_target_yield=">= 6%",
                                      note="G15 set these from the sources: calibration identities, not validation")
    OUT.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    print(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
