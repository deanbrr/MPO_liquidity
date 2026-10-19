# G7 Liquidity Ladder: Verification Log

- **Dossier checked:** `research/groups/dossiers/G7_liquidity_ladder.md` (stream G7, as of 2026-10-18). The dossier was not edited.
- **Date of check:** 2026-10-18. Adversarial fact-check ahead of the IC pack.
- **Method:**
  - Primary documents were fetched directly and PDFs were text-extracted locally (pypdf). Extractions and scripts are in the session scratchpad.
  - The [I-calc] numbers were re-run from an untouched copy of `g7_liquidity_ladder_calcs.py` (fixed seeds) and diffed against `g7_liquidity_ladder_results.json`.
  - Extra checks were scripted: Basel composition caps on ADIC-LCR(30d); survival with Treasury usable only down to 4% of NAV; an S1 owner draw based on current NAV; the reverse-stress cells.
  - Two classic academic citations were cross-checked in Consensus (§8). Web search was used for 2026 market facts.

---

## 1. Summary

- **Scope:** 34 load-bearing claims were checked: **28 confirmed, 6 corrected, 0 refuted, 0 unverifiable**.
- **The sourced evidence is strong.** The following match the primary text, often verbatim:
  - every regulatory citation: Basel LCR, Reg YY, SR 10-6, the 2023 Addendum, TPR, Directive (EU) 2025/2, FSB, ESMA;
  - every headline market statistic: CPP, OFR Form PF, MSCI, Jefferies, Lazard volume, ISDA, Fleming–Ruela, and Li–Strahan–Zhang's $482bn.
- **Source-level corrections:**
  1. Li–Strahan–Zhang: the post-Lehman ~6% loan rise took **about five weeks** (≈1.2% a week), not three.
  2. Lazard's **"~27% failed or paused" comes from a buyer survey in its GP-led (continuation-fund) section.** It is not a failure rate for LP-portfolio sales, yet the dossier uses it as the red-tier failure probability, as a calibration target and as an EWI threshold.
  3. WilmerHale says only that it was **"possible"** some funds could not be "given away". The dossier states it as fact.
  4. The 2023 Addendum is guidance ("should"). On collateral it asks for planning, not testing.
- **Analysis-level corrections.** These matter more for the IC:
  1. **ADIC-LCR(30d) = 4.5× ignores Basel's Level 2 (40%) and Level 2B (15%) caps.** With the caps it is **≈2.1×**, on the Green/Amber boundary of the dossier's own stage table.
  2. **The 28-month S1 survival assumes a fully usable Treasury.** Under the dossier's own SH_TP(s*) definition (buffer usable only to 4%) it is **17 months, which is the Red stage**.
  3. **S1 draws 10% of *opening* NAV,** about 15% of stressed NAV, while the Monte Carlo draws on current NAV. On current NAV the S1 needs are **$33.3bn / $45.3bn** rather than $36.7bn / $54.1bn.
- **Reproducibility:** every [I-calc] number reproduces exactly (0 differences on rerun). Only small rounding or transcription slips were found (§5).
- **Overall reliability: MEDIUM.** It is high for sourced facts, but the headline synthesis (30-day coverage "ample"; "survival is achievable"; S1 needs) must be restated with fixes R1–R3 before it reaches the IC.

---

## 2. Claims table

