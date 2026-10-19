# G11 · Real Assets: infrastructure

## Contracted, regulated and GDP-linked assets: cash yield, inflation pass-through, duration and leverage

**Stream:** G11 (Real Assets research, streams G10–G15). **Date:** 2026-10-18. **Author:** research stream G11. **Status:** dossier v1.0, for verification.

**Scope (context §1A re-read before finalising).**
- The user has *confirmed* Real Assets: real estate, infrastructure, and energy & natural resources (agriculture and timber excluded), held through funds, co-investments and direct assets or JVs, inside the ~60% private allocation. The working size is $18bn, with ≈$4bn unfunded.
- Design brief §9: ADIC's return series are net IRR/MOIC per holding with downside/base/upside cases, archived quarterly.
- This dossier covers infrastructure. It flags two boundaries: midstream (shared with energy & natural resources) and infrastructure debt (Private Credit).

**Evidence tags.** [S] sourced and read in session (URL in §10); [S-prior] sourced in an earlier, verified project file (file named); [P] practitioner consensus; [I] my inference or design default; [I-calc] my computation (scripts in `research/groups/addenda/G11_calcs/`); [A] client statement or working assumption; [U] unverified, never load-bearing. All model outputs are **SYNTHETIC – NOT ADIC DATA**.

**Research constraint.** The shared web-search budget ran out mid-stream. Later items were verified by fetching primary URLs and DOI records only; unverifiable claims are [U] or omitted.

---

## 1. Executive summary

**The question.** How should ADIC's infrastructure holdings be modelled so that the multi-period lab can price SELL / HOLD / REFINANCE / LEVER for each of them, and project their cash yield, value and liquidity in the states that matter? Those states are the drought, a demand bust, and today's Gulf-war supply shock.

**Twelve findings.**

