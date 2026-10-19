# G4 Co-investment dossier: verification log

- **Dossier checked:** `research/groups/dossiers/G4_coinvest.md` (as of 2026-10-18). The dossier was not edited.
- **Verified:** 2026-10-18, adversarial fact-check pass.
- **Method:**
  - Primary PDFs were downloaded and their text extracted locally with pypdf: the BJS accepted manuscript (ORA), FIL (NBER w19299), Kaplan-Strömberg (w14207), GKM (w21133), LMSZ (w24941), Bhardwaj-Gupta-Howell (w33435), Lopez-de-Silanes et al. (MPRA 28487), the BJSt manuscript (ORA), Lazard, Evercore, Jefferies, ILPA and Proskauer.
  - Web pages (Bain, PR Newswire, Law Gazette, Mondaq, Capstone, ABF Journal, SEC, IFR, Hamilton Lane, Investment Officer) were read directly.
  - Journal metadata was cross-checked on RePEc, Harvard DASH, AEA and Consensus search.
  - Model claims were checked against `G4_coinvest_calcs.py` and its results JSON, plus an independent re-run of the §6.5 decision examples (§5 below).
- **Verdict rule:** a claim is "unverifiable" unless a source was found. No benefit of the doubt was given.

---

## 1. Summary

- **Claims checked: 31.** Confirmed 26, corrected 4, refuted 0, unverifiable 1.
- **The evidence base is accurate.** Every academic number checked matches the source text or tables:
  - BJS Tables 4, 7 and 8 and their probit coefficients;
  - FIL Table II and its text;
  - Kaplan-Strömberg Table 2;
  - GKM's survey figures;
  - LPG, LMSZ and BJSt.

  The 2026 industry figures (Bain, Lazard, Evercore, Jefferies, Proskauer, ILPA, Sidley, Torys, Capstone) also match.
- **Four corrections, all minor or moderate:**
  1. The BJS portfolio-size result is misstated. Net of fees, VC co-investment portfolios never beat funds on a median basis. Under 0/20 terms, buyouts need about 30 deals, not 10.
  2. Torys' "~20%" is the share of tracked deals that *allow* broken-deal charging, not the share of deals that *incur* broken-deal costs.
  3. The 2021-vs-2017 cohort exit statistic comes from PitchBook LCD, not Bain.
  4. "Co-investors escaped $338m" overstates the KKR case. $338m was KKR's total broken-deal spend; the share misallocated away from co-investors was more than $17m.
- **The material problems are in the decision layer (§6.5) and the executive summary, not in the sourced facts:**
  - **SELL.** The worked example contradicts the dossier's own buyer-return model, which implies bids of 56–79% of NAV for that asset rather than 88–95%.
  - **REFI.** The breach probability is measured only at exit. With quarterly tests it is about 50% (normal) and 63% (drought), against the 29% and 37% reported.
  - **LEVER.** The executive summary compares the wrong pair of wipe-out probabilities.
  - **Recaps.** The Bhardwaj et al. effect is applied as a ×2.4 hazard multiplier, which matches neither of the paper's estimates.
  - **CV election.** It is modelled as a control ADIC can exercise every quarter, but only the GP can trigger it.
  - **Jefferies.** Its remark about syndicate capital on deals under $750m is reused as a drought stress parameter, which the source does not support.
- **Overall reliability: MEDIUM.** It is high for the sourced facts. It is medium to low for the SELL, REFI and LEVER conclusions until §6.5 is corrected.

---

## 2. Claims table

