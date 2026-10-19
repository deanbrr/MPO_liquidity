# Stream 04: Private-equity cash flows, NAV modelling and the DPI decline

*Research dossier for the ADIC multi-period robust Total Portfolio Approach (TPA) framework. Prepared 2026-10-18.*

**Evidence tags.** **[S]** is a sourced fact (citation in §10). **[P]** is practitioner consensus. **[I]** is this analyst's inference, proposed default or illustrative calculation.

**Units and definitions.** Amounts are in USD. "Distribution rate" means annualised period distributions divided by the prior-period NAV. "Contribution (call) rate" means annualised contributions divided by opening unfunded commitments plus newly raised capital. Both follow the MSCI definitions [S: MSCI Q2-2026, Notes & Calculations]. Data providers define these ratios differently, so every figure below names its source.

---

## 1. Executive summary

1. **The drought is the defining fact, and it is asymmetric [S].** In MSCI's global private-equity series, the distribution rate was 24/21/18/17% in 2017–2020 and 27% in 2021. It then fell to 11/9/11/11% in 2022–2025 and to **9% in H1 2026**, roughly half of the ~20% long-run norm. The contribution rate stayed at **27–31%** (39% in the 2021 boom). Net PE cash flow to LPs was −$127bn (2022), −$133bn (2023), −$52bn (2024), −$2bn (2025) and −$16.5bn (H1 2026). **Calls are sticky and distributions take the whole shock.** In the same series, 2025's $489bn of distributions was the second-highest dollar amount on record. The low rate comes from a NAV base that is far larger, not from small cheques.
2. **The constraint is exit scarcity, not exit pricing [S].** Top-quartile buyout exit multiples hit a series high of 18.2x EBITDA in H1 2026 (the series starts in 2016). The median held near 12.5x, against a median entry multiple of 11.3x. But about 32–33k unsold companies (about $3.8tn) sit in GP portfolios. Average holding periods are about 7 years. 52% of buyout-backed inventory has been held more than 4 years. Bain describes a 2026 "triple shock": an AI-driven software rerating, private-credit redemption stress, and an Iran-related energy spike. Q1-2026 marks on PE-held software fell about 8%.
3. **For ADIC the cash-flow swing is as large as the payout obligation [I].** I calibrated a toy programme to MSCI rates and to the Cambridge Associates DPI-by-age profile, scaled to $106bn NAV, about $27bn unfunded and about $11bn a year of commitments. Its net PE cash flow is about **+$10–12bn a year in a normal regime, about $0 in the drought, and about −$4.5bn in a crisis year**. Cumulative 2027–29 net flow is **+$47bn** in a V recovery, **+$34bn** in a U, **+$7.5bn** if the drought persists (L), and **+$5bn** in a crisis path. The sovereign payout over the same three years is **$27–53bn** (5–10% × $177bn × 3). The private book can therefore swing from funding most of the minimum payout to funding almost none of it.
4. **Recommended engine: a regime-switching, factor-driven, time-changed Takahashi–Alexander model (RFT-TA), run per asset or cohort.** It has six parts:
   - **Economic NAV:** a latent economic NAV with factor betas (BGG; Ang et al.).
   - **Reported NAV:** produced from economic NAV through a smoothing-and-lag filter.
   - **Calls:** a hazard on unfunded commitments.
   - **Distributions:** a hazard on economic NAV, driven by an *exit-window factor* and by regime multipliers.
   - **Effective-age clock:** a clock that slows in droughts to represent fund-life extensions. Without it, plain TA produces a mechanical catch-up as NAV ages; I show this artifact in §6.6.
   - **Inventory adverse selection:** the best assets leave first, so the residual inventory deteriorates.

   Each asset also carries explicit **SELL / HOLD / REFINANCE / LEVER operators**. SELL uses secondary pricing by strategy, age and regime. REFINANCE uses NAV loans with LTV caps and cash sweeps. LEVER covers commitments, secondary purchases and co-investment.
5. **Beliefs become drift.** A precision-weighted fusion (Bühlmann credibility, in the style of Bornhuetter–Ferguson) combines three inputs into a forward alpha: the *debiased underwritten* return, the *actual-to-date* return (PME or direct alpha on nowcast NAV), and the *group forecast*. The fused alpha is multiplied by an age-dependent "alpha runway", motivated by Bain's finding that fund IRR stagnates around year 7 and TVPI flattens after year 8.
6. **SELL decisions hinge on one comparison.** A sale makes sense when ADIC's **liquidity shadow price** exceeds the buyer's expected excess return. Historically buyers out-earn sellers by about 3–5pp a year in PME terms (Nadauld et al.). Current marks to sale are 91% of NAV for buyout, 79% for VC and 68% for real estate, and tail-end funds trade at discounts of 25% or more (Jefferies, H1-2026).
7. **What to tell the IC:** use a 9–12% distribution rate as the 2026–27 base case until the exit-window factor turns. Put explicit probabilities on the V, U, L, Crisis and "AI-bifurcation" scenarios. Report cash-flow-at-risk (CFaR) and the payout coverage ratio rather than a single pacing line.

---

## 2. Core concepts and theory

### 2.1 Anatomy of a closed-end commitment
For asset *i* (a fund interest, co-investment, continuation-vehicle stake or secondary position) on a quarterly grid (Δ = ¼ year), the state variables are:
- unfunded commitment $U$
- calls $C$
- distributions $D$
- latent **economic** NAV $V$
- **reported** NAV $N$

The accounting identities are:
$$V_{t+1}=V_t\,e^{r_{t+1}}+C_{t+1}-D_{t+1},\qquad U_{t+1}=U_t-C_{t+1}+Rc_{t+1}-Ex_{t+1}$$
Here $Rc$ is recallable distributions and $Ex$ is expired (never-called) commitment. The standard multiples are DPI $=\sum D/\sum C$, RVPI $=N/\sum C$ and TVPI $=$ DPI + RVPI.

### 2.2 Takahashi–Alexander, the Yale model [S]
Takahashi & Alexander (2002) give the deterministic baseline that most LP pacing models still use:
$$C_t = RC_t\,(CC-PIC_{t-1}),\quad D_t = RD_t\,NAV_{t-1}(1+G),\quad RD_t=\max\!\big(Y,(t/L)^B\big),\quad NAV_t=NAV_{t-1}(1+G)+C_t-D_t$$
- **Inputs:** the call-rate schedule $RC$, the commitment $CC$, the life $L$, the bow $B$, growth $G$ and yield $Y$.
- **Limitation:** the model produces one average path. It has no dispersion and no dependence on market state.

Luxenberg et al. (2022) rewrite it as a linear state-space system. The state is $(I_t,K_t)$ (illiquid NAV, uncalled commitment), with
$$K_{t+1}=K_t+n_t-C_t,\quad I_{t+1}=I_tR_t+C_t-D_t,\quad C_t=\lambda^0_t n_t+\lambda^1_t K_t,\quad D_t=\delta_t I_tR_t.$$
The intensities are stochastic and logit-normal: $\lambda^1=1/(1+e^{z_1})$ and $\delta=1/(1+e^{z_2})$. Returns are lognormal, $R=e^{z_3}$, and $z\sim N(\mu,\Sigma)$. Their annual example (in the arXiv preprint) uses mean $\lambda^1\approx0.26$, $\lambda^0\approx0.13$, $\delta\approx0.33$ and a 15.8% illiquid return (BlackRock buyout capital-market assumption, July 2021). That implies a steady-state NAV of about 3.7× the annual commitment. They then solve commitments by model predictive control (MPC) and track the "relaxed-liquid" frontier closely over 20 periods.

Jeet et al. (2026) replace the opaque bow $B$ with goal-based inputs: $d=\log M/(G\,L)$ and $B=e^{\pi d}/\sqrt2$, where $M$ is target TVPI, $G$ target IRR and $L$ fund life.

### 2.3 Continuous-time stochastic extensions [S]
Buchner, Kaserer & Wagner model the **drawdown rate** as a CIR process, $d\delta_t=\kappa(\theta-\delta_t)dt+\sigma\sqrt{\delta_t}\,dW_t$. Cumulative drawdowns follow $D^c_t=C\,(1-e^{-\int_0^t\delta_u du})$, so the uncalled balance decays exponentially. They motivate the process with a competition-for-deals argument.
- **2006 working paper:** distributions are lognormal at discrete dates, with serial correlation between consecutive cash flows, and fund value comes from equilibrium pricing.
- **Journal version (JAI, 2010):** estimates the model on fund data.
- **Related work:** BKW describe de Malherbe (2004) as modelling value dynamics with an explicit valuation-error term.

Neither family conditions on market state. RFT-TA (§6) puts that dependence back in.

### 2.4 Cash flows are cyclical [S]
Robinson & Sensoy (2016) use 837 funds from 1984–2010.
- **Direction:** calls and distributions are both procyclical. Distributions are more sensitive.
- **Elasticities:** in log-log Tobit regressions on ln(S&P P/D), buyout distributions have an elasticity of **0.37** and calls **0.33**. Because distributions are larger in levels, net cash flow is procyclical. Funds of a given age are liquidity *sinks* when valuations are low.
- **Credit spreads:** wider spreads reduce both calls and distributions, and distributions much more.
- **VC vs buyout:** VC is more procyclical.
- **Idiosyncratic share:** about **92%** of quarterly net-cash-flow variation is idiosyncratic once fund age and calendar time are controlled for.
- **Fund-age profile:** net cash flow turns positive at about age 3–4 and rises until about age 8.

