# Verification log: Stream 04, private-equity cash flows, NAV modelling and the DPI decline

| | |
|---|---|
| **Dossier** | `research/dossiers/04_pe_cashflows.md` (prepared 2026-10-18, 558 lines) |
| **Verified** | 2026-10-18, adversarial fact-check pass |
| **Overall reliability** | **HIGH** for the empirical evidence: all 18 author-flagged claims are confirmed against primary documents. **MEDIUM** for the design layer (Section 6 of the dossier): four must-fix logic or formula issues, listed in Section 5 below. |

---

## 1. Summary

**Coverage.** I checked 26 claims: all 18 author-flagged claims, plus 8 more. The extra claims were chosen because the IC narrative leans on them or because they looked suspicious:
- the MSCI exit and entry multiples;
- an MSCI attribution about "restrained calls";
- the stated range of MSCI data revisions;
- the PitchBook IPO line;
- the Basel LCR40.64 drawdown rates;
- the MSCI software multiples;
- the Cliffwater/ERSRI case study;
- an unsourced LP-survey statistic.

I also checked 18 references for existence and metadata.

| Verdict | Count |
|---|---|
| Confirmed | 22 (all 18 flagged, plus 4 supplementary) |
| Corrected | 3 |
| Refuted | 0 |
| Unverifiable | 1 |

**The market-data backbone is accurate.** I extracted the text layers of 11 primary PDFs locally and traced about 150 numbers.
- Every cell of the Section 4.1 MSCI cash-flow table matches the October-2026 report. The only difference is that MSCI prints 2018 net flow as +$18bn, against the dossier's arithmetic +$17bn.
- The Cambridge Associates vintage DPI and RVPI values match exactly.
- The figures attributed to the following papers were all found verbatim in the papers: Brown–Ghysels–Gredil, Robinson–Sensoy, Ljungqvist–Richardson, Sorensen–Wang–Yang, Gupta–Van Nieuwerburgh, Nadauld et al. and Luxenberg et al.

**The three corrections concern attribution and precision. No headline number is wrong.**
1. **"Restrained calls" is about all private capital, not PE.** MSCI's sentence explains the all-private-capital H1-2026 distribution/contribution (D/C) ratio of 1.1. For PE, H1-2026 net flow was −$16.5bn with a D/C ratio of 0.9.
2. **Revisions are +1 to +3pp, not "1–4pp".** This compares the PE distribution rates in MSCI's May-2026 deck with the October-2026 report.
3. **The PitchBook IPO line is misread.** The $27.6bn is "IPO value", not proceeds raised. It is also 26.9% of the $102.6bn exit value, not the 30.5% that Cherry Bekaert prints. That inconsistency is inside the source and was carried into the dossier.

**There is one citation error.** Sorensen, Wang & Yang (2014) is in *RFS* 27(7), pp. 1977–2021, not 27(2). The other 17 references exist with correct authors, year, venue and pages. That includes the recent Jeet et al. (2026) *JPMI* article, which I had marked as suspicious.

**Four issues in the design layer must be fixed before outputs reach the IC.** Details are in Section 5.1.
1. **Fees are double-counted.** The fused alpha is defined as *net* of fees (it is fused from net-of-fee PME and direct alpha), and E2 then subtracts the fees again. The result is a systematic bias toward SELL.
2. **The alpha runway runs on the drought-slowed clock.** It uses effective age, so a drought extends the full-alpha window by about 1.8 years at the current drought length. The model therefore credits extra value creation during exactly the stalled holds that the dossier's own evidence describes.
3. **The liquidity shadow price has a units error.** A dual (value per dollar at a date) is added to rates and compared with annual excess returns. The stated IRR rule is not equivalent to the NPV rule. The REFINANCE value test also places the collateral return in the wrong comparison.
4. **Exit pricing is calibrated to a selected statistic and is over-determined.** The "75% exit above the prior mark" figure is conditional on an exit having happened. It is applied to unsold inventory and SELL pricing, on top of a distribution rule that already prices exits off economic NAV.

---

## 2. Method and limitations

**Method.**
- **Primary PDFs.** I downloaded each into an isolated folder and extracted its text with pypdf:
  - the MSCI *Private Capital Benchmarks Summary Q2 2026* (October 2026);
  - the MSCI *Private Capital in Focus* deck (13 May 2026);
  - the Jefferies *Global Secondary Market Review* (July 2026);
  - the Cambridge Associates US PE legacy benchmark book (31 Dec 2019);
  - NBER working papers w17428 (Robinson–Sensoy), w9454 (Ljungqvist–Richardson), w19612 (Sorensen–Wang–Yang) and w26514 (Gupta–Van Nieuwerburgh);
  - the BGG working paper (UNC IPC, April 2020);
  - arXiv:2207.07767 (Luxenberg et al.);
  - the Cliffwater/ERSRI pacing plan (December 2023).
