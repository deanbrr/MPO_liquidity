export const meta = {
  name: 'adic-citation-consistency-fix',
  description: 'Apply the literature audit: re-run the co-investment barrier statistics, re-check unchecked citations via free indexes, fix citations/usage errors file by file, apply main-vs-group consistency edits, verify and log',
  phases: [
    { title: 'Prepare', detail: 'barrier re-run (G4) and re-check of citations left unchecked by the Consensus quota' },
    { title: 'Fix', detail: 'one editor per research file or file family applies every relevant correction' },
    { title: 'Verify', detail: 'sample-check the applied fixes and write the change log' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const PY = ROOT + '\\.venv\\Scripts\\python.exe'
const R = ROOT + '\\research'
const LIT = R + '\\literature'
const LIT_SYNTH = LIT + '\\00_LITERATURE_SYNTHESIS.md'
const RECHECK = LIT + '\\recheck'
const LOG = LIT + '\\01_CITATION_FIX_LOG.md'

const MAIN = [
  ['01', 'mpo'], ['02', 'endowment_swf'], ['03', 'sovereign_alm'], ['04', 'pe_cashflows'], ['05', 'secondaries_navfin'],
  ['06', 'leverage'], ['07', 'return_fusion'], ['08', 'action_valuation'], ['09', 'overlay'], ['10', 'scenarios_robustness'],
  ['11', 'objectives'], ['12', 'agentic_ai'], ['13', 'paper_deepread'], ['14', 'ic_deliberation'],
]
const GROUPS = [
  ['G1', 'pe_primaries'], ['G2', 'secondaries_group'], ['G3', 'cap_solutions'], ['G4', 'coinvest'], ['G5', 'public_markets'],
  ['G6', 'private_credit'], ['G7', 'liquidity_ladder'], ['G8', 'org_tpa_economics'], ['G9', 'synthetic_data'],
]

const COMMON = `PROJECT: ADIC multi-period robust portfolio framework research corpus at ${R}. A literature audit (${LIT_SYNTH}, section 2) found, across 574 checked citations: 12 not found (10 exist, none fabricated), 24 mismatched metadata, 16 usage errors that misstate a source (one changes numbers: the co-investment Broadie-Glasserman-Kou barrier correction), reference-hygiene problems (section 2.5) and 5 cross-file inconsistencies (section 2.6). Per-topic detail is in ${LIT}\\NN_key.lit.md and ${LIT}\\GN_key.lit.md (citation-integrity tables).
RULES: Do not browse for anything beyond what a correction needs. Do NOT use Consensus (quota exhausted). To confirm metadata use WebFetch (load via ToolSearch "select:WebFetch,WebSearch") on api.crossref.org/works?query.bibliographic=... , api.crossref.org/works/<DOI>, api.openalex.org/works?search=... , or the publisher/DOI page. Never invent a citation, DOI, page range or number; if you cannot confirm something, leave the original and mark it "[unverified: reason]". The Windows shell resets its cwd every call: use absolute paths. Python: ${PY}.`

const BARRIER_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string' },
    direction_explanation: { type: 'string' },
    scripts: { type: 'array', items: { type: 'string' } },
    results: { type: 'array', items: { type: 'object', properties: { metric: { type: 'string' }, old_value: { type: 'string' }, new_value: { type: 'string' }, where_used: { type: 'string' } }, required: ['metric', 'old_value', 'new_value', 'where_used'] } },
    notes_path: { type: 'string' },
  },
  required: ['summary', 'direction_explanation', 'results', 'notes_path'],
}
const RECHECK_SCHEMA = {
  type: 'object',
  properties: {
    topic: { type: 'string' },
    checked: { type: 'integer' }, ok: { type: 'integer' }, not_found: { type: 'integer' }, mismatched: { type: 'integer' },
    fixes: { type: 'array', items: { type: 'object', properties: { citation: { type: 'string' }, problem: { type: 'string' }, correction: { type: 'string' }, source_url: { type: 'string' } }, required: ['citation', 'problem', 'correction'] } },
    path: { type: 'string' },
  },
  required: ['topic', 'checked', 'ok', 'not_found', 'mismatched', 'fixes', 'path'],
}
const FIX_SCHEMA = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'string' } },
    applied: { type: 'array', items: { type: 'object', properties: {
      file: { type: 'string' }, location: { type: 'string' },
      kind: { type: 'string', enum: ['metadata', 'usage', 'missing_reference', 'inconsistency', 'consistency_edit', 'barrier_rerun', 'recheck'] },
      before: { type: 'string' }, after: { type: 'string' },
    }, required: ['file', 'location', 'kind', 'before', 'after'] } },
    skipped: { type: 'array', items: { type: 'object', properties: { item: { type: 'string' }, reason: { type: 'string' } }, required: ['item', 'reason'] } },
  },
  required: ['files', 'applied', 'skipped'],
}
const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    log_path: { type: 'string' },
    sampled: { type: 'integer' }, correct: { type: 'integer' },
    problems: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, issue: { type: 'string' } }, required: ['file', 'issue'] } },
    summary: { type: 'string' },
  },
  required: ['log_path', 'sampled', 'correct', 'problems', 'summary'],
}

