# Verification log: Stream 07, fusing underwritten, current-actual and forecast returns into calibrated forward beliefs

**Dossier checked:** `research/dossiers/07_return_fusion.md` (not edited).
**Verified:** 2026-10-18.
**Role:** adversarial fact-check before Investment Committee (IC) use.

---

## 1. Summary

**The empirical base is accurate, with no hallucinated citations. The design layer and one IC-facing worked example need repair before use.**

- **Claims.** 30 empirical claims checked: **24 confirmed, 2 corrected, 0 refuted, 4 unverifiable.**
  - All 19 claims the author flagged were checked: 16 confirmed, 1 corrected (Brown–Ghysels–Gredil numbers come from the working paper, not the RFS version), 2 unverifiable (Jenkinson–Sousa–Stucke 2013 specifics; PitchBook R²).
  - 11 more load-bearing claims were added. All were confirmed except one corrected data period (Nadauld et al.) and two unverifiable items (Barber–Yasuda specifics; Basel zone-threshold text).
- **Citations.** 26 references were checked for existence and metadata. All exist. Problems found:
  - one version mismatch (BGG);
  - one wrong sample period (Nadauld);
  - three load-bearing claims resting on weak secondary sources (Wikipedia for the Cooke 26/33 statistic, MOS history and Bühlmann; rdrr.io for Bates–Granger).
- **Arithmetic.** Every number in Worked Examples 1–5 reproduces to rounding. Two inputs are undocumented or inconsistent:
  - Example 1's P_miss requires σ_e = 30%/yr, but Example 3 uses 15%.
  - Example 3's 47/42/11 credibility weights cannot be reproduced from the §6.4 defaults.

**Five design problems would change what the IC sees:**

1. **Example 3's SELL rests on an optimistic bid (§6.8, Example 3).**
   - The example uses 88% of reported NAV for a 9.5-year-old fund interest and calls it "consistent with high-quality buyout pricing around 90%".
   - The dossier's own market sources price late-life interests much lower:
     - Jefferies H1 2026: tail-end (10+ years) at **25%+ discounts**.
     - Evercore H1 2026: tail-end **~70% since 2022**, with select high-quality tail-ends into the 80s.
   - The SELL/HOLD switch point is a bid of **86.9% of reported NAV** (PV_hold 347.6). At 75–80% of NAV, HOLD wins unless the liquidity shadow value is 9–16% or more.
2. **Underwriting or the prior is double-counted in the BF/Benktander "actual" signal (§6.6 with §6.4–6.5).**
   - U₀ is "debiased underwriting or reference class". The resulting signal is then fused next to the u-signal (ρ_ua = 0) and the reference-class prior.
   - Mack's formulas also require U₀ to be independent of C_k. The dossier's debiasing uses plan shortfall (u − a), which breaks that requirement.
3. **The Ω calibration mixes in outcome noise (§6.7).**
   - Errors are measured against realized outcomes y. The fusion target, however, is the expected return μ.
   - Naive estimates therefore become Ω + Var(y−μ)·11′, which inflates every ω and ρ and correlates the prior's error with the signal errors.
4. **Mack's t = 0.5 is presented as a sourced default (§6.4).**
   - In Mack (2000), t = 0.5 is some companies' BF-versus-CL *switching* rule. Mack says t "should" be estimated case by case; his examples give t = 0.346 and 0.309.
   - Plugging 0.5 into c* = p/(p+t) is a design choice ([I]), not an [S] default.
5. **The LEVER/REFI gate is mis-specified for asset-level recaps (§6.9, Example 1).**
   - It compares the posterior *levered-equity* forward return (13.6%) with recap debt cost (9%).
   - That comparison is right for a NAV loan against an LP interest. For a dividend recap on a buyout company, the comparison must be with the unlevered asset return. As written, the gate favours LEVER on assets that are already levered.

**Overall reliability: MEDIUM.**
- *High* for sourced facts, market data and citations.
- *Medium* for the fusion design (§6.4–§6.7, §6.9).
- *Low-to-medium* for the Example 3 recommendation as currently framed.

---

## 2. Method

- **Primary documents read in full** after download, not from summaries:
  - Cambridge Associates (2018); Mack (2000) with its correction note; Harris et al. (NBER w28109).
  - Korteweg & Sorensen (accepted manuscript, including Table 4); HM Treasury optimism-bias PDF; Nadauld et al. (NBER w22404).
  - Evercore H1 2026 Secondary Market Review; Jefferies Global Secondary Market Review, July 2026 (rendered pages).
  - Gompers–Kaplan–Mukharlyamov 2015 draft (text extracted from the PDF).
