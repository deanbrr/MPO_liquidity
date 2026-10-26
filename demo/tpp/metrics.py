"""Stakeholder metrics from a simulation (probability-weighted over paths and ER worlds).

Probabilities: each scenario carries pi_w / n, so every statistic is weighted; intervals use the effective sample
size 1 / sum(p^2) (Wilson interval for P(goal)). Tail statistics are exact weighted CVaRs (examples/mpo_v2
common.cvar_lower). One summary feeds every lens:
  Strategy        P(goal) with interval and by world, TWR distribution, CVaR, on-track probability by year
  Balance Sheet   NAV, debt, leverage, overcommitment and reserve fans by year
  Liquidity       owner draws, calls, distributions, net private flow, liquid sales, revolver use, forced sales,
                  coverage ratio, minimum reserve ratio
  Asset Allocation the same, plus the plan's change list (tpp.substitution)
Each group's objective is also a pass/fail test on every path (objective_flags), so every case reports the
probability that the 10% target and each group's objective are met, alone and together.
"""
from __future__ import annotations

import numpy as np

from .legacy import cvar_lower, quantile_w, wilson

QS = [0.05, 0.25, 0.5, 0.75, 0.95]


def _wq(x, p, qs=QS):
    return [float(quantile_w(x, q, p)) for q in qs]


def _fan(X, p):
    """(m, T) -> {q: [T values]} weighted quantiles per column."""
    return {f"p{int(q * 100)}": [float(quantile_w(X[:, t], q, p)) for t in range(X.shape[1])] for q in QS} | {
        "mean": [float(np.dot(p, X[:, t])) for t in range(X.shape[1])]}


REP_Q = ((0.10, "worst 10%"), (0.50, "median"), (0.90, "best 10%"))


def rep_paths(out: dict) -> list[dict]:
    """Representative paths for the year-by-year view: in each ER world, the paths at the 10th, 50th and 90th
    percentile of the five-year return, with what happened each year."""
    twr, world, ret = np.asarray(out["twr"]), np.asarray(out["world"]), np.asarray(out["ret"])
    res = []
    for w in range(3):
        idx = np.flatnonzero(world == w)
        if not len(idx):
            continue
        order = idx[np.argsort(twr[idx], kind="stable")]
        for q, label in REP_Q:
            i = int(order[int(round(q * (len(order) - 1)))])
            cum = np.cumprod(1 + ret[i])
            res.append({"world": w, "q": label, "twr": float(twr[i]), "ret": ret[i].tolist(),
                        "cum": [1.0] + cum.tolist(), "ann": (cum ** (1 / np.arange(1, 6)) - 1).tolist(),
                        **{k: np.asarray(out[f"r_{k}"][i]).tolist() for k in ("nav", "reserve", "debt", "lev", "ovc")},
                        **{k: np.asarray(out[f"y_{k}"][i]).tolist() for k in ("draw", "calls", "dist", "sales", "lr_sold",
                                                                             "rev_draw", "forced")},
                        "lcr": np.asarray(out["lcr"][i]).tolist(),
                        "macro": np.asarray(out["macro_y"][i]).astype(int).tolist() if "macro_y" in out else None,
                        "exit": np.asarray(out["exit_y"][i]).astype(int).tolist() if "exit_y" in out else None,
                        "cls": np.asarray(out["cls_y"][i]).astype(int).tolist() if "cls_y" in out else None})
    return res