Ljungqvist & Richardson (2003) report the investment pace:
- It takes **six years to invest 90% of commitments**, and the median fund takes four years to reach 80%.
- The average fund's IRR turns positive only in year 8.
- Funds ultimately invest about 95% of commitments (as cited by BKW).

**Two implications for ADIC [I].**
- Across hundreds of funds the idiosyncratic noise largely diversifies, so at portfolio level the *systematic* exit and financing state dominates. That remains true even though fund-level R² is low.
- The 2023–25 drought persisted while equity valuations were high. A P/D-only elasticity estimated on 1984–2010 data would have predicted *more* distributions. The exit factor must therefore load on financing conditions (rates, high-yield spreads, leveraged-loan issuance) and on the valuation gap of the inventory, not on equity valuations alone.

### 2.5 NAV smoothing and true risk [S]
- **Geltner (1991), the smoothing model:** $r^N_t=(1-\lambda)r^V_t+\lambda r^N_{t-1}$, which inverts to $r^V_t=(r^N_t-\lambda r^N_{t-1})/(1-\lambda)$. With i.i.d. true returns, $\mathrm{Var}(r^N)=\frac{1-\lambda}{1+\lambda}\mathrm{Var}(r^V)$; this ratio follows algebraically from the model. [unverified: attributed to the 1991 paper by its title, because neither Crossref nor OpenAlex indexes an abstract]
- **Geltner (1993), unsmoothing without assuming an efficient market:** recovers market-value returns from appraisal-based index returns "without presupposing or constraining the market value returns to be unpredictable or uncorrelated across time". It also corrects for temporal aggregation and the seasonality of reappraisals (abstract). It is the reference for unsmoothing when true returns may be serially correlated.
- **Getmansky, Lo & Makarov (2004):** reported returns are $\sum_j\theta_j r_{t-j}$ with $\sum\theta_j=1$, estimated by maximum likelihood.
- **Couts, Gonçalves & Rossi (2024):** funds with similar investments share a *common* smoothing component that fund-level unsmoothing does not remove. Their 3-step method raises measured systematic risk and lowers average alpha.
- **Brown, Ghysels & Gredil (BGG, 2023):** a weekly state-space model fitted to individual funds and estimated by Kalman filter and maximum likelihood. Its components are:
  - **Reported NAV:** an exponentially weighted average of past valuations, with weight $\lambda(1-w_t)$, where $w_t$ is the cash-flow share of assets ("first in, first out").
  - **Distributions:** $D_t=\delta(\cdot)V_t+\text{noise}$.
  - **Smoothing:** the median weekly $\lambda$ is 0.951 (working-paper figure), so about 77% of a NAV report reflects valuations at least five weeks old. That matches AR(2) coefficients of about (0.5, 0.3) on quarterly reported returns.
  - **Noise and betas:** NAV noise is 4.6% mean and 3.1% median (working-paper figures). Fund-level betas are 1.05–1.10 for buyout and 1.20–1.32 for VC in the working paper; the published abstract gives about 1.0 and 1.4.
  - **Total risk:** about **33%** a year for buyout and **38–40%** for VC, roughly 10–13pp above reported-NAV volatility. Ang et al. (2018)-style panel betas (about 1.25 buyout, 1.80 VC) are used as priors.
  - **Implied quarterly smoothing [I]:** $\lambda_q\approx0.951^{13}\approx0.52$.
- **A live example of the lag [S]:** in MSCI's Q2-2026 figures, ACWI IMI returned −2.7% in Q1 and +15.1% in Q2, while buyout returned −1.1% and +2.5%.

### 2.6 Performance, valuation and the cost of illiquidity [S]
- **Kaplan–Schoar PME:** distributions and NAV discounted at index returns, divided by calls discounted the same way.
- **GPME (Korteweg & Nagel 2016):** $\sum M_tCF_t$ with stochastic discount factor $M_t=\exp(a-b\,r^m_t)$. VC fund abnormal returns are close to zero, and their systematic payoffs resemble short index puts.
- **Direct alpha (Gredil, Griffiths & Stucke 2023):** compound cash flows to a common date at benchmark returns; the IRR of the result is the annualised excess return.
- **Strip valuation (Gupta & Van Nieuwerburgh 2021):** cash flows are replicated with dividend and capital-gain strips horizon by horizon. Average risk-adjusted profit is *negative* (working paper: −18c per $ for buyout, −11c VC, −17c real estate, −10c infrastructure). About a quarter of funds earn more than +10c, and expected returns decline over time.
- **Cash-flow-based risk and return:** Driessen, Lin & Phalippou (2012) and Ang et al. (2018).
- **Sorensen, Wang & Yang (2014):** the LP's break-even alpha is **3.08% a year** under a 2/20 fee structure, falling to 2.06% at a debt-to-equity ratio of 3. The cost of illiquidity is comparable to the cost of fees.
- **Nadauld et al. (2019, *JFE*):** buyers' annualised PME is 1.023 against sellers' 0.976 (the working paper has 0.974). That is about **5pp a year**; the working paper puts it at about 3pp for funds aged 4–9.

**Implication [I].** The NAV-drift alpha must be measured against a factor or strip benchmark. The default prior for net buyout alpha should be about 0 to +2%. The hurdle for HOLD and LEVER is not trivial.

### 2.7 LP portfolio choice with commitments [S]
- **Gourier, Phalippou & Westerfield (2024):** with ex-ante commitment, investors are under-allocated to PE. They would pay more to adjust the quantity committed than to remove timing uncertainty or limited tradability. Commitment risk premia *rise* with secondary-market liquidity and persist across many funds.
- **Giommetti & Sørensen (2021, working paper):** repeated TA-type commitments in a stock, bond and PE problem. Optimal PE allocation is non-monotone in risk aversion, and the paper adds a secondary-market extension.
- **Ang, Papanikolaou & Westerfield (2014):** continuous-time portfolio choice in which the illiquid asset can be traded only at Poisson-arriving liquidity events. This is the canonical treatment of illiquidity costs in dynamic allocation; the setup is as summarised by Luxenberg et al.
- **Dimmock, Wang & Yang (2024):** lock-ups plus proportional secondary costs produce endogenous rebalancing bands. "Liquidity diversification" through staggered lock-ups raises the optimal alternatives weight, and crisis states push holdings far from target.
- **Pacing and over-commitment:** Siegel (2008); Nevins et al. (2004); Hayes, Primbs & Chiquoine (2015, penalty-cost SAA).

---

## 3. Methods and models: trade-offs

| Class | Captures | Data needed | Strengths | Weaknesses | Role at ADIC |
|---|---|---|---|---|---|
| Deterministic TA | Average call, distribution and NAV path | 6 inputs per strategy | Transparent, IC-legible | No dispersion or regime; mechanical catch-up as NAV ages (§6.6) | Pacing baseline and sanity check |
| Stochastic TA (Luxenberg) | Random intensities, linear state-space | Fund cash flows | Fits MPC and convex optimisation directly | Time-homogeneous, i.i.d. shocks | Linearised dynamics for the optimiser |
| **RFT-TA (recommended)** | Regimes, exit factor, betas, smoothing, time change | Fund cash flows and NAVs, market factors | Scenario-ready, maps to IC narratives | More parameters; needs pooling | **Core engine** |
| BKW continuous-time | Stochastic drawdown and distribution rates | Fund cash flows | Analytical valuation | No market state; hard to extend | Benchmarking |
| Exit-hazard (survival) models | Company-level exits, competing risks (IPO, trade sale, sponsor-to-sponsor, CV, write-off) | Look-through holdings | Captures inventory, ageing and selection | Data heavy | Co-invests, directs, large positions |
| State-space nowcasting (BGG) | True NAV between reports, betas | Cash flows, NAVs, comparables | Principled filtering; uses secondary marks and M&A comps | Fails for heavy-tailed funds (~10% non-convergence in BGG) | Economic NAV input |
| Unsmoothing (Geltner 1991 inversion or Geltner 1993 procedure, GLM, CGR) | Volatility and beta correction | Return series | Simple | Needs long series | Calibration of the smoothing parameter λ |
| ML sequence models (Karatas et al.) | Nonlinear cash-flow dynamics with macro inputs | Large panels | Flexible | Opaque, overfits short regimes | Challenger model |
| Actuarial development triangles | Vintage × age development, with uncertainty | Cumulative cash flows | Mack and bootstrap errors; Bornhuetter–Ferguson blending | Assumes stable development | Distribution projection and its error bars |
| Strip valuation and GPME | Horizon-dependent discount rates, alpha | Long panels | Sound risk adjustment | Model-dependent | Alpha priors and hurdle rates |
| MPC and stochastic programming | Commitments, sales, NAV loans | Outputs of the above | Re-plans each period, yields shadow prices | Model-error sensitive | Decision layer (with the optimiser stream) |

**Ideas transferred from other disciplines [I, built on the sources shown].**
1. **Actuarial reserving.**
   - Treat distributions as claim development: a vintage × age triangle projected by chain-ladder, with Mack (1993) standard errors or an England–Verrall (2002) bootstrap for prediction intervals.
   - Use Bornhuetter–Ferguson to blend the *prior* (underwritten) with *emerging* experience (actuals). Bühlmann (1967) credibility $Z=n/(n+k)$ supplies the weights (§6.3, E3).
   - Fit lumpy, zero-inflated cash flows with a Tweedie compound Poisson–gamma GLM, or a hurdle model.
