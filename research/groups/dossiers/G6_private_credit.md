# Group stream G6: Private Credit — loan-pool cash flows, defaults, leverage and natural DPI

**As of:** 2026-10-18. **Scope:** ADIC's Private Credit group (working NAV ≈ US$14bn, synthetic): direct lending/unitranche, asset-based finance (ABF), mezzanine and opportunistic credit, held through SMAs, closed-end funds, evergreen (semi-liquid) vehicles and listed BDCs. The deliverable is a simulation-ready loan-pool/fund model with regime-dependent parameters, an impairment-aware NAV model, and SELL / HOLD / REFINANCE / LEVER economics.

**Evidence tags.** [S] sourced fact (dated; citation in §10). [P] practitioner consensus. [I] my inference, assumption or calculation. [K] cited from domain knowledge, not re-verified in this session. "(excerpt)" = taken from a search-result excerpt, not a full read. "(aggregator)" = taken from a secondary data aggregator (Yardeni Private Credit Monitor), not the primary filing.

**Research-process caveat.** The session-wide web-search budget ran out part-way through this stream. After that, I used only direct fetches of primary URLs already identified. Consensus (consensus.app) exposed only its authentication tools, so it was not used. Items I could not verify are flagged and listed in §9.

**Overlap with sibling dossiers.** Secondary-market mechanics, NAV-loan and CFO structures are in `05_secondaries_navfin.md`. Portfolio-level leverage and funding curves are in `06_leverage.md`. Return fusion is in `07_return_fusion.md`. The PE cash-flow engine is in `04_pe_cashflows.md`. This dossier adds credit-specific depth and links to those streams rather than repeating them.

---

## 1. Executive summary

1. **The credit cycle has turned, and the measured default rate depends on the definition.** As of Q2–Q3 2026:
   - **Fitch** U.S. Private Credit Default Rate: **6.3%** trailing 12 months (TTM) to August 2026, a series record. 47% of events were PIK or interest deferrals, 41% maturity extensions and only 8% hard payment defaults [S].
   - **Proskauer** (payment and covenant defaults only): **2.51%** in Q2 2026, after 1.84%, 2.46% and 2.73% in the three prior quarters [S].
   - **KBRA DLD:** **2.0%** TTM, with non-accruals at 1.8% (14 Oct 2026). Its 2026 forecast is 2.5% loan-weighted, up from 1.4% in 2025 [S].
   - **Lincoln** "bad-PIK" shadow default rate: **6.2%** of loans in Q2 2026, against 2.5% in Q4 2021 [S].

   The model must therefore simulate *payment default*, *selective default* (PIK switches and distressed amend-and-extend) and *loss* as separate states. A single payment-default rate understates impairment roughly 2–3× [I].
2. **2026 is a live stress test of semi-liquid private credit.**
   - Average redemption requests at the largest non-traded BDCs were **13.9% of NAV in Q2 and 13.0% in Q3 2026**, against 5% quarterly caps. Most funds prorated [S].
   - The Fed found that accepted redemptions exceeded inflows in Q1 2026 for the first time [S].
   - The IMF estimates buffers last **9–11 quarters** under mild stress but only **5–7 quarters** under a moderate shock [S].
   - **Design rule:** evergreen redemption rights are not liquidity. Model them as a queue with stochastic fulfilment.
3. **Marks lag, so reported NAV overstates economic value in stress.**
   - The IMF shows BDC first-lien marks move much less than B-rated loan prices, with gaps persisting for quarters [S].
   - Mid-2026 marks averaged **$0.98** against $0.96 for public loans [S].
   - Third-party tenders for non-traded BDC shares were priced at **15–30% discounts to NAV** (aggregator).
   - Every SELL/HOLD decision must run on a *desmoothed economic NAV*, not on the GP mark.
4. **Private credit is ADIC's best natural-DPI asset, but only if reinvestment can be switched off.** In a synthetic regime-switching model of a $14bn book [I], first-year cash under run-off is:

   | Regime | Run-off cash, % of NAV (after draws and fees) |
   |---|---|
   | Benign | 37% |
   | Normal | 30% |
   | Tight (today) | 22% |
   | Crisis | 14% |

   The reinvest policy yields only about 7%. Compare the PE distribution rate of **9% in H1 2026** (MSCI) [S]. Run-off is a "slow SELL" with no discount. In the synthetic model it beats selling LP interests unless ADIC's liquidity shadow price λ exceeds about 2% (Normal), 8% (Tight) or 21% (Crisis), at a SOFR+5% discount rate.
5. **Rates reach defaults through interest coverage.**
   - Average private-credit ICR was about 2.0× (vs 2.7× for leveraged loans) in 2023 [S].
   - 2021–22 vintages show median cash ICR of 1.7–1.8× [S].
   - The FOMC hiked to **3.75–4.00% on 16 Sep 2026** [S].
   - With a lognormal ICR cross-section calibrated so that 10% of borrowers sit below 1×, a +100bp base-rate shock raises the stressed share ×1.36. +300bp raises it ×2.2, and +300bp plus a 20% EBITDA fall raises it ×3.6 [I]. That matches the IMF's estimate that selective defaults could rise two- to three-fold in stressed scenarios [S].
6. **Leverage pays only while losses stay low, and back-leverage has a cure tail.**
   - Cliffwater's year-end-2025 inputs (SOFR 3.50%, spread 5.50%, OID 0.50%, losses 0.65%, 1.0× debt at 5.50%) give **6.84% unlevered and 8.93% levered** net returns [S].
   - 1× leverage adds value only while annual losses stay below about 4% of assets [I].
   - With a 65% contractual advance rate and lender marks, the synthetic probability of a borrowing-base deficiency within 3 years is ≈1% at a 45% starting LTV in Normal. It is ≈22% at 50% LTV in Tight and ≈41% at 50% LTV in Crisis [I].
   - **Default limit:** starting LTV ≤40–45% (≥20pp headroom).
7. **Forecasts are biased upward.**
   - Group forecasts use loss-adjusted yield (YTM − PD×LGD). The usual biases: PIK and OID counted as cash yield; recoveries benchmarked to syndicated loans (52%) when direct loans recovered about 33% [S]; narrow default definitions; a 3-year "takeout" life that extends in stress; smoothed marks.
   - Erel, Flanagan and Weisbach find net-of-fee risk-adjusted abnormal returns of private debt funds are statistically insignificant [S].
   - Shrink group alpha toward zero and fuse with market-implied loss-adjusted yields.
8. **Recommendation for the IC (current state RED).**
   - **HOLD** senior SMA books in run-off mode and turn reinvestment off where the documents allow.
   - **Do not REFINANCE above ~45% LTV.**
   - **SELL** only junior or software-heavy fund interests whose economic NAV is below the bid.
   - **Keep dry powder** for credit secondaries, which are richest when liquidity is scarce: H1-2026 credit secondary volume was $20bn, a record [S].

---

## 2. Core concepts and theory

### 2.1 What ADIC owns: four segments, four wrappers
- **Segments** [P]:
  - Direct lending: senior/unitranche, floating, sponsor-backed, ~5-year legal maturity, ~3-year expected life.
  - ABF: amortizing collateral pools with borrowing bases, exposed to fraud and collateral risk.
  - Mezzanine: fixed coupon with a PIK portion, low recovery.
  - Opportunistic: stressed or rescue financing with higher spread and equity-like risk.
- **Wrappers:**
  - SMAs: ADIC controls reinvestment and back-leverage.
  - Closed-end funds: the GP controls recycling during the investment period, with fund-level facilities.
  - Evergreen BDCs and interval funds: redemption queue, 5% quarterly cap.
  - Listed BDCs: daily liquidity at a P/NAV discount.

  The wrapper determines which SELL/HOLD/REFINANCE/LEVER (S/H/R/L) levers exist.
- **Market size** [S]:
  - Fed: U.S. private credit loans ≈ $1.4tn in H2 2025.
  - FSB: $1.5–2tn global at end-2024.
  - IMF: ≈$2.1tn including dry powder (2023).
  - Fed: perpetual BDCs hold $306bn gross / $161bn net assets; interval funds $119bn / $80bn. Together they are about 20% of private-credit net AUM.

### 2.2 Return anatomy
For a floating-rate loan held to its expected life $T_e$, the (unlevered) loss-adjusted yield is

$$\text{LAY}=\underbrace{\bar r^{fwd}+s}_{\text{coupon}}+\underbrace{\frac{o}{T_e}}_{\text{OID/fees}}-\underbrace{\text{PD}\cdot\text{LGD}}_{\text{expected loss}}-\text{fees},$$

and a fund levered at debt/equity $\ell$ with funding cost $c_B$ earns

$$r_E\approx \text{LAY}_{gross}+\ell\,(\text{LAY}_{gross}-c_B)-\text{fees}(\ell).$$

Cliffwater's 2026 decomposition is the canonical practitioner version [S]:

| Item | Value |
|---|---|
| SOFR | 3.50% |
| Loan spread | 5.50% |
| OID income | 0.50% |
| Credit losses | 0.65% unlevered; 1.30% at 1× |
| Cost of debt | 5.50% |
| Management fee | 1.00% unlevered; 1.25% levered |
| Incentive fee | 15% over a 6% preferred return |
| **Net return** | **6.84% unlevered; 8.93% levered; 8.34% public BDCs** |

### 2.3 Default as an intensity driven by coverage, not by price
Borrowers default when cash flow cannot cover debt service after liquidity buffers. With sponsors, defaults are often deferred through PIK, amendments or equity cures. So the hazard depends on interest coverage (ICR = EBITDA/interest), and the ICR moves with both base rates and earnings:

$$\text{ICR}_{i,t}=\frac{\text{EBITDA}_{i,t}}{D_{i,t}\,(\max(r_t,f_i)+s_i)} .$$

This is a reduced-form intensity model, Cox-process style [K: Lando 1998; Duffie & Singleton 1999], with a structural covariate.
- **Cross-sectional ICR dispersion** turns a shift in the mean into a convex rise in the "stressed share" (ICR < 1).
- **Correlated frailty** across borrowers produces default clustering [K: Duffie, Eckner, Horel & Saita 2009].
- **PD–LGD correlation:** recoveries fall when defaults rise [K: Altman, Brady, Resti & Sironi 2005; Frye 2000].

### 2.4 Three default concepts, and why they matter for ADIC

| Concept | Measured by | Level, mid-2026 | Role in model |
|---|---|---|---|
| Payment / covenant default | Proskauer; KBRA DLD (excludes PIK shifts and covenant violations) | 2.0–2.7% | Transition to non-accrual and workout |
| Selective default (PIK switch, distressed A&E, distressed exchange) | Fitch PCDR; Moody's (1.6% vs 4.7% for 2025 depending on inclusion of distressed exchanges) | 5.7–6.3% | Transition to the PIK/impaired state; income becomes non-cash |
| Shadow default (PIK added after close) | Lincoln bad PIK | 6.2% of loans | Leading indicator of loss |

All values [S]; see §4.2.

PIK-by-amendment predicts trouble:
- In US BDC loan data, PIK toggles are associated with a 1–2 percentage point higher next-quarter delinquency probability on a 3% base. This is an association with delinquency, not a measured default effect, and it is second-hand: Rintamäki & Steffen (2025) as reported by the FSB; the paper itself was not read [E] [corrected 2026-10-18: previously tagged [S] and worded as "add"].
- The bad-PIK cohort's average LTV rose from 39.4% at inception to 76.1% (Lincoln, Q1 2026) [S].

