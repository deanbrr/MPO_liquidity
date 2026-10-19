# Topic 07 literature review: fusing underwritten, current-actual and forecast returns

**Dossier reviewed:** `research/dossiers/07_return_fusion.md` (as of 18 Oct 2026, 581 lines)
**Prepared:** 18 Oct 2026
**Companion:** `research/verification/07_return_fusion.verify.md` (fact-check of the same dossier)
**Tools:** 33 Consensus searches, run one at a time with no filters: 19 citation checks and 14 topical backfill searches. Two WebSearch calls confirmed two works that Consensus could not return. No WebFetch was used.

**Conventions**
- Every paper link is the Consensus URL exactly as returned.
- In the bibliography, authors are listed as Consensus shows them, usually the first author plus "et al.". In the integrity table, the dossier's own author lists are kept.
- Citation counts are Consensus counts on 18 Oct 2026. Years are as Consensus shows them. Where Consensus shows an online-first, working-paper or preprint year, the entry says so.
- "[inference]" marks our own reasoning. Everything else restates a search result or an abstract.
- Status labels in §2:
  - **found**: Consensus has the work and the dossier's metadata match.
  - **mismatched**: the work exists, but the source of the cited claim differs from the citation in authors, year, title, venue or version.
  - **not found**: Consensus returned no record; one WebSearch was then tried.