1. **Segment beats label.** EDHECinfra (Q1 2021): 5-year volatility 7.3% (core) to 16.2% (airports); maximum drawdown 9.6% (wind) to 34.9% (airports) [S]. SIPA (to Sep 2025): 10-year volatility 9.3% (renewables) to 18.4% (data infrastructure) [S]. The engine uses nine archetypes, never one infrastructure beta [I].
2. **Closed-end infrastructure funds behave like PE.** 2002–2018 vintages: PME 0.93, mean net IRR 9.9%, GPME −0.257; procyclical cash flows; +10pp of early exits ↔ +2.6pp IRR [S: Andonov, Kräussl & Rauh 2021]. This confirms the interim rule: reuse the PE commitment engine, adding an income term [I].
3. **Strong recent returns; wide forward range.** MSCI private infrastructure +12.2% gross (12 months to Q1 2026); Cambridge Associates core/core-plus +10.4% net against value-add +7.9% [S]. Preqin 2010–2020 median net IRRs: core 12%, core-plus 10%, value-add 12%, opportunistic 8%, so risk has not paid [S]. Forward: J.P. Morgan 7.1% [S-prior] against SIPA 11.3% gross [S], a ≈4pp model range for the IC.
4. **Appraisals hide the risk.** Appraisal volatility is 2–3% against 7–12% market-implied [S: EDHECinfra]. MSCI shows one negative quarter since the GFC [S]. Carry economic and reported NAV separately; appraisal smoothing λ^app ≈ 0.85 a quarter for core (stream 04 used 0.6) [I-calc].
5. **Duration depends on what is held fixed.** With equity cash flows fixed, our archetypes give 7–13 [I-calc], consistent with EDHECinfra's 7.4–11.6 [S]. Under a permanent real-rate shock, refinancing at market lifts unregulated equity to 12–30; under a 5-year-half-life shock, 5–8; regulated assets with resets ≈1 [I-calc].
6. **Inflation pass-through is conditional.** Indexed revenue on nominal fixed debt gains per +1pp of expected inflation: regulated utility +13%, availability PPP +23%. Fixed-escalator assets lose: fixed-PPA renewables −27%, towers/data centres −23%, midstream −14% [I-calc]. Renewables were ≈2/3 of sector fundraising in 2025 and digital 28% of deals in H1 2026 [S], so the "inflation hedge" label fits the legacy book, not the current one [I].
7. **The worst state for values is a supply-shock stagflation.** In demand busts falling rates cushion values (EDHECinfra 2020: rates more than +5%, risk premia −9%) [S]. Synthetic sleeve, year-1 NAV P05: −11.8% economic (−3.5% reported) from today's Gulf-war start, −6.6% (−2.6%) from a demand bust [I-calc].
8. **Infrastructure carries itself but does not fund the payout.** Synthetic $7.2bn sleeve with $1.6bn unfunded: year-1 net +$0.17bn (normal), +$0.08bn (today), −$0.03bn (S1; P10 −$0.13bn) [I-calc], against PE's −$2.3bn in the drought [S-prior]. Operating yield (4.3–4.7%) persists; closed-end exits do not (infrastructure 5-year DPI ≈40% → ≈13%, McKinsey) [S-prior].
9. **Leverage is structural.** Liabilities/assets average 77–78% (≈90% for contracted projects) [S]. UK water: 55% notional gearing, eight companies above 70%, two of 17 with positive returns on regulated equity in 2024–25 [S]. Project-finance loans recover 77.9% [S], but equity is first loss. In S1, merchant power locks up in 64% of paths [I-calc].
10. **The most liquid private strategy after buyout, but not liquid.** LP pricing 91% of NAV (H1 2026), 82–83% in 2020 and 2022 [S]. Evergreen funds: 5% quarterly cap, pro rata, no carry-over [S]. An 8% holder recovers 90% in four quarters under stress, 48% with suspensions [I-calc]. Real assets are 15% of GP-led volume [S].
11. **With evidence-based beliefs, LEVER disappears and SELL comes sooner.** A fused 8.5% forward return (α\* 2.6%, against 11% in stream 08's example) removes LEVER. At today's 9/9/4/4/4 liquidity term structure a 91% bid is a SELL, because HOLD needs ≥ 9.7%; at an 83% bid REFINANCE wins [I-calc].
12. **Forecast bias is documented.** Rail patronage +106%; road traffic misses of more than ±20% in half of 183 projects, with no average optimism [S: Flyvbjerg et al. 2005]; toll roads show "considerable optimism bias" [S: Bain 2009]. Use reference-class haircuts by segment and stage [I].

**Design.**
- Model positions at the asset level (fund interests as cohorts) on nine archetypes driven by E's states and factors.
- Carry levered equity cash flows with DSCR lock-ups, coupon-roll refinancing and sweeps.
- Carry economic NAV by duration plus refinancing and cash-flow channels; carry reported NAV smoothed.
- Score actions on the single kernel. A partial stake sell-down is SELL.
- Credit inflation hedging only where θ^E > 1 is evidenced.
- The specification card is §6.10.

---

## 2. Core concepts and theory

### 2.1 What an infrastructure equity claim is

An infrastructure company converts a long-lived, specific, usually monopolistic asset into cash flows. Those cash flows are governed by one of three *business models* (SIPA/EDHECinfra TICCS® pillar) [S]:

| Business model | Revenue rule | Typical assets | Main risks |
|---|---|---|---|
| **Regulated** | Allowed revenue = opex + depreciation + allowed return × RAB; RAB often CPI-indexed; return reset every 4–8 years | Water, electricity and gas networks; some airports | Regulatory reset (allowed WACC, totex), political intervention, gearing |
| **Contracted** | Availability payments or PPAs; price fixed or indexed; volume risk sits with the off-taker | PPPs, contracted renewables, take-or-pay midstream, towers (master lease agreements) | Counterparty, re-contracting (merchant tail), cost inflation where the price is not indexed |
| **Merchant / GDP-linked** | Price × volume set by markets or concession tariffs | Toll roads, airports, ports, merchant power, data centres on re-leasing | Volume (GDP, pandemic, war), power price, competition, obsolescence |

Fund *strategy* labels layer onto these [S: GI Hub/Preqin]: core (operating, forecastable, low error), core-plus (more demand and cycle exposure), value-add (enhancement and usage growth) and opportunistic (capital growth, often without existing cash flow). TICCS's second axis is corporate structure: project finance or corporate.

### 2.2 Cash-flow identity and leverage

For asset i in segment k:

$$\mathrm{CFADS}_{t}=P_{t}Q_{t}-O_{t}-K^{m}_{t},\qquad \mathrm{ECF}_t=\mathbb 1\{\mathrm{DSCR}_t\ge \underline d_k\}\,\mathbb 1\{\text{no sweep}\}\,\big(\mathrm{CFADS}_t-\mathrm{DS}_t\big)^+,\qquad \mathrm{DSCR}_t=\frac{\mathrm{CFADS}_t}{\mathrm{DS}_t}$$

- P carries the pass-through θ_k; Q carries GDP elasticity and jumps; O (opex) is cost-indexed; K^m is maintenance capex; DS is debt service.
- Project finance sculpts debt to a target DSCR, typically 1.2–1.4× for contracted assets, and locks up distributions below ≈1.10–1.20× [P]. Holdcos pay interest only and refinance bullets, so their cost of debt *reprices* at each maturity (the refinancing channel, §2.4).
- In EDHECinfra's factor model leverage is the largest premium contributor, steep from low to medium leverage but flat beyond, because the most levered projects (≈90%: renewables, social infrastructure) are the safest contracted ones [S]. High leverage signals low asset risk; it is not a free return lever [I].

### 2.3 Valuation: three channels

Equity value is the PV of expected equity cash flows:

$$V^E_t=\sum_{\tau>t}\frac{\mathbb E_t[\mathrm{ECF}_\tau]}{(1+y^E_{t})^{\tau-t}},\qquad y^E=r+\pi^e+\mathrm{ERP}^E$$

Equivalently, under Modigliani–Miller, $V^E=V^A-V^D$, with assets and debt discounted on their own curves. Value changes through three channels:
- **Cash-flow news:** volume, price, opex, regulatory resets.
- **Discount-rate news:** real rate, expected inflation, risk premium.
- **Financing news:** coupon repricing, refinancing failure, covenants.

EDHECinfra finds the cash-flow and discount-rate channels of similar magnitude over 20 years. Over the five years to 2021, discount rates and risk premia dominated [S]. Over the three years to 2020, rate changes added ≈+15% to fair values while changes in expected cash flows added less than 1% [S: EDHECinfra/Bloomberg 2021].

EDHECinfra prices the risk premium with factors: size (a liquidity proxy, so larger assets carry *higher* premia), leverage, profits (negative), investment (a greenfield premium), term spread or country risk, and business-model and sector controls [S: Blanc-Brude & Tran 2019; Blanc-Brude & Gupta 2021]. Average expected returns fell from low double digits before 2008 to ≈6% at end-2016 ("peak infra"), settled at 7–8% after 2017, and on SIPA's measure reached 11.3% by November 2025 [S].

### 2.4 Duration, pass-through and the refinancing channel

Linearising $V^E=V^A-V^D$, with asset duration $D_A$, a fixed/hedged debt share h, debt duration $D_D$ and a regulatory-reset share ψ:

$$-\frac{\partial\ln V^E}{\partial r}\approx\frac{(1-\psi)\,D_AV^A-h\,D_D\,V^D}{V^E}+\underbrace{\frac{(1-h_{\text{eff}})V^D\,\bar A}{V^E}}_{\text{refinancing at market}},\qquad -\frac{\partial\ln V^E}{\partial\pi^e}\approx\frac{(1-\theta^{A})\,D_AV^A-h\,D_DV^D}{V^E}$$

- $\theta^A=(\theta-o-\kappa)/(1-o-\kappa)$ is the pass-through to CFADS when a share o of revenue is opex and κ is maintenance capex, both indexed to full inflation.
- $\bar A$ is the annuity value of the repriced coupons.

Four consequences [I-calc; §4.6]:
1. Indexed revenue on nominal fixed debt is *long* inflation for equity (a regulated network at 65% gearing gains as π^e rises).
2. Fixed escalators, unindexed PPAs and indexed opex on unindexed revenue give θ_A < 1, sometimes below 0: *short* inflation.
3. Regulatory resets (ψ ≈ 1 beyond the current control) make regulated equity nearly rate-neutral, provided the regulator follows market rates.
4. Constant-leverage holdcos that refinance at market carry a concealed short position in long real rates, doubling or tripling the cash-flow-fixed duration under permanent shocks.

**Limits of pass-through** [P/I]: indexation lags of 3–15 months; caps and floors in toll and tower contracts; political limits on regulated tariffs and windfall measures; opex and capex inflation outrunning indexation; and basis between the index used (CPI, CPIH, RPI, PPI) and the investor's own inflation.

### 2.5 Volume risk: transitory against permanent

A transitory revenue shock of size J that decays with persistence τ years costs, relative to value, roughly

$$\Delta\ln V^E\approx \mathrm{OL}_k\cdot J\cdot\frac{\tau}{D_k}$$

where OL, operating leverage, is the elasticity of CFADS to revenue. EDHECinfra notes that airports' long lives limited the *value* impact of the 2020–23 dividend losses, while the cash impact was severe [S]. Permanent shocks (GDP level losses, structural traffic shifts) move value one for one. The engine must separate the two: distributions see the whole transitory shock, value mostly the permanent part plus risk-premium moves.

### 2.6 Fund structure

Closed-end incentives (finite life, carry, fundraising) produce quick exits of the best assets, so cash flows look like PE despite "long-lived tangible assets" [S: Andonov et al. 2021]. Open-end funds and direct stakes avoid forced exits but take on queue risk (§4.4) [I]. Continuation vehicles are the GP-led middle ground (§5).

---

## 3. Methods and models: options and trade-offs

| Need | Options | Trade-off | Recommendation |
|---|---|---|---|
| Economic value | (a) Appraisal DCF (manager NAV); (b) mark-to-model factor pricing (EDHECinfra/SIPA: monthly asset DCFs, factor risk premia updated by Kalman filter on transactions) [S]; (c) listed proxies (FTSE Global Core Infrastructure 50/50, utilities); (d) secondary prices | (a) is stale and smooth, but it is what covenants and reports use. (b) is market-consistent but licensed and model-dependent. (c) has the wrong sector mix and business models; SIPA argues listed proxies mislead on diversification [S]. (d) is sparse and fund-level | Economic NAV = (b)-style duration model, calibrated to infraMetrics where licensed. Reported NAV = smoothed (a). Market-implied anchor = (d) plus listed infrastructure-trust discounts [I] |
| Cash flows | (a) Fund-level Takahashi–Alexander with yield; (b) asset-level structural model (revenue/opex/capex/debt); (c) reduced form (cash yield × NAV) | (a) handles commitment pacing but not covenants. (b) is needed for REFINANCE/LEVER and lock-ups but data-heavy. (c) is fast but misses lock-ups | (a) for closed-end fund interests (RFT-TA v2 with yield Y_k and exit-window multipliers); (b) for direct, co-investment and top-30 underlying assets; (c) only for small residuals |
| Rates and inflation | Fixed CPI pass-through vs explicit θ, lag, caps and resets | Fixed pass-through overstates hedging | Explicit θ_k, lag L_k, caps, reset period, debt type (nominal, floating, index-linked) |
| Volume | Gaussian GDP beta vs beta + jumps with decay | Gaussian misses the 2020 airport tail (EDHECinfra airports 1-year −19.8%, drawdown 34.9%) [S] | GDP elasticity + compound-Poisson jumps triggered by regime entry (pandemic, war) with segment-specific decay |
| Smoothing | Geltner inversion; Kalman nowcast with listed infrastructure, rates and spreads | Inversion amplifies noise; the Kalman nowcast needs factor loadings | Kalman nowcast (stream 07 FBE nowcast form) with duration-based loadings; Geltner as a check [I] |
| Leverage | Static LTV vs DSCR-sculpted PF vs constant-leverage holdco | Static LTV ignores lock-ups and refinancing | Two debt archetypes, amortising PF (DSCR covenant) and refinanced holdco (coupon roll + failure hazard), plus hedges |

**Rejected** [I]: one infrastructure beta; appraisal returns as risk inputs; since-inception IRR as a decision input (main §4.3); CPI linkage treated as a hedge regardless of debt structure; listed infrastructure as the *return* model (it is a *signal*); Gaussian airport volumes; one smoothing λ^app for core and value-add.

---

## 4. Empirical evidence and current market data

### 4.1 Academic evidence

| Study | Data | Key results | Use in the design |
|---|---|---|---|
| Andonov, Kräussl & Rauh (2021), *RFS* 34(8) [S] | Preqin/Burgiss closed-end funds, vintages 2002–2018 | PME 0.93 (median 0.95, SD 0.31, n = 157), against buyout 1.05, VC 0.99, real estate 0.94. Net IRR mean 9.92% (median 9.35%); MOIC 1.34. Burgiss: PME 0.89, IRR mean 5.6% (median 7.9%). GPME −0.257 with a market loading above 1. +10pp of exits within 5 years → +0.085 PME, +2.575pp IRR. Public investors −1.81pp IRR. Closed-fund AUM $59bn (2008) → $486bn (2019) | CEF engine = PE engine plus yield; no "low-risk" prior for CEFs; exit dependence → e_t drives CEF distributions |
| Gupta & Van Nieuwerburgh (2021), *JF* 76(6), as cited by Andonov et al. [S] | Strip valuation | Closed infrastructure funds earn −6¢ risk-adjusted profit per $; their cash-flow risk is replicable by listed infrastructure, Treasuries and the stock market | Factor structure for the nowcast; α\* prior near 0 for CEFs |
| Bitsch, Buchner & Kaserer (2010), *EIB Papers* 15(1) [S] | CEPRES: 363 infrastructure and 11,223 other realised deals, 1971–2009 (telecom- and VC-heavy, per a critic) | Higher performance and lower default frequency than non-infrastructure deals; no evidence of more stable cash flows; higher returns possibly from higher market risk | Early evidence against "stable cash" priors; sample definition matters |
| Bianchi, Bornholt, Drew & Howard (2014), *JBF* 42 [S] | US listed infrastructure rebuilt by factor mapping, 1927–2010 | Recent history may understate long-run tail risk, which is comparable to broad US equities; benefits for mean-variance and mean-CVaR investors | Long-run tail calibration for listed proxies |
| Blanc-Brude & Tran (2019), EDHECinfra [S] | 15 years of secondary transactions | Six factors (size, leverage, profits, term spread, value, growth) plus sector and geography explain prices; a price-regime shift in 2008–2015; road valuations cyclical; renewables at higher price-to-sales | Factor-based ERP; the "regime shift" risk to marks |
| Blanc-Brude & Gupta (2021), EDHECinfra [S] | Hundreds of firms, 2000–2021 | Total-return volatility 7–12% (appraisal 2–3%); duration 7.4–11.6 by segment (Table 1); leverage factor 77–78% on average; contracted projects' appraisal-NAV volatility 1.8–2.0% vs 7.3–11.5% market-implied | Calibration targets (§4.2) |
| Wurstbauer & Schäfers (2015), *JPIF* 33(1) [S] | US, 1991–2013, direct and listed | In the short run only direct infrastructure is a partial inflation hedge; all series co-move with inflation in the long run; direct infrastructure has the best inflation-protection properties | θ evidence is weak in the short run; credit hedging only by structure |
| Flyvbjerg, Skamris Holm & Buhl (2005), *JAPA* 71(2) [S] | 210 transport projects, 14 nations, $59bn | Rail overestimated in 9 of 10 cases, by 105.6% on average. Roads (183): half missed by more than ±20%, a quarter by more than ±40%; on average actual traffic was 9.5% *above* forecast (SD 44.3%); no improvement over 30 years; no toll/non-toll split | Volume-forecast error distributions by mode |
| Bain (2009), *Transportation* 36(5) [S] | More than 100 privately financed toll roads | Forecasts show "large errors and considerable optimism bias"; financing should absorb large deviations | Toll-road bias prior (greenfield) |

### 4.2 Index evidence: returns, volatility, drawdowns, duration

**EDHECinfra, data as of Q1 2021, local currency (Blanc-Brude & Gupta 2021, Table 1)** [S]:

| Index | 1y TR | 5y TR p.a. | 5y vol | 10y vol | 99.5% 1y VaR | Max DD | Duration | E[R] |
|---|---|---|---|---|---|---|---|---|
| infra300® | −3.9% | 4.1% | 9.8% | 12.7% | 21.2% | 13.8% | 8.7 | 8.8% |
| Contracted | 2.8% | 6.6% | 8.1% | 11.3% | 15.0% | 10.4% | 7.7 | 7.7% |
| Merchant | −3.4% | 5.8% | 11.8% | 14.6% | 27.2% | 21.6% | 7.7 | 10.6% |
| Transport | −4.2% | 6.2% | 11.5% | 14.9% | 26.9% | 22.4% | 8.6 | 8.7% |
| Airports | −19.8% | −0.9% | 16.2% | 17.8% | 36.0% | 34.9% | 11.6 | 8.9% |
| Wind | −0.3% | 7.9% | 8.2% | 10.5% | 11.4% | 9.6% | 7.4 | 6.6% |
| Core | 1.0% | 9.4% | 7.3% | 10.4% | 12.5% | 11.2% | 7.7 | 6.2% |
| Core+ | −1.9% | 11.0% | 9.7% | 12.4% | 14.6% | 11.9% | 9.2 | 9.1% |

**SIPA infraMetrics, gross, local currency, equal-weighted** [S: factsheet May 2026; CMA paper Jan 2026]:

| | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 3y / 5y / 10y p.a. | 3y / 5y / 10y vol | 10y max DD | Cash return |
|---|---|---|---|---|---|---|---|---|---|---|
| infra300 | −1.85% | 16.14% | 8.14% | 13.45% | 9.51% | 7.92% | 10.1 / 11.3 / 8.7% | 5.9 / 9.1 / 8.9% | −11.0% | 10.6% |
| infra100 Core | 3.28% | 9.88% | 4.62% | 16.81% | 9.22% | 4.40% | 9.0 / 8.9 / 8.6% | 7.2 / 10.8 / 10.4% | −12.1% | 8.0% |
| infraGreen | 2.07% | 5.57% | 5.88% | 10.53% | 11.97% | 7.62% | 9.3 / 9.8 / 8.4% | 5.1 / 8.9 / 8.0% | −10.8% | 9.6% |

- The cash return is the factsheet's "dividend yield". For infra300 it matches the 10.57-point year-on-year cash contribution in SIPA's Q1-2026 report, against −3.43 points of price return.
- infra300 is 49% contracted, 24% merchant and 27% regulated (probable chart mapping). It returned +3.76% year to date to May 2026 [S: Infrastructure Investor, 17 Jun 2026].
- SIPA's 8–11% cash yields are on lower, market-implied prices and include all shareholder cash, so they are not comparable with fund yields on appraisal NAV (≈4–6%) [I].

**SIPA forward-looking (median expected return; 10-year volatility)** [S]:
- Overall, as of 30 Nov 2025: infra300 11.31% (ERP 8.2%).
- By TICCS industry, as of 30 Sep 2025:

  | Industry | Expected return | 10y volatility |
  |---|---|---|
  | Data infrastructure | 13.77% | 18.37% |
  | Network utilities | 12.89% | 11.08% |
  | Social infrastructure | 11.14% | 9.55% |
  | Power generation excluding renewables | 11.10% | 10.84% |
  | Renewable power | 11.03% | 9.26% |
  | Energy & water | 11.01% | 13.03% |
  | Transport | 10.64% | 9.84% |

- Industry CMAs for private infrastructure range from 7% to 11%, with volatility of 10–19%; BlackRock uses 20%.

**MSCI Global Private Infrastructure Asset Index (appraisal-based, gross)** [S]:
- 12.2% over the year to Q1 2026 (943 assets, $412bn of equity); 11.7% a year since June 2008, with one negative quarter since the GFC. Airports and transport fell from 47% of value (2008–19) to 26% (2020–25).
- By sector, 3 years to Q2 2025: power generation 14.3%, digital 12.1%, transmission and distribution 12.1%, airports 11.7%, transport 10.8%, renewables 7.9% [S: CBRE IM Q4 2025]. One year to Q4 2025: power generation 23%, utilities 15%.
- Beat CPI + 400bp in 88% of rolling periods; rolling one-year correlation 0.4 with US inflation and 0.3 with Henry Hub gas (2005–25) [S: CBRE IM Q2 2026].

**Fund-level returns** [S]:
- Cambridge Associates, net, year to Q1 2026: core/core-plus 10.4%, value-add 7.9%. The universe is 80 core/core-plus funds ($242bn) and 92 value-add funds ($307bn).
- Preqin vintage 2022 net IRR (13 Jul 2026): quartiles 21.1 / 11.8 / 5.3%.
- Preqin 2010–2020 vintages, median net IRR (SD): debt 8% (7%), core 12% (10%), core-plus 10% (13%), value-add 12% (15%), opportunistic 8% (15%) [GI Hub 2024].
- MSCI private capital infrastructure: 12.6% in calendar 2025 [S-prior: G9]. J.P. Morgan 2027 LTCMA: 7.1% [S-prior: stream 07].

### 4.3 Market conditions, 2025–2026

| Item | Value | Date | Source |
|---|---|---|---|
| Fundraising (final closes) | Record $216.1bn in 2025 ($135.5bn in 2024). Q1 2026: 27 funds, $25bn; Q2 2026: 8 funds, $4.4bn. H1 2026 interim closes $57bn (H1 2025: $69bn). 731 funds seeking $463bn | to Jul 2026 | Preqin [S] |
| Fundraising (interim closes, other definition) | ≈$190bn year to date, "nearly three times 2025"; average target allocation > 6% (5% in 2023) | Sep 2026 | CBRE IM Q3 2026 [S] |
| Deal volume | ≈$960bn to Q3 2025 (+22% y/y); > $800bn in H1 2026 (record); digital 28% of deal activity; renewables > 40% of deal count; greenfield doubled in two years, half of it data centres | 2025–26 | Infralogic via CBRE IM [S] |
| Valuation marks | AGS Airports EV £1.5bn ≈ 23× EV/EBITDA; stabilised data-centre NOI yield on cost 9% (core US) to 12% (next-tier) | 2025 | Infralogic and Green Street via CBRE IM [S] |
| Demand drivers | Hyperscaler capex ≈$730bn in 2026. IEA cut its 2030 renewables forecast by 248 GW, the US the largest downward revision | 2025–26 | CBRE IM [S] |
| Rates and inflation | SOFR 3.89% (15 Oct 2026); 10y UST 5.09% [S-prior]. US CPI 3.8% in April 2026, the highest since March 2023 [S] | 2026 | FRED; CBRE IM |
| Gulf-war shock | Strikes from 28 Feb 2026; Hormuz shipping "extremely limited"; Brent averaged $114 in September; spot $126.55 on 14 Oct [S-prior: stream 03]. Air passenger traffic −3.4% y/y in April 2026, mainly because of the Middle East conflict, and +0.2% y/y in July after three months of decline [S] | 2026 | EIA via stream 03; CBRE IM |

The two fundraising series disagree because they count different things: final closes versus interim closes. The synthesis should cite one definition and state which [I].

### 4.4 Liquidity: secondaries, continuation vehicles, open-end terms

**Pricing and volume** [S]:
- Jefferies LP pricing: infrastructure 91% of NAV in H1 2026 (87% all strategies). Energy/infrastructure by year: 82, 93, 83, 87, 90, 90% for 2020–25 (probable chart mapping). Infrastructure portfolios often traded at single-digit discounts, and several deals above $1bn were 100% infrastructure.
- Real assets were 15% of GP-led volume in H1 2026 (13% in 2025); the average CV rollover is 14%.
- Infrastructure secondaries are ≈2% of infrastructure AUM (PE 5%); more than $10bn was raised in 2026 to date [S: CBRE IM Q3 2026]. Buyers hold ≈$20bn and mostly target 13–15% net [S-prior: stream 05, Evercore].

**Evergreen terms** (Stonepeak-Plus Infrastructure Fund, 10-K FY2025) [S]: monthly subscriptions; quarterly redemptions of up to 5% of units outstanding; a 5% deduction on units held under two years; pro rata above the cap, and "unsatisfied redemption requests will not be automatically carried over"; the GP may suspend with independent directors' approval; leverage ≤ 30%; 80–85% in infrastructure investments and 15–20% in debt and liquid securities. As an analogue for stressed queues, private-credit evergreen requests reached 13–14% of NAV against 5% caps in Q2–Q3 2026 [S-prior: groups synthesis, VRC].

**Queue model** (`g11_actions_queue.py`): ADIC requests its whole remaining holding every quarter, because requests are not carried over. Cumulative share of the holding paid [I-calc; SYNTHETIC]:

| Scenario | 1q | 2q | 4q | 8q | 12q |
|---|---|---|---|---|---|
| Normal (others request 1.5% of NAV a quarter); ADIC 8% of fund | 53% | 98% | 100% | 100% | 100% |
| Stress (others 8% a quarter for 6q; NAV −1% a quarter) | 33% | 59% | 90% (P05 83%) | 98% | 98% |
| Severe (others 15% a quarter for 8q; 25% quarterly chance of a 2q suspension) | 18% (P05 0) | 29% | 48% (P05 0) | 73% (P05 39%) | 90% (P05 76%) |
| Stress, ADIC 20% of fund | 19% | 37% | 67% | 97% | 97% |

These shares, the φ(h, S) interface, feed the ladder exactly as the hedge-fund state machine does. ADIC's own share of the fund is a first-order driver [I].

### 4.5 Leverage, defaults and recoveries

**Evidence** [S]:
- **EDHECinfra:** average leverage (liabilities/assets) 77–78% since 2011; contracted renewable and social projects ≈90%.
- **UK water** (Ofwat, *Monitoring Financial Resilience 2024–25*, via The UK Water Report, 9 Nov 2025): notional gearing cut to 55% for 2025–30, but only SES was below 60% and eight companies were above the 70% concern level. Only Severn Trent and Portsmouth earned a positive return on regulated equity, and 2020–25 sector returns were below the 4.1% base.
- **Moody's project-finance bank loans,** 1983–2018, 8,583 projects: ultimate recovery 77.9% (Basel) or 75.8% (Moody's definition); modal recovery 100% (58.1% of cases); recoveries largely independent of the default cycle. In March–May 2020, 66 corporates defaulted against two infrastructure/PF issuers. Unregulated power, ports, private airports and toll roads were most vulnerable; regulated utilities and availability PPPs most resilient.

