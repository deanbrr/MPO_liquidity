# Topic 11 (objectives): re-check of the citations the Consensus quota left unchecked

**Date:** 2026-10-18

**Scope:** the 6 works marked "not checked (quota)" in `research/literature/11_objectives.lit.md` (§1; §2 rows 2, 4, 6, 13, 20 and 26; §7), as cited in `research/dossiers/11_objectives.md`. The dossier was not edited.

**Method:**
- Crossref REST API: DOI records for Browne (1997), Campi & Garatti (2008), Ruszczyński (2010) and Avanzi (2009); bibliographic queries for Föllmer & Leukert (1999) and Fishburn (1977).
- RePEc/IDEAS pages: metadata for Fishburn, which has no Crossref record; abstracts for Föllmer & Leukert (1999) and Avanzi.
- Full texts that are openly accessible, with text extracted locally using pypdf:
  - Campi & Garatti (2008), author copy;
  - the Föllmer & Leukert (2000) preprint.
- Citing papers, used where the cited paper itself was paywalled:
  - Manganelli (2006 draft), for Fishburn's Theorem 2;
  - Jiang & Powell (arXiv:1509.01920), for Ruszczyński's time-consistency result;
  - Bayraktar & Young (arXiv:math/0703824), for Browne's safe level;
  - Angoshtari, Bayraktar & Young (arXiv:1806.07499), for the scope of Avanzi's survey.
- The Rutgers RUTCOR page, for the Ruszczyński abstract. Crossref and Semantic Scholar have no abstract for that paper.
- Six WebSearches, to find openly accessible copies or citing descriptions.
- Two of the PDFs (Campi & Garatti; Manganelli) were already in the session scratchpad from an earlier, unfinished run. I fetched both again from the URLs below, and the SHA-256 hashes matched before I used them.
- Sources not used:
  - OpenAlex returned HTTP 429 (Retry-After 35,157 s).
  - Springer article pages redirect to a login.
  - Consensus.

**Result:** 6 checked. 5 ok, 0 not found, 0 mismatched, 1 usage problem (minor). None is fabricated.
- The metadata in all six §10 entries is correct. This agrees with the verification log.
- **Usage problem.** §6.5 (l. 416) applies Browne's "danger zone" with a threshold that is not Browne's (note 1).
- **Reference hygiene.** The Föllmer & Leukert (2000) follow-up quoted in §2.1 is still missing from §10 (note 2).
- **Precision.**
  - The scenario-approach table does not state β.
  - The formula it uses is Campi & Garatti's Theorem 2.4, not Calafiore & Campi's bound (note 4).
- **Optional.** Add a DOI for Föllmer & Leukert (1999), and tighten the wording of the Avanzi bullet (note 6).

## Verdicts

