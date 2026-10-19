# Verification log: Stream 05, secondaries, NAV financing, CVs, preferred equity and CFOs

| | |
|---|---|
| **Dossier** | `research/dossiers/05_secondaries_navfin.md` (as of 2026-10-18) |
| **Verified** | 2026-10-18, adversarial fact-check pass |
| **Overall reliability** | **HIGH** for the empirical evidence; **MEDIUM** for the design and calibration layer. Six must-fix issues are listed in Section 5. |

---

## 1. Summary

**Coverage.** 42 claims checked: all 20 author-flagged claims, plus 22 additional load-bearing claims. The additional ones cover:
- the volume table and capital metrics;
- the H1-2026 Jefferies values tagged [C];
- the worked examples;
- three calibration defaults that are presented with [S] tags.

**Verdicts.**

| Verdict | Count |
|---|---|
| Confirmed | 31 |
| Corrected | 7 |
| Refuted | 2 |
| Unverifiable | 2 |

**The market-data backbone is unusually accurate.** I traced about 120 individual numbers to the primary documents, extracting the text layers locally. None was materially wrong. The documents were:
- Jefferies Jan-2025, Jul-2025, Feb-2026 and Jul-2026;
- Evercore FY-2025 and H1-2026;
- Lazard 1H-2026;
- Campbell Lutyens FY-2025;
- Proskauer FY-2023 and FY-2025;
- ILPA NAV guidance Parts I-III, ILPA 2023 CV guidance and ILPA 2017 subscription-line guidance;
- Nadauld et al. (NBER), the Bollen-Sensoy working paper, Unquote/Cogent, WilmerHale, Octus and Azalea.

This includes every cell of the volume table (Section 4.1) and the full 2019-2024 Jefferies strategy pricing panel (Section 4.2).

**The corrections are about attribution and overstatement, not wrong numbers.**
1. The 2008 claim that interests "could not be given away" is a *hypothetical* in WilmerHale (2009), not a reported event.
2. Bollen-Sensoy's "5-10 pp" comes from the 2015 working paper. The 2022 published version's abstract reaches a different headline conclusion, and its magnitude is unverified.
3. ILPA's recommendation of LPAC consent for distribution use is in **Part III**, not Parts I-II.
4. The tail-sale worked example (12.1%) does not reproduce from the stated inputs.
5. The NAV-facility cost example mixes simple and compounded conventions.

**The [C]-tagged H1-2026 Jefferies figures are confirmed from the primary report.** The Jul-2026 PDF is **not** image-only; its text layer extracts cleanly. All the values the dossier took from summaries match. Upgrade them to [S].

**Six must-fix issues before any output reaches the IC.** Details are in Section 5.
1. The capital-overhang regime thresholds are inverted relative to history: the multiple *rises* when volume collapses (3.1x in 2020).
2. The execution-probability default contradicts its own cited statistic. Liquidity coverage also uses *expected* execution where the stated constraint is a chance constraint.
3. The Tier-2 objective double-counts liquidity and fire-sale costs that are already inside simulated wealth.
4. The shadow-price SELL test (and the CV rule) omits the base value of the cash raised.
5. The crisis-price calibration risks double-counting NAV staleness.
6. The MCL linear program has a units error, so its dual is not "the marginal cost of the last dollar".

---

## 2. Method and limitations

**Method.**
- Primary PDFs were fetched with WebFetch.
- The fetch tool could not parse most of them, so the binaries were saved and their text layers extracted locally with `pypdf` (project venv, run with `python -I`). Downloads were kept in separate folders.
- Numerical checks were recomputed with `numpy`/`scipy` (IRR via `brentq`).
- Bibliographic metadata was checked against Crossref (`api.crossref.org`) and IDEAS/RePEc.

**Limitations.**
- The session's shared WebSearch budget was exhausted when this pass started, so no keyword searches were possible. Verification relied on direct fetches of the URLs the dossier cites, plus known publisher and metadata endpoints.
- Several secondary sites were blocked:
  - NakedCapitalism (403);
  - Buyouts Insider (paywall);
  - Yale Daily News (429);
  - pe-insights (403);
  - INFORMS DOI page (403).
- As a result, the Harvard-2008 outcome and the GIC/CIC/KIC sovereign process details could not be checked beyond what the dossier already tags [C].

---

## 3. Claims table

**Verdict key:** C = confirmed, X = corrected, R = refuted, U = unverifiable. F-numbers are the author-flagged claims; A-numbers are additional claims I selected.

