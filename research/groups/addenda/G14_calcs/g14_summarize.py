"""Print a compact summary of g14_ra_actions_results.json (SYNTHETIC - NOT ADIC DATA)."""
import json
from pathlib import Path

R = json.loads(Path(__file__).with_name("g14_ra_actions_results.json").read_text())
print(R["label"])

print("\n== Queue machine: cash share by quarter (P5 / P50) and value cost at ell ==")
for s, q in R["B_queue_machine"]["by_start_regime"].items():
    p5 = q["cash_share_P5_by_quarter"]
    p50 = q["cash_share_P50_by_quarter"]
    print(f"start {s}: P5 q1/q2/q4/q8 = {p5[0]:.2f}/{p5[1]:.2f}/{p5[3]:.2f}/{p5[7]:.2f}; "
          f"P50 q1/q2/q4/q8 = {p50[0]:.2f}/{p50[1]:.2f}/{p50[3]:.2f}/{p50[7]:.2f}")
    print("   value cost:", {k.replace('value_cost_at_ell_', 'ell='): v for k, v in q.items() if k.startswith('value_cost')})

print("\n== Refinancing wall: book totals ($bn, 24m) ==")
for reg, d in R["C_refinancing_wall"]["regimes"].items():
    t = d["book_totals_bn"]
    print(f"{reg}: ruthless mean {t['ruthless']['cash_in_mean']:.2f} p95(sum) {t['ruthless']['cash_in_p95']:.2f} "
          f"walk GAV {t['ruthless']['walk_gav']:.2f} | reputation mean {t['reputation_bound']['cash_in_mean']:.2f} "
          f"p95(sum) {t['reputation_bound']['cash_in_p95']:.2f}")
    for c, v in d["cohorts"].items():
        ru = v["ruthless"]
        print(f"   {c:<20} Pgap {ru['P_shortfall']:.2f} gap|D {ru['mean_shortfall_given_gap_pct_D']:.2f} "
              f"Puw {ru['P_underwater']:.2f} Pwalk {ru['P_walk']:.3f} Psale {ru['P_forced_sale']:.2f} "
              f"trap(float) {ru['P_cash_trap_floating_subbook']:.2f} dV {ru['mean_value_change']:+.2f}")

print("\n== SELL vs REFI threshold T* ==")
print(json.dumps(R["D_sell_vs_refi_threshold"], indent=1))
print("\n== Delta by LTV ==", R["E_delta_by_ltv"])
print("\n== Headroom cost conversion (PV per $ of month-24 headroom) ==")
for k, v in sorted(R["A_headroom_cost_conversion"]["levers"].items(), key=lambda kv: kv[1]):
    print(f"   {v:7.3f}  {k}")