**Practitioner ranges** [P, to be replaced by ADIC deal data]: project-finance gearing 70–85% (contracted renewables, PPPs) at DSCR 1.20–1.40×; regulated utilities 55–75% net debt/RAB; toll roads and airports 50–65% debt/EV, mostly bullets; towers and fibre ≈5–7× EBITDA; midstream ≈3.5–4.5× EBITDA; data centres ≈40–60% LTV plus development facilities.

### 4.6 Our archetype calculations: duration and pass-through

`g11_durations.py` builds forward-curve DCFs of eight archetypes. Base real rate 2.3%, expected inflation 2.8%.

| Archetype (gearing; θ; debt) | Equity IRR | Avg cash yield, y1–10 | D (equity CFs fixed) | D, permanent real shock | D, real shock HL 5y | D, +1pp inflation | D, +1pp asset ERP |
|---|---|---|---|---|---|---|---|
| Regulated utility, RAB CPI, 5y resets (65%; 1.0; regear, 10y fixed) | 11.5% | 9.0% | 12.9 | 0.8 | 0.7 | **−13.2** | 37.9 |
| Availability PPP, 25y (80%; 0.9; amortising) | 11.7% | 8.6% | 11.0 | 14.7 | 6.1 | **−23.1** | 58.3 |
| Contracted renewables, fixed PPA (75%; 0.1; amortising) | 12.4% | 11.7% | 7.8 | 11.5 | 5.4 | **+26.7** | 35.2 |
| Toll road, 40y (60%; 0.8; regear, 8y) | 13.3% | 12.4% | 8.5 | 26.6 | 8.0 | +0.4 | 36.1 |
| Airport, 50y (55%; 0.8; regear) | 13.7% | 11.6% | 9.9 | 29.8 | 7.7 | +3.7 | 38.2 |
| Tower/fibre, 3% fixed escalators (55%; 0.3) | 12.5% | 11.0% | 9.6 | 22.8 | 7.3 | +23.3 | 29.3 |
| Data centre (50%; 0.4; 5y fixed) | 14.1% | 12.2% | 9.3 | 24.0 | 8.3 | +23.3 | 27.1 |
| Midstream (50%; 0.5) | 13.3% | 13.6% | 6.8 | 12.9 | 5.1 | +14.5 | 18.3 |

