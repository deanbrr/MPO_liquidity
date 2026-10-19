# G13 Real Assets marks and valuation: verification log

*Adversarial fact-check of `research/groups/dossiers/G13_ra_marks_valuation.md` (stream G13: underwritten, appraisal-based current, forecast and market-implied marks; smoothing, bias and credibility). Prepared 2026-10-18. The dossier was not edited.*

## 1. Summary

**What was checked.**
- **30 empirical claims:** the author's 18 flagged claims plus 12 others I judged load-bearing or suspicious (§2).
- **References:** 20 academic references in detail and 14 industry references at document level (§3).
- **Design layer:** the design implications (§2.5, §2.7, §4.3 P2, §5, §6) and the specification card (§6.9), checked for reasoning, formula and action-availability errors (§4).
  - I read the relevant parts of `research/groups/addenda/G13_calcs/g13_ra_marks_sim.py`: the generator's τ (line 165), the Kalman measurement set (`kf_build`), R9 (`test_openend`) and P1–P4 (`public_illustrations`).
  - I re-did the P1, P2, P3 and census arithmetic by hand. Nothing in the project was run or written apart from this log.

**Method.**
- **Primary PDFs.** I downloaded each one myself, extracted the text layer with pypdf (`python -I`, one scratch folder per file), grepped for every number and read the surrounding text.
  - CGR 2024 (accepted version) and the Cannon & Cole MPRA working paper.
  - The Couts working paper (Nov 2022).
  - NCREIF: the NFI-ODCE 2Q-2026 release and the 2Q-2026 webinar slides.
  - Green Street CPPI (6 May 2026) and the Jefferies *Global Secondary Market Review* (Jul 2026).
  - The HICL Annual Report 2026, the SIPA report for GPIF (Sep 2024) and *Oxera Agenda* (Sep 2012).
- **Web pages (WebFetch).** The FCA multi-firm review, the CBRE brief, *Commercial Property Executive*, *Financial Advisor*, and Green Street's 6 Oct 2026 release.
- **Searches.** Used for:
  - the Sovacool et al. abstract (figshare returned 403);
  - BREIT and SREIT November 2022 fills (SEC filings);
  - Nareit fact sheets;
  - the S&P NAV Monitor (S&P page 403; syndicated copy);
  - the CoStar Q1-2025 rent report;
  - the EDHEC survey.
- **Metadata.** Crossref (until it returned HTTP 429), then OpenAlex. Consensus was not used.
- **Scratch.** Session scratchpad, `g13v/` (extraction script and text files).

**Bottom line: the factual layer is very strong.**
- **Flagged claims: all 18 are confirmed** against primary documents, essentially to the digit. Sources:
  - CGR Tables 6–7;
  - Cannon & Cole Tables 2A, 4A and 6–7;
  - Couts working paper, pp. 4–5 and 27–30;
  - the NCREIF release and webinar chart, and Green Street;
  - *Commercial Property Executive* (S&P data), Jefferies p. 5 and the HICL annual report;
  - SIPA/GPIF, Oxera and Sovacool;
  - CBRE, Papastamos et al., the FCA and Barkham & Geltner.
- **Additional claims.** Of the 12, 8 are confirmed, 2 corrected and 2 unverifiable.
  - **Corrected:** the Plazzi et al. overgeneralisation, and the wording of Cannon & Cole's calendar finding.
  - **Unverifiable:** Jefferies' "83% in 2019" and the EDHEC exit premia of 6–20%.
- **Two precision problems in correct numbers:**
  - Cannon & Cole's 12.5% / 8.1% are capital-gain-adjusted, while the −12.0%, +14.7% and +4.9% the dossier pairs with them are unadjusted (§4 S4).
  - BREIT's ≈$1.3bn / ≈43% and SREIT's 63% are true but are not in the cited *Financial Advisor* article (SEC filings carry them).
- **References.** All exist. There is one wrong title (Neuhaus 2025), one omitted co-author (Elliott & Liao 2026) and one mis-sourced set of facts (§3).

**The design layer has three must-fix problems (§4):**
1. **The SELL example is circular.** It presents a lower bound as a point estimate ("the economic discount is 13%, not 32%"); the 13% is just the assumed buyer premium compounded.
2. **The headline nowcast gains rest on an idealised transaction index τ.** In the generator τ is unbiased, unlagged white noise, and its equation is exactly the one the filter assumes. Secondary bids, specified as an observation, are not in the tested filter.
3. **REFINANCE and LEVER rules are not scoped by vehicle.** Asset-level refinancing and acquisition or development debt are not available to ADIC as an LP, and LP fund interests are 63% of the synthetic Real Assets NAV.

There are also seven should-fix and nine minor items.

**Overall reliability:** sourcing and citations **HIGH**; design and specification layer **MEDIUM**; **overall MEDIUM** until M1–M3 are fixed (§5).

## 2. Claims table

S = author-flagged claim; A = additional claim I selected. No claim was refuted.

