"""
G4 barrier re-run, step B: independent fine-grid check of the section 7 book simulation.
SYNTHETIC - NOT ADIC DATA.

Same model, parameters and event order as section 7 of G4_coinvest_calcs.py (BOOK, P_REG and SEED
are imported from the verbatim copy orig/G4_coinvest_calcs.py), except that enterprise value is
stepped K = 78 times per quarter (312 a year).  Quarter-end distributions are unchanged:
  * the quarterly Gaussian increments are split into K independent sub-step increments
    (market and idiosyncratic), so their quarterly sums have the original distribution;
  * the quarterly Kou jump is drawn exactly as in section 7 (at most one per position-quarter,
    applied when Poisson(lam_J*dt) > 0) and placed at a uniformly drawn sub-step;
  * debt amortises by (1 - amort*dt)**(1/K) per sub-step, so quarter-end debt is identical.
Recaps, follow-ons, exits, marks and deployment stay quarterly, exactly as in section 7.

The default barrier V <= kappa*D (kappa = 0.75) is checked under several monitoring rules.  All
rules run side by side on the SAME random numbers (common random numbers), so differences between
rules are pure monitoring effects:
  Q                 quarter ends only, barrier kappa*D               (= original section 7 rule)
  Q_bgk             quarter ends only, kappa*D*exp(+beta*sigma_V*sqrt(1/4))   (= corrected rule)
  Q_bgk_wrong_sign  quarter ends only, kappa*D*exp(-beta*sigma_V*sqrt(1/4))   (= dossier's printed formula)
  M                 month ends (every 26 sub-steps), kappa*D
  M_bgk             month ends, kappa*D*exp(+beta*sigma_V*sqrt(1/12))
  W                 week ends (every 6 sub-steps), kappa*D
  F                 every sub-step (312 a year), kappa*D
sigma_V = sqrt((beta_A*sig_m[regime])^2 + sig_id^2), the diffusive EV volatility; beta = 0.5826.
The continuous-monitoring limit is extrapolated from M, W and F using the sqrt(Delta) error law
(BGK 1997: the discrete-monitoring error is first order in sqrt(Delta)).

Paths run in batches of 2,000 with seeds different from the published run (independent draws).
Run:  <venv>/python.exe -I fine_grid_book.py [n_batches]   (writes fine_grid_book_results.json here)
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fine_grid_book_results.json")


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G4 = _load("g4_orig", os.path.join(HERE, "orig", "G4_coinvest_calcs.py"))
BOOK, P_REG, REG, SEED = G4.BOOK, G4.P_REG, G4.REG, G4.SEED
BETA = 0.5825971579390106          # -zeta(1/2)/sqrt(2*pi)
K = 78                             # sub-steps per quarter
VARIANTS = {                       # name: (check every m sub-steps, sign of the BGK exponent)
    "Q": (78, 0), "Q_bgk": (78, +1), "Q_bgk_wrong_sign": (78, -1),
    "M": (26, 0), "M_bgk": (26, +1), "W": (6, 0), "F": (1, 0),
}
DT = 0.25


def run_batch(start_regime: int, n_paths: int, quarters: int, seed: int) -> dict:
    b = BOOK
    rng = np.random.default_rng(seed)
    S = b["slots"]
    dts = DT / K
    amort_s = (1 - b["amort"] * DT) ** (1.0 / K)
    H = lambda t: (np.maximum(t, 0) / b["eta"]) ** b["k"]  # noqa: E731

    # ---- initial book, identical construction to section 7 (common to all variants)
    act0 = np.zeros((n_paths, S), bool)
    ev0 = np.zeros((n_paths, S)); debt0 = np.zeros((n_paths, S)); cost0 = np.zeros((n_paths, S))
    age0 = np.zeros((n_paths, S)); mark0 = np.zeros((n_paths, S))
    n0 = b["n_init"]
    act0[:, :n0] = True
    age0[:, :n0] = rng.uniform(0, 7, (n_paths, n0))
    cost0[:, :n0] = b["ticket"]
    growth = np.exp(rng.normal(0.05 * age0[:, :n0], 0.25 * np.sqrt(np.maximum(age0[:, :n0], 0.25))))
    eq0 = cost0[:, :n0] * growth
    eq0 *= 18.0 / eq0.sum(axis=1, keepdims=True)
    debt0[:, :n0] = cost0[:, :n0] * b["L_entry"] / (1 - b["L_entry"]) * (1 - b["amort"] * age0[:, :n0])
    ev0[:, :n0] = eq0 + debt0[:, :n0]
    mark0[:, :n0] = eq0
    nav0 = (np.maximum(ev0 - debt0, 0) * act0).sum(axis=1)

    st = {}
    for v in VARIANTS:
        st[v] = dict(act=act0.copy(), ev=ev0.copy(), debt=debt0.copy(), cost=cost0.copy(), age=age0.copy(),
                     mark=mark0.copy(), mark_prev=mark0.copy(), eq_lag=mark0.copy(),
                     pos_q=np.zeros(n_paths), n_wo=np.zeros(n_paths), wo_cost=np.zeros(n_paths),
                     dist_recap=np.zeros(n_paths), calls_fo=np.zeros(n_paths), dist_exit=np.zeros(n_paths),
                     n_exit=np.zeros(n_paths), zero_exits=np.zeros(n_paths), calls_new=np.zeros(n_paths),
                     yearly=np.zeros((n_paths, quarters // 4)), above=[], above_w=[])
    reg = np.full(n_paths, start_regime)
    regime_path = np.zeros((n_paths, quarters), int)

    for q in range(quarters):
        # 1. regime transition (common)
        u = rng.random(n_paths)
        cp = np.cumsum(P_REG[reg], axis=1)
        reg = (u[:, None] > cp).sum(axis=1)
        regime_path[:, q] = reg
        mu_m, sg_m = b["mu_m"][reg], b["sig_m"][reg]
        sig_v = np.sqrt((b["beta_A"] * sg_m) ** 2 + b["sig_id"] ** 2)
        # quarterly jump, as in section 7, placed at a uniform sub-step
        nj = rng.poisson(b["lam_J"] * DT, (n_paths, S))
        up = rng.random((n_paths, S)) < b["p_up"]
        jsize = np.where(up, rng.exponential(b["eta_up"], (n_paths, S)),
                         -rng.exponential(b["eta_dn"], (n_paths, S))) * (nj > 0)
        jstep = rng.integers(0, K, (n_paths, S))
        factors = {}
        for v, (m, sgn) in VARIANTS.items():
            factors[v] = (b["default_kappa"] * np.exp(sgn * BETA * sig_v * math.sqrt(m * dts)))[:, None]
        for v in VARIANTS:
            st[v]["pos_q"] += st[v]["act"].sum(axis=1)
        drift_m = (mu_m - 0.5 * sg_m ** 2) * dts
        vol_m = sg_m * math.sqrt(dts)
        c_id = (b["alpha_A"] - 0.5 * b["sig_id"] ** 2) * dts
        v_id = b["sig_id"] * math.sqrt(dts)
        # 2-3. EV on the fine grid, barrier checked per variant
        for k in range(K):
            r_m = drift_m + vol_m * rng.standard_normal(n_paths)
            r_ev = c_id + b["beta_A"] * r_m[:, None] + v_id * rng.standard_normal((n_paths, S))
            r_ev += np.where(jstep == k, jsize, 0.0)
            g = np.exp(r_ev)
            for v, (m, sgn) in VARIANTS.items():
                s = st[v]
                np.multiply(s["ev"], g, out=s["ev"], where=s["act"])
                np.multiply(s["debt"], amort_s, out=s["debt"], where=s["act"])
                if (k + 1) % m == 0:
                    wo = s["act"] & (s["ev"] <= factors[v] * s["debt"])
                    if wo.any():
                        s["wo_cost"] += (s["cost"] * wo).sum(axis=1)
                        s["n_wo"] += wo.sum(axis=1)
                        s["act"] &= ~wo
        # 4-8. quarterly events with common random numbers
        u_rc = rng.random((n_paths, S))
        u_fo = rng.random((n_paths, S))
        u_ex = rng.random((n_paths, S))
        upl = np.maximum(rng.normal(b["uplift_mu"], b["uplift_sd"], (n_paths, S)), -0.5)
        n_new = np.floor(b["deploy_q"][reg] / b["ticket"]).astype(int)
        tk = b["ticket"]
        for v in VARIANTS:
            s = st[v]
            act, ev, debt, cost, age = s["act"], s["ev"], s["debt"], s["cost"], s["age"]
            elig = act & (age >= 2.0) & (debt / np.maximum(ev, 1e-12) < b["recap_elig_L"])
            rc = elig & (u_rc < b["recap_p"][reg][:, None] * DT)
            d_up = b["recap_debt_up"] * debt * rc
            debt = debt + d_up
            dist_rc = (0.98 * d_up).sum(axis=1)
            s["dist_recap"] += dist_rc
            eq = np.maximum(ev - debt, 0.0)
            fo = act & (u_fo < b["fo_p"] * DT)
            call_fo = b["fo_size"] * eq * fo
            ev = ev + call_fo
            cost = cost + call_fo
            s["calls_fo"] += call_fo.sum(axis=1)
            eq = np.maximum(ev - debt, 0.0)
            perf = np.log(np.maximum(eq, 1e-9) / np.maximum(cost, 1e-9))
            haz = b["exit_mult"][reg][:, None] * (H(age + DT) - H(age)) * np.exp(b["gamma"] * np.clip(perf, -3, 3))
            ex = act & (u_ex < 1 - np.exp(-haz))
            proceeds = eq * (1 + upl) * ex
            if ex.any():
                live = ex & (proceeds > 0) & (s["mark_prev"] > 0)
                s["above"].append(((proceeds > s["mark_prev"]) & live).sum() / max(live.sum(), 1))
                s["zero_exits"] += (ex & (proceeds <= 0)).sum(axis=1)
            s["dist_exit"] += proceeds.sum(axis=1)
            s["n_exit"] += ex.sum(axis=1)
            s["yearly"][:, q // 4] += proceeds.sum(axis=1) + dist_rc
            act = act & ~ex
            mark_prev = np.where(act, s["mark"], 0.0)
            mark = np.where(act, b["lam_mark"] * s["mark"] + (1 - b["lam_mark"]) * s["eq_lag"], 0.0)
            eq_lag = np.where(act, eq, 0.0)
            free = ~act
            rank = np.cumsum(free, axis=1)
            newm = free & (rank <= n_new[:, None])
            ev = np.where(newm, tk / (1 - b["L_entry"]), ev)
            debt = np.where(newm, tk / (1 - b["L_entry"]) * b["L_entry"], debt)
            cost = np.where(newm, tk, np.where(act, cost, 0.0))
            age = np.where(newm, 0.0, age)
            mark = np.where(newm, tk, mark)
            mark_prev = np.where(newm, tk, mark_prev)
            eq_lag = np.where(newm, tk, eq_lag)
            s["calls_new"] += (newm * tk).sum(axis=1)
            act = act | newm
            age = np.where(act, age + DT, age)
            s.update(act=act, ev=ev, debt=debt, cost=cost, age=age, mark=mark, mark_prev=mark_prev, eq_lag=eq_lag)

    out = {}
    stayed_d = (regime_path == 2).all(axis=1)
    for v, s in st.items():
        eq_end = (np.maximum(s["ev"] - s["debt"], 0) * s["act"]).sum(axis=1)
        mark_end = (s["mark"] * s["act"]).sum(axis=1)
        out[v] = dict(nav0=nav0, dist=s["dist_exit"] + s["dist_recap"], dist_exit=s["dist_exit"],
                      dist_recap=s["dist_recap"], calls=s["calls_new"] + s["calls_fo"], calls_new=s["calls_new"],
                      n_wo=s["n_wo"], wo_cost=s["wo_cost"], pos_q=s["pos_q"], n_exit=s["n_exit"],
                      zero_exits=s["zero_exits"], yearly=s["yearly"], eq_end=eq_end, mark_end=mark_end,
                      stayed_d=stayed_d, above=np.array(s["above"]))
    return out


def pct(x):
    return dict(mean=float(np.mean(x)), p10=float(np.quantile(x, 0.10)),
                p50=float(np.median(x)), p90=float(np.quantile(x, 0.90)))


def ratio_se(num, den):
    """SE of sum(num)/sum(den) over i.i.d. paths (delta method)."""
    r = num.sum() / den.sum()
    n = len(num)
    return float(math.sqrt(np.var(num - r * den, ddof=1) / n) / den.mean())


def summarise(batches: list[dict], quarters: int) -> dict:
    cat = {v: {k: (np.concatenate([bt[v][k] for bt in batches]) if k != "yearly"
                   else np.vstack([bt[v][k] for bt in batches]))
               for k in batches[0][v]} for v in VARIANTS}
    res = {}
    for v, c in cat.items():
        net = c["dist"] - c["calls"]
        wo_rate_path = c["n_wo"]
        rate = float(wo_rate_path.sum() / (c["pos_q"].sum() * DT))
        res[v] = dict(
            dist_3y=pct(c["dist"]), calls_3y=pct(c["calls"]), net_cf_3y=pct(net),
            nav_end_economic=pct(c["eq_end"]), nav_end_reported=pct(c["mark_end"]),
            annual_dist_yield_on_nav0={f"Y{y + 1}": pct(c["yearly"][:, y] / c["nav0"]) for y in range(quarters // 4)},
            exits_3y=pct(c["n_exit"]), writeoffs_3y=pct(c["n_wo"]),
            writeoff_cost_share=float(c["wo_cost"].sum() / (c["calls_new"] + 18.0).sum()),
            annual_writeoff_rate_per_position=rate,
            annual_writeoff_rate_se=ratio_se(c["n_wo"], c["pos_q"] * DT),
            share_of_exits_at_zero=float(c["zero_exits"].sum() / max(c["n_exit"].sum(), 1)),
            annual_exit_rate_per_position=float(c["n_exit"].sum() / (c["pos_q"].sum() * DT)),
            recap_dist_over_exit_proceeds=float(c["dist_recap"].sum() / c["dist_exit"].sum()),
            p_exit_above_next_to_last_mark=float(np.mean(c["above"])),
            net_cf_3y_if_drought_throughout=pct(net[c["stayed_d"]]) if c["stayed_d"].any() else None,
            share_paths_drought_throughout=float(c["stayed_d"].mean()),
            reported_vs_economic_nav_gap=pct(c["mark_end"] / np.maximum(c["eq_end"], 1e-9) - 1),
        )
    # paired (common-random-number) differences in the write-off rate against the finest grid
    pq = cat["F"]["pos_q"] * DT
    res["paired_vs_F"] = {}
    for v in VARIANTS:
        d = cat[v]["n_wo"] / pq.mean() - cat["F"]["n_wo"] / pq.mean()   # pos_q is close across variants
        rate_v = cat[v]["n_wo"].sum() / (cat[v]["pos_q"].sum() * DT)
        rate_f = cat["F"]["n_wo"].sum() / (cat["F"]["pos_q"].sum() * DT)
        res["paired_vs_F"][v] = dict(diff=float(rate_v - rate_f), se_approx=float(np.std(d, ddof=1) / math.sqrt(len(d))))
    # continuous-monitoring limit from the sqrt(Delta) law
    sq = {"M": math.sqrt(1 / 12), "W": math.sqrt(1 / 52), "F": math.sqrt(1 / 312)}
    xs = np.array([sq[v] for v in ("M", "W", "F")])
    for metric in ("annual_writeoff_rate_per_position", "writeoff_cost_share"):
        ys = np.array([res[v][metric] for v in ("M", "W", "F")])
        slope, icpt = np.polyfit(xs, ys, 1)
        two_pt = ys[2] + (ys[2] - ys[1]) * xs[2] / (xs[1] - xs[2])
        res.setdefault("continuous_limit", {})[metric] = dict(lsq_MWF=float(icpt), two_point_WF=float(two_pt),
                                                             slope_per_sqrt_year=float(slope))
    ys = np.array([res[v]["writeoffs_3y"]["mean"] for v in ("M", "W", "F")])
    res["continuous_limit"]["writeoffs_3y_mean"] = dict(lsq_MWF=float(np.polyfit(xs, ys, 1)[1]))
    return res


def main():
    n_batches = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    n_paths, quarters = 2000, 12
    results = {"label": "SYNTHETIC - NOT ADIC DATA", "K_substeps_per_quarter": K, "n_paths_per_batch": n_paths,
               "n_batches": n_batches, "beta": BETA, "variants": {k: dict(check_every_substeps=m, bgk_sign=s)
                                                                  for k, (m, s) in VARIANTS.items()}}
    for start, seed_base in ((2, SEED + 1000), (1, SEED + 2000)):
        t0 = time.time()
        batches = [run_batch(start, n_paths, quarters, seed_base + i) for i in range(n_batches)]
        key = "start_drought" if start == 2 else "start_normal"
        results[key] = summarise(batches, quarters)
        r = results[key]
        print(f"--- {key}  ({time.time() - t0:.0f}s, {n_batches * n_paths} paths)")
        for v in VARIANTS:
            print(f"{v:18s} wo-rate {r[v]['annual_writeoff_rate_per_position']:.4f} (se {r[v]['annual_writeoff_rate_se']:.4f})"
                  f"  diff vs F {r['paired_vs_F'][v]['diff']:+.4f} (se {r['paired_vs_F'][v]['se_approx']:.4f})"
                  f"  wo/3y {r[v]['writeoffs_3y']['mean']:.3f}  cost share {r[v]['writeoff_cost_share']:.4f}"
                  f"  dist {r[v]['dist_3y']['mean']:.3f}  net {r[v]['net_cf_3y']['mean']:.3f}"
                  f"  Y1 {r[v]['annual_dist_yield_on_nav0']['Y1']['mean']:.4f}")
        print("continuous limit:", json.dumps(r["continuous_limit"]))
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
