# Verification log: Stream 03, sovereign ALM (oil-fiscal linkage; owner distribution demand as a stochastic liability)

**Dossier checked:** `research/dossiers/03_sovereign_alm.md` (as of 18 Oct 2026; not edited).
**Verified:** 2026-10-18.
**Role:** adversarial fact-check before Investment Committee (IC) use.

---

## 1. Summary

**Result: 32 claims checked: 28 confirmed, 4 corrected, 0 refuted, 0 unverifiable.**

The author flagged 20 claims, and every one was checked. Twelve more were added: findings attributed to papers, peer episodes, and the dossier's own [I-calc]/[I-MC] numbers.

**The empirical base is strong.** All of the following match primary sources exactly:
- **IMF UAE 2025 Article IV** (CR 25/327), Table 3a: breakevens 54.0 / 48.3 / 45.7 / 44.8 / 44.8 / 45.2 / 45.6 / 45.9 and hydrocarbon revenue 13.4 → 9.1% of GDP. The procyclicality sentence and the peg wording are verbatim.
- **IMF DataMapper.** UAE, Saudi and Kuwait net lending and UAE GDP match. UAE real GDP is −3.9% (2026) and +7.7% (2027), the WEO Oct 2026 vintage per press coverage.
- **EIA STEO.**
  - Oct 2026 Table 1: shut-ins 10.9 → 5.76 → 4.77 → 4.47 → 2.68 mb/d. UAE 740 kb/d average for Mar–Jul and 0 in Aug–Sep. Saudi 2,750 kb/d average for Mar–Jul.
  - Brent: US$114 (Sep), US$131 daily peak (15 Sep), forecasts US$105 / 96 / 87 / 84 / 74.
  - May 2026: UAE exit effective 1 May 2026; 2027 spare capacity 3.8 → 2.5 mb/d.
  - Feb 2026: US$58 / 53.
  - Jun 2026: "extremely limited since military action began on February 28".
- **EIA daily Brent:** US$135.51 (2 Oct) and US$126.55 (14 Oct).
- **Press:** both Al Jazeera articles; Gulf News/FTfm and IR Impact (2015 redemptions); Bain 2026.
- **Papers and official texts:** IMF Kuwait Article IV (CR 26/52); Valencia (Mexico hedge); Borensztein–Jeanne–Sandri; Bodie–Brière (footnote 11, Chile 1.05 / 0.15 / 0.10, −7%); Brown et al.; Bernanke (40–45%; 0.68 vs 0.05); Baumeister–Hamilton; Moutanabbir–Noureldin; Erbil; GFSR Apr 2026; EIA *Today in Energy* (Hormuz bypass).

**All [I-calc]/[I-MC] numbers reproduce exactly.**
- The public data (EIA RBRTE, Ken French US and Developed factors, CBOE VIX) were re-downloaded on 18 Oct 2026 into a clean folder, and the three scripts were re-run.
- `oil_equity_regimes.json`: 326 of 326 values identical.
- `draw_model_demo.json`: 92 of 92 identical.
- The HMM, shock-share and hybrid-price blocks are identical to the stored JSONs wherever keys overlap.

**No citation is hallucinated.** All 18 references checked exist, with correct authors, year, venue and pages (§4).

**Corrections, all minor or scoping:**
1. **IMF coverage caveat.** The "excludes SWF investment income; partial coverage of Abu Dhabi" note is footnote 3/ of Table 3a. It attaches to the *adjusted non-hydrocarbon primary balance* line, not to the breakeven or hydrocarbon lines.
   - The IMF publishes an "adjusted" balance precisely to strip staff-estimated SWF income.
   - So headline revenue, and possibly the 44.8 breakeven, may *include* fund income. This becomes design issue 4.
2. **Bain attribution.** The 14%-of-NAV distribution metric is MSCI data. The ~7-year holding period and the ~32,000 companies / US$3.8trn unsold are PitchBook/Preqin data, not MSCI.
3. **HMM outlier.** The unwinsorised 3-state HMM degenerated on **March 2020**, not April 2020. Month-end Brent went from 51.31 to 14.85, a log return of −1.24. April 2020 was +0.20.
4. **Low-price spell.** The 22-month spell is the longest "since mid-1990", not "since 1988". The trailing-36-month test is first defined in May 1990 (EIA daily Brent starts 20 May 1987), so the 1986 collapse is outside the sample.

