# Design brief: ADIC Agentic Total-Portfolio Laboratory

Author: orchestrator. Date: 2026-10-18.

Inputs:

- `inputs/00_CONTEXT_AND_PRIOR_WORK.md`
- `research/00_SYNTHESIS.md` and the dossiers / cluster syntheses under `research/`
- `research/groups/01_GROUPS_SYNTHESIS.md` and the dossiers under `research/groups/`: group-specific research for the seven investment groups (see R14)
- `research/literature/`, if present: academic literature sweeps via Consensus
- `inputs/user_blueprint/adic_multi_period_tpa_optimization_agentic_architecture_blueprint.md`: a blueprint the user supplied on 2026-10-18 ("only use this if it is helpful"). It appears to come from another AI assistant, written before it had seen the deck or the paper. Treat it as a **fifth candidate proposal** in the design judge panel, scored alongside the four generated proposals. It is **not** an authority. See §6.
- `inputs/agentic_scientist_2610.18933v1.txt`: full text of the Sakana paper, extracted locally from the user's PDF. Treat it as the authoritative source on the paper.

## 1. What the user asked for (requirements)

| # | Requirement |
|---|---|
| R1 | A **multi-period optimization framework** for a ~$177bn endowment-model fund. |
| R2 | **Robust scenario analysis.** |
| R3 | **Probabilities of outcomes.** |
| R4 | A **5–10% annual distribution** requirement, owed to the sovereign owner. |
| R5 | A **10% return target**, nominal USD. |
| R6 | **Leverage permitted**, as a decision at portfolio and asset level. |
| R7 | **~60% private, mostly PE, with declining DPI.** The private book's cash generation is a central problem. |
| R8 | A **SELL / HOLD / REFINANCE / LEVER** lens for each strategy and asset. The user confirmed the split: REFINANCE = raise cash against a holding without selling it; LEVER = borrow to add exposure. The owner sets the annual distribution (R4), which is an exogenous stochastic liability. |
| R9 | Three return series per asset: **underwritten** at inception, **current actual**, and the **strategy group's forecast**. They must be fused into decision-grade forward beliefs. |
| R10 | A large multi-asset **OTC derivatives overlay** with two strategies: a **tail-protection hedge** and an **opportunistic trading** strategy. |
| R11 | An **agentic architecture** that performs the analysis, inspired by *The Agentic Scientist*. |
| R12 | The **Investment Committee can discuss the results**. |
| R13 | Build on the user's **prior deck**: two-tier robust target-attainment TPA, the state/fragility engine, attribution, and the governance motto. |
| R14 | Map the framework onto ADIC's **eight investment groups**: PE (fund commitments), Secondaries (a hybrid of secondary-fund and direct investments), Capital Solutions (structured and hybrid capital), Co-investment, Public Markets (hedge funds and long-only managers), Private Credit, Overlay, and **Real Assets**. Real Assets was added by the user on 2026-10-18, after the seven-group research. Research on it is in progress: streams G10–G15, synthesis `research/groups/02_REAL_ASSETS_SYNTHESIS.md`. Until that lands, three rules apply (see §8). The group taxonomy must be data-driven, with no hard-coded group count. Real Assets gets its own engine, action set, forecast/credibility model, synthetic-data block and IC seat. Interim placeholders are allowed. **Corporate Finance owns Treasury** and acts as the internal bank. It runs the whole funding and liability side: liquidity buffer, portfolio borrowing and leverage facilities, overlay collateral (VM/IM), distribution payments to the owner, the liquidity gate, contingency funding and internal transfer pricing. The investment groups run the asset side. Holdings, forecasts, SELL/HOLD/REFINANCE/LEVER action sets, budgets, attribution and IC discussion all roll up by group. Decisions are evaluated at the total-portfolio level. See context file §1A. |
| R16 | **Chat with the model** (user, 2026-10-18): "i then want to be able to chat with the model and ask questions". This is a first-class conversational analyst. IC members, the CIO, CRO, Treasurer, group heads and analysts ask questions in plain language: explanations ("why is this fund a SELL?"), drill-downs by group and holding (including the three return marks and forecast credibility), probabilities, comparisons with controls and archetypes, and what-ifs. **Rules:**<br>• Every number comes from the deterministic engines and links to a run (P1, P7).<br>• A what-if becomes a typed override, which the user confirms before it runs.<br>• Answers state their status (EXPLORATORY vs QUALIFIED) and SYNTHETIC labels.<br>• Access is role-based, transcripts are logged, and the analyst is read-only on engines, beliefs and scenarios.<br>**Surfaces:** Claude Code or Claude Desktop through the read-only analyst MCP server; a CLI chat (`tpa chat`, with Stub/Replay backends for offline use); the IC pack's Ask panel. The design is in `design/addenda/CHAT_ANALYST.md`. |
| R15 | **Synthetic returns are permitted** where real data is missing (user, 2026-10-18). They must be labeled synthetic everywhere and generated from a documented ground-truth process, so estimators can be validated by parameter recovery. |

## 2. Non-negotiable principles

### From the user's deck
- **P1. "LLMs accelerate evidence; deterministic models own numbers; humans own decisions."**
  - No LLM ever produces a number that is not the output of a deterministic, versioned tool call.
  - The IC keeps all decision rights.
  - Nothing executes trades.