| # | Claim (dossier location) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | BJS: no adverse selection in 1,016 co-investments, 464 funds, 13,430 deals; buyout co-investment gross PME mean 1.76 vs 1.70 for other deals (§1.1, §4.1) | Confirmed | Exact. The investors number 458 LPs and the deals span 1981–2010. The 1.76 vs 1.70 difference is not significant (t = −0.55). | https://ora.ox.ac.uk/objects/uuid:f0b81a82-4ec1-44fc-abce-d5a64bfac082 |
| 2 | BJS: "portfolios of about 10 buyout deals beat funds net of fees; VC needs 20 or more" (§4.1, flagged) | **Corrected** | BJS Table 8 (net-net, median): **buyout** at 0/0 already ties or beats funds with 5 deals (1.48 vs 1.48*) and clearly beats them with 10 (1.63 vs 1.47). At 1/10 the median edges past funds at 10 deals (1.48* vs 1.47, 10% significance). At 0/20 it beats funds significantly only from about 30 deals (1.46*** vs 1.43; 10 deals 1.46 vs 1.47, not significant). Means beat funds at every size. **VC:** medians exceed funds only at 0/0 and from about 20 deals (1.17 vs 1.15, not significant; significant only at 50). With any fees, VC medians are *below* funds at every size up to 50. | ORA manuscript (BJS Table 8, text p. 30–31) |
| 3 | BJS Table 4, buyout co-investments: P25 0.26, median 1.16, P75 2.45, P99 8.43, SD 2.10, skew 2.50, N = 365. Table A's other rows (others, funds, VC) also checked (§1.2, §4.1 Table A) | Confirmed | All Table A cells match, including the capital-weighted means 1.76 / 1.59 / 1.59 / 1.55. | ORA manuscript, Table 4 |
| 4 | BJS: "only 35% of buyout deals beat their own fund's return" (§1.2) | Confirmed | BJS Fig. 2: 35% of deals in the 246 buyout funds beat their own fund's gross PME (VC 29%). This covers all deals, not only co-investments; §1.2 lists it under "For buyout co-investments". | ORA manuscript, Fig. 2 caption |
| 5 | BJS secondary figures (§2.1, §2.2, §4.1, §4.3, §4.4) | Confirmed | Net PME 1.76 / 1.59 / 1.56 vs funds 1.36. Bootstrap medians 1.16 / 1.48 / 1.63 / 1.65, mean 1.71, fund portfolios ≈ 1.44. Program cost 0.91% vs 0.11% of committed capital a year for 5 years (from FIL). Co-investment equity 32.3% of the fund's ticket (72 matched deals). Probit coefficients 0.092–0.120*** and 0.200–0.220**. | ORA manuscript, Tables 3, 7, 8 and Fig. 3 |
| 6 | BJS: "the largest deals not offered for co-investment perform worst (capital-weighted 1.59 vs 1.76)" (§4.2) | Confirmed (wording) | BJS say these deals perform "relatively poorly", and the difference is only weakly significant (10% level). "Worst" overstates it. | ORA manuscript p. 21 |
| 7 | FIL: 392 direct deals by 7 LPs, 1991–2011; capital-weighted co-investment TVPI/IRR 1.20 / −0.09% vs solo 3.08 / 16.8%; correlation −0.59 with fund commitments; mean EV $2.7bn, about 3× the GP's median deal (§1.1, §4.1, flagged) | Confirmed | Exact (Table II; text p. 16–17 and 29). The −0.59 comes from "unreported analysis". Co-investments are 288 deals ($13.9bn) of $22.6bn total. | https://www.nber.org/papers/w19299 |
| 8 | FIL: co-investment TVPI 1.18 / 1.10 / 0.78 for 2006 / 07 / 08; 73 matched deals with IRR >8 pp below the fund and no TVPI difference (later exits); 2-and-20 costs 5–7 pp a year (§1.1, §2.4, §4.1) | Confirmed | Exact. Most 2006–11 deals were unrealised when the data were collected (~2012). | https://www.nber.org/papers/w19299 |
| 9 | LMSZ: alternative vehicles reached 40% of PE commitments by 2017; they match the market but trail sponsors' main funds; top LPs get preferential access (flagged) | Confirmed | Exact (JFE 2022 abstract). The NBER WP reports 32% of investments and 17% of commitments over the full sample. The WP's discretionary-vehicle gap is −0.016 (p = 0.66); the GP-directed gap is −0.101 (p < 0.01). | https://dash.harvard.edu/entities/publication/e3f6e98d-7bcd-45a7-a12f-968964c16f5d ; https://consensus.app/papers/details/94e5f805d12f5f58b961fbb751940fc3/?utm_source=claude_desktop |
| 10 | LPG: ~1 in 10 investments returns no money; ~1 in 4 has an IRR above 50%; ~7,500 investments; median IRR 36% (smallest-scale decile) vs 16% (largest) (flagged) | Confirmed | The JFQA abstract says "does not return any money". The 2010 WP says "goes bankrupt". The 36% / 16% figures are from the WP. | https://mpra.ub.uni-muenchen.de/28487 ; https://consensus.app/papers/details/200e6cc97ac95325b4ef329c9d5a4a85/?utm_source=claude_desktop |
| 11 | Kaplan-Strömberg: 17,171 LBOs; exits strategic 38%, financial buyer 24%, IPO 14%, bankruptcy 6%, unknown 11%; exited by 2 / 5 / 6 / 7 / 10 years 12 / 42 / 51 / 58 / 76%; default ≈ 1.2% a year (flagged) | Confirmed | Exact (Table 2). The 1.2% a year assumes a 6-year hold and a 7% incidence (pre-2003 deals). The "exited" shares include bankruptcies. | https://www.nber.org/papers/w14207 |
| 12 | GKM: gross IRR/MOIC; median targets 25% IRR and 2.5×; 5-year horizon; 16% set exit = entry multiple; beta 2.3 (Axelson-Sorensen-Strömberg); debt/capital 60%, debt/EBITDA 4.0× (vs AJSW 70%); more than half do not adjust for leverage (flagged, §5, §6.3) | Confirmed | Exact (pp. 13–21). "16%" = 11 firms; fewer than 20% use DCF. | https://www.nber.org/papers/w21133 |
| 13 | BJSt: 13,523 deals in 865 funds; realised medians PME 1.4, MOIC 1.9, hold 4.3 years; persistence declined (§4.1; used for the 1.36 PME→MOIC conversion) | Confirmed | Exact (7,568 fully realised deals). | https://ideas.repec.org/a/eee/jfinec/v123y2017i2p273-291.html |
| 14 | Bain GPER 2026: debt/EV ~36% vs ~50% in 2015; entry ~14×; debt cost 8–9%; 10–12% EBITDA growth needed for 2.5× in 5 years; co-investment median 33¢ (range 0–110¢) per fee-bearing $; average buyout fee 1.6% in 2025 (Preqin); multiple expansion >50% of returns; 2025 exits $717bn on 1,570 deals; ~32,000 unsold companies, $3.8tn (flagged, §4.3, §4.5) | Confirmed | Exact. Bain's own example assumes entry/exit multiples of 14.0×/15.0× (2025) and 10.0×/12.5× (2015), with debt costs of 6% and 8%. | https://www.bain.com/insights/welcome-to-a-new-era-global-private-equity-report-2026/ ; https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ |
| 15 | Bain midyear 2026: holds ~7 years vs 5–6 in 2010–21; ~75% of buyout assets exit above the next-to-last mark; ILPA poll on exits >5% below the last mark; ~33,000 unsold companies; software marks down ~8% in Q1 (flagged, §2.5, §4.2) | Confirmed | All in the 8 Jun 2026 release, except "5–6 years in 2010–21", which is on Bain's Feb 2026 GPER outlook page (citation note). The 75% figure is an MSCI analysis cited by Bain. | https://www.prnewswire.com/news-releases/winning-firms-will-focus-on-what-they-can-control-weather-the-rest-as-triple-shock-brakes-private-equitys-latest-revival-bain--company-2026-midyear-pe-report-302793107.html |
| 16 | Lazard H1-2026: ~87% of SACV volume priced above 90% of NAV; 23% above par (8% in 2025); SACVs 54% of GP-led; volume $124bn, GP-led ~49%; existing LPs still prefer selling to rolling; "less reliance on sponsor-marked NAV" for software (flagged, §4.6) | Confirmed | Exact. Lazard also notes that "trophy assets continue to command strong valuations while transactions that do not meet pricing expectations appear less likely to close", so these are prices of completed deals (selection; see reasoning issue R1). | https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf |
| 17 | Evercore H1-2026: buyer target gross multiples ~2.3× SACV, ~1.9× MACV, ~1.8× single LP interest, ~1.7× diversified LP portfolios, over 4 years; SACVs 53% of GP-led ($34bn, +88% YoY); 52% at par, 14% above, 34% below; software CVs 10% vs 18%; directs 5% (flagged) | Confirmed | Exact; the chart is labelled "4 Year Time Horizon". Evercore says SACVs "typically feature a GP's highest-conviction asset". | https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf |
| 18 | Jefferies H1-2026: LP sales of co-investment exposure "gained momentum", including partial sales of large co-investments and one deal >$1bn; co-investment fundraising +17% to ~$27bn; syndicate capital for CVs <$750m "significantly decreased"; ~15% of buyers can write SACV checks >$250m; LP pricing 87% (buyout 91%; tail-end 25%+ discounts) (flagged) | Confirmed (context) | Quotes are exact. The $27bn is called "primary market fundraising" inside the co-investment paragraph. The <$750m decline is attributed to lead buyers underwriting entire deals, not to weaker demand (see R6). | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 19 | Sidley (Law Gazette, 3 Oct 2025): ~2/3 of managers charge no management fee; >1/2 no carry; ~1 in 10 charge the full fund rate; in together, out together; pre-emptive rights (flagged, §2.1, §4.3) | Confirmed | Exact. The figures come from an unnamed "recent industry survey". | https://www.lawgazette.co.uk/practice-points/compelling-case-for-co-investment/5124667.article |
| 20 | Investment Officer (27 Feb 2026): <7% of deals propose economics; ~62% of co-investment happens pre-signing (§4.3, §6.6) | Confirmed (weak) | Teaser text only; no underlying survey is named. Treat as anecdotal. | https://www.investmentofficer.lu/en/analyse/document/22508 |
| 21 | Torys (Mondaq, 23 Jul 2026): monitoring fees 1–2% of commitment a year; transaction fees 0.5–3% of EV; broken-deal costs/sharing in ~20% of deals; no fee offset (flagged, §1.6, §4.3) | **Corrected** | (a) The source says "approximately 20% of transactions tracked by Torys have featured the ability to charge [broken-deal] fees to passive co-investors". That is contractual ability in Torys' own sample, not costs incurred in 20% of deals. (b) The source gives monitoring fees as "between 1% and 2% of a co-investor's commitment"; "a year" is attached only to the dollar amount. Admin ($50–150k or 0.02–0.10%), transaction fees (0.5–3% of EV) and no offset are correct. | https://www.mondaq.com/unitedstates/fund-management-reits/1821370/when-no-fee-means-yes-fee-the-hidden-costs-of-co-investing |
| 22 | Bhardwaj, Gupta & Howell: recaps raise debt 84% and distress probability "by 2.4× the target-firm mean"; deal returns up, fund returns down; losses to pre-existing creditors (flagged, §1.7, §4.1) | Confirmed (as quoted) | Abstract wording matches. However, the 2.4× is a 10-year IV/LATE *increment* (+22.4 pp ≈ 2.4 × the mean of ~9.3%). The OLS estimate is +3.9 pp (≈ 42% of the mean). The dossier's ×2.4 multiplier misreads this (see R4). | https://www.nber.org/papers/w33435 |
| 23 | Capstone: sponsored recap loans $74.3bn in 2025 (+11%), after +326% in 2024; Q1-2026 −54.5% to $11bn (unattributed) (flagged) | Confirmed | Exact. 2025/2024 are from PitchBook's U.S. Interactive Leveraged Loan Volume Report (US data). Q1-2026 has no stated source, as the dossier says. | https://www.capstonepartners.com/?p=25403 |
| 24 | ABF Journal (PitchBook LCD): BSL dividends $43.6bn by 8 Dec 2025, the highest since the GFC; leverage 4.2× to 5.2×; 22% of 2025 recaps ≥6× vs 46% in 2021; LBO-to-recap lag 4.5 vs 3.6 years (§4.5) | Confirmed | Exact. The 22% / 46% shares refer to BSL-financed recaps. | https://www.abfjournal.com/the-dividend-recap-surge-what-record-sponsor-payouts-reveal-about-the-exit-impasse/ |
| 25 | "Only 17% of 2021-vintage deals had exited four years after investment, against 32% of the 2017 cohort [S: Bain via ABF Journal]" (§4.2) | **Corrected** (attribution) | The figures are right, but the source is **PitchBook LCD** (M. Lukatsky, 16 Dec 2025), via ABF Journal footnote 1, not Bain. | https://www.abfjournal.com/the-dividend-recap-surge-what-record-sponsor-payouts-reveal-about-the-exit-impasse/ |
| 26 | Proskauer FY-2025, primary NAV facilities: closing LTV mostly <25% (largest bucket 5–10%); spreads concentrated at 4–5% with a 7%+ tail of 21%; LTV sweeps 63%; no minimum MOIC 49%; 5-year maturities 45%; uses 45% follow-ons, 7% dividends (flagged, §4.7) | Confirmed (caveat) | The bucket shares match the extracted chart data: 23 / 32 / 36 / 9% and spreads 7–8% 14% plus 8%+ 7%. But Proskauer's *text* says "largest share in the 5% to 10% range" while its chart data show 36% in 10–25%. The dossier carries both statements, so it is internally inconsistent; check the chart image. The minimum-MOIC chart is not labelled primary-only. | https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025 |
| 27 | ILPA (May 2023): at least 30 calendar days to elect; status-quo option; non-response defaults to selling (flagged, §2.5) | Confirmed | Exact: "no less than 30 calendar days or 20 business days"; status quo with no minimum roll threshold; non-responders are "treated as liquidating their interests". | https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf |
| 28 | KKR case lesson: "Co-investors escaped $338m of costs for years" (§5 case 2; §2.4 phrasing is fine) | **Corrected** | $338m was KKR's *total* broken-deal and diligence spend over the 6 years ending 2011, borne by the funds. KKR misallocated "more than $17 million", the share co-investors should have borne, and paid ~$30m ($14m+ disgorgement, $4.5m+ interest, $10m penalty). | https://www.sec.gov/news/pressrelease/2015-131.html |
| 29 | HarbourVest simulation: P(<1.5×) 24% with 6 companies, 3% with 50 (§1.5, §4.4; a §6.8 calibration target) | Unverifiable | The author tags it ‡. The cited page (?p=11461) was not retrievable, and no copy of the figures was found. It should not be a calibration target until it is retrieved. | https://www.harbourvest.com/?p=11461 |
| 30 | Verisure Holdco (H&F): €1bn PIK-toggle notes, 5.625% cash / 6.375% PIK, 6 years, secured on a 43.7% listed stake; "largest and tightest" since 2019; private credit lends at a higher price (§4.7) | Confirmed | Exact (6NC1.5; issuer SPV Aegis Lux 1A). No numeric LTV is given. | https://www.ifre.com/ifr-awards/2332504/europe-high-yield-bond-verisure-holdcos-1bn-pik-notes |
| 31 | Hamilton Lane (23 Jul 2024): middle-market outperformance with "only slightly higher loss ratios"; "doubling down" risk; co-investment fund fees about half (§4.2, §5) | Confirmed | Exact. It is a marketing piece, as the dossier notes. | https://hamiltonlane.com/en-us/insight/middle-market-co-investments |

