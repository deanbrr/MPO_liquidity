# G10 · Real Assets: real estate

## Return, cash-flow, valuation and leverage model for closed-end funds, open-end core vehicles, joint ventures and direct assets

**Stream:** G10 (Real Assets, the eighth group) · **Date:** 2026-10-18 · **Status:** research dossier, design-grade · **Companions:** main report `research/00_SYNTHESIS.md` (§1, §2.3, §4.1–4.7), groups report `research/groups/01_GROUPS_SYNTHESIS.md` (§2–4, §6), design brief §8–9, sibling dossiers G14 (Real Assets actions and financing) and G15 (Real Assets book and cash map). **Calculations:** `research/groups/addenda/G10_calcs/`
- `g10_reit_series.py` → `g10_reit_series_results.json` (public Nareit data);
- `g10_public_and_arith.py` → `g10_public_and_arith_results.json` (public-data timing, desmoothing, queue calibration, decision arithmetic);
- `g10_re_engine.py` → `g10_re_engine_results.json`, `g10_re_engine_stdout.txt` (synthetic Monte Carlo of the real-estate sleeve, 10,000 paths × 20 quarters × 6 scenarios, common random numbers).

> **SYNTHETIC-DATA NOTICE.** Every ADIC position, sleeve size, cash map, refinancing gap, queue payout and decision example below is computed on a synthetic book: real estate $9.0bn NAV and $1.6bn unfunded inside the Real Assets working allocation of $18bn (sub-book totals aligned with G15's synthetic book; position detail is G10's). None of it is ADIC data. Tables carrying [I-calc] synthetic values end with *SYNTHETIC – NOT ADIC DATA*.

**User confirmations used (context §1A, design brief §8–9, 2026-10-18).** Real Assets covers real estate, infrastructure, and energy & natural resources (agriculture and timber excluded), held through funds, co-investments, and direct assets or JVs, inside the ~60% private allocation. Group marks are archived quarterly, as net IRR/MOIC per holding with downside/base/upside cases.

**Tags.** [S] read in-session at the primary page or file; [S-sec] via a search summary or secondary relay; [P] practitioner material; [I] inference or design default; [I-calc] my computation (public-data or synthetic, as labelled); [A] client statement or working assumption; [U] unverified, never load-bearing. **Research note:** the session's shared web-search budget was exhausted part-way through. Later facts were verified only by fetching known primary pages and files. Gaps are flagged in §8.

**Symbols** follow the main and groups reports: S_t macro regime {expansion, late-cycle/inflationary, crisis, recovery}; Z_t oil/fiscal shock type (GW = Gulf war, DB = demand bust); ℓ the liquidity premium from H's duals. New here:
- V^T true (transaction) value; V^A appraisal value;
- c cap rate; NOI net operating income; κ^cap capex share of value;
- G = ln V^A − ln V^T, the stale-appraisal gap; ν the listed-market sentiment wedge (REIT-implied value minus true value, in logs);
- e^RE ∈ {O, N, D, F} the real-estate transaction window (open, normal, drought, frozen);
- Q the open-end redemption queue (share of fund NAV); θ = economic ÷ reported NAV (as in G14).

---

## 1. Executive summary

1. **Today's state is a rate shock that appraisals have not absorbed.** The 10-year was 5.10% on 15 October (5.36% on 7 October, the highest since 2002), after a Fed hike to 3.75–4.00%; Brent is ≈$110 with Hormuz closed [S-sec]. REITs fell 8.3% from July to September [I-calc on Nareit data], while ODCE's preliminary Q3 return was +1.71% (+0.69% appreciation) [S]. The NPI appraisal cap rate (≈4.4%) sits below the 10-year; RCA transaction cap rates run from 5.6% to 8.3% [S]. Green Street: "If this rise in yields sticks, property prices are likely to go down" [S]. **Consequence:** every holding starts with a stale-appraisal gap G₀ of 5–8%, and actions are scored on a nowcast V\*, not on marks.
2. **The 2022–24 repricing calibrates timing and smoothing** [I-calc on public data]. ODCE fell 18.8% in total return (≈24% in appreciation) from Q3-2022 to Q2-2024. REITs relevered to ODCE leverage fell 25.7%, and ODCE's trough lagged theirs by three quarters. A Geltner filter with α ≈ 0.5–0.6 reproduces the listed-implied fall; α = 0.7 overshoots to −35%. Over 2022Q1–2026Q3 the two series end within 1pp of each other: same assets, different timing.
3. **No net premium for private or non-core real estate after adjustment.**
   - Restated private and REIT returns are statistically indistinguishable (Pagliari, Scherer & Monopoli 2005) [S-sec].
   - Value-add and opportunistic funds trail leverage-matched core by 326bp and 285bp a year (Bollinger & Pagliari 2019) [S-sec].
   - 375 US closed-end funds trailed REITs by 165bp a year and matched ODCE (Arnold, Ling & Naranjo 2021) [S].
   - MSCI's KS-PME falls from 1.07 to 1.01 once each fund's leverage is applied [S].
   - Delegation disproportionately cuts returns (Andonov, Eichholtz & Kok 2015) [S-sec].
4. **Real estate will not fill the DPI gap.** Real-estate fund distributions "breached new lows" in 2025 (MSCI), and LP interests trade at 68% of NAV (Jefferies) [S].
   - On the synthetic $9.0bn sleeve, year-1 net cash is −$0.10bn (P50; P5 −$0.18bn) from today's state, and −$0.21bn in a demand bust or credit crunch. Only the benign scenario is clearly positive: +$0.12bn in year 1, then +$0.47bn [I-calc].
   - Income reaching ADIC is ≈2.1% of NAV, because new debt at ≈6.8–7.6% costs more than cap rates of 5.6–6.9%.
   - G15's official T4′ line is harsher: it scales calls ×1.38, while G10 lets deployment slow in frozen markets (§6.5).
