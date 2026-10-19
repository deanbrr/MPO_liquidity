# G10 Real Assets, real estate: verification log

*Adversarial fact-check of `research/groups/dossiers/G10_ra_real_estate.md`, prepared 2026-10-18. I did not edit the dossier.*

## 1. Summary

**What I checked.**
- **Claims.** 32 empirical claims in total. That covers all 20 flagged claims (some split into parts) and 10 more that I judged load-bearing or suspicious (§2).
- **References.** 22 references in detail, plus the industry sources at document level (§3).
- **Design layer.** The design implications (§6.1–6.10) and the specification card (§6.11), checked for formula, sign, calibration and action-availability errors (§4).
- **Calculation scripts.**
  - I read `g10_public_and_arith.py` and `g10_re_engine.py` in full, and used the stored results JSON and stdout.
  - I re-ran the public-data timing and desmoothing calculations from a scratch script, on inputs I pulled myself.
  - Nothing in the project was written except this log.

**Method.**
- **Primary PDFs.** I downloaded each one, extracted the text layer with pypdf, and grepped every number in context. The files:
  - NCREIF: the NFI-ODCE 2Q26 release, the 2Q26 webinar slides and the ODCE attribution slides (16 Sep 2026);
  - Arnold, Ling & Naranjo (2021);
  - Jefferies *Global Secondary Market Review* (Jul-2026);
  - MSCI: *Private Capital Benchmarks* Q2-2026, RCA *Capital Trends* (Feb-2026), RCA CPPI (May-2026) and *Real Assets in Focus 2026*;
  - Glancy, FEDS 2026-025;
  - the RCLCO Q2-2026 summary.
- **Nareit.** I parsed both Nareit monthly files (`MonthlyReturns.xls` and `MonthlyHistoricalReturns.xls`) with xlrd in a throwaway uv environment, not the project venv. From them I recomputed the calendar-year returns and drawdowns.
- **Treasury yields.** Daily DGS10 from the FRED CSV.
- **Web pages (WebFetch).** Callan, Accordant, MSCI blogs, Yieldpro, Scotsman Guide, MBA NewsLink, Propmodo, the Fed's FEDS page, the NY Fed SR 1130 page, Business Today, The National, Daily News Egypt, Arab News, NBER, NBIM, MPRA, Green Street and RCLCO.
- **Standard web searches.** Used for the Fed decision, ADIA's ranges, the Reuters Dubai polls, the NPI release, Trepp and MBA.
- **Metadata.** From Crossref and OpenAlex. Both rate-limited part-way, and I retried. Consensus was not used.

**Bottom line: the factual layer is very strong.**
- **Overall tally.** Of 32 claims, 26 are confirmed, 4 are corrected (all minor) and 2 are unverifiable. None is refuted.
- **Flagged claims.** Every flagged market statistic matches its primary source to the digit:
  - NCREIF, Nareit, RCA, Callan and Accordant;
  - the Jefferies 68%, the MSCI benchmarks and MBA;
  - Trepp, The National and NBER.
- **Corrections.** All four are minor:
  - the 10-year "5.36% on 7 Oct" (the H.15 close was 5.28%; the peak close was 5.31% on 5 Oct);
  - "Hormuz closed" (the source says "severely disrupted");
  - "≈90bp higher than in Q2" (≈68bp on 15 Oct);
  - the 2024–25 range for same-store NOI growth (2024–25 values ran up to +0.91%; +0.49% is the 2026Q1 print).
- **Public-data calculation.** Replicated exactly: ODCE −18.8%, relevered REITs −25.7%, Geltner α of 0.5–0.6, the lead–lag correlations and the stale gap series.
- **References.** One citation is wrong: the Fisher & Hartzell DOI resolves to the special issue's editors' introduction. Two links have degraded (TradeArabia; mba.org returns 403). Everything else checks out.

**The design layer has five must-fix problems (§4.1–4.5):**
1. The starting stale gap G₀ of 5–8% is presented as a consequence of today's market, but the dossier's own evidence contradicts it.
2. The look-through LTV, maturity and hedging constraints bind mostly on fund-held debt that ADIC cannot manage as an LP.
3. The extension probabilities misread Glancy (2026).
4. The open-end queue gate V-RE2 is circular, and "today's ≈8% queue" is a model output.
5. The fund-interest SELL threshold is contradicted by its own arithmetic and omits the release of unfunded commitments.

## 2. Claims table

