export const meta = {
  name: 'adic-build-wave0',
  description: 'Build wave 0 of the ADIC TPA lab per BUILD_SPEC: WP-01 contracts (incl. analyst contracts), then WP-02 rng/numerics/stats, WP-03 testing kit + walking skeleton, WP-04 registry; each verified against the spec and fixed; integration run',
  phases: [
    { title: 'Contracts', detail: 'WP-01: pyproject, contracts, taxonomy config, analyst contracts; verify; fix' },
    { title: 'Foundations', detail: 'WP-02, WP-03, WP-04 in parallel, each implement -> verify -> fix' },
    { title: 'Integrate', detail: 'full test suite, layering, walking skeleton; final fixes; readiness to tag contracts-v1.0' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const PY = ROOT + '\\.venv\\Scripts\\python.exe'
const UV = 'C:\\Users\\dean\\AppData\\Local\\Microsoft\\WinGet\\Packages\\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\\uv.exe'
const SPEC = ROOT + '\\design\\BUILD_SPEC.md'
const ARCH = ROOT + '\\design\\ARCHITECTURE.md'
const CHAT = ROOT + '\\design\\addenda\\CHAT_ANALYST.md'
const BUILDLOG = ROOT + '\\design\\build_log'

const COMMON = `You are a senior Python engineer building the ADIC Agentic Total-Portfolio Laboratory from its build specification.
AUTHORITY: ${SPEC} (BUILD_SPEC v1.1, ~450 KB; use Grep to find headings, then Read the ranges you need). Read §0 (how to use it, precedence, the spec-level ADRs S-ADR-*), §1 (global conventions: units, time, signs, arrays, seeds, ids, logging, errors, config, SYNTHETIC labelling, determinism) and §2 (package layout) before writing code, then the sections for your work package. ${ARCH} and ${CHAT} (the conversational-analyst addendum; its §5 is binding for contracts/analyst.py) are context; BUILD_SPEC wins on interfaces unless it says otherwise.
ENVIRONMENT: Windows 11, PowerShell 5.1 (no &&; the cwd resets after every call, so use absolute paths everywhere). Python 3.12 venv: ${PY} (the bare "python" command does not work). uv: ${UV} (install into the venv with: & "${UV}" pip install --python "${PY}" <args>). Git is at C:\\Program Files\\Git\\cmd\\git.exe but DO NOT commit, tag or push: the orchestrator commits. Installed: numpy, scipy, pandas, pyarrow, cvxpy (HiGHS/CLARABEL/OSQP/SCS/ECOS), highspy, statsmodels, scikit-learn, hmmlearn, arch, numba, pydantic 2, typer, rich, jinja2, plotly, matplotlib, pytest, hypothesis, anthropic 1.15, mcp 2.3. No network access is needed or allowed for code paths; never add a dependency the spec does not list.
RULES: follow the package layout (src layout, import name adic_tpa) and the exact names, signatures, types, shapes, dtypes and units in BUILD_SPEC; where the spec is ambiguous, choose the simplest reading consistent with §0-§3, implement it, and record the decision as a deviation in your output (never silently). Match the surrounding code style: typed, small modules, docstrings that cite the BUILD_SPEC section, comments only where the reasoning is non-obvious. Every test runs offline and fast (unit tests < 1 s each unless the spec says otherwise). Run tests with: & "${PY}" -m pytest <paths> -q -p no:cacheprovider. Write only files your work package owns (BUILD_SPEC §2 and §9.2); if you need a change in a file another WP owns, do not edit it: report it in contract_issues (or interface_issues). Never write real ADIC data; everything synthetic carries the SYNTHETIC labels of §1.12.`

const IMPL_SCHEMA = {
  type: 'object',
  properties: {
    wp: { type: 'string' },
    files: { type: 'array', items: { type: 'string' } },
    tests_passed: { type: 'integer' },
    tests_failed: { type: 'integer' },
    failures: { type: 'array', items: { type: 'string' } },
    dod: { type: 'array', items: { type: 'object', properties: { item: { type: 'string' }, met: { type: 'boolean' }, evidence: { type: 'string' } }, required: ['item', 'met', 'evidence'] } },
    deviations: { type: 'array', items: { type: 'string' } },
    contract_issues: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['wp', 'files', 'tests_passed', 'tests_failed', 'failures', 'dod', 'deviations', 'contract_issues'],
}
const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    wp: { type: 'string' },
    report_path: { type: 'string' },
    tests_passed: { type: 'integer' },
    tests_failed: { type: 'integer' },
    issues: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] }, location: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'location', 'issue', 'fix'] } },
    verdict: { type: 'string' },
  },
  required: ['wp', 'report_path', 'tests_passed', 'tests_failed', 'issues', 'verdict'],
}
const FIX_SCHEMA = {
  type: 'object',
  properties: { wp: { type: 'string' }, fixed: { type: 'integer' }, not_fixed: { type: 'array', items: { type: 'string' } }, tests_passed: { type: 'integer' }, tests_failed: { type: 'integer' }, summary: { type: 'string' } },
  required: ['wp', 'fixed', 'not_fixed', 'tests_passed', 'tests_failed', 'summary'],
}
const INTEG_SCHEMA = {
  type: 'object',
  properties: { tests_passed: { type: 'integer' }, tests_failed: { type: 'integer' }, skeleton_green: { type: 'boolean' }, layering_green: { type: 'boolean' }, ready_to_tag: { type: 'boolean' }, blockers: { type: 'array', items: { type: 'string' } }, report_path: { type: 'string' }, summary: { type: 'string' } },
  required: ['tests_passed', 'tests_failed', 'skeleton_green', 'layering_green', 'ready_to_tag', 'blockers', 'report_path', 'summary'],
}

