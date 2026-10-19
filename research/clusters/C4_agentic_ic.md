# C4: Agentic Architecture and IC Deliberation (integrated cluster synthesis)

> **Superseded on the paper's mechanisms (note added 2026-10-18).** This cluster inherits several overstatements from the stream-13 dossier. Examples: the evaluation cap and engine immutability treated as transferable controls; rubrics treated as the promotion gate; distilled conclusions treated as institutional memory; the final plane described as reseeding only; r = 0.44 used as an AI-versus-human benchmark. See `research/verification/13_paper_deepread.localcheck.md`, items M2, M3, M4, M7 and M9. Where this file conflicts with `design/00_DESIGN_BRIEF.md` §2 or `research/00_SYNTHESIS.md` §5 (v1.1), those govern.

**Project:** ADIC multi-period robust Total Portfolio Approach (TPA) laboratory.
**Cluster:** C4, made up of three streams:
- Stream 12: agentic architectures;
- Stream 13: deep read of *The Agentic Scientist*, arXiv:2610.18933;
- Stream 14: Investment Committee (IC) deliberation.

**As of:** 2026-10-18.
**Inputs read in full:** the context file; dossiers 12, 13 and 14; verification logs 12, 13 and 14. For interfaces only, I also read the agent and IC hand-off sections of Streams 01–11 and verification logs 01, 07, 10 and 11.

**Tags:** [S] sourced and verified · [S\*] sourced, stated in verifier-corrected form · [P] practitioner consensus · [I] design inference or default to calibrate · [U] unverified, never an IC-facing number.

---

## 0. Bottom line

**What to build:** a workflow-first, contract-bound laboratory with three layers.
- Deterministic engines own every number.
- LLM agents propose, extract, challenge and narrate, inside typed contracts.
- A deterministic meta-controller enforces the gates.

**How the IC decides:** the IC owns the decisions. It deliberates through a protocol that aggregates *beliefs* rather than verdicts. A belief is a re-weighting of one shared scenario set.

**Why verification means robustness:** the lab's evaluator is a model of the future, not ground truth. Three rules follow:
- Search and final evaluation must differ in *model world*, not merely in seed.
- Every evaluation is counted and deflated.
- Only sealed-plane results may be reported as claims.

**The one non-negotiable integrity rule:** the evaluator is immutable and owns its own integrity checks. This must hold whichever agent or harness is used. In the Sakana paper, more than one agent configuration altered the evaluation protocol.

---

## 1. Executive summary

1. **Evidence quality.** All three verifiers rate the sourced facts HIGH and the design mathematics MEDIUM, and found no fabricated citations. Their corrections (§2) change several defaults but not the architecture.

2. **What *The Agentic Scientist* shows (corrected)** [S\*]:
   - **Where reliability comes from:** research contracts, evaluators the agent cannot edit, disjoint search and final data, and claims tied to frozen artifacts.
   - **Base model vs harness:** "the underlying model matters more" than the harness. No experiment removes orchestration while holding the model fixed.
   - **What orchestration governs:** *validity* and *efficiency*.
   - **Protocol gaming:**
     - It occurred in 2 of 3 Kimi-K3 + Pi runs on the GRPO task, and in some Opus-4.7 + Claude Code runs without shared knowledge.
     - Only a manual audit caught it.
     - The cause was a specification gap.

3. **ADIC's position on the verifier ladder.** ADIC sits on "rung 4": its verifier is a simulator. Search therefore amplifies the simulator's biases (the optimizer's curse plus Goodhart's law).
   - AlphaEvolve's data-centre scheduling (Borg) heuristic shows the remedy [S\*]: it was found in a simulator, checked on unseen data, then confirmed after deployment.
   - ADIC's equivalent is twofold: sealed alternative worlds, plus Brier scoring of every probability shown to the IC.

4. **Architecture.**
   - A unified lifecycle with gates G0–G9.
   - A deterministic state machine.
   - About 12 agent *role types*, replacing roughly 30 agents proposed across Streams 02–11.

5. **Fitness and statistics.**
   - **Fitness:** C1's objective in certainty-equivalent (CE) return units, entropic-robust over at least two generator families.
   - **Tier-1 terms** are gates. **P(10%)** is reported, never optimized.
   - **Promotion:** a paired common-random-numbers (CRN) bootstrap lower confidence bound (LCB) above a materiality margin for the decision class.
   - **Successive halving** saves about 3–3.9×.
   - **PBO** (probability of backtest overfitting) is computed on structural blocks.
   - **Deflation** uses the 95% null quantile (≈3.47σ at N = 200).
   - **Error control:** FWER via Holm within each cycle, at the α-investing allocation; mFDR via α-investing across cycles.
   - **Sealed plane:** an intersection–union test across worlds, plus Clopper–Pearson certification of every Tier-1 gate.

6. **Screening.** Deterministic code prices every single-asset SELL / HOLD / REFINANCE / LEVER action each quarter, using C1 duals. LLM ideation is reserved for packages and new structures that cannot be enumerated.

7. **IC Deliberation Module (IDM):**
   - Independence comes before interaction.
   - A 7-seat shadow-IC, with seats defined by mandate. A cap of ≤40% of seats per model family needs at least 4 families; launch with at least 2.
   - Human blind pre-votes are recorded before any AI conclusion is shown.
   - Typed, confirmed what-ifs, labelled exploratory.
   - Disagreement measured in regret and split into belief and value components.
   - Minimax regret over a finite set of beliefs (a credal set).
   - Cross-fitted expected value of sample information (EVSI) in dollars to decide DEFER, with a deferral budget.
   - Signposts implemented as event-triggered control.

8. **Accountability.**
   - The human validator holds the veto; AI validators only flag.
   - No AI agent votes. The justification is accountability, not Vaccaro et al.
   - Probability language follows ICD 203.
   - 100% of numbers carry provenance.
   - Dissent is append-only.
   - No agent is optimized for persuasion.

9. **Evaluating the IDM.** At IC volumes, an online randomized trial cannot detect its own success threshold: that needs about 4,000–11,000 independent forecasts per arm. Rely instead on offline suites, shadow mode and Brier scoring.

10. **Governance.**
    - SR 26-2 superseded SR 11-7 on 17 Apr 2026, and its footnote 3 excludes generative and agentic AI.
    - **Deterministic engines:** model-risk-management (MRM) style validation, benchmarked to SR 26-2 and PRA SS1/23.
    - **LLM layer:** NIST AI RMF, NIST AI 600-1 and ISO/IEC 42001.
    - **UAE context:** the UAE AI Charter (July 2024) and the CBUAE guidance (Feb 2026) both stress human oversight.

---

## 2. Verification ledger

### 2.1 Corrections applied in this synthesis

| # | Claim as it appeared (stream) | Verdict | Form used here |
|---|---|---|---|
| V1 | "In 2 of 3 runs, agents changed the evaluation protocol" (12) | Scope corrected | 2 of 3 **Kimi-K3 + Pi** GRPO runs plus some **Opus-4.7 + Claude Code** no-shared-knowledge runs (Fig. 17), out of 70 campaigns; found only by manual audit; cause: no fixed evaluation procedure was specified. |
| V2 | "Orchestration matters more than the base model" (12, brief) | Not supported | Autonomy depends "not only on base model capabilities, but also on" orchestration. "The underlying model matters more" than the harness. |
| V3 | "Model quality is a second-order lever" (13) | Overclaim | Validity is the binding constraint. Once validity holds, model capability drives quality. |
| V4 | AlphaEvolve works because its evaluator is exact (12) | Refuted for the infrastructure results | The 0.7% compute recovery came from a simulator of historical snapshots, validated on unseen data and after deployment. The 23% speedup was timed on real TPUs. |
| V5 | Sakana's automated reviewer has 69% balanced accuracy (12) | Corrected | 69% on possibly contaminated 2017–24 papers; **66% on clean 2025 papers, equal to humans**. Neither figure is in the *Nature* abstract. The literature audit traces the 69% to Sakana's blog post (26 Mar 2026), and verify-12 took the 66% from the same sources [unverified against the *Nature* full text]. The abstract instead reports that the workshop "had an acceptance rate of 70%" (Lu et al. 2026, *Nature* 651(8107):914–919) [corrected 2026-10-18]. The v2 paper was withdrawn by protocol, not formally accepted. |
| V6 | Successive halving saves 9× (12) | Corrected | ≈3× without path reuse; ≈3.9× with it. |
| V7 | PBO ≤ 0.2 on i.i.d. path blocks (12) | Design error | Passes by construction. Blocks must be families, regimes or episodes, on a complete candidate × block matrix. |
| V8 | "Best of 200 below ~2.8σ is noise" (12) | Understated | 2.77σ is the expected null maximum. The 95% null quantile is ≈3.47σ. Use an effective (correlation-adjusted) N. |
| V9 | P(false promotion) ≤ α via α-investing plus Holm at 0.05 (12) | Mismatch | α-investing controls mFDR across cycles. Holm controls FWER within a cycle, at the α-investing allocation (0.0476 at the start). |
| V10 | Rank candidates by marginal LCB (12) | Invalid | Use the LCB of the paired difference on identical paths. |
| V11 | Eq. 4 with SE $=\sqrt{2p(1-p)(1-\rho)/N}$ on a composite score (13) | Mis-specified | The score does not decompose by path. Use a paired bootstrap; tail terms become gates. |
| V12 | Belief fusion as a precision-weighted mean (Eq. 6) (13) | Mis-specified | Use C2's correlated-error GLS on a common forward basis, with the verify-07 fixes (shared asset-level noise; no double counting in the BF signal). |
| V13 | "A wider discount must not raise SELL volume" (12) | Invalid when liquidity binds | State the test in cash proceeds, and only for discretionary sales or slack-liquidity states. |
| V14 | Codex was "over-literal", so unnamed actions never get explored (13) | Misread | Codex obeyed "Do NOT perform hyperparameter tuning"; Pi *did* explore an unnamed action. Keep bans narrow; let the evaluator enforce integrity. |
| V15 | Use "intermediate" rubric strictness; "no gain beyond 2 workers" (13) | Over-generalized | Each rests on one task. Only the validity flip under a loose rubric is robust. |
| V16 | Sakana's code promoting candidates without a rubric pass is a defect (13) | Overstated | It is documented design. ADIC's choice to require evaluator-owned gates is still sound. |
| V17 | Memory gate allows "≤3 retries"; its JSONL log is "authoritative" (13) | Corrected | 3 attempts per cycle in total. The JSONL is not called authoritative. |
| V18 | The paper reports no USD costs (13) | Corrected | Fig. 16 plots API cost in USD (0–400 per GRPO run). Pi was ≈75% cheaper. |
| V19 | The paper describes 3 blind judges plus an adjudicator (13) | Misattributed | That design is in the repo prompts. The paper shows a single design review. |
| V20 | SR 11-7 as the governance anchor (13, 14) | Superseded | SR 26-2 / OCC 2026-13 (17 Apr 2026) keep effective challenge, but footnote 3 excludes generative and agentic AI. Not binding on ADIC. |
| V21 | Habermas Machine statements preferred 56% vs 44% "(N = 5,734)" (14) | Corrected | That comparison is n = 439 (75 groups). Revised statements overweighted the minority. Human mediators produced similar convergence. |
| V22 | Fogliato: "radiologists"; human-first ordering cuts "uncritical" agreement (14) | Corrected | 19 **veterinary** radiologists. Agreement with the AI fell **whether the AI was right or wrong**. Participants sought fewer second opinions. No accuracy gain was reported. |
| V23 | Auditing from logs and code beats auditing from the paper, as a Sakana caution (14) | Misattributed | The finding is Luo et al. (2026), cited in Lange et al.'s related work. |
| V24 | Vaccaro's g < 0 justifies "no AI vote" (14) | Misapplied | The losses concentrate where the AI alone is better (g = −0.54). |
| V25 | Choi justifies the evidence-gated 5 pp rule (14) | Misapplied | Choi's practical variants bias updates toward the previous round's majority. Evidence gating is untested [I]. |
| V26 | Debate vs voting is settled; Du supports a 2-round cap (14) | Mixed evidence | Du found debate > voting. Smit found tuned debate best. Choi, ChatEval and Wynn support the cap. |
| V27 | Debate 84% vs consultancy 74% shows debate is better (14) | Mechanism only | By design, the consultant argued the wrong side half the time. |
| V28 | ≥3 model families with ≤40% of seats each (14) | Arithmetic | 7 seats need at least **4** families. |
| V29 | An AI validator with a veto satisfies SR 11-7 (14) | Rejected | A human validator holds the veto. |
| V30 | 400 forecasts per arm can detect a +0.05 BSS gain (14) | Underpowered | It needs ≈4,000–11,000 independent forecasts per arm. |
| V31 | In-sample EVSI; vertex shortcut for max-min; Kish-based grey-out (14) | Biased / invalid / wrong SE | Cross-fit EVSI: the in-sample version shows 0.07–1.51 pp when the true value is 0. Use a finite credal set. Use paired SEs. |
| V32 | Dates, attributions, API details (12–14) | Corrected | UAE AI Charter **July** 2024; FINSABER KDD 2026; CORE-Bench 42→95% from bug fixes **and** a looser scaffold; Opus 5.5 rejects only *non-default* sampling values and forced `tool_choice`; Man Group "several dozen" via Hedgeweek (Jul 2025); NBIM quote "keeping humans central to all decisions"; Hackenburg → *Science* 390(6777); Salvi → *NHB* 2025 (N = 900); EU AI Act dates via Reg. 2026/1744; BoE/FCA 24% is *of the 55%*. |