- **Web pages.** I read these directly:
  - Bain's 2026 report chapter and its press release, and the Bain midyear press release;
  - the MSCI blog post of 14 January 2026;
  - Cherry Bekaert (17 August 2026) and Rede Partners (23 June 2026);
  - the NBER abstract pages, the OUP abstract of BGG, the UNC IPC abstract and the RePEc page for CEPR DP16910;
  - the CBS research portal, arXiv and BIS LCR40.
- **Reference metadata.** Checked against Crossref DOI records.
- **Arithmetic.** I recomputed every derived number used below in a script: D/C ratios, implied NAV bases, toy-programme flows, Markov spell probabilities, smoothing autocorrelations and the Luxenberg steady state.

**Limitations.**
- **Web search ran out.** The session-wide web-search budget was exhausted partway through. After that I verified only by fetching known primary URLs.
- **McKinsey is verified through a secondary source.** The primary McKinsey PDF timed out twice. The McKinsey figures were confirmed through the TEXPERS reproduction, which quotes McKinsey's sentences, and through other summaries of the 6%/16% figure.
- **Some published versions were not re-checked.** The numbers from Robinson–Sensoy, Gupta–Van Nieuwerburgh and Sorensen–Wang–Yang were verified in the NBER working papers, not in the published journal versions.

---

## 3. Claims table