| # | Claim (abridged) | Verdict | Corrected value / verifier note | Source URL |
|---|---|---|---|---|
| F1 | Jefferies FY-2025: US$240bn (+48%); LP-led US$125bn (52%); LP pricing 87% (−200 bp); buyout 92 / VC-growth 78 / credit 91 / RE 70; <5y 95%, >10y 73%; ~23% of LP deals deferred; dedicated capital US$327bn | C | Every figure matches the article (10-Feb-2026). Also: GP-led deferral ~29% of volume; total capital ~US$477bn. | https://www.jefferies.com/insights/the-big-picture/2025-global-secondary-market-review-another-record-breaking-year/ |
| F2 | Evercore H1-2026: US$121bn (+19%); GP-led 65, LP-led 56; dry powder ~194 (−10% YTD from ~215); overhang ~1.0x; quality buyout ~90%; tail ~70% since 2022; SWF share 12%→21%; 88% intermediated | C | Verbatim in report text (pp. 2-5, 13-15). The overhang chart shows ~1.0x and ~1.1x for the two segments; which is LP-led and which GP-led is not certain from the extracted text. The 88% figure reads "advisor-led, multi-bidder". The text also settles the CV chart the dossier called ambiguous: SACV 52% at par, 14% above, 34% below; MACV 71% below. The dossier's reading is right and the third-party "71% of SACVs at par" is wrong. | https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf |
| F3 | Buyer target gross multiples (~4y): SACV 2.3x, MACV 1.9x, single LP 1.8x, diversified LP 1.7x; VC 20%+ net IRR; infra 13-15% net IRR | C | Evercore H1-2026 p.10 ("Target Gross Multiples (4 Year Time Horizon)"), p.18 (infra "converging around 13-15% net IRR") and p.19 ("majority underwrite deals to 20%+ net IRRs"). The IRR conversion assumes a 4-year bullet; I recomputed 14.2 / 15.8 / 17.4 / 23.1%. If cash comes back around a 4-year mean instead, the IRRs are about 0.5-1.5 pp higher. | Same as F2 |
| F4 | Evercore FY-2025: SWFs 12% of LP-led (2025) vs 2% (2024); deferral use declined; third-party leverage 7%→14%; LP-led targets mid-to-high-teens gross | C | All in the Feb-2026 report (seller-mix chart p.8; text pp.8, 11-12). Caveat: 7%→14% is the *% of survey respondents* who used third-party leverage, not a share of deals or volume. | https://www.evercore.com/wp-content/uploads/2026/02/Evercore-PCA-2025-Secondary-Market-Report.pdf |
| F5 | Jefferies pricing panel 2019-24 (all 88/86/92/81/85/89; buyout 93/90/97/87/91/94); 2024 buyout by fund age 99/96/88/79/70; deferral in 20% of 2024 LP deals, ~+400 bp vs cash | C | Fig. 3, Fig. 4 and p.6 text. The VC, RE and credit rows of dossier Table 4.2 also match Fig. 3 exactly. | https://www.jefferies.com/wp-content/uploads/sites/4/2025/02/Jefferies-Global-Secondary-Market-Review-January-2025.pdf |
| F6 | Jefferies H1-2025: "Liberation Day" cut pricing 300-500 bp, then rebounded; avg LP pricing 90%; avg LP rollover ~17%; ~90% of SACVs and 60% of MACVs above 90% of NAV; Asia 30%+ discounts | C | pp.2, 6, 8. The SACV/MACV statistic sits in the buyout-CV discussion. By H1-2026 the Asia discount had widened to 35%+ (Jefferies Jul-2026). | https://www.jefferies.com/wp-content/uploads/sites/4/2025/08/Jefferies-Global-Secondary-Market-Review-July-2025.pdf |
| F7 | Cogent: average high bid 84.7% (H1-08) → 61% (H2-08); 83.5% after public-market adjustment | C | Unquote, 26-Jan-2009. Also confirms 22% of buyout funds bid above 80%, 15% of funds at or below 30%, and ~50 bp fee drag. Caveat: these are average *high bids*, an upper bound on clearing prices (see R5). | https://www.unquote.com/uk/news/85756/secondaries-pricing-dips-to-a-five-year-low |
| F8 | Late-2008 deals priced off pre-year-end NAVs: ~40% average discount, up to 50%+; some undesirable funds could not be given away; transfers took 3+ months (GP consent, ROFR) | **X** | Confirmed: 40% / 50%+; "three months or longer"; HarbourVest's MAC walk-away (Oct-2008). **Corrected:** WilmerHale only says it is *"possible"* sellers "will not be able to 'give away' certain funds". That is a forecast, not an observed event. Fix Sections 1, 2.2 and 4.2, or add a transaction-level source. | https://www.wilmerhale.com/-/media/files/wilmerhale_shared_content/files/editorial/publication/blt_ma09_secondarymarket.pdf |
| F9 | Nadauld et al.: average discount 13.8%; ~9% for 4-9y funds; ~10% for 10+y funds even with time fixed effects; buyers beat sellers ~5 pp/yr in PME (~3 pp for 4-9y); bigger discounts for small funds, small deals and scarce buyer capital | C | NBER w22404, pp.1-3 and 20-21. **Omitted finding (relevant to R7):** on a PME basis, *sellers of 10+ year funds earn more than buyers* (p.21), so the tail discount reflects lower-quality residual assets. | https://www.nber.org/papers/w22404 |
| F10 | Bollen-Sensoy: required returns up to 5-10 pp higher when haircuts are large; *Financial Management* 51(2), 2022 | **X** | The sentence is in the **17-May-2015 working paper** (p.2). The published paper (FM 51(2):501-538; online Aug-2021, print Jun-2022) has a different abstract: model-implied breakeven returns match observed returns for moderately risk-tolerant LPs with up to 40% in PE. The published magnitude is unverified (paywalled). Cite the figure to the working paper. | https://ilpa.org/wp-content/uploads/2015/09/Bollen-How-Much-For-A-Haircut-Illiquidity-The-Secondary-Market-And-The-Value-Of-Private-Equity-2015.05.pdf ; https://ideas.repec.org/a/bla/finmgt/v51y2022i2p501-538.html |
| F11 | Proskauer FY-2023: spreads over 3M Term SOFR of 533 / 681 / 764 / 982 bp by LTV; secondaries facilities 300-400 bp; tenor 4-5y (66%); LTV-based sweeps 57% | C | Also confirmed: 11-25% LTV most common (51%); OID 1-2.5%; fixed sweep 29%, none 14%; minimum MOIC below 1.30x prevalent; "may indeed be smaller than some reports suggest". Caveat: the charts cover the **standard fund-level NAV market only**, not LP-level facilities. | https://www.proskauer.com/uploads/insights-on-the-nav-lending-market-2023 |
| F12 | Proskauer FY-2025: primary spreads mostly below 5%, concentrated at 4-5%; secondaries mostly below 3%; primary LTV mostly below 25%, largest share 5-10%; secondaries LTV 25-70%; upfront fees 1-2%; LTV sweeps in 83% of secondaries facilities; heavy CFO and rated-feeder use | C | All in the text. "Mostly below 5%" means 55% of respondents; 31% price at 6% or more. Proskauer's text calls 5-10% the modal primary LTV bucket, but the chart values as extracted (23 / 32 / 36 / 9) suggest 10-25% may be modal. Treat the modal bucket as uncertain. | https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025 |
| F13 | ILPA (2024): NAV market ~US$100bn → US$600bn by 2030 (FFA, via 17Capital); 80% portfolio support vs 20% distributions; NAV facilities are fund-level leverage; LPAC consent recommended for distribution use | **X** (citation) | The first three points are in Part I (its footnote cites 17Capital, "In Defence of NAV Financing", Mar-2024). The LPAC point is in **Part III**: "GPs should seek LPAC approval if they intend to use any of the proceeds to generate a distribution". Part III also recommends LPAC consent before **any** NAV facility unless the LPA permits it. Synthetic DPI, recall risk and interest cost are in Part II, as stated. | https://ilpa.org/wp-content/uploads/2024/11/Part-I-Nav-Based-Facilities-Guidance.pdf ; https://ilpa.org/wp-content/uploads/2024/11/Part-III-Nav-Based-Facilities-Guidance.pdf |
| F14 | CFOs: average SOFR+295 bp on 2025 deals (one law firm); KBRA rated 14 US CFOs worth US$7.8bn in 2024; record 2022 with 25 deals worth US$13.1bn; senior notes single-A, bought by US insurers; GP retains the equity | C | Octus, 9-Sep-2025. Also confirmed: 12-15 year maturities; Coller US$2.4bn (Apr-2025); Churchill US$750m with a US$70m liquidity facility (Mar-2025); the 2024 UK matching-adjustment "predictable cash flows" reform. | https://octus.com/resources/articles/demand-for-collateralized-fund-obligations-surges-amid-uk-solvency-ii-reforms/ |
| F15 | Astrea 9: A-1 S$615m at 3.40%; A-2 US$200m at 5.70%; B US$107m PIK at 7.35%; call 2030, final 2040; NAV US$1,654m; LTV 35.2% (A) / 41.4% (B); Fitch upgraded to AA-sf / AA-sf / Asf in Aug-2026 | C | The upgrade is dated 7-Aug-2026 (from A+sf / Asf / BBBsf). The Class B US$107m includes two periods of PIK accrual, so it is not the issue size. Weighted coupon recomputed at 4.52%. | https://www.azalea.com.sg/products/astrea-9 |
| F16 | Lazard 1H-2026: ~US$124bn (+28%), LTM US$260bn; ~87% of SACV volume above 90% of NAV, 23% above par; MACV volume below 90% rose from 16% to 40%; ~27% of transactions failed or paused; LPs favour selling over rolling | C | All in the report. Caveats: the pricing charts are *buyout* CVs only. The 27% is a respondent-reported figure in the **GP-led deep dive**, during a record half. It is not an all-market failure rate for LP sales (see R2). | https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf |
| F17 | Campbell Lutyens: LP-led discount 13.9% (2025) vs 13.3% (2024); SACV 3.1% (3.6%); MACV 4.2% (9.0%); US$225bn total, LP-led 54% | C | Weighted by transaction value including unfunded. Preferred equity 5% of 2025 volume vs 7-10% in 2021-24, as stated. | https://campbell-lutyens.com/media/qwydmsgy/2025-secondary-market-flash-report_campbell-lutyens.pdf |
| F18 | ILPA 2023 CV guidance: at least 30 calendar or 20 business days to elect; non-response defaults to sell; 10 business days of LPAC review; status-quo option (no fee or carry changes, no crystallisation) | C | Also confirmed: GP rolls 100% of accrued carry "in almost all cases"; fairness opinion or partial third-party sale as price checks. | https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf |
| F19 | Yale "Project Gatsby": up to US$2.5bn, discount below 10%, Evercore advising, mosaic format, Lexington and HarbourVest evaluating; completion unverified | C (as reported) | PE Wire, 5-Jun-2025: deal "could close in the coming weeks". Completion is still unverified (no search budget). Moonfare (26-May-2025) had earlier reported "up to US$6bn". | https://www.privateequitywire.co.uk/yale-nears-2-5bn-secondary-sale-of-pe-and-vc-stakes/ |
| F20 | Harvard 2008: sought to sell ~US$1.5bn of LP stakes (Cogent hired Oct-2008); offers at 50%+ discounts on top-tier buyout; sold >US$1bn at steep discounts, only part of the target | U (partly corroborated) | WilmerHale (Mar/Apr-2009, citing NYT) confirms "Harvard is seeking to sell $1.5 billion of its private equity holdings". The discount levels, Cogent mandate and outcome could not be checked (NakedCapitalism 403, Buyouts paywall, YDN 429). Keep the low-confidence tag. | https://www.nakedcapitalism.com/2008/12/harvard-yale-other-big-endowments.html (blocked); WilmerHale URL in F8 |
| A1 | Jefferies Jul-2026 H1-2026 values tagged [C]: US$118bn (56 / 62); LP pricing 87%; buyout ~91, VC ~79, RE ~68; LP rollover ~14%; FY-26 forecast ~US$250-260bn | C, **upgrade to [S]** | From the primary text layer: US$118bn (+15%); LP US$56bn (47%); GP-led US$62bn (53%); LP pricing 87%; buyout 91%; venture 79%; RE 68%; average LP rollover 14%; updated FY-26 outlook ~US$260bn. **The dossier left two cells empty that the source fills: credit 89% and infrastructure 91%.** The dossier's statement that the PDF is image-only is incorrect. | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| A2 | Volume table 2018 to H1-2026 (Jefferies, Evercore and Lazard series) | C | Every cell matches the primary charts: Jefferies Jan-25 Fig. 1; Evercore FY-25 p.4 and H1-26 p.3; Lazard 1H-26 p.6. Also confirmed: LP volume −60% in 2020 (Jefferies); Evercore's "~55% of volume closes in H2"; Lazard's FY-26 forecast of US$275bn. | URLs in F1, F2, F4, F5, F16 |
| A3 | Buyer capital: Jefferies dedicated capital 288 / 302 / 327; overhang 1.8x / 1.5x vs ~2.2x five-year average; leverage = 15% of dry powder plus near-term fundraising; Evercore overhang 1.2x → 1.0x; evergreen ~US$500bn / >US$130bn / 45% (Evercore) and ~US$113bn / 41% (Jefferies) | C (stale) | All match. **The newer Jefferies data is omitted:** overhang 1.4x (2025) and 1.2x (H1-26 LTM; 1.3x adjusted); dedicated capital fell to US$290bn at H1-26. History: 3.1x in 2020 and 2.1x in 2022 (see R1). | URLs in F5, F6, A1, F2, F4 |
| A4 | ILPA draft CV guidance dated 24-Jun-2026, comments closed 5-Aug-2026 | C (dates only) | The ILPA page does not describe the content changes (the longer election window and the "remain in existing fund" option), so those stay [C] and unverified. | https://ilpa.org/industry-guidance/principles-best-practices/continuation-funds/ |
| A5 | ILPA subscription lines: cap of 15-25% of uncalled capital; at most 180 days outstanding; hurdle measured from the draw date; net IRR reported with and without the line | C | ILPA Jun-2017, recommendations 1, 2 and 9. | https://ilpa.org/wp-content/uploads/2017/06/ILPA-Subscription-Lines-of-Credit-and-Alignment-of-Interests-June-2017.pdf |
| A6 | Astrea 7 and 8 table rows; Astrea 9 ~3.4x subscribed with >S$3.4bn of demand; nine issues since 2006 | C | All Astrea 7 and 8 terms, NAVs, LTVs and cash flows match; their upgrades are dated 30-Sep-2026. The 3.4x / S$3.4bn figure is across all three Astrea 9 classes (news headlines listed on the Azalea site). | https://www.azalea.com.sg/products/astrea-7 ; https://www.azalea.com.sg/products/astrea-8 ; https://www.azalea.com.sg/ |
| A7 | Authors of "A Theory of Liquidity in Private Equity" (Maurin, Robinson, Strömberg) "not re-verified" | C | Crossref: *Management Science* 69(10):5740-5771 (Oct-2023). | https://api.crossref.org/works/10.1287/mnsc.2022.4612 |
| A8 | Albuquerque, Cassel, Phalippou and Schroth (2018) working paper exists | C (existence) | Crossref lists it on SSRN (2018) under the cited title. Its findings were not checked. | https://api.crossref.org/works?query.bibliographic=Liquidity+Provision+in+the+Secondary+Market+for+Private+Equity+Fund+Stakes |
| A9 | 17Capital: US$700bn NAV opportunity by 2030 (~US$150bn a year), from Preqin data plus its own assumptions | C | This is a vendor marketing estimate, not independent data. | https://www.17capital.com/ |
| A10 | Clifford Chance (2020): preferred-equity cash funding up to ~50% LTV | C | "Cash funding typically up to 50% LTV." | https://www.cliffordchance.com/content/dam/cliffordchance/briefings/2020/05/decoding-the-secondary-market-part-ii-preferred-equity.pdf |
| A11 | Morgan Lewis (2023): NAIC presumption that equity-backed debt is not a bond; LTV or liquidity tests divert cash from equity; senior interest can be deferred | C | 8-Nov-2023 ("rebuttable presumption"). Current NAIC status is still unverified, as the dossier itself says. | https://www.morganlewis.com/de/pubs/2023/11/collateralised-fund-obligations-and-rated-note-feeders-options-for-structuring-investment-into-private-funds |
| A12 | Yale endowment US$44.1bn at FY-2025 with an 11.1% return | C | Wikipedia citing P&I, 24-Oct-2025. This is a secondary source; prefer Yale's own report. | https://en.wikipedia.org/wiki/Yale_Investments_Office |
| A13 | Harvard 2008-09: HMC staff cut ~25%; endowment down ~US$8bn (~22%); hedge-fund positions liquidated | C | Wikipedia citing NYT, 20-Feb-2009. The 22% was the Jul-Oct-2008 drawdown; the full FY-2009 loss was larger. The US$2.5bn bond issue remains unverified. | https://en.wikipedia.org/wiki/Harvard_Management_Company |
| A14 | Davis Polk (2026): preferred equity is SPV equity senior to sponsor common, with a liquidation preference and enforcement through controlled accounts and monetisation rights rather than foreclosure | U | The landing page (23-Jan-2026, GLI Fund Finance 2026) carries no such description, and I did not check the chapter PDF. | https://www.davispolk.com/insights/articles-books/continuing-use-preferred-equity-private-equity-net-asset-value-facilities |
| A15 | GIC, CIC and KIC ~US$1bn trades "in aggregate explain the SWF share rising to 21%" [S] | **R** (as stated) | Evercore attributes the rise only to "large, repeat sellers". H1-26 SWF LP-led volume is about 21% × US$56bn ≈ **US$11.8bn**, roughly 4x the ~US$3bn of named processes, and GIC and CIC were 2025 processes. Retag as [I] and drop "explain". | https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf (p.14) |
| A16 | Moonfare: Yale up to US$6bn; Harvard ~US$1bn with Lexington; CalPERS sold "billions" to Ardian, AlpInvest and Partners Group; sellers add their best funds as sweeteners (HSBC) | C (as reported) | Moonfare, 26-May-2025. This is a secondary aggregator. | https://www.moonfare.com/blog/endowments-private-equity-secondaries |
| A17 | Worked example: tail interest, stale NAV 100, 0.90x remaining, sold at 70 → y = 12.1% | **X** | Not reproducible from the stated inputs. With the main example's cash-flow shape, y = **9.4%**; a flat 5-year profile gives 9.0% and a front-loaded one 13.3%. State the timing profile. The qualitative conclusion (belief dispersion matters more than the headline discount) still holds. | Verifier recomputation (scipy) |
| A18 | Worked example: NAV facility at 3.75% + 450 bp + 1.25% OID ≈ 8.7% (9.0% with sweep); 300 bp / 1% ≈ 7.1-7.4%; 2023 terms ≈ 13.0-13.4% | **X** (minor) | 8.7% is the simple sum. With quarterly pay, the effective annual IRR is **9.0% for a bullet and 9.4% with linear sweep amortisation**. For the 300 bp case: 7.1% simple, 7.3% bullet, 7.6% amortising. For 2023 terms: 12.8% simple, 13.6% bullet, 14.2% amortising. Use one convention throughout. | Verifier recomputation |
| A19 | Other worked examples: sale IRR 10.5 / 12.3 / 22.1% at prices 91 / 87 / 70; ±10% forecast → 6.3 / 10.5 / 14.5%; vendor-finance rates 9.6 / 15.4 / 21.3%; Astrea weighted coupon ~4.5%; sizing (US$106bn private, US$8.9-17.7bn payout, 4% of LP-led volume, ~21% of the SWF segment) | C | All reproduce to within 0.1 pp. | Verifier recomputation |
| A20 | Calibration: overhang O_t benign ≥1.8x, stress 1.0-1.5x, crisis <1.0x ("Jefferies, Evercore [S]") | **R** | History contradicts it. On Jefferies' measure the multiple was 3.1x in 2020 (COVID stress) and 2.1x in 2022 (stress), against 1.8x in benign 2021 and 1.4x / 1.2x in the record 2025 / H1-26 market. On Evercore's measure it was ~1.2x / 1.0x in benign 2025 / H1-26. The multiple is volume-endogenous (see R1). | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf (Fig. 11); Jefferies Jul-2025 (Fig. 9) |
| A21 | Calibration: execution probability p_j of 0.85-0.95 in benign regimes, based on "~27% failed or paused 1H-26 [S]" | **X** | The cited statistic implies p ≈ **0.73** in a *benign, record* half, and it covers GP-led processes, not LP portfolio sales. Evercore H1-26 also says the LP-led segment is "where bid-ask spreads are still pausing or pulling processes". Recalibrate to about 0.70-0.80 benign for GP-led-type processes, or label the default [I]. | URLs in F16 and F2 (p.21) |
| A22 | Calibration: benign NAV spreads by LTV (≤10 / 10-25 / 25-50%) of 400-450 / 450-500 / 550-650 bp, tagged "Proskauer 2025 [S]" | **X** (label) | Proskauer FY-2025 gives only an unconditional spread distribution (10% below 3%; 21% at 3-4%; 24% at 4-5%; 14% at 5-6%; 10% at 6-7%; 14% at 7-8%; 7% at 8% or more), not spreads by LTV. The LTV mapping is [I]. | URL in F12 |

