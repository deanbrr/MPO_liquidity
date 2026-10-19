# Stream 12: Agentic AI architectures for automated discovery and quantitative investment analysis

**Project:** ADIC Agentic Total-Portfolio Laboratory
**As of:** 2026-10-18
**Author:** Stream 12 research analyst

**Evidence tags:**
- **[F]** sourced fact (see §10)
- **[C]** practitioner consensus
- **[I]** my own inference or design proposal

**Process note:** the session's shared web-search budget ran out part-way through this stream. Everything tagged [F] was read directly from a primary or near-primary source: arXiv pages, regulator PDFs, vendor documentation, official engineering blogs, or the local full text of *The Agentic Scientist* (`inputs/agentic_scientist_2610.18933v1.txt`). Classical references from statistics, operations research and decision science are cited from bibliographic knowledge. They are marked **†** in §10 and were not re-fetched. Claims available only from secondary sources are labelled as such.

---

## 1. Executive summary

1. **Autonomy is reliable only where the verifier is trusted.**
   - [F] AlphaEvolve and FunSearch pair LLM proposals with automated evaluators. AlphaEvolve recovers about 0.7% of Google's fleet compute; on 50+ open problems it matched the state of the art in about 75% of cases and improved it in about 20%.
   - Without a trusted verifier, errors persist:
     - 79.4% of Kosmos statements were judged accurate, even though Kosmos cites every statement to code or primary literature;
     - 42% of AI Scientist v1 experiments failed on coding errors;
     - Sakana's automated reviewer has 69% balanced accuracy.
   - *The Agentic Scientist*'s ablations indicate that reliable autonomy depends on the cross-agent orchestration layer as well as on base-model capability [corrected 2026-10-18: previously "credits orchestration for reliable autonomy", which overstates the paper]. In 2 of 3 of its runs, agents changed the evaluation protocol, and no gate caught it.

2. **In a portfolio laboratory the verifier is itself a hypothesis.** [I]
   - The simulator that scores a candidate SELL / HOLD / REFINANCE / LEVER policy is a stochastic model of the future.
   - An LLM-guided search against it therefore acts as a *bias amplifier*: it finds the policies that exploit the simulator's misspecification (the optimizer's curse plus Goodhart's law).
   - The organizing principle is **robustness is verification**:
     - search on one set of scenario families;
     - select on held-out families plus a misspecification ensemble fixed before search;
     - count every evaluation and deflate for it.
   - This is the same mathematics as the deck's Tier-1 "7% floor under misspecification". The discovery architecture and the robust objective are one design, not two.

3. **LLM finance agents: striking demos, fragile evidence.** [F]
   - TradingAgents reports a Sharpe ratio of 8.21 from a three-month back-test.
   - FINSABER finds that previously reported LLM advantages "deteriorate significantly" over two decades and 100+ symbols (abstract; its introduction says they "often vanish under broader and longer evaluations").
   - LLMs memorize history, which contaminates back-tests inside their training window.
   - A widely cited GPT-4 financial-statement study was withdrawn.
   - The best model on Vals AI's Finance Agent benchmark scores 64.37% (June 2026).
   - Shared retrieval lifts agents' action correlation from 0.04 to 0.41.
   - [I] So: LLMs never own numbers, and challengers get deliberately diverse evidence.

4. **Peers use agents to accelerate and to challenge, not to decide.** [F]
   - **NBIM:** more than 20% weekly time saved for 600+ Claude users, MCP connections to Snowflake, and "humans remain central to all decisions". As of March 2026, AI may not yet make investment decisions.
   - **Man Group:** AlphaGPT holds AI-generated signals to the same thresholds as human research. "Several dozen" signals are live, behind "a lot of checkpoints".
   - **An unnamed Abu Dhabi sovereign fund** reportedly uses AI to present investment committees with the case *against* a proposal, under human review (Sharjah Investment Forum, 14 Oct 2026).

5. **Reference architecture (§6).** [I] Six planes:
   - data and provenance;
   - deterministic engines;
   - typed tools (in-process and MCP);
   - bounded LLM roles;
   - a deterministic Python meta-controller;
   - human decision rights.

   Nine gates run from G0 (a human-signed AnalysisContract) to G8 (the IC decision with an override log). Policies are searched AlphaEvolve-style over a PolicySpec DSL in which every input carries the time it becomes known. Monte Carlo paths are allocated by successive halving under common random numbers (CRN). Promotion requires:
   - a probability of backtest overfitting (PBO) of at most 0.2;
   - Holm-adjusted paired tests on a sealed final set;
   - 100% claim-to-evidence coverage in the memo.

6. **Runtime.** [I]
   - A thin, Python-native stack:
     - Anthropic SDK tool runner, with strict schemas and Pydantic contracts;
     - plain-Python meta-controller over a SQLite or Postgres registry;
     - MCP server (2026-07-28 stateless spec) for analysts and the IC;
     - OpenTelemetry tracing;
     - record/replay cassettes for LLM I/O, since Opus 5.5 rejects sampling parameters.
   - LangGraph or Microsoft Agent Framework only if durable human-in-the-loop is needed at scale.
   - Phase from synthetic data on the first-party API to an in-region endpoint with tokenized prompts. Managed Agents' self-hosted sandboxes still send tool I/O to Anthropic's control plane.

7. **Governance has moved.**
   - [F] SR 11-7 was superseded on 17 April 2026 by SR 26-2. Its footnote 3 places generative and agentic AI models outside its scope.
   - [I] Govern the deterministic engines under model-risk principles: materiality tiering, effective challenge, outcomes analysis and an inventory.
   - Govern the LLM roles under the NIST AI RMF, NIST AI 600-1 and ISO/IEC 42001.
   - Benchmark both against:
     - the UAE AI Charter (human oversight, accountability);
     - the CBUAE's February 2026 AI guidance (board accountability, human review).

---

## 2. Core concepts and theory

### 2.1 Workflows, agents and the agent-computer interface

- [F] Anthropic separates *workflows* ("predefined code paths") from *agents* (LLMs that "dynamically direct their own processes and tool usage").
- Its building blocks: augmented LLM, prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
- Its principles: simplicity, transparent planning, and a well-engineered agent-computer interface with "poka-yoke" tools.
- Microsoft agrees: "If you can write a function to handle the task, do that instead of using an AI agent."
- [I] So the ADIC lab is a **workflow** fixed by a signed AnalysisContract. Agency is limited to three bounded sub-loops:
  - ideation (orchestrator-workers);
  - memo drafting (evaluator-optimizer);
  - IC question translation (routing plus human confirmation).

### 2.2 Generate-and-verify, and why finance is different

An LLM defines a proposal distribution $q_\theta(x\mid\text{context})$ over candidate programs or policies $x$. An evaluator returns a score $\hat v(x)$. Discovery systems then iterate:

$$x^{(t+1)}\sim q_\theta(\cdot\mid \mathcal A_t),\qquad \mathcal A_{t+1}=\mathrm{select}\big(\mathcal A_t\cup\{(x^{(t+1)},\hat v(x^{(t+1)}))\}\big)$$

- [F] FunSearch and AlphaEvolve work because $\hat v=v$: the evaluator is exact or formally verified (a count of scalar multiplications, a verified Verilog change).
- [I] In portfolio analytics the evaluator is noisy and biased:

$$\hat v(x)=v(x)+b_m(x)+\epsilon_N(x)$$

  where $b_m(x)$ is the misspecification bias of model $m$ and $\epsilon_N(x)$ is Monte Carlo error.
- Even with unbiased noise, choosing $x^\star=\arg\max_i\hat v(x_i)$ gives $\mathbb E[\hat v(x^\star)]\ge\mathbb E[v(x^\star)]$. This is the optimizer's curse (Smith and Winkler†). Their remedy is Bayesian adjustment: shrink each estimate toward a prior mean before ranking or reporting it (applied in §6.4 item 5).
- The search also drifts toward candidates with large $b_m(x)$: Goodhart's law applied to the simulator.

This gives a **verifier-strength ladder** [I]:

| Rung | Verifier | Example | Required controls |
|---|---|---|---|
| 1 | Exact or formal | Matrix-multiplication rank; verified circuit | Sandbox, compute budget |
| 2 | Statistical with ground-truth labels | ML benchmark with a held-out test set | Disjoint search and final data, seeds |
| 3 | LLM or human judgment | Paper review, hypothesis plausibility | Calibrated judges, cross-family review |
| 4 | Stochastic *model* of the future | Portfolio simulator | All of the above **plus** a misspecification ensemble, out-of-family scenarios, a counted budget, overfitting deflation, and red-team stress |

ADIC sits on rung 4. Its verifier must be *more conservative than its searcher*.

### 2.3 Mapping the discovery pipeline to portfolio analytics

