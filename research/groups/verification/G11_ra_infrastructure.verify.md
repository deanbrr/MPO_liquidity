# G11 Real Assets infrastructure: verification log

*Adversarial fact-check of `research/groups/dossiers/G11_ra_infrastructure.md` (v1.0). Prepared 2026-10-18. The dossier was not edited.*

## 1. Summary

**What was checked.**
- **Flagged claims.** All 18 of the author's flagged claims (§2.1).
- **Other claims.** 17 further claims that are load-bearing or looked suspicious (§2.2), including every number that feeds the executive summary, the case table and the calibration targets.
- **References.** 10 academic references in detail and 15 industry documents at document level (§3).
- **Design layer.** The design implications (§6) and the specification card (§6.10), checked for reasoning, formula and admissibility errors. I read all three calculation scripts in `research/groups/addenda/G11_calcs/` and checked every dossier table against the three `*_results.json` files. I re-derived the internal sensitivities of the Monte Carlo engine in a scratch script that copies its parameters. Nothing in the project was imported, run or written, apart from this log.

**Method.**
- **Primary PDFs.** WebFetch could not read PDF streams, so I downloaded each PDF, extracted the text layer with pypdf and grepped it for every number. Files:
  - Andonov, Kräussl & Rauh (RFS open-access copy);
  - EDHECinfra P74 (May 2021);
  - Blanc-Brude & Tran (Jan 2019);
  - the SIPA 2026 CMA paper and the SIPA May-2026 factsheet;
  - GI Hub *Infrastructure Monitor 2024*;
  - Jefferies *Global Secondary Market Review* (Jul 2026);
  - Moody's (10 Jun 2020);
  - Ofwat's *Monitoring Financial Resilience Report 2024-25* (primary report, downloaded directly);
  - CBRE IM *Infrastructure Quarterly Q4 2025*;
  - Flyvbjerg et al. (arXiv full text).
- **Web pages (WebFetch).** Bloomberg/EDHECinfra, MSCI (Q1-2026 results and the Nov-2025 Quick Take), CBRE IM Q2-2026 and Q3-2026, the Stonepeak-Plus 10-K, The UK Water Report, Emerald (Wurstbauer & Schäfers), the Preqin blog and the Infra Insight blog (Bitsch et al. dataset).
- **Metadata.** Crossref (until HTTP 429), then OpenAlex. Standard web searches for the Bain abstract, Bitsch et al., Bianchi et al. and the BLS April-2026 CPI. Consensus was not used.
- **Scratch scripts** (session scratchpad, `g11v/scripts/`): `extract.py` (PDF text), `read_results.py` (result JSONs) and `mc_sens_check.py` (engine sensitivities against the §4.6 durations).

**Bottom line: the factual layer is strong.**
- **Flagged claims.** 16 of 18 are confirmed against primary documents, mostly to the digit; 2 are corrected; none are refuted or unverifiable.
  - **UK water (correction).** It is not true that "only two of 17 companies earned a positive return on regulated equity in 2024–25". Ofwat's primary report shows 7 of 17 reporting units with positive RoRE; only Severn Trent beat its base return, and the sector simple average was −2.32%. "Only SES below 60% gearing" is also wrong: Portsmouth was at 38.1%. The secondary source, The UK Water Report, is what got these wrong.
  - **Inflation correlations (correction).** The 0.4/0.3 inflation and Henry Hub correlations are computed on the **Cambridge Associates** index (net of fees), not MSCI. The 88%-above-CPI+400bp statistic covers 2010–2025, not 2005–2025.
- **Other claims.** All 17 are confirmed, apart from one minor wording point: US CPI of 3.8% in April 2026 was the highest since **May** 2023, not March 2023.
- **References.** All 10 academic references exist with correct year, title and venue. One author list is incomplete: P74 also has Luna Lu and Amanda Wee as authors. Several practitioner figures are attached to the wrong document (§3).
- **Internal consistency of reported numbers.** The §4.6, §4.4, §6.4 and §6.8 tables reproduce the result JSONs exactly. I re-derived the zero-premium row of "What you need to believe" by hand (5.2 / 3.7 / 1.6%) and the stream-06 break-even of 6.24%.