---

## 4. Citation check (the 10 most important references, plus problems found elsewhere)

| Ref | Exists | Authors, year, title, venue | Notes |
|---|---|---|---|
| 1. Jefferies (10-Feb-2026), *2025 Global Secondary Market Review: Another Record-Breaking Year* | Yes | Correct | Content verified. |
| 4. Jefferies (Jul-2026), *Global Secondary Market Review* | Yes | Correct | **Wrongly described as image-only.** The text layer extracts with pypdf. Ref 36 (Angel Investors Network, a low-reliability aggregator) can be dropped. |
| 5. Evercore PCA (Jul-2026), *H1 2026 Secondary Market Review* | Yes | Correct | Content verified. |
| 6. Evercore PCA (Feb-2026), *2025 Secondary Market Report* | Yes | Correct | Content verified. |
| 7. Lazard PCA (Aug-2026), *Interim Secondary Market Report 2026* | Yes | Correct | Content verified. |
| 9 / 10. Proskauer, *NAV Lending Market FY-2023* (pub. 2024) and *NAV Financing Market FY-2025* (pub. 2026) | Yes | Correct | Content verified. |
| 11. ILPA (2024), *NAV-Based Facilities guidance* | Yes | Correct | The LPAC-consent recommendation is cited to Parts I-II but lives in **Part III**, which the reference list omits. Add the Part III URL. |
| 14. Nadauld, Sensoy, Vorkink & Weisbach (2019), *JFE*, DOI 10.1016/j.jfineco.2018.11.007; NBER WP 22404 (2016) | Yes | Correct | Add volume, issue and pages: 132(3):158-181. |
| 15. Bollen & Sensoy (2022), *Financial Management* 51(2):501-538, DOI 10.1111/fima.12375 | Yes | Correct (online Aug-2021) | The quantitative claim comes from the 2015 working paper but is presented as a published result (see F10). |
| 17. *A Theory of Liquidity in Private Equity*, *Management Science*, DOI 10.1287/mnsc.2022.4612 | Yes | Authors **Maurin, Robinson & Strömberg are correct**; the dossier flagged them as unverified | Add 69(10):5740-5771 (2023). |
| 16. Albuquerque, Cassel, Phalippou & Schroth (2018) | Yes (SSRN) | Correct title and authors | The "Cass working paper" affiliation was not checked. |
| 19. WilmerHale / ABA *Business Law Today* 18(4), Mar/Apr-2009 | Yes | **Title garbled and authors missing** | The actual title is *"Trends in the Private Equity Secondary Market: A Response to Today's Financial Markets"*, by T. A. Beaudoin, J. C. Berrent, S. C. Evans and S. Rothermel. |
| 18. Unquote (26-Jan-2009) | Yes | Correct | Content verified. |
| 26 / 27 / 28 / 31. Azalea, Octus, Morgan Lewis, Clifford Chance | Yes | Correct | Content verified. |
| 30. Davis Polk (23-Jan-2026), GLI Fund Finance 2026 | Yes | Date and venue correct | "Ch. 9" and the instrument description were not verified (A14). |
| 22. Harvard 2008-09 sources (NakedCapitalism, Buyouts, YDN) | Partly | – | Blocked or paywalled. Claims rest on excerpts; keep the [S/C] low-confidence tag. |