// ---------------- Prepare ----------------
phase('Prepare')
const RECHECK_TOPICS = [['10', 'scenarios_robustness', 37], ['G3', 'cap_solutions', 12], ['14', 'ic_deliberation', 10], ['11', 'objectives', 6], ['13', 'paper_deepread', 4]]
const prep = await parallel([
  () => agent(`${COMMON}

TASK: fix the co-investment barrier-correction usage error and re-run the affected statistics.
The literature audit (${LIT_SYNTH} section 2.4 item 1, and ${LIT}\\G4_coinvest.lit.md) says: the co-investment dossier (${R}\\groups\\dossiers\\G4_coinvest.md) writes the Broadie-Glasserman-Kou discrete-monitoring correction as exp(-0.5826 sigma sqrt(Delta)), which raises survival, while the calculation script applies no correction at all; it recommends kappa_D * exp(+0.5826 sigma sqrt(Delta)) (Broadie, Glasserman & Kou 1997, Mathematical Finance 7(4):325-349), and asks to re-run every barrier statistic built on quarterly monitoring (the wipe-out and LTV-breach rates in the group report's finding 8 may be understated).
1. Verify the correct direction from first principles and the paper: when a continuously monitored barrier (wipe-out or covenant level below the current value) is approximated by quarterly simulation, which way must the barrier be shifted so that the discrete simulation matches continuous monitoring? Write the reasoning down.
2. Find the scripts that produced the barrier statistics (Grep under ${R}\\groups for "0.5826", "barrier", "wipe", "LTV" in .py files, e.g. the G4 verification calcs and ${R}\\groups\\addenda\\*_calcs). Copy them to ${R}\\groups\\addenda\\G4_barrier_rerun\\ (never edit originals), apply the correct shift, and re-run with ${PY}. Also run a fine-grid (e.g. monthly or weekly) simulation as an independent check that the corrected quarterly result approximates continuous monitoring.
3. Report old versus new values for every affected statistic, and where each is quoted (G4 dossier, GC1 cluster, the group report ${R}\\groups\\01_GROUPS_SYNTHESIS.md, the main report ${R}\\00_SYNTHESIS.md - Grep for the old values).
Write ${R}\\groups\\addenda\\G4_barrier_rerun\\RESULTS.md (label figures SYNTHETIC). Do not edit any report; editors in the next step will apply your results. Return the structured output.`, { label: 'barrier-rerun', phase: 'Prepare', schema: BARRIER_SCHEMA }),
  ...RECHECK_TOPICS.map(([n, k, cnt]) => () => agent(`${COMMON}

TASK: re-check the citations in topic ${n} (${k}) that were left unchecked when the Consensus quota ran out (about ${cnt} works). Find them in ${LIT}\\${n}_${k}.lit.md (look for "unchecked", "quota" or similar) and the corresponding dossier (${n.startsWith('G') ? R + '\\groups\\dossiers\\' + n + '_' + k + '.md' : R + '\\dossiers\\' + n + '_' + k + '.md'}).
For each work: confirm it exists and that authors, year, title, venue, volume/pages and DOI are right (Crossref/OpenAlex via WebFetch; publisher pages); where the dossier attributes a specific finding or number to it, check the abstract or an accessible version and say whether the usage is accurate. Record verdicts: ok / not_found / mismatched (with the correction) / usage problem.
Write ${RECHECK}\\${n}_${k}.recheck.md (table: citation | verdict | correction | source URL). Do not edit any dossier. Return the structured output.`, { label: `recheck:${n}`, phase: 'Prepare', schema: RECHECK_SCHEMA })),
])
const barrier = prep[0]
const rechecks = prep.slice(1).filter(Boolean)
log(barrier ? `Barrier re-run done: ${barrier.results.length} statistics updated.` : 'Barrier re-run FAILED: editors will leave barrier numbers flagged as provisional.')
for (const rc of rechecks) log(`Re-check ${rc.topic}: ${rc.ok}/${rc.checked} ok, ${rc.not_found} not found, ${rc.mismatched} mismatched, ${rc.fixes.length} fixes`)

