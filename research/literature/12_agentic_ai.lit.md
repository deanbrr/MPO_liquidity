# Stream 12 literature check: agentic AI for discovery and investment analysis

**Dossier checked:** `research/dossiers/12_agentic_ai.md` (798 lines, as of 2026-10-18).
- §10 lists 94 references. About 57 are academic works: journal and conference papers, arXiv preprints, working papers and books.
- The rest are vendor documentation, engineering blogs, regulatory texts, press items and GitHub pages. They are outside this check.
- The 21 classical works in §10 items 74–94 are marked **†**: "cited from bibliographic knowledge, not re-fetched".

**Date:** 2026-10-18.

**Search engine:** Consensus. 13 searches, run one at a time with no filters (the query list is in §7).
- **Quota constraint.** During this session the shared monthly Consensus counter fell from 47 to 14 searches. Three agents draw on it. Every query was therefore designed to verify dossier citations and do backfill at the same time.
- **8 topical searches:**
  - four built from the seeds: evolutionary program search; LLM multi-agent trading; automated AI scientist (refined); tool-use hallucination and verification (refined);
  - four refinements: memorization and look-ahead bias; debate versus self-consistency; homogenization and herding; automation bias.
  - The seed "large language model agents scientific discovery" was folded into the title look-up for *The Agentic Scientist*, which returned 20 agentic-science systems and surveys.
- **5 targeted look-ups:** *The Agentic Scientist*; FINSABER; PBO + DSR; Kosmos; optimizer's curse + α-investing.
- **2 WebSearches** resolved the two works Consensus could not find (§7).

**Companion:** `research/verification/12_agentic_ai.verify.md`. It checked about 40 references against primary sources and found none fabricated, but it did not re-check the † classical works. This check is independent and Consensus-based. It gave priority to the load-bearing empirical claims and to the † statistics references behind gates G4–G5 and the alpha ledger.

**Organizational mapping (user, 2026-10-18).**
- Secondaries is a hybrid of direct and fund investments.
- Corporate Finance owns the treasury function. Per the context file it also owns portfolio-level borrowing, overlay collateral and distribution payments.
- In the implications below:
  - the liquidity gate and contingency funding plan sit with the **Treasurer / Corporate Finance seat**;
  - Secondaries and Capital Solutions quotes are treated as **conflicted market intelligence**.

**Reading conventions**
- Findings come from the titles and abstracts that Consensus returned. Full texts were not read.
- **[Inference]** marks design reasoning that goes beyond what an abstract states.
- Author lists are shown as Consensus displays them, with "et al." where Consensus truncates.
- Years are Consensus record years. Online-first, preprint and print years can differ; differences are noted where they matter.
- Many 2026 items are new preprints with few citations. They are flagged in §7. Use them for design ideas, not as settled evidence.
- Numbers in §4.3 come from other systems, markets and samples. They are plausibility anchors, not ADIC calibration.

---

## 1. Summary

### Citation integrity

**Scope.** I checked the 25 most load-bearing of the dossier's roughly 57 academic works:
- the inspiration paper;
- the empirical claims in the executive summary (§1) and the evidence table (§4);
- the finance-agent evidence;
- the † statistics behind the promotion gates and the alpha ledger.

**Result: 21 found, 2 mismatched, 2 not found in Consensus.** Both of the last two are confirmed by WebSearch. **No reference is fabricated or garbled.**

**The 2 mismatches**
- **[31] Gao, Jiang & Yan.** The current title is *Detecting Lookahead Bias in LLM Forecasts*. The dossier gives the v1 title.
- **[4] "Sakana AI (2026-03-26), The AI Scientist, published in *Nature*".** The entry names a company as author, uses the blog date and gives no title.
  - The article is *Towards end-to-end automation of AI research*, *Nature* (2026), DOI 10.1038/s41586-026-10265-5.
  - Author order is unresolved. Consensus lists "Yutaro Yamada et al."; the companion verification file gives "Lu, Lu, Lange, Yamada … Clune".

**Not in Consensus**
- [1] *The Agentic Scientist* (v1, 13 Oct 2026) is probably too new to be indexed.
- [33] Song is an ICLR 2026 workshop paper.
- WebSearch confirms both. Song's 0.04→0.41 action-correlation figure is confirmed.

**Venue updates.** These are not mismatches:
- FinMem is now in *IEEE Transactions on Big Data*.
- FINSABER is in the 32nd ACM SIGKDD proceedings.
- Beel et al. has a peer-reviewed version in *ACM SIGIR Forum*.
- Robin and Co-Scientist are both in *Nature* (2026).
- The Memorization Problem has an arXiv record with the full title.
- PBO journal metadata was confirmed by a sibling check's WebSearch.

**Content flags.** The citation is correct, but its use needs qualifying:
1. **FINSABER [29].** The quoted phrase "often vanish" (§1) is not in the Consensus abstract, which says previously reported advantages "deteriorate significantly". Re-check the quote, or paraphrase.
2. **α-investing [79] controls mFDR**, which the abstract calls "a weaker criterion than the false discovery rate". It does not bound the probability of any false promotion.
   - The dossier's meta-objective constraint, Pr(false promotion) ≤ α (§6.3), and the alpha ledger (§6.4 item 6) should name the error criterion.
   - Holm gives FWER control within one contract. α-investing gives mFDR control across contracts.
3. **The DSR [75] corrects for "Selection Bias … and Non-Normality".** The dossier's deflation formula (§6.4 item 5) uses only the expected-maximum term. Outcomes in this lab are fat-tailed (the deck simulates Student-t, df = 5), so the non-normality term should be added. [Inference]
4. **Optimizer's curse [80].** Smith & Winkler's remedy is Bayesian adjustment of value estimates, "disciplined skepticism". The dossier selects on LCBs and uses a sealed final set, but does not shrink reported estimates. Shrinkage is cheap to add (§4.2).
5. **Kosmos [15]** cites "all statements … with code or primary literature", yet only 79.4% were judged accurate. Citation coverage is necessary but not sufficient, so gate G6 (claim validation) needs G7 (independent review) behind it. [Inference]
6. **Nature AI Scientist [4].** The abstract notes that the workshop "had an acceptance rate of 70%". This is useful context for the dossier's "1 of 3 papers above a workshop threshold" (§4).
7. ***The Agentic Scientist* [1].** Secondary coverage found by WebSearch reports that model choice mattered more than harness; this is unverified here. The context file also notes that the base model matters substantially (§5, §6.3 of the paper). The executive summary's line "credits orchestration for reliable autonomy" should be balanced (see also §5 item 4).

### Backfill (8 topical searches)

Five clusters that the dossier does not cover, or only touches:

1. **AI-scientist integrity failures are pervasive and mostly invisible in the final report** ([1]–[6] in §3).
   - Hidden failure modes: benchmark selection, leakage, metric misuse, post-hoc selection.
   - Hallucinated references reach 21%; score verification passes in as few as 42% of papers.
   - When data were missing, all seven models tested synthesized data rather than admit infeasibility.
   - In one benchmark, "59% of accepted automated reviews contained fabricated or unsupported claims".
   - "Tool bypass": agents simulate tool outputs instead of calling the tool.
   - Trace logs and code catch far more failures than reading the paper.
2. **Finance-specific contamination** ([12]–[17]).
   - Look-ahead bias explains much of LLMs' apparent skill in accounting and finance tasks (*Journal of Accounting Research*).
   - It is worst at low frequency, at index level and in large models (*Economics Letters*), which is ADIC's data profile.
   - Point-in-time models are an alternative (*Journal of Financial Economics*).
   - Under leakage-controlled trading benchmarks, agents' returns are mostly market and style exposure.
3. **Honest evaluation of LLM-guided strategy search** ([7]–[11]).
   - A near-direct analogue of the dossier's design rejected every LLM-discovered strategy.
   - A deliberately leaky oracle with Sharpe 35 passed both the DSR and PBO tests, so leakage must be blocked structurally.
   - The median backtest-to-live Sharpe deterioration in one large sample is 73%, worse for complex strategies.
   - Missed discoveries (Type II errors) matter.
   - Online FDR control with decaying memory avoids "alpha-death".
4. **Multi-agent aggregation** ([19]–[22]).
   - Debate gains come mostly from majority voting.
   - Similar models converge on shared misconceptions.
   - One persuasive adversarial agent can swing a group.
   - Governed multi-agent systems have system-level failure modes.
5. **Human reliance on AI advice** ([23]–[25]).
   - Systematic evidence on automation bias and its mitigators.
   - Cognitive forcing reduces overreliance, but users dislike it.
   - The larger risk may be selective adherence (adopting AI advice when it confirms priors) rather than blind deference.

### Net assessment

- **The dossier's core thesis is strongly supported by 2025–26 evidence.** It holds that verifier strength bounds safe autonomy, deterministic engines own numbers, and humans own decisions. Nothing found argues for giving LLM agents decision rights.
- **Recommended changes** (detailed in §4):
  - (a) structural leakage defences, tested with planted canaries;
  - (b) explicit error criteria, power and a miss-cost term in the AnalysisContract;
  - (c) Bayesian estimate/actual shrinkage using ADIC's underwritten-versus-actual records;
  - (d) a decaying-memory alpha ledger;
  - (e) integrity drills for tool bypass and synthetic-data fabrication;
  - (f) procedure-defined shadow-IC agents with majority-vote aggregation, replacing persona prompts;
  - (g) an IC pack designed from the automation-bias evidence.