No hallucinated references were found among the roughly 25 of 36 that I fetched or checked against Crossref. I did not fetch the rest: LMA Apr-2026, AI-CIO, Augment, BGOV, Bloomberg, DealStreetAsia and Angel Investors Network. Most are already tagged [C] in the dossier.

---

## 5. Reasoning issues and overclaims in the design implications

Severity scale: **H** = must fix before IC use; **M** = fix before calibration; **L** = tidy-up.

**R1 (H). The capital-overhang regime mapping is inverted (Section 6.6).** The overhang multiple is dedicated capital divided by LTM volume, so it is endogenous to volume. It *rises* when volume collapses: Jefferies shows 3.1x in 2020 and 2.1x in 2022, against 1.8x in benign 2021. It *falls* in booms: 1.4x in 2025 and 1.2x in H1-26. Under the dossier's thresholds, today's record market (1.2x Jefferies, ~1.0x Evercore) would be classed as "stress" or "crisis".

The two definitions also differ: Evercore includes leverage and LP co-investment; Jefferies uses dedicated capital only. Section 6.6 mixes them anyway, which contradicts the dossier's own warning in Section 1.

*Fix:* drop O_t as a regime classifier. Use it only as a depth-capacity input, conditioned on the regime from the HMM. Calibrate depth from buyer dry powder plus fundraising, haircut in stress.