*SYNTHETIC – NOT ADIC DATA.*
- **Units.** Durations are −Δln V^E per +100bp. A negative inflation duration means equity *gains* when expected inflation rises.
- **Debt tenor matters.** Lengthening the locked tenor from 3 to 25 years moves the toll road's permanent real-rate duration from 30.6 to 15.2 and its inflation duration from +3.5 to −8.5. The regulated utility moves to −9.2 (it gains from higher real rates) and −22.0 [I-calc].
- **Calibration of the cash-flow-fixed column.** It falls in EDHECinfra's 7.4–11.6 band; regulated is slightly above it.
- **Why the ERP column is large.** It applies a +1pp shift to the *asset* discount rate, levered 2–5× into equity. It is the channel through which risk-premium regimes move equity marks.

---

## 5. Practitioner and peer practice, and case studies

**Peers** [S-prior: stream 02]: NBIM caps unlisted renewable infrastructure at ≤ 2%; GIC's 2026 Strategic Portfolio gives real assets the inflation-resilience role; Australia's Future Fund deliberately overweights infrastructure.

**Practice** [P]:
- Sovereign and pension investors combine closed-end commitments (GP access and deal flow), open-end core funds (duration and yield) and direct or consortium stakes. The governance package covers board seats, reserved matters, ROFR/ROFO, tag/drag, pre-emption and lock-ups.
- Club-deal co-investors underwrite and then *sell down*, so sell-down capacity is part of entry.
- Owners recapitalise holdcos when rates are low. That is the origin of the refinancing channel in §2.4.

| Case | Evidence | Lesson for the engine |
|---|---|---|
| 2020 mobility shock [S] | Airports −19.8% (year to Q1 2021) and a 34.9% drawdown, against contracted +2.8%. 2020 attribution: dividends −3.5%, rates more than +5%, risk premia up to −9%. Moody's: airports, toll roads, ports and merchant power most vulnerable | Cash falls far more than value for long-lived GDP assets; separate transitory from permanent shocks (§2.5) |
| UK water [S] | 8 of 17 companies above 70% gearing against 55% notional; 2 of 17 with positive returns on regulated equity in 2024–25. The Thames Water holdco (Kemble) loan default in 2024 is widely reported [U] | "Regulated" protects the opco and senior debt, not levered equity; model holdco structures |
| 2022–26 rates and inflation [S] | SIPA expected return 9.55% → 11.31% (ERP +120–130bp), yet infra300 returned +8–13% a year on ≈10% cash returns. Renewables returned 7.9% a year against 14.3% for power generation; the IEA cut its 2030 renewables outlook by 248 GW | Fixed-price renewables and digital assets are rate- and inflation-short; merchant power in tight markets hedges inflation (+23%) |
| 2026 Gulf war [S/S-prior] | Air traffic −3.4% y/y in April 2026, +0.2% in July; Hormuz rerouting; US CPI 3.8% | The joint state [I]: real rates and risk premia up, Gulf transport volumes down, the owner's draw possibly up, midstream and merchant power up |
| Digital [S/P] | SIPA data infrastructure: expected return 13.8%, volatility 18.4%; hyperscaler capex ≈$730bn; data centres half of greenfield volume. Risks: tenant concentration, power, obsolescence, overbuild, AI-adoption timing | Treat as growth assets: risk-premium loading β^q = 1.2–1.6, long duration |
| CVs and secondaries [S] | Sponsors use CVs to keep "high-quality, cash-generative assets"; real assets 15% of GP-led volume; LP portfolios above $1bn that were 100% infrastructure drew multi-billion demand | SELL at ≈91% is a real lever; CV elections are recurring HOLD/SELL events |

---

## 6. Design implications for the ADIC framework

### 6.1 Placement, taxonomy and the synthetic sleeve

**Taxonomy (configuration)** [I]: `group = REAL_ASSETS`, `sector = INFRA`; `segment ∈ {REG, CON_IDX, CON_FIX, TOLL, AIR, PORT, MID, TOW, DC, MER, DEV}`; `business_model ∈ {regulated, contracted, merchant}` (TICCS-compatible); `stage ∈ {greenfield, brownfield}`; `vehicle ∈ {CEF, OEF, CO_INV, DIRECT, JV, CV}`.

**Boundaries for the synthesis:** midstream sits in infrastructure with an `energy_link` flag, sharing oil and gas loadings with the energy & natural-resources stream; infrastructure debt sits in Private Credit; listed infrastructure sits in Public Markets and is G11's market-implied anchor.

**Synthetic sleeve** (SYNTHETIC; pending the Real Assets synthesis):
- $7.2bn NAV (40% of Real Assets) and $1.6bn unfunded.
- Vehicles: closed-end 40%, co-investment/direct/JV 35%, open-end 25%. Whether the user's "funds" include open-end funds is to be confirmed.
- Weights: REG 18%, CON_IDX 8%, CON_FIX 14%, TOLL 12%, AIR 8%, MID 10%, TOW 10%, DC 12%, MER 8%. GCC exposure: 20% of airport NAV.

**Partial sell-downs are SELL.** The user's confirmed definition of SELL is "dispose of the holding, wholly or partly", whereas interim rule §8.3 lists partial-stake and JV sell-downs under REFINANCE. **Recommendation** [I]:
- Any disposal of common equity is **SELL** with fraction φ.
- Cash raised while all common equity is retained (holdco preferred, structured equity, debt) is **REFINANCE**.
- The integration memo should apply this to design brief §8.3.

### 6.2 State variables and factors

- **From E:** S_t; e_t ∈ {O, N, D, F}; Z_t ∈ {N, B, SG, DB, SS, GW}; factors r_t (10-year real), π^e_t, π_t, g_t, x^p_t (power), q_t (infrastructure risk premium; not to be confused with the exit window e_t), Δs_t (credit), and Brent for the midstream energy link.
- **Script regimes** [I]: N = expansion or recovery with Z ∈ {N, B}; I = inflationary late-cycle; C = crisis with Z = DB; G = Z ∈ {GW, SS}.
- **Asset state:** s^perm and J; c^fix, debt balance and maturity ladder; DSCR and lock-up/sweep counters; V^E and N; regulatory-reset clock and contract/concession expiry; unfunded U; open-end queue state.

### 6.3 Equations (implementable)

