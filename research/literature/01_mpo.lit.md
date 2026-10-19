# Stream 01 literature check: multi-period portfolio optimization and sequential decision methods

**Dossier checked:** `research/dossiers/01_mpo.md` (v1.0, 71 references).
**Date:** 2026-10-18.
**Search engine:** Consensus. 36 searches, run one at a time with no filters: 23 citation look-ups and 13 topical backfill searches.
**Companion:** `research/verification/01_mpo.verify.md`.

**Reading conventions**
- Findings come from the titles and abstracts that Consensus returned. Full texts were not read.
- **[Inference]** marks our design reasoning where it goes beyond what an abstract states.
- Author lists are shown as Consensus displays them, with "et al." where Consensus truncates.
- Years are the Consensus record year. Where that is the online-first or preprint year, the print year is noted.

---

## 1. Summary

### Citation integrity
- **Scope.** The dossier cites about 63 academic works. I checked **37**: every load-bearing reference behind the L1/L2/L3 architecture, plus every item the dossier itself marked *(unverified)*.
- **Result.** All 37 were found. **0 mismatched, 0 not found, no hallucinated references.**
- **Ten items need metadata fixes or completions:**
  - **Klaassen (2002).** The text cites it as "a published comment", but it is missing from the reference list.
  - **Four items the dossier marked unverified are now resolved:** Pflug & Pichler (2012); Campbell & Viceira (2002); the venue of Calafiore (2008); and the journal, DOI and subtitle of Mohajerin Esfahani & Kuhn.
  - **Dowson's policy-graph paper.** It resolves to *Networks* (2020) under the dossier's own title. The verification log's proposed title change appears to be reversed.
  - **Rockafellar & Uryasev.** Volume 2, pp. 21–41 is confirmed through a citing abstract. The issue number is not.
  - **Bailey et al. (PBO).** Consensus holds only the SSRN version, so the *Journal of Computational Finance* venue remains unconfirmed. I tried one WebSearch to confirm it, but the session's shared web-search budget was used up. No workaround was used.
  - **Brandt et al. (2005).** The RFS record is not in Consensus. Its working-paper precursor is, and two indexed abstracts cite it as RFS 18, 831–873.
  - **Powell, arXiv:1912.03513.** A published chapter version exists (DOI below).

### Backfill (13 topical searches)
The dossier's method base is sound, but it misses ten clusters of work that bear directly on ADIC's design:
1. SDDP with partially observed regimes (PO-SDDP), and evidence comparing Markov-chain with autoregressive SDDP.
2. Complexity results that limit SDDP's practical state dimension.
3. Portfolio-specific information-relaxation bounds, gradient penalties and weakly coupled dynamic-programming relaxations. Together these give the dossier's asset-level price decomposition a valid bound.
4. Private-equity portfolio models from the LP side:
   - recommitment rules;
   - secondary-market pricing of NAV plus unfunded commitments;
   - GP drawdown behaviour.
5. The theory of the shadow cost of illiquidity, which finds the cost is high precisely when illiquidity restricts payouts.
6. Empirical comparisons of scenario-generation methods.
7. Out-of-sample evidence on dynamic versus static policies.
8. Target-range and bPoE (buffered probability of exceedance) objectives.
9. Derivatives inside multistage stochastic programs.
10. The endowment and sovereign-fund spending-policy literature.

### Challenges
Several papers qualify the dossier's recommendations:
- **L2 state dimension.** SDDP's iteration complexity is exponential in state dimension in the worst case. This tempers the plan for a 15–30-state L2.
- **L1 tree pipeline.** Scenario-reduction trees can give biased and unstable solutions, and reduction based on probability metrics underperforms in high dimension.
- **Dynamic policies.** Out-of-sample evidence that long-horizon dynamic strategies beat fixed-mix is mixed, and the value of intertemporal hedging demands is negligible out of sample.
- **Payout arithmetic.** Spending at the expected return erodes a sovereign fund in both probability and expectation. This bears on the "10% target funds a 10% payout" reasoning.
- **Recourse rules and regressions.** Linear decision rules and least-squares Monte Carlo regressions both have documented failure modes.

None of these overturns the three-layer architecture. Several change defaults and add rubric checks (sections 4 and 5).

---

## 2. Citation-integrity table

Status values: found, mismatched or not found. Differences between online-first and print years are not counted as mismatches.