const reviewPrompt = (wp, scope) => `${COMMON}

TASK: adversarial SPEC-CONFORMANCE REVIEW of ${wp} (${scope}). Do not trust the implementer's report. Run its tests and the whole current suite (${ROOT}\\tests). Compare every public name, signature, type, shape, dtype, unit and invariant in the code against BUILD_SPEC (the §3 contracts and the §4 module section for ${wp}, §9.2 definition of done, §10 test plan items for ${wp}); check determinism (keyed RNG, no global state), SYNTHETIC labelling, error types (§1.10), config handling (§1.11), and that no test is vacuous (tests must fail on a plausible bug: mutate one line mentally and ask whether a test catches it). Check the DoD items one by one with evidence. Severity: critical = wrong numbers, broken determinism or a contract that other WPs will build against incorrectly; high = a DoD item unmet or a spec signature mismatch; medium = ambiguity or weak tests; low = polish.
Write ${BUILDLOG}\\review_${wp}.md and return the structured issues. Do not edit code.`

const fixPrompt = (wp, scope, review) => `${COMMON}

TASK: fix ${wp} (${scope}) using the review ${review ? review.report_path : '(review missing: re-run the tests and fix failures)'}: fix every critical and high issue and the medium ones unless you justify not doing so; keep to the files ${wp} owns (report anything else as contract_issues in your summary); re-run the WP's tests and the full suite until green. Return the structured summary.`