- **Fetched directly from the publisher or author:** abstract pages for NBER w22493, w16215, w22404, w21133 and w25207; ORA (Jenkinson et al. 2020); UNC KIPC (BGG working paper); OUP (BGG RFS 2023); arXiv; gov.uk; Bain; JPM LTCMA; AQR; Stanford GSB; EUR repository; Duke FDS; CAS.
- **Metadata** for Nadauld 2019, Yao et al. 2018, Blanc & Setzer 2020, Harris et al. 2023 and Wang et al. 2023 came from Crossref DOI lookups.
- **Constraint.** The session's shared web-search budget was exhausted when this check began. No search-engine queries were made. Blocked pages were not routed around:
  - SSRN 2229547 and the PitchBook PDF returned HTTP 403.
  - The Barber–Yasuda eScholarship PDF returned 403.
  - The BIS PDF text was not retrievable.
  The claims depending on those pages are marked unverifiable.
- **Recomputation.** All worked examples were re-derived in a script:
  - GLS posterior, weights, P_opt, P_miss and 80% bands;
  - Example 3 PV, break-even and buyer IRR;
  - Benktander/BF/CL ultimates;
  - credibility Z, design effect and range-widening factors;
  - exact Binomial(40, 0.10) cumulative probabilities.

---

## 3. Claims table

Verdicts: **C** = confirmed, **X** = corrected, **R** = refuted, **U** = unverifiable. "F" marks an author-flagged claim.