### 3.1 Author-flagged claims (18)

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| F1 | MSCI global PE distribution rate 24/21/18/17% (2017–20), 27% (2021), 11/9/11/11% (2022–25), 9% (H1-26). Contribution rate 27–31% (39% in 2021). | **Confirmed** | Every value matches p.13. The contribution rates read 31/30/28/29/39/31/27/28/29/31 (H1-26). | https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf |
| F2 | MSCI PE net flow −$127bn/−133/−52/−2/−16.5 (H1-26). D/C 0.7–1.0. 2025 distributions of $489bn were the second-highest in the series. | **Confirmed** | Matches p.13 (the H1 −$16.5bn is from the text). "Second-highest" is true only of the 2017–H1-2026 window MSCI shows. The executive summary's "on record" is not supported, because MSCI makes no record claim. The 2025 figure was revised from $449bn (May-2026 deck) to $489bn. | same as F1 |
| F3 | Bain: 32,000 unsold companies worth $3.8tn; buyout hold at exit about 7 years (5–6 years in 2010–21); distributions under 15% of NAV for four years, a record; 2025 exit value $717bn (+47%); IRR stagnates around year 7; TVPI flattens after year 8. | **Confirmed** | The IRR and TVPI pattern refers to 2000–15 vintages. Also confirmed: the 2025 rate was 14%; 1,570 exits (−2%); seven exits above $10bn were 22% of value; CVs were under 10% of exit value; "12 is the new 5" (5% versus 10–12% EBITDA growth for 2.5x over five years). | https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ ; https://www.bain.com/about/media-center/press-releases/2026/private-equity-resurgence-gathers-steam-as-new-era-challenges-firms-to-enhance-value-creationbain--company-global-pe-report/ |
| F4 | Jefferies H1-26: record $118bn; LP portfolios priced at 87% of NAV; buyout 91, VC 79, infrastructure 91, credit 89, real estate 68; tail-end funds (10+ years) at 25%+ discounts; 33% of LP sales structured (26% with deferrals); 2026 forecast about $260bn. | **Confirmed** | Also confirmed: 2025 volume $240bn; LP-led 47% and GP-led 53%; North America 88% and Europe 86%; pensions and SWFs 48% of LP supply. Jefferies itself warns that aggregate pricing "is not appropriate for the valuation of individual fund interests" (see R15). | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| F5 | Robinson–Sensoy: elasticities of buyout distributions and calls to ln(P/D) of 0.37 and 0.33; net cash flow procyclical; wider spreads cut distributions far more than calls; 92% idiosyncratic. | **Confirmed** | Checked in NBER WP (Sept 2011): 837 funds, 1984–2010. Buyout net cash flow is 92.1% idiosyncratic (VC 92.5%). The spread is Moody's Baa–Aaa, orthogonalised to P/D. Net cash flow turns positive at age 3–4 and rises until about age 8. The JFE 2016 version was not checked. | https://www.nber.org/system/files/working_papers/w17428/w17428.pdf |
| F6 | Ljungqvist–Richardson: six years to invest 90%; median fund takes four years to reach 80%; average fund's IRR turns positive only in year 8. | **Confirmed** | "it takes six years for 90 percent"; "average (median) fund takes 3.69 (4) years" to reach 80%; "does not turn positive until the eighth year". 93.6% is invested by year 10. | https://www.nber.org/system/files/working_papers/w9454/w9454.pdf |
| F7 | BGG: beta 1.05–1.10 (buyout) and 1.20–1.32 (VC) in the WP, versus about 1.0 and 1.4 in the published abstract; total risk 33% and 38–40%, 10–13pp above reported NAV; median weekly smoothing 0.951. | **Confirmed** | WP: risk 33% (38%), "+10 [13] percentage points". RFS abstract: beta "around 1.0 (1.4)", risk "33% (40%)". λ = 0.951 gives 77.4% weight on valuations at least 5 weeks old. NAV noise 4.6% mean, 3.1% median. About 10% of funds fail to converge with fund-specific estimates (3.3% after peer imputation). The Ang et al. priors are N(1.25, 0.25), N(1.80, 0.30) and N(0.77, 0.23). | https://academic.oup.com/rfs/article/36/3/945/6646564 ; https://uncipc.com/wp-content/uploads/2020/04/BGG_nowcasting.pdf |
| F8 | CA pooled US PE DPI at 31-Dec-2019: 2010 1.27 (RVPI 0.48); 2012 0.64 (0.93); 2014 0.36 (1.09); 2016 0.11. | **Confirmed** | Also confirmed: 2009 1.45, 2011 0.94, 2013 0.43, 2015 0.19, 2010 TVPI 1.75, and "at least six years to settle into their final quartile". Calling this the "normal" curve is an inference, and the ages the dossier maps to these vintages are off (see R6). | https://www.cambridgeassociates.com/wp-content/uploads/2020/06/WEB-2019-Q4-USPE-legacy-Benchmark-Book.pdf |
| F9 | McKinsey: DPI was 6% of PE AUM in the 12 months to June 2025 (2015–19 average 16%); more than 16,000 companies (52% of buyout inventory) held over 4 years. | **Confirmed (secondary)** | Quoted in TEXPERS's reproduction of McKinsey. Also confirmed: $1.3tn of 2025 PE-backed exit value (+41%). The primary PDF timed out. The "record" qualifier for the 52% could not be verified. | https://www.texpers.org/index.php?option=com_dailyplanetblog&view=entry&year=2026&month=02&day=13&id=386%3Amckinsey-s-global-private-markets-report-2026-private-equity-clearer-view-tougher-terrain |
| F10 | Nadauld et al.: buyer PME 1.023 against seller 0.974, about 5pp a year (about 3pp for funds aged 4–9); most trades at a discount to NAV. | **Confirmed** | NBER abstract. A published version exists in the JFE (doi 10.1016/j.jfineco.2018.11.007). | https://www.nber.org/papers/w22404 |
| F11 | Sorensen–Wang–Yang: break-even alpha 3.08% under 2/20, falling to 2.06% at D/E 3; illiquidity cost comparable to GP compensation. | **Confirmed** | WP text: "without leverage, the break-even alpha is 3.08%"; D/E 3.0 gives 2.06%. Total costs split about 50% illiquidity, 25% fees, 25% carry. (The citation issue number is wrong; see Section 4.) | https://www.nber.org/system/files/working_papers/w19612/w19612.pdf |
| F12 | CV flows equalled 20% of mature (10+ year) PE fund distributions in 2021–Q3 2025, against about 6% in 2016–20. | **Confirmed** | The metric is contributions to continuation funds *relative to* distributions from 10+ year funds: a ratio, not a share (see R14). Blog post of 14 January 2026. | https://www.msci.com/research-and-insights/blog-post/private-capital-in-focus-trends-to-watch-for-2026 |
| F13 | Across 2,617 IPO exits, one in four positions returned close to nothing in the two years after listing; listing is not the liquidity event. | **Confirmed** | p.3. MSCI also says "The listing itself is not the liquidity event". | same as F1 |
| F14 | Bain midyear: "triple shock"; PE software marks down about 8% in Q1-26; about 75% of buyout assets exit above the next-to-last mark; about 33,000 unsold companies. | **Confirmed** | Release of 8 June 2026. Software marks fell 8.9% in the US and 4.2% in Europe (proprietary MSCI analysis); tech deal value fell 70% QoQ. The ILPA poll (>5% discount) and "one in five cutting buyout" are also confirmed. | https://www.prnewswire.com/news-releases/winning-firms-will-focus-on-what-they-can-control-weather-the-rest-as-triple-shock-brakes-private-equitys-latest-revival-bain--company-2026-midyear-pe-report-302793107.html |
| F15 | PitchBook via Cherry Bekaert, 30-Jun-2026: distribution yield 14.8% (long-run 23.4%); median hold at exit about 5.5 years; 13,509 companies in inventory; Q2 exits $102.6bn across 353; NAV-loan LTV 5–30%. | **Confirmed (attribution caveat)** | All values appear in the 17-Aug-2026 article (hold down from 6.4 years; exits −46.3% QoQ and −7.4% YoY). Cherry Bekaert names PitchBook for chart data. It gives **no source** for the distribution yield, the inventory count, the NAV-loan LTV, the buyout share (63%) or the BDC redemption figures. | https://www.cbh.com/insights/reports/private-equity-mid-year-2026-report/ |
| F16 | Rede: NAV margins converging on 4–7%; most facilities used for follow-ons; early DPI-motivated deals. | **Confirmed** | "converge around a 4-7% margin range"; "early signs of an uptick in transactions specifically aimed at boosting DPI". Dated 23 June 2026. | https://www.rede-partners.com/news-insights-database/publication-rede-nav-2026 |
| F17 | Luxenberg et al.: stochastic linear state-space model with logit-normal intensities; λ1 ≈ 0.26, λ0 ≈ 0.13, δ ≈ 0.33; steady-state NAV about 3.7× annual commitment; MPC tracks the relaxed-liquid frontier over 20 periods. | **Confirmed** | λ1 = .26, λ0 = .128 (set as λ0 = ½λ1) and δ = .33; αI = 3.685; Figure 7 uses 200 simulations of 20 periods. Caveat: the 15.8% is the mean *log* return (variance 0.079), so E[R] is about 21.8%. The paper solves a growth problem with no payouts (see R16). | https://arxiv.org/pdf/2207.07767 |
| F18 | Gupta–Van Nieuwerburgh: average risk-adjusted profit (RAP) per $1 committed −18c (buyout), −11c (VC), −17c (real estate), −10c (infrastructure); about a quarter of funds above +10c. | **Confirmed** | NBER WP (Nov 2019): "about a quarter of funds delivering in excess of 10 cents" (real estate 22%, infrastructure 27%). Cash flows are normalised per $1 committed. Figures in the JF 2021 version were not checked. | https://www.nber.org/system/files/working_papers/w26514/w26514.pdf |

