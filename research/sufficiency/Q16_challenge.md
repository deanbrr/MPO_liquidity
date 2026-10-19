# Q16 challenge: liquidity survival and Corporate Finance funding

**Scope.** This is an adversarial check of `Q16_audit.md`. I only read files and ran no engine. Every [I-calc] figure is **SYNTHETIC**: SYN-ADIC-177, census v1.0, allocation v1 and proxy models M1–M6. "Skeptic arithmetic" marks my own derivations, which are not research results.

## 1. Verdict

**Revised: partial** (the audit said mostly_sufficient). The design holds and the build holds narrowly. But the audit's single blocker (re-running the revolver at 50%) understates the work: the numbers sit on a book the client has already replaced, and "literal T4 cannot be bought, T4′ can" compares rows at different facility credits.

## 2. Numbers checked

All ten load-bearing figures are where the audit cites them: $25–92bn; $32.2bn and 15 months; $17.7bn / $26.6bn and PIF's $15bn; θ\* = 0.76 and G\* = $11.1bn (`gap02_results.json` calibration.targets: 11.10 at θ = 0.759); $13.9bn / $6.1bn / $0; pooled θ\* 0.79 and $14.6bn; $13.6bn against $14.2bn; $32.7bn and $64.9bn; and 0.98%, 0.79%, 2.4% and 5.2–5.8%. `t1_engine.py` l.594 matches (index 3 = demand bust, DB; 5 = Gulf war, GW). Two figures carry a meaning problem (§3, items 1 and 3).

## 3. Claims refuted or overstated

1. **The literal-versus-calibrated comparison mixes conventions.**
   - `gap02_study.py` hard-codes facility credit at 80% for s\*(θ) (l.46) and 50% for literal T4 (l.55).
   - s\*(1.0) has exactly literal T4's gap ($16.08bn; JSON `gstar_theta`).
   - At equal credit, literal T4 needs $20.1bn at 80% or $32.2bn at 50%. T4′ needs $13.9bn at 80% or ≈$22.2bn at 50% (skeptic arithmetic: need = gap ÷ credit, l.969).
   - The brief sets credit at ≤50% (§7 item 2). At that level, do-nothing T4′ also exceeds PIF's $15bn, which was the test used to demote literal T4.
   - The "defensible direction" therefore holds only for T4′ plus pacing (≈$9.8bn) or plus the band.
2. **"Facility credit is already a parameter" is only half true.**
   - Only the ladder has it. The T6 Monte Carlo hard-codes availability (l.594: 80% in DB/GW crises, 90% in other crises, 100% otherwise), and the covenant flag (l.687) never cuts availability, despite the research citing Chodorow-Reich–Falato for that channel.
   - The build contract fixes 80% (ARCHITECTURE ADR-35; §4.9 l.581), while its H node limits use 100/100/50% by regime (l.706). Yet l.60 requires P, H and T4′ to reconcile by identity tests.
   - No ADR adopts or rejects brief §7 item 2, and `BUILD_SPEC.md` does not exist.
3. **T5 is the wrong yardstick for facility size.**
   - Limit 1 caps *drawn* recourse debt (00_SYNTHESIS §4.5 l.914). Drawn debt equals the gap: $16.1bn for literal T4 and $11.1bn for T4′. Both sit inside the $17.4bn hard limit even on stressed NAV (gap_02 §0).
   - At 50% credit the binding limit is market capacity: PIF $15bn [S], Mubadala $2bn and Danantara $1bn (groups gap_01 §4) [S; Danantara snippet-level].
4. **The census item is misclassified.**
   - "T4′ on census v1.1" is filed as needing ADIC data. But the user has already chosen v1.1 (context §1A l.155; brief §8), and ARCHITECTURE makes it the default (l.89). Re-running is a build experiment.
   - This re-run also pulls against the 50% correction. On v1.1, literal T4 falls to $19.5–21bn with fixed-USD draws and $2–4bn with current-NAV draws (groups gap_02 §0) [I-calc].
5. **Mix A's certification is fragile.**
   - Its point estimates are 0.900% (M4) and 0.906% (M5), with one-sided bounds of 0.973% and 0.979% (JSON `R15_N0_P6c_B0_Q14_A0_H0`) [I-calc]. A neighbouring mix fails at 1.02% (gap_02 §2.3).
   - Four un-run corrections each push P(red) up: availability at ≤50%; the literature's two-quarter pacing lag (the ladder credits the cut from month 2, l.871; the Monte Carlo at once, l.466–467); no revolver lead time in the Monte Carlo, though no revolver exists today; and no covenant feedback.
   - Its P99 debt/NAV reaches 17.5% (M5) and 32.4% (M6) against the 15% hard limit, through passive drift.
6. **"An owner-agreed 5% draw removes it."** The ladder applies the band in all 23 crisis months with certain acceptance (l.879–880), withholding roughly $14bn from the owner in the oil–fiscal state (skeptic arithmetic). The audit flags acceptance as a gap yet states $0 as a result.

## 4. Gaps the audit missed

| Gap | Impact | Close by |
|---|---|---|
| **Allocation v2 and Real Assets.** v2 "supersedes" v1, whose "numbers will be re-run" (context l.137). It moves $18bn out of PE and adds ≈$4bn unfunded, oil-linked energy assets, open-end queues, capex calls and asset-debt refinancing (brief §8). No T4′ or T6 number includes it; G10–G15 have not landed | high | build_experiment |
| **No oil factor.** Draw targets come from shock-type labels (gap_02 §7), so the "oil + crisis" state is a label, not a simulation | high | build_experiment |
| **8% floor relaxed without a decision.** The client deck makes IG + cash ≥ 8% a hard limit (context l.212); the 8%-elastic / 4%-hard split is unratified. A hard 8% floor adds ≈$4.7bn to the gap (literal T4: $16.1bn → $20.7bn, gap_02 §1.3). T4′ would then need ≈$19.7bn at 80% or ≈$31.6bn at 50% (skeptic arithmetic) | high | user_decision |
| **≤50% is itself an inference.** G7 literature B14 gives no percentage; Li–Strahan–Zhang find 2020 line draws were honoured with Fed support. Needs a 0–80% sweep with GCC-lender wrong-way risk, not a point swap | medium | build_experiment |
| **Revolver maturity.** A 3+2-year facility runs through a five-year Monte Carlo with no rollover logic, only a fee (l.162); literature §4.3 flags rollover risk | medium | build_experiment |
| **T6 not replicated across seeds.** gap_02's single θ\* seed was the lowest of ten (groups gap_01 §0) | medium | build_experiment |
| **Tightening premium.** The ≈1.1pp premium is missing from the audit's gap table | low | build_experiment |

## 5. Revised readiness

| Level | Ready? | Reason |
|---|---|---|
| Design | Yes | The design survives this check |
| Build | Yes, narrowly | Core code and tests exist. It needs an ADR settling availability across H, P and T4′, and the l.594 availability values turned into a parameter |
| IC answer | No | No facility figure exists on the current book (allocation v2, census v1.1) at the brief's conventions. The pending corrections pull in opposite directions |
| ADIC data | Yes | Hedge-fund terms τ, existing lines and covenants, syndicate appetite, Real Assets terms and a written band agreement |
