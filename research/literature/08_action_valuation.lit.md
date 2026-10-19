# Stream 08 literature check: one decision currency for SELL / HOLD / REFINANCE / LEVER

**Dossier checked:** `research/dossiers/08_action_valuation.md` (1,038 lines, as of 2026-10-18).
- §10 lists 34 academic works:
  - 21 on valuation, liquidity and real options;
  - 10 on optimisation, optimal stopping and decision analysis;
  - 3 on behaviour.
- The last line of §10 names 4 more academic works as "not verified this session": Davis & Norman (1990), Myers & Majd (1990), Hawkins (2003), and Gribik, Hogan & Pope (2007).
- The regulatory, official and practitioner sources (BCBS, FSI, Directive (EU) 2025/2, FRED, Jefferies, Rede, Proskauer, Bain, press) are outside this check. The verification log confirmed them against primary documents.

**Date:** 2026-10-18.

**Search engine:** Consensus. 42 searches, run one at a time with no filters:
- 29 targeted citation look-ups;
- 13 topical backfill searches: the 6 seed queries plus 7 refinements (secondary pricing, weakly coupled dynamic programs, continuation funds, NAV financing, value of information, internal capital markets, real options with debt).
- Five citations were confirmed by searches run for other purposes: Ang et al.; Dixit & Pindyck; Nadauld et al.; Adelman & Mersereau; and Brown, Smith & Sun.

One WebSearch confirmed the published version of Myers & Majd (1990). Consensus indexes it only as a 1983 working paper (§7).

**Companion:** `research/verification/08_action_valuation.verify.md`. It checked 16 references against publisher, NBER, RePEc, AEA and arXiv pages and found all of them correct. This file is an independent check using Consensus records.

**Organizational mapping (user, 2026-10-18)**
- Secondaries is a hybrid of direct and fund investments:
  - LP commitments to third-party secondary funds;
  - direct secondary deals (LP-portfolio purchases, GP-led continuation vehicles).
- Corporate Finance owns the treasury function. Per the context file it also owns portfolio-level borrowing and leverage facilities, overlay collateral (VM/IM) and distribution payments to the owner.
- The design implications below assign the funding side to Corporate Finance: the liquidity price ℓ (the internal transfer-pricing curve), the MCL curve, facility-level LEVER and the distribution policy. The seven investment groups own asset-level SELL / HOLD / REFINANCE / LEVER proposals.

**Reading conventions**
- Findings come from the titles and abstracts that Consensus returned. Full texts were not read.
- **[Inference]** marks design reasoning that goes beyond what an abstract states.
- Author lists are shown as Consensus displays them, with "et al." where Consensus truncates.
- Years are Consensus record years. Where a record carries the working-paper or online year, the print year is noted. Such differences are not counted as mismatches.
- "Also flagged by Stream NN" means a sibling literature file already lists the paper. It is repeated here only where it bears directly on SELL / HOLD / REFINANCE / LEVER valuation.

---

## 1. Summary

### Citation integrity
- **Scope.** The dossier names 38 academic works: 34 in §10 and 4 named only. I checked 35 of them in Consensus:
  - 31 of the 34 listed works;
  - all 4 named-only works.

  The other 3 listed works (Takahashi & Alexander; Cariño et al.; Kouwenberg) were already confirmed by the Stream 01, 04 and 06 literature checks. They were not re-searched.
- **Result:** 34 found, 1 mismatched, 0 not found.

  **No hallucinated or garbled references.** This agrees with the verification log, which found 16 of 16 correct.
- **Every claim that could be checked against an abstract matched, with two exceptions:** Ang et al.'s wording and Nadauld et al.'s seller PME (fixes 1 and 2 below). Confirmed examples:
  - McDonald & Siegel's "twice the investment cost";
  - Faulkender & Wang's "declines with larger cash holdings, higher leverage";
  - Brunnermeier & Pedersen's "mutually reinforcing";
  - Everett's "fail-safe" and "independent activities";
  - Sorensen, Wang & Yang's "LPs may just break even";
  - Udell & Boyd's bound "proportional to the maximal number of active constraints";
  - Whittle's multiplier-defined index;
  - Bolton, Chen & Wang's double-barrier policy.
- **Fixes**
  1. **Ang, Papanikolaou & Westerfield (2014).** The abstract says uncertainty about the illiquidity interval is "a primary determinant" of the cost of illiquidity. §2.1 says it "drives most" of that cost. The verification log flagged the same point.
  2. **Nadauld et al. (2019).** The JFE abstract gives a seller PME of **0.976**, not 0.974 (§2.1, §4). Add 132(3):158–181, from the verification log.
  3. **Udell & Boyd.** A journal version exists: *Computational Optimization and Applications*, DOI 10.1007/s10589-015-9819-4. Cite it alongside arXiv:1410.4158.
  4. **Gribik, Hogan & Pope.** Consensus dates "Market-Clearing Electricity Prices and Energy Uplift" to 2008, not 2007. This is the one mismatch. Add the title.
  5. **Takahashi & Alexander (2002) is an orphan.** It is listed in §10 but never cited in the text.
  6. **The four named-only works can be upgraded from "not verified" to verified,** with full metadata (table rows 35–38).
  7. **All five † items, which the dossier wrote from memory, are confirmed** with matching DOIs:
     - Whittle (1988);
     - Howard (1966);
     - Korteweg & Nagel (2016), via a working-paper record;
     - Tversky & Kahneman (1974);
     - Takahashi & Alexander (2002), via the sibling record.
- **Record-quality notes.** These are Consensus quirks, not dossier errors:
  - Shefrin & Statman's record carries an unrelated abstract.
  - Lerner, Schoar & Wongsunwai appears only as a *CFA Digest* summary.
  - Longstaff (2009) appears as a JSTOR record dated 2011, plus its working paper.
  - Dixit & Pindyck appears as a 1994 *Journal of Finance* record, apparently the book review.

### Backfill (13 topical searches)
The dossier's theory core is sound and its classic sources are correct. It misses nine clusters that bear directly on its design.

1. **Real options under financial constraints.** This is the published theory closest to the dossier's thesis.
   - Bolton et al. (2019): limited financial slack "significantly erodes" the value of growth and abandonment options, and constrained firms prefer front-loaded cash flows.
   - Bolton et al. (2012, *Market Timing, Investment, and Risk Management*) add stochastic financing windows.
   - Dai et al. (2024, *JF*) extend the theory to multi-division firms. Division investment is set by marginal q relative to the marginal value of cash, which maps onto ADIC's seven groups and Corporate Finance.
2. **SELL as constrained or regime-switching optimal stopping.**
   - Longstaff (2017) models illiquidity as a restriction on the stopping rules an investor can use when selling. Discounts can reach 30–50%, and immediacy is valued far above ongoing liquidity.
   - Chevalier et al. (2013) treat the bid discount as a mean-reverting process, with regime-dependent arrival of good offers.
   - Evans et al. (2008) make the sale threshold a proportion of the holder's liquid wealth.
   - Mazzon et al. (2024) add ambiguity aversion and learning.
3. **Incomplete-market real options.** Unhedgeable risk and risk aversion erode option value and lower exercise thresholds (Henderson 2007). **[Inference]** The dossier's waiting-option values (κ^irr) are probably upper bounds even before its own "perfect learning" caveat.
4. **Where the liquidity shadow price comes from.**
   - Shadow costs are low when illiquidity only distorts allocation, and high when it restricts consumption (Jansen et al. 2022; also flagged by Stream 01). **[Inference]** ADIC's ℓ should therefore come mainly from its distribution-floor and survival rows.
   - PME theory gives investor-specific discounting a formal basis: discount at the return on the investor's own wealth portfolio (Sørensen et al. 2015).
5. **Modern theory of weakly coupled dynamic programs (DPs).**
   - Lagrangian and approximate-LP bounds are usually close, so Lagrangian relaxation should be preferred (Brown et al. 2022).
   - Index policies need explicit tie-breaking and mixing rules (Brown et al. 2020, index policies).
   - However, when subsystems share exogenous signals, standard decompositions can lose asymptotic optimality (Brown et al. 2020, *shared resources and signals*). ADIC's funds share regimes in exactly this way.
6. **Secondary prices driven by liquidity supply.**
   - Discounts move with aggregate liquidity provision, not with future NAV returns (Albuquerque et al. 2018).
   - Interests with less undrawn capital are more liquid and win better bids (Kleymenova et al. 2012). This is direct LP-market evidence for the dossier's unfunded-share penalty, which verification-log R11 called an extrapolation.
   - Streams 04–06 also flag both papers.
