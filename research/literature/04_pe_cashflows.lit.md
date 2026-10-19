# Topic 04 literature review: PE cash-flow and NAV modelling, and the DPI decline

**Dossier reviewed:** `research/dossiers/04_pe_cashflows.md` (prepared 18 Oct 2026, 558 lines)
**Prepared:** 18 Oct 2026
**Companion:** `research/verification/04_pe_cashflows.verify.md` (fact-check of the same dossier)
**Tools:** 31 Consensus searches, run one at a time with no filters: 17 citation checks and 14 topical backfill searches. Two WebSearch calls confirmed two works that Consensus could not return. No WebFetch was used.

**Conventions**
- Every paper link is the Consensus URL exactly as returned.
- In the bibliography, authors are listed as Consensus shows them, usually the first author plus "et al." In the integrity table, the dossier's own author lists are kept.
- Citation counts are Consensus counts on 18 Oct 2026. Years are as Consensus shows them. Where Consensus shows an advance-access year or a working-paper year, the entry says so.
- "[inference]" marks our own reasoning. Everything else restates a search result or an abstract.
- **User context (18 Oct 2026).**
  - The Secondaries group is a hybrid of direct and fund investments.
  - Treasury is owned by Corporate Finance, a non-investment function that runs the funding and liability side of the balance sheet.
  - The design notes therefore send liquidity outputs (CFaR, liquidity tiers, crisis sale capacity) to the Corporate Finance / Treasury seat. Secondary-market evidence is read two ways: for the SELL operator, where ADIC is the seller, and for the Secondaries group's LEVER, where ADIC is the buyer.

---

## 1. Summary

### Citation integrity
The dossier cites 38 academic works plus one regulatory text (Basel LCR40). We checked 31 of them, including every work the design layer (§6 of the dossier) depends on.

| Outcome | Count | Detail |
|---|---|---|
| Found, metadata matches | 25 | Eight of these are indexed only as working-paper or SSRN records, or show an advance-access year. See the table in §2. |
| Mismatched | 4 | (1) **Luxenberg et al.** was published in the ACM ICAIF '22 proceedings, DOI 10.1145/3533271.3561769, so it is not only an arXiv preprint. (2) **Sorensen, Wang & Yang** is in *RFS* 27(7), pp. 1977–2021, not 27(2); the issue and pages come from the verification log. (3) **Nadauld et al.** is superseded by *JFE* 2019, DOI 10.1016/j.jfineco.2018.11.007, and the published seller PME is 0.976, not 0.974. (4) **Jeet et al. (2026)**: the published title wording differs, and the DOI 10.3905/jpmi.2026.1.010 should be added. |
| Not found in Consensus | 2 | Ljungqvist & Richardson (2003, NBER WP 9454) and Getmansky, Lo & Makarov (2004, *JFE*). WebSearch confirms that both exist with the dossier's metadata. |

- **No citation was fabricated.**
- **One correction to the companion verification log.** The log calls Luxenberg et al. "preprint only". Consensus indexes the ICAIF '22 proceedings version.
- **Three items the dossier marked "not verified" (§8) are now resolved:**
  - The "MSCI/Jeet market-sensitive periodic growth" model is Jeet (2020), an SSRN working paper.
  - de Malherbe's model is indexed as de Malherbe (2007). It is a four-factor model, and one of its factors is the reliability of reported values.
  - "Tausch et al." is Tausch et al. (2022), *Journal of Risk*.

### Backfill: what the dossier misses
We ran 14 topical searches. The most important gaps:

1. **Published precedent for factor-driven Takahashi–Alexander (TA).**
   - Cao et al. (2025, *FAJ*) add systematic factors and fund-specific randomness to TA call and distribution rates.
   - Beutler et al. (2023, *JPM*) run TA as a historical simulation that produces a range of outcomes.
   - The dossier says practitioner TA "usually" lacks dispersion and market dependence. That framing is now dated. What is genuinely new in RFT-TA is the regime layer, the effective-age clock, the smoothing filter and the action operators [inference].
2. **A paper written for the TPA setting.** Jeet et al. (2026) argue that cash-flow models must drive commitment pacing, liquidity management and allocation sizing, and that factor models belong to the liquid sleeve, direct investments and attribution.
3. **Literature on how reliable NAVs are**, none of it cited:
   - Jenkinson et al. (2013), on CalPERS fund valuations;
   - Jenkinson et al. (*The Accounting Review*), comparing NAVs with discounted realised cash flows;
   - Barber & Yasuda (2017);
   - Brown, Gredil & Kaplan (2019);
   - Hüther (*JFQA*).

   Together these let the mark-gap state be calibrated by strategy, fund age and GP fundraising status.
4. **Exit modelling.**
   - Competing-risks exit hazards rise and then fall rather than rising steadily (Giot & Schwienbacher 2007).
   - Debt and equity markets open and close exit windows (Jenkinson & Sousa 2015).
   - After an IPO, GPs hold their stakes for about three years on average (Jenkinson et al. 2025, *Management Science*).
5. **Commitment timing.** Timing new commitments yields modest gains at best, because LPs cannot time calls or exits (Brown et al. 2020, *JFE*).
6. **Secondary-market liquidity.**
   - Discounts track the supply of liquidity, not future NAV returns (Albuquerque et al. 2018).
   - Volume collapsed in early 2009 (Hege et al. 2011).
   - Fund-level traits drive how liquid an interest is (Kleymenova et al. 2012).
7. **Risk and alpha.**
   - Evidence from secondary prices and listed vehicles points to lower alpha and higher beta than cash-flow and NAV measures show (Boyer et al. 2021; Ennis et al. 2026).
   - A fund-level α that is less noisy than PME is available (Korteweg et al. 2024, *RFS*).
8. **The actuarial transfer.**
   - Our search found no paper that applies chain-ladder reserving to PE cash flows, so the dossier's idea appears new.
   - The actuarial toolkit it needs already exists: credibility chain ladder (Gisler & Wüthrich 2008), correlated triangles (Braun 2004), and age–period–cohort development models (Pittarello et al.).
9. **The 2022–26 drought itself.**
   - Three targeted searches found no peer-reviewed study of the drought.
   - The academic support is indirect: monetary tightening and financial conditions affect exit valuations (Simlai 2025), and exit windows depend on market conditions (Jenkinson & Sousa 2015).
   - The dossier therefore has to rely on practitioner data for the drought calibration.

### Challenges to the dossier (detail in §5)
- **Commitment pacing as a lever:** Brown et al. (2020).
- **Net-alpha prior and buyout beta:** Boyer et al. (2021); Ennis et al. (2026). Break-even alpha is also model-dependent: about 7% in Buchner et al. (2015, working paper) against 3.08% in Sorensen, Wang & Yang.
- **IPO sell-down over 4–8 quarters:** Jenkinson et al. (2025); Dong et al. (2020).
- **Uncertainty about forward alpha that shrinks with fund age:** Brown et al. (2020, "Evolution").
- **A constant smoothing parameter λ:** Cho et al. (2014); Bollen & Pool (2008).
- **Crisis SELL modelled through price alone:** Hege et al. (2011).
- **Crisis call multiplier of 0.8:** Robinson & Sensoy (2010, working paper); Bernstein et al. (2017).
- **The "75% of exits above the prior mark" calibration** is conditional on strategy and age: Jenkinson et al. (2013; *TAR*); Driessen et al.; Phalippou & Gottschalg. This supports verification issue R4.

**Usage message:** none appeared in any Consensus result.

---

## 2. Citation-integrity table (31 checked)

