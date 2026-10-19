export const meta = {
  name: 'adic-groups-research',
  description: 'Group-specific research for the seven ADIC investment groups: 9 streams, adversarial fact-check, 2 cluster syntheses, group synthesis, completeness critic, gap-fill',
  phases: [
    { title: 'Research', detail: '9 group-specific research streams, each writes a dossier' },
    { title: 'Verify', detail: 'adversarial fact-check of each dossier (pipelined)' },
    { title: 'Cluster synthesis', detail: 'private groups; liquidity, organization and data' },
    { title: 'Group synthesis', detail: 'integrated group report with per-group specifications' },
    { title: 'Critique', detail: 'completeness critic against R14/R15 and buildability' },
    { title: 'Gap-fill', detail: 'close high-severity gaps and revise the group report' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const CONTEXT_FILE = ROOT + '\\inputs\\00_CONTEXT_AND_PRIOR_WORK.md'
const MAIN_DOSSIERS = ROOT + '\\research\\dossiers'
const MAIN_SYNTH = ROOT + '\\research\\00_SYNTHESIS.md'
const G_ROOT = ROOT + '\\research\\groups'
const DOSSIER_DIR = G_ROOT + '\\dossiers'
const VERIFY_DIR = G_ROOT + '\\verification'
const CLUSTER_DIR = G_ROOT + '\\clusters'
const ADDENDA_DIR = G_ROOT + '\\addenda'
const SYNTH_FILE = G_ROOT + '\\01_GROUPS_SYNTHESIS.md'

const BRIEF = `CLIENT BRIEF (full detail in ${CONTEXT_FILE} - read it first, especially section 1A):
ADIC runs a ~US$177bn endowment-model portfolio. It must distribute 5-10% of the fund annually to its sovereign owner; its return target is 10% (nominal USD); leverage is permitted; ~60% is private markets (mostly private equity), and PE distributions (DPI), historically a major cash source, are declining. The user (a quant / data-science lead at ADIC) wants a multi-period optimization framework with robust scenario analysis and probabilities of outcomes; a SELL / HOLD / REFINANCE / LEVER lens for every strategy/asset; three return series per asset (underwritten at inception, current actual, the strategy group's forecast); modeling of a very large multi-asset OTC-derivatives overlay (tail-protection hedge + opportunistic trading); an agentic architecture inspired by Sakana AI's 'The Agentic Scientist'; and the ability of the Investment Committee to discuss the results.
ADIC's investment organization has SEVEN GROUPS: (1) Private Equity - allocates to third-party funds; (2) Secondaries - invests in secondary funds and does direct deals; (3) Capital Solutions - 'does interesting financial deals' (structured/hybrid capital); (4) Co-investment - direct co-investments alongside GPs; (5) Public Markets - hedge funds and long-only managers; (6) Private Credit; (7) Overlay - OTC derivatives tail hedge and opportunistic trading. The framework must map holdings, forecasts, group-specific SELL/HOLD/REFINANCE/LEVER action sets, budgets, attribution and IC discussion onto these groups while making decisions at total-portfolio level. The user allows synthetic returns where data is missing (always labeled synthetic). A working synthetic allocation (PE funds $52bn, Secondaries $14bn, Co-investment $18bn, Capital Solutions $8bn, Private Credit $14bn, hedge funds $20bn, long-only $36bn, treasury cash+IG $15bn; ~$38bn unfunded) is in context section 1A.`

const RULES = (path) => `RESEARCH RULES
1. First Read the context file ${CONTEXT_FILE}.
2. A parallel 14-stream research program writes dossiers to ${MAIN_DOSSIERS} (e.g., 02_endowment_swf.md, 04_pe_cashflows.md, 05_secondaries_navfin.md, 06_leverage.md, 07_return_fusion.md, 08_action_valuation.md, 09_overlay.md, 10_scenarios_robustness.md). Some may already exist: Glob that folder and skim any that overlap your stream so you add group-specific depth instead of duplicating them. Never edit them.
3. Load web tools with ToolSearch query "select:WebSearch,WebFetch". Use WebSearch mode "standard" for most queries and "extended" for recent market data (2025-2026), niche facts, or when standard results are thin. Read primary sources with WebFetch (arXiv/SSRN/NBER/journal pages, official and regulator reports, reputable practitioner research); WebFetch answers a prompt about the page using a small model, so ask specific, exhaustive extraction questions. Run many searches (typically 25-60) and read the most important sources rather than relying on snippets.
4. ACADEMIC SEARCH (optional): the user has a Consensus (consensus.app) account. Run ToolSearch with query "consensus" once. If it returns Consensus search tools (names starting with mcp__claude_ai_Consensus__ other than ..._authenticate and ..._complete_authentication), load them and use them for peer-reviewed literature alongside WebSearch. If only the authenticate tools appear, do NOT call them (authentication is interactive); use WebSearch/WebFetch.
5. Today is 2026-10-18. Prefer the most recent data and always give as-of dates. Distinguish (a) sourced facts, (b) practitioner consensus, (c) your own inference.
6. Never fabricate citations, numbers or URLs; if you cannot verify something, say so explicitly. Seed references named in your brief are hints from memory - verify authors, years and titles before citing them. Keep verbatim quotes under 125 characters.
7. Think across disciplines: operations research, control theory, actuarial science, bank treasury/ALM, insurance, organizational economics, decision science, real options, machine learning.
8. Write the dossier in Markdown to ${path} using the Write tool. Target 4,000-8,000 words: dense, technical, with equations where they clarify. Sections: 1) Executive summary; 2) Core concepts & theory; 3) Methods/models and trade-offs; 4) Empirical evidence & current market data (dated, sourced); 5) Practitioner/peer practice & case studies; 6) Design implications for the ADIC framework (state variables, decision variables, constraints, objective terms, equations, parameters with default values, calibration targets, data needs), ending with a SPECIFICATION CARD - a compact table an engineer can implement from: data fields; return and cash-flow equations; parameter defaults with sources; liquidity terms and stress behaviour; SELL/HOLD/REFINANCE/LEVER definitions and economics; how forecasts are produced and their typical biases; synthetic-data defaults; links to other groups; 7) Implementation notes (Python libraries, algorithms, numerical pitfalls); 8) Risks, pitfalls & limitations; 9) Open questions (including what ADIC must supply or confirm); 10) References (full citations with URLs).
9. Then return the structured output, faithfully summarizing the dossier. load_bearing_claims = the 10-20 empirical claims/numbers your recommendations depend on most, each with its source URL.`

const STREAMS = [
  { num: 'G1', key: 'pe_primaries', title: 'PE group: the fund-commitment program as a controllable system', body: `Focus: ADIC's Private Equity group allocates to third-party PE funds as an LP (primary commitments; working NAV ~$52bn plus most of the ~$38bn unfunded - context section 1A). Model the program and the group's decision levers so the total-portfolio optimizer can control them. Main-program stream 04 (pe_cashflows) covers generic call/distribution/NAV models and the DPI drought; you cover program management, the group's levers and its forecasts.

Research:
- Program design and pacing: commitment-pacing models and over-commitment (target NAV, commitment ratios, Takahashi-Alexander-based pacing; practitioner tools from Cambridge Associates, Hamilton Lane, StepStone, BlackRock, MSCI/Burgiss, Neuberger Berman); vintage diversification; strategy and geography mix (large/mid/small buyout, growth, venture, sector specialists, US/Europe/Asia); number of managers and concentration; recallable distributions and recycling.
- LP skill, access and relationships: Lerner, Schoar & Wongsunwai (2007 JF); Sensoy, Wang & Weisbach (2014 JFE); Cavagnaro, Sensoy, Wang & Weisbach (2019 JF); Harris, Jenkinson, Kaplan & Stucke (2023, persistence); Korteweg & Sorensen (2017). The option value of GP relationships and re-up rights; what skipping a fund costs (access risk), and how to model that as a penalty or lost option in the optimizer.
- The cost of pulling levers: slowing or pausing new commitments (effect on NAV, on distributions 4-8 years out, vintage gaps, co-investment deal flow, relationships); selling LP interests (pricing is in stream 05; you cover program-level effects such as vintage holes and lost re-ups); fund-term extensions; GP-led processes (continuation-vehicle elections: roll vs sell); GP-level NAV loans and dividend recaps that change LP cash flows; subscription lines and their effect on call timing and reported IRR (e.g., Albertus & Denes; Schillinger, Braun & Cornel - verify).
- Fees and net economics: management fees (committed vs invested), carry waterfalls (European vs American), fee offsets, gross-to-net spreads by strategy, total cost of ownership.
- Current market (2024-2026, dated, sourced): fundraising and GP concentration, holding periods, NAV overhang, distribution yields, DPI by vintage (2015-2022), LP behaviour (pacing cuts, denominator effects, secondary sales by large LPs).
- How PE groups forecast fund outcomes (GP projections, look-through portfolio-company models, NAV roll-forwards, cash-flow pacing models) and the known biases (interim-NAV behaviour around fundraising - Barber & Yasuda 2017; Brown, Gredil & Kaplan 2019; Jenkinson, Sousa & Stucke 2013; optimism on exit timing); how to grade those forecasts.
- SELL / HOLD / REFINANCE / LEVER for this group at fund-interest and program level, including 'slow pacing' as a program-level lever, and what is NOT admissible for a sovereign LP (e.g., defaulting on capital calls).
Deliverable emphasis: a program-level model spec - state (commitments by vintage x strategy, unfunded, NAV, fund ages, GP-relationship status), decisions (new commitments by strategy and quarter, secondary sales, NAV-loan usage, CV elections), transitions (linked to the cash-flow engine), relationship/access penalties, parameter tables with sources, and how the PE group's forecasts enter return fusion.` },

  { num: 'G2', key: 'secondaries_group', title: 'Secondaries group: secondary funds and direct secondary deals', body: `Focus: ADIC's Secondaries group invests in third-party secondary funds and does direct secondary deals (working NAV ~$14bn). Interpret 'direct deals' as direct LP-portfolio purchases and GP-led continuation-vehicle (CV) investments, and note other plausible meanings. Main-program stream 05 covers secondaries from ADIC's point of view as a SELLER; you cover the group as a BUYER and investor, and its links to the rest of ADIC.

Research:
- Market structure 2015-2026 (dated, sourced: Jefferies, Lazard, Evercore, PJT Park Hill, Campbell Lutyens, Setter, Preqin, PitchBook): LP-led vs GP-led volumes, buyer universe (dedicated funds; the growing role of evergreen/semi-liquid vehicles), pricing by strategy and fund age, buyers' use of leverage and deferred payments, 2025 and 2026 records.
- Returns and cash flows: secondary-fund net IRR / TVPI / DPI by vintage vs primaries (Cambridge Associates, MSCI/Burgiss, Preqin, Hamilton Lane); dispersion; J-curve mitigation and faster DPI; duration.
- Return decomposition: discount capture (buying at e.g. 85% of NAV creates an immediate mark-up to NAV under fair-value accounting - a reported-return artifact vs true economic alpha), NAV growth, leverage and deferred-payment effects on IRR and risk, fee/carry layers in secondary funds; evidence on whether discounts compensate for illiquidity or reflect information (Nadauld, Sensoy, Vorkink & Weisbach 2019 JFE; Albuquerque, Cassel, Phalippou & Schroth 2018).
- GP-led continuation vehicles: single- vs multi-asset, concentration, GP alignment (carry rollover), pricing near NAV, fairness opinions, ILPA guidance, available performance evidence 2018-2026.
- Cash-flow models for (a) purchased LP positions (older funds, immediate NAV exposure, tail-end risk), (b) commitments to secondary funds (fast deployment, shorter lives), (c) CV investments (concentrated, single-asset exit risk).
- Countercyclicality: volumes and pricing in stress (2009, 2020, 2022-2023) versus ADIC's own liquidity in stress; dry powder as a real option (the value of being able to buy when discounts are widest) and how the shadow price of liquidity should reflect it.
- Links to the rest of ADIC: the group as in-house pricing desk for the PE group's SELL decisions; conflicts and governance for internal crosses (a PE-group sale to the Secondaries group is near zero-sum at total-portfolio level); related-party policies at peers.
- SELL / HOLD / REFINANCE / LEVER for this group: tertiary sales, holding, deferred payments and NAV/portfolio facilities, deployment pacing.
Deliverable emphasis: models and parameters for the book (position-level cash flows, NAV dynamics, discount accretion vs economic return), a regime-dependent opportunity set (deal volume, pricing), decision levers, and how the group's forecasts and market quotes feed ADIC's own SELL pricing.` },

  { num: 'G3', key: 'cap_solutions', title: 'Capital Solutions group: structured and hybrid capital', body: `Focus: ADIC's Capital Solutions group 'does interesting financial deals' (working NAV ~$8bn). Interpret this as structured and hybrid capital - preferred equity, structured equity with kickers, convertibles, holdco/PIK and NAV-based financing, fund finance (NAV loans to funds, GP financing, GP stakes), asset-based and specialty finance, rescue/special-situations capital, structured LP solutions - and define the space from public descriptions of leading platforms (e.g., Blackstone Tactical Opportunities, Apollo Hybrid Value, KKR Strategic Investments, Carlyle AlpInvest, HPS, Ares, Goldman Sachs Capital Solutions, 17Capital, Hollyport, Oaktree; verify each).

Research:
- Instrument economics: cash and PIK coupons, OID and fees, equity kickers (warrants, conversion), MOIC floors and make-wholes, seniority, covenants, maturities and expected lives; target and realized gross/net returns by instrument; loss-given-default and recovery evidence; behaviour in stress (PIK accrual, conversions, restructurings); valuation practice (yield-based marks, enterprise-value coverage) and its lag; correlation with PE and credit cycles.
- Market size, growth and pricing 2023-2026 (dated, sourced) for fund-level NAV financing, preferred equity, hybrid capital and GP solutions. Demand drivers: the DPI drought pushes GPs and LPs to seek liquidity, so this book may be a natural internal hedge against the drought that hurts ADIC's PE distributions - test this claim with evidence.
- Simulation models: contractual cash flows plus stochastic default and prepayment plus a kicker payoff tied to equity value; structural (Merton-style payoff on underlying EV) vs reduced-form (intensity + recovery + equity option) formulations; regime dependence.
- Links to the rest of ADIC: the group's expertise and quotes as in-house pricing for ADIC's own REFINANCE options (NAV loans or preferred equity on ADIC's PE portfolio); conflicts (should ADIC's own refinancing be done with third parties?); the natural hedge with the PE book.
- SELL / HOLD / REFINANCE / LEVER for this book: syndication and secondary sales, hold, asset-level back-leverage, rated-feeder or CFO-style structures.
Deliverable emphasis: an instrument library (cash-flow formulas, parameters with dated sources), stress behaviour, a regime-dependent opportunity set, and decision economics for the group's book.` },

  { num: 'G4', key: 'coinvest', title: 'Co-investment group: direct minority co-investments', body: `Focus: ADIC's Co-investment group makes direct minority equity co-investments alongside GPs (working NAV ~$18bn).

Research:
- Performance evidence: Fang, Ivashina & Lerner (2015 JFE); Braun, Jenkinson & Schemmerl (2020 JFE, adverse selection); Lerner, Mao, Schoar & Zhang (2022 JFE, alternative vehicles); deal-level return distributions (e.g., Braun, Jenkinson & Stoff 2017 JFE) - probability of loss, skew, dispersion; fee and carry savings (no-fee/no-carry vs reduced terms); deal-size, sector and timing effects; verify all citations.
- Portfolio construction: number of deals needed for diversification; concentration; double exposure via the GP's fund; deal flow tied to fund commitments (cutting PE primary commitments can cut co-investment flow - a cross-group link).
- Cash-flow profile: funded at close (plus follow-ons), exits controlled by the lead GP, holding-period distributions, exit hazard rates by regime (IPO and M&A windows), dividend recaps as interim distributions, marks that follow the lead GP (lag and smoothing).
- Decision levers: SELL (single-asset direct secondary sales and their discounts; sale into GP-led CVs; tag-along), HOLD, REFINANCE (company-level recaps are GP-controlled; portfolio-level holdco/NAV financing on a concentrated co-invest pool - LTVs and pricing), LEVER (holdco PIK, NAV facility); minority-rights constraints.
- How co-investment teams forecast (deal models with base/downside cases at underwriting; updated cases) and their biases (underwriting optimism; the user's memo-corpus lessons: leverage above 6x EBITDA, dependence on multiple expansion, optimistic distribution timing after spread shocks).
Deliverable emphasis: a deal-level stochastic model (value process with idiosyncratic jumps and write-offs, exit hazard by regime, recap events), parameter tables with sources, diversification analytics, and decision economics.` },

  { num: 'G5', key: 'public_markets', title: 'Public Markets group: hedge funds and long-only managers as return source and liquidity reservoir', body: `Focus: ADIC's Public Markets group invests in hedge funds (working ~$20bn) and long-only managers (~$36bn). It is ADIC's main liquidity reservoir and rebalancing source.

Research:
- Hedge funds: strategy-level return, volatility, drawdown and crisis betas (HFR/HFRI, Preqin, PivotalPath, EurekaHedge; 2008, 2020, 2022, and 2025-2026 if available); multi-strategy platforms (pass-through fees, liquidity terms, capacity 2023-2026); macro and CTA convexity; fee levels; performance persistence and alpha decay; database biases (survivorship, backfill, self-selection - Fung & Hsieh 2000; Malkiel & Saha 2005; Aggarwal & Jorion 2010) and return smoothing (Getmansky, Lo & Makarov 2004).
- Liquidity terms and their stress behaviour: redemption frequency, notice periods, hard/soft lock-ups, investor- and fund-level gates, side pockets, suspensions; evidence from 2008-09 and later (Aragon 2007; Ang & Bollen 2010; Teo 2011; Agarwal, Daniel & Naik 2009; Aiken, Clifford & Ellis 2015; verify); the hedge-fund secondary market and its 2009 discounts; modelling redemption queues and the probability of gating conditional on market state.
- Long-only managers: active return, tracking error and information-ratio distributions by asset class; fees; alpha decay; transition and market-impact costs for USD 1-5bn trades.
- Total-portfolio roles: the liquidity waterfall (which managers to redeem first given notice ladders and gates); physical-to-synthetic replacement via the overlay (sell physical, hold futures/TRS: frees cash but adds financing cost, basis/roll and margin risk - give 2024-2026 implied financing spreads for major index futures and TRS); rebalancing policies (calendar vs threshold; NBIM-style rules); portable alpha (hedge-fund alpha on top of futures beta).
- SELL / HOLD / REFINANCE / LEVER for this group: redeem (subject to terms), hold, physical-to-synthetic as REFINANCE, synthetic exposure or portable alpha as LEVER.
- How the group forecasts manager returns, and how to grade those forecasts.
Deliverable emphasis: simulation-ready models (factor model + alpha + fat tails per manager; a liquidity-term state machine with notice, lock-ups and stress-conditional gates), parameter tables with sources, and decision economics including physical-to-synthetic replacement.` },

  { num: 'G6', key: 'private_credit', title: 'Private Credit group: loan-pool cash flows, defaults, leverage and natural DPI', body: `Focus: ADIC's Private Credit group invests in private credit (working NAV ~$14bn): direct lending/unitranche, asset-based finance, mezzanine, opportunistic credit. The user's prior deck flagged 'credit stress RED - private credit sleeve impaired', so the model must handle impairment.

Research:
- Market data 2022-2026 (dated, sourced): yields and spreads by segment (Cliffwater Direct Lending Index returns, yields and realized losses; 2024-2026 spread moves), non-accrual and default rates (Proskauer, Fitch U.S. Private Credit Default Rate, KBRA DLD, Lincoln International shadow defaults and PIK usage, BDC non-accruals), recoveries, PIK share of income, covenant trends, amend-and-extend; regulator analyses (IMF GFSR April 2024 ch. 2, Fed FSR, BoE, ECB); 2025-2026 stress episodes and redemption pressure on semi-liquid vehicles (verify specifics).
- Cash-flow model: floating coupons (base rate + spread), OID and fees, amortization, prepayments (refinancing waves when spreads tighten), defaults with intensity linked to macro and credit regimes and to base rates (interest coverage), recoveries and workout timelines, PIK toggles and accrual, delayed-draw and revolver commitments that DRAW in stress, fund-level leverage (BDC-style debt/equity; SMA back-leverage; rated note feeders), NAV marks that lag spreads.
- Private credit as natural DPI: cash yield plus repayments as a share of NAV per year, by regime; comparison with PE distribution yields; implications for sizing the book as a liquidity source vs its credit risk.
- SELL / HOLD / REFINANCE / LEVER: secondary sales of fund interests and loans (market size and pricing 2024-2026), hold to maturity, back-leverage or rated notes (REFINANCE), fund leverage (LEVER), and their risks (margin calls on back-leverage, LTV triggers).
- How credit teams forecast (expected-loss models, yield-to-maturity vs loss-adjusted yield) and typical biases.
Deliverable emphasis: a simulation-ready loan-pool/fund model with equations (coupons, defaults, recoveries, prepayments, PIK, delayed-draw draws, leverage, NAV marks), regime-dependent parameters with dated sources, and decision economics.` },

  { num: 'G7', key: 'liquidity_ladder', title: 'Total-portfolio liquidity across the seven groups: ladder, stress behaviour, contingency funding', body: `Focus: ADIC's total-portfolio liquidity across the seven groups plus central treasury: a liquidity ladder (time-to-cash and stressed haircuts by instrument and group), sources and uses in base and stress, the pecking order, survival metrics, and a contingency funding plan. Use ADIC's scale: USD 177bn, distributions 5-10% (about USD 8.9-17.7bn a year), ~USD 38bn unfunded (working assumption), working allocation in context section 1A. Main-program streams 05, 06 and 08 cover instruments, leverage and the shadow price of liquidity; you cover the cross-group ladder and its stress behaviour.

Research:
- Asset-owner liquidity frameworks: Basel LCR/NSFR ideas adapted to asset owners; peer practice (CPP Investments liquidity coverage and stress testing; Future Fund; NZ Super; GIC; Yale and Harvard after 2008; NBIM); pension liquidity buffers after the 2022 LDI episode (Bank of England, The Pensions Regulator); IMF/FSB work on non-bank liquidity; endowment liquidity tiers.
- Time-to-cash and haircuts by instrument, normal vs stress: public equities, IG bonds, Treasuries and repo, hedge funds (notice + gates), long-only funds, private credit (coupons; secondary sales at discounts), PE LP stakes (3-6 month sales; regime discounts), co-investments, capital-solutions positions, overlay (VM in or out; collateral eligibility); encumbrance (posted collateral, NAV-loan pledges).
- Uses in stress: owner distributions (possibly co-moving with oil), capital calls (evidence on call and distribution rates in 2008-09, 2020, 2022), private-credit delayed-draw and revolver draws, overlay VM, debt service, NAV-loan LTV cures.
- Methods: cash-flow ladders, survival horizon, liquidity-at-risk by Monte Carlo, reverse liquidity stress tests, waterfall/pecking-order policies consistent with a marginal-cost-of-liquidity curve, contingency funding plans (bank CFP analogy), triggers and early-warning indicators.
- Governance: who owns the liquidity pool (central treasury vs groups), liquidity budgets per group.
Deliverable emphasis: a concrete liquidity-ladder data model and simulation design (buckets, regimes, haircuts, timing), the liquidity constraints for the optimizer, definitions of survival metrics, and a contingency-funding-plan structure for the IC.` },

  { num: 'G8', key: 'org_tpa_economics', title: 'Organizational economics: internal capital markets, transfer pricing and forecast incentives', body: `Focus: ADIC allocates capital across seven internal groups (PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets, Private Credit, Overlay). The framework must make total-portfolio decisions while using the group structure. Research the economics and governance of multi-group capital allocation.

Research:
- Internal capital markets: Stein (1997 JF); Scharfstein & Stein (2000 JF); Rajan, Servaes & Zingales (2000 JF); Shin & Stulz (1998 QJE); winner-picking vs 'socialism'; influence costs (Milgrom 1988; Meyer, Milgrom & Roberts 1992); implications for an asset owner's allocation across groups.
- TPA operating models at peers (public sources): CPP Investments (total-portfolio committee, Reference Portfolio, department risk budgets), GIC (Reference/Policy/Active portfolios), NZ Super (reference portfolio + active strategies, opportunity allocation), Future Fund (total-portfolio team), NBIM, CalPERS' TPA move (verify dates and details), WTW Thinking Ahead Institute and CAIA TPA papers. How capital, risk and liquidity budgets are given to groups; how proposals compete (funding basket / opportunity cost - compare with the user's alpha*).
- Liquidity and risk transfer pricing: bank FTP (matched-maturity FTP, liquidity premium curves, contingent-liquidity charges; EBA and Basel guidance); applying FTP to an asset owner - charging groups for liquidity consumption (unfunded commitments, illiquidity duration), crediting liquidity providers (cash-generative books, the tail hedge); deriving the charges from optimizer duals so group incentives match total-portfolio shadow prices; risk-capital allocation (Euler allocation, Tasche; marginal contribution to risk; RAROC).
- Forecast incentives and calibration: group forecasts come from people whose budgets depend on them. Proper scoring rules (Brier 1950; Savage 1971; Gneiting & Raftery 2007 JASA); calibration tracking and track-record weights; Tetlock; evidence on budget gaming and sandbagging; elicitation formats (P10/P50/P90 rather than points); how to present group calibration to an IC without destructive politics.
- Internal transfers between groups (e.g., the Secondaries group buying a PE-group fund stake; Capital Solutions financing an ADIC-held position): governance, related-party policies, fairness opinions; near zero-sum at total-portfolio level except fees and execution.
- Attribution and incentives: contribution by group to total return, risk and liquidity; compensation linked to total-portfolio vs silo benchmarks (peer practice).
Deliverable emphasis: a design for (i) group budgets as optimizer outputs (pacing, NAV, risk, liquidity), (ii) transfer pricing derived from optimizer duals, (iii) a per-group forecast-scoring and credibility system feeding return fusion, (iv) IC presentation and decision-rights norms (group vs total portfolio), (v) treatment of internal transfers.` },

  { num: 'G9', key: 'synthetic_data', title: 'Synthetic data for a seven-group USD 177bn fund with a known ground truth', body: `Focus: specify a realistic, clearly labeled synthetic dataset for a USD 177bn endowment-model fund with seven groups and ~300-600 holdings, including the three return series per holding (underwritten, current actual, group forecast) with realistic biases, generated from a documented ground-truth process so the framework's estimators can be validated before ADIC data arrive. The user explicitly allowed synthetic returns; they must never be presented as ADIC data.

Research:
- Calibration sources and stylized facts by group: PE funds (MSCI/Burgiss, Cambridge Associates, Preqin, PitchBook: IRR/TVPI/DPI dispersion by vintage and strategy, PME distributions, cash-flow curves), secondaries, co-investment deal-level return distributions, capital solutions, private credit (Cliffwater, default/recovery), hedge funds (HFRI strategy statistics), long-only (index + tracking error), overlay inputs (implied-vol levels and skews by regime; VIX, MOVE, credit-index vol history).
- Methods: structural simulation (stochastic Takahashi-Alexander; factor + idiosyncratic), bootstrapping from public benchmarks, copulas for cross-sectional dependence, vintage and regime effects; deep generative tabular methods (GAN/diffusion/LLM) and why structural simulation is preferable when ground truth is needed; synthetic-data quality checks (stylized-fact tests, discriminator tests, distribution matching).
- The three return series with realistic biases: underwriting optimism (target vs realized returns in PE, real estate, infrastructure; reference-class evidence), interim-NAV biases by fund age and fundraising timing (Jenkinson, Sousa & Stucke 2013; Barber & Yasuda 2017; Brown, Gredil & Kaplan 2019), forecaster behaviour (anchoring to underwriting, smoothing, optimistic distribution timing after spread shocks - cf. the user's memo-corpus finding); per-group bias parameters.
- Ground-truth validation: simulation-based calibration (Talts et al. 2018), parameter-recovery tests for the fusion estimator, posterior-interval coverage tests, held-out realized-outcome tests.
- Industry data schemas: ILPA reporting and performance templates (including 2025 updates), capital-account and cash-flow formats, MSCI/Burgiss cash-flow data structure, Open Protocol (hedge-fund risk reporting), private-credit loan tapes, derivatives trade and CSA data; propose schemas for holdings, cash flows, NAV history, the three return series, liquidity terms and overlay positions.
- Plausible allocation and balance-sheet ratios for a large endowment-model sovereign fund with ~60% private (Yale, Harvard, Stanford, NACUBO large endowments; CPP, GIC, Temasek, ADIA and Mubadala public disclosures), unfunded/NAV ratios, overlay notional, leverage; check the working allocation in context section 1A.
Deliverable emphasis: a synthetic-data specification ready to implement - entities and schemas, sizes, distributions and parameters with sources, the bias-generation model, the ground-truth process, validation checks, and labeling rules.` },
]

const CLUSTERS = [
  { key: 'GC1_private_groups', title: 'The five private groups: PE funds, Secondaries, Capital Solutions, Co-investment, Private Credit', streams: ['pe_primaries', 'secondaries_group', 'cap_solutions', 'coinvest', 'private_credit'] },
  { key: 'GC2_liquidity_org_data', title: 'Public Markets, cross-group liquidity, organizational economics and synthetic data', streams: ['public_markets', 'liquidity_ladder', 'org_tpa_economics', 'synthetic_data'] },
]

const RESEARCH_SCHEMA = {
  type: 'object',
  properties: {
    stream: { type: 'string' },
    dossier_path: { type: 'string' },
    word_count: { type: 'integer' },
    executive_summary: { type: 'string' },
    key_insights: { type: 'array', items: { type: 'string' } },
    recommended_methods: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, use_for: { type: 'string' }, rationale: { type: 'string' }, python_tooling: { type: 'string' } }, required: ['name', 'use_for', 'rationale'] } },
    design_implications: { type: 'array', items: { type: 'string' } },
    calibration_targets: { type: 'array', items: { type: 'object', properties: { parameter: { type: 'string' }, value: { type: 'string' }, as_of: { type: 'string' }, source: { type: 'string' } }, required: ['parameter', 'value', 'source'] } },
    load_bearing_claims: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, source_url: { type: 'string' }, confidence: { type: 'string', enum: ['high', 'medium', 'low'] } }, required: ['claim', 'confidence'] } },
    used_consensus: { type: 'boolean' },
    cross_links: { type: 'array', items: { type: 'string' } },
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
    notes: { type: 'string' },
  },
  required: ['stream', 'checked', 'confirmed', 'corrected', 'refuted', 'unverifiable', 'corrections', 'overall_reliability'],
}

