# G9 verification log: Synthetic data with a known ground truth

*Adversarial fact-check of `research/groups/dossiers/G9_synthetic_data.md`. As of 2026-10-18. The dossier was not edited.*

## 1. Summary

- **Scope.** I checked 27 empirical claims: the author's 18 flagged claims and 9 more that are load-bearing or looked suspicious. I also checked 14 references and reviewed the design implications and the specification card (§1, §4.10, §6.2–§6.9).
- **Method.** Primary PDFs were downloaded and parsed locally with pypdf: BGK (NBER w22493), HJK (w17874), Gompers et al. (w22587), GLM (w9571), Campbell–Sharpe (FEDS 2007-12), the Cambridge Associates 2019 benchmark book, SEC Private Funds Statistics Q3-2025, MSCI Q2-2026, the CPP F2025 Annual Report, Jefferies July 2026 and the Korteweg–Sorensen accepted version. Press releases and web pages were fetched directly. I recomputed three derived statistics from raw data: the CA vintage dispersion, MOVE and VIX. Citations were also checked with the Consensus paper search.
- **Result: the numbers are very accurate.** Of the 27 claims:
  - 24 are confirmed, most of them to the exact digit. That includes BGK Table 1, GLM Table 10, Form PF Tables 8.13 and 8.22–8.24, MSCI, CPP, NACUBO, MOVE and VIX.
  - 2 need correction. One is a sample label: BGK's funds are USD-denominated, not US-only. The other is the context of BGK's "2.6pp typical distortion".
  - 1 is unverifiable: the Partners Capital whitepaper, whose URL was not captured.
  - None is refuted.
- **Result: the design layer has several material problems.**
  - The exec-summary claim that ADIC's unfunded "matches" the normal-regime Takahashi–Alexander (TA) steady state uses the wrong denominator.
  - The private-credit PD/LGD calibration contradicts its own V12 gate.
  - The vintage-alpha term has a scale error.
  - Index-level GLM smoothing is applied to individual funds.
  - Some REFINANCE and SELL actions are GP-level products that an LP cannot take on its own.
  - The 2.6pp figure is misused in the NAV-manipulation module.
- **Overall reliability: HIGH for the empirical claims, MEDIUM for the design implications.** Fix the items in §4 before the specification card reaches the IC.

## 2. Claims table

**Verdict key.**
- **C**: confirmed.
- **Corr**: corrected.
- **R**: refuted.
- **U**: unverifiable.

### 2.1 Author-flagged claims