// ---------------- WP-01 ----------------
phase('Contracts')
const wp01 = await agent(`${COMMON}

WORK PACKAGE WP-01 (wave 0): contracts, pyproject.toml, .gitattributes, tools/dev_install.py, config/taxonomy/* (see BUILD_SPEC §9.2 row WP-01, §2, §3 in full, §4.1, §1.11, §1.12, and CHAT_ANALYST §5.1, §5.3, §6.3 for contracts/analyst.py, i.e. WP-CHAT-01).
Deliver: every §3 model and enum (including the recourse protocol, BeliefDraws, the contexts, the LLM draft models and contracts/analyst.py), ids, arrays (dtype aliases and ARRAY_SPECS), units, calendar, hashing including canonical_artifact_hash, signing, contracts.rules (pure functions shared by owner, ledger, priv and H), errors, the JSON-mode config loader, the Protocols in contracts/ports.py, and taxonomy v1/v2 as configuration (eight groups in v2 including REAL_ASSETS; no hard-coded group ids anywhere: the group set comes from config). pyproject.toml must pin exactly what the spec pins and install the package in editable mode into the venv (& "${UV}" pip install --python "${PY}" -e "${ROOT}"); create tools/dev_install.py as specified.
Tests per §4.1 (including config round trip, LF-normalized hashing, signing, units, calendar, enum and schema tests such as additionalProperties false / no root anyOf for tool and analyst schemas) plus test_no_hardcoded_group_ids and the import-allowlist harness (tests/layering) described in §4.0, which later WPs extend.
Do NOT tag contracts (the walking skeleton from WP-03 must be green first). Return the structured output.`, { label: 'WP-01:implement', phase: 'Contracts', schema: IMPL_SCHEMA })
if (!wp01) { log('WP-01 failed; stopping wave 0.'); return { wp01: null } }
log(`WP-01: ${wp01.files.length} files, tests ${wp01.tests_passed} passed / ${wp01.tests_failed} failed, ${wp01.deviations.length} deviations.`)
const rev01 = await agent(reviewPrompt('WP-01', 'contracts, pyproject, taxonomy config, analyst contracts'), { label: 'WP-01:review', phase: 'Contracts', schema: REVIEW_SCHEMA })
const fix01 = await agent(fixPrompt('WP-01', 'contracts, pyproject, taxonomy config, analyst contracts', rev01), { label: 'WP-01:fix', phase: 'Contracts', schema: FIX_SCHEMA })
log(`WP-01 after fix: ${fix01 ? fix01.tests_passed + ' passed / ' + fix01.tests_failed + ' failed' : 'fix failed'}.`)