const CLUSTER_SCHEMA = {
  type: 'object',
  properties: {
    cluster: { type: 'string' },
    path: { type: 'string' },
    summary: { type: 'string' },
    key_insights: { type: 'array', items: { type: 'string' } },
    formulations: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, specification: { type: 'string' } }, required: ['name', 'specification'] } },
    calibration_targets: { type: 'array', items: { type: 'object', properties: { parameter: { type: 'string' }, value: { type: 'string' }, as_of: { type: 'string' }, source: { type: 'string' }, confidence: { type: 'string' } }, required: ['parameter', 'value', 'source'] } },
    cross_cluster_links: { type: 'array', items: { type: 'string' } },
    open_questions: { type: 'array', items: { type: 'string' } },
  },
  required: ['cluster', 'path', 'summary', 'key_insights', 'formulations'],
}

const GSYNTH_SCHEMA = {
  type: 'object',
  properties: {
    synthesis_path: { type: 'string' },
    word_count: { type: 'integer' },
    executive_summary: { type: 'string' },
    group_specs: { type: 'array', items: { type: 'object', properties: { group: { type: 'string' }, cash_flow_model: { type: 'string' }, actions: { type: 'string' }, forecast_bias_model: { type: 'string' }, liquidity_terms: { type: 'string' }, synthetic_defaults: { type: 'string' } }, required: ['group', 'cash_flow_model', 'actions'] } },
    cross_group_mechanisms: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, mechanism: { type: 'string' }, implication: { type: 'string' } }, required: ['title', 'mechanism', 'implication'] } },
    synthetic_data_spec_summary: { type: 'string' },
    ic_implications: { type: 'array', items: { type: 'string' } },
    questions_for_user: { type: 'array', items: { type: 'string' } },
    open_questions: { type: 'array', items: { type: 'string' } },
  },
  required: ['synthesis_path', 'executive_summary', 'group_specs', 'cross_group_mechanisms', 'questions_for_user'],
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
  properties: {
    gap: { type: 'string' },
    addendum_path: { type: 'string' },
    summary: { type: 'string' },
    key_findings: { type: 'array', items: { type: 'string' } },
    design_changes: { type: 'array', items: { type: 'string' } },
  },
  required: ['gap', 'addendum_path', 'summary'],
}

