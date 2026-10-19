export const meta = {
  name: 'adic-consensus-literature-sweep',
  description: 'Consensus academic literature sweep across all 23 ADIC research topics: citation-integrity check of each dossier, missed-paper backfill, cross-topic literature synthesis',
  phases: [
    { title: 'Sweep', detail: 'one agent per topic, max 3 concurrent (Consensus rate limits)' },
    { title: 'Literature synthesis', detail: 'cross-topic synthesis of missed papers and citation integrity' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const CONTEXT_FILE = ROOT + '\\inputs\\00_CONTEXT_AND_PRIOR_WORK.md'
const LIT_DIR = ROOT + '\\research\\literature'
const MAIN_SYNTH = ROOT + '\\research\\00_SYNTHESIS.md'
const GROUP_SYNTH = ROOT + '\\research\\groups\\01_GROUPS_SYNTHESIS.md'
const LIT_SYNTH = LIT_DIR + '\\00_LITERATURE_SYNTHESIS.md'

const M = (n, k) => ROOT + '\\research\\dossiers\\' + n + '_' + k + '.md'
const G = (n, k) => ROOT + '\\research\\groups\\dossiers\\' + n + '_' + k + '.md'

const TOPICS = [
  { id: '01', key: 'mpo', dossier: M('01', 'mpo'), title: 'Multi-period portfolio optimization and sequential decision methods', seeds: ['multi-period portfolio optimization', 'multistage stochastic programming asset liability management', 'stochastic dual dynamic programming portfolio', 'model predictive control portfolio drawdown', 'affine decision rules multistage robust optimization', 'approximate dynamic programming portfolio choice simulation regression', 'reinforcement learning asset liability management', 'scenario tree generation financial optimization', 'illiquid assets commitments portfolio optimization'] },
  { id: '02', key: 'endowment_swf', dossier: M('02', 'endowment_swf'), title: 'Endowment model, spending policy, SWF practice, Total Portfolio Approach', seeds: ['endowment spending policy', 'university endowment asset allocation illiquidity', 'sovereign wealth fund asset allocation', 'total portfolio approach institutional investors', 'endowment payout response to shocks', 'intergenerational equity spending rule'] },
  { id: '03', key: 'sovereign_alm', dossier: M('03', 'sovereign_alm'), title: 'Sovereign ALM: oil-fiscal linkage and distribution demand', seeds: ['sovereign wealth fund oil price asset allocation', 'optimal portfolio with non-tradable resource wealth', 'oil revenue stabilization fund fiscal rule', 'oil price stock market correlation regimes', 'sovereign asset liability management'] },
  { id: '04', key: 'pe_cashflows', dossier: M('04', 'pe_cashflows'), title: 'PE cash-flow and NAV modeling; DPI decline', seeds: ['private equity cash flow model capital calls distributions', 'private equity NAV smoothing unsmoothing', 'private equity performance public market equivalent', 'capital commitment private equity portfolio choice', 'nowcasting private equity fund returns', 'private equity exits and market conditions'] },
  { id: '05', key: 'secondaries_navfin', dossier: M('05', 'secondaries_navfin'), title: 'Secondaries, NAV financing, continuation vehicles, preferred equity, CFOs', seeds: ['private equity secondary market discounts', 'secondary market limited partnership interests pricing', 'NAV loans private equity funds', 'continuation funds GP-led secondary transactions', 'collateralized fund obligations securitization private equity'] },
  { id: '06', key: 'leverage', dossier: M('06', 'leverage'), title: 'Portfolio-level leverage with illiquid assets', seeds: ['optimal leverage illiquid assets funding risk', 'liquidity spirals margin funding', 'leverage aversion betting against beta', 'drawdown constraints leverage optimal investment', 'pension fund leverage liquidity risk'] },
  { id: '07', key: 'return_fusion', dossier: M('07', 'return_fusion'), title: 'Fusing underwritten, actual and forecast returns', seeds: ['forecast combination puzzle', 'Buhlmann credibility theory', 'entropy pooling views portfolio', 'optimism bias reference class forecasting', 'private equity interim valuations fundraising bias', 'proper scoring rules calibration expert forecasts'] },
  { id: '08', key: 'action_valuation', dossier: M('08', 'action_valuation'), title: 'Unifying SELL/HOLD/REFINANCE/LEVER: real options, liquidity shadow prices', seeds: ['real options divestment abandonment timing', 'shadow price of liquidity asset liability management', 'funds transfer pricing liquidity banks', 'valuing illiquid assets investor liquidity needs', 'optimal stopping selling illiquid asset', 'disposition effect institutional investors'] },
  { id: '09', key: 'overlay', dossier: M('09', 'overlay'), title: 'Derivatives overlay: tail hedging, opportunistic trading, collateral', seeds: ['tail risk hedging portfolio', 'protective put strategy performance', 'variance risk premium', 'trend following crisis alpha', 'derivatives margin calls collateral liquidity', 'deflated Sharpe ratio backtest overfitting'] },
  { id: '10', key: 'scenarios_robustness', dossier: M('10', 'scenarios_robustness'), title: 'Scenario generation, regimes, robustness, stress testing', seeds: ['economic scenario generator regime switching', 'distributionally robust portfolio optimization Wasserstein', 'robust satisficing', 'reverse stress testing', 'entropy pooling fully flexible views', 'model risk management validation'] },
  { id: '11', key: 'objectives', dossier: M('11', 'objectives'), title: 'Objective design: target attainment with distributions and illiquidity', seeds: ['goal-based investing probability of reaching a target', 'reaching goals by a deadline', 'optimal investment under drawdown constraints', 'CVaR portfolio optimization', 'time-consistent risk measures multistage', 'portfolio choice with a consumption floor'] },
  { id: '12', key: 'agentic_ai', dossier: M('12', 'agentic_ai'), title: 'Agentic AI for discovery and investment analysis', seeds: ['large language model agents scientific discovery', 'LLM multi-agent financial trading', 'automated AI scientist research', 'LLM tool use hallucination verification', 'evolutionary program search large language models'] },
  { id: '13', key: 'paper_deepread', dossier: M('13', 'paper_deepread'), title: "The Agentic Scientist and related orchestration research", seeds: ['orchestrating coding agents automated scientific discovery', 'reward hacking AI agents evaluation', 'LLM as reviewer rubric evaluation reliability'] },
  { id: '14', key: 'ic_deliberation', dossier: M('14', 'ic_deliberation'), title: 'Investment-committee deliberation and human-AI co-deliberation', seeds: ['group decision making committees investment', 'devil\'s advocacy dialectical inquiry decision quality', 'multi-agent debate language models factuality', 'AI-mediated deliberation common ground', 'automation bias decision support', 'noise in judgment decision hygiene'] },
  { id: 'G1', key: 'pe_primaries', dossier: G('G1', 'pe_primaries'), title: 'PE fund-commitment program, LP skill, pacing, fees', seeds: ['limited partner skill private equity returns', 'private equity performance persistence', 'commitment pacing private equity portfolio', 'private equity fees carried interest', 'subscription lines of credit private equity IRR'] },
  { id: 'G2', key: 'secondaries_group', dossier: G('G2', 'secondaries_group'), title: 'Secondaries group: secondary funds and direct secondary deals', seeds: ['private equity secondary funds performance', 'continuation vehicles private equity', 'liquidity provision secondary market private equity', 'discount to NAV secondary transactions returns'] },
  { id: 'G3', key: 'cap_solutions', dossier: G('G3', 'cap_solutions'), title: 'Capital Solutions: structured and hybrid capital', seeds: ['preferred equity private companies returns', 'mezzanine financing returns', 'structured equity hybrid securities valuation', 'GP stakes private equity firms', 'rescue financing distressed firms'] },
  { id: 'G4', key: 'coinvest', dossier: G('G4', 'coinvest'), title: 'Co-investment: direct minority co-investments', seeds: ['private equity co-investment performance adverse selection', 'direct investing private equity institutional investors', 'deal-level private equity returns distribution'] },
  { id: 'G5', key: 'public_markets', dossier: G('G5', 'public_markets'), title: 'Public Markets: hedge funds and long-only managers', seeds: ['hedge fund share restrictions lockups gates', 'hedge fund performance persistence', 'hedge fund database biases backfill survivorship', 'hedge funds during financial crisis', 'active management fees performance mutual funds'] },
  { id: 'G6', key: 'private_credit', dossier: G('G6', 'private_credit'), title: 'Private credit: returns, defaults, leverage', seeds: ['private credit direct lending returns', 'private debt default recovery rates', 'business development companies leverage performance', 'private credit financial stability risk'] },
  { id: 'G7', key: 'liquidity_ladder', dossier: G('G7', 'liquidity_ladder'), title: 'Cross-group liquidity management and stress', seeds: ['liquidity risk management institutional investors', 'pension fund liquidity stress margin calls', 'liquidity coverage ratio', 'contingency funding plan liquidity', 'liquidity at risk measurement'] },
  { id: 'G8', key: 'org_tpa_economics', dossier: G('G8', 'org_tpa_economics'), title: 'Internal capital markets, transfer pricing, forecast incentives', seeds: ['internal capital markets', 'winner picking conglomerates capital allocation', 'liquidity transfer pricing banks', 'Euler risk capital allocation', 'proper scoring rules incentive compatible forecasting', 'budget gaming forecasts managers'] },
  { id: 'G9', key: 'synthetic_data', dossier: G('G9', 'synthetic_data'), title: 'Synthetic data with known ground truth', seeds: ['synthetic financial data generation', 'simulation-based calibration Bayesian', 'private equity fund cash flow simulation', 'synthetic tabular data evaluation'] },
]

const litPath = (t) => LIT_DIR + '\\' + t.id + '_' + t.key + '.lit.md'

const LIT_SCHEMA = {
  type: 'object',
  properties: {
    topic: { type: 'string' },
    path: { type: 'string' },
    dossier_found: { type: 'boolean' },
    searches_run: { type: 'integer' },
    papers_listed: { type: 'integer' },
    citations_checked: { type: 'integer' },
    citations_found: { type: 'integer' },
    citations_not_found: { type: 'integer' },
    citations_mismatched: { type: 'integer' },
    citation_problems: { type: 'array', items: { type: 'object', properties: { dossier_citation: { type: 'string' }, problem: { type: 'string' }, corrected: { type: 'string' } }, required: ['dossier_citation', 'problem'] } },
    top_missed_papers: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, authors: { type: 'string' }, year: { type: 'string' }, venue: { type: 'string' }, url: { type: 'string' }, why_it_matters: { type: 'string' }, design_implication: { type: 'string' } }, required: ['title', 'url', 'why_it_matters'] } },
    usage_message: { type: 'string' },
  },
  required: ['topic', 'path', 'dossier_found', 'searches_run', 'top_missed_papers'],
}