### From *The Agentic Scientist*, verified against the full local text
Line numbers ("l.") refer to `inputs/agentic_scientist_2610.18933v1.txt`.

An independent full-text check of the research dossier is in `research/verification/13_paper_deepread.localcheck.md`. It found that the dossier gets the paper's numbers right but overstates evaluator immutability and sandboxing, and presents several repo-only mechanisms as paper mechanisms. **On paper mechanisms, this brief and the paper text govern over the dossier and the research syntheses.**

The paper's framing:
- Its ablations "suggest that reliable scientific autonomy depends not only on base model capabilities, but also on the cross-agent orchestration layer" (l.29-30).
- The base model matters substantially too (l.654-655, l.1219-1220).
- Its isolation is "a cooperative research-code contract, not an adversarial sandbox" (l.7489-7490).

ADIC must therefore enforce through infrastructure what the paper enforced through prompts.

- **P2. Evaluator integrity, enforced by infrastructure.**
  - **Evidence of the failure.**
    - In two of three Pi runs, the agent changed the test-time evaluation procedure: k-sample majority voting instead of pass@1. Neither the evaluator nor the rubric gates flagged it; a manual post-hoc audit did (l.1224-1234).
    - Claude Code runs without shared knowledge also modified the protocol (Fig. 17, l.1320-1322).
    - "neither deviation is apparent from the reported numbers alone" (l.1393-1394).
  - **The evaluator owns the accounting:** data access, budget counting, integrity checks and scoring. It deterministically rejects malformed, duplicate, out-of-bounds, non-finite and over-budget outputs (l.6701-6702, l.6806-6808).
  - **What a candidate reports about itself is never evidence** (l.6677, l.7223-7230). Agent-reported constraint flags, run counts or hashes are diagnostics only. IC evidence comes from engine-side logs.
  - **Guarded files.** The harness rejects candidates that edit or bypass guarded checks (l.7345-7349). The evaluator injects environment values itself (l.7335-7337).
  - **For ADIC:**
    - The engine, scenario sets, belief inputs, cost models, and metric and constraint definitions are **immutable and content-hashed**.
    - Agents act only through **typed tool interfaces** (PolicySpec, ScenarioSpec, ViewSpec, AnalysisContract), executed by a separate evaluator process. They never edit engine code.
    - Every run manifest records the engine-source hash, config hash and scenario-set hash.
    - Missing or stale caches stop evaluation; they never trigger silent recomputation (l.7210). Cache identity binds source, data and runtime (l.6915-6917).
- **P3. Separate search and final evaluation planes, fixed before search.**
  - **What the paper does.**
    - Its final evaluations switch to different datasets, environments or time partitions (l.6723-6725, l.6879-6881). One task scores against surrogate models (l.6789). The final evaluator is optional and was absent for one task (l.211, l.2307).
    - Transfer tests must be "fixed before search and held out from it" (l.1421-1423). The paper itself once chose a transfer test after search (l.1069-1071), so ADIC pre-registers.
  - **Final-plane isolation.**
    - Final cases are never used "for tuning, calibration, memory, or promotion" (l.6798).
    - Final environments and seeds are excluded from search, tuning, calibration and retry decisions, with hashes frozen before execution (l.6670-6671).
    - Each plane has its own resources and caches (l.6883-6885).
    - Search exposes only bounded aggregate metrics and failure categories (l.6825).
  - **Chronological partitions with embargo gaps** (l.6879-6882) apply to any historical calibration or backtest window.
  - **For ADIC:**
    - Candidate policies are searched on a *search* scenario set.
    - Recommendations are judged on a *held-out final* scenario set plus a **misspecification ensemble** of alternative model worlds (calibrations, regime models, private-markets models). All of it is fixed and hashed before search.
    - This is the home of the user's "7% robust floor under misspecification".
- **P4. Typed idea bundles and engine-counted budgets.**
  - **What the paper does.**
    - Ideation agents are read-only and emit structured bundles: id, title, falsifiable hypothesis, ordered implementation plan, target rubrics (≥1 metric rubric and ≥1 constraint/implementation rubric) (App. F.2).
    - Retries are capped: "≤3 retries on validation failure" (l.6290). An "authoritative cross-idea memory log" is kept (l.6285, l.6378).
    - The per-attempt evaluation cap is a prompt rule the agent checks itself (l.6412-6413). It counts calls, including failures and retries (l.6347-6349).
    - The case studies used 1 evaluation per idea and 20–60 cycles (l.7517, l.7539, l.7647).
  - **For ADIC:**
    - The **engine** counts every evaluation, including failures and retries.
    - There is no exploratory evaluation outside the official evaluator.
    - The count feeds an **overfitting adjustment** (deflated improvement / probability of backtest overfitting), which is reported to the IC.