2. **Bank ALM.**
   - Unfunded commitments resemble undrawn committed facilities. Basel LCR40.64 sets 30-day stress drawdown rates of 5% for retail, 10% (credit) or 30% (liquidity facilities) for non-financial corporates, 40% for banks, 40% or 100% for other financial institutions, and 100% for SPEs [S].
   - PE calls behave differently: they *fall* in stress (Robinson & Sensoy). The transferable part is the *behavioural run-off* method, applied to both legs: a distribution run-off (the deposit-outflow analogue) plus a call add-on for follow-ons and subscription-line clean-ups.
3. **Queueing and inventory.** Little's law gives residence time $W=L/\lambda$. US PE-backed inventory was 13,509 companies at Q2-2026, against roughly 1.5k exits a year annualised (353 in Q2) [S: PitchBook via Cherry Bekaert]. At current throughput that implies about **9 years** of average residence, against a 5.5-year median hold at exit. That gap is a direct measure of the backlog.
4. **Stochastic time change (operational time).** A fund's life clock slows in droughts. This is the effective-age clock, E4.
5. **Adverse selection (Akerlof).** The best assets exit first, so remaining NAV quality drifts down. Tail-end funds price at discounts of 25% or more [S: Jefferies].
6. **Real options.** SELL is an American put on NAV with a stochastic strike $(1-d_t)N_t$. Waiting has value when discounts mean-revert, so solve it with least-squares Monte Carlo (Longstaff–Schwartz).

---

## 4. Empirical evidence and current market data (as of 2026-10-18)

### 4.1 Global PE cash flows, MSCI (published October 2026) [S]

| Year | Contributions ($bn) | Distributions ($bn) | Net ($bn) | D/C ratio | Contribution rate | Distribution rate |
|---|---|---|---|---|---|---|
| 2017 | 261 | 319 | +58 | 1.2 | 31% | 24% |
| 2018 | 295 | 312 | +17 | 1.1 | 30% | 21% |
| 2019 | 325 | 309 | −16 | 1.0 | 28% | 18% |
| 2020 | 387 | 338 | −49 | 0.9 | 29% | 17% |
| 2021 | 677 | 715 | +38 | 1.1 | 39% | 27% |
| 2022 | 530 | 402 | −127 | 0.8 | 31% | 11% |
| 2023 | 457 | 324 | −133 | 0.7 | 27% | 9% |
| 2024 | 487 | 435 | −52 | 0.9 | 28% | 11% |
| 2025 | 491 | 489 | −2 | 1.0 | 29% | 11% |
| H1 2026 | 228 | 211 | −16.5 | 0.9 | 31% | 9% |

- **Q2 2026 alone:** +$4.7bn, with a D/C ratio of 1.04. MSCI attributes the H1 balance to restrained calls rather than a genuine pickup in distributions.
- **All private capital:** net flow was +$12.0bn in 2025 and +$22.9bn in H1 2026, after a −$101.1bn shortfall in 2024.
- **Revisions:** MSCI's May 2026 deck (data to Q4-2025) put PE distribution rates 1–4pp higher for the same years: 27% against 24% for 2017, 29% against 27% for 2021, and 10–12% against 9–11% for 2022–2025. Revisions of this size are a modelling risk in their own right.
- **Inconsistent benchmark:** MSCI calls H1-2026's 9% "roughly a third of the historical norm" for PE, while citing a historical average of about 20% for all private capital.
- **Other providers:**
  - Bain cites about 14% for 2025 (MSCI data, 12 months to Q3-2025) and says the rate has been below 15% for four years, an industry record.
  - PitchBook shows a US distribution yield of 14.8% against a 23.4% long-run average (as of 30 June 2026).
  - McKinsey shows distributions at **6%** of PE AUM in the 12 months to June 2025, against a 2015–19 average of 16%. AUM includes dry powder, so this is a different denominator. Five-year rolling DPI as a share of AUM hit a record low of about 10%.

### 4.2 DPI by vintage [S unless tagged]
- **Pre-drought baseline:** Cambridge Associates US PE pooled figures as of 31 Dec 2019.
  - Ages about 4–6: vintage 2016 DPI 0.11; 2015 0.19; 2014 0.36 (RVPI 1.09).
  - Ages about 7–9: 2013 0.43; 2012 0.64 (RVPI 0.93); 2011 0.94.
  - Ages about 10–11: 2010 1.27 (TVPI 1.75); 2009 1.45.
  - Note from the same report: most funds take at least six years to settle into their final quartile.
- **Current drought:**
  - Bain reports that 2017–2021 vintages have underdelivered DPI against the historical benchmark "for every vintage" (MSCI data, Q3-2025).
  - VC medians: about 0.31x for the 2017 vintage and 0.15x for 2018, per Carta Q1-2026 as aggregated by a secondary source. Carta's Q4-2025 report, as summarised in search results because the page blocked direct access, shows only just over half of 2020-vintage VC funds with any DPI.
  - Infrastructure: five-year DPI fell from a median of about 40% in the mid-2010s to about 13% (McKinsey 2026).
- **Illustration [I]:** the calibrated TA in §6.6 puts end-2026 DPI at 0.40 for the 2018 vintage under the drought, against 1.04 without it. For the 2015 vintage the figures are 1.10 against 1.55. RVPI is correspondingly inflated, which feeds the denominator effect.

### 4.3 Exits, holding periods and inventory [S]
- **Exits:**
  - 2025 buyout exit value was $717bn (+47%) on 1,570 exits (−2%). Seven exits above $10bn made up 22% of the value, and continuation vehicles were less than 10% of exit value (Bain).
  - McKinsey's broader definition gives $1.3tn of PE-backed exit value in 2025 (+41%).
  - US Q2-2026 exits were $102.6bn (−46% QoQ, −7% YoY) across 353 exits, and US exit value year-to-date was about 12% behind H1-2025 (PitchBook).
- **Holding periods:**
  - About 7 years for buyouts, against 5–6 years in 2010–2021. Nearly 40% of companies have been held more than 5 years, against 29% in 2019 (Bain).
  - More than 16,000 companies (52% of buyout-backed inventory) have been held more than 4 years, a record (McKinsey).
  - The US median hold at exit is 5.5 years, and the median for still-held companies is 4.2 years and rising (PitchBook).
- **Inventory:** about 32,000 unsold companies worth about $3.8tn (Bain 2026), and about 33,000 by June 2026 (Bain midyear).
- **Value creation:** IRR stagnates around year 7, and median TVPI flattens after year 8 (2000–2015 vintages).
- **Entry economics:** for the same 2.5x return, a deal that once needed about 5% annual EBITDA growth now needs 10–12% ("12 is the new 5").
- **Software:** the largest buyout subsector. Its entry multiples have run 5–7 turns above the buyout median since 2020, peaking near 19x, and its median exit multiple fell to 16.6x in 2025. Loss ratios on exited software deals are rising (MSCI, May 2026).

### 4.4 The IPO window in 2025–2026 [S]
- **2025:** PE-backed IPO activity rose 36% from a small base. Medline ($7.2bn, December 2025) was the largest PE-backed IPO ever (Bain).
- **Q2 2026:** US PE-backed IPOs raised $27.6bn across 12 deals, 30.5% of exit value. The median IPO size was $2.8bn (PitchBook).
- **Pipeline:** MSCI (October 2026) refers to blockbuster IPOs such as SpaceX and to OpenAI and Anthropic filing for public debuts.
- **A listing is not liquidity:** across 2,617 IPO exits, one in four positions returned close to nothing in the two years after listing (MSCI). Model IPO exits as staged, partly in-kind distributions.

### 4.5 Secondaries, continuation vehicles and NAV lending [S]
- **Jefferies, H1-2026 volume:** a record $118bn, against a full-year 2025 record of $240bn and a 2026 forecast of about $260bn. LP-led deals were 47% and GP-led 53%.
- **Jefferies, H1-2026 pricing (% of NAV):** LP portfolios averaged 87%. Buyout 91%, VC 79%, infrastructure 91%, credit 89% and real estate 68%.
  - Funds under 5 years old trade at single-digit discounts. Tail-end funds (10+ years) trade at discounts of 25% or more.
  - North America and Europe price at 86–88%.
  - About 33% of LP sales were structured, with deferrals in 26%.
  - Pensions and sovereign wealth funds supplied 48% of LP volume.
- **Continuation vehicles:** CV flows equalled 20% of distributions from mature PE funds in 2021–Q3 2025, against 6% in 2016–2020 (MSCI).
- **NAV loans:** loan-to-value of 5–30%, with buyout funds about 63% of the market (PitchBook via Cherry Bekaert). Margins are converging on 4–7%; most facilities so far have funded follow-ons, with early signs of DPI-motivated deals (Rede, June 2026).

### 4.6 The 2026 shocks and LP behaviour [S]
- **Shocks:** the Bain midyear "triple shock" (software rerating, private-credit redemptions, energy). Tech deal value fell 70% from Q4-2025 to Q1-2026. Software marks fell about 8% in Q1-2026: 8.9% in the US and 4.2% in Europe.
- **Exits versus marks:** about 75% of buyout assets still exit above their next-to-last mark. In an ILPA poll, most LPs said they lose confidence in a GP when a full exit comes in more than 5% below the last mark.
- **LP constraints and preferences:**
  - 53% of LPs say undrawn commitments limit new commitments, 15pp higher than at end-2024.
  - About two-thirds prefer to hold out for a higher MOIC rather than take near-term liquidity.
  - About one in five are cutting buyout allocations.