| Citation (dossier §10) | Verdict | Correction | Source URL |
|---|---|---|---|
| Browne, S. (1997). Survival and growth with a liability: optimal portfolio strategies in continuous time. *MOR* 22(2):468–493. DOI 10.1287/moor.22.2.468 (l. 560; used in §2.2 l. 109 and §6.5 l. 416) | usage problem (minor; §6.5 only). Metadata ok; §2.2 usage accurate | Metadata: no change. Crossref gives Sid Browne, May 1997, with the full title as cited. §2.2 matches the abstract. §6.5: Browne's danger zone is bounded by the riskless rate (wealth below c/r), not by the 6.8% payout sustainable at a 10% return. At the dossier's 3.5% cash rate, a fixed 5% payout is already inside it. Reword (note 1). | https://api.crossref.org/works/10.1287/moor.22.2.468 · https://arxiv.org/abs/math/0703824 |
| Föllmer, H., Leukert, P. (1999). Quantile hedging. *F&S* 3(3):251–273 (l. 564; used in §2.1 l. 84) | ok; usage accurate | Metadata: no change. Optional: add DOI 10.1007/s007800050062 (Crossref). The follow-up quoted in §2.1 is still missing from §10. Add: Föllmer, H., Leukert, P. (2000). Efficient hedging: cost versus shortfall risk. *Finance and Stochastics* 4(2):117–146. DOI 10.1007/s007800050008 (note 2). | https://api.crossref.org/works?query.bibliographic=Quantile+hedging+Follmer+Leukert+Finance+and+Stochastics&rows=5 · https://ideas.repec.org/a/spr/finsto/v3y1999i3p251-273.html · https://www2.mathematik.hu-berlin.de/~foellmer/papers/hedges_57.pdf |
| Fishburn, P.C. (1977). Mean-risk analysis with risk associated with below-target returns. *AER* 67(2):116–126 (l. 566; used in l. 17, l. 23, §2.1 l. 88–93, §3.1 l. 188, §6.5 l. 418) | ok; usage accurate (via a citing source) | Metadata: no change. RePEc gives March 1977, pp. 116–126. Crossref has no record, so there is no DOI to add. The usage is confirmed through Manganelli's restatement of Fishburn's Theorem 2 [unverified against Fishburn's own text: no abstract is online and JSTOR was not accessed] (note 3). | https://ideas.repec.org/a/aea/aecrev/v67y1977i2p116-26.html · https://igier.unibocconi.eu/sites/default/files/media/attach/Manganelli_160107.pdf |
| Campi, M., Garatti, S. (2008). The exact feasibility of randomized solutions of uncertain convex programs. *SIAM J. Optim.* 19(3):1211–1230. DOI 10.1137/07069821X (l. 583; used in §2.3 l. 121–128) | ok; usage accurate | Metadata: no change. Crossref gives M. C. Campi and S. Garatti, online 19 Nov 2008. The dossier's formula is Theorem 2.4, eq. (2.2). Two precision fixes (note 4): state β = 10⁻⁶ under the N table, and credit the binomial-tail formula to Campi & Garatti (2008). Calafiore & Campi (2006) give the looser bound C(N,d)(1−ε)^(N−d). | https://api.crossref.org/works/10.1137/07069821X · https://garatti.faculty.polimi.it/Publications/Journals/2008_campi-garatti.pdf |
| Ruszczyński, A. (2010). Risk-averse dynamic programming for Markov decision processes. *Math. Programming* 125(2):235–261. DOI 10.1007/s10107-010-0393-3 (l. 595; used in §2.5 l. 151) | ok; usage accurate (via a citing source) | Metadata: no change. Crossref gives online 21 Jul 2010, print Oct 2010. The abstract does not mention time consistency, but a citing paper states the theorem the dossier relies on (note 5). | https://api.crossref.org/works/10.1007/s10107-010-0393-3 · https://rutcor.rutgers.edu/Ruszczynski.html · https://arxiv.org/abs/1509.01920 |
| Avanzi, B. (2009). Strategies for dividend distribution: a review. *NAAJ* 13(2):217–251. DOI 10.1080/10920277.2009.10597549 (l. 606; used in §2.6 l. 174–175) | ok; usage broadly accurate | Metadata: no change. Crossref gives print April 2009. Optional wording fixes: de Finetti's criterion is expected discounted dividends until ruin, so it does not control ruin directly. Avanzi's abstract does not cover ratcheting (note 6). | https://api.crossref.org/works/10.1080/10920277.2009.10597549 · https://ideas.repec.org/a/taf/uaajxx/v13y2009i2p217-251.html · https://arxiv.org/abs/1806.07499 |

## Notes

**1. Browne (1997): the "danger zone".**
- **§2.2 (l. 109) is accurate.** The Crossref abstract describes the following:
  - an investor "forced to withdraw funds continuously at a fixed rate per unit time (e.g., to pay for a liability, to consume, or to pay dividends)", with risky stocks and "a riskless asset which has a constant rate of return";
  - "The fact that the withdrawal is continuously enforced, regardless of the wealth level, ensures that there is a region where there is a positive probability of ruin. In the complementary region ruin can be avoided with certainty. Call the former region the danger-zone and the latter region the safe-region."
- **§6.5 (l. 416) puts the boundary in the wrong place.**
  - The row argues as follows: a payout on lagged NAV lifts the effective rate from 5% to ~7.1%, which is "above the ~6.8% sustainable at 10% return", so the fund "enters Browne's 'danger zone'".
  - In Browne's model the boundary is the safe level c/r. This is the wealth at which the fixed withdrawal c can be paid forever from the riskless asset alone. Bayraktar & Young (2007, p. 7) write that Browne (1997) "sought to maximize the probability of hitting the safe level, c/r, before reaching zero wealth". [unverified in Browne's own text: the MOR full text is paywalled, and the abstract does not state the boundary.]
  - The boundary therefore depends on the riskless rate, not on the expected return. The dossier's cash rate is 3.5% nominal, about 1% real at 2.5% inflation. At that rate a fixed 5% payout is already inside Browne's danger zone. The 30% fall moves the fund deeper into the zone; it does not move it into the zone.
  - The row's economic point still stands: the payout rises above the rate that is sustainable in expectation. Only the Browne label is wrong.
  - Browne's withdrawal is a fixed amount per unit time. The analogy therefore fits a payout fixed on lagged or average NAV, as the row assumes, better than one set as a percentage of current NAV.
