# Stream 14 literature check: investment-committee deliberation and human–AI co-deliberation

**Dossier checked:** `research/dossiers/14_ic_deliberation.md` (1,049 lines, dated 2026-10-18).
- §10 lists 88 references. 79 are academic or practitioner-academic works: journal and conference papers, arXiv preprints, working papers, books, and HBR / MIT SMR articles.
- The other 9 are outside this check: regulatory texts (SR 11-7, ICD 203, EU AI Act, Santiago Principles), institutional web pages (NBIM, NZ Super), the BoE/FCA survey, a vendor case study and a PyPI listing.

**Date:** 2026-10-18.

**Search engine:** Consensus. 5 searches, run one at a time, using only the query parameter (no filters).
- **Quota constraint.** The first search reported 7 searches left this month. After the fifth the counter was **0**. Two other agents share it and used 3 of the 8 searches consumed during this run.
- The task asked for about 25 citation look-ups plus 8–14 topical searches; only 5 searches were possible. Each query was therefore one of the topical seeds (seeds 1–5), worded to confirm dossier citations at the same time.
- Seed 6 ("noise in judgment decision hygiene") could not be run.
- **11 WebSearches** were used, only after the quota ran out, to confirm metadata of load-bearing works that Consensus could no longer be asked about (§7).

**Companion:** `research/verification/14_ic_deliberation.verify.md`.
- It checked 41 claims against primary sources and found no fabricated reference.
- It could not verify Schwenk (1990) and did not re-check the classical *(nr)* items.
- This check gave priority to exactly those gaps.

**Organizational mapping (user, 2026-10-18).**
- Secondaries is a hybrid of direct and fund investments.
- Corporate Finance owns the treasury function. Per the context file it also owns portfolio-level borrowing, overlay collateral and distribution payments.
- In the implications below:
  - the **Treasurer / Corporate Finance seat** owns the liquidity gate and the contingency funding plan;
  - quotes from Secondaries and Capital Solutions are treated as **conflicted market intelligence**.

**Reading conventions**
- Findings come from Consensus titles and abstracts, or from WebSearch summaries of publisher and repository pages. No full texts were read.
- **[Inference]** marks design reasoning that goes beyond what an abstract states.
- Author lists are shown as Consensus displays them, with "et al." where Consensus truncates.
- Years are Consensus record years. Where the venue year differs, this is noted.
- Citation counts are as Consensus reported them on 2026-10-18.
- Many 2025–26 items are recent preprints or have few citations. Treat them as design hypotheses to test, not as settled evidence.
- The evidence comes from laboratories, benchmarks, mutual funds and public deliberation, not from sovereign ICs. As the dossier itself says (§4), transfer mechanisms, not effect sizes.

---

## 1. Summary

### Citation integrity

**Scope: 26 works.** These are the 25 most load-bearing of the 79 academic references, plus one extra.
- **16 checked:** 6 in Consensus, then 10 by WebSearch after the quota ran out.
- **10 not checked in this session** (quota).
  - The companion file checked all 10 against primary sources.
  - It flagged 3 of them: Fogliato, Hackenburg and Salvi. Its verdicts are carried over in §2 for completeness.

**Result: 16 of 16 found, 0 metadata mismatches, 0 not found.** No reference is fabricated or garbled.
- Six items the dossier marks *(nr)* can be upgraded to verified: Schwenk (1990); Stasser & Titus (1985); Lu, Yuan & McLeod (2012); Parasuraman & Manzey (2010); Baron et al. (2014); List & Pettit (2002).
- For Lu et al. the upgrade covers metadata only. The effect sizes are still unverified.

**Venue updates (not mismatches)**
- **Smit et al.:** ICML 2024, PMLR 235:45883–45905. In the proceedings the author order is Smit, Grinsztajn, Duckworth, Barrett, Pretorius.
- **Blinder & Morgan:** a peer-reviewed version appeared in the *Journal of Money, Credit and Banking* 37(5):789–811 (2005), retitled "Are Two Heads Better than One? Monetary Policy by Committee".
- **Wang, Morgenstern & Dickerson:** the *Nature Machine Intelligence* venue could not be confirmed. Only arXiv v3 (February 2025) was found.

**Content flags: the citation is correct, but how the dossier uses it needs fixing**
1. **Schwenk (1990) is overstated, and the correction changes a design default.**
   - The dossier says devil's advocacy (DA) and dialectical inquiry (DI) "both beat an expert-recommendation baseline".
   - The abstract says DA beat the expert approach in general, but "the superiority of the DI to the E was not demonstrated in experiments using relatively ill-structured tasks". Neither technique beat the other.
   - IC decisions are ill-structured. The dossier's own source therefore does not support "DI on cruxes".
2. **Smit et al.** The dossier cites only the negative result. The abstract also reports that adjusting agent agreement levels "can significantly enhance performance and even surpass all other non-debate protocols we evaluated".
3. **Parasuraman & Manzey (2010).** Automation bias occurs in experts too. The WebSearch summary says it "cannot be prevented by training or instructions". Seeded-error drills therefore monitor automation bias; they do not prevent it.
4. **Stasser & Titus (1985).** The paper is confirmed. The collective information-sampling formula that the dossier attributes to it is still unconfirmed.

### Backfill

**Volume.** 5 topical searches and 99 records screened (query log in §7).
- §3 annotates 25 papers. 22 of them are not cited in the dossier.
- About 40 more results are listed briefly in §3.6.

**The most important missed papers**
1. **Alsobay et al. (2025) [B1]: surfacing is not decision quality.**
   - Design: a pre-registered experiment with 1,475 participants in 281 live groups on a hidden-profile task.
   - A GPT-4o facilitator increased information sharing.
   - But neither AI nor human facilitation changed the final decision.
2. **Chiang et al. (2024, IUI) [B2]: aim the challenge at the AI.**
   - An LLM devil's advocate that argues against the *AI's* recommendation promoted appropriate reliance in AI-assisted group decisions.
   - The Red Team seat should therefore target the model and shadow-IC conclusion, not only the human majority.
3. **Nemeth et al. (2001) [B7] and Schulz-Hardt et al. (2002, 201 managers) [B8].** Authentic dissent beats role-played devil's advocacy, which can end up bolstering the initial view.
4. **Garlappi et al. (2017, *JFE*) [B22].**
   - Group investment decisions made with heterogeneous beliefs are typically dynamically inconsistent and lead to underinvestment.
   - This bears directly on aggregating member beliefs inside a multi-period optimizer, and on DEFER.
5. **Ferreira et al. (2026) [B13] vs Zhang et al. (2025) [B12]: conflicting evidence on model heterogeneity.** Keep the "≥ 3 model families" rule for error independence and auditability, but test it rather than assume it raises accuracy.
6. **Kraidia et al. (2026, *Sci. Rep.*) [B14].**
   - A single persuasive adversarial agent cut accuracy by 10–40% and raised consensus on wrong answers by more than 30%. Adding agents or rounds did not fix it.
   - This is the threat model for conflicted inputs from Secondaries and Capital Solutions.
7. **Investment-team evidence, which the dossier lacks:**
   - teams make less extreme decisions (Bär et al. 2011) [B23];
   - with accurate data, team-managed funds outperform (Patel & Sarkissian) [B24];
   - ideological diversity helps, through both decisions and monitoring (Evans et al. 2024) [B25];
   - members of larger committees invest less effort (McCannon et al. 2020, §3.6).
8. **Automation-bias work since 2022:**
   - with wrong AI suggestions, very experienced radiologists' accuracy fell from 82.3% to 45.5% (Dratsch 2023) [B19];
   - wrong AI advice does most harm when it arrives before the person's own judgment (Agudo 2024) [B17];
   - non-concurrent advice trades over-reliance for under-reliance (Kokje 2026) [B18];
   - override rate and override accuracy serve as trust KPIs (Atanassova 2026) [B21].

### Challenges to the dossier (details in §5)