| # | Claim (as in dossier) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | NFI-ODCE Q2-2026: 25 funds, $223.7bn net assets; leverage 27.1% vs 22.4% average since 2000 (range 15–34%); year-to-June contributions $10.4bn vs distributions and redemptions $19.1bn (net −$8.7bn); gross TR 1.49% (income 1.02%, appreciation 0.47%); 4.45% for the year | Confirmed | Verbatim in the release, which says "$223.7 billion of net real estate assets" ($280.4bn gross). $19.1bn = 8.5% of NAV, as the dossier says | https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf |
| 2 | NFI-ODCE preliminary Q3-2026 1.71% (income 1.02%, appreciation 0.69%); NPI Q2-2026 1.29% (1.17% / 0.12%) on 13,160 properties worth $943bn | Confirmed | Index page verbatim. The property count and value come from the NPI release, seen via a search summary only. The webinar summary rounds capital return to +0.11% | https://ncreif.org/indices/index-returns/ ; https://ncreif.org/__static/jdj5jdewjhnou3vmywrsudbrsghqcmjx/NPI-Press-Release-2Q2026(2).pdf |
| 3 | FTSE Nareit All Equity REITs total return (TR): 2022 −24.95%, Aug-2026 −2.71%, Sep-2026 −5.73% (−8.3% from the July peak); month-end drawdowns GFC −68.3%, 2022–23 −31.4%; also 2023 +11.36%, 2024 +4.92%, 2025 +2.27%, 2026 YTD +7.93%, COVID −24.4%, dividend yield 3.93% vs 2.59% | Confirmed | Recomputed to the digit from Nareit's files. GFC runs Jan-07 → Feb-09; 2022–23 runs Dec-21 → Oct-23 (quarterly −29.2%, Q4-21 → Q3-23) | https://www.reit.com/data-research/reit-indexes/monthly-index-values-returns |
| 4 | NPI Q2-2026: same-store NOI growth 0.78% (rolling 4Q), market-value-weighted occupancy 92.2%, appraisal cap rate ≈4.4%; sold properties clear within ±4% of marks; JLL bid/credit intensity 105/117; ODCE industrial market-to-contract gap 15–36% | Confirmed | All on the slides (pp. 8, 11, 16, 18, 29, 45) | https://ncreif.org/__static/jdj5jdewjfhaei55n3y0ehq3dxyyqvpj/NCREIF-Indices-Review-Webinar-Slides-2Q-2026.pdf |
| 5 | Same-store NOI growth "between −0.33% and +0.49% through 2024–25" (§4.4) | Corrected | The 2024–25 range is −0.33% to +0.91% (2024Q1 0.91%, Q2 0.75%, Q3 0.65%). +0.49% is the 2026Q1 print | same slides, p. 11 |
| 6 | MSCI RCA trailing-12-month cap rates, Feb-2026: apartment 5.6%, industrial 6.4%, data centre 6.8%, retail 6.9%, senior housing 7.1%, CBD office 7.3%, suburban office 7.5%, hotel 8.3%; volume $556bn (+21%) | Confirmed | Verbatim | https://www.msci.com/downloads/web/msci-com/data-and-analytics/real-estate/us-rca-capital-trends-report/2603-usct-bigpic-rca-msci-pg1.pdf |
| 7 | ODCE gross quarterly returns (1Q22–2Q26 as printed) imply −18.8% peak to trough (Q3-22 → Q2-24) and a 3-quarter trough lag vs REITs. Geltner α 0.5–0.6 reproduces the relevered-REIT −25.7%. Also: desmoothed −24.2 / −28.2 / −35.5 / −49.8% for α 0.5 / 0.6 / 0.7 / 0.8; lead–lag ρ −0.44 / 0.10 / 0.37 / 0.32 / 0.31; gap +41% (Q3-22), +1.0% (Q3-26); the annualized table and min/max | Confirmed | Inputs checked against slide p. 5 and the Nareit file; my independent re-run matches exactly. Sensitivity: with REIT leverage of 30–40% the relevered drawdown is −23.3% to −27.0% and the 2022Q1–26Q3 end-points differ by −1.4 to +2.1pp | https://ncreif.org/__static/jdj5jdewjc9ybldynw1nwu1tm3u2qnkw/NFI-ODCE-2026q2-Performance-Attribution-Webinar-Slides.pdf |
| 8 | ODCE queues peaked at 19.3% of NAV in 1Q24 (4Q24: average 16.4%, median 13.4%; large funds 6–33%, one at 56%; GFC peak ≈15%) | Confirmed | Verbatim | https://www.callan.com/blog/4q24-real-estate/ |
| 9 | ODCE queue just above 10% of NAV in Q1-2026; leverage ≈27%, cost of debt ≈4.5%, >75% fixed; cap rates 4.5–4.7%; ≈17% below replacement cost; new supply ≈54% below peak; data centres ≈19% one-year | Confirmed | Verbatim (Accordant, 25 Jun 2026) | https://www.accordantinvestments.com/knowledge-center/private-real-estate-enters-a-new-cycle-q1-2026-nfi-odce-index-insights |
| 10 | Arnold, Ling & Naranjo (2021): 375 US closed-end funds (2000–2014 vintages) | Confirmed | Every sub-figure checks:<br>• mean IRR 8.69% vs 10.34% for REITs (−165bp); median +13bp;<br>• 53% underperform, 68% after a 425bp adjustment;<br>• vs ODCE: mean +126bp, median +19bp;<br>• higher-risk 7.74% vs lower-risk 9.21%;<br>• leverage 60–70% vs REITs 35–40%;<br>• vintages: 2005 −5.58%, 2008 15.19%, 2009 16.76%;<br>• "quite speculative" | https://www.reit.com/sites/default/files/2021-07/PERE_Fund_Performance_Arnold_Ling_Naranjo_Final_Version.pdf |
| 11 | Bollinger & Pagliari (2019): against core levered to equal volatility, value-add ≈ −326bp and opportunistic ≈ −285bp a year (2000–2017); core leverage < 25%; matching needs ≈55% / ≈65% | Confirmed | Via the CFA summary (gross-return volatility matching); metadata via Crossref | https://rpc.cfainstitute.org/blogs/enterprising-investor/2019/private-real-estate-fund-categories-a-risk-return-assessment |
| 12 | MSCI (Robson & Harmse, 3 Aug 2022): 145 US closed-end funds (2005–2020 vintages, Burgiss); KS-PME 1.07 unlevered, 1.01 levered; 58% / 48% outperform; "2005–07 vintages mostly lost" | Confirmed (wording) | MSCI says 72% of 2005–07 vintage funds *underperformed* both benchmarks. That is relative underperformance, not necessarily absolute losses | https://www.msci.com/research-and-insights/blog-post/did-closed-end-real-estate-funds-add-value |
| 13 | Real-estate LP portfolio pricing "settled at 68% of NAV in H1 2026" | Confirmed | Verbatim (Jefferies p. 5) | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 14 | MSCI Global Private Real Estate closed-end index: 2023 −6.0%, 2024 −2.6%, 2025 +2.3%; quarterly −0.1 / +0.1 / −0.1 / +0.2; ACWI Real Estate +7.3% (2025) and +5.9% (Q2-26); "the clear laggard", +4% five-year; 1,779 funds, $1.31tn | Confirmed | Verbatim (column order checked: 2023, 2024, 2025, Q3-25 … Q2-26) | https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf |
| 15 | MBA: $875bn (17% of ≈$5.0tn) matures in 2026 after $957bn in 2025; $652bn in 2027 | Confirmed | The $957bn was the amount *scheduled* for 2025 in the prior survey. mba.org returns 403 to automated fetches, so I used MBA NewsLink | https://newslink.mba.org/?p=270033 |
| 16 | Trepp, Sep-2026: CMBS 30+ days 8.02%; office 12.16%, multifamily 8.04%, retail 6.58%, lodging 6.18%, industrial 1.14%; 9.66% including performing matured balloons | Confirmed | The six sector rates are corroborated by Scotsman Guide (6 Oct 2026). The 9.66% appears only in Yieldpro, which mislabels the month as "June" | https://yieldpro.com/2026/10/multifamily-cmbs-delinquency-rate-leads-overall-rate-higher-in-september ; https://www.scotsmanguide.com/news/cmbs-delinquencies-reach-highest-level-since-2020/ |
| 17 | Glancy (FEDS 2026): banks extended about half of maturing CRE loans in 2023–25 (Y-14Q); stress-era extensions were 5.1pp more likely to require a ≥5% paydown | Confirmed at the primary | FEDS 2026-025. "Roughly half", and "a similar share … before COVID". The paper says "about 5.1 percentage points more likely to entail paydowns exceeding 5% … relative to before the pandemic". The sample is large banks only | https://www.federalreserve.gov/econres/feds/pretend-or-amend-on-evergreening-in-cre.htm |
| 18 | 10-year ≈5.10% on 15 Oct 2026; Fed hiked to 3.75–4.00% on 16 Sep 2026; Brent ≈$110 | Confirmed | DGS10 was 5.10 on 15 Oct. The hike was a 25bp first hike since 2023, confirmed by several reports. Brent hit a $110 session high and closed at $109.86 on 16 Oct | https://fred.stlouisfed.org/series/DGS10 ; https://www.businesstoday.in/markets/story/brent-hits-110-as-hormuz-ship-attacks-houthi-strikes-on-saudi-trigger-oil-rally-562207-2026-10-17 |
| 19 | 10-year "5.36% on 7 October, the highest since 2002" | Corrected | The H.15 close on 7 Oct was **5.28%**. The peak close was **5.31% on 5 Oct**, which is still the highest close since 2002. 5.36% is not in H.15 and may be an intraday print | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10&cosd=2026-03-25&coed=2026-10-16 |
| 20 | "Brent is ≈$110 with Hormuz closed" (§1.1) | Corrected | The cited source says shipping is "severely disrupted" by attacks and blockades, not closed. The flagged version ("disrupted") is right | Business Today URL above |
| 21 | "With the 10-year now ≈90bp higher than in Q2" (§4.5) | Corrected | On 15 Oct (5.10%) the gap was **≈68bp** over the Q2-2026 average (4.42%) and 66bp over end-June (4.44%). It was ≈85–89bp only at the 30 Sep–5 Oct peak. Yields fell 19bp between 30 Sep and 15 Oct | FRED CSV above |
| 22 | Dubai residential sales Q3-2026: −47% by value (AED72.6bn) and −38% by volume YoY; S&P: prices 5–15% lower since end-2025 (industry estimates); transactions 26% lower a month since the war began; Emaar founder 5–10% | Confirmed | The 26% compares average monthly sales in Mar–Sep 2026 (12,644) with Jan–Feb 2026 (17,198) | https://www.thenationalnews.com/business/property/2026/10/07/dubai-home-sale-transactions-fall-in-third-quarter-due-to-regional-uncertainty/ |
| 23 | Dubai prices ≈55% below the Q3-2008 peak by mid-2010 (Reuters poll; Abu Dhabi ≈40%); later polls ≈58% | Confirmed (nuance) | The 8-Jul-2010 poll: Dubai −55% (median of 14), Abu Dhabi −40% (median of 12). The 58% is a Jul-2011 *forecast* of the total fall. By Apr-2011 Abu Dhabi was already −55%. The TradeArabia link now serves unrelated content, so I used a syndicated copy | https://www.dailynewsegypt.com/?p=120777 ; https://www.arabnews.com/archive/384681 ; https://www.arabnews.com/node/374960 |
| 24 | Gupta, Mittal & Van Nieuwerburgh (AER 2026): NYC office values −45% in 2020 and −39% long run ($453bn) | Confirmed | AER 116(2), 674–709, DOI 10.1257/aer.20231619 | https://www.nber.org/papers/w30526 |
| 25 | NBIM: unlisted real-estate debt ≤ 25% of the portfolio, ≤ 70% per investment; amended 9 Dec 2025 | Confirmed | Mandate §4.2.6 verbatim; the 70% is measured at acquisition or refinancing | https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/ |
| 26 | RCA CPPI May-2026: all property +1.6% YoY; CBD office 50% below its Mar-2022 peak (5-year −45.2%); industrial +10% since Jul-2022; apartments −20% and retail −7% vs that point | Confirmed | Verbatim | https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/rca-commercial-property-price-indexes-rca-cppi/2606-rcacppi-us-msci.pdf |
| 27 | Cannon & Cole (2011): appraisals miss sale prices by >12% individually and 4–5% at portfolio level; they lag in both directions | Confirmed | Abstract verbatim | https://mpra.ub.uni-muenchen.de/32589/ |
| 28 | ADIA's 2025 Review narrowed the real-estate range to 2–7% | Confirmed (secondary) | Down from 5–10%, per several press reports; the ADIA PDF itself was not opened | https://www.hedgeweek.com/news/adia-raises-hedge-fund-and-pe-allocation-targets |
| 29 | Plazzi, Torous & Valkanov: up to 30% of return variability from expected returns; cap rates track expected returns for apartments, retail and industrial, and marginally forecast office rent growth. Pagliari, Scherer & Monopoli: restated means and volatilities not different; gap ≈60bp in 1993–2001 | Confirmed | Abstracts via OpenAlex | https://api.openalex.org/works/doi:10.1093/rfs/hhq069 ; https://api.openalex.org/works/doi:10.1111/j.1080-8620.2005.00115.x |
| 30 | Green Street: "If this rise in yields sticks, property prices are likely to go down". MSCI: real-estate fund distributions "breached new lows". Target allocations fell in 2025 for the first time in 13 years (Hodes Weill & Cornell) | Confirmed | Green Street (6 Oct 2026, Rothemund); both MSCI 2026 outlook pieces | https://eu.greenstreet.com/waiting-for-price-clarity/ ; https://www.msci.com/research-and-insights/blog-post/private-capital-in-focus-trends-to-watch-for-2026 |
| 31 | ODCE Q2-2026 net return 1.29%, which anchors the "gross–net ≈20bp a quarter" fee calibration | Unverifiable | Not in the release, the slides or RCLCO. It equals NPI's 1.29% total, so check for a mix-up | — |
| 32 | ODCE queue ≈12% in mid-2025 (§4.6) | Unverifiable | Not in Callan or Accordant; it comes via G14 (Meketa/Townsend). It is also one of the queue-fit targets (§4.4) | — |