const dossierPath = (s) => DOSSIER_DIR + '\\' + s.num + '_' + s.key + '.md'
const verifyPath = (s) => VERIFY_DIR + '\\' + s.num + '_' + s.key + '.verify.md'
const clusterPath = (c) => CLUSTER_DIR + '\\' + c.key + '.md'

const researchPrompt = (s) => `You are a senior research analyst on a multidisciplinary team building a multi-period, robust, agentic portfolio decision framework for a sovereign endowment-model fund.

${BRIEF}

YOUR RESEARCH STREAM ${s.num}: ${s.title}

${s.body}

${RULES(dossierPath(s))}`

const verifyPrompt = (s, r) => `You are an adversarial fact-checker for a research program that will inform a sovereign fund's Investment Committee. Your job is to catch errors before they reach the IC.

Read the dossier at ${dossierPath(s)} (stream ${s.num}: ${s.title}). Background context: ${CONTEXT_FILE}.
The author flagged these load-bearing claims:
${JSON.stringify((r && r.load_bearing_claims) || [], null, 1)}

Tasks:
1. Select the 12-18 most load-bearing empirical claims in the dossier (numbers, dates, market statistics, regulatory facts, attributions of findings to specific papers/authors) - include the author's flagged claims plus any others you judge critical or suspicious.
2. Verify each against primary or high-quality sources (load tools via ToolSearch "select:WebSearch,WebFetch"; WebSearch mode "standard", or "extended" for recent/niche data). If ToolSearch "consensus" surfaces Consensus search tools other than the authenticate tools, you may use them to check academic citations; never call the authenticate tools. Verdict per claim: confirmed / corrected (give the corrected value and source) / refuted / unverifiable. Default to unverifiable if you cannot find support; do not give the benefit of the doubt.
3. Check that the 10 most important references exist with correct authors, year, title and venue (catch hallucinated or garbled citations).
4. Identify reasoning errors or overclaims in the dossier's design implications and specification card (e.g., a model that does not do what is claimed, a formula error, a mis-specified constraint, an action that is not actually available to an LP).
5. Write your verification log in Markdown to ${verifyPath(s)} with: summary; a table of claims (claim | verdict | corrected value | source URL); citation-check results; reasoning issues; overall reliability rating.
Do NOT edit the dossier itself. Then return the structured output.`

