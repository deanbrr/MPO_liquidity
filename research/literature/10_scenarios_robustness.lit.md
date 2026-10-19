# Topic 10 literature review: scenario generation, regimes, robustness and stress testing

**Dossier reviewed:** `research/dossiers/10_scenarios_robustness.md` (prepared 18 Oct 2026, 594 lines)
**Prepared:** 18 Oct 2026
**Companion:** `research/verification/10_scenarios_robustness.verify.md` (fact-check of the same dossier)
**Tools:**
- 11 Consensus searches, run one at a time, using only the query parameter (no filters).
- 2 WebSearch calls and 4 Crossref lookups (WebFetch). These confirmed metadata for four works that Consensus did not return.

**Why only 11 Consensus searches.** The task asked for 25 citation checks plus 8-14 topical searches, about 33-39 calls in all.
- The first search reported **49 searches left this month**, shared with two other agents running at the same time.
- After my 11 searches the counter stood at **20**. The other agents used the rest of the drop.
- Running the full set would have used most of the remaining monthly quota and could have stalled the other streams.
- So each query was built to do two jobs: check several dossier citations and backfill a topic. All six seed topics were searched; the log is in Appendix A.

**Conventions**
- Every paper link is the Consensus URL exactly as returned.
- In the bibliography, authors are listed as Consensus shows them, usually the first author plus "et al.". In the integrity table, the dossier's own author lists are kept.
- Citation counts are Consensus counts on 18 Oct 2026. Years are as Consensus shows them. Where Consensus shows an advance-access, working-paper or preprint year, the entry says so.
- "[inference]" marks my own reasoning. Everything else restates a search result or an abstract.
- "(also stream NN)" means another stream's literature review already annotates the paper.
- **User context (18 Oct 2026).**
  - The Secondaries group is a hybrid of direct and fund investments.
  - Treasury is owned by Corporate Finance, which runs the funding and liability side: the liquidity buffer, borrowing facilities, overlay collateral and distribution payments.
  - The design notes therefore send the liquidity gate, liquidity reverse-stress outputs and feasibility constraints to the Corporate Finance / Treasury seat.

---

## 1. Summary

### Citation integrity
The dossier cites **62 academic works**, plus 10 provider, regulatory and software references, which were out of scope. I checked the **25 most load-bearing**:
- the works behind the robustness layer (R1-R8 and the fragility link);
- the view machinery;
- the regime ESG;
- the private cash-flow block;
- scenario trees and SDDP;
- all three works the dossier marked "unverified".

| Outcome | Count | Detail |
|---|---|---|
| Found | 21 | **16** returned as direct Consensus records. Four show advance-access years: Pesenti et al. 2018, Guidolin & Timmermann 2006, Hansen & Sargent 2020, Dowson & Kapelevich 2020. Long, Sim & Zhou is indexed only as its SSRN preprint, under the earlier title *The Dao of Robustness*. **1** was confirmed through Crossref after Consensus missed it (Takahashi & Alexander 2002). **4** were confirmed indirectly, because an indexed abstract names them: Høyland & Wallace with its full reference; Aumann & Serrano, Brown & Sim and Klibanoff et al. by author and year only. |
| Mismatched | 4 | (1) **Mohajerin Esfahani & Kuhn**: the title is truncated. Full title "…: performance guarantees and tractable reformulations"; *Math. Programming*, DOI 10.1007/s10107-017-1172-1. (2) **Gao & Kleywegt** is published: *Math. of OR* 48(2):603-655 (2023), DOI 10.1287/moor.2022.1275. (3) **Xie** is published: *Math. Programming* 186(1-2):115-155 (2021), DOI 10.1007/s10107-019-01445-5. (4) **Shu, Yu & Mulvey** is published: *J. Asset Management* 25(5):493-507 (2024), DOI 10.1057/s41260-024-00376-x. |
| Not found | 0 | n/a |

- **No citation was fabricated.**
- **The three works the dossier marked "unverified" are now confirmed:**
  - Meucci (2008), through Consensus's arXiv record 1012.2848. Use it in place of the SSRN link that returned 403.
  - Pflug (2001), DOI 10.1007/pl00011398.
  - Rebonato & Denev (2014). Consensus indexes the CUP book's chapters.
- **One quotation is not verbatim.** For Glasserman & Xu (2014) the dossier writes "with little effort". The abstract says "very little computational effort beyond that required to evaluate performance under the baseline nominal model". The verification log flags the same point.
- **One citation is applied to the wrong problem.** Heitsch & Römisch (2003) reduces scenario sets. For multistage decision trees, their 2009 papers add the **filtration distance**. See §5, item 2.
- **One source is uncited.** The ENS diagnostic in §6.10 comes from Meucci (2012), *Effective Number of Scenarios in Fully Flexible Probabilities*.
- **Not checked here (37 works).** These are listed under the table in §2. The verification log already confirmed seven of them, and stream 04 confirmed Getmansky, Lo & Makarov.

### Backfill: what the dossier misses
1. **Robust satisficing (RS) and DRO are one frontier, not two instruments.**
   - Under Wasserstein ambiguity the two share a solution family. There is an explicit correspondence between the DRO radius and the RS target (Wang et al. 2025, *MSOM*).
   - An "estimation-fortified" RS handles prediction error in forecasts (Sim et al. 2024, *OR*).
2. **Robustness over time is under-specified.**
   - Time-rectangular robust control is over-pessimistic (Blanchet et al. 2025).
   - Hidden-state problems need separate robustness for the regime posterior and for the dynamics (Hansen & Sargent 2007).
   - Worst cases load on **regime persistence** (Hansen et al. 2019).
   - Ambiguity sets can switch with regimes (Pun et al. 2023, *MSOM*).
3. **The optimizer must handle a latent regime.**
   - Partially observable multistage SP carries a belief state (Dowson et al. 2020).
   - PO-SDDP has been applied to decades-long financial planning (Lee et al. 2023, *QF*; also stream 01).
   - This is the literature answer to verification finding R9.
4. **Multistage scenario trees need the filtration distance** (Heitsch & Römisch 2009). The 2003 algorithms the dossier cites target scenario sets.
5. **Reverse stress for path models, and stresses that go beyond the simulated support.**
   - Dynamic stressed measures can be re-simulated (Kroell et al. 2022).
   - Wasserstein reverse sensitivity moves outcomes rather than only reweighting them, and has an R package, SWIM (Pesenti 2021).
   - χ² sensitivity metrics have lower sampling error than KL (Makam et al. 2021).
   - f-divergence and Bregman generalizations of the KL worst case exist (Breuer & Csiszár, *Mathematical Finance*).
6. **View machinery.**
   - Path-based entropy pooling with discrete weights (van der Schans 2018).
   - The ENS source (Meucci 2012).
   - A modern survey on pooling densities (Koliander et al. 2022).
   - Scenario likelihoods and cascading to holdings in Bayesian nets (Rebonato 2018).
7. **Identify regimes on macro drivers.**
   - Macro-identified regimes beat return-identified ones, and return-based regimes become extreme after crises (Goodarzi et al. 2025).
   - Regimes on drivers are persistent and useful out of sample (Kritzman et al. 2012).
8. **Private cash flows.**
   - A factor-driven Takahashi-Alexander model is now published (Cao et al. 2025, *FAJ*; also streams 01, 04, 05).
   - Timing metrics, not just multiples, separate liquidity profiles (Shuang 2026).
9. **Model risk management.**
   - Model-weighted and superposed model-risk measures, with Bayesian weights on the model space (Jokhadze & Schmidt 2020). This answers the dossier's open question 3 on provider weights.
   - "Iterative reverse scenario logic" for chained models (Gerst et al. 2026).

### Main challenges to the dossier (detail in §5)
- **SDDP on a Markov policy graph is not "one-to-one" with a latent-regime ESG.** It needs a belief state (Dowson et al. 2020; Lee et al. 2023).
- **The IC card double-counts.** The W1/KL worst cases and k\*/η\* are, at least under Wasserstein, two coordinates of one robustness frontier (Wang et al. 2025).
- **Stacked robustness compounds pessimism.** Stagewise risk-averse SDDP plus a path-law KL ball can be over-pessimistic (Blanchet et al. 2025).
- **The structured ambiguity set varies only means.** Persistence ambiguity matters more for worst cases (Hansen et al. 2019). This echoes verification finding R8.
- **Regime estimation on market factors is fragile after crises** (Goodarzi et al. 2025).
- **KL is not the only sensible divergence.** χ² gives lower-variance sensitivity rankings (Makam et al. 2021).
- **View machinery cannot fix allocation instability.** Rebonato & Denev's own chapters say it is "foolhardy" to read a single allocation off a Bayesian net, because allocations are very sensitive to expected returns.