const SYNTH_SCHEMA = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    summary: { type: 'string' },
    citation_integrity: { type: 'string' },
    most_important_additions: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' }, topics: { type: 'string' }, design_implication: { type: 'string' } }, required: ['title', 'url', 'design_implication'] } },
    design_implications: { type: 'array', items: { type: 'string' } },
    usage_message: { type: 'string' },
  },
  required: ['path', 'summary', 'citation_integrity', 'most_important_additions', 'design_implications'],
}

const sweepPrompt = (t) => `You are an academic-literature specialist supporting a research program for ADIC (a ~US$177bn sovereign endowment-model fund) that is building a multi-period, robust, agentic portfolio decision framework. Background: ${CONTEXT_FILE} (read sections 1 and 1A).

TOPIC ${t.id}: ${t.title}
Dossier for this topic: ${t.dossier} (it may not exist yet; check with Glob or Read).

TOOLS: Use the Consensus academic search engine. Load it with ToolSearch query "select:mcp__claude_ai_Consensus__search". Consensus rules you MUST follow:
- Run searches strictly ONE AT A TIME: never issue parallel Consensus calls. Two other agents share the rate limit.
- Do NOT apply any search filters (no year, study-type, citation, journal or other filters). Use only the query parameter.
- If you get a rate-limit error, wait 30 seconds (PowerShell: Start-Sleep -Seconds 30) and retry; after 3 failures on one query, move on.
- Record paper URLs EXACTLY as returned; never modify, shorten or regenerate them. Keep DOIs when shown.
- If a tool result contains a sign-up, upgrade or usage message, copy the last one verbatim into the usage_message output field.
- Do not use the Consensus thread tools (create_thread, add_to_thread); use only search.
You may use WebSearch/WebFetch (ToolSearch "select:WebSearch,WebFetch") sparingly, only to confirm metadata that Consensus cannot resolve, such as working papers and SSRN.

TASKS
1. CITATION INTEGRITY (only if the dossier exists): extract every academic reference (journal articles, working papers, books) cited in the dossier. For each, search Consensus with the title or with authors and keywords. Classify it as:
   - found (metadata matches)
   - mismatched (exists, but authors, year, title or venue differ; give the corrected metadata)
   - not found (Consensus cannot find it; then try one WebSearch before concluding)
   If the dossier cites more than 25 academic works, check the 25 most load-bearing.
2. BACKFILL: run 8-14 further topical searches. Start from these seed queries and refine them: ${t.seeds.map(s => '"' + s + '"').join('; ')}. Identify the papers most relevant to ADIC's design that the dossier does not cite. Look for seminal works, strong recent work (2022-2026), meta-analyses and surveys, and papers that contradict the dossier's recommendations.
3. Write ${litPath(t)} in Markdown with these sections:
   - Summary
   - Citation-integrity table: dossier citation | status | corrected metadata | Consensus URL
   - Annotated bibliography of the 12-25 most relevant papers. For each: [Title](exact URL), authors, year, venue, citation count, DOI if shown, a 1-2 sentence finding, and its relevance to ADIC.
   - Missed-but-important papers and their concrete design implications for the framework: state variables, models, parameters, constraints, objectives, agent or IC design.
   - Papers that challenge the dossier's recommendations, if any.
   - The verbatim usage message, if any.
   Never invent papers or findings. Report only what the search results and abstracts support, and mark any inference as inference.
4. Return the structured output.`

