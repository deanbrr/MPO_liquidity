# Stream 09 literature check: derivatives overlay (tail hedging, opportunistic trading, collateral)

**Dossier checked:** `research/dossiers/09_overlay.md` (979 lines, prepared 2026-10-18).
- The reference list holds 39 academic works:
  - 22 "sourced and fetched" (§10, items 1–22);
  - 17 "cited from memory, not re-verified" [nrv]: 15 articles and 2 books.
- It also cites a BIS Bulletin, regulatory texts (BCBS, FSB, BoE, US rule), press and Wikipedia pages, and Cboe data. These are outside this check.

**Date:** 2026-10-18.

**Search engine:** Consensus. 33 searches, run one at a time with no filters (the query list is in §7):
- 19 targeted citation look-ups;
- 14 topical backfill searches: the 6 seed queries plus 8 refinements.

The seed searches also confirmed 5 dossier citations, and other searches confirmed 5 more incidentally. Four WebSearches confirmed journal metadata that Consensus could not resolve (§7).

**Companion:** `research/verification/09_overlay.verify.md`. It checked 25 references against primary PDFs and found none hallucinated, but it did not check the 17 [nrv] works. This check therefore gave the [nrv] works priority.

**Organizational mapping (user, 2026-10-18).**
- Secondaries is a hybrid of direct and fund investments.
- Corporate Finance owns the treasury function. Per the context file, it also owns:
  - overlay collateral (VM/IM) management;
  - portfolio-level borrowing;
  - distribution payments.
- Implications below are assigned on that basis:
  - collateral, margin and liquidity-pricing implications go to **Corporate Finance (the Treasurer seat)**;
  - hedge-book and opportunistic-book implications go to the **Overlay group**.

**Reading conventions**
- Findings come from the titles and abstracts that Consensus returned. Full texts were not read.
- **[Inference]** marks design reasoning that goes beyond what an abstract states.
- Author lists in bibliography entries are shown as Consensus displays them, with "et al." where Consensus truncates. Running text sometimes uses well-known co-author surnames; the links point to the Consensus records.
- Years are Consensus record years. Where a record carries the online-first or working-paper year, the print year is noted.
- Numbers in §4.3 come from other investors, markets and samples. They are plausibility anchors, not ADIC calibration.
- Several 2026 items are new preprints with few or no citations. They are flagged where they appear.

---

## 1. Summary

### Citation integrity
- **Scope.** I checked 29 works:
  - the 25 most load-bearing of the 39 academic works: 15 sourced and 10 [nrv];
  - 4 more confirmed incidentally by other searches: Hamill et al. (2016), Moreira & Muir (2017), Brunnermeier, Nagel & Pedersen (2009), and Coval & Shumway (2001) [nrv].
- **Result: 29 found, 0 mismatched, 0 not found.**
  - Getmansky–Lo–Makarov (2004) has no journal record in Consensus, only thesis versions and a citing abstract. WebSearch confirms JFE 74, 529–609.
  - **No hallucinated or garbled dossier references.**
- **[nrv] works now verified: 11 of 17.**
  - Verified: Rampini & Viswanathan; Rampini, Sufi & Viswanathan; Browne; Carr & Wu; Lo; Daniel & Moskowitz; Mohajerin Esfahani & Kuhn; Grossman & Zhou; Getmansky, Lo & Makarov; Hardy; Coval & Shumway.
  - Still unchecked: Demeterfi et al. (1999), Gatheral & Jacquier (2014), Kaminski & Lo (2014), Rockafellar & Uryasev (2000), and the books by Bhansali (2014) and Spitznagel (2021). See §7.
- **Every claim that could be checked against an abstract matched.** Examples:
  - Ang et al.'s "forgo 2% of their wealth";
  - Rampini & Viswanathan's "More constrained firms engage in less risk management";
  - Rampini, Sufi & Viswanathan's finding that hedging "drops substantially as airlines approach distress and recovers only slowly";
  - Browne's equivalence between probability maximization and "buying a European digital option";
  - Grossman–Zhou's surplus rule W − αM;
  - Harvey et al.'s finding that short-dated puts are "the most reliable defensive method but also the most costly";
  - Israelov & Nielsen's "Option prices may be low, but their expected values tend to be even lower".
  - The dossier's [nrv] horizon detail for Bollerslev–Tauchen–Zhou is now confirmed: predictability is "particularly strong at the intermediate quarterly return horizon".
- **Metadata to complete.** None of these is a substantive error.
  - **Koijen et al., *Carry*:** JFE 127(2), 197–225 (2018), per WebSearch. The Consensus record carries the correct abstract but garbled metadata: the title shows as "Ralph S. J. Koijen" and the venue as *Journal of Finance*.
  - **Bailey et al., *The Probability of Backtest Overfitting*:** J. Computational Finance 20(4), 2017, DOI 10.21314/jcf.2016.322, per WebSearch.
  - **Daniel & Moskowitz:** JFE 122(2), 221–247 (2016), DOI 10.1016/j.jfineco.2015.12.002, per WebSearch. Consensus holds only the SSRN and working-paper versions.
  - **Issue numbers, from the DOIs:** Israelov & Nielsen 41(4); Bailey & López de Prado 40(5); Harvey & Liu 42(1); Hurst et al. 44(1).
  - **Titles missing from three [nrv] entries:**
    - Rampini & Viswanathan (2010), *Collateral, Risk Management, and the Distribution of Debt Capacity*;
    - Rampini, Sufi & Viswanathan (2014), *Dynamic Risk Management*;
    - Hardy (2001), *A Regime-Switching Model of Long-Term Stock Returns*.
  - **Jeanne & Rancière:** the published version is *Economic Journal* 121:905–930 (2011). A citing abstract reports its benchmark optimum as **9.1%** of output, against the working paper's **10.1%** used in dossier §2.3.
- **Content flags.** The citation is correct, but its use needs qualifying:
  1. **Lo (2002).** The dossier quotes only the i.i.d. standard error. The abstract's headline result is that serial correlation can overstate an annualized Sharpe ratio "by as much as 65 percent".
  2. **Moreira & Muir (2017).** This is cited as support for vol scaling raising Sharpe ratios. Two papers dispute that out of sample: Cederburg et al. (2020) and Barroso & Detzel (2021) (§5).
  3. **Bollerslev, Tauchen & Zhou (2009).** The predictability result is contested. Heston et al. (2023) find that implied variance does not predict underlying futures returns for most of the 20 assets they study.
  4. **Daniel & Moskowitz (2016).** The paper studies cross-sectional (equity) momentum. It supports a trend-reversal stress only by analogy.

### Backfill (14 topical searches)
The dossier's core is sound. It misses seven clusters that bear directly on the overlay's design:
1. **Funding-liquidity spirals and margin procyclicality.**
   - Theory: Brunnermeier & Pedersen 2009.
   - How to measure IM procyclicality: Murphy et al., BoE FSP 29.
   - VM stress with payment delays: Bardoscia et al. 2021.
   - Fund-level VM coverage: Jukonis et al. 2022; Rousová et al. 2020.
   - Collateral demand by venue: Duffie et al. 2015.
   - Fire-sale order: Chaderina et al. 2026.
   - These belong to Corporate Finance.
2. **How much backtested Sharpe survives in live trading**, especially for dealer-marketed strategies: Suhonen et al. 2017; Liu 2026; McLean & Pontiff 2016.
   - Related: search-aware evaluation of LLM-generated strategies (Gençay 2026), which maps directly onto the Overlay-Design agent.
3. **Long-horizon and very-long-sample evidence on defensive strategies:** McQuinn et al. 2020; Baltussen et al. 2026; Ilmanen et al. 2021.
   - Also preference-based evidence against long puts: Driessen & Maenhout 2007.
   - Also a theory result that liquidity dominates derivatives hedging: Gamba & Triantis 2014.
4. **Robustness critiques of trend and vol scaling:** Huang et al. 2020; Kim et al. 2016; Hutchinson & O'Brien 2014; Cederburg et al. 2020.
5. **Option-market state variables beyond VIX, VRP and SKEW:**
   - the left-tail premium (Andersen et al. 2019);
   - the vol-of-vol premium (Kaeck 2018);
   - jump-fear dynamics (Todorov 2009).
6. **Hedging the sovereign balance sheet:** Bodie et al. 2013; Gintschel & Scherer 2008. These give the dossier's "fiscal linkage" risk a formal hedging-demand term.
7. **Joint stock–bond regimes and the drivers of stock–bond correlation:** Guidolin & Timmermann 2005; Molenaar et al. 2024. Also generalized unsmoothing for sizing synthetic beta: Couts et al. 2020.

### Net assessment
- **Supported.** The headline conclusions stand:
  - puts lose money on a standalone basis;
  - collateral binds in a crisis;
  - the case for protection rests on liquidity and enabling channels;
  - opportunistic Sharpe ratios need deflation.
- **Further support.** Bhansali (2008), Cao et al. (2025), Schwalbach et al. (2025) and Asif et al. (2022) support a linear and trend core with a convex residual (§5).
- **Three substantive shifts.**
  1. **The convex sleeve.** Its case is weaker than the dossier allows. Size it at the low end. Justify it by gap, decision-latency and ambiguity protection. Require it to beat an equal-cost cash buffer in the recourse LP. This independently supports verifier finding R3.
  2. **Trend and the defensive stack.** Model trend as a regime-dependent crisis beta with post-crisis decay, not as an alpha source. Add a defensive-equity sleeve (quality and low-risk) as a candidate.
  3. **Collateral and the opportunistic book.**
     - The collateral engine needs a single funding-stress state that drives margins, haircuts and liquidation costs together, plus procyclicality metrics owned by Corporate Finance.
     - The opportunistic book needs haircuts that depend on where a backtest came from, and a trial ledger inside the agent sandbox.