### 3.2 Supplementary claims (8)

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| S1 | Top-quartile buyout exit multiple 18.2x EBITDA in H1-26, a series high since 2016; median 12.5x; median entry 11.3x (Section 1 item 2). | **Confirmed** | p.11. The exit–entry spread is about 1.2x. | same as F1 |
| S2 | "MSCI attributes the H1 balance to restrained calls rather than a genuine pickup in distributions" (Section 4.1, about PE). | **Corrected** | MSCI's "restrained capital calls" sentence is about **all private capital** (H1 D/C 1.1, p.12). For **PE** (p.13), MSCI says Q2's +$4.7bn was "a partial offset to a weak Q1" and that the data point to "an exit market that is yet to bounce back". | same as F1 |
| S3 | MSCI's May-2026 deck put PE distribution rates "1–4pp higher" for the same years (Section 4.1, a modelling-risk claim). | **Corrected** | **+1 to +3pp**: 2017 27% vs 24% (+3); 2018–21 +2pp each (23/20/19/29 vs 21/18/17/27); 2022–25 +1pp each (12/10/12/12 vs 11/9/11/11). The May deck itself calls ~20% the PE "historical norm". | https://www.msci.com/downloads/web/msci-com/discover-msci/events/event-assets/2026/may/Presentation_%20Private%20Capital%20in%20Focus_USEurope_May132026.pdf |
| S4 | "Q2-2026 US PE-backed IPOs raised $27.6bn across 12 deals, 30.5% of exit value; median IPO $2.8bn" (Section 4.4). | **Corrected** | Cherry Bekaert reports "IPO value" of $27.6bn, not proceeds raised. $27.6bn / $102.6bn = **26.9%**, so the 30.5% share printed in the source is internally inconsistent. Flag it rather than carry it forward. The 12 listings and $2.8bn median are confirmed. | https://www.cbh.com/insights/reports/private-equity-mid-year-2026-report/ |
| S5 | Basel LCR40.64 30-day drawdown rates: retail 5%; non-financial corporates 10% (credit) or 30% (liquidity); banks 40%; other financial institutions 40% or 100%; SPEs 100%. | **Confirmed** | LCR40.64(1)–(7), verbatim. | https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30 |
| S6 | Software entry multiples 5–7 turns above the buyout median since 2020, peaking near 19x; 2025 median exit multiple 16.6x; rising loss ratios (MSCI, May 2026). | **Confirmed** | Deck pp.26–27: "peaking near 19x in 2021–22"; exits "pulled back materially in 2025 to 16.6x median". | same as S3 |
| S7 | Cliffwater/ERSRI: plan assets $10.9bn to $9.8bn in the shock case; PE 16% to about 18% against a 12.5% target; over-commitment ratio 1.5x–1.9x; 2% growth case; no-new-commitment case. | **Confirmed** | $10.87bn to $9.78bn; PE 16.2% to 18.4%; target 12.5%; (unfunded + fair value)/target between 1.48x and 1.93x. | https://data.treasury.ri.gov/dataset/40fb544c-65c5-464f-ba49-e3f65d1adc36/resource/7783fe26-a966-4850-82e0-f3f931812015/download/1a-cliffwater-pe-pc-ra-pacing-plan-dec-2023-final.pdf |
| S8 | "53% of LPs say undrawn commitments limit new commitments, 15pp higher than at end-2024; about two-thirds prefer to hold out for a higher MOIC" (Section 4.6). | **Unverifiable** | The dossier names no source. The figures are not in the Bain midyear release, and no search budget remained. Drop them or source them before IC use. | — |