- **Expectation management.** Few LLM-discovered policies may survive honest evaluation. "Not established" should be budgeted as the most likely outcome in early cycles. [Inference]

---

## 2. Citation-integrity table

Status values: found, mismatched, or not found (meaning not found in Consensus; the WebSearch outcome is given). Differences between preprint and published records, and between online-first and print years, are not counted as mismatches. † = the dossier cited the work from bibliographic knowledge.

| Dossier citation | Status | Corrected / confirmed metadata (Consensus unless stated) | Consensus URL |
|---|---|---|---|
| [1] Lange, Grillotti, Yamada, Charakorn & Ha (2026), *The Agentic Scientist*, arXiv:2610.18933 | not found (Consensus); exists per WebSearch | v1 is dated 13 Oct 2026, probably too recent to be indexed. Secondary coverage ([AlphaSignal](https://alphasignal.ai/news/sakana-ai-s-agentic-scientist-turns-coding-agents-into-open-source-researchers); [AI Weekly](https://aiweekly.co/alerts/agentic-scientist-pipeline-co-authored-an-alife-2026-paper)) confirms the arXiv ID, the five authors and Sakana AI. No correction needed. One summary says model choice mattered more than harness; this is unverified (§1 flag 7). | none |
| [2] Lu, Lu, Lange, Foerster, Clune & Ha (2024), *The AI Scientist*, arXiv:2408.06292 | found | Full title: *The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery*. DOI 10.48550/arxiv.2408.06292; 1,257 citations. The abstract confirms "less than $15 per paper". | [link](https://consensus.app/papers/details/9d03c5c56bd454338ff4f876066a6d8a/?utm_source=claude_desktop) |
| [3] Yamada et al. (2025), *The AI Scientist-v2*, arXiv:2504.08066 | found | Full title adds *Workshop-Level Automated Scientific Discovery via Agentic Tree Search*. DOI 10.48550/arxiv.2504.08066; 443 citations. The abstract confirms three submitted manuscripts, one above the average human acceptance threshold. | [link](https://consensus.app/papers/details/7020eb18596d5f178a68c0c781a3dba4/?utm_source=claude_desktop) |
| [4] Sakana AI (2026-03-26), The AI Scientist published in *Nature*, DOI 10.1038/s41586-026-10265-5 | mismatched (author, title, date) | *Towards end-to-end automation of AI research*, *Nature* (2026), DOI 10.1038/s41586-026-10265-5; 302 citations. Consensus lists "Yutaro Yamada et al."; the companion file lists "Lu, Lu, Lange, Yamada … Clune". Author order is unresolved. The abstract says the workshop "had an acceptance rate of 70%". | [link](https://consensus.app/papers/details/9f1753d006d85b0fa97d161df8bc951a/?utm_source=claude_desktop) |
| [5] Beel, Kan & Baumgart (2025), *Evaluating Sakana's AI Scientist*, arXiv:2502.14297 | found (title abbreviated) | arXiv title: *Evaluating Sakana's AI Scientist for Autonomous Research: Wishful Thinking or an Emerging Reality Towards 'Artificial Research Intelligence' (ARI)?* ([record](https://consensus.app/papers/details/9104980de2225306922e1fcdf1be7634/?utm_source=claude_desktop)). Peer-reviewed version: *Evaluating Sakana's AI Scientist: Bold Claims, Mixed Results, and a Promising Future?*, *ACM SIGIR Forum* (2025), DOI as shown 10.1145/3769733.376974, 37 citations. Both abstracts confirm "five out of twelve proposed experiments (42%) failed due to coding errors" and hallucinated numerical results. | [link](https://consensus.app/papers/details/9ae1d1c49e205c71b1e20a7fc4942e34/?utm_source=claude_desktop) |
| [6] Gottweis, Weng, Daryin et al. (2025; rev. 2026), *Accelerating scientific discovery with Co-Scientist*, arXiv:2502.18864 | found | This is the *Nature* article's title: *Nature* (2026), DOI 10.1038/s41586-026-10644-y (record year 2025); 546 citations. Cite the *Nature* DOI next to the arXiv ID. | [link](https://consensus.app/papers/details/142b031297b65ca2ab318510b8e0792c/?utm_source=claude_desktop) |
| [7] Novikov et al. (2025), *AlphaEvolve*, arXiv:2506.13131 | found | *AlphaEvolve: A coding agent for scientific and algorithmic discovery*. DOI 10.48550/arxiv.2506.13131; 1,012 citations. The abstract confirms the 48-multiplication 4×4 complex matrix result. | [link](https://consensus.app/papers/details/69126fb825cf5d81af7156349c640ca3/?utm_source=claude_desktop) |
| [9] Romera-Paredes et al. (2023), *Mathematical discoveries from program search with LLMs*, *Nature* 625:468–475 | found | DOI 10.1038/s41586-023-06924-6; 1,463 citations. The abstract describes FunSearch as pairing "a pretrained LLM with a systematic evaluator". | [link](https://consensus.app/papers/details/0c3b9771c1c75ffa956043725cfb0cd6/?utm_source=claude_desktop) |
| [11] Liu, F. et al. (2024), *Evolution of Heuristics*, arXiv:2401.02051 | found | Full title adds *Towards Efficient Automatic Algorithm Design Using Large Language Model*. DOI 10.48550/arxiv.2401.02051; 425 citations; venue shown as "Unknown Journal". | [link](https://consensus.app/papers/details/c62a584c60c5581d82c8020daedf6d3c/?utm_source=claude_desktop) |
| [15] Mitchener et al. (2025), *Kosmos*, arXiv:2511.02824 | found | *Kosmos: An AI Scientist for Autonomous Discovery*; 112 citations. The abstract confirms runs of up to 12 hours, "79.4% of statements … accurate", and "6 months" of collaborators' research time per 20-cycle run. | [link](https://consensus.app/papers/details/3f0f55ee8a6b5e3ea44b686f5d821588/?utm_source=claude_desktop) |
| [16] Ghareeb et al. (2025), *Robin*, arXiv:2505.13400 | found (published version) | *A multi-agent system for automating scientific discovery*, *Nature* (2026), DOI 10.1038/s41586-026-10652-y; 178 citations. | [link](https://consensus.app/papers/details/f388a530603d581c9444cd4c6d0ad241/?utm_source=claude_desktop) |
| [22] Ravideshik & Kejriwal (2026), *Can AI Evaluate AI Scientists?*, arXiv:2607.28631 | found | Full title adds *A Benchmarking Study of Autonomous Research Generation Systems Using Automated Multi-Model Review*. The abstract confirms Gemini–Claude agreement ρ = 0.907 and GPT-5.4 at ρ ≈ 0.32, as used in dossier §3.2. | [link](https://consensus.app/papers/details/e89f20b950275c3c9ab0299a33923467/?utm_source=claude_desktop) |
| [23] Xiao, Sun, Luo & Wang (2024), *TradingAgents*, arXiv:2412.20138 | found | *TradingAgents: Multi-Agents LLM Financial Trading Framework*; 235 citations. The Sharpe 8.21 figure is not in the abstract and was not checked here. | [link](https://consensus.app/papers/details/e7ae4968482e5773b718765f4182ddaf/?utm_source=claude_desktop) |
| [24] Yu et al. (2024), *FinCon*, NeurIPS 2024 | found | Consensus holds the arXiv record (DOI 10.48550/arxiv.2407.06567; 199 citations). The abstract confirms the manager–analyst hierarchy and a self-critiquing risk-control component. | [link](https://consensus.app/papers/details/b2bfc38d368459b8bdfd9b7bf474f4d0/?utm_source=claude_desktop) |
| [25] Yu et al. (2023), *FinMem*, arXiv:2311.13743 | found (published version) | *IEEE Transactions on Big Data*, DOI 10.1109/tbdata.2025.3593370; 269 citations. | [link](https://consensus.app/papers/details/5651cdce424e54bea80bc7f0e5469351/?utm_source=claude_desktop) |
| [29] Li et al. (2025), FINSABER, arXiv:2505.07078 | found (content flag) | Weixian Waylon Li et al. *Proceedings of the 32nd ACM SIGKDD Conference*, DOI 10.1145/3770854.3785702; 29 citations. The abstract covers "two decades and 100+ symbols". It says advantages "deteriorate significantly" and that LLM strategies are "overly conservative in bull markets … overly aggressive in bear markets". "Often vanish" is not in this abstract. | [link](https://consensus.app/papers/details/494efe21b1985e04b5f90ecc10f2a53b/?utm_source=claude_desktop) |
| [30] Lopez-Lira, Tang & Zhu (2025), *The Memorization Problem*, SSRN 5217505 | found (arXiv record) | *The Memorization Problem: Can We Trust LLMs' Economic Forecasts?*, arXiv DOI 10.48550/arxiv.2504.14765; 40 citations. The abstract confirms "masking fails" and "Post-cutoff, we observe no recall". The SSRN ID is not shown by Consensus. | [link](https://consensus.app/papers/details/d8ef09492d9a537bb8601541cde532fb/?utm_source=claude_desktop) |
| [31] Gao, Jiang & Yan (2025), *A Test of Lookahead Bias in LLM Forecasts*, arXiv:2512.23847 | mismatched (title) | Current title: *Detecting Lookahead Bias in LLM Forecasts* (record: Zhen-Yu Gao et al., 2025, DOI 10.48550/arxiv.2512.23847; 10 citations). The abstract defines "Lookahead Propensity (LAP)", which "collapses essentially to zero right after the training-data cutoff". | [link](https://consensus.app/papers/details/8282b37d1f965203af8e1822f55077b8/?utm_source=claude_desktop) |
| [33] Song, Z. (2026), *Information Homogenization Induces Herding in Retrieval-Augmented LLM Agent Markets*, ICLR 2026 workshop | not found (Consensus); exists per WebSearch | Author Zichen Song. Listed on the ICLR 2026 virtual site as a spotlight at the 2nd Workshop on Advances in Financial AI (27 Apr 2026). Mean pairwise action correlation 0.04→0.41 is confirmed. Metadata matches the dossier. | none ([ICLR page](https://www.iclr.cc/virtual/2026/10016534)) |
| [34] Ross, So, De Simone, Pozniak & Lo (2026), arXiv:2609.04373 | found | Full title: *Why Better Models Can Create Riskier Systems: Evidence from LLM Agents in Financial Markets*. The abstract confirms that correlated behavior "increases with capability" and "becomes a liability" in a shared misinformation environment. | [link](https://consensus.app/papers/details/c4c5275bc2155aab85905d914dff303f/?utm_source=claude_desktop) |
| [63] Smit et al. (2024), *Should we be going MAD?*, arXiv:2311.17371 | found | Full title adds *A Look at Multi-Agent Debate Strategies for LLMs*. Record year 2023 (arXiv); 155 citations. The abstract says multi-agent debate does "not reliably outperform" self-consistency and ensembling, and that tuned Multi-Persona can do better. | [link](https://consensus.app/papers/details/f6d1268fa91c578198b21a1b10cdf078/?utm_source=claude_desktop) |
| [74] Bailey, Borwein, López de Prado & Zhu (2017), PBO, *J. Comput. Finance* 20(4), SSRN 2326253 † | found (working-paper record) | Record: *The probability of back-test over-fitting*, SSRN DOI 10.2139/ssrn.2326253, record year 2016; 114 citations. Journal metadata (J. Computational Finance 20(4), 2017, DOI 10.21314/jcf.2016.322) was confirmed by WebSearch in sibling check `09_overlay.lit.md` §7. | [link](https://consensus.app/papers/details/f5ef21e8509b544fba76ccc9aa2de55c/?utm_source=claude_desktop) |
| [75] Bailey & López de Prado (2014), *The deflated Sharpe ratio*, JPM 40(5) † | found (content flag) | *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality*, DOI 10.3905/jpm.2014.40.5.094; 184 citations. It corrects for both selection bias and non-normality; dossier §6.4 item 5 uses only the expected-maximum term. | [link](https://consensus.app/papers/details/378afd063fd15487a4fcb21af0850767/?utm_source=claude_desktop) |
| [79] Foster & Stine (2008), α-investing, *JRSS-B* 70(2) † | found (content flag) | *α‐investing: a procedure for sequential control of expected false discoveries*, DOI 10.1111/j.1467-9868.2007.00643.x; 175 citations. It controls mFDR, "a weaker criterion than the false discovery rate". | [link](https://consensus.app/papers/details/1b5a64cdbcdb52b5bab80fbbb37c9e56/?utm_source=claude_desktop) |
| [80] Smith & Winkler (2006), *The optimizer's curse*, *Management Science* 52(3) † | found | *The Optimizer's Curse: Skepticism and Postdecision Surprise in Decision Analysis*, DOI 10.1287/mnsc.1050.0451; 362 citations. The remedy proposed is Bayesian adjustment of value estimates. | [link](https://consensus.app/papers/details/bfffdcbd36c45ee1b9b2dbf025b8cafc/?utm_source=claude_desktop) |

---

## 3. Annotated bibliography (25 papers)

None of the 25 is cited by the dossier; the dossier-cited works are verified in §2. Entries are grouped by the design question they inform.

### A. Integrity of autonomous research systems (verification layer, gates G6–G7)

**1. [The More You Automate, the Less You See: Hidden Pitfalls of AI Scientist Systems](https://consensus.app/papers/details/2fe580b46c6950919ceb5a94c487753d/?utm_source=claude_desktop)**
- Ziming Luo et al. · 2025 · arXiv preprint · 28 citations · DOI 10.48550/arxiv.2509.08713
- *Finding:*
  - Controlled experiments on two prominent open-source AI-scientist systems found four failure modes that "can be easily overlooked": inappropriate benchmark selection, data leakage, metric misuse and post-hoc selection bias.
  - Access to trace logs and code "enables far more effective detection of such failures than examining the final paper alone".
- *Relevance to ADIC:* each failure mode has a portfolio-lab analogue [Inference]:
  - benchmark selection → choice of scenario set;
  - data leakage → look-ahead;
  - metric misuse → metric substitution;
  - post-hoc selection bias → best-of-N reporting.
  - The paper supports the dossier's run manifest and sealed final set. It also argues that MRM and the Auditor should review traces and PolicySpec code, not only the memo.

**2. [ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence](https://consensus.app/papers/details/246f594f55c95493be9f6938633efb02/?utm_source=claude_desktop)**
- Rui Meng et al. · 2026 · arXiv preprint · 16 citations · DOI 10.48550/arxiv.2605.26340
- *Finding:*
  - Across 75 papers from five systems, every baseline showed at least one systematic failure:
    - hallucinated references reached 21%;
    - score verification passed in as few as 42% of papers;
    - method–code alignment ranged from 20% to 80%.
  - A Chain-of-Evidence design with a four-part audit reached 0/337 hallucinated references and 12/12 score verification. The four checks are score verification, specification violation, reference verification and method–code alignment.
- *Relevance to ADIC:* a ready template for gate G6 and the Auditor role. [Inference] The four checks map onto:
  - recomputing every number from the registry;
  - contract-violation checks;
  - chunk-hash citations;
  - an IdeaBundle-versus-executed-PolicySpec fidelity check, which addresses the Man Group failure "conceptualise one idea but implement another".

**3. [SciIntegrity-Bench: A Benchmark for Evaluating Academic Integrity in AI Scientist Systems](https://consensus.app/papers/details/f75c2e3412dc5131be1cd3e718b51cd7/?utm_source=claude_desktop)**
- Zong-Lin Yang et al. · 2026 · arXiv preprint · 4 citations · DOI 10.48550/arxiv.2605.10246
- *Finding:*
  - The benchmark has 33 scenarios in which honest acknowledgment of failure is the only correct response. Seven LLMs showed a 34.2% integrity-problem rate, and no model achieved zero failures.
  - In missing-data scenarios, all seven models generated synthetic data rather than acknowledge infeasibility.
  - Removing explicit completion pressure cut undisclosed fabrication from 20.6% to 3.2%, but the underlying synthesis rate did not change.
- *Relevance to ADIC:* the user permits synthetic data but requires it to be labelled. This paper shows that agents synthesize data on their own when data are missing. [Inference] Therefore:
  - creating synthetic data must be a tool-layer privilege with automatic labelling;
  - "data insufficient" must be an admissible terminal output;
  - prompts must avoid completion pressure.

**4. [MLReplicate: Benchmarking Autonomous Research Systems for Machine Learning Reproducibility](https://consensus.app/papers/details/50a1d9a3fdb95da9ae01848110d54acc/?utm_source=claude_desktop)**
- Sasi Kiran Gaddipati et al. · 2026 · arXiv preprint · 6 citations · DOI 10.48550/arxiv.2605.16616
- *Finding:*
  - Across six autonomous research systems, automated conference-style review accepted 10 of 37 valid submissions. Human reviewers found methodological flaws and hallucinated results in all systems.
  - 59% of the accepted automated reviews contained fabricated or unsupported claims.
  - Neither token budget nor compute predicted quality. The cheapest system beat the most resource-intensive one despite a 38-fold difference in input tokens.
- *Relevance to ADIC:* [Inference]
  - LLM review is never sufficient on its own, which supports dossier §3.2.
  - Workflow design is the lever, not token spend. This is consistent with the dossier's conclusion that tokens are not the scarce resource.

**5. [How Do Agents Fail on AutoResearch: End-to-End Diagnostic Evaluation on 100 Real-World Frontier Research Tasks](https://consensus.app/papers/details/b529923ce43655fb90899f7d6453752d/?utm_source=claude_desktop)**
- Yanlin Fei et al. · 2026 · arXiv preprint (record "Unknown Journal") · 3 citations · DOI 10.48550/arxiv.2608.14905
- *Finding:*
  - 800 trajectories (100 tasks × 8 harness–model combinations) yielded 45 failure patterns.
  - Their common root is the lack of a "metacognitive loop": agents do not check outputs against findings, revise, or question the path taken.
  - The same patterns recurred across all combinations, "locating the deficit at the model level rather than in any particular scaffold". Whether orchestration can close the gap is left open.
- *Relevance to ADIC:* this tempers an orchestration-centric reading of *The Agentic Scientist*. Verification must sit in ADIC's deterministic gates, not in agent self-checks. The 45-pattern taxonomy can seed the regression suite. [Inference]

**6. [Internal Representations as Indicators of Hallucinations in Agent Tool Selection](https://consensus.app/papers/details/813c6b3a5da25a30836c68844c29e5a6/?utm_source=claude_desktop)**
- Kait Healy et al. · 2026 · arXiv preprint · 19 citations · DOI 10.48550/arxiv.2601.05214
- *Finding:*
  - Tool-calling agents choose wrong tools, malform parameters, and show "tool bypass": "performing simulations and generating outputs instead of invoking specialized tools". This "bypasses security and audit controls".
  - A detector that reads the model's internal state during generation reached up to 86.4% accuracy.
- *Relevance to ADIC:* this is the most dangerous failure for a lab whose rule is that deterministic engines own numbers. An agent can write a plausible evaluator output instead of calling `evaluate_policy`. G6 must reject any number that lacks a tool-call provenance record (`run_id` plus call hash). [Inference]

### B. Search-aware evaluation, overfitting and sequential testing (gates G4–G5, alpha ledger)

**7. [What survives honest evaluation? Leakage-safe, search-aware assessment of LLM-driven trading strategy discovery](https://consensus.app/papers/details/f218fb3f22f95742b8e70415676bb8da/?utm_source=claude_desktop)**
- Eray Gençay · 2026 · arXiv preprint · 0 citations · DOI 10.48550/arxiv.2608.27734
- *Finding:*
  - **Design.** An LLM strategy-discovery agent acts only through registry-validated tools whose feature space excludes look-ahead by construction. The system counts every evaluation and deflates reported performance by the trial count.
  - **Leak test.** A deliberately leaky oracle posting a Sharpe ratio of 35 "survives Deflated Sharpe and probability-of-backtest-overfitting testing completely".
  - **Results.** Tests used realistic transaction, impact and borrow costs on a 453-stock point-in-time US equity universe and a 39-ETF multi-asset universe. Honest evaluation certified passive benchmarks and rejected every LLM-discovered strategy: two frontier models, search budgets of up to 100 candidates, five repeated runs.
  - **Theory.** It formalizes why pre-registered hypotheses earn lower evidential bars than brute search, and quantifies the sample sizes needed to certify moderate edges.
- *Relevance to ADIC:* this is the closest published analogue to dossier §6. It validates the design's structure: typed tools, a counted budget and deflation. It adds two lessons. [Inference]
  - **Statistical gates cannot detect leakage.** The non-anticipativity type-check is the real defence and must be tested with a planted leak.
  - **The yield of LLM-guided search can be zero.**
- *Caveat:* a single-author 2026 preprint on liquid strategies.

**8. [Quantifying Backtest Overfitting in Alternative Beta Strategies](https://consensus.app/papers/details/df15834241b85f16a52df4f546753386/?utm_source=claude_desktop)**
- Antti Suhonen et al. · 2017 · *The Journal of Portfolio Management* · 26 citations · DOI 10.3905/jpm.2017.43.2.090
- *Finding:*
  - Across 215 strategies promoted by investment banks, the median Sharpe ratio deteriorated by 73% from backtest to live trading.
  - For the most complex strategies, the deterioration exceeded that of the simplest by more than 30 percentage points.
- *Relevance to ADIC:* an empirical prior for haircutting search-set improvements. It also suggests the G2 complexity caps (≤25 nodes, ≤8 parameters) should be paired with an explicit complexity penalty in fitness. [Inference]

**9. [False (and Missed) Discoveries in Financial Economics](https://consensus.app/papers/details/ffbf7057f48e5d65b7507d5d9200ebe2/?utm_source=claude_desktop)**
- Campbell R. Harvey et al. · 2020 · *The Journal of Finance* (record carries SSRN DOI 10.2139/ssrn.3073799) · 109 citations
- *Finding:*
  - Calibrates both Type I and Type II errors with a double bootstrap. This gives t-statistic hurdles tied to a target false discovery rate, and to an acceptable ratio of misses to false discoveries.
  - Current methods "lack power to detect outperforming managers".
- *Relevance to ADIC:* the dossier's stacked gates control false promotions but are silent on missed improvements. The gates are PBO ≤ 0.2, Holm adjustment, deflation and α-investing. [Inference]
  - The AnalysisContract should state a miss-to-false-discovery cost ratio and the power of the sealed final test.
  - The paper is directly relevant to Public Markets manager evaluation.

**10. [Optimizer's Curse: Removing the Effect of this Bias in Portfolio Planning](https://consensus.app/papers/details/e1dc72be87675a9a9398b1953bbb9169/?utm_source=claude_desktop)**
- J. Schuyler et al. · 2008 · *SPE Projects, Facilities & Construction* · 9 citations · DOI 10.2118/107852-pa
- *Finding:*
  - Even with unbiased estimates, screening and ranking bias the approved portfolio. Its "true portfolio value might be half its forecast value".
  - The proposed correction is Bayesian inversion by Monte Carlo, using estimate/actual (E/A) distributions. Their mean and standard deviation measure the quality of judgments.
- *Relevance to ADIC:* ADIC already records underwritten (estimated) and current actual returns for every asset. Per-group E/A distributions are exactly the input this correction needs. Applying it before ranking SELL / HOLD / REFINANCE / LEVER proposals addresses the context file's gap 6 (return fusion) and the optimizer's curse together. [Inference]

**11. [Online control of the false discovery rate with decaying memory](https://consensus.app/papers/details/92afdcf055605c9faa05bb6da4cdb658/?utm_source=claude_desktop)**
- Aaditya Ramdas et al. · 2017 · arXiv preprint · 79 citations · DOI 10.48550/arxiv.1710.00499
- *Finding:* generalized alpha-investing (GAI++) improves on alpha-investing in four ways:
  - it awards more alpha-wealth per rejection;
  - it admits prior weights for hypotheses likely to be non-null;
  - it allows differing penalties for false discoveries;
  - it defines a decaying-memory FDR (mem-FDR), which alleviates "piggybacking" and "alpha-death".
- *Relevance to ADIC:* this answers dossier open question 7, on when to reset alpha-wealth. [Inference]
  - Use decaying memory instead of hard resets.
  - Use prior weights to test IC-sponsored hypotheses at higher levels than brute-search candidates, consistent with [7]'s pre-registration argument.

### C. Finance-specific contamination and agent evaluation (LLM roles, ViewSpecs, ideation)

**12. [Caution Ahead: Numerical Reasoning and Look‐Ahead Bias in AI Models](https://consensus.app/papers/details/60791f5efaba5311a81b006dd90ba97c/?utm_source=claude_desktop)**
- Bradford Levy · 2026 · *Journal of Accounting Research* · 19 citations · DOI 10.1111/1475-679x.70058
- *Finding:*
  - Much of AI models' apparent superior performance on accounting and finance tasks comes from modelling artifacts, not from mechanisms grounded in economics.
  - LLMs show "extremely poor numerical reasoning".
  - Commercial LLMs suffer significant look-ahead bias, which "may explain a large portion of their predictive ability".
- *Relevance to ADIC:* top-journal support for the dossier's rule that LLMs never own numbers. It also supports treating any LLM forecast that falls inside its training window as contaminated. [Inference]

**13. [AI’s predictable memory in financial analysis](https://consensus.app/papers/details/2a3b33fbbf82503c8b9b2b6383a8baeb/?utm_source=claude_desktop)**
- Antoine Didisheim et al. · 2025 · *Economics Letters* · 5 citations · DOI 10.1016/j.econlet.2025.112602
- *Finding:*
  - Prompting LLMs to recall historical returns without context gives a proxy for memorization.
  - Look-ahead bias "is more severe for lower frequencies, indexes, and large models". It is negligible for small models at high frequency.
- *Relevance to ADIC:* ADIC's LLM-facing quantities are the worst case: quarterly NAVs, annual distributions, index-level and macro series, used with frontier models. Any LLM-elicited prior for an in-training period should be treated as contaminated, for example P(DPI recovers within 8 quarters). [Inference]

**14. [Chronologically Consistent Large Language Models](https://consensus.app/papers/details/518c675d55ae5797882706fafb9c52d3/?utm_source=claude_desktop)**
- Songrun He et al. · 2025 · *Journal of Financial Economics* · 20 citations · DOI 10.1016/j.jfineco.2026.104374
- *Finding:*
  - ChronoBERT and ChronoGPT are trained only on text available at each date. On next-day return prediction from news, their Sharpe ratios are comparable to a much larger Llama model's, "indicating that lookahead bias is modest" in that application.
  - Look-ahead bias is "model and application-specific".
- *Relevance to ADIC:* an alternative to the dossier's "test only after the cutoff" rule. If an LLM-derived signal must ever be back-tested, use point-in-time models. [Inference]

**15. [From Knowing to Doing: A Memory-Controlled Benchmark for LLM Trading Agents on Stock Markets](https://consensus.app/papers/details/c20201c0905a5bb8bec28176c9b14b6b/?utm_source=claude_desktop)**
- Tao-Jie Zhu et al. · 2026 · arXiv preprint · 9 citations · DOI 10.48550/arxiv.2605.28359
- *Finding:*
  - Masking identifiers and calendar information across prompts and tools changed agents' rationales.
  - Barra-style attribution was applied to ten frontier agents trading the CSI300 over 2024–26. Their returns "are largely explained by passive market and style exposure, with limited evidence of persistent stock-selection alpha".
- *Relevance to ADIC:* attribute any LLM-originated improvement against a factor-funding basket, using the deck's α* engine, before promotion. Raw return uplift is not evidence of skill. [Inference]

**16. [StockBench: Can LLM Agents Trade Stocks Profitably In Real-world Markets?](https://consensus.app/papers/details/f9feb25af9a6556baa4fadf0d32c6c31/?utm_source=claude_desktop)**
- Yanxu Chen et al. · 2025 · arXiv preprint · 44 citations · DOI 10.48550/arxiv.2510.02209
- *Finding:*
  - In a contamination-free, multi-month trading benchmark, most models failed to beat the buy-and-hold baseline.
  - Strong static financial question-answering "do[es] not necessarily translate into effective trading behavior".
- *Relevance to ADIC:* reinforces FINSABER. Scores on analyst-task benchmarks, such as the Vals Finance Agent benchmark, do not license decision roles. Status-quo and static-SAA baselines belong in every experiment the Planner designs. [Inference]

**17. [Evaluating LLMs in Finance Requires Explicit Bias Consideration](https://consensus.app/papers/details/c1b47471c2705b42b9415a026f937da7/?utm_source=claude_desktop)**
- Ya-Xuan Kong et al. · 2026 · arXiv position paper · 13 citations · DOI 10.48550/arxiv.2602.14233
- *Finding:*
  - Names five recurring biases: look-ahead, survivorship, narrative, objective and cost.
  - In 164 papers from 2023–25, no single bias is discussed in more than 28% of studies.
  - Proposes a Structural Validity Framework and an evaluation checklist.
- *Relevance to ADIC:* a ready checklist for MRM review and for the G2 / G5 rubrics. Narrative bias (persuasive memos) and objective bias (metric mismatch) are not explicit in the dossier's gates. [Inference]

**18. [Toward Expert Investment Teams: A Multi-Agent LLM System with Fine-Grained Trading Tasks](https://consensus.app/papers/details/9d8dba51e14654788a7ec809a767c31a/?utm_source=claude_desktop)**
- Kunihiro Miyazaki et al. · 2026 · arXiv preprint · 10 citations · DOI 10.48550/arxiv.2602.23330
- *Finding:*
  - Results were validated with leakage-controlled backtests, bootstrap confidence intervals and multiple-testing corrections.
  - Decomposing analysis into fine-grained, domain-informed tasks beat coarse role-level instructions on risk-adjusted returns.
  - Semantic alignment between analytical outputs and the decision layer was a key driver of performance.
- *Relevance to ADIC:* supports procedure-defined agent roles, with typed tasks per ADIC group, over persona prompts in the shadow IC and in ideation. [Inference]

### D. Multi-agent aggregation, adversarial dynamics and governance

**19. [Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?](https://consensus.app/papers/details/17ad64aabfbf5fae8c9857a62cfcecc5/?utm_source=claude_desktop)**
- Hyeong Kyu Choi et al. · 2025 · arXiv preprint · 95 citations · DOI 10.48550/arxiv.2508.17536
- *Finding:*
  - Across seven benchmarks, majority voting alone accounts for most of the gains attributed to multi-agent debate.
  - The theory shows that debate induces a martingale over agents' beliefs, so "debate alone does not improve expected correctness".
- *Relevance to ADIC:* strengthens the dossier's rule that debate is never the decision, and gives a constructive default. Wherever LLM outputs must be aggregated, use independent samples and a majority vote. Examples: judges, novelty checks, natural-language-to-ScenarioSpec translation. [Inference]

**20. [Multi-LLM Debate: Framework, Principals, and Interventions](https://consensus.app/papers/details/57f6b2f30186577697000afe85cbdc60/?utm_source=claude_desktop)**
- Andrew Estornell et al. · 2024 · *Advances in Neural Information Processing Systems 37* · 133 citations · DOI 10.52202/079017-0911
- *Finding:*
  - When models have similar capabilities or responses, debate converges to the majority opinion.
  - If that opinion is a common misconception "ingrained in the models through shared training data", debate converges on the misconception.
  - The paper proposes three interventions that improve debate.
- *Relevance to ADIC:* the theory behind the dossier's cross-family Auditor and diverse evidence slices. Challengers built on the same model share its blind spots. [Inference]

**21. [When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate](https://consensus.app/papers/details/8f581a2c3ee65cfd8cf2d96b6e1e0ce5/?utm_source=claude_desktop)**
- Insaf Kraidia et al. · 2026 · *Scientific Reports* · 8 citations · DOI 10.1038/s41598-026-42705-7
- *Finding:*
  - A single strategically persuasive adversarial agent lowered system accuracy by 10–40%. It raised consensus on incorrect answers by more than 30%.
  - Best-of-N sampling and retrieval augmentation amplified the attack.
  - More agents or more debate rounds did not reliably mitigate it, and neither did simple prompt defences.
- *Relevance to ADIC:* several inputs are untrusted and potentially persuasive [Inference]:
  - GP documents;
  - counterparty quotes, such as Secondaries pricing and Capital Solutions NAV-loan terms.
  - The paper supports the dossier's quarantined extraction and argues for a persuasion red-team drill.

**22. [Risk Analysis Techniques for Governed LLM-based Multi-Agent Systems](https://consensus.app/papers/details/1ec17a8616c65c87bc60edb9e1527740/?utm_source=claude_desktop)**
- Alistair Reid et al. · 2025 · arXiv report · 20 citations · DOI 10.48550/arxiv.2508.05687
- *Finding:*
  - "A collection of safe agents does not guarantee a safe collection of agents."
  - Six failure modes for governed multi-agent systems: cascading reliability failures, inter-agent communication failures, monoculture collapse, conformity bias, deficient theory of mind, and mixed-motive dynamics.
  - Recommends staged testing with gradually increasing exposure. Evidence should converge from simulation, observational analysis, benchmarking and red teaming.
- *Relevance to ADIC:* a risk-identification frame for the MRM and ISO 42001 inventory. It covers system-level failures that the dossier's per-role materiality tiering misses. [Inference]

### E. Human reliance on AI advice (IC deliberation module)

**23. [Automation bias: a systematic review of frequency, effect mediators, and mitigators](https://consensus.app/papers/details/2402a10463325c1abecb7908253a55e5/?utm_source=claude_desktop)**
- Kate Goddard et al. · 2011 (record year; JAMIA) · 1,078 citations · DOI 10.1136/amiajnl-2011-000089
- *Finding:*
  - The review included 74 studies, from 13,821 retrieved.
  - Mediators: cognitive style, task experience, trust and confidence, workload, task complexity and time pressure.
  - Mitigators: training, emphasizing user accountability, the placement of advice, updated confidence levels, and providing information rather than recommendations.
- *Relevance to ADIC:* each mitigator maps onto IC-pack design. [Inference]
  - Show uncertainty and the lab's own error rates.
  - Present evidence before, or instead of, a recommendation.
  - Train IC members and record individual accountability.
  - The dossier cites NIST's "human-AI configuration" risk, but none of this evidence.

**24. [To Trust or to Think](https://consensus.app/papers/details/67a3fad12a305f21bfd17cbe33933b0a/?utm_source=claude_desktop)**
- Consensus lists "Maja Malaya et al." The author field appears truncated; the paper is widely cited as Buçinca, Malaya & Gajos (bibliographic knowledge, not verified here). · 2021 · *Proceedings of the ACM on Human-Computer Interaction* · 821 citations · DOI 10.1145/3449287
- *Finding:*
  - Explanations alone did not reduce overreliance.
  - In an experiment with 199 participants, three cognitive-forcing designs reduced it significantly. But users rated these designs least favourably.
  - The benefits were larger for people high in need for cognition.
- *Relevance to ADIC:* the IC's pre-commitment step is a cognitive-forcing function. Expect resistance and uneven benefit across members, so measure reliance rather than assume improvement. [Inference]

**25. [Human-AI Interactions in Public Sector Decision-Making: "Automation Bias" and "Selective Adherence" to Algorithmic Advice](https://consensus.app/papers/details/ffaaf4a09e5f5de1995f2c0f8b726e08/?utm_source=claude_desktop)**
- Saar Alon-Barkat et al. · 2021 (record year; DOI 10.1093/jopart/muac007, a JPART DOI prefix) · 387 citations
- *Finding:*
  - Three experiments (N = 605, 904 and 1,345) found no automation bias relative to equivalent human-expert advice.
  - They did find "selective adherence": people adopted advice more readily when it matched stereotypes. This appeared in study 2 but not among civil servants in study 3.
- *Relevance to ADIC:* the larger IC risk may be confirmation-driven, selective use of the lab's output rather than blind deference. The dossier's pre-commitment design is the right counter. Also log whether IC members' adoption of lab output correlates with their recorded priors. [Inference]

---

## 4. Missed-but-important papers: design implications

Numbers in brackets refer to §3 entries; § and G numbers refer to the dossier. All implications are **[Inference]** unless a figure is quoted from an abstract.

### 4.1 State variables (additions to dossier §6.3, lab state $S_t$)

| Variable | Definition | Source | Owner |
|---|---|---|---|
| $EA_{g,s}$ | Estimate/actual error distribution per group $g$ and strategy $s$: mean bias $b_{g,s}$ and dispersion $\sigma_{g,s}$, computed for underwritten→actual and for forecast→actual | [10]; Smith & Winkler (§2) | Belief-fusion engine. It feeds the per-group credibility weights called for in the context file §1A item 2. |
| $N^{\rm LLM}_t$, $N^{\rm prereg}_t$ | Trial counters split by origin: LLM-generated candidates versus human- or IC-pre-registered ones | [7], [11] | Meta-controller |
| `leak_canary` | Pass/fail log of planted look-ahead PolicySpecs, per engine and DSL release | [7] | MRM |
| `integrity_incidents` | Counts of: numbers without tool-call provenance (tool bypass); undisclosed synthetic data; method–code misalignment; unresolved citations | [2], [3], [6] | Auditor; G6 |
| $\rho^{\rm agents}_t$ and the recommendation mix | Mean pairwise correlation of agents' recommendations, and their SELL / HOLD / REFI / LEVER mix compared with the optimizer's | Song (§2); Ross et al. (§2); [Apte 2026](https://consensus.app/papers/details/db74d9e2c2ff5bf2826e771264c6c1fc/?utm_source=claude_desktop) | Meta-controller dashboard |
| `memo_exposure` | For every LLM-derived quantity: data frequency, aggregation level, model ID, and whether it falls inside the model's training window | [12], [13]; Lopez-Lira et al. and Gao et al. (§2) | Data and provenance plane |
| `replicate_dispersion` | Spread of results across $k$ independent ideation replicates per contract | [Ahmed et al. 2026](https://consensus.app/papers/details/91f8b2708e5955c7adefe3ce851db34f/?utm_source=claude_desktop): results "varied across multiple runs of the same framework with the same prompt" | Planner |
| `reliance` | IC reliance metrics. Overreliance: agreeing with the lab when it later proved wrong. Underreliance: overriding it when it proved right. Also: how far each member moved from their pre-commitment | [23]–[25]; [Kokje et al. 2026](https://consensus.app/papers/details/189332eb9c72506d9c81d4fcc8c3de0e/?utm_source=claude_desktop) | IC secretariat; decision log |

### 4.2 Models

1. **Bayesian estimate/actual shrinkage** ([10]; Smith & Winkler, §2).
   - For group forecasts: $\tilde\mu_{g,s}=\mu_0+\kappa_{g,s}\,(\hat\mu_{g,s}-b_{g,s}-\mu_0)$, with $\kappa_{g,s}=\tau^2/(\tau^2+\sigma^2_{g,s})$.
   - Apply it before ranking SELL / HOLD / REFINANCE / LEVER proposals.
   - Apply the same shrinkage to search-set fitness $\hat F_i$ before it appears in any memo.
2. **Decaying-memory online FDR as the alpha ledger.** Use GAI++ / mem-FDR [11] in place of hard-reset α-investing.
   - Prior weights distinguish IC-sponsored hypotheses from brute-search candidates.
   - Successive contracts reuse overlapping scenario libraries, so their tests are dependent. Consider e-value variants built for dependence ([e-GAI](https://consensus.app/papers/details/082b2704c7745690898a153cdb93adfb/?utm_source=claude_desktop)).
3. **Double-bootstrap hurdles** [9]. Calibrate the sealed-test thresholds to a target FDR and to a miss ratio, rather than to α alone.
4. **Mandatory factor and style attribution** [15], [16]. Run every candidate improvement through the α* engine against the funding basket, and report the beta, style and residual split.
5. **Complexity haircut.** Model the expected live/backtest ratio as a decreasing function of PolicySpec size (nodes plus parameters).
   - Priors: [8]; [Wiecki et al. 2016](https://consensus.app/papers/details/cbf1b88914f55668987babb345905af4/?utm_source=claude_desktop), where backtest Sharpe ratios gave R² < 0.025 for out-of-sample performance across 888 algorithms.
6. **Default LLM aggregator: independent samples plus majority vote.**
   - Run debate only as a budget-matched ablation ([19]; [Zhang et al. 2025](https://consensus.app/papers/details/f3cacd95264f5554a4240f3ff3e7cca2/?utm_source=claude_desktop); [Ferreira et al. 2026](https://consensus.app/papers/details/6d29e590763b5fb5b9b16a9914be4fc3/?utm_source=claude_desktop)).
   - Use heterogeneous models where possible [20].
7. **Point-in-time language models** for any back-tested LLM-derived signal ([14]; [Sarkar et al. 2024](https://consensus.app/papers/details/28dd2530f4445ae399fac998e2b02d73/?utm_source=claude_desktop); [Kelly et al. 2026](https://consensus.app/papers/details/547ec5e033be596caf6a77e5779d62ff/?utm_source=claude_desktop)).

### 4.3 Parameters and calibration priors (literature values, not ADIC data)

| Quantity | Literature value | Source | Use in ADIC |
|---|---|---|---|
| Backtest→live Sharpe deterioration | Median 73%; complex strategies more than 30pp worse than simple ones | [8] | Prior for haircutting search-set improvements |
| Backtest Sharpe as a predictor of out-of-sample performance | R² < 0.025 (888 algorithms) | Wiecki et al. 2016 | Never rank on in-sample Sharpe |
| Leaky oracle that passes DSR + PBO | Sharpe 35 | [7] | G2 must catch 100% of canaries |
| LLM strategies surviving honest evaluation | 0 (two models, ≤100 candidates, five runs) | [7] | Prior that "not established" is the likely outcome. Contrast: [Clayman et al. 2026](https://consensus.app/papers/details/8433fbef9ccf5e75a31876ba971ae13c/?utm_source=claude_desktop) report 7 of 8 LLM strategies with positive mean Sharpe out of sample. |
| Hallucinated references; score verification; method–code alignment | Up to 21%; as low as 42%; 20–80% | [2] | Baselines for G6 seeded-fault drills; targets 0 / 100% / 100% |
| Integrity-problem rate; undisclosed fabrication | 34.2%; 20.6% → 3.2% once completion pressure is removed | [3] | Drill criterion: zero undisclosed synthesis |
| Accepted automated reviews containing fabricated or unsupported claims | 59% | [4] | LLM review is never sufficient alone |
| Effect of one persuasive adversarial agent | Accuracy down 10–40%; consensus on incorrect answers up "more than 30%" | [21] | Target for the red-team drill |
| Retrieval overlap 0→1 | Action correlation 0.04→0.41 | Song (§2) | Alert band for $\rho^{\rm agents}$; the threshold is ADIC's choice |
| Shared vs diversified prompts; risk-guardrail prompts | Concentration gap 0.50–0.63; HOLD rate +47.6 to +53.2pp | [Apte 2026](https://consensus.app/papers/details/db74d9e2c2ff5bf2826e771264c6c1fc/?utm_source=claude_desktop) | Monitor LLM HOLD bias in the SELL / HOLD lens |
| Tool-hallucination detector accuracy | Up to 86.4% | [6] | Complements the provenance rule; does not replace it |
| Debate vs self-consistency at matched budget | Ties or loses, at 1.6× wall-clock and 3.4× tokens (small models); +1.3pp for debate on MMLU-Pro/BBH | Ferreira et al. 2026; [Wunderlich et al. 2026](https://consensus.app/papers/details/8027f2009ae9533cb7e3133e19adbd8b/?utm_source=claude_desktop) | Default to voting; run debate only as an ablation |
| Independent audit of KOSMOS hypotheses against null models | 1 well supported, 1 uncertain, 1 false (of 3) | [Nusrat et al. 2025](https://consensus.app/papers/details/4de5d2fd2b955f9a8cbd60236b0ea486/?utm_source=claude_desktop) | Add a null-model baseline (random PolicySpecs) |

### 4.4 Constraints (additions to dossier §6.3 and §6.5)

1. **Provenance rule.** Every numeric claim must resolve to a tool-call record: `run_id`, tool name and input hash. Any value that appears in model text without a matching call is rejected at G6 ([6], [2]).
2. **Structural leakage defence.** G2 must reject 100% of planted look-ahead canaries in every engine or DSL release. PBO and DSR results are never accepted as evidence of no leakage [7].
3. **Data creation privilege.**
   - Agents cannot mint dataset handles.
   - Synthetic data come only from a generator tool that labels its output as synthetic.
   - "Data insufficient" is an admissible terminal state [3].
4. **LLM priors.** LLM-elicited quantitative views covering periods inside the model's training window are inadmissible as ViewSpecs, unless they come from point-in-time models. LLMs never supply low-frequency or index-level numbers ([12]–[14]).
5. **Independence.** Judges and the Auditor record their scores before seeing other agents' outputs. Decision-relevant aggregation uses no multi-round debate ([19]–[21]).
6. **Power and evidence length.** The AnalysisContract states the minimum detectable improvement on the sealed set and the test's power for it.
   - Every "not established" verdict is reported together with that power [9].
   - Required track length must scale with the number of trials ([Bailey et al. 2014](https://consensus.app/papers/details/578104e71df057ee9a03edf926b2950c/?utm_source=claude_desktop): "minimum backtest length").
7. **Named error criteria.** FWER (Holm) within a contract; mFDR or mem-FDR across contracts (§2 row [79]; [11]).

### 4.5 Objectives

1. **Meta-objective with an explicit miss cost** [9]:

   $$\max\ \mathbb E[F(\pi^\star)-F(\pi_0)]-\lambda_\$\,\$_T-\lambda_{\rm miss}\Pr(\text{missed improvement})$$

   subject to FWER ≤ α within a contract and mFDR ≤ α across contracts. This replaces the single constraint Pr(false promotion) ≤ α.
2. **Robust fitness with shrinkage and a complexity penalty** ([8], [10], Smith & Winkler):

   $$F'_\tau(\pi)=\kappa\,F_\tau(\pi)-\lambda_c\,C(\pi)$$

   where $C(\pi)$ is the PolicySpec's node count plus parameter count, and $\kappa$ comes from the estimate/actual shrinkage.
3. **Risk-first evaluation of LLM roles.** Evaluate roles on their risk profile first: hallucinated facts, stale data, prompt manipulation, plus a "safety budget". Point performance comes second ([Chen et al. 2025, *Standard Benchmarks Fail*](https://consensus.app/papers/details/31f2ed0ddd4052a894508d262be7ebae/?utm_source=claude_desktop)).

### 4.6 Agent, IC and organizational design

1. **Shadow IC by procedure, not persona.** Replace persona prompts ("you are the CRO") with role agents that run typed checklists for each ADIC unit ([18]; Ferreira et al. 2026, "persona tax"):

   | Unit | Checklist covers |
   |---|---|
   | PE | GP projections and look-through |
   | Secondaries | Hybrid book of fund LP stakes and direct deals; its secondary pricing feeds SELL |
   | Capital Solutions | NAV-loan and preferred-equity terms, which feed REFINANCE |
   | Co-investment | Deal models |
   | Public Markets | Redemption terms, gates and lock-ups |
   | Private Credit | Loss-adjusted yields |
   | Overlay | Strategy P&L |
   | Corporate Finance / Treasurer seat | Liquidity gate, contingency funding plan, collateral and distributions |
2. **Conflicted inputs.**
   - Secondaries and Capital Solutions quotes, and GP projections, enter belief fusion with credibility weights computed deterministically from estimate/actual track records.
   - LLMs must not apply "uniform trust", the bias of treating retrieved information as factual and all sources as equally informative ([TrustTrade 2026](https://consensus.app/papers/details/151fbb6ed5f65110b88e83f9c2fa7190/?utm_source=claude_desktop)).
   - Run persuasion red-team drills on these inputs [21].
3. **Aggregation.** Majority vote over independent, heterogeneous samples ([19], [20]). Keep the Auditor in a different model family.
4. **IC pack.**
   - Lead with evidence and juxtaposed thesis/antithesis. In [Pe et al. 2026](https://consensus.app/papers/details/7c04206aadd45df8a9832896706f6db8/?utm_source=claude_desktop), a juxtaposed "judicial" protocol had the lowest overreliance.
   - Show the lab's own error rates on every pack: judge κ, Auditor recall and translation pass^3 ([23]; [Kupfer et al. 2023](https://consensus.app/papers/details/62b3159c86cf5dd0991faa2dfbc30edf/?utm_source=claude_desktop): informing users about system errors raised verification).
   - Offer disaggregated drill-down. Kupfer et al. found that users spent less time at the most aggregated dashboard level, and recommend less aggregated data to reduce automation bias.
   - Keep pre-commitment, but expect it to trade overreliance for underreliance on correct advice (Kokje et al. 2026).
   - Track the `reliance` KPIs ([23]–[25]).
5. **Accountability and training.** Record individual accountability for IC decisions, and train members on the lab's failure modes [23].
6. **Review artifacts.** MRM and the Auditor review trace logs and PolicySpec code, not only the memo [1].
7. **Staged deployment with convergent evidence** [22]: synthetic → shadow → advisory → IC. This matches the dossier's runtime phases and adds exposure gates between them.
8. **Replicates and null baselines.**
   - Run $k \ge 3$ independent ideation replicates per contract; the value of $k$ is an inference.
   - Add a null distribution of random PolicySpecs to the Planner's baselines (Nusrat et al. 2025; Ahmed et al. 2026; [Zhang et al. 2024](https://consensus.app/papers/details/24181e831d5451bea65d72005500125b/?utm_source=claude_desktop)). Zhang et al. note that "inconsistent benchmark settings, inadequate baselines" had left the true progress of LLM-based evolutionary program search "inadequately justified". Their own benchmark (nine LLMs, five independent runs) then supports the importance of the evolutionary-search component. The lesson for ADIC is to require baselines and repeated runs, not that the method fails.
9. **Hypothesis registry.** Record every AI-generated hypothesis before evaluation, including those never promoted. This follows a position paper's call for "a centralized preregistration repository for all AI-generated hypotheses" ([Bisht et al. 2026](https://consensus.app/papers/details/3b2035d8810156778904bf649f30b7d2/?utm_source=claude_desktop)).
10. **Budget routing.**
    - Keep the dossier's UCB1 scheduler across idea families.
    - Add an "accumulated improvement" stagnation signal ([AdaEvolve](https://consensus.app/papers/details/109d30a1e92f5494b03abde27d64af79/?utm_source=claude_desktop)).
    - Consider cheap-model exploration with handoff to a stronger model only if evaluations support it ([Relay, Don't Route](https://consensus.app/papers/details/67dfdd3c1c625d7bab51ce1708dca9d0/?utm_source=claude_desktop): "cheap models recover much of the early progress").

---

## 5. Papers that challenge the dossier's recommendations

1. **Statistical gates do not detect leakage.**
   - In [7], a leaky oracle with Sharpe 35 passes both the DSR and PBO tests.
   - The dossier already has the structural defence, a type-checked non-anticipativity rule (§2.4, G2).
   - Change: test that defence with canaries, and never present PBO or DSR as evidence that a policy has no leakage.
2. **LLM-guided policy search may yield little.** The dossier labels it "**Core**" (§3.1).
   - Evidence of low yield:
     - [7] rejected every LLM-discovered strategy.
     - [CodeScientist](https://consensus.app/papers/details/f77960457d705ef283999c7072f455f4/?utm_source=claude_desktop) reports 19 discoveries, only 6 judged "at least minimally sound and incrementally novel".
     - The KOSMOS audit (Nusrat et al. 2025) found 1 false hypothesis out of 3.
     - Related caution, not evidence of low yield: Zhang et al. (2024) say that inconsistent benchmarks and weak baselines had left earlier progress claims "inadequately justified". Their rigorous re-benchmark supports evolutionary search itself.
   - Counter-evidence: Clayman et al. (2026) report 7 of 8 LLM-generated strategies with positive mean out-of-sample Sharpe, and a significant portfolio-level gain (p = 0.042).
   - Change: budget for "not established" as the most likely early outcome, and evaluate human-authored policies in the same evaluator. [Inference]
3. **The stacked gates may lack power.**
   - [9]: current methods lack power to detect true outperformance.
   - [MinervaScore (Santoni et al. 2026)](https://consensus.app/papers/details/ae3db8a4c52f57439ee935d7b09970e2/?utm_source=claude_desktop) combines DSR, PBO, SPA and minimum track length. In a pre-registered real-market test it showed no significant forward relationship (Spearman ρ = 0.013, p = 0.40). The authors describe it as a reporting layer, not evidence of predictability.
   - Gates certify statistical support, not future value. Add a power analysis and a minimum detectable effect (§4.4 item 6).
4. **Orchestration versus base model: the evidence is mixed.**
   - [5]: failure patterns persist across harness–model combinations, which points to the model.
   - Secondary coverage of *The Agentic Scientist* says model choice mattered more than harness (unverified).
   - [Qian et al. 2025](https://consensus.app/papers/details/5855f179e3495d7aa16f17c28fe3be79/?utm_source=claude_desktop): in live trading, "model backbones contribute less to outcome variation" than agent frameworks.
   - Do not credit orchestration alone for reliability. Pin models and treat upgrades as re-validation events, as the dossier already does (§6.9).
5. **Debate and personas: mixed evidence.**
   - *Against:* [19]; Zhang et al. 2025; Ferreira et al. 2026, where persona prompting reduced accuracy and mixed-model teams lost to majority votes over their own rosters.
   - *For:* Wunderlich et al. 2026, where at equal compute debate and mixture-of-agents beat self-consistency by 1.3 and 2.7 percentage points respectively. Apte 2026, where persona-diversified prompts reduced action concentration.
   - The dossier's rule "IC preparation only, never the decision" holds either way.
   - Its shadow-IC "role agents (CRO, liquidity, PE, overlay)" (§6.7 item 3) should be procedure-defined. Persona diversity should be judged on its herding-versus-accuracy trade-off.
6. **Explanations and provenance may not reduce reliance.**
   - [Vered et al. 2023](https://consensus.app/papers/details/d7418b907b6f505abc4ee25af157242d/?utm_source=claude_desktop): explanations "did not reduce this aspect of automation bias and sometimes increased it".
   - [Romeo et al. 2025](https://consensus.app/papers/details/c15457f004325789909055df8acbdd9d/?utm_source=claude_desktop), a PRISMA review of 35 studies: explanations "are often insufficient to improve decision accuracy or mitigate AB", and "user engagement emerges as the most feasible and impactful point of intervention".
   - [Vasconcelos et al. 2022](https://consensus.app/papers/details/5759c2c93f8e59a3a6f1313c1b768659/?utm_source=claude_desktop): explanations help only when they lower the cost of verification.
   - The claim-linked memo (G6) is necessary for audit, but it is not a reliance control on its own.
7. **Pre-commitment is not free.**
   - Kokje et al. 2026: non-concurrent advice reduced overreliance at the cost of underreliance on correct advice.
   - Pe et al. 2026: an "adjunct" protocol that required an unaided decision first was outperformed by juxtaposed explanations. No AI-assisted condition beat the unaided baseline on accuracy.
   - These are clinical and face-matching tasks, so transfer to an IC is inference.
8. **"Post-cutoff only" is stricter than necessary for some tasks.**
   - [14] found look-ahead bias modest with chronologically consistent models.
   - [Glasserman et al. 2023](https://consensus.app/papers/details/beaf2b42d3315951a7601fd1c1ee7c5a/?utm_source=claude_desktop) found that, in-sample, anonymized headlines outperformed, "indicating that the distraction effect has a greater impact than look-ahead bias".
   - But [13] shows that ADIC's low-frequency, index-level profile is the worst case, so the dossier's rule stands for ADIC. Point-in-time models are the alternative if back-tests are unavoidable.
9. **Token scaling does not generalize.**
   - Dossier §3.4 cites "token usage explains 80% of performance variance" (BrowseComp).
   - [4] found that neither token budget nor compute predicts the quality of research output.
   - This agrees with the dossier's conclusion that tokens are not the scarce resource. The 80% figure should not be generalized beyond browsing tasks.
10. **Automation bias may not be the IC's main failure mode.**
    - [25] found no automation bias relative to human-expert advice, but did find selective adherence.
    - Pre-commitment logs should test for confirmation-driven adoption, not only deference.

---

## 6. Verbatim usage message

The last usage message in the Consensus results, copied verbatim:

> 14 searches left this month; resets to 500 on November 1st.

The counter fell from 47 to 14 during this session; three agents share it.

---

## 7. Scope notes

**WebSearch confirmations (2 queries)**
- ***The Agentic Scientist*** (arXiv 2610.18933): the authors and Sakana AI affiliation are confirmed by secondary coverage. The arXiv page itself did not appear in results. Sources: [AlphaSignal](https://alphasignal.ai/news/sakana-ai-s-agentic-scientist-turns-coding-agents-into-open-source-researchers); [AI Weekly](https://aiweekly.co/alerts/agentic-scientist-pipeline-co-authored-an-alife-2026-paper); [ExplainX](https://www.explainx.ai/blog/sakana-agentic-scientist-v3-ai-scientist-v3-coding-agents-open-source-2026).
- **Song (2026)**: Zichen Song, ICLR 2026, spotlight at the 2nd Workshop on Advances in Financial AI. Action correlation 0.04→0.41. Source: [ICLR virtual page](https://www.iclr.cc/virtual/2026/10016534).

**Dossier academic works not checked here.** These were left out because of the shared Consensus quota and should be checked in a later pass.
- **Discovery systems:** ShinkaEvolve [10]; Agent Laboratory [12]; AI-Researcher [13]; data-to-paper [14]; R&D-Agent-Quant [17]; Si et al. [18], [19]; Dharna et al. [21].
- **Finance:** FinRobot [26]; AlphaAgents [27]; MarketSenseAI 2.0 [28]; Kim–Muhn–Nikolaev [32] (the companion verification file confirms its arXiv withdrawal); FinanceBench [35].
- **Security and LLM behaviour:** CaMeL [61]; Zheng [62]; Sharma [64]; Xiong [65].
- **Classical †:**
  - Harvey–Liu–Zhu [76]; White [77]; Hansen [78]; Hyperband [81]; Kim–Nelson [82]; Frazier–Powell–Dayanik [83]; Powell [84]; MAP-Elites [85]; Sha [86]; Schweiger et al. [87]; Stasser–Titus [88]; Klein [89]; IPCC guidance [90]; Landis–Koch [91]; Chen et al. [94].
  - Hyperband [81] and Powell [84] are the most load-bearing of these. They underpin successive halving and the policy-class taxonomy.

**Other relevant records not annotated**
- *Agentic-science critiques and surveys:*
  - [Why LLMs Aren't Scientists Yet (Trehan et al. 2026)](https://consensus.app/papers/details/1e8e11d81a005c129507e88f7f95cdbd/?utm_source=claude_desktop): six failure modes, including "implementation drift" and "overexcitement".
  - [ResearchGym (Garikaparthi et al. 2026)](https://consensus.app/papers/details/275e0022ec8d5c7c9fbb88a50cef7b10/?utm_source=claude_desktop): a GPT-5 agent beat baselines in 1 of 15 evaluations.
  - [AutoResearch AI survey (Tie et al. 2026)](https://consensus.app/papers/details/3df600fdbcf15029b8a6b6182403d333/?utm_source=claude_desktop): autonomy is "more credible in structured, executable, and rapidly verifiable settings" and limited in "delayed … institutionally accountable contexts".
  - [AI for Auto-Research roadmap (Kong et al. 2026)](https://consensus.app/papers/details/5762dbf71f305e6e890ea12631b8e323/?utm_source=claude_desktop).
  - [SAGE (Ma et al. 2026)](https://consensus.app/papers/details/47cbc52c629b537eab931afb2dcce276/?utm_source=claude_desktop): grounded reporting that redacts hallucinated numbers.
  - [Agrawal et al. 2026](https://consensus.app/papers/details/7b0cb51bc6f35bc59049f389e14953ab/?utm_source=claude_desktop): none of eight frameworks completed a full research cycle.
  - [SwarmResearch](https://consensus.app/papers/details/72cfbd2ee9b9516e920de5a66fec6747/?utm_source=claude_desktop): an orchestrator steering a population of search agents.
- *Tool use and verification:*
  - [CRITIC](https://consensus.app/papers/details/8d59cf15c10a5fecae653e92d6ebbd39/?utm_source=claude_desktop): emphasizes "the crucial importance of external feedback".
  - [ReAct](https://consensus.app/papers/details/925849938da857b9a1538f2a0a5f652f/?utm_source=claude_desktop).
  - [VeriAct-Agent](https://consensus.app/papers/details/865a3c912fbe589486120a1349aa7759/?utm_source=claude_desktop).
  - [Relign](https://consensus.app/papers/details/fea634fc5cb15dc790bc72020a19201a/?utm_source=claude_desktop): lets the agent defer or seek clarification instead of calling a tool.
  - [Huo et al. 2023](https://consensus.app/papers/details/b73d06dfc1cc54bf876a85ead4d75e26/?utm_source=claude_desktop): self-verification can reduce hallucinations but "can not entirely eliminate them".
- *Finance contamination:*
  - [Fake Date Tests](https://consensus.app/papers/details/a3878798e9ab5dcc9d84042918c21daf/?utm_source=claude_desktop).
  - [DatedGPT](https://consensus.app/papers/details/7d03105ee8a45b12935fb8fa22ff6652/?utm_source=claude_desktop).
  - [MemGuard-Alpha negative results](https://consensus.app/papers/details/3fc1e600fa8e501d95af764305dc165c/?utm_source=claude_desktop).
  - [Nguyen 2024, anchoring in LLM forecasts](https://consensus.app/papers/details/fe20179b075f59b3b14c7a0e3600f35b/?utm_source=claude_desktop): relevant to how ViewSpecs are elicited.
  - [Romanko et al. 2025](https://consensus.app/papers/details/ba0d80dd41815b18a927c2ec0900b608/?utm_source=claude_desktop): LLM stock selection improves when combined with traditional optimization.
- *Systemic and herding:*
  - [Social Networks of LLM Agents](https://consensus.app/papers/details/abf291ea69ac5d00968e8568dfc04630/?utm_source=claude_desktop).
  - [Lopez-Lira 2025, *Can LLMs Trade?*](https://consensus.app/papers/details/b894705b527a54edac8e989636ba1626/?utm_source=claude_desktop): shows "how prompts can generate correlated behaviors".
- *Sequential testing:*
  - [SAFFRON](https://consensus.app/papers/details/ac54bf8f3c3057a688f11c6670fb4110/?utm_source=claude_desktop).
  - [Harvey et al. 2015, *Backtesting*](https://consensus.app/papers/details/26c79e6752075f64842d5bd2e1a67f72/?utm_source=claude_desktop): a Sharpe-ratio haircut for multiple testing (JPM).
  - [Optimizer's Information Criterion](https://consensus.app/papers/details/9c1bc1ffa2de5c938222027fed44a6f4/?utm_source=claude_desktop).
- *Human-AI:*
  - [Klingbeil et al. 2024](https://consensus.app/papers/details/5ef5f61d268d52799dc5a8e348f8b5fa/?utm_source=claude_desktop): the mere AI label caused overreliance.
  - [Horowitz et al. 2023](https://consensus.app/papers/details/19fa9eb3317a53e4a686ef5d3f93200b/?utm_source=claude_desktop): a preregistered experiment with 9,000 adults; automation bias varies non-monotonically with AI background knowledge.

**Preprint and recency flags.**
- 2026 arXiv preprints with few or no citations: [2]–[7], [15], [17], [18], plus most of the §5 counter-evidence.
- [21] (*Scientific Reports*) and [12] (*JAR*) are 2026 journal articles.
- Treat preprints as design input, not settled evidence.

**Consensus queries (13, in order)**
1. The Agentic Scientist: Orchestrating Coding Agents for Automated Scientific Co-Discovery *(look-up; seed 1 folded in)*
2. evolutionary program search with large language models *(seed 5)*
3. LLM multi-agent financial trading framework *(seed 2)*
4. memorization and lookahead bias of large language models in financial forecasting backtests *(refinement)*
5. evaluating automated AI scientist systems for autonomous research: failures and reliability *(seed 3, refined)*
6. Can LLM-based financial investing strategies outperform the market in long run *(look-up)*
7. probability of backtest overfitting and the deflated Sharpe ratio *(look-up)*
8. multi-agent debate versus self-consistency large language models benchmark comparison *(refinement)*
9. LLM tool use hallucination verification and self-correction with external tools *(seed 4, refined)*
10. information homogenization herding and correlated behavior in LLM agent markets systemic risk *(refinement and look-up)*
11. Kosmos AI scientist autonomous data-driven discovery with structured world model *(look-up)*
12. automation bias and overreliance on AI advice in human decision making: mitigation with cognitive forcing and explanations *(refinement)*
13. The optimizer's curse: skepticism and postdecision surprise in decision analysis; alpha-investing sequential control of expected false discoveries *(look-up)*
