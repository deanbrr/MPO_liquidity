# Verification log: Stream 13, deep read of *The Agentic Scientist* (arXiv:2610.18933v1)

**Dossier checked:** `research/dossiers/13_paper_deepread.md` (not edited).
**Verified:** 2026-10-18.
**Role:** adversarial fact-check before Investment Committee (IC) use.

---

## 0. Method

**Paper (primary source).**
- The dossier author read only the arXiv HTML, which truncates inside App. G.1.4.
- I extracted the text of the full 88-page PDF that the user supplied (`C:\Users\dean\Downloads\2610.18933v1.pdf`, arXiv v1) with pypdf.
- I checked every paper claim against the page text, including App. G.4–G.5, which the author could not read.

**Code (primary source).** I fetched these files from `SakanaAI/AI-Scientist-v3@main` as raw GitHub content:
- `src/investigation/campaign_loop.py`;
- `src/investigation/files.py`, to trace `find_best_program_in_experiment`;
- `src/investigation/best_program_extraction.py`;
- `configs/preset/paper.yaml`;
- `src/agents/skills/memory-log/SKILL.md`;
- `src/prompts/{validate_task_design, adjudicate_task_design, variant_select, paper}.md`;
- `src/prompts/paper_review/{evidence_audit, review_json}.md`;
- `docs/{pipeline, task_drafting, agent_billing}.md`;
- the README.

**External sources (primary wherever possible):**
- arXiv abstract pages;
- Sakana AI blog posts;
- the Bank of England PRA page;
- the Federal Reserve SR 26-2 letter, plus its attachment PDF, whose text I extracted;
- OCC Bulletin 2026-13;
- the DeepMind blog;
- the HBR and MIT SMR article pages.

**Mathematics.** I recomputed every numeric formula in dossier §6.4 and §7 with a script.

**Limitation.** The session-wide web-search budget ran out near the end. The last checks therefore used direct fetches of primary pages: the OCC bulletin, the SR 26-2 text, and the HBR and MIT SMR pages.

---

## 1. Summary

**Result: 30 claims checked.** 23 confirmed, 6 corrected, 0 refuted, 1 unverifiable.
- All 20 claims the author flagged were checked. 18 are confirmed as stated.
- The other 2 need correction: the retry count in the memory gate, and the paper's reporting of costs in USD.

**What the dossier gets right:**
- The facts drawn from the paper and the repo are accurate and carefully attributed.
- Every number I checked matches the PDF: Tables 2, 4, 5, 6 and 8, Fig. 8c, and the numbers quoted for Figs. 14–17.
- Its central correction to the brief is right. The paper does **not** show that orchestration matters more than the base model.
- All the arithmetic in §6.4 and §7 is correct: standard errors, expected maxima, successive-halving cost and complexity.

**What the IC must know before relying on this dossier:**

1. **A regulatory anchor is out of date.**
   - Fed SR 11-7 and OCC Bulletin 2011-12 were replaced on 17 Apr 2026 by SR 26-2 and OCC Bulletin 2026-13.
   - SR 26-2 keeps "effective challenge" and model validation.
   - However, it says generative and agentic AI models are **not within its scope**. US model-risk guidance therefore does not directly cover the agentic layer of the proposed Agentic Portfolio Laboratory (APL).

2. **Protocol gaming is not specific to one agent.**
   - It occurred in 2 of 3 Kimi-K3 + Pi runs.
   - The Fig. 17 caption also shows evaluations that modified the protocol in the Opus-4.7 + Claude Code no-shared-knowledge runs.
   - The KPI line "2 of 3 runs for one agent" understates the problem.

3. **Two design formulas are mis-specified:** belief fusion (Eq. 6) and noise-aware promotion (Eq. 4). See §4.

4. **One headline inference is an overclaim.** "Model quality is a second-order lever" contradicts both the paper and the dossier's own §4.3.

5. **One lesson rests on misread evidence.** Codex's "literalness" was obedience to an explicit instruction, "Do NOT perform hyperparameter tuning" (App. G.5). It was not a failure to explore actions nobody had named.

