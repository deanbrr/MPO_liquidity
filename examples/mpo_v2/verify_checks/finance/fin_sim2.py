"""Further decompositions of O1 on the headline book (SYNTHETIC - NOT ADIC DATA). Same set-up as fin_sim.py.
Usage: pythonw fin_sim2.py <out.txt> <out.json>
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
HERE = r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2"
os.chdir(os.path.dirname(os.path.abspath(sys.argv[1])))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from common import Params, cvar_lower  # noqa: E402
import world  # noqa: E402
from prep import prepare  # noqa: E402
from sim import Sim, run_policy  # noqa: E402

t0 = time.time()
P = Params(os.path.join(HERE, "params.json"))
R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
w = world.base(P)
D = prepare(P, w["units"], w["beliefs"], w["book"], w["gen"], w["tr"], use_beliefs=True)
ids, I, K = D["ids"], D["I"], len(D["tpl"])
tnames = D["tpl_names"]
hf_units = list(np.flatnonzero(D["is_hf"]))
plan = np.array([t.get("plan", 0.0) for t in D["tpl"]])
is_commit = D["tpl_is_commit"]
cards = {c["unit_id"]: c for c in R["cards"]}
root = R["root"]
FIN = ["REV", "TERM", "NAVF", "PREF", "CSBL", "SMABL", "RACO"]
trs = np.zeros(len(hf_units))
for row in R["change_list"]:
    if row["unit_id"].startswith("TRS:"):
        trs[hf_units.index(ids.index(row["unit_id"][4:]))] = row["size_bn"]
fin = np.zeros(7)
for k, v in root["debt_bn"].items():
    fin[FIN.index(k)] = v
O1 = {"sell": np.array([cards[u]["sell_frac"] for u in ids]), "redeem": np.array([cards[u]["redeem_frac"] for u in ids]),
      "add": np.array([cards[u]["add_frac"] for u in ids]),
      "tpl": np.array([root["templates_bn"].get(nm, 0.0) for nm in tnames]), "p2s": 0.0,
      "beta": float(root["synthetic_beta_bn"]), "trs": trs, "hed": float(root["tail_notional_bn"]),
      "opp": float(root["opp_im_bn"]), "fin": fin, "Lup": 0.0}
hmin = P.get("overlay.tail_budget")[0] / P.get("overlay.tail_premium")
B0r = {"sell": np.zeros(I), "redeem": np.zeros(I), "add": np.zeros(I), "tpl": np.where(is_commit, plan, 0.0),
       "p2s": 0.0, "beta": P.get("overlay.beta_sq"), "trs": np.zeros(len(hf_units)), "hed": hmin * D["W0"],
       "opp": P.get("overlay.opp_im_sq"), "fin": np.zeros(7), "Lup": 0.0}


def pol(r):
    return {"kind": "plan", "root": r, "nodes": {}, "stage1": [], "children": {}, "feat_mu": D["tr"]["feat_mu"],
            "feat_sd": D["tr"]["feat_sd"], "restore8": True, "playbook_years": (1,), "playbook": False}


def mod(r, **kw):
    r2 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in r.items()}
    r2.update(kw)
    return r2


hf = D["is_hf"]
pc = D["group"] == "PC"
lo = D["group"] == "LO"
ra02 = np.array([u == "RA-02" for u in ids])
pace_plan = np.where(is_commit, plan, O1["tpl"])
no_purch = np.where(is_commit, O1["tpl"], 0.0)
hfswap = dict(redeem=np.where(hf, O1["redeem"], 0.0), beta=O1["beta"])
pols = {
    "B0": {"kind": "B0", "restore8": False},
    "B4_1.0": {"kind": "B4", "restore8": False, "scale": 1.0},
    "B4_1.1": {"kind": "B4", "restore8": False, "scale": 1.1},
    "B4_1.2": {"kind": "B4", "restore8": False, "scale": 1.2},
    "B4_1.3": {"kind": "B4", "restore8": False, "scale": 1.3},
    "O1_rule": pol(O1),
    "O1_slim(noTRS,noTERM,pace_plan)": pol(mod(O1, trs=np.zeros(len(hf_units)), fin=np.zeros(7), tpl=pace_plan)),
    "O1_noHFredeem": pol(mod(O1, redeem=np.where(hf, 0.0, O1["redeem"]))),
    "O1_noLOadds": pol(mod(O1, add=np.zeros(I))),
    "O1_noPCtrades": pol(mod(O1, sell=np.where(pc, 0.0, O1["sell"]), tpl=no_purch)),
    "O1_noRA02redeem": pol(mod(O1, redeem=np.where(ra02, 0.0, O1["redeem"]))),
    "SIMPLE3(HFswap+opp1.5)": pol(mod(B0r, opp=1.5, **hfswap)),
    "SIMPLE4(HFswap+opp1.5+LOadds)": pol(mod(B0r, opp=1.5, add=np.where(lo, O1["add"], 0.0), **hfswap)),
    "SIMPLE3_opp1.0(HFswap+LOadds)": pol(mod(B0r, add=np.where(lo, O1["add"], 0.0), **hfswap)),
}


def run(pols, truth, label):
    s = Sim(D, w["gen"], 10000, P.get("seeds.cert"), truth, P.get("simulation.chunk"), idio=True, tpl_truth_seed=502)
    res = s.evaluate(pols)
    xs = np.array([cvar_lower(res[f"B4_{s_}"]["twr"], 0.10) for s_ in ("1.0", "1.1", "1.2", "1.3")])
    ys = np.array([np.mean(res[f"B4_{s_}"]["twr"] >= 0.10) for s_ in ("1.0", "1.1", "1.2", "1.3")])
    o = np.argsort(xs)
    print(f"\n==== {label} ({time.time() - t0:.1f}s)")
    g0 = res["B0"]["twr"] >= 0.10
    g1 = res["O1_rule"]["twr"] >= 0.10
    rows = {}
    for k, r in res.items():
        if k.startswith("B4"):
            continue
        twr = r["twr"]
        pg = float(np.mean(twr >= 0.10))
        cv = cvar_lower(twr, 0.10)
        v = pg - float(np.interp(cv, xs[o], ys[o]))
        d0 = (twr >= 0.10).astype(float) - g0
        d1 = (twr >= 0.10).astype(float) - g1
        rows[k] = {"p_goal": pg, "mean": float(twr.mean()), "cvar10": cv, "cvar1": cvar_lower(twr, 0.01), "veq": v,
                   "d_vs_B0": float(d0.mean()), "d_vs_O1": float(d1.mean()),
                   "se_vs_O1": float(d1.std(ddof=1) / np.sqrt(len(d1)))}
        print(f"{k:34s} P {pg:.4f} mean {twr.mean():.4f} cv10 {cv:+.4f} cv1 {rows[k]['cvar1']:+.4f} veq {100 * v:+.2f}pp "
              f"dP vs B0 {100 * d0.mean():+.2f}pp  dP vs O1 {100 * d1.mean():+.2f}pp (se {100 * rows[k]['se_vs_O1']:.2f})")
    return rows


allr = {"sealed": run(pols, w["book"]["truth"], "SEALED TRUTH (headline book, opp SR 0.672)")}
tr2 = copy.deepcopy(w["book"]["truth"])
tr2["opp_sharpe_true"] = 0.30
allr["sr030"] = run(pols, tr2, "SEALED TRUTH, opp SR 0.30")
json.dump(allr, open(OUTJ, "w", encoding="utf-8"), indent=1)
print("done", flush=True)
