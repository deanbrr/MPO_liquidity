# Stream 11 literature check: objective design (target attainment with distributions and illiquidity)

**Dossier checked:** `research/dossiers/11_objectives.md` (627 lines, "As of 2026-10-18").
- §10 lists 51 academic works: journal articles, working papers, arXiv preprints and one book chapter. It also lists market, peer and regulatory sources (MSCI, NACUBO, J.P. Morgan, Harvard Crimson, APFC, Solvency II, Basel, DNB, CPP), which are outside this check.
- One academic work is used in the text but missing from §10: Föllmer & Leukert (2000), the "follow-up" quoted in §2.1.

**Date:** 2026-10-18.

**Search engine:** Consensus. 12 searches, run one at a time with no filters (query list in §7).
- Every query was built to serve both tasks: it covered one of the six seed topics (or a refinement) and was aimed at a cluster of dossier references.
- 3 WebSearches confirmed metadata that Consensus did not return (§7).

**Quota note.** The Consensus monthly allowance is shared with two other agents. During this run it fell from 47 to 17 searches remaining; 12 were used here. I stopped at 12 to leave capacity for the other agents. As a result:
- title-by-title look-ups were replaced by topical queries that surface several dossier references at once;
- Consensus records already retrieved by sibling streams 01, 02, 03, 04, 06 and 09 were re-used for 7 references. They are labelled as such and were not re-searched.

**Companion:** `research/verification/11_objectives.verify.md`. It checked 40+ references against Crossref, arXiv and RePEc and found none hallucinated. It flags reasoning issues R1–R15. The most serious is **R1: the C3 risk-constrained-Kelly (RCK) drawdown constraint is infeasible across the whole 5–10% payout band**. This check adds Consensus confirmation of the most load-bearing references and the literature the dossier misses, including literature that bears directly on R1, R2, R4 and R5.

**Organizational mapping (user, 2026-10-18).**
- PE allocates to funds (interpretation confirmed).
- Secondaries is a hybrid of direct and fund investments.
- Corporate Finance owns the treasury function. Per the context file it also owns portfolio-level borrowing, overlay collateral and distribution payments.
- Implications below are assigned on that basis:
  - distribution reliability, liquidity coverage, the payout rule and the owner-demand model go to **Corporate Finance (Treasurer seat)**;
  - pacing and SELL / HOLD items go to the **private-markets groups** (PE, Secondaries, Co-investment, Capital Solutions, Private Credit);
  - risk limits on the opportunistic book go to **Overlay**;
  - objective, parameter and reporting choices go to the **IC**.

**Reading conventions**
- Findings come from the titles and abstracts Consensus returned. Full texts were not read.
- **[Inference]** marks design reasoning that goes beyond what an abstract states.
- Authors are shown as Consensus displays them, with "et al." where Consensus truncates. Running text sometimes uses well-known co-author surnames; links point to the Consensus records.
- Years are Consensus record years. Where a record carries an online-first or working-paper year, the print year is noted.
- Several 2025–2026 items are recent and have few citations. They are flagged where they appear.

---

## 1. Summary

### Citation integrity
- **Scope.** The 25 most load-bearing of the 51 works. The table has 26 rows because the scenario-approach pair (Calafiore & Campi; Campi & Garatti) is split.
- **Result: 20 confirmed, 0 mismatched, 0 not found, 6 not checked.**
  - 12 confirmed by this stream's own Consensus searches: Browne (1999); Das et al. (CMS); Basak & Shapiro; Grossman & Zhou; Chekhlov, Uryasev & Zabarankin; Busseti, Ryu & Boyd; Nemirovski & Shapiro; Brown & Sim; Chen & Sim; Shapiro (2009); Philpott & de Matos; Gourier, Phalippou & Westerfield (working-paper record).
  - 7 confirmed through Consensus records retrieved by sibling streams: Rockafellar & Uryasev (2000); Dybvig (1999); Boyd et al. (2017); Ang, Papanikolaou & Westerfield; Brown, Dimmock, Kang & Weisbenner; Mohajerin Esfahani & Kuhn; Calafiore & Campi.
  - 1 confirmed by WebSearch only: Long, Sim & Zhou (2023). A targeted Consensus query did not return it.
  - **Not checked (quota):** Browne (1997); Föllmer & Leukert (1999), which is indirectly corroborated; Fishburn (1977); Campi & Garatti (2008); Ruszczyński (2010); Avanzi (2009). The verification log confirmed all six against Crossref or RePEc.
- **No hallucinated or garbled references.**
- **Every claim that could be checked against an abstract matched.** Examples:
  - Browne: "equivalent to simply buying a European digital option";
  - Basak & Shapiro: VaR managers "often optimally choose a larger exposure to risky assets ... and consequently incur larger losses, when losses occur";
  - Grossman & Zhou's surplus rule W − αM;
  - Chekhlov et al.: CDD is the mean of the worst (1 − α) drawdowns, with max and average drawdown as limits;
  - Chen & Sim: "maximizes the shortfall-aware aspiration-level criterion", solved with CVaR LPs and SOCP decision rules;
  - Brown & Sim: satisficing measures are "dual to classes of risk measures";
  - Gourier et al.: investors "would pay more to adjust the quantity committed than to remove timing uncertainty or limited tradability" (stream 04 record).
- **Metadata to complete.** None of these is a substantive error.
  - Rockafellar & Uryasev (2000): add pp. 21–41 and DOI 10.21314/jor.2000.038. The dossier says "journal details from memory".
  - Das et al.: *Computational Management Science*, DOI 10.1007/s10287-019-00351-7. This resolves the dossier's ⚠.
  - Busseti, Ryu & Boyd: add the journal version, *The Journal of Investing* (2016), DOI 10.3905/joi.2016.25.3.118.
  - Boyd et al. (2017): add *Foundations and Trends in Optimization*, DOI 10.1561/2400000023.
  - Ang, Papanikolaou & Westerfield: add 60(11):2737–2761 and DOI 10.1287/mnsc.2014.1986.
  - "Esfahani, P.M." should read **Mohajerin Esfahani, P.**; add DOI 10.1007/s10107-017-1172-1.
  - Add Föllmer & Leukert (2000), *Finance and Stochastics* 4:117–146, to §10. The volume and pages are corroborated by a citing abstract in Consensus.
- **Consensus year quirks.** These are not dossier errors; the DOIs match the journal versions the dossier cites.
  - Browne shows 1996 (working-paper date).
  - Basak & Shapiro shows 1999.
  - Chekhlov et al. shows 2004 (SSRN).
  - Brown & Sim shows 2008 (online-first).

### Backfill (12 dual-purpose topical searches)
The 12 searches returned about 235 records (search 1 was dominated by psychology papers on deadlines). 25 are annotated in §3 and about 55 more are listed in §4.7. The dossier misses six bodies of work that bear directly on its objective design:
1. **Time consistency versus pre-commitment for CVaR-type objectives.** Forsyth (2020); Strub et al. (2019); Pflug & Pichler (2016); Homem-de-Mello & Pagnoncelli (2016); Dang et al. (2025) on buffered probability of exceedance (bPoE).
2. **Dynamic versus static risk limits.** Cuoco, He & Isaenko (2008); Wei (2021); Armstrong & Brigo (2019).
3. **Goal-based refinements.** Krabichler et al. (*Hedging goals*); Capponi et al. (2024); Das et al. (2021); Leibowitz et al. (2021); Kim et al. (2019).
4. **Joint and distributionally robust chance constraints.** Zymler, Kuhn & Rustem; Chen, Sim, Sun & Teo (2010); Jiang & Xie (ALSO-X); Chen, Kuhn & Wiesemann; and the DRO / robust-satisficing equivalence of Wang et al. (2025).
5. **Growth with downside control, and drawdown with payouts.** MacLean et al. (2021); Wei et al. (2024); Angoshtari, Bayraktar & Young; Cherny & Obłój.
6. **Spending-rule economics.** Campbell & Sigalov (reaching for yield); Dang, Forsyth & Vetzal (2017); Mork et al. (2022, two papers); Kashif et al. (2020); Jeon et al. on ratcheting.

### Net assessment
- **The dossier's architecture is well supported:** safety-filtered, shortfall-aware growth; a rolling horizon; robust CVaR constraints; IC pre-commitment; and P(10%) reported rather than maximized.
- **Five recommendations should be revised in light of the literature:**
  1. **Replace C3.** Use a regime-aware convex shortfall penalty below a payout-consistent threshold path (MacLean et al. 2021), or embed drawdown control in the utility (Cherny & Obłój). This addresses verification R1 and R2.
  2. **Restrict the target-shortfall exponent sweep to α > 1.** Probability maximization and expected-shortfall (α = 1) minimization can give the same policy (Krabichler et al.).
  3. **Do not promise "full time-consistency" through nested CVaR.** Formalize IC pre-commitment as an induced objective (Forsyth; Strub et al.), or use expected conditional risk measures (Homem-de-Mello & Pagnoncelli). Report bPoE for tail statements (Dang et al. 2025).
  4. **The cure for VaR-type gambling is dynamic re-imposition, not expected shortfall as such** (Cuoco et al.; Wei 2021). Make the C4 floor rolling.
  5. **Use joint chance-constraint approximations for C1** instead of union-bound splitting. Consider ALSO-X to cut CVaR conservatism, and validate every surrogate by simulation.
- **Two economic caveats belong in the IC pack:**
  - a hard sustainable-spending constraint induces **reaching for yield** when real rates fall (Campbell & Sigalov);
  - optimal spending for funds with a soft floor is **procyclical**, which cuts against smoothing and ratchets (Mork et al.).

---

## 2. Citation-integrity table

Status values: found, mismatched, not found, or not checked. Online-first versus print years, and working-paper versus journal records, are not counted as mismatches. "Stream 0X record" means the Consensus record was retrieved by that sibling stream's check and re-used here without a new search.

| # | Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|---|
| 1 | Browne (1999), *Reaching goals by a deadline: digital options and continuous-time active portfolio management*, AAP 31(2):551–577 | found | Record year 1996 (working-paper date); DOI 10.1239/aap/1029955147 matches; 133 citations. The abstract confirms "equivalent to simply buying a European digital option" and the log-optimal portfolio replacing the stock in the general case. A citing abstract gives "Adv Appl Probab 31(2):551–577, 1999" ([Krabichler et al.](https://consensus.app/papers/details/c7d8bb6499c75f8e93935fa3a567584b/?utm_source=claude_desktop)). | [link](https://consensus.app/papers/details/2e3d0f7c7f585f1395468ce6a2fa6816/?utm_source=claude_desktop) |
| 2 | Browne (1997), *Survival and growth with a liability*, MOR 22(2):468–493 | not checked (quota) | Confirmed against Crossref in the verification log. | — |
| 3 | Das, Ostrov, Radhakrishnan & Srivastav, *Dynamic portfolio allocation in goals-based wealth management*, SSRN 3211951 (2018); CMS (2020) ⚠ | found; resolves ⚠ | *Computational Management Science*, DOI 10.1007/s10287-019-00351-7; record year 2019 (online-first); 27 citations. The abstract confirms DP over efficient portfolios to maximize P(target wealth), and adds that the algorithm "accommodates periodic infusions or withdrawals of cash". The verification log gives 17(4):613–640 (2020). | [link](https://consensus.app/papers/details/fbbb8cd25dcd5b1884737b2b6a3f5903/?utm_source=claude_desktop) |
| 4 | Föllmer & Leukert (1999), *Quantile hedging*, F&S 3(3):251–273 | not checked directly; corroborated | No record of its own surfaced. Krabichler et al.'s abstract cites "Föllmer and Leukert in Finance Stoch 3:251–273, 1999". It also cites "Finance Stoch 4:117–146, 2000" for efficient hedging, the follow-up quoted in dossier §2.1 but missing from §10. | corroborating record: [Krabichler et al.](https://consensus.app/papers/details/c7d8bb6499c75f8e93935fa3a567584b/?utm_source=claude_desktop) |
| 5 | Basak & Shapiro (2001), RFS 14(2):371–405 | found | Record year 1999 (ERN working-paper label) with RFS DOI 10.1093/rfs/14.2.371; 923 citations. Abstract: VaR risk managers "often optimally choose a larger exposure to risky assets than non risk managers, and consequently incur larger losses, when losses occur"; the alternative is "based on the expectation of a loss". Later work qualifies the remedy (§5). | [link](https://consensus.app/papers/details/42ca5a173dc056ad80b9b762c211b613/?utm_source=claude_desktop) |
| 6 | Fishburn (1977), AER 67(2):116–126 | not checked (quota) | The verification log matched RePEc metadata; no abstract is online. | — |
| 7 | Dybvig (1999), *Using asset allocation to protect spending*, FAJ 55(1):49–62 | found (stream 02/03 record) | DOI 10.2469/faj.v55.n1.2241; 53 citations. The FAJ record has a blank author field; the 1998 working-paper record lists Dybvig. Separately, [Kashif et al. (2020)](https://consensus.app/papers/details/f11a9145a77b5305bdf13f26c640edcb/?utm_source=claude_desktop) describe hybrid-rule endowments as using "asset allocation to protect spending". | [link](https://consensus.app/papers/details/ac6b4afe4adf5de68e6dee26fa078f05/?utm_source=claude_desktop) |
| 8 | Grossman & Zhou (1993), Math. Finance 3(3):241–276 | found | DOI 10.1111/j.1467-9965.1993.tb00044.x; 385 citations. The abstract confirms risky investment "in proportion to the 'surplus' W_t − αM_t" for CRRA utility. | [link](https://consensus.app/papers/details/5e80ded6b6c8585aa0607d96ebbfa9ae/?utm_source=claude_desktop) |
| 9 | Rockafellar & Uryasev (2000), *Optimization of conditional value-at-risk*, J. Risk 2(3) ("journal details from memory") | found (stream 01/03 record) and confirmed by WebSearch | My title-phrase query did not return it. The stream 01/03 record carries DOI 10.21314/jor.2000.038 and 7,235 citations, but the abstract attached to it belongs to a different paper (a database artefact). WebSearch (Risk.net, IDEAS, a Deakin record) gives J. Risk 2(3), 2000, pp. 21–41; one listing says 21–42. **Add the pages and DOI.** | [link](https://consensus.app/papers/details/a500ccf654ae5205a70fe138eb0d82d7/?utm_source=claude_desktop) |
| 10 | Chekhlov, Uryasev & Zabarankin (2005), IJTAF 8(1):13–58 | found | Record year 2004 with SSRN DOI 10.2139/ssrn.544742, venue IJTAF; 330 citations. Abstract: CDD is "the mean of the worst (1 − α) * 100% drawdowns", includes maximal and average drawdown as limiting cases, and is "similar to Conditional Value-at-Risk". | [link](https://consensus.app/papers/details/b81e3a221093580dac48d13ea53f3975/?utm_source=claude_desktop) |
| 11 | Busseti, Ryu & Boyd (2016), *Risk-constrained Kelly gambling*, arXiv:1603.06183 | found (journal version) | *The Journal of Investing*, 2016, DOI 10.3905/joi.2016.25.3.118; 33 citations. **Add the journal version.** Abstract: a bound on drawdown probability yields a convex problem that "guarantees the drawdown risk constraint holds"; the bound is "reasonably close" to Monte Carlo drawdown risk in their experiments; the bets beat fractional Kelly at equal drawdown risk. The abstract does not cover payouts or negative-drift settings; see verification R1. | [link](https://consensus.app/papers/details/65435cc4469c5c10aedc8f58cb26c4cd/?utm_source=claude_desktop) |
| 12 | Nemirovski & Shapiro (2006/07), SIAM J. Optim. 17(4):969–996 | found | Record year 2006; DOI 10.1137/050622328; 1,341 citations. The abstract confirms convex conservative approximations whose feasible set lies inside the chance-constrained set, the "Bernstein approximation", and the ambiguous-distribution extension. | [link](https://consensus.app/papers/details/76780e4e76ac5c4ab0506a9ce75abc8d/?utm_source=claude_desktop) |
| 13 | Campi & Garatti (2008), SIAM J. Optim. 19(3):1211–1230 | not checked (quota) | Crossref match per the verification log. | — |
| 14 | Calafiore & Campi (2006), IEEE TAC 51(5):742–753 | found (stream 06 record) | DOI 10.1109/tac.2006.875041; 1,293 citations. Per stream 06, the abstract confirms an explicit sample-size bound. | [link](https://consensus.app/papers/details/6d4c42eea34d5c029d37a6e6102f72fa/?utm_source=claude_desktop) |
| 15 | Brown & Sim (2009), *Satisficing measures for analysis of risky positions*, MS 55(1):71–84 | found | Record year 2008 (online-first); DOI 10.1287/mnsc.1080.0929; 161 citations. The abstract confirms "dual to classes of risk measures", aspiration levels "much more natural to specify than risk tolerance parameters", and the ambiguity interpretation. | [link](https://consensus.app/papers/details/d3ae1fd6ec47539dba922af9c3f4308f/?utm_source=claude_desktop) |
| 16 | Chen & Sim (2009), *Goal-driven optimization*, OR 57(2):342–357 | found | DOI 10.1287/opre.1080.0570; 115 citations. The abstract confirms "maximizes the shortfall-aware aspiration-level criterion", subproblems "evaluated under the popular conditional-value-at-risk (CVaR) measure", and the SOCP decision-rule approximation. | [link](https://consensus.app/papers/details/dda9dcf544fc56e2bb6337ff4fe2424d/?utm_source=claude_desktop) |
| 17 | Long, Sim & Zhou (2023), *Robust satisficing*, OR 71(1):61–82 | found via WebSearch (not returned by Consensus) | A targeted Consensus query returned the follow-on *The Analytics of Robust Satisficing* (Sim et al. 2021) but not this paper. WebSearch (IDEAS/RePEc) gives OR 71(1):61–82, 2023, DOI 10.1287/opre.2021.2238, matching the dossier. | — (related record: [Sim et al. 2021](https://consensus.app/papers/details/d3fc5f3a81a2553097712b50a12ff714/?utm_source=claude_desktop)) |
| 18 | Esfahani & Kuhn (2018), Math. Prog. 171:115–166 | found (stream 01/09 record) | **Surname: Mohajerin Esfahani.** Full title: "Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations". DOI 10.1007/s10107-017-1172-1; 2,274 citations (stream 09). | [link](https://consensus.app/papers/details/955158b8081d595c9c09458e32f6c2c0/?utm_source=claude_desktop) |
| 19 | Shapiro (2009), ORL 37(3):143–147 | found | DOI 10.1016/j.orl.2009.02.005; 191 citations. Abstract: time consistency is "approached from an optimization point of view ... optimality of a decision policy should not involve states which cannot happen in the future". | [link](https://consensus.app/papers/details/b966f75799a75d31853788b4acb559a6/?utm_source=claude_desktop) |
| 20 | Ruszczyński (2010), Math. Prog. 125(2):235–261 | not checked (quota) | Crossref match per the verification log. | — |
| 21 | Philpott & de Matos (2012), EJOR 218(2):470–483 | found | DOI 10.1016/j.ejor.2011.10.056; 267 citations. The abstract confirms a time-consistent coherent risk measure inside an SDDP-type algorithm, applied to New Zealand hydro-thermal scheduling. | [link](https://consensus.app/papers/details/7bcb639f52af5a5298f60b6bd44f8d0d/?utm_source=claude_desktop) |
| 22 | Boyd et al. (2017), *Multi-period trading via convex optimization*, arXiv:1705.00109 | found (stream 01 record) | *Foundations and Trends in Optimization*, DOI 10.1561/2400000023. **Add the journal version.** | [link](https://consensus.app/papers/details/86cb196ea5dc58bba999226d0954af0c/?utm_source=claude_desktop) |
| 23 | Ang, Papanikolaou & Westerfield (2014), *Portfolio choice with illiquid assets*, MS; NBER w19436 | found (stream 01/09 record) | DOI 10.1287/mnsc.2014.1986; 171 citations. Per stream 09, the abstract confirms "forgo 2% of their wealth". **Add 60(11):2737–2761** (verification log). | [link](https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop) |
| 24 | Gourier, Phalippou & Westerfield (2024), *Capital commitment*, JF 79(5):3407–3457 | found | My search returned the 2014 working paper under its earlier title, *Capital Commitment and Illiquidity Risks in Private Equity* (Phalippou et al., 1 citation). Its abstract puts the many-fund commitment-risk welfare premium at the equivalent of "1:63% per annum" (sic, i.e., 1.63%). Stream 04 retrieved the *Capital Commitment* record (SSRN DOI 10.2139/ssrn.2490430), whose abstract supports the dossier's claim about paying to adjust committed quantities. WebSearch confirms JF 79(5):3407–3457, DOI 10.1111/jofi.13382. | [WP record](https://consensus.app/papers/details/9b5881d8cef05dffa4a40423d6b15bc8/?utm_source=claude_desktop); [stream 04 record](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop) |
| 25 | Brown, Dimmock, Kang & Weisbenner (2014), AER 104(3):931–962 | found (stream 02 record) | Full title "How University Endowments Respond to Financial Market Shocks: Evidence and Implications"; DOI 10.1257/aer.104.3.931; 119 citations. | [link](https://consensus.app/papers/details/7831f601f303581cb3e87906847e0fab/?utm_source=claude_desktop) |
| 26 | Avanzi (2009), *Strategies for dividend distribution: a review*, NAAJ 13(2):217–251 | not checked (quota) | Crossref match per the verification log. | — |

**Totals:** 26 rows · 20 confirmed (12 by this stream's searches, 7 through sibling-stream Consensus records, 1 by WebSearch only) · 0 mismatched · 0 not found · 6 not checked.

**Incidental corroboration (not counted):**
- *Dybvig (1995).* [Watson & Scott (2012)](https://consensus.app/papers/details/0a95294d002158cfab81b379c4e530bc/?utm_source=claude_desktop) write that "Dybvig [1995] finds optimal spending and investment strategies for a perpetual endowment that has no tolerance for spending declines. His spending rule is a ratchet". This is consistent with dossier §2.2. Stream 02 found the RES record itself ([link](https://consensus.app/papers/details/748fe37345405ad99e884e16ca31c814/?utm_source=claude_desktop)).
- *Not checked and not load-bearing:* Browne (1999, F&S), Nielsen (2013), Das, Markowitz, Scheid & Statman (2010), Kahneman & Tversky (1979), Artzner et al. (1999), Rockafellar & Uryasev (2002), Charnes & Cooper (1959), Roy (1952), Leibowitz & Henriksson (1989), Kelly (1956), Glasserman & Xu (2014), Hansen & Sargent (2001), Ruszczyński & Shapiro (2006), Pereira & Pinto (1991, found by stream 01), Tasche (2007), Wabersich & Zeilinger, Ames et al., Abate et al. (2008), Gerber & Shiu (1998), Tobin (1974, found by stream 02), Merton (1993, web-confirmed by streams 02 and 03), Constantinides (1990, found by stream 02), Grossman–Zhou's companions Cvitanić & Karatzas (1995, dossier ⚠) and Brunel (book, dossier ⚠).

---

## 3. Annotated bibliography (25 papers)

None of the 25 is cited by the dossier. Dossier-cited works are verified in §2. Entries are grouped by the design question they inform. Several illiquidity and sovereign papers that bear on this stream are already annotated by streams 01–05 and 09; they are listed in §4.7 rather than repeated here.

### A. The target term: pursuing 10% without gambling (IC)

**1. [Hedging goals](https://consensus.app/papers/details/c7d8bb6499c75f8e93935fa3a567584b/?utm_source=claude_desktop)**
- T. Krabichler et al. · record year 2021 (DOI indicates 2023) · *Financial Markets and Portfolio Management* · 1 citation · DOI 10.1007/s11408-023-00437-y
- *Finding:*
  - Extends Browne's (1999) link between goal-based investing and option hedging to varying risk aversion, using lower partial moments of different orders.
  - Maximizing the probability of reaching the goal (quantile hedging) and minimizing the expected shortfall below the goal (efficient hedging, Föllmer & Leukert 2000) "yield, in fact, the same optimal investment policy".
  - Offers a model-free reinforcement-learning approach that handles transaction costs.
- *Relevance to ADIC:* The dossier's default target-shortfall exponent is α = 2, but its IC sweep is α ∈ [1, 3] (§6.5), and §3.1 groups "Fishburn α ≥ 1" together.
  - **[Inference]** A target term with α = 1, expected shortfall below 10%, can reproduce the digital P-max policy. The sweep should start above 1, for example 1.5–3.
  - The RL route is a candidate for the agentic layer where frictions such as secondary discounts and fees make DP intractable.

**2. [A Continuous Time Framework for Sequential Goal-Based Wealth Management](https://consensus.app/papers/details/0fd71f5302ce52aead087822575e14e4/?utm_source=claude_desktop)**
- Agostino Capponi et al. · 2024 · *Management Science* · 8 citations · DOI 10.1287/mnsc.2022.02047
- *Finding:*
  - Sequential goals with a stochastic factor driving asset prices, goal amounts and income.
  - It is optimal to fund an expiring goal "up to the level where the marginal benefit of additional fundedness is exceeded by the opportunity cost of diverting wealth from future goals".
  - An all-or-nothing investor is more risk averse toward an approaching deadline if well funded, but more risk seeking if not on track, compared with an investor with flexible goals.
- *Relevance to ADIC:* Annual distributions are a sequence of goals with deadlines.
  - **[Inference]** Treat the 5% minimum as the all-or-nothing goal protected by C1, and top-ups as flexible goals. Flexibility dampens deadline gambling.
  - The funding rule answers a Treasurer question directly: how much of next year's payout to pre-fund in HQLA now, versus leaving it invested for later goals.

**3. [Dynamic optimization for multi-goals wealth management](https://consensus.app/papers/details/43df8dac96315454964d76f776c59bd5/?utm_source=claude_desktop)**
- Sanjiv R. Das et al. · 2021 · *Journal of Banking & Finance* · 20 citations · DOI 10.1016/j.jbankfin.2021.106192
- *Finding:*
  - Dynamic programming over multiple, potentially competing goals, each all-or-nothing or partially fulfillable. The method chooses which goals to fulfil and the portfolio.
  - It computes the probability of attaining each goal under the optimal policy, and "vastly outperforms" static strategies and target-date funds.
- *Relevance to ADIC:*
  - **[Inference]** A ready template for the dossier's L3 low-dimensional DP diagnostics. Goals would be each year's minimum distribution, each year's top-up, and the 10-year aspiration. Per-goal attainment probabilities are IC-readable KPIs.
  - Goal values must be concave in shortfall, or the method inherits the gambling issue (see entry 1).

**4. [Fund Success and Assurance Frontiers](https://consensus.app/papers/details/f9145b920f6b5c39bb9b2fbec424c295/?utm_source=claude_desktop)**
- Martin L. Leibowitz et al. · 2021 · venue label "Unknown Journal" (DOI indicates *Journal of Portfolio Management*) · 0 citations · DOI 10.3905/jpm.2021.1.294
- *Finding:*
  - A portfolio whose expected return just matches a fund's target gives only a 50/50 chance of success.
  - The authors map the efficient frontier into an "assurance frontier": risk-adjusted returns achievable with a specified probability, such as 60%.
  - The frontier's peak can lie well short of the fund's maximum risk limit. Longer horizons generally raise the peak.
- *Relevance to ADIC:*
  - **[Inference]** "The return we can assure with 60 / 75 / 90% confidence at each risk level" is a frontier the IC can read without making P(10%) the objective.
  - It makes visible that a 10% target is a median-type statement, consistent with dossier §2.5's horizon arithmetic.

**5. [Personalized goal-based investing via multi-stage stochastic goal programming](https://consensus.app/papers/details/f03987fc1a23597e921e27887e9a71fc/?utm_source=claude_desktop)**
- Woo Chang Kim et al. · 2019 · *Quantitative Finance* · 31 citations · DOI 10.1080/14697688.2019.1662079
- *Finding:* A goal-based model in which each goal gets a priority level. A sequential approach maximizes the probability of higher-priority goals unaffected by lower-priority ones, and the whole model is a linear program.
- *Relevance to ADIC:*
  - **[Inference]** If the IC insists on the deck's strict ordering (distributions first, 10% second), it is implementable as a sequence of LPs.
  - The dossier's ε-constraint sweeps remain preferable, because they expose the price of each priority.

### B. Time consistency and pre-commitment (IC; optimizer)

**6. [Multiperiod Mean Conditional Value at Risk Asset Allocation: Is It Advantageous to Be Time Consistent?](https://consensus.app/papers/details/f1547b977f055cdb8efcd20b57857a68/?utm_source=claude_desktop)**
- P. Forsyth · 2020 · *SIAM Journal on Financial Mathematics* · 23 citations · DOI 10.1137/19m124650x. The full abstract is on the [SSRN record](https://consensus.app/papers/details/3c7122fd5d6c5df7a3b78d0d01044106/?utm_source=claude_desktop) (2019, 16 citations, DOI 10.2139/ssrn.3340194).
- *Finding:*
  - Formulates the multi-period, time-consistent mean-CVaR problem with realistic constraints (no shorting, no leverage, discrete rebalancing) for a 30-year DC investor.
  - Adding the time-consistency constraint "compares unfavourably with the pure pre-commitment strategy".
  - The time-zero pre-commitment strategy "is identical to a time consistent strategy based on an alternative objective function", so it is implementable: "it would seem that there is little to be gained from enforcing time consistency".
- *Relevance to ADIC:* This challenges dossier §1 item 4 and §2.5.
  - **[Inference]** The IC's per-cycle pre-commitment (dossier §6.9 rule 6) can be formalized as this induced objective: fix the time-zero CVaR threshold and carry it as a state, so that rolling re-solves do not drift.
  - Caveat: a DC setting with no illiquid assets or liabilities.

**7. [Discrete-time mean-CVaR portfolio selection and time-consistency induced term structure of the CVaR](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop)**
- M. Strub et al. · 2019 · *Journal of Economic Dynamics and Control* · 46 citations · DOI shown 10.2139/ssrn.3040517 (SSRN)
- *Finding:*
  - Solves the time-inconsistent discrete-time mean-CVaR problem in an incomplete market by embedding it in a family of time-consistent expected-utility problems with piecewise-linear utility.
  - The cumulated risky investment is V-shaped in current wealth. The mean-CVaR frontier is a straight line.
  - A pre-committed mean-CVaR investor "behaves like a naive mean-CVaR investor with a time-increasing confidence level for the CVaR".
- *Relevance to ADIC:* **[Inference]**
  - Implement pre-commitment as a schedule of confidence levels ε_t rather than a constant ε.
  - V-shaped exposure, with risk rising as wealth falls below a threshold, is a signature to add to the dossier's §6.9 gambling detector.
  - The piecewise-linear embedding fits the dossier's LP/SOCP layer (L2).

**8. [Multiperiod Mean-Buffered Probability of Exceedance in Defined Contribution Portfolio Optimization](https://consensus.app/papers/details/50e851a2565f56639dabd7b0045072f5/?utm_source=claude_desktop)**
- D. Dang et al. · 2025 · *SIAM Journal on Financial Mathematics* · 5 citations (recent) · DOI 10.1137/25m1764773. Also annotated by stream 01.
- *Finding:*
  - Proposes buffered probability of exceedance (bPoE) as a "more intuitive, dollar-based alternative" to CVaR.
  - Precommitment mean-bPoE and mean-CVaR are equivalent through a one-to-one correspondence of scalarization optimal sets. No such equivalence holds in the time-consistent setting.
  - Time-consistent mean-bPoE strategies "closely resemble their precommitment counterparts", unlike time-consistent mean-CVaR, "which often leads to counterintuitive control behavior".
- *Relevance to ADIC:*
  - **[Inference]** Report the distribution-reliability constraint C1 as a buffered probability. The standard identity is bPoE_z(X) ≤ ε ⇔ CVaR_{1−ε}(X) ≤ z; it is not stated in these abstracts. So bPoE of the 5-year path-maximum deficit at zero is the probability-form reading of the dossier's CVaR constraint.
  - This gives the IC a coherent "probability" that also behaves well under re-solving.

**9. [Risk aversion in multistage stochastic programming: A modeling and algorithmic perspective](https://consensus.app/papers/details/6f373cedc1b15e7a817aa5179d898986/?utm_source=claude_desktop)**
- Tito Homem-de-Mello et al. · 2016 · *European Journal of Operational Research* · 108 citations · DOI 10.1016/j.ejor.2015.05.048
- *Finding:*
  - There is "no consensus on the best way" to put risk measures into multistage programs.
  - Nesting one-step risk measures ensures consistency but "has drawbacks from the algorithmic viewpoint".
  - Proposes expected conditional risk measures (ECRMs), illustrated on a defined-benefit pension problem.
  - [Khatami et al. (2024)](https://consensus.app/papers/details/7876295629a95b549b99348a7160d4c9/?utm_source=claude_desktop) add that ECRMs are time-consistent and that solving them costs the same as the risk-neutral problem.
- *Relevance to ADIC:* **[Inference]** If the dossier's optional full time-consistency layer is built (risk-averse SDDP with nested CVaR, §7), ECRMs are the cheaper alternative and avoid nested CVaR's interpretability problems.

**10. [Time-inconsistent multistage stochastic programs: Martingale bounds](https://consensus.app/papers/details/9fb02745a50d5d0eb3d6805a301fe5ed/?utm_source=claude_desktop)**
- G. Pflug et al. · 2016 · *European Journal of Operational Research* · 57 citations · DOI 10.1016/j.ejor.2015.02.033
- *Finding:*
  - Programs with Average Value-at-Risk at the final stage are not time consistent.
  - With risk parameters at a random level and an extended state space, the optimal value function evolves as a martingale and a dynamic programming principle applies. The risk profile "has to be accepted to vary over time".
- *Relevance to ADIC:* This refines dossier §2.5, which says CVaR of terminal wealth is "generally not" time-consistent.
  - **[Inference]** A terminal CVaR term, such as C4's 10-year CVaR floor, can be handled consistently by carrying the risk level as a state, provided the IC accepts a risk appetite that moves with outcomes.

**11. [On robust multi-period pre-commitment and time-consistent mean-variance portfolio optimization](https://consensus.app/papers/details/69bbf500ffbd50a9a76bc42c7714fc51/?utm_source=claude_desktop)**
- F. Cong et al. · 2017 · *International Journal of Theoretical and Applied Finance* · 11 citations · DOI 10.1142/s0219024917500492
- *Finding:*
  - Compares robust pre-commitment and time-consistent mean-variance strategies.
  - The time-consistent strategy "is more stable when possible incorrect assumptions regarding the future asset development are modeled".
  - In some situations it even generates higher efficient frontiers than pre-commitment, because "the time-consistency restriction appears to protect an investor".
- *Relevance to ADIC:* A counterweight to entry 6. Under model uncertainty, which dossier §8 calls ADIC's dominant risk, time-consistent or rolling rules can be the more robust choice.
  - **[Inference]** Evaluate both families across the model-variant set 𝓜 before choosing.

### C. Risk limits: static or dynamic, VaR or ES, and incentives (Treasurer; Overlay; agents)

**12. [Optimal Dynamic Trading Strategies with Risk Limits](https://consensus.app/papers/details/3904dafe5042536aacf42278cfc299db/?utm_source=claude_desktop)**
- D. Cuoco et al. · 2008 · *Operations Research* · 160 citations · DOI 10.1287/opre.1070.0433
- *Finding:*
  - Earlier negative conclusions about VaR limits "are based on models that are either static or dynamically inconsistent".
  - When the VaR limit is re-evaluated dynamically, "the optimal risk exposure of a trader subject to a VaR limit is always lower than that of an unconstrained trader and ... the probability of extreme losses is also lower".
  - A tail-conditional-expectation (TCE) limit can always be transformed into an equivalent VaR limit, and conversely.
- *Relevance to ADIC:* This qualifies the lesson dossier §2.1 draws from Basak & Shapiro.
  - **[Inference]** Probability-type constraints are acceptable if re-imposed at every decision epoch on the conditional distribution. Examples: P(red recourse) ≤ 1%; 12-month planned-payout reliability. The decisive design choice is dynamic re-evaluation, which dossier §2.5(i) already proposes, rather than the switch to expected shortfall.

**13. [Risk management with expected shortfall](https://consensus.app/papers/details/5bc6b8052fa75c37a94d6cfdd08d70f1/?utm_source=claude_desktop)**
- Pengyu Wei · 2021 · *Mathematics and Financial Economics* · 17 citations · DOI 10.1007/s11579-021-00298-x
- *Finding:*
  - In a dynamic expected-utility model with ES-based risk management, "ES managers can incur larger losses when losses occur, compared to benchmark managers".
  - In equilibrium, ES managers increase market volatility during stress.
  - Proposes "weighted shortfall", a coherent spectral risk measure, as the fix.
- *Relevance to ADIC:* This challenges the implicit remedy in dossier §2.1, Basak & Shapiro's expected-loss alternative.
  - **[Inference]** C4 (worst-model CVaR₉₀ of the 10-year return ≥ 0), if evaluated at a fixed horizon, could itself induce risk-taking in bad states.
  - Make C4 rolling, consider spectral weights, and add this case to the gambling detector.

**14. [Risk managing tail-risk seekers: VaR and expected shortfall vs S-shaped utility](https://consensus.app/papers/details/15341dccf86d5ae59b3ced24ab1c5890/?utm_source=claude_desktop)**
- J. Armstrong et al. · 2019 · *Journal of Banking & Finance* · 30 citations · DOI 10.1016/j.jbankfin.2019.01.010
- *Finding:*
  - Tail-risk-seeking players with S-shaped (Kahneman–Tversky) utility attain "the same supremum of expected utility with or without VaR or ES limits".
  - Constraints based on a second, conventional concave utility can reduce the S-shaped utility achievable.
  - A companion paper ([Armstrong et al., *Annals of OR*](https://consensus.app/papers/details/bc82c9e7083458bb9cafb259380dbc6b/?utm_source=claude_desktop)) finds dynamic risk constraints effective "provided that the risk control policy is sufficiently strict relative to the Sharpe ratio", but possibly ineffective "if the trader has access to a derivatives market".
- *Relevance to ADIC:* Applies to the Overlay's opportunistic book, and to any agent whose incentives are asymmetric.
  - **[Inference]** The safety filter (dossier §6.7) should include a concave-utility or convex-penalty expected-loss limit on the opportunistic book, not VaR or ES alone, because that book trades derivatives.

### D. Chance constraints and robustness for distribution reliability (Treasurer)

**15. [Distributionally robust joint chance constraints with second-order moment information](https://consensus.app/papers/details/8c13b90032cc5aa1a538b69b775db3c7/?utm_source=claude_desktop)**
- Steve Zymler et al. · record year 2011 · *Mathematical Programming* · 683 citations · DOI 10.1007/s10107-011-0494-7
- *Finding:*
  - Tractable SDP approximations for distributionally robust individual and joint chance constraints, given first and second moments and support.
  - For individual constraints with concave or quadratic functions, the worst-case CVaR approximation is exact.
  - For joint constraints it is "provably tighter than two popular benchmark approximations", and "essentially exact when the scaling parameters are chosen optimally" (tuned by sequential convex optimization). The example is water-reservoir control.
- *Relevance to ADIC:* C1 is a joint chance constraint over a 5-year path of liquidity deficits.
  - **[Inference]** Use a scaled worst-case CVaR across periods instead of splitting ε by the union bound (dossier §2.3). This recovers much of the conservatism that ε/H throws away.

**16. [From CVaR to Uncertainty Set: Implications in Joint Chance-Constrained Optimization](https://consensus.app/papers/details/793e74a285405a7c803b29f7fd3b8246/?utm_source=claude_desktop)**
- Wenqing Chen et al. · 2010 · *Operations Research* · 360 citations · DOI 10.1287/opre.1090.0712
- *Finding:*
  - Tractable robust approximations of individual chance constraints connect to bounds on CVaR.
  - For joint chance constraints, a new formulation "improves upon the standard approach" and is "applicable even if the constraints are correlated".
- *Relevance to ADIC:* **[Inference]**
  - The robust-optimization route to the same goal as entry 15.
  - It links CVaR constraints to uncertainty sets, which connects C1 (CVaR) with C2 (polyhedral named-stress set) in one framework.

**17. [ALSO-X and ALSO-X+: Better Convex Approximations for Chance Constrained Programs](https://consensus.app/papers/details/921da370fcd4548aa53a54c681f6ec35/?utm_source=claude_desktop)**
- Nan Jiang et al. · record year 2020 · *Operations Research* · 46 citations · DOI 10.1287/opre.2021.2225
- *Finding:*
  - CVaR has "been known to be the best" convex inner approximation of chance constraints "for more than a decade".
  - When uncertain constraints are convex in the decisions, ALSO-X "always outperforms the CVaR approximation".
  - The paper gives sufficient conditions for exact recovery, an alternating-minimization enhancement (ALSO-X+), and an extension to distributionally robust chance constraints under ∞-Wasserstein ambiguity.
- *Relevance to ADIC:* Dossier §8 worries that over-tight surrogates make the feasible set look empty.
  - **[Inference]** ALSO-X is a drop-in, less conservative replacement for the CVaR surrogate in C1 and C2 within the L2 LP layer.

**18. [On approximations of data-driven chance constrained programs over Wasserstein balls](https://consensus.app/papers/details/f69feb9051595f6e85764edfdd18d6c3/?utm_source=claude_desktop)**
- Zhi Chen et al. · record year 2022 · *Operations Research Letters* · 74 citations · DOI 10.1016/j.orl.2023.02.008
- *Finding:*
  - Compares three approximations of distributionally robust chance constraints over Wasserstein balls: a CVaR bound, Bonferroni decoupling, and an expected-violation bound.
  - The CVaR approximation is a tight convex approximation.
  - All three "can perform arbitrarily poorly in data-driven settings" and are generally incomparable.
- *Relevance to ADIC:* **[Inference]** Validate every surrogate by out-of-sample simulation, as dossier §8 already advises. Report surrogate slack against the simulated breach frequency as a rubric check.

**19. [On the Equivalence and Performance of Distributionally Robust Optimization and Robust Satisficing Models](https://consensus.app/papers/details/97d781784f8953ec915e053f62c18c68/?utm_source=claude_desktop)**
- Zhiyuan Wang et al. (co-authors include L. Ran and M. Zhou per the funding note) · 2025 · *Manufacturing & Service Operations Management* · 3 citations (recent) · DOI 10.1287/msom.2023.0531
- *Finding:*
  - Under the Wasserstein metric with a risk-aware convex objective, DRO and robust satisficing (RS) "share the same solution family".
  - A correspondence between the DRO radius and the RS target makes the optimal solutions coincide. The equivalence extends to the globalized versions.
  - Practical performance can still differ "depending on how the model parameters are selected"; cross-validation helps.
- *Relevance to ADIC:* This qualifies dossier §2.4.
  - **[Inference]** The fragility index κ (RS) and an ambiguity radius (DRO) are two parameterizations of one family. The IC sets the target τ; the system reports the implied radius; the challenge agent tunes it by cross-validation over model variants.

### E. Growth with downside control, and drawdown with payouts (IC; optimizer)

**20. [Kelly investing with downside risk control in a regime-switching market](https://consensus.app/papers/details/6510dbe8c3fa55139c8728a4efbfe07c/?utm_source=claude_desktop)**
- L. MacLean et al. · 2021 · *Quantitative Finance* · 7 citations · DOI 10.1080/14697688.2021.1993617. Also a companion entry in stream 06.
- *Finding:*
  - Maximizes growth "while staying above a specified downside wealth threshold with high probability, where shortfalls below the threshold are penalized with a convex function of shortfall".
  - Markov regimes, with lognormal prices within each regime.
  - The optimal strategy has a "modified Kelly format", with regime weights that incorporate the risk control.
- *Relevance to ADIC:* **[Inference]**
  - The closest published analogue to the dossier's SSG objective.
  - It offers a replacement for the C3 RCK constraint (verification R1): a convex penalty on shortfall below a threshold path. The path can be set to decline with the payout, so positive real drift net of distributions is not required.
  - Its regime-specific Kelly fractions map onto the dossier's HMM regime posterior.

**21. [Dynamic growth-optimal portfolio choice under risk control](https://consensus.app/papers/details/9de16903a7c554e0aa49029e121504a8/?utm_source=claude_desktop)**
- Pengyu Wei et al. · 2024 · *European Journal of Operational Research* · 1 citation (recent) · DOI 10.1016/j.ejor.2024.10.043
- *Finding:*
  - A growth-optimal portfolio problem with risk on log-returns measured by weighted VaR, which generalizes VaR and ES.
  - "Using VaR increases losses while ES reduces losses during market downturns."
  - The efficient frontier is a concave curve linking the minimum-risk portfolio to the growth-optimal portfolio. When the risk measure is applied to terminal wealth, it is a vertical line instead. The concave frontier "aids investors in setting reasonable investment targets".
- *Relevance to ADIC:* This supports the dossier's choice to measure target shortfall on log returns.
  - **[Inference]** The growth–risk frontier is an IC tool for setting the 10% aspiration consistently with risk appetite. ES, not VaR, should carry the log-return risk term.

**22. [Optimal investment to minimize the probability of drawdown](https://consensus.app/papers/details/830207da0a945981bfed4cc78b27e992/?utm_source=claude_desktop)**
- Bahman Angoshtari et al. · record year 2015 · *Stochastics* · 24 citations · DOI 10.1080/17442508.2016.1155590
- *Finding:* The optimal Black–Scholes investment strategy to minimize the probability that portfolio value reaches a fixed proportion of its running maximum, when the portfolio pays out a deterministic function of its value: "as might be the case for an endowment fund paying at a specified rate, for example, at a constant rate or at a rate that is proportional to the fund's value".
- *Relevance to ADIC:* **[Inference]**
  - An analytic benchmark for testing the simulator's drawdown-with-payout code.
  - It shows the IC how the payout form (fixed dollars versus % of NAV) changes optimal risk.
  - It also gives correct drawdown language for verification R2: peak-relative drawdown is a different event from falling below a fraction of initial wealth.

**23. [Portfolio optimisation under non-linear drawdown constraints in a semimartingale financial model](https://consensus.app/papers/details/5be6a6aabe4059f5aaa91bb3176069cb/?utm_source=claude_desktop)**
- V. Cherny et al. · record year 2011 (DOI indicates 2013) · *Finance and Stochastics* · 40 citations · DOI 10.1007/s00780-013-0209-4
- *Finding:*
  - Maximizes the long-term growth rate of expected utility subject to a drawdown constraint, as in Grossman & Zhou, in a general semimartingale market with general utilities and drawdown functions.
  - The problem "is in fact equivalent to an unconstrained problem with a suitably modified utility function". Value function and policy are explicit in terms of the unconstrained ones.
- *Relevance to ADIC:* **[Inference]** Drawdown control can be embedded in the objective as a utility modification instead of a conservative surrogate. This is a route around both the C3 infeasibility (R1) and the conic-program problem with the TWR term (R5).

### F. Payout-rule economics (Treasurer; IC; owner)

**24. [Portfolio Choice with Sustainable Spending: A Model of Reaching for Yield](https://consensus.app/papers/details/b029ce8a702156d8bc5e5d2fde4d3409/?utm_source=claude_desktop)**
- J. Campbell et al. · record year 2020 · *Journal of Financial Economics* · 54 citations · DOI shown 10.2139/ssrn.3527179 (SSRN). Also annotated by stream 02.
- *Finding:*
  - Reaching for yield (more risk when the real rate falls while the risk premium is constant) "results from imposing a sustainable spending constraint on an otherwise standard infinitely lived investor with power utility".
  - The effect intensifies when rates start low, and can change the sign of the response to the risk premium.
  - With a nominal sustainability constraint, low inflation also encourages risk-taking.
- *Relevance to ADIC:* The dossier's sustainability metric is real NAV net of distributions, and the payout band is nominal.
  - **[Inference]** Add the real rate as a state variable. Expect the optimizer to add risk when real rates fall if sustainability is hard-wired as a constraint. Add a reaching-for-yield check to the gambling detector, and treat sustainability as a soft target.

**25. [The 4% strategy revisited: a pre-commitment mean-variance optimal approach to wealth management](https://consensus.app/papers/details/be5936659c2a5006ac12e9527606e1ec/?utm_source=claude_desktop)**
- D. Dang et al. · 2017 · *Quantitative Finance* · 24 citations · DOI 10.1080/14697688.2016.1205211
- *Finding:*
  - Multi-period mean-variance with periodic withdrawals works "effectively [as] a down-side risk measure". Applications: DC decumulation and sustainable withdrawal rates for an endowment.
  - The analysis supports a 4% real withdrawal for pensions and "a somewhat lower rate for an endowment", but only under the MV-optimal allocation, not a fixed-proportion strategy.
  - Against constant proportions, the MV-optimal policy achieves the same expected terminal wealth with a much lower standard deviation and shortfall probability. It is "quite robust" to parameter uncertainty in historical tests.
- *Relevance to ADIC:* **[Inference]**
  - Supports state-dependent allocation in the presence of payouts.
  - Gives a sobering anchor for the 5–10% band, consistent with verification R4's ≈5–6% sustainable payout under current CMAs. The setting differs: real withdrawals, a jump-diffusion stock-bond model, no illiquid assets.

---

## 4. Missed-but-important papers: design implications

### 4.1 State variables (additions to dossier §6.1)
- **Real interest rate and inflation.** Owner: Treasurer and IC.
  - Sustainable-spending constraints make optimal risk depend on the real rate ([Campbell & Sigalov](https://consensus.app/papers/details/b029ce8a702156d8bc5e5d2fde4d3409/?utm_source=claude_desktop)).
  - The same mechanism appears for SWFs: "low real interest rates generate a 'reaching for yield' portfolio behavior" ([Michaelides et al. 2022](https://consensus.app/papers/details/5658a41f33655aeb9301328935c1591c/?utm_source=claude_desktop)).
  - **[Inference]** Without this state, the policy's sensitivity to real rates is invisible.
- **Owner fiscal state and state-dependent distribution demand.** Owner: Treasurer, who pays the distributions.
  - [Bodie & Brière](https://consensus.app/papers/details/848357ab551a580793407efeed637bbb/?utm_source=claude_desktop) derive "a performance-seeking portfolio and three hedging demand terms for the variability of the fiscal surplus and external and domestic debt".
  - [Gintschel & Scherer](https://consensus.app/papers/details/0644f03ab6be5e608a59b751de988332/?utm_source=claude_desktop) find the hedge decision more important than the choice of point on the efficient frontier.
  - [Lindset & Mork](https://consensus.app/papers/details/0c6e0c115ef95a64a46a430cf506d3e4/?utm_source=claude_desktop) find that the desire for smooth taxes and public services "translates into smoothing of SWF draws and lower risk taking".
  - Stream 03 covers this literature in depth. **[Inference]** It formalizes dossier §2.6's wrong-way-risk hypothesis. The project context does not state the owner's revenue mix, so this needs owner data.
- **Pre-commitment memory.** Owner: optimizer.
  - Carry the time-zero CVaR threshold, or the induced wealth target, as a state so that rolling re-solves honour the IC's commitment ([Forsyth](https://consensus.app/papers/details/f1547b977f055cdb8efcd20b57857a68/?utm_source=claude_desktop); [Strub et al.](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop); [Pflug & Pichler](https://consensus.app/papers/details/9fb02745a50d5d0eb3d6805a301fe5ed/?utm_source=claude_desktop)). **[Inference]**
- **Distribution memory.** Owner: Treasurer.
  - If a drawdown-on-distributions rule is adopted, the running maximum of distributions becomes a state ([Jeon et al. 2021](https://consensus.app/papers/details/3aaa8dfc3d295ab7a916910f9cf9c8ec/?utm_source=claude_desktop), generalizing Arun's drawdown constraint on consumption).
  - Under a soft-floor objective, the state is the gap to the norm ([Mork et al., JEDC](https://consensus.app/papers/details/62dbecedd3f75999bcf3364f3ba3f122/?utm_source=claude_desktop)).
  - The dossier lists "ratchet level" but not these alternatives.
- **Liquidity ladder.** Owner: private-markets groups.
  - Per-holding lock-up or expected-exit date, and a regime-dependent liquidation cost: in [Dimmock, Wang & Yang](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop) liquidity diversification across staggered lockups raises both alternatives allocations and welfare, and crisis illiquidity pushes holdings far from targets.
  - **[Inference]** Split the Secondaries hybrid book into two sub-books, fund-LP commitments and direct secondaries. They have different call and distribution intensities, and direct deals carry deferred-payment liabilities.

### 4.2 Models
- **MPC for commitment dynamics.** [Luxenberg et al. (ICAIF 2022)](https://consensus.app/papers/details/e63add9e25485ea691994d7731b433b1/?utm_source=claude_desktop) model illiquid positions as "a random linear system" and use convex MPC with the requirement "that we can meet the capital calls, with very high probability, with our liquid assets". Their policy performs close to a fully liquid benchmark.
  - It uses the same cvxpy stack as the dossier, and is annotated in streams 01 and 04.
  - **[Inference]** It is the natural L2 template once distributions and overlay margin are added; the abstract excludes external liabilities but says the method "is readily extended".
- **A baseline pacing rule.** In [de Zwart et al. (FAJ 2012)](https://consensus.app/papers/details/63deabfca2f15e65880fa9a8f5d03a13/?utm_source=claude_desktop), new commitments equal distributions received plus uncalled capital, scaled by target over current allocation. This held 86% of target with an 8% chance of being overinvested, and needed about 30% overcommitment during build-up.
  - **[Inference]** Use it as the explainable benchmark that L1 policy search must beat. The figures come from 1980–2005 Thomson VE data, not ADIC.
- **Objective template.** A regime-aware modified Kelly with a convex shortfall penalty below a threshold ([MacLean et al. 2021](https://consensus.app/papers/details/6510dbe8c3fa55139c8728a4efbfe07c/?utm_source=claude_desktop)). **[Inference]** It implements SSG with the dossier's regime posterior.
- **Distributions as sequential goals.** Treat them as goals with partial fulfilment for L3 diagnostics ([Capponi et al.](https://consensus.app/papers/details/0fd71f5302ce52aead087822575e14e4/?utm_source=claude_desktop); [Das et al. 2021](https://consensus.app/papers/details/43df8dac96315454964d76f776c59bd5/?utm_source=claude_desktop)).
- **Embedding for the LP layer.** The time-inconsistent mean-CVaR problem becomes a family of time-consistent piecewise-linear-utility problems ([Strub et al.](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop)). **[Inference]** This fits the L2 LP layer directly.
- **Analytic checks for the simulator.**
  - [Angoshtari et al.](https://consensus.app/papers/details/830207da0a945981bfed4cc78b27e992/?utm_source=claude_desktop): drawdown probability with an endowment-type payout.
  - [Élie & Touzi](https://consensus.app/papers/details/7af6963baf0d5fd08963d227269b5a4e/?utm_source=claude_desktop): closed-form consumption and investment under a drawdown constraint.
  - [Cherny & Obłój](https://consensus.app/papers/details/5be6a6aabe4059f5aaa91bb3176069cb/?utm_source=claude_desktop): the equivalence between a drawdown constraint and a modified utility.

### 4.3 Parameters and calibration priors (literature values, not ADIC data)
- **Target-shortfall exponent α:** IC sweep 1.5–3, excluding 1; default 2 ([Krabichler et al.](https://consensus.app/papers/details/c7d8bb6499c75f8e93935fa3a567584b/?utm_source=claude_desktop)).
- **Confidence schedule:** a rising ε_t schedule rather than a constant ε when re-solving under pre-commitment ([Strub et al.](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop)). **[Inference]**
- **Payout anchors.**
  - Sustainable endowment withdrawals are "somewhat lower" than 4% real, and only under the optimal dynamic allocation ([Dang, Forsyth & Vetzal](https://consensus.app/papers/details/be5936659c2a5006ac12e9527606e1ec/?utm_source=claude_desktop)).
  - Withdrawals matching expected returns still deplete the fund eventually, and "lower withdrawal rates help sustainability more fundamentally" than risk reduction ([Mork et al., IJFS 2022](https://consensus.app/papers/details/c93456144b3e598bbe6aa9eb8ae9d5d8/?utm_source=claude_desktop)).
  - **[Inference]** The payout rate is the primary sustainability lever. Lead with ≈5–6%, consistent with verification R4.
- **Illiquidity risk aversion γ.** The effect is model-dependent:
  - welfare losses are "negligible" when PE and stocks are close substitutes ([Buchner 2012](https://consensus.app/papers/details/4b82de353e7f5ab39a2937994c2aafe2/?utm_source=claude_desktop));
  - PE allocations are "not monotonically declining in risk aversion" ([Giommetti & Jørgensen](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop));
  - the commitment-risk premium rises to about 1.63% a year with many funds (Gourier et al. working paper, §2 row 24).
  - **[Inference]** Calibrate γ by simulating ADIC's own book rather than citing Ang et al. alone.
- **Tail-estimation sample size.** Expected shortfall "requires a larger sample size than VaR to provide the same level of accuracy" ([Yamai & Yoshiba 2005](https://consensus.app/papers/details/e1406753808953b59a6312393343fa52/?utm_source=claude_desktop)).
  - **[Inference]** Re-check the dossier's 50k-path budget for CVaR at the 0.2%-a-year reliability level; importance sampling is likely needed.

### 4.4 Constraints
- **C1, joint distribution reliability.** Owner: Treasurer.
  - Use a scaled worst-case CVaR ([Zymler et al.](https://consensus.app/papers/details/8c13b90032cc5aa1a538b69b775db3c7/?utm_source=claude_desktop)) or the joint formulation of [Chen et al. 2010](https://consensus.app/papers/details/793e74a285405a7c803b29f7fd3b8246/?utm_source=claude_desktop), instead of union-bound splitting.
  - Try ALSO-X to reduce conservatism ([Jiang & Xie](https://consensus.app/papers/details/921da370fcd4548aa53a54c681f6ec35/?utm_source=claude_desktop)).
  - A Wasserstein-robust C1 "can be reformulated as a conditional value-at-risk constrained optimization problem" ([Xie](https://consensus.app/papers/details/5edbc7b0218d5add938d96ea7faef333/?utm_source=claude_desktop)).
  - Validate by simulation ([Chen, Kuhn & Wiesemann](https://consensus.app/papers/details/f69feb9051595f6e85764edfdd18d6c3/?utm_source=claude_desktop)).
  - **[Inference]** Keep the ε/H translation only as a communication aid for the IC.
- **C3, replace RCK.**
  - Option 1: a convex shortfall penalty below a payout-consistent threshold path, with regime weights ([MacLean et al. 2021](https://consensus.app/papers/details/6510dbe8c3fa55139c8728a4efbfe07c/?utm_source=claude_desktop)).
  - Option 2: drawdown control through a modified utility ([Cherny & Obłój](https://consensus.app/papers/details/5be6a6aabe4059f5aaa91bb3176069cb/?utm_source=claude_desktop)).
  - Label the result as a floor (fall below a fraction of initial NAV) or as a drawdown (peak-relative); [Angoshtari et al.](https://consensus.app/papers/details/830207da0a945981bfed4cc78b27e992/?utm_source=claude_desktop) treat the peak-relative version with payouts.
  - **[Inference]** This addresses verification R1 and R2.
- **C4, robust floor.**
  - Re-impose it dynamically ([Cuoco et al.](https://consensus.app/papers/details/3904dafe5042536aacf42278cfc299db/?utm_source=claude_desktop)).
  - Consider spectral "weighted shortfall" weights ([Wei 2021](https://consensus.app/papers/details/5bc6b8052fa75c37a94d6cfdd08d70f1/?utm_source=claude_desktop)).
  - **[Inference]** A fixed-horizon C4 risks the ES pathology.
- **C6, payout rule.** Owner: Treasurer, with the IC.
  - Soft floor through a spliced utility: high curvature below the norm, low above ([Mork et al., JEDC](https://consensus.app/papers/details/62dbecedd3f75999bcf3364f3ba3f122/?utm_source=claude_desktop)).
  - Or barrier top-ups above a protected minimum. The MV-with-withdrawals literature finds it optimal to withdraw cash above a wealth threshold: [Dang & Forsyth 2016](https://consensus.app/papers/details/d7845d466a7154c7aab3f347813b48bb/?utm_source=claude_desktop) ("if the portfolio wealth exceeds a threshold, an MV optimal strategy is to withdraw cash") and [Cui et al. 2020](https://consensus.app/papers/details/b5b0f21a8b36504cbbea57d00baff832/?utm_source=claude_desktop). This is consistent with the dossier's de Finetti barrier.
  - Avoid strict ratchets unless the owner mandates them. Under ratcheting, the risky share "fluctuates between 0 and the value of an unconstrained individual" ([Jeon et al. 2018](https://consensus.app/papers/details/b6c025002fa5573a996b38f884696090/?utm_source=claude_desktop)).
- **Capital-call coverage.** Meet calls "with very high probability" from liquid assets ([Luxenberg et al.](https://consensus.app/papers/details/e63add9e25485ea691994d7731b433b1/?utm_source=claude_desktop)). **[Inference]** Make this an explicit Treasurer-owned chance constraint next to C1.
- **Overlay opportunistic book.** Add a concave-utility or expected-loss limit to the VaR/ES limits ([Armstrong & Brigo](https://consensus.app/papers/details/15341dccf86d5ae59b3ced24ab1c5890/?utm_source=claude_desktop)).

### 4.5 Objectives
- **Keep SSG and make it regime-aware.**
  - Regime-weighted Kelly with a downside threshold ([MacLean et al. 2021](https://consensus.app/papers/details/6510dbe8c3fa55139c8728a4efbfe07c/?utm_source=claude_desktop)).
  - Measure risk on log-returns with ES ([Wei et al. 2024](https://consensus.app/papers/details/9de16903a7c554e0aa49029e121504a8/?utm_source=claude_desktop)).
- **bPoE.** Report bPoE for tail statements and optionally optimize it ([Dang et al. 2025](https://consensus.app/papers/details/50e851a2565f56639dabd7b0045072f5/?utm_source=claude_desktop)). **[Inference]** It reads as a probability and stays coherent with C1.
- **Formalize pre-commitment.**
  - Use the induced objective of [Forsyth](https://consensus.app/papers/details/f1547b977f055cdb8efcd20b57857a68/?utm_source=claude_desktop) and [Strub et al.](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop).
  - If a time-consistent multistage risk measure is required, use ECRMs ([Homem-de-Mello & Pagnoncelli](https://consensus.app/papers/details/6f373cedc1b15e7a817aa5179d898986/?utm_source=claude_desktop)) rather than nested CVaR.
  - Compositions of law-invariant coherent risk measures "can be law invariant only for the expectation or max-risk measures" ([Shapiro 2012](https://consensus.app/papers/details/ce5f405a499852bfa63fabe0cd12fd1d/?utm_source=claude_desktop)). **[Inference]** A nested-CVaR number is therefore not the CVaR of any terminal distribution the IC can picture.
- **Owner total-wealth term.** Add a hedging term in the owner's total wealth ([Bodie & Brière](https://consensus.app/papers/details/848357ab551a580793407efeed637bbb/?utm_source=claude_desktop)). This needs owner data.
- **IC displays.**
  - The assurance frontier ([Leibowitz et al.](https://consensus.app/papers/details/f9145b920f6b5c39bb9b2fbec424c295/?utm_source=claude_desktop)).
  - The growth–risk frontier ([Wei et al. 2024](https://consensus.app/papers/details/9de16903a7c554e0aa49029e121504a8/?utm_source=claude_desktop)).
  - Both complement the dossier's four-panel frontier.

### 4.6 Agent, IC and organizational design
- **Gambling-detector additions (challenge agent).** **[Inference]**
  - V-shaped exposure in wealth ([Strub et al.](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop)).
  - Risk rising as real rates fall at constant premia ([Campbell & Sigalov](https://consensus.app/papers/details/b029ce8a702156d8bc5e5d2fde4d3409/?utm_source=claude_desktop)).
  - Larger losses in bad states under a terminal ES floor ([Wei 2021](https://consensus.app/papers/details/5bc6b8052fa75c37a94d6cfdd08d70f1/?utm_source=claude_desktop)).
  - A risky share collapsing to zero near a ratchet floor ([Jeon et al. 2018](https://consensus.app/papers/details/b6c025002fa5573a996b38f884696090/?utm_source=claude_desktop)).
- **Challenge-agent rubric.**
  - Report the RS target and the implied DRO radius side by side, tuned by cross-validation ([Wang et al. 2025](https://consensus.app/papers/details/97d781784f8953ec915e053f62c18c68/?utm_source=claude_desktop)).
  - Compare surrogate slack with simulated breach frequency ([Chen, Kuhn & Wiesemann](https://consensus.app/papers/details/f69feb9051595f6e85764edfdd18d6c3/?utm_source=claude_desktop)).
- **Groups as satisficing agents.** Robust satisficing "is also useful in allocating resources for multiple satisficing agents to meet their expected reward targets" ([Sim et al. 2021](https://consensus.app/papers/details/d3fc5f3a81a2553097712b50a12ff714/?utm_source=claude_desktop)).
  - **[Inference]** Each of the seven groups can be a satisficing agent with its own target, with the Treasurer allocating the liquidity budget.
  - Under risk, satisficing is "typically inferior to optimization strategies", but under uncertainty it "can be highly effective" ([Artinger et al., JEL 2022](https://consensus.app/papers/details/f7d393a8f8f35c85b0ff1d369b99c692/?utm_source=claude_desktop)). This argues for satisficing on the ambiguous private-market forecasts and optimization on well-specified liquid sleeves.
- **Pacing-proposal agent.** Evolutionary, "trustworthy and explainable" AI can design recommitment strategies ([Kieffer et al. 2023](https://consensus.app/papers/details/1a08544fb5305532bc1270a2b91fa377/?utm_source=claude_desktop)).
  - **[Inference]** Agents propose pacing rules; the deterministic simulator prices them, as in the Agentic-Scientist pattern and dossier §6.6.
- **Treasurer seat (Corporate Finance).**
  - Owns C1, capital-call coverage, C6 and the owner-demand model.
  - **[Inference]** The duals of these constraints become the internal transfer-pricing curve (context §1A).
  - Reporting the reliability constraints as bPoE makes them legible to a treasury audience used to confidence levels.
- **IC pre-commitment.** The IC sets per-cycle parameters: the ε schedule, α, the threshold path and the payout rule. These are formalized through the induced objective, and overrides are logged (dossier §6.9).
  - Practitioner goals-based investing frames the IC choice as "secure essential goals with the highest confidence level and maximize the chances to reach aspirational goals" ([Deguest et al.](https://consensus.app/papers/details/de16fdb8464558b9b2bf79dd0d64d0e7/?utm_source=claude_desktop)). See §5 for how this conflicts with the dossier.

### 4.7 Other relevant records surfaced (not annotated)

*Goal-based investing and the target*
- [Maximizing the Probability to Reach the Goal: An Exploration Exercise in Goal-Based Wealth Management](https://consensus.app/papers/details/f8965e7fb5ff54dca16eb31726d66f8d/?utm_source=claude_desktop) (Simonato, 2023, SSRN). The P-max goal-based investor beats a mean-variance investor in goal achievement; with transaction costs, goal-attentive MV and GBWM perform similarly in many cases.
- [Goal-based investing based on multi-stage robust portfolio optimization](https://consensus.app/papers/details/799d06edd867504783856f2e63ee9f0c/?utm_source=claude_desktop) (J. Kim et al., 2022, *Ann. OR*). Robust optimization with prioritized goals avoids the scenario-tree curse of dimensionality.
- [Goal-based Investing](https://consensus.app/papers/details/de16fdb8464558b9b2bf79dd0d64d0e7/?utm_source=claude_desktop) (Deguest et al., 2021, book, DOI 10.1142/12386). Performance-seeking versus goal-hedging building blocks.
- [Strategic Asset Allocation for Endowment Funds](https://consensus.app/papers/details/c03cd55b21a152c59cae91f3817636a8/?utm_source=claude_desktop) (K. Jacobs et al., 2021, JPM). A typical endowment mix "nearly maximizes the probability of achieving the dual long-term investment goals".
- [Interpreting Omega Ratio for Goals-Based Wealth Management](https://consensus.app/papers/details/4fdaebfdd6f1501590943cc6ccec8f09/?utm_source=claude_desktop) (Khadilkar et al., 2026, JWM; recent). A risk-sensitive Omega that blends goal probability and returns.

*Drawdown, floors and ratchets*
- [Optimal lifetime consumption and investment under a drawdown constraint](https://consensus.app/papers/details/7af6963baf0d5fd08963d227269b5a4e/?utm_source=claude_desktop) (Élie et al., 2008, F&S, 96 citations). Explicit value function and policies.
- [Portfolio Selection With a Drawdown Constraint](https://consensus.app/papers/details/93ffd532ae46584dbfab5bc5ef5c6ee1/?utm_source=claude_desktop) (Alexander et al., 2006, JBF). The constrained portfolio "can be notably mean-variance inefficient"; with a benchmark, the constraint raises tracking error.
- [Portfolio management under drawdown constraint in discrete-time financial markets](https://consensus.app/papers/details/edadc75170fe57be8b94ae682ff47d4a/?utm_source=claude_desktop) (Hernández-Hernández, 2022, J. Appl. Prob.). Optimal growth under drawdown limits via Markov decision processes.
- [Maximizing the goal-reaching probability before drawdown with borrowing constraint](https://consensus.app/papers/details/6b8ed083f84251ed880ebda1df5e3113/?utm_source=claude_desktop) (Yuan et al., 2021, AIMS Math.). Closed form with a leverage cap.
- [Portfolio selection with consumption ratcheting](https://consensus.app/papers/details/b6c025002fa5573a996b38f884696090/?utm_source=claude_desktop) (Jeon et al., 2018, JEDC, 41 citations); [Portfolio selection with drawdown constraint on consumption: a generalization model](https://consensus.app/papers/details/3aaa8dfc3d295ab7a916910f9cf9c8ec/?utm_source=claude_desktop) (Jeon et al., 2021, MMOR); [Optimal Discrete Ratchet Consumption](https://consensus.app/papers/details/0a95294d002158cfab81b379c4e530bc/?utm_source=claude_desktop) (Watson et al., 2012, SSRN), a finite-horizon Dybvig ratchet.

*Spending rules and sovereign owners* (several are annotated in streams 02 and 03)
- [Optimal portfolio and spending rules for endowment funds](https://consensus.app/papers/details/f11a9145a77b5305bdf13f26c640edcb/?utm_source=claude_desktop) (Kashif et al., 2020, RQFA). Under the hybrid smoothing rule the optimal portfolio is less risky and spending less volatile; it underperforms in strong bull markets.
- [Spending rules for endowment funds: A dynamic model with subsistence levels](https://consensus.app/papers/details/487b8dd4097a50a29b0253f0c1c8de84/?utm_source=claude_desktop) (Bajeux-Besnainou et al., year not shown). A minimum subsistence spending level placed in the objective.
- [Dynamic spending and portfolio decisions with a soft social norm](https://consensus.app/papers/details/62dbecedd3f75999bcf3364f3ba3f122/?utm_source=claude_desktop) (Mork et al., JEDC). Spending well below expected return and mostly procyclical; simple rules "can reach almost the same expected discounted utility".
- [Capital Preservation and Current Spending with Sovereign Wealth Funds and Endowment Funds: A simulation Study](https://consensus.app/papers/details/c93456144b3e598bbe6aa9eb8ae9d5d8/?utm_source=claude_desktop) (Mork et al., 2022, IJFS).
- [Strategic Asset Allocation for Sovereign Wealth Funds](https://consensus.app/papers/details/5658a41f33655aeb9301328935c1591c/?utm_source=claude_desktop) (Michaelides et al., 2022, SSRN). Taxation capacity and consumption commitments "substantially affect asset allocation".
- [Risk Taking and Fiscal Smoothing with Sovereign Wealth Funds in Advanced Economies](https://consensus.app/papers/details/0c6e0c115ef95a64a46a430cf506d3e4/?utm_source=claude_desktop) (Lindset et al., 2019, IJFS).
- [A note on portfolio choice for sovereign wealth funds](https://consensus.app/papers/details/5c3da8c349df5a82b6b777011c9a5e90/?utm_source=claude_desktop) (Scherer, 2009, FMPM). Three-fund separation: speculative demand plus hedges against oil-price and short-rate shocks.
- [Optimal asset allocation for commodity sovereign wealth funds](https://consensus.app/papers/details/2a0ef305e415569e9411d0fbceaa310d/?utm_source=claude_desktop) (Irarrazabal et al., QF). Results are "particularly sensitive to the correlation between oil and stock price changes".
- [Commodity-based Sovereign Wealth Funds; Managing Financial Flows in the Context of the Sovereign Balance Sheet](https://consensus.app/papers/details/c7141a01c2915f2c9d142ef65e3eee81/?utm_source=claude_desktop) (Al-Hassan et al., 2018, IMF WP). A sovereign asset-liability (SALM) framework, including drawdowns to cover financing gaps.

*Time consistency*
- [Time-consistent and self-coordination strategies for multi-period mean-Conditional Value-at-Risk portfolio selection](https://consensus.app/papers/details/3d1a474a2793567282728b01eedada0a/?utm_source=claude_desktop) (Cui et al., 2019, EJOR). The pre-committed and time-consistent strategies are the extreme cases of a self-coordination strategy; extended to regime switching.
- [Pre-commitment vs. time-consistent strategies for the generalized multi-period portfolio optimization with stochastic cash flows](https://consensus.app/papers/details/45057b53c5ad5a57bbc86f32206cceaf/?utm_source=claude_desktop) (Zhou et al., 2016, IME). The time-consistent strategy is "more stable and secure".
- [Dynamic Mean-Variance Asset Allocation](https://consensus.app/papers/details/efdcbaed1d3c593b826fdad7cea157d5/?utm_source=claude_desktop) (Basak et al., record year 2007, 585 citations). The time-consistent MV solution.
- [Multilevel Optimization Modeling for Risk-Averse Stochastic Programming](https://consensus.app/papers/details/24bd5c6347a55d41a8af3e6bd461f324/?utm_source=claude_desktop) (Eckstein et al., 2016, IJOC). Nested-form measures "have some undesirable and somewhat counterintuitive modeling properties".
- [Time consistency of dynamic risk measures](https://consensus.app/papers/details/ce5f405a499852bfa63fabe0cd12fd1d/?utm_source=claude_desktop) (Shapiro, 2012, ORL).
- [Risk-Averse Stochastic Programming: Time Consistency and Optimal Stopping](https://consensus.app/papers/details/e875c5882de65c55bc923e2dd102de83/?utm_source=claude_desktop) (Pichler et al., 2021, OR).
- [Tutorial on risk neutral, distributionally robust and risk averse multistage stochastic programming](https://consensus.app/papers/details/2331cc1ac83f5043b80b0912e7a8d2e0/?utm_source=claude_desktop) (Shapiro, 2021, EJOR).
- [Asset liability management under sequential stochastic dominance constraints](https://consensus.app/papers/details/295e2cc1acea519691f1da3da818ec23/?utm_source=claude_desktop) (Consigli et al., 2025, Ann. OR). A time-consistent funding constraint stated as second-order stochastic dominance of portfolio returns over liabilities. A possible alternative to CVaR for C1.

*Withdrawals and payout barriers*
- [Better than Pre-Commitment Mean-Variance Portfolio Allocation Strategies: A Semi-Self-Financing Hamilton-Jacobi-Bellman Equation Approach](https://consensus.app/papers/details/d7845d466a7154c7aab3f347813b48bb/?utm_source=claude_desktop) (Dang et al., 2016, EJOR, 80 citations).
- [Better than optimal mean-variance portfolio policy in multi-period asset-liability management problem](https://consensus.app/papers/details/b5b0f21a8b36504cbbea57d00baff832/?utm_source=claude_desktop) (Cui et al., 2020, ORL).

*Risk measures and limits*
- [Risk management with weighted VaR](https://consensus.app/papers/details/eacaa636f293523b9bc95db8d3b7d637/?utm_source=claude_desktop) (Wei, 2018, Math. Finance). VaR and ES allow "regulatory capital arbitrage, incurring larger losses when losses occur".
- [On the Equivalence Between Value-at-Risk and Expected Shortfall in Non-Concave Optimization](https://consensus.app/papers/details/7befd1622cc85b18a5ef8689b0215d27/?utm_source=claude_desktop) (An Chen et al., 2020, SSRN). For a surplus-driven institution, VaR and ES induce the same portfolio choice, unlike Basak & Shapiro.
- [Dynamic Portfolio Optimization under CVaR Constraints](https://consensus.app/papers/details/be228653d3365999930a6d4d36aea884/?utm_source=claude_desktop) (Hu et al., 2026; recent). A terminal CVaR constraint produces "an asymmetric reallocation across states rather than uniform de-risking".
- [From Value-at-Risk to Expected Shortfall: An Agent-Based Analysis of Market Stability](https://consensus.app/papers/details/95f25bdf1e7c52c48affc0c165e7b62c/?utm_source=claude_desktop) (Llacay et al., 2026, FRL; recent). Widespread ES limits can create instability spirals.
- [Value-at-risk versus expected shortfall: A practical perspective](https://consensus.app/papers/details/e1406753808953b59a6312393343fa52/?utm_source=claude_desktop) (Yamai et al., 2005, JBF, 371 citations).

*Chance constraints and robustness*
- [On distributionally robust chance constrained programs with Wasserstein distance](https://consensus.app/papers/details/5edbc7b0218d5add938d96ea7faef333/?utm_source=claude_desktop) (Xie, Math. Prog., 283 citations).
- [Analyzing and Quantifying the Intrinsic Distributional Robustness of CVaR Reformulation for Chance-Constrained Stochastic Programs](https://consensus.app/papers/details/95d58c07ab7b550e936b3affb9e57de8/?utm_source=claude_desktop) (Cao et al., 2020, IEEE TPWRS). The CVaR reformulation "is intrinsically robust".
- [The Analytics of Robust Satisficing](https://consensus.app/papers/details/d3fc5f3a81a2553097712b50a12ff714/?utm_source=claude_desktop) (Sim et al., 2021, SSRN).
- [Satisficing: Integrating Two Traditions](https://consensus.app/papers/details/f7d393a8f8f35c85b0ff1d369b99c692/?utm_source=claude_desktop) (Artinger et al., 2022, JEL).

*Growth-optimal and Kelly*
- [Long-term capital growth: the good and bad properties of the Kelly and fractional Kelly capital growth criteria](https://consensus.app/papers/details/e7d4306ef77b5ecfb7e2f36d18504752/?utm_source=claude_desktop) (MacLean et al., 2010, QF, 84 citations).
- [The Kelly Capital Growth Investment Criterion: Theory and Practice](https://consensus.app/papers/details/f4c7cf206e6a5802b1f8c86b2dd62137/?utm_source=claude_desktop) (MacLean et al., 2011, book, 260 citations). Only log utility "minimizes the expected time to arbitrary large goals", which offers a goal reading of growth that has no digital payoff.
- [Risk-Constrained Kelly Portfolios Under Alpha-Stable Laws](https://consensus.app/papers/details/aab22bfdf6ae58a6ae224a6906974861/?utm_source=claude_desktop) (Wesselhöfft et al., 2020, Comput. Econ.). Long puts improve growth at a given VaR or ES, supporting the dossier's point that the tail hedge's value appears in the constraints.
- [On Risk Reduction in Kelly Betting Using the Conservative Expected Value](https://consensus.app/papers/details/57473f6550795bedb7e16f4186d2cc24/?utm_source=claude_desktop) (Rujeerapaiboon et al., 2018, CDC). A systematic alternative to ad hoc fractional Kelly.

*Illiquidity, pacing and private markets* (mostly annotated in streams 01, 02, 04 and 05)
- [The Endowment Model and Modern Portfolio Theory](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop) (Dimmock et al., MS).
- [Optimal Allocation to Private Equity](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop) (Giommetti et al., 2021, SSRN).
- [Asset Allocation and Private Market Investing](https://consensus.app/papers/details/61e21abbf1425eac88e593ae69993030/?utm_source=claude_desktop) (Shen et al., 2021, JPM). Pacing trades performance against "the frequency of certain liquidity events with different severities".
- [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop) (Maurin et al., 2022, MS).
- [How much for a haircut? Illiquidity, secondary markets, and the value of private equity](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop) (Bollen et al., 2016, Fin. Mgmt).
- [Portfolio Optimization with Private Equity Funds](https://consensus.app/papers/details/4b82de353e7f5ab39a2937994c2aafe2/?utm_source=claude_desktop) (Buchner, 2012, SSRN).
- [Should Endowments Continue to Commit to Private Investments?](https://consensus.app/papers/details/8c1bbf433c6e5155b54d5003d2010389/?utm_source=claude_desktop) (Hammond, 2020, J. Investing).
- [A Dynamic Model of Private Asset Allocation](https://consensus.app/papers/details/da8e4aa55bd25aca8a43f6c4444f3334/?utm_source=claude_desktop) (Hui Chen et al., 2025, arXiv; recent).
- [Learning private equity recommitment strategies for institutional investors](https://consensus.app/papers/details/1a08544fb5305532bc1270a2b91fa377/?utm_source=claude_desktop) (Kieffer et al., 2023).
- [The Art of Commitment Pacing](https://consensus.app/papers/details/662d9b40176f5566bd73002284298286/?utm_source=claude_desktop) (Meyer, 2024, book). Covers modelling co-investments and secondaries in pacing plans, relevant to the hybrid Secondaries book.
- [Managing Illiquidity in Open-Ended Funds with Private Asset Allocations](https://consensus.app/papers/details/12cd077c32a755c9bbab6ea80a91706c/?utm_source=claude_desktop) (Leote de Carvalho et al., 2026; recent). Suspending future commitments can rebalance "without forced secondary sales".

---

## 5. Papers that challenge the dossier's recommendations

| Dossier recommendation (section) | Challenging paper(s) | What they show | Suggested response **[Inference]** |
|---|---|---|---|
| The design must be time-consistent. End-of-horizon floors and P(target at T) "change meaning as the horizon approaches"; nested or rolling formulations are preferred, and risk-averse SDDP with nested CVaR is offered for "full time-consistency" (§1 item 4; §2.5; §7) | [Forsyth 2020](https://consensus.app/papers/details/f1547b977f055cdb8efcd20b57857a68/?utm_source=claude_desktop); [Strub et al. 2019](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop); [Pflug & Pichler 2016](https://consensus.app/papers/details/9fb02745a50d5d0eb3d6805a301fe5ed/?utm_source=claude_desktop); [Eckstein et al. 2016](https://consensus.app/papers/details/24bd5c6347a55d41a8af3e6bd461f324/?utm_source=claude_desktop); [Shapiro 2012](https://consensus.app/papers/details/ce5f405a499852bfa63fabe0cd12fd1d/?utm_source=claude_desktop) | Enforcing time consistency in mean-CVaR "compares unfavourably" with pre-commitment, and pre-commitment is implementable through an induced time-consistent objective (Forsyth). Pre-commitment equals a naive investor with a time-increasing CVaR confidence level (Strub). Terminal AV@R becomes DP-tractable with an augmented risk-level state (Pflug & Pichler). Nested measures have "counterintuitive modeling properties" (Eckstein). Nested compositions are law-invariant only for expectation or max (Shapiro 2012). **Counter-evidence:** time-consistent strategies are more stable under misspecification ([Cong et al.](https://consensus.app/papers/details/69bbf500ffbd50a9a76bc42c7714fc51/?utm_source=claude_desktop)) and with stochastic cash flows ([Zhou et al.](https://consensus.app/papers/details/45057b53c5ad5a57bbc86f32206cceaf/?utm_source=claude_desktop)). | Keep rolling MPC. Formalize IC pre-commitment as an induced objective with a carried threshold state. Never show the IC a nested-CVaR number. Use ECRMs if a multistage time-consistent measure is needed. Run both pre-commitment and time-consistent variants across 𝓜 and report the difference. |
| "Probability constraints or objectives on wealth outcomes must be replaced by, or accompanied by, expectation-of-shortfall terms" (§2.1, citing Basak & Shapiro) | [Cuoco et al. 2008](https://consensus.app/papers/details/3904dafe5042536aacf42278cfc299db/?utm_source=claude_desktop); [Wei 2021](https://consensus.app/papers/details/5bc6b8052fa75c37a94d6cfdd08d70f1/?utm_source=claude_desktop); [Wei 2018](https://consensus.app/papers/details/eacaa636f293523b9bc95db8d3b7d637/?utm_source=claude_desktop); [An Chen et al. 2020](https://consensus.app/papers/details/7befd1622cc85b18a5ef8689b0215d27/?utm_source=claude_desktop) | Re-evaluated dynamically, VaR limits always lower risk exposure and extreme-loss probability, and TCE is equivalent to VaR in that setting (Cuoco). ES managers can also incur larger losses when losses occur (Wei 2021). VaR and ES both allow "regulatory capital arbitrage" (Wei 2018). For a surplus-driven institution VaR and ES induce the same portfolio (An Chen et al.). | The remedy is dynamic re-imposition, which dossier §2.5(i) already proposes, plus concavity (utility or spectral weights), not expected shortfall as such. Make C4 rolling. Keep P(red) constraints, but re-impose them each epoch. Add a terminal-ES test to the gambling detector. |
| Target-shortfall exponent α = 2, IC sweep 1–3; "α ≥ 1 is never risk-seeking below target" (§6.5; §3.1) | [Krabichler et al.](https://consensus.app/papers/details/c7d8bb6499c75f8e93935fa3a567584b/?utm_source=claude_desktop) | Maximizing P(goal) and minimizing expected shortfall "yield, in fact, the same optimal investment policy" in a goal-based setting. | Exclude α = 1 from the sweep (use 1.5–3). Keep α = 2 as default. Note that risk-neutral below target (α = 1) can still mean a digital-like policy. |
| The deck's two-tier "secure the floor, then pursue P(10%)" is criticized: P(10%) is called "the most risk-seeking criterion possible below target" (§1 item 2; §2.1) | [Deguest et al.](https://consensus.app/papers/details/de16fdb8464558b9b2bf79dd0d64d0e7/?utm_source=claude_desktop); [Kim et al. 2019](https://consensus.app/papers/details/f03987fc1a23597e921e27887e9a71fc/?utm_source=claude_desktop); [Simonato 2023](https://consensus.app/papers/details/f8965e7fb5ff54dca16eb31726d66f8d/?utm_source=claude_desktop); [Jacobs et al. 2021](https://consensus.app/papers/details/c03cd55b21a152c59cae91f3817636a8/?utm_source=claude_desktop) | The goals-based investing paradigm is to "secure essential goals with the highest confidence level and maximize the chances to reach aspirational goals". Strict-priority goal programming is an LP. A P-max goal-based investor beats mean-variance in goal achievement. A typical endowment SAA "nearly maximizes" the probability of its dual goals. | With a robustly secured floor and no leverage, P-max risks only the cushion. ADIC may lever, so the dossier's objection stands for ADIC. Still, acknowledge P(goal) as legitimate peer practice in static SAA, and restrict it to a reported KPI or to unlevered sleeves. The verification log (R12) also calls "most risk-seeking criterion possible" an overclaim. |
| The joint 5-year reliability is translated to a per-year ε by the union bound; CVaR is "the standard convex conservative surrogate" (§2.3; §6.4 C1) | [Zymler et al.](https://consensus.app/papers/details/8c13b90032cc5aa1a538b69b775db3c7/?utm_source=claude_desktop); [Wenqing Chen et al. 2010](https://consensus.app/papers/details/793e74a285405a7c803b29f7fd3b8246/?utm_source=claude_desktop); [Jiang & Xie](https://consensus.app/papers/details/921da370fcd4548aa53a54c681f6ec35/?utm_source=claude_desktop); [Zhi Chen et al.](https://consensus.app/papers/details/f69feb9051595f6e85764edfdd18d6c3/?utm_source=claude_desktop) | Joint formulations are tighter than Bonferroni-type benchmarks. ALSO-X is provably less conservative than CVaR when constraints are convex. All common DRCCP approximations "can perform arbitrarily poorly in data-driven settings". | Use a joint (scaled) worst-case CVaR. Try ALSO-X. Validate by simulation. Keep the ε/H translation only for communication. |
| Robust satisficing is preferred because it asks for a target rather than an ambiguity radius (§2.4) | [Wang et al. 2025](https://consensus.app/papers/details/97d781784f8953ec915e053f62c18c68/?utm_source=claude_desktop) | Wasserstein DRO and RS share one solution family; a radius–target correspondence makes their solutions coincide. Practical performance depends on how parameters are selected. | Present RS and DRO as two parameterizations of the same model. Report both τ and the implied radius, and tune by cross-validation. RS's advantage is elicitation, not a different solution. |
| Sustainability = real NAV net of distributions; payouts above ~7% are transfers from future to current owners (§1; §2.6; §6.4) | [Campbell & Sigalov](https://consensus.app/papers/details/b029ce8a702156d8bc5e5d2fde4d3409/?utm_source=claude_desktop); [Michaelides et al. 2022](https://consensus.app/papers/details/5658a41f33655aeb9301328935c1591c/?utm_source=claude_desktop); [Dang, Forsyth & Vetzal 2017](https://consensus.app/papers/details/be5936659c2a5006ac12e9527606e1ec/?utm_source=claude_desktop); [Mork et al., IJFS 2022](https://consensus.app/papers/details/c93456144b3e598bbe6aa9eb8ae9d5d8/?utm_source=claude_desktop) | Sustainable-spending constraints induce reaching for yield when real rates fall. Sustainable endowment withdrawals are "somewhat lower" than 4% real, under optimal allocation. Withdrawing expected returns eventually depletes the fund. Lower withdrawal rates help more than risk reduction. | Treat sustainability as a soft objective. Add the real-rate state and a reaching-for-yield check. Lead the IC payout discussion at ≈5–6% (verification R4), and show depletion risk as a function of d. |
| Payout smoothing (Yale) and an optional ratchet floor D_t ≥ (1 − ρ)D_{t−1} (§5; C6) | [Mork et al., JEDC](https://consensus.app/papers/details/62dbecedd3f75999bcf3364f3ba3f122/?utm_source=claude_desktop); [Mork et al., IJFS 2022](https://consensus.app/papers/details/c93456144b3e598bbe6aa9eb8ae9d5d8/?utm_source=claude_desktop); [Jeon et al. 2018](https://consensus.app/papers/details/b6c025002fa5573a996b38f884696090/?utm_source=claude_desktop) | Optimal spending is procyclical: losses "should, as a rule, be followed by larger than proportional spending cuts", except near the norm. Smoothing raises depletion risk after large negative returns, "though only modestly so". Under ratcheting, the risky share swings between 0 and the unconstrained level. | Prefer barrier top-ups above a protected minimum. If the owner tolerates dips, model the minimum as a soft floor (spliced utility). Avoid ratchets unless mandated. Quantify the depletion cost of smoothing for the IC. |
| γ = 3 is justified by illiquidity-induced risk aversion (Ang et al.) (§6.5) | [Buchner 2012](https://consensus.app/papers/details/4b82de353e7f5ab39a2937994c2aafe2/?utm_source=claude_desktop); [Giommetti & Jørgensen](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop); [Dimmock, Wang & Yang](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop) | Liquidity welfare losses are negligible when PE and traded stocks are close substitutes. PE allocations are not monotone in risk aversion. Liquidity diversification across staggered lockups raises optimal alternatives allocations. | Calibrate γ and the illiquidity premium by simulating ADIC's book. Do not treat γ = 3 as implied by Ang et al. alone. |
| The PE premium (J.P. Morgan PE 10.2%) underpins P(10%) and payout feasibility (§1; §6.10) | [Hammond 2020](https://consensus.app/papers/details/8c1bbf433c6e5155b54d5003d2010389/?utm_source=claude_desktop) | Over the last 15 years, private investments did not compensate the average endowment for illiquidity; in most periods they underperformed mPME-adjusted public markets. | Add a "no PE premium" variant to 𝓜, and show P(10%) and the sustainable payout under it. |

---

## 6. Verbatim usage message

The last usage message returned by Consensus in this run:

> 17 searches left this month; resets to 500 on November 1st.

---

## 7. Search log and scope notes

**Consensus searches (12), run sequentially with no filters.** The counter shows searches left after each call; the drops between calls reflect the two other agents sharing the quota.

| # | Query | Purpose | Counter after |
|---|---|---|---|
| 1 | reaching goals by a deadline | Seed; Browne (1999) check | 46 |
| 2 | goal-based investing probability of reaching a target | Seed; Das et al. check | 45 |
| 3 | optimal investment under drawdown constraints | Seed; Grossman & Zhou, Chekhlov et al., Cvitanić & Karatzas checks | 42 |
| 4 | portfolio choice with a consumption floor ratcheting spending endowment | Seed (refined); Dybvig checks | 40 |
| 5 | time-consistent risk measures multistage stochastic programming | Seed (refined); Shapiro, Ruszczyński, Philpott & de Matos checks | 35 |
| 6 | optimal allocation to illiquid private equity with capital commitments and endowment spending | Refinement; Ang et al. and Gourier et al. checks | 34 |
| 7 | robust satisficing aspiration level target-oriented optimization | Refinement; Brown & Sim, Chen & Sim, Long–Sim–Zhou checks | 30 |
| 8 | multi-period mean-CVaR asset allocation with withdrawals: pre-commitment versus time-consistent strategies | Seed "CVaR portfolio optimization" (refined toward multi-period and time consistency); challenge search | 29 |
| 9 | sovereign wealth fund optimal asset allocation with fiscal withdrawals and commodity revenue risk | Refinement (owner balance sheet) | 25 |
| 10 | optimization of conditional value-at-risk and convex approximations of chance constrained programs | Refinement; Rockafellar & Uryasev and Nemirovski & Shapiro checks | 22 |
| 11 | value-at-risk based risk management optimal dynamic trading strategies with risk limits expected shortfall | Refinement; Basak & Shapiro and Föllmer & Leukert checks; challenge search | 19 |
| 12 | risk-constrained Kelly gambling fractional Kelly growth optimal portfolio drawdown | Refinement; Busseti et al. check | 17 |

All six seed topics were covered. Seed 4 ("CVaR portfolio optimization") was folded into searches 8 and 10.

**WebSearches (3), metadata only:**
1. Long, Sim & Zhou, *Robust Satisficing*, OR 71(1):61–82 (2023), DOI 10.1287/opre.2021.2238. Sources: [IDEAS/RePEc](https://ideas.repec.org/a/inm/oropre/v71y2023i1p61-82.html); [EconBiz](https://econbiz.de/Record/robust-satisficing-long-daniel-zhuoyu/10014308279).
2. Rockafellar & Uryasev, *Optimization of conditional value-at-risk*, J. Risk 2(3), 2000, pp. 21–41 (one listing gives 21–42). Sources: [Risk.net](https://risk.net/journal-risk/2161159/optimization-conditional-value-risk); [IDEAS/RePEc](https://ideas.repec.org/a/rsk/journ4/2161159.html).
3. Gourier, Phalippou & Westerfield, *Capital Commitment*, JF 79(5):3407–3457 (2024), DOI 10.1111/jofi.13382. Sources: [CEPR DP16910](https://cepr.org/publications/dp16910); [IDEAS/RePEc](https://ideas.repec.org/p/cpr/ceprdp/16910.html).

**Not checked (quota):** Browne (1997); Föllmer & Leukert (1999) (indirectly corroborated); Fishburn (1977); Campi & Garatti (2008); Ruszczyński (2010); Avanzi (2009). All six were confirmed against Crossref or RePEc in the verification log.

**Consensus record quirks:**
- Working-paper or online-first years: Browne 1996; Basak & Shapiro 1999; Chekhlov et al. 2004; Brown & Sim 2008; Das et al. 2019.
- SSRN or NBER DOIs on journal records: Chekhlov et al.; Strub et al.; Campbell & Sigalov; Dimmock et al.
- The Rockafellar & Uryasev record carries an unrelated abstract (noted by streams 01 and 03).
- The Gourier et al. working paper appears under an earlier title.

**Not done:** Full texts were not read. No result in this run was filtered. The Consensus thread tools were not used.