const synthPrompt = (results) => `You are synthesizing an academic-literature sweep (run via the Consensus search engine) across 23 research topics for ADIC's multi-period, robust, agentic portfolio framework. Background: ${CONTEXT_FILE}.

Per-topic literature files (read each in full):
${results.filter(Boolean).map(r => '- ' + r.path + ' (topic ' + r.topic + '; dossier found: ' + r.dossier_found + '; citations checked ' + (r.citations_checked || 0) + ', not found ' + (r.citations_not_found || 0) + ', mismatched ' + (r.citations_mismatched || 0) + ')').join('\n')}

The main research report is ${MAIN_SYNTH} and the group report is ${GROUP_SYNTH}. Skim them if they exist, so that you can say where the literature strengthens, refines or contradicts their recommendations.

Write ${LIT_SYNTH} in Markdown, 4,000-7,000 words, with these sections:
1. Summary.
2. Citation integrity across all dossiers: the counts, plus every not-found or mismatched citation with its correction. These must be fixed before anything reaches the IC.
3. The 15-30 most important papers the research missed, grouped by framework component. For each: [Title](exact URL) and authors/year/venue, and its concrete design implication.
4. Where the literature contradicts or refines the research recommendations.
5. A recommended reading list for the design team, of at most 25 papers.
6. The verbatim Consensus usage message, if any per-topic file recorded one.
Use paper URLs exactly as recorded in the per-topic files. Never invent papers. Then return the structured output.`