const clusterPrompt = (c, results) => {
  const files = results.map(r => `- Stream ${r.stream.num} ${r.stream.title}\n  dossier: ${dossierPath(r.stream)}\n  verification log: ${r.verification ? verifyPath(r.stream) : '(verification failed - treat numbers with extra caution)'}`).join('\n')
  return `You are synthesizing one cluster of a 9-stream group-specific research program for ADIC's multi-period, robust, agentic portfolio framework.

${BRIEF}

CLUSTER: ${c.title}
Read the context file ${CONTEXT_FILE}, then read EVERY dossier and verification log below in full:
${files}
Where helpful, also consult the main research program's dossiers in ${MAIN_DOSSIERS} (if present) for consistency.

Produce an integrated cluster synthesis that:
1. Applies all verification corrections (never repeat a claim the verifier refuted or corrected without the correction; flag unverifiable numbers as such).
2. Reconciles disagreements between dossiers and gives a clear recommendation for every design question in this cluster.
3. Gives, for each group or component in the cluster, an implementable specification: data fields; return/cash-flow equations; state and decision variables; parameters with defaults and sources; liquidity terms and stress behaviour; the SELL/HOLD/REFINANCE/LEVER action set with economics and decision rules; forecast production and bias model; synthetic-data defaults.
4. Lists calibration targets (value, as-of date, source, confidence).
5. Identifies cross-group interactions (internal transfers, in-house pricing, natural hedges, deal-flow dependencies, liquidity competition) and links to the other cluster.
6. Notes open questions and the data ADIC must supply or confirm.
Write 6,000-10,000 words in Markdown to ${clusterPath(c)} using the Write tool. Then return the structured output.`
}