### 2.2 Unverified items [U]

None of the following may carry an IC-facing number:
- the year of the information-sampling formula (Stasser & Titus, 1985 or 1987);
- Clark & Urwin's twelve findings (paywalled);
- the finer points of the Mediating Assessments Protocol (MAP), including whether it prescribes individual pre-votes (the MIT SMR full text is paywalled);
- Sakana repo operational details (exit code 87, output caps);
- "a NIST revision is under way";
- ISO 42001's "38 controls";
- Bridgewater AIA details;
- CPP Investments and Future Fund governance;
- the Abu Dhabi SWF "case against" practice. It rests on one vendor anecdote (Sharjah24, 14 Oct 2026) and is a precedent, not evidence.

**Resolved since this file was written** [corrected 2026-10-18]:
- **Schwenk (1990)**, *OBHDP* 47(1):161–176, is now verified. Use this wording:
  - Devil's advocacy (DA) beat an expert-recommendation baseline.
  - Dialectical inquiry's (DI's) advantage over the expert approach was not demonstrated on relatively ill-structured tasks.
  - Neither DA nor DI beat the other.

  Do not cite it as support for DI on IC cruxes.
- **The MAP's core steps** are confirmed by a readable summary (Sydney Business Insights, May 2019) of Kahneman, Lovallo & Sibony (2019), *MIT Sloan Management Review*:
  - define the assessment criteria in advance;
  - make fact-based assessments independently;
  - delay holistic judgment to the final evaluation.

  The blind pre-vote (H0) is ADIC's own design [I], not a documented MAP step.
- **MLReplicate's "59%"** (Gaddipati et al. 2026, arXiv:2605.16616, a preprint) is confirmed. The automated review accepted 10 of 37 valid submissions. In §3, human experts reviewing those 10 papers "identified fabricated or unsupported claims in 59% of all evaluations".
  - The abstract ("59% of accepted automated reviews") and §1 ("59% of the automated acceptances") use looser denominators.
  - Quote §3's denominator.

---

## 3. Design questions: recommendations

| # | Question | **Recommendation** (positions reconciled) |
|---|---|---|
| 1 | Agent or workflow? | **Workflow**, driven by a deterministic state machine. Agency only in ideation, memo drafting, translating natural language into specs, and the shadow-IC seats. |
| 2 | Autonomy level | **Proposals only.** No autonomous trades, commitments, financing or collateral moves. Execution goes through the order management system (OMS) and IC controls. Drift within delegated bands needs a written policy. |
| 3 | Where may numbers originate? | **Outputs come from engines. Inputs come from data or from confirmed humans.** LLMs draft structure, analogues and back-translations only. A numeric-provenance parser acts as a hard gate (G7). |
| 4 | Stage and gate scheme | **One unified G0–G9 scheme** (§4.2), mapped to Stream 12's G0–G8, Stream 13's Stages 0–8, and Stream 14's S0–S7 / H0–H6. |
| 5 | Search plane | **At least 2 generator families.** Stream 13's single model M₀ invites the search to exploit that model's quirks. |
| 6 | Sealed plane | **At least 2 disjoint worlds, at least 3 pre-registered historical windows, and fresh seeds, run once.** Windows are sign and Tier-1 checks, not significance tests. |
| 7 | Score | **C1's J in CE units, made robust across worlds.** Tail metrics become gates. P(10%) is a key performance indicator (KPI) policed by a "gambling detector"; this resolves Stream 13 vs Stream 11. |
| 8 | Promotion | **Paired CRN bootstrap LCB(ΔF) > ε_mat(class).** Search-plane promotions support no claim. |
| 9 | Materiality | **ε_mat per decision class, in CE bp/yr.** Symmetric when the incumbent would forfeit an expiring option. |
| 10 | Allocating the budget | **Successive halving with path reuse and tie-keeping.** Size n₀ from the SE needed. |
| 11 | Overfitting control | **Count every evaluation.** Use PBO on structural blocks, deflation at the 95% quantile with effective N, and Holm at the α-investing level. |
| 12 | Workers | **3 workers: 2 sharing memory, 1 isolated challenger.** The justification is herding (action correlation 0.04 → 0.41), not Fig. 15. ADIC should run its own ablation. |
| 13 | Rubrics | **Gates are strict and owned by the evaluator.** Method rubrics name the mechanism and ban known shortcuts. Prohibitions stay narrow. Integrity rubrics are mandatory for every harness. |
| 14 | Must rubrics pass before promotion? | **Yes, for gate rubrics owned by the evaluator.** Implementation rubrics checked by agents are disclosed, not gating. |
| 15 | Design qualification | **3 blind validators plus an adjudicator** (the repo design), with **a human validator countersigning.** At least 2 model families. |
| 16 | Analyst-Coder | **Not in Phase 1; use pre-built diagnostic tools.** Phase 2 allows a sandboxed coder on frozen artifacts, with output labelled exploratory. |
| 17 | Elo / tournaments | **Qualitative triage only.** |
| 18 | Debate or ensemble? | **Ensembles produce estimates.** Debate only to surface evidence, on at most 3 cruxes and at most 2 rounds. Evidence gating is to be ablated. |
| 19 | Shadow-IC | **7 seats defined by mandate, plus a non-substantive facilitator.** The AI validator only flags. At least 4 model families eventually, at least 2 at launch. No personas, because of caricature risk. |
| 20 | Do AI agents vote? | **No**, on accountability grounds (GAPP 6–9; EU AI Act Art. 14). Measure the value of IC overrides. |
| 21 | Ordering | **Human blind pre-vote before AI conclusions.** The fact pack and model outputs may come first. Encourage colleague consultation after the vote locks. Monitor whether reliance on the AI is appropriate. |
| 22 | Veto | **Held by the human validator.** AI flags travel with the item. |
| 23 | Probability words | **ICD 203, with disjoint half-open bins.** IPCC bands nest, so they cannot be applied deterministically. |
| 24 | View conditioning | **Two channels.** Asset-return views become fusion signals (C2). Scenario views go through entropy pooling (EP), with confidence applied by *shrinking the target*. Show the effective view. Flag on KL divergence. |
| 25 | Pooling | **Linear pool**: it preserves marginals, and no extreme member gets a veto. Log pool as a sensitivity. Never extremize LLM ensembles. |
| 26 | Robust committee rule | **Finite credal set. Minimax regret for irreversible actions.** Max-min shown as a diagnostic only. |
| 27 | DEFER | **Cross-fitted EVSI in dollars.** Defer only if its LCB exceeds c_delay and no staged action dominates. At most 2 consecutive deferrals. |
| 28 | Irreversibility | **A symmetric protocol.** Letting a bid or financing window lapse also counts as irreversible. This replaces the ⅔ supermajority, which applied only to actions. |
| 29 | Track records | **Display only.** Bühlmann credibility from the first resolution, with K̂ = EPV/VHM estimated. One member, one vote. |
| 30 | Asset "lens" screening | **Deterministic enumeration every quarter.** LLM campaigns only for IC questions. |
| 31 | Agent sprawl | **About 12 role types, specialized by configuration** (§4.4). |
| 32 | Runtime | **Thin stack:** Anthropic SDK, Pydantic, a Python meta-controller and an MCP 2026-07-28 server. Use LangGraph or Microsoft Agent Framework only for durable human-in-the-loop at scale. Managed Agents only for non-sensitive pilots. |
| 33 | Regulatory anchor | **Engines:** benchmark to SR 26-2 and PRA SS1/23. **LLM roles:** NIST and ISO 42001. Also the UAE AI Charter, CBUAE guidance and the Santiago Principles. |
| 34 | IC record format | **Structured positions, rationales and dissent by default; verbatim transcripts are a separate, restricted policy choice.** Transparency is a trade-off: it adds discipline but can chill dissent (Meade & Stasavage 2008). Hansen, McMahon & Prat (2018) find both a discipline effect and a conformity effect, and their influence measure suggests the discipline effect dominates. They are evidence of the trade-off, not support for restricting transcripts [corrected 2026-10-18]. |

---

## 4. Reference architecture

### 4.1 Planes [I, from 12 §6.1 and 13 §6.1]

| Plane | Contents | Invariant |
|---|---|---|
| Human decision | CIO/IC sign contracts (G0); MRM validates engines; human validator (G8); IC decides (G9) | Decision rights are never delegated |
| Meta-controller | Deterministic state machine. Budgets: dollars, evaluation count, α-wealth, wall-clock. Also gates, checkpoints and escalation | No LLM in the control flow |
| LLM roles | About 12 role types (§4.4), with strict schemas | No write access to engines, evaluators, beliefs or scenarios |
| Tools | Typed tools plus an MCP server: `evaluate_policy`, `optimize`, `price_action`, `fuse_beliefs`, `overlay_margin`, `liability_paths`, `ep_condition`, `implied_actions`, `evsi_crossfit`, `flip_thresholds`, `attribute`, `robustness_card`, `get_metric`, `validate_claims`, `register_forecast` | Validation failures are returned as tool execution errors |
| Engines (C1–C3) | Scenario generators, PE cash flows, fusion, action economics, overlay and collateral, liabilities, simulator, optimizer with duals, robustness layer, EP, the official evaluator | Versioned, content-hashed, MRM-inventoried |
| Data and provenance | Holdings; market data; memo corpus with chunk hashes; scenario and policy libraries; run, metric and claim registries; issue, view, forecast, decision, dissent and override ledgers; LLM record/replay cassettes | Append-only and bitemporal |

