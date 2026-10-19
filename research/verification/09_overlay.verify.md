# Verification log: Stream 09, Derivatives overlay (tail protection, opportunistic trading, collateral and margin liquidity)

*Dossier checked:* `research/dossiers/09_overlay.md` (prepared 2026-10-18). *Verifier:* adversarial fact-check pass. *Date:* 2026-10-18.

*Method.* Every flagged claim was checked against a primary source wherever one could be reached, plus 23 further claims I judged load-bearing or suspicious. The checks used three routes:

1. **Cboe data.** I re-downloaded the Cboe daily files the author used (VIX, VIX3M, VVIX, SKEW, SPX, PPUT, CLL, CLLZ, VXTH; last observation 2026-10-16) and recomputed every "our computation" statistic independently, including a fresh fit of the 4-state Gaussian HMM.
2. **Full-text PDFs.** I extracted and searched the full text of the source papers and reports: Harvey et al. 2019, Harvey & Liu 2015, FSB 2020, Koijen et al. "Carry", Moskowitz–Ooi–Pedersen 2012, Bailey & López de Prado 2014, Jeanne & Rancière 2006, Israelov 2019, Israelov & Nielsen 2015, Harvey et al. 2018, and the 2015 Federal Register rule text.
3. **Direct fetches.** I fetched regulator, journal and press pages directly.

The session's shared web-search quota ran out partway through. After that, all evidence came from direct fetches of named URLs.

---

## 1. Summary

- **Empirical reliability is high.**
  - 42 claims checked: **38 confirmed, 3 corrected, 0 refuted, 1 unverifiable.** Four of the confirmations rest partly on the dossier's cited secondary source (Wikipedia) and are marked C*.
  - Every Cboe-based statistic replicated to the reported precision. That covers index CAGRs, volatilities, drawdowns, crisis-window returns, VRP buckets, spot–vol betas, VIX/SKEW/VVIX levels, SPX tail quantiles, the whole HMM (state means, stationary shares, durations, 21-day matrix, current posterior), PPUT carry by state, and SKEW by state.
  - Every paper, report and regulatory citation exists, and the quoted findings match the source text.
- **Corrections (3):**
  1. **CalPERS / LongTail Alpha.** "Held to 31 Mar ... several hundred million dollars" is Bloomberg's account. The source the dossier cites (Institutional Investor) says the LongTail hedge was being *unwound* between 1 Jan and 31 Mar and paid about **$150–175m**. The figure is contested and should be reported as a range.
  2. **Spot–vol default β⁻ = −1.7 for equation 6.4A.**
     - −1.70 is correct as a statistic: it is the OLS slope (with intercept) on days when SPX fell more than 2%.
     - It is the wrong parameter for the dossier's own piecewise-linear equation, which applies β⁻ to *every* down day with no intercept.
     - An all-days piecewise fit gives **β⁻ ≈ −1.34 to −1.37 and β⁺ ≈ −0.93 to −0.95**.
     - As written, the model overstates simulated VIX jumps by 11–46% on down days, which inflates hedge payoffs and VM inflows.
  3. **Sharpe-shrinkage example (§3.5).** The example mixes sampling frequencies: SE and posterior use annual data (T = 8), while the DSR uses monthly data (T = 96). At a consistent monthly frequency the results are SE ≈ 0.39, **posterior ≈ 0.50 (not 0.42)** and DSR ≈ 0.86. The gate conclusion does not change.
- **Unverifiable (1):** AQR's 2020 critique of tail funds, sourced to press summaries. The dossier itself notes that the primary page returned 403.
- **Secondary-only parts (C*):**
  - the 2009 secondary discount of 35% (WSJ is paywalled; the 2025 Jefferies figures *were* confirmed at the primary);
  - the BoE gilt purchase and sale totals (£19.3bn / £23.1bn);
  - Universa's 2008 return and the WSJ hypothetical portfolio;
  - Harvard's 2008–09 loss.
- **Most important reasoning issues:** see §5.
  - R1: spot–vol misspecification.
  - R2: the cost-per-crisis-payoff league table uses hindsight trough dating and non-common samples. On a common 2008–2026 window, CLLZ is 0.94, not 0.49.
  - R3: the Jeanne–Rancière illustration is not tied to the dossier's own measured instrument costs. Mapped to those costs, almost every option instrument is a "do not insure" corner.
  - R5: the IM calibration target overreads the FSB.
  - R6/R7: units and liquidity double counting in the objective, the ledger and the monetization rule.
- **Overall rating: HIGH for facts. The design layer is MEDIUM until R1–R7 are fixed.** None of the issues overturns the dossier's headline conclusions. These are that puts lose money on a standalone basis, that collateral binds in crises, that the case for protection rests on liquidity and enabling channels, and that opportunistic Sharpe ratios need heavy deflation. R1 and R2, however, bias the quantitative hedge valuation *in favour of* convexity.

---

## 2. Claims table

Verdicts: **C** = confirmed; **C\*** = confirmed, but part of the claim only via the dossier's cited secondary source; **COR** = corrected; **R** = refuted; **U** = unverifiable. F-rows are the author's flagged claims; E-rows are extra claims I selected.