| # | Claim (dossier §) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 F | Funds take 6–8 years to settle into their final quartile; VC and FoF 7–9; secondaries 5–7; TVPI settles later than IRR; most funds rank in nearly all quartiles (§1, §4.3) | C | Verbatim. Sample: 2,606 funds, vintages 1995–2005 (pre-ASC 820). 85% (IRR) and 87% (TVPI) ranked in 3–4 quartiles; about half ranked in all four. | https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2018/05/PI-Portfolio-Benchmarking-Best-Practices.pdf |
| 2 F | 57% of buyout funds top quartile at fundraising end top quartile; ~23% of bottom-quartile funds end above median (24% post-2000); no buyout persistence at fundraising post-2000, while VC persists; buyout MOICs cluster at 1.73–1.78x across prior quartiles (§1, §4.1, §4.3, §4.4) | C | Verbatim (p.15, Table 5; p.13, Table 4). The quartiles are PME quartiles of the *previous* fund, interim vs final. JCF 81 (2023) 102361 confirmed. | https://www.nber.org/system/files/working_papers/w28109/w28109.pdf |
| 3 F | The top–bottom quartile expected-return spread is 7–8 pp/yr (buyout IQR 8.03, VC 6.60); after 50 funds only 53–61% stay top quartile; the learning weight is the signal-to-noise ratio s with variance shrinking by (1−s); VC needs a 3-normal mixture (§2.4, §3, §4.4, §6.3) | C | Verbatim. 8.03/6.60 are Spec I (intercept only). Spec II (vintage FE) gives 7.51 (BO) and 7.42 (VC). Late sample (≥1997) BO 7.33; US BO 6.99. σγ(BO) = 0.060 is reported directly. | https://research-api.cbs.dk/ws/files/55394727/morten_soerensen_skill_and_luck_in_private_equity_performance_acceptedversion.pdf |
| 4 F | Mack (2000): c* = p/(p+t), t = E[α²]/(Var U₀ + Var U − E[α²]); BF beats CL iff p < t; Benktander almost always has lower mse; some companies use t = 0.5; Gogol z = σ²/(σ²+τ²), τ² = ln(1+β²q/p) (§1, §2.5, §6.4) | C | Theorem 3 (p.339), p.340, abstract and §5 all match. **Usage caveat:** t = 0.5 is a BF/CL switching rule. Mack says t should be estimated (his examples: t = 0.346, 0.309). A 2001 correction note revises Gogol μ₁; the dossier does not use it. | https://www.casact.org/library/astin/vol30no2/333.pdf |
| 5 F | Jenkinson, Sousa & Stucke 2013: CalPERS, 761 fund investments; NAVs understate distributions by ~35%; Q4 jump; inflation during fundraising, reversed after; interim IRRs during fundraising poorly predict final (§1, §4.2) | U | SSRN 403; search unavailable. The fundraising-inflation finding is consistent with secondary descriptions in Harris et al. 2020 (p.9) and Nadauld et al. 2016 (p.10). The 761, 35% and Q4 specifics are **not** verified. Verify before IC use. | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2229547 |
| 6 F | Some underperforming managers inflate NAVs while fundraising and are less likely to raise a next fund; top performers understate (§1, §4.2) | C | NBER w22493 abstract matches. JFE 132(2):267–297 (2019). | https://www.nber.org/papers/w22493 |
| 7 F | Buyout NAVs show little systematic bias; VC NAVs are aggressively biased, especially since 2000; 384 VC + 195 BO funds, 1988–2016 (§4.2) | C | ORA abstract matches. TAR 95(1):191–210 (online 2019). | https://ora.ox.ac.uk/objects/uuid:691dbf3a-2fb2-4156-8d12-967cdf89301e |
| 8 F | BGG nowcasting: median total risk ~33% (BO) / 38% (VC), 10 and 13 pp above as-reported; betas ~1.05 / ~1.20; cited as RFS 2023 (§4.2, §6.4) | **X** | These figures come from the **2020 working-paper** abstract on the UNC page, where the betas are ranges: **1.05–1.10 (BO) and 1.20–1.32 (VC)**. The **published RFS 36(3):945–986 (Mar 2023)** abstract instead gives an average-fund beta of **≈1.0 (BO) and ≈1.4 (VC)** and total risk of **≈33% (BO) and ≈40% (VC)**. Use the published numbers or label them as WP. This matters for venture β̃ in the nowcast. | https://academic.oup.com/rfs/article/36/3/945/6625642 ; https://uncipc.org/publication/nowcasting-net-asset-values-the-case-of-private-equity/ |
| 9 F | Executives' 80% intervals contain realized market returns only 36% of the time (13,300+ forecasts) (§1, §4.5) | C | Verbatim. QJE 128(4):1547–1584. | https://www.nber.org/papers/w16215 |
| 10 F | 210 transport projects in 14 nations; rail overestimated in 9 of 10 by 106%; half of roads off by >±20%; no improvement over 30 years (§4.1) | C | Verbatim. JAPA 71(2):131–146. | https://arxiv.org/abs/1303.6654 |
| 11 F | HM Treasury uplifts (upper bounds, duration/capex): standard buildings 4/24, non-standard civil engineering 25/66, equipment/development 54/200; reduced toward the lower bound as mitigation is evidenced (§4.1, §5) | C | Table 1 matches exactly. §3.17: mitigation "must be observed, and should be independently verified". **Note:** uplifts cover capex and works duration only. Mott MacDonald "was unable to recommend" benefit-shortfall uplifts (guidance §4.1). PDF dated Jan 2003; gov.uk page 21 Apr 2013. | https://assets.publishing.service.gov.uk/media/5a74dae740f0b65f61322c72/Optimism_bias.pdf |
| 12 F | Distributions/NAV ~14% in 2025, below 15% four years running; 32,000 unsold companies worth $3.8tn; ~7-year holds; IRR stagnates around year 7 and median TVPI flattens after year 8 (2000–2015 vintages); 2017–2021 vintages under-deliver (§1, §4.3, §4.6) | C | Verbatim. "Almost 40%" of companies held more than 5 years (29% in 2019). | https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ |
| 13 F | 2.5x in 5 years needed ~5% EBITDA growth in 2015 vs 10–12% today; 8–9% debt cost; 30–40% leverage; "12 is the new 5"; multiple expansion "powered over 50% of all buyout returns" (§1, §4.1) | C | Verbatim. 2015 leverage was ~50% at 6–7%. | https://www.bain.com/insights/welcome-to-a-new-era-global-private-equity-report-2026/ |
| 14 | 2025 buyout investment $904bn (+44%); exits $717bn (+47%) (§4.6) | C | Verbatim. | https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ |
| 15 F | H1 2026 secondaries $121bn (+19%), GP-led $65bn, LP-led $56bn; FY2025 >$226bn; quality buyout ~90% of NAV; senior credit at par or better; VC/growth softer; infrastructure buyers 13–15% net IRR; VC buyers 20%+ (§1, §4.6, §5) | C | All match (pp.2–3, 15, 18–19). The **same report** puts tail-end pricing at **~70% since 2022** (select high-quality into the 80s), which bears on Example 3. Sources disagree on volume: Jefferies has H1 2026 $118bn and FY2025 $240bn. | https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf |
| 16 | Average LP portfolio pricing 89% of NAV (2024); 87% in H1 2026 (§4.6) | C | 2024: Jefferies article of 16 May 2025. **H1 2026 87% is now verified** from the July 2026 PDF; the dossier said "search index only". Same PDF: buyout 91%; tail-end funds (10+ years) at "25%+ discounts". | https://www.jefferies.com/insights/markets/secondaries-get-a-second-wind/ ; https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 17 F | LP secondaries: buyer PME 1.023 vs seller 0.974, ~5 pp/yr; ~3 pp for funds aged 4–9 (§4.6, §5) | C | Verbatim. JFE 132(3):158–181 (2019). By fund age (Table 6): 0–3 years +24.5 pp; 4–9 years +3.0 pp; ≥10 years −0.8 pp (buyout −2.2 pp, i.e. sellers out-earned buyers). | https://www.nber.org/papers/w22404 |
| 18 | Nadauld et al. data period "2006–2017" (§4.6 table) | **X** | The transaction data cover **2006–2014** (WP pp.1, 11, 24). The published version reports the same headline PMEs. | https://www.nber.org/system/files/working_papers/w22404/w22404.pdf |
| 19 F | Estimated combination weights underperform equal weights because estimation adds bias and variance (§2.3) | C | Abstract matches. IJF 32(3):754–762. | https://repub.eur.nl/pub/81568 |
| 20 F | Optimizer's curse: unbiased estimates still yield post-decision disappointment; Bayesian adjustment mitigates it (§2.6, §6.9) | C | MS 52(3):311–322. | https://fds.duke.edu/db/aas/stat/faculty/bob.winkler/publications/278471 |
| 21 F | Pension return assumptions extrapolate own past performance across risky asset classes; in PE the extrapolation is "driven by stale investments" (§4.4) | C | Verbatim. WP 3659 (Feb 2018). The RFS 2022 version (†) was not checked this session. | https://www.gsb.stanford.edu/faculty-research/working-papers/return-expectations-institutional-investors |
| 22 F | PitchBook: interim vs final IRR R² 0.40 at age 4 and 0.54 at age 5; MAE 5.2% and 4.3% (§4.3) | U | PDF returns 403; search unavailable. Do not use in IC packs until verified. | https://files.pitchbook.com/website/files/pdf/PitchBook_Manager_Performance_Scoring.pdf |
| 23 | GKM: 79 PE investors, >$750bn AUM; rely primarily on IRR and multiples; target ~25% IRR (§4.1) | C | Draft: "target median IRRs of 25%" (gross, Table 8a); median net IRR marketed 20–25%. JFE 121(3):449–476. The "2014 trade report, 27% gross" was not checked. | https://www.nber.org/papers/w21133 ; https://www2.nber.org/conferences/2015/PRs15/Gompers_Kaplan_Mukharlyamov.pdf |
| 24 | JPM 2027 LTCMA: US large cap 7.5%, global core RE 7.9%, global infrastructure 7.1%; data as of Sep 2026 (§4.6, §6.3, Example 2) | C | Matches; 10–15-year horizon. | https://am.jpmorgan.com/us/en/asset-management/adv/insights/portfolio-insights/ltcma/ |
| 25 | AQR 2026 CMA: global 60/40 expected real return 3.4%; "risk premia are compressed" (§4.6) | C | Published 14 Jan 2026, as of 31 Dec 2025. | https://www.aqr.com/Insights/Research/Alternative-Thinking/2026-Capital-Market-Assumptions-for-Major-Asset-Classes |
| 26 | Cooke classical model: 33 post-2006 studies, 320 experts, performance weighting best in 26 (in-sample) (§3, §4.5) | C | Matches the cited page, but the 26/33 count is that Wikipedia article's own uncited analysis. **Cite primary work instead** (Cooke, Marti & Mazzuchi 2021; Eggstaff et al. 2014 for out-of-sample). | https://en.wikipedia.org/wiki/Structured_expert_judgment:_the_classical_model |
| 27 | MOS conceived at NWS TDL in 1965; first forecasts issued in 1968 (§5) | C | Matches the cited page (Wikipedia). Glahn & Lowry (1972) is the primary source. | https://en.wikipedia.org/wiki/Model_output_statistics |
| 28 | Secondary-transaction PE indices have higher betas and volatilities and lower alphas than NAV-based indices (§4.2) | C | Verbatim. NBER w25207 (Nov 2018). | https://www.nber.org/papers/w25207 |
| 29 | Barber & Yasuda 2017: low-reputation GPs with low realization rates peak at fundraising, then erode (§4.2) | U | eScholarship page empty and PDF 403. Title and venue confirmed through K&S's reference list; mechanism details not verified. | https://escholarship.org/uc/item/01h178mf |
| 30 | Basel traffic light: green if cumulative probability < 95%, red from 99.99% (§6.7, Example 5) | U | BCBS title and date (4 Jan 1996) confirmed; the threshold text was not retrievable. **Under the stated rule, Example 5's zones are exactly right:** P(X≤6) = 0.900, P(X≤7) = 0.958, P(X≤11) = 0.99962, P(X≤12) = 0.99991. That gives green 0–6, yellow 7–11, red ≥12. | https://www.bis.org/publ/bcbs22.htm |

