# G5 Public Markets: verification log

**Dossier:** `research/groups/dossiers/G5_public_markets.md` (prepared 2026-10-18). The dossier was not edited.
**Verification date:** 2026-10-18.
**Scope:**
- 40 empirical claims: all 20 the author flagged, plus 20 others chosen because they are load-bearing, marked [nrv]/[ss], or feed calibration targets.
- 30 references (existence, authors, year, title, venue).
- Design implications (§6), the specification card (§6.16), and the worked-example script `research/groups/verification/G5_public_markets_examples.py` with its JSON output.

**Method**
- **OFR Hedge Fund Monitor API**, queried directly: every Form PF series quoted in §4.2 (investor and portfolio liquidity, GAV- and NAV-weighted leverage, GAV- and NAV-weighted cash ratios), plus the mnemonic metadata and the OFR chart definitions.
- **Primary PDFs**, fetched and read or text-extracted locally (pypdf in the project venv, isolated mode):
  - Paul Weiss / Bloomberg mass-redemption primer (Apr 2009);
  - Cambridge Associates (CA), *Is the "Hedge Fund Business Model" Broken?* (Jan 2009);
  - CA, *2024 Hedge Fund Discretionary Expense Summary* (10 Oct 2025);
  - SEC Form PF (current form), investor-liquidity instructions;
  - Eurex, EURO STOXX 50 box-spread paper (Jun 2026).
- **Web pages**, fetched directly:
  - RePEc/IDEAS and NBER abstracts (16 papers);
  - Hedgeweek (5 articles), WealthBriefing (2), Family Wealth Report, InvestmentNews, HedgeCo;
  - Mondo Visione / HFR (2 releases), Reuters via Kitco (2), Bloomberg via TheWealthAdvisor, TheWealthAdvisor (HFR fees);
  - D. E. Shaw; Fed FSR May 2026 (leverage and funding-risk pages); Lovdata (GPFG mandate); NBIM mandate; Man Institute; BarclayHedge (CTA and HF indices); NY Fed SOFR API; FRED DGS10.
- **Web search** (standard mode) was used only where a page would not load or no URL was known: the CME June-2026 roll article (page timed out), ADIC press coverage, HFRI Macro 2025, the Rattray et al. citation, and the Form PF definitions.
- **Consensus:** the `search` tool only, with no authentication tool called. It returned results without sign-in. It was used to confirm Ang & Bollen, Aggarwal & Jorion, Aragon (2007), Jenkinson et al., and Busse–Goyal–Wahal, and to look for related evidence.
- **Arithmetic:** every worked example in §2.2, §4.1, §4.9, §6.5, §6.7 and §6.14 was re-derived independently. The author's script and JSON output were read in full.

---

## 1. Summary