## 3. Citation check

| Reference | Status | Notes |
|---|---|---|
| NCREIF NFI-ODCE 2Q2026 release (30 Jul 2026); index page; 2Q26 webinar slides; ODCE attribution slides (16 Sep 2026) | OK | Dates, titles and contents match |
| Arnold, Ling & Naranjo (Jun 2021), Nareit-hosted | OK | Authors, date and title match the PDF |
| Bollinger & Pagliari (2019), *JPM* 45(7), 95–112, doi 10.3905/jpm.2019.1.098 | OK | Crossref: "Another Look at Private Real Estate Returns by Strategy" |
| Robson & Harmse (3 Aug 2022), MSCI | OK | — |
| Wrighton (2026), MSCI PCB Summary Q2-2026 | OK | Author in the PDF metadata |
| Jefferies (Jul 2026); Callan (4Q24); Accordant (25 Jun 2026) | OK | — |
| Gupta, Mittal & Van Nieuwerburgh (2026), *AER* 116(2), 674–709 | OK | NBER page gives the published version |
| Gupta & Van Nieuwerburgh (2021), *JF* 76(6), 3255–3307 | OK | OpenAlex |
| Pagliari, Scherer & Monopoli (2005), *REE* 33(1), 147–187 | OK | Crossref |
| Riddiough, Moriarty & Yeatman (2005), *REE* 33(1), 121–146 | OK | Crossref (findings still [U], as the dossier says) |
| Plazzi, Torous & Valkanov (2010), *RFS* 23(9), 3469–3519 | OK | Crossref |
| Andonov, Eichholtz & Kok (2015), *JFM* 22, 73–103 | OK | Crossref |
| Chervachidze, Costello & Wheaton (2009), *JPM* 35(5), 50–69 | OK | OpenAlex |
| Delfim & Hoesli (2021), *REE* 49(1), 75–105 | OK | Online 2019, print 2021 |
| Cao & van Beek (2025), *FAJ* 81(3), 60–75 | OK | Crossref |
| Geltner (1991), *JREFE* 4(3), 327–345; Geltner (1993), *JRER* 8(3), 325–345 | OK | — |
| Fisher, Geltner & Webb (1994), *JREFE* 9, 137–164 | OK, minor | The issue is 9(2) |
| Fisher, Geltner & Pollakowski (2007), *JREFE* 34(1), 5–33 | OK | Crossref doi 10.1007/s11146-007-9001-6 |
| Takahashi & Alexander (2002), *JPM* 28(2), 90–100 | OK | Crossref |
| **Fisher & Hartzell (2016)** | **Wrong DOI** | doi 10.1007/s11146-016-9556-1 is the *editors' introduction* to the special issue (Eichholtz, Geltner & Ong, *JREFE* 52(4), 323–326). The correct reference is **Lynn M. Fisher & David J. Hartzell, "Class Differences in Real Estate Private Equity Fund Performance," *JREFE* 52(4), 327–346, doi 10.1007/s11146-015-9526-z** |
| Cannon & Cole (2011) | Incomplete | Published in *JPM* 35(5), 68–88, doi 10.3905/jpm.2011.35.5.068 (Crossref) |
| Pagliari (2017) | Incomplete | Published in *REE* 48(1), 89–134 (online 2017, print 2020), doi 10.1111/1540-6229.12190 |
| Glancy (2026), via Propmodo | Upgrade | Cite the primary instead: FEDS 2026-025, doi 10.17016/FEDS.2026.025 (findings verified there) |
| Crosignani & Prazad, NY Fed SR 1130 | OK | Oct 2024, revised Jun 2026, per the NY Fed page |
| TradeArabia (8 Jul 2010) | Link degraded | Now serves unrelated content. The Reuters poll text is confirmed via the Daily News Egypt syndication |
| MBA (9 Feb 2026) | Link 403 | Content confirmed on MBA NewsLink |
| Macro prints, ref. 32 | Partly wrong | The CNBC URL returned 403 (the hike was confirmed elsewhere); 5.36% is not an H.15 close; Hormuz is "disrupted", not "closed" |
| Yieldpro (Trepp) | Weak relay | Mislabels the month and the retail direction. Prefer Trepp's own release; the figures are corroborated by Scotsman Guide |

