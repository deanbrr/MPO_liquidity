# G9 literature check: Synthetic data with known ground truth

**Dossier checked:** `research/groups/dossiers/G9_synthetic_data.md` (as of 2026-10-18; about 40 academic works in §10). The dossier was not edited.
**Companion:** `research/groups/verification/G9_synthetic_data.verify.md` (the verification log, "VL").
**Date:** 2026-10-18.

> **Blocker: Consensus was unavailable for this run.**
> - My first query (the Talts et al. title) was rejected three times, about 30 seconds apart, with the monthly-quota message in §6. The quota covers the whole account and resets on 1 November 2026, so I sent no further Consensus calls. **No Consensus search completed.** The same block hit the G1–G6 runs earlier today.
> - **OpenAlex** and **Semantic Scholar** returned HTTP 429 on the first probe.
> - **DBLP** now serves an anti-bot challenge page instead of JSON. I did not try to get around it, so six venue look-ups failed. Five were redone on official proceedings pages; CTGAN's venue rests on its arXiv comment ("Accepted to NeurIPS 2019").
> - **Consequence.** The only Consensus URLs in this file are records that sibling streams saved earlier today, copied character for character. §7 gives a rerun plan.

**Fallbacks (disclosed)**
1. **Crossref REST API [CR].** Used for DOI look-ups and bibliographic searches.
   - Links are Crossref's own `URL` field, which I checked for every DOI cited here.
   - Citation counts are Crossref `is-referenced-by-count` values ("CR"), as of 2026-10-18. They usually run below Consensus or Google Scholar counts.
2. **arXiv export API [AX].** Used for abstracts and version dates.
   - Links are the `id` URLs exactly as returned (`http://`, version-suffixed).
   - arXiv gives no citation counts ("cites n/a").
3. **Official proceedings pages [PG].** Each was fetched once to confirm a venue the APIs could not: PMLR (2 pages), JMLR (1) and the OpenReview API (2 queries). This stands in for the sparing WebFetch use the brief allows. I did not use WebSearch.
4. **Saved Consensus records [CS-saved: stream].** Taken from sibling literature files (streams 02, 03, 04, 06, 07, 09, 10, 12, G3) and not re-run.
5. **The VL**, which fetched NBER and FEDS PDFs for several references.

**Reading conventions**
- Findings restate retrieved abstracts. I read no full texts. **[Inference]** marks anything beyond an abstract.
- "In dossier" means cited in the G9 dossier.
- **Codes:** B1–B25 are annotated papers (§3); F1–F27 are further records (§4.3).
- **Discovery tags:**
  - T01–T14: found by one of the 14 topical searches.
  - K01–K19: known-item look-ups. I identified these papers from domain knowledge, then confirmed metadata and abstract by look-up.

  Every finding still comes from a retrieved abstract or, where stated, a sibling's saved Consensus record.

**Organizational mapping (user-confirmed, 2026-10-18)**
- **Secondaries is a hybrid of direct and fund investments.**
  - The dossier's census already splits the book: 25 fund interests and 15 directs (§6.2).
  - [Inference] Keep that split in the truth tables, so SELL pricing and cash-flow engines are scored separately for each half.
- **Capital Solutions** is the structured and hybrid capital group. Truth engine T5 (contractual instrument with kicker) fits that description.
- **Corporate Finance owns Treasury.** That covers the liquidity gate, contingency funding plan, portfolio facilities, overlay collateral and owner distributions.
  - [Inference] The synthetic `Treasury`, `csa` and `collateral` tables and the sealed owner-demand path D_t (in `truth_world`) belong to that owner.
  - The Treasurer seat's liquidity-gate calls can then be graded against the oracle in V19 (decision regret), separately from the seven groups' asset-level proposals.

---

## 1. Summary

### Citation integrity
- **Scope.** §10 holds about 40 academic works:
  - 11 simulation and synthetic-data papers (refs 14–24);
  - 5 papers on fund performance, NAV behaviour and hedge-fund smoothing (refs 1–4 and 11);
  - 3 forecasting papers (refs 8–10);
  - 13 cited "via streams 04/07" (ref 12);
  - 8 cited "from memory" (ref 13).

  Practitioner, official and press sources are excluded. As the brief requires, I checked the **25 most load-bearing**:
  - 10 of the 11 SBC and synthetic-data references (all but GReaT);
  - the 12 papers behind the calibration anchors and bias parameters;
  - the three † method references the design depends on: Cont, Gretton and Keelin.

  The other 15 are listed under the table, with their status from sibling checks.
- **Result: 24 found, 1 mismatched (minor), 0 not found.** There are no hallucinated or garbled references, which agrees with the VL.
- **Mismatched.** Modrák et al. is cited as 2023. The issue is *Bayesian Analysis* 20(2):461–488 (2025); 2023 is the advance-publication year.
- **Remove the †; the details are confirmed:**
  - Campbell & Sharpe, *JFQA* 44(2):369–390 (2009);
  - Cont, *QF* 1(2):223–236;
  - Gretton et al., *JMLR* 13(25):723–773;
  - Keelin, *Decision Analysis* 13(4):243–277.
- **Add missing details:**
  - Gompers–Gornall–Kaplan–Strebulaev (GGKS), *JFE* 135(1):169–190;
  - Alaa et al., ICML 2022, PMLR 162:290–306;
  - Lopez-Paz & Oquab, ICLR 2017;
  - TabDDPM, PMLR 202:17564–17579;
  - Quant GANs, *QF* 20(9):1419–1440;
  - the Brown–Gredil–Kaplan (BGK) journal DOI;
  - Gelman's (2017) correction to Cook–Gelman–Rubin.
- **Use issue.** Campbell & Sharpe's anchor is "the value of previous months' releases", the latest *realized* value. That calibrates O4's weight on the actual (w_a) or the revision persistence ρ_f, not the weight on underwriting (w_u) [inference; the VL's R8 makes the same point].
- **Cannot be verified from abstracts.** G9's Brown–Ghysels–Gredil (BGG) smoothing figures (weekly λ 0.951, NAV noise 4.6%) are not in the *RFS* abstract.
- **† analogies with no references.** The dossier cites two analogies from memory: OSSEs (§2.2) and simulated actuarial triangles (§5 item 3). This file supplies primary sources:
  - for OSSEs: Errico et al. 2013, Privé et al. 2013, Hoffman & Atlas 2016;
  - for claims simulators: Gabrielli & Wüthrich 2018, Avanzi et al. 2021.

### Backfill: what the dossier misses
I ran 14 topical searches (4 seeds and 10 refinements) and 19 known-item look-ups. Seven gaps matter for design:
1. **Does validation on a synthetic truth transfer to real data?** The dossier cites none of the direct evidence.
   - Advani, Kitagawa & Słoczyński (2019) find that data-calibrated Monte Carlo designs are "worse than random" at choosing minimum-bias estimators.
   - RealCause (2020) states that the best estimators on synthetic data "are unlikely to be the best" on real data.
   - Athey et al. (2024) find that no estimator wins in every setting.
   - **This is the main challenge to the dossier.**
2. **The OSSE literature cuts both ways.**
   - NASA's validated OSSE showed "slightly higher" forecast skill than real data, possibly from "insufficient model error" (Privé et al. 2013).
   - Validation needed correlated observation errors (Errico et al. 2013).
3. **Standards for simulation studies:** ADEMP (Morris et al. 2019) and preregistration against questionable research practices (Pawel et al. 2024).
4. **SBC has moved on.**
   - ECDF simultaneous bands (Säilynoja et al. 2022) are the method behind V16, but the dossier does not cite them.
   - Posterior SBC checks calibration conditional on the observed data (2025).
   - A classifier-based calibration test (2023) and SBC-based recalibration (2026) are now available.
   - Average coverage is not enough (2026), and neural posteriors are often overconfident (2022).
5. **Evaluating synthetic data.**
   - Treating synthetic data as real causes downstream errors (van Breugel et al. 2023).
   - Statistically realistic data can still fail analytical queries (TabQueryBench 2026).
   - Distance-based privacy proxies fail (DCR Delusion 2025).
6. **Small data and regime ground truth in finance:**
   - a generative market simulator built for small data (Bühler et al. 2020);
   - semi-synthetic series with known regime breaks (ProteuS 2025).
7. **Agents.** Probabilistic programs written by LLMs are often statistically wrong while passing unit tests. The right verifier is calibration, meaning posterior predictive checks plus SBC (Xu et al. 2026).

**PE calibration.** Kang (2026; Preqin, 7,904 funds, 1982–2025) adds cash-flow timing targets that reach recent vintages. That eases the dossier's §8 concern about outdated calibration vintages.

### Bottom line [inference]
- The structural generator of record is still the right core while ADIC has no data.
- But the dossier over-reads what a synthetic book can prove. The fixes:
  - Use SYN-ADIC-177 for computational correctness, recovery of injected biases and robustness envelopes.
  - Do not use it alone to pick among estimators.
  - Inject model error and correlated observation errors.
  - Preregister the generator variants.
  - Plan a semi-synthetic release once ADIC data arrive.