### 2.1 Flagged claims

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| S1 | CGR, 66 NCREIF private CRE funds, Q1-1994–Q4-2017: fund AC1 0.45, aggregate AC1 0.75. Aggregate AC1 is 0.46 after 1-step and −0.02 after 3-step unsmoothing | **Confirmed** | Exact (Table 6, pp. 2149–50).<br>• Fund AC1 0.45, with 63.6% of funds significant at 10%; fund AC4 0.21.<br>• Aggregate (equal-weighted) AC1 0.75, AC4 0.31.<br>• Aggregate AC1 0.46 after 1-step (AR(2), Geltner; p = 0.0%) and −0.02 after 3-step (p = 86.7%).<br>• Sample: funds with ≥36 uninterrupted quarters. RFS 37(7), 2110–2155. | https://uncipc.org/wp-content/uploads/2024/12/Couts_Goncalves_Rossi_2024RFS_UnsmoothingReturns.pdf |
| S2 | CGR 3-step: volatility 13.1% → 24.1%; β to public CRE 0.07 → 0.34; 1-factor α 4.3% → 1.6%; 2-factor α 4.0% → 0.8% | **Confirmed** | Exact (Table 7, p. 2150).<br>• σ 13.1 → 25.3 → 24.1% (observed → 1-step → 3-step).<br>• 1-factor β_re 0.07 → 0.22 → 0.34; α 4.3 → 2.7 → 1.6%.<br>• 2-factor α 4.0 → 2.4 → 0.8% (β_re 0.02 → 0.15 → 0.21; β_e 0.10 → 0.15 → 0.26).<br>• Public CRE factor: FTSE Nareit All Equity REITs excess return. | https://doi.org/10.1093/rfs/hhae006 |
| S3 | NCREIF NPI sales 1984–2010 against the appraisal two quarters earlier: mean absolute 12.5% (median 8.1%). Signed −12.0% (2008), −8.9% (2009), up to +14.7% (2002–07). More than half of the signed error is systematic | **Confirmed** (precision note) | • Table 4A: 12.5% / 8.1% are **adjusted** for capital gains (unadjusted 13.2% / 8.5%).<br>• Table 2A, by appraisal year, **unadjusted**: 2008 −12.0%, 2009 −8.9%; 1988–93 −2.5% to −8.9%; 1996–99 +2.9% to +9.8%; 2002–07 +3.4% to +14.7% (2005). Adjusted: 2008 −11.0%, 2009 −3.5%.<br>• Abstract: "largely systematic; we can explain more than half of the variation in the signed percentage difference". This is an adjusted R² of 0.507 for the quarterly average error on same-quarter market variables (Table 7); see §4 S4. | https://mpra.ub.uni-muenchen.de/32589/ |
| S4 | Unlisted infrastructure NAV indices: 10-year σ 3.11% (Preqin) and 3.26% (MSCI); MSCI maximum drawdown 0.00%. Fund appraisal-NAV σ 2.7–2.9% (SIPA for GPIF) | **Confirmed** | Exact (p. 8).<br>• Preqin: return 10.41%, σ 3.11%, maximum drawdown 1.37%. MSCI: 13.42%, 3.26%, 0.00%.<br>• 13 funds, c.USD 23.4bn: NAV σ 2.7% / 2.7% / 2.9% over 3 / 5 / 10 years.<br>• The deck gives no end date for the index window, so "to 2024" is inferred. | https://gpif.go.jp/investment/research_20241213_en.pdf |
| S5 | Couts, NFI-OE 2004–15: long-short NAV timing earned a private-RE-factor α of 18.2% before queues. Queue-adjusted returns equal buy-and-hold; buffers amplify the transfer when added to queues | **Confirmed** (working paper) | • Working paper p. 4: index-vs-T-bill α 18.2% (5-factor 15.5%); quintiles 5.9% (3.5%).<br>• Queue-adjusted returns are "statistically and economically equivalent to those of buy-and-hold"; the abstract says "liquidity buffers amplify them when added to liquidity restrictions".<br>• Also exact: subscriptions +18% / 21% / 43% of an SD; median cash 3.6%; 1-SD cash → +25.8% of an SD in outflows (19.8% in the GFC); lock-ups and notice periods ineffective.<br>• Nuance (p. 27): queue-adjusted market-timing returns are about 60% of unconstrained, and only the long portfolio is "no longer different" from buy-and-hold.<br>• The figures come from the Nov 2022 working paper. The 2025 published version was not compared. | https://doi.org/10.1111/1540-6229.12532 ; https://lusk.usc.edu/sites/default/files/working_papers/SSRN-id3445622.pdf |
| S6 | NFI-ODCE 2Q-2026: 1.49% (income 1.02%, appreciation 0.47%); 1-year 4.45%; leverage 27.1%; 25 funds, $223.7bn net; year to June net flows −$8.7bn | **Confirmed** | Exact (release of 30 Jul 2026).<br>• 1-year: 4.08% income + 0.36% appreciation.<br>• Leverage: average since 2000 22.4%, range 15–34%.<br>• $280.4bn gross.<br>• Flows: quarter −$2.8bn; year contributions $10.4bn, distributions and redemptions $19.1bn. | https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf |
| S7 | NFI-ODCE calendar returns from the NCREIF chart: 2022 +7.5%, 2023 −12.0%, 2024 −1.4%, 2025 +3.8%; −18.8% over 7 quarters; REITs −24.95% in 2022 | **Confirmed** | • Webinar slide 5, quarterly totals 1Q22–2Q26: 7.4, 4.8, 0.5, −5.0 / −3.2, −2.7, −1.9, −4.8 / −2.4, −0.4, 0.2, 1.2 / 1.1, 1.0, 0.7, 0.9 / 1.2, 1.5.<br>• Recompounded by hand: +7.5%, −12.0%, −1.4%, +3.8%; 3Q22 → 2Q24 is −18.8% over 7 quarters.<br>• REITs 2022 −24.95% (Nareit Dec-2022 fact sheet).<br>• Comparability: ODCE is a gross, levered (27%) index. | https://ncreif.org/__static/jdj5jdewjc9ybldynw1nwu1tm3u2qnkw/NFI-ODCE-2026q2-Performance-Attribution-Webinar-Slides.pdf |
| S8 | Green Street CPPI (6 May 2026): 130.9, −15.5% from the 2022 peak (office −35%, apartment −19%, industrial −12%). 6 Oct 2026: +4.7% over 12 months | **Confirmed** | • 6 May (April data): 130.9; −0.1% m/m; **+3.1%** y/y; −15.5% (rounded −16%) from peak.<br>• Sectors: office −35%, apartment −19%, industrial −12%, data center −9%, self-storage −22%.<br>• 6 Oct (September data): −0.1% m/m, +4.7% y/y; no from-peak figure given.<br>• The executive summary pairs April's from-peak figure with September's y/y (§4 m1). | https://info.greenstreet.com/hubfs/GSCPPI-20260506press.pdf ; https://www.greenstreet.com/waiting-for-price-clarity/ |
| S9 | US equity REITs at a median 9.35% discount to consensus NAV, 30 Jul 2026 (office 22.37%) | **Confirmed** | Exact. *Commercial Property Executive*, 25 Aug 2026 (modified 16 Sep): 9.35%; industrial 9.87%; office 22.37%. Source: S&P Global Market Intelligence. | https://www.commercialsearch.com/news/2026-reit-trading-trends/ |
| S10 | H1-2026 LP secondary pricing: real estate 68% (83% in 2019), infrastructure 91%, all strategies 87% | **Confirmed** (except the 2019 comparator) | • p. 5: "Real estate pricing settled at 68% of NAV in H1 2026"; infrastructure 91%; all strategies "approximately 87%".<br>• The Fig. 2 real-estate series ends …71, 71, 72, 70, 68 (2022 → H1-26), consistent with the dossier's 71 (2022) and 70 (2025).<br>• The chart starts in **2020**, so "83% in 2019" is not in this report (A3). | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| S11 | HICL, year to 31 Mar 2026: discount rate 8.5% (8.4%); ±0.5% moves NAV −6.8p / +7.4p on 160.2p; share discount 24% (28%); A63 sold at a 21% premium | **Confirmed** | Exact.<br>• Rates: weighted-average discount rate 8.5% (8.4%); ERP 3.5% (3.4%).<br>• NAV and sensitivity: NAV 160.2p (153.1p); ±0.5% DR → (6.8)p / +7.4p ("Valuation sensitivities", PDF p. 51).<br>• Discount: narrowed from 28% to 24%.<br>• A63 (24.0% stake): c.£311m, a 21% premium to the 30 Sep 2025 valuation.<br>• APG PPP portfolio (c.£225m): "in line with HICL's 31 March 2025 valuation".<br>• HICL attributes the 8.4 → 8.5% rise to the A63 sale and growth-asset revaluations (see §4 S3). | https://www.hicl.com/wp-content/uploads/2026/05/HICL-Annual-Report-2026.pdf |
| S12 | Toll-road traffic averaged 23% below forecast across >100 concessions (Bain 2009 via Oxera 2012) | **Confirmed** | Exact (p. 1): "actual traffic volumes being, on average, 23% below the forecast levels for a dataset of more than 100 road, bridge and tunnel concessions". Footnote: Bain (2009), *Transportation* 36(5), 469–82. | https://www.oxera.com/wp-content/uploads/2018/03/Optimism-bias-strategy-and-overbidding2-3.pdf |
| S13 | 401 electricity projects, 57 countries, 1936–2014: mean overrun 66.3% per project; hydro and nuclear worst, solar and wind least risky | **Confirmed** (abstract level) | • 66.3% per project ($388bn in total; $968m mean).<br>• Hydro and nuclear show the greatest amount and frequency of overruns; solar and wind present the least construction risk.<br>• "57 countries, 1936–2014" describes the same dataset in the companion *Energy* 74 (2014) paper.<br>• Full text not accessed (figshare 403). | https://sussex.figshare.com/articles/journal_contribution/An_international_comparative_assessment_of_construction_cost_overruns_for_electricity_infrastructure/23424974 |
| S14 | 2Q-2022 prime multifamily underwriting: 4.3% a year 3-year rent growth (1.8% in 2020), going-in 3.76%, exit 4.43% | **Confirmed** | Exact (21 Jul 2022): 4.3% (4.5% in Q1; 1.8% in the 2020 survey); going-in 3.76% (+39bp); exit 4.43% (+30bp); IRR target 6.04%. | https://www.cbre.com/insights/briefs/prime-multifamily-underwriting-reacts-to-market-volatility |
| S15 | UK real-estate consensus forecasts are smoothed: too low in booms, too high in recessions | **Confirmed** | • Abstract: "Across all of the series, forecasts tend to be smoothed with forecaster's under-estimating performance during economic booms and vice versa in recessions."<br>• "All of the series" includes the macro series, and the abstract says "forecasts", not "consensus".<br>• JRER 40(3), 309–346. | https://doi.org/10.1080/10835547.2018.12091503 |
| S16 | BREIT ≈8.5% in 2022 to October vs public REITs ≈−30%. In Nov-2022 it repurchased ≈$1.3bn (2%-of-NAV monthly limit), ≈43% of each request | **Confirmed**; second sentence mis-sourced | • *Financial Advisor* (6 Dec 2022): BREIT "about 8.5%"; SREIT 10.2%; "public REITs with similar portfolio assets are down around 30%, sources said".<br>• The article does **not** contain $1.3bn, 43% or SREIT's 63%. BREIT's Nov-2022 NAV 424B3 does: repurchases at the 2% monthly limit, ≈$1.3bn, ≈43% of shares submitted. | https://www.fa-mag.com/news/blackstone--starwood-limit-redemptions-as-investors-seek-liquidity-70935.html ; https://www.sec.gov/Archives/edgar/data/1662972/000166297222000143/breitnavnovember2022.htm |
| S17 | FCA (Mar 2025): most firms lacked a formal ad hoc revaluation process and waited for the next cycle; the FCA asks for defined triggers against stale valuations | **Confirmed** | Exact (5 Mar 2025).<br>• "Most firms did not conduct ad hoc valuations and waited for changes to flow through at the next valuation cycle"; "most firms did not have a formal process".<br>• "Firms should consider incorporating a defined process for ad hoc valuations to mitigate the risk of stale valuations."<br>• Infrastructure equity: "All firms used the income approach as their primary methodology". | https://www.fca.org.uk/publications/multi-firm-reviews/private-market-valuation-practices |
| S18 | Price discovery occurs in securitised markets; information takes a year or more to reach US unsecuritised markets | **Confirmed** | Abstract: discovery "occurs in the securitized market structure in both countries" and "does not fully transmit to the unsecuritized markets for a year or more"; the UK link is closer than the US. RE Econ 23(1), 21–44. | https://doi.org/10.1111/1540-6229.00656 |

