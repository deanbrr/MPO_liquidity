export const meta = {
  name: 'adic-research-sufficiency-audit',
  description: 'Audit whether the research answers each part of the ADIC task: per-requirement evidence audit, adversarial challenge, sufficiency matrix and verdict',
  phases: [
    { title: 'Audit', detail: 'one auditor per requirement/question maps research evidence, numbers and gaps' },
    { title: 'Challenge', detail: 'one skeptic per audit checks numbers against files and tries to refute sufficiency' },
    { title: 'Synthesize', detail: 'sufficiency matrix, overall verdict, ranked gaps and what can be told to the IC today' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const P = (rel) => `${ROOT}\\${rel}`
const OUT = P('research\\sufficiency')

const CORPUS = `
RESEARCH CORPUS (all on disk, read-only for you; use Grep to find the relevant sections, then Read them; do not read every file whole):
- Requirements: ${P('design\\00_DESIGN_BRIEF.md')} (R1-R15, P1-P15, section 5 decisions, section 7 literature refinements); client facts and the prior deck: ${P('inputs\\00_CONTEXT_AND_PRIOR_WORK.md')}.
- Master synthesis v1.1: ${P('research\\00_SYNTHESIS.md')} (sections 0-11; evidence tags [S] sourced, [C] checked/computed, [I] inference/working assumption).
- Group layer: ${P('research\\groups\\01_GROUPS_SYNTHESIS.md')} (may be mid-revision; use what is on disk), group addenda ${P('research\\groups\\addenda')}\\gap_*.md, group dossiers ${P('research\\groups\\dossiers')}, group verification logs ${P('research\\groups\\verification')}, group clusters ${P('research\\groups\\clusters')}.
- Gap addenda: ${P('research\\addenda')}\\gap_01.md .. gap_05.md (+ *_calcs folders with scripts and results JSON).
- Stream dossiers 01-14: ${P('research\\dossiers')}; adversarial verification logs: ${P('research\\verification')} (incl. 13_paper_deepread.localcheck.md for The Agentic Scientist); cluster syntheses: ${P('research\\clusters')}.
- Literature sweep: ${P('research\\literature\\00_LITERATURE_SYNTHESIS.md')} (citation audit section 2, missed papers section 3, verdicts on recommendations section 4) and per-topic files ${P('research\\literature')}\\*.lit.md.
- The paper: ${P('inputs\\agentic_scientist_2610.18933v1.txt')} (grep only).
CONTEXT: ADIC, ~$177bn endowment-model sovereign fund; owner-set distribution 5-10% a year (exogenous stochastic liability); 10% nominal USD target; leverage allowed; ~60% private, mostly PE, declining DPI; big multi-asset OTC overlay (tail hedge + opportunistic book); seven investment groups (PE funds, Secondaries hybrid fund+direct, Capital Solutions, Co-investment, Public Markets HF+long-only, Private Credit, Overlay); Corporate Finance owns Treasury (facilities, collateral, distributions, FTP). REFINANCE = cash-out against a holding; LEVER = borrow to add exposure. All quantitative results in the research are on a SYNTHETIC ADIC-like book unless stated otherwise.
RULES: Read-only on everything except your own output file. No web browsing and no Consensus (quota exhausted). Every number you report must carry its source (file + section) and evidence tag, and be labeled SYNTHETIC where it comes from the synthetic book. Do not inflate: "the research proposes X" is not "the research shows X works". Distinguish four readiness levels: enough to DESIGN the component; enough to BUILD it (specified precisely enough to code and test); enough to give the IC a defensible ANSWER today (on synthetic data, with stated uncertainty); and what NEEDS ADIC's REAL DATA.
`

const QUESTIONS = [
  { id: 'Q01', req: 'R1', q: 'Is there a sound, buildable multi-period optimization formulation for ADIC (policy classes, here-and-now scenario program with duals, MPC, policy search), and is it solvable on HiGHS/CLARABEL within the performance targets?' },
  { id: 'Q02', req: 'R2', q: 'Is there a robust scenario-analysis design (scenario generator with oil/fiscal factors and regimes, model worlds/misspecification, stress family, reverse stress, entropy-pooling views) with calibration targets?' },
  { id: 'Q03', req: 'R3', q: 'Can the framework produce credible probabilities of outcomes (P(10%), red events, drawdowns, liquidity breaches) with honest uncertainty across model classes, and what are those probabilities today on the synthetic book?' },
  { id: 'Q04', req: 'R4', q: 'Is the owner-set 5-10% distribution modeled credibly as an exogenous, oil-linked stochastic liability (calibration, Abu Dhabi vs UAE data, owner behavior in crises), and what does it imply for payout sustainability?' },
  { id: 'Q05', req: 'R5', q: 'Can ADIC reach the 10% nominal target? Is there an explicit, evidence-based return bridge (CMA beta to 10%, levers, drags), and what does the research conclude?' },
  { id: 'Q06', req: 'R6', q: 'Is leverage (portfolio and asset level) analysed well enough to decide on it: costs, availability in stress, limits, when it helps or hurts?' },
  { id: 'Q07', req: 'R7', q: 'Is the private book with declining PE DPI modeled well enough: cash-flow and NAV engines per group (PE funds, Secondaries, Co-investment, Capital Solutions, Private Credit), the DPI drought, unfunded commitments, pacing?' },
  { id: 'Q08', req: 'R8', q: 'Is the SELL / HOLD / REFINANCE / LEVER lens specified per group and per asset with instruments, pricing, regime availability, execution lags, and a consistent valuation rule (liquidity price lambda, envelopes, Phase I)?' },
  { id: 'Q09', req: 'R9', q: 'Is the fusion of underwritten, current actual and group-forecast returns (plus a market-implied anchor) specified and evidence-based, including per-group forecast credibility and bias?' },
  { id: 'Q10', req: 'R10', q: 'Is the OTC overlay (tail hedge + opportunistic book) modeled well enough: position/Greek layer, pricing, collateral VM/IM, monetization, net-vega limits, value vs a cash buffer?' },
  { id: 'Q11', req: 'R11', q: 'Is the agentic architecture inspired by The Agentic Scientist correctly grounded in the paper (verified against the full text) and specified well enough to build, with integrity enforced by infrastructure?' },
  { id: 'Q12', req: 'R12', q: 'Is the Investment Committee discussion layer (IC pack, shadow IC, protocol, Q&A, view conditioning, decision log) evidence-based and specified well enough to build?' },
  { id: 'Q13', req: 'R13', q: 'What survives from the user\'s prior deck (v8: two-tier robust target attainment, state/fragility engine, attribution, governance), what changes and why (e.g. the uplift re-estimate), and is that analysis sound?' },
  { id: 'Q14', req: 'R14', q: 'Are the seven groups and Corporate Finance (internal bank) integrated: group taxonomy, group-specific actions, internal capital market (FTP curve, quantity envelopes), netting of internal transfers, group credibility, decision rights?' },
  { id: 'Q15', req: 'R15', q: 'Is the synthetic data generator specified with a known ground truth, realistic biases in the three marks, stylized-fact and parameter-recovery checks, and SYNTHETIC labeling, and is its limited role (correctness, not estimator selection) clear?' },
  { id: 'Q16', req: 'cross-cutting', q: 'Liquidity survival and Corporate Finance funding: is the 24-month stress question answered (literal vs calibrated stress, facility needs, IG floor, HF queue, owner band, facility reliability in an oil+crisis state), and is the answer robust to the literature\'s challenges?' },
]

const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    verdict: { type: 'string', enum: ['sufficient', 'mostly_sufficient', 'partial', 'insufficient'] },
    design_ready: { type: 'boolean' },
    build_ready: { type: 'boolean' },
    ic_answer_ready: { type: 'boolean' },
    needs_adic_data: { type: 'boolean' },
    answer_today: { type: 'string' },
    key_numbers: { type: 'array', items: { type: 'object', properties: {
      value: { type: 'string' }, meaning: { type: 'string' }, source: { type: 'string' }, evidence_tag: { type: 'string' },
    }, required: ['value', 'meaning', 'source', 'evidence_tag'] } },
    gaps: { type: 'array', items: { type: 'object', properties: {
      gap: { type: 'string' },
      impact: { type: 'string', enum: ['high', 'medium', 'low'] },
      how_to_close: { type: 'string', enum: ['adic_data', 'build_experiment', 'more_research', 'user_decision'] },
      detail: { type: 'string' },
    }, required: ['gap', 'impact', 'how_to_close', 'detail'] } },
    contradictions: { type: 'array', items: { type: 'string' } },
    path: { type: 'string' },
  },
  required: ['id', 'verdict', 'design_ready', 'build_ready', 'ic_answer_ready', 'needs_adic_data', 'answer_today', 'key_numbers', 'gaps', 'contradictions', 'path'],
}

const CHALLENGE_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    upheld: { type: 'boolean' },
    revised_verdict: { type: 'string', enum: ['sufficient', 'mostly_sufficient', 'partial', 'insufficient'] },
    revised_readiness: { type: 'object', properties: {
      design_ready: { type: 'boolean' }, build_ready: { type: 'boolean' }, ic_answer_ready: { type: 'boolean' }, needs_adic_data: { type: 'boolean' },
    }, required: ['design_ready', 'build_ready', 'ic_answer_ready', 'needs_adic_data'] },
    number_checks: { type: 'array', items: { type: 'object', properties: {
      value: { type: 'string' }, found: { type: 'boolean' }, location: { type: 'string' },
    }, required: ['value', 'found', 'location'] } },
    refuted_claims: { type: 'array', items: { type: 'object', properties: {
      claim: { type: 'string' }, problem: { type: 'string' },
    }, required: ['claim', 'problem'] } },
    missed_gaps: { type: 'array', items: { type: 'object', properties: {
      gap: { type: 'string' },
      impact: { type: 'string', enum: ['high', 'medium', 'low'] },
      how_to_close: { type: 'string', enum: ['adic_data', 'build_experiment', 'more_research', 'user_decision'] },
      detail: { type: 'string' },
    }, required: ['gap', 'impact', 'how_to_close', 'detail'] } },
    path: { type: 'string' },
  },
  required: ['id', 'upheld', 'revised_verdict', 'revised_readiness', 'number_checks', 'refuted_claims', 'missed_gaps', 'path'],
}