**The design layer carries the real risk.** Several exec-summary inferences are contradicted by the dossier's own model or rest on estimates far noisier than presented (§5):
- "ADIC should expect to sit near the cap": the model gives mean SG/DB draws of 6.8–6.9%.
- The 266m-bbl hedge size ignores ρ = 0.5 smoothing, so year-1 exposure is about half.
- The cap kink of ≈US$31 depends on an unsupported linear-in-log-oil fiscal mapping. The dossier's own η_P ≈ 1 revenue equation implies ≈US$22–24.
- "Buy hybrids now" rests on realised correlation, including a 6-month window with a 95% CI of −0.95 to +0.44, rather than priced correlation.

---

## 2. Claims table

Flagged claims are F1–F20; additional claims are A1–A12.

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| F1 | IMF UAE 2025 Art. IV (pre-war): consolidated breakeven 54.0 / 48.3 / 45.7 / 44.8 / 45.9 (2030); hydrocarbon revenue 11.3% (2026) → 9.1% (2030) of GDP; figures exclude SWF investment income and cover Abu Dhabi partially | **corrected (scope)** | All numbers exact (CR 25/327, Table 3a, p.29; Board 1 Dec 2025, published 8 Dec). Footnote 3/ ("Excludes staff estimates of SWFs investment income; partial coverage of Abu Dhabi government and Abu Dhabi pension fund accounts") attaches to the *adjusted non-hydrocarbon primary balance* line. The existence of an "adjusted" series implies headline revenue (Other revenue ≈9–11% of GDP) may include SWF income. Do not assume the 44.8 breakeven excludes it. | https://www.imf.org/-/media/files/publications/cr/2025/english/1areea2025001-source-pdf.pdf |
| F2 | UAE GG net lending +1.7 (2014), −6.4 (2015), −2.4 (2020), +3.9 (2025), +1.5 (2026), +4.4 (2027); GDP US$661bn (2026) | confirmed | Exact. GDP 424.9 (2014), 382.0 (2015), 614.4 (2025), 661.0 (2026). 2026–27 values are projections, not outturns. | https://www.imf.org/external/datamapper/api/v1/GGXCNL_NGDP/ARE ; https://www.imf.org/external/datamapper/api/v1/NGDPD/ARE |
| F3 | DataMapper UAE real GDP −3.9% (2026), +7.7% (2027); vintage presumed WEO Oct 2026 | confirmed | Exact. Press coverage of the 13 Oct 2026 WEO reports the same figures: −3.9% (cut 7pp from April) and +7.7%, assuming Hormuz reopens in March 2027. Vintage confirmed. | https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH/ARE ; https://www.thenationalnews.com/business/economy/2026/10/13/imf-cuts-2026-growth-forecasts-for-gulf-economies-due-to-prolonged-hormuz-closure/ |
| F4 | EIA STEO Oct 2026: shut-ins peak ≈10.9 mb/d (May), 5.8 (Aug), 4.8 (Sep), 4.5 (4Q26F), 2.7 (1Q27F); UAE 0.74 (Mar–Jul avg), 0 (Aug–Sep); Brent US$114 (Sep), US$105 (4Q26), US$84 (2027), US$74 (4Q27) | confirmed | Table 1 (p.5): 5,760 / 4,770 / 4,470 / 2,683 kb/d; UAE 740 / 0 / 0; Saudi 2,750. Text: US$131 daily peak on 15 Sep; 2Q27 US$87; 2026 average US$96. Released 6 Oct 2026, forecast completed 1 Oct. | https://www.eia.gov/outlooks/steo/ ; https://www.eia.gov/outlooks/steo/report/global_oil.php |
| F5 | EIA STEO May 2026: UAE leaves OPEC effective 1 May 2026; 2027 OPEC spare capacity cut 3.8 → 2.5 mb/d | confirmed | Verbatim, p.3. | https://www.eia.gov/outlooks/steo/archives/may26.pdf |
| F6 | Feb 2026 STEO Brent US$58 (2026), US$53 (2027); military action began 28 Feb 2026; Hormuz "extremely limited" (Jun STEO) | confirmed | Feb STEO: US$58 / 53, against a 2025 average of US$69. Jun STEO p.5 is verbatim. Jun STEO also gives UAE shut-ins of 1,450 / 1,100 / 1,350 kb/d (Mar–May) and May Brent of US$107. Note that the Feb numbers come from feb26.pdf, not the cited jun26.pdf. | https://www.eia.gov/outlooks/steo/archives/feb26.pdf ; https://www.eia.gov/outlooks/steo/archives/jun26.pdf |
| F7 | EIA Brent spot US$135.51 (2 Oct), US$126.55 (14 Oct); realised vol ≈77% since 1 Mar 2026 vs 36% (2015–19) | confirmed | Spot values exact; 15 Sep was 130.80. Re-computed vol is 76.8% vs 35.7%. Excluding the 2 Oct spike it is 74.3%, so the figure is robust. | https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RBRTE&f=D |
| F8 | Monthly oil–equity ρ −0.14 (1988–2007), +0.43 (2008–19), +0.32 (2020–Aug 26), −0.58 (Mar–Aug 26); lower-tail dependence 0.08 / 0.30; rolling 36m −0.28 (Aug 26) | confirmed | Reproduced exactly from fresh downloads. **Precision caveat:** 95% CIs are (−0.26, −0.01; n = 240), (0.29, 0.56; n = 144), (0.11, 0.51; n = 80 paired months), and **(−0.95, +0.44)** for the n = 6 war window. Tail dependence is 2/24 vs 7/23 joint months (Fisher exact p = 0.07). | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html ; EIA RBRTE |
| F9 | Of six years with Brent ≤ −30% (1991, 1997, 1998, 2008, 2014, 2015) only 2008 had negative US equities; P(eq ≤ −10% \| oil ≤ −30%) = 26% (18% pre, 30% post-2008); longest low-price spell 22 months from Dec 2014 | confirmed | Reproduced exactly. **Fragility:**<br>- 2015 US equity total return was +0.21% (KF); the S&P 500 price index fell 0.7% that year.<br>- The 26% is 14 of 54 overlapping months, and 11 of the 14 come from Oct 2008–Aug 2009. The 3 "hit" episodes are Sep 1988, Oct–Nov 2001 and the GFC, out of 11 conditioning episodes. | EIA RBRTE ; Ken French library |
| F10 | US/Israeli attacks began 28 Feb 2026; UAE hit more than Israel and all GCC combined; capacity 4.8 vs quota 3.2 mb/d; Fujairah 1.7 mb/d (2025) | confirmed | Verbatim: "the UAE has been hit more than Israel and all Gulf Cooperation Countries (GCC) together"; "4.8 million bpd"; "3.2 million bpd"; 1.7 mb/d "last year"; target of 5 mb/d by 2027. The Ember (Kingsmill Bond) "oil demand in decline / sell as much as possible" framing is also confirmed. | https://www.aljazeera.com/news/2026/4/29/uae-quits-opec-what-that-means-for-the-gulf-energy-markets-and-beyond |
| F11 | IMF WEO Oct 2026 (via Al Jazeera): ME&CA −0.3% (April +1.9%); Kuwait −16.7, Iraq −16.0, Qatar −15.6, Bahrain −11.3, Saudi −3.3 | confirmed | All exact; Iran −7.6 also exact. The article says "latest economic outlook". WEO Oct 2026 was released 13 Oct 2026. | https://www.aljazeera.com/economy/2026/10/13/middle-east-and-central-asias-economy-to-shrink-in-2026-amid-war-imf-says |
| F12 | Bain PE Report 2026 (MSCI data): distributions ≈14% of NAV (2025), <15% four years, last this low 2008–09; holding ≈7 yrs; ≈32,000 companies / US$3.8trn unsold | **corrected (attribution)** | Numbers exact. Bain calls the four years "an industry record". The 14% is MSCI data (Fig. 19). The holding period (buyout, "around seven years") and the 32,000 / US$3.8trn are PitchBook/Preqin data (Fig. 17), not MSCI. | https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ |
| F13 | 2015: SWFs pulled ≥US$46.5bn from managers (eVestment / FTfm); Moody's "plug fiscal deficits"; SAMA ≈US$70bn; ME oil SWFs US$19bn in Q3 2015 | confirmed | Gulf News: "at least $46.5 billion ... in 2015"; Moody's quote. IR Impact (7 Dec 2015, citing FT/eVestment): US$19bn in Q3, "fastest rate of withdrawal ever"; SAMA US$70bn; BlackRock US$31bn (Morgan Stanley). | https://gulfnews.com/business/markets/sovereign-wealth-funds-pull-at-least-465b-from-asset-managers-1.1677026 ; http://www.ir-impact.com/2015/12/gulf-governments-pull-cash-swfs-record-pace/ |
| F14 | Endowments cut payouts after negative but not positive shocks ("hoarding") | confirmed | Abstract: endowments "actively reduce payouts relative to their stated payout policies following negative, but not positive, shocks". | https://www.aeaweb.org/articles?id=10.1257/aer.104.3.931 |
| F15 | Mexico hedge: Asian puts near budget price, ≈29% of production; ≈0.1% of GDP a year since 2001; paid 0.5 / 0.6 / 0.3% of GDP (2009/15/16); borrowing costs ≈19bp higher without | confirmed | All verbatim. Valencia, IMF blog, 26 Mar 2018; most contracts are on Maya. | https://www.imf.org/external/np/blog/dialogo/032618.pdf |
| F16 | BJS WP/09/229: gains mainly from reducing precautionary foreign assets, "several percentage points of annual consumption", ≫ smoothing | confirmed | Abstract verbatim (Oct 2009). The smoothing channel is ≈0.4% of consumption. | https://www.imf.org/external/pubs/ft/wp/2009/wp09229.pdf |
| F17 | Kuwait 2025 Art. IV: FLL enacted March 2025, first issuance since 2017; 2025 issuance 4.6% domestic + 7.2% external of GDP for deficits and GRF; FGF transfers ≈0; KIA ≈640% of GDP | confirmed | CR 26/52 (24 Feb 2026): all verbatim. FGF transfers in the table are 0.0 / 0.1 / 0.0 / 0.0. KIA was 640% (end-2025), up from 605%. | https://www.imf.org/-/media/files/publications/cr/2026/english/1kwtea2026001-source-pdf.pdf |
| F18 | Bodie–Brière: speculative portfolio plus hedging demands; hedge the revenue-flow variability, not the price; Chile copper sensitivity 0.15 | confirmed | Footnote 11 is verbatim. Sensitivities are 1.05 / 0.15 / 0.10 (1991–2009). The text attaches them to the "expenditure growth rate" but uses them for receipts, as the dossier already notes. Developed equities have −7% correlation with the fiscal surplus. | https://research-center.amundi.com/files/nuxeo/dl/1ff3c6f5-2e14-4633-a55a-5379b02dc112 |
| F19 | IMF: UAE GG fiscal stance historically procyclical, balance and expenditure changes positively correlated with oil | confirmed | ¶12 verbatim, followed by "conservatively based annual budgets ... similar to an automatic stabilizer". | (CR 25/327 PDF above) |
| F20 | ADIC: 2007 ADIA spin-off; March 2018 law under Mubadala; ≈US$123bn (SWFI, 2018); Bloomberg 4 Feb 2026 ≈US$160bn, ≥10% target; US$177bn and 5–10% band not public | confirmed | The National (21 Mar 2018) gives US$123bn (ADIC) and US$127bn (Mubadala) from SWFI, plus the bank stakes. Wikipedia gives April 2007, the ADIA spin-off and the March 2018 law (citing WAM / Official Gazette); The National does not contain these. The Bloomberg headline and summary confirm US$160bn and ≥10%. The 177bn and 5–10% are not found publicly. | https://www.thenationalnews.com/business/abu-dhabi-investment-council-to-join-forces-with-mubadala-1.714997 ; https://en.wikipedia.org/wiki/Abu_Dhabi_Investment_Council ; https://www.bloomberg.com/news/articles/2026-02-04/abu-dhabi-s-160-billion-endowment-style-fund-eyes-bolder-bets |
| A1 | Bernanke (2016): Hamilton-style regression; ≈40–45% of the decline demand-driven; demand+risk component ρ 0.68 vs residual 0.05 | confirmed | With P. Olson; copper, dollar and 10y yield, with ΔVIX added. | https://www.brookings.edu/articles/the-relationship-between-stocks-and-oil-prices/ |
| A2 | Baumeister–Hamilton (2019): supply disruptions a bigger historical factor; supply shocks hit activity with a lag | confirmed | Abstract: "Supply shocks lead to a reduction in global economic activity after a significant lag". | https://www.aeaweb.org/articles?id=10.1257/aer.20151569 |
| A3 | Moutanabbir–Noureldin (2018): annual 1976–2016; equity shocks negatively correlated with oil-income shocks; oil hedging demand ≈0.01–0.07pp except at extreme risk aversion | confirmed | Table 5: 0.01–0.07, but 9.53 at γ = 12 with oil variance ×1.15. | https://erf.org.eg/app/uploads/2018/03/1172_Final.pdf |
| A4 | Norway's first-ever withdrawal in January 2016 | confirmed | Full-year 2016 withdrawal was NOK 101bn. The January amount varies by source. | https://www.cnbc.com/2016/03/07/norway-taps-its-oil-fund-for-the-first-time.html |
| A5 | SAMA moved SAR150bn (US$40bn) to PIF in Mar–Apr 2020 | confirmed | Per Al-Jadaan (May 2020). **This was a reallocation to fund opportunistic purchases, not a fiscal draw.** See §5 issue 9. | https://www.bloomberg.com/news/articles/2020-05-29/saudi-central-bank-transferred-40-billion-to-sovereign-fund |
| A6 | GFSR Apr 2026: frequent supply shocks weaken the equity–bond hedge; risk of simultaneous sell-offs | confirmed | "simultaneous and larger sell-offs of equities and bonds occur during market downturns, reflecting more frequent supply shocks". | https://www.imf.org/en/publications/gfsr/issues/2026/04/14/global-financial-stability-report-april-2026 |
| A7 | Erbil (2011): 28 developing oil producers 1990–2009; strongly procyclical; expenditure countercyclical in the high-income group | confirmed | Abstract verbatim. Cyclicality is measured against non-oil output, not the oil price. | https://www.imf.org/external/pubs/ft/wp/2011/wp11171.pdf |
| A8 | Hormuz 20 mb/d (2024, ≈20%); East-West 5 mb/d (7 temporarily); UAE line 1.8 mb/d; ≈2.6 mb/d unused bypass | confirmed | EIA *Today in Energy*, 16 Jun 2025. The 7 mb/d was a temporary expansion in 2019. | https://www.eia.gov/todayinenergy/detail.php?id=65504 |
| A9 | Comparators: Saudi −14.9 / −13.2 / −10.2 / −6.5 (2015, 2016, 2020, 2026); Kuwait 29.8 / 0.2 / 15.8 (2014, 2020, 2026) | confirmed | Exact. Note that Saudi 2025 was already −5.8. | https://www.imf.org/external/datamapper/api/v1/GGXCNL_NGDP/SAU |
| A10 | §4.3 / §7: unwinsorised 3-state HMM "collapsed onto the April 2020 outlier" | **corrected** | **March 2020**: month-end Brent 51.31 → 14.85, log −1.24. April 2020 was +0.20 (14.85 → 18.11). | EIA RBRTE (re-run) |
| A11 | §1.4 / §4.2: 22-month spell is "the longest such spell since 1988" | **corrected** | The test is defined only from May 1990, so it is the longest since mid-1990. The 1986 price war, the canonical SG analogue, is outside the sample. | EIA RBRTE; `oil_equity_regimes.py` |
| A12 | [I-calc]/[I-MC] HMM (calm/turbulent ρ 0.01 / 0.16, durations 18.6 / 8.9 months), shock shares (59.6 / 17.8 / 13.5 / 5.0 / 4.1%), kinks 64.4 / 31.1, sensitivity grid, hybrid table | confirmed | Re-run is identical. Scope caveats are in §5 issues 5 and 8. | local re-run (see §3) |

