# Q12 challenge: the IC discussion layer (R12)

**Auditor's verdict:** mostly_sufficient (design yes, build no, IC answer no, ADIC data yes).
**Skeptic's verdict:** **partial.** The four readiness flags stand; the verdict does not. The audit contradicts itself on build readiness, calls an unreconciled design "reconciled", and the evidence supports the failure modes far better than the remedies.

Scope: the research corpus as of 2026-10-18; `design/` is cited only where it changes the picture.

## 1. Number checks (10)

| Number | Found | Where | Note |
|---|---|---|---|
| Tier A ≈$0.44bn ($0.4425bn) | Yes | synthesis §6.1; verify-14 §5 | [I] default on the client's NAV |
| 12 seats; ≤40% per family ⇒ ≥3 families | Yes | synthesis §6.2; groups §7.1 | Arithmetic holds: ⌊0.4×12⌋ = 4 seats per family [I-calc]. The roster itself is stale (G1) |
| 41 claims: 35 / 4 / 0 / 2 | Yes | verify-14 §1, §7 | [S] |
| ≈6,300 per arm (4,000–11,000) | Yes | synthesis §6.6; C4 §6.11; verify-14 R1 | 6,279 at BS_model = 0.20 (numcheck14 output) [C] |
| In-sample EVSI 0.07–1.51pp; cross-fitted ≈0 | Yes | verify-14 R2, §5 | [C], toy simulation, **true EVSI = 0 only** |
| −0.120 vs −0.210 | Yes | verify-14 R3; C4 §6.6 | [C], toy |
| c = 0.6: 30% → 18% | Yes | synthesis §6.4; C4 §6.4; verify-14 R13 | [C] |
| KL flags 0.05 / 0.25 / 1.20 / 2.30; ESS ≥ 5,000; weight ratio ≤ 50 | Yes | synthesis §6.4; C4 §6.4, §7 | [I]. The 1.20 and 2.30 thresholds come from ENS/N = e^−KL, which holds only under uniform p (dossier 14 §6.5a; verify-14 R17) |
| 0.02–0.06 nats | Yes | synthesis L11 [C]; verify-10 §1, R1; C4 §8 ("Medium") | Rests on the verifier's "illustrative haircuts" (verify-10 §1), not on raw CMA data |
| 16/16 found; 0 mismatched; 10 unchecked | Stale | 14.lit §1; lit synthesis §2.1 | `literature/recheck/14_ic_deliberation.recheck.md` re-checked all 10: 8 ok, 2 mismatched |

**Also confirmed:** 15pp / 10bp CE and $17.7m per bp [C] (C4 §5.4, §8); Hedges' g [S] (verify-14 F9); n = 439 [C] (F1); 1,475 in 281 groups (14.lit §1 item 1, not §5 row 4 as cited); 17 months [I-calc, SYNTHETIC] (synthesis §6.7).

## 2. Where the audit overstates

1. **"Complete and reconciled."** The audit's own §2 lists four open contradictions, and synthesis §6.3/§6.6 still carry ≤2 debate rounds, "≥80% surfacing" and a rotating human devil's advocate, all challenged by the literature (14.lit §4.3; §5 rows 2, 4).
2. **"Specified well enough to build an MVP" (§1) contradicts its own BUILD = Not yet.** In the research:
   - `Ballot`, `DecisionRecord`, `MinorityReport`, `Signpost` and `ForecastRecord` are names marked "See §6" (C4 §5.2); §6 has only prose.
   - The belief/value split's "committee median (q_m, θ_m)" is never defined (dossier 14 §6.5c; C4 §6.5); the pooled rule uses q̄ instead.
   - θ_k is a placeholder.
3. **"Evidence-informed at the level of mechanisms."** This holds for failure modes, not for remedies:
   - The source study for the blind pre-vote found no accuracy gain, and its AI-first arm did marginally better (recheck row 23; verify-14 R5).
   - Non-concurrent advice traded over-reliance for under-reliance, with no net gain (Kokje 2026; 14.lit §5 row 5).
   - Mandatory "how could it be wrong" notes raised acceptance of wrong suggestions (Beck 2025; row 7).
   - Showing the AI's track record did not produce appropriate reliance (He 2023; row 8).
   - Evidence gating is untested (verify-14 R6).

   No remedy has positive efficacy evidence in a committee setting.
4. **"3–4pp model range vs ≈0.2pp MC error" mixes units:** a spread of mean annual returns (synthesis §1 finding 2) against the Kish SE of a probability (dossier 14 §6.5a). The conclusion survives like-for-like: P(10y ≥ 10%) spans 20–54% across models [I-calc, SYNTHETIC] (synthesis §1 finding 1).
5. **Gap 13 is stale.** The 10 citations it lists as unchecked were re-checked (table above).

## 3. Gaps the audit missed

- **G1. The roster assumes seven groups; the brief now has eight.** Brief R14 and §8 rule 1 require IC seats generic over groups, with a seat for the Real Assets head. No Real Assets synthesis is on disk. The main synthesis, the groups synthesis and ARCHITECTURE §8.5 all still have twelve seats.
- **G2. Decision-log contracts are unspecified in the research** (§2 item 2). ARCHITECTURE.md defines a `DecisionRecord`, but it sits outside the corpus.
- **G3. The human electorate is undefined.** C4 §6 sets a ⅔ quorum and synthesis §6.1 a simple majority, but neither names the voters; 14.lit §4.3's 5–7-member voting core is neither adopted nor rejected.
- **G4. Human beliefs → q_k.** H0 elicits probabilities and a provisional action, not ViewSpecs, yet minimax regret needs a q_k per member; frozen questions would need to be simulator-measurable. The audit's gap 7 covers AI seats only.
- **G5. Scoring horizon.** "Every IC probability Brier-scored at 1, 4 and 8 quarters" cannot cover 10-year probabilities. Which proxy questions are valid is still open (C4 §13 Q9).
- **G6. DEFER operating characteristics.** numcheck14 tests only the case true EVSI = 0. Nothing estimates false-DEFER or missed-DEFER rates under the LCB₀.₈₀ rule, and the "no staged action dominates" condition has no test.
- **G7. η_max against view size.** Shifting a path metric's mean by δ costs KL ≈ δ²/2σ², so 0.05 nats admits about 0.32σ [C, identity; verify-10 §5]. No one has computed typical IC views' KL on SYN-ADIC-177; if most exceed η_max, minimax regret runs over a credal set close to {p}.
- **G8. No ablations of the remedies.** The suites in synthesis §6.6 do not A/B the pre-vote ordering, cognitive forcing or the track-record display, and under-reliance is not a tracked KPI.
- **G9. Further unadopted literature** (14.lit §4.1–4.6): a conviction band (Bär), an influence cap, a Red Team aimed at the AI's recommendation (Chiang), an integration step, a plan-consistency state variable.
- **G10. No IDM acceptance test.** The Phase-0 exit criteria and the six MVP questions cover only liquidity, actions and the return bridge (synthesis §10).
- **G11. KL thresholds after tilted re-simulation.** With non-uniform p, 1.20 and 2.30 nats lose their ENS rationale; they become bare [I] defaults (low).

## 4. Revised verdict

**Partial.** The layer can be **designed**: failure-mode evidence is strong (verify-14 rates sourced facts HIGH). It cannot be **built** from the research alone (G1–G4, G10), and evidence that its remedies improve decisions is null or contested (§2 item 3, G8). Readiness is unchanged: design true; build false; IC answer false; needs ADIC data true.
