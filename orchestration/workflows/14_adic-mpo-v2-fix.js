export const meta = {
  // NOT RUN TO COMPLETION: launched 19 Oct (run wf_bb94343b-058), stopped during planning at the user's request
  // ("do not rebuild") before it changed any code. Kept for the record; relaunch only if the user asks.
  name: 'adic-mpo-v2-fix',
  description: 'Fix the MPO v2 prototype against its independent math and finance verification: issue register and work plan with adversarial plan review, sequential work packages each reviewed in an isolated worktree, consolidated review fixes, then a full deterministic re-run with regenerated results',
  phases: [
    { title: 'Plan', detail: 'issue register and work packages from verify_math.md and verify_finance.md; adversarial plan review' },
    { title: 'Implement', detail: 'one agent per work package in order (shared files); each committed locally and reviewed in a worktree while the next proceeds' },
    { title: 'Fixup', detail: 'apply every medium-or-worse review finding' },
    { title: 'Run', detail: 'full pipeline twice (determinism); results.json and RESULTS.md regenerated with a Verification section' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const EX = ROOT + '\\examples\\mpo_v2'
const PY = 'C:\\Users\\dean\\AppData\\Roaming\\uv\\python\\cpython-3.12.15-windows-x86_64-none\\python.exe'
const VPY = ROOT + '\\tools\\vpy.py'
const BG = ROOT + '\\tools\\bgrun.py'
const GIT = 'C:\\Program Files\\Git\\cmd\\git.exe'
const PLAN = EX + '\\FIX_PLAN.md'
const LOG = EX + '\\FIX_LOG.md'
const BASE = '2aafbad'
const SCR = 'C:\\Users\\dean\\AppData\\Local\\Temp\\claude\\C--users-dean-ai-envs\\e78f6185-0aea-4458-8bbb-ae3b68b29e97\\scratchpad'

const COMMON = `PROJECT: ADIC multi-period portfolio optimization lab (repo ${ROOT}). ADIC: ~$177bn endowment-model sovereign fund; the owner sets a 5-10% annual distribution (exogenous, higher when oil is weak) that must be paid; 10% nominal USD return goal; leverage allowed; ~60% private. Eight investment groups: PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets (hedge funds + long-only), Private Credit, Overlay (tail hedge + opportunistic book), Real Assets. Corporate Finance owns Treasury, facilities, collateral and distributions. User definitions: REFINANCE = raise cash against a holding without selling it; LEVER = borrow to add exposure. Governing principle: "LLMs accelerate evidence; deterministic models own numbers; humans own decisions."

WHERE THINGS STAND: ${EX} is the working prototype of the approved slim design (five components: data and three-return fusion; scenario tree; multi-period optimizer; simulator; reports). Spec: ${ROOT}\\design\\DECISION_SPACE_AND_GOAL_OBJECTIVE.md v1.1 ("DSGO") with ${EX}\\spec_review.md; design: ${ROOT}\\design\\SLIM_ARCHITECTURE.md. Its first full run (RESULTS.md, results.json, run_log.txt; committed as ${BASE}) was independently checked in ${EX}\\verify_math.md (issues 1-11 in its section 9 table; call them M1-M11) and ${EX}\\verify_finance.md (findings F1-F13 in section 5, and L1-L5 under "Low"). Verdicts: the arithmetic is right, but the headline is overstated. About 40% of the value at equal tail is one lucky synthetic draw on a short-volatility book; the pacing attribution is a Phase I artefact; the year-1 contingent plans add nothing out of sample and carry a gambling signature; the tail guard holds only inside the LP's own ledger because draws accrue at the status quo's return; the hedge-fund redemptions rest on a prior with no put-writing premium; several rows add nothing; H16 is vacuous; H9 is degenerate; O2 is a heuristic labelled exact. The verifiers' scripts and outputs are preserved in ${EX}\\verify_checks\\math and ${EX}\\verify_checks\\finance (written for an old scratchpad path and the now-blocked venv launcher: adapt paths and the Python command if you re-run them). This stage corrects all of it.

RESEARCH TO FOLLOW (read the parts you need): ${ROOT}\\research\\00_SYNTHESIS.md (section 3: L9 objectives that cannot gamble, with payouts accruing at the fund's own return; L10 policy classes and the cushion-monotone standing rule. Section 4.4: action economics, the pacing corridor by liquidity stage and the eta signs. Section 4.5: leverage; term debt only for the reserve against the cyclical shortfall; a hedge-fund TRS adds no redemption liquidity; synthetic financing spreads. Section 4.6: overlay; exposure templates, the variance risk premium in the scenario engine, the deflated-Sharpe gate, OV1-OV3, no P(10%) in the overlay objective. Section 4.9: objective). Also ${ROOT}\\research\\literature\\00_LITERATURE_SYNTHESIS.md (section 3.9: hedge funds need near-zero alpha AND a put-writing baseline), ${ROOT}\\research\\addenda\\gap_01.md (hedge-fund liquidity ladder, gates, holdbacks, swaps), and ${ROOT}\\research\\groups\\01_GROUPS_SYNTHESIS.md and 02_REAL_ASSETS_SYNTHESIS.md (group action sets and economics).

RULES:
1. Honesty over headline. Report what the corrected model shows, even if the value-add shrinks or disappears. Never tune a parameter, cap or seed to restore a result. A parameter changes only with a research source, or as a labelled assumption [A] with a rationale in params.json. Pre-registered tests run exactly as DSGO section 6.5 specifies, as corrected by the verifiers.
2. Engines own numbers. RESULTS.md, and every number in it, is generated from results.json by report.py; never retype numbers.
3. Traceability. FIX_LOG.md cites the issue IDs (M#, F#, L#) for every code change. Spec changes go into a short "Errata after prototype verification" section at the end of DSGO, and only where the spec itself was wrong or must change.
4. Scope. Change only ${EX}, plus DSGO errata, FIX_PLAN.md and FIX_LOG.md. Do NOT modify src/ or tests/; importing src/adic_tpa read-only is fine. Do not touch design/FRAMEWORK_DESCRIPTION.md: another workflow is revising it.
5. Determinism. Seeds stay deterministic; prefer numpy SeedSequence spawning for independent streams. The same inputs give bit-identical results.
6. SYNTHETIC. Every output keeps the "SYNTHETIC - NOT ADIC DATA" label.

ENVIRONMENT: Windows; PowerShell 5.1 (no &&; the working directory resets after every call, so use absolute paths). Windows Smart App Control blocks ${ROOT}\\.venv\\Scripts\\python.exe, and pythonw.exe is unreliable too, so run ALL Python as
  & '${PY}' -X utf8 '${VPY}' <script.py> [args]      (also '${VPY}' -m pytest -q <path>, or '${VPY}' -c "<code>")
vpy.py puts the venv's packages (numpy, scipy, pandas, highspy, cvxpy with HIGHS and CLARABEL, numba, matplotlib, plotly) and src/adic_tpa on the base interpreter, and multiprocessing (spawn) workers inherit them. A tool call is cut off at about 10 minutes, so run anything longer (e.g. the full pipeline) detached:
  & '${PY}' -X utf8 '${BG}' start <name> -- '${PY}' -X utf8 '${VPY}' <script.py> [args]
then repeat  & '${PY}' -X utf8 '${BG}' wait <name> --max 540  until it prints EXITED. It shows the log tail; the full log is ${ROOT}\\runs\\bg\\<name>\\log.txt. The machine has 24 CPUs and the pipeline uses up to 20 worker processes; if another heavy job may be running (check with bgrun status <name>), use fewer. Git: & '${GIT}' -C ${ROOT} <args>. Commit with  -c user.email=dean@dsconsult.ai -c user.name=dean  and end every commit message with a blank line and "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Never push. No network.
FILES OF RECORD: ${PLAN} is the fix plan (issue register and work packages). ${LOG} is append-only: one section per work package with changes, issue IDs, every check run with its result, decisions, and anything left open.`

const WP_ITEM = { type: 'object', properties: { id: { type: 'string' }, title: { type: 'string' }, issues: { type: 'array', items: { type: 'string' } }, files: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' }, acceptance: { type: 'array', items: { type: 'string' } }, review: { type: 'boolean' } }, required: ['id', 'title', 'issues', 'files', 'summary', 'acceptance', 'review'] }
const PLAN_SCHEMA = { type: 'object', properties: { plan_path: { type: 'string' }, issues_total: { type: 'integer' }, wps: { type: 'array', items: WP_ITEM }, decisions: { type: 'array', items: { type: 'string' } }, not_fixing: { type: 'array', items: { type: 'string' } }, runtime_budget: { type: 'string' } }, required: ['plan_path', 'issues_total', 'wps', 'decisions', 'not_fixing', 'runtime_budget'] }
const CRITIC_SCHEMA = { type: 'object', properties: { plan_path: { type: 'string' }, problems: { type: 'array', items: { type: 'string' } }, issues_total: { type: 'integer' }, wps: { type: 'array', items: WP_ITEM }, decisions: { type: 'array', items: { type: 'string' } }, not_fixing: { type: 'array', items: { type: 'string' } }, runtime_budget: { type: 'string' } }, required: ['plan_path', 'problems', 'issues_total', 'wps', 'decisions', 'not_fixing', 'runtime_budget'] }
const WP_SCHEMA = { type: 'object', properties: { wp_id: { type: 'string' }, status: { type: 'string', enum: ['done', 'partial', 'failed'] }, commit: { type: 'string' }, issues_closed: { type: 'array', items: { type: 'string' } }, issues_open: { type: 'array', items: { type: 'string' } }, checks: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, pass: { type: 'boolean' }, detail: { type: 'string' } }, required: ['name', 'pass', 'detail'] } }, smoke_ok: { type: 'boolean' }, notes: { type: 'string' } }, required: ['wp_id', 'status', 'commit', 'issues_closed', 'issues_open', 'checks', 'smoke_ok', 'notes'] }
const REVIEW_SCHEMA = { type: 'object', properties: { report_path: { type: 'string' }, verdict: { type: 'string' }, issues: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] }, issue: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'issue', 'fix'] } } }, required: ['report_path', 'verdict', 'issues'] }
const FIXUP_SCHEMA = { type: 'object', properties: { fixed: { type: 'integer' }, rejected: { type: 'array', items: { type: 'string' } }, commit: { type: 'string' }, smoke_ok: { type: 'boolean' }, notes: { type: 'string' } }, required: ['fixed', 'rejected', 'commit', 'smoke_ok', 'notes'] }
const RUN_SCHEMA = { type: 'object', properties: { results_path: { type: 'string' }, runtime_s: { type: 'number' }, determinism_identical: { type: 'boolean' }, commit: { type: 'string' }, headline: { type: 'array', items: { type: 'string' } }, p_goal_oos: { type: 'object', properties: { status_quo: { type: 'number' }, best_rule: { type: 'number' }, four_line_rule: { type: 'number' }, optimized: { type: 'number' } }, required: ['status_quo', 'optimized'] }, value_at_equal_tail_pp: { type: 'string' }, issue_status: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, status: { type: 'string' }, evidence: { type: 'string' } }, required: ['id', 'status', 'evidence'] } }, notes: { type: 'string' } }, required: ['results_path', 'runtime_s', 'determinism_identical', 'commit', 'headline', 'p_goal_oos', 'value_at_equal_tail_pp', 'issue_status', 'notes'] }

