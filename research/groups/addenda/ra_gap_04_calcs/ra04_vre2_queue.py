"""
ra_gap_04 - V-RE2: out-of-sample validation of the G10 open-end queue machine.
Inputs are PUBLIC data (not ADIC data); the queue path is a model output on those inputs [I-calc].

Machine (G10 sec. 4.6; fitted on 2024-26 targets: b = 0.12, w = 0.08; fixed r0 0.6%, l0 0.25%, contributions
1.2% / 0.4%, dispositions 1.0/0.6/0.4/0.2% of GAV by window O/N/D/F):
  R_t = r0 + b (G_{t-1})^+ ; W_t = w Q_t 1{G_{t-1} <= 3%} ; L_t = l0 + d(e) GAV/NAV + c_t ; P_t = min(Q_t + R_t - W_t, L_t)
G (stale-NAV premium) = ln(cumulative appraisal fund return) - ln(cumulative REIT return relevered to fund leverage),
from a base date with G = 0.
Tests:
  A. GFC (fully out of sample): appraisal series = NCREIF NPI quarterly total returns 2005Q1-2010Q2 (Cannon & Cole
     2011, Appendix Table 1), relevered to fund leverage L_O = 0.25 [I] at a 6% cost of debt [I]; REITs = FTSE Nareit
     All Equity total-return index (G10_calcs, Nareit monthly file), unlevered at L_R = 0.35 [I]. Base end-2006;
     window path [I]: N 2007H1, D 2007Q3-2008Q3, F 2008Q4-2009Q4, D 2010. Start queue 0 in 2007Q1.
     Target: GFC peak ~15% of NAV (Callan, 20 Feb 2025; Meketa) to ~21% of core NAV in 2009 (Townsend, via PREA
     Quarterly, Winter 2024). Gate (pre-registered): peak in [12%, 24%] and in 2008Q4-2010Q2.
  B. 2023 payout speed (not a fit target): G10's 2022-26 replay inputs (NCREIF ODCE quarterly returns, REITs);
     target ~5% of the queue a quarter in 2023 (Townsend/PREA); gate: 2023 mean payout ratio in [2.5%, 10%].
  C. Fund dispersion (calibration, not validation): 25 funds with fund-specific redemption sensitivity
     b_f = 0.12 exp(s z_f - s^2/2) and fund gap noise; which s reproduces 6-33% for large funds at 4Q24 (Callan)?
Run:  .venv\\Scripts\\python.exe -I -B ra04_vre2_queue.py -> ra04_vre2_queue_results.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "ra04_vre2_queue_results.json"
LBL = "PUBLIC-DATA INPUTS; queue paths are model outputs [I-calc]; not ADIC data"
B_FIT, W_FIT = 0.12, 0.08
R0, L0, C_HI, C_LO = 0.006, 0.0025, 0.012, 0.004
DISP = {"O": 0.010, "N": 0.006, "D": 0.004, "F": 0.002}

# NCREIF NPI quarterly TOTAL returns, % (Cannon & Cole 2011, Appendix Table 1)
NPI = {"2005Q1": 3.5, "2005Q2": 5.3, "2005Q3": 4.4, "2005Q4": 5.4, "2006Q1": 3.6, "2006Q2": 4.0, "2006Q3": 3.5,
       "2006Q4": 4.5, "2007Q1": 3.6, "2007Q2": 4.6, "2007Q3": 3.6, "2007Q4": 3.2, "2008Q1": 1.6, "2008Q2": 0.6,
       "2008Q3": -0.2, "2008Q4": -8.3, "2009Q1": -7.3, "2009Q2": -5.4, "2009Q3": -3.3, "2009Q4": -2.1,
       "2010Q1": 0.8, "2010Q2": 3.3}
# NFI-ODCE gross quarterly total returns 2022Q1-2026Q3 as used in G10 (NCREIF webinar, 16 Sep 2026; 3Q26 prelim.)
ODCE = [7.4, 4.8, 0.5, -5.0, -3.2, -2.7, -1.9, -4.8, -2.4, -0.4, 0.2, 1.2, 1.1, 1.0, 0.7, 0.9, 1.2, 1.5, 1.71]


def reit_quarterly():
    j = json.loads((HERE.parent / "G10_calcs" / "g10_reit_series_results.json").read_text(encoding="utf-8"))
    tri = dict((d[:7], v) for d, v in j["quarterly_tri_1999_on"])
    keys = sorted(tri)
    out = {}
    for a, b in zip(keys[:-1], keys[1:]):
        y, m = int(b[:4]), int(b[5:7])
        out[f"{y}Q{(m - 1) // 3 + 1}"] = tri[b] / tri[a] - 1
    return out


def queue_path(gap, e_path, gav_nav, b=B_FIT, w=W_FIT, q0=0.0, gcap=None, mark=None, wm=0.0):
    Q = q0
    qs, paid, ratio = [], [], []
    for t in range(len(gap)):
        g_prev = gap[t - 1] if t > 0 else 0.0
        gp = max(0.0, g_prev) if gcap is None else min(max(0.0, g_prev), gcap)
        req = R0 + b * gp
        wd = w * Q if g_prev <= 0.03 else 0.0
        if mark is not None and wm:
            wd = wd + min(1.0, wm * max(0.0, -mark[t])) * Q        # cancellations as the fund marks down
        contrib = C_LO if (g_prev > 0.03 or Q > 0.05) else C_HI
        L = L0 + DISP[e_path[t]] * gav_nav + contrib
        avail = max(0.0, Q + req - wd)
        pay = min(avail, L)
        ratio.append(pay / avail if avail > 1e-9 else None)
        Q = avail - pay
        qs.append(Q)
        paid.append(pay)
    return qs, paid, ratio


def gfc(L_O=0.25, L_R=0.35, rd=0.06, base="2006Q4", e_variant="base"):
    reit = reit_quarterly()
    quarters = [k for k in NPI if k > base]
    rdq = rd / 4
    npi = np.array([NPI[k] / 100 for k in quarters])
    rr = np.array([reit[k] for k in quarters])
    fund = (npi - L_O * rdq) / (1 - L_O)                       # appraisal fund return at fund leverage
    reit_unlev = (1 - L_R) * rr + L_R * rdq
    reit_fund = (reit_unlev - L_O * rdq) / (1 - L_O)
    gap = np.log(np.cumprod(1 + fund)) - np.log(np.cumprod(1 + reit_fund))
    e = []
    for k in quarters:
        y, q = int(k[:4]), int(k[-1])
        if e_variant == "base":
            e.append("N" if (y == 2007 and q <= 2) or y < 2007 else ("D" if (y == 2007 or (y == 2008 and q <= 3))
                     else ("F" if y == 2008 or y == 2009 else "D")))
        elif e_variant == "harsher":                       # frozen from 2008Q3 through 2010Q2
            e.append("N" if (y == 2007 and q <= 2) or y < 2007 else ("D" if y == 2007 or (y == 2008 and q <= 2)
                                                                     else "F"))
        else:                                              # milder: D throughout the crisis
            e.append("N" if (y == 2007 and q <= 2) or y < 2007 else "D")
    qs, paid, ratio = queue_path(list(gap), e, 1 / (1 - L_O))
    i = int(np.argmax(qs))
    return dict(quarters=quarters, gap_pct=[round(100 * x, 1) for x in gap], queue_pct=[round(100 * x, 1) for x in qs],
                paid_pct=[round(100 * x, 2) for x in paid], payout_ratio=[None if r is None else round(r, 3) for r in ratio],
                peak_pct=round(100 * qs[i], 1), peak_quarter=quarters[i], e_path=e)


def replay_2022():
    reit = reit_quarterly()
    qs_ = [f"{y}Q{q}" for y in range(2022, 2027) for q in range(1, 5)][:len(ODCE)]
    odce = np.array(ODCE) / 100
    rr = np.array([reit[k] for k in qs_])
    L_R, L_O, rd = 0.33, 0.25, 0.045 / 4                       # G10's assumptions
    reit_unlev = (1 - L_R) * rr + L_R * rd
    reit_as = (reit_unlev - L_O * rd) / (1 - L_O)
    gap = np.log(np.cumprod(1 + odce)) - np.log(np.cumprod(1 + reit_as))
    e = ["N", "N"] + ["D"] * 8 + ["N"] * 9
    qs, paid, ratio = queue_path(list(gap), e, 1 / (1 - 0.27))
    r23 = [r for k, r in zip(qs_, ratio) if k.startswith("2023") and r is not None]
    return dict(quarters=qs_, queue_pct=[round(100 * x, 1) for x in qs], paid_pct=[round(100 * x, 2) for x in paid],
                payout_ratio=[None if r is None else round(r, 3) for r in ratio], payout_ratio_2023_mean=float(np.mean(r23)),
                gap_pct=[round(100 * x, 1) for x in gap])


def dispersion(s_list=(0.3, 0.5, 0.7, 0.9), nf=25, reps=400, seed=11):
    rng = np.random.default_rng(seed)
    base = replay_2022()
    gap = np.array(base["gap_pct"]) / 100
    e = ["N", "N"] + ["D"] * 8 + ["N"] * 9
    idx = base["quarters"].index("2024Q4")
    out = {}
    for s in s_list:
        p5, p95, mx, med, avg = [], [], [], [], []
        for _ in range(reps):
            b_f = B_FIT * np.exp(s * rng.standard_normal(nf) - s * s / 2)
            noise = 0.02 * rng.standard_normal((nf, len(gap)))
            qend = []
            for f in range(nf):
                qs, _, _ = queue_path(list(gap + noise[f]), e, 1 / (1 - 0.27), b=b_f[f])
                qend.append(qs[idx])
            qend = np.array(qend)
            p5.append(np.percentile(qend, 5)); p95.append(np.percentile(qend, 95)); mx.append(qend.max())
            med.append(np.median(qend)); avg.append(qend.mean())
        out[str(s)] = dict(p5=float(np.mean(p5)), p95=float(np.mean(p95)), max=float(np.mean(mx)),
                           median=float(np.mean(med)), mean=float(np.mean(avg)))
    return out


def saturation_test():
    """Structural fix candidate: requests respond to the stale premium only up to a cap G_cap. For each cap, refit
    (b, w) on G10's 2022-26 targets (19.3% in 2024Q1, ~12% in 2025Q2, ~10.5% in 2026Q1), then replay the GFC.
    Choosing the cap with the GFC makes the GFC in-sample for G_cap only (stated)."""
    base = replay_2022()
    qs_ = base["quarters"]
    gap22 = np.array(base["gap_pct"]) / 100
    e22 = ["N", "N"] + ["D"] * 8 + ["N"] * 9
    g = gfc()
    gapg = np.array(g["gap_pct"]) / 100
    out = {}
    for cap in (None, 0.30, 0.25, 0.20, 0.15, 0.10):
        best = None
        for b in np.linspace(0.02, 0.60, 117):
            for w in np.linspace(0.0, 0.30, 31):
                path, _, _ = queue_path(list(gap22), e22, 1 / (1 - 0.27), b=b, w=w, gcap=cap)
                err = ((path[qs_.index("2024Q1")] - 0.193) ** 2 + (path[qs_.index("2025Q2")] - 0.12) ** 2
                       + (path[qs_.index("2026Q1")] - 0.105) ** 2)
                if best is None or err < best[0]:
                    best = (err, b, w, path)
        qg, _, rg = queue_path(list(gapg), g["e_path"], 1 / (1 - 0.25), b=best[1], w=best[2], gcap=cap)
        i = int(np.argmax(qg))
        _, paid22, r22 = queue_path(list(gap22), e22, 1 / (1 - 0.27), b=best[1], w=best[2], gcap=cap)
        r23 = float(np.mean([r for k, r in zip(qs_, r22) if k.startswith("2023") and r is not None]))
        out["none" if cap is None else str(cap)] = dict(
            b=round(float(best[1]), 3), w=round(float(best[2]), 3), fit_rmse_pp=round(100 * np.sqrt(best[0] / 3), 2),
            q2024Q1=round(100 * best[3][qs_.index("2024Q1")], 1), q2026Q1=round(100 * best[3][qs_.index("2026Q1")], 1),
            gfc_peak_pct=round(100 * qg[i], 1), gfc_peak_quarter=g["quarters"][i], payout_2023=round(r23, 3),
            gfc_pass=bool(12 <= 100 * qg[i] <= 24))
    return out


def markdown_test():
    """Structural fix candidate 2: requests are cancelled in proportion to the fund's own markdowns (the stale
    premium that motivated them is being removed): W += min(1, w_m x markdown) Q. Refit (b, w, w_m) on the
    2022-26 targets; replay the GFC (out of sample for all three parameters)."""
    base = replay_2022()
    qs_ = base["quarters"]
    gap22 = np.array(base["gap_pct"]) / 100
    mark22 = np.array(ODCE) / 100 - 0.009                   # ODCE total return less ~0.9% income = capital mark
    e22 = ["N", "N"] + ["D"] * 8 + ["N"] * 9
    g = gfc()
    gapg = np.array(g["gap_pct"]) / 100
    L_O, rdq = 0.25, 0.06 / 4
    npi_cap = np.array([NPI[k] / 100 for k in g["quarters"]]) - 0.0135   # NPI total less ~1.35% income (2007-09)
    markg = (npi_cap - L_O * rdq) / (1 - L_O)
    best = None
    for wm in (0.0, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0):
        for b in np.linspace(0.02, 0.60, 59):
            for w in np.linspace(0.0, 0.30, 16):
                path, _, _ = queue_path(list(gap22), e22, 1 / (1 - 0.27), b=b, w=w, mark=list(mark22), wm=wm)
                err = ((path[qs_.index("2024Q1")] - 0.193) ** 2 + (path[qs_.index("2025Q2")] - 0.12) ** 2
                       + (path[qs_.index("2026Q1")] - 0.105) ** 2)
                if best is None or err < best[0] - 1e-12:
                    best = (err, b, w, wm)
    rows = {}
    for wm in (0.0, 2.0, 4.0, 6.0, 8.0):
        bb = None
        for b in np.linspace(0.02, 0.60, 59):
            for w in np.linspace(0.0, 0.30, 16):
                path, _, _ = queue_path(list(gap22), e22, 1 / (1 - 0.27), b=b, w=w, mark=list(mark22), wm=wm)
                err = ((path[qs_.index("2024Q1")] - 0.193) ** 2 + (path[qs_.index("2025Q2")] - 0.12) ** 2
                       + (path[qs_.index("2026Q1")] - 0.105) ** 2)
                if bb is None or err < bb[0]:
                    bb = (err, b, w)
        qg, _, _ = queue_path(list(gapg), g["e_path"], 1 / (1 - L_O), b=bb[1], w=bb[2], mark=list(markg), wm=wm)
        _, _, r22 = queue_path(list(gap22), e22, 1 / (1 - 0.27), b=bb[1], w=bb[2], mark=list(mark22), wm=wm)
        r23 = float(np.mean([r for k, r in zip(qs_, r22) if k.startswith("2023") and r is not None]))
        i = int(np.argmax(qg))
        rows[str(wm)] = dict(b=round(float(bb[1]), 3), w=round(float(bb[2]), 3), fit_rmse_pp=round(100 * np.sqrt(bb[0] / 3), 2),
                             gfc_peak_pct=round(100 * qg[i], 1), gfc_peak_quarter=g["quarters"][i],
                             payout_2023=round(r23, 3), gfc_pass=bool(12 <= 100 * qg[i] <= 24))
    return dict(best_fit_2022_26=dict(b=float(best[1]), w=float(best[2]), wm=float(best[3]),
                                      fit_rmse_pp=round(100 * np.sqrt(best[0] / 3), 2)), by_wm=rows)


def main():
    res = dict(label=LBL, fitted=dict(b=B_FIT, w=W_FIT))
    res["A_gfc_base"] = gfc()
    sens = {}
    for L_O in (0.20, 0.30):
        sens[f"L_O={L_O}"] = gfc(L_O=L_O)
    for L_R in (0.30, 0.45):
        sens[f"L_R={L_R}"] = gfc(L_R=L_R)
    for base in ("2005Q4", "2007Q2"):
        sens[f"base={base}"] = gfc(base=base)
    for ev in ("harsher", "milder"):
        sens[f"window={ev}"] = gfc(e_variant=ev)
    res["A_gfc_sensitivity"] = {k: dict(peak_pct=v["peak_pct"], peak_quarter=v["peak_quarter"]) for k, v in sens.items()}
    pk = res["A_gfc_base"]["peak_pct"]
    peaks = [v["peak_pct"] for v in sens.values()] + [pk]
    res["A_gate"] = dict(peak_in_12_24=bool(12 <= pk <= 24),
                         timing_2008Q4_2010Q2=bool("2008Q4" <= res["A_gfc_base"]["peak_quarter"] <= "2010Q2"),
                         sensitivity_peak_range=[min(peaks), max(peaks)])
    res["B_2022_replay"] = replay_2022()
    r23 = res["B_2022_replay"]["payout_ratio_2023_mean"]
    res["B_gate"] = dict(payout_2023_mean=r23, in_2p5_10pct=bool(0.025 <= r23 <= 0.10))
    res["C_dispersion"] = dispersion()
    res["D_saturation"] = saturation_test()
    res["E_markdown_cancellation"] = markdown_test()
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    for k, v in res["D_saturation"].items():
        print("cap", k, v)
    print("markdown best fit on 2022-26:", res["E_markdown_cancellation"]["best_fit_2022_26"])
    for k, v in res["E_markdown_cancellation"]["by_wm"].items():
        print("  w_m", k, v)
    a = res["A_gfc_base"]
    print("GFC base: peak", a["peak_pct"], "% at", a["peak_quarter"])
    print("  quarters", a["quarters"])
    print("  gap %   ", a["gap_pct"])
    print("  queue % ", a["queue_pct"])
    print("  payout  ", a["payout_ratio"])
    print("sensitivity:", res["A_gfc_sensitivity"])
    print("gate A:", res["A_gate"])
    print("2022 replay queue:", dict(zip(res["B_2022_replay"]["quarters"], res["B_2022_replay"]["queue_pct"])))
    print("2023 payout ratios:", res["B_2022_replay"]["payout_ratio"][4:8], "mean", round(r23, 3), "gate B:", res["B_gate"])
    print("dispersion (4Q24, 25 funds):", json.dumps(res["C_dispersion"]))


if __name__ == "__main__":
    main()