| # | Claim (as in dossier) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | CPP one-month LCR 6.9× at 31 Mar 2025 (5.0× a year earlier) vs a 1.0× minimum; horizon moved from 10 days to one month effective 1 Apr 2024 | Confirmed | Note 10.1 table: "Liquidity coverage ratio 1.0x 6.9x 5.0x". Footnote: "Effective April 1, 2024, the Board approved changing the time horizon ... from 10 days to one month". The 2024 comparative is restated ("certain comparatives have been updated"). The definition of liquidity risk is also verbatim. | https://www.cppinvestments.com/wp-content/uploads/attachments/CPP-Investments-F2025-Annual-Report-English.pdf |
| 2 | OFR Form PF qualifying hedge funds, 30 Jun 2026. Investors: ≤7d 8.4%, 8–90d 27.3%, >90d 64.4% (53.9% at end-2019). Portfolio: ≤1d 41.2%, 8–90d 15.9%, >90d 19.3% | Confirmed | All seven values match the OFR API series (FPF-ALLQHF_INVESTORLIQUIDITY* and PORTFOLIOLIQUIDITY*). OFR labels the units "percent of total"; the dossier's "of gross assets" label (§1.6) is unverified. | https://data.financialresearch.gov/hf/v1/series/timeseries?mnemonic=FPF-ALLQHF_INVESTORLIQUIDITYGT90_PERCENT |
| 3 | MSCI global PE contribution/distribution rates: 2020 29/17; 2022 31/11; 2023 27/9; 2025 29/11; H1-2026 31/9, "about one-third of the historical average". All private capital ~10–11% vs ~20% | Confirmed | The table columns are 2017–2025, then 2026 YTD (= H1), then Q2-2026. H1-2026 D/C is 0.9. The full 2017–2026 table in §4.2 matches. Definitions: contribution rate = contributions ÷ (starting dry powder + newly raised capitalisation); distribution rate = distributions ÷ previous valuation; both annualised. | https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf |
| 4 | Li–Strahan–Zhang: C&I loans +$482bn between 11 Mar and 1 Apr 2020, all via drawdowns of existing commitments; vs 0.12% average weekly growth; "~6% in three weeks after Lehman" | **Corrected** | Confirmed: $482bn, the dates, 0.12% (45 years, sd 0.47%), and "all of the increase in lending occurred through drawdowns on existing credit commitments" (an "evidence suggests" finding). **Post-Lehman, lending rose "about 6% during last three weeks of September 2008 and the first two weeks of October, or about 1.2% per week": about 5 weeks, not 3.** March 2020 ran at more than 6% a week. | https://www.nber.org/system/files/working_papers/w27256/w27256.pdf |
| 5 | Mar-2020: 5y/10y Treasury order-book depth fell to ~10% of post-crisis averages; price impact rose ~5–6×; 30y bid-ask exceeded 6× its average | Confirmed | The post says depth fell "as low as 10 percent of their post-crisis averages", price impact reached "roughly 5-6 times", and the 30y spread exceeded "six times". | https://libertystreeteconomics.newyorkfed.org/2020/04/treasury-market-liquidity-during-the-covid-19-crisis.html |
| 6 | Basel LCR parameters: L2A 15%; L2B RMBS 25%, corporates/equities 50%; L2 ≤ 40% and L2B ≤ 15% of HQLA; inflows ≤ 75% of outflows; HQLA unencumbered, periodically monetised and controlled by the liquidity function; usable in stress (LCR20.5) | Confirmed | LCR30.43–30.45 (haircuts); LCR30.42 (40% cap); LCR30.33 (15% cap); LCR40.1 (75% inflow cap); LCR30.15, 30.16 and 30.18 (operational requirements). LCR20.5 verbatim: "it would be entirely appropriate for banks to use their stock of HQLA, thereby falling below the minimum". The ≤40% 30-day equity price-fall condition is also confirmed. | https://www.bis.org/committees/bcbs/basel-framework/LCR/standard.pdf |
| 7 | Basel 30-day drawdown 40% (credit) / 100% (liquidity) for undrawn facilities to other financial institutions (LCR40.64); 0% inflow for facilities held at other institutions | Confirmed | LCR40.64(5)–(6); LCR40.82. *But the prior is not used in the dossier's calculation (R6).* | https://www.bis.org/committees/bcbs/basel-framework/LCR/standard.pdf |
| 8 | Reg YY: overnight, 30-day, 90-day and 1-year horizons; buffer covers the 30-day net stressed need; a line of credit is not a cash-flow source for horizons ≤ 30 days | Confirmed | 12 CFR 252.35(a)(4), (b)(1)–(2) and (a)(5)(iii); scenarios at (a)(3)(i). | https://www.law.cornell.edu/cfr/text/12/252.35 |
| 9 | 2023 Addendum: CFPs "must" recognise lines may become unavailable, and it "requires" regular testing of contingency lines and collateral mobility. SR 10-6 CFP elements | **Corrected (wording)** | The Addendum is supervisory guidance. CFPs "should recognize that during times of stress, contingency lines may become unavailable", and institutions "should regularly test any contingency borrowing lines". On collateral it asks for "planning that recognizes the operational challenges involved in moving and posting collateral", plus pre-pledging and small-value discount-window test transactions; it does not require collateral-mobility testing. SR 10-6 is confirmed: the CFP elements, "delineate policies to manage a range of stress environments", "periodic testing", "liquidity gap analysis", and buckets "daily ... out to weekly, monthly, and quarterly". | https://www.federalreserve.gov/newsevents/pressreleases/files/bcreg20230728a1.pdf ; https://www.federalreserve.gov/boarddocs/srletters/2010/sr1006a1.pdf |
| 10 | ~27% of secondary transactions failed or were paused in H1-2026, when LP-led deals were ~51% of ~$124bn | **Corrected (scope)** | $124bn and LP-led ~51% (GP-led ~49%) are confirmed. **The 27% sits in Section II "GP-Led Deep Dive" (p. 9): "respondents reporting approximately 27% of transactions having failed or been paused in 1H 2026", in a passage on the GP-led and Technology backlog.** It is a buyer-survey figure about (GP-led) transactions, not a measured failure rate for LP-portfolio sale processes. | https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf |
| 11 | H1-2026 LP pricing 87% of NAV (buyout 91%, credit 89%, VC 79%, RE 68%); deferrals in 26% of LP sales | Confirmed | Verified directly, not only via stream 08. Jefferies H1 volume is $118bn with a 47% LP share. | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 12 | GFC: deals priced on pre-YE2008 NAVs traded at ~40% discounts, sometimes 50%+; HarbourVest walked from a signed deal under a MAC (Oct 2008); some unfunded-heavy funds "could not be given away" | **Corrected** | Confirmed: discounts were "averaging around 40 percent and going up to 50 percent or more" for pricing before the 31 Dec 2008 financials. Confirmed as reported: "In October 2008, it was reported that HarbourVest Partners backed out of a signed agreement ... in reliance on a MAC condition". **"Given away" is a forecast in the source ("It is possible that this disconnect will be so extreme that sellers will not be able to 'give away' certain funds"), not an observed event.** §4.1's 'Some funds "given away"' is likewise unsupported. | https://www.wilmerhale.com/-/media/files/wilmerhale_shared_content/files/editorial/publication/blt_ma09_secondarymarket.pdf |
| 13 | Cambridge Associates (Oct 2008): time-to-cash table; gated hedge-fund exits "several years"; credit lines not guaranteed; calls at or above the long-term average; calls-double/distributions-stop scenario | Confirmed | All verbatim (Saviano & Dallas). The report also confirms the money-market fund "breaking the buck", the line of credit as "a liquidity insurance policy", and HFR's 43% fund-of-funds share at 31 Mar 2008. | https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2014/12/Liquidity-Considerations-in-Todays-Environment-Oct-2008.pdf |
| 14 | TPR LDI guidance (24 Apr 2023): ≥250bp market-stress buffer replenishable within five days, plus an operational buffer; collateral typically within five working days | Confirmed | "at a minimum, 250 bps"; "replenish the buffer within five days"; a 100bp operational example (350bp in total); calls met "typically within five working days". | https://www.thepensionsregulator.gov.uk/en/document-library/scheme-management-detailed-guidance/funding-and-investment-detailed-guidance/liability-driven-investment |
| 15 | ISDA (Mar 2026): cash was 68.3% of non-cleared VM received (80% in 2020); CCP VM must be cash; EWIs, stress testing, fire drills and playbooks; $1.5tn non-cleared IM + VM; $389.8bn CCP IM | Confirmed | All verbatim. Also confirmed: "arranging repo and committed liquidity facilities", and FX hedge rollovers and settlement as liquidity drivers. | https://www.isda.org/a/RZtiE/Managing-Liquidity-Risk-Opportunities-and-Challenges-for-Australian-Superannuation-Funds.pdf |
| 16 | Harvard 2008–09: $11bn of commitments through 2018; distributions 56% of FAS income; Dec-2008 $1.5bn taxable at T+335–337.5bp plus $1bn tax-exempt, partly for swap terminations ($330.4m) | Confirmed (citation fix) | The Dec 2008 article confirms the bonds, the spreads, yields of 5.03/6.06/6.53%, the swap-termination use and the $330.4m swap fair value (30 Jun 2008). **The $11bn and 56% are in "Liquidity and Leverage" (Jul 2009), not the Dec 2008 URL cited for the flagged claim.** | https://www.harvardmagazine.com/print/3822?page=all ; https://www.harvardmagazine.com/2009/07/liquidity-leverage |
| 17 | PE calls and distributions are both procyclical, distributions more so; net flows procyclical; PE funds are liquidity sinks when valuations are low | Confirmed | Robinson & Sensoy abstract: "distributions are more sensitive than calls. Net cash flows are therefore procyclical and private equity funds are liquidity providers (sinks) when market valuations are high (low)". JFE 122(3):521–543. | https://www.nber.org/papers/w17428 |
| 18 | Directive (EU) 2025/2: Art. 144a liquidity risk management plan; Art. 144b suspension of redemption rights as a last resort, ≤3 months, renewable | Confirmed | Art. 144a: a short-term plan plus liquidity risk indicators; medium- and long-term analysis where the supervisor requires it ("optional" in §5 is loose). Art. 144b: "last resort"; "no more than three months"; renewable while the reasons persist. OJ 8 Jan 2025. | https://eur-lex.europa.eu/eli/dir/2025/2/oj/eng |
| 19 | Partners Capital: base liquidity funds 7 years of spending; 40% illiquid becomes ~50% in a GFC shock before markdowns | Confirmed | "We budget for base level liquidity to fund 7 years of spending"; "nearly 50% illiquid ... before private assets were marked down or any actions were taken" (c. 42–44% after marks). | https://partners-cap.com/wp-content/uploads/Setting-a-Portfolios-Long-term-Illiquidity-Budget-2.pdf |
| 20 | [I-calc] synthetic results: S1 need $36.7bn / $54.1bn; survival 28 / 14 months; P(red, 5y) 18.1% → 1.2%; LaR95/99 $24.0bn / $33.9bn | Confirmed (reproducible) | The rerun reproduces the results JSON exactly (0 differences), and the dossier matches the JSON to rounding. **Interpretation issues: R1–R3, R5, R7.** | research/groups/addenda/G7_calcs/g7_liquidity_ladder_results.json |
| 21 | "ADIC-LCR(30d) is 4.5×, using Basel haircuts"; short-horizon coverage is "ample" (§1.1, §6.6) | **Corrected** | The calculation omits the Basel composition caps. In the uncapped numerator, L2B is 57% and L2 is 72% (limits 15% and 40%; LCR30.34–30.39). **With the caps the numerator is $13.9bn and the ratio ≈2.10×**, or ≈3.7× only if the whole long-only fixed-income book were Level 1. See R1. | https://www.bis.org/committees/bcbs/basel-framework/LCR/standard.pdf (rerun harness) |
| 22 | S1 survival on Treasury + Public Markets = 28 months, presented as the IC survival result (§1.2, §6.6) | **Corrected** | §6.5 defines SH_TP(s*) with the buffer usable only down to 4% of NAV. **Under that definition the script's own ladder gives 17 months (24 with the CFP pacing cut): Red stage (12–18m), not Green.** See R2. | rerun harness on the G7 script |
| 23 | All firms drew credit lines first; later only the highest-rated tapped markets | Confirmed | "all firms drew down bank credit lines"; "only the highest-rated firms switched to capital markets". | https://www.nber.org/papers/w27601 |
| 24 | March 2020 Treasury evidence "points to forced selling" by leveraged investors | Confirmed | Schrimpf, Shin & Sushko, BIS Bulletin 2 (2 Apr 2020). | https://www.bis.org/publ/bisbull02.htm |
| 25 | The IMF framework reports "cumulated counterbalancing capacity at the end of each maturity bucket" after haircuts and roll-over rates | Confirmed | IMF WP/12/3; authors as cited. | https://www.imf.org/external/pubs/ft/wp/2012/wp1203.pdf |
| 26 | ESMA: a reverse stress test "starts from the identification of the pre-defined outcome"; two principal approaches to asset liquidity | Confirmed | ESMA34-39-897 (16/07/2020): the definitions, and para 43 ("Liquidation cost and time to liquidity are the two principal approaches"). | https://www.esma.europa.eu/sites/default/files/library/esma34-39-897_guidelines_on_liquidity_stress_testing_in_ucits_and_aifs_en.pdf |
| 27 | FSB (10 Dec 2024): eight recommendations (tolerance and CFPs; "extreme but plausible" stress tests; diverse liquid assets; collateral operations; counterparty engagement) | Confirmed | Recommendations 1–3 cover governance, 4–5 stress testing and 6–8 collateral management. | https://www.fsb.org/2024/12/liquidity-preparedness-for-margin-and-collateral-calls-final-report/ |
| 28 | Deferred consideration "typically settles within twelve months" | Confirmed | Evercore H1-2026 review, p. 9. | https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf |
| 29 | Pensions and SWFs supplied 48% of LP volume in H1-2026 [S→08] | Confirmed | Jefferies, Jul 2026. | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 30 | Brent was $126.55 on 14 Oct 2026 [S→03] | Confirmed (label) | The EIA Europe Brent spot FOB price was 126.55 on 14 Oct 2026 (135.51 on 2 Oct). Press reports put ICE Brent futures around $105–110 in mid-October, so **label it "EIA spot"**. | https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RBRTE&f=D |
| 31 | The UAE left OPEC on 1 May 2026 [S→03] | Confirmed | Announced 28 Apr 2026, effective 1 May (WAM via ABC/AP; Enerdata). | https://abcnews.com/Business/wireStory/united-arab-emirates-leave-opec-effective-1-132450136?rand=1513 |
| 32 | H2-2008 average high bid was 61% of NAV (83.5% after public-market adjustment) [S→05] | Confirmed | Unquote (26 Jan 2009), citing Cogent's Winter 2008 interim update. Buyout was 64.7% and VC 55% (Buyouts Insider). PEI describes the window as the five months to Nov 2008. | https://www.unquote.com/uk/news/85756/secondaries-pricing-dips-to-a-five-year-low |
| 33 | Investors would give up ~2% of wealth to hedge once-a-decade illiquidity crises [S→09] | Confirmed | Ang, Papanikolaou & Westerfield (2014): "willing to forgo 2% of their wealth to hedge against illiquidity crises occurring once every 10 years" [C1]. | https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop |
| 34 | The Monte Carlo "uses the stream-04 regime matrix" | Confirmed (internal) | P_Q in the script equals 04's default quarterly matrix (row B 0.85/0.12/0.02/0.01 through row C 0.02/0.08/0.15/0.75). Stream 04 itself warns that a homogeneous chain makes the current 18-quarter drought implausible (p ≈ 0.11). | research/dossiers/04_pe_cashflows.md |