### 2.5 Marks: appraisal smoothing applied to loans
- **Reported fair value is mark-to-model** (ASC 820 Level 3). It adjusts partially toward economic value each quarter.
- **Partial-adjustment model** [K: Geltner 1993; Getmansky, Lo & Makarov 2004]:
  $$p^{R}_t=p^{R}_{t-1}+\kappa\,(p^{E}_t-p^{R}_{t-1}),\qquad \kappa\in(0,1].$$
- **The mark gap creates first-mover incentives** in redeemable vehicles, which the IMF warned of in 2024 and which surfaced in 2026 [S].
- **Secondary buyers and lenders price off market-based marks.** So SELL and REFINANCE outcomes depend on $p^E$, while ADIC's reported performance depends on $p^R$.

### 2.6 Liquidity: contractual self-liquidation vs embedded liquidity calls
A loan book returns principal through amortization, prepayment, maturity and recovery. In a run-off book this is natural DPI.

Against it sit:
- delayed-draw term loans (DDTLs) and revolvers, which are drawn in stress (the March-2020 "dash for cash," when "all firms drew down bank credit lines" in the first phase [S: Acharya & Steffen 2020]);
- fund-level borrowing-base cures;
- for evergreen holders, the inability to get out.

Bank-ALM analogies:
- The Basel LCR assumes 30-day drawdowns of 10% on committed credit facilities to non-financial corporates and 30% on liquidity facilities [S, via 04 dossier].
- An NSFR-style rule should stop short-term funding of these loans.

### 2.7 Cross-disciplinary transfers
- **Actuarial/insurance:**
  - Credibility-weighted loss estimates by segment and vintage (Bühlmann 1967).
  - Reserving triangles for recoveries (incurred-but-not-recovered).
  - Run-off accounting for books closed to new business: the "run-off" policy here is literally that.
- **Mortgage-backed securities (MBS) prepayment modelling:** CPR/SMM with refinancing incentive (spread tightening) and burnout [K: Stanton 1995]. This is the private-credit analog of 2024-style repricing waves.
- **Operations research:** the semi-liquid redemption mechanism is a capacity-constrained queue (5% cap per period). Requests that exceed capacity accumulate as backlog; the reneging and resubmitting behaviour matters.
- **Control theory:** borrowing-base covenants are barrier constraints, $h_t = BB_t - B_t \ge 0$. Keep headroom proportional to collateral volatility, in control-barrier-function style.
- **Real options:** SELL is an American option with a regime-dependent strike (secondary price). Run-off vs reinvest is a switching option whose value rises with new-issue spreads (dry-powder value).

---

## 3. Methods/models and trade-offs

| Method | Use | Strengths | Weaknesses | Recommendation |
|---|---|---|---|---|
| Loan-level competing-risks hazard MC (default / prepay / PIK switch / A&E) | Core engine for SMA look-through and fund look-through | Captures ICR, sector, vintage and sponsor effects; impairment states explicit | Needs loan tapes; heavy compute | **Primary** where ADIC has tapes (SMAs, large funds) |
| Cohort (pool) Markov model with regime-dependent transition rates | Funds without tapes; fast scenario runs | Simple, fast, calibratable to Fitch/KBRA/Lincoln series | Loses borrower heterogeneity | **Primary** for fund interests; used in the §6.8 illustration |
| Vasicek / Gaussian-copula one-factor loss distribution | Tail loss, concentration | Closed-form Large Homogeneous Pool (LHP) quantiles [K: Vasicek 2002; Gordy 2003] | Static; wrong tails if correlation mis-set | Cross-check for P95/P99 losses |
| Takahashi–Alexander (TA) fund model (Takahashi & Alexander 2002; L=6, B=1.0, Y=8% in 04 dossier) | Pacing for new commitments | Matches LP cash-flow data | No credit states; no rate link | Use only for new commitments; replace with cohort model for existing book |
| Structural (Merton-type) firm model | Stress mapping (EBITDA → default) | Economic interpretability | Data-hungry for private firms | Use the ICR-distribution reduced form instead (§6.4) |
| Desmoothing (Geltner 1993 inverse; Kalman state-space with public-loan/BDC factors) | Economic NAV and mark gap | Uses LSTA/BDC prices as observables | κ unstable in calm periods | **Required** for S/H decisions |
| LSMC / real-options on regime lattice | SELL/REFI timing; run-off switch | Handles path dependence | Per-asset; approximation error | Asset-level screens |
| Queue model for evergreen redemptions | Liquidity of semi-liquid holdings | Captures caps, proration, backlog | Behavioural parameters uncertain | **Required** wherever ADIC holds evergreen units |
| Bayesian hierarchical PD/LGD (segment × vintage × sponsor) | Shrinkage of sparse default data | Partial pooling, credible intervals | Prior sensitivity | For calibrating hazards and the group-forecast bias |

**Why a hybrid?** ADIC needs three things the methods above provide separately:
- impairment states, for the RED light;
- liquidity paths, for natural DPI and draws;
- decision values, for S/H/R/L.

A cohort-level competing-risks engine with an ICR covariate delivers all three in a 50,000-path total-portfolio simulation, and degrades gracefully to fund-level data. Loan-level detail is added where tapes exist [I].

---

## 4. Empirical evidence and current market data (dated, sourced)

### 4.1 Returns, yields and spreads

| Series | Value | As of | Source |
|---|---|---|---|
| CDLI (unlevered, gross; BDC assets) | H1 2026 **+3.0%**; TTM **+7.7%**; ~22-yr average 9.5% | 30 Jun 2026 | Cliffwater release 19 Aug 2026 [S] |
| CDLI realized losses | ≈0.5%, "one-half their 1.0% long-term average" | H1 2026 | same [S] |
| CDLI software markdowns | 3% in Q1 2026; <1% in Q2 | 2026 | same [S] |
| CDLI non-interest cash flow (repayments) | "above 6% per quarter" | mid-2026 | same [S] |
| Private vs public loan prices | $0.98 vs $0.96 (Morningstar LSTA LL100) | Jun 2026 | same [S] |
| CDLI size | 23,000+ loans, $553bn | Jun 2026 | same [S] |
| CDLI 2023 | total 12.13%; income 12.08%; realized −0.86% (long-term −1.03%); unrealized +0.92% | CY2023 | Cliffwater Q4-2023 report (excerpt) |
| CDLI 2025 interest income | 10.4% | CY2025 | Cliffwater 2025 release (excerpt) |
| CDLI income return | 10.9% a year (2005–2024) vs HY 7.4%, leveraged loans 5.9% | 2005–2024 | Golub (CDLI data) [S] |
| MSCI Global Private Credit closed-end fund index | 2023 10.2%; 2024 7.5%; 2025 9.5%; Q3-25 2.0; Q4-25 1.7; Q1-26 0.9; Q2-26 1.7 | Q2 2026 | MSCI [S] |
| MSCI direct lending sub-index | 12.1 / 7.5 / 10.8; quarterly 1.8, 1.5, 0.4, 1.0 | Q2 2026 | MSCI [S] |
| MSCI opportunistic lending sub-index | 11.4 / 8.4 / 9.4; Q2-26 2.4 | Q2 2026 | MSCI [S] |
| New-issue spreads (KBRA DLD, Sep 2026) | UMM/large-cap LBO **S+512**; core MM S+510; lower MM S+528 | Sep 2026 | KBRA [S] |
| Spread moves (KBRA DLD) | average LBO spreads +40bp vs Feb-2026 low; private vs single-B premium 177bp | Sep 2026 | KBRA [S] |
| Leverage and equity (KBRA DLD) | total leverage 4.3–4.6×; equity contribution 67% | Sep 2026 | KBRA [S] |
| Volume (KBRA DLD) | 3Q26 $38.9bn, lowest since 2Q23; 2026 run-rate ≈$200bn, −38% y/y | Sep 2026 | KBRA [S] |
| Unitranche terms (VRC) | coupons S+500–575; credit spreads S+525–600; OID 98.75–99.25; spot yields 9.33–10.08%, up ≈35bp q/q | 30 Sep 2026 | VRC [S] |
| Peak vs now | spread ≈6% over SOFR at the 2023 peak; all-in yields fell from 11%+ to ≈8.5%; SOFR from ≈5.4% to 3.73% | Feb 2026 | Fortune [S] |
| Cliffwater YE-2025 inputs | spread 5.50%, OID 0.50% a year, losses 0.65% | 31 Dec 2025 | Cliffwater 2026 report [S] |
| Base rates | SOFR **3.89%** (15 Oct 2026); FOMC +25bp to 3.75–4.00% (16 Sep 2026); 10y UST 5.09% | Oct 2026 | 06 dossier [S]; GFM [S] |

*Read [I]:* spreads compressed from ≈S+600 (2023) to a ≈S+470 low (Feb 2026), then widened by 40–50bp as stress built. New-issue yields are back near 10%. The existing book, priced at 2025 spreads, is under water by roughly 2.5 × 50bp ≈ 1.25 points on a spread-duration basis.

### 4.2 Defaults, non-accruals, PIK, recoveries

**Fitch U.S. Private Credit Default Rate (PCDR)** [S]
- TTM: 5.6% (Dec 2025), 5.8% (Jan 2026), 5.7% (Q1), 6.0% (Q2), 6.1% (Jul), **6.3% (Aug 2026)**.
- Event mix: 47% PIK/deferral, 41% maturity extensions, 8% payment defaults, 4% bankruptcy or restructuring.
- By sector: healthcare 9.9%, industrials 9.9%, software 0.6%.
- By borrower size: under $25m EBITDA, 12%.
- By component: Model-Implied Credit Opinion (MCO) 5.6%; Privately Monitored Ratings (PMR) 8.5%.

**Proskauer** [S]
- Quarterly: Q3-25 1.84%, Q4-25 2.46%, Q1-26 2.73%, Q2-26 **2.51%** (716 loans; $195.6bn).
- By EBITDA band: 1.9% below $25m; 3.4% at $25–50m; 2.4% at $50m or more.

**KBRA** [S]
- DLD TTM: 2.3% by count in Jun 2026, matching the late-2023 peak; 2.0% by Oct 2026.
- Non-accruals 1.8%.
- 2026 forecast 2.5% loan-weighted (1.4% in 2025); about 3.5% by count, roughly 111 issuers.
- KBRA Middle Market Default Monitor: 3.3% by count, 2.4% by debt (12 months to Jun 2026).

**Lincoln** (Q2 2026) [S]
- Covenant defaults 2.7% (six-year average 3.9%).
- PIK in 11.1% of loans; 11.3% of interest income.
- Bad PIK 6.2% of all loans.
- Lender takeovers $22.3bn in H1 2026 vs $24.2bn in all of 2025, 70% of it from 2021–22 buyouts.
- Software loans with LTV above 50% marked at 87.1% of par.

**PIK history** (OHA/T. Rowe Price, Lincoln data) [S]
- PIK-by-amendment share of direct-lending investments: 2.6% (Q4-21), 3.5% (Q4-22), 5.4% (Q4-23), 6.6% (Q4-24), 6.1% (Q3-25).
- PIK at origination: 4–5%.
- PIK was 7% of CDLI net investment income in Q2 2025.
- PIK-at-origination typically expires within ~2 years and pays a 25–50bp premium. The cash portion is typically "base rate plus half of the loan's spread".