- **Suggested wording:** "…a 5% minimum then becomes ~7.1%, above the ~6.8% sustainable at a 10% return, so the payout is no longer sustainable in expectation [I]. In Browne's (1997) terms, ruin has positive probability under every policy (the 'danger zone') whenever the fixed payout exceeds what the riskless asset alone can fund, which is already true at 5%."

**2. Föllmer & Leukert (1999) and the missing follow-up.**
- **The 1999 usage is accurate.**
  - The IDEAS abstract says the paper studies "what an investor can do who is unwilling to spend that much [the superhedging capital], and who is ready to use a hedging strategy which succeeds with high probability".
  - Its keywords include "Neyman Pearson lemma" and "value at risk".
- **The usage of the follow-up is accurate.** It was checked against the author-hosted preprint of Föllmer & Leukert (2000):
  - Abstract: "In a previous paper we determined quantile hedges which succeed with maximal probability, given a capital constraint. Here we look for strategies which minimize the shortfall risk defined as the expectation of the shortfall weighted by some loss function."
  - Introduction: quantile hedging is "a dynamic version of the static Value at Risk concept" that "does not take into account the size of the shortfall but only the probability of its occurrence".
  - §2 describes the earlier problem as finding a strategy "which minimizes the probability of a shortfall" under a constraint on initial capital. This matches the dossier's "maximizes the probability of a successful hedge under a budget".
- **Still missing from §10.** The lit file and the verification log both flagged this. Crossref metadata: Föllmer, H., Leukert, P. (2000). Efficient hedging: cost versus shortfall risk. *Finance and Stochastics* 4(2):117–146. DOI 10.1007/s007800050008.

**3. Fishburn (1977).**
- No abstract is online; IDEAS says "No abstract is available for this item". Crossref has no record of the article.
- Manganelli (draft of 25 Oct 2006, *Asset Allocation by Penalized Least Squares*) restates the paper:
  - risk terms ∫_{−∞}^t |t−y|^α dF(y) "were employed by Fishburn (1977)";
  - "Fishburn (1977) (see his theorem 2) shows" that the consistent von Neumann–Morgenstern utility is u(y) = y for y > t and u(y) = y − h(t−y)^α for y ≤ t;
  - "Values of α greater than 1 imply risk aversion with regard to returns below target, α = 1 implies risk neutrality, and α < 1 is associated with risk seeking behavior";
  - "Fishburn's class of risk measures includes the Safety First criterion of Roy (1952) and the semivariance of Markowitz (1959)".
- **So the dossier's usage is accurate.** This covers:
  - the measure E[(t−R)_+^α];
  - α = 0 as the shortfall probability (safety first);
  - α = 1 as risk-neutral expected shortfall;
  - α = 2 as below-target semivariance;
  - α < 1 risk-seeking and α > 1 risk-averse;
  - §6.5's "α ≥ 1 is never risk-seeking below target".
- **Optional support for the default α = 2.** Manganelli adds that "it is only for α ≥ 2 that the (α,t) efficient set is a subset of third order stochastically non-dominated portfolios", citing Bawa (1975) and Fishburn (1977).
- **Not a citation issue.** l. 23 calls P(10%) "the most risk-seeking criterion possible". α = 0 is only the boundary of Fishburn's family; the verification log's reasoning section already flags this overstatement.

