"""Replication books with the opportunistic Sharpe draw neutralized (SYNTHETIC - NOT ADIC DATA).

For one replication book: rebuild and re-solve O1 exactly as tasks.run_book does (world.build + run_gbo), then
simulate B0, the risk-matched line and O1 (playbook and rule) on the book's own sealed truth (as published) and with
the truth's opportunistic Sharpe set to the prior mean (0.30) and to 0. Writes nothing into the project folder.
Usage: pythonw fin_books.py <BOOK_ID> <out.txt> <out.json>
"""
import sys
import os
import json
import time
import copy

sys.dont_write_bytecode = True
BOOK = sys.argv[1]
OUT = open(sys.argv[2], "w", encoding="utf-8")
sys.stdout = OUT
sys.stderr = OUT
OUTJ = sys.argv[3]
HERE = r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2"
os.chdir(os.path.dirname(os.path.abspath(sys.argv[2])))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from common import Params, cvar_lower  # noqa: E402
import world  # noqa: E402
from tasks import run_gbo  # noqa: E402
from sim import Sim  # noqa: E402

SPEC = {"BOOK_7101": (7101, {"alpha_dispersion": 0.5, "bid_info": 1.0, "placebo": False}),
        "BOOK_7102": (7102, {"alpha_dispersion": 1.5, "bid_info": 1.0, "placebo": False}),
        "BOOK_7103": (7103, {"alpha_dispersion": 0.5, "bid_info": 0.5, "placebo": False}),
        "BOOK_7104": (7104, {"alpha_dispersion": 1.5, "bid_info": 0.5, "placebo": False}),
        "BOOK_PLACEBO": (20261019, {"alpha_dispersion": 1.0, "bid_info": 1.0, "placebo": True})}
t0 = time.time()
P = Params(os.path.join(HERE, "params.json"))
sd, var = SPEC[BOOK]
w2 = world.build(P, log=None, book_seed=sd, variant=var, phase1=False)
o1 = run_gbo(w2, {"id": BOOK + " GBO"})
print(f"{BOOK}: GBO ok={o1.get('ok')} label={o1.get('label')} phi={o1.get('phi')} at {time.time() - t0:.1f}s", flush=True)
rt = o1["root"]
print("root: beta %.3f opp %.3f hed %.3f E/W %.3f trs %s fin %s" % (rt["beta"], rt["opp"], rt["hed"], rt["E_W0"],
      np.round(rt["trs"], 3).tolist(), np.round(rt["fin"], 3).tolist()), flush=True)
print("templates", dict(zip(w2["D"]["tpl_names"], np.round(rt["tpl"], 3).tolist())), flush=True)
pols = {"B0": {"kind": "B0", "restore8": False}}
for s_ in (1.0, 1.1, 1.2, 1.3):
    pols[f"B4_{s_}"] = {"kind": "B4", "restore8": False, "scale": s_}
pols["O1_playbook"] = o1["policy"]
pols["O1_rule"] = dict(o1["policy"], playbook=False)
pols["O1_rule_opp1.0"] = dict(o1["policy"], playbook=False, root=dict(o1["policy"]["root"], opp=1.0))


def veq(res, name, idx):
    cvs = np.array([cvar_lower(res[f"B4_{s}"]["twr"][idx], 0.10) for s in (1.0, 1.1, 1.2, 1.3)])
    ps = np.array([np.mean(res[f"B4_{s}"]["twr"][idx] >= 0.10) for s in (1.0, 1.1, 1.2, 1.3)])
    o = np.argsort(cvs)
    cv = cvar_lower(res[name]["twr"][idx], 0.10)
    return float(np.mean(res[name]["twr"][idx] >= 0.10) - np.interp(cv, cvs[o], ps[o]))


out = {"book": BOOK, "opp_sharpe_true": w2["book"]["truth"]["opp_sharpe_true"], "root_opp": rt["opp"],
       "root_beta": rt["beta"], "root_E_W": rt["E_W0"]}
for lab, srv in (("own", None), ("sr030", 0.30), ("sr0", 0.0)):
    tr = copy.deepcopy(w2["book"]["truth"])
    if srv is not None:
        tr["opp_sharpe_true"] = srv
    s = Sim(w2["D"], w2["gen"], 10000, P.get("seeds.cert") + 1000, tr, 2000, idio=True, tpl_truth_seed=sd + 1)
    res = s.evaluate(pols)
    ent = {}
    for nm, idx in (("first4000", slice(0, 4000)), ("all10000", slice(0, 10000))):
        e = {k: float(np.mean(res[k]["twr"][idx] >= 0.10)) for k in pols}
        e.update({f"veq_{k}": veq(res, k, idx) for k in ("O1_playbook", "O1_rule", "O1_rule_opp1.0")})
        e.update({f"cvar10_{k}": cvar_lower(res[k]["twr"][idx], 0.10) for k in ("B0", "O1_playbook", "O1_rule")})
        ent[nm] = e
    out[lab] = ent
    print(f"[{lab}] opp SR {tr['opp_sharpe_true']:.3f} at {time.time() - t0:.1f}s:", json.dumps(ent), flush=True)
json.dump(out, open(OUTJ, "w", encoding="utf-8"), indent=1)
print("done", flush=True)