**The design and specification layer has three must-fix problems (§4):**
1. **The illustrative Monte Carlo engine does not do what the dossier says it does.**
   - Its cash flows have **no inflation indexation**: CFADS grows at a fixed nominal rate while coupons reprice with π^e.
   - Its inflation sensitivities are 2–16× smaller than the §4.6 structural results depending on segment, and the wrong sign for regulated assets. It has **no regulatory reset**.
   - **Inflation.** Once debt reprices, the engine's regulated and availability-PPP equity *loses* about 20% per +1pp of expected inflation. §4.6, finding 6 and §6.6 say it *gains* 13% and 23%.
   - **Real rates.** Regulated equity carries a real-rate sensitivity of about 12 (rising to 32 once all debt reprices), against 0.7–0.8 structurally.
   - The headline stress numbers (finding 7, the §6.8 cash map, the specification card's "Stress behaviour") come from this engine.
2. **The §2.4 linearised duration formula double-counts the refinancing channel.**
   - Its first term is already the Modigliani–Miller V^A − V^D sensitivity, so adding (1 − h_eff)V^D Ā/V^E counts the same effect twice.
   - The script behind §4.6 computes −Δln(V_A − V_D) with no add-on, so the §4.6 numbers are fine. An implementer coding §2.4 would not be.
3. **Actions are not gated by vehicle and control.**
   - Holdco recaps, opco up-sizing, sale-leasebacks and acquisition or development debt are listed as ADIC REFINANCE/LEVER instruments.
   - For closed-end and open-end fund interests (65% of the synthetic sleeve) and minority co-investments, these are GP or controlling-owner decisions, not ADIC actions.

**Overall reliability: medium.** The evidence base is high quality. Two IC-facing facts need correcting, and the engine behind the stress numbers contradicts the dossier's own structural analysis, so the design layer needs a revision pass before the Real Assets synthesis uses its stress figures, its per-segment inflation hedging or its action menu.

---

## 2. Claims

### 2.1 Flagged claims (18)

| # | Claim (as flagged) | Verdict | Corrected value / note | Source |
|---|---|---|---|---|
| 1 | Closed-end infrastructure funds, vintages 2002–2018: PME 0.93 vs S&P 500 (SD 0.31), mean net IRR 9.92%, GPME −0.257, procyclical cash flows, +10pp early exits ↔ +2.575pp IRR, public investors −1.81pp IRR | **Confirmed** | Table 3: PME 0.93 (median 0.95, SD 0.31, n = 157); IRR 9.92% (median 9.35%, n = 210); MOIC 1.34. Burgiss: PME 0.89, IRR 5.60% (median 7.94%). GPME −0.257 with a market loading "well above one". +10pp exits in the first 5 years → +0.085 PME, +2.575pp IRR, +0.079 MOIC. Public investors: "1.810 percentage points lower IRR". AUM $59bn (2008) → $486bn (2019). Every detail in dossier §4.1 matches | https://openaccess.city.ac.uk/id/eprint/33251/1/hhab048.pdf (open-access copy of https://academic.oup.com/rfs/article/34/8/3880/6239714) |
| 2 | EDHECinfra Q1-2021: 5y vol core 7.33%, contracted 8.13%, merchant 11.77%, airports 16.22%; max DD contracted 10.35%, merchant 21.60%, transport 22.41%, airports 34.89%; duration 7.40–11.63; airports 1y TR −19.79% | **Confirmed** | All values match Table 1 (local currency, as of Q1 2021). Two notes: (i) the executive summary's text says "7.6% to 11.6%", while the table runs 7.40 (wind) to 11.63 (airports); (ii) EDHEC's "Core" and "Core+" are expected-return quantile buckets, not fund-strategy labels. That matters where §6.8 uses "core DD 11.2%" as the REG anchor | https://www.edhecinfraprivateassets.com/wp-content/uploads/2021/05/P74_EDHEC-LTIIA_Volatility.pdf |
| 3 | Appraisal indices 2–3% vol (Sharpe > 3) vs 7–12% market-implied; leverage 77–78%, ≈90% for contracted renewables/social | **Confirmed** | "Appraisal-based indices typically report unrealistic total return volatility in the 2-3% range … (Sharpe ratio above 3)"; "7-12% range"; "average leverage is high but stable at 77-78%". Table 8 runs from 76.97% (Q1 2020) to 78.49% (Q1 2011). Leverage is defined as *senior* liabilities over total assets; renewables and social are at "c.90%". Tables 2–3 give appraisal NAV vol of 2.0 / 2.0 / 1.8% against 7.3 / 8.2 / 11.5% market-implied | same P74 PDF |
| 4 | 1pp discount-rate rise → about −10% fair value; 2020 NAV attribution: dividends −3.5%, rates > +5%, risk premia up to −9% | **Confirmed** | Quotes: "a 1% increase in the discount rate would reduce the fair value … by 10%"; dividends ≈ −3.5%; rates "more than +5%"; risk premia "as much as −9%". Three-year cumulative effect: rates +15% against < 1% for cash flows. The −9% is an upper bound (see R8). The airports point in §2.5 comes from P74 p.33, not this article, and is confirmed there | https://sponsored.bloomberg.com/article/edhec-infra/inflation-risk-how-exposed-are-investors-in-infrastructure |
| 5 | SIPA, 30 Nov 2025: infra300 median E[R] 11.31% (ERP 8.2%; 9.55% three years earlier); 3/5/10y returns 11.33/11.42/9.22%; data infrastructure 13.77% with 10y vol 18.37%; industry CMAs 7–11% | **Confirmed** | Table 4: 11.31% / 9.55% / 8.53% (now / 3y / 10y ago); ERP 8.2 / 7.0 / 6.6%, "up ~120-130bps". Table 3 gives the returns. Table 5 (as of 30 Sep 2025) gives data infrastructure at 13.77% and 18.37%. Industry ranges: returns 7–11%, volatility 10–19%; BlackRock uses 20% for infra. SIPA adds: "Industry CMAs are generally provided net of fees" (see R6) | https://publishing.sipametrics.com/papers/20260115_capital_market_assumptions.pdf |
| 6 | SIPA infra300, May-2026 factsheet: 10y vol 8.92%, 10y max DD −11.04%; 2020 −1.85%, 2022 +8.14%, 2025 +7.92%; cash return ≈10.6% | **Confirmed** | The "LATEST" URL still serves the May-2026 edition. Dividend yield 10.57%. The 3/5/10y returns (10.12 / 11.29 / 8.72%) and the infra100 Core and infraGreen rows also match. TICCS business-risk weights for infra300 are 49 / 24 / 27% (contracted / merchant / regulated), confirmed because each column sums to 100. Archive the file: the URL will roll forward | https://publishing.sipametrics.com/factsheets/indices/LATEST_infraMetrics_equity_market_indices_factsheet.pdf |
| 7 | MSCI Global Private Infrastructure Asset Index: 12.2% gross over the year to Q1 2026 (943 assets, $412bn); 11.7% annualized since June 2008; one negative quarter since the GFC | **Confirmed (citation fix)** | The Q1-2026 page (10 Jun 2026) confirms 12.2%, 943 assets and $412bn. The 11.7% "since June 2008" and "only one quarter of negative returns since the 2008 global financial crisis" come from MSCI's Quick Take of 20 Nov 2025 (data to mid-2025), not from the Q1-2026 page. The page does not say "gross"; the label is acceptable for an asset-level index, and CBRE describes it as "gross of fees" | https://www.msci.com/data-and-analytics/private-asset-solutions/global-private-infrastructure-asset-index-q1-2026-results ; https://www.msci.com/research-and-insights/quick-take/the-new-drivers-of-infrastructure-performance |
| 8 | Cambridge Associates, net, 1 year to Q1 2026: core/core-plus 10.4% vs value-add 7.9% | **Confirmed** | CBRE IM Q3 2026 (13 Oct 2026). Note: §4.2's universe description (80 core/core+ funds, $242bn; 92 value-add funds, $307bn) comes from CBRE IM Q4 2025, is **as of Q2 2025**, and is "market capitalization" | https://www.cbreim.com/insights/articles/infrastructure-quarterly-q3-2026 |
| 9 | Preqin, funds launched 2010–2020, median net IRR (SD): core 12% (10%), core-plus 10% (13%), value-add 12% (15%), opportunistic 8% (15%), debt 8% (7%) | **Confirmed** | Exact match ("Source: Preqin (2024b)"). GI Hub's own reading: "higher risk strategies do not necessarily provide higher returns" | https://cdn.gihub.org/umbraco/media/5551/section-2_infrastructure-funds_monitor-2024.pdf |
| 10 | Infrastructure LP pricing 91% of NAV in H1 2026 (all strategies 87%); chart series ≈82% (2020) and ≈83% (2022); real assets 15% of GP-led volume in H1 2026 | **Confirmed** | Text: "Infrastructure pricing remained robust in H1 2026 at 91% of NAV"; all strategies ≈87%. **Chart mapping cross-checked.** Splitting the 41 chart labels into series reproduces every H1-2026 and YE-2025 value the text states (all 87/87, venture 78→79, real estate 68, credit 91→89, infra 91). That gives infrastructure 82 / 93 / 83 / 87 / 90 / 90 / 91 for 2020 to H1 2026. Fig. 9: real assets 15% of GP-led volume in H1 2026 (13% in 2025); average LP rollover 14%. The "single-digit discounts" and "> $1bn … 100% infrastructure" statements are both confirmed. Caveat: 82–83% are annual averages, not stress troughs | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 11 | Stonepeak-Plus FY2025 10-K: quarterly redemptions up to 5% of units, pro rata, no automatic carry-over, 5% deduction under two years, GP may suspend, leverage limit 30% | **Confirmed** | Details: (i) the 5% is "either by number of Units or aggregate transactional NAV" at the prior quarter-end, and the GP may redeem above the cap; (ii) suspension or material modification needs Independent Directors' approval; (iii) the Fund "typically seeks" to stay within 30% leverage, a target that may be exceeded; (iv) 80–85% of NAV in infrastructure investments and 15–20% in debt and other securities; (v) monthly subscriptions | https://www.sec.gov/Archives/edgar/data/0002045458/000204545826000012/sp-20251231.htm |
| 12 | Project-finance bank loans 1983–2018 (8,583 projects): ultimate recovery 77.9% (Basel), mode 100% (58.1%); 2020 vulnerable and resilient sectors | **Confirmed (context missing)** | 8,583 projects, 67.1% of global PF originations. Recovery 77.9% (Basel) and 75.8% (Moody's definition); 100% in 58.1% of cases; recoveries independent of the default cycle. March–May 2020: 66 corporates defaulted against two infra/PF issuers. Most vulnerable: unregulated utilities and power, ports, privately managed airports and toll roads. Most resilient: regulated utilities and availability PPPs. **Omitted:** 77.9% is the *workout* recovery; distressed-sale exits averaged 49.5% (Basel) and 47.5% (Moody's) (see R7) | https://ma.moodys.com/rs/961-KCJ-308/images/Default%20Reports%20-%20Infrastructure-Project-Finance-Global%20-%2010Jun20.pdf |
| 13 | Ofwat MFR 2024–25: notional gearing cut to 55% for AMP8; eight companies above the 70% concern level; only two of 17 earned a positive RoRE in 2024–25 | **Corrected** | **55%** (from 60%) and **8 above 70%** are correct (TMS, AFW, SRN, SEW, NES, WSX, ANH, YKY). **Positive RoRE: 7 of 17 reporting units, not 2.** Ofwat: "Only Seve[r]n Trent reported a RoRE above its base return. Six companies reported a positive RoRE but below their base return. All other companies reported a negative RoRE." Values: SVE 8.96%, PRT 4.15%, YKY 2.52%, Bristol region 1.82%, UUW 1.05%, WSX 0.54%, AFW 0.44%; the other 10 were negative. Sector simple average −2.32% (range −12.64% to +8.97%); AMP7 average 1.71% against a 4.10% base. **Below 60% gearing: Portsmouth (38.1%) and SES (59.8%)**, not "only SES" as §4.5 says | https://www.ofwat.gov.uk/wp-content/uploads/2025/11/The-Monitoring-Financial-Resilience-Report_2024-25.pdf (primary; the dossier cites https://www.thewaterreport.co.uk/single-post/financial-resilience-and-positive-returns-lacking) |
| 14 | Transport forecasts (210 projects): rail overestimated by 105.6% (9 of 10); for 183 roads, half miss by more than ±20%; actual traffic averaged 9.5% above forecast (SD 44.3%) | **Confirmed** | 27 rail and 183 road projects, 14 nations, $59bn. Rail is overestimated in "more than 9 out of 10" projects, by an average of 105.6% (95% CI 66.0–169.9). Roads: 50% miss by more than ±20% and 25% by more than ±40%; actual traffic is 9.5% above forecast (sd = 44.3). "the present data do not allow" a toll/non-toll split. No improvement over 30 years | https://arxiv.org/abs/1303.6654 (JAPA 71(2)) |
| 15 | Privately financed toll-road forecasts (> 100 projects) show large errors and considerable optimism bias | **Confirmed** | The abstract says "over 100 international, privately financed toll road projects … large errors and considerable optimism bias". The year-1 statistics usually quoted (mean 0.77, SD 0.26, n = 104) trace to the S&P study (Bain & Polakovic 2005), not this abstract. The paraphrase "financing should absorb large deviations" was not checked (paywalled) | https://doi.org/10.1007/s11116-009-9199-7 (via Crossref/OpenAlex and abstract search) |
| 16 | Private infrastructure (MSCI) rolling 1y returns correlate 0.4 with US inflation and 0.3 with Henry Hub (2005–2025) and beat CPI + 400bp 88% of the time; air traffic −3.4% y/y in April 2026 because of the Middle East conflict; US inflation 3.8% in April 2026 | **Corrected** | **Index:** the correlations use the "Cambridge Associates Private Infrastructure Index, in USD, net of fees" (Figure 2 caption), not MSCI, with data from Q1 2005 to Q4 2025. **88%:** this is for **Q1 2010–Q4 2025**, per "CBRE IM analysis", with no index named. Air traffic −3.4% "driven primarily by the Middle East conflict" is confirmed. US CPI of 3.8% in April 2026 is confirmed by BLS. Dossier §4.3's "highest since March 2023" (CBRE's wording) should read **May 2023 (4.0%)** | https://www.cbreim.com/insights/articles/infrastructure-quarterly-q2-2026 ; https://www.bls.gov/news.release/archives/cpi_05122026.htm |
| 17 | MSCI 3y annualized returns to Q2 2025: power generation 14.3, digital 12.1, T&D 12.1, airports 11.7, transport 10.8, renewables 7.9%; renewables about two-thirds of sector-specific fundraising, Q1–Q3 2025 | **Confirmed** | Figure 2: MSCI expanded index, gross, fixed USD, as of Q2 2025. "renewables represented the largest share at about two-thirds of capital allocations" (Infrastructure Investor, closed-end funds). The dossier's adjacent "one year to Q4 2025: power generation 23%, utilities 15%" is from CBRE IM **Q2 2026** (confirmed there) | https://mediaassets.cbre.com/-/media/project/cbre/bussectors/cbreim/insights/articles/2025/december/infrastructure-quarterly-q4-2025/infrastructure-quarterly-q4-2025.pdf |
| 18 | Short run: only direct infrastructure is a partial inflation hedge; all series co-move with inflation in the long run (US, 1991–2013) | **Confirmed** | Structured abstract: US, 1991–2013; Fama–Schwert, Engle–Granger cointegration and Granger causality. Direct infrastructure has the "most favorable inflation protection". The limitation (a single composite direct-infrastructure index) supports dossier §8.3 | https://www.emerald.com/insight/content/doi/10.1108/JPIF-04-2014-0026/full/html |