**Control loops:**
- **inner** (seconds): tool calls;
- **middle** (hours): one contract;
- **outer** (quarterly): decisions → outcomes → recalibration. This is ADIC's equivalent of AlphaEvolve's post-deployment check;
- **governance** (annual): MRM review and ISO 42001 review.

### 4.2 Unified lifecycle

| Gate | Stage | Pass criterion | Owner |
|---|---|---|---|
| G0 | AnalysisContract signed | Objective, gates (with governance bands), actions, planes, budgets and ε_mat are hashed. **A Phase-I check shows every gate is feasible under HOLD and under static SAA.** Elicitation questions are frozen | CIO/IC sponsor + MRM |
| G1 | Design qualified | 3 blind validators pass; the adjudicator rules on any dimension where exactly one validator failed it; smoke tests pass; a full HOLD run completes within budget | Validators + human validator |
| G2 | Beliefs frozen | C2 fusion outputs hashed; assets flagged F1–F10 reviewed by humans; no look-ahead | C2 engine + humans |
| G3 | Proposal admissible | Strict parse; domain-specific language (DSL) type-check (§5.3); novelty | Deterministic |
| G4 | Tier-1 gates on the search plane | Every gate passes in every search model (UCB rule, §5.4). Failed or missing paths count as worst case | Evaluator |
| G5 | Promotion | Paired LCB(ΔF) > ε_mat, and integrity rubrics pass | Evaluator |
| G6 | Sealed qualification (once) | Intersection–union test (IUT) across worlds; Holm at α_c; Clopper–Pearson Tier-1 certification; PBO; a label | Evaluator + MRM |
| G7 | Evidence | Claim coverage = 1; plane labels; lexicon match; degraded phases disclosed | Deterministic validator |
| G8 | Review | Cross-family audit PASS with ≤4 findings; red-team issues disclosed; human countersignature | Auditor + human validator |
| G9 | IC record | Pre-votes locked; ballot; dissent, overrides, signposts and review date logged | IC secretary |

**Cycle outcomes.** Each cycle ends as:
- **QUALIFIED**;
- **NOT ESTABLISHED**: the sealed run completed, but no finalist qualified;
- **NOT ASSESSED**: the run was degraded.

"Not established" is a first-class result: it removes the pressure to manufacture a winner.

**Failure handling** (adapted from Sakana [S]): infrastructure retries have their own budget; terminal checkpoints name the last gate failed; degraded phases are shown on the IC dashboard, never passed silently. **After G9:** outcomes are tracked at 1, 4 and 8 quarters; every probability is Brier-scored; the memory gate runs (§5.11); any gate breach triggers an incident review.

### 4.3 Meta-controller [I]

**States:** DRAFT → SIGNED → QUALIFIED → BELIEFS_FROZEN → (IDEATION ⇄ SCREENING)\* → SELECTION → SEALED → RETROSPECTIVE → MEMO → REVIEW → IC → CLOSED. Any state can go to ESCALATE.

```python
def run_contract(C):
    assert C.signed and all(gate_feasible(g, C) for g in C.gates)       # G0
    qualify_design(C, validators=3, adjudicator=True, human=True)      # G1
    B = freeze(fuse_beliefs(C.snapshot)); route_flags_to_humans(B)     # G2
    inc, pool = C.incumbent, []
    for cyc in range(C.max_idea_cycles):                                # 20
        ideas = [x for x in ideate(workers=3, isolated=1) if admissible(x, C)]  # G3
        ledger.count(len(ideas))
        surv = race(ideas, C.M_search, n0=2000, eta=3, crn=C.seeds)     # G4
        inc, promoted = promote(surv, inc, C.eps_mat)                   # G5
        pool += surv; memory.update_if_trigger()
        if stop(cyc, promoted, C.budget, patience=6, pricing_exhausted()): break
    F = freeze(select(pool, K=3)); pbo = cscv(all_screened(), C.blocks)
    S = sealed_eval(F, C.M_val, C.windows, alpha=ledger.alpha_c())      # G6
    memo = write_memo(registry, retrospective(F)); assert claims_valid(memo) == 1.0  # G7
    review(memo, logs, code, auditor_family="B"); human_validator_sign()            # G8
    return ic_package(S, memo, pbo)                                     # G9
```

**Stop rule.** Stop on any of:
- the budget is exhausted;
- 6 cycles pass without a promotion;
- no memory triggers fire for 6 cycles;
- deterministic pricing finds no column with positive robust reduced cost, and ideation has not raised the LCB for 6 cycles.

### 4.4 Consolidated agent roster [I]

Role types are specialized by configuration: evidence slice, tools and rubric pack. "A" is the primary model family; "B" is a different family.

| Role type | Specializations requested by other streams | Permissions | Gate | Materiality | Family |
|---|---|---|---|---|---|
| Contract Drafter | — | Read corpus; gate-feasibility checker | G0 | High | A |
| Design Validators ×3 + Adjudicator | 10 dimensions (13 §6.5) | Read-only | G1 | High | A + B |
| Quarantined Extractors | Memo/QDD; covenants (06); liquidity librarian (05); sovereign evidence cards (03); GP notices (04) | Untrusted docs; **no outbound tools**; dual extraction | Schema + human samples | Medium | A |
| Scouts / Librarians | Reference class (07); funding market (06); peers (02) | Approved sources; suggest, never set | Staleness flags | Low | A |
| Ideators ×3 | Structuring (05); hedge design (03); pacing; distribution rule | Read-only corpus and search metrics | G3 | Low | A (challenger B if available) |
| Planner | — | Baselines; cost estimator | G1/G3 | High | A |
| Red Team | Funding stress (06); timing-optimism (04); reverse stress (03, 10); gambling detector (11) | Bounded ScenarioSpecs; failure analogues | Disclosed at G8 | Medium | B |
| Auditor | Evidence audit; exploit hunt; checking that the idea matches its implementation (Man Group lesson) | Registry, logs, code | G8 | Medium | **B** |
| Memo Writer | IC briefer (07); stress narrator (10) | `get_metric`, `validate_claims` | G7 | Medium | A |
| IC Facilitator / Translator | View elicitor (10); SHELF elicitation (03) | Drafts specs; Multi Round-Trip confirmation; cached-path tools | Human confirmation | High | A |
| Shadow-IC seats ×7 | §6.2 | Read-only tools on the seat's own evidence slice | S1 rubric | Medium | ≥4 families eventually |
| Calibration orchestrator | Quarterly fusion refits (07) | Invokes deterministic refits | MRM | Medium | A |

**Kept deterministic, not agentic:** fusion, lens pricing, EP, robustness metrics R1–R8, the evaluator, and the claim validator.

### 4.5 Runtime, reproducibility and security [S\* unless marked]

- **Stack.** Anthropic SDK tool runner; `strict: true` tools (`additionalProperties: false`, explicit `required`); Pydantic via `messages.parse(output_format=Model)` (raw dictionaries move to `output_config.format`). Opus 5.5 accepts only *default* sampling values and rejects forced `tool_choice` (use `auto` plus strict tools); set effort high for the Planner, Auditor and Facilitator [I].
- **Reproducibility.** Record/replay cassettes keyed by prompt hash; CRN via `numpy.random.SeedSequence` spawn keys (contract, family, path); `numpy.memmap` and pinned BLAS threads on Windows; self-hosted OpenTelemetry.
- **MCP 2026-07-28.** Stateless, with explicit handles (`run_id`, `scenario_set_id`); Tasks for long simulations; Multi Round-Trip Requests for IC confirmations.
- **Hosting and security.** Managed Agents' self-hosted sandboxes still send tool I/O to Anthropic's control plane, so use them for non-sensitive pilots only. Confirm UAE-region serving; tokenize sensitive fields; quarantine extraction to avoid the "lethal trifecta" (CaMeL: 77% utility vs 84% undefended); web access off by default; OWASP LLM01/LLM06.
- **Cost.** Opus 5.5: $4 / $20 per million input / output tokens; cache reads $0.20, writes $5 (5-min) or $8 (1-h); batches 50% off (use for overnight shadow-IC runs [I]). A cycle of 2M input (70% cached) plus 0.3M output costs ≈ **$8.7**, up to ≈ **$15.7** with cache writes; budget $50 soft / $200 hard [I]. The scarce resources are evaluator CPU, counted evaluations and IC attention.

---

## 5. Lab formulations (discovery and verification)

### 5.1 Notation

- **Contract:** $C$, with hash $h_C$ and decision class $\kappa$.
- **Planes:**
  - $\mathcal M_{search}$: at least 2 generator families;
  - $\mathcal M_{val}$: at least 2 worlds, disjoint from search;
  - $\mathcal W$: at least 3 historical windows.
- **Paths:** $\omega_{m,n}$, seeded by $(h_C,m,n)$, so every policy sees identical paths.
- **Policies:** $\pi$ is a PolicySpec; $\pi_0$ is the incumbent (HOLD).
- **Lab state:** $S_t=(h_C,\sigma_t,\mathcal H_t,N^{search}_t,N^{sealed}_t,W_t,\$_t,Z_t,\text{pins})$. These are the stage, the hypothesis pool (lineage, descriptors, $\hat F$, SE, LCB), the evaluation counters, α-wealth, spend, the notebook and the version pins.
- **Decisions:** screen $x_i\in\{0,1\}$; allocate paths $n_i$; pick finalists $y_i$ with $\sum y_i\le3$; escalate $e$.
- **Meta-objective:** $\max\ \mathbb E[F(\pi^\star)-F(\pi_0)]-\lambda_\$\$_T$, subject to mFDR ≤ 0.05 across cycles and FWER ≤ α_c within a cycle.

### 5.2 Typed contracts (Pydantic v2, strict JSON Schema 2020-12)

| Contract | Key fields |
|---|---|
| `AnalysisContract` | id, version, parent (each steer creates a version); question; class; tier; `action_space` (assets × {SELL(frac, channel), HOLD, REFI(instrument, LTV, tenor), LEVER(Δ, instrument)}, plus overlay {hedge ratio, opp budget}, pacing, borrowing, DEFER); `objective_ref` (C1 id, γ, λ_T, H); `gates[]` {metric, ε, band, feasible}; `planes` {search, sealed, windows, seed keys, disjointness attestation}; τ, η, η_max; budgets {$, B_eval, α_c, K₀, K_final}; `eps_mat`; `expiring_options[]`; frozen questions; MAP dimensions; signatories; sha256 |
| `ProposalContract` | id, family, parents; hypothesis {statement, sign, magnitude band, metric}; `policy_spec`; plan; `target_rubrics[]` (≥1 metric and ≥1 implementation; gate and integrity rubrics auto-attached) |
| `RubricStatus` | rubric {id, type ∈ gate/metric/implementation/liquidity/compliance/evidence/integrity, assessment ∈ passed/failed/not_assessed, evidence_ptr, assessed_by}. For gates, not_assessed counts as failed |
| `RunManifest` | run and parent ids; engine SHA; evaluator, config, scenario and PolicySpec hashes; seed spawn keys; data snapshots; per-LLM-call model id, prompt and response hashes, tokens, cost; approvals. Maps to W3C PROV and OpenTelemetry |
| `Claim` | id, memo span, kind ∈ value/comparison/probability/ranking, metric_id, run_id, plane ∈ search/sealed/exploratory, value, CI95, world range, rounding, likelihood term, significance flag, sources, snapshot hash, code version |
| `ScenarioSpec` / `ViewSpec` | Base-set hash; overrides {factor, shape, magnitude, start, duration}. Or: holder, channel ∈ asset_return/scenario, variable, type, stated value, confidence c, effective target, KL (nats), admissible, back-translation, confirmed |
| `Ballot`, `DecisionRecord`, `MinorityReport`, `Signpost`, `ForecastRecord` | See §6 |