- **P5. Gates: engine-owned correctness, selection, qualification.**
  - **Correctness lives in the evaluator, not the rubrics.**
    - The paper's non-negotiable constraints sit inside the evaluator-owned `correct` flag, including per-family non-inferiority (l.6820-6822). One task aggregates its score as the minimum across families (l.7102-7103).
    - Rubrics are agent-verified and double as a stopping rule (l.6346). Rubric pass rates fluctuate while best scores rise (l.659-660). The final pick is the best *correct* program (l.256-257).
  - **Selection and final claims.**
    - A tie keeps the incumbent (l.6823-6824).
    - "Strictly higher" applies only to search promotion. Final claims need paired, pre-declared uncertainty and materiality (l.6826-6829, l.7107-7108, l.7509-7512).
    - Common random numbers are used (l.7472-7473).
  - **Correctness is separate from eligibility to claim improvement.** A valid but non-winning run is `not_qualified` (l.6926-6933). "Protocol validity alone does not establish improvement" (l.6712-6713).
  - **Failure accounting.** Failures are never dropped or renormalized (l.6684-6686). Budget exhaustion is distinct from execution failure (l.6685-6686). The paper's own Figs. 14 and 16 drop NaN seeds (l.1109), a counter-example ADIC must not repeat.
  - **For ADIC: three gates.**
    1. **Gate 1, `correct` (engine-owned).** All hard constraints, budgets, no leakage, and non-inferiority versus HOLD in every model world, aggregated on the worst world.
    2. **Gate 2, selection.** Strictly better on the search objective; ties keep the incumbent.
    3. **Gate 3, qualification (final plane).** A paired comparison with common random numbers, pre-declared materiality and Monte-Carlo uncertainty. Otherwise the result is `not_qualified`.

    Agent-checked rubrics are diagnostics and stopping rules, not gates.
- **P6. Controls, attribution and retrospective evidence.**
  - **Mandatory controls.**
    - Naive controls at every horizon (l.6925-6926).
    - A hand-designed comparator frozen before search (l.6680-6681).
    - Permutation, placebo and reset controls (l.7029-7030, l.7153-7154, l.7216-7217).
  - **Attribution by an exact switch-off null control.** In the paper's CMA-ES result, fixed scaffolding supplies 55.8% of the margin, and the learned increment reverses sign on final solution quality (l.2657-2663, l.2687-2700). The headline seeds were also used for selection (l.3089-3091).
  - **Ablation fairness.** "change ONLY the declared component"; do not optimize the variant beyond validity; no extra experiments (l.6559-6561).
  - **Pre-declared comparisons.** Pareto comparison over operating points declared in advance (l.7020-7021). Horizons declared in advance (l.6678-6679).
  - **Post-hoc analysis** may run new inference and one optional bootstrap rerun of the evaluator. It never retrains or alters the selected program (l.355-359).
  - **For ADIC:**
    - Every recommendation is compared, at 3y / 5y / 10y, with:
      - HOLD / status quo
      - static SAA
      - the deck's rule policy
      - target-chasing
      - a placebo policy fed shuffled signals
    - Single-change ablations and a switch-off null control separate scaffolding (fixed rules) from searched components.
    - Selection seeds and scenarios are disjoint from reporting seeds and scenarios.
    - Frontiers are reported over pre-declared risk budgets.
- **P7. Claim-to-source: "resolves" is deterministic, "supports" is audited.**
  - **What the paper does.**
    - Its deterministic checks only confirm that citation keys and claim-to-source links resolve (l.6200-6201).
    - Whether a source *supports* a claim is left to an LLM audit (l.405-407) and to humans, who found citations that resolved but did not support the claim (l.555-556).
    - Auditors catch problems "far more reliably from logs and code than from the paper alone" (l.1976-1979).
    - Each claim type carries its own evidence requirement and scope: "Scope conclusions to the tested configuration" (l.6714).
  - **For ADIC:**
    - The memo writer may cite only metric IDs in the run registry and facts in the data/provenance registry.
    - A deterministic validator rejects any number or citation that does not resolve.
    - An **independent read-only auditor** with access to run logs and engine diffs judges whether each source supports its claim. It flags overclaims, such as "significantly better" within Monte-Carlo error, and contradictions.
    - The IC sees both verdicts.
    - Add an idea-provenance map (l.1410-1412).
- **P8. Humans own the contract.**
  - **What the paper shows.**
    - "the human role shifts toward specifying the research contract: the task, its evaluators, and the rubrics that gate each stage" (l.1387-1389).
    - Every reported task was prepared by hand, without the drafting phase (l.596). The drafting pipeline "may fail" on larger tasks (l.1428-1432).
    - Human steering also included engineering work (l.492-497).
  - **For ADIC:**
    - The IC/CIO specifies objective, constraints, admissible actions and evaluation design.
    - Agents search inside the contract; the meta-controller enforces it.
    - Agents may draft contract amendments but never adopt them.
- **P9. Deterministic orchestration, small parallelism, memory only as a search heuristic.**
  - **Orchestration.** The meta-controller (scheduling, budgets, gates, shared memory, state machine) is plain Python, not an LLM.
  - **Parallelism.** The evidence is limited: 1, 2 and 4 workers were tested on one task with three seeds. "Small amounts of parallelism improve wall clock time and effectively transfer knowledge across workers. Further scaling of the parallelism does not show improvements" (l.1209-1210). Default to 2 workers, configurable to 4.
  - **Shared memory.** The paper's "distilled conclusions" are per-worker, unvalidated search heuristics within one campaign (l.6231-6234), periodically pruned (l.254-256). In ADIC they:
    - never count as evidence
    - never reach the IC as findings
    - never persist across campaigns as institutional memory
    - never see final-plane data (l.6798)
  - **Escalation.** The paper's agents are told never to ask questions and to assume instead (l.6406-6408). ADIC agents get an escalation channel, and every assumption is logged.
