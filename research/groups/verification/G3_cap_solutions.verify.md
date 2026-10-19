# Verification log: G3, Capital Solutions group (structured and hybrid capital)

| | |
|---|---|
| **Dossier** | `research/groups/dossiers/G3_cap_solutions.md` (as of 2026-10-18) |
| **Verified** | 2026-10-18, adversarial fact-check pass (read-only; the dossier was not edited) |
| **Overall reliability** | **MEDIUM overall.** The empirical layer is **HIGH**: 17 of 18 author-flagged claims are confirmed number for number, and the one correction is an attribution. The decision layer is **MEDIUM-LOW**: three high-severity reasoning issues sit under executive-summary conclusions (Section 5). |

---

## 1. Summary

**Coverage.** I checked 35 claims: the 18 author-flagged claims plus 17 others. The others cover:
- statements in the executive summary;
- calibration targets;
- rate inputs;
- platform sizes;
- every worked example in Section 5.6.

**Verdicts.**

| Verdict | Count |
|---|---|
| Confirmed (C) | 27 |
| Corrected (X) | 6 |
| Refuted (R) | 0 |
| Unverifiable (U) | 2 |

**The market-data backbone is accurate.** Every number in the flagged claims traces to the primary document:
- Rede 2026 and 2025;
- Proskauer FY-2025 NAV survey and the Q2-2026 default index;
- Lazard 1H-2026;
- ILPA NAV Part I;
- Blackstone's Q2-2026 10-Q;
- Böni-Manigart (published FAJ text);
- Erel-Flanagan-Weisbach (NBER w32278);
- IMF GFSR April 2024 Ch. 2;
- IPEV 2025;
- the Clifford Chance 2026 briefing;
- the Expedia 8-K.

For the Proskauer survey I also mapped chart bars to labels using text coordinates, because extraction order alone can mislead.

**What needs fixing on the evidence side.**
1. **Misattribution (F11).** The Fed FEDS Note's recovery values (direct loans ~33%, syndicated loans 52%, HY 39%) come from **KBRA DLD** (Figure 15), not from an S&P study. The S&P study cited in that note is about repeat defaults.
2. **Executive-summary error (A1).** "Largest share 5-10%" for Proskauer primary LTVs is wrong per the chart: **10-25% is the largest bucket (36%)**, and 5-10% is 32%. Proskauer's own narrative makes the same error, and the dossier's own table in §4.3 contradicts the summary.
3. **Stale calibration target (A2).** The Fitch event mix to use is now about **47/41/8/4** (12 months to August 2026), not 60/27/6/8. The 6.3% August record, which the dossier tagged [C], is now corroborated (Bloomberg, 14-Sep-2026) and can be upgraded.
4. **Framing corrections.**
   - The IMF does not say competitor supply is pro-cyclical. It says the evidence is "mixed", and that private credit "did not dry up" in March 2020 (A3).
   - Lazard's 14% structured-solutions share is a reversion to 2023-24 levels (14-15%), not growth (A4).

**Must-fix reasoning issues before IC use.** Details are in Section 5.
- **R1. The deploy-vs-wait headline is an artifact.** "A 13% drought deal only breaks even at a 9% liquidity shadow price" holds only if ℓ_D = 9% is charged flat for four years. That contradicts both the dossier's own Markov chain and stream 08's 9/9/4% fallback path. Under either, the break-even drought IRR is about 10.5-11.5%, not 13%.
- **R2. LEVER economics ignore losses and PIK.**
  - The "+1.8pp RoE at D/E 0.5" is computed on the gross 11% contractual yield. On a loss-adjusted basis, alternative-lender leverage *reduces* RoE.
  - At the dossier's own drought PIK share (30%), alternative-lender back-leverage has negative cash carry (−2.3% per dollar of debt).
- **R3. REFINANCE pricing for ADIC's own PE book is calibrated to the wrong product.** It uses GP-level fund NAV facilities (Rede explicitly excludes fund-of-funds and secondary portfolios). As an LP, ADIC can only use LP-level portfolio financing or structured secondaries, which require GP consents and price differently.

---

## 2. Method and limitations

**Method.**
- **PDFs.** Primary PDFs were downloaded, each into its own empty folder, and their text layers extracted with `pypdf` (project venv, `python -I`). The IMF PDF returned 403 to scripted download, so it was obtained through WebFetch's saved binary and then extracted locally.
- **Chart mapping.** Proskauer chart values were mapped to labels with pypdf text coordinates. These are horizontal bar charts, so each value label sits on the same y-coordinate as its category, at an x-position proportional to bar length.
- **Web pages.** Read with WebFetch: SEC 8-K, Fed note (also raw HTML), press releases, Moody's, CFO.com, Funds Society, Bloomberg Law, Investment Executive, The Lead, PE150.
- **Bibliography.** Checked against Crossref (`api.crossref.org`). Consensus search was used for two characterisation checks.
- **Worked examples.** Recomputed with `numpy`/`scipy` (IRR via `brentq`). The script is in the session scratchpad and may not persist: `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g3v\scripts\recompute.py`.
- **Rates.** SOFR from the NY Fed rates API; FOMC decision from the Fed press release.

**Limitations.**
- Fitch's own PCDR reports were not accessed. Fitch values come from Funds Society, Bloomberg Law, Investment Executive, The Lead and PE150. The August event mix (47/41/8/4) rests on PE150 plus search excerpts, so treat it as [C].
- Business Wire returned 403, so the Ares release was read on Stocktitan.
- FRED timed out. The 10-year UST level (5.09%) was **not** checked.
- Not checked: Harvest Partners fact sheet; GTCR (dossier [C]); Goldman Capital Solutions Group (dossier [C]); HPS 2026 fund (dossier [C]); Blue Owl (dossier [C]); Osler 2025; Mayer Brown and Chapman (NAIC); Campbell Lutyens. The Campbell Lutyens and MSCI distribution-rate figures were confirmed against primary documents in the stream-05 and stream-04 verification logs.

---

## 3. Claims table

**Verdict key:** C = confirmed, X = corrected, R = refuted, U = unverifiable. F-numbers are the author-flagged claims; A-numbers are additional claims I selected.

