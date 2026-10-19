export const meta = {
  name: 'adic-framework-description',
  description: 'Write a precise description of the slim MPO framework (variables, multi-period approach, optimization math, scenario types by example), verify it against the spec and prototype code, and fix',
  phases: [
    { title: 'Write', detail: 'framework description from the spec, slim architecture and prototype code' },
    { title: 'Verify', detail: 'check every symbol, equation and scenario claim against spec and code' },
    { title: 'Fix', detail: 'apply corrections' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const DOC = ROOT + '\\design\\FRAMEWORK_DESCRIPTION.md'
const SOURCES = `SOURCES (read what you need; the spec governs the design, the code shows what is actually implemented):
- ${ROOT}\\design\\SLIM_ARCHITECTURE.md (the approved engine-first design: five components).
- ${ROOT}\\design\\DECISION_SPACE_AND_GOAL_OBJECTIVE.md (v1.1 with its "Review changes" section): decision space, beliefs, the goal objective (GBO / bPOE, exact max-P MILP, CRRA), hard constraints H1-H15, guards, tree and simulator, value-add tests.
- ${ROOT}\\examples\\mpo_v2\\ (the prototype being verified now: common.py, book.py, fusion.py, scenarios.py, tree.py, prep.py, model.py, optim.py, policy.py, tasks.py, report.py, mpo_v2.py, params.json, RESULTS.md, spec_review.md). Read model.py and optim.py closely for the actual LP/MILP formulation, tree.py and scenarios.py for the scenario generator and tree, fusion.py for beliefs, params.json for parameter values.
- Background, only where needed: ${ROOT}\\research\\00_SYNTHESIS.md (§4.1 scenario generator, §4.3 belief fusion, §4.4 action economics, §4.9 objective), ${ROOT}\\research\\groups\\01_GROUPS_SYNTHESIS.md, ${ROOT}\\research\\groups\\02_REAL_ASSETS_SYNTHESIS.md, ${ROOT}\\design\\ARCHITECTURE.md §4-§5.
CONTEXT: ADIC (~$177bn endowment-model sovereign fund; owner-set 5-10% annual distribution, an exogenous liability, higher when oil is weak; 10% nominal return goal; leverage allowed; ~60% private; OTC overlay with a tail hedge and an opportunistic book; eight investment groups: PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets (HF + long-only), Private Credit, Overlay, Real Assets; Corporate Finance owns Treasury, facilities, collateral and distributions). User definitions: REFINANCE = raise cash against a holding without selling it; LEVER = borrow to add exposure. Each holding has three return series (underwritten, actual, group forecast) as since-inception net IRR/MOIC with cases, archived quarterly. All data is SYNTHETIC. Windows paths; do not modify any file except the one you are told to write.`

const W_SCHEMA = { type: 'object', properties: { path: { type: 'string' }, words: { type: 'integer' }, sections: { type: 'array', items: { type: 'string' } }, not_implemented_yet: { type: 'array', items: { type: 'string' } } }, required: ['path', 'words', 'sections', 'not_implemented_yet'] }
const V_SCHEMA = { type: 'object', properties: { report_path: { type: 'string' }, verdict: { type: 'string' }, issues: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] }, location: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'location', 'issue', 'fix'] } } }, required: ['report_path', 'verdict', 'issues'] }
const F_SCHEMA = { type: 'object', properties: { fixed: { type: 'integer' }, not_fixed: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['fixed', 'not_fixed', 'summary'] }

phase('Write')
const w = await agent(`You are writing the reference description of ADIC's multi-period optimization framework for the quant lead who commissioned it (expert reader) and for IC members (educated non-specialists).
${SOURCES}
The user asked: "write out a description of the framework, the variables considered, the multiperiod approach, the optimization math, the type of scenarios that it can consider by way of example".
WRITE ${DOC} (about 6,000-9,000 words; GitHub-flavoured Markdown with LaTeX math in $...$ and $$...$$ blocks, which GitHub renders; tables for variables). Required sections:
1. Overview: what the framework decides, for whom, the five components (data and three-return fusion; scenario tree; multi-period optimizer; simulator; reports and chat), one diagram (mermaid), and the principle that it is objective (deterministic engine: same inputs, same outputs; humans set limits and approve).
2. Variables considered, as tables with symbol, meaning, units, granularity (per holding / group / portfolio / node), and source:
   (a) state variables (cash/HQLA, holding values, unfunded commitments, debt balances by facility and by holding, synthetic exposures, overlay positions and margin, hedge-fund redemption queues, draw basis, regime/belief state);
   (b) decision variables by lens and lever (SELL, ADD, REFINANCE, LEVER, HOLD; PACE, REBALANCE, HEDGE, FUND, REDEEM), per holding and per group, with the instruments behind each;
   (c) exogenous random variables (factor returns, regimes, oil/Brent, implied vol, PE calls and distributions, secondary bids, default and recovery, owner draw, financing spreads and facility availability);
   (d) parameters and limits (the hard constraints, caps, haircuts, costs);
   (e) beliefs derived from the three marks (fused forward return, uncertainty, group bias, credibility, market-implied anchor).
3. The multi-period approach: stages and time grid, the scenario tree (structure as implemented, e.g. branching per stage, fans, number of leaves, probabilities), non-anticipativity, here-and-now decisions versus contingent plans, recourse rules, rolling re-optimization (MPC), terminal values, why a tree for decisions and a simulator for probabilities.
4. The optimization math, precisely as implemented (cross-check against model.py and optim.py): the state transition and cash-balance equations; every constraint family (owner draw, cash floors, stress coverage, leverage, LTV/encumbrance, depth caps, oil caps, red-event surrogate, guards); the three objectives with derivations: the Goal-Buffered Objective / buffered probability of exceedance (definition of bPOE, its relation to CVaR, the LP form, why it cannot be gamed, the PLAN vs STRETCH regimes and the degeneracy finding), the exact maximum-probability MILP (indicator per leaf, big-M), and the CRRA(3)+shortfall alternative; plan selection by out-of-sample probability; duals: the liquidity price (lambda/ell), the reservation price p*, the hurdle and break-even return, and the reading rules that turn them into SELL / HOLD / REFINANCE / LEVER / ADD; problem size and solver (HiGHS).
5. Data and three-return fusion: the translation of since-inception IRR/MOIC and cases into a forward return on current NAV; credibility weights; group bias correction from the archive; the market-implied anchor from bids; equations.
6. The simulator and out-of-sample certification: fresh paths, sealed truth vs beliefs, common random numbers, the metrics (P(goal), CVaR, P(red event), drawdowns, bimodality), confidence intervals and pre-registered tests.
7. Scenarios it can consider, BY EXAMPLE (at least 12, each with: the story, how it is represented in the model (which variables or parameters move and by how much, which regime or shock type), what decisions it typically triggers, and whether it is implemented in the prototype now or is configurable / planned): e.g. a persistent PE distribution drought; an oil crash with a higher owner draw and halved credit-line availability; a 2008-style equity and credit crash with 30-40% secondary discounts; stagflation and a rate shock; a Gulf geopolitical shock with a Brent spike; a private-credit default wave; a real-estate repricing / open-end queue; hedge-fund gating; an overlay variation-margin spike; a benign recovery with an exit window opening; an IC view entered as a typed override (e.g. a group's forecast realizes lower, spreads +250bp) via entropy pooling or parameter override; a reverse stress (find the scenario that breaks a limit); model-world disagreement (different capital-market assumptions).
8. Outputs: the change list, contingent plans, probabilities and their confidence, attribution by action family, the frontier, and how the chat answers questions using only engine numbers.
9. Assumptions, limitations and what the production build adds.
10. Glossary of symbols.
Leave a clearly marked placeholder section "Results from the prototype (to be filled after verification)" instead of quoting results; the prototype is still being verified.
Accuracy rules: describe what the spec and code actually do; where the spec and code differ, say so; mark anything not yet implemented as planned. Return the structured output.`, { label: 'write', phase: 'Write', schema: W_SCHEMA })

phase('Verify')
const v = await agent(`You are an adversarial technical verifier.
${SOURCES}
TASK: verify ${DOC} line by line against the spec and the code. For every symbol, equation, constraint, parameter value, tree dimension and scenario claim: is it what the spec says and what model.py / optim.py / tree.py / scenarios.py / fusion.py / params.json actually implement? Check the bPOE/CVaR derivation and LP form mathematically; check the MILP description; check the dual/reservation-price/hurdle formulas; check that each scenario example is genuinely representable as described (name the variables/parameters) and correctly labelled implemented vs planned; check the user's REFINANCE/LEVER definitions are used correctly; flag unclear writing for IC readers. Write ${ROOT}\\design\\framework_description_review.md and return the structured issues. Do not edit the document.`, { label: 'verify', phase: 'Verify', schema: V_SCHEMA })

phase('Fix')
const f = await agent(`Fix ${DOC} using ${ROOT}\\design\\framework_description_review.md: fix every critical, high and medium issue (low ones if cheap), keeping the structure and the placeholder results section. Edit in place. Add a one-line revision note at the end. Return the structured output.
${SOURCES}`, { label: 'fix', phase: 'Fix', schema: F_SCHEMA })

return { write: w, verify: v && { verdict: v.verdict, n: v.issues.length, counts: ['critical', 'high', 'medium', 'low'].map(s => s + ':' + v.issues.filter(i => i.severity === s).length).join(' ') }, fix: f }