5. **Leverage and refinancing are the tail risks** [I-calc].
   - Look-through debt is $8.0bn on $17.0bn of GAV (LTV 47%, against NBIM's 25% portfolio cap [S]), and $3.4bn matures within 24 months.
   - Refinancing gaps are $0.22bn (6.6% of maturing debt) from today's state and $0.81bn (22.8%) in a GFC-type crunch.
   - A 2021 loan at 65% LTV, refinanced at a 6.0% cap rate with +10% NOI, needs a cure of 19% of value.
   - Backdrop [S-sec]: $875bn of US CRE mortgages mature in 2026 (MBA); CMBS office delinquency is 12.16% (Trepp, September); banks extended about half of maturing loans in 2023–25 (Glancy).
6. **The open-end queue machine is calibrated on ODCE** [I-calc].
   - Specification: requests of 0.6% of NAV a quarter plus 0.12 × the lagged stale-NAV premium; payouts of ≈1.2–1.5% of NAV a quarter; 8% of the queue withdrawn each quarter once the premium is gone.
   - Fit: it reproduces the 19.3% peak (model 19.4%) and the ≈10% queue of Q1-2026 (model 9.8%).
   - From today's ≈8% queue, a full ADIC redemption is 34% paid within a year (25% at P5). In a credit crunch it is 23% within a year and 48% within three.
   - Units therefore enter the ladder as P5 cash by horizon, never at NAV.
7. **Price on V\*, report V^A.** Trough lags are 3–4 quarters, and marks reach 80% of a true move after ≈3.7–5.5 quarters (α 0.55–0.70). Individual appraisals miss sale prices by more than 12%, and portfolios by 4–5% (Cannon & Cole 2011) [S]. At a 10% stale gap, redeeming through a queue is worth 92.5–94.7% of NAV, against 90.5% for holding [I-calc].
8. **Forecasts need structural correction before bias shrinkage.** Business plans embed exit-cap, rent-growth, capex and hold optimism. Early projected IRRs are "quite speculative" (Arnold, Ling & Naranjo) [S], and fund class does not predict returns (Fisher & Hartzell) [S-sec]. Proposed priors for b^u run from +0.5pp a year (core) to +4.0pp (opportunistic) [I].
9. **Gulf real estate is wrong-way with the owner's draw.** Dubai home sales fell 47% by value in Q3-2026 and prices are 5–15% lower since end-2025 [S]; in 2008–10 prices fell ≈55–58% [S-sec]. Gulf assets load on Z (GW, DB) and on oil through the fiscal channel.
10. **Inflation pass-through is partial.** Same-store NOI grew 0.78% in the year to Q2-2026 [S]. In synthetic stagflation (CPI ≈5%) NOI falls 0.9% a year, because sticky opex and long leases outrun rent resets [I-calc].
11. **Actions** (G14 holds the instrument library).
    - LEVER rarely passes in 2026: it needs c − κ^cap + g > r_D plus charges.
    - Cash-out REFINANCE belongs at maturity, on low-LTV assets.
    - A fund-interest SELL at 68% clears HOLD only if θ ≤ ≈0.85, forward growth is low and ℓ ≥ ≈5%.
    - A JV sell-down is a partial SELL.

---

## 2. Core concepts and theory

**2.1 Value, return and the cap rate.** For an income property with next-period NOI₁, discount rate r and growth g,

$$V_t=\frac{NOI_{t+1}}{r_t-g_t}=\frac{NOI_{t+1}}{c_t},\qquad r_{t+1}\approx\underbrace{\tfrac{NOI_{t+1}}{V_t}}_{\text{yield}}-\underbrace{\kappa^{cap}_{t+1}}_{\text{capex}}+\underbrace{g^{NOI}_{t+1}}_{\text{NOI growth}}-\underbrace{\tfrac{\Delta c_{t+1}}{c_{t+1}}}_{\text{cap-rate change}}+\text{interaction}.$$

These five terms are exactly NCREIF's attribution components (NOI yield, CapEx %, NOI growth, cap-rate change, interaction) [S: NCREIF 2Q-2026 slides]. Log-linearizing the present-value identity gives $\ln c_t\approx k+\sum_j\rho^j E_t(r_{t+1+j}-g_{t+1+j})$. The cap rate therefore moves with expected returns *and* expected rent growth. Using US metro transaction data, Plazzi, Torous & Valkanov (2010) attribute up to 30% of return variability to expected-return variation. Cap rates track expected returns for apartments, retail and industrial, and only marginally forecast office rent growth [S-sec]. Beyond Treasuries, cap rates load on the economy-wide risk premium and on credit availability (Chervachidze, Costello & Wheaton 2009) [S-sec]. The engine's cap-rate target therefore carries a 10-year term, a credit-spread term and a credit-availability term (§6.2).

**2.2 Leases filter inflation.** NOI = in-place rent × occupancy − opex. In-place rent converges to market rent at the lease-roll rate ρ ≈ Δt/WALT, plus contractual escalators. Opex (taxes, insurance, wages) reprices at inflation immediately. Hence:
- NOI's short-run inflation beta is below one, and can be negative for long-lease, high-opex assets;
- long-run pass-through depends on market-rent elasticity β_π;
- residential, hotels and self-storage reprice within a year; office, logistics and net-lease retail take 5–10 years.

**2.3 Leverage.** For asset return r_U, debt cost r_D and debt-to-equity D/E:

$$r_E=r_U+\tfrac{D}{E}(r_U-r_D).$$

Leverage is accretive in expectation only if $E[r_U]=c-\kappa^{cap}+g>r_D$. Its *cash* accretion requires c > r_D. Non-recourse debt makes equity a call on V struck at D; G14 §2.4 adds ϖ, the probability that ADIC honours underwater debt for reputational reasons.

**2.4 Appraisal smoothing.** Appraisers rationally blend new evidence with prior values (Geltner 1991, 1993):

$$r^A_t=(1-\alpha)\,r^T_{t-\ell}+\alpha\,r^A_{t-1}\quad\Longleftrightarrow\quad r^T_{t-\ell}=\frac{r^A_t-\alpha r^A_{t-1}}{1-\alpha}.$$

- Desmoothing restores volatility. It also amplifies noise, and over short samples it biases means (Fisher, Geltner & Webb 1994; later ERES work [S-sec]).
- Delfim & Hoesli (2021) add a robust filter so that extreme desmoothed values do not dominate risk metrics [S-sec].
- Transaction-based indices avoid the smoothing and lagging bias (Fisher, Geltner & Pollakowski 2007) [S-sec].
- **Rule (consistent with main §4.3):** de-smooth for risk, or nowcast with staleness for value, but never both on the same series.

**2.5 Open-end vehicles and stale NAV.**
- Mechanism: redemptions settle at the appraisal NAV. When V^A > V^T, a redeemer sells above value and the remaining holders absorb the dilution. That creates a first-mover advantage, and queues form exactly when the gap is widest (run mechanics: G14 §2.5).
- Treatment: a redemption right is a claim on other investors' new money, on retained income and on dispositions. All three shrink in stress, so the payout rate, not the NAV, is the liquidity variable.

**2.6 Closed-end real-estate funds** are commitment vehicles, like PE.
- **Calls:** value-add and opportunistic funds deploy quickly when transactions are open and slow sharply when they freeze.
- **Distributions:** they carry a thin income floor and depend on exits, so their distributions load on transaction volume and the cap-rate path.
- **Pricing:** the secondary price is (1 − d) × reported NAV, where d bundles θ < 1, buyers' required returns and illiquidity.

**2.7 Private versus listed.**
- Both price the same buildings, at different frequencies and leverage and under different fees.
- After desmoothing and leverage matching, the return gap is small (§4.2). Listed REITs and transaction indices are therefore the natural *market-implied anchor* for the fourth mark.
- Caveats: REITs carry a sentiment wedge ν, embed operating platforms, and their sector mix differs from private books.

---

## 3. Methods, models and trade-offs

| Component | Chosen method | Alternatives considered | Why |
|---|---|---|---|
| NOI | Lease-roll model by sector × region: market rent, roll rate 1/WALT, escalators, occupancy, sticky opex (§6.2) | Reduced-form AR(1) NOI growth; tenant-level DCF | Captures partial inflation pass-through, mark-to-market gaps and operating leverage with eight parameters per sector. Tenant-level DCF needs rent rolls (an ADIC data request); AR(1) cannot separate inflation from real drift |
| Cap rate | Partial adjustment toward a target loaded on Δy10, ΔBaa, a credit-availability premium by regime and a structural drift (office) | Real-rate regression; present-value VAR; REIT-implied cap rates as the state | The target maps onto main §4.1's factors (rates, spreads, regime). A VAR needs long sector cap-rate histories. REIT-implied cap rates enter as the observation, not the state |
| Value | V^T = NOI × (1 + ĝ_fwd)/c | Full DCF with exit cap | Equivalent at portfolio scale. DCF is reserved for business-plan translation (§6.7) |
| Appraisal | Log-level Geltner smoothing, α by vehicle, one-quarter lag, noise | Seasonal annual reappraisal; Kalman nowcast | α is calibrated on the 2022–24 episode. The Kalman nowcast is the FBE's job (§6.7) |
| Debt | Maturity hazard on legacy debt; refinancing capacity min(LTV_max V^T, NOI/(DSCR_min r_new)); extension, cure or hand-back; cash trap at DSCR < 1.10 | Loan-level Merton default; CMBS-style intensity models | Liquidity, not default probability, is ADIC's binding risk. Cures are the cash event |
| Open-end funds | Queue machine driven by the stale-NAV premium, payout capacity from income, dispositions and contributions, and withdrawals; pro rata | FIFO; logit gate model | Pro rata is now standard (G14 §2.5). Two fitted parameters reproduce the ODCE path |
| Closed-end funds | RFT-TA v2 with real-estate rates and an effective-age clock; income floor = 80% of positive property cash flow after debt service | Fixed income yield Y | A fixed Y overstates distributions under negative leverage |
| JVs and direct | Asset engine at vehicle level × ADIC share; capex and development draws; cures and shortfalls paid by owners | Waterfall-level promote modelling | Promotes matter for the partner's incentives, not ADIC's liquidity; flagged for the deal-level tool |

**Trade-offs.**
1. *Realism versus data.* Lease-roll and debt-tape engines need ADIC's property data (§9). Until then sector cohorts carry them.
2. *Two cap-rate layers.* NCREIF appraisal cap rates (≈4.4%) and RCA transaction cap rates (5.6–7.5%) differ in quality, mix and NOI basis. The engine runs on appraisal-consistent levels per holding and uses transaction levels only for lender sizing tests and outside-view checks.
3. *Smoothing as a parameter.* α = 0.55 (open-end) to 0.70 (direct) is a calibration choice. A higher α hides more risk and lengthens the catch-up, while a lower one makes marks noisier. The FBE should estimate α per manager from the archive.
4. *No published real-estate Takahashi–Alexander set.* Takahashi & Alexander (2002) publish venture parameters. Cao & van Beek (2025) extend the model with latent macro factors across PE, real estate, credit and infrastructure, but their real-estate estimates were not accessible this session.
   - G10 keeps dossier 04's real-estate call schedule (25/30/35/40% of remaining unfunded) and smoothing (0.65).
   - It replaces the fixed 3% yield with an income floor tied to property cash flow after debt service.
   - Exits run on an effective-age schedule loaded on e^RE, anchored to MSCI's record-low real-estate distributions in 2025 [S] and to G15's realization rates (18% of NAV normal, 6% drought).

---

## 4. Empirical evidence and current market data

### 4.1 Long-run and recent returns

**NCREIF and Nareit, annualized to 30 June 2026** (NCREIF ODCE attribution webinar, 16 Sep 2026) [S].

| Horizon | NPI (unlevered, gross) | NPI-ODCE property | NFI-ODCE (fund, gross) | FTSE Nareit | S&P 500 |
|---|---|---|---|---|---|
| 1 year | 5.0% | 4.9% | 4.4% | 15.4% | 22.3% |
| 3 years | 1.2% | 0.9% | −0.6% | 10.1% | 20.6% |
| 5 years | 3.4% | 3.1% | 2.7% | 3.7% | 13.4% |
| 10 years | 4.8% | 4.5% | 4.6% | 5.8% | 15.5% |
| 20 years | 6.1% | 5.8% | 5.4% | 6.6% | 11.4% |
| 30 years | 8.2% | 8.0% | 7.8% | 9.4% | 10.4% |
| 40 years | 7.2% | 6.6% | 6.6% | 9.4% | 11.2% |
| Min / max of the slide's "3-yr trailing" series over 40 years (read as rolling 3-year annualized returns [I]) | −4.7% / 18.2% | −5.8% / 17.3% | −11.0% / 18.4% | −25.0% / 42.2% | −16.2% / 32.9% |

- **Recent quarters** [S: NCREIF]. ODCE Q2-2026 was 1.49% gross (1.29% net), with income 1.02% and appreciation 0.47%. Its year to June was 4.45%. Q3-2026 preliminary is 1.71% (appreciation 0.69%). NPI Q2-2026 was 1.29% (income 1.17%, appreciation 0.12%) on 13,160 properties worth $943bn.
- **Strategy returns, MSCI APRE fund index, to March 2026** [S: MSCI, 12 Aug 2026].
  - 12 months: core 3.8%, core-plus 3.1%, value-add 1.1%, opportunistic −0.5%.
  - 15 years: core 5.8%, value-add 7.9%, opportunistic 7.3% (all funds 6.6%).
- **MSCI Global Private Real Estate closed-end fund index** [S: MSCI Private Capital Benchmarks, Q2-2026].
  - Calendar years: 2023 −6.0%, 2024 −2.6%, 2025 +2.3%. Quarterly: −0.1, +0.1, −0.1, +0.2 (Q3-25 to Q2-26).
  - MSCI ACWI Real Estate: +7.3% in 2025 and +5.9% in Q2-26.
  - Five-year cumulative +4%, "the clear laggard" of private capital. Coverage: 1,779 real-estate funds, $1.31tn cumulative capitalization.
- **FTSE Nareit All Equity REITs, total return** [I-calc on Nareit's monthly file, through September 2026].
  - Calendar years: 2022 −24.95%, 2023 +11.36%, 2024 +4.92%, 2025 +2.27%; 2026 to September +7.93%.
  - Drawdowns on month-end data: GFC −68.3% (January 2007 → February 2009); COVID −24.4%; 2022–23 −31.4%; July–September 2026 −8.3%.
  - The dividend yield is 3.93%, against 2.59% in December 2021.

### 4.2 Academic evidence: private versus listed, fees and fund performance

| Study | Sample | Finding | Tag |
|---|---|---|---|
| Pagliari, Scherer & Monopoli (2005), *REE* 33(1) | NCREIF vs REITs 1981–2001, controlling property mix, leverage, smoothing | Restated means and volatilities are not statistically different; the gap narrowed to ≈60bp in 1993–2001 | [S] metadata; [S-sec] findings |
| Riddiough, Moriarty & Yeatman (2005), *REE* 33(1) | Private vs public asset performance | Citation verified; findings not retrieved this session | [S] metadata; findings [U] |
| Bollinger & Pagliari (2019), *JPM* 45(7) | Non-core fund composites 2000–2017 | Against core levered to equal volatility: value-add −326bp, opportunistic −285bp a year. Core leverage < 25%; matching volatility needs ≈55% (value-add) and ≈65% (opportunistic) | [S] metadata; [S-sec] CFA Institute summary |
| Pagliari (2017), *REE* | Strategy indices | Value-add strongly underperforms core risk-adjusted; opportunistic weakly | [S-sec] |
| Arnold, Ling & Naranjo (2021), Nareit-hosted paper | 375 US closed-end funds (2000–2014 vintages, Cambridge Associates) | Mean IRR 8.69% vs REIT-equivalent 10.34% (−165bp); median +13bp; 53% underperform, 68% after a 425bp risk adjustment. Against ODCE, mean +126bp, median +19bp. Higher-risk funds 7.74% vs lower-risk 9.21%. Estimated closed-end leverage 60–70% vs REITs 35–40% | [S] |
| MSCI, Robson & Harmse (Aug 2022) | 145 US closed-end funds, 2005–2020 vintages, Burgiss | KS-PME 1.07 unlevered, 1.01 levered. 58% beat the unlevered index, 48% the levered one; 2005–07 vintages mostly lost | [S] |
| Fisher & Hartzell (2016), *JREFE* | Burgiss real-estate fund cash flows | Class labels do not predict performance; development exposure predicted poor results for pre-GFC vintages | [S-sec] |
| Andonov, Eichholtz & Kok (2015), *JFM* 22 | Pension real-estate allocations | Large funds invest internally at lower cost with higher net returns; delegation disproportionately reduces returns | [S] metadata; [S-sec] findings |
| Gupta & Van Nieuwerburgh (2021), *JF* 76(6) | Strip valuation of fund cash flows | Risk-adjusted profit negative on average (real estate −17¢ per $ in the WP) | [S] via dossier 04 |
| Gupta, Mittal & Van Nieuwerburgh (2026), *AER* 116(2) | NYC office revaluation | Office values −45% in 2020 and −39% in the long run ($453bn) | [S] |

### 4.3 The 2022–26 repricing by vehicle and sector

**Timing and smoothing** (public-data computation, `g10_public_and_arith.py`) [I-calc].

| Series, 2022Q1–2026Q3 | Peak → trough | Drawdown | Notes |
|---|---|---|---|
| NFI-ODCE gross total return | 2022Q3 → 2024Q2 | −18.8% | Appreciation-only ≈ −23.7% (income netted at 0.9%/qtr, an approximation) |
| FTSE Nareit All Equity, quarterly | 2021Q4 → 2023Q3 | −29.2% | −31.4% on month-end data |
| REITs unlevered at 33%, relevered to 25% | 2021Q4 → 2023Q3 | −25.7% | Debt cost 4.5% |
| ODCE desmoothed, α = 0.5 / 0.6 / 0.7 / 0.8 | — | −24.2 / −28.2 / −35.5 / −49.8% | α ≈ 0.5–0.6 matches the listed-implied fall |

- **Lead–lag.** The correlation of ODCE's return with REITs' return k quarters earlier is −0.44 at k = 0, 0.10 at k = 1, 0.37 at k = 2, 0.32 at k = 3 and 0.31 at k = 4. The trough lag is three quarters.
- **Stale-NAV gap.** ln(ODCE) − ln(relevered REIT), cumulated from end-2021, peaked at +41% in 2022Q3. It was +8% in 2024Q1, −6% in 2026Q2 and +1% in 2026Q3. Over the full period the two series end within 1pp.

**Sector dispersion.**
- **RCA CPPI, May 2026** [S]: all property +1.6% year on year. CBD office remains 50% below its March 2022 peak (5-year −45.2%). Industrial is up 10% since July 2022, while apartments are 20% and retail 7% below that point.
- **Green Street** [S-sec, June 2026]: all property 14% below the 2022 peak; office 34%, apartments 19%, industrial 11% and self-storage 22% below.
- **Europe** [S, Green Street, 8 Oct 2026]: the CPPI fell about 1% in Q3-2026 (office −1.7%, industrial −2.1%, residential −2.0%) as bid yields widened.

### 4.4 Current fundamentals and yields (October 2026)

| Item | Value (as of) | Source |
|---|---|---|
| NPI occupancy | 92.2% market-value weighted (Q2-26) | NCREIF slides [S] |
| Same-store NOI growth, rolling 4Q | 0.78% (Q2-26), from 3.16% (Q1-23); between −0.33% and +0.49% through 2024–25 | NCREIF slides [S] |
| NPI appraisal cap rate | ≈4.4% ("essentially flat"); income yield 4.7% (NPI), 4.1% (ODCE) | NCREIF slides [S]; RCLCO [S] |
| ODCE cap rates | 4.5–4.7%; existing assets ≈17% below replacement cost; new supply ≈54% below peak; debt ≈27% of assets, ≈4.5% cost, > 75% fixed | Accordant, Q1-26 [S] |
| Transaction cap rates, trailing 12 months (Feb-26) | Apartment 5.6%; industrial 6.4%; data centre 6.8%; retail 6.9%; senior housing 7.1%; CBD office 7.3%; suburban office 7.5%; hotel 8.3% | MSCI RCA Capital Trends [S] |
| US transaction volume | $556bn trailing 12 months (+21%) to Feb-26 | MSCI RCA [S] |
| Bid and credit intensity | JLL Global Bid Intensity 105; Credit Intensity 117 (May 2026) | NCREIF slides, citing JLL [S] |
| Sales versus marks | Sold properties "clear within ±4% of current marks"; trailing losers sell more often | NCREIF slides [S] |
| Industrial mark-to-market | Market-to-contract rent gap 15–36% by building size (ODCE, Q2-26) | NCREIF ODCE slides [S] |
| Data centres | ≈19% one-year trailing unlevered return | Accordant [S] |
| Allocations | Target allocations to real estate fell in 2025 for the first time in 13 years; investors tilted to real-estate debt | MSCI, citing Hodes Weill & Cornell [S] |

**What the yields imply** (B2, `g10_public_and_arith.py`) [I-calc].
- At the NPI appraisal yield, the premium over the 10-year is only 0.3–1.3pp: $y+g-\kappa^{cap}-y_{10}$ with y = 4.7%, κ^cap = 1.3% and g = 2–3%.
- On RCA apartment and industrial cap rates the premium is ≈1.7–2.5pp.
- Restoring a 2.5pp premium at g = 2–3% and κ^cap = 1.2% needs cap rates of 5.8–6.8%.
- Repricing grid (`cap_rate_shock_value_change_pct`): +50bp on a 4.5% cap rate costs 10.0% of value at flat NOI (7.3% with 3% NOI growth); +100bp costs 18.2%; +100bp on 5.5% costs 15.4%.

### 4.5 Debt markets and the maturity wall

- **Maturities** [S-sec: MBA, 9 Feb 2026]: $875bn (17% of ≈$5.0tn) matures in 2026, after $957bn in 2025; $652bn follows in 2027 (sector shares in G14).
- **Delinquency** [S-sec: Trepp via Yieldpro, Sep 2026]: CMBS 30+ days 8.02%. By sector: office 12.16%, multifamily 8.04%, retail 6.58%, lodging 6.18%, industrial 1.14%. Including performing matured balloons the rate is 9.66%.
- **Extend-and-pretend.**
  - Crosignani & Prazad (NY Fed SR 1130, revised June 2026): weakly capitalized banks extended distressed CRE loans to preserve capital, building near-term maturities [S]. The 2024 version's ≈$400bn of near-term maturities (27% of bank capital) is from press coverage [S-sec].
  - Glancy (FEDS, 2026), on Y-14Q data: banks extended about half of maturing loans in 2023–25, as before the pandemic. Stress-era extensions were 5.1pp more likely to require a ≥5% paydown [S-sec].
- **Lending standards** [S: Fed SLOOS, July 2026]: modest-to-moderate net easing for nonfarm nonresidential and multifamily loans, before the September hike (G14: FRED net tightening fell from 68.3% in Q3-2023 to −11.3% in Q3-2026).
- **Lending terms** (via G14 [S]: CBRE, Q2-2026): commercial spread 204bp, LTV 59.6%, DSCR 1.43, debt yield 10.2%, average rate 5.7%. With the 10-year now ≈90bp higher than in Q2, all-in fixed rates of ≈6.8–7.1% for core and ≈7.6% or more for transitional loans are my inference [I].
- **Negative equity** (via G14 [S]): 14% of CRE loans and 44% of office loans exceed property value (Jiang, Matvos, Piskorski & Seru).

### 4.6 Vehicle liquidity in stress

**Open-end US core.**
- Queues [S: Callan; Accordant; G14 adds Meketa and Townsend]: 9.2% of NAV (Q4-2020); 19.3% (Q1-2024; average 16.4%, median 13.4% in Q4-2024, with large funds between 6% and 33% and one at 56%); ≈12% (mid-2025); just above 10% (Q1-2026). The GFC peak was ≈15%.
- Flows [S: NCREIF]: the year to June 2026 brought $10.4bn of contributions against $19.1bn of distributions and redemptions (8.5% of NAV).
- Payout speed (via G14 [S: Townsend/PREA]): funds paid ≈71% of queues a quarter on average after 2007, but ≈5% in 2023. Redemptions averaged < 1.5% of NAV a quarter.

**Non-traded REITs** [S-sec].
- BREIT (limits 2% of NAV a month, 5% a quarter) filled ≈15% of $4.5bn of requests in March 2023 and 100% of $961m in February 2024.
- SREIT cut its limits to 0.33%/1% in 2024, raised them to 0.5%/1.5% in 2025, and filled ≈3% of each request in March 2026.

**Europe** [S-sec]. UK daily-dealing property funds suspended dealing in 2016 and 2020 (more than £12.5bn trapped), and the FCA consulted on 90–180-day notice periods. Nine German open-ended funds liquidated after 2008; new units now carry a 24-month minimum holding and 12-month notice (via G14).

**Fund-interest secondaries.**
- Real estate priced at 68% of NAV in H1-2026; Jefferies wrote that pricing "settled at 68% of NAV in H1 2026 as liquidity conditions remained challenged" [S].
- History: 83 / 76 / 79 / 71 / 71 / 72 / 70% for 2019–2025 [S/C, dossier 05].

### 4.7 Gulf real estate

- **2026** [S: The National, 7 Oct 2026]. Q3 Dubai residential sales were AED72.6bn, −47% by value and −38% by volume year on year. S&P counts transactions 26% lower a month since the war began, and prices 5–15% lower since end-2025 (industry estimates). It expects apartments, given 2027–28 deliveries, and luxury to fall most. Emaar's founder cited a 5–10% adjustment.
- **2008–10** [S-sec]. Reuters polls put Dubai residential prices ≈55–58% below the 2008 peak (Abu Dhabi ≈40%). Carnegie cites ≈50% corrections in the UAE and ≈60% in Kuwait, as oil fell from ≈$144 to $34 (IMF *F&D*).
- **Reading:** Gulf property falls in both oil states. In 2008–10 the oil collapse cut fiscal and credit flows (the DB analogue). In 2026 war risk and missile strikes hit foreign demand even with oil high (the GW analogue).

---

## 5. Practitioner and peer practice, and case studies

**Peer limits.**
- **NBIM:** unlisted real-estate debt ≤ 25% of the portfolio and ≤ 70% per investment (mandate amended 9 Dec 2025) [S, via G14 and dossier 06].
- **ADIA:** its 2025 Review narrowed the real-estate range to 2–7% [S, dossier 02].
- **CalPERS:** LTV < 50% and DSCR > 1.5 (via G14 [S-sec]).
- **Lesson:** peers separate agency-facing recourse leverage from asset-level debt limits written into the real-estate mandate. ADIC's synthetic sleeve, at 47% look-through, is closer to a value-add fund than to NBIM.

**How real-estate teams forecast.**
- *Business plans* project rent, occupancy, capex and a terminal value at an exit cap rate, typically rendered as IRR/MOIC with downside/base/upside cases. ADIC archives these quarterly, net of fees (brief §9).
- *Marks* are appraisals (DCF and direct capitalization), externally reviewed with a lag. Open-end funds appraise quarterly; closed-end GP NAVs follow the same appraisal cycle with a further reporting lag.
- *Documented biases.*
  - Net alpha of non-core strategies is negative (Bollinger & Pagliari; Pagliari 2017).
  - Early projected IRRs are speculative (Arnold, Ling & Naranjo).
  - Vintage timing dominates: US closed-end 2005 vintages averaged −5.58%, 2008–09 vintages 15–17% (ALN) [S].
  - Development exposure predicted pre-GFC losses (Fisher & Hartzell).
  - Appraisals trail sales in both directions (Cannon & Cole).
  - Exit-cap and rent-growth optimism are common practitioner knowledge but were not quantified from a primary source this session [P]. They are estimated from ADIC's archive (§6.7).

**Lessons from the cases in §4.**
- *ODCE 2022–26:* a "quarterly" open-end vehicle behaved as a 2–3-year liquidity asset in stress, and its NAV stayed above listed-implied value for six quarters.
- *BREIT and SREIT:* the payout rule is the asset's liquidity term, so the caps are modelled as a state machine (§6.2).
- *NYC office:* the long-run −39% revaluation (Gupta, Mittal & Van Nieuwerburgh), CBD prices 50% below peak and 12.16% delinquency justify office's structural cap-rate drift (+10bp a year), negative real rent drift and heavy capex.
- *Dubai:* Gulf assets need loadings on oil, fiscal and war states, and sales volumes fall 26–47% before prices do.
- *October 2026:* REITs fell 8.3% from July while ODCE's Q3 appreciation was +0.69%. The stale-NAV gap is reopening, so the nowcast must not wait for appraisals.

---

## 6. Design implications for the ADIC framework

### 6.1 Holdings schema and state

**Static fields per holding** (extending groups §3.0):
- `market_id` (sector × metro), `region`, `vehicle` ∈ {OE, CE, JV, DIR, CO}, ADIC share ω, GCC/oil flag, `is_synthetic`;
- appraisal: date, method, appraiser, appraisal cap rate;
- rent-roll summary: WALT, expiry ladder, escalators, market-to-contract gap; occupancy; opex ratio; capex plan;
- debt tape by tranche: balance; fixed or floating; coupon or spread; hedge type, strike and expiry; maturity and extension options; amortization; DSCR, LTV and debt-yield covenants; recourse and guarantees; lender type;
- JV terms: control, ROFO/ROFR, buy–sell, promote, consents;
- open-end terms: notice, payment rule (pro rata or FIFO), caps, queue position;
- closed-end terms: commitment, unfunded, vintage, term and extensions, fees, transfer consent;
- business plan with cases: IRR/MOIC, exit cap, rent growth, capex, hold.

**Dynamic state** (path × quarter):
- property: M, R^ip, O, E, NOI, c, V^T, V^A, G = ln V^A − ln V^T, ν;
- debt: tranches and coupons, hedge state, DSCR, LTV on V^T, cash-trap flag, extension clock;
- vehicle: open-end Q (others) and ADIC's outstanding request; closed-end U and effective age a^e.

### 6.2 Engine equations (quarterly, Δ = ¼)

Property layer, by sector k and market m:

$$\Delta\ln M_{t+1}=\Delta(\mu_k+\beta^\pi_k\pi_{t+1}+\beta^g_kg_{t+1})+\sigma^M_k\sqrt\Delta\,\varepsilon,\qquad R_{t+1}=R_t(1+e_k\Delta)+\rho_k\big[M_{t+1}-R_t(1+e_k\Delta)\big],\ \rho_k=\min(1,\Delta/\text{WALT}_k)$$

$$O_{t+1}=\text{clip}\big(O_t+0.15(\bar O_k+\beta^O_kg_{t+1}-O_t)+0.005\varepsilon,\,0.4,\,0.99\big),\qquad E_{t+1}=E_t(1+\pi_{t+1}\Delta),\qquad NOI_t=(R_tO_t-E_t)\,(1-h_k(Z_t)\mathbb 1_{GCC})$$

$$c_{t+1}=c_t+\kappa_c(c^*_{t+1}-c_t)+\sigma_c\varepsilon,\qquad c^*_t=c_0+\beta_y(y^{10}_t-y^{10}_0)+\beta_s(s_t-s_0)+\lambda^{liq}(S_t)-\lambda^{liq}(S_0)+\delta_k t+\phi(Z_t)\mathbb 1_{GCC}$$

$$V^T_t=\frac{NOI_t(1+\hat g_t)}{c_t},\quad \hat g_t=\tfrac12(\mu_k+\beta^\pi_k\pi_t),\qquad \text{CAPX}_t=\kappa^{cap}_k\Delta V^T_t,\qquad r^U_{t+1}=\frac{NOI_{t+1}\Delta-\text{CAPX}_{t+1}+V^T_{t+1}-V^T_t}{V^T_t}$$

Observation layer:

$$\ln V^A_t=\alpha_v\ln V^A_{t-1}+(1-\alpha_v)\ln V^T_{t-1}+\eta_t,\qquad \ln V^{MI}_t=\ln V^T_t+\nu_t,\quad \nu_{t+1}=\bar\nu(S)+\rho_\nu(\nu_t-\bar\nu(S))+\sigma_\nu\varepsilon$$

Debt and refinancing. Legacy tranches mature on a hazard; extended loans fall due again four quarters later.

$$\text{Cap}_t=\min\Big(LTV^{max}(S_t)\,V^T_t,\ \frac{NOI_t}{DSCR^{min}_v\,r^{new}_t},\ \frac{NOI_t}{DY^{min}}\Big),\quad r^{new}_t=y^{10}_t+s_v+\Delta s(S_t),\qquad \text{gap}_t=\Big(M_t-\tfrac{M_t}{D_t}\text{Cap}_t\Big)^+$$

A gap is resolved in order:
1. **Extend** with probability p_ext(S), at a 5% paydown and +25bp, with a re-test after four quarters.
2. Otherwise **cure** if $V^T-D+\text{gap}>1.1\,\text{gap}$.
3. Otherwise **hand back** the collateral share (non-recourse). G14's ϖ replaces this rule when ADIC would honour the debt.

Equity cash flow is $CFE_t=NOI_t\Delta-\text{CAPX}_t-I_t$. It is distributed if DSCR ≥ 1.10 and otherwise swept to debt. Floating coupons are $f_t+s$, capped at the hedge strike while the hedge is live.

*Prototype simplifications:* `g10_re_engine.py` omits the debt-yield term and rate caps (floating debt is unhedged), so its refinancing gaps and interest costs are conservative on hedged books.

Open-end queue machine (per fund; calibrated on ODCE 2022–26, §4.3):

$$R_t=NAV_t\big[r_0+b\,(G^{MI}_{t-1})^+\big],\quad G^{MI}=\ln V^A-\ln V^{MI};\qquad W_t=w\,Q_t\mathbb 1\{G^{MI}\le3\%\}$$
$$L_t=NAV_t\big[l_0+d(e^{RE})\tfrac{GAV}{NAV}+c_t\big]-\text{cures}_t-\text{shortfalls}_t,\quad c_t=\begin{cases}c^{lo}&G^{MI}>3\%\ \text{or}\ Q_t>5\%\\c^{hi}&\text{otherwise}\end{cases}$$
$$P_t=\min(Q_t+R_t-W_t,\,L_t),\qquad Q_{t+1}=Q_t+R_t-W_t-P_t$$

ADIC receives $P_t\cdot q^{ADIC}_t/(Q_t+R_t-W_t)$ at NAV^A (pro rata). Retail-REIT variants add hard caps, P_t ≤ min(2%·NAV per month, 5% per quarter), with the option to cut the caps (SREIT: 0.33%/1%). The ladder interface is $\varphi_f(h,S)$, the P5 share of the request paid by horizon h, exactly as for hedge-fund lots (groups §3.5).

Closed-end fund interest (RFT-TA v2 with real-estate parameters):

$$C_t=(1-e^{-\lambda(a)m^C(e^{RE})\Delta})U_t,\qquad D_t=x_tNAV^T_t+0.8(CFE_t-\text{fee}_t)^+,\quad x_t=1-e^{-\delta(a^e_t)m^D(e^{RE})\Delta},\qquad a^e_{t+1}=a^e_t+\kappa(e^{RE})\Delta$$

Cures are funded first from U and then by fund borrowing (which lowers distributions). New investments are bought at V^T at target LTV. Reported NAV uses V^A; secondary bids use reported NAV; economics use V^T.

JV, direct and co-investment: ADIC receives ω·CFE, funds ω·(cures + shortfalls + capex and development draws), and co-investments exit at 12% of NAV a year × m^D(e^RE).

### 6.3 Parameter defaults

**(a) Sectors** (US basis; Europe +25bp and Gulf +150bp on cap rates). All [I], anchored as noted.

| Sector | c (appraisal basis) | WALT (yrs) | Escalator | β_π | Real rent drift μ | β_g | Ō | β_O | Opex share | κ^cap (%V/yr) | σ_M | Market-to-contract gap | Cap-rate drift |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Logistics | 4.1% | 5 | 3% | 0.5 | −1.0% | 1.0 | 94% | 0.5 | 10% | 0.8 | 4% | +10% (NCREIF 15–36% by size [S]) | 0 |
| Residential | 4.3% | 1 | 0 | 0.6 | −1.5% | 0.8 | 94% | 0.5 | 38% | 1.2 | 3.5% | 0 | 0 |
| Office | 6.2% | 6 | 2.5% | 0.3 | −2.0% | 1.5 | 82% | 1.5 | 40% | 2.5 | 6% | −10% | +10bp/yr (GMVN [S]) |
| Retail | 5.4% | 5 | 2% | 0.4 | −0.5% | 1.2 | 93% | 0.8 | 15% | 1.2 | 4% | 0 | 0 |
| Data centres | 4.8% | 8 | 3% | 0.3 | +1.0% | 0.6 | 95% | 0.3 | 20% | 1.5 | 5% | +8% | 0 |
| Hotels | 7.5% | daily | 0 | 0.8 | −0.5% | 2.5 | 70% | 3.0 | 70% | 4.0 | 10% | 0 | 0 |
| Alternatives | 5.3% | 1.5 | 1% | 0.6 | 0 | 1.0 | 88% | 0.8 | 45% | 1.5 | 5% | 0 | 0 |

The weighted appraisal yield (≈4.7%) matches the NPI income return (RCLCO [S]). Same-store NOI growth of 0.5–0.8% a year at CPI 3.3–4.0% matches NCREIF's 0.78% [S].

**(b) Regimes and financing.**

| | Expansion | Late / inflationary | Crisis | Recovery | Source |
|---|---|---|---|---|---|
| LTV_max for refinancing | 65% | 60% | 50% | 60% | [I]; CBRE Q2-26 commercial LTV 59.6% (via G14 [S]) |
| New-loan spread add-on | 0 | +25bp | +150bp | +50bp | [I] |
| P(extension) | 0.35 | 0.50 | 0.50 | 0.40 | Glancy 2026: ≈half extended in 2023–25 [S-sec] |
| Credit-availability premium λ^liq | 0 | 10bp | 75bp | 25bp | [I]; debt-flow channel (Chervachidze et al. [S-sec]) |
| Listed wedge mean ν̄ | 0 | −2% | −12% | +3% | [I]; REIT drawdowns §4.1 |
| Transaction window e^RE | N (O if Baa < 1.6%) | D if y10 > 4.75% or GW | F | N | [I] |

- **Cap-rate loadings:** β_y = 0.45 (range 0.30–0.60), β_s = 0.50 (0.3–0.8), κ_c = 0.15 a quarter (half-life ≈4 quarters), σ_c = 12bp a quarter [I].
- **Consistency check:** with β_y = 0.45, a +280bp move in the 10-year lifts cap rates ≈125bp. That is ≈−22% at flat NOI from 4.5%, in line with ODCE's ≈−24% appreciation in 2022–24 [I-calc].
- **Listed wedge:** ρ_ν = 0.70, σ_ν = 6% a quarter.
- **Spreads s_v over the 10-year:** open-end 160bp, direct 180bp, JV 220bp, closed-end and co-investment 250bp (CBRE commercial 204bp [S via G14]).
- **DSCR_min:** 1.25 for open-end and direct, 1.20 otherwise.

**(c) Vehicles.**

| Vehicle | G₀ (initial V^A/V^T, log) | Smoothing α | Fees | Payout policy | Liquidity terms |
|---|---|---|---|---|---|
| Open-end core (ODCE-like) | 5% | 0.55 | 0.85% of NAV (ODCE gross–net ≈20bp a quarter [S]) | 90% of (NOI − interest − fee); capex debt-funded, so leverage drifts up (22.4% → 27.1% [S]) | Queue: r₀ 0.6%/qtr, b 0.12, w 0.08, l₀ 0.25%, d(e^RE) = 1.0/0.6/0.4/0.2% of GAV (O/N/D/F), c^hi/c^lo 1.2/0.4%; starting queue 8% (US), 5% (Europe) |
| Closed-end value-add / opportunistic | 8% | 0.65 | 1.5% of NAV (carry ignored in stress) | Exits δ(a^e) = 3/12/22/30/35% for a^e < 3/5/7/9/9+ years; m^D = 1.3/1.0/0.45/0.25; income 80% of positive cash flow after debt service | Calls 25/30/35/40% of unfunded by age; m^C = 1.2/1.0/0.75/0.6; κ(e) = 1.2/1.0/0.6/0.5; secondary at (1 − d)·NAV^A with d 32% (H1-26 [S]) |
| JV | 6% | 0.65 | Promote off-model | Free cash flow if DSCR ≥ 1.10 | Partner consent, ROFO/buy–sell; capex draws 20% a year of unfunded; development at 1.25× yield-on-cost premium, +15% cost overrun in crisis |
| Direct | 6% | 0.70 | — | As JV | Sale 3–9 months (median 135 days UK, via G14) |
| Co-investment | 7% | 0.65 | — | As JV, plus exits at 12% a year × m^D | Sponsor's clock |

### 6.4 Scenario loading

Real estate loads on main §4.1's factors and states:
- **Factors:** y10, the Baa spread s, CPI π, the growth gap g and the short rate f.
- **Master regime S:** sets LTV_max, Δs, λ^liq, ν̄ and e^RE.
- **Shock type Z:** sets Gulf NOI hits h_k (GW: hotels −25%, retail −10%, office −6%, others −4%; DB: 1.5× those plus 5%), a Gulf cap-rate add-on φ (GW +75bp, DB +150bp) and +0.8pp CPI in GW.
- **Transaction window e^RE:** couple it to the main exit window e_t (an HSMM with real-estate multipliers) and filter it on RCA volume growth, JLL bid and credit intensity, ODCE flows and CMBS issuance.
- **Initial state (October 2026):** S = late-cycle, Z = GW, e^RE = D; y10 5.10%, short rate 3.90%, CPI 3.7%, Baa spread ≈2.0%; G₀ by vehicle as above; open-end queues 8% (US) and 5% (Europe).

**Named scenarios** (forced regime paths; all other dynamics stochastic):

| Id | Specification |
|---|---|
| base_mc | Markov regimes from the October-2026 state (P(late → crisis) 6% a quarter) |
| higher_for_longer | Late-cycle for 8 quarters; y10 target +40bp (median 5.2–5.3% at q4–q8); spreads +40bp; Gulf war ends after 4 quarters |
| demand_bust | Crisis for 6 quarters, then recovery for 6; Z = DB; Baa ≈3.6–3.7%; y10 falls to a median 4.1% by q8 |
| stagflation_gulf | Late-cycle for 8 quarters; y10 median 5.5–5.8%; CPI ≈5.1–5.6%; spreads +100bp; Gulf war for 8 quarters with 1.6× Gulf NOI hits |
| benign | Expansion from quarter 2; y10 median 4.1% by q8, heading to ≈3.7%; Baa ≈1.4%; Gulf war ends next quarter |
| credit_crunch | GFC-type: crisis for 6 quarters, Baa median 4.9–5.3%, listed wedge −22%, then recovery |

### 6.5 Synthetic results ($9.0bn sleeve; 10,000 paths per scenario; common random numbers) [I-calc]

| Metric | base_mc | higher_for_longer | demand_bust | stagflation_gulf | benign | credit_crunch |
|---|---|---|---|---|---|---|
| Year-1 net cash, $bn: P5 / P50 / P95 | −0.18 / −0.10 / +0.07 | −0.17 / −0.12 / −0.08 | −0.24 / −0.21 / −0.17 | −0.19 / −0.15 / −0.11 | +0.05 / +0.12 / +0.19 | −0.25 / −0.21 / −0.18 |
| Year-2 net cash P50, $bn | +0.03 | −0.06 | −0.27 | −0.15 | +0.47 | −0.32 |
| Year-1 inflows (income + distributions) / outflows (calls + cures + draws), P50 | 0.39 / 0.49 | 0.37 / 0.49 | 0.30 / 0.51 | 0.35 / 0.51 | 0.65 / 0.53 | 0.30 / 0.51 |
| Same-store NOI growth, 2-year annualized, P50 | 0.5% | 0.7% | −2.5% | −0.9% | 1.6% | −2.5% |
| Max 3-year drawdown, true NAV: P50 (P5) | −2.9% (−22.1%) | −4.3% (−15.1%) | −28.0% (−34.4%) | −13.1% (−23.7%) | −1.0% (−4.1%) | −38.4% (−44.0%) |
| Max 3-year drawdown, reported NAV, P50 | −10.5% | −12.6% | −32.4% | −21.1% | −7.5% | −41.9% |
| P(true drawdown > 15% within 3 years) | 13% | 5% | 100% | 37% | 0% | 100% |
| Trough lag, reported vs true (quarters) | 3 | 3 | 3 | 3 | — | 5 |
| Debt maturing within 24 months / refinancing gap, $bn (gap share) | 3.37 / 0.22 (6.6%) | 3.42 / 0.27 (7.7%) | 3.54 / 0.72 (20.3%) | 3.45 / 0.35 (10.2%) | 3.03 / 0.06 (2.0%) | 3.55 / 0.81 (22.8%) |
| Debt handed back over 5 years, % of initial debt: P50 / P95 | 0.0 / 2.4 | 0.0 / 2.3 | 1.3 / 3.1 | 0.4 / 2.7 | 0.0 / 1.7 | 1.9 / 4.7 |
| Peak LTV on true values, 3 years: P50 / P95 | 51% / 56% | 51% / 54% | 58% / 61% | 53% / 56% | 51% / 52% | 62% / 64% |
| Open-end queue peak, % NAV: P50 / P95 | 8.0 / 21.4 | 8.0 / 20.0 | 15.0 / 24.8 | 8.5 / 20.9 | 6.7 / 8.9 | 26.1 / 39.4 |
| Full ADIC open-end redemption, share paid by q4 / q8 / q12, P50 (P5) | 34 / 62 / 83% (25 / 43 / 57%) | 34 / 60 / 79% (28 / 46 / 60%) | 26 / 41 / 60% (22 / 34 / 48%) | 33 / 58 / 76% (27 / 45 / 58%) | 45 / 90 / 100% (36 / 69 / 90%) | 23 / 35 / 48% (20 / 30 / 41%) |
| 3-year annualized total return, true / reported basis, P50 | 3.6 / −1.6% | 0.6 / −4.1% | −6.5 / −12.7% | −3.0 / −8.1% | 13.4 / 6.3% | −13.6 / −18.3% |

*SYNTHETIC – NOT ADIC DATA.* Look-through: $8.0bn of debt on $17.0bn of GAV (ADIC share), LTV 47.1%. Sub-books: open-end 2.7, closed-end 2.6 (unfunded 1.2), JV and direct global 1.7 (0.2), Gulf 1.2 (0.2), co-investment 0.8. Reported returns start from marks ≈10% (equity level) above true value, so markdowns are realized over the period.

**Reading.**
1. The sleeve is a modest cash *user* in every state except benign. It cannot offset the PE drought.
2. Measured from today's stale marks, reported drawdowns exceed true ones, because marks must first fall to true value. After that, reported NAV trails the true path by about three quarters, so reported volatility understates risk at turning points.
3. The 24-month refinancing gap ($0.7–0.8bn in stress) is the main asset-level funding need. In the engine about half is extended. The rest is cured from fund unfunded (inside calls), from open-end fund liquidity (slowing the queue) or from ADIC cash for JV and direct assets (≈$0.05bn in year 1), or handed back.
4. Open-end units are not a near-term liquidity source: even from today's state, a full redemption returns about a third of the holding within a year.

**Against G15** (real-estate lines of `g15_ra_results.json`, 12 months).
- G15 shows +$0.31bn (normal), −$0.07bn (drought), −$0.51bn (S1) and −$0.60bn (T4′), against G10's +0.12 (benign), −0.10 (base), −0.21 (demand bust) and −0.21 (credit crunch).
- The stress gap is the canonical T4′ convention (calls ×1.38, distributions at 10.8% of drought rates), against G10's structural slowdown of deployment in frozen markets (m^C = 0.6) offset by cures.
- Tier 1 should keep T4′ (conservative). P and H should use the structural engine, with the call multiplier as an explicit misspecification axis.

### 6.6 SELL / HOLD / REFINANCE / LEVER for real estate

All actions are scored by main §4.4's kernel on V\* (the nowcast true value, §6.7), never on V^A. G14 holds the instrument formulas, the merit order in κ per $ of month-24 headroom, transfer taxes and lock-in value Λ. The table gives the real-estate engine outputs each action needs; "B4" to "B6" refer to the arithmetic blocks in `g10_public_and_arith.py` (results in `partB`).

| Level | SELL | HOLD | REFINANCE (cash-out) | LEVER (exposure up) |
|---|---|---|---|---|
| Direct asset | $p=V^T(1-d^{liq}(e^{RE}))-\text{tax}_{seller}-tc-\Lambda$; 3–9 months; failure 30–50% in stress (G14) | Continuation: forward CFE + V^T path; fund capex and cures | At maturity: $\text{Cap}_t-D-\text{fees}$; early cash-out surrenders Λ (marginal rate ≈14% for 40→55% LTV, G14). Ground lease ≈35% of value at a 7.4% economic yield (G14) | Passes only if $c-\kappa^{cap}+\hat g>r_D$ + charges and P(DSCR < 1.1 in 12m) ≤ 5%. Fails for core in October 2026: cap 5.6–6.4% vs debt ≈6.8–7.1% gives levered cash yields of 3.8–5.8% at 60% LTV (B4) |
| JV stake | Partner ROFO/buy–sell; minority or control discount; partial sell-down = **partial SELL** (exposure falls), whatever its label | As direct, pro rata ω | Asset-level debt by consent; recap through the partner | Development debt ≤ pre-leased share |
| Closed-end fund interest | $(1-d)\,NAV^A$ with d 32% (H1-26); buyer assumes unfunded; GP consent; 3–6 months. At 68%, SELL beats HOLD only if θ ≤ ≈0.85, μ ≈ 4% and ℓ ≥ ≈5% (hold value 69.4%); at θ = 1 and μ = 8% HOLD is worth 89–100% (B5) | Fund calls and cures from U | LP-level NAV facility: dominated (low LTV, pledge consent; groups §2.3) | Re-up only with posterior skill (groups §3.1) |
| Open-end units | Redemption = queued SELL at NAV^A on payment date; φ(h,S) from the §6.2 queue machine. At a 10% stale gap, redeeming captures 92.5–94.7% vs 90.5% HOLD (B6). Unit secondaries −8% to +3% normally, −15% to −25% in UK stress (G14) | Income ≈3% of NAV | None at LP level | Subscriptions face entry queues in booms |

**Decision rules** (main §4.4, with real-estate inputs):
- SELL iff $p^{ce}>p^*$, using E[LAPV(HOLD + best REFI)] computed on V\* and the engine's cure distribution.
- REFI iff $\hat s+f/T+\lambda_{Lev}+\text{covenant charge}+h/T<\bar\ell$, at maturity only unless Λ ≈ 0.
- LEVER iff ADD and REFI both pass.
- For open-end units, the redemption is lodged when $\hat\alpha^{net}+\kappa^{reentry}<\bar\ell(T^{cash})$, with $T^{cash}$ taken from φ(h,S). Requests are revocable in most ODCE documents, which is worth confirming per fund (§9).

### 6.7 Marks, forecasts and the FBE translation

**Four marks.**
1. *Underwritten:* yield-on-cost, IRR/MOIC, exit cap.
2. *Current:* V^A with its date and method.
3. *Forecast:* the business-plan IRR/MOIC with cases, read as P10/P50/P90 (brief §9).
4. *Market-implied:* the stale gap Ĝ, estimated from:
   - sector-matched, relevered REIT returns since the appraisal date (V^MI);
   - transaction indices (RCA CPPI, Green Street) by sector and metro;
   - secondary bids for fund interests (68% of NAV);
   - ADIC's own sale-to-mark ratios (NPI sales cleared within ±4% in Q2-26).

**Nowcast.** $V^*_t=V^A_t\,e^{-\hat G_t}$, where Ĝ_t comes from a Kalman filter on §6.2's appraisal equation, with V^MI and transaction indices as observations. α is estimated per manager from the archive (prior 0.55–0.70; the 2022–24 ODCE fit gives 0.5–0.6). This is the real-estate instance of main §4.3's $V^*_t=N_{t-s}\exp(\tilde\beta\Delta m-\psi)$. G13 owns the cross-sector fusion.

**Translating a business plan** onto the forward basis (forward log return on V\*, net):
1. Correct the components before computing the return [I]:
   - NOI growth: $g^{corr}=g^{plan}-\tfrac12(g^{plan}-g^{cons})$;
   - exit cap: $c^{corr}_{exit}=\max(c^{plan}_{exit},\,c_0+10\text{bp}\times H,\,\hat c^{fwd})$, where $\hat c^{fwd}$ is the market-implied forward cap rate from REIT pricing;
   - capex: $\kappa^{corr}=\max(\kappa^{plan},\kappa^{cap}_{sector})$;
   - hold: $H^{corr}=H^{plan}+\{0,2,4,6\}$ quarters in e^RE ∈ {O, N, D, F};
   - debt per tape, at forward rates.
2. Compute the return: $\rho_f=H^{-1}\ln(R^{corr}_f/V^*_t)$.
3. Apply the residual bias $b^f$ and precision $1/(\kappa^2\hat\sigma^2)$ (groups §5).

**Bias priors** [I], anchored on net alpha of −2.85 to −3.26pp a year (Bollinger & Pagliari) and on ALN's realized IRRs:

| Strategy | b^u (pp a year) | b^f (pp a year) | κ (coverage of a stated 80% interval) | Structural checks |
|---|---|---|---|---|
| Core open-end | +0.5 | +0.5 | 1.5 (61%) | Appraisal lag; leverage drift |
| JV and direct, stabilized | +1.5 | +1.0 | 1.75 (54%) | Exit cap; capex; Gulf flag |
| Value-add | +3.0 | +2.0 | 2.0 (48%) | Lease-up timing; rent growth > P75 of consensus |
| Opportunistic and development | +4.0 | +2.5 | 2.2 (44%) | Development share; construction costs; exit cap below entry |

**Scoring.** WIS on archived cases; Mincer–Zarnowitz regressions of realized on planned exit cap, rent growth and hold; timing-centroid shift. The misspecification ensemble (groups §6) adds M1 regime-dependent optimism, which binds hardest for real estate in e^RE = D.

### 6.8 Constraints and objective terms (proposals for IC ratification) [I]

1. **RE-LT1, look-through LTV.** Real-estate look-through LTV ≤ 50% (soft) and 55% (hard), on V\*. The synthetic book is at 47% on appraisal and peaks at 51% (base, P50) or 62% (credit crunch). Single asset ≤ 70% at acquisition or refinancing (NBIM).
2. **RE-MAT, maturity concentration.** ≤ 25% of real-estate debt maturing in any rolling 12 months and ≤ 40% in 24 months. The synthetic book has ≈42% in 24 months ($3.4bn of $8.0bn), so it breaches: stagger maturities and extend early only when Λ ≈ 0.
3. **RE-FLT, floating exposure.** Unhedged floating ≤ 25% of real-estate debt; hedge expiry ≥ loan maturity (the CRE-CLO cap lesson, G14).
4. **RE-CURE, cures.** The 12-month cure need is a chance constraint, P(cures + shortfalls > budget) ≤ 5%, under the restored problem. It enters L4 as a group budget and CLC = c_buf·Σω_h O^stress_h.
5. **RE-OE, open-end units.** ADIC ≤ 10% of any open-end fund. Units are credited at P5 φ(h,S), never at NAV.
6. **RE-GCC, Gulf exposure.** Gulf real estate carries a wrong-way charge in the kernel, jointly with G12's energy book. It is sized so that the Gulf share of Real Assets NAV in DB and GW states respects the Tier-1 floor.
7. **RE-DEV, development.** Development ≤ 10% of real-estate NAV, with pre-leasing ≥ 50% before debt is drawn.

**Objective terms.**
- Value is measured on V\*.
- λ_Lev × look-through debt is charged as its own row, not added to T5's recourse limit (G14 §6.3).
- CVaR is computed on desmoothed returns.
- κ^irr carries transfer taxes and Λ.
- The listed wedge ν is risk, never alpha.

### 6.9 Links to other groups and Corporate Finance

- **Other investment groups.**
  - *Private Credit:* real-estate loans on the same property markets share one property-market draw per path (extends V24).
  - *Capital Solutions:* preferred and rescue equity, and reserve-price quotes only (groups §4.2).
  - *Secondaries:* buyer of real-estate LP interests at 68%, behind the §4.5 gate.
  - Every intra-ADIC transfer raises zero liquidity.
- **Overlay and Public Markets.** The Overlay holds caps and swaptions (Δ-adjusted, G14) and any listed-REIT hedges of real-estate beta, judged on true-value P&L because of basis and the ν wedge. Public Markets' REIT data feed the fourth mark.
- **Corporate Finance.**
  - Cures, shortfalls, capex and development draws are contingent outflows in L4.
  - Real-estate maturities are planned alongside CF's revolver.
  - FTP is charged on each holding's cash-weighted life (≈ the queue horizon for open-end units).

### 6.10 Calibration targets and validation gates

**Targets** (all sourced in §4): long-run returns (NPI 40-year 7.2%; ODCE 6.6%, minimum rolling 3-year −11.0%); income yields 4.1–4.7%; same-store NOI growth 0.78%; ODCE leverage 27.1%; the 2022–24 drawdowns and three-quarter lag; queues (19.3% peak, ≈10% in Q1-26, payouts < 1.5% of NAV a quarter); LP pricing 68%; levered KS-PME 1.01; non-core alpha −285 to −326bp; Dubai −55% to −58% (2008–10) and −5% to −15% (2026).

**New gates** (pre-registered alongside groups V1–V24):

| Gate | Check |
|---|---|
| V-RE1 | Same-store NOI growth within ±1pp of NCREIF's trailing four quarters at the start state |
| V-RE2 | ODCE replay: queue at 1Q24 within 17–22% and at 1Q26 within 8–12% |
| V-RE3 | Desmoothed 2022–24 drawdown within ±5pp of relevered REITs |
| V-RE4 | Accounting identity GAV = D + E per holding; cash conservation across vehicle layers |
| V-RE5 | One property-market draw per path, shared by Real Assets equity and Private Credit real-estate loans |
| V-RE6 | Reported NAV never used in the kernel; every card shows V^A, V\* and Ĝ |
| V-RE7 | Open-end units credited only through φ(h,S) |
| V-RE8 | Secondary prices within ±3pp of the latest Jefferies print by strategy |

### 6.11 SPECIFICATION CARD: real estate within Real Assets

| Item | Specification |
|---|---|
| **Holdings and data fields** | Per holding: market_id, region, vehicle {OE, CE, JV, DIR, CO}, ω, GCC flag, appraisal (date, method, cap), rent-roll summary (WALT, expiries, escalators, market-to-contract gap), occupancy, opex, capex plan; debt tranches (balance, fixed/floating, coupon/spread, hedge strike and expiry, maturity, extension options, DSCR/LTV/DY covenants, recourse); JV rights; open-end terms (notice, pro rata/FIFO, caps, queue position); closed-end terms (commitment, unfunded, vintage, term, fees, consent); business plan with cases; `is_synthetic` |
| **NAV equations** | $V^T=NOI(1+\hat g)/c$; c partial-adjusts to $c^*=c_0+0.45\Delta y_{10}+0.50\Delta s+\lambda^{liq}(S)+\delta_kt+\phi(Z)$; $\ln V^A_t=\alpha\ln V^A_{t-1}+(1-\alpha)\ln V^T_{t-1}+\eta$; NAV^A = ωΣ(V^A − D); economic NAV = ωΣ(V^T − D); nowcast $V^*=V^Ae^{-\hat G}$ |
| **Return equations** | $r^U=y-\kappa^{cap}+g^{NOI}-\Delta c/c$ (+ interaction); $r^E=r^U+\tfrac{D}{E}(r^U-r_D)$; net of fees by vehicle |
| **Cash-flow equations** | Property CFE = NOIΔ − CAPX − I, trapped if DSCR < 1.10. Open-end distributions = 0.9(NOI − I − fee). Closed-end: TA calls on U and distributions x·NAV^T + 0.8(CFE − fee)^+ on the effective-age clock. JV/direct: ω·CFE less ω·(cures + shortfalls + draws). Co-investment exits 12% a year × m^D |
| **Leverage and refinancing** | Cap = min(LTV_max(S)·V^T, NOI/(DSCR·r^new), NOI/DY); gap → extend (p_ext(S), 5% paydown) → cure (if V^T − D + gap > 1.1·gap) → hand-back (ϖ from G14 overrides) |
| **Liquidity terms and stress** | Open-end queue machine, §6.2 (r₀ 0.6%, b 0.12, w 0.08, payout ≈1.2–1.5% of NAV a quarter), output φ(h,S). Retail REITs: 2%/5% caps, cuttable. Fund interests: 68% of NAV, 3–6 months. Assets: 3–9 months, taxes per G14. Stress: crisis LTV_max 50%, +150bp spreads, +75bp λ^liq, e^RE = F, ν̄ −12% |
| **Parameter defaults and sources** | §6.3(a)–(c). Anchors: NCREIF (NOI growth, cap rates, leverage, returns), RCA (sector cap rates and CPPI), Nareit (drawdowns), Callan/Accordant/Townsend (queues), Jefferies (68%), MBA/Trepp (maturities, delinquency), Glancy (extensions), Bollinger–Pagliari/ALN/MSCI (alpha) |
| **SELL** | Asset at V^T(1 − d^liq) − seller taxes − tc − Λ; JV stake via ROFO/buy–sell (a sell-down is a partial SELL); fund interest at 68% (d by age and θ); open-end unit = queued SELL at NAV^A on payment date |
| **HOLD** | Fund calls, capex, cures; continuation on V\* paths; keep cheap legacy debt (Λ) |
| **REFINANCE** | Cash-out only at maturity, or where Λ ≈ 0; ground lease ≈35% of value at ≈7.4%; NAV facility on fund interests dominated; rule ŝ + f/T + λ_Lev + covenant + h/T < ℓ̄ |
| **LEVER** | Acquisition or development debt iff c − κ^cap + ĝ > r_D + charges and the DSCR chance constraint holds; currently fails for most core (negative leverage) |
| **Forecasts and biases** | Business-plan IRR/MOIC with cases → corrected components (exit cap, rent growth, capex, hold) → forward return on V\*; b^u/b^f priors +0.5/+0.5 (core) to +4.0/+2.5 (opportunistic); κ 1.5–2.2; estimated from the quarterly archive |
| **Synthetic defaults** | Real estate $9.0bn NAV / $1.6bn unfunded (G15 sub-books); 31 positions (6 open-end, 14 closed-end, 5 JV, 3 direct, 3 co-investment); US 60%, Europe 21%, Asia 6%, Gulf 13%; logistics 26%, residential 27%, office 21%, retail 8%, data centres 4%, hotels 6%, alternatives 8%; look-through LTV 47%; start state as §6.4 |
| **Links** | Private Credit (shared property draws), Capital Solutions (preferred and rescue quotes), Secondaries (68% buyer), Overlay (caps, REIT hedges), Public Markets (V^MI feed), CF (cures and draws in L4, maturity ladder, FTP), G12 (oil wrong-way), G13 (mark fusion), G14 (instrument library), G15 (book and cash map) |

*Parameters are [I] unless sourced in §4; SYNTHETIC defaults are not ADIC data.*

---

## 7. Implementation notes

**Code structure.**
- `g10_re_engine.py` is a single-file prototype, vectorized in numpy over paths: one 10,000-path × 20-quarter scenario runs in about a second. Production should split it into four modules:
  1. `re_property` (§6.2 property and observation layers, keyed by market_id);
  2. `re_debt` (tranche ledger, hedges, refinancing resolver);
  3. `re_vehicle` (open-end queue machine, closed-end TA, JV/direct/co-investment wrappers);
  4. `re_observe` (appraisal, listed wedge, secondary bids, nowcast Kalman filter).
- **Seeding.** Draw each property market once per path from a SeedSequence child keyed by market_id, so Real Assets equity, Private Credit real-estate loans and Capital Solutions preferreds see the same shocks (gate V-RE5).
- **Accounting.** Hold debt as tranche arrays (balance, coupon, maturity, hedge strike and expiry, extension flag) with a ledger. Check GAV = D + E and cash conservation every quarter (V-RE4).

**Numerical pitfalls.**
1. *Appraisal in logs.* Smooth in log levels and floor V^T. Keep G explicit; never difference V^A to get returns and then desmooth them back.
2. *Desmoothing amplifies noise.* At α = 0.8 the 2022–24 ODCE drawdown becomes −50%. Use a robust filter (Delfim & Hoesli 2021) and estimate α jointly with the lag. Short series also bias means downward.
3. *DSCR and LTV ratios.* Guard divisions by NOI and interest near zero, and floor NOI at 10% of starting NOI. Recompute capacity on V^T, never V^A (lenders appraise, but in stress they lend on transaction evidence).
4. *Hand-back.* A pure option rule (cure iff equity after cure > 1.1·gap) is ruthless. G14's ϖ must be a policy input, because ϖ = 1 turns every gap into a capital call.
5. *Queue accounting.* Compute payouts pro rata, *after* new requests and withdrawals. A standing queue Q₀ competes with any new request from the first quarter, which is why ADIC's base-case fill is 34% within a year. The replay drives requests with last quarter's gap. The prototype uses the current quarter's gap on already-lagged appraisals; production should use the lagged form.
6. *Closed-end consistency.* Buy and sell at V^T and carry NAV^A separately. Exits remove the same share of every tranche, and cures draw on U before fund borrowing.
7. *Same-store versus book NOI.* Report NOI growth from the property index. Calls and exits contaminate the vehicle total: an early prototype showed 3.5% "NOI growth" that was mostly acquisitions.
8. *Common random numbers* across scenarios and actions keep paired differences (SELL vs HOLD) precise. *Business-plan IRRs* use the groups' `perf_module` conventions, and cases are quantiles, never scenarios to average.

**Integration.**
- Feed the main scenario engine's y10, Baa, CPI, growth, short-rate, S, Z and e paths instead of the prototype's reduced generator.
- Export to the ladder: φ(h,S) for open-end units; calls, cures, shortfalls and draws by horizon for L4; look-through debt for the leverage row.
- Export to H: SELL, REFI and LEVER columns with V\*-based cash flows.

---

## 8. Risks and limitations

1. **Synthetic and stylized.** The sector parameters, regime financing terms, G₀ and the Gulf shocks are [I]. Only a few anchors are directly sourced: same-store NOI growth, the yield level, the 2022–24 drawdowns and lag, queue peaks, payouts and the secondary price.
2. **Data provenance.** ODCE quarterly returns 2022Q1–2026Q2 are read from NCREIF's printed webinar slide. Several figures are [S-sec] because the search budget ran out: the Green Street June-2026 sector figures, the MBA wall (read by G14), Trepp's September figures, BREIT/SREIT fills, Dubai 2008–10 and the 2026 macro prints (yields, Brent, Fed). They should be re-verified at the primaries before IC use.
3. **Unverified seed.** The findings of Riddiough, Moriarty & Yeatman (2005) were not retrieved [U]; only the citation is verified.
4. **Queue calibration is aggregate.** It fits ODCE as a whole; fund-level queues range from 6% to 56% of NAV. ADIC's exposure depends on *which* funds it holds and on their payment rules (pro rata vs FIFO, revocability).
5. **The listed wedge is not observed directly.** ν is calibrated to REIT behaviour, and REIT sector mixes (towers, data centres, healthcare) differ from private books. Sector-matched REIT baskets and transaction indices reduce but do not remove the basis.
6. **Two cap-rate worlds.** Appraisal-basis levels (≈4.4–4.7%) and transaction cap rates (5.6–8.3%) are not reconciled at asset level. Lender sizing on in-place NOI may be harsher than the engine's DSCR test.
7. **Gulf and Asia are thin.** No repeat-sales index was fetched for Dubai or Abu Dhabi; the shocks are inferred from transaction values and industry price estimates. Asia-Pacific has no calibration beyond sector analogues.
8. **Omitted mechanisms.** Tenant-level credit, lease-by-lease rollover, development completion risk beyond a cost-overrun factor, promote waterfalls, taxes beyond G14's table, FX (non-USD assets are treated as USD-hedged) and climate and insurance cost shocks (part of the opex path) are not modelled.
9. **Stress conventions differ from G15.** G10's structural engine slows calls in frozen markets; G15's T4′ scales them up. Tier 1 keeps T4′ until ADIC data resolve the direction.

---

## 9. Open questions (what ADIC must supply or confirm)

1. **Size and split.** Is real estate ≈$9bn of the $18bn Real Assets book (G15)? What is the split across open-end funds, closed-end funds, JVs, direct and co-investments, and what share is in the Gulf?
2. **Debt tapes for JV and direct assets:** maturities, fixed/floating, hedge strikes and expiries, covenants, recourse and guarantees. Who funds cures: the group budget or CF? What is ADIC's walk-away policy (ϖ)?
3. **Open-end holdings:** the fund list, ADIC's share of each fund, notice and payment rules (pro rata or FIFO, revocable or not), current queue positions, and any side letters.
4. **Appraisal policy:** frequency, external or internal, quarter-end seasonality, and whether ADIC adjusts GP NAVs (θ) before reporting.
5. **Forecast archive fields:** do the quarterly business plans store exit cap, rent growth, capex and hold, or only IRR/MOIC with cases? Component fields enable the structural corrections in §6.7.
6. **Mandate limits:** does ADIC have real-estate leverage, maturity or development limits today? If so, they replace RE-LT1 to RE-DEV.
7. **Gulf exposures:** sovereign-related tenants, developers or co-investors, and whether domestic real estate is in scope for this group or held elsewhere in the sovereign system.
8. **Overlap:** does Private Credit lend against assets the Real Assets group owns? This determines the shared-draw graph (V-RE5) and intra-ADIC netting.

---

## 10. References

Primary data and market sources (read in-session unless tagged):

1. NCREIF (30 Jul 2026). *Core Real Estate Fund Performance Improves in 2Q2026* (NFI-ODCE press release). https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf
2. NCREIF. *Index Returns* (NPI 2Q2026; NFI-ODCE 3Q2026 preliminary). https://ncreif.org/indices/index-returns/
3. NCREIF (Aug 2026). *Second Quarter 2026 Data and Indices Results Webinar* (slides). https://ncreif.org/__static/jdj5jdewjfhaei55n3y0ehq3dxyyqvpj/NCREIF-Indices-Review-Webinar-Slides-2Q-2026.pdf
4. NCREIF (16 Sep 2026). *NFI-ODCE 2026 Q2 Results: Performance Attribution Webinar* (slides). https://ncreif.org/__static/jdj5jdewjc9ybldynw1nwu1tm3u2qnkw/NFI-ODCE-2026q2-Performance-Attribution-Webinar-Slides.pdf
5. RCLCO (2026). *2026 Q2 ODCE and NCREIF Property Index (NPI) Results*. https://www.rclco.com/publication/2026-q2-odce-and-ncreif-property-index-npi-results/
6. Reid, B., Patkar, R., Limaye, K., & R, A. (12 Aug 2026). *How Strategy Shaped Returns in Private Real Estate*. MSCI. https://www.msci.com/research-and-insights/blog-post/how-strategy-shaped-returns-in-private-real-estate
7. Wrighton, J. (2026). *MSCI Private Capital Benchmarks Summary, Q2 2026*. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
8. MSCI (Jan 2026). *Real Assets in Focus: Trends to Watch for 2026*. https://www.msci.com/downloads/web/msci-com/research-and-insights/blog-post/real-assets-in-focus-trends-to-watch-for-2026/Real-Assets-in-Focus-Trends-to-Watch-for-2026.pdf
9. MSCI (2026). *Private Capital in Focus: Trends to Watch for 2026*. https://www.msci.com/research-and-insights/blog-post/private-capital-in-focus-trends-to-watch-for-2026
10. MSCI (25 Jun 2026). *RCA CPPI US, May 2026*. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/rca-commercial-property-price-indexes-rca-cppi/2606-rcacppi-us-msci.pdf
11. MSCI (Mar 2026). *US RCA Capital Trends, Big Picture (Lender edition), February 2026*. https://www.msci.com/downloads/web/msci-com/data-and-analytics/real-estate/us-rca-capital-trends-report/2603-usct-bigpic-rca-msci-pg1.pdf
12. Robson, W., & Harmse, N. (3 Aug 2022). *Did Closed-End Real Estate Funds Add Value?* MSCI. https://www.msci.com/research-and-insights/blog-post/did-closed-end-real-estate-funds-add-value
13. Green Street (6 Oct 2026). *Waiting For Price Clarity* (US CPPI, September 2026). https://eu.greenstreet.com/waiting-for-price-clarity/
14. Green Street (8 Oct 2026). *It's Happening* (European CPPI, Q3 2026). https://www.greenstreet.com/its-happening/
15. CRE Daily (2026). *Green Street Index Reveals Sector-Based CRE Pricing Gains* [S-sec]. https://www.credaily.com/briefs/green-street-index-reveals-sector-based-cre-pricing-gains/
16. Nareit. *FTSE Nareit U.S. Real Estate Index Series: Monthly Index Values & Returns* (data through September 2026). https://www.reit.com/data-research/reit-indexes/monthly-index-values-returns
17. Callan (2025). *4Q24 Real Estate Performance: Highlights and Key Issues*. https://www.callan.com/blog/4q24-real-estate/
18. Accordant Investments (2026). *Private Real Estate Enters a New Cycle: Q1 2026 NFI-ODCE Index Insights*. https://www.accordantinvestments.com/knowledge-center/private-real-estate-enters-a-new-cycle-q1-2026-nfi-odce-index-insights
19. Jefferies (Jul 2026). *Global Secondary Market Review*. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
20. Board of Governors of the Federal Reserve System (Aug 2026). *July 2026 Senior Loan Officer Opinion Survey on Bank Lending Practices*. https://www.federalreserve.gov/data/sloos/sloos-202607.htm
21. Mortgage Bankers Association (9 Feb 2026). *17 Percent of Commercial and Multifamily Mortgage Balances to Mature in 2026* [S-sec here; read by G14]. https://www.mba.org/news-and-research/newsroom/news/2026/02/09/17-percent-of-commercial-and-multifamily-mortgage-balances-to-mature-in-2026
22. Yieldpro (Oct 2026). *Multifamily CMBS Delinquency Rate Leads Overall Rate Higher in September* (Trepp data) [S-sec]. https://yieldpro.com/2026/10/multifamily-cmbs-delinquency-rate-leads-overall-rate-higher-in-september
23. Crosignani, M., & Prazad, S. (2024, rev. Jun 2026). *Extend-and-Pretend in the U.S. CRE Market*. Federal Reserve Bank of New York Staff Reports 1130. https://doi.org/10.59576/sr.1130 ; https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1130.pdf
24. Glancy, D. (2026). *Pretend or Amend? On Evergreening in CRE*. FEDS working paper, as summarized by Propmodo [S-sec]. https://propmodo.com/why-the-extend-and-pretend-story-was-wrong/
25. The National (7 Oct 2026). *Dubai home sale transactions fall in third quarter amid regional uncertainty*. https://www.thenationalnews.com/business/property/2026/10/07/dubai-home-sale-transactions-fall-in-third-quarter-due-to-regional-uncertainty/
26. Arabian Post (2026). *Dubai property sales slump as war pressures prices* (S&P Global Ratings Credit FAQ) [S-sec]. https://thearabianpost.com/dubai-property-sales-slump-as-war-pressures-prices/
27. TradeArabia (8 Jul 2010). *UAE house prices set to plunge in 2010* (Reuters poll) [S-sec]. https://www.tradearabia.com/news/CONS_182702.html
28. Carnegie Endowment (Mar 2010). *GCC Crisis Highlights Policy Challenges* [S-sec]. https://carnegieendowment.org/research/2010/03/gcc-crisis-highlights-policy-challenges?lang=en
29. Khamis, M. (2010). The GCC and the global crisis. *Finance & Development*, IMF [S-sec]. https://www.imf.org/external/pubs/ft/fandd/2010/03/pdf/khamis.pdf
30. NBIM. *Investment mandate – Government Pension Fund Global* (amended 9 Dec 2025) [S via G14 and dossier 06]. https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/
31. ADIA (2026). *ADIA Review 2025* [S via dossier 02]. https://www.adia.ae/en/pr/2025a/index.html
32. Macro prints, October 2026 [S-sec]: Fed decision of 16 Sep 2026, https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html ; 10-year yield (H.15/FRED DGS10), https://fred.stlouisfed.org/series/dgs10 ; Brent at $110, https://www.businesstoday.in/markets/story/brent-hits-110-as-hormuz-ship-attacks-houthi-strikes-on-saudi-trigger-oil-rally-562207-2026-10-17 ; Hormuz status, https://straits.live/
33. FCA (2020). *FCA consults on new rules to improve open-ended property fund structures* [S-sec]. https://www.fca.org.uk/news/press-releases/fca-consults-new-rules-improve-open-ended-property-fund-structures
34. BREIT and SREIT redemption fills [S-sec]: Commercial Observer (Mar 2024), https://commercialobserver.com/2024/03/blackstone-breit-fulfills-100-percent-redemption-requests-first-time-since-late-2022 ; The DI Wire, https://thediwire.com/sreit-lowers-capacity-on-share-repurchase-plan-says-stanger

Academic sources:

35. Andonov, A., Eichholtz, P., & Kok, N. (2015). Intermediated investment management in private markets: Evidence from pension fund investments in real estate. *Journal of Financial Markets* 22, 73–103. https://doi.org/10.1016/j.finmar.2014.11.002
36. Arnold, T. R., Ling, D. C., & Naranjo, A. (Jun 2021). *Private Equity Real Estate Fund Performance: A Comparison to REITs and Open-end Core Funds* (Nareit-hosted paper). https://www.reit.com/sites/default/files/2021-07/PERE_Fund_Performance_Arnold_Ling_Naranjo_Final_Version.pdf
37. Bollinger, M. A., & Pagliari, J. L. (2019). Another look at private real estate returns by strategy. *Journal of Portfolio Management* 45(7), 95–112. https://doi.org/10.3905/jpm.2019.1.098 (findings via CFA Institute *Enterprising Investor*, 2019: https://rpc.cfainstitute.org/blogs/enterprising-investor/2019/private-real-estate-fund-categories-a-risk-return-assessment)
38. Cannon, S. E., & Cole, R. A. (2011). How accurate are commercial-real-estate appraisals? Evidence from 25 years of NCREIF sales data. *Journal of Portfolio Management* (MPRA Paper 32589). https://mpra.ub.uni-muenchen.de/32589
39. Cao, W., & van Beek, M. (2025). A latent factor cash flow model for alternative investment funds. *Financial Analysts Journal* 81(3), 60–75. https://doi.org/10.1080/0015198X.2025.2489923
40. Chervachidze, S., Costello, J., & Wheaton, W. (2009). The secular and cyclic determinants of capitalization rates: The role of property fundamentals, macroeconomic factors, and "structural changes". *Journal of Portfolio Management* 35(5), 50–69 [S-sec]. https://doi.org/10.3905/JPM.2009.35.5.050 ; https://dspace.mit.edu/handle/1721.1/64724
41. Delfim, J.-C., & Hoesli, M. (2021). Robust desmoothed real estate returns. *Real Estate Economics* 49(1), 75–105 [S-sec]. https://doi.org/10.1111/1540-6229.12313
42. Fisher, J. D., Geltner, D. M., & Pollakowski, H. O. (2007). A quarterly transactions-based index of institutional real estate investment performance and movements in supply and demand. *Journal of Real Estate Finance and Economics* 34(1), 5–33 [S-sec]. https://ideas.repec.org/a/kap/jrefec/v34y2007i1p5-33.html
43. Fisher, J. D., Geltner, D. M., & Webb, R. B. (1994). Value indices of commercial real estate: A comparison of index construction methods. *Journal of Real Estate Finance and Economics* 9, 137–164 [S-sec]. https://link.springer.com/doi/10.1007/BF01099972
44. Fisher & Hartzell (2016). Class differences in real estate private equity fund performance. *Journal of Real Estate Finance and Economics* [S-sec; authors' initials not verified]. https://doi.org/10.1007/s11146-016-9556-1
45. Geltner, D. (1991). Smoothing in appraisal-based returns. *Journal of Real Estate Finance and Economics* 4(3), 327–345 [S via dossier 04]. https://doi.org/10.1007/BF00161933
46. Geltner, D. (1993). Estimating market values from appraised values without assuming an efficient market. *Journal of Real Estate Research* 8(3), 325–345 [S-sec]. https://ideas.repec.org/a/jre/issued/v8n31993p325-346.html
47. Gupta, A., Mittal, V., & Van Nieuwerburgh, S. (2026). Work from home and the office real estate apocalypse. *American Economic Review* 116(2), 674–709; NBER WP 30526. https://www.nber.org/papers/w30526
48. Gupta, A., & Van Nieuwerburgh, S. (2021). Valuing private equity investments strip by strip. *Journal of Finance* 76(6), 3255–3307 [S via dossier 04]. https://doi.org/10.1111/jofi.13073
49. Pagliari, J. L. (2017). Real estate returns by strategy: Have value-added and opportunistic funds pulled their weight? *Real Estate Economics* [S-sec; working paper: https://aeaweb.org/conference/2017/preliminary/paper/ed3k2AQ2 ; SSRN https://doi.org/10.2139/ssrn.4360769]
50. Pagliari, J. L., Scherer, K. A., & Monopoli, R. T. (2005). Public versus private real estate equities: A more refined, long-term comparison. *Real Estate Economics* 33(1), 147–187. https://doi.org/10.1111/j.1080-8620.2005.00115.x
51. Plazzi, A., Torous, W., & Valkanov, R. (2010). Expected returns and expected growth in rents of commercial real estate. *Review of Financial Studies* 23(9), 3469–3519 [S-sec]. https://doi.org/10.1093/rfs/hhq069
52. Riddiough, T. J., Moriarty, M., & Yeatman, P. J. (2005). Privately versus publicly held asset investment performance. *Real Estate Economics* 33(1), 121–146 [citation S; findings U]. https://doi.org/10.1111/j.1080-8620.2005.00114.x
53. Takahashi, D., & Alexander, S. (2002). Illiquid alternative asset fund modeling. *Journal of Portfolio Management* 28(2), 90–100. https://doi.org/10.3905/jpm.2002.319836

Internal: G14 `research/groups/dossiers/G14_ra_actions_financing.md` (instrument library, Townsend/PREA payouts, CBRE lending terms, Jiang–Matvos–Piskorski–Seru, Chen & Chen, transfer taxes); G15 `research/groups/addenda/G15_calcs/g15_ra_results.json` (Real Assets book and cash map); main and groups reports as cited.