---

## 3. Reproduction of the dossier's own computations

**Data.** Everything was downloaded on 18 Oct 2026 into a fresh scratch folder:
- EIA RBRTE daily HTML (last value 14 Oct 2026 = 126.55);
- `F-F_Research_Data_Factors_CSV.zip`;
- `Developed_3_Factors_CSV.zip`;
- CBOE `VIX_History.csv` (last value 16 Oct 2026 = 19.99).

**Scripts.** The three scripts in `research/addenda/03_sovereign_alm_calcs/` were run unmodified with `python -I`.

**Results:**

| Script | Stored JSON | Outcome |
|---|---|---|
| `oil_equity_regimes.py` | `oil_equity_regimes.json` | 326 of 326 values identical |
| `draw_model_demo.py` | `draw_model_demo.json` | 92 of 92 values identical |
| `regimes_and_hybrids.py` | `regimes_and_hybrids.json`, `regimes_hmm_winsorized.json` | All overlapping keys identical |

**Version mismatch.** For `regimes_and_hybrids.py`, the only differences are missing keys:
- the stored `regimes_and_hybrids.json` came from an earlier script version (it has an unwinsorised `hmm_3state` block that the current script cannot produce);
- `regimes_hmm_winsorized.json` is not written under that name by any script.

**Hygiene fix.** Archive the input data snapshot, and pin script versions to JSON outputs.