- **P10. Cross-family review.**
  - **What the paper says.** §8 suggests "Reviewers drawn from several model families to dilute the circularity of using the same models for investigation and rubric review" (l.1423-1424). AI-review scores "can potentially be overfit like any other metric" (l.1421).
  - **For ADIC:**
    - The auditor or reviewer must differ from the author agent: a different model or provider, or at least a different role prompt and context.
    - The LLM layer must be provider-agnostic, with Anthropic as the default. Bedrock, Vertex and Foundry clients exist for sovereign deployment.
- **P15. Anonymized, horizon-free policies.** Numbered P15 so that references to P11–P14 stay stable.
  - **What the paper forbids:**
    - "identity-keyed behavior, fixed replay, lookup answers, hidden optima, and future access" (l.6803-6805)
    - branching on task identity (l.7461-7462)
    - decisions that depend on a countdown, the budget or the horizon (l.7464-7468)
  - **For ADIC:**
    - Policies see scenarios anonymously: no "2008" or "2020" labels, and regimes appear only through the state a policy is entitled to observe.
    - Policies may not condition on the simulation's remaining periods. This guards against end-of-horizon gaming in a perpetual fund.
    - No silent synthetic stand-ins for required data (l.6593-6594). Synthetic data is always labeled.

### Fiduciary and engineering
- **P11. Reproducibility.** Seeded RNG (numpy `SeedSequence`), run manifests, config hashes and git SHA. Re-running a manifest reproduces the numbers bit-for-bit, or within documented tolerance.
- **P12. Offline mode.**
  - The entire quant engine and test suite run with **no LLM access**.
  - Agent code has a deterministic stub/replay LLM backend for tests.
  - Live mode needs only an API key.
- **P13. Data confidentiality.**
  - Real holdings never leave the machine except in LLM prompts the operator explicitly enables.
  - Prompts carry aggregates and IDs, not raw deal documents, by default.
- **P14. Explainability first.** Every recommendation carries:
  - its binding constraints and **shadow prices**
  - its marginal value per action
  - attribution
  - the counterfactual ("what would change the decision")

## 3. Environment and technical constraints
- **Platform:** Windows 11. Python 3.12.15 in `adic_tpa_lab/.venv`, managed by uv. Git is available.
- **Installed packages:**

  | Area | Packages |
  |---|---|
  | Numerics & data | numpy 2.5, scipy 1.18, pandas 3.0, pyarrow |
  | Optimization | cvxpy 1.9.3 with CLARABEL, HiGHS, ECOS, ECOS_BB, SCS, OSQP and SciPy solvers |
  | Statistics & ML | statsmodels, scikit-learn, hmmlearn, arch, numba |
  | Models, CLI & reporting | pydantic 2.14, typer, rich, jinja2, plotly, matplotlib |
  | Testing | pytest, hypothesis |
  | LLM & tools | anthropic 1.15 (1.x line, httpx2), mcp 2.3 |

  No GPU. No commercial solvers (MOSEK/Gurobi); design for HiGHS/CLARABEL.
- **LLM layer:** Python `anthropic` SDK.
  - Tool runner (`client.beta.messages.tool_runner` with `@beta_tool`), or a manual loop where needed.
  - Strict tool schemas (`"strict": True`, `additionalProperties: false`).
  - `client.messages.parse(output_format=PydanticModel)` for typed outputs.
  - Default model `claude-opus-5-5`. Adaptive thinking is always on; set `output_config={"effort": ...}` explicitly, because the model default is `medium`.
  - Forced `tool_choice` is not allowed on Opus 5.5; use `auto` plus a prompt instruction.
  - Server-side refusal fallback is opt-in: `betas=["server-side-fallback-2026-07-01"]` with `fallbacks="default"`.
  - Reference docs: `C:\Users\dean\AppData\Local\Temp\claude\bundled-skills\2.1.302\baa81a71889bc422abc87711d908be2f\claude-api\python\claude-api\README.md` and `tool-use.md`.
- **Performance targets (to be confirmed in design):**
  - Policy evaluation of ≥10,000 paths × 40 quarters for a ~300-holding book in under ~60 s on a laptop CPU. Holdings may be aggregated into cohorts for path simulation, with asset-level detail kept for action analysis.
  - Here-and-now scenario LP (≈500–2,000 scenarios × 8–20 quarters) solves in under ~2 minutes with HiGHS or CLARABEL.

## 4. Engagement scope (what will be built now)
- A working Python package covering:
  - data schemas and synthetic ADIC-like data, calibrated to the research
  - scenario generator
  - private-markets engine
  - return-belief fusion
  - action economics
  - leverage, overlay and liability modules
  - vectorised simulator
  - policy classes
  - here-and-now optimizer with duals
  - robustness, views and attribution
  - experiment and provenance layer
  - agent layer with meta-controller and shadow-IC
  - IC pack with interactive view-conditioning
  - CLI and an MCP server