const BARRIER_TXT = barrier
  ? `BARRIER RE-RUN RESULTS (apply wherever the old values appear; cite ${barrier.notes_path}):\nDirection: ${barrier.direction_explanation}\n` + barrier.results.map(x => `- ${x.metric}: ${x.old_value} -> ${x.new_value} (quoted in: ${x.where_used})`).join('\n')
  : `BARRIER RE-RUN FAILED: where co-investment wipe-out or LTV-breach rates built on quarterly monitoring appear, add "[provisional: discrete-monitoring barrier correction under review, see literature synthesis 2.4 item 1]".`
const RECHECK_TXT = rechecks.length
  ? 'RE-CHECK RESULTS for previously unchecked citations (apply where these works are cited):\n' + rechecks.map(rc => `Topic ${rc.topic} (${rc.path}):\n` + rc.fixes.map(f => `- ${f.citation}: ${f.problem} -> ${f.correction}${f.source_url ? ' [' + f.source_url + ']' : ''}`).join('\n')).join('\n')
  : 'RE-CHECK RESULTS: none available.'

// ---------------- Fix ----------------
phase('Fix')
const editorPrompt = (scope, files, extra) => `${COMMON}

YOU EDIT ONLY THESE FILES (no other file): 
${files.map(f => '- ' + f).join('\n')}
SCOPE: ${scope}

SOURCES OF CORRECTIONS:
1. ${LIT_SYNTH} section 2 (2.2 not found, 2.3 mismatched, 2.4 usage errors, 2.5 reference hygiene, 2.6 cross-file inconsistencies). Read it fully.
2. The per-topic citation-integrity tables relevant to your files (${LIT}\\*.lit.md; for a dossier, its own topic file).
3. ${BARRIER_TXT}
4. ${RECHECK_TXT}
${extra || ''}
PROCEDURE: for every correction, Grep your file(s) for the cited work (author names, years, titles, DOIs) or the affected number/claim; apply the correction with the Edit tool. Metadata fixes: correct the reference entry and in-text citation. Usage fixes: reword the claim so it matches the source, or correct the number; if a corrected number changes a conclusion in the same file, update that conclusion too and mark it "[corrected 2026-10-18: ...]". Missing references: add full entries. Cross-file inconsistencies: apply the resolution given; where the audit says "confirm", check via Crossref/OpenAlex and apply what you confirm. Do not touch anything else; keep tables valid. At the end of each edited file, append (or extend) a section "## Citation corrections (2026-10-18)" listing each change in one line. If your file has a verification log that the audit says wrongly accepted something, you may add one erratum line to that log only if it is in your file list.
Return the structured output listing every change (before/after) and every correction you skipped and why.`

