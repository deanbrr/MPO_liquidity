export const meta = {
  name: 'adic-framework-description-verify',
  description: 'Verify design/FRAMEWORK_DESCRIPTION.md (v1.0 draft) against the spec and the prototype code from two independent angles, fix it, and check closure; implementation details that the parallel prototype fix will change are deferred to a later sync',
  phases: [
    { title: 'Verify', detail: 'two verifiers in parallel: mathematics and spec; variables, scenarios and IC readability' },
    { title: 'Fix', detail: 'apply every critical, high and medium finding' },
    { title: 'Closure', detail: 'independent check that the findings are closed' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const DOC = ROOT + '\\design\\FRAMEWORK_DESCRIPTION.md'
const EX = ROOT + '\\examples\\mpo_v2'
const BASE = '2aafbad'
const PY = 'C:\\Users\\dean\\AppData\\Roaming\\uv\\python\\cpython-3.12.15-windows-x86_64-none\\python.exe'
const VPY = ROOT + '\\tools\\vpy.py'
const GIT = 'C:\\Program Files\\Git\\cmd\\git.exe'
const RA = ROOT + '\\design\\reviews\\framework_description_review_math.md'
const RB = ROOT + '\\design\\reviews\\framework_description_review_scenarios.md'
const SYNC = ROOT + '\\design\\reviews\\framework_description_sync_todo.md'

const CTX = `CONTEXT: ADIC is a ~$177bn endowment-model sovereign fund. The owner sets a 5-10% annual distribution, an exogenous liability that is higher when oil is weak. 10% nominal USD return goal; leverage allowed; ~60% private; an OTC overlay with a tail hedge and an opportunistic book. Eight investment groups: PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets (hedge funds + long-only), Private Credit, Overlay, Real Assets. Corporate Finance owns Treasury, facilities, collateral and distributions. User definitions: REFINANCE = raise cash against a holding without selling it; LEVER = borrow to add exposure. Each holding has three return series (underwritten, actual, group forecast) as since-inception net IRR/MOIC with cases, archived quarterly. All data is SYNTHETIC.
THE DOCUMENT: ${DOC} is the v1.0 draft reference description of the framework: variables, multi-period approach, optimization mathematics, fusion, simulator, scenarios by example, outputs, limitations, glossary. Readers: the quant lead who commissioned it (expert) and IC members (educated non-specialists). It describes the approved slim design and cross-references the prototype.
SOURCES (the spec governs the design; the code shows what is actually implemented):
- ${ROOT}\\design\\SLIM_ARCHITECTURE.md (the approved engine-first design, five components)
- ${ROOT}\\design\\DECISION_SPACE_AND_GOAL_OBJECTIVE.md v1.1 ("DSGO", with its "Review changes" section)
- the prototype as of git commit ${BASE}: ${EX} (model.py, optim.py, tree.py, scenarios.py, prep.py, fusion.py, book.py, sim.py, policy.py, tasks.py, mpo_v2.py, params.json, RESULTS.md, spec_review.md)
- background only where needed: ${ROOT}\\research\\00_SYNTHESIS.md (4.1, 4.3-4.6, 4.9), ${ROOT}\\design\\ARCHITECTURE.md (4-5)
IMPORTANT, A PARALLEL FIX IS RUNNING: the prototype is being corrected right now by another workflow, after its independent verification (${EX}\\verify_math.md section 9 and ${EX}\\verify_finance.md section 5). Those files list what will change: the H16 cap, the H9 red-event row, O2's label, draw accrual, the opportunistic book, hedge-fund premia, TRS and term loan, pacing, seeds and books, reporting. Files in ${EX} may change while you work, so read the code as committed in ${BASE} (e.g. & '${GIT}' -C ${ROOT} show ${BASE}:examples/mpo_v2/model.py). If a statement in the document matches the ${BASE} code but concerns an item those two reports say will be fixed, classify the finding as SYNC-LATER, not as an error to fix now. If you need to run Python: & '${PY}' -X utf8 '${VPY}' <script.py>. The venv launcher is blocked by Windows Smart App Control, so use this form. Windows PowerShell 5.1; use absolute paths.`

const V_SCHEMA = { type: 'object', properties: { report_path: { type: 'string' }, verdict: { type: 'string' }, issues: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] }, kind: { type: 'string', enum: ['fix-now', 'sync-later'] }, location: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'kind', 'location', 'issue', 'fix'] } } }, required: ['report_path', 'verdict', 'issues'] }
const F_SCHEMA = { type: 'object', properties: { fixed: { type: 'integer' }, not_fixed: { type: 'array', items: { type: 'string' } }, sync_later: { type: 'integer' }, words: { type: 'integer' }, summary: { type: 'string' } }, required: ['fixed', 'not_fixed', 'sync_later', 'words', 'summary'] }
const C_SCHEMA = { type: 'object', properties: { closed: { type: 'integer' }, reopened_and_fixed: { type: 'array', items: { type: 'string' } }, still_open: { type: 'array', items: { type: 'string' } }, new_problems_fixed: { type: 'array', items: { type: 'string' } }, verdict: { type: 'string' } }, required: ['closed', 'reopened_and_fixed', 'still_open', 'new_problems_fixed', 'verdict'] }

