# Q02 audit: robust scenario-analysis design (R2)

- **Date:** 2026-10-18.
- **Scope:** the research corpus named in the task. `design/ARCHITECTURE.md` exists but was not audited.
- **Tags:** as in 00_SYNTHESIS §0. [S] sourced, [C] corrected by a verifier, [I] inference or design default, [I-calc] computed.
- **Verdict: MOSTLY SUFFICIENT.** The design is ready and the build is close, but no scenario engine has yet been run as specified.

## 1. Answer today

**Yes, the research contains a robust scenario-analysis design with calibration targets. No working, validated generator exists yet.** The research *proposes* the design below (00_SYNTHESIS §4.1, §4.10, §5.1 item 4, §5.4; C1 §5.10–5.12; C3 §5.1). It does not show that the design works.

**Generator E**
- A monthly regime-switching factor model. The macro regime S_t follows a hidden semi-Markov chain, with K chosen from 3–5 by out-of-sample log score.
- About 20 factors, with t₅ innovations.
- CMA anchoring: exact ergodic mean matching, then 10-year compound-return roots, then a Higham correlation repair.
- An exit-window chain e_t (open, normal, drought, frozen).
- An oil/fiscal shock-type chain Z_t (N, B, SG, DB, SS, GW), coupled to S_t.
- Two-factor Brent with Gulf-war jumps, started from the futures curve.
- Implied-vol states (VIX tenor map, MOVE, OVX) keyed to S and Z.

**Model worlds**
- Six fee-consistent CMA models: M1–M3 base; M4 persistent drought; M5 stagflation; M6 "risk premia rise" with drought and overlay stress. All run on common random numbers.
- A held-out block-bootstrap/FHS generator.
- Search runs on at least 2 generator families. Sealed qualification runs once, on at least 2 disjoint worlds and at least 3 historical windows.

**Robustness and stress**
- Robustness metrics are reweightings of one scenario matrix (R1–R8):
  - KL worst-case probability, mean and CVaR;
  - W∞ for probabilities, W1 for Lipschitz metrics;
  - breakdown divergence η*;
  - misspecification sensitivity k_MS;
  - ensemble minimum and maximum.
- Stresses: eight named stresses, plus the calibrated stress family s*(θ).
- Reverse stress has three parts:
  - the minimum-KL failure world;
  - a Pesenti sensitivity ranking;
  - a red-team search over ScenarioSpecs that must beat the GW→SG→DB benchmark.
- IC views enter through entropy pooling, with KL and Kish-ESS gates.

| Value | Meaning | Source | Tag |
|---|---|---|---|
| 3–4pp vs ≈0.2pp | Spread of mean returns across CMA providers vs Monte Carlo error | 00_SYNTHESIS §1, finding 2 | [C]; SYNTHETIC stylised book |
| 6.2–9.7%; 27–51%; 31–55%; 0.02–0.06 nats | Fee-consistent ensemble: book return; P(5y ≥ 10%); P(5y < 7%); KL vs JPM | §7.1; verify-10 claim 6 | [C]; SYNTHETIC, JPM risk used for every model |
| η 0.05 (sweep 0.02–0.10); η_L 0.01; 0.5pp | KL reporting radius; rare-event radius; W∞/W1 radii | §4.10; C1 §5.11 | [I], re-derived from [C] |
| 50k × 120 months per model; SE ≈0.10pp | Reporting paths; standard error of a 5% probability at 50k paths | §4.1; C1 §7 | [I]; SE verified |
| θ* 0.76 (pooled 0.79); $13.9bn ($14.6bn) / $6.1bn / $0 | T4′ calibration at M6's P99.6; 24-month facility need with no action / pacing cut / owner band | gap_02 §1.2–1.3; groups synthesis §2.4 | [I-calc]; SYNTHETIC proxies |
| 1% met in M1–M5; M6 floor 2.4% (CP bound 2.5%) | Red-event gate T6 by model class | gap_02 §2.3 | [I-calc]; SYNTHETIC proxies |
| Calm ≥ 0.99; F_t 0.10 vs 0.17 base rate; drought 0.87; GW ≈0.85 | Initial state, October 2026 | gap_04 §4.2, §6.2 | [I-calc] on public data; GW elicited [I] |
| −0.14 / +0.43 / +0.32 | Monthly oil–equity correlation target (1988–2007 / 2008–19 / 2020–26) | C3 §6; dossier 03 §4.1 | [I-calc]; verifier reproduced it |
| N 0.55–0.65 … DB 0.02–0.06; P(crisis \| DB) ≥ 0.8 | Shock-type stationary-share and coupling targets | C3 §5.1(a) | [I] |

## 2. Evidence

**Strongest**
- **Verify-10.** 26 claims checked: 22 confirmed, 4 corrected, 0 refuted. The core formulas check out: R1–R3, the entropy-pooling dual and ergodic matching.
  - Rated MEDIUM: derived ranges and gate designs were wrong. C1 §2 and §4.10 carry the fixes.
- **Verify-03.** 28 of 32 claims confirmed, and every script reproduces exactly. Design inferences are rated medium.
- **gap_04.** A pre-registered out-of-sample harness (purge, embargo, Holm) defines F_t. Forecasts of 0.08 / 0.12 / 0.17 verified at 0.10 / 0.14 / 0.24 [I-calc].
- **Literature §4.8.** Robustness is "Refined", not contradicted. Topic 10: 21 citations found, 4 metadata mismatches, none fabricated.

**Weakest**
- **Engine E has never been built.** Every scenario number comes from `t1_engine.py`.
  - Its header says the models are "STYLISED PROXIES … NOT the production scenario engine E".
  - It is quarterly, uses Gaussian equity shocks and simulates no oil price (gap_02 §2.1, §7).
  - Stream 10's robustness prototype drew regimes i.i.d. (verify-10 R12).