**R2 (H). Execution risk is both mis-calibrated and mis-specified (Sections 3.4, 6.3 and 6.6).**
- (a) The benign p_j of 0.85-0.95 is cited to Lazard's 27% failed-or-paused rate. That rate comes from the GP-led section in a record half, and implies about 0.73 (A21).
- (b) The coverage rule sums *expected* liquidity, q^eff = p_j·Δq_j·1{τ_j ≤ H}, and requires it to cover the need. That is coverage in expectation, not the stated chance constraint Pr(…) ≥ 1−α. Execution is binary and failures are correlated within a regime (market-wide pauses, buyers walking away as in 2008), so expected-value coverage overstates survival.

*Fix:* simulate correlated execution indicators per scenario (a common regime factor plus idiosyncratic risk) and impose the chance constraint on realised liquidity.

**R3 (H). The Tier-2 objective double-counts (Section 6.4).** Suppose W_T and Pr(R ≥ 10%) come from a simulation that already books sale proceeds, forgone distributions, financing flows and forced sales. Then subtracting PV_m(G) − PV_m(L) and ξ·E[fire-sale loss] counts the same economics a second time. The objective also adds a probability, which is dimensionless, to dollar-valued penalties without any scaling.

*Fix:* let simulated wealth carry the cash-flow economics. Add separate penalties only for items not in cash flows (signalling, relationship). Alternatively, use a value-based objective in which liquidity cost enters exactly once. Normalise every term to a common unit.

