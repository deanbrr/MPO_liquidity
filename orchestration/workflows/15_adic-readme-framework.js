export const meta = {
  // As run 20-21 Oct (run wf_9410fdcc-6b8): the writer finished README.md, then hit the monthly spend limit while
  // trimming it; the verify and fix phases did not run. The README was checked by hand instead (static GitHub-
  // rendering and link checks, content read against FRAMEWORK_DESCRIPTION.md v1.1) and pushed.
  name: 'adic-readme-framework',
  description: 'Redo README.md as the comprehensive framework readme (variables, multi-period approach, formulas, constraints, objectives, fusion, simulator, scenarios, outputs, honest prototype status, repo map, quick start) in the compact style of framework description v0, with content taken from the verified v1.1; two independent verifiers; fix',
  phases: [
    { title: 'Write', detail: 'README.md from v0 (style and scope) and v1.1 (verified content)' },
    { title: 'Verify', detail: 'formulas, variables and constraints; coverage, accuracy and GitHub rendering' },
    { title: 'Fix', detail: 'apply every critical, high and medium finding' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const README = ROOT + '\\README.md'
const SCR = 'C:\\Users\\dean\\AppData\\Local\\Temp\\claude\\C--users-dean-ai-envs\\e78f6185-0aea-4458-8bbb-ae3b68b29e97\\scratchpad'
const V0 = SCR + '\\FRAMEWORK_v0.md'
const OLD = SCR + '\\README_current.md'
const V11 = ROOT + '\\design\\FRAMEWORK_DESCRIPTION.md'
const DSGO = ROOT + '\\design\\DECISION_SPACE_AND_GOAL_OBJECTIVE.md'
const EX = ROOT + '\\examples\\mpo_v2'
const RA = SCR + '\\readme_review_math.md'
const RB = SCR + '\\readme_review_coverage.md'
const PY = 'C:\\Users\\dean\\AppData\\Roaming\\uv\\python\\cpython-3.12.15-windows-x86_64-none\\python.exe'
const VPY = ROOT + '\\tools\\vpy.py'
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'

const CTX = `CONTEXT: private GitHub repo deanbrr/MPO_liquidity (local clone ${ROOT}). It holds the research, design and prototypes of a multi-period, liquidity-aware portfolio optimizer for ADIC, a ~$177bn endowment-model sovereign fund. The owner sets a 5-10% annual distribution, an exogenous liability that is higher when oil is weak. 10% nominal USD return goal; leverage allowed; ~60% private; an OTC overlay with a tail hedge and an opportunistic book. Eight investment groups: PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets (hedge funds + long-only), Private Credit, Overlay, Real Assets. Corporate Finance owns Treasury, facilities, collateral and distributions. User definitions: REFINANCE = raise cash against a holding without selling it; LEVER = borrow to add exposure. All data is SYNTHETIC.
WHY THIS TASK: the user wrote "you removed the comprehensive readme file with formulas, variables, constraints and other. redo the readme". The document they mean is framework description v0 (${V0}; also git show ae6ae5f:design/FRAMEWORK_DESCRIPTION.md): a compact (~3,900 words), comprehensive description with variables, the multi-period approach, formulas, the constraint table, objectives, fusion, the simulator, a scenario table and outputs. It was later replaced at design/FRAMEWORK_DESCRIPTION.md by v1.1 (${V11}, ~26,000 words, heavy with audit notes). v1.1 has been verified line by line against the spec (${DSGO}) and the prototype code (${EX}, commit 2aafbad), and it corrects several v0 statements. The front-page README (current text: ${OLD}) never carried the formulas. The user wants README.md itself to be that comprehensive, readable document.
SOURCES OF TRUTH: v1.1 is authoritative for facts, formulas, constraint rows, parameter values, tree dimensions, scenario statuses and known issues; where v0 and v1.1 disagree, v1.1 wins. DSGO and the code (${EX}) settle anything v1.1 leaves unclear. The prototype's results and their verification are in ${EX}\\RESULTS.md, ${EX}\\verify_math.md and ${EX}\\verify_finance.md. The user decided on 19 October 2026 not to rebuild, so the prototype stays as first run (commit 2aafbad) and its verification findings are documented, not fixed.
GITHUB RENDERING RULES (the README must render cleanly on github.com):
- Write display equations as fenced math blocks (three backticks followed by the word math) rather than $$...$$, because they are immune to Markdown interference.
- Inline math is $...$, with no space just inside either dollar sign. Keep inline math short.
- Never put a bare currency dollar sign on a line that has inline math. Write money as "USD 177bn", or escape it as \\$177bn.
- Inside table cells, never use a literal | in math; use \\vert or \\mid.
- Avoid * and _ sequences that Markdown could read as emphasis inside inline math (use \\ast; keep subscripts in braces).
- Use only standard MathJax macros. Mermaid is fine in a mermaid code block, with labels in quotes.
Windows PowerShell 5.1; use absolute paths. Run Python only as: & '${PY}' -X utf8 '${VPY}' <script.py> (the venv launcher is blocked by Smart App Control). Do not modify any file except the one you are told to write.`

const V_SCHEMA = { type: 'object', properties: { report_path: { type: 'string' }, verdict: { type: 'string' }, issues: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] }, location: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'location', 'issue', 'fix'] } } }, required: ['report_path', 'verdict', 'issues'] }
const W_SCHEMA = { type: 'object', properties: { path: { type: 'string' }, words: { type: 'integer' }, sections: { type: 'array', items: { type: 'string' } }, v0_corrections: { type: 'array', items: { type: 'string' } } }, required: ['path', 'words', 'sections', 'v0_corrections'] }
const F_SCHEMA = { type: 'object', properties: { fixed: { type: 'integer' }, not_fixed: { type: 'array', items: { type: 'string' } }, words: { type: 'integer' }, summary: { type: 'string' } }, required: ['fixed', 'not_fixed', 'words', 'summary'] }