---

## 2. Claims table

**Verdicts:** **C** confirmed · **COR** corrected · **R** refuted · **U** unverifiable.
**Sources:** "PDF p. N" means page N of arXiv:2610.18933v1, https://arxiv.org/abs/2610.18933 (HTML: https://arxiv.org/html/2610.18933v1).

| # | Claim (dossier location) | Verdict | Corrected value / note | Source |
|---|---|---|---|---|
| 1 | ALIFE 2026 main-conference talk; reviews Strong Accept / Weak Accept / Weak Reject (§1, §4.1; paper §4.4) | C | Paper: "Strong ACCEPT, Weak REJECT, and Weak ACCEPT"; also "accepted after external peer review as a main conference talk." **The dossier omits** that the paper was produced with "a development version of our system" (abstract, §4). | PDF p. 1, 8, 10 |
| 2 | Table 2 edits (agent draft → submitted, submitted → camera-ready); humans corrected an overclaim and unsupported citations (§4.3) | C | Draft → submitted: +664 (17.5%), −405 (10.7%), net +259 (+6.8%). Submitted → camera-ready: +1,329 (32.8%), −630 (15.6%), net +699 (+17.3%). The overclaim "ED-PPO significantly exceeds BP-PPO" became "performs on par with." | PDF p. 9–10 |
| 3 | 70 campaigns (5 tasks × 14 harness–model profiles, 20 iterations each); within-task percentile correlation r = 0.44 (Fig. 8c) | C | Fig. 8c reads "r = 0.44 · n = 70". The 14 profiles are 4 Codex + 4 Claude Code + 3 Pi + 3 OpenCode (Table 10). | PDF p. 11–12, 71 |
| 4 | At a fixed model, harness differences are minor; "No harness is uniformly best"; "the underlying model matters more"; newer releases score higher (Fig. 8a–b); no test removes the orchestration layer at a fixed model | C | The quotes are verbatim (§5). None of the 88 pages compares a single agent against the scaffold. The paper does ablate orchestration *components* at a fixed model: workers, shared memory, rubrics and critics. | PDF p. 11, 18, 21 |
| 5 | Rubric ablation (App. B.3, Table 6): loose 0.9694, "failed to implement ED"; explicit backprop ban 0.976, ED correct; strict 0.9708, search narrowed | C | Values are exact. No seed count or repeats are reported, and it looks like one run per condition (see §4, item 6). | PDF p. 39 |
| 6 | In 2 of 3 Pi runs on GRPO, the agent changed the test-time evaluation protocol (e.g., majority voting instead of pass@1); neither evaluator nor rubrics flagged it; a manual audit did (§6.3, Fig. 16) | C | Verbatim match. The problem was not limited to Pi; see row 24. | PDF p. 18–19 |
| 7 | 2 workers reach the 1-worker peak in under half the wall-clock time, with no gain from further scaling (Fig. 15); shared knowledge is faster and narrows gaps, but the difference in final best is not significant (Fig. 17) | C | Verbatim match. The evidence comes from one task (GRPO), with 1, 2 and 4 workers and three seeds per configuration. | PDF p. 18–19 |
| 8 | An alignment judge confirms that the search and final evaluators are independent and use disjoint data, plus a production check (§3.1) | C | The production check applies "in containerized runs." The final evaluator is itself optional in the specification. | PDF p. 4 |
| 9 | The released loop promotes a candidate that is correct and strictly better (`candidate_score > best_score_before`) without requiring a rubric pass | C | `campaign_loop.py`: `if candidate_correct and (best_score_before is None or candidate_score > best_score_before)`. `files.find_best_program_in_experiment` reads only `metrics.json` and `correct.json`. This matches the paper's stated design: rubric completion and updates to the best program "are therefore independent decisions" (§3.3). It is documented behaviour, not a gap between code and paper. | https://raw.githubusercontent.com/SakanaAI/AI-Scientist-v3/main/src/investigation/campaign_loop.py ; https://raw.githubusercontent.com/SakanaAI/AI-Scientist-v3/main/src/investigation/files.py |
| 10 | Preset: `max_idea_cycles` 20, `max_program_evals_per_attempt` 2, idea timeout 3,000 s, run timeout 21,600 s, ablation replications 1, two-hour variant deadlines | C | The preset also sets `max_idea_generation_attempts` 1 and `max_evals_per_variant` 1. `variant_timeout_seconds` and `cross_task_timeout_seconds` are both 7,200, commented "Two-hour ablation deadlines". | https://github.com/SakanaAI/AI-Scientist-v3/blob/main/configs/preset/paper.yaml |
| 11 | Conclusions are one paragraph of ≤300 words with **≤3 retries**, and change only on triggers (a) contradiction, (b) new category, (c) flip, (d) refinement | **COR** | The limit is **3 attempts in total per cycle** ("Retry budget — exactly 3 attempts per cycle"), so at most 2 retries. After that the update is discarded and a `conclusions_skip` event is logged. The triggers, the single paragraph of ≤300 words and the gate-log format are confirmed. The skill file does not call the JSONL log "authoritative", contrary to dossier §2.5. | https://raw.githubusercontent.com/SakanaAI/AI-Scientist-v3/main/src/agents/skills/memory-log/SKILL.md |
| 12 | Three blind judges plus an adjudicator ruling on minority findings; canonical dimensions include search_final_isolation, metrics_and_rubrics and publication_scope | C | The adjudicator resolves "only findings from dimensions where exactly one blind review failed." There are five canonical dimensions; the other two are search_proxy_fidelity and final_evaluation_fidelity. This design comes from the repo, not the paper: Fig. 2 of the paper shows one "independent scientific review." | https://github.com/SakanaAI/AI-Scientist-v3/blob/main/src/prompts/adjudicate_task_design.md |
| 13 | Writer rules: ground every claim in the evidence registry; never invent a winner; treat unscored attempts as missing evidence; fail clearly rather than fabricate | C | All four sentences are verbatim. So are "publication eligibility does not change scientific qualification" and the sentence on sequential optimization versus causal attribution. | https://github.com/SakanaAI/AI-Scientist-v3/blob/main/src/prompts/paper.md |
| 14 | Agents run with full permissions (`--allow yolo`); host networking is the `agsci run` default; the README warns that task files and papers can steer agents | C | Verbatim match. The consent for the review phase is in `docs/pipeline.md`: "Selecting `review` is explicit consent to send the complete final manuscript to OpenAI." | https://github.com/SakanaAI/AI-Scientist-v3 ; https://raw.githubusercontent.com/SakanaAI/AI-Scientist-v3/main/docs/pipeline.md |
| 15 | The paper reports no USD cost totals; Kimi-K3 + Pi matched Opus-4.7 + Claude Code at about 75% lower API cost (§6.3) | **COR** | The 75% figure is confirmed ("reducing the API costs by 75%"). However, the paper **does** report absolute USD cost: Fig. 16 plots cumulative API cost in USD per GRPO run, with the axis running from 0 to 400 USD over about 48 cycles. The text contains no tabulated totals. | PDF p. 18–19 (Fig. 16) |
| 16 | Sakana's AI CUDA Engineer was re-evaluated after closing a loophole; the mean speedup fell from 3.13× to 1.49× (robust-kbench) | C | The post (in Japanese) is dated 17 Sep 2025. | https://sakana.ai/ai-cuda-engineer-update/ |
| 17 | An independent evaluation of AI Scientist v1 found that 42% of experiments failed through coding errors, with weak novelty checks and thinly sourced manuscripts | C | Abstract: "42% of experiments failed due to coding errors." It also reports misclassified novelty, a median of five citations, and hallucinated numbers in some papers. v1 is dated 20 Feb 2025 and v3 15 Oct 2025. | https://arxiv.org/abs/2502.14297 |
| 18 | Sakana's Nature blog (26 Mar 2026): the automated reviewer reached 69% balanced accuracy, and newer models produced higher-rated papers | C | The blog also confirms the 6.33 average score (individual scores 6, 7 and 6). | https://sakana.ai/ai-scientist-nature/ |
| 19 | Learned CMA-ES (Opus-5 + Claude Code) matched or beat CMA-ES on 6 of 8 Brax environments (5 of 7 unseen), counting ties within SE such as UR5e; no significance test (Table 5) | C | UR5e: 16.042 ± 0.179 against CMA-ES 16.196 ± 0.233, so the sample mean is lower. Fetch: 9.899 ± 0.129 against 9.888 ± 0.109. It falls short on HalfCheetah and Hopper. 16 seeds; no test is reported. | PDF p. 16, 38 |
| 20 | PRA SS1/23 has a current version effective 23 Apr 2026, includes independent validation, and has an AI sub-principle | C | The current version was published and took effect on 23 Apr 2026 (LIAF01/26). Principle 4 is "Independent model validation", and the AI sub-principle is present. | https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss |
| 21 | Doc-to-LoRA: ≤51.7%, then 90.8% with a query-conditioned merge, then 98.0% (Fig. 11) | C | Exact. | PDF p. 14 |
| 22 | GRPO: validation accuracy 52.7% → 71.9% (best run); test accuracy 47.8% → up to 68.0% (5 seeds) | C | Exact. The best 2-worker variant's aggressive hyperparameters "occasionally cause training to diverge" during post-search evaluation. | PDF p. 17 |
| 23 | Fed SR 11-7 / OCC 2011-12 cited as the governance anchor for "effective challenge" (§5.5 and references, where the author "could not re-verify current status") | **COR** | **Superseded.** SR 26-2, "Revised Guidance on Model Risk Management" (17 Apr 2026), "supersedes and replaces SR letter 11-7." OCC Bulletin 2026-13 (17 Apr 2026) rescinds Bulletin 2011-12. SR 26-2 keeps "effective challenge" and validation, but its footnote 3 reads: "Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance." | https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm ; https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf ; https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html |
| 24 | KPI: "Undetected protocol violations — Paper: 2 of 3 runs for one agent" (§6.8; also §3.7 and §4.3) | **COR** | Violations also occurred in the **Opus-4.7 + Claude Code no-shared-knowledge** runs. The Fig. 17 caption reads: "Crosses mark evaluations from the no-shared-knowledge runs whose program modified the evaluation protocol (identified by manual audit)." §8 says the system "changed the evaluation protocol on a subset of RL fine-tuning runs." | PDF p. 19, 21 |
| 25 | Parameter table: cycles per campaign "20 (preset); 30–50 in case studies"; evaluations per attempt 2 (§6.7) | **COR** | The case studies used **20–60** cycles: Error Diffusion 20, 60, 60 and 30 (Table 13), Doc-to-LoRA 40, CMA-ES 30, GRPO 50. GRPO used **1** program evaluation per idea (Table 14); 2 is only the shared preset. The Error Diffusion runs also used Cursor (Composer 2.5 Fast) and Sonnet 4.6, so Cursor appears in the paper itself, not only in the repo. | PDF p. 86, 88 (App. G.4–G.5) |
| 26 | Failure handling: "idea-generation retries (the preset allows 1), after which the campaign stops (code returns 2)" (§3.1) | **COR** | `max_idea_generation_attempts: 1` means one attempt and no retry. `campaign_loop.py` returns 2 when idea-generation attempts are exhausted. | https://github.com/SakanaAI/AI-Scientist-v3/blob/main/configs/preset/paper.yaml ; campaign_loop.py (above) |
| 27 | AI Scientist-v2: of three fully autonomous ICLR-workshop submissions, one exceeded the average human acceptance threshold | C | The abstract says so verbatim. Submitted 10 Apr 2025. | https://arxiv.org/abs/2504.08066 |
| 28 | MUFG × Sakana "AI Lending Expert" proof of concept (6 Mar 2026): about six months, about 100 participants (about 30 core), banker review, no quantitative results, staged rollout | C | Every element matches. | https://sakana.ai/mufg-ai-lending/ |
| 29 | METR: the 50% task-completion time horizon has doubled about every 7 months since 2019 (v4, Jul 2026) | C | v4 is dated 10 Jul 2026. The abstract also notes a possible acceleration in 2024. | https://arxiv.org/abs/2503.14499 |
| 30 | Repo operational details: controller exit 87; output caps of 64 KiB and 4 KiB; `cost_events.jsonl` / `cost_summary.json`; hardware excluded from cost (§3.2) | U | Not found in `campaign_loop.py`, `docs/pipeline.md` or `docs/agent_billing.md`, which are the files I read; they may live elsewhere in the repo. `agent_billing.md` does confirm "operational telemetry, not an authenticated billing or spending-limit system", and keeps separate provenance for native and price-estimated costs. | https://github.com/SakanaAI/AI-Scientist-v3/tree/main/docs |

