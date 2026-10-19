# Stream 07: Fusing underwritten, current-actual and forecast returns into calibrated forward beliefs

*ADIC multi-period robust TPA framework. Research dossier, as of 2026-10-18.*

**Evidence tags.** [S] = sourced fact (citation in §10). [P] = practitioner consensus. [I] = my inference or design choice. A † in §10 marks a reference cited from memory and not re-verified online in this session. The session's shared web-search budget ran out partway through (§8), so some details come from search-index summaries. Where that happens, the text says so.

---

## 1. Executive summary

The underwritten return (u), the current actual return (a) and the strategy group's forecast (f) are not three estimates of the same quantity:

- **u** is the deal team's base-case path set at entry. It is an *inside view*, produced by people who wanted approval.
- **a** is a *sunk* since-inception path. It mixes realized market beta, realized idiosyncratic performance and mark error from stale, smoothed or managed NAVs.
- **f** is the current inside view of remaining cash flows. It often comes from the same people who wrote u.

The only quantity that matters for a SELL / HOLD / REFINANCE / LEVER decision is the **forward return on current (nowcast) NAV**. That is the IRR a buyer paying 100% of today's value would earn. Since-inception IRR is a sunk-cost metric [S: Arkes & Blumer 1985]. It is useful only as a noisy signal of asset quality.

**Recommendation: a deterministic, auditable "Forward Belief Engine" (FBE)** with six steps.

1. **Translate** u, a and f onto one basis: annualized forward log-return on nowcast NAV, plus an exit-timing distribution.
2. **Anchor** each asset on a *reference-class prior* (the outside view) by strategy × age × regime.
3. **Debias** each signal with level, slope and variance corrections learned from ADIC's own forecast–outcome history (the 18-year IC memo corpus). Use hierarchical partial pooling, with literature-based priors where history is thin. This is the finance analogue of weather-service Model Output Statistics.
4. **Fuse** by precision weighting with correlated errors. This is Bates–Granger GLS, which is the same thing as multi-source Bühlmann credibility. Shrink the weights toward simple defaults (the forecast-combination puzzle) and constrain them to be non-negative.
5. **Report** the posterior mean and variance of the forward return, the probability that the forecast is optimistic, base-rate percentiles, flags and "what you need to believe".
6. **Score continuously** with proper scoring rules, PIT and coverage checks, Basel-style traffic lights and drift detection. Credibility weights are re-estimated as forecasts resolve.

For fund interests, maturity-dependent credibility comes from actuarial reserving. The Bornhuetter–Ferguson, Benktander and Mack methods give a closed-form weight on "actual" of c* = p/(p+t), where p is the percent developed [S: Mack 2000].

**Why this matters now:**

- Interim marks settle slowly. Funds take 6–8 years to settle into their final quartile [S: Cambridge Associates 2018].
- Only 57% of buyout funds that showed top-quartile numbers at fundraising ended top quartile [S: Harris et al. 2020].
- NAVs are inflated around fundraising by weaker managers [S: Jenkinson et al. 2013; Barber & Yasuda 2017; Brown et al. 2019].
- Executives' 80% intervals contain outcomes only 36% of the time [S: Ben-David et al. 2013].
- Optimism is endemic in long-horizon project forecasts [S: Flyvbjerg et al. 2005; HM Treasury Green Book].
- The 2026 environment raises the stakes:
  - PE distributions are about 14% of NAV, below 15% for four years running.
  - About $3.8tn of value sits in ~32,000 unsold companies, with holding periods near 7 years [S: Bain 2026].
  - Deals now need 10–12% annual EBITDA growth, against 5% in 2015, to reach 2.5x in five years. Bain calls this "12 is the new 5".
  - High-quality buyout LP interests clear at about 90% of NAV in secondaries [S: Evercore H1 2026].

**Worked results (§6.8):**

- **Buyout co-invest.** The group forecasts a 22.2% forward IRR, a "hockey stick" against a 9.0% since-inception IRR. The fused posterior is 13.6% (80% band 7.8–19.7%), and P(forecast optimistic) is 96%.
- **Late-life fund.** Taking the group's forecast at face value implies HOLD (PV 387 vs a bid of 352). The posterior implies a marginal SELL (PV 348). The decision turns on whether the group's late-life bias is at most 2.8% a year.

**Data priority:** start a **point-in-time (bitemporal) forecast archive now**. Without it, forecaster credibility cannot be learned without look-ahead bias.

---

## 2. Core concepts and theory

### 2.1 What each number actually measures

| Input | What it measures | Time stamp | Producer | Dominant failure modes |
|---|---|---|---|---|
| u: underwritten | Base-case IRR/MOIC/hold at entry, often gross and deal-level, with downside and upside cases | t₀ | Deal team seeking approval | Inside-view optimism, strategic misrepresentation, staleness after entry |
| a: current actual | Since-inception path: β × realized market + realized idiosyncratic alpha + mark error | t − s (NAV lag s) | GP or ADIC valuation | Sunk; J-curve; NAV smoothing and management; momentum is not persistence |
| f: forecast | Remaining exit value and timing as seen today | t | Strategy group, often the original team | Anchoring on u, escalation and disposition, exit-timing optimism, overconfident ranges |
| **Target ρᵢ** | **Expected forward annualized log-return on nowcast NAV over remaining life Hᵢ** | t | FBE | n/a |

### 2.2 Since-inception versus forward returns

The since-inception IRR solves Σ_{s≤t} CF_s(1+IRR)^{−s} + NAV_t(1+IRR)^{−t} = 0. It blends past realized cash flows with today's mark.

The **forward IRR** solves

  −V*_t − Σ_{s>t} E[calls_s](1+r)^{−(s−t)} + Σ_{s>t} E[dist_s](1+r)^{−(s−t)} = 0,

where V*_t is the nowcast NAV. For a single-exit asset, r^fwd = [(M_f·PI − D_t)/V*_t]^{1/H} − 1 (PI = paid-in, D = distributions to date).

For single-draw deals the life multiple factorizes: M_life ≈ (1+IRR_SI)^τ·(1+r^fwd)^H. So a forecast that keeps the life multiple close to underwriting after years of underperformance *mechanically* implies an extreme forward return. That is the "hockey stick" signature of anchoring and escalation [I].

### 2.3 Forecast combination

Bates & Granger (1969) derive variance-minimizing weights for a pair of forecasts from portfolio logic [S]. Later work writes the general case in matrix form: w* = Σ⁻¹1/(1′Σ⁻¹1), where Σ is the forecast-error covariance. With diagonal Σ this reduces to inverse-MSE weights.

The **forecast-combination puzzle** is that equal weights often beat estimated "optimal" weights. Claeskens, Magnus, Vasnev & Wang (2016) show the cause: once weights are estimated, the combination is biased and has higher variance [S]. Smith & Wallis (2009) attribute it to weight-estimation error [S]. Wang, Hyndman, Li & Kang (2023) review fifty years of the literature [S]. The remedy is to shrink toward equal or prior weights: Diebold & Pauly (1990), and the egalitarian ridge/LASSO of Diebold & Shin (2019) [S].

Here the errors are positively correlated: f is anchored on u and on the current mark. GLS correctly discounts redundant information but can produce negative weights. I recommend constraining w ≥ 0 and reporting any binding constraint [I].

When the true model is not in the candidate set, *stacking* of predictive distributions under a proper scoring rule is preferred to Bayesian model averaging [S: Yao, Vehtari, Simpson & Gelman 2018].

### 2.4 Credibility is Bayesian shrinkage

Bühlmann (1967) gives the premium as Z·X̄ + (1−Z)·μ, with Z = n/(n+k) and k = EPV/VHM. EPV is the expected process variance and VHM is the variance of hypothetical means [S]. Bühlmann–Straub replaces n with exposure m_i [S]. Under normal–normal conjugacy the Bayesian posterior mean has exactly this form. With several independent sources it generalizes to precision weighting.

Efron & Morris (1975) showed with baseball batting averages that shrinkage cuts prediction error several-fold [S]. Korteweg & Sorensen (2017) model LP learning about PE skill the same way: each new fund updates beliefs with weight equal to a signal-to-noise ratio, and posterior variance shrinks by (1−s) [S]. Their headline results:

- Skill differences are real: the gap in expected returns between top- and bottom-quartile firms is 7–8 pp a year.
- Identifying skill is hard: even after observing 50 past funds, only 53–61% of past top-quartile firms are expected to stay top quartile [S].