| # | Dossier citation | Status | Corrected metadata / note | Consensus URL |
|---|---|---|---|---|
| 1 | Takahashi & Alexander (2002), *JPM* 28(2), 90–100 | found | 2002, 68 cit., DOI 10.3905/jpm.2002.319836. Venue shown as "Unknown Journal"; the DOI is *JPM*. | https://consensus.app/papers/details/da7ee2d8587e575f99e3a36a590d2be6/?utm_source=claude_desktop |
| 2 | Buchner, Kaserer & Wagner (2010), *JAI* 13(1), 41–54; WP 2006 | found | 2010, *JAI*, 11 cit., DOI 10.3905/jai.2010.13.1.041. The *JAI* abstract models distributions as an arithmetic Brownian motion with time-dependent drift. The 2006 WP, with lognormal distributions, has its own record: "Stochastic Modeling of Private Equity – An Equilibrium Based Approach to Fund Valuation" (2006, 5 cit., https://consensus.app/papers/details/6dab83afa3435997830b95f79d64ff75/?utm_source=claude_desktop). The dossier's descriptions fit both. | https://consensus.app/papers/details/0c7ff969c8d35cf6b99fbc57dac1b715/?utm_source=claude_desktop |
| 3 | Luxenberg, Boyd, Kochenderfer, van Beek, Cao, Diamond, Ulitsky, Menda & Vairavamurthy (2022), arXiv:2207.07767 | **mismatched (venue)** | Published in the *Proceedings of the Third ACM International Conference on AI in Finance* (ICAIF '22), 2022, DOI 10.1145/3533271.3561769, 4 cit. Cite the proceedings version. The abstract confirms the random linear system, the convex MPC and that "we focus on the growth problem, with no external liabilities or income". | https://consensus.app/papers/details/e63add9e25485ea691994d7731b433b1/?utm_source=claude_desktop |
| 4 | Jeet, V., et al. (2026), "A Crucial Enhancement to the Takahashi and Alexander's Cash Flow Model", *JPMI* 24(3) | **mismatched (minor: title)** | Published title: "A Crucial Enhancement to the Takahashi–Alexander Cash Flow Model", 2026, DOI 10.3905/jpmi.2026.1.010, 0 cit. The dossier's wording matches the SSRN precursors: Jeet (2024), "Enhancement to the Takahashi and Alexander's Cash Flow Model", DOI 10.2139/ssrn.4803317 (https://consensus.app/papers/details/09a316c73ea25406ba665dd2e6b61687/?utm_source=claude_desktop), and "Further Enhancement…", DOI 10.2139/ssrn.4819761 (https://consensus.app/papers/details/e289ee8056fd5a3e8ee9871d2ede108b/?utm_source=claude_desktop). Add the DOI. | https://consensus.app/papers/details/544adcd5b0c45e76b96dedc6b316f6c2/?utm_source=claude_desktop |
| 5 | Brown, Ghysels & Gredil (2023), *RFS* 36(3), 945–986 | found (WP record) | Consensus returns only the SSRN version: 2020, 20 cit., DOI 10.2139/ssrn.3507873. Its abstract gives beta "around 1.0 (1.4)" and total risk "33% (40%)", matching the figures the dossier attributes to the published abstract. The verification log confirmed the *RFS* version. | https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop |
| 6 | Robinson & Sensoy (2016), *JFE* 122(3), 521–543 | found | 203 cit., DOI 10.1016/j.jfineco.2016.09.008. Consensus shows no abstract. An earlier working paper by the same authors is indexed separately (see §4.7). | https://consensus.app/papers/details/86bf821b6ba65861a9da20fed7862965/?utm_source=claude_desktop |
| 7 | Ljungqvist & Richardson (2003), NBER WP 9454 | **not found in Consensus; exists (web-verified)** | Two queries returned only the companion paper "The Investment Behavior of Private Equity Fund Managers" (2003, 174 cit., DOI 10.2139/ssrn.482546, https://consensus.app/papers/details/73f51017cd3a5ba6a31787fa143032f1/?utm_source=claude_desktop). WebSearch confirms NBER WP w9454 (RePEc: https://ideas.repec.org/p/nbr/nberwo/9454.html) and an NYU Stern WP version dated January 2003. The dossier's metadata are consistent. | none |
| 8 | Gourier, Phalippou & Westerfield (2024), *JF* 79(5), 3407–3457 | found (SSRN record) | The record shows "SSRN Electronic Journal", 2024, 8 cit., DOI 10.2139/ssrn.2490430; the *JF* DOI is not shown. The abstract confirms every content claim: under-allocation; a larger premium to adjust the quantity committed than to remove timing uncertainty or limited tradability; premia that rise with secondary liquidity and persist across many funds. | https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop |
| 9 | Giommetti & Sørensen (2021), WP, SSRN 3761243 | found | 2021, 5 cit., DOI 10.2139/ssrn.3761243. The abstract says the LP "repeatedly commits capital to PE funds", that allocations are "not monotonically declining in risk aversion", and that the model has a secondary-market extension. | https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop |
| 10 | Ang, Papanikolaou & Westerfield (2014), *Mgmt Sci* 60(11) | found | 171 cit., DOI 10.1287/mnsc.2014.1986. | https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop |
| 11 | Sorensen, Wang & Yang (2014), *RFS* 27(2) | **mismatched (issue/pages)** | Consensus: *RFS*, DOI 10.1093/rfs/hhu013, 110 cit., dated 2013 (advance access). The verification log, from the NBER page, gives ***RFS* 27(7), 1977–2021**. Correct the issue number and add the pages. | https://consensus.app/papers/details/15cb135a45b35616b82e97bf090f24ae/?utm_source=claude_desktop |
| 12 | Dimmock, Wang & Yang (2024), *Mgmt Sci* 70(3), 1554–1579 | found | The record is dated 2019 and carries the NBER DOI 10.3386/w25559; the venue is *Mgmt Sci* and the abstract cites DOI 10.1287/mnsc.2023.4759. 25 cit. | https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop |
| 13 | Geltner (1991), *JREFE* 4(3) | found | 391 cit., DOI 10.1007/bf00161933. | https://consensus.app/papers/details/fa03b920e943538884c1f281325a576b/?utm_source=claude_desktop |
| 14 | Getmansky, Lo & Makarov (2004), *JFE* 74(3), 529–609 | **not found in Consensus; exists (web-verified)** | Two queries returned only Getmansky's 2004 thesis, which carries the same abstract (https://consensus.app/papers/details/4e43d079332f5046860f2f39350f56f9/?utm_source=claude_desktop), plus papers that cite GLM. WebSearch confirms *JFE* 74(3), 529–609, DOI 10.1016/j.jfineco.2004.04.001, and NBER WP 9571 (https://www.nber.org/papers/w9571). The dossier's metadata are correct. | none |
| 15 | Couts, Gonçalves & Rossi (2024), *RFS* 37(7) | found (WP record) | SSRN 2020, 14 cit., DOI 10.2139/ssrn.3544854. The abstract confirms a common source of spurious autocorrelation and a lower average alpha for illiquid funds. | https://consensus.app/papers/details/38f7d68ab4a759ecb109c8dfcba5597d/?utm_source=claude_desktop |
| 16 | Kaplan & Schoar (2005), *JF* 60(4) | found | *JF*, 366 cit. Consensus shows the SSRN DOI 10.2139/ssrn.473341. | https://consensus.app/papers/details/3eb9b802f17153de8190c3e72ac28aed/?utm_source=claude_desktop |
| 17 | Korteweg & Nagel (2016), *JF* 71(3) | found (WP record) | NBER/SSRN 2015, 134 cit., DOI 10.2139/ssrn.2309596. The abstract confirms that VC fund abnormal returns are "close to zero" and that systematic payoffs resemble selling index puts. | https://consensus.app/papers/details/38b28ae37b555f3087e387f515331a0f/?utm_source=claude_desktop |
| 18 | Gredil, Griffiths & Stucke (2023), *JCF* 81, 102360 | found (WP draft only) | Only the 2014 first draft is indexed (42 cit., no DOI). The *JCF* record was not returned; the verification log confirmed it through Crossref. | https://consensus.app/papers/details/391cace55063580f9b81031f13ef5aee/?utm_source=claude_desktop |
| 19 | Gupta & Van Nieuwerburgh (2021), *JF* 76(6) | found | 24 cit., DOI 10.1111/jofi.13073. | https://consensus.app/papers/details/a07fbcfb0fdd5d5891ce4d67340cbeb8/?utm_source=claude_desktop |
| 20 | Driessen, Lin & Phalippou (2012), *JFQA* 47(3) | found | 124 cit., DOI 10.1017/s0022109012000221. The abstract adds that self-reported NAVs "significantly overstate fund values for mature and inactive funds". | https://consensus.app/papers/details/b5ef57e8c67457f39a784f755550d51a/?utm_source=claude_desktop |
| 21 | Ang, Chen, Goetzmann & Phalippou (2018), *JF* 73(4) | found | *JF*, 142 cit. The record is dated 2014 and carries the SSRN DOI 10.2139/ssrn.2356553. | https://consensus.app/papers/details/f0d68e17b4ce5f69b3724f06e4078dc2/?utm_source=claude_desktop |
| 22 | Nadauld, Sensoy, Vorkink & Weisbach (2016), NBER WP 22404 | **mismatched (superseded; figure)** | Published as "The liquidity cost of private equity investments: Evidence from secondary market transactions", *JFE*, 2019, DOI 10.1016/j.jfineco.2018.11.007, 66 cit. The published abstract gives buyers' PME 1.023 against **sellers' 0.976**; the dossier's 0.974 comes from the WP. The gap is still about 5pp a year. Cite the *JFE* version. | https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop |
| 23 | Hayes, Primbs & Chiquoine (2015), *JPM* 41(2) | found | 9 cit., DOI 10.3905/jpm.2015.41.2.033. | https://consensus.app/papers/details/8de41b199daf5479889844ffcbd866e6/?utm_source=claude_desktop |
| 24 | Nevins, Conner & McIntire (2004), *JAI* 6(4) | found | 14 cit., DOI 10.3905/jai.2004.391062. | https://consensus.app/papers/details/3e6cf885868b515eb681d05ea4ffa665/?utm_source=claude_desktop |
| 25 | Karatas, Klinkert & Hirsa (2021), arXiv:2108.02853 | found | 2 cit., DOI 10.48550/arxiv.2108.02853. | https://consensus.app/papers/details/9d8b4ed0f74e55bb9563bee22abf44a7/?utm_source=claude_desktop |
| 26 | Bühlmann (1967), *ASTIN Bulletin* 4(3) | found | 67 cit. No DOI is shown, and the author name is garbled in the record. | https://consensus.app/papers/details/5542fe373291540f857447d36cf464a8/?utm_source=claude_desktop |
| 27 | Harris, Jenkinson & Kaplan (2014), *JF* 69(5) | found | 537 cit., DOI 10.1111/jofi.12154. | https://consensus.app/papers/details/db976ea21cdc505480145e648346890d/?utm_source=claude_desktop |
| 28 | Franzoni, Nowak & Phalippou (2012), *JF* 67(6) | found | 251 cit., DOI 10.1111/j.1540-6261.2012.01788.x. | https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop |
| 29 | Jegadeesh, Kräussl & Pollet (2015), *RFS* 28(12) | found | 88 cit., DOI 10.1093/rfs/hhv046. | https://consensus.app/papers/details/0e0c66f44a5d50b99383e02fcaf6e5a0/?utm_source=claude_desktop |
| 30 | Korteweg & Sorensen (2010), *RFS* 23(10) | found | *RFS*, 216 cit. Consensus shows the SSRN DOI 10.2139/ssrn.1108610. | https://consensus.app/papers/details/e504307dedfa551190d5d5dc752d6636/?utm_source=claude_desktop |
| 31 | Phalippou & Gottschalg (2009), *RFS* 22(4) | found | 507 cit., DOI 10.1093/rfs/hhn014, dated 2008 (advance access). | https://consensus.app/papers/details/724f1392076c53649afdf46637dce8b4/?utm_source=claude_desktop |

**Not checked (7):** Geltner (1993), Metrick & Yasuda (2010), Axelson et al. (2013), Kaplan & Strömberg (2009), Siegel (2008), Mack (1993) and England & Verrall (2002).
- None of these drives an equation.
- Metrick & Yasuda matters for the fee fix the verification log proposes (R1). Check it before that fix is coded.
- Basel LCR40 is regulatory, not academic.

### Dossier §8 "not verified" items, now resolved

| Dossier item | What Consensus returned | Consensus URL |
|---|---|---|
| "MSCI/Jeet market-sensitive periodic growth" model | Jeet, V. (2020), "Modeling Private Investment Cash Flows With Market Sensitive Periodic Growth", SSRN, DOI 10.2139/ssrn.3775008, 1 cit. | https://consensus.app/papers/details/19f6b1a1e177534a8ffc2f0eea7cb9e5/?utm_source=claude_desktop |
| de Malherbe, beyond BKW's description | de Malherbe, E. (2007), "Towards a Stochastic Cash Flow Model for Private Equity Funds". A four-factor model of drawdowns, investment performance, payback and "how reliable are the fund intermediary values reported by the manager". 0 cit. The 2004 version cited by BKW was not returned. | https://consensus.app/papers/details/6bf2e247016e532ca0285194c8bcce47/?utm_source=claude_desktop |
| "Tausch et al." (named in the dossier with no reference) | Tausch, C., et al. (2022), "Modeling the exit cashflows of private equity fund investments", *Journal of Risk*, DOI 10.21314/jor.2022.029, 2 cit. | https://consensus.app/papers/details/06a53f89abd05350ae89e3e77c5fc5e6/?utm_source=claude_desktop |

---

## 3. Annotated bibliography (25 papers)

Tags:
- **[cited]**: the dossier cites the paper.
- **[missed]**: the dossier does not cite it.
- **[challenge]**: the paper contradicts or qualifies a dossier claim.

### A. Cash-flow engines

**1. [A Latent Factor Cash Flow Model for Alternative Investment Funds](https://consensus.app/papers/details/bb74f63a8fc15983a1e7753d4057d4f0/?utm_source=claude_desktop)** [missed]
- Wenbo Cao et al. · 2025 · *Financial Analysts Journal* · 1 cit. · DOI 10.1080/0015198x.2025.2489923
- **Finding.**
  - The model builds on TA. It adds systematic economic factors and fund-specific randomness to call and distribution rates, and uses a factor-based PME for growth.
  - This ties cash flows to macroeconomic conditions, for scenario analysis, stress testing, commitment design and multi-asset risk management.
  - A 2026 paper describes it as adding latent factors and heavy-tailed idiosyncratic terms to TA ([Feng 2026](https://consensus.app/papers/details/a6ba45ba559453a78fe55e3f03919cff/?utm_source=claude_desktop)).
- **Relevance.**
  - This is the closest published precedent for the RFT-TA call and distribution intensities (E5, E6) and for factor growth (E2).
  - Feng attributes the model to Cao and van Beek, who are both co-authors of Luxenberg et al.
  - Use it as the benchmark RFT-TA must beat out of sample [inference].

**2. [Modeling the Cash Flow Dynamics of Private Equity Funds: Theory and Empirical Evidence](https://consensus.app/papers/details/0c7ff969c8d35cf6b99fbc57dac1b715/?utm_source=claude_desktop)** [cited]
- A. Buchner et al. · 2010 · *The Journal of Alternative Investments* · 11 cit. · DOI 10.3905/jai.2010.13.1.041
- **Finding.**
  - The drawdown rate follows a mean-reverting square-root process. Distributions follow an arithmetic Brownian motion with time-dependent drift.
  - Calibrated by conditional least squares on mature European funds, the model explains up to 99.6% of the variation in average cumulated net cash flows.
- **Relevance.** The dossier is right to use this as a benchmark. The fit is to average cumulated flows, not to dispersion or dependence on market state, so it cannot replace a state-dependent engine [inference].

**3. [Takahashi–Alexander Revisited: Modeling Private Equity Portfolio Outcomes Using Historical Simulations](https://consensus.app/papers/details/be3095d7eb5f506bad9e4cc2743d1096/?utm_source=claude_desktop)** [missed; challenge]
- Dawson Beutler et al. · 2023 · venue not shown (DOI is *JPM*) · 1 cit. · DOI 10.3905/jpm.2023.1.496
- **Finding.**
  - Deterministic TA is sensitive to its assumptions and gives no range of outcomes, which can make investors overconfident.
  - A historical-simulation version built on realised PE cash flows needs no user assumptions and produces a range of outcomes.
- **Relevance.**
  - This is a cheap, assumption-light challenger model the IC can see beside RFT-TA [inference].
  - It also contradicts the dossier's §5 claim that practitioner TA lacks dispersion.

**4. [Strategic Asset Allocation with Illiquid Alternatives](https://consensus.app/papers/details/e63add9e25485ea691994d7731b433b1/?utm_source=claude_desktop)** [cited; venue corrected]
- Eric Luxenberg et al. · 2022 · *Proceedings of the Third ACM International Conference on AI in Finance* · 4 cit. · DOI 10.1145/3533271.3561769
- **Finding.**
  - Illiquid dynamics are written as a random linear system, and a convex MPC policy allocates liquid assets and sets new commitments.
  - Performance is "surprisingly close" to a fictional fully liquid setting.
  - The paper solves the growth problem with "no external liabilities or income".
- **Relevance.** This is E10's linearised dynamics. ADIC pays out 5–10% a year, so results transfer only after that extension is built (consistent with verification issue R16) [inference].

**5. [The Emperor Has No Cash Flows: Integrating Cash Flow Dynamics into Total Portfolio Approach](https://consensus.app/papers/details/3efa59a891125d279f6eb98f81b48d52/?utm_source=claude_desktop)** [missed]
- Vishv Jeet et al. · 2026 · venue not shown (DOI is *JPMI*) · 0 cit. · DOI 10.3905/jpmi.2026.003
- **Finding.**
  - Factor models measure NAV volatility and factor exposures. They do not measure capital risk (permanent loss over a fund's life) or funding liquidity risk (capital calls relative to liquid reserves), and both are orthogonal to factor exposures.
  - Cash-flow models must therefore drive commitment pacing, liquidity management and allocation sizing.
  - Factor models keep a role in the liquid sleeve, direct investments and performance attribution.
- **Relevance.**
  - The paper addresses TPA, ADIC's stated architecture, directly.
  - It supports a formal division of labour: Tier-1 liquidity gates run on cash-flow paths, while factor risk serves the liquid sleeve, co-investments and attribution [inference].
  - Funding liquidity risk is a Corporate Finance / Treasury metric.

### B. Exits, inventory and holding periods

**6. [IPOs, trade sales and liquidations: Modelling venture capital exits using survival analysis](https://consensus.app/papers/details/1e054ead96575c55952157435b5a7763/?utm_source=claude_desktop)** [missed]
- P. Giot et al. · 2007 · *Journal of Banking and Finance* · 323 cit. · DOI 10.2139/ssrn.461840
- **Finding.**
  - Competing-risks models are fitted to time to IPO, trade sale and liquidation for about 6,000 VC-backed firms (more than 20,000 rounds).
  - The conditional IPO probability is non-monotone: it rises, plateaus, then falls for firms that have not yet exited.
- **Relevance.**
  - This is the method for the dossier's exit-hazard class (co-investments, direct secondaries, look-through holdings).
  - It is evidence that the exit hazard of residual inventory falls with age. That is the mechanism behind the adverse-selection drift in q, and a reason the TA bow should not push distribution rates mechanically upward as funds age [inference].

**7. [What determines the exit decision for leveraged buyouts](https://consensus.app/papers/details/b00a0c697037509298b77f023b42f307/?utm_source=claude_desktop)** [missed]
- Tim Jenkinson et al. · 2015 · *Journal of Banking and Finance* · 69 cit. · DOI 10.1016/j.jbankfin.2015.06.007
- **Finding.**
  - In 1,022 European PE exits, more than 43% were sales to other PE funds.
  - Debt-market and equity-market conditions strongly influence the exit route.
  - Funds exploit "windows of opportunity", and the value-maximising route varies with market conditions.
- **Relevance.** This is academic support for loading E1's exit-window factor on both debt and equity markets, and for giving each exit route (IPO, trade sale, secondary buyout) its own sensitivity [inference].

**8. [Long Goodbyes: How Do Private Equity Funds Manage Sell-Downs After Initial Public Offerings?](https://consensus.app/papers/details/f7b88f404c7d560a934abcfbc53a9c0d/?utm_source=claude_desktop)** [missed; challenge]
- T. Jenkinson et al. · 2025 · *Management Science* · 0 cit. · DOI 10.1287/mnsc.2022.02043
- **Finding.**
  - GPs hold post-IPO stakes for three years on average, although lockups expire after six months.
  - There is no evidence that the timing of sell-downs adds value, and GPs appear reluctant to sell losers.
  - Long goodbyes are more likely when the fund is performing well, which raises payments to GPs.
- **Relevance.** E6 stages IPO exits over 4–8 quarters. This evidence implies about 12 quarters on average, and longer for losers [inference]. That slows DPI from any reopened IPO window.

**9. [Modeling the exit cashflows of private equity fund investments](https://consensus.app/papers/details/06a53f89abd05350ae89e3e77c5fc5e6/?utm_source=claude_desktop)** [missed; the dossier names "Tausch et al." without a reference]
- Christian Tausch et al. · 2022 · *Journal of Risk* · 2 cit. · DOI 10.21314/jor.2022.029
- **Finding.**
  - A joint deal-level model covers exit timing, built for interval-censored data, and the exit multiple, built for the high number of defaults.
  - It is estimated by maximum likelihood on buyout and VC data and used in Monte Carlo risk management.
- **Relevance.** This is a ready specification for the asset-level engine of the Co-investment group and of the direct book within the Secondaries group: time to exit and multiple drawn jointly, with zero inflation [inference].

**10. [The Evolution of Private Equity Fund Value](https://consensus.app/papers/details/86f58dd5a5655117a6f2b36792e3eabd/?utm_source=claude_desktop)** [missed; challenge]
- Gregory W. Brown et al. · 2020 · venue not shown (SSRN DOI) · 2 cit. · DOI 10.2139/ssrn.3621407
- **Finding.**
  - Across 1,400 mature buyout and VC funds, future returns fall off once funds are about 7–8 years old.
  - Contrary to common wisdom, dispersion in future IRR and direct alpha *increases* for funds older than five years.
  - Predictors of future returns include distributions to date, dry powder, the prior fund's performance, fund size, GP fundraising, prior public-market returns and credit spreads. High dry powder hurts young funds and helps older ones.
- **Relevance.**
  - The dossier's alpha runway rests on Bain. This paper gives it academic support, keyed to calendar age (consistent with verification issue R2) [inference].
  - It contradicts E3's assumption that uncertainty about forward alpha shrinks with age (see §5).
  - It supplies covariates for E3 and for the exit factor X_t.

### C. NAV, smoothing and mark reliability

**11. [Nowcasting Net Asset Values: The Case of Private Equity](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop)** [cited]
- Gregory W. Brown et al. · 2020 (SSRN record of the 2023 *RFS* paper) · 20 cit. · DOI 10.2139/ssrn.3507873
- **Finding.**
  - Weekly unsmoothed NAVs for individual funds beat extrapolations of reported NAVs.
  - The average buyout (VC) beta is about 1.0 (1.4), and total risk is 33% (40%) a year.
  - Risk and return vary over time and across funds. Risk-taking and reporting quality persist by manager.
- **Relevance.** This is the core of E2 and E7. Persistent reporting quality by manager supports a manager-level mark-quality parameter in the hierarchical pooling of dossier §6.7 [inference].

**12. [How Fair are the Valuations of Private Equity Funds](https://consensus.app/papers/details/e297da1e0d0658d8ae2ca7a7a7b6987c/?utm_source=claude_desktop)** [missed]
- Tim Jenkinson et al. · 2013 · venue not shown (SSRN DOI) · 88 cit. · DOI 10.2139/ssrn.2229547
- **Finding.** The paper uses the full history of 761 CalPERS fund investments.
  - Over a fund's life, valuations are conservative and smoothed. On average they understate subsequent distributions by about 35%.
  - Valuations jump in the fourth quarter, when funds are audited.
  - Valuations are inflated while follow-on funds are being raised, then gradually reverse.
  - Performance reported during fundraising predicts final returns poorly, especially IRR. PME measures predict better.
- **Relevance.**
  - Calibrate E7's mark gap by fund stage and fundraising status.
  - Feed E3's actual-to-date input with PME or direct alpha, not IRR.
  - The fourth-quarter jump makes reported NAV seasonal, which matters for the payout and payout-coverage calendar [inference].

**13. [Private Equity Net Asset Values and Future Cash Flows](https://consensus.app/papers/details/44d91cea6b8b53b481621e6ed4e6ef9e/?utm_source=claude_desktop)** [missed]
- Tim Jenkinson et al. · 2019 (per Consensus) · *The Accounting Review* · 31 cit. · DOI 10.2308/accr-52486
- **Finding.**
  - The paper compares reported NAVs with the discounted value of realised cash flows for 384 VC and 195 buyout funds (1988–2016).
  - Buyout NAVs show little systematic bias. VC NAVs are relatively aggressive, especially since 2000.
- **Relevance.**
  - This gives a strategy-specific prior for the mark gap G = ln N − ln V: near zero for buyout, and negative for VC, where reported NAV sits above economic value [inference].
  - It bears on the dossier's "AI-bifurcation" scenario, in which VC and growth marks rise.

**14. [Interim Fund Performance and Fundraising in Private Equity](https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop)** [missed]
- Brad M. Barber et al. · 2017 · *Journal of Financial Economics* · 113 cit. · DOI 10.1016/j.jfineco.2017.01.001
- **Finding.**
  - Interim performance has large effects on fundraising, especially when backed by exits and for low-reputation GPs.
  - GPs time fundraising to coincide with performance peaks, through exits and through NAV management.
  - Low-reputation GPs with low realisation rates show peaks followed by erosion after fundraising.
- **Relevance.** Haircut marks (E7) and the actual-to-date signal (E3) when a GP is fundraising and realisation is low. The realisation ratio ρ, which E3 already uses, is the right conditioning variable [inference].

### D. Performance measurement and the alpha prior

**15. [Discount Rate Risk in Private Equity: Evidence from Secondary Market Transactions](https://consensus.app/papers/details/d9f67be2c83856ea8703fcd0bfeb3f57/?utm_source=claude_desktop)** [missed; challenge]
- Brian H. Boyer et al. · 2021 · *SSRN Electronic Journal* (NBER WP) · 4 cit. · DOI 10.2139/ssrn.3823332
- **Finding.**
  - An index built from secondary transaction prices shows that PE discount rates vary considerably.
  - The index's standard alpha is zero, while cash-flow-based performance measures for the same funds are large and positive.
  - Ignoring the variation in discount rates misallocates capital.
- **Relevance.**
  - This challenges two dossier choices: PME or direct alpha as an unbiased actual-to-date alpha signal in E3, and the prior of 0 to +2% net alpha (see §5).
  - Secondary prices, which the Secondaries group observes, give a market-based state variable for the discount rate [inference].

**16. [Buyout Performance with Assets Valued at Market](https://consensus.app/papers/details/3acac11a0e225ab8b04a38002b7e440d/?utm_source=claude_desktop)** [missed; challenge]
- Richard M. Ennis et al. · 2026 · venue not shown (DOI is *JPMI*) · 0 cit. · DOI 10.3905/jpmi.2026.011
- **Finding.**
  - For listed PE on European exchanges, volatility and stock-market correlation are higher when measured with market prices than with cash flows and NAVs.
  - Beta is about 1.5 and there is no statistically meaningful alpha. The authors say this aligns with secondary-market studies.
- **Relevance.** This challenges the dossier's buyout beta of 1.05–1.25 and its alpha prior. At minimum, add a beta-1.5 sensitivity to E2 [inference].

**17. [Risk-Adjusted Returns of Private Equity Funds: A New Approach](https://consensus.app/papers/details/d7fa0f4765285b498d96677eb55bdff5/?utm_source=claude_desktop)** [missed]
- Arthur Korteweg et al. · 2024 · *The Review of Financial Studies* · 6 cit. · DOI 10.1093/rfs/hhae067
- **Finding.**
  - A new fund-level α is much less sensitive to cash-flow noise than PME or GPME, with the same aggregate pricing implications as GPME.
  - Its cross-fund standard deviation is much lower, and it improves prediction of future funds' performance.
- **Relevance.** Measuring the actual-to-date signal y^A in E3 with this α lowers its noise τ_A. It is also a better basis for estimating credibility by manager and by group [inference].

**18. [Has Persistence Persisted in Private Equity? Evidence from Buyout and Venture Capital Funds](https://consensus.app/papers/details/c9d05f78edee5236895cb0968f1c5e62/?utm_source=claude_desktop)** [missed]
- Robert S. Harris et al. · 2020 · *SSRN Electronic Journal* (NBER) · 109 cit. · DOI 10.3386/w28109
- **Finding.**
  - On Burgiss data, persistence before 2000 is confirmed.
  - After 2000 there is little persistence for buyout funds, except at the lower end of the distribution. VC persistence remains.
- **Relevance.**
  - E3 gives interim performance a unit loading on forward alpha, which is too high for buyout (verification issue R7).
  - Use strategy-specific loadings: near zero for buyout plus a bottom-quartile penalty, and higher for VC [inference].

### E. Commitments, pacing and liquidity

**19. [Can investors time their exposure to private equity?](https://consensus.app/papers/details/b5880343ab7b57ebaf68b353dfff48da/?utm_source=claude_desktop)** [missed; challenge]
- Gregory W. Brown et al. · 2020 · *Journal of Financial Economics* · 30 cit. · DOI 10.1016/j.jfineco.2020.08.014
- **Finding.**
  - PE performance is cyclical: high fundraising is followed by low performance.
  - Realistic strategies that time commitments still gain modestly at best, because investors can time commitments but not calls or exits.
  - Net cash flows are highly correlated over time, even across very different commitment strategies.
- **Relevance.**
  - This tempers the value of LEVER through new commitments, both for performance and for near-term liquidity.
  - It supports the dossier's inference that the systematic exit state dominates portfolio cash flows [inference].

**20. [Capital Commitment](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop)** [cited]
- Elise Gourier et al. · 2024 · SSRN record (published in *JF*) · 8 cit. · DOI 10.2139/ssrn.2490430
- **Finding.**
  - Ex-ante commitment has large effects on portfolios and welfare, and investors are under-allocated to private-market funds.
  - Investors would pay more to adjust the quantity committed than to remove timing uncertainty or limited tradability.
  - Commitment risk premia rise with secondary-market liquidity and do not disappear across many funds.
- **Relevance.** This supports treating the quantity committed as E10's key decision variable, and pricing the commitment friction explicitly rather than ignoring it [inference].

**21. [Private Equity Recommitment Strategies for Institutional Investors](https://consensus.app/papers/details/63deabfca2f15e65880fa9a8f5d03a13/?utm_source=claude_desktop)** [missed]
- G. D. de Zwart et al. · 2012 · *Financial Analysts Journal* · 13 cit. · DOI 10.2469/faj.v68.n3.1
- **Finding.**
  - New commitments equal distributions received plus uncalled capital from old commitments, scaled by the ratio of target to current allocation.
  - In historical simulations on 1980–2005 data, the rule reaches 86% of target, with an 8% probability of being over-invested.
  - Building a portfolio needs commitments about 30% above target, and on average about 10% of committed capital is never invested.
- **Relevance.**
  - This is a transparent baseline policy that the E10 MPC must beat.
  - The 10% never-invested figure brackets the dossier's ~5% expiry assumption [inference: different sample and period].

**22. [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop)** [missed]
- Vincent Maurin et al. · 2022 · *Management Science* · 8 cit. · DOI 10.1287/mnsc.2022.4612
- **Finding.**
  - Sequential capital calls arise as the optimal answer to GP moral hazard, but they expose LPs to illiquidity risk.
  - LPs that tolerate illiquidity earn higher returns.
  - GPs may inefficiently accelerate drawdowns to avoid LP defaults.
  - A secondary market narrows differences in fund returns, but differences in LP returns remain.
- **Relevance.**
  - This is the theoretical basis for treating ADIC's tolerance of illiquidity as a priced edge in the liquidity shadow price.
  - It also motivates a call-acceleration term in stress (c^stress) [inference].

### F. Secondary market (the SELL operator and the Secondaries group)

**23. [The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop)** [cited as the WP; this is the published version]
- Taylor D. Nadauld et al. · 2019 · *Journal of Financial Economics* · 66 cit. · DOI 10.1016/j.jfineco.2018.11.007
- **Finding.**
  - Most transactions occur at a discount to NAV.
  - Buyers' annualised PME is 1.023 against sellers' 0.976, so buyers out-earn sellers by about 5pp a year.
  - Relatively flexible buyers earn returns by supplying liquidity.
- **Relevance.**
  - This is E9's anchor for the buyer's excess return; use the published 0.976.
  - For the Secondaries group, the same spread is the LEVER return when ADIC supplies the liquidity [inference].
  - Verification issue R15 already treats it as an upper bound for 2026.

**24. [Liquidity Provision in the Secondary Market for Private Equity Fund Stakes](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop)** [missed]
- R. Albuquerque et al. · 2018 · venue not shown (SSRN DOI) · 11 cit. · DOI 10.2139/ssrn.3182481
- **Finding.**
  - On a broker's proprietary bid data, aggregate liquidity shocks lower contemporaneous bids. The effect is strongest for funds likely to be sold when liquidity is low.
  - The response is unrelated to future NAV-to-NAV returns and to future bidding.
  - Discounts therefore vary with the supply of liquidity.
- **Relevance.** Model the discount d̄ as a function of an aggregate liquidity state, not as a signal about future NAV. That puts the endogenous liquidity effect the dossier flags (§8) directly into SELL pricing [inference].

**25. [The Private Equity Secondaries Market During the Financial Crisis and the "Valuation Gap"](https://consensus.app/papers/details/e2a6180114bb5e16be2ab5d849fa5cbf/?utm_source=claude_desktop)** [missed; challenge]
- U. Hege et al. · 2011 · *The Journal of Private Equity* · 5 cit. · DOI 10.3905/jpe.2011.14.3.042
- **Finding.**
  - Effective liquidity in the secondaries market contracted severely in early 2009, to a fraction of earlier volume.
  - A "valuation gap" opened between sellers and buyers, which the authors attribute to framing and loss aversion.
  - The market recovered quickly, with no more protracted turbulence than the stock market.
- **Relevance.**
  - In regime C, SELL needs a cap on volume, not just a lower price [inference].
  - The quick recovery supports the option value of waiting that the dossier's least-squares Monte Carlo SELL timing captures.

---

## 4. Missed-but-important papers and their design implications

### 4.1 State variables

| State to add or change | Evidence | Where it enters |
|---|---|---|
| **Mark-bias state** per asset: the expected mark gap ln N − ln V given strategy, age, activity and GP fundraising status | [Jenkinson et al. 2013](https://consensus.app/papers/details/e297da1e0d0658d8ae2ca7a7a7b6987c/?utm_source=claude_desktop) (conservative overall; inflated during fundraising); [Jenkinson et al., *TAR*](https://consensus.app/papers/details/44d91cea6b8b53b481621e6ed4e6ef9e/?utm_source=claude_desktop) (buyout little bias; VC aggressive since 2000); [Brown, Gredil & Kaplan 2019](https://consensus.app/papers/details/3331159853ab59dea783df670c91ee0a/?utm_source=claude_desktop) (underperformers boost NAVs while fundraising; top funds understate); Driessen et al. 2012 and Phalippou & Gottschalg [cited] (mature or inactive funds overstated; "living dead" holdings); [Hüther, *JFQA*](https://consensus.app/papers/details/834e2e8848615de6808f6adbd5bdda10/?utm_source=claude_desktop) (no inflation at deal level; peaks come from a cohort effect) | E7 mark-gap prior. It replaces the single "75% of exits above the prior mark" calibration, as verification issue R4 asks [inference]. |
| **GP pressure**: time to the end of the investment period or fund life, unused capital, fundraising flag | [Arcot et al.](https://consensus.app/papers/details/e31810e79f6a5141b950725271e50dac/?utm_source=claude_desktop) (pressured sellers exit at lower multiples after shorter holds; pressured buyers pay higher multiples); [Figge et al. 2012](https://consensus.app/papers/details/50d160808df053308b242dd7aa7b9194/?utm_source=claude_desktop) (exits near the end of fund life earn lower deal-level returns); [Kandel et al. 2011](https://consensus.app/papers/details/a8debc8f9ade5075a1db4b8dc0d07e81/?utm_source=claude_desktop) (ageing VC funds continue bad projects and stop monitoring good projects that are prone to delay) | E6 exit pricing and quality drift q; E7 tail-end overstatement [inference]. |
| **Carry-in-the-money indicator** | [Gredil 2021, *JFQA*](https://consensus.app/papers/details/19c56a5254225ac2a85f26e6cd173381/?utm_source=claude_desktop) (GPs sell at industry peaks only when they have performance fees to harvest); Jenkinson et al. 2025, bibliography #8 (long goodbyes when the fund performs better) | A term in the distribution intensity δ and in IPO sell-down speed [inference]. |
| **Secondary liquidity state** L_t (aggregate bid depth and volume) | Albuquerque et al. 2018, #24; Hege et al. 2011, #25; [Kleymenova et al. 2012](https://consensus.app/papers/details/9bc5ce1dd6415d858fb1193b5b1b3466/?utm_source=claude_desktop) | E9 discount and sale capacity; the option value of the Secondaries group's dry powder [inference]. |
| **Separate latent call and distribution factors** | Cao et al. 2025, #1 | E5 and E6 intensities. X_t becomes the distribution factor, and a call factor is added beside it [inference]. |
| **Subscription-line usage** per fund | [Albertus & Denes 2020](https://consensus.app/papers/details/84b7e9e9b66151e78637a4ebfac077ae/?utm_source=claude_desktop) (funds using lines call less capital; timing-sensitive measures are distorted; lines are more common in poorly performing funds); [Brown et al. 2024](https://consensus.app/papers/details/911bba796e2a56e5924f1563664ff4b4/?utm_source=claude_desktop) (interim IRRs are strongly affected by subscription lines and deployment pace) | E5 call timing (deferred, lumpier calls); IRR debiasing in E3 [inference]. |
| **Industry dry powder** | Brown et al. 2020, #10 (dry powder predicts future returns, by fund age); [Simlai 2025](https://consensus.app/papers/details/862f7f824aad5a2ebb2d6ad8ea634d11/?utm_source=claude_desktop) (dry powder and easy lending fuel deal competition; tightening constrains activity) | An input to X_t and to the regime model [inference]. |

### 4.2 Models

1. **Benchmark RFT-TA against published TA extensions** before keeping its extra complexity.
   - Benchmark against the factor TA of Cao et al. (#1) and the historical-simulation TA of Beutler et al. (#3).
   - Require better out-of-sample interval coverage in the dossier's §6.7 backtest [inference].
   - For calibration targets beyond Cambridge Associates, use [Kang Shuang 2026](https://consensus.app/papers/details/bfcee2acb48956d2b7c78208c910bb46/?utm_source=claude_desktop). It covers 7,904 Preqin funds (1982–2025), defines three timing metrics (contribution, breakeven and distribution timing), and calibrates TA to them by asset class, vintage, strategy and size. That responds to verification issue R6.
2. **Exit engine for the Co-investment group and the Secondaries group's direct book.**
   - Use competing-risks hazards with non-monotone baselines ([Giot & Schwienbacher 2007](https://consensus.app/papers/details/1e054ead96575c55952157435b5a7763/?utm_source=claude_desktop); [Félix et al. 2014](https://consensus.app/papers/details/865da2e561b15ad9af6e349f7e156775/?utm_source=claude_desktop), whose hazards are non-monotone for every exit form).
   - Draw timing and multiple jointly, as in Tausch et al. (#9).
   - Give each exit route its own sensitivity to debt and equity markets: Jenkinson & Sousa (#7), and [Wang 2012](https://consensus.app/papers/details/4fd52fd0a7d95726a0b8596f5d1f6dd1/?utm_source=claude_desktop), who finds secondary buyouts more likely when equity markets are cold and debt markets favourable.
3. **Actuarial projection layer.**
   - Pool ADIC's own development triangles with industry triangles through a Bayesian or credibility chain ladder ([Gisler & Wüthrich 2008](https://consensus.app/papers/details/f320f0ed754a5fd5a464b8b87ff0ddf9/?utm_source=claude_desktop)).
   - Compute prediction error for correlated strategy triangles ([Braun 2004](https://consensus.app/papers/details/c0fe9ee7ba165fbfb84c25183c99b9a9/?utm_source=claude_desktop)).
   - Separate vintage, age and calendar effects with an age–period–cohort development model ([Pittarello et al.](https://consensus.app/papers/details/02c8f72039825595b0a3d16d81758997/?utm_source=claude_desktop)).
   - Hiabu shows that chain-ladder factors equal a hazard in reversed development time, and that chain ladder is biased when row effects differ across levels of aggregation ([Hiabu 2017](https://consensus.app/papers/details/a1190b5121e05c39a4da92fd886093b0/?utm_source=claude_desktop)).
   - This directly answers verification issue R6, which faults the calibration for mixing vintage and calendar effects [inference].
4. **Performance input to E3.**
   - Use the α of Korteweg et al. (#17) or direct alpha, and avoid IRR. [Larocque et al. 2020](https://consensus.app/papers/details/bc277472043e5f12ae76b6ac41eeb268/?utm_source=claude_desktop) attribute more than half of funds' IRR to timing. See also Jenkinson et al. 2013 (#12) and Brown et al. 2024.
   - Adjust cash-flow-based alpha for variation in discount rates using a secondary-price index (Boyer et al., #15).
   - PME theory says the discount rate should approximate the return on the investor's overall wealth portfolio ([Sørensen & Jagannathan 2015](https://consensus.app/papers/details/d8f3498ac57a5fe8865988cd887d8d99/?utm_source=claude_desktop)). Under TPA, that means benchmarking against ADIC's own total portfolio [inference].
5. **Smoothing filter (E7).**
   - Make λ regime-dependent: smoothing varies over time, rising when prices or uncertainty rise and falling in recessions ([Cho et al. 2014](https://consensus.app/papers/details/6bd79b131c5b5ecfa9e1c669c80634b1/?utm_source=claude_desktop)).
   - Consider asymmetry, with gains reported fully and losses delayed ([Bollen & Pool 2008](https://consensus.app/papers/details/91dda5ed60b15d64a9ed06cae10e125d/?utm_source=claude_desktop)). This evidence comes from real estate and hedge funds, so applying it to PE is [inference].
   - For heavily smoothed series, unsmoothed volatility can overstate true volatility, and cross-asset correlations cannot be fully recovered ([Frei 2024](https://consensus.app/papers/details/d35d4e1ecf44524eb84639452a64a82c/?utm_source=claude_desktop)). Validate against secondary or listed prices (Ennis, #16; Boyer, #15).
6. **Idiosyncratic noise in E2.**
   - Fund multiples have fat tails, especially in VC, with "infinite variance over the lifetime of the fund" ([Lahr 2022](https://consensus.app/papers/details/ccdf65b87d465bbbbb2d03e387b6d20c/?utm_source=claude_desktop)).
   - Replace Gaussian ε_i with a heavy-tailed draw. This is consistent with BGG's estimation failing for heavy-tailed funds [inference].
7. **Optimiser (E10).**
   - Compare the linearised MPC with a dynamic model that includes business-cycle states and serial correlation in observed returns, solved with machine-learning methods ([Chen et al. 2025](https://consensus.app/papers/details/da8e4aa55bd25aca8a43f6c4444f3334/?utm_source=claude_desktop)).
   - Compare it also with interpretable learned recommitment rules ([Kieffer et al. 2023](https://consensus.app/papers/details/1a08544fb5305532bc1270a2b91fa377/?utm_source=claude_desktop)).
   - Keep the de Zwart rule (#21) as the baseline.

### 4.3 Parameters

| Parameter | Dossier | Literature | Suggested change [inference] |
|---|---|---|---|
| IPO sell-down (E6) | 4–8 quarters | Post-IPO holdings average 3 years, and losers are held longer (Jenkinson et al. 2025, #8). Sponsors hold "well beyond lockup expiration" ([Dong et al. 2020](https://consensus.app/papers/details/051a66c6db04509ab20158088ddb324d/?utm_source=claude_desktop)). | 8–16 quarters; slower when the post-IPO return is negative |
| Buyout economic beta | 1.05–1.25 | About 1.0 (BGG, cited); close to 1 for listed funds of funds (Jegadeesh et al., cited); about 1.5 for listed buyout at market prices (Ennis et al. 2026, #16) | Keep the base; add a 1.5 sensitivity |
| Net buyout alpha prior | 0 to +2% | **Positive:** Harris, Jenkinson & Kaplan 2014 [cited] (more than 3% a year over the S&P 500); [Korteweg 2019 review](https://consensus.app/papers/details/996d0a57b17957dd81fec3ac0698ec30/?utm_source=claude_desktop) (buyout positive before and after fees against a levered stock portfolio). **Zero or negative:** Boyer et al. 2021 (zero alpha on the secondary index); Ennis et al. 2026 (no meaningful alpha); Gupta & Van Nieuwerburgh [cited] (negative risk-adjusted profit); Phalippou & Gottschalg [cited] (−3.83% a year net); Jegadeesh et al. [cited] (market expects −0.5% to 2%); Franzoni et al. [cited] (a liquidity factor takes alpha to zero) | Centre the prior near zero with wide, symmetric uncertainty, and let the IC choose the scenario |
| Break-even alpha (the hurdle for HOLD and LEVER) | 3.08% (Sorensen, Wang & Yang) | "Annual break-even alphas amount to around 7 percent" under a standard compensation contract ([Buchner et al. 2015 WP](https://consensus.app/papers/details/75d3e23d140b53f792352cb16b7cac6c/?utm_source=claude_desktop)) | Report a range; the hurdle depends on the model |
| Loading of interim performance on forward alpha (E3) | Implicitly 1 | Little buyout persistence after 2000 except at the bottom (Harris et al. 2020, #18). Persistent in the long run but too noisy to invest on ([Korteweg & Sorensen 2017](https://consensus.app/papers/details/a0bf5a58fd485ea895fabd5c39cb76ce/?utm_source=claude_desktop)). | 0–0.3 for buyout; higher for VC |
| Cash-election probability in continuation vehicles (E6) | Rises with π_t | "An estimated 80%–90% of legacy investors choose to cash out" ([Deane et al. 2025, CFA Institute report](https://consensus.app/papers/details/23aed12e6aa650ac9d160c9cf1c5ed5a/?utm_source=claude_desktop)) | Base of about 0.85, then modulated by π_t |
| Never-called share of commitments | About 5% | About 10% (de Zwart et al. 2012, #21; Thomson VE, 1980–2005) | A 5–10% range |
| Early drawdown speed (European funds) | §6.4 schedule | 23% drawn at the vintage date, 60% within three years; LPs get their money back slightly after year 7 ([Diller & Kaserer 2004](https://consensus.app/papers/details/e500278e15e858aab6328618d2c58212/?utm_source=claude_desktop); older European data) | A regional calibration check |
| Fund-level secondary discount | Strategy, age, quality, geography | An interest is more liquid when the fund is larger and buyout-focused, has less undrawn capital and fewer distributions, and draws non-traditional buyers in favourable markets. Liquidity is priced in winning bids (Kleymenova et al. 2012). | Add fund size and undrawn-share terms to d_i |
| Exit-factor inputs z (E1) | IPO and M&A volume, high-yield OAS, loan issuance, rates, secondary pricing, valuation gap | Debt and equity conditions drive the exit route (Jenkinson & Sousa 2015). Secondary buyouts rise when equity is cold and debt is favourable (Wang 2012). Exit valuations are cointegrated with the term spread, credit spread and financial conditions (Simlai 2025). Market liquidity reaches PE returns through funding liquidity (Franzoni et al., cited). | Add the term spread and a financial-conditions index |
| Calls in a crisis (regime C) | m^C = 0.8 plus a stress add-on | In 2007–09, the part of calls not explained by macro factors spiked, and sensitivities changed ([Robinson & Sensoy 2010 WP](https://consensus.app/papers/details/670e7c8aa77251b2afbd54c9ad57d9b2/?utm_source=claude_desktop)). PE-backed firms received more equity and debt during the 2008 crisis ([Bernstein et al. 2017](https://consensus.app/papers/details/97432e549ab95294a7e793a5bc138616/?utm_source=claude_desktop)). | Treat m^C(C) as uncertain, 0.8–1.1 |
| Smoothing λ | Constant per strategy | Varies over time (Cho et al. 2014); conditional on gains versus losses (Bollen & Pool 2008) | Make λ depend on the regime, λ(S) |

### 4.4 Constraints

- **SELL capacity and feasibility.**
  - Cap the volume sellable per quarter by regime (Hege et al., #25).
  - Model transfer restrictions and GP consent. [Lerner & Schoar 2004](https://consensus.app/papers/details/490b5722c3535ebe9382df360741067d/?utm_source=claude_desktop) document transfer restrictions in PE partnership contracts. The restrictions are less prevalent in later funds of the same firm, and where LPs, such as endowments and foundations, are known to have few liquidity shocks.
  - Add a reputational cost of selling to future fund access [inference].
- **Over-commitment.** Use de Zwart et al. (#21) as a reference point for k^max: 30% over-commitment during build-up, with an 8% probability of over-investment [inference].
- **Treasury liquidity tiers.** Set tiers for unfunded commitments by observed call speed, and account for diversification of call risk across managers ([Schneider et al. 2022](https://consensus.app/papers/details/e62567eabe7e5b1fa024e17415c9e803/?utm_source=claude_desktop), "liquidity tiering", which covers PE and private debt). Corporate Finance owns this constraint.
- **Suspending commitments as a feasible action.** Stress tests show that suspending future commitments can rebalance a portfolio without forced secondary sales ([Leote de Carvalho et al. 2026](https://consensus.app/papers/details/12cd077c32a755c9bbab6ea80a91706c/?utm_source=claude_desktop); the setting is open-ended funds).

### 4.5 Objectives

- **Cash-flow risk terms.** Add explicit capital-risk and funding-liquidity-risk terms to the pacing objective (Jeet et al. 2026, #5). Express them through CFaR and liquidity-adjusted VaR, as in the risk-management framework of [Buchner 2017](https://consensus.app/papers/details/b537bb56a809528a9fc72ddf13ee980e/?utm_source=claude_desktop).
- **Commitment timing.** Do not credit commitment timing with alpha (Brown et al. 2020, #19). Credit robustness to the drought instead [inference].
- **Illiquidity tolerance.** Price it as a source of return (Maurin et al., #22; Gourier et al., #20). The objective should credit dry powder held for drought-time opportunities in the Secondaries and Capital Solutions groups [inference].
- **Co-investment concentration.** Penalise it. Skill uncertainty and diversification constraints lower certainty-equivalent returns by 2–8% ([Gredil et al. 2020](https://consensus.app/papers/details/062234d9141e5e2b843e6c5c5a3e736d/?utm_source=claude_desktop)) [inference].

### 4.6 Agent and IC design

- **Mark-credibility agent.**
  - Applies the mark-bias state in §4.1.
  - Flags funds that are fundraising (Barber & Yasuda, #14), funds with low realisation, and old or inactive funds (Driessen et al.; Phalippou & Gottschalg).
  - Treats VC more aggressively than buyout (Jenkinson et al., *TAR*, #13).
- **Timing-optimism challenger.** This sharpens an agent the dossier already proposes.
  - Use reference-class ("outside view") forecasting ([Lovallo & Kahneman 2003](https://consensus.app/papers/details/fb54a75a54765f52834bd50ea8261ef7/?utm_source=claude_desktop)), with priors from Brown et al. 2020 (#10) and Tausch et al. (#9).
  - Run lookback calibration of past forecasts.
  - Survey evidence on corporate managers finds them not over-optimistic on average, but overprecise and prone to overextrapolation ([Barrero 2018](https://consensus.app/papers/details/90c814a773305cee82f296e5b721227a/?utm_source=claude_desktop)). If the same holds for GPs and the groups, forecast bias b_F should vary with recent performance, and forecast-error variance should be inflated [inference].
- **Secondary-market intelligence agent**, run by the Secondaries group.
  - Maintains the liquidity state L_t from bid data (Albuquerque et al., #24; Kleymenova et al.).
  - Needs conflict-of-interest controls: in continuation vehicles the GP sits on both sides (Deane et al. 2025).
- **IC dashboard.**
  - Show drawdown probabilities on both reported and economic NAV. Smoothing turns a 15–16% three-year probability of a 30% drawdown into an observed probability near zero ([Baz et al. 2022](https://consensus.app/papers/details/caa37340c87c559094d28c3d3ae9b696/?utm_source=claude_desktop)).
  - Present the alpha debate as an explicit scenario parameter: positive per Harris, Jenkinson & Kaplan and Korteweg 2019; zero or negative per Boyer, Ennis, Gupta & Van Nieuwerburgh, and Phalippou & Gottschalg.
- **Corporate Finance / Treasury seat.** Owns CFaR, the liquidity tiers, the crisis scenario for SELL capacity and the stress-call add-on.

### 4.7 Further relevant papers (one line each)

**Cash-flow models and pacing**
- [Jeet 2020, market-sensitive periodic growth](https://consensus.app/papers/details/19f6b1a1e177534a8ffc2f0eea7cb9e5/?utm_source=claude_desktop): the model the dossier could not find.
- [de Malherbe 2007](https://consensus.app/papers/details/6bf2e247016e532ca0285194c8bcce47/?utm_source=claude_desktop): a four-factor stochastic fund model that includes the reliability of reported values.
- [Meyer 2024, *The Art of Commitment Pacing*](https://consensus.app/papers/details/662d9b40176f5566bd73002284298286/?utm_source=claude_desktop): a book-length treatment of pacing, cash-flow forecasting, stress scenarios, and modelling of co-investments and secondaries.
- [Shen et al. 2021, *JPM*](https://consensus.app/papers/details/61e21abbf1425eac88e593ae69993030/?utm_source=claude_desktop): links bottom-up private cash flows to top-down allocation and measures how often liquidity events of different severity occur.
- [Reus et al. 2015, *J. Asset Mgmt*](https://consensus.app/papers/details/a41e24edf0b25f32b3f29cf414b80885/?utm_source=claude_desktop): a multistage stochastic program for PE commitments; in their model, the leverage option lowers performance.

**Illiquidity, fees and the hurdle**
- [Buchner 2015, *RFE*](https://consensus.app/papers/details/24c3c46694cf5534b14b393ab4547dcb/?utm_source=claude_desktop): an upper bound on the discount for lack of marketability of $35.3 per $100 committed at fund start, about 7% a year.

**Smoothing and benchmarks**
- [Ilmanen et al. 2019, *JAI*](https://consensus.app/papers/details/a68bd35193035f3682f6c18567bb5cff/?utm_source=claude_desktop): a levered small-cap index may be the better benchmark; smoothing understates risk; the expected edge declines over time.
- [Pedersen et al. 2014, *FAJ*](https://consensus.app/papers/details/7aafc0cc9de654aa807e423ab440e3da/?utm_source=claude_desktop): lagged-beta multi-factor risk model for all alternatives.
- [Anson 2024, *JPM*](https://consensus.app/papers/details/b824603706ab55abbca0473de791c8d8/?utm_source=claude_desktop): lagged betas extended to secondary PE, private credit and private real estate.
- [Jeet et al. 2024, *JPM*](https://consensus.app/papers/details/f60b12086bca57b8a706cd0e7a03b79a/?utm_source=claude_desktop): Bayesian state-space model that desmooths returns and estimates alpha and beta jointly.

**LP and manager skill**
- [Cavagnaro et al. 2019, *JF*](https://consensus.app/papers/details/ce8a4e711b4e52be85a0d0b03ffe44dd/?utm_source=claude_desktop): one standard deviation of LP skill is worth 1–2pp a year. A prior for the credibility ADIC gives its own groups [inference].

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier recommendation | Challenging evidence | What it implies |
|---|---|---|---|
| 1 | LEVER through new commitments, with pacing as a main control (E9, E10) | Brown et al. 2020, *JFE* (#19): commitment-timing strategies gain modestly at best; investors cannot time calls or exits; net cash flows are highly correlated across strategies. | Pacing changes give little near-term liquidity relief or alpha. For payout coverage in 2027–29, lean on SELL, REFINANCE and the overlay, and keep pacing for long-run exposure [inference]. The same paper supports the dossier's view that the systematic state dominates portfolio cash flows. |
| 2 | Net buyout alpha prior of 0 to +2%, and PME or direct alpha as the actual-to-date signal (§2.6, E3) | Boyer et al. 2021 (#15): zero alpha on the secondary-price index, against large positive cash-flow measures. Ennis et al. 2026 (#16): no meaningful alpha. Also the cited Gupta & Van Nieuwerburgh and Phalippou & Gottschalg. | Centre the prior at or below zero for HOLD and LEVER tests, and adjust PME-type signals for variation in discount rates [inference]. The contrary evidence (Harris, Jenkinson & Kaplan 2014; Korteweg 2019) should appear as an IC scenario rather than be averaged away. |
| 3 | Buyout economic beta of 1.05–1.25 (§6.4) | Ennis et al. 2026 (#16): beta about 1.5 at market prices. | Add a 1.5 sensitivity. A higher beta raises crisis-path CFaR and makes selling ahead of drawdowns more attractive [inference]. |
| 4 | Break-even alpha of 3.08% as the hurdle (§2.6) | Buchner et al. 2015 WP: break-even alphas of "around 7 percent" under a standard compensation contract. | The hurdle depends on the model. Show a range, and make sure fees are not double-counted (verification issue R1) [inference]. |
| 5 | IPO exits staged over 4–8 quarters (E6) | Jenkinson et al. 2025, *Mgmt Sci* (#8): post-IPO holdings average 3 years, and losers are held longer. Dong et al. 2020: sponsors hold well beyond lockup. | Lengthen the sell-down to about 8–16 quarters and make it depend on post-IPO performance. DPI from a reopening IPO window arrives more slowly than modelled [inference]. This is consistent with MSCI's "the listing itself is not the liquidity event" (dossier §4.4). |
| 6 | Noise in the actual-to-date signal shrinks with effective age, Var(e^A) = τ_A²/(a^e·ρ) (E3) | Brown et al. 2020, "Evolution" (#10): dispersion of future IRR and direct alpha increases for funds older than about 5–8 years. | Do not let posterior uncertainty about forward alpha collapse for old funds. Add a forward-uncertainty term that grows with age [inference]. |
| 7 | A constant smoothing parameter λ_s per strategy (E7, §6.4) | Cho et al. 2014: smoothing "varies substantially over time". Bollen & Pool 2008: losses are reported with a delay. | Make λ depend on the regime, and possibly on whether returns are gains or losses. The evidence is from real estate and hedge funds, so applying it to PE is [inference]. |
| 8 | SELL priced with a regime discount only; regime C at 60–75% of NAV (E9, §6.5) | Hege et al. 2011 (#25): volume fell to a fraction of earlier levels in early 2009. Albuquerque et al. 2018 (#24): discounts track the supply of liquidity. | Add a capacity constraint and a discount driven by the liquidity state; in a crisis, volume binds as well as price. The quick recovery supports the option to wait [inference]. |
| 9 | Crisis call multiplier m^C(C) = 0.8 plus an add-on (§6.5, E5) | Robinson & Sensoy 2010 WP: the unexplained part of calls spiked during 2007–09. Bernstein et al. 2017: PE-backed firms received more equity during the crisis. Maurin et al. 2022: GPs may accelerate drawdowns. | Net crisis calls may not fall at all. Treat m^C(C) as uncertain (0.8–1.1) and test payout coverage at the high end [inference]. |
| 10 | Exit proceeds calibrated so that P(proceeds > next-to-last mark) ≈ 0.75 (E7) | Jenkinson et al. 2013 (#12): valuations understate subsequent distributions by about 35% on average, but are inflated during fundraising. Jenkinson et al., *TAR* (#13): buyout NAVs show little bias, VC NAVs are aggressive. Driessen et al. and Phalippou & Gottschalg: mature and inactive funds are overstated. | The uplift depends on strategy, age and activity. This supports verification issue R4 [inference]. |
| 11 | The novelty claim: practitioner TA lacks dispersion and market dependence (§5) | Cao et al. 2025 (#1); Beutler et al. 2023 (#3); Jeet 2020. | Published TA extensions already add factors, randomness and historical simulation. Present RFT-TA as an extension of them and benchmark it against them [inference]. |
| 12 | LEVER through leverage, accepted when the robust gate passes (E9) | Reus et al. 2015: in their multistage model, the leverage option for PE lowers performance even when PE volatility is low. | The result is model-specific and weak evidence. It is one more reason to keep LEVER behind the Tier-1 robust gate [inference]. |

**Missed papers that support the dossier.**
- Jenkinson & Sousa 2015 and Simlai 2025: an exit factor driven by financing conditions.
- Giot & Schwienbacher 2007: falling exit hazards in residual inventory, behind the adverse-selection drift in q.
- Brown et al. 2020, "Evolution": the alpha runway.
- Kandel et al. 2011, Arcot et al. and Figge et al. 2012: weaker prices at the tail end of fund life.
- Franzoni et al. 2012 (cited) and Maurin et al. 2022: the funding-liquidity channel.

---

## 6. Usage message

None. No Consensus result in this session contained a sign-up, upgrade or usage message.

---

## 7. Search log

**Consensus: citation checks (17 queries)**
1. Takahashi Alexander Illiquid Alternative Asset Fund Modeling
2. Buchner Kaserer Wagner Modeling the Cash Flow Dynamics of Private Equity Funds: Theory and Empirical Evidence
3. Luxenberg Boyd Strategic Asset Allocation with Illiquid Alternatives
4. A Crucial Enhancement to the Takahashi and Alexander's Cash Flow Model
5. Brown Ghysels Gredil Nowcasting Net Asset Values: The Case of Private Equity
6. Robinson Sensoy Cyclicality, Performance Measurement, and Cash Flow Liquidity in Private Equity
7. Ljungqvist Richardson The Cash Flow, Return and Risk Characteristics of Private Equity
8. cash flow, return and risk characteristics of private equity funds drawdown of committed capital years to invest
9. Gourier Phalippou Westerfield Capital Commitment private equity
10. Giommetti Sorensen Optimal Allocation to Private Equity
11. Geltner Smoothing in Appraisal-Based Returns
12. Getmansky Lo Makarov An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns
13. econometric model of serial correlation and illiquidity in hedge fund returns smoothing profile
14. Korteweg Nagel Risk-Adjusting the Returns to Venture Capital generalized public market equivalent
15. Gredil Griffiths Stucke Benchmarking private equity: The Direct Alpha method Journal of Corporate Finance
16. Karatas Klinkert Hirsa Supervised Neural Networks for Illiquid Alternative Asset Cash Flow Forecasting
17. Bühlmann Experience Rating and Credibility ASTIN Bulletin

**Consensus: topical backfill (14 queries)**

Seeds 1, 2 and 4–6 were run as refined below. The PME seed was covered by the PME-focused citation-check queries (14, 15) together with query 20.

18. private equity cash flow model capital calls distributions stochastic macroeconomic factors
19. private equity NAV smoothing unsmoothing stale valuations systematic risk beta
20. nowcasting private equity fund returns between quarterly reports secondary market prices
21. private equity exits and market conditions IPO window credit spreads holding period exit timing
22. optimal commitment pacing private equity liquidity constraint overcommitment dynamic programming institutional investor
23. private equity distribution drought low DPI rising interest rates exit slowdown limited partners liquidity 2023
24. continuation funds GP-led secondary transactions pricing conflicts of interest limited partners
25. subscription lines of credit private equity funds capital call timing IRR fund-level leverage
26. competing risks hazard model private equity portfolio company exit IPO trade sale secondary buyout write-off duration
27. private equity fund term extension zombie funds tail-end residual net asset value overvaluation
28. chain ladder development triangle actuarial reserving method applied to private equity fund cash flow forecasting
29. private equity capital calls and distributions during the 2008 financial crisis limited partner liquidity shock default on commitments
30. secondary market for private equity fund stakes discounts liquidity provision financial crisis buyers sellers
31. optimism bias in private equity deal projections underwriting forecasts versus realized returns exit timing

**WebSearch (2 queries; used only for works Consensus could not return)**
- W1. Ljungqvist & Richardson, NBER WP 9454 → https://ideas.repec.org/p/nbr/nberwo/9454.html
- W2. Getmansky, Lo & Makarov (2004), *JFE* 74(3), 529–609 → https://www.nber.org/papers/w9571
