export const meta = {
  name: 'adic-chat-analyst-design',
  description: 'Design the conversational analyst (R16: chat with the model): best-practice research, inventory of existing Q&A capability, persona question taxonomy and golden set, design addendum, adversarial critique, revision',
  phases: [
    { title: 'Inputs', detail: 'evidence research, capability inventory, persona question taxonomy (parallel)' },
    { title: 'Design', detail: 'architect writes design/addenda/CHAT_ANALYST.md' },
    { title: 'Critique', detail: 'adversarial review against P1/P7, access control, buildability' },
    { title: 'Revise', detail: 'apply the critique' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const PY = ROOT + '\\.venv\\Scripts\\python.exe'
const ARCH = ROOT + '\\design\\ARCHITECTURE.md'
const SPEC = ROOT + '\\design\\BUILD_SPEC.md'
const BRIEF = ROOT + '\\design\\00_DESIGN_BRIEF.md'
const CONTEXT = ROOT + '\\inputs\\00_CONTEXT_AND_PRIOR_WORK.md'
const ADD = ROOT + '\\design\\addenda'
const DOC = ADD + '\\CHAT_ANALYST.md'
const SKILL = 'C:\\Users\\dean\\AppData\\Local\\Temp\\claude\\bundled-skills\\2.1.302\\baa81a71889bc422abc87711d908be2f\\claude-api\\python\\claude-api'

const COMMON = `PROJECT: the ADIC Agentic Total-Portfolio Laboratory (${ROOT}). ADIC: ~$177bn endowment-model sovereign fund; owner-set 5-10% distribution (exogenous, oil-linked); 10% nominal target; leverage allowed; ~60% private; big OTC overlay (tail hedge + opportunistic book). Eight investment groups (PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets, Private Credit, Overlay, Real Assets - the last added on 18 Oct, research in progress); Corporate Finance owns Treasury (internal bank). Governing motto: "LLMs accelerate evidence; deterministic models own numbers; humans own decisions."
NEW REQUIREMENT R16 (read ${BRIEF} section 1, R16): the user said "i then want to be able to chat with the model and ask questions". Users (IC members, CIO, CRO, Treasurer, group heads, analysts) must be able to chat with the framework in plain language: explanations, drill-downs by group and holding (including the three return marks - underwritten, actual, forecast - and forecast credibility), probabilities, comparisons with controls and archetypes, and what-ifs. Every number must come from the deterministic engines with a run link; what-ifs become confirmed typed overrides; answers carry EXPLORATORY/QUALIFIED and SYNTHETIC labels; role-based access; logged transcripts; the analyst is read-only on engines, beliefs and scenarios. Surfaces: Claude Code / Claude Desktop through the read-only analyst MCP server, a CLI chat (tpa chat) with Stub/Replay backends, and the IC pack's Ask panel.
DATA FACTS (brief section 9): ADIC archives group forecasts every quarter (point-in-time history exists); the three series are IRR/MOIC per holding since inception, net of fees and carry; forecasts carry ranges or cases.
ENVIRONMENT: Windows 11, Python 3.12 venv (${PY}); anthropic 1.15 (claude-opus-5-5; adaptive thinking always on; set output_config effort explicitly; strict tool schemas; tool_choice must stay auto on Opus 5.5; client.messages.parse for typed outputs; tool runner client.beta.messages.tool_runner with @beta_tool; no sampling parameters, no assistant prefill), mcp 2.3; no web framework is installed (stdlib http.server is available); offline-first (Stub and Replay LLM backends). SDK reference docs: ${SKILL}\\README.md and ${SKILL}\\tool-use.md (read them before specifying SDK usage; never guess SDK APIs).
The authoritative design is ${ARCH} (Grep then Read ranges; relevant: §3.3 deterministic/agentic boundary, §7.3 roles and tools, §8.1 decision rights, §8.7 Q&A / W1 / W2 / W3 and NL -> typed overrides, §8.10 politics rules, §9 data, §10.6 claim validation, §11.1-11.4 offline mode, LLM configuration, MCP server, CLI). ${SPEC} is being written now (use what is on disk; it may be partial). Windows shell: the cwd resets every call, so use absolute paths.`

const R_SCHEMA = { type: 'object', properties: { path: { type: 'string' }, key_points: { type: 'array', items: { type: 'string' } } }, required: ['path', 'key_points'] }
const Q_SCHEMA = { type: 'object', properties: { path: { type: 'string' }, golden_path: { type: 'string' }, n_questions: { type: 'integer' }, personas: { type: 'array', items: { type: 'string' } }, key_points: { type: 'array', items: { type: 'string' } } }, required: ['path', 'golden_path', 'n_questions', 'key_points'] }
const D_SCHEMA = { type: 'object', properties: { path: { type: 'string' }, words: { type: 'integer' }, tools: { type: 'array', items: { type: 'string' } }, work_packages: { type: 'array', items: { type: 'string' } }, open_questions: { type: 'array', items: { type: 'string' } } }, required: ['path', 'words', 'tools', 'work_packages', 'open_questions'] }
const C_SCHEMA = { type: 'object', properties: { path: { type: 'string' }, verdict: { type: 'string' }, issues: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] }, issue: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'issue', 'fix'] } } }, required: ['path', 'verdict', 'issues'] }
const V_SCHEMA = { type: 'object', properties: { path: { type: 'string' }, fixed: { type: 'integer' }, rejected: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['path', 'fixed', 'rejected', 'summary'] }

phase('Inputs')
const [research, inventory, questions] = await parallel([
  () => agent(`${COMMON}

TASK: research best practice for a conversational analyst over quantitative/financial models where numbers must be exact and traceable. Load web tools with ToolSearch "select:WebSearch,WebFetch" (do NOT use Consensus: its quota is exhausted). Cover, with sources and dates:
- reliability of LLM tool use and text-to-query/text-to-tool for analytics (error modes; evaluation such as tau-bench style pass^k, function-calling benchmarks; numeric reasoning failures in finance QA such as FinQA/TAT-QA findings);
- grounding and provenance patterns: answers rendered from tool outputs with placeholders, citation of run ids, refusing to state numbers not returned by tools, claim validation;
- confirmation patterns for parameter changes (NL -> typed override -> show effective change -> confirm), and latency tiers;
- MCP server design for read-only analyst tools (resources vs tools, typed schemas, long-running tasks), and Anthropic SDK tool-runner patterns (read ${SKILL}\\README.md and tool-use.md);
- human factors: automation bias and over-reliance in AI-assisted decisions, how to present uncertainty in chat, and the literature already in the project (${ROOT}\\research\\dossiers\\14_ic_deliberation.md, ${ROOT}\\research\\literature\\00_LITERATURE_SYNTHESIS.md sections 3.12 and 4.15);
- security: prompt injection via documents, role-based access and information barriers between investment groups (MNPI walls), logging and audit for regulated institutions.
Write ${ADD}\\chat_research.md (2,500-4,000 words, sourced, with concrete design implications). Return the structured output.`, { label: 'chat:research', phase: 'Inputs', schema: R_SCHEMA }),
  () => agent(`${COMMON}

TASK: inventory what the current design already provides for chatting with the model, and what is missing for R16. Read the relevant sections of ${ARCH} and whatever exists of ${SPEC}. List: existing modes (Ask, W1, W2, W3), roles (Translator, writer, auditor), tools (the evaluator tools of §7.3 and the analyst MCP server tools of §11.3: get_metric, list_metrics, get_provenance, pack queries, W2 what-ifs), the claim validator and placeholder renderer, the registry and run links, labels, decision rights, politics rules, offline backends, CLI commands. Then the gaps: missing tools for explanation and drill-down (e.g. explain a card, show binding constraints and shadow prices, the three marks and credibility for a holding, group roll-ups, compare policies/archetypes, probability queries under views), the missing chat surfaces (tpa chat REPL; pack Ask panel backend), conversation memory, access control by role, transcript logging, clarifying-question behaviour, evaluation, cost limits. Be precise with section references and exact tool names.
Write ${ADD}\\chat_inventory.md (1,500-3,000 words). Return the structured output.`, { label: 'chat:inventory', phase: 'Inputs', schema: R_SCHEMA }),
  () => agent(`${COMMON}

TASK: write the question taxonomy and a golden question set. Personas: IC member; CIO; CRO; Treasurer (Corporate Finance); each of the eight group heads (PE, Secondaries, Capital Solutions, Co-investment, Public Markets, Private Credit, Overlay, Real Assets); TPA analyst; Board/owner liaison. For each persona write 8-15 realistic questions they would ask of this framework in plain language (e.g. "Why is the 2018 buyout fund a SELL this quarter?", "What is the probability of a red event if the owner draws 10% next year?", "How far off have the Co-investment team's forecasts been, and how much weight do they get?", "What happens to the facility need if PE distributions stay at 9%?", "Show me the three marks for fund X and why the fused number differs", "Which constraint is binding and what is it costing us?", "Compare the recommendation with archetype B"). For every question give: category (explain, drill-down, probability, what-if, comparison, data lookup, process/governance, out-of-scope), the tool calls needed (use names from ARCHITECTURE §7.3, §8.7 and §11.3 where they exist; propose new tool names where needed and mark them NEW), the expected answer shape (numbers with run links, labels, charts or tables), latency tier (instant / ~60 s / minutes-overnight), access rule (who may see it; information barriers between groups), and the failure mode to test (hallucinated number, wrong scope, missing label, unconfirmed override, leak across groups, speculation).
Write ${ADD}\\chat_questions.md and a machine-readable golden set ${ADD}\\chat_golden_questions.json (an array of {id, persona, question, category, tools, answer_checks, access, latency}); validate the JSON with ${PY}. Aim for 100-150 questions. Return the structured output.`, { label: 'chat:questions', phase: 'Inputs', schema: Q_SCHEMA }),
])

phase('Design')
const design = await agent(`${COMMON}

TASK: write the design addendum for the conversational analyst: ${DOC}. Inputs (read all): ${research ? research.path : '(research missing)'}, ${inventory ? inventory.path : '(inventory missing)'}, ${questions ? questions.path + ' and ' + questions.golden_path : '(questions missing)'}; plus ${ARCH} and ${SPEC} as needed.
SECTIONS:
1. Purpose and requirement R16; what "chat with the model" means here and what it never does (no autonomous decisions, no numbers from the LLM's own knowledge).
2. Principles mapped to P1, P7, P8, P9, P12, P13 and the politics rules.
3. Surfaces: (a) Claude Code / Claude Desktop through the read-only analyst MCP server (exact server name, transport, tool list, resources); (b) tpa chat, a CLI REPL built on the Anthropic SDK tool runner with the same tools, Stub/Replay backends offline, provider-agnostic; (c) the IC pack Ask panel, backed by a localhost-only service (stdlib http.server, token-protected) or degraded to W1-only offline. Show how one question flows through each.
4. Conversation pipeline: classify -> clarify if ambiguous -> plan -> typed tool calls -> render the answer from tool outputs through placeholders -> claim validation (every number traced to a run_id:artifact:path; labels; ICD-203 probability words) -> answer with provenance and a "what would change this" line; what happens on validation failure; refusing to speculate; escalation to a human.
5. Tool catalogue: every tool with exact name, purpose, typed input and output schema (Pydantic-style), latency tier, plane, and which roles may call it. Include existing tools (get_metric, list_metrics, get_provenance, pack queries, W1/W2/W3 what-ifs, implied_actions, flip_thresholds, attribute, robustness_card) and the NEW explanation and drill-down tools the questions need (e.g. explain_card, binding_constraints, holding_marks with the three marks + market-implied + fused belief + credibility, group_rollup, compare_policies, probability_query under views, forecast_track_record, run_whatif with confirm token, get_run_status). Keep tool count disciplined and schemas strict.
6. What-if protocol: NL -> typed ViewSpec/override -> effective view, KL and ESS shown -> user confirms (confirm token) -> W1 (<1 s) / W2 (<=60 s) / W3 (minutes-overnight, run handle) -> EXPLORATORY label -> any number entering the decision log is recomputed by the Python engine.
7. Explanations: how "why SELL?" is answered from the card (reservation price vs bid, binding constraints and their shadow prices, flip thresholds, belief card with the three marks, consent scenario, Gamma status); how the three return series and forecast credibility are shown, respecting the politics rules.
8. Memory and sessions: per-session context only; no institutional memory; how follow-up questions resolve references; transcript storage.
9. Access control and information barriers: roles, what each persona can see (e.g. group heads see their own holdings plus portfolio aggregates), MNPI walls, real vs synthetic data classes, redaction, the read-only guarantee.
10. Security: prompt injection (documents and quotes are data), tool allowlists, no outbound network for the analyst except the LLM API in live mode, rate and cost limits.
11. Logging and audit: transcripts hashed into the registry; questions and answers linked to runs and, when used in a decision, to the DecisionRecord.
12. Evaluation: the golden set (${questions ? questions.golden_path : 'golden set'}) as a CI suite with metrics (tool-selection accuracy, argument accuracy, number-provenance rate = 100%, label correctness, refusal correctness, access-violation rate = 0, pass^3 >= 0.9, latency by tier), replayed offline with recorded responses; human evaluation and automation-bias monitoring.
13. Cost and performance budgets.
14. Build work packages (WP-CHAT-01 ...), each with dependencies on BUILD_SPEC modules, deliverables and definition of done; how this folds into BUILD_SPEC and the build waves.
15. Open questions for the user (at most 5) with working assumptions.
Length: 5,000-8,000 words; precise; tables for the tool catalogue and access matrix. Return the structured output.`, { label: 'chat:design', phase: 'Design', schema: D_SCHEMA })
if (!design) { log('Design failed; stopping.'); return { research, inventory, questions } }

phase('Critique')
const crit = await agent(`${COMMON}

TASK: adversarially review ${DOC}. Look for: any path by which an LLM-originated number could reach a user without engine provenance (P1/P7 violations); what-ifs that could run unconfirmed or be mistaken for qualified results; information leaks across groups or roles; prompt-injection paths; tool schemas that are ambiguous, overlapping or not strict; SDK usage that contradicts ${SKILL}\\README.md or tool-use.md (check them); conflicts with ${ARCH} (decision rights, politics rules, planes - the analyst must never reach the final plane or sealed truth) and with ${SPEC} as written so far; gaps against the golden question set (questions no tool can answer); untestable acceptance criteria; over-scope for a first build. Severity: critical (wrong numbers or a principle broken), high (requirement unmet or likely failure), medium (ambiguity causing rework), low.
Write ${ADD}\\chat_critique.md and return the structured issues.`, { label: 'chat:critique', phase: 'Critique', schema: C_SCHEMA })

phase('Revise')
const rev = crit ? await agent(`${COMMON}

TASK: revise ${DOC} to address ${ADD}\\chat_critique.md: fix every critical and high issue and the medium ones unless you justify rejecting them; edit in place; add a short revision note at the end listing each issue id and its disposition. Return the structured output.`, { label: 'chat:revise', phase: 'Revise', schema: V_SCHEMA }) : null

return { research: research && research.key_points, inventory: inventory && inventory.key_points, questions: questions && { n: questions.n_questions, golden: questions.golden_path }, design, critique: crit && { verdict: crit.verdict, counts: ['critical', 'high', 'medium', 'low'].map(s => s + ':' + crit.issues.filter(i => i.severity === s).length).join(' ') }, revision: rev }