### 2.2 Additional claims

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| A1 | §2.2: cap rates "are persistent and predict both returns and rent growth" (Plazzi, Torous & Valkanov 2010) | **Corrected** | Cap rates "capture fluctuations in expected returns" for apartments, retail and industrial. For offices they "do not forecast (in-sample) returns" but "marginally forecast office rent growth", and not rent growth for the other types. Design consequence in §4 S2. | https://doi.org/10.1093/rfs/hhq069 (OpenAlex abstract) |
| A2 | §2.4: REITs transmit fundamental information to private markets; passive unlevered core REITs beat their private benchmark by ≈49bp a year, 1994–2012 (Ling & Naranjo 2015) | **Confirmed** (nuance) | • 49bp annualised: confirmed.<br>• REITs "react to fundamental (latent) asset pricing information more quickly than private market returns".<br>• But "REIT returns do not embed additional commercial real-estate-specific information useful in predicting private market returns". The transmission role holds "when asset pricing variables are omitted". | https://doi.org/10.1111/1540-6229.12069 |
| A3 | §4.3: Jefferies real-estate pricing 83% in 2019 | **Unverifiable** | Not in the cited report; Fig. 2 covers 2020–H1-26. Re-source to the Jan-2020 Jefferies review, or drop. | (as S10) |
| A4 | §4.2: EDHEC *Fair Value or Fair Guess?* (Jun 2025): most exits above internal valuations, "predominantly" at 6–20% premiums; only a third adjust valuations in stress | **Unverifiable** | The survey exists (EIPA, *Fair Value or Fair Guess? Inside the Engines of Infrastructure Valuation*, Jun 2025). The cited Mondo Visione page returned an error, and the figures were not found elsewhere. Already tagged [S-sec]. | https://mondovisione.com/media-and-resources/news/edhec-infra-and-private-assets-survey-reveals-serious-flaws-in-private-asset-valua-202579/ |
| A5 | §2.3: about half of NCREIF properties sold in 1984–2010 "had no appraisal in the two quarters before sale" | **Corrected** (wording) | Paper p. 20: "about half of our sold properties had no appraisal two quarters prior to sale, and about one quarter had internal appraisals and one quarter had external appraisals". That is, at the t−2 date the value was carried forward; this does not mean no appraisal in either of the two quarters. | https://mpra.ub.uni-muenchen.de/32589/ |
| A6 | §4.3: S&P REIT discount 16.2% at end-January 2026 and 18.3% at 31 Dec 2025 | **Confirmed** (December implied) | • January: "median 16.2% discount" for equity REITs ≥ $200m (office 33.6%), "2.1 percentage points" lower than December.<br>• So 18.3% is implied (16.2 + 2.1), not printed.<br>• November 2025: 18.2%. | https://seekingalpha.com/article/4867057-nav-monitor-us-reits-end-january-median-16-2-percent-discount-to-net-asset-value |
| A7 | §4.1: REITs 2023 +11.4%, 2025 +2.27%. 2Q-2026: FTSE Nareit +10.7%, NFI-ODCE +1.5%, NPI +1.3% | **Confirmed** | • Nareit: 2023 +11.36% (Dec-2023 fact sheet); 2025 +2.27% (Dec-2025 fact sheet).<br>• Quarter: webinar slide 4 shows 10.7% / 1.5% / 1.3% for the quarter to 6/30/2026. | https://www.reit.com/sites/default/files/2026-01/MediaFactSheet_Dec-2025.pdf |
| A8 | §4.4: US asking-rent growth "just above 1%" a year from mid-2023 into 2025 | **Confirmed** | Apartments.com / CoStar (2 Apr 2025): 1.1% y/y at Mar-2025 (same as Dec-2024), hovering ≈1% since mid-2023; luxury units 0.5%. | https://www.businesswire.com/news/home/20250402768234/en/Apartments.com-Releases-Multifamily-Rent-Report-for-the-First-Quarter-of-2025 |
| A9 | §4.5: SREIT paid 63% of requests in November 2022 | **Confirmed**; mis-sourced | Requests were 3.2% of NAV, honoured pro rata to the 2% limit, so 63% of each request was satisfied (SREIT NAV supplement; CoStar). Not in the cited *Financial Advisor* article. | https://www.sec.gov/Archives/edgar/data/1711929/000095017023008659/0223_nav_supplement.htm |
| A10 | §4.4: infrastructure fund cash flows are as volatile and cyclical as PE (Andonov, Kräussl & Rauh 2021) | **Confirmed** | Abstract: "display similar volatility and cyclicality as other private equity investments". The "633 funds" figure is not in the abstract and was not checked. | https://doi.org/10.1093/rfs/hhab048 |
| A11 | §5.3: SIPA prices unlisted infrastructure with a Kalman filter on factor premia from 1,000+ deals. Segment errors −2.1% to +0.6%; no serial correlation | **Confirmed** (vendor claim) | pp. 11, 15 and 17: errors run from −2.1% (social) to +0.6% (data) on a "sample of 1k+ transaction"; "infraMetrics indices exhibit no serial correlation". | https://gpif.go.jp/investment/research_20241213_en.pdf |
| A12 | §2.2: on a 30-year project a 100bp discount-rate error matters more than a 20% cash-flow error | **Confirmed** | p. 13: "A 100-basis point error in the discount rate is worse that a 20% error in the dividend cash flow forecast!" | (as A11) |