---

## 2. Citation-integrity table

| Dossier citation | Status | Corrected metadata / note | Consensus URL |
|---|---|---|---|
| Long, D.Z., Sim, M., Zhou, M. (2023). Robust satisficing. *OR* 71(1):61-82 | found (preprint record) | Indexed only as the SSRN preprint *The Dao of Robustness* (2020, DOI 10.2139/ssrn.3478930). This is the same SSRN id as the dossier's preprint link. The abstract confirms the fragility measure: a Brown-Sim satisficing measure that is monotone, positively homogeneous and subadditive, linked to Aumann-Serrano riskiness. The *OR* 2023 record was not returned. | [link](https://consensus.app/papers/details/73bdaf0f743d5e3bb2328eed3266af67/?utm_source=claude_desktop) |
| Meucci, A. (2008). Fully flexible views: theory and practice. *Risk* 21(10) | found | The record is the arXiv version: arXiv:1012.2848, DOI 10.48550/arxiv.1012.2848, 2008. The *Risk* venue is not displayed. Replace the SSRN link (403) with the arXiv link. This resolves the dossier's "unverified" flag. | [link](https://consensus.app/papers/details/9ed7d3116f4656ada56ea14eb7491b12/?utm_source=claude_desktop) |
| Breuer, T., Csiszár, I. (2013). Systematic stress tests with entropic plausibility constraints. *JBF* 37(5) | found | DOI 10.1016/j.jbankfin.2012.04.013. The abstract confirms the relative-entropy ball and the Maximum Loss theorem. | [link](https://consensus.app/papers/details/e39c45b4323b5b83a85c01457ba70c96/?utm_source=claude_desktop) |
| Glasserman, P., Xu, X. (2014). Robust risk measurement and model risk. *QF* 14(1) | found (quote fix) | DOI 10.1080/14697688.2013.822989. The dossier's quote "with little effort" should read "very little computational effort beyond that required to evaluate performance under the baseline nominal model". | [link](https://consensus.app/papers/details/6312a826b7aa56f9b9227cf9bc4c0be5/?utm_source=claude_desktop) |
| Pesenti, S.M., Millossovich, P., Tsanakas, A. (2019). Reverse sensitivity testing. *EJOR* 274(2) | found | DOI 10.1016/j.ejor.2018.10.003. Consensus year 2018 (advance access). The abstract confirms that it runs on "a single set of input/output scenarios". | [link](https://consensus.app/papers/details/0aafabf4667c53f79982150bca7390d0/?utm_source=claude_desktop) |
| Glasserman, P., Kang, C., Kang, W. (2015). Stress scenario selection by empirical likelihood. *QF* 15(1) | found | DOI 10.1080/14697688.2014.926019 | [link](https://consensus.app/papers/details/dfb066c744f9534f9354125656683f26/?utm_source=claude_desktop) |
| Hansen, L.P., Sargent, T.J. (2022). Structured ambiguity and model misspecification. *JET* 199:105165 | found | DOI 10.1016/j.jet.2020.105165. Consensus year 2020 (advance access). | [link](https://consensus.app/papers/details/ddf8e69b97c6576d81c62a9d3a135015/?utm_source=claude_desktop) |
| Hansen, L.P., Sargent, T.J. (2001). Robust control and model uncertainty. *AER* 91(2) | found | DOI 10.1257/aer.91.2.60 | [link](https://consensus.app/papers/details/835893898149517fa858d5c645341ace/?utm_source=claude_desktop) |
| Anderson, E., Hansen, L.P., Sargent, T.J. (2003). A quartet of semigroups… *JEEA* 1(1) | found | DOI 10.1162/154247603322256774 | [link](https://consensus.app/papers/details/675ba7d9c9a950abaf5a1adf9026796b/?utm_source=claude_desktop) |
| Mohajerin Esfahani, P., Kuhn, D. (2018). Data-driven distributionally robust optimization using the Wasserstein metric. *Math. Programming* | **mismatched** (minor) | The full title adds ": performance guarantees and tractable reformulations". *Mathematical Programming*, DOI 10.1007/s10107-017-1172-1. Consensus shows year 2015 and lists only "D. Kuhn" as author, an index artifact. | [link](https://consensus.app/papers/details/955158b8081d595c9c09458e32f6c2c0/?utm_source=claude_desktop) |
| Gao, R., Kleywegt, A.J. DRSO with Wasserstein distance. arXiv:1604.02199 ("accepted, *Math. of OR*") | **mismatched** (incomplete) | Not returned by the Consensus topical search. Crossref: *Mathematics of Operations Research* 48(2):603-655 (May 2023), DOI 10.1287/moor.2022.1275. | n/a (Crossref) |
| Xie, W. On distributionally robust chance constrained programs with Wasserstein distance. arXiv:1806.07418 | **mismatched** (incomplete) | Not returned by Consensus. Crossref: *Mathematical Programming* 186(1-2):115-155 (2021; online 13 Nov 2019), DOI 10.1007/s10107-019-01445-5. | n/a (Crossref) |
| Guidolin, M., Timmermann, A. (2007). Asset allocation under multivariate regime switching. *JEDC* 31(11) | found | DOI 10.1016/j.jedc.2006.12.004. Consensus year 2006 (advance access). The abstract confirms four regimes ("crash, slow growth, bull and recovery") and "substantial" welfare costs. | [link](https://consensus.app/papers/details/7d340a58cd2a5c6e94a2f82b8061eb98/?utm_source=claude_desktop) |
| Shu, Y., Yu, C., Mulvey, J.M. (2024). Downside risk reduction using regime-switching signals: a statistical jump model approach. arXiv:2402.05272 | **mismatched** (preprint cited) | Crossref: *Journal of Asset Management* 25(5):493-507 (2024), DOI 10.1057/s41260-024-00376-x. Consensus returned a different 2024 paper by the same group instead (*Annals of OR*, DOI 10.1007/s10479-024-06266-0). | n/a (Crossref) |
| Takahashi, D., Alexander, S. (2002). Illiquid alternative asset fund modeling. *JPM* 28(2):90-100 | found (Crossref) | Consensus did not return the record, but several indexed papers build on it (e.g., Cao et al. 2025). The WebSearch found only citing works. Crossref confirms title, authors, *JPM* 28(2):90-100, 2002, DOI 10.3905/jpm.2002.319836, all matching the dossier. | n/a (Crossref) |
| Pflug, G.Ch. (2001). Scenario tree generation for multiperiod financial optimization by optimal discretization. *Math. Programming* 89 | found | DOI 10.1007/pl00011398. This resolves the dossier's "unverified" flag. | [link](https://consensus.app/papers/details/f6641c737c125d13851a68fe92d6ba3d/?utm_source=claude_desktop) |
| Heitsch, H., Römisch, W. (2003). Scenario reduction algorithms in stochastic programming. *COA* 24(2-3) | found (scope note) | DOI 10.1023/a:1021805924152. The metadata is correct, but this paper reduces scenario sets. For multistage trees, add Heitsch & Römisch (2009); see §3 #19. | [link](https://consensus.app/papers/details/616a491b8703553dabdc035b194f8841/?utm_source=claude_desktop) |
| Høyland, K., Wallace, S.W. (2001). Generating scenario trees for multistage decision problems. *MS* 47(2):295-307 | found (indirect) | The record was not returned. The exact reference ("Manag. Sci. 47 (2001) 295-307") is reproduced in the abstract of Beraldi et al. (2010), linked here. | [link](https://consensus.app/papers/details/577f4d47226e5d4ea377f5a967ddb2f9/?utm_source=claude_desktop) |
| Dowson, O. (2020). The policy graph decomposition of multistage stochastic programming problems. *Networks* 76(1) | found | DOI 10.1002/net.21932 | [link](https://consensus.app/papers/details/8ce7e05fa5bc5e38849108e50d33276e/?utm_source=claude_desktop) |
| Dowson, O., Kapelevich, L. (2021). SDDP.jl. *IJOC* 33(1) | found | DOI 10.1287/ijoc.2020.0987. Consensus year 2020 (advance access). | [link](https://consensus.app/papers/details/0376bfa984505d2f96c7c72cd2583a88/?utm_source=claude_desktop) |
| Philpott, A.B., de Matos, V.L. (2012). Dynamic sampling algorithms for multi-stage stochastic programs with risk aversion. *EJOR* 218(2) | found | DOI 10.1016/j.ejor.2011.10.056 | [link](https://consensus.app/papers/details/7bcb639f52af5a5298f60b6bd44f8d0d/?utm_source=claude_desktop) |
| Rebonato, R., Denev, A. (2014). *Portfolio Management under Stress*. CUP | found | Consensus indexes the book's chapters (DOIs 10.1017/cbo9781107256736.0xx). The book description matches. This resolves the dossier's "unverified" flag. | [link](https://consensus.app/papers/details/6dce18f9e5f958b5b3d99e3eb4b65d44/?utm_source=claude_desktop) |
| Aumann, R.J., Serrano, R. (2008). An economic index of riskiness. *JPE* 116(5) | found (indirect, author-year only) | The record was not returned. Long et al.'s indexed abstract cites "the riskiness index of Aumann and Serrano (2008)". The verification log confirmed the full metadata via RePEc. | [link](https://consensus.app/papers/details/73bdaf0f743d5e3bb2328eed3266af67/?utm_source=claude_desktop) |
| Brown, D.B., Sim, M. (2009). Satisficing measures for analysis of risky positions. *MS* 55(1) | found (indirect, author-year only) | The record was not returned. Long et al.'s abstract calls the fragility measure "a class of Brown and Sim (2009) satisficing measure". | [link](https://consensus.app/papers/details/73bdaf0f743d5e3bb2328eed3266af67/?utm_source=claude_desktop) |
| Klibanoff, P., Marinacci, M., Mukerji, S. (2005). A smooth model of decision making under ambiguity. *Econometrica* 73(6) | found (indirect, author-year only) | The record was not returned. Hansen & Sargent (2011, *JET*) cite "the smooth ambiguity model of Klibanoff et al. (2005)" in their abstract, linked here. | [link](https://consensus.app/papers/details/5642448bc64f50e78d209047542342ae/?utm_source=claude_desktop) |

**Not checked in this pass (37 works).** Aas et al. 2009; Ang & Bekaert 2002\*; Barillas, Hansen & Sargent 2009; Barone-Adesi et al. 1999; Ben-Tal et al. 2013; Broadie, Du & Moallemi 2015; Buehler et al. 2020; Campbell, Chan & Viceira 2003\*; Campi & Garatti 2008\*; Carr & Wu 2009; Chen & Sim 2009; Cont & da Fonseca 2002; Delage & Ye 2010; Gatheral & Jacquier 2014; Genest & Zidek 1986; Getmansky, Lo & Makarov 2004\*\*; Gordy & Juneja 2010; Hamilton 1989; Higham 2002\*; Kleywegt, Shapiro & Homem-de-Mello 2002; Kritzman & Li 2010; Kritzman, Li, Page & Rigobon 2011; Kuhn, Shafiee & Wiesemann 2025\*; Lange et al. 2026\*; Maenhout 2004; Mak, Morton & Wood 1999; Nystrup, Madsen & Lindström 2018; Nystrup, Lindström & Madsen 2020; O'Hagan et al. 2006; Pástor & Stambaugh 2012\*; Pflug, Pichler & Wozabal 2012; Politis & Romano 1994; Politis & White 2004; Rockafellar & Uryasev 2000; Smith & Winkler 2006; White 2000; Wiese et al. 2020.
- \* confirmed by the verification log via RePEc, Crossref or arXiv.
- \*\* confirmed by stream 04's literature review via WebSearch.

---

## 3. Annotated bibliography (25 papers)

Selection favours papers that are relevant to ADIC's design, that the dossier does not cite, and that no other stream already covers. Papers already annotated elsewhere are tagged.

### A. Robustness objectives and ambiguity sets

**1. [On the Equivalence and Performance of Distributionally Robust Optimization and Robust Satisficing Models](https://consensus.app/papers/details/97d781784f8953ec915e053f62c18c68/?utm_source=claude_desktop)**
- Zhiyuan Wang et al. · 2025 · *Manufacturing & Service Operations Management* · 3 cit. · DOI 10.1287/msom.2023.0531
- *Finding:* With Wasserstein-based models and a risk-aware convex objective, DRO and robust satisficing "share the same solution family". There is a correspondence between the DRO radius and the RS target at which the optimal solutions coincide, and it extends to globalized versions. Practical performance still depends on how the parameters are selected; cross-validation helps.
- *Relevance:* The dossier's IC card reports radius-based worst cases (KL η, W1 ε) alongside target-based k\* and η\* as separate evidence. Under this result they are two parameterizations of one frontier. The proof covers Wasserstein, not KL, so the exact mapping for R7 still needs to be checked [inference].

**2. [The Analytics of Robust Satisficing: Predict, Optimize, Satisfice, Then Fortify](https://consensus.app/papers/details/97e7837f827158799eb76e800e49f491/?utm_source=claude_desktop)**
- M. Sim et al. (the abstract names Sim, Tang, Zhou and Zhu) · 2024 · *Operations Research* · 24 cit. · DOI 10.1287/opre.2023.0199
- *Finding:* "Estimation-fortified robust satisficing" combines predictive and prescriptive analytics to fortify decisions against both risk ambiguity and estimation uncertainty. It consistently outperforms conventional predictive methods when data are sparse.
- *Relevance:* Each ADIC asset carries noisy return predictions: underwritten, current actual and group forecast. A fortified RS floor (T1-F) can treat forecast error explicitly rather than only distributional ambiguity. This links to stream 07 (return fusion) [inference].

**3. [Data-Driven Distributionally Robust CVaR Portfolio Optimization Under A Regime-Switching Ambiguity Set](https://consensus.app/papers/details/05518e72407e555380b0afd7eb56f5f9/?utm_source=claude_desktop)**
- Chi Seng Pun et al. · 2023 · *MSOM* · 16 cit. · DOI 10.2139/ssrn.4378930 (the abstract gives the e-companion at 10.1287/msom.2023.1229)
- *Finding:*
  - It embeds regime switching in a Wasserstein ambiguity set, estimated with a hidden Markov model plus covariates, and the problem stays tractable.
  - Above a stated sample size the set contains the true distribution with high probability.
  - The portfolio beat 1/N and other benchmarks, and reallocated promptly in 2008.
- *Relevance:* This is a template for **regime-conditional robustness**: a separate radius per regime, for example wider in the crisis and DPI-drought regimes. The dossier uses one global η and ε on the 5-year path law [inference].

**4. [Bayesian Distributionally Robust Merton Problem with Nonlinear Wasserstein Projections](https://consensus.app/papers/details/20388d7cb73c5106b87a0491333f62c0/?utm_source=claude_desktop)**
- José H. Blanchet et al. · 2025 · arXiv preprint · 3 cit. · DOI 10.48550/arxiv.2512.01408
- *Finding:*
  - Time-rectangular distributionally robust control "replenishes adversarial power at every instant and induces over-pessimism".
  - The paper instead places a single ambiguity set on the drift prior, which preserves learning and tractability.
  - It calibrates the radius by a nonlinear Wasserstein projection, and the result is less pessimistic than rectangular control.
- *Relevance:* In a 10-year problem with annual stages, robustness applied at every stage compounds. Examples are nested risk measures in SDDP or per-stage ambiguity. Put ambiguity on CMA and prior parameters (the dossier's structured layer) and on the path law, not at every stage [inference]. This is a preprint.

**5. [Recursive robust estimation and control without commitment](https://consensus.app/papers/details/b88a782e5625543c82fe19c60577d8bc/?utm_source=claude_desktop)**
- L. Hansen et al. · 2007 · *Journal of Economic Theory* · 214 cit. · DOI 10.1016/j.jet.2006.06.010
- *Finding:* With hidden states, the posterior is a state variable. Two risk-sensitivity operators give robustness to (i) the dynamics conditional on the hidden state and (ii) the prior over the hidden state.
- *Relevance:* ADIC's regime is filtered, not observed; it comes from the deck's State/Fragility engine. Robustness to the regime posterior and robustness to the conditional dynamics should be separate dials. A single KL ball on the path law mixes them [inference].

**6. [Macroeconomic uncertainty prices when beliefs are tenuous](https://consensus.app/papers/details/27668b78be6b5bb48c584e7a2e2326d9/?utm_source=claude_desktop)**
- Lars Peter Hansen et al. · 2019 · *Journal of Econometrics* · 27 cit. · DOI 10.1016/j.jeconom.2019.11.010
- *Finding:* The paper separates ambiguity (which structured model is right) from misspecification (all of them may be wrong). In its quantitative example the investor fears "high persistence of low growth rate states and low persistence of high growth rate states".
- *Relevance:* Worst cases load on **persistence**. ADIC's structured set should vary the regime transition matrix, for example longer DPI-drought and crisis dwell times, and not only the CMA means. This agrees with verification finding R8 [inference].

**7. [Measuring Distribution Model Risk](https://consensus.app/papers/details/5a9597cc3ff75ae7a338a13f97e35929/?utm_source=claude_desktop)**
- T. Breuer et al. · 2013 (Consensus year) · *Mathematical Finance* · 87 cit. · DOI 10.1111/mafi.12050
- *Finding:* Distribution model risk is the maximum expected loss over plausible distributions defined by relative entropy, "another f‑divergence or Bregman distance". The paper gives formulas and the explicit worst-case distribution.
- *Relevance:* This generalizes the dossier's KL-only toolkit (R1-R3, R6) to divergences with different tail behaviour while keeping closed-form worst cases [inference].

### B. Stress testing and reverse stress testing

**8. [Stressing Dynamic Loss Models](https://consensus.app/papers/details/ce04d40b9c585067a632648bcb9d6bae/?utm_source=claude_desktop)**
- Emma Kroell et al. · 2022 · SSRN · 8 cit. · DOI 10.2139/ssrn.4268639
- *Finding:*
  - Reverse stress testing for a dynamic (compound Poisson) model: the stressed measure minimizes KL to the reference model subject to terminal constraints such as VaR, or VaR and CVaR together.
  - Under the stressed measure, intensity and severity become time- and state-dependent.
  - The paper gives an algorithm to simulate paths under the stressed measure.
- *Relevance:* The dossier's R6 tilts terminal path features. This shows how to turn a tilt into stressed **dynamics** and re-simulate. The IC then sees how a failure unfolds, for example when a drought and margin calls coincide [inference].

**9. [Reverse Sensitivity Analysis for Risk Modelling](https://consensus.app/papers/details/9bdfc1fbec735f4a91035e0ba7db63eb/?utm_source=claude_desktop)**
- Silvana M. Pesenti · 2021 · SSRN · 9 cit. · DOI 10.2139/ssrn.3878879
- *Finding:*
  - For a stress on the output, it derives the unique stressed output distribution closest in **Wasserstein** distance to the baseline, plus the stressed inputs.
  - Allowed stresses include mean and variance, any distortion risk measure (including VaR and ES), and expected-utility constraints.
  - Everything is computed from baseline Monte Carlo samples, and it is implemented in the R package SWIM.
- *Relevance:* A Wasserstein stress moves outcomes rather than only reweighting them. That addresses the KL support-blindness flagged in dossier §8 and verification finding R2 [inference].

**10. [Sensitivity analysis with χ2-divergences](https://consensus.app/papers/details/3ac0b7b157035b85b9267d48ad8b4100/?utm_source=claude_desktop)**
- V. Makam et al. · 2021 · *Insurance: Mathematics and Economics* · 4 cit. · DOI 10.1016/j.insmatheco.2021.06.007
- *Finding:*
  - The χ²-minimizing change of measure under an expectation stress has an explicit finite-space solution and needs only one simulated input/output set.
  - It supports both reverse and forward sensitivity metrics.
  - In a simulation study, χ²-based metrics have **lower sampling error** than KL-based ones.
- *Relevance:* For the Pesenti-style input ranking in dossier §6.11, χ² may give more stable rankings at 50k paths. KL can stay for worst-case bounds [inference].

**11. [Reverse stress testing: Scenario design for macroprudential stress tests](https://consensus.app/papers/details/79ce0dc1485c5694bd182547353503a4/?utm_source=claude_desktop)**
- M. Baes et al. · 2023 · *Mathematical Finance* · 10 cit. · DOI 10.1111/mafi.12373
- *Finding:*
  - An algorithmic reverse stress test that includes losses from distressed liquidations, given banks' optimal responses.
  - 10,000 worst-case scenarios cluster into 12 families, and each family tends to hit the same banks.
  - The authors call this an "Anna Karenina" principle: the precise scenario matters less than targeting the most vulnerable.
- *Relevance:* For ADIC the analogues are forced secondary sales and margin-driven liquidations. Cluster reverse-stress worlds into families and report which groups and holdings they consistently hit, rather than polishing one narrative [inference].

**12. [A financially justifiable and practically implementable approach to coherent stress testing](https://consensus.app/papers/details/8660b9ce52fe53fa8c47251b363d202b/?utm_source=claude_desktop)**
- R. Rebonato · 2018 · *Quantitative Finance* · 5 cit. · DOI 10.1080/14697688.2018.1532103
- *Finding:* Bayesian-net stress testing that satisfies consistency and continuity conditions. It cascades a scenario from a few macro-financial variables to the constituents of a granular portfolio, and gives "an approximate but robust estimate of the likelihood of a given scenario".
- *Relevance:* It fills two gaps in the dossier's narrative-to-numbers workflow (§6.10): cascading Bayesian-net scenarios down to group and asset P&L, and attaching a likelihood before entropy pooling [inference].

### C. Views and probability vectors

**13. [Entropy Pooling with Discrete Weights in a Time-Dependent Setting](https://consensus.app/papers/details/31c6342de05759f8964245b370c4dc8d/?utm_source=claude_desktop)**
- M. L. van der Schans · 2018 · *Computational Economics* · 0 cit. · DOI 10.1007/s10614-018-9824-7
- *Finding:*
  - Written for long-term investors who combine forecasting models with forward-looking market assumptions.
  - It applies computational entropy pooling to **sample paths** rather than to points.
  - A heuristic forces the weights to be discrete, so the adjusted forecast is a finite set of equally weighted scenarios.
  - It notes that allocations can be sensitive to small adjustments of the density.
- *Relevance:* This is ADIC's exact set-up: a CMA-anchored path ESG plus IC views. With discrete weights, tree builders and SDDP can consume the view posterior as plain paths [inference].

**14. [Effective Number of Scenarios in Fully Flexible Probabilities](https://consensus.app/papers/details/9602d72f6f065f43974fbfbb196c33bc/?utm_source=claude_desktop)**
- Attilio Meucci · 2012 · venue not shown · 7 cit. · (also stream 07)
- *Finding:* A method to count the effective number of scenarios when fully-flexible-probability weights are arbitrary, so that confidence intervals for risk numbers can be computed.
- *Relevance:* This is the uncited source of the dossier's ENS diagnostic. Verification finding R4 shows that, with uniform priors, the exp-entropy ENS equals N·exp(−KL). A Kish-type ESS should be added to detect weight concentration [inference].

**15. [Fusion of Probability Density Functions](https://consensus.app/papers/details/85c889118c0c59d2a8cee92119e0323f/?utm_source=claude_desktop)**
- Günther Koliander et al. · 2022 · *Proceedings of the IEEE* · 118 cit. · DOI 10.1109/jproc.2022.3154399
- *Finding:* A survey, with new results, on fusing several densities using axiomatic, optimization-based (divergence or distance minimization) and supra-Bayesian approaches.
- *Relevance:* A current reference for pooling IC members' posteriors (dossier §6.10), updating Genest & Zidek (1986) [inference].

### D. Regimes

**16. [Asset allocation with recursive parameter updating and macroeconomic regime identifiers](https://consensus.app/papers/details/b859291f240d53db8323f68bc6adf7dd/?utm_source=claude_desktop)**
- M. Goodarzi et al. · 2025 · *European Journal of Finance* · 1 cit. · DOI 10.1080/1351847x.2025.2465453
- *Finding:* With recursively updated regime parameters, performance improves substantially when regime dynamics are estimated from **macroeconomic data** rather than financial-return data. After the dot-com bust and 2008, return-based estimation identified extreme regimes, which led to "very extreme hedging demands".
- *Relevance:* Anchor ADIC's regime filter on macro identifiers such as growth, inflation and policy. Return, VIX and spread features can destabilize regimes after crises [inference].

**17. [Regime Shifts: Implications for Dynamic Strategies (corrected)](https://consensus.app/papers/details/9653830d96ae5137a61a7bb353eeef70/?utm_source=claude_desktop)**
- M. Kritzman et al. · 2012 · *Financial Analysts Journal* · 148 cit. · DOI 10.2469/faj.v68.n3.3
- *Finding:* Markov-switching models fitted to **drivers** (market turbulence, inflation, economic growth) show persistent "normal" and "event" regimes. Out of sample, a dynamic process beat static allocation, especially for investors who seek to avoid large losses.
- *Relevance:* This supports regimes defined on drivers rather than on asset returns, and gives names the IC can read. The dossier cites Kritzman's turbulence and absorption-ratio papers but not this one [inference].

### E. Multistage optimization and scenario trees

**18. [Partially observable multistage stochastic programming](https://consensus.app/papers/details/cea97fcf25c15378a878e9a8a393b54c/?utm_source=claude_desktop)**
- Oscar Dowson et al. · 2020 · *Operations Research Letters* · 14 cit. · DOI 10.1016/j.orl.2020.06.005
- *Finding:* Defines partially observable multistage stochastic programs with a Bayesian update of a belief-state vector. The cost-to-go functions have saddle-function properties, and the solution algorithm is derived from SDDP.
- *Relevance:* This answers verification finding R9. ADIC's regime is latent, so the SDDP policy graph should carry the belief state (the filtered regime probabilities) rather than the true regime [inference].

**19. [Scenario tree reduction for multistage stochastic programs](https://consensus.app/papers/details/53a49780d76c5f50a58604585c86eba2/?utm_source=claude_desktop)**
- H. Heitsch et al. · 2009 · *Computational Management Science* · 177 cit. · DOI 10.1007/s10287-008-0087-y
- *Finding:* A framework for reducing multistage trees so that optimal values and approximate solution sets stay close. "The important difference from scenario reduction in two-stage models consists in incorporating the filtration distance." It includes a node-removal algorithm that meets an error tolerance.
- *Relevance:* The dossier cites the 2003 algorithms for multistage training sets. Annual SELL / HOLD / REFINANCE / LEVER decisions need trees that preserve the information structure, which is what the filtration distance controls [inference]. The companion paper on tree construction is listed in §4.7.

**20. [Large-scale financial planning via a partially observable stochastic dual dynamic programming framework](https://consensus.app/papers/details/9e40ee775ba15434888d552a046a6c09/?utm_source=claude_desktop)**
- Jinkyu Lee et al. · 2023 · *Quantitative Finance* · 7 cit. · DOI 10.1080/14697688.2023.2221296 · (also stream 01)
- *Finding:* The stagewise-independence assumption is the major obstacle to SDDP in financial planning over several decades. The authors propose PO-SDDP: discrete-valued, partially observable Markov states plus feasibility cuts.
- *Relevance:* A precedent for ADIC's regime-driven, multi-decade plan. Feasibility cuts are a natural form for the Corporate Finance liquidity gate (T1-L) [inference].

**21. [Modeling time-dependent randomness in stochastic dual dynamic programming](https://consensus.app/papers/details/889e982ca4c8514ea4b791ce145b8493/?utm_source=claude_desktop)**
- N. Löhndorf et al. · 2019 · *EJOR* · 90 cit. · DOI 10.1016/j.ejor.2018.08.001 · (also streams 01, 03)
- *Finding:*
  - The Markov-chain version of SDDP closed its optimality bounds faster than the time-series version, and its policy dominated.
  - On real data, the quality of the stochastic model mattered.
  - An AV@R formulation made the policy "robust against a misspecified stochastic model".
- *Relevance:* This supports the dossier's Markov-regime policy graph. AV@R inside the optimizer is a cheap robustness device to pair with the KL and Wasserstein layer, as long as the two are not stacked carelessly (see #4) [inference].

### F. Private-markets block of the ESG

**22. [A Latent Factor Cash Flow Model for Alternative Investment Funds](https://consensus.app/papers/details/bb74f63a8fc15983a1e7753d4057d4f0/?utm_source=claude_desktop)**
- Wenbo Cao et al. · 2025 · *Financial Analysts Journal* · 1 cit. · DOI 10.1080/0015198x.2025.2489923 · (also streams 01, 04, 05)
- *Finding:*
  - It extends Takahashi-Alexander with systematic economic factors and fund-specific randomness in call and distribution rates, plus a factor-based public-market equivalent for growth.
  - This enables scenario analysis, stress testing, commitment design and multi-asset risk management.
  - It covers PE, real estate, private credit and infrastructure.
- *Relevance:* Published precedent for the dossier's regime-dependent call and distribution rates, γ_c(S_t, ·) and γ_d(S_t, ·, X^exit) (§6.3). The regime layer and the exit-activity index X^exit remain ADIC-specific [inference].

**23. [Cash-Flow Timing in Private Markets: Evidence from the PFD Framework](https://consensus.app/papers/details/bfcee2acb48956d2b7c78208c910bb46/?utm_source=claude_desktop)**
- Kang Shuang · 2026 · venue not shown (DOI 10.3905/jpmi.2026.1.013) · 0 cit.
- *Finding:*
  - Uses Preqin records for 7,904 funds from 1982 to 2025.
  - Timing differs systematically across asset classes, vintages, strategies and fund sizes: when contributions come in, how long breakeven takes, and when distributions arrive.
  - Funds with similar end-stage performance can have materially different liquidity profiles.
  - The paper calibrates Takahashi-Alexander to these timing metrics.
- *Relevance:* It gives calibration targets for γ_c and γ_d beyond TVPI and IRR. For the hybrid Secondaries book, strategy-level timing benchmarks help separate fund interests from direct deals [inference].

### G. Model risk management

**24. [Measuring Model Risk in Financial Risk Management and Pricing](https://consensus.app/papers/details/f680cc6e77c45512ad48cc1e8e11727e/?utm_source=claude_desktop)**
- Valeriane Jokhadze et al. · 2020 · *International Journal of Theoretical and Applied Finance* · 20 cit. · DOI 10.2139/ssrn.3113139
- *Finding:* Defines model-weighted and superposed market-risk measures over a space of models, axioms for model-risk measures, and superposed measures relative to a reference model. Probabilities on the model space can come from Bayesian analysis.
- *Relevance:* A formal answer to the dossier's open question 3 (provider weights). It also lets model risk be reported relative to the house model [inference].

**25. [Using iterative reverse scenario logic to manage model risk in financial climate risk assessment](https://consensus.app/papers/details/e930743850fe57cb9b0f30a5bd76f37f/?utm_source=claude_desktop)**
- M. Gerst et al. · 2026 · *Climatic Change* · 0 cit. · DOI 10.1007/s10584-026-04260-y
- *Finding:*
  - Current model risk management is insufficient when complex models are chained under deep uncertainty.
  - Reverse stress testing alone does not address the risks introduced by linking models.
  - The paper proposes "iterative reverse scenario logic": scenario discovery coupled with periodic expert judgment on plausibility, both within and across models.
- *Relevance:* ADIC chains ESG → private cash flows → overlay margin → liquidity gate. An agent loop with IC plausibility checkpoints maps directly onto this proposal [inference].

---

## 4. Missed-but-important papers: concrete design implications

References: [#n] is an entry in §3; [A#n] is an entry in §4.7.

### 4.1 State variables
- **Belief state.** Add b_t ∈ Δ^K, the filtered regime probabilities from the State/Fragility engine, as an explicit decision-state variable updated by Bayes' rule. The optimizer conditions on b_t, not on the true regime S_t [#18, #20, #5].
- **Regime identifiers.** Let a macro block (growth, inflation, policy rate, a turbulence index) drive the regime filter. Market variables such as VIX, spreads and skew then enter as regime-conditional factors rather than identifiers [#16, #17] [inference].
- **Private cash-flow states.**
  - Systematic call-rate and distribution-rate factors plus fund-level idiosyncratic shocks [#22].
  - Timing metrics (contribution, breakeven, distribution timing) by strategy and vintage as calibration targets [#23].
  - For the **hybrid Secondaries book**: fund interests follow factor Takahashi-Alexander dynamics. Direct deals and continuation vehicles need deal-level exit timing and exit-multiple states, as in [Modeling the exit cashflows of private equity fund investments](https://consensus.app/papers/details/06a53f89abd05350ae89e3e77c5fc5e6/?utm_source=claude_desktop) (Christian Tausch et al., 2022, *Journal of Risk*, DOI 10.21314/jor.2022.029) [inference; also stream 04].
- **Stress-path state.** In reverse-stress runs, carry the likelihood-ratio (distortion) process so stressed paths can be re-simulated with time- and state-dependent dynamics [#8].

### 4.2 Models
- **ESG regime engine.** Keep the regime-switching factor VAR, but estimate regime dynamics on macro identifiers. Report regime ambiguity as soft weights rather than hard K = 4 labels [#16, #17, A#13].
- **Cash-flow engine.** Use factor Takahashi-Alexander as primary [#22], with a historical-simulation Takahashi-Alexander as challenger [A#21].
- **Optimizer.**
  - POMSP or PO-SDDP over the belief state [#18, #20].
  - Markov-chain SDDP rather than the time-series form where dependence is regime-driven [#21].
  - The discrete SELL / HOLD / REFINANCE / LEVER actions and decision-dependent effects, such as a forced sale widening the secondary discount, need the newer policy-graph extensions [A#18]. The SDDP review [A#16] covers their assumptions.
- **Scenario trees.**
  - Build decision trees with multistage reduction that controls the filtration distance [#19, A#14, A#15].
  - Feed the entropy-pooling posterior into tree builders as equally weighted paths [#13].
  - Keep Heitsch-Römisch (2003) for reducing evaluation fans.
- **Robustness layer.**
  - Regime-conditional Wasserstein balls [#3].
  - f-divergence and Bregman alternatives to KL [#7].
  - Dynamic, path-dependent model-risk bounds for drawdown and minimum-liquidity metrics [A#4].
- **Reverse stress.**
  - Dynamic stressed measure plus re-simulation [#8].
  - Wasserstein reverse sensitivity via the SWIM approach [#9].
  - χ² sensitivity rankings [#10].
  - Clustering of worst-case worlds into families [#11].
- **Views.**
  - Discrete-weight path entropy pooling [#13].
  - Dynamic entropy pooling for views with different horizons [A#11].
  - Bayesian-net cascade with scenario likelihoods [#12].
  - An explicit, documented pooling rule [#15].

### 4.3 Parameters and calibration
- **Radius ↔ target.** Calibrate η and ε jointly with the target τ and publish the mapping [#1]. No values are asserted here.
- **Radius cross-check.** Compare the expert-disagreement radius (dossier §4.2) with a data-driven radius, such as the inference-based selection in [A#2].
- **Per-regime radii** [#3].
- **Persistence alternatives in the structured set,** for example multipliers on drought and crisis dwell times [#6]. Values are to be calibrated, and none are asserted here.
- **Detection-error calibration** of robustness parameters in a hidden-Markov setting [A#3].
- **Model weights.** Use a Bayesian posterior over the model space as the default, with IC-set weights as an override [#24].
- **Cash-flow calibration.**
  - Timing targets by strategy and vintage [#23].
  - Factor loadings of call and distribution rates [#22].

### 4.4 Constraints
- **T1-L liquidity gate as feasibility cuts** in PO-SDDP, owned by the Corporate Finance / Treasury seat [#20] [inference].
- **No compounding of rectangular ambiguity.** If nested CVaR or AV@R is applied per stage, either reduce the path-law η or drop one layer, and document which [#4, #21] [inference].
- **Unfunded-commitment stress.**
  - GPs may accelerate drawdowns to avoid LP default ([A#20], also streams 01, 02, 04, 05, 06).
  - So stressed capital calls can rise when ADIC is liquidity-constrained [inference].
- **Support-blindness fix for rare liquidity breaches.**
  - Use a Wasserstein-type reverse stress [#9] together with importance sampling.
  - This agrees with verification finding R2.

### 4.5 Objectives
- **T1-F floor.**
  - Use estimation-fortified robust satisficing where the floor depends on group forecasts [#2].
  - RS admits two-sided confidence intervals for the optimal loss [A#1].
- **Tier 2.** AV@R inside SDDP is a cheap robustness complement [#21].
- **IC output.** Present a single robustness frontier (DRO radius ↔ RS target) rather than parallel worst-case and fragility figures [#1].

### 4.6 Agent and IC design
- **Robustness Auditor.**
  - Computes the radius ↔ target mapping [#1].
  - Reports per-regime radii [#3].
  - Flags stacked stagewise and path-law pessimism [#4].
- **Stress Narrator.**
  - Re-simulates under the stressed dynamics and describes how the failure unfolds [#8].
  - Presents clustered failure families and the ADIC groups each one hits [#11].
- **View Elicitor.**
  - Tags each view with its horizon [A#11].
  - Cascades Bayesian-net scenarios to holdings, with likelihoods [#12].
  - Records the pooling rule [#15].
- **MRM Validator.**
  - Reports model-risk measures relative to the reference model [#24, A#22].
  - Runs iterative reverse scenario logic, with IC plausibility checkpoints across the chained models [#25].
  - Uses importance-sampling estimators when evaluating risk-averse policies [A#17].
- **Treasurer / Corporate Finance seat.**
  - Owns T1-L, the liquidity reverse stress, the feasibility cuts and the contingency funding plan.
  - This follows the user's 18 Oct 2026 statement that Corporate Finance owns Treasury [inference].
- **Secondaries and Capital Solutions as data sources.**
  - Their quotes feed the secondary discount δ and the NAV-loan spreads, subject to conflict controls (context file §1A).
  - [#11] shows liquidation losses are endogenous in stress. So δ should respond to ADIC's own forced sales in crisis paths [inference].

### 4.7 Additional relevant papers surfaced (not annotated)
- **A1.** [Statistical Properties of Robust Satisficing](https://consensus.app/papers/details/ec7b49fac25151bbb3bad9f0bd652859/?utm_source=claude_desktop). Zhiyi Li et al., 2024, arXiv, DOI 10.48550/arxiv.2405.20451.
  - Two-sided confidence intervals for the optimal loss and finite-sample generalization bounds.
  - Results extend to distribution shift, and RS is less sensitive to hyperparameter tuning than DRO.
- **A2.** [Distributionally Robust Mean-Variance Portfolio Selection with Wasserstein Distances](https://consensus.app/papers/details/f8bd5e6f959e5c1a93dd3ebb5eed9aaa/?utm_source=claude_desktop). J. Blanchet et al., 2018 (Consensus year), *Management Science*, 175 cit., DOI 10.1287/mnsc.2021.4155.
  - The robust problem reduces to regularized variance minimization.
  - The size of the uncertainty set and the robust target return are selected from data.
- **A3.** [Robust hidden Markov LQG problems](https://consensus.app/papers/details/a82f4368ac5c5b40ae2b366bf588635e/?utm_source=claude_desktop). L. Hansen et al., 2010, *JEDC*, DOI 10.1016/j.jedc.2010.05.004. Detection-error probabilities calibrate robustness parameters in hidden Markov models.
- **A4.** [Non-Parametric Robust Model Risk Measurement with Path-Dependent Loss Functions](https://consensus.app/papers/details/3858b29a97b057c4a6bf0784637595c7/?utm_source=claude_desktop). Yu Feng, 2019, SSRN, DOI 10.2139/ssrn.3659110. Extends Glasserman-Xu to dynamic, path-dependent losses under any f-divergence.
- **A5.** [Generalized Robustness and Dynamic Pessimism](https://consensus.app/papers/details/9adb7ee3480f51ca81cae5361be7fef3/?utm_source=claude_desktop). Pascal J. Maenhout et al., 2020, NBER w26970, DOI 10.3386/w26970. Replacing relative entropy with Cressie-Read discrepancies makes distorted beliefs an endogenous state; estimated pessimism has a business-cycle component.
- **A6.** [The Uniqueness of Exponential Second-Order Expected Utility](https://consensus.app/papers/details/1388c96e6eb85e70ace8abf79020e4cf/?utm_source=claude_desktop). Yosuke Hashidate, 2026, arXiv. Within the power-divergence family, only KL has a log-sum-exp dual. This supports the dossier's computational choice.
- **A7.** [A theory of multivariate stress testing](https://consensus.app/papers/details/2948d4e03961525f9669f768f3bc530a/?utm_source=claude_desktop). Pietro Millossovich et al., 2024, *EJOR*. Dependence-focused stressing mechanisms that are invariant to monotone transformations; useful for stressing correlations by regime.
- **A8.** [Numerical Computation of Worst-Case Distributions in Monte Carlo Portfolio Risk Management](https://consensus.app/papers/details/d13bcd91cd9d580b8acb259022d53b21/?utm_source=claude_desktop). M. Jandačka et al., 2026, *Journal of Applied Mathematics*, DOI 10.1155/jama/3089179. Implements the Breuer-Csiszár worst case inside Monte Carlo as a one-dimensional root-finding problem, which supports the dossier's R2 implementation. Worst cases can be much larger than standard stress scenarios.
- **A9.** [A macroeconomic reverse stress test](https://consensus.app/papers/details/b1f5554c333f5d2d8375dd7079bc41f8/?utm_source=claude_desktop). P. Grundke et al., 2017, *Review of Quantitative Finance and Accounting*. Reverse stress results are "exposed to considerable model and estimation risk", so "numerous robustness checks" are needed.
- **A10.** [Quantitative reverse stress testing, bottom up](https://consensus.app/papers/details/9b0cec26825a5693835caccb7f69cd57/?utm_source=claude_desktop). C. Albanese et al., 2023, *QF*. Mines simulated future states for forward-looking fragilities, with liquidity-risk and model-validation applications.
- **A11.** [Dynamic portfolio management with views at multiple horizons](https://consensus.app/papers/details/2e6d41892d2d5ec88144b81f8ac418b8/?utm_source=claude_desktop). Attilio Meucci et al., 2016, *Applied Mathematics and Computation* (also stream 07). Dynamic entropy pooling for non-synchronous views with "life spans ranging from minutes to years".
- **A12.** [Sequential Entropy Pooling Heuristics](https://consensus.app/papers/details/824adf298b5757abba1cabcbfe824a8c/?utm_source=claude_desktop). Anton Vorobets, 2021, SSRN, DOI 10.2139/ssrn.3936392. Consensus returned no abstract. Probably the method behind fortitudo.tech's SeqEP, since the dossier credits that package to Vorobets [inference].
- **A13.** [Policy Regimes versus Economic Regimes: Implications for Portfolio Construction](https://consensus.app/papers/details/fa9778c63f5d50aca8e7eb12878f07fe/?utm_source=claude_desktop). M. Kritzman et al., 2026, DOI 10.3905/jpm.2026.006. Weights historical observations by "relevance" instead of rigid regime labels; incorporating regime ambiguity "yields clearer allocation guidance".
- **A14.** [Scenario tree modeling for multistage stochastic programs](https://consensus.app/papers/details/bf5079db0e675925a6c69ead4095086a/?utm_source=claude_desktop). H. Heitsch et al., 2009, *Mathematical Programming*, 342 cit., DOI 10.1007/s10107-007-0197-2. Forward and backward tree generation by recursive reduction and bundling, with stability conditions.
- **A15.** [Dynamic generation of scenario trees](https://consensus.app/papers/details/e9963a43a6a654f7b5e0e1c50261e7f2/?utm_source=claude_desktop). G. Pflug et al., 2015, *COA*, DOI 10.1007/s10589-015-9758-0. The tree structure adapts to meet a transportation-distance criterion for stochastic processes.
- **A16.** [Stochastic Dual Dynamic Programming and Its Variants: A Review](https://consensus.app/papers/details/7db5dd5169e35ac19c12c5e823524ce0/?utm_source=claude_desktop). Christian Füllner et al., 2025, *SIAM Review*, DOI 10.1137/23m1575093.
- **A17.** [Evaluating policies in risk-averse multi-stage stochastic programming](https://consensus.app/papers/details/ba034cb15d615ded9ac6216ca2b0251d/?utm_source=claude_desktop). V. Kozmík et al., 2014, *Mathematical Programming*. The standard upper-bound estimator performs poorly under risk aversion; importance-sampling estimators fix this. Applied to multi-stage asset allocation.
- **A18.** [MDP modeling for multi-stage stochastic programs](https://consensus.app/papers/details/a92ef4525fd450859f6621430f1de867/?utm_source=claude_desktop). David P. Morton et al., 2025, *Mathematical Programming*. Policy graphs with decision-dependent transition probabilities, plus SDDP variants that approximate non-convexities.
- **A19.** [A Dynamic Model of Private Asset Allocation](https://consensus.app/papers/details/da8e4aa55bd25aca8a43f6c4444f3334/?utm_source=claude_desktop). Hui Chen et al., 2025, arXiv.
  - Models illiquidity, commitment-call-distribution lags, business-cycle states and serially correlated observed returns, and uses machine-learning policies.
  - This is a close academic analogue for the optimizer stream.
- **A20.** [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop). Vincent Maurin et al., 2022, *Management Science* (also streams 01, 02, 04, 05, 06).
- **A21.** [Takahashi–Alexander Revisited](https://consensus.app/papers/details/be3095d7eb5f506bad9e4cc2743d1096/?utm_source=claude_desktop). Dawson Beutler et al., 2023, DOI 10.3905/jpm.2023.1.496 (also stream 04).
- **A22.** [Assessing financial model risk](https://consensus.app/papers/details/82e1d8eab5c75d8684b3d1b950f19af6/?utm_source=claude_desktop). P. Barrieu et al., 2013 (Consensus year), *EJOR*, 87 cit., DOI 10.1016/j.ejor.2014.10.032. Absolute, relative and local measures of model risk.
- **A23.** [Model Risk Management](https://consensus.app/papers/details/30bef0615c3e576180a5b36e57fd893d/?utm_source=claude_desktop). Ludger Rüschendorf et al., 2023, CUP book, DOI 10.1017/9781009367189. Tools to quantify model uncertainty and the best upper and lower risk bounds for risk-aggregation functionals. Useful for private assets whose joint dependence is poorly identified [inference].
- **A24.** [Model risk management in stress testing: The road up to here](https://consensus.app/papers/details/d4096d3d56975f81868d8befbab120fc/?utm_source=claude_desktop). Eduardo Canabarro, 2024, *Journal of Risk Management in Financial Institutions*. How to interpret stress-test results in the presence of model risk.
- **A25.** [Tough enough? Robust satisficing as a decision norm for long-term policy analysis](https://consensus.app/papers/details/7ce39126af765f0f8c6c317c1a2adda4/?utm_source=claude_desktop). Andreas L. Mogensen et al., 2022, *Synthese*. See §5.
- **A26.** [Economic Scenario Generation with Regime Switching Models](https://consensus.app/papers/details/bc86c79fcbf55c59b89ea249cf1965c5/?utm_source=claude_desktop). M. Sherris et al., 2009, SSRN. ESG design for insurance and superannuation; historical data are limited relative to the number of parameters.
- **A27.** [The importance of considering regimes in long‐term asset allocation to real estate](https://consensus.app/papers/details/66a0c64db3b75fdc8b69e8bd067a3579/?utm_source=claude_desktop). Massimo Guidolin et al., 2026, *Real Estate Economics*.
  - Allocations become less sensitive to the prevailing regime as the horizon lengthens.
  - This supports using regimes for near-term paths and CMA anchors for the long run, as the dossier's ergodic matching does [inference].

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier recommendation (section) | Challenging paper(s) | What the paper says | Implication [inference] |
|---|---|---|---|---|
| 1 | SDDP on a Markovian policy graph "maps one-to-one onto a regime ESG" and is "the best fit" (§3, §6.7) | Lee et al. 2023 [#20]; Dowson et al. 2020 [#18] | Stagewise independence is the major obstacle to SDDP in finance. They propose partially observable Markov states and belief-state SPs. | ADIC's regime is latent. Use POMSP or PO-SDDP, or state explicitly that the regime is treated as observed (a look-ahead). Agrees with verification finding R9. |
| 2 | Heitsch-Römisch (2003) forward/backward reduction for multistage training scenarios (§3, §6.7) | Heitsch et al. 2009 [#19], [A#14] | Multistage reduction must incorporate "the filtration distance". | Use the 2009 tree methods for decision trees and the 2003 algorithms only for evaluation fans. |
| 3 | IC card shows KL/W1 worst cases and η\*/k\* as separate instruments (§6.8-6.9) | Wang et al. 2025 [#1] | DRO and RS share the same solution family under Wasserstein, with a radius ↔ target correspondence. | Show one frontier and avoid double-counting. The equivalence is proved for Wasserstein, so the KL case needs its own check. |
| 4 | Tier-2 "KL-robust expected utility" plus risk-averse SDDP à la Philpott-de Matos (§3, §6.9) | Blanchet et al. 2025 [#4] | Time-rectangular distributionally robust control is over-pessimistic; prefer prior-level ambiguity. | Do not stack stagewise robustness on top of the path-law KL ball; calibrate the layers jointly. |
| 5 | Structured ambiguity = CMA-provider means + KL ball, η = 0.10 (§1 #5, §6.6) | Hansen et al. 2019 [#6]; Hansen & Sargent 2007 [#5] | Worst-case fears load on the persistence of bad states. A hidden-state prior needs its own robustness operator. | Add alternative transition matrices to the structured set, and robustness on the regime posterior. Echoes verification finding R8 (means-only ambiguity). |
| 6 | Regimes fitted on about 20 monthly factors including VIX, skew and spreads; fixed K = 4 labels (§1 #6, §6.2) | Goodarzi et al. 2025 [#16]; Kritzman et al. 2026 [A#13] | Macro-identified regimes outperform return-identified ones, and return-based regimes become extreme after crises. Regime ambiguity is better handled with relevance weights than rigid labels. | Anchor regime identification on macro drivers and treat the regime labels as soft. |
| 7 | KL as the default divergence for Pesenti-style sensitivity ranking (§6.11) | Makam et al. 2021 [#10]; Breuer & Csiszár, *Mathematical Finance* [#7]; Maenhout et al. 2020 [A#5] | χ²-based sensitivity metrics have lower sampling error. Other divergences are valid and change tail behaviour or the dynamics of pessimism. | Use χ² for rankings and keep KL for bounds. Counterpoint: only KL has the log-sum-exp dual [A#6]. |
| 8 | "All robustness, stress-testing and IC-view work is then a reweighting … or a transport" of one fixed matrix (§1 #1) | Kroell et al. 2022 [#8]; Pesenti 2021 [#9] | A stressed measure changes the dynamics themselves (time- and state-dependent). Wasserstein stresses move outcomes. | Re-simulate under the stressed dynamics for path narratives and rare liquidity events. The dossier already re-simulates for structural views; extend that to reverse stress. |
| 9 | Robust satisficing (k\*) as the Tier-1 floor objective (§6.9) | Mogensen et al. 2022 [A#25] | RS may draw its plausibility from implicit probabilities, and choosing a satisficing norm over a robustness-sensitive optimizing norm is not settled. | Keep the Tier-2 optimizing objective. Document why a satisficing floor is adopted and how τ is chosen. |
| 10 | Takahashi-Alexander as "the industry template", made stochastic and regime-dependent (§5, §6.3) | Beutler et al. 2023 [A#21]; Shuang 2026 [#23] | Takahashi-Alexander is sensitive to its assumptions and gives no range of outcomes, which breeds overconfidence. Funds with similar end performance can have very different liquidity profiles. | Run a historical-simulation challenger and calibrate timing metrics, not only multiples. |
| 11 | Bayesian-net plus entropy-pooling "narrative-to-numbers" view workflow (§6.10) | Rebonato & Denev, [How to use Bayesian nets: our recommended approach](https://consensus.app/papers/details/66affcb339f853c2a1fd9e09d0c29bcd/?utm_source=claude_desktop) and [Analysis of portfolio allocation](https://consensus.app/papers/details/73db0b6d3f305208943f4e604fe1a0ba/?utm_source=claude_desktop) (CUP chapters); Baes et al. 2023 [#11] | It would be "foolhardy" to read off with confidence a single set of allocations from a Bayesian net, because allocations are "very sensitive to the precise values of the expected returns". The precise scenario specification matters less than targeting vulnerabilities. | Views must pass through the robustness layer before they move allocations. Focus reverse stress on vulnerabilities (liquidity gate, unfunded commitments, margin) rather than narrative detail. |

**Evidence that supports the dossier** (for balance):
- Löhndorf et al. 2019 [#21] supports the Markov-chain form of SDDP.
- Pun et al. 2023 [#3] supports combining regimes with DRO.
- Cao et al. 2025 [#22] supports factor- and regime-dependent cash flows.
- Jandačka et al. 2026 [A#8] supports the one-dimensional root-finding implementation of the KL worst case on Monte Carlo scenarios.
- Hashidate 2026 [A#6] supports KL's computational convenience.
- Guidolin et al. 2026 [A#27] supports regimes for near-term paths with long-run CMA anchoring.

---

## 6. Usage message (verbatim, last one returned)

> 20 searches left this month; resets to 500 on November 1st.

---

## Appendix A. Consensus search log
All 11 searches were run one at a time, with the query parameter only. The counter is the remaining monthly quota after each search; drops larger than 1 reflect the two other agents searching at the same time.

| # | Query | Purpose (seed / citations) | Remaining after |
|---|---|---|---|
| 1 | Robust satisficing Long Sim Zhou fragility target | seed "robust satisficing"; Long et al., Brown & Sim, Aumann & Serrano | 49 |
| 2 | Meucci fully flexible views entropy pooling scenario probabilities | seed "entropy pooling fully flexible views"; Meucci 2008 | 46 |
| 3 | stress testing worst-case distribution relative entropy plausibility model risk reverse sensitivity | seed "reverse stress testing"; Breuer & Csiszár, Pesenti et al., Glasserman, Kang & Kang | 43 |
| 4 | distributionally robust portfolio optimization Wasserstein ambiguity set | seed "distributionally robust portfolio optimization Wasserstein"; Mohajerin Esfahani & Kuhn, Gao & Kleywegt, Xie | 39 |
| 5 | regime switching models for long-term asset allocation and economic scenario generation | seed "economic scenario generator regime switching" (refined); Guidolin & Timmermann, Ang & Bekaert | 36 |
| 6 | stochastic model of private equity fund cash flows capital calls distributions Takahashi Alexander | Takahashi & Alexander; cash-flow backfill | 35 |
| 7 | structured ambiguity model misspecification relative entropy robust risk measurement Hansen Sargent Glasserman Xu | Hansen & Sargent 2022 and 2001, Anderson, Hansen & Sargent, Glasserman & Xu | 31 |
| 8 | scenario tree generation and scenario reduction for multistage stochastic programming optimal discretization moment matching | Pflug 2001, Heitsch & Römisch, Høyland & Wallace | 29 |
| 9 | stochastic dual dynamic programming Markov chain policy graph partially observable risk averse multistage | Dowson 2020, Dowson & Kapelevich, Philpott & de Matos; verification finding R9 gap | 27 |
| 10 | Portfolio management under stress Bayesian net approach coherent asset allocation stress scenarios | Rebonato & Denev 2014 | 23 |
| 11 | model risk management validation quantification of financial model risk | seed "model risk management validation" | 20 |

## Appendix B. Non-Consensus metadata sources (WebSearch and Crossref)
- **Takahashi & Alexander (2002).**
  - The WebSearch did not return the record, only citing works: [Strategic Asset Allocation with Illiquid Alternatives](https://arxiv.org/pdf/2207.07767), [NBER w25559](https://www.nber.org/system/files/working_papers/w25559/w25559.pdf) and [The Endowment Model and Modern Portfolio Theory](https://conference.nber.org/conf_papers/f103442.pdf).
  - Crossref confirmed the metadata: <https://api.crossref.org/works/10.3905/jpm.2002.319836>.
- **Gao & Kleywegt.**
  - WebSearch: [arXiv 1604.02199v3](https://arxiv.org/abs/1604.02199v3), [Georgia Tech ISyE page](https://www.isye.gatech.edu/node/9890), [MIT ORC page](https://orc.mit.edu/?p=5553).
  - Crossref: <https://api.crossref.org/works/10.1287/moor.2022.1275>.
- **Xie.** Crossref query: <https://api.crossref.org/works?query.bibliographic=On+distributionally+robust+chance+constrained+programs+with+Wasserstein+distance+Xie&rows=3>.
- **Shu, Yu & Mulvey.** Crossref query: <https://api.crossref.org/works?query.bibliographic=Downside+risk+reduction+using+regime-switching+signals+statistical+jump+model+approach+Shu+Yu+Mulvey&rows=3>.
- **Incidental finds, not checked in Consensus.** The Takahashi-Alexander WebSearch surfaced two papers directly relevant to ADIC's endowment model:
  - *The Endowment Model and Modern Portfolio Theory* (NBER conference paper). The search summary attributes a related "natural liquidity" argument to Dimmock, Wang & Yang, NBER WP 25559.
  - *Strategic Asset Allocation with Illiquid Alternatives* (arXiv 2207.07767). This is probably the Luxenberg et al. ICAIF '22 paper that stream 04 already covers [inference].
  - Stream 02 (endowment and SWF) should confirm whether it cites the Dimmock, Wang & Yang paper.