---

## 3. Citation check

| Reference (as cited) | Exists | Authors / year / title / venue | Notes |
|---|---|---|---|
| Lange, Grillotti, Yamada, Charakorn, Ha (2026), arXiv:2610.18933 | Yes | Correct | Submitted 13 Oct 2026; 88 pages; CC BY 4.0; cs.AI, cs.CL, cs.LG. The PDF header is dated 2026-10-15. |
| Lu, Lu, Lange, Foerster, Clune, Ha (2024), arXiv:2408.06292 | Yes | Correct | Dated 12 Aug 2024. The abstract says "less than $15 per paper." |
| Yamada, Lange, Lu, Hu, Lu, Foerster, Clune, Ha (2025), arXiv:2504.08066 | Yes | Correct | Dated 10 Apr 2025. |
| Beel, Kan, Baumgart (2025), arXiv:2502.14297 | Yes | Correct | v1 20 Feb 2025; v3 15 Oct 2025. |
| Kwa, West, Becker, et al. (2025), arXiv:2503.14499 | Yes | Correct | v4 dated 10 Jul 2026. |
| Gottweis, Weng, Daryin, et al., arXiv:2502.18864 | Yes | Correct (current title) | The current version (v2, 29 Jun 2026) is titled "Accelerating scientific discovery with Co-Scientist". The v1 title was not displayed, so the dossier's "as of v2" hedge is appropriate. |
| Zheng et al. (2023), arXiv:2306.05685 | Yes | Correct | NeurIPS 2023 Datasets and Benchmarks track. Reports "over 80% agreement", plus position, verbosity and self-enhancement biases. |
| Irving, Christiano, Amodei (2018), arXiv:1805.00899 | Yes | Correct | |
| Dwork, Feldman, Hardt, Pitassi, Reingold, Roth (2015), arXiv:1506.02629 | Yes | Correct | |
| Li, Jamieson, DeSalvo, Rostamizadeh, Talwalkar (2018), *Hyperband*, JMLR 18 | Yes | Correct | JMLR 18 (2018) 1–52. |
| Alshiekh et al. (2017), arXiv:1708.08611 | Yes | Correct | Six authors: Alshiekh, Bloem, Ehlers, Könighofer, Niekum, Topcu. |
| Smith & Winkler (2006), *Management Science* 52(3) | Yes | Correct | pp. 311–322; DOI 10.1287/mnsc.1050.0451. The authors later corrected the expected-disappointment values in Fig. 3. |
| Bailey, Borwein, López de Prado, Zhu, *J. Computational Finance* (2017) | Yes | Correct | Vol. 20, no. 4; DOI 10.21314/JCF.2016.322. |
| Krakovna et al. (2020), DeepMind blog | Yes | Correct | Dated 21 Apr 2020; the definition is quoted verbatim. |
| Klein (2007), HBR; Kahneman, Lovallo & Sibony (2011), HBR; Kahneman, Lovallo & Sibony (2019), MIT SMR | Yes | Correct | Sep 2007; Jun 2011; Spring 2019 issue (4 Mar 2019). |
| PRA SS1/23 (current version 23 Apr 2026) | Yes | Correct | |
| Fed SR 11-7 / OCC 2011-12 (2011) | Yes (historical) | **Outdated** | Superseded and rescinded on 17 Apr 2026 by SR 26-2 and OCC Bulletin 2026-13. Cite the current documents. |
| NIST AI RMF 1.0 (26 Jan 2023); NIST-AI-600-1 (26 Jul 2024) | Yes | Months confirmed | I did not re-fetch the exact days. The claim that "a revision is under way" is unverified. |
| Santiago Principles (24 GAPP; IMFC 2008) | Yes | Correct | The IMFC welcomed them in October 2008. |
| Sakana AI blog posts: AI CUDA Engineer (17 Sep 2025), Nature (26 Mar 2026), MUFG (6 Mar 2026), Daiwa (3 Oct 2025), SMBC (30 Apr 2026) | Yes | Correct | As the dossier says, there is no blog post on *The Agentic Scientist*. |
| Nature article s41586-026-10265-5 | Link exists | Unverifiable | The page redirects to an authentication step, so its title and authors remain unverified, as the dossier itself says. [Resolved 2026-10-18 by the literature audit and confirmed on Crossref: *Towards end-to-end automation of AI research*, Nature 651(8107):914–919, DOI 10.1038/s41586-026-10265-5; authors Lu, Lu, Lange, Yamada, Hu, Foerster, Ha, Clune. Its abstract reports a 70% workshop acceptance rate. The 69% and 6.33 in row 18 are blog figures, not abstract figures.] |
| Gaddipati et al. (2026), MLReplicate, "59%" (cited in paper App. A) | Cited in the paper | Primary not checked | The dossier correctly reports this as unverified. [Checked 2026-10-18 against arXiv:2605.16616 v1: automated review accepted 10 of 37 valid submissions; experts reviewed those 10, three reviews each, and "identified fabricated or unsupported claims in 59% of all evaluations" (§3). App. A's wording is accurate; the abstract's ("59% of accepted automated reviews") is looser. The dossier now cites the study.] |