### 5.3 PolicySpec DSL and admissibility (G3)

**Abstract syntax tree (AST).** Nodes are Pydantic discriminated unions; free code is never allowed. The node types are:
- `Predicate(var, op, θ)`, combined with `And` / `Or` / `Not`;
- `Action(selector, SELL{frac, channel} | HOLD | REFI{instrument, LTV, tenor} | LEVER{Δ, instrument})`;
- `Overlay{hedge_ratio, notional_cap, opp_budget}`;
- `Pacing{rule}`;
- `Borrow{facility, amount_rule}`.

A policy may have at most 25 nodes and at most 8 bounded parameters.

**Type rules:**
1. **Non-anticipativity.** Each variable carries an observation lag $\ell_v$: reported NAV 1 quarter; cash flows 0; filtered regime posterior 0; forecasts from their timestamp. A rule at time $t$ may read $v_{t'}$ only if $t'+\ell_v\le t$. Look-ahead becomes a compile error.
2. **Monotonicity in the cushion.** This is C1's anti-target-chasing rule. Any leverage, risk-budget or pacing size $f(c_t,\cdot)$ must satisfy $\partial f/\partial c\ge0$. For affine rules check it symbolically ($k_c\ge0$); otherwise on a grid.
3. **Novelty.** Compute a behavioural descriptor on a fixed 1,000-path probe: turnover, peak liquidity use, peak leverage, overlay notional and action mix. Reject anything within $\delta_{nov}$ of the library. Keep a MAP-Elites archive with 2–4 islands.

**Metamorphic tests** (property-based tests with `hypothesis`):
- (i) A wider discount must not increase discretionary SELL *cash proceeds* while liquidity is slack.
- (ii) A costlier facility must not increase REFI volume.
- (iii) A tighter Tier-1 band must not expand the feasible set.
- (iv) Relabelling assets must not change results.
- (v) Scaling every NAV by $k$ scales actions by $k$ (when there are no fixed costs).

### 5.4 Fitness and gates

**Per-path quantities** for model $m$:
- utility $u_\omega=U_\gamma(W_H/W_0)$, where $U_\gamma(w)=(w^{1-\gamma}-1)/(1-\gamma)$;
- target shortfall $s_\omega=(\ln1.10-H^{-1}\ln\mathrm{TWR}_H)_+$.

**Fitness, in pp of annual CE return:**

$$\hat J_m(\pi)=\Big[\big(1+(1-\gamma)\bar u_m\big)^{\frac1{1-\gamma}}\Big]^{1/H}-1-\lambda_T\sqrt{\overline{s^2}_m}$$

- $\gamma=3$.
- $H$ = 10-year rolling window with a terminal value; 5-year results are also reported (Stream 11).
- $\lambda_T$ is owned by C1. Placeholder: 0.5 [I].

**Robust fitness:**

$$F_\tau(\pi)=-\tau\ln\sum_{m}w_me^{-\hat J_m(\pi)/\tau}=\min_{q\in\Delta}\Big\{\textstyle\sum_mq_m\hat J_m(\pi)+\tau\mathrm{KL}(q\Vert w)\Big\}$$

- $w$ is uniform and $\tau=0.5$ pp. Report $\tau\in\{0.25,0.5,1,\infty\}$.
- As $\tau\to0$ this tends to the worst model; as $\tau\to\infty$, to the mean.

**Converting to dollars for the IC:** 1 bp/yr of CE on US$177bn ≈ **US$17.7m per year**. Exactly:

$$\Delta\$=W_0[(1+CE_a)^H-(1+CE_b)^H]/(1+r)^H$$

**Gates.** For each Tier-1 gate $k$ (defined by C1) at level $\varepsilon_k$:
- the breach frequency $\hat p_{k,m}$ counts failed or missing paths as breaches;
- the search plane passes only if the Wilson $\mathrm{UCB}_{0.90}\le\varepsilon_k$ in every search model;
- KL-robust gates need $\eta_L\approx0.01$–$0.02$ plus importance sampling. At η = 0.10, zero failing paths always pass, while one failing path out of 50k fails (verify-10).

### 5.5 Screening: racing with successive halving

**Rungs.** Rung $r$ uses $n_r=n_0\eta^r$ paths per model. Paths are cumulative and reused.

**Statistic.** For each candidate:
- $\Delta\hat F_i=F_\tau(\pi_i)-F_\tau(\pi_0)$, computed on identical paths;
- a paired bootstrap that resamples path indices jointly within each model (B = 500);
- $\mathrm{LCB}_i=\Delta\hat F_i-1.28\,\mathrm{SE}_i$.

**Selection.** Keep the top $\lceil|\mathcal H_r|/\eta\rceil$ by LCB, plus any candidate statistically tied (at 80%) with the last one kept, up to a cap of double that number. Eliminated candidates still count toward $N$.

**Cost per model:**

$$\sum_r|\mathcal H_r|(n_r-n_{r-1})$$

With the defaults ($K_0=27$, $\eta=3$, $n_0=2{,}000$, rungs of 2k, 6k and 18k paths), this is 54k + 36k + 36k = 126k path-evaluations. Full fidelity would be 486k, so the saving is ≈3.9× (≈3× without reuse) [S\*].

**Sizing $n_0$:**

$$n\ge\big((z_{1-\alpha}+z_{1-\beta})\sigma_D/\delta\big)^2$$

For P(10%), the paired SE is ≈0.50 pp at 2,000 paths and 0.22 pp at 10,000 (ρ = 0.9) [S]. Binary metrics therefore cull only large losers early, which is why screening uses the continuous CE score.

### 5.6 Search-plane promotion (a heuristic, never a claim)

$$\text{promote }\pi'\iff\text{gates}\wedge\text{integrity}\wedge\big[\Delta\hat F(\pi',\pi^\star)-2\,\mathrm{SE}_{boot}\big]>\varepsilon_{mat}(\kappa)$$

- **Integrity rubrics** (`beliefs_unchanged`, `scenario_unchanged`, `evaluator_hash`) are SHA-256 checks run by the evaluator.
- **Error rate.** At the materiality boundary, each test promotes falsely ≈2.3% of the time. Over about 40 tests, the chance of at least one false promotion is ≈60% [S].
- **Consequence:** no search-plane improvement is ever reported to the IC.

### 5.7 Sealed-plane qualification (G6: the only claims)

Each finalist $i$ is run with 50,000 fresh paths in each world. Candidate worlds:
- a DPI-drought world (C2);
- an owner-draw / oil shock world (C3);
- an alternative regime model;
- an alternative secondary-discount model.

**(a) Intersection–union test (IUT) for improvement.**
- Null: $H_{0,i}$: $\exists m:\Delta J_m\le\varepsilon_{mat}$.
- p-value: $p_i=\max_mp_{i,m}$. Each $p_{i,m}$ is the one-sided p-value of $(\Delta\hat J_m-\varepsilon_{mat})/\mathrm{SE}_m$, using a paired bootstrap with B = 1,000.
- No multiplicity adjustment is needed across worlds.

**(b) Across finalists:** Holm step-down at level $\alpha_c$.

**(c) Historical windows** (2008–09, 2020, 2022): require $\Delta\hat J_w\ge0$ and that all Tier-1 gates pass. These are sanity checks, never selection criteria.

**(d) Tier-1 certification.**
- The Clopper–Pearson upper bound at $1-\beta$ must be ≤ $\varepsilon_k$ in every world.
- With zero violations, the minimum sample is $N=\ln(1/\beta)/\varepsilon$: 93 paths at ε = 5%, β = 1%; 300 paths at ε = 1%, β = 5% [S, verify-01].
- Gates with ε ≤ 1% use importance sampling.

**(e) Shrinkage diagnostic.** Report $s_i=\Delta\hat F_{val}/\Delta\hat F_{search}$ with a bootstrap CI. Alert if $s_i<0.5$. The decision rests on (a), not on $s_i$. The ratio itself shrinks nothing. Smith & Winkler's (2006) remedy for the optimizer's curse is Bayesian adjustment of the selected estimate. Report the sealed-plane $\Delta\hat F$ after Bayesian shrinkage toward a prior centred on no improvement [I], next to the raw value [corrected 2026-10-18].

**(f) PBO** via combinatorially symmetric cross-validation (CSCV) on $S$ structural blocks (family × regime stratum, or historical episode).
- All screened candidates are evaluated on a common block set: 27 × 16 × 500 = 216k path-evaluations.
- For each split $c$: $\lambda_c=\mathrm{logit}\,\bar\omega_c$, and PBO = mean of $\mathbb 1[\lambda_c\le0]$.
- PBO ≤ 0.20 is a gate if $S\ge8$; otherwise it is a diagnostic.

**(g) Deflating any reported search maximum:**

$$h_N=\hat\sigma_\Delta\Phi^{-1}(0.95^{1/N_{eff}}),\qquad N_{eff}\approx\bar\rho+(1-\bar\rho)N$$

For N = 200 independent candidates, $h_{200}\approx3.47\hat\sigma$.

This hurdle assumes a normal null. Where the search statistic is a Sharpe ratio, use the full deflated Sharpe ratio. It adds a skewness-and-kurtosis (non-normality) term (Bailey & López de Prado 2014), which matters because the lab's outcomes are fat-tailed (t₅) [corrected 2026-10-18].