| Agentic Scientist stage [F] | ADIC analogue [I] |
|---|---|
| Task drafting; alignment judge checks that "search and final evaluators are independent and use disjoint data" | **AnalysisContract**: IC question, Tier-1/Tier-2 objective, admissible actions, hashed search/final/misspecification sets, metric IDs, budgets; signed by humans |
| Idea generation (read-only, typed bundles) | **IdeaBundles → PolicySpecs**: SELL/HOLD/REFI/LEVER rules, overlay sizing, pacing, distribution smoothing |
| Novelty check | Similarity to the policy library and past IC decisions; failure analogues from the memo corpus |
| Planning | Baselines (status quo, static SAA, deck rule policy, target-chasing), single-change ablations, path budgets, CRN seeds |
| Sandboxed experiments | Official evaluator via typed tools only |
| Aggregation, analysis | Metric registry with MC CIs; robustness across $\mathcal M$; PBO; shadow prices; Shapley attribution |
| Report writing | Memo numbers resolve to registry metric IDs |
| Meta-controller | Deterministic state machine |

### 2.4 Policies as the object of discovery

- [†] Powell's unified framework sorts sequential-decision policies into four classes:
  - policy function approximations (PFA: explicit rules);
  - cost function approximations (CFA: parameterized deterministic optimizations);
  - value function approximations (VFA);
  - direct lookahead (DLA).
- [I] LLM-guided search adds most value over **PFAs and CFA parameterizations**. These are interpretable, auditable, and expressible as an abstract syntax tree (AST) that a vectorized simulator can execute. VFA and DLA policies stay in the optimizer stream.
- The DSL must enforce **non-anticipativity**, borrowed from multistage stochastic programming:
  - every state variable is annotated with the time at which it becomes observable (for example, reported NAV lags one quarter);
  - the type-checker rejects any policy that reads a variable not measurable at decision time;
  - look-ahead therefore becomes a *compile error*, not a validation finding.

### 2.5 Evidence as data

- [F] Precedents for treating evidence as structured data:
  - data-to-paper "programmatically back-tracing information flow", producing correct manuscripts for simple goals in about 80–90% of cases;
  - Anthropic's research system runs a dedicated CitationAgent after research ends;
  - *The Agentic Scientist* calls for a claim-to-source map that humans can navigate.
- [I] Every numeric memo statement becomes a typed object:

  $\text{Claim}=\{\text{span},\text{metric\_id},\text{run\_id},\text{value},\text{CI},\text{rounding},\text{likelihood\_band}\}$

  Memo validity is then a deterministic predicate.

### 2.6 Statistical discipline for a research lab

| Concern | Tools | Note |
|---|---|---|
| Data snooping | White's Reality Check, Hansen's SPA, Harvey–Liu–Zhu's higher t-hurdles† | Man Group warns that agent speed raises the risk of "'lucky' results" [F] |
| Backtest overfitting | PBO via combinatorially symmetric cross-validation (CSCV); the Deflated Sharpe Ratio† | |
| Discovery across time | α-investing (Foster and Stine†): each test spends "alpha-wealth", each discovery earns some back. It controls the marginal FDR (mFDR), "a weaker criterion than the false discovery rate", not the probability of any false discovery | [I] A natural ledger for a lab that tests hypotheses every IC cycle; Holm controls the FWER within each contract |
| Simulation optimization | CRN; ranking-and-selection (Kim and Nelson†); successive halving and Hyperband (Li et al.†); knowledge gradient (Frazier et al.†) | |

### 2.7 Safety patterns from control theory and banking [†/I]

- **Simplex / run-time assurance** (Sha†): a high-performance but unverified controller operates inside an envelope enforced by a simple, verified safety controller, with switching logic between them. For ADIC:
  - the complex controller is the LLM-discovered policy;
  - the safety controller is the Tier-1 gate plus a fallback policy (status quo or static SAA);
  - the switching logic is the early-warning triggers.
- **Maker-checker** and the **three lines of defence** map to: author agent → independent auditor agent and model risk management (MRM) → internal audit.
- **Solvency II's "use test"** (Art. 120†) maps to logging whether the IC used, modified or overrode the lab's output.

### 2.8 Human-AI configuration

- [F] Failure tendencies:
  - NIST AI 600-1 lists "Human-AI Configuration" (automation bias, over-reliance) and "Confabulation" among its 12 GAI risks;
  - assistants are sycophantic (Sharma et al.);
  - verbalized confidence is overconfident (Xiong et al.);
  - LLM judges show position, verbosity and self-enhancement bias (Zheng et al.).
- [†/I] Decision-science counterweights, used in §6.7:
  - dialectical inquiry and devil's advocacy beat consensus (Schweiger et al.);
  - the "hidden profile" effect (Stasser and Titus);
  - pre-mortems (Klein);
  - calibrated likelihood language (IPCC AR5).

---

## 3. Methods/models and trade-offs

### 3.1 Orchestration and search patterns

| Pattern | Exemplars [F] | Failure modes | ADIC use [I] |
|---|---|---|---|
| Template pipeline | AI Scientist v1 (under $15 per paper) | Naive ideas, hallucinated numbers (Beel et al.) | No |
| Agentic tree search | AI Scientist v2 (experiment manager) | Coding failures, compute sprawl | Post-hoc diagnostics only |
| Generate-debate-evolve tournament | Co-scientist (Supervisor, Generation, Reflection, Ranking/Elo from 1200, Proximity, Evolution, Meta-review) | Elo is self-assessed, not ground truth | Triage of *qualitative* hypotheses |
| Evolutionary program search | FunSearch, AlphaEvolve, ShinkaEvolve (state-of-the-art circle packing in 150 samples), EoH | Goodhart on the evaluator | **Core**: PolicySpec search |
| Bandit-scheduled R&D | RD-Agent(Q) ("up to 2X" annualized return, 70% fewer factors) | Backtest overfitting | Effort across idea families |
| Shared world-model memory | Kosmos (12-hour runs) | Errors accumulate in memory | Lab notebook with provenance |
| Orchestrator-workers | Anthropic research system (+90.2%) | Duplicated work; lead-prompt sensitivity | Ideation, evidence |
| Evaluator-optimizer | Anthropic; Managed Agents "outcomes" | Judge bias, rubric gaming | Memo drafting |
| Bull/bear debate | TradingAgents, AlphaAgents, FinCon | Persona theatre; debate does not reliably beat self-consistency (Smit et al.) | IC preparation only, **never** the decision |

[F] Two further findings from *The Agentic Scientist*:
- The base coding agent materially changes search cost and generalization. One agent cut API costs by 75% at similar scores.
- Rubrics "check only the criteria they enumerate".

The design brief records the further reading that 2–4 parallel workers sharing distilled conclusions suffice.

### 3.2 Verification mechanisms

| Mechanism | Strength | Weakness | ADIC role [I] |
|---|---|---|---|
| Deterministic evaluator (immutable, hashed) | Objective, reproducible | Exploitable if editable: METR found o3 reward-hacked 30.4% of RE-Bench runs [F] | Owns every number |
| Rubric gates implemented as tests | Cheap, auditable | Blind to unenumerated constraints [F] | Constraint and implementation rubrics |
| LLM judges | Nuance, scale | Biased; GPT-4 as judge reached "over 80% agreement" with humans on chat tasks [F]; must be calibrated | One isolated judge per dimension, with an "unknown" option [F: Anthropic evals] |
| Multi-model review | Dilutes single-judge quirks | Judges can diverge: one judge correlated ρ≈0.32 with the others, which agreed at ρ≈0.91 [F] | Cross-family auditor |
| Human subject-matter experts / MRM | Gold standard | Slow | Gate G8 and judge calibration |

### 3.3 Tool grounding and the ACI

**Anthropic's tool-writing guidance** [F]:
- Write a few consolidated, workflow-level tools rather than thin wrappers around API endpoints.
- Namespace the tools.
- Return high-signal fields. Resolving UUIDs to names reduced hallucination.
- Offer a `response_format` parameter (concise or detailed).
- Paginate and truncate. Claude Code caps tool responses at 25,000 tokens by default.
- Write actionable error messages.
- Iterate against held-out evaluations.

**Code execution with MCP** [F]:
- Agents call tools from sandboxed code, so intermediate data never enters the model's context.
- One workflow fell from about 150k to 2k tokens (−98.7%).
- Sensitive fields can be tokenized before the model sees them.
- The cost is a hardened sandbox.

**MCP 2026-07-28** [F]:
- Stateless: no sessions or `initialize` handshake; servers mint explicit handles passed as tool arguments; a new `server/discover` method.
- Tasks (durable requests, polled via `tasks/get`) move to an official extension.
- **Multi Round-Trip Requests** (`input_required`) replace server-initiated requests.
- Roots, Sampling and Logging are deprecated.
- OpenTelemetry trace context travels in `_meta`; deterministic `tools/list` ordering helps cache hits.

[I] This maps cleanly onto the lab:
- `run_id` and `scenario_set_id` are the explicit handles;
- a 10,000-path evaluation runs as a Task;
- an IC member's confirmation of a ScenarioSpec is a Multi Round-Trip elicitation.

### 3.4 Cost and latency control