---

## 2. Citation-integrity table

Status values: found, mismatched or not found. Differences between online-first and print years, and between working-paper and journal records, are not counted as mismatches.

| Dossier citation | Status | Corrected / confirmed metadata (Consensus unless stated) | Consensus URL |
|---|---|---|---|
| Harvey, Hoyle, Rattray, Sargaison, Taylor & Van Hemert (2019), *The Best of Strategies for the Worst of Times: Can Portfolios Be Crisis Proofed?*, JPM 45(5) | found | DOI 10.3905/jpm.2019.45.5.007 (venue label "Unknown Journal"); 19 citations. The abstract confirms three claims: short-dated puts are "the most reliable defensive method but also the most costly"; the post-2000 negative bond–equity correlation is "a historical rarity"; and TSMOM and quality performed well in drawdowns. | [link](https://consensus.app/papers/details/5c7e32af13ba53568cc69406ac82d5ef/?utm_source=claude_desktop) |
| Israelov (2019), *Pathetic Protection: The Elusive Benefits of Protective Puts*, JAI Winter 2019 | found | Record year 2018 (online-first); DOI 10.3905/jai.2018.1.066; 13 citations. A Practical Applications summary confirms the Winter 2019 JAI issue ([record](https://consensus.app/papers/details/d2883d57ff2f59b7a6359094b68d6bc1/?utm_source=claude_desktop)). The abstract says puts are "quite ineffective at reducing drawdowns versus the simple alternative of statically reducing exposure". | [link](https://consensus.app/papers/details/04d935e886325c24865db95e8121bfc9/?utm_source=claude_desktop) |
| Israelov & Nielsen (2015), *Still Not Cheap: Portfolio Protection in Calm Markets*, JPM | found | Add 41(4) (DOI 10.3905/jpm.2015.41.4.108); 16 citations. Covers 10 global equity indexes. | [link](https://consensus.app/papers/details/2f57572b2aef568f845db2b16628725e/?utm_source=claude_desktop) |
| Ang, Papanikolaou & Westerfield (2014), *Portfolio Choice with Illiquid Assets*, MS 60(11) | found | DOI 10.1287/mnsc.2014.1986; 171 citations. The abstract confirms state-dependent risk aversion and "forgo 2% of their wealth". | [link](https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop) |
| Froot, Scharfstein & Stein (1993), *Risk Management: Coordinating Corporate Investment and Financing Policies*, JF (NBER WP 4084) | found | Record year 1992 (WP); DOI 10.1111/j.1540-6261.1993.tb05123.x (JF 1993); 3,258 citations. The abstract confirms that hedging adds value when external finance costs more than internal funds, and mentions "nonlinear" instruments such as options. | [link](https://consensus.app/papers/details/547e703af74f547c9d16e38b79b642e9/?utm_source=claude_desktop) |
| Bolton, Chen & Wang (2011), *A Unified Theory of Tobin's q, Corporate Investment, Financing, and Risk Management*, JF 66(5) | found | The record carries NBER DOI 10.3386/w14845; 716 citations. The abstract confirms the double-barrier cash policy. | [link](https://consensus.app/papers/details/e303976b52515556ab7c0f0476889f19/?utm_source=claude_desktop) |
| Rampini & Viswanathan (2010), JF 65(6) [nrv] | found | Add title: *Collateral, Risk Management, and the Distribution of Debt Capacity*. DOI 10.1111/j.1540-6261.2010.01616.x; 489 citations. The dossier's claim matches the abstract. | [link](https://consensus.app/papers/details/ce566f1026cb5056852a77eb71fef1bb/?utm_source=claude_desktop) |
| Rampini, Sufi & Viswanathan (2014), JFE 111(2) [nrv] | found | Add title: *Dynamic Risk Management*. The record carries SSRN DOI 10.2139/ssrn.1875051; 235 citations. The abstract finds that more constrained airlines hedge less. | [link](https://consensus.app/papers/details/e86c89b63aeb51dcaea2c9919a32ce73/?utm_source=claude_desktop) |
| Dimmock, Wang & Yang (2024), *The Endowment Model and Modern Portfolio Theory*, MS 70(3) | found | Record year 2019 (NBER DOI 10.3386/w25559; venue *Manag. Sci.*). The abstract cites the MS supplement DOI 10.1287/mnsc.2023.4759; 25 citations. Crisis-state deviation from targets is confirmed. | [link](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop) |
| Browne (1999), *Reaching goals by a deadline: digital options and continuous-time active portfolio management*, Adv. Appl. Prob. 31(2) [nrv] | found | Record year 1996 (database artifact); DOI 10.1239/aap/1029955147; 133 citations. A citing abstract gives "Adv Appl Probab 31(2):551–577, 1999" ([Krabichler et al.](https://consensus.app/papers/details/c7d8bb6499c75f8e93935fa3a567584b/?utm_source=claude_desktop)). | [link](https://consensus.app/papers/details/2e3d0f7c7f585f1395468ce6a2fa6816/?utm_source=claude_desktop) |
| Jeanne & Rancière (2006), *The Optimal Level of International Reserves for Emerging Market Countries: Formulas and Applications*, IMF WP/06/229 | found | DOI 10.5089/9781451864892.001.a001; 293 citations. Published version: *Economic Journal* 121:905–930 (2011), DOI 10.1111/j.1468-0297.2011.02435.x, 382 citations ([record](https://consensus.app/papers/details/aaef823b3d385a89bdd71e64ee5fc430/?utm_source=claude_desktop)). [Mihailov et al. (2022)](https://consensus.app/papers/details/938d1ffd0ec15dfcb1901bf763e82e2b/?utm_source=claude_desktop) report the EJ benchmark optimum as 9.1% of output; the dossier's 10.1% is the WP figure. | [link](https://consensus.app/papers/details/418aee72f3cf5d33bf9a8355267b481f/?utm_source=claude_desktop) |
| Carr & Wu (2009), *Variance Risk Premiums*, RFS 22(3) [nrv] | found | DOI 10.1093/rfs/hhn038; 1,202 citations | [link](https://consensus.app/papers/details/aa330c81450d5cf6b34212059cd0fbb0/?utm_source=claude_desktop) |
| Bollerslev, Tauchen & Zhou (2009), *Expected Stock Returns and Variance Risk Premia*, RFS 22(11) | found | DOI 10.1093/rfs/hhp008; 296 citations. The abstract's "particularly strong at the intermediate quarterly return horizon" resolves the dossier's [nrv] horizon detail. A 2007 FEDS working paper also exists ([record](https://consensus.app/papers/details/998c8556931956c6bfde887106a3529f/?utm_source=claude_desktop)). | [link](https://consensus.app/papers/details/ec54a04e5a2f5bdb8ead82d72efcb84b/?utm_source=claude_desktop) |
| Bailey & López de Prado (2014), *The Deflated Sharpe Ratio*, JPM | found | Add 40(5) (DOI 10.3905/jpm.2014.40.5.094); 184 citations | [link](https://consensus.app/papers/details/378afd063fd15487a4fcb21af0850767/?utm_source=claude_desktop) |
| Bailey, Borwein, López de Prado & Zhu, *The Probability of Backtest Overfitting*, J. Comput. Finance (no year given) | found | Record year 2016; SSRN DOI 10.2139/ssrn.2326253; 114 citations. WebSearch: J. Computational Finance 20(4), 2017, DOI 10.21314/jcf.2016.322 (§7). | [link](https://consensus.app/papers/details/f5ef21e8509b544fba76ccc9aa2de55c/?utm_source=claude_desktop) |
| Harvey & Liu (2015), *Backtesting*, JPM Fall 2015 | found | Add 42(1) (DOI 10.3905/jpm.2015.42.1.013); 120 citations | [link](https://consensus.app/papers/details/26c79e6752075f64842d5bd2e1a67f72/?utm_source=claude_desktop) |
| Lo (2002), *The Statistics of Sharpe Ratios*, FAJ 58(4) [nrv] | found (use flag) | DOI 10.2469/faj.v58.n4.2453; 796 citations. The abstract's main result is that serial correlation can overstate an annual Sharpe ratio "by as much as 65 percent", and that √12 annualization is valid only "under very special circumstances". The dossier uses only the i.i.d. formula. | [link](https://consensus.app/papers/details/ae10105da6315c3da6ea60251ec0b456/?utm_source=claude_desktop) |
| Moskowitz, Ooi & Pedersen (2012), *Time Series Momentum*, JFE 104 | found | DOI 10.1016/j.jfineco.2011.11.003; 1,391 citations. The abstract confirms the strategy "performs best during extreme markets". | [link](https://consensus.app/papers/details/1e4090b52b0e50cc9e781c24971f060a/?utm_source=claude_desktop) |
| Koijen, Moskowitz, Pedersen & Vrugt, *Carry*, JFE (no year given) | found (garbled record) | The Consensus record has the *Carry* abstract, but its title reads "Ralph S. J. Koijen", with venue *The Journal of Finance*, year 2019 and DOI 10.1111/jofi.12643. **WebSearch: JFE 127(2), 197–225 (2018)** (§7). The abstract confirms that "carry downturns" coincide with "global recessions and liquidity crises". | [link](https://consensus.app/papers/details/564ce5970457555f927659bfb135fb3b/?utm_source=claude_desktop) |
| Hurst, Ooi & Pedersen (2017), *A Century of Evidence on Trend-Following Investing*, JPM Fall | found | Add 44(1) (DOI 10.3905/jpm.2017.44.1.015); 200 citations. The abstract confirms good performance in 8 of the 10 largest crisis periods since 1880. | [link](https://consensus.app/papers/details/0036703e863d57ab9239171b7a183db8/?utm_source=claude_desktop) |
| Daniel & Moskowitz (2016), *Momentum Crashes*, JFE 122(2) [nrv] | found (working-paper record) | Record: SSRN 2013, DOI 10.2139/ssrn.2371227, 838 citations. A 2011 WP record carries the abstract ([record](https://consensus.app/papers/details/1ce888448b7c5b8a86ada8b5c7cdfcaf/?utm_source=claude_desktop)): crashes "occur following market declines, when market volatility is high, and contemporaneous with market 'rebounds'". WebSearch: JFE 122(2), 221–247 (2016), DOI 10.1016/j.jfineco.2015.12.002. | [link](https://consensus.app/papers/details/940469f5dc2150e38955788f154aaa67/?utm_source=claude_desktop) |
| Mohajerin Esfahani & Kuhn (2018), Math. Prog. 171 [nrv] | found | Add title: *Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations*. DOI 10.1007/s10107-017-1172-1; 2,274 citations. The record lists only "D. Kuhn" and the preprint year 2015. | [link](https://consensus.app/papers/details/955158b8081d595c9c09458e32f6c2c0/?utm_source=claude_desktop) |
| Grossman & Zhou (1993), Math. Finance 3(3) [nrv] | found | Title: *Optimal Investment Strategies for Controlling Drawdowns*. DOI 10.1111/j.1467-9965.1993.tb00044.x; 385 citations. The abstract confirms the surplus rule W − αM. | [link](https://consensus.app/papers/details/5e80ded6b6c8585aa0607d96ebbfa9ae/?utm_source=claude_desktop) |
| Getmansky, Lo & Makarov (2004), JFE 74(3) [nrv] | found (working-paper records) | Two searches found no JFE record in Consensus. They returned thesis versions (Getmansky 2004 and [Makarov 2006](https://consensus.app/papers/details/ea8aa97099675752b481ce72e12ee5a0/?utm_source=claude_desktop)) and a citing abstract ([Di Cesare et al. 2015](https://consensus.app/papers/details/813ea087fa875f2a993953c2b1ac93ea/?utm_source=claude_desktop)). WebSearch: JFE 74 (2004) 529–609, DOI 10.1016/j.jfineco.2004.04.001. Issue number not confirmed. | [link](https://consensus.app/papers/details/4e43d079332f5046860f2f39350f56f9/?utm_source=claude_desktop) |
| Hardy (2001), NAAJ 5(2) [nrv] | found | Add title: *A Regime-Switching Model of Long-Term Stock Returns*. DOI 10.1080/10920277.2001.10595984; 523 citations. NAAJ 5(2):41–53 per a citing reference list ([record](https://consensus.app/papers/details/b9e0f142d515597b9dfc23f580cd8dc2/?utm_source=claude_desktop)). | [link](https://consensus.app/papers/details/4a85ab3069f756119b3c62ced49a131e/?utm_source=claude_desktop) |
| *Incidental:* Hamill, Rattray & Van Hemert (2016), *Trend Following: Equity and Bond Crisis Alpha*, Man AHL WP | found | SSRN DOI 10.2139/ssrn.2831926; 12 citations. The abstract confirms positive skew and strong performance in the worst equity and bond environments. Restrictions on long equity or bond positions "enhance the crisis alpha, but reduce the average return". | [link](https://consensus.app/papers/details/a91139d2da255358a68541aaf2958626/?utm_source=claude_desktop) |
| *Incidental:* Moreira & Muir (2017), *Volatility-Managed Portfolios*, JF 72(4) | found (use flag) | DOI 10.1111/jofi.12513; 437 citations. For the out-of-sample challenges, see §5. | [link](https://consensus.app/papers/details/a589969cb06858b8b654a0c6f054fb32/?utm_source=claude_desktop) |
| *Incidental:* Brunnermeier, Nagel & Pedersen (2009), *Carry Trades and Currency Crashes*, NBER Macro Annual 2008, 23 | found | Record year 2008; DOI 10.1086/593088; 1,049 citations. The "sudden unwinding" mechanism is confirmed. | [link](https://consensus.app/papers/details/8f1e8fe523865f0bbbf8aacf4c453be9/?utm_source=claude_desktop) |
| *Incidental:* Coval & Shumway (2001), *Expected Option Returns*, JF 56(3) [nrv] | found | DOI 10.1111/0022-1082.00352; 772 citations. The abstract reports that zero-beta ATM straddles lose "approximately three percent per week". | [link](https://consensus.app/papers/details/20605949192753459266a5abb7b25945/?utm_source=claude_desktop) |

---

## 3. Annotated bibliography (25 papers)

None of the 25 is cited by the dossier; the dossier-cited works are verified in §2. Entries are grouped by the design question they inform.

### A. Collateral, margin and funding liquidity (Corporate Finance / Treasurer)

**1. [Market liquidity and funding liquidity](https://consensus.app/papers/details/7c944d8f27a65feea50c7b83eea8e1e3/?utm_source=claude_desktop)**
- M. Brunnermeier et al. · 2009 · *Review of Financial Studies* · 5,153 citations · DOI 10.1093/rfs/hhn098
- *Finding:*
  - Margins can be destabilizing. Market liquidity and traders' funding liquidity are mutually reinforcing, which produces liquidity spirals.
  - The model explains why market liquidity can suddenly dry up, is common across securities, is related to volatility, is subject to flight to quality, and comoves with the market.
- *Relevance to ADIC:* The dossier sets three groups of inputs separately: IM rates m(s), collateral haircuts h, and recourse capacity and cost ȳ_k(s), c_k(s).
  - **[Inference]** This paper implies they should move together, driven by one funding-stress state, so that margin calls, haircuts and liquidation costs spike together in S3.
  - Corporate Finance's C2 coverage test should use that joint spike.

**2. [Financial Stability Paper No. 29 – May 2014](https://consensus.app/papers/details/6ccff24a70ce5d71aa08e81931ababd2/?utm_source=claude_desktop)**
- David Murphy et al. · 2014 · Bank of England Financial Stability Paper (venue label "Unknown Journal") · 47 citations · no DOI shown
- *Finding:*
  - Common initial-margin models are procyclical.
  - The paper proposes two measures: margin variation across the cycle, and short-term margin increases.
  - Models that pass common risk-sensitivity tests "can have very different levels of procyclicality".
  - It recommends that CCPs and dealers disclose these measures so that users can anticipate margin calls.
- *Relevance to ADIC:* This is the right replacement for the dossier's calibration target of ">100% IM jump within ~1 week of S3", which the verifier flagged (R5).
  - **[Inference]** Corporate Finance should obtain these two metrics from each CCP and dealer and calibrate IM paths by venue.

**3. [Simulating liquidity stress in the derivatives market](https://consensus.app/papers/details/2ed33ac2bdc9586d98e71535615286bf/?utm_source=claude_desktop)**
- M. Bardoscia et al. · 2021 · *Journal of Economic Dynamics and Control* · 48 citations · DOI 10.2139/ssrn.3508655 (SSRN DOI on the record)
- *Finding:*
  - The paper simulates VM calls in a stress scenario from trade-repository data and compares them with cash buffers.
  - Institutions delay payments while waiting for receipts, so shortfalls grow as they spread through the network.
  - The aggregate shortfall was a modest fraction of daily repo borrowing. Central coordination of payments would avoid only a small part of it.
- *Relevance to ADIC:* The dossier books VM inflows on the hedge book as T+1 receipts.
  - **[Inference]** In S3, add a receipt-delay and partial-payment haircut on VM that stressed dealers owe ADIC. That is exactly when the convex sleeve pays.

**4. [The Impact of Derivatives Collateralisation on Liquidity Risk: Evidence from the Investment Fund Sector](https://consensus.app/papers/details/8235e347f86b5b799f4cd8e4e7e31838/?utm_source=claude_desktop)**
- Audrius Jukonis et al. · 2022 · SSRN · 2 citations · DOI 10.2139/ssrn.4305519. An IMF WP version (2024) also exists ([record](https://consensus.app/papers/details/4ff5997db80f577d9b07b655015e66fe/?utm_source=claude_desktop)).
- *Finding:*
  - Using transaction-level derivatives data, between 13% and 33% of euro-area funds with sizeable derivatives exposure may lack the liquidity buffers to meet VM calls in stress scenarios.
  - Those funds would likely redeem MMF shares, sell assets procyclically and draw credit lines.
- *Relevance to ADIC:*
  - This is a method template for ADIC's VM stress: revalue each transaction under each scenario, then compare with unencumbered HQLA.
  - It is also a plausibility anchor that naive buffers fail. Corporate Finance owns this test.

**5. [Central Clearing and Collateral Demand](https://consensus.app/papers/details/c3c3447985445b129533b8517cc5f424/?utm_source=claude_desktop)**
- J. D. Duffie et al. · 2015 · SSRN · 229 citations · DOI 10.2139/ssrn.2388894
- *Finding:*
  - The paper decomposes collateral demand in CDS, including the "velocity drag" of VM movements.
  - IM requirements significantly raise system-wide collateral demand.
  - Once dealers post IM to each other, central clearing lowers system-wide demand unless CCPs proliferate. It still has distributional effects across types of participant.
- *Relevance to ADIC:* Venue choices change ADIC's collateral demand: listed options, OTC under a CSA, or cleared CDX.
  - **[Inference]** C2 and C3 should include a velocity-drag term for collateral in transit and the IM cost of each venue. Corporate Finance should charge the overlay accordingly.

### B. Why insure, and against what (theory)

**6. [Corporate Risk Management: Integrating Liquidity, Hedging, and Operating Policies](https://consensus.app/papers/details/c6027dda48605911a46b3578a9a0a3ea/?utm_source=claude_desktop)**
- Andrea Gamba et al. · 2014 · *Management Science* · 87 citations · DOI 10.1287/mnsc.2013.1752
- *Finding:*
  - With several frictions, liquidity plays a "critical and distinct role in risk management, justifying high levels of cash".
  - The marginal value of derivatives hedging "is likely to be low".
  - Interactions with operating flexibility are non-monotonic.
- *Relevance to ADIC:* This is independent theoretical support for verifier finding R3: on Jeanne–Rancière logic, cash buffers dominate option insurance.
  - **[Inference]** Set the cash and T-bill buffer first. Then require each option program to add value beyond an equal-cost cash buffer in the recourse LP.

**7. [Sovereign Wealth and Risk Management: A Framework for Optimal Asset Allocation of Sovereign Wealth](https://consensus.app/papers/details/848357ab551a580793407efeed637bbb/?utm_source=claude_desktop)**
- Z. Bodie et al. · 2013 · SSRN · 21 citations · DOI 10.2139/ssrn.1460692
- *Finding:*
  - Contingent-claims analysis of the sovereign's economic balance sheet.
  - Optimal sovereign wealth combines a performance-seeking portfolio with three hedging demands: against the variability of the fiscal surplus, external debt and domestic debt.
  - Applied to Chile, it finds sovereign investment under-diversified.
- *Relevance to ADIC:* The owner's distribution claim is ADIC's liability.
  - **[Inference]** The tail hedge should also target the owner's fiscal-surplus shock (the high-λ states), not only equity drawdowns. This gives the dossier's "fiscal linkage" risk (§8) a formal hedging-demand term.

**8. [An Empirical Portfolio Perspective on Option Pricing Anomalies](https://consensus.app/papers/details/39ee84c156a85bf1a821939d34d237d8/?utm_source=claude_desktop)**
- Joost Driessen et al. · 2007 · *Review of Finance* · 135 citations · DOI 10.1093/rof/rfm024
- *Finding:*
  - Using S&P 500 options, CRRA investors "always" find it optimal to short OTM puts and ATM straddles. This is robust to transaction costs, margins and peso problems.
  - Loss-averse and disappointment-averse investors also hold short option positions.
  - Only "highly distorted probability assessments" give positive put weights.
- *Relevance to ADIC:* On preferences alone, buying puts is suboptimal. The dossier's case therefore has to rest on constraints (liquidity, the floor, decision latency), and the recourse LP must demonstrate them.
  - **[Inference]** The same logic makes short volatility look attractive for the opportunistic book. The dossier's λ-adjusted ranking is the necessary correction.

### C. Tail-hedge design evidence (Overlay)

**9. [Portfolio Protection? It's a Long (Term) Story…](https://consensus.app/papers/details/e9f89272a0c75f1694ec26afc6a78044/?utm_source=claude_desktop)**
- Nicholas McQuinn et al. · 2020 · *Journal of Portfolio Management* (DOI 10.3905/jpm.2020.1.203; venue label "Unknown Journal"; February 2021 issue per its [Practical Applications summary](https://consensus.app/papers/details/5db574b66d8a5b00bca57b3f771ea5f9/?utm_source=claude_desktop)) · 3 citations
- *Finding:*
  - Options-based hedging works over short periods, but its efficacy "wanes at longer horizons". It eventually underperforms 60/40 even in bad outcomes for 60/40, and it is punitive in long bull markets.
  - Defensive equities, risk parity, alternative risk premia and trend added value more consistently in long drawdowns. Unlike puts, they can also profit in rising markets.
- *Relevance to ADIC:* The Tier-2 objective, P(5-year return ≥ 10%), is a long-horizon target.
  - **[Inference]** Judge the convex sleeve on 5-year outcome deltas, not on payoffs in crash windows. Slow grinds such as 2000–02 and 2022 weigh more on P(5y ≥ 10%) than fast crashes do.

**10. [The Best Defensive Strategies: Two Centuries of Evidence](https://consensus.app/papers/details/631cea0eea6a5c49ac808ba06cdf9685/?utm_source=claude_desktop)**
- Guido Baltussen et al. · 2026 · *Financial Analysts Journal* · 0 citations (new) · DOI 10.1080/0015198x.2025.2602270
- *Finding:*
  - Over more than 220 years of global data, defensive equity factors (low-risk, quality and value) consistently provide downside protection.
  - Gold and put options are "less drawdown or cost-effective".
  - A multi-asset defensive absolute return (DAR) portfolio and trend-following are the most effective, and each diversifies the other across stages of a drawdown.
- *Relevance to ADIC:* The dossier's own Harvey et al. table lists quality long/short among the most promising crisis hedges, yet the recommended stack omits defensive equity.
  - **[Inference]** Add a quality or low-risk long/short sleeve, via swaps or Public Markets managers, to the candidate set for the defensive-stack frontier.

**11. [Tail Risk Hedging: Contrasting Put and Trend Strategies](https://consensus.app/papers/details/43784349e13c5677906664bba2e5b7c7/?utm_source=claude_desktop)**
- A. Ilmanen et al. · 2021 · *Journal of Systematic Investing* · 7 citations · DOI 10.52354/jsi.1.1.vi
- *Finding:*
  - The paper compares index put buying with multi-asset trend as tail hedges, on long-run cost and on reliability and efficiency in equity tail events.
  - The common view that puts cost more but hedge better "contains a kernel of truth". The cost advantage nonetheless favors trend.
- *Relevance to ADIC:* It supports trend as the core and argues for keeping the put budget small.

**12. [Equity Tail Protection Strategies Before, During, and After COVID-19](https://consensus.app/papers/details/4f6c8f8b5663580c902b7823c7d1f6c3/?utm_source=claude_desktop)**
- Roni Israelov et al. · 2023 · *Journal of Portfolio Management* (venue label "Unknown Journal") · 0 citations · DOI 10.3905/jpm.2023.1.575
- *Finding:* The paper studies four strategies across four periods around COVID: puts, long volatility via options, long VIX futures, and a VIX-call overlay.
  - Hedging is expensive.
  - The variable equity exposure embedded in options is a source of risk and path dependence.
  - Whether to delta-hedge changes results "in nonforecastable ways".
  - Hedgers "should plan for the possibility that their hedges make things worse in times of stress".
- *Relevance to ADIC:* The dossier does not specify a delta-hedging policy.
  - **[Inference]** Make delta-hedging an explicit, IC-approved parameter of the convex sleeve and run both variants as ablations.

**13. [Tail Risk Management with Puts and Trend Following: A CVaR Framework for Crashes and Drawdowns](https://consensus.app/papers/details/92a1311197d0523f80a910cfee7401eb/?utm_source=claude_desktop)**
- Miquel Noguer I. Alonso · 2026 · arXiv preprint · 0 citations · DOI 10.48550/arxiv.2607.00883
- *Finding:*
  - The paper models put options and trend inside one continuous-time CVaR mandate, with the option sleeve marked to market.
  - Convex insurance reprices immediately when a jump hits. Trend is "late on the first shock" but grows more defensive through persistent drawdowns.
  - In stylized Monte Carlo, hybrids reduce terminal CVaR relative to either sleeve alone. The best weights depend on calibration.
  - It proposes a four-axis diagnostic: conditional convexity, tail-event reliability, non-stress carry and drawdown persistence.
- *Relevance to ADIC:* It formalizes the dossier's logic of a linear and trend core with a convex residual for gaps.
  - **[Inference]** Use the four axes as columns of the IC's defensive-stack frontier. Note that this is a preprint with stylized results only.

**14. [The Pricing of Tail Risk and the Equity Premium: Evidence From International Option Markets](https://consensus.app/papers/details/756ab3d8847a5e9980ed69e3bcd9d922/?utm_source=claude_desktop)**
- Torben G. Andersen et al. · 2019 · *Journal of Business & Economic Statistics* · 75 citations · DOI 10.1080/07350015.2018.1564318
- *Finding:*
  - The premium for negative tail events in index options "displays persistent shifts, unrelated to volatility".
  - It predicts future equity returns for all the indices studied. Implied volatility forecasts only future return variation.
  - Compensation for negative jump risk is the main driver of the equity premium, with strong commonality across markets.
- *Relevance to ADIC:* The dossier times option purchases on VRP and SKEW.
  - **[Inference]** Add an option-implied left-tail premium as the state variable for the cost of protection. A high tail premium makes protection dear exactly when expected equity returns are high, which also informs the dynamic beta overlay.

**15. [Variance-of-variance risk premium](https://consensus.app/papers/details/6b580eebc04850629b97dce54c28d233/?utm_source=claude_desktop)**
- Andreas Kaeck · 2018 · *Review of Finance* · 12 citations · DOI 10.1093/rof/rfx008
- *Finding:*
  - Over 2006–2014, strategies that exploit the gap between implied and realized variance of the VIX earned average excess returns of **−24.16% per month**.
  - The alpha was −16.98% after Fama–French, Carhart and variance-risk adjustments.
- *Relevance to ADIC:* **[Inference]** Read as a large premium paid by buyers of VIX convexity.
  - The VIX-call sleeve's carry should embed a strongly negative vol-of-vol premium.
  - The dossier's VXTH cost of 0.09 per crisis dollar depends on COVID; the verifier found 0.42 ex-COVID on a common window.
  - Treat VIX calls as a small, crash-specific sleeve.

### D. Robustness of trend and vol scaling (Overlay)

**16. [Time series momentum: Is it there?](https://consensus.app/papers/details/5d98bd221fe45fc38bf795d02c220009/?utm_source=claude_desktop)**
- Da-Shan Huang et al. · 2020 · *Journal of Financial Economics* · 102 citations · DOI 10.1016/j.jfineco.2019.08.004
- *Finding:*
  - Asset-by-asset regressions show "little evidence" of time-series momentum, in or out of sample.
  - The pooled t-statistic falls below parametric and nonparametric bootstrap critical values.
  - The strategy is profitable, but performs "virtually the same" as a strategy based on historical sample means, which needs no predictability.
- *Relevance to ADIC:* This weakens trend as an alpha source.
  - **[Inference]** Value trend for its crisis convexity, through a regime-dependent beta, rather than for a positive unconditional Sharpe ratio. Treat the dossier's 0.3 normal-state template as an upper bound.

**17. [Is This Time Different? Trend-Following and Financial Crises](https://consensus.app/papers/details/0f71676fcce356dbb83d98b7ca85c713/?utm_source=claude_desktop)**
- Mark C. Hutchinson et al. · 2014 · *Journal of Alternative Investments* · 19 citations · DOI 10.3905/jai.2014.17.2.082
- *Finding:*
  - Using almost a century of data, trend's average returns in "an extended period following financial crises" are less than half those in no-crisis periods.
  - Futures markets lose much of their usual time-series predictability, and returns are weak in the four years after a crisis begins.
  - Regional crises show a similar pattern.
- *Relevance to ADIC:* The dossier's trend template rises to a Sharpe of 0.6 in S3 but has no post-crisis state.
  - **[Inference]** Add a recovery regime in which trend's Sharpe ratio is cut by at least half for several years.

**18. [On the performance of volatility-managed portfolios](https://consensus.app/papers/details/a5037358ed56548e9b242074c574271b/?utm_source=claude_desktop)**
- Scott Cederburg et al. · 2020 · *Journal of Financial Economics* · 100 citations · DOI 10.1016/j.jfineco.2020.04.015
- *Finding:*
  - Across 103 equity strategies, volatility-managed portfolios do not systematically outperform the unmanaged originals.
  - The alphas from spanning regressions are not implementable in real time.
  - Realistic out-of-sample versions earn lower certainty equivalents and Sharpe ratios than the unmanaged portfolios, because the spanning regressions are structurally unstable.
- *Relevance to ADIC:* The dossier cites Moreira & Muir as [S] support for vol scaling raising Sharpe ratios (§2.6).
  - **[Inference]** Justify the opportunistic book's vol targeting ℓ_t = v_t / σ̂ by tail and vol-of-vol control, as in Harvey et al. 2018. Set the expected Sharpe uplift to zero in the base case.

### E. Opportunistic book: evidence standards and agent evaluation (Overlay and agents)

**19. [Quantifying Backtest Overfitting in Alternative Beta Strategies](https://consensus.app/papers/details/df15834241b85f16a52df4f546753386/?utm_source=claude_desktop)**
- Antti Suhonen et al. · 2017 · *Journal of Portfolio Management* · 26 citations · DOI 10.3905/jpm.2017.43.2.090
- *Finding:*
  - For 215 alternative-beta strategies developed and promoted by global investment banks, Sharpe ratios fell by a **median 73%** from backtest to live trading.
  - The most complex strategies deteriorated by over 30 percentage points more than the simplest.
  - Risk-factor exposures were reasonably robust for equity volatility and FX carry, and weak for equity value.
- *Relevance to ADIC:* ADIC's opportunistic book is an OTC derivatives book, which plausibly includes dealer-designed strategies.
  - **[Inference]** Apply a haircut based on where the backtest came from before the DSR gate: at least 70% for dealer backtests, more for complex ones. The dossier's Sharpe prior of 0.3 is consistent with this.

**20. [Evaluating Structured Strategy Backtests: Peer Benchmarks, Regime Timing, and Live Performance](https://consensus.app/papers/details/d70409fd4c065825a2f18fa4ce135eff/?utm_source=claude_desktop)**
- Chang Liu · 2026 · arXiv preprint · 0 citations · DOI 10.48550/arxiv.2604.18821
- *Finding:*
  - Across 1,726 commercially distributed structured strategies from ten institutions, pro-forma performance has "only limited portability" into live trading. It weakens sharply when measured against peer and external benchmarks.
  - Marketed backtests mainly reflect the factor regime before launch.
  - Strategies launched after unusually strong factor conditions deteriorate more.
- *Relevance to ADIC:* **[Inference]** The Overlay-Challenge agent should benchmark each dealer backtest against peer strategies, and raise the discount when launch follows an extreme factor run.

**21. [Sharpe Ratio Inference: A New Standard for Decision Making and Reporting](https://consensus.app/papers/details/a5bf04463c2f5b8e8d1a6b474c79443f/?utm_source=claude_desktop)**
- Marcos López de Prado et al. · 2026 · *Journal of Portfolio Management* (venue label "Unknown Journal") · 2 citations · DOI 10.3905/jpm.2026.1.837
- *Finding:*
  - The paper names five recurring pitfalls in Sharpe-ratio inference, including assuming i.i.d. normal returns and ignoring test power and multiple testing.
  - It derives a closed-form approximation to the sampling distribution of the Sharpe ratio when returns are jointly non-normal and serially correlated.
- *Relevance to ADIC:* **[Inference]** This should replace the i.i.d. standard error on the opportunistic evidence card (§2.6). Using one consistent inference framework also removes the verifier's frequency-mixing problem (R4/E23).

**22. [What survives honest evaluation? Leakage-safe, search-aware assessment of LLM-driven trading strategy discovery](https://consensus.app/papers/details/f218fb3f22f95742b8e70415676bb8da/?utm_source=claude_desktop)**
- Eray Gençay · 2026 · arXiv preprint · 0 citations · DOI 10.48550/arxiv.2608.27734
- *Finding:*
  - The agent can act only through registry-validated tools that exclude look-ahead by construction.
  - A deliberately leaky oracle with a Sharpe ratio of 35 "survives Deflated Sharpe and probability-of-backtest-overfitting testing completely".
  - The system records every evaluation and deflates results by the agent's own trial count. On that basis, honest evaluation certified passive benchmarks and rejected every LLM-discovered strategy, across two frontier models, search budgets up to 100 candidates, and five runs.
- *Relevance to ADIC:* This is a direct analogue of the Overlay-Design agent.
  - **[Inference]** Statistical deflation does not substitute for leakage control. Build a point-in-time data registry and a ledger of every trial into the sandbox, and feed that ledger into the N used by DSR and PBO.

### F. State engine and exposure measurement

**23. [An Econometric Model of Nonlinear Dynamics in the Joint Distribution of Stock and Bond Returns](https://consensus.app/papers/details/155cfe8fb73053bdbec4607b90579297/?utm_source=claude_desktop)**
- Massimo Guidolin et al. · 2005 · *Journal of Applied Econometrics* · 280 citations · DOI 10.1002/jae.824
- *Finding:*
  - Two- or three-state models capture stocks or bonds alone. The joint distribution needs four regimes: crash, slow growth, bull and recovery.
  - Exits from the crash state go almost always to recovery, "with close to 50 percent chance", a bounce-back effect.
- *Relevance to ADIC:* The dossier's state engine is a 4-state HMM on VIX alone.
  - **[Inference]** A joint stock–bond regime layer would capture the post-crash recovery state, when trend reverses and hedges must be monetized, and would give the duration sleeve a regime-dependent payoff.

**24. [Empirical Evidence on the Stock–Bond Correlation](https://consensus.app/papers/details/0ca1d37b4a305867b81d7c3a53abb95d/?utm_source=claude_desktop)**
- R. Molenaar et al. · 2024 · *Financial Analysts Journal* · 14 citations · DOI 10.1080/0015198x.2024.2317333
- *Finding:*
  - The stock–bond correlation shows "abrupt regime shifts" after long periods of stability.
  - Inflation, real rates and government creditworthiness are important drivers.
  - Increases in the correlation raise multi-asset portfolio risk and bond risk premia.
- *Relevance to ADIC:* These are concrete state variables for the dossier's rule to hold duration only when the correlation regime supports it.

**25. [Unsmoothing Returns of Illiquid Funds](https://consensus.app/papers/details/38f7d68ab4a759ecb109c8dfcba5597d/?utm_source=claude_desktop)**
- Spencer J. Couts et al. · 2020 · SSRN · 14 citations · DOI 10.2139/ssrn.3544854
- *Finding:*
  - Funds with similar investments share a common source of spurious autocorrelation. Traditional unsmoothing does not fully remove it, so systematic risk is underestimated.
  - A generalized unsmoothing method improves measured risk exposures and risk-adjusted performance for hedge funds and private real-estate funds.
  - Average illiquid-fund alpha is lower than previously thought.
- *Relevance to ADIC:* The synthetic-beta notional N^β depends on the de-smoothed private beta (§3.6, which uses Getmansky–Lo–Makarov θ-weights).
  - **[Inference]** Generalized unsmoothing across the PE book reduces the risk of understating true beta, and hence of mis-sizing the beta overlay.

---

## 4. Missed-but-important papers: design implications

Numbers in brackets refer to §3. Other papers are linked inline.

### 4.1 State variables (additions to dossier §6.2)
- **Funding-stress state F_t.** Repo haircuts, secured–unsecured funding spreads and dealer balance-sheet stress jointly drive m(s), h(s), ȳ_k(s) and c_k(s) [1].
  - [Boudt et al. 2017](https://consensus.app/papers/details/f810e62599e25377b4a05ce2c696246b/?utm_source=claude_desktop) find that equity-collateralized funding liquidity switches regime near a TED spread of 48 bp (2006–2011 sample).
  - **[Inference]** TED is LIBOR-based. Re-estimate the threshold on a current secured–unsecured spread.
- **Left-tail premium τ_t.** Add it as the cost-of-protection signal, alongside VRP and SKEW [14].
  - [Todorov 2009](https://consensus.app/papers/details/87881ba544365291beac3962db734c84/?utm_source=claude_desktop) shows that willingness to pay for jump protection "increases significantly immediately after the occurrence of jumps".
  - This is the mechanism behind the dossier's rule never to "catch up" in the stress state.
  - [Aït-Sahalia et al. 2020](https://consensus.app/papers/details/c0602e53d78351b6a2bf4d17613bbd73/?utm_source=claude_desktop) show the effect is "stronger for short maturities, but more persistent for long maturities". That supports the dossier's heuristic to monetize short-dated options and re-buy longer-dated ones after spikes.
- **VIX vol-of-vol premium** for pricing the VIX-call sleeve [15].
- **Drivers of stock–bond correlation:** inflation, real rates and sovereign creditworthiness [24].
  - [Ahelegbey et al. 2026](https://consensus.app/papers/details/19b5132515e85e34b7c1f19bace18338/?utm_source=claude_desktop) estimate inflation thresholds from the data. Above them, stock–bond correlations "become significantly stronger".
- **Joint stock–bond regime with a recovery state** [23]. **[Inference]** It can sit alongside the VIX HMM as a second regime stream.
- **Crisis beta of the hedge-fund book.**
  - [Agarwal & Naik (2003/2004)](https://consensus.app/papers/details/6c11eda0862b5ed6b3244b0e9d97c335/?utm_source=claude_desktop): many equity-oriented hedge-fund strategies have payoffs "resembling a short position in a put option on the market index".
  - [Boyson et al. 2010](https://consensus.app/papers/details/010bdfd384ec50809ef53bffb82b8263/?utm_source=claude_desktop): contagion across hedge-fund styles rises with adverse liquidity shocks (credit spreads, the TED spread, prime-broker and bank stocks).
  - **[Inference]** Size the tail hedge on the total portfolio, netting the short-put exposure embedded in the Public Markets group's hedge funds (working NAV $20bn).
- **Owner fiscal and oil state** [7].
  - [Gintschel & Scherer 2008](https://consensus.app/papers/details/0644f03ab6be5e608a59b751de988332/?utm_source=claude_desktop) find the hedge potential of financial assets against oil reserves "substantial": risk reduction up to 50%, or 10% without short sales. They find the hedge decision more important than the choice of point on the efficient frontier.
  - **[Inference]** Add the oil price and the owner's fiscal balance to x_t, and link D_t to them.

### 4.2 Models
- **IM engine.** Report Murphy et al.'s two procyclicality metrics for each venue [2]. Calibrate central IM from margin histories and keep the >100% jump as a stress quantile, as the verifier advised (R5).
- **VM engine.** Add a network and receipt-delay layer [3], and revalue each transaction under each scenario [4].
  - [Rousová et al. 2020](https://consensus.app/papers/details/1568e37e2c845eef816b5c7ccc9f8648/?utm_source=claude_desktop) report that euro-area funds met "the fivefold increase in variation margin" in the COVID stress, some only by repo, asset sales and credit-line draws.
- **Collateral demand by venue** [5]. Include velocity drag and IM for each venue in the C2 and C3 tests.
- **Liquidation waterfall.**
  - [Chaderina et al. 2026](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop) find that selling the most liquid bonds first "can backfire" when they are widely held and buying capital is scarce: liquid bonds suffered the largest price declines in fire sales.
  - **[Inference]** Make the cost of each waterfall step depend on crowding. Keep cash and T-bills as the first line, as the dossier already recommends.
- **De-smoothing for synthetic beta** [25].
- **Allocating the defensive stack.** Use a joint puts-plus-trend CVaR control [13].
  - Add [Cao et al. 2025](https://consensus.app/papers/details/39d8f0dc908957eb9ed5c2a6d24d70da/?utm_source=claude_desktop) as a baseline. They find a naive futures hedge "remarkably effective at managing tail risk". Few other methods beat it, and estimation error explains why.
  - **[Inference]** The meta-controller should include a naive futures hedge among its baselines.
- **Chance constraints under ambiguity.**
  - [Ji & Lejeune 2020](https://consensus.app/papers/details/54e3a182544c5fdea9d5c1226a16c30c/?utm_source=claude_desktop) give MILP, MISOCP and LP reformulations for data-driven Wasserstein chance constraints.
  - **[Inference]** These make C1 and C8 tractable inside the robust layer.
- **Operational MPC loop.**
  - [Nystrup et al. 2018](https://consensus.app/papers/details/88b77eb53f2f532483982aba3c5ba5fb/?utm_source=claude_desktop) combine MPC with multivariate HMM forecasts and adjust risk aversion to realized drawdown. They control drawdowns "with little or no sacrifice of mean–variance efficiency".
  - This is a working precedent for the dossier's monthly MPC loop.

### 4.3 Parameters and calibration priors (literature values, not ADIC data)

| Parameter | Literature value | Source | Use in the framework |
|---|---|---|---|
| Fall in Sharpe ratio from backtest to live, dealer alternative-beta strategies | Median −73%; complex strategies >30 pp worse | [19] | Haircut on dealer strategies before the DSR gate |
| Out-of-sample and post-publication decay of published predictors | −26% out of sample; −58% after publication | [McLean & Pontiff 2016](https://consensus.app/papers/details/91c15861c4fc5b96bc84c44174fcd8ec/?utm_source=claude_desktop) | Haircut on academic strategies. **[Inference]** These are equity cross-sectional predictors; applying them to macro carry and trend is an assumption. |
| Backtest Sharpe as a predictor of out-of-sample performance | R² < 0.025 (888 Quantopian algorithms) | [Wiecki et al. 2016](https://consensus.app/papers/details/cbf1b88914f55668987babb345905af4/?utm_source=claude_desktop) | Supports shrinkage weight w close to zero for unvalidated strategies |
| Peak VM multiple in COVID, euro-area funds | About 5× | [Rousová et al. 2020](https://consensus.app/papers/details/1568e37e2c845eef816b5c7ccc9f8648/?utm_source=claude_desktop) | Fund-level VM stress scenario; compare with the FSB per-CCP 2.3× vs the prior quarter |
| Share of derivative-heavy funds whose buffers fail under VM stress | 13–33% | [4] | Plausibility check on C2 under naive buffers |
| Trend return after a crisis | Below half of no-crisis returns for an extended period; weak for about 4 years | [17] | Trend Sharpe multiplier ≤ 0.5 in a recovery regime |
| Return on VIX variance strategies | −24.16% per month (2006–2014) | [15] | Carry on the VIX-call sleeve outside crashes |
| Out-of-sample Sharpe uplift from vol management | None on average | [18]; [Barroso & Detzel 2021](https://consensus.app/papers/details/9215ab0a4dd7570bba231fc4f29794f2/?utm_source=claude_desktop) (zero abnormal returns after costs for factors other than the market) | Set the uplift to 0 in the base case |
| Vol targeting across a portfolio of CTA managers | +0.53% to +0.80% a year out of sample | [Molyboga 2020](https://consensus.app/papers/details/273253dcf8a75e1ab6b2d8ece50c2642/?utm_source=claude_desktop) | Applies only if the opportunistic book allocates to external CTAs |
| Overstatement of hedge-fund Sharpe from serial correlation | Up to 65% | Lo (2002), verified in §2 | Evidence card; external manager track records |
| Funding-regime threshold | TED spread ≈ 48 bp (2006–2011) | [Boudt et al. 2017](https://consensus.app/papers/details/f810e62599e25377b4a05ce2c696246b/?utm_source=claude_desktop) | Threshold for F_t; re-estimate on a current spread |
| Risk at the drawdown limit | Keep a small "risk floor" instead of cutting to zero | [Zhou et al. 2015](https://consensus.app/papers/details/a51e4fdec00e59f7a150158ff3f078c8/?utm_source=claude_desktop) | Floor on g(DD) (§4.4) |

### 4.4 Constraints
- **C2, stressed collateral coverage.**
  - Apply regime-dependent haircuts and margins driven by F_t [1].
  - Haircut VM receivables from stressed counterparties for delays [3].
  - Use liquidation values that depend on crowding ([Chaderina et al. 2026](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop)).
- **C5, counterparty.** **[Inference]** Beyond default probability, model delayed or partial VM from stressed dealers [3]. Cut the liquidity recognition factor φ^OTC in S3 accordingly.
- **C6, precommitment.**
  - Rampini, Sufi & Viswanathan (2014), verified in §2, show that hedging falls as firms approach distress.
  - [Rampini et al., *Risk Management in Financial Institutions* (NBER WP)](https://consensus.app/papers/details/57b5729c2197580ea311659a6e2d3970/?utm_source=claude_desktop) find that better-capitalized institutions hedge more, and that institutions hit by net-worth shocks "reduce hedging substantially".
  - Both support the floor h_min and logged IC overrides.
  - **[Inference]** Fix h_min in a multi-year budget rather than by annual discretion.
- **C7, capacity.**
  - [Baltas & Kosowski 2013](https://consensus.app/papers/details/fca5e103448d5fa9ba2a269e8f7ba03e/?utm_source=claude_desktop) find no statistically significant capacity constraints in time-series momentum across futures markets.
  - **[Inference]** Trend caps can be looser than caps on relative value or short volatility. ADV caps still apply at ADIC's size.
- **C7, drawdown stop.**
  - [Zhou et al. 2015](https://consensus.app/papers/details/a51e4fdec00e59f7a150158ff3f078c8/?utm_source=claude_desktop) show that with transaction costs, Grossman–Zhou scaling can produce negative expected returns near the drawdown limit. They propose a risk floor or "no-action zone".
  - **[Inference]** Replace g(DD) = (1 − DD/DD_max)⁺ with max(g_min, (1 − DD/DD_max)⁺).
  - Kaminski & Lo (2014) remains unchecked (§7).

### 4.5 Objectives
- **Behind-target risk-taking.**
  - [Capponi & Zhang 2024](https://consensus.app/papers/details/0fd71f5302ce52aead087822575e14e4/?utm_source=claude_desktop) find that an all-or-nothing goal investor is "more risk seeking if not on track", and more risk averse near the deadline when well funded.
  - **[Inference]** Maximizing P(5y ≥ 10%) can therefore reward gambling when the fund is behind target, for example by levering the opportunistic book or selling convexity.
  - Keep the C8 floor and the CVaR(DD) term. Report any increase in risk taken while behind target to the IC.
- **State-dependent floor.**
  - [Bernard et al. 2014](https://consensus.app/papers/details/82b1f7d2c1045a94a08df3af8321c4f5/?utm_source=claude_desktop) impose constraints on final wealth in stressed-market states and show the resulting strategies outperform traditional diversified ones in worst-case scenarios.
  - **[Inference]** Express the Tier-1 floor as a constraint on stressed states.
- **Ambiguity value of options.**
  - [Drechsler 2013](https://consensus.app/papers/details/71219fa7e399578680a3b58da1c70e3c/?utm_source=claude_desktop) finds investors pay "a large premium for index options because they hedge important model misspecification concerns".
  - **[Inference]** This supports the dossier's robust valuation (§3.4, item 5). The hedge's value must then show up in the robust layer, not in the nominal one.
- **λ includes opportunity value.**
  - [Jeanne & Sandri 2020](https://consensus.app/papers/details/f9b4a53e5a2659498fe09425a1534edb/?utm_source=claude_desktop): accumulate reserves "when global liquidity is high to buy back domestic assets at a discount when global financial conditions tighten".
  - [Kinlaw et al. 2013](https://consensus.app/papers/details/87606279740d57b4b0350e859446911b/?utm_source=claude_desktop) distinguish a liquidity "shadow asset" (used to raise utility, including by exploiting opportunities) from a "shadow liability" (used to stop utility falling).
  - [Bolton et al., *Market Timing, Investment, and Risk Management*](https://consensus.app/papers/details/e1bcae07d2be506289e7506e93615bb2/?utm_source=claude_desktop): with stochastic financing conditions, firms build precautionary cash. The marginal value of cash can then rise with financial slack.
  - **[Inference]** λ_t should include the Secondaries group's opportunity to buy in a crisis, and should depend on the financing state, not only on the current shortfall. Corporate Finance publishes it as the transfer-pricing curve.
- **Drawdown under a payout.**
  - [Angoshtari et al. 2015](https://consensus.app/papers/details/830207da0a945981bfed4cc78b27e992/?utm_source=claude_desktop) minimize the probability of drawdown for a portfolio with a payout, "as might be the case for an endowment fund paying at a specified rate".
  - **[Inference]** This is a candidate formulation for survival constraints with D_t.

### 4.6 Agent, IC and organizational design
- **Overlay-Design agent and sandbox** [22].
  - Keep a ledger of every trial.
  - Use a tool registry that is free of look-ahead by construction.
  - Earn lower evidential bars only for pre-registered hypotheses.
  - Use the Sharpe inference of [21] and the unified DSR variants of [López de Prado et al. 2026, *The Deflated Sharpe Ratio: A Unified Framework…*](https://consensus.app/papers/details/60fe2b8163ba516cb2ce633a20451d2e/?utm_source=claude_desktop) (DSR-L, DSR-LS, DSR-EO) for the gate.
- **Additions to the Overlay-Challenge agent's checklist:**
  - a provenance haircut and peer benchmark for dealer strategies [19][20];
  - sensitivity to the delta-hedging policy [12];
  - coverage of persistent drawdowns [9][13];
  - netting of the short-put exposure embedded in the hedge-fund book (Agarwal & Naik).
- **Meta-controller baselines.** Add a naive futures hedge (Cao et al. 2025) and a defensive-equity sleeve [10].
- **Rubric.**
  - When comparing candidate programs across seeds, test Sharpe differences robustly ([Ledoit & Wolf 2008](https://consensus.app/papers/details/86e0717f26b85e2daaaa5f62ba4fce77/?utm_source=claude_desktop)).
  - Report hedge metrics that respect cash-flow timing ([Chang et al. 2022](https://consensus.app/papers/details/e6e7a8ee39bd5e649658b16ce182c79e/?utm_source=claude_desktop)). They warn that compounded returns "can potentially paint an inaccurate picture" for levered payoffs.
- **IC artifacts.**
  - Add the four diagnostic axes to the defensive-stack frontier [13].
  - Show ambiguity value as a separate line in the "what we are paying for" decomposition (Drechsler 2013).
  - Report 5-year outcome deltas next to crash-window payoffs [9].
- **Treasurer seat (Corporate Finance, user-confirmed owner of VM/IM).** It owns:
  - the VM and IM stress [3][4];
  - IM procyclicality reporting [2];
  - collateral demand by venue [5];
  - the liquidation order ([Chaderina et al. 2026](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop));
  - the λ / transfer-pricing curve (Jeanne & Sandri; Kinlaw et al.).
  - **[Inference]** Charge the overlay E[λ × contingent collateral need] and credit it E[λ × hedge cash inflow]. This is consistent with context §1A.

---

## 5. Papers that challenge the dossier's recommendations

| Dossier recommendation (location) | Challenging evidence | What it implies **[Inference]** |
|---|---|---|
| Small convex sleeve of put spreads and VIX calls, 0.25–0.5% NAV a year (§1.4, §6.7) | [6]: the marginal value of derivatives hedging is "likely to be low"; liquidity justifies high cash. [8]: CRRA, loss-averse and disappointment-averse investors optimally *short* puts. [Chambers et al. 2014](https://consensus.app/papers/details/e0ede0d68e76538b9f874e92a2511824/?utm_source=claude_desktop): OTM put protection "may include a significant premium" (1987–2012). [9]: efficacy wanes at long horizons. | Keep the sleeve at the bottom of the range. It must beat an equal-cost cash buffer in the recourse LP on 5-year outcome deltas. Partial counterweights: [Broadie et al. 2009](https://consensus.app/papers/details/e3d219fd2bcf540cac60eca2e930f363/?utm_source=claude_desktop) find large put-writing returns "not even inconsistent with the Black-Scholes model", so measured premia are noisy; Drechsler (2013) explains option premia as hedges against ambiguity. |
| VIX calls as a cheap crash hedge (VXTH cost 0.09, §1.4 and §4.3) | [15]: a large negative VIX variance premium. [12]: outcomes are widely dispersed across VIX futures and VIX-call overlays, and hedges "make things worse" in some stresses. | Size the sleeve on ex-COVID costs. Keep it crash-specific and small. |
| Trend as the core of the defensive stack, with Sharpe templates rising to 0.6 in S3 (§1.4, §6.4C) | [16]: weak asset-by-asset evidence; the strategy is similar to one based on sample means. [Kim et al. 2016](https://consensus.app/papers/details/8c31356bd81e54b1b93d60aa866caee8/?utm_source=claude_desktop): Moskowitz–Ooi–Pedersen results are "largely driven by volatility-scaling". [17]: weak returns after crises. [Sullivan et al. 2025](https://consensus.app/papers/details/4d1944d19ba3544b9c6dddb23e13fb88/?utm_source=claude_desktop): managed-futures managers gave "comparatively poor portfolio mitigation" in drawdowns, relative to global macro. [Sepp et al. 2019](https://consensus.app/papers/details/efda7331d0275269a142f5178a17f683/?utm_source=claude_desktop): trend's diversification comes from "'crisis' beta, and not crisis 'alpha'". | Keep trend, as supported by Hurst et al. (verified), [10] and [11], and by [Asif et al. 2022](https://consensus.app/papers/details/7931e3a10e975129b3532b22aa625f26/?utm_source=claude_desktop) (CTAs cut crisis exposure "in less than 15 days"). But model it as a regime-dependent beta with post-crisis decay, and underwrite it on live manager data. |
| Vol scaling of the opportunistic book, citing Sharpe gains (§2.6, citing Moreira & Muir) | [18]; [Barroso & Detzel 2021](https://consensus.app/papers/details/9215ab0a4dd7570bba231fc4f29794f2/?utm_source=claude_desktop); [Liu, Tang & Zhou 2019](https://consensus.app/papers/details/f16f005a0b02501b8835341bc2d23c4e/?utm_source=claude_desktop): once look-ahead bias is corrected, maximum drawdowns are "68%–93%". | Justify scaling on tail control only. Partial counterweight: [DeMiguel et al. 2024](https://consensus.app/papers/details/b194457f3a945677a98e3f3fee82f2c1/?utm_source=claude_desktop) find a conditional multifactor version outperforms "even out-of-sample and net of costs". |
| Heavy deflation of opportunistic Sharpe ratios, with a DSR ≥ 0.95 gate (§1.6, C7) | [Jensen et al. 2021](https://consensus.app/papers/details/e70e9b4b51b35178b6e16cbf78086437/?utm_source=claude_desktop): most factors replicate and "work out-of-sample" across 93 countries. [Chen & Zimmermann 2022](https://consensus.app/papers/details/f9baa892c98f5787ac4e65797cb5fb4c/?utm_source=claude_desktop): publication-bias shrinkage is only "10 to 15 percent". [Harvey & Liu 2020](https://consensus.app/papers/details/ffbf7057f48e5d65b7507d5d9200ebe2/?utm_source=claude_desktop): current methods "lack power to detect outperforming managers". | Mixed. Heavy haircuts are right for dealer-marketed backtests [19][20]. Replicated academic premia warrant lighter shrinkage. Set the gate from explicit costs of Type I and Type II errors, and shrink hierarchically by strategy family rather than applying one threshold. |
| VRP as the signal that protection is cheap, and VRP predicting equity returns via Bollerslev–Tauchen–Zhou (§2.4) | [Heston et al. 2023](https://consensus.app/papers/details/db0fd9754cf65b46b571efc32881aee5/?utm_source=claude_desktop): the S&P 500 realized VRP was "not significantly different from zero" in 2006–2020, and implied variance "does not positively predict" futures returns for most assets. [Ogawa et al. 2020](https://consensus.app/papers/details/3d55aeb907475608865e5e28b00798a4/?utm_source=claude_desktop): the US VRP–return correlation is insignificant near the zero lower bound. [14]: the tail premium, not variance, drives the equity premium. | Do not use VRP as a return forecast. Time protection on the tail premium. Note that measuring VRP as VIX minus realized vol (the dossier's 4.1-point figure) differs from option-portfolio VRP returns. |
| Tier-2 objective P(5y ≥ 10%), with options shaping the distribution (§2.2, Browne) | [Capponi & Zhang 2024](https://consensus.app/papers/details/0fd71f5302ce52aead087822575e14e4/?utm_source=claude_desktop): risk-seeking when behind target. | Add governance against risk-taking when behind target (§4.5). |
| League table of cost per unit of crisis payoff, from index CAGRs (§4.3, IC artifact 2) | [Chang et al. 2022](https://consensus.app/papers/details/e6e7a8ee39bd5e649658b16ce182c79e/?utm_source=claude_desktop): compounded returns misstate levered payoffs, so the timing and size of cash flows must be included. [Broadie et al. 2009](https://consensus.app/papers/details/e3d219fd2bcf540cac60eca2e930f363/?utm_source=claude_desktop): judge option returns against returns generated by pricing models. | Report metrics that respect cash-flow timing and are benchmarked against models. This complements verifier finding R2 on hindsight windows and non-common samples. |
| Recommended stack has no defensive-equity sleeve (§1.4) | [10]; Harvey et al. (2019), verified, list quality among the most promising hedges. | Add quality and low-risk long/short as a candidate. |
| Collateral waterfall: cash → T-bills → USTs by maturity → … (§3.7) | [Chaderina et al. 2026](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop): the most liquid, widely held bonds fall most in fire sales. | Supports cash and T-bills first. Do not assume Treasuries sell at mid in S3; apply haircuts that depend on crowding. |

**Supportive evidence in the backfill.**
- [Bhansali 2008](https://consensus.app/papers/details/ff8fc074f7655456a49faf2be95fe727/?utm_source=claude_desktop): choose hedges "based on their cost and joint performance in periods of stress", with tail risk measured by macro scenario analysis. This matches the dossier's crisis-type approach.
- [Schwalbach et al. 2025](https://consensus.app/papers/details/4d700518172e5e54a940c1be3a357ecd/?utm_source=claude_desktop): trend and tail-hedge overlays are complementary within a portable-alpha framework.
- [Campasano 2024](https://consensus.app/papers/details/7441652e0fb55fc2b9a22ebaaa50ed4a/?utm_source=claude_desktop): a strategy conditioned on the VIX (buy puts when VIX is below average, write calls when above) outperformed over 2005–2022. This is weak support for state-conditioned purchases.

---

## 6. Verbatim usage message

No sign-up, upgrade or usage message appeared in any of the 33 Consensus results in this session, so there is nothing to copy.

---

## 7. Scope notes

**WebSearch confirmations (4 queries).**
- **Getmansky–Lo–Makarov:** JFE 74 (2004) 529–609, DOI 10.1016/j.jfineco.2004.04.001. Sources: [NBER w9571](https://www.nber.org/papers/w9571); [SUFE academic newsletter](https://academicnewsletter.sufe.edu.cn/info/357649); [Lo, MIT page](https://web.mit.edu/Alo/www/Papers/serialhf.html).
- **Koijen et al., *Carry*:** JFE 127(2), 197–225 (2018). Sources: [RePEc, Vrugt](https://ideas.repec.org/e/pvr15.html); [Moskowitz CV](https://som.yale.edu/sites/default/files/2025-06/CV_moskowitz_2025.pdf); [NBER w19325](https://www.nber.org/papers/w19325).
- **Bailey et al., PBO:** J. Computational Finance 20(4), 2017, DOI 10.21314/jcf.2016.322. Sources: [eScholarship](https://escholarship.org/content/qt4w1110bb/qt4w1110bb.pdf); [WMU ScholarWorks](https://scholarworks.wmich.edu/math_pubs/42); [SSRN 2326253](https://papers.ssrn.com/abstract=2326253).
- **Daniel & Moskowitz:** JFE 122(2), 221–247 (2016), DOI 10.1016/j.jfineco.2015.12.002. Sources: [NBER w20439](https://www.nber.org/papers/w20439); [SUFE academic newsletter](https://academicnewsletter.sufe.edu.cn/info/356387).

**Dossier works not checked here.**
- [nrv] works:
  - Demeterfi et al. (1999); Gatheral & Jacquier (2014); Rockafellar & Uryasev (2000); the books by Bhansali (2014) and Spitznagel (2021).
  - Kaminski & Lo (2014) is the most load-bearing remaining item, because it underpins the drawdown-stop design. Check it in a later pass.
- Sourced works confirmed by the verification log but not re-searched:
  - Harvey et al. (2018); Khandani & Lo (2011); Sepp & Lucic (2026); the Huang & Takáts (2020) BIS Bulletin.
  - Buehler et al. (2018) is cited as arXiv. A 2025 citing abstract refers to "Buehler et al.'s 2019 Deep Hedging paradigm" ([Ma 2025](https://consensus.app/papers/details/8f4a8bb1772b5d5184b170da912c36d6/?utm_source=claude_desktop)), which suggests a 2019 journal version. Not checked.

**Records returned without abstracts, so not annotated.**
- [Pintér (2023), *An Anatomy of the 2022 Gilt Market Crisis*](https://consensus.app/papers/details/1eaf0e7c6cb9564da3739bd8ae4fe0fe/?utm_source=claude_desktop) (SSRN, 29 citations).
- For the UK LDI case study, [Chen (2023), IMF WP, *Putting Out the NBFIRE*](https://consensus.app/papers/details/917a86050f945e1ab7f8422669477b43/?utm_source=claude_desktop) has an abstract and covers what amplified the turmoil and why the BoE intervention worked.

**Preprint and recency flags.**
- [13], [20] and [22] are 2026 arXiv preprints.
- [10] and [21] are 2026 journal articles with 0–2 citations.
- Use them for design ideas, not as settled evidence.

**Consensus queries (33, in order).**
1. *Seeds:* tail risk hedging portfolio · protective put strategy performance · variance risk premium · trend following crisis alpha · derivatives margin calls collateral liquidity · deflated Sharpe ratio backtest overfitting.
2. *Citation look-ups:* The Best of Strategies for the Worst of Times… · Still Not Cheap… · Ang Papanikolaou Westerfield… · Risk Management: Coordinating Corporate Investment and Financing Policies · Rampini Viswanathan collateral risk management… · Browne reaching goals by a deadline… · Jeanne Rancière optimal level of international reserves… · Expected Stock Returns and Variance Risk Premia · The Probability of Backtest Overfitting… · Harvey Liu Backtesting… · Lo The Statistics of Sharpe Ratios · Moskowitz Ooi Pedersen time series momentum · Koijen Moskowitz Pedersen Vrugt Carry · Daniel Moskowitz Momentum Crashes · Data-driven distributionally robust optimization using the Wasserstein metric… · Grossman Zhou optimal investment strategies for controlling drawdowns · Getmansky Lo Makarov… (authors) · An econometric model of serial correlation and illiquidity in hedge fund returns · Hardy regime-switching model of long-term stock returns….
3. *Refinements:* market liquidity and funding liquidity margin spiral · volatility-managed portfolios out-of-sample performance real-time implementation · why are index put options so expensive puzzle of index option returns · stock-bond correlation sign changes inflation monetary policy regimes · sovereign wealth fund oil price risk hedging optimal asset allocation fiscal withdrawals · 2022 UK gilt market crisis liability-driven investment pension funds collateral calls fire sales · Is there a replication crisis in finance factor premia Bayesian hierarchical out-of-sample · timing equity tail hedges option implied volatility skew signal cost of downside protection.