---

## 3. Citation check (ten key references, plus others)

| Reference (dossier §10) | Status | Notes |
|---|---|---|
| 1. Fang, Ivashina & Lerner (2015), JFE 116(1):160–178; NBER w19299 | Correct | RePEc matches; WP issued Aug 2013. |
| 2. Braun, Jenkinson & Schemmerl (2020), JFE 136(1):44–62 | Correct | RePEc matches. ORA lists 2019 (online first); the accepted manuscript is dated Dec 2018. |
| 3. Lerner, Mao, Schoar & Zhang (2022), JFE 143(1):359–380 | Correct | DASH matches, with this author order. The WP (w24941) lists Lerner, Schoar, Mao, Zhang and says "Private Capital" in its title; that is harmless. |
| 4. Braun, Jenkinson & Stoff (2017), JFE 123(2):273–291 | Correct | RePEc matches. |
| 5. Lopez-de-Silanes, Phalippou & Gottschalg (2015), JFQA 50(3):377–411 | Correct (title truncated) | Full title: "Giants at the Gate: Investment Returns and Diseconomies of Scale in Private Equity". The MPRA WP (2010) is titled "...On the Cross-section of Private Equity Investment Returns". |
| 6. Kaplan & Strömberg (2008), NBER w14207; JEP 23(1), 2009 | Correct | The JEP pages are 121–146. |
| 7. Gompers, Kaplan & Mukharlyamov (2016), JFE 121(3):449–476 | Correct | RePEc matches. |
| 8. Bhardwaj, Gupta & Howell (2025), NBER w33435 | Correct | Exact title and authors; issued Jan 2025, revised Apr 2025. |
| 9. Bain GPER 2026 (Feb 2026), two pages | Correct | Both pages exist and contain the cited figures. |
| 10. ILPA (May 2023), Continuation Funds guidance | Correct | The PDF exists and the text matches. |
| SEC 2015-131 (29 Jun 2015) | Correct | See claim 28 for the content issue. |
| Sidley (Lowe & Gertner, 3 Oct 2025) | Correct | Authors are Jessica Lowe and Oren Gertner. |
| Torys (Appotive, Clarkin & Stauder, 23 Jul 2026) | Correct | Mondaq lists "Michele Clarkin (Cousens)". |
| Jefferies / Evercore / Lazard 2026 | Correct | All PDFs exist and the figures match. |
| Proskauer FY-2025 | Correct | The URL redirects to a CDN-hosted PDF. |
| Capstone (26 Jun 2026) | Correct | Full title: "What Private Equity Sponsors Need to Know About Dividend Recapitalizations and Solvency Opinions"; no byline. |
| ABF Journal (Dec 2025) | Correct | The author (Lisa Rafter) is not listed in the dossier. The page shows no date; its footnotes are from Dec 2025. |
| IFR (Verisure), Hamilton Lane, Investment Officer | Correct | All exist and match. |
| HarbourVest (‡), Capital Dynamics (‡) | Not retrievable | The author's own flag stands. |
| Rede, Freshfields/GRR, Altius/PEI | Not checked | Low load-bearing. |