**Tally (30 claims):** 26 confirmed, 2 corrected, 0 refuted, 2 unverifiable.

## 3. Citation check

### 3.1 Academic references

| Reference as cited | Status | Note |
|---|---|---|
| Couts, Gonçalves & Rossi (2024), RFS 37(7), 2110–2155 | Correct | Accepted-version p. 1: received 25 Nov 2020; advance access 9 Mar 2024 |
| Cannon & Cole (2011), JPM 35(5), 68–88, doi 10.3905/jpm.2011.35.5.068 | Correct | Crossref. Working paper: MPRA 32589 (draft of 25 May 2011) |
| Couts (2025), RE Econ 53(5), 1009–1044 | Correct | Crossref; published online 3 Apr 2025 |
| Barkham & Geltner (1995), RE Econ 23(1), 21–44 | Correct | OpenAlex |
| Papastamos, Matysiak & Stevenson (2018), JRER 40(3), 309–346 | Correct | OpenAlex |
| McAllister & Nase (2020), JPR 37(2), 147–170 | Correct | OpenAlex |
| Sovacool, Gilbert & Nugent (2014), ERSS 3, 152–160 | Correct | OpenAlex |
| Bain (2009), *Transportation* 36(5), 469–482 | Correct | OpenAlex; matches Oxera's footnote |
| Lizieri, Satchell & Wongwachara (2012), RE Econ 40(4), 775–807 | Correct | Crossref |
| Ling & Naranjo (2015), RE Econ 43(1), 163–208 | Correct | Crossref (content nuance in A2) |
| Plazzi, Torous & Valkanov (2010), RFS 23(9), 3469–3519 | Correct metadata; content overstated | See A1 |
| Geltner (1993), JRER 8(3), 325–345 | Correct | OpenAlex |
| Clayton, Geltner & Hamilton (2001), RE Econ 29(3), 337–360 | Correct | Crossref |
| Brown, Ghysels & Gredil (2023), RFS 36(3), 945–986 | Correct | OpenAlex lists 2019 (the SSRN year); the published issue is 2023 |
| Andonov, Kräussl & Rauh (2021), RFS 34(8), 3880–3934 | Correct | Crossref |
| Fisher, Gatzlaff, Geltner & Haurin (2003), RE Econ 31(2), 269–303 | Correct | The abstract confirms constant-liquidity values "lead both transaction-based and appraisal-based indices" |
| Quan & Quigley (1991), JREFE 4(2) | Correct | OpenAlex |
| Diaz & Wolverton (1998), RE Econ 26(2), 349–358 | Correct | OpenAlex |
| **Elliott, G. et al. (2026)**, JBES, doi 10.1080/07350015.2026.2661980 | **Author list incomplete** | Two authors: **Graham Elliott and Jie Liao**. Online 23 Jul 2026, pp. 1–13. Title correct |
| **Neuhaus, W. (2025)**, "Parameter-free Benktander-type reserving", SAJ, doi 10.1080/03461238.2025.2536811 | **Wrong title** | The DOI is **"The Benktander Golden Stairs and other parameter-free credibility methods in loss reserving"**, Walther Neuhaus, SAJ (online 4 Aug 2025; 2026(4), 392–411) |