---

## 3. Citation check (most important references)

| Ref | Exists? | Authors, year, title, venue | Issue |
|---|---|---|---|
| CPP Investments F2025 Annual Report | Yes | Correct | The LCR table is in Note 10.1 and the MD&A text matches. The "p. 44" page reference was not checked. |
| OFR Hedge Fund Monitor / Form PF API | Yes | Correct | None. |
| MSCI *Private Capital Benchmarks Summary Q2 2026* | Yes | Correct; author James Wrighton per PDF metadata | None. |
| Lazard *Interim Secondary Market Report 2026* | Yes | Correct | The content is misapplied (claim 10), not the citation. |
| Jefferies *Global Secondary Market Review*, Jul 2026 | Yes | Correct | None. |
| Li, Strahan & Zhang (2020) | Yes | RCFS 9(3):472–500; NBER w27256 | **Title truncated**: the full title adds ": Evidence from the COVID-19 Crisis". |
| Robinson & Sensoy (2016) | Yes | JFE 122(3):521–543; NBER w17428 (Sep 2011) | None. |
| Basel Framework, LCR standard | Yes | Correct; paragraph cites verified (LCR20.5, 30.15–30.18, 30.33, 30.42–30.45, 40.1, 40.64, 40.82) | None. |
| 12 CFR 252.34–252.35 (Reg YY) | Yes | Correct; (a)(3)(i), (a)(4), (a)(5)(iii), (b)(1) | None. |
| SR 10-6 (17 Mar 2010) and Addendum (28 Jul 2023; Fed, FDIC, NCUA, OCC) | Yes | Correct | See the wording nuance in claim 9. |
| Cambridge Associates (Oct 2008) | Yes | Correct | Authors omitted (John-Austin Saviano, Celia Dallas). |
| WilmerHale / ABA *Business Law Today* 18(4), Mar/Apr 2009 | Yes | — | **Garbled**: authors and title omitted. It should read: Beaudoin, T. A., Berrent, J. C., Evans, S. C., & Rothermel, S. (2009), "Trends in the Private Equity Secondary Market: A Response to Today's Financial Markets". |
| Harvard Magazine (19 Dec 2008; 1 Jul 2009) | Yes | Correct; the Dec 2008 title is "Harvard Borrows $2.5 Billion: The Costs and Rationale" | **Claim–source mismatch**: the $11bn and 56% are in the Jul 2009 article. |
| Partners Capital (Miranda & Patel, Q3 2023) | Yes | Correct | None. |
| Acharya & Steffen (2020) | Yes | RCFS 9(3):430–471; NBER w27601 | **Title truncated**: the full title adds "in the Midst of COVID". |
| Schmieder, Hesse, Neudorfer, Puhr & Schmitz (2012) | Yes | IMF WP/12/3 | None. |
| Fleming & Ruela (17 Apr 2020), *Liberty Street Economics* | Yes | Correct | None. |
| Schrimpf, Shin & Sushko (2 Apr 2020), *BIS Bulletin* 2 | Yes | Correct | Title omitted ("Leverage and margin spirals in fixed income markets during the Covid-19 crisis"). |
| TPR (24 Apr 2023); Directive (EU) 2025/2 (OJ 8 Jan 2025); ESMA34-39-897 (16 Jul 2020); FSB (10 Dec 2024); ISDA (Mar 2026) | Yes | Correct | None. |
| Ang, Papanikolaou & Westerfield (2014); Nadauld, Sensoy, Vorkink & Weisbach (2019) | Yes | *Management Science* (DOI 10.1287/mnsc.2014.1986) [C1]; JFE (DOI 10.1016/j.jfineco.2018.11.007) [C2] | None. |

