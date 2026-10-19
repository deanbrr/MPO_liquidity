# G1 PE primaries: verification log

*Adversarial fact-check of `research/groups/dossiers/G1_pe_primaries.md`. Prepared 2026-10-18. The dossier was not edited.*

## 1. Summary

**What was checked.** 28 empirical claims: the author's 18 flagged claims plus 10 others I judged load-bearing. I also checked 20 references and reviewed the design implications and specification card (§3, §6) for reasoning errors.

**Method.**
- I downloaded every primary PDF myself into clean folders and extracted the text with pypdf: K&S, HJKS w28109, LSW w11136, Albertus & Denes, LSMZ w24941, SWY w19612, ILPA 2017, the ILPA Model LPA, ILPA CF 2023, both ILPA NAV documents (2024), Cliffwater/ERSRI, Bain GPER 2026, Evercore H1-2026 and MSCI Q2-2026.
- I then grepped for each number and read the surrounding text.
- Web pages (NBER abstracts, Cherry Bekaert, the HLS forum, Hamilton Lane, PR Newswire) were read with WebFetch.
- Bibliographic details were checked against Crossref metadata and Consensus search.
- I re-ran all four of the author's synthetic scripts in isolated mode and wrote one small check script of my own: `scratchpad/vg1/scripts/check_cohort_irr.py`.

**Bottom line.** The factual layer is strong:
- 25 claims are confirmed exactly, 3 are corrected and none is refuted.
- Every core citation exists, with correct authors, year, title and venue.

The analytical layer has several material problems:
1. **The pause's "implied financing rate" (≈10.5–11%) is the engine's assumed NAV growth rate G restated.** I verified this: a normal-regime cohort's IRR is exactly 11.00%, and the 2027 vintage on path L is 10.51%. It is also compared with a debt cost (the NAV facility) without any risk adjustment, and the fee basis of G is ambiguous.
2. **The access-value formula R2 (§6.5) overstates relationship value**, because it assumes the LP learns a GP's skill γ exactly before each re-up.
3. **The CV price "≈99% of FMV" is Evercore's figure for GP-led *private-credit* secondaries**, not for PE continuation vehicles.
4. **The control experiment did not apply the pacing corridor the dossier recommends.** The recommended gains breach that corridor.
5. **Subscription lines are modelled as delayed deployment, not as line-financed investment.**

Fix these before the dossier's pacing-versus-facility ranking or its access penalties reach the IC.

## 2. Claims table

