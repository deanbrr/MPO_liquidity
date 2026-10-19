"""G12 episode statistics for listed proxies (US industries, Ken French 49) vs Brent. [I-calc] on public data.

Episodes: 2014-06..2016-01 oil bust (supply glut), 2008-06..2009-02 (demand bust), 2020-01..2020-04 (demand bust),
2022-01..2022-12 (supply spike), 2026-02..2026-08 (Gulf war). Reports cumulative total returns.
Usage: python -I g12_episode_stats.py <data_dir> <out_json>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g12_oil_betas import INDUSTRIES, parse_eia_daily, parse_ff_first_monthly_block, read_zip_csv  # noqa: E402


def main():
    data_dir, out_json = Path(sys.argv[1]), Path(sys.argv[2])
    brent = parse_eia_daily(data_dir / "eia_brent_daily.html")
    ind = parse_ff_first_monthly_block(read_zip_csv(data_dir / "ind49.zip"))
    ff3 = parse_ff_first_monthly_block(read_zip_csv(data_dir / "ff3.zip"))
    b_me = brent.resample("ME").last()
    b_me.index = b_me.index.to_period("M")
    M = pd.DataFrame(index=ind.index)
    M["Market"] = ff3["Mkt-RF"] + ff3["RF"]
    for c in INDUSTRIES:
        M[c] = ind[c]
    eps = {"oil_bust_2014-06_2016-01": ("2014-07", "2016-01", "2014-06"),
           "gfc_2008-06_2009-02": ("2008-07", "2009-02", "2008-06"),
           "covid_2019-12_2020-04": ("2020-01", "2020-04", "2019-12"),
           "covid_2019-12_2020-03": ("2020-01", "2020-03", "2019-12"),
           "supply_spike_2021-12_2022-12": ("2022-01", "2022-12", "2021-12"),
           "gulf_war_2026-02_2026-08": ("2026-03", "2026-08", "2026-02")}
    out = {"label": "[I-calc] public data; listed US industry proxies; not ADIC data", "episodes": {}}
    for k, (a, b, base) in eps.items():
        W = M.loc[pd.Period(a, "M"):pd.Period(b, "M")]
        cum = (1 + W).prod() - 1
        bo = float(b_me.loc[pd.Period(b, "M")] / b_me.loc[pd.Period(base, "M")] - 1)
        out["episodes"][k] = {"brent_change": round(bo, 3), **{c: round(float(v), 3) for c, v in cum.items()}}
    Path(out_json).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