**4. Campi & Garatti (2008).**
- **Theorem 2.4 of the author copy:** under Assumption 1, P^N{V(x*_N) > ε} ≤ Σ_{i=0}^{d−1} C(N,i) ε^i (1−ε)^(N−i). The bound holds with equality for fully supported problems.
  - d is the dimension of the decision vector (x ∈ R^d), and N is the number of sampled constraints.
  - Assumption 1: every sampled instance is feasible with nonempty interior, and its solution exists and is unique. Existence and uniqueness are assumed to simplify the presentation; §2.1, point 5, explains how to relax them.
  - So the dossier's certificate (l. 121) is accurate.
- **β is not stated.** I recomputed the table's N values from this formula.
  - At β = 10⁻⁶ the formula reproduces 3,260 / 9,086 / 27,418 / 1,801 exactly.
  - At β = 10⁻³ they would be 2,259 / 7,460 / 24,633 / 1,482.
  - Add "β = 10⁻⁶" to the table. This is verification R8.
- **Attribution.** The binomial-tail formula is Campi & Garatti's.
  - The "key result" of Calafiore & Campi (2006), which is their ref. [6], is the looser bound P^N{V(x*_N) > ε} ≤ C(N,d)(1−ε)^(N−d).
  - Campi & Garatti say their bound "outperforms the previous bound from [6], at times by a huge extent".
  - Suggested wording: "the scenario approach (Calafiore & Campi 2006), with the exact bound of Campi & Garatti (2008, Thm 2.4)".

**5. Ruszczyński (2010).**
- **The abstract, from the Rutgers RUTCOR page,** introduces "the concept of a Markov risk measure". It derives "risk-averse dynamic programming equations and a value iteration method" for a finite-horizon and a discounted infinite-horizon model, and adds a policy-iteration method and a Newton method. It does not mention time consistency.
- **Jiang & Powell (arXiv:1509.01920, version of 10 May 2017)** state the following:
  - Ruszczyński and Shapiro (2006a) and Ruszczyński (2010) prove "that any time-consistent dynamic risk measure can be written as compositions of one-step conditional risk measures".
  - Under normalization and translation conditions, "it is proven in Ruszczyński [2010]" that a time-consistent dynamic risk measure has the nested form ρ_{t,T}(C_t,…,C_T) = C_t + ρ_t(C_{t+1} + ρ_{t+1}(C_{t+2} + ⋯ + ρ_{T−1}(C_T)⋯)).
  - One can also "take the reverse approach and define a time-consistent dynamic risk measure by simply specifying a set of one-step conditional risk measures".
  - Their reference list gives the same metadata as the dossier: *Mathematical Programming* 125(2):235–261, 2010.
- **So the claim is accurate:** nested risk measures and risk-averse DP (Ruszczyński 2010) are time-consistent. [unverified against Ruszczyński's own text: the Springer full text is behind a login.]

**6. Avanzi (2009).**
- **The IDEAS abstract** says that de Finetti in 1957 "criticized this approach" (assessing stability by the probability of ruin) "and laid the foundations of what would become an increasingly popular topic: the study of dividend strategies". The paper aims "at a taxonomical synthesis of the 50 years of actuarial research that followed de Finetti's original paper".
- **The survey covers barrier and band strategies.** Angoshtari, Bayraktar & Young (arXiv:1806.07499, version of 25 Mar 2019) write: "to maximize the expected discounted dividends until bankruptcy, it is optimal to pay dividends according to a band strategy or its special case of a barrier strategy; see Avanzi (2009) for a survey". This supports the dossier's barrier/band rules.
- **Optional wording points:**
  - De Finetti's criterion pays the owner until ruin but does not bound ruin. "Pay the owner while controlling ruin" needs a ruin constraint or penalty added on top, such as the Gerber–Shiu penalty in the next bullet (l. 176).
  - "Pay the minimum" is the dossier's adaptation; the classic barrier strategy has no minimum payout.
  - The dossier does not credit ratcheting to Avanzi, and his abstract does not mention it. If "ratcheting variants" needs a source, there are two options:
    - Dybvig (1995), already in §10;
    - Angoshtari, Bayraktar & Young (arXiv:1806.07499). Their paper extends "Duesenberry's optimal-consumption problem under a ratcheting constraint, studied by Dybvig (1995)" to dividends, where "the time of ruin could be finite".
