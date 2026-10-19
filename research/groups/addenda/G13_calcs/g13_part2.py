"""Runs the non-desmoothing G13 tests (V-RA1, R4-R9, P1-P4) with the same seeds and sizes as the full run,
so they are available while the Kalman recovery tests (R1-R3) are still running. SYNTHETIC - NOT ADIC DATA.
Run: .venv/Scripts/python.exe -I -B g13_part2.py   (writes g13_ra_marks_results_part2.json)"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import g13_ra_marks_sim as g  # noqa: E402

W, T, SEED = 200, 80, 20261018
t0 = time.time()
res = dict(label=g.SYN, run=dict(worlds=W, T=T, seed=SEED, part="2 (V-RA1, R4-R9, P)"))
res["sales_vs_appraisal"] = g.test_sales_vs_appraisal(max(20, W // 2), T, SEED)
res["bias"] = g.test_bias(W, T, 40, SEED)
res["scoring"] = g.test_scoring(max(20, W // 4), T, SEED)
res["fusion"] = g.test_fusion(max(20, W // 2), T, SEED)
res["bf_benktander"] = g.test_bf(max(20, W // 2), SEED)
res["openend"] = g.test_openend(max(20, W), T, SEED)
res["public"] = g.public_illustrations()
res["run"]["seconds"] = round(time.time() - t0, 1)


def conv(o):
    import numpy as np
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


(HERE / "g13_ra_marks_results_part2.json").write_text(json.dumps(res, indent=1, default=conv), encoding="utf-8")
print("wrote part2 in", res["run"]["seconds"], "s", g.SYN)