### 3.2 Industry, regulatory and market references

| Reference | Status | Note |
|---|---|---|
| NCREIF NFI-ODCE 2Q-2026 release (30 Jul 2026) | Correct | All figures exact |
| NCREIF 2Q-2026 webinar slides (16 Sep 2026) | Correct | Quarterly bars (slide 5); asset-class table (slide 4) |
| Green Street CPPI, 6 May 2026, "Commercial Property Plods Along" | Correct | |
| Green Street CPPI, 6 Oct 2026 | Correct | Page title "Commercial Property Price Index Dips 0.1% in September" |
| *Commercial Property Executive*, 2026 REIT trading trends | Correct | 25 Aug 2026, modified 16 Sep 2026 |
| Jefferies *Global Secondary Market Review* (Jul 2026) | Correct | The 2019 comparator is not in it (A3) |
| HICL Annual Report 2026 | Correct | |
| SIPA for GPIF (Sep 2024) | Correct | Title: *The Fair Value of Investments in Unlisted Infrastructure Equity – Summary of Report* |
| *Oxera Agenda* (Sep 2012), "Optimism bias, strategy and overbidding" | Correct | Content use partly off (§4 m2) |
| CBRE (21 Jul 2022) | Correct | |
| FCA (5 Mar 2025) | Correct | Quoted phrase verified verbatim |
| ***Financial Advisor*** (6 Dec 2022) | **Partly mis-sourced** | Supports the 8.5%, 10.2% and ≈−30% figures only. The $1.3bn, 43% and SREIT 63% come from BREIT's Nov-2022 NAV 424B3 and SREIT's NAV supplement (SEC) |
| S&P Global NAV Monitor (Feb 2026) | Exists | The S&P page returns 403; title and figure confirmed via the syndicated copy. The 18.3% December figure is implied, not printed |
| EDHEC *Fair Value or Fair Guess?* (Mondo Visione summary) | **Link broken** | Page error. The survey exists; the cited figures are unverified |

