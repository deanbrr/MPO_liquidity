# Q05 audit (R5): can ADIC reach the 10% nominal target?

*Research-sufficiency audit, 2026-10-18. Read-only on the corpus. Every ADIC figure is SYNTHETIC (context §1A working allocation v1) unless stated. Tags follow the synthesis: [S] sourced, [C] corrected, [I] inference, [I-calc] computed, [U] unverified. [Aud] marks this auditor's own rough check (`C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\q05_audit\r8_sensitivity.py`), not a research result.*

**Verdict: mostly sufficient.** There is an explicit, coded, evidence-based bridge, and its direction is clear. But its headline numbers sit on a superseded allocation, and its only "Plan" verdict breaks under conventions the corpus has not settled.

## 1. Answer today

The research gives a positive account of the route to 10% and concludes that ADIC should expect about 8–9% nominal, not 10%. On evidence-central assumptions, 10% is a stretch in most capital-market models. No single lever closes the gap; it closes only through a joint outcome, leverage at the cap *and* above-median levers.

| Item | Value | Source | Tag |
|---|---|---|---|
| Fee-consistent CMA beta, 10y geometric | 5.8–10.0% (equal-weight mean 7.85%) | gap_05 §1, §3 | [I-calc] SYNTHETIC |
| + α\* (8 sleeves) / + overlay / + leverage 1.05× / − drags | +0.37 / +0.37 / −0.02 to +0.23 / −0.31 to −0.64pp | gap_05 §5–§6; synthesis §4.12 | priors [I]; sums [I-calc] |
| Evidence-central E[R] | 6.1–10.5% (mean 8.3%) | gap_05 §6 | [I-calc] SYNTHETIC |
| P(10y TWR ≥ 10%) | 20–54% (mean 36%) | gap_05 §6 | [I-calc] SYNTHETIC |
| Verdicts | **Plan** M2 (BlackRock fee-adjusted, 10.47%). **Stretch** M1/M4/M5 (J.P. Morgan-anchored): gap 1.1–1.4pp; P(true μ ≥ 10%) 0–16% at 1.05×, 12–38% at 1.30×. **Aspiration** M3/M6 (AQR; BlackRock "risk premia rise"): gap 3.2–3.9pp | gap_05 §1, §6 | [I-calc] SYNTHETIC |
| M1 single-lever break-evens | PE +4.7pp/yr; co-investment +12.3; secondaries +15.5; hedge funds +10.1; overlay SR 1.02 at 1.5% vol; leverage 1.42× (cap 1.30×). Prior probability of each ≤ 0.2% | gap_05 §7 | [I-calc] SYNTHETIC |
| v8 deck's +3.5pp route to 10% | Falls to +0.61 / +0.35 / +0.47pp; ≈30% was knowledge of the path, ≈54% unevidenced claims | gap_05 §8; synthesis §4.11 | [I-calc] SYNTHETIC |
| Real-preserving return hurdles | 7.9 / 10.8 / 13.9% at a 5 / 7.5 / 10% payout. At 8.3%, real NAV holds only at a ≈5.3% payout | synthesis §2.3(a); gap_05 §1 | [I-calc] |

ADIC's endowment model "rests on beta and liquidity management, not on demonstrated alpha": central α\* plus the overlay adds +0.75pp a year (gap_05 §4). Leverage buys the most P(10%), +7.6pp at the cap in M1, but it is beta. It lifts volatility from 14.4% to 18.2%, destroys value in M6, and must never be sized to the gap. P(10%) is reported, never maximized (synthesis §1 findings 1, 8, 9).

## 2. Evidence

**Strongest sources.**
- gap_05 §1–§10, with `bridge.py` and `v8_rerun.py`. I read the results JSONs, and every figure above reproduces from them (M1: beta 8.330%, central 8.845%, P(μ ≥ 10%) 0.95% with independent levers). The regression test reproduces verifier 10 exactly (9.17% arithmetic, 13.08% vol, 8.39% geometric). My replication of M2 matches gap_05 exactly.
- **CMA inputs** were checked against primary sources and put on a fee-consistent basis (verifier 10: 22 of 26 claims confirmed, 4 corrected, none refuted) [S/C].
- **Lever-prior evidence** is citation-verified in the G1, G4 and G5 logs (Korteweg–Sorensen, Harris–Jenkinson–Kaplan–Stucke, Begenau–Siriwardane, Braun–Jenkinson–Schemmerl, Fang–Ivashina–Lerner, Ben-David–Birru–Rossi, Dichev–Yu) [S]. The priors themselves are judgment syntheses [I] (gap_05 §10; synthesis §9.2 item 16).
- **The literature supports** the payout arithmetic (lit. §4.1) and never maximizing P(10%) (lit. §4.7).

**Weak points.**
- gap_05 has no adversarial verification log of its own.
- Its base-rate anchor, Ennis's −1.87pp, is flagged twice. Verifier 02 reattributes it to a 2021 paper. The literature audit (§2.3) says the figure is not in that paper's abstract and must be verified [U].

