# G14 Real Assets actions and financing: verification log

*Adversarial fact-check of `research/groups/dossiers/G14_ra_actions_financing.md`. Prepared 2026-10-18. The dossier was not edited.*

## 1. Summary

**What was checked.**
- 29 empirical claims: the author's 20 flagged claims plus 9 others I judged load-bearing or suspicious (§2).
- 13 academic references in detail and 20 industry references at document level (§3).
- The design implications and the specification card (§2.4–2.7, §3, §6, §7), for reasoning and formula errors. I read `research/groups/addenda/G14_calcs/g14_ra_actions.py` in full and re-ran parts of it from a scratch script. The script imported the module without running `main()`, so nothing in the project was written.

**Method.**
- **Primary PDFs.** I downloaded each primary PDF myself, extracted the text layer with pypdf, grepped for every number and read the surrounding text. Files: Jefferies *Global Secondary Market Review* (Jul-2026), Campbell Lutyens *1H 2026* (Aug-2026), the NCREIF NFI-ODCE 2Q2026 release, Meketa (Jul-2024), Chen & Chen (9 Jun 2025), the Latham & Watkins Q&A (22 Apr 2015) and IFM Investors (2023).
- **Web pages (WebFetch).**
  - Market data: PREA Quarterly, CBRE (Q2-2026 and Q3-2023 releases), FRED (SUBLPDRCSN, SOFR, DGS5, DGS10), MBA Newslink, Accordant, the Jefferies insight page, Yieldpro.
  - Papers and press: NBER w31970, Commercial Observer, Investing.com (Safehold), Haynes Boone, DTZ Investors, Alliance Global Advisors.
  - Official and other: the NBIM mandate, nyc.gov, tax.ny.gov, Morningstar DBRS, Bisnow, Wikipedia (Thames Water).
- **Standard web searches.** Used for:
  - the Devaney & Scofield abstract (the CentAUR page was behind a bot wall);
  - the paywalled Harken Capital figures;
  - Thames Water's 2023–24 funding;
  - CPP's leverage limit, Ofwat gearing, BREIT fills and the Brookfield DTLA defaults.
- **Metadata.** From Crossref (until it returned HTTP 429) and then OpenAlex. Consensus was not used.
- **Scratch scripts** (session scratchpad, `g14v/scripts/`):
  - `extract.py`: PDF text extraction;
  - `queue_check.py`: queue, JV and Merton re-runs;
  - `cap_check.py`: cap repricing.

**Bottom line: the factual layer is very strong.**
- **Flagged claims.** 19 of the 20 are confirmed against primary documents, essentially to the digit. One, the Harken energy-fund bids for 2H-2015, cannot be checked at the primary because the article is paywalled. A search summary of the same article is consistent with it.
- **NYS transfer tax.** The 0.65% rate that the dossier tags [U] is **confirmed** on tax.ny.gov. It is a 0.4% base tax plus a 0.25% additional base tax on non-residential conveyances of $2m or more in cities of 1m+ people, paid by the grantor. The NYC κ of 6.9% therefore stands.
- **Additional claims.** Of the 9, 6 are confirmed and 3 are corrected. The corrections:
  - **Thames Water.** The £750m was a conditional pledge, not an injection, and the £500m withheld in March 2024 was its first tranche.
  - **IFM.** The "secondary pricing, not NAV" sentence describes closed-ended funds, not open-end ones.
  - **CBRE Q3-2023.** Banks were the largest lender in Q3-2023 at 38.4%. The dossier's 2023-versus-2026 lender-mix story omits this.
- **References.** Every academic reference exists with correct authors, year, title and venue. The problems are minor labelling and tagging issues (§3).

**The design and specification layer has five must-fix problems (§4):**
1. **The open-end queue's value cost charges time value twice.** Queued units are held at constant NAV but discounted at SOFR × (1+ℓ), which contradicts the code's own "NAV = economic value" assumption.
   - At ℓ = 10% the corrected cost is 3.6% / 10.3% / 16.2% (N / T / C), against the dossier's 5.0% / 13.9% / 21.7%. At ℓ = 20% in C it is 28.0%, not 32.4%.
   - Against a 25% stress bid, the break-even for selling units moves from ℓ ≈ 13% to ≈ 17%.
2. **JV stake pricing applies an asset-level discount to levered equity.**
   - Corrected κ_JV is 7.7% / 27% / 58% (N / T / C), not 6.3% / 19% / 40%.
   - T\* becomes ≈2.4 / 6.7 / 9.2 years, not 1.8 / 5.3 / 7.7.
   - In T and C, SELL 100% becomes cheaper than the JV sell-down. That reverses the worked example's "JV sell-down for size" and "avoid SELL 100%" advice in C.
3. **Irreversible REFINANCE is costed as a 2-year loan.** Ground leases and sale-leasebacks get ≈0.08 per $ of headroom, although the dossier calls a ground lease a "near-irreversible 99-year senior claim". Over just 10 years the same ŝ gives ≈0.34, next to real-estate LP sales.
4. **The default ϖ = 1 is inconsistent with the leverage accounting.** The dossier says ϖ = 1 debt is "economically recourse", yet T5 limit 1 counts only the P95 of 24-month cures, and asset-level pledges are kept out of the encumbrance limit.
5. **The worked example prices a "maturity cash-out" as if it were available today.** The loan has two years left, so the "cheapest for a 1-year need" result holds only for needs that arise at maturity.

**Overall reliability:** sourcing and citations **HIGH**; design and specification layer **MEDIUM**; **overall MEDIUM** until R1–R5 are fixed (§6).

## 2. Claims table

