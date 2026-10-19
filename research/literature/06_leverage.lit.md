# Stream 06 literature check: portfolio-level leverage with illiquid assets

**Dossier checked:** `research/dossiers/06_leverage.md` (570 lines, as of 2026-10-18).
- The reference list holds 32 academic entries: 33 works, counting the Gorton–Metrick *Haircuts* working paper cited alongside their JFE article.
- It also cites the Basel III LCR standard.

**Date:** 2026-10-18.

**Search engine:** Consensus. 34 searches, run one at a time with no filters:
- 20 targeted citation look-ups;
- 14 topical backfill searches: the 5 seed queries plus 9 refinements. The seed queries also confirmed 5 dossier citations.

Three WebSearches confirmed metadata that Consensus could not resolve (§7).

**Companion:** `research/verification/06_leverage.verify.md`.

**Organizational mapping (user, 2026-10-18).**
- Secondaries is a hybrid of direct and fund investments.
- Corporate Finance owns the treasury function. Per the context file, it also owns portfolio-level borrowing and leverage facilities, overlay collateral (VM/IM) and distribution payments.
- Design implications below are assigned on that basis: Corporate Finance runs the funding and liability side, and the seven investment groups run the asset side.

**Reading conventions**
- Findings come from the titles and abstracts that Consensus returned. Full texts were not read.
- **[Inference]** marks design reasoning that goes beyond what an abstract states.
- Author lists in bibliography entries are shown as Consensus displays them, with "et al." where Consensus truncates.
- In running text, a few well-known two- and three-author papers are named by their full surnames from bibliographic knowledge where Consensus truncated the list. Examples: Gilbert & Hrdlicka, He & Xiong, Brunnermeier & Yogo. The links point to the Consensus records.
- Years are Consensus record years. Where a record carries the online-first or working-paper year, the print year is noted.
- Numbers in §4.3 come from other investors and markets. They are plausibility anchors, not ADIC calibration.

---

## 1. Summary

### Citation integrity
- **Scope.** I checked 26 works:
  - the 25 most load-bearing of the 32 academic entries;
  - the *Haircuts* companion working paper.

  Of the remaining 7 entries:
  - 5 lower-weight methods references were already confirmed by the Stream 01 literature check. They are listed but were not re-searched.
  - 2 one-line references were not checked (§7).
- **Result:**
  - 25 found;
  - 0 mismatched;
  - 1 not in Consensus (*Haircuts*), but WebSearch confirms it exists.

  **No hallucinated or garbled references.** This agrees with the verification log, which checked 18 references and found all correct.
- **Every claim that could be checked against an abstract matched.** Examples:
  - Ang et al.'s "2% of wealth";
  - Sorensen et al.'s "LPs may just break even";
  - both Frazzini–Pedersen quotes;
  - Grossman–Zhou's surplus rule;
  - the reciprocal-gamma result that the dossier attributes to Milevsky & Robinson.
- **Minor fixes:**
  - **Brown, Dimmock, Kang & Weisbenner (2014).** The full title ends ": Evidence and Implications". The dossier links NBER w15861, but that is the precursor working paper, titled "Why I Lost My Secretary: The Effect of Endowment Shocks on University Operations". Cite DOI 10.1257/aer.104.3.931 instead.
  - **Kelly (1956).** The *Bell System Technical Journal* 35:917–926 citation is confirmed by a citing abstract. Consensus indexes the *IRE Transactions on Information Theory* printing. The verification log's attribution caveat still stands: the continuous-time growth formula is not in Kelly (1956).
  - **DOIs and published versions to add (from WebSearch):**
    - Getmansky–Lo–Makarov: 10.1016/j.jfineco.2004.04.001.
    - Stafford: 10.1093/rfs/hhab020. This comes from a search excerpt; volume and pages remain unconfirmed.
    - Gorton–Metrick *Haircuts*: published in FRB St. Louis *Review* 92(6), 2010, pp. 507–520.
  - **MacLean, Thorp & Ziemba (2011).** Add the subtitle "Theory and Practice" and DOI 10.1142/7598.
  - **Indirect confirmation only.** Issue and page details are partly unconfirmed for these three:
    - Merton (1971), via a 1975 reprint and citing abstracts;
    - Barro (1979), via a citing abstract;
    - Geanakoplos (2010), via the volume editorial.

### Backfill (14 topical searches)
The dossier's theory core is sound, but it misses ten clusters that bear directly on ADIC's leverage design:
1. **Commitment risk as leverage.**
   - Unfunded commitments carry a large welfare cost and behave like hidden leverage.
   - Fund-level subscription lines defer calls and inflate IRRs.
2. **PE's funding-liquidity beta.** PE returns load on the same liquidity factor as public equity, through a funding-liquidity channel. That is wrong-way risk for any leverage secured on, or repaid from, PE.
3. **Margin-call liquidity risk at non-banks.**
   - Dutch pension funds' swap margin calls can exceed 6% of assets.
   - "LASH" risk: hedges that drain liquidity when solvency *improves*.
   - The 2022 gilt episode is the stress case.
4. **Repo and futures funding microstructure.**
   - Haircut spikes were segment-specific: bilateral repo, not tri-party.
   - The futures–cash basis is a measurable gauge of leverage demand.
5. **Secondary-market liquidity provision.** Discounts move with the supply of liquidity, and volume collapsed in early 2009.
6. **Rollover risk and maturity structure.**
   - rollover losses (He & Xiong);
   - the "maturity rat race";
   - Brunnermeier & Yogo's effective-maturity objective;
   - maturity dispersion.
7. **Frictions and dynamic-leverage costs.**
   - risk-parity critiques;
   - the covariance drag of dynamic leverage;
   - market impact on levered sizing.
8. **Soft drawdown control.**
   - drawdown-scaled risk aversion inside MPC;
   - Kelly growth with convex shortfall penalties under regimes.
9. **Endowment payout constraints and borrowing.** A binding payout constraint destroys the endowment's buffer-stock role.
10. **Funds transfer pricing (FTP).** Internal pricing with contingency-buffer and term-liquidity charges. This is directly usable by Corporate Finance as ADIC's internal bank.

### Challenges
Several papers qualify the dossier's recommendations (§5):
- The BAB and levered-risk-parity evidence behind "lever low-volatility exposures" is contested.
- Vintage diversification does not remove commitment risk.
- The endowment "hoarding" asymmetry is not found in every sample.
- Secondary-market capacity can collapse in stress.
- A hard drawdown barrier has known feasibility and cost problems.
- Selling the most liquid assets first can backfire when they are crowded.
- Ex-post bridge borrowing cannot remove all the cost of illiquidity.

None of these overturns the dossier's central conclusions:
- leverage is mainly a liquidity and implementation tool;
- "lever the liquid, not the illiquid";
- leverage limits belong in Tier 1.

Several change defaults, add state variables or add rubric checks (§4).

---

## 2. Citation-integrity table

Status values: found, mismatched or not found. Differences between online-first and print years are not counted as mismatches.

