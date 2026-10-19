"""
RA gap 02 - sealed SYNTHETIC per-tranche debt tape for the ten-sleeve Real Assets census of record (RA report s11).

*** SYNTHETIC - NOT ADIC DATA. Generated once (seed 20261019), written with a SHA-256 seal; the engine verifies the
seal and never regenerates. ***

Census (RA s11): NAV / unfunded / look-through LTV per sleeve; look-through debt $17.43bn, GAV $35.43bn (49.2%).
Calibration anchors (sources in ra_gap_02.md):
  Real estate  MBA (9 Feb 2026): 17% of CRE balances mature in 2026; by holder CMBS/CLO 25%, credit companies 29%,
               banks 21%, life companies 10%.  CBRE Q2-2026 originations: LTV 59.6%, DSCR 1.43, DY 10.2%, spread 204bp.
               Accordant Q1-2026: ODCE debt ~27% of assets, >75% fixed, cost ~4.5%.  CRED iQ (Mar 2023): ~40% of 682
               CRE-CLO loans had caps expiring before maturity.  Glancy (FEDS 2026-025): extensions after 2022 needed
               more paydown; non-recourse and low-debt-yield loans were 5-7pp less likely to be extended.
  Infrastructure  practitioner PF norms: sculpted to min DSCR ~1.20, lock-up ~1.10-1.20, default ~1.05 (Arthur Cox;
               G11 s5); gearing by archetype (G11), scaled to the census sleeve LTV; hedged 80-95% [P].
  ENR          OCC Comptroller's Handbook, O&G E&P Lending (v2.2): advance rates 50-65% of risk-adjusted PV, price deck
               below the futures curve, semiannual redeterminations plus 1-2 interim; Latham (2015): deficiencies cured
               in 3-6 monthly instalments.
Outputs: ra_tape_assets_v1.csv, ra_tape_tranches_v1.csv, ra_tape_manifest.json (hashes, calibration and s7.5 checks).
Run:  .venv\\Scripts\\python.exe -B ra_tape.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261019
OUT_A = os.path.join(HERE, "ra_tape_assets_v1.csv")
OUT_T = os.path.join(HERE, "ra_tape_tranches_v1.csv")
OUT_M = os.path.join(HERE, "ra_tape_manifest.json")
SOFR0 = 0.0389

CENSUS = {  # sleeve: (NAV, unfunded, LTV, positions, control, strategy)
    "RE_OE": (2.7, 0.0, 0.27, 6, "LP", "RE"),
    "RE_CE": (2.6, 1.2, 0.60, 14, "LP", "RE"),
    "RE_DIR_GL": (1.7, 0.2, 0.45, 6, "sole_joint", "RE"),
    "RE_DIR_GCC": (1.2, 0.2, 0.45, 2, "sole_joint", "RE"),
    "RE_COI": (0.8, 0.0, 0.60, 3, "minority", "RE"),
    "INF_OE": (2.0, 0.0, 0.50, 6, "LP", "INF"),
    "INF_CE": (2.5, 1.3, 0.55, 25, "LP", "INF"),
    "INF_DIR": (2.0, 0.3, 0.55, 20, "mixed", "INF"),
    "ENR_CE": (1.6, 0.6, 0.35, 16, "LP", "ENR"),
    "ENR_DIR": (0.9, 0.2, 0.40, 8, "mixed", "ENR"),
}
SECT_RE = ["LOG", "RES", "OFF", "RET", "DC", "HOT", "ALT"]
CAP_APP = {"LOG": 0.041, "RES": 0.043, "OFF": 0.062, "RET": 0.054, "DC": 0.048, "HOT": 0.075, "ALT": 0.053}
REG_ADJ = {"US": 0.0, "EU": 0.0025, "AS": 0.0, "GCC": 0.015}
# infrastructure archetypes (G11 s6.10): gearing, DSCR0, lock-up, fixed/hedged share, maturity (y), debt policy
ARCH = {
    "REG": dict(gear=0.65, dscr0=1.45, lock=1.15, h=0.85, mat=9, pol="bond"),
    "CON_IDX": dict(gear=0.80, dscr0=1.25, lock=1.20, h=0.95, mat=15, pol="pf"),
    "CON_FIX": dict(gear=0.75, dscr0=1.35, lock=1.20, h=0.90, mat=12, pol="pf"),
    "TOLL": dict(gear=0.60, dscr0=1.70, lock=1.15, h=0.80, mat=7, pol="bullet"),
    "AIR": dict(gear=0.55, dscr0=1.80, lock=1.15, h=0.85, mat=7, pol="bullet"),
    "MID": dict(gear=0.50, dscr0=2.50, lock=1.15, h=0.90, mat=6, pol="bullet"),
    "TOW": dict(gear=0.55, dscr0=2.00, lock=1.15, h=0.80, mat=6, pol="bullet"),
    "DC": dict(gear=0.50, dscr0=1.90, lock=1.15, h=0.60, mat=5, pol="termloan"),
    "MER": dict(gear=0.40, dscr0=1.80, lock=1.20, h=0.80, mat=8, pol="termloan"),
}
CF_YIELD = {"REG": 0.060, "CON_IDX": 0.072, "CON_FIX": 0.075, "TOLL": 0.058, "AIR": 0.055, "MID": 0.085,
            "TOW": 0.050, "DC": 0.048, "MER": 0.085}       # CFADS / EV at t0 [I]; equity yields as G11 y0
W_INF = {"INF_OE": {"REG": 30, "CON_IDX": 10, "CON_FIX": 5, "TOLL": 15, "AIR": 10, "MID": 10, "TOW": 10, "DC": 10},
         "INF_CE": {"REG": 10, "CON_IDX": 6, "CON_FIX": 18, "TOLL": 10, "AIR": 6, "MID": 10, "TOW": 12, "DC": 16,
                    "MER": 12},
         "INF_DIR": {"REG": 18, "CON_IDX": 8, "CON_FIX": 14, "TOLL": 12, "AIR": 8, "MID": 10, "TOW": 10, "DC": 12,
                     "MER": 8}}


def rnd(rng, lo, hi):
    return float(rng.uniform(lo, hi))


# MBA (9 Feb 2026) share of balances maturing in 2026 by holder -> remaining maturity ~ U{1..Q_max}, Q_max = 4/h
MBA_H = {"bank": 0.21, "life": 0.10, "cmbs": 0.25, "credit_co": 0.29, "gcc_bank": 0.21}


def mba_maturity(rng, holder, qmin=1):
    qmax = int(round(4.0 / MBA_H[holder]))
    return int(rng.integers(qmin, qmax + 1))


def mk_asset(**kw):
    base = dict(asset_id="", sleeve="", position_id="", strategy="", segment="", region="US", gcc_flag=0,
                control="", adic_share=1.0, gav_adic=0.0, noi_yield=0.0, capex_rate=0.0, dev_flag=0, age_q=0,
                enr_type="", decline=0.0, hedge_share=0.0, reset_phase_q=0, energy_link=0, unfunded_adic=0.0)
    base.update(kw)
    return base


def mk_tranche(**kw):
    base = dict(tranche_id="", asset_id="", pool_position="", sleeve="", lender="", balance_adic=0.0,
                commit_adic=0.0, ltv_t0_app=0.0, orig_year=2021, maturity_q=8, amort="IO", amort_years=0.0,
                rate_type="fixed", coupon=0.0, spread=0.0, swap_share=0.0, cap_strike=0.0, cap_expiry_q=0,
                ext_options=0, ext_len_q=4, ext_dscr=0.0, ext_dy=0.0, ext_ltv=0.0, ext_paydown=0.0,
                cov_trap_dscr=1.10, cov_default_dscr=1.00, cov_ltv_max=0.0, cov_dy_min=0.0,
                recourse="nonrecourse_carveouts", guarantee_share=0.0, rbl_adv=0.0, rbl_deck=0.0,
                rbl_redet_q=0, dev_ltc=0.0, controllable=0)
    base.update(kw)
    return base


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    assets, tranches = [], []
    na = nt = 0

    def aid():
        nonlocal na
        na += 1
        return f"SYN-RA-A{na:04d}"

    def tid():
        nonlocal nt
        nt += 1
        return f"SYN-RA-T{nt:04d}"

    # ---------------- RE_OE: 6 ODCE-type funds; 6 assets each, 4 mortgaged (LTV 40-60%), 1 fund line
    nav, unf, ltv, npos, ctrl, _ = CENSUS["RE_OE"]
    gav_s = nav / (1 - ltv)
    w_f = rng.dirichlet([4] * npos)
    mixes = [dict(LOG=35, RES=30, OFF=15, RET=10, ALT=10), dict(LOG=30, RES=35, OFF=15, RET=10, ALT=10),
             dict(LOG=40, RES=25, OFF=12, RET=13, ALT=10), dict(LOG=30, RES=30, OFF=20, RET=10, ALT=10),
             dict(LOG=35, RES=30, OFF=25, RET=10), dict(LOG=30, RES=35, OFF=25, RET=10)]
    for f in range(npos):
        pid = f"SYN-RA-P-REOE{f+1}"
        reg = "US" if f < 4 else "EU"
        share = rnd(rng, 0.03, 0.08)
        secs = list(mixes[f])
        p = np.array([mixes[f][k] for k in secs], float); p /= p.sum()
        gav_f = gav_s * w_f[f]
        sizes = rng.dirichlet([3] * 6) * gav_f
        ids = []
        for j in range(6):
            sec = str(rng.choice(secs, p=p))
            a = mk_asset(asset_id=aid(), sleeve="RE_OE", position_id=pid, strategy="RE", segment=sec, region=reg,
                         control=ctrl, adic_share=share, gav_adic=float(sizes[j]),
                         noi_yield=CAP_APP[sec] + REG_ADJ[reg] + rnd(rng, -0.002, 0.002),
                         capex_rate={"OFF": 0.025, "HOT": 0.04}.get(sec, 0.010))
            assets.append(a); ids.append(a)
        debt_f = ltv * gav_f
        mort_assets = ids[:4]
        mort_ltv = [rnd(rng, 0.40, 0.60) for _ in mort_assets]
        mort_bal = [l * a["gav_adic"] for l, a in zip(mort_ltv, mort_assets)]
        line_bal = max(0.0, debt_f - sum(mort_bal))
        if line_bal < 0.05 * debt_f:          # rescale mortgages so the fund line is ~15% of fund debt
            sc = 0.85 * debt_f / sum(mort_bal)
            mort_bal = [b * sc for b in mort_bal]
            line_bal = debt_f - sum(mort_bal)
        for a, b in zip(mort_assets, mort_bal):
            fixed = rng.random() < 0.88
            oy = int(rng.integers(2016, 2026))
            lender = str(rng.choice(["life", "bank", "cmbs"], p=[.5, .3, .2]))
            tranches.append(mk_tranche(
                tranche_id=tid(), asset_id=a["asset_id"], sleeve="RE_OE", lender=lender,
                balance_adic=b, commit_adic=b, ltv_t0_app=b / a["gav_adic"], orig_year=oy,
                maturity_q=mba_maturity(rng, lender), amort="IO" if rng.random() < 0.6 else "annuity30", amort_years=30.0,
                rate_type="fixed" if fixed else "floating",
                coupon=(0.033 if oy <= 2021 else 0.055) + rnd(rng, -0.004, 0.006) if fixed else 0.0,
                spread=0.0 if fixed else rnd(rng, 0.016, 0.022), cap_strike=0.0 if fixed else 0.045,
                cap_expiry_q=0 if fixed else int(rng.integers(2, 9)),
                cov_trap_dscr=1.15, cov_default_dscr=1.00, cov_ltv_max=0.0, recourse="nonrecourse_carveouts",
                guarantee_share=0.0))
        tranches.append(mk_tranche(
            tranche_id=tid(), asset_id="", pool_position=pid, sleeve="RE_OE", lender="bank_line",
            balance_adic=line_bal, commit_adic=line_bal * 1.6, ltv_t0_app=debt_f / gav_f, orig_year=2024,
            maturity_q=int(rng.integers(3, 12)), amort="revolver", rate_type="floating", spread=rnd(rng, 0.014, 0.0175),
            ext_options=2, ext_len_q=4, ext_dscr=1.50, ext_ltv=0.40, ext_paydown=0.0, cov_trap_dscr=0.0,
            cov_default_dscr=0.0, cov_ltv_max=0.35, recourse="fund_unsecured"))

    # ---------------- RE_CE: 14 VA/OP funds, 3 assets each, one loan per asset (bridge/transitional)
    nav, unf, ltv, npos, ctrl, _ = CENSUS["RE_CE"]
    gav_s = nav / (1 - ltv)
    w_f = rng.dirichlet([3] * npos)
    u_f = rng.dirichlet([2] * npos) * unf
    ce_mix = [dict(OFF=35, RES=30, LOG=20, RET=15), dict(RES=40, LOG=30, ALT=30), dict(LOG=40, RES=30, OFF=10, ALT=20),
              dict(RES=40, LOG=30, DC=10, ALT=20), dict(OFF=30, LOG=30, RES=30, RET=10), dict(LOG=40, RES=40, OFF=20),
              dict(OFF=50, RES=25, RET=25), dict(LOG=50, RES=30, OFF=20), dict(OFF=30, HOT=20, RES=25, RET=25),
              dict(RES=30, LOG=20, DC=20, HOT=10, ALT=20), dict(OFF=35, HOT=20, RES=25, LOG=20),
              dict(OFF=30, RES=30, LOG=20, HOT=20), dict(RES=35, LOG=25, ALT=40), dict(OFF=40, RET=30, HOT=30)]
    regions = ["US", "US", "US", "US", "EU", "EU", "US", "AS", "US", "US", "EU", "AS", "US", "AS"]
    ages = [7, 5, 3, 1, 5, 2, 6, 3, 8, 3, 5, 4, 2, 6]
    early_flags = list(rng.permutation([True] * 17 + [False] * 25))   # CRED iQ: ~40% of capped loans expire early
    for f in range(npos):
        style = "VA" if f < 8 else "OP"
        pid = f"SYN-RA-P-RECE{f+1}"
        mix = ce_mix[f]; secs = list(mix); p = np.array([mix[k] for k in secs], float); p /= p.sum()
        gav_f = gav_s * w_f[f]
        sizes = rng.dirichlet([3] * 3) * gav_f
        for j in range(3):
            sec = str(rng.choice(secs, p=p)); reg = regions[f]
            a = mk_asset(asset_id=aid(), sleeve="RE_CE", position_id=pid, strategy="RE", segment=sec, region=reg,
                         control=ctrl, adic_share=1.0, gav_adic=float(sizes[j]),
                         noi_yield=(0.054 if style == "VA" else 0.050) + rnd(rng, -0.006, 0.006) + REG_ADJ[reg],
                         capex_rate=0.015, age_q=4 * ages[f], unfunded_adic=float(u_f[f]) / 3)
            assets.append(a)
            l0 = float(np.clip(rng.normal(0.58 if style == "VA" else 0.64, 0.09), 0.35, 0.82))
            fl = rng.random() < 0.70
            r_m = rng.random()   # initial maturity: 30% within 4q, 25% within 5-8q, 45% 9-16q (MBA 25-29%/yr holders)
            m0 = int(rng.integers(1, 5)) if r_m < 0.30 else (int(rng.integers(5, 9)) if r_m < 0.55 else int(rng.integers(9, 17)))
            early = fl and early_flags.pop()            # CRED iQ: ~40% of caps expire before maturity
            tranches.append(mk_tranche(
                tranche_id=tid(), asset_id=a["asset_id"], sleeve="RE_CE",
                lender=str(rng.choice(["debt_fund_clo", "bank", "cmbs_sasb"], p=[.55, .30, .15])),
                balance_adic=l0 * a["gav_adic"], commit_adic=l0 * a["gav_adic"] * 1.05, ltv_t0_app=l0,
                orig_year=int(rng.integers(2021, 2026)), maturity_q=m0, amort="IO",
                rate_type="floating" if fl else "fixed", coupon=0.0 if fl else rnd(rng, 0.040, 0.066),
                spread=rnd(rng, 0.0275, 0.0425) if fl else 0.0, cap_strike=rnd(rng, 0.030, 0.050) if fl else 0.0,
                cap_expiry_q=(max(0, m0 - int(rng.integers(1, 5))) if early else m0) if fl else 0,
                ext_options=int(rng.integers(1, 3)) if fl else 0, ext_len_q=4, ext_dscr=rnd(rng, 1.10, 1.25),
                ext_dy=rnd(rng, 0.070, 0.085), ext_ltv=0.70, ext_paydown=0.025,
                cov_trap_dscr=1.05, cov_default_dscr=1.00, cov_dy_min=0.065, recourse="nonrecourse_sponsor_carry"))

    # ---------------- RE_DIR_GL: 6 JV / direct assets (one development data-centre JV)
    nav, unf, ltv, npos, ctrl, _ = CENSUS["RE_DIR_GL"]
    gav_s = nav / (1 - ltv)
    spec = [("LOG", "US", 0.90), ("RES", "US", 0.85), ("RES", "EU", 0.80), ("DC", "US", 0.80), ("LOG", "AS", 0.80),
            ("OFF", "EU", 1.0)]
    w = rng.dirichlet([5] * npos)
    for j, (sec, reg, sh) in enumerate(spec):
        pid = f"SYN-RA-P-REDGL{j+1}"
        dev = sec == "DC"
        a = mk_asset(asset_id=aid(), sleeve="RE_DIR_GL", position_id=pid, strategy="RE", segment=sec, region=reg,
                     control="sole" if sh == 1.0 else "joint", adic_share=sh, gav_adic=float(gav_s * w[j]),
                     noi_yield=CAP_APP[sec] + REG_ADJ[reg] + 0.006 + rnd(rng, -0.003, 0.003),
                     capex_rate={"OFF": 0.025}.get(sec, 0.008), dev_flag=int(dev), unfunded_adic=unf if dev else 0.0)
        assets.append(a)
        l0 = rnd(rng, 0.38, 0.52)
        lender = "bank" if j % 2 == 0 else "life"
        swapped = rng.random() < 0.75
        if dev:   # development asset: construction facility only (LTC 55%), drawn to ~50% of as-is value
            commit = 0.55 * (a["gav_adic"] + unf)
            tranches.append(mk_tranche(
                tranche_id=tid(), asset_id=a["asset_id"], sleeve="RE_DIR_GL", lender="bank_construction",
                balance_adic=0.50 * a["gav_adic"], commit_adic=commit, ltv_t0_app=0.50, orig_year=2025, maturity_q=12,
                amort="IO", rate_type="floating", spread=0.0275, cap_strike=0.045, cap_expiry_q=8,
                ext_options=2, ext_len_q=2, ext_dscr=0.0, ext_ltv=0.60, cov_trap_dscr=0.0, cov_default_dscr=0.0,
                recourse="completion_guarantee", guarantee_share=1.0, dev_ltc=0.55, controllable=1))
            continue
        tranches.append(mk_tranche(
            tranche_id=tid(), asset_id=a["asset_id"], sleeve="RE_DIR_GL", lender=lender,
            balance_adic=l0 * a["gav_adic"], commit_adic=l0 * a["gav_adic"], ltv_t0_app=l0,
            orig_year=int(rng.integers(2018, 2026)),
            maturity_q=mba_maturity(rng, lender),
            amort="annuity30" if lender == "life" else "IO", amort_years=30.0,
            rate_type="fixed" if lender == "life" else ("swapped" if swapped else "floating"),
            coupon=rnd(rng, 0.036, 0.058) if lender == "life" else 0.0,
            spread=rnd(rng, 0.017, 0.022) if lender == "bank" else 0.0, swap_share=1.0 if (lender == "bank" and swapped) else 0.0,
            cap_strike=0.045 if (lender == "bank" and not swapped) else 0.0,
            cap_expiry_q=int(rng.integers(2, 9)) if (lender == "bank" and not swapped) else 0,
            ext_options=1 if lender == "bank" else 0, ext_len_q=4, ext_dscr=1.25, ext_ltv=0.60, ext_paydown=0.025,
            cov_trap_dscr=1.15 if lender == "life" else 1.10, cov_default_dscr=1.00,
            cov_ltv_max=0.65 if lender == "bank" else 0.0, recourse="nonrecourse_carveouts",
            guarantee_share=0.15, controllable=1))

    # ---------------- RE_DIR_GCC: 4 Gulf assets, GCC bank loans (amortising, floating, half swapped, guarantees)
    nav, unf, ltv, npos, ctrl, _ = CENSUS["RE_DIR_GCC"]
    gav_s = nav / (1 - ltv)
    spec = [("OFF", 0.30), ("RET", 0.25), ("HOT", 0.20), ("RES", 0.25)]
    for j, (sec, wj) in enumerate(spec):
        pid = f"SYN-RA-P-REGCC{j+1}"
        a = mk_asset(asset_id=aid(), sleeve="RE_DIR_GCC", position_id=pid, strategy="RE", segment=sec, region="GCC",
                     gcc_flag=1, control="sole", adic_share=1.0, gav_adic=gav_s * wj,
                     noi_yield=CAP_APP[sec] + REG_ADJ["GCC"] + rnd(rng, -0.003, 0.003),
                     capex_rate={"HOT": 0.04}.get(sec, 0.010), unfunded_adic=unf if j == 0 else 0.0)
        assets.append(a)
        l0 = rnd(rng, 0.38, 0.52)
        tranches.append(mk_tranche(
            tranche_id=tid(), asset_id=a["asset_id"], sleeve="RE_DIR_GCC", lender="gcc_bank",
            balance_adic=l0 * a["gav_adic"], commit_adic=l0 * a["gav_adic"], ltv_t0_app=l0, orig_year=int(rng.integers(2020, 2026)),
            maturity_q=mba_maturity(rng, "gcc_bank"), amort="annuity", amort_years=float(rng.integers(18, 26)),
            rate_type="floating", spread=rnd(rng, 0.0175, 0.0250), swap_share=0.5,
            cov_trap_dscr=1.15, cov_default_dscr=1.05, cov_ltv_max=0.65, recourse="corporate_guarantee" if j in (0, 2) else "nonrecourse_carveouts",
            guarantee_share=1.0 if j in (0, 2) else 0.15, controllable=1))

    # ---------------- RE_COI: 3 minority co-investments, sponsor financing (CO1 senior + mezz)
    nav, unf, ltv, npos, ctrl, _ = CENSUS["RE_COI"]
    gav_s = nav / (1 - ltv)
    spec = [("OFF", "US", 0.60, 6, 0.30), ("LOG", "EU", 0.50, 12, 0.60), ("ALT", "US", 0.60, 10, 0.40)]
    w = np.array([0.33, 0.33, 0.34])
    for j, (sec, reg, l0, mq, fx) in enumerate(spec):
        pid = f"SYN-RA-P-RECO{j+1}"
        a = mk_asset(asset_id=aid(), sleeve="RE_COI", position_id=pid, strategy="RE", segment=sec, region=reg,
                     control="minority", adic_share=1.0, gav_adic=float(gav_s * w[j]),
                     noi_yield=CAP_APP[sec] + REG_ADJ[reg] + 0.008, capex_rate=0.015)
        assets.append(a)
        parts = [(l0 - 0.10, "senior"), (0.10, "mezz")] if j == 0 else [(l0, "senior")]
        for lj, kind in parts:
            fl = rng.random() > fx
            tranches.append(mk_tranche(
                tranche_id=tid(), asset_id=a["asset_id"], sleeve="RE_COI", lender="cmbs_sasb" if kind == "senior" else "mezz_fund",
                balance_adic=lj * a["gav_adic"], commit_adic=lj * a["gav_adic"], ltv_t0_app=l0, orig_year=2022,
                maturity_q=mq, amort="IO", rate_type="floating" if fl else "fixed",
                coupon=0.0 if fl else (0.052 if kind == "senior" else 0.095),
                spread=(0.030 if kind == "senior" else 0.070) if fl else 0.0, cap_strike=0.040 if fl else 0.0,
                cap_expiry_q=(max(0, mq - 2) if j == 0 else mq) if fl else 0, ext_options=1 if fl else 0, ext_len_q=4, ext_dscr=1.15,
                ext_dy=0.075, ext_ltv=0.70, ext_paydown=0.03, cov_trap_dscr=1.05, cov_dy_min=0.065,
                recourse="nonrecourse_sponsor"))

    # ---------------- infrastructure sleeves
    def infra_sleeve(sl, n_assets, ctrl_rule):
        nonlocal assets, tranches
        nav, unf, ltv, npos, ctrl, _ = CENSUS[sl]
        gav_s = nav / (1 - ltv)
        wmap = W_INF[sl]; keys = list(wmap); p = np.array([wmap[k] for k in keys], float); p /= p.sum()
        segs = [str(s) for s in rng.choice(keys, size=n_assets, p=p)]
        size = rng.dirichlet([2.5] * n_assets) * gav_s
        g_raw = np.array([ARCH[s]["gear"] for s in segs])
        gscale = ltv * gav_s / float((g_raw * size).sum())
        n_pos = max(1, min(npos, n_assets // 2 if sl != "INF_DIR" else n_assets))
        u_split = rng.dirichlet([2] * n_pos) * unf
        for j, sg in enumerate(segs):
            posn = j % n_pos
            pid = f"SYN-RA-P-{sl.replace('_', '')}{posn+1}"
            control = ctrl_rule(j)
            a = mk_asset(asset_id=aid(), sleeve=sl, position_id=pid, strategy="INF", segment=sg,
                         region=str(rng.choice(["US", "EU", "AS", "GCC"], p=[.45, .40, .10, .05])),
                         control=control, adic_share=1.0 if sl != "INF_DIR" else rnd(rng, 0.15, 0.60),
                         gav_adic=float(size[j]), noi_yield=CF_YIELD[sg] + rnd(rng, -0.004, 0.004),
                         dev_flag=int(sg == "DC" and rng.random() < 0.4), reset_phase_q=int(rng.integers(1, 21)),
                         energy_link=int(sg == "MID"), age_q=int(rng.integers(4, 40)),
                         unfunded_adic=float(u_split[posn]) / max(1, sum(1 for k in range(n_assets) if k % n_pos == posn)))
            a["gcc_flag"] = int(a["region"] == "GCC")
            assets.append(a)
            arc = ARCH[sg]
            gear = float(np.clip(arc["gear"] * gscale * rnd(rng, 0.9, 1.1), 0.15, 0.85))
            debt = gear * a["gav_adic"]
            ctl = int(control in ("sole", "joint"))
            if arc["pol"] == "pf":
                tranches.append(mk_tranche(
                    tranche_id=tid(), asset_id=a["asset_id"], sleeve=sl, lender="pf_bank_club", balance_adic=debt,
                    commit_adic=debt, ltv_t0_app=gear, orig_year=int(rng.integers(2014, 2025)),
                    maturity_q=4 * int(rng.integers(10, 20)), amort="sculpted", amort_years=float(rng.integers(10, 20)),
                    rate_type="swapped", spread=rnd(rng, 0.0125, 0.0175), swap_share=arc["h"],
                    coupon=rnd(rng, 0.030, 0.050), cov_trap_dscr=arc["lock"], cov_default_dscr=1.05,
                    recourse="nonrecourse_project", controllable=ctl))
            elif arc["pol"] == "bond":   # regulated opco bonds: laddered fixed + a floating bank tranche
                for part, sh in (("bond", arc["h"]), ("bank", 1 - arc["h"])):
                    tranches.append(mk_tranche(
                        tranche_id=tid(), asset_id=a["asset_id"], sleeve=sl, lender="opco_bond" if part == "bond" else "bank",
                        balance_adic=debt * sh, commit_adic=debt * sh, ltv_t0_app=gear, orig_year=int(rng.integers(2014, 2025)),
                        maturity_q=int(rng.integers(4, 49)) if part == "bond" else int(rng.integers(4, 21)), amort="IO",
                        rate_type="fixed" if part == "bond" else "floating",
                        coupon=rnd(rng, 0.028, 0.055) if part == "bond" else 0.0,
                        spread=rnd(rng, 0.010, 0.014) if part == "bank" else 0.0,
                        cov_trap_dscr=0.0, cov_default_dscr=0.0, cov_ltv_max=0.78, recourse="nonrecourse_opco",
                        controllable=ctl))
            else:   # holdco / opco bullets and term loans
                hedge = arc["h"]
                tranches.append(mk_tranche(
                    tranche_id=tid(), asset_id=a["asset_id"], sleeve=sl,
                    lender="holdco_bank" if arc["pol"] == "termloan" else "opco_bond_bank", balance_adic=debt,
                    commit_adic=debt, ltv_t0_app=gear, orig_year=int(rng.integers(2017, 2026)),
                    maturity_q=int(rng.integers(2, 4 * arc["mat"] + 1)), amort="IO",
                    rate_type="swapped" if hedge >= 0.8 else "floating", swap_share=hedge,
                    coupon=rnd(rng, 0.032, 0.058), spread=rnd(rng, 0.0175, 0.030),
                    cap_strike=0.045 if hedge < 0.8 else 0.0, cap_expiry_q=int(rng.integers(4, 13)) if hedge < 0.8 else 0,
                    ext_options=1 if arc["pol"] == "termloan" else 0, ext_len_q=4, ext_dscr=1.40, ext_ltv=0.65,
                    cov_trap_dscr=arc["lock"] + 0.05, cov_default_dscr=1.05, cov_ltv_max=0.70 if arc["pol"] == "termloan" else 0.0,
                    recourse="nonrecourse_holdco", controllable=ctl))
            if a["dev_flag"]:
                commit = 0.25 * a["gav_adic"]
                tranches.append(mk_tranche(
                    tranche_id=tid(), asset_id=a["asset_id"], sleeve=sl, lender="construction_bank", balance_adic=0.4 * commit,
                    commit_adic=commit, orig_year=2025, maturity_q=12, amort="IO", rate_type="floating", spread=0.0250,
                    cap_strike=0.045, cap_expiry_q=8, ext_options=2, ext_len_q=2, cov_trap_dscr=0.0, cov_default_dscr=0.0,
                    recourse="completion_guarantee" if ctl else "sponsor_completion", guarantee_share=1.0 if ctl else 0.0,
                    dev_ltc=0.60, controllable=ctl))

    infra_sleeve("INF_OE", 30, lambda j: "LP")
    infra_sleeve("INF_CE", 36, lambda j: "LP")
    infra_sleeve("INF_DIR", 14, lambda j: "sole" if j % 4 == 0 else ("joint" if j % 4 == 1 else "minority"))

    # ---------------- ENR sleeves
    def enr_sleeve(sl, spec):
        nav, unf, ltv, npos, ctrl, _ = CENSUS[sl]
        gav_s = nav / (1 - ltv)
        tot_w = sum(s[1] for s in spec)
        debt_target = ltv * gav_s
        raw = []
        for j, (typ, wj, lev, control) in enumerate(spec):
            pid = f"SYN-RA-P-{sl.replace('_', '')}{j+1}"
            a = mk_asset(asset_id=aid(), sleeve=sl, position_id=pid, strategy="ENR", segment=typ,
                         region="US", control=control, adic_share=1.0, gav_adic=gav_s * wj / tot_w,
                         noi_yield={"PDP": 0.11, "MID": 0.080, "ROY": 0.09, "OTH": 0.06}[typ],   # FCF after maintenance capex [I]
                         enr_type=typ, decline={"PDP": 0.12, "ROY": 0.08}.get(typ, 0.0),
                         hedge_share=rnd(rng, 0.50, 0.75) if typ == "PDP" else 0.0, energy_link=1,
                         age_q=int(rng.integers(4, 24)), unfunded_adic=unf * wj / tot_w)
            assets.append(a)
            raw.append((a, typ, lev))
        scale = debt_target / sum(a["gav_adic"] * lev for a, _, lev in raw)
        for a, typ, lev in raw:
            d = a["gav_adic"] * lev * scale
            if d <= 1e-6:
                continue
            ctl = int(a["control"] in ("sole", "joint"))
            if typ in ("PDP", "ROY"):
                tranches.append(mk_tranche(
                    tranche_id=tid(), asset_id=a["asset_id"], sleeve=sl, lender="rbl_syndicate", balance_adic=d,
                    commit_adic=d * 1.3, ltv_t0_app=d / a["gav_adic"], orig_year=int(rng.integers(2022, 2026)),
                    maturity_q=int(rng.integers(8, 21)), amort="revolver", rate_type="floating",
                    spread=rnd(rng, 0.025, 0.035), rbl_adv=rnd(rng, 0.55, 0.65), rbl_deck=0.85,
                    rbl_redet_q=int(rng.integers(1, 3)), cov_trap_dscr=0.0, cov_default_dscr=0.0,
                    recourse="nonrecourse_rbl", controllable=ctl))
            else:
                tranches.append(mk_tranche(
                    tranche_id=tid(), asset_id=a["asset_id"], sleeve=sl, lender="notes", balance_adic=d, commit_adic=d,
                    ltv_t0_app=d / a["gav_adic"], orig_year=int(rng.integers(2019, 2026)),
                    maturity_q=int(rng.integers(4, 33)), amort="IO", rate_type="fixed", coupon=rnd(rng, 0.045, 0.070),
                    cov_trap_dscr=1.20, cov_default_dscr=1.05, cov_ltv_max=0.0, recourse="nonrecourse_holdco",
                    controllable=ctl))

    enr_sleeve("ENR_CE", [("PDP", 0.12, 0.55, "LP")] * 6 + [("MID", 0.10, 0.45, "LP")] * 3 + [("ROY", 0.06, 0.15, "LP")])
    enr_sleeve("ENR_DIR", [("PDP", 0.15, 0.45, "minority"), ("PDP", 0.15, 0.45, "minority"), ("MID", 0.25, 0.50, "joint"),
                           ("MID", 0.25, 0.50, "joint"), ("ROY", 0.10, 0.20, "sole"), ("ROY", 0.10, 0.0, "sole"),
                           ("OTH", 0.10, 0.0, "minority")])

    # ---------------- rescale debt to the census look-through debt exactly (per sleeve)
    for sl, (nav, unf, ltv, *_r) in CENSUS.items():
        target = nav * ltv / (1 - ltv)
        ts = [t for t in tranches if t["sleeve"] == sl]
        cur = sum(t["balance_adic"] for t in ts)
        for t in ts:
            k = target / cur
            t["balance_adic"] *= k
            t["commit_adic"] *= k
        gav_target = nav / (1 - ltv)
        as_ = [a for a in assets if a["sleeve"] == sl]
        g = sum(a["gav_adic"] for a in as_)
        for a in as_:
            a["gav_adic"] *= gav_target / g
    # recompute appraisal LTV per secured tranche
    amap = {a["asset_id"]: a for a in assets}
    for t in tranches:
        if t["asset_id"]:
            same = [u for u in tranches if u["asset_id"] == t["asset_id"]]
            t["ltv_t0_app"] = sum(u["balance_adic"] for u in same) / amap[t["asset_id"]]["gav_adic"]
    return assets, tranches


def to_csv(rows, header_note):
    buf = io.StringIO()
    buf.write(header_note + "\n")
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})
    return buf.getvalue()


def checks(assets, tranches):
    amap = {a["asset_id"]: a for a in assets}
    out = {}
    tot_debt = sum(t["balance_adic"] for t in tranches)
    tot_gav = sum(a["gav_adic"] for a in assets)
    out["lookthrough_debt_bn"] = round(tot_debt, 3)
    out["lookthrough_gav_bn"] = round(tot_gav, 3)
    out["lookthrough_ltv"] = round(tot_debt / tot_gav, 4)

    def mat_share(ts, h):
        b = sum(t["balance_adic"] for t in ts)
        return round(sum(t["balance_adic"] for t in ts if 0 < t["maturity_q"] <= h) / b, 4) if b else None

    by = {}
    for sl in CENSUS:
        ts = [t for t in tranches if t["sleeve"] == sl]
        b = sum(t["balance_adic"] for t in ts)
        fl = sum(t["balance_adic"] * (1 - t["swap_share"]) for t in ts if t["rate_type"] in ("floating", "swapped"))
        capped = sum(t["balance_adic"] * (1 - t["swap_share"]) for t in ts
                     if t["rate_type"] in ("floating", "swapped") and t["cap_strike"] > 0)
        cap_before = sum(t["balance_adic"] for t in ts if t["cap_strike"] > 0 and t["cap_expiry_q"] < t["maturity_q"])
        nfl = sum(t["balance_adic"] for t in ts if t["rate_type"] == "floating" and t["cap_strike"] > 0)
        by[sl] = {"tranches": len(ts), "debt_bn": round(b, 3), "maturing_12m": mat_share(ts, 4),
                  "maturing_24m": mat_share(ts, 8), "floating_share": round(fl / b, 3) if b else None,
                  "unhedged_floating_share": round((fl - capped) / b, 3) if b else None,
                  "caps_expiring_before_maturity_share_of_capped_floating": round(cap_before / nfl, 3) if nfl else None,
                  "w_avg_maturity_years": round(sum(t["balance_adic"] * t["maturity_q"] for t in ts) / b / 4, 2) if b else None}
    out["by_sleeve"] = by
    re_ts = [t for t in tranches if t["sleeve"].startswith("RE_")]
    out["real_estate"] = {"maturing_12m": mat_share(re_ts, 4), "maturing_24m": mat_share(re_ts, 8),
                          "targets": "MBA 2026: 17% of all CRE balances mature in the year (CMBS/CLO 25%, credit cos 29%, "
                                     "banks 21%, life cos 10%); G10 RE book 42% within 24 months"}
    out["all"] = {"maturing_12m": mat_share(tranches, 4), "maturing_24m": mat_share(tranches, 8),
                  "G15_uniform_assumption": "17% a year (MBA 2026 snapshot), i.e. 17% / 34%"}
    # s7.5 controllable-debt tests (origination tests applied to the legacy book at t0, appraisal basis)
    ctl = [t for t in tranches if t["controllable"]]
    cb = sum(t["balance_adic"] for t in ctl)
    ctl_assets = {t["asset_id"] for t in ctl if t["asset_id"]}
    cg = sum(amap[a]["gav_adic"] for a in ctl_assets)
    single = []
    for a in ctl_assets:
        aa = amap[a]
        d = sum(t["balance_adic"] for t in ctl if t["asset_id"] == a and t["recourse"] != "completion_guarantee")
        lim = 0.70 if aa["segment"] in ("REG", "CON_IDX", "CON_FIX") else (0.40 if aa["enr_type"] in ("PDP", "ROY") else 0.65)
        basis = aa["gav_adic"] * (0.85 if aa["enr_type"] in ("PDP", "ROY") else 1.0)   # RBL test on deck PV
        single.append({"asset": a, "sleeve": aa["sleeve"], "segment": aa["segment"], "ltv": round(d / basis, 3),
                       "limit": lim, "breach": bool(d / basis > lim)})
    fl_ctl = sum(t["balance_adic"] * (1 - t["swap_share"]) for t in ctl if t["rate_type"] in ("floating", "swapped")
                 and t["cap_strike"] == 0)
    fl_cap_short = sum(t["balance_adic"] * (1 - t["swap_share"]) for t in ctl
                       if t["rate_type"] in ("floating", "swapped") and 0 < t["cap_strike"] and t["cap_expiry_q"] < t["maturity_q"])
    dev = [t for t in ctl if t["dev_ltc"] > 0]
    out["s7_5_controllable"] = {
        "controllable_debt_bn": round(cb, 3), "controllable_gav_bn": round(cg, 3),
        "portfolio_ltv": round(cb / cg, 4), "portfolio_target_45pct": bool(cb / cg <= 0.45), "portfolio_hard_55pct": bool(cb / cg <= 0.55),
        "maturing_12m": mat_share(ctl, 4), "test_12m_le_25pct": bool(mat_share(ctl, 4) <= 0.25),
        "maturing_24m": mat_share(ctl, 8), "test_24m_le_40pct": bool(mat_share(ctl, 8) <= 0.40),
        "unhedged_floating_share": round(fl_ctl / cb, 4), "unhedged_or_cap_short_share": round((fl_ctl + fl_cap_short) / cb, 4),
        "test_unhedged_le_25pct": bool(fl_ctl / cb <= 0.25),
        "test_hedged_to_maturity": bool(fl_cap_short == 0),
        "single_asset_breaches": [s for s in single if s["breach"]], "single_asset_n": len(single),
        "development_ltc_max": max([t["dev_ltc"] for t in dev], default=0.0), "test_dev_ltc_le_60pct": all(t["dev_ltc"] <= 0.60 for t in dev),
        "note": "P(covenant trigger within 12m) <= 2% per loan is evaluated in ra_engine (simulation)"}
    # recourse measure (T5 limit 1 inputs): guarantees by type
    rec = {}
    for t in tranches:
        if t["guarantee_share"] > 0 and t["controllable"]:
            k = t["recourse"]
            w = {"completion_guarantee": 1.0, "corporate_guarantee": 1.0}.get(k, 0.10)   # carve-outs at 10% [I]
            expo = (t["commit_adic"] if k == "completion_guarantee" else t["balance_adic"]) * t["guarantee_share"] * w
            rec[k] = round(rec.get(k, 0.0) + expo, 4)
    out["t5_recourse_exposure_bn"] = rec
    return out


def maturity_profile(tranches):
    out = []
    for sl in CENSUS:
        ts = [t for t in tranches if t["sleeve"] == sl]
        b = sum(t["balance_adic"] for t in ts)
        for h in (4, 8):
            out.append(sum(t["balance_adic"] for t in ts if 0 < t["maturity_q"] <= h) / b)
    return np.array(out)


def select_seed(n_ref=200, n_cand=64):
    """Pre-stated selection rule (fixed before any engine run): among n_cand candidate seeds, keep the tape whose
    sleeve-level 12- and 24-month maturity shares deviate least (max abs) from the generator's own expectation
    (mean over n_ref reference seeds). It targets representativeness only, never an engine outcome."""
    ref = np.mean([maturity_profile(build(SEED + 1000 + k)[1]) for k in range(n_ref)], axis=0)
    best = None
    for k in range(n_cand):
        dev = float(np.abs(maturity_profile(build(SEED + k)[1]) - ref).max())
        if best is None or dev < best[1]:
            best = (SEED + k, dev)
    return best[0], best[1], ref


def main():
    seed, dev, ref = select_seed()
    assets, tranches = build(seed)
    note = "# SYN-ADIC-177 Real Assets debt tape v1 (ra_gap_02). SYNTHETIC - NOT ADIC DATA. seed=%d. USD bn at ADIC share." % seed
    ca = to_csv(assets, note + " ASSETS")
    ct = to_csv(tranches, note + " TRANCHES")
    with open(OUT_A, "w", encoding="utf-8", newline="") as fh:
        fh.write(ca)
    with open(OUT_T, "w", encoding="utf-8", newline="") as fh:
        fh.write(ct)
    ha = hashlib.sha256(ca.encode("utf-8")).hexdigest()
    ht = hashlib.sha256(ct.encode("utf-8")).hexdigest()
    keys = [f"{sl}_{h}m" for sl in CENSUS for h in (12, 24)]
    man = {"label": "SYNTHETIC - NOT ADIC DATA", "seed": seed, "generated": "2026-10-19",
           "selection_rule": "min over 64 candidate seeds of the max abs deviation of sleeve 12/24-month maturity "
                             "shares from the generator expectation (200 reference seeds); chosen before any engine run",
           "selection_max_abs_dev": round(dev, 4),
           "generator_expected_maturity_shares": dict(zip(keys, [round(float(v), 4) for v in ref])),
           "files": {os.path.basename(OUT_A): ha, os.path.basename(OUT_T): ht},
           "n_assets": len(assets), "n_tranches": len(tranches), "checks": checks(assets, tranches),
           "V_mat_definition": "V^mat_{i,T} = omega_i * V*_{i,T}: ADIC share of the nowcast economic value of tranche i's own "
                               "collateral at its (possibly extended) maturity quarter T, from that collateral's simulated "
                               "path (RE: NOI(1+g)/c; INF: structural V^A; ENR: PV at the strip; RBL: PV at the bank deck). "
                               "Pool-secured fund lines use the pool. Maintenance covenants test appraisal V^A; refinancing "
                               "capacity tests V^mat."}
    with open(OUT_M, "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=1)
    print(json.dumps(man, indent=1))


if __name__ == "__main__":
    main()
