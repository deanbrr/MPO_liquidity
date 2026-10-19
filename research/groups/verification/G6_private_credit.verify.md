# G6 Private Credit: verification log

**Dossier:** `research/groups/dossiers/G6_private_credit.md` (as of 2026-10-18). The dossier was not edited.
**Verification date:** 2026-10-18.
**Scope:**
- 37 empirical claims: all 20 the author flagged, plus 17 others chosen as load-bearing or suspicious.
- 15 references.
- The design implications (§6) and the specification card (§6.11).
- The synthetic model script behind §6.8.

**Method**
- **Primary PDFs:** fetched and text-extracted locally (pypdf), then searched:
  - Cliffwater *2026 Asset Allocation Report*;
  - IMF GFSR Apr-2024 ch.2 and Apr-2026 ch.1;
  - FSB (May 2026);
  - MSCI Q2-2026;
  - Evercore H1-2026;
  - T. Rowe Price/OHA;
  - CDLI fact page;
  - BCBS 238;
  - Proskauer release PDF.
- **Web pages:** fetched directly:
  - GFM, Proskauer, KBRA, PE Wire;
  - Lincoln (Q2-2026 and Q4-2025);
  - PR Newswire (CDLI);
  - two Fed FEDS Notes and the Fed FSR;
  - VRC, ECB;
  - five NBER pages;
  - two BoE pages;
  - iCapital, Fortune, Kadenwood, Moody's;
  - two Wikipedia pages;
  - NY Fed SOFR API and US Treasury yield table.
- **Consensus:** the search tool only, used for two academic citations. No authentication tool was called.
- **Arithmetic:** re-derived independently.
- **Author's script:** read in full. Its JSON output was compared with every §6.8 table, and two sensitivity runs were performed.
- **Constraint:** the session's web-search budget ran out part-way through. After that only direct fetches of known primary URLs were used. Claims that needed a search (for example, the Jefferies pricing series) are marked unverifiable.

---

## 1. Summary

**Sourcing quality is high.**
- Of 37 claims checked: **29 confirmed** (2 from secondary sources only), **4 corrected**, **0 refuted**, **4 unverifiable**.
- No fabricated statistics or hallucinated references were found.
- All 20 author-flagged numbers match their sources. One flagged claim (Proskauer) carries a wrong definition.

**Four factual corrections, all minor to moderate:**
1. **Proskauer** is not "payment and covenant defaults only".
   - It is a loan-count ratio.
   - Beyond payment and covenant defaults, it counts distressed restructurings, bankruptcies, other material defaults and loans modified in anticipation of default.
   - This weakens the dossier's cleanest example of definitions explaining "2.5% vs 6.3%".
2. **The 31% Form PF share** belongs to public and private pensions together, as a share of private-credit fund assets. It is not the share of "U.S. public pensions".
3. **The bad-PIK cohort LTV** (39.4% → 76.1%) comes from Lincoln's Q4-2025 release, not Q1 2026.
4. **The IMF's 2020 reference** is to funding pressure from correlated revolver drawdowns. It does not describe collateral calls on back-leverage.

**The decision economics need rework before the IC.** The largest problems:
- **R1/R2.** The synthetic model treats the whole $14bn as one ADIC-controlled, SMA-like pool. As a result:
  - the run-off uplift ($2.2bn, "12–25% of the payout") is not valid for the actual wrapper mix;
  - the SELL-vs-HOLD break-evens (λ* of 2% / 8% / 21%) are not valid for any actual wrapper;
  - on the SMA sleeve alone the uplift is about $0.8–0.9bn;
  - with the dossier's own loan-sale prices, the SMA SELL/HOLD verdict flips in Normal and Tight.
- **R4.** The script does not implement several documented mechanisms. It also uses a PIK-cohort default hazard about 9× the cash-pay hazard, where the dossier documents ×1.3–1.7. Switching to the documented value cuts the 5-year P99 loss from 17.2% to 12.2%.
- **R3.** DL recoveries of 60–65% in Benign/Normal contradict the dossier's own rule "use 33–55%, not 60–70%".
- **R5.** The claim that the model "reproduces Fitch's 6.3%" is circular.

**Overall reliability: MEDIUM.**
- High for the sourced market and regulatory facts (§4).
- Medium to low for the synthetic decision numbers: §1 items 4, 6 and 8, §6.8, and the spec-card SELL/REFINANCE/LEVER rules.

---

## 2. Claims table

Verdicts are confirmed, corrected, refuted or unverifiable. "F" marks an author-flagged claim.