---

## 4. Citation check

| Reference as cited | Verified metadata | Status |
|---|---|---|
| Takahashi & Alexander (2002), *JPM* 28(2) 90–100 | Crossref: *JPM* 28(2), 90–100, 2002 | Correct |
| Luxenberg, Boyd, Kochenderfer, van Beek, Cao, Diamond, Ulitsky, Menda, Vairavamurthy (2022), arXiv:2207.07767 | arXiv: same nine authors, v1 of 15 Jul 2022; preprint only | Correct |
| Brown, Ghysels & Gredil (2023), *RFS* 36(3) 945–986 | OUP: *RFS* 36(3), March 2023, 945–986 (online 25 Jul 2022) | Correct |
| Robinson & Sensoy (2016), *JFE* 122(3) 521–543; NBER 17428 | NBER page: *JFE* 122(3), 521–543 | Correct. The figures come from the 2011 WP, so label them as WP figures, as the dossier already does for SWY, GVN and Nadauld. |
| Ljungqvist & Richardson (2003), NBER WP 9454 | NBER: Jan 2003, "The cash flow, return and risk characteristics of private equity" | Correct |
| **Sorensen, Wang & Yang (2014), *RFS* 27(2)** | NBER page: ***RFS* 27(7), 1977–2021** | **Error: issue number and pages wrong** |
| Nadauld, Sensoy, Vorkink & Weisbach (2016), NBER 22404 | NBER: Jul 2016; published in *JFE* (doi 10.1016/j.jfineco.2018.11.007) | Correct; the published version is not cited |
| Gupta & Van Nieuwerburgh (2021), *JF* 76(6) 3255–3307 | Crossref: *JF* 76(6), 3255–3307, Dec 2021 | Correct |
| Buchner, Kaserer & Wagner (2010), *JAI* 13(1) 41–54 | Crossref: identical | Correct |
| Gourier, Phalippou & Westerfield (2024), *JF* 79(5) 3407–3457 | Crossref: identical. The CEPR DP16910 abstract confirms the content claims: under-allocation; investors would pay more to adjust quantity than to remove timing uncertainty; premia rise with secondary liquidity and persist across many funds. | Correct |
| Couts, Gonçalves & Rossi (2024), *RFS* 37(7) 2110–2155 | Crossref: identical | Correct |
| Dimmock, Wang & Yang (2024), *MS* 70(3) 1554–1579 | Crossref: identical | Correct |
| Ang, Papanikolaou & Westerfield (2014), *MS* 60(11) 2737–2761 | Crossref: identical | Correct |
| Gredil, Griffiths & Stucke (2023), *JCF* 81, 102360 | Crossref: identical | Correct |
| Korteweg & Nagel (2016), *JF* 71(3) 1437–1470 | NBER w19347 page: identical. The abstract confirms "VC fund abnormal returns close to zero" and that the systematic payoffs resemble short index puts. | Correct |
| Jeet et al. (2026), *JPMI* 24(3) | Journal site: Vol. 24, No. 3 (Spring 2026), published 15 Jun 2026. The formulas d = log M/(G·L) and b = e^{πd}/√2 match. | Correct (it was flagged as suspicious; it exists) |
| Karatas, Klinkert & Hirsa (2021), arXiv:2108.02853 | arXiv: identical, 5 Aug 2021 | Correct |
| Giommetti & Sørensen (2021), WP, SSRN 3761243 | CBS portal: 2021 WP. Confirms "not monotonically declining in risk aversion" and the secondary-market extension. "Repeated TA-type commitments" is not stated in the abstract. | Correct |