---

## 2. Citation-integrity table (25 checked)

**Status key**
- **found:** metadata match; additions are noted.
- **mismatched:** the work exists, but its metadata differ; corrected metadata are given.
- **not found:** no record located.

The Consensus URL column shows sibling records only, because of the quota; otherwise it reads "none".

| # | Dossier citation | Status | Corrected metadata / note | Consensus URL |
|---|---|---|---|---|
| 1 | Talts, Betancourt, Simpson, Vehtari & Gelman (2018, rev. 2020), arXiv:1804.06788 | found [AX] | v1 18 Apr 2018; v2 21 Oct 2020. No journal version in Crossref. Crossref returned instead the SBC chapters of Gelman et al., *Bayesian Workflow* (Chapman & Hall/CRC, 2026; F15). | none |
| 2 | Cook, Gelman & Rubin (2006), *JCGS* 15(3):675–692 | found [CR] | DOI 10.1198/106186006x136976; CR 280. **Add** Gelman (2017), "Correction to Cook, Gelman, and Rubin (2006)", *JCGS* 26(4):940, DOI 10.1080/10618600.2017.1377082. Confirmed in Crossref; the VL also recommends it. | none |
| 3 | Modrák et al. (2023), *Bayesian Analysis*, doi:10.1214/23-BA1404 | **mismatched (year; minor)** | ***Bayesian Analysis* 20(2):461–488 (2025)**. 2023 is the advance-publication year: arXiv v3 (19 Oct 2023) says "upcoming in Bayesian Analysis". All eight authors confirmed. CR 29. The dossier's quote ("an especially useful test quantity") is verbatim in the abstract. | none |
| 4 | Brown, Gredil & Kaplan (2019), *JFE* 132(2) (online 2018); NBER WP 22493 | found [CR] [CS-saved: 07] | *JFE* 132(2):267–297, **DOI 10.1016/j.jfineco.2018.10.011** (add it); CR 186. NBER (2016, DOI 10.3386/w22493) and SSRN (2013, DOI 10.2139/ssrn.2271690) versions exist. | https://consensus.app/papers/details/3331159853ab59dea783df670c91ee0a/?utm_source=claude_desktop |
| 5 | Harris, Jenkinson & Kaplan (2014), *JF* 69(5):1851–1882; NBER WP 17874 | found [CR] [CS-saved: 04] | DOI 10.1111/jofi.12154; CR 522 (Consensus 537). The published abstract covers "nearly 1,400 U.S. buyout and venture capital funds" (Burgiss). The dossier's "over 200 investment programs" and PME 1.20/1.11 come from the working paper (VL). | https://consensus.app/papers/details/db976ea21cdc505480145e648346890d/?utm_source=claude_desktop |
| 6 | Gompers, Gornall, Kaplan & Strebulaev, NBER WP 22587 (2016); *JFE* "(volume and pages not verified)" | found [CR] | ***JFE* 135(1):169–190 (2020)**, DOI 10.1016/j.jfineco.2019.06.011; CR 795. Crossref holds no abstract, so the survey figures were not re-checked here (see the VL). | none |
| 7 | Jenkinson, Landsman, Rountree & Soonawalla (2020), *TAR* 95(1):191–210 | found [CR] [CS-saved: 07] | DOI 10.2308/accr-52486; online 2019; CR 50. The abstract confirms 384 VC and 195 buyout funds (1988–2016), little buyout bias and aggressively biased VC NAVs. It adds that accuracy was worse in the first half of the sample, even though NAVs were then more conservative. | https://consensus.app/papers/details/44d91cea6b8b53b481621e6ed4e6ef9e/?utm_source=claude_desktop |
| 8 | Getmansky, Lo & Makarov (2004), *JFE* 74(3):529–609 | found [CR] | DOI 10.1016/j.jfineco.2004.04.001; CR 790. Consensus indexes only Getmansky's 2004 thesis, which carries the same abstract (streams 04, 09, G3, G5, G6). | thesis record: https://consensus.app/papers/details/4e43d079332f5046860f2f39350f56f9/?utm_source=claude_desktop |
| 9 | Campbell & Sharpe (2007), FEDS 2007-12 ("published *JFQA* 2009 †") | found [CR]; **remove †** | ***JFQA* 44(2):369–390 (2009)**, DOI 10.1017/s0022109009090127; CR 155. **Use note:** the abstract tests bias "toward the value of previous months' releases", the latest realized value. That maps to O4's weight on the actual (w_a) or to the revision persistence ρ_f, not to the weight on underwriting (w_u) [inference; same point as VL R8]. The "on the order of 30 percent" figure is not in the abstract. | none |
| 10 | Coibion & Gorodnichenko (2015), *AER* 105(8):2644–78 | found [CR] | DOI 10.1257/aer.20110306; CR 1094. The full title adds ": A Simple Framework and New Facts". The abstract also reports "state-dependence in the expectations formation process", which supports making the bias regime-dependent. | none |
| 11 | Bordalo, Gennaioli, Ma & Shleifer (2020), *AER* 110(9):2748–82 | found [CR] [CS-saved: 07] | DOI 10.1257/aer.20181219; CR 593. The Consensus record shows the year as 2018 (421 citations). The abstract confirms that individuals overreact and consensus forecasts under-react. | https://consensus.app/papers/details/4fabd9f27a1359a5a8e026ed6e04a384/?utm_source=claude_desktop |
| 12 | Ben-David, Graham & Harvey (2013) (ref 12, via stream 07) | found [CR] [CS-saved: 07] | *QJE* 128(4):1547–1584, DOI 10.1093/qje/qjt023; CR 737. The abstract confirms more than 13,300 distributions and 36% coverage of 80% intervals. | https://consensus.app/papers/details/c521fdc6c47d5eb9bae7b451ebce14fc/?utm_source=claude_desktop |
| 13 | Takahashi & Alexander (2002) (ref 12, via stream 04) | found [CR] [CS-saved: 06] | "Illiquid Alternative Asset Fund Modeling", *JPM* 28(2):90–100, DOI 10.3905/jpm.2002.319836; CR 56 (Consensus 68). | https://consensus.app/papers/details/da7ee2d8587e575f99e3a36a590d2be6/?utm_source=claude_desktop |
| 14 | Brown, Ghysels & Gredil (2023) (ref 12, via stream 04): "weekly BGG λ = 0.951 … NAV noise mean 4.6%" | found [CR] [CS-saved: 07, SSRN record] | *RFS* 36(3):945–986 (online 2022), DOI 10.1093/rfs/hhac045; CR 28. The λ and noise figures are not in the abstract, so they are unverified here. The abstract gives β ≈ 1.0 (1.4) and total risk of 33% (40%) for buyout (venture). It also says "reporting quality appear[s] to persist by manager". | https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop |
| 15 | Nadauld, Sensoy, Vorkink & Weisbach (2019) (ref 12, via stream 04): "+5pp/yr" | found [CR] [CS-saved: 07, 03, G3] | *JFE* 132(3):158–181, DOI 10.1016/j.jfineco.2018.11.007; CR 90. Stream 07 confirmed the figure from the published abstract: buyers' PME 1.023 against sellers' 0.976, about 5 pp a year. | https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop |
| 16 | Xu, Skoularidou, Cuesta-Infante & Veeramachaneni (2019), CTGAN, NeurIPS 2019 | found [AX] | arXiv 1907.00503 (v2 28 Oct 2019); the arXiv comment reads "Accepted to NeurIPS 2019". Its own benchmark used "7 simulated and 8 real datasets". | none |
| 17 | Kotelnikov, Baranchuk, Rubachev & Babenko (2023), TabDDPM, ICML 2023 (PMLR 202) | found [AX] [PG] | **PMLR 202:17564–17579** (PMLR page). The abstract confirms "superiority over existing GAN/VAE alternatives". | none |
| 18 | Alaa, van Breugel, Saveliev & van der Schaar (2022), arXiv:2102.08921 | found [AX] [PG] | **ICML 2022, PMLR 162:290–306** (add the venue). The abstract confirms α-Precision, β-Recall and Authenticity. | none |
| 19 | Lopez-Paz & Oquab (2017), arXiv:1610.06545 | found [AX] [PG] | **ICLR 2017** (OpenReview: "ICLR 2017 Poster"). The abstract confirms that under the null, held-out accuracy should remain "near chance-level". | none |
| 20 | Wiese, Knobloch, Korn & Kretschmer (2020), Quant GANs, *Quantitative Finance* | found [CR] [AX] | ***QF* 20(9):1419–1440**, DOI 10.1080/14697688.2020.1730426; CR 273. | none |
| 21 | Potluru et al. (2023), arXiv:2401.00081 | found [AX] | Posted 29 Dec 2023; v2 20 Mar 2024 ("journal submission"). No journal record in Crossref. | none |
| 22 | Qian, Cebere & van der Schaar (2023), "Synthcity", arXiv:2301.07573 | found [AX]; version note | The full arXiv title is "Synthcity: facilitating innovative use cases of synthetic data in different data modalities". OpenReview also lists a NeurIPS 2023 Datasets and Benchmarks poster, "Synthcity: a benchmark framework for diverse use cases of tabular synthetic data" [PG]. I did not retrieve that paper's authors, so whether it is the same work is unverified. | none |
| 23 | Cont (2001), *Quantitative Finance* 1(2) † | found [CR]; **remove †** | "Empirical properties of asset returns: stylized facts and statistical issues", *QF* 1(2):223–236, DOI 10.1080/713665670; CR 2720. | none |
| 24 | Gretton et al. (2012), *JMLR* 13 † | found [PG]; **remove †** | "A Kernel Two-Sample Test", *JMLR* 13(25):723–773 (JMLR page). Not in Crossref. | none |
| 25 | Keelin (2016), "The metalog distributions", *Decision Analysis* 13(4) † | found [CR]; **remove †** | *Decision Analysis* 13(4):243–277, DOI 10.1287/deca.2016.0338; CR 69. The abstract confirms closed-form quantile functions and wide shape flexibility, which supports §3.4. | none |