**BDC aggregates** (aggregator)
- Median non-accruals 2.8% in Q2 2026, the highest since 2017.
- PIK at 9.8% of income in Q1 2026.
- Unrealized losses 2.35% of NAV.
- Moody's (14 Oct 2026): a "true" default rate of 5.8% vs 4% reported, with PIK masking defaults.

**Recoveries**
- Fed FEDS note (2024): direct-loan post-default value **≈33%**, vs 52% for syndicated loans and 39% for HY. More than half of value-weighted private credit is in low-collateral sectors [S].
- First-lien recoveries ≈55% (Sep 2026, aggregator).
- KBRA expects implied recoveries to "decline further," especially for smaller borrowers [S]. Its ~51–53% sample figures came only via excerpts.
- HY bond recoveries averaged 39% over 1988–2025 (36% in 2025) [S: Cliffwater].

**Interest coverage**
- Average ICR ≈2.0× vs 2.7× for leveraged loans (2023) [S: Fed note].
- Median cash ICR: 1.7–1.8× for 2021–22 vintages, ≈2.0× for 2023, 2.2–2.3× for 2024–26. 2021-vintage leverage is up ≈1.0× since origination and its ICR down ≈0.7× [S: VRC].
- More than one-third of public firms with private-credit-like size and leverage had ICR < 1 (EBIT basis) [S: IMF 2024].
- About 10% of middle-market CLO borrowers lacked cash flow to cover interest [S: FSB citing S&P].

**Covenants and amend-and-extend**
- Maturity extensions were 41% of Fitch default events (45% in August 2026) [S].
- Moody's Analytics: distressed restructurings were ≈65% of 2025 defaults [S].
- ABF Journal's reading of Lincoln data: amendments that "preempt or waive technical breaches" keep reported defaults low [S].
- The Fed (2024) cites industry commentary that recent deals are "devoid of financial maintenance covenants" [S].
- Block, Jang, Kaplan & Schulze (2024) find direct-lending funds use both financial and incurrence covenants, and that sponsors help write them [S].

### 4.3 Regulators' analyses
- **IMF GFSR April 2024, ch. 2, "The Rise and Risks of Private Credit"** [S]:
  - Vulnerabilities: fragile borrowers, semi-liquid vehicles, "multiple layers of leverage," stale valuations.
  - Leverage: BDC debt/equity ≈0.8–1.2×; closed-end funds ≈0–1.3×; middle-market CLOs ≈6×. The 95th-percentile closed-end fund has borrowing/assets of about 1.27.
  - The PIK share of BDC interest income doubled after 2019.
  - Average annual credit losses (2013–22) were below HY and bank loans.
  - BDC loan marks react far less than B-rated loan prices, and deviations "persist for several quarters".
  - Bank leverage carries LTV triggers that can force "large collateral calls," and revolver drawdowns can create "considerable funding needs".
- **IMF GFSR April 2026, ch. 1** [S]:
  - About one-fifth of direct-lending loans are in software, and software exposure "may exceed 50 percent of NAV" in leveraged vehicles.
  - Selective defaults have stabilized while payment defaults keep rising.
  - Selective defaults could rise **2–3×** under "stressed rates" or "stressed earnings" scenarios.
  - Perpetual BDCs could meet 5% quarterly redemptions for 9–11 quarters under mild stress and 5–7 under a moderate shock. The horizon is shorter with revolver draws or unsecured debt that cannot be refinanced.
- **Fed FSR, May 2026** [S]:
  - Private credit ≈$1.4tn, about one-third of below-IG non-bank-loan debt.
  - Accepted redemptions "somewhat exceeded new inflows" in Q1 2026, a first.
  - The 10 largest perpetual BDCs have bank credit and cash to cover at least three quarters of 5% net redemptions.
  - Risks "appear limited and manageable".