phase('Write')
const w = await agent(`${CTX}
TASK: rewrite ${README} completely, as the comprehensive framework readme. Read v0 in full; it sets the scope, the order and the compact, plain style the user liked. Then read v1.1 for every fact, formula and status, and the current README for the repository map, quick start and status. Target 5,000-8,000 words: comprehensive, but far shorter than v1.1, with no audit clutter.
Structure (keep v0's order and depth, corrected by v1.1):
0. Title "MPO_liquidity", a one-sentence purpose, the SYNTHETIC-data note, a short contents list, and a one-paragraph summary of what the framework decides.
1. Overview: the five components with a mermaid diagram, and the principle (deterministic engine; same inputs give the same outputs; people set limits and approve; no language model produces a number).
2. Variables considered, as tables:
   - index sets;
   - state variables (symbol, meaning, units, granularity);
   - decision variables by lens and lever (SELL, HOLD, ADD, REFINANCE, LEVER, REDEEM, PACE, REBALANCE, HEDGE, FUND), with the user's definitions, example instruments, and the R1 labelling rule stated correctly as in v1.1;
   - exogenous random variables, including the owner-draw formula;
   - beliefs from the three return series;
   - limits and parameters.
3. The multi-period approach: time grid and goal; the tree as implemented (10 x 7 x 3 = 210 leaves, node counts, probabilities, moment matching); here-and-now, contingent and recourse decisions; non-anticipativity; rolling re-optimization (MPC); terminal values; why a tree for decisions and a simulator for probabilities.
4. The optimization mathematics as implemented, with formulas:
   - node dynamics (holding value, unfunded, cash balance, debt) and wealth at the leaves, including how draws are accrued;
   - the full hard-constraint table (every H row v1.1 lists, with its formula or rule, and which rows the prototype implements);
   - the objectives: GBO/bPOE with the definition, the CVaR link, the LP (Charnes-Cooper) form, and the PLAN and STRETCH regimes; the maximum-probability comparison (the exact MILP as specified, and what the prototype actually runs, LP rounding); and CRRA(3) plus shortfall;
   - choosing the plan on selection and certification sets;
   - Phase I;
   - shadow prices: the liquidity premium, reservation price, hurdle, break-even return, and the reading rules into SELL / HOLD / ADD / REFINANCE / LEVER;
   - size and solver.
5. Three-return fusion with its equations (the translation of each mark onto one forward basis, bias, credibility, the market anchor, predictive spread).
6. Simulator and out-of-sample certification (fresh paths, common random numbers, sealed truth, metrics, value at equal tail, pre-registered tests).
7. Scenarios by example: a table of at least 13 scenarios with columns for how each is represented, the decisions it typically triggers, and its status (implemented / configurable / planned), all as corrected in v1.1. For example, rate shocks cannot be configured; an oil crash raises the draw to about 7%; in crises bonds fall with equities (code observation).
8. Outputs.
9. The prototype's first run and what its verification found: a short honest table (as published vs as restated), a few plain sentences, and a note that the fixes were not implemented (decision of 19 October 2026). Copy every number exactly from v1.1's results section, RESULTS.md or the verification reports.
10. Assumptions and limitations, including a compact list of the main known issues (one line each, with pointers).
11. Repository map, Quick start (including the Smart App Control note and the tools\\vpy.py commands from the current README), Not included, and Status. Keep the current README's content for these, updated where needed.
Link to design/FRAMEWORK_DESCRIPTION.md as the full verified reference, and to DSGO, SLIM and the prototype files, using relative links. Follow the GITHUB RENDERING RULES strictly. Return the structured output, listing in v0_corrections each place where you followed v1.1 instead of v0.`, { label: 'write', phase: 'Write', schema: W_SCHEMA })
if (!w) { log('Writer failed; stopping.'); return { error: 'write failed' } }
log(`README drafted: ${w.words} words; ${w.v0_corrections.length} corrections to v0.`)