| # | Claim (dossier §) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| C1 F | Fitch PCDR 6.3% TTM Aug-2026 (record), 6.1% Jul. Events: 47% PIK/deferral, 41% extensions, 8% payment. Healthcare and industrials 9.9%, software 0.6%; <$25m EBITDA 12%; MCO 5.6%, PMR 8.5% (§1, §4.2) | confirmed | All figures match (TTM event shares). "Record" covers a short series: the PCDR began in Aug 2024. The "4% bankruptcy/restructuring" in §4.2 is not in this source (see C36). | https://gfmag.com/private-credit/fed-rate-hike-squeezes-an-already-stressed-private-credit-sector/ |
| C2 F | Proskauer "(payment and covenant defaults only)": 2.51% Q2-26, after 2.73%, 2.46%, 1.84%; 716 loans, $195.6bn (§1, §2.4, §4.2) | **corrected** | Numbers are confirmed; the definition is wrong. Per its latest published methodology (2023), the index is defaulted loans ÷ number of loans. Default is dated to the earliest of: a missed payment; a distressed restructuring; bankruptcy; a financial-covenant default; another material default expected to last >30 days; or a loan modification in anticipation of default. It therefore captures part of what the dossier calls "selective default". The "payment and covenant only" wording comes from a secondary source (Kadenwood). | https://www.proskauer.com/report/proskauers-private-credit-default-index-reveals-rate-of-251-for-q2-2026 ; methodology: https://www.proskauer.com/release/proskauers-q3-2023-private-credit-default-index-highlights-the-resilience-of-private-credit-in-a-turbulent-economy ; Q3-25 (1.84%): https://www.proskauer.com/report/proskauers-private-credit-default-index-reveals-rate-of-184-for-q3-2025 |
| C3 F | KBRA DLD (14 Oct 2026): default 2.0% (from 2.2%), non-accrual 1.8%. LBO spreads S+510–528, +40bp vs the Feb-26 low, 177bp over single-B. Leverage 4.3–4.6×. 3Q26 volume $38.9bn, lowest since 2Q23 | confirmed | Exact. The leverage range omits lower middle market (3.8×). Published 16 Oct. KBRA does not say whether the 2.0% is by count or by dollar, so the "2.3% by count (Jun) → 2.0% (Oct)" decline in §4.2 may compare different bases. | https://www.kbra.com/analytics/products/dld/insights/monthly-insights-and-outlook-at-a-glance-october-14-2026 |
| C4 F | KBRA 2026 forecast 2.5% loan-weighted (1.4% in 2025); 2.3% by count in Jun-26, equal to the late-2023 peak; recoveries to decline further | confirmed | The ~3.5% by count (~111 issuers) in §4.2 is also confirmed. | https://www.privateequitywire.co.uk/private-credit-default-rates-return-to-peak-levels-says-kbra/ |
| C5 F | Lincoln Q2-26: bad PIK 6.2% of loans (5.9% Q1). Covenant defaults 2.7% (six-year average 3.9%). PIK in 11.1% of loans and 11.3% of interest income. Takeovers $22.3bn in H1-26 vs $24.2bn in FY25, 70% from 2021–22 | confirmed | Exact. Also confirms software loans with LTV>50% at 87.1% of par, and the "~9% loss → zero IRR" illustration (see R13). | https://www.lincolninternational.com/news/the-lincoln-private-market-index-earnings-growth-drove-a-q2-rebound-while-private-markets-became-more-selective/ |
| C6 F | CDLI +3.0% H1-26, +7.7% TTM. Realised losses ≈0.5% vs 1.0% long-term. Private $0.98 vs public $0.96. Repayments >6%/qtr. Software −3% in Q1-26 | confirmed | The release states realised losses as "one-half their 1.0% long-term average" (≈0.5% implied). The price date is not explicit in the release. | https://www.prnewswire.com/news-releases/private-credit-shows-resilience-in-cliffwater-direct-lending-index-data-302854703.html |
| C7 F | Cliffwater 2026: SOFR 3.50, spread 5.50, OID 0.50, losses 0.65 (1.30 at 1×), cost of debt 5.50. Net 6.84 / 8.93 / 8.34. 3-yr takeout = 3-yr average life | confirmed | Exhibit 28 (p.20) and the p.19 footnote. The dossier's §2.2 table omits operating expenses (0.25/0.45/0.60%), the BDC fee of 2.50% of NAV, and the +0.80% P/NAV-discount amortisation that produces 8.34%. HY recoveries of 39% (1988–2025) and 36% in 2025 are also confirmed (p.17). | https://www.bdcs.com/docs/CapitalMarketAssumptions.pdf?v=20220116 |
| C8 F | IMF GFSR Apr-2026: about one-fifth of DL loans are software, >50% of NAV in levered vehicles. Selective defaults could rise 2–3× under stressed rates/earnings. Perpetual BDCs last 9–11 quarters (mild) or 5–7 (moderate) | confirmed | Ch.1 p.21 and fn 24. The IMF adds that the horizon is also shorter if funds allow redemptions above 5%. | https://www.imf.org/-/media/files/publications/gfsr/2026/april/english/ch1.pdf |
| C9 F | IMF GFSR Apr-2024 ch.2: $2.1tn (2023, including undeployed capital). BDC D/E 0.8–1.2×, CEF 0–1.3×. Over one-third of PC-like firms with ICR<1. BDC marks react less than B-rated loans, with deviations persisting several quarters | confirmed | PDF pp.3, 8, 12 (Table 2.2) and 14. The 1.27 borrowing-to-assets ratio for the 95th-percentile CEF is also verbatim (p.11, citing the Fed). | https://www.imf.org/-/media/files/publications/gfsr/2024/april/english/ch2.pdf |
| C10 F | Cai & Haque (Feb 2024): ICR ~2.0× vs 2.7× for leveraged loans (2023). Post-default value 33% vs 52% syndicated vs 39% HY. Maturity ~5 years | confirmed | The 2.7× is LCD data for 2023; the year of the private-credit 2.0× is not stated. | https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html |
| C11 F | Fed FSR May-2026: perpetual BDCs $306bn / $161bn; interval funds $119bn / $80bn. Redemptions exceeded inflows in Q1-26 for the first time. The top-10 BDCs can cover at least 3 quarters of 5% | confirmed | The wording is "somewhat exceeded". Also confirmed: about 20% of PC net AUM; $1.4tn; about one-third of below-IG non-bank-loan debt. | https://www.federalreserve.gov/publications/2026-may-financial-stability-report-funding-risks.htm |
| C12 F | VRC Q3-26: requests of 13.9% (Q2) and 13.0% (Q3) at 11 of the 14 largest non-traded BDCs, against ~5% caps. Unitranche S+500–575, OID 98.75–99.25. ICR 1.7–1.8× (2021–22) vs 2.2–2.3× (2024–26) | confirmed | VRC measures requests as % of prior-quarter shares outstanding (≈NAV). ICR data are as of 30 Jun 2026. Medians: 13.3% and 11.5%. | https://www.valuationresearch.com/insights/private-credit-trends-q3-2026/ |
| C13 F | Evercore H1-26: credit secondaries $20bn, more than FY2025. GP-led deals at ~99% of FMV; senior portfolios at par or better; $31bn dry powder | confirmed | The $20bn is total deal value including continuation-vehicle (CV) leverage; equity commitments were $10bn. Evercore's chart also shows FY2025 at about $20bn, so "surpassing" is marginal. "Par or better" comes from the LP-led senior-credit pricing commentary (p.15). | https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf |
| C14 F | MSCI Q2-26: PE distribution rate 9% in H1-26 (11% in 2025; 24% in 2017; 27% in 2021). PC index 10.2 / 7.5 / 9.5; DL sub-index 12.1 / 7.5 / 10.8 | confirmed | MSCI defines the distribution rate as annualised, so comparing it with annual run-off cash is like-for-like. The quarterly figures in §4.1 also match. | https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf |
| C15 F | FSB May-2026: asset-based facilities allow LTV ≤65%, NAV facilities ≤30%. PIK in ~12% of loans, about half toggles. Toggles add 1–2pp to next-quarter delinquency on a 3% base. ~$220bn of bank lines | confirmed | The 12% comes from S&P credit-estimate data (Graph 9). The 1–2pp effect is on delinquency of US BDC loans, not on default, and is an association. The NAV ≤30% comes from "some member data". | https://www.fsb.org/uploads/P060526.pdf |
| C16 F | ECB FSR May-2026: 10% default at 50% LGD in general; 30% at 80% for software. US PC fund leverage ~30% | confirmed | Bank losses are "not exceeding 1.3% of total equity" (total equity, not CET1). | https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202605_04~3f2135af91.en.html |
| C17 F | OHA/T. Rowe Price: PIK by amendment 2.6% (Q4-21) → 6.6% (Q4-24) → 6.1% (Q3-25). PIK 7% of CDLI NII (Q2-25). 25–50bp premium; cash portion = base + half the spread | confirmed | The series is Morgan Stanley's analysis of the Lincoln VOG database. Endnote 1 sources the 7% to the CDLI. The cover is dated "Summer 2025". | https://www.troweprice.com/content/dam/gdx/pdfs/2026-q1/piking-your-spots-in-private-credit.pdf |
| C18 F | Erel, Flanagan & Weisbach (NBER w32278): net-of-fee abnormal return insignificant; gross-of-fee positive | confirmed | Dated March 2024. | https://www.nber.org/papers/w32278 |
| C19 F | Berrospide et al. (May 2025): $95bn committed / $56bn drawn (Y-14, 2024Q4). BDC line rate ~6.4% ≈ SOFR+200 | confirmed | The 6.4% is from Table 1; the note's own text says 6.6%. "≈SOFR+200" is the dossier's inference and is not in the note. | https://www.federalreserve.gov/econres/notes/feds-notes/bank-lending-to-private-credit-size-characteristics-and-financial-stability-implications-20250523.html |
| C20 F | FOMC +25bp to 3.75–4.00% on 16 Sep 2026, the first hike since 2023 | confirmed | Official statement; 12–0 vote. | https://federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm |
| C21 | "U.S. public pensions account for about 31% of private-credit fund investors (Form PF, 2021)" (§5) | **corrected** | "Public and private pension funds together held about 31% ($307bn) of private credit fund assets" (Form PF, Q4 2021). | https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html |
| C22 | Bad-PIK cohort LTV 39.4% at inception → 76.1% "(Lincoln, Q1 2026)" (§2.4) | **corrected** | The figures are right but come from Lincoln's Q4-2025 release (published Feb 2026). | https://lincolninternational.com/news/the-lincoln-private-market-index-ends-the-year-with-its-slowest-quarter-of-growth-in-2025 |
| C23 | Lincoln bad PIK was 2.5% of loans in Q4-2021 (§1) | confirmed | Lincoln Q4-25: 6.4%, vs 2.5% in Q4-21. The dossier's OHA series shows 2.6% for Q4-21 (a different series); harmless, but worth a footnote. | https://lincolninternational.com/news/the-lincoln-private-market-index-ends-the-year-with-its-slowest-quarter-of-growth-in-2025 ; https://fortune.com/2026/02/22/private-credit-market-shadow-default-rate-deals/ |
| C24 | Moody's: 2025 PC default 1.6% vs 4.7% depending on distressed exchanges; distressed restructurings ~65% of 2025 defaults (§2.4, §4.2) | confirmed | Moody's, 28 Apr 2026. | https://www.moodys.com/web/en/us/insights/credit-risk/private-credit/us-corporate-default-risk-in-2026.html |
| C25 | KBRA Middle Market Default Monitor: 3.3% by count, 2.4% by debt (12 months to Jun-26) (§4.2) | confirmed (secondary only) | Found only in Kadenwood (Aug 2026). The KBRA primary source was not retrieved. | https://kadenwoodcapital.com/perspectives/special-situations-into-2027 |
| C26 | "Industry commentary cited by the IMF says private-credit funds faced collateral pressures in 2020" (§5, back-leverage case) | **corrected** | The IMF says correlated revolver drawdowns "could create considerable funding needs", and that "such pressures were seen during the height of COVID-19 stress in 2020". That is a funding-need channel; it is not documented back-leverage collateral calls. | https://www.imf.org/-/media/files/publications/gfsr/2024/april/english/ch2.pdf (printed p.64) |
| C27 | BoE SWES (19 Jun 2026, 46 firms): 5-year recession, CPI 7%, Bank Rate 7%, FTSE −35%, European LL +390bp; final report 2027. July-2026 FSR quotes (§4.3) | confirmed | The FSR says "some" of the listed vulnerabilities, a group that includes private credit, became more pronounced. | https://www.bankofengland.co.uk/financial-stability/boe-system-wide-exploratory-scenario-exercise/publication-of-the-stress-scenario-for-the-private-markets-system-wide-exploratory-scenario ; https://www.bankofengland.co.uk/financial-stability-report/2026/july-2026 |
| C28 | First Brands: Ch.11 Sep-25; $10–50bn liabilities; indictments 29 Jan 2026; Ch.7 on 1 Sep 2026; UBS >$500m; Jefferies-affiliated $715m. Tricolor: Ch.7 Sep-25; JPM $170m; SEC 18 Aug 2026 (§4.4) | confirmed (secondary only) | Wikipedia only. Adequate for context, not for IC citation. | https://en.wikipedia.org/wiki/First_Brands_Group ; https://en.wikipedia.org/wiki/Tricolor_Holdings |
| C29 | Public BDCs ~80% of NAV; average BDC D/E 0.91× vs a 2.0× limit; Cliffwater-index redemptions 1.6% (Q3-25) and 4.8% (Q4-25) (§4.5, §6.4(8)) | confirmed | iCapital, 3 Mar 2026. The 1.6%/4.8% (Cliffwater index cited by iCapital) and the 12–14% (VRC non-traded BDCs) come from different samples (see R7). | https://icapital.com/insights/investment-market-strategy/bdc-redemptions-looking-beyond-the-gates/ |
| C30 | SOFR 3.89% (15 Oct 2026); 10y UST 5.09% (§4.1) | confirmed | SOFR was 3.89% on 15 Oct (NY Fed). The 10y 5.09% is the 16 Oct close; 15 Oct was 5.10%. | https://markets.newyorkfed.org/api/rates/secured/sofr/last/10.json ; https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202610 |
| C31 | Basel LCR: 10% 30-day drawdown on committed credit facilities to non-financial corporates, 30% on liquidity facilities (§2.6) | confirmed | BCBS 238, para 131(b)–(c). | https://www.bis.org/publications/201301-standards-basel-iii-liquidity-coverage-ratio-and-liquidity-risk-monitoring-tools.pdf |
| C32 | Golub: CDLI income return 10.9% (2005–24) vs HY 7.4% and leveraged loans 5.9% (§4.1) | confirmed | — | https://education.golubcapital.com/wp-content/uploads/2025/07/3-5-Consistent-Yield-Cushion-Helps-Smooth-Ride-20250729.pdf |
| C33 | Fortune (22 Feb 2026): ~6% over SOFR at the peak; all-in yields 11%+ → 8.5%; SOFR 5.4% → 3.73%; Blue Owl retail-redemption halt, shares −6% (§4.1, §4.4) | confirmed | The article does not name the peak year; the dossier's "2023" is an inference. | https://fortune.com/2026/02/22/private-credit-market-shadow-default-rate-deals/ |
| C34 | Jefferies credit LP pricing (% of NAV), 2019–2025, and H1-26 ≈89 (§4.5, §6.5, §6.9) | unverifiable | The primary PDF is image-only and the search budget was exhausted. The series anchors the regime table's secondary prices, so it needs re-sourcing. | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| C35 | CDLI 2023 components: total 12.13%, income 12.08%, realised −0.86%, unrealised +0.92% (§4.1) | unverifiable | Not in the CDLI Dec-2025 fact page; excerpt-only, as the dossier itself flags. The components are internally consistent. | https://www.bdcs.com/docs/CDLI-Fact-Page.pdf |
| C36 | The Fitch event mix includes "4% bankruptcy or restructuring" (§4.2) | unverifiable | Not in the cited GFM article. It appears to be the residual 100 − 47 − 41 − 8. | (GFM, as in C1) |
| C37 | Aggregator items: non-traded BDC tenders at 15–30% discounts to NAV; Moody's "true" default 5.8% vs 4%; BDC median non-accruals 2.8%; first-lien recoveries ~55% (§1, §4.2, §4.5) | unverifiable | Yardeni aggregator only, as the dossier flags. The 15–30% tender discount appears in the executive summary and should not reach the IC without a primary source. | https://yardeni.com/tools/private-credit-monitor |