- **Fed FEDS notes** [S]:
  - Cai & Haque (2024): average maturity about 5 years; private credit's spread premium over TLB narrowed below 200bp and widened in 2023.
  - Berrospide et al. (2025): bank lines to private-credit vehicles of $95bn committed / $56bn utilized (2024-Q4); average rate ≈6.4% for BDCs (the note's Table 1; its text gives 6.6%); utilization ≈57%.
- **FSB, May 2026** [S]:
  - Bank credit lines to private credit ≈$220bn (member data); commercial estimates suggest more than twice that.
  - Asset-based facilities allow LTV up to 65%; NAV facilities generally ≤30%.
  - Middle-market portfolio-finance structures carry 30–40% equity tranches.
  - PIK in ≈12% of loans, about half of them toggles.
- **ECB FSR special feature, May 2026** [S]:
  - Average fund leverage is about 30% for U.S. private-credit funds.
  - Stress scenario: 10% defaults at 50% LGD in general, and **30% defaults at 80% LGD for software**. Bank losses stay ≤1.3% of equity; second-round valuation losses dominate.
- **BoE** [S]:
  - July 2026 FSR: vulnerabilities "more pronounced since the December 2025" FSR, and they could "crystallise simultaneously".
  - Private-markets system-wide exploratory scenario (SWES), launched 19 Jun 2026 with 46 firms: a 5-year global recession with CPI peaking at 7%, Bank Rate at 7%, FTSE −35% and European leveraged-loan spreads +390bp. Final report in 2027.

### 4.4 Stress episodes, autumn 2025 to 2026
- **First Brands** (Chapter 11, Sep 2025) [S]:
  - Liabilities "$10–50bn" funded by "opaque off-balance sheet financing".
  - A federal probe into alleged "double-pledging" of receivables.
  - Indictments on 29 Jan 2026; conversion to Chapter 7 on 1 Sep 2026.
  - Exposures disclosed by UBS (more than $500m), Jefferies-affiliated funds ($715m) and others.
- **Tricolor**, a subprime auto lender [S]:
  - Chapter 7 in Sep 2025; JPMorgan disclosed a $170m loss.
  - The SEC (18 Aug 2026) alleges double-pledging of loans to multiple ABS and lenders.
  - *Lesson for ABF [I]:* collateral verification and fraud are fat-tail jump risks that the default model does not capture.
- **Semi-liquid redemption wave** (aggregator unless marked):
  - BCRED ≈$3.8bn (7.9%) in Q1, then ≈10% requests prorated at 5% in Q2 and Q3.
  - Cliffwater's interval fund received 14–17% requests and was capped at 5%.
  - Blue Owl OCIC 21.9% (Q1) and 16.8% (Q3); OTIC 39% (Q3).
  - Ares ASIF 11.6% then 14.4%; Apollo ADS 11.2%, 16.8% and 14.7%.
  - Q2-2026 requests were 12.4% of NAV with 38% fulfilled (aggregator).
  - Q3 averages from VRC [S] are in §1.
  - Blue Owl stopped retail redemptions at a private debt fund in Feb 2026, and its shares fell 6% [S: Fortune]. The aggregator identifies the fund as OBDC II, halted 19 Feb and put into wind-down 21 Apr.
- **Software/AI repricing:**
  - CDLI software marks −3% in Q1 2026 [S].
  - Software credits priced 50–100bp wider (VRC) [S].
  - Software spreads gapped 50bp over non-software tech (KBRA) [S].
  - Fitch's software default rate stays low, at 0.6% [S]: so far the risk shows up as marks and spreads more than defaults.
- **Middle East conflict** from late Feb 2026 (BoE) [S], and a Fed hike in Sep 2026 [S]. That is a stagflation-type macro mix, unfavourable to floating-rate borrowers.

### 4.5 Secondary and financing markets (S/H/R/L inputs)
- **Credit LP-interest pricing** (Jefferies, % of NAV; via 05 dossier): 2019 85, 2020 78, 2021 83, 2022 72, 2023 77, 2024 91, 2025 91; H1 2026 ≈89 (via summaries) [S/C].
- **Evercore H1 2026** [S]:
  - Credit secondaries **$20bn**, surpassing FY2025, mostly GP-led.
  - GP-led credit priced ≈**99% of FMV**; high-quality senior portfolios "at Par or better".
  - $31bn of dedicated equity dry powder; more than 90% of buyers plan to raise more.
- **Loan trades:** most observed secondary loan trades were above 95% of par (Lincoln, Q2 2026) [S].
- **BDC equity:**
  - Public BDCs ≈80% of NAV (Feb 2026, Raymond James via iCapital) [S].
  - Many at 10–20% discounts, some at 40–50% (Oct 2026, VRC) [S].
  - Tender offers for non-traded BDC shares at 15–30% discounts to NAV (Jul 2026, aggregator).
- **Fund leverage:**
  - Average BDC debt/equity 0.91× against a 2.0× regulatory limit (Feb 2026) [S].
  - The BDC debt/equity cap rose from 1 to 2 in 2018 [S: IMF].
  - Bank lines cost ≈6.4% (2024-Q4, when SOFR was ≈4.3–4.6%) [S: Berrospide et al., Table 1; the note's text gives 6.6%], i.e. ≈SOFR+200bp [I]. Either figure gives roughly S+180–230bp. The S+200 is this dossier's inference, not the note's.
  - Back-leverage terms: see the FSB items in §4.3.

---

## 5. Practitioner and peer practice; case studies

- **How credit teams forecast** [P, with sources]:
  - Underwriting uses a base-case yield to a 3-year takeout. Cliffwater defines "3Yr Takeout Yield" assuming par repayment in three years, "the average life of direct loans" [S].
  - Expected loss is PD × LGD, from internal ratings or private credit estimates (S&P credit estimates, Fitch MCO/PMR, KBRA).
  - Levered fund IRR targets sit on top. In survey evidence, funds target unlevered returns that the authors judge high relative to risk, and use leverage, but much less than banks and CLOs [S: Block et al., paraphrased].
  - Quarterly valuations are yield-based (discount rate calibrated to market spreads), or recovery-based once impaired, often by third-party agents.
- **Typical forecast biases**, and the ADIC correction for each:

  | # | Bias | Evidence | ADIC correction |
  |---|---|---|---|
  | 1 | Yield illusion: PIK and OID booked as income | PIK = 11.3% of interest income [S: Lincoln] | Forecast cash yield separately |
  | 2 | Recovery optimism: syndicated-loan recoveries (52%) used where direct loans realized ≈33% [S: Fed] | IMF notes lower collateralization in software [S] | Use segment- and regime-specific recoveries |
  | 3 | Narrow default definitions | 2.5% vs 6.3% for the same market and quarter [S] | Model selective default explicitly |
  | 4 | Life-extension blind spot: the 3-year takeout fails in stress | 41% of defaults are maturity extensions [S] | Stress-dependent prepayment and extension |
  | 5 | Mark smoothing: NAV at 98–99 vs secondary at 89 and BDC equity at 0.8× | [S] | Desmoothing |
  | 6 | Vintage complacency: 2021–22 deals at 6–7× leverage | 70% of 2026 takeovers [S] | Vintage factor |
  | 7 | Gross-to-net slippage: fees and leverage costs absorb most excess return | Net risk-adjusted abnormal return insignificant [S: Erel et al. 2024] | Net everything |

  The prior deck's memo corpus already flags "distribution timing too optimistic after spread shocks" and says to "challenge recovery assumptions" (context §2, slide 8).
- **Case: semi-liquid vehicles in 2026** [S/aggregator]:
  - The 5% cap held at most funds, but proration fed further requests: the FSB notes limits "may also have stimulated further redemption pressures".
  - Q1 liquidity was partly sponsor-supplied (BCRED: cap raised to 7% with $400m of firm capital, aggregator).
  - *Lesson [I]:* the gate is a discretionary option held by the manager. ADIC holding evergreen units has a claim on a queue, not on cash.
- **Case: sponsor support vs lender takeover.** PE sponsors inject equity when stress looks transient; the IMF finds sponsored loans default less in stress [S]. In 2025–26, though, lenders took the keys on $22–24bn a year (Lincoln) [S]. *Model implication [I]:* a sponsor-support probability that falls with sponsor fund age, the size of the equity cushion and the regime.
- **Case: back-leverage in March 2020.** Industry commentary cited by the IMF says private-credit funds faced collateral pressures in 2020 [S]. Market-value facilities with lender marks are the transmission channel. Borrowing-base facilities with ratings-based advance rates are slower but similar.
- **Peer allocators:** public and private pension funds together held about 31% ($307bn) of private-credit fund assets (Form PF, Q4 2021) [S: Fed 2024, Cai & Haque] [corrected 2026-10-18: previously "U.S. public pensions account for about 31% of private-credit fund investors"]. I could not verify SWF-specific practices on SMA back-leverage or run-off policies in this session (§9).

---

## 6. Design implications for the ADIC framework

### 6.1 Role of the Private Credit group in the total-portfolio approach (TPA)
1. **Contractual liquidity ladder.** Run-off cash flows enter the liquidity engine at regime-conditional P05 values, not at their means.
2. **Credit-risk sleeve with a lagged mark.** Economic NAV drives risk and decisions; reported NAV drives reporting and IC optics.
3. **Opportunity set** (credit secondaries, rescue financing). It is richest when ADIC's liquidity shadow price is highest, so dry powder carries option value. This matches §1A implication 5 in the context file.

### 6.2 State variables (quarterly; monthly for evergreen queues and margin)
- **Global/market:**
  - credit regime $s_t\in\{B,N,T,C\}$, from the state engine with posterior $\pi_t$;
  - SOFR $r_t$ and its forward curve;
  - new-issue spread $s^{new}_t$ by segment;
  - LSTA price index $L_t$ and HY OAS;
  - BDC P/NAV index $q_t$;
  - systematic EBITDA index $E_t$;
  - frailty $\xi_t$;
  - credit-secondary price $\pi^{sec}_t$;
  - back-leverage terms $(a_t, s^B_t)$.
- **Per loan or cohort $i$ (segment $k$, vintage $v$, sponsor flag):**
  - par $P_{i,t}$ (including capitalized PIK);
  - status $\sigma_{i,t}\in\{\text{C}, \text{P}, \text{N}, \text{R}, \text{X}\}$: cash-pay, PIK-amended, non-accrual/workout, resolved, repaid;
  - spread $s_i$ and floor $f_i$;
  - origination PIK fraction $\pi^0_i(t)$;
  - remaining OID $o_{i,t}$;
  - maturity $T_i$ and amortization $a_i$;
  - undrawn commitment $U_{i,t}$;
  - $\text{ICR}_{i,t}$, $\text{LTV}_{i,t}$, sector (software flag);
  - economic price $p^E_{i,t}$ and reported price $p^R_{i,t}$.
- **Per vehicle $j$:**
  - wrapper type, investment-period flag, recycling rights;
  - facility balance $B_{j,t}$, advance rate $a_j$, eligibility rules, cure period;
  - unsecured notes maturities;
  - fees;
  - LP unfunded $C^{unf}_{j,t}$;
  - evergreen request backlog $Q_{j,t}$;
  - ADIC ownership share.
- **Three return series per asset:**
  - $y^{UW}_i$: underwritten YTM and EL at close;
  - $y^{ACT}_i$: realized IRR to date on cash flows plus $p^R$;
  - $y^{GRP}_i$: the group's forward LAY.

### 6.3 Decision variables
- **Per SMA:**
  - reinvestment switch $\rho_{j,t}\in[0,1]$, the share of principal recycled;
  - back-leverage draw or paydown $\Delta B_{j,t}$;
  - loan sales $x_{i,t}$;
  - new commitments $n_{j,t}$.
- **Per fund interest:**
  - SELL fraction $x_{j,t}$, with cash or deferred structure;
  - REFINANCE via LP-level NAV loan or rated feeder/CFO, with amount $L_{j,t}$;
  - new commitment $n_{j,t}$.
- **Per evergreen:** tender request $R^{req}_{j,t}$.
- **Per listed BDC:** sale $x_{j,t}$ at $q_t\cdot$NAV.
- **Group-level:**
  - target book size and segment mix;
  - DDTL funding policy;
  - dry-powder reserve for opportunistic secondaries $D^{op}_t$.

### 6.4 Core equations

**(1) Coupons and income** (quarter Δ = 0.25):

$$c_{i,t}=\max(r_t,f_i)+s_i\ \text{(floating)}\quad\text{or}\quad c_i\ \text{(fixed)}$$

$$I^{cash}_{i,t}=\mathbb 1_{\sigma=C}\,P_{i,t}c_{i,t}\Delta\,(1-\pi^0_i(t)),\qquad I^{PIK}_{i,t}=\mathbb 1_{\sigma=C}P_{i,t}c_{i,t}\Delta\,\pi^0_i(t)+\mathbb 1_{\sigma=P}P_{i,t}(c_{i,t}+\delta^{PIK})\Delta$$

- $\delta^{PIK}\approx$ 25–50bp [S: OHA].
- OID is received in cash at funding and accreted by the effective-interest method. For income forecasting, use $o_i/T_e$ per year.
- Non-accrual loans earn zero income; reverse any accrued-unpaid income at transition.

**(2) Hazards** (competing risks, annualized; quarterly probability $1-e^{-h\Delta}$):

$$h^{def}_{i,t}=\phi^{def}_k\cdot \Phi\!\left(\frac{-\ln \overline{\text{ICR}}_{c,t}}{\sigma_{ICR}(s_t)}\right)\cdot \xi_t\cdot e^{\beta'x_i}\qquad\text{(cohort form)}$$

$$\overline{\text{ICR}}_{c,t}=\text{ICR}_{c,0}\cdot\frac{E_t}{E_0}\cdot\frac{r_0+s_c}{r_t+s_c},\qquad \xi_t=e^{\sigma_\xi Z_t-\sigma_\xi^2/2}$$

- $h^{sw}$ (cash-pay → PIK) has the same form with $\phi^{sw}$.
- PIK-cohort default: $h^{def}_P=m_P\cdot h^{def}$, with $m_P$ calibrated to the FSB's second-hand report of Rintamäki–Steffen (+1–2pp next-quarter delinquency over a 3% base, US BDC loans), i.e. ×1.3–1.7 on delinquency [E/I]. The source effect is an association with delinquency, so applying it to the default hazard is an assumption [corrected 2026-10-18: previously tagged [S/I]].
- PIK cure: $h^{cure}$ falls as stress rises.
- Covariates $x_i$: sector (software), sponsor (−), vintage 2021–22 (+), EBITDA < $25m (+; Fitch 12% vs about 6% overall) [S].
- Prepayment (refinancing incentive and exit activity):

$$\text{CPR}_{i,t}=\text{CPR}_k(s_t)\cdot\exp\!\big(\beta_{ref}(s_i-s^{new}_t)^+ +\beta_X X^{exit}_t\big),\qquad \text{SMM}=1-(1-\text{CPR})^{\Delta}$$

  $X^{exit}$ is the PE exit-window factor from the 04 dossier: sponsor exits repay loans.
- Maturity: if stressed at $T_i$, extend with probability $e_k(s_t)$ (defaults 0.2/0.3/0.5/0.6 by regime [I]). The extension adds 4–8 quarters, +50–100bp and often PIK. This counts as a selective default.

**(3) Defaults, recoveries and workout:**

$$\text{Def}_{i,t}=P_{i,t}(1-e^{-h^{def}\Delta}),\quad R_i=\bar R_k(s_{\tau})\,(1+\eta\varepsilon_i),\quad \text{RecCash}_{t}=\omega(s_\tau)\,W^{rec}_{t-1},\quad \omega=1/\tau_w$$

- Loss is recognized at default: $(1-R_i)\text{Def}_{i,t}$.
- Expected recovery $W^{rec}$ is carried at PV until it is resolved.
- PD–LGD correlation comes from $\bar R_k(s)$ falling with the regime.

**(4) Par roll-forward:**

$$P_{t+1}=P_t+I^{PIK}_t-A_t-\text{Prep}_t-\text{Def}_t+\text{Draw}_t+\rho_t(\text{A}_t+\text{Prep}_t+\text{RecCash}_t)$$

The last term applies for reinvested or new loans at $s^{new}_t$, so the composition updates.

**(5) Delayed-draw and revolver commitments:**

$$\text{Draw}_{i,t}=U_{i,t}\big(1-(1-d_k(s_t))^{\Delta}\big),\qquad U_{i,t+1}=U_{i,t}-\text{Draw}_{i,t}-U_{i,t}\tfrac{\text{Prep}+A}{P}-\text{Expiry}$$

- The crisis draw rate is front-loaded in the first two quarters (dash for cash).
- Drawn revolvers enter $P$ at $p^E$ below par in stress, so the lender funds at par an asset worth less.

**(6) Marks:**

$$p^E_{i,t}=1-D^s_i\,(s^{mkt}_{k,t}-s_i)-\ell^{liq}-\mathbb 1_{\sigma=P}\,\theta^{PIK},\qquad p^R_t=p^R_{t-1}+\kappa(s_t)(p^E_t-p^R_{t-1})$$

- Defaults: $D^s\approx2.5$ years, $\ell^{liq}\approx0.3$ points, $\theta^{PIK}\approx$ 10–15 points; workout loans are carried at $R_i$.
- **Desmoothing for decisions:** $\hat p^E_t=(p^R_t-(1-\kappa)p^R_{t-1})/\kappa$. Use a Kalman filter with observables $L_t$ (LSTA), $q_t$ (BDC P/NAV) and secondary prints.

**(7) Fund layer:** assets $A_{j,t}$, debt $B_{j,t}$, equity $E_{j,t}=A-B$.
- Borrowing base:
  $$BB_{j,t}=a_j\Big[\sum_{\sigma=C}P\,p^L_{t}+\epsilon^{PIK}\sum_{\sigma=P}P\,p^L_t\Big],\qquad \text{deficiency } \Delta^{BB}_{j,t}=(B_{j,t}-BB_{j,t})^+$$
  - $p^L$ are lender-agent marks, close to loan-sale prices: 1.00/0.99/0.96/0.85 by regime [I].
  - $\epsilon^{PIK}\approx0.5$; non-accrual loans are ineligible.
  - A deficiency must be cured within the cure period by cash, collateral or sales at $p^{sale}$.
- BDC asset coverage: $A/B\ge1.5$.
- Interest: $B(r_t+s^B(s_t))\Delta$.
- LP cash flow: distributions = net income (cash) + return of capital (post investment period, or when $\rho<1$) − calls (unfunded, DDTL funding) − cures. For closed-end funds the GP chooses $\rho$ in the investment period.

**(8) Evergreen queue** (per vehicle, quarterly):

$$R^{paid}_t=\min\big(Q_{t-1}+R^{new}_t,\ \bar c\,\text{NAV}_t,\ \text{Liq}_t\big),\quad Q_t=\varsigma\,(Q_{t-1}+R^{new}_t-R^{paid}_t)$$

- Cap $\bar c$ = 5%.
- $\varsigma$ is the resubmission share. Industry requests $R^{new}/\text{NAV}$ were 1.6% (Q3-25), 4.8% (Q4-25), ≈12–14% (Q2–Q3 2026) [S].
- Fulfilment is ≈38% in a gated quarter (aggregator).

**(9) ADIC cash and NAV aggregation:** $CF^{PC}_t=\sum_j \text{own}_j\cdot CF^{LP}_{j,t}+\sum_{SMA}(\ldots)$. Economic NAV is $\sum \text{own}_j E^E_{j,t}$ and reported NAV is $\sum \text{own}_j E^R_{j,t}$. Intra-ADIC transfers (for example, Secondaries buying a PC fund stake) net to zero liquidity, per §1A.

### 6.5 Regime-dependent parameters (defaults; recalibrate quarterly)

| Parameter | B (benign) | N (normal) | T (tight; Oct 2026) | C (crisis) | Basis |
|---|---|---|---|---|---|
| New-issue unitranche spread | S+470–500 | S+525 | S+525–600 | S+700–900 | Fortune (≈S+600 peak 2023; 8.5% all-in Feb 2026); KBRA S+510–528 (Sep 2026); VRC S+500–600; C: BoE SWES LL +390bp [S/I] |
| OID (points) | 0.75–1.0 | 1.0 | 1.0–1.5 | 2–3 | VRC; Lincoln 1.5 [S]; C [I] |
| Payment default (annual, par-weighted) | 1.0–1.3% | 1.5–1.8% | 2.3–2.6% | 5–8% | KBRA 1.4% (2025), 2.5% (2026F); IMF 2–3×; synthetic model §6.8 [S/I] |
| Selective default (incl. PIK switch, distressed A&E) | 3–4% | 4.5–5% | 6–6.5% | 11–18% | Fitch 5.6–6.3%; Lincoln 6.2% [S]; C [I] |
| Recovery: DL first-lien/unitranche | 65% | 60% | 50–55% | 35–45% | Fed 33% post-default value; 55% first-lien (aggregator); ECB 50% LGD [S/I] |
| Recovery: ABF / mezz / opportunistic | 75/35/55% | 70/30/50% | 62/22/40% | 50/12–15/30% | HY 39% average as a mezz ceiling [S]; [I] |
| Software overlay (C only) | — | — | spread +50–100bp | default ×3, LGD 80% | VRC, KBRA [S]; ECB scenario [S] |
| Workout length (quarters) | 4–6 | 6 | 8 | 10–12 | [P/I] |
| CPR (prepay + maturity), DL | 30–35% | 22–26% | 12–16% | 5–8% | avg life 3y ≈ ⅓ turnover; >6%/qtr repayments mid-2026 [S]; T/C [I] |
| ABF scheduled amortization | 20%/yr | 20% | 20% | 15% | [I] |
| Undrawn draw rate (annual) | 15% | 20% | 30% | 60% (front-loaded) | Basel LCR 10%/30d; Acharya–Steffen [S/I] |
| PIK share of interest income | 6–7% | 7–9% | 10–12% | 15–20% | 7% (Q2-25), 11.3% (Q2-26) [S]; C [I] |
| Mark catch-up κ per quarter | 0.5 | 0.45 | 0.4 | 0.3 | IMF 2024 lag evidence [S]; [I] |
| Spread duration $D^s$ | 2.5–3.0 years | | | | 3y takeout life [S]; [I] |
| Credit LP secondary price (% NAV) | 0.97–1.00 | 0.92–0.95 | 0.85–0.89 | 0.70–0.78 | Jefferies 2020 78, 2022 72, 2024–25 91, H1-26 89; Evercore [S] |
| Performing-loan sale price (% par) | 1.00 | 0.99 | 0.95–0.97 | 0.80–0.88 | Lincoln >95 [S]; C [I] |
| Listed BDC P/NAV | 1.00–1.05 | 0.95 | 0.80–0.90 | 0.60–0.70 | iCapital/VRC [S]; C [K] |
| New back-leverage advance rate | 65–70% | 60–65% | 55% | 40–50% | FSB ≤65% [S]; [I] |
| Back-leverage cost | S+175–200 | S+200 | S+225–275 | S+300–400 or closed | Fed 6.4% (2024-Q4; Table 1, the note's text gives 6.6%); Cliffwater, Lincoln S+200 [S]; [I] |
| Evergreen requests (% NAV per quarter) | 1–3% | 2–5% | 10–17% | 15–25% | 2026 data [S]; iCapital 20% scenario [S] |
| Evergreen fulfilment at 5% cap | 100% | 100% | 30–50% | 20–35% | [S/aggregator]; [I] |
| Default-rate elasticity to base rate (via ICR) | +100bp → ×1.36; +300bp → ×2.2 | | | | own calculation, σ_ICR = 0.54 [I] |
| Quarterly regime transitions (rows B, N, T, C) | B 0.85/0.12/0.02/0.01; N 0.05/0.85/0.08/0.02; T 0.02/0.12/0.80/0.06; C 0.03/0.07/0.20/0.70 | | | | [I]; stationary 20/43/28/9%; replace with the state-engine HSMM |

### 6.6 Constraints (recommended defaults; IC to ratify)
1. **Liquidity counting.**
   - PC run-off cash counts at regime-conditional P05 in the 12-month liquidity test.
   - Evergreen units count at $\min(\bar c, \text{expected fulfilment})\times$NAV per quarter, and zero in C.
   - DDTL/revolver draws count as contingent outflows at the C rate.
2. **Back-leverage headroom.** $P(\Delta^{BB}>0 \text{ within } 12\text{m})\le2\%$ and within 36 months ≤5%, implying a starting LTV of about 40–45% at a 65% advance rate (§6.8).
3. **Asset coverage.** BDC-style A/B ≥ 1.5 hard. Internal look-through debt/equity ≤ 1.0×.
4. **Concentration.**
   - Software ≤ 15% of PC economic NAV (vs ≈20% of DL loans market-wide [S]).
   - Single borrower ≤ 2%.
   - Single manager ≤ 20%.
   - Evergreen units ≤ 10% of PC NAV.
5. **Credit-risk budget.** 5-year P99 cumulative loss ≤ 20% of PC NAV, and PC contribution to total-portfolio CVaR95 ≤ its budget.
6. **Tier 1 compatibility.** Any LEVER or REFINANCE action must pass the deck's robust floor and liquidity gate, including the cure tail.

### 6.7 Objective terms and shadow prices
- PC enters Tier 2 through:
  - expected log-wealth contribution, net LAY × NAV;
  - minus expected loss and CVaR of cumulative loss;
  - minus financing costs;
  - minus the expected cure cost $\times(1+\lambda^{cure})$;
  - plus the liquidity value $\lambda_t\times$ cash released.
- The optimizer's liquidity dual $\lambda_t$ is the exchange rate for run-off, SELL and REFINANCE.
- The **reinvestment option value** $V^{reinv}_t=\mathbb E[\text{PV}(s^{new}_t-c^{opp}_t)]$ is the forgone carry when switching to run-off. It is highest in T/C, when $s^{new}$ is wide.

### 6.8 Decision economics: illustrative results from the synthetic model
*All numbers are SYNTHETIC and [I]: a $14bn book (DL 60%, ABF 15%, mezz 10%, opportunistic 15%), quarterly regime chain as in §6.5, 20,000 paths. Script: session scratchpad `g6_scripts\g6_pc_pool_sim.py` (path in §7). Not ADIC data.*

**A. One-year outcomes by regime, run-off policy (% of starting NAV)**

| Regime | Interest cash | Principal | Draws | Net cash | Payment default | Selective default | Loss |
|---|---|---|---|---|---|---|---|
| B | 8.2 | 30.7 | −0.9 | **37.2** | 1.35 | 3.8 | 0.56 |
| N | 8.6 | 23.7 | −1.3 | **30.3** | 1.77 | 4.9 | 0.82 |
| T | 9.0 | 15.4 | −2.0 | **21.6** | 2.30 | 6.4 | 1.27 |
| C | 8.8 | 9.8 | −4.2 | **13.7** | 4.08 | 11.1 | 2.71 |

*Read:* the synthetic selective-default rate in T (6.4%) reproduces Fitch's 6.3% [S]. The crisis-year payment default of 4.1% rises in year 2.

**Natural DPI vs PE.**
- MSCI's PE distribution rate was 24% (2017) and 27% (2021), against 9–11% in 2022–H1 2026 [S].
- PC run-off delivers 2.4× PE's current rate in T and about 3–4× PE's crisis rate (≈3–5% under the 04 dossier's $m^D$ 0.3–0.35) [I].
- Under reinvestment PC delivers only ≈7% of NAV a year, so **the reinvestment switch is the liquidity lever** [I].
- For ADIC's $14bn, switching from reinvest to run-off in T adds ≈$2.2bn in year 1. That is 12–25% of the $8.9–17.7bn payout, for SMA and harvest-period books only [I].

**B. Five years starting in T**

| Policy | Cumulative net cash: mean (P05–P95) | Year-1 cash: mean (P05) | Cumulative loss: mean / P95 / P99 (% NAV) | Max reported-vs-economic gap: mean / P95 |
|---|---|---|---|---|
| Run-off | $12.2bn ($10.3–13.7bn) | $3.2bn ($2.5bn) | 6.1 / 12.6 / 17.2 | 2.0% / 3.5% |
| Reinvest | $5.0bn ($4.4–5.4bn) | $0.9bn | 8.4 / 16.9 / 22.5 | 2.1% / 3.6% |

The synthetic κ catches up quickly. Real gaps are likely larger (IMF evidence), so test with κ = 0.2–0.3.

**C. SELL (LP interest at the regime price) vs HOLD (run-off).** The break-even liquidity premium is $\lambda^*=V^H/(\pi\,\text{NAV})-1$; SELL only if $\lambda_t>\lambda^*$.

| Start regime | Sale price | $V^H$ at SOFR+5% | $\lambda^*$ at SOFR+5% | $\lambda^*$ at SOFR+3% | $\lambda^*$ using $V^H$ at P05 (SOFR+5%) |
|---|---|---|---|---|---|
| N | 0.94 | $13.46bn | 2.3% | 7.7% | −2.6% |
| T | 0.88 | $13.25bn | **7.5%** | 13.8% | 0.6% |
| C | 0.75 | $12.69bn | **20.8%** | 28.2% | 8.9% |

*Rule [I]:* sell in T only junior, software-heavy or tail positions where $\hat p^E<\pi$, or when the optimizer's λ exceeds the threshold. Never sell senior books in C unless λ exceeds about 20%.

**D. REFINANCE (back-leverage) cure tail.** $4bn equity, $8bn of first-lien loans at inception, 65% contractual advance rate, lender marks, PIK loans 50% eligible, 3-year horizon:

| Starting LTV | P(deficiency): start N | start T | start C | Mean cure given deficiency |
|---|---|---|---|---|
| 40% | 0.05% | 0.1% | 1.5% | ≈$0.06–0.11bn |
| 45% | 1.0% | 3.0% | 12.8% | ≈$0.12–0.20bn |
| 50% | 13.2% | 22.3% | 41.4% | ≈$0.17–0.31bn |
| 55% | 30.3% | 50.1% | ≈100% | ≈$0.37–0.39bn |

*Reading [I]:*
- REFINANCE at ≤40–45% LTV is a cheap bridge: S+200 on proceeds of ≈$3.2–3.6bn per $8bn of loans.
- At 50% or more it embeds a short put on credit marks, exercised exactly when λ spikes.
- **Rated feeder/CFO** structures (05 dossier: senior LTV 35–45%, ≈S+250–300bp, 6–12-month lead time) avoid mark-to-market cures but must be set up before stress.

**E. LEVER.**
- Equity return at debt/equity ℓ: $r_E=y_A-\text{EL}+\ell(y_A-\text{EL}-c_B)-\text{fees}$. Leverage adds value iff $\text{EL}<y_A-c_B\approx$ 9.5% − 5.5% = **4.0%** a year (Cliffwater YE-2025 inputs [S]; arithmetic [I]).
- The synthetic C-year loss (2.7%) clears this hurdle. A P99 five-year loss (≈17–22%) concentrated in two years (≈9–11% a year) does not.
- Lincoln (Q2 2026) estimates a ≈9% cumulative principal loss sends a levered S+500 loan (1.5% OID, S+200 debt, 50% leverage) to zero IRR [S]. I could not reconcile that with simple carry arithmetic, which gives a higher break-even. Treat it as Lincoln's figure.
- *Rule:* LEVER only senior, non-software books in B/N, at ≤1.0× debt/equity, and never in T/C.

**F. Group-specific S/H/R/L menu**

| Action | Definition (PC group) | Economics | Main risk |
|---|---|---|---|
| SELL | LP-interest secondary (cash or deferred); single-loan or portfolio sales; listed BDC sales; evergreen tenders | $\pi(s)\,\text{NAV}(1+\lambda)$; loans at $p^{sale}$; BDC at $q_t$ | Selling at a stressed π; signalling; tender proration |
| HOLD | Hold to maturity, reinvesting ($\rho=1$) or in run-off ($\rho=0$) | $V^H$; run-off releases principal at no discount | Credit losses; extension risk |
| REFINANCE | SMA back-leverage; LP-level NAV loan; rated feeder/CFO; sale of senior A-notes keeping B-notes | Proceeds ℓV at $r+s^B$; value $=\lambda L-\text{PV(cost)}-\mathbb E[\text{cure}](1+\lambda^{cure})$ | Borrowing-base cures; refinancing at maturity; encumbrance |
| LEVER | Raise fund debt/equity; fund DDTLs; new commitments or credit-secondary purchases in stress | $r_E$ formula; secondary α when discounts are wide | Loss amplification; wrong-way liquidity |

### 6.9 Calibration targets (dated)
1. **Default levels:**
   - Fitch PCDR 6.3% (Aug 2026); KBRA DLD 2.0% (Oct 2026), non-accrual 1.8%.
   - Proskauer 2.51% (Q2 2026); Lincoln bad PIK 6.2% (Q2 2026).
   - Mix: 47% PIK/deferral, 41% extensions.
2. **Returns:** CDLI TTM 7.7% (Jun 2026); realized loss ≈0.5% vs 1.0% long-term; MSCI private credit 9.5% (2025).
3. **Spreads:** S+510–528 (Sep 2026), +40bp from the Feb-2026 low; spot unitranche 9.33–10.08% (Q3 2026).
4. **ICR:** mean ≈2.0×; 2021–22 vintages 1.7–1.8×; about 10% of borrowers below 1×.
5. **Repayments:** above 6% of assets per quarter (normal-to-tight); average life ≈3 years.
6. **Evergreen requests:** 13.9% (Q2) and 13.0% (Q3) of NAV vs a 5% cap.
7. **Secondary pricing:** credit LP interests at 89–91% (2025–26) and 72% (2022); GP-led credit at 99% (H1 2026).
8. **Mark gap:** CDLI $0.98 vs LSTA $0.96 (Jun 2026). BDC equity at 0.8–0.9× NAV is an upper-bound proxy for the economic-to-reported discount, because it includes manager and leverage effects.

### 6.10 Data ADIC must supply
- **Loan tapes:**
  - for SMAs and the top 20 funds: par, spread, floor, OID, maturity, amortization, PIK status and history, non-accrual flag;
  - borrower EBITDA, leverage, ICR, LTV, sector, sponsor;
  - undrawn DDTL/revolver.
- **Vehicle documents:** investment period, recycling, leverage, facility terms (advance rates, eligibility, valuation agent, cure periods), fees, redemption terms.
- **Cash-flow history** (calls, distributions) and quarterly NAV by holding.
- **Underwriting memos:** underwritten YTM, EL, base and downside cases.
- **The positions behind the "credit stress RED / sleeve impaired" signal.**

### 6.11 SPECIFICATION CARD (Private Credit group)

| Item | Specification |
|---|---|
| **Data fields (per loan/cohort)** | id, vehicle, own%, segment {DL, ABF, MEZZ, OPP}, vintage, sponsor flag, sector (software flag), par, spread $s$, floor $f$, fixed coupon, PIK-at-origination % and expiry, PIK-amended flag/date, OID remaining, maturity, amortization, undrawn DDTL/revolver, EBITDA, total leverage, ICR, LTV, status {C, P, N, R, X}, $p^R$ (GP mark), last secondary/loan-sale print |
| **Data fields (per vehicle)** | wrapper {SMA, CEF, evergreen, listed BDC}, investment-period end, recycling rule, facility (B, advance rate a, eligibility, cure period, spread, maturity), unsecured notes, fees (mgmt, incentive, hurdle), unfunded, redemption cap/backlog, P/NAV if listed |
| **Return and cash-flow equations** | Coupons/PIK: §6.4(1). Hazards with ICR covariate: §6.4(2). Recovery/workout: (3). Par roll-forward with reinvest switch ρ: (4). DDTL draws: (5). Marks and desmoothing: (6). Fund borrowing base, cures, LP cash flows: (7). Evergreen queue: (8). Net LP return $r_E=y_A-\text{EL}+\ell(y_A-\text{EL}-c_B)-\text{fees}$ |
| **Parameter defaults** | Regime table §6.5. ICR mean 2.0×, σ_ICR = 0.54 (10% below 1×); $\phi^{def}=0.17$, $\phi^{sw}=0.35$ per unit stressed share; frailty $\sigma_\xi=0.35$; $D^s=2.5$; κ 0.5/0.45/0.4/0.3; fees 1.0% of NAV all-in (SMA 0.5–0.75%) |
| **Liquidity terms** | SMA: run-off principal 22–30% a year (N), 12–16% (T), 5–8% (C). CEF: income distributions ≈7–9% during the investment period, then income + principal. Evergreen: 5%/qtr cap, fulfilment 100/100/30–50/20–35%. Listed BDC: daily at P/NAV 1.0/0.95/0.85/0.65 |
| **Stress behaviour** | Prepayments collapse; DDTL draws spike (60% a year, front-loaded); PIK switches and extensions rise; recoveries fall; marks lag (gap 2–10%); back-leverage cures; evergreen gates; secondary π 0.70–0.78 |
| **SELL** | LP secondary at π(s)·NAV (deferred: +≈4pp price, receivable ≤12m per 05 dossier); loan sales at $p^{sale}$; BDC at $q_t$; evergreen tender (queue). Execute iff $\lambda_t>V^H/(\pi\,\text{NAV})-1$ |
| **HOLD** | ρ = 1 (reinvest) or ρ = 0 (run-off). Run-off is the default liquidity lever in T/C for SMAs and harvest-period funds; value forgone = reinvestment option $V^{reinv}$ |
| **REFINANCE** | Back-leverage ≤40–45% starting LTV (65% advance), S+200 (N) / S+225–275 (T); rated feeder/CFO set up in B/N; LP NAV loan ≤ 15–25% LTV per 05 dossier. Gate: P(cure in 36m) ≤ 5% |
| **LEVER** | Fund debt/equity ≤1.0× for senior non-software books in B/N only; EL < $y_A-c_B$ (≈4%) test under P95 losses; opportunistic credit-secondary purchases from the dry-powder reserve when π ≤ 0.85 |
| **Forecasts and biases** | Group forecast = forward LAY on mark. Known upward biases: PIK/OID-in-yield, recovery (use 33–55% not 60–70%), narrow default definition, 3-year-life assumption, smoothed marks, vintage 2021–22, gross-to-net. Shrink group alpha toward 0 (Erel et al.); fuse with market-implied LAY using the 07 dossier's credibility weights |
| **Synthetic-data defaults (label SYNTHETIC)** | $14bn NAV: DL 60% (S+550, 1% amortization), ABF 15% (S+475, 20% amortization), mezz 10% (12% fixed, ⅓ PIK), OPP 15% (S+750). Wrappers: SMA 40%, CEF 45%, evergreen 10%, listed BDC 5%. Undrawn $1.0bn; fund unfunded $3.0bn; look-through debt/equity 0.5–0.75× |
| **Links to other groups** | PE/Co-invest: shared borrowers and sponsors (wrong-way; sponsor support); X^{exit} drives prepayments. Secondaries: credit-secondary pricing and dry powder (conflict controls). Capital Solutions: ABF/NAV lending overlap, REFINANCE pricing, CFO expertise. Public Markets: listed BDCs, HY/loan managers; LSTA/BDC prices as nowcast observables. Overlay: CDX HY/loan hedges for marks (basis risk); rate hedges vs floating-rate income. Treasury: DDTL draws, cures, calls |

---

## 7. Implementation notes
- **Libraries:**
  - `numpy` + `numba`: vectorized cohort Monte Carlo (MC); loans × paths arrays with float32 where safe.
  - `pandas`: tapes and cash-flow ledgers.
  - `scipy.stats`: Φ, copulas.
  - `statsmodels`: Markov-switching and discrete-time logit hazards.
  - `lifelines` and `scikit-survival`: Cox and competing-risks (Aalen–Johansen; Fine–Gray, i.e. Fine & Gray 1999) estimation on loan histories.
  - `QuantLib-Python`: SOFR schedules, ACT/360, floors, amortization.
  - `pymc` or `numpyro`: hierarchical PD/LGD with segment × vintage × sponsor pooling.
  - `pykalman` or `statsmodels` `UnobservedComponents`: mark desmoothing.
  - `cvxpy`: the outer optimizer with shadow prices.
- **Algorithms:**
  - Run aggregated cohorts (segment × vintage × rating × sponsor) for the 50k-path total-portfolio engine. Run loan-level only for SMAs and stress deep-dives.
  - Use common random numbers across policies (run-off vs reinvest, S/H/R/L) so differences are low-variance.
  - Use importance sampling on frailty $Z$ for P99 losses, and Sobol QMC for regime paths.
  - Use LSMC on regime-state features ($p^E$, λ, $s^{new}$, π) for optimal SELL timing.
- **Numerical pitfalls:**
  - **Hazard units.** Annual → quarterly is $1-e^{-h\Delta}$, not $h\Delta$, at crisis levels. Competing risks must share one draw per period.
  - **PIK.** Capitalize PIK before computing next-period interest. Never count PIK in cash yield or in DPI.
  - **Non-accrual.** Reverse accrued income at transition, and carry workout loans at PV of recovery, not at par.
  - **OID.** Amortize by EIR over the *expected* life. Re-estimate the life when prepayment speeds change, or income is mis-timed.
  - **Revolver draws.** Fund drawn amounts at par but mark them at $p^E$, which creates an immediate loss in stress.
  - **Desmoothing.** κ estimates are unstable in calm samples; impose priors (0.3–0.6) and validate against 2020 and 2022.
  - **Definitions.** Map each external series (Proskauer, KBRA, Fitch, Lincoln) to the model state it measures before calibrating. Never calibrate one hazard to a mixture.
  - **Index biases.** CDLI is BDC-based, valuation-based, asset-weighted and partly back-tested (pre-2015) [S]. MSCI is fund-level with LP-reported cash flows. Neither is a loan-level default database.
  - **Units and seeds.** Keep units consistent (US$bn, quarterly) and use deterministic seeds. The illustration script is `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g6_scripts\g6_pc_pool_sim.py`, with results JSON in the same scratchpad under `g6_out\`. Both are session-scoped; copy them to `src/` if retained.

---

## 8. Risks, pitfalls and limitations
1. **No full-cycle history at today's scale.** The IMF notes the sector "has never experienced a severe economic downturn at its current size". Hazard calibrations rest on 2020 and 2022–26, plus leveraged-loan analogs [S].
2. **Definitional and data opacity.** Private ratings, manager marks and inconsistent default definitions (2.5% vs 6.3%) make calibration fragile. Report ranges rather than point estimates.
3. **Concentration in software and AI.** About 20% of DL loans are software, and exposure exceeds 50% of NAV in leveraged vehicles [S]. Today the stress shows up in marks and spreads, not defaults (Fitch software 0.6%). A regime change could arrive as a jump; the ECB uses 30% default at 80% LGD [S].
4. **Fraud and collateral jumps in ABF** (First Brands, Tricolor) are not captured by ICR hazards. Add a compound-Poisson jump with collateral-audit controls [I].
5. **Wrong-way liquidity.** In C, PC run-off slows, DDTLs draw, back-leverage cures and evergreen gates bind, all while PE DPI collapses and overlay margin rises. The PC book helps liquidity less exactly when it is most needed. Its liquidity value must use P05, not mean.
6. **Rate double-edge.** Floating coupons raise income in hikes but raise defaults through ICR. The September 2026 hike and the 10y at 5.09% point to T persisting [S].
7. **Model risk** in the synthetic engine:
   - ICR dispersion and the φ parameters set the rate elasticity;
   - recovery and workout timing drive loss timing;
   - the mark-gap model is simple.

   All §6.8 numbers are illustrative.
8. **Governance.** GP marks feed reported performance and incentive fees. Secondary quotes from ADIC's Secondaries group and refinancing quotes from Capital Solutions need conflict controls (§1A).

---

## 9. Open questions (including what ADIC must confirm)
1. What drives "credit stress RED / private credit sleeve impaired"? Which positions, what loss estimate, and is it marks, non-accruals or PIK?
2. What is the actual split by segment and wrapper, and how much of the book can switch to run-off within 12 months (SMA rights; funds past their investment period)?
3. Undrawn DDTL/revolver amounts and fund unfunded commitments within the ~$38bn total unfunded.
4. Existing back-leverage and fund facilities: advance rates, valuation agent, cure mechanics, maturities.
5. Evergreen holdings: current tender status, backlog and fulfilment.
6. Underwritten vs actual vs group-forecast data, needed to estimate group bias, and the group's EL methodology.
7. **Not verified in this session** (search budget exhausted):
   - full CDLI annual series (2024 return; 2025 components beyond the excerpt);
   - Jefferies H1-2026 credit pricing from the primary document (image-only PDF);
   - KBRA recovery-rate sample figures;
   - the Research Square preprint on 2026 gates (content not retrievable);
   - Moody's "true default" methodology;
   - the private-credit CDS index launched in Apr 2026 (aggregator only);
   - SWF/peer SMA practices;
   - BDC P/NAV in March 2020.
8. Should ADIC's owner-payout band (§1) interact with PC run-off? For example, pre-commit PC run-off to fund the 5% floor in T/C.

---

## 10. References
*[V] = read in this session (full text or official page). [E] = search excerpt only. [K] = from domain knowledge, not re-verified. [M] = metadata confirmed in the 2026-10-18 literature check (Crossref; web sources where no DOI exists); the text was not re-read.*

**Market data and practitioner sources**
- Cliffwater (19 Aug 2026). *Private Credit Shows Resilience in Cliffwater Direct Lending Index Data* (PR Newswire). https://www.prnewswire.com/news-releases/private-credit-shows-resilience-in-cliffwater-direct-lending-index-data-302854703.html [V]
- Cliffwater (31 Mar 2026). *Cliffwater Direct Lending Index Data Supports Strength of Private Credit* (2025 results). https://www.cliffwater.com/files/docs/CliffwaterPressRelease_CDLI_2025_Results.pdf [E; certificate error on fetch]
- Cliffwater (Jan 2026). *2026 Asset Allocation Report* (S. L. Nesbitt). https://www.bdcs.com/docs/CapitalMarketAssumptions.pdf?v=20220116 [V]
- Cliffwater (Dec 2025). *CDLI fact page*. https://www.bdcs.com/docs/CDLI-Fact-Page.pdf [V]
- Golub Capital (Jul 2025). *Consistent Yield Cushion Helps Smooth the Ride* (CDLI income data). https://education.golubcapital.com/wp-content/uploads/2025/07/3-5-Consistent-Yield-Cushion-Helps-Smooth-Ride-20250729.pdf [V]
- Proskauer (28 Jul 2026). *Private Credit Default Index Reveals Rate of 2.51% for Q2 2026*. https://www.proskauer.com/report/proskauers-private-credit-default-index-reveals-rate-of-251-for-q2-2026 [V]
- Proskauer (2026). *... Rate of 2.73% for Q1 2026*. https://www.proskauer.com/report/proskauers-private-credit-default-index-reveals-rate-of-273-for-q1-2026 [V]
- Global Finance (Sep 2026). *Fed Rate Hike Squeezes an Already Stressed Private Credit Sector* (Fitch PCDR, Aug 2026). https://gfmag.com/private-credit/fed-rate-hike-squeezes-an-already-stressed-private-credit-sector/ [V]
- Funds Society (2 Mar 2026). *U.S. Private Credit Default Rate Continues to Climb* (Fitch PCDR, Jan 2026). https://www.fundssociety.com/en/news/alternatives/u-s-private-credit-default-rate-continues-to-climb/ [V]
- KBRA DLD (14/16 Oct 2026). *Monthly Insights & Outlook — At a Glance*. https://www.kbra.com/analytics/products/dld/insights/monthly-insights-and-outlook-at-a-glance-october-14-2026 [V]
- The Lead Left (Oct 2026). *KBRA DLD Default Indices*. https://theleadleft.com/kbra-dld-default-indices/ [V]
- Private Equity Wire (17 Jun 2026). *Private credit default rates return to peak levels, says KBRA*. https://www.privateequitywire.co.uk/private-credit-default-rates-return-to-peak-levels-says-kbra/ [V]
- Alternative Credit Investor (25 Nov 2025). *Defaults set to rise as mid-market faces "force of reckoning"*. https://alternativecreditinvestor.com/2025/11/25/defaults-set-to-rise-as-mid-market-faces-force-of-reckoning/ [V]
- Lincoln International (Aug 2026). *The Lincoln Private Market Index: Earnings Growth Drove a Q2 Rebound*. https://www.lincolninternational.com/news/the-lincoln-private-market-index-earnings-growth-drove-a-q2-rebound-while-private-markets-became-more-selective/ [V]
- ABF Journal (2025). *Covenant Defaults and the "Bad PIK" Signal*. https://www.abfjournal.com/covenant-defaults-and-the-bad-pik-signal-what-lincoln-internationals-senior-debt-index-is-telling-direct-lenders/ [V]
- Fortune (22 Feb 2026). *Private credit market shadow default rate*. https://fortune.com/2026/02/22/private-credit-market-shadow-default-rate-deals/ [V]
- Kaden Wood Capital (2026). *Private Credit Default Rates in 2026: Why Published Numbers Range From 2.5% to 6%*. https://kadenwoodcapital.com/perspectives/special-situations-into-2027 [V]
- Valuation Research Corporation (8 Oct 2026). *Private Market Trends: Q3 2026*. https://www.valuationresearch.com/insights/private-credit-trends-q3-2026/ [V]
- Yardeni Research. *Private Credit Monitor* (aggregator of 2026 fund events). https://yardeni.com/tools/private-credit-monitor [V; aggregator]
- iCapital (3 Mar 2026). *BDC Redemptions: Looking Beyond the Gates*. https://icapital.com/insights/investment-market-strategy/bdc-redemptions-looking-beyond-the-gates/ [V]
- OHA / T. Rowe Price (2025–26). *PIKing Your Spots in Private Credit*. https://www.troweprice.com/content/dam/gdx/pdfs/2026-q1/piking-your-spots-in-private-credit.pdf [V]
- MSCI (Sep 2026). *MSCI Private Capital Benchmarks Summary Q2 2026*. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf [V]
- Evercore (Jul 2026). *H1 2026 Secondary Market Review*. https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf [V]
- Jefferies (Jul 2026). *Global Secondary Market Review*. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf [image-only; figures via 05 dossier]

**Regulators and official sector**
- IMF (Apr 2024). *Global Financial Stability Report*, ch. 2, "The Rise and Risks of Private Credit". https://www.imf.org/-/media/files/publications/gfsr/2024/april/english/ch2.pdf [V]
- IMF (Apr 2026). *Global Financial Stability Report*, ch. 1. https://www.imf.org/-/media/files/publications/gfsr/2026/april/english/ch1.pdf [V]
- Federal Reserve (May 2026). *Financial Stability Report — Funding Risks*. https://www.federalreserve.gov/publications/2026-may-financial-stability-report-funding-risks.htm [V]
- Cai, F. & Haque, S. (23 Feb 2024). *Private Credit: Characteristics and Risks*. FEDS Notes. DOI 10.17016/2380-7172.3462. https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html [V]
- Berrospide, J., Cai, F., Lewis-Hayre, S. & Zikes, F. (23 May 2025). *Bank Lending to Private Credit: Size, Characteristics, and Financial Stability Implications*. FEDS Notes. DOI 10.17016/2380-7172.3802. https://www.federalreserve.gov/econres/notes/feds-notes/bank-lending-to-private-credit-size-characteristics-and-financial-stability-implications-20250523.html [V]
- FSB (6 May 2026). *Report on Vulnerabilities in Private Credit*. https://www.fsb.org/uploads/P060526.pdf [V]
- ECB (May 2026). *Stress in global private credit markets and its implications for euro area financial stability*. FSR special feature. https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202605_04~3f2135af91.en.html [V]
- Bank of England (7 Jul 2026). *Financial Stability Report — July 2026*. https://www.bankofengland.co.uk/financial-stability-report/2026/july-2026 [V]
- Bank of England (19 Jun 2026). *Private markets SWES: publication of the stress scenario*. https://www.bankofengland.co.uk/financial-stability/boe-system-wide-exploratory-scenario-exercise/publication-of-the-stress-scenario-for-the-private-markets-system-wide-exploratory-scenario [V]

**Episodes**
- Wikipedia. *First Brands Group*. https://en.wikipedia.org/wiki/First_Brands_Group [V]
- Wikipedia. *Tricolor Holdings*. https://en.wikipedia.org/wiki/Tricolor_Holdings [V]

**Academic**
- Erel, I., Flanagan, T. & Weisbach, M. S. (2024). *Risk-Adjusting the Returns to Private Debt Funds*. NBER WP 32278 (March 2024), DOI 10.3386/w32278; SSRN versions DOI 10.2139/ssrn.4771873 and 10.2139/ssrn.4779852; no journal version in Crossref. https://www.nber.org/papers/w32278 [V]. An April 2026 draft with the same title revises most estimates but not the conclusion cited here (insignificant net abnormal return), per `research/literature/recheck/G3_cap_solutions.recheck.md`.
- Block, J., Jang, Y. S., Kaplan, S. N. & Schulze, A. (2023/2024). *A Survey of Private Debt Funds*. NBER WP 30868; *Review of Corporate Finance Studies* 13(2). https://www.nber.org/papers/w30868 [V]
- Chernenko, S., Erel, I. & Prilmeier, R. (2022). *Why Do Firms Borrow Directly from Nonbanks?* *Review of Financial Studies* 35(11): 4902–4947. https://www.nber.org/papers/w26458 [V]
- Acharya, V. V. & Steffen, S. (2020). *The Risk of Being a Fallen Angel and the Corporate Dash for Cash in the Midst of COVID*. *Review of Corporate Finance Studies* 9(3): 430–471. https://www.nber.org/papers/w27601 [V]
- Li, L., Strahan, P. E. & Zhang, S. (2020). *Banks as Lenders of First Resort: Evidence from the COVID-19 Crisis*. *Review of Corporate Finance Studies* 9(3): 472–500. https://www.nber.org/papers/w27256 [V]
- Rintamäki, P. & Steffen, S. (2025). *PIK Now and Pay Later - How Deferred Interest Reshapes Private Credit*. SSRN working paper, DOI 10.2139/ssrn.5341145; Crossref holds no abstract. Findings as cited in the FSB (2026) report (fn 46); SSRN page not retrieved [E].
- Altman, E., Brady, B., Resti, A. & Sironi, A. (2005). *The Link between Default and Recovery Rates: Theory, Empirical Evidence, and Implications*. *Journal of Business* 78(6): 2203–2228. DOI 10.1086/497044. [M]
- Duffie, D. & Singleton, K. (1999). *Modeling Term Structures of Defaultable Bonds*. *Review of Financial Studies* 12(4): 687–720. DOI 10.1093/rfs/12.4.687. [M]
- Duffie, D., Eckner, A., Horel, G. & Saita, L. (2009). *Frailty Correlated Default*. *Journal of Finance* 64(5): 2089–2123. DOI 10.1111/j.1540-6261.2009.01495.x. [M]
- Lando, D. (1998). *On Cox Processes and Credit Risky Securities*. *Review of Derivatives Research* 2(2–3): 99–120. DOI 10.1007/BF01531332. [M]
- Vasicek, O. (2002). *The Distribution of Loan Portfolio Value* (Risk.net lists it as "Loan portfolio value"). *Risk* 15(12): 160–162; no DOI. Gordy, M. (2003). *A Risk-Factor Model Foundation for Ratings-Based Bank Capital Rules*. *Journal of Financial Intermediation* 12(3): 199–232. DOI 10.1016/S1042-9573(03)00040-8. [M]
- Frye, J. (2000). *Collateral Damage*. *Risk* 13(4), April 2000; the Federal Reserve Bank of Chicago copy is titled "Collateral Damage: A Source of Systematic Credit Risk". No DOI. [unverified: page range not found; issue 4 inferred from the April date] [M]
- Geltner, D. (1993). *Estimating Market Values from Appraised Values without Assuming an Efficient Market*. *Journal of Real Estate Research* 8(3): 325–345. DOI 10.1080/10835547.1993.12090713. This is the 1993 *JRER* paper, not Geltner (1991) in *JREFE*. Getmansky, M., Lo, A. & Makarov, I. (2004). *An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns*. *Journal of Financial Economics* 74(3): 529–609. DOI 10.1016/j.jfineco.2004.04.001. [M]
- Stanton, R. (1995). *Rational Prepayment and the Valuation of Mortgage-Backed Securities*. *Review of Financial Studies* 8(3): 677–708. DOI 10.1093/rfs/8.3.677. [M]
- Bühlmann, H. (1967). *Experience Rating and Credibility*. *ASTIN Bulletin* 4(3): 199–207. DOI 10.1017/S0515036100008989 (Crossref, checked 2026-10-18). It is not the 1969 paper of the same title, *ASTIN Bulletin* 5(2): 157–165, DOI 10.1017/S0515036100008023. [M]
- Takahashi, D. & Alexander, S. (2002). *Illiquid Alternative Asset Fund Modeling*. *Journal of Portfolio Management* 28(2): 90–100. DOI 10.3905/jpm.2002.319836. [M]
- Fine, J. P. & Gray, R. J. (1999). *A Proportional Hazards Model for the Subdistribution of a Competing Risk*. *Journal of the American Statistical Association* 94(446): 496–509. DOI 10.1080/01621459.1999.10474144. [M]

**Sibling dossiers (ADIC project):** `research/dossiers/04_pe_cashflows.md`, `05_secondaries_navfin.md`, `06_leverage.md`, `07_return_fusion.md`, `08_action_valuation.md`, `10_scenarios_robustness.md`.

---

## Citation corrections (2026-10-18)

*Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 ("audit"); `research/literature/G6_private_credit.lit.md` §1 fixes 1–5 and §2 table ("lit"); `research/literature/recheck/G3_cap_solutions.recheck.md` (Lando, Erel et al., Cai & Haque); and a Crossref look-up on 2026-10-18 of both Bühlmann DOIs. One line per change.*

1. §2.4: the Rintamäki & Steffen "+1–2pp" is reworded from "add" to an association with next-quarter delinquency of US BDC loans (not default), and re-tagged [S] → [E] as second-hand via the FSB (audit §2.4 item 15; VL C15).
2. §6.4(2): the basis for the $m_P$ calibration is re-tagged [S/I] → [E/I], with the same caveat that the source measures delinquency, not default (audit §2.4 item 15).
3. §5: "U.S. public pensions account for about 31% of private-credit fund investors (Form PF, 2021)" → "public and private pension funds together held about 31% ($307bn) of private-credit fund assets (Form PF, Q4 2021)" (audit §2.4 item 15; VL C21).
4. §4.3: the Berrospide et al. BDC line rate "≈6.4%" is now marked as the note's Table 1 figure, noting that its text gives 6.6% (audit §2.4 item 15; VL C19).
5. §4.5: the same mark on "≈6.4%". "≈SOFR+200bp [I]" is kept, noting that either figure gives about S+180–230bp and that S+200 is this dossier's inference, not the note's (audit §2.4 item 15; VL C19).
6. §6.5, back-leverage cost basis: "Fed 6.4% (2024-Q4)" now adds "Table 1, the note's text gives 6.6%" (audit §2.4 item 15).
7. §2.7: "(Bühlmann)" → "(Bühlmann 1967)", with a matching §10 entry (lit fix 2).
8. §3 table: the Takahashi–Alexander fund model now cites "Takahashi & Alexander 2002", with a matching §10 entry (lit fix 2).
9. §3 table: "Geltner inverse" → "Geltner 1993 inverse", naming the 1993 *JRER* paper rather than the 1991 *JREFE* paper (audit §2.6 item 4; lit fix 5).
10. §7: "Fine–Gray" now cites Fine & Gray (1999), with a matching §10 entry (an optional entry in lit §2).
11. §10 legend: adds [M] (metadata confirmed in the 2026-10-18 literature check; the text was not re-read).
12. §10 Altman, Brady, Resti & Sironi (2005): full title (adds "Theory, Empirical Evidence, and Implications"), 78(6): 2203–2228, DOI 10.1086/497044; [K] → [M] (audit §2.5; lit fix 1).
13. §10 Duffie & Singleton (1999): 12(4): 687–720, DOI 10.1093/rfs/12.4.687; [K] → [M] (audit §2.5; lit fix 1).
14. §10 Duffie, Eckner, Horel & Saita (2009): 64(5): 2089–2123, DOI 10.1111/j.1540-6261.2009.01495.x; [K] → [M] (audit §2.5; lit fix 1).
15. §10 Lando (1998): 2(2–3): 99–120, DOI 10.1007/BF01531332; [K] → [M] (audit §2.5; lit fix 1; G3 recheck, ref 55).
16. §10 Vasicek (2002): 15(12): 160–162, with Risk.net's title variant "Loan portfolio value", no DOI; [K] → [M] (audit §2.5; lit fix 1).
17. §10 Gordy (2003): 12(3): 199–232, DOI 10.1016/S1042-9573(03)00040-8; [K] → [M] (audit §2.5; lit fix 1).
18. §10 Frye (2000): adds April 2000 and the Chicago Fed copy's full title, notes that no DOI exists, and marks the page range and issue number [unverified]; [K] → [M] (audit §2.5; lit fix 1).
19. §10 Geltner (1993): 8(3): 325–345, DOI 10.1080/10835547.1993.12090713, noted as not Geltner (1991); [K] → [M] (audit §2.5 and §2.6 item 4; lit fixes 1 and 5).
20. §10 Getmansky, Lo & Makarov (2004): 74(3): 529–609, DOI 10.1016/j.jfineco.2004.04.001; [K] → [M] (audit §2.5; lit fix 1).
21. §10 Stanton (1995): 8(3): 677–708, DOI 10.1093/rfs/8.3.677; [K] → [M] (audit §2.5; lit fix 1).
22. §10 Erel, Flanagan & Weisbach (2024): adds "March 2024", DOI 10.3386/w32278, the SSRN DOIs 10.2139/ssrn.4771873 and 10.2139/ssrn.4779852, and a note on the April 2026 draft, which does not change the conclusion cited (lit fix 4; G3 recheck, ref 42).
23. §10 Cai & Haque (2024): adds DOI 10.17016/2380-7172.3462 (lit fix 4; G3 recheck, ref 41).
24. §10 Berrospide et al. (2025): adds DOI 10.17016/2380-7172.3802 (lit fix 4).
25. §10 Rintamäki & Steffen (2025): full title "PIK Now and Pay Later - How Deferred Interest Reshapes Private Credit", DOI 10.2139/ssrn.5341145, no abstract in Crossref; the entry stays [E] (lit fix 3).
26. §10 new entry: Bühlmann (1967), *ASTIN Bulletin* 4(3): 199–207, DOI 10.1017/S0515036100008989, checked in Crossref. DOI …8023 belongs to the 1969 paper of the same title, 5(2): 157–165. This settles audit §2.6 item 2: this dossier's assignment was correct.
27. §10 new entry: Takahashi & Alexander (2002), *Journal of Portfolio Management* 28(2): 90–100, DOI 10.3905/jpm.2002.319836 (lit fix 2).
28. §10 new entry: Fine & Gray (1999), *JASA* 94(446): 496–509, DOI 10.1080/01621459.1999.10474144 (optional entry in lit §2).

*Checked, no change made:*
- None of the G4 barrier re-run values (BGK shift, 49.6/62.5% LTV breach, write-off rates) appears in this dossier.
- Of the re-checked works, only Lando, Erel et al. and Cai & Haque are cited here (items 15, 22 and 23).
- This dossier cites the 33/52/39% recoveries to the FEDS Note and never to S&P, so the G3 attribution fix does not apply.
- In-text [K: …] tags are kept, because the cited texts were not re-read.