| # | Claim (abridged) | Verdict | Corrected value / verifier note | Source URL |
|---|---|---|---|---|
| F1 | Rede 2026: weighted-average target margin 4.8% secured (5.2%) and 6.1% recourse-light (6.6%); banks 3.0% vs alternative lenders 5.6% secured; banks 60% of volume; 36% expect spreads up vs 17% down; 36 lenders | C | All values are verbatim (PDF pp. 3, 5-6, 11, 13, 15-16). Recourse-light by lender type is also confirmed (banks 4.2%, alternative lenders 6.8%). **Caveats:** these are lender *target* margins from a survey, not realised margins. The 60% bank share is "of reported lending volume on our sample"; banks were 36% of respondents. Rede's scope excludes GP/management-company lending, fund-of-funds and secondary portfolios (relevant to R3). | https://www.rede-partners.com/s/NAV-Financing-Market-Report-2026_FINAL.pdf |
| F2 | Proskauer FY-2025: primary closing LTV <5% 23%, 5-10% 32%, 10-25% 36%; secondaries 25-50% 57%, 50-75% 43%; OID mostly 1-2%; no minimum MOIC in 49%; LTV-based sweeps 63% (primary) and 83% (secondaries); follow-ons 45%, dividend recaps 7% | C | All chart values match (PDF pp. 7, 10-11, 13-14); bar-label mapping checked by coordinates. **Notes:** (a) primary 25%+ is 9%; (b) the text says secondaries close "between 50% and 70%", the chart bucket is 50-75%; (c) a further **15%** of primary respondents report a *combined* use that includes "dividend recap/liquidity to investors", so distribution-related use is up to 22%, not 7% (R13). The 45%/19%/7% pie values are mapped by stream order, which is consistent with the text: follow-on first, debt management "a distant second". | https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025 |
| F3 | NAV-facility market ~US$100bn → US$600bn by 2030 (FFA via ILPA); FFA 80% portfolio support vs 20% distributions; 17Capital US$700bn "opportunity" vs ~US$150bn by 2030 | C | ILPA Part I p. 5 and p. 7 (80/20). **ILPA's footnote 1 cites 17Capital, *In Defence of NAV Financing* (Mar-2024)** for the FFA estimate. 17Capital's homepage: "$700bn NAV finance market opportunity forecast by 2030, resulting in approximately $150 billion deployment per annum", based on Preqin data "with 17Capital assumptions overlayed". Its 1-Sep-2026 article: "about $150 billion by 2030". These are different metrics: addressable opportunity and annual flow vs projected stock. All three figures trace to one vendor (R18). | https://ilpa.org/wp-content/uploads/2024/11/Part-I-Nav-Based-Facilities-Guidance.pdf ; https://www.17capital.com/ ; https://www.17capital.com/insights/structural-drivers-of-a-fast-growing-asset-class |
| F4 | Lazard 1H-2026: preferred and other structured solutions 14% of GP-led volume vs 10% (2025); ~27% failed or paused; DPI/liquidity pressure the top opportunity | C | PDF pp. 9, 11 and 20. The DPI opportunity was chosen by 30% of respondents. **Context:** the same chart gives **14% (2023) and 15% (2024)** (A4). The 27% is respondent-reported, in the GP-led deep dive ("transactions that paused or failed to close in 1H"). | https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf |
| F5 | Blackstone Tac Opps at 30-Jun-2026: US$44.3bn committed incl. co-invest; 1.6x gross MOIC; net IRR 11% total / 16% realised (main funds 10%/15%); BXGP 12% net since 2014 | C | 10-Q printed p. 101: committed US$44,258m; unrealised US$16.6bn at 1.2x; realised US$45.1bn at 1.9x; total 1.6x. Net IRR 16% realised and 11% total; main funds 15%/10%; Co-Investment and Other 18%/15%. MOIC is "before management fees, expenses and Performance Revenues" (fn c), i.e. gross. BXGP Total Net Return 12% (inception 2014); AUM US$13.1bn incl. non-perpetual and co-invest vehicles (fn s). "Thematically driven, hybrid capital investment strategy" is verbatim. | https://www.sec.gov/Archives/edgar/data/0001393818/000119312526340208/d158269d10q1.pdf |
| F6 | Böni-Manigart: 448 funds, Preqin, cut-off Dec-2020; mean net IRR 9.19%; mezzanine 9.04% (median 9.4%, 1.34x); special situations 12.62% (median 8.0%, SD 23.1%); wider ex-ante credit spreads → higher multiples and outperformance; TED spread hurts | C | Published text (open access), Tables 2-3 and pp. 2-4. Every value matches: vintages 1986-2018; distressed 8.37% and 1.37x; direct lending 8.78% (median 7.9%); PME vs HY 1.06; top quartile 23.3%, bottom −3.6%. **Omitted nuance (R4):** performance is "highest when credit spreads expand ex ante and ex post, whilst TED spreads contract". The ex-ante funding-illiquidity effect is "more than twice as large as that of performance persistence". | https://www.tilburguniversity.edu/sites/default/files/download/B%C3%B6ni_Manigart_2022_Private%20Debt%20Fund%20Returns_Persistence_and%20Market%20Conditions.pdf |
| F7 | Erel-Flanagan-Weisbach: 532 USD funds, 1992-2015 vintages; average IRR 8.6% (mezzanine 8.4%, distressed 8.3%); risk-adjusted net profit ≈ 0 with equity plus bond factors; gross alpha ~4% ≈ fees of 3.1-3.9%; 15-20% of holdings equity-linked | C | NBER w32278 (Mar-2024), Tables 6-7 and pp. 13-15, 20. RAP (both factors) −0.001; GPME 0.041 (t = 1.46). Gross IRR 13.9% and alpha 4.1% come from a **65-fund subsample**. The 3.1% (1.5/15) and 3.9% (2/20) fees are **imputed** from assumed contract terms, not observed. Equity features: 15% of holdings (20% value-weighted), from Pitchbook. Sample sizes: mezzanine 193, distressed 163. | https://www.nber.org/papers/w32278 |
| F8 | Fitch PCDR 5.8% in Jan-2026 (MCO 4.5-4.7%, PMR 9.2-9.4%); TTM event mix 60/27/6/8; record 6.0% in Apr-2026; 6.3% in Aug "per a secondary report" | C | Funds Society (2-Mar-2026): 5.6% → 5.8%; MCO 4.5→4.7%; PMR 9.2→9.4%; 89 events from 74 defaulters; mix 60/27/6/8 (12 months to Jan-2026). Bloomberg Law (18-May-2026): record 6% for the 12 months to 30-Apr; 99 events. **Upgrade the 6.3% from [C]:** Bloomberg (14-Sep-2026), Investment Executive and The Lead report a record 6.3% for August, up from 6.1% in July, with 109 events from 89 defaulters. See A2 for the newer mix. | https://www.fundssociety.com/en/news/alternatives/u-s-private-credit-default-rate-continues-to-climb/ ; https://news.bloomberglaw.com/financial-accounting/us-private-credit-defaults-hit-new-record-of-6-in-april-fitch ; https://www.investmentexecutive.com/news/research-and-markets/u-s-private-credit-defaults-rise-fitch-4/ |
| F9 | Proskauer Private Credit Default Index: 2.51% (Q2-26), 2.73% (Q1-26), 2.46% (Q4-25); 716 loans; US$195.6bn | C | Release dated 28-Jul-2026; covers US senior-secured and unitranche loans. The 2.46% appears only as the title of a linked Proskauer release, not in the Q2 release body. Q2 by EBITDA: <US$25m 1.9%; US$25-49.9m 3.4%; ≥US$50m 2.4%. | https://www.proskauer.com/report/proskauers-private-credit-default-index-reveals-rate-of-251-for-q2-2026 |
| F10 | IMF GFSR Apr-2024: PIK share of BDC interest income doubled since 2019; over a third of comparable public firms have ICR < 1; BDC marks react much less to credit shocks than B-rated loan prices, with deviations lasting several quarters | C | Verbatim: Ch. 2 pp. 59-60 (Fig. 2.4) and p. 66 (Fig. 2.10). Also confirmed: "compounding losses" (p. 59); credit losses not above HY and comparable to leveraged loans (10-year window 2013-22, Fig. 2.5); PE-sponsored loans default less in stress. | https://www.imf.org/-/media/files/publications/gfsr/2024/april/english/ch2.pdf |
| F11 | Post-default recovery ~33% direct loans vs 52% syndicated vs 39% HY ("S&P study cited by the Federal Reserve") | **X** | **The values are correct; the attribution is wrong.** The Fed FEDS Note (Cai & Haque, 23-Feb-2024) sources them to **KBRA DLD** ("Figure 15. Recovery Rate. Source: KBRA DLD"). The S&P Global study it cites is on *repeat defaults*. Fix §1.5, §4.5 and the claim text. | https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html |
| F12 | Moody's: 471 preferred-stock impairments, 1983-2008; recovery 35.9% when a dividend omission is not followed by a bond default, 15.9% when part of a bond default | C | Verbatim (5-Nov-2009). Also: preferred recoveries after an omission "surpass those on junior subordinated bonds by nearly 50%". Recovery is market-based (see R10 on the basis). | https://ir.moodys.com/press-releases/news-details/2009/Moodys-Analytics-Preferred-Stock-Default-Recoveries-Approach-Those-of-Senior-Unsecured-Bonds/default.aspx |
| F13 | Moody's recovery, historical vs expected: first-lien 87/68, second-lien 61/21, senior unsecured 40/32, subordinated 28/18 | C | CFO.com, 24-Jun-2008, by Stephen Taub, quoting Moody's Kenneth Emery. US issuers; the Moody's report is not named. | https://www.cfo.com/news/holders-of-distressed-debt-beware/672046/ |
| F14 | Expedia 2020 preferred: US$1.2bn liquidation preference at 98%; 9.5% dividend accruable to year 3, up to 50% to year 6; step-ups +100bp (years 5-7) and +150bp (years 8-9); calls 105/103/102/101/100; 8.4m ten-year warrants at US$72, ≈50% of face | C | 8-K dated 23-Apr-2020, Item 1.01. Each purchaser bought 600,000 shares plus 4.2m warrants for US$588m; warrants struck at US$72, net-settled, ten-year; 8.4m × 72 / 1,200m = **50.4%**. The preferred is non-convertible; each purchaser designates one director, and Apollo also gets a non-voting observer; the dividend rate has leverage-based adjustments. **Omitted:** US$12m of fees to purchaser affiliates (effective price ≈97%). The call applies to the Preference Amount (liquidation preference plus accruals) and is still 101% at exactly the 4th anniversary. | https://www.sec.gov/Archives/edgar/data/1324424/000119312520117346/d913320d8k.htm |
| F15 | 2026 preferred practice: minimum cash pay and capped PIK replaced pure PIK after Mallinckrodt/Cineworld; control priced with yield; anti-priming; conversion as an alternative to enforcement | C (as attributed) | Verbatim in Clifford Chance, 21-Apr-2026 (J. Ewart, T. McGowan; first published in Butterworths JIBFL), including "Hybrid structures with cash-pay floors have replaced pure PIK dividends" and "Formal enforcement remains uncommon". **Caveats (R16):** a qualitative law-firm piece with no data. Footnote 1 supports the Mallinckrodt/Cineworld point with an unrelated 2016 *Lyondell* decision. Its Basel III Endgame timeline ("expected to take effect in 2025") is out of date. The impairment characterisation was not independently verified. | https://www.cliffordchance.com/content/dam/cliffordchance/briefings/2026/05/Control%20as%20economics.pdf |
| F16 | IPEV 2025: debt valued by yield/DCF calibrated at entry; par not automatically fair value even with EV coverage; warrants separate; PIK at expected PV of the recoverable amount; indicative offers may be deliberately high or low | C | Dated December 2025. Section I debt commentary. Section II §5.6 (pp. 58-59, verbatim "Par value or face value or cost value is not automatically Fair Value, even if there is sufficient Enterprise Value to cover the liability"), §5.7 (p. 59) and §5.8 (pp. 59-60; it also covers "price indications for debt or equity refinancing"). Convertibles: "debt-like… and equity-like component", calibrated separately. | https://www.privateequityvaluation.com/Portals/0/Documents/Guidelines/2025%20IPEV%20Valuation%20Guidelines.pdf |
| F17 | Rede: net DPI experience −27% in 2025 (from −53%); 2026 net +17% (39% vs 22%); 42% did NAV or hybrid facilities on CVs; 31% syndicate, on average just under half | C | PDF pp. 5, 10, 16-18 and 20. The text gives −27%; the chart label reads −28% (rounding). 75% expect more CV activity and no lender expects a decrease. Three respondents syndicated 100% of their book. | https://www.rede-partners.com/s/NAV-Financing-Market-Report-2026_FINAL.pdf |
| F18 | Fund closes: Apollo HVF III ~US$6.5bn (5-May-2026; Fund I US$3.3bn, Fund II US$4.6bn), "primarily structured equity"; Ares >US$9.8bn incl. ASOF III >US$8.3bn of equity (30-Mar-2026); 17Capital Credit Fund 2 US$7.5bn (31-Mar-2026) | C | Apollo: final close; "primarily invests in structured equity opportunities, including preferred and convertible securities". Ares: total includes "related transaction vehicles"; dated 30 or 31 March (BW URL code 20260330; Stocktitan 31-Mar 16:15 EDT). 17Capital: "approximately $7.5 billion, **including affiliated mandates**". | https://www.apollo.com/insights-news/pressreleases/2026/05/apollo-hybrid-value-fund-iii-raises-6-5-billion-3287636 ; https://stocktitan.net/news/ARES/ares-raises-over-9-8-billion-for-leading-opportunistic-credit-byffnb8p0bwi.html ; https://www.17capital.com/insights/17capital-closes-credit-fund-2-at-7-5-billion |
| A1 | §1.3: Proskauer primary LTVs "mostly below 25% (largest share 5-10%)" | **X** | **The largest bucket is 10-25% (36%); 5-10% is 32%** (bar lengths from coordinates: x = 467 vs 430). Proskauer's narrative contradicts its own chart, and the dossier's §4.3 table shows 36% for 10-25%. The buckets have unequal widths, so 5-10% has the highest *density* per point of LTV, but not the largest share. | https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025 |
| A2 | §6.13 calibration target: Fitch event mix 60/27/6/8; §6.7 split of ~14% hard / ~87% soft | **X** (stale) | 12 months to Aug-2026: **47% deferral/PIK, 41% stressed maturity extensions, 8% uncured payment default, 4% bankruptcy, liquidation or debt-for-equity** (PE150, 1-Oct-2026, citing Fitch). The hard share falls to ~12%, so the 2.5% loss-relevant rate barely moves, but extension hazards need recalibrating. The PCDR counts unique defaulters (89) while the mix is over events (109), so splitting the rate by event shares is approximate. | https://www.pe150.com/p/private-credit-defaults-are-rising-but-the-stress-is-more-nuanced-than-the-headlines ; https://theleadpc.com/middle-market-private-credit-9-14-2026/ |
| A3 | §4.7: "Competitor supply is pro-cyclical [S: IMF 2024]" | **X** | The IMF says "Evidence is mixed regarding the cyclicality of private credit lending". Private credit "did not 'dry up'" in March 2020 and is "less responsive to a sudden credit shock" than HY or leveraged loans. The pro-cyclical evidence (BIS correlation; BDC lending contracting when banks tighten) mainly concerns BDCs: "New lending by private credit funds seems to be less procyclical than BDC lending" (pp. 60-61). | https://www.imf.org/-/media/files/publications/gfsr/2024/april/english/ch2.pdf |
| A4 | §1.2: "A large, crowded, growing market"; structured solutions at 14%, "up from 10%" | **X** (framing) | Lazard's series (PDF p. 11) is **14% (2023), 15% (2024), 10% (2025), 14% (1H-26)**: flat over three years, with 2025 the outlier. | https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf |
| A5 | Rede 2025: spreads widened 140bp in 2022 and reversed in 2023 | C | "lenders reported a 140bps widening of spreads in 2022, that was reversed in 2023", with a further 40bp fall in 2024. | https://www.rede-partners.com/s/Rede-NAV-report-2025_FINAL.pdf |
| A6 | SOFR 3.89% on 15-Oct-2026; FOMC raised to 3.75-4.00% on 16-Sep-2026 | C | NY Fed: 3.89% on 15-Oct (3.88% on 14-Oct). FOMC: "raise the target range… by 1/4 percentage point to 3-3/4 to 4 percent". The 10-year UST at 5.09% was not checked. | https://markets.newyorkfed.org/api/rates/secured/sofr/search.json?startDate=2026-10-08&endDate=2026-10-17 ; https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm |
| A7 | Jefferies: LP credit pricing 91% of NAV in 2025; credit GP-led volume more than tripled | C | "credit pricing remained stable at 91 percent"; volumes "more than tripling since 2024"; GP-leds were a majority of credit secondary volume for the first time (10-Feb-2026). | https://www.jefferies.com/insights/the-big-picture/2025-global-secondary-market-review-another-record-breaking-year/ |
| A8 | 17Capital: advance rates 5-20% of NAV; US$450m GP financing and US$970m LP facility (Apr-2026); >US$20bn deployed | C | About page: "ranging from 5% to 20% of NAV". The NAV-finance page lists both April 2026 deals. Homepage: "$20bn+ Deployed", "$9bn+ Realized" (as of June 2026). | https://www.17capital.com/about-us ; https://www.17capital.com/nav-finance |
| A9 | Platforms: Oaktree Opps XII ~US$16bn (Feb-2025); AlpInvest "SPF II" US$3.2bn, platform >US$4bn, LP recaps for sovereign funds (Apr-2025); HPS SIP V US$17bn investable / US$12bn equity (Apr-2023); KKR ABF ~US$9.2tn by 2029 | C | Oaktree's figure includes "co-investment and affiliated vehicles". AlpInvest's fund is **ASPF II**; its US$3.2bn includes parallel SMAs and co-investments ("LP portfolio recapitalizations for sovereign wealth funds and asset managers"). HPS as stated. KKR: data as of 31-Mar-2024; "limited sensitivity to corporate cash flows" verbatim. | https://www.sfnet.com/home/chapters/canada/news-detail/2025/02/13/oaktree-closes-opportunities-fund-xii-at-$16-billion ; https://carlyle.com/media-room/news-release-archive/alpinvest-partners-raises-over-4-billion-portfolio-finance-platform ; https://www.hpspartners.com/insights-and-news/hps-investment-partners-close-capital ; https://www.kkr.com/insights/abf-private-credit |
| A10 | Penn Mutual: S&P BDC Index down more than 20% since Jun-2025; KBRA DLI default rate 1.5% vs leveraged loans 1.28% | C (as reported) | 18-Jun-2026. The KBRA and leveraged-loan figures are footnoted to "J.P. Morgan – Default Monitor; 6/1/26", so they are still secondary. | https://www.pennmutualam.com/market-insights/blogs/chart-of-the-week/2026-06-18-the-pik-picture-tracking-non-cash-income-in-bdc-portfolios |
| A11 | Fed: private credit ~US$1.7tn vs leveraged loans ~US$1.4tn vs HY ~US$1.3tn (Jun-2023) | C | Figure 1 note: "Data as of June 2023". | https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html |
| A12 | §5.6 A: Expedia-terms preferred, scenarios S1-S5 | C | All reproduce (Section 6). S3 needs the year-6 step-up to 10.5% to give 1.52 / 1.75x. Caveats are in R10. | Verifier recomputation |
| A13 | §5.6 B: NAV loan, Normal and Drought rows | C | Reproduces exactly with annual steps and distributions = δ × post-growth NAV: 10.8% / 1.30y / 114%, and 10.3% / 2.17y / 78%. | Verifier recomputation |
| A14 | §5.6 B: Crisis and Deep-crisis rows | U | The paths are under-specified (de-smoothing method, the meaning of "−10%", recovery speed). The 5-year maturity is not applied, although the deep-crisis WAL is 4.7y. | – |
| A15 | §5.6 C: natural-hedge Monte Carlo, PE distributions 15.4 / 7.4 / 3.4 | U | Not reproducible from the stated inputs: US$70bn × 20/10/6% = **14.0 / 7.0 / 4.2**. Either noise or a lag is unstated, or the table is wrong. The direction of the conclusion is unaffected. | Verifier recomputation |
| A16 | §1.6 / §5.6 C2: "A 13% drought deal only breaks even at a 9% shadow price"; waiting pays only above ~21% crisis returns | **X** | The deploy-now column reproduces under the stated formula, (IRR − r_f − ℓ_s) × 4. But the formula holds ℓ_D = 9% for **all four years**, which is inconsistent with (a) the dossier's own Markov chain (D persistence 0.72) and (b) stream 08's fallback ℓ = 9%/9%/4%. With ℓ following the chain, deploy-now from D is **+0.061 per $1** at (0.5/9/15), not 0.00. On the 9/9/4/4 path it is **+0.10**, a break-even drought IRR of **≈10.5%**. The waiting values cannot be reproduced because no discount rate or horizon is given. | Verifier recomputation; `research/dossiers/08_action_valuation.md` (ℓ fallback row) |
| A17 | §5.6 D and E arithmetic: RoE 12.8/14.6/11.5/12.0%; LTV 33/50%; cushions 33/17%; external interest 207/166/285/228m | C | All reproduce at SOFR 3.89%. The economics are flawed (R2): losses and PIK are ignored, and the D/E 1.0 row uses a 60% trigger. | Verifier recomputation |