const SYNTH_SCHEMA = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    overall_verdict: { type: 'string' },
    matrix: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, req: { type: 'string' }, verdict: { type: 'string' },
      design_ready: { type: 'boolean' }, build_ready: { type: 'boolean' }, ic_answer_ready: { type: 'boolean' }, needs_adic_data: { type: 'boolean' },
      one_line: { type: 'string' },
    }, required: ['id', 'req', 'verdict', 'design_ready', 'build_ready', 'ic_answer_ready', 'needs_adic_data', 'one_line'] } },
    top_gaps: { type: 'array', items: { type: 'object', properties: {
      gap: { type: 'string' }, impact: { type: 'string' }, how_to_close: { type: 'string' }, owner: { type: 'string' },
    }, required: ['gap', 'impact', 'how_to_close', 'owner'] } },
    answers_today: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['path', 'overall_verdict', 'matrix', 'top_gaps', 'answers_today', 'summary'],
}

log(`Auditing ${QUESTIONS.length} requirement questions; each audit is challenged as soon as it lands.`)

const results = await pipeline(
  QUESTIONS,
  (q) => agent(
`You are a research-sufficiency AUDITOR for the ADIC Agentic Total-Portfolio Laboratory. Your question:

${q.id} (${q.req}): ${q.q}

${CORPUS}
TASK: Find everything the research corpus says that bears on this question. Then judge whether it is enough. Write a concise audit (600-1,500 words) to ${OUT}\\${q.id}_audit.md with sections:
1. Answer today: what the research concludes, in plain language, with the key numbers (source + tag + SYNTHETIC label).
2. Evidence: the strongest supporting sources and their strength; any contradictions between files (e.g. synthesis vs group synthesis vs literature verdicts vs verification logs); errors flagged by the literature citation audit that touch this question.
3. Readiness: DESIGN / BUILD / IC ANSWER / NEEDS ADIC DATA, each yes/no with a one-line reason.
4. Gaps: each with impact (high/medium/low) and how to close it (adic_data, build_experiment, more_research, user_decision).
Verdict scale: sufficient (all four readiness levels that can be met without ADIC data are met); mostly_sufficient (design-ready and nearly build-ready, minor gaps); partial (design-ready only, or important open questions); insufficient (cannot design it yet).
Return the structured summary (path = your audit file).`,
    { label: `audit:${q.id}`, phase: 'Audit', schema: AUDIT_SCHEMA }),
  (audit, q) => audit ? agent(
`You are an adversarial SKEPTIC reviewing a research-sufficiency audit for the ADIC Agentic Total-Portfolio Laboratory. Default to doubt: your job is to find where the audit overstates sufficiency or misses gaps.

QUESTION ${q.id} (${q.req}): ${q.q}
AUDIT FILE: ${audit.path}
AUDIT SUMMARY: verdict=${audit.verdict}; design_ready=${audit.design_ready}; build_ready=${audit.build_ready}; ic_answer_ready=${audit.ic_answer_ready}; needs_adic_data=${audit.needs_adic_data}.
KEY NUMBERS CLAIMED:
${audit.key_numbers.map(n => `- ${n.value} | ${n.meaning} | ${n.source} | ${n.evidence_tag}`).join('\n')}

${CORPUS}
TASK:
1. Check up to 10 of the most load-bearing numbers against the files: is the value actually there, in the cited place, with the stated meaning? Use Grep. Record found=true/false and the exact location.
2. Try to refute the readiness claims: is the component really specified precisely enough to BUILD (equations, parameters, interfaces), or only described? Is the IC ANSWER defensible given model-class ranges, synthetic data and the literature's contested/contradicted verdicts (00_LITERATURE_SYNTHESIS section 4)? Are there unresolved contradictions across files?
3. List gaps the auditor missed.
Then give a revised verdict and readiness (keep the auditor's if it survives). Write your challenge (400-1,000 words) to ${OUT}\\${q.id}_challenge.md and return the structured summary (path = your challenge file).`,
    { label: `challenge:${q.id}`, phase: 'Challenge', schema: CHALLENGE_SCHEMA }).then(ch => ({ q, audit, challenge: ch })) : null,
)