**Contradictions.**
1. **Allocation.** The bridge uses working allocation v1 (PE $52bn). Context §1A v2 carves Real Assets ($18bn) out of PE, "supersedes" v1, and says the seven-group numbers "will be re-run". The Real Assets research (G10–G15) is not on disk.
2. **Hedge-fund priors.** Main §4.3 sets hedge-fund α priors of 0.5–2.0%. The bridge (§4.12) uses 0 central. The literature (§4.11) and design brief §7.8 require α ≈ 0, with α = 0 as a mandatory sensitivity. The benchmarks differ (factor α versus J.P. Morgan's median-manager line), and the benchmark-definition field does not reconcile them.
3. **Lever priors versus the literature verdicts** (lit. §3.7, §3.9, §4.11; brief §7.8), none folded into gap_05:
   - PE should weight GP access over selection (Korteweg–Panageas–Systla 2026) and add a fund-size penalty.
   - Private Credit should use a fund-age prior (Böni–de Roon: alpha falls from 8.2% early to 3.9% late) with a downside-beta charge, instead of the zero prior from Erel–Flanagan–Weisbach.
   - Long-only priors should be sleeve-specific (+31bp net for institutional accounts).
4. **Risk convention.** The bridge applies J.P. Morgan's 2026 Σ to every model (verifier 10-R8, still open). It also treats BlackRock's figures as compound returns plus J.P. Morgan's arithmetic-to-compound spread. [Aud] Re-running M2 with BlackRock's own PE and equity vols:
   - means held fixed: 9.97%, P(μ ≥ 10%) 48–49%, a Stretch;
   - conversion consistent with BlackRock's vols: 10.69%, a Plan;
   - BlackRock's figures read as arithmetic: 8.84%, a Stretch.

   The only "Plan" is therefore convention-dependent. Ennis et al. (2026), with listed-buyout β ≈ 1.5 (lit. 04), also suggests PE risk is understated.
5. **Drags versus Tier-1 cost.** The bridge's drags for reserve, facilities and pacing (0.14 / 0.03 / 0.09pp in M1) are not tied to gap_02's certified mixes, which cost a 21bp premium with the owner band and 62bp without it. gap_02 also prices the 14% reserve and the pacing lever at 28bp each, on a different cost measure.
6. **Leverage cap.** Verifier 06 notes that 1.30× sits below CPP (≈1.36×) and OTPP's 2024 level (1.43×). M1's 1.42× break-even is a peer-level exposure, so the cap is a choice, not a fact.

The main and groups syntheses do not conflict here, because the groups layer never recomputes the bridge. (The "bridge" stage in groups gap_04 is an engine reconciliation.)

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | Yes | The formula, double-count guard, lever priors, drag list, τ treatment, verdict rule and WYNTB card are all specified (gap_05 §2, §9; synthesis §4.12, §6.7). |
| BUILD | Yes | `bridge.py` runs, with a regression test and `test_v8_replica` (±0.05pp). Expose per-provider Σ, BlackRock compounding and a Real Assets class as switches. |
| IC ANSWER | Yes, directional | "10% is a stretch, not the central case (mean ≈8.3%), and no single lever closes it" survives every open issue found; most push lower. The per-model labels and decimals need the v2 re-run and the convention fix before anyone quotes them. |
| NEEDS ADIC DATA | Yes | Real weights; net PME and fee terms; co-investment deal flows; secondary discounts against outcomes; the overlay's full trial list (for the deflated Sharpe ratio); treasury and financing terms; the owner's definition of the target. |

## 4. Gaps

| Gap | Impact | Close by |
|---|---|---|
| The bridge runs on the superseded v1 allocation. Add a Real Assets CMA line and prior, then re-run on v2 | High | build_experiment |
| M2's "Plan" depends on BlackRock compounding and per-provider risk (verifier 10-R8); BlackRock's methodology tab may settle it | High | more_research |
| Model weights: the equal-weight mean gives J.P. Morgan 3 of 6 seats; the IC must vote (synthesis §9.3 Q14) | High | user_decision |
| The lever priors are judgmental; update them with ADIC's realized evidence through FBE credibility weighting (gap_05 §9 items 2 and 9) | High | adic_data |
| The real book, treasury, facility and financing terms drive both the weights and the drags | High | adic_data |
| The literature's prior revisions (PE access, Private Credit fund-age, long-only by sleeve, hedge-fund α = 0 sensitivity) are not applied | Medium | more_research |
| Drags are not tied to the Tier-1 mix chosen in gap_02 | Medium | build_experiment |
| The target's definition (gross or net, which horizon) is only assumed (C3 DQ1; synthesis §9.3 Q2) | Medium | user_decision |
| Leverage appetite: the 1.30× cap against M1's 1.42× break-even | Medium | user_decision |
| The bridge is analytic and lognormal, with a fixed SAA; its [I-calc] figures must be replicated in the production engine (gap_05 §10) | Medium | build_experiment |
| gap_05 has no adversarial log, and Ennis's −1.87pp is unverified | Low | more_research |