## 4. Reasoning issues and overclaims

### Must-fix

**4.1 The starting stale-appraisal gap G₀ (5–8% asset level, ≈10% equity level) contradicts the dossier's own evidence.**
- **How it is presented.** §1.1 calls it a "**Consequence**" of today's market. In fact it is an [I] assumption, and it drives these results:
  - the §6.5 reported-versus-true gaps (base_mc reported 3-year return −1.6% vs true +3.6%; reported drawdown −10.5% vs true −2.9%);
  - the "Reading 2" narrative;
  - the B6 example at a 10% gap;
  - the SELL thresholds.
- **Evidence against it, from the dossier itself:**
  - **Listed-implied gap.** The public-data series puts ln(ODCE) − ln(relevered REITs) at **+1.0% at 2026Q3**, and −6.1% at 2026Q2 (§4.3; `g10_public_and_arith_results.json`).
  - **Sales evidence.** NCREIF's Q2 sales cleared within ±4% of marks.
  - **Rate timing.** The rate shock happened *within* Q3 (10-year 4.44% → 5.29%), which the Sep-30 REIT prices already reflect. Yields then *fell* to 5.10% by 15 Oct, so there is no further "October shock".
  - **Engine dynamics.** The engine's own partial adjustment (κ_c = 0.15 a quarter) would carry only about 15% of a one-quarter cap-rate shock into V^T, so it cannot generate an immediate 5–8% gap.
  - **Cap-rate comparison.** The NPI appraisal cap rate (4.4%) is compared with RCA transaction cap rates (5.6–8.3%), but §3 trade-off 2 says those two series differ in quality, mix and NOI basis.
