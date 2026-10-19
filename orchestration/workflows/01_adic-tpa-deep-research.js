export const meta = {
  name: 'adic-tpa-deep-research',
  description: 'ADIC multi-period framework: 14-stream multidisciplinary research, adversarial fact-check, cluster + master synthesis, completeness critic, gap-fill',
  phases: [
    { title: 'Research', detail: '14 parallel research streams, each writes a dossier' },
    { title: 'Verify', detail: 'adversarial fact-check of each dossier (pipelined)' },
    { title: 'Cluster synthesis', detail: '4 cluster syntheses as soon as their streams finish' },
    { title: 'Master synthesis', detail: 'integrated research report with cross-disciplinary leaps' },
    { title: 'Critique', detail: 'completeness critic against the user requirements' },
    { title: 'Gap-fill', detail: 'close high-severity gaps and revise the report' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const CONTEXT_FILE = ROOT + '\\inputs\\00_CONTEXT_AND_PRIOR_WORK.md'
const DOSSIER_DIR = ROOT + '\\research\\dossiers'
const VERIFY_DIR = ROOT + '\\research\\verification'
const CLUSTER_DIR = ROOT + '\\research\\clusters'
const ADDENDA_DIR = ROOT + '\\research\\addenda'
const SYNTH_FILE = ROOT + '\\research\\00_SYNTHESIS.md'

const BRIEF = `CLIENT BRIEF (full detail in ${CONTEXT_FILE} - read it first):
ADIC runs a ~US$177bn endowment-model portfolio. It must distribute 5-10% of the fund annually to its sovereign owner; its return target is 10% (nominal USD); leverage is permitted; ~60% is private markets (mostly private equity), and PE distributions (DPI), historically a major cash source, are declining. The user (a quant / data-science lead at ADIC) wants: a multi-period optimization framework with robust scenario analysis and probabilities of outcomes; every strategy/asset examinable through a SELL / HOLD / REFINANCE / LEVER lens; per-asset return data = underwritten return (at inception), current actual return, and the strategy group's forecast return; modeling of a very large multi-asset OTC-derivatives overlay with two strategies (a tail-protection hedge and an opportunistic trading strategy that tries to make money); an agentic architecture (inspired by Sakana AI's 'The Agentic Scientist', arXiv:2610.18933) that performs the analysis; and the ability of the Investment Committee (IC) to discuss the results. The user's prior deck (two-tier robust target-attainment Total Portfolio Approach: Tier 1 = 7% robust floor under model misspecification + liquidity survival gate; Tier 2 = maximize P(10%) and opportunity-cost alpha net of shadow costs; HMM state/fragility engine; 50k-path Monte Carlo; Shapley attribution; multi-agent extraction/challenge/synthesis with deterministic math and human sign-off) is summarized in the context file, together with its gaps versus the new requirements.`

const RULES = (path) => `RESEARCH RULES
1. First Read the context file ${CONTEXT_FILE}.
2. Load web tools with ToolSearch query "select:WebSearch,WebFetch". Use WebSearch mode "standard" for most queries and "extended" for recent market data (2025-2026), niche facts, or when standard results are thin. Read primary sources with WebFetch (arXiv/SSRN/NBER/journal pages, official and regulator reports, reputable practitioner research). WebFetch answers a prompt about the page using a small model, so ask it specific, exhaustive extraction questions. Run many searches (typically 25-60) and read the most important sources rather than relying on snippets.
3. Today is 2026-10-18. Prefer the most recent data and always give as-of dates. Distinguish (a) sourced facts, (b) practitioner consensus, (c) your own inference.
4. Never fabricate citations, numbers or URLs; if you cannot verify something, say so explicitly. Seed references named in your brief are hints from memory - verify authors/years/titles before citing them. Keep verbatim quotes under 125 characters.
5. Think across disciplines: actively seek transferable ideas from operations research, control theory, actuarial science, bank treasury/ALM, insurance, public finance, decision science, real options and machine learning.
6. Write the dossier in Markdown to ${path} using the Write tool. Target 4,000-8,000 words: dense, technical, with equations where they clarify. Sections: 1) Executive summary; 2) Core concepts & theory; 3) Methods/models and trade-offs; 4) Empirical evidence & current market data (dated, sourced); 5) Practitioner/peer practice & case studies; 6) Design implications for the ADIC framework (concrete state variables, decision variables, constraints, objective terms, equations, parameters with default values, calibration targets, data needs); 7) Implementation notes (Python libraries, algorithms, complexity, numerical pitfalls); 8) Risks, pitfalls & limitations; 9) Open questions; 10) References (full citations with URLs).
7. Then return the structured output, faithfully summarizing the dossier. load_bearing_claims = the 10-20 empirical claims/numbers your recommendations depend on most, each with its source URL.`

const STREAMS = [
  { num: '01', key: 'mpo', title: 'Multi-period portfolio optimization & sequential decision methods', body: `Focus: the mathematical and computational core of a multi-period (dynamic) portfolio decision framework for a ~$177bn endowment-model fund with ~60% illiquid assets, quarterly decisions, a 5-10 year horizon, asset-level discrete-ish actions (sell / hold / refinance / lever), portfolio leverage, a derivatives overlay, and hard requirements on annual distributions (5-10% of NAV) and liquidity survival.

Research and compare, with formulations:
(a) Dynamic programming & stochastic control for portfolio choice: Merton/Samuelson; Campbell-Viceira strategic asset allocation; Brandt, Goyal, Santa-Clara & Stroud (2005) simulation-and-regression ADP; the curse of dimensionality and what it implies here.
(b) Multistage stochastic programming for ALM: Russell-Yasuda Kasai (Carino, Ziemba et al.), InnoALM (Geyer & Ziemba), CAP:Link (Mulvey), Dantzig-Infanger, Kouwenberg (2001) scenario generation for ALM, Hoyland-Wallace moment matching, Pflug-Pichler nested distance; SDDP including Markov-chain (regime) SDDP and risk-averse nested CVaR (Pereira-Pinto; Shapiro; Philpott; Dowson & Kapelevich SDDP.jl; Kozmik & Morton); progressive hedging (Rockafellar-Wets; mpi-sppy).
(c) Model predictive control / rolling-horizon convex optimization: Boyd et al. (2017) 'Multi-Period Trading via Convex Optimization'; Nystrup, Boyd, Lindstrom & Madsen (drawdown control; regime-based MPC); certainty-equivalent vs scenario-based MPC.
(d) Decision rules: linear/piecewise-linear decision rules and affinely adjustable robust counterparts (Ben-Tal et al.; Kuhn, Wiesemann & Georghiou); use for chance-constrained multi-stage problems.
(e) Policy search / simulation-optimization: parametric policies tuned by Monte Carlo (CMA-ES, Bayesian optimization, cross-entropy, stochastic approximation, gradients through differentiable simulators e.g. JAX); common random numbers; overfitting to scenarios and out-of-sample validation.
(f) Reinforcement learning for portfolio/ALM: what works, what does not (sample efficiency, non-stationarity, interpretability, safety), and when RL is inappropriate for a fiduciary.
Organize everything with Warren Powell's unified framework for sequential decisions (state, decision, exogenous information, transition, objective; policy classes PFA, CFA, VFA, DLA) and recommend a hybrid for ADIC.

Also cover: fixed costs and discrete actions (MILP vs convex relaxation vs rounding heuristics); commitment-call-distribution dynamics of illiquid assets inside optimization models; leverage, margin and collateral constraints; chance constraints and convex approximations (CVaR, Bernstein, the scenario approach of Calafiore-Campi); time consistency; terminal-value and horizon effects; here-and-now vs recourse decisions; value of the stochastic solution (VSS) and EVPI as IC-facing diagnostics; dual variables/shadow prices from scenario LPs as decision support (e.g., a state- and time-contingent shadow price of liquidity); Lagrangian/dual decomposition, Benders and progressive hedging for scale (hundreds of assets x thousands of scenarios).
Python tooling: cvxpy (CLARABEL, ECOS, SCS, OSQP, HiGHS, MOSEK, Gurobi), Pyomo + mpi-sppy, scipy.optimize/HiGHS, OR-Tools, PySDDP/msppy, JAX/numba for fast simulation, nevergrad/optuna/cma for policy search. Give realistic problem sizes and solve times.
Deliverable emphasis: a recommended layered optimization architecture for ADIC with explicit formulation sketches (state, decision variables, transitions, constraints, objective), including (i) a here-and-now two-stage or multistage scenario program for today's IC decisions that exposes shadow prices, (ii) a rolling-horizon/MPC or parametric-policy simulator for evaluating policies over 5-10 years with thousands of paths, and (iii) how the two interact.` },

  { num: '02', key: 'endowment_swf', title: 'Endowment model, distribution/spending policy, SWF peer practice & Total Portfolio Approach', body: `Focus: how endowment-model funds and sovereign funds set and manage spending/distributions, return targets, private-market allocations and total-portfolio frameworks - and what ADIC (5-10% annual distributions, 10% target, leverage allowed, ~60% private) should learn.

Research:
- Theory: Tobin (1974) intergenerational equity; Merton (1993) 'Optimal investment strategies for university endowment funds'; Dybvig ratchet / no-decline spending ('Using asset allocation to protect spending'); Dimmock, Wang & Yang 'The Endowment Model and Modern Portfolio Theory' (illiquidity + spending + leverage); Gilbert & Hrdlicka (2015); Brown, Dimmock, Kang & Weisbenner (2014, AER) on endowment payout responses to shocks; Campbell (2012) 'Investing and spending'; Cejnek, Franz, Randl & Stoughton survey; Ennis critiques of endowment-model performance.
- Spending-rule designs and dynamics: fixed % of trailing average NAV; Yale/Stanford hybrid (smoothing weight + target rate x NAV, inflation adjustment); Alaska Permanent Fund POMV (5% of average of 5 of the last 6 years); Norway's fiscal rule (3% expected real return); band rules (min/max); quantify spending volatility vs NAV sustainability trade-offs.
- Feasibility arithmetic for ADIC: with 5-10% distributions and a 10% nominal target, implied real growth, depletion probabilities under realistic return volatility, volatility drag, sequence-of-returns risk; is the 10% target gross or net of distributions (analyze both interpretations and their consequences).
- Stress history of the endowment model: 2008-09 (Harvard, Yale, Stanford, Princeton liquidity crises, bond issuance, private secondary sales), the 2022 denominator effect, 2024-2026 pressures (Yale and Harvard secondary sales in 2025, US endowment tax changes), recent performance vs 60/40 (NACUBO/Commonfund, Cambridge Associates, FY2024-FY2026 where available).
- SWF and pension peers: Norway NBIM (fiscal rule, rebalancing rules), CPP Investments (Reference Portfolio, TPA, leverage), NZ Super (Reference Portfolio, active strategies, derivatives overlay, TPA), Australia's Future Fund (TPA, liquidity), GIC (Reference Portfolio + Active Portfolio framework), Temasek (Astrea PE bonds, return targets), ADIA, Mubadala, Alaska Permanent Fund (POMV draw, private markets), Texas PSF, KIA. Extract concrete practices: risk budgeting, reference portfolios, leverage use, liquidity policy, private-markets pacing, distribution management, IC processes.
- Total Portfolio Approach: Thinking Ahead Institute/WTW, CAIA, CFA Institute and peer write-ups (2019-2026): operational meaning, governance, opportunity-cost / 'funding basket' comparison of proposals (relevant to the user's alpha*), common pitfalls.
Deliverable emphasis: how to model ADIC's distribution requirement (deterministic rule within the band, stochastic exogenous demand, or decision variable); candidate distribution rules to test; which peer practices to adopt (and which not); implications for objectives and constraints.` },

  { num: '03', key: 'sovereign_alm', title: 'Sovereign ALM: oil-fiscal linkage and distribution demand as a stochastic liability', body: `Focus: ADIC distributes to a sovereign owner whose fiscal position depends heavily on hydrocarbons. Investigate whether and how the owner's distribution demands (within the 5-10% band) co-move with oil prices, global markets and private-market exit conditions - i.e., liability-side 'wrong-way risk' - and what this implies for ADIC's portfolio, liquidity buffers and hedging.

Research:
- Theory of SWF allocation with non-tradable resource wealth and fiscal liabilities: Gintschel & Scherer (2008) 'Optimal asset allocation for sovereign wealth funds'; Scherer on oil-based SWFs; van den Bremer, van der Ploeg & Wills (2016) 'The elephant in the ground'; Bodie & Briere (2014) sovereign balance sheet / contingent claims; IMF work on sovereign ALM (e.g., Das, Lu, Mulder & Sy 2009) and on stabilization vs savings funds; Ang, Goetzmann & Schaefer reports for Norway; hedging below-ground oil wealth.
- Empirical: oil-price correlations with global equities, credit spreads, and PE exit/distribution activity across regimes (2008, 2014-16, 2020, 2022); evidence of Gulf/oil SWF withdrawals during oil busts (Saudi Arabia 2015-16 and 2020, Kuwait's General Reserve Fund 2020-21, Norway's first net withdrawals 2016 and 2020, Oman, Bahrain); IMF Regional Economic Outlook estimates of UAE / Abu Dhabi fiscal breakeven oil prices (latest 2025-2026); UAE fiscal diversification.
- Modeling: a stochastic distribution-demand model D_t = clip(f(oil_t, fiscal balance_t, policy), 5%, 10%) x NAV with regime dependence; scenario archetypes (oil-down / global recession, oil-up / inflation, long-run energy-transition demand decline, peg stress); calibration with limited data (expert elicitation, IMF projections).
- Hedging: oil puts/collars vs equity puts for a sovereign whose liabilities are oil-sensitive; theory that an oil SWF should underweight oil-correlated assets; cross-hedging and basis risk; designing ADIC's tail hedge for the joint state 'oil down + equities down + exits closed'.
- Abu Dhabi / UAE institutional context from PUBLIC sources only: the Abu Dhabi SWF landscape (ADIA, Mubadala, ADQ, L'imad, ADIC); what is publicly reported about ADIC's history and current status (established 2007; integration into Mubadala in 2018 - verify and report any later changes); strictly factual, flag uncertainty, no speculation about internal matters.
Deliverable emphasis: concrete factor and liability design for the scenario generator (oil, fiscal draw), constraints (e.g., distribution coverage under oil-down regimes), and hedge-design implications.` },

  { num: '04', key: 'pe_cashflows', title: 'Private equity cash-flow & NAV modeling; the DPI decline', body: `Focus: a regime-dependent stochastic model of capital calls, distributions and NAV for ADIC's private book (~$106bn of a $177bn fund, mostly PE), capturing today's distribution drought and plausible recovery/deterioration paths.

Research:
- Cash-flow models: Takahashi & Alexander (2002) Yale model; stochastic extensions (Buchner, Kaserer & Wagner 2010; de Malherbe; Jeet/MSCI 'market-sensitive periodic growth'; Tausch & Pietz; Cambridge Associates, Hamilton Lane, StepStone, BlackRock, MSCI pacing models); Brown, Ghysels & Gredil (2023 RFS) nowcasting NAVs; cash-flow-at-risk; how calls and distributions depend on public equity levels, credit spreads, M&A and IPO activity (elasticities).
- LP portfolio choice with commitments: Gourier, Phalippou & Westerfield 'Capital Commitment' (JF 2024); Giommetti & Jorgensen 'Optimal allocation to private equity'; Ang, Papanikolaou & Westerfield (2014); Sorensen, Wang & Yang (2014 RFS) 'Valuing private equity'; over-commitment strategies and pacing rules.
- NAV smoothing and true risk: Geltner unsmoothing; Getmansky, Lo & Makarov (2004); Couts, Goncalves & Rossi (2020); estimated PE betas; PE performance measurement: PME (Kaplan & Schoar), GPME (Korteweg & Nagel), direct alpha (Gredil, Griffiths & Stucke), strip-based valuation (Gupta & Van Nieuwerburgh 2021 JF), Driessen, Lin & Phalippou; Ang, Chen, Goetzmann & Phalippou (2018).
- Current market data (dated, sourced, 2022-2026): distribution yields (distributions/NAV) by year; DPI by vintage (2015-2021); exit volume and holding periods; unrealized value overhang and unsold companies (Bain Global Private Equity Report 2025 and 2026, McKinsey Global Private Markets Review 2025/2026, PitchBook, Preqin, Carta, Raymond James, Hamilton Lane, MSCI/Burgiss, Cambridge Associates); call rates; IPO window 2025-2026; outlook for distributions 2026-2028.
- Calibration targets by strategy (buyout, growth, VC, private credit, real estate, infrastructure, secondaries, co-investments): call schedules, distribution rates by age, bow factors, fund-life extensions, NAV growth, betas, idiosyncratic vol.
Deliverable emphasis: a concrete, implementable model - equations for per-asset (or per-cohort) economic NAV, reported NAV (lag/smoothing), calls and distributions as functions of age, regime and market factors; parameter tables with sources; how to plug asset-level forward-return beliefs (from fusing underwritten/actual/forecast returns) into NAV drift; how to represent the current DPI drought and scenarios of its persistence or recovery.` },

  { num: '05', key: 'secondaries_navfin', title: 'Liquidity tools for private holdings: secondaries, NAV financing, continuation vehicles, preferred equity, CFOs - the economics of SELL and REFINANCE', body: `Focus: the instruments ADIC can use to sell or refinance private holdings, their pricing, availability by market regime, and how to compute each instrument's implied cost of liquidity.

Research:
- LP-led secondaries: pricing (% of NAV) by strategy, fund age, quality and regime - historical series 2008-2026 (Jefferies, Lazard, Evercore, PJT Park Hill, Greenhill/Mizuho, Campbell Lutyens, Setter, Coller Capital); 2025 and 1H-2026 volumes and pricing; portfolio vs single-fund sales; tail-end discounts; deferred-payment structures; unfunded transfer; academic work on discounts and the cost of liquidity (Nadauld, Sensoy, Vorkink & Weisbach 2019 JFE; Bollen & Sensoy; Albuquerque, Cassel, Phalippou & Schroth 2018; Kleymenova, Talmor & Vasvari).
- Case studies: Yale's 2025 secondary sale(s); Harvard's 2025 sale; other endowments/pensions/SWFs (CalPERS, CalSTRS, New York pensions, GIC, Temasek, Mubadala, ADIA) 2023-2026; Harvard and others' forced sales in 2008-09; lessons on timing, pricing and governance.
- GP-led continuation vehicles: volumes, pricing, LP elections (roll vs sell), fairness opinions, ILPA guidance.
- NAV financing: LP-level vs fund-level NAV loans; LTV ranges, pricing (SOFR + spread), tenors, covenants (LTV triggers, cash sweeps, PIK toggles), market size 2024-2026, providers; risks (LTV breaches in downturns acting like margin calls, cross-collateralization, cash sweeps); ILPA 2024 guidance; use-of-proceeds controversies.
- Preferred equity and structured secondaries; collateralized fund obligations (CFOs) and rated note feeders (NAIC treatment); Temasek's Astrea PE bond series as a sovereign template (structure, tranches, ratings, coupons, retained equity); other SWF/pension securitizations.
- Subscription lines (GP-level) and their effect on DPI/IRR timing.
Deliverable emphasis: an 'action economics' library - for each instrument: immediate proceeds; future cash flows given up; financing costs; retained upside/downside; unfunded commitment transfer; execution time; availability and pricing as functions of market regime; signaling/relationship costs; irreversibility. Give formulas for each instrument's implied cost of liquidity (IRR of the liquidity raised) and a pecking-order / marginal-cost-of-liquidity curve construction, with dated calibration numbers.` },

  { num: '06', key: 'leverage', title: 'Portfolio-level leverage for an endowment/SWF with illiquid assets', body: `Focus: when and how ADIC should use leverage (it is permitted), at portfolio and asset levels, given ~60% illiquid assets, mandatory 5-10% distributions, a large derivatives overlay, and a 10% target.

Research:
- Theory: optimal leverage with illiquid assets and funding risk - Ang, Papanikolaou & Westerfield; Dimmock, Wang & Yang; Brunnermeier & Pedersen (2009) liquidity spirals; Frazzini & Pedersen (2014) and Asness, Frazzini & Pedersen (2012) leverage aversion / risk parity; Kelly / fractional Kelly; volatility drag; Grossman-Zhou drawdown constraints; leverage + spending + illiquidity interaction (forced-sale cascades).
- Sources and terms (2024-2026): bond issuance by endowments/SWFs/pensions (Harvard, Yale, Stanford, CPP Investments, OTPP, OMERS, Temasek, Mubadala, PIF), repo of government bonds, revolving credit facilities, NAV facilities, derivatives/synthetic exposure (futures, TRS, swaps - implied financing costs), securities lending; maturity profiles, covenants, ratings.
- Practice: CPP Investments' leverage policy and ratios; GIC; NZ Super; Canadian/Dutch pension repo-financed duration; Norway's no-leverage policy; post-2022 UK LDI lessons for leveraged overlays (Bank of England); 2008 endowment experiences (Harvard swaps, bond issuance).
- Risk metrics and limits: gross/net/economic leverage, liquidity coverage under stressed haircuts, encumbrance, maturity matching, recourse, covenant headroom, rating impact.
Deliverable emphasis: how to model leverage as decision variables (cost curves by source, availability and haircuts by regime, LTV/covenant dynamics), which constraints to impose, and decision rules for when 'LEVER' is rational for an asset or for the total portfolio (forward expected return vs all-in financing cost plus risk and liquidity penalties), with quantified examples.` },

  { num: '07', key: 'return_fusion', title: 'Fusing underwritten, current-actual and forecast returns into calibrated forward beliefs', body: `Focus: for each private asset/strategy ADIC has (1) the underwritten return at inception, (2) the current actual return, (3) the strategy group's forecast. Design a principled, auditable method to fuse these into a calibrated distribution of FORWARD returns (on current NAV) that drives sell/hold/refinance/lever decisions and the simulator. Note: the user's prior work mined an 18-year IC memo corpus (QDD); discuss how such a corpus (underwritten base/downside cases and realized outcomes) can calibrate underwriting bias and forecaster credibility.

Research:
- Forecast combination: Bates & Granger (1969); Timmermann (2006, Handbook of Economic Forecasting); the forecast-combination puzzle; optimal weights with correlated errors; shrinkage to equal weights; Bayesian model averaging.
- Bayesian updating and credibility: Buhlmann and Buhlmann-Straub credibility (actuarial science), weight = n/(n+k); hierarchical / empirical-Bayes partial pooling across assets, strategies and managers; Kalman filtering for evolving beliefs; Black-Litterman views with confidences; Meucci entropy pooling.
- Evidence on biases: underwriting optimism (target vs realized returns in PE, real estate, infrastructure; reference-class forecasting and optimism bias - Kahneman & Lovallo; Flyvbjerg); interim valuation behavior (Jenkinson, Sousa & Stucke 2013; Barber & Yasuda 2017; Brown, Gredil & Kaplan 2019 'Do private equity funds manipulate reported returns?'); how predictive interim IRR/TVPI at age t is of final outcomes (Harris, Jenkinson, Kaplan & Stucke on persistence; Korteweg & Sorensen 2017 'Skill and luck in private equity performance'); J-curve distortions; disposition effect and escalation of commitment in internal investment teams; agency/incentive bias in internal forecasts; calibration of expert forecasts (Tetlock).
- Since-inception vs forward: why since-inception IRR is a sunk-cost metric for hold/sell decisions; implied forward IRR from forecast MOIC/TVPI and remaining life; consistency checks (e.g., a forecast implying a forward IRR far above base rates for that strategy and age).
- Calibration and scoring: proper scoring rules (log score, CRPS), calibration curves, PIT histograms, track-record-based forecaster weights per strategy group, drift detection; learning the weights from ADIC's own history of underwritten -> interim -> realized, and literature-based priors when history is thin.
Deliverable emphasis: a concrete model specification with equations - inputs (u, a, f, asset age, strategy, NAV staleness, forecaster track record, dispersion), outputs (posterior mean and variance of forward return; probability the forecast is optimistic; flags), default prior parameters from the literature, worked numerical examples, and diagnostics an IC can understand.` },

  { num: '08', key: 'action_valuation', title: 'Unifying SELL / HOLD / REFINANCE / LEVER: real options, liquidity shadow prices, decision theory', body: `Focus: a single decision-theoretic framework in which every asset-level action is valued in a common currency that is consistent with the portfolio-level multi-period optimization.

Research:
- Real options and optimal stopping for divestment/abandonment and timing (Dixit & Pindyck; McDonald & Siegel; option to wait vs sell; irreversibility premium); valuing illiquid holdings for an investor with liquidity needs (Sorensen, Wang & Yang; Ang, Papanikolaou & Westerfield; Longstaff 2001 and 2009; Kahl, Liu & Longstaff).
- The shadow price of liquidity: Lagrange multipliers of liquidity/distribution constraints in scenario ALM programs; state- and time-contingent liquidity values; liquidity-adjusted NPV; bank treasury funds-transfer-pricing (FTP) curves and contingent-liquidity charges (Basel LCR/NSFR concepts); insurer ALM; constructing a marginal-cost-of-liquidity (MCL) curve from available sources (credit lines, NAV loans, secondaries, liquid-asset sales, pausing commitments).
- Decision framework: represent each action as a bundle of state-contingent cash flows, risk contribution, irreversibility and governance/relationship cost; value it with the fund's stochastic discount factor or with scenario shadow prices; derive decision rules (sell if price >= liquidity-adjusted continuation value; refinance if implied cost < MCL and retained upside is valuable; lever if forward expected return - all-in cost - risk and liquidity penalties > 0); show how portfolio-level duals price liquidity, risk budget and leverage capacity for asset-level decisions (Lagrangian / price decomposition), making hundreds of decisions tractable and explainable.
- Behavioral pitfalls: sunk cost (since-inception IRR), disposition effect, anchoring to NAV, fire-sale risk; how to present to an IC.
- Portfolio interplay: tail-end vs core fund sales, diversification and vintage concentration, unfunded transfer, GP relationships and re-up rights.
Deliverable emphasis: precise formulations and at least two fully worked numerical examples (e.g., a 2018-vintage buyout fund: NAV $500m, unfunded $50m, fused forward IRR 11% +/- 6%, secondary bid 88% of NAV, NAV loan available at SOFR+600bps with 15% LTV, current portfolio liquidity shadow price 9% p.a. in years 1-2 falling to 4% - what to do and why; and a case where LEVER is optimal).` },

  { num: '09', key: 'overlay', title: 'Derivatives overlay: tail protection, opportunistic trading, collateral & margin liquidity', body: `Focus: ADIC runs a very large multi-asset OTC (bilateral ISDA/CSA) derivatives overlay with (a) a tail-protection hedge and (b) an opportunistic trading strategy that tries to make money. Research how to model, value and optimize both inside a multi-period total-portfolio framework with illiquid assets and mandatory distributions.

Research:
- Tail-hedging evidence and design: protective puts, put spreads, collars, VIX calls, variance swaps, CDS index protection, long Treasuries, trend-following/managed futures ('crisis alpha'), defensive factors; carry cost; monetization/reset rules; evidence from Israelov (AQR 'Pathetic protection'), Israelov & Nielsen, Harvey et al. (2019, Man Group 'The best of strategies for the worst of times'), Hamill, Rattray & Van Hemert (trend), Bhansali 'Tail Risk Hedging', Spitznagel/Universa claims and critiques, Cboe benchmark indices (PPUT, CLL), the variance-risk-premium literature.
- Valuing tail protection inside a total portfolio with illiquid assets and spending: the hedge as state-contingent liquidity (cash/collateral inflows exactly when PE distributions stop, secondary discounts widen, margin calls hit and fiscal draws may rise) and as rebalancing capital; methods to quantify (scenario valuation with liquidity shadow prices; avoided forced-sale costs; impact on P(distribution breach), P(target), drawdown); optimal hedge ratio, strike, tenor, roll and monetization design; when hedges with negative expected return are worth holding.
- Opportunistic overlay strategies: typical designs (macro, relative value, carry, trend, dispersion, rates curve), realistic Sharpe ratios and their uncertainty (Bayesian shrinkage; deflated Sharpe ratio - Bailey & Lopez de Prado), crowding, crisis correlation, capacity, risk budgeting (vol targets, drawdown stops), modeling their return distributions.
- Collateral and margin: ISDA/CSA mechanics, daily VM, IM (SIMM, uncleared margin rules), cleared vs bilateral, eligible collateral and haircuts, margin procyclicality (BCBS-IOSCO 2022 review, ESRB), stress episodes (March 2020 dash for cash; UK LDI September 2022 - Bank of England; 2022 commodity margin spike); liquidity stress testing of derivatives books; magnitude rules of thumb.
- Synthetic beta overlays / portable alpha for rebalancing and managing exposure when private NAVs are stale; the overlay as the fast policy lever (hedge vs amplify).
Deliverable emphasis: simulation-ready models for (i) tail-hedge P&L, carry, monetization and collateral flows under regime-switching scenarios (option pricing with regime-dependent implied vol and skew), (ii) opportunistic-strategy returns, drawdowns and margin, (iii) overlay financing and VM for synthetic exposure; plus integration into liquidity constraints and the optimizer (decision variables, constraints, valuation in the objective).` },

  { num: '10', key: 'scenarios_robustness', title: 'Scenario generation, regime models, robustness & probabilistic stress testing', body: `Focus: generating credible joint scenarios for ADIC's assets, liabilities and liquidity; making decisions robust to model misspecification; conditioning results on IC views.

Research:
- Economic scenario generators for long-horizon ALM: VAR (Campbell-Viceira), regime switching (Hamilton; Ang & Bekaert; Guidolin & Timmermann), HMM/HSMM regime inference (Nystrup et al.), GARCH/stochastic vol, fat tails (Student-t, skewed-t), copulas (t, vine), stationary/block bootstrap, filtered historical simulation; macro-financial factors (growth, inflation, rates, credit spreads, equities, oil, USD, volatility); calibrating to capital-market assumptions (JPM LTCMA 2026, BlackRock, Vanguard, AQR, Research Affiliates, GMO - record the 2026 numbers for major asset classes); consistency for option pricing (implied-vol dynamics).
- Scenario reduction and trees for optimization (Heitsch & Romisch, Hoyland & Wallace moment matching, clustering, optimal quantization); sample-average approximation error and out-of-sample evaluation; how many paths are needed for P99 metrics, with standard errors.
- Robustness: DRO with phi-divergence/KL balls (Ben-Tal, den Hertog, De Waegenaere, Melenberg & Rennen 2013), Wasserstein (Mohajerin Esfahani & Kuhn 2018), moment-based (Delage & Ye 2010); Hansen & Sargent robustness (multiplier preferences, entropy penalty); Glasserman & Xu (2014) robust risk measurement; robust satisficing (Long, Sim & Zhou 2023 Operations Research; Brown & Sim 2009; Chen & Sim goal-driven optimization); model ensembles / misspecification sets (relevant to the user's 7% robust floor); ambiguity about private-asset parameters.
- Probabilistic stress testing and views: reverse stress testing (Breuer & Csiszar 'Systematic stress tests with entropic plausibility constraints'; Glasserman, Kang & Kang 'Stress scenario selection by empirical likelihood'); Bayesian networks for coherent stress scenarios (Rebonato 2010; Rebonato & Denev 2014); Meucci entropy pooling ('Fully Flexible Views', 'Fully Flexible Probabilities') to condition scenario sets on views; narrative-to-quantitative scenario translation; eliciting probabilities from experts/IC.
- Model risk management (SR 11-7 / OCC 2011-12, PRA SS1/23): validation, benchmarking, sensitivity analysis, documentation - and how to apply it to an LLM-agent-assisted system.
Deliverable emphasis: a recommended ESG design for ADIC (factors, regime structure, frequency, horizon, calibration, path counts), a cheap-to-compute robustness layer on simulated scenarios (worst-case metrics over KL/Wasserstein balls; robust-satisficing fragility), and a view-conditioning design (entropy pooling) with equations and algorithms.` },

  { num: '11', key: 'objectives', title: 'Objective design: target attainment with mandatory distributions, leverage and illiquidity', body: `Focus: the precise objective and constraint set ADIC's multi-period optimizer should use to 'meet distributions with near-certainty, survive liquidity stress, preserve long-run value, and pursue a 10% return'. Build on and critique the user's two-tier design (Tier 1 robust 7% floor + liquidity gate; Tier 2 maximize P(10%) and alpha* net of shadow costs).

Research:
- Goal-based investing: Browne (1999) 'Reaching goals by a deadline' (digital-option-like optimal policies, 'gambling for resurrection'); Das, Ostrov, Radhakrishnan & Srivastav (2020) DP for goals-based wealth management; Das, Markowitz, Scheid & Statman (2010) mental accounts; Brunel; target attainment in ALM.
- Pathologies of P(target) maximization and remedies: expected shortfall vs target and lower partial moments (Fishburn), CVaR (Rockafellar & Uryasev), utility with floors/habits (Dybvig ratchet; Constantinides), loss aversion / prospect theory, drawdown control (Grossman-Zhou; Cvitanic-Karatzas; Chekhlov, Uryasev & Zabarankin CDaR), satisficing and robust satisficing (Brown & Sim; Long, Sim & Zhou), lexicographic/two-tier designs, multi-objective Pareto frontiers.
- Time consistency (nested vs end-of-horizon risk measures; Shapiro, Ruszczynski), horizon choice (3/5/10 years; rolling), annualized vs cumulative, geometric vs arithmetic, nominal vs real; how a 10% target interacts with 5-10% distributions (gross vs net-of-distribution interpretations; NAV sustainability); how leverage changes the attainable set.
- Chance constraints on distributions and liquidity (e.g., P(pay >= 5% each year) >= 99%) and convex approximations (CVaR, scenario approach); robust floors under misspecification.
Deliverable emphasis: a precise recommended objective + constraint specification (equations and convex surrogates); how to present trade-offs to the IC (frontiers of P(10%) vs P(distribution breach) vs robust floor vs liquidity); how to avoid target-chasing; how to set the numbers (99%? 95%? which horizon?) with justification.` },

  { num: '12', key: 'agentic_ai', title: 'Agentic AI architectures for automated discovery & quantitative investment analysis', body: `Focus: the state of the art (through October 2026) in agentic AI systems that (a) automate scientific/quantitative discovery and (b) support investment analysis - to design an 'agentic portfolio laboratory' for ADIC. (A separate agent deep-reads 'The Agentic Scientist' paper; you cover the broader landscape and engineering patterns.)

Research:
- Automated discovery systems and orchestration patterns: Sakana 'The AI Scientist' (v1, v2), Google 'AI co-scientist' (generate-debate-evolve; tournament/Elo ranking), DeepMind AlphaEvolve and FunSearch (LLM-guided evolutionary program search with automated evaluators), Agent Laboratory, AI-Researcher, data-to-paper, FutureHouse systems, and other 2025-2026 systems; mechanisms: idea generation, novelty checks, sandboxed experiments, automated reviewers/rubrics, tree search over experiments, meta-controllers, budget allocation, provenance, human co-discovery; documented failure modes (reward hacking, fabricated results, p-hacking analogues).
- LLM multi-agent systems in finance: TradingAgents, FinCon, FinRobot, FinMem, FinAgent, AlphaAgents, persona-based 'AI hedge fund' agents, MarketSenseAI, and any 2025-2026 asset-owner deployments (public statements by large pensions/SWFs/asset managers about agentic AI in investment processes); evidence of value and failure modes (hallucinated numbers, look-ahead bias, overconfidence, herding/homogeneity across agents).
- Tool-grounded designs where deterministic engines compute numbers and LLMs plan/critique/explain: function calling / MCP, typed tool contracts, code-execution sandboxes, claim-to-evidence provenance, run manifests and reproducibility, caching, evaluation harnesses (rubric-based LLM judges, golden test sets, regression tests), guardrails (every number must cite a tool output), cost/latency control. Include Anthropic's engineering guidance ('Building effective agents': workflows vs agents, orchestrator-workers, evaluator-optimizer; the multi-agent research system write-up; the Claude Agent SDK; MCP) and alternatives (LangGraph, AutoGen/AG2, CrewAI, OpenAI Agents SDK), with suitability for a regulated sovereign investor (on-prem/VPC, data security, auditability).
- Applying discovery patterns to portfolio analytics: hypotheses = candidate policies/actions/scenarios; experiments = simulator/optimizer runs; baselines and ablations = static SAA, rule policies, component ablations/Shapley; verification = rubric checks + adversarial review; report = IC memo; LLM-guided policy search (AlphaEvolve-style) over interpretable policy rules evaluated by a deterministic simulator, with safeguards against overfitting to simulated scenarios.
- AI governance for investment decisions: SR 11-7 applied to LLM components, NIST AI RMF, ISO/IEC 42001, audit trails, human decision rights, UAE/Abu Dhabi AI policy context (public).
Deliverable emphasis: a reference architecture (components, agent roles, tools, data flows, control loops, verification gates, provenance) with concrete patterns and anti-patterns, and a recommendation of runtime/framework choices.` },

  { num: '13', key: 'paper_deepread', title: "Deep read: 'The Agentic Scientist' (arXiv:2610.18933)", body: `Focus: read the ENTIRE paper 'The Agentic Scientist: Orchestrating Coding Agents for Automated Scientific (Co-)Discovery' (Lange, Grillotti, Yamada, Charakorn, Ha; Sakana AI; arXiv:2610.18933v1, October 2026). Use WebFetch on https://arxiv.org/html/2610.18933v1 and page through the whole document with the offset parameter until the end, including appendices (prompts, rubrics, ablations). Because WebFetch answers via a small model, issue many targeted extraction prompts (section by section, figure by figure, appendix by appendix) asking for exhaustive detail. If the HTML fails, try https://arxiv.org/abs/2610.18933 and https://arxiv.org/pdf/2610.18933v1. Also search for any accompanying blog post, code repository, or discussion (e.g., Sakana AI blog, GitHub).

Extract precisely: the system architecture; every pipeline stage (purpose, inputs, outputs, agents involved, prompts/rubrics, verification criteria, failure handling); the meta-controller (scheduling, parallelism, budget and compute allocation, retries, state management, how it decides to advance or redo stages); how human input enters ('co-discovery'); sandboxing and environment management; result aggregation; how baselines and ablations are automated; analysis and report writing; evaluation methodology and results (e.g., ALIFE 2026 acceptance, autonomous runs on open ML problems), orchestration ablations and the evidence that orchestration matters more than base-model capability; costs; limitations and failure modes; any released prompts/rubrics.

Then translate for ADIC: a detailed mapping table from each mechanism to an 'agentic portfolio laboratory' supporting IC decisions (asset-level sell/hold/refinance/lever analysis, scenario analysis, multi-period policy optimization, overlay design, IC deliberation). For each mechanism: what transfers directly, what must be adapted (e.g., 'novelty' -> 'decision relevance'; 'paper' -> 'IC memo'; 'reviewer' -> 'risk/model-validation rubric'), and what must NOT transfer (fiduciary accountability, determinism and auditability, confidentiality, no autonomous execution of trades). Propose concrete rubrics for each stage of an investment-analysis pipeline, modeled on the paper's rubrics. Cite sections/figures; keep verbatim quotes under 125 characters.` },

  { num: '14', key: 'ic_deliberation', title: 'Investment-committee deliberation, decision science & human-AI co-deliberation', body: `Focus: how an IC should discuss and decide using the framework's probabilistic outputs, and how AI agents can improve (not degrade) that deliberation.

Research:
- IC governance for large asset owners/SWFs: decision rights and delegation, IC composition, pre-reads and decision memos, dissent recording, escalation, two-key approvals; Clark & Urwin best-practice governance; Ambachtsheer; the Santiago Principles (IFSWF); CFA Institute / ILPA guidance; examples (CPP Investments, NZ Super, Future Fund, Norway's Ministry-NBIM split).
- Decision science for committees: groupthink (Janis), hidden profiles (Stasser & Titus), anchoring and order effects, noise and decision hygiene (Kahneman, Sibony & Sunstein; the mediating assessments protocol), pre-mortems (Klein), devil's advocacy vs dialectical inquiry (Schwenk), Delphi and the nominal group technique, independent estimates before discussion, calibrated probability elicitation and Brier scoring (Tetlock), decision journals, reference-class forecasting (Flyvbjerg), structured analytic techniques (Heuer & Pherson: ACH, key assumptions check, indicators and signposts).
- Multi-agent LLM debate and simulated committees: Du et al. (2023); Liang et al. (2023); Irving, Christiano & Amodei (2018); Khan et al. (2024); ChatEval; evidence on when debate helps; failure modes (sycophancy, conformity / majority collapse, persona caricature, homogeneous 'opinions', persuasion over truth); AI-mediated deliberation (Tessler et al. 2024 Science, the 'Habermas Machine'; Polis / Talk to the City); AI as facilitator vs participant; human-AI teaming and automation bias.
- Interfaces for IC discussion of model results: interactive what-if (views -> re-weighted scenarios), explanation (attribution, binding constraints and shadow prices, counterfactuals), uncertainty communication (fan charts, frequency framing - Gigerenzer; Spiegelhalter), disagreement mapping (each member's views -> implied decision), voting with rationale capture, minutes, action tracking, closed-loop learning (forecast vs outcome scoring).
Deliverable emphasis: a concrete 'IC deliberation module' design - (1) an AI shadow-IC with diverse, evidence-grounded roles and a structured protocol (independent assessment -> reveal -> structured debate -> pre-mortem -> minority report -> questions for the human IC); (2) human-IC interaction (Q&A grounded in run artifacts, live view-conditioning via entropy pooling, decision and dissent capture); (3) safeguards (numbers only from tools with run citations, dissent preservation, no persuasion optimization, automation-bias countermeasures); (4) evaluation of whether it improves decision quality.` },
]

const CLUSTERS = [
  { key: 'C1_portfolio_math', title: 'Optimization core, scenario & robustness layer, objective design', streams: ['mpo', 'scenarios_robustness', 'objectives'] },
  { key: 'C2_private_liquidity', title: 'Private book, liquidity instruments, leverage, asset-level action economics, return-belief fusion', streams: ['pe_cashflows', 'secondaries_navfin', 'leverage', 'action_valuation', 'return_fusion'] },
  { key: 'C3_liabilities_overlay', title: 'Distribution policy & sovereign liabilities, peers/TPA, derivatives overlay', streams: ['endowment_swf', 'sovereign_alm', 'overlay'] },
  { key: 'C4_agentic_ic', title: 'Agentic architecture & IC deliberation', streams: ['agentic_ai', 'paper_deepread', 'ic_deliberation'] },
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

const SYNTH_SCHEMA = {
  type: 'object',
  properties: {
    synthesis_path: { type: 'string' },
    word_count: { type: 'integer' },
    executive_summary: { type: 'string' },
    conceptual_leaps: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, disciplines: { type: 'string' }, mechanism: { type: 'string' }, implication: { type: 'string' } }, required: ['title', 'mechanism', 'implication'] } },
    component_recommendations: { type: 'array', items: { type: 'object', properties: { component: { type: 'string' }, recommended_approach: { type: 'string' }, alternatives: { type: 'string' }, key_parameters: { type: 'string' } }, required: ['component', 'recommended_approach'] } },
    agentic_principles: { type: 'array', items: { type: 'string' } },
    ic_module_design: { type: 'string' },
    data_requirements: { type: 'array', items: { type: 'string' } },
    open_questions: { type: 'array', items: { type: 'string' } },
    phased_build_plan: { type: 'array', items: { type: 'string' } },
  },
  required: ['synthesis_path', 'executive_summary', 'conceptual_leaps', 'component_recommendations', 'agentic_principles', 'phased_build_plan'],
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
2. Verify each against primary or high-quality sources (load tools via ToolSearch "select:WebSearch,WebFetch"; WebSearch mode "standard", or "extended" for recent/niche data). Verdict per claim: confirmed / corrected (give the corrected value and source) / refuted / unverifiable. Default to unverifiable if you cannot find support; do not give the benefit of the doubt.
3. Check that the 10 most important references exist with correct authors, year, title and venue (catch hallucinated or garbled citations).
4. Identify reasoning errors or overclaims in the dossier's design implications (e.g., a method that does not do what is claimed, a formula error, a mis-specified constraint).
5. Write your verification log in Markdown to ${verifyPath(s)} with: summary; a table of claims (claim | verdict | corrected value | source URL); citation-check results; reasoning issues; overall reliability rating.
Do NOT edit the dossier itself. Then return the structured output.`

const clusterPath = (c) => CLUSTER_DIR + '\\' + c.key + '.md'

const clusterPrompt = (c, results) => {
  const others = CLUSTERS.filter(x => x.key !== c.key).map(x => x.title).join('; ')
  const files = results.map(r => `- Stream ${r.stream.num} ${r.stream.title}\n  dossier: ${dossierPath(r.stream)}\n  verification log: ${r.verification ? verifyPath(r.stream) : '(verification failed - treat numbers with extra caution)'}`).join('\n')
  return `You are synthesizing one cluster of a 14-stream research program for ADIC's multi-period, robust, agentic portfolio framework.

${BRIEF}

CLUSTER: ${c.title}
Read the context file ${CONTEXT_FILE}, then read EVERY dossier and verification log below in full:
${files}

Produce an integrated cluster synthesis that:
1. Applies all verification corrections (never repeat a claim the verifier refuted or corrected without the correction; flag unverifiable numbers as such).
2. Reconciles disagreements between dossiers and gives a clear recommendation for every design question in this cluster.
3. Specifies concrete, implementable model formulations (equations, state/decision variables, parameters with default values and sources) for the components in this cluster, precise enough for an engineer to implement in Python.
4. Lists calibration targets (value, as-of date, source, confidence).
5. Identifies the strongest cross-disciplinary insights within the cluster and the links to the other clusters (${others}).
6. Notes open questions and the data ADIC must supply.
Write 6,000-10,000 words in Markdown to ${clusterPath(c)} using the Write tool. Then return the structured output.`
}

const masterPrompt = (clusters, streamResults) => {
  const cl = clusters.filter(Boolean).map(c => `- ${c.cluster}: ${c.path}\n  summary: ${c.summary}`).join('\n')
  const ds = streamResults.filter(Boolean).map(r => `- ${r.stream.num} ${r.stream.title}: ${dossierPath(r.stream)}${r.verification ? ' | verification: ' + verifyPath(r.stream) : ''}`).join('\n')
  return `You are the lead author of the integrated research report for ADIC's multi-period, robust, agentic portfolio decision framework.

${BRIEF}

Read the context file ${CONTEXT_FILE}, then the four cluster syntheses below in full, consulting individual dossiers and verification logs where you need more depth.
Cluster syntheses:
${cl}
Dossiers (and verification logs):
${ds}

Write the integrated report to ${SYNTH_FILE} (12,000-18,000 words, Markdown) with these sections:
0. Title, date (2026-10-18), scope.
1. Executive summary for the CIO and IC (at most 1,200 words): the problem, the core thesis, what the framework will do, the top 10 findings, and the recommended architecture in one diagram (mermaid or ASCII).
2. Problem framing: ADIC's balance sheet as a controlled stochastic system (state, decisions, exogenous information, transitions, objective - Powell's framework), using ADIC's numbers ($177bn, ~60% private mostly PE, 5-10% distributions, 10% target, leverage, overlay) and a first-order feasibility analysis (liquidity sources and uses under base and stress; explicit back-of-envelope with stated assumptions).
3. Cross-disciplinary conceptual leaps: 8-15 integrating ideas, each with origin disciplines, mechanism, why it matters for ADIC, how it enters the framework, and strength of evidence. Candidate themes to validate, refine or replace based on the research: the state-contingent shadow price of liquidity as the common currency linking sell/hold/refinance/lever, commitments, leverage and the overlay (bank FTP analogue); liability-side wrong-way risk (oil-fiscal draws co-moving with exit droughts) and hedge design for that joint state; tail hedges valued as contingent liquidity rather than standalone return; credibility-weighted fusion of underwritten/actual/forecast returns with incentive-aware bias correction; target-attainment pathologies (Browne) and why lexicographic / robust-satisficing objectives fix them; Powell's policy classes as the organizing principle for combining rules, MPC and policy search; the agentic-scientist loop applied to policy discovery with deterministic evaluators and rubric gates; entropy pooling as the IC's language for views; decision hygiene (Kahneman, Klein) applied to human+AI committees.
4. Component designs (one subsection each: recommended method, formulation, parameters, calibration, alternatives considered and why rejected): 4.1 scenario generator (including oil/fiscal factors and regimes); 4.2 private-markets cash-flow and NAV engine; 4.3 return-belief fusion; 4.4 action economics for sell/hold/refinance/lever (instruments: secondaries, NAV loans, preferred equity, continuation vehicles, CFO/Astrea-type structures); 4.5 leverage module; 4.6 overlay module (tail hedge, opportunistic strategy, collateral); 4.7 distribution policy / liability module; 4.8 optimization core (here-and-now scenario program with duals; policy evaluation / MPC; policy search); 4.9 objective and constraints (improving on the two-tier design); 4.10 robustness and stress testing (DRO, robust satisficing, reverse stress, model ensembles); 4.11 attribution and explanation (Shapley/ablation, shadow prices, counterfactuals).
5. Agentic architecture: principles, agent roles, tools, control loops modeled on The Agentic Scientist (stages, meta-controller, rubric gates), verification and provenance, governance (SR 11-7, NIST AI RMF), deployment considerations for a sovereign investor.
6. IC deliberation module: AI shadow-IC protocol, human-IC interaction (Q&A, view conditioning, decision capture), safeguards, evaluation.
7. Calibration and data: consolidated table of calibration targets (value, as-of, source, confidence) and the data ADIC must supply (schemas).
8. Validation plan for the framework itself (backtests, benchmarks, sensitivity, out-of-sample, model-risk management).
9. Risks, limitations, open questions.
10. Phased build plan (MVP -> production), including what can be built now on synthetic data.
11. Consolidated bibliography (deduplicated, with URLs).
Rules: apply all verification corrections; never introduce unsourced numbers (label assumptions as assumptions); be decisive - recommend, do not survey; write for a sophisticated quant audience while keeping the executive summary accessible. Use the Write tool (you may write the file in several chunks/edits if it is long). Then return the structured output.`
}

const REQUIREMENTS = `1) a multi-period optimization framework; 2) robust scenario analysis; 3) probabilities of outcomes; 4) the 5-10% annual distribution requirement; 5) the 10% return target; 6) leverage permitted (portfolio and asset level); 7) ~60% private (mostly PE) with declining DPI; 8) a SELL / HOLD / REFINANCE / LEVER lens for each strategy/asset; 9) fusion of underwritten, current actual and forecast returns; 10) the OTC derivatives overlay with a tail-protection hedge and an opportunistic trading strategy; 11) an agentic architecture inspired by The Agentic Scientist; 12) the IC's ability to discuss results; 13) building on the user's prior two-tier robust TPA deck.`

const criticPrompt = `You are a demanding completeness critic reviewing the integrated research report for ADIC's multi-period, robust, agentic portfolio framework.

