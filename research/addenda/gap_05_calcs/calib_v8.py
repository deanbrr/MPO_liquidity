"""Calibrate the v8-replica vol scale to v8's static-SAA outputs (mean 7.3%, P>=10% 31.7%, P10 -0.3%, P(DD>15%) 23.9%)."""
import sys

sys.path.insert(0, sys.argv[1])
sys.argv = [sys.argv[0], "unused.json", sys.argv[2] if len(sys.argv) > 2 else "20000"]
import numpy as np  # noqa: E402

import v8_rerun as V  # noqa: E402

V.N = int(sys.argv[2])
for vs in (0.6, 0.7, 0.8, 0.9, 1.0):
    R, reg, eps, par = V.gen_market(20261018, "named", vs)
    cfg = dict(V.CFGS["A_v8_replica"], kS=1.0, kM=1.0)
    on = {p: False for p in V.PLAYERS}
    yr = np.arange(V.T) // 12
    hs = np.zeros((V.T, V.N), bool)
    ann, navs, aux = V.simulate(cfg, on, R, reg, eps, par, hs, hs, yr)
    m = V.metrics(ann, navs)
    on_all = {p: True for p in V.PLAYERS}
    ann1, navs1, _ = V.simulate(cfg, on_all, R, reg, eps, par, hs, hs, yr)
    m1 = V.metrics(ann1, navs1)
    print(f"vol_scale {vs}: static {({k: round(v, 4) for k, v in m.items()})}  robust(kS=kM=1) {({k: round(v, 4) for k, v in m1.items()})}")