That is the right prior for how much weight any single track record deserves.

### 2.5 Actuarial reserving as a template for maturity-dependent credibility

The mapping from claims reserving to private assets:

| Reserving | Private assets |
|---|---|
| Ultimate claims U | Final TVPI (or total distributions) |
| Paid C_k | DPI |
| Incurred (paid + case reserves) | TVPI (D + NAV) |
| A priori U₀ | Debiased underwriting or reference class |
| Percent developed p_k = 1/LDF_k | Share of ultimate value "reported" by age k, from development triangles |

The estimators [S: Bornhuetter & Ferguson 1972; Mack 2000]:

- Chain ladder: U_CL = C/p.
- Bornhuetter–Ferguson: U_BF = C + (1−p)U₀ = p·U_CL + (1−p)U₀.
- Benktander: U_GB = C + (1−p)U_BF = [1−(1−p)²]U_CL + (1−p)²U₀. Iterating further converges to CL.

Mack (2000) derives the MSE-optimal credibility weight on CL as **c* = p/(p+t)**, with t = E[α²(U)] / (Var(U₀) + Var(U) − E[α²(U)]). He shows:

- BF beats CL when p < t ("green" years).
- Benktander almost always has lower MSE than BF or CL and is close to exact Bayes.
- Some companies use t = 0.5 [S].

Gogol's lognormal–lognormal Bayes gives credibility z = σ²/(σ²+τ²), with τ² = ln(1+β²q/p) [S: via Mack 2000].

The lesson for ADIC is that the weight on "actual" should rise with maturity p, at a rate set by how noisy development is (t). The paid-vs-incurred reconciliation of the Munich chain ladder suggests using the DPI/TVPI realization ratio as an extra signal of NAV reliability [I; Quarg & Mack 2004†].

### 2.6 Bias taxonomy and where each bias enters the model

| Mechanism | Evidence | Model term |
|---|---|---|
| Inside-view optimism / planning fallacy | Kahneman & Lovallo 1993; Flyvbjerg 2006; Lovallo, Clarke & Camerer 2012 (PE) [S] | α_u, α_f > 0 |
| Strategic misrepresentation / agency | Flyvbjerg 2006; NAV inflation in fundraising windows [S] | α larger for in-house originations and fundraising GPs |
| Anchoring, escalation, disposition | Staw 1976; Guler 2007† (VC follow-ons); Shefrin & Statman 1985† | Forecast error increasing in plan shortfall (u − a); serially correlated revisions |
| Overconfidence | Ben-David, Graham & Harvey 2013 [S] | Stated ranges too narrow: inflate ω |
| Overreaction / extrapolation | Bordalo et al. 2019; Andonov & Rauh 2018 [S] | Slope β_f > 1 (MZ slope b < 1) |
| NAV staleness, smoothing, management | Jenkinson et al. 2013; Brown, Ghysels & Gredil 2023 [S] | Nowcast and NAV-bias terms |
| Selection on noisy estimates | Smith & Winkler 2006 [S] | Rank and decide on posteriors, never raw forecasts |

### 2.7 Calibration and scoring

- **Proper scoring rules** make honest probabilistic reporting optimal. Log score: −ln p(y). CRPS(F,y) = ∫(F(z) − 1{z≥y})²dz = E|X−y| − ½E|X−X′|. For a Gaussian, CRPS = σ[z(2Φ(z)−1) + 2φ(z) − 1/√π] [S: Gneiting & Raftery 2007].
- **Paradigm:** maximize sharpness subject to calibration [S: Gneiting, Balabdaoui & Raftery 2007].
- **PIT values** u = F(y) should be i.i.d. U(0,1) under correct specification [S: Diebold, Gunther & Tay 1998].
- **Mincer–Zarnowitz regression** y = a + b·f + e tests forecast efficiency (a = 0, b = 1) [S: Mincer & Zarnowitz 1969].
- **Nordhaus (1987) weak efficiency:** forecast revisions should be unpredictable. Serially correlated revisions reveal smoothing or anchoring [S].

---

## 3. Methods, models and trade-offs

| Method | Data need | Strength | Weakness | Role in ADIC |
|---|---|---|---|---|
| Simple average of u, a, f | None | Robust, transparent | Ignores bias, staleness, maturity | Baseline only |
| Inverse-MSE (Bates–Granger, diagonal) | Per-source error history | Simple | Double-counts correlated sources | Sanity check |
| Full GLS weights | Error covariance | Uses correlation | Unstable, negative weights | Only with shrinkage and w ≥ 0 |
| Shrink-to-prior weights (Diebold–Pauly / egalitarian ridge) | Moderate | Resolves the puzzle | Shrinkage target matters | **Default weighting** |
| MOS / Mincer–Zarnowitz debiasing | Forecast–outcome pairs | Corrects level and slope | Needs ~30+ effective pairs | **Core debiasing**, pooled hierarchically |
| EMOS / non-homogeneous Gaussian regression: y ~ N(a+b·f, c+d·S²) | Pairs + stated ranges S | Calibrates spread as well as mean; min-CRPS fit; operational in weather services [S: Gneiting et al. 2005; MOS origin: Glahn & Lowry 1972] | Gaussian unless extended | **Calibrates strategy-group ranges** |
| Hierarchical / empirical Bayes | Panel of assets × groups × vintages | Small-sample discipline; separates common vintage shocks from forecaster bias | MCMC, priors to justify | **Calibration engine** |
| Kalman / state space | Quarterly NAVs, cash flows, comps | Handles staleness and smoothing; dynamic credibility (Kalman gain) | Tuning, model risk | **NAV nowcast and belief updates** [S: Brown, Ghysels & Gredil 2023] |
| BF / Benktander / Mack | Development triangles | Age-aware, closed form, IC-legible | Needs stable development pattern | **Fund-interest ultimates** |
| Black–Litterman / entropy pooling | Views + confidences | Brings IC views and fused beliefs into the scenario set | Confidence calibration | **IC views; tilting the 50k-path simulation** [†] |
| Cooke classical model | Resolved "seed" questions | Rewards calibration × informativeness | Needs seeds | **Weighting IC and team views**. Performance weights beat equal weights in 32 of 33 studies in-sample and in 26 of 33 on an out-of-sample validity index, but their out-of-sample statistical accuracy is lower [S: Colson & Cooke 2017] [corrected 2026-10-18: was "won in 26 of 33 studies in-sample"] |
| Stacking | LOO predictive scores | Robust when no model is true | Data-hungry | Choosing among fusion variants |
| Conformal wrappers (split / adaptive) | Residual history | Distribution-free coverage, including under drift [S: Gibbs & Candès 2021] | Marginal, not conditional, coverage | Interval-coverage guardrail |
| ML on memo features (GBM, quantile regression) | Large labeled set | Nonlinear feature effects | Overfits hundreds of deals | Bias covariates only, heavily regularized |

**Trade-offs.**

- Interpretability favours closed-form Gaussian fusion and credibility formulas. Calibration rigor favours hierarchical Bayes. The two combine cleanly: hierarchical Bayes estimates the parameters (α, β, ω, σ_k) offline, quarterly, and a closed-form posterior applies them online per asset. The IC sees the same weights the code uses [I].
- Gaussian log-returns are adequate for buyout, infrastructure and core real estate. For VC and growth, use mixtures or skew-t. Korteweg & Sorensen needed a three-normal mixture for VC performance [S].

---

## 4. Empirical evidence and current market data

### 4.1 Underwriting optimism

- **PE targets are high.** Gompers, Kaplan & Mukharlyamov surveyed 79 PE investors with more than $750bn of AUM. Investors "rely primarily on IRR and multiples" and target about 25% IRR (draft version; a 2014 trade report cites 27% gross) [S]. Buyout fund multiples cluster at 1.73–1.78x whatever the predecessor fund's quartile at fundraising [S: Harris et al. 2020].
- **Required operating performance has risen.** In 2015 a 2.5x/5-year buyout needed about 5% annual EBITDA growth. With 8–9% debt costs and 30–40% leverage it now needs about 10–12% ("12 is the new 5"). In the low-rate era, rising multiples "powered over 50% of all buyout returns" [S: Bain 2026]. Underwriting built on 2010s playbooks is therefore biased in the current regime [I].
- **Reference-class evidence from infrastructure and projects:**
  - Across 210 transport projects in 14 nations, rail passenger forecasts were too high in nine of ten projects, by 106% on average.
  - In half of road projects, traffic missed the forecast by more than ±20%.
  - Accuracy did not improve over 30 years [S: Flyvbjerg, Skamris Holm & Buhl 2005].