**No hallucinated references were found.** There are three truncated or garbled entries (Li et al., Acharya & Steffen, WilmerHale) and one claim–source mismatch (Harvard).

---

## 4. Reasoning issues and overclaims (design implications and spec card)

### R1 (HIGH): ADIC-LCR(30d) omits the Basel composition caps it claims to follow

- **What the dossier says.** §1.1 and §6.6 present 4.5× "using Basel haircuts", and the author lists the 40% and 15% caps as load-bearing facts.
- **What the code does.** `lcr30_t0()` simply sums the five buckets: L1 cash $4.4bn, UST $3.92bn, L2A IG $4.25bn, L2B DM equity $11.0bn, and long-only fixed income $6.0bn.
- **Composition.** Long-only fixed income gets a 25% haircut, a rate Basel reserves for RMBS. L2B is 57% of the numerator against the 15% cap, and L2 is 72% against the 40% cap.
- **Capped result.** Applying LCR30.34–30.39 gives a numerator of $13.9bn and **LCR ≈2.10×**. Even if the whole long-only fixed-income book were Level 1 sovereigns, it would be only ≈3.7×.
- **Consequence.** 2.1× sits on the Green/Amber boundary (Green ≥ 2.0) of the dossier's own CFP table. "Short-horizon coverage is ample" overstates it.
- **Operational requirements.** The numerator counts DM equities held by external long-only managers (Public Markets). Under LCR30.17–30.18, which §6.11 itself invokes, assets must be under the control of the liquidity function. Commingled holdings would also be T+0–30 (Cambridge Associates), not T+1.
- **Fix.**
  - Apply the caps.
  - Classify long-only fixed income by Basel category.
  - Count only assets that Treasury controls and can monetise inside 30 days, or state the deviation explicitly.