7. **Behaviour specific to delegated and institutional holdings.**
   - Delegated assets show a *reverse* disposition effect (Chang et al. 2016).
   - Institutions cut risk after losses rather than ride losers (O'Connell et al. 2009).
   - Making the purchase price salient causally raises the disposition effect (Frydman et al. 2019). This supports the decision card's greyed-out since-inception IRR.
8. **Value of information (VOI).**
   - EVPI is neither necessary nor sufficient for deciding whether to buy more diligence. Decide on EVSI net of its cost (Eckermann et al. 2010).
   - Two-action problems have closed forms (Bickel 2008).
   - This supports verification-log R8.
9. **Internal capital markets.** These literatures describe the governance risks of Corporate Finance's internal transfer-pricing curve:
   - winner-picking (Stein 1997);
   - divisional rent-seeking and "socialism" (Scharfstein et al. 2000);
   - manager power (Glaser et al. 2013).

### Challenges (§5)
Twelve papers or clusters qualify specific recommendations:
- the direction of the LP disposition-effect flag;
- the κ^GP prior built on Lerner, Schoar & Wongsunwai (2007);
- the size of waiting-option values;
- static prices when funds share regimes;
- "spend part of the EVPI";
- the unconditional 9%/4% ℓ fallback;
- strip sales as a default mitigant;
- "avoid selling during the GP's fundraise";
- commitment pacing as an MCL step;
- tax components in implied liquidity spreads;
- ℓ assumed to rise monotonically as liquidity becomes scarcer;
- the assumption that the LEVER interaction term is small.

None of these overturns the core architecture:
- one currency, priced by the portfolio optimizer's duals;
- an exact MILP decides, and prices explain;
- pre-emptive liquidity rather than crisis sales.

Several change defaults, add state variables or tighten IC rubrics (§4).

---

## 2. Citation-integrity table

Status values are found, mismatched or not found. Online-first or working-paper record years are not counted as mismatches. "(†)" marks items the dossier says were written from memory.

| # | Dossier citation | Status | Corrected / confirmed metadata (Consensus unless stated) | Consensus URL |
|---|---|---|---|---|
| 1 | Acharya & Pedersen (2005), *Asset pricing with liquidity risk*, JFE 77(2) | found | DOI 10.1016/j.jfineco.2004.06.007; 2,927 citations; venue label "Unknown Journal". A second record (SSRN DOI 10.2139/ssrn.366300) shows JFE. The abstract confirms that required returns depend on expected illiquidity and on the covariances of return and illiquidity with market return and market illiquidity. | [link](https://consensus.app/papers/details/336797e7f0075604a16d469cc6a96e12/?utm_source=claude_desktop) |
| 2 | Ang, Papanikolaou & Westerfield (2014), *Portfolio choice with illiquid assets*, MS 60(11) | found (wording fix) | DOI 10.1287/mnsc.2014.1986; 171 citations. "Forgo 2% of their wealth" is confirmed. Uncertain illiquidity duration is "a primary determinant" of the cost, not what "drives most" of it (§2.1). | [link](https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop) |
| 3 | Bolton, Chen & Wang (2011), *A unified theory of Tobin's q…*, JF 66(5) | found | Record carries the NBER DOI 10.3386/w14845; 716 citations. Double-barrier cash policy confirmed. | [link](https://consensus.app/papers/details/e303976b52515556ab7c0f0476889f19/?utm_source=claude_desktop) |
| 4 | Brennan & Schwartz (1985), *Evaluating natural resource investments*, J. Business 58(2) | found | DOI 10.1086/296288; 2,415 citations. The abstract covers optimal policies for "developing, managing, and abandoning" projects. The switching / mothballing hysteresis point in §2.2 cannot be checked from the abstract. | [link](https://consensus.app/papers/details/01c1219fed6e5e19b3a1313ce8855eab/?utm_source=claude_desktop) |
| 5 | Brunnermeier & Pedersen (2009), *Market liquidity and funding liquidity*, RFS 22(6) | found | DOI 10.1093/rfs/hhn098; 5,153 citations. "Mutually reinforcing" is in the abstract. | [link](https://consensus.app/papers/details/7c944d8f27a65feea50c7b83eea8e1e3/?utm_source=claude_desktop) |
| 6 | Dimmock, Wang & Yang (2024), *The endowment model and modern portfolio theory*, MS 70(3) | found | Record year 2019; *Manag. Sci.*; NBER DOI 10.3386/w25559 (supplement DOI 10.1287/mnsc.2023.4759); 25 citations. Staggered lock-ups, endogenous time-varying rebalancing boundaries and crisis deviations are all confirmed. | [link](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop) |
| 7 | Dixit & Pindyck (1994), *Investment under Uncertainty*, Princeton UP | found (indirect record) | Indexed as "Investment Under Uncertainty.", author field "E. Schwartz et al.", 1994, *Journal of Finance*, DOI 10.2307/2329279, 7,403 citations. This appears to be the JF book-review record; its abstract is the book description. Publisher metadata is not shown. | [link](https://consensus.app/papers/details/cd37622c7e6b520eb023e1fc950ea746/?utm_source=claude_desktop) |
| 8 | Faulkender & Wang (2006), *Corporate financial policy and the value of cash*, JF 61(4) | found (working-paper record) | SSRN DOI 10.2139/ssrn.563595; record year 2004; 1,640 citations. The quoted phrase is in the abstract. The JF volume is not shown. | [link](https://consensus.app/papers/details/d1f0480c79135cf383a0600ba9f0785f/?utm_source=claude_desktop) |
| 9 | Gupta & Van Nieuwerburgh (2021), *Valuing private equity investments strip by strip*, JF 76(6) | found | DOI 10.1111/jofi.13073; 24 citations. The abstract reports negative risk-adjusted profits for the average fund in most PE categories. | [link](https://consensus.app/papers/details/a07fbcfb0fdd5d5891ce4d67340cbeb8/?utm_source=claude_desktop) |
| 10 | Holmström & Tirole (1998), *Private and public supply of liquidity*, JPE 106(1) | found | Record year 1996; JPE; DOI 10.1086/250001; 1,934 citations. The abstract says that under aggregate uncertainty the private sector cannot meet its own liquidity needs. This is consistent with §2.3. | [link](https://consensus.app/papers/details/5d6eff64796d59f1a7fb8d3bb2528237/?utm_source=claude_desktop) |
| 11 | Kahl, Liu & Longstaff (2003), *Paper millionaires…*, JFE 67(3) | found | Record year 2001; JFE; DOI 10.1016/s0304-405x(02)00258-1; 228 citations. Hedging the locked position and smoothing consumption are confirmed. | [link](https://consensus.app/papers/details/118fbb17c28751ccb74c326551ea0487/?utm_source=claude_desktop) |
| 12 | Korteweg & Nagel (2016), *Risk-adjusting the returns to venture capital*, JF 71(3) (†) | found (working-paper record) | Record year 2015; DOI 10.2139/ssrn.2309596; 134 citations. The paper generalizes PME with SDF methods; VC fund abnormal returns are "close to zero". | [link](https://consensus.app/papers/details/38b28ae37b555f3087e387f515331a0f/?utm_source=claude_desktop) |
| 13 | Lerner, Schoar & Wongsunwai (2007), *Smart institutions, foolish choices…*, JF 62(2) | found (digest record only) | Consensus returns only a *CFA Digest* summary with the same title: author field "J. D. de Villiers", 2007, DOI 10.2469/dig.v37.n3.4773, 410 citations, no abstract. The JF record is not shown. The verification log confirmed the JF metadata on RePEc. | [link](https://consensus.app/papers/details/c049d11a508950cabe26c62acb800ef7/?utm_source=claude_desktop) |
| 14 | Longstaff (2001), *Optimal portfolio choice and the valuation of illiquid securities*, RFS 14(2) | found | DOI 10.1093/rfs/14.2.407; 300 citations. Bounded-variation trading and the shadow cost of illiquidity are confirmed. | [link](https://consensus.app/papers/details/a670a5fde5275bb3b4f8fb0b9d5a80df/?utm_source=claude_desktop) |
| 15 | Longstaff (2009), *Portfolio claustrophobia*, AER 99(4) | found (JSTOR record + working paper) | There is an AER/JSTOR record (year shown 2011, 76 citations, no DOI). The working paper "Asset Pricing in Markets with Illiquid Assets" (2005, DOI 10.2139/ssrn.687298, 34 citations, [record](https://consensus.app/papers/details/a4595be7526e5194a75e9f468b8bdb54/?utm_source=claude_desktop)) states that agents "abandon diversification as a strategy and choose highly polarized portfolios", and that a liquid asset can be worth up to 25% more. | [link](https://consensus.app/papers/details/150afc54e0635b19ab8f6ab9cbe67257/?utm_source=claude_desktop) |
| 16 | McDonald & Siegel (1986), *The value of waiting to invest*, QJE 101(4) | found | DOI 10.2307/1884175; 3,935 citations. "Twice the investment cost" is confirmed. | [link](https://consensus.app/papers/details/b10fe378894f50539e6bbe12f00fbade/?utm_source=claude_desktop) |
| 17 | Nadauld, Sensoy, Vorkink & Weisbach (2019), *The liquidity cost of private equity investments*, JFE | found (minor fix) | DOI 10.1016/j.jfineco.2018.11.007; 66 citations. The JFE abstract gives buyer PME 1.023 against seller PME **0.976** (dossier: 0.974). It attributes buyer returns to "relatively flexible buyers… supplying liquidity". The asymmetric-information wording in §2.1 is not in this abstract; it may come from NBER WP 22404. Add 132(3):158–181. | [link](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop) |
| 18 | Robinson & Sensoy (2016), *Cyclicality, performance measurement, and cash flow liquidity in private equity*, JFE 122(3) | found | DOI 10.1016/j.jfineco.2016.09.008; 203 citations; no abstract shown. The authors' 2010 working paper ([record](https://consensus.app/papers/details/670e7c8aa77251b2afbd54c9ad57d9b2/?utm_source=claude_desktop)) reports two things. Calls and distributions are both more likely and larger when public valuations rise and when liquidity conditions tighten. In 2007–09 the unexplained component of calls spiked and distributions plummeted. | [link](https://consensus.app/papers/details/86bf821b6ba65861a9da20fed7862965/?utm_source=claude_desktop) |
| 19 | Shleifer & Vishny (2011), *Fire sales in finance and macroeconomics*, JEP 25(1) | found | DOI 10.1257/jep.25.1.29; 700 citations. The abstract's own definition is "forced sales of assets in which high-valuation bidders are sidelined, typically due to debt overhang problems afflicting many specialist bidders simultaneously". **[Inference]** That definition fits ADIC better than the phrase §2.6 quotes, which the verification log found in the paper's text. | [link](https://consensus.app/papers/details/38094184238d5f8f9fe8944a05e37411/?utm_source=claude_desktop) |
| 20 | Sorensen, Wang & Yang (2014), *Valuing private equity*, RFS 27(7) | found | Record year 2013; DOI 10.1093/rfs/hhu013; 110 citations. "LPs may just break even" is confirmed. The abstract adds "Debt is cheap and reduces these costs". | [link](https://consensus.app/papers/details/15cb135a45b35616b82e97bf090f24ae/?utm_source=claude_desktop) |
| 21 | Takahashi & Alexander (2002), *Illiquid alternative asset fund modeling*, JPM 28(2) (†) | not re-searched (found in Stream 04 and 06 checks) | DOI 10.3905/jpm.2002.319836; 68 citations. **Orphan reference:** it is never cited in the dossier text. | [link](https://consensus.app/papers/details/da7ee2d8587e575f99e3a36a590d2be6/?utm_source=claude_desktop) |
| 22 | Adelman & Mersereau (2008), *Relaxations of weakly coupled stochastic dynamic programs*, OR 56(3) | found | DOI 10.1287/opre.1070.0445; 226 citations. Lagrangian versus approximate-LP relaxations, plus column generation, are confirmed. | [link](https://consensus.app/papers/details/80a57bb0dc385a61b01ce4b8ac352bfd/?utm_source=claude_desktop) |
| 23 | Andersen & Broadie (2004), *Primal-dual simulation algorithm…*, MS 50(9) | found | DOI 10.1287/mnsc.1040.0258; 459 citations. | [link](https://consensus.app/papers/details/b5d77078565b58c5849c929352fb999c/?utm_source=claude_desktop) |
| 24 | Brown, Smith & Sun (2010), *Information relaxations and duality in stochastic dynamic programs*, OR 58(4) | found | DOI 10.1287/opre.1090.0796; 248 citations. | [link](https://consensus.app/papers/details/3f70ae2e398c524592d67076b594acd0/?utm_source=claude_desktop) |
| 25 | Cariño et al. (1994), *The Russell–Yasuda Kasai model*, Interfaces 24(1) | not re-searched (found in Stream 01 check) | DOI 10.1287/inte.24.1.29. The full title adds ": An Asset/Liability Model for a Japanese Insurance Company Using Multistage Stochastic Programming". | [link](https://consensus.app/papers/details/1f457f819115540d83c7b7d4289b0b66/?utm_source=claude_desktop) |
| 26 | Everett (1963), *Generalized Lagrange multiplier method…*, OR 11(3) | found | DOI 10.1287/opre.11.3.399; 1,382 citations. "Fail-safe" and "independent activities" are in the abstract. | [link](https://consensus.app/papers/details/d7ed8686080c5fb690d81a462b5f023a/?utm_source=claude_desktop) |
| 27 | Howard (1966), *Information value theory*, IEEE TSSC 2(1) (†) | found | DOI 10.1109/tssc.1966.300074; 1,060 citations. The abstract adds that eliminating uncertainty about several independent factors jointly can be worth a different amount from the sum of eliminating each separately. **[Inference]** This matters for per-input EVPI on decision cards. | [link](https://consensus.app/papers/details/916059b396215e39b1d19ad8894baf81/?utm_source=claude_desktop) |
| 28 | Kouwenberg (2001), *Scenario generation and stochastic programming models for ALM*, EJOR 134(2) | not re-searched (found in Stream 01 check) | DOI 10.1016/s0377-2217(00)00261-7. | [link](https://consensus.app/papers/details/6189d2de3bb559f69ad7e1576d594bd5/?utm_source=claude_desktop) |
| 29 | Longstaff & Schwartz (2001), *Valuing American options by simulation…*, RFS 14(1) | found | DOI 10.1093/rfs/14.1.113; 3,480 citations; venue label "The Finance". | [link](https://consensus.app/papers/details/80f7e4358bab534185c423e61ad9ce8e/?utm_source=claude_desktop) |
| 30 | Udell & Boyd (2016), *Bounding duality gap for separable problems with linear constraints*, arXiv:1410.4158 | found (minor fix: journal version) | Published in *Computational Optimization and Applications*, DOI 10.1007/s10589-015-9819-4; record year 2014 (the arXiv year); 39 citations; volume and pages not shown. Abstract wording matches §2.5. | [link](https://consensus.app/papers/details/ffa6fb7a6af7504883b03862a628825a/?utm_source=claude_desktop) |
| 31 | Whittle (1988), *Restless bandits…*, J. Appl. Prob. 25(A) (†) | found | DOI 10.2307/3214163; 1,423 citations. The Lagrange multiplier on the activation constraint defines the index. | [link](https://consensus.app/papers/details/11f485608054529693d52b6d7d17e464/?utm_source=claude_desktop) |
| 32 | Arkes & Blumer (1985), *The psychology of sunk cost*, OBHDP 35(1) | found | DOI 10.1016/0749-5978(85)90049-4; 2,564 citations. The abstract adds two points. A sunk cost inflated estimated success probabilities. The effect "was not lessened by having taken prior courses in economics". | [link](https://consensus.app/papers/details/430c3de70ba65268a9b0b76602aae5d2/?utm_source=claude_desktop) |
| 33 | Shefrin & Statman (1985), *The disposition to sell winners too early and ride losers too long…*, JF 40(3) | found (record-quality note) | DOI 10.1111/j.1540-6261.1985.tb05002.x; 2,158 citations. The Consensus record omits the subtitle ": Theory and Evidence", shows "Unknown Journal" and carries an unrelated abstract (on security-paper manufacture). The attribution is confirmed by citing abstracts, e.g. [Odean 1996](https://consensus.app/papers/details/0a000b2e6f935848916b78f445f32894/?utm_source=claude_desktop). | [link](https://consensus.app/papers/details/27df25b96d0d5a5f8a5d3abcd4198f17/?utm_source=claude_desktop) |
| 34 | Tversky & Kahneman (1974), *Judgment under uncertainty: heuristics and biases*, Science 185(4157) (†) | found | DOI 10.1126/science.185.4157.1124; 38,904 citations. Anchoring and adjustment is in the abstract. | [link](https://consensus.app/papers/details/2a6602227c8159d48fe8bdd0abb79e5b/?utm_source=claude_desktop) |
| 35 | Davis & Norman (1990), transaction-cost no-trade regions (named only) | found: upgrade to verified | "Portfolio Selection with Transaction Costs", *Math. Oper. Res.*, DOI 10.1287/moor.15.4.676; 1,320 citations. Optimal trading occurs at the boundaries of a wedge-shaped region. Pages 676–713 per a citing abstract ([record](https://consensus.app/papers/details/a4659bf8e4cc5f71b75e65c925f6df0c/?utm_source=claude_desktop)). | [link](https://consensus.app/papers/details/dd44cc19665454fdb5e7b33341cbc00d/?utm_source=claude_desktop) |
| 36 | Myers & Majd (1990), abandonment value (named only) | found (working-paper record; published version confirmed by WebSearch) | Consensus indexes only the 1983 MIT working paper "Calculating abandonment value using option pricing theory" (S. Myers et al., 78 citations). It models abandonment as an American put on a dividend-paying asset. WebSearch: Myers & Majd (1990), "Abandonment value and project life", *Advances in Futures and Options Research* 4:1–21 (§7). | [link](https://consensus.app/papers/details/73cc34a3ed675559af4088b5a0ca2c87/?utm_source=claude_desktop) |
| 37 | Hawkins (2003), Lagrangian decomposition of weakly coupled DPs (named only) | found: upgrade to verified | J. T. Hawkins, "A Lagrangian decomposition approach to weakly coupled dynamic optimization problems and its applications", PhD thesis, MIT Sloan School / Operations Research Center, 2003; 87 citations. The record title misspells "Langrangian". | [link](https://consensus.app/papers/details/c5c7d1378de15b7fa78ce4c42d20e5b4/?utm_source=claude_desktop) |
| 38 | Gribik, Hogan & Pope (2007), convex-hull pricing (named only) | **mismatched (year)** | "Market-Clearing Electricity Prices and Energy Uplift", P. Gribik et al., record year **2008**, 251 citations, no venue or DOI. The abstract compares three pricing models for uniform prices and energy uplift. The dossier's 2007 could not be confirmed here. | [link](https://consensus.app/papers/details/4e56045db7795352a73950e5dd29f759/?utm_source=claude_desktop) |

---

## 3. Annotated bibliography (25 papers)

None of the 25 is cited by dossier 08. Entries are grouped by the design question they inform.

### A. Real options when liquidity is scarce

**1. [Investment under uncertainty with financial constraints](https://consensus.app/papers/details/e521e348363650419eabc63c7669c095/?utm_source=claude_desktop)**
- P. Bolton et al. · 2019 · *J. Econ. Theory* · 70 citations · DOI 10.1016/j.jet.2019.06.008
- *Finding:*
  - The paper builds an integrated theory of investment, equity issuance, liquidation and savings with growth and abandonment options.
  - "Limited financial slack significantly erodes the value of growth & abandonment options."
  - Firms prefer projects with front-loaded cash flows.
  - Hoarding internal funds can delay investment substantially.
  - Mature firms sit in payout, inaction or liquidation regions.
- *Relevance to ADIC:* This is the closest published analogue to the dossier's thesis. **[Inference]**
  - It supports LAPV's preference for early distributions.
  - It supports the finding that the option to sell is weakest when liquidity is needed.
  - κ^irr must be computed conditional on ADIC's liquidity state.
  - The inaction region is the formal counterpart of the dossier's no-trade bands.

**2. [Market Timing, Investment, and Risk Management](https://consensus.app/papers/details/e1bcae07d2be506289e7506e93615bb2/?utm_source=claude_desktop)**
- P. Bolton et al. · 2012 (record) · venue shown "Social Science Research Network" · 384 citations · DOI 10.2139/ssrn.1571149
- *Finding:*
  - When external financing conditions are stochastic, firms hoard cash and time favourable windows.
  - Market timing can make investment fall, and the marginal value of cash rise, as financial slack increases.
  - A constrained firm may gamble.
- *Relevance:* **[Inference]**
  - NAV-loan and secondary markets open and close. ℓ is therefore window-dependent and need not be monotone.
  - This argues for a financing-window state variable, separate from the asset regime z (§4.1).
  - It also argues for drawing committed facilities and selling while windows are open. That is the dossier's "pre-emptive liquidity" with a formal basis.

**3. [A q Theory of Internal Capital Markets](https://consensus.app/papers/details/2311defdb8b152ab80b1442580fa023f/?utm_source=claude_desktop)**
- Min Dai et al. · 2024 · *The Journal of Finance* · 9 citations · DOI 10.1111/jofi.13318. The record title shows a typesetting artifact ("q$q$"). NBER version: [record](https://consensus.app/papers/details/586e994df1775cc398a8b4429bd27206/?utm_source=claude_desktop).
- *Finding:* For a multi-division firm with costly external finance:
  - allocation follows both productivity and risk;
  - firms may spin off *productive* divisions to raise liquidity;
  - diversification can reduce value in low-liquidity states;
  - corporate socialism makes liquidity less valuable;
  - division investment is set by marginal q relative to the marginal value of cash.
- *Relevance:* This maps one-to-one onto ADIC. The seven groups are divisions and Corporate Finance is the internal capital market. **[Inference]**
  - The "marginal q ÷ marginal value of cash" rule is the division-level analogue of the dossier's ADD test against ℓ.
  - Selling good assets for liquidity can be optimal. The dossier's "misuse" guard (§8) should test whether ℓ is credible, not forbid such sales.

**4. [Valuing the option to invest in an incomplete market](https://consensus.app/papers/details/4656177aa2d556bc8f3d138431407c73/?utm_source=claude_desktop)**
- Vicky Henderson · 2007 · *Mathematics and Financial Economics* · 183 citations · DOI 10.2139/ssrn.569865
- *Finding:*
  - Risk aversion and idiosyncratic (unhedgeable) risk erode option value and lower the exercise threshold.
  - In some parameter regions complete- and incomplete-market models give opposite signals.
  - Higher volatility can speed up investment.
- *Relevance:* PE fund risk is largely unspanned for ADIC. **[Inference]** Complete-market LSMC on simulator paths will tend to overstate the waiting option (κ^irr). Compute it under ADIC's SDF or by utility indifference (§4.2).

### B. Where the liquidity shadow price comes from

**5. [The Shadow Costs of Illiquidity](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop)**
- Kristy A. E. Jansen et al. · 2022 · *JFQA* · 3 citations · DOI 10.1017/s0022109022000473 · also flagged by Stream 01
- *Finding:*
  - Illiquidity that only distorts allocation carries low shadow costs.
  - Costs are high when illiquidity restricts consumption.
  - They are therefore high for short-term investors, for investors facing substantial liquidity shocks, and for investors who want a large illiquid allocation.
- *Relevance:* ADIC has all three features: mandated 5–10% payouts, a DPI drought and a ~60% illiquid book. **[Inference]**
  - That supports a material ℓ.
  - ℓ should come mainly from the distribution-floor and survival rows (ν, μ), and be near zero where payouts are covered.

**6. [Valuing Thinly Traded Assets](https://consensus.app/papers/details/6c8df97df07f58b48b77c15948c6c242/?utm_source=claude_desktop)**
- F. Longstaff · 2017 (record) · *Manag. Sci.* · 2 citations · DOI 10.1287/mnsc.2016.2718. NBER version: [record](https://consensus.app/papers/details/5bec3828dbf85a0386c2a3874c4de614/?utm_source=claude_desktop), 2014, 19 citations, DOI 10.3386/w20589.
- *Finding:*
  - Illiquidity is modelled as a restriction on the stopping rules an investor can follow when selling.
  - Discounts can approach 30–50%.
  - "Immediacy… is valued much more than ongoing liquidity."
  - Holders of illiquid enterprises have strong incentives to raise payouts, which creates agency conflicts.
  - Illiquidity and volatility are entangled.
- *Relevance:* This is the SELL-as-constrained-stopping formulation the dossier proposes, by an author it already cites twice. **[Inference]**
  - Front-load ℓ.
  - Treat GP-level NAV loans and recaps that accelerate distributions as partly an agency response to LP illiquidity when ADIC votes on LPACs.

**7. [Valuing a Lost Opportunity: An Alternative Perspective on the Illiquidity Discount](https://consensus.app/papers/details/6f6ed257f1425818b50eeab791add2f4/?utm_source=claude_desktop)**
- Jamil Baz et al. · 2020 · venue label "Unknown Journal" (the DOI indicates *Journal of Portfolio Management*) · 3 citations · DOI 10.3905/jpm.2020.1.197
- *Finding:*
  - The illiquidity discount reflects the opportunity cost of forgone trading opportunities.
  - More skilled investors require larger discounts.
  - The equilibrium discount reflects *perceived* rather than actual skill.
- *Relevance:* It formalizes context §1A point 5: dry powder for Secondaries and Capital Solutions has option value. **[Inference]** ℓ should credit that opportunity set in stress. But because the discount follows perceived skill, opportunity forecasts should be credibility-weighted α* from the fusion stream, not group assertions.

**8. [The Public Market Equivalent and Private Equity Performance](https://consensus.app/papers/details/d8f3498ac57a5fe8865988cd887d8d99/?utm_source=claude_desktop)**
- M. Sørensen et al. · 2015 · *Financial Analysts Journal* · 95 citations · DOI 10.2469/faj.v71.n4.4 · also flagged by Stream 04
- *Finding:*
  - PME is equivalent to valuing with Rubinstein's dynamic CAPM.
  - The discount rate should approximate the return on the investor's overall wealth portfolio, and "may vary across investors, even for the same fund".
- *Relevance:* This gives investor-specific valuation a formal basis, and it is the natural fix for verification-log R2. **[Inference]** The scenario state prices π_{s,t} should embed an SDF built on ADIC's own total portfolio.

**9. [Liquidity and Portfolio Choice: A Unified Approach](https://consensus.app/papers/details/87606279740d57b4b0350e859446911b/?utm_source=claude_desktop)**
- W. Kinlaw et al. · 2013 · *The Journal of Portfolio Management* · 29 citations · DOI 10.3905/jpm.2013.39.2.019 · also flagged by Stream 02
- *Finding:*
  - Liquidity used to raise expected utility is a shadow asset attached to tradable assets.
  - Liquidity used to prevent utility from falling is a shadow liability attached to non-tradables.
  - Both map into expected return and risk.
  - Liquidity serves to exploit opportunities as well as to meet demands.
- *Relevance:* **[Inference]** This is an IC-friendly way to split ℓ into a defensive part (survival and distribution rows) and an offensive part (opportunity value, item 7).

### C. SELL as optimal stopping; secondary pricing

**10. [Optimal liquidation of an illiquid asset under stochastic liquidity and regime shifting](https://consensus.app/papers/details/924560c825e05f3a969385f3f1b22fc8/?utm_source=claude_desktop)**
- Etienne Chevalier et al. · 2013 · SSRN · 0 citations · DOI 10.2139/ssrn.2254973
- *Finding:*
  - Unfavourable bids are always available, but favourable offers arrive rarely.
  - The liquidity premium implicit in bids evolves stochastically (mean-reverting CIR).
  - The arrival rate of good offers follows a regime-shifting Markov chain.
  - The result is a multidimensional optimal-stopping problem with explicit solutions for power and log utility.
- *Relevance:* This is a ready template for the dossier's view that the real option is on the discount p_t (§2.2(a)). **[Inference]** Use it as a closed-form benchmark to validate LSMC.

**11. [Optimal Timing for an Indivisible Asset Sale](https://consensus.app/papers/details/11ef6d4a78625f5e81269d130f28a10f/?utm_source=claude_desktop)**
- Jonathan Evans et al. · 2008 · *Mathematical Finance* · 33 citations · DOI 10.1111/j.1467-9965.2008.00347.x
- *Finding:* With power utility and other wealth in a complete market, it is optimal to sell the non-traded asset the first time its value exceeds a certain proportion of the agent's trading wealth.
- *Relevance:* **[Inference]**
  - The sale boundary depends on the ratio of the illiquid position to liquid wealth. Add that ratio to the SELL policy state (§4.1).
  - Large concentrated co-investments should reach the boundary sooner.

**12. [Optimal stopping and divestment timing under scenario ambiguity and learning](https://consensus.app/papers/details/70344425d3d15aa6ba579b133695f05f/?utm_source=claude_desktop)**
- Andrea Mazzon et al. · 2024 · arXiv · 2 citations · DOI 10.48550/arxiv.2408.09349
- *Finding:*
  - Divestment is posed as optimal stopping with learning under smooth ambiguity aversion.
  - A minimax result reduces it to a series of standard stopping problems with learning.
  - Examples include divesting a coal plant under transition-scenario ambiguity.
- *Relevance:* **[Inference]** This gives a principled answer to open question 5 (robust or expected duals). Run SELL timing as ambiguity-averse stopping over the Tier-1 misspecification ensemble, instead of mixing robust and expected duals across actions. Verification-log R9(c) notes that mixing duals breaks "one currency".

**13. [Liquidity Provision in the Secondary Market for Private Equity Fund Stakes](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop)**
- R. Albuquerque et al. · 2018 · SSRN · 11 citations · DOI 10.2139/ssrn.3182481 · also flagged by Streams 04, 05 and 06
- *Finding:*
  - Demand responses to aggregate liquidity shocks are negatively related to contemporaneous bids, more so for funds likely sold in low-liquidity times.
  - These responses are unrelated to future NAV-to-NAV returns.
  - Discounts therefore track liquidity provision.
- *Relevance:* **[Inference]** Model p_t with an aggregate liquidity-supply factor, not only with fundamentals. This justifies the dossier's stress multiplier h(z) and the covariance between bids and ℓ.

**14. [Liquidity in the Secondaries Private Equity Market](https://consensus.app/papers/details/9bc5ce1dd6415d858fb1193b5b1b3466/?utm_source=claude_desktop)**
- Anya Kleymenova et al. · 2012 · working paper · 10 citations · no DOI · also flagged by Streams 04, 05 and 06
- *Finding:* A fund interest is more liquid when:
  - the fund is larger and buyout-focused;
  - it has less undrawn capital and fewer distributions;
  - the manager's funds have traded before.

  More non-traditional bidders and favourable markets help. Liquidity proxies are positively associated with winning bids.
- *Relevance:* This is LP-secondary evidence for the dossier's unfunded-share penalty (§2.7). It answers verification-log R11, which noted that the Jefferies quote concerned GP-led deals. **[Inference]** Use bid count and dispersion as bid-model features.

### D. Price decomposition at scale

**15. [Technical Note – On the Strength of Relaxations of Weakly Coupled Stochastic Dynamic Programs](https://consensus.app/papers/details/e8af8aeb5faf5365ac03e17f5d8289af/?utm_source=claude_desktop)**
- David B. Brown et al. · 2022 · *Oper. Res.* · 8 citations · DOI 10.1287/opre.2022.2287. SSRN version: [record](https://consensus.app/papers/details/392fc18540815419b6cb52eb13630994/?utm_source=claude_desktop).
- *Finding:*
  - Approximate-LP and Lagrangian bounds are very close and often identical, so Lagrangian relaxation "should usually be the preferred choice".
  - The relaxation gap is bounded independently of the number of subproblems.
  - It is zero for binary actions with unimodular linking constraints.
- *Relevance:* This updates the dossier's Adelman & Mersereau (2008) reference. **[Inference]** Use Lagrangian decomposition for multi-quarter SELL timing across funds, with a formal small-gap argument.

**16. [Dynamic Programs with Shared Resources and Signals: Dynamic Fluid Policies and Asymptotic Optimality](https://consensus.app/papers/details/5d959b6409d9539aaaf4a9781599a0eb/?utm_source=claude_desktop)**
- David B. Brown et al. · 2020 (record; SSRN DOI) · *Oper. Res.* · 18 citations · DOI 10.2139/ssrn.3728111
- *Finding:*
  - Subsystems share random exogenous signals and random budgets; the examples include capital budgeting with randomly evolving funding.
  - A dynamic fluid relaxation (deterministic subsystem states, stochastic signals) gives asymptotically optimal policies.
  - "Competing state-of-the-art approaches… in general fail to provide asymptotic optimality."
- *Relevance:* ADIC's holdings are coupled by shared regimes (z_t, p_t, ℓ_t) and by a random liquidity budget. **[Inference]** Prices should be signal-conditioned, not static.

**17. [Index Policies and Performance Bounds for Dynamic Selection Problems](https://consensus.app/papers/details/0981d1842ec350f08266e02296f350bc/?utm_source=claude_desktop)**
- David B. Brown et al. · 2020 · *Manag. Sci.* · 80 citations · DOI 10.1287/mnsc.2019.3342
- *Finding:*
  - Lagrangian index policies and bounds for repeated selection under a cardinality constraint are asymptotically optimal when there are many items.
  - Mixed policies and tie-breaking "play an essential role" and can affect performance in surprising ways.
- *Relevance:* This backs the dossier's liquidity index ℓ*_i. **[Inference]** The "split" (marginal) assets are exactly where tie-breaking and mixing rules matter, so the IC's handling of them must be explicit.

### E. Behaviour and the decision card

**18. [Looking for Someone to Blame: Delegation, Cognitive Dissonance, and the Disposition Effect](https://consensus.app/papers/details/a0f9802ccd9354a1bc4a57ba8caf9c9e/?utm_source=claude_desktop)**
- T. Chang et al. · 2016 · *Journal of Finance* · 153 citations · DOI 10.1111/jofi.12311
- *Finding:*
  - The disposition effect applies only to non-delegated assets such as individual stocks.
  - Delegated assets such as mutual funds show "a robust reverse-disposition effect".
  - Making delegation more salient strengthens the reversal.
- *Relevance:* **[Inference]** Most of ADIC's holdings are delegated (PE funds, hedge funds). The likelier bias is selling losing managers too fast and blaming the GP, not riding losers (§5, row 1).

**19. [The Impact of Salience on Investor Behavior: Evidence from a Natural Experiment](https://consensus.app/papers/details/45258c5053a65f3795e7982968a2cd43/?utm_source=claude_desktop)**
- Cary Frydman et al. · 2019 · *The Journal of Finance* · 162 citations · DOI 10.1111/jofi.12851
- *Finding:* A shock that made the purchase price more salient, without changing information, causally increased the disposition effect by 17%.
- *Relevance:* This is causal support for the decision card's design (§6.14): since-inception IRR and paid-in capital greyed out, and NAV shown only next to economic NAV. **[Inference]** It generalizes from brokerage investors to an IC.

**20. [Institutional Investors, Past Performance, and Dynamic Loss Aversion](https://consensus.app/papers/details/fbe3a65b54c85dd19de4116c4c87d30d/?utm_source=claude_desktop)**
- P. O'connell et al. · 2009 · *JFQA* · 123 citations · DOI 10.1017/s0022109009090048
- *Finding:*
  - Large institutional currency investors are not prone to the disposition effect.
  - They "aggressively reduce risk following losses" and mildly increase it after gains.
  - The pattern is stronger later in the year and among older funds.
- *Relevance:* **[Inference]** The institutional bias to guard against is procyclical de-risking after drawdowns, i.e. crisis selling. That is the dossier's own central warning. The IC agent should flag "sell because we lost" as firmly as "hold because of sunk cost".

### F. Value of information on decision cards

**21. [The Value of Value of Information](https://consensus.app/papers/details/58efc229925853bd9fc7b730ec70d808/?utm_source=claude_desktop)**
- S. Eckermann et al. · 2010 · *PharmacoEconomics* · 122 citations · DOI 10.2165/11537370-000000000-00000
- *Finding:* EVPI "provide[s] neither a necessary nor a sufficient condition" for judging whether further research is worthwhile. Choose by maximizing EVSI minus expected cost across designs.
- *Relevance:* This supports verification-log R8. **[Inference]** For each diligence action (re-underwrite, a third bidder), decision cards should show EVSI net of cost, not "spend part of the EVPI".

**22. [The Relationship Between Perfect and Imperfect Information in a Two-Action Risk-Sensitive Problem](https://consensus.app/papers/details/759535db43b2551ea70de079a8e86d52/?utm_source=claude_desktop)**
- J. Bickel · 2008 · *Decision Analysis* · 49 citations · DOI 10.1287/deca.1080.0118
- *Finding:*
  - The value of imperfect information has a closed form in two-action problems with normal priors and exponential utility.
  - Its value relative to perfect information is greatest when the decision maker is indifferent between the actions.
  - A signal with correlation ρ is worth ρ, or ρ², times the value of perfect information under stated conditions.
- *Relevance:* SELL versus KEEP is a two-action problem, and close calls (P ≈ 45% in Example 1) are where diligence pays most. **[Inference]** EVSI ≈ ρ- or ρ²-scaled EVPI gives an auditable formula for cards.

### G. Fire sales, pre-emptive liquidity and leverage

**23. [Do Asset Fire Sales Exist? An Empirical Investigation of Commercial Aircraft Transactions](https://consensus.app/papers/details/1f12c0aa9d425ed1b582ce98535bd082/?utm_source=claude_desktop)**
- Todd C. Pulvino · 1998 · *Journal of Finance* · 670 citations · DOI 10.1111/0022-1082.00040
- *Finding:*
  - Financially constrained airlines receive lower prices than unconstrained rivals.
  - They sell to industry outsiders more often in downturns.
  - Unconstrained airlines step up buying when prices are depressed.
- *Relevance:* **[Inference]** This is empirical grounding for both sides of ℓ. Constrained sellers get worse prices, which argues for selling early. Unconstrained buyers earn the discount, which is the opportunity value of Secondaries dry powder.

**24. [Dynamic Investment, Capital Structure, and Debt Overhang](https://consensus.app/papers/details/c10673afc91154b6b87c6a1af1c7aa3a/?utm_source=claude_desktop)**
- Suresh Sundaresan et al. · 2015 · *The Review of Corporate Finance Studies* · 174 citations · DOI 10.2139/ssrn.952540
- *Finding:*
  - Firms choose conservative leverage to limit debt overhang on future growth-option exercise.
  - Debt seniority and priority structures have significant effects on exercise and leverage.
- *Relevance:* **[Inference]**
  - LEVER today uses up the option to deploy capital in stress. Add that forgone option value to λ_Lev.
  - Model facility priority explicitly (portfolio facility versus asset-level NAV loans).

### H. Corporate Finance as internal capital market

**25. [The Dark Side of Internal Capital Markets: Divisional Rent-Seeking and Inefficient Investment](https://consensus.app/papers/details/75689033f1ce55ef910f66907b8387a8/?utm_source=claude_desktop)**
- D. Scharfstein et al. · 2000 · *Journal of Finance* · 1,760 citations · DOI 10.1111/0022-1082.00299
- *Finding:*
  - Division managers' rent-seeking can subvert an internal capital market.
  - The CEO may pay them with preferential capital allocations.
  - The result is "socialism", in which weaker divisions are subsidized by stronger ones.
- *Relevance:* **[Inference]** Groups may lobby to keep weak holdings or to win LEVER budgets. One published ℓ curve, scored actions and logged overrides are the safeguards (§4.6).

---

## 4. Missed-but-important papers: design implications

### 4.1 State variables to add (per scenario s, quarter t)

| Variable | Basis | Owner | Use |
|---|---|---|---|
| **Liquid-wealth ratio** w_{s,t} = (cash + haircut HQLA) / total NAV | The sale boundary scales with the illiquid position relative to liquid wealth ([Evans et al. 2008](https://consensus.app/papers/details/11ef6d4a78625f5e81269d130f28a10f/?utm_source=claude_desktop)). The marginal value of cash and the payout / inaction / liquidation regions depend on the cash–capital ratio (Bolton et al. 2011; [Bolton et al. 2019](https://consensus.app/papers/details/e521e348363650419eabc63c7669c095/?utm_source=claude_desktop)). | Corporate Finance | **[Inference]** Report ℓ as a function of w, not only of t. Use w in the SELL policy. |
| **Financing-window regime** f_{s,t} ∈ {open, tight, closed}, for NAV / fund facilities and the secondary market | Stochastic financing conditions create hoarding and timing motives, and can make the marginal value of cash rise with slack ([Bolton et al. 2012](https://consensus.app/papers/details/e1bcae07d2be506289e7506e93615bb2/?utm_source=claude_desktop)) | Corporate Finance (facilities); Capital Solutions (quotes) | **[Inference]** Drives s_B and availability A_{s,t}, and the timing of REFI and LEVER. Keep it separate from the asset regime z. |
| **Secondary liquidity-supply factor** q_{s,t}: dedicated dry powder, bid counts, bid dispersion | Discounts track liquidity provision ([Albuquerque et al.](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop)). Bidder count and mix price into winning bids ([Kleymenova et al.](https://consensus.app/papers/details/9bc5ce1dd6415d858fb1193b5b1b3466/?utm_source=claude_desktop)). | Secondaries group, under the context file's conflict controls | **[Inference]** Replaces part of h(z) in p_{i,s,t}, and links bids to ℓ. |
| **Offer-arrival intensity** a_{s,t} | Good offers arrive rarely, at regime-dependent rates ([Chevalier et al.](https://consensus.app/papers/details/924560c825e05f3a969385f3f1b22fc8/?utm_source=claude_desktop)). Lower acquirer arrival enlarges the optimal sell-out region ([Nishihara et al. 2021](https://consensus.app/papers/details/40eb3d8a45a15df8ae88919c60a5c5ad/?utm_source=claude_desktop)). The offer rate can be raised at a cost ([Hobson et al. 2019](https://consensus.app/papers/details/f34d864c870950d9864f145f0e2ab1b5/?utm_source=claude_desktop)). | Secondaries | **[Inference]** Makes "run a competitive process" a priced control (effort → arrival rate). This separates price improvement from information, as verification-log R8 requires. |
| **NAV-quality flag** (GP fundraising window; strategy) | Some GPs boost reported NAVs while fundraising, while top performers under-report ([Brown et al. 2019](https://consensus.app/papers/details/fd6f1f1f8a1d5b87a04484478701209a/?utm_source=claude_desktop); [Barber et al. 2017](https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop)). Since 2000, VC NAVs have been more aggressively biased than buyout NAVs ([Jenkinson et al.](https://consensus.app/papers/details/44d91cea6b8b53b481621e6ed4e6ef9e/?utm_source=claude_desktop)). | PE, Secondaries | **[Inference]** Adjust reported NAV toward economic NAV before applying p (dossier pitfall 9). |
| **Fund-class tax status** | Secondary discounts include a tax component when tax-exempt sellers hold fund classes that are unfavourable to taxable buyers ([Mason et al. 2023](https://consensus.app/papers/details/480f7ceb6b345835a7453cf1ee01ca84/?utm_source=claude_desktop)) | Secondaries; Legal | **[Inference]** Strip the tax component before comparing implied spreads with ℓ (calibration targets 5 and 7). ADIC's tax status is not stated in the context file. |
| **Belief state with learning** (already in X_t) | Under drift uncertainty, optimal liquidation follows an increasing, time-dependent boundary ([Ekström et al. 2011](https://consensus.app/papers/details/d2cbad71122e55149adfe7ce44d2bd55/?utm_source=claude_desktop)). Ambiguity-averse stopping with learning reduces to standard problems ([Mazzon et al.](https://consensus.app/papers/details/70344425d3d15aa6ba579b133695f05f/?utm_source=claude_desktop)). | Fusion stream; PE | **[Inference]** Make the SELL boundary time-dependent and ambiguity-aware. |

### 4.2 Models
1. **κ^irr under ADIC's own preferences.** **[Inference]**
   - Run LSMC under ADIC's SDF, or by utility indifference, instead of complete-market LSMC. [Henderson (2007)](https://consensus.app/papers/details/4656177aa2d556bc8f3d138431407c73/?utm_source=claude_desktop) and Bolton et al. (2019) both imply lower waiting values when risk is unspanned or slack is limited.
   - Validate against closed-form cases from Chevalier et al. and Evans et al.
   - Keep the dual upper bounds the dossier already cites. [Haugh et al.](https://consensus.app/papers/details/2f8e256edd7050af8d5956da33471254/?utm_source=claude_desktop) (*Oper. Res.*, record year 2018, DOI 10.1287/opre.1030.0070) is the duality reference underlying Andersen & Broadie.
   - [Stentoft (2004)](https://consensus.app/papers/details/9c2adc2799ed525dac7a05cdcd54bceb/?utm_source=claude_desktop) gives LSMC convergence results.
2. **SELL as constrained stopping.** [Longstaff (2017)](https://consensus.app/papers/details/6c8df97df07f58b48b77c15948c6c242/?utm_source=claude_desktop) links restricted stopping rules to illiquidity discounts, and finds immediacy priced far above ongoing liquidity. **[Inference]** Test the brief's "9% then 4%" term structure against that front-loaded shape rather than imposing it.
3. **Strip sales.** [Henderson et al. (2020)](https://consensus.app/papers/details/0c3aa67c130e5150af6a60a525518c9e/?utm_source=claude_desktop) solve multiple optimal stopping with partial liquidation. Under S-shaped, reference-dependent preferences the investor sells pieces at distinct thresholds above the reference level. **[Inference]**
   - Use the model normatively for strip sizing.
   - Use it also as a behavioural benchmark. An IC strip pattern that clusters just above NAV suggests NAV anchoring.
4. **Decomposition.** **[Inference]**
   - (a) Use Lagrangian decomposition for multi-quarter timing ([Brown et al. 2022](https://consensus.app/papers/details/e8af8aeb5faf5365ac03e17f5d8289af/?utm_source=claude_desktop)).
   - (b) Condition prices on the regime signal with a dynamic fluid relaxation: deterministic fund states, stochastic regimes ([Brown et al. 2020, shared signals](https://consensus.app/papers/details/5d959b6409d9539aaaf4a9781599a0eb/?utm_source=claude_desktop)).
   - (c) Write tie-breaking and mixing rules for the split assets ([Brown et al. 2020, index policies](https://consensus.app/papers/details/0981d1842ec350f08266e02296f350bc/?utm_source=claude_desktop)). Indices defined from optimal dual variables have a long pedigree ([Bertsimas et al. 2000](https://consensus.app/papers/details/14f637b6f6b958f5b43d97d21f976dbe/?utm_source=claude_desktop)).
   - (d) The electricity literature computes exact convex-hull prices by Dantzig–Wolfe column generation ([Andrianesis et al.](https://consensus.app/papers/details/a417a53c80985ca4853c974f02adc352/?utm_source=claude_desktop)). This matches the dossier's "asset scoring as the pricing subproblem".
   - (e) Prices from fixing integer variables perform well when the MILP gap is very small ([Byers et al. 2022](https://consensus.app/papers/details/8677f6f31f775ebd9a10044d870fb7d5/?utm_source=claude_desktop)). That supports the dossier's step 5, re-solving the LP with the selected actions fixed.
   - (f) Test formulation dependence. Convex-hull prices can change between formulations of the same problem ([Zhao et al. 2021](https://consensus.app/papers/details/088ea61f66185ebd965ff10756412268/?utm_source=claude_desktop)), so the aggregated coupling rows in §6.4 can move ℓ.
5. **Value of information.** **[Inference]**
   - Report EVSI net of cost for each diligence action ([Eckermann et al.](https://consensus.app/papers/details/58efc229925853bd9fc7b730ec70d808/?utm_source=claude_desktop)), using [Bickel (2008)](https://consensus.app/papers/details/759535db43b2551ea70de079a8e86d52/?utm_source=claude_desktop) for the two-action SELL / KEEP choice where its normal-prior, exponential-utility assumptions are acceptable.
   - Use nested Monte Carlo with enough inner samples for partial EVPI. Maxima of Monte Carlo estimates are biased upward ([Brennan et al. 2007](https://consensus.app/papers/details/ebf9ca1047945eeb8f0f8f14ef9e5f60/?utm_source=claude_desktop)).
   - Never add per-input EVPIs. They are not additive (Howard 1966; [Samson et al. 1989](https://consensus.app/papers/details/bd2745d5823354dd8c8c90af31217325/?utm_source=claude_desktop)).
   - EVPI-based sensitivity combines the probability of a decision change with its payoff, which is more informative than distance to a threshold ([Felli et al. 1998](https://consensus.app/papers/details/a6e1ca47f8fd5408be37e97ce0ab773c/?utm_source=claude_desktop)). Show it next to the flip thresholds.

### 4.3 Parameters and calibration

| Parameter | Dossier default | Evidence | Proposed change |
|---|---|---|---|
| ℓ fallback | 9% / 9% / 4% (brief) | Shadow costs are high only when illiquidity restricts consumption ([Jansen et al.](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop)). One investor case study found the shadow cost of liquidity below 1% ([Sharaiha et al. 2014](https://consensus.app/papers/details/49ef8f8a3f2255569f04a3dadb8185de/?utm_source=claude_desktop)). Breakeven returns match observed returns for moderately risk-tolerant LPs with up to 40% in PE ([Bollen et al.](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop)). | **[Inference]** Apply the fallback only in states where the 5% distribution floor or the survival row binds. Elsewhere default to the implied spread of the marginal MCL source, and show the range. |
| κ^irr | LSMC; perfect-learning upper bound | Henderson 2007; Bolton et al. 2019 | **[Inference]** Show the incomplete-market κ^irr next to the current figure, and expect it to be lower. |
| κ^GP | 0.3–1% of NAV for core GPs with re-up intent | Endowments' edge came from early access to top VC and disappeared after 1999 ([Sensoy et al. 2014](https://consensus.app/papers/details/f4aeacf09dae5b4c9e87522d93f16191/?utm_source=claude_desktop)). There is little investable persistence ([Korteweg et al. 2017](https://consensus.app/papers/details/a0bf5a58fd485ea895fabd5c39cb76ce/?utm_source=claude_desktop)). LP skill is worth 1–2 pp a year in one sample ([Cavagnaro et al. 2019](https://consensus.app/papers/details/ce8a4e711b4e52be85a0d0b03ffe44dd/?utm_source=claude_desktop)). Top LPs get preferential access to top alternative vehicles ([Lerner et al. 2021](https://consensus.app/papers/details/94e5f805d12f5f58b961fbb751940fc3/?utm_source=claude_desktop)). | **[Inference]** Lower the prior on re-up selection value. Price access to co-investments and alternative vehicles as the main channel; that value sits with the Co-investment group. |
| Secondary price p | Strategy × age × geography × h(z) | The discount for lack of marketability is U-shaped in beta and highest for low-beta infrastructure and real estate ([Patel 2026](https://consensus.app/papers/details/64f833009af051b588c84d39bb3c5bc5/?utm_source=claude_desktop)). Liquidity supply (Albuquerque). Fund traits (Kleymenova). | **[Inference]** Add beta and liquidity-supply terms. Re-check Example 2's core-plus infrastructure asset (β 0.5) against a larger discount. |
| Concentrated co-investments | LAPV at r_h | Certainty-equivalent returns are 2–8% below average fund performance under skill uncertainty and diversification constraints ([Gredil et al. 2020](https://consensus.app/papers/details/062234d9141e5e2b843e6c5c5a3e736d/?utm_source=claude_desktop), working paper) | **[Inference]** Apply a certainty-equivalent haircut that scales with concentration. |
| Unfunded-share penalty in bids | Justified by GP-led evidence (R11) | Less undrawn capital makes interests more liquid and raises winning bids (Kleymenova). NAV and unfunded liabilities can be priced separately ([Giommetti et al.](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop)). | Keep the penalty, cite Kleymenova, and estimate it from adviser bid data. |
| Price impact | Concave in size per half-year | Divestiture returns are lower in industry-wide distress; the effect is driven by constrained sellers and core assets and rises with deal size ([Finlay et al.](https://consensus.app/papers/details/75653a7181bd528a94d27d1212961005/?utm_source=claude_desktop)). Constrained sellers get lower prices (Pulvino). | **[Inference]** Make impact state-dependent (higher when q is low) as well as size-dependent. |

### 4.4 Constraints
- **No-trade bands.** **[Inference]**
  - Davis & Norman's wedge-shaped region is now verified.
  - In multiperiod mean–variance with proportional costs, the no-trade region is a parallelogram; under market impact one trades to the boundary of a state-dependent region ([Mei et al. 2016](https://consensus.app/papers/details/5c64c32179705e39885e01e4aee2ba86/?utm_source=claude_desktop)).
  - The frictionless shadow price lies inside the bid–ask band ([Kallsen et al. 2010](https://consensus.app/papers/details/d1817eea5e0a584ab60ead8ef2d6bcbf/?utm_source=claude_desktop)). Define the HOLD band as [p*_sell, p*_buy] and trade only to its edge. This formalizes the hysteresis of pitfall 7.
- **Leverage and option preservation.** **[Inference]**
  - Conservative leverage preserves future option exercise, and seniority matters ([Sundaresan et al.](https://consensus.app/papers/details/c10673afc91154b6b87c6a1af1c7aa3a/?utm_source=claude_desktop)).
  - Debt overhang distorts long-lived investment most ([Hennessy 2004](https://consensus.app/papers/details/29266a7848465c99995e85a85b06a097/?utm_source=claude_desktop)).
  - So the interaction term I(e, b) in LEVER = ADD + REFI + I may not be small in stress. Estimate it with forgone deployment options included.
- **Cheap but unstable funding.** Repo-style funding carries shadow costs: it requires higher liquid reserves and raises the cost of long-term debt ([Klimenko et al. 2016](https://consensus.app/papers/details/535f2d64925952b9a23d803735d1f86f/?utm_source=claude_desktop)). **[Inference]** Charge uncommitted lines (MCL step 4) for contingent liquidity.
- **Commitment pacing.** Realistic commitment-timing strategies give modest gains at best, because investors cannot time calls or exits ([Brown et al. 2020](https://consensus.app/papers/details/b5880343ab7b57ebaf68b353dfff48da/?utm_source=claude_desktop)). **[Inference]** Cap the capacity credited to MCL step 10 in years 1–2.

### 4.5 Objective
- **Give the here-and-now LP an objective whose duals carry ADIC's SDF** (verification-log R2). **[Inference]**
  - PME theory says to discount at the return on the investor's overall wealth portfolio (Sørensen et al. 2015).
  - [Gredil et al. (2019)](https://consensus.app/papers/details/6d1e275e4a435f189165927c393d7da1/?utm_source=claude_desktop) develop portfolio-specific SDFs for assets that standard benchmarks do not span, with a finite-sample bias correction for long-duration NPV inference.
- **Distribution within the 5–10% band is a payout-region decision** (Bolton et al. 2011, 2019). ℓ is highest when payouts are restricted (Jansen et al.). **[Inference]** Report ℓ conditional on whether the 5% floor binds. The owner's ν^own (open question 1) then decides how often that happens.

### 4.6 Agent and IC design
- **Two-sided behaviour flags.** **[Inference]**
  - Keep the sunk-cost check. Arkes & Blumer show that economics training does not remove the bias, so the process must.
  - Add "sell because we lost" and "blame the GP" checks ([Chang et al.](https://consensus.app/papers/details/a0f9802ccd9354a1bc4a57ba8caf9c9e/?utm_source=claude_desktop); [O'Connell et al.](https://consensus.app/papers/details/fbe3a65b54c85dd19de4116c4c87d30d/?utm_source=claude_desktop)).
  - A literature review found no disposition effect in the institutional studies it covered ([Aren et al. 2016](https://consensus.app/papers/details/aeae5ec3830e5d609386d6e653d03e6d/?utm_source=claude_desktop)).
- **Salience and framing.** **[Inference]**
  - Keep cost basis and since-inception IRR greyed out ([Frydman et al.](https://consensus.app/papers/details/45258c5053a65f3795e7982968a2cd43/?utm_source=claude_desktop)).
  - Fewer people persevered with a failing project when the alternative was selling to someone who could use the materials than when it was selling for scrap value at the same price ([Arkes 1996](https://consensus.app/papers/details/b96fce2a96ba5738bd187f0736e5771f/?utm_source=claude_desktop)).
  - Framing a transaction as a transfer rather than a sale mitigated the disposition effect ([Niehaus et al. 2014](https://consensus.app/papers/details/57588359dca35d8ab249e32a33a12027/?utm_source=claude_desktop)).
  - Present SELL as a reallocation to a natural owner, next to the re-buy test.
- **Corporate Finance as internal capital market.** **[Inference]**
  - Headquarters creates value by winner-picking even when it cannot relax firm-wide constraints ([Stein 1997](https://consensus.app/papers/details/6a07d86c178059559396b6c5f188a331/?utm_source=claude_desktop)).
  - Rent-seeking produces socialism (Scharfstein et al.).
  - Powerful managers capture cash windfalls and overinvest ([Glaser et al. 2013](https://consensus.app/papers/details/848f600b945b589a8924c56d7af118ab/?utm_source=claude_desktop)).
  - Committing *not* to reallocate part of the funds can preserve incentives ([Brusco et al. 2005](https://consensus.app/papers/details/40acbb6c7a165685bd32a0c4dbb5897a/?utm_source=claude_desktop)).
  - Budgets with layers of approval counter opportunism ([Hoang et al.](https://consensus.app/papers/details/60b81a1ffdb95bef9df302df23e13088/?utm_source=claude_desktop)).
  - Rules that follow:
    - one published ℓ curve per run, owned by Corporate Finance;
    - DPI windfalls allocated by Score, not by negotiation;
    - group overrides logged with the flip thresholds accepted;
    - a protected minimum budget per group.
- **VOI across groups.** When groups compute VOI separately under one organizational utility, rank information sources by certainty-equivalent increase, not expected-utility increase ([Abbas et al. 2024](https://consensus.app/papers/details/f2bcc4ca625b5817a3c0e2d78fbeb30c/?utm_source=claude_desktop)).
- **LPAC test agent.** **[Inference]**
  - GP-level NAV loans and recaps that speed up distributions can be an agency response to LP illiquidity (Longstaff 2017). Score them at ADIC's ℓ.
  - For continuation vehicles, a CFA Institute report estimates that 80–90% of legacy investors cash out. The GP sits on both sides, and a fair, competitive process is the main safeguard ([Deane et al. 2025](https://consensus.app/papers/details/23aed12e6aa650ac9d160c9cf1c5ed5a/?utm_source=claude_desktop)). Record process quality on SELL-versus-ROLL cards.
  - A VC fund's limited life leads the GP to continue bad projects ([Kandel et al. 2011](https://consensus.app/papers/details/a8debc8f9ade5075a1db4b8dc0d07e81/?utm_source=claude_desktop)). Apply a governance discount to HOLD for tail-end funds.
- **Group mapping.** **[Inference]**
  - **Secondaries** (hybrid book): supplies q, a and bid models under conflict controls. Its dry powder is the opportunity component of ℓ (Baz et al.; Pulvino).
  - **Capital Solutions:** supplies f and s_B quotes.
  - **PE:** SELL candidates and κ^GP.
  - **Co-investment:** concentration haircut and the Evans et al. boundary.
  - **Corporate Finance:** owns ℓ, the MCL curve, facilities and the distribution policy.

---

## 5. Papers that challenge the dossier's recommendations

| # | Paper(s) | Dossier position | What the evidence says | Proposed change |
|---|---|---|---|---|
| 1 | [Chang et al. 2016](https://consensus.app/papers/details/a0f9802ccd9354a1bc4a57ba8caf9c9e/?utm_source=claude_desktop); [O'Connell et al. 2009](https://consensus.app/papers/details/fbe3a65b54c85dd19de4116c4c87d30d/?utm_source=claude_desktop); [Aren et al. 2016](https://consensus.app/papers/details/aeae5ec3830e5d609386d6e653d03e6d/?utm_source=claude_desktop) | §2.6: the LP disposition effect is "selling near-NAV winners while riding tail-end losers" | Delegated assets show a reverse disposition effect. Institutions cut risk after losses. A review found no disposition effect in the institutional studies it covered. | **[Inference]** Make the flag two-sided, and weight procyclical "sell after losses" at least as heavily. |
| 2 | [Sensoy et al. 2014](https://consensus.app/papers/details/f4aeacf09dae5b4c9e87522d93f16191/?utm_source=claude_desktop); [Korteweg et al. 2017](https://consensus.app/papers/details/a0bf5a58fd485ea895fabd5c39cb76ce/?utm_source=claude_desktop) | §2.6 and §2.7: κ^GP motivated by endowments' re-up skill (Lerner et al. 2007) | The edge came from early access to top VC and vanished after 1999. There is little investable persistence. | Lower the prior. Price access through co-investments and alternative vehicles ([Lerner et al. 2021](https://consensus.app/papers/details/94e5f805d12f5f58b961fbb751940fc3/?utm_source=claude_desktop)). Keep showing the break-even κ. |
| 3 | [Henderson 2007](https://consensus.app/papers/details/4656177aa2d556bc8f3d138431407c73/?utm_source=claude_desktop); [Bolton et al. 2019](https://consensus.app/papers/details/e521e348363650419eabc63c7669c095/?utm_source=claude_desktop); [Huchzermeier et al. 2001](https://consensus.app/papers/details/379faf3aad825a61b089f9bd00703d7a/?utm_source=claude_desktop) | §2.2 and Ex. 1: waiting option worth $9.9m (an upper bound under perfect learning) | Unspanned risk and limited slack erode option value. More variability can even *reduce* the value of flexibility. | **[Inference]** Report incomplete-market κ^irr. The magnitudes fall, and the qualitative "sell pre-emptively" conclusion gets stronger. |
| 4 | [Brown et al. 2020 (shared signals)](https://consensus.app/papers/details/5d959b6409d9539aaaf4a9781599a0eb/?utm_source=claude_desktop); [Nadarajah et al. 2024](https://consensus.app/papers/details/173afec25a135dbb9a5e46f6e011ab73/?utm_source=claude_desktop) | §2.5: Everett and Udell–Boyd justify static price decomposition | Standard weakly coupled methods can lose asymptotic optimality when subsystems share signals. Dualizing linking constraints "averages away combinatorial information". | Use regime-conditioned prices. Keep the exact MILP as the decider, as the dossier already does. |
| 5 | [Eckermann et al. 2010](https://consensus.app/papers/details/58efc229925853bd9fc7b730ec70d808/?utm_source=claude_desktop); [Bickel 2008](https://consensus.app/papers/details/759535db43b2551ea70de079a8e86d52/?utm_source=claude_desktop) | §6.11: "spend part of the ~$33m EVPI on competitive tension and a re-underwrite" | EVPI is neither necessary nor sufficient. Decide on EVSI minus cost. | Replace it with EVSI net of cost per diligence action (consistent with verification-log R8). |
| 6 | [Jansen et al. 2022](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop); [Sharaiha et al. 2014](https://consensus.app/papers/details/49ef8f8a3f2255569f04a3dadb8185de/?utm_source=claude_desktop); [Bollen et al.](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop) | §6.8: ℓ fallback of 9% / 9% / 4% | The shadow cost depends on whether illiquidity restricts payouts. One case study finds it below 1%. Observed returns break even with up to 40% in PE. | Use the fallback only in payout-binding states; otherwise use the marginal MCL spread. |
| 7 | [Damaraju et al.](https://consensus.app/papers/details/23b28a59568e51fb95f6928f49aa2b9a/?utm_source=claude_desktop) (*Strategic Management Journal*) | §2.7: "sell strips and keep a stub" as a mitigant | In corporate divestitures, staged modes create options worth less than either not divesting or divesting fully | **[Inference]** This is a different setting. Treat strips as a priced alternative, justified by GP relationship value or price impact, not as a default. |
| 8 | [Barber et al. 2017](https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop); [Brown et al. 2019](https://consensus.app/papers/details/fd6f1f1f8a1d5b87a04484478701209a/?utm_source=claude_desktop) | §2.7: "avoid selling during the GP's fundraise" | Some GPs manage NAVs upward around fundraising; top performers under-report | **[Inference]** Fundraising windows need a NAV-quality adjustment, not only a relationship rule. A bid quoted on an inflated NAV overstates the cash-equivalent price. |
| 9 | [Brown et al. 2020](https://consensus.app/papers/details/b5880343ab7b57ebaf68b353dfff48da/?utm_source=claude_desktop) (*JFE*) | §6.7, MCL step 10: commitment pacing | Realistic timing of commitments yields modest gains at best | Treat pacing as a slow lever with small credited capacity in years 1–2. |
| 10 | [Mason et al. 2023](https://consensus.app/papers/details/480f7ceb6b345835a7453cf1ee01ca84/?utm_source=claude_desktop) | §6.9, targets 5 and 7: the implied spread of executed sales ≈ ℓ | Secondary discounts include a tax component | **[Inference]** Remove the tax component before comparing with ℓ. |
| 11 | [Wang et al. 2012](https://consensus.app/papers/details/fd02d9b3f4645c8a884efdcbf8ab0f46/?utm_source=claude_desktop) (*JFE*) | §2.3: ℓ implicitly rises monotonically as liquidity becomes scarcer | With a flexible exit option, the private marginal value of liquidity *falls* as liquidity falls and exit becomes more likely | **[Inference]** Expect non-monotone ℓ near the SELL boundary. Treat it as a diagnostic, not an error. |
| 12 | [Sundaresan et al. 2015](https://consensus.app/papers/details/c10673afc91154b6b87c6a1af1c7aa3a/?utm_source=claude_desktop) | §2.4: LEVER ≡ ADD + REFI + I, with I small | Leverage changes future option exercise through debt overhang | **[Inference]** Estimate I with forgone deployment options included; it may not be small in stress. |

**Evidence that supports contested points**
- **Unfunded-share penalty.** Kleymenova et al. supply the LP-market evidence that verification-log R11 found missing.
- **Greyed-out cost basis.** Frydman et al. show causally that purchase-price salience increases the disposition effect.
- **Pre-emptive liquidity.** Three sources support it:
  - [Pulvino 1998](https://consensus.app/papers/details/1f12c0aa9d425ed1b582ce98535bd082/?utm_source=claude_desktop);
  - [Shleifer et al. 1992](https://consensus.app/papers/details/fa39990f63685ac6a7cbf5f932b9e7c2/?utm_source=claude_desktop), on cheap assets in bad times when industry buyers are constrained; also flagged by Stream 06;
  - [Nishihara et al. 2021](https://consensus.app/papers/details/40eb3d8a45a15df8ae88919c60a5c5ad/?utm_source=claude_desktop), where lower asset liquidity enlarges the sell-out region.

---

## 6. Usage message

No sign-up, upgrade or usage message appeared in any of the 42 Consensus results.

---

## 7. Search log and limitations

**Consensus queries** (in order; S = seed, R = refinement, C = citation look-up)
1. C: Paper millionaires: how valuable is stock to a stockholder who is restricted from selling it
2. C: Holmstrom Tirole Private and public supply of liquidity
3. C: Acharya Pedersen asset pricing with liquidity risk
4. C: Brennan Schwartz evaluating natural resource investments
5. C: Valuing American options by simulation: a simple least-squares approach
6. C: Andersen Broadie primal-dual simulation algorithm for pricing multidimensional American options
7. C: Whittle restless bandits: activity allocation in a changing world
8. S: disposition effect institutional investors
9. C: Shefrin Statman the disposition to sell winners too early and ride losers too long: theory and evidence
10. C: Everett generalized Lagrange multiplier method for solving problems of optimum allocation of resources
11. C: Udell Boyd bounding duality gap for separable problems with linear constraints
12. C: Bolton Chen Wang a unified theory of Tobin's q, corporate investment, financing, and risk management
13. C: Faulkender Wang corporate financial policy and the value of cash
14. C: Smart institutions, foolish choices: the limited partner performance puzzle
15. C: McDonald Siegel the value of waiting to invest
16. C: Longstaff optimal portfolio choice and the valuation of illiquid securities
17. C: Longstaff portfolio claustrophobia: asset pricing in markets with illiquid assets
18. S: real options divestment abandonment timing
19. S: shadow price of liquidity asset liability management
20. S: funds transfer pricing liquidity banks
21. S: valuing illiquid assets investor liquidity needs
22. S: optimal stopping selling illiquid asset
23. R: secondary market private equity fund stakes pricing discount liquidity provision
24. C: Dimmock Wang Yang endowment model and modern portfolio theory illiquid alternatives lock-up
25. C: Sorensen Wang Yang valuing private equity limited partner illiquidity management fees carry break even
26. C: Robinson Sensoy cyclicality, performance measurement, and cash flow liquidity in private equity
27. C: Brunnermeier Pedersen market liquidity and funding liquidity margin spirals
28. C: Shleifer Vishny fire sales in finance and macroeconomics
29. R: relaxations of weakly coupled stochastic dynamic programs Lagrangian relaxation index policies performance bounds
30. C: Arkes Blumer psychology of sunk cost escalation of commitment divestment decisions
31. R: continuation funds GP-led secondaries limited partners sell or roll conflicts returns
32. R: net asset value NAV loans private equity fund-level borrowing distributions to limited partners
33. R: Howard information value theory expected value of perfect and sample information decision analysis
34. C: Information Value Theory IEEE Transactions on Systems Science and Cybernetics 1966
35. C: valuing private equity investments strip by strip stochastic discount factor generalized public market equivalent
36. C: Tversky Kahneman judgment under uncertainty heuristics and biases anchoring 1974
37. C: Davis Norman portfolio selection with transaction costs no-trade region
38. C: Myers Majd abandonment value and project life
39. C: Gribik Hogan Pope market-clearing electricity prices and energy uplift convex hull pricing
40. C: Hawkins Lagrangian decomposition approach to weakly coupled dynamic optimization problems thesis
41. R: internal capital markets headquarters allocates scarce liquidity across divisions marginal value of cash spinoffs
42. R: real options investment timing with debt financing leverage debt overhang optimal exercise

**WebSearch** (1 query: Myers & Majd 1990)
- The published version appears in a Springer article's bibliography as "Myers SC, Majd S (1990) Abandonment value and project life. Adv Future Option Res 4:1–21" ([unpaywall](https://unpaywall.org/10.1007%2Fs00500-007-0162-2)).
- IDEAS lists the 1983 MIT Sloan working paper 1462-83, "Calculating abandonment value using option pricing theory" ([IDEAS](https://ideas.repec.org/p/mit/sloanp/2056.html)).
- A citing paper describes its method: numerical valuation of the option to abandon over a known project life, with constant or stochastic salvage value ([realoptions.org](https://realoptions.org/papers2004/ClarkRealOp2004.pdf)).
- The full text of the 1990 paper was not read.

**Limitations**
- Abstracts only; no full texts were read.
- No findings are claimed for records without abstracts:
  - Robinson & Sensoy (2016, JFE);
  - Baker (2024) and Reddy (2024) on NAV financing;
  - Long et al. (2020) on behavioural abandonment decisions, whose abstract was truncated.
- Several records carry working-paper or online years (Bolton et al. 2012; Dimmock et al.; Holmström & Tirole; Kahl et al.; Sorensen et al.; Brown et al.).
- Three listed references rely on sibling-stream Consensus records rather than a new search (rows 21, 25 and 28).
- Overlap with other streams:
  - Jansen et al. 2022 (Stream 01);
  - Kinlaw et al. (Stream 02);
  - Sørensen et al. 2015 (Stream 04);
  - Albuquerque et al., Kleymenova et al., Bollen et al., Giommetti et al. and Sensoy et al. (Streams 04–06);
  - Shleifer et al. 1992, plus the bank FTP papers by Dermine, Choudhry and Lindblom (Stream 06).

  These are repeated here only where they change SELL / HOLD / REFINANCE / LEVER valuation. The orchestrator may want one canonical reference set across streams.