- **Fix.**
  - Derive G₀ explicitly. For example, the cap-rate nowcast: β_y × Δy10 ≈ 0.45 × 85bp ≈ +38bp, or ≈ −8% at a 4.5% cap rate. The REIT-implied method gives ≈0–2%.
  - Run G₀ ∈ {0, 2%, 5–8%} as a sensitivity and tag it [I].
  - Reword §1.1.

**4.2 The look-through constraints mostly bind on debt ADIC cannot manage.**
- **Where the debt sits.** Of the synthetic $8.03bn of look-through debt:
  - ≈$4.62bn (**58%**) sits inside open-end (≈$0.98bn) and closed-end (≈$3.64bn) funds;
  - ≈$1.07bn (13%) sits in sponsor-led co-investments;
  - only ≈$2.33bn (29%) is JV or direct (computed from `g10_re_engine_results.json`).
- **Why that breaks the constraints.**
  - RE-MAT's remedy ("stagger maturities and extend early") and RE-FLT ("hedge expiry ≥ loan maturity") are not available to an LP.
  - RE-LT1's *hard* 55% limit on V\* is breached at the credit-crunch P50 peak (62%). Inside funds it can only be cured by SELLing LP interests at about 68% of NAV, a pro-cyclical fire sale.
- **Fix.** Split controllable debt (JV/direct, and co-investments with consent rights) from monitored debt (fund look-through). Apply the hard limits to the first, and charge the second as a risk term (λ_Lev, CVaR) rather than imposing a constraint.

