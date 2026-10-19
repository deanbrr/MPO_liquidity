"""
ri_mc (item 3): red-event probability (T6: any liquidity-driven red sale or failed attempt, or a payout below the
owner's call, within 5 years) for do-nothing, Mix A and Mix B, M1-M6, v1 versus v2. SYNTHETIC - NOT ADIC DATA.

Two engines, both the local copy of ra_gap_01's ra_engine (itself gap_04's engine extended with the RA module):
  playbook-free ('t1'): gap_02's certification engine - rate-mode groups, t1 overlay and stage, gap_02 initial
     state (drought, Z0 = GW with p 0.7), no group playbooks, no contingent budgets. For v2 the Real Assets cash flows
     run (RA state machine) and RA follows the policy's pacing rule, but RA's own playbook (open-end notices, JV
     sell-downs, cash-outs, ENR SELL) is off, so the engine stays playbook-free. 50,000 paths; one-sided 95%
     Clopper-Pearson bounds. Reproduces gap_02's certified mixes on the published v1 book (Cfg.t1()).
  integrated: groups gap_04's engine with group playbooks (cohort groups, L1 overlay, CFP stage machine with the
     T4' survival proxy at the book's own theta*, current contingent-budget triggers, links), the October-2026
     initial state; v2 adds Real Assets as the tenth player with its playbook. 20,000 paths.
Policies (gap_02 s2.3): Mix A = revolver $15bn, pacing $6bn + stage cut, reserve 14%; Mix B = revolver $10bn,
pacing $12bn + stage cut, owner band, reserve 8%, $5bn hedge-fund notice; do-nothing = $12bn pacing, 8% reserve,
hedge-fund notices at Amber. Seed 20261018 everywhere (common random numbers across books and policies).
The 'stressed class' is M6 (BlackRock risk-premia-rise + persistent drought + overlay stress), as in gap_02.
Run: <venv>/python.exe -I -B ri_mc.py  -> ri_mc_results.json
"""
from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ri_common as C  # noqa: E402

N_T1 = 50000
N_INT = 20000
WORKERS = 23
KEYS = ("p_red", "k_red", "cp_upper_red", "p_black", "p_black_12m", "cp_upper_black_12m", "p_band_12m",
        "mean_wtilde", "mean_withheld", "mean_commit_forgone", "mean_red_sales", "p_covenant", "max_debt_ratio_p99")


def cfg_for(engine, book, theta, raoff=False):
    import ra_engine as R
    bk = C.BOOKS[book]
    has_ra = R.RB.BOOKS[bk["rb_book"]]["ra"]
    census = "gc2" if bk["census"] == "gap02" else "v1"
    if engine == "t1":
        players = frozenset(R.PLAYERS) if has_ra else frozenset(R.PLAYERS9)
        return R.Cfg(init="gap02", groups="rate", overlay="t1", links=False, stage="t1", census=census,
                     players=players, trigger="none", book=bk["rb_book"], theta=theta,
                     ra_notices=False, ra_jv=False, ra_cashout=False, enr_sell=0.0)
    players = frozenset(R.PLAYERS) if (has_ra and not raoff) else frozenset(R.PLAYERS9)
    return R.Cfg(players=players, trigger="current", book=bk["rb_book"], census=census, theta=theta)


def _job(args):
    engine, book, mk, pk, theta, n, raoff = args
    import ra_engine as R
    t0 = time.time()
    pol = R.E.Policy(pk, **C.POLICY_KW[pk])
    r = R.simulate(R.E.MODELS[mk], pol, cfg_for(engine, book, theta, raoff), n=n, seed=C.SEED)
    out = {k: r[k] for k in KEYS if k in r}
    out["ce"] = R.ce_wealth(r["_w"])
    out["secs"] = time.time() - t0
    if "ra" in r:
        out["ra"] = {k: r["ra"][k] for k in ("cures24", "jv_cash", "oe_redemptions", "forced_sale_cash",
                                             "enr_cash_t0", "oil_delta_t0")}
    return (engine, book, mk, pk, raoff), out


def main():
    th = {b: C.theta_star(b) for b in ("v1pub",) + C.MAIN_BOOKS}
    jobs = []
    for b in ("v1pub",) + C.MAIN_BOOKS:
        for mk in C.MODELS:
            for pk in ("dn", "mixA", "mixB"):
                jobs.append(("t1", b, mk, pk, th[b], N_T1, False))
                jobs.append(("integrated", b, mk, pk, th[b], N_INT, False))
    for b in ("v2u16", "v2u11"):
        for mk in C.MODELS:
            for pk in ("dn", "mixA", "mixB"):
                jobs.append(("integrated", b, mk, pk, th[b], N_INT, True))
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        res = dict(ex.map(_job, sorted(jobs, key=lambda j: -j[5]), chunksize=1))
    secs = time.time() - t0
    out = {"note": C.LABEL, "conventions": __doc__, "theta_star": th, "n_t1": N_T1, "n_integrated": N_INT,
           "secs": secs, "runs": {}}
    for (eng, b, mk, pk, raoff), r in res.items():
        out["runs"][f"{eng}{'_raoff' if raoff else ''}|{b}|{mk}|{pk}"] = r
    # summary tables
    summ = {}
    for eng in ("t1", "integrated", "integrated_raoff"):
        for b in ("v1pub",) + C.MAIN_BOOKS:
            for pk in ("dn", "mixA", "mixB"):
                key = f"{eng}|{b}|{pk}"
                rows = {mk: out["runs"].get(f"{eng}|{b}|{mk}|{pk}") for mk in C.MODELS}
                if any(v is None for v in rows.values()):
                    continue
                summ[key] = dict(p_red_pct={mk: 100 * v["p_red"] for mk, v in rows.items()},
                                 cp_upper_pct={mk: 100 * v["cp_upper_red"] for mk, v in rows.items()},
                                 max_cp_M1_M5_pct=max(100 * rows[mk]["cp_upper_red"] for mk in C.MODELS[:5]),
                                 ce={mk: v["ce"] for mk, v in rows.items()})
    out["summary"] = summ
    C.save("ri_mc_results.json", out)
    print(f"mc: {len(jobs)} runs in {secs:.0f}s; theta* {th}")
    for k, v in summ.items():
        print(f"{k:32s} P(red)% " + " ".join(f"{mk} {v['p_red_pct'][mk]:6.2f}" for mk in C.MODELS)
              + f" | max CP M1-M5 {v['max_cp_M1_M5_pct']:.2f}% | CP M6 {v['cp_upper_pct']['M6']:.2f}%")


if __name__ == "__main__":
    main()