**Tally:** 18 checked; 16 confirmed, 2 corrected, 0 refuted, 0 unverifiable.

### 2.2 Other claims checked (17)

| Claim (dossier location) | Verdict | Note | Source |
|---|---|---|---|
| Expected returns: low double digits before 2008 → ≈6% at end-2016 → 7–8% after 2017 (§2.3) | Confirmed | P74 p.7 | P74 PDF |
| Cash-flow and discount-rate channels similar over 20 years; rates and risk premia dominate the last 5 years (§2.3) | Confirmed | P74 pp.6–7 ("at least as much"; "past five years") | P74 PDF |
| Airports' long lives limit the value impact of 2020–23 dividend losses (§2.5) | Confirmed | P74 p.33 | P74 PDF |
| Gupta & Van Nieuwerburgh: −6¢ per $, replicable with listed infrastructure, Treasuries and the stock market (§4.1) | Confirmed | As cited in Andonov et al. p.3883 | Andonov OA PDF |
| Bitsch et al.: 363 infrastructure and 11,223 other deals, 1971–2009, CEPRES; telecom- and VC-heavy per a critic (§4.1) | Confirmed | Telecom 58.7%, VC 52.9% | https://www.infrainsightblog.com/analysis-of-infrastructure-investments-produces-surprising-findings |
| Blanc-Brude & Tran: six factors; 2008–2015 price-regime shift; roads cyclical; renewables at higher P/S (§4.1) | Confirmed | Executive summary pp.5–6 | https://www.edhecinfraprivateassets.com/wp-content/uploads/2019/01/blanc-brude_and_tran_2019.pdf |
| Bianchi et al.: 1927–2010 factor-mapped listed infrastructure; tail risk comparable to US equities; mean-variance and mean-CVaR benefits (§4.1) | Confirmed | Abstract via bibliographic mirrors | https://ideas.repec.org/a/eee/jbfina/v42y2014icp314-325.html |
| Airports and transport fell from 47% (2008–19) to 26% (2020–25) of MSCI index value (§4.2) | Confirmed | "2020 to mid-2025" | MSCI Quick Take |
| Preqin: $216.1bn in 2025 ($135.5bn in 2024); Q1 2026: 27 funds, $25bn; Q2: 8 funds, $4.4bn; H1 interim closes $57bn ($69bn); 731 funds seeking $463bn; vintage-2022 quartiles 21.1 / 11.8 / 5.3% (§4.2–4.3) | Confirmed | Preqin does not label the $216.1bn as "final closes", as the dossier's table does | https://www.preqin.com/insights/research/blogs/unlisted-infrastructure-in-2026-and-why-selectivity-matters |
| CBRE Q3 2026: ≈$190bn of interim closes YTD; allocations > 6% (5% in 2023); secondaries 2% of AUM (PE 5%) and > $10bn raised; deals > $800bn; renewables > 40% of deal count; greenfield doubled, half of it data centres; NOI yield on cost 9–12%; July air traffic +0.2% after three months of decline (§4.3–4.4) | Confirmed | Digital's 28% is described as "market share", not share of deal activity | CBRE Q3 2026 |
| CBRE Q4 2025: $960bn (+22% y/y) to Q3 2025; AGS £1.5bn ≈ 23× EV/EBITDA; IEA 2030 renewables −248 GW, with the US the largest cut (§4.3) | Confirmed | | CBRE Q4 2025 PDF |
| CBRE Q2 2026: hyperscaler capex ≈ $730bn in 2026; 1y to Q4 2025 power generation 23%, utilities 15% (§4.2–4.3) | Confirmed | | CBRE Q2 2026 |
| SIPA infra300 TICCS weights 49% contracted / 24% merchant / 27% regulated (§4.2, "probable chart mapping") | Confirmed | Each column sums to 100 | SIPA factsheet |
| infra300 +3.76% year to date to May 2026 (§4.2) | Confirmed | Factsheet YTD column: 3.76% | SIPA factsheet |
| US CPI 3.8% in April 2026, "the highest since March 2023" (§4.3) | Confirmed / wording corrected | BLS: 3.8% (3.3% in March). The last higher reading was May 2023 (4.0%) | BLS archive |
| The UK Water Report's account of Ofwat (§4.5) | Secondary source in error | See claim 13 | Ofwat primary |
| Internal: the §4.6, §4.4, §6.4 and §6.8 tables against the result JSONs; the "what you need to believe" ℓ = 0 row; the 6.2% stream-06 break-even | Confirmed | Exact matches; ℓ = 0 re-derived as 5.2 / 3.7 / 1.6%; g\* = 6.24% | `G11_calcs/*_results.json` |