${BRIEF}

Read the context file ${CONTEXT_FILE} and the report at ${SYNTH_FILE} in full; skim dossiers in ${DOSSIER_DIR} and verification logs in ${VERIFY_DIR} as needed.
Evaluate against the user's explicit requirements: ${REQUIREMENTS}
Also evaluate: buildability (is each component specified precisely enough to implement in Python now on synthetic data and later on ADIC data?), internal consistency (contradictions between sections), evidence quality (unsupported or stale numbers; ignored verification corrections), and whether the report genuinely integrates disciplines rather than surveying them.
Return at most 8 gaps, most severe first. Severity: high = a requirement is unaddressed or a component is not buildable; medium = thin or weakly evidenced; low = polish. Each gap must include a concrete research task that would close it.`

const gapPrompt = (g, i) => `Close a gap in the integrated research report for ADIC's multi-period, robust, agentic portfolio framework.

${BRIEF}

GAP: ${g.gap}
WHY IT MATTERS: ${g.why_it_matters || ''}
TASK: ${g.research_task}

Read the context file ${CONTEXT_FILE} and the report ${SYNTH_FILE} first (plus any relevant dossiers in ${DOSSIER_DIR}). Research as needed (load tools via ToolSearch "select:WebSearch,WebFetch"). Never fabricate citations or numbers. Write a focused addendum (1,500-4,000 words, with formulations, sourced and dated numbers, and design implications) to ${ADDENDA_DIR}\\gap_${String(i + 1).padStart(2, '0')}.md using the Write tool. Then return the structured output.`

const revisePrompt = (addenda, critic) => `Revise the integrated research report at ${SYNTH_FILE} for ADIC's multi-period, robust, agentic portfolio framework.