**Tally:** C 24 · X 2 · R 0 · U 4. Author-flagged claims: C 16 · X 1 · U 2.

**Erratum (2026-10-18, literature audit: `research/literature/07_return_fusion.lit.md` §2 and `research/literature/00_LITERATURE_SYNTHESIS.md` §2.3):** two claims were wrongly accepted. **Row 26:** in Colson & Cooke (2017, *RESS* 163:109–120, DOI 10.1016/j.ress.2017.02.003), performance weights beat equal weights in-sample in 32 of 33 studies. 26 of 33 is the out-of-sample validity-index result, and out-of-sample statistical accuracy is below equal weighting's. The dossier's "in-sample" label was therefore wrong: X, not C. **Row 17:** the published *JFE* 132(3):158–181 abstract gives a sellers' PME of 0.976; 0.974 is the working-paper figure. So this is X, not C, and row 18's note that the published version reports the same headline PMEs is wrong. **Also:** the §5 citation check accepted Smith & Winkler's truncated title (full title: "The optimizer's curse: Skepticism and postdecision surprise in decision analysis"). Indexed abstracts have since confirmed rows 5 and 29 (U). **Corrected tally:** C 24 · X 4 · R 0 · U 2; author-flagged C 16 · X 2 · U 1. The dossier has been corrected.