**Erratum (2026-10-18).** The literature audit (`research/literature/04_pe_cashflows.lit.md` §2) found two references mismatched that this table marks Correct, and Crossref confirms both: (1) Luxenberg et al. is not preprint-only: it was published in *Proceedings of the Third ACM International Conference on AI in Finance (ICAIF '22)*, pp. 249–256, DOI 10.1145/3533271.3561769, with five authors (Luxenberg, Boyd, van Beek, Cao, Kochenderfer); the nine-author list is arXiv v1's, and the F17 figures checked there stand for the preprint. (2) Jeet et al. (2026) exists, but its published title is "A Crucial Enhancement to the Takahashi–Alexander Cash Flow Model" (Jeet, Stucke & Partani), *The Journal of Private Markets Investing* 24(3), 62–73, DOI 10.3905/jpmi.2026.1.010; Section 1's statement that the other 17 references have correct authors, year, venue and pages excludes these two.

The market sources were all retrieved and match their stated dates: MSCI Q2-2026, the MSCI May-2026 deck, the MSCI blog of 14 Jan 2026, Bain (23 Feb 2026), the Bain midyear release (8 Jun 2026), Jefferies (Jul 2026), Cherry Bekaert (17 Aug 2026), Rede (23 Jun 2026), Cambridge Associates 2019-Q4 and Cliffwater (Dec 2023). **Source-quality note:** the MSCI Q2-2026 PDF at msci.com still contains production notes ("TEXT UPDATED SEPT. 24", card-swap instructions with internal SharePoint links). Its numbers are internally consistent. Cite it as "MSCI, published October 2026".

---

## 5. Reasoning issues and overclaims in the design implications

### 5.1 Must-fix (would bias SELL / HOLD / REFINANCE / LEVER outputs)

**R1. Fees are double-counted (E2 against E3 and Section 2.6).**
- *Where alpha is net.* E3 defines the fused α as the "forward **net** alpha". The actual-to-date input is PME or direct alpha from LP cash flows, which are net of fees and carry; MSCI states "all returns are net of fees". Section 2.6 sets the prior for "net buyout alpha" at 0 to +2%.
- *Where fees come off again.* E2 then subtracts fees f_i (1.5–2% management fee and 20% carry, per SWY) from a drift that already contains the net α̂.
- *Effect.* The HOLD and LEVER drift is understated by roughly the fee load, about 2–4pp a year including carry in good states. That tilts every operator toward SELL.
- *Fix.* Either make α̂ gross (and convert y^U, y^A and y^F to gross through the LPA waterfall), or drop f_i from E2. Model management fees on commitments and carry as an option on profits (Metrick–Yasuda; SWY), not as a proportional drag on NAV.

**R2. The alpha runway runs on the drought clock (E2, E3, E4).**
- *Mechanism.* E2 multiplies alpha by g(a^e), where a^e is effective age, and E4 sets κ(D) = 0.6. During the current 18-quarter drought, effective age advances 2.7 years instead of 4.5, so the full-alpha window is **extended by about 1.8 years**.
- *Why that is wrong.* It credits extra value creation exactly during the extended holds that Bain links to IRR stagnation from about year 7. MSCI says these assets are carried at marks above realistic clearing prices. It also works against E6's adverse-selection drift in q.
- *Fix.* Key g(·) to calendar age or holding period, or to a separate value-creation clock that does not slow in droughts. Only the distribution schedule should run on a^e.

**R3. The liquidity shadow price is used with the wrong units (E9, executive summary item 6, the REFINANCE test).**

π_t is the dual of a cash constraint at date t: the value of one extra dollar at t. The dossier uses it in four ways that do not respect that:
- **As a rate.** The hurdle h_t = r^opp + π_t adds a level multiplier to an annual rate.
- **Against annual returns.** A sale is said to make sense when π exceeds the buyer's expected *annual* excess return. The rate-equivalent liquidity premium is the expected rate of change of the shadow value, about (π_t − E_t π_{t+1})/(1 + E_t π_{t+1}) per period. A one-off discount d should be compared with a one-off shadow value, or with the buyer's excess return multiplied by the remaining duration.
- **As an IRR rule.** "Equivalently, sell when the buyer's IRR is below the hurdle" is not equivalent to the NPV rule. (D − C) streams that include unfunded calls can have several IRRs, and π_τ varies across paths.
- **In the REFINANCE test.** The test π_t > (r_b + m) − E[collateral excess return] puts the collateral return in the wrong comparison. Borrowing versus not borrowing leaves the collateral return unchanged, apart from sweeps. It matters only for REFINANCE versus SELL.

*Fix.* Write every operator test as a path-wise NPV under one deflator multiplied by (1 + π_τ). Derive any "hurdle" from the term structure of π.

**R4. Exit pricing uses a selected statistic and is over-determined (E6 and E7).**
- *Selection.* E7 calibrates ln(P/N_{t−2}) so that P(P > N_{t−2}) ≈ 0.75, using the Bain/MSCI statistic. That statistic is **conditional on an exit having happened**: GPs sell when bids clear the mark, and the drought inventory is the population that did not clear. Applying it to unsold inventory, to drought paths and to SELL valuation overstates realisable value. The dossier's own Section 8 and MSCI's introduction both point the other way: marks on 2015–2022/23 vintages likely sit above clearing prices.
- *Over-determination.* E6 already sets D from economic NAV V. A separate lognormal on P/N_{t−2} therefore fixes exit values twice.
- *Fix.* Derive the exit uplift from the modelled mark gap G = ln N − ln V, with a selection mechanism such as an exit hazard that rises with the gap. Use the 75% only as a moment for exiting assets.

### 5.2 Should-fix

**R5. The TA bow, written as an intensity, breaks at the end of fund life (E6).**
- δ̄(a) = −ln[1 − max(Y, (a/L)^B)] is infinite at a^e = L and undefined (the log of a negative number) beyond it.
- Section 6.4 sets L at 6 for private credit, 8 for secondary funds and 12 for real estate, so the break occurs inside a 10-year projection.
- Cap the argument at 1 − ε and add an explicit terminal-liquidation or extension rule.

**R6. The calibration targets are mis-specified (Sections 4.2, 6.6 and 6.7).**
- **Not a normal curve.** The "normal" DPI-by-age curve is a single Cambridge Associates cross-section on 31-Dec-2019, near the top of a strong 2014–19 exit market. It mixes vintage and calendar effects, so it is a benign profile rather than a normal one.
- **Ages overstated.** The ages are about 0.5–1 year too high. At end-2019, vintages 2016, 2015 and 2014 were about 3.5, 4.5 and 5.5 years old, not "about 4–6". Vintage 2010 was about 9.5, but it is mapped to "age 10". A curve fitted to inflated ages is too slow.
- **"Reproduces" is generous.** The fit misses age 8 by about 19% (0.76 against 0.64).
- **Two providers mixed.** The calibration combines CA DPI curves with MSCI rates, contrary to Section 8's own advice to stay with one provider.
- **Fix.** Fit age and calendar effects jointly on MSCI vintage-by-age panels across several calendar windows. The development-triangle approach the dossier already proposes would do this.

**R7. The belief-fusion formulas are internally inconsistent (E3).**
- The "credibility form" Z·y^A + (1 − Z)[w·y^F + (1 − w)·y^U]:
  - omits the prior α_s, which the GLS posterior shrinks toward;
  - uses Z = a^e/(a^e + k) and so ignores the realisation ratio ρ, which appears in the stated variance τ_A²/(a^e·ρ);
  - uses fixed weights w and (1 − w), although with corr(e^U, e^F) = ρ_UF the GLS weights depend on ρ_UF and one of them can turn negative.
- y^A enters with a unit loading on *forward* alpha, which assumes interim performance persists fully. Buyout persistence has been weak since 2000 and interim marks are suspect, so a persistence loading below 1, estimated on ADIC's exits, is needed.
- Run the GLS form in code. Keep the credibility form only as an IC explanation derived from the same parameters.

**R8. Feeding optimiser shadow prices into the operators is underspecified (E10 to E9).**
- Duals from a linearised mean-dynamics MPC (Luxenberg's A/B form) are not state-contingent, yet E9 uses π_τ inside path-wise expectations.
- Chance constraints are non-convex. Staying within cvxpy requires a CVaR or scenario approximation.
- Duals are zero while a constraint is slack and jump when it binds.
- Large sales change the constraint itself, so they are not marginal decisions.
- The asset decisions and π therefore need a joint solution: a scenario-tree stochastic program, approximate dynamic programming, or a fixed-point loop.

**R9. The payout coverage ratio mixes risk levels (E8).**
- The numerator uses an expectation, E[NCF]; the denominator uses a P99 margin.
- The tail quantities are treated as additive, although NCF collapses in the same states in which overlay margin spikes and the tail hedge pays.
- Compute coverage path by path, as E10's chance constraint already does, and report quantiles of the path-wise ratio.

**R10. The toy programme and the headline drawn from it (executive summary item 3, Section 6.6).**
- **Run-off is built in.** Commitments of $11.2bn a year on $106bn of NAV are about 23% below replacement. At the dossier's normal rates (distributions 24% of NAV, growth 11%), holding NAV flat needs about $13.8bn of calls (about $14.5bn of commitments) a year. The toy is therefore in run-off, which inflates net cash flow.
- **The normal-regime figure does not follow from the stated rates.** At those rates, normal-regime net flow is 25.4 − 10.7 ≈ **+$14.7bn**, not "+$10–12bn". Either explain the age-mix difference or change the summary.
- **The V scenario is understated.** "Funding most of the minimum payout" undersells V: +$47bn is 177% of the $26.6bn three-year minimum and about 89% of the $53.1bn maximum.
- **Every private asset is modelled as buyout.** All $106bn uses buyout parameters, although the private book includes credit and real assets.
- **For the IC.** State the commitment-pace assumption next to the headline.

### 5.3 Minor

- **R11. Little's law (Section 3.3).** 13,509 / (353 × 4) = 9.6 years is a stock-to-flow ratio, not a mean residence time. The system is not stationary, exit counts leave out write-offs, and the comparison sets a mean against a 5.5-year median. Present it as a backlog-turnover indicator.
- **R12. Regime duration (Section 6.5).** The probability of an 18-quarter spell when p_DD = 0.88 is 0.88^17 ≈ 0.11. That is weak evidence from a single spell and does not by itself "argue for" duration dependence. The HSMM is defensible on priors, not on this data point.
- **R13. Smoothing conversion (Sections 2.5 and 7, E7).**
  - λ_q = λ_w^13 ≈ 0.52 captures the persistence of the NAV level, but not the autocorrelation of quarterly reported returns.
  - Weekly exponential smoothing at λ_w = 0.951 implies quarterly reported returns follow an ARMA(1,1) with first-order autocorrelation of about 0.66.
  - BGG's AR(2) coefficients (0.5, 0.3) imply about 0.71.
  - A quarterly AR(1) with λ_q = 0.5 therefore understates smoothing. Fit λ_q and the lag ℓ jointly to the reported-return autocorrelations.
- **R14. CV metric (Section 6.7).** MSCI's 20% is a ratio of CV contributions to mature-fund distributions, not a "share of mature-fund distributions".
- **R15. Secondary-price anchors (Section 6.5, E9, LEVER).**
  - Jefferies disclaims using its aggregate pricing for individual fund interests.
  - Its prices are quoted against lagged reference-date NAV and reflect which portfolios get sold (sweeteners added to lift price, a flight to quality).
  - The regime-B anchor (about 94%, H1-2025) comes from a period the dossier classifies as drought. Buyout pricing in the drought held at 91–94%, so regime dependence of d̄ should be estimated, not assumed.
  - "Capture the buyer's 3–5pp" assumes ADIC can earn the buyer excess return that Nadauld et al. measured for intermediary-era funds-of-funds buyers, in a 2026 market with $290bn of dedicated secondary capital. Treat it as an upper bound.
- **R16. Luxenberg's steady-state multiple.** In the example, 0.158 is the mean log return, so E[R] ≈ 1.218. Check: E[R(1 − δ)] + E[Rδ] = 0.729 + 0.490 = 1.218. The 3.685× multiple depends on that return, and the paper's problem has no payouts. Do not transfer it to ADIC.
- **R17. E1 specification.** The observables z drive the state equation and are also supposed to be fitted "as a dynamic factor model". In a DFM, observables load on X in the measurement equation. Choose one.
- **R18. Scenario set.** The executive summary asks for probabilities on five scenarios, but Section 6.6 spreads 100% over four. Say whether AI-bifurcation is an overlay or a fifth scenario. Monitor effective sample size when entropy-pooling to IC probabilities that sit far from base simulation frequencies.

---

## 6. Additional observations for the IC

- **Revision risk, quantified.**
  - Between MSCI's May-2026 deck (data to Q4-2025) and the October-2026 report, PE distribution rates for 2017–25 were revised **down** by 1–3pp.
  - Over the same revision, 2025 distribution dollars were revised **up** from $449bn to $489bn (+9%), and contributions from $450bn to $491bn. The dataset grew, and NAV denominators grew faster.
  - Rates and dollar flows can therefore move in opposite directions. Calibrate on one data vintage and record which one.
- **The "historical norm" depends on the source.**

  | Source | Norm stated | H1-2026 / latest |
  |---|---|---|
  | MSCI May-2026 deck | PE "~20% historical norm" | — |
  | MSCI Oct-2026 report | PE 9% is "about one-third of the historical average" (implies about 27%) | 9% |
  | Jefferies | LP portfolios: 25% average since 2001 | about 10% |
  | PitchBook (via Cherry Bekaert) | US: 23.4% long-run | 14.8% |

  The dossier's "roughly half of ~20%" is the mildest reading. The IC should see that 9% is 33–45% of the various norms.
- **Low-weight items not verified.** These are not in the table:
  - McKinsey's five-year rolling DPI of about 10%, and infrastructure five-year DPI falling from 40% to 13%;
  - Carta VC DPI medians, taken from ValueAddVC;
  - Hamilton Lane Cobalt covering more than 69,000 funds;
  - the "record" qualifier on McKinsey's 52%.

---

## 7. Overall reliability rating

**HIGH for the empirical content; MEDIUM for the design layer.**
- **Empirical content.** Every author-flagged number was traced to its primary document. The three corrections are attribution and precision fixes, and one citation has the wrong issue number.
- **Design layer.** Four issues must be fixed before the engine's SELL / HOLD / REFINANCE / LEVER outputs are shown to the IC:
  - R1, the fee double-count;
  - R2, the alpha runway on effective age;
  - R3, the shadow-price units;
  - R4, the selected exit statistic.
- **Calibration.** R5–R7 should be fixed before calibration work starts.

---

## Citation corrections (2026-10-18)

- **§4:** added one erratum line below the citation-check table. Luxenberg et al. (2022) is not preprint-only (ICAIF '22, pp. 249–256, DOI 10.1145/3533271.3561769), and Jeet et al. (2026) was published as "A Crucial Enhancement to the Takahashi–Alexander Cash Flow Model" (DOI 10.3905/jpmi.2026.1.010). The rest of the log is unchanged.