**4.3 The P(extension) calibration misreads Glancy.**
- **Unconditional vs conditional.** Glancy's "roughly half" is the *unconditional* share of maturing large-bank loans that are extended, and it was "similar … before COVID". The engine instead applies P(ext) only *conditional on a refinancing gap*, and sets it at 0.35 in expansion rising to 0.50 in late-cycle and crisis.
- **Wrong direction in stress.** Glancy finds the opposite for risky loans after 2022:
  - low-debt-yield loans were ≈7pp less likely to be extended, and non-recourse loans ≈5pp less likely;
  - terms tightened (more paydowns, guarantees and spreads).
- **Consequence.** A crisis P(ext | gap) of 0.50 probably overstates extension relief, which understates cures and hand-backs. The 0.35/0.50 regime pattern has no support in the cited source.
- **Coverage.** Glancy covers banks with more than $100bn of assets only; CMBS servicers, life companies and debt funds behave differently.
- **Fix.** Re-anchor P(ext | gap, S) on loan-level distress studies, or treat it as a misspecification axis.

**4.4 The queue validation is circular, and the starting queue is a model output.**
- **Circular gate.** b = 0.12 and w = 0.08 were fitted to the 2024Q1 (19.3%), 2025Q2 (≈12%) and 2026Q1 (≈10.5%) targets. Gate V-RE2 then tests the same 1Q24 and 1Q26 points, so it cannot fail.
- **Fix for the gate.** Validate out of sample, for example:
  - the GFC queue peak (≈15%);
  - Townsend payout speeds (≈71% of the queue a quarter after 2007; ≈5% in 2023; cited via G14, not verified here);
  - fund-level dispersion (6–56%).
