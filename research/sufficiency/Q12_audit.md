# Q12 audit: the IC discussion layer (R12)

**Question.** Is the Investment Committee discussion layer (IC pack, shadow IC, protocol, Q&A, view conditioning, decision log) evidence-based and specified well enough to build?

**Verdict: mostly_sufficient.** Ready to design, nearly ready to build. Not yet able to tell the IC whether it works.

**Scope.** Research corpus only, as of 2026-10-18. Tags follow synthesis §0: [S] sourced; [C] verifier-corrected; [I] inference or default; [I-calc] recomputed. "Lit" means an abstract-level item from the literature sweep.

## 1. Answer today

The research **proposes** an IC Deliberation Module (IDM); it does not **show** that it works. The design is complete and reconciled across dossier 14, verify-14, C4, synthesis v1.1 §6 and groups synthesis §7:

- **Decision rights.** Tier A triggers include actions ≥ 0.25% of NAV, ≈$0.44bn [I] (synthesis §6.1). A symmetric irreversibility protocol applies, with Board and owner escalations.
- **Shadow IC.** Twelve mandate-defined seats. AI seats flag and never vote. At ≤40% of seats per model family, ≥3 families are needed and 4 is the target [I] (§6.2).
- **Protocol** (§6.3):
  - frozen questions at T−10;
  - independent seat assessments;
  - evidence-gated debate on ≤3 cruxes;
  - pre-mortem and hashed minority reports;
  - a **blind human pre-vote**, then an ordered reveal and the ballot.
- **Q&A and views** (§6.4):
  - Answers cite `run_id:artifact:path`.
  - Asset-return views feed the Forward Belief Engine (FBE).
  - Scenario views go through entropy pooling with target shrinkage: at c = 0.6, "30% below base" becomes 18% below [C].
  - KL flags sit at 0.05 / 0.25 / 1.20 / 2.30 nats, with Kish ESS ≥ 5,000 [I]. They are anchored on a cross-provider KL of 0.02–0.06 nats [C] (synthesis L11, public CMA data).
- **Rules and log** (§6.5–6.6):
  - Disagreement is measured in regret, with a belief/value split. A minority report triggers at 15pp or 10bp CE [I].
  - Irreversible actions use minimax regret. DEFER is allowed only on cross-fitted EVSI.
  - Signposts carry hysteresis.
  - Decision, dissent and override ledgers are append-only, and every IC probability is Brier-scored at 1, 4 and 8 quarters.

**Plain answer.** The layer is evidence-informed at the level of mechanisms. It is specified well enough to build an MVP on synthetic data. Nobody can yet say whether it improves IC decisions:
- An online trial would need ≈6,300 effective forecasts per arm to detect a 0.01 Brier gain [C] (§6.6). Evidence of efficacy can therefore come only from offline suites and 6–12 months of shadow mode.
- No IDM component has run. The research calcs contain no entropy-pooling solver, implied-action code, shadow-IC run or IC pack.
- The only IC-facing numbers so far come from other components. Example: "liquidity gate red, 17 months under T4′ on the do-nothing book" [I-calc, SYNTHETIC] (§6.7).

## 2. Evidence

**Strongest sources.**
- **Verify-14:** 41 claims checked; 35 confirmed, 4 corrected, 0 refuted, 2 unverifiable. Sourced facts rate HIGH and the design layer MEDIUM (§1, §7). C4 and the synthesis fix its three main defects, each shown on toy simulations [C]:
  - R1: the online trial is underpowered;
  - R2: in-sample EVSI is biased toward DEFER, reading 0.07–1.51pp when the true value is 0;
  - R3: the max-min vertex shortcut gives −0.120 against a true −0.210.
- **Empirical findings [S]:**
  - human–AI teams underperform the better of the two: Hedges' g −0.23, and −0.54 when the AI alone is better (Vaccaro);
  - persuasion gains came with accuracy losses (N = 76,977; Hackenburg);
  - transparency both disciplines a committee and chills dissent (Hansen, McMahon & Prat).
- **Model range:** 3–4pp across providers, against a Monte Carlo error of ≈0.2pp [C] (synthesis §1 finding 2; 4.2pp on the working book, SYNTHETIC). This justifies leading every probability with its model range.
- **Literature sweep (14.lit):** 16 of 16 checked citations found, 0 mismatched; 22 missed papers; 12 challenges. All of it is abstract-level evidence from labs and benchmarks, not from sovereign ICs. It transfers mechanisms, not effect sizes.