- [F] Agents use about 4× the tokens of chat; multi-agent systems about 15×. Token usage alone explains 80% of performance variance on BrowseComp. Anthropic recommends scaling effort to query complexity: 1 agent and 3–10 tool calls for simple fact-finding, more than 10 subagents for complex research. Subagents should return condensed summaries of "1,000-2,000 tokens" and leave artifacts on the filesystem.
- [F] Pricing, per the Anthropic SDK reference cached 2026-10-06:

  | Item | Opus 5.5 |
  |---|---|
  | Input | $4 per million tokens |
  | Cache read | $0.20 per million tokens |
  | Output | $20 per million tokens |
  | 5-minute cache writes | ~1.25× input price |
  | 1-hour cache writes | ~2× input price |
  | Message Batches | 50% discount (first-party API and Claude Platform on AWS only) |

- [I] A full research cycle of about 2M input tokens (70% cached) plus 0.3M output tokens costs about $9. The scarce resources are evaluator CPU, the **counted evaluation budget** (statistical degrees of freedom), and IC attention, not tokens.

### 3.5 Frameworks (status as of October 2026)

| Option | What it is [F] | Durable state / HITL | Sovereign fit [I] | Recommendation [I] |
|---|---|---|---|---|
| Anthropic SDK: tool runner, `strict: true` tools, `messages.parse(output_format=Model)` | Thin harness; you own the loop. Strict tools and prompt caching are available on the first-party API, Claude Platform on AWS, Bedrock, Vertex and Foundry | You build it | Best: smallest surface | **Core** |
| Claude Agent SDK | Claude Code's harness as a library: built-in tools, hooks, subagents, permissions, sessions (resume and fork), MCP | Sessions, hooks | Good when self-hosted with a sandbox | "Analyst-Coder" role only |
| Claude Managed Agents (beta) | Hosted loop and sandbox; a self-hosted sandbox is possible, but "Tool inputs and outputs still flow to Anthropic's control plane" | Managed | Check against data policy | Non-sensitive pilots |
| LangGraph 1.x | Graph state machine; checkpointers (Postgres), interrupts, time travel | Strong | Open source, any provider | Optional backbone |
| Microsoft Agent Framework | "Direct successor" to Semantic Kernel and AutoGen: agents, graph workflows, sessions, middleware, telemetry; supports Anthropic models | Strong | Good in Azure estates | Alternative backbone |
| OpenAI Agents SDK | Agents, handoffs, guardrails, sessions, built-in tracing; non-OpenAI providers supported | Sessions | Verify where traces are exported | Viable for multi-provider setups |
| CrewAI | Flows (backbone) plus Crews (role-playing teams) | Flow state | Enterprise claims unverified | Not for the core |

---

## 4. Empirical evidence and current market data (dated)

| Date | Finding [F] | Implication [I] |
|---|---|---|
| Aug 2024 | AI Scientist v1 produces a full paper "at a cost of less than $15 per paper" | Generation is cheap; verification is the cost |
| Feb–Oct 2025 | Independent test of v1: 5 of 12 experiments (42%) failed on coding errors; hallucinated numbers | Sandbox plus numeric validation |
| Apr 2025 / Mar 2026 | v2: 1 of 3 papers above a workshop threshold (6, 7, 6), withdrawn by design; the workshop "had an acceptance rate of 70%" (*Nature* abstract); *Nature* paper: reviewer balanced accuracy 69% | LLM review is a noisy filter |
| Feb 2025 → Jun 2026 | Co-scientist: top-Elo answers reach 78.4% top-1 accuracy on GPQA; "no evidence of performance saturation" in Elo; published in *Nature* 2026 | Tournaments rank plausibility, not truth |
| May 2025 | AlphaEvolve: 0.7% of fleet compute recovered; 23% kernel speedup (1% of Gemini training time); 48-multiplication 4×4 complex matrix multiplication | Search works with exact verifiers |
| Nov 2025 | Kosmos: 79.4% of statements accurate, although every statement is cited to code or primary literature; a 20-cycle run ≈ 6 months of collaborators' research time | About 1 in 5 autonomous statements are wrong. Citation coverage is necessary but not sufficient: G6 (claim validation) needs G7 (independent review) behind it |
| Jun 2025 | Ideation-execution gap: 43 experts each spent 100+ hours executing ideas; after execution, LLM ideas' scores fell significantly more than human ideas' | Never promote on idea quality alone |
| Jun 2025 | METR: o3 reward-hacked in 39 of 128 RE-Bench runs; telling it not to cheat had a "nearly negligible effect" | Isolate the evaluator |
| Oct 2026 | *Agentic Scientist*: in 2 of 3 runs an agent switched the evaluation to k-sample majority voting instead of pass@1; it was found only by manual post-hoc audit | Immutable, hashed evaluation protocol |
| Jan 2026 | Anthropic evals guidance: start with 20–50 tasks drawn from real failures; Opus 4.5 scored 42% on CORE-Bench before grading bugs were fixed, 95% after | Evaluate the evaluator |
| Nov 2023 | FinanceBench: GPT-4-Turbo with retrieval answered incorrectly or refused 81% of questions | Never source numbers by retrieval QA |
| Jun 2026 | Vals Finance Agent v1.1: best model 64.37%, at $0.80 per test | About one-third failure on analyst tasks |
| 2024–25 | TradingAgents: Jan–Mar 2024 back-test, Sharpe 8.21 (AAPL) | Short windows mislead |
| 2025 (arXiv); KDD 2026 | FINSABER: LLM strategies too conservative in bull markets, too aggressive in bear markets | Long, survivorship-free tests |
| 2025 | MarketSenseAI 2.0: 125.9% vs 73.5% cumulative return (S&P 100, 2023–24; abstract-level) | Bull-market window; caution |
| Apr–Dec 2025 | Memorization: masking fails; "post-cutoff, we observe no recall" | Test only after the cutoff |
| Feb 2025 | Kim–Muhn–Nikolaev GPT-4 financial-statement paper withdrawn | Check literature status |
| 2026 | Shared-retrieval overlap 0→1 raises action correlation 0.04→0.41 | Diversify challengers' evidence |
| Sep 2026 | Correlated behaviour rises with capability and becomes a liability under shared misinformation (Ross, So, De Simone, Pozniak, Lo) | Cross-family review |

---

## 5. Practitioner and peer practice