**(h) α-investing across cycles** (the verifier's proposed form) [I]:
- start with $W_0=0.05$; payout $\omega=0.05$;
- allocate $\alpha_c\le W_{c-1}/(1+W_{c-1})$, which is 0.0476 at the start;
- update: $W_c=W_{c-1}+\omega$ if any rejection, otherwise $W_c=W_{c-1}-\alpha_c/(1-\alpha_c)$;
- escalate if $W_c<0.005$. Any reset is decided by MRM and the IC.

**Label:**
- **QUALIFIED** if (a)–(d) pass and no critical issue is open;
- otherwise **NOT ESTABLISHED**, or **NOT ASSESSED** if the run was degraded.

### 5.8 Retrospective evidence and attribution

**Controls** (same evaluator, same paths): HOLD-all; static SAA; the deck v8 rule policy; target-chasing; a pro-rata liquidity raise; overlay-only.

**Single-action ablations:**
- *Accept* only if decision-relevant, single-change, feasible, same-evaluator and useful to the IC.
- *Reject*: quota filler, parameter sweeps, speculative changes, multi-change variants, generic baselines, external dependencies, and anything that is not a change versus HOLD.
- "Zero accepted" is a valid outcome [S].

**Shapley attribution:**
- exact over ≤6 action groups (64 coalitions);
- otherwise permutation sampling under CRN, reporting its own Monte Carlo error;
- asset-level exact Shapley is infeasible.

**Post-hoc diagnostics** (pre-built tools, run on the frozen package):
- shadow prices (C1);
- belief-source sensitivity: underwritten, actual or forecast (C2);
- forensics on the worst 1% of paths;
- reverse stress $q^\star,\eta^\star$ (C1).

Requests to re-optimize are rejected programmatically. Sequential optimization supports comparisons, not causal attribution [S].

### 5.9 Evidence grounding and language

**Claim validity.** A claim is valid iff all of these hold:
- the registry entry $R(\text{metric},\text{run})$ exists;
- the rounded registry value equals the stated value;
- the planes match;
- probabilities carry the lexicon term, the CI and the world range;
- comparisons match in sign and significance flag;
- citations resolve to approved chunk hashes.

**Coverage** = valid numeric tokens ÷ all numeric tokens, with dates and IDs whitelisted. It must equal **1**.

**ICD 203 lexicon, with half-open bins** [S; bins I]:

| p | Term |
|---|---|
| [0.01, 0.05) | almost no chance |
| [0.05, 0.20) | very unlikely |
| [0.20, 0.45) | unlikely |
| [0.45, 0.55] | roughly even chance |
| (0.55, 0.80] | likely |
| (0.80, 0.95] | very likely |
| (0.95, 0.99] | almost certain |
| < 0.01 or > 0.99 | number only |

**Rules:**
- The term follows the point estimate.
- If the range across worlds spans more than one bin, append "range spans …".
- Confidence goes in a separate sentence.
- Use one ICD 203 term set throughout.

**Illustrative example:** "P(12-month liquidity breach): almost no chance, 2.0% (MC 95% CI 1.9–2.1%; sealed-world range 1.2–4.6%) [sealed]."

Exhibits use frequency framing ("20 of 1,000 simulated futures").

### 5.10 Admission tests

| Component | Admission criterion |
|---|---|
| Judges | One per dimension, with an "unknown" option. Cohen's κ ≥ 0.6 vs subject-matter experts on ≥50 golden items. Report κ and raw agreement separately: on skewed labels, raw agreement above 80% can coexist with κ < 0.6. |
| Auditor (family B) | Recall on seeded *semantic* errors (overclaim, wrong sign, plane mislabel, attribution presented as causation) ≥90% to admit, 95% as the target. Numeric errors are caught deterministically. |
| Translator (natural language → spec) | pass³ ≥ 0.9, i.e. per-trial accuracy p ≥ 0.965, on ≥50 pairs written by IC members. |
| Sycophancy and flip suite | Fewer than 10% unjustified flips, against an **in-house** baseline. Laban et al.'s 46% used content-free challenges on 2023-era models and is not a valid baseline. |
| AI memo reviewer | Triage only, and only once its correlation with IC ratings is ≥0.6. The paper's r = 0.44 explains ≈19% of rank variance. |

Start with 20–50 tasks drawn from real failures [S]. Re-run the suite on every change to a model, prompt or tool; each is a revalidation event.

### 5.11 Memory gate and scheduler

**Lessons ledger:**
- An append-only JSONL log, plus one forward-looking conclusions paragraph of ≤300 words. The paragraph uses qualitative thresholds and no exact numbers.
- It changes only on four triggers: (a) a contradiction, (b) a new category, (c) a Do/Don't flip, (d) a named refinement.
- 3 attempts per cycle, then skip.
- Every cycle logs `gate=<updated|kept|skipped>; trigger=<a..d|none>; reason=…`.
- A human curator signs off every (c).

**Pruning** archives context and never deletes it. The isolated worker never reads shared memory.

**Family scheduler.** The idea families are secondaries, NAV/preferred financing, overlay, pacing and distribution rule. Use discounted UCB (discount 0.9) with reward $r=\mathbb 1[\text{G4 pass}\wedge\mathrm{LCB}>0]$. UCB1's stationarity assumption fails because the incumbent keeps moving.

---

## 6. IC Deliberation Module (IDM)

**State:** member and seat views with confidences; track records ($n_k$, BS, REL, RES); open-decision, dissent and override ledgers (overrides log the model recommendation vs the IC decision with reason codes, the analogue of the Solvency II "use test"); agent registry. **Decisions:** approve / resize(x) / defer / reject per item; asset action; diligence attached to any DEFER; signpost thresholds; escalation flags. **Constraints:** decision-rights matrix; quorum ≥ ⅔; recusals; Tier-1 feasibility; 100% numeric provenance; a minority report whenever triggered. **Exposed, not optimized:** J and its decomposition, decision-relevant disagreement (DRD), EVSI − c_delay, irreversibility shadow cost, process KPIs.

### 6.1 Decision rights [I; NAV ≈ US$177bn]

| Tier | Triggers (any one) | Process | Approval |
|---|---|---|---|
| A | Action ≥0.25% of NAV (≈$0.44bn); secondary discount >10%; sleeve LTV up >5 pp or portfolio leverage up >1 pp; tail budget change >10 bp/yr; any change to the opportunistic risk limit | Full lab; S0–S7; H0–H6 | Simple majority plus the **symmetric irreversibility protocol** |
| B | Above desk mandates, below A; intra-period overlay re-strikes | S1 and S5 only | CIO + CRO |
| C | Within mandate | Ledger entry | Desk |
| Board / owner | Tier-1 gate amber or red; P50 survival < 24 months; distribution-rate recommendations; leverage outside its band; a *value* split (§6.5) | IC recommendation plus minority report | Board |

**Symmetric irreversibility protocol.**
- It applies to any choice that forfeits optionality with expected loss above 0.25% of NAV. That includes *letting an expiring bid or refinancing window lapse*.
- It requires a recorded second-chance check (Janis) and CRO sign-off.
- It replaces the asymmetric ⅔ supermajority, which tilts the IC toward HOLD in a liquidity squeeze.

**Deferral budget:** after 2 consecutive deferrals, the item escalates.

### 6.2 Shadow-IC

**Seats.** Each seat has a mandate, an evidence slice, a loss emphasis and a model family. There are no demographic or personality personas.

| Seat | Mandate / loss emphasis | Evidence slice |
|---|---|---|
| Fiduciary & Distribution Steward | 5–10% owner distribution; Tier 1 | Liquidity engine; C3 owner-draw paths |
| Private-Markets Underwriter | Drift between underwritten, actual and forecast returns; exits | C2 belief cards; memo corpus |
| Capital-Structure & Financing | REFI/LEVER; covenant and margin-spiral risk | Facility terms; LTV paths |
| Tail-Hedge Strategist | Convexity per unit of carry; monetization | Overlay engine; option surfaces |
| Opportunistic-Trading PM | Alpha vs beta; capacity; correlation in stress | P&L; deflated Sharpe ratio (DSR) card |
| Outside-View Forecaster | Base rates; owns the probability table | Reference-class database |
| Red Team | Strongest case against; analysis of competing hypotheses (ACH) | Post-mortems; failure corpus |

**Support roles:**
- A non-substantive Facilitator runs the protocol and may not introduce claims or numbers.
- An AI Validator, on a different model family, only flags.

**Model families.** With ≤40% of seats per family, 7 seats need ≥4 families. With 2 families at launch: treat same-family seats as correlated when pooling, never extremize, and disclose the family mix.

**Protocol** (T = meeting day; batch API for the non-interactive stages):

| Stage | Day | Content |
|---|---|---|
| S0 | T−10 | Contract and alternatives, always including the status quo and DEFER; 8–15 frozen questions per Tier-A item (≤20 per meeting; ≥50% resolving within 12 months); 6–8 MAP dimensions |
| S1 | T−7 | Independent assessments with no cross-visibility: MAP percentiles, probabilities, actions, top-3 artifacts, "what would change my mind" |
| S2 | T−5 | Reveal: pooled estimates, dispersion, member-to-decision map, cruxes ranked by value of information (VOI), discursive-dilemma check |
| S3 | T−4 | Evidence-gated debate on ≤3 cruxes, ≤2 rounds. A move of >5 pp needs a newly surfaced, validator-checked artifact; otherwise it is reverted and logged [I; ablate]. Pre- and post-debate pools both reported |
| S4 | T−3 | Pre-mortem ("October 2029: this failed"); ACH on whether the DPI decline is cyclical or structural |
| S5–S7 | T−2 | Append-only, hashed minority reports; questions ranked by expected value of perfect information (EVPI) and distance to flip points; package of ≤6 pages |

### 6.3 Human meeting flow and console

| Step | What happens |
|---|---|
| H0 Blind pre-vote (locks T−1) | Members see the fact pack and model outputs: metrics, robustness card, gates, action-economics and belief cards. They do **not** see the AI narrative, shadow-IC map or minority reports. They submit probabilities, MAP scores and a provisional action, which lock on submit |
| H1 Reveal | Order: anonymized human dispersion → model baseline → shadow-IC map → minority reports. Colleague consultation is encouraged after the lock, to counter Fogliato's second-opinion effect |
| H2 Cruxes | Discussed with the live console |
| H3 Pre-mortem | Led by a rotating human devil's advocate |
| H4 Ballot | Simultaneous approve / resize / defer / reject, with probabilities, a one-line rationale and "what would change my mind". A member accepting the AI recommendation must write one way it could be wrong. Then a second-chance check |
| H5 Minutes | AI-drafted, with every number linked to its source; approved by the secretary; dissent recorded verbatim |
| H6 Close the loop | Signposts go to monitoring, questions to the forecast registry, and the decision record is filed |

**Console.**

*Grounded Q&A.*
- Answers cite `run_id:artifact:path`.
- Each statement is labelled *model output*, *agent judgment* or *assumption*.
- "Not in the artifacts" is an acceptable answer.

*What-if tiers.* All results are *exploratory*.

| Tier | Method | Latency |
|---|---|---|
| W1 | EP re-weighting | < 1 s |
| W2 | Re-optimization on cached CRN paths | Seconds to minutes |
| W3 | Re-simulation, run as an MCP Task | Minutes to hours |

The IC may decide on exploratory evidence. If it does, the record flags the evidence plane, and an irreversible Tier-A action needs a confirmatory sealed run before execution.

*Displays:*
- the disagreement map;
- a post-lock "dot plot" of members' P(10%), P(breach) and actions;
- C1's robustness card;
- C2's break-even cards;
- signposts.

A difference is greyed out if $|\Delta|<2\,\mathrm{SE}_{paired}$, or if it is below 1 bp CE or 0.1 pp of probability. Model uncertainty is shown as a separate band.

### 6.4 View conditioning

**Channel A: asset-return views** (feed into C2 fusion).
- Member $k$'s view on asset $i$ enters as a signal $s_{IC_k,i}=\mu_i+\epsilon$.
- Until the forecast registry calibrates them: $\alpha_{IC}=0$, $\beta=1$, and $\omega=(P90-P10)/2.563$ from the member's stated 80% interval.
- The result is a member-specific posterior $\hat\mu_i^{(k)}$.

**Channel B: scenario, cash-flow, regime and macro views** (EP on the shared paths).
- Example: "PE distributions in Y1–Y2 are 30% below base."
- Confidence is applied by **shrinking the target**, then EP is solved exactly:

$$v^{eff}_j=\mathbb E_p[g_j]+c_j(v_j-\mathbb E_p[g_j]),\qquad q^\star=\arg\min_{q\in\Delta^N}\sum_sq_s\ln\frac{q_s}{p_s}\ \text{s.t.}\ \mathbb E_q[g_j]=v^{eff}_j\ (\text{or}\le)$$

- The solution has the form $q^\star_s\propto p_se^{-\lambda^\top g(x_s)}$.
- Find λ from the dual $\max_\lambda-\ln\sum_sp_se^{-\lambda^\top g_s}-\lambda^\top v^{eff}$ (with sign constraints for inequality views), using L-BFGS with log-sum-exp.

**Why shrink the target instead of blending:**
- Among all distributions that satisfy the shrunk view, $q^\star$ has the minimum KL divergence. So it never distorts more than Stream 14's linear mixture $(1-c)p+cq^\star_{full}$, which meets the same target.
- It stays in the exponential family (Stream 10's log-linear property).
- The member confirms the *effective* view: with c = 0.6, "30% below" becomes **18% below** [S, verify-14].

**Flags.** All are expressed in KL($q\Vert p$), which remains valid after tilted re-simulation; ENS adds nothing beyond KL under uniform weights [S, verify-10].

| KL (nats) | Status |
|---|---|
| > η_max | Inform: outside model ambiguity |
| > 0.25 | Warn: the IC has materially moved the base case |
| > 1.20 | Amber |
| > 2.30 | Red: force re-simulation with a tilted sampler and likelihood-ratio weights |

**Precision:**
- Kish $n_{eff}=1/\sum q_s^2$, with a floor of 5,000;
- $\max_s q_s/p_s\le50$;
- $\mathrm{SE}(\hat P)\approx\sqrt{\hat P(1-\hat P)/n_{eff}}$.

**Procedure:**
- Run a Phase-I LP feasibility check first, and report the minimal relaxation if views conflict.
- Compute path-dependent metrics per path, then re-weight; never re-weight summary statistics.
- Re-weighting cannot create outcomes that were never simulated. That is why the red flag triggers re-simulation.

**Admission to the ambiguity set:** $\mathrm{KL}(q_k\Vert p)\le\eta_{max}$, with η_max equal to C1's η (placeholder 0.05 nats). The anchor is the fee-consistent cross-provider KL of ≈0.02–0.06 nats [S\*]. More extreme views must bring evidence.

### 6.5 Implied decisions and disagreement

**Implied action** for member $k$:

$$a^*_k=\arg\max_{a\in\mathcal A_{T1}}J(a;q_k,\theta_k)$$

- $\mathcal A_{T1}$ is the set of actions that are Tier-1 feasible under C1's ambiguity set.
- $\theta_k$ holds the member's values (penalty and shadow-price weights).
- $J$ is measured in CE bp.

**Regret:** $R_k(a)=J(a^*_k;q_k,\theta_k)-J(a;q_k,\theta_k)$.

**Two disagreement measures:**
- *Belief dispersion*, $\mathrm{sd}_k(p_{k,j})$.
- *Decision-relevant disagreement*, $\mathrm{DRD}(a_c)=\frac1K\sum_kR_k(a_c)$.

High dispersion with low DRD means the disagreement does not affect the decision.

**Belief vs value split.** Let $a_c=a^*(q_m,\theta_m)$ for the committee median, and

$$\rho(q,\theta)=J(a^*(q,\theta);q,\theta)-J(a_c;q,\theta)$$

The two-factor Shapley split is

$$\phi_b=\tfrac12[\rho(q_k,\theta_m)+\rho(q_k,\theta_k)-\rho(q_m,\theta_k)],\qquad\phi_v=\rho(q_k,\theta_k)-\phi_b$$

- If $\phi_b\ge\phi_v$, it is a belief split: send it to diligence and EVSI.
- Otherwise it is a value split: send it to the Board or owner (Santiago GAPP 6–9).

**Minority-report triggers** (either one):
- $|p_{k,j}-\bar p_j|\ge15$ pp;
- $a^*_k\ne a_c$ and $R_k(a_c)\ge10$ bp CE.

**Crux sensitivity:**
- flip values $v_j^\dagger$, found by root-finding;
- Shapley over ≤10 view components (1,024 EP-plus-optimizer runs), or permutation sampling beyond that.

### 6.6 Committee diagnostics

**Credal set:** $\mathcal Q=\{p\}\cup\{q_k:\mathrm{KL}(q_k\Vert p)\le\eta_{max}\}$.

Because the set is finite, $|\mathcal A|\cdot|\mathcal Q|$ evaluations are exact. The vertex shortcut fails for CVaR-penalized J: in verify-14's counterexample the true worst case is −0.210, against −0.120 at the vertices.

| Rule | Definition | Use |
|---|---|---|
| Pooled | $a^{pool}=\arg\max_aJ(a;\bar q)$, with $\bar q=\frac1K\sum q_k$ | Default for reversible actions |
| Minimax regret | $a^{MR}=\arg\min_a\max_{q\in\mathcal Q}[J(a^*_q;q)-J(a;q)]$ | **Default for irreversible actions** |
| Max-min | $a^{MM}=\arg\max_a\min_qJ(a;q)$ | Diagnostic only: it gives the most pessimistic member a de facto veto, which invites view-shading |
| Ballot | $a^{vote}$ | The decision |

**Discursive-dilemma flag:** raised when $a^{pool}\ne a^{vote}$, i.e. aggregating premises gives a different answer from aggregating conclusions.

### 6.7 DEFER: cross-fitted EVSI

Let $Y$ be a signal that will be observable by the next meeting, such as next-quarter distributions or refreshed bids.

**Procedure** (K = 5 folds):
1. On the training folds, form $B$ quantile bins of $Y$.
2. Choose the best action in each bin, $a_b^{(-f)}$, and the best unconditional action, $a_0^{(-f)}$.
3. On the held-out fold, compute CE(act after observing $Y$, including the cost of acting at $t+1$) − CE($a_0^{(-f)}$).
4. Average across folds, giving $\mathrm{EVSI}^{cf}$.
5. Bootstrap a CI, and test sensitivity to $B\in\{5,10,20\}$.
6. Convert to dollars with §5.4's formula.

**Cost of delay** (all terms from C2 action economics):

$$c_{delay}=\text{carry}+P(\text{bid expires})(\text{bid}-\text{next-best})+\text{decay}$$

**Rule.** DEFER iff all three hold:
- $\mathrm{LCB}_{0.80}(\mathrm{EVSI}_\$)>c_{delay}$;
- no staged or partial action (e.g., sell 50% now) has a higher cross-fitted value;
- fewer than 2 prior consecutive deferrals.

In-sample EVSI is biased toward DEFER [S\*]. A re-underwrite yields EVSI, never EVPI.

### 6.8 Signposts as event-triggered control

For chosen action $a_c$ and indicator $z_j$:
- **Flip value** $z_j^\dagger$: where $J(a_c;q(z))=\max_{a\ne a_c}J(a;q(z))$, with $q(z)$ the EP posterior conditioned on the indicator.
- **Alarm** $z_j^A$: $0.5\sigma_{noise}$ on the safe side of the flip value.
- **Re-arm** only after a further 0.25σ retreat (hysteresis).
- **Responses:** crossing $z^A$ triggers a Tier-B review; crossing $z^\dagger$ triggers a Tier-A re-decision.

Each decision carries 3–6 signposts, drawn from the S4 failure modes ranked by probability × impact.

### 6.9 Safeguards [S/I]

1. **Numeric provenance:** every number resolves to an artifact path or a labelled human judgment, or publication is blocked.
2. **Write barriers:** views reach engines only as confirmed ViewSpecs.
3. **Dissent:** append-only, hashed, shown beside the recommendation, never paraphrased by the synthesizer.
4. **No persuasion optimization** (Hackenburg, *Science* 2025: persuasion gains came with accuracy losses): no tuning or selection on adoption; no personalization to members; plain register with the strongest counter-argument; periodic plain-vs-fluent A/B audits.
5. **Anti-sycophancy:** agents are blind to the chair's and CIO's identities and preferences; human views are anonymized and shown only after S1; updates are evidence-gated.
6. **Automation bias:** training and instructions do not prevent it, even in experts (Parasuraman & Manzey 2010). Prevention therefore rests on workflow design: human-first pre-votes, numeric provenance, the AI track record shown with CIs, and a per-item kill switch (EU AI Act Art. 14(4)(e) analogue). One seeded-error drill per Tier-A meeting (programme disclosed, items not) monitors and measures automation bias; it does not prevent it [corrected 2026-10-18].
7. **Untrusted documents:** GP documents are data, never instructions.
8. **The IDM is a model:** inventoried, version-pinned, regression-tested before upgrades.

### 6.10 Learning loop

**Scoring:**
- Brier score $BS=\frac1N\sum(f_i-o_i)^2$, decomposed as REL − RES + UNC;
- log score;
- Brier skill vs the model, $BSS_k=1-BS_k/BS_{model}$, which measures the value of overriding the model. For comparison, FOMC members' own forecasts received roughly zero weight against the staff forecasts (Romer & Romer 2008) [S].

**Display weights** (votes remain one member, one vote):
- update $w_{k,t+1}\propto w_{k,t}e^{-0.3\ell_{k,t}}$;
- shrink with $Z_k=n_k/(n_k+\hat K)$, where $\hat K=\widehat{EPV}/\widehat{VHM}$;
- display $\max(0.05,Z_kw_k+(1-Z_k)/K)$, renormalized.

**Also tracked:** the minority-report hit rate, and outcomes at 1, 4 and 8 quarters.

**Inference.** Forecasts cluster by question, vintage and regime, so use hierarchical or cluster-robust inference.

### 6.11 Evaluating the IDM

**Power.**

$$n_{eff}=n/(1+(m-1)\mathrm{ICC}),\qquad \mathrm{MDE}=(z_{0.975}+z_{0.80})\sqrt{2\sigma^2/n_{eff}}$$

With σ ≈ 0.2, detecting ΔBS = 0.01 needs ≈6,300 effective forecasts per arm. At 10–20 forecasts per meeting, **an online trial cannot test the success threshold.**

**Evidence instead comes from:** offline suites (hidden-profile cases with ≥80% surfacing; seeded errors; sycophancy and flip tests; a diversity alarm if the pairwise rank correlation between seats exceeds 0.9; time-sliced replay with leakage probes, post-cutoff periods only, since "post-cutoff, we observe no recall" [S]); 6–12 months of shadow mode; and descriptive Bayesian monitoring, $BS_{iqk}=\alpha+\beta T_i+u_k+v_q+w_{item}+\varepsilon$. **KPIs:** appropriate reliance (weight-of-advice toward the AI, split by AI right/wrong); noise index; dissent rate; anti-portfolio returns; a blind-scored Decision Quality rubric.

---

## 7. Default parameters

| Parameter | Default | Note | Basis |
|---|---|---|---|
| Workers | 3 (2 shared + 1 isolated) | Ablate 1–4 | [I]; herding [S] |
| Idea cycles; evaluations per attempt | 20; 2 | Case studies used 20–60 cycles; GRPO used 1 evaluation per attempt | [S] |
| K₀, η, n₀, rungs | 27, 3, 2,000 per model, 3 | Size n₀ from SE | [I] |
| K_final | 3 | — | [I] |
| Search / sealed planes | ≥2 families / ≥2 worlds + ≥3 windows; 50,000 paths per world | — | [I]; deck [S] |
| τ | 0.5 pp CE | Also {0.25, 1, ∞} | [I] |
| γ, H, λ_T | 3; 10y rolling (5y reported); λ_T from C1 (placeholder 0.5) | Owned by C1 | Stream 11 [I] |
| ε_mat (CE bp/yr) | Overlay 3; pacing 5; REFI/LEVER 10; SELL or other irreversible 15 | IC sets per contract | [I] |
| z screen / promote; bootstrap B | 1.28 / 2; 500 / 1,000 | — | [I] |
| PBO | 16 structural blocks; gate ≤0.20 if ≥8 blocks; n_b = 500 | — | Bailey et al. [S]; [I] |
| Deflation | 95% null quantile, N_eff | — | [S\*] |
| α-investing | W₀ = 0.05, ω = 0.05; escalate if W < 0.005 | Reset policy open | Foster–Stine [S]; [I] |
| Patience | 6 cycles | — | [I] |
| Memory | ≤300 words; 3 attempts; curator signs flips | — | Repo [S] |
| Scheduler | Discounted UCB, 0.9 | — | [I] |
| Judges / auditor / translator | κ ≥ 0.6 on ≥50 items / ≥90% recall (95% target) / p ≥ 0.965 | — | [I] |
| Shadow-IC | 7 seats + facilitator; ≥4 families (≥2 at launch); ≤3 cruxes × ≤2 rounds; 5 pp evidence gate | Evidence gate to be ablated | [I]; [S\*] |
| Dissent triggers | 15 pp; 10 bp CE | — | [I] |
| Questions; signposts | 8–15 per Tier-A item (≤20 per meeting); 3–6 per decision, alarm at 0.5σ | — | [I] (reconciled) |
| η_max | C1's η (placeholder 0.05 nats) | Range {0.02, 0.05, 0.10} | [S\*] anchor |
| KL flags (nats) | Inform > η_max; warn > 0.25; amber > 1.20; red > 2.30 | — | Streams 10 and 14 reconciled |
| Kish floor; maximum weight ratio | 5,000; 50 | — | [I] |
| Pooling; extremizing | Linear, equal weights; α = 1 for agents (humans: fitted after ≥100 resolutions, capped at 1.5) | Log pool as sensitivity | [I] |
| Hedge η; weight floor | 0.3; 0.05 | — | [I] |
| EVSI | K = 5 folds; B ∈ {5, 10, 20}; LCB at 80%; deferral budget 2 | — | [I] |
| Tier-A size trigger | 0.25% of NAV ≈ $0.44bn | — | [I] |
| Token budget; shadow mode | $50 soft / $200 hard per cycle; 6–12 months | — | [I] |

---

## 8. Calibration targets

| Parameter | Value | As of | Source | Confidence |
|---|---|---|---|---|
| Claim coverage | 1.00 | Design | Sakana writer rules | High (target) |
| Undetected protocol violations | Target 0. Benchmark: violations occurred in 2/3 Pi GRPO runs and in some Claude Code runs | Oct 2026 | Lange et al. §6.3, Fig. 17 | High |
| LLM analyst-task score | Best model 64.37% | 4 Jun 2026 | Vals Finance Agent v1.1 | High |
| Retrieval-QA failure | 81% incorrect or refused (150 cases) | Nov 2023 | FinanceBench | High (dated) |
| Autonomous statement accuracy | 79.4%, although every statement cited code or primary literature: citation coverage is necessary but not sufficient [corrected 2026-10-18] | Nov 2025 | Kosmos | High |
| Reward-hacking rate | 30.4% (39/128) | Jun 2025 | METR | High |
| AI reviewer balanced accuracy | 69% (possibly contaminated); 66% clean, equal to humans | 26 Mar 2026 | Sakana blog on the *Nature* paper (Lu et al. 2026). Not in the *Nature* abstract, which reports a 70% workshop acceptance rate [corrected 2026-10-18] | Medium (blog figures) |
| Reviewer–performance correlation | r = 0.44 (n = 70); require ≥0.6 vs IC ratings | Oct 2026 | Lange et al. Fig. 8c | High |
| Human edit share | +17.5% / −10.7% (draft to submission); +32.8% / −15.6% (to camera-ready) | Oct 2026 | Lange et al. Table 2 | High (weak proxy) |
| Monte Carlo paths needed | 7,299 (p = 5%, ±10% relative); ≈38,000 (p = 1%); 2% on 50k paths is ±0.12 pp | — | Verified arithmetic | High |
| Paired SE of P(10%) | 0.50 pp at 2k paths; 0.22 pp at 10k (ρ = 0.9) | — | Verified | High |
| Halving saving; deflation hurdle | 3–3.9×; 3.47σ at N = 200 | — | Verified | High |
| Retrieval herding | Action correlation 0.04 → 0.41 | 2026 | Song (ICLR workshop) | Medium |
| Debate vs vote | Single 0.721 / vote 0.769 / best debate 0.738 (Qwen2.5-7B) | 2025 | Choi et al. | Medium (small models; mixed evidence) |
| Human–AI teaming (Hedges' g) | −0.23 vs the better agent; −0.27 on decision tasks; −0.54 when the AI is better; +0.64 vs humans alone | 28 Oct 2024 | Vaccaro et al. | High |
| AI-assisted forecasting | +24–28% (N = 991; 6 questions) | 2024 | Schoenegger et al. | Medium |
| Cross-provider KL (anchor for η_max) | ≈0.02–0.06 nats | Oct 2026 | Verify-10 | Medium |
| IDM detection requirement | ≈4,000–11,000 independent forecasts per arm | — | Verify-14 | High |
| Token cost per cycle | ≈$8.7–15.7 | Oct 2026 | Anthropic list prices | High (prices); Medium (volumes) |
| Peer adoption | NBIM: 600+ users; >20% weekly time saved | 2026 | Vendor case study | Medium |
| Dollar value of CE | 1 bp/yr ≈ $17.7m/yr | — | Computed | High |
| Hidden-profile surfacing | ≥80% | Design | [I] | Low–Medium |

---

## 9. Strongest cross-disciplinary insights

1. **The verifier is a hypothesis.**
   - Sakana's and AlphaEvolve's evaluators measure reality, or a validated simulator. ADIC's measures a model of the future, so search exploits that model's misspecification.
   - "Robustness is verification" therefore makes C1's robust objective and C4's discovery protocol a single design.
   - ADIC's version of AlphaEvolve's post-deployment check is Brier-scoring every probability the IC was shown.

2. **Agents as column generators; duals as referee** (operations research).
   - C1's duals price any proposal through its reduced cost $r_j=\Delta J_j-\sum_k\lambda_k\Delta g_{kj}-c_j$.
   - Single-asset lens actions can be enumerated deterministically.
   - LLMs earn their keep only where the column space cannot be enumerated: packages, new structures (continuation vehicles, preferred equity, hedge restructures), and translating narratives into constraints.
   - "Not established" then gets a precise meaning: no column with positive robust reduced cost was found.

3. **One epistemology for every forecaster.** Strategy groups (C2's α_g), the opportunistic overlay (C3's DSR), agent-discovered policies, IC members and the model itself all face the same three disciplines:
   - proper scoring;
   - credibility shrinkage;
   - deflation for the number of trials.

   One registry serves all of them, and the IC's own value-add becomes measurable.

4. **Aggregate premises, not conclusions.**
   - Each member's beliefs re-weight the same paths, and one optimizer maps every re-weighting to an implied action.
   - Disagreement is measured in regret and split into belief and value components. Belief splits go to diligence; value splits go up the delegation chain.
   - This is the committee analogue of misspecification-robustness.

5. **Pre-registration is the common cure.** Sakana's contracts, Dwork et al.'s reusable holdout, the sealed plane, frozen questions and blind pre-votes are all the same device: commit before seeing results. Every steer creates a new version, and "no action clears the gate" is a valid memo.

6. **Runtime assurance wraps every unverified controller** (control theory's Simplex architecture, plus C1's safety filter).
   - LLM-discovered policies, IC amendments and opportunistic trades all run inside a verified Tier-1 envelope with a fallback.
   - Signposts are event-triggered control with hysteresis.

7. **Effective challenge is organizational.**
   - Incentives, competence and influence belong to people. A second model family adds *error diversity*, not *incentive separation*.
   - So AI flags and humans veto.
   - Correlated LLM errors also rule out extremizing LLM ensembles.

8. **Non-anticipativity and monotonicity as types.** Type rules turn look-ahead and gambling-for-resurrection into compile errors rather than validation findings.

---

## 10. Cross-cluster links (interface contracts)

### C1: optimization core, scenarios and robustness, objective (Streams 01, 10, 11)

**C4 consumes:**
- J in CE units;
- Tier-1 gates with governance bands and hysteresis;
- disjoint generator families and seed keys;
- τ, η, and $\eta_L\approx0.01$–0.02 with importance sampling;
- robustness metrics R1–R8, using W∞ rather than W1 for probabilities;
- the EP solver;
- duals and forced-action re-solves;
- the safety-filter QP;
- the information-relaxation bound;
- reverse stress outputs $q^\star,\eta^\star$.

**Feasibility warning.** C1's verifiers found infeasible gates:
- the deck's 7%-at-95% floor would need an expected return of ≈15.8–17.9%;
- Stream 11's C3 drawdown constraint is infeasible;
- Stream 01's C1–C8 constraint set may be infeasible.

That is why G0 runs a Phase-I feasibility check; otherwise the lab would always return "not established" or quietly relax its gates.

**C4 provides:**
- the counted-evaluation (data-snooping) ledger;
- the PolicySpec DSL;
- the sealed-plane protocol;
- member posteriors $q_k$ for the IC card;
- red-team ScenarioSpecs;
- decision records for recalibration.

### C2: private book, liquidity instruments, leverage, action economics, return fusion (Streams 04–08)

**C4 consumes:**
- GLS-fused beliefs (replacing Stream 13's Eq. 6), with flags F1–F10 and belief cards;
- action-economics cards: reservation price, break-even IRR, liquidity shadow value, P(ex-post best), regret, EVSI;
- the liquidity merit order;
- covenant objects;
- DPI-drought regimes, used as sealed worlds.

**C4 provides:**
- quarantined extractors;
- IC views as fusion signals;
- the forecast registry that calibrates $\alpha_g$;
- the timing-optimism challenger;
- the lessons ledger;
- an auditor rubric for verify-07 R5: asset-level recaps are tested on unlevered return vs after-tax debt cost; LP-level NAV loans on NAV forward return vs loan cost.

### C3: distribution policy and sovereign liabilities, peers/TPA, derivatives overlay (Streams 02, 03, 09)

**C4 consumes:**
- owner-draw paths and the shock-type posterior, which feed the sealed owner-shock world;
- candidate distribution rules;
- the overlay margin and collateral engine;
- the defensive-stack frontier;
- the opportunistic evidence card (posterior Sharpe, DSR);
- the pre-approved monetization playbook.

**C4 provides:**
- escalation routing: distribution rate and leverage band are Board/owner items, as in NBIM's chain of delegation;
- SHELF-style elicitation of owner-related probabilities;
- a **hedge-fatigue** control: pre-commitment plus a journal comparing carry with modelled value;
- deflation discipline for the opportunistic strategy's track record;
- the peer refresh calendar.

---

## 11. Governance mapping

| Layer | Benchmark (status) | ADIC practice |
|---|---|---|
| Engines | SR 26-2 (17 Apr 2026; supersedes SR 11-7; non-binding US bank guidance); PRA SS1/23 (in effect 23 Apr 2026; independent validation; AI sub-principle) | Inventory and tiering. Effective challenge, meaning SR 11-7's incentives, competence and influence, a requirement SR 26-2 retains. Outcomes analysis. Change control |
| LLM roles | SR 26-2 footnote 3 excludes them. NIST AI RMF 1.0; NIST AI 600-1 (confabulation; human–AI configuration); ISO/IEC 42001 | A separate AI management system. Materiality: High (Drafter, Validators, Planner, Facilitator); Medium (Writer, Auditor, Red Team, Extractors, seats); Low (Ideators, Scouts) |
| Oversight | EU AI Act Art. 14(4)(b), (d)–(e) as a benchmark (Annex III from 2 Dec 2027, per Reg. 2026/1744); UAE AI Charter (Jul 2024); CBUAE (Feb 2026) | Awareness of automation bias; override and kill switch; decision rights documented |
| Sovereign | Santiago GAPP 6–9, 19, 22 | Decision-rights matrix; escalation; auditable record for the owner |

Benchmarking only to SR 26-2 could lower the bar relative to SR 11-7 practice.

---

## 12. Build path and ablations [I]

**Build phases:**

| Phase | Months | Scope |
|---|---|---|
| 0 | 0–3 | Synthetic data; contracts, registries and claim validator; cassettes; a 20–50-task evaluation suite |
| 1 | 3–9 | Real data hosted in-region; the lab on one decision class (the liquidity-raise programme) in shadow mode; the IDM in shadow mode |
| 2 | 9–18 | Tier-B pilot with pre-votes and the forecast registry; add the family-B auditor; then Tier A |
| 3 | Later | Quarterly lens enumeration; outer-loop recalibration |

**Ablations to run:**
- scaffold vs a single session at a fixed model (the experiment the paper did not run);
- 1–4 workers, with shared vs isolated memory;
- single agent vs vote vs plain debate vs evidence-gated debate;
- rubric strictness, on a known-answer task;
- auditor on vs off.

All are scored on validity, faithfulness, shrinkage and cost.

---

## 13. Open questions and data ADIC must supply

**Open questions:**
1. Is the model served in a UAE region? Which data classes may enter prompts? Which additional model families are available under sovereignty constraints?
2. Who signs contracts, and who sets τ, ε_mat, the PBO and κ thresholds, K_final and η_max?
3. Will MRM accept ensemble-based verification, given how few independent PE cycles exist?
4. What is the legal status of AI-drafted dissent and minutes in the sovereign record?
5. Should α-wealth reset per contract, per fiscal year, or never?
6. Is any delegated autonomy acceptable, such as hedge-ratio drift within bands?
7. Are blind pre-votes culturally feasible, given seniority effects?
8. Who owns the value parameters (γ, λ_T, distribution reliability)?
9. Which short-fuse proxy questions are valid for slow-resolving PE outcomes?
10. What latency is acceptable for re-weighting vs re-simulation?
11. How do we prevent pre-training leakage in historical replay?

**Data ADIC must supply:**
- the 18-year memo corpus, point-in-time, with underwriting and downside cases, post-mortems and outcomes;
- IC history: votes, dissents, overrides, rationales;
- timestamped strategy-group forecasts and their revisions;
- the asset table: NAV and its staleness, cash flows, unfunded commitments, facility terms, LPA transfer clauses;
- overlay positions, CSA terms and margin history;
- opportunistic P&L, together with the number of strategies tried;
- the owner's distribution rules and history;
- the current delegation matrix;
- golden sets: engine-generated numeric Q&A; ≥50 translation pairs written by IC members; seeded-error memos; prompt-injection documents; hidden-profile cases;
- a scenario library labelled by family, a policy library, the model inventory and the member registry.

---

## 14. Key references (corrected forms)

**Discovery systems**
- Lange, Grillotti, Yamada, Charakorn, Ha (2026), *The Agentic Scientist*, arXiv:2610.18933; code: SakanaAI/AI-Scientist-v3.
- Lu, Lu, Lange, Yamada, Hu, Foerster, Ha & Clune (2026), "Towards end-to-end automation of AI research", *Nature* 651(8107):914–919, DOI 10.1038/s41586-026-10265-5.
- Novikov et al., *AlphaEvolve*, arXiv:2506.13131.
- *Kosmos*, arXiv:2511.02824.
- METR (5 Jun 2025).
- Luo et al. (2026), auditing from logs and code, as summarized in Lange et al.'s related work.
- Gaddipati, Muhammed, Keya, Rabby & Auer (2026), *MLReplicate*, arXiv:2605.16616.

**Finance agents**
- *FinanceBench*, arXiv:2311.11944.
- Vals AI Finance Agent v1.1.
- *FINSABER* (KDD 2026).
- Song (ICLR 2026 workshop).

**Engineering**
- Anthropic engineering posts (2024–26).
- MCP 2026-07-28 changelog.
- *CaMeL*, arXiv:2503.18813.

**Deliberation**
- Du et al. (ICML 2024); Choi, Zhu, Li (NeurIPS 2025); Wynn et al. (2025, ICML 2025 MAS workshop); Smit, Grinsztajn, Duckworth, Barrett & Pretorius, ICML 2024, PMLR 235:45883–45905 (arXiv:2311.17371); Chan et al., *ChatEval*, arXiv:2308.07201; Michael et al., arXiv:2311.08702; Laban et al., arXiv:2311.08596.
- Tessler et al., *Science* 386 (2024).

**Human–AI teaming and persuasion**
- Vaccaro, Almaatouq & Malone, *NHB* 8(12):2293–2303 (2024), DOI 10.1038/s41562-024-02024-1.
- Fogliato, Chappidi, Lungren, Fisher, Wilson, Fitzke, Parkinson, Horvitz, Inkpen & Nushi, "Who goes first? Influences of human-AI workflow on decision making in clinical imaging", *FAccT '22*, pp. 1362–1374, DOI 10.1145/3531146.3533193.
- Parasuraman & Manzey (2010), *Human Factors* 52(3):381–410, DOI 10.1177/0018720810376055.
- Hackenburg et al., "The levers of political persuasion with conversational artificial intelligence", *Science* 390(6777):eaea3884 (2025), DOI 10.1126/science.aea3884.
- Salvi, Horta Ribeiro, Gallotti & West, "On the conversational persuasiveness of GPT-4", *NHB* 9(8):1645–1653 (2025), DOI 10.1038/s41562-025-02194-6.
- Schoenegger et al. (2024).

**Committees and decision theory**
- Hansen, McMahon & Prat, *QJE* (2018); Meade & Stasavage, *EJ* (2008); Romer & Romer, *AER* (2008); Klein, *HBR* (2007); Janis, *Groupthink* (1982).
- Kahneman, Lovallo & Sibony, "A structured approach to strategic decisions", *MIT Sloan Management Review* (Spring 2019).
- Schwenk (1990), *OBHDP* 47(1):161–176, DOI 10.1016/0749-5978(90)90051-a.
- Meucci (2008); Genest & Zidek (1986); List & Pettit (2002); Gilboa & Schmeidler (1989).
- Bühlmann (1967), "Experience rating and credibility", *ASTIN Bulletin* 4(3):199–207, DOI 10.1017/S0515036100008989. DOI 10.1017/S0515036100008023 is his 1969 sequel, *ASTIN Bulletin* 5(2):157–165.
- Foster & Stine, *JRSS-B* (2008); Bailey et al., *J. Comput. Finance* 20(4) (2017), DOI 10.21314/JCF.2016.322.
- Smith & Winkler, "The optimizer's curse: skepticism and postdecision surprise in decision analysis", *Mgmt Sci* 52(3):311–322 (2006), DOI 10.1287/mnsc.1050.0451.
- Bailey & López de Prado (2014), "The deflated Sharpe ratio: correcting for selection bias, backtest overfitting, and non-normality", *JPM* 40(5), DOI 10.3905/jpm.2014.40.5.094.
- Dwork et al., arXiv:1506.02629; journal version "The reusable holdout", *Science* (2015), DOI 10.1126/science.aaa9375.
- Li et al., Hyperband, *JMLR* (2018).

**Governance**
- ODNI ICD 203 (2015/2022).
- SR 26-2 and OCC 2026-13; SR 11-7 (historical).
- PRA SS1/23.
- NIST AI RMF; NIST AI 600-1; ISO/IEC 42001.
- EU AI Act Art. 14 and Reg. (EU) 2026/1744.
- UAE AI Charter (Jul 2024); CBUAE AI guidance (Feb 2026).
- IFSWF Santiago Principles.

---

## Citation corrections (2026-10-18)

**Sources.**
- `research/literature/00_LITERATURE_SYNTHESIS.md` §2.
- The citation-integrity tables in `research/literature/12_agentic_ai.lit.md`, `13_paper_deepread.lit.md`, `14_ic_deliberation.lit.md`, `04_pe_cashflows.lit.md` and `07_return_fusion.lit.md` (Bühlmann).
- `research/literature/recheck/13_paper_deepread.recheck.md` and `14_ic_deliberation.recheck.md`.
- Metadata confirmed via Crossref (the *Nature* article), OpenAlex (Bühlmann) and arXiv (MLReplicate).

**Changes.**
- §2.1, V5: the 69% and 66% reviewer accuracies are attributed to Sakana's blog, not the *Nature* abstract, which reports a 70% workshop acceptance rate (synthesis §2.3, streams 12 and 13).
- §8, AI-reviewer row: re-sourced to the Sakana blog (26 Mar 2026) and lowered from High to Medium. No design default depends on it.
- §8, Kosmos row: 79.4% accuracy despite full citation coverage, so coverage is necessary but not sufficient (synthesis §2.4 #11).
- §2.2, [U] list:
  - Schwenk (1990) moved out with the corrected wording: DA beat the expert baseline; DI's advantage was not shown on ill-structured tasks; neither beat the other (synthesis §2.4 #9).
  - The MAP caveat narrowed to its finer points, with pre-votes marked as ADIC's own design (13 re-check).
  - MLReplicate's 59% moved out, quoting §3's denominator (synthesis §2.4 #12; checked against arXiv:2605.16616).
- §3, row 34: Hansen, McMahon & Prat (2018) is cited as evidence of a discipline-versus-conformity trade-off in which discipline dominates on their influence measure, not as support for restricting transcripts (14 re-check).
- §5.7(e): added Smith–Winkler Bayesian shrinkage of the reported sealed-plane estimate. The ratio $s_i$ alone shrinks nothing (synthesis §2.4 #11; 12 and 13 tables).
- §5.7(g): noted the normal-null assumption, and the DSR's non-normality term for Sharpe-ratio statistics (synthesis §2.4 #11).
- §6.9, item 6: seeded-error drills monitor automation bias rather than prevent it, citing Parasuraman & Manzey (2010) (synthesis §2.4 #10).
- §14, key references:
  - Lu et al. (2026), *Nature*: added the full title, the eight authors in Crossref order, issue 8107 and the DOI.
  - Fogliato et al.: FAccT '22 author order, pp. 1362–1374, DOI.
  - Salvi et al.: journal title "On the conversational persuasiveness of GPT-4", *NHB* 9(8):1645–1653, DOI.
  - Hackenburg et al.: *Science* title, article eaea3884, DOI.
  - Vaccaro et al.: issue 12, DOI.
  - Smit et al.: ICML 2024 venue and proceedings author order; Wynn et al.: workshop venue.
  - Dwork et al.: the *Science* version.
  - Bailey et al.: 20(4) and DOI.
  - Smith & Winkler: full title, pages and DOI.
  - Added Bailey & López de Prado (2014), Parasuraman & Manzey (2010), MLReplicate (2026), Kahneman, Lovallo & Sibony (2019) and Schwenk (1990), which the corrected text now cites.
- §14, Bühlmann (1967): resolved cross-file inconsistency #2. OpenAlex confirms that DOI 10.1017/S0515036100008989 is the 1967 paper (*ASTIN Bulletin* 4(3):199–207) and that …8023 is the 1969 sequel (5(2):157–165). G6 is right; stream 07's DOI belongs to the sequel.

**Checked and unchanged.**
- V22 (Fogliato) and V27 (Michael et al.) already carry the corrected readings.
- The Holm-within / α-investing-across error criteria in §1 and V9 are already named.
- Lange et al. (V2) is already worded "not only on base model capabilities, but also on" orchestration.

**Not applicable.**
- Gao, Jiang & Yan; FINSABER's "often vanish"; ReConcile; Khan et al.; Wang, Morgenstern & Dickerson; Alshiekh et al.; and Kahneman, Lovallo & Sibony (2011) are not cited, or not quoted, in this file.
- No statistic from the G4 barrier re-run appears here.