S = author-flagged claim; A = additional claim I selected.

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| S1 | K&S: buyout top–bottom quartile spread 8.03pp/yr (VC 6.60pp); signal-to-noise (S/N) per fund 0.141–0.148 buyout, 0.035–0.051 VC; with 5 funds of top-quartile history, 47% (buyout) / 37% (VC) chance of top-quartile expected returns | **Confirmed** | Exact (text pp. 22–28; Table 4). VC 6.60% is the point-estimate value; 6.59% allows for parameter uncertainty. With vintage fixed effects (Spec II) the spreads are 7.51% (buyout) and 7.42% (VC). | https://research-api.cbs.dk/ws/files/55394727/morten_soerensen_skill_and_luck_in_private_equity_performance_acceptedversion.pdf |
| S2 | HJKS: post-2000 buyout shows no persistence at fundraising (only avoiding bottom quartile helps); first-time funds do at least as well; VC prior top-quartile PME 1.70 vs 0.91; 57% of top-quartile-at-fundraising buyout funds end top quartile | **Confirmed** | Exact (pp. 3, 13–15). **Caveat:** 1.70 vs 0.91 is the full sample. Post-2000 VC at fundraising is **1.20 vs 0.91**, post-2000 first-time VC funds average 1.23, and the four-quartile test is not significant. The dossier cites only the full-sample figure. | https://www.nber.org/system/files/working_papers/w28109/w28109.pdf |
| S3 | LSW: endowments' follow-on funds 31% vs 7% IRR; public pensions 6% vs −2%; reinvestment rates ~60/50/39% | **Confirmed** | Exact (working paper Feb 2005, pp. 26–27). The sample is funds raised 1991–2001, not strictly "the 1990s". | https://www.nber.org/system/files/working_papers/w11136/w11136.pdf |
| S4 | Sensoy, Wang & Weisbach: endowments' 1991–98 edge came from access to top VC and vanished in 1999–2006; 14,380 investments, 1,852 LPs, 1,250 funds | **Confirmed** | Exact (abstract). | https://www.nber.org/papers/w18793 |
| S5 | Brown et al.: PE returns cyclical; realistic commitment-timing strategies give modest gains because calls and exits cannot be timed | **Confirmed** | Abstract: "modest gains, at best". Published as JFE 139(2) 561–577 (2021). | https://www.nber.org/papers/w26755 |
| S6 | Albertus & Denes: 26.6% of buyout funds used lines (2014Q2–2019Q1, Burgiss); IRR +2.6pp; TVPI −0.006; PME +0.036; bottom quartile +8.3pp more likely to use lines; a 25%-of-fund line held 1 year raises carry 1.4% | **Confirmed** | All exact. 26.6% is the "SLC mean of 0.266" in the fund-level relative-performance sample; about 30% of fund-quarters use lines in the capital-call sample. Mean leverage 5.8% and the hurdle figures (0.6% to 5.5%) are also confirmed. | https://conference.nber.org/conf_papers/f141738/f141738.pdf |
| S7 | ILPA 2017: line ≤180 days and 15–25% of uncalled capital; preferred return from the draw date; IRR reported with and without the line; Cobalt study (498 funds): +206bp by year 3, 35–45bp by end of life | **Confirmed** | Exact (pp. 3–4, footnote 2). 15–25% and 180 days are given as example thresholds ("such as", "e.g."). | https://ilpa.org/wp-content/uploads/2017/06/ILPA-Subscription-Lines-of-Credit-and-Alignment-of-Interests-June-2017.pdf |
| S8 | ILPA Model LPA 2020: default remedies (10% interest, forfeited distributions, forced sale at 50% of the lesser of contributions or value, up to 100% forfeiture); term 10+1+1; fee ends at initial term; recycling of investments realised within 12 months plus fees | **Confirmed** | Exact (§6.6.3–6.6.4.3, §18.1, §8.3.1, §6.4 and footnote 11 on the 110% cap). The first extension needs LPAC consent, the second a Majority in Interest. Preferred return [8]%, catch-up [80]/[20], carry [20]% and the 100% fee offset are also confirmed. | https://ilpa.org/wp-content/uploads/2020/07/ILPA-Model-Limited-Partnership-Agreement-WOF.pdf |
| S9 | Cliffwater/ERSRI no-new-commitments case: net cash flow (NCF) +$18m/+87m/+165m/+208m in 2024–27 (≈40% of $1.2bn forgone); NAV 32% below base by 2027; over-commitment (OC) 1.00x by 2026 | **Confirmed** | NCF 142/318/397/415 vs base 124/231/232/207: Δ sums to 478 of 1,200, i.e. 39.8%. NAV 1,107 vs 1,621 is −31.7%. OC is 1.00x at 12/31/2026. | https://data.treasury.ri.gov/dataset/40fb544c-65c5-464f-ba49-e3f65d1adc36/resource/7783fe26-a966-4850-82e0-f3f931812015/download/1a-cliffwater-pe-pc-ra-pacing-plan-dec-2023-final.pdf |
| S10 | Bain GPER 2026: buyout fundraising −16% to $395bn; buyout funds closed −23%; 53% of LPs constrained (+15pp); ~15% of series fail to re-raise normally (~20% in the GFC); CVs +62% YoY but <10% of exit value; LPs tolerate ~1 CV a year; 2017–21 vintages below the DPI benchmark | **Confirmed** | All exact. Bain: LPs "will usually tolerate only one CV a year at most". The benchmark is the average median DPI of 2010–17 vintages, as of Q3-2025. | https://www.bain.com/globalassets/noindex/2026/bain-report_global-private-equity-report-2026.pdf |
| S11 | Cherry Bekaert/PitchBook H1-2026: $159.6bn across 223 funds (FY2025 $308bn/551); 23 first-time funds vs 181 average (2021–23); buyout distribution yield 14.8% vs 23.4% long-run | **Confirmed** | Exact, as of 30 Jun 2026. The yield is for buyout, but the report does not define its measurement period. | https://www.cbh.com/insights/reports/private-equity-mid-year-2026-report/ |
| S12 | Evercore H1-2026: sovereign wealth funds (SWFs) 12%→21% of LP-led volume; 88% intermediated; **GP-led ≈99% of FMV**; tail-end ≈70% of NAV since 2022; quality buyout "in the 90s" | **Corrected** | SWF, 88%, tail-end and "in the 90s" are confirmed. **"≈99% of FMV" is the H1-2026 average for GP-led *private-credit* secondaries** (p. 17, "Deep Dive: Private Credit Secondaries"), not for PE GP-leds or CVs. For PE single-asset CVs, Evercore says "the majority of SACV volume transacts at par, with an additional 14% clearing above NAV". The chart split appears to be roughly 52% at par, 14% above and 34% below. | https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf |
| S13 | Begenau & Siriwardane: fee tiers in the same fund differ by ~91bp of management fee and ~5.8pp of carry (~2,400 funds, 1990–2019); VC uses fewer tiers | **Confirmed** | Exact per the HLS summary ("about 91 basis points and 5.8%"). Published JF 79(2) 1199–1247. | https://corpgov.law.harvard.edu/2024/05/10/fee-variation-in-private-equity/ |
| S14 | LSMZ: alternative vehicles were 32% of LP investments and 17% of commitments; underperformed main funds; better for LPs with stronger past performance | **Confirmed** | Exact (abstract: "32% of investments (17% of capital commitments)"; 112 LPs; ~5,500 investments). | https://www.nber.org/papers/w24941 |
| S15 | Lerner & Schoar: transfer restrictions screen for deep-pocket LPs, **so forced-looking sales can raise an LP's future cost of access** | **Corrected** | The screening theory and evidence are confirmed (fewer restrictions in later funds and where LPs have few liquidity needs). The access-cost consequence for a selling LP is the dossier's **inference**: the model is about lowering the *GP's* future cost of capital. Tag it [I]. | https://www.nber.org/papers/w9146 |
| S16 | MSCI Q2-2026: PE distribution rate 9% in H1-2026, contribution rate 31%; **marks for 2015 to 2022–23 vintages likely exceed realistic clearing prices** | **Corrected** | 9% and 31% are confirmed, and both are annualized per MSCI's definitions, so the comparison with the engine's 10.6% is like-for-like. MSCI's actual words: "**A meaningful share** of the vintages raised between 2015 and the 2022–23 rate reset continues to sit on the books at marks that likely **don't reflect** a realistic clearing price." MSCI adds that buyout exits "are not happening at distressed prices". The flagged wording drops "a meaningful share" and asserts a direction ("exceed"). §4.1 of the dossier quotes MSCI correctly. | https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf |
| S17 | Synthetic engine: pausing one vintage returns 20% of forgone in year 1 and ~69% by year 4; −$4.1bn cumulative 2027–40 per $5.1bn paused; implied financing rate 10.5–11% | **Confirmed (reproduced)** | Re-ran `g1_program_calib.py`: 1.02/5.11, 3.6/5.1, −4.1, and IRR 10.5% (path L) / 11.0% (path U). **The IRR equals the engine's G by construction** (see R1). | local: scratchpad\g1_scripts\g1_program_calib.py |
| S18 | Hamilton Lane: LPs overwhelmingly elect liquidity in GP-leds; GPs roll their entire carry in almost 70% of deals (2020–21) | **Confirmed** | Exact (2022 Market Overview, "Investment Activity"). | https://experience.hamiltonlane.com/investment-activity1 |
| A1 | Cavagnaro et al.: a one-s.d. rise in LP skill is worth 1–2pp/yr (published), ~3pp (2016 working paper) | **Confirmed** | JF 74(6) 3089–3134 abstract; WP w22547 abstract. | https://www.nber.org/papers/w22547 |
| A2 | SWY: LP break-even alpha 3.08%/yr under 2/20 | **Confirmed** | Add the qualifier: **without leverage**. At D/E of 3.0 it is 2.06% (WP pp. 3–4). | https://www.nber.org/system/files/working_papers/w19612/w19612.pdf |
| A3 | ILPA CF 2023: elections ≥30 calendar or 20 business days; non-responses default to sell; status-quo option | **Confirmed** | Exact. ILPA also says the GP should roll 100% of accrued carry "in almost all cases". | https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf |
| A4 | ILPA NAV guidance: NAV facilities are fund-level leverage; LPAC consent for distribution use; ~20% of facilities funded distributions; proceeds often recallable | **Confirmed** | Exact (July and Nov 2024 versions): "GPs should seek LPAC approval if they intend to use any of the proceeds to generate a distribution". The 20% is an FFA estimate. | https://ilpa.org/wp-content/uploads/2024/11/Part-I-Nav-Based-Facilities-Guidance.pdf ; https://ilpa.org/wp-content/uploads/2024/07/ILPA-Guidance-on-NAV-Facilities-2024.pdf |
| A5 | K&S secondary figures: 13.70pp (12.5–87.5 percentiles); overlap explains 44% of autocorrelation; 25+ funds needed for VC; least persistence in the US, most in the rest of the world; small funds more persistent | **Confirmed** | 43.6% average, range 25.8–61.7%. | (K&S URL above) |
| A6 | HJKS secondary figures: buyout repeat 34.8%, above median 57.3%, bottom stays bottom 39.2%; PME 1.30 vs 1.01; perfect foresight +2–2.5%/yr; VC repeat 45%; ~23% of bottom-quartile funds end above median; no size–performance relation | **Confirmed** | Exact. | (HJKS URL above) |
| A7 | Bain midyear (8 Jun 2026): ~1 in 5 LPs reducing buyout allocations (ILPA poll); software marks −8% (US −8.9%, Europe −4.2%). GPER Fig. 28: US stocks beat buyout over the decade, PE leads in Europe | **Confirmed** | Exact. | https://www.prnewswire.com/news-releases/winning-firms-will-focus-on-what-they-can-control-weather-the-rest-as-triple-shock-brakes-private-equitys-latest-revival-bain--company-2026-midyear-pe-report-302793107.html |
| A8 | Cherry Bekaert extras: KKR NA XIV $23bn + Clearlake VIII $14.8bn (≈24% of YTD); experienced $139.3bn vs emerging $20.3bn; US evergreen PE $99bn from $50bn | **Confirmed** | The derived share is 23.7%. | (CBH URL above) |
| A9 | Phalippou (2009): funds beat the S&P 500 before fees and lag after fees | **Confirmed** | JEP 23(1) 147–166 abstract. | https://www.aeaweb.org/articles?id=10.1257/jep.23.1.147 |
| A10 | ERSRI base and shock cases: PE 16.2% → 11.9–12.5% of assets; OC 1.93x → ~1.5x; −10% assets → 18.4%; combined shock 21–23%; ~87/13 buyout/VC commitments | **Confirmed** | Combined shock 21.1%/22.8%. The 2024 commitment split is 210/30, i.e. 87.5/12.5, drifting to about 85/15 later. | (ERSRI URL above) |