## 4. Reasoning issues in the design layer and specification card

### Must-fix

**M1. The SELL example is circular and treats a lower bound as a point estimate** (§6.5 SELL; §1 finding 3; §4.3 P2; spec card "Liquidity and stress").
- **The claim.** "At 68% with θ̂ ≈ 0.78, the economic discount is 13%, not 32%."
- **Why it is circular.** θ̂ ≈ 0.78 is P2's θ = p·[(1+y_P)/(1+y_V)]^D, computed from the same 68% price.
  - Substituting gives 1 − p/θ̂ = 1 − [(1+y_V)/(1+y_P)]^D = 1 − (1.09/1.14)³ = 12.6% for **any** p.
  - The "13%" is the assumed 5-point buyer premium compounded over the assumed 3 years. It says nothing about value or staleness.
- **Why it is biased.** The dossier itself calls P2 an upper bound on staleness, because the 68% also prices liquidity and selection. That makes θ_P2 a **lower** bound on θ, so 1 − p/θ̂ is a **lower** bound on the economic discount.
  - The economic discount therefore lies between ≈13% and 32%: 20% at θ = 0.85, 24% at θ = 0.90, 32% at θ = 1.0.
  - Presenting 13% biases the kernel toward SELL in illiquid markets. That is when the owner's draw is highest, when oil is weak.
- **Production risk.** RAME's bid observation (§3.2: ln q = v − a − D(y_P − y_V) + ε) feeds θ̂. Unless the bid under evaluation is left out, the SELL comparison partly scores the bid against itself.
- **Fix.**
  - State "economic discount ≥ 1 − [(1+y_V)/(1+y_P)]^D (assumption-driven)".
  - Take θ̂ for SELL from the appraisal + listed + τ nowcast, excluding the bid being priced.
  - Add a θ sensitivity row.

**M2. The headline nowcast gains rest on an idealised transaction index; bids are untested** (§1 finding 6; §6.7 R2; spec card "Recovery gates").
- **How τ is generated.** `τ = v̄ + σ_τ·N(0,1)` (line 165). It is unbiased, contemporaneous white noise, and exactly the filter's own τ equation (τ_t = v_t + ε).
  - R3's misspecification variants change λ(z, q) only, never τ.
- **Real τ candidates are not like that:**
  - Green Street's CPPI comes from analysts' NAV models of REIT portfolios: judgmental and partly smoothed.
  - Transaction and repeat-sales indices carry closing lags, liquidity selection and estimation smoothing (Fisher et al. 2003, cited in the dossier).
  - SIPA's infraMetrics is a vendor model, and the dossier itself notes the vendor's interest.
- **Consequence.** "Cuts nowcast error from 8.8–10.8% to 2.5–3.1%" and "Pass with τ (28–33% of appraisal RMSE)" are best cases.
  - The defensible IC figures are listed-only (AL) at 5.3–7.3% and yearly τ (ALT4) at 4.4–6.4%.
  - Use them until a misspecified-τ test is run: lag 1–2 quarters, AR smoothing 0.3–0.5, and a level bias.
- **Bids.** §3.2 and the card's "Nowcast" row list secondary bids as an observation. The implemented filter observes the appraisal, listed and τ series only (`kf_build`, columns 0–2), so the bid channel is specified but untested.

