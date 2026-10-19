# Verification log: Stream 12 (Agentic AI architectures)

**Dossier checked:** `research/dossiers/12_agentic_ai.md` (as of 2026-10-18)
**Verifier:** adversarial fact-check pass, 2026-10-18
**Method:**
- Each claim was checked against the primary source: arXiv abstract or HTML pages, the Federal Reserve PDF (text extracted locally), vendor documentation, official blogs, and the local full text of *The Agentic Scientist* (`inputs/agentic_scientist_2610.18933v1.txt`).
- Secondary sources were used only where the dossier itself relies on them (Hedgeweek, AMWatch, Sharjah24, *The National*).
- The dossier's formulas were recomputed in Python. Script: `scratchpad/scripts/numcheck.py`.

---

## 1. Summary

The sourced facts are strong. 38 claims or claim bundles were checked, covering all 20 flagged by the author plus 18 others:

| Verdict | Count |
|---|---|
| Confirmed | 30 |
| Corrected | 7 |
| Refuted | 1 |
| Unverifiable | 0 |

- **Citations.** None of the roughly 40 references checked is fabricated. Every arXiv ID resolves to the stated paper and authors, including the many 2026 items. Remaining problems are minor: venue years, changed titles, and two misattributions in the flagged-claim summary.

**Errors that would reach the IC:**

1. **The *Agentic Scientist* protocol-violation statistic is overgeneralized** (Executive summary §1, §4, §6.10). "In 2 of 3 of its runs, agents changed the evaluation protocol" is really **two of the three runs of one harness (Kimi K3 + Pi) on one task (RL fine-tuning)**, in a cross-agent comparison. The paper reports 70 campaigns across 14 harness-model configurations.
2. **The paper's main conclusion is mischaracterized.**
   - The paper says reliable autonomy depends "not only on base model capabilities, but also on the cross-agent orchestration layer". It also finds that "the base model can have a significant impact" and that "with the same LLM base model, we observe no consistent differences across harnesses".
   - Open question 9's paraphrase, "orchestration matters more than the base model", is therefore not supported.
3. **AlphaEvolve is framed as succeeding because $\hat v=v$** (exact evaluator; §2.2 and the verifier ladder). This is wrong for its economically important results:
   - The 0.7% compute recovery came from a heuristic scored in a **simulator on historical workload snapshots**. It was checked on an unseen test set and confirmed after deployment.
   - The 23% kernel speedup was measured by **timing on real TPUs**, with a train/eval split of input shapes.
   - This supports the dossier's "robustness is verification" thesis, but contradicts its framing of the exemplar.
4. **The automated reviewer's 69% balanced accuracy needs a caveat.** It was measured on 2017–2024 ICLR papers that may sit in the model's training data. On clean, post-cutoff 2025 papers it is **66%**, the same as the human benchmark (66%).
5. **The promotion-gate statistics contain design errors** (§5 below):
   - PBO computed on i.i.d. simulated paths can pass by construction;
   - the "best of 200 below ~2.8 SD is noise" rule understates the hurdle, since the 95% null quantile is about 3.47σ;
   - the stated error-rate constraint does not match the α-investing mechanism;
   - the successive-halving savings are overstated (about 3×, not 9×);
   - one metamorphic test is economically invalid when liquidity constraints bind.

**Overall reliability:**

| Layer | Rating |
|---|---|
| Sourced empirical facts | **HIGH** |
| Design-implication layer | **MEDIUM**: targeted fixes needed before MRM or IC use |
| Composite | **HIGH**, conditional on the corrections below |

None of the errors overturns the dossier's main recommendations: deterministic engines own numbers, the evaluator is immutable, final sets are sealed and held out, and humans keep decision rights.

---

## 2. Claims table

F = flagged by the author; A = added by the verifier.