| Dossier citation | Status | Corrected / confirmed metadata (Consensus unless stated) | Consensus URL |
|---|---|---|---|
| Ang, Papanikolaou & Westerfield (2014), *Portfolio Choice with Illiquid Assets*, MS 60(11) | found | DOI 10.1287/mnsc.2014.1986; 171 citations. The abstract confirms state-dependent risk aversion and "willing to forgo 2% of their wealth" against once-a-decade illiquidity crises. | [link](https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop) |
| Asness, Frazzini & Pedersen (2012), *Leverage Aversion and Risk Parity*, FAJ 68(1) | found | DOI 10.2469/faj.v68.n1.1; 314 citations. The abstract reports risk parity at market risk beating the market by about 4% a year over 1926–2010. An editor's note discloses the authors' AQR affiliation. | [link](https://consensus.app/papers/details/3544dc48133655e39cf2c08067e8b2da/?utm_source=claude_desktop) |
| Brunnermeier & Pedersen (2009), *Market Liquidity and Funding Liquidity*, RFS 22(6) | found | DOI 10.1093/rfs/hhn098; 5,153 citations | [link](https://consensus.app/papers/details/7c944d8f27a65feea50c7b83eea8e1e3/?utm_source=claude_desktop) |
| Brown, Dimmock, Kang & Weisbenner (2014), *How University Endowments Respond to Financial Market Shocks*, AER 104(3); dossier links NBER w15861 | found (minor fix) | Full title: "…Shocks: Evidence and Implications"; DOI **10.1257/aer.104.3.931**; 119 citations. NBER w15861 is the precursor WP, titled *Why I Lost My Secretary: The Effect of Endowment Shocks on University Operations* (2010) ([record](https://consensus.app/papers/details/d68ad94aa01e5f5a8ab704fb7d1d65e5/?utm_source=claude_desktop)). Cite the AER DOI instead of w15861. | [link](https://consensus.app/papers/details/7831f601f303581cb3e87906847e0fab/?utm_source=claude_desktop) |
| Dimmock, Wang & Yang (2024), *The Endowment Model and Modern Portfolio Theory*, MS 70(3) | found | Record year 2019, with NBER DOI 10.3386/w25559 and venue *Manag. Sci.* The abstract cites the MS supplement DOI 10.1287/mnsc.2023.4759. | [link](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop) |
| Frazzini & Pedersen (2014), *Betting Against Beta*, JFE 111(1) | found | Record year 2012 (online); DOI 10.1016/j.jfineco.2013.10.005; 1,930 citations. Both quoted phrases appear in the abstract. | [link](https://consensus.app/papers/details/cda6065026d75504aaae76aa498f4391/?utm_source=claude_desktop) |
| Gorton & Metrick (2012), *Securitized Banking and the Run on Repo*, JFE 104(3) | found | Record year 2011 (online); DOI 10.1016/j.jfineco.2011.03.016; 1,687 citations; venue label "Unknown Journal". JFE 104:425–451 (2012) per a citing abstract ([Du 2020](https://consensus.app/papers/details/282ba3b3293f5133a241dafe456ea26b/?utm_source=claude_desktop)). | [link](https://consensus.app/papers/details/1731101d29a15c0da2c78761804fb43d/?utm_source=claude_desktop) |
| Gorton & Metrick, *Haircuts*, NBER WP 15273 (cited with the entry above) | not found (in Consensus); exists per WebSearch | No Consensus record. WebSearch: NBER WP 15273 (2009); published in FRB St. Louis *Review* 92(6), Nov/Dec 2010, pp. 507–520. Sources in §7. | — |
| Grossman & Zhou (1993), *Optimal Investment Strategies for Controlling Drawdowns*, Math. Finance 3(3) | found | DOI 10.1111/j.1467-9965.1993.tb00044.x; 385 citations. The abstract confirms risky investment in proportion to the surplus W − αM. | [link](https://consensus.app/papers/details/5e80ded6b6c8585aa0607d96ebbfa9ae/?utm_source=claude_desktop) |
| Kelly (1956), *A New Interpretation of Information Rate*, BSTJ 35(4): 917–926 | found | Consensus indexes the *IRE Trans. Inf. Theory* printing (DOI 10.1109/tit.1956.1056803; 2,009 citations). BSTJ 35:917–926 is confirmed by a citing abstract ([Ziemba & MacLean 2011](https://consensus.app/papers/details/3b45433656a157f7a64492d1f6adaf05/?utm_source=claude_desktop)). Attribution caveat as in the verification log. | [link](https://consensus.app/papers/details/bed81db3476d56b78bd5caa19f281dc5/?utm_source=claude_desktop) |
| Sorensen, Wang & Yang (2014), *Valuing Private Equity*, RFS 27(7) | found | Record year 2013; DOI 10.1093/rfs/hhu013; 110 citations. The abstract confirms "LPs may just break even" and adds "Debt is cheap and reduces these costs". | [link](https://consensus.app/papers/details/15cb135a45b35616b82e97bf090f24ae/?utm_source=claude_desktop) |
| Agarwal, Driscoll & Laibson (2013), *Optimal Mortgage Refinancing: A Closed-Form Solution*, JMCB 45 | found | DOI 10.1111/jmcb.12017; 159 citations. The abstract gives the Lambert-W rule in ρ, λ, σ, κ/M and τ. | [link](https://consensus.app/papers/details/c7c1dc14b2d4554dbae95a5574401f89/?utm_source=claude_desktop) |
| Merton (1971), *Optimum Consumption and Portfolio Rules in a Continuous-Time Model*, JET 3(4): 373–413 | found (reprint record) | Consensus holds a 1975 reprint (DOI 10.1016/b978-0-12-780850-5.50052-6; 3,601 citations). JET 3, 373–413 (1971) is confirmed by citing abstracts ([Sethi & Taksar 1988](https://consensus.app/papers/details/2ff36b799814592c95ef2d74fdb31219/?utm_source=claude_desktop); [Marín-Solano & Navas 2009](https://consensus.app/papers/details/c3c6abf61e015a4092afb808ae779c82/?utm_source=claude_desktop)). Issue number not confirmed. | [link](https://consensus.app/papers/details/0105883e335c5158ae5fbebb7c83fae3/?utm_source=claude_desktop) |
| MacLean, Thorp & Ziemba (eds.) (2011), *The Kelly Capital Growth Investment Criterion*, World Scientific | found | Full title adds ": Theory and Practice"; DOI 10.1142/7598; 260 citations | [link](https://consensus.app/papers/details/f4c7cf206e6a5802b1f8c86b2dd62137/?utm_source=claude_desktop) |
| Dufresne (1990), *The distribution of a perpetuity, with applications to risk theory and pension funding*, Scand. Actuarial J.: 39–79 | found | DOI 10.1080/03461238.1990.10413872; 417 citations. Pages not shown. | [link](https://consensus.app/papers/details/1944cda3fada5becbac811f550f64c82/?utm_source=claude_desktop) |
| Milevsky & Robinson (2000), *Self-annuitization and ruin in retirement*, NAAJ 4(4) | found | DOI 10.1080/10920277.2000.10595940; 138 citations. The abstract states that, for the eventual ruin probability, the stochastic present value of consumption "is known to be a reciprocal gamma distribution". | [link](https://consensus.app/papers/details/bfd6e5b8066455a0aeb4c13ab7f514bf/?utm_source=claude_desktop) |
| Barro (1979), *On the Determination of the Public Debt*, JPE 87(5): 940–971 | found (citing abstract) | No direct record. A Consensus-indexed abstract (Jiang et al., PNAS 2024) cites "J. Polit. Econ. 87, 940-971 (1979)". Issue number not confirmed. | [citing record](https://consensus.app/papers/details/7831475fa65c51cf9bcee3f9b69387fc/?utm_source=claude_desktop) |
| Geanakoplos (2010), *The Leverage Cycle*, NBER Macroeconomics Annual 2009, 24: 1–65 | found (volume record) | No direct record. The *NBER Macroeconomics Annual* editorial (Acemoğlu et al. 2010, DOI 10.1086/648284) names "The Leverage Cycle" by Geanakoplos as the first paper of the 24th edition. A discussion record also exists ([Shin 2009](https://consensus.app/papers/details/b2022a40206c59c49db520d1456f6f5e/?utm_source=claude_desktop)). Pages not confirmed. | [link](https://consensus.app/papers/details/84682672dd27505689e8054451631fa4/?utm_source=claude_desktop) |
| Adrian & Shin (2010), *Liquidity and Leverage*, JFI 19(3) | found | Venue *J. Financial Intermediation*; the record carries SSRN DOI 10.2139/ssrn.1139857; 2,456 citations. Volume and pages not shown. | [link](https://consensus.app/papers/details/3e7e2832b412506996f30f112de8fa80/?utm_source=claude_desktop) |
| Gârleanu & Pedersen (2011), *Margin-Based Asset Pricing and Deviations from the Law of One Price*, RFS 24(6) | found | DOI 10.1093/rfs/hhr027 (venue label shows NBER); 663 citations | [link](https://consensus.app/papers/details/c5d81d132abf5d118a3a62c20200c195/?utm_source=claude_desktop) |
| Shleifer & Vishny (2011), *Fire Sales in Finance and Macroeconomics*, JEP 25(1) | found | DOI 10.1257/jep.25.1.29; 700 citations | [link](https://consensus.app/papers/details/38094184238d5f8f9fe8944a05e37411/?utm_source=claude_desktop) |
| Stafford (2022), *Replicating Private Equity with Value Investing, Homemade Leverage, and Hold-to-Maturity Accounting*, RFS 35(1): 299–342 | found | Record year 2015; venue RFS; SSRN DOI 10.2139/ssrn.2720479; 36 citations. A WebSearch excerpt gives RFS 2022 and DOI 10.1093/rfs/hhab020. Volume and pages not confirmed. | [link](https://consensus.app/papers/details/b981a74e3c6259a7b94f9c86f41ce6bc/?utm_source=claude_desktop) |
| Takahashi & Alexander (2002), *Illiquid Alternative Asset Fund Modeling*, JPM 28(2) | found | DOI 10.3905/jpm.2002.319836 (*Journal of Portfolio Management*; venue label "Unknown Journal"); 68 citations | [link](https://consensus.app/papers/details/da7ee2d8587e575f99e3a36a590d2be6/?utm_source=claude_desktop) |
| Getmansky, Lo & Makarov (2004), *An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns*, JFE 74(3): 529–609 | found (working-paper records) | No JFE record in Consensus. Consensus returned thesis versions (Getmansky 2004 and [Makarov 2006](https://consensus.app/papers/details/ea8aa97099675752b481ce72e12ee5a0/?utm_source=claude_desktop)) and a citing abstract ([Di Cesare et al. 2015](https://consensus.app/papers/details/813ea087fa875f2a993953c2b1ac93ea/?utm_source=claude_desktop)). WebSearch: JFE 74 (2004) 529–609, DOI 10.1016/j.jfineco.2004.04.001. | [link](https://consensus.app/papers/details/4e43d079332f5046860f2f39350f56f9/?utm_source=claude_desktop) |
| Calafiore & Campi (2006), *The scenario approach to robust control design*, IEEE TAC 51(5) | found | DOI 10.1109/tac.2006.875041; 1,293 citations. The abstract confirms an explicit sample-size bound. | [link](https://consensus.app/papers/details/6d4c42eea34d5c029d37a6e6102f72fa/?utm_source=claude_desktop) |
| Ames et al. (2017), *Control Barrier Function Based Quadratic Programs for Safety Critical Systems*, IEEE TAC 62(8) | found | Record year 2016 (online); DOI 10.1109/tac.2016.2638961; 3,014 citations | [link](https://consensus.app/papers/details/ec2102e7248f5f40b65bd94d78ff60ea/?utm_source=claude_desktop) |
| Boyd et al. (2017), *Multi-Period Trading via Convex Optimization* | not re-searched (found in Stream 01 check) | FnT Optim., DOI 10.1561/2400000023 (Stream 01 record) | [link](https://consensus.app/papers/details/86cb196ea5dc58bba999226d0954af0c/?utm_source=claude_desktop) |
| Rockafellar & Uryasev (2000), *Optimization of Conditional Value-at-Risk*, J. Risk 2(3) | not re-searched (found in Stream 01 check) | DOI 10.21314/jor.2000.038. Stream 01 notes the record carries an unrelated abstract. | [link](https://consensus.app/papers/details/a500ccf654ae5205a70fe138eb0d82d7/?utm_source=claude_desktop) |
| Cariño et al. (1994), *The Russell–Yasuda Kasai Model*, Interfaces 24(1) | not re-searched (found in Stream 01 check) | DOI 10.1287/inte.24.1.29 | [link](https://consensus.app/papers/details/1f457f819115540d83c7b7d4289b0b66/?utm_source=claude_desktop) |
| Pereira & Pinto (1991), Math. Prog. 52 | not re-searched (found in Stream 01 check) | DOI 10.1007/bf01582895 | [link](https://consensus.app/papers/details/fb85e1a196295794a2ba53f5aef51db2/?utm_source=claude_desktop) |
| Ben-Tal, Goryashko, Guslitzer & Nemirovski (2004), Math. Prog. 99 | not re-searched (found in Stream 01 check) | DOI 10.1007/s10107-003-0454-y | [link](https://consensus.app/papers/details/ce4bf774291b55cabf5e91b522ffb2c8/?utm_source=claude_desktop) |
| Mayne, Seron & Raković (2005), Automatica 41(2) | not checked | One [K] mention (tube MPC); low design weight | — |
| Dowson & Kapelevich (2021), *SDDP.jl*, IJOC 33(1) | not checked | Software citation | — |

---

## 3. Annotated bibliography (25 papers)

None of the 25 is cited by the dossier. Entries are grouped by the design question they inform.

### A. Should ADIC lever, and how much?

**1. [Will My Risk Parity Strategy Outperform?](https://consensus.app/papers/details/efc234a01031512da8540369cc25e099/?utm_source=claude_desktop)**
- R. M. Anderson et al. · 2012 · *Financial Analysts Journal* · 122 citations · DOI 10.2469/faj.v68.n6.7
- *Finding:*
  - Over 1926–2010, transaction costs can reverse strategy rankings, "especially if leverage is used".
  - After market frictions, risk parity levered to market volatility underperformed the market on both return and risk-adjusted return. For this simple strategy, "market frictions fully explain the anomaly".
  - Backtest start and end dates materially change the results.
- *Relevance to ADIC:* This directly qualifies the dossier's use of Asness et al. (2012) to justify levering low-volatility exposures (§2.3).
  - **[Inference]** ADIC's AA funding is cheaper than the frictions assumed here, so the conclusion may not transfer in full.
  - Even so, every levered sleeve should be justified by a frictions-included, net-of-funding α* for its own period, not by the factor literature.

**2. [Determinants of Levered Portfolio Performance](https://consensus.app/papers/details/8a242fcc6d1d5d5bb393e76ffce91e3a/?utm_source=claude_desktop)**
- R. M. Anderson et al. · 2014 · *Financial Analysts Journal* · 25 citations · DOI 10.2469/faj.v70.n5.6
- *Finding:* The cumulative return of a levered strategy decomposes into five elements. Over 1929–2013, for volatility-targeting strategies:
  - The covariance between leverage and the source portfolio's excess return, a previously undocumented element, cut annualized arithmetic return by 0.64–4.23%.
  - Leverage-induced turnover cost 0.27–2.59%.
  - Variance drag cost 0.41–2.84% of geometric return.
- *Relevance:* **[Inference]** Any rule that changes leverage with the state is a dynamic levered strategy. In the dossier that includes:
  - the drawdown barrier (constraint 10);
  - the Kelly cap (constraint 9);
  - regime-dependent overlay sizing.

  Score each with this decomposition. The covariance term is invisible in one-period analysis. It also separates financing cost, covariance drag, turnover and variance drag cleanly, which avoids the double counting flagged in verifier R6.

**3. [Betting against betting against beta](https://consensus.app/papers/details/17755f59391c5311b233e577e07dd1ef/?utm_source=claude_desktop)**
- Robert Novy-Marx et al. · 2018 (record year) · *Journal of Financial Economics* · 73 citations · DOI 10.2139/ssrn.3300965 (SSRN)
- *Finding:*
  - BAB's performance is driven by non-standard construction that effectively equal-weights stock returns. On average it commits $1.05 per dollar invested to stocks in the bottom 1% by market capitalization.
  - It earns positive returns after costs, but through profitability and investment tilts that are fairly compensated.
  - "Predictable biases" from its beta estimation drive results presented as support for the theory.
- *Relevance:* This weakens the empirical pillar of dossier §2.3. **[Inference]** The case for levering defensive or low-beta sleeves should rest on ADIC's own net-of-cost α*, not on the BAB factor.

**4. [Optimal Leveraged Portfolio Selection Under Quasi-Elastic Market Impact](https://consensus.app/papers/details/626d6c94bb4f5c1c912d5ce4d1ee0ef3/?utm_source=claude_desktop)**
- Chanaka Edirisinghe et al. · 2023 · *Operations Research* · 5 citations · DOI 10.1287/opre.2023.2462
- *Finding:*
  - With both temporary and permanent price impact, levering to reach a higher return target significantly erodes risk-adjusted returns, even in relatively liquid ETFs.
  - The losses steepen as the target, and with it the leverage, rises.
  - Leverage-constrained, less risk-averse investors who ignore liquidity costs ex ante lose most.
- *Relevance:* This is formal support for two positions:
  - the dossier's conclusion that gearing the whole book is not a route to 10%;
  - the deck's guard against target-chasing.

  **[Inference]** Add impact terms to synthetic-exposure sizing and to forced-deleveraging paths. A companion paper, [Edirisinghe et al., EJOR 2021](https://consensus.app/papers/details/0ab4f389888e5acaa873cf35e741dad1/?utm_source=claude_desktop), optimizes deleveraging under market impact and margin restrictions.

**5. [Liquidation Values and Debt Capacity: A Market Equilibrium Approach](https://consensus.app/papers/details/fa39990f63685ac6a7cbf5f932b9e7c2/?utm_source=claude_desktop)**
- A. Shleifer et al. · 1992 · *Journal of Finance* · 2,926 citations · DOI 10.1111/j.1540-6261.1992.tb04661.x
- *Finding:*
  - A distressed seller's natural buyers, its industry peers, are usually in trouble at the same time, so assets sell below value in best use.
  - This illiquidity "makes assets cheap in bad times, and so ex ante is a significant private cost of leverage".
  - Debt capacity therefore varies with asset liquidity across industries and over the cycle.
- *Relevance:* This is the seminal basis for tying debt capacity to how liquid assets are *in stress*. **[Inference]**
  - ADIC's natural buyers of LP interests are other pensions and SWFs, which supplied 48% of LP secondary volume (Jefferies, per the dossier).
  - Those buyers face the same DPI drought.
  - Leverage secured on, or repaid from, private assets should therefore be sized on stress-state liquidation values.

### B. Illiquid assets, commitments and look-through leverage

**6. [Capital Commitment](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop)**
- Elise Gourier et al. · 2024 · *SSRN Electronic Journal* (record) · 8 citations · DOI 10.2139/ssrn.2490430
- Earlier version: [Capital Commitment and Illiquidity Risks in Private Equity](https://consensus.app/papers/details/9b5881d8cef05dffa4a40423d6b15bc8/?utm_source=claude_desktop), Ludovic Phalippou et al., 2014, 1 citation.
- *Finding (2024):*
  - In a dynamic allocation model, ex-ante commitment has large effects on portfolios and welfare.
  - Investors would pay a larger premium to adjust the *quantity committed* than to remove timing uncertainty or limited tradability.
  - Commitment-risk premiums *increase* with secondary-market liquidity and do not disappear when investments are spread over many funds.
- *Finding (2014 version):*
  - Holding many funds diversifies liquidity events but creates a "costly funding mismatch".
  - In the limit, the welfare premium is equivalent to 1.63% a year of return.
- *Relevance:* The dossier's leverage definitions omit ADIC's unfunded commitments (≈US$38bn, working assumption), a fixed-claim-like liability. Verifier R5 flags the same gap.
  - **[Inference]** Count commitments in leverage (§4.1).
  - **[Inference]** Evaluate LEVER jointly with commitment pacing C_t.

**7. [Private Equity Performance and Liquidity Risk](https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop)**
- Francesco Franzoni et al. · 2012 · *Journal of Finance* · 251 citations · DOI 10.1111/j.1540-6261.2012.01788.x
- *Finding:*
  - PE has significant exposure to the same liquidity risk factor as public equity and other alternatives.
  - The unconditional liquidity risk premium is about 3% a year. In a four-factor model, including it reduces alpha to zero.
  - The link to market liquidity runs through a funding-liquidity channel.
- *Relevance:* **[Inference]** Four things worsen in the same funding-liquidity state:
  - PE marks;
  - secondary bids;
  - NAV-facility LTVs;
  - ADIC's own refinancing terms.

  Model that wrong-way risk with one shared factor, not as independent stresses.

**8. [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop)**
- Vincent Maurin et al. · 2022 (record; MS) · *Management Science* · 8 citations · DOI 10.1287/mnsc.2022.4612
- *Finding:*
  - Sequential capital calls are an optimal answer to GP moral hazard, but they expose LPs to illiquidity risk.
  - Funds with more illiquidity-tolerant LPs earn higher returns.
  - GPs "may inefficiently accelerate drawdowns to avoid default by LPs".
  - A secondary market narrows fund-level return differences but not LP-level ones.
- *Relevance:* This puts a return on illiquidity tolerance. **[Inference]**
  - An LP that can always meet calls earns more. ADIC's reserve and committed facilities therefore have return value beyond avoiding forced sales, which supports the dossier's dry-powder reading.
  - Watch for call acceleration in stress.

**9. [Hidden in Plain Sight—The Impact of Undrawn Commitments](https://consensus.app/papers/details/d99e5eff8f48558898b24269df59ba18/?utm_source=claude_desktop)**
- T. Meyer · 2020 · *Journal of Alternative Investments* (DOI 10.3905/jai.2020.1.101; venue label "Unknown Journal") · 2 citations
- *Finding:*
  - Uncalled capital carries significant risk and opportunity cost.
  - Markets price it, for example through larger secondary discounts and through subscription lines that use it as collateral.
  - Some audit conventions treat undrawn commitments as hidden leverage.
  - The author proposes treating a fund as one instrument, with the LP's uncalled capital as a loan against it.
- *Relevance:* This is a direct modelling device for a commitment-adjusted leverage metric (§4.1). It closes the gap that verifier R5 found in the dossier's LCR and NSFR analogs.

**10. [Distorting Private Equity Performance: The Rise of Fund Debt](https://consensus.app/papers/details/84b7e9e9b66151e78637a4ebfac077ae/?utm_source=claude_desktop)**
- James F. Albertus et al. · 2020 · *SSRN Electronic Journal* · 4 citations · DOI 10.2139/ssrn.3410076
- *Finding:*
  - Buyout funds that use subscription lines of credit call less capital.
  - Their performance measures that are sensitive to cash-flow timing are substantially distorted.
  - Subscription lines are more common among poorly performing funds, and they raise carried interest.
- *Relevance:* Fund debt is look-through leverage that ADIC does not control (dossier §2.1). It also biases the "current actual return" input to the return-fusion stream.
  - **[Inference]** Adjust IRRs for subscription-line use.
  - **[Inference]** Model subscription-line repayment as a deferred call surge in stress.
  - Related: [Brown et al. 2024](https://consensus.app/papers/details/911bba796e2a56e5924f1563664ff4b4/?utm_source=claude_desktop) find that interim IRRs are strongly affected by subscription lines and deployment pacing.

**11. [Nowcasting Net Asset Values: The Case of Private Equity](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop)**
- Gregory W. Brown et al. · 2020 · *SSRN Electronic Journal* · 20 citations · DOI 10.2139/ssrn.3507873
- *Finding:*
  - Weekly unsmoothed NAV estimates for individual funds beat extrapolations of reported NAVs.
  - Average buyout fund: market beta about 1.0, total risk 33% a year.
  - Average venture fund: market beta 1.4, total risk 40%.
- *Relevance:* NAV-facility LTVs are often set on pools of a few funds. **[Inference]**
  - Fund-level volatility is far above the dossier's 15% portfolio-level private volatility. LTV-breach chance constraints (constraint 7) must therefore be stressed on nowcast NAVs.
  - Covenant triggers are still tested on reported NAV with its lags, as the dossier already says.

**12. [Valuing Private Equity Investments Strip by Strip](https://consensus.app/papers/details/a07fbcfb0fdd5d5891ce4d67340cbeb8/?utm_source=claude_desktop)**
- Arpit Gupta et al. · 2021 · *Journal of Finance* · 24 citations · DOI 10.1111/jofi.13073
- *Finding:*
  - The method replicates PE cash flows with listed strips and values them with a rich factor model.
  - Under that model, the average fund in most PE categories has negative risk-adjusted profit.
  - Cross-sectional variation and persistence are substantial.
  - Expected returns decline in the later part of the sample.
- *Relevance:* This supports the dossier's asset-level LEVER test (§6.8(b)), which rejects return-seeking leverage on a buyout fund interest. **[Inference]** The default α* for PE in the LEVER test should be close to zero unless fund-specific evidence says otherwise.

### C. The SELL comparator in stress

**13. [The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop)**
- Taylor D. Nadauld et al. · 2019 · *Journal of Financial Economics* · 66 citations · DOI 10.1016/j.jfineco.2018.11.007
- *Finding:*
  - Most secondary transactions occur at a discount to NAV.
  - Buyers average an annualized public market equivalent (PME) of 1.023, against 0.976 for sellers. Buyers outperform by about 5 percentage points a year, market-adjusted.
  - Flexible buyers earn this by supplying liquidity.
- *Relevance:* This is an empirical anchor for two numbers:
  - the implied cost of SELL in dossier §6.9C, which is about 5% a year for buyout at 3% growth;
  - the return on Secondaries-group dry powder.

  **[Inference]** ADIC earns this gap when it buys and pays it when it sells.

**14. [Liquidity Provision in the Secondary Market for Private Equity Fund Stakes](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop)**
- R. Albuquerque et al. · 2018 · SSRN (DOI 10.2139/ssrn.3182481) · 11 citations
- *Finding:* Using a broker's proprietary bid data:
  - The demand response to aggregate liquidity shocks is negatively related to contemporaneous bids.
  - The effect is stronger for funds likely to be sold in times of low liquidity.
  - The response is unrelated to future NAV-to-NAV returns.

  So variation in discounts reflects liquidity provision, not fundamentals.
- *Relevance:* This supports a discount function d_i(s_t) driven by a liquidity-supply state, not only by the regime label.

**15. [The Private Equity Secondaries Market During the Financial Crisis and the "Valuation Gap"](https://consensus.app/papers/details/e2a6180114bb5e16be2ab5d849fa5cbf/?utm_source=claude_desktop)**
- U. Hege et al. · 2011 · *Journal of Private Equity* · 5 citations · DOI 10.3905/jpe.2011.14.3.042
- *Finding:*
  - Secondary-market liquidity "contracted severely in early 2009 to only a fraction of earlier volume", then recovered quickly.
  - The authors explain the buyer–seller valuation gap with framing and loss aversion.
- *Relevance:* This qualifies the dossier's statement that the market "can absorb ADIC-sized sales" (§4.3). That statement rests on H1 2026 data. **[Inference]** Add a per-quarter stress-capacity limit on SELL.

### D. Funding liquidity, margins and repo (overlay and Corporate Finance)

**16. [Pension Liquidity Risk](https://consensus.app/papers/details/65e862e24881598a97200e1611a991ed/?utm_source=claude_desktop)**
- Kristy A. E. Jansen et al. · 2026 · *Review of Financial Studies* · 0 citations · DOI 10.1093/rfs/hhag068
- An SSRN version also exists ([2023 record](https://consensus.app/papers/details/1316f05b545455a5a9a3bd6d9add99c4/?utm_source=claude_desktop)).
- *Finding:*
  - Dutch pension funds with worse funding ratios use interest-rate swaps more aggressively.
  - Margin calls when rates rise "can exceed 6% of their total assets".
  - Funds meet realized calls by procyclically selling medium-term government bonds, which depresses the prices of the bonds they sell.
- *Relevance:* This is a recent top-journal calibration point for a rates overlay's collateral need. **[Inference]** It backs verifier R11:
  - recalibrate the BoE 250 bp buffer by instrument;
  - include the price impact of the HQLA that ADIC itself would sell.

**17. [LASH risk and Interest Rates](https://consensus.app/papers/details/d194a64624745726be3cb46d2cb00e74/?utm_source=claude_desktop)**
- Laura Alfaro et al. · 2024 · SSRN (NBER DOI 10.3386/w33241) · 6 citations
- *Finding:*
  - Institutions take "liquidity after solvency hedging" (LASH) risk when their hedges need liquidity as their solvency improves.
  - In UK repo and swap data for 2019–22, at peak LASH a 100 bp rate rise would have required liquidity close to the cash holdings of the pension and insurance sector.
  - Pre-crisis LASH predicted bond sales in the 2022 crisis.
- *Relevance:* **[Inference]** Two ADIC exposures fit this pattern:
  - The tail hedge pays in stress but drains collateral as markets recover, which is exactly when ADIC's solvency improves.
  - Any receive-fixed duration overlay drains collateral when rates rise.

  Overlay liquidity therefore needs testing in both tails, not only at P99 stress margin.

**18. [Sizing Up Repo](https://consensus.app/papers/details/22caff417161575d85e2ef9c58fabe56/?utm_source=claude_desktop)**
- A. Krishnamurthy et al. · 2014 · *Journal of Finance* · 443 citations · DOI 10.1111/jofi.12168
- *Finding:*
  - Most repo extended by money market funds (MMFs) and securities lenders was backed by Treasury or agency collateral.
  - Repo against private collateral contracted in the crisis, but the contraction was small next to the ABCP contraction.
  - Haircuts on MMF-to-dealer repo rose less than those reported for dealer-to-dealer and dealer-to-hedge-fund repo. The authors read this as a credit crunch among dealers.
- *Companion paper:* [Repo runs: Evidence from the tri-party repo market](https://consensus.app/papers/details/b4498a6023e95908834404ffd98876ab/?utm_source=claude_desktop) (Adam M. Copeland et al., 2012, 273 citations). Tri-party haircuts and funding were "surprisingly stable", Lehman aside, unlike bilateral haircuts.
- *Relevance:* The Gorton–Metrick "run on repo", which the dossier uses for its stress parameters, was segment-specific. **[Inference]**
  - Haircut stress schedules (§6.5) should depend on collateral type and market segment.
  - As a dealer client, ADIC faces dealer-to-client terms.

**19. [Beyond Basis Basics: Liquidity Demand and Deviations from the Law of One Price](https://consensus.app/papers/details/a7d47a2caaad5fd793813e19bd55a5d2/?utm_source=claude_desktop)**
- Todd M. Hazelkorn et al. · 2022 · *Journal of Finance* · 5 citations · DOI 10.1111/jofi.13198
- *Finding:*
  - The futures–cash basis reflects liquidity demand for equity exposure.
  - It comoves with dealer and investor futures positions, and it negatively predicts futures and spot returns.
  - Persistent supply–demand imbalances imply "an annual premium of 5% to 6%".
  - The [SSRN version](https://consensus.app/papers/details/ec8be5409274522b812f73c7ea211269/?utm_source=claude_desktop) ties bases to intermediaries' cost of capital and to leverage demand.
- *Relevance:* This is an academic basis for the dossier's futures-financing inputs, which currently come from D. E. Shaw and CME. It also separates futures-implied financing from equity-repo financing (verifier R12). **[Inference]** Treat a rich basis as a state variable: synthetic leverage is expensive exactly when forward index returns are lower.

### E. Debt structure, refinancing and internal pricing (Corporate Finance)

**20. [Rollover Risk and Credit Risk](https://consensus.app/papers/details/272186b246105b7e98e6c262a594de43/?utm_source=claude_desktop)**
- Zhi-Guo He (as displayed; Consensus shows one author) · 2012 · *Journal of Finance* · 630 citations · DOI 10.1111/j.1540-6261.2012.01721.x
- *Finding:*
  - Losses on rolling over maturing debt fall on equity holders, who absorb them only while keeping the firm alive is worth it.
  - Deteriorating market liquidity and shorter debt maturity both make costly default happen at higher fundamental thresholds.
- *Relevance:* **[Inference]** For ADIC's facilities:
  - refinancing cost and failure probability should rise together with market illiquidity and with the share of debt maturing soon;
  - rollover should be modelled endogenously, replacing the dossier's fixed "50% rollover failure in Stress" in §6.9D.

**21. [A Note on Liquidity Risk Management](https://consensus.app/papers/details/e5d07eaeb7cb57e9977a1900ca0d5a7a/?utm_source=claude_desktop)**
- M. Brunnermeier et al. · 2009 · *American Economic Review* (P&P) · 89 citations · DOI 10.1257/aer.99.2.578
- *Finding:*
  - Minimizing rollover risk means maximizing the *effective* maturity of liabilities across several refinancing cycles, not the maturity of the bonds now outstanding.
  - Short-term debt lets a healthy firm readjust its maturity structure faster.
- *Relevance:* **[Inference]** Constraint 8 (weighted-average funding maturity ≥ gap duration) should be complemented by a dynamic issuance policy evaluated in the simulator. Terming out while healthy can beat a static maturity floor.

**22. [Fund Transfer Pricing for Deposits and Loans, Foundation and Advanced](https://consensus.app/papers/details/59596c9dbc355d4a93f649ba14e8e1fc/?utm_source=claude_desktop)**
- J. Dermine · 2011 (record) · *The Journal of Financial Perspectives* · 18 citations · DOI 10.2139/ssrn.2069917
- *Finding:* After the crisis, FTP must handle five previously ignored issues:
  - interbank rationing;
  - the cost of a Basel III contingency liquidity buffer;
  - credit-risk-specific transfer prices;
  - a liquidity premium for long-term funding;
  - consistent treatment of the bank's own credit spread.
- *Relevance:* Corporate Finance owns treasury and the funding side. **[Inference]** Its internal transfer-pricing curve should contain each component:
  - a term liquidity premium by time to liquidity;
  - a charge for the cost of carrying the contingency reserve;
  - ADIC's own spread.

  The optimizer's λ then validates the curve.

### F. Payout, drawdown and growth constraints

**23. [Why are University Endowments Large and Risky](https://consensus.app/papers/details/248d35997763530a9386a6a4059638f2/?utm_source=claude_desktop)**
- Thomas J. Gilbert et al. · 2015 · *Review of Financial Studies* · 42 citations · DOI 10.1093/rfs/hhv031
- *Finding:*
  - The model combines universities' production decisions with endowment size and allocation.
  - Adding the UPMIFA 7% payout constraint reproduces observed endowment sizes and allocations.
  - The constraint harms universities that value their internal projects. It "prevents the endowment's use as an effective buffer stock", raises production volatility and slows the most productive universities' growth.
- *Relevance:* **[Inference]** ADIC's 5–10% band has both a floor and a cap, and either can bind. The value of flexibility inside the band should be computed and shown to the IC and the owner, as the dossier proposes in §6.8(e).

**24. [Multi-period portfolio selection with drawdown control](https://consensus.app/papers/details/88b77eb53f2f532483982aba3c5ba5fb/?utm_source=claude_desktop)**
- P. Nystrup et al. · 2018 (record; Ann. OR 2019) · *Annals of Operations Research* · 62 citations · DOI 10.1007/s10479-018-2947-3
- *Finding:*
  - The method is MPC with hidden-Markov forecasts, with risk aversion adjusted to realized drawdown.
  - Tested out of sample over two decades on liquid indices, it controlled drawdowns "with little or no sacrifice of mean–variance efficiency".
  - Leverage raised returns without raising maximum drawdown.
- *Relevance:* This is a soft alternative to the dossier's hard drawdown barrier (constraint 10), which verifier R4 found can force a net-short overlay. It fits inside the MPC architecture the dossier already recommends.

**25. [Optimal capital growth with convex shortfall penalties](https://consensus.app/papers/details/4ce92007e72c5b1aab545cdc2e59de35/?utm_source=claude_desktop)**
- L. MacLean et al. · 2016 · *Quantitative Finance* · 8 citations · DOI 10.1080/14697688.2015.1059469
- Companion: [Kelly investing with downside risk control in a regime-switching market](https://consensus.app/papers/details/6510dbe8c3fa55139c8728a4efbfe07c/?utm_source=claude_desktop), L. MacLean et al., 2021, QF, 7 citations, DOI 10.1080/14697688.2021.1993617.
- *Finding:*
  - The method maximizes growth while staying above a discrete-time wealth path with high probability, penalizing shortfalls below the path with a convex function.
  - Markets switch between regimes as a Markov chain, and the problem is reformulated as a deterministic program.
  - The 2021 paper derives a "modified Kelly" strategy with regime weights and a downside threshold.
- *Relevance:* **[Inference]** This merges the dossier's constraints 9 (fractional-Kelly cap) and 10 (drawdown barrier) into one tractable, regime-aware rule with a soft floor. That suits the robust 7% floor, which works as a target path rather than a hard wall.

---

## 4. Missed-but-important papers: design implications

### 4.1 State variables

- **Commitment-adjusted leverage, as a reported state and a constraint input.**
  - **[Inference]** Define L^c_t = (B^recourse_t + Σ_i κ̄_i(stress, age) · U_{i,t}) / E_t, where κ̄_i is the stressed call rate over the next 12–24 months. Report it beside recourse and economic leverage.
  - The basis is [Meyer (2020)](https://consensus.app/papers/details/d99e5eff8f48558898b24269df59ba18/?utm_source=claude_desktop) (uncalled capital as a loan) and [Gourier et al.](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop) (large commitment-risk premia).
  - This addresses verifier R5(b).
- **A funding-liquidity factor f_t shared by assets and liabilities.** [Franzoni et al.](https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop) find PE loads on market liquidity through a funding channel.
  - **[Inference]** Let f_t drive, jointly:
    - private-asset return shocks;
    - the secondary discount d_i;
    - segment-specific haircuts h_k;
    - the refinancing spread and rollover-failure probability.
  - **[Inference]** Candidate observable proxies:
    - the futures–cash basis ([Hazelkorn et al.](https://consensus.app/papers/details/a7d47a2caaad5fd793813e19bd55a5d2/?utm_source=claude_desktop));
    - a TED-type spread, where [Boudt et al.](https://consensus.app/papers/details/f810e62599e25377b4a05ce2c696246b/?utm_source=claude_desktop) find a regime switch for equity-collateralized funding near 48 bp;
    - dealer balance-sheet usage.
  - This makes wrong-way risk endogenous instead of imposed by scenario.
- **Secondary-market capacity state Cap^sec_t.** Two papers show discounts track liquidity supply and capacity can vanish:
  - [Albuquerque et al.](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop): discounts track liquidity supply.
  - [Hege et al.](https://consensus.app/papers/details/e2a6180114bb5e16be2ab5d849fa5cbf/?utm_source=claude_desktop): volume collapsed in early 2009.

  **[Inference]** Make d_i(s_t, Cap_t, x_i) depend on capacity and on size. [Dinç et al.](https://consensus.app/papers/details/ee77045e07675a659c38a6f8264d43a1/?utm_source=claude_desktop) give a block-size slope (§4.3).
- **Look-through fund debt per fund.** Track a subscription-line balance and GP NAV-facility usage for each fund.
  - [Albertus & Denes](https://consensus.app/papers/details/84b7e9e9b66151e78637a4ebfac077ae/?utm_source=claude_desktop): subscription lines reduce calls and distort IRRs.
  - **[Inference]** Subscription-line balances are deferred calls. Add a "call surge on facility repayment" term to κ_i in stress.
  - **[Inference]** Flag subscription-line-inflated IRRs to the return-fusion stream.
- **Nowcast NAV and its volatility, per fund.** [Brown, Ghysels & Gredil](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop) estimate weekly unsmoothed NAVs. **[Inference]**
  - Use nowcasts for LTV stress on NAV-facility pools.
  - Keep reported NAV, with its lags, for covenant triggers.
- **Overlay liquidity sensitivity in both tails.**
  - [Alfaro et al.](https://consensus.app/papers/details/d194a64624745726be3cb46d2cb00e74/?utm_source=claude_desktop) (LASH) and [Jansen et al.](https://consensus.app/papers/details/65e862e24881598a97200e1611a991ed/?utm_source=claude_desktop) document both sides of the exposure.
  - **[Inference]** Carry two state variables: VM sensitivity to a recovery or rally (the tail hedge bleeds collateral) and VM sensitivity to rate rises (receive-fixed swaps). Do not carry only P99 stress margin.
- **Debt maturity profile with a dispersion index.** [Choi, Hackbarth & Zechner](https://consensus.app/papers/details/6b5c98278cb25bf89a91f66648b97f5f/?utm_source=claude_desktop) find that maturity dispersion is a distinct dimension of capital structure, and that new issues depend on the existing profile. **[Inference]** Add a dispersion statistic to the maturity buckets B^{(m)}_{k,t}.

### 4.2 Models

- **Endogenous rollover in the funding-plan module.** **[Inference]** Make the probability of rollover failure and the refinancing spread functions of (regime, f_t, own leverage, maturity profile), replacing the fixed 50% stress rate. Evidence:
  - [He & Xiong](https://consensus.app/papers/details/272186b246105b7e98e6c262a594de43/?utm_source=claude_desktop): illiquidity and short maturity raise default thresholds.
  - [Brunnermeier & Oehmke](https://consensus.app/papers/details/82205f71ae1f51b3b3dddb774ade800f/?utm_source=claude_desktop): the "maturity rat race" means lenders shorten maturities, most of all in volatile periods. **[Inference]** Long tenors may be unavailable in the Tight and Stress regimes, so the tenor menu should depend on the state.
- **An effective-maturity objective for the issuance policy** ([Brunnermeier & Yogo](https://consensus.app/papers/details/e5d07eaeb7cb57e9977a1900ca0d5a7a/?utm_source=claude_desktop)). **[Inference]** Tune term-out rules in the simulation-based policy search of dossier §3, rather than fixing a static weighted-average maturity.
- **A hedge-before-sell ordering with a no-trade band.**
  - [Gallien et al. (Risks 2018)](https://consensus.app/papers/details/fdaa9420b76e5195a1ed02f64d9fb772/?utm_source=claude_desktop) study an investor holding an illiquid alpha fund under a lower bound on net return. After a loss, the investor either pays transaction costs to deleverage or hedges with liquid futures and keeps the residual risk. Higher alpha and lower beta widen the no-trading zone.
  - **[Inference]** This formalizes "lever and hedge the liquid, not the illiquid". In the forced-deleveraging module, use the order: overlay hedge → reserve → committed lines → term debt → SELL. Use SELL only outside a band that widens with an asset's α* and narrows with its β.
  - Note the venue: *Risks* (MDPI), 2 citations. Use it for structure, not calibration.
- **Overlay as the illiquid book's hedging portfolio.**
  - [Bichuch & Guasoni (Math. Finance 2018)](https://consensus.app/papers/details/cf16e709e2b25092baad0b1e4e7982a4/?utm_source=claude_desktop) derive four-fund separation: the safe asset, the myopic portfolio, the illiquid asset and its hedging portfolio. Liquid assets create diversification and hedging motives that reduce trading in the illiquid asset.
  - **[Inference]** This is a theoretical basis for assigning the overlay the role of the PE book's hedging portfolio.
- **Collateralize rather than sell liquid assets when opportunities persist.**
  - [Parlatore (JFE 2019)](https://consensus.app/papers/details/10225d185aa35c0f8f48c7a351c60eb6/?utm_source=claude_desktop): liquid assets are used as collateral rather than sold when investment opportunities are persistent, and they carry funding-liquidity and collateral premia.
  - **[Inference]** For liquid holdings, the choice between REFINANCE (repo) and SELL should weigh how persistent the opportunity set is, for example secondaries dry powder in stress, against encumbrance.
- **Commitment layer benchmarks.**
  - [Gourier et al.](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop) and [Giommetti & Jørgensen](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop) are dynamic LP models with commitments and a secondary market.
  - **[Inference]** Use them as regression tests for how the simulator trades off LEVER against pacing C_t.
- **Attribution for every leverage policy.** **[Inference]** Add the five-term decomposition of [Anderson et al. (2014)](https://consensus.app/papers/details/8a242fcc6d1d5d5bb393e76ffce91e3a/?utm_source=claude_desktop) to the ablation and attribution module (deck slide 6): source return, financing, covariance, turnover and variance drag.
- **Market impact in synthetic leverage and deleveraging.** [Edirisinghe et al. 2023](https://consensus.app/papers/details/626d6c94bb4f5c1c912d5ce4d1ee0ef3/?utm_source=claude_desktop) and [Edirisinghe et al. 2021](https://consensus.app/papers/details/0ab4f389888e5acaa873cf35e741dad1/?utm_source=claude_desktop).
- **Soft drawdown control instead of a hard barrier.** **[Inference]** Any of the three removes the infeasibility in verifier R4:
  - drawdown-scaled risk aversion inside MPC ([Nystrup et al.](https://consensus.app/papers/details/88b77eb53f2f532483982aba3c5ba5fb/?utm_source=claude_desktop));
  - a convex shortfall penalty below a wealth path, with regimes ([MacLean et al. 2016](https://consensus.app/papers/details/4ce92007e72c5b1aab545cdc2e59de35/?utm_source=claude_desktop); [2021](https://consensus.app/papers/details/6510dbe8c3fa55139c8728a4efbfe07c/?utm_source=claude_desktop));
  - the LP-representable Conditional Drawdown-at-Risk measure ([Chekhlov et al.](https://consensus.app/papers/details/b81e3a221093580dac48d13ea53f3975/?utm_source=claude_desktop), 330 citations) inside the convex inner problem.

  For payout-plus-drawdown structure:
  - [Élie & Touzi (Finance & Stochastics 2008)](https://consensus.app/papers/details/7af6963baf0d5fd08963d227269b5a4e/?utm_source=claude_desktop) solve consumption and investment under a drawdown constraint in closed form.
  - [Roche (QF 2018)](https://consensus.app/papers/details/f9801d5251745a0bb468a76fb08c8366/?utm_source=claude_desktop) studies foundations with endogenous withdrawals under a drawdown constraint and finds risky investment "may decrease as wealth approaches its maximum".
- **Tax smoothing when markets are incomplete.** This refines the dossier's Barro analogy (§2.7).
  - [Aiyagari et al. (JPE 2002)](https://consensus.app/papers/details/f0b79e6a65be56d3ad5a96eff11dafe3/?utm_source=claude_desktop): with risk-free debt only, a near-unit root enters debt and taxes, and without limits on asset holdings outcomes "can diverge in important ways from Barro's".
  - [Bohn (AER)](https://consensus.app/papers/details/c93a801346f35768aad39cf4811faeec/?utm_source=claude_desktop): optimal government liabilities include state-contingent securities that hedge budget shocks. The Consensus record year is 2016, but the abstract carries a 1990 AEA copyright.
  - **[Inference]** The payout-band rule should smooth close to a random walk with an explicit cap on the debt state. ADIC's state-contingent "liabilities" play the role Bohn favors:
    - the tail hedge;
    - committed facilities;
    - deferred-payment secondary sales.

### 4.3 Parameters and calibration priors (literature values, not ADIC data)

- **Rates-overlay margin.** Swap margin calls can exceed 6% of total assets when rates rise (Dutch pension funds; [Jansen et al.](https://consensus.app/papers/details/65e862e24881598a97200e1611a991ed/?utm_source=claude_desktop)).
- **LASH scale.** At peak, a 100 bp rate rise implied liquidity needs close to the UK pension and insurance sector's cash holdings ([Alfaro et al.](https://consensus.app/papers/details/d194a64624745726be3cb46d2cb00e74/?utm_source=claude_desktop)).
- **Repo cost versus margin.** In stressed times, each 1 pp increase in initial margin was followed by about a 10 bp rise in repo rates (Italian repo, 2011–12; [Miglietta et al.](https://consensus.app/papers/details/eebc5164b7da543ba4a7fc5bd45fa88a/?utm_source=claude_desktop)). **[Inference]** Use this as a slope linking h_k to c_k in §6.5.
- **Funding-regime boundary.** For equity-collateralized funding, the regime switch occurs near a TED spread of 48 bp ([Boudt et al.](https://consensus.app/papers/details/f810e62599e25377b4a05ce2c696246b/?utm_source=claude_desktop)).
- **Futures basis.** Persistent imbalances imply a 5–6% annual premium ([Hazelkorn et al.](https://consensus.app/papers/details/a7d47a2caaad5fd793813e19bd55a5d2/?utm_source=claude_desktop)). This is a return premium to liquidity supply, not a funding spread. Do not plug it into c_k.
- **Cost of selling.** Secondary buyers outperform sellers by about 5 pp a year, market-adjusted (PME 1.023 vs 0.976; [Nadauld et al.](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop)).
- **Size-dependent fire-sale discount.**
  - Distressed sales of minority equity stakes: about 8% discount.
  - Stakes above 5% of the firm, or sold as a block: 13–14%.
  - Prices recover afterwards ([Dinç et al.](https://consensus.app/papers/details/ee77045e07675a659c38a6f8264d43a1/?utm_source=claude_desktop)).
  - **[Inference]** Use this as a prior slope for ADIC-size tranches (dossier §7, "market impact").
- **PE liquidity premium.** About 3% a year; alpha falls to about zero once it is included ([Franzoni et al.](https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop)).
- **Commitment-risk premium.** Equivalent to about 1.63% a year with many funds ([Phalippou et al. 2014](https://consensus.app/papers/details/9b5881d8cef05dffa4a40423d6b15bc8/?utm_source=claude_desktop)).
- **Fund-level unsmoothed risk** ([Brown, Ghysels & Gredil](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop)):
  - buyout: β ≈ 1.0, σ ≈ 33% a year;
  - venture: β ≈ 1.4, σ ≈ 40%.
- **Dynamic-leverage drags, 1929–2013** ([Anderson et al. 2014](https://consensus.app/papers/details/8a242fcc6d1d5d5bb393e76ffce91e3a/?utm_source=claude_desktop)):
  - covariance term: −0.64 to −4.23% a year;
  - turnover: −0.27 to −2.59%;
  - variance drag: −0.41 to −2.84%.
- **Hedge-fund liquidity and smoothing** ([Cao et al., MS 2017](https://consensus.app/papers/details/263bf0e52d355c0baf0c7fef98bc44e5/?utm_source=claude_desktop)):
  - 33% of reported smoothing is due to managerial reporting;
  - fund-level liquidity is associated with a 1.7% annual performance reduction.

  Use these for redemption terms in the Public Markets group.
- **Sharpe-ratio inflation.** Annual hedge-fund Sharpe ratios can be overstated by as much as 65% because of serial correlation ([Lo 2002](https://consensus.app/papers/details/ae10105da6315c3da6ea60251ec0b456/?utm_source=claude_desktop)). **[Inference]** Kelly-cap inputs built from smoothed returns overstate leverage capacity.

### 4.4 Constraints

- **A commitment-adjusted leverage limit.** **[Inference]** Example form: P(L^c_t > ℓ^c for any t ≤ 3y) ≤ 5%, alongside the dossier's recourse limit. Basis: Meyer and Gourier et al.
- **Liquidity coverage in both tails.** **[Inference]**
  - Constraint 12 should cover rally-side collateral drain on the tail hedge ([Alfaro et al.](https://consensus.app/papers/details/d194a64624745726be3cb46d2cb00e74/?utm_source=claude_desktop)) as well as stress-side margin.
  - Rates buffers should be instrument-specific ([Jansen et al.](https://consensus.app/papers/details/65e862e24881598a97200e1611a991ed/?utm_source=claude_desktop)). This supports verifier R11.
- **Segment-specific haircuts** ([Krishnamurthy et al.](https://consensus.app/papers/details/22caff417161575d85e2ef9c58fabe56/?utm_source=claude_desktop); [Copeland et al.](https://consensus.app/papers/details/b4498a6023e95908834404ffd98876ab/?utm_source=claude_desktop)). **[Inference]** Split the §6.5 repo rows by:
  - collateral: Treasury vs agency or IG;
  - segment: tri-party vs bilateral dealer-to-client.

  Tie the stressed haircut add-on in constraints 1 and 12 to segment.
- **SELL capacity in stress.** **[Inference]** Cap x_{i,t} at a share of Cap^sec_t, and apply a size-dependent discount. Basis: Hege et al., Albuquerque et al. and Dinç et al.
- **Maturity.**
  - [Choi et al.](https://consensus.app/papers/details/6b5c98278cb25bf89a91f66648b97f5f/?utm_source=claude_desktop) support constraint 8's 12-month concentration cap.
  - **[Inference]** Replace the static weighted-average-maturity ≥ gap rule with an effective-maturity test in simulation ([Brunnermeier & Yogo](https://consensus.app/papers/details/e5d07eaeb7cb57e9977a1900ca0d5a7a/?utm_source=claude_desktop)).
- **Drawdown as a soft constraint** (§4.2).
  - Control-engineering results warn against a hard barrier:
    - QPs built on control barrier functions (CBF-QPs) "can easily become infeasible" with many safety constraints and tight control limits ([Xiao & Belta, IEEE TAC 2021](https://consensus.app/papers/details/98c515a2e4a75c27aa67781548e204c7/?utm_source=claude_desktop)).
    - CBF-QPs can introduce undesirable stable equilibria at the boundary of the safe set ([Reis et al. 2020](https://consensus.app/papers/details/7e7aeda030d35494b90baa1df6b74f1c/?utm_source=claude_desktop)).
  - **[Inference]** By analogy, a hard barrier on a 60%-illiquid book can trap the overlay at zero or negative exposure (verifier R4).
- **Chance constraints in MPC.**
  - In scenario MPC, probabilistic constraints must be read as average-in-time, not pointwise-in-time, and specified and observed closed-loop violation rates can differ ([Schildbach et al., Automatica](https://consensus.app/papers/details/058e4932889a5540b1b831734b326d4d/?utm_source=claude_desktop)).
  - **[Inference]** State whether constraint 7 (covenant breach ≤ 2% within 12 months) is per path or per period, and verify closed-loop rates in the simulator.
- **The Kelly cap (constraint 9).**
  - Compute it on desmoothed σ (Getmansky–Lo–Makarov; Lo 2002).
  - Shrink the mean. The Kelly strategy has "great sensitivity to parameter estimates, especially the means" ([Ziemba & MacLean 2011](https://consensus.app/papers/details/3b45433656a157f7a64492d1f6adaf05/?utm_source=claude_desktop)).
- **Regulatory scenarios.** Flag these for the Adversarial Funding-Stress agent; they are not facts.
  - The FSB minimum-haircut framework would bind hardest on larger and more leveraged non-banks ([Grill et al. 2024](https://consensus.app/papers/details/207fee1b265957658425edfa8ffae8b2/?utm_source=claude_desktop)).
  - An analysis piece argues that the US Treasury clearing mandate converts credit risk into margin-driven liquidity risk ([Pirrong 2024](https://consensus.app/papers/details/fe4749db8c0156f9b63e85da6e94f7d4/?utm_source=claude_desktop); opinion, not empirical). This bears on dossier §8's unverified clearing point.

### 4.5 Objectives

- **Do not lever toward the target.**
  - Two papers show losses from target-driven or frictionless leverage: [Edirisinghe et al. 2023](https://consensus.app/papers/details/626d6c94bb4f5c1c912d5ce4d1ee0ef3/?utm_source=claude_desktop) and [Anderson et al. 2012](https://consensus.app/papers/details/efc234a01031512da8540369cc25e099/?utm_source=claude_desktop).
  - This supports dossier §6.8(a): aggregate leverage is a risk-budget decision, never an α decision.
- **Price the flexibility of the payout band.**
  - [Gilbert & Hrdlicka](https://consensus.app/papers/details/248d35997763530a9386a6a4059638f2/?utm_source=claude_desktop): a binding payout constraint destroys the buffer-stock role.
  - [Friedman et al. (JAI 2025)](https://consensus.app/papers/details/7217d92bfdb25b3b92a4df1561cce5c4/?utm_source=claude_desktop): the faster a pension fund raises contributions after downturns, the greater its capacity for illiquid assets. The authors extend the analysis to endowments.
  - **[Inference]** For ADIC the analog is payout flexibility. Report its value on the IC frontier.
- **Replace eventual-ruin headlines.**
  - [Milevsky (FAJ 2016)](https://consensus.app/papers/details/b62c9501e06c5b3189cadb150a5a9de5/?utm_source=claude_desktop) argues against ruin probabilities as the guiding metric and proposes portfolio longevity.
  - **[Inference]** Show the time-to-depletion distribution over IC horizons (verifier R10).
- **Avoid double counting** (verifier R6). **[Inference]** Simulate the decomposition terms in Anderson et al. (2014) explicitly, and add penalties only for unmodeled items: rating migration, covenant-cure frictions and signalling.

### 4.6 Agent, IC and organizational design

- **Corporate Finance (Treasurer seat).** It runs the funding and liability side: facilities, overlay collateral and distribution payments.
  - **[Inference]** It publishes a matched-maturity FTP curve with three components ([Dermine](https://consensus.app/papers/details/59596c9dbc355d4a93f649ba14e8e1fc/?utm_source=claude_desktop)):
    - a term liquidity premium;
    - a contingency-reserve carry charge;
    - ADIC's own spread.
  - Two cautions from the FTP literature:
    - An inappropriate or artificial FTP drives poor business decisions ([Choudhry](https://consensus.app/papers/details/088daee33e4a5ee695fd3a369db68288/?utm_source=claude_desktop)).
    - Even sophisticated FTP systems are unclear about who bears unexpected liquidity risk ([Lindblom et al.](https://consensus.app/papers/details/5af9b637fad751aab54838072ca31169/?utm_source=claude_desktop)).
  - **[Inference]** Validate the curve against the optimizer's λ.
  - **[Inference]** Charge group LEVER and REFINANCE proposals at FTP plus a contingent-liquidity charge.
  - **[Inference]** Credit the tail hedge for stress inflows, and charge it for LASH-type collateral use when markets rally.
  - **[Inference]** Corporate Finance owns the rollover and maturity model (§4.2) and the payout-band valuation.
- **Secondaries group (hybrid fund and direct book).**
  - **Liquidity provider.** It is ADIC's countercyclical liquidity provider: flexible buyers earn about 5 pp a year ([Nadauld et al.](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop)).
  - **SELL intelligence.** Its quotes feed SELL. Bids fall with aggregate liquidity shocks ([Albuquerque et al.](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop)). Interests are more liquid when the fund is larger, buyout-focused and has less undrawn capital ([Kleymenova et al.](https://consensus.app/papers/details/9bc5ce1dd6415d858fb1193b5b1b3466/?utm_source=claude_desktop)), which can rank SELL candidates.
  - **Look-through leverage in the fund sleeve.** A practitioner article notes that secondaries funds and funds of funds increasingly borrow against their LP interests ([Kerfoot et al. 2017, *Journal of Investment Compliance*](https://consensus.app/papers/details/a5ded5adb80a56b79645ea92c5cdd6b6/?utm_source=claude_desktop)). **[Inference]** That is look-through leverage in the group's third-party fund sleeve.
  - **[Inference]** Keep the context file's rule: a transfer between ADIC groups is zero-sum and never counts as liquidity raised.
- **Capital Solutions.**
  - It supplies NAV-loan and preferred-equity pricing.
  - Academic NAV-loan evidence is thin: the two NAV-financing papers found ([Baker 2024](https://consensus.app/papers/details/f457b903aae95a57844b6cd41904b1d7/?utm_source=claude_desktop); [Reddy 2024](https://consensus.app/papers/details/dfec35a563a150b0ac00b68fa35ab87d/?utm_source=claude_desktop)) had no abstract in Consensus.
  - **[Inference]** Treat NAV-loan terms as market data from live quotes, not literature calibration (verifier R14).
- **PE group.**
  - **[Inference]** Report GP subscription-line and NAV-facility usage per fund as look-through leverage.
  - **[Inference]** Adjust interim IRRs before they enter return fusion ([Albertus & Denes](https://consensus.app/papers/details/84b7e9e9b66151e78637a4ebfac077ae/?utm_source=claude_desktop)).
- **Public Markets.**
  - Hedge funds' leverage depends on prime-broker credit supply, and that matters more in stress ([Li et al., FEDS 2024](https://consensus.app/papers/details/98d0571e779f5dd5809059c7f37fea58/?utm_source=claude_desktop)).
  - **[Inference]** Look-through leverage in the hedge-fund book contracts exactly when ADIC may want redemptions.
- **Private Credit.**
  - A 2026 survey finds that risk-adjusted returns for the average private-credit fund are "largely consumed by fees" ([Zou](https://consensus.app/papers/details/312d67578aa95bf9b14b429c5165f5d0/?utm_source=claude_desktop)).
  - **[Inference]** Back-leverage should clear the dossier's asset LEVER test on α* net of fees.
- **Devil's-advocate agent.** **[Inference]** Keep a register of contested evidence (§5). Challenge any proposal that leans on BAB or levered risk parity, on endowment "hoarding" behaviour, or on vintage diversification as a cure for commitment risk.
- **Rubric checks for every LEVER recommendation.** **[Inference]** Each must include:
  - a frictions-included backtest;
  - the Anderson et al. decomposition;
  - segment-specific haircuts;
  - a SELL-capacity stress;
  - commitment-adjusted leverage.

---

## 5. Papers that challenge the dossier's recommendations

| Dossier position | Challenging evidence | Strength and caveats | Suggested response |
|---|---|---|---|
| §2.3: leverage aversion and BAB imply ADIC should lever low-volatility, high-Sharpe exposures; risk parity should be levered | [Anderson et al. 2012](https://consensus.app/papers/details/efc234a01031512da8540369cc25e099/?utm_source=claude_desktop): after frictions, levered risk parity underperformed the market (1926–2010). [Novy-Marx & Velikov](https://consensus.app/papers/details/17755f59391c5311b233e577e07dd1ef/?utm_source=claude_desktop): BAB rests on non-standard construction and biased betas. [Barroso et al., JFE 2025](https://consensus.app/papers/details/deed93563219563e8ded549062aa1a01/?utm_source=claude_desktop): leverage-constraint theory "counterfactually predicts" that BAB Sharpe ratios rise with volatility. [Schneider et al., JF 2020](https://consensus.app/papers/details/e9efdab7b66f54418cdbc668339cdc0e/?utm_source=claude_desktop): controlling for skewness makes BAB alphas insignificant. [Cederburg & O'Doherty, JF 2016](https://consensus.app/papers/details/710888c2d1ea5d8fbc4f4319fdeb8c27/?utm_source=claude_desktop): a conditional CAPM resolves the beta anomaly. | Mixed. On the other side: [betting against correlation (JFE 2020)](https://consensus.app/papers/details/9fcadced645455f18d9739996f42e8b5/?utm_source=claude_desktop) supports leverage-constraint theories, and [Boguth & Simutin (JFE)](https://consensus.app/papers/details/eca014dd9f02504cb2ba8d33b3e9291e/?utm_source=claude_desktop) find that leverage-constraint tightness predicts BAB. **[Inference]** ADIC's AA funding is cheaper than the frictions assumed in the critiques. | Keep "lever the liquid", but justify each levered sleeve on its own net-of-friction α*. Require frictions-included backtests. Do not present BAB to the IC as settled. |
| §2.4 and the Dimmock–Wang–Yang implication: staggered lock-ups and vintage diversification are a liquidity asset | [Phalippou et al. 2014](https://consensus.app/papers/details/9b5881d8cef05dffa4a40423d6b15bc8/?utm_source=claude_desktop): many funds diversify liquidity events but create a costly funding mismatch, and the commitment premium *rises* (to ≈1.63% a year). [Gourier et al. 2024](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop): premia do not disappear across many funds, and they increase with secondary liquidity. | Both are model-based, and the setting differs: commitments and calls, not lock-up expiry. | Treat vintage diversification as reducing the variance of distribution timing, not commitment risk. Size unfunded commitments explicitly in leverage (§4.4). |
| §2.7: Brown et al. (2014) "hoarding" asymmetry underpins the payout band as an implicit liquidity option | [Rosen & Sappington 2019](https://consensus.app/papers/details/30db9b06ea85503da3e4097350b48651/?utm_source=claude_desktop): payouts respond *symmetrically* to positive and negative shocks (700+ universities, 1987–2009). | The evidence is contested and comes from different samples. It weakens the behavioural prior, not the option model. | Do not calibrate owner behaviour from endowment evidence. Elicit the owner's tolerance (dossier open question 2). |
| §4.3: "the market can absorb ADIC-sized sales" | [Hege et al.](https://consensus.app/papers/details/e2a6180114bb5e16be2ab5d849fa5cbf/?utm_source=claude_desktop): early-2009 volume fell to a fraction of prior levels. [Albuquerque et al.](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop): bids fall with aggregate liquidity shocks. [Dinç et al.](https://consensus.app/papers/details/ee77045e07675a659c38a6f8264d43a1/?utm_source=claude_desktop): block discounts of 13–14%. | Strong qualitatively. The 2009 market was far smaller than today's. Verifier R13 already flags the extrapolation. | Add a SELL capacity constraint and a size-dependent discount (§4.4). |
| §2.6 and constraint 10: a hard drawdown barrier (CPPI or CBF) on discretionary exposure | [Anderson et al. 2014](https://consensus.app/papers/details/8a242fcc6d1d5d5bb393e76ffce91e3a/?utm_source=claude_desktop): dynamic leverage pays a negative covariance drag of 0.64–4.23% a year. [Xiao & Belta](https://consensus.app/papers/details/98c515a2e4a75c27aa67781548e204c7/?utm_source=claude_desktop) and [Reis et al.](https://consensus.app/papers/details/7e7aeda030d35494b90baa1df6b74f1c/?utm_source=claude_desktop): CBF-QPs can be infeasible or create spurious boundary equilibria. Soft alternatives: [Nystrup et al.](https://consensus.app/papers/details/88b77eb53f2f532483982aba3c5ba5fb/?utm_source=claude_desktop) and [MacLean et al.](https://consensus.app/papers/details/4ce92007e72c5b1aab545cdc2e59de35/?utm_source=claude_desktop). | The covariance evidence comes from volatility targeting, not drawdown rules **[Inference]**. The CBF results transfer by analogy only. | Use a soft penalty or risk-aversion scaling, with feasibility checks, and report the covariance drag in attribution. |
| Executive summary 5, §6.9D and §2.6: forced deleveraging falls on the liquid sleeve, and HQLA sells at par less haircut | [Chaderina et al., MS 2026](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop): selling the most liquid bonds first "can backfire", because widely held liquid bonds fall most when many sell at once. [Jansen et al.](https://consensus.app/papers/details/65e862e24881598a97200e1611a991ed/?utm_source=claude_desktop): procyclical sales of safe bonds depress their prices. | Evidence comes from insurer and pension bond portfolios. ADIC's liquid sleeve is multi-asset. | Model price impact on crowded HQLA in stress, and diversify the reserve's composition: cash, bills, committed lines. |
| Executive summary 2(a) and §6.8(c): borrow ex post to bridge temporary gaps instead of selling | [Anglin & Gao (REE 2011)](https://consensus.app/papers/details/29f5d1f3ce855a36b86e0c22a1ef2f0c/?utm_source=claude_desktop): "borrowing to pay for a liquidity shock cannot overcome all of the costs of owning an illiquid asset", whereas borrowing at t = 0 "benefits from the complementarity in the assets". | A real-estate portfolio model; qualitative. It is consistent with the dossier's own Monte Carlo, in which a debt-funded reserve dominates. | Prefer ex-ante term funding and committed lines sized before the shock over ex-post NAV loans. |
| §2.7: tax smoothing, in which debt absorbs temporary shocks | [Aiyagari et al.](https://consensus.app/papers/details/f0b79e6a65be56d3ad5a96eff11dafe3/?utm_source=claude_desktop): with only risk-free debt, outcomes can diverge without asset limits. [Bohn](https://consensus.app/papers/details/c93a801346f35768aad39cf4811faeec/?utm_source=claude_desktop): optimal liabilities are partly state-contingent. | Theory for governments. A refinement, not a contradiction. | Cap the debt state explicitly and use state-contingent funding instruments (§4.2). |
| Executive summary 6 and §6.9B: the infinite-horizon ruin headline (≈58%) | [Milevsky 2016](https://consensus.app/papers/details/b62c9501e06c5b3189cadb150a5a9de5/?utm_source=claude_desktop): ruin probabilities should not be the guiding metric. A [discussion of Milevsky & Robinson](https://consensus.app/papers/details/92335896aced5314a5b9fa0df406beaf/?utm_source=claude_desktop) notes that a constant-consumption rule is generally not optimal, which limits the framework's theoretical value. | An argument about communication and theory. It agrees with verifier R10. | Report the time-to-depletion distribution over IC horizons. |
| §6.5: one regime-dependent haircut schedule per repo class | [Krishnamurthy et al.](https://consensus.app/papers/details/22caff417161575d85e2ef9c58fabe56/?utm_source=claude_desktop) and [Copeland et al.](https://consensus.app/papers/details/b4498a6023e95908834404ffd98876ab/?utm_source=claude_desktop): haircut spikes were concentrated in bilateral and dealer-to-hedge-fund repo, while tri-party stayed stable. | Strong empirical evidence. | Use segment- and collateral-specific schedules (§4.4). |

**Supporting rather than challenging:**
- [Gupta & Van Nieuwerburgh](https://consensus.app/papers/details/a07fbcfb0fdd5d5891ce4d67340cbeb8/?utm_source=claude_desktop) find negative risk-adjusted profit for the average PE fund. This supports §6.8(b): do not lever PE for return. [Korteweg's review](https://consensus.app/papers/details/996d0a57b17957dd81fec3ac0698ec30/?utm_source=claude_desktop) is more favourable to buyouts against a levered stock portfolio, so the asset test should stay estimate-dependent.
- [Sorensen et al.](https://consensus.app/papers/details/15cb135a45b35616b82e97bf090f24ae/?utm_source=claude_desktop) (a dossier citation) also find that "debt is cheap and reduces these costs" at the deal level. **[Inference]** GP-level leverage already gives ADIC that benefit through look-through, which strengthens the case against adding ADIC-level leverage on top.
- Two papers support the dossier's dry-powder optionality:
  - [Axelson et al.](https://consensus.app/papers/details/74aef73fbf5e56dc86d4d2845cda8f7d/?utm_source=claude_desktop): PE "investments in bad states outperform investments in good states".
  - [Chambers et al.](https://consensus.app/papers/details/3cc939a9b2035c5fb75ebc1b198bb14b/?utm_source=claude_desktop): endowments invested countercyclically at crisis times.
- [Shleifer & Vishny 1992](https://consensus.app/papers/details/fa39990f63685ac6a7cbf5f932b9e7c2/?utm_source=claude_desktop) supports the dossier's NSFR-style rule against funding illiquid assets with short-term debt.
- Two papers support the payout-band and liquidity-gate design:
  - [Broeders et al. (JPEF 2020)](https://consensus.app/papers/details/8b49b3ae1d5757e2841d44d78698c845/?utm_source=claude_desktop): payments and derivative margining create liquidity requirements that shape illiquid allocations.
  - [Gilbert & Hrdlicka](https://consensus.app/papers/details/248d35997763530a9386a6a4059638f2/?utm_source=claude_desktop): a binding payout constraint destroys the buffer-stock role.
- [Jeet et al. (JPM 2026)](https://consensus.app/papers/details/3efa59a891125d279f6eb98f81b48d52/?utm_source=claude_desktop) argue that funding-liquidity risk is orthogonal to factor exposures and needs cash-flow models. This supports the dossier's balance-sheet simulator.

---

## 6. Verbatim usage message

None. No Consensus result in this run contained a sign-up, upgrade or usage message.

---

## 7. Scope notes

- **Not re-searched or not checked.** These entries appear in §2:
  - **Already confirmed by the Stream 01 check:** Boyd et al. (2017); Rockafellar & Uryasev (2000); Cariño et al. (1994); Pereira & Pinto (1991); Ben-Tal et al. (2004). Their URLs are copied from `01_mpo.lit.md`.
  - **Not checked:** Mayne, Seron & Raković (2005); Dowson & Kapelevich (2021).
  - **Out of scope:** the Basel LCR standard, which is regulatory.
- **Consensus record quirks found:**
  - Online-first or working-paper years differ from print years for 7 items: Frazzini–Pedersen, Gorton–Metrick, Sorensen–Wang–Yang, Dimmock–Wang–Yang, Ames et al., Stafford and Nystrup et al.
  - Some records carry SSRN or NBER DOIs on journal articles: Adrian–Shin, Stafford, Dimmock–Wang–Yang and Novy-Marx–Velikov.
  - The Gârleanu–Pedersen record has an NBER venue label on an RFS DOI.
  - The Bohn (AER) record shows the year 2016 for a 1990 article.
  - Author fields are truncated: He & Xiong is shown as "Zhi-Guo He"; *Betting against correlation* is shown under "Andrea Frazzini et al.".
- **Abstract not shown, so no findings claimed.** These are likely relevant to NAV financing and LDI stress calibration and are worth a full-text read:
  - [Pintér (2023), *An Anatomy of the 2022 Gilt Market Crisis*](https://consensus.app/papers/details/1eaf0e7c6cb9564da3739bd8ae4fe0fe/?utm_source=claude_desktop), 29 citations;
  - [Baker (2024), *Net Asset Value Financing and Private Equity*](https://consensus.app/papers/details/f457b903aae95a57844b6cd41904b1d7/?utm_source=claude_desktop);
  - [Reddy (2024), *Private Equity and Net Asset Value Debt*](https://consensus.app/papers/details/dfec35a563a150b0ac00b68fa35ab87d/?utm_source=claude_desktop);
  - [Kodres (2023), *Too Many Cooks, Not Enough Risk Management*](https://consensus.app/papers/details/e29c9c23cda75d86bd89b226764d419c/?utm_source=claude_desktop).
- **Other relevant records, not annotated:**
  - [Chen (IMF WP 2023)](https://consensus.app/papers/details/917a86050f945e1ab7f8422669477b43/?utm_source=claude_desktop) and [Tucker (ARFE 2024)](https://consensus.app/papers/details/4f8ab15c4e5559fd9af85098084030ac/?utm_source=claude_desktop) on lessons from the LDI episode;
  - [Bardoscia et al. (JEDC 2021)](https://consensus.app/papers/details/2ed33ac2bdc9586d98e71535615286bf/?utm_source=claude_desktop): a simulated derivatives VM stress in which liquidity shortfalls can grow as delayed payments spread through the network;
  - [Kuong (RFS)](https://consensus.app/papers/details/9eac915839e3537c84d0453bd058fae1/?utm_source=claude_desktop): self-fulfilling fire sales in collateralized short-term debt, with leverage caps and central clearing as stabilizers;
  - [Cont & Wagalath (Math. Finance 2016)](https://consensus.app/papers/details/e7ee16a2acfb50f497d6e7a1e0c98a03/?utm_source=claude_desktop): fire sales spike realized volatility and correlations, which is relevant to stress-regime parameters;
  - [Aymanns & Farmer (JEDC)](https://consensus.app/papers/details/36e75dfe6ea55ba6bc65ef9f2eab0592/?utm_source=claude_desktop): VaR-driven procyclical leverage produces leverage cycles, and countercyclical rules raise the stable ceiling;
  - [Gerber & Shiu (NAAJ 2003)](https://consensus.app/papers/details/6b9798b6571d53aca67636b999f47d70/?utm_source=claude_desktop): a pension funding band with sponsor contributions and refunds at the barriers, a possible template for the payout band;
  - [Rosen & Sappington (2016)](https://consensus.app/papers/details/44cde5eeef8d56f9ad350569b42f1312/?utm_source=claude_desktop): university leverage decisions follow a pecking order.
- **Overlap with Stream 01.** Stream 01's literature file already covers several leverage-adjacent items, which are not repeated here:
  - PE recommitment (de Zwart et al.);
  - Giommetti & Jørgensen;
  - Cao & van Beek;
  - variation-margin stress (Rousová et al.; Jukonis et al.);
  - intermediary balance-sheet costs (Fleckenstein & Longstaff);
  - the leverage-constraint shadow cost (Lu & Qin).
- **WebSearch (3 queries), metadata only:**
  - *Haircuts:* [NBER w15273](https://www.nber.org/papers/w15273); [RePEc](https://ideas.repec.org/p/nbr/nberwo/15273.html); [FRASER, St. Louis Fed *Review*, Nov/Dec 2010](https://fraser.stlouisfed.org/title/review-federal-reserve-bank-st-louis-820/november-december-2010-620770).
  - *Getmansky–Lo–Makarov:* [MIT author page](https://web.mit.edu/Alo/www/Papers/serialhf.html); [NBER w9571](https://www.nber.org/papers/w9571).
  - *Stafford:* [AQR Insight Award page](https://www.aqr.com/About-Us/AQR-Insight-Award/2016/Replicating-Private-Equity-with-Value-Investing-Homemade-Leverage-and-HoldtoMaturity-Accounting); [HBS Working Knowledge](https://hbswk.hbs.edu/item/replicating-private-equity-with-value-investing-homemade-leverage-and-hold-to-maturity-accounting). The RFS DOI 10.1093/rfs/hhab020 comes from the search tool's summary and was not seen on a primary page. Verify it before external use.