---

## 3. Citation check

### 3.1 Academic references

| Reference (dossier §10) | Exists | Authors | Year | Title | Venue / pages | Checked via |
|---|---|---|---|---|---|---|
| Andonov, Kräussl & Rauh | Yes | Correct | 2021 | Correct | *RFS* 34(8), 3880–3934 | Crossref; full text |
| Bain | Yes | Correct (Robert Bain) | 2009 | Correct | *Transportation* 36(5), 469–482 | Crossref, OpenAlex |
| Bianchi, Bornholt, Drew & Howard | Yes | Correct | 2014 | Correct | *JBF* 42, 314–325 | OpenAlex |
| Bitsch, Buchner & Kaserer | Yes | Correct | 2010 | Correct | *EIB Papers* 15(1), 106–136 | EIB issue listing / TUM record (search) |
| Blanc-Brude & Tran | Yes | Correct (Frédéric Blanc-Brude, Christy Tran) | Jan 2019 | Correct | EDHEC Infrastructure Institute-Singapore | PDF title page |
| Blanc-Brude & Gupta | Yes | **Incomplete:** Blanc-Brude, Gupta, **Luna Lu, Amanda Wee** | May 2021 | Correct | EDHEC Infrastructure Institute-Singapore, with LTIIA support | PDF "About the Authors" |
| Flyvbjerg, Skamris Holm & Buhl | Yes | Correct | 2005 | Correct | *JAPA* 71(2), 131–146 | Crossref; arXiv text |
| Gupta & Van Nieuwerburgh | Yes | Correct | 2021 | Correct | *JF* 76(6), 3255–3307 | Crossref |
| Rödel & Rothballer | Yes | Correct | 2012 | Correct ("…Fact or Fantasy?") | *JAI* 15(1), 110–123 | Crossref |
| Wurstbauer & Schäfers | Yes | Correct | 2015 | Correct | *JPIF* 33(1), 19–44 | Emerald |