1. **Revenue.**

   $$\Delta\ln R_t=[\theta_k\pi_{t-L_k}+(1-\theta_k)\bar\varepsilon_k]\Delta+[\mu^Q_k+\beta^g_k(g_t-\bar g)]\Delta+\Delta J_t+m_k\Delta x^p_t$$

   - The price leg is capped and floored at $[\underline c_k,\bar c_k]\Delta$.
   - Regulated revenue is $R_t=(\omega_t+\delta)\mathrm{RAB}_t+O^{allow}_t$. The RAB is CPI-indexed, and ω resets every $T^{reg}$ to $r_t+\mathrm{ERP}^{reg}+\eta$, passing through half of any risk-premium change.
2. **Jumps.**

   $$J_{t+\Delta}=J_t\,2^{-\Delta/h_k}+\xi_t$$

   They arrive on regime entry:

   | Trigger | Segment | ξ | Half-life h |
   |---|---|---|---|
   | Entering C, mobility shock (probability 0.25) | AIR | −0.55 | 3q |
   | Entering C, mobility shock (probability 0.25) | TOLL | −0.18 | 1q |
   | Entering G | AIR | −0.25 × gcc_share − 0.03 | 3q |
   | Entering C (probability 0.5) | DC | −0.10 | 8q |
   | Entering C | MID | −0.08 | 4q |
3. **Cash flows.**

   $$\mathrm{CFADS}_t=\mathrm{CFADS}^{plan}_te^{\mathrm{OL}_ks^{rev}_t}$$

   $$\mathrm{DS}_t=\mathrm{DS}^{plan}_t\big[\kappa^{int}_k\,c_t/c_0+(1-\kappa^{int}_k)\big]$$

   $$c^{fix}_{t+\Delta}=c^{fix}_t(1-\tfrac{\Delta}{M_k})+i_t\tfrac{\Delta}{M_k},\qquad c_t=h_kc^{fix}_t+(1-h_k)i_t,\qquad i_t=r_t+\pi^e_t+s_k+\Delta s(S_t)$$

   - ECF follows §2.2, with lock-up at $\underline d_k$.
   - A refinancing failure, with probability $p^{fail}(S_t)\cdot\min(1,4\Delta/M_k)$ a quarter, triggers a 4-quarter sweep and a 3% distress cost.
4. **Economic NAV.**

   $$\Delta\ln V^E=(\mu_k-y_k-\tfrac12\sigma^2)\Delta-D_k[\Delta r+(1-\theta^E_k)\Delta\pi^e+\beta^q_k\Delta q]+\mathrm{OL}_k\Delta s^{perm}+\omega\,\Delta\ln \mathrm{ECF}^{ss}(c)+\tfrac{\tau_k}{D_k}\mathrm{OL}_k\xi^{new}+\sigma^{id}_k\sqrt\Delta\,\epsilon$$

   Here ω = 0.5 sets the persistence of coupon repricing, and $\mathrm{ECF}^{ss}=\mathrm{DSCR}_0-\mathrm{DS}/\mathrm{DS}^{plan}$.
5. **Reported NAV.**

   $$N_t=\lambda^{app}_kN_{t-1}+(1-\lambda^{app}_k)V^E_{t-1}$$

   λ^app = 0.85 a quarter for core and contracted assets, 0.70 for value-add and opportunistic. Covenant tests and LP-secondary bids reference N; risk and value reference V^E.
6. **Closed-end funds (RFT-TA v2 with infrastructure parameters).**
   - Calls: $C=(1-e^{-\lambda\Delta})U$, with a call schedule of 20/25/30/35% of remaining unfunded [S-prior: stream 04].
   - Distributions: $Y_kN\Delta$ (operating yield net of fees) $+\,x(e_t)\,V^E\,p^{exit}(e_t)\,\Delta$.
   - Exit rate x = 14 / 10 / 4 / 1.5% a year and exit price $p^{exit}$ = 1.06 / 1.03 / 0.98 / 0.90 for O / N / D / F [I, anchored on McKinsey's DPI decline and Andonov's exit dependence].
7. **Open-end funds.** The quarterly fill and other investors' requests are

   $$\text{fill}_t=\min\{1,\bar g\,\mathrm{NAV}_t/(R^{oth}_t+R^{ADIC}_t)\}$$

   $$R^{oth}_t=\mathrm{NAV}_t\,\mathrm{clip}\big(\rho_0+\rho_1[(N_t-V^E_t)/V^E_t]^++\rho_2\mathbb 1\{S_t=C\},0,\bar\rho\big)$$

   - Requests are not carried over, so ADIC resubmits each quarter.
   - A suspension hazard depends on the regime. The 5% early deduction applies below 2 years.
   - The ρ₁ term encodes the first-mover incentive: redeeming pays when stale reported NAV exceeds economic value [I].
8. **Market-implied anchor.** The anchor $y^{MKT}$ is built from LP-secondary bids, listed infrastructure-fund discounts and listed infrastructure. It enters the FBE as a signal, never as NAV, using stream 07's secondary-implied yield form $(1+y_P)\approx(1+y_V)(\theta/p)^{1/D}$ [S-prior].

### 6.4 Decision variables and action economics

| Action | Instruments | Economics and rule |
|---|---|---|
| **SELL** | (a) Direct or co-investment stake, full or partial (fraction φ); (b) LP-interest secondary (buyer assumes unfunded); (c) open-end redemption (queue); (d) CV election when offered | (a) p = V^E(1 − d_dir(S)) − tc, with d_dir 0–3% (N), 5–8% (D), 15–25% (C) [I]; 6–12 months; ROFR, tag and consents. (b) p = N·p̄(S): 0.91 (N/D), 0.83 (2020/2022 analogue), 0.70–0.75 in crisis [S/I]; 3–6 months. (c) φ(h, S) from §4.4. Rule: SELL iff p^ceq > LAPV(HOLD + best REFI). Sales to ADIC's Secondaries group raise no liquidity |
| **HOLD** | Fund calls and capex; elect to roll in CVs | Continuation value under fused beliefs, less concentration and duration CVaR charges |
| **REFINANCE** (cash-out, common equity retained) | Holdco recap; opco refinancing or up-sizing; holdco preferred or structured equity (Capital Solutions quote); NAV facility on fund interests (CF-owned; dominated as a lever, groups synthesis §2.3); sale-leaseback or ground lease (data centres, land) | REFI iff ℓ̄ > s + f/T + λ_Lev + covenant charge. Holdco spreads S+250–350 (N), S+450 or more (C) [I]. A recap raises look-through leverage *and* real-rate duration through the refinancing channel, so charge both (λ_Lev, CVaR) |
| **LEVER** (exposure up) | Acquisition debt for add-ons; construction or development debt (DC, renewables); opco up-sizing for growth capex | LEVER iff ADD and REFI both pass. With α\* ≈ 2.6% it needs all-in financing ≲ α\* − λ_R m − λ_Lev ≈ S+190bp, i.e. investment-grade opco debt only [I-calc] |

**Region map** (`g11_actions_queue.py`; per $ of NAV; 5-year horizon; flat ℓ) [I-calc; SYNTHETIC]:

| Input set | ADD | HOLD | LEVER | REFI | SELL | At ℓ = 9/9/4/4/4 |
|---|---|---|---|---|---|---|
| A: stream 08 example (forward 11%, yield 6.5%, α\* 5.0%, S+250, bid 0.91) | ℓ < 3.0% | — | 3.0–5.5% | 5.5–9.0% | ≥ 9.0% | REFI |
| B: G11 evidence (forward 8.5%, yield 5%, α\* 2.6%, S+300, 1% fee, bid 0.91) | < 2.5% | 2.5–4.0% | never | 4.0–5.5% | ≥ 5.5% | **SELL** (+4.5% of NAV vs HOLD) |
| B-stress (bid 0.83, S+450) | < 2.5% | 2.5–5.5% | never | 5.5–8.5% | ≥ 8.5% | REFI (+1.0%) |

**What you need to believe: the forward return at which HOLD equals SELL** (5-year hold, 5% cash yield, hurdle r_h = 5.9%) [I-calc]:

| Liquidity premium ℓ | Bid 0.97 (direct stake) | Bid 0.91 (LP, normal) | Bid 0.83 (LP, stress) |
|---|---|---|---|
| 0% | 5.2% | 3.7% | 1.6% |
| 2% | 7.2% | 5.7% | 3.5% |
| 4% | 9.2% | 7.6% | 5.5% |
| 9/9/4/4/4 | 11.3% | 9.7% | 7.5% |

The stream 06 risk-neutral shortcut gives break-even growth of 6.2% for a direct sell-down at 0.97 against holdco debt at SOFR + 300bp. Selling therefore beats borrowing when the forward equity return is below about 6% [I-calc].

### 6.5 Constraints

For IC ratification [I]:

| Constraint | Limit |
|---|---|
| Look-through leverage (counted in the leverage module) | Sleeve debt/(debt + equity) ≤ 70% |
| Lock-up chance constraint | P(lock-up within 12 months) ≤ 10% per asset (≤ 25% for merchant) |
| Default chance constraint | P(equity wipe-out within 3 years) ≤ 2% |
| Maturity wall | ≤ 20% of look-through debt maturing in any 12 months (leverage limit 5); weighted maturity ≥ 6 years |
| Hedging floor | Fixed or hedged share h ≥ 75% for refinanced holdcos |
| Merchant cap | ≤ 25% of sleeve CFADS |
| Digital cap | DC + TOW ≤ 30% of sleeve NAV |
| GCC exposure | Capped on GDP-linked assets |
| Single asset | ≤ 1% of total NAV |
| GP | ≤ 5% of private NAV + unfunded (existing) |
| Open-end concentration | ≤ 10–15% of any fund |
| Existing inadmissible list | No call default; no non-consented transfers or pledges |

### 6.6 Objective terms and prices

