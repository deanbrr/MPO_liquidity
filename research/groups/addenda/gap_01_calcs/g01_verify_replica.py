"""Assert that g01_core.gl_ladder reproduces gap_02's t1_engine.ladder exactly. SYNTHETIC - NOT ADIC DATA."""
import g01_core as G
from g01_core import E, s_star, t4_literal

READINGS = {
    "s*(0.76)": s_star(0.76),
    "s*(0.42)": s_star(0.42),
    "T4 literal canonical": t4_literal(),
    "T4 as written": t4_literal(floor=0.08),
    "T4 critic": t4_literal(floor=0.08, draw_basis="fixed_usd", hf_pass=0.0, pc_cs_rates=(0.0, 0.0)),
    "T4 current": t4_literal(draw_basis="current"),
}
POLICIES = [E.Policy("A"), E.Policy("r", rcf=13.9), E.Policy("c", pace_cut=True), E.Policy("b", band=True),
            E.Policy("am", amber_t0=3.0), E.Policy("MixA", rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
            E.Policy("MixB", rcf=10.0, pace=12.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0),
            E.Policy("nav", navf=2.0)]
KEYS = ("min_head_tpf_24", "SH_TP", "SH_TPF", "fac_need_24", "gstar", "nco24")
worst = 0.0
for rn, s in READINGS.items():
    for pol in POLICIES:
        a = E.ladder(s, pol)
        b = G.gl_ladder(s, pol=pol)
        for k in KEYS:
            va, vb = a[k], b[k]
            if va is None or vb is None:
                assert va == vb, (rn, pol.name, k, va, vb)
                continue
            worst = max(worst, abs(va - vb))
            assert abs(va - vb) < 1e-9, (rn, pol.name, k, va, vb)
print("replica OK; max abs diff", worst)