Integrate these addenda (read each in full):
${addenda.map(a => `- ${a.addendum_path}: ${a.summary}`).join('\n')}
Also resolve these contradictions flagged by the critic: ${JSON.stringify((critic && critic.contradictions) || [])}

Edit the report in place with the Edit tool: insert new material into the appropriate sections (not as an appendix dump), fix the inconsistencies, update the executive summary, conceptual leaps and build plan if conclusions changed, and keep everything else intact. Then return the structured output reflecting the revised report.`

// ---------------- orchestration ----------------
phase('Research')
log(`Launching ${STREAMS.length} research streams; each is fact-checked as soon as it lands.`)

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

const synth = await agent(masterPrompt(clusters, streamResults), { label: 'synth:master', phase: 'Master synthesis', schema: SYNTH_SCHEMA })
log('Master synthesis written: ' + (synth ? synth.synthesis_path : 'FAILED'))

let finalSynth = synth
let critic = null
let addenda = []
if (synth) {
  critic = await agent(criticPrompt, { label: 'critic', phase: 'Critique', schema: CRITIC_SCHEMA })
  if (critic && critic.gaps && critic.gaps.length) {
    const high = critic.gaps.filter(g => g.severity === 'high')
    const med = critic.gaps.filter(g => g.severity === 'medium')
    const toFill = high.concat(med).slice(0, 5)
    const skipped = critic.gaps.length - toFill.length
    log(`Critic found ${critic.gaps.length} gaps (${high.length} high, ${med.length} medium); filling ${toFill.length}${skipped > 0 ? `; ${skipped} lower-priority gaps recorded but not researched` : ''}`)
    if (toFill.length) {
      addenda = (await parallel(toFill.map((g, i) => () => agent(gapPrompt(g, i), { label: `gap:${i + 1}`, phase: 'Gap-fill', schema: GAP_SCHEMA })))).filter(Boolean)
      if (addenda.length) {
        const rev = await agent(revisePrompt(addenda, critic), { label: 'revise-synthesis', phase: 'Gap-fill', schema: SYNTH_SCHEMA })
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
    verification: r.verification ? { checked: r.verification.checked, confirmed: r.verification.confirmed, corrected: r.verification.corrected, refuted: r.verification.refuted, unverifiable: r.verification.unverifiable, reliability: r.verification.overall_reliability } : null,
  } : { stream: STREAMS[i].key, failed: true }),
  clusters: clusters.map((c, i) => c ? { cluster: c.cluster, path: c.path } : { cluster: CLUSTERS[i].key, failed: true }),
  synthesis: finalSynth,
  critic,
  addenda: addenda.map(a => ({ gap: a.gap, path: a.addendum_path, summary: a.summary })),
}