- **Credit stress:** private-credit semi-liquid redemption requests reached about 15% in a single quarter at non-traded BDCs (PitchBook via Cherry Bekaert).

---

## 5. Practitioner and peer practice; case studies

- **The TA model is the de facto pacing standard [P].** It is typically run with a base path and ad hoc stress paths. Dispersion and market dependence are usually missing, which is why RFT-TA is needed.
- **Public pension case: Cliffwater pacing plan for Rhode Island ERSRI (December 2023) [S].** The plan projects each legacy fund from its actual data and new commitments from industry curves. Its scenarios include:
  - base commitments
  - **no new commitments**
  - a **market-shock / denominator case**, in which plan assets fall from $10.9bn to $9.8bn and PE's share jumps from 16% to about 18% against a 12.5% target
  - slower (2%) plan growth

  It tracks an **over-commitment metric**: (unfunded + fair value) ÷ target allocation, between 1.5x and 1.9x. ADIC should adopt this metric, computed on both reported and economic NAV.
- **Data platforms [S].** MSCI (Burgiss) covers more than 15,000 closed-end funds. Hamilton Lane's Cobalt database covers more than 69,000 funds. Jefferies publishes semi-annual secondary pricing. These are the natural calibration feeds.
- **The 2022–26 drought response playbook [S].**
  - LP secondary sales, increasingly structured.
  - Elections on GP-led continuation vehicles.
  - NAV loans, first at GP level and now spreading to DPI-motivated deals.
  - Reduced re-ups (53% of LPs constrained).
- **The prior deck's own memo-corpus blind spot.** Distribution timing was repeatedly too optimistic after spread shocks and exit-window closures. The engine must therefore *structurally* encode slower distributions after financing shocks, not leave them to analyst judgment.

---

## 6. Design implications for the ADIC framework

### 6.1 Engine architecture
```
Market & regime layer ──► Exit-window factor X_t, regime S_t (HSMM), factor returns
          │
Asset/cohort layer (RFT-TA) ──► V (economic NAV), N (reported), U, C, D, a_eff, quality q
          │                         ▲
Belief fusion (E3) ─────────────────┘ (α̂_i, runway g)
          │
Action operators: SELL / HOLD / REFINANCE / LEVER  ◄── liquidity shadow prices π_t (optimiser)
          │
Outputs: cash-flow paths, CFaR, payout coverage, DPI paths, denominator metrics, IC tables
```
The engine runs at the **cohort** level (strategy × vintage × region × sector bucket, about 300–500 cohorts) for the 50k-path portfolio Monte Carlo. It runs at the **asset** level, on 5–10k common-random-number paths, for the per-asset SELL / HOLD / REFINANCE / LEVER analysis.

### 6.2 State variables
| Symbol | Meaning | Level |
|---|---|---|
| $S_t\in\{B,N,D,C\}$, duration $d_t$ | Regime (open window, normal, drought, crisis) and time spent in it | Global |
| $X_t$ | Exit-window factor (standardised) | Global |
| $f_t$ | Market factors: equity excess return, credit spread change, rates, sector (software or AI) | Global |
| $V_{i,t},N_{i,t},U_{i,t}$ | Economic NAV, reported NAV, unfunded | Asset |
| $a_{i,t}, a^e_{i,t}$ | Calendar age and effective age | Asset |
| $q_{i,t}$ | Inventory quality index (residual NAV quality) | Asset/cohort |
| $G_{i,t}=\ln N-\ln V$ | Mark gap | Asset |
| $B_{i,t}$ | NAV-loan balance | Asset/portfolio |
| $\hat\alpha_{i,t},\ s_{i,t}$ | Posterior forward alpha and its uncertainty | Asset |

### 6.3 Equations

**E1. Regime and exit factor.** $S_t$ is a hidden semi-Markov chain, so duration dependence captures "drought fatigue". The exit factor follows
$$X_{t+1}=\phi_XX_t+b'\Delta z_{t+1}+\sigma_X\eta_{t+1}.$$
The inputs $z$ are PE-backed IPO volume, sponsor and strategic M&A volume, high-yield OAS, leveraged-loan issuance, base rates, secondary buyout pricing and an inventory valuation gap (entry multiple of the inventory against the prevailing exit multiple). Estimate it as a dynamic factor model by Kalman filter. Its posterior feeds the existing state and fragility engine.

**E2. Economic NAV.**
$$r_{i,t+1}=\big[r_f+\beta_i\,\mathrm{ERP}_t+\hat\alpha_{i,t}\,g(a^e_{i,t})-f_i-\tfrac12\sigma_i^2\big]\Delta+\beta_i\varepsilon^m_{t+1}+\gamma_i\Delta cs_{t+1}+\omega_i'\varepsilon^{sec}_{t+1}+\sigma^{id}_i\sqrt\Delta\,\varepsilon_{i,t+1}+J_{i,t+1}$$
- $J$ is a regime-dependent jump for write-downs, with higher intensity in $C$.
- Fees $f_i$ follow the LPA. Sorensen, Wang & Yang give typical terms of 1.5–2% management fee and 20% carry [S].
- For a cohort aggregate, scale idiosyncratic variance by $1/N_{\text{eff}}$, where $N_{\text{eff}}=1/\sum w_j^2$.

**E3. Fusing underwritten, actual and forecast returns into drift.** Treat the three return measures as noisy, biased signals of the forward net alpha $\alpha_i$, measured against a beta- or strip-adjusted benchmark:
$$y^U_i=\alpha_i+b_U+e^U,\quad y^A_i=\alpha_i+b_A(a)+e^A,\quad y^F_i=\alpha_i+b_F+e^F$$
- **Variances:** $\mathrm{Var}(e^A)=\tau_A^2/(a^e_i\,\rho_i)$, where $\rho_i$ is the realisation ratio DPI/TVPI. The forecast and underwriting errors are correlated, $\mathrm{corr}(e^U,e^F)=\rho_{UF}$, because group forecasts anchor on underwriting.
- **Prior:** $\alpha_i\sim N(\alpha_s,\tau_0^2)$.
- **Posterior:** generalised least squares, $\hat\alpha_i=(\tau_0^{-2}+\mathbf1'\Sigma_e^{-1}\mathbf1)^{-1}(\tau_0^{-2}\alpha_s+\mathbf1'\Sigma_e^{-1}(y-b))$.
- **Credibility form (Bornhuetter–Ferguson analogue):** $\hat\alpha_i\approx Z\,y^A_{adj}+(1-Z)[w\,y^F_{adj}+(1-w)\,y^U_{adj}]$ with $Z=a^e/(a^e+k_s)$.
- **Calibrating the biases** $b_U$ and $b_F$: regress realised outcomes on underwriting and forecasts across ADIC's exited deals. The memo corpus suggests a material optimism bias in timing.
- **Alpha runway [I]:** $g(a^e)=1$ for $a^e\le6$, declining linearly to 0 at $a^e=10$. Beyond that, apply an ageing drag of $\psi\approx1$–2% a year. This is motivated by Bain's IRR-stagnation and TVPI-flattening evidence [S].
- **Cash-flow forecasts:** when the group forecasts cash flows rather than an IRR, solve $\sum_\tau CF^F_\tau(1+\mu^F_i)^{-(\tau-t)}=V_{i,t}$ for the implied forward IRR on *economic* NAV.

**E4. Effective-age clock (time change) [I].**
$$a^e_{i,t+1}=a^e_{i,t}+\kappa(S_t)\,\Delta,\quad \kappa(B)=1.2,\ \kappa(N)=1,\ \kappa(D)=0.6,\ \kappa(C)=0.5$$
- The distribution schedule is evaluated at $a^e$, not at calendar age. This represents fund-life extensions.
- It also prevents the TA artifact in which a drought ages NAV and raises distribution rates mechanically (§6.6).
- Legal term-extension events are triggered when calendar age exceeds the LPA term.

**E5. Calls.**
$$C_{i,t+1}=(1-e^{-\lambda_{i,t}\Delta})\,U_{i,t},\quad \lambda_{i,t}=\bar\lambda_s(a_{i,t})\,m^C(S_t)\,e^{\kappa^C_s z^{PD}_t+u^C_i}$$
- Calls at closing are $\lambda^0_s n_{s,t}$.
- After the investment period, residual unfunded commitment expires at rate $\xi_s$.
- Recallable distributions return to $U$.
- **Stress add-on (the bank-ALM analogue):** in $C$, add a follow-on and subscription-line clean-up call of $c^{stress}_s U$.

