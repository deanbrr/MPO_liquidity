"""Independent finance-review checks on examples/mpo_v2 (SYNTHETIC - NOT ADIC DATA).

Rebuilds the headline world exactly as world.base does, reconstructs O1's root decision from results.json, and runs
decomposition variants through the prototype's own simulator (sim.Sim / run_policy) on the certification seed.
Nothing is written into the project folder (bytecode disabled, outputs to the scratchpad).
Usage: pythonw fin_sim.py <out.txt> <out.json> [n_paths]
"""
import sys
import os
import json
import time
import copy

sys.dont_write_bytecode = True
OUT = open(sys.argv[1], "w", encoding="utf-8")
sys.stdout = OUT
sys.stderr = OUT
OUTJ = sys.argv[2]
NP = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
HERE = r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2"
os.chdir(os.path.dirname(os.path.abspath(sys.argv[1])))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from scipy.stats import skew, kurtosis  # noqa: E402

from common import Params, cvar_lower, sarle_bimodality  # noqa: E402
import world  # noqa: E402
from prep import prepare  # noqa: E402
from sim import Sim, run_policy  # noqa: E402
from book import make_book  # noqa: E402

t0 = time.time()
P = Params(os.path.join(HERE, "params.json"))
R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
w = world.base(P)
D = prepare(P, w["units"], w["beliefs"], w["book"], w["gen"], w["tr"], use_beliefs=True)
print(f"world built in {time.time() - t0:.1f}s; W0 {D['W0']:.3f}, W* {D['Wstar']:.3f}", flush=True)
ids = D["ids"]
I = D["I"]
K = len(D["tpl"])
tnames = D["tpl_names"]
hf_units = list(np.flatnonzero(D["is_hf"]))
plan = np.array([t.get("plan", 0.0) for t in D["tpl"]])
is_commit = D["tpl_is_commit"]

# ---------------------------------------------------------------- replication-book opportunistic Sharpe draws
sr = {}
for nm, sd, var in [("HEADLINE", P.get("seeds.book"), {"alpha_dispersion": 1.0, "bid_info": 1.0, "placebo": False}),
                    ("BOOK_7101", 7101, {"alpha_dispersion": 0.5, "bid_info": 1.0, "placebo": False}),
                    ("BOOK_7102", 7102, {"alpha_dispersion": 1.5, "bid_info": 1.0, "placebo": False}),
                    ("BOOK_7103", 7103, {"alpha_dispersion": 0.5, "bid_info": 0.5, "placebo": False}),
                    ("BOOK_7104", 7104, {"alpha_dispersion": 1.5, "bid_info": 0.5, "placebo": False}),
                    ("BOOK_PLACEBO", P.get("seeds.book"), {"alpha_dispersion": 1.0, "bid_info": 1.0, "placebo": True})]:
    b = make_book(P, w["units"], sd, var)
    sr[nm] = b["truth"]["opp_sharpe_true"]
print("opportunistic Sharpe truth draws:", json.dumps(sr), flush=True)

# ---------------------------------------------------------------- O1 root decision reconstructed from results.json
cards = {c["unit_id"]: c for c in R["cards"]}
root = R["root"]
sell = np.array([cards[u]["sell_frac"] for u in ids])
redeem = np.array([cards[u]["redeem_frac"] for u in ids])
add = np.array([cards[u]["add_frac"] for u in ids])
tpl = np.array([root["templates_bn"].get(nm, 0.0) for nm in tnames])
trs = np.zeros(len(hf_units))
for row in R["change_list"]:
    if row["unit_id"].startswith("TRS:"):
        trs[hf_units.index(ids.index(row["unit_id"][4:]))] = row["size_bn"]
fin = np.zeros(7)
FIN = ["REV", "TERM", "NAVF", "PREF", "CSBL", "SMABL", "RACO"]
for k, v in root["debt_bn"].items():
    fin[FIN.index(k)] = v
O1root = {"sell": sell, "redeem": redeem, "add": add, "tpl": tpl, "p2s": float(root["p2s_bn"]),
          "beta": float(root["synthetic_beta_bn"]), "trs": trs, "hed": float(root["tail_notional_bn"]),
          "opp": float(root["opp_im_bn"]), "fin": fin, "Lup": 0.0}
hmin = P.get("overlay.tail_budget")[0] / P.get("overlay.tail_premium")
B0root = {"sell": np.zeros(I), "redeem": np.zeros(I), "add": np.zeros(I), "tpl": np.where(is_commit, plan, 0.0),
          "p2s": 0.0, "beta": P.get("overlay.beta_sq"), "trs": np.zeros(len(hf_units)), "hed": hmin * D["W0"],
          "opp": P.get("overlay.opp_im_sq"), "fin": np.zeros(7), "Lup": 0.0}