// ---------------- WP-02..04 ----------------
phase('Foundations')
const WPS = [
  { wp: 'WP-02', scope: 'rng, numerics, stats', body: `BUILD_SPEC §9.2 row WP-02, §1.7 (seeds: keyed counter-based Philox streams, key from SHA-256, counter from (path, month), vectorized blocks), §4.2 rng (incl. samplers: vectorized inverse-CDF, one uniform per variate), §4.3 numerics (PWL, roots, linalg helpers), §4.4 stats (Clopper-Pearson, bootstrap, Holm, alpha-investing/mFDR, DSR, PBO, MDE, bPOE, CE conversion per §1.2). DoD: §4.2-4.4 tests; numpy-Philox equivalence; throughput >= 50M uniforms/s (measure and report; a perf test may be marked slow).` },
  { wp: 'WP-03', scope: 'testing kit, research-fixture port, walking skeleton', body: `BUILD_SPEC §9.2 row WP-03, §4.5 testing, §10.4 golden files. Deliver: mini book (allocation v1 and v2), mini cube, mini FlowCube, fixture tree, fake engines and ledger, fixture H (LPModel, HSolution, DualSet, Tree from the gap_02 export), fakes for the stress filter, owner draws and belief draws, the synthetic committee, golden loader, tools/port_research.py with research fixtures copied read-only from ${ROOT}\\research (hf_ladder, t1_engine ladder readings, gap_02 and groups gap_01 coefficient exports, the gap_02 G*(theta) grid and per-model gap quantiles, perf golden cases, bridge, v8 replica, SIMM example, sealed PE history) each with SHA-256 in a port manifest, and the WALKING SKELETON (§4.5): the thinnest end-to-end path through the frozen Protocols on mini_book that must be green before contracts are tagged. DoD: frozen checksums committed (write them; the orchestrator commits), skeleton green, fakes pass Protocol conformance, manifest lists every source file and hash.` },
  { wp: 'WP-04', scope: 'registry', body: `BUILD_SPEC §9.2 row WP-04 and §4.6: SQLite + artifact store, append-only hash chain, metric registry, provenance (run_id:artifact:path references), mFDR table; tamper drill test. Keep everything under the run directory conventions of §1 and §2 (runs/ is git-ignored).` },
]
const found = await pipeline(
  WPS,
  (w) => agent(`${COMMON}

WORK PACKAGE ${w.wp} (wave 0): ${w.scope}. ${w.body}
WP-01 (contracts) is implemented; build against its public API. If a contract is missing or wrong, do not edit contracts: report it in contract_issues and work around it with the narrowest local adapter, marked TODO(contracts).
Return the structured output.`, { label: `${w.wp}:implement`, phase: 'Foundations', schema: IMPL_SCHEMA }),
  (impl, w) => impl ? agent(reviewPrompt(w.wp, w.scope), { label: `${w.wp}:review`, phase: 'Foundations', schema: REVIEW_SCHEMA }).then(r => ({ impl, review: r })) : null,
  (x, w) => x ? agent(fixPrompt(w.wp, w.scope, x.review), { label: `${w.wp}:fix`, phase: 'Foundations', schema: FIX_SCHEMA }).then(f => ({ ...x, fix: f })) : null,
)
for (let i = 0; i < WPS.length; i++) {
  const x = found[i]
  log(x ? `${WPS[i].wp}: impl ${x.impl.tests_passed}/${x.impl.tests_failed}; review ${x.review ? x.review.issues.length + ' issues' : 'n/a'}; after fix ${x.fix ? x.fix.tests_passed + ' passed / ' + x.fix.tests_failed + ' failed' : 'n/a'}` : `${WPS[i].wp}: FAILED`)
}

// ---------------- Integrate ----------------
phase('Integrate')
const contractIssues = [wp01, ...found.map(x => x && x.impl)].filter(Boolean).flatMap(r => r.contract_issues || [])
const integ = await agent(`${COMMON}

TASK: wave-0 INTEGRATION. You may edit any wave-0 file (contracts, rng, numerics, stats, testing, registry, pyproject, tests) to make the wave coherent.
1. Apply these contract issues raised by WP-02..04 where they are valid against BUILD_SPEC (record each decision): ${JSON.stringify(contractIssues).slice(0, 6000)}
2. Remove TODO(contracts) local adapters once contracts are fixed.
3. Run the full suite (${ROOT}\\tests), the layering/allowlist tests and test_no_hardcoded_group_ids; make the walking skeleton green on mini_book; confirm determinism (run the skeleton twice: identical canonical hashes).
4. Check the wave-0 gate in BUILD_SPEC §9.1 (walking skeleton green, frozen fixture checksums present, layering and allowlist tests active) and say whether contracts are ready to tag contracts-v1.0 (the orchestrator tags).
Write ${BUILDLOG}\\wave0_integration.md (test counts, gate checklist with evidence, every change made, remaining blockers) and return the structured output.`, { label: 'wave0:integrate', phase: 'Integrate', schema: INTEG_SCHEMA })

return {
  wp01: { impl: { files: wp01.files.length, passed: wp01.tests_passed, failed: wp01.tests_failed, deviations: wp01.deviations }, review: rev01 && { issues: rev01.issues.length, verdict: rev01.verdict }, fix: fix01 },
  foundations: found.map((x, i) => x ? { wp: WPS[i].wp, impl: { files: x.impl.files.length, passed: x.impl.tests_passed, failed: x.impl.tests_failed, deviations: x.impl.deviations }, review: x.review && { issues: x.review.issues.length, verdict: x.review.verdict }, fix: x.fix } : { wp: WPS[i].wp, failed: true }),
  integration: integ,
}