| Dossier citation | Status | Corrected / confirmed metadata (Consensus) | Consensus URL |
|---|---|---|---|
| #49 Luxenberg et al. (2022), *Strategic asset allocation with illiquid alternatives*, arXiv:2207.07767 | found | Consensus indexes the ICAIF '22 proceedings version, DOI 10.1145/3533271.3561769. The abstract matches: random linear system, convex MPC, performance close to a fully liquid benchmark. | [link](https://consensus.app/papers/details/e63add9e25485ea691994d7731b433b1/?utm_source=claude_desktop) |
| #8 Boyd et al. (2017), *Multi-period trading via convex optimization*, FnT Optim. 3(1) | found | DOI 10.1561/2400000023 | [link](https://consensus.app/papers/details/86cb196ea5dc58bba999226d0954af0c/?utm_source=claude_desktop) |
| #9 Boyd, Mueller, O'Donoghue & Wang (2014), *Performance bounds and suboptimal policies for multi-period investment*, FnT Optim. 1(1) | found | Consensus record year 2013; DOI 10.1561/2400000001. The abstract contains the "typically close" wording. | [link](https://consensus.app/papers/details/69b4274bd1bc50dd82122cc1467ba72f/?utm_source=claude_desktop) |
| #56 Nystrup, Boyd, Lindström & Madsen (2019), *Multi-period portfolio selection with drawdown control*, Ann. OR 282 | found | Online 2018; DOI 10.1007/s10479-018-2947-3 | [link](https://consensus.app/papers/details/88b77eb53f2f532483982aba3c5ba5fb/?utm_source=claude_desktop) |
| #61 Powell (2019), *A unified framework for stochastic optimization*, EJOR 275(3) | found | DOI 10.1016/j.ejor.2018.07.014 | [link](https://consensus.app/papers/details/ab76d63d106c536683f1fb197164274c/?utm_source=claude_desktop) |
| #62 Powell, *From reinforcement learning to optimal control…*, arXiv:1912.03513 | found | Consensus links a published version, DOI 10.1007/978-3-030-60990-0_3 (Springer chapter). Add it. | [link](https://consensus.app/papers/details/31595b3009cb5ab2ad57a5acf53709f3/?utm_source=claude_desktop) |
| #58 Pereira & Pinto (1991), *Multi-stage stochastic optimization applied to energy planning*, Math. Prog. 52 | found | DOI 10.1007/bf01582895. The abstract mentions the 39-reservoir case. | [link](https://consensus.app/papers/details/fb85e1a196295794a2ba53f5aef51db2/?utm_source=claude_desktop) |
| #31 Füllner & Rebennack (2025), *SDDP and its variants: a review*, SIAM Rev. 67(3) | found | DOI 10.1137/23m1575093 | [link](https://consensus.app/papers/details/7db5dd5169e35ac19c12c5e823524ce0/?utm_source=claude_desktop) |
| #68 Valladão, Silva & Poggi (2019), Ann. OR 282 | found | Online 2018; DOI 10.1007/s10479-018-2991-z | [link](https://consensus.app/papers/details/9cf93dec2abe56dfa26354d463424a0a/?utm_source=claude_desktop) |
| #60 Philpott & de Matos (2012), EJOR 218(2) | found | DOI 10.1016/j.ejor.2011.10.056 | [link](https://consensus.app/papers/details/7bcb639f52af5a5298f60b6bd44f8d0d/?utm_source=claude_desktop) |
| #45 Kozmík & Morton (2015), Math. Prog. | found | Online 2014; DOI 10.1007/s10107-014-0787-8 | [link](https://consensus.app/papers/details/ba034cb15d615ded9ac6216ca2b0251d/?utm_source=claude_desktop) |
| #70 Zou, Ahmed & Sun (2019), *Stochastic dual dynamic integer programming*, Math. Prog. | found | Online 2018; DOI 10.1007/s10107-018-1249-5. The abstract says the experiments include financial portfolio management. | [link](https://consensus.app/papers/details/c6c1d4d44d1c5e2cbd03660d44cad25a/?utm_source=claude_desktop) |
| #25 Dowson, *The policy graph decomposition of multistage stochastic programming problems* (preprint; journal unverified) | found | *Networks* (2020), DOI 10.1002/net.21932, under the **dossier's title** ("…programming problems"). The 2018 preprint record is titled "…optimization problems" ([link](https://consensus.app/papers/details/ae3bfdedb32f50d982e6108cbe0f782f/?utm_source=claude_desktop)). Keep the dossier's title. The verification log's retitling appears reversed. | [link](https://consensus.app/papers/details/8ce7e05fa5bc5e38849108e50d33276e/?utm_source=claude_desktop) |
| #1 Ang, Papanikolaou & Westerfield (2014), MS 60(11) | found | DOI 10.1287/mnsc.2014.1986 | [link](https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop) |
| #23 Dimmock, Wang & Yang (2024), MS 70(3) | found | The Consensus record shows year 2019 with the NBER DOI 10.3386/w25559 and venue *Manag. Sci.* The abstract cites the MS supplement DOI 10.1287/mnsc.2023.4759, consistent with the dossier. | [link](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop) |
| #10 Brandt, Goyal, Santa-Clara & Stroud (2005), RFS 18(3) | found (working-paper record) | Consensus has only the 2001 SSRN precursor, *Dynamic Portfolio Choice: A Simulation Approach* (DOI 10.2139/ssrn.271188). Two indexed abstracts cite the article as RFS 18, 831–873 (2005): [van Binsbergen & Brandt 2007](https://consensus.app/papers/details/ec54684eaa9e556f9440ad9c4f5783d5/?utm_source=claude_desktop) and [Detemple et al. 2007](https://consensus.app/papers/details/6ab73322c47e5d2a9fab362afd09fad1/?utm_source=claude_desktop). | [link](https://consensus.app/papers/details/72b6fdc64bbc5a06b87efccaa5ebe7aa/?utm_source=claude_desktop) |
| #11 Brown, Smith & Sun (2010), OR 58(4) | found | DOI 10.1287/opre.1090.0796 | [link](https://consensus.app/papers/details/3f70ae2e398c524592d67076b594acd0/?utm_source=claude_desktop) |
| #39 Haugh, Kogan & Wang (2006), OR 54(3) | found | DOI 10.1287/opre.1060.0279 | [link](https://consensus.app/papers/details/74166a30536a557ab9b0931ed85eef83/?utm_source=claude_desktop) |
| #32 Gârleanu & Pedersen (2013), JF 68(6) | found | DOI 10.1111/jofi.12080 | [link](https://consensus.app/papers/details/a1d18543c1ef5cf6b0b4179f31e2a44b/?utm_source=claude_desktop) |
| #44 Kouwenberg (2001), EJOR 134(2) | found | DOI 10.1016/s0377-2217(00)00261-7. "Could be improved drastically" is in the abstract. | [link](https://consensus.app/papers/details/6189d2de3bb559f69ad7e1576d594bd5/?utm_source=claude_desktop) |
| #41 Høyland & Wallace (2001), MS 47(2) | found | DOI 10.1287/mnsc.47.2.295.9834 | [link](https://consensus.app/papers/details/a33c1b9eaddc5e95b676dc56bc00a1ad/?utm_source=claude_desktop) |
| §3.1 text, "a published comment" (missing from the reference list) | found | Klaassen, P. (2002), *Comment on "Generating Scenario Trees for Multistage Decision Problems"*, Management Science, DOI 10.1287/mnsc.48.11.1512.261. **Add to references.** | [link](https://consensus.app/papers/details/a8d98491955d57858f98c0a0232dd32a/?utm_source=claude_desktop) |
| #28 Fleten, Høyland & Wallace (2002), EJOR 140(1) | found | DOI 10.1016/s0377-2217(01)00195-3 | [link](https://consensus.app/papers/details/16752e94781a54349e3700a65a1219bc/?utm_source=claude_desktop) |
| #19 Cariño et al. (1994), *The Russell-Yasuda Kasai model*, Interfaces 24(1) | found | DOI 10.1287/inte.24.1.29. The full title adds ": An Asset/Liability Model for a Japanese Insurance Company Using Multistage Stochastic Programming". | [link](https://consensus.app/papers/details/1f457f819115540d83c7b7d4289b0b66/?utm_source=claude_desktop) |
| #20 Cariño & Ziemba (1998), OR 46(4) | found | DOI 10.1287/opre.46.4.433. The abstract confirms the 5-year horizon plus a steady-state end-effects period and the penalty costs for constraint violations. | [link](https://consensus.app/papers/details/b26c5bff42ae50c5b845842b3b0c1506/?utm_source=claude_desktop) |
| #22 Dantzig & Infanger (1993), Ann. OR 45 | found | DOI 10.1007/bf02282041 | [link](https://consensus.app/papers/details/05fab9cd71365553b46839ee85d3b764/?utm_source=claude_desktop) |
| #6 Ben-Tal, Goryashko, Guslitzer & Nemirovski (2004), Math. Prog. 99(2) | found | DOI 10.1007/s10107-003-0454-y | [link](https://consensus.app/papers/details/ce4bf774291b55cabf5e91b522ffb2c8/?utm_source=claude_desktop) |
| #46 Kuhn, Wiesemann & Georghiou (2011), Math. Prog. 130(1) | found | DOI 10.1007/s10107-009-0331-4 | [link](https://consensus.app/papers/details/4cf363d17bb358dba655361d9f7a7d12/?utm_source=claude_desktop) |
| #33 Georghiou, Kuhn & Wiesemann (2019), CMS 16(4) | found | Online 2018; DOI 10.1007/s10287-018-0338-5 | [link](https://consensus.app/papers/details/c37a3569894d532d8f666b65da2c8455/?utm_source=claude_desktop) |
| #14 Calafiore (2008), *Multi-period portfolio optimization with linear control policies* (venue unverified) | found | *Automatica* confirmed; DOI 10.1016/j.automatica.2008.02.007. Volume and pages are not shown by Consensus. | [link](https://consensus.app/papers/details/61237b5f6ac150e1992041fc8370a21e/?utm_source=claude_desktop) |
| #59 Pflug & Pichler (2012), *A distance for multistage stochastic optimization models* (unverified) | found | SIAM J. Optim., DOI 10.1137/110825054. Vol. 22, pp. 1–23 per a citing abstract ([Analui & Pflug 2014](https://consensus.app/papers/details/96c87e89f23256d3a671a40ae08d6a44/?utm_source=claude_desktop)). | [link](https://consensus.app/papers/details/198ce73368485a5180014bb46e03881d/?utm_source=claude_desktop) |
| #53 Mohajerin Esfahani & Kuhn, arXiv:1505.05116 (journal unverified, no year) | found | *Mathematical Programming*, DOI 10.1007/s10107-017-1172-1. Full title: "…using the Wasserstein metric: performance guarantees and tractable reformulations". The Consensus author field shows only "D. Kuhn" and the record year 2015 (preprint), both record artefacts. | [link](https://consensus.app/papers/details/955158b8081d595c9c09458e32f6c2c0/?utm_source=claude_desktop) |
| #63 Rockafellar & Uryasev (2000), *Optimization of conditional value-at-risk*, J. Risk 2(3) (volume and pages "from memory") | found | J. Risk, DOI 10.21314/jor.2000.038. Vol. 2, pp. 21–41 per a citing abstract ([Beliakov & Bagirov 2006](https://consensus.app/papers/details/423e0238bd8a5347a1d10adf1e117ba6/?utm_source=claude_desktop)). Issue number not confirmed. The abstract text attached to the Consensus record belongs to a different paper (record error). | [link](https://consensus.app/papers/details/a500ccf654ae5205a70fe138eb0d82d7/?utm_source=claude_desktop) |
| #16 Campbell & Viceira (2002), *Strategic Asset Allocation* (unverified) | found | Oxford University Press, DOI 10.1093/0198296940.001.0001 | [link](https://consensus.app/papers/details/fbff03a0440e50618cc2df48b7009907/?utm_source=claude_desktop) |
| #4 Bailey, Borwein, López de Prado & Zhu (2017), *The probability of backtest overfitting*, J. Comput. Finance (unverified) | found (SSRN version) | Consensus has a 2016 SSRN record, DOI 10.2139/ssrn.2326253, which matches the dossier's URL. The journal venue and year cannot be resolved in Consensus, and WebSearch was unavailable, so the venue is still **unconfirmed**. | [link](https://consensus.app/papers/details/f5ef21e8509b544fba76ccc9aa2de55c/?utm_source=claude_desktop) |
| #36 Hambly, Xu & Yang (2023), Math. Finance 33(3) | found | Online 2021; DOI 10.1111/mafi.12382 | [link](https://consensus.app/papers/details/fb3dec1d4e3259f3ab893fad34216b32/?utm_source=claude_desktop) |
| #18 Cao & van Beek (2025), *A latent factor cash flow model for alternative investment funds*, FAJ 81(3) | found | FAJ, DOI 10.1080/0015198x.2025.2489923. Consensus gives the first author as "Wenbo Cao" (the verification log wrote "Wen Cao"). The abstract matches: Takahashi–Alexander extension with systematic factors, stress testing, commitment design. | [link](https://consensus.app/papers/details/bb74f63a8fc15983a1e7753d4057d4f0/?utm_source=claude_desktop) |

---

## 3. Annotated bibliography (25 papers)

In each entry, "In dossier" states whether the dossier already cites the paper. Most entries are missed papers. Four dossier citations are kept here as anchors.

**1. [Large-scale financial planning via a partially observable stochastic dual dynamic programming framework](https://consensus.app/papers/details/9e40ee775ba15434888d552a046a6c09/?utm_source=claude_desktop)**
- Jinkyu Lee et al. · 2023 · *Quantitative Finance* · 7 citations · DOI 10.1080/14697688.2023.2221296 · In dossier: no
- *Finding:* The authors identify stagewise independence as the main obstacle to using SDDP for financial planning. They propose PO-SDDP, which models uncertainty as discrete, partially observable Markov states and adds feasibility cuts.
- *Relevance to ADIC:* L2 indexes cuts by regime *j* as if the regime were known, but ADIC's regime is an HMM/HSMM posterior. **[Inference]** PO-SDDP, or a belief-state policy graph, is the formulation that matches. Feasibility cuts suit the hard liquidity constraints.

**2. [Modeling time-dependent randomness in stochastic dual dynamic programming](https://consensus.app/papers/details/889e982ca4c8514ea4b791ce145b8493/?utm_source=claude_desktop)**
- N. Löhndorf et al. · 2019 · *EJOR* · 90 citations · DOI 10.1016/j.ejor.2018.08.001 · In dossier: no
- *Finding:* On Brazil's power system, Markov-chain SDDP closed its bounds faster than the autoregressive (TS-SDDP) formulation, and its policy dominated. On real data, model quality also mattered, and an AV@R formulation made the policy robust to a misspecified stochastic model.
- *Relevance to ADIC:* This is empirical support for the dossier's Markov-chain L2. **[Inference]** It also argues for an AV@R variant as a cheap hedge against generator misspecification (the result transfers from hydro to finance only by analogy).

**3. [Stochastic dual dynamic programming for multistage stochastic mixed-integer nonlinear optimization](https://consensus.app/papers/details/c3bb3cbfbd5f58858b54e03033005617/?utm_source=claude_desktop)**
- Shixuan Zhang et al. · 2019 (record; the DOI indicates 2022) · *Mathematical Programming* · 46 citations · DOI 10.1007/s10107-022-01875-8 · In dossier: no
- *Finding:* For *d*-dimensional states, the iterations needed for an ε-optimal solution are bounded above by O((2LT/ε)^d). They are bounded below by O((LT/4ε)^d) in general and by O((LT/8ε)^{d/2−1}) in the convex case, while growing only polynomially in the number of stages.
- *Relevance to ADIC:* This is the theoretical counterweight to the dossier's claim that SDDP "handles state dimensions in the tens" with 15–30 L2 states. It is a worst-case result: Valladão et al. (entry 5) solved a 100-asset problem in practice.

**4. [Complexity of stochastic dual dynamic programming](https://consensus.app/papers/details/0cf847831a025cc281826e46c115e58d/?utm_source=claude_desktop)**
- Guanghui Lan · 2019 (record; the DOI indicates 2020) · *Mathematical Programming* · 41 citations · DOI 10.1007/s10107-020-01567-1 · In dossier: no
- *Finding:* SDDP's complexity grows only mildly with the number of stages, linearly for discounted problems. It is therefore efficient for problems with many stages and relatively few decision variables per stage.
- *Relevance to ADIC:* It supports a 40-quarter L2 and reinforces the need for an aggressively aggregated per-stage state.

**5. [Time-consistent risk-constrained dynamic portfolio optimization with transactional costs and time-dependent returns](https://consensus.app/papers/details/9cf93dec2abe56dfa26354d463424a0a/?utm_source=claude_desktop)**
- D. Valladão et al. · 2018 (print 2019) · *Annals of Operations Research* · 30 citations · DOI 10.1007/s10479-018-2991-z · In dossier: **yes (#68)**
- *Finding:* The paper solves a Markov-chain SDDP model with one-period CVaR constraints. Unlike dynamic risk measures in the objective, the model has relatively complete recourse and a straightforward lower bound. It is near-optimal on a 100-asset, 5-factor problem.
- *Relevance to ADIC:* It is the best template for L2. **[Inference]** Per-period CVaR constraints, rather than a nested risk objective, keep SDDP's bound valid (the dossier's SDDP.jl caveat) and help with verification issue R6 (relatively complete recourse).

**6. [On Solving Multistage Stochastic Programs with Coherent Risk Measures](https://consensus.app/papers/details/ad91661921665c598fb1b5e3a76299cb/?utm_source=claude_desktop)**
- A. Philpott et al. · 2013 · *Operations Research* · 145 citations · DOI 10.1287/opre.2013.1175 · In dossier: no
- *Finding:* An inner approximation of the future cost functions gives an upper bound on the cost of an optimal risk-averse policy, and an outer approximation gives a lower bound. Both can be used inside SDDP.
- *Relevance to ADIC:* It addresses the missing bound under risk aversion, flagged in dossier §3.2 and verification issue R9, for any risk-averse L2 variant. See also [dual SDDP for risk-averse programs](https://consensus.app/papers/details/bcf8f37a8e1250bf9c30decc8629b3af/?utm_source=claude_desktop) (deterministic upper bounds).

**7. [Dynamic Portfolio Optimization with Transaction Costs: Heuristics and Dual Bounds](https://consensus.app/papers/details/4ea8b439c29a59fdb15efeefe4be19c5/?utm_source=claude_desktop)**
- David B. Brown et al. · 2011 · *Management Science* · 172 citations · DOI 10.1287/mnsc.1110.1377 · In dossier: no
- *Finding:* Simple heuristics derived from simpler models are paired with information-relaxation upper bounds: perfect foresight plus a penalty, evaluated by Monte Carlo. With 3 or 10 risky assets, the heuristics are often very close to the bound.
- *Relevance to ADIC:* This is a portfolio application of the bounds the dossier cites only in general form (Brown, Smith & Sun 2010; Haugh, Kogan & Wang 2006). It is a direct template for L3's gap certificate.

**8. [Information Relaxations, Duality, and Convex Stochastic Dynamic Programs](https://consensus.app/papers/details/3b9b32a6560f512781bd69b9a6881290/?utm_source=claude_desktop)**
- David B. Brown et al. · 2014 · *Operations Research* · 61 citations · DOI 10.1287/opre.2014.1322 · In dossier: no
- *Finding:* Gradient penalties built from approximate value functions turn the perfect-information subproblems into deterministic convex programs. They can give tight bounds and improve on Lagrangian bounds.
- *Relevance to ADIC:* **[Inference]** The slopes of L2's SDDP cuts are natural gradient penalties. Each L3 path's dual problem then becomes a deterministic LP, so L3 can compute its gap certificate natively within the architecture.

**9. [Relaxations of Weakly Coupled Stochastic Dynamic Programs](https://consensus.app/papers/details/80a57bb0dc385a61b01ce4b8ac352bfd/?utm_source=claude_desktop)**
- Daniel Adelman et al. · 2008 · *Operations Research* · 226 citations · DOI 10.1287/opre.1070.0445 · In dossier: no
- *Finding:* The paper treats subproblems linked only by coupling constraints on actions. It fits additively separable value-function approximations by Lagrangian relaxation and by the LP approach to ADP, and compares both with each other and with the optimal value.
- *Relevance to ADIC:* About 300 positions linked through the cash constraint form exactly such a weakly coupled program. **[Inference]** This gives the dossier's price decomposition across assets (§3.3) a bound-backed basis, replacing the Shapley–Folkman argument that the verification log rejected (R7). See also [information plus Lagrangian relaxations for weakly coupled programs](https://consensus.app/papers/details/770c1979bd04545f95020fceeb9ef4fb/?utm_source=claude_desktop), whose bound is uniform in the number of subproblems.

**10. [Parametric Portfolio Policies: Exploiting Characteristics in the Cross Section of Equity Returns](https://consensus.app/papers/details/d764d9977ca95514bf5676342353a7ae/?utm_source=claude_desktop)**
- Michael W. Brandt et al. · 2009 · *Review of Financial Studies* · 438 citations · DOI 10.1093/rfs/hhp003 · In dossier: no
- *Finding:* Portfolio weights are modelled directly as functions of asset characteristics, with coefficients chosen to maximize average realized utility. The method is simple and robust in and out of sample compared with modelling the joint return distribution.
- *Relevance to ADIC:* It is the finance precedent for L3's parametric policy tuning. **[Inference]** Parameterize commitments and SELL/LEVER thresholds directly on the underwritten/actual/forecast return marks and group signals, rather than routing everything through full distributional forecasts.

**11. [Strategic Asset Allocation with Illiquid Alternatives](https://consensus.app/papers/details/e63add9e25485ea691994d7731b433b1/?utm_source=claude_desktop)**
- Eric Luxenberg et al. · 2022 · *Proc. 3rd ACM ICAIF* · 4 citations · DOI 10.1145/3533271.3561769 · In dossier: **yes (#49)**
- *Finding:* Illiquid dynamics are modelled as a random linear system. A convex MPC policy for liquid allocations and new commitments comes surprisingly close to a fictional fully liquid benchmark. The paper treats the growth problem only, with no liabilities, but says the extension is ready.
- *Relevance to ADIC:* It is L3's benchmark and transition model. The payout obligation is precisely the untested extension, and the verification log flags calibration inconsistencies (R4).

**12. [Private Equity Recommitment Strategies for Institutional Investors](https://consensus.app/papers/details/63deabfca2f15e65880fa9a8f5d03a13/?utm_source=claude_desktop)**
- G. D. de Zwart et al. · 2012 · *Financial Analysts Journal* · 13 citations · DOI 10.2469/faj.v68.n3.1 · In dossier: no
- *Finding:* New commitments equal distributions received plus uncalled capital, scaled by the ratio of target to current allocation. In simulations on 1980–2005 data the rule reached 86% of target with an 8% probability of being overinvested. The build-up phase needed about 30% overcommitment, and about 10% of committed capital was never called.
- *Relevance to ADIC:* It is a ready-made, explainable baseline rule for commitment pacing in L3. **[Inference]** Its parameters give priors for the pacing parameter κ and for commitment multipliers. They are not ADIC data.

**13. [Optimal Allocation to Private Equity](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop)**
- Nicola Giommetti et al. · 2021 · SSRN working paper · 5 citations · DOI 10.2139/ssrn.3761243 · In dossier: no
- *Finding:* An LP repeatedly commits to PE funds whose capital is called and later distributed. PE materially changes optimal allocations, and the PE share is not monotone in risk aversion. An extension with a secondary market prices both NAV and unfunded liabilities.
- *Relevance to ADIC:* It supplies SELL economics. **[Inference]** The secondary discount should depend on the stake's unfunded/NAV ratio as well as on the regime, consistent with the dossier's continuation value CV_i netting future calls.

**14. [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop)**
- Vincent Maurin et al. · 2022 · *Management Science* · 8 citations · DOI 10.1287/mnsc.2022.4612 · In dossier: no
- *Finding:*
  - Sequential capital calls solve the GP's moral-hazard problem but expose LPs to illiquidity.
  - Illiquidity-tolerant LPs earn higher returns.
  - GPs may accelerate drawdowns to avoid LP default.
  - A secondary market narrows differences in fund returns but not in LP returns.
- *Relevance to ADIC:* **[Inference]** Call intensities can rise exactly when LPs are stressed, which strengthens the case for stress-coupled calls. ADIC's illiquidity tolerance is itself a return source that the liquidity gate protects.

**15. [The Shadow Costs of Illiquidity](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop)**
- Kristy A. E. Jansen et al. · 2022 · *JFQA* · 3 citations · DOI 10.1017/s0022109022000473 · In dossier: no
- *Finding:* Illiquidity that only distorts asset allocation has low shadow costs. Costs are high when illiquidity restricts consumption, and so are high for investors who face large liquidity shocks or want a large illiquid share.
- *Relevance to ADIC:* The 5–10% mandated payout is the "consumption" channel. **[Inference]** The cash dual λ should spike mainly where payouts and calls bind. The IC's shadow-cost table should break λ down by binding constraint.

**16. [Margin-Based Asset Pricing and Deviations from the Law of One Price](https://consensus.app/papers/details/c5d81d132abf5d118a3a62c20200c195/?utm_source=claude_desktop)**
- Nicolae Gârleanu et al. · 2011 · Consensus venue "NBER"; the DOI indicates *RFS* · 663 citations · DOI 10.1093/rfs/hhr027 · In dossier: no
- *Finding:* Margin constraints bind after negative shocks. The resulting basis depends on the shadow cost of capital, which can be captured by the spread between collateralized and uncollateralized loans.
- *Relevance to ADIC:* **[Inference]** This gives an observable market proxy against which to check ADIC's implied liquidity rate ρ and Treasury's funds-transfer-pricing curve. It is also a candidate regime feature.

**17. [Scenario tree generation and multi-asset financial optimization problems](https://consensus.app/papers/details/3116632fca3a5358a2b66101b6f6aa5d/?utm_source=claude_desktop)**
- Alois L. J. Geyer et al. · 2013 · *Operations Research Letters* · 18 citations · DOI 10.1016/j.orl.2013.06.003 · In dossier: no
- *Finding:* On a problem with a known analytic solution, moment matching plus an arbitrage check reproduces the solution precisely. Scenario-reduction trees, even when arbitrage-free, give biased and highly variable solutions.
- *Relevance to ADIC:* It challenges L1's reduction step (regime-stratified k-medoids). **[Inference]** Make moment matching with Klaassen's arbitrage check the primary method and keep clustering as a challenger.

**18. [An empirical analysis of scenario generation methods for stochastic optimization](https://consensus.app/papers/details/3705d75ee7385a15936f6937cdae08af/?utm_source=claude_desktop)**
- N. Löhndorf · 2016 · *EJOR* · 102 citations · DOI 10.1016/j.ejor.2016.05.021 · In dossier: no
- *Finding:* Voronoi cell sampling gave the lowest errors, especially for heavy tails, including under a CVaR objective. The paper reports evidence that methods minimizing probability metrics are ineffective under high-dimensional randomness.
- *Relevance to ADIC:* L1's uncertainty is high-dimensional: returns, marks, calls, distributions, spreads and variation margin. **[Inference]** Add Voronoi cell sampling as a generator and do not rely only on metric-based reduction, including the nested-distance reduction the dossier endorses.

**19. [From Empirical Observations to Tree Models for Stochastic Optimization: Convergence Properties](https://consensus.app/papers/details/6ca73942bd8e503ab1dda52f20fe2d98/?utm_source=claude_desktop)**
- G. Pflug et al. · 2016 · *SIAM J. Optim.* · 57 citations · DOI 10.1137/15m1043376 · In dossier: no
- *Finding:* When the law has a density, the empirical measure built from sample paths does not converge in nested distance. Kernel-smoothed versions do converge.
- *Relevance to ADIC:* **[Inference]** Building the L1 tree by clustering 50,000 simulated paths is an empirical path construction. Branches should be drawn from conditional distributions, or smoothed, so that the tree represents the information structure.

**20. [Can long-run dynamic optimal strategies outperform fixed-mix portfolios? Evidence from multiple data sets](https://consensus.app/papers/details/ca2f60c16bdb54f892e81d42b625549c/?utm_source=claude_desktop)**
- Daniele Bianchi et al. · 2013 (record; the DOI indicates 2014) · *EJOR* · 11 citations · DOI 10.1016/j.ejor.2014.01.030 · In dossier: no
- *Finding:* In-sample, optimal long-horizon dynamic weights differ enormously from the mean-variance benchmark. Out of sample there is no clear-cut, systematic outperformance of naive diversification (frictionless HARA setting, five data sets).
- *Relevance to ADIC:* It qualifies the dossier's evidence that stochastic programming dominates fixed-mix, which rests on simulation. Counter-evidence appears in section 5.

**21. [Long-Term Strategic Asset Allocation: An Out-of-Sample Evaluation](https://consensus.app/papers/details/508f632144295e13b57ad0c444d846c1/?utm_source=claude_desktop)**
- Bart Diris et al. · 2015 · *Management Science* · 32 citations · DOI 10.1287/mnsc.2014.1924 · In dossier: no
- *Finding:* Out of sample, a myopic market-timing strategy performed almost identically to the dynamic one. The value of intertemporal hedging demands appears negligible, because it depends on predicting the predictors.
- *Relevance to ADIC:* It challenges dossier §2.2's claim that time-varying opportunities are a first-order source of horizon effects. **[Inference]** Payout obligations and illiquidity frictions should carry the multi-period machinery, not return predictability.

**22. [Multiperiod Mean-Buffered Probability of Exceedance in Defined Contribution Portfolio Optimization](https://consensus.app/papers/details/50e851a2565f56639dabd7b0045072f5/?utm_source=claude_desktop)**
- D. Dang et al. · 2025 · *SIAM J. Financial Mathematics* · 5 citations · DOI 10.1137/25m1764773 · In dossier: no
- *Finding:* The paper uses bPoE as a dollar-based alternative to CVaR. Time-consistent mean-bPoE policies resemble their precommitment counterparts and respect a minimum acceptable wealth, whereas time-consistent mean-CVaR "often leads to counterintuitive control behavior".
- *Relevance to ADIC:* **[Inference]** bPoE of the 7% floor and of the liquidity-coverage (LCR) shortfall is a convex surrogate calibrated to the breach probability the IC reads. It may also sidestep verification issue R5 (a CVaR ≤ 0 constraint on a non-negative shortfall).

**23. [A stochastic programming model for dynamic portfolio management with financial derivatives](https://consensus.app/papers/details/09d2998dfe0355d5a7900dbca2e5754e/?utm_source=claude_desktop)**
- Diana Barro et al. · 2022 · *Journal of Banking & Finance* · 21 citations · DOI 10.1016/j.jbankfin.2022.106445 · In dossier: no
- *Finding:* A multistage stochastic program includes OTC equity options and a VIX ETF, with arbitrage-free scenarios generated for both returns and option prices and a wealth–CVaR objective solved as an LP. Options strengthen tail-risk control. Options plus VIX improved risk-adjusted returns in and out of sample.
- *Relevance to ADIC:* It is the template for representing the tail-hedge overlay explicitly at L1 nodes, instead of valuing it only through shadow prices. See also [pension stochastic programming with put options, stochastic-dominance constraints and nodal contamination](https://consensus.app/papers/details/fe7dc9c3e32e5f6b801e03656280c570/?utm_source=claude_desktop).

**24. [Optimal chance-constrained pension fund management through dynamic stochastic control](https://consensus.app/papers/details/499dbe03567f574f8a2749df30f4f669/?utm_source=claude_desktop)**
- D. Lauria et al. · 2022 · *OR Spectrum* · 6 citations · DOI 10.1007/s00291-022-00673-0 · In dossier: no
- *Finding:* The paper combines an open-loop linear-feedback policy with a chance constraint on the funding ratio, solved as a QP. Continuous risk distributions are kept. The approach avoids the curse of dimensionality, in-sample instability and approximation error typical of multistage SP, and is validated in and out of sample.
- *Relevance to ADIC:* **[Inference]** It offers a tree-free cross-check of L1's liquidity and floor chance constraints within the dossier's decision-rule family.

**25. [The Emperor Has No Cash Flows: Integrating Cash Flow Dynamics into Total Portfolio Approach](https://consensus.app/papers/details/3efa59a891125d279f6eb98f81b48d52/?utm_source=claude_desktop)**
- Vishv Jeet et al. · 2026 · venue not named by Consensus (DOI prefix 10.3905/jpmi) · 0 citations · DOI 10.3905/jpmi.2026.003 · In dossier: no
- *Finding:* Factor models measure NAV volatility and exposures but not capital risk or funding liquidity risk (calls relative to liquid reserves). Cash-flow models must drive commitment pacing, liquidity management and allocation sizing. Factor models stay useful for liquid sleeves, direct deals and attribution.
- *Relevance to ADIC:* It is practitioner support for the dossier's cash-flow-state design within a TPA. **[Inference]** Split the work: the return-fusion and factor engine serves liquid sleeves and co-investments, and a cash-flow model of the Cao–van Beek type serves fund interests.

---

## 4. Missed-but-important papers: design implications

### 4.1 State variables

- **Make the regime a belief, not a label.**
  - Add the regime posterior, or a discretized belief grid, to the L2 state. This is the [PO-SDDP](https://consensus.app/papers/details/9e40ee775ba15434888d552a046a6c09/?utm_source=claude_desktop) formulation.
  - For L3, information-relaxation bounds extend to partially observed problems, and "in general, the belief-state formulation provides tighter bounds" ([Haugh et al., IEEE TAC 2020](https://consensus.app/papers/details/3e0beb4607e857dca9b8711db5c32a45/?utm_source=claude_desktop)).
  - **[Inference]** Compute L3's gap in belief space.
- **Add a latent private-markets cash-flow factor.**
  - [Cao & van Beek (2025)](https://consensus.app/papers/details/bb74f63a8fc15983a1e7753d4057d4f0/?utm_source=claude_desktop) put systematic factors into call and distribution rates.
  - [Feng (2026)](https://consensus.app/papers/details/a6ba45ba559453a78fe55e3f03919cff/?utm_source=claude_desktop) describes a "same-direction cash-flow squeeze", in which distributions fall while calls concentrate. This is a lower-tier venue; use it for intuition only.
  - **[Inference]** One latent factor should jointly drive λ⁰, λ¹ and δ beyond the regime label. This puts dossier risk #5 (coupled stress) directly into the transition.
- **Pacing-rule inputs.** [de Zwart et al. (2012)](https://consensus.app/papers/details/63deabfca2f15e65880fa9a8f5d03a13/?utm_source=claude_desktop) condition on distributions received, uncalled capital and current/target allocation. **[Inference]** Expose these at group level to the L3 policies.
- **Make the secondary-sale state depend on the unfunded share.** [Giommetti & Jørgensen](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop) price NAV and unfunded liabilities separately. **[Inference]** The discount δ^sec should depend on the unfunded/NAV ratio as well as on the regime and the volume sold.
- **Add observable funding-cost proxies to the information state I_t.** **[Inference]** These are plausibility anchors from other investor types, not ADIC calibration:
  - the collateralized versus uncollateralized spread ([Gârleanu & Pedersen 2011](https://consensus.app/papers/details/c5d81d132abf5d118a3a62c20200c195/?utm_source=claude_desktop));
  - intermediary balance-sheet costs of 81 bp on average and above 200 bp in crises ([Fleckenstein & Longstaff](https://consensus.app/papers/details/d645b98807705ad284aa783668911531/?utm_source=claude_desktop));
  - a leverage-constraint shadow cost averaging 0.56% a year, with spikes at quarter-ends ([Lu & Qin](https://consensus.app/papers/details/0ea626fa694a50f2ad7e32baa61755e1/?utm_source=claude_desktop)).

### 4.2 Models

**L2 (strategic values)**
- **Keep the Markov-chain discretization.** [Löhndorf & Shapiro](https://consensus.app/papers/details/889e982ca4c8514ea4b791ce145b8493/?utm_source=claude_desktop) found it closes bounds faster and dominates autoregressive SDDP. **[Inference]** Add an AV@R run as a misspecification hedge.
- **Robust variants.** **[Inference]** ADIC's private-market histories are short, so a distributionally robust L2 is the natural way to formalize the dossier's model set 𝓜. Candidates:
  - [distributionally robust SDDP](https://consensus.app/papers/details/6e12c9c7298c5d6782743f1a2db25124/?utm_source=claude_desktop);
  - [nested-distance DRO solved by SDDP](https://consensus.app/papers/details/f1e70ef1b4fe54d8911587ca8aba2894/?utm_source=claude_desktop), applied to dynamic portfolio selection with "superior out-of-sample performance";
  - [data-driven Wasserstein multistage models](https://consensus.app/papers/details/47229517dbe65539ad4b18d0bdc6d356/?utm_source=claude_desktop), which "could outperform" risk-neutral and risk-averse multistage stochastic models "when the data size is small".
- **State dimension.** **[Inference]** Choose L2's dimension by convergence diagnostics. Start with about 10 aggregated states and add states only while the bound gap still closes. Evidence:
  - The theory bounds are exponential in *d* ([Zhang & Sun](https://consensus.app/papers/details/c3bb3cbfbd5f58858b54e03033005617/?utm_source=claude_desktop); [Lan](https://consensus.app/papers/details/0cf847831a025cc281826e46c115e58d/?utm_source=claude_desktop); [Neural SDDP](https://consensus.app/papers/details/b1824f8bea20522c9cd665e2eb4405ab/?utm_source=claude_desktop) notes the same worst case).
  - [Quadratic regularization](https://consensus.app/papers/details/d657c301378e5fd8815df6b4ee3820a8/?utm_source=claude_desktop) gives larger speed-ups in higher-dimensional problems with Markov uncertainty.
- **Valid bounds under risk aversion.** Options:
  - one-period CVaR constraints ([Valladão et al.](https://consensus.app/papers/details/9cf93dec2abe56dfa26354d463424a0a/?utm_source=claude_desktop)), which keep a straightforward lower bound;
  - inner approximations ([Philpott et al. 2013](https://consensus.app/papers/details/ad91661921665c598fb1b5e3a76299cb/?utm_source=claude_desktop));
  - [dual SDDP](https://consensus.app/papers/details/bcf8f37a8e1250bf9c30decc8629b3af/?utm_source=claude_desktop).
- **Payout and goal structures already solved by SDDP:**
  - [constrained consumption–investment via SDDP](https://consensus.app/papers/details/36b5bb700ca25966a8352ded3b2f4618/?utm_source=claude_desktop), benchmarked against a closed form;
  - [goal tracking with Markov-regime returns over 28 periods](https://consensus.app/papers/details/da0c7b8cecbb51b58e3552e0117600be/?utm_source=claude_desktop).
  - **[Inference]** Use them as regression tests for L2's distribution decision.

**L1 (here-and-now program)**
- **Tree construction.** **[Inference]** Draw branches from conditional distributions, or use Voronoi cell sampling. Then match moments, check for arbitrage ([Klaassen 2002](https://consensus.app/papers/details/a8d98491955d57858f98c0a0232dd32a/?utm_source=claude_desktop)), and run k-medoids trees only as out-of-sample challengers. Evidence: [Geyer et al.](https://consensus.app/papers/details/3116632fca3a5358a2b66101b6f6aa5d/?utm_source=claude_desktop), [Löhndorf 2016](https://consensus.app/papers/details/3705d75ee7385a15936f6937cdae08af/?utm_source=claude_desktop) and [Pflug & Pichler 2016](https://consensus.app/papers/details/6ca73942bd8e503ab1dda52f20fe2d98/?utm_source=claude_desktop).
- **Path-based alternatives to a 1×40×25 tree:**
  - [CVaR-constrained ALM on sample paths](https://consensus.app/papers/details/bf554cdfae01541ba4cf2638a93de749/?utm_source=claude_desktop) shares decisions across groups of paths, so problem size grows linearly rather than exponentially;
  - [hybrid simulation/tree models](https://consensus.app/papers/details/581c90a41442552bbe22688e94cba74a/?utm_source=claude_desktop) evaluate and control risk better than pure trees;
  - [SDDP embedded in scenario trees](https://consensus.app/papers/details/44ed80de0ea85bf8a87f94c21134b6f8/?utm_source=claude_desktop) is a third option.
  - **[Inference]** Bundles formed non-anticipatively avoid the clairvoyance problem of fans and scale better at 12 quarters.
- **Tree-free cross-check.** Chance-constrained linear-feedback control ([Lauria et al.](https://consensus.app/papers/details/499dbe03567f574f8a2749df30f4f669/?utm_source=claude_desktop)).
- **Overlay inside L1.** Represent tail-hedge options per node with arbitrage-free prices ([Barro et al.](https://consensus.app/papers/details/09d2998dfe0355d5a7900dbca2e5754e/?utm_source=claude_desktop)), and stress-test with nodal contamination ([Moriggia et al.](https://consensus.app/papers/details/fe7dc9c3e32e5f6b801e03656280c570/?utm_source=claude_desktop)).

**L3 (policy simulator)**
- **Gap certificates.** **[Inference]** The last item gives a constrained bound for C7 and C8, which addresses verification issue R9.
  - portfolio heuristics with dual bounds ([Brown & Smith 2011](https://consensus.app/papers/details/4ea8b439c29a59fdb15efeefe4be19c5/?utm_source=claude_desktop));
  - gradient penalties ([2014](https://consensus.app/papers/details/3b9b32a6560f512781bd69b9a6881290/?utm_source=claude_desktop));
  - a [tutorial with a portfolio example](https://consensus.app/papers/details/7b6109ad529056818306c4e34a82b8bc/?utm_source=claude_desktop);
  - [nonanticipative duality for chance-constrained programs](https://consensus.app/papers/details/682cde7659bb589ca6b69c33a73ba965/?utm_source=claude_desktop).
- **Decomposition.** **[Inference]** Validate the dual-price "liquidity merit order" against these bounds.
  - weakly coupled relaxations ([Adelman & Mersereau](https://consensus.app/papers/details/80a57bb0dc385a61b01ce4b8ac352bfd/?utm_source=claude_desktop));
  - price versus resource coordination of coupled units ([Carpentier et al.](https://consensus.app/papers/details/f14edca49a465c22bce6b90ea17e6b6f/?utm_source=claude_desktop)), "much faster and give better results than the standard stochastic dual dynamic programming method" for urban microgrids.
- **Continuation values for SELL.** **[Inference]** Use regress-later LSMC with control randomization, and check it against dual bounds.
  - LSMC with switching costs, transient liquidity costs and permanent price impact ([Zhang et al., QF](https://consensus.app/papers/details/bd9ffca561a3514889e2a5038e8ed79a/?utm_source=claude_desktop));
  - regression errors "accumulate over time and typically blow up" without corrections such as control randomization with policy iteration ([Andreasson & Shevchenko](https://consensus.app/papers/details/4b66358238d35c29bbd7e57dd1acc824/?utm_source=claude_desktop));
  - iterate on policies rather than value functions when constraints bind ([van Binsbergen & Brandt](https://consensus.app/papers/details/ec54684eaa9e556f9440ad9c4f5783d5/?utm_source=claude_desktop));
  - regress-later makes dual bounds cheap ([Nadarajah et al.](https://consensus.app/papers/details/0197fc9b64f252bb8a5ab668a0a881d2/?utm_source=claude_desktop)).
- **Policy search:**
  - [parametric portfolio policies](https://consensus.app/papers/details/d764d9977ca95514bf5676342353a7ae/?utm_source=claude_desktop);
  - an [evolutionary search for PE recommitment rules](https://consensus.app/papers/details/1a08544fb5305532bc1270a2b91fa377/?utm_source=claude_desktop), a direct precedent for the CMA-ES plan;
  - [parametric cost-function approximation](https://consensus.app/papers/details/7c57fa41f7e4597e99fcb62f0eb96d0a/?utm_source=claude_desktop) with [stochastic-search tuning](https://consensus.app/papers/details/b0b347e585545e16850eea36f3583f96/?utm_source=claude_desktop);
  - [rule-based strategies](https://consensus.app/papers/details/2cc4314fcfd355ba8d2e99f26662baf2/?utm_source=claude_desktop) that are more stable and easier to explain than DP.
- **RL challenger.**
  - A 2026 survey classifies hybrid, scalable and end-to-end RL for multi-period planning ([Luo et al.](https://consensus.app/papers/details/382c1e2a57645aabb826468c2807966d/?utm_source=claude_desktop)).
  - [Neural-progressive hedging](https://consensus.app/papers/details/f7d54251973a5974a4dd691aa73ed871/?utm_source=claude_desktop) enforces CVaR and liquidity constraints while an RL policy executes.
  - **[Inference]** If an RL challenger is built, prefer this kind of constraint-enforcing hybrid.

### 4.3 Parameters and calibration priors (literature values, not ADIC data)

- **Commitment pacing** ([de Zwart et al.](https://consensus.app/papers/details/63deabfca2f15e65880fa9a8f5d03a13/?utm_source=claude_desktop)):
  - about 30% overcommitment during build-up;
  - about 10% of commitments never called;
  - 86% of target achieved with an 8% probability of overinvestment.
  - **[Inference]** Benchmark the dossier's κ = 0.25–0.5 per quarter against this rule.
- **Smoothing the payout within the band.** The "snake-in-the-tunnel" rule with 3–7% bands cuts short-run spending reductions ([Wang et al., FAJ 2018](https://consensus.app/papers/details/c6c980011c485d7b9f5d75004167b9cc/?utm_source=claude_desktop)). **[Inference]** Use analogous band mechanics inside the 5–10% band.
- **Illiquidity-cost range.** **[Inference]** For ADIC, the payout channel should decide where in this range to calibrate.
  - welfare premium for commitment risk equivalent to 1.63% a year with many funds ([Phalippou et al.](https://consensus.app/papers/details/9b5881d8cef05dffa4a40423d6b15bc8/?utm_source=claude_desktop));
  - negligible when PE and public equity are close substitutes ([Buchner](https://consensus.app/papers/details/4b82de353e7f5ab39a2937994c2aafe2/?utm_source=claude_desktop));
  - high when illiquidity restricts consumption ([Jansen et al.](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop)).
- **Variation-margin stress.** **[Inference]** Use these to size stressed VM multipliers in C3 and C5.
  - Variation margin rose fivefold at the height of the 2020 stress ([Rousová et al.](https://consensus.app/papers/details/1568e37e2c845eef816b5c7ccc9f8648/?utm_source=claude_desktop)).
  - 13–33% of euro-area funds with sizeable derivatives exposure may lack the buffers to meet stressed calls ([Jukonis et al.](https://consensus.app/papers/details/8235e347f86b5b799f4cd8e4e7e31838/?utm_source=claude_desktop)).
- **Backtest haircut.** Live Sharpe ratios showed a median 73% deterioration from backtests, and complex strategies deteriorated more than 30 pp further than simple ones ([Suhonen et al.](https://consensus.app/papers/details/df15834241b85f16a52df4f546753386/?utm_source=claude_desktop)). **[Inference]** Haircut tuned-policy gains in IC packs.

### 4.4 Constraints

- **CVaR constraints.**
  - Per-period CVaR constraints in L2 keep relatively complete recourse and a valid bound ([Valladão et al.](https://consensus.app/papers/details/9cf93dec2abe56dfa26354d463424a0a/?utm_source=claude_desktop)).
  - Multiple CVaR constraints at different confidence levels "shape the profit/loss distribution" ([Krokhmal et al.](https://consensus.app/papers/details/1c488d85f2725582b63cf6820a9feee3/?utm_source=claude_desktop)).
  - **[Inference]** Express C7 and C8 as a small ladder of CVaR or bPoE constraints rather than a single CVaR ≤ 0.
- **bPoE floor.** Use bPoE for the 7% floor and the liquidity shortfall ([Dang et al.](https://consensus.app/papers/details/50e851a2565f56639dabd7b0045072f5/?utm_source=claude_desktop)).
- **Funding constraint as stochastic dominance.** A time-consistent sequential SSD constraint of assets over liabilities works, and imposing it at the last-but-one stage enforces it at every stage ([Consigli et al. 2025](https://consensus.app/papers/details/295e2cc1acea519691f1da3da818ec23/?utm_source=claude_desktop)). **[Inference]** This is an alternative to the fund-level LCR chance constraint.
- **Decision-rule caveats.** Linear decision rules "can be inadequate and even lead to infeasible instances" even with complete recourse ([Chen et al. 2008](https://consensus.app/papers/details/26c1f3114deb5332a2978f908796ba74/?utm_source=claude_desktop)). Remedies:
  - [lifted, piecewise-linear rules](https://consensus.app/papers/details/f024ebd922875d4faf8d0dc5ec2083c7/?utm_source=claude_desktop);
  - [two-stage linear decision rules](https://consensus.app/papers/details/8481d1424b1653429f4c1004f3d55718/?utm_source=claude_desktop);
  - [splitting the uncertainty set for integer decisions](https://consensus.app/papers/details/ea94e5aa95865546965c9ede51ecdd8c/?utm_source=claude_desktop).
  - **[Inference]** The integer variant is the relevant one for REFINANCE and LEVER triggers.
- **Margin liquidity.** Include stressed variation margin in the fund LCR. The derivatives-liquidity evidence in 4.3 supports the dossier's C3 and C5.

### 4.5 Objectives and the distribution decision

- **Do not maximize P(target).** An all-or-nothing investor becomes more risk-seeking when behind on goals ([Capponi & Zhang 2024](https://consensus.app/papers/details/0fd71f5302ce52aead087822575e14e4/?utm_source=claude_desktop)), which supports dossier §1.3(c). Alternatives:
  - **Target range.** A lower capital-protection target plus an upper goal gave a better downside trade-off than CRRA ([Zhang et al., J. Comput. Finance](https://consensus.app/papers/details/c48e4af4f7e358c38f21d42292b0c4a6/?utm_source=claude_desktop)).
  - **Lexicographic goals.** Prioritized goal programming solved as an LP ([Kim et al.](https://consensus.app/papers/details/f03987fc1a23597e921e27887e9a71fc/?utm_source=claude_desktop)) maps naturally to Tier 1 and Tier 2.
- **Treat the payout as a decision.** **[Inference]** Make the payout path within 5–10% a decision variable with a smoothing penalty. For each payout policy, report P(nominal and real NAV erosion).
  - For a sovereign fund, the optimal spending rate is well below the expected real return, and spending at that return erodes the fund in probability and expectation ([Aase 2024](https://consensus.app/papers/details/b92a25866b5350709012a3b8f6d1047b/?utm_source=claude_desktop)).
  - Spending and investment rules should be set together, especially when cuts are unwelcome ([Blume 2010](https://consensus.app/papers/details/0eca9b34b4cb5f0abedadc7fdcb1b6a9/?utm_source=claude_desktop)).
  - Endowments revise their spending rules often, and spending changes lead allocation changes ([Brown et al.](https://consensus.app/papers/details/dbb718a2963d55a1b5ae773ef65f8950/?utm_source=claude_desktop)).
- **Time consistency.**
  - A precommitted mean-CVaR investor behaves like a naive investor whose CVaR confidence level rises over time ([Strub et al.](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop)).
  - [Shapiro's 2021 tutorial](https://consensus.app/papers/details/2331cc1ac83f5043b80b0912e7a8d2e0/?utm_source=claude_desktop) covers the risk-averse and distributionally robust versions.
  - **[Inference]** Re-solving a static five-year CVaR every quarter implies a predictable drift in effective risk aversion. Disclose this to the IC alongside plan revisions.

### 4.6 Agent and IC design

- **Evaluation and verification agent.** **[Inference]** Rubric checks:
  - at least *N* seeds per policy;
  - a distribution of outcomes across seeds and generators;
  - a complexity penalty.
  
  Sources:
  - Multiplicity-aware evaluation: DRL Sharpe ratios "vary substantially across random seeds" and apparent outperformance often vanishes ([Grądzki 2026](https://consensus.app/papers/details/2bdfd029e65f5d789ba6949df75719a7/?utm_source=claude_desktop)).
  - [Deflated Sharpe ratio](https://consensus.app/papers/details/378afd063fd15487a4fcb21af0850767/?utm_source=claude_desktop) and probability of backtest overfitting.
  - The backtest-deterioration priors in 4.3.
- **Bound agent.** **[Inference]** It computes the L3 gap with L2-gradient penalties (entries 7–8) and reports it beside every policy ranking.
- **Scenario agent.** **[Inference]** It runs competing generators (Voronoi cell sampling, moment matching with an arbitrage check, nested-distance reduction) and publishes the in-sample versus out-of-sample stability of first-stage actions, so the IC sees how much an action depends on the generator.
- **Treasurer seat (Corporate Finance owns Treasury).** **[Inference]** This seat owns the λ/ρ curve and the funds-transfer-pricing hurdles, and checks them against market shadow-cost proxies (4.1). The λ breakdown by binding constraint (entry 15) tells the IC whether liquidity is scarce because of the payout, calls, margin or covenants.
- **Secondaries group (hybrid fund and direct book) as SELL intelligence.** **[Inference]** Its quotes should be decomposed into NAV and unfunded components ([Giommetti & Jørgensen](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop); [Bollen & Sensoy](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop)), under the conflict controls the context file already requires.
- **When to revise decisions.** Partially adaptive multistage SP chooses the best revision stages under limited flexibility and reaches performance "comparable to fully flexible settings" ([Kayacık et al. 2024](https://consensus.app/papers/details/42399f110c7950539ace896d78520a52/?utm_source=claude_desktop)). **[Inference]** This supports a "commit now, revisit at a trigger" playbook instead of re-optimizing every action every quarter.

---

## 5. Papers that challenge the dossier's recommendations

| Dossier position | Challenging evidence | Strength and caveats | Suggested response |
|---|---|---|---|
| §3.2 and §6.2: SDDP "handles state dimensions in the tens"; L2 with about 20 states | [Zhang & Sun](https://consensus.app/papers/details/c3bb3cbfbd5f58858b54e03033005617/?utm_source=claude_desktop): iteration bounds exponential in state dimension *d* (sharp). [Lan](https://consensus.app/papers/details/0cf847831a025cc281826e46c115e58d/?utm_source=claude_desktop): efficient when per-stage dimension is small. | Worst-case theory. [Valladão et al.](https://consensus.app/papers/details/9cf93dec2abe56dfa26354d463424a0a/?utm_source=claude_desktop) solved 100 assets near-optimally in practice. | Choose L2's dimension by bound-gap diagnostics; regularize; compress the belief state. |
| §6.1 step 1 and §7: regime-stratified k-medoids plus moment matching; nested distance "the right metric" for reduction | [Geyer et al.](https://consensus.app/papers/details/3116632fca3a5358a2b66101b6f6aa5d/?utm_source=claude_desktop): reduction trees biased and variable. [Löhndorf 2016](https://consensus.app/papers/details/3705d75ee7385a15936f6937cdae08af/?utm_source=claude_desktop): probability-metric methods ineffective in high dimension. [Pflug & Pichler 2016](https://consensus.app/papers/details/6ca73942bd8e503ab1dda52f20fe2d98/?utm_source=claude_desktop): empirical path trees do not converge. | Test problems are stylized (analytic portfolio, newsvendor). Pflug & Pichler supports the nested distance as the *metric* but not raw-path trees. | Run competing generators and report out-of-sample stability (the dossier's "solve on tree A, evaluate on set B" test, made mandatory). |
| §1.4 and §4.1: stochastic programming dominates fixed-mix | [Bianchi & Guidolin](https://consensus.app/papers/details/ca2f60c16bdb54f892e81d42b625549c/?utm_source=claude_desktop): no clear out-of-sample edge over naive diversification. | The evidence is mixed. On the other side, [MPC beat fixed-mix out of sample over 2006–2020](https://consensus.app/papers/details/ac9e8b4b30f4576b9edd6f8ff1631f99/?utm_source=claude_desktop), and [out-of-sample tests favoured SP for a Finnish pension insurer](https://consensus.app/papers/details/9b7ab8d483ee58a78aa639241ac3957c/?utm_source=claude_desktop). | Make fixed-mix and simple rules first-class L3 baselines on held-out generators. Rest the IC case on payouts and illiquidity rather than on predictability. |
| §2.2: time-varying opportunities are a first-order source of horizon effects | [Diris et al.](https://consensus.app/papers/details/508f632144295e13b57ad0c444d846c1/?utm_source=claude_desktop): hedging demands worth almost nothing out of sample because of predictor-forecast error. | Evidence is from public stocks and bonds. Liabilities and frictions, also cited in §2.2, are unaffected. | Shrink terms driven by return predictors; keep the payout and illiquidity terms. |
| §4.3: a 10% return target is "roughly the return needed to fund the maximum payout without eroding NAV in nominal terms" | [Aase 2024](https://consensus.app/papers/details/b92a25866b5350709012a3b8f6d1047b/?utm_source=claude_desktop): spending at the expected (real) return erodes a sovereign fund in probability and expectation. | Stylized real-terms life-cycle model. **[Inference]** The same volatility-drag logic applies in nominal terms. | Report P(erosion) by payout path and make the payout an explicit IC lever. |
| §3.5: linear decision rules for recourse and policy rules | [Chen et al. 2008](https://consensus.app/papers/details/26c1f3114deb5332a2978f908796ba74/?utm_source=claude_desktop): rules can be inadequate or infeasible even with complete recourse. | Applies to plain affine rules. | Use lifted or piecewise rules (the dossier already mentions "lifted" rules) and two-stage rules. |
| §2.2 and §6.7: least-squares Monte Carlo regression for continuation values | [Andreasson & Shevchenko](https://consensus.app/papers/details/4b66358238d35c29bbd7e57dd1acc824/?utm_source=claude_desktop): regression errors accumulate and blow up. [van Binsbergen & Brandt](https://consensus.app/papers/details/ec54684eaa9e556f9440ad9c4f5783d5/?utm_source=claude_desktop): value-function iteration is biased under constraints, high risk aversion and long horizons. | Known, fixable failure modes. | Control randomization, policy iteration, regress-later, and dual-bound checks. |
| §2.4: static CVaR in L1, re-solved quarterly; nested EAVaR in L2 | [Strub et al.](https://consensus.app/papers/details/a214149a040e57f1ae7cd78cdb2bdd3e/?utm_source=claude_desktop): precommitment is equivalent to a naive investor with a rising CVaR level. [Dang et al.](https://consensus.app/papers/details/50e851a2565f56639dabd7b0045072f5/?utm_source=claude_desktop): time-consistent mean-CVaR can give counterintuitive controls. | Results come from DC and stylized markets. | Consider bPoE floors; disclose the drift in risk aversion to the IC. |
| §3.7: deep RL unsuitable except as an R&D challenger | Supporting: [Grądzki 2026](https://consensus.app/papers/details/2bdfd029e65f5d789ba6949df75719a7/?utm_source=claude_desktop); [Aboussalah et al.](https://consensus.app/papers/details/547a904fb1435227b90efa0f66befe2d/?utm_source=claude_desktop) (most algorithms struggled to converge). More favourable: [neural-network control near the HJB optimum](https://consensus.app/papers/details/58f25fb181df5ab99439f4193d9eafad/?utm_source=claude_desktop); [Deep ALM](https://consensus.app/papers/details/29c5ad0d19b6530b885f42eb2b2d7b4d/?utm_source=claude_desktop); [2026 survey](https://consensus.app/papers/details/382c1e2a57645aabb826468c2807966d/?utm_source=claude_desktop). | No direct contradiction, since the dossier allows a challenger. The positive results come from settings where a DP or HJB benchmark exists. | Keep RL as a challenger; prefer constraint-enforcing hybrids; use multi-run evaluation. |
| §6.7: tail-hedge value at shadow prices exceeds its expected payoff | [Gamba & Triantis](https://consensus.app/papers/details/c6027dda48605911a46b3578a9a0a3ea/?utm_source=claude_desktop): liquidity plays a "critical and distinct role"; the marginal value of derivatives hedging is "likely to be low". | Corporate-finance model, so transfer is weak. **[Inference]** It is not a contradiction of the shadow-price identity. | Let the cash buffer and the hedge compete at the same λ. The overlay ablation is already in the plan. |
| §2.2 and §4.1: Ang et al.'s "about 2% of wealth" cost of illiquidity | Lower: [Buchner](https://consensus.app/papers/details/4b82de353e7f5ab39a2937994c2aafe2/?utm_source=claude_desktop) (negligible for close substitutes). Similar or higher: [Phalippou et al.](https://consensus.app/papers/details/9b5881d8cef05dffa4a40423d6b15bc8/?utm_source=claude_desktop) (1.63% a year with many funds); [Jansen et al.](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop) (high when consumption is restricted). | Model-dependent range. | Calibrate through the payout channel; show the IC a range rather than a point. |

**Supporting rather than challenging:**
- [Capponi & Zhang](https://consensus.app/papers/details/0fd71f5302ce52aead087822575e14e4/?utm_source=claude_desktop) supports §1.3(c) (do not maximize P(target)).
- [Löhndorf & Shapiro](https://consensus.app/papers/details/889e982ca4c8514ea4b791ce145b8493/?utm_source=claude_desktop) supports the Markov-chain L2.
- [Jeet et al.](https://consensus.app/papers/details/3efa59a891125d279f6eb98f81b48d52/?utm_source=claude_desktop) supports the cash-flow-centred design.
- [Nystrup et al. 2016](https://consensus.app/papers/details/af3cdb9829f25b799e30e1b827609c36/?utm_source=claude_desktop) supports the dossier's smoothing penalties: a trading penalty increased robustness.

---

## 6. Verbatim usage message

None. No Consensus result in this run contained a sign-up, upgrade or usage message.

---

## 7. Scope notes

- **Not re-checked here.** These were mostly already confirmed by the verification log, or carry little design weight:
  - Birge (1982); Calafiore & Campi (2006); Campi & Garatti (2008); Shapiro (2009); Nemirovski & Shapiro (2006);
  - Rockafellar & Wets (1991); Watson & Woodruff (2011); Knueven et al. (2023);
  - Moallemi & Sağlam (2017); Longstaff & Schwartz (2001);
  - Geyer & Ziemba (2008); Mulvey et al. (2000); Kusy & Ziemba (1986);
  - Brown, Dimmock, Kang & Weisbenner (2014); Merton (1969, 1993); Samuelson (1969); Tobin (1974);
  - Karatas et al. (2021); Dulac-Arnold et al. (2019); Bühler et al. (2018); Han & E (2016);
  - Frazier (2018); Hansen (CMA-ES); Optuna (2019); Gondzio & Grothey (2006);
  - Dowson & Kapelevich (2021); Ding et al. (msppy); Goulart & Chen (2024).
- **Consensus record quirks found:**
  - online-first or preprint years differ from print years (7 items);
  - truncated author fields (Mohajerin Esfahani & Kuhn shown as "D. Kuhn");
  - one record carries an unrelated abstract (Rockafellar & Uryasev);
  - one NBER venue label sits on an RFS DOI (Gârleanu & Pedersen 2011).
- **Abstract not shown.** Consensus returned no abstract for [Robinson & Sensoy (2016, JFE), *Cyclicality, performance measurement, and cash flow liquidity in private equity*](https://consensus.app/papers/details/86bf821b6ba65861a9da20fed7862965/?utm_source=claude_desktop). It is likely relevant to regime-dependent calls and distributions, but no finding is claimed here.
- **WebSearch.** One attempt was made, for the Bailey et al. venue. It failed because the session's shared budget was exhausted, and no workaround was used.
