export const meta = {
  name: 'adic-design-judge-panel',
  description: 'ADIC TPA lab design: 4 independent architecture proposals + user blueprint, 3-lens judge panel, chief architect + spec writer, 2 spec critics, revision',
  phases: [
    { title: 'Propose', detail: '4 independent architecture proposals from different angles' },
    { title: 'Judge', detail: 'quant/CRO, engineering, IC/governance judges score all 5 proposals' },
    { title: 'Architect', detail: 'chief architect writes ARCHITECTURE.md; spec writer writes BUILD_SPEC.md' },
    { title: 'Critique', detail: 'quant-consistency critic and buildability critic' },
    { title: 'Revise', detail: 'architect revises both documents and logs every change' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const P = (rel) => `${ROOT}\\${rel}`
const BLUEPRINT = P('inputs\\user_blueprint\\adic_multi_period_tpa_optimization_agentic_architecture_blueprint.md')
const ARCH = P('design\\ARCHITECTURE.md')
const SPEC = P('design\\BUILD_SPEC.md')

const CTX = `
PROJECT: ADIC Agentic Total-Portfolio Laboratory. Root folder: ${ROOT}
Shell: Windows 11, PowerShell 5.1 (no &&; the shell cwd resets after every call, so always use absolute paths). Python venv: ${ROOT}\\.venv\\Scripts\\python.exe (bare "python" does not work).

CLIENT FACTS
- ADIC: ~$177bn endowment-model sovereign fund. The OWNER sets the annual distribution within 5-10% of NAV (an exogenous, stochastic liability, likely higher when oil is weak; NOT a decision variable). 10% nominal USD return target. Leverage allowed. ~60% private, mostly PE, with declining DPI. A large multi-asset OTC derivatives overlay with two strategies: a tail-protection hedge and an opportunistic trading book.
- Seven investment groups run the ASSET side: (1) PE (allocates to funds); (2) Secondaries (hybrid of secondary-fund and direct investments); (3) Capital Solutions (preferred/structured equity, NAV/fund finance, GP solutions, special situations); (4) Co-investment; (5) Public Markets (hedge funds + long-only managers); (6) Private Credit; (7) Overlay.
- Corporate Finance (a non-investment function) owns Treasury and runs the whole FUNDING/LIABILITY side as the internal bank: liquidity buffer, portfolio borrowing and leverage facilities, overlay collateral (VM/IM), distribution payments to the owner, liquidity gate, contingency funding plan, internal transfer pricing.
- User-confirmed definitions: REFINANCE = raise cash against a holding without selling it (NAV loan, preferred equity, recap) = "cash-out". LEVER = borrow to add exposure = "exposure-up".
- Synthetic data is allowed but must always be labeled SYNTHETIC and generated from a documented ground-truth process (so estimators can be validated by parameter recovery).
- Governing motto (user's deck): "LLMs accelerate evidence; deterministic models own numbers; humans own decisions."

READ THESE (precedence on conflicts, highest first)
1. ${P('design\\00_DESIGN_BRIEF.md')} : requirements R1-R15, principles P1-P15 (section 2 governs on what The Agentic Scientist paper does and does not do), environment (section 3), scope (section 4), the 21 decisions the design must make (section 5), and the assessment of the user's blueprint (section 6).
2. ${P('inputs\\00_CONTEXT_AND_PRIOR_WORK.md')} : client facts, the seven groups (section 1A), the prior v8 deck and its gaps, the synthetic working allocation.
3. ${P('research\\00_SYNTHESIS.md')} (v1.1, ~256 KB). Read sections 0-1 fully, then what you need: section 2 (framing, feasibility), 3 (conceptual leaps L1-L16), 4 (component designs 4.1-4.12), 5 (agentic architecture), 6 (IC Deliberation Module), 7 (calibration), 9 (risks/open questions), 10 (phased build plan). Evidence tags: [S] sourced, [C] checked or computed, [I] inference / working assumption.
4. ${P('research\\groups\\01_GROUPS_SYNTHESIS.md')} (the group layer; it may be revised while you work, so use what is on disk) plus ${P('research\\groups\\addenda')}\\gap_*.md if present.
5. ${P('research\\addenda')}\\gap_01.md .. gap_05.md (Tier-1 feasibility and the calibrated stress, penalty-pinned duals / Phase I, the overlay position and Greek layer, the F_t stress filter and initial state, the expected-return bridge).
6. ${BLUEPRINT} : the user's own blueprint (the 5th candidate proposal). Brief section 6 lists what to graft and the cautions (e.g. a P(CAGR>=10%) indicator inside a weighted objective invites gambling; a neural-operator surrogate conflicts with P1; distribution-as-decision is rejected).
7. ${P('research\\verification\\13_paper_deepread.localcheck.md')} and the paper full text ${P('inputs\\agentic_scientist_2610.18933v1.txt')} (481 KB: grep it for specific mechanisms, do not read it whole).
Optional: ${P('research\\literature\\00_LITERATURE_SYNTHESIS.md')} if it exists (peer-reviewed literature sweep); prior-deck figures in ${P('inputs\\deck_v8\\media')}\\*.png.

RESEARCH FINDINGS ANY DESIGN MUST RESPECT (details and numbers in the synthesis; all numbers there are on a SYNTHETIC working book)
- One state-contingent liquidity price lambda prices every SELL/HOLD/REFINANCE/LEVER action and becomes Corporate Finance's transfer-pricing (FTP) curve; it decentralizes to the groups only when paired with quantity envelopes from the same optimizer (L14), and it is meaningful only on a feasible problem (L15: Phase I / recovery glide path; a CI test fails any card priced on a penalty-pinned dual).
- Safety first: Tier-1 survival constraints; the binding gate is the <=1% red event; P(10%) is reported but never maximized. 10% is a stretch on fee-consistent CMAs (evidence-central ~8.3%); the return bridge must be explicit.
- The literal 24-month stress T4 is infeasible within debt limits; the design uses the calibrated stress family s*(theta) / T4' with canonical conventions (draw reset on opening NAV, facility credit by instrument and horizon, IG floor, HF queue) and model-class tolerance bands (T6).
- The overlay is a POSITION layer (trades, Greeks, SIMM-like IM, VM ladders) with economic net-vega limits (OV1-OV3), not a Sharpe process.
- F_t is a calibrated 3-month stress probability (a filter), distinct from the model-robustness index k_MS.
- Group layer: Secondaries, Co-investment, Capital Solutions and Private Credit carry PE through the DPI drought; hedge funds need a liquidity-terms state machine; long-only can be replaced physical-to-synthetic via the overlay; the three marks per asset (underwritten, current actual, group forecast) plus a market-implied (secondary-pricing) anchor are fused per group with forecast-credibility scoring.

ENVIRONMENT (hard constraints)
Python 3.12; numpy, scipy, pandas, pyarrow; cvxpy with HiGHS / CLARABEL / ECOS / SCS / OSQP (NO MOSEK, NO Gurobi, no commercial MILP); statsmodels, scikit-learn, hmmlearn, arch, numba; pydantic 2, typer, rich, jinja2, plotly, matplotlib; pytest, hypothesis; anthropic 1.15 (default model claude-opus-5-5, adaptive thinking, explicit effort, strict tool schemas, messages.parse for typed outputs, provider-agnostic LLM layer) and mcp 2.3. No GPU, no Julia, no Node. Small pure-Python PyPI additions only if justified in writing.
Performance targets: >=10,000 paths x 40 quarters policy evaluation for a ~300-600-holding book in < ~60 s on a laptop CPU (cohorting allowed for path simulation, asset-level detail kept for action analysis); here-and-now scenario LP (~500-2,000 scenarios x 8-20 quarters) in < ~2 min on HiGHS/CLARABEL.
Offline-first: the whole quant engine and test suite run with no LLM access; agent code has a deterministic stub/replay LLM backend; live mode needs only an API key.

RULES
- Do not edit any file under research/ or inputs/ or design/00_DESIGN_BRIEF.md. Write only to the output path(s) you are given (create folders as needed).
- Do not browse the web; everything you need is on disk. Do not call any Consensus/authenticate tools.
- Cite the research by file and section (e.g. "00_SYNTHESIS §4.8", "gap_02", "GROUPS §3.2") for every load-bearing choice or number. Label synthetic numbers SYNTHETIC.
- Write in plain, precise English for a quant/data-science lead at a sovereign fund. Prefer tables, equations and concrete interfaces over prose.
`

const PROPOSAL_TEMPLATE = `
REQUIRED STRUCTURE (use exactly these numbered sections so the judges can compare proposals like for like):
1. Thesis: one paragraph naming the organizing idea of this architecture.
2. Requirements and principles trace: a table R1-R15 (where and how satisfied) and a table P1-P15 (how enforced, by what mechanism).
3. System decomposition: layers and modules. For each module: responsibility, inputs/outputs, deterministic or agentic, which ADIC function owns it (CIO office, Risk, Corporate Finance, a named group, MRM), and its interfaces to other modules.
4. Quant core: time grid and the meaning of the 10% target; state representation (holding vs cohort; per-path state and memory budget); scenario generator (factors, regimes, oil/fiscal, the owner's distribution demand); private engines per group; belief fusion (three marks plus market-implied anchor, credibility per group); action economics per group (what SELL / HOLD / REFINANCE / LEVER mean, instruments, pricing, regime availability, execution lags); leverage; overlay (tail hedge + opportunistic book as a position layer; collateral); liabilities; the internal capital market (lambda / FTP curve plus quantity envelopes; Corporate Finance as internal bank); optimizer formulation (here-and-now scenario LP with duals, Phase I feasibility, MPC, parametric policy search, Lagrangian action scoring); objective and constraints (improve the two-tier design); robustness (model worlds, misspecification, entropy-pooling views, reverse stress); attribution. Give variable/constraint counts and a solve-time estimate on HiGHS/CLARABEL for the here-and-now program.
5. Agentic layer: roles, typed tools, deterministic meta-controller state machine, planes, gates (engine-owned correct / selection / qualification with not_qualified), budgets, memory, escalation channel and assumption log, cross-family review, offline stub.
6. IC layer: what the IC and the seven group heads plus the Treasurer see each quarter; shadow-IC roster and protocol; discussion structure by group and by total portfolio; Q&A; view conditioning; decision log.
7. Data and synthetic generator: schemas (holding -> group -> strategy -> sub-strategy), the three return series with realistic biases, ground-truth process, parameter-recovery and stylized-fact checks, SYNTHETIC labeling, adapters for real data later.
8. Package layout and build order: modules and dependencies, what can be built in parallel, the MVP slice that runs end to end first, test strategy (unit, property, metamorphic, regression, parameter recovery).
9. Key choices versus alternatives: at least 8, each with the research evidence.
10. Risks, and what this proposal deliberately leaves out or defers.
11. Brief section 5 decisions 1-21: a one-to-three-line answer for each.
Length: about 5,000-8,000 words. Be concrete: equations, schemas, function names, numbers with sources.
`

const ANGLES = [
  { id: 'PA', file: 'PA_quant_rigor.md', name: 'Quant-rigor first',
    brief: 'Start from the mathematics. Formulate ADIC as one controlled stochastic system and make every module a consistent piece of it: the multi-period problem and its policy classes, the here-and-now scenario program and its duals, feasibility first (Phase I), the liquidity price lambda and quantity envelopes, robustness as verification across model worlds, and attribution that is exact. Keep the agent layer minimal and in service of the mathematics. Be explicit about every approximation (cohorting, scenario reduction, LP relaxation) and its error bound or test.' },
  { id: 'PB', file: 'PB_agentic_lab.md', name: 'Agentic-laboratory first',
    brief: 'Start from the Agentic Scientist mapping (as corrected in brief section 2 and the localcheck). Design the laboratory: human-owned contracts, sealed search and final planes, engine-owned evaluation and budgets, typed idea bundles (PolicySpec DSL, action packages, overlay structures), ideation/execution/ablation agents, the three gates, controls and switch-off null attribution, claim-to-source validation, cross-family review, memory as search heuristic only, escalation. The quant engines are evaluator services the lab calls. Show how one quarterly campaign runs end to end, what it costs, and how integrity is enforced by infrastructure rather than prompts.' },
  { id: 'PC', file: 'PC_ic_decision_room.md', name: 'IC decision-room first',
    brief: 'Start from the decisions the human IC, the CIO, the CRO, the Treasurer (Corporate Finance) and the seven group heads must take each quarter and each year (pacing, envelopes, SELL/HOLD/REFINANCE/LEVER cards, leverage, overlay budgets, liquidity buffer, responses to the owner\'s distribution demand). Work backwards to the evidence each decision needs, then to the engines and agents that produce it. Design the IC pack, the shadow IC (opposing utilities, devil\'s advocate, pre-votes, dissent), Q&A, view conditioning, decision log and signposts, and the politics of group forecast credibility and internal transfer pricing. Usability and governance are first-class requirements.' },
  { id: 'PD', file: 'PD_pragmatic_production.md', name: 'Pragmatic production path',
    brief: 'Start from what a small quant team can build, test and operate on the given environment (Windows laptop, Python 3.12, HiGHS/CLARABEL, offline-first) in increments, while still meeting every requirement. Define the minimal architecture with clean interfaces, an end-to-end MVP slice in the first increment, then v1 and v2. Be strongest on interfaces, data contracts and adapters for real data, performance budgets with estimates, determinism and provenance, test strategy, operability and cost. Push back on research ideas that are too heavy for the environment and say what simpler substitute keeps the guarantee.' },
]

const PROPOSAL_SCHEMA = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    words: { type: 'number' },
    thesis: { type: 'string' },
    key_choices: { type: 'array', items: { type: 'string' } },
    biggest_risk: { type: 'string' },
  },
  required: ['path', 'words', 'thesis', 'key_choices', 'biggest_risk'],
}

const JUDGE_SCHEMA = {
  type: 'object',
  properties: {
    judge: { type: 'string' },
    report_path: { type: 'string' },
    rankings: { type: 'array', items: { type: 'object', properties: {
      proposal: { type: 'string' },
      overall: { type: 'number' },
      fatal_flaws: { type: 'array', items: { type: 'string' } },
      best_ideas: { type: 'array', items: { type: 'string' } },
    }, required: ['proposal', 'overall', 'fatal_flaws', 'best_ideas'] } },
    recommended_base: { type: 'string' },
    graft_list: { type: 'array', items: { type: 'string' } },
    must_fix: { type: 'array', items: { type: 'string' } },
  },
  required: ['judge', 'report_path', 'rankings', 'recommended_base', 'graft_list', 'must_fix'],
}

const ARCH_SCHEMA = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    words: { type: 'number' },
    base: { type: 'string' },
    grafts: { type: 'array', items: { type: 'string' } },
    rejected: { type: 'array', items: { type: 'string' } },
    open_questions: { type: 'array', items: { type: 'string' } },
    adr_count: { type: 'number' },
  },
  required: ['path', 'words', 'base', 'grafts', 'rejected', 'open_questions', 'adr_count'],
}