print("O1 root reconstructed: beta", O1root["beta"], "opp", O1root["opp"], "hed", O1root["hed"], "trs", trs.tolist(),
      "fin", fin.tolist(), flush=True)
print("templates", dict(zip(tnames, tpl.round(4).tolist())), flush=True)


def plan_pol(r):
    return {"kind": "plan", "root": r, "nodes": {}, "stage1": [], "children": {}, "feat_mu": D["tr"]["feat_mu"],
            "feat_sd": D["tr"]["feat_sd"], "restore8": True, "playbook_years": (1,), "playbook": False}


def mod(r, **kw):
    r2 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in r.items()}
    for k, v in kw.items():
        r2[k] = v
    return r2


hf_mask = D["is_hf"]
re_mask = D["is_re_open"]
pace_O1 = np.where(is_commit, O1root["tpl"], 0.0)
purch_O1 = np.where(is_commit, 0.0, O1root["tpl"])
pols = {
    "B0": {"kind": "B0", "restore8": False},
    "B4_1.0": {"kind": "B4", "restore8": False, "scale": 1.0},
    "B4_1.1": {"kind": "B4", "restore8": False, "scale": 1.1},
    "B4_1.2": {"kind": "B4", "restore8": False, "scale": 1.2},
    "B4_1.3": {"kind": "B4", "restore8": False, "scale": 1.3},
    "O1_rule": plan_pol(O1root),
    "O1_opp1.0": plan_pol(mod(O1root, opp=1.0)),
    "O1_pace_plan": plan_pol(mod(O1root, tpl=np.where(is_commit, plan, O1root["tpl"]))),
    "O1_opp1.0_pace_plan": plan_pol(mod(O1root, opp=1.0, tpl=np.where(is_commit, plan, O1root["tpl"]))),
    "O1_noTERM": plan_pol(mod(O1root, fin=np.zeros(7))),
    "O1_beta10": plan_pol(mod(O1root, beta=10.0)),
    "O1_noTRS": plan_pol(mod(O1root, trs=np.zeros(len(hf_units)))),
    "B0p": plan_pol(B0root),
    "B0p_opp1.5": plan_pol(mod(B0root, opp=1.5)),
    "B0p_paceO1": plan_pol(mod(B0root, tpl=np.where(is_commit, O1root["tpl"], 0.0))),
    "B0p_HFswap": plan_pol(mod(B0root, redeem=np.where(hf_mask, O1root["redeem"], 0.0), beta=O1root["beta"])),
    "B0p_opp1.5_paceO1": plan_pol(mod(B0root, opp=1.5, tpl=np.where(is_commit, O1root["tpl"], 0.0))),
}


def run(pols, truth, label, keep_world=True):
    s = Sim(D, w["gen"], NP, P.get("seeds.cert"), truth, P.get("simulation.chunk"), idio=bool(P.get("simulation.idio")),
            tpl_truth_seed=502)
    out = {k: [] for k in pols}
    extra = {"eqcum": [], "opp_year": [], "tail_year": [], "eq_year": []}
    nch = int(np.ceil(NP / s.chunk))
    for ci in range(nch):
        n = min(s.chunk, NP - ci * s.chunk)
        wd = s._chunk_world(ci, n)
        b0r = run_policy(D, wd, {"kind": "B0", "restore8": False})
        g_ext = b0r["green_path"].astype(bool)
        for nm, pol in pols.items():
            if pol["kind"] == "B0" and not pol.get("restore8", False):
                r = b0r
            else:
                pp = dict(pol, green_ext=g_ext) if pol["kind"] == "plan" else pol
                r = run_policy(D, wd, pp)
            out[nm].append({k: r[k] for k in ("twr", "twr_rep", "red", "maxdd", "lev_max", "lev_path", "lev_pre",
                                              "loss_path", "behind_path", "capcls_path")})
        if keep_world:
            f = wd["sim"]["f"]
            extra["eqcum"].append(f[:, :, 0].sum(1))
            extra["opp_year"].append(wd["oppret"].reshape(n, 5, 4).sum(2))
            extra["tail_year"].append(wd["tail"])
            extra["eq_year"].append(np.stack([f[:, 4 * y:4 * y + 4, 0].sum(1) for y in range(5)], 1))
    res = {k: {kk: np.concatenate([o[kk] for o in v]) for kk in v[0]} for k, v in out.items()}
    ex = {k: np.concatenate(v) for k, v in extra.items()} if keep_world else {}
    print(f"[{label}] simulated {NP} paths x {len(pols)} policies at {time.time() - t0:.1f}s", flush=True)
    return res, ex


