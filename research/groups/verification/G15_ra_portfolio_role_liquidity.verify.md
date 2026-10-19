# G15 Real Assets in the Total Portfolio: Verification Log

- **Dossier checked:** `research/groups/dossiers/G15_ra_portfolio_role_liquidity.md` (stream G15, dated 2026-10-18). The dossier was not edited.
- **Background read:** context §1A (eight groups; Real Assets confirmed as real estate, infrastructure, and energy & natural resources, via funds, co-investments and JVs/direct; working size $18bn); design brief §8 (interim Real Assets rules); `research/groups/addenda/G15_calcs/g15_ra_calcs.py` and `g15_ra_results.json`.
- **Date of check:** 2026-10-18. Adversarial fact-check ahead of the IC pack.
- **Method:**
  - Primary pages were fetched directly. PDFs were downloaded to isolated scratch folders and text-extracted with pypdf (`python -I`). These were: NCREIF NFI-ODCE 4Q-2025 and 2Q-2026 releases, the NCREIF 2Q-2026 webinar, the MSCI Private Capital Benchmarks Summary Q2-2026, AQR (2019), Cambridge Associates (2016), the GIC Report 2025/26, Jefferies H1-2026 and NBER w26514.
  - Academic metadata came from the Crossref and OpenAlex APIs, with abstracts where available. The Hoesli–Lizieri–MacGregor abstract came from the Geneva open archive, and the Andonov–Eichholtz–Kok abstract from RePEc. Consensus was not used.
  - The FRED series QAEN628BIS (BIS UAE residential prices) and CPIAUCNS were re-read live.
  - An untouched copy of `g15_ra_calcs.py` was re-run and diffed against `g15_ra_results.json`.
  - Independent checks were scripted: UAE–Brent lead-lag, Geltner-consistent reported marks under T4′, stressed LTVs, and fund-level refinancing shortfalls. The scripts are saved next to this log as `G15_ra_verify_checks.py` and `G15_ra_verify_fund_cures.py`.
- **Synthetic notice:** book-level figures quoted below (sleeves, cures, ladder, LTVs) are the dossier's synthetic defaults. *SYNTHETIC – NOT ADIC DATA.*

---

## 1. Summary

- **Scope:** 40 claims were checked: **31 confirmed, 5 corrected, 2 refuted, 2 unverifiable**.
  - All **20 author-flagged claims** hold: 18 confirmed and 2 corrected for wording or scope only. None was refuted.
  - The 2 refutations and 2 of the corrections concern the dossier's *own analysis*, not its sources.
- **The sourced evidence is strong.** The following match the primary text, mostly verbatim:
  - **Market data:** NCREIF (both releases and the webinar), MSCI Q2-2026, Callan, Accordant, bfinance/Infralogic, MBA, Green Street via Bisnow, Cambridge Associates 2016, The National, the IMF, Jefferies.
  - **Peers:** GIC, NBIM, CalPERS, CA FY2025 endowments.
  - **Public data:** the UAE cycles and the CPI figures, re-read on FRED.
  - **Academic findings:** Andonov–Kräussl–Rauh, Hoesli–Lizieri–MacGregor, Rödel–Rothballer, Wurstbauer–Schäfers, Muckenhaupt–Hoesli–Zhu, Couts–Gonçalves–Rossi, Andonov–Eichholtz–Kok, Gupta–Van Nieuwerburgh.
- **Source-level corrections:**
  1. **Ares's 7% is for "global real estate funds".** The article names no data source and no vehicle type, so "closed-end" is the author's inference. It nonetheless calibrates the closed-end VA/opp sleeve.
  2. **ADIA *lowered* its real-estate range rather than narrowing it:** "declined from 5%-10% to 2%-7%", so the width is unchanged. PE went from 12–17% to 15–20%, and Financial Alternatives from 5–10% to 7–12%. ADIA's investments page still shows the pre-Review ranges.
  3. **AQR's "1–3%" REIT outperformance is measured since inception, not over 1980–2012.**
- **Citation problems:**
  - The **Pagliari (2017)** reference is the wrong paper. The capex ≈ ⅓ NOI figure that AQR uses comes from *JPM* 43(6):44–61, not *REE* 45(1).
  - The NBIM limits are not on the cited page.
  - Stein (1997) and Getmansky–Lo–Makarov (2004) are cited in the text but missing from the references.
  - Two practitioner titles are slightly off (§3).
- **Analysis-level issues.** These matter more for the IC:
  1. **R1: fund-level refinancing stress is claimed but not modelled.** The dossier's own cure formula on fund sleeves adds **$0.22bn (12m) / $0.54bn (24m)** of T4′ shortfall. That is larger than the $0.23bn lower bound of the claimed T4′ relief versus PE.
  2. **R2: the look-through LTV ≤ 50% and single-asset ≤ 60% limits break in the dossier's own T4′.** Look-through LTV goes from 49% to ≈62%; the closed-end VA/opp real-estate and real-estate co-investment sleeves reach ≈80%. Most of the book (63% in funds) is also outside ADIC's control as LP.
  3. **R3: REFINANCE, JV sell-down and cure actions are booked on GP-controlled co-investment sleeves.**
  4. **R4: "reported marks ≈ ⅓ of the true loss" contradicts the dossier's own Geltner φ.** That φ gives ≈⅔ (≈$4.9bn, not $2.7bn).
  5. **R5: the 2–6-quarter oil lag for GCC real estate is not supported** by the dossier's own lead-lag, which peaks at 0–1 quarter and is not significant.
  6. **R6–R7:** the inflation-hedge claim is stronger than the evidence (R6), and the 26bp return cost compares CMAs that do not match the book's leverage and strategy mix (R7).