**Citation problems found:**
- One figure is misattributed: Bain vs PitchBook LCD (claim 25).
- In flagged claim 9, the "5–6 years" figure is cited to the midyear PR but sits on the GPER outlook page.
- The LPG title is truncated.
- The Proskauer minimum-MOIC statistic is not primary-specific.
- HarbourVest cannot be retrieved but is used as a calibration target (§6.8 item 8).
- No hallucinated or garbled academic citations were found.
- **Erratum (2026-10-18, literature audit):** this log missed two usage errors, both now corrected in the dossier. The §7 Broadie–Glasserman–Kou shift had the wrong sign (a quarterly check must use κD·e^{+0.5826σ√Δ}), and R2 relied only on the pitfall's direction. §4.2 also cited Lopez-de-Silanes et al. as deal-size evidence, although their "scale" is the number of simultaneous investments; claim 10 checked only the numbers.

---

## 4. Reasoning issues and overclaims (design implications and specification card)

Ordered by severity. "Calc" refers to `G4_coinvest_calcs.py` and its results JSON.

**R1. [High] The SELL worked example contradicts the dossier's own bid model and misapplies the SACV price data (§1.8, §6.5).**
- The dossier's bid model is p = E_b[X]/(1+y_b)^τ with y_b ≈ 20–25% for single assets, which matches Evercore's ~2.3× over 4 years (≈ 23% IRR).
- Applied with the example's own beliefs (E[exit equity] ≈ $498m at τ = 2.5y; $494m at τ = 3.5y), it implies a bid of **79% / 71% of NAV (normal)** and **65% / 56% (drought)**.
- At the 95% bid used in the example, a buyer would earn 11.5% (normal) or 7.7% (drought), less than half its target.
- The 88–95% bids come from the Lazard and Evercore distributions of *completed* GP-led SACVs. Both reports describe these as sponsors' highest-conviction or trophy assets, and Lazard says deals that miss price expectations tend not to close. That is a selected sample.
- So "in a drought it [SELL] wins outright" rests on a bid the dossier's own model says no buyer would pay. It also contradicts the context's point that secondary discounts widen in a DPI drought.
- The executive summary calls the asset "good", but its expected IRR at NAV is 9.2%, essentially the 9% hurdle.
- **Fix:** derive the bid from the buyer model conditional on asset quality. Apply the SACV pricing distribution only to assets that would qualify for a GP-led SACV, and cut the bid in a drought.