const SPEC_SCHEMA = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    words: { type: 'number' },
    modules: { type: 'array', items: { type: 'object', properties: {
      name: { type: 'string' }, package_path: { type: 'string' }, wave: { type: 'number' },
      depends_on: { type: 'array', items: { type: 'string' } },
    }, required: ['name', 'package_path', 'wave', 'depends_on'] } },
    work_packages: { type: 'number' },
  },
  required: ['path', 'words', 'modules', 'work_packages'],
}

const CRITIQUE_SCHEMA = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    verdict: { type: 'string' },
    issues: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' },
      severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] },
      location: { type: 'string' },
      issue: { type: 'string' },
      fix: { type: 'string' },
    }, required: ['id', 'severity', 'location', 'issue', 'fix'] } },
  },
  required: ['path', 'verdict', 'issues'],
}

const REVISION_SCHEMA = {
  type: 'object',
  properties: {
    log_path: { type: 'string' },
    fixed: { type: 'number' },
    partially: { type: 'number' },
    rejected: { type: 'number' },
    open_questions: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['log_path', 'fixed', 'partially', 'rejected', 'open_questions', 'summary'],
}

// ---------------- Phase 1: proposals ----------------
phase('Propose')
log('Writing 4 independent architecture proposals; the user blueprint enters as proposal PE.')
const proposals = await parallel(ANGLES.map(a => () => agent(
`You are an independent senior architect. Write ONE complete architecture proposal for the ADIC Agentic Total-Portfolio Laboratory from this angle:

ANGLE ${a.id}: ${a.name}
${a.brief}

Work independently: do NOT open anything in ${P('design\\proposals')} other than your own output file.
${CTX}
${PROPOSAL_TEMPLATE}
OUTPUT: write the proposal to ${P('design\\proposals\\' + a.file)} . Title it "Proposal ${a.id}: ${a.name}".
Return the path, word count, a one-paragraph thesis, your 6-12 key choices (one line each), and the single biggest risk of your design.`,
  { label: `propose:${a.id}`, phase: 'Propose', schema: PROPOSAL_SCHEMA })))

const props = proposals.map((r, i) => r ? { id: ANGLES[i].id, name: ANGLES[i].name, ...r } : null).filter(Boolean)
const dropped = ANGLES.filter((a, i) => !proposals[i]).map(a => a.id)
if (dropped.length) log(`Proposals that failed and are excluded: ${dropped.join(', ')}`)
const PROPOSAL_LIST = props.map(p => `- ${p.id} (${p.name}): ${p.path}`).join('\n') +
  `\n- PE (user-supplied blueprint, written by the user before this research; judge it on its ideas, not its format): ${BLUEPRINT}`
log(`${props.length} proposals written plus the user blueprint.`)

// ---------------- Phase 2: judges ----------------
phase('Judge')
const JUDGES = [
  { id: 'quant_cro', file: 'judge_quant_cro.md', name: 'Quant / CRO judge', criteria: `
Q1 Mathematical coherence of the multi-period formulation: policy classes, here-and-now scenario program, duals, Phase I feasibility, Lagrangian action scoring.
Q2 Faithfulness to the research findings listed above and in 00_SYNTHESIS §1 (lambda plus envelopes; feasibility before prices; calibrated stress T4' and T6 bands; the <=1% red event as the binding gate; P(10%) reported not maximized; explicit return bridge; overlay position layer and OV1-OV3; F_t defined; Tier-2 accrual fix; the group cash map).
Q3 Liquidity and funding realism: Corporate Finance as internal bank, facilities, collateral VM/IM, owner distributions, HF liquidity state machine, IG floor, CFP.
Q4 Private-markets realism per group and the three-mark (+ market-implied) fusion with per-group credibility.
Q5 Overlay realism: tail hedge and opportunistic book, Greeks, SIMM-like IM, VM ladders, monetization rules.
Q6 Robustness and verification: model worlds, misspecification, controls and placebo, switch-off null attribution, deflation, sealed qualification.
Q7 Synthetic data with ground truth and parameter recovery.
Q8 Model risk and failure modes, including what happens when an assumption is wrong.` },
  { id: 'engineering', file: 'judge_engineering.md', name: 'Engineering buildability judge', criteria: `
E1 Buildability in the stated environment (Windows, Python 3.12, no commercial solvers, no GPU, offline-first).
E2 Performance credibility: 10k paths x 40 quarters < ~60 s; here-and-now LP < ~2 min on HiGHS/CLARABEL. Check the proposal's variable counts and estimates; flag MILPs or problem sizes that will not solve.
E3 Module boundaries and interface clarity; can modules be built in parallel by separate agents without conflicts?
E4 Testability: unit, property (hypothesis), metamorphic, regression, parameter recovery, CI gates such as no-pinned-duals.
E5 Determinism, reproducibility (SeedSequence, manifests, hashes) and provenance.
E6 Incremental delivery: is there a credible end-to-end MVP slice first? Risk of over-scope.
E7 Agent-layer engineering: deterministic meta-controller, typed tools, strict schemas, stub/replay LLM, failure handling, cost control, provider-agnostic.
E8 Data adapters for real ADIC data, schemas, confidentiality.` },
  { id: 'ic_governance', file: 'judge_ic_governance.md', name: 'IC usability and governance judge', criteria: `
G1 Decision rights: humans own decisions and contracts; agents propose only.
G2 IC pack clarity: what the IC sees; how probabilities and uncertainty are communicated (ICD-203 style lexicon, model-world ranges).
G3 Usability of SELL / HOLD / REFINANCE / LEVER by group; fairness and incentives of the internal capital market (FTP, envelopes) for the seven group heads.
G4 Shadow IC and deliberation design: opposing utilities, devil's advocate, pre-votes, dissent and minority reports, anti-sycophancy, decision log and signposts.
G5 Explainability: binding constraints, shadow prices, marginal value per action, attribution, counterfactuals.
G6 Governance: model-risk management, AI governance, audit trail, claim-to-source.
G7 Group forecast-credibility handled constructively rather than politically destructive.
G8 Corporate Finance / Treasurer integration and the relationship with the owner over distributions.` },
]

const judgeResults = await parallel(JUDGES.map(j => () => agent(
`You are the ${j.name} on a design review panel for the ADIC Agentic Total-Portfolio Laboratory.
${CTX}
THE PROPOSALS TO JUDGE (read every one in full):
${PROPOSAL_LIST}

SCORING: for each proposal score every criterion below 1-10 with a one-to-three-sentence justification that cites the proposal's section, then an overall score (your weighted judgement, 1-10). Identify fatal flaws (things that would make the system wrong, unbuildable or ungovernable if adopted as written) and the best ideas worth grafting into the final architecture (cite proposal and section precisely). Check each proposal against the research findings and the brief; penalize claims that contradict them or ignore user-confirmed definitions (REFINANCE = cash-out, LEVER = exposure-up, owner-set distribution as an exogenous liability).
CRITERIA:${j.criteria}

Then recommend a BASE proposal (or an explicit composite), a prioritized GRAFT LIST (specific ideas, with source), and a MUST-FIX list that the final architecture has to address regardless of base.
OUTPUT: write your full report (score tables, justifications, fatal flaws, grafts, must-fix) to ${P('design\\reviews\\' + j.file)} and return the structured summary.`,
  { label: `judge:${j.id}`, phase: 'Judge', schema: JUDGE_SCHEMA })))

const judges = judgeResults.map((r, i) => r ? { id: JUDGES[i].id, ...r } : null).filter(Boolean)
const JUDGE_LIST = judges.map(j => `- ${j.judge}: ${j.report_path} (recommended base: ${j.recommended_base})`).join('\n')
for (const j of judges) log(`${j.judge}: base=${j.recommended_base}; ` + j.rankings.map(r => `${r.proposal}=${r.overall}`).join(', '))

// ---------------- Phase 3: chief architect, then spec writer ----------------
phase('Architect')
const arch = await agent(
`You are the CHIEF ARCHITECT of the ADIC Agentic Total-Portfolio Laboratory. Produce the final architecture by choosing a base and grafting the best ideas from the other proposals (including the user's blueprint, PE) as directed by the judge panel, while resolving every conflict explicitly.
${CTX}
PROPOSALS:
${PROPOSAL_LIST}
JUDGE REPORTS (read all three in full):
${JUDGE_LIST}

Conflicts you must resolve with an ADR (examples, not exhaustive): number of lab workers (brief P9 says default 2, configurable to 4; the synthesis §5.3 proposes 3 with one isolated challenger); the size and form of the here-and-now program on HiGHS/CLARABEL (LP vs MILP; scenario counts; cohorting) given the ~2-minute target; how the user's blueprint ideas (market-implied fourth mark, Zombie-NAV flag and catalyst milestones, liquidity-margin constraint, opposing-utility personas, three archetype policies, NL what-ifs to typed overrides, phased roadmap) enter; what is deferred to later releases.

WRITE ${ARCH} with these sections:
0. Purpose, scope and reading guide (who reads what).
1. Requirements (R1-R15) and principles (P1-P15) trace table: where each is satisfied and by which mechanism.
2. System context: actors (owner, IC, CIO, CRO, Treasurer/Corporate Finance, the seven group heads, MRM, operators), external systems and data sources, LLM providers, trust boundaries.
3. Architecture overview: layers and modules (an ASCII or mermaid diagram), deterministic vs agentic boundaries, data flow for one quarterly cycle.
4. Quant core, one subsection per module: purpose, method and key equations, state, inputs/outputs with units, calibration source, evidence references, known limitations.
5. Optimization and policies: the multi-period problem, policy classes, the here-and-now scenario program (variables, constraints, objective, robustification) with size and solve-time budget, duals and Lagrangian SELL/HOLD/REFINANCE/LEVER scoring, Phase I and recovery mode, MPC loop, parametric policy search, PolicySpec DSL, anonymized horizon-free policies.
6. Internal capital market: lambda/FTP curve, quantity envelopes, group budgets, Secondaries/Capital Solutions as in-house pricing sources with conflict controls, dry-powder option value, netting of internal transfers.
7. Agentic laboratory: roles, tools, meta-controller state machine, planes, gates, budgets, memory, escalation, cross-family review, integrity enforced by infrastructure, offline stub.
8. IC Deliberation Module and IC pack: what the IC sees each quarter, shadow-IC roster and protocol, discussion by group and total portfolio, Q&A, view conditioning, archetype policies, decision log, signposts.
9. Data: schemas (holding -> group -> strategy -> sub-strategy), the four marks, the synthetic data generator with ground truth and parameter recovery, SYNTHETIC labeling, real-data adapters, confidentiality.
10. Experiment and provenance layer: manifests, hashes, metric registry, evaluator contracts, budgets, controls, null attribution, deflation, claim validation.
11. Runtime, deployment and security: offline mode, LLM configuration, MCP server, CLI, performance budgets, sovereign deployment notes.
12. ADR log: at least 25 architecture decision records (context, options, decision, consequences, evidence).
13. Brief section 5 decisions 1-21: the final answer for each, pointing to the section that implements it.
14. Provenance of the design: what was taken from each proposal (PA-PD and PE) and each judge's must-fix, what was rejected and why.
15. Open questions for the user (at most 8, each with the working assumption used until answered).
Length: as long as needed to be complete and unambiguous (expect 12,000-20,000 words). This document is the contract the build follows.
Return the structured summary.`,
  { label: 'architect', phase: 'Architect', schema: ARCH_SCHEMA })

if (!arch) { log('Chief architect failed; stopping.'); return { proposals: props, judges } }
log(`ARCHITECTURE.md written (${arch.words} words, ${arch.adr_count} ADRs, base ${arch.base}).`)

const spec = await agent(
`You are the LEAD ENGINEER. Turn the final architecture into a build specification precise enough that separate coding agents can build modules in parallel without talking to each other, and the pieces fit.
${CTX}
THE ARCHITECTURE (authoritative; read in full): ${ARCH}
Also consult the proposals and judge reports as needed:
${PROPOSAL_LIST}
${JUDGE_LIST}

WRITE ${SPEC} with these sections:
1. Global conventions: package name (src layout, e.g. src/adic_tpa/), Python version, units (state the unit of every money quantity, e.g. USD bn; every rate: decimal per quarter vs annualized), time index and calendar, sign conventions for cash flows (inflow positive to ADIC?), array axis order and dtypes (e.g. [path, quarter, asset]), currency, seeds (numpy SeedSequence spawn tree), IDs, logging, error types, config format (pydantic models + YAML/TOML), SYNTHETIC labeling rule.
2. Package layout: the full directory tree with every module file and its owner work package.
3. Data contracts: every pydantic model (fields, types, units, validators) and every array contract (name, shape, axis order, dtype, units, invariants). Include the holding/group/strategy schema, the four marks, scenarios, cash-flow paths, facilities, collateral, overlay trades and Greeks, liability paths, policy specs, action cards, envelopes, FTP curve, run manifests, claims, ballots, decision records.
4. Module specifications, one per module: purpose; public API as exact Python signatures with type hints and docstring summaries; algorithms (equations or pseudo-code where non-obvious); invariants; performance budget; failure modes and errors raised; dependencies (which other modules' public APIs it may import); tests with acceptance criteria (unit, property, metamorphic, regression, parameter recovery).
5. The here-and-now program: exact variable and constraint inventory with index sets and sizes, the cvxpy formulation outline, solver settings for HiGHS/CLARABEL, dual extraction and sign conventions, Phase I, the no-pinned-duals CI test, scale test and timing acceptance.
6. Synthetic data specification: holdings count per group (~300-600 total), allocation reconciling to $177bn and the context file's working allocation, parameters and ground-truth processes for the three marks plus market-implied mark, biases by group, unfunded commitments, facilities, overlay book, owner distribution process; parameter-recovery tests and stylized-fact checks with tolerances.
7. Agent layer specification: LLM provider interface (Anthropic default, stub/replay backend), typed tools (names, input/output schemas), roles and prompts (where stored), meta-controller states and transitions, budgets, gates, logs, escalation; the MCP server tool list; CLI commands.
8. IC pack specification: the HTML pack (jinja2 + plotly, self-contained, offline), its sections and figures, client-side view conditioning (entropy pooling) data payload and algorithm, claim-to-run links, archetype policies, decision log format.
9. Build plan: waves of work packages (WP-01 ...), each with owner module(s), inputs it depends on, deliverables, definition of done, and which WPs can run in parallel; the end-to-end MVP slice first; an end-to-end demo acceptance test that produces an IC pack on synthetic data.
10. Performance and test plan: benchmarks with targets, the CI suite, coverage expectations, golden files, tolerance policy for reproducibility.
11. Traceability: a table mapping each architecture section and ADR to the modules and tests that implement it.
Length: as long as needed (expect 12,000-25,000 words). Exact names matter: signatures in one module must match their use in another.
Return the structured summary listing every module with its package path, build wave and dependencies, and the number of work packages.`,
  { label: 'spec-writer', phase: 'Architect', schema: SPEC_SCHEMA })

if (!spec) { log('Spec writer failed; stopping after architecture.'); return { proposals: props, judges, arch } }
log(`BUILD_SPEC.md written (${spec.words} words, ${spec.modules.length} modules, ${spec.work_packages} work packages).`)

// ---------------- Phase 4: critics ----------------
phase('Critique')
const CRITICS = [
  { id: 'quant', file: 'critique_quant.md', lens: `QUANT-CONSISTENCY lens. Check both documents against the research (00_SYNTHESIS v1.1, the group synthesis and addenda, gap_01-05) and the brief: mathematical correctness (units, signs, dual conventions, feasibility logic, the objective and constraints, the stress family, the red-event gate, return bridge, overlay Greek and margin logic, belief fusion, synthetic ground truth); coverage of R1-R15 and P1-P15 and decisions 1-21; user-confirmed definitions; any place where an LLM could produce a number (violating P1); any claim stronger than its evidence; anything important from the research that the design dropped without an ADR.` },
  { id: 'build', file: 'critique_build.md', lens: `BUILDABILITY lens. Check BUILD_SPEC.md for internal consistency (every signature used by one module exists with the same name, types, shapes and units in the module that defines it; pydantic models referenced exist; array axis orders agree), environment feasibility (no commercial solvers, Windows, no GPU, offline), performance realism (problem sizes vs HiGHS/CLARABEL; vectorisation; memory), test-plan completeness and acceptance criteria that are actually checkable, work-package boundaries that let parallel agents build without file conflicts, missing modules or glue, over-scope for a first build, and whether the end-to-end demo is reachable. Also check that ARCHITECTURE.md and BUILD_SPEC.md agree.` },
]
const critiques = await parallel(CRITICS.map(c => () => agent(
`You are an adversarial design critic with a ${c.lens}
${CTX}
DOCUMENTS UNDER REVIEW (read in full): ${ARCH} and ${SPEC}
Context: proposals and judge reports
${PROPOSAL_LIST}
${JUDGE_LIST}
Find real problems, not style nits. For each issue give: id (${c.id.toUpperCase()}-NN), severity (critical = wrong numbers or unbuildable; high = a requirement or principle unmet, or a likely integration failure; medium = ambiguity that will cause rework; low = minor), exact location (document and section), what is wrong, and the concrete fix. Where you can check something numerically (e.g. a size estimate or a unit), do so with the venv Python and say so.
OUTPUT: write your critique to ${P('design\\reviews\\' + c.file)} with a verdict paragraph at the top, then the issue table. Return the structured summary.`,
  { label: `critic:${c.id}`, phase: 'Critique', schema: CRITIQUE_SCHEMA })))

const crits = critiques.filter(Boolean)
const allIssues = crits.flatMap(c => c.issues)
const sev = s => allIssues.filter(i => i.severity === s).length
log(`Critics found ${allIssues.length} issues: critical ${sev('critical')}, high ${sev('high')}, medium ${sev('medium')}, low ${sev('low')}.`)

// ---------------- Phase 5: revision ----------------
phase('Revise')
const revision = await agent(
`You are the CHIEF ARCHITECT again. Revise ${ARCH} and ${SPEC} to address the critics' findings.
${CTX}
CRITIQUES (read both in full):
${crits.map(c => `- ${c.path}`).join('\n')}
Rules: fix every critical and high issue; fix medium issues unless you can justify rejecting them; low issues at your discretion. Keep the two documents consistent with each other. Edit in place (use precise edits; do not rewrite unaffected sections). Add a short "Revision history" note at the end of each document.
Write ${P('design\\reviews\\revision_log.md')} : a table with every issue id, severity, action (fixed / partially fixed / rejected), where it was changed, and the reason for any rejection. List any questions that only the user can answer (at most 6), each with the working assumption.
Return the structured summary.`,
  { label: 'revise', phase: 'Revise', schema: REVISION_SCHEMA })

return {
  proposals: props.map(p => ({ id: p.id, path: p.path, words: p.words, thesis: p.thesis, biggest_risk: p.biggest_risk })),
  judges: judges.map(j => ({ judge: j.judge, report: j.report_path, base: j.recommended_base, rankings: j.rankings.map(r => ({ proposal: r.proposal, overall: r.overall, fatal_flaws: r.fatal_flaws })), must_fix: j.must_fix })),
  architecture: arch,
  spec: { path: spec.path, words: spec.words, work_packages: spec.work_packages, modules: spec.modules },
  critiques: crits.map(c => ({ path: c.path, verdict: c.verdict, counts: { critical: c.issues.filter(i => i.severity === 'critical').length, high: c.issues.filter(i => i.severity === 'high').length, medium: c.issues.filter(i => i.severity === 'medium').length, low: c.issues.filter(i => i.severity === 'low').length } })),
  revision,
}