---

## 4. Worked-example recomputation

| Example | Dossier | Recomputed | Status |
|---|---|---|---|
| 1, independent | μ̂ 13.9%, σ̂ 0.036, weights 36/36/20/8, P_opt 97.5%, gap 704 bp, band 8.8–19.3% | 13.90%, 0.0360, 36/36/20/8, 97.5%, 704 bp, 8.8–19.3% | ✓ |
| 1, correlated | μ̂ 13.6%, σ̂ 0.041, weights 47/35/13/6, P_opt 96.3%, gap 732 bp, band 7.8–19.7%, P(μ<9%) 15.8% | 13.59%, 0.0411, 47/35/13/6, 96.3%, 732 bp, 7.8–19.7%, 15.8% | ✓ |
| 1, P_miss | 62.8% / 63.3% | Reproduces **only with σ_e = 30%/yr** (unstated). With Example 3's σ_e = 15%: 73.5% / 74.0% | Undocumented input |
| 1, reference-class percentile | 95th | 95.3% | ✓ |
| 2 | 8.15%, σ̂ 0.016, weights 60/32/6/2, P_opt 79%, gap 124 bp | 8.15%, σ̂ **0.0155**, 60/32/6/2, 78.9%, 124 bp | ✓ (σ̂ rounding) |
| 3, money | E[R] 431.3, median 417.8, PV_hold 347.7, PV_face 387.0, break-even 436.6 (1.092x), P 43.1%, required μ 4.71%, buyer IRR 13.2% / 7.1%, convexity ~3% | 431.2, 417.7, 347.6, 387.0, 436.6 (1.092x), 43.0%, 4.71%, 13.21% / 7.09%, 3.2% | ✓ |
| 3, weights | 47/42/11 | **Not reproducible** from the §6.4 defaults: ω_a(9.5) = 0.097 with ρ_fa = 0.3 gives 49/45/6; independent errors give 44/44/12. The a-signal value is unstated. μ̂ is robust (≈4.3%) | Undocumented input |
| 4 | U_CL 1.235, U_BF 1.356, U_GB 1.263, U_c* 1.283 (c* 0.606); forward IRR 6.0 / 8.1 / 6.5 / 6.8 / 16.2 / 19.8% | Identical | ✓ |
| 5 | n_eff 33.7, k 36, Z 0.48, bias 3.73%, sd 1.44%, widening ×1.81 / ×2.74, zones 0–6 / 7–11 / ≥12 | Identical | ✓ |
| §6.3 σ_k | 8.03/(2×0.674) ≈ 6% | 5.95%; matches K&S σγ = 0.060 | ✓ |

---

## 5. Citation check (existence, authors, year, title, venue)