phase('Plan')
const plan = await agent(`${COMMON}

TASK: write ${PLAN}, the fix plan, then return the structured output. Do not change any code.
Read fully: verify_math.md, verify_finance.md, spec_review.md, RESULTS.md (the run being fixed), and the prototype code: model.py, optim.py, sim.py, tasks.py, mpo_v2.py, policy.py, report.py, scenarios.py, tree.py, prep.py, book.py, fusion.py, world.py, common.py; params.json as needed. Read the research and DSGO sections that the fixes depend on.
The plan must contain:
1. ISSUE REGISTER: one row per issue, M1-M11, F1-F13 and L1-L5. Merge duplicates and say so: e.g. M2 with F2, F8 and F9 on the red-event row; M8 with F1 on seeds; M3 with F10 on O2. For each issue give:
   - its severity;
   - its root cause located in the code (file and function);
   - the fix: follow the verifier's proposed fix unless you have a better one, and justify any deviation;
   - a concrete, runnable ACCEPTANCE CHECK with a pass criterion. It must be able to fail; nothing hard-coded to pass;
   - the expected direction of the effect on results.
2. DECISIONS grounded in the research, each with its source and value. Cover at least:
   - how the opportunistic book is sized: outside the goal objective (SYN 4.6); interim IM held at $1.0bn, with any upsizing shown as a separate IC risk card with its crash loss;
   - the put-writing / variance premium for every short-volatility exposure (hedge funds and the opportunistic book alike);
   - the hedge-fund redemption state machine for full-lot redemptions (gates, holdbacks);
   - TRS and term-loan treatment;
   - the Amber pacing corridor and the eta signs;
   - how owner draws accrue at each policy's own return (fixed-point re-solve, with a convergence test);
   - how the tree carries enough tail (A22);
   - the red-event surrogate recalibrated to the simulator, with a non-degenerate definition;
   - the DRT synthetic financing spread;
   - the 10-year check (A10).
3. MULTI-PERIOD VALUE. The user asked for a multi-period optimizer that shows value, and the year-1 contingent plans failed out of sample. Specify the honest test of multi-period value:
   - rolling re-optimization at year 1 (E3/MPC) on a subsample of certification paths, if it fits the runtime budget;
   - a one-decision-plus-standing-rule policy (SYN L10) as the comparison.
   If MPC cannot be built in the prototype, say why and mark it planned.
4. WORK PACKAGES: 4 to 7, in execution order. Each is a coherent unit one agent can implement and test in about an hour. Give for each:
   - id (WP-0, WP-1, ...), title, issue IDs, files owned, steps and acceptance checks;
   - whether it needs an independent review: true for anything touching the LP, the ledger, the scenario engine, the tree or the simulator.
   WP-0 must add:
   - a FAST SMOKE MODE to the pipeline: a command-line flag (small tree, one book, 1,000 paths, few switch-offs) that finishes in under 3 minutes;
   - a regression harness that prints the key outputs, so every later package can test quickly.
   Order: harness, then LP and ledger correctness, then economics and specification, then measurement and certification, then reporting. Fix all critical and high issues. Fix medium ones unless you justify otherwise in a "Not fixing" list. Fix low ones where cheap.
5. RUNTIME BUDGET for the full run: at most 30 minutes wall-clock on 20 workers. The headline book uses 10,000 certification paths; there are at least 8 replication books. State the paths per book and the resulting precision.
6. RISKS: how each package avoids breaking what works (cash balances, non-anticipativity, determinism, the verified bPOE/CVaR arithmetic).
Also create ${LOG} with a header: title, SYNTHETIC label, base commit ${BASE}, and how entries are written. Return the structured output, with the wps in execution order.`, { label: 'plan', phase: 'Plan', schema: PLAN_SCHEMA })
if (!plan) { log('Planning failed; stopping.'); return { error: 'plan failed' } }
log(`Plan drafted: ${plan.wps.length} work packages over ${plan.issues_total} issues.`)

