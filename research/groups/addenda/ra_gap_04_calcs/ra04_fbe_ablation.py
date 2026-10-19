"""
ra_gap_04 - design ablation of the robust RA forecast engine (FBE-R-RA).   SYNTHETIC - NOT ADIC DATA.

Which components of the robust estimator help on the RA world? Runs before any gate is frozen; it chooses the
estimator structure, not gate values. Options: u-f covariance on/off; control coefficient and w_a estimated or
fixed (-1, 0.30); fusion by GLS or by the sec. 8.5 rule (precision weights shrunk 50% toward equal).
Run:  set RA04_W=600 ; .venv\\Scripts\\python.exe -I -B -W ignore ra04_fbe_ablation.py  -> ra04_fbe_ablation_results.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ra04_fbe_ensemble as F  # noqa: E402

OPTS = {
    "R_full_gls": dict(),
    "R_noCuf_gls": dict(use_cuf=False),
    "R_fixedCoef_gls": dict(fixed_ra_coefs=True),
    "R_fixedCoef_noCuf_gls": dict(fixed_ra_coefs=True, use_cuf=False),
    "R_shrink50": dict(fusion="shrink50"),
    "R_fixedCoef_shrink50": dict(fixed_ra_coefs=True, fusion="shrink50"),
    "R_fixedCoef_shrink50_noCuf": dict(fixed_ra_coefs=True, fusion="shrink50", use_cuf=False),
}


def main():
    F.load_rame_linkage()
    out = dict(label=F.SYN, worlds=F.W, table={})
    for i, v in enumerate(["M0", "M1", "M2", "M4", "M5", "M5s", "M6", "MALL"]):
        d = F.generate(v, 5000 + i, {})
        o = F.metrics(d, *F.oracle(d))
        row = {"oracle": o, "B": F.metrics(d, *F.fbe_b(d))}
        for k, opt in OPTS.items():
            m, s, _ = F.fbe_r(d, **opt)
            row[k] = F.metrics(d, m, s)
        for k, r in row.items():
            if k == "oracle":
                continue
            r["crps_excess_vs_oracle"] = r["crps_pp"] / o["crps_pp"] - 1
            r["regret_excess_vs_oracle"] = r["regret_pp"] / o["regret_pp"] - 1
            r.pop("cov80_by_segment", None)
        out["table"][v] = row
        print(v, " | ".join(f"{k}: {r['crps_excess_vs_oracle']:+.1%}/{r['cov80']:.3f}/{r['bias_sell_pp']:+.2f}/"
                            f"{r['regret_excess_vs_oracle']:+.0%}" for k, r in row.items() if k != "oracle"), flush=True)
    (HERE / "ra04_fbe_ablation_results.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