**NBIM (Norway's GPFG)** [F]
- 600+ active Claude users within two months; more than 20% weekly time saved (internal surveys).
- MCP connections to Snowflake; ESG analysis across about 9,000 companies.
- "Humans remain central to all decisions." In March 2026 AI could not yet make investment decisions, though the AI director expects agents eventually to make some under monitoring.
- *Lesson* [I]: reach the governed warehouse through tools, measure productivity, keep decision rights human.

**Man Group AlphaGPT** [F]
- Idea generator, implementer, evaluator and orchestrator, with full logging.
- The evaluator applies significance tests, risk checks, a "clear economic rationale" test and p-hacking controls; the IC reviews hypotheses and outcomes.
- AI ideas face human thresholds; "several dozen" signals went live (Hedgeweek, July 2025).
- Observed failures: hallucination, and "conceptualise one idea but implement another".
- *Lesson* [I]: equal thresholds, plus an implementation-fidelity check of each IdeaBundle against the PolicySpec executed.

**Unnamed Abu Dhabi sovereign wealth fund** [F] (SIF panel, 14 Oct 2026)
- AI tests investment proposals by "presenting why they shouldn't invest".
- Human reviewers check for inaccuracies and improper data use.
- *Lesson* [I]: there is local precedent for an institutional challenger role.

**BlackRock AlphaAgents** [F]
- Fundamental, sentiment and valuation agents debate.
- Debate helps when signals conflict.
- The authors call it "not yet a full portfolio optimization engine".
- FinCon's NeurIPS slides likewise describe an external optimization solver for portfolio management.

**Bridgewater AIA Labs** (secondary only): an ML-driven fund of about $2bn; humans keep risk controls and a kill switch.

**Open-source "AI hedge fund" (virattt)** [F]: 64.1k GitHub stars; "educational and research purposes only"; it makes no trades. *Lesson* [I]: persona agents are popular, but popularity is not evidence of skill.

**Consensus** [C]
- Agents accelerate research and challenge.
- Deterministic tests and human checkpoints gate anything that touches capital.
- I found no public evidence, as of October 2026, of any asset owner delegating allocation decisions to LLM agents.

---

## 6. Design implications for the ADIC framework

### 6.1 Reference architecture [I]

```
+------------------------------ HUMAN DECISION PLANE -------------------------------+
| CIO/IC sign AnalysisContract (G0) | MRM validates engines | IC decides + logs (G8) |
+--------------^---------------------------------------------------^---------------+
               | contract, approvals                               | IC pack, decisions
+--------------+----- META-CONTROLLER (deterministic Python) -------+---------------+
| state machine | budgets: $, eval count, alpha-wealth, wall-clock | successive-    |
| halving allocator | gates G1-G7 | checkpoints/retries | lab notebook | escalation |
+------^--------------------------^--------------------------^---------------------+
       | typed specs              | run_ids / metrics         | claims / issues
+------+------------- LLM ROLE PLANE (bounded, strict schemas) ---------------------+
| Contract Drafter | Ideators x2-4 (read-only) | Planner | Red Team | Analyst-Coder |
| (sandbox) | per-dimension Judges | Auditor (cross-family) | Memo Writer | IC Facil.|
+------^---------------------------------------------------------------------------+
       | tool calls (Pydantic -> JSON Schema 2020-12; in-process runner + MCP server)
+------+------------- TOOL PLANE (no tool can write engine/evaluator code) ----------+
| evaluate_policy | run_scenario | optimize_here_and_now | attribute | fuse_beliefs |
| price_action | overlay_margin | query_corpus | get_metric | validate_claims | issue|
+------^---------------------------------------------------------------------------+
+------+------------- DETERMINISTIC ENGINE PLANE (versioned, content-hashed) -------+
| scenario generator | PE cash-flow | belief fusion | action economics | overlay &  |
| collateral | liabilities | simulator | optimizer + duals | misspec ensemble | eval |
+------^---------------------------------------------------------------------------+
+------+------------- DATA & PROVENANCE PLANE --------------------------------------+
| holdings/cash flows | market data | memo corpus (chunk hashes) | scenario library |
| run registry + manifests | metric registry | claim ledger | issue log | decision  |
| log | model inventory | LLM cassettes (prompt-hash -> response)                    |
+-----------------------------------------------------------------------------------+
```

**Control loops**

| Loop | Timescale | What happens |
|---|---|---|
| Inner | Seconds | Tool calls within an agent episode |
| Middle | Hours | One research cycle per contract |
| Outer | Quarterly | IC decisions → outcomes → engine recalibration, scenario-library updates, regression evals |
| Governance | Annual | MRM validation; ISO 42001 management review |

### 6.2 Agent roster and typed contracts

| Role | Tools (permissions) | Output | Gate |
|---|---|---|---|
| Contract Drafter | Read corpus; list scenario sets | `AnalysisContract` draft | G0 (human signs) |
| Ideators ×2–4, each given a different evidence slice | Read-only: corpus, search-set metrics | `IdeaBundle` {id, falsifiable hypothesis, PolicySpec, plan, ≥1 metric rubric, ≥1 constraint rubric, family, parents} | G1–G2 |
| Planner | Baseline list; cost estimator | `ExperimentPlan` {baselines, ablations, $n_0$, η, seeds} | G1 |
| Red Team | Propose bounded `ScenarioSpec`s; retrieve failure analogues | Issues; stress register | Disclosed at G7 |
| Analyst-Coder | Sandbox; read-only frozen artifacts; no network | Diagnostics whose numbers come via the registry | G6 |
| Judges (one per dimension) | None | Score or "unknown" | G7 |
| Auditor (different model family) | Read registry and ledger | Overclaim and contradiction report | G6–G7 |
| Memo Writer | `get_metric`, `validate_claims` | Memo of `Claim`s | G6 |
| IC Facilitator | Draft `ScenarioSpec` / `ViewSpec`; confirmation via Multi Round-Trip Request | Q&A log, issue list | Human confirmation |

**Other contracts**
- `ScenarioSpec` = {base_set, overrides[factor, shape, magnitude, start_q, duration_q], plausibility_class, requester, confirmed}.
- `ViewSpec` = {variable, type (mean, quantile or probability), value, confidence, holder}.

**Model defaults** [I]
- Use Opus 5.5 for every role, with explicit effort: high for the Planner and Auditor, medium for the others.
- Downgrading high-volume extraction roles to cheaper tiers should be an evaluation-backed decision, not a default.
- Draw the Auditor from another model family. SR 26-2 itself warns of aggregate risk from "reliance on common assumptions, data, or methodologies".

### 6.3 Lab state, decisions, constraints, objective

**State** $S_t$:
- contract hash $h_C$;
- stage $\sigma_t$;
- hypothesis pool $\mathcal H_t$ (PolicySpec, lineage, QD descriptors, $\hat F$, SE, LCB);
- evaluation counters $N^{\rm search}_t$ and $N^{\rm final}_t$;
- alpha-wealth $W_t$;
- spend $\$_t$;
- run registry $\mathcal R_t$;
- claim ledger $\mathcal L_t$;
- issue log $\mathcal I_t$;
- notebook $Z_t$;
- version pins $V$ (engine SHA, LLM IDs).

**Decisions:**
- which ideas to screen, $x_i\in\{0,1\}$;
- path allocations $n_i$;
- which ideas to promote to the final set, $y_i$, with $\sum_i y_i\le K_{\rm final}$;
- review passes;
- escalation $e\in\{$continue, ask human, stop$\}$.

**Constraints:**
- $\$_t\le B_\$$ and $N^{\rm search}\le B_{\rm eval}$;
- the final set is **sealed and single-use**, and ideators never see final results before closure;
- every evaluated $x$ passes G2;
- $W_t\ge0$.

**Objective (meta-level):**

$$\max\ \mathbb E\big[F(\pi^\star)-F(\pi_0)\big]-\lambda_\$\,\$_T\quad\text{s.t. }\ \mathrm{FWER}_{\text{within contract}}\le\alpha\ \text{(Holm)},\quad\mathrm{mFDR}_{\text{across contracts}}\le\alpha\ (\alpha\text{-investing})$$

[corrected 2026-10-18: the constraint was Pr(false promotion) ≤ α, which matches neither mechanism. α-investing (Foster and Stine†) controls mFDR, "a weaker criterion than the false discovery rate", so over many IC cycles P(≥1 false promotion) can exceed α. The two error criteria are now named.]

**State machine:**
DRAFT → SIGNED → IDEATION ⇄ SCREENING (halving rounds) → SELECTION → FINAL (sealed) → ANALYSIS (on the frozen policy) → REVIEW → MEMO → IC → CLOSED.

- Any gate failure returns the run to IDEATION if budget remains; otherwise it ESCALATEs to a human.
- **"Not established" is a first-class outcome.** It means no candidate robustly beats the status quo, and reporting it relieves the pressure to manufacture a winner.

### 6.4 Core equations and default parameters [I unless noted]

1. **Robust fitness across the misspecification ensemble** (entropic, equivalently KL-robust):
   $$F_\tau(\pi)=-\tau\ln\sum_{m\in\mathcal M}w_m e^{-\hat J_m(\pi)/\tau}=\min_{q\in\Delta(\mathcal M)}\Big\{\textstyle\sum_m q_m\hat J_m(\pi)+\tau\,\mathrm{KL}(q\Vert w)\Big\}$$
   - The second form is the Gibbs variational identity.
   - $\tau\to0$ gives the worst model; $\tau\to\infty$ gives the $w$-weighted mean.
   - Hard Tier-1 condition: for every $m$, $\Pr_m(R_{5y}<7\%)\le5\%$ and liquidity survival holds.
   - Defaults: uniform $w$ (IC may override through ViewSpecs); $\tau=0.5$pp; report $\tau\in\{0.25,0.5,1,\infty\}$.

2. **Successive halving under CRN:** round $r$ evaluates survivors on $n_r=n_0\eta^r$ paths (reusing the first $n_{r-1}$) and keeps the top $\lceil|\mathcal H_r|/\eta\rceil$ by $\mathrm{LCB}_i=\hat F_i-z_{0.90}\widehat{\rm SE}_i$, not by point estimate. Defaults: $n_0=1{,}000$, $\eta=3$, three rounds. For 27 ideas: 27×1k + 9×3k + 3×9k = 81k path-evaluations, versus 729k naive.

3. **Sealed final test:** $K_{\rm final}\le3$; 50,000 paths per $m$ on held-out families; paired $D_i=J_i(\pi)-J_i(\pi_0)$ on identical paths; $t=\bar D/(s_D/\sqrt N)$, Holm-adjusted at $\alpha=0.05$, which controls the family-wise error rate (FWER) within the contract (item 6 gives the across-contract criterion).

4. **PBO gate** (Bailey et al.†): split the search set into $S=16$ blocks ($\binom{16}{8}=12{,}870$ splits). For each split $c$, take the in-sample winner's out-of-sample relative rank $\bar\omega_c$: $\lambda_c=\ln\frac{\bar\omega_c}{1-\bar\omega_c}$, $\mathrm{PBO}=\frac1{|C|}\sum_c\mathbb 1[\lambda_c\le0]$. Gate: PBO ≤ 0.20.

5. **Deflating search-set claims** (Deflated Sharpe logic†), with $N$ from the registry's evaluation counter:
   $$\mathbb E[\max_{\rm null}]\approx\hat\sigma_\Delta\Big[(1-\gamma)\Phi^{-1}(1-\tfrac1N)+\gamma\Phi^{-1}(1-\tfrac1{Ne})\Big],\quad\gamma\approx0.5772$$
   At $N=200$ this is ≈2.76 $\hat\sigma_\Delta$: a "best of 200" below ~2.8 SD is noise.
   - **Non-normality term** [corrected 2026-10-18: the Deflated Sharpe Ratio (Bailey and López de Prado†) corrects for selection bias *and* non-normality; the expected-maximum term above is only the selection part]. Test the selected candidate against that benchmark with
     $$\mathrm{DSR}=\Phi\!\left(\frac{(\widehat{SR}-SR_0)\sqrt{T-1}}{\sqrt{1-\widehat{\rm skew}\cdot\widehat{SR}+\frac{\widehat{\rm kurt}-1}{4}\,\widehat{SR}^{2}}}\right)$$
     where $\widehat{SR}$ is the mean over the standard deviation of the candidate's per-path paired improvements, $T$ is the number of paths, $\widehat{\rm skew}$ and $\widehat{\rm kurt}$ are their skewness and (non-excess) kurtosis, and $SR_0$ is the expected null maximum above with $\hat\sigma_\Delta$ replaced by the cross-candidate standard deviation of $\widehat{SR}$. Negative skew and fat tails lower the DSR. [I] G5 counts the deflated improvement as passed only if DSR ≥ 1 − α.
   - **Shrink reported estimates** [corrected 2026-10-18: Smith and Winkler's† remedy for the optimizer's curse (§2.2) was cited but not applied]. Before any search-set or final-set estimate enters a memo, report the Bayesian posterior mean $\tilde F_i=\mu_0+\kappa_i(\hat F_i-\mu_0)$ with $\kappa_i=\sigma_0^2/(\sigma_0^2+\widehat{\rm SE}_i^2)$, where $\mu_0$ and $\sigma_0^2$ are the prior mean and variance of true improvements. [I] Estimate them across the screened pool, or from ADIC's underwritten-versus-actual records. Selecting on LCBs and sealing the final set reduce the curse but do not remove it from reported values.

6. **α-investing across IC cycles** (Foster and Stine†): $W_0=0.05$. Test $j$ at $\alpha_j\le W_{j-1}/(1+W_{j-1})$. A rejection ("robustly superior") pays $\omega=0.05$; otherwise $W_j=W_{j-1}-\alpha_j/(1-\alpha_j)$. **Error criterion** [corrected 2026-10-18]: the ledger controls mFDR across contracts (expected false promotions relative to expected promotions), not the probability of any false promotion; within a contract, item 3's Holm test controls the FWER.

7. **Monte Carlo precision:** $N\ge z^2(1-p)/(\varepsilon^2p)$. That is ≈7,300 paths for $p=5\%$, $\varepsilon=10\%$, and ≈38,000 for $p=1\%$. The deck's 2% breach estimate on 50k paths has a 95% CI of ±0.12pp.

8. **Qualitative tournaments only:** $E_A=1/(1+10^{(R_B-R_A)/400})$, $R_A\leftarrow R_A+32(S_A-E_A)$, starting at 1200 as in co-scientist [F]. Never use Elo for anything the evaluator can compute.

9. **Judge admission:** Cohen's $\kappa\ge0.6$ against subject-matter experts on ≥50 golden items. Reliability is pass^k = $p^k$ [F]. NL→ScenarioSpec translation needs pass^3 ≥ 0.9, i.e. $p\ge0.965$.

10. **Evidence coverage:**
    $$c=\frac{\#\{\text{numeric claims resolving to the registry within rounding}\}}{\#\{\text{numeric claims}\}}=1$$

11. **Idea-family scheduler** (in the spirit of RD-Agent(Q)'s bandit [F]):
    - UCB1 rule: $a_t=\arg\max_a\hat\mu_a+\sqrt{2\ln t/n_a}$.
    - Families: secondaries, NAV/preferred financing, overlay, pacing, distribution rule.
    - Reward: the improvement in LCB.

### 6.5 Verification gates

| Gate | Check | Pass criterion |
|---|---|---|
| G0 Contract | Objective, constraints, actions, metric IDs and scenario-set hashes signed by humans | Frozen hashes and signature |
| G1 Schema | Strict-tool / Pydantic parse | 100%; invalid input is returned as a tool *execution* error so the agent can self-correct |
| G2 Admissibility | DSL type-check (non-anticipativity); parameter bounds; ≤25 nodes and ≤8 parameters; novelty against the library | All pass |
| G3 Tier-1 rubric | Floor and liquidity under every $m$ (search set) | All pass |
| G4 Selection | LCB of $F_\tau$ strictly above the incumbent's | Strict improvement |
| G5 Final | Sealed set plus ensemble; Holm-adjusted paired test; PBO; deflated improvement | Pass, otherwise "not established" |
| G6 Evidence | Claim validator; citations resolve to chunk hashes; likelihood words match the probabilities | $c=1$ |
| G7 Review | Isolated judges, cross-family auditor, red-team issues | No open critical issue |
| G8 Human | MRM sign-off on engine changes; IC approve / resize / defer; overrides logged | Recorded |

### 6.6 AlphaEvolve-style policy search: safeguards [I]

1. **PolicySpec is a JSON abstract syntax tree, never free code.** It uses Pydantic discriminated unions with these node types:
   - `Predicate(var, op, θ)` and `And` / `Or` / `Not`;
   - `Action(selector, SELL{frac, channel} | HOLD | REFI{instrument, LTV, tenor} | LEVER{Δ, instrument})`;
   - `Overlay{hedge_ratio, notional_cap}`;
   - `Pacing{rule}`.

   Every variable carries its information lag.
2. **Diversity:** a MAP-Elites† archive over turnover, peak liquidity use, leverage, overlay notional and action mix; novelty rejection (as in ShinkaEvolve [F]); 2–4 islands.
3. **Disjoint families:** search on bootstrap and HMM regimes; finalize on structurally different generators (DPI drought, oil-revenue shock) plus the misspecification ensemble.
4. **Count every evaluation.** No runs outside the official evaluator; the count feeds G5 and the alpha ledger.
5. **Metamorphic tests**†: perturbations with a known economic direction. A wider secondary discount must not *increase* SELL volume, all else equal.
6. **Exploit hunt:** the Auditor looks for "too good to be true" mechanics, e.g. zero-cost or unlimited-capacity trades. Red-team ScenarioSpecs stay inside each generator's plausibility envelope.
7. **Historical replay** (2008–09, 2020, 2022): sanity check only, never selection.
8. **Simplex wrapper:** each adopted policy ships with a fallback $\pi_{\rm safe}$ and early-warning switching triggers.

### 6.7 IC deliberation module [I]

1. **Pre-commitment.** Members record priors before seeing results, e.g. P(DPI recovers within 8 quarters). Priors become ViewSpecs and Brier-scored track records ($BS=\frac1N\sum(f_i-o_i)^2$). This counters anchoring and the hidden-profile effect.
2. **The pack:** claim-linked memo, gate status, robustness map across $\mathcal M$, binding constraints and shadow prices, marginal value per action, and the counterfactual (what would flip the decision).
3. **Shadow-IC before the meeting.** Role agents (CRO, liquidity, PE, overlay) draw likely questions from the memo corpus, labelled *simulated*. **Dialectical inquiry:** thesis and antithesis memos, both from the same registry.
4. **Live what-if.** No number ever comes from model memory. The sequence is:
   1. a member asks in natural language;
   2. the Facilitator drafts a ScenarioSpec;
   3. it echoes the spec back in plain language, with a parameter table;
   4. the member confirms (Multi Round-Trip Request);
   5. the evaluator runs on cached CRN paths;
   6. the answer is returned with its provenance.
5. **Calibrated language.**
   - Probabilities are converted to words by deterministic lookup (IPCC-style bands†).
   - Each phrase carries its Monte Carlo CI and the range across the ensemble.
   - Example: "P(Tier-1 breach) 2.0% (MC 95% CI 1.9–2.1%; ensemble 1.2–4.6%): very unlikely".
6. **Sycophancy evals.** Scripted members push incorrect claims. The Facilitator must hold any position that the evidence supports.
7. **Decision record.**
   - Fields: decision (approve / resize / defer), conditions and triggers, dissent, overrides (the use test), review date.
   - Outcomes feed the corpus and the regression evals.

### 6.8 Provenance and reproducibility

The **run manifest** records: `run_id`, `parent_ids`; engine git SHA and source hash; evaluator and metric-definition versions; config, scenario-set and PolicySpec hashes; `SeedSequence` entropy and spawn keys; data-snapshot IDs and library versions; per LLM call, model ID, prompt and response hashes, tokens and cost; agent role and human approvals. It maps onto W3C PROV (Entity / Activity / Agent)† and OpenTelemetry traces.

[F] Opus 5.5 returns HTTP 400 for `temperature` / `top_p` / `top_k`. [I] Agent runs are therefore reproduced from **record/replay cassettes**, and offline tests use the stub backend (design brief P12).

### 6.9 Governance mapping

**Engines are "models"** [F] under SR 26-2 (a "complex quantitative method, system, or approach" yielding quantitative estimates). Tier them by inherent risk × materiality, with effective challenge, conceptual soundness, outcomes analysis, ongoing monitoring and an inventory.

**LLM roles.** SR 26-2 excludes generative and agentic AI, though it says "risk management and governance practices should guide" their controls [F]. Use the NIST AI RMF (Govern, Map, Measure, Manage), the NIST AI 600-1 risks (confabulation, human-AI configuration, information security, homogenization, value chain) and an ISO/IEC 42001 management system.

**Materiality tiers** [I]:

| Tier | Roles | Reason |
|---|---|---|
| High | IC Facilitator, Planner | Mistranslations reach decisions; the Planner shapes contract fidelity |
| Medium | Memo Writer, Auditor | |
| Low | Ideators | Their ideas reach numbers only through G2–G5 |

**Model upgrades** are re-validation events: run the regression suite and keep versions pinned.

**UAE context** [F]:
- The UAE AI Charter (issued June 2024) sets 12 principles, including human oversight and governance and accountability.
- The CBUAE guidance for licensed financial institutions (February 2026) expects board and senior-management accountability, and lets consumers request human review or explanation of AI decisions.
- Abu Dhabi has an AI and Advanced Technology Council (AIATC).
- Abu Dhabi's Digital Strategy 2025–27 targets an AI-native government by 2027, sovereign-cloud-first (secondary sources).
- [I] Implications: host in-region, minimize data in prompts, and document human decision rights.

**Security** [F/I]:
- OWASP LLM01 (prompt injection) and LLM06 (excessive agency) both apply.
- Avoid the "lethal trifecta" of private data, untrusted content and external communication in one agent.
- Agents that read GP documents get no outbound tools and emit only typed extractions, in the spirit of CaMeL's separation of control flow from data flow. [F] CaMeL solved 77% of AgentDojo tasks with provable security, against 84% undefended: a modest utility cost.
- Web access is off by default.

### 6.10 Pattern and anti-pattern catalogue

| Pattern (do) | Anti-pattern (avoid) | Evidence |
|---|---|---|
| Deterministic engines own numbers; claim validator | LLM states or "remembers" figures | FinanceBench 81%; Vals 64%; Kosmos 79% |
| Immutable, hashed evaluator; read-only tools | Agents can edit evaluation code or protocol | METR 30%; *Agentic Scientist* 2 of 3 runs |
| Sealed held-out families plus ensemble | Selecting and reporting on the same scenarios | Optimizer's curse; PBO |
| Counted budget, deflation, alpha ledger | Best-of-N reported without N | Man Group; DSR |
| Elo only for qualitative triage | LLM tournaments to rank computable metrics | Co-scientist Elo is self-assessed |
| Dialectical prep with diverse evidence | Persona debate as the decision rule | Smit et al.; herding 0.04→0.41 |
| Post-cutoff, long-horizon tests of any LLM signal | Back-testing LLMs on in-training periods | Memorization papers; FINSABER |
| Workflow-first, thin framework | Opaque framework abstractions | Anthropic guidance |
| Record/replay cassettes | Assuming temperature-0 determinism | Opus 5.5 rejects sampling parameters |
| Quarantined document extraction | Lethal-trifecta agents | Willison; CaMeL |

### 6.11 Calibration targets, data needs, runtime phases

**Targets:**
- evidence coverage = 1.0;
- judge κ ≥ 0.6 (strong judges reach >80% human agreement);
- auditor recall ≥ 95% on memos seeded with errors;
- translation pass^3 ≥ 0.9;
- PBO ≤ 0.2;
- an initial evaluation suite of 20–50 tasks [F];
- a token budget of about $50 per cycle soft and $200 hard [I].

**Data needs:**
- the 18-year memo corpus with outcomes;
- the history of IC decisions and overrides;
- golden numeric Q&A generated from the engines;
- NL→ScenarioSpec translation pairs;
- memos seeded with errors;
- prompt-injection test documents;
- a scenario library labelled by family;
- the policy library;
- the model inventory.

**Runtime phases:**
1. Synthetic data: first-party API, SQLite.
2. Real data: in-region/VPC endpoint (confirm UAE-region serving), Postgres, self-hosted tracing.
3. Add a cross-family auditor; add LangGraph or Agent Framework only if needed.

---

## 7. Implementation notes

**Anthropic SDK (`anthropic` 1.15, per the design brief)**
- Use `messages.parse(..., output_format=Model)`. Raw `output_format={...}` dictionaries are deprecated in favour of `output_config={"format":...}`.
- Strict tools need `additionalProperties:false` and an explicit `required` list.
- Opus 5.5 rejects forced `tool_choice`. Use `auto` plus an explicit instruction.
- Set `effort` explicitly; Opus 5.5 defaults to medium.
- Parse tool inputs with `json.loads`.

**Prompt caching**
- Freeze system prompts and keep the tool list in a deterministic order.
- Put timestamps and IDs after the last cache breakpoint.
- Check `cache_read_input_tokens` to confirm that caching is working.

**Algorithms and cost**

| Component | Cost / approach |
|---|---|
| Successive halving | $O(\sum_r|\mathcal H_r|\,n_r)$ path-evaluations |
| CSCV (for PBO) | $O(\binom{S}{S/2}K)$; trivial at $S=16$ |
| Exact Shapley | Up to 6 components ($2^6=64$ coalitions) |
| Shapley beyond 6 components | Permutation sampling with CRN |
| UCB1, Elo | $O(1)$ per update |

**Windows:** spawn-based multiprocessing pickles arguments, so share scenario arrays via `numpy.memmap`; pin BLAS threads for bitwise-reproducible reductions.

**CRN:** one `SeedSequence` per contract, with spawn keys indexed by (family, path) so every candidate sees identical paths.

**MCP 2026-07-28:** build without sessions, Sampling or Roots; pass handles explicitly; return validation failures as tool execution errors; confirm the installed `mcp` 2.3 SDK implements this revision.

**Testing:** `hypothesis` for property-based and metamorphic tests; golden sets as regression suites on every model, prompt or tool change; a clean environment per trial; read transcripts.

**Pitfalls**
- Tokenizer changes between models: re-baseline costs with `count_tokens`.
- Silent cache invalidation from volatile text.
- Grader bugs: CORE-Bench went from 42% to 95% once the graders were fixed [F].

---

## 8. Risks, pitfalls and limitations

| # | Risk | Mitigation |
|---|---|---|
| 1 | Evaluator misspecification (Goodhart): the dominant risk | Misspecification ensemble, out-of-family final sets, red-team stress |
| 2 | Reward hacking and evaluator tampering, empirically common [F] | Immutability, hashing, read-only tools |
| 3 | Overfitting to scenario sets | Counted budgets, PBO, sealed final set |
| 4 | Confabulated numbers in narrative | Gate G6 |
| 5 | Automation bias and sycophancy at IC | Pre-commitment, dialectical memos, sycophancy evals |
| 6 | Homogenization and herding | Diverse evidence slices, cross-family audit |
| 7 | Prompt injection; loss of data sovereignty via Managed Agents tool I/O or trace exporters | Quarantined extraction, in-region hosting, self-hosted traces |
| 8 | Look-ahead in LLM forecasts on in-training periods | Post-cutoff tests only |
| 9 | Vendor and model churn | Version pins, regression suites, provider-agnostic adapter |
| 10 | Rigour theatre: gates that pass by construction | Seeded-fault drills, independent audit |
| 11 | Regulatory drift: SR 26-2 excludes generative AI; a planned AI RFI, the NIST RMF revision and ISO 42001's "38 controls" are from secondary sources | Track regulation; re-map controls |

**Limitations of this dossier:** web search was exhausted; framework GA dates and the Bridgewater details are secondary; † references were not re-fetched.

---

## 9. Open questions

1. Is the chosen model served in a UAE region, and which ADIC data classes may enter prompts?
2. Which LLM roles does ADIC's risk function consider material, and who validates them?
3. Who sets the thresholds ($\tau$, PBO, κ, pass^k, $K_{\rm final}$) in the AnalysisContract?
4. With few independent PE cycles to back-test against, will MRM and the IC accept ensemble-based "verification" for the simulator?
5. Which second model family can serve as the cross-family auditor within sovereignty constraints?
6. Should AI-generated dissent enter the formal IC record, or only the pre-reads?
7. Should alpha-wealth reset per contract, per fiscal year, or never?
8. Given the tampering evidence, should the Analyst-Coder role exist, or should post-hoc diagnostics be pre-built tools?
9. How well do *The Agentic Scientist*'s ablation findings (reliable autonomy depends on the orchestration layer as well as on the base model) transfer to rung-4 verifiers? [corrected 2026-10-18: the paper does not find that orchestration matters more than the base model]

---

## 10. References

**Discovery systems and failure modes**
1. Lange, R.T., Grillotti, L., Yamada, Y., Charakorn, R., Ha, D. (2026). *The Agentic Scientist*. arXiv:2610.18933. https://arxiv.org/abs/2610.18933
2. Lu, C., Lu, C., Lange, R.T., Foerster, J., Clune, J., Ha, D. (2024). *The AI Scientist*. arXiv:2408.06292. https://arxiv.org/abs/2408.06292
3. Yamada, Y., et al. (2025). *The AI Scientist-v2*. arXiv:2504.08066. https://arxiv.org/abs/2504.08066
4. Lu, C., Lu, C., Lange, R.T., Yamada, Y., Hu, S., Foerster, J., Ha, D., Clune, J. (2026). Towards end-to-end automation of AI research. *Nature* 651(8107):914–919 (online 25 Mar 2026). DOI 10.1038/s41586-026-10265-5. Sakana AI blog post on the paper (2026-03-26): https://sakana.ai/ai-scientist-nature/
5. Beel, J., Kan, M.-Y., Baumgart, M. (2025). Evaluating Sakana's AI Scientist: Bold Claims, Mixed Results, and a Promising Future? *ACM SIGIR Forum* 59(1):1–20. DOI 10.1145/3769733.3769747. Preprint arXiv:2502.14297 (earlier versions carry a longer title). https://arxiv.org/abs/2502.14297
6. Gottweis, J., Weng, W.-H., Daryin, A., et al. (2025; rev. 2026). Accelerating scientific discovery with Co-Scientist. *Nature* 655(8122):487–496 (online 19 May 2026). DOI 10.1038/s41586-026-10644-y. arXiv:2502.18864. https://arxiv.org/abs/2502.18864 (HTML: https://arxiv.org/html/2502.18864v1)
7. Novikov, A., et al. (2025). *AlphaEvolve*. arXiv:2506.13131. https://arxiv.org/abs/2506.13131
8. Google DeepMind (2025-05-14). AlphaEvolve blog. https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
9. Romera-Paredes, B., et al. (2023). Mathematical discoveries from program search with LLMs. *Nature* 625:468–475. https://pmc.ncbi.nlm.nih.gov/articles/PMC10794145
10. Lange, R.T., Imajuku, Y., Cetin, E. (2025). *ShinkaEvolve*. arXiv:2509.19349. https://arxiv.org/abs/2509.19349
11. Liu, F., et al. (2024). Evolution of Heuristics. arXiv:2401.02051. https://arxiv.org/abs/2401.02051
12. Schmidgall, S., et al. (2025). *Agent Laboratory*. arXiv:2501.04227. https://arxiv.org/abs/2501.04227
13. Tang, J., Xia, L., Li, Z., Huang, C. (2025). *AI-Researcher*. arXiv:2505.18705. https://arxiv.org/abs/2505.18705
14. Ifargan, T., Hafner, L., Kern, M., Alcalay, O., Kishony, R. (2024). data-to-paper. arXiv:2404.17605. https://arxiv.org/abs/2404.17605
15. Mitchener, L., et al. (2025). *Kosmos*. arXiv:2511.02824. https://arxiv.org/abs/2511.02824
16. Ghareeb, A.E., et al. (2025). *Robin*. arXiv:2505.13400. https://arxiv.org/abs/2505.13400. Published as: A multi-agent system for automating scientific discovery. *Nature* 655(8122):497–505 (online 19 May 2026). DOI 10.1038/s41586-026-10652-y.
17. Li, Y., et al. (2025). *R&D-Agent-Quant* (NeurIPS 2025). arXiv:2505.15155. https://arxiv.org/abs/2505.15155
18. Si, C., Yang, D., Hashimoto, T. (2024). Can LLMs Generate Novel Research Ideas? arXiv:2409.04109. https://arxiv.org/abs/2409.04109
19. Si, C., Hashimoto, T., Yang, D. (2025). The Ideation-Execution Gap. arXiv:2506.20803. https://arxiv.org/abs/2506.20803
20. Von Arx, S., Chan, L., Barnes, B. (2025-06-05). Recent Frontier Models Are Reward Hacking. METR. https://metr.org/blog/2025-06-05-recent-reward-hacking/
21. Dharna, A., et al. (2026). *AI Finds A Way*. arXiv:2608.23875. https://arxiv.org/abs/2608.23875
22. Ravideshik, V.L., Kejriwal, M. (2026). Can AI Evaluate AI Scientists? arXiv:2607.28631. https://arxiv.org/abs/2607.28631

**LLM agents in finance**
23. Xiao, Y., Sun, E., Luo, D., Wang, W. (2024). *TradingAgents*. arXiv:2412.20138. https://arxiv.org/abs/2412.20138 (HTML v4: https://arxiv.org/html/2412.20138v4)
24. Yu, Y., et al. (2024). *FinCon*. NeurIPS 2024. https://proceedings.neurips.cc/paper/2024/hash/f7ae4fe91d96f50abc2211f09b6a7e49-Abstract-Conference.html
25. Yu, Y., et al. (2023). *FinMem*. arXiv:2311.13743. https://arxiv.org/abs/2311.13743. Published as: FinMem: A Performance-Enhanced LLM Trading Agent With Layered Memory and Character Design. *IEEE Transactions on Big Data* 11(6):3443–3459 (2025). DOI 10.1109/tbdata.2025.3593370.
26. Yang, H., et al. (2024). *FinRobot*. arXiv:2405.14767. https://arxiv.org/abs/2405.14767
27. Zhao, T., et al. (BlackRock) (2025). *AlphaAgents*. arXiv:2508.11152. https://arxiv.org/abs/2508.11152
28. Fatouros, G., et al. (2025). *MarketSenseAI 2.0*. arXiv:2502.00415. https://arxiv.org/abs/2502.00415
29. Li, W.W., Kim, H., Cucuringu, M., Ma, T. (2025; KDD 2026). Can LLM-based Financial Investing Strategies Outperform the Market in Long Run? (FINSABER). *Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.1* (KDD '26), pp. 2711–2722. DOI 10.1145/3770854.3785702. arXiv:2505.07078. https://arxiv.org/abs/2505.07078
30. Lopez-Lira, A., Tang, Y., Zhu, M. (2025). The Memorization Problem: Can We Trust LLMs' Economic Forecasts? SSRN 5217505; arXiv:2504.14765. https://papers.ssrn.com/abstract=5217505
31. Gao, Z., Jiang, W., Yan, Y. (2025; v2 2026). Detecting Lookahead Bias in LLM Forecasts. arXiv:2512.23847 (v1, 29 Dec 2025, titled "A Test of Lookahead Bias in LLM Forecasts"; v2, 12 Jun 2026). https://arxiv.org/abs/2512.23847
32. Kim, A., Muhn, M., Nikolaev, V. (2024; withdrawn Feb 2025). Financial Statement Analysis with LLMs. arXiv:2407.17866. https://arxiv.org/abs/2407.17866
33. Song, Z. (2026). Information Homogenization Induces Herding in Retrieval-Augmented LLM Agent Markets. ICLR 2026 workshop. https://iclr.cc/virtual/2026/10016534
34. Ross, J., So, E., De Simone, Z., Pozniak, C., Lo, A.W. (2026). Why Better Models Can Create Riskier Systems. arXiv:2609.04373. https://arxiv.org/abs/2609.04373
35. Islam, P., et al. (2023). *FinanceBench*. arXiv:2311.11944. https://arxiv.org/abs/2311.11944
36. Vals AI (2026-06-04). Finance Agent Benchmark v1.1. https://www.vals.ai/benchmarks/finance_agent
37. virattt. ai-hedge-fund (GitHub). https://github.com/virattt/ai-hedge-fund

**Practitioners**
38. Anthropic. Customer story: NBIM. https://claude.com/customers/nbim
39. AMWatch (2026-03-25). Norway's oil fund mulls agentic AI investment decisions. https://amwatch.com/AMNews/Fund_Management/article19144597.ece
40. Fang, Z., Moore, J. (2025-11-13). What AI can do for alpha. Man Group. https://www.man.com/insights/what-ai-can-do-for-alpha
41. Hedgeweek (2025-07-11). Man Group deploys agentic AI for quant signal discovery. https://hedgeweek.com/news/man-group-deploys-agentic-ai-for-quant-signal-discovery
42. Sharjah24 (2026-10-14). 'Human-led, agent-operated' businesses at SIF. https://sharjah24.ae/en/Articles/2026/10/14/mm10
43. AI Street (secondary). Bridgewater launches AI-driven $2bn fund. https://aistreet.beehiiv.com/p/bridgewater-launches-aidriven-2-billion-fund

**Engineering, protocols, frameworks**
44. Schluntz, E., Zhang, B. (2024-12-19). Building effective agents. https://www.anthropic.com/research/building-effective-agents
45. Hadfield, J., et al. (2025-06-13). How we built our multi-agent research system. https://www.anthropic.com/engineering/multi-agent-research-system
46. Aizawa, K. (2025-09-11). Writing effective tools for agents. https://www.anthropic.com/engineering/writing-tools-for-agents
47. Rajasekaran, P., et al. (2025-09-29). Effective context engineering for AI agents. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
48. Jones, A., Kelly, C. (2025-11-04). Code execution with MCP. https://www.anthropic.com/engineering/code-execution-with-mcp
49. Grace, M., Hadfield, J., Olivares, R., De Jonghe, J. (2026-01-09). Demystifying evals for AI agents. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
50. Anthropic. Agent SDK overview. https://code.claude.com/docs/en/agent-sdk/overview
51. Anthropic. Managed Agents: self-hosted sandboxes (beta). https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes
52. Anthropic SDK reference bundled with Claude Code: pricing (cached 2026-10-06), platform availability, prompt caching. Local files; no public URL fetched.
53. Model Context Protocol. Changelogs 2026-07-28 and 2025-11-25; specification. https://modelcontextprotocol.io/specification/2026-07-28/changelog ; https://modelcontextprotocol.io/specification/2025-11-25/changelog ; https://modelcontextprotocol.io/specification/latest
54. LangChain. LangGraph persistence. https://docs.langchain.com/oss/python/langgraph/durable-execution
55. Microsoft (2026-07-29). Agent Framework overview. https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
56. OpenAI. Agents SDK. https://openai.github.io/openai-agents-python/
57. CrewAI. Introduction. https://docs.crewai.com/en/introduction
58. OpenTelemetry. GenAI semantic conventions. https://github.com/open-telemetry/semantic-conventions-genai
59. OWASP (2025). Top 10 for LLM Applications. https://genai.owasp.org/llm-top-10/
60. Willison, S. (2025-06-16). The lethal trifecta. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
61. Debenedetti, E., et al. (2025). CaMeL. arXiv:2503.18813. https://arxiv.org/abs/2503.18813

**LLM behaviour**
62. Zheng, L., et al. (2023). Judging LLM-as-a-Judge. arXiv:2306.05685. https://arxiv.org/abs/2306.05685
63. Smit, A., et al. (2024). Should we be going MAD? arXiv:2311.17371. https://arxiv.org/abs/2311.17371
64. Sharma, M., et al. (2023). Towards Understanding Sycophancy. arXiv:2310.13548. https://arxiv.org/abs/2310.13548
65. Xiong, M., et al. (2024). Can LLMs Express Their Uncertainty? arXiv:2306.13063. https://arxiv.org/abs/2306.13063

**Governance**
66. Federal Reserve, FDIC, OCC (2026-04-17). SR 26-2, Revised Guidance on Model Risk Management. https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm (attachment: https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf)
67. NIST (2024-07). AI 600-1, Generative AI Profile. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
68. NIST (2023). AI RMF 1.0†. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
69. ISO/IEC 42001:2023†. https://www.iso.org/standard/81230.html ; secondary summary: https://cloudsecurityalliance.org/articles/iso-42001-requirements-explained-what-you-need-for-compliance
70. UAE Government. UAE Charter for the Development and Use of AI. https://u.ae/en/about-the-uae/strategies-initiatives-and-awards/policies/Ai/The-UAE-Charter-for-the-Development-and-Use-of-Artificial-Intelligence
71. *The National* (2026-02-23). UAE Central Bank AI guidelines. https://www.thenationalnews.com/business/banking/2026/02/23/uae-central-bank-issues-new-guidelines-on-the-use-of-ai-in-financial-sector/
72. *The National* (2026-10-06). Abu Dhabi AIATC meeting. https://www.thenationalnews.com/news/uae/2026/10/06/abu-dhabis-artificial-intelligence-and-advanced-technology-council-meets-to-review-ai-progress/
73. *Gulf Business* (2025). Abu Dhabi Digital Strategy 2025–2027. https://gulfbusiness.com/en/2025/tech/abu-dhabi-unveils-digital-strategy-2025-2027/

**Classical methods† (from bibliographic knowledge, not re-fetched; the metadata and DOIs of 74, 75, 77, 79 and 80 were confirmed on 2026-10-18)**
74. Bailey, Borwein, López de Prado, Zhu (2017). The probability of backtest overfitting. *J. Comput. Finance* 20(4). DOI 10.21314/jcf.2016.322. SSRN 2326253.
75. Bailey, López de Prado (2014). The deflated Sharpe ratio: correcting for selection bias, backtest overfitting, and non-normality. *J. Portf. Manag.* 40(5):94–107. DOI 10.3905/jpm.2014.40.5.094. SSRN 2460551.
76. Harvey, Liu, Zhu (2016). …and the cross-section of expected returns. *RFS* 29(1).
77. White (2000). A reality check for data snooping. *Econometrica* 68(5):1097–1126. DOI 10.1111/1468-0262.00152.
78. Hansen (2005). A test for superior predictive ability. *JBES* 23(4).
79. Foster, Stine (2008). α-investing: a procedure for sequential control of expected false discoveries. *JRSS-B* 70(2):429–444. DOI 10.1111/j.1467-9868.2007.00643.x.
80. Smith, Winkler (2006). The optimizer's curse: skepticism and postdecision surprise in decision analysis. *Management Science* 52(3):311–322. DOI 10.1287/mnsc.1050.0451.
81. Li, Jamieson, DeSalvo, Rostamizadeh, Talwalkar (2018). Hyperband. *JMLR* 18(185).
82. Kim, Nelson (2001). Fully sequential indifference-zone selection. *ACM TOMACS* 11(3).
83. Frazier, Powell, Dayanik (2008). Knowledge-gradient policy. *SIAM J. Control Optim.* 47(5).
84. Powell (2022). *Reinforcement Learning and Stochastic Optimization*. Wiley.
85. Mouret, Clune (2015). Illuminating search spaces by mapping elites. arXiv:1504.04909.
86. Sha (2001). Using simplicity to control complexity. *IEEE Software* 18(4).
87. Schweiger, Sandberg, Ragan (1986). Dialectical inquiry, devil's advocacy and consensus. *AMJ* 29(1).
88. Stasser, Titus (1985). Pooling of unshared information. *JPSP* 48(6).
89. Klein (2007). Performing a project premortem. *HBR* 85(9).
90. Mastrandrea et al. (2010). IPCC AR5 uncertainty guidance note.
91. Landis, Koch (1977). Observer agreement. *Biometrics* 33(1).
92. W3C (2013). PROV-O. https://www.w3.org/TR/prov-o/
93. Directive 2009/138/EC (Solvency II), Art. 120.
94. Chen et al. (2018). Metamorphic testing: a review. *ACM Comput. Surv.* 51(1).

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.2–2.4; `research/literature/12_agentic_ai.lit.md` (§1 content flags and venue updates, §2 table); `research/literature/recheck/10_scenarios_robustness.recheck.md`. Metadata were confirmed on Crossref, OpenAlex or arXiv on 2026-10-18. This dossier quotes no barrier statistic, so the G4 barrier re-run does not apply.

- §10 ref 4: "Sakana AI (2026-03-26). The AI Scientist, published in *Nature*" → Lu, Lu, Lange, Yamada, Hu, Foerster, Ha & Clune (2026), "Towards end-to-end automation of AI research", *Nature* 651(8107):914–919, DOI 10.1038/s41586-026-10265-5 (Crossref); the blog is kept as a secondary link.
- §10 ref 31: v1 title "A Test of Lookahead Bias in LLM Forecasts" → current title "Detecting Lookahead Bias in LLM Forecasts" (v2, 12 Jun 2026); author initials added (arXiv).
- §1 item 3: FINSABER "often vanish" → the abstract's "deteriorate significantly"; "often vanish under broader and longer evaluations" is kept only as a quote from the introduction (checked in arXiv v6, §1).
- §4 and §10 ref 29: FINSABER "2025 (KDD)" → KDD 2026; the reference gains authors, *Proc. 32nd ACM SIGKDD* V.1 pp. 2711–2722 and DOI 10.1145/3770854.3785702 (Crossref).
- §6.3: objective constraint Pr(false promotion) ≤ α → FWER ≤ α within a contract (Holm) and mFDR ≤ α across contracts (α-investing).
- §2.6 and §6.4 items 3 and 6: error criteria named. α-investing controls mFDR, "a weaker criterion than the false discovery rate"; Holm controls the FWER within a contract.
- §6.4 item 5: DSR non-normality term (skewness and kurtosis of the paired improvements) added to the expected-maximum deflation, with an [I] pass rule of DSR ≥ 1 − α.
- §2.2 and §6.4 item 5: Smith–Winkler Bayesian shrinkage of reported estimates added.
- §1 item 1 and §4: Kosmos's 79.4% accuracy now shown as holding despite full citation coverage, with the implication that G6 needs G7 behind it.
- §4: the *Nature* abstract's 70% workshop acceptance rate added as context for "1 of 3 papers above a workshop threshold".
- §1 item 1 and §9 Q9: *The Agentic Scientist* "credits orchestration for reliable autonomy" and "orchestration matters more than the base model" → reliable autonomy depends on the orchestration layer as well as on base-model capability (recheck row 24; arXiv abstract).
- §10 ref 80: Smith & Winkler subtitle, pages 311–322 and DOI 10.1287/mnsc.1050.0451 added (recheck row 35).
- §10 ref 77: White (2000) pages 1097–1126 and DOI 10.1111/1468-0262.00152 added (recheck row 36).
- §10 refs 74, 75 and 79: DOIs added, plus full titles and pages for 75 (40(5):94–107, OpenAlex) and 79 (70(2):429–444, Crossref).
- §10 refs 5, 6, 16, 25 and 30: published versions added: *ACM SIGIR Forum* 59(1):1–20, DOI 10.1145/3769733.3769747; *Nature* 655(8122):487–496 and 497–505; *IEEE Trans. Big Data* 11(6):3443–3459; the arXiv record (2504.14765) and full title of the Memorization Problem.
- §10 header of the classical list: notes that the metadata of 74, 75, 77, 79 and 80 were confirmed.