const TASKS = [
  ...MAIN.map(([n, k]) => ({ label: `fix:${n}`, scope: `stream ${n} (${k}) dossier and its verification log`, files: [`${R}\\dossiers\\${n}_${k}.md`, `${R}\\verification\\${n}_${k}.verify.md`] })),
  ...GROUPS.map(([n, k]) => ({ label: `fix:${n}`, scope: `group stream ${n} (${k}) dossier and its verification log`, files: [`${R}\\groups\\dossiers\\${n}_${k}.md`, `${R}\\groups\\verification\\${n}_${k}.verify.md`] })),
  { label: 'fix:clusters', scope: 'the four main cluster syntheses', files: [`${R}\\clusters\\C1_portfolio_math.md`, `${R}\\clusters\\C2_private_liquidity.md`, `${R}\\clusters\\C3_liabilities_overlay.md`, `${R}\\clusters\\C4_agentic_ic.md`] },
  { label: 'fix:group-clusters', scope: 'the two group cluster syntheses', files: [`${R}\\groups\\clusters\\GC1_private_groups.md`, `${R}\\groups\\clusters\\GC2_liquidity_org_data.md`] },
  { label: 'fix:main-addenda', scope: 'the five main gap addenda', files: [1, 2, 3, 4, 5].map(i => `${R}\\addenda\\gap_0${i}.md`),
    extra: `5. CONSISTENCY ITEM from the group report's question 12: strike the "10.5-11%" citation from gap_02 section 2.1 (it is not supported; record what you removed).` },
  { label: 'fix:group-addenda', scope: 'the four group gap addenda', files: [1, 2, 3, 4].map(i => `${R}\\groups\\addenda\\gap_0${i}.md`) },
  { label: 'fix:main-synthesis', scope: 'the main synthesis v1.1 (body and bibliography, section 11)', files: [`${R}\\00_SYNTHESIS.md`],
    extra: `5. CONSISTENCY EDITS requested by the group report v1.1 (question 12; read ${R}\\groups\\01_GROUPS_SYNTHESIS.md section 0 ledger and ${R}\\groups\\addenda\\gap_01.md section 5): apply groups gap_01 section 5's replacement text to the main report (finding 5, section 2.3(d), section 4.9, section 6.2); set LR1/T3 to 1.91x on CF-controlled HQLA where the main report says otherwise; remove "NAV-facility documents activated" from the main CFP Amber row; reconcile the main section 4.11 "<= 6 exact-Shapley" rule with the group report. Record each as kind consistency_edit.` },
  { label: 'fix:group-synthesis', scope: 'the seven-group synthesis v1.1 (body and bibliography)', files: [`${R}\\groups\\01_GROUPS_SYNTHESIS.md`],
    extra: `5. Apply the barrier re-run results to the group report's finding 8 and wherever wipe-out or LTV-breach rates are quoted, updating dependent statements.` },
]
log(`Applying corrections with ${TASKS.length} editors (one per file or file family).`)
const fixes = await parallel(TASKS.map(t => () => agent(editorPrompt(t.scope, t.files, t.extra), { label: t.label, phase: 'Fix', schema: FIX_SCHEMA }).then(r => r ? { ...r, label: t.label } : null)))
const okFix = fixes.filter(Boolean)
const failedFix = TASKS.filter((t, i) => !fixes[i]).map(t => t.label)
if (failedFix.length) log(`Editors that failed: ${failedFix.join(', ')}`)
const nApplied = okFix.reduce((a, f) => a + f.applied.length, 0)
const nSkipped = okFix.reduce((a, f) => a + f.skipped.length, 0)
log(`Applied ${nApplied} changes; skipped ${nSkipped}.`)

// ---------------- Verify ----------------
phase('Verify')
const CHANGES = okFix.map(f => `### ${f.label}\n` + f.applied.map(a => `- [${a.kind}] ${a.file} @ ${a.location}: "${(a.before || '').slice(0, 160)}" -> "${(a.after || '').slice(0, 160)}"`).join('\n') + (f.skipped.length ? '\nSkipped:\n' + f.skipped.map(s => `- ${s.item}: ${s.reason}`).join('\n') : '')).join('\n\n')
const verify = await agent(`${COMMON}

TASK: verify the applied corrections and write the change log.
The editors reported these changes (truncated quotes):
${CHANGES}
${failedFix.length ? 'Editors that FAILED (their files were not corrected): ' + failedFix.join(', ') : ''}

1. Sample at least 30 changes across files (all barrier_rerun and consistency_edit changes, plus a spread of usage, metadata and missing-reference fixes). Open each file and confirm the change is present, correct against ${LIT_SYNTH} section 2 (or the re-check/barrier results), and did not break surrounding text or tables.
2. Grep for the audit items that no editor reported (compare section 2 of ${LIT_SYNTH} with the change list) and list anything left unfixed.
3. Write ${LOG}: summary counts; a table of every change by file (kind, location, before -> after); skipped items with reasons; verification results; items still open (including any that need ADIC or a user decision, and works still unverifiable).
Return the structured output.`, { label: 'verify-log', phase: 'Verify', schema: VERIFY_SCHEMA })

return {
  barrier: barrier ? { summary: barrier.summary, results: barrier.results } : null,
  rechecks: rechecks.map(rc => ({ topic: rc.topic, checked: rc.checked, ok: rc.ok, not_found: rc.not_found, mismatched: rc.mismatched })),
  applied: nApplied, skipped: nSkipped, failed_editors: failedFix,
  verification: verify,
}