- **The oil/fiscal layer has three open defects** (gap_04 §6.2):
  - a spot start gives a 2027 Brent average of $111, against EIA's $84;
  - the memoryless chain spends 49% of 2027 in GW, against the IMF's ≈17%;
  - the Ready-style supply/demand decomposition fails its back-check.
- **Shock labels depend on the identification scheme** (03.lit §5 item 2: Braun 2023; Kilian 2024).

**Contradictions between files**
1. The stream 10 dossier still carries uncorrected values:
   - η = 0.10;
   - P(5y ≥ 10%) of 27–59%;
   - ENS gates;
   - W1 threshold probabilities;
   - KL ≤ 1% gates.

   The synthesis and C1 carry the corrections and govern.
2. **View confidence:** C1 D14 and §5.12 use Meucci's linear blend. Synthesis §6.4 shrinks the view target instead.
3. **θ\*:** 0.76 and $13.9bn in the main synthesis; 0.79 and $14.6bn pooled in groups synthesis §2.4.
4. **Provider risk:** §4.1 and C1 D11 say each provider keeps its own volatilities, but no computation does. gap_05 §2 and stream 10 use JPM risk for every model (verify-10 R8); the gap_02 proxies share one equity volatility. The computed ranges therefore understate tail ambiguity.
5. **Breadth of the ensemble:** design brief P3 asks for worlds that vary calibrations, regime models and private-markets models. The ensemble varies only CMA means plus three structures on one factor architecture. Synthesis §9.2 item 3 concedes that a shared misspecification survives the ensemble.
6. **Literature refinements:** design brief §7 items 5–6 call for ambiguity on regime persistence, one DRO / robust-satisficing frontier, no stacked ambiguity sets, regime-conditional radii, tree reduction by filtration distance and re-simulated stress dynamics. Synthesis v1.1 has none of these; it re-simulates only for large IC views (§6.4).
7. **Notation and coupling:**
   - S_t and z_t both name the macro regime, Z_t names the shock type, and z_t also names the valuation gap.
   - G9 uses the regimes {B, N, D, C}.
   - Synthesis §4.1 leaves the S_t–e_t coupling unspecified; the proxy hard-codes one.

**Citation audit** (lit synthesis §2.3 and §2.4 item 13). None of these changes a number.
- Glasserman–Xu is misquoted.
- Heitsch–Römisch (2003) is a two-stage method. Multistage trees need their 2009 filtration-distance paper, which changes the method.
- The ENS diagnostic comes from Meucci (2012).
- Four references need metadata fixes.
- 37 stream-10 works are still unchecked.

## 3. Readiness

| Level | Status | Reason |
|---|---|---|
| DESIGN | Yes | Every element the question names has equations, defaults, targets, validation tests (§8) and rejected alternatives, with verifier corrections applied. |
| BUILD | Not yet (close) | The robustness layer, entropy-pooling solver, s*(θ), initial-state procedure and vol states can be coded now. The core generator still lacks: the S–e coupling; fixes to the Z chain; an assignment of worlds to the search and sealed planes; persistence ambiguity; and its estimation runs. |
| IC ANSWER | Yes, qualified | The IC can be given the design, its targets and proxy ranges labelled SYNTHETIC. There is no output from E, no probabilistic reverse-stress world and no entropy-pooling view on the ADIC-like book. Synthesis §9.2 item 10 also requires [I] toy results to be replicated in one engine before IC use. |
| NEEDS ADIC DATA | Yes, for calibration | The design itself needs no ADIC data. Calibration needs ADIC's owner draw history and fiscal basis, cash flows by vintage, bid and quote histories, and VM/IM and CSA history, to replace the US proxies (§7.2 items 2, 5, 8, 9, 16). |

## 4. Gaps

| Gap | Impact | Close by | Detail |
|---|---|---|---|
| E never built or jointly validated | High | build_experiment | Fit and run E. Check the CMA, drought-yield, VIX-persistence and oil-correlation targets together. |
| Oil/fiscal Z layer | High | more_research | Label history under several identification schemes, use a Dirichlet posterior over the labels, condition GW dwell on elapsed duration, and start from the futures curve. GW has no historical analogue, and P^BE and w_GW cannot be separately identified. |
| Narrow misspecification ensemble | High | build_experiment | Add alternative regime models, transition matrices and private-markets model families, and give each provider its own volatilities. |
| Assignment of worlds to the search and sealed planes | Medium | user_decision | Pre-register which models and generators belong to each plane. |
| Literature refinements not yet adopted | Medium | more_research | One frontier (the KL case is unproven), regime-conditional radii, no stacking, re-simulated reverse stress. Record each decision in an ADR. |
| Reverse stress never run on the book | Medium | build_experiment | KL cannot see outcomes outside the simulated paths, so rare liquidity breaches are missed. Add importance sampling or a Wasserstein reverse stress. |
| Governance parameters | Medium | user_decision | η; the T6 bands; M6's weight; the θ* rule (0.76, pooled 0.79 or mixture 0.42); model weights. |
| Thin, US-proxy targets | Medium | adic_data | Tail dependence rests on 2 of 24 vs 7 of 23 months. There is only one drought spell, and the frozen state has no historical analogue. |
| Inconsistencies (view-confidence rule, θ*, notation) | Low | user_decision | Choose one rule and one set of symbols. |
| Missing market data; unchecked citations | Low | more_research | FX and CDX option-vol data; GMO and Research Affiliates CMAs; the 37 unchecked stream-10 references. |