---

## 4. Citation check

| # | Reference as given | Status | Note |
|---|---|---|---|
| 1 | Gintschel & Scherer (2008), *J. Asset Management* 9, 215–238 | correct | Crossref DOI 10.1057/jam.2008.19, issue 9(3). |
| 2 | Scherer (2009), *Fin. Markets & Portfolio Mgmt* 23, 315–327 | correct | Matches the ERF WP 1172 reference list. |
| 3 | Scherer (2011), *J. Alternative Investments* 13, 24–34 | correct | ERF reference list; the EDHEC page confirms the Winter 2011 JAI issue. |
| 4 | van den Bremer, van der Ploeg & Wills (2016), *EER* 82, 113–131 | correct | Crossref DOI 10.1016/j.euroecorev.2015.10.005. |
| 5 | Bodie & Brière (2014), *JOIM* 12(1) | correct | The JOIM listing gives Vol 12 No 1, Q1 2014; one workshop source dates it Q4 2013. The Amundi WP-011-2011 (rev. June 2013) title says "A New Framework". |
| 6 | Brown, Dimmock, Kang & Weisbenner (2014), *AER* 104(3), 931–62 | correct | AEA page. |
| 7 | Kilian (2009), *AER* 99(3), 1053–69 | correct | AEA page. |
| 8 | Baumeister & Hamilton (2019), *AER* 109(5), 1873–1910 | correct | AEA page. |
| 9 | Känzig (2021), *AER* 111(4), 1092–1125 | correct | AEA page. |
| 10 | Ready (2018), *Review of Finance* 22(1), 155– | correct, incomplete | Pages are 155–176 (Crossref). Published online 2017, print 2018. |
| 11 | Robinson & Sensoy (2016), *JFE* 122(3) | correct, incomplete | Pages are 521–543. The abstract confirms distributions are more cyclical than calls. |
| 12 | Borensztein, Jeanne & Sandri (2009), IMF WP/09/229 | correct | October 2009. The JDE 2013 version was not checked here; the dossier marks it [U]. |
| 13 | Moutanabbir & Noureldin (2018), ERF WP 1172 | correct | February 2018. |
| 14 | Das, Lu, Mulder & Sy (2009), IMF WP/09/179 | correct | The IMF page lists Mulder, Sy, Lu, Das (1 Aug 2009), as the dossier notes. |
| 15 | Erbil (2011), IMF WP/11/171 | correct | July 2011. |
| 16 | Valencia (2018), IMF blog | correct | 26 Mar 2018. |
| 17 | Bernanke (2016), Brookings | correct | 19 Feb 2016; co-analysis with Peter Olson. |
| 18 | Balding & Yao (2011), *Int. Finance Review* 12, 293–312 | correct | ERF reference list; Emerald DOI series S1569-3767(2011)0000012014. |