### 3.2 Industry documents

All 15 exist, with titles and dates matching the dossier unless noted below:
- SIPA CMA (Jan 2026) and factsheet (May 2026);
- Moody's (10 Jun 2020), whose full title is "*…Defaults & recoveries: Fewer coronavirus-driven downgrades than nonfinancial corporates*";
- Jefferies (Jul 2026);
- the Stonepeak-Plus 10-K (FY2025);
- GI Hub (2024);
- The UK Water Report (9 Nov 2025);
- CBRE IM Q2 2026 (25 Jun 2026) and Q3 2026 (13 Oct 2026);
- MSCI Q1-2026 results (10 Jun 2026) and Quick Take (20 Nov 2025, Niel Harmse);
- Preqin (9 Sep 2026);
- EDHECinfra/Bloomberg (28 Apr 2021), which is sponsored content written by EDHECinfra.

### 3.3 Citation problems

1. **MSCI.** The 11.7% since June 2008 and "one negative quarter since the GFC" come from the Nov-2025 Quick Take (data to mid-2025), not the Q1-2026 results page given as the source.
2. **CBRE IM Q2 2026.** The 0.4/0.3 correlations are on the Cambridge Associates index (net of fees), not MSCI. The 88% CPI + 400bp statistic covers Q1 2010–Q4 2025.
3. **Cambridge Associates universe.** The 80 core/core+ funds ($242bn) and 92 value-add funds ($307bn), as "market capitalization", are from CBRE IM Q4 2025 as of Q2 2025, not from the Q1-2026 data they sit beside.
4. **Blanc-Brude & Gupta (2021).** Two co-authors are missing: Luna Lu and Amanda Wee.
5. **"One year to Q4 2025: power generation 23%, utilities 15%".** This sits under the CBRE IM Q4 2025 tag but comes from CBRE IM Q2 2026.
6. **UK water.** The facts are cited through The UK Water Report, which misstates Ofwat's primary report on positive RoRE and on sub-60% gearing. Cite Ofwat's *Monitoring Financial Resilience Report 2024-25* directly.
7. **CBRE IM Q4 2025 date.** §10 dates it "Nov 2025"; the asset path (`…/2025/december/…`) and the file metadata (3 Dec 2025) indicate December 2025.
8. **US CPI.** "Highest since March 2023" repeats CBRE's wording; the last higher reading was May 2023 (4.0%).
9. **Bain (2009) reference class.** The §6.7 prior (mean 0.80, SD 0.30) is not a statistic in the 2009 abstract. The commonly cited year-1 figures (mean 0.77, SD 0.26, n = 104) come from the S&P study (Bain & Polakovic 2005). Tag the prior [I] and say what informs it.
10. **SIPA factsheet URL.** It is a "LATEST" link and will roll forward. Archive the May-2026 file used.