const crit = await agent(`${COMMON}

TASK: ADVERSARIAL REVIEW of the fix plan ${PLAN}. Check it against verify_math.md, verify_finance.md, the code and the research:
(a) Coverage: is every issue M1-M11, F1-F13 and L1-L5 in the register, with nothing silently dropped or merged away?
(b) Correctness: does each fix remove the root cause rather than the symptom? Is it right mathematically and financially? For example: a draw-accrual fixed point that converges; a red-event definition that is not degenerate; a clustered H6 test that really clusters by book; seeds that are truly independent.
(c) Artefact risk: could any fix create a new way to fake the value-add (tuning, hard limits doing the work, in-sample selection, end-of-horizon effects, mislabelled actions)?
(d) Acceptance checks: can each one fail, and does it test the claim?
(e) Feasibility: package sizes, order and dependencies, the runtime budget and the smoke mode.
(f) Research consistency of every decision.
EDIT ${PLAN} in place to fix what you find, and append a "Plan review" section listing your changes. Do not change code. Return the structured output with the FINAL work-package list in execution order; the implementation agents will follow it.`, { label: 'plan:critic', phase: 'Plan', schema: CRITIC_SCHEMA })
const fin = (crit && crit.wps && crit.wps.length) ? crit : plan
log(`Final plan: ${fin.wps.map(w => w.id).join(', ')}; plan review raised ${crit ? crit.problems.length : 'no'} problems.`)