**E6. Distributions.**
$$D_{i,t+1}=(1-e^{-\delta_{i,t}\Delta})\,V_{i,t}e^{r_{i,t+1}}\,\zeta_{i,t+1},\qquad \delta_{i,t}=\bar\delta_s(a^e_{i,t})\,m^D(S_t)\,e^{\kappa^D_sX_t+\varsigma_s(q_{i,t})+u^D_i}$$
- **Schedule:** $\bar\delta_s(a)=-\ln[1-\max(Y_s,(a/L_s)^{B_s})]$, the TA bow written as an intensity.
- **Lumpiness:** $\zeta$ is a zero-inflated multiplicative noise with mean 1 (hurdle-lognormal or Tweedie).
- **IPO exits:** split into staged and in-kind tranches over 4–8 quarters, with public-equity beta during the sell-down.
- **CV events:** an elective payout. The LP takes cash at the CV price or rolls; the probability of cash election rises with the liquidity shadow price $\pi_t$.
- **Exit selection [I]:** exits draw from the top of the quality distribution, so $q$ drifts down in droughts: $\Delta q_{i}= -\chi\,(D_i/V_i)$.

**E7. Reported NAV and mark gap.**
$$r^N_{i,t}=(1-\lambda_s)\,r_{i,t-\ell}+\lambda_s\,r^N_{i,t-1}+\eta_{i,t},\qquad N_{i,t}=N_{i,t-1}e^{r^N_{i,t}}+C_{i,t}-D_{i,t}$$
- Defaults are $\lambda_q\approx0.5$ and a one-quarter lag $\ell=1$. The 0.5 is this stream's conversion of BGG's weekly λ ($0.951^{13}\approx0.52$, §2.5 [I]), not a figure BGG report.
- **Exit proceeds** are set relative to the prior marks: $\ln(P/N_{t-2})\sim N(\mu_e(S),\sigma_e)$, calibrated so that P(proceeds > next-to-last quarterly mark) ≈ 0.75 for buyout [S: Bain midyear 2026, citing MSCI]. Fit σ_e to ADIC's own realised exits.
- **Tail-end overstatement:** for aged residual inventory, allow $\mu_e<0$. MSCI notes that many 2015–2022/23 vintage marks likely exceed realistic clearing prices.

**E8. Liquidity metrics.**
- Net private cash flow: $\mathrm{NCF}_{t:t+H}=\sum(D-C)+\text{secondary proceeds}+\text{NAV-loan draws}-\text{debt service}$.
- Cash-flow-at-risk: $\mathrm{CFaR}_q(H)=-Q_q(\mathrm{NCF}_{t:t+H})$.
- **Payout coverage ratio:** $PCR_t=(\text{haircut liquid assets}+\mathrm{E}_{q}[\mathrm{NCF}])/(\text{sovereign payout}+P99\ \text{overlay margin})$. This extends the prior deck's liquidity coverage ratio.

**E9. Action operators.**

*SELL.* The sale price is
$$P_{i,t}=N_{i,t-\ell}\big(1-d_{i,t}\big),\quad d_{i,t}=\bar d_s(S_t)+d_{age}\mathbb 1\{a>10\}+d_{q}(1-q_{i,t})+d_{geo}+\epsilon$$
- H1-2026 anchors for $\bar d$: buyout 9%, VC 21%, credit 11%, infrastructure 9%, real estate 32%. Funds under 5 years old trade at single-digit discounts; tail-end funds at 25% or more [S].
- **Deferred consideration:** a fraction $\phi$ paid at T+12 months adds an effective discount of $\phi\,(1-(1+r_{def})^{-1})$.
- **Decision rule:** sell when
$$P_{i,t}(1+\pi_t)>\mathbb E_t\Big[\sum_\tau M_{t,\tau}(1+\pi_\tau)(D_{i,\tau}-C_{i,\tau})\Big].$$
  Equivalently, sell when the buyer's implied IRR is below ADIC's hurdle $h_t=r^{opp}+\pi_t$. Typical buyer excess return is about 3–5pp a year (Nadauld et al.) [S].

*REFINANCE.* A NAV-loan draw satisfies $B_{i,t}\le \mathrm{LTV}^{max}(S_t)N_{i,t}$.
- **Terms:** the LTV ceiling is 5–30% [S], tightening in drought and crisis [I]. The cost is base rate plus a margin $m\in[4\%,7\%]$ [S].
- **Covenant:** if LTV exceeds the covenant, distributions are swept to repay the loan.
- **Equity volatility:** levered equity volatility is about $\sigma_V/(1-\mathrm{LTV})$.
- **Value test:** the loan adds value if $\pi_t > (r_b+m) - \mathbb E[\text{collateral excess return}]$, after charging for sweep and covenant risk in crisis paths.

*LEVER.* There are three routes. Each is accepted only if the marginal $\hat\alpha$, net of financing and the liquidity shadow price, is positive under the Tier-1 robust gate.
- new commitments $n_{s,t}$, which drive the pacing
- secondary purchases at discount $d$, which capture the buyer's 3–5pp
- co-investment (low fees, high idiosyncratic risk)

*HOLD* is the baseline path.

**E10. Optimiser coupling (for the multi-period stream).**
- **Linearised dynamics:** per cohort, in the Luxenberg A/B form, with scenario-based chance constraints:
  - $P(\text{liquid}_t<\text{floor})\le\varepsilon$
  - $N_t/W_t\le w^{max}$, on both reported and economic NAV
  - $(U_t+N_t)/(w^*W_t)\le k^{max}$
  - NAV-loan LTV limits
- **Objective terms:** target-attainment probability or terminal wealth, minus discount costs, loan interest, a CFaR penalty and liquidity-shortfall penalties.
- **Shadow prices:** the dual on the liquidity constraint, $\pi_t$, feeds the asset-level operators in E9.

### 6.4 Default parameters by strategy (annualised; [I] unless tagged)
| Parameter | Buyout | Growth | VC | Private credit | Real estate (VA/opp.) | Infrastructure | Secondary funds | Co-invest |
|---|---|---|---|---|---|---|---|---|
| Call schedule on remaining unfunded, years 1–5 | 20/25/30/35/40% (reproduces ~90% called by yr 6 [S: LR]) | 20/25/30/35/40% | 15/20/25/30/35% | 35/45/50/50% | 25/30/35/40% | 20/25/30/35% | 50/40/40% | ~100% at close |
| Never-called share | ~5% [S: LR via BKW] | 5% | 8% | 5% | 5% | 5% | 3% | 0 |
| Bow (normal): L, B, Y | **16, 2.0, 0** (fitted to CA DPI and RVPI by age, §6.6) | 15, 2.0, 0 | 18, 2.5, 0 | 6, 1.0, 8% | 12, 2.0, 3% | 15, 1.5, 4% | 8, 1.5, 0 | Exit hazard; median hold ~5.5y [S] |
| Growth G (normal, net) | 11% (fit) | 11% | 12% | 8% | 7% | 8% | 10% | 12% |
| Economic beta | 1.05–1.25 [S: BGG, ACGP] | 1.2 | 1.2–1.8 [S] | 0.3–0.5 | 0.77 [S: ACGP prior in BGG] | 0.5–0.7 | 1.0 | 1.2–1.5 |
| Fund-level total volatility | 33% [S] | 35% | 38–40% [S] | 8–12% | 15–20% | 12–15% | 15–20% | 40–60% |
| Quarterly smoothing λ_q / lag | 0.5 / 1q [S-derived] | 0.55 / 1q | 0.6 / 1–2q | 0.3 / 1q | 0.65 / 1q | 0.6 / 1q | 0.5 / 1–2q | 0.5 / 1q |
| Distribution elasticity | 0.37 per ln(P/D) [S: RS]; load on X | ~1.2× buyout | >buyout [S: RS] | low | medium | low–medium | medium | high |
| Secondary price, H1 2026 | 91% [S] | n/a | 79% [S] | 89% [S] | 68% [S] | 91% [S] | n/a | Single-asset CV comparables |

### 6.5 Regime table (multipliers relative to normal; [I], anchored on [S] where noted)
| Regime | Empirical anchor | m^D | m^C | κ (age speed) | Secondary buyout price | LTV^max | NAV drift |
|---|---|---|---|---|---|---|---|
| B: open window | 2021: distribution rate 27%, calls 39% [S] | 1.25 | 1.3 | 1.2 | ~94% (Jefferies H1-2025, via search summary) | 30% | + |
| N: normal | 2017–20: 17–24%, calls 28–31% [S] | 1.0 | 1.0 | 1.0 | ~90–92% | 25% | 0 |
| D: drought | 2022–H1 2026: 9–11%, calls 27–31% [S] | 0.45–0.5 | 0.95–1.0 | 0.6 | 87–91% [S] | 20% | slight − |
| C: crisis | No MSCI analogue; assumption | 0.3–0.35 | 0.8 (plus stress calls) | 0.5 | 60–75% (assumption) | 10% | −15 to −25% mark, lagged |

**Default quarterly transition matrix** (rows and columns ordered B, N, D, C; to be re-estimated as an HSMM): B (0.85, 0.12, 0.02, 0.01); N (0.04, 0.88, 0.06, 0.02); D (0.03, 0.06, 0.88, 0.03); C (0.02, 0.08, 0.15, 0.75). The current drought is 18 quarters old, longer than a homogeneous chain with $p_{DD}=0.88$ makes plausible (probability about 0.11). That argues for duration-dependent hazards, and for IC-elicited priors on the probability of exiting D.