**R2. [High] The REFI breach probability is computed only at exit (§1.8, §6.5).**
- Calc section 6 reports `p_nav_down_33pct_at_exit`, which is P(exit equity < 2/3 NAV) on the terminal date.
- An LTV trigger is tested along the path. Re-running the same inputs with quarterly tests on economic equity:
  - the 1.5×-LTV trigger is breached with probability **49.6% (normal) and 62.5% (drought)**, against 28.6% and 37.5% at exit only;
  - the 2×-LTV default level is reached with probability **32.7% and 47.9%**, against 19.7% and 29.3%.
- Testing on smoothed GP marks would lower these somewhat, but they would stay well above the terminal figures.
- The dossier's own §7 pitfall says discrete or terminal monitoring overstates survival. The headline "29–37% chance of breaching" should be about 50–63%.
- [re-checked 2026-10-18, barrier re-run] These quarterly-test rates stand: the covenant itself is tested quarterly, so a quarterly simulation needs no Broadie–Glasserman–Kou shift. If LTV were monitored continuously, the trigger would be reached with probability 62.2% / 73.4% and the default level with 42.5% / 57.4%. Monthly tests give 54.6% / 67.0% and 36.4% / 51.7% (`research/groups/addenda/G4_barrier_rerun/RESULTS.md` §5.1; SYNTHETIC).