---

## 4. Reasoning issues: design implications and specification card

Severity shows how far each issue could mislead the IC or the build: **High** (must fix before synthesis), **Medium**, **Low**.

**R1 [High]. The illustrative engine (`g11_infra_mc.py`) does not implement the inflation, reset and smoothing mechanics the dossier attributes to it.**

It produces finding 7, finding 8, the §6.8 calibration and cash map, and the specification card's "Stress behaviour". Five gaps:
- **(a) No inflation indexation in cash flows.** CFADS = DS0 × G_t × DSCR0 × e^{OL·s_rev}. G_t grows at a fixed nominal `GPLAN`, and s_rev contains only GDP news, jumps and power prices. The §6.3(1) revenue term θ_k π_{t−L_k} is not implemented. Coupons, by contrast, reprice with i_t = r_t + π^e_t + s.
  - **Effect.** Inflation raises debt service with no revenue offset, so indexed assets are *short* inflation in the engine.
  - **Numbers.** From `mc_sens_check.py`: with all debt repriced, a +1pp π^e move costs REG equity ≈20.0% and CON_IDX ≈19.2%. §4.6 has them *gaining* 13.2% and 23.1%.
- **(b) θ^E is far too small.** The value equation uses −D_k(1 − θ^E_k)Δπ^e with θ^E = 1.3 / 1.3 / 0.1 / 0.0 / 0.2 / 0.4 for REG / CON_IDX / CON_FIX / TOW / DC / MID.
  - Including the engine's coupon channel, the instantaneous sensitivities are +0.1 / −1.4 / +7.9 / +11.4 / +11.9 / +5.1. The structural §4.6 values are −13.2 / −23.1 / +26.7 / +23.3 / +23.3 / +14.5.
  - Reproducing §4.6 at the stated D_k would need θ^E ≈ 2.5 / 4.0 / −2.6 / −1.3 / −1.1 / −0.9.