const groupSynthPrompt = (clusters, streamResults) => {
  const cl = clusters.filter(Boolean).map(c => `- ${c.cluster}: ${c.path}\n  summary: ${c.summary}`).join('\n')
  const ds = streamResults.filter(Boolean).map(r => `- ${r.stream.num} ${r.stream.title}: ${dossierPath(r.stream)}${r.verification ? ' | verification: ' + verifyPath(r.stream) : ''}`).join('\n')
  return `You are the lead author of the GROUP report for ADIC's multi-period, robust, agentic portfolio decision framework. It complements the main research report (${MAIN_SYNTH}; read it if it exists, otherwise skim the main dossiers in ${MAIN_DOSSIERS}) and must be consistent with it.

${BRIEF}

Read the context file ${CONTEXT_FILE}, then the cluster syntheses below in full, consulting individual dossiers and verification logs where you need depth.
Cluster syntheses:
${cl}
Dossiers (and verification logs):
${ds}

Write the group report to ${SYNTH_FILE} (10,000-15,000 words, Markdown):
0. Title, date (2026-10-18), scope, relationship to the main report.
1. Executive summary (at most 1,000 words).
2. ADIC as an internal capital market of seven groups: total-portfolio vs group view; a cash-generation map by group (sources and uses in base and stress, with explicit assumptions, using the working synthetic allocation); the cross-group liquidity ladder.
3. Per-group specifications, one subsection per group (PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets, Private Credit, Overlay). For each: mandate and working interpretation; holdings and data schema; return and cash-flow model with equations; parameters (defaults, sources, dates, confidence); liquidity terms and stress behaviour; the SELL/HOLD/REFINANCE/LEVER action set with economics and decision rules; how the group forecasts and its bias/credibility model; synthetic-data defaults; interactions with other groups. For the Overlay, cross-reference the main program's overlay work and add only group-specific items (collateral, synthetic exposure provided to other groups, liability-aware hedging).
4. Cross-group mechanisms: netting of internal transfers; in-house pricing desks with conflict controls; liquidity/risk transfer pricing from optimizer duals; group budgets as optimizer outputs; option value of dry powder; natural hedges between groups; co-investment flow dependence on primary commitments.
5. Forecast credibility and scoring per group (how it feeds return fusion).
6. Synthetic dataset specification (entities, sizes, distributions, bias model, ground truth, validation checks, SYNTHETIC labeling).
7. IC implications: group-head personas in the shadow IC; how group-level results are discussed; decision rights; politics-aware presentation of forecast calibration.
8. Consolidated calibration table (value, as-of, source, confidence).
9. Questions for the user (interpretations to confirm, e.g., what Capital Solutions actually does; data ADIC must supply).
10. Bibliography (deduplicated, with URLs).
Rules: apply all verification corrections; never introduce unsourced numbers (label assumptions as assumptions); be decisive - recommend, do not survey. Use the Write tool (several chunks/edits are fine). Then return the structured output.`
}