- **The UK Treasury institutionalizes the correction.** Its Green Book guidance says "project appraisers have the tendency to be over optimistic." It prescribes uplifts. Upper bounds are works-duration / capex: standard buildings 4%/24%, non-standard civil engineering 25%/66%, equipment/development 54%/200%. The upper bound is reduced as risk mitigation is evidenced [S: HM Treasury 2003, published online 2013].
- Kahneman & Lovallo (1993): "Overly optimistic forecasts result from the adoption of an inside view." In a PE test, a reference class of analogies outperformed a few analogies familiar to the decision maker [S: Lovallo, Clarke & Camerer 2012].

### 4.2 Interim valuation behaviour

- **Jenkinson, Sousa & Stucke (2013)**, using CalPERS's 761 fund investments, found reported values understate subsequent distributions by about 35% on average, with a Q4 (audit) jump. Valuations are inflated during follow-on fundraising and reverse afterwards. Interim IRRs reported during fundraising have little power to predict ultimate returns, while PME-based measures predict better [S: abstract via search index; SSRN page blocked].
- **Barber & Yasuda (2017):** low-reputation GPs with low realization rates show performance that peaks around fundraising and then erodes [S].
- **Brown, Gredil & Kaplan (2019):** some underperformers inflate NAVs while fundraising, and are less likely to raise a next fund. Top performers appear to understate [S].
- **Jenkinson, Landsman, Rountree & Soonawalla (2020):** buyout NAVs show little systematic bias. VC NAVs are aggressively biased, especially since 2000 (sample of 384 VC and 195 buyout funds, 1988–2016) [S].
- **Brown, Ghysels & Gredil (2023)** nowcast fund NAVs weekly with a state-space model of cash flows, reported NAVs and public comparables. In the published *RFS* version, the average fund's market beta is about 1.0 (buyout) and 1.4 (venture), and total risk is about 33% and 40% a year [S]. [corrected 2026-10-18: this line previously gave betas around 1.05 and 1.20 and median total risk of 33% and 38%, 10 and 13 pp above as-reported series. Those are 2020 working-paper figures, not the cited *RFS* version's.]
- Secondary-transaction indices show higher betas and volatilities, and lower alphas, than NAV-based indices [S: Boyer, Nadauld, Vorkink & Weisbach 2018].

### 4.3 How predictive are interim returns of final outcomes?

- Funds take **6–8 years** on average to settle into their ultimate quartile (VC and fund-of-funds 7–9; secondaries 5–7). TVPI settles later than IRR. Most funds rank in nearly every quartile at some point [S: Cambridge Associates 2018].
- Of buyout funds showing top-quartile numbers at fundraising, **57%** ended top quartile. About **23%** of bottom-quartile-at-fundraising funds ended above median (24% post-2000) [S: Harris, Jenkinson, Kaplan & Stucke 2020].
- PitchBook reports R² of interim versus final IRR of **0.40 at age 4** and **0.54 at age 5**, with median absolute errors of 5.2% and 4.3% [S: search-index summary; PDF returned 403].
- For 2000–2015 vintages, IRR stagnates around year 7 and median TVPI flattens after year 8 [S: Bain 2026]. Forward returns on late-life NAV are structurally low [I].

### 4.4 Skill, luck and extrapolation

- Long-term persistence is real: the top–bottom quartile spread in expected returns is 7–8 pp a year (buyout interquartile 8.03 pp; VC 6.60 pp). Investable persistence is low [S: Korteweg & Sorensen 2017].
- Using information available at fundraising, post-2000 buyouts show little or no persistence, while VC persistence survives [S: Harris et al. 2020].
- US public pension return assumptions extrapolate past own performance across all risky asset classes. In PE this extrapolation is "driven by stale investments" [S: Andonov & Rauh 2018].
- Analysts' most optimistic long-term growth forecasts precede the lowest returns, consistent with overreaction [S: Bordalo, Gennaioli, La Porta & Shleifer 2019].

### 4.5 Calibration of expert forecasts

- Across more than 13,300 executive forecasts, "realized market returns are within the executives' 80% confidence intervals only 36% of the time." Miscalibrated firms invest more and borrow more [S: Ben-David, Graham & Harvey 2013].
- Cooke's classical model weights experts by statistical accuracy × informativeness on seed questions. Across 33 professionally contracted studies run in 2006–2015 (320 experts [unverified: the expert count came from a Wikipedia page and is not in the Colson & Cooke abstract]), performance weights beat equal weights in-sample in 32 of 33. Under cross-validation (training sets of 80% of the calibration variables), they beat equal weights on the combined out-of-sample validity index in 26 of 33 (p = 0.001). Their out-of-sample statistical accuracy is lower than equal weighting's [S: Colson & Cooke 2017]. [corrected 2026-10-18: previously sourced to Wikipedia and read as an in-sample result.]
- Geopolitical forecasting tournaments found that training, teaming and aggregation with extremizing improve accuracy [†: Tetlock 2005; Mellers et al. 2014. S: Baron et al. 2014].

### 4.6 Current market data