---

## 4. Citation check

| Ref | Exists | Authors, year, title, venue | Notes |
|---|---|---|---|
| 19. Rede Partners (Jun-2026), *NAV Financing Market Report 2026* | Yes | Correct | Content verified (F1, F17). |
| 20. Rede Partners (Jun-2025), *NAV Financing Market Report 2025* | Yes | Correct | The 140bp sentence was verified directly, not only via stream 08. |
| 21. Proskauer (2026), *Insights on the NAV Financing Market, FY2025* | Yes | Correct | Content verified. The narrative's modal-LTV sentence contradicts the chart (A1). |
| 24. ILPA (2024), *NAV-Based Facilities Part I* | Yes | Correct | The FFA figure is footnoted to 17Capital (Mar-2024); say so when citing it. |
| 25. Lazard (2026), *Interim Secondary Market Report 2026* | Yes | Correct | Content verified. The publication month was not visible in the extracted text. |
| 2. Blackstone Inc., Form 10-Q, Q2-2026 | Yes | Correct (quarter ended 30-Jun-2026) | Content verified. |
| 43. Böni, P. & Manigart, S. (2022), *FAJ* 78(4):121-144, DOI 10.1080/0015198X.2022.2092384 | Yes | Correct (Crossref; online 18-Aug-2022) | The article is **open access**; the Tilburg copy is the published version. |
| 42. Erel, I., Flanagan, T. & Weisbach, M. S. (2024), NBER WP 32278 | Yes | Correct (March 2024; DOI 10.3386/w32278) | No journal version in Crossref as of this check. |
| 40. IMF (Apr-2024), GFSR Ch. 2, "The Rise and Risks of Private Credit" | Yes | Correct | Content verified. |
| 41. Cai, F. & Haque, S. (23-Feb-2024), FEDS Notes | Yes | Correct | **The recovery figures are KBRA DLD data, not S&P (F11).** A correction was posted on 26-Feb-2024 (Figure 13 source). |
| 18. Expedia Group 8-K (Apr-2020) | Yes | Correct (dated 23-Apr-2020) | Content verified. |
| 35. IPEV (Dec-2025) | Yes | Correct | Content verified. |
| 29. Clifford Chance (21-Apr-2026) | Yes | Correct date | Authors (Ewart, McGowan) are omitted. The URL path says /2026/05/. First published in Butterworths JIBFL. |
| 36. Moody's Analytics (5-Nov-2009) | Yes | Correct | Content verified. |
| 37. CFO.com (24-Jun-2008) | Yes | Correct | The author, Stephen Taub, is omitted. The underlying Moody's report is unnamed. |
| 44-51. Merton 1974; Jarrow-Turnbull 1995; Duffie-Singleton 1999; Ayache-Forsyth-Vetzal 2003; Longstaff-Schwartz 2001; Altman-Brady-Resti-Sironi 2005; Acharya-Bharath-Srinivasan 2007; Kaplan-Strömberg 2003 | Yes | All correct: authors, title, journal, volume, issue, pages and year match Crossref | The characterisations of Altman et al. and Acharya et al. are corroborated (see the Consensus cross-check below). |
| 52. Kaplan, S. N. & Schoar, A. (2005), *JF* 60(4):1791-1823 | Yes | Correct | **Orphan reference:** it is not cited anywhere in the body. |
| 53. [K] Black, F. & Cox, J. C. (1976) | Yes | *JF* 31(2):**351-367**, DOI 10.1111/j.1540-6261.1976.tb01891.x | Can be upgraded from [K]. |
| 54. [K] Tsiveriotis, K. & Fernandes, C. (1998) | Yes | *Journal of Fixed Income* 8(2):**95-102**, DOI **10.3905/jfi.1998.408243** | Can be upgraded from [K]. The dossier's failed DOI lookup probably used a neighbouring suffix. |
| 55. [K] Lando, D. (1998) | Yes | *Review of Derivatives Research* 2(2-3):**99-120**, DOI 10.1007/BF01531332 | Can be upgraded from [K]. |
| 1, 5, 6, 8, 9, 12. Apollo, Carlyle/AlpInvest, HPS, Ares, SFNet/Oaktree, 17Capital releases | Yes | Correct | Several headline sizes include affiliated vehicles, SMAs or co-invest (F18, A9). Carlyle's fund name is "ASPF II". |
| 31, 32. Funds Society (2-Mar-2026); Bloomberg Law (18-May-2026) | Yes | Correct | Content verified. |
| 33. Webull/Benzinga (Fitch 6.3%) | Not fetched | – | Replace with Bloomberg (14-Sep-2026) or Investment Executive (14-Sep-2026). |
| 26, 28, 34, 11, 13. Jefferies, KKR, Penn Mutual, 17Capital pages | Yes | Correct | Content verified. |

