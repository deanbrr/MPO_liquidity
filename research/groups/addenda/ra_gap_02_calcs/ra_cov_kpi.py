"""Which controllable loans breach the s7.5 test P(covenant trigger within 12 months) <= 2%? SYNTHETIC - NOT ADIC DATA.
Usage: python -B ra_cov_kpi.py [n_paths]
"""
import json
import sys

import ra_engine as E

n = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
assets, tranches, _ = E.load_tape()
amap = {a["asset_id"]: a for a in assets}
out = {}
for scen in ("base_mc", "t4p_struct"):
    r = E.run(scen, n=n, keep=True)
    rows = []
    for (sl, ctl, p), t in zip(r["_diag"]["trig_loans"], [t for s in E.C_SLEEVES for t in tranches if t["sleeve"] == s]):
        if ctl and p > 0.02:
            a = amap.get(t["asset_id"], {})
            rows.append({"tranche": t["tranche_id"], "sleeve": sl, "segment": a.get("segment"), "lender": t["lender"],
                         "trap_dscr": t["cov_trap_dscr"], "ltv_cov": t["cov_ltv_max"], "p_trigger_12m": round(p, 4)})
    out[scen] = rows
    print(scen, json.dumps(rows, indent=0))
json.dump(out, open("ra_cov_kpi_results.json", "w", encoding="utf-8"), indent=1)