Twelve recommendations face contrary or qualifying evidence. The most consequential:
- DI on cruxes (Schwenk's own abstract);
- assigned dissent (Nemeth; Schulz-Hardt);
- the hidden-profile surfacing KPI (Alsobay);
- model-family diversity as a lever for accuracy (Ferreira);
- belief aggregation without commitment in a multi-period setting (Garlappi);
- evidence gating against selectively retrieved but legitimate documents (Kraidia).

### Not done (quota)

- Seed 6 (noise and decision hygiene) was not run.
- Nor were the planned refinements: social influence and the wisdom of crowds; sycophancy and persuasion; debate-based oversight; LLM forecasting; committee transparency.
- §7 lists these, and the 10 unchecked citations, for the 1 November quota reset.

---

## 2. Citation-integrity table

**Status key**
- **Found (C):** confirmed in Consensus.
- **Found (W):** confirmed by WebSearch after the Consensus quota was exhausted.
- **Not checked:** the quota ran out. The companion file's primary-source verdict is shown for reference; it was not re-checked here.

| # | Dossier citation | Status | Corrected metadata / notes | Consensus URL |
|---|---|---|---|---|
| 1 | Tessler, Bakker, Jarrett et al. (2024). AI can help humans find common ground in democratic deliberation. *Science* 386(6719):eadq2852 | Found (C) | Matches: *Science*, 2024, DOI 10.1126/science.adq2852, 306 citations. The abstract confirms N = 5,734 and that participants preferred AI statements. It also says successful statements "incorporated dissenting voices while respecting the majority position" (see §2.1). | [link](https://consensus.app/papers/details/e067e2c53d0357b9b08dd90c4a298b17/?utm_source=claude_desktop) |
| 2 | Choi, Zhu & Li (2025). Debate or vote: which yields better decisions in multi-agent LLMs? NeurIPS 2025 | Found (C) | Matches. Consensus record: arXiv, 2025, DOI 10.48550/arxiv.2508.17536, 95 citations. The abstract confirms that majority voting accounts for most of MAD's gains, the martingale result, and "biasing the belief update toward correction". | [link](https://consensus.app/papers/details/17ad64aabfbf5fae8c9857a62cfcecc5/?utm_source=claude_desktop) |
| 3 | Du, Li, Torralba, Tenenbaum & Mordatch (2024). Improving factuality and reasoning in language models through multiagent debate. ICML 2024 | Found (C) | Matches. The Consensus record is the 2023 arXiv version: DOI 10.48550/arxiv.2305.14325, 2,428 citations. | [link](https://consensus.app/papers/details/9f340342ab41509887e5a52bc07e6dd0/?utm_source=claude_desktop) |
| 4 | Liang et al. (2024). Encouraging divergent thinking in LLMs through multi-agent debate. EMNLP 2024 | Found (C) | Matches. The Consensus record is the 2023 arXiv version: DOI 10.48550/arxiv.2305.19118, 1,455 citations. The abstract confirms degeneration-of-thought, the "adaptive break", the "modest level of 'tit for tat'" and that an LLM judge may be unfair. | [link](https://consensus.app/papers/details/208317d4064351d0a3b0e032ccbd38de/?utm_source=claude_desktop) |
| 5 | Smit, Duckworth, Grinsztajn, Barrett & Pretorius (2023/2024). Should we be going MAD? (arXiv) | Found (C); venue update (W) | Consensus record: arXiv, 2023, DOI 10.48550/arxiv.2311.17371, 155 citations. **Venue:** ICML 2024, PMLR 235:45883–45905, with proceedings author order Smit, Grinsztajn, Duckworth, Barrett, Pretorius. **Content:** the dossier omits that tuned agreement levels let MAD surpass every non-debate protocol tested. | [link](https://consensus.app/papers/details/f6d1268fa91c578198b21a1b10cdf078/?utm_source=claude_desktop) |
| 6 | Schwenk (1990). Effects of devil's advocacy and dialectical inquiry on decision making: a meta-analysis. *OBHDP* 47(1):161–176 *(nr)* | Found (C); **content flag** | Matches: *OBHDP*, 1990, DOI 10.1016/0749-5978(90)90051-a, 190 citations. Upgrade from *(nr)*. **The dossier's claim that "both beat an expert baseline" is not supported for DI on ill-structured tasks** (§2.1). | [link](https://consensus.app/papers/details/a5794152500f5f829a00e765ca1b6f1f/?utm_source=claude_desktop) |
| 7 | Stasser & Titus (1985). Pooling of unshared information in group decision making: biased information sampling during discussion. *JPSP* 48(6):1467–1478 *(nr in §2.2)* | Found (W) | Matches, DOI 10.1037/0022-3514.48.6.1467. Upgrade from *(nr)*. The attribution of the formula p_mention(h) = 1 − (1 − p)^h (dossier §2.2) is unconfirmed (§2.1). | — (WebSearch: [Stasser & Titus PDF](https://www.uni-muenster.de/imperia/md/content/psyifp/aeechterhoff/vorlesungkommunikation/stasser_titus_unsharedinfogroupdisc_jpsp1985.pdf)) |
| 8 | Lu, Yuan & McLeod (2012). Twenty-five years of hidden profiles in group decision making: a meta-analysis. *PSPR* 16(1):54–75 *(nr)* | Found (W) | Matches, DOI 10.1177/1088868311417243 (online 6 Sep 2011). It pools 65 studies, with 101 independent effects and 3,189 groups. The magnitudes are still unverified (paywall). | — (WebSearch: [SAGE](https://journals.sagepub.com/doi/10.1177/1088868311417243)) |
| 9 | Parasuraman & Manzey (2010). Complacency and bias in human use of automation: an attentional integration. *Human Factors* 52(3):381–410 *(nr)* | Found (W) | Matches, DOI 10.1177/0018720810376055. Upgrade from *(nr)*. **Content:** automation bias affects naive and expert users and is not prevented by training or instructions (§2.1). | — (WebSearch: [SAGE](https://journals.sagepub.com/doi/10.1177/0018720810376055); [TU Berlin repository](https://depositonce.tu-berlin.de/items/0c787d91-6021-480b-a333-009e0d1d0092/full)) |
| 10 | Baron, Mellers, Tetlock, Stone & Ungar (2014). Two reasons to make aggregated probability forecasts more extreme. *Decision Analysis* 11(2):133–145 *(nr)* | Found (W) | Matches, DOI 10.1287/deca.2014.0293. Upgrade from *(nr)*. The two reasons support the dossier's rule on α (§2.1). | — (WebSearch: [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/deca.2014.0293); [RePEc](https://ideas.repec.org/a/inm/ordeca/v11y2014i2p133-145.html)) |
| 11 | List & Pettit (2002). Aggregating sets of judgments: an impossibility result. *Economics and Philosophy* 18(1):89–110 *(nr in §2.4)* | Found (W) | Matches. | — (WebSearch: [RePEc](https://ideas.repec.org/a/cup/ecnphi/v18y2002i01p89-110_00.html); [PhilArchive](https://philarchive.org/rec/LISASO-3)) |
| 12 | Meucci (2008). Fully flexible views: theory and practice. *Risk* 21(10):97–102 | Found (W) | Matches. An arXiv copy is 1012.2848. Follow-on work extends entropy pooling to CVaR views (Meucci, Ardia & Keel). | — (WebSearch: [RePEc/arXiv](https://ideas.repec.org/p/arx/papers/1012.2848.html)) |
| 13 | Schemmer, Kühl, Benz, Bartos & Satzger (2023). Appropriate reliance on AI advice. IUI 2023 | Found (W) | Matches: IUI '23, pp. 410–422, DOI 10.1145/3581641.3584066. It proposes a two-dimensional "Appropriateness of Reliance" (AoR) measure, tested with 200 participants. | — (WebSearch: [arXiv](https://arxiv.org/abs/2302.02187v3); [KIT](https://publikationen.bibliothek.kit.edu/1000158077)) |
| 14 | Blinder & Morgan (2000). Are two heads better than one? An experimental analysis of group vs. individual decisionmaking. NBER WP 7909 | Found (W); venue update | The WP citation is correct (companion file A3). **Peer-reviewed version:** "Are Two Heads Better than One? Monetary Policy by Committee", *JMCB* 37(5):789–811, October 2005. That abstract: groups are not slower and tend to outperform individuals under both unanimity and majority rule. | — (WebSearch: [RePEc](https://ideas.repec.org/a/mcb/jmoncb/v37y2005i5p789-811.html)) |
| 15 | Wang, Morgenstern & Dickerson (2025). LLMs that replace human participants can harmfully misportray and flatten identity groups. *Nature Machine Intelligence* | Found (arXiv, W); **venue unconfirmed** | arXiv 2402.01908 confirmed (v3, Feb 2025); authors and title match. Human studies used 3,200 participants across 16 identities and four LLMs. The NMI publication was not confirmed; until a DOI is found, cite arXiv v3. | — (WebSearch: [arXiv](https://arxiv.org/abs/2402.01908v1); [arXiv v3](https://arxiv.org/html/2402.01908v3)) |
| 16 | Schoenegger, Tuminauskaite, Park & Tetlock (2024). Wisdom of the silicon crowd (arXiv) *(extra check)* | Found (W) | arXiv 2402.19379 v6 (Jul 2024): 12 LLMs, **31 binary questions**, 925 human forecasters. The author list changed between versions (v5 included R. V. S. Bastos). No journal version was confirmed. | — (WebSearch: [arXiv](https://arxiv.org/abs/2402.19379v6)) |
| 17 | Vaccaro, Almaatouq & Malone (2024). When combinations of humans and AI are useful. *NHB* 8:2293–2303 | Not checked (quota) | Companion F9: confirmed, all values exact. Issue 12. It also reports g = −0.54 when the AI alone outperforms humans. | — |
| 18 | Khan et al. (2024). Debating with more persuasive LLMs leads to more truthful answers. ICML 2024 | Not checked (quota) | Companion F8: confirmed, PMLR 235:23662–23733. | — |
| 19 | Michael et al. (2023). Debate helps supervise unreliable experts (arXiv) | Not checked (quota) | Companion F7: confirmed. By design, the consultant argues for the wrong answer half the time. | — |
| 20 | Laban, Murakhovs'ka, Xiong & Wu (2023). Are you sure? The FlipFlop experiment (arXiv) | Not checked (quota) | Companion F5: confirmed (46% flip rate, −17% accuracy). | — |
| 21 | Wynn, Satija & Hadfield (2025). Talk isn't always cheap (arXiv) | Not checked (quota) | Companion F4: confirmed. ICML 2025 MAS workshop. | — |
| 22 | Chen, Saha & Bansal (2024). ReConcile. ACL 2024 | Not checked (quota) | Companion F15: confirmed. | — |
| 23 | Fogliato et al. (2022). Who goes first? FAccT 2022 | Not checked (quota) | **Companion F11 (carried over):** the participants were 19 *veterinary* radiologists. The abstract reports no accuracy gain. | — |
| 24 | Hackenburg et al. (2025). The levers of political persuasion with conversational AI (arXiv) | Not checked (quota) | **Companion F13 (carried over):** the peer-reviewed version is in *Science* 390(6777), DOI 10.1126/science.aea3884, with the title ending "...conversational artificial intelligence". | — |
| 25 | Salvi, Horta Ribeiro, Gallotti & West (2024; *NHB* 2025). On the conversational persuasiveness of LLMs | Not checked (quota) | **Companion A6 (carried over):** the journal title is "On the conversational persuasiveness of GPT-4", DOI 10.1038/s41562-025-02194-6. It reports N = 900 and +81.2% relative odds. | — |
| 26 | Hansen, McMahon & Prat (2018). Transparency and deliberation within the FOMC. *QJE* 133(2):801–870 | Not checked (quota) | Companion F16: confirmed. | — |

**Counts for the 16 checked:** 16 found, 0 mismatched, 0 not found. The two venue updates (Smit; Blinder & Morgan) and one unconfirmed venue (Wang et al.) are listed above.

### 2.1 Content and attribution flags

1. **Schwenk (1990): overstated in dossier §2.3 and §3.**
   - **What the dossier says:** "Schwenk 1990 meta-analysis: both beat an expert-recommendation baseline". The dossier therefore uses both a standing DA seat and "DI on the top cruxes".
   - **What the abstract says:** "the DA is more effective than the E approach in general. However, the superiority of the DI to the E was not demonstrated in experiments using relatively ill-structured tasks. Neither the DA nor the DI was shown to be a more effective method of introducing conflict into decision making."
   - **Corrected wording:** "DA beat an expert-recommendation baseline. DI's advantage over the expert approach was not demonstrated on relatively ill-structured tasks, and neither DA nor DI beat the other."
   - Two later experiments in the same Consensus result set also found DA ahead of both DI and the expert approach: Schwenk et al. (1994, *OBHDP*) and Valacich et al. (1995, *OBHDP*). See §3.6.
   - A third paper, Valacich et al. (1995, *Decision Sciences*; B9), compared objective with "carping" DA rather than DA with DI.

2. **Smit et al. (2024): incomplete.** The abstract also says that MAD protocols "might not be inherently worse than other approaches, but... more sensitive to different hyperparameter settings". It adds that adjusting agent agreement levels "can significantly enhance performance and even surpass all other non-debate protocols we evaluated". Add this to dossier §2.5, next to "do not reliably outperform".

3. **Tessler et al. (2024): a nuance, not an error.**
   - The dossier (§1, §8) stresses drift toward majority positions.
   - The Consensus abstract adds that successful statements "incorporated dissenting voices while respecting the majority position".
   - The companion file reports that revised statements *overweighted* the minority. It also corrects the scope of N for the 56% vs 44% preference.

4. **Parasuraman & Manzey (2010): weakens a safeguard's stated purpose.**
   - Per the WebSearch summary of the paper, complacency appears in naive and expert participants and "cannot be overcome with simple practice", and automation bias "cannot be prevented by training or instructions".
   - The dossier lists seeded-error drills among the automation-bias *countermeasures* (§6.10 item 6). It labels them "automation-bias monitoring" only in §6.8.
   - [Inference] Present them as monitoring and measurement. Rely on workflow design (H0 ordering, provenance, verification cost) for prevention.

5. **Stasser & Titus (1985): attribution.**
   - The paper proposes the biased information-sampling account.
   - The formal collective information-sampling formula that the dossier gives in §2.2 is usually credited to later model papers. Stasser & Titus (1987), *JPSP* 53:81–93, was confirmed to exist, but the formula's source was not.
   - A secondary source in the WebSearch results says that Lu et al. (2012) and Reimer, Reimer & Czienskowski (2010) support the claim that high information load worsens discussion bias toward shared information. This is a secondary claim and was not verified.

6. **Baron et al. (2014): supports the dossier's α rule.**
   - Per the WebSearch summary, there are two reasons to extremize.
     1. The probability scale is compressed near 0 and 1, so random error pulls averages toward 0.5. This reason does not affect the median or (arguably) the mean of log odds.
     2. Each forecaster accounts only for their own incomplete information, missing what the crowd pools. This reason affects all three aggregates.
   - The dossier pools weighted logits, so only reason 2 applies.
   - [Inference] Reason 2 is weak for LLM agents that share pre-training data and the same fact pack. This supports α ≤ 1 for agent ensembles, and α > 1 only for humans whose private information (for example, group heads' deal knowledge) has been shown by a track record.

7. **Lu, Yuan & McLeod (2012):** the metadata is confirmed. The dossier's "magnitudes nr" caveat still stands.

8. **Wang et al.:** the NMI venue is unconfirmed (row 15).

---

## 3. Annotated bibliography (25 papers)

Entries B1–B25. "Dossier-cited" marks the 3 entries the dossier already cites; the other 22 are missed papers. The finding comes from the Consensus abstract.

### 3.1 AI inside human group deliberation

**B1. [Bringing Everyone to the Table: An Experimental Study of LLM-Facilitated Group Decision Making](https://consensus.app/papers/details/00dfd56f864f59fc943420a4d8f3b5d6/?utm_source=claude_desktop)**
Mohammed Alsobay et al., 2025, *Proceedings of the ACM on Human-Computer Interaction*, 5 citations, DOI 10.1145/3816907.
- *Finding:*
  - Design: a pre-registered randomized experiment with 1,475 participants in 281 live groups on a hidden-profile task, under four conditions: no facilitation, a one-time prompt, a human facilitator, or a GPT-4o facilitator.
  - LLM facilitation increased the information shared by raising members' minimum engagement, at little attitudinal cost.
  - Neither human nor AI facilitation had a significant effect on the final decision.
  - The authors release the GRAIL platform.
- *Relevance to ADIC:*
  - This is the closest test of the IDM's core aim of surfacing uniquely held facts, such as a financing specialist's knowledge of NAV-loan covenants.
  - It shows that more sharing does not by itself produce better decisions.
  - [Inference] Replace the "hidden-profile surfacing ≥ 80%" target with decision accuracy on hidden-profile suites. Add an explicit integration step (§4).

**B2. [Enhancing AI-Assisted Group Decision Making through LLM-Powered Devil's Advocate](https://consensus.app/papers/details/5102feb21e155efa857abd4c30195548/?utm_source=claude_desktop)**
Chun-Wei Chiang et al., 2024, *Proceedings of the 29th International Conference on Intelligent User Interfaces*, 117 citations, DOI 10.1145/3640543.3645199.
- *Finding:*
  - Four LLM devil's-advocate styles were compared: interactive vs non-interactive, each targeting either the AI recommendation or the group majority.
  - In a randomized experiment, devil's advocates that argued against the AI's recommendation showed potential to promote groups' appropriate reliance on AI.
  - Perceived workload did not rise substantially. Interactive devil's advocates were seen as more collaborative and of higher quality.
- *Relevance to ADIC:*
  - This is direct evidence for an AI red-team seat in a human committee.
  - [Inference] By default, point the Red Team at the optimizer and shadow-IC recommendation, and make it interactive during H2/H3, rather than producing only a written memo.

**B3. [Conversational Agents as Catalysts for Critical Thinking: Challenging Social Influence in Group Decision-making](https://consensus.app/papers/details/08d0916b0f225086a7c0024cd8049026/?utm_source=claude_desktop)**
Soohwan Lee et al., 2025, *Extended Abstracts of the CHI Conference on Human Factors in Computing Systems*, 25 citations, DOI 10.48550/arxiv.2503.14263.
- *Finding:*
  - Design: 48 participants in 12 four-person groups, each with three senior members and one junior.
  - An LLM devil's advocate's counterarguments created a more flexible atmosphere and raised process and outcome satisfaction, most of all for the junior (minority) member.
  - Workload rose slightly but not significantly.
- *Relevance to ADIC:*
  - This bears on the dossier's open question 3: can anonymous reveal work alongside seniority?
  - [Inference] An AI challenger can voice counterarguments that junior staff hesitate to raise. Pair it with anonymized reveal.

**B4. [Towards Human-AI Deliberation: Design and Evaluation of LLM-Empowered Deliberative AI for AI-Assisted Decision-Making](https://consensus.app/papers/details/a6193280eaf65e8589f0b9a63e81b327/?utm_source=claude_desktop)**
Shuai Ma et al., 2024 (venue CHI 2025), *Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems*, 114 citations, DOI 10.1145/3706598.3713423.
- *Finding:* "Human-AI Deliberation" elicits opinions dimension by dimension, updates decisions iteratively and structures discussion between human and AI. It outperformed conventional explainable AI on appropriate reliance and task performance in a mixed-methods study.
- *Relevance to ADIC:*
  - This supports the dossier's MAP scorecards.
  - [Inference] Show each member where their MAP-dimension scores differ from the shadow-IC's, and let them query dimension by dimension, instead of offering only accept/reject on a recommendation.

**B5. [AI can help humans find common ground in democratic deliberation](https://consensus.app/papers/details/e067e2c53d0357b9b08dd90c4a298b17/?utm_source=claude_desktop)** *(dossier-cited; verified)*
Michael Henry Tessler et al., 2024, *Science*, 306 citations, DOI 10.1126/science.adq2852.
- *Finding:* Participants (N = 5,734) preferred AI-mediated group statements to those of human mediators and often converged after deliberation. Successful statements incorporated dissent while respecting the majority. The result replicated in a virtual citizens' assembly.
- *Relevance to ADIC:* Confirms the dossier's anchor study. The nuance in §2.1 item 3 applies. The mediation objective (endorsement) still differs from ADIC's (accuracy and coverage of dissent), as the dossier notes.

### 3.2 Structured dissent

**B6. [Effects of devil's advocacy and dialectical inquiry on decision making: A meta-analysis](https://consensus.app/papers/details/a5794152500f5f829a00e765ca1b6f1f/?utm_source=claude_desktop)** *(dossier-cited; content flag)*
Charles R. Schwenk, 1990, *Organizational Behavior and Human Decision Processes*, 190 citations, DOI 10.1016/0749-5978(90)90051-a.
- *Finding:* DA beat the expert approach in general. DI's superiority over the expert approach was not demonstrated on relatively ill-structured tasks. Neither technique beat the other.
- *Relevance to ADIC:* IC questions are ill-structured. [Inference] Make objective DA the default form of structured conflict. Use DI only where rival assumption sets are explicit and model-ready, for example a scenario set for cyclical versus structural DPI decline.

**B7. [Devil's advocate versus authentic dissent: stimulating quantity and quality](https://consensus.app/papers/details/246662213fa05d4991aa2ef601144715/?utm_source=claude_desktop)**
C. Nemeth et al., 2001, *European Journal of Social Psychology*, 230 citations, DOI 10.1002/ejsp.58.
- *Finding:*
  - An authentic minority produced more and better solutions than any of three forms of devil's advocate.
  - Prior work had found that a devil's advocate mainly prompts cognitive bolstering of the initial view.
  - The authors stress "the difficulty in cloning such authenticity by role-playing techniques".
- *Relevance to ADIC:*
  - This challenges the reliance on assigned dissent: the Red Team seat and the rotating human devil's advocate.
  - [Inference] Give genuine minority positions (from H0 pre-votes and independent S1 seats) priority over role-played dissent, and label Red Team output as "assigned".

**B8. [Productive conflict in group decision making: genuine and contrived dissent as strategies to counteract biased information seeking](https://consensus.app/papers/details/08050bebdff5542e977a6b280426e4ad/?utm_source=claude_desktop)**
S. Schulz-Hardt et al., 2002, *Organizational Behavior and Human Decision Processes*, 298 citations, DOI 10.1016/s0749-5978(02)00001-8.
- *Finding:* In a two-factor experiment with 201 employees and managers, genuine dissent (groups mixing a minority and a majority faction) prevented confirmatory information seeking better than devil's advocacy did. Confidence was an important mediator.
- *Relevance to ADIC:*
  - The participants are practitioners, so this evidence transfers better than student samples.
  - [Inference] When H0 pre-votes are homogeneous, confirmatory search is most likely. Trigger an outside challenge in that case, such as a co-opted expert (the NZ Super precedent) or the Treasurer seat's liquidity view. Log group confidence before and after discussion.

**B9. [Structuring Conflict in Individual, Face‐to‐Face, and Computer‐Mediated Group Decision Making: Carping Versus Objective Devil's Advocacy](https://consensus.app/papers/details/6a4fbbc91ec55155ae50d2f4f4f4c85b/?utm_source=claude_desktop)**
J. Valacich et al., 1995, *Decision Sciences*, 48 citations, DOI 10.1111/j.1540-5915.1995.tb01433.x.
- *Finding:* An objective, non-emotional devil's advocate produced higher-quality decisions than an emotional, "carping" one. Face-to-face groups facing carping devil's advocacy considered the fewest alternatives, reached the lowest quality and reached consensus fastest.
- *Relevance to ADIC:* [Inference] Red-team agents should critique assumptions in a plain, objective register. This fits the dossier's no-rhetoric rule. Add a tone check to the validator rubric.

**B10. [The utilization of individual capabilities in group approaches to strategic decision‐making](https://consensus.app/papers/details/48c5e4900f005068a4683cc481bdc4c7/?utm_source=claude_desktop)**
D. Schweiger et al., 1989, 167 citations, DOI 10.1002/smj.4250100104.
- *Venue:* Consensus labels it "Southern Medical Journal". [Inference] The DOI prefix 10.1002/smj indicates *Strategic Management Journal*, so the label looks like a record error.
- *Finding:*
  - DI and DA groups produced recommendations and assumptions of significantly higher quality than the average of their members; consensus groups did not.
  - DI groups' recommendations and assumptions, and DA groups' recommendations, exceeded those of the best individual.
- *Relevance to ADIC:* Structured conflict is the mechanism by which a committee can beat its best member. It supports the IC as the decision unit, provided conflict is structured rather than consensus-seeking.

### 3.3 Machine deliberation (multi-agent LLMs)

**B11. [Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?](https://consensus.app/papers/details/17ad64aabfbf5fae8c9857a62cfcecc5/?utm_source=claude_desktop)** *(dossier-cited; verified)*
Hyeong Kyu Choi et al., 2025, arXiv (NeurIPS 2025), 95 citations, DOI 10.48550/arxiv.2508.17536.
- *Finding:* Across seven NLP benchmarks, majority voting accounts for most of MAD's gains. Debate induces a martingale over agents' beliefs. Biasing updates toward correction helps.
- *Relevance to ADIC:* Confirms the ensemble-first rule for estimates. The companion file notes that the practical correction variants use the previous round's majority.

**B12. [If Multi-Agent Debate is the Answer, What is the Question?](https://consensus.app/papers/details/a0329768a070563eb64e91b08c2e60c9/?utm_source=claude_desktop)**
Hang-Fan Zhang et al., 2025, arXiv, 27 citations, DOI 10.48550/arxiv.2502.08788.
- *Finding:* Across 5 MAD methods, 9 benchmarks and 4 base models, MAD often failed to outperform chain-of-thought or self-consistency, even with more inference compute. Model heterogeneity acted as a "universal antidote" that consistently improved MAD.
- *Relevance to ADIC:* Supports ensemble-first and model-family diversity, but see B13. [Inference] Every IDM evaluation should include a compute-matched self-consistency baseline.

**B13. [Beyond Symmetric Agents: Cognitive Diversity and Multi-Agent Debate in Small Language Models](https://consensus.app/papers/details/6d29e590763b5fb5b9b16a9914be4fc3/?utm_source=claude_desktop)**
L. Ferreira et al., 2026, arXiv preprint, 0 citations, DOI 10.48550/arxiv.2609.35875.
- *Finding:*
  - Scope: 23 open-weight models from 11 vendor families, 5 tasks, more than 5,500 runs.
  - The hypothesis that cognitive diversity drives gains was rejected on every axis tested: personas, temperature and model identity.
  - At a matched budget, debate tied or lost to self-consistency, at 1.6× the wall-clock time and 3.4× the tokens.
  - Persona prompting reduced accuracy (a "persona tax").
  - Mixed-model teams lost to majority votes over their own rosters, and accuracy tracked member capability.
  - Nearly all of debate's benefit came from the first exchange of answers.
  - Transcripts silently overflowing the context window distorted the comparisons.
- *Relevance to ADIC:*
  - The results come from small models, so transfer to frontier models is uncertain.
  - The paper challenges the accuracy rationale for "≥ 3 model families" and supports the no-persona rule.
  - [Inference] Default to 1 debate round. Justify family diversity by error independence and auditability. Add context-overflow checks to the transcript validator.

**B14. [When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate](https://consensus.app/papers/details/8f581a2c3ee65cfd8cf2d96b6e1e0ce5/?utm_source=claude_desktop)**
Insaf Kraidia et al., 2026, *Scientific Reports*, 8 citations, DOI 10.1038/s41598-026-42705-7.
- *Finding:*
  - A single adversarial agent using coherent, confident, misleading arguments lowered system accuracy by 10–40% and raised consensus on incorrect answers by more than 30%.
  - Best-of-N and retrieval-augmented generation amplified the attack.
  - More agents, more rounds or prompt-based defenses did not reliably mitigate it.
- *Relevance to ADIC:*
  - This is the threat model for conflicted inputs: Secondaries pricing (the hybrid direct-plus-fund book), Capital Solutions NAV-loan and preferred-equity terms, and GP documents.
  - [Inference] Evidence gating must audit *which* evidence was retrieved, not only its provenance. Add a second-source rule for conflicted quotes (§4).

### 3.4 Automation bias and reliance

**B15. [Exploring automation bias in human–AI collaboration: a review and implications for explainable AI](https://consensus.app/papers/details/c15457f004325789909055df8acbdd9d/?utm_source=claude_desktop)**
Giuseppe Romeo et al., 2025, *AI & SOCIETY*, 202 citations, DOI 10.1007/s00146-025-02422-7.
- *Finding:*
  - A PRISMA review of 35 studies (2015 to April 2025).
  - Explanations may raise perceived acceptability but are often insufficient to improve accuracy or reduce automation bias. Overly technical or simplistic explanations can even reinforce misplaced trust.
  - User engagement and verification effort are the most effective points of intervention.
- *Relevance to ADIC:* [Inference] Make verification cheap. Every number should be one click from its run artifact, and the console should offer one-click "re-run with my view". This matters more than narrative explanations.

**B16. [Explanations Can Reduce Overreliance on AI Systems During Decision-Making](https://consensus.app/papers/details/5759c2c93f8e59a3a6f1313c1b768659/?utm_source=claude_desktop)**
Helena Vasconcelos et al., 2022 (Consensus record year), *Proceedings of the ACM on Human-Computer Interaction*, 433 citations, DOI 10.1145/3579605.
- *Finding:*
  - Five studies (N = 731) frame reliance as a cost-benefit choice. Task difficulty, explanation difficulty and incentives all shifted overreliance.
  - Explanations reduce overreliance when they lower the cost of verifying the AI. Null results in the literature may reflect explanations that did not lower that cost.
- *Relevance to ADIC:* This qualifies the dossier's scepticism about explanations, which rests on Bansal et al. 2021. [Inference] Favor explanations that are verification devices: binding constraints, flip thresholds, artifact links.

**B17. [The impact of AI errors in a human-in-the-loop process](https://consensus.app/papers/details/6b25796435175963b3bc7577650bf3f0/?utm_source=claude_desktop)**
Ujué Agudo et al., 2024, *Cognitive Research: Principles and Implications*, 70 citations, DOI 10.1186/s41235-023-00529-3.
- *Finding:* In two experiments (the second pre-registered), incorrect algorithmic support reduced the accuracy of human judgments. The effect was strongest when support came *before* participants gave their own judgment.
- *Relevance to ADIC:* Independent support for H0, the blind pre-vote before AI conclusions are shown, beyond Fogliato et al.

**B18. [AI-augmented decision-making in face matching: comparing concurrent and non-concurrent advice presentation](https://consensus.app/papers/details/189332eb9c72506d9c81d4fcc8c3de0e/?utm_source=claude_desktop)**
Eesha Kokje et al., 2026, *Cognitive Research: Principles and Implications*, 4 citations, DOI 10.1186/s41235-026-00707-z.
- *Finding:*
  - Three pre-registered experiments found no significant difference in overall performance between concurrent and non-concurrent advice (on-demand or conditional).
  - Advice shown after a contradicting unaided decision was followed less, and participants rejected incorrect advice more confidently.
  - The cost was under-reliance on correct advice.
- *Relevance to ADIC:* Human-first ordering shifts errors rather than removing them. The dossier already warns of this (§8). [Inference] Track under-reliance on correct model output as a KPI alongside over-reliance.

**B19. [Automation Bias in Mammography: The Impact of Artificial Intelligence BI-RADS Suggestions on Reader Performance.](https://consensus.app/papers/details/11958235302859f690f268ce3fbd76cb/?utm_source=claude_desktop)**
T. Dratsch et al., 2023, *Radiology*, 318 citations, DOI 10.1148/radiol.222176.
- *Finding:* 27 radiologists read 50 mammograms with a purported AI. Accuracy fell sharply when the AI was wrong, at every level of experience.
  - Inexperienced: 79.7% vs 19.8%.
  - Moderately experienced: 81.3% vs 24.8%.
  - Very experienced: 82.3% vs 45.5%.
- *Relevance to ADIC:* Seniority does not immunize against automation bias. [Inference] Seeded-error drills must include the most senior IC members and the chair.

**B20. [Bias in the Loop: How Humans Evaluate AI-Generated Suggestions](https://consensus.app/papers/details/30ea9cdb30c05a549f230f5b3b8cd97b/?utm_source=claude_desktop)**
Jacob Beck et al., 2025, arXiv, 10 citations, DOI 10.48550/arxiv.2509.08514.
- *Finding:* In a randomized experiment with 2,784 participants, requiring corrections for flagged AI errors *reduced* engagement and increased acceptance of incorrect suggestions. Attitudes toward AI predicted performance best: sceptics detected errors more reliably.
- *Relevance to ADIC:*
  - The task is annotation, not investment decisions.
  - [Inference] It warns that the dossier's forcing rule could backfire if it becomes a burden. The rule says that a member who accepts an AI recommendation must write one way it could be wrong. Keep it to one line, A/B-test it, and consider a rotating "AI sceptic" reviewer role.

**B21. [When Should Your Team Override AI? A Trust Calibration Routine](https://consensus.app/papers/details/89b4d132bc3a518fa9b3f708ff8d0df7/?utm_source=claude_desktop)**
Iva Atanassova et al., 2026, *Academy of Management Perspectives*, 2 citations, DOI 10.5465/amp.2025.0019.
- *Finding:*
  - The paper proposes a five-stage team routine: co-sensing, co-framing, co-deciding, action and feedback, and trust reconfiguration.
  - Its core indicators of calibrated trust are the override rate (the share of AI recommendations reversed) and override accuracy (how often reversals prove correct).
- *Relevance to ADIC:* The dossier already logs overrides with reason codes. [Inference] Compute override accuracy over time as a primary KPI, next to the skill score against the model baseline (BSS).

### 3.5 Investment committees and teams (finance evidence)

**B22. [Ambiguity and the Corporation: Group Disagreement and Underinvestment](https://consensus.app/papers/details/349a3e540a9f507c999fa811de9d8775/?utm_source=claude_desktop)**
Lorenzo Garlappi et al., 2017, *Journal of Financial Economics*, 64 citations, DOI 10.1016/j.jfineco.2017.06.005.
- *Finding:* The paper models dynamic investment decided by agents with heterogeneous beliefs under a "utilitarian" influence-weighted rule.
  - (i) Group decisions are typically dynamically inconsistent.
  - (ii) The inconsistency causes inefficient underinvestment.
  - (iii) Trading securities among insiders or with outsiders can restore efficiency, but in some cases leads to overinvestment.
- *Relevance to ADIC:*
  - The IDM's pooled-belief optimum uses influence weights $w_k$, and in the framework it sits inside a multi-period optimizer.
  - [Inference] Re-aggregating member beliefs at each meeting may produce time-inconsistent plans and a bias toward DEFER/HOLD: under-commitment and unused dry powder in dislocations. Design responses are in §4.

**B23. [Is a team different from the sum of its parts? Evidence from mutual fund managers](https://consensus.app/papers/details/be40b9004e4b554d9a2d383970d86703/?utm_source=claude_desktop)**
M. Bar et al., 2011, *Review of Finance*, 39 citations, DOI 10.1093/rof/rfq014.
- *Finding:*
  - Using US equity mutual funds, the paper rejects group-shift theory in favor of diversification of opinions: extreme views average out.
  - Teams follow less extreme styles, hold less industry-concentrated portfolios, and have lower active share and lower idiosyncratic risk.
  - Teams are less likely to produce extreme performance.
- *Relevance to ADIC:*
  - Committees moderate.
  - [Inference] Committee averaging, combined with a max-min robust rule, may systematically under-size high-conviction contrarian actions: secondary purchases in a DPI drought, structured capital in a crisis, opportunistic overlay trades.
  - Consider a delegated, conviction-scaled band, following the NZ Super confidence-scaled tilting the dossier cites.

**B24. [To Group or Not to Group? Evidence from Mutual Fund Databases](https://consensus.app/papers/details/95474c7c92aa5d76954ac1ae9771eb84/?utm_source=claude_desktop)**
Saurin Patel et al., 2015 (Consensus record year), *Journal of Financial and Quantitative Analysis*, 93 citations, DOI 10.1017/s0022109017000655.
- *Finding:*
  - Discrepancies in manager-structure data (CRSP/Morningstar vs SEC records) hid the effect of teams.
  - With accurate data, team-managed funds outperform single-managed funds, with no more risk, and the team-size relation is nonlinear.
  - The SSRN version ([record](https://consensus.app/papers/details/abacd70fef6a5d9898f17f1f81821218/?utm_source=claude_desktop), DOI 10.2139/ssrn.2047094) adds two points: the largest gains came with three managers, and in teams more homogeneous in age and education.
- *Relevance to ADIC:*
  - Finance-domain support for collective decisions, which the dossier draws mainly from FOMC lab analogies.
  - [Inference] Support a small decision core, such as a three-person Tier-B subcommittee. Mutual-fund teams are not ICs.

**B25. [Identity, Diversity, and Team Performance: Evidence from U.S. Mutual Funds](https://consensus.app/papers/details/f22bf3628480573889f8a14f6a899f33/?utm_source=claude_desktop)**
Richard B. Evans et al., 2024, *Management Science*, 7 citations, DOI 10.1287/mnsc.2022.00544.
- *Finding:*
  - Politically diverse fund-management teams outperform homogeneous ones, through better decisions and more monitoring.
  - The benefit disappears when polarization is high.
  - Entrenched managers prefer homogeneous teams.
- *Relevance to ADIC:*
  - [Inference] Build diversity of perspective into the IC and shadow-IC. Examples are the Treasurer seat's liquidity loss function and the Outside-View seat. Manage affective conflict at the same time.
  - The preference of entrenched leaders for homogeneous committees is a governance risk for the Board to watch.
  - This sits in tension with B24's SSRN finding favoring age and education homogeneity.

### 3.6 Other results consulted (one line each)

**Machine deliberation**
- [Diversity of Thought Elicits Stronger Reasoning Capabilities in Multi-Agent Debate Frameworks](https://consensus.app/papers/details/cb0dec2135195613aaa4b18e439fd347/?utm_source=claude_desktop) (Hegazy, 2024, arXiv, 20 cit.): after 4 rounds, diverse medium models reached 91% on GSM-8K vs 82% for three Gemini-Pro instances. Pro-heterogeneity; contrast with B13.
- [Improving Multi-Agent Debate with Sparse Communication Topology](https://consensus.app/papers/details/99a2e1e098065cac85eaf519069623c3/?utm_source=claude_desktop) (Yun-Xuan Li et al., 2024, arXiv, 145 cit.): sparse topologies match or beat fully connected debate at lower cost.
- [SELENE: Selective and Evidence-Weighted LLM Debating for Efficient and Reliable Reasoning](https://consensus.app/papers/details/5396f924eb435dc3b68cf76d659e4f21/?utm_source=claude_desktop) (Verma et al., 2026, EACL Industry, DOI 10.18653/v1/2026.eacl-industry.7): debate starts only on detected disagreement, with evidence-weighted aggregation. About 50% fewer tokens, with better accuracy and calibration. Supports debate-on-demand for cruxes.
- [RAG-Induced Failures in Multi-Agent Large Language Model Debate](https://consensus.app/papers/details/9ee418d1bd585ef1ab849f87d3ab77fd/?utm_source=claude_desktop) (Kraidia et al., 2026, ICETES): a malicious agent controlling retrieval of *legitimate* documents cut majority-vote accuracy by up to 38%.
- [Tool-MAD: A Multi-Agent Debate Framework for Fact Verification With Diverse Tool Augmentation and Adaptive Retrieval](https://consensus.app/papers/details/39978aaaaee55aff9cd8ea24f1c727d9/?utm_source=claude_desktop) (Jeong et al., 2026, *IEEE Access*): giving each agent a distinct external tool raised accuracy by up to 11.2 pp over MAD. Supports seats defined by evidence slices.
- ["Tipping the Balance": Human Intervention in Large Language Model Multi‐Agent Debate](https://consensus.app/papers/details/aa02d6acdf4a5f8eaf1b7b9afcc89400/?utm_source=claude_desktop) (Triem et al., 2024, *Proc. ASIS&T*): LLM agents weighed human input above AI opinion, but only slightly.

**AI in human deliberation**
- [Moderator Chatbot for Deliberative Discussion](https://consensus.app/papers/details/94a98141d6495b0bb0cfc4f8b913705c/?utm_source=claude_desktop) (Kim et al., 2021, PACM HCI, 78 cit.): structure diversified opinions; facilitation aligned consensus with independent individual opinions and evened out contribution.
- [Competent but Rigid: Identifying the Gap in Empowering AI to Participate Equally in Group Decision-Making](https://consensus.app/papers/details/544d74a6def657418d0c81d760faa698/?utm_source=claude_desktop) (Chengbo Zheng et al., 2023, CHI, 52 cit.): an AI given an equal vote on a committee still played a secondary role. Supports "no AI vote" on separate grounds.
- [Artificial Intelligence in Deliberation: The AI Penalty and the Emergence of a New Deliberative Divide](https://consensus.app/papers/details/287de1d48423566ab4da1ecacb1b5d65/?utm_source=claude_desktop) (Jungherr et al., 2025, *Government Information Quarterly*, 31 cit.): in a pre-registered experiment (n = 1,850), AI-facilitated deliberation drew less willingness to take part and lower quality ratings.
- [When Machines Join the Moral Circle: The Persona Effect of Generative AI Agents in Collaborative Reasoning](https://consensus.app/papers/details/781880fa3c3158dfa6aabf326acb95f9/?utm_source=claude_desktop) (Jin et al., 2025, arXiv): contrarian AI teammates broadened framing; final decisions tracked initial stances.
- [The Empty Chair: Using LLMs to Raise Missing Perspectives in Policy Deliberations](https://consensus.app/papers/details/b007347ca88b5975b1b1eef018e6bdd0/?utm_source=claude_desktop) (Fulay et al., 2025, arXiv): simulated absent stakeholders sparked discussion, but outputs were generic and raised overreliance concerns. A caution for any simulated "owner seat".
- [AI-Mediated Communication Reshapes Social Structure in Opinion-Diverse Groups](https://consensus.app/papers/details/f524a86ae3be5cdebe0905680013f2c0/?utm_source=claude_desktop) (Huq et al., 2025, arXiv, N = 557): stance-personalized assistance increased clustering. Supports the dossier's no-personalization rule.
- [Accountable Human-AI Deliberation with LLMs: Scaling Collective Intelligence through Symbiotic Scaffolding](https://consensus.app/papers/details/a7e595ea51d752eab15f2b247fc0647b/?utm_source=claude_desktop) (Zaghouani, 2026, arXiv, 0 cit.): a blueprint proposing coverage, diversity and erasure metrics, clause-level provenance, and human primacy for ratification. No empirical results.
- [Can AI mediation improve democratic deliberation?](https://consensus.app/papers/details/bc801b60b4185f2bbd77676d1ca6192a/?utm_source=claude_desktop) (Tessler et al., 2026, arXiv): the Habermas Machine authors' own discussion of remaining challenges.
- [EchoMind: Supporting Real-time Complex Problem Discussions through Human-AI Collaborative Facilitation](https://consensus.app/papers/details/6e8139cc06585ba0bd3719b357ed9ef0/?utm_source=claude_desktop) (W.-H. Chen et al., 2025, PACM HCI, N = 16): live LLM issue mapping helped teams stay on objectives.
- [Using collective dialogues and AI to find common ground between Israeli and Palestinian peacebuilders](https://consensus.app/papers/details/395430cc781e554da7da2da36e8a1675/?utm_source=claude_desktop) (Konya et al., 2025, FAccT): a field deployment of bridging-based ranking.

**Structured dissent**
- [Devil's Advocacy and Dialectical Inquiry Effects on Face-to-Face and Computer-Mediated Group Decision Making](https://consensus.app/papers/details/76a71d342625525499bd997d290f0129/?utm_source=claude_desktop) (Valacich et al., 1995, *OBHDP*, 126 cit.): DA groups considered more alternatives and chose better recommendations than DI or expert groups.
- [Effects of Devil′s Advocacy and Dialectical Inquiry on Individuals versus Groups](https://consensus.app/papers/details/ecb5880bd2685309b4cb89466b09b758/?utm_source=claude_desktop) (Schwenk et al., 1994, *OBHDP*, 106 cit.): DA produced higher-quality solutions than DI or expert approaches.
- [Group Approaches for Improving Strategic Decision Making: A Comparative Analysis of Dialectical Inquiry, Devil's Advocacy, and Consensus](https://consensus.app/papers/details/0b699d4e3819550b9a416fb7634d6883/?utm_source=claude_desktop) (Schweiger et al., 1986, *AMJ*, 753 cit.): seminal. The Consensus abstract is truncated.
- [Experiential Effects of Dialectical Inquiry, Devil's Advocacy and Consensus Approaches to Strategic Decision Making](https://consensus.app/papers/details/f092c6f6fdf85feab23f83452dd66ffb/?utm_source=claude_desktop) (Schweiger et al., 1989, *AMJ*, 520 cit.): a longitudinal study with middle managers. The abstract is truncated.
- [Uncovering hidden profiles: advocacy in team decision making](https://consensus.app/papers/details/fdf654e2521d519aa37b369d071fe9f6/?utm_source=claude_desktop) (Waddell et al., 2013, *Management Decision*): in hidden-profile teams, DA raised decision quality over free discussion but increased affective conflict.
- [Devil's advocacy and cyber space. In support of quality assurance and decision making](https://consensus.app/papers/details/d32fdc90a8dd59c09692ee869fff0c35/?utm_source=claude_desktop) (Claver, 2021, *Journal of Intelligence History*): the standing "devil's advocate shop" in Israeli military intelligence after 1973. An institutional precedent for a permanent red team.

**Automation bias and reliance**
- [Trust and reliance on AI - An experimental study on the extent and costs of overreliance on AI](https://consensus.app/papers/details/5ef5f61d268d52799dc5a8e348f8b5fa/?utm_source=claude_desktop) (Klingbeil et al., 2024, *Computers in Human Behavior*, 435 cit.): knowing that advice came from AI caused overreliance, even against contextual information and the participant's own judgment.
- [Why Highly Reliable Decision Support Systems Often Lead to Suboptimal Performance and What We Can Do About it](https://consensus.app/papers/details/033b843b53925418b75d44cfaf1fd1df/?utm_source=claude_desktop) (Rieger et al., 2025, *IEEE THMS*): human–automation pairs often do worse than the system alone because humans override correct recommendations. Relevant to measuring override value.
- [How Stated Accuracy of an AI System and Analogies to Explain Accuracy Affect Human Reliance on the System](https://consensus.app/papers/details/04e9769fa4b752f5bdd49f6b32f154e5/?utm_source=claude_desktop) (He et al., 2023, PACM HCI, loan task): explaining stated accuracy did not produce appropriate reliance. A track-record display alone is insufficient.
- [The effects of explanations on automation bias](https://consensus.app/papers/details/d7418b907b6f505abc4ee25af157242d/?utm_source=claude_desktop) (Vered et al., 2023, *Artificial Intelligence*): explanations did not reduce automation bias and sometimes increased it, but often raised accuracy.
- [Human Performance Consequences of Automated Decision Aids](https://consensus.app/papers/details/73b0ecb21a42591c83da2b92fcf87004/?utm_source=claude_desktop) (D. Manzey et al., 2012, *JCEDM*, 292 cit.): automation failures had stronger effects than positive experience. Identifies three mechanisms of commission errors. Relevant to the design of seeded-error drills.
- [Check the box! How to deal with automation bias in AI-based personnel selection](https://consensus.app/papers/details/62b3159c86cf5dd0991faa2dfbc30edf/?utm_source=claude_desktop) (Kupfer et al., 2023, *Frontiers in Psychology*): telling decision makers about system errors increased verification; telling them about their responsibility did not. Less aggregated data reduced automation bias.
- [Drivers and influence of social conformity on decision making in human-AI teams](https://consensus.app/papers/details/538b5a3ce7b45b6db16dc97d11cb992c/?utm_source=claude_desktop) (Zhong et al., 2026, *Scientific Reports*): AI advisors exert informational but not normative pull. Participants under-weighted advice relative to a Bayesian benchmark.
- [How transparency modulates trust in artificial intelligence](https://consensus.app/papers/details/f86e1db6845c5ed1b20575328d62baaf/?utm_source=claude_desktop) (Zerilli et al., 2022, *Patterns*, 234 cit.): a review placing "algorithmic vigilance" between aversion and complacency. Confidence and performance metrics may beat explanations.
- [Automation Bias in AI-Assisted Medical Decision-Making under Time Pressure in Computational Pathology](https://consensus.app/papers/details/bdbf4d7d6b58533ca7e2893123440bde/?utm_source=claude_desktop) (Rosbach et al., 2024) and [Stuck on Suggestions](https://consensus.app/papers/details/4523c8f11349555cb8756f3379743482/?utm_source=claude_desktop) (Rosbach et al., 2026): 28 experts showed a 7% automation-bias rate, plus anchoring that time pressure intensified.
- [Engaging with AI: How Interface Design Shapes Human-AI Collaboration in High-Stakes Decision-Making](https://consensus.app/papers/details/646fc3c6d60b56779cdbaead22345562/?utm_source=claude_desktop) (Z.-C. Chen et al., 2025, arXiv, N = 108): confidence levels, text explanations and performance visualizations helped; AI-generated questions cut performance.
  - *Caution:* [Henderson, 2026](https://consensus.app/papers/details/407575f7d3d95393ab58d699809ce265/?utm_source=claude_desktop) reports a near-identical design (108 participants, 18 per condition). Cite the Chen et al. record.

**Committees and teams**
- [Individual Competence and Committee Decision Making: Experimental Evidence](https://consensus.app/papers/details/db5975e381e555328e2940a0470eccab/?utm_source=claude_desktop) (McCannon et al., 2020, *Southern Economic Journal*): as committees grow, members invest less effort in competence (free riding).
- [Mutual fund performance, management teams, and boards](https://consensus.app/papers/details/92fdbc1ed1ff5a6bbc6f0f25addb58d0/?utm_source=claude_desktop) (Adams et al., 2016, *Journal of Banking & Finance*, 50 cit.): the benefits of team management appear only under strong board monitoring.
- [Do Teams Alleviate or Exacerbate Behavioral Biases? Evidence from Extrapolation Bias in Mutual Funds](https://consensus.app/papers/details/404eae43ae8c533d8eb692db2dfa5bf7/?utm_source=claude_desktop) (Barahona et al., 2021): teams strongly attenuate return extrapolation. Relevant to IC review of drift between underwritten, actual and forecast returns.
- [Two heads are less bubbly than one: team decision-making in an experimental asset market](https://consensus.app/papers/details/ae34a94e82675854aae9581db8d269fc/?utm_source=claude_desktop) (Cheung et al., 2011, *Experimental Economics*, 52 cit.): two-person teams substantially reduced bubbles.
- [Performance Characteristics of Individually-Managed versus Team-Managed Mutual Funds](https://consensus.app/papers/details/d3b7e04e87b8554598d6a3981d952610/?utm_source=claude_desktop) (Bliss et al., 2008, *JPM*): no significant difference in risk-adjusted performance; teams carry less risk and turn over less.
- [Are N+1 heads better than one?: The case of mutual fund managers](https://consensus.app/papers/details/89f7b57b9b065925b4c1ef5becf11941/?utm_source=claude_desktop) (Prather et al., 2002, *JEBO*, 115 cit.): results consistent with classical decision theory and market efficiency rather than team superiority.
- [Individual Decision Making and Group Decision Processes](https://consensus.app/papers/details/51b9c2bc7cc6509b8b26d0699febeecf/?utm_source=claude_desktop) (Payne et al., 2002, *Journal of Psychology and Financial Markets*): "a lot of literature on group decision-making, but little or none on investment committees". Includes a survey of IC members.
- [Grouped data, investment committees & multicriteria portfolio selection](https://consensus.app/papers/details/9731ecaadf8c58c58ce54811f9f83446/?utm_source=claude_desktop) (Xidonas et al., 2021, *Journal of Business Research*): decision support that combines IC members' discrete recommendations across multiple criteria.
- *Malformed Consensus records (do not cite):* ["JEL-Classification: Mutual Funds, Team Management, Investment Behaviour"](https://consensus.app/papers/details/ca300398f6a55a789aafbb975460316a/?utm_source=claude_desktop) appears to be a working-paper version of B23; ["patel, saurin and sarkissian, sergei"](https://consensus.app/papers/details/c6179801a99a5c1b832998a33a41cadf/?utm_source=claude_desktop) duplicates the SSRN version of B24.

---

## 4. Missed-but-important papers: concrete design implications

All items below are **[Inference]** unless they restate an abstract. They extend dossier §6.

### 4.1 State variables to add to $S_t$ (dossier §6.7)

| New state variable | Definition | Source | Use in the IDM |
|---|---|---|---|
| `dissent_authenticity[i]` | For agenda item *i*: the share of H0 human pre-votes and S1 seats whose implied action differs from the median, plus a tag saying whether each minority position is authentic or assigned (Red Team) | B7, B8 | If no authentic dissent exists, trigger an external challenge: a co-opted expert, or the Treasurer / Corporate Finance seat's liquidity view. Show authentic minority reports first. |
| `unique_fact_ledger` | Facts held by exactly one seat or member, flagged surfaced, discussed, changed a MAP score, or changed the implied action | B1 | Measures how far surfacing converts into use. This feeds the revised hidden-profile KPI. |
| `reliance_state[k]` | Per member: override rate, override accuracy, and over- and under-reliance rates, each split by whether the model or AI was right | B21, B18, B17 | Calibrated-trust KPI and member feedback. Replaces raw agreement. |
| `group_confidence[i]` | Members' confidence before and after discussion | B8 (confidence as mediator) | Flags confidence that rises without new validator-accepted evidence. |
| `plan_consistency[t]` | The gap between the committee's plan for *t+1*, made at *t*, and the plan re-optimized at *t+1* under unchanged beliefs | B22 | Detects dynamic inconsistency and drift toward underinvestment or DEFER. |
| `seat_influence[s]` | The shift in the pooled estimate attributable to each seat during S3 | B14 | Flags a single seat that moves consensus without new evidence. Conflicted seats get extra scrutiny. |

### 4.2 Models

- **Committee policy with commitment (B22).** In the multi-period optimizer, compute two plans:
  - (a) a *re-aggregation plan*, in which member beliefs are pooled again at each meeting;
  - (b) a *pre-committed state-contingent plan*, fixed at S0 through signposts.

  Report the value gap as the "cost of committee inconsistency". Use (b) for irreversible actions.
  - *Recalled background, not searched:* dynamically consistent max-min updating needs a "rectangular" set of priors (Epstein & Schneider, *JET* 2003). Check this with the robust-optimization stream before using max-min over member credal sets across periods.
- **Model of accuracy before and after discussion (B1).** Fit a hierarchical model of the Brier change after H2 discussion. Separate gains from information sharing (via `unique_fact_ledger`) from conformity (via changes in confidence and dispersion with no new evidence).
- **Reliance model (B17–B19, B21).** Model accept/reject by member against model-correct/model-wrong, with seniority, time pressure and item type as covariates. This estimates over- and under-reliance and tracks how they evolve after seeded-error drills.

### 4.3 Parameters

| Parameter | Dossier default (§6.8) | Suggested change | Source |
|---|---|---|---|
| Debate rounds per crux | 2 | **Default 1.** Allow a second round only if the crux stays open *and* new validated evidence has appeared. Report the deltas for round 1 and round 2. | B13 (benefit almost all from the first exchange). The dossier's own sources point both ways: Wynn (degradation) vs Du (more rounds helped). |
| Model-family rule | ≥ 3 families, ≤ 40% each | **Keep, but justify it by error independence and auditability.** Make it a parameter tested by ablation (best family × N vs mixed), always against a compute-matched self-consistency baseline. | B13 vs B12 and Hegazy (§3.6) |
| Red Team target | "Strongest case against" | **Two targets:** (a) the model and shadow-IC recommendation, the default and interactive at H2/H3; (b) the human majority after H1. | B2 |
| Mode of structured conflict | Standing DA seat + DI on the top cruxes | **Objective DA by default.** Use DI only for cruxes with explicit rival assumption sets that can be run as scenario sets. | B6; B9 (objective vs carping DA); §3.6 (Valacich et al. 1995, *OBHDP*; Schwenk et al. 1994) |
| Debate trigger | Top ≤ 3 cruxes by EVPI | Add a disagreement trigger (selective debate): EVPI rank *and* dispersion ≥ δ_p | SELENE (§3.6) |
| Size of the voting IC | 6–12 people (dossier §8) | A smaller voting core (about 5–7) plus per-meeting co-opted experts without votes. A three-person core for Tier B. | McCannon (§3.6); B24 (mutual funds, not ICs) |
| Conviction band | None | A Board-approved, delegated risk band in which high-conviction contrarian actions are sized by the desk or group, e.g. the opportunistic overlay or Secondaries dry powder in a DPI drought | B23; NZ Super confidence-scaled tilting (dossier §5) |
| Hidden-profile target | Surfacing ≥ 80% | **Hidden-profile decision accuracy:** the share of suites in which the committee picks the option the full information set supports. Set the target from shadow-mode baselines and also report the surfacing-to-use conversion rate. | B1 |

### 4.4 Constraints

1. **Second-source rule for conflicted quotes (B14).**
   - An evidence-gated update (S3) that rests on pricing from the Secondaries group or on NAV-loan and preferred-equity terms from the Capital Solutions group needs an independent second source, such as an external broker quote or a reference-class dataset.
   - The context file flags these groups' quotes as conflicted market intelligence (§1A, item 4).
2. **Retrieval audit (B14; RAG paper in §3.6).** The validator checks the *selection* and relevance of retrieved documents, not just their provenance. It rejects updates where contrary documents in the corpus were not retrieved.
3. **Influence cap.** No single seat's S3 arguments may move the pooled estimate by more than δ without validator-accepted new evidence. This generalizes the dossier's 5 pp rule from a seat's own estimate to its influence on others.
4. **Drills include seniors (B19).** Seeded-error drills cover the chair and CIO. Drills are monitoring, not prevention (Parasuraman & Manzey; §2.1 item 4).
5. **Red Team register (B9).** Critiques must be objective and assumption-focused; the validator rubric rejects "carping" output.

### 4.5 Objectives and KPIs (dossier §6.11)

- **Replace** "hidden-profile surfacing ≥ 80%" with decision accuracy on hidden-profile suites, and report surfacing-to-use conversion (B1).
- **Add override accuracy** alongside the override rate and BSS against the model baseline (B21).
- **Track under-reliance** on correct model output as well as over-reliance (B18; Rieger in §3.6).
- **A/B-test the cognitive-forcing burden** and measure engagement, not just compliance (B20).
- **Monitor underinvestment:** DEFER frequency, anti-portfolio performance, and `plan_consistency` (B22).
- **Survey perceived legitimacy** of AI-supported deliberation among IC members each year. Jungherr (§3.6) found an "AI penalty" in public deliberation.

### 4.6 Agent and IC design

- **Facilitator seat.**
  - Keep it: LLM facilitation raised minimum engagement at little cost (B1), and structured facilitation aligned consensus with independent opinions (Kim 2021, §3.6).
  - Add an explicit **integration step** between H2 and H4: "Which uniquely held facts change any MAP score or implied action?" Answers go to `unique_fact_ledger`.
- **Red Team seat.**
  - Make it interactive, aim it at the model and shadow-IC conclusion (B2), and keep its tone objective (B9).
  - Its output is labelled "assigned dissent" and shown after authentic minority reports (B7, B8).
- **Juniors and hierarchy.** Route anonymized concerns from junior staff through the facilitator or AI challenger (B3). This addresses dossier open question 3.
- **Deliberation by dimension.** Offer a per-dimension view of each member's MAP scores against the shadow-IC's, with Q&A at the level of each dimension (B4).
- **Treasurer / Corporate Finance seat as a source of authentic dissent.**
  - This seat owns the liquidity gate and contingency funding plan, and its loss function genuinely differs from the asset groups'. It is a natural source of authentic dissent on SELL, REFINANCE and LEVER proposals (B8).
  - [Speculative] B22 finds that trading among insiders can restore efficient group investment. Corporate Finance's internal liquidity transfer pricing may play an analogous role in reconciling heterogeneous beliefs across groups. Test this before relying on it.
- **Committee composition.** Seek diversity of perspective while limiting affective conflict (B25). Watch for the CIO's or chair's preference for a homogeneous committee.
- **Seats for conflicted groups.** Agents or members representing Secondaries and Capital Solutions may provide evidence but cannot be the sole source on cruxes whose outcome benefits their book (B14).

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier recommendation (§) | Challenging paper(s) | What the evidence says | Suggested response [Inference] |
|---|---|---|---|---|
| 1 | "Both: a standing red-team seat (DA) and DI on the top cruxes (Schwenk)" (§2.3, §3) | **Schwenk 1990 (B6), the dossier's own source**; Valacich et al. 1995 (*OBHDP*) and Schwenk et al. 1994 (§3.6) | DA beat the expert approach; DI was not shown to beat it on ill-structured tasks; DA was not worse than DI and in later experiments did better | Use objective DA by default. Restrict DI to cruxes with explicit rival scenario sets. Correct the dossier text. |
| 2 | Red Team as "assigned dissent"; rotating human devil's advocate (§6.3, §6.4 H3) | Nemeth 2001 (B7); Schulz-Hardt 2002 (B8) | Authentic dissent beats contrived devil's advocacy, which can bolster the initial view | Give priority to authentic minority positions. Treat the Red Team as a fallback when pre-votes are homogeneous, aimed at the AI recommendation (B2). |
| 3 | ≥ 3 model families; "the diversity originating from different models is critical" (§3, §6.8) | Ferreira 2026 (B13). The opposite view: Zhang 2025 (B12), Hegazy 2024 | Heterogeneity did not drive gains in small models, accuracy tracked member capability, and mixed teams lost to majority votes | Treat this as an open empirical question. Keep the rule for error independence and auditability, and test it. |
| 4 | Target "hidden-profile surfacing ≥ 80%" (§6.8, §6.11) | Alsobay 2025 (B1) | LLM facilitation raised information sharing, but neither AI nor human facilitation changed decisions | Measure decision accuracy and conversion. Add an integration step. |
| 5 | Human-first ordering: AI conclusions hidden until the vote locks (§3, §6.4 H0) | Kokje 2026 (B18); in support, Agudo 2024 (B17) | Non-concurrent advice reduced over-reliance, but caused under-reliance on correct advice, with no net performance gain | Keep H0, since Agudo supports it. Track under-reliance explicitly. The dossier §8 already anticipates this. |
| 6 | Explanations treated as raising acceptance "regardless of correctness" (§1, §2.6) | Vasconcelos 2023 (B16); Romeo 2025 (B15) | Explanations reduce over-reliance when they lower verification cost. Engagement is the key lever. | Design explanations as cheap verification tools (artifact links, flip thresholds, one-click re-run), not narratives. |
| 7 | Cognitive forcing: a member accepting an AI recommendation writes one way it could be wrong (§6.10 item 6) | Beck 2025 (B20) | Mandatory corrections reduced engagement and increased acceptance of wrong suggestions, in an annotation task | Keep the requirement light (one line). A/B-test it and monitor engagement. |
| 8 | Display the AI track record with confidence intervals as a safeguard (§6.10 item 6) | He et al. 2023 (§3.6) | Information about stated accuracy did not produce appropriate reliance | Not enough on its own. Pair it with personal feedback on override accuracy (B21). |
| 9 | "Aggregate beliefs, not verdicts"; pooled-belief optimum and max-min or minimax-regret over member beliefs (§1 item 4, §2.4, §6.5) | Garlappi 2017 (B22) | Group decisions with heterogeneous beliefs and influence weights are dynamically inconsistent and lead to underinvestment | Add a plan with commitment, a consistency check and a DEFER-bias monitor. Check whether the credal set is rectangular. |
| 10 | Evidence-gated updates: move > 5 pp only with a newly surfaced, validator-checked artifact (§2.5, §6.4 S3) | Kraidia 2026 (B14); RAG paper (§3.6) | Persuasive agents, or selectively retrieved legitimate documents, drive wrong consensus. More agents or rounds do not help. | Audit retrieval selection. Add a second-source rule for conflicted quotes and an influence cap. |
| 11 | "Ensemble for estimates; debate only to surface evidence" presented as settled (§3) | Smit 2024, the dossier's own source (§2.1 item 2) | With tuned agreement levels, debate surpassed every non-debate protocol tested | Keep ensemble-first, but treat debate settings as tunable and re-test on ADIC suites. The companion file also flags this as contested. |
| 12 | Committees outperform individuals, so the committee is the decision unit (§1) | Bär 2011 (B23); Bliss 2008 and Prather 2002 (§3.6). For: Patel & Sarkissian (B24) | Finance teams make less extreme decisions. Performance evidence is mixed and depends on data quality. | Keep the committee as decision unit, but recognize its moderating effect. Add a delegated conviction band. |

---

## 6. Verbatim usage message

> 0 searches left this month; resets to 500 on November 1st.

This was the message after the last search. The counter after each search read 7, 4, 2, 1 and 0. Drops larger than 1 reflect the two other agents searching at the same time.

---

## 7. Query log, WebSearch sources and next searches

### 7.1 Consensus searches (one at a time, query parameter only)

| # | Query | Seed | Records | Dossier citations confirmed | Counter after |
|---|---|---|---|---|---|
| 1 | multi-agent debate language models factuality reasoning | Seed 3 (refined) | 19 | Du; Liang; Choi; Smit | 7 |
| 2 | automation bias overreliance on AI decision support and human-AI team performance | Seed 5 (refined) | 20 | None (backfill only; Vaccaro, Bansal and Buçinca not returned) | 4 |
| 3 | AI-mediated deliberation common ground group discussion | Seed 4 | 20 | Tessler | 2 |
| 4 | devil's advocacy dialectical inquiry group decision quality | Seed 2 | 20 | Schwenk | 1 |
| 5 | investment committees group versus individual decision making teams fund managers | Seed 1 (refined) | 20 | None (Blinder & Morgan not returned) | 0 |

Seed 6 ("noise in judgment decision hygiene") was not run because the quota was exhausted.

### 7.2 WebSearch look-ups (after the quota ran out)

1. Lu, Yuan & McLeod (2012): [SAGE](https://journals.sagepub.com/doi/10.1177/1088868311417243); [Wikipedia: Hidden profile](https://en.wikipedia.org/wiki/Hidden_profile).
2. Baron et al. (2014): [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/deca.2014.0293); [RePEc](https://ideas.repec.org/a/inm/ordeca/v11y2014i2p133-145.html); [Wharton PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2015---two-reasons-to-make-aggregated-probability-forecasts_1.pdf).
3. Parasuraman & Manzey (2010): [SAGE](https://journals.sagepub.com/doi/10.1177/0018720810376055); [TU Berlin](https://depositonce.tu-berlin.de/items/0c787d91-6021-480b-a333-009e0d1d0092/full); [TRID](https://trid.trb.org/View/1085175).
4. List & Pettit (2002): [RePEc](https://ideas.repec.org/a/cup/ecnphi/v18y2002i01p89-110_00.html); [PhilArchive](https://philarchive.org/rec/LISASO-3); [LSE](https://researchonline.lse.ac.uk/id/eprint/704).
5. Meucci (2008): [RePEc / arXiv 1012.2848](https://ideas.repec.org/p/arx/papers/1012.2848.html); [ar5iv](https://ar5iv.labs.arxiv.org/html/1012.2848).
6. Stasser & Titus (1985, 1987): [1985 PDF](https://www.uni-muenster.de/imperia/md/content/psyifp/aeechterhoff/vorlesungkommunikation/stasser_titus_unsharedinfogroupdisc_jpsp1985.pdf); [Wikipedia: Hidden profile](https://en.wikipedia.org/wiki/Hidden_profile); [Pressbooks: shared information bias](https://pressbooks.pub/teams1/chapter/shared-information-bias).
7. Schemmer et al. (2023): [arXiv](https://arxiv.org/abs/2302.02187v3); [KIT](https://publikationen.bibliothek.kit.edu/1000158077); [OpenAlex](https://api.openalex.org/works/doi:10.1145%2F3581641.3584066).
8. Wang, Morgenstern & Dickerson: [arXiv v1](https://arxiv.org/abs/2402.01908v1); [arXiv v3](https://arxiv.org/html/2402.01908v3). The NMI venue was not confirmed.
9. Schoenegger et al., silicon crowd: [arXiv v6](https://arxiv.org/abs/2402.19379v6); [Wharton Knowledge](https://knowledge.wharton.upenn.edu/article/can-ai-predict-the-future/).
10. Blinder & Morgan (2005): [RePEc](https://ideas.repec.org/a/mcb/jmoncb/v37y2005i5p789-811.html); [Berkeley PDF](https://faculty.haas.berkeley.edu/rjmorgan/Two%20Heads.pdf).
11. Smit et al. (ICML 2024): [PMLR](https://proceedings.mlr.press/v235/smit24a.html); [ICML poster](https://icml.cc/virtual/2024/poster/34657).

### 7.3 Next searches after the 1 November reset

1. **Re-check in Consensus** the 10 citations not checked (§2, rows 17–26).
2. **Seed 6:** "noise in judgment decision hygiene"; also "noise audit professional judgment".
3. **"social influence wisdom of crowds deliberation small groups accuracy".** This tests the dossier's principle of independence before interaction (Lorenz et al.). Candidates to look for, recalled and unverified: Navajas et al. (2018), small-group debates aggregated; Becker, Brackbill & Centola (2017), network social influence; Da & Huang (2020), herding in earnings forecasts.
4. **"hidden profile information sharing meta-analysis effect size":** the magnitudes for Lu et al., and the information-load moderator.
5. **"sycophancy persuasion large language models factual accuracy":** re-check Sharma, and confirm the journal versions of Salvi (NHB) and Hackenburg (*Science*).
6. **"debate scalable oversight non-expert judges":** Khan, Michael, Irving, plus 2025–26 follow-ups.
7. **"LLM forecasting versus human forecasters calibration":** the Schoenegger papers and newer benchmarks.
8. **"committee transparency deliberation dissent"** (Hansen; Meade & Stasavage) and **"investment committee pension trustee decision making"** for evidence specific to ICs.