phase('Implement')
const done = []
const reviews = []
const isSha = s => typeof s === 'string' && /^[0-9a-f]{7,40}$/.test(s.trim())
for (const wp of fin.wps) {
  const r = await agent(`${COMMON}

TASK: implement work package ${wp.id}, "${wp.title}" (issues ${wp.issues.join(', ')}), exactly as specified in ${PLAN}; then test, log and commit it.
1. Read ${PLAN}: the global rules, the issue-register rows for your issues, and your package. Read ${LOG}: what earlier packages changed and what they left open. If ${LOG} already has a completed entry for ${wp.id} (from an interrupted earlier attempt), check that the code still contains the change, re-run its acceptance checks, and finish only what is missing.
2. Before changing anything, run the smoke mode (if it exists yet) to confirm the pipeline works as you found it. If an earlier package left it broken, fix that first and log it.
3. Implement. Keep the code's existing style. params.json keeps a unit, rationale and source for every value.
4. Run every acceptance check for your package, and the smoke mode. Fix until they pass, or record honestly why a check fails.
5. Append your entry to ${LOG}: changes by file and function; issue IDs; each check with its command and result; decisions made, with their research source; open items for later packages.
6. Commit only the files you changed, with the message "MPO v2 fix ${wp.id}: <short title>" (identity and trailer as in ENVIRONMENT). Return the structured output, including the full commit SHA.`, { label: `impl:${wp.id}`, phase: 'Implement', schema: WP_SCHEMA })
  if (!r) {
    log(`${wp.id}: the implementation agent failed; stopping before the run.`)
    const rv = (await Promise.all(reviews)).filter(Boolean)
    return { plan: { wps: fin.wps.map(w => w.id), decisions: fin.decisions }, done, reviews: rv, stopped_at: wp.id }
  }
  done.push(r)
  log(`${wp.id}: ${r.status}, commit ${r.commit}; closed ${r.issues_closed.join(' ') || '-'}${r.issues_open.length ? '; open ' + r.issues_open.join(' ') : ''}; smoke ${r.smoke_ok ? 'ok' : 'FAILING'}`)
  if (wp.review && isSha(r.commit)) {
    const sha = r.commit.trim()
    const wt = `${SCR}\\wt_${wp.id}`
    reviews.push(agent(`${COMMON}

TASK: ADVERSARIAL REVIEW of work package ${wp.id}, "${wp.title}" (issues ${wp.issues.join(', ')}), as committed in ${sha}.
Another agent is already editing the working tree for the next package. So do NOT edit or run anything in ${ROOT} itself. Create an isolated worktree:
  & '${GIT}' -C ${ROOT} worktree add --detach ${wt} ${sha}
and run all checks inside it, using at most 8 workers (tools\\vpy.py and tools\\bgrun.py work from a worktree). Remove it at the end:
  & '${GIT}' -C ${ROOT} worktree remove --force ${wt}
Read the package spec in ${PLAN}, the issue texts in verify_math.md and verify_finance.md, the ${LOG} entry, and the diff (& '${GIT}' -C ${ROOT} show ${sha}). Check:
(a) Does each change remove the ROOT CAUSE of its issue?
(b) New bugs: signs, units, stage and node indexing, double counting, the cash-balance and non-anticipativity invariants, determinism.
(c) Do the acceptance checks really test the claims? Re-run them; can they fail?
(d) Was any parameter changed without a research source or an [A] label? Does any change tune toward a headline?
(e) Does the smoke mode still run?
Write ${EX}\\fix_reviews\\${wp.id}.md (create the folder if needed) and return the structured issues: severity critical, high, medium or low, each with a concrete fix. Do not edit any other project file.`, { label: `review:${wp.id}`, phase: 'Implement', schema: REVIEW_SCHEMA }).then(v => (v ? { wp: wp.id, v } : null)))
  }
}
const revs = (await Promise.all(reviews)).filter(Boolean)
const serious = revs.flatMap(x => x.v.issues.filter(i => i.severity !== 'low').map(i => ({ wp: x.wp, id: i.id, severity: i.severity, issue: i.issue, fix: i.fix })))
log(`Reviews returned: ${revs.length}; findings of medium severity or worse: ${serious.length}.`)