def metrics(r, eqcum=None):
    twr = r["twr"]
    W = (1 + twr) ** 5
    m = {"p_goal": float(np.mean(twr >= 0.10)), "p_goal_rep": float(np.mean(r["twr_rep"] >= 0.10)),
         "mean": float(twr.mean()), "median": float(np.median(twr)), "sd": float(twr.std()),
         "cvar10": cvar_lower(twr, 0.10), "cvar5": cvar_lower(twr, 0.05), "cvar1": cvar_lower(twr, 0.01),
         "skew": float(skew(twr)), "exkurt": float(kurtosis(twr)), "sarle": sarle_bimodality(twr),
         "EW": float(W.mean()), "p_red": float(r["red"].mean()), "dd95": float(np.quantile(r["maxdd"], 0.95)),
         "lev_t0": float(np.median(r["lev_path"][:, 0])), "lev_max_med": float(np.median(r["lev_max"])),
         "p_twr_lt0": float(np.mean(twr < 0)), "p_twr_lt5": float(np.mean(twr < 0.05))}
    lp, pre, lo_, bh, cc = r["lev_path"], r["lev_pre"], r["loss_path"], r["behind_path"], r["capcls_path"]
    ys = slice(1, 5)
    m["lev_up_after_loss"] = float(((lp[:, ys] > pre[:, ys] + 0.01) & (lo_[:, ys] > 0.5)).mean())
    m["lev_at_cap_behind"] = float(((bh[:, ys] > 0.5) & (lp[:, ys] >= cc[:, ys] - 0.005)).mean())
    if eqcum is not None:
        y = 5 * np.log1p(twr)
        x = eqcum
        m["eq_beta_5y"] = float(np.cov(x, y)[0, 1] / np.var(x, ddof=1))
    return m


def line_interp(res, cv, scales=("1.0", "1.1", "1.2", "1.3")):
    xs = np.array([cvar_lower(res[f"B4_{s}"]["twr"], 0.10) for s in scales])
    ys = np.array([np.mean(res[f"B4_{s}"]["twr"] >= 0.10) for s in scales])
    o = np.argsort(xs)
    return float(np.interp(cv, xs[o], ys[o]))


def report(res, ex, label):
    rows = {}
    print(f"\n==== {label}")
    hdr = ("policy", "P(goal)", "Prep", "mean", "median", "cv10", "cv5", "cv1", "skew", "exkurt", "sarle", "EW/W0",
           "veq", "dd95", "lev0", "levmax", "upLoss", "capBeh", "eqbeta", "P<0")
    print(" | ".join(hdr))
    for k, r in res.items():
        m = metrics(r, ex.get("eqcum"))
        if not k.startswith("B4"):
            m["veq"] = m["p_goal"] - line_interp(res, m["cvar10"])
        else:
            m["veq"] = float("nan")
        rows[k] = m
        print(f"{k} | {m['p_goal']:.4f} | {m['p_goal_rep']:.4f} | {m['mean']:.4f} | {m['median']:.4f} | "
              f"{m['cvar10']:.4f} | {m['cvar5']:.4f} | {m['cvar1']:.4f} | {m['skew']:.3f} | {m['exkurt']:.3f} | "
              f"{m['sarle']:.3f} | {m['EW']:.4f} | {m['veq']:+.4f} | {m['dd95']:.3f} | {m['lev_t0']:.3f} | "
              f"{m['lev_max_med']:.3f} | {m['lev_up_after_loss']:.4f} | {m['lev_at_cap_behind']:.4f} | "
              f"{m.get('eq_beta_5y', float('nan')):.3f} | {m['p_twr_lt0']:.4f}")
    # paired differences vs O1_rule and vs B0
    for base in ("O1_rule", "B0", "B0p"):
        if base not in res:
            continue
        gb = res[base]["twr"] >= 0.10
        print(f"-- paired dP(goal) vs {base} (pp, 95% CI)")
        for k, r in res.items():
            if k == base or k.startswith("B4"):
                continue
            d = (r["twr"] >= 0.10).astype(float) - gb.astype(float)
            se = d.std(ddof=1) / np.sqrt(len(d))
            print(f"   {k}: {100 * d.mean():+.2f} [{100 * (d.mean() - 1.96 * se):+.2f}, {100 * (d.mean() + 1.96 * se):+.2f}]")
    return rows


allrows = {"opp_sharpe_draws": sr}
# 1. sealed truth as published (headline SR draw)
res1, ex1 = run(pols, w["book"]["truth"], "sealed truth, headline book (opp SR %.3f)" % w["book"]["truth"]["opp_sharpe_true"])
allrows["sealed"] = report(res1, ex1, "SEALED TRUTH (headline book)")