| Reference | Result | Notes |
|---|---|---|
| Mack (2000) *ASTIN Bulletin* 30(2):333–347 | ✓ exists, metadata correct | A 2001 correction note is appended to the CAS PDF. |
| Korteweg & Sorensen (2017) *JFE* 124(3):535–562 | ✓ | |
| Harris, Jenkinson, Kaplan & Stucke (NBER w28109, Nov 2020; *JCF* 81, 2023, 102361) | ✓ | Crossref confirms the JCF details. |
| Brown, Ghysels & Gredil (2023) *RFS* 36(3):945–986 | ✓ exists; **content mismatch** | The cited URL (UNC KIPC) carries the 2020 WP abstract, whose numbers differ from the RFS abstract (row 8). |
| Brown, Gredil & Kaplan (2019) *JFE* 132(2):267–297 | ✓ | Volume and pages corroborated by Harris et al.'s reference list. |
| Jenkinson, Landsman, Rountree & Soonawalla (2020) *TAR* 95(1):191–210 | ✓ | |
| Ben-David, Graham & Harvey (2013) *QJE* 128(4):1547–1584 | ✓ | |
| Flyvbjerg, Skamris Holm & Buhl (2005) *JAPA* 71(2):131–146 | ✓ | |
| Nadauld, Sensoy, Vorkink & Weisbach (2019) *JFE* 132(3):158–181 | ✓ | The dossier gives the DOI only, which is correct. The **data period in the §4.6 table is wrong** (row 18). |
| Claeskens, Magnus, Vasnev & Wang (2016) *IJF* 32(3):754–762 | ✓ | |
| Smith & Winkler (2006) *Management Science* 52(3):311–322 | ✓ | |
| Bornhuetter & Ferguson (1972) *PCAS* LIX:181–195 | ✓ | |
| Gompers, Kaplan & Mukharlyamov (2016) *JFE* 121(3):449–476 | ✓ | |
| Yao, Vehtari, Simpson & Gelman (2018) *Bayesian Analysis* 13(3):917–1007 | ✓ | Crossref. |
| Wang, Hyndman, Li & Kang (2023) *IJF* 39(4):1518–1547 | ✓ | Crossref. |
| Blanc & Setzer (2020) *Management Science* 66(12):5720–5737 | ✓ | The authors marked † are correct. **Orphan reference:** it is never cited in the body. |
| Efron & Morris (1975) *JASA* 70(350):311–319 | ✓ | Confirmed via K&S's reference list. The dossier's link (chance.amstat.org) is contextual only. |
| Andonov & Rauh (2018) Stanford GSB WP 3659 | ✓ | RFS 2022 not verified (†). |
| Barber & Yasuda (2017) *JFE* | ✓ title and venue | Volume, pages and content not verifiable this session. |
| Boyer, Nadauld, Vorkink & Weisbach, NBER w25207 | ✓ | |
| Cambridge Associates (2018); Bain GPER 2026; Evercore H1 2026; Jefferies (May 2025; Jul 2026); JPM 2027 LTCMA; AQR 2026 CMA; HM Treasury (2003/2013); BCBS (1996) | ✓ all exist; dates correct | The Jefferies July 2026 figures *are* readable as rendered images. The dossier's "not machine-readable" note is outdated. |
| Bühlmann (1967) cited via a Wikipedia URL; Bates & Granger (1969) via rdrr.io | ⚠ weak sourcing | Replace with the journal records (*ASTIN Bulletin* 4(3); *ORQ* 20(4):451–468). |
| PitchBook "Manager Performance Scoring"; Jenkinson, Sousa & Stucke (2013) SSRN | ⚠ inaccessible (403) | The figures attributed to them are unverified (rows 5, 22). |

No hallucinated or garbled citations were found.

---

## 6. Reasoning issues and overclaims in the design implications (ranked)

**R1. HIGH. The Example 3 SELL verdict depends on an unrepresentative bid.**
- The 88%-of-NAV bid is benchmarked to "high-quality buyout ~90%" (Evercore), but the interest is 9.5 years old.
  - Jefferies (Jul 2026): "Tail-end funds (10+ years old) … priced at 25%+ discounts."
  - Evercore: tail-end "~70% since 2022, with select high-quality tail-ends into the 80s".
  - Nadauld et al.: in buyout tail-end sales, sellers out-earned buyers by 2.2 pp/yr on PME.
- The decision switches at a bid of 347.6/400 = **86.9%** of reported NAV.
  - At 80% (320), HOLD wins unless λ_liq ≥ 8.6%.
  - At 75% (300), λ_liq must be ≥ 15.9%.
  - At 70% (280), λ_liq must be ≥ 24%.