S = author-flagged claim; A = additional claim I selected.

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| S1 | Jefferies H1-2026 LP pricing (% of NAV): real estate 68, infrastructure 91, all strategies 87. Real estate liquidity "remained challenged". Energy/upstream pricing and demand rose on commodity volatility | **Confirmed** | Exact (p. 5).<br>• Real estate: "settled at 68% of NAV in H1 2026 as liquidity conditions remained challenged across the asset class".<br>• Energy: "Commodity price volatility in the energy markets significantly increased the pricing and demand of upstream and natural resources funds".<br>• Strategies: buyout 91, venture 79, credit 89.<br>• Fig. 2 text layer, real estate 2020→H1-26: 76, 79, 71, 71, 72, 70, 68. This matches dossier §4.1. The 2019 value (83) is not in this report (unverified sub-item).<br>• Also confirmed: 33% of LP sales structured (26% with deferrals, 7% other), and the real-assets CV text. | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| S2 | Campbell Lutyens 1H-2026: average LP-led discount 13.3%, infrastructure 5.0%; energy pricing +9.2%; infrastructure secondaries $10bn in 1H-26 (78% GP-led) after $20bn in 2025 | **Confirmed** | Exact.<br>• p. 6: 13.3% (13.6% in FY-25); infrastructure 5.0%; private credit 5.1%; venture 32% (26%). Energy "increasing 9.2% as energy-focused buyers entered the market with conviction that oil prices will stay higher for longer". Real estate "remains at significant discounts… pricing improved 6.0%".<br>• p. 17: $10bn "roughly flat against 1H 2025". GP-led ≈$8bn = 78%, against 55% in 2025 and "the 41% low in 2023". Volumes $9bn (2022) → $20bn (2025); CL forecasts $26bn for 2026. | https://campbell-lutyens.com/media/keapzv55/campbell-lutyens-1h-2026-secondary-market-full-report_august-2026.pdf |
| S3 | NFI-ODCE Q2-2026: 25 funds; $280.4bn gross and $223.7bn net; leverage 27.1%; net flows −$8.7bn over the year to June 2026 | **Confirmed** | Exact (release of 30 Jul 2026).<br>• Leverage 27.1% (27.3% the prior quarter); range 15–34% since 2000; average 22.4%.<br>• Year to 30 Jun 2026: contributions $10.4bn, distributions and redemptions $19.1bn. | https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf |
| S4 | Since 2007 ODCE funds paid ≈71% of queues a quarter on average; core funds ≈5% a quarter in 2023; core queues ≈21% of NAV (2009) and ≈16–17% (late 2023) | **Confirmed** | Exact (Kochis & Moné, Townsend; PREA Quarterly, Winter 2024).<br>• "NFI-ODCE funds paid out an average of 71% of their queues each quarter"; queues were completely paid off "nearly 60% of the time"; 5% a quarter in 2023; "16% to 17% today versus 21% in 2009".<br>• Redemptions averaged under 1.5% of NAV a quarter (range 0.4–3.5%). The most common notice period is 90 days, with some funds at 45 or 60. Most funds have moved away from FIFO.<br>• "Perhaps 2% of NAV" is the authors' suggested reserve, not observed practice.<br>• See R12: 71% is a full-cycle average, not a normal-regime value. | https://www.prea.org/publications/quarterly/negative-fundraising/ |
| S5 | ODCE queue 19.3% of NAV in Q1-2024, against 9.2% (Q4-2020) and a 15% GFC peak; just above 10% in Q1-2026 (Accordant) | **Confirmed** | Exact.<br>• Meketa p. 6: "roughly 19.3% of net asset value in the redemption queue as of Q1 2024… more than double the 9.2%… Q4 2020… higher than… the GFC which reached a peak of 15%". It also says investors "were quick to rescind their redemption requests" in prior cycles.<br>• Accordant (25 Jun 2026): "Redemption queues declined to just above 10% of NAV".<br>• §4.2's "≈12% (Q3-2025)" is **not** on the Accordant page (unverified sub-item). | https://meketa.com/wp-content/uploads/2024/07/MEKETA_Current-State-of-Core-Real-Estate.pdf ; https://www.accordantinvestments.com/knowledge-center/private-real-estate-enters-a-new-cycle-q1-2026-nfi-odce-index-insights |
| S6 | CBRE Q2-2026: spread 204bp, LTV 59.6%, DSCR 1.43, debt yield 10.2%, average rate 5.7%; lender mix alternative lenders 38%, banks 30%, life companies 21%, CMBS 11% | **Confirmed** | Exact (3 Aug 2026).<br>• 204bp (−21bp YoY); multifamily 162bp; LTV 59.6% (60.8%) and multifamily 63.3%; DSCR 1.43 (1.34); debt yield 10.2% (9.7%); "Average mortgage interest rates edged down to 5.7%".<br>• Lender shares 38 (34) / 30 (24) / 21 / 11 (19).<br>• Caveats:<br>  – Spreads are "based on fixed-rate, five-to-10-year permanent loans". The release does not name Treasuries as the benchmark, and does not say the 5.7% is fixed-rate only.<br>  – These are **Q2** terms. The 5-year UST rose from ≈4.09% (Q2 average) to 4.91% on 15 Oct 2026 (R8). | https://www.cbre.com/press-releases/commercial-real-estate-lending-fundamentals-remain-strong-q2-2026-cbre |
| S7 | Net % of banks tightening nonfarm-nonresidential CRE standards peaked at 68.3% (2023:Q3 in FRED's dating); −11.3% for 2026:Q3 | **Confirmed** | Exact: 2023-07-01 = 68.3; 2026-07-01 = −11.3. Every intermediate value in §4.3 matches: 41.5, 52.9, 57.6, 66.7, 68.3, 67.2, 42.4 … 3.3, −3.6, −3.3, −11.3. | https://fred.stlouisfed.org/data/SUBLPDRCSN |
| S8 | $875bn (17% of $5.0tn) matures in 2026, after $957bn in 2025; 30% of hotel and 17% of office loans mature in 2026 | **Confirmed** | Exact (MBA, 9 Feb 2026).<br>• By property type: industrial 23%, healthcare 15%, multifamily 13%.<br>• By holder: depositories $396bn (21%); CMBS/CLO/ABS $200bn (25%); credit companies and others $163bn (29%); life companies $76bn (10%); GSEs $39bn (4%). | https://newslink.mba.org/mba-newslinks/2026/february/mba-newslink-tuesday-feb-10-2026/17-of-commercial-and-multifamily-mortgage-balances-to-mature-in-2026/ |
| S9 | 14% of all CRE loans and 44% of office loans are in negative equity; used as the crisis calibration target | **Confirmed** | Exact (NBER w31970; Dec-2023, revised Dec-2024): "14% of all CRE loans and 44% of office loans are in negative equity". The calibration reproduces both shares (re-derived; see §4 "Arithmetic"), but its identification is conditional (R14). | https://www.nber.org/papers/w31970 |
| S10 | A 1pp rise in the rate gap cuts the CRE refinancing probability by 11.1%; rollover-risk sales ≈12–13% below refinance valuations | **Confirmed (units caveat)** | Exact (Jiakai Chen & Yifan Chen, Univ. of Hawaiʻi at Mānoa; WP 9 Jun 2025).<br>• Table 9: "reduces the likelihood of refinancing by 11.1%" (12.8% in the matched sample). This comes from a **linear probability model** whose outcome is refinance-versus-sale among transacting properties, so it means ≈11.1 **percentage points** in the refinance share of transactions (R15).<br>• Table 10: sales valued ≈12% below refinance transactions, and 13% after controlling for the rate gap. The comparators are refinance appraisals.<br>• $2.26tn maturing by end-2028: confirmed. | https://haas.berkeley.edu/wp-content/uploads/archive/The-Writing-on-the-MAturity-Wall.pdf |
| S11 | 2023: a $337.5m 4%-strike cap's cost rose from ≈$0.78m to ≈$3.5m (+348% YoY); ≈40% of 682 CRE-CLO loans had caps expiring before maturity | **Confirmed** | Exact (McDevitt, CRED iQ; Commercial Observer, 27 Mar 2023).<br>• The cap expires Feb-2024. The article calls it a "348 percent year-over-year increase" and says "Of the 682 loans observed…".<br>• Uncapped note rates are ≈200bp higher.<br>• Transferability caveat: the spec card applies the 40% as a parameter to ADIC's floating book (R14). | https://commercialobserver.com/2023/03/cre-clo-interest-rate-cap-agreements-spotlight |
| S12 | NBIM mandate (amended 9 Dec 2025): unlisted real estate debt ratio ≤ 25% and ≤ 70% per investment; unlisted renewables ≤ 60% over time and ≤ 70% per investment | **Confirmed** | Exact.<br>• §4.2.6: "shall not exceed 25 per cent"; "No single investment shall be financed with more than 70 per cent debt", measured at acquisition or refinancing.<br>• §4.3.2(e): the portfolio is organised "with the aim that the debt ratio of the portfolio over time" stays within 60%, so it is an aim, not a hard cap. Single renewables investments ≤ 70%. | https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/ |
| S13 | Safehold Q2-2026 originations: GLTV 35%, rent coverage 3.0×, economic yield 7.4%. Portfolio: GLTV 52%, cash yield 3.8%, economic yield 6.0% | **Confirmed** | Exact (30 Jul 2026).<br>• Originations: $150m across seven multifamily properties.<br>• Portfolio: coverage 3.4×; GAAP yield 5.5%; economic yield 6.0% is forward-looking with 2% inflation.<br>• The Q1-26 7.2% in §4.4 is not on this page. | https://www.investing.com/news/company-news/safehold-q226-slides-multifamily-focus-drives-growth-amid-valuation-gap-93CH-4826424 |
| S14 | UK commercial property: median 135 days marketing-to-completion for a sale and 104 days for a purchase (578 deals, 2004–13) | **Confirmed** | Exact, from the abstract ("578 transactions over the period 2004-2013"; purchase from introduction to completion 104 days; sale from marketing to completion 135 days). Metadata from Crossref: *J. Property Research* 32(4), 362–383, DOI 10.1080/09599916.2015.1089924. | https://centaur.reading.ac.uk/43823 ; https://doi.org/10.1080/09599916.2015.1089924 |
| S15 | Spring 2020: a large majority expected borrowing-base cuts of ≥ 20%; 45% expected ≥ 30%; banks' base-case deck 15.6% below fall 2019 | **Confirmed** | Exact (1 Apr 2020).<br>• "a sizable majority of respondents expect borrowing bases to decrease by at least 20%".<br>• "45%… of 30% or more".<br>• "The average Base Case for oil post-crash is 15.6% lower than the fall 2019 Base Case". | https://www.haynesboone.com/news/press-releases/spring-2020-oil-and-gas-industry-surveys |
| S16 | RBL bases redetermined semi-annually; deficiencies cured in 3–6 equal monthly installments; production payments are a bankruptcy-remote sale; monetizing hedges triggers a redetermination | **Confirmed** | Exact (Q&A with J. Michael Chambers, 22 Apr 2015).<br>• Scheduled redeterminations twice a year (spring and fall), plus 1–2 interim ones.<br>• Cures by "equal monthly installment payments – usually between three and six installments".<br>• A production payment, "properly structured, is a sale of assets… a bankruptcy remote transaction".<br>• Unwinding or resetting hedges "will almost certainly result in a borrowing base redetermination". "Triggers" slightly overstates this. | https://www.lw.com/admin/Upload/Documents/Are-You-an-E-and-P-Company-Facing-a-Liquidity-Crunch-and-Considering-Restructuring.pdf |
| S17 | UK open-end unit secondaries: bids −25%, offers −15% (Nov-2022, two most liquid diversified funds); mid-2021 bids −5.0% to +3.5% | **Confirmed** | Exact (S. Berry, DTZ Investors, 8 Dec 2023). Mid-2021 offers ranged from −2% to +6%. "Managers generally have up to two years to pay out redemptions." | https://www.dtzinvestors.com/en/news/2023/december/breaking-through-the-noise-the-viability-of-open-ended-real-estate-funds-in-the-wake-of-ongoing-redemption-deferrals |
| S18 | Trepp Sep-2026 CMBS delinquency: overall 8.02%, office 12.16%, multifamily 8.04%, industrial 1.14% (secondary relay) | **Confirmed (relay)** | Exact against the relay (M. Rudy, 4 Oct 2026).<br>• Also: retail 6.58%, lodging 6.18%; including performing matured loans, 9.66%.<br>• The relay has typos: it labels the overall rate "June" and says retail "fell 62 basis points higher". Check Trepp's primary before IC use. | https://yieldpro.com/2026/10/multifamily-cmbs-delinquency-rate-leads-overall-rate-higher-in-september |
| S19 | NYC RPTT on commercial transfers above $500k is 2.625%, plus a NYS tax on NYC conveyances of $2m or more (0.65% unverified) | **Confirmed; [U] resolved** | Exact.<br>• nyc.gov: 1.425% up to $500k; 2.625% above.<br>• tax.ny.gov: a 0.4% base plus an "additional base tax of $1.25 for each $500" (0.25%) on non-residential conveyances of $2m or more in cities of 1m+ people, so **0.65%**. "Paid by the grantor (seller)".<br>• The NYC κ of 6.9% reproduces. | https://www.nyc.gov/site/finance/property/property-real-property-transfer-tax-rptt.page ; https://www.tax.ny.gov/bus/transfer/rptidx.htm |
| S20 | Energy-fund median secondary bids fell to 61–76% of NAV in 2H-2015, the lowest of all strategies (Harken Capital, via a search summary of a paywalled article) | **Unverifiable at primary** | The article is paywalled (A. Le, 29 Feb 2016); only the headline "Energy and venture pricing fell further in H2" is visible. A search summary of the same article gives 61–76% (up to 80% in 1H-15), the lowest of all strategies, with all strategies at 78–89%. That is consistent, but no stronger than the dossier's own evidence. Keep the [S-sec]/low tag. | https://www.pei-secondariesinvestor.com/energy-and-venture-pricing-fall-further-in-h2/ |
| A1 | Brookfield did not repay the Gas Company Tower's $350m mortgage and $65m + $50m mezzanine at the 9 Feb 2023 maturity; with 777 Tower ($319m) the total was $784m; receivership followed | **Confirmed** | Gas Company Tower $465m (extension options unused). 777 Tower: a $268.6m mortgage plus $50m mezzanine = $318.6m. The 777 default came from **declining the required interest-rate protection**, a live example of the dossier's cap cliff. | https://www.bisnow.com/news/los-angeles/commercial-real-estate/brookfield-default-downtown-los-angeles-gas-tower-777-figueroa-117640 ; https://commercialobserver.com/2023/04/brookfield-gas-company-tower-recievership/ |
| A2 | Thames Water: "Shareholders injected £750m in July 2023 (£1bn sought), then withheld the first payment of a larger plan in March 2024"; OMERS (31.7%) wrote to zero in May 2024; debt ≈£20bn by January 2026; creditors proposed write-offs of > £13bn; ADIA's Infinity is a shareholder | **Corrected** | In **July 2023** shareholders **conditionally agreed to provide** £750m of new equity for the rest of AMP7, short of the £1bn sought. The first **£500m tranche** was due by 31 Mar 2024, within a ≈£3.25bn plan to 2030. On **28 Mar 2024** they declined to provide that £500m because the conditions were unmet. The £750m was not "injected".<br>Confirmed:<br>• OMERS 31.7%, written down in full in May 2024;<br>• debt over £20bn at Jan-2026;<br>• the creditor (L&VW) plan writing off more than £13bn of existing value (Sky News, Jan-2026);<br>• Infinity Investments SA (ADIA) 9.9% of Kemble.<br>See R10 for what the case implies. | https://thameswater.co.uk/news/shareholder-update ; https://en.wikipedia.org/wiki/Thames_Water |
| A3 | Q3-2023 crunch (CBRE): LTV 61.4% (58.3% in Q2), cap rate 5.68%, loan constants 6.72% (+79bp), life companies 33.5%, alternative lenders 27.5%, CMBS conduits < 1%. §5 adds: "alternative lenders and banks lead in 2026" | **Corrected (completeness)** | Every number quoted is exact (13 Nov 2023). But the same release says **banks originated 38.4%** of Q3-2023 non-agency volume, the **largest** share and above banks' 30% in Q2-2026. §5 implies banks retreated in the crunch, and CBRE's data do not show that. The regime contrasts that hold are CMBS (< 1% → 11%) and alternative lenders (27.5% → 38%). | https://www.cbre.com/press-releases/commercial-real-estate-lending-market-shows-signs-of-stabilizing-in-q3-2023 |
| A4 | Open-end infrastructure (IFM 2023): redemptions met "from cash yield or queued capital"; units trade on the secondary market at prices set by market conditions, not NAV | **Corrected (attribution)** | The first half is exact for **open-ended** funds (Fig. 2, "Liquidity" row). The sentence "Units can be traded on the secondary market with pricing dependent on market conditions rather than NAV" is in the **closed-ended** column, beside "Entry is restricted to usually 12 months after initial close". §2.5's "not by selling assets" is an inference: IFM lists "asset divestment" as a liquidity source for closed-ended funds only. | https://www.ifminvestors.com/siteassets/shared-media/news--insights-pdfs/tl_ifm065_infra_oce_funds_v8.pdf |
| A5 | CPP Investments: recourse debt 9.7% of adjusted net assets in FY2025, against a Board recourse-leverage limit of 45% of net assets | **Confirmed (S-sec for the limit)** | DBRS: C$76.6bn, which is 9.7% of adjusted net assets (net assets plus recourse debt); also 9.7% in F2024. The 45% Board limit is in S&P (Jan-2023 and Jan-2025 reports), not DBRS, and is measured on net assets, a different denominator. | https://dbrs.morningstar.com/research/457796/morningstar-dbrs-confirms-cpp-investments-at-aaa-and-cppib-capital-inc-at-aaa-and-r-1-high-stable-trends |
| A6 | BREIT met 43% of requests (Nov-22), ≈25% (Jan-23), 35% (Feb-23), 15% (Mar-23) and 29% (Apr-23); limits of 2% a month and 5% a quarter | **Confirmed in part** | Confirmed: Nov-22 43% (SEC 424B3); Feb-23 35%; Mar-23 15% ($666m); Apr-23 29% (≈$1.3bn); the 2% / 5% limits. **Jan-23 "≈25%" was not found**; an SEC filing surfaced in search gives Dec-22 at 4%. Sep-23 and Jun-2024 were not checked. | https://www.bisnow.com/news/national/capital-markets/breit-fulfills-29-of-aprils-45b-withdrawal-requests-marking-a-sixth-limited-month-118746 ; https://www.sec.gov/Archives/edgar/data/1662972/000166297222000143/breitnavnovember2022.htm |
| A7 | Ofwat PR24 notional gearing 55% (60% at PR19), set for BBB+/Baa1 | **Confirmed (secondary)** | The PR24 final methodology (Dec-2022) cut notional gearing from 60% to 55%. Company submissions (Yorkshire, Southern, Wessex) and CCW agree; Yorkshire argues 55% looks more like A2/A3. No Ofwat primary was read. | https://www.ofwat.gov.uk/wp-content/uploads/2022/09/NWG_Setting_Notional_Gearing.pdf |
| A8 | Jefferies: infrastructure secondaries ≈$30bn in 2026 | **Confirmed** | "About $30 billion… up from roughly $20 billion in 2025" (9 Jun 2026). | https://www.jefferies.com/insights/markets/infrastructure-secondaries-hit-their-stride-a-once-niche-corner-of-the-market-could-reach-30-billion-in-2026/ |
| A9 | Open-end unit secondaries in normal markets: −8% to +3% of NAV; 2–6 weeks to execute | **Confirmed** | M. Rzoski, 29 Oct 2020: "from an 8% discount to a 3% premium to NAV"; "between 2-6 weeks to complete". The page does not discuss manager transfer approval explicitly. | https://alliance-globaladvisors.com/blog/transacting-on-the-open-end-fund-secondary-market |

**Tally:** 29 checked: 25 confirmed (S1–S19, A1, A5–A9), 3 corrected (A2, A3, A4), 0 refuted, 1 unverifiable (S20).

## 3. Citation check

**Academic references (metadata from Crossref or OpenAlex).**

| Reference as cited | Exists | Authors | Year | Title | Venue / pages | Note |
|---|---|---|---|---|---|---|
| Jiang, Matvos, Piskorski & Seru, NBER w31970 | Yes | ✓ | Dec-2023, rev. Dec-2024 ✓ | ✓ | NBER WP ✓ | Working paper, not peer-reviewed |
| Chen & Chen (2025), *The writing on the maturity wall* | Yes | ✓ (Jiakai Chen, Yifan Chen) | 9 Jun 2025 ✓ | ✓ | WP ✓ | Hosted on a Berkeley Haas URL; the authors are at the University of Hawaiʻi at Mānoa. Not peer-reviewed. |
| Devaney & Scofield (2015) | Yes | ✓ | ✓ | ✓ | *JPR* 32(4) 362–383 ✓ | Add DOI 10.1080/09599916.2015.1089924. The CentAUR link is bot-walled. |
| Benmelech, Garmaise & Moskowitz (2005) | Yes | ✓ | ✓ | ✓ | *QJE* 120(3) 1121–1154 ✓ | — |
| Black, Krainer & Nichols (2017; online 2016) | Yes | ✓ | ✓ (online 11 Feb 2016) | ✓ | *JREFE* 55(1) 1–31 ✓ | — |
| Bond, Hwang, Lin & Vandell (2007) | Yes | ✓ | ✓ | ✓ | *JREFE* 34(4) 447–461 ✓ | — |
| Chen, Goldstein & Jiang (2010) | Yes | ✓ | ✓ | ✓ | *JFE* 97(2) 239–262 ✓ | — |
| Ciochetti, Deng, Gao & Yao (2002) | Yes | ✓ | ✓ | ✓ | *REE* 30(4) 595–633 ✓ | — |
| Diamond & He (2014) | Yes | ✓ | ✓ (online 2013) | ✓ | *JF* 69(2) 719–762 ✓ | — |
| Fisher, Gatzlaff, Geltner & Haurin (2003) | Yes | ✓ | ✓ | ✓ | *REE* 31(2) 269–303 ✓ | — |
| Lin & Vandell (2007) | Yes | ✓ | ✓ | ✓ | *REE* 35(3) 291–330 ✓ | — |
| Myers (1977) | Yes | ✓ | ✓ | ✓ | *JFE* 5(2) 147–175 ✓ | The dossier says "from memory; not re-checked". It is now checked. |
| Shleifer & Vishny (1992) | Yes | ✓ | ✓ | ✓ | *JF* 47(4) 1343–1366 ✓ | — |

**Industry references.** Each was read at the URL given and exists with the stated publisher and date:
- secondaries: Jefferies (Jul-2026 review; 9 Jun 2026 insight), Campbell Lutyens (Aug-2026);
- open-end real estate: NCREIF (30 Jul 2026), PREA (Kochis & Moné, Winter 2024), Meketa (Jul-2024), Accordant (25 Jun 2026), DTZ (Berry, 8 Dec 2023), Alliance (Rzoski, 29 Oct 2020), IFM (2023);
- debt markets: CBRE (3 Aug 2026; 13 Nov 2023), MBA (9 Feb 2026), Yieldpro (Rudy, 4 Oct 2026), Commercial Observer (McDevitt, 27 Mar 2023);
- energy: Latham & Watkins (22 Apr 2015), Haynes Boone (1 Apr 2020), *Secondaries Investor* (Le, 29 Feb 2016; paywalled);
- other: NBIM mandate (amended 9 Dec 2025), Safehold via Investing.com (30 Jul 2026), DBRS (CPP), Bisnow (BREIT; Brookfield).

**Problems.**
1. **IFM (2023): misattribution.** The secondary-pricing sentence belongs to the closed-ended column (A4).
2. **Tag inflation.**
   - Exec summary item 10 tags the buyer-side taxes (UK 5%, Netherlands 10.4%, Germany 3.5–6.5%, Dubai 4%) as [S]. In §4.5 they are [S-sec] or [P].
   - §6.1 tags the 135-day median [S], while §4.5 tags it [S-sec] and the reference list says "abstract-level check only". It is now confirmed at abstract level, so [S] is acceptable.
3. **The Latham & Watkins reference omits the interviewee** (J. Michael Chambers).
4. **The CPP 45% limit is attributed to "DBRS, S&P"** but appears only in S&P, on a different denominator from DBRS's 9.7% (A5).
5. **Sub-items not found at the cited pages:**
   - real estate LP pricing of 83% in 2019 (the Jefferies chart starts in 2020);
   - the Accordant ≈12% queue for Q3-2025;
   - Safehold's 7.2% for Q1-2026;
   - BREIT's ≈25% for Jan-2023.
6. **The Yieldpro relay contains typos** (S18). Cite Trepp's primary report.
7. **NYS 0.65% can be re-tagged [S]** (tax.ny.gov), and the §8 "evidence gaps" list updated.

## 4. Reasoning issues and overclaims (design implications and specification card)

### Must-fix before the specification card is implemented

**R1. The open-end queue's value cost double-charges time value** (§6.1 "Open-end redemption" row; §6.4 rule 4; code `queue_machine`).
- **What the code does.** Payments are fractions of a NAV held constant at 1 and discounted at ((1+SOFR)(1+ℓ))^(−t/4).
- **Why that is inconsistent.**
  - The code says "NAV = economic". Queued units stay invested: they bear NAV changes and receive income until redeemed.
  - The SELL side of the same script (`lapv`) discounts HOLD cash flows at (1+r_h)(1+ℓ), so the cost of waiting there comes only from ℓ.
  - In the queue, the code's cost at ℓ = 0 is 1.5% / 4.3% / 7.0% (N / T / C), when it should be 0.
- **Corrected values.** Re-running the dossier's own machine with the risk-free leg removed, at ℓ = 10%:

  | Regime | Dossier | Corrected |
  |---|---|---|
  | N | 5.0% | 3.6% |
  | T | 13.9% | 10.3% |
  | C | 21.7% | 16.2% |

  At ℓ = 20% in C, the cost is 28.0%, not 32.4%.
- **Consequence for rule 4.** Selling units at a ≈25% stress bid beats queuing only above ℓ̄ ≈ 17%, not ≈13%. The P5 cash-share columns are unaffected.

**R2. JV stake pricing applies an asset-level discount to levered equity** (§3.1 "SELL: JV stake"; §6.1 JV rows; worked example; code `decision_example`).
- **The inconsistency.** The formula P = ωE(1−d_z)(1−δ^m)(1−f) uses the same regime discount d_z that the direct sale applies to V. If the asset clears at (1−d)V, equity clears at E − dV, a discount of d·V/E on equity. At 40% LTV that is 1.67d.
- **Corrected values** (worked example, code parameters):

  | Quantity | Dossier (N / T / C) | Corrected (N / T / C) |
  |---|---|---|
  | κ_JV | 6.3% / 19.3% / 39.8% | **7.7% / 26.7% / 58.5%** |
  | Cheapest sale in T and C | JV sell-down | SELL 100% (23.5% / 45.9%) |
  | T\* (maturity cash-out) | 1.8 / 5.3 / 7.7 years | ≈2.4 / 6.7 / 9.2 years |
  | T\* (junior capital), N | 0.5 years | ≈0.7 years |

- **Recommendations affected.**
  - The C row "JV sell-down 40% for size … Avoid SELL 100%, 46%" reverses.
  - "Bridge with a JV sell-down (κ 6.3%)" is understated.
  - Exec summary item 3 ("T\* ≈ 1.8 years, matching main §4.4's ≈2 years") holds only by accident of this formula.
- **Fix.** Use (1 − d_z·V/E), or a separate, explicitly equity-level discount.

**R3. Irreversible REFINANCE is priced as a 2-year loan in the merit order** (exec summary item 2: "JV sell-downs and ground leases ≈0.08–0.10"; code `headroom_cost`).
- **What the code does.** It converts every REFINANCE row to headroom cost as ŝ × A(SOFR, 2)/κ₂₄. That includes the ground lease (code T = 30) and the sale-leaseback (T = 15).
- **The contradiction.** §3.1 calls the ground lease "a near-irreversible 99-year senior claim", and the lease cannot be repaid at par after two years.
- **Scale.** Costed over even 10 years at the code's own ŝ ≈ 3.5%, the ground lease's cost is ≈0.34 per $ of headroom. That puts it next to real-estate LP sales (0.37), not core sales.
- **Fix.** Price irreversible financing as permanent (PV of the spread over its life, or a buy-back cost), or as a sale plus a lease liability.

**R4. The default ϖ = 1 is inconsistent with the leverage and encumbrance accounting** (§2.4, §6.3, spec card "ϖ = 1 until ADIC confirms").
- **The tension.**
  - §2.4: with ϖ = 1 "the debt is economically recourse".
  - The code's reputation policy repays loans in full from ADIC's liquidity when no lender exists.
  - Yet §6.3 adds to T5 limit 1 only the P95 of 24-month cures, about $2.8bn in C. That covers only the 40% of debt maturing within 24 months.
  - §6.3 also keeps asset-level pledges out of the encumbrance limit on ring-fencing grounds, which ϖ = 1 waives.
- **Why it matters.** "Look-through debt ≈ the recourse budget" ($15.5bn against $17.7bn). Under the dossier's own default, T5 limit 1 would be close to exhausted by Real Assets alone.
- **Fix: choose one.**
  - (a) Treat ϖ = 1 as an implicit guarantee and count look-through debt in limit 1 at a stated credit-conversion factor.
  - (b) Relabel the P95-cure add-on as a stressed-liquidity measure (O^stress / CLC) and stop calling ϖ = 1 debt "economically recourse".

**R5. The worked example treats "cash-out at maturity" as available today** (§6.4 table; code row "3b").
- The loan has two years to run, so a no-lock-in cash-out exists only at month 24.
- The "Cheapest for a 1-year need: maturity cash-out, κ 4.2%" cells, and the T\* comparisons against sales that close in 4.5–6 months, are valid only for needs that arise at maturity.
- For a need arising now, the menu is early cash-out (κ 26% at 2 years), junior capital, JV sell-down and sale.
- The month-24 headroom metric partly hides this. State the timing condition explicitly.

### Should-fix

**R6. Several levers are not ADIC actions unless ADIC controls the asset.**
- **Affected levers.** Asset-level cash-outs, early refinancing, mezzanine and preferred, ground leases, sale-leasebacks, holdco debt and opco recaps, RBL draws, production-payment sales and hedge monetization (§6.1–6.2).
- **The gap.** §2.1 recognises GP ownership of fund-level decisions. But:
  - the instrument library and the availability table do not gate on control;
  - the hidden-call engine applies asset-level cure decisions to the whole $22.8bn direct and JV book;
  - the code describes the energy sleeve as "co-investments and direct assets".
- **Why it matters.** ADIC's co-investments are typically minority positions alongside GPs, so the sponsor decides financing, hedging and cures. ADIC's exposure is a pro-rata call, if the documents oblige one.
- **Fix.** Add a `control` field (sole / joint / minority / LP) and an availability rule. Minority positions get stake sale, pro-rata cure and consent rights only.

**R7. The Overlay hedge ratio should use N(d2), not N(d1)** (§6.5: h\*_i = Δ_i·floating share_i).
- Δ = N(d1) is the equity's sensitivity to asset value. That is correct for T5 limit 2 exposure.
- A floating-rate shock raises the amount owed, and in Merton ∂E/∂K = −e^(−rT)N(d2).
- At the dossier's settings (σ = 18%, 3 years) the two diverge for distressed assets:

  | LTV | N(d1) | N(d2) |
  |---|---|---|
  | 0.85 | 0.85 | 0.77 |
  | 1.00 | 0.70 | 0.59 |
  | 1.15 | 0.53 | 0.41 |

- So h\* = Δ·share still over-hedges underwater assets. Use [ϖ + (1−ϖ)N(d2)]·share.

**R8. Rate anchors are stale and mixed-dated; ŝ and cap pricing use inconsistent curves.**
- **SOFR.** 3.89% on 15 Oct 2026 is correct (FRED).
- **The benchmark.** The code's 5-year fixed benchmark is SOFR + 70bp = 4.59%. The 70bp is CBRE's **Q2** remark ("a 70-basis-point spread between SOFR and the 5-year fixed rate"), when SOFR averaged ≈3.62%. On 15 Oct 2026 the 5-year UST was 4.91% and the 10-year 5.10%; Q2 averages were 4.09% and 4.42%.
- **Effect on r_new and the lock-in figures.** With UST + 204bp, r_new ≈ 6.95%, not 6.63%. That puts Λ at ≈2.3–5.3% of GAV (not 2.1–4.8%) and r_marg at ≈15.5% (not 14.3%). The direction strengthens "never refinance early", but the N-regime terms are labelled "today" while being Q2 data.
- **Cap pricing.** It assumes a flat forward at spot SOFR, which contradicts the code's own upward-sloping curve. With a 4.25–4.50% average forward, a 3-year 4.5%-strike cap at 110bp costs 1.0–1.3% of notional, not 0.69%. The "≈0.2–1.1%" range is therefore low.
- **ŝ basis.** ŝ = r_fixed − SOFR counts the 5-year term spread (70bp in the code, ≈100bp today) as a liquidity cost compared with ℓ̄. Use a maturity-matched benchmark, or state the convention.
- **Fee basis.** §3.1 charges fees on L_new; the code charges them on (L_new − D).

**R9. Energy borrowing-base capacity in oil-down: the table and the code disagree.**
- §6.2 gives the OD RBL capacity as "0.6–0.8 of the prior borrowing base", citing the 2020 survey of ≥ 20% cuts.
- The code's OD terms imply far less: the advance rate falls from 0.575 to 0.40, NOI falls 15% a year for 2 years, and cap rates rise 200bp. The borrowing base comes out at ≈0.4 of the prior one.
- The OD hidden-call figures ($0.33–0.47bn mean; $1.59–2.02bn P95) rest on the harsher code assumptions.
- **Fix.** Align the two, or present OD as a severe tail beyond the 2020 evidence.

**R10. The Thames Water case is read against the facts** (§5).
- Besides the factual correction (A2), the lesson "politics cut against a ruthless policy" does not match what shareholders did.
- The owners, including ADIA's Infinity (9.9%) and OMERS (31.7%), **declined** the conditional £500m and accepted write-downs.
- The case is a precedent that a Gulf SWF co-owner exercised limited liability. It belongs in the ϖ discussion (open question 3) as evidence that ϖ < 1 is practised, not as support for ϖ = 1.

**R11. "The comonotone sum of cohort P95s is an upper bound" (§7) is not generally true.**
- VaR is not subadditive. Cohorts whose probability of any cash call is below 5% contribute 0 to the sum of P95s, yet can push up the P95 of the total.
- Report CVaR95, which is subadditive (the sum of cohort CVaRs is a true bound), or the joint-path quantile §7 already plans. The §1 table headers should say "sum of cohort P95s".

### Minor

- **R12. q_N = 0.71 is a full-cycle average (2007–2023), not a normal-regime value.** It includes the GFC and 2023 quarters, so "N anchored [S]" overstates the anchoring; queues "were completely paid off nearly 60% of the time". The choice is conservative, but label it.
- **R13. The NBIM precedent is used selectively.** The T5-RA portfolio LTV target of 45% (hard limit 55%) is about twice NBIM's 25% real-estate portfolio cap, and NBIM's renewables 60% is an aim "over time". Reconcile the two, or say why ADIC's book (infrastructure-heavy, fund-level leverage) justifies more.
- **R14. The calibration reproduces 44% and 14% only under its assumptions** (I re-derived both analytically: ≈45% and ≈14.5%).
  - The assumptions are LTV ~ N(62%, 12%), cap₀ 6%, 10% idiosyncratic value volatility and 6% NOI noise over **3 years**. The shock is not uniquely identified, because dispersion trades off against the cap-rate shock.
  - The book then applies +242bp over **2 years** from a 6.5% office cap rate.
  - The CRED iQ 40% early-expiry share comes from transitional CRE-CLO loans and may not transfer to ADIC's floating book.
- **R15. Chen & Chen: implement the 11.1% as −11.1pp** in a refinance-versus-sale share conditional on a transaction, not as a relative cut to an unconditional refinancing hazard. Treat the 12–13% as a discount to refinance **appraisals**, which may be upper-biased.
- **R16. Smaller items.**
  - Cash-out encumbrance "$2.0 per $" assumes 50% LTV, while N-regime LTV^max is 60–65% ($1.5–1.7).
  - "A 30-day row credits every Real Assets lever at 0" conflicts with the day-scale levers listed (hedge monetization, subscription lines). This is conservative but inconsistent.
  - Exec summary item 6 says "40% of its debt matures within 24 months"; the spec card says "40% of **non-energy** debt".
  - The open-end infrastructure statement in §2.5 relies on the misattributed IFM text (A4).

### Arithmetic reproduced and found correct

Each item below matches the dossier and `g14_ra_actions_results.json`:
- **Sale κ:** 3.3% (US), 6.9% (NYC), 8.8% (KSA).
- **Lock-in and marginal rate:** Λ = 2.09% / 4.77% of GAV (2 / 5 years left); r_marg = 14.3%.
- **Δ by LTV:** 1.00 / 0.99 / 0.95 / 0.85 / 0.70 / 0.53 (σ = 18%, 3 years, r = 3.89%).
- **Look-through totals:** GAV $33.5bn; debt $15.5bn (46%; 8.8% of $177bn); equity $18.0bn.
- **ŝ:** 3.2% / 4.4% / 7.2% for cash-outs; 10.0% / 13.6% for mezzanine.
- **LP-sale κ:** real estate 31% (N) and 45% (C); infrastructure 5% (N) and 15% (C).
- **Merit-order conversions:** 0.04 / 0.065 / 0.073 / 0.37.
- **T\*:** 1.8 / 5.3 / 7.7 years, given the code's JV formula (R2).
- **CLC:** $24–42m a year (1.5% × $1.59–2.79bn).
- **Worked example (N):** Λ = $10.5m; JV cash $138m; maturity cash-out $74m.
- **Cap prices:** 0.07–1.12% of notional under the code's flat forward (R8).

## 5. Things the dossier gets right that the IC should hear

- **Market evidence.** The secondary-market, ODCE and debt-market facts are exact to the digit:
  - Jefferies, Campbell Lutyens, NCREIF, PREA, Meketa, CBRE, FRED, MBA and Jiang et al.;
  - FRED's quarter dating is handled carefully;
  - the energy-financing mechanics (semi-annual redeterminations, 3–6-month cures, production payments, hedge-unwind effects) are faithfully sourced.
- **Structural insights hold up.** All of these survive the corrections above:
  - asset-level debt is encumbrance-efficient but procyclical;
  - lock-in value makes early refinancing very costly;
  - caps expiring before maturity create cliffs (Brookfield's 777 Tower default is a live example);
  - internal financing from Private Credit or Capital Solutions raises zero liquidity and strips limited liability;
  - cures should be priced at ℓ̄ under a **declared** default policy.
- **Hygiene.** The dossier separates [S], [S-sec], [P] and [I] carefully (with two tag-inflation exceptions), labels synthetic numbers, and is candid that the search budget ran out.

## 6. Overall reliability rating

| Layer | Rating | Why |
|---|---|---|
| Sourced facts and citations | **HIGH** | 25 of 29 claims confirmed, 3 corrected (none numeric in a flagged claim), 0 refuted, 1 paywalled. All 13 academic references are correct. |
| Design implications and specification card | **MEDIUM** | Five must-fix structural issues (R1–R5). Two of them change recommendations: unit sales against the queue, and JV sell-down against outright sale in stress. Two more change governance treatment: recourse under ϖ = 1, and action availability by control. |
| **Overall** | **MEDIUM** | Safe to cite the market evidence now. Do not adopt the §6.4 thresholds, the merit-order positions of the ground lease and JV levers, or the T5-RA recourse treatment until R1–R6 are fixed and the calculations re-run. |

## 7. Notes for the orchestrator

1. **Dossier text edits:**
   - re-tag NYS 0.65% as [S];
   - correct the Thames Water funding sentence (A2) and the §4.2 IFM row (A4);
   - add banks' 38.4% to the Q3-2023 lender-mix statement (A3);
   - drop or verify "≈12% (Q3-2025)", "83 (2019)", "7.2% (Q1-26)" and "≈25% (Jan-23)".
2. **Code changes in `g14_ra_actions.py`, then re-run:**
   - `queue_machine`: remove the SOFR discount, or accrue NAV at the fund return (R1);
   - `decision_example`: lever the asset discount onto equity in the JV row (R2), and condition the maturity cash-out on the maturity date (R5);
   - `headroom_cost`: price ground leases and sale-leasebacks as permanent (R3);
   - anchor the benchmark on the observed 5-year UST or swap at the pricing date, and price caps off the forward curve (R8).
3. **Market-state flag for the synthesis.** Between the Q2-2026 anchors and 15 Oct 2026 the 5-year UST rose ≈80bp and the 10-year ≈70bp, to 4.91% and 5.10%. CBRE's Q2 lending terms and the July SLOOS predate that move. For rates, the "today" state may sit closer to T than N.
4. **Decision for ADIC (open question 3).** The Thames Water facts (R10) and Brookfield (A1) both show large institutions exercising limited liability. Present ϖ as a genuine choice with precedent on both sides.