| Item | Value | As of | Source |
|---|---|---|---|
| PE distributions / NAV | ~14% in 2025; <15% for 4 consecutive years | FY2025 (published 2026) | Bain GPER 2026 [S] |
| Unsold buyout inventory | ~32,000 companies, ~$3.8tn; average hold at exit ~7y; ~40% held >5y | 2025 | Bain 2026 [S] |
| 2017–2021 vintages vs historical DPI benchmark | Below in every year | 2025 | Bain 2026 [S] |
| 2025 buyout deal value / exit value | $904bn (+44%) / $717bn (+47%) | 2025 | Bain 2026 [S] |
| Secondary volume | ~$121bn H1 2026 (+19% YoY): GP-led $65bn, LP-led $56bn. FY2025 >$226bn | H1 2026 | Evercore Jul 2026 [S] |
| LP pricing | High-quality buyout ~90% of NAV ("in the 90s"); quality senior credit at par or better; VC/growth softer | H1 2026 | Evercore [S] |
| Average LP portfolio pricing | 89% of NAV in 2024. Reported 87% in H1 2026 | 2024 / H1 2026 | Jefferies (May 2025) [S]; H1 2026 figure from search index only (image-only PDF) |
| Secondary buyers' target returns | Infrastructure 13–15% net IRR; venture 20%+ net | H1 2026 | Evercore [S] |
| Buyer vs seller returns in LP secondaries | Buyers' PME 1.023 vs sellers' 0.976: ~5 pp/yr; ~3 pp for funds aged 4–9 [corrected 2026-10-18: sellers' 0.974 was the working-paper figure] | 2006–2014 transaction data [corrected 2026-10-18: was 2006–2017] | Nadauld et al. 2019 [S] |
| Capital market assumptions | US large cap 7.5%, global core RE 7.9%, global infrastructure 7.1% (10–15y) | Data as of Sep 2026 | J.P. Morgan 2027 LTCMA [S] |
| Global 60/40 expected real return | 3.4% ("risk premia are compressed") | 31 Dec 2025 | AQR 2026 CMA [S] |

---

## 5. Practitioner and peer practice, and case studies

1. **Secondary buyers already "fuse" for a living [P].** They re-underwrite GP forecasts bottom-up, haircut exit values and timing, and discount at target returns (13–15% infra, 20%+ VC in H1 2026 [S]). The gap between buyer and seller returns, about 5 pp a year [S], is the price of information and liquidity that ADIC either pays when selling or captures when buying. The FBE should compute ADIC's own forward distribution *before* reading the bid. That prevents anchoring on the bid and lets the IC see the bid's implied buyer IRR.
2. **LP pacing models** (Takahashi & Alexander 2002†, the "Yale model") project calls and distributions from growth, bow and yield parameters. Common practice feeds them GP marks and house forecasts unadjusted [P]. The FBE should supply *posterior* growth and timing parameters per fund. That is the hand-off to the DPI cash-flow stream.
3. **Public infrastructure appraisal** (UK HM Treasury / DfT) institutionalized reference-class uplifts that shrink as evidence accumulates [S]. This is the template for the default underwriting haircut and its "mitigation" schedule.
4. **Weather services** have post-processed raw model output statistically since the US NWS developed MOS [S: Glahn & Lowry 1972]. MOS was conceived in 1965 and first issued in 1968 [unverified: these dates rested on a Wikipedia page, now replaced, and Glahn & Lowry's abstract does not state them]. Ensemble MOS calibrates both mean and spread [S: Gneiting et al. 2005]. Read "strategy-group forecast" as "raw model output".
5. **Insurers** price with Bühlmann credibility and reserve with BF/Benktander. These are among the most audited Bayesian procedures in finance [S].
6. **Banks** backtest risk models with the Basel "traffic light" [S: BCBS 1996]. The same binomial test applies to how often deals breach their downside cases.
7. **Case vignette (ADIC prior work).** The v8 deck's memo-corpus mining found that leverage above 6× EBITDA, reliance on multiple expansion and weak downside cases preceded failures. It also found distribution timing was "repeatedly too optimistic after spread shocks and exit-window closures". Those findings are bias covariates (§6.7) and a timing-bias term. They are the first calibration targets.

---

## 6. Design implications for the ADIC framework

### 6.1 Inputs and state variables (per asset i, as-of date t)

| Variable | Definition |
|---|---|
| k(i), g(i), v(i) | Strategy class; forecasting group; vintage |
| τᵢ, sᵢ | Age (years since first draw); NAV staleness (quarters) |
| PIᵢ, Dᵢ, Vᵢ, Uncalledᵢ | Paid-in, distributions to date, reported NAV, unfunded commitment |
| u = (M_u, IRR_u, T_u, downside, upside) | Underwriting cases from the memo (point-in-time) |
| f = (M_f or remaining CFs, T_f, range S_f) | Current forecast with its range and timestamp |
| β_k, Δm | Strategy beta to public comparables; comparables return since the last NAV date |
| z_t | Regime state from the State/Fragility engine |
| x_i | Bias covariates: entry leverage, share of value creation from multiple expansion, GP fundraising status, hold versus T_u, plan shortfall (u − a), revision history |
| θ_g = (α_{j,g}, β_{j,g}, ω_{j,g}) | Calibrated per-group, per-source bias, slope and noise (from §6.7) |

### 6.2 Translation layer

- **Nowcast NAV:** V*_t = V_{t−s}·exp(β̃_k·Δm_{t−s→t} − ψ_k), where ψ_k is a calibrated NAV-bias correction (for example, a fundraising-window adjustment). Use a Brown–Ghysels–Gredil-style state space in production.
- **Forecast to forward:** ρ_f = (1/H_f)·ln(R_f/V*_t), with R_f = M_f·PI − D (or solve the forward-IRR equation of §2.2 with calls). Floor H_f at 1 year.
- **Underwriting to forward**, using the *growth* interpretation: ρ_u = ln(M_u)/T_u. Compute the *catch-up* rate ρ_u^catch = ln(M_u·PI/V*)/(T_u − τ) for diagnosis only. Treat underwriting as expired when τ > T_u + 1.
- **Actual to forward** (market-adjusted momentum): α̂ᵢ = [ln TVPIᵢ − β_k·ln(Market_t/Market_{t₀})]/τ, and ρ_a = β_k·E[r_m] + α̂ᵢ. Ignore it when τ < 3 because of the J-curve (credibility close to 0).
- **Market-implied** (when a bid π exists): ρ_π = (1/H)·ln(R̂/(π·V)). This gives the buyer's required return. It is a diagnostic, not a signal of expected cash flows (bids are adversely selected).

### 6.3 Prior (outside view)

  μᵢ ~ N(m_k(τ, z_t), σ_k²),  with m_k(τ, z) = m_k⁰ + δ_k(τ) + γ_k(z)

- m_k⁰ is anchored on house CMAs (e.g., JPM 2027 LTCMA: infrastructure 7.1%, core real estate 7.9% [S]) and ADIC's own development triangles.
- δ_k(τ) declines after about year 7 for buyout [S: Bain 2026].
- γ_k(z) is the regime tilt from the State engine.
- σ_k is the dispersion of *true expected* returns (Bühlmann's VHM). The firm-level buyout interquartile spread of 8.03 pp implies σ ≈ 8.03/(2 × 0.674) ≈ 6% [S-derived]. Use about 6% for buyout fund interests and 6–8% for single deals; 5% firm-level for VC, inside a skewed mixture; 2–3% for core infrastructure and real estate [I].

### 6.4 Signal equations and default parameters

  s_j = α_j + β_j·μᵢ + ε_j,  ε ~ N(0, Ω),  Ω_jl = ρ_jl·ω_j·ω_l,  j ∈ {f, u, a, (IC views)}

| Parameter | Default (buyout) | Basis |
|---|---|---|
| α_f (forecast optimism, log pa) | +0.03, prior N(0.03, 0.02²) | [I] synthesized from §4.1–4.5 and ADIC's QDD timing finding; replace with ADIC MZ estimates |
| β_f | 1.0 (allow >1 for overreaction) | [S] Bordalo et al. direction; size [I] |
| ω_f | 0.06; heteroscedastic ω_f² = c + d·S_f² | EMOS form [S: Gneiting et al. 2005]; values [I] |
| α_u | +0.05 (in-house deals; +0.02 core infrastructure) | [I], consistent with GKM targets, Bain "12 is the new 5", Green Book |
| ω_u(τ) | √(0.06² + 0.0006·τ); expired when τ > T_u + 1 | [I] |
| ω_a(τ) | √(σ_idio²/τ + (σ_mark/τ)² + σ_np²), with σ_idio 0.25, σ_mark 0.15, σ_np 0.05 | σ_idio from BGG total risk [S]; rest [I] |
| ρ_fu, ρ_fa, ρ_ua | 0.5, 0.3, 0 | [I]; estimate from history |
| Late-life α_f | +0.04 | [I]: exit-timing optimism (ADIC QDD) |
| t (Mack volatility) | 0.5 until triangles exist | [S] industry rule cited by Mack 2000 |

### 6.5 Posterior, outputs and flags

**Posterior.** Let s̃_j = (s_j − α_j)/β_j and Ω̃ = D⁻¹ΩD⁻¹ with D = diag(β). Then

  Λ = σ_k⁻² + 1′Ω̃⁻¹1,  μ̂ = Λ⁻¹(m/σ_k² + 1′Ω̃⁻¹s̃),  σ̂² = Λ⁻¹.

Credibility weights are w₀ = σ_k⁻²/Λ for the prior and w = Ω̃⁻¹1/Λ for the signals. They sum to 1. Show them to the IC as "votes" [I].

**Outputs per asset:**

- μ̂, σ̂, and the 80% band for expected forward IRR.
- **P_opt = P(μᵢ < ρ_f | data) = Φ((ρ_f − μ̂)/σ̂)** and the optimism gap (ρ_f − μ̂) in bp.
- **P_miss = Φ((ρ_f − μ̂)/√(σ̂² + σ_e²/H))**. For a calibrated median forecast this is about 0.5.
- The forecast's percentile in the reference class, Φ((ρ_f − m)/σ_k).
- An exit-timing distribution.
- Posterior-predictive draws for the simulator.

**Flags (defaults [I]):**

| Flag | Trigger |
|---|---|
| F1 Optimism | P_opt > 0.90 and gap > 300 bp |
| F2 Base-rate outlier | Forecast above the 90th percentile of the reference class (or below the 10th: pessimism) |
| F3 Hockey stick / anchoring | ρ_f − IRR_SI > 1,000 bp and M_f ≥ 0.9·M_u while TVPI is more than 25% below the plan path |
| F4 Stale NAV | s > 1 quarter and \|nowcast adjustment\| > 5% |
| F5 Fundraising window | GP raising its next fund |
| F6 Expired underwriting | τ > T_u + 1 |
| F7 Low-credibility forecaster | Z_g < 0.3, or coverage traffic light yellow or red |
| F8 Revision drift | 3 or more same-sign revisions (Nordhaus test) |
| F9 Overconfident range | Stated range more than 40% narrower than the calibrated interval |
| F10 Market disagreement | \|ρ_π − μ̂\| > 400 bp |

### 6.6 Maturity credibility for fund interests (BF / Benktander module)

Development triangles of TVPI (incurred) and DPI (paid) by age, built from ADIC's history plus external benchmarks, give LDF_τ and p_τ = 1/LDF_τ. U₀ is the debiased underwriting or reference class. Compute U_CL, U_BF, U_GB and U_c* = c*·U_CL + (1−c*)·U_BF with c* = p/(p+t). Convert to a forward return with ρ = ln((U − DPI)/NAV*)/H.

This module produces the "actual" signal for fund interests in place of the raw momentum signal. It makes the J-curve treatment explicit: when p is low, BF dominates [I].

### 6.7 Calibrating from ADIC's 18-year memo corpus

1. **Extract.** Use the dual-LLM extraction plus reconciliation from the prior work, with human audit samples. For each deal: date, team, strategy, base/downside/upside MOIC, IRR and hold; entry multiple and leverage; value-creation bridge (growth / multiple / deleveraging); exit route. Then add every subsequent valuation memo and re-forecast. Track the field-level extraction error rate and propagate it as measurement noise.
2. **Link** each deal to the cash-flow ledger and quarterly NAVs. Build three archives:
   - (a) underwriting → outcome pairs;
   - (b) forecast-revision panels;
   - (c) development triangles.
3. **Model** the debiased error of source j for asset i at vintage v with a hierarchical regression [I]:

  e_ij = y_i − s_ij = −α_{j,g} − x_i′γ_j − δ_v + η_ij,  α_{j,g} ~ N(α_j⁰, τ_j²),  δ_v ~ N(0, τ_v²)

   The vintage random effect δ_v keeps common market surprises (2008, 2022) from being booked as forecaster bias. Extend to EMOS for spreads, and add a survival model of exit timing (hazard ratio of realized versus forecast hold).
4. **Censoring.** Unexited deals enter through BF/CL-developed ultimates with their uncertainty, or a censored likelihood. Exited deals alone are biased, because winners exit early.
5. **Leakage.** Use only point-in-time memos (bitemporal store). Down-weight old vintages, for example with an 8-year half-life [I], or use regime covariates.
6. **Effective sample size.** Clustering by vintage reduces information: n_eff = n/(1 + (m−1)·ICC). The credibility of a group-specific bias is then Z = n_eff/(n_eff + σ_e²/τ_g²) (Example 5).
7. **Downside-case calibration.** If the downside is meant as a P10, breaches should follow Binomial(N, 0.10). Apply Basel zones: green if the cumulative probability is below 95%, red from 99.99% [S: BCBS 1996].

### 6.8 Worked examples (all hypothetical; computed with the equations above)

**Example 1: buyout co-invest, behind plan, hockey-stick forecast.**

Inputs:

- 100 invested at t₀; τ = 5.0; NAV 154 (TVPI 1.54x, IRR_SI 9.0%).
- Underwritten 2.5x over 5 years (IRR 20.1%; ρ_u = 0.1833).
- Forecast 2.3x at year 7: forward multiple 1.494x over 2 years, so forward IRR 22.2% (ρ_f = 0.2006).
- Comparables +45% over 5 years with β = 1, so α̂ = +1.2% pa. With E[r_m] = 6.5%, ρ_a = 0.077.
- Prior m = 0.100, σ_k = 0.06.

Debiased signals: f 0.1706 (ω 0.060), u 0.1333 (ω 0.081), a 0.0770 (ω 0.126).

| Fusion | μ̂ (IRR) | σ̂ | Weights prior / f / u / a | P_opt | Gap | P_miss | 80% band (IRR) |
|---|---|---|---|---|---|---|---|
| Independent errors | 0.1301 (13.9%) | 0.036 | 36 / 36 / 20 / 8 % | 97.5% | 704 bp | 62.8% | 8.8–19.3% |
| Correlated (ρ_fu 0.5, ρ_fa 0.3) | **0.1274 (13.6%)** | **0.041** | **47 / 35 / 13 / 6 %** | **96.3%** | 732 bp | 63.3% | **7.8–19.7%** |

Reading the result:

- The forecast sits at the 95th percentile of the reference class of expected returns.
- Flags: F1, F2 and F3. The plan-path shortfall is 38%, yet the forecast multiple is 92% of underwriting.
- Correlation matters. Treating the sources as independent overstates precision (σ̂ 0.036 vs 0.041) and gives too much weight to underwriting.
- LEVER/REFI gate: P(μ < 9% all-in recap cost) = 15.8%.

**Example 2: core-plus infrastructure (well-behaved).**

Inputs:

- m = ln(1.081): LTCMA 7.1% plus a 100 bp core-plus premium [I]; σ_k = 0.02.
- u: 9.0% (α 0.015, ω 0.038). a: 0.0736 (ω 0.066). f: 9.5% (α 0.010, ω 0.025).

Result: posterior 8.15% (σ̂ 0.016). Weights are 60/32/6/2. P_opt = 79%, with a gap of 124 bp. No flag: the forecast is mildly rich but inside tolerance.

**Example 3: late-life buyout fund LP interest, SELL vs HOLD.**

Inputs:

- Reported NAV 400 (30 Jun 2026); τ = 9.5; TVPI 1.55x; IRR_SI 9.5%.
- Comparables −6% in Q3 (hypothetical), so nowcast V* = 376.0.
- Forecast: 480 of remaining distributions over about 2.5 years. That is 1.20x on reported NAV (7.6% forward IRR) but 1.277x on nowcast NAV (10.3%).
- Prior m = ln(1.08)/2.5 = 0.031, σ_k 0.05. Late-life α_f = 0.04, ω_f = 0.05. Underwriting expired.

Results:

- Posterior μ̂ = 0.0421 (4.3% IRR), σ̂ = 0.034. Weights 47/42/11. P_opt = 94.7%.
- Hold value at ADIC's opportunity-cost hurdle h = 9% [I], with σ_e = 15% pa:
  - E[R] = 431.3 (median 417.8), so **PV_hold = 347.7**.
  - At forecast face value, PV = 387.0.
  - The **bid is 88% of reported NAV = 352.0**, or 93.6% of nowcast. This is consistent with high-quality buyout pricing around 90% [S].
- Break-even remaining value is 436.6 (1.092x reported NAV). P(R ≥ break-even) = 43.1%.
- The buyer earns 13.2% if the forecast is right, and 7.1% at our median.
- **What you need to believe:** HOLD breaks even only if the group's late-life bias is ≤ 2.8% pa (posterior mean ≥ 4.71%).
- A 2% liquidity shadow value from the liquidity engine (effective bid 359) makes it a SELL.
- Since-inception IRR and TVPI play no role in the decision.

**Example 4: growth fund at age 4 (BF/Benktander).**

Inputs: TVPI 0.95x (DPI 0.10, NAV 0.85); underwriting 2.2x, debiased to U₀ = 1.76x [I]; LDF₄ = 1.30, so p = 0.769.

| Estimate | Ultimate TVPI | Forward IRR on NAV over 5 years |
|---|---|---|
| U_CL | 1.235x | 6.0% |
| U_BF | 1.356x | 8.1% |
| U_GB | 1.263x | 6.5% |
| U_c* (t = 0.5, c* = 0.606) | 1.283x | 6.8% |
| Group forecast 1.9x | 1.9x | 16.2% (F2/F3) |
| Underwriting 2.2x | 2.2x | 19.8% |

**Example 5: credibility of a group's bias.**

Inputs: 64 resolved forecasts over 16 vintages (m = 4 per vintage). Mean error +4.5%; σ_e = 12%; ICC 0.3.

- Design effect 1.9, so n_eff = 33.7.
- Population prior: a₀ = 3%, τ_g = 2%, so k = 36 and **Z = 0.48**.
- Credibility bias = 3.73%, with a posterior sd of 1.44%. That uncertainty is common to every asset the group forecasts (§6.9).
- **Range calibration:** stated 80% ranges that contain 52% of outcomes need widening ×1.81. At 36% coverage (Ben-David et al.) the factor is ×2.74.
- **Traffic light** (N = 40 downside cases intended as P10): green 0–6 breaches, yellow 7–11, red ≥ 12.

### 6.9 Interfaces to the optimizer and simulator

- **Belief state.** The multi-period optimizer's state carries (μ̂ᵢ, σ̂ᵢ) and updates them each quarter with a Kalman recursion: μ_{t+1} = m + φ(μ_t − m) + η_t, observed through nowcast NAV returns, revisions and cash flows. This is a belief-state MDP (POMDP). It gives HOLD its real option value of learning, because σ̂ shrinks with maturity [I].
- **Simulation.** Draw μᵢ once per path, not per period. Add a **common group-bias shock** ε_g ~ N(0, sd(α_g)²) loaded on every asset in group g, scaled by w_f,i. Otherwise portfolio-level forecast risk appears falsely diversified [I]. To impose fused beliefs on the existing 50k-path scenario set without re-simulating, use entropy pooling: p* ∝ p₀·exp(λ′g(x)) [†Meucci 2008].
- **Decision rules.** All rules are in posterior terms, which neutralizes the optimizer's curse [S].
  - **SELL** if π·V·(1 + λ_liq) > E[PV_h(R) | data] + switching costs.
  - **REFINANCE / LEVER** only if P(μᵢ < c_debt + spread) < ε (for example 10%) *and* the downside-quantile LTV passes.
  - **Re-underwrite** (value of information) when |PV_hold − bid|/PV < 5% and σ̂ is large. Use the knowledge-gradient logic of Powell & Ryzhov† [I].
- **Objective and constraints.** Tier 2 uses posterior expected forward returns. Tier 1 robustness should use the lower posterior quantile (e.g., q₁₀ of μᵢ) and stress α_g at +2 sd. λ_liq comes from the liquidity / DPI stream.
- **Calibration targets.** PIT histograms within 95% bands; 80% interval coverage of 75–85%; MZ slope 0.9–1.1; CRPS skill against the reference-class prior > 0; traffic lights green.

### 6.10 IC diagnostics

- **Belief card per asset.** u, a and f on the forward basis next to the base rate and the posterior band. A credibility "votes" bar. P_opt, P_miss and flags. "What you need to believe". The bid's implied buyer IRR.
- **Group scorecard.** Bias, MZ slope, coverage, CRPS skill, n_eff, CUSUM state (k = 0.5, h = 5; in-control ARL ≈ 465, textbook values†), and traffic light.
- **Reliability diagram and PIT histogram** per group. **Development-triangle chart** of TVPI by age and vintage against underwriting.
- **IC members as forecasters.** Views are entered as signals with confidence, through the Black–Litterman mapping (Ω from confidence†), and recorded. Members are scored over time with Cooke/CRPS weights. The IC's own credibility is learned.

### 6.11 Agent roles (hand-off to the architecture stream)

LLMs extract, retrieve, challenge and explain. Deterministic code owns every number. Each stage carries a rubric check, as in Sakana's orchestration [I]. The agents:

- **Translator:** units, gross/net, dates.
- **Reference-class librarian:** class choice, plus sensitivity to that choice.
- **Calibration agent:** quarterly hierarchical refit and scorecards.
- **Fusion engine:** deterministic.
- **Challenger:** failure analogues for flagged assets; requests evidence from the group.
- **IC briefer:** citation-traced belief cards.

---

## 7. Implementation notes

**Python stack** (versions as observed Sep–Oct 2026):

| Need | Tools |
|---|---|
| Fusion and constrained weights | numpy / scipy; cvxpy for w ≥ 0 and shrinkage |
| Hierarchical models | PyMC, NumPyro or CmdStanPy, plus ArviZ (R-hat, ESS, PSIS-LOO for stacking); statsmodels MixedLM for fast empirical Bayes |
| State space / nowcasting | statsmodels.tsa.statespace |
| Scoring | `scoringrules` 0.11.0 (Jun 2026: CRPS, log, energy, threshold-weighted CRPS) [S] |
| Reserving | `chainladder` 0.10.1 (Sep 2026; CAS-supported) for triangles and IBNR-style methods [S] |
| Exit timing | lifelines / scikit-survival |
| Conformal | MAPIE |
| Drift detection | river (ADWIN, Page–Hinkley) |
| Cash-flow IRRs | pyxirr |

**Complexity.** The per-asset posterior is O(J³) with J ≤ 6, so microseconds. The hierarchical refit takes minutes to hours on 10⁴ forecast–outcome rows, run quarterly. Simulator draws are O(paths × assets) with on-the-fly generation.

**Numerical pitfalls:**

- IRR has multiple roots or blows up. Work in log multiples and XIRR with bracketing, floor H at 1 year and handle NAV ≈ 0 in dollars.
- Jensen's inequality. E[e^{ρH}] = e^{μH + ½Var}; Example 3's convexity term is about 3%.
- Gross vs net and currency mismatches between u (often gross) and f (often net).
- Timestamp misalignment and look-ahead.
- Negative GLS weights.
- Singular Ω. Use Ledoit–Wolf shrinkage.
- The posterior feeding back into marks. Keep the valuation function independent of the FBE.

---

## 8. Risks, pitfalls and limitations

- **Small samples and regime change.** 18 years contains perhaps 2–3 credit cycles, and the drivers of return have changed ("12 is the new 5"). Literature priors must carry real weight. Report sensitivity to them.
- **Shrinkage penalizes true outliers.** Use heavy-tailed (Student-t) priors, so that strong evidence escapes shrinkage, plus a documented override log.
- **Goodhart and gaming.** Scoring changes behaviour. Proper scoring rules make honest forecasts optimal, but sandbagging or range-padding is possible. Score sharpness as well as calibration.
- **Reference-class choice is itself a model.** The librarian agent must show the sensitivity.
- **Adverse selection** in secondary bids and in which assets get forecast attention.
- **Political acceptance.** Strategy groups may see the FBE as a judgment on them. Co-design the scorecards with the groups.
- **Research limitation.** The shared web-search budget was exhausted mid-session. Several references are cited from memory (†). The PitchBook R² values and the Jefferies H1 2026 pricing figure come from search-index summaries. Jenkinson et al. (2013) is cited from abstract text, because the SSRN page was blocked. Verify these before external use.
- **Parameters marked [I] are design defaults, not estimates.** In particular α, ω, ρ and σ_k for deals must be replaced by ADIC-calibrated values.

---

## 9. Open questions

1. Does ADIC hold *point-in-time* historical forecasts, or only current ones? This determines whether forecaster credibility can be learned or must start from priors.
2. In ADIC's data, how much realized deal-level alpha persists, and how much does past performance at the same age predict future performance?
3. Are underwritten returns in the memos gross or net, and are definitions consistent across 18 years and across teams?
4. Is optimism pro-cyclical? Should α be regime-conditional through the State engine?
5. What is the right SELL hurdle: the α* funding basket, the cost of NAV financing, or the marginal value of liquidity from the distribution-policy stream?
6. Should IC members' views be scored and weighted? What is the governance for that?
7. For co-investments that sit alongside fund positions with the same GP, how should correlated forecast errors be modelled across the two exposures?
8. Which external base-rate datasets (Burgiss/MSCI, Cambridge, Preqin) can ADIC license for development triangles at deal level?

---

## 10. References

(† = cited from memory, not re-verified online in this session.)

1. Andonov, A. & Rauh, J. (2018). The Return Expectations of Institutional Investors. Stanford GSB WP 3659. https://www.gsb.stanford.edu/faculty-research/working-papers/return-expectations-institutional-investors (later published as "The Return Expectations of Public Pension Funds", *RFS* 2022†)
2. Arkes, H. & Blumer, C. (1985). The psychology of sunk cost. *OBHDP* 35(1):124–140.
3. Bain & Company (2026). Global Private Equity Report 2026. https://www.bain.com/insights/topics/global-private-equity-report/ ; https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ ; https://www.bain.com/insights/welcome-to-a-new-era-global-private-equity-report-2026/
4. Barber, B. & Yasuda, A. (2017). Interim fund performance and fundraising in private equity. *JFE* 124(1):172–194. https://escholarship.org/uc/item/01h178mf
5. Baron, J., Mellers, B., Tetlock, P., Stone, E. & Ungar, L. (2014). Two reasons to make aggregated probability forecasts more extreme. *Decision Analysis* 11(2).
6. Basel Committee on Banking Supervision (1996). Supervisory framework for the use of "backtesting"… (4 Jan 1996). https://www.bis.org/publ/bcbs22.htm
7. Bates, J. & Granger, C. (1969). The combination of forecasts. *Operational Research Quarterly* (now *Journal of the Operational Research Society*) 20(4):451–468. DOI 10.1057/jors.1969.103.
8. Ben-David, I., Graham, J. & Harvey, C. (2013). Managerial miscalibration. *QJE* 128(4):1547–1584. https://www.nber.org/papers/w16215
9. Black, F. & Litterman, R. (1992). Global portfolio optimization. *FAJ* 48(5):28–43.†
10. Blanc, S. & Setzer, T. (2020). Bias–variance trade-off and shrinkage of weights in forecast combination. *Management Science* 66(12):5720–5737. https://pubsonline.informs.org/doi/10.1287/mnsc.2019.3476
11. Bordalo, P., Gennaioli, N., La Porta, R. & Shleifer, A. (2019). Diagnostic expectations and stock returns. *JF* 74(6):2839–2874. https://www.nber.org/papers/w23863
12. Bornhuetter, R. & Ferguson, R. (1972). The actuary and IBNR. *PCAS* 59:181–195. https://www.casact.org/abstract/actuary-and-ibnr
13. Boyer, B., Nadauld, T., Vorkink, K. & Weisbach, M. (2018). Private equity indices based on secondary market transactions. NBER WP 25207. https://www.nber.org/papers/w25207
14. Brown, G., Ghysels, E. & Gredil, O. (2023). Nowcasting net asset values: The case of private equity. *RFS* 36(3):945–986. DOI 10.1093/rfs/hhac045. (The UNC page https://uncipc.org/publication/nowcasting-net-asset-values-the-case-of-private-equity/ carries the 2020 working-paper abstract, whose figures differ.)
15. Brown, G., Gredil, O. & Kaplan, S. (2019). Do private equity funds manipulate reported returns? *JFE* 132(2):267–297. https://www.nber.org/papers/w22493
16. Bühlmann, H. (1967). Experience rating and credibility. *ASTIN Bulletin* 4(3):199–207. DOI 10.1017/S0515036100008989. (DOI 10.1017/S0515036100008023 is a different paper with the same title: Bühlmann 1969, *ASTIN Bulletin* 5(2):157–165.)
17. Bühlmann, H. & Straub, E. (1970). Glaubwürdigkeit für Schadensätze. *Mitt. VSVM* 70:111–133.†
18. Cambridge Associates (2018). Portfolio Benchmarking Best Practices for Private Investments. https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2018/05/PI-Portfolio-Benchmarking-Best-Practices.pdf
19. Claeskens, G., Magnus, J., Vasnev, A. & Wang, W. (2016). The forecast combination puzzle: A simple theoretical explanation. *IJF* 32(3):754–762. https://repub.eur.nl/pub/81568
20. Clemen, R. (1989). Combining forecasts: A review and annotated bibliography. *IJF* 5(4):559–583. https://people.duke.edu/~clemen/bio/Published%20Papers/13.CombiningReview-Clemen-IJOF-89.pdf
21. Cooke, R. (1991). *Experts in Uncertainty*. OUP. Classical-model performance evidence: Colson, A. R. & Cooke, R. M. (2017). Cross validation for the classical model of structured expert judgment. *Reliability Engineering & System Safety* 163:109–120. DOI 10.1016/j.ress.2017.02.003.
22. Diebold, F., Gunther, T. & Tay, A. (1998). Evaluating density forecasts, with applications to financial risk management. *IER* 39:863–883. https://www.nber.org/papers/t0215
23. Diebold, F. & Pauly, P. (1990). The use of prior information in forecast combination. *IJF* 6(4):503–508.
24. Diebold, F. & Shin, M. (2019). Machine learning for regularized survey forecast combination: Partially-egalitarian LASSO and its derivatives. *IJF* 35(4):1679–1691 (online 2018). DOI 10.1016/j.ijforecast.2018.09.006. Related working paper "Beating the Simple Average: Egalitarian LASSO for Combining Economic Forecasts": https://economics.sas.upenn.edu/node/10513
25. Efron, B. & Morris, C. (1975). Data analysis using Stein's estimator and its generalizations. *JASA* 70(350):311–319 (details†). https://chance.amstat.org/?p=8791 (context)
26. Evercore (2026). H1 2026 Secondary Market Review (July 2026). https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf
27. Flyvbjerg, B. (2006). From Nobel Prize to project management: Getting risks right. *Project Management Journal* 37(3):5–15. https://arxiv.org/abs/1302.3642
28. Flyvbjerg, B., Skamris Holm, M. & Buhl, S. (2005). How (in)accurate are demand forecasts in public works projects? *JAPA* 71(2):131–146. https://arxiv.org/abs/1303.6654. Note: the article carries a Notice of Redundant Publication (*JAPA* 78(3):352, 2012), because a 2006 *Transport Reviews* duplicate, since retracted, reproduced it. The *JAPA* article itself stands.
29. Gibbs, I. & Candès, E. (2021). Adaptive conformal inference under distribution shift. https://arxiv.org/abs/2106.00170
30. Glahn, H. & Lowry, D. (1972). The use of model output statistics (MOS) in objective weather forecasting. *J. Appl. Meteor.* 11(8):1203–1211. DOI `10.1175/1520-0450(1972)011<1203:TUOMOS>2.0.CO;2`.
31. Gneiting, T. & Raftery, A. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102(477):359–378.
32. Gneiting, T., Balabdaoui, F. & Raftery, A. (2007). Probabilistic forecasts, calibration and sharpness. *JRSS-B* 69(2):243–268.
33. Gneiting, T., Raftery, A., Westveld, A. & Goldman, T. (2005). Calibrated probabilistic forecasting using ensemble MOS and minimum CRPS estimation. *Monthly Weather Review* 133(5):1098–1118.
34. Gompers, P., Kaplan, S. & Mukharlyamov, V. (2016). What do private equity firms say they do? *JFE* 121(3):449–476. https://nber.org/papers/w21133 ; draft: https://m.nber.org/conferences/2015/PRs15/Gompers_Kaplan_Mukharlyamov.pdf
35. Gupta, A. & Van Nieuwerburgh, S. (2019/2021). Valuing private equity strip by strip. NBER WP 26514 (*JF* 2021). https://www.nber.org/papers/w26514
36. Harris, R., Jenkinson, T., Kaplan, S. & Stucke, R. (2020). Has persistence persisted in private equity? NBER WP 28109 (*JCF* 2023). https://www.nber.org/system/files/working_papers/w28109/w28109.pdf
37. HM Treasury (2003; published online 21 Apr 2013). Supplementary Green Book Guidance: Optimism Bias. https://www.gov.uk/government/publications/green-book-supplementary-guidance-optimism-bias
38. Ilmanen, A., Chandra, S. & McQuinn, N. (2019). Demystifying illiquid assets: Expected returns for private equity. *JAI*. https://www.aqr.com/Insights/Research/Journal-Article/Demystifying-Illiquid-Assets-Expected-Returns-for-Private-Equity
39. AQR (2026). 2026 Capital Market Assumptions for Major Asset Classes (14 Jan 2026). https://www.aqr.com/Insights/Research/Alternative-Thinking/2026-Capital-Market-Assumptions-for-Major-Asset-Classes
40. J.P. Morgan Asset Management (2026). 2027 Long-Term Capital Market Assumptions (data as of Sep 2026). https://am.jpmorgan.com/us/en/asset-management/adv/insights/portfolio-insights/ltcma/
41. Jefferies (2025). Secondaries get a second wind (16 May 2025). https://www.jefferies.com/insights/markets/secondaries-get-a-second-wind/ ; H1 2026 review: https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf (figures not machine-readable)
42. Jenkinson, T., Sousa, M. & Stucke, R. (2013). How fair are the valuations of private equity funds? SSRN 2229547. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2229547
43. Jenkinson, T., Landsman, W., Rountree, B. & Soonawalla, K. (2020). Private equity net asset values and future cash flows. *The Accounting Review* 95(1):191–210. https://ora.ox.ac.uk/objects/uuid:691dbf3a-2fb2-4156-8d12-967cdf89301e
44. Kahneman, D. & Lovallo, D. (1993). Timid choices and bold forecasts. *Management Science* 39(1):17–31. https://iaorifors.com/paper/10039
45. Korteweg, A. & Sorensen, M. (2017). Skill and luck in private equity performance. *JFE* 124(3):535–562. https://research-api.cbs.dk/ws/files/55394727/morten_soerensen_skill_and_luck_in_private_equity_performance_acceptedversion.pdf
46. Lovallo, D., Clarke, C. & Camerer, C. (2012). Robust analogizing and the outside view. *SMJ* 33(5):496–512. https://authors.library.caltech.edu/30252
47. Mack, T. (2000). Credible claims reserves: The Benktander method. *ASTIN Bulletin* 30(2):333–347. https://www.casact.org/library/astin/vol30no2/333.pdf
48. Meucci, A. (2008). Fully flexible views: Theory and practice. *Risk* 21(10).† SSRN 1213325.
49. Mincer, J. & Zarnowitz, V. (1969). The evaluation of economic forecasts. In J. Mincer (ed.), *Economic Forecasts and Expectations: Analysis of Forecasting Behavior and Performance*, NBER, pp. 3–46. https://www.nber.org/chapters/c1214.pdf
50. Nadauld, T., Sensoy, B., Vorkink, K. & Weisbach, M. (2019). The liquidity cost of private equity investments: Evidence from secondary market transactions. *JFE* 132(3):158–181 (DOI 10.1016/j.jfineco.2018.11.007). Figures follow the published abstract; the NBER link is working paper w22404: https://www.nber.org/papers/w22404
51. Nordhaus, W. (1987). Forecasting efficiency: Concepts and applications. *REStat* 69(4):667–674.
52. PitchBook. Manager Performance Scoring (methodology). https://files.pitchbook.com/website/files/pdf/PitchBook_Manager_Performance_Scoring.pdf (403; figures via search index)
53. Powell, W. & Ryzhov, I. (2012). *Optimal Learning*. Wiley.†
54. Quarg, G. & Mack, T. (2004). Munich chain ladder. *Blätter der DGVFM* 26(4).†
55. Smith, J. & Winkler, R. (2006). The optimizer's curse: Skepticism and postdecision surprise in decision analysis. *Management Science* 52(3):311–322. DOI 10.1287/mnsc.1050.0451. https://fds.duke.edu/db/aas/stat/faculty/bob.winkler/publications/278471
56. Smith, J. & Wallis, K. (2009). A simple explanation of the forecast combination puzzle. *Oxford Bulletin of Economics and Statistics* 71(3):331–355. DOI 10.1111/j.1468-0084.2008.00541.x.
57. Takahashi, D. & Alexander, S. (2002). Illiquid alternative asset fund modeling. *Journal of Portfolio Management* 28(2):90–100.†
58. Timmermann, A. (2006). Forecast combinations. *Handbook of Economic Forecasting* Vol. 1, ch. 4 (pages†).
59. Wang, X., Hyndman, R., Li, F. & Kang, Y. (2023). Forecast combinations: An over 50-year review. *IJF* 39(4):1518–1547. https://arxiv.org/abs/2205.04216
60. Yao, Y., Vehtari, A., Simpson, D. & Gelman, A. (2018). Using stacking to average Bayesian predictive distributions. *Bayesian Analysis* 13(3) (DOI 10.1214/17-BA1091). https://arxiv.org/abs/1704.02030
61. Other background cited from memory†: Staw (1976) "Knee-deep in the big muddy", *OBHP* 16(1) (verified by the 2026-10-18 literature audit; no dagger); Guler (2007), *ASQ* 52(2); Shefrin & Statman (1985), *JF* 40(3); Tetlock (2005) *Expert Political Judgment*; Mellers et al. (2014), *Psychological Science* 25(5); Kalman (1960); Hoeting et al. (1999), *Statistical Science* 14(4); Idzorek (2005) on Black–Litterman confidences; Page (1954) on CUSUM.
62. Python packages: scoringrules https://pypi.org/project/scoringrules/ ; chainladder https://pypi.org/project/chainladder/

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2; `research/literature/07_return_fusion.lit.md` §2; `research/literature/recheck/10_scenarios_robustness.recheck.md`. Metadata confirmed on Crossref or OpenAlex where noted.

- §4.5 and §3 (Cooke row): "performance weights won in 26 of 33 studies in-sample" corrected. Colson & Cooke (2017) report 32 of 33 in-sample; 26 of 33 is the out-of-sample validity-index result, and out-of-sample statistical accuracy is below equal weighting's. Now sourced to Colson & Cooke; "320 experts" marked unverified (synthesis §2.3).
- §4.2: Brown–Ghysels–Gredil figures replaced with the published *RFS* abstract values (beta ≈1.0 buyout / 1.4 venture; total risk ≈33% / 40%). The old 1.05/1.20, 38% and "10 and 13 pp" figures are labelled as 2020 working-paper values (synthesis §2.3; Crossref 10.1093/rfs/hhac045).
- §4.6: Nadauld et al. sellers' PME changed from 0.974 to 0.976, as in the published *JFE* abstract (confirmed on IDEAS/RePEc). Data period changed from 2006–2017 to 2006–2014 (synthesis §2.3; lit row 30).
- §2.3: Bates & Granger (1969) now credited with weights for a pair of forecasts; the matrix form is attributed to later work (lit row 1; verification R12).
- §2.7: Mincer–Zarnowitz and Nordhaus tags changed from [†] to [S]. Both works exist (synthesis §2.2 items 6–7).
- §2.7, §3 (EMOS row), §5 item 4, §6.4 (ω_f row): Gneiting & Raftery, Gneiting–Balabdaoui–Raftery and Gneiting et al. (2005) tags changed from † to [S]. The MOS origin is now sourced to Glahn & Lowry (1972) (lit rows 13–15, 17).
- §5 item 4: the MOS dates (1965 conceived, 1968 first issued) are marked unverified. They rested only on the Wikipedia page, and Glahn & Lowry's abstract does not state them (OpenAlex abstract checked).
- §1, §2.3, §2.6, §4.5: daggers removed from the in-text citations of Arkes & Blumer, Diebold & Pauly, Staw and Baron et al. (lit §1, "twelve † flags can be removed").
- §10 refs 2, 5, 10, 23, 31, 32, 33, 35 and 51: daggers removed (Arkes & Blumer; Baron et al.; Blanc & Setzer; Diebold & Pauly; the three Gneiting papers; Gupta & Van Nieuwerburgh; Nordhaus).
- §10 ref 7 (Bates & Granger): rdrr.io link replaced with DOI 10.1057/jors.1969.103 (Crossref; synthesis §2.5).
- §10 ref 14 (Brown, Ghysels & Gredil): DOI 10.1093/rfs/hhac045 added; the UNC link is labelled as the working-paper abstract.
- §10 ref 16 (Bühlmann 1967): Wikipedia link replaced with DOI 10.1017/S0515036100008989. Crossref places that DOI at *ASTIN Bulletin* 4(3):199–207; 10.1017/S0515036100008023 is the 1969 paper of the same title, 5(2):157–165. This resolves synthesis §2.6 item 2 in G6's favour.
- §10 ref 21 (Cooke): Wikipedia link replaced with Colson, A. R. & Cooke, R. M. (2017), *RESS* 163:109–120, DOI 10.1016/j.ress.2017.02.003 (OpenAlex).
- §10 ref 24 (Diebold & Shin): "(journal details†)" replaced with 35(4):1679–1691 and DOI 10.1016/j.ijforecast.2018.09.006 (OpenAlex; lit row 5).
- §10 ref 28 (Flyvbjerg et al. 2005): note added on the Notice of Redundant Publication (*JAPA* 78(3):352, 2012). The article stands (lit row 38).
- §10 ref 30 (Glahn & Lowry): dagger and Wikipedia "MOS history" link removed; DOI added (Crossref).
- §10 ref 49 (Mincer & Zarnowitz): dagger replaced with full details: in J. Mincer (ed.), *Economic Forecasts and Expectations*, NBER, pp. 3–46, chapter c1214 (synthesis §2.2 item 6).
- §10 ref 50 (Nadauld et al.): *JFE* 132(3):158–181 added; the NBER link is labelled as the working paper.
- §10 ref 55 (Smith & Winkler): subtitle restored ("Skepticism and postdecision surprise in decision analysis") and DOI 10.1287/mnsc.1050.0451 added (Crossref; topic 10 recheck).
- §10 ref 56 (Smith & Wallis): "(details†…)" replaced with 71(3):331–355 and DOI 10.1111/j.1468-0084.2008.00541.x (Crossref).
- §10 ref 61: Staw (1976) marked as verified by the audit.