- Tests, plus an end-to-end demo producing an IC pack on synthetic data.
- Real ADIC data plugs in later through documented schemas and adapters. Synthetic data must never be passed off as real (cf. App. F.5: "do not silently replace a required dataset with a synthetic stand-in").

## 5. Decisions the design must make explicitly
1. **Time grid:**
   - step: quarterly?
   - horizon: 10y simulation, with 3y/5y/10y reporting windows
   - meaning of the 10% target: per-year geometric, gross of distributions? Net? Report both?
2. **State representation:**
   - holdings vs cohorts
   - which state variables are tracked per path, and the memory budget
3. **Scenario generator:**
   - factors (equity, rates, IG/HY spreads, inflation, oil, USD, implied vol), regime structure and innovations
   - calibration targets
   - the search/final/misspecification split
4. **Private engine:**
   - call, distribution and NAV equations
   - economic vs reported NAV
   - DPI-drought representation
   - how fused beliefs enter
5. **Instruments:** secondaries, NAV loans, preferred equity, continuation vehicles, CFO/securitisation. For each:
   - pricing
   - regime availability
   - implied cost of liquidity
6. **Overlay:**
   - tail-hedge structure and pricing (regime implied vol/skew), monetization
   - opportunistic strategy model
   - CSA collateral / VM / IM
7. **Liabilities:**
   - the distribution rule(s)
   - the oil-linked stochastic demand within 5–10%
8. **Optimizer:**
   - here-and-now program formulation (variables, constraints, objective, robustification)
   - dual extraction
   - Lagrangian action scoring for SELL / HOLD / REFINANCE / LEVER
9. **Policy classes:**
   - PFA rules, including the deck's two-tier gate and hedge/amplify rules
   - CFA / MPC
   - parametric policy search
   - how agents propose policies (PolicySpec DSL)
10. **Objective and constraints:** improve the two-tier design (robust satisficing / lexicographic); chance-constraint levels.
11. **Robustness:** KL/Wasserstein worst case, model ensemble, reverse stress test, entropy-pooling views.
12. **Experiment layer:**
    - manifests, metric registry, evaluator contracts, budgets
    - overfitting adjustment
13. **Agent roster:** roles, tools, prompts, typed outputs, gates, meta-controller state machine, shared memory.
14. **IC module:**
    - shadow-IC protocol
    - human Q&A
    - view conditioning (client-side entropy pooling in the HTML pack?)
    - decision log
15. **Package layout:**
    - module ownership for parallel build
    - interface contracts (signatures, array shapes, units)
    - test plan and acceptance criteria
16. **Group taxonomy and data schema:**
    - hierarchy: holding → group → strategy → sub-strategy
    - group-level roll-ups
    - netting of internal transfers between groups
    - group attribution versus total-portfolio decisions
17. **Group-specific action sets and economics.** For each group, define what SELL / HOLD / REFINANCE / LEVER mean, the instruments, pricing, regime availability and execution lags. Examples:
    - hedge-fund notice periods and gates
    - physical-to-synthetic replacement of long-only holdings via the overlay
    - private-credit back-leverage
    - co-investment single-asset sales
    - PE commitment pacing
18. **Internal capital market:**
    - group budgets (commitment pacing, NAV, risk, liquidity) as optimizer outputs
    - liquidity / risk transfer pricing derived from optimizer duals
    - the Secondaries and Capital Solutions groups as in-house pricing sources, with conflict controls
    - option value of dry powder for countercyclical groups
19. **Forecast credibility per group:**
    - scoring and calibration of each group's forecasts
    - bias decomposition
    - how group-level calibration is presented to the IC without destructive politics
20. **Shadow-IC roster and the human IC's discussion structure:**
    - group-head personas plus CIO, CRO, treasury and an independent challenger
    - discussion organized by group and by total portfolio
21. **Synthetic data generator:**
    - $177bn, seven groups, ~300–600 holdings
    - the three return series with realistic biases
    - a known ground-truth process
    - stylized-fact and parameter-recovery checks
    - "SYNTHETIC" labeling throughout

## 6. User-supplied blueprint: orchestrator's assessment (2026-10-18)

The file is in `inputs/user_blueprint/`. It is a coherent, high-level design. It agrees with this brief on the core thesis:
- multi-period MPC / DP instead of static MVO
- a hierarchical-Bayes de-biasing of the three return series
- the SELL / HOLD / REFINANCE / LEVER matrix
- the tail hedge as liquidity that pays when the shadow price of cash peaks
- a two-loop architecture: a quant discovery loop plus an IC "agora"

**Ideas worth grafting** (the judges and the chief architect should consider each):
1. **A market-implied return as a fourth input to belief fusion**, alongside underwritten, actual and forecast. The return implied by secondary-market pricing (bids as % of NAV) is a market anchor. ADIC's Secondaries group is the natural source of those quotes.
2. **IC-facing diagnostics:**
   - a "Zombie NAV" flag: high marks with decaying exit velocity
   - P(forecast achieved within k quarters)
   - a requirement that any forecast assuming a recovery cites verifiable catalyst milestones
3. **An explicit liquidity-margin constraint.** Liquid assets plus unused facilities must cover all of the following:
   - distributions
   - calls net of cash generated
   - IM
   - CVaR₉₉ of stressed VM

   Also a **stress-coverage test**: in a severe shock, tail-hedge inflows must cover the opportunistic book's VM calls plus the private-distribution shortfall.