| # | Claim (dossier) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | Resolved **US** buyout funds (Burgiss): net TVPI p5/p25/p50/p75/p95 = 0.60/1.18/1.56/2.03/3.38 (mean 1.72); KS-PME 0.48/0.89/1.22/1.53/2.16 (mean 1.27); IRR median 11.29%, mean 13.63%, SD 18.62 | **Corr** (label only) | Every number matches BGK Table 1 exactly. The sample is **USD-denominated** buyout funds, not US funds: 997 in total, of which 641 focus on North America. "Resolved" means NAV < 2% of commitment, with data to March 2012. The same mislabel appears in the docstring of `g9_prototype.py`. | https://www.nber.org/system/files/working_papers/w22493/w22493.pdf (p.9; Table 1, p.41) |
| 2 | Resolved VC funds: TVPI 0.31/0.72/1.19/1.98/5.87; IRR median 3.46%; KS-PME median 0.80 | **C** | Exact match to BGK Table 1. The VC mean TVPI is 2.00 and the mean KS-PME 1.26, also as stated in §4.1. 910 of the 1,074 VC funds focus on North America. | same as #1 |
| 3 | The "typical PE NAV reporting distortion **around fundraising** is ≈2.6pp of quarterly returns". It reaches nearly 5pp for a fund 2 SD below peers after 5 years without a new fund, and about 1pp for top performers. Inflating managers "rarely" raise a next fund | **Corr** (context) | The quote is accurate, but BGK's 2.6pp is the **one-SD peer-chasing reversion** (coefficient −0.205 × SD 0.13). It is symmetric: funds above their peers report lower returns and funds below report higher. It is not specific to fundraising windows. "Nearly 5pp" and "about 1pp" come from model (ii) and apply to buyout funds 2 SD **below** or **above** peers after five years without a new fund; the authors say VC magnitudes are similar. The abstract says such managers are "unlikely to raise a next fund", so "rarely" overstates it. | same as #1 (pp. 25–26, fn. 25; abstract) |
| 4 | HJK (Burgiss): average buyout PME 1.20 (median 1.11) vs the S&P 500; Long–Nickels excess return 6.6% (median 3.4%); LP-sourced data from over 200 investment programs | **C** | Exact match to the WP text (pp. 16–17). Capital-weighted LN excess return is 3.7% (median 3.0%). The data cover "over 200 investment programs" and over $1tn committed. | https://www.nber.org/system/files/working_papers/w17874/w17874.pdf |
| 5 | VC required IRR averages 31%; required multiple mean 5.5, median 5; marketed net IRR about 24% (median 20%) and 3.5x; only 1 in 10 analyze past decisions quantitatively | **C** | All exact, and 885 VCs at 681 firms and "93% expect to beat the public markets" also check out. The 31% applies to respondents who use IRR, and the authors note that early-stage IRRs may be "if successful" figures. The dossier already treats it as a hurdle. | https://www.nber.org/system/files/working_papers/w22587/w22587.pdf |
| 6 | CA US PE (31 Dec 2019): SD of ln pooled TVPI over 1995–2010 vintages = 0.139; vintage component ≈ 0.13 after removing noise of ≈0.05 (ICC ≈ 0.12); within-vintage σ ≈ 0.35 for 2000–2010 vintages | **C** (reproduced) | Recomputed from the CA TVPI table (book p.16): SD of ln pooled TVPI **0.1388**; within-vintage σ from the IQR **0.35** for 2000–10 (range 0.23–0.40); noise σ_w/√n ≈ **0.057**; vintage component **0.127**; ICC **0.11**. **Caveats.** Pooled TVPI is capital-weighted, so the effective n is below the fund count. With n_eff at half to a third of the count, the vintage component falls to 0.10–0.11 and the ICC to 0.07–0.09. The 2009–10 vintages are still largely unrealized (RVPI 0.84 and 0.48). Script: `g9verify\scripts\ca_calc.py`. | https://www.cambridgeassociates.com/wp-content/uploads/2020/06/WEB-2019-Q4-USPE-legacy-Benchmark-Book.pdf |
| 7 | MMS consensus forecasts (1990–2006) are anchored toward the previous release with weight "on the order of 30 percent", roughly 20–40% by series | **C** (nuance) | The quote is exact (p.3), and the abstract gives 1990–2006 while the body says 1991–2006. Retail Sales at about 20% is described as "middle of the pack" for change variables, so some series sit below 20%. The maximum is about 40% (Consumer Confidence). The paper was published in *JFQA* in 2009, and its anchoring test is contested by Hess & Orbe (2013, *Review of Finance*). | https://www.federalreserve.gov/pubs/feds/2007/200712/200712pap.pdf |
| 8 | GLM, CSFB/Tremont indices: ρ₁ = 56.6% (convertible arbitrage), 39.6 (fixed-income arbitrage), 34.8 (event-driven), 29.4 (emerging markets and equity market neutral), 15.9 (long/short), 5.6 (macro), 3.2 (managed futures); θ₀ from 0.49 to 1.04 | **C** | Exact match to GLM Table 10, Jan 1994–Oct 2002, T = 106. Emerging markets and equity market neutral really do both show 29.4%. The paper's text gives 42.6% for convertible arbitrage, but that is a typo for ρ₂; the table value of 56.6% is right. **Design caveat:** these are index-level estimates (see §4, R5). | https://www.nber.org/system/files/working_papers/w9571/w9571.pdf |
| 9 | Form PF Q3-2025: investor liquidity 6.8/19.1/35.0/58.2% within 1/30/90/365 days; portfolio liquidity 61.1% within 30 days; GAV/NAV 8.8 RV, 8.2 macro, 3.3 multi-strategy, 1.9 equity, 1.8 credit; $121bn gated | **C** | Exact match to Tables 8.22, 8.23, 8.13 and 8.24. Also confirmed: may suspend $3,182bn, may gate $2,053bn, side-pocketed $103bn, suspended $25bn, and a Sep-2025 sum of Table 8.1 of about $5.16tn. | https://www.sec.gov/files/investment/private-funds-statistics-2025-q3.pdf |
| 10 | CDLI about 9.46% annualized since 2004; 9.3% in 2025; realized losses about half their 1.0% long-term average | **C** (decimal unverified) | Confirmed in primary releases. The 31 Mar 2026 release gives "9.3% for the calendar year" and "20 years of returns averaging 9.5%". The 19 Aug 2026 release says "Realized losses from defaults remain stable at one-half their 1.0% long-term average", with H1-2026 at 3.0% and trailing twelve months at 7.7%. **The exact 9.46% could not be traced to a primary source**; the releases say "averaging 9.5%". Cite the releases, not a search summary. | https://www.prnewswire.com/news-releases/private-credit-shows-resilience-in-cliffwater-direct-lending-index-data-302854703.html ; https://www.morningstar.com/news/pr-newswire/20260331la23388/cliffwater-direct-lending-index-data-supports-strength-of-private-credit |
| 11 | MSCI Q2-2026: 15,799 funds, US$13.65tn; 2025 returns buyout 10.0%, VC 21.0%, direct lending 10.8%; Q2-2026 VC +12.7%, buyout +2.5% vs ACWI IMI +15.1% | **C** | Exact. The 15,799 is 14,153 funds plus 1,646 funds-of-funds, and the capitalization is US$13,650,903m. Also confirmed: private credit 9.5%, infrastructure 12.6% and private real estate 2.3% in 2025; Q1-2026 buyout −1.1% vs ACWI −2.7%; median entry multiple 11.3x and exit 12.5x; direct lending 12.1/7.5/10.8% for 2023/24/25; PE distribution rate 11/9/11/11% for 2022–25 and 9% in H1-2026. | https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf |
| 12 | CPP F2025: base-CPP recourse leverage 36.3% of net assets (limit 45%); derivatives notional C$724.9bn vs net assets C$714.4bn; unfunded about C$63.4bn (8.9%) | **C** | Exact. Recourse leverage 36.3% against a 45% limit is in Note 10.2. Total derivatives notional is C$724,932m (Note 4.2). Unfunded is C$752m plus C$62,648m, or C$63.4bn, which is 8.87% of net assets (Note 16). | https://www.cppinvestments.com/wp-content/uploads/attachments/CPP-Investments-F2025-Annual-Report-English.pdf |
| 13 | NACUBO FY2025: >$5bn cohort holds 62.5% alternatives and 8.2% fixed income; dollar-weighted PE 16.8%, VC 12.2%, marketable alternatives 15.4%; effective spending 4.9% | **C** | Exact (release of 12 Feb 2026). Also confirmed: public equity 31.5% and US equity 13.7%. | https://www.nacubo.org/Press-Releases/2026/US-Higher-Education-Endowments-Report-Stable-Returns-Increase-Spending-to-33-4-Billion-in-FY25 |
| 14 | ILPA Reporting Template v2.0, released Jan 2025, replaces the 2016 template for funds still in their investment period in Q1 2026 or launched on or after 1 Jan 2026; comes with a Performance Template (granular and gross) and a Capital Call & Distribution Template | **C** (nuance) | Confirmed. The Performance Template has a Granular and a Gross Up methodology (v1.1 issued Apr 2025) and is expected for funds commencing on or after 1 Jan 2026. The Capital Call & Distribution Template was "refreshed later in 2025", not released with the others in January. | https://ilpa.org/industry-guidance/templates-standards-model-documents/reporting-template ; https://ilpa.org/industry-guidance/templates-standards-model-documents/updated-ilpa-templates-hub |
| 15 | Buyout NAVs show "little systematic bias"; VC NAVs "relatively aggressively biased", especially since 2000 (384 VC and 195 buyout funds, 1988–2016) | **C** | Confirmed. *The Accounting Review* 95(1):191–210, doi:10.2308/accr-52486, published online July 2019 with the issue dated 2020. | https://ora.ox.ac.uk/objects/uuid:691dbf3a-2fb2-4156-8d12-967cdf89301e |
| 16 | About 75% of buyout exits clear the next-to-last quarterly mark (Bain midyear 2026, citing MSCI) | **C** | Bain's wording: "roughly 75% of buyout **assets** are still exiting above their next-to-last quarterly mark" (8 Jun 2026, MSCI analysis). This is a company-level statistic subject to exit selection. | https://www.prnewswire.com/news-releases/winning-firms-will-focus-on-what-they-can-control-weather-the-rest-as-triple-shock-brakes-private-equitys-latest-revival-bain--company-2026-midyear-pe-report-302793107.html |
| 17 | MOVE monthly closes, Dec 2002 to 16 Oct 2026: median 80, p90 125, p95 141, p99 192; maximum 214 (Nov 2008); latest 101 | **C** (reproduced) | Recomputed from Yahoo ^MOVE: median 80.0, p75 103.9, p90 125.2, p95 140.7, p99 192.2, maximum 214.0 (Nov 2008), share of months above 120 = 12.5%, 2022/23 means of monthly closes 120.3/118.2, latest 101.1. The daily peak of **264.6 on 10 Oct 2008**, which the dossier flagged as unverified, is confirmed in the daily series. The cited ICE page describes the index and does not hold the data. Script: `g9verify\scripts\move_check.py`. | https://query1.finance.yahoo.com/v8/finance/chart/%5EMOVE (data); https://developer.ice.com/fixed-income-data-services/catalog/ice-data-indices-move-index |
| 18 | SBC validates Bayesian computation through uniform ranks; data-dependent test quantities, especially the joint data log-likelihood, extend its sensitivity | **C** (wording) | The abstract says "the joint likelihood of the data is an especially useful test quantity". It also says earlier implementations could never detect cases "when the posterior is equal to the prior". Ranks are invariant to taking logs, so the likelihood/log-likelihood difference does not matter. Published in *Bayesian Analysis*, doi:10.1214/23-BA1404. | https://arxiv.org/abs/2211.02383 |