### 6.6 Representing the drought: calibration and scenarios [I]
- **Fit.** Deterministic TA with the call schedule in §6.4, expiry after year 8, L = 16, B = 2.0 and G = 11% reproduces the Cambridge Associates profile. The model gives age 6 DPI 0.32 against CA's 0.36, age 8 DPI 0.76 against 0.64, and age 10 DPI 1.27 and RVPI 0.43 against 1.27 and 0.48. Calls reach 90% by year 6, in line with LR. The fitted programme gives a 24% distribution rate and a 28% call rate. Both are consistent with MSCI 2017–20 (distributions 17–24%, contributions 28–31%), with the distribution rate at the top of the range.
- **The artifact.** If the drought is represented only as a rate multiplier, ageing NAV mechanically pushes distribution rates back up. Recoveries then overshoot: a +35% multiplier produced a 43% rate. The effective-age clock (κ_D = 0.6), combined with $m^D\approx0.5$ for 2022–26, reproduces the observed ~10–11% rates without that overshoot.
- **Scenario results.** The toy programme below assumes constant commitments of $11.2bn a year, end-2025 NAV of $106bn and unfunded of $27bn.

| Scenario 2027–29 | Specification | Average distribution rate 2027–29 | Worst annual net CF | Cumulative net CF | NAV end-2029 |
|---|---|---|---|---|---|
| V: window reopens | m^D 1.1, κ 1.3 in 2027–28 | 24% | +$15bn | **+$47bn** | $103bn |
| U: gradual | m^D 0.75 then 0.9; κ 0.8, 1.0, 1.1 | 19% | +$7.5bn | **+$34bn** | $114bn |
| L: drought persists | m^D 0.5; κ 0.6 to 2029 | 11% | +$1.4bn | **+$7.5bn** | $133bn (denominator pressure) |
| Crisis 2027 | m^D 0.35, G −20%, then recovery | 13% | **−$4.5bn** | **+$5bn** | $98bn |

The model reproduces the observed 2025 and 2026 rates: 11.3% and 9.8%, against MSCI's 11% and 9%.

- **Two more scenarios for IC discussion:**
  - **AI-bifurcation:** marks on software-heavy buyouts fall 15–25%, while AI-linked VC and growth NAV rises; VC returned +12.7% in Q2-2026 [S]. Distributions concentrate in IPO-staged VC and growth, and the buyout drought persists.
  - **Structural-shift sensitivity:** scale $\bar\delta$ by Φ between 0.75 and 1.0. This covers the possibility that higher rates, "12 is the new 5" and CV substitution make part of the drought permanent.
- **Starting probabilities for the IC to override:** V 20%, U 40%, L 25%, Crisis 15%. Reweight the Monte Carlo paths to the IC's probabilities by entropy pooling (minimum relative entropy) rather than re-simulating.

### 6.7 Calibration procedure and targets
1. **Simulated method of moments.** Fit cohort parameters to:
   - MSCI annual and quarterly distribution and contribution rates, and D/C ratios (2016–2026)
   - the CA DPI and RVPI-by-age curves
   - LR call speed
   - RS elasticities and the idiosyncratic share
   - BGG beta, volatility and smoothing
   - Jefferies discounts by strategy, age and region
   - P(buyout exit > next-to-last quarterly mark) ≈ 0.75
   - the CV share of mature-fund distributions (20%)
   - the IPO-to-cash lag
2. **Bayesian hierarchical pooling.** Pool across strategy → manager → fund, in the spirit of BGG's peer-imputed parameters, so that young or opaque funds borrow strength.
3. **Regime model.** Fit an HSMM on the MSCI quarterly series combined with exit-factor observables. Validate it against 2008–09 and 2022–26 using ADIC's own history.
4. **Backtest.** Compare out-of-sample 4–8 quarter cash-flow forecasts with realised cash flows (BGG-style), reporting coverage of the 80% and 95% intervals.

### 6.8 Data needs at ADIC
- **Cash flows:** quarterly (ideally daily) fund cash flows and NAVs for every interest, including recallables, fees and carry.
- **Look-through:** holdings with sector, entry multiple, leverage and software or AI tags.
- **Deal history:** underwriting memos (IRR, MOIC, hold and exit assumptions) and the strategy groups' forecast history, both needed to calibrate the biases b_U and b_F.
- **Market evidence:** secondary bids received and executed, CV election history, and NAV-loan term sheets.
- **Liabilities:** the sovereign payout calendar.

**External feeds:** MSCI/Burgiss and Jefferies or Evercore pricing. If affordable, add IPO and M&A pipelines and leveraged-finance data for the exit factor X.

### 6.9 Interfaces with other streams
- **Multi-period optimiser:** consumes the cash-flow, NAV and action-operator tensors and returns the shadow prices π_t.
- **State engine:** supplies the S_t posterior; this stream contributes X_t.
- **Belief fusion:** supplies or validates E3.
- **Overlay:** tail-hedge payoffs arrive exactly when D collapses and discounts widen. Their value as liquidity insurance should be credited against avoided fire sales.
- **IC deliberation layer:** scenario cards, a "what must be true" for V versus L, and probability elicitation.
- **Agent hooks:** agents ingest notices, run the nowcast and maintain the X-factor dashboard. A "timing-optimism challenger" compares GP-projected exits with model hazards. All numbers come from deterministic code.

---

## 7. Implementation notes

- **Python stack:**
  - **Core:** numpy, numba or JAX (vectorised path simulation), xarray (path × time × asset tensors), pandas.
  - **Filtering:** statsmodels state-space MLEModel and Kalman filter, or filterpy.
  - **Regimes:** hmmlearn as the HMM baseline. Write a custom HSMM in NumPyro or by EM.
  - **Survival:** lifelines or scikit-survival for exit hazards and competing risks.
  - **GLMs and challengers:** statsmodels GLM (Tweedie family) and LightGBM (tweedie objective) for zero-inflated cash flows.
  - **Bayesian pooling:** PyMC or NumPyro.
  - **Actuarial:** chainladder (Casualty Actuarial Society community package) for development triangles and Mack or bootstrap errors.
  - **Optimisation:** cvxpy for MPC and penalty-cost programmes.
  - **Sampling and sensitivity:** scipy.stats.qmc for Sobol paths; SALib for global sensitivity.
- **Algorithms:**
  - Use common random numbers across actions so that SELL/HOLD/REFINANCE/LEVER differences are low-variance.
  - Use antithetic and Sobol paths, and importance-sample regime C.
  - Solve SELL timing by least-squares Monte Carlo, regressing continuation value on N, a^e, q, X and S.
  - Run SMM with optuna or CMA-ES on the moment vector, then refine locally with BFGS.
- **Complexity:** cost is O(P·T·K). At P = 50k paths, T = 40 quarters and K = 400 cohorts that is 8×10⁸ updates, about 10 state variables each. That is feasible in float32 with JAX on a single GPU in minutes, or with numba in chunked CPU batches. Asset-level runs (K ≈ 2,000, P ≈ 5k) are similar in size.
- **Numerical pitfalls:**
  - Use intensity forms, 1−e^{−λΔ}, to keep calls and distributions within bounds.
  - Enforce U ≥ 0 and V ≥ 0.
  - Convert smoothing between frequencies: λ_q = λ_w^{13}.
  - Keep log and simple returns consistent.
  - Align fee and carry timing.
  - Align reporting lags against the *payout date*.
  - Fix HMM label switching by ordering regimes on m^D.
  - Do not over-fit a 10-year MSCI series that contains a single boom and a single drought.
  - Calibrate cohort idiosyncratic noise with N_eff.
  - Handle currency where funds are non-USD.

---

## 8. Risks, pitfalls and limitations

- **Cyclical or structural?** Higher base rates, "12 is the new 5", CV substitution and evergreen capital may lower the normal distribution rate permanently. The Φ sensitivity covers this; do not assume the 2017–19 normal.
- **Definitions disagree.** For the same period, MSCI shows 9–12%, Bain 14%, PitchBook 14.8% and McKinsey 6% (an AUM denominator). Vintages of the MSCI series also differ by 1–4pp. Calibrate to one provider and keep its definition throughout.
- **The direction of mark bias is ambiguous.** Exits run about 75% above prior marks, which suggests conservative marks. But stale 2019–22 inventory and software assets may be over-marked. Model both and let secondary bids arbitrate.
- **Old elasticities may mislead.** The RS estimates come from 1984–2010 data and miss the rate-shock channel. Treat κ as a prior and re-estimate it.
- **Endogenous liquidity.** Correlated LP selling widens discounts, and NAV-loan capacity shrinks in crisis. Avoid valuing SELL or REFINANCE as unconstrained options.
- **Behavioural frictions.** GP incentives, IPO lock-ups, in-kind distributions, CV conflicts and GP consent or rights of first refusal on transfers all affect outcomes.
- **Limits of this session.**
  - The shared web-search budget ran out mid-session. Several sources were therefore read as primary PDFs through a local text extractor, and some came through secondary summaries: McKinsey 2026 via TEXPERS and the search tool, Carta via ValueAddVC.
  - **Not verified:** the original TA example parameters. Three items first listed here are now identified by the literature audit (`research/literature/04_pe_cashflows.lit.md` §2), with metadata checked in Crossref; all three are in §10.
    - The "MSCI/Jeet market-sensitive periodic growth" model is Jeet (2020), SSRN 3775008.
    - "Tausch et al." is Tausch, Buchner & Schlüchtermann (2022), *Journal of Risk*.
    - The de Malherbe model that BKW describe is de Malherbe (2004), *IJTAF* 7(3). BKW's 2006 working paper credits it with an estimation-error term for reported values. A 2007 version, "Towards a Stochastic Cash Flow Model for Private Equity Funds", is a four-factor model whose factors include the reliability of reported values [unverified: indexed by Consensus only; a Crossref search did not return it, so no venue or DOI is confirmed].
  - **Working-paper versions:** the Gupta–Van Nieuwerburgh and Sorensen–Wang–Yang figures come from NBER working papers. For Nadauld et al., the PMEs (1.023 against 0.976) are the published *JFE* (2019) figures; the age split (about 3pp for funds aged 4–9) comes from the working paper.
  - **Illustrative only:** the toy programme is not ADIC data.

