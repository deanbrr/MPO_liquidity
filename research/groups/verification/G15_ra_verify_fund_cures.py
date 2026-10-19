"""Hypothetical fund-level refinancing shortfalls under T4' if the dossier's own cure formula is applied to fund
sleeves (open-end and closed-end), which the engine currently excludes. Uses the scratch copy of g15_ra_calcs.
Usage: python -I fund_cures.py <dir_with_g15_ra_calcs_copy>
"""
import copy
import sys

sys.path.insert(0, sys.argv[1])
import g15_ra_calcs as g  # noqa: E402

base = g.run_book("T4prime", T=24)
sleeves = copy.deepcopy(g.SLEEVES)
for s in sleeves:
    s["direct"] = True          # apply the cure formula to every sleeve
alls = g.run_book("T4prime", T=24, sleeves=sleeves)
for h in (12, 24):
    b = sum(float(base[k]["cures"][:h].sum()) for k in base)
    a = sum(float(alls[k]["cures"][:h].sum()) for k in alls)
    fund = {k: round(float(alls[k]["cures"][:h].sum()), 3) for k in alls
            if not next(s for s in g.SLEEVES if s["id"] == k)["direct"]}
    coi = round(float(base["RE_COI"]["cures"][:h].sum()), 3)
    print(f"{h}m: modelled cures (direct sleeves) {b:.3f}, of which RE co-investment {coi}; "
          f"fund-sleeve shortfalls not modelled {a - b:.3f}; by fund sleeve {fund}")