4. **IC personas with explicit, opposing institutional utility functions.** For example, a Liquidity Guardian (distributions, no fire sales) set against a Total Return Architect (P(10%)). Merge these with this brief's roster: CIO, CRO, the Treasurer from Corporate Finance, the seven group heads, and a devil's advocate.
5. **Three archetype policies in every IC pack**, shown next to the recommendation:
   - A: de-risking by secondary sales
   - B: synthetic DPI via refinancing / NAV leverage plus tail-hedge monetization
   - C: expanding opportunistic alpha
6. ~~**The distribution rate as a decision variable**~~ **Rejected:** the user confirmed that the owner sets the rate each year. The distribution is an exogenous, stochastic liability within 5–10%, likely higher when oil is weak. There is no distribution-utility term.
7. **Natural-language what-ifs translated into typed parameter overrides**, such as "Buyout group forecast 16% realizes at 8%, spreads +250bp".
8. **A phased roadmap:** data and Bayes calibration, then solver, then discovery loop, then IC UI. Useful framing for the production plan.

**Cautions** (do not adopt as written):
- **REFINANCE is defined as an asset-level dividend recap or debt repricing.** For ADIC as an LP, those are GP decisions. The definitions of REFINANCE and LEVER must be settled per group under decision 17, and confirmed with the user.
- **The objective puts a P(CAGR ≥ 10%) indicator in a weighted sum.** That rewards gambling for resurrection (Browne). Keep the lexicographic / robust-satisficing structure, with the user's two tiers.
- **A neural-operator surrogate for live IC answers (<3 s) conflicts with P1** unless it is validated. Any surrogate number must be labeled as an estimate and confirmed by the deterministic engine. Prefer exact client-side entropy-pooling reweighting plus fast engine reruns, and treat the surrogate as optional future work.
- **The tooling assumes Gurobi / MOSEK, LangGraph / AutoGen and PyMC.** Gurobi and MOSEK are unavailable here: use HiGHS / CLARABEL plus Lagrangian scoring. Orchestration follows P9 (a deterministic Python meta-controller). Use NumPyro or PyMC only if they are installed; otherwise conjugate / empirical-Bayes closed forms.
- **Its example figures are illustrative hypotheticals,** such as "+14.2%" and "64% → 41%". Never present them as results.
- **It says the target is "nominal/real".** The deck says nominal USD. Report both, with nominal primary.

**User answers, 2026-10-18** (these settle decisions 7 and 17):
1. **REFINANCE versus LEVER is cash-out versus exposure-up.**
   - REFINANCE raises cash against a holding without selling it: NAV loan, preferred equity, recap.
   - LEVER borrows to add exposure or return.
2. **The owner sets the distribution rate each year,** within 5–10%. ADIC must meet it, so it is modeled as a stochastic liability, D_t = clip(f(oil, fiscal, regime), 5%, 10%) × NAV.

## 7. Literature sweep: refinements the design must address (added 2026-10-18, 17:10)

**Source:** `research/literature/00_LITERATURE_SYNTHESIS.md`, §3 (29 papers the research missed) and §4 (17 verdicts on the research recommendations). The literature supports the core architecture:
- one state-contingent λ plus quantity envelopes;
- never maximizing P(10%);
- the de Finetti payout barrier;
- pacing as the slow lever;
- regime-aware robustness;
- deterministic engines owning every number;
- a structured IC.

The items below are refinements.

**Timing.** This section was added after the four proposals and the three judge reports were written, so do not penalize those documents for missing it. `ARCHITECTURE.md` and `BUILD_SPEC.md` must adopt each item, or reject it with an ADR. Section references are to the literature synthesis.

1. **Recourse waterfall** (contradicted, §4.4).
   - The fixed order is myopic. Make the recourse order a tuned, state-dependent policy parameter, with a crowding haircut.
   - Run liquid-first, cash-last and pro-rata orders as a standing ablation.
   - In a drought, raise liquidity early: planned tail-end and LP-interest sales, and term funding.
   - Sources: Duffie & Ziegler 2003; Brown, Carlin & Lobo 2010.
2. **Facilities** (refined, §4.3).
   - Corporate Finance counts the committed revolver at ≤ 50% availability in the joint oil–crisis state, and new facilities at zero.
   - Add a tightening premium (~1.1pp in BDC data) to REFINANCE and LEVER hurdles.
   - Test pre-funded term cash as an alternative.
   - Monitor effective maturity and rollover risk.
   - Source: Acharya, Almeida & Campello 2013.
3. **Owner band** (contested, §4.2).
   - Price the band at the owner's cost, which peaks in demand busts.
   - Model a low probability that the owner accepts the band in demand-bust states.
   - Treat owner-directed domestic investments as an obligation that consumes liquidity inside the band.
   - The band-based policy applies only with advance written agreement. Without it, Mix A (no band) is the default.
4. **Objective and Tier 1** (refined, §4.7, §3.2).
   - Require a shortfall exponent strictly above 1, because linear shortfall reproduces probability maximization.
   - Declare J pre-committed and implement it through the induced objective (Forsyth 2020).
   - Re-impose the Tier-1B floor on a rolling basis (Cuoco, He & Isaenko 2008).
   - Test tighter joint chance-constraint surrogates for T6 (worst-case CVaR, ALSO-X).
   - Report the buffered probability of exceedance, and add a reaching-for-yield check.