### 2.2 Additional claims selected by the checker

| # | Claim (dossier) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 19 | VIX, 1990 to 16 Oct 2026: mean 19.4, median 17.6, p95 32.9, p99 46.7 | **C** (reproduced) | Yahoo ^VIX daily closes give 19.43 / 17.57 / 32.90 / 46.71. Script: `g9verify\scripts\vix_check.py`. | https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX |
| 20 | Jefferies H1-2026 LP pricing: buyout about 91%, VC 79%, credit 89%, RE 68%; funds under 5 years at single-digit discounts; tail-end at 25%+ discounts; 26% of deals with deferrals | **C** | Exact. Deferrals are "26% of all LP sales". Infrastructure is 91% and the all-strategy average 87%. | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 21 | Korteweg–Sorensen firm-level spread σ ≈ 6% | **C** | Their "spread" is the interquartile range q75 − q25 of expected returns, 7–8pp a year (6.60% for VC). That gives σ ≈ 7.5/1.349 ≈ 5.2–5.9%. *JFE* 124(3):535–562 (2017). | https://research-api.cbs.dk/ws/files/55394727/morten_soerensen_skill_and_luck_in_private_equity_performance_acceptedversion.pdf |
| 22 | Secondary buyers out-earn sellers by about 5pp a year in PME terms (Nadauld et al.) | **C** | Buyer PME 1.023 vs seller 0.976, "5 percentage points annually". *JFE* 2019, doi:10.1016/j.jfineco.2018.11.007. | https://doi.org/10.1016/j.jfineco.2018.11.007 |
| 23 | Executives' 80% intervals cover outcomes 36% of the time | **C** | Ben-David, Graham & Harvey, *QJE* 2013, "Managerial Miscalibration". | https://doi.org/10.2139/ssrn.1640552 |
| 24 | BGK: share of follow-on fundraisers in the top vs bottom interim tercile is 44.7% vs 18.8% (buyout) and 42% vs 22.9% (VC); about 10% of top funds at life-end were bottom tercile during fundraising | **C** | Exact (BGK p.13 and Table 3). Still-alive TVPI quartiles 1.00/1.18/1.35 (buyout) and 0.88/1.11/1.35 (VC) at a mean age of 5.3y also match. | NBER w22493 (as #1) |
| 25 | HJK: VC PME < 1 for 1999–2008 vintages except 2005 | **C** | "Except for 2005, none of those vintages have a weighted average or simple average PME greater than 1.0." | NBER w17874 (as #4) |
| 26 | Harvard FY2026 payout $2.6bn on $56.9bn; Yale FY2025 $2.1bn; ADIA 2025 ranges PE 15–20%, financial alternatives 7–12%, real estate 2–7% | **C** | All confirmed. Harvard's endowment was $68bn at FYE2026, so 4.6% is on a beginning-of-year basis and 3.8% on year-end. | https://www.harvardmagazine.com/university-finances/harvard-endowment-financial-report-fiscal-year-2026 ; https://news.yale.edu/2025/10/24/yale-reports-investment-return-fiscal-2025 ; https://www.adia.ae/en/pr/2025a/index.html |
| 27 | Partners Capital stress model gives a 40–50% maximum illiquid allocation for a typical endowment | **U** | No URL or title was captured, and I could not trace it. Do not present it to the IC as sourced. | — |

**Not re-checked (inherited from other streams):**
- the weekly BGG λ = 0.951 (the arithmetic 0.951¹³ ≈ 0.52 is correct) and NAV noise of 4.6%;
- the C3 VIX thresholds and the stream-09 VRP and SKEW figures;
- OTPP notional/assets of 3.1x;
- "secondary funds settle into their final quartile in 5–7 years (CA 2018)". The CA 2019 book states only that "most funds take at least six years to settle into their final quartile".

## 3. Citation check (the 14 most important references)

| Reference | Exists? | Authors / year / title / venue correct? | Notes |
|---|---|---|---|
| Brown, Gredil & Kaplan, "Do private equity funds manipulate reported returns?" *JFE* 132(2), 2019; NBER w22493 | Yes | Yes | The "US" sample label is wrong (see #1) |
| Harris, Jenkinson & Kaplan, "Private equity performance: What do we know?" *JF* 69(5):1851–82, 2014; NBER w17874 | Yes | Yes | The cited numbers come from the Feb-2012 WP and match it |
| Gompers, Gornall, Kaplan & Strebulaev, "How do venture capitalists make decisions?" NBER w22587 | Yes | Yes | Supply the volume: *JFE* 135(1):169–190 (2020), doi:10.1016/j.jfineco.2019.06.011 |
| Jenkinson, Landsman, Rountree & Soonawalla, *TAR* 95(1):191–210 | Yes | Yes | Online 2019, issue dated 2020 |
| Getmansky, Lo & Makarov, *JFE* 74(3):529–609, 2004; NBER w9571 | Yes | Yes | — |
| Campbell & Sharpe, FEDS 2007-12 | Yes | Yes | The † can be removed: published in *JFQA* (2009), doi:10.1017/S0022109009090127 |
| Coibion & Gorodnichenko, *AER* 105(8):2644–78, 2015 | Yes | Yes | doi:10.1257/aer.20110306 |
| Bordalo, Gennaioli, Ma & Shleifer, *AER* 110(9):2748–82, 2020; NBER w24932 | Yes | Yes | The WP title is hyphenated ("Over-reaction") |
| Talts, Betancourt, Simpson, Vehtari & Gelman, arXiv:1804.06788 | Yes | Yes | — |
| Cook, Gelman & Rubin, *JCGS* 15(3):675–692, 2006 | Yes | Yes | Also cite **Gelman (2017), "Correction to Cook, Gelman, and Rubin (2006)", *JCGS*, doi:10.1080/10618600.2017.1377082** |
| Modrák et al., *Bayesian Analysis*, doi:10.1214/23-BA1404; arXiv:2211.02383 | Yes | Yes | Eight authors (Modrák, Moon, Kim, Bürkner, Huurre, Faltejsková, Gelman, Vehtari) |
| SEC Private Funds Statistics Q3-2025; MSCI Q2-2026 summary; CPP F2025 AR; CA 2019 benchmark book | Yes | Yes | Table numbers cited correctly |
| Potluru et al., arXiv:2401.00081; Qian, Cebere & van der Schaar, arXiv:2301.07573 | Yes | Yes | No journal reference on either |
| Cliffwater (ref 26) | Partly | — | The CDLI homepage has no extractable figures. Replace the "search summary" with the PR Newswire releases of 31 Mar 2026 and 19 Aug 2026 |

**Other citation problems.**
- The Partners Capital whitepaper has no URL (#27).
- The MOVE source URL does not contain the statistics; cite the data source.
- The ILPA Capital Call & Distribution Template dates from later in 2025, not January 2025.
- Among the items cited from memory (†), the ones I recognize have the correct bibliographic details: Fang–Ivashina–Lerner *JFE* 116(1); Braun–Jenkinson–Schemmerl *JFE* 136(1); Keelin *Decision Analysis* 13(4); Cont *QF* 1(2); Gretton et al. *JMLR* 13; Barras–Scaillet–Wermers *JF* 65(1).

No hallucinated or garbled citations were found.

## 4. Reasoning issues and overclaims (ranked by severity)

**R1. The unfunded steady-state comparison uses the wrong denominator (§1 item 6, §4.10). Material.**
- `g9_prototype.py` E2 is a PE-fund-only TA programme, so its steady-state ratio is unfunded divided by **PE** NAV: 0.37 in the normal regime and 0.24 in drought.
- The dossier compares that ratio with total unfunded over total **private** NAV: 38/106 = 0.36. That denominator includes credit, Capital Solutions and co-investment, which carry little unfunded. On that basis it concludes "matches the normal steady state".
- The dossier's own census gives a PE ratio of **24/52 = 0.46**. That is 1.25× the normal steady state and 1.9× the drought steady state.
- The "about $9bn/yr commitments" inference, by contrast, uses the PE-only $24bn, so the dossier is internally inconsistent.
- **Fix:** say that unfunded is *above* steady state in both regimes, which strengthens the heavy-commitment inference.

**R2. The private-credit loss calibration contradicts its own release gate (§4.6, T6, V12). Material.**
- PD 2.5% × LGD 40% = 1.0% is set as the regime-multiplier-1 (normal) level.
- The spec then multiplies PD by 1.5 in D and 3 in C and adds 15pp to LGD in crisis. That pushes the long-run average above 1%. With illustrative regime shares of N 70%, D 20%, C 10%, the expected loss is about **1.4%/yr**, which fails V12 (0.8–1.2%).
- CDLI's 1.0% long-run average already includes the GFC.
- **Fix:** calibrate the regime-weighted average to 1.0%. With the shares above, that means a normal-regime PD of about 1.8%.

**R3. The vintage-alpha term has a scale error (T2). Material.**
- The spec sets a_v = −0.5·z_v, and z has a stationary SD of about 0.2.
- That implies a vintage-alpha SD of about **10%/yr** from this term alone. That is 2.5× the stated total σ_α ≈ 4%/yr and incompatible with the CA vintage-component target of 0.13 (V4).
- Either z is in different units or the coefficient is per fund life, not per year. Specify which and recalibrate, for example to about −0.05 per year.

**R4. BGK's 2.6pp is misused in the manipulation module (§2.5, §4.3, O1 Δm). Moderate.**
- The 2.6pp is BGK's symmetric one-SD peer-chasing effect, not inflation during fundraising (see #3).
- Δm = min(0.05, 0.013·z_gap·(1 + 0.2·y)) returns 2.6pp at z_gap = 2 and y = 0. But BGK's interaction model implies *persistence*, not inflation, when FundTiming = 0.
- For a fund 2 SD **above** peers after 5 years, BGK implies a +1pp bias, while the formula gives ≤ 0.
- **Fix:** re-anchor the module on BGK model (ii): +5pp at 2 SD below peers after 5 years and +1pp at 2 SD above after 5 years. Treat 2.6pp as the scale of the generic peer reversion.

**R5. Index-level hedge-fund smoothing is applied to individual funds (T7, V10). Moderate.**
- GLM's ρ₁ and θ₀ by strategy come from CSFB/Tremont **indices**. GLM itself warns that "the process of aggregation can change the statistical behavior of any time series".
- Using these as fund-level MA(2) weights, and gating fund-level output against them, conflates aggregation with smoothing.
- **Fix:** use GLM's TASS fund-level estimates (Tables 8 and 9; for example, mean θ₀ by category) for funds, and apply the index targets to the simulated strategy aggregate.

**R6. Some actions are not available to an LP as specified (§4.5, spec card SELL and REFINANCE). Moderate.**
- "Single-fund NAV loan, SOFR + 480–610bp, LTV 5–20%, 50% sweep" and "secondaries-fund facility, SOFR + ≤300–400bp" are **GP-level, fund-level** products. ADIC's Capital Solutions group might *lend* them, but ADIC as an LP cannot put one on a third-party fund.
- The LP equivalents are LP portfolio financing, preferred equity or structured secondaries, and CFOs. They need GP consent to pledge or transfer and are priced differently.
- "Co-investment holdco PIK 12–15%" and exiting via a "CV" are GP-controlled.
- "Credit loan or interest sales at about 89% of NAV" applies Jefferies' *credit-fund LP-interest* pricing to loan-level sales.
- **Fix:** re-specify these actions with LP-accessible instruments, a consent probability and separate pricing.

**R7. The overlay "modest by peer standards" judgement rests on gross notional (§1 item 6, §4.10).**
- CPP's C$724.9bn of notional is mostly FX forwards (C$149bn) and interest-rate swaps (C$252bn).
- CPP itself states that notional amounts "do not necessarily represent the amount of potential market risk".
- The notional of an options-heavy tail-hedge book is not comparable.
- **Fix:** compare delta- or vega-adjusted exposure, stressed VM/IM, or a recourse-leverage-style net notional.

**R8. The anchoring evidence is mapped to the wrong parameter (§2.5, O4).**
- Campbell–Sharpe's ≈30% weight is on the *previous month's release*, a recent realized value. In the generator that corresponds to w_a or ρ_f, not to w_u, the underwriting at inception.
- Combined with ρ_f = 0.6, the immediate weight a PE forecast puts on new oracle information is (1 − 0.6) × 0.5 = **0.2** per quarter. That is much stronger rigidity than the "≈0.3 anchoring" label suggests.
- The C&S test is also contested (Hess & Orbe 2013).
- **Fix:** label w_u as an [I] analogy and document the combined rigidity.

**R9. Overconfidence is not reconciled with the cited evidence (O4).**
- With unbiased normal errors, BGH's 36% coverage of 80% intervals implies κ_conf ≈ 0.37.
- The dossier's κ_conf of 0.45–0.7 implies 44–63% coverage before bias.
- **Fix:** state whether the b^f bias is meant to close the gap, or lower κ_conf.

**R10. The co-investment dispersion back-out is fragile (§4.5).**
- σ_fund = 0.40 is BGK *net* TVPI pooled across vintages. It includes vintage and market dispersion and is compressed by carry.
- The formula also treats fund ln TVPI as an average of deal ln MOICs, whereas a fund's multiple is an arithmetic, value-weighted average of deal multiples.
- σ_deal ≈ 0.77 is a rough [I]. Keep the stated 0.66–1.00 range as the sensitivity, and do not gate on 0.77.

**R11. The tail-end over-mark is inferred from secondary discounts (§4.3).**
- Jefferies' 25%+ tail-end discounts also reflect buyer return hurdles, illiquidity, fees on the residual and adverse selection.
- The discount is not a measure of NAV over-marking. The +12% must remain [I].

**R12. "PME is transportable" holds only when β ≈ 1 (§2.3).**
- KS-PME implicitly assumes β = 1. With the tested β of 0.8–1.2, PME targets also depend on the market path.

**R13. Technical points in T3.**
- E[exp(t₅ shock)] is not finite, so the Gaussian −½σ²Δ correction does not give the intended drift. Truncate the shocks, or use a distribution with a moment-generating function such as NIG.
- The jumps J (0.75%/q × N(−0.35, 0.2²)) subtract about 1%/yr uncompensated. α_s = +3% is therefore "skill" net of about 1% of write-down drift, and should be labeled that way.

**R14. Minor inconsistencies.**
- §1 says the overlay is "about 20–50% of NAV", while §4.10 and §6.2 give $50–90bn = 28–51%.
- The BGK "resolved US buyout" label is repeated in `g9_prototype.py`.
- Some u/b^u values are in IRR points while the table header says "annualized log-return points".

**Checked and correct:**
- n_eff = 64/(1 + 3·0.3) ≈ 34.
- The E3 coverage of 0.757, against an analytic value of 0.767 for ICC 0.3 (0.83 at ICC 0.15, 0.70 at ICC 0.5).
- The E4 χ²₁₉ critical value of 30.1.
- The exit uplift N(0.10, 0.15²), which gives P = 0.75.
- PD × LGD = 1.0% in the normal regime.
- The census arithmetic: 489 holdings plus 6 Treasury sleeves = 495; NAV and unfunded totals; lognormal medians reproduce the group NAVs.
- The co-investment σ_deal grid: 0.66–1.00, central 0.77, P(MOIC < 1) of 19–28% and 22%.

## 5. Overall reliability rating

- **Empirical and sourced claims: HIGH.** 24 of 27 are confirmed, most to the last digit, with 2 corrections of context or label, 1 unverifiable item and none refuted.
- **Design implications and specification card: MEDIUM.** R1–R6 should be fixed before IC use. R1 is an exec-summary statement, R6 affects which actions the IC is told are available, and R2–R3 would make the generator fail its own gates V12 and V4.
- **Overall: HIGH (facts), with the design-layer fixes above required.**

*Reproducibility.* Downloads, extracted text and scripts are in `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g9verify\` (scripts: `ca_calc.py`, `move_check.py`, `vix_check.py`, `pdf2txt.py`).

## Citation corrections (2026-10-18)

- Erratum (§3, Modrák et al. row): this log accepted the dossier's year, 2023, as correct. The article is *Bayesian Analysis* 20(2):461–488 (2025), doi:10.1214/23-BA1404; 2023 is the advance-publication year (literature synthesis §2.3; `G9_synthetic_data.lit.md` §2 row 3). The dossier's ref 16 is now corrected.