### R2 (HIGH): The survival metric reported is not the metric defined for the IC

- **Definitions.** §6.5 defines SH_TP(s*) as survival under the 24-month named stress with recourse T + P and the **buffer usable down to 4%**. §2.3 makes 4% the hard minimum in stress.
- **What is reported.** §1.2 and §6.6 report 28 months (Treasury usable to 0%) and 14 months (8% floor unusable), but never the defined metric.
- **Recomputed.** The script's own ladder with a 4%-of-NAV floor gives:
  - **S1: 17 months**, which is Red (12–18m) on the stage table;
  - S1 with the CFP pacing cut: 24 months.
- **Consequence.** Under its own design the synthetic book starts in the Red stage for s*. The exec-summary messages "survival is achievable" and "the binding horizon is 24 months" need restating.

### R3 (HIGH): The S1/S2 owner draw is fixed at 10% of opening NAV

- **What the code does.** `run_named()` uses `draw = rate × NAV0`, i.e. $17.7bn a year in S1 (and S2, and in the reverse-stress grid). That is **14.9% of stressed NAV at month 12 and 15.5% in year 2**.
- **Inconsistency.** The Monte Carlo sets the draw as a percentage of current NAV. The exec summary calls S1 "the owner drawing at the 10% cap", which is true only if the mandate is fixed in USD; the dossier itself leaves the draw rule open (§9 Q1).
- **Sensitivity.** With 10% of current NAV, S1 needs **$33.3bn (12m) and $45.3bn (24m)** instead of $36.7bn and $54.1bn. 24-month T + P cover rises from 1.01 to ≈1.21.
- **Fix.** State the S1 draw convention explicitly, reconcile it with the Monte Carlo, and show both.