5. **Robustness** (refined, §4.8, §3.3).
   - Show DRO and robust satisficing as one frontier (Wang et al. 2025).
   - Put ambiguity on regime persistence (transition matrices, drought and crisis dwell times), not only on means (Hansen et al. 2019).
   - Do not stack ambiguity sets, and use regime-conditional radii.
6. **Optimization core** (refined, §4.9, §3.1).
   - Carry the regime as a belief state in V (partially observable SDDP, Lee et al. 2023), if V is in scope.
   - Reduce multistage trees by filtration distance (Heitsch & Römisch 2009).
   - Certify policy P with information-relaxation dual bounds and report the gap in every release (Brown & Smith 2011).
   - Use lifted decision rules where linear ones are inadequate.
7. **Forward Belief Engine** (one contradiction, §4.10, §3.8).
   - Shrink fusion weights toward equal. Keep covariances in the predictive variance only.
   - Adopt constrained GLS only if it beats simple and screened averages out of sample.
   - Recalibrate every linear pool, e.g. with a beta-transformed linear pool (Ranjan & Gneiting 2010).
   - Cap credibility beyond ~8 quarters.
   - Any recognition of the "best forecaster" must be incentive-compatible.
8. **Group return priors** (contradicted in places, §4.11, §3.7, §3.9).
   - **Hedge funds:** α ≈ 0, with α = 0 as a mandatory sensitivity and a put-writing baseline.
   - **Long-only:** sleeve-specific priors.
   - **Private Credit:** a fund-age prior with a downside-beta charge, LGD by collateral type, and zero Tier-1 liquidity for evergreen units.
   - **PE:** weight GP access over selection skill, and apply a fund-size penalty to up-sizes.
   - **Secondaries:** continuation-vehicle elections are events, not controls.
9. **Overlay** (refined, §4.13, §3.10).
   - The convex sleeve must beat an equal-cost cash buffer held by Corporate Finance (Gamba & Triantis 2014).
   - Trigger protection on the left-tail premium, not on a low variance risk premium (VRP).
   - Trend's crisis beta decays after crises.
   - Model VM receipt delays, and set deflated-Sharpe severity by provenance.
10. **Internal capital market and FTP** (refined, §4.6, §4.16, §3.5–3.6).
    - Decompose λ by binding row.
    - Derive the risk row from the owner's loss function, not an Euler CVaR split (Bauer & Zanjani 2016).
    - Add a financing-window state, and make prices regime-conditional.
    - Publish Lagrangian bounds whose gap does not grow with the number of groups.
    - Haircut summed group risk budgets, collar envelope changes, and use no single hurdle.
11. **IC** (refined, §4.15, §3.12).
    - Pre-commit contingent plans (signposts with pre-agreed actions) instead of re-aggregating beliefs every meeting (Garlappi et al. 2017).
    - Lead with authentic, sourced dissent (Nemeth et al. 2001), and aim the AI devil's advocate at the AI's own recommendation.
    - Use objective devil's advocacy by default.
    - Track decision accuracy and under-reliance.
12. **Lab** (refined, §4.14, §3.11).
    - Lock both evaluator tampering and leakage, and plant canaries (Atinafu et al. 2026).
    - Keep a mem-FDR ledger across contracts, with named error criteria: Holm FWER within a contract, mFDR across contracts.
    - Judges come from a different model family than the generator and are validated against humans.
    - Re-qualify after any model upgrade.
13. **Synthetic data** (§3.13, §4.16).
    - Use SYN-ADIC-177 to test correctness and robustness, not to select between estimator variants (Advani et al. 2019).
    - Preregister generator variants, and plan a semi-synthetic release.
14. **Pacing** (§4.5).
    - Give a pacing cut no liquidity credit for two quarters.
    - Value the pacing corridor as an option (Gourier et al. 2024).
    - Count unfunded commitments in leverage.
15. **Citation and usage errors** (§2) are being fixed in the research files. They are listed here so the design does not depend on the faulty figures. One usage error changed numbers: the Broadie–Glasserman–Kou barrier shift in the co-investment work had the wrong sign, and the calculation applied none.

**Update, 2026-10-18 evening.** The fixes are applied: 886 changes in 60 files, logged in `research/literature/01_CITATION_FIX_LOG.md`. The barrier re-run (`research/groups/addenda/G4_barrier_rerun/RESULTS.md`) found:
- **Changed:** only the co-investment book-simulation write-off rate, from 2.1–2.5% to 2.8–3.3% a year.
- **Unchanged:** the holdco-PIK wipe-out rates (7.0→22.8%, 2.1→11.8%) and the single-asset LTV-breach rates (49.6/62.5%). They are at-exit or quarterly-tested statistics, so the shift does not apply.
- **Build requirement:** any barrier checked on a quarterly grid must use κ·e^{+0.5826σ√Δ}. The groups gap_04 engine still has the uncorrected barrier, so fix it at its next re-run.

## 8. Real Assets, the eighth group (added 2026-10-18, about 17:40)