- **User context (18 Oct 2026).**
  - The Secondaries group is a hybrid of direct and fund investments. Evidence on fund-level NAVs (the PE group's funds and the Secondaries group's fund commitments) is therefore read separately from deal-level evidence (Co-investment and the Secondaries group's direct deals).
  - Treasury is owned by Corporate Finance, which runs the funding and liability side. The Forward Belief Engine's (FBE) posterior quantiles feed Corporate Finance's portfolio-level LEVER and liquidity decisions. The Treasurer seat's own forecasts (liquidity, distributions) should be scored like any group's [inference].

---

## 1. Summary

### Citation integrity
The dossier cites about 60 academic works: 51 numbered references plus 9 background works in reference 61. We checked 42, including every work that drives an equation, a default parameter or a headline claim.

| Outcome | Count | Detail |
|---|---|---|
| Found, metadata match | 37 | Five are indexed only as working-paper, SSRN or arXiv records (Timmermann; Andonov & Rauh; Harris et al.; Ben-David et al.; Meucci). Four show an online-first year (Wang et al. 2022; Yao et al. 2017; Diebold & Shin 2018; Jenkinson et al. *TAR* 2019). Four Consensus records carry garbled or outdated venue labels that the DOI resolves (Bornhuetter & Ferguson; Lovallo et al.; Diebold & Pauly; Bates & Granger). |
| Mismatched | 3 | (1) **Cooke's "26 of 33 studies in-sample"** (§3). The primary source is Colson & Cooke (2017, *RESS*). There, 26 of 33 is the **out-of-sample** validity-index result; **in-sample, performance weights beat equal weights in 32 of 33**, and out-of-sample statistical accuracy is *lower* than equal weighting. (2) **Brown, Ghysels & Gredil**: the betas 1.05/1.20 and the 38% VC total risk come from an earlier working paper, not the cited *RFS* version. The indexed abstract gives β ≈ 1.0 (buyout) and 1.4 (VC), with total risk of 33% and 40%. (3) **Nadauld et al. (2019)**: the published *JFE* abstract gives the sellers' PME as **0.976**; the dossier's 0.974 is the working-paper figure. |
| Not found in Consensus | 2 | Mincer & Zarnowitz (1969) and Nordhaus (1987). WebSearch confirms both with the dossier's metadata. A *JBES* comment that Consensus does index also lists both in its references. |

- **No citation was fabricated.**
- **Two items the verification log marked unverifiable are now confirmed** by indexed abstracts:
  - Jenkinson, Sousa & Stucke (2013): 761 CalPERS fund investments, a ~35% understatement, the Q4 jump, inflation during fundraising, and interim IRRs that predict ultimate returns poorly.
  - Barber & Yasuda (2017): low-reputation GPs with low realization rates show performance peaks, then erosion after fundraising.
- **Link hygiene.**
  - Replace the Wikipedia links (Bühlmann; the Cooke statistic) and the rdrr.io link (Bates & Granger) with the journal DOIs in §2.
  - Flyvbjerg et al. (2005) carries a Notice of Redundant Publication; the *JAPA* article itself stands.
- **Twelve † ("from memory") flags can be removed.** Consensus confirms these works and their metadata: Arkes & Blumer; Staw; Glahn & Lowry; Gneiting & Raftery; Gneiting, Balabdaoui & Raftery; Gneiting et al. (2005); Baron et al.; Diebold & Pauly; Smith & Wallis; Diebold & Shin (*IJF*); Gupta & Van Nieuwerburgh (*JF* 2021); Blanc & Setzer (authors).

### Backfill: what the dossier misses
We ran 14 topical searches. The most important gaps:

1. **Pooling predictive distributions makes them miscalibrated.** Any non-trivial weighted average of distinct, calibrated forecasts is uncalibrated and too wide (Ranjan & Gneiting 2010). Convex combinations are almost always Mincer–Zarnowitz-inefficient (Pincheira-Brown et al. 2023).
   - The dossier's stacking step, IC-view pooling and entropy-pooled scenario sets are all linear pools, but it never recalibrates after pooling [inference].
2. **Dynamic and hierarchical fusion.**
   - Bayesian predictive synthesis adapts to time-varying biases, miscalibration and dependence among forecasters (McAlinn & West 2019).
   - Hierarchical stacking lets weights vary by input with partial pooling (Yao et al. 2022). In ADIC terms, by group × strategy × age [inference].
3. **"Machine benchmark" debiasing from finance.** Characteristic forecasts predict analysts' errors (So 2013). Conditional bias, measured as the forecast minus an ML benchmark, grows with horizon (van Binsbergen et al. 2023). This is the finance version of the dossier's MOS step, and it has published evidence behind it.
4. **How forecasters err.**
   - Individuals overreact while consensus forecasts underreact (Bordalo et al. 2020).
   - Forecasters are anchored to priors and overreact to private information (Adam et al. 2025).
   - Miscalibration is a persistent personal trait that does not improve with feedback (Boutros et al. 2020).
   - Optimism rises with sentiment for hard-to-value firms (Hribar & McInnis 2012). This answers the dossier's open question 4 (§9).
5. **Elicitation and aggregation for the IC.**
   - Separate shared from private information (Palley & Soll 2019).
   - Collect forecasts blind (Da & Huang 2020).
   - Aggregate distributions, not point forecasts (Cooke 2026; Cooke et al. 2021).
   - Deliberate in small groups, then aggregate (Navajas et al. 2018).
6. **Incentives and scoring.**
   - Competition makes forecasters exaggerate (Lichtendahl & Winkler 2007; Witkowski et al. 2023).
   - CRPS averages over-weight high-uncertainty cases (Bolin & Wallin 2023).
   - PITs of multi-step forecasts are serially correlated (Knüppel 2015).
   - Proxy scores allow scoring before outcomes resolve (Witkowski et al. 2017).
7. **The credibility toolkit the FBE needs.**
   - Hierarchical, multidimensional and evolutionary credibility (Bühlmann & Gisler 2005).
   - Credibility that combines internal data, expert opinion and industry data (Bühlmann, Shevchenko & Wüthrich 2007).
   - Parameter-free Benktander-type methods (Neuhaus 2025), which avoid the unsourced t = 0.5 (verification issue R4).
8. **PE marks: deal level versus fund level, and the valuation regime.**
   - There is no deal-level inflation around fundraising, only a cohort effect (Hüther, *JFQA*).
   - After ASC 820, NAVs predict distributions more accurately (Easton et al. 2020).
   - Marks respond asymmetrically to market moves during the reporting lag (Czasonis et al., via Meng et al. 2019).
9. **The prior's anchor.** Several equity premia vary more across institutions than over time, and the differences persist (Dahlquist et al. 2026). A prior anchored on one house CMA (JPM) understates uncertainty in the prior mean [inference].
10. **De-escalation governance.**
    - Pre-set review triggers and process-based evaluation reduce escalation (Simonson & Staw 1992).
    - Specific normative instructions work where warnings do not (Ohlert & Weißenberger 2020).
    - Handing a decision to a new person fails if that person is psychologically connected to the first decision-maker (Gunia et al. 2009).

**Gap.** Our searches found no academic study of PE deal-level underwriting projections against realized outcomes. Lovallo et al. (2012) remains the only PE-specific test of the outside view we found. ADIC's 18-year memo corpus would be close to unique evidence [inference].

### Challenges to the dossier (detail in §5)
- **Correlated GLS weights (ρ_fu = 0.5, ρ_fa = 0.3).** Smith & Wallis (2009) recommend ignoring error covariances when *estimating weights*; Timmermann (2005) agrees.
- **Beating simple averages.**
  - The equal-weight average is hard to beat once data snooping is accounted for (Genre et al. 2013).
  - "Discard most forecasts, average the rest" (Diebold & Shin 2019; Elliott et al. 2026).
- **Fusing point signals.** Point-forecast errors are fat-tailed and do not aggregate well (Cooke 2026).
- **"Proper scoring rules make honest forecasts optimal" (§8).** Not when groups compete on rank (Lichtendahl & Winkler 2007; Witkowski et al. 2023).
- **Performance weights "won in-sample".** Corrected by Colson & Cooke (2017); see also Lin & Cheng (2009) and Hemming et al. (2021).
- **i.i.d. PIT and coverage tests for multi-year forecasts.** Knüppel (2015).
- **CRPS skill pooled across assets.** Bolin & Wallin (2023); Du (2021).
- **Overreaction default β_f ≥ 1.** Group consensus forecasts may underreact (Bordalo et al. 2020; Adam et al. 2025). Identification caveat: Yee (2026).
- **F5 fundraising haircut applied to deals.** Hüther; Ellis et al. (2011).
- **Static bias and "no improvement in 30 years".** Hoque et al. (2021; 2024); Välilä (2024).
- **Reference-class effectiveness.** Bärenbold (2023); Prater et al. (2017); Cantarelli et al. (2025).
- **Simple models versus analysts.** Commonly used linear earnings models do not work out of sample and are worse than analysts (van Binsbergen et al. 2023).

**Usage message:** none appeared in any Consensus result.

---

## 2. Citation-integrity table (42 checked)

| # | Dossier citation | Status | Corrected metadata / note | Consensus URL |
|---|---|---|---|---|
| 1 | Bates & Granger (1969), *Operational Research Quarterly* 20(4):451–468; cited via rdrr.io | found | Indexed as *Journal of the Operational Research Society* (the journal's later name), 1969, DOI 10.1057/jors.1969.103, 3645 cit. The abstract covers the two-forecast case, consistent with verification issue R12. **Replace the rdrr.io link with the DOI.** | https://consensus.app/papers/details/0235871925f15706bd35eb697c897289/?utm_source=claude_desktop |
| 2 | Claeskens, Magnus, Vasnev & Wang (2016), *IJF* 32(3):754–762 | found | DOI 10.1016/j.ijforecast.2015.12.005, 268 cit. The abstract matches the dossier's description. | https://consensus.app/papers/details/355eb70a27bf5d8083917adbbf4623fb/?utm_source=claude_desktop |
| 3 | Smith & Wallis (2009), *OBES* 71(3) (details†) | found; remove † | *Oxford Bulletin of Economics and Statistics*, DOI 10.1111/j.1468-0084.2008.00541.x, 373 cit. The abstract also "supports the popular recommendation to ignore forecast error covariances in estimating the weight" (see §5, challenge 1). | https://consensus.app/papers/details/f8bdb7ea82bb52c681576c06475bb34a/?utm_source=claude_desktop |
| 4 | Diebold & Pauly (1990), *IJF* 6(4):503–508† | found; remove † | DOI 10.1016/0169-2070(90)90028-a (the *IJF* prefix); Consensus shows "Unknown Journal". 168 cit. Bayesian shrinkage of weights toward equality; "a large amount of shrinkage was found to be optimal" for US GNP forecasts. | https://consensus.app/papers/details/786340ac75285de3b6a56586008c5ab7/?utm_source=claude_desktop |
| 5 | Diebold & Shin (2019), *IJF* 35(4) (journal details†) | found | *IJF*, online year 2018, DOI 10.1016/j.ijforecast.2018.09.006, 146 cit. **Add the DOI.** The abstract: "The vast majority of forecasters should be discarded, and the remainder should be averaged." The PIER working-paper record (2017) is also indexed. | https://consensus.app/papers/details/4cb0f6c792ad523094ee7a7fcdc2bb1d/?utm_source=claude_desktop |
| 6 | Wang, Hyndman, Li & Kang (2023), *IJF* 39(4):1518–1547 | found | Online year 2022, DOI 10.1016/j.ijforecast.2022.11.005, 295 cit. | https://consensus.app/papers/details/399206acf087541caad5cd5ac5a516d1/?utm_source=claude_desktop |
| 7 | Timmermann (2006), *Handbook of Economic Forecasting* Vol. 1, ch. 4 (pages†) | found (WP record only) | "Forecast Combinations", 2005, "Unknown Journal", 226 cit, no DOI. The Handbook chapter record was not returned, so the pages remain unverified. | https://consensus.app/papers/details/4fd1e95759945288b568eb0ffc5600f2/?utm_source=claude_desktop |
| 8 | Blanc & Setzer (2020), *Mgmt Sci* 66(12):5720–5737 (authors†) | found; remove † | Authors confirmed (Sebastian M. Blanc et al.). DOI 10.1287/mnsc.2019.3476, 16 cit. It is still an orphan reference, never cited in the body (verification log). | https://consensus.app/papers/details/9c2636a9e408557bb78a7ba67371d736/?utm_source=claude_desktop |
| 9 | Yao, Vehtari, Simpson & Gelman (2018), *Bayesian Analysis* 13(3), DOI 10.1214/17-BA1091 | found | Online year 2017; DOI matches; 446 cit. The abstract confirms that BMA is flawed in the M-open setting. | https://consensus.app/papers/details/346e109a0940557dbdc3bf8436393cfc/?utm_source=claude_desktop |
| 10 | Bühlmann (1967), *ASTIN Bulletin* 4(3):199–207; cited via Wikipedia | found | *ASTIN Bulletin*, 1967, DOI 10.1017/s0515036100008023, 441 cit. **Replace the Wikipedia link with the DOI.** A second record with the same title (DOI 10.1017/s0515036100008989, 33 cit, https://consensus.app/papers/details/40917c7c0e68585c96d0795be7d49cbc/?utm_source=claude_desktop) appears to be Bühlmann's companion paper; Consensus dates it 1967 too. | https://consensus.app/papers/details/cf8d4938d64d54fa9d6f6fdffe9f6f85/?utm_source=claude_desktop |
| 11 | Bornhuetter & Ferguson (1972), *PCAS* 59:181–195 | found (garbled record) | The record is a scan with garbled metadata: year 1999, no venue, 0 cit. A Consensus-indexed citing paper (Han & Gau 2008, *IME*, https://consensus.app/papers/details/e3ae7d54d6c4562e8195b0aa5278b291/?utm_source=claude_desktop) gives "Proc. Casualty Actuarial Soc. 59, 181–195" (1972), matching the dossier. | https://consensus.app/papers/details/fa4ff1a0d5b1595c89f49ef15b2b30bb/?utm_source=claude_desktop |
| 12 | Mack (2000), *ASTIN Bulletin* 30(2):333–347 | found | DOI 10.2143/ast.30.2.504639, 48 cit. The abstract confirms that Benktander almost always has a smaller MSE and is "almost as precise as an exact Bayesian procedure". Usage caveat on t = 0.5: see verification issue R4. | https://consensus.app/papers/details/6b4380749f325dc5adedb777bc68eeba/?utm_source=claude_desktop |
| 13 | Gneiting & Raftery (2007), *JASA* 102(477):359–378† | found; remove † | DOI 10.1198/016214506000001437, 7352 cit. The abstract also covers the interval score and quantile scoring. | https://consensus.app/papers/details/cb608bdcfc4b52baa11789d9cfee6d2c/?utm_source=claude_desktop |
| 14 | Gneiting, Balabdaoui & Raftery (2007), *JRSS-B* 69(2):243–268† | found; remove † | DOI 10.1111/j.1467-9868.2007.00587.x, 2009 cit. The "sharpness subject to calibration" paradigm is confirmed verbatim. | https://consensus.app/papers/details/b41a42fb6d295521bb46aba1b4c53e0b/?utm_source=claude_desktop |
| 15 | Gneiting, Raftery, Westveld & Goldman (2005), *MWR* 133(5):1098–1118† | found; remove † | DOI 10.1175/mwr2904.1, 1103 cit. EMOS corrects bias and underdispersion; the predictive mean is a bias-corrected weighted average of members. | https://consensus.app/papers/details/c9767832ef92574c8c3ff0dfca82b801/?utm_source=claude_desktop |
| 16 | Diebold, Gunther & Tay (1998), *IER* 39:863–883 | found | DOI 10.2307/2527342, 1517 cit. | https://consensus.app/papers/details/12b83128ea8057b486fdcdee3d8664d8/?utm_source=claude_desktop |
| 17 | Glahn & Lowry (1972), *J. Appl. Meteor.* 11(8):1203–1211† | found; remove † | DOI 10.1175/1520-0450(1972)011<1203:tuomos>2.0.co;2 (page 1203 confirmed), 1132 cit. Use this primary source for the MOS claims instead of Wikipedia. | https://consensus.app/papers/details/f333fe1649a05560a99debd7d48a103a/?utm_source=claude_desktop |
| 18 | Mincer & Zarnowitz (1969), "The evaluation of economic forecasts", NBER† | **not found in Consensus; exists (web-verified)** | No own record. WebSearch: NBER chapter, pp. 3–46 in J. Mincer (ed.), *Economic Forecasts and Expectations* (https://www.nber.org/chapters/c1214.pdf). The reference list of a Consensus-indexed *JBES* comment (Croushore 2012, https://consensus.app/papers/details/c89794c4240a551dbbc0ad1f5281ec16/?utm_source=claude_desktop) gives the same details. Add the pages. | none |
| 19 | Nordhaus (1987), *REStat* 69(4):667–674† | **not found in Consensus; exists (web-verified)** | No own record. WebSearch (EconPapers): *REStat* 69(4), 667–674, November 1987, with an earlier Cowles Foundation discussion paper. The Croushore (2012) reference list confirms it too. | none |
| 20 | Meucci (2008), "Fully flexible views: Theory and practice", *Risk* 21(10)†; SSRN 1213325 | found (arXiv record) | 2008, arXiv DOI 10.48550/arxiv.1012.2848, 92 cit. The *Risk* venue is not shown. | https://consensus.app/papers/details/9ed7d3116f4656ada56ea14eb7491b12/?utm_source=claude_desktop |
| 21 | Baron, Mellers, Tetlock, Stone & Ungar (2014), *Decision Analysis* 11(2)† | found; remove † | DOI 10.1287/deca.2014.0293, 124 cit. | https://consensus.app/papers/details/5489c24713215f528ab9f73a93ecf055/?utm_source=claude_desktop |
| 22 | Cooke (1991), *Experts in Uncertainty*, plus Wikipedia for "performance weights won in 26 of 33 studies in-sample" (§3) and "best combined score in 26" (§4.5) | **mismatched (source and description)** | Primary source: **Colson, A. & Cooke, R. (2017), "Cross validation for the classical model of structured expert judgment", *Reliability Engineering & System Safety*, DOI 10.1016/j.ress.2017.02.003**, 106 cit. Across 33 post-2006 studies, performance weighting beat equal weighting **in-sample in all but 1**. Out of sample it "incurs an out-of-sample penalty", with statistical accuracy *lower* than equal weighting. **26 of 33 is the result on an out-of-sample validity index** (training sets of 80% of the calibration variables; p = 0.001). §4.5 is roughly right; §3's "in-sample" is wrong. A 1991 book cannot source a statistic on 2006–2015 studies. | https://consensus.app/papers/details/dbe7edfbdd19501caa1d757e57fd4aad/?utm_source=claude_desktop |
| 23 | Korteweg & Sorensen (2017), *JFE* 124(3):535–562 | found | DOI 10.1016/j.jfineco.2017.03.006, 150 cit. The abstract confirms the 7–8 pp spread and "little investable persistence". | https://consensus.app/papers/details/a0bf5a58fd485ea895fabd5c39cb76ce/?utm_source=claude_desktop |
| 24 | Harris, Jenkinson, Kaplan & Stucke (2020), NBER WP 28109 (*JCF* 2023) | found (WP record) | 2020, DOI 10.3386/w28109, 109 cit. The abstract confirms little post-2000 buyout persistence except at the low end, and persistent VC. The *JCF* record was not returned; the verification log confirmed it. | https://consensus.app/papers/details/c9d05f78edee5236895cb0968f1c5e62/?utm_source=claude_desktop |
| 25 | Jenkinson, Sousa & Stucke (2013), SSRN 2229547 | found; **specifics now confirmed** | 2013, DOI 10.2139/ssrn.2229547, 88 cit. The abstract confirms all of the following, resolving verification row 5 ("U"): 761 CalPERS fund investments; NAVs understate subsequent distributions by about 35%; a Q4 audit jump; inflation during fundraising with gradual reversal; little predictive power of interim performance, especially IRR; PME improves predictability. | https://consensus.app/papers/details/e297da1e0d0658d8ae2ca7a7a7b6987c/?utm_source=claude_desktop |
| 26 | Barber & Yasuda (2017), *JFE* 124(1):172–194 | found; **mechanism now confirmed** | DOI 10.1016/j.jfineco.2017.01.001, 113 cit. The abstract confirms that "low reputation GPs with low realization rates experience performance peaks and erosions in performance after fundraising", resolving verification row 29 ("U"). | https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop |
| 27 | Brown, Gredil & Kaplan (2019), *JFE* 132(2):267–297 | found | *JFE*, 2019, NBER DOI 10.3386/w22493, 90 cit. A second record carries the SSRN DOI 10.2139/ssrn.2271690. | https://consensus.app/papers/details/3331159853ab59dea783df670c91ee0a/?utm_source=claude_desktop |
| 28 | Jenkinson, Landsman, Rountree & Soonawalla (2020), *TAR* 95(1):191–210 | found | Online year 2019, DOI 10.2308/accr-52486, 31 cit. The abstract confirms 384 VC and 195 buyout funds (1988–2016), little buyout bias and aggressive VC NAVs. | https://consensus.app/papers/details/44d91cea6b8b53b481621e6ed4e6ef9e/?utm_source=claude_desktop |
| 29 | Brown, Ghysels & Gredil (2023), *RFS* 36(3):945–986; figures β ≈ 1.05 (BO) / 1.20 (VC), total risk 33% / 38% | **mismatched (version of the figures)** | Only the SSRN record is indexed: 2020, DOI 10.2139/ssrn.3507873, 20 cit. Its abstract gives β "around 1.0 (1.4)" and total risk "33% (40%)", which the verification log says match the *RFS* abstract. The dossier's 1.05/1.20 and 38% come from an earlier working paper (the UNC page). **Use 1.0/1.4 and 33%/40%, or cite the earlier working paper explicitly.** | https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop |
| 30 | Nadauld, Sensoy, Vorkink & Weisbach (2019), *JFE*, DOI 10.1016/j.jfineco.2018.11.007; "buyers' PME 1.023 vs sellers' 0.974" | **mismatched (figure from WP)** | The published abstract gives **sellers' PME 0.976** (buyers 1.023; about 5 pp a year); 66 cit. 0.974 is the working-paper value. The data period is 2006–2014 (verification log, row 18). | https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop |
| 31 | Gompers, Kaplan & Mukharlyamov (2016), *JFE* 121(3):449–476 | found | *JFE*, 2016, SSRN DOI 10.2139/ssrn.2600524, 304 cit. The abstract confirms 79 investors, more than $750bn, and "rely primarily on internal rates of return and multiples". | https://consensus.app/papers/details/9c44ffc9ab6a5bdbaeebc0798a59f4d5/?utm_source=claude_desktop |
| 32 | Gupta & Van Nieuwerburgh (2019/2021), NBER WP 26514 (*JF* 2021†) | found; remove † | *JF* 2021, DOI 10.1111/jofi.13073, 24 cit. Negative risk-adjusted profits for the average fund in most categories. | https://consensus.app/papers/details/a07fbcfb0fdd5d5891ce4d67340cbeb8/?utm_source=claude_desktop |
| 33 | Andonov & Rauh (2018), Stanford GSB WP 3659 (*RFS* 2022†) | found (WP record) | "The Return Expectations of Institutional Investors", SSRN 2019, DOI 10.2139/ssrn.3091976, 54 cit. The abstract confirms "In private equity, the extrapolation of past performance is driven by stale investments." The *RFS* version was not returned; keep the †. | https://consensus.app/papers/details/ed7719fccddd54da8e7194de9784a9d6/?utm_source=claude_desktop |
| 34 | Ben-David, Graham & Harvey (2013), *QJE* 128(4):1547–1584 | found (SSRN record) | SSRN DOI 10.2139/ssrn.1640552, 527 cit. The abstract confirms more than 13,300 forecasts, 36% coverage of 80% intervals, and that miscalibrated firms invest more and use more debt. | https://consensus.app/papers/details/c521fdc6c47d5eb9bae7b451ebce14fc/?utm_source=claude_desktop |
| 35 | Kahneman & Lovallo (1993), *Mgmt Sci* 39(1):17–31 | found | DOI 10.1287/mnsc.39.1.17, 2268 cit. The dossier's quotation ("Overly optimistic forecasts result from the adoption of an inside view") is verbatim in the abstract. | https://consensus.app/papers/details/362af47ccd0951fdbdcba53cf4e1a7ba/?utm_source=claude_desktop |
| 36 | Lovallo, Clarke & Camerer (2012), *SMJ* 33(5):496–512 | found (Consensus venue label wrong) | Consensus shows "Southern Medical Journal", but DOI 10.1002/smj.962 is *Strategic Management Journal*; 106 cit. The dossier is correct. The abstract confirms the PE test and adds similarity-based forecasting (SBF). | https://consensus.app/papers/details/ed83cdf118b1502aa2f0891e3460e131/?utm_source=claude_desktop |
| 37 | Flyvbjerg (2006), *Project Management Journal* 37(3):5–15 | found | DOI 10.1177/875697280603700302, 461 cit. | https://consensus.app/papers/details/84dbc82fedfe545faca5e377dcfdda22/?utm_source=claude_desktop |
| 38 | Flyvbjerg, Skamris Holm & Buhl (2005), *JAPA* 71(2):131–146 | found; **add a note** | DOI 10.1080/01944360508976688, 809 cit. The abstract confirms 210 projects in 14 nations, a 106% average rail overestimate, roads off by more than ±20% in half of projects, and no improvement over 30 years. **It also states that the article is the subject of a Notice of Redundant Publication (*JAPA* 78(3):352, 2012)**, because a 2006 *Transport Reviews* duplicate, since retracted, reproduced it. The *JAPA* article stands. | https://consensus.app/papers/details/cdbd141e345f53678560f7f4ee38f3ed/?utm_source=claude_desktop |
| 39 | Bordalo, Gennaioli, La Porta & Shleifer (2019), *JF* 74(6):2839–2874 | found | DOI 10.1111/jofi.12833, 277 cit. | https://consensus.app/papers/details/9140f87365dc550e92436355c510a7c0/?utm_source=claude_desktop |
| 40 | Smith & Winkler (2006), *Mgmt Sci* 52(3):311–322 | found | DOI 10.1287/mnsc.1050.0451, 362 cit. | https://consensus.app/papers/details/bfffdcbd36c45ee1b9b2dbf025b8cafc/?utm_source=claude_desktop |
| 41 | Arkes & Blumer (1985), *OBHDP* 35(1):124–140† | found; remove † | DOI 10.1016/0749-5978(85)90049-4, 2564 cit. The abstract adds that people who had incurred a sunk cost "inflated their estimate of how likely a project was to succeed". That directly supports α_f > 0 when the original team writes the forecast [inference]. | https://consensus.app/papers/details/430c3de70ba65268a9b0b76602aae5d2/?utm_source=claude_desktop |
| 42 | Staw (1976), *OBHP* 16(1)† (reference 61) | found; remove † | *Organizational Behavior and Human Performance*, DOI 10.1016/0030-5073(76)90005-2, 2019 cit. The greatest escalation occurs when decision-makers are "personally responsible for negative consequences". | https://consensus.app/papers/details/52949433073e5d24a34d88f53b320076/?utm_source=claude_desktop |

**Not checked (18):**
- Numbered references: Black & Litterman (1992)†, Bühlmann & Straub (1970)†, Quarg & Mack (2004)†, Takahashi & Alexander (2002)†, Powell & Ryzhov (2012)†, Efron & Morris (1975), Clemen (1989), Boyer et al. (2018), Ilmanen et al. (2019) and Gibbs & Candès (2021).
- Eight background works in reference 61: Guler (2007), Shefrin & Statman (1985), Tetlock (2005), Mellers et al. (2014), Kalman (1960), Hoeting et al. (1999), Idzorek (2005) and Page (1954).
- Only Black–Litterman (Ω from confidence) and Bühlmann–Straub (exposure weights) feed a dossier formula. Both are standard; check them before the code is written.

### Verification-log items affected by these searches

| Verification item | What Consensus returned | Consensus URL |
|---|---|---|
| Row 5 (U): Jenkinson–Sousa–Stucke specifics (761 / 35% / Q4) | All confirmed by the indexed abstract | https://consensus.app/papers/details/e297da1e0d0658d8ae2ca7a7a7b6987c/?utm_source=claude_desktop |
| Row 29 (U): Barber–Yasuda mechanism | Confirmed by the indexed abstract | https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop |
| Row 26 (C, weak source): Cooke 26/33 | Primary source found (Colson & Cooke 2017). It shows that the dossier's §3 "in-sample" is wrong. | https://consensus.app/papers/details/dbe7edfbdd19501caa1d757e57fd4aad/?utm_source=claude_desktop |
| Row 8 (X): BGG figures | The indexed SSRN 2020 abstract gives 1.0/1.4 and 33%/40% | https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop |
| Row 17: Nadauld PMEs | The published abstract gives sellers 0.976 | https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop |
| Row 22 (U): PitchBook interim-versus-final R² | Not academic, and not found. A citable academic substitute is Noh et al. (2023, *Applied Economics*): interim versus final IRR for 238 liquidated buyout and 233 VC funds (1985–2019). Buyout interim performance tends to be underestimated; VC is under- or overestimated depending on the period. The abstract reports no R². | https://consensus.app/papers/details/08bfa07531845d8d9c74b9984e2fd7dc/?utm_source=claude_desktop |
| §5 weak sourcing: Bühlmann (Wikipedia), Bates & Granger (rdrr.io), MOS (Wikipedia) | Journal records with DOIs: rows 10, 1 and 17 | see rows 10, 1, 17 |

---

## 3. Annotated bibliography (25 papers)

Tags:
- **[cited]**: the dossier cites the paper.
- **[missed]**: the dossier does not cite it.
- **[challenge]**: the paper contradicts or qualifies a dossier recommendation.

### A. Combination weights and the forecast-combination puzzle

**1. [A Simple Explanation of the Forecast Combination Puzzle](https://consensus.app/papers/details/f8bdb7ea82bb52c681576c06475bb34a/?utm_source=claude_desktop)** [cited; challenge]
- Jeremy P. Smith et al. · 2009 · *Oxford Bulletin of Economics and Statistics* · 373 cit. · DOI 10.1111/j.1468-0084.2008.00541.x
- **Finding.**
  - Simple combinations beat weighted ones because of finite-sample error in estimating the weights.
  - Monte Carlo evidence and a large-sample approximation "support the popular recommendation to ignore forecast error covariances in estimating the weight".
- **Relevance.**
  - The dossier cites this paper for the puzzle but recommends full GLS with ρ_fu = 0.5 and ρ_fa = 0.3, estimated from history (§2.3, §6.4, §6.7).
  - With a few dozen effective pairs per group, the paper argues for diagonal or heavily shrunk Ω when computing weights [inference].
  - Correlation can still enter the posterior variance σ̂², which addresses the dossier's concern that independence overstates precision [inference].

**2. [Combining Forecasts - On Why Averaging Beats Optimal Linear Weights](https://consensus.app/papers/details/05b1b772993e59638a60da357348567e/?utm_source=claude_desktop)** [missed; challenge]
- Graham Elliott et al. · 2026 · *Journal of Business & Economic Statistics* · 2 cit. · DOI 10.1080/07350015.2026.2661980
- **Finding.**
  - Under empirically and theoretically reasonable restrictions, gains from optimal weights can be small.
  - Where gains can be large, the best approach is to discard some forecasts and average the rest. The authors derive a new weight estimator from this.
- **Relevance.**
  - This is a strong recent result on the dossier's "default weighting" choice.
  - The FBE benchmark should include "screen, then average the debiased signals", not only the prior-weighted GLS [inference].

**3. [Optimal and robust combination of forecasts via constrained optimization and shrinkage](https://consensus.app/papers/details/68f1a886329956979a4a484fc7a2fc9b/?utm_source=claude_desktop)** [missed]
- Francesco Roccazzella et al. · 2021 (per Consensus) · *International Journal of Forecasting* · 23 cit. · DOI 10.1016/j.ijforecast.2021.04.002
- **Finding.**
  - Weights are constrained to be non-negative and penalized by a divergence from a reference scheme, so selection and combination happen in one step.
  - Using the portfolio analogy, the paper gives an analytical optimal penalty strength for an L2 penalty toward equal weights.
- **Relevance.** This is a closed-form, IC-explainable default for the dossier's "shrink toward simple defaults, w ≥ 0" step, implemented in its own stack (cvxpy) [inference].

**4. [Combining expert forecasts: Can anything beat the simple average?](https://consensus.app/papers/details/cf9391f178015486ade67819ae4ef27f/?utm_source=claude_desktop)** [missed; challenge]
- Véronique Genre et al. · 2012 (per Consensus) · *International Journal of Forecasting* · 318 cit. · DOI 10.1016/j.ijforecast.2012.06.004
- **Finding.**
  - On the ECB Survey of Professional Forecasters, few schemes beat the equal-weight average for GDP and unemployment; the evidence is stronger for inflation. The schemes tested include performance weighting, least squares and Bayesian shrinkage.
  - After White's reality check, the results "caution against any assumption that the identified improvements would persist".
- **Relevance.** Any claim that the FBE beats simple averaging needs out-of-sample tests corrected for multiple comparisons [inference].

### B. Fusing predictive distributions, calibration and evaluation

**5. [Combining probability forecasts](https://consensus.app/papers/details/31e8187029a5589da40b94611fcee9f2/?utm_source=claude_desktop)** [missed; challenge]
- Roopesh Ranjan et al. · 2010 · *JRSS-B* · 275 cit. · DOI 10.1111/j.1467-9868.2009.00726.x
- **Finding.**
  - "Any non-trivial weighted average of two or more distinct, calibrated probability forecasts is necessarily uncalibrated and lacks sharpness", so linear pooling requires recalibration.
  - The paper proposes a beta-transformed linear pool.
- **Relevance.**
  - Several dossier steps produce linear pools: stacking of fusion variants (§3), IC views pooled with group views (§6.10), and posterior-predictive draws mixed with the scenario set (§6.9).
  - Each pooling step needs a recalibration layer and a fresh PIT check [inference].
  - The Gaussian precision-weighted posterior itself is a Bayesian update, not a linear pool, so this critique does not apply to it [inference].

**6. [Dynamic Bayesian predictive synthesis in time series forecasting](https://consensus.app/papers/details/33ee33f0e35a5f05a45ac5444023f8bd/?utm_source=claude_desktop)** [missed]
- K. McAlinn et al. · 2016 (per Consensus) · *Journal of Econometrics* · 134 cit. · DOI 10.1016/j.jeconom.2018.11.010
- **Finding.** Agent-opinion-analysis theory gives a density-combination framework that encompasses existing pooling methods. Dynamic latent factor models "adapt to time-varying biases, miscalibration and inter-dependencies among multiple models or forecasters".
- **Relevance.**
  - This is the principled dynamic version of the FBE's debias-and-fuse step. The dossier estimates α, β and Ω quarterly but treats them as static between refits.
  - Run it as the calibration agent's challenger model [inference].

**7. [Bayesian Hierarchical Stacking: Some Models Are (Somewhere) Useful](https://consensus.app/papers/details/a4b00b538ce85aec8fe94621ab013300/?utm_source=claude_desktop)** [missed]
- Yu-Ling Yao et al. · 2021 (per Consensus) · *Bayesian Analysis* · 60 cit. · DOI 10.1214/21-ba1287
- **Finding.** Stacking works best when models' predictive performance varies across inputs. Hierarchical stacking makes the weights functions of the inputs, partially pooled and estimated by Bayesian inference.
- **Relevance.** This extends the dossier's own stacking reference (Yao et al. 2018) to the case ADIC faces: the right weight on f, u and a differs by group, strategy and asset age, and the data are thin [inference].

**8. [Evaluating the Calibration of Multi-Step-Ahead Density Forecasts Using Raw Moments](https://consensus.app/papers/details/a665841d31cc55d188a58665426c71b0/?utm_source=claude_desktop)** [missed; challenge]
- M. Knüppel · 2015 · *Journal of Business & Economic Statistics* · 70 cit. · DOI 10.1080/07350015.2014.948175
- **Finding.**
  - PITs of multi-step-ahead forecasts are serially correlated.
  - Existing tests rely on data-dependent critical values, lack power, or have size distortions even asymptotically.
  - A raw-moments test on standardized PITs has correct size and good power.
- **Relevance.**
  - The dossier's calibration targets (§2.7, §6.9) assume i.i.d. PITs and binomial coverage.
  - ADIC's forecasts span overlapping multi-year horizons, so these tests over-reject. Use autocorrelation-robust tests [inference].

**9. [Local scale invariance and robustness of proper scoring rules](https://consensus.app/papers/details/9779c3c565ed561881f0049cd13e6098/?utm_source=claude_desktop)** [missed; challenge]
- D. Bolin et al. · 2019 (per Consensus) · *Statistical Science* · 32 cit. · DOI 10.1214/22-sts864
- **Finding.**
  - Averages of popular proper scores, including CRPS, give more weight to observations with large uncertainty, which can produce unintuitive rankings.
  - The scaled CRPS (SCRPS) is locally scale invariant, and the paper derives outlier-robust proper scores.
- **Relevance.**
  - The group scorecard's "CRPS skill" averages across assets with very different outcome uncertainty: venture total risk is about 40% a year (BGG, cited), far above core infrastructure. The most uncertain assets would dominate every group's score [inference].
  - Use SCRPS or standardized scores, and report by strategy [inference].

### C. How forecasters err, and finance precedents for debiasing

**10. [Overreaction in Macroeconomic Expectations](https://consensus.app/papers/details/4fabd9f27a1359a5a8e026ed6e04a384/?utm_source=claude_desktop)** [missed; challenge]
- P. Bordalo et al. · 2018 (per Consensus) · *American Economic Review* · 421 cit. · DOI 10.1257/aer.20181219
- **Finding.** Using Coibion–Gorodnichenko regressions of forecast errors on revisions, "individual forecasters typically overreact to news, while consensus forecasts under-react". A diagnostic-expectations model reconciles the two.
- **Relevance.**
  - β_f and flag F8 (revision drift) should be estimated at the level where the forecast is produced: an individual deal team versus a group-level consensus. The sign can differ [inference].
  - Replace F8's "3+ same-sign revisions" count with a regression of error on revision [inference].

**11. [A New Approach to Predicting Analyst Forecast Errors: Do Investors Overweight Analyst Forecasts?](https://consensus.app/papers/details/c5040412da0b5ed6a325a4e87f819007/?utm_source=claude_desktop)** [missed]
- Eric C. So · 2013 · *Journal of Financial Economics* · 221 cit. · DOI 10.1016/j.jfineco.2013.02.002
- **Finding.**
  - "Characteristic forecasts" map firm characteristics into future earnings.
  - Contrasting characteristic and analyst forecasts predicts analyst forecast errors and revisions, and prices do not fully reflect these predictable errors.
- **Relevance.**
  - This is the finance precedent for the dossier's MOS-style debiasing with bias covariates x_i (§6.1, §6.7).
  - Add a point-in-time characteristic forecast per asset as an extra signal. The gap between f and that forecast is the key covariate [inference].

**12. [Man versus Machine Learning: The Term Structure of Earnings Expectations and Conditional Biases](https://consensus.app/papers/details/7234d3491eba54459de63f6d3e6d99d4/?utm_source=claude_desktop)** [missed; challenge]
- J. V. van Binsbergen et al. · 2022 (per Consensus) · *The Review of Financial Studies* · 39 cit. · DOI 10.1093/rfs/hhac085
- **Finding.**
  - Conditional bias is defined as analysts' expectations minus a statistically optimal ML benchmark. On average it is upward and "increases in the forecast horizon".
  - It predicts negative returns, and managers of firms with the most upward-biased forecasts are more likely to issue stock.
  - "Commonly used linear earnings models do not work out-of-sample and are inferior to those analysts provide."
- **Relevance.**
  - Bias should depend on the remaining horizon H [inference].
  - A naïve linear reference-class prior may be *less* accurate than the group forecast, so the prior's weight must be earned out of sample, not assumed [inference].
  - The issuance result is the analogue of the dossier's "strategic misrepresentation" term [inference].

**13. [The Persistence of Miscalibration](https://consensus.app/papers/details/b4ff9b1507b756f1affc7bfc68dd8a4c/?utm_source=claude_desktop)** [missed]
- M. Boutros et al. · 2020 · *SSRN Electronic Journal* · 21 cit. · DOI 10.2139/ssrn.3462107
- **Finding.** In more than 28,400 CFO forecasts of the S&P 500, intervals that are too narrow show "no improvement with task repetition or evidence of learning". Miscalibration "appears to be a persistent personal trait".
- **Relevance.**
  - The dossier widens stated ranges by ×1.81–2.74 (§6.8 Example 5). Make the widening person-specific and permanent rather than expecting feedback to remove it [inference].
  - Add forecaster-level random effects to θ_g [inference].

**14. [Investor Sentiment and Analysts' Earnings Forecast Errors](https://consensus.app/papers/details/a6db6d24c8e15a899e64fabe11140591/?utm_source=claude_desktop)** [missed]
- P. Hribar et al. · 2012 · *Management Science* · 287 cit. · DOI 10.1287/mnsc.1110.1356
- **Finding.** When sentiment is high, analysts' one-year and long-term growth forecasts are relatively more optimistic for "uncertain" or "difficult-to-value" firms. The bias "is unlikely to be strategic in nature".
- **Relevance.**
  - This answers the dossier's open question 4: optimism is conditional on the state.
  - Make α_f a function of the State/Fragility engine's regime z and of how hard the asset is to value, larger for VC and growth than for core infrastructure [inference].

### D. Elicitation, aggregation and incentives for groups and the IC

**15. [Cross validation for the classical model of structured expert judgment](https://consensus.app/papers/details/dbe7edfbdd19501caa1d757e57fd4aad/?utm_source=claude_desktop)** [missed; corrects the dossier]
- A. Colson et al. · 2017 · *Reliability Engineering & System Safety* · 106 cit. · DOI 10.1016/j.ress.2017.02.003
- **Finding.**
  - In 33 post-2006 studies, performance weighting beat equal weighting in-sample in all but one study.
  - Out of sample there is a penalty: statistical accuracy falls below equal weighting. It reaches 75% of the equal-weight value when training sets hold 80% of the calibration variables.
  - Informativeness doubles once training sets hold at least 50% of them.
  - On the authors' out-of-sample validity index, performance weighting wins 26 of 33.
- **Relevance.**
  - This is the primary source for the dossier's statistic, which mislabels it as in-sample.
  - Performance-weighting IC members (§6.10) needs a large bank of resolved, relevant seed questions. Default to equal weights until it exists [inference].

**16. [Wisdom/Madness of Crowds and Perils of Point Forecasts](https://consensus.app/papers/details/9c1e4f9af0845fba93c7333b6060aba7/?utm_source=claude_desktop)** [missed; challenge]
- Roger M. Cooke · 2026 · *Decision Analysis* · 1 cit. · DOI 10.1287/deca.2025.0437
- **Finding.**
  - Expert point-forecast errors are "very fat tailed", and their averages may not converge.
  - More experts or more diverse panels *degrade* aggregated point forecasts. With probabilistic forecasts, both help.
  - "Point estimates elicited from multiple experts should not be aggregated"; aggregate distributions instead, preferably with performance weights.
- **Relevance.**
  - The FBE fuses u and f mostly as points (§6.4), with ranges only as a heteroscedasticity input.
  - Elicit P10/P50/P90 from deal teams, groups and IC members, and fuse distributions [inference].

**17. [Extracting the Wisdom of Crowds When Information Is Shared](https://consensus.app/papers/details/4ec1cb2ce9b05effba83cec250fb50c2/?utm_source=claude_desktop)** [missed]
- Asa B. Palley et al. · 2019 · *Management Science* · 79 cit. · DOI 10.1287/mnsc.2018.3047
- **Finding.**
  - Shared information creates correlated errors.
  - Ask each respondent for their own forecast and a guess of the average forecast of others. "Pivoting" then separates shared from private information and recombines them optimally, beating the simple average.
- **Relevance.**
  - The dossier's central dependence problem is that f is anchored on u and on the current mark.
  - Ask each group for its forecast and its prediction of the reference-class or peer forecast. The gap identifies private information, gives a direct estimate of ρ_fu and works in IC sessions too [inference].

**18. [Harnessing the Wisdom of Crowds](https://consensus.app/papers/details/49b11db4ec0c5f9bb3955f8a0fb7c08a/?utm_source=claude_desktop)** [missed]
- Zhi Da et al. · 2020 · *Management Science* · 147 cit. · DOI 10.2139/ssrn.2731884
- **Finding.**
  - On Estimize, users who viewed more public information put less weight on their own. Individual forecasts improved, but the consensus got worse.
  - Randomized experiments confirmed that independent forecasts make the consensus more accurate, and the platform switched to "blind" mode.
- **Relevance.**
  - Collect group forecasts and IC views *before* the belief card shows the prior, the underwriting or the bid.
  - The dossier already applies this to bids (§5.1: compute ADIC's view before reading the bid). Extend it to all elicitation [inference].

**19. [Probability Elicitation, Scoring Rules, and Competition Among Forecasters](https://consensus.app/papers/details/fe4cb9e41fbf5cd596aa6cfd0ce34799/?utm_source=claude_desktop)** [missed; challenge]
- Kenneth C. Lichtendahl et al. · 2007 · *Management Science* · 64 cit. · DOI 10.1287/mnsc.1070.0729
- **Finding.**
  - Forecasters who care about relative performance should report more extreme probabilities, which can make well-calibrated forecasters look overconfident.
  - A decision-maker can adjust for this.
  - Joint scoring rules based on business sharing are strictly proper.
- **Relevance.**
  - The dossier says proper scores make honesty optimal (§8). Group scorecards and published traffic lights create relative-performance incentives [inference].
  - Avoid rank tables. Consider joint or shared scores, and read F9 ("overconfident range") with incentives in mind [inference].

### E. Credibility and reserving

**20. [A Course in Credibility Theory and its Applications](https://consensus.app/papers/details/2175a651e7b75b57ad98f08ab7ffdb0b/?utm_source=claude_desktop)** [missed]
- Alois Gisler et al. (Bühlmann & Gisler) · 2005 · venue not shown (Springer book) · 379 cit. · DOI 10.1007/3-540-29273-x
- **Finding.**
  - No abstract is shown. The record lists the chapters: Bayes premium, credibility estimators, Bühlmann–Straub, large claims, hierarchical credibility, multidimensional credibility, credibility in the regression case, and evolutionary credibility with recursive calculation (univariate and multidimensional).
  - A book review in the same search describes Bühlmann's estimator as a linear approximation to the Bayesian predictive mean, with structural parameters estimated by empirical Bayes from aggregated data.
- **Relevance.**
  - Each FBE component has a chapter-level counterpart:
    - group → strategy → asset hierarchy: hierarchical credibility;
    - several sources: multidimensional credibility;
    - bias covariates: regression credibility;
    - Kalman belief updates (§6.9): evolutionary credibility.
  - Use it as the reference specification for the calibration agent [inference].

**21. [The Benktander Golden Stairs and other parameter-free credibility methods in loss reserving](https://consensus.app/papers/details/f0afe8fc96ab5554a91bcff8d4d2a12f/?utm_source=claude_desktop)** [missed]
- W. Neuhaus · 2025 · *Scandinavian Actuarial Journal* · 0 cit. · DOI 10.1080/03461238.2025.2536811
- **Finding.** On weighted-average relative efficiency, Benktander outperforms chain ladder and Bornhuetter–Ferguson. Three classes of alternative parameter-free credibility methods give a similar conclusion.
- **Relevance.**
  - The dossier plugs Mack's t = 0.5 into c* = p/(p+t) as a sourced default. Verification issue R4 shows that t = 0.5 is a switching rule, not a credibility parameter.
  - Until ADIC's triangles let t be estimated, use parameter-free Benktander, which needs only p [inference].

### F. PE marks, reference classes and the prior

**22. [How Fair are the Valuations of Private Equity Funds](https://consensus.app/papers/details/e297da1e0d0658d8ae2ca7a7a7b6987c/?utm_source=claude_desktop)** [cited; specifics now confirmed]
- Tim Jenkinson et al. · 2013 · venue not shown (SSRN DOI) · 88 cit. · DOI 10.2139/ssrn.2229547
- **Finding.** The paper uses the full history of 761 CalPERS fund investments.
  - Over a fund's life, valuations are conservative and smoothed, understating subsequent distributions by about 35%.
  - Valuations jump in Q4, when funds are audited.
  - They are inflated during follow-on fundraising, then gradually reverse.
  - Interim performance, especially IRR, predicts ultimate returns poorly; PME improves predictability.
- **Relevance.**
  - The indexed abstract confirms the numbers the verification log could not.
  - Keep F5 for fund NAVs.
  - Feed the "actual" signal with PME-type measures rather than since-inception IRR, as the dossier's forward-return translation already implies.

**23. [Do Private Equity Managers Raise Funds on (Sur)real Returns? Evidence from Deal-Level Data](https://consensus.app/papers/details/834e2e8848615de6808f6adbd5bdda10/?utm_source=claude_desktop)** [missed; challenge]
- Niklas Hüther · 2019 (per Consensus) · *Journal of Financial and Quantitative Analysis* · 8 cit. · DOI 10.1017/s0022109022000990
- **Finding.**
  - There is no evidence of inflated performance at the deal level.
  - Fund-level peaks reflect a cohort effect: "late investments are made under pressure before fundraising and have lower returns".
- **Relevance.**
  - Do not apply F5's mark haircut to co-investment or direct-deal marks [inference].
  - Instead add a deployment-pressure covariate, "invested late in the sponsor's investment period", to the bias model for the Co-investment group and the Secondaries group's direct deals [inference].

**24. [Institutions' return expectations across assets and time](https://consensus.app/papers/details/62e491254237554c8f213f500eb58995/?utm_source=claude_desktop)** [missed]
- Magnus Dahlquist et al. · 2026 · *Journal of Financial Economics* · 0 cit. · DOI 10.1016/j.jfineco.2025.104188
- **Finding.**
  - The sample covers asset managers, consultants, wealth advisors, public pensions and professional forecasters.
  - Their subjective risk premia "vary one-to-one with objective risk premia" available in real time and are countercyclical.
  - Several equity premia vary more across institutions than over time, and the heterogeneity persists.
- **Relevance.**
  - The prior mean m_k⁰ is anchored on one house CMA (JPM 2027 LTCMA, §6.3).
  - Use several CMAs and add their cross-sectional dispersion to the prior's variance, so that prior-mean uncertainty is not treated as zero [inference].

**25. [Governing Large Projects: A Three-Stage Process to Get It Right](https://consensus.app/papers/details/883bb411756958febb3bb698bfbdb88a/?utm_source=claude_desktop)** [missed]
- Dan Lovallo et al. · 2023 · *Academy of Management Perspectives* · 35 cit. · DOI 10.5465/amp.2021-0129
- **Finding.**
  - The paper reviews evidence for the accuracy of reference-class forecasting and newer extensions such as similarity-based forecasting.
  - It sets out organizational remedies for unfounded optimism and deception: debiasing techniques and measures that curb principal–agent problems.
- **Relevance.**
  - Similarity-based forecasting suits the reference-class librarian agent: weight analogues by similarity instead of hard class boundaries [inference].
  - The governance remedies map onto the Challenger agent and the IC's role [inference].

---

## 4. Missed-but-important papers and their design implications

### 4.1 State variables

| State to add or change | Evidence | Where it enters |
|---|---|---|
| **Forecaster identity** (deal team or person), with a persistent calibration effect | Boutros et al. 2020 (#13); [Atanasov et al. 2020](https://consensus.app/papers/details/f16b54b0d90f5d9a97e55c096c467cd4/?utm_source=claude_desktop) (the most accurate forecasters make frequent, small updates; low-skill forecasters confirm their initial judgments or make large, infrequent revisions) | θ_g becomes θ_{g,person}. The EMOS spread term carries a person random effect. Revision style becomes a credibility covariate [inference]. |
| **Revision path** (frequency, size, sign, confirmation) | Bordalo et al. 2020 (#10); [Adam et al. 2025](https://consensus.app/papers/details/ee63acaddf2f5402b78c257b2bc0e189/?utm_source=claude_desktop) (anchored to prior beliefs; overreact to private information; errors correlate positively with past revisions at the consensus level but negatively at the individual level); [McElroy 2025](https://consensus.app/papers/details/4d4b2c1459185b129f2707bb33d67b9b/?utm_source=claude_desktop) (revision-efficiency tests are biased under public noise; instrument revisions with past errors) | Bias covariates x_i. F8 becomes an IV regression of error on revision, run separately for teams and for group consensus [inference]. |
| **Sentiment or regime z** in the bias terms | Hribar & McInnis 2012 (#14); [Kremer et al. 2011](https://consensus.app/papers/details/5b81a4368144592bb1cfe3ea430e160d/?utm_source=claude_desktop) (forecasters overreact in stable environments and underreact in unstable ones) | α_f(z) and β_f(z), using the State/Fragility engine's z [inference] |
| **Remaining horizon H** as a bias covariate | van Binsbergen et al. (#12); [Afrouzi et al. 2023](https://consensus.app/papers/details/f9410fbf367c5f72bea3bc4edf839eed/?utm_source=claude_desktop) (overreaction is stronger for longer horizons and less persistent processes); [Wessel et al. 2024](https://consensus.app/papers/details/5fb7786a0b6c5e218896c9febfe11cc7/?utm_source=claude_desktop) (one lead-time-continuous post-processing model, with lead time as a covariate, matches or beats separate models when data are scarce) | One pooled α_f(H) and ω_f(H), instead of a separate "late-life" parameter set [inference] |
| **Information overlap** between f and u | Palley & Soll (#17); [Lee & Seregina](https://consensus.app/papers/details/017aefa264895a399d7ace3bda903dcb/?utm_source=claude_desktop) (forecasters share information and so make common mistakes; a factor graphical LASSO separates common from idiosyncratic errors, with regime-dependent weights) | Ω estimation; a pivoting adjustment to f [inference] |
| **Characteristic (machine) benchmark** c_i per asset | So 2013 (#11); van Binsbergen et al. (#12); [Gao et al. 2014](https://consensus.app/papers/details/8632b8d2fd905f8ca3868a6b4b8965b3/?utm_source=claude_desktop) (combining analysts' long-term growth forecasts with past growth, forward E/P and past returns gives unbiased, more accurate growth forecasts) | A new signal in the fusion. The conditional bias f − c_i becomes the main bias covariate [inference]. |
| **Valuation-regime flags**: ASC 820 era; auditor and third-party valuation provider; sign of the public-market move during the reporting lag | [Easton et al. 2020](https://consensus.app/papers/details/1413389f130f5efdabeb8b4a6f93c1aa/?utm_source=claude_desktop) (after ASC 820, NAVs of liquidated funds predict future net distributions more accurately); [Easton et al. 2024](https://consensus.app/papers/details/82772d8ae414565ea614e5534a8dac23/?utm_source=claude_desktop) (reporting quality varies with auditor involvement and third-party providers, differently for buyout and VC); [Meng et al. 2019](https://consensus.app/papers/details/be4aa6e7580057658f0363a55efb7f1c/?utm_source=claude_desktop) (a summary of Czasonis, Kritzman & Turkington: managers raise marks when markets rise during the reporting delay but do not lower them when markets fall; Q4 differs because it is audited) | The NAV-bias term ψ_k in the nowcast. ADIC's 18-year corpus spans the 2008 ASC 820 change, so calibration needs an era dummy [inference]. |
| **Deal cohort within the sponsor fund** (deployment pressure) | Hüther (#23); [Degeorge et al. 2012](https://consensus.app/papers/details/0133ed403d8755e9abbb9552d5ee3003/?utm_source=claude_desktop) (secondary-buyout underperformance is confined to deals made under buying pressure, towards the end of the investment period) | x_i for co-investments and for the Secondaries group's direct deals [inference] |
| **Cross-institution dispersion of CMAs** | Dahlquist et al. 2026 (#24); [Jennings et al. 2025](https://consensus.app/papers/details/9b6b3b75e3025b3ca3c12a7e11547e5b/?utm_source=claude_desktop) (consultants' PE and VC CMAs embed "a meaningful differentiated return unrelated to factors") | The prior's mean and variance. Strip unevidenced non-factor return from PE CMAs before using them as m_k⁰ [inference]. |
| **Manager scale** for Public Markets alpha forecasts | [Dahlquist et al. 2025](https://consensus.app/papers/details/708fa38c07db5a6d82c72d9a0a22eec1/?utm_source=claude_desktop) (analyst-implied fund alphas ignore decreasing returns to scale; ratings from a rational-learning model outperform analysts' ratings out of sample) | A bias covariate for the Public Markets group's manager-alpha expectations. A rational-learning model serves as that group's "machine benchmark" [inference]. |

### 4.2 Models

1. **Recalibrate after every pooling step.**
   - Pooling steps include stacking of fusion variants, mixing IC views with group views, and entropy-pooled scenario sets.
   - Apply a beta-transformed or spread-adjusted linear pool: Ranjan & Gneiting (#5) and [Gneiting & Ranjan](https://consensus.app/papers/details/a555c675dd495eb2ae31ccbb56398421/?utm_source=claude_desktop) (generalized, spread-adjusted and beta-transformed pools; density forecasts of S&P 500 returns).
   - Then run a second-stage Mincer–Zarnowitz check on the fused mean. [Pincheira-Brown et al. 2023](https://consensus.app/papers/details/cf1c3452f9b45b96ae411f9fcff72f02/?utm_source=claude_desktop) show that convex combinations are "almost always" MZ-inefficient, even when each input is efficient [inference].
   - When individual signals are biased, quantile averaging beats linear or log pools ([Busetti](https://consensus.app/papers/details/01c8e29a772c59e5af94e7f6efe1643c/?utm_source=claude_desktop)).
2. **Add dynamic and hierarchical challengers to the static GLS fusion.**
   - Dynamic Bayesian predictive synthesis (#6) and hierarchical stacking (#7).
   - Time-varying weights from past performance with an incomplete model set ([Billio et al. 2013](https://consensus.app/papers/details/b101b72fe4b457bf983ed637dcbc04b5/?utm_source=claude_desktop)).
   - Keep the closed-form posterior for IC legibility, but require it to match or beat these challengers out of sample [inference].
3. **"Machine benchmark" debiasing.**
   - Build a point-in-time, nonlinear benchmark forecast from memo features (#11, #12). Use f minus the benchmark as the bias regressor.
   - Gradient-boosted or regularized models are reasonable here, consistent with the dossier's "bias covariates only, heavily regularized" (§3) [inference].
4. **Credibility specification.** Bühlmann & Gisler (#20) gives the overall structure. Specific pieces:
   - [Bühlmann, Shevchenko & Wüthrich 2007](https://consensus.app/papers/details/cb1c53d0d20f58759d5e08e64d850dc9/?utm_source=claude_desktop): a full credibility approach combining internal data, expert opinion and industry data. This is ADIC's problem with its own history, group forecasts and reference classes.
   - [Yan & Song 2022](https://consensus.app/papers/details/8ada59d414f056558f066d2b7cb051ca/?utm_source=claude_desktop): Bühlmann's linear estimator "is not robust and sensitive to heavy-tailed" claims. An optimally weighted combination of robust and efficient credibility estimators fixes this, which matters for VC.
   - [Hong & Martin 2021](https://consensus.app/papers/details/d5f640e5868a5ecab3dabdd40132f583/?utm_source=claude_desktop): an "imprecise credibility" interval estimator that stays robust when the hyperparameters are uncertain. This is a natural robust-scenario output for the IC [inference].
5. **Reserving module (§6.6).**
   - Use parameter-free Benktander or Golden-Stairs weights until t can be estimated (#21; [Hürlimann 2009](https://consensus.app/papers/details/1190b7fa60185988b095a75ea258050e/?utm_source=claude_desktop), pragmatic optimal credibility weights with a straightforward MSE calculation).
   - Model calendar-year (diagonal) effects such as 2022-type markdowns. [Bühlmann & Moriconi 2015](https://consensus.app/papers/details/be97fa10984d5f0c95424ac68d17b8fb/?utm_source=claude_desktop) find that random diagonal effects "can be significant for the reserve estimates and, especially, for the evaluation of the MSEP".
   - A Dirichlet model nests chain ladder and BF and lets the available information select between them ([Sriram & Shi 2019](https://consensus.app/papers/details/b1ce2149bd505489ae79cff993d4cbf1/?utm_source=claude_desktop)).
   - [Wüthrich & Merz 2008](https://consensus.app/papers/details/0798e46d291b5665adcab469bcbd287f/?utm_source=claude_desktop) collects credible reserving, Bühlmann–Straub, multidimensional credibility, the Kalman filter and the Munich chain ladder in one text. That also covers the dossier's Quarg & Mack† reference.
6. **Entropy pooling of the 50,000-path set (§6.9).**
   - Monitor the effective number of scenarios after tilting ([Meucci 2012](https://consensus.app/papers/details/9602d72f6f065f43974fbfbb196c33bc/?utm_source=claude_desktop)), so that strong views do not collapse the tails onto a few paths [inference].
   - Views on remaining-life returns have different horizons. [Meucci et al. 2016](https://consensus.app/papers/details/2e6d41892d2d5ec88144b81f8ac418b8/?utm_source=claude_desktop) (dynamic entropy pooling) handles "non-synchronous views" with life spans "from minutes to years".
   - For tail views, [Meucci et al. 2011](https://consensus.app/papers/details/c95d627e659850a0aec5cd0476452d2c/?utm_source=claude_desktop) processes views on conditional value at risk and represents the distribution on a grid.
7. **Rationality and calibration tests for fixed-event, multi-horizon forecasts.**
   - A generalized MZ regression of the outcome on the longest-horizon forecast and all intermediate revisions, plus multi-horizon bound tests, has good power. Source: the discussion record of [Patton & Timmermann (2012)](https://consensus.app/papers/details/e8a527e05c3f5bfb839904cab0663048/?utm_source=claude_desktop).
   - When forecasts mix models and judgment, use two-stage least squares with the consensus forecast as instrument ([Franses 2021](https://consensus.app/papers/details/947504438eb45ac19dd31edc83d45140/?utm_source=claude_desktop)).
   - MZ quantile regressions recover the forecaster's implied loss asymmetry ([Gűler et al. 2017](https://consensus.app/papers/details/4d7f4d3fbd9c55329fbd01595af1f512/?utm_source=claude_desktop); the Fed treats over-prediction as about 1.5 times as costly as under-prediction). For ADIC this separates deliberate asymmetric loss from bias [inference].
   - Multi-step PIT tests: Knüppel (#8). A small-sample density test with power at about 100 observations: [Berkowitz 2001](https://consensus.app/papers/details/b43b64b8701c500aa8b65ba693be532c/?utm_source=claude_desktop).

### 4.3 Parameters

| Parameter | Dossier | Literature | Suggested change [inference] |
|---|---|---|---|
| ρ_fu, ρ_fa used in the weights | 0.5 and 0.3, then estimated from history (§6.4, §6.7) | Ignore error covariances when estimating weights (Smith & Wallis, #1). Simple combinations that ignore correlations "often dominate" ([Timmermann 2005](https://consensus.app/papers/details/4fd1e95759945288b568eb0ffc5600f2/?utm_source=claude_desktop)). | Compute weights from diagonal Ω or a strongly shrunk Ω. Use the full Ω only for σ̂². Estimate ρ from cross-source differences and pivoting (Palley & Soll), not from raw errors (see verification issue R3). |
| Shrinkage intensity toward simple weights | "Shrink to simple defaults"; w ≥ 0 | Large shrinkage was optimal for US GNP forecasts (Diebold & Pauly, cited). Closed-form optimal L2 penalty toward equal weights under w ≥ 0 (Roccazzella et al., #3). Positive, sum-to-one constraints act as shrinkage ([Conflitti et al. 2015](https://consensus.app/papers/details/074806288ac7580ebd7e5806074cf24b/?utm_source=claude_desktop)). | Use the Roccazzella closed form as the default intensity. Show the shrunk weights as the IC "votes". |
| β_f | 1.0, allowing values above 1 for overreaction | Individuals overreact while consensus underreacts (#10). Forecasters are anchored to priors (Adam et al.). High persistence with overreaction is observationally equivalent to low persistence with underreaction in CG regressions ([Yee 2026](https://consensus.app/papers/details/de7eded70fcc594f8305ac5f5d63d65c/?utm_source=claude_desktop)). | Centre the prior at 1 with symmetric room on both sides. Estimate it separately for team-level and group-consensus forecasts, and identify it jointly with persistence. |
| α_f | +0.03 constant; +0.04 late-life | Optimism is sentiment-conditional for hard-to-value firms (#14). Bias rises with horizon (#12). | α_f(z, H, hard-to-value). Keep a separate exit-timing term for late-life funds, which is a different mechanism. |
| Range widening (ω_f) | ×1.81–2.74 from calibration (Example 5) | Miscalibration is a persistent personal trait with no learning (#13). In a near-doubled sample "the degree of miscalibration has worsened" ([Ben-David et al. 2019 slides](https://consensus.app/papers/details/a30deeb4126f5a08a4504dd558e98258/?utm_source=claude_desktop)). | Make widening permanent and person-specific; do not decay it with feedback. |
| Mack t in c* = p/(p+t) | 0.5, presented as sourced (§6.4) | Parameter-free Benktander-type methods outperform chain ladder and BF (#21). Pragmatic optimal weights (Hürlimann 2009). | Use Benktander, which is parameter-free, until ADIC triangles allow t to be estimated. This also resolves verification issue R4. |
| Down-weighting of old vintages | 8-year half-life [I] | MOS bias correction uses a decaying average; the decay factor trades short-term against long-term bias ([Glahn 2014](https://consensus.app/papers/details/6449b8649eb05e48b9993b5f7beb8146/?utm_source=claude_desktop)). | Choose the half-life by out-of-sample CRPS or log score on the memo corpus. |
| Prior mean m_k⁰ and its uncertainty | One house CMA; σ_k measures the dispersion of true expected returns only | CMAs are heterogeneous across institutions (#24). Consultants embed non-factor return in PE CMAs (Jennings et al. 2025). | Use several CMAs. Add cross-CMA dispersion as prior-mean uncertainty, shared by every asset in a class, as a common shock in the simulator. |
| Eligibility for performance weights (IC members, groups) | Cooke weights from resolved seeds | Out-of-sample statistical accuracy stays below equal weighting, reaching 75% of it with 80% training sets (#15). Irrelevant seed questions mean equal weights should be used ([Hemming et al. 2021](https://consensus.app/papers/details/4c889a151c4a5571817fc9197b2a7091/?utm_source=claude_desktop)). Performance-weighted aggregation drops out of sample ([Lin & Cheng 2009](https://consensus.app/papers/details/0600cc6851f5567d9388ef2981d221f8/?utm_source=claude_desktop)). Empirical-Bayes shrinkage of weights helps in small experiments ([Dharmarathne et al. 2023](https://consensus.app/papers/details/0ad2cee67b5e563f9f988d516eb65990/?utm_source=claude_desktop)). | Use equal weights until enough relevant, resolved seeds exist, then shrunk performance weights. |
| NAV-bias correction ψ_k | A fundraising-window adjustment | No deal-level inflation (#23). ASC 820 improved accuracy (Easton et al. 2020). Asymmetric response to lag-period moves (Meng et al. 2019 summary). Interim valuations were conservative early and normalized after 4–6 years in UK data ([Ellis et al. 2011](https://consensus.app/papers/details/ab6497018bed5a71b6c824c19d3e6e0c/?utm_source=claude_desktop)). | Make ψ depend on level (fund or deal), era (before or after 2008), fund age and the sign of the lag-period market move. |

### 4.4 Constraints

- **Screen before averaging.** Drop low-accuracy or highly correlated sources, then use a trimmed mean ([Lichtendahl & Winkler 2020](https://consensus.app/papers/details/8a5450469fc2591e9db6a5f55f6175dc/?utm_source=claude_desktop)). "Discard most, average the rest" (Diebold & Shin, cited; Elliott et al., #2). Keep w ≥ 0 and sum-to-one, which act as shrinkage (Conflitti et al. 2015).
- **Relevance of seed questions.** Performance weights may only use resolved forecasts from the same strategy and role (Hemming et al. 2021) [inference].
- **Entropy-pooling tilt budget.** Set a floor on the effective number of scenarios after tilting (Meucci 2012). A view that breaches the floor goes to the IC as a scenario, not a tilt [inference].
- **Independence of elicitation.** Group forecasts and IC views must be time-stamped before the belief card is shown (Da & Huang, #18). Enforce this in the bitemporal archive the dossier already proposes [inference].

### 4.5 Objectives, scoring and calibration targets

- **Scores pooled across assets:** use SCRPS or standardized scores (Bolin & Wallin, #9). Always include the log score: CRPS "prefers the outcome close to the median of the forecast distribution regardless of the probability mass" ([Du 2021](https://consensus.app/papers/details/be5d4378ba92552aa42ec7ec93d5c252/?utm_source=claude_desktop)).
- **Downside emphasis** for SELL, LEVER and REFINANCE gates:
  - censored-likelihood and localized proper scores, which have "excellent power properties" ([Diks & van der Weide 2025](https://consensus.app/papers/details/57fab6e0abd75f0487522b5ef33ef0d5/?utm_source=claude_desktop));
  - threshold-weighted CRPS and related scores ([Allen 2023](https://consensus.app/papers/details/bcbaf16f504158e7b131f9fb388391a1/?utm_source=claude_desktop)).
  - Conclusions "vary greatly across different scoring rules", so the choice must fit the decision ([Merkle & Steyvers 2013](https://consensus.app/papers/details/f48c829019b0503f9dec2e0227a63b37/?utm_source=claude_desktop)).
- **Feedback before outcomes resolve.** Private-asset forecasts take years to resolve.
  - Proxy scoring rules give immediate scores and are "competitive with proper scoring rules when the number of questions is small" ([Witkowski et al. 2017](https://consensus.app/papers/details/7e9fbfa502db5b1890af53557c908b60/?utm_source=claude_desktop)).
  - Scoring against the best ex-post aggregate of peers predicts out-of-sample skill better than scoring against noisy outcomes ([WOMAC, Srinivasan et al. 2025](https://consensus.app/papers/details/126058e1f2e15bcc961b82192fadb453/?utm_source=claude_desktop)).
  - Candidate proxies for ADIC: later fused posteriors, secondary bids and realized DPI [inference].
- **Group scorecard decomposition.**
  - Split scores into miscalibration, discrimination and uncertainty, with inference ([Dimitriadis et al. 2026](https://consensus.app/papers/details/528dbdd5b3da57c28138496eb1d8fa29/?utm_source=claude_desktop)).
  - Use conditional decompositions to find the regimes in which a group's forecasts fail ([Allen et al. 2023](https://consensus.app/papers/details/0312c1a9c93a5eca8b2680b63b5e8ba4/?utm_source=claude_desktop)).
  - Decompose aggregator gains into bias, information and noise ([Salikhov et al. 2022](https://consensus.app/papers/details/cdc0f1ab80a4579ba473bf793ae2dfab/?utm_source=claude_desktop)). Simple averaging "operates almost entirely by reducing noise".
- **Estimation objective for EMOS.**
  - Minimum-CRPS and maximum-likelihood fits that disagree signal misspecification. Heavy-tailed logistic or Student-t distributions improve calibration ([Gebetsberger et al. 2018](https://consensus.app/papers/details/759928e4b0415166a0453ca0a1cf151d/?utm_source=claude_desktop)).
  - This supports the dossier's skew-t for VC and argues for running both fits as a diagnostic [inference].

### 4.6 Agent and IC design

- **Elicitation protocol** (Translator agent and IC briefer):
  1. Collect forecasts blind (Da & Huang, #18).
  2. Ask for distributions, not points: P10, P50 and P90 (Cooke 2026, #16). [Cooke et al. 2021](https://consensus.app/papers/details/c12996d48dda566f88cc5538b1d71b20/?utm_source=claude_desktop) find that "medians of combined expert distributions outperform combined medians" and that performance weighting adds more.
  3. Ask for a prediction of peers' or the reference-class forecast, to support pivoting (Palley & Soll, #17; [Palley & Satopää 2023](https://consensus.app/papers/details/795b23f7f2d950ce90974d390c7b1967/?utm_source=claude_desktop), closed-form weights from peer predictions; [McCoy & Prelec 2023](https://consensus.app/papers/details/845de03d07fe5bda901c5ade7b02a21d/?utm_source=claude_desktop), a hierarchical model that does not privilege majority opinion).
- **Deliberation format.**
  - Small independent groups that deliberate, then aggregate. "Combining as few as four consensus choices outperformed the wisdom of thousands" ([Navajas et al. 2018](https://consensus.app/papers/details/2bf6f067143a5f8a80ab6ab330eb3534/?utm_source=claude_desktop)).
  - Teamed prediction polls with temporal decay, performance weighting and recalibration beat prediction markets ([Atanasov et al. 2017](https://consensus.app/papers/details/8586986bbee753508ac70bd80195dea8/?utm_source=claude_desktop)).
  - For the shadow IC: break-out pairs by group, then pool [inference].
- **Dispersion is not uncertainty.** Spread across views captures between-view variance but misses within-view variance ([Raftery et al. 2005](https://consensus.app/papers/details/d38125954a535e879f1545055a9dcd4a/?utm_source=claude_desktop), BMA variance decomposition). The belief card should show both [inference].
- **Incentives.**
  - Do not run rank tournaments among groups (Lichtendahl & Winkler, #19). Winner-take-all prizes distort reports toward extremes; incentive-compatible competition mechanisms exist ([Witkowski et al. 2023](https://consensus.app/papers/details/4e78c77d15a55452942b3ca0721c296a/?utm_source=claude_desktop)).
  - Nuance: competitive forecasters exaggerate private information, which can make the *average* of competitive forecasts more accurate than the average of truthful ones ([Lichtendahl et al. 2013](https://consensus.app/papers/details/d3dea0152fe4520392dce33f9b9d0a8c/?utm_source=claude_desktop)).
  - Score and fuse distributions, and treat individual-level exaggeration as a known distortion [inference].
- **De-escalation, for the Challenger agent and the IC.**
  - Three techniques worked best: make negative outcomes less threatening; set minimum target levels that trigger a policy change in advance; evaluate decision-makers on process rather than outcome ([Simonson & Staw 1992](https://consensus.app/papers/details/54b9be547b3e588a9d3ab6cb9c92225e/?utm_source=claude_desktop)). These map onto pre-set HOLD-review triggers and process-based group scorecards [inference].
  - Specific instructions on normative incremental-decision rules reduced escalation; simple warnings did not ([Ohlert & Weißenberger 2020](https://consensus.app/papers/details/2999228ae82e5b49b9e4ba31bba7d681/?utm_source=claude_desktop)). The belief card should *show* the forward-only rule, not merely warn about sunk costs [inference].
  - Handing the decision to a second person fails when that person is psychologically connected to the first ([Gunia et al. 2009](https://consensus.app/papers/details/0611bccf089a58018e6197e17d9c2e44/?utm_source=claude_desktop)). The Challenger must be independent of the originating team [inference].
  - Staw (1976, cited) supports a bias covariate for "forecaster is the original underwriter".
- **Reference-class librarian.**
  - Reference-class forecasting is mainly shown effective for large projects, and its effectiveness "depends on the definition of the reference class" ([Bärenbold 2023](https://consensus.app/papers/details/e261cc8647da57b38191bc2bbfa8bad3/?utm_source=claude_desktop)).
  - Use similarity-based analogues (Lovallo et al. 2012, cited; #25).
  - Track forecast accuracy by development stage, as the Hong Kong RCF study did with stage-dependent accuracy distributions ([Flyvbjerg et al. 2016](https://consensus.app/papers/details/3e086a7467ef5274b23a8184f3c7d009/?utm_source=claude_desktop)). This is the analogue of credibility that depends on maturity [inference].
- **Feedback to groups.** Outcome feedback reduced over-forecasting and overconfidence but raised noise enough to cancel the accuracy gain ([Niu & Harvey 2021](https://consensus.app/papers/details/0641e76ff3cc50799be206a9f0ff7582/?utm_source=claude_desktop)). Scorecards should report noise as well as bias [inference].
- **Mapping to groups** [inference]:
  - Fund-level NAV evidence applies to the PE group and to the Secondaries group's fund commitments.
  - Deal-level evidence (#23; [Braun et al. 2017](https://consensus.app/papers/details/00af5930c4c75ef99ef2ac1654c52789/?utm_source=claude_desktop), deal-level buyout persistence "has substantially declined") applies to Co-investment and the Secondaries group's direct deals.
  - Manager-alpha evidence (Dahlquist et al. 2025) applies to Public Markets.
  - **Gap:** our searches returned no behavioural evidence specific to private-credit or structured-capital yield forecasts. Treat the Private Credit and Capital Solutions groups' bias priors as wide.
  - The Corporate Finance / Treasury seat consumes the posterior quantiles for LEVER gates. Its liquidity forecasts should enter the same scoring system.
- **Survey for the IC-deliberation stream.** [Novelli et al. 2026](https://consensus.app/papers/details/fc5b871ff9c953cda7fe259670b078a0/?utm_source=claude_desktop) (*Academy of Management Annals*) integrates 936 articles on decision-making in private equity and private credit, across economic, social and psychological traditions.

### 4.7 Further relevant papers (one line each)

**Combination**
- [Granger & Ramanathan 1984](https://consensus.app/papers/details/3e86706ecc36575394c4bc77ec2023cb/?utm_source=claude_desktop): adding a constant and not constraining weights to sum to one was best for hog-price forecasts. This is the regression-combination root of the dossier's debias-then-fuse step.
- [Aiolfi et al. 2010](https://consensus.app/papers/details/8759b88bf3e7535585fac2fbc63e5da9/?utm_source=claude_desktop): equal-weighted survey forecasts beat the best model, and averaging survey with model forecasts can add more. This is an obvious baseline for "group forecast plus reference class" [inference].
- [Frazier et al. 2023](https://consensus.app/papers/details/de0c542d2ec75f10a6041f831eda7304/?utm_source=claude_desktop): the puzzle partly reflects low-power, size-distorted tests. More efficient estimation can avoid it.
- [Jore et al. 2010](https://consensus.app/papers/details/09268334457c5309972a9b02bfce3da1/?utm_source=claude_desktop): equal-weight *density* combinations were poorly calibrated under instability; recursive log-score weights were well calibrated. This qualifies "equal weights by default" for densities.

**Credibility and reserving**
- [Saluz 2017](https://consensus.app/papers/details/5521fb87f99552bab24ce3a0b2d42828/?utm_source=claude_desktop): how to estimate the BF development pattern, and its prediction error.

**PE evidence**
- [Cong & Xiao 2021](https://consensus.app/papers/details/c1d3686d429c549e926166219f17e804/?utm_source=claude_desktop): VC persistence can arise without skill differences, with mean reversion in the long run. Another reason to cap the weight on track records.
- [Cohn et al. 2014](https://consensus.app/papers/details/14a9b3cb720c5d85baab98c11e7820b6/?utm_source=claude_desktop): tax-return data show little post-LBO operating improvement, unlike firms with public statements. Underwriting priors built from public-statement samples may be selected [inference].
- [Baik 2022](https://consensus.app/papers/details/04c80fa918545f3a80abe8fe37fc4d91/?utm_source=claude_desktop): low-reputation GPs inflate NAVs during fundraising through both valuation multiples and portfolio-company earnings.

**Debiasing and behaviour**
- [Joos 2019](https://consensus.app/papers/details/1bf1b6f61be451b48989b4b5ae89c9f7/?utm_source=claude_desktop): analysts' "bold" sales-growth forecasts, judged against mean reversion, are more biased. This supports flag F2.
- [Clement & Tse 2005](https://consensus.app/papers/details/ff485ac5aa4657e08af6491caec26122/?utm_source=claude_desktop): bold analyst forecasts are more accurate than herding ones and carry more private information. This counterweights F2: departures from the reference class can be informative [inference].
- [Garland et al. 1990](https://consensus.app/papers/details/e78bffbf2ec6569586348efb5ef9cc00/?utm_source=claude_desktop): petroleum geologists *de*-escalated as dry wells accumulated. Escalation is not universal among experts.

**Scoring**
- [Waghmare & Ziegel 2025](https://consensus.app/papers/details/b9088aab88355d828651b60dbc27f62f/?utm_source=claude_desktop): a recent review of proper scoring rules for estimation and evaluation.
- [Colson & Cooke 2018](https://consensus.app/papers/details/14279feee46f5e57b65b8ebf0f573267/?utm_source=claude_desktop): fewer than one-third of experts in 33 classical-model studies were statistically accurate.

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier recommendation | Challenging evidence | What it implies [inference unless stated] |
|---|---|---|---|
| 1 | Full GLS weights with correlated errors (ρ_fu 0.5, ρ_fa 0.3), estimated from history; "correlation matters" (§2.3, Example 1) | Smith & Wallis 2009 (#1): ignore covariances when estimating weights. Timmermann 2005: simple combinations ignoring correlations often dominate. | Estimate weights with diagonal or shrunk Ω; keep correlation in σ̂². This keeps the dossier's precision point without the estimation-error cost. |
| 2 | Shrink-to-prior weights as the "default weighting" that resolves the puzzle (§3) | Genre et al. 2013 (#4): few schemes beat equal weights after a reality check. Diebold & Shin (cited): discard most, average the rest. Elliott et al. 2026 (#2): gains from optimal weights are small; discard-and-average is the route to large gains. | Show out-of-sample superiority over (a) the simple average of debiased signals, (b) screened averages and (c) the prior alone, before the FBE's weights reach the IC. |
| 3 | Fuse u and f as points, with stated ranges used only for heteroscedasticity (§6.4) | Cooke 2026 (#16): point-forecast errors are fat-tailed, and aggregating points degrades with more and more diverse experts. Cooke et al. 2021: combined distributions beat combined medians. | Elicit and fuse distributions (P10/P50/P90). Treat point-only inputs as low-credibility. |
| 4 | "Proper scoring rules make honest forecasts optimal" (§8); group scorecards and traffic lights (§6.10) | Lichtendahl & Winkler 2007 (#19); Witkowski et al. 2023; Lichtendahl et al. 2013 | Relative-performance displays induce exaggeration. Use joint or shared scoring, avoid rank tables, and adjust F9 for incentive effects. |
| 5 | Cooke performance weights "won in 26 of 33 studies in-sample" (§3) | Colson & Cooke 2017 (#15): in-sample 32 of 33; out-of-sample penalty; 26 of 33 on the out-of-sample index. Lin & Cheng 2009: no out-of-sample dominance. Hemming et al. 2021: use equal weights without relevant seeds. | Correct the text. Weight IC members equally until enough relevant, resolved seeds exist. |
| 6 | PIT i.i.d. U(0,1), binomial coverage and Basel-zone tests (§2.7, §6.7, §6.9) | Knüppel 2015 (#8): multi-step PITs are serially correlated, and standard tests are mis-sized. Verification issue R7 makes the same point about clustering. | Use autocorrelation-robust tests on overlapping multi-year forecasts. Vintage-clustered breach counts. |
| 7 | CRPS skill as a group-scorecard metric (§6.9, §6.10) | Bolin & Wallin 2023 (#9): averaged CRPS overweights high-uncertainty observations. Du 2021: CRPS's preference for the median; always include the log score. | Use SCRPS or standardized scores, plus the log score, reported by strategy. |
| 8 | "Maximize sharpness subject to calibration" (§2.7) | [Mitchell & Wallis 2011](https://consensus.app/papers/details/9e83f7c0da3a5356a20943279716145f/?utm_source=claude_desktop): the example behind the paradigm "has some unrealistic features"; they conclude "there is no need for a subsidiary criterion of sharpness". | A mild challenge. Keep sharpness as a diagnostic, but judge calibration with information-based tests. |
| 9 | β_f ≥ 1 (overreaction) as the default slope (§6.4) | Bordalo et al. 2020 (#10): consensus forecasts underreact. Adam et al. 2025: forecasters are overly anchored to priors. Yee 2026: CG regressions cannot separate persistence from reaction without joint identification. | Group-consensus forecasts may have β_f < 1. Estimate at the level of production and identify jointly. |
| 10 | F5 fundraising-window haircut applied generally (§6.5) | Hüther (#23): no deal-level inflation; a cohort effect instead. Ellis et al. 2011: UK interim valuations were conservative early, with no systematic overvaluation. | Apply F5 to fund NAVs, especially low-reputation GPs (Barber & Yasuda, cited), not to deal marks. Use a deployment-pressure covariate for deals. |
| 11 | "Accuracy did not improve over 30 years" (§4.1); bias parameters implicitly stable | [Hoque et al. 2021](https://consensus.app/papers/details/1255557983a358d78fe898bfb775e93a/?utm_source=claude_desktop) (1,291 road projects): "more recent forecasts were more accurate, and the mean deviation changed direction". [Hoque et al. 2024](https://consensus.app/papers/details/92dad6f56eac5f81831faaf8492b2661/?utm_source=claude_desktop): US transit ridership shortfall fell from about 52% (pre-2000) to about 22% after evaluation tools were introduced. [Välilä 2024](https://consensus.app/papers/details/a4f315f29c655f12a0387bfdbd5aff1f/?utm_source=claude_desktop): welfare destruction is "no foregone conclusion" from the Flyvbjerg database. | Bias is time-varying, and institutional scrutiny can reduce it. Keep α time-varying with decay. Expect ADIC's own scoring to shift α, which makes old calibrations stale. |
| 12 | Reference-class prior as the outside-view anchor (§6.3) | Bärenbold 2023: effectiveness depends on the reference-class definition and is shown mainly for large projects. [Prater et al. 2017](https://consensus.app/papers/details/78f3d24533b153ac98f887bfad927736/?utm_source=claude_desktop): outside engineering, "no experimental and statistically validated research into the effectiveness" of reference-class forecasting. [Cantarelli et al. 2025](https://consensus.app/papers/details/bad34d0cfbea57009bd19d232dd05ca4/?utm_source=claude_desktop): questions remain about validity, applicability and limitations. | The dossier's sensitivity analysis on class choice is essential, not optional. Validate the prior's weight out of sample on ADIC's corpus. |
| 13 | A simple reference-class prior gets 36–60% weight in the worked examples (§6.8) | van Binsbergen et al. 2023 (#12): commonly used linear models do not work out of sample and are inferior to analysts' forecasts. Only well-built ML benchmarks beat analysts. | The prior's weight must be earned. If the reference class is a simple linear model, the FBE may over-shrink good group forecasts. |
| 14 | Stacking of predictive distributions to choose among fusion variants (§2.3, §3) | Ranjan & Gneiting 2010 (#5): linear pools of calibrated forecasts are uncalibrated. | Recalibrate the stacked output (beta-transformed or spread-adjusted pool), or use hierarchical stacking with a post-hoc calibration layer. |

**Missed papers that support the dossier**
- **Shrinkage and constrained weights:** Conflitti et al. 2015 (w ≥ 0 and sum-to-one act as shrinkage); Diebold & Pauly (large shrinkage optimal).
- **Sunk costs and personal responsibility bias the forecast:** Arkes & Blumer (sunk cost inflates estimated success probability); Staw 1976 (escalation is strongest under personal responsibility).
- **Low weight on track records and on "actual":** Braun et al. 2017 (deal-level persistence declined); Cong & Xiao 2021 (persistence without skill).
- **Fusion and outside-view architecture:**
  - [Flyvbjerg 2008](https://consensus.app/papers/details/72e2bbdabffd58deb808abf98cf07d67/?utm_source=claude_desktop): reference-class forecasting in UK planning practice.
  - Bühlmann, Shevchenko & Wüthrich 2007: credibility that fuses internal data, expert opinion and industry data.
  - Gao et al. 2014: fusing analysts' forecasts with market and accounting information gives unbiased growth forecasts.
- **Flag F2:** Joos 2019 (bold forecasts are more biased).

---

## 6. Usage message

None. No Consensus result in this session contained a sign-up, upgrade or usage message.

---

## 7. Search log

**Consensus: topical backfill (14 queries; run first).** The six seeds were run as given or lightly refined.
1. forecast combination puzzle
2. Buhlmann credibility theory experience rating
3. entropy pooling views portfolio
4. optimism bias reference class forecasting
5. private equity interim valuations fundraising bias
6. proper scoring rules calibration expert forecasts
7. combining predictive distributions linear pool uncalibrated recalibration density forecast combination
8. forecast revisions predict forecast errors overreaction individual forecasters underreaction consensus
9. aggregating judgments when forecasters share information correlated errors wisdom of crowds
10. forecasters competing for rank proper scoring rule no longer incentive compatible exaggerate forecasts
11. calibrated probabilistic forecasting ensemble model output statistics minimum CRPS estimation statistical postprocessing
12. classical model structured expert judgment performance-based weights out-of-sample validation calibration informativeness
13. leveraged buyout management projections forecast accuracy realized operating performance versus plan
14. capital market assumptions institutional investors subjective expected returns asset managers predictive accuracy

Backfill queries 1, 4–6, 12 and 14 also confirmed 15 cited works: Claeskens; Smith & Wallis; Wang; Timmermann; Flyvbjerg 2006; Jenkinson–Sousa–Stucke; Barber & Yasuda; Brown–Gredil–Kaplan; Gompers et al.; Gneiting & Raftery; Gneiting et al. 2005; Baron et al.; Blanc & Setzer; Andonov & Rauh; and the source of the Cooke statistic. Query 13 found no study of PE projection accuracy (see the gap note in §1).

**Consensus: citation checks (19 queries)**
15. Bates Granger The Combination of Forecasts Operational Research Quarterly
16. Diebold use of prior information in forecast combination shrinkage toward equal weights egalitarian LASSO survey forecasts
17. Bühlmann Experience Rating and Credibility ASTIN Bulletin 1967
18. Mack credible claims reserves Benktander method Bornhuetter-Ferguson actuary and IBNR
19. Bornhuetter Ferguson The Actuary and IBNR Proceedings of the Casualty Actuarial Society 1972
20. evaluating density forecasts probability integral transform financial risk management; probabilistic forecasts calibration and sharpness
21. Yao Vehtari Simpson Gelman using stacking to average Bayesian predictive distributions
22. Meucci Fully Flexible Views: Theory and Practice entropy pooling
23. skill and luck in private equity performance persistence has persistence persisted buyout venture capital funds
24. private equity net asset values future cash flows reporting bias; nowcasting net asset values private equity state space
25. Ben-David Graham Harvey managerial miscalibration executives confidence intervals stock market forecasts
26. timid choices and bold forecasts inside view; robust analogizing and the outside view private equity investment forecasts
27. Bordalo Gennaioli La Porta Shleifer diagnostic expectations and stock returns long-term earnings growth forecasts
28. Smith Winkler the optimizer's curse skepticism and postdecision surprise in decision analysis
29. Nordhaus forecasting efficiency concepts and applications weak efficiency forecast revisions; Mincer Zarnowitz evaluation of economic forecasts
30. Arkes Blumer the psychology of sunk cost; Staw knee-deep in the big muddy escalating commitment
31. Glahn Lowry the use of model output statistics (MOS) in objective weather forecasting
32. Flyvbjerg Skamris Holm Buhl how (in)accurate are demand forecasts in public works projects transportation
33. Nadauld Sensoy Vorkink Weisbach liquidity cost of private equity investments evidence from secondary market transactions

**WebSearch (2 queries; used only for works Consensus could not return)**
- W1. Nordhaus (1987). EconPapers lists the *REStat* publication (November 1987, 69(4), 667–674) and a 1985 Cowles Foundation discussion paper (No. 774) → https://econpapers.repec.org/RePEc:cwl:cwldpp:774
- W2. Mincer & Zarnowitz (1969), NBER chapter → https://www.nber.org/chapters/c1214.pdf