**Sources for the [PG] confirmations:**
- PMLR: https://proceedings.mlr.press/v162/alaa22a.html and https://proceedings.mlr.press/v202/kotelnikov23a.html
- JMLR: https://jmlr.org/papers/v13/gretton12a.html
- OpenReview: https://api.openreview.net/notes/search?term=Revisiting%20Classifier%20Two-Sample%20Tests&limit=3 and https://api2.openreview.net/notes/search?term=Synthcity&limit=3

### Not checked here: the 15 academic works outside the top 25

| Reference (as cited) | Status from sibling streams | Saved Consensus URL |
|---|---|---|
| Korteweg & Sorensen (2017) | found (stream 07): *JFE* 124(3), DOI 10.1016/j.jfineco.2017.03.006 | https://consensus.app/papers/details/a0bf5a58fd485ea895fabd5c39cb76ce/?utm_source=claude_desktop |
| Barber & Yasuda (2017) | found (stream 07): *JFE* 124(1), DOI 10.1016/j.jfineco.2017.01.001 | https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop |
| Jenkinson, Sousa & Stucke (2013) | found (stream 07): SSRN, DOI 10.2139/ssrn.2229547 | https://consensus.app/papers/details/e297da1e0d0658d8ae2ca7a7a7b6987c/?utm_source=claude_desktop |
| Harris, Jenkinson, Kaplan & Stucke (2020) | found, working-paper record (stream 07); *JCF* 81 (2023) per G1 | https://consensus.app/papers/details/c9d05f78edee5236895cb0968f1c5e62/?utm_source=claude_desktop |
| Gompers, Kaplan & Mukharlyamov (2016) | found (stream 07): *JFE* 121(3) | https://consensus.app/papers/details/9c44ffc9ab6a5bdbaeebc0798a59f4d5/?utm_source=claude_desktop |
| Robinson & Sensoy (2016) | found (streams 03, 04): *JFE* 122(3), DOI 10.1016/j.jfineco.2016.09.008 | https://consensus.app/papers/details/86bf821b6ba65861a9da20fed7862965/?utm_source=claude_desktop |
| Ljungqvist & Richardson (2003) | not found in Consensus; exists (stream 04 web check, NBER WP 9454) | none |
| Flyvbjerg, Skamris Holm & Buhl (2005) | found (stream 07), with a notice of redundant publication | https://consensus.app/papers/details/cdbd141e345f53678560f7f4ee38f3ed/?utm_source=claude_desktop |
| Andonov & Rauh (2018) | found, working-paper record (stream 07) | https://consensus.app/papers/details/ed7719fccddd54da8e7194de9784a9d6/?utm_source=claude_desktop |
| Fang, Ivashina & Lerner (2015), *JFE* 116(1) † | Stream 02 holds a Consensus record (2014) titled "The Disintermediation of Financial Markets: Direct Investing in Private Equity"; the journal details were not checked | https://consensus.app/papers/details/4e0c268caabc5b468d053656985a3deb/?utm_source=claude_desktop |
| Braun, Jenkinson & Schemmerl (2020), *JFE* 136(1) † | Stream 02 Consensus record: *JFE* 2020, SSRN DOI 10.2139/ssrn.2871458 | https://consensus.app/papers/details/74305f05d7e758dfbc4c1b624c2fa5db/?utm_source=claude_desktop |
| Barras, Scaillet & Wermers (2010), *JF* 65(1) † | found (G5, Crossref): *JF* 65(1):179–216, DOI 10.1111/j.1540-6261.2009.01527.x | none |
| Aas et al. (2009) † (via stream 10) | **not checked by any stream** (stream 10 listed it as unchecked) | none |
| López de Prado (2018), *Advances in Financial Machine Learning* † | not checked | none |
| Borisov et al. (2023), GReaT | not checked | none |

**A body-only mention with no §10 entry.** The "Geltner/BGG filter" in §2.5 and O1 has no reference. G6's Crossref check gives Geltner, *Journal of Real Estate Research* 8(3):325–345. [Inference] Add an entry.

---

## 3. Annotated bibliography (25 papers)

### A. Does validation on a synthetic truth transfer to real data?