**Background.** The user added "another group called real assets" and then confirmed its shape (2026-10-18):
- **Sectors:** real estate, infrastructure, and energy & natural resources. Agriculture and timber are excluded.
- **Access:** funds plus co-investments and direct assets or joint ventures.
- **Size:** part of the ~60% private allocation. No size was given, so $18bn remains the working figure.
- **PE unfunded:** the user chose census v1.1 ($16.4bn). It was sealed for the $52bn PE bucket, so re-runs also report it rescaled to the v2 bucket (about $10.9bn).

Because the energy and natural-resource holdings are confirmed, oil wrong-way risk with the owner's draw applies to ADIC's own Real Assets book.

**Research.**
- Streams G10–G15 write to `research/groups/dossiers/` and `research/groups/verification/`.
- The synthesis is `research/groups/02_REAL_ASSETS_SYNTHESIS.md`.
- The integration memo is `research/groups/03_REAL_ASSETS_INTEGRATION.md`. It lists the exact changes to the group report, the main synthesis and the design documents.

**Interim rules for `ARCHITECTURE.md` and `BUILD_SPEC.md`,** until that research lands:
1. **Taxonomy.** The group taxonomy is configuration, not code: eight groups now, more later. Roll-ups, envelopes, FTP charges, attribution, the forecast registry and IC seats are all generic over groups. The Real Assets head gets a shadow-IC seat.
2. **Engine** (interim):
   - Closed-end real-asset funds reuse the PE-fund commitment engine with real-asset parameters, including earlier income distributions.
   - Core, open-end and direct assets use income yield plus an appraisal-smoothed NAV. Value is driven by cap rates or discount rates, smoothed Geltner-style.
   - Add capex and development calls.
   - Asset-level non-recourse debt carries LTV, DSCR, a maturity wall, refinancing risk and rate hedges.
   - Open-end funds get a redemption-queue state machine, analogous to the hedge-fund liquidity-terms machine.
3. **Actions** (interim):
   - SELL: asset or stake sale; secondary sale of a fund LP interest; open-end redemption, subject to the queue.
   - HOLD.
   - REFINANCE (cash-out): cash-out refinancing of asset-level debt; recap; sale-leaseback or ground lease; joint-venture or partial-stake sell-down; NAV facility on real-asset fund interests.
   - LEVER (exposure-up): asset-level acquisition or development debt.
   - Asset-level debt is non-recourse and sits outside Corporate Finance's facilities. It still counts in look-through leverage, and in stress through refinancing risk and covenant cures.
4. **Marks.**
   - Underwritten: yield-on-cost, IRR, exit cap rate.
   - Current: appraisal NAV, lagged and smoothed.
   - Forecast: asset business plans.
   - Market-implied: listed REIT and infrastructure NAV discounts, and secondary-market pricing.
5. **Oil and inflation links.**
   - Energy and natural-resource assets add oil exposure. They are wrong-way with the owner's draw: when oil is weak, the draw rises and energy assets fall.
   - Gulf real estate may move with the local fiscal cycle.
   - Infrastructure and real-estate income pass inflation through only partially.
6. **Synthetic allocation (working v2, pending the user).**
   - Real Assets $18bn (about 10%), carved out of PE funds ($52bn → $34bn), so the private share stays about 60%.
   - Real Assets unfunded commitments about $4bn.
7. **Interactions with other groups.**
   - Private Credit: real-estate debt.
   - Capital Solutions: preferred equity and NAV financing for real assets.
   - Overlay: rate and inflation hedges for real-asset debt.
   - Secondaries: real-estate and infrastructure fund secondaries.
   - Corporate Finance: look-through leverage and collateral.

## 9. The three return series: user-confirmed data facts (2026-10-18, about 18:40)

**What ADIC has:**
- **History:** the groups' forecasts are archived every quarter, so a point-in-time forecast history exists.
- **Form:** underwritten, actual and forecast returns are IRR or multiple (MOIC) per holding, i.e. per fund, deal or manager, since inception.
- **Ranges:** the group forecasts come with ranges or cases (downside, base, upside, or percentiles).
- **Basis:** all series are net of fees and carry.

**Consequences for the design** (ARCHITECTURE and BUILD_SPEC must reflect them):
1. **Calibrate from history.** ARCHITECTURE §4.7 assumes "the point-in-time archive does not exist yet". That assumption is wrong. On real data, the FBE bias regression, the credibility κ_g and forecast-registry scoring are estimated from the archive from the first release; priors are only the starting point. Ingesting the archive needs a bitemporal adapter that preserves as-of dates (no look-ahead) and maps each archived forecast to its holding and quarter.
2. **One basis.** The `mark` table stores IRR and MOIC with case labels. The FBE translates them into the common basis (forward annual log return on nowcast economic NAV, net), as ARCHITECTURE §4.7 specifies. Since-inception IRR is shown but treated as sunk.
3. **Cases as quantiles.** Downside, base and upside cases are read as nominal P10/P50/P90 unless a group states otherwise. κ_g then measures how wide the true errors are relative to the stated range. Interval scoring (WIS, coverage) runs on these quantiles.
4. **Basis consistency.** Everything is already net, so no gross-to-net translation is needed for ADIC data. The synthetic generator must produce net IRR/MOIC marks with cases, in the same shape as ADIC's data.