def summarize(out: dict, goal: float) -> dict:
    p = np.asarray(out["prob"], float)
    p = p / p.sum()
    neff = 1.0 / float(np.sum(p ** 2))
    g = out["goal"].astype(float)
    pg = float(p @ g)
    lo, hi = wilson(pg * neff, int(round(neff)))
    twr = out["twr"]
    by_world = {}
    for w, name in enumerate(["Downside", "Base", "Upside"]):
        mk = out["world"] == w
        if mk.any():
            pw = p[mk] / p[mk].sum()
            by_world[name] = {"p_goal": float(pw @ g[mk]), "twr_mean": float(pw @ twr[mk]),
                              "twr_p50": float(quantile_w(twr[mk], 0.5, pw))}
    # on track: annualized TWR to year t >= goal
    lr = np.log1p(out["ret"])
    ontrack = [float(p @ ((np.exp(lr[:, :t].mean(1)) - 1) >= goal - 1e-12)) for t in range(1, 6)]
    hist_edges = np.linspace(-0.10, 0.25, 36)
    hist = np.histogram(np.clip(twr, hist_edges[0], hist_edges[-1] - 1e-9), bins=hist_edges, weights=p)[0]
    nav = out["r_nav"]
    lcr = out["lcr"]
    res = {
        "plan": out["plan"],
        "n_scenarios": int(out["m"]), "n_eff": neff,
        "p_goal": pg, "p_goal_ci": [float(lo), float(hi)], "by_world": by_world, "on_track": ontrack,
        "twr_mean": float(p @ twr), "twr_q": _wq(twr, p),
        "cvar10": float(cvar_lower(twr, 0.10, p)), "cvar5": float(cvar_lower(twr, 0.05, p)),
        "cvar1": float(cvar_lower(twr, 0.01, p)),
        "wealth_mean_bn": float(p @ out["wealth"]), "W0_bn": float(out["W0"]),
        # the fund the owner sees: its size after the owner's distributions, and what the owner received
        "p_preserve": float(p @ (nav[:, 5] >= nav[:, 0] - 1e-9)), "nav5_p50_bn": float(quantile_w(nav[:, 5], 0.5, p)),
        "owner5_p50_bn": float(quantile_w(out["y_draw"].sum(1), 0.5, p)),
        "owner_cum_fan": _fan(np.c_[np.zeros(len(twr)), np.cumsum(out["y_draw"], axis=1)], p),
        "goal_wealth_bn": float(out["W0"] * (1 + goal) ** 5),
        "shortfall_mean_bn": float(p @ np.maximum(out["W0"] * (1 + goal) ** 5 - out["wealth"], 0.0)),
        "hist": {"edges": hist_edges.tolist(), "p": hist.tolist()},
        "p_red": float(p @ out["red"].astype(float)), "forced_mean_bn": float(p @ out["forced_total"]),
        "forced_p95_bn": float(quantile_w(out["forced_total"], 0.95, p)),
        "forced_p99_bn": float(quantile_w(out["forced_total"], 0.99, p)),
        "p_revolver": float(p @ out["rev_used"].astype(float)), "rev_max_p95_bn": float(quantile_w(out["rev_max"], 0.95, p)),
        "min_reserve_ratio_p5": float(quantile_w(out["min_reserve_ratio"], 0.05, p)),
        "lcr_min_p5": float(quantile_w(lcr.min(1), 0.05, p)), "lcr_min_p50": float(quantile_w(lcr.min(1), 0.5, p)),
        "fans": {k: _fan(out[f"r_{k}"], p) for k in ("nav", "reserve", "lr", "priv", "unf", "debt", "lev", "ovc", "rev")},
        "flows": {k: _fan(out[f"y_{k}"], p) for k in ("draw", "dist", "calls", "interest", "forced", "lr_sold",
                                                      "rev_draw", "sales", "vm", "deploy")},
        "lcr_fan": _fan(lcr, p),
        "net_private_fan": _fan(out["y_dist"] - out["y_calls"], p),
        "leverage_t0": float(np.mean(out["r_lev"][:, 0])), "debt_t0_bn": float(np.mean(out["r_debt"][:, 0])),
        "ovc_t0": float(np.mean(out["r_ovc"][:, 0])),
        # the five years: growth of $1 at the TWR (owner draws out of the return), annualized return to date
        "cum_fan": _fan(np.c_[np.ones(len(twr)), np.cumprod(1 + out["ret"], axis=1)], p),
        "ann_fan": _fan(np.exp(np.cumsum(lr, axis=1) / np.arange(1, 6)) - 1, p),
        "rep_paths": rep_paths(out),
    }
    return res


# bits of the per-path objective byte (the Strategy group's objective, TWR >= hurdle, is tested from the TWR itself)
OBJ_BS, OBJ_LIQ, OBJ_AA = 1, 2, 4


def objective_flags(o: dict, o_ref: dict | None, lev_cap: float, overcommit: float, goal: float) -> np.ndarray:
    """Per path, whether each group's objective is met (one byte, bits OBJ_*), always against the house limits:
      Balance Sheet     gross leverage within lev_cap and overcommitment ((private NAV + unfunded) / NAV) within
                        overcommit at every year-end
      Liquidity         every capital call and owner distribution paid without a forced private sale
      Asset Allocation  the substitutions never cost the target: wherever the status quo reaches the hurdle on a
                        path, the plan does too; set for the status quo itself (o_ref None), where it does not apply.
                        The page recomputes this bit from the two TWR arrays so it follows the hurdle control."""
    bs = (np.asarray(o["r_lev"]).max(1) <= lev_cap + 1e-6) & (np.asarray(o["r_ovc"]).max(1) <= overcommit + 1e-6)
    liq = ~np.asarray(o["red"], bool)
    hit = np.asarray(o["twr"]) >= goal - 1e-12
    aa = (hit | (np.asarray(o_ref["twr"]) < goal - 1e-12)) if o_ref is not None else np.ones(len(bs), bool)
    return (bs.astype(np.uint8) * OBJ_BS) | (liq.astype(np.uint8) * OBJ_LIQ) | (aa.astype(np.uint8) * OBJ_AA)


def objective_rates(o: dict, flags: np.ndarray, goal: float) -> dict:
    """Probability-weighted rates of each objective, and of all of them with the hurdle (p_all)."""
    p = np.asarray(o["prob"], float)
    p = p / p.sum()
    g = np.asarray(o["twr"]) >= goal - 1e-12
    bs, liq, aa = (flags & OBJ_BS) > 0, (flags & OBJ_LIQ) > 0, (flags & OBJ_AA) > 0
    return {"p_goal": float(p @ g), "p_bs": float(p @ bs), "p_liq": float(p @ liq), "p_aa": float(p @ aa),
            "p_all": float(p @ (g & bs & liq & aa))}


def paired_delta(a: dict, b: dict) -> dict:
    """Paired difference (plan a minus plan b) on common paths: P(goal), mean TWR, with a normal interval."""
    p = np.asarray(a["prob"], float)
    p = p / p.sum()
    neff = 1.0 / float(np.sum(p ** 2))
    dg = a["goal"].astype(float) - b["goal"].astype(float)
    dt = a["twr"] - b["twr"]
    mg, mt = float(p @ dg), float(p @ dt)
    sg = float(np.sqrt(max(p @ (dg - mg) ** 2, 0.0) / neff))
    st = float(np.sqrt(max(p @ (dt - mt) ** 2, 0.0) / neff))
    return {"d_p_goal": mg, "d_p_goal_ci": [mg - 1.96 * sg, mg + 1.96 * sg], "d_twr": mt,
            "d_twr_ci": [mt - 1.96 * st, mt + 1.96 * st]}