**Counts:** 28 checked, 25 confirmed, 3 corrected, 0 refuted, 0 unverifiable.

**Not checked.** Items the dossier itself tags [P] or attributes to other streams:
- CEM 380/571bp;
- the Houlihan Lokey roll rate of ~15%;
- the NAV-facility cost of 7–9% and the 8–15% implied sale cost (Stream 05);
- vendor pacing tools.

## 3. Citation check

| Reference as cited | Result |
|---|---|
| Korteweg & Sorensen (2017), *JFE* 124(3) 535–562 | Correct (Crossref, DOI 10.1016/j.jfineco.2017.03.006). |
| Harris, Jenkinson, Kaplan & Stucke, NBER w28109; *JCF* 81, 102361 | Correct (Crossref: JCF 81, article 102361, 2023). |
| Lerner, Schoar & Wongsunwai (2007), *JF* 62(2) 731–764 | Correct. The NBER WP lists the third author as "Wan Wong", with a "?" in the title. |
| Sensoy, Wang & Weisbach (2014), *JFE* 112(3) 320–343 | Correct (NBER page). |
| Brown, Harris, Hu, Jenkinson, Kaplan & Robinson (2020), NBER w26755 | Correct. Published version: *JFE* 139(2) 561–577 (2021); worth adding. |
| Albertus & Denes (2020), "Private Equity Fund Debt: Capital Flows, Performance, and Agency Costs" (26 May 2020) | Correct (title page). [Update 2026-10-18: a journal version by the same two authors now exists: "Private Equity Fund Debt: Agency Costs and Cash Flow Management", *JFQA*, online 7 May 2026, pp. 1–64, DOI 10.1017/s0022109026102890 (Crossref, OpenAlex). Its figures were not checked against S6: neither index has an abstract and the publisher page returned 403.] |
| Begenau & Siriwardane (2024), *JF* pp. 1199–1247 | Correct. Volume and issue are now verified: **79(2)** (DOI 10.1111/jofi.13319). |
| Lerner & Schoar (2002/2004), NBER w9146; *JFE* 72(1) | Correct, pages 3–40. |
| Lerner, Schoar, Mao & Zhang (2018), NBER w24941 | Correct as an NBER WP (that is NBER's author order). Published as Lerner, **Mao, Schoar**, Zhang (2022), *JFE* 143(1) 359–380, retitled "…in Private Equity". |
| Cavagnaro, Sensoy, Wang & Weisbach (2019), *JF* 74(6) 3089–3134 | Correct. |
| Brown, Gredil & Kaplan (2019), *JFE* 132(2) | Correct, pages 267–297. |
| Barber & Yasuda (2017), *JFE* 124(1) | Correct, pages 172–194. |
| Hochberg, Ljungqvist & Vissing-Jørgensen (2014), *RFS* 27(1) | Correct, pages 102–152. Published title spells it "Holdup". |
| Phalippou (2009), *JEP* 23(1) 147–166 | Correct. |
| Harris, Jenkinson & Kaplan (2014), *JF* | Correct: 69(5) 1851–1882. |
| Gourier, Phalippou & Westerfield (2024), DOI 10.1111/jofi.13382 | Correct: "Capital Commitment", *JF* 79(5) 3407–3457. |
| Sorensen, Wang & Yang (2014), w19612 | Correct: *RFS* 27(7) 1977–2021. |
| Luxenberg et al. (2022), arXiv 2207.07767 | Correct: "Strategic Asset Allocation with Illiquid Alternatives". |
| Robinson & Sensoy w17428; Nadauld et al. w22404 | Both exist with the stated topics (JFE 2016 and JFE 2019). |
| Schillinger, Braun & Cornel (2019), SSRN 3434112 | The paper exists (TUM CEFS page). The SSRN ID was not directly confirmed. [Resolved 2026-10-18: the literature review (`research/literature/G1_pe_primaries.lit.md` §2) confirmed SSRN 3434112 via Crossref, DOI 10.2139/ssrn.3434112. The Crossref abstract matches the dossier's summary.] |
| Industry documents (ILPA ×4, Cliffwater/ERSRI, Bain ×2, CBH, Evercore, MSCI, Hamilton Lane) | All resolve and contain the cited material, except the Evercore 99%-of-FMV attribution (S12). MSCI's document is stamped "text updated Sept. 24", while the dossier dates it "October 2026"; this is cosmetic. |

No hallucinated or garbled citations were found.

## 4. Reasoning issues and overclaims (most severe first)

**R1 (high). The "implied financing rate" of a pacing cut is an input restated as a result, and its comparison with a NAV facility is not like-for-like.** Affects §1 item 2, §3.3, §6.8 and §6.12.
- **It is G by construction.** In a Takahashi–Alexander (TA) cohort model with growth G, discounting a cohort's (distributions − calls) at G telescopes to zero, so every cohort's IRR is G. A pause's ΔNCF is minus one vintage's cash flows. I verified it: normal cohort IRR 11.0000%; 2027 vintage on path L 10.51%. So "≈10.5–11%" is the Stream-04 G assumption, not a finding.
- **It is risk-inclusive.** The forgone vintage's IRR is an expected return on a risky equity stream. A NAV facility rate is a debt cost. A pause *reduces* exposure; a facility *adds* leverage. The dossier's own §3.3 kernel says a cut's value is −NPV_m(vintage), i.e. the forgone alpha plus any illiquidity premium, not the forgone IRR. The exec summary's "more than an LP-level NAV facility (≈7–9%)" contradicts that framework.
- **Its fee basis is ambiguous.** T8 says fees must *not* be netted inside G (so G is gross), yet the engine has no fee flows. If G is gross, the dossier's own fee model (11% gross → 8.1% net) puts the pause's net rate at ≈8%, inside the 7–9% facility range, and the ranking disappears.
- **Fix.** State G's fee basis. Compare levers on a risk-adjusted basis: forgone net PME or alpha per $, or the cost after the forgone beta is replaced through the overlay (G7).

**R2 (high). The access-value formula overstates relationship value, and hence the access penalty κ^GP.** Affects §6.5 R2, R4, R5 and the worked illustration.
- **The flaw.** v_g = E[(γ−h)⁺]·D^PV is the payoff of committing only when the true γ exceeds the hurdle. The LP never observes γ; at each re-up it sees only its posterior mean μ_{g,k}. The decision value is E[(μ_{g,k} − h)⁺], which is never larger and can be far smaller. For a fund committed today, the value is simply (μ_g − h)·D^PV, which can be negative.
- **Size of the bias.** With K&S parameters and μ = h, the formula overstates value by 2.6× (buyout, 1 fund of history), 1.5× (5 funds) and 1.3× (10 funds). For VC the factors are 5.0×, 2.4× and 1.8× (`check_cohort_irr.py`).
- **Example.** With the prior σγ = 6%, the buyout example's E[(γ−h)⁺] = 1.5% corresponds to μ − h ≈ −2%/yr. That is a GP expected to *miss* the hurdle, yet it is assigned a ~$10m skip penalty.
- **Fix.** Use preposterior or option-on-posterior valuation, e.g. the LSMC already listed in §3.4. Use these numbers only as an upper bound.

**R3 (medium). The control experiment does not test the recommended policy.** Affects §1 item 3, §3.2 and §6.6.
- **Corridor not applied.** The recommended gain k_E = 0.15–0.3 produces minimum commitments of **0.69× and 0.45× plan** for the exposure rule (author's script output). That breaches the 0.75–1.25× corridor and, at k = 0.3, even the 0.5× IC-override floor. The experiment never clips to the corridor, so the reported troughs (28.2–28.6%) are not those of the constrained policy.
- **Exec summary misstates the comparison.** It says the NAV rule "produces a near-zero commitment year". At the same k = 0.6, the exposure rule produces an **actual zero-commitment year**: minimum 0.00 against 0.03 for the NAV rule.
- **MPC untested.** MPC is recommended, but only proportional rules were simulated.
- **No PE markdown.** The shock cuts W by 20% with no PE markdown, which maximises the denominator spike.

**R4 (medium). Subscription lines are modelled as delayed deployment.** Affects §4.2, §6.4 T2 and §6.6.
- **What the model does.** T2 and the engine shift the call hazard (age a − τ). In a TA engine, NAV is created only by calls, so investment is delayed too.
- **What a line does.** A line keeps investment timing, creates a fund liability B^SL that accrues interest, and defers LP calls. LP economic exposure exists before the calls.
- **Consequence.** The "+$4.3bn unfunded by 2031" is uninvested commitment in the engine. Conventional unfunded reports do not "understate" line-financed amounts, because those amounts remain in reported U; what reports understate is the timing and certainty of the calls.
- **Stressed-call formula.** Σλ·U + c^SL·ΣB^SL counts B^SL twice, since it is part of U. Use λ(U − B^SL) + c^SL·B^SL.

**R5 (medium). The CV price parameter is misattributed** (§2.4, §6.8 SELL, §6.10). "≈99% of FMV" is the price of GP-led private-credit secondaries (S12). Replace it with Evercore's PE single-asset CV price distribution or with a Stream-05 PE GP-led price.

**R6 (medium). The ERSRI "reproduction" is overstated** (§1 item 2, §6.11).
- The 46%/−30% match uses the engine's **normal** regime with flat commitments.
- With drought in the stop years (the regime used for all the ADIC lever numbers), NAV falls −21% against Cliffwater's −32%.
- A release of 46–47% against 40% means the engine returns ~15–18% more cash than Cliffwater's model.
- Call rates do not respond to the regime in the engine (M_U = 2.41 in both regimes), whereas MSCI contribution rates fell from 39% in 2021 to 27% in 2023. That likely overstates the speed of drought-period release.
- Present it as a loose consistency check, not a validation.

**R7 (low–medium). Some actions are not the PE group's to take** (§6.3, §6.8).
- "ADIC-level borrowing to fund calls" and b_t (an LP-level NAV-facility draw) appear as G1 decisions. The context file (§1A) assigns portfolio-level borrowing and leverage facilities to Corporate Finance, so G1 can only propose them.
- "LPAC seat required" for extension votes holds only for the first extension. Under the ILPA model, the second is a Majority-in-Interest LP vote.

**R8 (low). Evidence tags are inflated in places.** Some [S] tags sit on inferences:
- **Δp(access) "lower now [S] Bain/PitchBook".** Bain's 15%/20% figures are GP re-raise failure rates. Nothing measures LP access after a skip, so "the chance of losing access after a skip is low today" (§1 item 5) is [I].
- **Fee levels "1.75–2.0% → 1.25–1.5%… [S: ILPA; B&S]".** ILPA leaves fee rates blank, and B&S measure gaps between tiers, not levels.
- **The Lerner–Schoar access-cost implication** (S15).
- **Co-investment ratio ρ ≈ 0.2 "S-derived".** LSMZ's 17% covers all alternative vehicles, including GP-directed sidecars, and those vehicles underperform on average.

**R9 (low). Persistence evidence is applied selectively.**
- Access penalties are aimed at "top VC and growth" on the strength of VC PME 1.70 vs 0.91. The post-2000 at-fundraising figure is 1.20 vs 0.91, and HJKS does not study growth equity.
- The R1 prior uses full-sample K&S (buyout σγ 6.0%, S/N 0.15). K&S's large-fund and US buyout subsamples give σγ ≈ 4.8–5.3% and S/N 0.12–0.14, which is closer to ADIC's likely GP universe.
- The Kalman rule treats signals from overlapping funds as independent. K&S note that overlap slows learning.

**R10 (low). There are internal inconsistencies.**
- PE unfunded is $29bn in §1 item 9 but the working case is $25bn in §6.12.
- `growth_calibration()` (target $29bn) hits its 40%/yr grid ceiling and reaches only $23.1bn. That is an unreported non-convergence. The 10.5% IRR also appears in the mature calibration, so S17 stands.
- The §6.7 objective adds dollar terms to a target-attainment probability without stating an exchange rate.
- It also subtracts "fees" even though T8 places fees inside calls, a possible double count.

## 5. Synthetic-script reproduction

I re-ran `g1_program_calib.py` (with numpy via uv), `g1_control.py`, `g1_fees.py` and `g1_ersri_check.py`, all with `python -I`. Every synthetic number quoted in the dossier reproduces exactly:

| Area | Values reproduced |
|---|---|
| Steady state | M_N 6.88; M_U 2.41; 25.0% distribution rate; 28.3% call rate; drought M_N 16.1; 10.17 after drought |
| Calibration | Pace $5.1bn; U $12.3bn; 2026 NCF +$0.2bn; distribution rate 10.6% |
| Lever table | All rows; 61–66% release on the U path |
| Subscription lines | +$4.3bn |
| Duration | PV duration 4.39 / 7.75 |
| Concentration | Vintage HHI 0.076 |
| Control table | All rows; E/N 1.43 |
| Fees | 2.5–4.6pp spreads; 9.8% → 11.1% net IRR |
| ERSRI | 46%, −30% |

The figures are arithmetically faithful. The issues are in their interpretation (R1, R3, R4, R6).

## 6. Overall reliability

- **Facts and citations: high.** 25 of 28 claims confirmed, 3 corrected, none refuted, no bad citations.
- **Design implications and specification card: medium.** R1 and R2 change headline IC messages: the ranking of a pacing cut against a NAV facility, and the size of access penalties. R4 and R5 mis-specify a transition and a parameter.

**Overall: medium.** Fix S12, S15 and S16 and resolve R1–R5 before the dossier goes to the IC.

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.6 item 3 and the citation-integrity table in `research/literature/G1_pe_primaries.lit.md` §2. The literature audit found no entry that this log wrongly accepted, so there is no erratum. The dossier's own citation corrections are listed at the end of `research/groups/dossiers/G1_pe_primaries.md`.

- §3 Albertus & Denes: added the 2026 *JFQA* journal version (DOI 10.1017/s0022109026102890, confirmed on Crossref and OpenAlex). Its figures were not checked.
- §3 Schillinger, Braun & Cornel: the open item "SSRN ID was not directly confirmed" is marked resolved (DOI 10.2139/ssrn.3434112, per the literature review).