### R4 (MEDIUM): Lazard's 27% is used as the LP-sale failure rate

- **Where it is used.**
  - the red-tier failure probability (§4.1, §6.9 step 10, the spec card's "~27% failure");
  - a calibration target (§6.12);
  - the survivorship-bias argument (§8);
  - the soft EWI "failed processes > 35%".
- **What the source says.** It is a respondent-reported share of transactions failed or paused, given in Lazard's GP-led deep dive.
- **Fix.** Find an LP-portfolio source, or relabel it as an [I] assumption.

### R5 (MEDIUM): "The price of safety is low" overclaims

- **(a) No standby costs.** The Monte Carlo charges interest only on drawn balances. There are no commitment or unused fees on the $5bn RCF or the pre-arranged NAV facility, and no arrangement fees.
- **(b) Owner's cost ignored.** Policy D cuts the owner draw to 5% in crisis or Red *even when the fiscal-shock state sets it at 10%*. Distribution-inclusive wealth counts draws at face value whatever their timing, so the owner's cost of deferral in its worst fiscal states is ignored. The dossier mentions only the costs that understate the benefit.
- **(c) No forced paydowns.** Facility LTV and availability cuts in crisis never force repayments or cures, because `take()` floors availability at 0. Yet §2.6 and (L6) say ADIC is short lenders' LTV/MAC options.
- **Consequence.** The policy ladder (18.1% → 1.5%) and the "<0.2% wealth difference" are optimistic for policies B–E.

### R6 (MEDIUM): The stated Basel prior for unfunded commitments is not applied

- **What the dossier says.** §2.1 cites Basel's 40%/100% 30-day drawdown as "a conservative prior".
- **What the code does.** The ADIC-LCR(30d) assumes ≈3.8% of regular unfunded commitments a month (`monthly_rate(0.375)`).
- **Sensitivity.** The stated 40% prior would add roughly $12–14bn of outflow. The ratio would be ≈1.5× uncapped and below 1.0× capped.
- **Fix.** Rejecting the bank prior is defensible: GPs call on ~10 days' notice and spread calls across quarters. But the dossier should say it rejects the prior and why.

### R7 (MEDIUM): Liquid-share definitions and stage thresholds are inconsistent

- **Two definitions.** §6.5 defines liquid share as (Treasury + LO + HF ≤ 90d) ÷ NAV, which is 32.8% at t0 on the synthetic book. §1.2 and §6.6 report 40.1% → 17.6% → 9.5% using *all* hedge funds.
- **Two sets of thresholds.** The Monte Carlo stages Amber below 26% and Red below 20%, but the CFP table has Amber at 24–28% and Red at 20–24%.
- **Consequence.** The triggers for policies C–E depend on these thresholds.

### R8 (LOW–MEDIUM): Physical-to-synthetic is mis-modelled in the Monte Carlo

- **What the code does.** In normal quarters DM equity is sold at 0.998 − 4% IM, i.e. treated as a P2S conversion. But the exposure is removed from NAV and no futures notional is added.
- **Consequence.** Contingent VM in later crises is understated, which is the dossier's own pitfall ("creates contingent VM").

### R9 (LOW): CPP peer comparability

- §3 calls the ratios "peer-comparable (CPP)", and §1.1 sets CPP's 6.9× beside ADIC's 4.5×.
- CPP's LCR uses its own undisclosed haircuts and obligation definitions, so the two figures are not comparable.

### R10 (LOW): (L1) is "hard" but carries a slack term

- (L1) is labelled hard, yet it contains u^M_t, as does C1's T1.3.
- Clarify whether u^M is a management-action credit or a penalised slack.

### R11 (LOW): Statements in the exec summary and §4

- "Some funds 'given away'" is a WilmerHale forecast, not an event (claim 12).
- "~6% in three weeks after Lehman" should read about five weeks (claim 4).
- "12-month failures occur only in ... calls ≥ 1.25×" holds only as a necessary condition: of the four cells meeting those conditions, one (distributions 30%, calls 1.25×) passes with cover 1.06.

**LP feasibility of actions.** I found no action that an LP cannot take. Two notes:
- Pledging LP interests to a portfolio NAV facility, and strip or partial transfers, need GP consent and depend on LPA transfer clauses. The dossier lists these clauses as a data need, so the lead time and availability assumptions should be conditioned on them.
- Physical-to-synthetic and T+1 sales assume separately managed accounts, not commingled long-only funds.

---

## 5. Minor numeric slips (rerun JSON vs dossier text)

| Item | Dossier | Rerun |
|---|---|---|
| S1 overlay net, 12m | −6.1 | −6.02. The swing vs B0 is 6.2, not 6.3. |
| Policy C P(red) | 4.5% | 4.445%, which rounds to 4.4% (CI 4.2–4.7 is correct) |
| LCR(12m), S1 + CFP, TPF | 1.52 | 1.51 |
| LCR(12m), S2, TP | 2.65 | 2.66 |
| LCR(12m), S3, TP / TPF | 4.07 / 4.92 | 4.06 / 4.90 |
| Policy D median max illiquid share | 76.3% | 76.25%, which rounds to 76.2% |
| Policy E P(payout shortfall) | 0.29% | 0.295% (≈0.30%) |

All other [I-calc] figures checked match:
- S1 12m/24m need, survival (T 3, TP 28, floor-8 14);
- liquid-share path;
- LCR30 numerator ($29.57bn) and net outflow ($6.60bn);
- group sources and uses;
- P(red) A/B/D/E and their CIs;
- LaR95/99;
- reverse-stress counts (3 and 58 of 96) and covers (0.95, 0.97, 1.21–1.84);
- sensitivities;
- crisis share of first red events (85.8–99.3%).

---

## 6. Not checked (out of scope or low weight)

- GIC, CIC and KIC ~$1bn sale processes [S→05, flagged by the author as coming from search excerpts].
- "53% of LPs" [S→04].
- Yale −6.7% for FY2010 [S→02].
- SWFs withdrawing $46.5bn in 2015 [S→03].
- SOFR, FOMC, 10y UST, VIX and SKEW levels [S→06/09].
- Proskauer and Rede NAV-facility metrics [S→05/08].
- DBRS's $1.5bn facility.
- CalPERS Feb-2026 report details.
- NZ Super quotes.

These sit outside G7's load-bearing set or were already verified by their home streams.

---

## 7. Overall reliability: MEDIUM

- **Evidence layer: high.** 28 of 34 claims are confirmed and none are refuted. The corrections are about scope or wording, apart from the Lehman timing.
- **Synthesis layer: needs revision before the IC.**
  - R1 roughly halves the 30-day coverage message.
  - R2 moves S1 from Green to Red under the dossier's own metric.
  - R3 makes the S1 headline needs depend on an undeclared fixed-USD draw convention that is inconsistent with the Monte Carlo.
  - R4–R7 bias the policy ladder and the stage triggers.
- **Recommendation.** Fix R1–R3, relabel the Lazard 27% and the WilmerHale "given away" points, and restate §1. The design architecture (ladder, nested recourse tiers, CFP stages, testing regime) is sound and well grounded in SR 10-6, Reg YY, Basel and the FSB.

---

## 8. References retrieved via Consensus

- [C1] [Portfolio Choice with Illiquid Assets](https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop) (Ang, Papanikolaou & Westerfield, 2014, *Management Science*, DOI 10.1287/mnsc.2014.1986; 171 citations).
- [C2] [The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop) (Nadauld, Sensoy, Vorkink & Weisbach, 2019, *Journal of Financial Economics*, DOI 10.1016/j.jfineco.2018.11.007; 66 citations).

---

## Citation corrections (2026-10-18)

- **Erratum (literature audit: `research/literature/G7_liquidity_ladder.lit.md` §1–§2; `research/literature/00_LITERATURE_SYNTHESIS.md` §2.4 item 14 and §2.5).** §3 flags three of the eight incomplete academic titles the audit found (Li et al., Acharya & Steffen, Schrimpf–Shin–Sushko) but marks Robinson & Sensoy, Ang et al. and Nadauld et al. "None", although their entries omit titles (Nadauld et al. also volume and pages). Brunnermeier–Pedersen, Bolton–Chen–Wang and the four body-named methods without §10 entries (Glasserman–Kang–Kang, Gerber–Shiu, Little, Clopper–Pearson) are not covered. The log also missed two usage gaps: the Gorton–Metrick haircut spike was in bilateral repo (tri-party margins stayed stable), and Li–Strahan–Zhang's own abstract ties banks' 2020 capacity to Fed liquidity programs, deposit inflows and strong capital (claim 4 confirms the numbers only). All are now fixed in the dossier; see its "Citation corrections (2026-10-18)" section.