All [I]:
- One kernel, with FTP charged on each holding's cash-weighted life (≈9–12 years for direct infrastructure), so the per-NAV liquidity charge is high when ℓ is humped.
- Inflation-hedge value enters only through scenario P&L via structural θ^E_k (§4.6); there is no generic real-asset credit.
- Duration risk is charged through CVaR in the I/G supply-shock stresses, where infrastructure, bonds and equities fall together. The Overlay may hedge real-rate exposure at portfolio level (payer swaps), booked to Real Assets at FTP; asset-level swaps are in h_k.
- Open-end φ(h, S) feeds the ladder. Closed-end calls and DC development capex feed the L4 budgets.

### 6.7 Forecasts: the three series and their biases

**Inputs.** ADIC's series are net IRR/MOIC per holding with downside/base/upside cases (read as P10/P50/P90), archived quarterly (design brief §9) [A]. The FBE translates them to the forward log return on nowcast economic NAV.

**Structural corrections before the residual bias** [I unless tagged]:
1. Replace the plan's inflation path with E's, applied through θ_k.
2. Replace assumed refinancing coupons with forwards plus a spread (the refinancing channel).
3. Apply volume reference classes, as actual/forecast ratios:
   - greenfield toll road: mean 0.80, SD 0.30 (Bain);
   - brownfield road: mean 1.00, SD 0.15 (Flyvbjerg: no average optimism, wide dispersion);
   - rail patronage: × 0.5 (Flyvbjerg's +106%) [S-based];
   - brownfield airport: mean 0.97, SD 0.10, plus jumps.
4. Shrink the exit multiple 50% toward entry and toward the market-implied multiple.
5. Slip exits by +2–4 quarters (D) or +4–8 quarters (F).
6. Apply Green-Book-style capex and duration uplifts to greenfield projects [S-prior: stream 07].

**Residual bias priors** (per year, underwritten b^u / forecast b^f):

| Strategy | b^u | b^f | Prior σ_k |
|---|---|---|---|
| Core/core-plus | +1.5pp | +1.0pp | 2–3% [S-prior] |
| Value-add | +3.0pp | +2.0pp | 4% |
| Greenfield/development | +4.0pp | +3.0pp | 6% |

**Other FBE inputs:**
- *Prior m:* J.P. Morgan core 7.1% plus segment premia (core-plus +1.0pp, value-add +2.0pp, digital +2.5pp), with SIPA's 11.3% reported as the upper model.
- *Actuals* de-smoothed with λ^app = 0.85; the signal $y^{MKT}$ as in §6.3(8).
- *Flags:* traffic CAGR above the reference P75; exit multiple above entry; refinancing below forward coupons; downside-case DSCR headroom < 0.15×; merchant share rising after contract expiry.

### 6.8 Illustrative engine: calibration and the sleeve cash map

`g11_infra_mc.py`: 20,000 paths, 40 quarters, nine segments, gross of fees. **Calibration from a normal start** [I-calc; SYNTHETIC], compared with the evidence:

| Segment | Mean TR | Cash yield | Volatility, economic / reported | 10y max DD, P50 / P95 | P(lock-up, 3y) | Evidence anchor |
|---|---|---|---|---|---|---|
| REG | 8.7% | 5.1% | 8.7 / 2.1% | 15 / 27% | 0.0% | Network utilities 10y vol 11.1% (SIPA); core DD 11.2% (EDHEC) |
| CON_IDX | 8.3% | 6.8% | 6.2 / 1.5% | 13 / 24% | 0.2% | Contracted vol 8.1%, DD 10.4% |
| CON_FIX | 8.5% | 7.8% | 8.5 / 1.9% | 21 / 35% | 0.2% | Renewables vol 9.3%, wind DD 9.6% |
| TOLL | 9.5% | 4.4% | 9.7 / 2.4% | 16 / 28% | 0.2% | Transport vol 9.8–11.5%, DD 22.4% |
| AIR | 9.7% | 3.2% | 13.9 / 3.6% | 25 / 47% | 8.9% | Airports vol 16.2–17.8%, DD 34.9% |
| MID | 9.6% | 8.1% | 8.8 / 2.0% | 20 / 34% | 0.0% | — (listed proxies are higher) |
| TOW | 10.0% | 2.7% | 12.1 / 3.0% | 18 / 31% | 0.0% | — |
| DC | 10.8% | 1.8% | 15.4 / 3.9% | 23 / 38% | 0.0% | Data infrastructure vol 18.4% |
| MER | 10.6% | 8.6% | 13.9 / 2.7% | 25 / 40% | 30.5% | Merchant vol 11.8–14.6%, DD 21.6% |
| **Sleeve** | **9.7%** | **5.3% gross (4.3% net of fees)** | **9.2 / 2.3%** | **15 / 26%** | — | infra300 10y vol 8.9%, 10y DD 11.0% (SIPA); appraisal 2–3% (EDHEC) |

- **Fit.** Volatilities fit. The model's drawdowns are 3–10pp deeper than EDHECinfra's single historical path for contracted assets, because the simulation includes stagflationary real-rate regimes that the 2011–2021 sample lacks.
- **Next step.** Refit on licensed infraMetrics monthly series [I].

**Sleeve cash map, first 12 months** ($bn; mean, with P10 in brackets; $7.2bn NAV, $1.6bn unfunded) [I-calc; SYNTHETIC]:

| Start state | Distributions (% of NAV) | Of which operating | Exits | Calls | **Net** | 5-year cumulative net (P50) | Y1 NAV change P05, economic / reported |
|---|---|---|---|---|---|---|---|
| Normal (N, N exits) | 0.58 (8.1%) | 0.31 | 0.27 | 0.42 | **+0.17** (+0.03) | +1.62 | −7.4 / −2.1% |
| Drought (N, D exits) | 0.46 (6.4%) | 0.31 | 0.15 | 0.42 | **+0.05** (−0.04) | +1.34 | −7.6 / −2.2% |
| **Today: Gulf war + drought (G, D)** | 0.49 (6.7%) | 0.34 | 0.15 | 0.41 | **+0.08** (−0.02) | +1.23 | **−11.8 / −3.5%** |
| Inflationary late-cycle + drought (I, D) | 0.47 (6.5%) | 0.32 | 0.15 | 0.40 | **+0.07** (−0.03) | +1.25 | −11.0 / −3.1% |
| S1-like demand bust (C, F) | 0.36 (5.0%) | 0.24 | 0.12 | 0.39 | **−0.03** (−0.13) | +1.15 | −6.6 / −2.6% |

- **T4′ conventions.** Distributions are operating yield plus exits at 10.8% of drought rates, and calls are ×1.38. That gives a year-1 net of ≈ 0.24 + 0.02 − 0.57 = **−$0.32bn** [I-calc].
- **Reading.** Infrastructure stays near cash-neutral in stress because operating yield (≈3.3–4.7% of NAV) persists. Its marks fall most in the supply-shock state. In S1, merchant assets lock up in 64% of paths in year 1 [I-calc].

### 6.9 Calibration targets and data needs

**Calibration targets:**

| Target | Value | Source |
|---|---|---|
| Economic volatility | Sleeve 8–10%; segment bands as in §6.8 | EDHECinfra; SIPA |
| Reported volatility | 2–3% | EDHECinfra |
| Cash-flow-fixed duration | 7.4–11.6 | EDHECinfra |
| 2020 attribution | Rates +5%; risk premia −9%; dividends −3.5% | EDHECinfra |
| Infrastructure LP pricing | 91% (normal); 82–83% (2020/2022) | Jefferies |
| Core vs value-add net returns | 10.4% vs 7.9% (1 year to Q1 2026) | Cambridge Associates |
| Closed-end PME | 0.93 | Andonov et al. |
| Recovery on project-finance loans | 77.9% | Moody's |
| UK water gearing | 55% notional; > 70% at 8 of 17 companies | Ofwat |

**Data ADIC must supply** [A]: the items in §9, organised by the specification card's fields.

### 6.10 SPECIFICATION CARD

| Item | Specification |
|---|---|
| **Data fields** | `position_id, group=RA, sector=INFRA, segment, business_model, stage, vehicle, country, gcc_flag, energy_link, ownership_pct, governance_rights{board, ROFR, tag, drag, reserved}, consent_flags{transfer, pledge}, commitment, unfunded, call_schedule, fee_terms, NAV_reported(t), NAV_asof, revenue_index{theta, lag, cap, floor, index}, reg_reset_date, allowed_return, RAB, contract_expiry, merchant_tail_share, volume_plan(t), volume_actual(t), OL, opex_share, capex_plan(t), debt[{tranche, opco/holdco, amortising/bullet, balance, maturity, coupon, fixed/hedged share, covenants{lockup_DSCR, default_DSCR, ICR, LTV}}], DSCR_hist, OEF_terms{cap, freq, early_deduction, suspension}, OEF_share_of_fund, CV_offers, marks{u,a,f: IRR/MOIC + P10/P50/P90, asof}, is_synthetic` |
| **Return equation** | Economic: §6.3(4), with D_k, θ^E_k, β^q_k, OL_k, τ_k from the table below. Total return = ΔlnV^E + ECF/V^E. Gross-to-net: the fee drag by vehicle is CEF 2.0%, OEF 1.0%, co-investment 0.5% of NAV a year [I] (ADIC data is already net) |
| **NAV equations** | Economic V^E (duration, refinancing and cash-flow channels) and reported N_t = λ^app N_{t−1} + (1 − λ^app)V^E_{t−1}: λ^app = 0.85 (core/contracted) or 0.70 (value-add/opportunistic), lag one quarter. Covenants and LP bids use N; risk, value and Tier-1 use V^E |
| **Cash-flow equations** | Revenue §6.3(1), jumps (2), CFADS/DS/coupon roll (3), lock-up and sweep, ECF §2.2. CEF: calls 20/25/30/35% of unfunded by age; distributions = Y_k·N + x(e)·V^E·p^exit(e). DC development capex 6% of direct DC NAV a year (4% in C) |
| **Segment defaults** | See the parameter table below |
| **Liquidity terms** | Direct/co-investment SELL: 6–12 months, d_dir 0–3 / 5–8 / 15–25% (N/D/C). LP secondary: 3–6 months, p̄ 0.91 / 0.83 / 0.70–0.75. Open-end: quarterly, 5% cap, pro rata, no carry-over, suspension hazard 0 / 1 / 25% a quarter (N/D/C), φ(h, S) per §4.4. CV: GP-triggered offers, average rollover 14% |
| **Stress behaviour** | Supply shock (G/I): real rates +0.6–1.0pp, π^e +1.0–1.5pp, ERP +0.2–0.4pp → sleeve Y1 P05 −11 to −12% economic. Demand bust (C): rates −1pp, ERP +1pp, GDP −3%, mobility jumps, merchant lock-ups, spreads +200bp, 15% of maturing debt fails to refinance → year-1 distributions −38% against normal (operating cash −23%), NAV P05 −6.6%. Exits follow e_t |
| **SELL** | Rule: p^ceq > LAPV(HOLD + best REFI). Partial sell-downs are SELL (φ). Intra-ADIC sales raise zero. Break-even forward returns in §6.4 |
| **HOLD** | Fund calls and capex; CV roll; continuation value at the FBE posterior less concentration and duration CVaR charges |
| **REFINANCE** | Holdco recap (S+250–350 N / S+450+ C, LTV/ICR covenants), opco refinancing or up-sizing, holdco preferred (Capital Solutions reserve quote, ≥ 3 RFQs), NAV facility (CF). Rule: ℓ̄ > s + f/T + λ_Lev + covenant charge. Raises look-through leverage and real-rate duration |
| **LEVER** | Acquisition, development or opco growth debt. Rule: ADD ∧ REFI. With α\* ≈ 2.6% it needs financing ≲ S+190bp |
| **Forecasts and biases** | Structural corrections first (inflation path, forward refinancing rates, volume reference classes, exit-multiple shrink, timing slip, construction uplift), then residual bias b^u / b^f of +1.5/+1.0 (core), +3.0/+2.0 (value-add), +4.0/+3.0 (greenfield) pp a year. Cases read as P10/P50/P90; κ_g estimated from the archive |
| **Market-implied anchor** | y^MKT from LP bids (Jefferies segment index), listed infrastructure-trust discounts and FTSE GCI 50/50; a signal in the FBE, never NAV |
| **Synthetic defaults** | $7.2bn NAV, $1.6bn unfunded; weights REG 18 / CON_IDX 8 / CON_FIX 14 / TOLL 12 / AIR 8 / MID 10 / TOW 10 / DC 12 / MER 8%; vehicles CEF 40 / co-investment and direct 35 / OEF 25%; ≈60 positions (25 CEF interests, 20 direct/co-investment, 6 OEF, 9 CV stakes) [I]; marks generated as net IRR/MOIC with P10/P50/P90 cases; label SYNTHETIC |
| **Links** | **CF:** look-through leverage, maturity wall, FTP, φ(h, S) into the ladder. **Overlay:** real-rate and inflation hedges, FX. **Capital Solutions:** holdco preferred and NAV-loan quotes (firewalled). **Secondaries:** infrastructure LP pricing (firewalled); internal sales raise zero. **Private Credit:** infrastructure debt (boundary). **Energy & NR stream:** midstream oil and gas loadings, Z-state wrong-way. **Public Markets:** listed infrastructure anchor |

**Segment parameter table** (defaults used in `g11_infra_mc.py`; [I] unless tagged; replace with ADIC data):

| Segment | y₀ | μ (gross) | D_k | θ^E | β^q (ERP) | β^g | m (power) | OL | Leverage | DSCR₀ / lock-up | h | M (years) | σ^id | Anchors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REG | 5.0% | 8.5% | 9.0 | 1.3 | 0.6 | 0 | 0 | 1.3 | 65% | 1.45 / 1.15 | 0.85 | 9 | 3% | Ofwat 55% notional; EDHEC duration |
| CON_IDX | 7.0% | 8.5% | 7.7 | 1.3 | 0.5 | 0 | 0 | 1.2 | 80% | 1.25 / 1.20 | 0.95 | 15 | 3% | EDHEC contracted 7.67; leverage ≈90% |
| CON_FIX | 8.0% | 8.5% | 7.4 | 0.1 | 0.6 | 0 | 0.10 | 1.2 | 75% | 1.35 / 1.20 | 0.90 | 12 | 4% | EDHEC wind 7.40 |
| TOLL | 4.5% | 9.5% | 8.6 | 0.9 | 1.0 | 0.8 | 0 | 1.4 | 60% | 1.70 / 1.15 | 0.80 | 7 | 5% | EDHEC transport 8.56 |
| AIR | 3.5% | 10.0% | 11.6 | 0.6 | 1.4 | 1.8 | 0 | 2.0 | 55% | 1.80 / 1.15 | 0.85 | 7 | 6% | EDHEC airports 11.63, DD 34.9% |
| MID | 8.0% | 9.5% | 7.7 | 0.4 | 1.0 | 0.6 | 0.15 | 1.5 | 50% | 2.50 / 1.15 | 0.90 | 6 | 5% | Energy link |
| TOW | 3.0% | 10.0% | 10.0 | 0.0 | 1.2 | 0.3 | 0 | 1.3 | 55% | 2.00 / 1.15 | 0.80 | 6 | 6% | Fixed escalators |
| DC | 2.0% | 11.0% | 11.0 | 0.2 | 1.6 | 0.5 | 0 | 1.6 | 50% | 1.90 / 1.15 | 0.60 | 5 | 8% | SIPA data vol 18.4%; NOI YoC 9–12% |
| MER | 8.0% | 10.0% | 7.7 | 0.8 | 1.3 | 0.3 | 0.80 | 1.5 | 40% | 1.80 / 1.20 | 0.80 | 8 | 6% | EDHEC merchant 7.70, DD 21.6% |

**Common factor and regime parameters.**

| Parameter | Value |
|---|---|
| Regime means of the real rate (N / I / C / G) | 1.8 / 2.4 / 0.8 / 2.4% |
| Regime means of π^e (N / I / C / G) | 2.3 / 3.3 / 1.6 / 3.8% |
| Regime means of real GDP growth (N / I / C / G) | 2.3 / 1.3 / −3.0 / 0.3% |
| Regime means of the power-price factor (N / I / C / G) | 0 / 0.15 / −0.30 / 0.35 |
| Regime means of the risk-premium factor q (N / I / C / G) | 0 / 0.20 / 1.00 / 0.40pp |
| Regime means of the credit-spread shock (N / I / C / G) | 0 / 25 / 200 / 50bp |
| Refinancing failure p^fail (N / I / C / G) | 0 / 1 / 15 / 3% of maturing debt |
| Mean reversion κ_r, κ_π, κ_p, κ_q (a year) | 0.3, 0.6, 1.2, 1.0 |
| Volatility σ_r, σ_π, σ_g, σ_p, σ_q | 0.6%, 0.4%, 1.5%, 30%, 0.25% (q correlated −0.5 with GDP shocks; r and π^e correlated +0.3) |
| Quarterly transition matrix, rows N / I / C / G | (0.92, 0.04, 0.025, 0.015) / (0.06, 0.86, 0.05, 0.03) / (0.15, 0.03, 0.80, 0.02) / (0.08, 0.10, 0.05, 0.77) |

In production these factors and regimes come from E.

---

## 7. Implementation notes

**Modules** [I]:

| Module | Contents |
|---|---|
| `infra/segments.yaml` | The parameter table, versioned and dated |
| `infra/asset_engine.py` | Structural forward-curve DCF and debt schedules (as `g11_durations.py`) |
| `infra/mc.py` | Vectorised segment engine on E's common random numbers (as `g11_infra_mc.py`) |
| `infra/vehicles.py` | CEF via RFT-TA v2 with yield and e_t exits; the OEF queue machine; CV offers |
| `infra/actions.py` | Kernel scoring and decision cards (as `g11_actions_queue.py`) |
| `infra/calibrate.py` | Simulated moments on economic and reported volatility, drawdown, duration and cash yield (targets in §6.9) |

**Algorithms.** NumPy vectorisation over paths × assets: about 8 seconds for 20k × 40 quarters × 9 segments. Value structurally at decision dates only, re-anchoring the duration form to the structural value between them. Least-squares Monte Carlo for refinancing and sale timing. A Kalman nowcast of V^E from N, listed infrastructure, rates and spreads.

**Numerical pitfalls:**
1. **Two durations.** Cash-flow-fixed and structural durations are different objects. Apply a rate shock once, through the discount rate *and* refinancing coupons; never add −D·Δr on top of a structural revaluation.
2. **Negative equity.** Floor V^E at 0 when V^A < V^D and route the asset to default and recovery.
3. **Terminal value.** It dominates long concessions; cap it and test sensitivity to the exit multiple.
4. **Nominal and real.** Discount nominal cash flows on nominal curves, and index the RAB and revenues on the same π path.
5. **Smoothing.** De-smooth once (FBE); re-smooth only for reporting.
6. **Jumps.** Book a jump's value impact at arrival and its cash impact over its decay.
7. **Conventions.** Quarterly conversion per main §0; common random numbers across actions; SYNTHETIC labels.

**Tests:** reproduce the §4.6 table to ±0.05 and the §4.4 φ table on its seeds; LEVER = ADD + REFI; V2 netting (an intra-ADIC sale changes liquidity by 0); calibration bands in CI.

---

## 8. Risks and limitations

1. **Measurement.** Appraisal series (MSCI, Cambridge Associates) and mark-to-model series (EDHECinfra/SIPA) differ in cash-yield basis, and SIPA's history before its 2019 launch is back-filled [S]. Preqin strategy medians rest on small, partly immature vintages.
2. **The model is illustrative.** Segment parameters are [I] and loosely calibrated. Contracted drawdowns run deeper than EDHECinfra's history. The regimes are a placeholder for E, and ω = 0.5 is a judgement.
3. **Pass-through.** The academic evidence is weak in the short run (Wurstbauer & Schäfers), and our θ^E values are structural, not estimated. Political caps and windfall measures are not modelled.
4. **Liquidity.** Wealth-channel evergreen terms (Stonepeak-type) differ from institutional open-end funds. Institutional queue sizes for 2023–26 (e.g. IFM GIF, J.P. Morgan IIF) were not verified [U]. d_dir is [I].
5. **Policy and transition risk.** US renewables policy, offshore-wind costs, AI-capex cyclicality and midstream stranding enter only through jumps and risk-premium loadings.
6. **Geopolitics.** The GCC share and its interaction with the owner's draw are assumptions [A].
7. **Sources.** Fundraising statistics conflict by definition. The search-budget cut-off left some practitioner facts (named cases, rating-agency DSCR criteria) as [P] or [U].

---

## 9. Open questions (what ADIC must supply or confirm)

1. **Size and mix.** The infrastructure share of the $18bn book (40% here is synthetic), the segment and vehicle mix, and whether "funds" includes open-end funds (with ADIC's share of each).
2. **Capital structures.** Look-through opco and holdco debt for every direct, co-investment and JV position: maturities, fixed share, covenants and DSCR history. This is the most valuable item for REFINANCE and LEVER.
3. **Revenue terms.** Indexation (index, lag, caps, floors), reset calendars, contract expiries and merchant tails.
4. **Forecast archive.** Infrastructure IRR/MOIC cases, and volume plans against actuals, to estimate bias and κ.
5. **GCC exposure.** Gulf-located or Gulf-traffic assets and their link to the owner's fiscal state.
6. **Boundaries.** Midstream (infrastructure or energy & natural resources?) and infrastructure debt (Private Credit?).
7. **Rights.** Consent, ROFR and drag rights; CV offer history; sell-down agreements.
8. **Classification.** Confirm that partial sell-downs are SELL (§6.1).
9. **Limits.** IC limits for merchant share, digital share, look-through leverage and the maturity wall (§6.5).

---

## 10. References

**Academic**
- Andonov, A., Kräussl, R., & Rauh, J. (2021). Institutional Investors and Infrastructure Investing. *Review of Financial Studies* 34(8), 3880–3934. https://doi.org/10.1093/rfs/hhab048 (open access: https://openaccess.city.ac.uk/id/eprint/33251/1/hhab048.pdf)
- Bain, R. (2009). Error and optimism bias in toll road traffic forecasts. *Transportation* 36(5), 469–482. https://doi.org/10.1007/s11116-009-9199-7
- Bianchi, R. J., Bornholt, G., Drew, M. E., & Howard, M. F. (2014). Long-term U.S. infrastructure returns and portfolio selection. *Journal of Banking & Finance* 42, 314–325. https://doi.org/10.1016/j.jbankfin.2014.01.034
- Bitsch, F., Buchner, A., & Kaserer, C. (2010). Risk, return and cash flow characteristics of infrastructure fund investments. *EIB Papers* 15(1), 106–136. https://www.eib.org/files/efs/eibpapers/eibpapers_2010_v15_n01_en.pdf (working paper: https://www.efmaefm.org/0EFMSYMPOSIUM/2011-Toronto/papers/bitsch.pdf; dataset description via https://www.infrainsightblog.com/analysis-of-infrastructure-investments-produces-surprising-findings)
- Blanc-Brude, F., & Tran, C. (2019). *Which Factors Explain Unlisted Infrastructure Asset Prices? Evidence from 15 years of secondary market transaction data.* EDHEC Infrastructure Institute. https://www.edhecinfraprivateassets.com/wp-content/uploads/2019/01/blanc-brude_and_tran_2019.pdf
- Blanc-Brude, F., & Gupta, A. (2021). *The Volatility of Unlisted Infrastructure Investments: Valuation drivers and trends, 2000–2021.* EDHECinfra. https://www.edhecinfraprivateassets.com/wp-content/uploads/2021/05/P74_EDHEC-LTIIA_Volatility.pdf
- Flyvbjerg, B., Skamris Holm, M. K., & Buhl, S. L. (2005). How (In)accurate Are Demand Forecasts in Public Works Projects? The Case of Transportation. *Journal of the American Planning Association* 71(2), 131–146. https://doi.org/10.1080/01944360508976688 (arXiv: https://arxiv.org/abs/1303.6654)
- Gupta, A., & Van Nieuwerburgh, S. (2021). Valuing Private Equity Investments Strip by Strip. *Journal of Finance* 76(6), 3255–3307. https://doi.org/10.1111/jofi.13073 (infrastructure result as cited in Andonov et al. 2021)
- Rödel, M., & Rothballer, C. (2012). Infrastructure as Hedge against Inflation—Fact or Fantasy? *Journal of Alternative Investments* 15(1), 110–123. https://doi.org/10.3905/jai.2012.15.1.110 (bibliography verified; findings not re-read)
- Wurstbauer, D., & Schäfers, W. (2015). Inflation hedging and protection characteristics of infrastructure and real estate assets. *Journal of Property Investment & Finance* 33(1), 19–44. https://doi.org/10.1108/JPIF-04-2014-0026

**Index providers, market data and practitioners**
- CBRE Investment Management (Nov 2025). *Infrastructure Quarterly: Q4 2025.* https://mediaassets.cbre.com/-/media/project/cbre/bussectors/cbreim/insights/articles/2025/december/infrastructure-quarterly-q4-2025/infrastructure-quarterly-q4-2025.pdf
- CBRE Investment Management (25 Jun 2026). *Infrastructure Quarterly: Q2 2026.* https://www.cbreim.com/insights/articles/infrastructure-quarterly-q2-2026
- CBRE Investment Management (13 Oct 2026). *Infrastructure Quarterly: Q3 2026* (data as of 30 Jun 2026). https://www.cbreim.com/insights/articles/infrastructure-quarterly-q3-2026
- EDHECinfra / Bloomberg Media Studios (28 Apr 2021). *Inflation Risk: How Exposed Are Investors in Infrastructure?* https://sponsored.bloomberg.com/article/edhec-infra/inflation-risk-how-exposed-are-investors-in-infrastructure
- Global Infrastructure Hub (2024). *Infrastructure Monitor 2024: Infrastructure funds* (citing Preqin 2024b). https://cdn.gihub.org/umbraco/media/5551/section-2_infrastructure-funds_monitor-2024.pdf
- Infrastructure Investor (17 Jun 2026). *infra300 posts best monthly return in 2026.* https://www.infrastructureinvestor.com/infra300-posts-best-monthly-return-in-2026/
- Jefferies (Jul 2026). *Global Secondary Market Review.* https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
- Moody's Investors Service (10 Jun 2020). *Infrastructure & Project Finance – Global: Defaults & recoveries.* https://ma.moodys.com/rs/961-KCJ-308/images/Default%20Reports%20-%20Infrastructure-Project-Finance-Global%20-%2010Jun20.pdf
- MSCI (2026). *Global Private Infrastructure Asset Index: Q1 2026 results.* https://www.msci.com/data-and-analytics/private-asset-solutions/global-private-infrastructure-asset-index-q1-2026-results
- MSCI (20 Nov 2025). *The New Drivers of Infrastructure Performance.* https://www.msci.com/research-and-insights/quick-take/the-new-drivers-of-infrastructure-performance
- Preqin (2026). *Unlisted infrastructure in 2026 and why selectivity matters.* https://www.preqin.com/insights/research/blogs/unlisted-infrastructure-in-2026-and-why-selectivity-matters
- Scientific Infra & Private Assets (Jan 2026). *Expected Returns in Private Equities and Infrastructure: 2026 Capital Market Assumptions.* https://publishing.sipametrics.com/papers/20260115_capital_market_assumptions.pdf
- Scientific Infra & Private Assets (May 2026). *Private Infrastructure Indices Factsheet.* https://publishing.sipametrics.com/factsheets/indices/LATEST_infraMetrics_equity_market_indices_factsheet.pdf
- Stonepeak-Plus Infrastructure Fund LP (2026). *Form 10-K for FY2025.* https://www.sec.gov/Archives/edgar/data/0002045458/000204545826000012/sp-20251231.htm
- The UK Water Report (9 Nov 2025). *Financial resilience and positive returns lacking* (on Ofwat, *Monitoring Financial Resilience 2024–25*). https://www.thewaterreport.co.uk/single-post/financial-resilience-and-positive-returns-lacking

**Project files cited as [S-prior]**
- `research/dossiers/02_endowment_swf.md` (peer mandates)
- `research/dossiers/03_sovereign_alm.md` (Gulf-war data, EIA STEO)
- `research/dossiers/04_pe_cashflows.md` (McKinsey 2026 infrastructure DPI; RFT-TA infrastructure defaults)
- `research/dossiers/05_secondaries_navfin.md` (Evercore infrastructure secondary targets)
- `research/dossiers/07_return_fusion.md` (J.P. Morgan 2027 LTCMA; Green Book uplifts; FBE forms)
- `research/groups/dossiers/G9_synthetic_data.md` (MSCI calendar-2025 returns)
- `research/groups/01_GROUPS_SYNTHESIS.md` (cash map, VRC evergreen queues, ladder, rules)

**Computations (SYNTHETIC)**
- `research/groups/addenda/G11_calcs/g11_durations.py` → `g11_durations_results.json`
- `research/groups/addenda/G11_calcs/g11_infra_mc.py` → `g11_infra_mc_results.json`
- `research/groups/addenda/G11_calcs/g11_actions_queue.py` → `g11_actions_queue_results.json`