- **(c) No regulatory reset.** §6.3(1) resets ω to r_t + ERP^reg + η, and finding 5 and §4.6 give regulated equity a real-rate duration of 0.7–0.8. The engine has no reset and no ψ: REG carries D = 9 plus coupon repricing, ≈11.8 instantaneously and ≈31.7 once all debt reprices.
- **(d) One smoothing parameter for every segment.** λ^app = 0.85 applies everywhere, although §3 lists "one smoothing λ^app for core and value-add" among *rejected* approaches and §6.3(5) and §6.10 specify 0.70 for value-add.
- **(e) Two smaller mismatches.**
  - Closed-end calls are a flat 25% a year × a regime factor, not the 20/25/30/35%-by-age schedule in §6.3(6) and §6.10.
  - The code adds a power-price value term (0.35·m_k·Δx^p) that is not in §6.3(4).

**Consequence.** §6.6's statement that "inflation-hedge value enters only through scenario P&L via structural θ^E_k (§4.6)" does not describe the engine, and finding 6 and finding 7 cannot both be read off one model.
- **Sleeve level.** Year-1 sleeve numbers may move only modestly: the long and short inflation legs offset, and π^e starts close to the G mean.
- **Segment level.** Lock-ups, distributions in the I/G states and per-holding SELL/HOLD inputs are mis-specified.
- **Fix.** Index CFADS through θ_k (and the RAB), implement the reset, take the inflation and real-rate loadings from the structural archetypes (or value structurally at decision dates, as §7 already proposes), and use segment-specific λ^app. Until then, label the stress numbers as coming from a reduced-form engine without pass-through or resets.

**R2 [Medium]. The §2.4 real-rate duration formula double-counts the refinancing channel.**
- **The double count.** The first term, [(1 − ψ)D_A V^A − h D_D V^D]/V^E, is the Modigliani–Miller sensitivity of V^E = V^A − V^D. In it, floating and refinanced debt priced at market (≈ par) already passes the full rate effect to equity. The extra term (1 − h_eff)V^D Ā/V^E counts the same effect a second time: about +1.5·Ā years for a 60%-geared holdco.
- **What the code does.** `g11_durations.py` computes D_real_P = −Δln(V_A − V_D) with no add-on, so the §4.6 numbers are internally sound. An engineer implementing §2.4 literally would overstate holdco real-rate durations.
- **Where the add-on belongs.** It is valid only in the equity-cash-flow-fixed frame used by §6.3(4), where D_k is the cash-flow-fixed equity duration.
- **The two formulas disagree.** The inflation formula in §2.4 leaves out coupon repricing, while the real-rate formula includes it.
- **Consequence 4 is mis-framed.** The "concealed short in long real rates" is, in the MM computation, mostly leverage applied to a long asset duration (D_A·V^A/V^E). Fixed-rate debt offsets it less as the locked tenor shortens; it is not an additional channel.
- **Fix.** Write §2.4 in one frame. Either use pure MM with no refinancing add-on, or use the ECF-fixed D^E plus the refinancing term.

**R3 [Medium]. Actions are not gated by vehicle or control.**
- **The problem.** §6.4 and §6.10 list holdco recaps, opco refinancing or up-sizing, sale-leasebacks and ground leases, acquisition debt and development debt as ADIC REFINANCE/LEVER instruments.
  - **Fund interests.** For CEF and OEF interests (40% + 25% = 65% of the synthetic sleeve), these are GP decisions.
  - **Minority co-investments.** They need the sponsor's and co-investors' consent.
  - **What ADIC can actually do there.** SELL (secondary, redemption queue, CV election) and HOLD; REFINANCE only through fund-interest NAV facilities, which the dossier assigns to Corporate Finance, or through financing at ADIC's own holding vehicle.
- **The gap.** The specification card captures `governance_rights` and `consent_flags` but has no rule that uses them.
- **Fix.** Add an admissibility matrix by `vehicle` × control (board or reserved-matter rights) and test it, as is already done for "no non-consented transfers".

**R4 [Medium-low]. The stress narrative does not match the simulation.**
- **The claim.** The specification card attributes "sleeve Y1 P05 −11 to −12% economic" to "real rates +0.6–1.0pp, π^e +1.0–1.5pp, ERP +0.2–0.4pp".
- **What the engine does.** Those figures are differences between regime means (G or I against N). The "today" run starts at r = 2.3%, π^e = 3.5% and the G ERP mean, so the expected year-1 factor moves are small. The P05 comes from regime switching and volatility.
- **Deterministic check.** Applying the stated moves through the engine's own loadings (sleeve W·D = 8.94, W·D(1 − θ^E) = 3.38, W·D·β^q = 9.12) gives about −10.6% to −17.7% before coupon effects. The match at the low end is a coincidence, not validation.
- **Fix.** Report a deterministic scenario loss and a simulated percentile separately.