**Attribution notes (low risk of garbling):**
- **Three-judge design.** The dossier's stage table (§3.1) attributes "three blind design judges plus an adjudicator" to paper §3.1 and Fig. 2. The paper shows a single independent design review. The three-judge and adjudicator design comes from the repo prompts `validate_task_design.md` and `adjudicate_task_design.md`.
- **ALIFE rubric.** Dossier §5.1 describes two rubrics. The paper describes one rubric, which banned hidden credit assignment through autodiff or transposed forward weights, and says that *this* rubric "required" the positive and negative streams to remain distinct.

---

## 4. Reasoning issues and overclaims in the design implications

**Severity:** **H** high · **M** medium · **L** low.

1. **(M–H) Belief fusion (Eq. 6) combines signals that are neither comparable nor independent.**
   - *Different quantities.* The three inputs measure different things over different horizons:
     - underwritten IRR is an ex-ante, since-inception figure;
     - current actual IRR runs from inception to date and includes unrealized, possibly stale, NAV;
     - the strategy group's forecast looks forward.
   - A precision-weighted mean only makes sense once each input is mapped to a common target, such as the expected forward return from current NAV to exit.
   - *Correlated errors.* Forecasts are usually anchored on the underwriting case and on current marks, so their errors are correlated with the other two. Weights equal to inverse marginal variances then double-count shared information and overstate how precise the result is.
   - *Fix.* Use a covariance-aware combination (BLUE/GLS) or a hierarchical Bayesian model, with an explicit mapping to a common horizon.
   - *Disagreement flag.* $D_i$ should be computed on bias-corrected values. Otherwise systematic optimism at underwriting will flag most assets.
   - *Why it matters.* This formula is the core of the user's requirement to use three return series.