**B1. [Mostly harmless simulations? Using Monte Carlo studies for estimator selection](https://doi.org/10.1002/jae.2724)** (T05) · **challenge**
- Arun Advani, Toru Kitagawa, Tymon Słoczyński · 2019 · *Journal of Applied Econometrics* 34(6):893–910 · CR 13 · DOI 10.1002/jae.2724 · In dossier: no
- **Finding.** The paper tests two proposals for "empirically motivated" Monte Carlo studies to select a treatment-effect estimator; they are uninformative except under restrictive conditions. Where true performance was known, both were "worse than random at selecting estimators that minimize absolute bias" (better for mean squared error), and "a simple bootstrap is at least as good and often better".
- **Relevance.** This is the most direct test of G9's premise that a calibrated synthetic book can rank ADIC's estimators. [Inference] Use G9 for correctness, bias recovery and robustness envelopes. Do not let synthetic rankings alone choose among the stream-07 fusion variants.

**B2. [RealCause: Realistic Causal Inference Benchmarking](http://arxiv.org/abs/2011.15007v2)** (T07) · **challenge**
- Brady Neal, Chin-Wei Huang, Sunand Raghupathi · 2020 (v2 2021) · arXiv preprint · cites n/a · In dossier: no
- **Finding.** "The best causal estimators on synthetic data are unlikely to be the best causal estimators on real data." Generative models fitted to real data give a benchmark that "both yields ground-truth and is realistic"; the authors use it to evaluate more than 1,500 estimators.
- **Relevance.** This contradicts §2.6's claim that learned generators cannot carry truth or counterfactuals. [Inference] Plan a semi-synthetic release fitted to ADIC holdings once data arrive, with the truth defined by the fitted mechanisms.

**B3. [Using Wasserstein Generative Adversarial Networks for the design of Monte Carlo simulations](https://doi.org/10.1016/j.jeconom.2020.09.013)** (T06; journal record from K01)
- Susan Athey, Guido W. Imbens, Jonas Metzger, Evan Munro · 2024 · *Journal of Econometrics* 240(2):105076 · CR 38 · DOI 10.1016/j.jeconom.2020.09.013 · NBER WP 26566 (2019) · abstract from [arXiv 1909.02210](http://arxiv.org/abs/1909.02210v3) · In dossier: no
- **Finding.** WGANs can generate artificial data that "closely mimics real economic datasets, while limiting the degrees of freedom for the researcher". Comparing average-treatment-effect estimators across three real-data settings, "there is not one estimator that outperforms the others in all three settings".
- **Relevance.** This supports setting-specific validation; ADIC's groups (PE, Credit, hedge funds) are different settings. [Inference] Rank estimators separately by group, and show ranking stability across generator variants on IC pages.

**B4. [Validation of the forecast skill of the Global Modeling and Assimilation Office Observing System Simulation Experiment](https://doi.org/10.1002/qj.2029)** (K02) · **challenge**
- N. C. Privé, R. M. Errico, K.-S. Tai · 2013 · *Quarterly Journal of the Royal Meteorological Society* 139(674):1354–1363 · CR 29 · DOI 10.1002/qj.2029 · In dossier: no (OSSEs are cited from memory, †)
- **Finding.** The OSSE's forecast skill was "slightly higher than for real data, with smaller observation impacts overall, possibly due to insufficient model error in the OSSE". The ranking of observation impacts mostly agreed with real data, but not for individual satellite channels.
- **Relevance.** The dossier's closest analogue reports that even a validated synthetic world was too easy. [Inference]
  - Treat estimator scores on SYN-ADIC-177 as upper bounds.
  - Inject model error that the estimators do not model.
  - Report a synthetic-to-real skill haircut once ADIC data exist.

**B5. [Development and validation of observing-system simulation experiments at NASA's Global Modeling and Assimilation Office](https://doi.org/10.1002/qj.2027)** (K02)
- Ronald M. Errico, Runhua Yang, Nikki C. Privé, King-Sheng Tai, Ricardo Todling, Meta E. Sienkiewicz, Jing Guo · 2013 (online 2012) · *QJRMS* 139(674):1162–1178 · CR 98 · DOI 10.1002/qj.2027 · In dossier: no
- **Finding.** Validation compares statistics from assimilating simulated observations with those from real observations. The OSSE "is validated remarkably well", but only after the authors used "horizontally correlated observation errors" for some instruments. The simulated errors cover both instrument and representativeness components.
- **Relevance.** This is a primary source for §2.2 and a concrete gate. [Inference]
  - Compare the fusion engine's innovations (forecast minus realized; NAV revisions) on synthetic and on ADIC data.
  - Add correlated reporting and forecast errors to O1 and O4.

**B6. [Using simulation studies to evaluate statistical methods](https://doi.org/10.1002/sim.8086)** (K12)
- Tim P. Morris, Ian R. White, Michael J. Crowther · 2019 · *Statistics in Medicine* 38(11):2074–2102 · CR 1286 · DOI 10.1002/sim.8086 · In dossier: no
- **Finding.** Simulation studies are valuable because some "truth" is known, but they are "often poorly designed, analyzed, and reported". The tutorial structures them by aims, data-generating mechanisms, estimands, methods and performance measures ("ADEMP"), and covers how to estimate performance measures.
- **Relevance.** G9's experiments (E1–E4) and gates (V16–V19) lack this protocol. [Inference] Ship an ADEMP card with Monte Carlo standard errors for each release gate.

**B7. [Pitfalls and potentials in simulation studies: Questionable research practices in comparative simulation studies allow for spurious claims of superiority of any method](https://doi.org/10.1002/bimj.202200091)** (K13)
- Samuel Pawel, Lucas Kook, Kelly Reeve · 2024 (online 2023) · *Biometrical Journal* 66(1) · CR 31 · DOI 10.1002/bimj.202200091 · In dossier: no
- **Finding.** With questionable research practices, a method with no expected gain is easily made to "appear superior" in a comparative simulation study. The authors recommend preregistered protocols, neutral studies, and code and data sharing.
- **Relevance.** G9's generator, misspecification variants and estimators all come from one lab. [Inference] Preregister and hash the variants, estimands and pass criteria before scoring, and make the scorer independent of the estimators' authors.

### B. Simulation-based calibration and posterior checks

**B8. [Validating Bayesian Inference Algorithms with Simulation-Based Calibration](http://arxiv.org/abs/1804.06788v2)** · in dossier
- Sean Talts, Michael Betancourt, Daniel Simpson, Aki Vehtari, Andrew Gelman · 2018 (v2 2020) · arXiv · cites n/a
- **Finding.** SBC validates inferences from any algorithm that produces posterior samples. It catches inaccurate computation and inconsistencies in the model implementation, summarizes problems graphically, and is "a critical part of a robust Bayesian workflow".
- **Relevance.** Confirms §2.1 and §3.6. The current canonical reference is the 2026 CRC book *Bayesian Workflow* (F15).

**B9. [Simulation-Based Calibration Checking for Bayesian Computation: The Choice of Test Quantities Shapes Sensitivity](https://doi.org/10.1214/23-ba1404)** · in dossier
- Martin Modrák, Angie H. Moon, Shinyoung Kim, Paul Bürkner, Niko Huurre, Kateřina Faltejsková, Andrew Gelman, Aki Vehtari · 2025 · *Bayesian Analysis* 20(2):461–488 · CR 29 · DOI 10.1214/23-ba1404 · arXiv [2211.02383](http://arxiv.org/abs/2211.02383v3)
- **Finding.** Data-dependent test quantities let SBC detect, in principle, any problem with the posterior, including a posterior equal to the prior; "the joint likelihood of the data is an especially useful test quantity". The paper also separates SBC from checks based on the data-averaged posterior.
- **Relevance.** Confirms the dossier's quote. [Inference] Make the joint log-likelihood a mandatory test quantity in V16.

**B10. [Graphical test for discrete uniformity and its applications in goodness-of-fit evaluation and multiple sample comparison](https://doi.org/10.1007/s11222-022-10090-6)** (K09)
- Teemu Säilynoja, Paul-Christian Bürkner, Aki Vehtari · 2022 · *Statistics and Computing* 32(2) · CR 52 · DOI 10.1007/s11222-022-10090-6 · In dossier: no
- **Finding.** Simultaneous confidence bands for the whole ECDF of PIT values, built by simulation and optimization, give a graphical test of uniformity. They work when the reference is a finite sample, which is "useful, for example, for simulation-based calibration".
- **Relevance.** This is the method behind V16's "ECDF inside 95% bands", which the dossier does not cite. [Inference] Use the same bands for V18's PIT checks.

**B11. [Posterior SBC: Simulation-Based Calibration Checking Conditional on Data](http://arxiv.org/abs/2502.03279v2)** (T02)
- Teemu Säilynoja, Marvin Schmitt, Paul-Christian Bürkner, Aki Vehtari · 2025 · arXiv · cites n/a · In dossier: no
- **Finding.** Standard SBC tests inference only for parameters that are plausible under the prior. Posterior SBC validates inference "conditionally on observed data"; the paper shows three case studies, one with amortized neural inference.
- **Relevance.** This partly answers the dossier's §8 risk of false comfort from SBC. [Inference] When ADIC data arrive, rerun SBC in the region of parameter space that ADIC's data imply (a new gate, V16b).

**B12. [Discriminative calibration: Check Bayesian computation from simulations and flexible classifier](http://arxiv.org/abs/2305.14593v2)** (T02)
- Yuling Yao, Justin Domke · 2023 · NeurIPS 2023 (per the arXiv comment) · cites n/a · In dossier: no
- **Finding.** Rank-based SBC has an ad hoc test statistic, makes interactions hard to examine, struggles with multiple testing, and its p-value is not a divergence measure. A learned classifier "typically has a higher statistical power" and returns an interpretable divergence measure of miscalibration.
- **Relevance.** G9's engines carry dozens of parameters (group biases, credibility weights, smoothing), so per-parameter χ² tests run into multiple testing. [Inference] Add a joint classifier-based test to V16.

**B13. [Approximate posterior recalibration](http://arxiv.org/abs/2603.20068v1)** (T02)
- Tiffany Cai, Philip Greengard, Ben Goodrich, Andrew Gelman · 2026 · arXiv · cites n/a · In dossier: no
- **Finding.** Two methods extend SBC to widen approximate posterior intervals so that they aim for marginal calibration. The paper discusses hierarchical models.
- **Relevance.** G9's prototype E4 found 80% intervals covering only 73%. [Inference] Offer SBC-based widening as a stopgap while the model is repaired, badged "recalibrated" in IC outputs.

**B14. [A Trust Crisis In Simulation-Based Inference? Your Posterior Approximations Can Be Unfaithful](http://arxiv.org/abs/2110.06581v3)** (K07)
- Joeri Hermans, Arnaud Delaunoy, François Rozet, Antoine Wehenkel, Volodimir Begy, Gilles Louppe · 2022 (TMLR version; arXiv v1 2021) · cites n/a · In dossier: no
- **Finding.** Every benchmarked simulation-based inference algorithm (NPE, NRE, SNL and ABC variants) "can yield overconfident posterior approximations". Ensembles of posterior surrogates give more reliable approximations.
- **Relevance.** If ADIC adopts neural or amortized estimators (nowcast surrogates, agent-trained models), overconfidence is the expected failure. [Inference] Make V17 one-sided against overconfidence, and require ensembles for neural estimators.

**B15. [Coverage is not enough: Frequentist tests of simulation-based inference for primordial non-Gaussianity](http://arxiv.org/abs/2605.00980v2)** (T13) · **challenge**
- Toka Alokda, Cristiano Porciani, Alexander Eggemeier · 2026 · *Astronomy & Astrophysics* 714:A66 (per the arXiv journal reference) · cites n/a · In dossier: no
- **Finding.** Coverage diagnostics under the prior predictive "probe calibration only in an averaged sense and do not constrain posterior behavior at fixed parameter value". The authors' simulation-based posteriors were often underconfident "despite passing coverage tests".
- **Relevance.** V16 and V17 are average-coverage gates. [Inference] Add coverage tests at fixed parameter values at decision-relevant corners: the drought regime, high optimism bias and high vintage ICC.

**B16. [L-C2ST: Local Diagnostics for Posterior Approximations in Simulation-Based Inference](http://arxiv.org/abs/2306.03580v2)** (T13)
- Julia Linhart, Alexandre Gramfort, Pedro L. C. Rodrigues · 2023 · NeurIPS 2023 (per the arXiv comment) · cites n/a · In dossier: no
- **Finding.** Most methods evaluate posterior estimators only on average over observations. L-C2ST evaluates them locally, at any given observation, without samples from the true posterior; on standard benchmarks it outperformed local coverage tests based on highest predictive density.
- **Relevance.** It lets ADIC check calibration at its own observed book. [Inference] Pair it with B11 once ADIC data exist. It extends the dossier's use of C2ST from realism checks to inference checks.

**B17. [OASIS: Observation-Aware Simulation-Based Inference via Distributional Matching](http://arxiv.org/abs/2606.22572v1)** (T13)
- Arya Farahi, Conghao Zhou, Ritwik Vashistha · 2026 · arXiv · cites n/a · In dossier: no
- **Finding.** OASIS embeds the observation model (measurement error, selection effects) in the simulator and infers from the distribution of observed data, using an MMD-reweighted pseudo-posterior. It delivered robust parameter recovery and calibrated uncertainty under heterogeneous, non-Gaussian noise.
- **Relevance.** It formalizes G9's world / truth / observation split on the inference side. [Inference]
  - The stream-04 nowcast and the stream-07 fusion engine should consume G9's observation operator (smoothing, lags, fundraising inflation) rather than treat reported NAVs as noisy truth.
  - The same method can calibrate G9's own parameters to published distributions.

### C. Using and auditing synthetic data

**B18. [Synthetic data, real errors: how (not) to publish and use synthetic data](http://arxiv.org/abs/2305.09235v2)** (T14)
- Boris van Breugel, Zhaozhi Qian, Mihaela van der Schaar · 2023 · ICML 2023 (per the arXiv comment) · cites n/a · In dossier: no
- **Finding.** Using synthetic data "as if it is real" yields downstream models and analyses that do not generalize to real data. A Deep Generative Ensemble, which approximates a posterior over the generator's parameters, improves training, evaluation and uncertainty quantification, with the largest gains in low-density regions.
- **Relevance.** This formalizes the dossier's misspecification ensemble, and ADIC's decision-relevant tails (crisis regime, tail-end funds) are exactly the low-density regions. [Inference] Score estimators across an ensemble of generator-parameter draws, not on one SYN-ADIC-177 vintage.

**B19. [TabQueryBench: A Query-Centric Benchmark for Synthetic Tabular Data](http://arxiv.org/abs/2607.03926v2)** (T04)
- Jialin Zhang, Fenghao Dong, Yajie Zhou, Vyas Sekar, Shinan Liu · 2026 · arXiv · cites n/a · In dossier: no
- **Finding.** Across 49 datasets and 11 generators, the best model reached query-centric fidelity of 0.76 ± 0.23, against 1.00 for real data. Failures concentrate in high-cardinality attributes and in local or tail queries: synthetic data "can appear statistically realistic yet still fail to preserve the analytical behavior of real data".
- **Relevance.** IC questions are roll-ups by group, manager and vintage (high-cardinality) and tail queries. [Inference] Add query-centric gates next to V15's C2ST.

**B20. [The DCR Delusion: Measuring the Privacy Risk of Synthetic Data](http://arxiv.org/abs/2505.01524v1)** (T08) · **challenge**
- Zexi Yao, Nataša Krčo, Georgi Ganev, Yves-Alexandre de Montjoye · 2025 · arXiv · cites n/a · In dossier: no
- **Finding.** Distance to Closest Record and other distance-based metrics "fail to identify privacy leakage". Datasets these proxies deem private, from Baynet, CTGAN and diffusion models alike, are "highly vulnerable to MIAs". The authors urge membership-inference attacks (MIAs) as the standard.
- **Relevance.** §8 relies on "authenticity metrics" for memorization audits. [Inference]
  - Require MIA-based audits before output from any generator fitted to ADIC data leaves the lab.
  - Authenticity is also a similarity-based copying score and may share the weakness; the abstract does not test it.

### D. Finance-specific generators and ground truth

**B21. [A Data-driven Market Simulator for Small Data Environments](http://arxiv.org/abs/2006.14498v1)** (K15)
- Hans Bühler, Blanka Horvath, Terry Lyons, Imanol Perez Arribas, Ben Wood · 2020 · arXiv · cites n/a · In dossier: no
- **Finding.** Generative market simulation is model-free in principle, but its modeling choices decide the features of the simulated paths. Most generative models need large training sets; this one "works reliably in environments where the amount of available training data is notoriously small", using a rough-paths perspective combined with a parsimonious VAE.
- **Relevance.** This weakens §2.6's objection that learned tails are thin when n is small, at least for public sleeves and overlay drivers. [Inference] Use it as a realism challenger to the regime block bootstrap (§3.2), judged with the stylized-facts suite.

**B22. [ProteuS: A Generative Approach for Simulating Concept Drift in Financial Markets](http://arxiv.org/abs/2509.11844v1)** (T11)
- Andrés L. Suárez-Cetrulo, Alejandro Cervantes, David Quintana · 2025 · arXiv · cites n/a · In dossier: no
- **Finding.** Real financial data lack a ground truth for regime changes. ProteuS fits ARMA-GARCH models to ETF regimes and simulates gradual and abrupt transitions between them, giving "a known ground truth of regime changes"; the generated market states overlap substantially.
- **Relevance.** G9 seals the regime path S_t in `truth_world` but does not specify the shape of transitions. [Inference] Include both gradual and abrupt transitions, with timestamps, in R1 and R2. That lets the lab grade stream-10 regime detection and the agents' "explain the DPI shortfall" task.

### E. Domain analogues and PE calibration

**B23. [An Individual Claims History Simulation Machine](https://doi.org/10.3390/risks6020029)** (K04)
- Andrea Gabrielli, Mario V. Wüthrich · 2018 · *Risks* 6(2):29 · CR 58 · DOI 10.3390/risks6020029 · In dossier: no (the analogy is cited from memory, †)
- **Finding.** A stochastic simulation machine based on neural networks, "fully calibrated ... based on real non-life insurance data", lets anyone simulate a synthetic portfolio of individual claims histories and "back-test thier [sic] preferred claims reserving method".
- **Relevance.** A primary source for §5 item 3. [Inference] Like G9, it is a calibrated generator published for back-testing. ADIC could publish a non-sensitive SYN-ADIC benchmark for external model validation in the same way.

**B24. [Cash-Flow Timing in Private Markets: Evidence from the PFD Framework](https://consensus.app/papers/details/bfcee2acb48956d2b7c78208c910bb46/?utm_source=claude_desktop)** [CS-saved: 04, 10]
- Kang Shuang · 2026 · venue not shown (DOI 10.3905/jpmi.2026.1.013) · 0 cit. · In dossier: no
- **Finding.** This is stream 10's summary of the saved Consensus record; I did not retrieve the abstract myself. Preqin records for 7,904 funds (1982–2025) show that the timing of contributions, breakeven and distributions differs systematically by asset class, vintage, strategy and fund size. Funds with similar end performance can have different liquidity profiles. The paper calibrates Takahashi–Alexander to these timing metrics.
- **Relevance.** G9's PE gates miss the shape of cash-flow timing and recent vintages (§8). V5 tests only DPI by age against CA 2019, and V6 only rates by regime. [Inference] Add gates for contribution timing, breakeven and distribution timing by strategy and vintage, and check the Preqin licence.

### F. Agents

**B25. [Calibration, Not Compilation: Detecting and Repairing Misspecified Probabilistic Programs Written by Language Models](http://arxiv.org/abs/2606.31630v1)** (T12)
- Jian Xu, Delu Zeng, John Paisley, Qibin Zhao · 2026 · arXiv · cites n/a · In dossier: no
- **Finding.** Of the runnable probabilistic programs LLMs wrote from scratch, 15–47% were statistically misspecified, and unit tests caught none.
  - A calibration oracle (posterior predictive checks, SBC, sampler diagnostics and held-out density) flagged bugs with AUC 0.97 when handed a correct reference program, which the authors call an upper bound. A reference-free version reached 62–78%.
  - In repair loops, unit-test feedback was "significantly worse than no feedback at all".
- **Relevance.** Directly relevant to the agentic layer, which will write the fusion, nowcast and regime code. [Inference] Make G9's SBC and posterior-predictive harness the verifier for every agent-authored statistical program (C4 rubric verification), not unit tests.

---

## 4. Missed-but-important papers: concrete design implications

Every item below is [Inference] unless stated otherwise. Codes refer to §3 and §4.3; "#n" refers to rows of the §2 table.

### 4.1 By framework element

**State variables and generator content**
1. **A model-error component (B4).**
   - Add a latent structural deviation to the truth engine that no production estimator models: for example, a time-varying β, or a nonlinear exit hazard in drought.
   - Once ADIC data allow, calibrate its size so that estimator skill on synthetic data matches skill on real data. This is the OSSE validation step.
   - Seal it in `truth_world`.
2. **Correlated observation errors (B5; BGG abstract, #14).**
   - Replace O1's independent NAV noise, η ~ N(0, 0.04²), with η = η^admin + η^GP + η^idio.
   - Give the smoothing λ_s and the noise a manager-level random effect. BGG finds that "reporting quality appear[s] to persist by manager".
   - Add a time-varying group "house view" shock to b^f in O4.
3. **Era-dependent NAV bias (JLRS abstract, #7).** Let the conservatism and bias parameters differ by vintage era. NAV accuracy was worse in the first half of 1988–2016, while NAVs were then more conservative.
4. **State-dependent expectations (Coibion–Gorodnichenko abstract, #10).** Make b^f and ρ_f regime-dependent in the default generator, not only in a misspecification variant.
5. **Regime transitions with labels (B22).** R1 and R2 worlds include both gradual and abrupt transitions, with the break dates stored in `truth_world`.
6. **Truth for owner demand and collateral (Corporate Finance's role, user-confirmed).** Seal the demand path D_t and the CSA calls, so the Treasurer seat's liquidity-gate decisions can be graded in V19.

**Models**
7. **A semi-synthetic release, R3 (B2, B3; F9).**
   - After ADIC data arrive, fit a conditional generator to ADIC holdings and outcomes, and define the truth as the fitted mechanisms.
   - Use it to test estimator rankings on ADIC-like data.
   - Keep the structural book for counterfactual SELL / HOLD / REFINANCE / LEVER runs.
8. **A generator ensemble with a calibrated spread (B18, B17; F13).**
   - Replace E1's grid search with simulation-based inference over the generator's parameters, fitted to the BGK, CA and MSCI targets.
   - Draw worlds from that posterior. This gives the misspecification ensemble a principled spread.
9. **A small-data market generator (B21; F7, F27)** as a realism challenger for public sleeves and overlay drivers.

**Parameters and calibration targets**
10. **Timing targets (B24; F18).** Add contribution, breakeven and distribution timing by strategy and vintage (Preqin, 1982–2025) to V5 and V6. Benchmark the regime layer against the latent-factor Takahashi–Alexander model.
11. **The anchoring mapping (#9).** Re-map Campbell–Sharpe's ≈ 0.3 to w_a or ρ_f, since the anchor is the latest actual (VL R8 agrees). Keep w_u as an [I] default backed by underwriting evidence (GGKS).

**Constraints: release gates**
12. **V16 (SBC):**
    - cite B10 for the ECDF bands;
    - make the joint log-likelihood a mandatory test quantity (B9);
    - add a classifier-based joint test (B12);
    - once ADIC data exist, add posterior SBC (B11) and L-C2ST at ADIC's own observation (B16).
13. **V17 (coverage):**
    - add tests at fixed parameter values at the stress corners (B15);
    - add a one-sided overconfidence test, and require ensembles for neural estimators (B14).
14. **A new V21, OSSE-style innovation match (B5).** Once ADIC data exist, the fusion engine's innovations must have the same distribution on synthetic and real data, within tolerance.
15. **V15 (realism):** add query-centric fidelity on IC roll-ups (B19), and logical-consistency metrics for accounting identities (F3).
16. **A recalibration fallback (B13).** When V16 or V17 fails, widen intervals by SBC and badge the outputs.
17. **Privacy (§8 and rule L8):**
    - MIA-based audits for any generator fitted to ADIC data (B20; F1);
    - canary-based audits for synthetic memo text generated by LLMs (F2).

**Objectives and evaluation protocol**
18. **ADEMP cards (B6)** for every experiment, with Monte Carlo standard errors on coverage, CRPS and regret.
19. **Preregistration (B7).** Freeze and hash the generator variants, estimands and pass criteria before scoring, and use an independent scorer.
20. **An estimator-selection policy (B1–B3).**
    - G9 decides correctness and robustness.
    - Among estimators that pass, choose using held-out ADIC outcomes (V18 time-travel tests on real data) and robustness across several estimators.
    - Report ranking stability by group.
21. **A skill haircut (B4).** Report the ratio of synthetic to real skill once ADIC data exist.

**Agent and IC design**
22. **Calibration as the agents' verifier (B25).**
    - Any agent-authored probabilistic program must pass posterior predictive checks, SBC and sampler diagnostics on SYN-ADIC-177 before use. Unit tests are not enough.
    - Amortized inference (F11) can make per-change SBC cheap enough to run in CI. B14's warning about overconfidence still applies.
23. **Graded agent tasks (F10).** An LLM model-discovery agent was evaluated both in backtests and in a market simulator with "synthetic but causally plausible" paths and news. That supports the dossier's graded tasks (§5 item 6). Deflate scores when agents try many policies (F22).
24. **IC slides.** Show estimator-ranking stability across generator variants and the synthetic-to-real skill haircut, under the "SYNTHETIC – NOT ADIC DATA" footer (rule L4).

### 4.2 Evidence that supports the dossier
- Generators fail to maintain logical consistency and dependencies (F3). That supports keeping accounting identities structural (V1).
- CTGAN underperforms in low-sample settings (F4). That supports §2.6's small-n caution.
- A carefully built observation layer can pass validation: Errico et al.'s OSSE was "validated remarkably well" (B5).
- PE cash-flow simulation where the true values are known has precedent:
  - Li & Riddiough (F19) find that a covariate-regression ML method gives the least biased and least noisy estimates of benchmarked performance;
  - Achleitner et al. (F20) simulate fund-of-funds investments from transaction data.

### 4.3 Further records

| Code | Record | Metadata | Finding (from the abstract unless stated) | Use for ADIC [inference] |
|---|---|---|---|---|
| F1 | [Synthetic Data -- Anonymisation Groundhog Day](http://arxiv.org/abs/2011.07018v6) (K17) | Stadler, Oprisanu, Troncoso · 2020 (v6 2022) · arXiv · cites n/a | Synthetic data "either does not prevent inference attacks or does not retain data utility"; the privacy–utility trade-off is "hard to predict". | Make no "synthetic means shareable" assumption for generators fitted to ADIC data. |
| F2 | [The Canary's Echo: Auditing Privacy Risks of LLM-Generated Synthetic Text](http://arxiv.org/abs/2502.14921v2) (T08) | Meeus, Wutschitz, Zanella-Béguelin, Tople, Shokri · 2025 · ICML 2025, PMLR 267:43557–43580 · cites n/a | MIAs show that synthetic text generated by an LLM leaks information about the data it was fine-tuned on; canaries with an in-distribution prefix improve audits. | Audit any synthetic IC-memo corpus generated by models tuned on ADIC memos. |
| F3 | [Evaluating Inter-Column Logical Relationships in Synthetic Tabular Data Generation](http://arxiv.org/abs/2502.04055v2) (T04) | Long, Xu, Brintrup · 2025 (v2 2026) · arXiv | Existing generators "often fail to rigorously maintain logical consistency" and dependencies, both temporal and mathematical. | Supports structural identities; gives V1 metrics for when challengers are used. |
| F4 | [MargCTGAN: A "Marginally'' Better CTGAN for the Low Sample Regime](http://arxiv.org/abs/2307.07997v1) (T04) | Afonja, Chen, Fritz · 2023 · ICML 2023 workshop (per comment) | CTGAN "underperforms in low sample settings", and statistical measures deteriorate quickly. | Supports the small-n caution in §2.6. |
| F5 | [A Comprehensive Survey of Synthetic Tabular Data Generation](http://arxiv.org/abs/2504.16506v3) (T04) | Shi, Wang, Du, Shen, Chang, Wang · 2025 · arXiv | Survey of traditional, diffusion and LLM-based methods, evaluation and privacy. | A current survey for the realism-challenger shortlist. |
| F6 | [TabSynDex: A Universal Metric for Robust Evaluation of Synthetic Tabular Data](http://arxiv.org/abs/2207.05295v2) (T04) | Chundawat, Tarun, Mandal, Lahoti, Narang · 2022 (v2 2024) · *IEEE Trans. AI* (per comment) | A single bounded score built from component similarity scores. | An optional summary metric; not a substitute for B19. |
| F7 | [Systematic comparison of deep generative models applied to multivariate financial time series](http://arxiv.org/abs/2412.06417v1) (T11) | Caulfield, Gleeson · 2024 · arXiv | Compares deep generative models with parametric models on increasingly complex synthetic data, then shows a benefit from the best of them in an implied-volatility trading task. | Evidence for deep generative challengers in the public sleeves. |
| F8 | [High-Quality Synthetic Financial Time-Series using a GAN-Diffusion Framework](http://arxiv.org/abs/2605.27113v1) (T11) | Masi, Coletta, Bartolini · 2026 · arXiv | Reproducing all stylized facts "remains an open challenge"; a GAN critic guides diffusion to enforce correlation structures. | A realism challenger for correlated equity paths. |
| F9 | [A Doubly Stochastic Simulator with Applications in Arrivals Modeling and Simulation](http://arxiv.org/abs/2012.13940v3) (T06) | Zheng, Zheng, Zhu · 2020 (v3 2023) · arXiv | Combines a classical Monte Carlo simulator's interpretable "physics" with a WGAN for complex dependence; proves consistency and convergence rates. | A template for hybrid structural-plus-learned generators (R3). |
| F10 | [To Trade or Not to Trade: An Agentic Approach to Estimating Market Risk Improves Trading Decisions](http://arxiv.org/abs/2507.08584v1) (T11) | Emmanoulopoulos, Olby, Lyon, Stillman · 2025 · arXiv | LLM agents discover stochastic differential equations; evaluated by backtests and by a market simulator with "synthetic but causally plausible price paths and news events". | Precedent for grading agents in a simulator. |
| F11 | [BayesFlow: Amortized Bayesian Workflows With Neural Networks](http://arxiv.org/abs/2306.16015v2) (T12) | Radev, Schmitt, Schumacher, Elsemüller, Pratz, Schälte, Köthe, Bürkner · 2023 · arXiv | After training, the networks perform inference "almost instantaneously". | Makes thousands of SBC fits cheap; pair it with B14's caution. |
| F12 | [A Bayesian workflow for securitizing casualty insurance risk](http://arxiv.org/abs/2407.14666v3) (T02) | Haines, Goold, Shoun · 2024 (v3 2025) · arXiv | The workflow uses prior predictive simulations and SBC "to aid model specification" when forecasting loss ratios. | A finance-adjacent precedent for SBC in production model governance. |
| F13 | [The frontier of simulation-based inference](https://doi.org/10.1073/pnas.1912789117) (K14) | Cranmer, Brehmer, Louppe · 2020 · *PNAS* 117(48):30055–30062 · CR 1012 | Review: simulators give high-fidelity models but are "poorly suited for inference"; simulation-based inference addresses the resulting inverse problems. | Calibrate G9's parameters to published targets by simulation-based inference (item 8). |
| F14 | [Bayesian Workflow](http://arxiv.org/abs/2011.01808v1) (K08) | Gelman, Vehtari, Simpson, Margossian, Carpenter, Yao, Kennedy, Gabry et al. · 2020 · arXiv | The workflow covers iterative model building, model checking, validation, troubleshooting and model comparison, across many fitted models. | A basis for the lab's model-development SOP. |
| F15 | [Bayesian Workflow (book)](https://doi.org/10.1201/9781003044024) (K18) | Gelman, Vehtari, McElreath, Simpson, Margossian, Yao, Kennedy, Gabry et al. · 2026 · Chapman & Hall/CRC · CR 8 | No abstract. Chapters include "Simulation-based calibration checking" (pp. 249–254, [DOI](https://doi.org/10.1201/9781003044024-17)) and "Simulation-based calibration checking in model development workflow" (pp. 471–482, [DOI](https://doi.org/10.1201/9781003044024-35)). | The current canonical SBC reference. |
| F16 | [Future Observing System Simulation Experiments](https://doi.org/10.1175/bams-d-15-00200.1) (K03) | Hoffman, Atlas · 2016 · *BAMS* 97(9):1601–1616 · CR 116 | OSSE systems "must evolve in parallel" with operational systems; coupled systems need coupled nature runs and coupled observation simulators. | G9 must co-evolve with the estimators it tests, through versioned releases. |
| F17 | [SynthETIC: An individual insurance claim simulator with feature control](https://doi.org/10.1016/j.insmatheco.2021.06.004) (K05) | Avanzi, Taylor, Wang, Wong · 2021 · *IME* 100:296–308 · CR 12 | No abstract retrieved. | A second actuarial simulator for §5 item 3. |
| F18 | [A Latent Factor Cash Flow Model for Alternative Investment Funds](https://consensus.app/papers/details/bb74f63a8fc15983a1e7753d4057d4f0/?utm_source=claude_desktop) [CS-saved: 10] | Wenbo Cao et al. · 2025 · *FAJ* · 1 cit. · DOI 10.1080/0015198x.2025.2489923 | Per stream 10's record: extends Takahashi–Alexander with systematic factors and fund-specific randomness, for stress tests and commitment design. | A benchmark for the PE engine's regime layer. |
| F19 | [Benchmarking Private Equity Performance When Fund-Level Cash Flows are Missing](https://doi.org/10.2139/ssrn.4943452) (T03) | Li, Riddiough · 2024 · SSRN · CR 0 | Of three simulation methods, the covariate-regression ML method gives the least biased and least noisy estimates. | Imputation for ADIC funds with missing histories; testable on G9. |
| F20 | [Risk of Private Equity Fund-of-Fund Investments: A Detailed Cash Flow-Based Approach](https://doi.org/10.2139/ssrn.1342499) (T03) | Achleitner, Braun, Schaller, Tappeiner · 2009 · SSRN · CR 0 | Simulates fund-of-funds investments from proprietary transaction data; strategy parameters strongly affect risk and return. | Historical resampling as an alternative engine for co-investment portfolios. |
| F21 | [Modeling the Cash Flow Dynamics of Private Equity Funds: Theory and Empirical Evidence](https://doi.org/10.3905/jai.2010.13.1.041) (K06) | Buchner, Kaserer, Wagner · 2010 · *JAI* 13(1):41–54 · CR 9 | No abstract retrieved. | A stochastic PE cash-flow model to cite beside Takahashi–Alexander. |
| F22 | [The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality](https://consensus.app/papers/details/378afd063fd15487a4fcb21af0850767/?utm_source=claude_desktop) [CS-saved: 09, 12] | Bailey & López de Prado · 2014 · *JPM* 40(5) · 184 cit. · DOI 10.3905/jpm.2014.40.5.094 | Per stream 12's record: corrects for selection bias and non-normality. | Deflate metrics when agents try many policies on synthetic worlds. |
| F23 | [Learned Causal Method Prediction](http://arxiv.org/abs/2311.03989v2) (T07) | Gupta, Zhang, Hilmkil · 2023 · arXiv | Trains a predictor of the best method on synthetic causal datasets; it generalizes to semi-synthetic and real benchmarks. | An alternative to one fixed estimator: learn which estimator suits which group. |
| F24 | [DoTime: A Synthetic Benchmark Generator for Interventional and Counterfactual Time Series](http://arxiv.org/abs/2607.27263v1) (T07) | Thumm, Anthony, Chen · 2026 · arXiv | Temporal structural causal models with interventions, regime switching and shared-noise counterfactuals, all with exact ground truth. | Its shared-noise counterfactuals mirror G9's common random numbers across actions. |
| F25 | [Synthetic Data -- what, why and how?](http://arxiv.org/abs/2205.03257v1) (K16) | Jordon, Szpruch, Houssiau, Bottarelli, Cherubin, Maple, Cohen, Weller · 2022 · arXiv (commissioned by the Royal Society) | An explainer on synthetic data, focused on privacy. | Governance background for rules L1–L8. |
| F26 | [Generating synthetic data in finance](https://doi.org/10.1145/3383455.3422554) (K11) | Assefa, Dervovic, Mahfouz, Tillman, Reddy, Veloso · 2020 · ICAIF '20, pp. 1–8 · CR 176 | No abstract retrieved. | A finance precedent alongside Potluru et al. |
| F27 | [Machine Learning Techniques for Synthetic Data Generation in Energy and Financial Markets](https://doi.org/10.2139/ssrn.6457798) (T01) | Castello, Corazza · 2026 · SSRN · CR 0 | Compares families of deep generative models on theoretical distributions and on market data, under varying data availability; they reproduce "heavy tails, asymmetry, and multimodality". | A partial counterweight to §2.6's thin-tails claim, for liquid markets only. |

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier recommendation | Challenging evidence | Strength and caveats | Suggested response [inference] |
|---|---|---|---|---|
| 1 | §1 item 2 and §2.6: deep generators have "no interpretable θ", "cannot emit counterfactuals or truth", and "tails are thin with small n". Their role is limited to realism challenger. | **RealCause (B2):** generators fitted to real data can yield ground truth and be realistic. **Athey et al. (B3):** WGAN-designed simulations mimic real data and limit researcher freedom. **Bühler et al. (B21):** a generator that is reliable with small data. **Castello & Corazza (F27):** deep generators reproduce heavy tails and asymmetry. | Strong against the "cannot carry truth" wording. It does not overturn the structural core while ADIC has no data. The evidence comes from causal inference, econometrics and liquid markets, not PE. | Keep the structural generator of record. Add the semi-synthetic release R3 (§4.1 item 7). Reword the §2.6 rows on truth columns and counterfactuals to "possible by construction in semi-synthetic designs". |
| 2 | §3.6 items 2–4 and gates V17–V19: score estimators against the truth on the synthetic book, implicitly to choose among them. | **Advani et al. (B1):** data-calibrated Monte Carlo designs are worse than random at choosing minimum-bias estimators; a simple bootstrap is as good or better. **RealCause (B2):** the best estimators on synthetic data are unlikely to be the best on real data. **Athey et al. (B3):** rankings vary by setting. | Strong. The evidence concerns treatment-effect estimators, but the mechanism (simulated process ≠ true process) applies to ADIC [inference]. | Use G9 for correctness, bias recovery and robustness envelopes. Choose among estimators that pass using held-out ADIC outcomes, and report several estimators side by side. |
| 3 | §2.2: the OSSE analogy as support for the world / truth / observation design | **Privé et al. (B4):** a validated OSSE gave "slightly higher" skill than real data and smaller observation impacts, possibly from insufficient model error. **Errico et al. (B5):** validation needed correlated observation errors. | It supports the analogy but documents the analogy's known failure mode. | Inject model error and correlated observation errors. Report a skill haircut and add an innovation-match gate (V21). |
| 4 | V16 and V17 as release gates: SBC rank χ² p > 0.01, ECDF bands, coverage within ±5pp | **Alokda et al. (B15):** posteriors can pass coverage tests yet be miscalibrated at fixed θ. **Yao & Domke (B12):** rank SBC has low power and multiple-testing problems. **Hermans et al. (B14):** simulation-based posteriors are often overconfident. Modrák et al. (B9, already cited) shows that a posterior equal to the prior passes naive SBC. | Moderate to strong. B15 is a cosmology result. | Add data-dependent test quantities, a classifier-based joint test and coverage at fixed θ at the stress corners. After ADIC data arrive, add posterior SBC and L-C2ST. |
| 5 | V15: C2ST AUC ≤ 0.60 as the joint-realism gate | **TabQueryBench (B19):** statistically realistic synthetic data can still fail analytical queries, especially high-cardinality and tail queries. | Moderate; the benchmark uses public tabular data, not finance. | Add query-centric fidelity gates that mirror IC queries (group DPI, unfunded by group, liquidity ladder). |
| 6 | §8: "apply memorization audits (authenticity metrics) before any external sharing" | **DCR Delusion (B20):** distance-based privacy proxies fail; MIAs are needed. **Stadler et al. (F1):** synthetic data does not reliably beat anonymisation. **Meeus et al. (F2):** synthetic text from LLMs leaks training data. | Strong for distance-based proxies. Authenticity is not tested in the abstracts [inference: it is a similar similarity-based copying score]. | Use MIA-based audits. Share no synthetic data fitted to ADIC data externally without a formal privacy assessment. Use canary audits for synthetic memo text. |
| 7 | §3.6 item 5 and §8: "freezing estimator code before scoring" as the Goodhart mitigation | **Pawel et al. (B7):** questionable research practices in simulation studies can make any method look superior; preregistration is recommended. | Strong (methodological). This refines the dossier rather than contradicting it. | Also preregister and hash the generator variants, estimands and pass criteria, and use an independent scorer. |
| 8 | O4: anchoring weight w_u calibrated to Campbell–Sharpe's ≈ 0.3 (§2.5, §6.4) | The cited paper's own abstract: the anchor is "previous months' releases", the latest realized values. | This is a use issue with one of the dossier's own citations; VL R8 makes the same point. | Map the ≈ 0.3 to w_a or ρ_f. Keep w_u as an [I] parameter. |

---

## 6. Verbatim usage message

The last (and only) message Consensus returned, on all three attempts:

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Search log and rerun plan

**Consensus `search`.** Three attempts on the query "Validating Bayesian inference algorithms with simulation-based calibration", about 30 seconds apart. All three returned the quota message in §6. I used no filters and no thread tools.

**Probes.**
- OpenAlex: HTTP 429 on the first request.
- Semantic Scholar: HTTP 429 on the first request.
- DBLP: HTTP 202 with an anti-bot challenge page. Six venue look-ups failed and were not retried. Official proceedings pages [PG] confirmed five of those venues; CTGAN's rests on its arXiv comment.

**Topical searches (14; plain queries, no filters).** Notable hits follow each query.

| # | Engine and query | Notable hits |
|---|---|---|
| T01 | Crossref: "synthetic financial data generation" (seed) | Mostly low-impact 2020–2026 items (GAN frameworks and privacy frameworks in minor outlets). Castello & Corazza (F27) is the only one kept. |
| T02 | arXiv: abs:"simulation-based calibration" AND abs:Bayesian (seed) | Talts (B8); posterior SBC (B11); discriminative calibration (B12); approximate posterior recalibration (B13); Haines et al. (F12) |
| T03 | Crossref: "private equity fund cash flow simulation stochastic model" (seed, refined) | Achleitner et al. (F20); Li & Riddiough (F19); Robinson & Sensoy (already cited) |
| T04 | arXiv: abs:"synthetic tabular data" AND abs:evaluation (seed) | TabQueryBench (B19); Long et al. (F3); MargCTGAN (F4); Shi et al. survey (F5); TabSynDex (F6) |
| T05 | Crossref: "Monte Carlo simulation studies estimator selection empirical Monte Carlo design mostly harmless" | Advani et al. (B1), with IFS and SSRN working-paper versions |
| T06 | arXiv: Monte Carlo + generative adversarial + estimators + simulations | Athey et al. (B3); doubly stochastic simulator (F9) |
| T07 | arXiv: causal inference + benchmark + ground truth + generative | RealCause (B2); CAMP (F23); DoTime (F24) |
| T08 | arXiv: "synthetic data" + "membership inference" | DCR Delusion (B20); Canary's Echo (F2) |
| T09 | Crossref: OSSE, nature run, validation, data assimilation | Only applied OSSEs (e.g., a 2022 *J. Hydrometeorology* nature run; a 2008 *MWR* hybrid ETKF–3DVAR OSSE). The primary validation papers came from K02 and K03. |
| T10 | Crossref: individual claims simulation machine, synthetic claims, reserving | Reserving textbooks only. The primary simulators came from K04 and K05. |
| T11 | arXiv: financial time series + generative + evaluation + synthetic | Caulfield & Gleeson (F7); Masi et al. (F8); ProteuS (B22); Emmanoulopoulos et al. (F10) |
| T12 | arXiv: "Bayesian workflow" AND simulation | BayesFlow (F11); "Calibration, Not Compilation" (B25); Haines et al. (F12) |
| T13 | arXiv: "simulation-based inference" + coverage + posterior | "Coverage is not enough" (B15); L-C2ST (B16); OASIS (B17); conformal and robust variants of neural posterior estimation (not annotated) |
| T14 | arXiv: "synthetic data" + downstream + "deep generative" + uncertainty | van Breugel et al. (B18) |

**Known-item look-ups (19).** These papers were identified from domain knowledge, then confirmed by Crossref or arXiv:

| Code | Look-up |
|---|---|
| K01 | Athey et al., journal version |
| K02 | Errico et al. and Privé et al. (OSSE validation) |
| K03 | Hoffman & Atlas |
| K04 | Gabrielli & Wüthrich |
| K05 | Avanzi et al. |
| K06 | Buchner, Kaserer & Wagner |
| K07 | Hermans et al. |
| K08 | Gelman et al. 2020 |
| K09 | Säilynoja et al. 2022 |
| K10 | Gelman 2017 correction |
| K11 | Assefa et al. |
| K12 | Morris et al. |
| K13 | Pawel et al. |
| K14 | Cranmer et al. |
| K15 | Bühler et al. |
| K16 | Jordon et al. |
| K17 | Stadler et al. |
| K18 | *Bayesian Workflow* (2026 book) |
| K19 | Schad, Betancourt & Vasishth (2021, *Psychological Methods* 26(1):103–126, DOI 10.1037/met0000275). No abstract was retrieved, so it is not annotated. |

**Citation look-ups.**
- 26 jobs: one arXiv batch of 9 IDs, 19 Crossref queries and 6 DBLP queries. All 6 DBLP queries failed.
- Plus 5 official-page fetches [PG].
- Plus 39 Crossref `URL`-field confirmations, which cover every DOI linked in this file.

**Totals.**
- 67 search calls attempted: 3 Consensus, 14 topical, 19 known-item, 26 citation look-ups and 5 [PG] fetches.
- 58 of them completed. The 3 Consensus attempts were refused by the quota, and the 6 DBLP calls were blocked.

**Limits**
- Crossref ranks results by keyword, and arXiv search is a Boolean match on title and abstract. Neither matches Consensus's semantic ranking.
- Recall is weaker for peer-reviewed social-science work, because Elsevier and NBER deposit few abstracts in Crossref.
- arXiv-only papers carry no citation counts here.
- The known-item look-ups reflect my domain knowledge and are flagged with K-tags.
- Findings for B24, F18 and F22 come from sibling summaries of saved Consensus records, not from abstracts I retrieved.

**Rerun plan (after 1 November 2026)**
1. Re-run T01–T14 in Consensus, as plain queries with no filters.
2. Retrieve Consensus records for the 16 checked citations that have none: rows 1–3, 6, 9, 10 and 16–25.
3. Add citation counts for the arXiv-only items: B2, B8, B11–B22 and B25.
4. Check the 15 references not checked here. Start with Aas et al. (2009), López de Prado (2018) and Borisov et al. (2023), which no stream has checked.