# overlay stress check (OV2-style offset): opportunistic P&L vs tail payoff in the worst equity years, O1 sizes held in $
eqy = ex1["eq_year"].ravel()
oppy = ex1["opp_year"].ravel()
taily = ex1["tail_year"].ravel()
q = np.quantile(eqy, [0.01, 0.05])
for lab, th in (("worst 1% equity years", q[0]), ("worst 5% equity years", q[1])):
    msk = eqy <= th
    opp_pl = 1.5 * oppy[msk]
    tail_pl = O1root["hed"] * taily[msk]
    print(f"OV2 check, {lab}: mean equity log excess {eqy[msk].mean():+.3f}; opportunistic P&L at IM 1.5 "
          f"{opp_pl.mean():+.3f} $bn (P5 {np.quantile(opp_pl, 0.05):+.3f}); tail ladder payoff at 6.15 notional "
          f"{tail_pl.mean():+.3f} $bn; mean loss/payoff ratio {(-opp_pl.mean()) / max(tail_pl.mean(), 1e-9):.2f}")
    allrows[f"ov2_{lab}"] = {"eq": float(eqy[msk].mean()), "opp_pl": float(opp_pl.mean()),
                             "opp_pl_p5": float(np.quantile(opp_pl, 0.05)), "tail_pl": float(tail_pl.mean())}

# 2. same paths, opportunistic Sharpe truth set to the prior mean 0.30
tr2 = copy.deepcopy(w["book"]["truth"])
tr2["opp_sharpe_true"] = P.get("truth_model.opp_sr_mean")
sub = {k: pols[k] for k in ("B0", "B4_1.0", "B4_1.1", "B4_1.2", "B4_1.3", "O1_rule", "O1_opp1.0", "O1_pace_plan",
                            "B0p", "B0p_opp1.5", "B0p_paceO1")}
res2, ex2 = run(sub, tr2, "sealed truth with opp SR = prior mean 0.30")
allrows["sealed_sr030"] = report(res2, ex2, "SEALED TRUTH, opportunistic Sharpe at the prior mean 0.30")

# 3. opportunistic Sharpe truth at zero (a book with no skill)
tr3 = copy.deepcopy(w["book"]["truth"])
tr3["opp_sharpe_true"] = 0.0
sub3 = {k: pols[k] for k in ("B0", "B4_1.0", "B4_1.1", "B4_1.2", "B4_1.3", "O1_rule", "O1_opp1.0")}
res3, ex3 = run(sub3, tr3, "sealed truth with opp SR = 0")
allrows["sealed_sr0"] = report(res3, ex3, "SEALED TRUTH, opportunistic Sharpe 0")

# 4. post-horizon commitment credits and the unfunded charge switched off in the evaluation only
P.overrides["pacing.c_pace"] = {"PE": 0.0, "SEC": 0.0, "RA": 0.0, "PC": 0.0, "CS": 0.0}
sub4 = {k: pols[k] for k in ("B0", "B4_1.0", "B4_1.1", "B4_1.2", "B4_1.3", "O1_rule", "O1_pace_plan", "B0p", "B0p_paceO1")}
res4, ex4 = run(sub4, w["book"]["truth"], "c_pace = 0 in the evaluation")
allrows["sealed_cpace0"] = report(res4, ex4, "SEALED TRUTH, c_pace = 0 in terminal wealth")
P.overrides.pop("pacing.c_pace")

# static exposure arithmetic (economic $bn) for B0 and O1 at t0
V0 = np.array([u["nav_econ"] for u in w["units"]])
Beq = np.array([u["B"][0] for u in w["units"]])
grp = D["group"]
x_o1 = 1 - O1root["sell"] - O1root["redeem"] + O1root["add"]
eq_b0 = float((V0 * Beq).sum() + P.get("overlay.beta_sq"))
hf_beq = Beq[hf_units]
eq_o1 = float((V0 * x_o1 * Beq).sum() + O1root["beta"] + (O1root["trs"] * hf_beq).sum())
print(f"\nStatic equity-beta dollars: B0 {eq_b0:.2f} ({eq_b0 / D['W0']:.3f} of W0); O1 after trades {eq_o1:.2f} "
      f"({eq_o1 / D['W0']:.3f} of W0), redeemed HF still earning HF returns in the notice year not counted", flush=True)
for g in ("PE", "SEC", "CO", "CS", "PC", "HF", "LO", "RA"):
    m_ = grp == g
    print(f"  group {g}: B0 {V0[m_].sum():.2f}  O1 {(V0 * x_o1)[m_].sum():.2f}")
allrows["static"] = {"eq_b0": eq_b0, "eq_o1": eq_o1, "W0": float(D["W0"])}
print(f"commitments a year: plan {plan[is_commit].sum():.2f}, O1 {O1root['tpl'][is_commit].sum():.2f}")
print(f"done at {time.time() - t0:.1f}s", flush=True)
json.dump(allrows, open(OUTJ, "w", encoding="utf-8"), indent=1)