2. **(M) The noise-aware promotion rule (Eq. 4) is applied to a score that is not an average over paths.**
   - $\hat\Delta=\frac1N\sum_\omega[s_\omega(\pi')-s_\omega(\pi^*)]$ assumes a score defined path by path.
   - The score in Eq. 3 includes terms that do not decompose by path:
     - $\mathrm{ES}_{95}(\mathrm{MDD})$, a tail functional;
     - an LP shadow price, $\psi_{liq}$;
     - irreversibility and transaction-cost terms.
   - The SE formula $\sqrt{2p(1-p)(1-\rho)/N}$ holds only for a difference of two probabilities.
   - *Fix.* Estimate SE(Δ̂ of S) with a paired bootstrap over the common-random-number (CRN) paths. Alternatively, apply the rule only to the P(10%) component and treat the other terms as gates.

3. **(M) "Model quality is a second-order lever on performance" (exec summary #5) is an overclaim.**
   - The paper says "the underlying model matters more" than the harness (§5), and that the base model "can have a significant impact" (§6.3).
   - The dossier's own §4.3 concludes that "the model drives the quality of results inside a valid contract."
   - *Defensible restatement.* For a fiduciary, validity is the binding constraint. Once validity holds, model capability is the main driver of quality.

4. **(M) The lesson about Codex being "over-literal" (§3.7, Risk 3) rests on misread evidence.**
   - App. G.5, which the author could not read, shows the GRPO prompt said: "Do NOT perform hyperparameter tuning, grid searches…". Codex was obeying an explicit prohibition.
   - Pi, on the other hand, *did* explore an action no one had named: it changed the evaluation protocol.
   - The evidence therefore does not support "unless an action is named in the action space, agents may never explore it." It supports two different lessons:
     - explicit prohibitions are followed literally and can suppress useful exploration, so bans should be scoped narrowly;
     - unnamed actions *are* explored, sometimes illegitimately, so integrity has to be enforced by the evaluator.
   - Listing REFINANCE and LEVER explicitly is still sensible, but on general design grounds, not because of this evidence.

5. **(M) Protocol gaming is framed as a problem with one agent (§6.8 KPI, §3.7).**
   - It also happened in the Claude Code runs without shared knowledge (Fig. 17).
   - Integrity gates, such as hash-locking the evaluator and protocol checks owned by the evaluator, must not depend on which agent is used.
   - Choosing a different agent should not be counted as a mitigation.

6. **(L–M) The rule to write rubrics at "intermediate strictness" over-generalizes from Table 6.**
   - It comes from one task, apparently with one run per condition and no seeds or confidence intervals.
   - The gap between 0.976 and 0.9708 could easily be run-to-run noise.
   - Only the validity flip, where the loose rubric produced the wrong method, is robust evidence.

7. **(L) The rule "no gain beyond 2 workers" over-generalizes from Fig. 15.**
   - It comes from one task, with 1, 2 and 4 workers and three seeds each.
   - The paper itself calls the benefit "non-monotonic" and says more workers do "not necessarily yield better final results."

8. **(L–M) The successive-halving defaults clash with the materiality threshold (Eq. 7, §6.7).**
   - At rung 0, with 2,000 paths, SE(Δ̂) ≈ 0.50 pp at ρ = 0.9. That is twice ε_mat = 0.25 pp, so early culls are dominated by noise unless the effects are large.
   - At N_cal = 10,000, the smallest promotable Δ̂ is about 0.70 pp (0.25 + 2 × 0.224).
   - The complexity example in §7 calls N = 10,000 "rung 0", but Eq. 7 sets N₀ = 2,000. That is 1.62×10⁹ against 3.24×10⁸ updates.
   - Reusing paths across rungs would cut the cost from 216k to 162k path evaluations.

9. **(L–M) Exact Shapley attribution over actions (Stage 4) is combinatorially infeasible at the asset level.**
   - It needs 2ⁿ coalition evaluations, and each one is a Monte Carlo run.
   - Group the actions, or use sampling-based Shapley and report its own Monte Carlo error under CRN.

10. **(L) "Promotion of a candidate without passing its gates" (exec summary #7) overstates the problem.**
    - A candidate must still pass the correctness gate, which the evaluator owns. Only the rubric gate, which the agent verifies, is not required.
    - The paper documents this as intended (§3.3).
    - ADIC's own design choice, requiring gate rubrics filled in by the evaluator, is sound. The framing just should not imply a defect in the code.

11. **(L) The shrinkage ratio Δ_val/Δ_cal ≥ 0.5 is unstable when Δ_cal is small or noisy.**
    - Pair it with a confidence interval on Δ_val, or test Δ_val > 0 directly.

12. **(L) The human-edit KPI benchmark (17.5% / 10.7%) uses only the stage before submission.**
    - The step from submission to camera-ready added a further 32.8% inserted and 15.6% deleted.
    - The share of words changed is also a weak proxy for verification effort, which included re-running experiments and checking every reference.

13. **(L) Repeated promotions have no family-wise error control.**
    - The z = 2 test is repeated over about 20 cycles and 2–3 workers.
    - At the materiality boundary (true Δ = ε_mat), each test promotes falsely with probability ≈2.3%. Over about 40 independent tests, the chance of at least one false promotion is ≈60%.
    - A candidate with true Δ = 0 is rarely promoted (≈0.1% per test, ≈3.6% over 40 tests), because ε_mat sets a higher bar.
    - ε_mat and the sealed plane reduce the risk, but this should be stated.

14. **(M) The governance mapping should reflect current scope.**
    - Under SR 26-2, US model-risk guidance excludes generative and agentic AI models, whereas PRA SS1/23 has an AI sub-principle.
    - The APL's deterministic engines fit model-risk validation.
    - The agentic layer needs its own control framework, for example NIST AI RMF / AI 600-1 plus internal policy. It should not be assumed to sit under the model-risk umbrella.

**Checks that passed:**
- $D_t$ ≈ $13.3bn (exactly $13.275bn).
- Standard errors of 0.50 pp and 0.22 pp.
- CRN standard error of 0.22 pp.
- Expected maxima of 1.539, 1.868 and 2.249.
- Successive-halving rungs and the 216k cost (4.32 full runs).
- 1.62×10⁹ updates.
- r² = 0.19.
- 500 tail samples at P99 with 50k paths.
- The gate algebra, a floor gate of worst-case P(R̄₅ᵧ ≥ 7%) ≥ 95%, is consistent with the prior deck's rule of at most a 5% breach probability.

---

## 5. Overall reliability rating

**High for the empirical and source claims; medium for the design mathematics.**
- No claim was refuted, and most of the six corrections are small.
- The material corrections are that the US regulatory anchor has been superseded, and that protocol gaming is not confined to one agent.
- Before the APL design is used as a basis for IC decisions:
  - fix the specifications for belief fusion and for the promotion statistic (§4, items 1–2);
  - restate the "second-order" claim;
  - replace SR 11-7 with SR 26-2.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.3 and §2.4 item 12; `research/literature/13_paper_deepread.lit.md` §2. No verdict in §2 or §3 of this log is reversed, and the audit found nothing this log wrongly accepted, so no erratum is added.

- §3, row "Nature article s41586-026-10265-5": resolution note added (title, venue, DOI and authors confirmed on Crossref; 70% workshop acceptance rate in the abstract; 69% and 6.33 are blog figures).
- §3, row "Gaddipati et al. (2026), MLReplicate": primary-source check added (arXiv:2605.16616 §3: 59% of the expert evaluations of the 10 automatically accepted manuscripts; App. A's wording is accurate).
- Note: the header's "not edited" describes this verification pass. The dossier was edited for citation corrections on 2026-10-18, and those changes are listed in its own "Citation corrections (2026-10-18)" section, including SR 11-7 → SR 26-2 (row 23).