**Source-pointer problems** (not hallucinations):
- **F6:** the Feb-STEO prices are in `feb26.pdf`, not the cited `jun26.pdf`.
- **F20:** the cited The National article does not contain the 2007 / ADIA or 2018-law facts; Wikipedia does.
- **F12:** "(MSCI data)" is over-broad.
- **F1:** the coverage caveat is attributed to the wrong lines.

---

## 5. Reasoning issues and overclaims in the design layer

Issues are ranked by how much they would change what the IC sees.

**1. [Medium-high] The exec summary contradicts the dossier's own draw model.**
- *What the dossier says:* §1.4 says that in a 2014–16-type glut "ADIC should expect to sit near the cap". The §2.4 state table gives DB → "cap" and SG → "rises toward cap", and the §6.7 liquidity table uses a 10% draw in DB.
- *What its model says:* mean draws by state are:

  | Breakeven | DB | SG |
  |---|---|---|
  | Default US$44.8 | 6.9% | 6.8% |
  | Prior median US$55 | 7.6% | 7.6% |
  | US$65 | 8.1% | 8.2% |

  P(draw ≥ 9.5%) in SG is 2.5% at the default.
- *Why the "6× band width" argument fails:*
  - it ignores ADIC's share ω, the other pockets (ADIA, Mubadala, L'imad/ADQ) and debt substitution, which is the Kuwait precedent the dossier itself cites;
  - it applies the 2014–15 net sensitivity (h ≈ 13%) to 2026, although h is now 11.3%, falling to 9.1%. That gives ≈7.2pp, not 8.1pp.
