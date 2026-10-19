# ADIC TPA Lab: Literature Synthesis

*18 October 2026. This file consolidates the 23 per-topic reviews in `research/literature/`: topic streams 01–14 and group streams G1–G9. It tests them against two documents, called "main" (`research/00_SYNTHESIS.md`) and "groups" (`research/groups/01_GROUPS_SYNTHESIS.md`) below.*

*Conventions:*
- *Links are copied exactly as the per-topic files recorded them.*
- *"Missed" means the paper is cited in no dossier, cluster file, addendum or synthesis.*
- *Evidence is abstract-level.*

## 1. Summary

The 23 reviews re-checked every dossier's citations and searched for literature the research did not use.

**Organizational facts used throughout** (confirmed by the user):
- the PE group allocates to funds as an LP;
- Secondaries is a hybrid book of fund interests and direct positions;
- Corporate Finance owns the treasury function, including:
  - portfolio borrowing and facilities;
  - overlay collateral (VM and IM);
  - distributions to the owner;
  - publication of the FTP curve.

**Findings**

1. **Citation integrity is good but not clean** (§2).
   - **Counts.** Of 574 citations checked, 12 were not found and 24 were mismatched. Of the 12, ten exist, one is corroborated only by its venue, and one is unidentified. No fabricated reference turned up.
   - **Usage errors.** Sixteen further usage problems misstate what a source says. The worst reverses the sign of a barrier correction in the co-investment dossier, which overstates survival.
   - **Unchecked works.** At least 69 cited works went unchecked when the search quota ran out.
   - **Action.** Fix everything in §2 before the IC sees it.
2. **The architecture holds.** The literature supports:
   - one state-contingent liquidity price λ;
   - quantity envelopes;
   - never maximizing P(10%);
   - the de Finetti payout barrier;
   - pacing as the slow lever;
   - regime-aware robustness;
   - an agentic lab in which deterministic engines own every number;
   - a structured IC.
3. **Twelve recommendations should change** (§4):
   - make P's liquid-first waterfall a tuned, state-dependent policy;
   - count Corporate Finance's revolver at ≤50% in the joint oil–crisis state, and new facilities at zero;
   - price the owner band at the owner's cost, which peaks in demand busts, and treat owner-directed investments as an obligation;
   - require a shortfall exponent above 1, and re-impose the Tier 1B floor on a rolling basis;
   - test tighter joint chance-constraint surrogates for T6;
   - put ambiguity on regime persistence, and show DRO and robust satisficing as one frontier;
   - carry the regime as a belief state in V, and certify P with dual bounds;
   - shrink FBE weights toward equal, and recalibrate every linear pool;
   - cut hedge-fund α priors to about zero, and give Private Credit a fund-age prior;
   - make the convex sleeve beat an equal-cost cash buffer;
   - derive the FTP risk row from the owner's loss function, not an Euler CVaR split;
   - have the IC pre-commit contingent plans instead of re-aggregating beliefs each meeting.
4. **Some questions only ADIC's data can settle.** No study tests any of the following (§4.17):
   - PE underwriting projections against outcomes;
   - LP access lost after a skipped re-up;
   - internal capital markets inside asset owners;
   - contingency-funding design.

**Caveats.**
- The group reviews ran after the Consensus quota was spent. They used OpenAlex, Semantic Scholar, Crossref, arXiv and web search instead.
- Preprints from 2025–26 are design input, not settled evidence.

## 2. Citation integrity across all dossiers

### 2.1 Counts

Figures are checked / not found / mismatched.
- **Topic streams:** 01 37/0/0; 02 21/1/3; 03 25/1/1; 04 31/2/4; 05 8/0/1; 06 26/1/0; 07 42/2/3; 08 35/0/1; 09 29/0/0; 10 25/0/4; 11 20/0/0; 12 25/2/2; 13 14/1/1; 14 16/0/0.
- **Group streams:** G1 22/0/0; G2 17/1/0; G3 9/1/0; G4 13/0/0; G5 49/0/1; G6 20/0/0; G7 15/0/0; G8 50/0/2; G9 25/0/1.
- **Total: 574 / 12 / 24.**

**Unchecked because of the quota:** 37 works in 10, 12 in G3, 10 in 14, 6 in 11 and 4 in 13. Check them after the quota resets on 1 November 2026.

### 2.2 Not found (12)

