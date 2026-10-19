# Verification log: Stream 02, endowment model, distribution policy, SWF peer practice and TPA

**Dossier checked:** `research/dossiers/02_endowment_swf.md` (as of 18 Oct 2026; not edited).
**Verified:** 2026-10-18.
**Role:** adversarial fact-check before Investment Committee (IC) use.

---

## 1. Summary

**Result: 27 claims checked: 17 confirmed, 9 corrected, 0 refuted, 1 unverifiable.**

**The empirical base is strong.** These match their primary sources exactly:
- Yale, Alaska, Norway and Singapore rules;
- DWY tables (34.48% / 5.32% / 27.78% / ~2% CE / 60.24% at α=3%);
- the Dybvig quotes;
- Brown et al.;
- NACUBO FY2025;
- Bain 2026;
- Harvard FY2026;
- CPP, GIC and NBIM headline figures;
- the CFA TPA guide quotes.

No citation is hallucinated. The dossier's own Monte Carlo reproduces: an independent re-simulation and an analytic check both match it within simulation noise.

**Corrections that matter for IC material:**
1. **Kuwait 2020.** The 10% FGF transfer was *temporarily halted / made contingent on a budget surplus*, not "removed".
2. **Ennis.** The −1.1% to −1.8% alphas (t −2.7 to −4.9) are for *six size cohorts*, not the 43 endowments. The −1.87% comes from a later (2021) paper.
3. **Harvard 2008–09.** The cited article gives a *projected* 30% decline and "$24 billion or so". It does not contain −27.3% / $26bn, "taxable" bonds or a ~$500m swap payment.
4. **CPP.** The 13.2% is the *benchmark portfolios'* return, not a "reference portfolio" return.
5. **Stanford.** The 70/30 / 5.5% / 4–6% rule is stale. Since October 2021 it is 80/20, a 5.25% target and 4.25–6.25% boundaries.
6. **Minor fixes:**
   - NBIM's 2024 inflow is NOK 409bn, not 411bn.
   - ADIA's ranges were *shifted*, not widened or narrowed.
   - NZ Super's "since 2010 8.65% vs 10.09%" is not in the cited pages. The 20-year figures are 9.68% vs 8.19%.
   - Yale's "up to 15%" discount is not in the cited source.

**The design layer carries the real risk.** Five problems would change what the IC sees:
1. **The §6.4 objective is ill-defined.** Additive habit h=0.8 with CRRA γ=2 has a non-positive argument whenever real distributions fall by more than 20%. Under the dossier's own return model that happens on roughly 75–78% of 20-year paths for fixed-% rules.
2. **Forced-sale probabilities are an artifact of the 25% liquidity floor.** The author's own 15% floor runs give 0.2% (base) and 10.9% (drought) at a 7.5% payout, against the headline 4.8% and 60.4%. The headline also reports frequency, not severity: mean cumulative discount loss is 0.03–0.64% of NAV₀. A chance constraint on "any forced sale" can be satisfied by lowering the floor.
3. **The DWY result is over-extended.**
   - The α=3% → 60% result has no spending floor.
   - The floor case is reported only at α=2%.
   - DWY's α includes the illiquidity premium.
   - The ~2% CE cost of a 5.2% floor is not a valid "value of mandate flexibility" for a 5–10% band, nor a calibration target.
4. **Shadow prices.** The proposed CMA-ES/Optuna policy search yields no multipliers, so "shadow prices" need a stated estimation method.
5. **The default constraints are infeasible at a 7.5% payout under the dossier's own base case.** P(private share >70%) is 23.7%, above the 10% ceiling. Median real NAV₁₀ is 0.78, so the IG constraint fails.

**Overall reliability: MEDIUM.** It is high for sourced facts and citations, and medium for the design implications in §1.4, §2.4, §3.3, §6.3, §6.4 and §6.6. Fix those before anything reaches an IC pack.

---

## 2. Method

- **Direct primary fetches:**
  - Yale Policy 2202; APFC FY26 release and APFC glossary;
  - Singapore MOF NIRC page; NBER w25559 page; AEA (Brown et al.);
  - NACUBO FY25 release; Bain GPER 2026;
  - Gulf News (19 and 23 Aug 2020); Harvard Magazine (Jul 2009; 15 Oct 2026);
  - CPP FY2026 release; Morningstar DBRS (3 Jul 2025);
  - GIC (24 Jul 2026); NBIM AR2025 web report;
  - HedgeFundAlpha/Swedroe; Institutional Investor (1 Apr 2021);
  - Stanford Fingate; Foley; ADIA Review 2025; NZ Super pages;
  - PE Wire (Yale 2025); Pension Pulse (CPP TPA engine).