const REQUIREMENTS = `R14) map the framework onto ADIC's seven investment groups - holdings, forecasts, group-specific SELL/HOLD/REFINANCE/LEVER action sets, budgets, attribution and IC discussion by group, with decisions evaluated at total-portfolio level; R15) synthetic data with a documented ground-truth process, realistic biases in the three return series, and SYNTHETIC labeling; plus consistency with the original requirements (multi-period optimization, robust scenarios, probabilities of outcomes, 5-10% distributions, 10% target, leverage, ~60% private with declining DPI, fusion of underwritten/actual/forecast returns, the overlay's two strategies, agentic architecture, IC discussion).`

const criticPrompt = `You are a demanding completeness critic reviewing the GROUP report for ADIC's multi-period, robust, agentic portfolio framework.

${BRIEF}

Read the context file ${CONTEXT_FILE} and the group report at ${SYNTH_FILE} in full; skim dossiers in ${DOSSIER_DIR}, verification logs in ${VERIFY_DIR}, and the main report ${MAIN_SYNTH} if it exists.
Evaluate against: ${REQUIREMENTS}
Also evaluate: buildability (can an engineer implement each group's model and action set in Python now on synthetic data?), internal consistency (and consistency with the main report if present), evidence quality (unsupported or stale numbers; ignored verification corrections), and whether cross-group interactions are genuinely modeled rather than listed.
Return at most 6 gaps, most severe first. Severity: high = a requirement is unaddressed or a component is not buildable; medium = thin or weakly evidenced; low = polish. Each gap must include a concrete research task that would close it.`