**Counts:**
- 29 confirmed, including two (C25 and C28) supported only by secondary sources.
- 4 corrected: C2, C21, C22, C26.
- 0 refuted.
- 4 unverifiable: C34–C37.

---

## 3. Citation check: the ten most important references, plus extras

| Reference as cited | Exists? | Authors / year / title / venue | Issues |
|---|---|---|---|
| Erel, Flanagan & Weisbach (2024), *Risk-Adjusting the Returns to Private Debt Funds*, NBER WP 32278 | Yes | Correct: NBER WP 32278, Mar 2024; also SSRN 4771873 (Consensus record matches the abstract) | None |
| Cai & Haque (23 Feb 2024), *Private Credit: Characteristics and Risks*, FEDS Notes | Yes | Correct | One finding misquoted (C21) |
| Berrospide, Cai, Lewis-Hayre & Zikes (23 May 2025), *Bank Lending to Private Credit…*, FEDS Notes | Yes | Correct | The note's own text and table disagree on the BDC line rate (6.6% vs 6.4%) |
| IMF (Apr 2024), GFSR ch.2, "The Rise and Risks of Private Credit" | Yes | Correct | None |
| IMF (Apr 2026), GFSR ch.1 | Yes | Correct. The chapter title ("Global Financial Markets Confront the War in the Middle East and Amplification Risks") is not given | Cosmetic |
| FSB (6 May 2026), *Report on Vulnerabilities in Private Credit* | Yes | Correct | None |
| ECB (May 2026), FSR special feature, "Stress in global private credit markets…" | Yes | Correct title. The authors (Cera, Dieckelmann, Nikolov, Schepens, Schwartz Blicke) are omitted | Cosmetic |
| Cliffwater (Jan 2026), *2026 Asset Allocation Report* (S. L. Nesbitt) | Yes | Correct. PDF metadata: created 16 Jan 2026, author Stephen L. Nesbitt | The URL query string `v=20220116` suggests 2022, but the content is the 2026 report |
| Block, Jang, Kaplan & Schulze (2023/2024), *A Survey of Private Debt Funds*, NBER w30868; *RCFS* 13(2) | Yes | Correct: *RCFS* 13(2): 335–383 (2024) | NBER's published-version metadata adds "Isil Erel", probably the handling editor. Not a dossier error |
| Acharya & Steffen (2020), *RCFS* 9(3): 430–471 | Yes | Correct. The quote "all firms drew down bank credit lines" in the first phase is confirmed | None |
| Rintamäki & Steffen (2025), *PIK Now and Pay Later*, SSRN | Yes (seminar listings; FSB fn 46) | Paul Rintamäki and Sascha Steffen (Frankfurt School). Full title per the FSB: "PIK now and pay later: how deferred interest reshapes private credit" (Aug 2025) | Neither the dossier nor this check retrieved the SSRN page; the findings are as the FSB reports them, and the dossier tags them [E]. *[Added 2026-10-18: Crossref holds the record (DOI 10.2139/ssrn.5341145, "PIK Now and Pay Later - How Deferred Interest Reshapes Private Credit") with no abstract, so the finding is still second-hand (`research/literature/G6_private_credit.lit.md` §2). The dossier's in-text tags in §2.4 and §6.4(2), previously [S] and [S/I], are now [E] and [E/I].]* |
| Chernenko, Erel & Prilmeier (2022), *RFS* 35(11): 4902–4947 | Yes | Correct | NBER metadata adds a fourth name (Matvos), probably an editor artifact |
| Li, Strahan & Zhang (2020), *RCFS* 9(3): 472–500 | Yes | Correct | None |
| Duffie, Eckner, Horel & Saita (2009), *Frailty Correlated Default*, *JF* 64(5) | Yes | Correct (Consensus: *JF* 2009, DOI 10.1111/j.1540-6261.2009.01495.x) | None |
| Practitioner and market sources (Proskauer, KBRA, Lincoln, VRC, Evercore, MSCI, T. Rowe/OHA, iCapital, Fortune, GFM, PE Wire, Kadenwood) | Yes, all fetched | Dates and titles match | The Kadenwood URL slug ("special-situations-into-2027") does not match its title, although the content does. The Lincoln LTV statistic is attributed to the wrong quarter (C22) |

The remaining [K] references match standard bibliographic records from domain knowledge but were not re-fetched:
- Altman, Brady, Resti & Sironi (2005);
- Duffie & Singleton (1999);
- Lando (1998);
- Vasicek (2002);
- Gordy (2003);
- Frye (2000);
- Geltner (1993);
- Getmansky, Lo & Makarov (2004);
- Stanton (1995).

*Update 2026-10-18:* the literature check (`research/literature/G6_private_credit.lit.md` §2) has since confirmed all nine, plus Duffie et al. (2009), with full metadata. Eight were confirmed in Crossref; Vasicek and Frye, which have no DOI, were confirmed by WebSearch. The dossier's §10 now gives their pages and DOIs and tags them [M]. It also adds entries for two works it names only in the body: Bühlmann (1967), DOI 10.1017/S0515036100008989, and Takahashi & Alexander (2002).

**Result:** no hallucinated or garbled citations. The problems are attribution-level (C21, C22, C26 and the Proskauer definition) and cosmetic.

---

## 4. Reasoning issues and overclaims, ranked

Severity: **High** changes an IC-facing number or recommendation. **Medium** changes model behaviour or calibration. **Low** is presentation or a minor specification point.

### R1 (High). The run-off liquidity uplift is computed for a book ADIC mostly cannot switch.
- **What the dossier does:** §6.8 and §1 item 4 simulate the whole $14bn as one ADIC-controlled pool. There is no wrapper layer, and capital calls on the $3.0bn fund unfunded are ignored.
- **Who controls the switch** under the dossier's own synthetic wrapper mix (SMA 40%, CEF 45%, evergreen 10%, listed BDC 5%):
  - SMAs: ADIC controls reinvestment, so the switch is an ADIC action.
  - CEFs past their investment period: they already return principal, so switching adds nothing.
  - CEFs in their investment period: the GP decides on recycling and calls capital.
  - Evergreen funds and listed BDCs: there is no run-off option.
- **Corrected size:** the claim that switching to run-off in Tight "adds ≈$2.2bn in year 1 (12–25% of the payout)" scales to about **$0.8–0.9bn**, or roughly 5–10% of the $8.9–17.7bn payout, on the SMA sleeve. More is possible only if ADIC obtains recycling waivers.
- The run-off cash table in §1 item 4 (37 / 30 / 22 / 14%) describes an SMA-like pool, not the blended book.

### R2 (High). The SELL-vs-HOLD break-even mixes wrappers, and the SMA verdict flips with the dossier's own prices.
- **What the dossier does:** λ* = V^H/(π·NAV) − 1 prices the whole book at the LP-interest secondary price π (0.94 / 0.88 / 0.75). It uses SMA-style run-off as the HOLD path.
- **Why the comparison fails:**
  - SMA books are sold as loans, at the loan-sale prices in §6.5 (0.99 / 0.96 / 0.85), not as LP interests.
  - CEF interests in their investment period cannot be put into run-off by an LP.
- **Re-computed with the dossier's own numbers** (V^H at SOFR+5% and the §6.5 loan-sale prices):

  | Start regime | λ* for SMA loan sales |
  |---|---|
  | Normal | ≈ −2.9% |
  | Tight | ≈ −1.4% |
  | Crisis | ≈ +6.6% |

  Selling SMA loans therefore beats holding in Normal and Tight, even with no liquidity premium.
- **Why:** V^H is below NAV in every regime. The SOFR+5% discount rate exceeds the book's expected net return.
- **Consequence:** the rule "never sell senior books in C unless λ > ~20%" and the 2% / 8% / 21% thresholds (§1, the spec-card SELL rule) are artifacts of mixing wrappers and of the discount-rate choice.
- **Fix:** compute λ* per wrapper, each with its own HOLD path and sale price, and show the sensitivity to the discount rate.

### R3 (Medium-High). Recovery assumptions contradict the dossier's own bias correction.
- **The contradiction:**
  - The spec card says "recovery (use 33–55% not 60–70%)", and bias #2 cites the Fed's 33% direct-loan post-default value.
  - Yet the regime table and the script use DL recoveries of **65% (Benign) and 60% (Normal)**, with 52% in Tight and 40% in Crisis.
- **Sensitivity** (author's model re-run, 5-year run-off loss starting in Tight):

  | DL recoveries (B/N/T/C) | Mean loss | P99 loss |
  |---|---|---|
  | As published (65/60/52/40) | 6.1% | 17.2% |
  | 55/50/45/35 | 6.6% | 18.2% |
  | 45/40/35/30 | 7.1% | 19.4% |

  The last setting is close to the 20%-of-NAV credit-risk budget in §6.6.

### R4 (High). The §6.8 illustration does not implement several documented mechanisms, and one undocumented choice drives the losses.
§3 says the cohort engine is "used in the §6.8 illustration". `g6_pc_pool_sim.py` differs from the §6.4 specification in these ways:
- **(a) Reinvestment spread.** Recycled principal earns the original segment spread, not the new-issue spread s^new. The composition never updates and V^reinv is not modelled. The run-off-vs-reinvest comparison therefore omits reinvestment's main benefit in Tight and Crisis.
- **(b) Maturity extensions.** There is no extension state, although extensions are 41% of Fitch events and §6.4(2) counts them as selective defaults. The model's "selective default" is payment default plus PIK switch.
- **(c) Prepayment.** There is no refinancing-incentive CPR and no exit factor X^exit. CPR is a deterministic constant per regime.
- **(d) Mark catch-up.** κ is a constant 0.45, not the regime-dependent 0.5 / 0.45 / 0.4 / 0.3.
- **(e) PIK-cohort default hazard.** The code uses 0.15·√(S/0.10) per year. That is about 15% a year at baseline stress, roughly 9× the cash-pay hazard, whereas the dossier documents a multiplier m_P of ×1.3–1.7.
  - With the documented ×1.5, the 5-year loss falls from 6.1% to **4.2%** (mean) and P99 falls from 17.2% to **12.2%**.
  - This undocumented parameter is the single largest driver of the loss results.
  - The ×9 may be the more realistic value, since bad-PIK LTV is 76%, but the specification and the code must agree.
- **(f) Hazard units.** Quarterly probabilities use hΔ, the pitfall §7 itself warns against. Immaterial at these levels.
- **(g) Missing layers.** There is no fund layer (CEF recycling, capital calls, fund facilities), no evergreen queue and no listed-BDC P/NAV, although the specification card lists all of them.
- **(h) Back-leverage.** The cure simulation has no repayments, cash sweeps, interest or recoveries; collateral only erodes. The P(deficiency) table is therefore not conditional on any facility waterfall.
- **(i) Crisis rates.** The Crisis regime pulls SOFR down to 2.75%, which raises ICR. The stagflationary crisis the dossier emphasises (rate hikes; BoE SWES Bank Rate of 7%) is not represented, so Crisis-regime defaults may be understated for exactly that scenario.

### R5 (Medium). Calibration is presented as validation.
- **Circularity:** "The synthetic selective-default rate in T (6.4%) reproduces Fitch's 6.3%" is circular. The Tight target (6–6.5%) was set from Fitch, and the switch intensity φ^sw is a free parameter.
- **Different mixture:**

  | Share of default events | Model | Fitch |
  |---|---|---|
  | Payment default | ≈36% (2.3pp of 6.4pp) | 8% |
  | PIK switch / deferral | ≈64% | 47% |
  | Maturity extension | 0% | 41% |

  This breaches the dossier's own rule "never calibrate one hazard to a mixture".
- **Loose match to the IMF:** the ICR elasticity "matches" the IMF's 2–3× only loosely. The stressed share is not a default rate, and the IMF's scenario magnitudes are not replicated.

### R6 (Medium). The default-definition comparison is overstated.
- Two claims go too far:
  - "2.5% vs 6.3% for the same market and quarter";
  - "a single payment-default rate understates impairment roughly 2–3×".
- **How the two series differ:**
  - Sample: Proskauer covers 716 senior/unitranche loans; Fitch covers its MCO/PMR universe. Borrowers with <$25m EBITDA default at 12% in Fitch but 1.9% in Proskauer.
  - Weighting: loan count vs issuers.
  - Window: quarter-end vs TTM to August.
  - Definition: Proskauer's is broader than the dossier states (C2).
- Default incidence is not impairment: PIK events often cure, and the dossier's own model includes cures.
- **Fix:** say "default incidence varies 2–3× across series" and leave the loss impact to the model.

### R7 (Medium). The evergreen liquidity rule is mis-specified.
- **The formula mixes levels:** §6.6.1, "min(c̄, expected fulfilment) × NAV", combines a fund-level cap (5% of fund NAV) with a holder-level proration rate (30–50% of a request).
- **How proration works:** under pro-rata tenders, a holder receives fulfilment × its request. For example, 5/13 ≈ 38% of a full-position request, not min(5%, 38%) of its NAV.
- **Replacement:** use E[min(1, c̄·NAV_fund/Σrequests)] × R^req_ADIC, with ADIC's own request included in Σrequests.
- **Double count:** queue equation (8) calibrates new requests (R^new) to industry request rates of 12–14%, which already include resubmissions. It then adds ς × backlog on top.
- **Mixed samples:** the 1.6% / 4.8% rates (Cliffwater index, via iCapital) and the 13–14% rates (VRC, non-traded BDCs) come from different samples.

### R8 (Medium). The "regime-conditional P05" liquidity haircut is nearly cosmetic.
- CPR, amortisation and draws are deterministic within a regime.
- The fixed-regime P05 of run-off cash is therefore 97–99% of the mean (Tight: 21.3% vs 21.6%; JSON field `net_cash_p05`).
- The §6.6.1 rule ("count at regime-conditional P05, not the mean") gives little protection unless either:
  - repayment-speed uncertainty is modelled, for example a stochastic CPR linked to X^exit; or
  - regime uncertainty is included.

### R9 (Medium). The Tight-regime prepayment calibration conflicts with current data.
- The CDLI's non-interest cash flow of ">6% per quarter" in mid-2026 is about 22% a year, which is Normal-level in the dossier's own table.
- The regime labelled "today" (Tight) uses a DL CPR of 12–16% (script: 14% plus 1% amortisation).
- Either the current repayment state is not Tight, or the Tight CPR is too low. Run-off cash in Tight may be understated.

### R10 (Medium). The credit-secondary dry-powder argument does not follow from its evidence.
- The IC recommendation says credit secondaries "are richest when liquidity is scarce: H1-2026 volume was $20bn, a record". That evidence points the other way:
  - Evercore shows GP-led credit at ≈99% of FMV and senior portfolios at par or better, i.e. a seller's market.
  - The $20bn includes CV leverage; equity was $10bn.
- The option-value argument may hold for a future stress, but the cited evidence does not show buyer value today.

### R11 (Low-Medium). The reinvestment option value omits expected losses.
- V^reinv = E[PV(s^new − c^opp)] should subtract expected losses on the new loans.
- As written it overstates reinvestment value in exactly the Tight and Crisis regimes where the dossier says it is highest.

### R12 (Low-Medium). The ICR calibration is mislabelled and incomplete.
- **Median labelled as mean:** ICR₀ = 2.0 is used as the lognormal median (σ = 0.54 puts 10% below 1×), but it is labelled "mean", following the Fed's "average".
- **If 2.0 is the mean:**
  - σ = 0.54 puts 15.5% below 1×, not 10%;
  - matching both a 2.0 mean and 10% below 1× needs σ ≈ 0.46;
  - with σ ≈ 0.46 the rate elasticities rise to ×1.46 / ×2.5 / ×4.3, against the dossier's ×1.36 / ×2.2 / ×3.6.
- **Omissions:** the cohort ICR ignores PIK capitalisation (debt growth) and rate floors.

### R13 (Low). The LEVER test survives; Lincoln's break-even does not reconcile.
- **LEVER hurdle:** "EL < y_A − c_B ≈ 4.0%" ignores fees that rise with leverage.
  - With Cliffwater's fee stack and 6% hurdle, the break-even is still about 4.0%, because incentive fees vanish below the hurdle. The number survives.
  - At the dossier's own Tight-regime back-leverage cost (S+225–275), the hurdle falls to about 3.25–3.75%.
- **Lincoln's figure:** the dossier is right that Lincoln's "~9% cumulative loss → zero IRR" does not reconcile. Simple carry arithmetic gives a break-even of about 18–31% of assets over a 3–5-year life. Do not calibrate to the 9% until Lincoln's metric is clarified.

### R14 (Low). Some listed actions are not discretionary for an LP.
- "DDTL funding policy" (§6.3) and "fund DDTLs" (LEVER menu) are contractual obligations: refusing a borrower's draw is a lender default. Only the source of financing is discretionary.
- "Raise fund debt/equity" is not an LP action in CEF, evergreen or listed-BDC wrappers. Restrict LEVER to SMAs.
- Credit-secondary purchases are deployment, not leverage.

### R15 (Low). One constraint is redundant.
- "A/B ≥ 1.5" never binds alongside "look-through D/E ≤ 1.0×", because D/E ≤ 1 already implies A/B ≥ 2.

---

## 5. Overall reliability rating

**MEDIUM.**

| Part of the dossier | Rating | Why |
|---|---|---|
| Empirical layer (§4) | High | 29 of 37 checked claims confirmed and none refuted. The four corrections are attribution or definition errors. |
| Decision economics (§6.8), §1 items 4, 6 and 8, spec-card SELL/REFINANCE/LEVER rules | Medium to low | The headline IC numbers ($2.2bn run-off uplift; λ* of 2% / 8% / 21%; "never sell senior books") rest on a single-pool synthetic model that ignores wrappers. That model departs from the documented specification on its main loss driver and uses recoveries the dossier itself calls biased. |

### Required before the IC
1. **Add a wrapper layer** to the §6.8 illustration: SMA, CEF by investment-period status, evergreen, listed BDC.
   - Recompute the run-off uplift and λ* per wrapper, each with its own sale price and HOLD path.
   - Include capital calls on fund unfunded commitments.
2. **Reconcile two parameters and report results under both settings:**
   - the PIK-cohort hazard (≈×9 in the code vs ×1.3–1.7 documented);
   - the DL recoveries (60–65% used vs "33–55%" recommended).
3. **Correct the text:**
   - fix C2, C21, C22 and C26;
   - drop the "reproduces Fitch" validation claim;
   - restate the 2.5% vs 6.3% comparison.
4. **Fix the liquidity mechanics:**
   - correct the evergreen liquidity formula and the queue double count;
   - make CPR stochastic, so that the P05 rule has content.
5. **Re-source or remove** the Jefferies credit pricing series and the 15–30% tender discount before they appear in IC-facing text.

### Verification artefacts (session scratchpad)
- **Folder:** `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\verify_g6\`. It holds the text extractions and helper scripts.
- **`scripts\check_math.py`** re-derives:
  - the stationary distribution (19.8 / 42.7 / 28.2 / 9.2%, matching the dossier);
  - the λ* values;
  - the ICR elasticities;
  - the fee-inclusive leverage break-even (3.98%);
  - the Lincoln carry check;
  - the wrapper-adjusted uplift.
- **`scripts\sensitivity.py`** re-runs the author's model with alternative DL recoveries and with the documented PIK multiplier.
- **Author's model reviewed:** `...\scratchpad\g6_scripts\g6_pc_pool_sim.py`. Its output, `...\scratchpad\g6_out\g6_pc_pool_sim_results.json`, matches every §6.8 table.

---

## Citation corrections (2026-10-18)

*Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 and `research/literature/G6_private_credit.lit.md` §2. The audit names nothing this log wrongly accepted, so no erratum is added. One line per change.*

1. §3 citation table, Rintamäki & Steffen row: adds the Crossref record (DOI 10.2139/ssrn.5341145, full title, no abstract) and notes that the dossier's in-text tags are now [E] and [E/I].
2. §3, after the list of [K] references: adds a note that the literature check confirmed all ten [K] works with full metadata, that the dossier's §10 now carries it, and that the dossier now has entries for Bühlmann (1967) and Takahashi & Alexander (2002).
3. Status: findings C15, C19 and C21 are now applied in the dossier (audit §2.4 item 15; dossier "Citation corrections (2026-10-18)" items 1–6).
4. Status: C2 (Proskauer definition), C22 (Lincoln quarter) and C26 (IMF 2020 reference) remain open in the dossier. The literature audit does not list them, so this pass did not apply them.
