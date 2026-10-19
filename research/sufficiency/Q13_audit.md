# Q13 audit: prior deck v8, what survives, what changes, is it sound

Research-sufficiency audit, 2026-10-18. **Verdict: mostly sufficient.** Every quantity below is SYNTHETIC (v8's stylized book or the SYN working allocation) unless marked *public data*. Tags follow synthesis §0. [I-aud] marks this auditor's own check.

## 1. Answer today

**What survives is the architecture.**
- The safety-first, growth-second, never-target-chasing structure: Tier 1A survival set, Tier 1B floor, Tier 2 objective (synthesis §4.9, L9).
- A hard liquidity gate. v8's IG + cash and P99-margin coverage become T2/T3 and the 24-month T4′ stress.
- The state engine as a risk conditioner rather than a return forecaster (gap_04 §1).
- The overlay as the fast hedge lever, and the Shapley/ablation machinery.
- v8's rules, kept as a frozen comparator (brief P6).
- QDD, kept as a governance tool scored on forecast skill (gap_05 §9.6).
- The motto, kept verbatim as P1.

**What changes is most of the numbers and four mechanisms.**
- **Tier-1 floor.** "≤5% chance the 5-year return is below 7%" needs a 15.8–17.9% expected return. P(5y<7%) is 31–55% on fee-consistent CMAs (verifier 10 #7; C1 §1 item 4) [C]. The replacement is a mixture median of the 10-year TWR ≥ 7% plus a worst-model CVaR10% ≥ 0. The 7% thereby becomes a central-tendency test (dossier 11 §6.4, C4).
- **Tier 2.** "Maximize P(10%) + α\*" becomes CRRA utility with a squared shortfall, and P(10%) is reported only. With leverage, maximizing P(10%) replicates a digital option (Browne [S]). In a toy model it moves P from 34% to 68% at the cost of a 4.6% chance of a >40% loss [I].
- **IG + cash.** An 8% hard floor fails at t0 by $0.56bn, so it becomes 8% elastic and 4% hard (synthesis §4.9 T2; untagged, built on [A]).
- **State engine.**
  - F_t is a calibrated 3-month stress probability from a forward-filtered HMM.
  - Turbulence and the absorption ratio add nothing out of sample: all 12 Holm-adjusted p = 1.0 (gap_04 §4; *public data*, [I-calc]).
  - Valuation and mean reversion leave the policy.
  - The HSMM must pass the same harness; the K4 proxy failed.
  - Eight lights become a 12-row panel with three layers. The market layer reads calm (F_t 0.10 vs a 0.17 base rate), while the exit layer (drought 0.87) and the owner layer (Gulf war 0.85) read stressed (gap_04 §6.2).
- **Uplift re-estimate** (gap_05 §8, [I-calc]).
  - v8's +3.5pp falls to +0.61pp on the v8 book, +0.35pp on the ADIC book on the named path, and +0.47pp ex ante.
  - Ablations attribute ≈30% of the uplift to knowing the path and ≈54% to unevidenced claims for α\*, QDD and the overlay.
  - Survive: overlay +0.37–0.38pp (only if the DSR gate passes) and state +0.11–0.16pp.
  - Do not survive: mean reversion (−0.04 to +0.14), α\* reallocation (−0.01 to +0.04) and QDD (+0.02).

**Is it sound?** Directionally, yes; several specific claims are overstated (§2). What the IC can be told today: the architecture stands, the headline numbers do not, and a realistic uplift is a fraction of a point, mostly from an *assumed* overlay Sharpe ratio.

## 2. Evidence

**Strongest sources.**
1. **Tier-1 infeasibility.** Recomputed independently by verifier 10 (#7, R6) [C]. Strong.
2. **State-engine rebuild.** A pre-registered out-of-sample harness, 1990–2026, with purge/embargo, HAC, Holm and both halves, on *public data* (gap_04 §3–4). Strong for "no added information". Limited by US proxies and ≈30 independent drawdown episodes (§10).
3. **Objective change.** Browne is confirmed by verifier 11 (#1). Literature §4.7 supports never maximizing P(10%) and requires a shortfall exponent above 1, which J meets.
4. **Uplift re-run.** v8_rerun.py: exact 64-coalition Shapley on common random numbers (CRN), 50k paths. Moderate. I re-derived the ablation shares from v8_rerun_results.json: 29.4% and 53.7%, with singles summing to −2.92 against a joint −2.89. The arithmetic holds [I-aud]. But no verifier log covers any gap addendum, and gap_05 §10 requires replication "before IC use".
5. **Supporting evidence.**
   - Stand-alone attribution misleads: index 0.7–2.6 (groups synthesis §4.3) [I-calc].
   - The paper reports "the decomposition rather than the headline"; its fixed anchor supplied 55.8% of the margin (l.2658–2663, 2705–2707) [S].

**Contradictions and overstatements.**
- **State protection's risk effect is a whole-policy effect.**
  - Synthesis §4.11 credits state protection with cutting P(drawdown > 15%) from 31.6% to 19.8% and forced sales from 4.4% to 0.03%.
  - v8_rerun.py computes those metrics only for the empty and full coalitions. The full coalition includes the put spread, a 5% reserve top-up and a facility [I-aud].
- **"Reproduces v8 exactly"** (synthesis §4.11).
  - The replica is calibrated. Notionals were scaled to 62% and 48%, and the additive terms were fitted, so the attribution rows match by construction.
  - Levels match only approximately: 7.14% vs 7.3% and 10.64% vs 10.8% (gap_05 §8A).
- **The survivors are priors.**
  - The overlay's +0.375pp is the prior SR of 0.30 × 1.25% volatility (gap_05 §4). α\* and QDD are likewise prior × exposure.
  - "≈54% unevidenced" swaps v8's assertions for literature priors. It does not measure ADIC skill.
- **The lab gate counts the wrong uncertainty.**
  - The bridge treats lever uncertainty as non-diversifying (gap_05 §2). The re-run draws SR, α and QDD per path, so the ≤0.4bp Shapley SE is Monte Carlo error only.
  - The §9.6 gate (lower 95% bound ≥ 5bp) would pass the overlay on its prior, although the prior's P10 is SR −0.02 [I-aud].
- **"Lose money"** (synthesis finding 10) vs gap_04 §7: none of the seven timing rules clears zero at 90%. Contrarian timing, for example, is −48bp with a CI of −121 to +21.
- **The Tier-2 critique** (literature 11; verifier 11 R12).
  - "Secure the floor, then maximize P(goal)" is legitimate goals-based practice.
  - Unlevered, it risks only the cushion. The objection holds for ADIC because ADIC may lever.
- **Resolved.**
  - C1 §1 item 3 still accrues payouts at 10%; synthesis v1.1 §4.9 corrects this.
  - Dossier 10's 24–55% and 16.6% were corrected to 31–55% and 15.8–17.9%.
  - Dossier 01's "[S deck]" floor wording is inference (verifier 01 R15).
- **Minor.** v8's +280bp secondaries α\* is called "break-even-scale" (gap_05 §7; synthesis §4.12), but the break-even is +15.5pp.

**Citation-audit items** (literature §2.4).
- Schwenk (1990) is overstated (item 9). This bears on the deck's devil's advocate, and Nemeth (2001) favours authentic dissent (§3.12).
- The DSR lacks its non-normality term (item 11), and dealer backtests lose a median 73% of their Sharpe ratio live (§4.13). Both weaken the only surviving alpha component.
- Moreira & Muir is disputed out of sample (item 7).
- No audit entry covers gap_04's or gap_05's own citations.

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | Yes | An element-by-element mapping with reasons: synthesis §4.9 table, §4.11 and §6.7; gap_04; P1/P6. ARCHITECTURE.md's R13 row (outside this corpus) adopts it. |
| BUILD | Nearly (no) | F_t, the panel, Tier 1A/1B, J, the Shapley/CRN protocol, `test_v8_replica` and the prototypes are all specified. Three items are not: the gate's uncertainty definition is defective, per-player tail attribution is specified but was never applied, and rolling Tier 1B (literature §3.2) is undecided. |
| IC ANSWER | Yes (directional) | The mapping and the order of magnitude are defensible on synthetic data. The attributions must be restated and replicated first (gap_05 §10). |
| NEEDS ADIC DATA | Yes | Overlay track record and trial list, memo-corpus outcomes, net PME and fee terms, ADIC's VM, bid and draw histories, and the real book. |

## 4. Gaps

| # | Gap | Impact | Close | Detail |
|---|---|---|---|---|
| 1 | gap_05 is unverified | high | build_experiment | Replicate in the production engine, with an independent verifier. |
| 2 | The survivors are literature priors | high | adic_data | The overlay DSR needs the full trial list (non-normality term, provenance severity); QDD needs memo outcomes; α\* needs net PME. |
| 3 | The floor has been re-specified | high | user_decision | 5-year at 95% becomes a 10-year median plus a worst-model CVaR10 ≥ 0. The deck author must accept it. |
| 4 | Risk metrics are not attributed per player | medium | build_experiment | Apply the §4.11 tail-marginal rule to P(drawdown) and P(forced sale). |
| 5 | The gate uses Monte Carlo SE | medium | more_research | Use parameter uncertainty (the bridge's τ) or per-world draws. |
| 6 | One fixed filter drives "30% path knowledge" | medium | build_experiment | Run sensitivity with gap_04's F_t filter and macro-identified regimes (literature 10). |
| 7 | Tier 1B on the working book was never computed | medium | build_experiment | Lognormal check at σ 14.4% with the bridge's E[R]: worst-model CVaR10 ≈ −0.8% (M3) and −1.5% (M6), so it likely fails [I-aud]. |
| 8 | F_t targets are US proxies | medium | adic_data | Use ADIC's VM, bid and draw histories (gap_04 §9.9). |
| 9 | Wording | low | more_research | Correct "exactly", "lose money" and "break-even-scale" before the IC sees them. |