- A second, opposite-direction sensitivity is R6.
- **Fix:** present the bid as a distribution conditioned on fund age and quality. Show the switching bid and switching liquidity value, and state that Example 3 is illustrative.
- Also: "a 2% liquidity shadow value … makes it a SELL" is misleading. The base case is already a marginal SELL (352.0 > 347.7).

**R2. HIGH. Double counting in the BF/Benktander "actual" signal (§6.6).**
- U₀ is "debiased underwriting or reference class". The BF/Benktander output replaces ρ_a and is then fused with the u-signal (default ρ_ua = 0) and the reference-class prior m.
  - If U₀ is debiased underwriting, the a-signal carries a (1−p)-weighted copy of u, so ρ_ua ≠ 0.
  - If U₀ is the reference class, the prior enters twice.
  - Either way σ̂ is understated and P_opt overstated.
- Mack's formulas also assume U₀ is independent of C_k. Mack (§7) warns they "probably will not hold any more for a 'prior' U₀ which has been adjusted during the development period". The dossier debiases u with covariates built from the current marks (plan shortfall u − a; revision history; §6.1).
- **Fix:** freeze U₀ at inception, from the outside view only. For fund interests, either drop the separate u-signal or estimate the a–u error covariance explicitly.

**R3. MEDIUM. Outcome noise contaminates Ω in calibration (§6.7).**
- The model targets μᵢ, the expected forward return. Calibration errors e_ij = y_i − s_ij, however, include the asset's realized-outcome noise (y_i − μ_i), which every source for that asset shares.
- Naive estimation gives Ω̂ ≈ Ω + σ²_{y|μ}·11′. That inflates every ω_j and ρ_jl, and it makes the prior's error correlated with the signal errors, violating the independence behind Λ = σ_k⁻² + 1′Ω̃⁻¹1.
- The vintage effect δ_v does not remove asset-specific outcome noise.
- **Fix:** add an asset-level random effect shared across sources. Alternatively, identify Ω from cross-source differences (s_j − s_l) and from revisions, where outcome noise cancels.

**R4. MEDIUM. Mack's t = 0.5 is presented as a sourced default (§6.4).**
- Mack mentions that "some companies use this rule with t = 0.5", meaning BF when p < 0.5 and CL otherwise. He then says t "varies from one business to the other and therefore the actuary should try to estimate t in every single case". His examples give t ≈ 0.31–0.35.
- Using t = 0.5 inside c* = p/(p+t) is an [I] choice.
- Mack's variance model, Var(C_k/U|U) = p·q·β², describes paid-claims development. TVPI contains a GP mark rather than a partial realization. Test whether TVPI or DPI triangles fit that model before reusing c*.

**R5. MEDIUM. The LEVER/REFI gate compares levered equity return with debt cost (§6.9; Example 1).**
- "P(μ < 9% all-in recap cost) = 15.8%" uses μ = 13.6%, the forward return on a levered buyout equity stake.
- For an asset-level dividend recap, the relevant hurdle is the unlevered asset return versus the after-tax cost of debt, plus the change in equity risk. Adding leverage raises expected equity return mechanically (Modigliani–Miller), so the gate as written is biased toward LEVER.
- For an LP-level NAV loan, comparing the forward return on NAV with the loan cost is appropriate. The rule should distinguish the two cases.
- P(μ < c) also ignores outcome risk σ_e. The LTV quantile test only partly covers that.

**R6. MEDIUM. Timestamp mismatch inside Example 3.**
- The forecast numerator (480) is held fixed while the denominator is nowcast down 6% for Q3 comps. That lifts the forecast's forward IRR from 7.6% to 10.3%, about +2.5 pp of ρ_f.
- If the forecast predates the Q3 move, it should be nowcast too. That would cut ρ_f to about 7.3% (log) and μ̂ by about 1 pp, strengthening SELL.
- The dossier warns about "timestamp misalignment" in §7, but its own example shows it.
- **Fix:** require forecast and NAV as-of dates in the translation layer, and nowcast both.

**R7. MEDIUM. The Binomial/Basel traffic light assumes independent breaches (§6.7.7; Example 5).**
- Downside-case breaches cluster by vintage and regime, the same common shocks δ_v that the dossier models.
- Under clustering, a calibrated forecaster lands in yellow or red far more often than 5% / 0.01% in bad vintages, and looks falsely green otherwise.
- **Fix:** use a beta-binomial or vintage-clustered test, or apply zones to vintage-demeaned breach rates.