phase('Fixup')
let fx = null
if (serious.length) {
  fx = await agent(`${COMMON}

TASK: apply the independent review findings for the fix work packages. Findings of medium severity or worse, by package:
${JSON.stringify(serious, null, 1)}
The full reviews are in ${EX}\\fix_reviews\\. For each finding, fix it; if you conclude it is wrong, say why with evidence. Re-run the affected acceptance checks and the smoke mode. Append a "Review fixes" section to ${LOG}. Commit with the message "MPO v2 fix: review fixes". Return the structured output.`, { label: 'fixup', phase: 'Fixup', schema: FIXUP_SCHEMA })
  log(fx ? `Fixup: ${fx.fixed} fixed, ${fx.rejected.length} rejected; smoke ${fx.smoke_ok ? 'ok' : 'FAILING'}.` : 'Fixup agent failed.')
}

phase('Run')
const run = await agent(`${COMMON}

TASK: the FULL RUN after all fixes.
1. Read ${PLAN} and ${LOG}. Run the full pipeline (detached; see ENVIRONMENT). Then run it a second time and confirm that the determinism hash and the results are identical. If the run fails or a result is implausible, debug and fix it, and log that in ${LOG}. Never tune toward a headline.
2. Make sure results.json and RESULTS.md are regenerated by the code (report.py). RESULTS.md must now:
   - lead with the defensible out-of-sample headline: value at equal tail clustered across the replication books, with the opportunistic Sharpe at its prior mean, on both NAV bases and per CMA world;
   - show the corrected change list with honest labels;
   - have a "Verification" section that lists every issue from verify_math.md and verify_finance.md with its status (fixed / partly fixed / not fixed, with the reason) and evidence, plus the checks re-run after the fixes;
   - include a table of pre-fix vs post-fix headline numbers, with pre-fix values taken from git ${BASE}.
3. Update the module docstrings and RESULTS.md section 11 (spec conformance) so they list exactly what is and is not implemented.
4. Commit with the message "MPO v2 fix: full re-run (results regenerated)". Return the structured output.`, { label: 'run', phase: 'Run', schema: RUN_SCHEMA })
if (run) log(`Run: ${Math.round(run.runtime_s)}s, determinism ${run.determinism_identical ? 'identical' : 'DIFFERS'}; P(goal) OOS status quo ${run.p_goal_oos.status_quo}, optimized ${run.p_goal_oos.optimized}; value at equal tail ${run.value_at_equal_tail_pp}.`)

return {
  plan: { wps: fin.wps.map(w => ({ id: w.id, title: w.title, issues: w.issues })), decisions: fin.decisions, not_fixing: fin.not_fixing, runtime_budget: fin.runtime_budget, plan_review_problems: crit ? crit.problems : null },
  wps: done.map(d => ({ id: d.wp_id, status: d.status, commit: d.commit, closed: d.issues_closed, open: d.issues_open, smoke_ok: d.smoke_ok, failed_checks: d.checks.filter(c => !c.pass).map(c => c.name + ': ' + c.detail) })),
  reviews: revs.map(x => ({ wp: x.wp, verdict: x.v.verdict, counts: ['critical', 'high', 'medium', 'low'].map(s => s + ':' + x.v.issues.filter(i => i.severity === s).length).join(' ') })),
  fixup: fx,
  run,
}