---

## 9. Open questions

1. What is ADIC's actual unfunded commitment, and its strategy, vintage and sector mix (especially software exposure)? These matter more than any parameter in §6.4.
2. Is the sovereign payout set on beginning-of-year NAV, smoothed, or fixed? What is its intra-year timing relative to the quarterly cash-flow seasonality?
3. Can the strategy groups' "forecast return" be expressed as cash-flow forecasts, so that E3 can solve for the implied forward IRR on economic NAV?
4. How much secondary-sale capacity, and what deferral tolerance, will the IC and the GPs (consents) accept? Are NAV loans at ADIC level permitted by the investment policy?
5. Should the payout-coverage gate (E8) be a hard Tier-1 constraint or a penalised soft constraint?
6. Which exit-factor observables can be licensed (IPO and M&A pipelines, leveraged-loan issuance), and at what latency?
7. How should CV elections be governed, given that sellers face information asymmetry (Nadauld et al.)?

---

## 10. References

**Academic and technical**
- Takahashi, D., & Alexander, S. (2002). Illiquid Alternative Asset Fund Modeling. *Journal of Portfolio Management* 28(2), 90–100. https://doi.org/10.3905/jpm.2002.319836
- Buchner, A., Kaserer, C., & Wagner, N. (2010). Modeling the Cash Flow Dynamics of Private Equity Funds: Theory and Empirical Evidence. *Journal of Alternative Investments* 13(1), 41–54. https://doi.org/10.3905/jai.2010.13.1.041. Working paper (2006): https://www.cfr-cologne.de/download/kolloquium/2007/buchner_et_al.pdf
- de Malherbe, E. (2004). Modeling Private Equity Funds and Private Equity Collateralised Fund Obligations. *International Journal of Theoretical and Applied Finance* 7(3), 193–230. https://doi.org/10.1142/S0219024904002359
- Tausch, C., Buchner, A., & Schlüchtermann, G. (2022). Modeling the Exit Cashflows of Private Equity Fund Investments. *Journal of Risk*. https://doi.org/10.21314/jor.2022.029 (the Crossref and OpenAlex records give no volume, issue or pages)
- Luxenberg, E., Boyd, S., van Beek, M., Cao, W., & Kochenderfer, M. (2022). Strategic Asset Allocation with Illiquid Alternatives. In *Proceedings of the Third ACM International Conference on AI in Finance (ICAIF '22)*, 249–256. ACM. https://doi.org/10.1145/3533271.3561769. Preprint, which lists nine authors (adding Diamond, S., Ulitsky, A., Menda, K., & Vairavamurthy, V.) and is the source of the §2.2 example figures: arXiv:2207.07767, https://arxiv.org/abs/2207.07767
- Karatas, T., Klinkert, F., & Hirsa, A. (2021). Supervised Neural Networks for Illiquid Alternative Asset Cash Flow Forecasting. arXiv:2108.02853. https://arxiv.org/abs/2108.02853
- Jeet, V., Stucke, R. R., & Partani, A. (2026). A Crucial Enhancement to the Takahashi–Alexander Cash Flow Model. *The Journal of Private Markets Investing* 24(3), 62–73. https://doi.org/10.3905/jpmi.2026.1.010 (journal page: https://iij.journals.publicknowledgeproject.org/index.php/JPMI/article/view/14501)
- Jeet, V. (2020). Modeling Private Investment Cash Flows With Market Sensitive Periodic Growth. SSRN working paper. https://doi.org/10.2139/ssrn.3775008
- Brown, G. W., Ghysels, E., & Gredil, O. (2023). Nowcasting Net Asset Values: The Case of Private Equity. *Review of Financial Studies* 36(3), 945–986. https://doi.org/10.1093/rfs/hhac045. Working paper: https://uncipc.com/wp-content/uploads/2020/04/BGG_nowcasting.pdf
- Robinson, D. T., & Sensoy, B. A. (2016). Cyclicality, Performance Measurement, and Cash Flow Liquidity in Private Equity. *Journal of Financial Economics* 122(3), 521–543. https://doi.org/10.1016/j.jfineco.2016.09.008. NBER WP 17428: https://www.nber.org/papers/w17428
- Ljungqvist, A., & Richardson, M. (2003). The Cash Flow, Return and Risk Characteristics of Private Equity. NBER WP 9454. https://www.nber.org/papers/w9454
- Gourier, E., Phalippou, L., & Westerfield, M. M. (2024). Capital Commitment. *Journal of Finance* 79(5), 3407–3457. https://doi.org/10.1111/jofi.13382. CEPR DP16910: https://ideas.repec.org/p/cpr/ceprdp/16910.html
- Giommetti, N., & Sørensen, M. (2021). Optimal Allocation to Private Equity. Working paper. https://doi.org/10.2139/ssrn.3761243 (portal: https://research.cbs.dk/en/publications/optimal-allocation-to-private-equity/)
- Ang, A., Papanikolaou, D., & Westerfield, M. M. (2014). Portfolio Choice with Illiquid Assets. *Management Science* 60(11), 2737–2761. https://doi.org/10.1287/mnsc.2014.1986
- Sorensen, M., Wang, N., & Yang, J. (2014). Valuing Private Equity. *Review of Financial Studies* 27(7), 1977–2021. https://doi.org/10.1093/rfs/hhu013. NBER WP 19612 (figures cited from the WP): https://www.nber.org/papers/w19612
- Dimmock, S. G., Wang, N., & Yang, J. (2024). The Endowment Model and Modern Portfolio Theory. *Management Science* 70(3), 1554–1579. https://doi.org/10.1287/mnsc.2023.4759
- Geltner, D. (1991). Smoothing in Appraisal-Based Returns. *Journal of Real Estate Finance and Economics* 4(3), 327–345. https://doi.org/10.1007/BF00161933
- Geltner, D. (1993). Estimating Market Values from Appraised Values without Assuming an Efficient Market. *Journal of Real Estate Research* 8(3), 325–345. https://doi.org/10.1080/10835547.1993.12090713
- Getmansky, M., Lo, A. W., & Makarov, I. (2004). An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns. *Journal of Financial Economics* 74(3), 529–609. https://doi.org/10.1016/j.jfineco.2004.04.001
- Couts, S. J., Gonçalves, A. S., & Rossi, A. (2024). Unsmoothing Returns of Illiquid Funds. *Review of Financial Studies* 37(7), 2110–2155. https://doi.org/10.1093/rfs/hhae006
- Kaplan, S. N., & Schoar, A. (2005). Private Equity Performance: Returns, Persistence, and Capital Flows. *Journal of Finance* 60(4), 1791–1823. https://doi.org/10.1111/j.1540-6261.2005.00780.x
- Korteweg, A., & Nagel, S. (2016). Risk-Adjusting the Returns to Venture Capital. *Journal of Finance* 71(3), 1437–1470. https://doi.org/10.1111/jofi.12390
- Gredil, O., Griffiths, B., & Stucke, R. (2023). Benchmarking Private Equity: The Direct Alpha Method. *Journal of Corporate Finance* 81, 102360. https://doi.org/10.1016/j.jcorpfin.2023.102360
- Gupta, A., & Van Nieuwerburgh, S. (2021). Valuing Private Equity Investments Strip by Strip. *Journal of Finance* 76(6), 3255–3307. https://doi.org/10.1111/jofi.13073. NBER WP 26514: https://www.nber.org/papers/w26514
- Driessen, J., Lin, T.-C., & Phalippou, L. (2012). A New Method to Estimate Risk and Return of Nontraded Assets from Cash Flows: The Case of Private Equity Funds. *JFQA* 47(3), 511–535. https://doi.org/10.1017/S0022109012000221
- Ang, A., Chen, B., Goetzmann, W. N., & Phalippou, L. (2018). Estimating Private Equity Returns from Limited Partner Cash Flows. *Journal of Finance* 73(4), 1751–1783. https://doi.org/10.1111/jofi.12688
- Nadauld, T. D., Sensoy, B. A., Vorkink, K., & Weisbach, M. S. (2019). The Liquidity Cost of Private Equity Investments: Evidence from Secondary Market Transactions. *Journal of Financial Economics* 132(3), 158–181. https://doi.org/10.1016/j.jfineco.2018.11.007. NBER WP 22404 (2016): https://www.nber.org/papers/w22404
- Harris, R. S., Jenkinson, T., & Kaplan, S. N. (2014). Private Equity Performance: What Do We Know? *Journal of Finance* 69(5), 1851–1882. https://doi.org/10.1111/jofi.12154
- Phalippou, L., & Gottschalg, O. (2009). The Performance of Private Equity Funds. *Review of Financial Studies* 22(4), 1747–1776. https://doi.org/10.1093/rfs/hhn014
- Metrick, A., & Yasuda, A. (2010). The Economics of Private Equity Funds. *Review of Financial Studies* 23(6), 2303–2341. https://doi.org/10.1093/rfs/hhq020
- Franzoni, F., Nowak, E., & Phalippou, L. (2012). Private Equity Performance and Liquidity Risk. *Journal of Finance* 67(6), 2341–2373. https://doi.org/10.1111/j.1540-6261.2012.01788.x
- Jegadeesh, N., Kräussl, R., & Pollet, J. M. (2015). Risk and Expected Returns of Private Equity Investments: Evidence Based on Market Prices. *Review of Financial Studies* 28(12), 3269–3302. https://doi.org/10.1093/rfs/hhv046
- Axelson, U., Jenkinson, T., Strömberg, P., & Weisbach, M. S. (2013). Borrow Cheap, Buy High? The Determinants of Leverage and Pricing in Buyouts. *Journal of Finance* 68(6), 2223–2267. https://doi.org/10.1111/jofi.12082
- Korteweg, A., & Sorensen, M. (2010). Risk and Return Characteristics of Venture Capital-Backed Entrepreneurial Companies. *Review of Financial Studies* 23(10), 3738–3772. https://doi.org/10.1093/rfs/hhq050
- Kaplan, S. N., & Strömberg, P. (2009). Leveraged Buyouts and Private Equity. *Journal of Economic Perspectives* 23(1), 121–146. https://doi.org/10.1257/jep.23.1.121
- Siegel, L. B. (2008). Alternatives and Liquidity: Will Spending and Capital Calls Eat Your "Modern" Portfolio? *Journal of Portfolio Management* 35(1), 103–114. https://doi.org/10.3905/JPM.2008.35.1.103
- Nevins, D., Conner, A., & McIntire, G. (2004). A Portfolio Management Approach to Determining Private Equity Commitments. *Journal of Alternative Investments* 6(4), 32–46. https://doi.org/10.3905/jai.2004.391062
- Hayes, M., Primbs, J. A., & Chiquoine, B. (2015). A Penalty Cost Approach to Strategic Asset Allocation with Illiquid Asset Classes. *Journal of Portfolio Management* 41(2), 33–41. https://doi.org/10.3905/jpm.2015.41.2.033
- Mack, T. (1993). Distribution-free Calculation of the Standard Error of Chain Ladder Reserve Estimates. *ASTIN Bulletin* 23(2), 213–225. https://doi.org/10.2143/AST.23.2.2005092
- Bühlmann, H. (1967). Experience Rating and Credibility. *ASTIN Bulletin* 4(3), 199–207. https://doi.org/10.1017/S0515036100008989
- England, P. D., & Verrall, R. J. (2002). Stochastic Claims Reserving in General Insurance. *British Actuarial Journal* 8(3), 443–518. https://doi.org/10.1017/S1357321700003809
- Basel Committee on Banking Supervision. Basel Framework, LCR40 (net cash outflows), para. LCR40.64. https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30

**Market data and practitioner sources**
- MSCI (October 2026). *Private Capital Benchmarks Summary Q2 2026*. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
- MSCI (May 2026). *Private Capital in Focus: US & Europe* (presentation). https://www.msci.com/downloads/web/msci-com/discover-msci/events/event-assets/2026/may/Presentation_%20Private%20Capital%20in%20Focus_USEurope_May132026.pdf
- MSCI (2026). *The distribution drought in private equity persists*. https://www.msci.com/data-and-analytics/private-asset-solutions/visualizations/the-distribution-drought-in-private-equity-persists
- MSCI (14 January 2026). *Private Capital in Focus: Trends to Watch for 2026*. https://www.msci.com/research-and-insights/blog-post/private-capital-in-focus-trends-to-watch-for-2026
- MSCI (2026). *Private Capital Benchmarks Summary Q4 2025* (preview). https://www.msci.com/research-and-insights/paper/msci-private-capital-benchmarks-summary-q4-2025
- Bain & Company (February 2026). *Global Private Equity Report 2026: Outlook, Gaining Traction*. https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/
- Bain & Company (8 June 2026). Midyear PE report press release. https://www.prnewswire.com/news-releases/winning-firms-will-focus-on-what-they-can-control-weather-the-rest-as-triple-shock-brakes-private-equitys-latest-revival-bain--company-2026-midyear-pe-report-302793107.html
- Chronograph (2025). Summary of Bain Global PE Report 2025. https://www.chronograph.pe/top-takeaways-from-bains-2025-private-equity-report/
- McKinsey & Company (February 2026). *Global Private Markets Report 2026, Private Equity: Clearer View, Tougher Terrain*. https://www.mckinsey.com/~/media/mckinsey/industries/private%20equity%20and%20principal%20investors/our%20insights/mckinseys%20global%20private%20markets%20report/2026/private%20equity/gpmr2026-private-equity-clearer-view-tougher-terrain_final_v10.pdf; summary: https://www.texpers.org/index.php?option=com_dailyplanetblog&view=entry&year=2026&month=02&day=13&id=386%3Amckinsey-s-global-private-markets-report-2026-private-equity-clearer-view-tougher-terrain
- Jefferies (July 2026). *Global Secondary Market Review*. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
- Cherry Bekaert (2026). *Private Equity Mid-Year 2026 Report* (PitchBook data as of 30 June 2026). https://www.cbh.com/insights/reports/private-equity-mid-year-2026-report/
- Hamilton Lane (11 March 2026). *2026 Market Overview* (release). https://www.prnewswire.com/news-releases/hamilton-lane-2026-market-overview-302710433.html
- Cambridge Associates (2020). *US Private Equity (Legacy Definition) Index and Selected Benchmark Statistics, 31 December 2019*. https://www.cambridgeassociates.com/wp-content/uploads/2020/06/WEB-2019-Q4-USPE-legacy-Benchmark-Book.pdf
- Rede Partners (June 2026). *NAV Financing Market Report 2026*. https://www.rede-partners.com/news-insights-database/publication-rede-nav-2026
- Cliffwater for ERSRI (December 2023). *Private Equity / Private Credit / Real Assets Pacing Plan*. https://data.treasury.ri.gov/dataset/40fb544c-65c5-464f-ba49-e3f65d1adc36/resource/7783fe26-a966-4850-82e0-f3f931812015/download/1a-cliffwater-pe-pc-ra-pacing-plan-dec-2023-final.pdf
- Value Add VC (August 2026). *The DPI Drought* (secondary aggregation of Carta data). https://valueaddvc.com/dpi-drought-report
- Carta (2026). *Q4 2025 VC Fund Performance* (blocked for automated access; cited via secondary sources). https://carta.com/data/vc-fund-performance-q4-2025/

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 and `research/literature/04_pe_cashflows.lit.md` §2. Metadata was confirmed in Crossref and OpenAlex on 2026-10-18.

- **Luxenberg et al. (2022), §2.2 and §10:** the arXiv-only entry now cites the ICAIF '22 proceedings (pp. 249–256, DOI 10.1145/3533271.3561769), whose Crossref record lists five authors. The nine-author arXiv:2207.07767 is kept as the preprint, and the §2.2 example figures are marked as coming from it.
- **Jeet et al. (2026), §10:** the title "…Takahashi and Alexander's Cash Flow Model" is now "A Crucial Enhancement to the Takahashi–Alexander Cash Flow Model". Added the authors (Jeet, Stucke, Partani), pages 62–73 and DOI 10.3905/jpmi.2026.1.010.
- **Sorensen, Wang & Yang (2014), §10:** *RFS* 27(2) is now 27(7), 1977–2021. Added DOI 10.1093/rfs/hhu013.
- **Nadauld et al., §2.6, §8 and §10:** now cites *JFE* 132(3), 158–181 (2019), DOI 10.1016/j.jfineco.2018.11.007, keeping NBER WP 22404 (2016). The seller PME is now 0.976 (was 0.974). The age split (about 3pp at ages 4–9) is labelled as a working-paper figure. The ~5pp gap and the 3–5pp range in §1 item 6 and E9 do not change.
- **Geltner, §2.5 and §3:** "Geltner (1991, 1993)" is split into the 1991 smoothing model and the 1993 recovery procedure, which does not assume that true returns are serially uncorrelated.
- **BGG, §2.5:** the weekly λ of 0.951 and the 4.6%/3.1% NAV noise are labelled as working-paper figures.
- **E7:** λ_q ≈ 0.5 "(from BGG)" is relabelled as this stream's conversion of BGG's weekly λ, not a BGG estimate.
- **§8 and §10, the three items listed as not verified:** identified and added to §10: Jeet (2020), SSRN 3775008; Tausch, Buchner & Schlüchtermann (2022), *Journal of Risk*, DOI 10.21314/jor.2022.029; de Malherbe (2004), *IJTAF* 7(3), 193–230, DOI 10.1142/S0219024904002359. The 2007 de Malherbe version is marked [unverified].
- **Checked, no change (Giommetti & Sørensen):** Crossref and OpenAlex list Morten Sorensen (Sørensen) as second author of SSRN 3761243, so the "Jørgensen" in streams 01, 06 and 11 is the error.
- **Checked, no change (other references):** Crossref resolves Bühlmann (1967), DOI 10.1017/S0515036100008989, to *ASTIN Bulletin* 4(3), 199–207. Ljungqvist & Richardson (NBER WP 9454) and Getmansky, Lo & Makarov (*JFE* 74(3), 529–609) were already correct. Mack (1993) matches the Crossref record cited in the G3 re-check.