**M3. Action availability is not scoped by vehicle** (§6.2 Decisions; §6.5 REFINANCE / LEVER; spec card "SELL / HOLD / REFINANCE / LEVER").
- **What is asset-level.** The REFINANCE rule (lenders size on D^max = min(LTV^max·A, N/(DSCR^min·k)): cash-out refi, recap, sale-leaseback) and LEVER (acquisition or development debt; half-Kelly on desmoothed σ) are asset-level decisions.
- **Who can take them.**
  - ADIC controls them only in directs and controlled JVs.
  - In closed-end and open-end funds ADIC is an LP, so they are GP decisions.
  - In minority co-investments and many JVs they need GP or partner consent.
- **Scale.** In the G15 census the dossier uses, fund vehicles are $11.4bn of the $18.0bn NAV (63%): RE open-end 2.7, RE closed-end 2.6, infrastructure open-end 2.0, infrastructure closed-end 2.5, energy closed-end 1.6.
  - For these, REFINANCE means a NAV facility on the LP interest, which lenders size on reported NAV.
  - LEVER is not available at holding level; portfolio-level leverage belongs to Corporate Finance (context §1A).
- **Fix.**
  - Add an availability matrix: vehicle {CE, OE, CO, JV, DIR} × action, with control and consent flags.
  - Apply the D^max rule only to DIR and controlled JVs.
  - Size NAV facilities on NAV^rep, with risk on θ^eq.
- **Related taxonomy conflict.** "JV sell-down" sits under REFINANCE, inherited from design brief §8. The user-confirmed definition is "SELL: dispose of the holding, wholly or partly", so a partial stake sale is a partial SELL. Reconcile with G14.

### Should-fix

**S1. The wealth-transfer formula's units are undefined, and P4's arithmetic is off** (§2.5 W; §6.5 open-end option; §4.5 P4).
- **The formula.** W = Σ paid_t(NAV_t/V_t − 1) holds only if paid_t is a fraction of units, measured at true value. That is how R9's code uses it (fund normalised to V = 1), so R9 is consistent.
  - If paid_t is cash paid at NAV — the natural reading, and P4's ("each 2% monthly redemption") — the transfer is paid_t(1 − V_t/NAV_t) = paid_t(1 − θ_t).
- **P4's denominator.** 0.02 × (NAV/V − 1) = 0.40–0.70% is a share of the fund's **true** value. As a share of NAV it is 0.02 × (1 − V/NAV) = **0.34–0.52%**.
- **P4's leverage basis.** P4 sets BREIT's **levered** NAV total return (+8.5%) against an **unlevered** "true" return (½–1 × −30% × (1 − 0.35)). That contradicts the dossier's own θ^eq = (θA − D)/(A − D).
  - On a levered-to-levered basis the equity overstatement would be materially larger than 20–35%.
  - The two errors pull in opposite directions, so the illustration's numbers are unreliable either way. Recompute or drop them.
- **Wording.** §1's "BREIT's NAV was up ≈8.5%" should read total return; the *Financial Advisor* article says "return".

**S2. The cap-rate return formula is applied to every segment** (§2.2; §6.3 step 4 "valuation view"; F-RA2).
- Plazzi et al. find no return predictability from office cap rates, only marginal rent-growth predictability (A1).
- E_t r ≈ h(ȳ+g) + (1 − φ_κ^h)(κ_t − κ̄) assumes cap-rate deviations revert through prices.
- For office (−35% from peak; 22.37% REIT discount) a high κ may signal low expected rent growth instead. The valuation view would then overstate office expected returns and mis-fire F-RA2.
- **Fix:** make the decomposition segment-specific, routing office κ deviations through g.

**S3. The HICL "discount-rate stickiness" calibration target is a portfolio-mix effect** (§6.8).
- "8.4 → 8.5% while its share discount moved 28 → 24%" is not evidence of stickiness:
  - HICL attributes the +10bp to "the sale of the A63 and the increase in the valuation of HICL's growth assets";
  - the listed discount **narrowed**, so the market-implied rate moved toward the appraisal rate.
- **Fix:** use a same-portfolio series (HICL, INPP and peer discount rates against gilt yields, 2021–26) or the SIPA evidence.

**S4. Cannon & Cole is described as "predictable", and the V-RA1 target mixes bases** (§1 finding 1; §4.2; §6.7 V-RA1).
- **"Predictable".** The adjusted R² of 0.507 comes from an in-sample regression of the **quarterly average** signed error on five **same-quarter** market variables: NPI appreciation, number of NPI sales, Δ income return, Δ RERC yield and Δ construction cost.
  - That supports "systematic" and "explained by market observables", not property-level, ex-ante "predictable".
- **Mixed bases.** V-RA1's target "12.5%, +4.9%, −12.0%, up to +14.7%" mixes the adjusted MAE with unadjusted signed figures.
  - Unadjusted: MAE 13.2% (median 8.5%), signed mean +4.9%, 2008 −12.0%, maximum +14.7% (2005).
  - Adjusted: MAE 12.5% (median 8.1%), +3.9%, −11.0%, maximum +11.6% (2006).
- **Fix:** match the generator to one basis, preferably adjusted.