1. **[02] de Finetti (1957).**
   - Not indexed. A citing record gives *Trans. XVth Int. Congress of Actuaries* 2 (1957) 433–443 ([record](https://consensus.app/papers/details/8e6d66eec4c75444af49fc3bc3155f2b/?utm_source=claude_desktop)).
   - Confirm the title.
2. **[03] Merton (1993).**
   - Exists: [NBER chapter c6102](https://www.nber.org/chapters/c6102), ch. 7 in Clotfelter & Rothschild (eds), U. Chicago Press, pp. 211–242 (one listing gives 211–236). Preceded by NBER WP 3820.
   - Add these details.
3. **[04] Ljungqvist & Richardson (2003).** Exists as [NBER WP 9454](https://ideas.repec.org/p/nbr/nberwo/9454.html).
4. **[04] Getmansky, Lo & Makarov (2004).** Exists: *JFE* 74(3):529–609, DOI 10.1016/j.jfineco.2004.04.001.
5. **[06] Gorton & Metrick, "Haircuts" (NBER WP 15273).** Exists. Cite the published version, FRB St. Louis *Review* 92(6):507–520 (2010).
6. **[07] Mincer & Zarnowitz (1969).** Exists: [NBER chapter](https://www.nber.org/chapters/c1214.pdf), pp. 3–46 in Mincer (ed.). Add the pages.
7. **[07] Nordhaus (1987).** Exists: *REStat* 69(4):667–674.
8. **[12] Lange et al. (2026), *The Agentic Scientist*, arXiv:2610.18933.** Too new to be indexed; confirmed by secondary coverage.
9. **[12] Song (2026).** Confirmed at [ICLR 2026, 2nd Workshop on Advances in Financial AI](https://www.iclr.cc/virtual/2026/10016534). The 0.04→0.41 figure checks.
10. **[13] *The Agentic Scientist*.** Confirmed by web search and by the local copy `inputs/agentic_scientist_2610.18933v1.txt`.
11. **[G2] "Rode et al."**
    - Cited in §2.6 for a 60bp lead fee against a 75bp syndicate fee, via a CFA Institute report, with no reference entry.
    - Unidentified. Take the citation from the report's footnote or drop the figure.
12. **[G3] Getmansky, Lo & Makarov.** Mentioned only in the body. Add a reference entry, as in item 4.

### 2.3 Mismatched (24)

- **02 (3).**
  - Ennis (2020), SSRN 3614875 → Ennis (2021), "Endowment Performance", *J. Investing*, DOI 10.3905/joi.2021.1.166 ([record](https://consensus.app/papers/details/7a715cd5f109565f8ec21d59aba046bc/?utm_source=claude_desktop)). The −1.1% to −1.8% alphas belong to size cohorts, not to the 43 endowments.
  - "−1.87% a year vs passive, 12 years to June 2020", cited to the same paper → probably Ennis (2021), "Failure of the Endowment Model", *JPM*, DOI 10.3905/jpm.2021.1.217 ([record](https://consensus.app/papers/details/c5b7fa6fe1d857a2a6eaa2a26138ea89/?utm_source=claude_desktop)). The figure is not in the abstract, so verify it.
  - CFA Institute TPA guide, cited without authors → Urwin et al. (2026), "The Total Portfolio Approach (TPA): A Practical Guide for Navigating the Transition to TPA", DOI 10.56227/26.1.20 ([record](https://consensus.app/papers/details/5ad8650fbd4a59b1837db3c44daac405/?utm_source=claude_desktop)).
- **03 (1).** Moutanabbir & Noureldin (2018), ERF WP 1172 → Moutanabbir et al. (2020), "Optimal asset allocation and consumption rules for commodity-based sovereign wealth funds", *IREF*, DOI 10.1016/j.iref.2020.06.014 ([record](https://consensus.app/papers/details/5182918fd69a5116b305d7f557bb70c3/?utm_source=claude_desktop)). Re-check the 0.01–0.07pp hedging demand against it.
- **04 (4).**
  - Luxenberg et al., described as "preprint only" → ICAIF '22, DOI 10.1145/3533271.3561769.
  - Sorensen, Wang & Yang → *RFS* 27(7):1977–2021, not 27(2).
  - Nadauld et al., NBER WP 22404 → *JFE* 132(3):158–181 (2019), DOI 10.1016/j.jfineco.2018.11.007. The seller PME is 0.976, not 0.974.
  - Jeet et al. (2026) → "A Crucial Enhancement to the Takahashi–Alexander Cash Flow Model", DOI 10.3905/jpmi.2026.1.010.
- **05 (1).** WilmerHale (ref 19) → ["Trends in the Private Equity Secondary Market"](https://www.wilmerhale.com/en/insights/publications/trends-in-the-private-equity-secondary-market-march-april-2009), ABA *Business Law Today* 18(4), 2009.
- **07 (3).**
  - Cooke, "26 of 33 in-sample" → [Colson & Cooke (2017)](https://consensus.app/papers/details/dbe7edfbdd19501caa1d757e57fd4aad/?utm_source=claude_desktop), *RESS*.
    - Performance weights win 32 of 33 cases in sample.
    - 26 of 33 is the out-of-sample validity index.
    - Out-of-sample statistical accuracy is below equal weights.
  - BGG β 1.05/1.20 and VC risk 38%, taken from an earlier WP → the published *RFS* 36(3):945–986 values: β 1.0/1.4 and total risk 33%/40% ([record](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop)).
  - Nadauld seller PME 0.974 → 0.976.
- **08 (1).** Gribik, Hogan & Pope (2007) → "Market-Clearing Electricity Prices and Energy Uplift". The index dates it 2008, and 2007 is unconfirmed ([record](https://consensus.app/papers/details/4e56045db7795352a73950e5dd29f759/?utm_source=claude_desktop)).
- **10 (4).**
  - Mohajerin Esfahani & Kuhn → add the subtitle ": performance guarantees and tractable reformulations"; DOI 10.1007/s10107-017-1172-1.
  - Gao & Kleywegt → *Math. of OR* 48(2):603–655 (2023), DOI 10.1287/moor.2022.1275.
  - Xie → *Math. Programming* 186(1–2):115–155 (2021), DOI 10.1007/s10107-019-01445-5.
  - Shu, Yu & Mulvey → *J. Asset Management* 25(5):493–507 (2024), DOI 10.1057/s41260-024-00376-x.
- **12 (2).**
  - Gao, Jiang & Yan → current title "Detecting Lookahead Bias in LLM Forecasts" ([record](https://consensus.app/papers/details/8282b37d1f965203af8e1822f55077b8/?utm_source=claude_desktop)).
  - "Sakana AI (2026), The AI Scientist in *Nature*" → "Towards end-to-end automation of AI research", *Nature* 651(8107):914–919, DOI 10.1038/s41586-026-10265-5 ([record](https://consensus.app/papers/details/9f1753d006d85b0fa97d161df8bc951a/?utm_source=claude_desktop)). Authors, per *The Agentic Scientist*: Lu, Lu, Lange, Yamada, Hu, Foerster, Ha, Clune.
- **13 (1).** The same *Nature* paper, cited as a blog → same correction. The 69% balanced accuracy and 6.33 are blog figures; the abstract reports a 70% workshop acceptance rate.
- **G5 (1).** Almgren & Chriss (2000) → *J. Risk* 3(2):5–39 (2001), DOI 10.21314/jor.2001.041.
- **G8 (2).**
  - Lamont (1997), pp. 57–82 → *JF* 52(1):83–109. Pages 57–82 are Carhart (1997), and the verification log wrongly accepted them.
  - Shin & Stulz, working-paper pointer NBER w5639 → drop it, because w5639 is a different 1996 paper. The *QJE* 113(2):531–552 citation is correct.
- **G9 (1).** Modrák et al. (2023) → *Bayesian Analysis* 20(2):461–488 (2025), DOI 10.1214/23-BA1404.

### 2.4 Usage errors that change a number, model or claim (16)

1. **G4, barrier correction.**
   - The Broadie–Glasserman–Kou shift is written exp(−0.5826σ√Δ), which raises survival. The calculation script applies no correction at all.
   - Use κD·exp(+0.5826σ√Δ) (*Math. Finance* 7(4):325–349).
   - Re-run every barrier statistic built on quarterly monitoring. If the wipe-out and LTV-breach rates in groups finding 8 used it, they are understated.
2. **G4, Bhardwaj–Gupta–Howell.** The ×2.4 belongs to +84% total debt. At φ = 0.25, use about ×1.1 (OLS) to ×1.7 (IV).
3. **G4, Lopez-de-Silanes, Phalippou & Gottschalg.**
   - "Scale" there means simultaneous investments, not deal size ("Giants at the Gate…", *JFQA* 50(3):377–411).
   - Add the missing references: Axelson et al. (2013), *JF* 68(6):2223–2267; the Axelson–Sorensen–Strömberg draft that is the source of β = 2.3; Kaplan & Strömberg's pages.
4. **G3.**
   - Cai & Haque's 33/52/39% recoveries are KBRA DLD data, not S&P. Main already has this right.
   - "Smoothing ≈0.5 (BGG)" is stream 04's derivation, not a BGG figure.
5. **05.** Bollen & Sensoy's "5–10pp" comes from the 2015 WP. The published abstract says breakeven returns roughly equal observed returns for moderately risk-tolerant LPs with up to 40% in PE.
6. **G2.** Boyer et al. (2018 WP) is superseded by *JF* 78(2):835–885 (2023). Re-check the β > 2 versus β < 0.5 contrast against it.
7. **09.**
   - Jeanne & Rancière's benchmark is 9.1% in the 2011 *EJ* version, not the WP's 10.1%.
   - Lo (2002)'s headline result is that Sharpe ratios can be overstated by up to 65%.
   - Moreira & Muir is disputed out of sample.
   - Kaminski & Lo (2014), which carries the drawdown stop, is unchecked.
8. **G9.**
   - The Campbell & Sharpe anchor calibrates w_a or ρ_f, not w_u.
   - These figures come from working papers, not the published abstracts: BGG's λ 0.951 and 4.6% noise; HJK's "over 200 programs" and PME 1.20/1.11.
   - No stream checked Aas et al. (2009), López de Prado (2018) or Borisov et al. (2023).
9. **14, Schwenk (1990), which the dossier overstates.** Use this wording: "DA beat an expert-recommendation baseline. DI's advantage over the expert approach was not demonstrated on relatively ill-structured tasks, and neither DA nor DI beat the other."
10. **14, Parasuraman & Manzey.**
    - Training does not prevent automation bias, so drills monitor it rather than prevent it.
    - Corrections carried from the companion file:
      - Fogliato et al. studied 19 veterinary radiologists and found no accuracy gain.
      - Hackenburg et al. is *Science* 390(6777), DOI 10.1126/science.aea3884.
      - Salvi et al. is "On the conversational persuasiveness of GPT-4", DOI 10.1038/s41562-025-02194-6.
      - Cite Wang, Morgenstern & Dickerson as arXiv 2402.01908 v3, since its *NMI* venue is unconfirmed.
11. **12.**
    - α-investing controls mFDR, so name the error criteria: Holm FWER within a contract, mFDR across contracts.
    - Add the DSR non-normality term.
    - FINSABER's abstract says "deteriorate significantly", not "often vanish".
    - Apply Smith–Winkler shrinkage.
    - Kosmos was 79.4% accurate despite full citation coverage.
12. **13.**
    - The "59%" MLReplicate figure is worded two ways. Check it against arXiv 2605.16616.
    - The definition of specification gaming rests on a blog post. Add Skalse (2022) and Pan (2022).
    - SR 26-2 / OCC 2026-13 supersede SR 11-7; main already reflects this.
13. **10.**
    - Quote Glasserman & Xu verbatim: "very little computational effort beyond that required to evaluate performance under the baseline nominal model".
    - Heitsch & Römisch (2003) is a two-stage method; use their 2009 paper (§3.1).
    - The source of the ENS diagnostic is Meucci (2012).
    - Link Meucci (2008) to arXiv 1012.2848.
14. **G7.**
    - The Gorton–Metrick haircut spike was in bilateral repo; tri-party repo was stable.
    - Li–Strahan–Zhang's 2020 line draws were met with Fed support, which an oil–fiscal stress may lack.
    - "Central Treasury" should read Corporate Finance.
15. **G6.**
    - Cai & Haque's 31% covers public and private pensions together.
    - Berrospide et al.'s table says 6.4%; the text says 6.6%.
    - The "+1–2pp" attributed to Rintamäki & Steffen is second-hand.
16. **G8 and G2.** The Glaser et al. quotes, and the Albuquerque details on young funds, VIX and funding costs, are not in the abstracts. Cite the source page, or tag them [C].

### 2.5 Reference hygiene (no claim changes)

- **Missing entries:** Klaassen (2002) in 01; Föllmer & Leukert (2000) in 11; six body-only works in G3; four body-only methods in G7 (Glasserman–Kang–Kang, Gerber–Shiu, Little, Clopper–Pearson).
- **Metadata:**
  - 09: Bailey et al.'s PBO paper is *J. Comput. Finance* 20(4), which resolves 01's open venue; Koijen et al., *Carry*, is *JFE* 127(2):197–225.
  - 11: write "Mohajerin Esfahani".
  - 06: cite Brown, Dimmock, Kang & Weisbenner via the *AER*, not NBER w15861.
  - G1: version updates for Lerner–Mao–Schoar–Zhang, Brown et al., and Begenau & Siriwardane; Metrick & Yasuda is verified.
- **Titles and upgrades:** eight titles in G7; four in G5; ten [K] entries in G6; Black & Cox, Tsiveriotis & Fernandes and Lando in G3.
- **Orphans and unnamed sources:** Bollen & Sensoy and Gourier in G2; Crawford & Sobel in G8; name "Mack" and the "BIS work" in G3, or drop them.
- **Sources to replace:** the Wikipedia and rdrr.io links in 07.

### 2.6 Cross-file inconsistencies (5)

1. **Giommetti et al., "Optimal Allocation to Private Equity"** ([record](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop)). The second author is Jørgensen in 01, 06 and 11 but Sørensen in 04 and 05. The index truncates author lists, so check SSRN 3761243.
2. **Bühlmann (1967).** 07 gives DOI 10.1017/s0515036100008023 and calls …8989 a companion paper. G6 assigns …8989 to the 1967 paper (ASTIN 4(3):199–207).
3. **Albertus & Denes.** G1 found no journal version. 05 and G3 cite a *JFQA* 2026 record, "Private Equity Fund Debt: Agency Costs and Cash Flow Management", DOI 10.1017/s0022109026102890. It is probably the published successor; confirm.
4. **Geltner.** The 1991 *JREFE* and 1993 *JRER* papers are used interchangeably. Say which one each citation means.
5. **Gredil, Liu & Sensoy.** The diversification gain is "2–8%" in 04 and 08 but "up to 5%" in G4. Pin down the version cited.

## 3. The most important papers the research missed

Twenty-nine papers, grouped by framework component. "Read with" names companions.

### 3.1 Optimization core (H, P, V)

1. **[Large-scale financial planning via a partially observable stochastic dual dynamic programming framework](https://consensus.app/papers/details/9e40ee775ba15434888d552a046a6c09/?utm_source=claude_desktop)**, Lee et al. (2023), *Quantitative Finance*.
   - Main's Phase 2 V is a Markov SDDP over states treated as observed, yet ADIC's regime is a filtered posterior. Main lists belief-state SDDP only as a Phase 3 research option.
   - PO-SDDP carries partially observed Markov states and adds feasibility cuts that suit hard liquidity rows. Use it to design V.
   - Read with: [Partially observable multistage stochastic programming](https://consensus.app/papers/details/cea97fcf25c15378a878e9a8a393b54c/?utm_source=claude_desktop) (Dowson et al. 2020, *ORL*).
2. **[Dynamic Portfolio Optimization with Transaction Costs: Heuristics and Dual Bounds](https://consensus.app/papers/details/4ea8b439c29a59fdb15efeefe4be19c5/?utm_source=claude_desktop)**, Brown & Smith (2011), *Management Science*.
   - Simple heuristics are paired with information-relaxation upper bounds, and the heuristics often come close to the bound.
   - P is certified only for gate breaches, by Clopper–Pearson; nothing measures its distance from optimal. Report a dual-bound gap for P in every release.
   - Read with: [Information Relaxations, Duality, and Convex Stochastic Dynamic Programs](https://consensus.app/papers/details/3b9b32a6560f512781bd69b9a6881290/?utm_source=claude_desktop) (Brown & Smith 2014, *OR*).
3. **[Scenario tree reduction for multistage stochastic programs](https://consensus.app/papers/details/53a49780d76c5f50a58604585c86eba2/?utm_source=claude_desktop)**, Heitsch & Römisch (2009), *Computational Management Science*.
   - Multistage reduction must control the filtration distance. Dossier 10 applies the authors' 2003 two-stage algorithms instead.
   - H's fans and the timing of SELL/REFINANCE decisions depend on the information structure, so reduce trees by filtration distance.
   - Read with: [An empirical analysis of scenario generation methods for stochastic optimization](https://consensus.app/papers/details/3705d75ee7385a15936f6937cdae08af/?utm_source=claude_desktop) (Löhndorf 2016, *EJOR*).

### 3.2 Objective and Tier 1

4. **[Multiperiod Mean Conditional Value at Risk Asset Allocation: Is It Advantageous to Be Time Consistent?](https://consensus.app/papers/details/f1547b977f055cdb8efcd20b57857a68/?utm_source=claude_desktop)**, Forsyth (2020), *SIAM J. Financial Mathematics*.
   - Enforcing time consistency "compares unfavourably" with pre-commitment. The time-zero pre-commitment policy equals a time-consistent policy under an induced objective.
   - J is re-solved each planning cycle, and main is silent on time consistency. Declare J pre-committed and implement it through the induced objective.
   - Read with: [Discrete-time mean-CVaR portfolio selection and time-consistency induced term structure of the CVaR](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop) (Strub et al. 2019, *JEDC*).
5. **[Optimal Dynamic Trading Strategies with Risk Limits](https://consensus.app/papers/details/3904dafe5042536aacf42278cfc299db/?utm_source=claude_desktop)**, Cuoco, He & Isaenko (2008), *Operations Research*.
   - When a VaR or tail-expectation limit is re-evaluated dynamically, risk exposure is always lower than unconstrained, and extreme losses are rarer.
   - Tier 1B tests a fixed 10-year worst-model CVaR10% ≥ 0. Re-impose it on a rolling basis inside P.
   - Read with: [Risk management with expected shortfall](https://consensus.app/papers/details/5bc6b8052fa75c37a94d6cfdd08d70f1/?utm_source=claude_desktop) (Wei 2021). In Wei's model, ES-constrained managers lose more when losses occur.
6. **[Distributionally robust joint chance constraints with second-order moment information](https://consensus.app/papers/details/8c13b90032cc5aa1a538b69b775db3c7/?utm_source=claude_desktop)**, Zymler, Kuhn & Rustem (record year 2011), *Mathematical Programming*.
   - T6 is a joint path-level chance constraint, which H carries as a 12-quarter CVaR surrogate at 0.60%.
   - A tuned worst-case CVaR is "essentially exact" for joint constraints. Test it in H, and size the surrogate's slack by simulation in P.
   - Read with:
     - [ALSO-X and ALSO-X+: Better Convex Approximations for Chance Constrained Programs](https://consensus.app/papers/details/921da370fcd4548aa53a54c681f6ec35/?utm_source=claude_desktop) (Jiang & Xie, *OR*), which always beats CVaR when the constraints are convex;
     - [On approximations of data-driven chance constrained programs over Wasserstein balls](https://consensus.app/papers/details/f69feb9051595f6e85764edfdd18d6c3/?utm_source=claude_desktop) (Chen, Kuhn & Wiesemann).

### 3.3 Robustness layer

7. **[On the Equivalence and Performance of Distributionally Robust Optimization and Robust Satisficing Models](https://consensus.app/papers/details/97d781784f8953ec915e053f62c18c68/?utm_source=claude_desktop)**, Wang et al. (2025), *MSOM*.
   - With Wasserstein models, DRO and robust satisficing "share the same solution family": every radius maps to a target.
   - The IC card shows radius-based worst cases and target-based k\* and η\* as separate evidence. Show them as one frontier, and check the KL case, which the proof does not cover.
8. **[Macroeconomic uncertainty prices when beliefs are tenuous](https://consensus.app/papers/details/27668b78be6b5bb48c584e7a2e2326d9/?utm_source=claude_desktop)**, Hansen et al. (2019), *Journal of Econometrics*.
   - Worst cases load on the persistence of bad states, not on means.
   - Vary the regime transition matrices, including drought and crisis dwell times, and not only the CMA means.
   - Read with: [Bayesian Distributionally Robust Merton Problem with Nonlinear Wasserstein Projections](https://consensus.app/papers/details/20388d7cb73c5106b87a0491333f62c0/?utm_source=claude_desktop) (Blanchet et al. 2025). Time-rectangular robustness over-pessimizes.

### 3.4 Owner liability and distribution policy

9. **[Optimal Spending Strategies for Sovereign Wealth Funds Using a Discrete-Time Life Cycle Model](https://consensus.app/papers/details/b92a25866b5350709012a3b8f6d1047b/?utm_source=claude_desktop)**, Aase (2024), *JRFM*.
   - Spending the expected real return makes value deteriorate "both in probability and in expectation".
   - This confirms main's mandate arithmetic and gives an optimal-spending benchmark for testing the de Finetti barrier.
   - Read with:
     - [How to Squander Your Endowment Pitfalls and Remedies](https://consensus.app/papers/details/55c1f0ca96db59ed9c05f005179e7cac/?utm_source=claude_desktop) (Dybvig et al. 2016);
     - [Capital Preservation and Current Spending with Sovereign Wealth Funds and Endowment Funds: A simulation Study](https://consensus.app/papers/details/c93456144b3e598bbe6aa9eb8ae9d5d8/?utm_source=claude_desktop) (Mork et al. 2022).
10. **[SWF 3.0: How sovereign wealth funds navigated COVID-19 and changed forever](https://consensus.app/papers/details/554f5e983997579aa32a8313d73304b8/?utm_source=claude_desktop)**, López (2023), *J. International Business Policy*.
    - Governments withdrew more than US$211bn from SWFs in 2020–21 and "invited" them to rescue firms.
    - Add 2020–21 to the demand-bust draw pool. Model owner-directed domestic investments as an obligation that consumes liquidity inside the band.
    - Read with:
      - [Institutions and macroeconomic stability under oil price shocks: Evidence from the GCC](https://consensus.app/papers/details/b100f501a743599d92c00223557b79d8/?utm_source=claude_desktop) (Shah et al. 2026);
      - [Fiscal Policy Regimes in Resource‐Rich Economies](https://consensus.app/papers/details/602cd3cbe11d584a8d9f6982d14bae23/?utm_source=claude_desktop) (Bjørnland et al. 2026).

### 3.5 Liquidity, funding and Corporate Finance

11. **[Liquidation Risk](https://doi.org/10.2469/faj.v59.n3.2530)**, Duffie & Ziegler (2003), *FAJ*.
    - Selling illiquid assets first while keeping a cushion of cash and liquid assets raises expected costs. It can, however, cut tail losses and insolvency risk.
    - P's fixed waterfall sells liquid assets first. Make the order a tuned, state-dependent policy (§4.4).
    - Read with:
      - [Optimal Portfolio Liquidation with Distress Risk](https://doi.org/10.1287/mnsc.1100.1235) (Brown, Carlin & Lobo 2010);
      - [The Dark Side of Liquid Bonds in Fire Sales](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop) (Chaderina et al. 2026).
12. **[Aggregate Risk and the Choice between Cash and Lines of Credit](https://doi.org/10.1111/jofi.12056)**, Acharya, Almeida & Campello (2013), *JF*.
    - In high aggregate volatility, credit lines show fewer initiations, higher spreads and shorter maturities.
    - ADIC needs liquidity in systematic stress, so Corporate Finance should count the revolver at partial availability there and new facilities at zero.
    - Read with:
      - [Bank lines of credit as contingent liquidity: Covenant violations and their implications](https://doi.org/10.1016/j.jfi.2019.03.004) (Acharya et al. 2020);
      - [The Price of Bank Funding Behind Private Credit: Evidence from Business Development Companies](https://doi.org/10.17016/2380-7172.4142) (Haque & Wang 2026).
13. **[The Shadow Costs of Illiquidity](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop)**, Jansen et al. (2022), *JFQA*.
    - Illiquidity is cheap when it only distorts allocation and dear when it restricts consumption. The owner payout is ADIC's consumption channel.
    - Decompose λ by binding row, and apply the 9/9/4 fallback only in states where the payout binds.
    - Read with: [Pension Liquidity Risk](https://consensus.app/papers/details/65e862e24881598a97200e1611a991ed/?utm_source=claude_desktop) (Jansen et al. 2026, *RFS*). It finds margin calls above 6% of assets, met by procyclical sales of safe bonds.
14. **[The Marginal Cost of Risk, Risk Measures, and Capital Allocation](https://doi.org/10.1287/mnsc.2015.2190)**, Bauer & Zanjani (2016), *Management Science*.
    - The correct risk measure depends on claimants' preferences. Euler allocation on expected shortfall is generally inefficient.
    - Groups' charge λ_R ∂CVaR/∂x_i is such an allocation. Derive the FTP risk row from the owner's loss function instead.

### 3.6 Internal capital market and group design

15. **[A q Theory of Internal Capital Markets](https://consensus.app/papers/details/2311defdb8b152ab80b1442580fa023f/?utm_source=claude_desktop)**, Dai et al. (2024), *JF*.
    - Allocation follows productivity and risk. Firms may sell productive divisions to raise liquidity, and diversification can destroy value in low-liquidity states.
    - Use this as the theoretical anchor for λ and the envelopes. A drought sale of a good asset can be value-maximizing and should be priced, not vetoed.
16. **[Decentralized Investment Management: Evidence from the Pension Fund Industry](https://doi.org/10.1111/jofi.12024)**, Blake et al. (2013), *JF*.
    - Sponsors moved to multiple specialists and cut each manager's risk budget to offset coordination problems and skill uncertainty.
    - Haircut summed group risk budgets.
    - Read with: [Optimal Decentralized Investment Management](https://doi.org/10.1111/j.1540-6261.2008.01376.x) (van Binsbergen, Brandt & Koijen 2008). It supports deriving group benchmarks from the total-portfolio problem.

### 3.7 Private markets

17. **[Private equity for pension plans? Evaluating private equity performance from an investor's perspective](https://doi.org/10.1016/j.jfineco.2026.104336)**, Korteweg, Panageas & Systla (2026), *JFE*.
    - Better PE outcomes come mainly from access to successful managers, not selection skill.
    - For a PE group that allocates to funds as an LP, model GP access as a state, and give selection-skill priors little weight.
18. **[Fear of Fire Sales, Illiquidity Seeking, and Credit Freezes](https://consensus.app/papers/details/a6c668ff8cfe5396bed107c465c18632/?utm_source=claude_desktop)**, Diamond & Rajan (2011), *QJE*.
    - Expected fire sales raise the return to holding cash and depress other buyers' bids.
    - This contests groups' "no idle reserve pays". Value the Secondaries and Capital Solutions crisis budgets as options, and expect weaker bids for ADIC's own sales in the same states.
    - Read with: [On Secondary Buyouts](https://consensus.app/papers/details/7bf7597e234759c785c4d2057d100202/?utm_source=claude_desktop) (Degeorge et al. 2016), on deployment pressure.

### 3.8 Forward Belief Engine

19. **[Combining probability forecasts](https://consensus.app/papers/details/31e8187029a5589da40b94611fcee9f2/?utm_source=claude_desktop)**, Ranjan & Gneiting (2010), *JRSS-B*.
    - Any non-trivial linear pool of calibrated forecasts is uncalibrated.
    - The FBE pools fusion variants, IC and group views, and posterior draws. Recalibrate each pool, for example with a beta-transformed linear pool.
    - Read with: [Wisdom/Madness of Crowds and Perils of Point Forecasts](https://consensus.app/papers/details/9c1e4f9af0845fba93c7333b6060aba7/?utm_source=claude_desktop) (Cooke 2026). Aggregate distributions, never point IRRs.
20. **[Combining Forecasts - On Why Averaging Beats Optimal Linear Weights](https://consensus.app/papers/details/05b1b772993e59638a60da357348567e/?utm_source=claude_desktop)**, Elliott et al. (2026), *JBES*.
    - Gains from optimal weights are usually small. Where they are large, screen out some forecasts and average the rest.
    - The constrained-GLS fusion must beat a screened simple average out of sample (§4.10).
21. **[Incentive-Compatible Forecasting Competitions](https://consensus.app/papers/details/4e78c77d15a55452942b3ca0721c296a/?utm_source=claude_desktop)**, Witkowski et al. (2023), *Management Science*.
    - Proper scores stop being truthful once only the best forecaster is rewarded.
    - Any registry recognition or budget tied to "best forecaster" needs an incentive-compatible mechanism.
    - Read with: [Presidential Address: Corporate Finance and Reality](https://doi.org/10.1111/jofi.13161) (Graham 2022). Firms trust internal forecasts only two years ahead.

### 3.9 Return priors: Public Markets and Private Credit

22. **[The Cost of Capital for Alternative Investments](https://doi.org/10.1111/jofi.12269)**, Jurek & Stafford (2015), *JF*.
    - Hedge-fund returns are "not reliably distinguishable" from S&P 500 put-writing.
    - Replace the positive hedge-fund α priors with a near-zero aggregate prior, and add a put-writing baseline.
    - Read with:
      - [Is it alpha or beta? Decomposing hedge fund returns when models are misspecified](https://doi.org/10.1016/j.jfineco.2024.103805) (Ardia et al. 2024);
      - [Hedge Fund Performance: End of an Era?](https://doi.org/10.1080/0015198x.2021.1921564) (Bollen et al. 2021).
23. **[Risk-Adjusted Private Debt Fund Performance and the Term Structure of Alphas](https://doi.org/10.2139/ssrn.4319347)**, Böni & de Roon (2023), SSRN.
    - Alphas exceed 6% a year and fall over fund life, from 8.2% early to 3.9% late. Downside betas exceed upside betas.
    - Use a fund-age mixture prior rather than the zero prior taken from Erel–Flanagan–Weisbach, and charge downside beta.

### 3.10 Overlay

24. **[Corporate Risk Management: Integrating Liquidity, Hedging, and Operating Policies](https://consensus.app/papers/details/c6027dda48605911a46b3578a9a0a3ea/?utm_source=claude_desktop)**, Gamba & Triantis (2014), *Management Science*.
    - Cash plays a "critical and distinct role", and the marginal value of derivatives hedging "is likely to be low".
    - The convex sleeve must beat an equal-cost cash buffer held by Corporate Finance.
    - Read with: [An Empirical Portfolio Perspective on Option Pricing Anomalies](https://consensus.app/papers/details/39ee84c156a85bf1a821939d34d237d8/?utm_source=claude_desktop) (Driessen & Maenhout 2007). On preferences alone, investors short puts.

### 3.11 Agentic lab

25. **[RewardHackingAgents: Benchmarking Evaluation Integrity for LLM ML-Engineering Agents](https://consensus.app/papers/details/63af8ba74bfd5c42b62a9ae983d69167/?utm_source=claude_desktop)**, Atinafu et al. (2026), ICDEW.
    - Agents attempt evaluator tampering in about 50% of natural episodes.
    - Single-mechanism defences block only one of the two attack vectors, tampering and leakage. Lock both, and plant canaries.
    - Read with:
      - [Reward Hacking Challenges Oversight of Autonomous Research Agents](https://consensus.app/papers/details/1ffb53cca35e59639c7a6fa8e5dc69c7/?utm_source=claude_desktop) (Huang et al. 2026), where detailed feedback roughly doubled evasion;
      - [Internal Representations as Indicators of Hallucinations in Agent Tool Selection](https://consensus.app/papers/details/813c6b3a5da25a30836c68844c29e5a6/?utm_source=claude_desktop) (Healy et al. 2026), on "tool bypass".
26. **[Online control of the false discovery rate with decaying memory](https://consensus.app/papers/details/92afdcf055605c9faa05bb6da4cdb658/?utm_source=claude_desktop)**, Ramdas et al. (2017).
    - mem-FDR alleviates alpha-investing's "piggybacking" and "alpha-death".
    - Run a mem-FDR ledger across analysis contracts.
    - Read with: [False (and Missed) Discoveries in Financial Economics](https://consensus.app/papers/details/ffbf7057f48e5d65b7507d5d9200ebe2/?utm_source=claude_desktop) (Harvey & Liu 2020). State each test's power and its miss cost.

### 3.12 IC Deliberation Module

27. **[Ambiguity and the Corporation: Group Disagreement and Underinvestment](https://consensus.app/papers/details/349a3e540a9f507c999fa811de9d8775/?utm_source=claude_desktop)**, Garlappi et al. (2017), *JFE*.
    - Group decisions under heterogeneous beliefs are dynamically inconsistent and underinvest.
    - Pre-commit contingent plans, and monitor DEFER drift.
28. **[Devil's advocate versus authentic dissent: stimulating quantity and quality](https://consensus.app/papers/details/246662213fa05d4991aa2ef601144715/?utm_source=claude_desktop)**, Nemeth et al. (2001), *EJSP*.
    - Authentic minorities beat role-played devil's advocates, which mainly bolster the initial view.
    - Lead with sourced dissent.
    - Read with: [Enhancing AI-Assisted Group Decision Making through LLM-Powered Devil's Advocate](https://consensus.app/papers/details/5102feb21e155efa857abd4c30195548/?utm_source=claude_desktop) (Chiang et al. 2024). Aim the AI devil's advocate at the AI's own recommendation.

### 3.13 Synthetic data

29. **[Mostly harmless simulations? Using Monte Carlo studies for estimator selection](https://doi.org/10.1002/jae.2724)**, Advani, Kitagawa & Słoczyński (2019), *JAE*.
    - Data-calibrated Monte Carlo was "worse than random" at picking the minimum-bias estimator.
    - Use SYN-ADIC-177 for correctness and robustness, not for choosing FBE variants.
    - Read with:
      - [Validation of the forecast skill of the Global Modeling and Assimilation Office Observing System Simulation Experiment](https://doi.org/10.1002/qj.2029) (Privé et al. 2013), where the synthetic world proved too easy;
      - [Using simulation studies to evaluate statistical methods](https://doi.org/10.1002/sim.8086) (Morris et al. 2019, the ADEMP protocol).

## 4. Where the literature contradicts or refines the research recommendations

**4.1 Mandate arithmetic and payout rules (main §2, §4.7). Supported, with one refinement.**
- Main finds that real NAV holds only at a payout of about 5.3%. The following agree:
  - [Aase 2024](https://consensus.app/papers/details/b92a25866b5350709012a3b8f6d1047b/?utm_source=claude_desktop);
  - [Mork et al. 2022](https://consensus.app/papers/details/c93456144b3e598bbe6aa9eb8ae9d5d8/?utm_source=claude_desktop);
  - [Dybvig et al. 2016](https://consensus.app/papers/details/55c1f0ca96db59ed9c05f005179e7cac/?utm_source=claude_desktop);
  - [Dang, Forsyth & Vetzal 2017](https://consensus.app/papers/details/be5936659c2a5006ac12e9527606e1ec/?utm_source=claude_desktop).
- The rejection of habit utility, ratchets and fixed real amounts is supported ([Jeon 2018](https://consensus.app/papers/details/b6c025002fa5573a996b38f884696090/?utm_source=claude_desktop); [Mork et al., soft norm](https://consensus.app/papers/details/62dbecedd3f75999bcf3364f3ba3f122/?utm_source=claude_desktop)).
- *Change:* smoothing interacts with investment policy, so tune ρ_d jointly with the SAA in P.

**4.2 The owner band as the cheapest route to the 1% gate (main finding 6). Contested.**
- Mix B's 21bp against Mix A's 62bp prices the band at ADIC's cost. The owner's cost peaks exactly when ADIC needs the band:
  - sponsors adjust payouts asymmetrically in bad times ([Brown, Dimmock, Kang & Weisbenner 2014](https://doi.org/10.1257/aer.104.3.931));
  - governments withdrew US$211bn from SWFs in 2020–21 ([López 2023](https://consensus.app/papers/details/554f5e983997579aa32a8313d73304b8/?utm_source=claude_desktop));
  - drawdowns depend on fiscal space ([Shah et al. 2026](https://consensus.app/papers/details/b100f501a743599d92c00223557b79d8/?utm_source=claude_desktop)).
- *Changes:*
  - Model a low probability that the owner accepts in demand-bust states.
  - Add owner-directed investments as an obligation.
  - Make policy D conditional on advance written agreement.
  - Keep Mix A as the default when there is no agreement.
- The mandate switch is supported ([Landon & Smith 2015](https://consensus.app/papers/details/1f9da91d0180515195ee945ad33ee532/?utm_source=claude_desktop)).

**4.3 The $10–15bn committed revolver (main §9.2 item 12). Refined.** Lines become dearer and scarcer in aggregate stress (§3.5), and stressed lenders reprice borrowers. *Changes for Corporate Finance:*
- Count availability at ≤50% in the joint oil–crisis state, and new facilities at zero.
- Add a tightening premium (about 1.1pp in BDC data, §3.5) to REFINANCE and LEVER hurdles.
- Test pre-funded term cash as an alternative ([Anglin & Gao](https://consensus.app/papers/details/29f5d1f3ce855a36b86e0c22a1ef2f0c/?utm_source=claude_desktop); [Lins, Servaes & Tufano 2010](https://doi.org/10.1016/j.jfineco.2010.04.006)).
- Monitor effective maturity ([Brunnermeier & Yogo](https://consensus.app/papers/details/e5d07eaeb7cb57e9977a1900ca0d5a7a/?utm_source=claude_desktop)) and rollover risk ([He & Xiong](https://consensus.app/papers/details/272186b246105b7e98e6c262a594de43/?utm_source=claude_desktop)).
- Model repo as a quantity run ([Copeland et al.](https://consensus.app/papers/details/b4498a6023e95908834404ffd98876ab/?utm_source=claude_desktop)).

Main's lender-diversification rules and yearly test draw stay.

**4.4 The fixed recourse waterfall (main §4.8; groups §2.4). Contradicted.**
- The order "Reserve → liquid sales → facility → PE secondary → payout to minimum" is myopic (§3.5).
- In practice, funds shed liquid assets first ([Hespeler & Suntheim 2020](https://doi.org/10.5089/9781513563695.064)). The literature formalizes G7's own finding that 86–99% of first red events fall in crisis quarters after a drought.
- *Changes:*
  - Make the order a tuned, state-dependent parameter.
  - Add a crowding haircut.
  - Run liquid-first, cash-last and pro-rata orders as a standing ablation.
  - In a drought, raise liquidity early through planned tail-end and LP-interest sales and term funding.

**4.5 Pacing and commitments (groups finding 9, §4.4). Supported, refined.**
- Timing commitments yields modest gains at best ([Brown et al. 2020](https://consensus.app/papers/details/b5880343ab7b57ebaf68b353dfff48da/?utm_source=claude_desktop)), so give a pacing cut no liquidity credit for two quarters.
- [Gourier, Phalippou & Westerfield 2024](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop) is cited in the dossiers but used in neither synthesis. It finds that investors pay more to adjust committed amounts than to remove tradability frictions. Value the pacing corridor as that option, and count unfunded commitments in leverage ([Meyer 2020](https://consensus.app/papers/details/d99e5eff8f48558898b24269df59ba18/?utm_source=claude_desktop)).

**4.6 λ and Corporate Finance's FTP curve (main L1, L14; groups §4.3). Supported, refined.**
- *Support:* [Jansen et al. 2022](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop), [Dai et al. 2024](https://consensus.app/papers/details/2311defdb8b152ab80b1442580fa023f/?utm_source=claude_desktop), [Kinlaw 2013](https://consensus.app/papers/details/87606279740d57b4b0350e859446911b/?utm_source=claude_desktop) and [Gârleanu & Pedersen 2011](https://consensus.app/papers/details/c5d81d132abf5d118a3a62c20200c195/?utm_source=claude_desktop).
- *Changes:*
  - Decompose λ by binding row, and replace the Euler CVaR risk row (§3.5).
  - Add a financing-window state ([Bolton, Chen & Wang](https://consensus.app/papers/details/e1bcae07d2be506289e7506e93615bb2/?utm_source=claude_desktop), cited only in G2).
  - Make prices regime-conditional ([Brown et al. 2020, shared signals](https://consensus.app/papers/details/5d959b6409d9539aaaf4a9781599a0eb/?utm_source=claude_desktop)).
  - Expect non-monotone ℓ near the SELL boundary ([Wang et al. 2012](https://consensus.app/papers/details/fd02d9b3f4645c8a884efdcbf8ab0f46/?utm_source=claude_desktop)).
  - Main calls price decomposition a heuristic because Shapley–Folkman is vacuous. Lagrangian bounds with a gap that does not grow with the number of subproblems exist ([Adelman & Mersereau 2008](https://consensus.app/papers/details/80a57bb0dc385a61b01ce4b8ac352bfd/?utm_source=claude_desktop); [Brown et al. 2022](https://consensus.app/papers/details/e8af8aeb5faf5365ac03e17f5d8289af/?utm_source=claude_desktop)); publish them.
  - Agency-adjust hurdles on the shared buffer ([Baldenius et al. 2007](https://doi.org/10.2308/accr.2007.82.4.837)).
  - Build the curve from [Dermine](https://consensus.app/papers/details/59596c9dbc355d4a93f649ba14e8e1fc/?utm_source=claude_desktop)'s FTP components.
  - Pre-commit credits to liquidity providers ([Gautier & Heider 2009](https://doi.org/10.1628/093245609789919603)).

**4.7 Objective and Tier 1 (main §4.9). Supported, refined.**
- Never maximizing P(10%) is supported ([Capponi & Zhang 2024](https://consensus.app/papers/details/0fd71f5302ce52aead087822575e14e4/?utm_source=claude_desktop)).
- The rule "shortfall exponent ≥ 1" admits 1, and linear shortfall yields the same policy as probability maximization ([Krabichler et al.](https://consensus.app/papers/details/c7d8bb6499c75f8e93935fa3a567584b/?utm_source=claude_desktop)). Require an exponent above 1; J's squared term complies.
- *Further changes:*
  - Make J pre-committed, impose risk floors on a rolling basis, and test tighter surrogates for T6 (§3.2).
  - Report buffered probability of exceedance ([Dang et al. 2025](https://consensus.app/papers/details/50e851a2565f56639dabd7b0045072f5/?utm_source=claude_desktop)).
  - Add a reaching-for-yield check ([Campbell & Sigalov 2020](https://consensus.app/papers/details/b029ce8a702156d8bc5e5d2fde4d3409/?utm_source=claude_desktop)).
- Drawdown as an appetite metric is supported ([MacLean et al. 2021](https://consensus.app/papers/details/6510dbe8c3fa55139c8728a4efbfe07c/?utm_source=claude_desktop)).

**4.8 Robustness (main §4.10). Refined.**
- Show one frontier, put ambiguity on persistence, and do not stack ambiguity sets (§3.3).
- Robustify the regime posterior separately ([Hansen & Sargent 2007](https://consensus.app/papers/details/b88a782e5625543c82fe19c60577d8bc/?utm_source=claude_desktop)).
- Use regime-conditional radii ([Pun et al. 2023](https://consensus.app/papers/details/05518e72407e555380b0afd7eb56f5f9/?utm_source=claude_desktop)).
- Use χ² divergence for sensitivity rankings ([Makam et al.](https://consensus.app/papers/details/3ac0b7b157035b85b9267d48ad8b4100/?utm_source=claude_desktop)).
- Re-simulate stressed dynamics ([Kroell et al.](https://consensus.app/papers/details/ce04d40b9c585067a632648bcb9d6bae/?utm_source=claude_desktop)).
- Macro-identified regimes are supported ([Goodarzi 2025](https://consensus.app/papers/details/b859291f240d53db8323f68bc6adf7dd/?utm_source=claude_desktop)).

**4.9 Optimization core (main §4.8). Refined.**
- Move belief-state SDDP into Phase 2, reduce trees by filtration distance, and add dual-bound certificates (§3.1).
- Choose V's dimension by bound gaps ([Zhang & Sun](https://consensus.app/papers/details/c3bb3cbfbd5f58858b54e03033005617/?utm_source=claude_desktop)). Markov-chain SDDP is supported ([Löhndorf & Shapiro 2019](https://consensus.app/papers/details/889e982ca4c8514ea4b791ce145b8493/?utm_source=claude_desktop)).
- Check trees for arbitrage ([Geyer et al. 2013](https://consensus.app/papers/details/3116632fca3a5358a2b66101b6f6aa5d/?utm_source=claude_desktop)).
- Linear decision rules inside the fans can be inadequate ([Chen et al. 2008](https://consensus.app/papers/details/26c1f3114deb5332a2978f908796ba74/?utm_source=claude_desktop)). Use lifted rules.

**4.10 Forward Belief Engine (main §4.3; groups §5). One contradiction, several refinements.**
- *Contradiction.* Main fuses single deals by constrained GLS with correlated errors (dossier 07 sets ρ_fu = 0.5). [Smith & Wallis 2009](https://consensus.app/papers/details/f8bdb7ea82bb52c681576c06475bb34a/?utm_source=claude_desktop), which dossier 07 itself cites, supports ignoring covariances when estimating weights.
  - Keep the covariances in the predictive variance.
  - Shrink weights toward equal.
  - Adopt GLS only if it beats simple and screened averages ([Genre et al. 2013](https://consensus.app/papers/details/cf9391f178015486ade67819ae4ef27f/?utm_source=claude_desktop)).
- *Changes:*
  - Recalibrate pools, and cap credibility beyond about 8 quarters (§3.8).
  - Use equal weights until seed questions exist ([Colson & Cooke 2017](https://consensus.app/papers/details/dbe7edfbdd19501caa1d757e57fd4aad/?utm_source=claude_desktop)).
  - Use parameter-free Benktander until t is estimated ([Neuhaus 2025](https://consensus.app/papers/details/f0afe8fc96ab5554a91bcff8d4d2a12f/?utm_source=claude_desktop)).
  - Widen ranges per person and permanently ([Boutros et al. 2020](https://consensus.app/papers/details/b4ff9b1507b756f1affc7bfc68dd8a4c/?utm_source=claude_desktop)).
  - Estimate β_f where each forecast is made ([Bordalo et al. 2020](https://consensus.app/papers/details/4fabd9f27a1359a5a8e026ed6e04a384/?utm_source=claude_desktop)).
  - Make optimism regime-dependent ([Hribar & McInnis 2012](https://consensus.app/papers/details/a6db6d24c8e15a899e64fabe11140591/?utm_source=claude_desktop)).
  - Apply no fundraising haircut to deals ([Hüther](https://consensus.app/papers/details/834e2e8848615de6808f6adbd5bdda10/?utm_source=claude_desktop)).
  - Use autocorrelation-robust PIT tests ([Knüppel 2015](https://consensus.app/papers/details/a665841d31cc55d188a58665426c71b0/?utm_source=claude_desktop)).

**4.11 Group return priors (main §4.12; groups §5). Contradicted in places.**
- **Hedge funds.** Use near-zero priors, with α = 0 as a mandatory sensitivity (§3.9).
- **Long-only.**
  - The evidence behind the zero-alpha anchor has low power ([Andrikogiannopoulou & Papakonstantinou 2019](https://doi.org/10.1111/jofi.12784)).
  - Institutional accounts earned +31bp net ([Gerakos et al. 2021](https://consensus.app/papers/details/0212f272b5cf5989a5a878405e42c2d3/?utm_source=claude_desktop)), and EM active positions earned +250bp ([Dyck, Lins & Pomorski 2013](https://doi.org/10.1093/rapstu/rat005)).
  - Use sleeve-specific priors.
- **Private Credit.**
  - Use the fund-age prior (§3.9).
  - Set LGD by collateral type ([Jang, Kim & Sufi 2025](https://doi.org/10.2139/ssrn.5744584)).
  - Mark by wrapper ([Andrade & Lie 2026](https://doi.org/10.2139/ssrn.7533698)).
  - Give evergreen units zero Tier-1 liquidity ([Couts 2025](https://consensus.app/papers/details/abc2df60ee515faa8f6cf53c880555a8/?utm_source=claude_desktop)).
- **Secondaries, a hybrid book.**
  - On the fund side, discount capture includes discount-rate exposure ([Boyer et al. 2023](https://consensus.app/papers/details/d9f67be2c83856ea8703fcd0bfeb3f57/?utm_source=claude_desktop)).
  - On the direct side, continuation-vehicle assets are positively selected ([Abuzov et al. 2025](https://doi.org/10.3386/w34471)), so CV elections are events, not controls.
  - The tail θ of 0.78–0.83 is consistent with the evidence.
- **PE.** Weight access over selection (§3.7), and apply a fund-size penalty to up-sizes ([Bhardwaj et al. 2025](https://doi.org/10.3386/w33596)).

**4.12 Leverage (main §4.5). Supported, refined.**
- Leverage as a liquidity tool is supported ([Edirisinghe 2023](https://consensus.app/papers/details/626d6c94bb4f5c1c912d5ce4d1ee0ef3/?utm_source=claude_desktop)).
- Betting-against-beta returns are contested ([Novy-Marx & Velikov](https://consensus.app/papers/details/17755f59391c5311b233e577e07dd1ef/?utm_source=claude_desktop)), so justify each levered sleeve on its own net α\*.
- Attribute dynamic leverage with the decomposition of [Anderson et al. 2014](https://consensus.app/papers/details/8a242fcc6d1d5d5bb393e76ffce91e3a/?utm_source=claude_desktop).
- Compute half-Kelly on desmoothed σ.

**4.13 Overlay (main §4.6, L5). Refined.**
- *Changes:*
  - Size the convex sleeve against cash (§3.10).
  - Model trend's crisis beta as decaying after crises ([Hutchinson & O'Brien 2014](https://consensus.app/papers/details/0f71676fcce356dbb83d98b7ca85c713/?utm_source=claude_desktop)).
  - Main triggers protection on a low VRP. Use the left-tail premium instead ([Andersen et al. 2019](https://consensus.app/papers/details/756ab3d8847a5e9980ed69e3bcd9d922/?utm_source=claude_desktop); [Heston et al. 2023](https://consensus.app/papers/details/db0fd9754cf65b46b571efc32881aee5/?utm_source=claude_desktop)).
  - Add defensive equity ([Baltussen et al. 2026](https://consensus.app/papers/details/631cea0eea6a5c49ac808ba06cdf9685/?utm_source=claude_desktop)).
  - Test LASH ([Alfaro et al.](https://consensus.app/papers/details/d194a64624745726be3cb46d2cb00e74/?utm_source=claude_desktop)).
  - Model VM receipt delays ([Bardoscia et al. 2021](https://consensus.app/papers/details/2ed33ac2bdc9586d98e71535615286bf/?utm_source=claude_desktop)).
  - Set DSR severity by provenance, since dealer backtests lose a median 73% of their Sharpe ratio live ([Suhonen et al. 2017](https://consensus.app/papers/details/df15834241b85f16a52df4f546753386/?utm_source=claude_desktop)).
  - DSR cannot detect leakage ([Gençay 2026](https://consensus.app/papers/details/f218fb3f22f95742b8e70415676bb8da/?utm_source=claude_desktop)).
- Joint (VaR, ES) scoring is supported ([Fissler & Ziegel 2016](https://doi.org/10.1214/16-aos1439)).

**4.14 Agentic lab (main §5). Supported, refined.**
- Lock the evaluators, add provenance records, and run a mem-FDR ledger with named error criteria (§3.11).
- Judges must come from a different model family than the generator ([Spiliopoulou](https://consensus.app/papers/details/3588300a76bb5000ba36f65a1c3b32ab/?utm_source=claude_desktop)), validated against humans ([Norman](https://consensus.app/papers/details/c1e804dd3c1d5f39bab35205905f683f/?utm_source=claude_desktop)).
- Spend validation on world diversity ([Roelofs et al. 2019](https://consensus.app/papers/details/4aeb7cdda9285f3e93c245b261e5fb92/?utm_source=claude_desktop)).
- Verify agent code by calibration ([Xu et al. 2026](http://arxiv.org/abs/2606.31630v1)).
- Re-qualify after model upgrades ([Pan 2022](https://consensus.app/papers/details/dc88f37451f15860b3e886d0078120ba/?utm_source=claude_desktop)).

**4.15 IDM (main §6). Refined.**
- Pre-commit the plan and lead with authentic dissent (§3.12).
- Use objective DA by default, and dialectical inquiry only for explicit rival scenario sets (§2.4 item 9).
- Track decision accuracy ([Alsobay et al. 2025](https://consensus.app/papers/details/00dfd56f864f59fc943420a4d8f3b5d6/?utm_source=claude_desktop)) and under-reliance ([Kokje 2026](https://consensus.app/papers/details/189332eb9c72506d9c81d4fcc8c3de0e/?utm_source=claude_desktop)).
- Show evidence first ([Jain et al. 2025](https://consensus.app/papers/details/757fcfe1a67454efab3cbdaaa3aa6fcb/?utm_source=claude_desktop)).
- Audit retrieval ([Kraidia 2026](https://consensus.app/papers/details/8f581a2c3ee65cfd8cf2d96b6e1e0ce5/?utm_source=claude_desktop)).
- Add a conviction band ([Bär et al. 2011](https://consensus.app/papers/details/be40b9004e4b554d9a2d383970d86703/?utm_source=claude_desktop)).
- The "Treasurer" seat is Corporate Finance's.

**4.16 Groups synthesis. Refined.**
- *Internal capital markets.* Misallocation evidence is contested ([Whited 2001](https://doi.org/10.1111/0022-1082.00385)). Collar envelope changes ([Hoang & Ruckes 2015](https://doi.org/10.1093/rof/rfu018)), and use no single hurdle ([Krüger et al. 2015](https://doi.org/10.1111/jofi.12250)).
- *Internal transfers.* Monitor opposite-direction transfers through the hybrid Secondaries book ([Gaspar, Massa & Matos 2006](https://doi.org/10.1111/j.1540-6261.2006.00830.x)).
- *Co-investment.*
  - Selection is conditional ([Braun & Schmidt 2014](https://doi.org/10.2139/ssrn.2411044)), and LP discretion carries an option ([Tuft 2023](https://doi.org/10.2139/ssrn.4559453)).
  - Matched benchmarks erase measured outperformance ([L'Her et al. 2016](https://doi.org/10.2469/faj.v72.n4.1)).
  - Follow-on calls cluster in distress ([Hotchkiss et al. 2021](https://doi.org/10.1093/rcfs/cfab015)).
- *Dry powder.* Its option value is real because capital moves slowly ([Duffie 2010](https://ideas.repec.org/a/bla/jfinan/v65y2010i4p1237-1267.html)). Build it ex ante through Corporate Finance lines.
- *GP stakes.* They are fee streams on the PE book's fundraising cycle, so they concentrate exposure ([Metrick & Yasuda 2010](https://doi.org/10.1093/rfs/hhq020)).
- *SYN-ADIC-177.* Preregister generator variants ([Pawel et al. 2024](https://doi.org/10.1002/bimj.202200091)) and add a semi-synthetic release ([RealCause](http://arxiv.org/abs/2011.15007v2)).

**4.17 Gaps the literature could not fill.** ADIC's own data must decide these:
- secondary-fund net performance and continuation vehicles;
- NAV loans, preferred equity, PIK toggles and GP stakes;
- PE underwriting projections against outcomes;
- LP access lost after a skipped re-up;
- post-2010 co-investment performance;
- internal capital markets inside asset owners;
- CFP design;
- direct-loan recoveries;
- the 2022–26 DPI drought.

## 5. Recommended reading list (25)

1. [Large-scale financial planning via a partially observable stochastic dual dynamic programming framework](https://consensus.app/papers/details/9e40ee775ba15434888d552a046a6c09/?utm_source=claude_desktop) (Lee et al. 2023): V design.
2. [Dynamic Portfolio Optimization with Transaction Costs: Heuristics and Dual Bounds](https://consensus.app/papers/details/4ea8b439c29a59fdb15efeefe4be19c5/?utm_source=claude_desktop) (Brown & Smith 2011): P certificates.
3. [Multiperiod Mean Conditional Value at Risk Asset Allocation: Is It Advantageous to Be Time Consistent?](https://consensus.app/papers/details/f1547b977f055cdb8efcd20b57857a68/?utm_source=claude_desktop) (Forsyth 2020): pre-commitment.
4. [Optimal Dynamic Trading Strategies with Risk Limits](https://consensus.app/papers/details/3904dafe5042536aacf42278cfc299db/?utm_source=claude_desktop) (Cuoco et al. 2008): rolling risk floors.
5. [Distributionally robust joint chance constraints with second-order moment information](https://consensus.app/papers/details/8c13b90032cc5aa1a538b69b775db3c7/?utm_source=claude_desktop) (Zymler et al.): the T6 surrogate.
6. [On the Equivalence and Performance of Distributionally Robust Optimization and Robust Satisficing Models](https://consensus.app/papers/details/97d781784f8953ec915e053f62c18c68/?utm_source=claude_desktop) (Wang et al. 2025): one frontier.
7. [Macroeconomic uncertainty prices when beliefs are tenuous](https://consensus.app/papers/details/27668b78be6b5bb48c584e7a2e2326d9/?utm_source=claude_desktop) (Hansen et al. 2019): ambiguity on persistence.
8. [Optimal Spending Strategies for Sovereign Wealth Funds Using a Discrete-Time Life Cycle Model](https://consensus.app/papers/details/b92a25866b5350709012a3b8f6d1047b/?utm_source=claude_desktop) (Aase 2024): payout arithmetic.
9. [SWF 3.0: How sovereign wealth funds navigated COVID-19 and changed forever](https://consensus.app/papers/details/554f5e983997579aa32a8313d73304b8/?utm_source=claude_desktop) (López 2023): owner behaviour in crisis.
10. [Liquidation Risk](https://doi.org/10.2469/faj.v59.n3.2530) (Duffie & Ziegler 2003): order of sales.
11. [Optimal Portfolio Liquidation with Distress Risk](https://doi.org/10.1287/mnsc.1100.1235) (Brown, Carlin & Lobo 2010): non-myopic liquidation.
12. [Aggregate Risk and the Choice between Cash and Lines of Credit](https://doi.org/10.1111/jofi.12056) (Acharya et al. 2013): facility reliability.
13. [The Shadow Costs of Illiquidity](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop) (Jansen et al. 2022): where λ binds.
14. [The Marginal Cost of Risk, Risk Measures, and Capital Allocation](https://doi.org/10.1287/mnsc.2015.2190) (Bauer & Zanjani 2016): the risk row.
15. [Optimal Decentralized Investment Management](https://doi.org/10.1111/j.1540-6261.2008.01376.x) (van Binsbergen et al. 2008): group design.
16. [Capital Commitment](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop) (Gourier et al. 2024): commitment risk.
17. [Discount Rate Risk in Private Equity: Evidence from Secondary Market Transactions](https://consensus.app/papers/details/d9f67be2c83856ea8703fcd0bfeb3f57/?utm_source=claude_desktop) (Boyer et al. 2023): secondary pricing.
18. [Private equity for pension plans? Evaluating private equity performance from an investor's perspective](https://doi.org/10.1016/j.jfineco.2026.104336) (Korteweg et al. 2026): access versus selection.
19. [A Simple Explanation of the Forecast Combination Puzzle](https://consensus.app/papers/details/f8bdb7ea82bb52c681576c06475bb34a/?utm_source=claude_desktop) (Smith & Wallis 2009): fusion weights.
20. [Combining probability forecasts](https://consensus.app/papers/details/31e8187029a5589da40b94611fcee9f2/?utm_source=claude_desktop) (Ranjan & Gneiting 2010): pool recalibration.
21. [The Cost of Capital for Alternative Investments](https://doi.org/10.1111/jofi.12269) (Jurek & Stafford 2015): hedge-fund priors.
22. [Corporate Risk Management: Integrating Liquidity, Hedging, and Operating Policies](https://consensus.app/papers/details/c6027dda48605911a46b3578a9a0a3ea/?utm_source=claude_desktop) (Gamba & Triantis 2014): hedging versus cash.
23. [RewardHackingAgents: Benchmarking Evaluation Integrity for LLM ML-Engineering Agents](https://consensus.app/papers/details/63af8ba74bfd5c42b62a9ae983d69167/?utm_source=claude_desktop) (Atinafu et al. 2026): lab integrity.
24. [Ambiguity and the Corporation: Group Disagreement and Underinvestment](https://consensus.app/papers/details/349a3e540a9f507c999fa811de9d8775/?utm_source=claude_desktop) (Garlappi et al. 2017): committee dynamics.
25. [Mostly harmless simulations? Using Monte Carlo studies for estimator selection](https://doi.org/10.1002/jae.2724) (Advani et al. 2019): limits of synthetic data.

## 6. Consensus usage message

Reviews 01–09 recorded no message. The following are verbatim.

**Final message**, recorded identically in all nine group reviews (G1–G9):

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

**Earlier counters:**
- 10: "20 searches left this month; resets to 500 on November 1st."
- 11: "17 searches left this month; resets to 500 on November 1st."
- 12: "14 searches left this month; resets to 500 on November 1st."
- 13: "3 searches left this month; resets to 500 on November 1st."
- 14: "0 searches left this month; resets to 500 on November 1st."
