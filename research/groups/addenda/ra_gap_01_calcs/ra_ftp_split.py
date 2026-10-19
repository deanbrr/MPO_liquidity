"""FTP_RA split into the scheduled part (calls less distributions) and the cure part (cures, protective calls and
distribution stops), so FTP and CLC price each item once (main s4.11). SYNTHETIC - NOT ADIC DATA.
Run: <venv>/python.exe -I -B ra_ftp_split.py  (writes ra_ftp_split_results.json)"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra_book as B  # noqa: E402
import ra_ladder as RL  # noqa: E402

CAL = json.load(open(os.path.join(HERE, "ra_calib_results.json"), encoding="utf-8"))
out = {}
for book in ("v2u16", "v2u11"):
    th = CAL["theta_star"][book]["theta"]
    s = RL.s_star(th)
    base = RL.lev_of(reserve=0.0, book=book, census="v1")
    coef = RL.coefficients(s, base, th)
    for st in ("R1", "R0"):
        rr = RL.restore_and_solve(coef, st)
        sol = rr["restored"]
        lv = RL.plan_lev(coef, sol, base)
        r = RL.gl_ladder(s, lv, theta=th)
        ra = r["ra"]
        mu = sol["mu"]
        sched = np.cumsum(ra["calls"] - ra["income"] - ra["realiz"])[:24]
        cure = np.cumsum(ra["cures"] + ra["prot_calls"] + ra["dist_stop"])[:24]
        nav = 18.0
        out[f"{book}|{st}"] = dict(theta=th, mu_sum=float(mu.sum()),
                                   ftp_total_bp=1e4 * float(mu @ (sched + cure)) / (5 * nav),
                                   ftp_scheduled_bp=1e4 * float(mu @ sched) / (5 * nav),
                                   ftp_cure_bp=1e4 * float(mu @ cure) / (5 * nav),
                                   nco24_scheduled=float(sched[-1]), nco24_cure=float(cure[-1]))
        print(book, st, {k: round(v, 3) for k, v in out[f'{book}|{st}'].items()})
# CLC as bp of RA NAV a year
main = json.load(open(os.path.join(HERE, "ra_main_results.json"), encoding="utf-8"))
for k, v in main["clc"].items():
    out[f"clc|{k}"] = dict(clc_m=1e3 * v["clc_bn_yr_15pct_pooled"], clc_bp_of_ra_nav=1e4 * v["clc_bn_yr_15pct_pooled"] / 18.0,
                          clc_m_worst=1e3 * v["clc_bn_yr_15pct_worst"])
    print(k, {kk: round(vv, 2) for kk, vv in out[f'clc|{k}'].items()})
with open(os.path.join(HERE, "ra_ftp_split_results.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