**R4 (H). The shadow-price SELL test omits the base value of the cash raised (Sections 2.1 and 3.2(3)).** As written, the test is Σ λ_{t,s}·L ≥ PV_m(G) + Signal + Irrev, where λ is "the dual price of the liquidity constraint". That multiplier is zero when the constraint is slack, so the rule would reject *any* sale, including one above fair value.

*Fix:* use Σ (m_{t,s} + λ_{t,s})·L ≥ PV_m(G) + Signal + Irrev, or redefine λ explicitly as the full marginal value of a dollar. The same fix applies to the CV rule λ·P_CV ≥ PV_m(…), which should use (1+λ)·P_CV.

**R5 (H/M). Crisis-price calibration risks double-counting staleness (Sections 6.5 and 6.6).**
- The crisis π of 0.60-0.65 is calibrated to the H2-2008 *headline* (61% of stale NAV).
- The price equation in Section 6.5 separately multiplies by V̂/NAV^ref, the de-smoothing factor.
- If both are applied, crisis prices fall to about 0.45. Cogent's adjusted figure implies a residual discount of only about 16.5% against adjusted NAV.

Two further problems:
- 61% is the average *high bid*: an upper bound on clearing prices, from a selected sample of funds brought to market.
- "Crisis = normal × 61/89" pairs the 2008 crisis with a 2024 baseline. The H1-2008 baseline of 84.7 would give a 0.72 multiplier, against 0.685.