- **Reproducibility:** the re-run reproduces `g15_ra_results.json` exactly (0 differences), and every dossier [I-calc] figure matches it to rounding. The §6.5 ladder table omits the real-estate co-investment row that the totals include (§5).
- **Overall reliability: MEDIUM.** It is **high for sourced facts** and **medium for the design layer**. R1–R4 should be fixed, and findings 2 and 6 and IC implications (d)–(e) restated, before IC use.

---

## 2. Claims table

| # | Claim (as in dossier) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | Closed-end RE fund distributions 7% of NAV (rolling 4Q to Q3-2025), ≈⅓ of the 10-year average, a 10-year low. 2025 RE secondary volume a record $20.3bn: GP-led $14.5bn; LP-led $5.8bn, of which core open-end $2.65bn and VA/opp $3.1bn. Core discounts "single digits"; global direct volumes −34% vs 2021 (CBRE) | **Corrected (scope)** | Every number is verbatim (11 Feb 2026). **The 7% is "the rolling annual sum of quarterly distributions across global real estate funds as a percentage of NAV".** The article names no data source and does not say closed-end, so applying it to the closed-end VA/opp sleeve is an inference [I]. | https://www.ares.com/us/news-and-insights/real-estate-secondary-market-volume-hits-record-20-billion-2025 |
| 2 | MSCI Q2-2026: PE distribution rate 9% in H1-2026 (11% in 2025); all private capital 10–11% (historical ≈20%). Returns 2023/24/25 and Q1/Q2-26: private RE −6.0/−2.6/+2.3 and −0.1/+0.2; infrastructure +8.5/+6.4/+12.6 and 1.7/2.5; NR +1.6/+3.7/+4.9 and 6.9/3.6 | Confirmed | The fund-benchmark table (p. 7) and the capital-flow tables (pp. 12–13) match exactly. MSCI: PE "just 9% in H1, down from 11% in 2025"; all private capital "roughly 10–11% ... historical average of around 20%". Distribution rate = distributions ÷ previous valuation, annualised. | https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf |
| 3 | NFI-ODCE 4Q-2025: leverage 27.1% (22.3% average since 2000, range 15–34%). 2025 contributions $12.2bn vs distributions and redemptions $19.9bn (net −$7.7bn). 25 funds, GAV $277.5bn, NAV $227.3bn. 2025 total return 3.79% (income 4.09%) | Confirmed | Verbatim in the 30 Jan 2026 release. | https://ncreif.org/__static/jdj5jdewjezar2nuz3rrtevsy2rnqm5l/NFI-ODCE-Press-Release-for-4Q-2025.pdf |
| 4 | ODCE queues peaked at 19.3% of NAV in 1Q24 vs ≈15% in the GFC. 4Q24 average 16.4%, median 13.4%; large funds 6–33% (one outlier at 56%). The decline came mainly from rescissions | Confirmed | Verbatim (Iman & Quach, Callan, 20 Feb 2025). The page title differs from the dossier's reference (§3). | https://www.callan.com/blog/4q24-real-estate/ |
| 5 | Accordant Q1-2026: queues "just above 10% of NAV"; payments ">10%"; leverage ≈27%; cost of debt ≈4.5%, >75% fixed; cap rates 4.5–4.7%; debt "not yet broadly accretive"; acquisitions > dispositions; ≈17% below replacement cost | Confirmed | All verbatim (25 Jun 2026). | https://www.accordantinvestments.com/knowledge-center/private-real-estate-enters-a-new-cycle-q1-2026-nfi-odce-index-insights |
| 6 | bfinance via Infralogic: open-end infrastructure targets ≈10% return and ≥6% yield; closed-end core/core-plus 10–12% return and 4–5% yield; value-add 12%+ and 3–4% | Confirmed | Verbatim (5 Jun 2026). These are *target* fund-level yields. | https://ionanalytics.com/insights/infralogic/open-ended-funds-appeal-endures-despite-lull/ |
| 7 | Desmoothed private RE correlates 0.66 with equities vs 0.82 for REITs, and 0.77 with REITs. Desmoothed unlevered vol ≈11% (vs ≈9% for 60/40). Capex ≈⅓ of NOI; NCREIF NOI yield 4.4% → 2.9% FCF. Citing Shepard et al. 2015 and Pagliari 2017 via AQR 2019 | Confirmed (citation fix) | Verbatim in AQR (Ilmanen, Chandra & McQuinn, 31 Jan 2019), pp. 2–5 and appendix. The NOI yield is as of 30 Sep 2018. **AQR's Pagliari (2017) is "Some Thoughts on Real Estate Pricing", *JPM* 43(6):44–61, not the *REE* paper in the dossier's list (§3).** | https://www.aqr.com/-/media/AQR/Documents/White-Papers/Demystifying-Illiquid-Assets---Expected-Returns-for-Real-Estate.pdf |
| 8 | Private infrastructure beta to a 50/40/10 portfolio: 0.6 in MSCI's factor model, vs ≈0.1 on smoothed valuations, ≈0.2 as a bond proxy and 1.3 for listed US infrastructure | Confirmed | Verbatim (Hayes & Liu, 4 Aug 2021). The infrastructure sleeve is **unlevered** (55% US utilities, 25% US industrials, 20% North American energy). The betas are to the 50/40/10 multi-asset portfolio, **not to equities** (see R9). | https://www.msci.com/research-and-insights/blog-post/assessing-private-infrastructure-in-a-multi-asset-class-portfolio |
| 9 | Infrastructure fund cash flows are as volatile and cyclical as other PE and depend on quick exits; public investors underperform; ESG explains ≈25–40% of allocations and ≈30% of underperformance | Confirmed | Abstract: cash flows "display similar volatility and cyclicality as other private equity investments, and their *performance* similarly depends on quick deal exits"; "ESG preferences *and regulations* explain 25%–40% ... and 30% of their underperformance". RFS 34(8). | https://doi.org/10.1093/rfs/hhab048 |
| 10 | Long-run returns (including RE) are positively linked to expected inflation, not to shocks. Adjustment is "gradual and not within period"; direct RE differs from equities | Confirmed | Abstract: "In the long-run, once real and monetary variables are included, asset returns are positively linked to anticipated inflation but not to inflation shocks. Adjustment processes are, however, gradual and not within period." The §2.2 gloss "long-run δ near 1" is not in the abstract [U]. | https://doi.org/10.1007/s11146-007-9062-6 ; https://archive-ouverte.unige.ch/unige:5738 |
| 11 | Listed infrastructure (824 firms, 46 countries, 37 years) hedges inflation about as well as equities. Only strong-pricing-power firms do slightly better, at five-year horizons | Confirmed | Abstract verbatim (OpenAlex). | https://doi.org/10.3905/jai.2012.15.1.110 |
| 12 | On EDHECinfra data for Q4-2019 to Q3-2024, infrastructure equity returned more when US CPI ≥ 4%: over 1pp a quarter more in network utilities and transport. It also beat MSCI ACWI and the Bloomberg Global Aggregate | Confirmed | Chen & Shen, PGIM, 14 Apr 2025. The regime is US CPI YoY above or below 4%, with "quarterly returns increasing by more than a percentage point". CPI was ≥ 4% in only about 8–9 of the 20 quarters, all in one episode, 2021–23 (R6). | https://www.pgim.com/es/en/institutional/insights/asset-class/multi-asset/multi-asset-solutions/direct-infrastructure-equity-performance-return-attribution |
| 13 | MBA: $875bn (17%) of $5.0tn matures in 2026 ($957bn in 2025); hotel 30%, industrial 23%, office 17%, multifamily 13% | Confirmed | Verbatim (9 Feb 2026). | https://newslink.mba.org/?p=270033 |
| 14 | UAE residential prices −36.5% (2008Q2–2010Q4) and −30.2% (2014Q4–2020Q3). 4-quarter changes correlate 0.32–0.36 with Brent at 0–1-quarter lags | Confirmed | FRED QAEN628BIS (index 2010 = 100; last observation 2024Q1, updated 27 Jun 2024): 151.366 → 96.1115 (−36.5%); 174.7548 → 121.9808 (−30.2%); then +43.8%. Recomputed independently: 0.320 / 0.363 / 0.312 / 0.216 / 0.158 / 0.170 / 0.250 at L = 0 / 1 / 2 / 3 / 4 / 6 / 8. **With n_eff ≈ 20, t ≈ 1.4–1.65, so none is significant at 5%** (R5). | https://fred.stlouisfed.org/series/QAEN628BIS |
| 15 | Dubai Q3-2026 home sales −47% by value (Dh72.6bn) and −38% by count (34,000) (Cavendish Maxwell). Prices −5% to −15% from end-2025 to Sep-2026 (S&P citing industry reports). Monthly sales 12,644 (Mar–Sep) vs 17,198 (Jan–Feb) | Confirmed | Verbatim (7 Oct 2026). Two nits: the S&P/DLD monthly averages are "total real estate sale transactions", not homes; and the article says "robust supply pipeline", without the dossier's "2027–28". | https://www.thenationalnews.com/business/property/2026/10/07/dubai-home-sale-transactions-fall-in-third-quarter-due-to-regional-uncertainty/ |
| 16 | CA private energy benchmark −20.5% in 2015 vs −32.9% S&P GSCI and −25.5% MSCI World NR | Confirmed | Verbatim (June 2016). The benchmark covers PE energy plus upstream energy and royalty funds, and uses appraisal marks. The public figures are time-weighted total returns (footnote 1). | https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2016/06/Real-Asset-Dynamics-June-2016.pdf |
| 17 | ADIA's 2025 Review "narrowed" real estate from 5–10% to 2–7% and raised PE to 15–20%; the website shows infrastructure at 2–7% | **Corrected (wording)** | The Review says **"Real Estate declined from 5%-10% to 2%-7%"**: the range was lowered and its width is unchanged. Also "Private Equity increased from 12%-17% to 15%-20%" and "Financial Alternatives increased from 5%-10% to 7%-12%"; there is no infrastructure change. **The ADIA investments page still shows the pre-Review ranges** (RE 5–10%, PE 12–17%, infrastructure 2–7%). | https://www.adia.ae/en/pr/2025a/index.html ; https://www.adia.ae/en/investments |
| 18 | GIC Real Assets 22% at 31 Mar 2026 (23% in 2025). The Strategic Portfolio has three groups: Equities (growth), Fixed Income (income), Real Assets (inflation). GIC increased commodities, gold and infrastructure for inflation resilience | Confirmed | Table 2 and Box 3 of the GIC Report 2025/26, verbatim. The grouping "covers our holdings across both public and private markets". | https://www.gic.com.sg/uploads/2026/07/GIC_AR_2025-26_PRINT.pdf |
| 19 | NBIM at 30 Jun 2026: unlisted RE 1.6%, unlisted renewable infrastructure 0.5%; limits 7% and 2% | Confirmed (citation fix) | The fund-value page confirms 1.6% / 0.5% (NOK 373bn / 104bn) but **shows no limits**. The limits are in NBIM's 2023 submission ("up to 7 per cent ... unlisted real estate and up to 2 per cent in unlisted renewable energy infrastructure"); the investment-areas page shows the 2%. | https://www.nbim.no/en/investments/the-funds-value/ ; https://www.nbim.no/en/publications/submissions-to-ministry/2023/regulation-of-unlisted-investments-in-the-management-mandate-for-the-government-pension-fund-global |
| 20 | Green Street CPPI 22% below its Mar-2022 peak by Nov-2023; core −25%, office −35%, multifamily −30% | Confirmed | Verbatim (Bisnow, 8 Dec 2023). | https://www.bisnow.com/news/national/capital-markets/green-street-cre-prices-fell-another-3-but-may-well-have-hit-bottom-121991 |
| 21 | US CPI (CPIAUCNS) Dec/Dec: 6.45% (2022), 3.35% (2023), 2.89% (2024), 2.68% (2025). +3.98% in Jan–Sep 2026; 3.74% YoY to Sep 2026 | Confirmed | FRED (updated 14 Oct 2026): Dec 2021–25 = 278.802 / 296.797 / 306.746 / 315.605 / 324.054; Sep-2025 = 324.800; Sep-2026 = 336.940. | https://fred.stlouisfed.org/series/CPIAUCNS |
| 22 | MSCI five-year cumulative returns to Q2-2026: NR +60%, infrastructure +56%, private RE +4%. NR +6.9% in Q1-2026 | Confirmed | MSCI summary, pp. 7–8. | (MSCI PDF, row 2) |
| 23 | Jefferies LP pricing in H1-2026: RE ≈68%, infrastructure 91% of NAV | Confirmed | "Infrastructure pricing remained robust in H1 2026 at 91% of NAV"; "Real estate pricing settled at 68%". | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 24 | NFI-ODCE trailing year to 2Q-2026: total 4.45%, income 4.08% (gross) | Confirmed | NCREIF 2Q-2026 release (30 Jul 2026). Its Q1/Q2-2026 totals (1.25% / 1.49%) match the script's inputs (1.2 / 1.5). | https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf |
| 25 | ODCE's 40-year 3-year-trailing standard deviation is 6.9%, vs 9.6% for NAREIT | Confirmed (interpretation caveat) | Webinar slide 4, StdDev row: T-bill 2.4%, S&P 500 9.9%, NAREIT 9.6%, NFI-ODCE 6.9%. **This is the dispersion of overlapping 3-year annualised returns, not return volatility.** The S&P 500's 9.9% shows it should not be read as a risk ratio. | https://ncreif.org/__static/jdj5jdewjc9ybldynw1nwu1tm3u2qnkw/NFI-ODCE-2026q2-Performance-Attribution-Webinar-Slides.pdf |
| 26 | Average risk-adjusted profit is −17¢ per $1 for real estate funds and −10¢ for infrastructure funds | Confirmed | NBER w26514: "-17 cents in real Estate, and -10 cents in Infrastructure" (Preqin data; the Burgiss robustness check gives −21¢ for infrastructure). | https://www.nber.org/system/files/working_papers/w26514/w26514.pdf |
| 27 | US endowments above $3bn average 9% real assets; the peer average fell 2pp in three years | Confirmed | Verbatim (CA, 20 Feb 2026). "Mostly private" is not stated in what was read [U]. | https://publishedresearch.cambridgeassociates.com/fiscal-year-2025-annual-review-of-endowments-asset-allocation-and-implementation/ |
| 28 | IMF PIN 10/20: "mid-2008 bursting of the Dubai property bubble"; Dubai World standstill "through May 2010, including on bonded debt owed by Nakheel"; hydrocarbon export revenues ≈ −45% in 2009 ($102.7bn → $56.8bn) | Confirmed | Verbatim (17 Feb 2010). | https://www.imf.org/en/News/Articles/2015/09/28/04/53/pn1020 |
| 29 | J.P. Morgan assumptions: PE 10.2% (2026 LTCMA); core RE 7.9% and infrastructure 7.1% (2027 LTCMA) | Confirmed | The 2027 LTCMA page (data as of Sep 2026) shows "global core real estate 7.9%" and "global infrastructure 7.1%" (also confirmed upstream, stream-07 verify #24). PE 10.2% is from the 2026 press release; one J.P. Morgan piece says 10.3%. See R7 on comparability. | https://am.jpmorgan.com/us/en/asset-management/adv/insights/portfolio-insights/ltcma/ |
| 30 | "Over 1980–2012 REITs outperformed NCREIF by 1–3% a year unadjusted; the gap almost disappears after leverage and sector adjustment" (AQR citing Ang et al. 2013) | **Corrected** | **AQR's "1–3%" is REIT outperformance "since inception"** (footnote 4: arithmetic 2.9% / 1.8%, geometric 1.6% / 1.0% vs NPI / NTBI since 1978 / 1984). The 1980–2012 window is a separate Ang et al. exhibit, in which unadjusted REITs earned 14.0% a year against ≈8.3–8.4% for the appraisal-based series. Only "almost disappears after adjustment" belongs to the 1980–2012 exhibit. | (AQR PDF, row 7) |
| 31 | BREIT requests first exceeded its limits in Nov-2022; it filled ≈52% in Dec-2023, 88% in Jan-2024 and 100% ($961m) in Feb-2024 | Confirmed | Verbatim (Bisnow, 1 Mar 2024). The 2% / 5% caps are not in this article; the dossier flags them as via search summary. | https://www.bisnow.com/national/news/capital-markets/breit-fulfills-all-redemption-requests-for-first-time-in-more-than-a-year-123143 |
| 32 | CalPERS real assets returned 6.3% in FY2025-26 (private assets lagged a quarter). TPA launched July 2026 against a 75/25 reference portfolio | Confirmed | Release of 13 Jul 2026; the board approved TPA in Nov 2025. | https://www.calpers.ca.gov/newsroom/calpers-news/2026/calpers-posts-preliminary-investment-return-for-fiscal-year-2025-26 |
| 33 | CPP sold Greenway Plaza "with no net proceeds" in fiscal 2026 | Unverifiable | The dossier gives no source. Bisnow (10 Apr 2026) reports a *receivership* sale to Interra after the CPP / Nuveen / Silverpeak venture could not refinance a $465m loan in May 2022. That is consistent with zero equity recovery, but the quoted phrase was not found. The fiscal-2026 dating is also unconfirmed (CPP's year ends 31 March; the report is dated April). | https://www.bisnow.com/news/houston/office/interra-buys-45m-sf-greenway-plaza-office-campus-receivership-sale-134074 |
| 34 | NFI-ODCE queue ≈12% at 3Q25 (Accordant, via search summary) | Unverifiable | Not in the Accordant Q1-2026 article, and no 3Q25 queue figure was found in session. Not load-bearing, as the dossier flags. | (Accordant URL, row 5) |
| 35 | All [I-calc] numbers reproduce: cash map, ladder, queue machine, true-value impacts, public checks | Confirmed | A re-run of an untouched copy of `g15_ra_calcs.py` reproduces `g15_ra_results.json` exactly (**0 differences**). The dossier text matches the JSON to rounding. | `research/groups/addenda/G15_calcs/g15_ra_results.json` |
| 36 | Look-through LTV 49% ($17.4bn of debt on $18bn of equity); ≈$3.0bn matures a year; at 100% in T5 it uses 65% of $26.6bn | Confirmed (arithmetic; SYNTHETIC) | GAV 35.43, debt 17.43, LTV 49.2%; 0.17 × 17.43 = 2.96; 17.43 / 26.6 = 65.5%. | (script re-run) |
| 37 | "Lagged reported marks fall by only ≈$2.7bn, about a third of the true loss" (T4′, 12 months; §1 finding 6) | **Corrected** | **The $2.7bn comes from hard-coded equity mark paths (`T4_MARKS`), not from the dossier's own Geltner specification** (φ_q 0.65 / 0.6 / 0.5). Applied to the same true-value path, the specification gives **≈$4.9bn, ≈67% of the $7.35bn true loss**. See R4. *SYNTHETIC.* | `G15_ra_verify_checks.py` |
| 38 | GCC real estate lags oil by 2–6 quarters through the fiscal and credit channels (§2.5; spec §7.7) | **Corrected** | **The dossier's own lead-lag peaks at 0–1 quarter** (0.32–0.36) and decays to 0.16–0.22 at 3–4 quarters. No lag is significant (t ≤ 1.65, n_eff ≈ 20). The data support "0–2 quarters, weak". See R5. | https://fred.stlouisfed.org/series/QAEN628BIS |
| 39 | The queue machine "reproduces 2022–26 queues" (§3 methods table) | **Refuted (as stated)** | **The script contains no fit or backtest against the 2022–26 path** (19.3% → 16.4% → ≈10%); the parameters are set by hand. The drought calibration's own steady state is a 3.75% queue. See R8. | `g15_ra_calcs.py` (QUEUE_STATES) |
| 40 | For fund sleeves, "cures come through calls or income cuts" (§6.3) | **Refuted (not implemented)** | **The engine applies cures only to `direct=True` sleeves.** Fund calls stay at canonical rates on unfunded, and income factors do not depend on LTV. Applying the dossier's own cure formula to fund sleeves adds **$0.22bn (12m) and $0.54bn (24m)** of T4′ refinancing shortfall, mostly closed-end VA/opp RE. See R1. *SYNTHETIC.* | `G15_ra_verify_fund_cures.py` |

---

## 3. Citation check

Each reference was checked on Crossref and OpenAlex (DOI resolution, authors, year, title, venue, volume and pages), and the abstract against the use made of it.

| Reference (as cited) | Verified metadata | Status |
|---|---|---|
| Andonov, Kräussl & Rauh (2021), *RFS* 34(8), 3880–3934 | "Institutional Investors and Infrastructure Investing"; online 20 Apr 2021 | ✓ The abstract supports both uses (§4.2 and §5.2). |
| Couts, Gonçalves & Rossi (2024), *RFS* 37(7), 2110–2155 | "Unsmoothing Returns of Illiquid Funds"; online 9 Mar 2024 | ✓ Abstract: "common source of spurious autocorrelation not fully resolved by traditional unsmoothing ... average illiquid fund alpha is lower than previously thought". Applied to hedge funds and private commercial real-estate funds. |
| Hoesli, Lizieri & MacGregor (2008), *JREFE* 36(2), 183–206 | Exact title as cited; online 21 Jul 2007 | ✓ The "δ near 1" gloss in §2.2 is not in the abstract. |
| Rödel & Rothballer (2012), *JAI* 15(1), 110–123 | "Infrastructure as Hedge against Inflation—Fact or Fantasy?" | ✓ |
| Wurstbauer & Schäfers (2015), *JPIF* 33(1), 19–44 | Exact title as cited | ✓ The abstract supports "only direct infrastructure provides a partial [short-run] hedge" and long-run co-movement (US, 1991–2013). |
| Muckenhaupt, Hoesli & Zhu (2025), *JREFE* 70(2), 189–239 | "Listed Real Estate as an Inflation Hedge Across Regimes"; online 16 Oct 2023 | ✓ The finding is about *listed* RE (US 1975–2023), which §2.2 should say. |
| **Pagliari (2017), *REE* 45(1), 75–132**, cited for capex ≈ ⅓ NOI "as used by AQR" | The *REE* paper exists ("Another Take on Real Estate's Role in Mixed-Asset Portfolio Allocations", online 13 Feb 2016), but its abstract is about allocation, not capex | **✗ Wrong paper.** AQR's reference is **Pagliari, J. L. Jr. (2017), "Some Thoughts on Real Estate Pricing", *Journal of Portfolio Management* 43(6), 44–61, doi:10.3905/jpm.2017.43.6.044** (AQR misprints the volume as "34(6)"). |
| Andonov, Eichholtz & Kok (2015), *JFM* 22, 73–103 | Exact title as cited | ✓ RePEc abstract: "increases costs and disproportionally reduces returns"; larger funds invest internally, with "lower costs, and higher net returns". |
| Fama & Schwert (1977), *JFE* 5(2), 115–146 | "Asset returns and inflation" | ✓ Metadata only; the classic result is stated from the literature, as the dossier says. |
| Geltner (1991), *JREFE* 4(3), 327–345; Geltner (1993), *JRER* 8(3), 325–345 | Exact titles as cited | ✓ |
| Gupta & Van Nieuwerburgh (2021), *Journal of Finance* (NBER w26514) | *JF* 76(6), 3255–3307, doi:10.1111/jofi.13073 | ✓ Add volume and pages. The −17¢ / −10¢ figures are from the NBER version. |
| Neville, Draaisma, Funnell, Harvey & Van Hemert (2021), *JPM* 47(8), 8–37 | doi:10.3905/jpm.2021.1.274 | ✓ The dossier links SSRN 3813202; give the DOI. |
| Diamond & Dybvig (1983); Baumol & Fabian (1964); Scharfstein & Stein (2000); Flyvbjerg, Skamris Holm & Buhl (2005) | *JPE* 91(3):401–419; *Mgmt Sci* 11(1):1–32; *JF* 55(6):2537–2564; *JAPA* 71(2):131–146 | ✓ Flyvbjerg's full title adds ": The Case of Transportation". |
| **Missing:** Stein (1997), cited in §2.6 | *JF* 52(1), 111–133, "Internal Capital Markets and the Competition for Corporate Resources" | Add to §10. |
| **Missing:** Getmansky–Lo–Makarov, cited in §3 | *JFE* 74(3), 529–609 (2004), doi:10.1016/j.jfineco.2004.04.001 | Add to §10. |

**Practitioner and peer citations:**
- **Callan:** the page is titled "Private Real Estate Valuations May Have Bottomed; REITs Fall" (Iman & Quach, 20 Feb 2025), not "4Q24 Real Estate Performance: Highlights and Key Issues".
- **PGIM:** the title is "Direct Infrastructure Equity: Performance, Return Attribution, & Inflation Resilience".
- **NBIM:** the 7% / 2% limits are not on the fund-value page. Cite the 2023 submission.
- **ADIA:** cite the 2025 Review for the new ranges, because the investments page still shows the old ones.
- **Ares:** the article gives no data source or vehicle type for the 7%.
- **The National:** "2027–28" is not in the article.
- **CPP Greenway Plaza:** no source is given.

---

## 4. Reasoning issues and overclaims (design implications and specification card)

### R1 (High): fund-level refinancing stress is claimed but not modelled
- **What the dossier says.**
  - §6.3: "In closed-end and open-end funds, cures come through calls or income cuts".
  - The T4′ drain is −$2.46bn over 24 months.
  - Finding 2: "RA helps in T4′, modestly", with relief of $0.2–1.3bn against PE.
- **Problem.**
  - `run_book` computes cures only where `direct=True`.
  - Fund calls are the canonical λ×1.38 on unfunded.
  - Income factors (×0.85 / 0.92 / 0.60) are sector-wide and do not depend on LTV or maturities.
  - So the closed-end VA/opp real-estate sleeve (60% look-through LTV, ≈80% after the T4′ shock) carries **no refinancing consequence at all**.
- **Evidence.** The dossier's own cure formula, applied to fund sleeves, gives **$0.219bn (12m) and $0.536bn (24m)**:
  - closed-end RE $0.18bn / $0.41bn;
  - closed-end infrastructure $0.03bn / $0.10bn;
  - total ≈1.5× the modelled direct-sleeve cures ($0.13bn / $0.36bn).
- **Consequence.**
  - The lower bound of the claimed T4′ relief against PE at the same unfunded is **$0.23bn over 24 months**, which is smaller than the omitted term.
  - The shortfall may appear as protective calls (bounded by unfunded, partly overlapping the ×1.38), as suspended distributions or as NAV loss. Either way, it must be modelled, or ×1.38 must be stated to include it.
- **Fix.**
  - Add a fund-level refinancing module: shortfall → calls up to unfunded → distribution stop → NAV loss.
  - Restate finding 2's relief as a range that includes zero.

### R2 (High): the leverage limits cannot hold in stress, and most of the book is outside ADIC's control
- **What the dossier says.** IC implication (d) and §6.7 set four limits: look-through LTV ≤ 50%; any directly held asset ≤ 60%; ≤ 25% of RA debt maturing within 12 months; unhedged floating ≤ 30%.
- **Controllability.**
  - 63% of RA NAV sits in open- and closed-end funds, whose leverage, maturities and hedges are set by GPs.
  - Co-investment financing is GP-controlled.
  - ADIC can enforce these limits only at commitment (manager selection, LPA leverage caps) and when refinancing its own JV and direct assets.
- **Feasibility.** Under the dossier's own T4′ true-value shock, debt fixed:
  - look-through LTV rises from **49.2% to ≈61.6%** ($17.3bn of debt on $28.1bn of true GAV);
  - sleeve LTVs reach ≈80% (closed-end VA/opp RE and RE co-investment), ≈64% (GCC JV), ≈62% (infrastructure) and ≈60% (global JV).
  - Both limits are breached exactly when the only remedies are cures or fire sales at 0.475–0.86 of reported NAV (the §6.5 T4′ prices).
  - An optimizer that treats them as hard constraints either becomes infeasible or is pushed into SELL at the worst prices.
- **Fix.**
  - Specify them as origination and commitment tests on reported values, with a stress-breach protocol: no forced SELL, a cure-versus-handback decision, and true LTV reported as a monitored metric.
  - Apply the maturity-wall and hedging limits to JV and direct debt only. For funds, make them manager-selection criteria.

### R3 (Medium-High): some actions are not available to ADIC as specified
- **Cash-out refinancing ($0.90bn) and JV sell-down ($2.51bn, normal) are computed on every `direct=True` sleeve.** These include:
  - the GP-controlled RE co-investment sleeve (§6.1: "GP-controlled exits");
  - the infrastructure and energy "direct/co-investment" sleeves ("Partner-led exits").
- As a minority co-investor, ADIC cannot initiate a refinancing or a JV sell-down; it can only sell its stake, which is already a SELL route. On the synthetic book:
  - ≈$0.30bn of JV capacity sits on the RE co-investment sleeve, and up to ≈$1.1bn more on the mixed infrastructure and energy sleeves;
  - ≈$0.37bn of the cash-out capacity sits on the mixed sleeves.
- **Equity cures on the RE co-investment sleeve are 43% (12m) and 36% (24m) of the modelled T4′ cures.**
  - For GP-led deals ADIC's participation is optional (it accepts dilution otherwise).
  - Counting "expected cures at T4′: $0.36bn" as contingent recourse in T5 (§6.7) is prudent, but it conflicts with §7.4's own cure-versus-handback option. Pick one treatment.
- **"JV sell-down ... keeping control and fees" (§6.6).** Fee retention applies only where ADIC, or an ADIC-owned platform, is the managing partner (the CPP model). The user described JVs with operating partners, in which ADIC pays fees.
- **Fix.**
  - Make the `control` field (ADIC / partner / GP) a hard gate on REFINANCE, LEVER and JV sell-down.
  - Route co-investments to SELL (stake secondary) or HOLD only.

### R4 (Medium): the reported-versus-true marks contradict the dossier's own smoothing model
- **Finding 6:** under T4′, true RA equity falls by ≈$7.3bn, while "lagged reported marks fall by only ≈$2.7bn, about a third of the true loss".
- **The mismatch.**
  - The $2.7bn comes from the hard-coded equity mark paths in `T4_MARKS`.
  - Applying the dossier's own φ_q (0.65 real estate, 0.6 infrastructure, 0.5 energy; §6.3 and spec card) to the same true-value path, as appraisal smoothing of asset value with debt fixed, gives **≈$4.9bn (67%) after four quarters**.
  - The script's marks capture 30–45% by sector. Reproducing "a third" needs φ ≈ 0.85.
- **Why it matters.** The figure feeds:
  - the denominator-effect narrative (§2.3c);
  - stale-mark haircuts;
  - the "price per $ of reported NAV" used in SELL.
- **Fix.** Either generate reported marks from the Geltner equation, or justify a stress φ explicitly and carry it into the spec card.

### R5 (Medium): the oil-lag specification is not supported by the dossier's own data
- §2.5 says both Gulf channels "lag oil by 2–6 quarters", and §7.7 tells the build to "include a lag of 2–6 quarters for GCC real estate".
- The dossier's own lead-lag table (§4.7, reproduced) **peaks at L = 1 (0.36)** and falls to 0.16–0.22 at L = 3–4.
- With overlapping windows (n_eff ≈ 20), t ≈ 0.7–1.65, so **no lag is significant**.
- **Fix:** present the lag as a prior with a 0–6-quarter range, and estimate it on ADIC asset data and stream-03 fiscal series.

### R6 (Medium): the inflation-hedge claim is stronger than the evidence
"An inflation hedge, but only through infrastructure" (bottom line; IC implication (b)) rests on three things:
1. **MSCI private infrastructure +19.1% real over 2023–25.**
   - The window excludes 2022 (CPI 6.45%) and spans years of 2.7–3.4% inflation.
   - The returns are appraisal-smoothed.
   - It is set against ODCE −17.7% over a *different* window, 2022–24, which contains both the inflation spike and the rate shock.
2. **The PGIM / EDHECinfra regime split,** which has CPI ≥ 4% in only about 8–9 of 20 quarters, all from one episode.
3. **The literature.** Rödel & Rothballer find listed infrastructure is *no better than equities*, and Wurstbauer & Schäfers find only a *partial* short-run hedge for direct infrastructure.

The evidence supports "contract-dependent partial pass-through (β_π < 1)", which is what the §6.3 β_π table already assumes. It does not support "hedge". The cross-window comparison should be dropped or put on the same years.

### R7 (Medium): the return-cost estimate uses CMAs that do not fit the book
- The ≈26bp ($0.47bn) cost compares PE at 10.2% (2026 LTCMA) with J.P. Morgan's **global core** real estate (7.9%) and **global infrastructure** (7.1%).
- But the synthetic book has 49% look-through LTV, 37% in closed-end VA/opp and core-plus/value-add funds, and 14% in energy & NR.
- The energy return needed to reproduce 26bp is ≈8%, and it is not stated (6% → 29bp; 9% → 25bp).
- A return consistent with the book's strategy and leverage would be higher, so **the cost is probably overstated**. The mixed-edition caveat in §8 does not cover this.
- **Fix:** use strategy-matched CMAs (core / value-add / energy) on levered terms, or present the cost as a range.

### R8 (Low-Medium): queue machine
- §3 says the machine "reproduces 2022–26 queues", but no fit or backtest exists (claim 39).
- The §6.3 formula omits the update of ADIC's request $R_k$. It also applies pro-rata payment to $Q_k$, whereas the code applies rescissions and new requests first.
- §2.4's first-mover argument is muddled. Under pro-rata payment, lodging early helps only by joining more payment rounds; FIFO queues, which some ODCE funds use, behave differently.
- A large redemption notice from ADIC (6% of a fund in the model) can itself move other investors and carries relationship costs. Both should be priced in the notice rule.

### R9 (Low): beta mix-up
- §6.8 sets "infrastructure ≈0.5–0.6 against equities".
- MSCI's 0.6 is a beta to a **50/40/10 multi-asset portfolio**, for an **unlevered** sleeve. It is neither an equity beta nor applicable to a book at 50–55% LTV.
- Use the dossier-04 equity-beta defaults, adjusted for leverage.

### R10 (Low): presentation and parameter scope
- **Ladder table (§6.5):** it omits the real-estate co-investment row (12-month cash 0.25 / 0.15 / 0.00 / 0.15 in normal / drought / T4′ / SG), although the 9.02 / 4.31 / 0.92 / 3.60 totals include it.
- **ODCE vs NAREIT "6.9% vs 9.6%":** this is not a volatility comparison (claim 25).
- **MBA's 17%** is a 2026 snapshot of US CRE mortgages, inflated by extensions. Applying it as a steady-state maturity rate to infrastructure and energy debt is an [I] choice and should be labelled so.
- **Spec card:** the cure formula uses $V^{mat}$ without defining it (§6.3 defines it as $D^{mat}/LTV_0$).

**What holds up.**
- The synthetic labelling is consistent throughout.
- The JV sell-down classification problem is correctly flagged for the user.
- Search-summary facts are flagged and kept out of load-bearing positions.
- The core equations are correct:
  - equity cash yield $y^E=((1-\kappa)c-LTV\cdot i)/(1-LTV)$, with the worked example's 2.2%;
  - the positive-leverage condition $(1-\kappa)c>i$;
  - the Gordon duration (≈20% for +100bp at c = 4.6%);
  - the Geltner variance ratio $(1-\phi)/(1+\phi)$;
  - the T4′ / S1 factors (0.108, 1.38, 0.318).

---

## 5. Reproducibility and arithmetic checks

- **Re-run:** `g15_ra_calcs.py`, copied untouched, reproduces `g15_ra_results.json` with **0 differences**.
- **Cash map** (SYNTHETIC): every figure in the dossier's cash-map tables matches the JSON, including:
  - normal +0.40, drought −0.16, S1 −1.14;
  - T4′ −1.32 (12m) and −2.46 (24m: distributions 1.23, calls 3.33, cures 0.36);
  - the pacing stop −1.65 and calls ×1.0 −0.84 / −1.70;
  - SG / GW −0.30 / −0.12 (24m −0.54 / −0.11);
  - the PE-rate rows (+0.76, −1.55 / −2.69; at U/NAV 0.32: +0.30, −2.23 / −3.76).
- **Ladder and REFINANCE** (SYNTHETIC):
  - SELL totals 9.02 / 4.31 / 0.92 / 3.60;
  - queue machine 7% / 27% / 49% (drought) and 3% / 10% / 26% (T4′);
  - cash-out $0.90bn, and JV $2.51bn / $1.06bn (T4′).
  - The §6.5 table rows sum to 8.76 in normal markets; the missing 0.25 is the RE co-investment row (R10).
- **Public-data arithmetic:**
  - Real returns: ODCE −17.7% (2022–24), MSCI RE −14.2% and infrastructure +19.1% (2023–25).
  - Annual real returns recompute exactly from FRED CPI and the MSCI and NCREIF figures.
  - The 2024 and 2025 ODCE annual returns (−1.43%, 3.79%) match the NCREIF releases. The 2022 and 2023 figures (7.46%, −12.04%) are compounded from the script's rounded quarterly inputs, which also match the 2Q-2026 webinar for 3Q25–2Q26; they agree to rounding with NCREIF's published ≈7.5% and ≈−12.0%.
- **Queue calibration:** 19.9 / 227.3 = 8.75%; less 4% income = 4.75% a year ≈ 1.19% a quarter ✓.
- **Leverage:** look-through LTV 49.2%; maturities $2.96bn a year; T5 usage 65.5% ✓.
- **Return cost:** 26bp requires an unstated ≈8% energy & NR return (R7).

---

## 6. Overall reliability

**MEDIUM.**
- **Sourced facts: high.** Every flagged market, peer and academic claim is confirmed. The corrections concern scope or wording (the vehicle type behind Ares's 7%; ADIA's range "lowered", not "narrowed"; the window of AQR's REIT gap), and there is one wrong reference (Pagliari).
- **Design layer: medium.** Four issues touch IC-facing conclusions and must be fixed before the IC pack:
  1. **R1:** model fund-level refinancing, and restate finding 2's T4′ relief as a range that includes zero.
  2. **R2:** recast the LTV, maturity and hedging limits as origination tests with a stress-breach protocol, applied to controllable assets.
  3. **R3:** gate REFINANCE, LEVER, JV sell-down and cures on `control`, removing co-investment capacity.
  4. **R4:** regenerate reported marks from the stated Geltner φ, or justify a stress φ, and restate the "≈⅓ of the true loss" message.
- **Second-tier fixes:** R5–R7 (oil lag; inflation-hedge wording and windows; strategy-matched CMAs) and the citation fixes in §3.