**R8. LOW–MEDIUM. P_opt is presented as a finding.**
- The executive summary's "P(forecast optimistic) is 96%" is a posterior under [I] defaults: m = 10%, σ_k = 6%, α_f = +3% and the ρ values.
- Even with α_f = 0, P_opt ≈ 94%, because of shrinkage to m.
- Label it model-conditional and show its sensitivity to m, σ_k and α_f.

**R9. LOW. σ_k calibration choice.**
- 8.03% is K&S Spec I (1969–2001 liquidated funds, Preqin IRR).
- Spec II with vintage FE (7.51%), the late sample (≥1997, 7.33%) and US buyout (6.99%) imply σ ≈ 5.2–5.6%.
- Given Harris et al.'s post-2000 findings, 6% sits at the high end. A lower σ_k gives the prior more weight.

**R10. LOW. σ_idio = 25% is a fund-level figure (BGG).**
- Example 1 applies it to a single-deal co-invest, whose idiosyncratic volatility is materially higher. The a-signal's precision is overstated; its weight is small (6–8%).

**R11. LOW. Undocumented or inconsistent example inputs.**
- σ_e is 30% in Example 1 versus 15% in Example 3.
- Example 3's weights cannot be reproduced, and its a-signal value is missing.
- Example 2's σ̂ is 0.0155, reported as 0.016.

**R12. LOW. Equivalence and attribution overclaim (§2.3, §1).**
- "Bates–Granger GLS … is the same thing as multi-source Bühlmann credibility" holds only when covariances are known, signals are debiased and the prior's error is independent of the signals' (see R3).
- Bates & Granger (1969) derive the two-forecast case. The matrix GLS form comes from later literature.

**R13. LOW. The Green Book analogy is about mechanics, not magnitudes.**
- The uplifts are for public-project capex and duration; benefits uplifts were explicitly not recommended. As a template for underwriting-return haircuts, label them [I] and use them only for the "start high, reduce with verified mitigation" workflow.

**R14. LOW. The secondary cost of selling is not age-conditioned (§5.1).**
- "About 5 pp a year … the price ADIC pays when selling" is the Nadauld full-sample mean, which crisis-era young-fund sales dominate.
- For 4–9-year funds it is about 3 pp; for tail-end funds it is about zero or negative.

**R15. LOW. Overstatement (§1).**
- "The only quantity that matters for a SELL / HOLD / REFINANCE / LEVER decision is the forward return on current (nowcast) NAV" is too strong.
- The dossier's own rules also need the bid versus PV at the hurdle, liquidity shadow values, downside LTV and total-portfolio risk contribution.

---

## 7. Required changes before IC use

1. Re-frame Example 3 with an age- and quality-conditioned bid distribution, the switching bid (86.9% of NAV), the switching λ_liq, and an explicit forecast as-of date.
2. Fix the BF/Benktander integration: inception-frozen outside-view U₀, no separate u-signal for fund interests (or a modelled a–u covariance), and t estimated from ADIC triangles.
3. Specify Ω estimation net of shared outcome noise.
4. Split the LEVER/REFI gate into NAV-loan and asset-recap variants, the latter using the unlevered asset return.
5. Replace the BGG figures with the published RFS numbers or label them as WP. Fix the Nadauld period to 2006–2014.
6. Verify or drop Jenkinson–Sousa–Stucke specifics (761 / 35% / Q4) and the PitchBook R² values.
7. Replace Wikipedia and rdrr.io citations for the Cooke 26/33 statistic, Bühlmann and Bates–Granger with primary sources.
8. Make the downside-breach traffic light cluster-robust.

---

## 8. Overall reliability

**MEDIUM.**
- Sourced facts, market statistics and citations are of high quality: 24/30 confirmed, no refutations, no hallucinated references, and fully reproducible arithmetic.
- The fusion design has several medium-to-high issues (R1–R7). One of them, R1, flips the headline SELL recommendation under realistic tail-end pricing. Fix these before any number from §6 reaches an IC pack.

---

## Citation corrections (2026-10-18)

- §3: one erratum line added after the tally. It records three wrongly accepted items: row 26 (Cooke's 26 of 33 is out-of-sample; in-sample is 32 of 33, per Colson & Cooke 2017), row 17 and row 18's note (the published Nadauld sellers' PME is 0.976) and the truncated Smith & Winkler title in the §5 citation check. It also notes that rows 5 and 29 are now confirmed, and gives the corrected tally C 24 · X 4 · R 0 · U 2.