- *Fix:* state draw levels conditional on P^BE and ω, and label cap draws in the DCR as a stress assumption, not an expectation.

**2. [Medium] Hedge sizing ignores the dossier's own smoothing and non-linearity.**
- *What the dossier says:* the 266m-bbl "put-spread notional" (§1.1, §6.11).
- *The problems:*
  - It is the *average* slope of the target rate d* between the kinks.
  - With ρ = 0.5, the same-year draw moves half as much (≈133m bbl at US$177bn). The rest arrives in later years as a strip (Asian-like), which §2.3 acknowledges but the sizing ignores.
  - In the log model, the local delta ranges from ≈190m bbl at US$64 to ≈390m bbl at US$31.
  - A 1–2-year put spread at 20–40% of 266m bbl can therefore be about twice the year-1 exposure.
- *Fix:* size the hedge against simulated d_t paths, not d*, using strips.

**3. [Medium] The kinks and strikes depend on an unsupported functional form.**
- *What the dossier says:* "the fiscal balance is roughly linear in log oil", so the draw is "exactly" a log-put spread.
- *The problems:*
  - This contradicts §6.5's own revenue equation with η_P ≈ 1, under which revenue, and hence FB, is linear in the price level.
  - Under a linear-in-P mapping (h = 11.3% at a US$60–65 reference price), the cap kink moves from ≈US$31 to ≈US$22–24 and the floor kink from ≈US$64 to ≈US$66–68. That relocates the recommended short-put strike.
  - "Exactly" holds only with w = 0, ρ = 0, no override and no NAV co-movement.
  - The code uses 100h = 11.0, while the text says 11.3. With 11.3, the kinks are 63.8 / 31.4 rather than 64.4 / 31.1.