**Sourcing quality is high.**
- Of 40 claims checked: **35 confirmed, 2 corrected, 0 refuted, 3 unverifiable.**
- Of the 20 author-flagged claims, 19 match their sources to the stated precision. One (the ADIC press item) is corrected.
- No fabricated statistics or hallucinated references were found. Every OFR number in §4.2 matches the API to the last decimal.
- Three items can be upgraded from [nrv]/[ss] to [S]:
  - Aragon's (2007) 4–7% lock-up premium (abstract, via Consensus);
  - Jenkinson, Jones & Martinez's "no evidence that these recommendations add value" (abstract, via Consensus);
  - HFRI Macro 2025 +7.2% (HFR's December 2025 release).

**Two factual corrections:**
1. **ADIC $15bn (flagged).**
   - Bloomberg-sourced trade coverage (Hedgeweek, 12 Jun 2026) describes plans *under consideration*, not an adopted plan that ADIC "leads". The Jawlah wording is a paraphrase.
   - The structure has been reported, so "the structure is not public" is wrong. ADIC is said to be working with local banks on **total return swaps (TRS) giving synthetic exposure to a broad hedge-fund portfolio, mainly large multi-strategy funds**.
2. **Fed FSR (semi-liquid credit).**
   - The source says requests were "much larger than 5 percent of NAV", not "well above 5%".
   - It says accepted redemption requests "somewhat exceeded new inflows" in Q1 2026, the first time since these vehicles were created.

**The design layer needs rework before IC use.** The most important problems:
- **R1. Form PF investor-liquidity buckets are not time to cash, and they already assume gates.**
  - The figures in exec-summary item 1 are amounts that can be *noticed* within each window: $1.7bn within a week, $7.1bn within a quarter, and $5.8bn "with crisis gating". They are not cash received.
  - The crisis haircut partly double-counts gates that Form PF filers are told to assume are imposed. Meanwhile payment lags, holdbacks and suspensions are left out.
- **R2. A GAV-weighted leverage figure (12.3×) is used as a calibration target and risk statistic for an LP book.** The leverage per dollar of LP capital is the NAV-weighted mean, 4.5× for multi-strategy. That is 2.75× lower.
- **R3. The §6.8 waterfall program double-counts synthetic cash.** Synthetic notional y is credited with sale proceeds (1 − m − b) in the cash constraint. It is also credited with replacing the beta removed by redemptions in the exposure constraint.
- **R4. Long-only credibility is inconsistent with the dossier's own priors.** On the §6.11 priors, Z(5y) is about 0.10 (DM) to 0.17 (EM/small cap), not 0.36.
- **R5–R8 (medium):**
  - R5: impact extrapolated beyond the square-root law's empirical range;
  - R6: financing tenors mixed in the stress calibration;
  - R7: units in the REFINANCE inequality;
  - R8: actions that are usually not freely available to an LP (rescindable notices, transfers and pledges without consent).

**Overall reliability: HIGH for facts and citations, MEDIUM for design. Overall MEDIUM until R1–R4 are fixed.**

---

## 2. Claims table

**Verdict key.** C = confirmed; Corr = corrected; R = refuted; U = unverifiable. **F** = author-flagged; **A** = added by the verifier.

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| F1 | OFR/Form PF investor liquidity at 30 Jun 2026: 8.4% ≤7d, 27.3% 8–90d, 64.4% >90d. The >90d share was 55.7% (Mar 2013) and 56.2% (Mar 2020) | C | Exact. Dec 2022 (8.1/29.5/62.4) and Mar 2020 (13.0/30.8/56.2) also match. The Mar 2013 short buckets exist (8.5/35.8), though §4.2 shows "—". **See R1 for the definition** (gates assumed; notice-based) | https://data.financialresearch.gov/hf/v1/series/timeseries?mnemonic=FPF-ALLQHF_INVESTORLIQUIDITYGT90_PERCENT ; https://data.financialresearch.gov/hf/v1/series/multifull?mnemonics=FPF-ALLQHF_INVESTORLIQUIDITYLE7_PERCENT,FPF-ALLQHF_INVESTORLIQUIDITYGT7LE90_PERCENT |
| F2 | Multi-strategy GAV-weighted leverage 12.3× (Jun 2026), 6.5× (Mar 2020), 4.1× (Mar 2013). Unencumbered cash fell from 26.8% to 20.3% of NAV | C | 12.291 / 6.454 / 4.089. Cash 26.767 → 20.327 is the **NAV-weighted** mean, in % of net assets. The rest of the §4.2 leverage table (7 strategies × 3 dates, plus the NAV-weighted column) and macro cash (43.9 → 35.1) all match. GAV-weighted multi-strategy cash is only 4.6% of gross assets. **See R2** | https://data.financialresearch.gov/hf/v1/series/multifull?mnemonics=FPF-STRATEGY_MULTI_LEVERAGERATIO_GAVWMEAN,FPF-STRATEGY_MACRO_LEVERAGERATIO_GAVWMEAN,FPF-STRATEGY_RV_LEVERAGERATIO_GAVWMEAN,FPF-STRATEGY_EQUITY_LEVERAGERATIO_GAVWMEAN,FPF-STRATEGY_CREDIT_LEVERAGERATIO_GAVWMEAN,FPF-STRATEGY_FUTURES_LEVERAGERATIO_GAVWMEAN,FPF-STRATEGY_EVENT_LEVERAGERATIO_GAVWMEAN ; https://data.financialresearch.gov/hf/v1/series/multifull?mnemonics=FPF-STRATEGY_MULTI_CASHRATIO_GAVWMEAN,FPF-STRATEGY_MULTI_CASHRATIO_NAVWMEAN,FPF-STRATEGY_MACRO_CASHRATIO_NAVWMEAN,FPF-STRATEGY_MULTI_LEVERAGERATIO_NAVWMEAN |
| F3 | 2008: industry assets −$782bn (−39%) to $1.21trn; net redemptions $399bn (20%), the largest on record (Hennessee) | C | "the largest outflow of assets in the hedge fund history". Performance accounted for −$382bn | https://www.hedgeweek.com/redemptions-and-performance-losses-cut-hedge-fund-assets-usd782bn-says-hennessee/ |
| F4 | Dec 2008 outflows > $100bn. Fund-level gate (e.g. 20%) pro rata; investor-level gates 10–15% per date; suspensions common; PIK and liquidating SPVs used | C | The $100bn is an "estimated outflow". A fund gate gives the sponsor the *option* to pro-rate unless the gate is mandatory. The primer notes investor-level gates were historically uncommon. "Gated 2–4 times, then paid in full" also confirmed. Author: Jennifer A. Spiegel | https://www.paulweiss.com/media/1517346/pw_spgl_apr09.pdf |
| F5 | Secondary discounts "as high as 50%" in extreme cases (Oct 2008, WSJ). Hedgebay average 79.8% of NAV (Dec 2009), range 56–97% | C | Both exact. The FWR "50 per cent" sentence is the article's own; the article draws on WSJ reporting | https://www.familywealthreport.com/article.php/Hedge-Fund-Investors-Use-Secondary-Market-To-Pull-Out-Money-_dash_-Report ; https://www.wealthbriefing.com/html/article.php/hedge-funds-trading-at-historic-discounts-_dash_-hedgebay |
| F6 | Ang & Bollen (2010): 2-year lock-up plus 3-month notice ≈ 1% for CRRA-3; > 10% if the manager can suspend at will | C | Abstract exact (FM 39(3)). An earlier SSRN version, "When Hedge Funds Block the Exits", reports ~4% and ">5% per year". Do not mix versions | https://ideas.repec.org/a/bla/finmgt/v39y2010i3p1069-1096.html |
| F7 | CA 2024 data (pub. 10 Oct 2025): median management fee 1.50% (macro 2.00%, FoHF 0.95%); multi-manager pass-through 0.87–12.99%, mean 5.93%, median 4.53% | C | Exact; 159 funds. 1.50% is the per-strategy median for L/S, credit and multi-strategy; no overall median is published. CA does not state the denominator ("of NAV") or the year for the pass-through range, so those are the dossier's inference | https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2025/10/2025-10-Hedge-Fund-Discretionary-Expense-Summary-2024.pdf |
| F8 | Ben-David, Birru & Rossi: 22 years, 5,917 funds; effective incentive fee 2.5× contractual (~50%); investors keep ~36¢ per $ above risk-free | C | The abstract says investors "collected 36 cents"; 5,917 funds is from the NBER summary. Published in RCFS 15(3), 704–747 (2026) | https://www.nber.org/papers/w27454 |
| F9 | Tremont–TASS merger: hidden survivorship > 5%/yr (1994–2001); ~60% of funds added 1999–2001 were survivors | C | "60 percent ... added ... between April 1999 and November 2001 are likely to be survivors" | https://ideas.repec.org/a/taf/ufajxx/v66y2010i2p69-74.html |
| F10 | Q1 2020: HFRI FWC −9.4%, EH −12.9%, ED −15.3%, Macro +0.1%; S&P 500 −19.6%; loss ratios 0.48 / 0.66 / 0.78 | C | Exact. −19.6% is the S&P 500 total return. Ratios recomputed: 0.480 / 0.658 / 0.781 | https://publishedresearch.cambridgeassociates.com/hedge-fund-update-first-quarter-2020/ |
| F11 | HFRI FWC −19.03% (2008, worst), +20.04% (2009), −4.2% (2022, Macro +9.3%), +12.6% (2025, best since 2009) | C | All exact. The flagged URL supports only 2008–09. The 2022 figures come from HFR via Mondo Visione (also EH −10.2%, HFRI 500 Trend +14.4%, capital $3.83trn); 2025 from WealthBriefing / HFR | https://investmentnews.com/alternatives/hedge-funds-have-best-year-since-1999/26328 ; https://mondovisione.com/media-and-resources/news/hedge-fund-capital-rises-to-conclude-volatile-2022-as-managers-position-for-risk-2023120/ ; https://mondovisione.com/media-and-resources/news/hfri-500-macro-gains-in-december-leads-industry-to-record-outperformance-in-202-2023110/ ; https://www.wealthbriefing.com/html/printarticle.php?id=206626 |
| F12 | S&P 500 implied financing averaged ~0.3% over risk-free in 2021–23 and peaked > 1.4% in Dec 2024 (20-day average); asset-manager demand vs dealer balance sheets | C | Exact; F = S(1+r+s) − E[D] also confirmed. The date (c. 23 Jan 2025) is inferred from the PDF filename | https://www.deshaw.com/library/imbalance-sheet |
| F13 | US equity financing ~200bp over fed funds on 26 Jun 2026 (Morgan Stanley data), highest since Dec 2024; then 89bp on a quarterly-maturity metric; dealer exposure ~$211bn | C | Exact (Reuters). The $211bn is primary dealers' exposure as of 24 Jun (Fed data); the $10trn market size is a Barclays estimate. The 200bp and 89bp are **different metrics and tenors (see R6)** | https://www.kitco.com/news/off-the-wire/2026-07-09/us-markets-brace-renewed-funding-pressure-leverage-rises |
| F14 | 4,617 institutional products (1991–2008): four-factor alphas indistinguishable from zero; persistence weak to none | C | Exact (1,448 firms). Open point: whether these alphas are gross of fees. The 2006 working-paper version implies gross; if so, net ≈ −fee | https://ideas.repec.org/a/bla/jfinan/v65y2010i2p765-790.html |
| F15 | 3,400 plan sponsors (1994–2003) hire after large positive excess returns that do not continue; fired managers do as well as replacements | C | Exact | https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1805-1847.html |
| F16 | Square-root law Δ = Yσ√(Q/V), Y of order unity, holding from ~10⁻⁴ to a few % of daily volume | C | The formula and "of order unity" are exact (§1, Eq. 1). The range is the span of CFM's futures data, "from a few 10⁻⁴ to a few %", not a tested validity bound. **See R5** (applied at 12.5% of ADV) | https://arxiv.org/html/1105.1694v3 |
| F17 | GPFG: rebalance when equity deviates > 2pp from 70%, tested on the last trading day of the month; expected tracking error ≤ 1.25pp | C | §1-6(4) and §2-4(6); the 70% is in §1-5(2). The trigger tests the **actual reference index's** equity share, not the fund's holdings. Last amended 5 Oct 2026 | https://lovdata.no/dokument/INS/forskrift/2010-11-08-1414 |
| F18 | Monthly-rebalanced 60/40 max drawdown 1.2× buy-and-hold (~5pp worse) in 2007–09; trend-informed rebalancing improves drawdowns by 2–3pp | C | Exact. The 2–3pp is the improvement in **average maximum drawdown across five crises**. Article dated 1 Jun 2020 | https://www.man.com/maninstitute/strategic-rebalancing |
| F19 | Citadel limits quarterly withdrawals to 6.25% under certain circumstances (16 quarters); Millennium raised $10bn for a fund with a ≥5-year exit (Bloomberg, Dec 2021) | C | Exact (Burton & Kumar, 6 Dec 2021). The limit applies "under certain circumstances", and a fee can shorten it. Point72 allowed 25%/quarter. **See R9** | https://www.thewealthadvisor.com/article/millennium-citadel-winning-war-keep-client-cash-longer |
| F20 | ADIC "reportedly leads a plan" to deploy up to $15bn into leveraged HF strategies (Jawlah, citing Bloomberg); "structure not public" | **Corr** | Bloomberg (via Hedgeweek, 12 Jun 2026) reports plans **under consideration** to deploy up to $15bn through leveraged structures. ADIC is said to be **working with local banks on total return swaps** for synthetic exposure to a broad HF portfolio, mainly **large multi-strategy funds**. Internal target ≥ 10%; AUM ~$160bn per that report | https://www.hedgeweek.com/abu-dhabis-adic-weighs-15bn-leveraged-hedge-fund-push-via-swap-structures/ ; https://jawlah.co/en/58501 |
| A21 | 2008 detail (CA, Jan 2009): HFRI YTD-Nov FWC −18.18%, EH −26.03%, Distressed −20.77%, Convertible arbitrage −35.50%; Sep −6.12%, Oct −6.44%; ~70% of losses in the 6 weeks after Lehman; 20–25% of capital redeemed at year-end (Morgan Stanley: 15–20% US, 25–30% Europe/Asia); capital calls a named driver; gates "liberally exercised"; GS VIP −19.07% in Q3 2008 | C | All exact. Author: Stephen Tedeschi | https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2014/10/Is-the-Hedge-Fund-Business-Model-Broken-Jan-2009.pdf |
| A22 | Fed FSR May 2026: HF leverage "stable at record-high levels" (Form PF to Q3 2025); skewed to large funds; basis-trade decline offset by swap spreads; March 2026 SCOOS unchanged | C | Exact. The Form PF subsection says "near all-time high levels" | https://www.federalreserve.gov/publications/2026-may-financial-stability-report-leverage.htm |
| A23 | Fed FSR: semi-liquid credit requests "well above 5%"; most capped at 5% of NAV; perpetual BDC redemptions exceeded inflows for the first time | **Corr** | "a number of funds received requests that were much larger than 5 percent of NAV"; "Most managers chose to cap redemptions at 5 percent of NAV"; "Accepted redemption requests somewhat exceeded new inflows in the first quarter of 2026", the first such occurrence since these vehicles were created | https://www.federalreserve.gov/publications/2026-may-financial-stability-report-funding-risks.htm |
| A24 | HFR Q2 2026: record $5.6trn, +$409.3bn ($364bn performance, $45.2bn inflows); H1 inflows $77.2bn (>$5bn managers) vs $2.2bn (small); H1 FWC +7.5%, EH +9.6%, ED +7.4%, Macro +6.1% (systematic +9.7%), RV +3.7% | C | Exact. "Small" means under $1bn; $1–5bn managers took $10.3bn | https://www.hedgeweek.com/hedge-fund-assets-surge-by-record-409bn-to-5-6tn-in-q2/ |
| A25 | Barclay CTA Index: 1987 +57.3%, 2008 +14.09%, 2020 +5.43%, 2022 +7.13%, 2026 YTD +8.69%; 2009–2025 mean 1.89% (sd 3.79%) | C | Exact. Mean 1.886, sample sd 3.791 recomputed. 2026 YTD is an estimate as of 18 Oct | https://portal.barclayhedge.com/cgi-bin/indices/displayCtaIndex.cgi?indexCat=Barclay-CTA-Indices&indexName=Barclay-CTA-Index |
| A26 | S&P 500 futures June-2026 roll +81bp over 3m SOFR, the richest June roll since at least 2007 | C | Confirmed from a search excerpt of the CME article; the page itself timed out | https://www.cmegroup.com/articles/2026/funding-the-us-equity-market-to-new-heights.html |
| A27 | "+38bp in Q2 2025" (same §4.8 row) | U | Not found in the excerpt; page not retrievable | https://www.cmegroup.com/articles/2026/funding-the-us-equity-market-to-new-heights.html |
| A28 | Pass-through economics: Barclays ~42% investor share; 15% of allocators willing to pay pass-through (from > 20%); Balyasny Atlas Enhanced 15.2% gross vs 2.8% net; ExodusPoint 8.4%; Citadel $12.5bn (2022–Sep 2024); BNP 59% retained vs 46% | C | All exact. Reuters words the Barclays figure as managers "take over half of gains back, leaving investors with an average 42% return on investment"; the share-of-gains reading is reasonable | https://www.kitco.com/news/off-the-wire/2024-08-02/hedge-fund-investor-appetite-hit-high-fees-and-private-credit-says ; https://www.hedgeweek.com/hedge-funds-charging-billions-in-no-limit-passthrough-fees/ |
| A29 | HFR Q3 2022 average fees: management 1.35%, incentive 16.01%, lowest since HFR began publishing in 2008 | C | Exact | https://www.thewealthadvisor.com/article/hedge-fund-fees-fall-lowest-level-2008-financial-crisis-hfr |
| A30 | Eurex: 3m EURO STOXX 50 box 223bp vs €STR 210.1bp (2 Jan 2025–31 May 2026), +12.9bp; typically 12–20bp above €STR | C | Exact (text extracted from the PDF) | https://www.eurex.com/resource/blob/5356176/37f5745e27e9eb4f6d033f92c825b610/data/research-paper_eurostoxx50-index-options-box-spreads.pdf |
| A31 | Aragon (2007) lock-up premium ~4–7%/yr (dossier: [nrv]) | C | The abstract says "approximately 4-7% per year higher". **Upgrade to [S]** | https://consensus.app/papers/details/c4b55868f55556a9a6e48db4a364822a/?utm_source=claude_desktop |
| A32 | Jenkinson, Jones & Martinez: consultant recommendations add no value (dossier: [nrv]) | C | The abstract says "no evidence that these recommendations add value" (US active equity). **Upgrade to [S]**. Counter-evidence for HFs: Joenväärä et al. (2026, SSRN) find consultant-recommended hedge funds earn FH7 alpha of 0.70%/yr (R9) | https://consensus.app/papers/details/760c6bf6c8eb5ced8d92754ebb965e73/?utm_source=claude_desktop ; https://consensus.app/papers/details/b7f56cc827ff57d29b6c417e2bfe65b1/?utm_source=claude_desktop |
| A33 | Fung & Hsieh (2000) bias sizes: survivorship ≈ 3%/yr, backfill ≈ 1.4%/yr ([nrv]) | U | The abstract gives no magnitudes; full text not accessed. Keep [nrv] | https://ideas.repec.org/a/cup/jfinqa/v35y2000i03p291-307_00.html |
| A34 | HFRI Macro 2025 +7.2% ([ss]) | C | HFR's December 2025 commentary: +7.2% (asset-weighted +6.9%), from a search excerpt. **Upgrade to [S]** | https://www.hfr.com/media/market-commentary/hfri-surges-to-strongest-annual-gain-since-2009-as-risks-opportunities-evolve/ |
| A35 | SOFR 3.89% (15 Oct 2026) | C | Exact | https://markets.newyorkfed.org/api/rates/secured/sofr/last/10.json |
| A36 | 10y UST 5.09% (16 Oct 2026) | U | FRED DGS10 shows 5.10% on 15 Oct; 16 Oct is not yet published. Consistent | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10&cosd=2026-10-01&coed=2026-10-17 |
| A37 | Hedgebay Illiquid Asset Index 67% of NAV (Jul 2010) | C | "rose to 67 per cent in July, the highest average recorded in nearly a year" | https://www.hedgeweek.com/illiquid-trading-dominates-secondary-market-awaits-locked-funds/ |
| A38 | ~$100bn still locked in a "sliver" of funds (2011) | C | Headline-level only (HedgeCo repost of InvestmentNews, 29 May 2011); the figure is not repeated in the body | https://www.hedgeco.net/news/?p=22752 |
| A39 | Barclay Hedge Fund Index Mar 2026 −3.53%, Apr 2026 +4.41% | C | Exact | https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=Barclay-Hedge-Fund-Indices&indexName=Barclay-Hedge-Fund-Index |
| A40 | NBIM internal mandate: annualised relative ES(97.5%) ≤ 3.75% (amended 9 Dec 2025) | C | §4.1.8; the source states "per cent" | https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/ |

**Tally:**

| Verdict | Count | Rows |
|---|---|---|
| Confirmed | 35 | — |
| Corrected | 2 | F20, A23 |
| Refuted | 0 | — |
| Unverifiable | 3 | A27, A33, A36 |

---

## 3. Citation check

These are the 30 most load-bearing references. All exist with the authors, year, title and venue given unless noted.

| # | Reference (as cited) | Status | Note | Verified at |
|---|---|---|---|---|
| 1 | Ang & Bollen (2010), *Financial Management* 39(3) 1069–1096 | Correct | Abstract magnitudes confirmed; an SSRN predecessor has different numbers | RePEc; Consensus |
| 2 | Aggarwal & Jorion (2010), *FAJ* 66(2) 69–74 | Correct | — | RePEc; Consensus |
| 3 | Ben-David, Birru & Rossi (2020 NBER w27454; *RCFS* 15(3), 2026) | Correct | Pages 704–747 are not given in the dossier | NBER |
| 4 | Busse, Goyal & Wahal (2010), *JF* 65(2) 765–790 | Correct | — | RePEc; Consensus |
| 5 | Goyal & Wahal (2008), *JF* 63(4) 1805–1847 | Correct | — | RePEc |
| 6 | Tóth, Lempérière, Deremble, de Lataillade, Kockelkoren & Bouchaud (2011), *PRX* 1, 021006 | Correct | — | arXiv |
| 7 | Getmansky, Lo & Makarov (2004), *JFE* 74(3) 529–609; NBER w9571 | Correct | Sample of 908 TASS funds confirmed | NBER |
| 8 | Fung & Hsieh (2004), *FAJ* 60(5) 65–80 | Correct | "up to 80 percent" confirmed | RePEc |
| 9 | Spiegel (Paul, Weiss) (2009), "Handling Mass Redemptions: A Primer" | Correct | Bloomberg reprint | PDF |
| 10 | Cambridge Associates (Jan 2009), "Is the 'Hedge Fund Business Model' Broken?" | Correct | Author (Stephen Tedeschi) not named in the dossier | PDF |
| 11 | Cambridge Associates (10 Oct 2025), *2024 Hedge Fund Discretionary Expense Summary* | Correct | — | PDF |
| 12 | Teo (2011), *JFE* 100(1) 24–44 | Correct | 4.79% confirmed | RePEc; Consensus |
| 13 | Dichev & Yu (2011), *JFE* 100(2) 248–263 | Correct | 3–7% confirmed | RePEc |
| 14 | Sadka (2010), *JFE* 98(1) 54–71 | Correct | ~6% (1994–2008) confirmed | RePEc; Consensus |
| 15 | Barras, Scaillet & Wermers (2010), *JF* 65(1) 179–216 | Title truncated | Full title: "False Discoveries in Mutual Fund Performance: Measuring Luck in Estimated Alphas". 75% and "almost none by 2006" confirmed | RePEc |
| 16 | Berk & van Binsbergen (2015), *JFE* 118(1) 1–20 | Correct | $3.2m confirmed | RePEc |
| 17 | Ben-David, Franzoni & Moussawi (2012), *RFS* 25(1) 1–54 | Correct | The abstract says "aggregate portfolio" (13F stock holdings); 29% and 3× confirmed | RePEc |
| 18 | Mitchell & Pulvino (2001), *JF* 56(6) 2135–2175 | Correct | 4%/yr after costs confirmed | RePEc |
| 19 | Aiken, Clifford & Ellis (2015), *JFE* 116(1) 197–218 | Correct | Findings confirmed | RePEc; Consensus |
| 20 | Hombert & Thesmar (2014), *JFE* 111(1) 26–44 | Correct | Findings confirmed | RePEc |
| 21 | Cipriani, Martin, McCabe & Parigi (2014), FRBNY SR 670 | Correct | Theoretical; framed around money funds (R9) | NY Fed |
| 22 | Asness, Krail & Liew (2001), *JPM* | Correct | 1994–2000 "no value" finding confirmed | AQR |
| 23 | Brooks, Gould & Richardson (2020), *Journal of Fixed Income* | Correct | Spring 2020 | AQR |
| 24 | Aragon (2007), *JFE* 83(1) 33–58 | Correct | 4–7% confirmed (Consensus abstract; online 2006) | RePEc; Consensus |
| 25 | Rattray, Granger, Harvey & Van Hemert (2020), *JPM* 46(6) | Correct | pp. 10–31 | Duke Scholars (search) |
| 26 | Jenkinson, Jones & Martinez (2016), *JF* 71(5) 2333–2370 | Exists | Confirmed via SSRN abstract; JF volume and pages not independently checked. **Update 2026-10-18:** Crossref confirms *JF* 71(5):2333–2370, DOI 10.1111/jofi.12289 (literature check, Table A25) | Consensus; Crossref |
| 27 | Fung & Hsieh (2000), *JFQA* 35(3) 291–307 | Correct | Magnitudes are not in the abstract | RePEc; Consensus |
| 28 | Burton & Kumar (Bloomberg, 6 Dec 2021) | Correct | Republished by TheWealthAdvisor | TheWealthAdvisor |
| 29 | Jawlah (11 Jun 2026) | Exists; weak source | Secondary paraphrase ("plan led by ADIC"). Cite the Bloomberg original, or Hedgeweek 12 Jun 2026, for status and structure | Jawlah; Hedgeweek |
| 30 | Fed FSR May 2026; Lovdata GPFG mandate; NBIM mandate; D. E. Shaw "Imbalance Sheet" | Correct | D. E. Shaw date inferred from the filename | Fetched |

**No hallucinated or garbled citations.** Minor citation issues:
- Barras et al. title truncated.
- The CA Jan 2009 author is unnamed.
- Jawlah is a secondary source.
- The HFRI flagged claim cites one URL for four facts from three sources.
- The $100bn (2011) figure appears only in a headline.
- The FWR 50% sentence is not directly attributed to WSJ.
- The OFR cites Form PF "question 50"; the current form numbers the investor-liquidity item differently (53 and 64).

---

## 4. Reasoning issues and overclaims

**Severity scale:**
- **High:** changes an IC-facing number or makes a model wrong.
- **Medium:** biases a parameter or decision rule.
- **Low:** wording, overclaim or notation.

### R1 (High). Form PF investor liquidity is notice-based and already assumes gates, so it is not cash in hand
- **Where:** exec-summary item 1 ($1.7bn within a week; $7.1bn within a quarter; "$5.8bn with crisis gating"); §6.12 target 1; spec card "Industry anchor: 8.4 / 27.3 / 64.4%"; the script's `hf_book_*` outputs.
- **Source:** the current Form PF investor-liquidity instruction reads: "Assume that you would impose gates where applicable but that you would not completely suspend withdrawals/redemptions and that there are no redemption fees. Please base on the notice period before the valuation date rather than the date proceeds would be paid to investors." It adds: "Make a good faith determination of the provisions that would likely be triggered during conditions that you view as significant market stress." (SEC Form PF, https://www.sec.gov/files/formpf.pdf ; OFR definition: https://www.financialresearch.gov/hedge-fund-monitor/categories/liquidity/chart-47/)
- **Problems:**
  - (a) The buckets measure when a redemption can be *effective*, not when cash arrives. The dossier's own terms vector models a payment lag p and a holdback h, and both push cash later. "$7.1bn within a quarter" is therefore an optimistic cash figure.
  - (b) The crisis overlay (25% of the 8–90d bucket deferred) is applied to a measure in which stress-triggered gates are already assumed. This partly double-counts gates. Suspensions, side pockets, payment lags and holdbacks, which Form PF excludes, are still not captured.
  - (c) The figures are NAV-weighted aggregates for qualifying hedge funds (≥ $500m). They are not a proxy for ADIC's own terms.
  - (d) The script's comment mentions "5% of book side-pocketed", but that adjustment is not applied in `crisis_90d`.
- **Fix:**
  - Build ADIC's ladder from τ: notice + dealing date + p + h + gate state.
  - Use OFR only as a sanity range, after converting its buckets to cash timing.
  - Calibrate the synthetic book to Form PF on Form PF's own definition: notice-based, gates on, no suspensions, no fees.

### R2 (High). The GAV-weighted mean is the wrong leverage statistic for an LP's look-through
- **Where:** §1 item 5; §4.2; §6.12 target 1 ("Multi-strategy GAV-weighted leverage of about 12×"); §8 crowding risk.
- **Problem:**
  - The NAV-weighted mean of GAV/NAV equals ΣGAV/ΣNAV, the leverage per dollar of investor capital across a NAV-weighted cross-section. For multi-strategy that is **4.46×** (Jun 2026), against 12.29× GAV-weighted, a ratio of 2.75×.
  - The GAV-weighted mean over-weights the most levered funds. It is the right measure of systemic footprint, not of an LP book's leverage.
  - The dossier also pairs GAV-weighted leverage with NAV-weighted cash (20.3% of NAV). The GAV-weighted cash figure is 4.6% of gross assets.
- **Fix:**
  - Calibrate look-through leverage on NAV-weighted means, or on ADIC's actual holdings.
  - Keep 12× only for stress narratives about the largest platforms. This matters if the reported $15bn programme targets large multi-strategy funds, but it should then be computed holding by holding.

### R3 (High). The §6.8 waterfall program double-counts synthetic cash
- **Where:** §6.8 constraints: cash Σφ_i x_i V_i + Σ(1 − m_m − b_m) y_m ≥ Need, and drift |Σβ_i x_i V_i − Σy_m| ≤ δ.
- **Problem:**
  - The cash constraint treats y_m as a physical-to-synthetic conversion: it sells physical, so each unit of notional frees (1 − m − b).
  - The drift constraint treats y_m as a futures add that replaces the beta removed by sales and redemptions x_i.
  - Both cannot be true. If a long-only x_i and a y_m are used on the same mandate, the sale proceeds are counted twice. If y_m replaces redeemed HF beta, it consumes (m + b)·y_m of cash rather than freeing (1 − m − b)·y_m.
- **Also:**
  - φ_i is overloaded. It is a cost term in the objective and the P5 cash factor in the constraint.
  - The linear φ_i(h)·x_i·V_i ignores that ADIC's own request lowers the payout ratio π_d (the dossier's own reflexivity point in §2.4).
- **Fix:**
  - Use two variables: y^p2s (exposure-neutral; cash +(1 − m − b)) and y^add (exposure +1; cash −(m + b)). Only y^add enters the drift constraint.
  - Rename the objective cost term.
  - Make cash receipt a function of ADIC's share of requests (piecewise), or keep the concentration cap C-PM2 binding.

### R4 (Medium–High). Long-only credibility weights contradict the §6.11 priors
- **Where:** §6.14 ("TE 3%, τ 1%: Z = 0.25 / 0.36 / 0.53"); spec card "Z(5y) ≈ 0.36 (LO)".
- **Problem:**
  - §6.11 sets the DM large-cap prior sd of the true net IR at 0.15 with TE 3%. That gives τ = 0.45%, k = (3/0.45)² = 44.4, and **Z = 0.06 / 0.10 / 0.18** at 3 / 5 / 10 years.
  - For EM and small cap (TE 5%, IR sd 0.20, so τ = 1%), k = 25 and Z = 0.11 / 0.17 / 0.29.
  - The dossier's 0.36 mixes the DM TE with the EM τ. That would over-weight realised long-only alpha by 2–3.5× in the Stream 07 fusion.
- **On the HF side:**
  - Z = 0.465 at 5 years is consistent with the event/credit row (6%, 2.5%).
  - HF Z(10y) is 0.6345, which rounds to 0.63, not 0.64.
  - HF credibility also varies widely by strategy: multi-strategy (4%, 2.5%) gives 0.66 at 5 years; trend (11%, 2.0%) gives 0.14.
- **Also:** compute residual σ on de-smoothed returns. Reported σ understates true σ by 14–36% (§2.2), which inflates Z.

### R5 (Medium). Square-root impact is extrapolated beyond its range and uses index volatility
- **Where:** §1 item 1; §4.9 table; §6.6 c_j(Q,S).
- **Problem:**
  - US small cap at $5bn is 12.5% of assumed ADV, and $2bn is 5%. Tóth et al.'s data run "from a few 10⁻⁴ to a few %".
  - The calculation uses index daily volatility (1.0% for US large cap). Single-name metaorder impact scales with each stock's own volatility, which is well above index volatility because of diversification. Without an explicit cross-impact (market-mode) argument, costs may be understated.
  - The §4.9 statement that spreading a trade "lowers neither expected impact nor cost much" is a within-range property of the square-root law. It does not justify single-day execution of programmes at 5–15% of ADV, where participation limits and impact decay between days matter.
- **Fix:**
  - Cap the formula at a few % of ADV.
  - Above that, use multi-day schedules (Almgren–Chriss) or risk-transfer quotes, as §3 already suggests for > 5% of ADV.
  - Calibrate σ at constituent level, or justify the index-σ choice.

### R6 (Medium). The financing-spread stress calibration mixes metrics and tenors
- **Where:** §6.11 financing table ("CRIS 150–200bp+"); §6.7 stress f = 175bp; §6.12 target 8 ("tail events of 140–200bp [S]").
- **Problem:**
  - The ~200bp print (26 Jun 2026) is Morgan Stanley's short-tenor metric.
  - On the same episode, the quarterly-tenor measures were 81bp (CME roll) and 89bp (Reuters' quarterly-maturity metric).
  - The highest documented quarterly-tenor 20-day average is "over 1.4%" (D. E. Shaw, Dec 2024).
  - For a quarterly-rolled futures REFINANCE, 175bp is a stress *assumption* above any documented 20-day quarterly level. It should be labelled [I], not [S].
- **Fix:** separate tenor-specific series in the financing state f_{b,t}.

### R7 (Medium). The REFINANCE inequality has unit and double-count problems
- **Where:** §6.7 table and spec card: ℓ̄ ≥ f̄ + α̂ + TC/τ + λ_Lev·N/NAV + κ^VM.
- **Problems:**
  - ℓ̄ is per dollar of cash freed, while f̄, α̂ and TC/τ are per dollar of notional. The 1/(1 − m − b) scaling is missing: 1.22× in the normal case and 1.82× in stress. The worked example applies it correctly; the formal rule does not.
  - λ_Lev·N/NAV puts a portfolio-level charge inside a per-unit inequality.
  - κ^VM prices VM outflows that the pre-funded buffer b (already deducted from cash freed) partly covers.
- **Fix:**
  - Express every term per dollar of cash freed per year.
  - Charge leverage on the actual Δ(economic leverage).
  - Price VM only beyond the buffer.

### R8 (Medium). Some actions are not generally available to an LP as modelled
- **Redemption notices as options.** §6.3 and §6.7 say "Notices are options: ladder them early when rescindable". Hedge-fund offering documents commonly make redemption requests irrevocable unless the board or GP consents (verifier inference; the τ vector has no rescindable field).
  - Default to irrevocable and add a `notice_revocable` flag to τ.
  - Treat pre-emptive notices as costly. They signal, and they can trigger gates (the dossier's own Cipriani et al. point).
- **Secondary sale and borrowing against HF units.** Transfers and pledges of HF interests typically need manager consent. Availability should be a τ field and should shrink in CRIS.
- **Leveraged-HF sleeve.** The reported ADIC structure (corrected F20) is a **bilateral TRS on an HF basket with local banks**. That brings:
  - margin on NAV moves;
  - independent amounts;
  - bank early-termination rights;
  - the bank's own gate and suspension exposure on its hedge.

  C-PM4 (HQLA backing) should extend explicitly to HF-TRS collateral. The state machine needs a TRS-termination branch, and the "double-leverage stress" should be specified against TRS terms.

### R9 (Low). Overclaims
- **§4.5.** "Platform liquidity is a fixed amortisation schedule. It does not respond to the market regime." Citadel's 6.25% applies "under certain circumstances" and can be shortened for a fee, and Point72 allowed 25% a quarter. The terms are contingent, not fixed.
- **§2.3.** "Discretionary clauses are worth far more to the manager than lock-ups." Ang & Bollen measure the cost *to the investor*, not the value to the manager.
- **§1 item 2 and §2.4.** Cipriani et al. is stated as fact ("the mere possibility of a gate triggers preemptive runs"). It is a theoretical model framed around money funds; label it as a model prediction.
- **§6.11.** Positive net-IR priors for EM and small cap (0.10) and HY/EMD (0.05) conflict with §1 item 6 ("net alpha between −fee and 0") without cited support. Gerakos, Linnainmaa & Morse (JF 2021) attribute institutional outperformance to factor exposures: https://consensus.app/papers/details/0212f272b5cf5989a5a878405e42c2d3/?utm_source=claude_desktop
- **§6.14 bias table.** Jenkinson et al. covers US active equity. For HF mandates, a 2026 SSRN study finds consultant-recommended hedge funds outperformed (FH7 alpha 0.70%/yr), so the evidence for HFs is mixed.

### R10 (Low). The portable-alpha IM convention is unstated
- **Where:** §6.7 / script, where IM +$0.12bn = (12% − 6%) × $2bn of original notional.
- **Problem:** after a −33% move the notional is $1.34bn. At 12% the increment is about $0.04bn, so the total call is about $0.70bn rather than $0.78bn.
- **Fix:** if CCP IM is set per contract and doubles, $0.12bn holds; state the convention. The error is conservative. R1's caveats also apply to the HF 90-day figures ($0.65 / 0.52 / 0.32bn).

### R11 (Low). Notation and specification nits
- **§6.5 step 3.** π_d is applied unconditionally. It should be 1 when a discretionary gate is not imposed (probability 1 − p^gate).
- **§6.5 gate hazard.** M_i subtracts portfolio liquidity, which OFR measures as a share of **gross** assets, from investor liquidity, a share of **net** assets. Put both on a common base and net out financing that must be repaid as assets are sold.
- **ρ_S.** It is quarterly; convert it per dealing date for monthly funds.
- **§6.7.** The definition of ℓ̄ dangles: it does not appear in the Score formula.
- **§4.4.** The "mid-2009 average discount ~8% after a 20% March peak [ss]" sits awkwardly with WealthBriefing's description of Dec 2009 (~20% discount) as a record low price level.

---

## 5. Arithmetic re-derivation (worked examples)

Every number below was recomputed independently; the author's script reproduces the dossier.

| Item | Result | Status |
|---|---|---|
| GLM table (§2.2) | σ_o/σ 0.863 / 0.735 / 0.644; Sharpe ×1.159 / 1.361 / 1.552; ρ₁ 0.171 / 0.296 / 0.506 | Correct |
| Crisis loss ratios (§4.1) | 0.514, 0.480, 0.658, 0.781, 0.232, 0.564 | Correct. S&P 500 TR −37.0% (2008) and −18.1% (2022) are correct values, though marked [nrv] |
| CTA 2009–2025 | Mean 1.886, sd 3.791 | Correct |
| REFINANCE table (§6.7) | Cash freed $4,115m / $4,015m / $2,750m; costs 0.40–0.70%, 0.80–1.11%, 2.87–3.33% | Correct as computed. See R7 for the formal rule |
| Comparators | NAV loan 5.76% over SOFR; secondary 4.55%/yr (12/88 over 3 years) | Correct. The 3-year amortisation is an arbitrary horizon |
| HF book ladder | $1.68bn / $7.14bn; crisis $5.78bn | Arithmetic correct. Concept wrong (R1) |
| Portable-alpha stress | $0.66bn VM + $0.12bn IM; HF $0.65 / 0.52 / 0.32bn | Arithmetic correct. IM convention per R10 |
| §6.5 sanity check | Two-quarter gate probability 36% (credit/RV), 19% (ED), 7.8% (EqLS), 5.9% (multi), 2.0% (macro); ~17% of book | Correct if the 40% "illiquid" bucket is all credit/RV |
| §6.12 target 5 | $100bn ÷ $1.2–1.5trn = 6.7–8.3% | Correct |
| Credibility (§6.14) | LO 0.25 / 0.36 / 0.53 reproduces the script, but the inputs are inconsistent (R4). HF Z(10y) = 0.634 | R4 |
| Impact table (§4.9) | All cells reproduce (Y = 0.5–1.0) | Arithmetic correct. Domain caveats in R5 |

---

## 6. Overall reliability rating

| Layer | Rating | Basis |
|---|---|---|
| Sourced empirical facts and regulatory text | **High** | 35 of 40 confirmed, mostly to the last digit. 2 corrections, both wording or status; 0 refuted; 3 unverifiable minor items |
| References | **High** | All 30 checked references exist with correct venues. One title truncated; one weak secondary source (Jawlah) |
| Design implications and specification card | **Medium** | R1–R3 change IC-facing liquidity numbers and make the waterfall LP wrong. R4 mis-weights long-only evidence. R5–R8 bias costs and assume actions that are not generally available |

**Overall: MEDIUM.** It becomes HIGH once R1–R4 are fixed and the F20/A23 wording is corrected.

**Reproducibility:**
- Extracted Form PF and Eurex PDFs, and the grep helper `grep_pdf.py`, are in `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\` (subfolders `pdf_formpf`, `pdf_eurex`, `scripts`).
- The OFR series can be re-queried with the API URLs in §2.

---

## Citation corrections (2026-10-18)

The source is the literature audit (`research/literature/00_LITERATURE_SYNTHESIS.md` §2) and its G5 citation-integrity tables (`research/literature/G5_public_markets.lit.md`, Tables A and B). The audit agrees with this log's §3: it found no fabricated or garbled reference, and no reference that this log wrongly accepted, so no erratum is needed.

- §3 row 26: added the Crossref confirmation of *JF* 71(5):2333–2370 and DOI 10.1111/jofi.12289. This closes the open note "volume and pages not independently checked".
- Applied in the dossier (recorded here; this log's findings are unchanged):
  - the A31 (Aragon 4–7%) and A32 (Jenkinson et al.) upgrades to [S];
  - row 3's missing pages 704–747;
  - row 15's truncated Barras et al. title;
  - volume and pages for row 22 (Asness et al., *JPM* 28(1), 6–19) and row 23 (Brooks et al., *JFI* 29(4), 5–19);
  - the DOI for row 25 (Rattray et al., 10.3905/jpm.2020.1.150).
- Found by the literature audit outside the 30 references checked here, and corrected in the dossier:
  - Almgren & Chriss is dated 2001, not 2000 (*J. Risk* 3(2), 5–39);
  - three more shortened titles (Chen–Goldstein–Jiang, Bollen & Pool, Jagannathan et al.);
  - missing volume and pages for Pástor et al. and Getmansky–Lee–Lo;
  - the published version of Dao et al.
- Not applied, because they fall outside the literature audit: A34 (HFRI Macro 2025, [ss] → [S]), the F20 and A23 wording corrections, and design findings R1–R11. They are still open in the dossier.
- Not applicable:
  - the G4 barrier re-run, because this dossier has no barrier statistics;
  - the re-check results for topics 10, 11, 13, 14 and G3, because none of those works is cited here.