const gapPrompt = (g, i) => `Close a gap in the GROUP report for ADIC's multi-period, robust, agentic portfolio framework.

${BRIEF}

GAP: ${g.gap}
WHY IT MATTERS: ${g.why_it_matters || ''}
TASK: ${g.research_task}

Read the context file ${CONTEXT_FILE} and the group report ${SYNTH_FILE} first (plus relevant dossiers in ${DOSSIER_DIR}). Research as needed (load tools via ToolSearch "select:WebSearch,WebFetch"; Consensus search tools may be used if ToolSearch "consensus" surfaces them - never call the authenticate tools). Never fabricate citations or numbers. Write a focused addendum (1,500-4,000 words, with formulations, sourced and dated numbers, and design implications) to ${ADDENDA_DIR}\\gap_${String(i + 1).padStart(2, '0')}.md using the Write tool. Then return the structured output.`

const revisePrompt = (addenda, critic) => `Revise the GROUP report at ${SYNTH_FILE} for ADIC's multi-period, robust, agentic portfolio framework.

Integrate these addenda (read each in full):
${addenda.map(a => `- ${a.addendum_path}: ${a.summary}`).join('\n')}
Also resolve these contradictions flagged by the critic: ${JSON.stringify((critic && critic.contradictions) || [])}

Edit the report in place with the Edit tool: insert new material into the appropriate sections (not as an appendix dump), fix the inconsistencies, update the executive summary and per-group specifications if conclusions changed, and keep everything else intact. Then return the structured output reflecting the revised report.`