**S5. V-RA1's "Pass" contradicts the spec-card gate** (§6.7; §6.9 synthetic defaults).
- The gate is "appraisal–sale mean absolute 10–14%". VA_RE gives 17.1% (and a boom error of +20.0% against Cannon & Cole's maximum of +14.7%), yet the row says "Pass".
- **Fix:** restrict the gate to CORE_RE (Cannon & Cole is the NPI, mostly core) and add a VA gate, or recalibrate VA σ_e (0.07).

**S6. Overlay hedges at desmoothed betas: the collateral timing is missing** (§6.5 links; spec card "Links").
- A REIT TRS sized on the desmoothed β (0.57 against an observed 0.22 in R3) posts variation margin immediately. Reported NAV, and covenant tests, move 2–6 quarters later.
- In a listed rally the hedge calls collateral against assets whose reported value has not moved, and reported P&L volatility rises.
- This belongs in Corporate Finance's collateral pool and the liquidity gate; Corporate Finance owns overlay VM and IM (context §1A).

**S7. The SIPA inference "implies λ_infra ≥ 0.85" leaves out its assumption** (§6.8).
- With (σ_obs/σ_true)² = (1 − λ)/(1 + λ), λ ≥ 0.85 needs a true unlevered volatility of ≈9.5–11.6% for observed 2.7–3.3%.
- **Fix:** state that assumption and its source.

### Minor

- **m1. CPPI vintages are mixed** (§1 finding 3).
  - "16% below its 2022 peak (office −35%)" is April data (May release); "+4.7% over 12 months" is September data (October release).
  - Y/y rose from +3.1% to +4.7% and August was +0.8% m/m, so the September gap from peak is probably smaller than 15.5%. Date the two figures or update them.
- **m2. Oxera is cited for the winner's curse** (§2.6).
  - Oxera calls it "a popular view", then gives "a strong criticism of the winner's curse theory": the common-value assumption is too restrictive for concessions. It favours optimism bias and strategic bidding.
  - Cite Oxera for those, not for the winner's curse.
- **m3. "Needs ≥10 funds per segment"** (§3.1 table) reads as a CGR result. CGR's aggregation assumes a large cross-section (J → ∞) but states no threshold; tag it [I].
- **m4. Ling & Naranjo** (A2): REITs are a faster channel, not a source of extra CRE-specific information. That supports the listed proxy as a timeliness signal only.
- **m5. "Income … is cash"** (§2.2): NCREIF income returns are NOI-based (accrual). The design point stands.
- **m6. R9's buffer result passes by construction.** The code raises the cap to 2% + cash, so more redemptions are paid at stale NAV. It illustrates Couts's mechanism; it is not independent evidence.
- **m7. The open-end staleness option is an IC policy choice.** Lodging notices when θ̂ < 0.9 is within fund terms, but a sovereign LP systematically timing stale NAVs against co-investors carries GP-relationship and reputational costs. Present it to the IC as a policy choice.
- **m8. The Couts figures come from the 2022 working paper.** The dossier says so, but the 2025 published version should be spot-checked before IC use.
- **m9. Two references** (§3) need fixing: the Neuhaus title and the Elliott & Liao author list. Also re-source the BREIT and SREIT fills to the SEC filings.

**Checked and correct.**
- **Value identity and smoothing algebra:**
  - Var Δa / Var Δv = (1−λ)/(1+λ);
  - the (1−λ)^−2 desmoothed variance;
  - the mean-reversion term (1 − φ^h)(κ − κ̄);
  - the exit-cap arithmetic (75bp at 5% ≈ −3.0pp a year over 5 years).
- **Leverage and bids:**
  - θ^eq = (θA − D)/(A − D) ⇔ θ^eq − 1 = (θ − 1)/(1 − L), and every census row (13.7% … 25.0%);
  - the secondary-bid identity θ = p[(1+y_P)/(1+y_V)]^D, and P2 (0.778 / 0.738 / 1.031 / 0.969).
- **HICL P1:** 11.33% linear and 12.2% power-law.
- **Debt and updating:**
  - D^max with the debt constant k;
  - the scalar Kalman update K = P/(P + σ²).
- **Reserving, calibration and SYN arithmetic:**
  - the Benktander identity c* = 1 − (1 − 1/LDF)², equivalent to iterated BF;
  - κ-to-coverage (1.67 → 56%, 2.0 → 48%, 2.22 → 44%);
  - the R2 ratios (28–33%, 56–68%), the R3 ratios (75–85%; 25–48%) and R7 (+8%, P90 +13%).

## 5. Overall reliability

- **Evidence and sourcing: HIGH.**
  - Every flagged number checks out against the primary document, and no claim is refuted.
  - The corrections are an overgeneralised paper summary (Plazzi et al.), one wording slip, adjusted-versus-unadjusted mixing, and two mis-sourced (but true) figures.
- **Design and specification: MEDIUM.**
  - The core architecture is sound and well supported by the cited literature. It comprises the seven-state appraisal Kalman model, CGR's cross-sectional step, the component bias model with a desmoothed common-shock control, scoring against unsmoothed outcomes, and shrink-to-equal fusion.
  - Three IC-facing statements need fixing first:
    - M1: the SELL economic discount is a lower bound and assumption-driven.
    - M2: the nowcast gains assume an ideal τ.
    - M3: REFINANCE and LEVER are not available to ADIC on its LP fund interests.
- **Overall: MEDIUM until M1–M3 are fixed.** It moves to HIGH once they are, with S1–S7 addressed in the next revision.