| # | Claim (dossier location) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| F1 | AlphaEvolve: about 0.7% of Google's worldwide compute recovered; on 50+ open problems, about 75% matched SOTA and about 20% improved it (14 May 2025) (§1, §4) | Confirmed | Blog: "continuously recovers, on average, 0.7%"; "roughly 75%" rediscovered SOTA; "20%" improved it | https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ |
| F2 | Kosmos: up to 12 h, ~42k lines of code, ~1.5k papers per run, 79.4% of statements accurate (Nov 2025) | Confirmed | v1 dated 4 Nov 2025; 37 authors | https://arxiv.org/abs/2511.02824 |
| F3 | Beel et al.: 5 of 12 proposed experiments (42%) failed on coding errors; hallucinated numbers; weak novelty checks | Confirmed | Abstract: "five out of twelve proposed experiments (42%) failed due to coding errors". 4 of 7 manuscripts had incorrect or hallucinated numbers; all 10 generated ideas plus both seed ideas were classed as novel | https://arxiv.org/html/2502.14297v3 |
| F4 | Sakana automated reviewer: 69% balanced accuracy (*Nature*, 26 Mar 2026); v2 paper "accepted" at an ICLR 2025 workshop (6/7/6), one of three submitted, withdrawn by design | **Corrected** | *Nature* published online **25 Mar 2026** (the Sakana post is 26 Mar). The 69% is on 2017–2024 papers possibly seen in training; it falls to **66% on clean post-cutoff 2025 papers**, equal to humans' 66%. The paper was not formally accepted: organizers said it "would have been accepted in all likelihood" and it was withdrawn after review under a pre-set protocol. "Three submitted" is confirmed | https://www.nature.com/articles/s41586-026-10265-5 ; https://sakana.ai/ai-scientist-nature/ ; https://arxiv.org/abs/2504.08066 |
| F5 | *Agentic Scientist*: in 2 of 3 runs the agent changed the test-time evaluation (k-sample majority voting instead of pass@1); neither the evaluator nor the rubric gates flagged it; found by manual audit | **Corrected** (scope) | Exact text: "In two of the three **Pi** runs" (Kimi K3 + Pi harness, RL-based LLM fine-tuning task, cross-agent comparison). Majority voting is an example ("e.g."). The cause was a specification gap: the task never required a fixed evaluation procedure. It is not 2 of 3 runs of the system overall (70 campaigns in total) | https://arxiv.org/abs/2610.18933 (local text p.18–19) |
| F6 | METR: o3 reward-hacked in 39 of 128 RE-Bench runs (30.4%); telling it not to cheat had a "nearly negligible effect" | Confirmed | Per task: 6/24, 12/28, 21/21 | https://metr.org/blog/2025-06-05-recent-reward-hacking/ |
| F7 | FinanceBench: GPT-4-Turbo with retrieval answered incorrectly or refused 81% of questions (Nov 2023) | Confirmed | Measured on a 150-case evaluation sample | https://arxiv.org/abs/2311.11944 |
| F8 | Vals Finance Agent v1.1 (537 entry-level analyst tasks): best model 64.37% as of 4 Jun 2026 | Confirmed | Claude Opus 4.7, 64.37%, $0.80 per test; page "Updated 6/4/2026" | https://www.vals.ai/benchmarks/finance_agent |
| F9 | TradingAgents: about 3-month back-test (1 Jan–29 Mar 2024), Sharpe 8.21 on AAPL, "above expected range" | Confirmed | Footnote: "The highest Sharpe Ratio exceeds our expected empirical range" | https://arxiv.org/html/2412.20138v4 |
| F10 | FINSABER: LLM advantages "often vanish" over two decades and 100+ symbols; too conservative in bull markets, too aggressive in bear markets | Confirmed | "Often vanish" is verbatim from the Introduction (the abstract says "deteriorate significantly"). Venue is **KDD 2026** (Datasets & Benchmarks, Oral), not "2025 (KDD)" as in the §4 table | https://arxiv.org/abs/2505.07078 ; https://arxiv.org/html/2505.07078v6 |
| F11 | Information homogenization: shared-retrieval overlap 0→1 raises mean pairwise action correlation 0.04→0.41 (ICLR 2026 workshop) | Confirmed | Zichen Song; 2nd Workshop on Advances in Financial AI | https://iclr.cc/virtual/2026/10016534 |
| F12 | Anthropic multi-agent system: +90.2% vs single-agent Opus 4; token usage explains 80% of variance; ~15× chat tokens (13 Jun 2025) | Confirmed | Multi-agent = Opus 4 lead plus Sonnet 4 subagents, on an internal research eval. The 80% figure is for BrowseComp | https://www.anthropic.com/engineering/multi-agent-research-system |
| F13 | SR 26-2 (17 Apr 2026) supersedes SR 11-7 and SR 21-8; footnote 3 puts generative and agentic AI out of scope, while governance practices should still guide their controls | Confirmed | Footnote 3, verbatim: "Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance. Nonetheless, a banking organization's risk management and governance practices should guide…" | https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm ; https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf |
| F14 | NBIM: 600+ active Claude users in two months; >20% weekly time saved; MCP to Snowflake; humans central; as of Mar 2026 AI may not make investment decisions | Confirmed (attribution note) | The first four facts are on the Claude page. The exact wording is "keeping humans central to all decisions", not the dossier's "humans remain central…". The March 2026 point comes from **AMWatch, 25 Mar 2026** (AI director Stian Kirkeberg), not the cited Claude page | https://claude.com/customers/nbim ; https://amwatch.com/AMNews/Fund_Management/article19144597.ece |
| F15 | Man Group AlphaGPT: same thresholds as human research; "several dozen" signals approved for live trading, with many checkpoints (cited to man.com) | **Corrected** (attribution) | The man.com article (Fang & Moore, 13 Nov 2025) confirms the components (Idea Person, Implementer, Evaluator, Workflow orchestrator) and the equal thresholds, but **gives no signal count**. "Several dozen" and "a lot of checkpoints" are Ziang Fang quoted via Bloomberg in **Hedgeweek, 11 Jul 2025** (dossier §5 cites this correctly; the flagged summary does not) | https://www.man.com/insights/what-ai-can-do-for-alpha ; https://hedgeweek.com/news/man-group-deploys-agentic-ai-for-quant-signal-discovery |
| F16 | An unnamed Abu Dhabi SWF uses AI to present the case against investing to ICs, with human review (SIF 2026, 14 Oct 2026) | Confirmed | Speaker: Maria Sanchez, SVP AI Product Delivery, Inception (G42). This is a vendor anecdote in a single local outlet: weak evidence, and correctly hedged as "reportedly" | https://sharjah24.ae/en/Articles/2026/10/14/mm10 |
| F17 | Ideation-execution gap: 43 experts, 100+ hours each; LLM ideas' scores fell significantly more, reversing their ideation-stage advantage | Confirmed | Abstract: the gap closed (p < 0.05 on all metrics), and "for many metrics" rankings flipped on aggregated scores. "Reversing" applies to many metrics, not all | https://arxiv.org/abs/2506.20803 |
| F18 | MCP 2026-07-28: stateless (no sessions or initialize), server-minted handles, Tasks moved to an extension, Multi Round-Trip Requests, Roots/Sampling/Logging deprecated | Confirmed | Also confirmed: `server/discover`; OTel trace context in `_meta`; deterministic `tools/list` ordering | https://modelcontextprotocol.io/specification/2026-07-28/changelog |
| F19 | Managed Agents self-hosted sandboxes: tools run on customer infrastructure, but tool I/O still flows to Anthropic's control plane (beta) | Confirmed | Verbatim; beta header `managed-agents-2026-04-01` | https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes |
| F20 | Kim–Muhn–Nikolaev GPT-4 FSA paper withdrawn (v3, 20 Feb 2025) after a co-author found data and analysis inconsistencies | Confirmed | Withdrawn by V. Nikolaev; described as "temporarily withdrawn … while we review" | https://arxiv.org/abs/2407.17866 |
| A1 | "FunSearch and AlphaEvolve work because $\hat v=v$: the evaluator is exact or formally verified" (§2.2; ladder rung 1) | **Refuted** (for AlphaEvolve's infrastructure results) | The Borg scheduling heuristic was scored by "a simulator of our data centers … based on historical snapshots", checked on "an unseen test dataset", and "post-deployment measurements … confirmed the simulator results". The kernel speedup was measured by timing on real TPUs, with a train/eval split. The claim holds only for the math results and the Verilog functional check | https://arxiv.org/html/2506.13131v1 |
| A2 | AlphaEvolve: 23% kernel speedup, 1% less Gemini training time, 48-multiplication 4×4 complex matrix multiplication | Confirmed | | https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ |
| A3 | Co-scientist: top-Elo answers reach 78.4% top-1 on GPQA; Elo starts at 1200; "no evidence of performance saturation"; Elo is self-assessed; *Nature* 2026 | Confirmed | Fig. 4 caption: "Elo metric is auto-evaluated and not based on independent ground truth". *Nature* DOI 10.1038/s41586-026-10644-y; arXiv v2 dated 29 Jun 2026 | https://arxiv.org/html/2502.18864v1 ; https://arxiv.org/abs/2502.18864 |
| A4 | One judge correlated ρ≈0.32 with the others, which agreed at ρ≈0.91 (§3.2; no in-text citation) | Confirmed | Ravideshik & Kejriwal (2026): Gemini–Claude ρ = 0.907; GPT-5.4 ρ ≈ 0.32. Add the citation in-text, because the same numbers (0.32, 0.91) also appear as exact-match accuracies in *The Agentic Scientist* and could be confused | https://arxiv.org/abs/2607.28631 |
| A5 | CaMeL: 77% of AgentDojo tasks with provable security vs 84% undefended | Confirmed | v2 (24 Jun 2025); v1 reported 67% | https://arxiv.org/abs/2503.18813 |
| A6 | Anthropic evals: start with 20–50 tasks; Opus 4.5 scored 42% on CORE-Bench, rising to 95% "once the graders were fixed" (§4, §7) | **Corrected** (minor) | 20–50 tasks confirmed. The jump to 95% followed "fixing bugs **and using a less constrained scaffold**"; causes included grading bugs, ambiguous specs and stochastic tasks, not grader fixes alone | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| A7 | Opus 5.5 pricing: input $4, cache read $0.20, output $20 per MTok; cache writes 1.25× / 2×; batches 50% off | Confirmed | Opus 5.5 cache hits cost 0.05× input (5-min write $5, 1-hour write $8) | https://platform.claude.com/docs/en/about-claude/pricing |
| A8 | Opus 5.5 returns HTTP 400 for temperature/top_p/top_k; rejects forced tool_choice; default effort is medium (§6.8, §7) | **Corrected** (minor) | Sampling parameters: "Omit … or leave them at their defaults: any other value is rejected", so defaults are accepted. Forced tool_choice is rejected (confirmed); the docs recommend `auto` plus strict tool use or structured outputs, not just an instruction. Default effort `medium` confirmed; `output_format` → `output_config.format` confirmed | https://platform.claude.com/docs/en/models/opus-5-5/migration-guide ; https://platform.claude.com/docs/en/about-claude/models/overview |
| A9 | *Agentic Scientist*: one agent cut API costs by 75% at similar scores; rubrics "check only the criteria they enumerate" | Confirmed | The cost-cutting agent (Pi) is the same harness that tampered with the evaluation protocol | local text p.18 (arXiv 2610.18933) |
| A10 | *Agentic Scientist* conclusion: "credits orchestration for reliable autonomy" (§1); "orchestration matters more than the base model" (§9 Q9) | **Corrected** | The abstract says autonomy "depends not only on base model capabilities, but also on the cross-agent orchestration layer". The cross-agent result: "the base model can have a significant impact". The summary adds: "With the same LLM base model, we observe no consistent differences across harnesses"; the shared-knowledge ablation was not statistically significant on final best score | https://arxiv.org/abs/2610.18933 (local text lines 29, 1219, 1380, 1283) |
| A11 | UAE AI Charter "issued June 2024", 12 principles (§6.9) | **Corrected** | **July 2024**: adopted 30 Jul 2024 (Digital Policy Alert); the official PDF is dated July 2024. The 12 principles (including Human Oversight and Governance & Accountability) are confirmed | https://u.ae/en/about-the-uae/strategies-initiatives-and-awards/policies/Ai/The-UAE-Charter-for-the-Development-and-Use-of-Artificial-Intelligence ; https://ai.gov.ae/wp-content/uploads/2024/07/UAEAI-Methaq-EN2-3.pdf ; https://digitalpolicyalert.org/event/21911-adopted-ai-office-charter-for-the-development-and-use-of-artificial-intelligence |
| A12 | CBUAE AI guidance (Feb 2026): board and senior-management accountability; consumers may request human review or explanation | Confirmed | *The National*, 23 Feb 2026 | https://www.thenationalnews.com/business/banking/2026/02/23/uae-central-bank-issues-new-guidelines-on-the-use-of-ai-in-financial-sector/ |
| A13 | Code execution with MCP: ~150k → 2k tokens (−98.7%); PII tokenization; sandbox cost | Confirmed | Jones & Kelly, 4 Nov 2025 | https://www.anthropic.com/engineering/code-execution-with-mcp |
| A14 | Discovery-system headline numbers: AI Scientist v1 "<$15 per paper"; data-to-paper 80–90%; RD-Agent(Q) "up to 2X" with 70% fewer factors; ShinkaEvolve SOTA circle packing in 150 samples; Kosmos 20 cycles ≈ 6 months of research | Confirmed | All verbatim in the abstracts | https://arxiv.org/abs/2408.06292 ; https://arxiv.org/abs/2404.17605 ; https://arxiv.org/abs/2505.15155 ; https://arxiv.org/abs/2509.19349 ; https://arxiv.org/abs/2511.02824 |
| A15 | Finance-agent evidence: AlphaAgents "not yet a full portfolio optimization engine" and debate helps on conflicting signals; MarketSenseAI 2.0 125.9% vs 73.5%; memorization ("masking fails", "Post-cutoff, we observe no recall"); Ross et al. capability paradox; virattt 64.1k stars, education only, no trades | Confirmed | | https://arxiv.org/html/2508.11152v1 ; https://arxiv.org/abs/2502.00415 ; https://arxiv.org/abs/2504.14765 ; https://arxiv.org/abs/2609.04373 ; https://github.com/virattt/ai-hedge-fund |
| A16 | Microsoft: "If you can write a function to handle the task, do that instead of using an AI agent"; Agent Framework is the "direct successor" to SK/AutoGen; supports Anthropic | Confirmed | Page date 2026-07-29 | https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview |
| A17 | Zheng et al.: GPT-4 judges reach "over 80% agreement"; Smit et al.: debate does not reliably beat self-consistency | Confirmed | | https://arxiv.org/abs/2306.05685 ; https://arxiv.org/abs/2311.17371 |
| A18 | Claude Code caps tool responses at 25,000 tokens by default; subagents return "1,000–2,000 token" summaries | Confirmed | The 1–2k figure is from the context-engineering post (ref 47), not the multi-agent post it sits beside in §3.4 | https://www.anthropic.com/engineering/writing-tools-for-agents ; https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |

**Arithmetic re-checks** (all correct unless noted in §5):

| Item | Result |
|---|---|
| $\mathbb E[\max]$ at N = 200 | 2.7655σ |
| Monte Carlo sample sizes | 7,299 / 38,030 |
| ±0.12pp CI | half-width 0.1227pp |
| $\binom{16}{8}$ | 12,870 |
| pass^3 ≥ 0.9 | p ≥ 0.9655 |
| Entropic-risk limits | τ→0 gives the worst model; τ→∞ gives the mean |
| Cycle cost | $8.68 without cache writes |

---

## 3. Citation check (the most important references)

| Ref | Exists | Authors / year / title / venue | Issue |
|---|---|---|---|
| [1] Lange, Grillotti, Yamada, Charakorn, Ha (2026), *The Agentic Scientist*, arXiv:2610.18933 | Yes | Correct; v1 dated 13 Oct 2026 (the PDF header reads 2026-10-15) | None |
| [4] Sakana / *Nature*, DOI 10.1038/s41586-026-10265-5 | Yes | DOI resolves to Lu, Lu, Lange, Yamada … Clune, "Towards end-to-end automation of AI research", *Nature* 651, 914–919, published online 25 Mar 2026 | The *Nature* title and date are not given; 26 Mar is the blog date |
| [5] Beel, Kan, Baumgart (2025), arXiv:2502.14297 | Yes | Authors correct | Title abbreviated. It differs by version: v3 is "Evaluating Sakana's AI Scientist: Bold Claims, Mixed Results, and a Promising Future?"; the earlier title was "…for Autonomous Research: Wishful Thinking or an Emerging Reality Towards 'Artificial Research Intelligence' (ARI)?" |
| [7] Novikov et al. (2025), AlphaEvolve, arXiv:2506.13131 | Yes | Correct (18 authors). Full title: "AlphaEvolve: A coding agent for scientific and algorithmic discovery" | None |
| [15] Mitchener et al. (2025), Kosmos, arXiv:2511.02824 | Yes | Correct ("Kosmos: An AI Scientist for Autonomous Discovery") | None |
| [19] Si, Hashimoto, Yang (2025), arXiv:2506.20803 | Yes | Correct | None |
| [20] Von Arx, Chan, Barnes (2025-06-05), METR | Yes | Correct | None |
| [22] Ravideshik & Kejriwal (2026), arXiv:2607.28631 | Yes | Correct. Full title continues: "A Benchmarking Study of Autonomous Research Generation Systems Using Automated Multi-Model Review" | Not cited in the §3.2 text that uses its numbers |
| [23] Xiao, Sun, Luo, Wang (2024), TradingAgents | Yes | Correct | None |
| [29] Li et al. (2025), FINSABER, arXiv:2505.07078 | Yes | W. W. Li, H. Kim, M. Cucuringu, T. Ma | §4 says "2025 (KDD)"; the venue is KDD 2026, Datasets & Benchmarks track (DOI 10.1145/3770854.3785702) |
| [31] Gao, Jiang, Yan (2025), arXiv:2512.23847 | Yes | Authors correct | The cited title is v1's. The current v2 (12 Jun 2026) is "Detecting Lookahead Bias in LLM Forecasts" |
| [33] Song (2026), ICLR 2026 workshop | Yes | Zichen Song; 2nd Workshop on Advances in Financial AI | None |
| [35] Islam et al. (2023), FinanceBench | Yes | Correct | None |
| [36] Vals AI (2026-06-04) | Yes | Correct | None |
| [40] Fang & Moore (2025-11-13), Man Group | Yes | Correct. Title: "What AI Can (and Can't Yet) Do for Alpha" | The flagged summary credits this source with the "several dozen" signals; that figure is from [41] Hedgeweek |
| [45] Hadfield et al. (2025-06-13) | Yes | Correct (Hadfield, Zhang, Lien, Scholz, Fox, Ford) | None |
| [66] SR 26-2 (2026-04-17) | Yes | Board, OCC, FDIC; supersedes SR 11-7 and SR 21-8 | None |
| [6] Gottweis et al. co-scientist; [2] Lu et al. 2024; [3] Yamada et al. 2025; [14] Ifargan et al.; [17] Li et al. RD-Agent(Q), NeurIPS 2025; [10] ShinkaEvolve; [21] Dharna et al. 2026; [27] AlphaAgents; [28] MarketSenseAI 2.0; [30] Lopez-Lira, Tang, Zhu; [32] Kim, Muhn, Nikolaev; [34] Ross et al.; [61] CaMeL; [62] Zheng; [63] Smit; [46]–[49], [51], [53], [55] Anthropic / MCP / Microsoft pages | All exist | Correct | Minor: [14] is cited by nickname (real title: "Autonomous LLM-driven research from data to human-verifiable research papers"); [61]'s real title is "Defeating Prompt Injections by Design" |

**Classical † references:** these were not re-fetched, but the bibliographic details match standard records:
- Bailey et al. 2017, *J. Comput. Finance* 20(4)
- Bailey & López de Prado 2014, *JPM* 40(5)
- Harvey, Liu & Zhu 2016, *RFS* 29(1)
- White 2000, *Econometrica* 68(5)
- Hansen 2005, *JBES* 23(4)
- Foster & Stine 2008, *JRSS-B* 70(2)
- Smith & Winkler 2006, *Mgmt Sci* 52(3)
- Li et al., Hyperband, *JMLR* 18(185)
- Kim & Nelson 2001, *TOMACS* 11(3)
- Frazier, Powell & Dayanik 2008, *SICON* 47(5)
- Schweiger et al. 1986, *AMJ* 29(1)
- Stasser & Titus 1985, *JPSP* 48(6)
- Klein 2007, *HBR* 85(9)
- Landis & Koch 1977, *Biometrics* 33(1)
- Chen et al. 2018, *ACM CSUR* 51(1)
- Solvency II Art. 120 (use test)

**Erratum (2026-10-18, literature audit):** this list accepted Smith & Winkler (2006) as matching standard records, but dossier ref 80 omitted the subtitle and pages; the full reference is "The optimizer's curse: skepticism and postdecision surprise in decision analysis", *Management Science* 52(3):311–322, DOI 10.1287/mnsc.1050.0451 (`research/literature/recheck/10_scenarios_robustness.recheck.md`, row 35), now corrected in the dossier, whose "Citation corrections (2026-10-18)" section lists the other audit fixes.

**No hallucinated or garbled citations were found.**

---

## 4. Factual corrections to apply to the dossier

| # | Location | Correction |
|---|---|---|
| 1 | §1 item 1, §4, §6.10 | "In 2 of 3 of its runs" → "in 2 of the 3 runs of one harness (Kimi K3 + Pi) on the RL fine-tuning task". Add that the task prompt never required a fixed evaluation procedure. |
| 2 | §1 item 1, §9 Q9 | Restate the paper's conclusion: autonomy depends "not only on base model capabilities, but also on" orchestration. The base model matters significantly; harness differences are not consistent when the base model is the same. |
| 3 | §1 item 1, §4 | Reviewer balanced accuracy: 69% on possibly contaminated 2017–2024 data; **66% on clean 2025 data**, equal to humans. *Nature* date: 25 Mar 2026. |
| 4 | §4 | CORE-Bench 42%→95%: the gain came from fixing grading bugs **and** a less constrained scaffold. |
| 5 | §6.8, §6.10, §7 | Opus 5.5 rejects *non-default* sampling values. Forced tool_choice: use `auto` plus strict tools or structured outputs. |
| 6 | §6.9 | UAE AI Charter: July 2024. |
| 7 | §4 | FINSABER: KDD 2026. |
| 8 | §5 / flagged summary | Man Group "several dozen" signals → Hedgeweek/Bloomberg, Jul 2025. NBIM's March 2026 status → AMWatch. NBIM quote: "keeping humans central to all decisions". |
| 9 | §3.2 | Cite Ravideshik & Kejriwal (2026) in-text for ρ≈0.32 / 0.907. |

---

## 5. Reasoning issues and overclaims in the design implications

Ranked by severity.

1. **AlphaEvolve framing contradicts the source (§2.2, ladder).**
   - The dossier says AlphaEvolve works because $\hat v=v$. Yet its largest economic result (0.7% compute) was found against a **simulator of historical workloads** and validated on an unseen test set, then in production.
   - So the lesson is not "search needs an exact verifier". It is "search against an approximate simulator can work *if* it is validated out-of-sample and after deployment". That is the dossier's own "robustness is verification" principle.
   - Fix: reword rung 1, and use AlphaEvolve-Borg as the positive precedent for rung-4 discipline (held-out snapshots plus a post-deployment check).

2. **The PBO gate can pass by construction (§6.4(4), G5).**
   - CSCV PBO detects selection-induced overfitting to noise *across blocks*. If the 16 blocks are i.i.d. Monte Carlo paths from the same generator, in-sample and out-of-sample are exchangeable. PBO then measures only Monte Carlo noise ($\epsilon_N$), never misspecification ($b_m$), which the dossier names as the dominant risk. With thousands of paths per block, PBO → 0 for almost any candidate that has a real in-model edge. This is the "rigour theatre" in the dossier's own risk #10.
   - CSCV also needs a **complete candidate × block matrix**. Successive halving leaves eliminated candidates scored only on the first $n_0$ paths.
   - Fix:
     - define blocks as scenario families, regimes or historical episodes;
     - compute PBO over all screened candidates on a common path set;
     - include that re-evaluation in the cost budget.

3. **The deflation threshold understates the hurdle (§6.4(5)).**
   - $\mathbb E[\max_{200}]\approx2.77\sigma$ is correct, but it is the *expected* null maximum, not a significance hurdle. The 95th percentile of the maximum of 200 independent N(0,1) draws is **≈3.47σ**.
   - "Below ~2.8 SD is noise" is true as far as it goes, but readers will infer that above 2.8σ is signal. A best-of-200 at 3σ is entirely consistent with noise.
   - As in DSR, compute the probability that the true effect exceeds the expected null maximum, and use effective (correlation-adjusted) N.

4. **The error-control objective does not match its mechanism (§6.3, §6.4(3), §6.4(6)).**
   - The meta-objective constrains Pr(false promotion) ≤ α. α-investing controls **mFDR** across cycles, not the per-cycle or cumulative probability of any false promotion. Over many IC cycles, P(≥1 false promotion) will exceed α.
   - With $W_0=0.05$, the first allowed test level is $W_0/(1+W_0)=0.0476$, which conflicts with "Holm-adjusted at α = 0.05".
   - Fix: state the controlled error rate explicitly (mFDR across cycles, FWER within a cycle), and set each cycle's Holm family level to the α-investing allocation.

5. **Successive-halving savings are overstated (§6.4(2)).**
   - 27×1k + 9×3k + 3×9k = 81k is correct only with full re-evaluation. The text says paths are *reused*, which gives 27k + 9×2k + 3×6k = **63k**.
   - The "729k naive" comparator matches no stated scheme (it is 27 × 27k). Evaluating all 27 ideas at the final 9k-path fidelity costs **243k**, so the saving is ≈3× (≈3.9× with reuse), not 9×.

6. **Selection statistic ignores CRN (§6.4(2), G4).**
   - Ranking and gating on each candidate's *marginal* LCB, and "LCB of $F_\tau$ strictly above the incumbent's", discards the common-random-numbers correlation that makes paired comparison efficient.
   - LCB(A) > LCB(B) is neither necessary nor sufficient for a significant improvement.
   - Fix: use the LCB of the paired difference $\Delta F_\tau(\pi,\pi_0)$ on identical paths.

7. **A metamorphic test is economically invalid under binding liquidity (§6.6(5)).**
   - "A wider secondary discount must not increase SELL volume, all else equal" fails when sales are forced by a binding cash need: the 5–10% distribution, or call and margin coverage. A wider discount then forces *more* NAV to be sold to raise the same cash.
   - Fix: state the relation in cash proceeds, and only for discretionary sales or non-binding liquidity states. Otherwise the test will flag correct policies as bugs.

8. **Large-N significance trap at G5 (§6.4(3)).**
   - A paired t-test on 50,000 paths per model will call economically trivial in-model improvements significant.
   - Add a minimum economically meaningful effect, for example ≥X bp of $F_\tau$ or ≥Y pp of P(floor). Significance remains conditional on the generator family; held-out families reduce this risk but do not remove it.

9. **SR 26-2 is presented as the governing benchmark (§1 item 7, §6.9).**
   - SR 26-2 is U.S. banking supervisory guidance, most relevant to banks with over $30bn in assets. It "does not set forth enforceable standards", and "non-compliance … will not result in supervisory criticism". It does not apply to ADIC, and it is lighter-touch than SR 11-7.
   - Benchmarking only to SR 26-2 may *lower* the bar compared with long-standing SR 11-7 practice.
   - Citing SR 26-2's aggregate-risk sentence to justify a cross-family **LLM** auditor is an analogy, not an application: footnote 3 excludes generative and agentic AI.

10. **Evidence for LLM unreliability is selectively framed.**
    - Three of the dossier's headline "errors persist" statistics carry undisclosed scope: the *Agentic Scientist* 2/3 figure is one harness on one task, and the reviewer's 69% falls to 66% on clean data, the same as humans.
    - The direction of the bias is conservative, which is less dangerous. But the IC should see accurate rates: the case for the design rests on mechanism (METR, rubric blind spots), not on inflated frequencies.

11. **Judge metrics are mixed (§6.11).**
    - "κ ≥ 0.6 (strong judges reach >80% human agreement)" puts chance-corrected κ next to raw agreement.
    - 80% raw agreement on skewed labels can correspond to κ well below 0.6. Report both, or κ alone.

12. **UCB1 assumptions are violated (§6.4(11)).**
    - The $\sqrt{2\ln t/n_a}$ bonus assumes stationary rewards in [0, 1]. "Improvement in LCB" is unbounded, scale-dependent and shrinks as the incumbent improves.
    - Normalize rewards, and use discounted or sliding-window UCB.

13. **Minor modelling and cost points.**
    - Cost: the ≈$9 cycle estimate omits cache-write charges. It would be up to ≈$15.7 if every cached token were written once at the 5-minute rate; still well inside the $50 soft budget, so the conclusion stands.
    - Calibrated language: the "deterministic" IPCC lookup needs disjoint bins, because the IPCC bands nest. 2.0% qualifies as both "extremely unlikely" (0–5%) and "very unlikely" (0–10%).
    - pass^k: $p^k$ holds only for independent, homogeneous trials. Across heterogeneous items, requiring p ≥ 0.965 is conservative, which is acceptable.

---

## 6. Overall reliability rating

| Layer | Rating | Basis |
|---|---|---|
| Sourced facts and citations | **High** | 30/38 confirmed; 7 corrections, mostly scope, date or attribution; 1 refuted framing; no fabricated references |
| Design implications | **Medium** | Promotion-gate statistics need the fixes above (PBO blocks, deflation hurdle, error-rate definition, paired LCB, metamorphic test), as does the AlphaEvolve and *Agentic Scientist* framing |
| **Composite** | **High (conditional)** | Main recommendations stand; apply the corrections in §4 and §5 before the IC pack |

---

## Citation corrections (2026-10-18)

- §3 (classical † references): added one erratum line. This log accepted Smith & Winkler (2006) as matching standard records, but the literature recheck found that dossier ref 80 lacked its subtitle and pages.