**R3. [Medium-High] The executive summary misreports the LEVER result (§1.8).**
- "Doubles wipe-out risk in a drought, from 12% to 23%" compares the *levered* position in normal conditions (11.8%) with the levered position in drought (22.8%).
- The effect of levering, from calc `p_wipeout` vs `p_residual_zero`:
  - in a drought: **7.0% unlevered → 22.8% levered** (≈ 3.3×);
  - in normal conditions: **2.1% → 11.8%** (≈ 5.5×).
- The summary therefore understates the risk added by the holdco PIK. §6.5's own numbers are stated correctly.
- [re-checked 2026-10-18, barrier re-run] These are at-exit probabilities with no barrier monitoring, so the Broadie–Glasserman–Kou fix does not change them. With the dossier's E3 barrier (V ≤ 0.75D at any time) as a sensitivity they are 7.6% → 22.9% (drought) and 2.2% → 11.8% (normal), and the conclusion holds (`RESULTS.md` §5.2; SYNTHETIC).

**R4. [Medium] The recap distress effect is misapplied (E5; §1.7 "raise distress probability 2.4× its mean").**
- Bhardwaj, Gupta & Howell's IV estimate is +22.4 pp in 10-year distress probability, "about 2.4 times the mean among dividend recap targets". That is an *increment*, so a firm at the mean would go to about **3.4×** the mean.
- It is a LATE for firms induced to recap by CLO credit supply. The OLS estimate is +3.9 pp (≈ **1.4×**).
- E5's "target ×2.4 on the distress mean" matches neither estimate.
- **Fix:** parameterise the post-recap hazard multiplier over roughly 1.4–3.4 and state the definition and horizon. [corrected 2026-10-18: 1.4–3.4 applies to the paper's average recap, which raises total debt by 84%. At E5's φ = 0.25, linear scaling gives about ×1.1 (OLS) to ×1.7 (IV) (`research/literature/00_LITERATURE_SYNTHESIS.md` §2.4 item 2).]