phase('Verify')
const [va, vb] = await parallel([
  () => agent(`You are an adversarial technical verifier (mathematics and specification).
${CTX}
TASK: verify sections 3 (multi-period approach), 4 (optimization mathematics), 5 (data and three-return fusion), 6 (simulator and certification) and 10 (glossary) of ${DOC}, line by line against DSGO and the code.
- Re-derive every equation: bPOE and its CVaR link; the Charnes-Cooper LP form and the threshold variable; the GBO PLAN/STRETCH logic and the degeneracy finding; the MILP indicator and big-M; CRRA(3) plus shortfall; plan selection by out-of-sample probability; Phase I; and the dual-based liquidity price, reservation price, hurdle and break-even formulas with the reading rules into SELL / HOLD / REFINANCE / LEVER / ADD.
- Check every constraint family, symbol, unit, parameter value and tree dimension against params.json and the code.
- Check the fusion equations against fusion.py, and the simulator description against sim.py.
- Flag notation that is inconsistent across sections, or used before it is defined.
Write ${RA} and return the structured issues. Tag each issue fix-now or sync-later (see CONTEXT). Do not edit the document.`, { label: 'verify:math', phase: 'Verify', schema: V_SCHEMA }),
  () => agent(`You are an adversarial verifier (variables, scenarios, outputs and readability).
${CTX}
TASK: verify sections 1, 2, 7, 8 and 9 of ${DOC} against DSGO, SLIM and the code.
- Section 2: is every variable table complete and correct (symbol, meaning, units, granularity, source)? Is anything the model actually uses missing, and is anything listed that it does not use?
- Section 7, each scenario example: is it genuinely representable as described? Name the variables or parameters that move, and check the magnitudes and which regime or shock carries it. Is the implemented / configurable / planned tag right for the ${BASE} code?
- Are the user's REFINANCE and LEVER definitions used correctly everywhere?
- Sections 8 and 9: are the outputs and limitations stated accurately?
- Readability for IC members: undefined jargon, sentences that would mislead a non-specialist, and places where a short plain-English gloss is needed.
Write ${RB} and return the structured issues. Tag each issue fix-now or sync-later (see CONTEXT). Do not edit the document.`, { label: 'verify:scenarios', phase: 'Verify', schema: V_SCHEMA }),
])
const all = [va, vb].filter(Boolean).flatMap(v => v.issues)
const cnt = k => ['critical', 'high', 'medium', 'low'].map(s => s + ':' + all.filter(i => i.kind === k && i.severity === s).length).join(' ')
log(`Verification: fix-now ${cnt('fix-now')}; sync-later ${cnt('sync-later')}.`)

phase('Fix')
const f = await agent(`${CTX}
TASK: fix ${DOC} using the two reviews, ${RA} and ${RB}.
- Fix every fix-now issue of critical, high or medium severity, and the low ones where cheap. Keep the document's structure and its placeholder results section. Edit in place.
- Do NOT fix sync-later issues. Write them all to ${SYNC} as a checklist (location, what will change, and what the prototype fix must settle first), for the sync pass after the prototype is corrected.
- Update the header: version 1.1, 19 October 2026. Replace the "Draft" sentence with: "Verified against the specification and the prototype code (commit ${BASE}); the prototype is being corrected after its own verification, and implementation details will be re-synced when that finishes (see design/reviews/framework_description_sync_todo.md)."
- Add a one-line revision note at the end.
Return the structured output.`, { label: 'fix', phase: 'Fix', schema: F_SCHEMA })

phase('Closure')
const c = await agent(`You are an independent closure checker.
${CTX}
TASK: confirm that every fix-now issue of critical, high or medium severity in ${RA} and ${RB} is actually fixed in ${DOC}. Read each issue and then the current text.
- If one is not fixed, or the fix is wrong, fix it in place yourself.
- Also look for problems the fixes introduced: broken LaTeX (GitHub renders $...$ and $$...$$), broken tables or mermaid, numbering, and symbols that are now inconsistent. Fix them.
- Check that ${SYNC} exists and lists the sync-later items.
Return the structured output.`, { label: 'closure', phase: 'Closure', schema: C_SCHEMA })

return { verify: { math: va && va.verdict, scenarios: vb && vb.verdict, fix_now: cnt('fix-now'), sync_later: cnt('sync-later') }, fix: f, closure: c }