phase('Verify')
const [va, vb] = await parallel([
  () => agent(`You are an adversarial technical verifier (formulas, variables and constraints).
${CTX}
TASK: verify ${README} line by line against v1.1 (${V11}), DSGO and the code.
- Every formula: re-derive the bPOE definition and its CVaR link, the LP form, PLAN and STRETCH, the MILP rows, CRRA, the reservation-price, hurdle and break-even algebra, the fusion equations, the dynamics and the cash balance. Check each matches v1.1 and the code.
- Every variable and symbol: meaning, units, consistency across sections.
- Every constraint row: right number, right content, and the right implemented / not-implemented flag.
- Every parameter value and tree dimension.
- The R1 rule and the user's REFINANCE / LEVER definitions.
- Anything stated as implemented that is not, and the reverse.
Write ${RA} and return the structured issues. Do not edit the README.`, { label: 'verify:math', phase: 'Verify', schema: V_SCHEMA }),
  () => agent(`You are an adversarial verifier (coverage, accuracy, readability and GitHub rendering).
${CTX}
TASK: verify ${README}.
(a) Coverage against v0: is everything the user valued (variables, formulas, constraints, objectives, multi-period approach, fusion, simulator, scenario table, outputs) present and at least as clear?
(b) Accuracy: scenario rows and statuses against v1.1; the results table and every number against v1.1's results section, ${EX}\\RESULTS.md and the verification reports; the honesty of the prototype status.
(c) Repository map, quick start and links: do the paths exist? Do the relative links resolve?
(d) Readability for IC members and for a quant reader.
(e) GitHub rendering. Statically check every math segment against the GITHUB RENDERING RULES (unbalanced or adjacent dollar signs, currency dollars on math lines, | inside table math, emphasis characters in inline math, unsupported macros), plus table column counts and mermaid syntax. Then do an approximate visual render. Write a small Python script in ${SCR} that:
   - protects the math segments;
   - renders the Markdown with markdown_it (installed; mdit_py_plugins is not);
   - restores the math;
   - writes an HTML page that loads MathJax 3 from https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js, configured for $...$ inline math and for the math code blocks.
   Screenshot it with "${EDGE}" --headless=new --disable-gpu --user-data-dir=${SCR}\\edge_profile --window-size=1400,9000 --virtual-time-budget=15000 --screenshot=<png> <file URL>, and inspect the PNG with the Read tool for raw or broken math.
Write ${RB} and return the structured issues. Do not edit the README.`, { label: 'verify:coverage', phase: 'Verify', schema: V_SCHEMA }),
])
const all = [va, vb].filter(Boolean).flatMap(v => v.issues)
log(`Verification: ${['critical', 'high', 'medium', 'low'].map(s => s + ' ' + all.filter(i => i.severity === s).length).join(', ')}.`)

phase('Fix')
const f = await agent(`${CTX}
TASK: fix ${README} using the two reviews, ${RA} and ${RB}. Fix every critical, high and medium issue, and the low ones where cheap. Keep the structure, the compact style and the length (5,000-8,000 words). After editing, re-run the static GitHub-rendering checks from ${RB} on the whole file (dollar signs, | in table math, table column counts, fenced math blocks closed) and fix anything they flag. Return the structured output.`, { label: 'fix', phase: 'Fix', schema: F_SCHEMA })

return { write: { words: w.words, sections: w.sections, v0_corrections: w.v0_corrections }, verify: { math: va && va.verdict, coverage: vb && vb.verdict, counts: ['critical', 'high', 'medium', 'low'].map(s => s + ':' + all.filter(i => i.severity === s).length).join(' ') }, fix: f }