**R5. [Medium] The CV election is modelled as an ADIC control (§6.5 channel list; spec card SELL row).**
- A CV election exists only when the GP launches a continuation vehicle that includes the asset, so it is a GP-triggered, exogenous event, like E5 recaps.
- ILPA's protections (30 calendar days or 20 business days, status quo, default to sell) are recommendations aimed at the selling fund's LPs. Whether a co-investment vehicle participates is contractual, as the dossier itself says in §2.5 and §9.
- In the optimiser, the CV channel must be an offer event with its own arrival rate, not a per-quarter decision.
- LP-led strip sales likewise depend on GP consent and ROFR and may be barred for partial transfers. They need a feasibility flag, not an always-available fraction x.

**R6. [Medium] A Jefferies remark is turned into an unsupported drought stress (§4.6; spec card stress row "SACV syndication thins for deals <$750m").**
- Jefferies says syndicate capital on deals under $750m decreased because lead buyers increasingly "underwrite the entire portion of transaction equity" (pre-emptive deals). This was in an H1-2026 market with record volume.
- That is about allocation structure, not a shortage of demand, and it is not drought-specific.
- The [I] "liquidity constraint" inference and the stress parameter are not supported by the source.

**R7. [Medium] "P(loss) does not depend on leverage" is a model artifact presented as a property (§1.3, §2.3 property 1).**
- It holds only because the model fixes debt in PME units (D_T ≈ D_0), uses the same G distribution at every L and has no coverage-driven default.
- Fixing debt in PME units also implicitly charges debt at the equity-benchmark return rather than today's 8–9%.
- Property 3 (failure through cash flow above 6×) contradicts it.
- The re-based means (1.73 → 1.45 → 1.30) inherit these assumptions. They should be reported as a stylised sensitivity, not as the reference class.

**R8. [Medium] θ = 0.33 is tagged [S] but used as an LP-level offer rate (§1.9, §6.6.1).**
- Bain's 33¢ median is a GP-level ratio of co-investment offered to fee-bearing capital, framed as a 25% cut in GP revenue.
- Using it as the co-investment ADIC receives per dollar of *its own* commitments is an assumption. LMSZ show allocations are skewed toward top LPs.
- Tag it [I] and calibrate it from ADIC's offer log (open question 4).

**R9. [Low-Medium] The LEVER rule is mis-specified (§6.5 rule).**
- The rule reads: lever if μ̂ − r_PIK > ℓ̄ + risk charge.
- The worked LEVER example is a cash-out holdco PIK on an existing position. By the dossier's own taxonomy that is REFI, and it *releases* liquidity, so ℓ̄ should be a credit, not a hurdle.
- If LEVER means a debt-funded ADD (cash-neutral), ℓ̄ should not appear at all.
- Reconcile with dossier 08's LEVER ≡ ADD + REFI.

**R10. [Low-Medium] The diversification results overclaim (§1.5 "this matches the BJS bootstrap"; "diversify across vintages more than across deals").**
- The model's ρ = 0 medians (1.63 at 5 deals, 1.68 at 10, 1.73 at 20, 1.75 at 50) sit above the BJS no-fee medians (1.48, 1.63, 1.61, 1.65).
- The gaps of 0.10–0.15 at 5, 20 and 50 deals exceed BJS's ~0.05 program-cost deduction. BJS portfolios are also capital-weighted, while the model uses equal weights.
- The model therefore diversifies faster than the data, a point §6.3 itself concedes.
- The vintage conclusion is driven by the *assumed* factor sizes (vintage loading 0.20 vs global 0.05), not by evidence.

**R11. [Low] "Today's" leverage is inconsistent.**
- The dossier uses three values: 36% debt/EV in the text (Bain), L = 0.40 in the re-basing table, and L₀ = 0.45 "(today)" in the spec card and the synthetic book simulation (calc `BOOK.L_entry = 0.45`).
- The 3-year cash-flow and write-off outputs therefore use more leverage than the stated current reference class.

**R12. [Low] The REFI example breaks the dossier's own LTV schedule (§6.5).** It applies 15% LTV to a single asset, while the schedule caps LTV at ≤10% when effective N < 10.

**R13. [Low] The required-growth formula is under-specified (§2.3).**
- ℓ_T is undefined. The formula is right only if ℓ_T is exit debt divided by *entry* EBITDA, and it ignores interest and cash generation.
- With Bain's inputs it gives 12–13%, against Bain's own 10–12%.
- Bain's 2025 example assumes multiple expansion (14× → 15×), which the dossier's own "what you need to believe" check would flag.

