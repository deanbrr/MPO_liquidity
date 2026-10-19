"""Quick probe of v2 ladder magnitudes (not a deliverable). SYNTHETIC."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ra_ladder as RL  # noqa: E402

E = RL.E
for book in ("v1", "v1s", "v2u16", "v2u11"):
    for ra_mode in (["canonical"] if book.startswith("v2") else ["-"]):
        for opts_name, opts in ([("canon", {}), ("noavail", dict(availability=False)),
                                 ("g15", dict(mode="g15"))] if book.startswith("v2") else [("-", {})]):
            lev = RL.lev_of(reserve=0.08, book=book, census="v1")
            row = []
            for th in (0.0, 0.5, 0.6, 0.7, 0.76, 0.8, 0.9, 1.0):
                r = RL.gl_ladder(RL.s_star(th), lev, theta=th, ra_opts=dict(opts))
                row.append(f"{th:.2f}:G*{r['gstar']:6.2f}/SH{r['SH_TP']}")
            print(book, opts_name, " ".join(row))
lev = RL.lev_of(reserve=0.08, book="v2u16", census="v1")
r = RL.gl_ladder(RL.s_star(0.76), lev, theta=0.76)
for g in ("pe", "sec", "co", "cs", "pc", "ra"):
    d12, c12 = r["gf"][g]["dist"][:12].sum(), r["gf"][g]["calls"][:12].sum()
    d24, c24 = r["gf"][g]["dist"][:24].sum(), r["gf"][g]["calls"][:24].sum()
    print(g, f"12m {d12:.2f}/{c12:.2f}/{d12 - c12:+.2f} 24m {d24 - c24:+.2f}")
print("draw y1", r["cf"]["draw"][:12].sum(), "y2", r["cf"]["draw"][12:24].sum(), "fac", r["fac_need_24"])
