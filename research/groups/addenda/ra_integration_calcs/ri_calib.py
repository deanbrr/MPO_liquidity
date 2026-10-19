"""
ri_calib: theta* for every book with the canonical rule (gap_02 s1.2; groups gap_01; ra_gap_01 s2).
SYNTHETIC - NOT ADIC DATA.

Rule: theta* sets the deterministic ladder's facility-free 24-month gap G*(s*(theta)) equal to the worst model's
quantile at 1 - eps24 (eps24 = 1 - 0.99^(8/20) = 0.40%) of the action-free G* replica computed on every Monte Carlo
path (rate mode = t1 conventions, gap_02 initial state: drought, Z0 = GW with p 0.7; do-nothing Policy A with the
8% top-up; no RA actions). 50,000 paths per model, seed 20261018; SAA band from five more seeds of the worst model
(pooled over all six seeds). The ladder curve is each book's own (local ra_ladder, theta-indexed RA leg).
Books: v1pub (reproduces 0.76), v1 (census v1.1, new), v2u16 and v2u11 (re-derive ra_gap_01's 0.835 / 0.877).
Also the October-2026 (gap_04) initial state as a sensitivity.
Run: <venv>/python.exe -I -B ri_calib.py  -> ri_calib_results.json
"""
from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ri_common as C  # noqa: E402

N_CAL = 50000
SAA_SEEDS = [C.SEED + 101 * i for i in range(1, 6)]
EPS24 = 1 - (1 - 0.01) ** (8 / 20)
WORKERS = 23


def _job(args):
    book, mk, seed, init = args
    import ra_engine as R
    bk = C.BOOKS[book]
    cfg = R.Cfg(init=init, groups="rate", overlay="t1", links=False, stage="t1",
                census=("gc2" if bk["census"] == "gap02" else "v1"),
                players=frozenset(R.PLAYERS9), trigger="none", book=bk["rb_book"])
    r = R.simulate(R.E.MODELS[mk], R.E.Policy("A"), cfg, n=N_CAL, seed=seed)
    return (book, mk, seed, init), np.asarray(r["_gstar"], dtype=np.float64)


def ladder_curve(book, thetas):
    import ra_ladder as RL
    bk = C.BOOKS[book]
    g = []
    for th in thetas:
        lev = RL.lev_of(reserve=0.08, book=bk["rb_book"], census=bk["census"])
        g.append(RL.gl_ladder(RL.s_star(th), lev, theta=th)["gstar"])
    return np.array(g)


def main():
    books = ("v1pub",) + C.MAIN_BOOKS
    jobs = [(b, mk, C.SEED, "gap02") for b in books for mk in C.MODELS]
    jobs += [(b, "M6", s, "gap02") for b in books for s in SAA_SEEDS]
    jobs += [(b, mk, C.SEED, "gap04") for b in C.MAIN_BOOKS for mk in C.MODELS]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        res = dict(ex.map(_job, jobs, chunksize=1))
    secs = time.time() - t0
    thetas = np.round(np.arange(0.0, 1.2001, 0.01), 4)
    curves = {b: ladder_curve(b, thetas) for b in books}
    out = {"note": C.LABEL, "rule": "worst-model P(1-eps24) of the action-free 24-month G*, eps24 = 0.40%",
           "n_paths": N_CAL, "seed": C.SEED, "eps24": EPS24, "secs": secs, "thetas": thetas.tolist(),
           "ladder_gstar_curve": {b: v.tolist() for b, v in curves.items()}, "theta_star": {}, "saa": {},
           "gap04_init": {}, "quantiles": {}}
    for b in books:
        p = {mk: float(np.quantile(res[(b, mk, C.SEED, "gap02")], 1 - EPS24)) for mk in C.MODELS}
        worst = max(p, key=p.get)
        th = float(np.interp(p[worst], curves[b], thetas))
        mix = float(np.quantile(np.concatenate([res[(b, mk, C.SEED, "gap02")] for mk in C.MODELS]), 1 - EPS24))
        reps = [p["M6"]] + [float(np.quantile(res[(b, "M6", s, "gap02")], 1 - EPS24)) for s in SAA_SEEDS]
        pooled = float(np.quantile(np.concatenate([res[(b, "M6", C.SEED, "gap02")]]
                                                  + [res[(b, "M6", s, "gap02")] for s in SAA_SEEDS]), 1 - EPS24))
        out["theta_star"][b] = dict(worst_model=worst, gstar_p996=p[worst], theta=th, by_model=p,
                                    mixture_p996=mix, theta_mixture=float(np.interp(mix, curves[b], thetas)),
                                    ladder_gstar_at_076=float(np.interp(0.76, thetas, curves[b])))
        out["saa"][b] = dict(gstar=reps, theta=[float(np.interp(x, curves[b], thetas)) for x in reps],
                             pooled_gstar=pooled, pooled_theta=float(np.interp(pooled, curves[b], thetas)))
        for mk in C.MODELS:
            g = res[(b, mk, C.SEED, "gap02")]
            out["quantiles"][f"{b}|{mk}"] = [float(x) for x in np.quantile(g, [0.5, 0.9, 0.95, 0.99, 1 - EPS24,
                                                                                0.999])]
    for b in C.MAIN_BOOKS:
        p4 = {mk: float(np.quantile(res[(b, mk, C.SEED, "gap04")], 1 - EPS24)) for mk in C.MODELS}
        w4 = max(p4, key=p4.get)
        out["gap04_init"][b] = dict(worst_model=w4, gstar_p996=p4[w4],
                                    theta=float(np.interp(p4[w4], curves[b], thetas)), by_model=p4)
    C.save("ri_calib_results.json", out)
    print(f"calibration: {len(jobs)} runs x {N_CAL} paths in {secs:.0f}s")
    for b in books:
        t = out["theta_star"][b]
        s = out["saa"][b]
        print(f"{b:6s} worst {t['worst_model']} G*P99.6 {t['gstar_p996']:.2f} theta* {t['theta']:.4f} "
              f"(SAA {min(s['theta']):.3f}-{max(s['theta']):.3f}, pooled {s['pooled_theta']:.3f}); "
              f"mixture theta {t['theta_mixture']:.3f}; ladder G*(0.76) {t['ladder_gstar_at_076']:.2f}")
    for b in C.MAIN_BOOKS:
        print(b, "gap04 init theta", round(out["gap04_init"][b]["theta"], 4))


if __name__ == "__main__":
    main()