- *Fix:* estimate the mapping and publish the kinks under both forms.

**4. [Medium] The draw rule may be circular because of how the fiscal state is defined.**
- *The problem:*
  - IMF UAE GG revenue includes a large "Other revenue" line (≈9–11% of GDP).
  - The IMF publishes an "adjusted" balance specifically to remove staff-estimated SWF investment income. So the headline balance, and possibly the 44.8 breakeven, may include fund income, potentially ADIC's own distributions.
  - A rule d* = Π(c − b·FB) on such an FB is simultaneous: higher draws raise FB, which lowers the draw.
- *Fix:* define the owner state as the financing need *before* fund transfers (or use the adjusted non-hydrocarbon primary balance), and define P^BE on the same basis. This also bears on the "effective breakeven" elicitation in exec-summary item 5.

**5. [Medium] "Buy joint-state hybrids now" is unsupported (§1.8(v), §4.9, §6.11.3).**
- *The problems:*
  - The recommendation rests on *realised, P-measure* correlation: rolling 36m −0.28 and war months −0.58 with n = 6 (95% CI −0.95 to +0.44). Dealer-implied correlation was not observed.
  - The priced structure pays only if oil is below 80% *at expiry*: a terminal-conditional put, not the "knock-in" the exec summary describes. A barrier knock-in would cost more.
  - The bivariate GBM has no correlation skew.
  - The text compares dealer "correlation marks" with a "DB probability", which are different objects.
- *Fix:* get dealer quotes, and compare Q-implied joint-down probabilities with risk-premium-adjusted P-probabilities from the Z_t posterior.

**6. [Medium] Calibration targets are treated as precise when they are not (§6.12 "must reproduce").**
- *How thin the evidence is:*
  - Tail dependence 0.08 → 0.30 rests on 2/24 vs 7/23 joint months (Fisher p ≈ 0.07).
  - The 26% conditional probability is 14 of 54 overlapping months, 11 of them from the GFC. The pre/post-2008 split is effectively "GFC vs not".
  - "Only 2008 had falling equities" depends on 2015 being +0.2%.
- *Specification problem:* §6.4 is a time-homogeneous annual Markov mixture. It cannot reproduce three era-specific *monthly* correlations without breaks or era states.
- *Fix:* express targets as intervals with effective n, and model era explicitly.

**7. [Medium-low] The DCR and override-reserve constructions are inconsistent (§6.8).**
- *DCR:*
  - It mixes conditional-mean inflows (E[PE dist], E[hedge payoff]) with P99 margin outflows.
  - It counts committed facilities at face value despite the counterparty wrong-way risk (WWR) flagged in §8.
  - Hedge payoffs and overlay margin may net within the same CSA.
- *Override reserve:* p^ov × E[u] × NAV is an expected-loss reserve. In GW that is ≈US$0.12bn, against an event costing US$3.5–8.9bn (2–5% of NAV above the cap).
- *Fix:*
  - stress the inflows (for example at P10);
  - haircut facilities for counterparty risk;
  - size the override buffer to the event at the constraint's confidence level, or fold it into the chance constraint.

**8. [Low-medium] The illustrative [I-MC] outputs omit specified components.**
- *What is missing:* the draw run excludes the band override, the PS overlay, the ET drift, the declining h_t path (11.3% → 9.1%) and jumps. Only jumps are disclosed. The headline "≈1% → 10–15%" should carry this scope.
- *Transition prior:* the stationary shares (DB 7%, N 49%) miss the dossier's own calibration target #4 (DB 4.1%, N 59.6%).