*Fix:* calibrate exp(μ_crisis) to the staleness-adjusted level and let the staleness term carry the rest. Document which NAV each π refers to.

**R6 (M). The MCL linear program has a units error (Sections 3.4 and 6.5).** The objective min Σ c_j·x_j multiplies a *per-dollar* cost by a tranche *fraction* x_j ∈ [0,1], with no tranche size. Large tranches therefore look free, and the coverage dual is not "the marginal cost of the last dollar".

*Fix:* minimise Σ c_j·Δq_j·x_j, or define x_j in dollars. Separately, c_j is defined as either "value cost per dollar" or "IRR spread over the hurdle". The reserve-price rule y^SG_i − λ ≤ δ^belief then compares an IRR with a PV-per-dollar dual. Pick one unit.

**R7 (M). The tail-end implied cost of "about 15-25%" conflicts with the dossier's own evidence (Sections 1 and 3).**
- Nadauld et al. find that, on a PME basis, *sellers* of 10+ year funds outperform buyers. The tail discount therefore compensates for lower-quality residual assets and NAV overstatement, not a liquidity transfer.
- The dossier's own tail example gives 9-13% (A17).

*Fix:* present the tail cost as belief-dependent, with a lower central estimate, and cite the PME finding.

**R8 (M). "Irrev" is not the option value of waiting (Section 6.4).** The definition max(0, E[π_{t+1}] − π_t)·V̂ applies max to an expectation, whereas option value is an expectation of a max (Jensen's inequality). It also ignores interim cash flows, discounting and the risk that π falls. It is inconsistent with the Dixit-Pindyck hurdle in Section 2.3.

*Fix:* use the continuation value from the Longstaff-Schwartz stopping problem already proposed in Section 7.

**R9 (M). Evergreen buyer capital is treated as stable depth, but it is pro-cyclical.** Jefferies Jul-2026 (p.11) reports that 2026 "triggered elevated redemptions across the evergreen capital pool", with several managers activating 5% NAV gates. The dossier counts evergreen capital (~US$500bn AUM, 41-46% allocated to secondaries) as deepening the market.

*Fix:* haircut evergreen buyer capacity in stress regimes, inside Depth_s and the price-impact term.

**R10 (L/M). The 30-day revolver haircut is inconsistent with its stated analogy (Section 6.3(2)).** Basel III's LCR gives *zero* credit (a 100% haircut) to committed facilities a bank receives, yet the dossier sets h^rev ≥ 50%.

*Fix:* either adopt 100% for the 30-day stress bucket or justify 50% from the legal draw-stop terms.

**R11 (L/M). NAV-facility mechanics (Sections 3.2(4) and 6.5).**
- The LTV recursion adds both accrued interest (B_t·r_t·Δ) and PIK_t, which double-counts if PIK is the accrued interest. Cash interest paid from distributions is not separated from the principal sweep.
- y_NAV adds E[fire-sale loss]/B_0, a one-off fraction, to annual rates without annualising it.
- E[fire-sale] sums per-period breach probabilities, which double-counts paths that breach repeatedly.

*Fix:* use path-wise first-passage loss from the Monte Carlo already proposed.

**R12 (L). The preferred-equity accrual recursion over-accrues (Section 3.2(6)).** Acc_t = Acc_{t−1}(1+r_p) − X_{t−1} charges interest on amounts already paid, by r_p·X_{t−1} each period.

*Fix:* Acc_t = (Acc_{t−1} − X_{t−1})(1+r_p).

**R13 (L). The "common kernel" is defined inconsistently (Section 2.1).** It is given as "scenario deflators *or* a risk-adjusted hurdle by asset". Asset-specific hurdles are not one kernel, and they undermine the stated purpose of comparing sales and loans consistently.

**R14 (L). The price-impact functional form changes between sections.** Section 3.4 uses a linear form, π(q) = π_0 − κq/Depth. Section 6.5 uses a log-linear form, exp(−κq/Depth). Choose one.

**R15 (L/M). Several derived values carry [S] tags in Section 6.6.**
- The buyer target IRRs of 14 / 16 / 17 / 23% are M^(1/4) conversions assuming a 4-year bullet.
- The NAV spreads by LTV are inferred (A22).
- "Credit (senior)" stress values of 0.72-0.77 come from Jefferies' *all-credit* series for 2022-23, not senior credit.
- The real-estate "stress" value of 0.70 is almost equal to "benign" (0.71). That implies no stress sensitivity, although RE fell from 83% to 76% in 2020.

**R16 (L). The belief-gap interpretation is too binary (Section 3.2(1)).** Δy > 0 is read as "SG forecast too optimistic or ADIC has private information". Two other explanations exist:
- Buyer targets are *gross* hurdles, often enhanced by deferral (a form of leverage) and third-party leverage (14% of respondents in 2025). They are not clearing returns.
- Risk and illiquidity premia differ between a long-horizon sovereign holder and a fund buyer.

**Also noted.**
- The dossier's "deferral share 26-50%" default understates deferral depth. In Evercore's H1-26 data, about half of deferred LP-led volume defers more than 50% of the price (26-50%: 16% of volume; 51-75%: 12%; 76-100%: 5%), and 9% of LP-led volume defers more than 18 months.
- Jefferies H1-26 reports deferrals in 26% of LP sales and structured elements in 33%. Update Section 6.6.

---

## 6. Recomputed numbers

| Item | Dossier | Recomputed | Status |
|---|---|---|---|
| Sale IRR at 91 / 87 / 70 (flows 22, 28, 30, 25, 15) | 10.5 / 12.3 / 22.1% | 10.48 / 12.34 / 22.14% | OK |
| Forecast ×0.9 / 1.0 / 1.1 at 91 | 6.3 / 10.5 / 14.5% | 6.29 / 10.48 / 14.50% | OK |
| Tail 0.90x sold at 70 | 12.1% | 9.4% (same shape); 9.0% (flat); 13.3% (front-loaded) | Not reproducible |
| Buyer multiples → IRR (4-year bullet) | 14 / 16 / 17 / 23% | 14.2 / 15.8 / 17.4 / 23.1% | OK (bullet assumption) |
| Vendor-finance rate for 50 / 33 / 25% deferred | 9.6 / 15.4 / 21.3% | 9.64 / 15.37 / 21.33% | OK |
| NAV facility, 3.75% + 450 bp + 1.25% OID, 3y | 8.7% (9.0% with sweep) | 8.67% simple; 9.02% bullet; 9.42% amortising | Labels mixed |
| NAV facility, 300 bp + 1% OID | 7.1-7.4% | 7.08 / 7.32 / 7.63% | OK, roughly |
| NAV facility, 2023 terms (5.30% + 681 bp + 2%) | 13.0-13.4% | 12.78 / 13.56 / 14.24% | Slightly low |
| Astrea 9 weighted coupon | ~4.5% | 4.52% | OK |
| Sizing: private NAV; payout; US$5bn as % of LP-led; as % of SWF segment | 106 / 8.9-17.7 / 4% / ~20% | 106.2 / 8.85-17.70 / 4.0% / 21.3% | OK |
| Staleness factor 61/83.5 | 0.73 | 0.7305 | OK |

---

## 7. New primary-source data the dossier should absorb

All of the following come from Jefferies Jul-2026 (primary text), unless noted.

- **Dedicated capital and overhang:** dedicated capital US$290bn at H1-26, down from US$327bn. Overhang 1.2x (H1-26 LTM; 1.3x adjusted) and 1.4x (2025). Total available capital including traditional LPs is ~US$328bn.
- **Pricing gaps:** credit 89% and infrastructure 91% in H1-26. Tail-end funds (10+ years) at 25%+ discounts. Asia and emerging markets at 35%+ discounts.
- **Deal structure:** structured elements in 33% of LP sales, deferrals in 26%. Average LP rollover in CVs 14%. 82 of the top 100 sponsors have done a CV.
- **Distribution yield:** LP portfolios yielded ~10% in H1-26. The yield has been below 20% since 2023, against a 25% average since 2001. This is directly relevant to ADIC's declining DPI, so share it with the PE cash-flow stream.
- **Evergreen stress:** elevated redemptions in 2026, and 5% NAV gates activated at several managers (R9).
- **Evercore H1-26 deferral depth:** see the note at the end of Section 5.

---

## 8. Overall reliability rating

**HIGH (empirical layer) and MEDIUM (design and calibration layer).**

The evidence base can go to the IC once the seven corrections in Section 3 are applied: F8, F10, F13, A17, A18, A21 and A22, plus the refutations A15 and A20.

The design implications should not drive any IC-facing number until R1-R5 are fixed. These issues change which instruments the optimiser chooses and how much liquidity it believes it can raise in stress:
- regime classification;
- execution and chance-constraint treatment;
- objective double-counting;
- the SELL decision rule;
- crisis-price calibration.

R6-R9 should be fixed before calibration.