**Erratum (2026-10-18, citation re-check).** The row for refs 44-51 wrongly passed Kaplan & Strömberg (2003) as matching Crossref on title: the dossier drops the subtitle ": An Empirical Analysis of Venture Capital Contracts" (DOI 10.1111/1467-937X.00245). Also, F7's "GPME 0.041" is the stock-factor-only GPME (EFW fn 7: GPME cannot use both factors), so it does not support the dossier's "with equity and bond factors" label; the both-factor estimate is RAP −0.001 (t = −0.01, Table 4B). Source: `research/literature/recheck/G3_cap_solutions.recheck.md`.

**Hallucinated references.** None found among the ~40 references I fetched or checked against Crossref.

**Consensus cross-check of two characterisations.**
- The dossier says recoveries are lower when default rates are high. This matches Altman et al.: "recovery rates are a function of supply and demand for the securities, with default rates playing a pivotal role" [1].
- It says recoveries are lower when the defaulter's industry is in distress. This matches Acharya et al.: "creditors of defaulted firms recover significantly lower amounts in present-value terms when the industry of defaulted firms is in distress", with a fire-sale effect [2].

[1] [The Link between Default and Recovery Rates: Theory, Empirical Evidence and Implications](https://consensus.app/papers/details/4b638f0501945f7395fa9f005cdcc41f/?utm_source=claude_desktop) (Altman et al., *The Journal of Business*, DOI 10.1086/497044; Consensus lists 2003, the working-paper year; Crossref gives 78(6):2203-2228, 2005)
[2] [Does Industry-Wide Distress Affect Defaulted Firms? Evidence from Creditor Recoveries](https://consensus.app/papers/details/6b9770edca525bec9ae7167d872bfcd4/?utm_source=claude_desktop) (Acharya, Bharath & Srinivasan, 2007, *Journal of Financial Economics*, DOI 10.1016/j.jfineco.2006.05.011)

---

## 5. Reasoning issues and overclaims in the design implications and specification card

Severity: **H** = must fix before IC use; **M** = fix before calibration; **L** = tidy-up.

**R1 (H). The deploy-vs-wait analysis charges a flat shadow price for four years (§1.6, §5.6 C2, Opportunity row of the spec card).**
- **The problem.** Excess value is computed as (IRR_s − r_f − ℓ_s) × 4, with ℓ_s fixed at its starting-state value for all four years. The dossier's own Markov chain makes D only 72% persistent. Stream 08's fallback path is ℓ = 9%/9%/4%: 9% applies only in years 1-2.
- **The consequence.** The headline "a 13% drought deal only breaks even at a 9% shadow price" (executive summary, "The catch") is an artifact of the assumption.
  - With ℓ following the chain, deploy-now from D is +0.061 per $1 (≈ +1.5pp a year).
  - On the 9/9/4/4 path it is +0.10, and the break-even drought IRR is ≈10.5%.
- **Two further problems.**
  - The formula ignores how capital is returned. NAV loans return capital with a WAL of 1.3-2.2 years, so ℓ should apply only to capital still outstanding.
  - The waiting values cannot be reproduced, because neither a discount rate nor a horizon is given.
- **Inconsistency with the dossier itself.** §6.5 already prescribes valuing deployment through the LAPV kernel π_{s,t}. C2 contradicts that.
- *Fix:* value deployment as path-wise LAPV with the state-contingent kernel, or at least integrate E[ℓ_{S_t}] over the capital-outstanding profile. Present the IC statement conditionally ("only if ADIC's shadow price stays at 9% for the life of the deal").

**R2 (H). LEVER and back-leverage economics ignore losses and the cash/PIK mismatch (§1.8, §5.6 D, §6.11).**
- **Losses.** RoE = r_A + (r_A − r_B)·D/E uses the 11% *contractual* yield. Take the dossier's own drought parameters: a 2.5% loss-relevant default rate and an LGD of about 0.7. The asset return is then ≈9.25%, which gives:
  - **bank leverage:** RoE 10.2% at D/E 0.5 (+0.9pp, not +1.8pp);
  - **alternative-lender leverage:** RoE 8.9% at D/E 0.5, *below* the unlevered 9.25%.
- **Cash.** At the drought PIK share of 30%, cash yield is 7.7%. The alternative-lender all-in cost is 9.99%, so cash carry is −2.3% per dollar of debt. Leverage becomes a cash drain in exactly the regime the dossier says ADIC is in.
- **Triggers.** The D/E 1.0 rows use a 60% LTV trigger, while D/E 0.5 uses 50%. On the common 50% trigger, D/E 1.0 has zero cushion at inception.
- *Fix:* compute RoE on a loss-adjusted, cash basis. Add a cash-carry constraint: stressed cash income ≥ facility interest plus fees. Compare leverage levels at a common trigger.

**R3 (H/M). REFINANCE for ADIC's own PE book is calibrated to a product an LP cannot use (§1.7, §5.6 E, §6.10, pricing service in the spec card).**
- **Wrong comparables.**
  - Rede, Proskauer-primary and ILPA describe GP-level facilities against direct PE portfolios. Rede explicitly excludes "Fund of Funds or secondary portfolios".
  - ADIC is an LP in third-party funds. Its REFINANCE options are LP-level portfolio financings or structured secondaries: preferred equity or an NAV loan into an SPV holding its LP interests (AlpInvest "LP portfolio recapitalizations", 17Capital's US$970m LP facility).
  - These need **GP consent to transfer or pledge** interests, are priced off different comparables, and allow different LTVs. Proskauer's secondaries-facility terms (25-70% LTV, spreads at or below 4%) are a closer, but still imperfect, anchor.
- **Example E and the quote function.**
  - Example E applies Rede's 3.0%/5.6% margins and a 15% LTV to an LP book.
  - The quote function is to be trained on "the Rede and Proskauer distributions". Those are *marginal* survey distributions, with no joint LTV-structure-spread data, so they cannot identify a conditional P10/P50/P90.
- **A related SELL issue.** SELL (c), "credit GP-led", can only be initiated where ADIC controls the positions. As an LP in third-party credit funds, ADIC can only choose to sell or roll in a GP-led process.
- *Fix:* re-anchor on LP-portfolio-financing comparables, add per-fund consent and transfer-feasibility flags, and use the survey marginals only as unconditional priors.

**R4 (M). The "opportunity hedge" evidence is overstated (§1.6, §3.6, §6.7).**
- Böni-Manigart's positive ex-ante credit-spread effect comes paired with a *negative* ex-ante TED-spread (funding-illiquidity) effect that is "more than twice as large as that of performance persistence". In a liquidity crisis both widen.
- Erel-Flanagan-Weisbach find zero net risk-adjusted alpha, so higher crisis-vintage IRRs may be compensation for equity beta rather than excess return π_t. π_t is how the dossier's own hedge condition is defined.
- The IMF calls competitor cyclicality "mixed" (A3).
- The crisis vintage IRR of 14-18% net in §6.7 exceeds every Böni-Manigart strategy mean; special situations is 12.6% mean and 8.0% median.
- *Fix:* state the full Böni-Manigart result, measure π_t on a risk-adjusted basis, and label the crisis IRRs as optimistic [I].

**R5 (M). The underwritten-vs-realised prior is mislabelled, and one correction term has a units error (§6.8, §4.4).**
- "Realised net ≈ underwritten gross − 4 to 6pp [S-anchored: EFW, BM, Tac Opps]" is not supported. None of these sources measures *underwritten* returns.
  - EFW's 13.9% vs 8.6% compares *realised* gross (65 funds) with realised net (532 funds): a fee and sample gap, not underwriting optimism.
  - Tac Opps reports a gross MOIC and a net IRR; it has no gross IRR.
- The "extension drag (WAL × Δcarry)" correction is in percentage points, not percentage points per year, and must be annualised.
- The PIK haircut (1 − pL) and −PD·LGD in the debiased-return formula can double-count losses on accrued PIK.
- *Fix:* retag as [I], calibrate on ADIC's own underwriting history, and fix the units.

**R6 (M). Constraint #6 contradicts the instrument library (§6.4 vs §6.6).** "New deals require minimum cash pay ≥ 50% of the coupon after year 2." Yet the library includes:
- #7, the holdco PIK note ("Full PIK, bullet");
- #2, hybrid NAV / fund-level preferred ("Preferred return accrues (PIK)");
- #11, LP portfolio preferred ("As #2").

The optimiser would either never select these or violate the constraint. *Fix:* define the PIK rule per family, or as a book-level cap only.

**R7 (M). The NAV-loan recursion forgives interest, and example B has no loss state (§3.1, §3.4, §5.6 B).**
- B_{t+1} = B_t − σ(ℓ)(D − I)^+ drops unpaid interest whenever distributions fall short of interest (D < I). There is no capitalisation and no default.
- Worked example B has no default, LTV default trigger or maturity. The deep-crisis WAL of 4.7 years runs into the 5-year maturity. "The IRR is robust" therefore holds by construction.
- *Fix:* B_{t+1} = B_t + (I − D)^+ − σ(ℓ)(D − I)^+, with ℓ^def, maturity and extension states, and an LGD branch in the example.

**R8 (L/M). The ICR⁻¹ hazard covariate breaks down at low or negative earnings (§3.2).** It flips sign for negative EBITDA, which *lowers* the hazard, and it explodes near zero. The IMF notes that interest-cover ratios are missing when earnings are negative. *Fix:* use a bounded transform plus a negative-EBITDA indicator.

**R9 (L/M). Liquidity costs may be counted twice (§6.5).** If LAPV already includes unfunded draws and back-leverage flows under the liquidity kernel, the separate "liquidity charge on unfunded commitments and back-leverage cure risk" double-counts. This is the same issue as stream-05 R3. *Fix:* charge each cost once.

**R10 (L). Example A has two small errors (§5.6 A).**
- **Recovery basis in S4 and S5.** Moody's preferred recoveries are post-default prices relative to par. The example applies them to the accreted 1.31x claim, which *raises* recovered dollars. On face, the results are −28.5% / 0.37x (S4) and −45.5% / 0.16x (S5).
  - The text's explanation, that the loss is severe "because the accreted claim… is exactly what is impaired", is backwards.
- **S2 call price.** Redemption at exactly year 4 is 101% under the 8-K, not par. The effect is negligible.

**R11 (L). Example C is not reproducible (§5.6 C).** The PE distributions do not follow from the stated inputs (A15). The +0.96 correlation is, as the dossier itself admits, mostly built in by construction. Publish the script.

**R12 (L). The Tac Opps realised-vs-total gap is attributed to adverse inventory selection (§4.4).** The "total" figure includes funds still in their investment period (asterisked; US$15.5bn of available capital), and young deals carry low MOICs mechanically. Compare by vintage before drawing this inference.

**R13 (L). The counter-evidence understates distribution use (§4.7).** Primary use of proceeds for dividend recaps or liquidity to investors is 7% standalone *plus* 15% combined, up to 22% in total.

**R14 (L). The book's own repayments are not a low-cost funding source in a drought (§1.6).** "Fund counter-cyclical deployment from… the book's own repayments" contradicts examples B and C. In a drought, cash back by year 2 falls 32% (114% → 78% of outlay) and the book's cash returned falls 41% (US$4.11bn → US$2.43bn).

**R15 (L). The execution probability of 0.7-0.9 is partly unsupported (spec card, liquidity terms).**
- Lazard's 27% failed or paused implies p ≈ 0.73 for GP-led processes in a record half.
- The upper end, 0.9, has no support, and no stress haircut is applied.
- The Lazard statistic covers GP-led transactions, not sales of credit or structured positions.

**R16 (L). One law-firm briefing sets defaults (§5.2, §6.4 #6, §6.6).** A single qualitative piece (F15) is treated as [S] market practice. It sets "default features of the instrument library" and the PIK constraint. Retag it as [P].

**R17 (L). Cross-sectional spreads are used as a regime swing (§1.3).** 533-982bp is the 2023 spread range *across LTV bands*, not across regimes. The regime evidence is the +140bp of 2022 (A5).

**R18 (L). The NAV market-size range comes from one vendor (§1.2, §8).** US$150bn, US$600bn and US$700bn all trace to 17Capital, including the FFA/ILPA figure. Present them as one vendor's evolving estimates, not as independent definitions.

---

## 6. Recomputed numbers

| Item | Dossier | Recomputed | Status |
|---|---|---|---|
| Warrant strike notional / face | ≈50% | 50.4% | OK |
| S1: called year 2 at 103%, m = 1.6 | 25.6% / 1.55x | 25.63% / 1.553x | OK |
| S2: par at year 4, m = 1.25 | 12.8% / 1.54x | 12.78% / 1.537x (12.98% / 1.547x at the 8-K's 101%) | OK |
| S2b: no kicker | 10.1% / 1.41x | 10.13% / 1.408x | OK |
| S3: drought | 10.0% / 1.75x / 1.52 | 10.03% / 1.755x / 1.516 with the year-6 step-up; 9.88% / 1.740x / 1.509 without | OK |
| S4: recovery 35.9% | −21.7% / 0.48x | −21.65% / 0.481x on the accreted claim; −28.45% / 0.366x on face | OK (basis) |
| S5: recovery 15.9% | −40.3% / 0.21x | −40.28% / 0.213x; −45.46% / 0.162x on face | OK (basis) |
| NAV loan, Normal | 10.8% / 1.3y / 15% / 114% | 10.81% / 1.30y / 15.0% / 114.1% | OK |
| NAV loan, Drought | 10.3% / 2.2y / 15% / 78% | 10.32% / 2.17y / 15.0% / 78.3% | OK |
| NAV loan, Crisis and Deep crisis | 10.1% / 3.3y; 9.9% / 4.7y | – | Under-specified |
| Monte Carlo PE distributions (N/D/C) | 15.4 / 7.4 / 3.4 | 14.0 / 7.0 / 4.2 (70 × stated rates) | Not reproducible |
| C2, deploy now from N | 0.26 | 0.26 | OK |
| C2, deploy now from D (ℓ_D 3/6/9%) | 0.24 / 0.12 / 0.00 | Flat ℓ: 0.24 / 0.12 / 0.00. Markov-path ℓ: 0.255 / 0.154 / 0.061. 9/9/4/4 path: 0.10 | Formula OK; conclusion fragile (R1) |
| C2, waiting values | 0.20 … −0.08 | – | Not reproducible |
| D, RoE (bank; alternative lender) | 12.8 / 14.6; 11.5 / 12.0 | 12.80 / 14.61; 11.50 / 12.01 | OK |
| D, cushion to trigger | 33% / 17% | 33.3% / 16.7% (0.0% at D/E 1.0 on the 50% trigger) | OK (triggers differ) |
| D, loss-adjusted RoE at D/E 0.5 / 1.0 (default 2.5%, LGD 0.7) | – | Bank 10.2% / 11.1%; alternative 8.9% / 8.5%; unlevered 9.25% | New (R2) |
| D, cash carry per $ of debt at 30% PIK | – | Bank +0.3%; alternative −2.3% | New (R2) |
| E, external interest | 207 / 166 / 285 / 228m | 206.7 / 165.4 / 284.7 / 227.8m | OK |
| SOFR + 5.6% | ≈9.5% | 9.49% | OK |

---

## 7. New primary-source data the dossier should absorb

- **Fitch PCDR.**
  - 6.1% (July) → 6.3% (August, record); 12 months to August: 109 events from 89 defaulters.
  - Event mix 47/41/8/4.
  - August sector rates: healthcare providers and industrials 9.9%; software 0.6% [C].
  - April: 99 events (Bloomberg Law).
- **Lazard structured-solutions share:** 14% / 15% / 10% / 14% for 2023 / 2024 / 2025 / 1H-26.
- **Proskauer FY-2025:** a further 15% "follow-on + debt management + dividend recap/liquidity" use category; primary maturities 45% at 5 years.
- **Proskauer default index, Q2-26 by EBITDA:** 1.9% (<US$25m), 3.4% (US$25-49.9m), 2.4% (≥US$50m).
- **Expedia 8-K:**
  - US$12m of fees to the purchasers;
  - an Apollo non-voting observer;
  - a two-thirds class vote is needed to issue senior or pari passu stock;
  - expected closing on or about 5-May-2020.
- **17Capital (June 2026):** US$20bn+ deployed and US$9bn+ realised. Its ~US$60bn of annual deal flow is "about 1.5 percent" of a ~US$4tn unrealised-buyout pool.
- **Rede 2026:** the DPI net-experience chart reads −28% (text −27%). Banks were 36% of respondents. Scope exclusions are listed in F1.
- **IMF:** private-credit fund lending is less procyclical than BDC lending.
- **Fed FEDS Note:** S&P finds repeat defaults marginally more likely, and sooner, among private-credit borrowers.

---

## 8. Overall reliability rating

**MEDIUM overall: HIGH for the sourced empirical layer, MEDIUM-LOW for the decision layer.**

**Empirical layer.** It can go to the IC once the six corrections are applied (F11, A1, A2, A3, A4, A16) and the 6.3% Fitch figure is upgraded from [C]. No numbers were refuted. Every flagged statistic matches its primary document.

**Decision layer.** It should not drive IC-facing conclusions until R1-R3 are fixed. These three issues change the substance of executive-summary items 6-8:
- whether drought-regime deployment pays;
- whether back-leverage adds return;
- how ADIC's own REFINANCE is priced and whether it is feasible.

R4-R7 should be fixed before calibration, and R8-R18 are tidy-ups.

---

## Citation corrections (2026-10-18)

- §4: added one erratum line under the citation table. Kaplan & Strömberg's title is truncated, and F7's GPME 0.041 is the stock-factor-only estimate (source: `research/literature/recheck/G3_cap_solutions.recheck.md`). The dossier's corresponding fixes are listed in its own "Citation corrections (2026-10-18)" section.