**R14. [Low] The exit hazard double-counts terminations.**
- The Weibull (k = 1.447, η = 7.70) is fitted to Kaplan-Strömberg *all-cause* exits, which include bankruptcy and unknown exits. E3 then adds a separate default channel.
- The simulated write-off rate, about 2.8–3.3% a year after the barrier fix, is about 2.3–2.8× KS's 1.2% a year, with no reconciliation [corrected 2026-10-18: was "2.1–2.5% a year ... about double", from a quarterly barrier check with no correction; the fix strengthens this issue (`research/groups/addenda/G4_barrier_rerun/RESULTS.md` §3, §8)]. At the old rate it was judged consistent with LPG's ~10% zero-return share, so the sources disagree and the dossier should say so [not re-checked at the corrected rate, which implies a higher lifetime write-off share].
- Use cause-specific hazards, which §7 already recommends.

**R15. [Low] Internal inconsistencies.**
- PME → MOIC conversion is 1.07^T in the fee analysis but a constant 1.36 in the G9 recalibration.
- The fee-drag table uses the historical class (L = 0.60, mean gross 2.48×), although §6.4 says underwriting must use the re-based class.
- §1.2 places BJS's all-deal 35% statistic under "For buyout co-investments".

---

## 5. Independent re-computation (decision examples)

Script: `scratchpad/g4v_scripts/check_decisions.py`. It uses the same inputs as calc section 6:
- NAV $400m, nowcast 97% of NAV, net debt 6.0× at 14× EV;
- normal: τ = 2.5y, μ = 6%, σ = 28%; drought: τ = 3.5y, μ = 4%, σ = 30%;
- 400k paths, quarterly steps.

| Metric | Normal | Drought | Dossier value |
|---|---|---|---|
| E[exit equity] ($m) | 498.3 | 493.2 | 498.5 / 494.6 |
| P(trigger: equity < 2/3 NAV), at exit only | 28.6% | 37.5% | 29% / 37% (reproduced) |
| P(trigger), tested quarterly | **49.6%** | **62.5%** | not reported |
| P(default level: equity < 1/2 NAV), at exit | 19.7% | 29.3% | 19.8% / 29.2% |
| P(default level), tested quarterly | **32.7%** | **47.9%** | not reported |
| Bid implied by the dossier's buyer model, y_b = 20% | **79% of NAV** | **65% of NAV** | example uses 88% / 95% |
| Bid implied by the dossier's buyer model, y_b = 25% | **71% of NAV** | **56% of NAV** | n/a |
| Buyer IRR at a 95% bid | 11.5% | 7.7% | 11.5% / 7.8% (matches) |

From calc JSON, unlevered vs levered wipe-out at exit: 2.1% → 11.8% (normal) and 7.0% → 22.8% (drought) [re-checked 2026-10-18: unchanged by the barrier fix; see R3].

---

## 6. Overall reliability rating

**MEDIUM.**
- **Sourced facts: high.** 26 of 31 claims are confirmed exactly, 4 have minor or moderate corrections, none are refuted and 1 (‡, already flagged by the author) is unverifiable.
- **Model and decision layer: medium to low until fixed.** Issues R1–R5 directly change the SELL, REFI, LEVER and recap guidance the IC would see:
  - SELL is overstated in drought;
  - single-asset REFI breach risk is understated by about 20–25 pp;
  - the LEVER risk increase is misreported;
  - the recap hazard multiplier is mis-sourced;
  - CV election is treated as an ADIC control.
- Issues R6–R15 are calibration and labelling fixes.

**Recommended before IC use:** correct §1.8 and §6.5 (R1–R3, R5, R9), re-specify E5 (R4), drop the Jefferies-based drought stress (R6), re-tag θ as [I] (R8), and apply the four corrections in §2.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.4 items 1–3; `research/literature/G4_coinvest.lit.md` §1–§2; `research/groups/addenda/G4_barrier_rerun/RESULTS.md`. The dossier was edited on this date by the citation-correction pass, not by this verification.

- R14: simulated write-off rate "2.1–2.5% a year ... about double" KS's 1.2% → "about 2.8–3.3% a year ... about 2.3–2.8×" after the BGK barrier fix; the LPG comparison is flagged as not re-checked.
- R2: note added that the quarterly-test breach rates (49.6% / 62.5%; default level 32.7% / 47.9%) are unchanged by the BGK fix, with continuous (62.2% / 73.4%; 42.5% / 57.4%) and monthly bounds.
- R3: note added that the wipe-out rates are at-exit figures unchanged by the BGK fix, with the E3-barrier sensitivity (7.6% → 22.9%; 2.2% → 11.8%).
- R4: the fix range 1.4–3.4 is annotated as applying to +84% debt; it is about ×1.1 (OLS) to ×1.7 (IV) at φ = 0.25.
- §5: the wipe-out line is labelled "at exit".
- §3: one erratum line added for the missed BGK sign error and the Lopez-de-Silanes et al. "scale" misreading.