const done = results.filter(Boolean)
const failed = QUESTIONS.filter((q, i) => !results[i]).map(q => q.id)
if (failed.length) log(`Questions without a completed audit+challenge: ${failed.join(', ')}`)
for (const r of done) {
  const v = r.challenge ? r.challenge.revised_verdict : r.audit.verdict
  log(`${r.q.id}: auditor=${r.audit.verdict}, skeptic=${r.challenge ? r.challenge.revised_verdict : 'n/a'}${r.challenge && !r.challenge.upheld ? ' (downgraded)' : ''}`)
}

phase('Synthesize')
const LIST = done.map(r => `- ${r.q.id} (${r.q.req}): audit ${r.audit.path}; challenge ${r.challenge ? r.challenge.path : 'none'}; auditor verdict ${r.audit.verdict}; skeptic verdict ${r.challenge ? r.challenge.revised_verdict : 'n/a'}`).join('\n')
const synth = await agent(
`You are the lead research reviewer. Produce the definitive answer to the user's question: "Did the research find enough information to solve or answer the ADIC task?" The task (the user's own words, summarized): build a multi-period optimization framework for ADIC's ~$177bn endowment-model fund (owner-set 5-10% distributions, 10% target, leverage, ~60% private with declining PE DPI) with robust scenario analysis and probabilities of outcomes, a SELL / HOLD / REFINANCE / LEVER lens per strategy/asset, fusion of underwritten / current / forecast returns, a large OTC overlay (tail hedge + opportunistic), an agentic architecture inspired by The Agentic Scientist, and IC discussion of the results; the user's prior deck answered an "ADIC Data Science Lead Case Study".

${CORPUS}
AUDITS AND CHALLENGES (read every one; where the skeptic and auditor disagree, decide and say why):
${LIST}

WRITE ${P('research\\00_RESEARCH_SUFFICIENCY.md')} with:
1. Verdict (one paragraph): enough to design? to build? to answer the IC today (on synthetic data)? to solve it for ADIC's real portfolio? Be direct and honest.
2. Sufficiency matrix: one row per question (Q01-Q16) with requirement, final verdict, DESIGN / BUILD / IC ANSWER / NEEDS ADIC DATA, and a one-line answer.
3. What we can tell the IC today: the 8-12 most important answers with numbers (each labeled SYNTHETIC, with model-class range and source).
4. What the research could not settle: ranked gaps (impact, how to close: ADIC data request / build-time experiment / further research after the Consensus quota resets on 1 November / user decision; and who owns it: user, Corporate Finance, a named group, Risk, the build).
5. Evidence-quality caveats: synthetic data; unchecked citations (~69 because of the quota); citation and usage errors still to fix (including the co-investment barrier-correction sign error); preprints; model-class M6.
6. A data request list for ADIC (what real data would most change the answers), ordered by value.
Keep it to about 2,500-4,000 words; tables first, prose second. Return the structured summary.`,
  { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA })

return {
  audited: done.map(r => ({ id: r.q.id, req: r.q.req, auditor: r.audit.verdict, skeptic: r.challenge ? r.challenge.revised_verdict : null, upheld: r.challenge ? r.challenge.upheld : null, numbers_checked: r.challenge ? r.challenge.number_checks.length : 0, numbers_not_found: r.challenge ? r.challenge.number_checks.filter(n => !n.found).length : 0 })),
  failed,
  synthesis: synth,
}