- **PDFs decoded locally.** WebFetch could not read their compressed streams, so a C# text extractor (Flate/LZW/ToUnicode) read:
  - the Dybvig 1998 draft;
  - DWY NBER WP 25559 (rev. Nov 2022);
  - the CFA Institute TPA guide (Jul 2026);
  - the CAIA "From Vision to Execution" report (Oct 2025);
  - S&P on CPPIB (20 Jan 2025);
  - the Gilbert–Hrdlicka white paper (2017).
- **Search budget.** The session's shared web-search cap was exhausted partway through. After that I used only direct fetches of primary or cited pages.
- **Blocked sites.** These blocked the fetcher, and the affected items are marked:
  - regjeringen.no (direct fetch; its text was confirmed via search results before the cap);
  - temasek.com.sg, akleg.gov, SSRN, top1000funds.com, harvardmagazine.com/breaking-news (403);
  - investments.yale.edu 2009 PDF and the MOF Budget 2025 PDF (404);
  - dash.harvard.edu (429);
  - cbk.gov.kw Fitch PDF (socket closed).
- **Monte Carlo re-check.**
  - Read the author's raw outputs (`spendsim_T20_v2.md`, `sweep_T20.md`) and checked every transcribed cell of dossier Tables 1–3.
  - Recomputed the mixture moments analytically and P(20-year annualized ≥10%) by conditioning on the number of crisis years.
  - Re-simulated Cases A and B independently (100k paths, C#).

---

## 3. Claims table

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | **Yale rule:** 80% prior spending + 20% × 5.25% × prior-year beginning MV, inflation-adjusted, 4.0–6.5% band; effective 1 Mar 2023, revised 1 Jul 2026 | Confirmed | Exact. The inflation adjustment applies to the *sum*, and the band is measured on fair value at the start of the prior year. The dossier's R5 inflates only the λ term and clips to 5–10% of $W_t$. That is fine as an ADIC analogue but is not Yale's literal rule. | https://your.yale.edu/policies-procedures/2202-endowment-spending-and-distributions |
| 2 | **Alaska:** POMV 5% of avg MV, first 5 of preceding 6 FYs; FY26 draw $3.8bn; $4.0bn for FY27; $91.9bn; 12.42%; $1.5bn inflation-proofing skipped for lack of appropriation | Confirmed | All figures match APFC (2 Sep 2026): "12.42% net of fees", "$91.9 billion", "$3.8 billion", "$4.0 billion commitment", no FY26 inflation-proofing transfer (est. $1.5bn) "Given the lack of appropriation". APFC's glossary confirms the "first five of the preceding six fiscal years" basis under AS 37.13.140(b). The 5% rate is not stated on the APFC pages fetched (statute site 403) but is consistent with the draws. | https://apfc.org/fund-news/fy26-audit-and-budget-proposal/ ; https://apfc.org/terms-and-acronyms/ |
| 3 | **Norway:** fiscal rule ties spending to the expected real return; cut from 4% to 3% in Feb 2017 with a 70% equity share | Confirmed | Ministry release and speech of 16 Feb 2017: the estimate was cut from 4% (in place since 2001) to 3%, the equity share was raised to 70%, and the rule itself was unchanged. Feb 2017 was the announcement and proposal, adopted in spring 2017. The direct fetch returned 403; the page text was confirmed via search results. | https://www.regjeringen.no/en/aktuelt/increased-equity-share-in-the-government-pension-fund-global-and-adjustment-to-the-expected-rate-of-return-in-the-fiscal-policy-guidelines/id2539303/ |
| 4 | **Singapore NIRC:** up to 50% of NIR on net assets of GIC, MAS and Temasek, on expected long-term real returns with presidential concurrence, since 2008 | Confirmed (nuance) | Correct as stated: ELTRRORs with the President's concurrence after consulting the CPA; net of government liabilities; NIR framework from 2008. **Nuance:** the NIRC also includes up to 50% of NII on the remaining assets (framework from 2001), which is *realized* income. "Singapore spends from expected, not realized, returns" (§1.7, §2.7) is true only of the NIR part. FY2025 NIRC of S$27.14bn is unverified (MOF PDF 404). | https://www.mof.gov.sg/policies/reserves/net-investment-returns-contribution/ |
| 5 | **DWY (NBER):** α=2% gives 34.5% alternatives and 5.32% spending; a 5.2% floor cuts alternatives to 27.8% and costs ~2% CE; ~60% alternatives needs ~3% α | Confirmed | Table 6: α=1% gives 12.69%; α=2% gives 53.93/11.59/34.48, band (27.47, 64.94), spending 5.32%; α=3% gives 60.24%, band (51.02, 88.50), spending 5.60%. Table 9: a 5.2% floor gives 27.78% and 5.30%. Text: "approximately 2% of the investor's certainty equivalent wealth". Calibration (γ=2, ψ=0.5, r=4%, ε=15%, ρ=0.625, δ=4%) and crisis liquidation cost 0.25 vs 0.10 also confirmed. **Caveat:** DWY's α "includes the risk premium and illiquidity premium" (see §5 R3). | https://www.nber.org/papers/w25559 |
| 6 | **Dybvig:** hold spending/riskless rate in safe assets; at 5%, max perpetual spending is $5m per $100m; a 5%/yr decline gives protection that "is not worth much" | Confirmed | Draft of 30 Oct 1998, Table 1: risky holding $K(w-s/r)$, spending raised only to keep $s\ge \underline r w$. Page 7: "$100 million ... 5% ... $5 million per year". Fig. 7 caption: decline limited to 5%/yr, "the protection is not worth much". | https://phildybvig.com/research/papers/ratchet2p.pdf |
| 7 | **Brown et al.:** endowments cut payouts below policy after negative shocks but not after positive ones ("hoarding") | Confirmed | Abstract: "actively reduce payouts relative to their stated payout policies following negative, but not positive, shocks", consistent with "endowment hoarding". It also covers the president-tenure benchmark and personnel cuts. | https://www.aeaweb.org/articles?id=10.1257/aer.104.3.931 |
| 8 | **NACUBO FY2025:** 10.9% 1-yr, 7.7% 10-yr, 4.9% spending, 62.5% alternatives and 11.8% for >$5bn, 15.2% of budgets | Confirmed | Exact (12 Feb 2026; 657 institutions; $944.3bn; private 5.4%, public 4.1%; $33.4bn; largest cohorts 18–19%; >$5bn 8.2% fixed income). | https://www.nacubo.org/Press-Releases/2026/US-Higher-Education-Endowments-Report-Stable-Returns-Increase-Spending-to-33-4-Billion-in-FY25 |
| 9 | **Bain:** PE distributions ~14% of NAV in the 12 months to Q3 2025, unseen since 2008–09, below 15% for four years; 32,000 companies worth $3.8tn | Confirmed | Exact: "essentially flat at 14%" (Q4'24–Q3'25), "four years running—an industry record". Also confirmed: exits $717bn (+47%), CVs +62%, holds ~7 years. **Note:** this is an industry buyout ratio, not an ADIC statistic. | https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ |
| 10 | **Kuwait 2020:** KD2bn Treasury liquidity vs KD1.7bn/month GRF draw; automatic 10% FGF transfer *removed*; FGF not drawable without parliament | **Corrected** | KD2bn and KD1.7bn/month are confirmed (19 Aug 2020). Parliament voted to "**temporarily halt**" the 10% transfer in deficit years; the 23 Aug 2020 article says future transfers would be "contingent on a budget surplus". It was not removed. The FGF needing legislation is supported only by Bloomberg reporting seen in search results. Fitch's "imminent depletion" language is from **Feb 2021**. "FGF ≈400% of GDP" is unverified. | https://gulfnews.com/world/gulf/kuwait/kuwait-cant-pay-salaries-beyond-october-minister-tells-parliament-1.1597852565530 ; https://gulfnews.com/business/banking/kuwait-to-transfer-2b-dinars-to-general-reserve-fund-1.73368385 |
| 11 | **Harvard 2008–09:** $36.9bn to ~$26bn (−27.3%); $2.5bn (taxable) bonds Dec 2008; ~$500m swap termination; $11bn unfunded | **Corrected (citation)** | The cited article has $36.9bn, a "projected 30 percent decline", an endowment "now worth $24 billion or so", "$2.5 billion in borrowings last December" (not described as taxable), swap collateral calls with "potential losses in the hundreds of millions", and $11bn of commitments "through 2018". It contains **no** −27.3%, $26bn or ~$500m figure; those need Harvard's FY2009 report, which was not fetched here. "56% of FAS income" refers to "the year just ended" from a mid-2009 vantage, so the year is ambiguous. | https://www.harvardmagazine.com/2009/07/liquidity-leverage |
| 12 | **Harvard FY2026:** 27.1%, $68bn, $2.6bn (~39–40% of revenue); tax 1.4%→8% (~$300m/yr); FY27 distribution flat; CA 15.5% | Confirmed | Exact (15 Oct 2026). Also confirmed: 5% distribution rate, 8% return objective, Stanford 31.7%, MIT 10.3%. | https://www.harvardmagazine.com/university-finances/harvard-endowment-financial-report-fiscal-year-2026 |
| 13 | **CPP:** FY2026 7.8% (10-yr 8.8%), C$793.3bn; "reference portfolio" returned 13.2% | **Corrected (label)** | 7.8%, 8.8% and $793.3bn are confirmed (20 May 2026). The 13.2% is the "**benchmark portfolios'** fiscal 2026 return ... exceeded the Fund's net return of 7.8% by 5.4%". Reference portfolios were relabelled market risk targets in FY2025, so the dossier's label contradicts its own §5. | https://www.newswire.ca/news-releases/cpp-investments-net-assets-total-793-3-billion-at-2026-fiscal-year-end-814459989.html |
| 14 | **CPP leverage:** recourse debt 9.7% of adjusted net assets (FY2025); relabelled "market risk targets"; S&P cites a 45% board limit | Confirmed | From DBRS (3 Jul 2025): C$76.6bn = 9.7%; investment liabilities C$222.5bn (31 Mar 2025); FY2025 relabelling. **The 45% is not in DBRS.** It is in S&P (20 Jan 2025): "recourse leverage limit of 45% of net assets, starting in fiscal 2023". | https://dbrs.morningstar.com/research/457796/morningstar-dbrs-confirms-cpp-investments-at-aaa-and-cppib-capital-inc-at-aaa-and-r-1-high-stable-trends ; https://www.cppinvestments.com/wp-content/uploads/2025/04/SP-RatingsDirect_CPPIB_3310933_Jan-20-2025.pdf |
| 15 | **GIC:** 20-yr 5.6% USD nominal / 3.4% real to 31 Mar 2026; new Strategic Portfolio (equities, fixed income, real assets) | Confirmed | Exact (24 Jul 2026). Real return is "the primary metric". The GIC Portfolio aims to beat the SP "within approved risk parameters". | https://www.gic.com.sg/newsroom/all/gic-delivers-steady-long-term-returns-within-its-mandate-and-stays-focused-on-portfolio-resilience-in-a-structurally-changed-world/ |
| 16 | **NBIM:** 6.64% / 4.34% real since 1998; 15.1% in 2025; inflows with no withdrawals 2024–25; TE 1.25pp; unlisted RE ≤7% | **Corrected (minor)** | All confirmed except the 2024 inflow: AR2025 Table 1 gives **NOK 409bn** (2025: NOK 327bn), not 411bn. Unlisted renewable infrastructure ≤2% and NOK 21,268bn also confirmed. | https://www.nbim.no/en/news-and-insights/reports/2025/annual-report-2025/web-report-annual-report-2025/ |
| 17 | **Ennis:** 43 large endowments FY2009–19 had alphas of −1.1% to −1.8% (t −2.7 to −4.9); large endowments trailed passive by 1.87%/yr over 12 years to June 2020 | **Corrected** | The alpha range and t-stats are for "**six cohorts of fund size**". For the 43 largest endowments, "None ... outperformed with statistical significance" and "one in four underperformed with statistical significance". The −1.87% (endowments >$1bn) comes from Ennis's later "third and concluding paper" (II, Apr 2021), worded "over the 12 years" with no explicit "per year". Costs of 1–2% of assets are confirmed. [2026-10-18: the later paper is probably Ennis (2021), "Failure of the Endowment Model", *JPM* 47(5):128–143, DOI 10.3905/jpm.2021.1.217. This is inferred, because II does not name it. The dossier now cites it separately.] | https://hedgefundalpha.com/strategies/the-enduring-futility-of-the-endowment-model/ ; https://www.institutionalinvestor.com/article/2bswtbayp11p67nyfj3ls/portfolio/its-time-to-replace-the-grossly-inefficient-endowment-model-says-richard-ennis |
| 18 | **TPA:** the reference portfolio is "not intended as a benchmark to be closely tracked", with TE ~4–5%/yr; mature TPA replaces funding-asset mapping with opportunity cost | Confirmed | Urwin & Hayman (CFA RPC, Jul 2026), p. 20: exact quote; "tracking error typically around 4%–5% per year". The funding-to-opportunity-cost point is from the **CAIA** report (Filbeck & Bok, Oct 2025): "TPA decouples the concept of 'funding' ... focuses on opportunity cost and portfolio improvement". | https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/fti_tpa-report_online.pdf ; https://www.thinkingaheadinstitute.org/content/uploads/2025/10/2025-TPA-Report-from-Vision-to-Execution.pdf |
| 19 | **Own MC:** P(20y ≥10%) = 42.2%; median real NAV₂₀ 0.78 (A) / 0.53 (B) at 7.5%; forced sale 4.8% base / 60.4% drought | Confirmed (as computed) | Every checked cell matches the raw outputs. Case A mixture moments: mean 10.00%, SD 12.00%. Analytic P(≥10%) is 42.3%. Independent re-sim: 42.0–42.6%, 0.783 (A), 0.537 (B), P(<NAV₀) 68.1% / 89.4%. **Caveat:** forced-sale figures assume a 25% floor; the author's 15% floor runs give 0.2% and 10.9% (see R2). | `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\sim\sweep_T20.md` ; `...\scratchpad\sim\spendsim_T20_v2.md` |
| 20 | **Stanford** 2020 rule: 70/30, 5.5%, 4–6% | **Corrected** | The current rule ("effective October 2021") is 80% prior payout + 20% × (5.25% × 31 Dec value) + a 4% growth factor. Below 4.25% and above 6.25% the rule switches to fixed 4.75% / 5.75% formulas. The 2020 parameters were not verified; use the current ones as the peer analogue. | https://fingate.stanford.edu/managing-funds/endowment-payout-process |
| 21 | **Endowment excise tax:** tiers 1.4% / 4% / 8%, tax years after 31 Dec 2025, ≥3,000 tuition-paying students | Confirmed | 1.4% ($500k–$750k per student), 4% ($750k–$2m), 8% (>$2m). Effective 1 Jan 2026. The student threshold rises from 500 to 3,000. | https://www.foley.com/insights/publications/2025/07/changes-to-the-college-and-university-endowment-tax/ |
| 22 | **ADIA 2025:** "widened" PE to 15–20% and FA to 7–12%; "narrowed" RE to 2–7% | **Corrected (wording)** | PE was "increased from 12%-17% to 15%-20%", FA "from 5%-10% to 7%-12%", RE "declined from 5%-10% to 2%-7%". The ranges were **shifted**, and each is still 5pp wide. | https://www.adia.ae/en/pr/2025a/index.html |
| 23 | **NZ Super:** FY2026 14.17%, NZ$94.4bn; Reference Portfolio since 2010 8.65% vs actual 10.09%; 2026 review cut value-add from 1.0% to 0.9% | **Corrected** | 14.17% and $94.4bn are confirmed (16 Sep 2026; the Fund lagged the RP by 0.1pp in FY26). The verifiable long-run figures are **20-year 9.68% vs Reference Portfolio 8.19%**; the since-2010 pair is not on the cited pages. The value-add cut is unverified (top1000funds 403). RP composition (75% global equities, 5% NZ equities, 20% fixed income; 100% NZD-hedged) is confirmed. | https://nzsuperfund.nz/news-and-media/strong-all-round-performance-sees-super-fund-grow-by-9-3-billion/ ; https://nzsuperfund.nz/how-we-invest/reference-portfolio/ |
| 24 | **Temasek:** S$518bn; 20-yr TSR 6.8% S$ / 8.0% USD; 10-yr 7.5% USD | Unverifiable | temasek.com.sg returned 403. Treat these as unverified in the peer table. | https://www.temasek.com.sg/en/news-and-resources/news-room/news/2026/temasek-net-portfolio-value-grows-to-518b-up-49b-from-last-year |
| 25 | **CPP TPA engine:** five pillars; leverage as a "balance sheet risk stabiliser"; multi-horizon LCRs; public and private "compete explicitly on a common risk-adjusted basis"; same test for resizing or selling | Confirmed (secondary) | All quoted from the CPP paper (Shen, Walker, Rubin) via Top1000funds and Pension Pulse. "Applies to both new and existing investments" is a quote; the resize/sell-down equivalence is the **journalist's paraphrase**. The balancing portfolio followed the 2016 institutionalisation; no separate date is given. | https://pensionpulse.blogspot.com/2026/05/inside-cpp-investments-tpa-engine.html |
| 26 | **TPA adopters +1.3% p.a.** | Confirmed | The CFA guide (p. 28) cites the Thinking Ahead Institute (2025c): "1.3% per year better than SAA adopters in a 10-year, 26-fund study". It flags confounders itself (size, mandates, high alternatives exposure). | https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/fti_tpa-report_online.pdf |
| 27 | **Yale 2025 secondary:** up to ~$2.5bn; discount below 10%, up to 15% on parts | **Corrected (partial)** | "valued at up to $2.5bn", "discount of less than 10% to net asset value", pending as of 5 Jun 2025. **No "up to 15%"** in the cited source. | https://www.privateequitywire.co.uk/yale-nears-2-5bn-secondary-sale-of-pe-and-vc-stakes/ |

---

## 4. Citation check (12 most important references)

| Ref | As cited | Result |
|---|---|---|
| Tobin (1974) | *AER* 64(2):427–432 | **Correct** ("What Is Permanent Endowment Income?"). |
| Merton (1993) | Chapter in Clotfelter & Rothschild (eds.), *Studies of Supply and Demand in Higher Education*, U. Chicago Press; NBER c6102, WP 3820 | **Correct** (Chapter 7). WP number not re-checked. [2026-10-18: ch. 7, pp. 211–242 confirmed from the NBER chapter PDF cover; NBER WP 3820 (Aug 1991) confirmed on the NBER chapter page. Dossier reference completed.] |
| Dybvig (1999) | *FAJ* 55(1):49–62 | **Correct.** The 30 Oct 1998 draft's quotes are verified. |
| Dybvig (1995) | *RES* 62(2):287–313 (marked "unverified") | **Correct** (DOI 10.2307/2297806). Can be upgraded to verified. [2026-10-18: upgraded in the dossier, with the full title.] |
| Dimmock, Wang & Yang (2024) | *Management Science* 70(3):1554–1579; NBER WP 25559 | **Correct** (DOI 10.1287/mnsc.2023.4759; WP Feb 2019, rev. Nov 2022). |
| Gilbert & Hrdlicka (2015) | *RFS*, doi:10.1093/rfs/hhv031; white paper 12 Nov 2017 | **Correct** ("Why Are University Endowments Large and Risky?", *RFS* 28(9)). The white-paper quote "universities need cash in recessions just as everyone else does" and the 7% UPMIFA passage are verified. |
| Brown, Dimmock, Kang & Weisbenner (2014) | *AER* 104(3):931–62 | **Correct.** |
| Campbell (2012) | *Forum Futures 2012* (DASH) | **Not checked** (DASH HTTP 429). The "immortality vs vigor" characterization is unverified. |
| Cejnek, Franz, Randl & Stoughton (2014) | *JOIM* 12(3):90–117 | **Title, authors, volume and issue correct.** Pages and the "least developed areas" claim are behind a login and were not checked. |
| Ennis (2020), SSRN 3614875 | One reference for both the FY2009–19 alphas and the −1.87% | **Garbled.** The 2020 study "Endowment Performance" exists per Swedroe, but the SSRN ID was not checked (403). The −1.87% is from Ennis's later 2021 paper (II, 1 Apr 2021). Split into two references. [2026-10-18: OpenAlex confirms SSRN 3614875 as Ennis's 2020 working paper "Endowment Performance and the Demise of the Multi-Asset-Class Model". It was published as Ennis (2021), "Endowment Performance", *J. Investing* 30(3):6–20, DOI 10.3905/joi.2021.1.166. The later paper is probably Ennis (2021), "Failure of the Endowment Model", *JPM* 47(5):128–143, DOI 10.3905/jpm.2021.1.217 (inferred). The dossier's ref 10 is now split into (a) and (b).] |
| Urwin & Hayman (2026) | CFA Institute RPC, *The Total Portfolio Approach (TPA): A Practical Guide ...*, Jul 2026 | **Correct.** The reference omits the authors. [2026-10-18: OpenAlex confirms the authors as Roger Urwin and Genevieve Hayman, published 28 Jul 2026, DOI 10.56227/26.1.20. The audit's "Urwin et al." reflects index truncation. Dossier reference corrected.] |
| Filbeck & Bok (2025) | CAIA, *From Vision to Execution*, Oct 2025 | **Correct.** The four dimensions, exemplar funds, Urwin quote, GIC overlay passage and Future Fund PE/VC/infrastructure tilt are all verified. |

**Other source-use problems:**
- Harvard Magazine (Jul 2009) is cited for numbers it does not contain (claim 11).
- The Stanford reference is a stale primary (claim 20).
- The flagged CPP claim cites DBRS for the 45% limit, which is in S&P (claim 14).

---

## 5. Reasoning issues and overclaims

**R1. HIGH. §6.4: the objective function is ill-defined.**
- The issue: $u(D^{real}_t-hD^{real}_{t-1})$ with CRRA γ=2 and h=0.8 needs $D_t>0.8D_{t-1}$ in every period.
- For a fixed-% rule, $D_t/D_{t-1}=(1-d)(1+R_t)/(1+\pi_t)$. At d=7.5% the argument turns non-positive when $\ln(1+R)<-0.12$.
- Under the dossier's own mixture that has probability ≈0.89 in a crisis year (8%/yr). That is ≈7.2% per year, or **≈78% of 20-year paths** (≈75% at d=5%).
- The objective therefore cannot rank the baseline rules it is meant to rank. The 88–98% "P(real cut >10%)" in Table 1 is consistent with this.
- **Fix:** use a ratio habit $u(D_t/D_{t-1}^{h})$, or a lower h with a subsistence floor. Alternatively, treat $D_t\le hD_{t-1}$ as a reported constraint violation.

**R2. HIGH (IC-facing). §1.4, §3.3 Table 3, §6.3: forced-sale probabilities are assumption artifacts.**
- **Floor sensitivity.** The headline numbers depend on the 25% liquidity floor. The author's own 15% floor runs (`spendsim_T20_v2.md`) give, against the 25% floor:

  | Case | 15% floor | 25% floor |
  |---|---|---|
  | 7.5% payout, base | 0.2% | 4.8% |
  | 7.5% payout, drought | 10.9% | 60.4% |
  | Yale-type, base | 2.5% | 15.6% |
  | Yale-type, drought | 33.6% | 67.2% |
  | 10% payout, drought | 99.0% | 100% |

  The dossier does not disclose this.
- **Circular definition.** A "forced sale" is a breach of a self-imposed floor. The chance constraint P(forced sale) ≤ 5% (§6.3) can therefore be met by lowering the floor.
- **Frequency is not severity.** Mean cumulative discount loss is 0.03% of NAV₀ (base, 7.5%) and 0.64% (drought, 7.5%) over 10 years. An IC reading "60%" will overweight it.
- **Fix:**
  - show a floor sweep (10/15/20/25%);
  - define the liquidity event against an *external* hard constraint (missed owner payment, unmet call or margin);
  - report E[loss] and CVaR of sale losses alongside frequency.

**R3. MEDIUM. §2.4, §1.6, §2.7, §6.6: DWY is over-extended.**
- **The 3% α is a lower bound, not a threshold.** "~60% private plus a hard 5% floor is consistent with DWY only if α ≥ ~3%" does not follow.
  - DWY's 60.24% at α=3% has **no** spending floor, with optimal spending of 5.60%.
  - The floor case is reported only at α=2%, where it cuts alternatives by a fifth.
  - DWY note the floor binds in high-alternatives states, so the α needed with a floor is above 3% and unknown.
- **ADIC's likely demand is far above DWY's optimum.** An owner demand near 7.5% is well above DWY's optimal 5.3–5.6%.
- **DWY's α is not skill.** It "includes the risk premium and illiquidity premium". Compare it with PME or direct-alpha excess returns, not with GP skill.
- **The ~2% CE figure is a category error in two places.** Using it as the "value of mandate flexibility" for a 5–10% band, or as a calibration target tagged [S], misuses it. It is a model output for a floor 0.12pp below optimal spending.
- **Fix:** re-solve a DWY-type model at ADIC parameters, or label 3% explicitly as a lower bound.

**R4. MEDIUM. §1.6, §3.5, §6.2–6.3: shadow prices without a method.**
- Policy search over θ (CMA-ES or Optuna through a non-convex simulator, §7) produces no Lagrange multipliers.
- "Report the shadow price of the floor and cap" and "$u_t$ ... whose multipliers are reported" need a defined estimator. Options:
  - finite-difference re-optimization across constraint levels, with common random numbers and confidence intervals;
  - or duals taken only from the convex cvxpy / pyomo sub-problems.
- Shadow prices on chance constraints are noisy and must carry standard errors.

**R5. MEDIUM. §6.3: default constraints are infeasible under the dossier's own base case at a 7.5% payout.**
- P(private share >70% ever) is 23.7%, against a ceiling of ≤10%.
- Median real NAV₁₀ is 0.78, so P($W^{real}_{10}<0.8W_0$) is above 50%, against ε_IG = 20%.
- Only the 5% payout meets both (5.0%; median 1.02).
- The framework must detect and report infeasibility, through soft constraints with penalties or an explicit owner-endorsed decumulation path. It should not let the optimizer silently gravitate to the floor.

**R6. LOW–MEDIUM. §3.4: the NACUBO cross-check is mis-specified.**
- The 4.8% break-even uses π=2.5%.
- Realized US CPI-U over June 2015 to June 2025 averaged about 3.1% a year (my estimate from index levels; not re-fetched). That gives a break-even of about 1−1.031/1.077 ≈ 4.3%, below the 4.9% spending rate.
- US endowments also receive gifts, which ADIC lacks.
- The cross-check does not validate the arithmetic; if anything it shows spending above break-even, sustained by gifts.

**R7. LOW. §3.1 R6: the formula does not match its label.**
- $\frac15\sum_{k=1}^{5}W_{t-k}$ averages the five *most recent* years.
- "First 5 of prior 6" means $k=2..6$, and the statute's "including the fiscal year just ended" timing lengthens the lag further.
- Confirm that the simulator and the documented equation agree.

**R8. LOW. §2.7, §3.1 R12: "exactly the LQ family" is overstated.**
- $r^*_tW_t=(r_0+\kappa(F_t-1))W_t$ is bilinear in $(F_t,W_t)$ and clipped.
- It is linear only after linearizing around F=1. The text hedges this, but the table label "LQ-optimal form" should read "linearized LQ form".

**R9. LOW. §3.1 R8: the "Dybvig-type [S]" label is misleading.**
- The capped ratchet has no protective allocation.
- Its 10%·$W_t$ cap breaks the no-decline property.
- Dybvig's protection comes from holding $s/r$ in riskless assets. Relabel it "ratchet heuristic [I]".

**R10. LOW. §1.3, §2.1: "constant payout removes sequence risk" is too strong.**
- That is true for terminal NAV only.
- Under a fixed-% rule the payout stream, and therefore cumulative distributions, still depend on return order: an early crash lowers every later payout.

**R11. LOW. §6.6: assumptions are tagged as sourced calibration targets [S].**
- The "crisis 4–8%" distribution yields are the dossier's own scenario values, not Bain's.
- "Up to 15%" secondary discounts are not in the cited source.
- The Yale <10% is a single top-tier, strong-market sale and should not anchor the "normal" discount for an ADIC-scale seller.

**R12. LOW. §1.3, §3.3(b): the smoothing comparison is partly confounded.**
- The Yale-type rule at r*=7.5% pays more on average than fixed 7.5% (7.74% vs 7.50% in Case A).
- Part of the 15.6% vs 4.8% gap is payout level.
- The payout-matched R12 (10.3%) is the cleaner comparison and should be the headline.

**R13. LOW. §1.7, §2.7: "Singapore spends from expected returns" needs qualifying.**
- The NIRC's NII component spends realized income (see claim 4).

---

## 6. Arithmetic checks that passed

- **Net reading:** $(1+R)=1.10/(1-d)$ gives 15.8% / 18.9% / 22.2%. ✓
- **Sustainable payout $d^*=1-(1+\pi)/(1+g)$:** 6.8% (g=10%); 6.2–6.3% (arithmetic 10% at 12% vol, geometric ≈9.3–9.4%); 4.5% at 7.38% (4.6% at exactly 7.4%). ✓
- **§3.4 table:** all 21 cells. ✓
- **Volatility drag** 0.72pp / 1.28pp and **half-lives** 1.9 / 3.1 / 6.6 years. ✓
- **Stale-NAV leak:** 0.84 vs 0.75, so 8.4% of economic NAV. **Denominator effect:** 64%, then 69.5%. ✓
- **Deterministic sequence test:** 7.5% fixed gives 0.589 in every crash year; fixed real gives 0.000 / 0.111 / 0.470. ✓ The Yale and POMV rows were not recomputed.
- **Mixture calibration:** Case A normal-regime parameters (0.1156, 0.0746) plus crisis (8%, −0.22, 0.08) give arithmetic mean 10.00% and SD 12.00%. ✓
- **P(20-year annualized ≥10%):** 42.3% analytic, 42.0–42.6% re-simulated. ✓
- **Tables 1–3:** every transcribed cell matches `spendsim_T20_v2.md` and `sweep_T20.md` (25% floor runs) to rounding. ✓
- **Payout size:** 7.5% × $177bn ≈ $13.3bn. ✓

---

## 7. Overall reliability rating

**MEDIUM.**
- **Sourced facts and citations: HIGH.** The 17 confirmed claims include all the policy rules and peer statistics that drive calibration. No citation is fabricated.
- **Corrections are mostly attribution and labelling** (Kuwait, Ennis, Harvard 2009, CPP benchmark, Stanford, NBIM, ADIA, NZ Super, Yale discount). They are easy to fix but should be fixed before IC use.
- **Design implications: MEDIUM-to-LOW in places.** R1 (ill-defined habit utility) and R2 (floor-driven, frequency-only forced-sale probabilities) would mislead an IC if shipped as is. R3–R5 change how DWY and the constraint set should be presented.

## Citation corrections (2026-10-18)

The dossier's citations were corrected on 2026-10-18 from two sources: the literature audit (`research/literature/00_LITERATURE_SYNTHESIS.md` §2) and its stream-02 table (`research/literature/02_endowment_swf.lit.md` §2). Where this log quotes the dossier's references, it describes the text before that correction; "Ennis (2020), SSRN 3614875" is one example. Changes to this log:
- §3 claim 17: noted the probable published source of the −1.87% figure: Ennis (2021), *JPM* 47(5):128–143, inferred.
- §4 Merton (1993): noted that ch. 7, pp. 211–242 and NBER WP 3820 (Aug 1991) are now confirmed.
- §4 Dybvig (1995): noted the upgrade to verified in the dossier.
- §4 Ennis (2020): noted three things:
  - SSRN 3614875 is confirmed as the 2020 working paper;
  - it was published as Ennis (2021), *J. Investing* 30(3):6–20, DOI 10.3905/joi.2021.1.166;
  - the later paper is probably *JPM* 47(5):128–143.
- §4 Urwin & Hayman (2026): noted that both authors and DOI 10.56227/26.1.20 are confirmed, so this log's author attribution stands.
- No erratum: the audit reports nothing that this log wrongly accepted.