- **Starting queue.** "Today's ≈8% queue" (§1.6, §6.4) is the replay's own extrapolation (8.3% at Q2-26; 6.8% at Q3-26). The last observation was "just above 10%" (Q1-26). The headline φ(h,S) figure, 34% paid within a year, depends on it.
- **Fix for the starting queue.** Label it model-implied and show φ from a 10% start.

**4.5 The fund-interest SELL threshold (§1.11, §6.6) is contradicted by B5, and B5 omits unfunded commitments.**
- **The arithmetic.** At θ = 0.85, μ = 4% and ℓ = 5%, the script's hold value is **69.4% > the 68% bid**, so SELL still loses about 1.4pp. A break-even needs θ < ≈0.83 or ℓ > 5%.
- **Unfunded commitments.** B5 assumes no unfunded commitments, yet the action table says the buyer assumes them.
  - The synthetic closed-end book has $1.2bn of unfunded on $2.6bn of NAV (U/NAV ≈ 0.46).
  - Shedding contingent calls in a DPI drought has liquidity value that the comparison leaves out, which biases it against SELL for young funds.
  - The 68% is also an *average* LP-portfolio price; fund-specific discounts depend on age and unfunded.

### Should-fix

**4.6 Ranges are trimmed relative to the script's own grids.**
- **B4.** Levered cash yields for debt at 6.8–7.1% are **3.35–5.8%**, not 3.8–5.8%. The text's range uses the 6.8% rate only, and is computed before capex.
- **B6.** Redemption value at a 10% gap is **91.6–94.7%** across the script's 5–25%-a-quarter payout grid, not 92.5–94.7%. The dropped 5%-a-quarter case is the stress-relevant one: Townsend (as cited via G14) reports ≈5% of the queue paid a quarter in 2023, and the engine's credit crunch pays about 6% a quarter.

**4.7 Misattributed causes.**
- **Income.** "Income reaching ADIC is ≈2.1% of NAV *because* new debt at 6.8–7.6% costs more than cap rates of 5.6–6.9%" does not describe the engine.
  - Engine income comes from appraisal-basis yields (≈4.7%), capex, fees, and legacy coupons (3.0–6.0%) plus floating debt at f + spread.
  - New-debt pricing against transaction cap rates matters for refinancing and LEVER, not current income.
  - Retail at 6.9% is not below 6.8%.
- **Leverage.** "Capex debt-funded, so leverage drifts up (22.4% → 27.1%)" misreads NCREIF.
  - 22.4% is the 2000–2026 *average*, not a starting point.
  - The 2022–24 rise is mostly a denominator effect: a ≈20% value fall takes 22% leverage to ≈27.5%. Redemption funding adds to it. NCREIF does not attribute the rise to capex.
  - Debt-funding all open-end capex also ratchets leverage up mechanically in every scenario.

**4.8 The cap-rate "consistency check" (§6.3b) mixes levels.**
- **The check.** ≈−22% at flat NOI for unlevered property is compared with ODCE's ≈−24% *fund-level, levered* appreciation. At ≈25% leverage that is about −18% at asset level.
- **Partial offset.** The check also ignores 2022–24 NOI growth. The two errors roughly cancel, but the check does not validate β_y = 0.45 as stated.