| # | Claim (dossier location) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| F1 | 1m ATM puts −7.4% p.a. excess, positive in 8/8 drawdowns; 10y UST +10.6% p.a. in drawdowns (+3.1% normal), effective only post-2000; short credit −3.6% p.a.; gold +9.0% p.a. in drawdowns, positive 7/8 (§1, §4.1) | C | All verbatim in the paper. Also confirmed: short credit +128% in 2007–09; CDX cost <0.1% p.a.; "historical rarity" quote. | https://people.duke.edu/~charvey/Research/Published_Papers/P140_The_best_of.pdf |
| F2 | 1m/3m TSMOM good in crises, 12m negative in the 3 most recent drawdowns; equity cap costs 1.1% (3m) / 0.9% (12m) p.a.; trading costs 0.6–0.8% p.a. | C | Paper: the 0.6–0.8% cost is for the **three-month** strategy only. The exec summary applies it to "1–3-month trend" (see R12). | same as F1 |
| F3 | PPUT 7.97% p.a. (30 Jun 1986–16 Oct 2026) vs SPX price 8.85%; 2.3–3.3 pp behind SPX TR; COVID-window excess ≈ +22 pp | C | Replicated: PPUT 7.973%, SPX 8.855%. Geometric gap 2.33 / 2.83 / 3.34 pp at 1.5 / 2.0 / 2.5% dividend yield. COVID excess +21.95 pp. | https://cdn.cboe.com/api/global/us_indices/daily_prices/PPUT_History.csv |
| F4 | VIX − next-21d realized vol: mean 4.10, positive 85.9% of days, 2.8 (VIX<15) to 6.5 (VIX 30–40); spot–vol −1.16 per 1%, −1.70 on SPX<−2% days | C (as statistics) | Replicated with RMS realized vol: 4.10; 85.88%; buckets 2.82 / 4.13 / 4.87 / 6.52 / 5.78; p5 −4.87. Spot–vol with **log** returns: −1.155, −1.696, up days −1.021. With simple returns: −1.153 / −1.787 / −1.006. **The −1.70 is misused as an equation parameter (see E22 and R1).** | https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv |
| F5 | VXTH +27.6% vs SPX −33.9% (19 Feb–23 Mar 2020); −29.2% vs −25.4% (3 Jan–12 Oct 2022) | C | Replicated: +27.57 / −33.92; −29.24 / −25.43. | https://cdn.cboe.com/api/global/us_indices/daily_prices/VXTH_History.csv |
| F6 | Puts reduce drawdowns only with no VRP and drawdown coinciding with the holding period; divesting to equal expected return is more efficient (Israelov, JAI Winter 2019) | C | Full sentence verified. The paper sizes the divested portfolio (36.5% SPX / 63.5% cash) to the *same compounded return* as PPUT, and an ex-ante version also wins. The paper also finds options "shine" only for one-day crashes. | https://www.aqr.com/Insights/Research/White-Papers/Pathetic-Protection-The-Elusive-Benefits-of-Protective-Puts |
| F7 | The VRP, not the VIX level, determines whether protection is cheap; protection is expensive even in calm markets (Israelov & Nielsen 2015) | C | The PDF confirms Israelov **and** Nielsen, JPM 41(4), Summer 2015. The CFA Digest confirms the VRP is "consistently positive" across VIX deciles. | https://www.aqr.com/Insights/Research/Journal-Article/Still-Not-Cheap-Portfolio-Protection-in-Calm-Markets ; https://rpc.cfainstitute.org/research/cfa-digest/2015/12/still-not-cheap-portfolio-protection-in-calm-markets-digest-summary |
| F8 | March 2020: IM at some CCPs rose more than 100% vs the prior quarter; most of the increase came 6–13 Mar; daily IM increments "notably smaller" than same-day VM; APC tools dampened IM "only for a short time period" | C | All verbatim (FSB 2020, Box 4.2 and p.25). The exec summary's "dwarfed" overstates "notably smaller" (R12). | https://www.fsb.org/wp-content/uploads/P171120-2.pdf |
| F9 | 30y gilt yields up more than 270 bp from 1 Aug to the 14 Oct 2022 peak, briefly above 5%, more than twice the March 2020 move; FPC requires resilience to a yield shock of "around 250 basis points, at a minimum" | C | The 270 bp / 5% / "more than twice" text is in **BoE FSR Dec 2022**, not the FPC Mar 2023 page cited in the flagged list. The 250 bp text is in FPC Mar 2023. The staff paper splits 250 bp into ~170 bp systemic and ~80 bp baseline. | https://www.bankofengland.co.uk/financial-stability-report/2022/december-2022 ; https://www.bankofengland.co.uk/financial-policy-summary-and-record/2023/march-2023 |
| F10 | LCR40.56 HLBA = "largest absolute net 30-day collateral flow realised during the preceding 24 months"; LCR40.52 = 20% of posted non-Level-1 collateral | C | Also confirmed: 40.49 (100% net derivative outflows), 40.51 (3-notch downgrade), 40.53–55 (100%). | https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30 |
| F11 | "Sovereign entity" (central government, or its agency, department, ministry or central bank) is excluded from "financial end user"; MSE $8bn; IM threshold $50m | C | Verbatim. **Nuance omitted (R14):** the rule preamble says the term "includes only central governments" and "the existence of a government guarantee does not in and of itself exclude the entity". | https://www.law.cornell.edu/cfr/text/12/237.2 ; https://www.govinfo.gov/content/pkg/FR-2015-11-30/html/2015-28671.htm |
| F12 | Schedule IM: equity / commodity / other 15%, FX 6%, IR 1/2/4%, credit 2/5/10%; IM = (0.4 + 0.6·NGR)·gross; haircuts: government 0.5/2/4%, S&P 500 15%, gold 15% (plus S&P 1500 25%, FX mismatch +8%) | C | Appendix A and B tables verified. The rule buckets by **duration**, not maturity. The 8% FX add-on sits in §__.6(c), not Appendix B. | https://www.govinfo.gov/content/pkg/FR-2015-11-30/html/2015-28671.htm |
| F13 | Investors forgo about 2% of wealth to hedge once-a-decade illiquidity crises; uncertain-duration illiquidity raises effective risk aversion (Ang, Papanikolaou & Westerfield) | C | Abstract verbatim. | https://www.nber.org/papers/w19436 |
| F14 | Secondary discount 35% in 2009 (7% in 2013); 2025 LP portfolios at 87% of NAV (buyout 92%, venture/growth 78%) | C* | **2025 figures confirmed at the primary** (Jefferies, 10 Feb 2026: "87 percent of NAV"; buyout 92%; venture and growth 78%). The 2009 35% and 2013 7% are confirmed only via Wikipedia citing WSJ (24 Apr 2014, paywalled). 2009's 35% is an *annual average*, not the trough. | https://www.jefferies.com/insights/the-big-picture/2025-global-secondary-market-review-another-record-breaking-year/ ; https://en.wikipedia.org/wiki/Private_equity_secondary_market |
| F15 | Carry Sharpe 0.6–0.9 within asset classes, 1.49 diversified; diversified TSMOM Sharpe above 1, about 2.5× equity | C | The Carry paper says "0.6 to 0.9" and its table shows SR 1.49. **The TSMOM half comes from Moskowitz–Ooi–Pedersen (2012)**, not Carry.pdf; that paper also confirms SR 1.1 for 1966–85 and large profits in Oct–Dec 2008. | https://pages.stern.nyu.edu/~lpederse/papers/Carry.pdf ; https://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf |
| F16 | Harvey–Liu haircuts are non-linear: "almost always more than ... 50%" when SR < 0.4; "at most 25%" when SR > 1.0 | C | Verbatim (JPM Fall 2015). These are conditional on the paper's exhibit settings, which are calibrated to its own sample length and number of tests. | https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF |
| F17 | J–R: p = 1 + δ/(π(1−δ−π)); ρ ≈ λ + γ − (1 − p^(−1/σ)); benchmark π = 0.1, δ = 1.5%, σ = 2 gives 10.1% of GDP | C | Both formulas are in the paper (p-definition, equations 16–17). The 10.1% comes from the **exact** equation 16 (r = 5%, g = 3.3%). The approximate equation 17 gives 9.97%. [2026-10-18: the published version, *Economic Journal* 121(555), 905–930 (2011), reports a benchmark of 9.1% of output per a citing paper (Mihailov & Nasir 2022) [unverified: EJ text not accessed]. The dossier now gives both figures.] | https://www.imf.org/external/pubs/ft/wp/2006/wp06229.pdf |
| F18 | 16 Oct 2026: SKEW 168.6 vs 1990–2026 mean 123.3 (record 183.1 on 18 Feb 2025); VIX 19.99; HMM 0.64 / 0.36 on S1/S2; SPX 7,659, 2% below its 6 Oct 2026 record | C | Replicated: SKEW 168.59, mean 123.26, max 183.12 on 2025-02-18. VIX 19.99 (high 22.31). HMM posterior S1 0.638 / S2 0.361. SPX 7,659.44 vs record 7,818.93 on 2026-10-06 (−2.04%). | https://cdn.cboe.com/api/global/us_indices/daily_prices/SKEW_History.csv |
| F19 | CalPERS had Universa unwind by Jan 2020 (cost, scalability, "better alternatives"); missed about $1bn; a LongTail hedge **held to 31 Mar earned several hundred million** | COR | The Universa part is confirmed (notice Oct 2019, unwound by Jan 2020, missed ">$1 billion"). **LongTail:** II (Segal, 17 Apr 2020), the cited source, says the hedge "was in the unwinding process between January 1 and March 31" with a final distribution of "around $150 million to $175 million". Bloomberg (Schatzker, 13 Apr 2020) says it was not terminated until 31 Mar and earned "several hundred million". Report as contested, $150–175m to "several hundred million". | https://www.institutionalinvestor.com/article/b1l7lrcp6tnwlm/CalPERS-Abandoned-Tail-Hedge-Starts-a-War-of-Words ; https://www.financial-planning.com/articles/calpers-missed-a-1-billion-payday-by-scrapping-market-hedge-ahead-of-the-coronavirus-outbreak |
| E1 | 14% of days since 1985 are drawdown days; an equal-weight equity-plus-put mix is negative in each crisis; quality L/S costs 1.0–2.0% p.a.; 5–10% OTM puts "no longer consistently positive" (OTC broker data, 1996–2018) | C | All in Harvey et al. 2019, including the appendix. | P140 PDF (as F1) |
| E2 | §4.2 table: CAGR, vol, max DD and window returns for SPX, PPUT, CLLZ, CLL (from 26 Aug 2008) and VXTH (from 31 Mar 2006) | C | Every cell replicated within rounding. Example: CLLZ 8.108% / 14.55% / −47.22%; CLL 6.874% vs SPX 10.407%; Oct–Nov 2008 is 30 Sep–20 Nov. | Cboe files (pattern as F3) |
| E3 | §4.3 mean crisis-window excess PPUT +9.6, CLLZ +5.5, CLL +9.1, VXTH +13.7; costs per $ 0.29 / 0.49 / 0.58 / 0.09; VXTH 0.30 ex-COVID | C | Reproduced exactly using SPX peak-to-trough windows (9.60 / 5.49 / 9.04 / 13.65; VXTH ex-COVID mean 4.12, giving 0.30). **The method is fragile; see R2.** | Cboe files |
| E4 | §4.4 HMM: n = 9,262; state means 12.5 / 16.3 / 21.1 / 30.7; stationary shares 27.6 / 27.5 / 26.2 / 18.6%; durations 41 / 19 / 20 / 35 days; 21-day matrix; SPX vol 8.6 / 12.2 / 17.0 / 31.7; PPUT carry −1.8 / −3.8 / −3.2 / −5.1; SKEW 124.8 / 126.1 / 121.4 / 119.5; S3 episodes | C | Replicated on VIX∩SPX dates. SPX vol and p1 by state match only when returns are taken the day *after* the Viterbi state (next-day convention). PPUT carry in S2 comes out at −3.31. | Cboe files |
| E5 | VIX mean 19.42, median 17.56, p90 / p95 / p99 28.50 / 32.88 / 46.70, max 82.69 (16 Mar 2020); >30 on 7.9% of days, >40 on 2.2%; 5 Feb 2018 17.31 → 37.32 (+115.6%); 5 Aug 2024 intraday 65.73, close 38.57; 8 Apr 2025 close 52.33; 2026 max close 31.05 (27 Mar); VIX3M/VIX median 1.13, below 1 on 7.5% of days, 0.90 at VIX ≥ 40; VVIX mean 93.9, max 207.6, latest 109.9 | C | All identical. Note that VIX3M statistics cover only 18 Sep 2009 onward, which is the start of the file. | Cboe files |
| E6 | SPX tail table: 1d / 10d / 21d p1, p0.1 and worst (−20.47% on 19 Oct 1987; −31.47%; −32.97% on 23 Mar 2020); 3m p2.5 −13.7%; 1y p2.5 −23.3%, p1 −36.2%; −34% in 23 trading days in 2020 | C | Identical. | Cboe SPX file |
| E7 | Forward 12m SPX return by VIX at entry: <15 11.1%, 30–40 18.1%, ≥40 33.0% | C (values) | Values exact (11.06 / 18.04 / 32.95), but the table **omits** 15–20 (10.26%) and 20–30 (**5.86%**). The pattern is not monotone (R9). | Cboe files |
| E8 | Foreign holders sold almost $300bn of Treasuries in March 2020 | C | Verbatim; about one-fifth were official sales. | FSB 2020 PDF |
| E9 | BoE bought £19.3bn of gilts and sold them for £23.1bn; FSR quotes "vicious spiral" and buffers "too low and less usable in practice than expected" | C* | The quotes are verbatim in FSR Dec 2022 (primary). The £ figures are confirmed only via Wikipedia (sold over the following 16 months; profit £3.8bn). I found no £ total in the first 300k characters of the FSR, and Bank Underground gives only "0.9% of GDP". | https://en.wikipedia.org/wiki/September_2022_United_Kingdom_mini-budget ; FSR (F9) |
| E10 | Clarus: average peak VM per CCP $2.5bn, 1.6× the previous peak (Jun 2016), 2.3× the prior quarter; ~$150bn across 59 clearing services "not the maximum margin call" | C | Verbatim (C. Barnes, 15 Jul 2020). | https://www.clarusft.com/margin-calls-during-covid-19/ |
| E11 | BCBS–CPMI–IOSCO 2022: VM "significantly higher than in February"; uncleared IM "relatively stable"; FSB Dec 2024: eight recommendations; BCBS–IOSCO Jan 2025: eight recommendations | C | All confirmed (d537, 29 Sep 2022; FSB, 10 Dec 2024). | https://www.bis.org/bcbs/publ/d537.htm ; https://www.fsb.org/2024/12/liquidity-preparedness-for-margin-and-collateral-calls-final-report/ |
| E12 | FSB 2023: oil up >30%, European gas and industrial metals doubled, margin spike especially in Europe, LME nickel the exception | C | Verbatim (20 Feb 2023). | https://www.fsb.org/2023/02/the-financial-stability-aspects-of-commodities-markets/ |
| E13 | Universa +3,612% on invested capital (Mar 2020); >100% in 2008; WSJ 3.3% Universa / 96.7% SPX portfolio at 12.3% CAGR for the 10 years to Feb 2018 | C* | The 3,612% is also in the Bloomberg piece republished by Financial Planning. The 2008 and WSJ-hypothetical figures are confirmed only via Wikipedia, which says "the rest" in S&P, not 96.7%. | https://en.wikipedia.org/wiki/Universa_Investments |
| E14 | PPUT had 18 monthly declines of ≥6% vs 35 for the S&P 500 (Cboe 2021) | C (as attributed) | Verbatim in Cboe (15 Jul 2021). My calendar-month replication (SPX price, Jul 1986–Jun 2021) gives PPUT 18 but **SPX 32**. Cboe's month definition probably differs. | https://www.cboe.com/insights/posts/benchmark-indices-series-hedging-downside-exposure-with-pput-cll-and-cllz-indices |
| E15 | AQR 2020 critique: crash-month winners lose most of their allocated capital in good times | U | Press summary only. The Advisor Perspectives primary returned 403 to the author, and the Universa Wikipedia page does not mention it. | https://www.advisorperspectives.com/articles/2020/05/06/an-aqr-warning-and-a-3-612-return-fire-up-the-black-swan-debate |
| E16 | Volatility scaling raises Sharpe for risk assets only but cuts tails and vol-of-vol across all assets (Harvey et al. 2018) | C | Verbatim. JPM 45(1), 14–33, Fall 2018. | https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf |
| E17 | ISDA SIMM infohub lists v2.6 (Sep 2023) and semiannual calibration from 2025 | C | v2.6 dated 15 Sep 2023; "move to semiannual calibration from 2025". | https://www.isda.org/isda-solutions-infohub/isda-simm/ |
| E18 | Harvard endowment fell about $8bn (~22%) amid a "cash squeeze" | C* | Confirmed only via Wikipedia, citing NYT (20 Feb 2009); primary not fetched. | https://en.wikipedia.org/wiki/Harvard_Management_Company |
| E19 | Sepp & Lucic (2026): trend-system skewness positive at every horizon under white noise | C | Abstract verbatim (arXiv v1, 21 Jul 2026). | https://arxiv.org/abs/2607.19497 |
| E20 | Hurst, Ooi & Pedersen (2017) extend trend to 1880 and flag post-2008 correlations and AUM | C | Confirmed on the AQR page. | https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing |
| E21 | NZ Super uses derivatives to complete the portfolio and rebalance, holds a collateral pool, and treats closing positions as an immediate cash source | C | Verbatim on the derivatives page. Tilting is described on the separate tilting page the dossier also cites. | https://www.nzsuperfund.nz/how-we-invest/actual-portfolio/how-we-add-value/derivatives/ |
| E22 | §6.7 default: spot–vol β⁻ = −1.7, β⁺ = −1.0 for equation 6.4A ("Cboe data") | COR | For the dossier's own functional form, β⁻·min(100r, 0) + β⁺·max(100r, 0) estimated on all days, the fit gives **β⁻ = −1.34, β⁺ = −0.95** (log returns) or **−1.37 / −0.93** (simple). −1.70 is the slope only *within* SPX < −2% days and carries a negative intercept. | Cboe files (R1) |
| E23 | §3.5 example: SR 1.0 over 8 years (skew −0.5, kurtosis 5) gives SE ≈ 0.56 and posterior ≈ 0.42; DSR ≈ 0.86 (N = 50, dispersion 0.25) | COR | Internally inconsistent frequency. **Monthly (T = 96):** SE 0.39, posterior **0.50**, DSR 0.86. **Annual (T = 8):** SE 0.56, posterior 0.42, DSR **0.77**. The DSR paper uses non-annualized SR with T observations. | https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf |

**Tally (42 rows):** confirmed 38 (F1–F18, E1–E14, E16–E21; of these, F14, E9, E13 and E18 are C*); corrected 3 (F19, E22, E23); refuted 0; unverifiable 1 (E15).

---

## 3. Replication of the "our computation" figures

The scripts and outputs are in the scratchpad at `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\v09_overlay_verify\scripts\`:

- `verify_cboe.py`
- `hmm_check.py`
- `hmm_state_stats.py`
- `spotvol_variants.py`
- `crisis_windows.py`
- `common_window.py`
- `check_formulas.py`

| Statistic | Dossier | Replicated |
|---|---|---|
| PPUT / SPX price CAGR, 30 Jun 1986–16 Oct 2026 | 7.97% / 8.85% | 7.973% / 8.855% |
| PPUT vol / max DD | 13.5% / −42.0% | 13.50% / −41.96% |
| VXTH / SPX CAGR from 31 Mar 2006 | 9.85% / 9.04% | 9.854% / 9.037% |
| COVID window: SPX, PPUT, CLLZ, CLL, VXTH | −33.9, −11.8, −30.9, −14.9, +27.6 | −33.92, −11.79, −30.91, −14.86, +27.57 |
| VRP mean / % positive / p5 | 4.10 / 85.9% / −4.9 | 4.10 / 85.88% / −4.87 |
| Spot–vol: all days / SPX < −2% / up days | −1.16 / −1.70 / −1.01 | −1.155 / −1.696 / −1.021 (log returns) |
| Piecewise all-days β⁻ / β⁺ (the equation 6.4A form) | used −1.7 / −1.0 | **−1.34 / −0.95** (log); −1.37 / −0.93 (simple) |
| Mean ΔVIX on SPX days in [−2.5, −2) / [−3.5, −2.5) / [−5, −3.5) / < −5% | implied by −1.7: 3.81 / 4.97 / 7.03 / 11.76 | actual **2.61 / 3.95 / 6.34 / 10.40** |
| HMM 21-day diagonal | .664 / .442 / .468 / .605 | .664 / .443 / .468 / .605 |
| HMM posterior on 16 Oct 2026 | S1 .635 / S2 .364 | S1 .638 / S2 .361 |
| PPUT carry by entry state | −1.8 / −3.8 / −3.2 / −5.1 | −1.81 / −3.81 / −3.31 / −5.13 |
| Forward 12m SPX by VIX: <15 / 15–20 / 20–30 / 30–40 / ≥40 | 11.1 / – / – / 18.1 / 33.0 | 11.06 / **10.26** / **5.86** / 18.04 / 32.95 |
| Cost per crisis $ on a **common** 2008–2026 window (5 windows): PPUT / CLLZ / CLL / VXTH | 0.29 / 0.49 / 0.58 / 0.09 (own samples) | 0.28 / **0.94** / 0.59 / 0.07; ex-COVID: 0.44 / 0.86 / 0.81 / 0.42 |

---

## 4. Citation check (25 references checked; none hallucinated)

| Reference as cited | Exists | Authors / year / title / venue correct? | Note |
|---|---|---|---|
| Harvey, Hoyle, Rattray, Sargaison, Taylor, Van Hemert (2019), JPM 45(5) | Yes | Yes (PDF: JPM, July 2019) | – |
| Israelov (2019), "Pathetic Protection", JAI Winter 2019 | Yes | Yes | AQR page dated 31 Dec 2018 |
| Israelov & Nielsen (2015), "Still Not Cheap", JPM | Yes | Yes | Add vol 41(4), Summer 2015. The AQR web page lists only Israelov; the PDF lists both. |
| Ang, Papanikolaou & Westerfield (2014), Management Science 60(11) | Yes | Authors and abstract verified (NBER w19436, Sep 2013) | Journal pages not fetched |
| Jeanne & Rancière (2006), IMF WP/06/229 | Yes | Yes (Oct 2006; exact title verified) | – |
| Koijen, Moskowitz, Pedersen & Vrugt, "Carry", JFE / NBER w19325 | Yes | Yes | No year or volume given; the published version is JFE 2018 (not fetched) |
| Moskowitz, Ooi & Pedersen (2012), JFE 104, 228–250 | Yes | Yes (PDF header) | – |
| Harvey & Liu (2015), "Backtesting", JPM Fall 2015 | Yes | Yes | – |
| Bailey & López de Prado (2014), "The Deflated Sharpe Ratio", JPM | Yes | Yes; formulas match | – |
| FSB (2020), *Holistic Review of the March Market Turmoil*, 17 Nov 2020 | Yes | Yes | – |
| BoE FSR Dec 2022; FPC record Mar 2023 | Yes | Yes | The 270 bp text is in the FSR, not the FPC page (see F9) |
| BCBS–CPMI–IOSCO (2022), *Review of margining practices* (d537) | Yes | Yes (29 Sep 2022) | – |
| FSB (2024) margin and collateral final report; FSB (2023) commodities | Yes | Yes (10 Dec 2024; 20 Feb 2023) | – |
| Dimmock, Wang & Yang (2024), Management Science 70(3), 1554–1579 | Yes | Yes (NBER published-version note) | – |
| Hurst, Ooi & Pedersen (2017), JPM Fall | Yes | Yes | – |
| Harvey et al. (2018), "The Impact of Volatility Targeting", JPM Fall | Yes | Yes (45(1), 14–33) | – |
| Sepp & Lucic (2026), arXiv:2607.19497 | Yes | Yes (21 Jul 2026) | – |
| 12 CFR 237.2; FR 2015-28671; Basel LCR40 | Yes | Yes | – |
| Barnes (2020), Clarus; Segal (2020), II; Schatzker (2020), Bloomberg via Financial Planning; Cboe (2021) | Yes | Yes | The II article does not support "several hundred million" (F19) |

**Citation problems found:**

1. The flagged-claims list sources the TSMOM statistics to Carry.pdf. They come from Moskowitz–Ooi–Pedersen (2012). The dossier body (§4.7) cites this correctly.
2. The 270 bp / "more than twice" gilt facts are attributed to the FPC Mar 2023 page. They are in BoE FSR Dec 2022.
3. The LongTail "several hundred million" is attributed to Institutional Investor. II says $150–175m; the phrase is Bloomberg's.
4. Minor: Israelov & Nielsen and Koijen et al. lack volume and issue details. [Resolved 2026-10-18: dossier refs 3 and 7 now give *JPM* 41(4), 108–120 and *JFE* 127(2), 197–225 (2018), confirmed via Crossref.]

---

## 5. Reasoning issues and overclaims in the design implications

**R1 (High). Spot–vol coupling misspecified (§2.4, §6.4A, §6.7, §6.8).**
- Equation 6.4A applies β⁻ = −1.7 to *every* down move with no intercept.
- −1.70 is the OLS slope estimated only on SPX < −2% days. That regression has a negative intercept; the ratio of means is −1.32.
- Fitting the dossier's own piecewise form on all days gives β⁻ ≈ −1.34 (log) or −1.37 (simple) and β⁺ ≈ −0.95 / −0.93. On 0 to −2% days the slope is ≈ −1.12.
- With −1.7, simulated ΔVIX is overstated by about 46% on −2 to −2.5% days, 26% on −2.5 to −3.5% days, and 11–13% on larger falls.
- This inflates vega P&L on puts and VIX calls, OTC VM inflows in sell-offs, and therefore the "liquidity value" of hedges. It biases the framework *toward* convexity.
- **Fix:** re-estimate on all days with a convex or threshold term that carries its own intercept, and validate conditional ΔVIX by return bucket as a calibration target.

**R2 (Medium–High). The cost-per-crisis-payoff league table (§4.3, exec summary 4, IC artifact 6.10-2) is fragile.**
1. Windows are SPX peak-to-trough dates chosen with hindsight. Payoffs are therefore measured at the exact trough, which no rules-based monetization policy (§3.3) can capture.
2. The indices are measured over different samples, with crisis frequencies of 0.20/yr (PPUT, CLLZ) against 0.28–0.29/yr (CLL, VXTH), and the "annual gap" nets these different frequencies of payoff.
   - On a common 26 Aug 2008–16 Oct 2026 window (five common crisis windows), c is PPUT 0.28, **CLLZ 0.94 (vs 0.49)**, CLL 0.59, VXTH 0.07.
   - Ex-COVID, PPUT and VXTH are both ≈ 0.4.
- **Fix:** report common-window, ex-COVID and rule-based (non-hindsight) monetization variants, together with the per-window distribution.
- The §2.2 worked example also mixes an empirical c, which embeds about 0.2 crises a year, with π = 10%.

**R3 (Medium). The Jeanne–Rancière lesson is not connected to the dossier's own costs (§2.3 vs §4.3).**
- By the dossier's own mapping (δ = carry per unit of crisis liquidity), the measured costs give corner solutions ("do not insure") at π = 0.10 and λ + γ = 15%:
  - PPUT (0.29), CLLZ (0.49) and CLL (0.58) are corners at σ = 2, 5 and even 10.
  - VXTH (0.09) is a corner at σ = 2, gives ρ ≈ 1.1% NAV at σ = 5, and ≈ 7.8% at σ = 10.
- The illustration's δ = 1.5–5% values correspond to cash- or T-bill-like buffers, not options.
- The IC should be told that, on J–R logic alone, cash buffers dominate option insurance. Options must therefore be justified by the non-J–R channels: enabling, rebalancing, and gap or decision-latency protection.

**R4 (Medium). The Sharpe example mixes frequencies (§3.5).** See E23. Skew, kurtosis, SR, T and DSR must all be computed at one sampling frequency. The default Sharpe prior of 0.3 / 0.25 and the shrinkage template will be copied, so this matters.

**R5 (Medium). The IM calibration target overreads the FSB (§6.8).**
- The dossier's target is "a >100% IM jump within ~1 week of an S3 shift".
- The FSB's evidence is narrower: >100% versus the *previous quarter* at *some* CCPs, with "substantial variation", and most of the increase in 6–13 March.
- That describes a cross-CCP tail outcome over a quarter. It should be a stress quantile in the scenario set, not a central calibration target. Calibrate central IM by product and CCP from margin histories.

**R6 (Medium). Units in the objective and recourse LP (§6.4E, §6.6, §6.7).**
- Π_D is defined as "1.0 per $" (§6.7) and used as a per-$ recourse cost (§6.4E), but §6.6 multiplies it by E[# shortfalls], which is a count.
- The objective adds a probability to $-denominated recourse costs without a weight.
- The c_k terms mix per-annum spreads (facility draws) with one-off losses (d/(1−d)), so the LP dual λ mixes units.
- The single-period LP also understates intertemporal shadow prices.
- **Fix:** express each c_k as PV per $ raised, give each objective term explicit units and a weight, and fix one meaning for Π_D.

**R7 (Medium). Liquidity double counting and inconsistency (§3.3, §6.4B, §6.4E).**
- The ledger adds ΔR_t at 100%, while §6.4B recognizes only φ^OTC = 0.7.
- VM appears only as an outflow, but it should be signed across all books, including synthetic beta, the opportunistic book and IM returns.
- The monetization rule adds λ_t·V_{j,t} even though, under a CSA, most of V has already arrived as VM collateral. Only the incremental usable liquidity should count, i.e. roughly V(1−ba) minus the collateral already recognized.

**R8 (Low–Medium). The IV surface is flat in tenor beyond 3 months (§3.2 Option A).** The tenor factor equals ρ_s for all τ ≥ 3m, yet the default ladder is 3/6/12m weighted to 6m, so the core hedge legs are priced at 3-month vol. Anchor longer tenors to Cboe VIX6M and VIX1Y, or to fitted term structures.

**R9 (Low–Medium). Forward returns by VIX are reported selectively (§4.5).** The table omits the 15–20 (10.3%) and 20–30 (5.9%) buckets. The relationship is not monotone and rests on overlapping windows and two episodes (2008–09, 2020). It does not support a quantified "rebalancing value".

**R10 (Low). The valuation identity is notationally inconsistent (§1 vs §2.2).**
- If m is the market SDF, E[mX] − P0 ≡ 0, so the term cannot be "VRP < 0".
- If m is ADIC's own marginal utility, the sign of that term is not fixed.
- The exec summary instead uses E^P[(1+λ)X] ≥ P0(1+r).
- Define carry once, as E^P[X]/(1+r) − P0.

**R11 (Low). The worked-example sensitivity (§2.2) assumes enabling value scales linearly with payoff.** If enabling value is held fixed, the total is ≈ 0.30%, not 0.45%.

**R12 (Low). Overstatements.**
- "Same-day VM calls dwarfed the incremental IM demand": the FSB says "notably smaller".
- The 0.6–0.8% trading cost was estimated for 3-month TSMOM and is not evidence for 1-month trend.
- Moskowitz–Ooi–Pedersen also document sharp TSMOM losses when crises end (Mar–May 2009). Trend reversal should be added to the defensive-stack stress set.

**R13 (Low). Look-ahead in the HMM evidence (§2.4, §3.3).**
- The calm-versus-stress carry contrast (−1.8% vs −5.1%) uses full-sample Viterbi labels.
- It is offered as motivation for regime timing, yet the dossier itself requires filtered probabilities for decisions.
- Re-estimate the contrast with filtered states before citing it.

**R14 (Low). The UMR scope analysis is incomplete (§2.5, §9).**
- The US rule's "sovereign entity" covers only central governments and their agencies, departments, ministries and central banks.
- Sub-national government entities are not excluded, and a government guarantee alone does not qualify.
- Independent amounts can be required by contract regardless of status.
- ADIC's legal analysis should test against these points.

**R15 (Low). C2 mixes horizons.** It combines a 30-day HLBA, 10-day 99% VM and 3-month flows, and takes max(HLBA, VM + ΔIM) where Basel treats HLBA as an *additive* outflow. Define one horizon, and treat HLBA as additive or justify the max.

**R16 (Low). VIX − RV overstates the ATM-put VRP.** VIX prices the whole strike strip, and the dossier's own c_ATM = 0.90 implies ATM IV ≈ 0.9·VIX. Present the 4.1-point figure as a variance-swap-style VRP, not a put cost.

---

## 6. Overall reliability rating

**HIGH for empirical content. The design layer is MEDIUM until R1–R7 are addressed.**

The factual base is unusually strong:

- Every number derived from Cboe data replicated, including the HMM.
- Every flagged literature and regulatory claim matched its primary text, with two exceptions: the LongTail figure, and the 2009 secondary discount, which could be confirmed only via its cited secondary source.
- Citation errors are limited to source locations, not invented sources.

The weaknesses are in the build specification:

- The spot–vol parameterization (R1) and the hindsight-based cost metric (R2) both make convexity look better than it is.
- The J–R illustration omits that its own cost data imply corner solutions (R3).
- Several unit and double-counting errors in the ledger and objective (R6, R7) would propagate directly into the simulator and the reported λ.

Correct these before the Overlay Engine's outputs reach the IC.

---

## Citation corrections (2026-10-18)

- §2 F17 (Jeanne & Rancière): note added that the published *Economic Journal* (2011) version reports a 9.1% benchmark (per Mihailov & Nasir 2022; unverified in the EJ text). The working-paper verdict (10.1%, confirmed) stands.
- §4 citation problem 4 (Israelov & Nielsen; Koijen et al.): marked resolved; the dossier references now carry Crossref-confirmed volume, issue, pages and DOI.
- No erratum: literature synthesis §2.4 item 7 flags no claim that this log accepted wrongly. Lo (2002), Moreira & Muir (2017) and Kaminski & Lo (2014), whose use the audit corrected, were outside this log's checks; the dossier itself is corrected.