**R5 [Low-medium]. Intra-ADIC netting covers SELL only.**
- Sales to the Secondaries group correctly raise zero.
- Holdco preferred or structured equity, or NAV loans, *supplied* by ADIC's Capital Solutions or Private Credit groups also raise zero group-level liquidity. The dossier treats Capital Solutions only as a "quote".
- **Fix.** Extend the V2 netting test to REFINANCE.

**R6 [Low-medium]. The "≈4pp model range" mixes bases.**
- J.P. Morgan's 7.1% is a core infrastructure CMA. SIPA notes that industry CMAs are "generally provided net of fees".
- SIPA's 11.3% is a gross, mark-to-model expected return on market-implied prices for a broad (not core) index.
- Fees (≈1–2pp) and core-versus-broad composition explain part of the 4pp.
- **Fix.** Put both on one basis before presenting the range to the IC (finding 3, §6.7).

**R7 [Low]. The recovery anchor is the workout figure.**
- Moody's 77.9% is the *workout* ultimate recovery; distressed-sale exits averaged 49.5% (Basel) and 47.5% (Moody's).
- If the engine sends refinancing failures to sales (§7 pitfall 2, "default and recovery"), 77.9% overstates recoveries.

**R8 [Low]. The 2020 risk-premium target is an upper bound.**
- In the source, "risk premia −9%" is "as much as −9%".
- §6.9 uses it as a calibration target, and the engine's C-regime ERP shock (+1pp, "EDHECinfra attribution") is calibrated to it.
- P74 Table 7 shows −3.9% for the broad market over the year to Q1 2021 (−13.7% for airports, −8.2% over three years).
- **Fix.** Calibrate the average and the tail separately.

**R9 [Low]. Finding 8 overstates the persistence of operating yield.**
- It says "operating yield (4.3–4.7%) persists", which omits the demand-bust value: operating cash falls 23% to $0.24bn, 3.3% of NAV.
- §6.8 correctly says 3.3–4.7%.

**R10 [Low]. The synthetic defaults break the proposed limits.**
- DC's fixed/hedged share is h = 0.60, against the §6.5 floor of 75% for refinanced holdcos.
- The default chance constraint (P(equity wipe-out within 3 years) ≤ 2%) cannot be evaluated, because the engine has no V^E floor or default state.

**R11 [Low]. Floating coupons key off the wrong rate.**
- §6.3(3) prices the floating share at i_t = r_t + π^e_t + s, with r_t the 10-year real rate.
- Floating debt resets on short rates: today SOFR is 3.89% against a 10-year UST of 5.09%. The floating channel is mis-specified whenever the curve is not flat.
- **Fix.** Use the short rate for (1 − h) and the forward curve for refinancing.

**R12 [Low]. The LEVER bound and the SELL/HOLD comparison.**
- **The bound.** "Financing ≲ α\* − λ_R m − λ_Lev ≈ S+190bp" follows from LEVER = ADD + REFI. That identity charges a borrowed dollar the hurdle r_h (5.9% ≈ SOFR + 200bp) plus the spread.
- **Exact break-even.** The script also deducts the covenant charge (0.2%) and the fee (0.2% a year), so it is ≈S+150bp. The qualitative result, never LEVER at α\* = 2.6% and S+300, stands.
- **SELL against HOLD.** The region map compares bid × NAV with LAPV(HOLD) per $ of the same NAV. It therefore ignores the gap between reported N and economic V^E that §6.3(5) creates. With a stale N in a downturn, the true boundary shifts toward SELL.

**R13 [Low]. "So risk has not paid" over-reads the evidence.**
- Finding 3 draws this from Preqin medians for small, immature 2010–2020 vintages, which §8.1 itself warns about. Soften it to "has not been rewarded in median outcomes to date".

**On the UK water correction (claim 13).** The lesson survives and is stronger: the sector average RoRE was −2.32% in 2024–25 and only Severn Trent beat its base return. Update the numbers in finding 9, §4.5, the §5 case table and the §6.9 calibration target ("> 70% at 8 of 16 companies reporting gearing"; "positive RoRE at 7 of 17 reporting units, 1 above base").

---

## 5. Overall reliability

**Medium** for the dossier as an IC input. The rating is:
- **High for the empirical evidence:** 16 of 18 flagged claims and all 17 further claims confirmed, mostly to the digit, and every academic reference real.
- **Lowered** by two IC-facing factual corrections (UK water RoRE; the index and period behind the inflation correlations).
- **Lowered further** by design-layer problems that would propagate into the synthesis:
  - the stress engine contradicts the dossier's own structural inflation and rate sensitivities (R1);
  - the §2.4 duration formula double-counts (R2);
  - the action menu includes instruments ADIC cannot use as an LP or minority co-investor (R3).

All are fixable without new research. The architecture is sound and evidence-based: asset-level archetypes, economic against reported NAV, DSCR lock-ups, the open-end queue machine, partial sell-downs classified as SELL, and no generic inflation-hedge credit.
