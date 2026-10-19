export const meta = {
  name: 'adic-real-assets-research',
  description: 'Real Assets (8th ADIC group): 6 research streams, adversarial fact-check, synthesis with spec card, critic, gap-fill, revision, quantitative re-run with Real Assets, integration memo',
  phases: [
    { title: 'Research', detail: '6 Real Assets research streams (G10-G15), each writes a dossier' },
    { title: 'Verify', detail: 'adversarial fact-check of each dossier (pipelined)' },
    { title: 'Synthesis', detail: 'Real Assets group report with specification card' },
    { title: 'Critique', detail: 'completeness critic vs R14/R15, buildability, consistency' },
    { title: 'Gap-fill', detail: 'close high-severity gaps and revise the Real Assets report' },
    { title: 'Integrate', detail: 'quantitative re-run with Real Assets; integration memo for reports and design' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const PY = ROOT + '\\.venv\\Scripts\\python.exe'
const CONTEXT_FILE = ROOT + '\\inputs\\00_CONTEXT_AND_PRIOR_WORK.md'
const BRIEF_FILE = ROOT + '\\design\\00_DESIGN_BRIEF.md'
const MAIN_DOSSIERS = ROOT + '\\research\\dossiers'
const MAIN_SYNTH = ROOT + '\\research\\00_SYNTHESIS.md'
const LIT_SYNTH = ROOT + '\\research\\literature\\00_LITERATURE_SYNTHESIS.md'
const G_ROOT = ROOT + '\\research\\groups'
const G_SYNTH = G_ROOT + '\\01_GROUPS_SYNTHESIS.md'
const DOSSIER_DIR = G_ROOT + '\\dossiers'
const VERIFY_DIR = G_ROOT + '\\verification'
const ADDENDA_DIR = G_ROOT + '\\addenda'
const RA_SYNTH = G_ROOT + '\\02_REAL_ASSETS_SYNTHESIS.md'
const RA_INTEG = G_ROOT + '\\03_REAL_ASSETS_INTEGRATION.md'
const RA_CALCS = ADDENDA_DIR + '\\ra_integration_calcs'

const BRIEF = `CLIENT BRIEF (full detail in ${CONTEXT_FILE}: read section 1A first; design brief ${BRIEF_FILE} section 8 holds the interim Real Assets rules):
ADIC runs a ~US$177bn endowment-model portfolio for a sovereign owner. The owner sets an annual distribution of 5-10% of the fund (an exogenous, stochastic liability, likely higher when oil is weak). Return target 10% nominal USD; leverage permitted; ~60% private markets (mostly PE) with declining PE distributions (DPI). The framework under construction is a multi-period robust optimization lab with probabilities of outcomes, a SELL / HOLD / REFINANCE / LEVER lens for every strategy and asset (REFINANCE = raise cash against a holding without selling it, i.e. cash-out; LEVER = borrow to add exposure), fusion of three return series per asset (underwritten, current actual, group forecast) plus a market-implied anchor, a large OTC overlay (tail hedge + opportunistic book), an agentic architecture, and IC discussion.
ADIC has EIGHT investment groups: PE funds; Secondaries (hybrid fund + direct); Capital Solutions; Co-investment; Public Markets (hedge funds + long-only); Private Credit; Overlay; and REAL ASSETS, which the user added after the seven-group research was finished. Corporate Finance (non-investment) owns Treasury and runs the funding/liability side as internal bank (liquidity buffer, facilities, overlay collateral, distribution payments, transfer pricing).
Real Assets working interpretation (to be confirmed by the user; re-read context section 1A before you finalize, because the user's answers may be added there while you work): private real assets - real estate (core to opportunistic), infrastructure (core to value-add, energy transition, digital), possibly energy/natural resources and agriculture/timber - via closed-end funds, open-end core funds, co-investments, joint ventures and direct assets. Working allocation v2: Real Assets $18bn (~10% of NAV) carved out of PE funds ($52bn -> $34bn) so private stays ~60%; Real Assets unfunded ~$4bn. All quantitative work is on a SYNTHETIC book and must be labeled SYNTHETIC.`

const RULES = (path) => `RESEARCH RULES
1. First read ${CONTEXT_FILE} (section 1A) and ${BRIEF_FILE} section 8. Then skim the seven-group report ${G_SYNTH} (its per-group specification format in section 3, the cash map in section 2, the cross-group mechanisms in section 4) and the main report ${MAIN_SYNTH} (sections 1, 2.3, 4.2-4.7) so your work is consistent with them and adds Real Assets depth rather than repeating them. Skim overlapping main dossiers in ${MAIN_DOSSIERS} (03_sovereign_alm for oil/fiscal links, 04_pe_cashflows, 05_secondaries_navfin, 06_leverage, 07_return_fusion, 08_action_valuation, 09_overlay) and group dossiers in ${DOSSIER_DIR}. Never edit any of them.
2. Load web tools with ToolSearch query "select:WebSearch,WebFetch". Use WebSearch mode "standard" for most queries and "extended" for 2025-2026 market data, niche facts, or thin results. Read primary sources with WebFetch (journal/SSRN/NBER pages, index providers, regulator and central-bank reports, reputable practitioner research); WebFetch answers a prompt about the page using a small model, so ask specific extraction questions. Run many searches (typically 25-60) and read the important sources rather than relying on snippets.
3. Do NOT use Consensus (the account's monthly quota is exhausted). For academic metadata use WebFetch on api.crossref.org/works?query=..., api.openalex.org/works?search=..., or api.semanticscholar.org/graph/v1/paper/search?query=... .
4. Today is 2026-10-18. Prefer recent data and give as-of dates. Distinguish (a) sourced facts, (b) practitioner consensus, (c) your own inference.
5. Never fabricate citations, numbers or URLs; say so when you cannot verify. Seed references in your brief are hints from memory: verify authors, year, title and venue before citing. Keep verbatim quotes under 125 characters.
6. Think across disciplines: real-estate economics, infrastructure finance, commodity economics, actuarial smoothing, bank ALM, real options, organizational economics.
7. You may run illustrative calculations with ${PY} (scripts and results in ${ADDENDA_DIR}\\<your stream id>_calcs\\); label outputs SYNTHETIC.
8. Write the dossier in Markdown to ${path} with the Write tool (several writes/edits are fine). Target 4,000-8,000 words, dense and technical, with equations. Sections: 1) Executive summary; 2) Core concepts and theory; 3) Methods/models and trade-offs; 4) Empirical evidence and current market data (dated, sourced); 5) Practitioner and peer practice, case studies; 6) Design implications for the ADIC framework (state and decision variables, constraints, objective terms, equations, parameter defaults, calibration targets, data needs), ending with a SPECIFICATION CARD (a compact table an engineer can implement from: data fields; return, NAV and cash-flow equations; parameter defaults with sources; liquidity terms and stress behaviour; SELL/HOLD/REFINANCE/LEVER definitions and economics; how forecasts are produced and their biases; synthetic-data defaults; links to other groups and Corporate Finance); 7) Implementation notes (Python, algorithms, numerical pitfalls); 8) Risks and limitations; 9) Open questions (what ADIC must supply or confirm); 10) References (full citations with URLs).
9. Return the structured output, faithfully summarizing the dossier. load_bearing_claims = the 10-20 empirical claims or numbers your recommendations depend on most, each with its source URL.`

const STREAMS = [
  { num: 'G10', key: 'ra_real_estate', title: 'Real estate: return, cash-flow, valuation and leverage model for funds, open-end core vehicles, JVs and direct assets', body: `Research:
- Strategy spectrum (core, core-plus, value-add, opportunistic) and sectors (office, logistics, residential, retail, data centers, hospitality, alternatives) across US, Europe, Asia and the GCC. Net-of-fee return, volatility and drawdown by strategy and vehicle (NCREIF NPI and ODCE, MSCI/IPD, INREV, Cambridge Associates, Preqin, MSCI-Burgiss, FTSE Nareit REITs), long-run and 2022-2026, dated.
- Academic evidence (verify every seed): private versus listed real estate after desmoothing and leverage adjustment (e.g. Pagliari, Scherer & Monopoli 2005; Riddiough, Moriarty & Yeatman 2005; Bollinger & Pagliari 2019); pension real-estate performance and intermediation costs (Andonov, Eichholtz & Kok); real-estate fund cash flows and PME evidence; REIT-versus-private pricing (Van Nieuwerburgh and co-authors).
- Cash-flow model: NOI = rent x occupancy - opex; NOI growth versus inflation; maintenance capex and leasing costs; income distributions; development calls; closed-end real-estate fund call/distribution profiles versus PE (Takahashi-Alexander parameters for real estate if published); open-end fund income distributions.
- Valuation: cap-rate model V = NOI_next / (r - g); cap-rate dynamics versus real rates and credit spreads (the 2022-2025 repricing, peak-to-trough by sector and vehicle); appraisal smoothing and lag versus transaction indices (MSCI RCA CPPI, NCREIF TBI) and REITs.
- Leverage: property-level LTV by strategy, DSCR/ICR covenants, fixed versus floating, the 2024-2027 CRE maturity wall (MBA, Trepp, MSCI data), refinancing gaps, extend-and-pretend, CMBS and office delinquency 2023-2026, bank CRE lending standards (Fed SLOOS).
- Crisis behaviour: 2008-09, 2020, 2022-24 (office), Dubai 2008-10; open-end fund redemption queues (ODCE queue as % of NAV 2022-2026; non-traded REIT limits, e.g. BREIT and SREIT 2022-23) as a liquidity-terms state machine.
- How real-estate teams forecast (business plans, underwritten IRR, exit cap rates) and the documented biases (exit cap and rent growth optimism).
- SELL / HOLD / REFINANCE / LEVER for real estate at asset, JV, fund-interest and open-end-unit level, with lags and transfer costs.
Deliverable emphasis: a simulation-ready real-estate model (NOI process, cap-rate process loaded on the scenario factors, appraisal smoothing, leverage and refinancing, open-end queue machine, closed-end fund cash flows) with parameter tables and dated sources.` },

  { num: 'G11', key: 'ra_infrastructure', title: 'Infrastructure: contracted, regulated and GDP-linked assets; cash yield, inflation pass-through, duration and leverage', body: `Research:
- Strategy spectrum (core, core-plus, value-add, opportunistic) and subsectors (regulated utilities, contracted renewables and PPAs, transport GDP-linked assets such as toll roads, airports and ports, midstream energy, digital infrastructure such as towers, fibre and data centers). Net returns, volatility, drawdowns and cash yields by segment (EDHECinfra/Scientific Infra indices, Preqin, Cambridge Associates, MSCI-Burgiss, listed infrastructure indices), dated.
- Academic evidence (verify every seed): institutional infrastructure investing and fund performance (e.g. Andonov, Kraussl & Rauh, Review of Financial Studies 2021); early unlisted infrastructure evidence (e.g. Bitsch, Buchner & Kaserer 2010); long-run listed infrastructure returns (e.g. Bianchi, Bornholt, Drew & Howard 2014); Blanc-Brude and EDHEC work on valuation and discount rates.
- Cash flows and valuation: contracted or regulated yield; inflation pass-through (RAB indexation, tariff escalators, CPI-linked contracts) and its limits; DCF valuation and discount-rate sensitivity (effective duration of core infrastructure); merchant power-price risk; volume risk in transport (2020 airports).
- Leverage: holdco/opco structures, project finance, amortization profiles, covenants, refinancing risk; how much leverage is typical by segment.
- Vehicles and liquidity: closed-end funds, open-end infrastructure funds (redemption terms and queues 2022-2026), GP-led continuation vehicles, direct consortia with sovereign co-investors; secondary pricing for infrastructure fund stakes.
- Energy transition and stranded-asset risk; digital infrastructure's equity-like risk.
- How infrastructure teams forecast and their biases (traffic forecast optimism is well documented, e.g. Flyvbjerg and co-authors; verify).
- SELL / HOLD / REFINANCE / LEVER for infrastructure: stake sell-downs to co-investors, holdco refinancing and recaps, asset-level debt, CV elections.
Deliverable emphasis: a simulation-ready infrastructure model (cash yield with inflation pass-through, discount-rate-driven value, volume/merchant risk by segment, leverage and refinancing, vehicle liquidity) with parameter tables and dated sources.` },

  { num: 'G12', key: 'ra_natural_resources_energy', title: 'Energy and natural resources, agriculture and timber: oil linkage and wrong-way risk with the owner draw', body: `Research:
- Segments: upstream and midstream oil and gas, mining and metals, power generation, timberland, farmland. Returns, volatility, drawdowns and cash yields (Cambridge Associates natural-resources indices, NCREIF Timberland and Farmland, listed proxies), dated; energy-fund performance after 2014 and 2020.
- Oil linkage: the sensitivity of each segment's value and distributions to oil prices and to the oil-fiscal state used in ADIC's scenario generator (main report section 4.1 and stream 03). For a sovereign whose owner depends on oil revenue, oil-linked assets are wrong-way: when oil is weak the owner draws more and these assets fall. Review the sovereign-wealth literature on hedging the oil 'asset in the ground' and underweighting oil-linked assets (verify seeds such as Gintschel & Scherer 2008; van den Bremer, van der Ploeg & Wills 2016; NBIM's 2019 decision to divest upstream oil and gas exposure; IMF work on SWF asset allocation). Quantify the implied correlation and hedging demand where possible.
- Valuation and cash flows: reserve-based NPV under commodity forward curves, depletion, royalties and streaming structures, timber biological growth and harvest optionality, farmland rent plus land value; inflation hedging properties (verify with sources).
- Energy-transition risk: stranded assets, carbon pricing, policy risk.
- How these segments enter the scenario generator (oil factor loadings by regime, commodity-curve shocks) and the Tier-1 stress (the oil-crisis state).
- SELL / HOLD / REFINANCE / LEVER for natural resources (asset sales, reserve-based lending as REFINANCE, streaming and royalty sales as cash-out, hedging production via the overlay).
Deliverable emphasis: segment models with oil and commodity loadings, the wrong-way-risk analysis for ADIC (a clear recommendation on whether and how much oil-linked real-asset exposure ADIC should hold, conditional on the owner's oil dependence), and parameter tables with dated sources.` },

  { num: 'G13', key: 'ra_marks_valuation', title: 'Real Assets marks: underwritten, appraisal-based current, forecast and market-implied; smoothing, bias and credibility', body: `Research:
- The four marks for real assets: underwritten (yield-on-cost, IRR, exit cap rate at underwriting), current (appraisal NAV, lagged and smoothed), group forecast (business-plan re-forecasts), and market-implied (listed REIT and listed-infrastructure NAV premia/discounts, e.g. Green Street NAV tracking; secondary pricing of real-estate and infrastructure fund stakes from Jefferies, Lazard, Evercore and others, dated).
- Appraisal smoothing and desmoothing: Geltner (1993) and Fisher, Geltner & Webb (1994); Getmansky, Lo & Makarov (2004) applied to real assets; more recent unsmoothing methods (e.g. Couts, Goncalves & Rossi; verify); the lead-lag between REITs and private marks; stale pricing in open-end NAVs and the wealth transfer it causes under redemptions.
- Forecast and underwriting bias in real assets: exit-cap and rent-growth optimism, development cost overruns and delays (megaproject evidence), infrastructure traffic-forecast optimism; evidence on appraisal bias around transactions and fundraising.
- How the Forward Belief Engine (main report section 4.3, group report section 5) should treat real assets: a state-space (Kalman) desmoothing of appraisal marks, Bornhuetter-Ferguson/Benktander for closed-end real-asset funds, credibility weights, PIT-based scoring, and the literature's advice to shrink fusion weights toward equal and recalibrate pools (literature synthesis ${LIT_SYNTH} section 4.10).
- Synthetic ground truth for SYN-ADIC-177: a true value process (NOI and cap-rate or cash-yield and discount-rate), smoothing parameter and lag, bias parameters for the underwritten and forecast marks, noise, and the parameter-recovery tests that show the estimators work.
Deliverable emphasis: mark-generation equations, desmoothing and fusion procedures, bias and credibility model with parameters, and synthetic-data defaults with recovery tests.` },

  { num: 'G14', key: 'ra_actions_financing', title: 'Real Assets actions and financing: SELL / HOLD / REFINANCE / LEVER instruments, pricing, availability, lags, and links to Corporate Finance', body: `Research:
- SELL: direct asset and portfolio sales (marketing time, bid-ask, transfer taxes and stamp duties by jurisdiction), JV stake sales, fund LP-interest secondaries for real estate and infrastructure (pricing by strategy and regime, dated), open-end fund redemptions (queues, pro-rata limits, NAV-based exit) versus secondary sales of open-end units.
- REFINANCE (cash-out, keep the asset): cash-out refinancing of property- or asset-level debt (LTV, DSCR, spreads by regime, the 2023 CRE credit crunch), recapitalizations, sale-leasebacks and ground-lease structures, JV or partial-stake sell-downs to co-investors, preferred equity, NAV facilities on real-asset fund interests; their cost of liquidity in the same units the main report uses for PE (main report section 4.4).
- LEVER (exposure-up): acquisition and development financing, subscription lines; how leverage changes risk (unlevering real-estate returns; covenant and refinancing risk).
- Non-recourse asset-level debt versus Corporate Finance's recourse facilities: whether and how asset-level debt should count in ADIC's look-through leverage limits (main report T5), stress behaviour (refinancing walls, covenant cures, equity injections as hidden capital calls), and rate hedging (caps and swaps) through the Overlay group.
- Regime availability and execution lags for every instrument (normal versus stress versus the oil-crisis state).
- Interactions: Private Credit lending to real-estate assets (internal conflicts, zero-sum transfers), Capital Solutions providing preferred equity or NAV loans, Secondaries buying real-asset fund stakes, Corporate Finance's FTP charges and envelopes (group report section 4).
Deliverable emphasis: a real-assets instrument library (cash-flow formulas, pricing, availability by regime, lags, costs) in the same format as the main report's instrument library, with decision rules priced by the liquidity shadow price.` },

  { num: 'G15', key: 'ra_portfolio_role_liquidity', title: 'Real Assets in the total portfolio: inflation and diversification evidence, drought-era cash generation, liquidity ladder, peers and organization', body: `Research:
- Inflation hedging and diversification of real estate, infrastructure and natural resources after desmoothing (verify seeds such as Hoesli, Lizieri & MacGregor 2008; Rodel & Rothballer 2012; recent 2021-2024 inflation-episode evidence). Short-run versus long-run hedging; correlation with equities and rates after desmoothing.
- Cash generation in the 2022-2026 distribution drought: real-estate and infrastructure fund distribution yields versus PE; income yield of core assets; whether Real Assets helps or hurts ADIC's drought cash map (compare with group report section 2).
- Liquidity ladder entries: time-to-cash and stressed haircuts by vehicle (open-end core funds, closed-end funds, JV stakes, direct assets) in normal, stress and oil-crisis states; open-end queue dynamics 2022-2026; encumbrance by asset-level debt.
- Behaviour in the oil-fiscal stress: Gulf real estate's link to oil and government spending (Dubai 2008-10 and later cycles), energy assets, and what this means for ADIC's Tier-1 stress.
- Peer practice: real-asset allocations, vehicles and organization at ADIA, GIC, NBIM (unlisted real estate and renewable infrastructure), CPP Investments, Future Fund, NZ Super, Yale, Harvard, CalPERS and others; direct platforms versus funds; liquidity policies for real assets; dated and sourced.
- Organization: how a Real Assets group should interact with PE, Co-investment, Private Credit, Capital Solutions, Secondaries and Corporate Finance in ADIC's internal capital market (envelopes, FTP, conflicts, deal flow), and what its head brings to the shadow IC.
Deliverable emphasis: the Real Assets row of the cross-group cash map and liquidity ladder (base, drought, T4-prime stress), a peer-based allocation range with rationale, and IC-facing implications.` },
]

const DOSSIER_SCHEMA = {
  type: 'object',
  properties: {
    stream: { type: 'string' },
    dossier_path: { type: 'string' },
    word_count: { type: 'integer' },
    executive_summary: { type: 'string' },
    key_insights: { type: 'array', items: { type: 'string' } },
    design_implications: { type: 'array', items: { type: 'string' } },
    calibration_targets: { type: 'array', items: { type: 'object', properties: { parameter: { type: 'string' }, value: { type: 'string' }, as_of: { type: 'string' }, source: { type: 'string' } }, required: ['parameter', 'value', 'source'] } },
    load_bearing_claims: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, source_url: { type: 'string' }, confidence: { type: 'string', enum: ['high', 'medium', 'low'] } }, required: ['claim', 'confidence'] } },
    open_questions: { type: 'array', items: { type: 'string' } },
  },
  required: ['stream', 'dossier_path', 'executive_summary', 'key_insights', 'design_implications', 'load_bearing_claims'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    stream: { type: 'string' },
    verification_path: { type: 'string' },
    checked: { type: 'integer' },
    confirmed: { type: 'integer' },
    corrected: { type: 'integer' },
    refuted: { type: 'integer' },
    unverifiable: { type: 'integer' },
    corrections: { type: 'array', items: { type: 'object', properties: { original: { type: 'string' }, corrected: { type: 'string' }, source_url: { type: 'string' } }, required: ['original', 'corrected'] } },
    citation_problems: { type: 'array', items: { type: 'string' } },
    reasoning_issues: { type: 'array', items: { type: 'string' } },
    overall_reliability: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
  required: ['stream', 'checked', 'confirmed', 'corrected', 'refuted', 'unverifiable', 'corrections', 'overall_reliability'],
}

const SYNTH_SCHEMA = {
  type: 'object',
  properties: {
    synthesis_path: { type: 'string' },
    word_count: { type: 'integer' },
    executive_summary: { type: 'string' },
    sub_strategies: { type: 'array', items: { type: 'string' } },
    cash_flow_model: { type: 'string' },
    actions: { type: 'string' },
    forecast_bias_model: { type: 'string' },
    liquidity_terms: { type: 'string' },
    synthetic_defaults: { type: 'string' },
    oil_wrong_way_recommendation: { type: 'string' },
    questions_for_user: { type: 'array', items: { type: 'string' } },
  },
  required: ['synthesis_path', 'executive_summary', 'cash_flow_model', 'actions', 'synthetic_defaults', 'questions_for_user'],
}

const CRITIC_SCHEMA = {
  type: 'object',
  properties: {
    gaps: { type: 'array', items: { type: 'object', properties: { gap: { type: 'string' }, severity: { type: 'string', enum: ['high', 'medium', 'low'] }, why_it_matters: { type: 'string' }, research_task: { type: 'string' } }, required: ['gap', 'severity', 'research_task'] } },
    contradictions: { type: 'array', items: { type: 'string' } },
    overall_assessment: { type: 'string' },
  },
  required: ['gaps', 'overall_assessment'],
}

const GAP_SCHEMA = {
  type: 'object',
  properties: { gap: { type: 'string' }, addendum_path: { type: 'string' }, summary: { type: 'string' }, design_changes: { type: 'array', items: { type: 'string' } } },
  required: ['gap', 'addendum_path', 'summary'],
}

const QUANT_SCHEMA = {
  type: 'object',
  properties: {
    results_path: { type: 'string' },
    scripts: { type: 'array', items: { type: 'string' } },
    deltas: { type: 'array', items: { type: 'object', properties: { metric: { type: 'string' }, before_v1: { type: 'string' }, after_v2: { type: 'string' }, note: { type: 'string' } }, required: ['metric', 'before_v1', 'after_v2'] } },
    caveats: { type: 'array', items: { type: 'string' } },
  },
  required: ['results_path', 'deltas', 'caveats'],
}

const INTEG_SCHEMA = {
  type: 'object',
  properties: {
    memo_path: { type: 'string' },
    edits_groups_report: { type: 'integer' },
    edits_main_report: { type: 'integer' },
    edits_design: { type: 'integer' },
    headline_changes: { type: 'array', items: { type: 'string' } },
    questions_for_user: { type: 'array', items: { type: 'string' } },
  },
  required: ['memo_path', 'headline_changes', 'questions_for_user'],
}

const dossierPath = (s) => DOSSIER_DIR + '\\' + s.num + '_' + s.key + '.md'
const verifyPath = (s) => VERIFY_DIR + '\\' + s.num + '_' + s.key + '.verify.md'

// ---------------- Research + Verify (pipelined) ----------------
phase('Research')
log('Launching 6 Real Assets research streams (G10-G15); each is fact-checked as soon as it lands.')
const streamResults = await pipeline(
  STREAMS,
  (s) => agent(`You are a senior research analyst on a multidisciplinary team building a multi-period, robust, agentic portfolio decision framework for a sovereign endowment-model fund.

${BRIEF}

YOUR RESEARCH STREAM ${s.num}: ${s.title}

${s.body}

${RULES(dossierPath(s))}`, { label: `research:${s.num}`, phase: 'Research', schema: DOSSIER_SCHEMA }),
  (r, s) => r ? agent(`You are an adversarial fact-checker for a research program that will inform a sovereign fund's Investment Committee. Catch errors before they reach the IC.

Read the dossier at ${dossierPath(s)} (stream ${s.num}: ${s.title}). Background: ${CONTEXT_FILE} section 1A and ${BRIEF_FILE} section 8.
The author flagged these load-bearing claims:
${JSON.stringify((r && r.load_bearing_claims) || [], null, 1)}

Tasks:
1. Select the 12-18 most load-bearing empirical claims (numbers, dates, market statistics, attributions of findings to specific papers/authors), including the flagged ones and any you find suspicious.
2. Verify each against primary or high-quality sources (load tools via ToolSearch "select:WebSearch,WebFetch"; WebSearch mode "standard", or "extended" for recent/niche data; do NOT use Consensus; for academic metadata use WebFetch on api.crossref.org or api.openalex.org). Verdict per claim: confirmed / corrected (give corrected value and source) / refuted / unverifiable. Default to unverifiable if you cannot find support.
3. Check that the 10 most important references exist with correct authors, year, title and venue.
4. Identify reasoning errors or overclaims in the design implications and specification card (a model that does not do what is claimed, a formula or sign error, a mis-specified constraint, an action not actually available to ADIC as LP, JV partner or owner).
5. Write the verification log in Markdown to ${verifyPath(s)}: summary; claims table (claim | verdict | corrected value | source URL); citation check; reasoning issues; overall reliability.
Do NOT edit the dossier. Return the structured output.`, { label: `verify:${s.num}`, phase: 'Verify', schema: VERIFY_SCHEMA }).then(v => ({ stream: s, dossier: r, verification: v })) : null,
)

const done = streamResults.filter(Boolean)
for (const d of done) {
  const v = d.verification
  log(v ? `Verified ${d.stream.num}: ${v.confirmed}/${v.checked} confirmed, ${v.corrected} corrected, ${v.refuted} refuted, ${v.unverifiable} unverifiable (${v.overall_reliability})` : `${d.stream.num}: verification failed`)
}
const missing = STREAMS.filter((s, i) => !streamResults[i]).map(s => s.num)
if (missing.length) log(`Streams that failed: ${missing.join(', ')}`)

// ---------------- Synthesis ----------------
phase('Synthesis')
const DS = done.map(d => `- ${d.stream.num} ${d.stream.title}: ${dossierPath(d.stream)}${d.verification ? ' | verification: ' + verifyPath(d.stream) : ' | (verification failed: treat numbers with extra caution)'}`).join('\n')
const synthPrompt = `You are the lead author of the REAL ASSETS group report for ADIC's multi-period, robust, agentic portfolio decision framework. It extends the seven-group report ${G_SYNTH} (v1.1) and the main report ${MAIN_SYNTH} (v1.1) to the eighth group and must be consistent with them (same conventions: canonical stress T4-prime, Phase I / priced_on flags, lambda and envelopes, FBE, SYN-ADIC-177 gates).

${BRIEF}

Read ${CONTEXT_FILE} section 1A (check whether the user has confirmed the Real Assets scope, access route or size; if so, follow it and say so) and ${BRIEF_FILE} sections 7-8. Read every dossier and verification log in full:
${DS}
Consult the literature synthesis ${LIT_SYNTH} (sections 3-4) where relevant.

Write ${RA_SYNTH} (8,000-12,000 words, Markdown):
0. Title, date (2026-10-18), scope, relationship to the group and main reports; what the user confirmed and what is a working assumption.
1. Executive summary (at most 1,000 words).
2. Mandate interpretation and sub-strategy structure; recommended working allocation within Real Assets and its rationale (peer evidence).
3. Holdings and data schema (holding -> group -> strategy -> sub-strategy; vehicle types; asset-level debt fields).
4. Return, NAV and cash-flow models with equations, per sub-strategy and vehicle type (closed-end funds via the PE engine with real-asset parameters; core/open-end/direct via income yield plus appraisal-smoothed NAV; development; asset-level debt and refinancing; open-end queue state machine).
5. Parameters: defaults, sources, dates, confidence.
6. Liquidity terms and stress behaviour: ladder rows (time-to-cash, haircuts) in base, drought, T4-prime and oil-crisis states.
7. SELL / HOLD / REFINANCE / LEVER action set: instruments, economics in liquidity-price units, regime availability, lags, decision rules; asset-level non-recourse debt and look-through leverage.
8. The four marks, desmoothing, bias and credibility model, and how they enter the FBE.
9. Oil, inflation and rates linkages: scenario-generator loadings by regime; the wrong-way-risk recommendation on oil-linked real assets.
10. Interactions with other groups and Corporate Finance (FTP, envelopes, internal transfers, conflicts, Overlay hedges).
11. Synthetic-data block for SYN-ADIC-177 (holding counts, size distributions, ground truth, biases, recovery tests, SYNTHETIC labels).
12. IC implications (the Real Assets seat persona, KPIs, how Real Assets results are discussed).
13. Consolidated calibration table.
14. Questions for the user.
15. Bibliography (deduplicated, with URLs).
End with a SPECIFICATION CARD for the Real Assets group in the same format as the seven-group report's per-group specs.
Rules: apply all verification corrections; never introduce unsourced numbers (label assumptions); be decisive. Use the Write tool (several chunks/edits are fine). Return the structured output.`
const synth = await agent(synthPrompt, { label: 'ra-synthesis', phase: 'Synthesis', schema: SYNTH_SCHEMA })
if (!synth) { log('Real Assets synthesis failed; stopping.'); return { streams: done.map(d => d.stream.num) } }

// ---------------- Critique ----------------
phase('Critique')
const critic = await agent(`You are a demanding completeness critic reviewing the REAL ASSETS group report for ADIC's multi-period, robust, agentic portfolio framework.

${BRIEF}

Read ${CONTEXT_FILE} section 1A, ${BRIEF_FILE} sections 1, 7 and 8, and the report ${RA_SYNTH} in full; skim the Real Assets dossiers (${DOSSIER_DIR}\\G10-G15*) and verification logs (${VERIFY_DIR}\\G10-G15*), and check consistency with ${G_SYNTH} and ${MAIN_SYNTH}.
Evaluate: R14 (Real Assets mapped like the other groups: holdings, forecasts, group-specific SELL/HOLD/REFINANCE/LEVER, budgets, attribution, IC discussion, decided at total-portfolio level); R15 (synthetic data with ground truth, realistic mark biases, recovery tests, labels); buildability (can an engineer implement the Real Assets engine and action set now?); consistency with the canonical conventions of the other reports; evidence quality (unsupported or stale numbers, ignored verification corrections); whether oil wrong-way risk, asset-level debt and open-end liquidity are genuinely modeled rather than listed.
Return at most 5 gaps, most severe first, each with a concrete research task.`, { label: 'ra-critic', phase: 'Critique', schema: CRITIC_SCHEMA })

// ---------------- Gap-fill + revise ----------------
phase('Gap-fill')
const gaps = ((critic && critic.gaps) || []).filter(g => g.severity !== 'low').slice(0, 4)
if (critic && critic.gaps.length > gaps.length) log(`Critic raised ${critic.gaps.length} gaps; filling ${gaps.length} (low-severity gaps skipped).`)
const addenda = (await parallel(gaps.map((g, i) => () => agent(`Close a gap in the REAL ASSETS group report for ADIC's multi-period, robust, agentic portfolio framework.

${BRIEF}

GAP: ${g.gap}
WHY IT MATTERS: ${g.why_it_matters || ''}
TASK: ${g.research_task}

Read ${CONTEXT_FILE} section 1A and the report ${RA_SYNTH} first (plus the relevant Real Assets dossiers in ${DOSSIER_DIR}). Research as needed (ToolSearch "select:WebSearch,WebFetch"; no Consensus). You may compute with ${PY} (scripts in ${ADDENDA_DIR}\\ra_gap_${String(i + 1).padStart(2, '0')}_calcs\\; label SYNTHETIC). Never fabricate citations or numbers. Write a focused addendum (1,500-4,000 words, with formulations, sourced and dated numbers, and design implications) to ${ADDENDA_DIR}\\ra_gap_${String(i + 1).padStart(2, '0')}.md. Return the structured output.`, { label: `ra-gap:${i + 1}`, phase: 'Gap-fill', schema: GAP_SCHEMA })))).filter(Boolean)

let revised = synth
if (addenda.length || (critic && critic.contradictions && critic.contradictions.length)) {
  revised = await agent(`Revise the REAL ASSETS group report at ${RA_SYNTH}.

Integrate these addenda (read each in full):
${addenda.map(a => `- ${a.addendum_path}: ${a.summary}`).join('\n')}
Also resolve these contradictions flagged by the critic: ${JSON.stringify((critic && critic.contradictions) || [])}
Re-read ${CONTEXT_FILE} section 1A in case the user has since confirmed the Real Assets scope, access route or size, and align the report with it.
Edit in place with the Edit tool: insert new material into the right sections (not as an appendix dump), fix inconsistencies, update the executive summary and the specification card if conclusions changed, keep everything else intact. Add a short version note (v1.1) at the top. Return the structured output for the revised report.`, { label: 'ra-revise', phase: 'Gap-fill', schema: SYNTH_SCHEMA }) || synth
}

// ---------------- Integrate ----------------
phase('Integrate')
const quant = await agent(`You are a quantitative analyst. Re-run the key total-portfolio numbers with Real Assets added, on the SYNTHETIC book.

${BRIEF}

Inputs: the Real Assets report ${RA_SYNTH} (its models, parameters and ladder rows); ${CONTEXT_FILE} section 1A (allocation v2, or the user's confirmed size if recorded there); the existing calculation scripts from the seven-group and main research, for example ${ADDENDA_DIR}\\GS_calcs\\gs_group_cashmap.py, ${ADDENDA_DIR}\\gap_01_calcs\\ (g01_core.py, g01_run.py), ${ADDENDA_DIR}\\gap_02_calcs\\, ${ROOT}\\research\\addenda\\gap_02_calcs\\ (t1_engine.py, gap02_study.py, phase1_demo.py) and ${ROOT}\\research\\addenda\\gap_01_calcs\\. Do NOT modify those originals: copy what you need into ${RA_CALCS}\\ and adapt the copies.
Compute, for allocation v1 (seven groups, as published) versus v2 (with Real Assets carved from PE funds), using the same canonical conventions (T4-prime = s*(theta*), census choice as recorded in the context file or census v1.1 by default):
1. The cross-group cash map: base, drought, and T4-prime 12- and 24-month net cash by group, with a Real Assets row.
2. The committed-facility need under T4-prime (do-nothing, with stage-triggered pacing, with the owner band), survival months on Treasury + Public Markets, and the T4-prime hard-row gap.
3. If feasible with the existing engines, the red-event probability for Mixes A and B in at least M1 and the stressed class.
4. Oil sensitivity: the change in the oil-crisis-state shortfall from the Real Assets oil loadings (with and without oil-linked natural-resource exposure).
Run everything with ${PY}. Save scripts and a results JSON in ${RA_CALCS}\\ and a short Markdown results note ${RA_CALCS}\\RESULTS.md. Label every figure SYNTHETIC; state every assumption; if an engine cannot be adapted, say so and give a first-order estimate with its formula instead. Return the structured output.`, { label: 'ra-quant', phase: 'Integrate', schema: QUANT_SCHEMA })

const integ = await agent(`You are the integration editor. Write the memo that tells the project exactly how to fold Real Assets (the eighth group) into the existing reports and design documents. Do NOT edit those documents yourself; another step will apply your memo after the design workflow and the citation fixes finish.

${BRIEF}

Read: the Real Assets report ${RA_SYNTH}; the quantitative re-run ${RA_CALCS}\\RESULTS.md${quant ? '' : ' (it may be missing: the re-run step failed)'}; the seven-group report ${G_SYNTH}; the main report ${MAIN_SYNTH}; and, if they exist, ${ROOT}\\design\\ARCHITECTURE.md and ${ROOT}\\design\\BUILD_SPEC.md.
Write ${RA_INTEG} with:
1. Headline changes: what adding Real Assets changes in the conclusions (cash map, facility need, survival, red-event gate, oil wrong-way risk, return bridge), with SYNTHETIC numbers from the re-run.
2. Edits to the group report: for each affected section of ${G_SYNTH}, the exact replacement or insertion text (e.g. a new per-group specification subsection for Real Assets in section 3, a Real Assets row in the cash map and ladder, credibility and synthetic-data additions, the IC seat).
3. Edits to the main report: exact replacement or insertion text for the affected sections of ${MAIN_SYNTH} (group count, cash generation, feasibility, oil/fiscal wrong-way risk L3, return bridge 4.12, instrument library 4.4, calibration 7.1, data requests 7.2).
4. Edits to ARCHITECTURE.md and BUILD_SPEC.md (if present): taxonomy/config, the Real Assets engine and its module/API, action-library entries, synthetic-data block (holding counts and allocation), shadow-IC roster, tests and acceptance criteria, and any ADRs to add.
5. Questions for the user that remain open.
Return the structured output.`, { label: 'ra-integration-memo', phase: 'Integrate', schema: INTEG_SCHEMA })

return {
  streams: done.map(d => ({ stream: d.stream.num, dossier: dossierPath(d.stream), verification: d.verification ? { checked: d.verification.checked, confirmed: d.verification.confirmed, corrected: d.verification.corrected, refuted: d.verification.refuted, unverifiable: d.verification.unverifiable, reliability: d.verification.overall_reliability } : null })),
  synthesis: { path: RA_SYNTH, executive_summary: revised.executive_summary, oil_wrong_way: revised.oil_wrong_way_recommendation, questions_for_user: revised.questions_for_user },
  critic: critic ? { gaps: critic.gaps.map(g => ({ gap: g.gap, severity: g.severity })), assessment: critic.overall_assessment } : null,
  addenda: addenda.map(a => a.addendum_path),
  quant,
  integration: integ,
}