// ---------------- orchestration ----------------
phase('Research')
log(`Launching ${STREAMS.length} group research streams; each is fact-checked as soon as it lands.`)

const streamPromises = {}
for (const s of STREAMS) {
  streamPromises[s.key] = (async () => {
    const r = await agent(researchPrompt(s), { label: `research:${s.key}`, phase: 'Research', schema: RESEARCH_SCHEMA }).catch(() => null)
    if (!r) { log(`Stream ${s.num} ${s.key} failed - excluded from synthesis`); return null }
    const v = await agent(verifyPrompt(s, r), { label: `verify:${s.key}`, phase: 'Verify', schema: VERIFY_SCHEMA }).catch(() => null)
    if (v) log(`Verified ${s.key}: ${v.confirmed}/${v.checked} confirmed, ${v.corrected} corrected, ${v.refuted} refuted, ${v.unverifiable} unverifiable (reliability ${v.overall_reliability})`)
    return { stream: s, research: r, verification: v }
  })()
}

const clusterPromises = CLUSTERS.map(c => (async () => {
  const results = (await Promise.all(c.streams.map(k => streamPromises[k]))).filter(Boolean)
  if (!results.length) return null
  const out = await agent(clusterPrompt(c, results), { label: `synth:${c.key}`, phase: 'Cluster synthesis', schema: CLUSTER_SCHEMA }).catch(() => null)
  if (out) log(`Cluster ${c.key} synthesized`)
  return out
})())

const streamResults = await Promise.all(STREAMS.map(s => streamPromises[s.key]))
const clusters = await Promise.all(clusterPromises)

const gsynth = await agent(groupSynthPrompt(clusters, streamResults), { label: 'synth:groups', phase: 'Group synthesis', schema: GSYNTH_SCHEMA })
log('Group synthesis written: ' + (gsynth ? gsynth.synthesis_path : 'FAILED'))

let finalSynth = gsynth
let critic = null
let addenda = []
if (gsynth) {
  critic = await agent(criticPrompt, { label: 'critic:groups', phase: 'Critique', schema: CRITIC_SCHEMA })
  if (critic && critic.gaps && critic.gaps.length) {
    const high = critic.gaps.filter(g => g.severity === 'high')
    const med = critic.gaps.filter(g => g.severity === 'medium')
    const toFill = high.concat(med).slice(0, 4)
    const skipped = critic.gaps.length - toFill.length
    log(`Critic found ${critic.gaps.length} gaps (${high.length} high, ${med.length} medium); filling ${toFill.length}${skipped > 0 ? `; ${skipped} lower-priority gaps recorded but not researched` : ''}`)
    if (toFill.length) {
      addenda = (await parallel(toFill.map((g, i) => () => agent(gapPrompt(g, i), { label: `gap:${i + 1}`, phase: 'Gap-fill', schema: GAP_SCHEMA })))).filter(Boolean)
      if (addenda.length) {
        const rev = await agent(revisePrompt(addenda, critic), { label: 'revise-groups', phase: 'Gap-fill', schema: GSYNTH_SCHEMA })
        if (rev) finalSynth = rev
      }
    }
  }
}

return {
  streams: streamResults.map((r, i) => r ? {
    stream: r.stream.key,
    dossier: dossierPath(r.stream),
    words: r.research.word_count,
    used_consensus: r.research.used_consensus || false,
    verification: r.verification ? { checked: r.verification.checked, confirmed: r.verification.confirmed, corrected: r.verification.corrected, refuted: r.verification.refuted, unverifiable: r.verification.unverifiable, reliability: r.verification.overall_reliability } : null,
  } : { stream: STREAMS[i].key, failed: true }),
  clusters: clusters.map((c, i) => c ? { cluster: c.cluster, path: c.path } : { cluster: CLUSTERS[i].key, failed: true }),
  synthesis: finalSynth,
  critic,
  addenda: addenda.map(a => ({ gap: a.gap, path: a.addendum_path, summary: a.summary })),
}