**Contradictions.**
1. **Seat count.** Dossier 14 has 9 seats, C4 has 7, the syntheses have 12. Resolved to 12 (synthesis §9.1 item 11; groups R4).
2. **AI validator.** Verify-14 R12 and the synthesis say an AI validator only flags. Groups synthesis §7.1 still has an AI Validator that "rejects any pack" lacking `priced_on`. This stays open until restated as a deterministic gate.
3. **Literature refinements missing from synthesis v1.1** (literature synthesis §3.12, §4.15; brief §7.11):
   - pre-committed contingent plans, not re-aggregation at every meeting (Garlappi);
   - authentic dissent first and objective devil's advocacy, not a rotating role-played devil's advocate (Nemeth; Schulz-Hardt);
   - one debate round, not ≤2;
   - decision accuracy as the KPI, not "≥80% surfacing" (Alsobay);
   - a retrieval audit and a second-source rule for conflicted Secondaries and Capital Solutions quotes (Kraidia).
4. **W2 latency.** Synthesis §6.4 says seconds to minutes. Synthesis §4.8 says tens of minutes on HiGHS, and no commercial solver is available (brief §3).
5. **Resolved:** the ⅔ supermajority (replaced by the symmetric protocol), confidence blending (now target shrinkage) and probability words (now ICD 203).

**Citation-audit errors.**
- Schwenk (1990) is overstated. Dialectical inquiry was not shown to beat the expert baseline on ill-structured tasks, which changes a default (literature synthesis §2.4 item 9).
- Seeded-error drills monitor automation bias; they do not prevent it (Parasuraman & Manzey; item 10).
- Carried corrections:
  - Fogliato studied 19 veterinary radiologists and reported no accuracy gain;
  - Hackenburg should be cited from *Science*;
  - Salvi's journal version has N = 900;
  - the Habermas Machine's 56% vs 44% rests on n = 439, not 5,734 (verify-14 F1).
- "Logs and code" auditing is Luo et al. (2026), summarized in the paper's related work (paper l.1976–1979). Brief P7 lists it under what the paper does.
- Dossier 14 was never edited and still carries the uncorrected text.

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | Yes | Complete, reconciled IDM with formulas, defaults and verified fixes (synthesis §6; C4 §6) |
| BUILD | Not yet | The formal core can be coded and tested (C4 §5.2, §6.4–6.10). Missing: member values θ_k, a commitment-plan formulation, the mapping from seat outputs to q_k, W2 latency, golden suites |
| IC ANSWER | No | The design and its evidence base can be presented. There is no working pack and no measured decision-quality gain, even on synthetic data |
| NEEDS ADIC DATA | Yes | Needs real IC history, the memo corpus, IC-written translation pairs, shadow-mode outcomes, permitted model families and governance choices |

## 4. Gaps

| # | Gap | Impact | Close by | Detail |
|---|---|---|---|---|
| 1 | No synthetic demonstration | High | build_experiment | Phase-0 shadow IC and pack on SYN-ADIC-177 (synthesis §10). Offline suites: hidden-profile decision accuracy, seeded errors, sycophancy and flip tests |
| 2 | Efficacy on a real IC | High | adic_data | 6–12 months of shadow mode. Track reliance split by whether the AI was right, override accuracy, dissent and anti-portfolio returns |
| 3 | Compute on HiGHS | High | build_experiment | Load: 12 seats' implied actions, 2×2 belief/value counterfactuals, Shapley (≤1,024 runs), 5-fold EVSI. Benchmark; precompute before the meeting; test Lagrangian scoring |
| 4 | Literature refinements | Medium | user_decision | Adopt each, or reject it with an ADR (brief §7.11) |
| 5 | Member values θ_k | Medium | user_decision | They drive the value split that routes items to the Board. No elicitation protocol; ownership open (dossier 14 §9 Q1; C4 §13 Q8) |
| 6 | Dynamic consistency | Medium | more_research | Formulate the committed plan. Check rectangularity before using minimax regret across periods (14.lit §4.2: recalled, not searched) |
| 7 | Seat outputs → q_k | Medium | user_decision | How LLM seat outputs become re-weightings, and whether their probabilities are ever pooled with model outputs |
| 8 | Model families | Medium | user_decision | ≥3 needed for 12 seats. In-region availability unknown (synthesis §9.3 Q11); accuracy benefit contested (Ferreira vs Zhang) |
| 9 | Golden sets and corpora | Medium | adic_data | ≥50 IC-written translation pairs; IC votes, dissents and overrides; 18-year memo corpus (C4 §5.10, §13) |
| 10 | Legal and cultural | Medium | user_decision | Legal status of AI-drafted minutes; feasibility of blind pre-votes under seniority; transcript policy |
| 11 | Validator wording | Low | user_decision | Restate groups synthesis §7.1 "rejects" as a deterministic gate |
| 12 | Unarchived checks | Low | build_experiment | `numcheck14.py` exists only in the session scratchpad. Promote it to unit tests |
| 13 | Residual literature | Low | more_research | 10 citations not re-checked in Consensus (verify-14 checked them); seed 6 (noise) not run |

**Outside the corpus (not audited).** `design/ARCHITECTURE.md` §8 appears to close gaps 4, 5, 7 and 11 in design. Its 60-second W2 figure is a target, not a measurement.