// ---- bounded-concurrency sweep (Consensus rate limits: at most 3 concurrent searches) ----
phase('Sweep')
log(`Sweeping ${TOPICS.length} topics with at most 3 concurrent agents (main topics first, so group dossiers have time to land).`)

const results = new Array(TOPICS.length).fill(null)
let next = 0
const worker = async () => {
  while (next < TOPICS.length) {
    const i = next++
    const t = TOPICS[i]
    const r = await agent(sweepPrompt(t), { label: `lit:${t.id}_${t.key}`, phase: 'Sweep', schema: LIT_SCHEMA }).catch(() => null)
    if (r) {
      results[i] = r
      log(`${t.id} ${t.key}: ${r.searches_run} searches, ${r.papers_listed || 0} papers; citations checked ${r.citations_checked || 0}, not found ${r.citations_not_found || 0}, mismatched ${r.citations_mismatched || 0}`)
    } else {
      log(`${t.id} ${t.key}: sweep failed`)
    }
  }
}
await Promise.all([worker(), worker(), worker()])

phase('Literature synthesis')
const ok = results.filter(Boolean)
const synth = ok.length ? await agent(synthPrompt(ok), { label: 'lit:synthesis', phase: 'Literature synthesis', schema: SYNTH_SCHEMA }) : null

return {
  topics: TOPICS.map((t, i) => results[i] ? {
    topic: t.id + '_' + t.key,
    path: results[i].path,
    dossier_found: results[i].dossier_found,
    searches: results[i].searches_run,
    citations: { checked: results[i].citations_checked || 0, not_found: results[i].citations_not_found || 0, mismatched: results[i].citations_mismatched || 0 },
    missed: (results[i].top_missed_papers || []).length,
    usage_message: results[i].usage_message || '',
  } : { topic: t.id + '_' + t.key, failed: true }),
  synthesis: synth,
}