**4.9 Specification ambiguities that will bite implementers.**
- **Notation collisions:**
  - M_t is both market rent and maturing debt (the gap formula);
  - c_t is both the cap rate and the contribution rate (the queue);
  - Q is defined as a share of NAV but is updated with dollar R_t, W_t and P_t.
- **Undifferenced Gulf terms.** λ^liq is differenced against S₀, but the Gulf add-ons φ(Z_t) and h_k(Z_t) are not differenced against Z₀ = GW. Gulf assets therefore take an immediate +75bp cap-rate target and a 4–25% NOI cut at t = 1, although the war has been under way since about March 2026. Either state that appraisals have not priced the war, which overlaps with G₀, or difference against Z₀.
- **Transaction window.** The engine sets e^RE = D whenever Z = GW in *any* regime, while the §6.3(b) table restricts that rule to late-cycle.

**4.10 The rate narrative is misdated.**
- §1.1 frames "today's state" as an October rate shock. In fact the shock ran from Jul to Sep, and yields eased in October (§2, rows 19–21).
- The all-in debt rate inference uses 10y + spread, so its numbers are barely affected. The "≈90bp since Q2" statement should be fixed, though.

### Minor

- **4.11** "ODCE NAV stayed above listed-implied value for six quarters" (§5): the dossier's own gap series is positive for **10** consecutive quarters (2022Q1–2024Q2) and above +20% for six of them.
- **4.12** The ≈1.7–2.5pp premium on RCA apartment and industrial cap rates uses g = 2.5% only, while the NPI calculation alongside it uses g = 2–3%. Over the same assumptions the range is ≈1.2–3.0pp.
- **4.13** The lead–lag correlations rest on 15–19 quarterly observations (SE ≈ 0.25). The 3-quarter trough lag is a single-episode estimate and should be treated as a prior, not a gate target.
- **4.14** The NOI-growth target is ambiguous. NCREIF's same-store rolling-4Q figure is 0.78%, while RCLCO reports *overall* NPI NOI growth of 2.2% for the year. V-RE1 and the inflation pass-through claim (§1.10) should name the measure.
- **4.15** "Cash accretion requires c > r_D" (§2.3) ignores capex. It should read c − κ^cap > r_D, or use the loan constant if the debt amortizes, which matches the LEVER rule used later.
- **4.16** The §4.4 "Allocations" row and §1.4 cite MSCI correctly. Note, though, that *Real Assets in Focus* says closed-end distributions "flatlined"; "breached new lows" is from the *Private Capital in Focus* piece.

### Checked and found sound

- §2.1's return decomposition (exact with c_{t+1} in the denominator) and its log-linearization.
- §2.3's leverage identity.
- §2.4's Geltner forward and inverse filters.
- The 80% catch-up of 3.7–5.5 quarters for α 0.55–0.70 (1-quarter lag), and the κ_c half-life of ≈4.3 quarters.
- The repricing grid (−10.0 / −7.3 / −18.2 / −15.4%) and the required cap rate of 5.8–6.8%.
- The cure condition (V^T − D + gap > 1.1·gap ⇔ V^T − D > 0.1·gap) and the refinancing-gap allocation.
- The open-end payout band of ≈1.2–1.5% of NAV a quarter, consistent with ODCE's 8.5%-of-NAV annual outflow less income distributions.
- The 2021-loan cure of 18.8% of value.
- LTV 47.1%, and 42% of debt maturing within 24 months.
- The SELL / HOLD / REFINANCE / LEVER availability by vehicle (no LP-level REFINANCE for open-end units; NAV facility dominated). The reclassification of JV sell-downs as partial SELLs is consistent with the user's definitions, though it departs from the brief's interim list (§8).

## 5. Overall reliability

**Factual layer: high.**
- Every flagged number traces to its primary source.
- The public-data calculations replicate exactly.
- The four corrections are presentational: one Treasury print, Hormuz wording, one bp-move statement, and one NOI range.
- One DOI is wrong and two links have degraded.

**Design and specification layer: medium.**
- §4.1–4.5 should be fixed before IC use. The G₀ assumption is the most consequential: it drives the headline reported-versus-true results and is contradicted by the dossier's own listed-implied and sales evidence.
- §4.2 and §4.3 change which constraints bind and how large the cure and hand-back tails are.

**Overall: medium.** The dossier is a reliable evidence base. Its synthetic outputs and decision thresholds should be re-run after the fixes above.