**9. [Low] Some peer evidence is mischaracterised.**
- SAMA→PIF (US$40bn, 2020) was a reserve reallocation to fund opportunistic investment, not a fiscal draw on a fund.
- The Saudi 2026 deficit of −6.5% is only 0.7pp worse than 2025 (−5.8%), so it is weak support for "oil up but fiscally negative".
- w_GW = −6pp is calibrated from a single *projected* year (WEO Oct 2026). That year includes the Mar–Jul UAE volume loss, which EIA now puts at zero for Aug–Sep.
- §6.12 target #7 lists the 2025→26 projection as if it were a realised swing.

**10. [Low] Formula, unit and tagging slips.**
- **Murban basis units.** β^M is specified in US$/bbl but enters as e^{β^M} in the HR equation (§6.5). It should be additive, or a log basis.
- **Tagging.** ψ₁ ≈ 0.3 is tagged [S: IMF], but the IMF supports only the sign.
- **Double count.** λ_H·premia double-counts premia already in ΔW, unless it is intended as a governance penalty.
- **Notation.** β is overloaded: discount factor, owner beta, Murban basis and distribution beta.
- **Buffer-release value.** It uses μ_illiq − r_cash with no risk adjustment.
- **Arithmetic.** "DB→SG→SG ≈ US$50–60bn" against the dossier's own table sum of ≈US$46.7bn.

**11. [Low] The SDDP tractability claim (§7) omits the convexity requirement.**
- The smoothed draw rate (a continuous state) × NAV is bilinear.
- Clip binaries and chance constraints are non-convex.
- Standard SDDP cuts are therefore invalid unless the oil and draw states are discretised into the Markov chain, or SDDiP/Lagrangian cuts are used.

**12. [Low] Reproducibility hygiene.** Input data are not archived, and the stored JSONs mix script versions (see §3).

**What the dossier gets right** (worth keeping):
- honest [U] / [I] tagging;
- it catches the Bodie–Brière expenditure-vs-receipts inconsistency;
- it correctly reports EIA's downward revision of UAE shut-ins;
- the structural point that shock *type* (SG vs DB vs GW), not the oil level, drives liability wrong-way risk is supported by the evidence (Bernanke, Kilian, Baumeister–Hamilton, Ready).

---

## 6. Overall reliability rating

**High for evidence; medium for design inferences.**

**Evidence.** Facts, sources and computations are reliable:
- 32 claims checked: 28 confirmed, 4 corrected (all minor or scoping), 0 refuted, 0 unverifiable;
- 18 of 18 citations correct;
- all scripts reproduce exactly from fresh public data.

**Design inferences.** Before this stream feeds IC material, revise the following:
- exec-summary items 1 (sensitivity and hedge size), 4 ("near the cap") and 8(v) ("buy hybrids now");
- §5 issues 3, 4 and 7 (kinks, fiscal-state definition and DCR).

---

## 7. Method and limits

**Tools.** Primary documents were fetched directly: the IMF Article IV PDFs, DataMapper API, EIA STEO PDFs (text-extracted), the EIA RBRTE HTML, Amundi, ERF and IMF working-paper PDFs, and AEA pages. Crossref was used for DOIs.

**Rate limits.** The IMF site and Crossref returned HTTP 429 intermittently; retries succeeded.

**Paywalled sources.**
- Bloomberg (4 Feb 2026): only the headline and summary were read.
- AGBI (Dec 2025): HTTP 403. A search snippet attributes "≈65% of ADIC's assets in private markets" to it. If confirmed, that would be a public source broadly consistent with the client's ~60% private, which the dossier says has none. Treat it as an unverified lead.

**Not checked** (not load-bearing for this stream):
- NBIM inflow series and the NOK 22,683bn value;
- Alaska ANS prices and SB 26 details (covered by Stream 02);
- Mubadala, L'imad and ADQ AUM;
- the Jawlah US$15bn hedge-fund plan. A Finance Middle East headline ("ADIC considers $15B bet in hedge funds") corroborates it, but was not opened.

---

## Citation corrections (2026-10-18)

- Erratum to §4 #13 and §2 A3 (Moutanabbir & Noureldin): the literature audit (`research/literature/00_LITERATURE_SYNTHESIS.md` §2.3) classes ERF WP 1172 (2018) as superseded by Moutanabbir, K. & Noureldin, D. (2020), *International Review of Economics & Finance* 69:708–730, DOI 10.1016/j.iref.2020.06.014 (Crossref). A3's figures (1976–2016 sample, negative equity–oil-income correlation, 0.01–0.07pp hedging demand) were confirmed against the WP only [unverified in the journal version: its abstract gives none of them, and the full text is paywalled].
