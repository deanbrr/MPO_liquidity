"""Per-world breakdown (M1, M2, M6) of the headline certification (SYNTHETIC - NOT ADIC DATA).
Usage: pythonw fin_sim3.py <out.txt>
"""
import sys
import os
import json
import time

sys.dont_write_bytecode = True
OUT = open(sys.argv[1], "w", encoding="utf-8")
sys.stdout = OUT
sys.stderr = OUT
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
ids, I = D["ids"], D["I"]
tnames = D["tpl_names"]
hf_units = list(np.flatnonzero(D["is_hf"]))
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


def pol(r):
    return {"kind": "plan", "root": r, "nodes": {}, "stage1": [], "children": {}, "feat_mu": D["tr"]["feat_mu"],
            "feat_sd": D["tr"]["feat_sd"], "restore8": True, "playbook_years": (1,), "playbook": False}


pols = {"B0": {"kind": "B0", "restore8": False},
        "B4_1.0": {"kind": "B4", "restore8": False, "scale": 1.0},
        "B4_1.1": {"kind": "B4", "restore8": False, "scale": 1.1},
        "B4_1.2": {"kind": "B4", "restore8": False, "scale": 1.2},
        "B4_1.3": {"kind": "B4", "restore8": False, "scale": 1.3},
        "O1_rule": pol(O1), "O1_opp1.0": pol(dict(O1, opp=1.0)), "O1_beta10": pol(dict(O1, beta=10.0))}
s = Sim(D, w["gen"], 10000, P.get("seeds.cert"), w["book"]["truth"], P.get("simulation.chunk"), idio=True,
        tpl_truth_seed=502)
out = {k: [] for k in pols}
wl = []
for ci in range(8):
    wd = s._chunk_world(ci, 1250)
    wl.append(wd["w"])
    b0r = run_policy(D, wd, {"kind": "B0", "restore8": False})
    g = b0r["green_path"].astype(bool)
    for k, p_ in pols.items():
        r = b0r if p_["kind"] == "B0" else run_policy(D, wd, dict(p_, green_ext=g) if p_["kind"] == "plan" else p_)
        out[k].append(r["twr"])
res = {k: np.concatenate(v) for k, v in out.items()}
wv = np.concatenate(wl)
names = P.get("worlds.names")
print("world | n | policy | P(goal) | mean TWR | CVaR10 | CVaR1 | value at equal tail (own-world B4 line)")
for wi, nm in enumerate(names):
    m = wv == wi
    xs = np.array([cvar_lower(res[f"B4_{s_}"][m], 0.10) for s_ in (1.0, 1.1, 1.2, 1.3)])
    ys = np.array([np.mean(res[f"B4_{s_}"][m] >= 0.10) for s_ in (1.0, 1.1, 1.2, 1.3)])
    o = np.argsort(xs)
    for k in ("B0", "B4_1.1", "O1_rule", "O1_opp1.0", "O1_beta10"):
        t = res[k][m]
        pg = np.mean(t >= 0.10)
        cv = cvar_lower(t, 0.10)
        veq = pg - np.interp(cv, xs[o], ys[o]) if not k.startswith("B4") else float("nan")
        print(f"{nm} | {m.sum()} | {k} | {100 * pg:.2f} | {100 * t.mean():.2f} | {100 * cv:.2f} | {100 * cvar_lower(t, 0.01):.2f} | {100 * veq:+.2f}")
    d = (res["O1_rule"][m] >= 0.10).astype(float) - (res["B0"][m] >= 0.10)
    print(f"{nm}: O1_rule - B0 dP {100 * d.mean():+.2f}pp (se {100 * d.std(ddof=1) / np.sqrt(m.sum()):.2f}); "
          f"dMean TWR {100 * (res['O1_rule'][m].mean() - res['B0'][m].mean()):+.2f}pp")
print(f"done {time.time() - t0:.1f}s")
