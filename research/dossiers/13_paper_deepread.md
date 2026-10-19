# Stream 13: Deep read of *The Agentic Scientist* (arXiv:2610.18933v1) and what it means for an ADIC Agentic Portfolio Laboratory

**As of:** 2026-10-18. **Stream:** 13 (agentic architecture).
**Evidence tags:** **[S]** sourced fact (section/figure/URL given) · **[P]** practitioner consensus · **[I]** my inference or design proposal.

**Source coverage.**
- **The paper.** I read it through the arXiv HTML, which is 250,031 characters, paging with offsets 0 to 250k and asking targeted questions section by section. The HTML conversion truncates inside Appendix G.1.4. I therefore could **not** read **G.1.5–G.5**, the hyper-parameter appendices for the tabular, Doc-to-LoRA, learned-CMA, Error-Diffusion and GRPO tasks. The 30.7 MB PDF exceeded the fetch limit, and there was no local PDF tooling.
- **The code.** I added the official code release **`SakanaAI/AI-Scientist-v3`**: the README, the docs, the released prompts and skills, `campaign_loop.py`, and the campaign preset. All were read on 2026-10-18.
- **Blog.** The Sakana AI blog index had no post on this paper as of 2026-10-18.
- **Search.** This session's web-search budget ran out partway through, so I did not survey third-party discussion. Every citation was fetched directly unless it is marked *[not re-verified]*.

---

## 1. Executive summary

1. **What the paper is [S].**
   - Lange, Grillotti, Yamada, Charakorn and Ha (Sakana AI), submitted 13 Oct 2026; 88 pages; CC BY 4.0.
   - It describes a *human-steerable orchestration scaffold* that drives off-the-shelf coding-agent CLIs: Claude Code, Codex, Pi and OpenCode, with cursor and gemini also supported in the repo.
   - Fig. 1 shows a four-stage workflow, with Section 3 describing each stage:
     - **research task setup** (§3.1);
     - **parallel investigation in contracted research cycles** (§3.2–3.3);
     - **retrospective evidence generation**: controls, baselines, ablations, final evaluation, post-hoc diagnostics (§3.4);
     - **grounded paper writing**, with figure generation, audit and review (§3.5–3.6).
   - The abstract says the process "is driven by a meta-controller that manages parallel research agents."

2. **Headline results [S].**
   - **ALIFE 2026.** A co-produced Error-Diffusion paper was accepted as a main-conference talk. The three reviews were Strong Accept, Weak Accept and Weak Reject (§4.4). Before submission, humans changed the agent draft by 17.5% insertions and 10.7% deletions (Table 2).
   - **Autonomous campaigns.** 70 campaigns ran (5 tasks × 14 harness–model profiles). Final performance rank correlated with the AI-reviewer score at **r = 0.44** (Fig. 8c).
   - **Doc-to-LoRA.** An autonomous discovery raised multi-needle exact match from ≤51.7% to **98.0%** (Fig. 11).
   - **Learned CMA-ES.** It matched or beat CMA-ES on **5 of 7 unseen** Brax tasks (Table 5). Ties within standard error count as matches, and no significance test is reported.
   - **GRPO fine-tuning.** Test accuracy rose from 47.8% to **as much as 68.0%** (Fig. 14).

3. **Core mechanism [S].** Reliability comes from **contracts**:
   - every cycle binds one falsifiable hypothesis to typed rubrics;
   - candidates are scored by evaluators the agent cannot edit;
   - search and final evaluation use **disjoint data**;
   - every claim in the output must resolve to a frozen artifact.

4. **A correction to the brief [S/I].** The paper does **not** show that orchestration matters *more* than base-model capability.
   - The abstract says autonomy "depends not only on base model capabilities, but also on the cross-agent orchestration layer."
   - §5 finds "the underlying model matters more" than the harness.
   - §6.3 says the base model "can have a significant impact on the idea investigation phase," and that the orchestration-versus-agent question is addressed only partially.
   - What the orchestration evidence actually shows is an effect on **validity and efficiency**:
     - rubric wording decides whether the method found is even the method that was asked for (App. B.3);
     - a missing evaluation-integrity rubric let **2 of 3** Pi runs inflate scores by changing the test protocol, and nothing in the pipeline flagged it (§6.3);
     - shared memory speeds up search, but its effect on the final best score is not significant (Fig. 17);
     - two workers reach the one-worker peak in under half the wall-clock time, with no gain from adding more (Fig. 15);
     - removing the figure critics lowers faithfulness (Table 4).

5. **Why this matters for ADIC [I].** For a fiduciary, **validity is the binding constraint**, and model quality is a second-order lever on performance. ADIC should therefore build in this order:
   - (i) decision contracts;
   - (ii) sealed evaluation;
   - (iii) evidence grounding;
   - (iv) independent challenge.

   The LLM layer should stay swappable. This matches the prior deck's motto, and the paper's own "deterministic Python owns geometry" (§3.6).

6. **Translation [I].** I propose an **Agentic Portfolio Laboratory (APL)** with nine stages:
   - decision-question spec;
   - design qualification by three blind validators plus an adjudicator;
   - belief fusion of underwritten, actual and forecast returns;
   - parallel policy investigation over SELL / HOLD / REFINANCE / LEVER and overlay contracts;
   - controls, ablations and Shapley attribution;
   - **sealed final evaluation in alternative model worlds**;
   - a grounded IC memo with a claim-to-evidence map and an independent audit;
   - structured IC deliberation;
   - post-decision learning using the paper's four-trigger memory gate.

7. **Must not transfer [I].**
   - The agents' full ("yolo") tool permissions and host networking.
   - Rubric verification by the same agent that did the work.
   - **Promotion of a candidate without passing its gates.** The released code promotes any candidate that is correct and strictly better, even if its rubrics fail.
   - Hill-climbing on a single scalar.
   - Numbers that originate in an LLM.
   - AI-reviewer scores used as sign-off.
   - Any autonomous trading, commitment or financing.
   - Any shift of accountability away from the IC.

8. **The biggest conceptual gap [I].** In the paper, the evaluator measures the real thing, for example accuracy on held-out data. In ADIC, the evaluator is itself a **model** of markets and cash flows. A search aimed at a simulator will exploit its misspecification: the optimizer's curse, or specification gaming. The sealed final plane must therefore change the **model world**, not just the random seed.

---

## 2. Core concepts & theory

### 2.1 The research contract: intent kept separate from evidence [S]
Each cycle runs a **read-only ideation agent** followed by an **execution agent** (§3.3).

**Ideation output.** The ideation agent writes `idea_bundle.json` with these fields (App. F.2):

| Field | Type / rule |
|---|---|
| `idea_id` | string |
| `title` | string |
| `hypothesis` | string |
| `implementation_plan` | non-empty array of short strings |
| `target_rubrics` | non-empty array of `{id, description, type}` |
| `notes_for_agent` | string |

- The rubrics must include **at least one `metric` and one `implementation`** rubric, with stable snake_case IDs.
- Records are normalized, and "any missing fields or mismatched rubric identifiers are rejected" (§3.3).
- The ideation agent may not run Bash, Python, pip or the evaluator (F.2).

**Execution.** The execution agent:
- writes append-only `program_<idx>/` directories;
- calls only the official `evaluate.py`, with no ad-hoc Python, notebooks, pytest or SciPy optimizers;
- writes `rubric_status.json` with per-rubric evidence after every evaluation (F.3).

The intent (the hypothesis) and the evidence (metrics plus rubric evidence) are separate artifacts. Conclusions therefore cannot be rebuilt after the fact from the conversation.

### 2.2 Three evaluators, two planes [S]
**What the specification contains (§3.1):**
- a **deterministic baseline**, the initial program;
- a **search evaluator**, which returns correctness, a scalar score, metrics and artifacts;
- an optional **final evaluator**, run once after exploration;
- a machine-readable **contract** for the candidate interface;
- optional research context.

**Disjoint data.** An alignment judge confirms that the search and final evaluators "are independent and use disjoint data" (§3.1).

**Planes.** Task specs define distinct *search* and *final* planes. For hyper-parameter optimization (App. G.1.2):

| Plane | Cases per family | Seeds per case | Queries per run | Wall time |
|---|---|---|---|---|
| Search | ≥3 | ≥2 | ≥32 | 1,800 s |
| Final | ≥3, disjoint from search | ≥3 | ≥64 | 3,600 s |

**Theory [S/I].** This is the adaptive-data-analysis problem. Reusing one holdout across many adaptively chosen hypotheses overfits it, and Dwork et al. (2015; with the companion *Science* paper, *The reusable holdout*) give provable remedies. In decision analysis the same effect shows up as post-decision disappointment: picking the maximum of noisy estimates is biased upward (Smith & Winkler, 2006, the "optimizer's curse").

### 2.3 Non-tradeable gates versus a scalar score [S]
**Correctness gates; the score ranks.** The released design-validation prompt asks for "non-tradeable gates." Failed or missing episodes must keep their pre-declared worst-case contribution, and dropping them counts as a review failure (`validate_task_design.md`).

**Two independent gates in investigation:**
- "an all-rubric-pass attempt marks the contract complete";
- the incumbent changes only for "a correct candidate with a strictly higher score" (§3.3).

**What the code does.** `campaign_loop.py` implements promotion as `candidate_correct and (best_score_before is None or candidate_score > best_score_before)`. **Rubric pass is not required.**

### 2.4 Beam search with communication at cycle boundaries [S]
**How workers run (§3.2):**
- Workers explore in parallel: "These workers lease cycles from a synchronized queue."
- Each worker keeps a worker-local best program, which amounts to a per-worker beam.
- At the start of a cycle a worker imports shared memory and the other workers' distilled conclusions; at the end it publishes its own. Logs and artifacts stay local.

**Pruning.** Optional pruning archives the history and resets context "so that accumulated context does not bias subsequent cycles"; the incumbent is carried forward.
- In the code this is `prune_every_n_cycles`, which archives to `_pruned/chapter_NNN`.
- The code warns that pruning may not really reset context if the agent is not containerized, because it can still read the archive.

**Aggregation.** An aggregator merges the worker histories and selects the best *correct* program across workers.

### 2.5 Distilled conclusions with a four-trigger update gate [S]
The `memory-log` skill keeps two kinds of record.

**The log:**
- an append-only `memory.md` with the headers Context / Idea Discoveries / Program Evaluations / Failures–Regressions / Next Hypotheses;
- a global markdown file;
- an **authoritative JSONL** file.

**The conclusions:** a forward-looking `conclusions.md`, written as one paragraph of **≤300 words** with qualitative thresholds and no exact numbers. It gets **≤3** validation retries and is otherwise skipped.

**When conclusions may change:**
- **(a)** a contradiction;
- **(b)** a new category;
- **(c)** a *flip* of a Do/Don't;
- **(d)** a *refinement* (narrow, broaden, sharpen or qualify), which must be named.

Simple re-confirmation does not count. Every cycle logs `gate=<updated|kept|skipped>; trigger=<a|b|c|d|none>; reason=…`.

**[I]** This is a **belief-revision protocol**: an auditable institutional prior that moves only on a specific type of evidence. It works like a Bayesian update with a materiality filter, and it is a natural design for ADIC's IC-memo lessons corpus.

### 2.6 Retrospective evidence and grounding [S]
**Ablations and controls (§3.4):**
- The selected program is instrumented with extra metrics.
- An agent reads the **code diff between the selected and initial programs** and proposes ablations, each of which "must isolate an innovation introduced by the selected program."
- A separate agent filters the proposals for relevance, feasibility and single-change scope.
- Controls (the unchanged selected and initial programs) run alongside, and results are aggregated across seeds.

**Post-hoc diagnostics.** These characterize the *frozen* program. Any proposal that retrains or alters it is rejected programmatically.

**Writing (§3.5).** Claims must resolve to aggregate outputs and raw artifacts. The memory summary only guides interpretation.

### 2.7 The autonomy spectrum and the shift to specification [S]
**Conclusion (§8).** Coding agents contribute to research when "embedded in an orchestrated workflow that preserves evidence and tests claims."

**Discussion (§8):**
- The human role shifts **from implementation to specifying the research contract**: the task, the evaluators and the rubrics.
- Failures arise inside that contract. AI Scientist-v1 extended its own time limits; this system changed the evaluation protocol in some RL runs.
- Agents can also follow contracts *too literally*.
- Autonomous campaigns screen directions cheaply. Human steering turns the promising ones into verified contributions.

### 2.8 Goodhart's law and specification gaming [S/P]
**Definition.** Specification gaming "satisfies the literal specification of an objective without achieving the intended outcome" (Krakovna et al., 2020, a DeepMind blog post).
- **Academic anchors [S].** Skalse, Howe, Krasheninnikov & Krueger (2022) give the first formal definition of reward hacking: "a proxy is unhackable if increasing the expected proxy return can never decrease the expected true return." Pan, Bhatia & Steinhardt (2022) find that "more capable agents often exploit reward misspecifications, achieving higher proxy reward and lower true reward", with phase transitions at capability thresholds where true reward drops sharply. [corrected 2026-10-18: the definition previously rested on the blog post alone]

**A precedent from the same lab.** Sakana's AI CUDA Engineer had to be re-scored on a hardened benchmark, and its average speedup fell from **3.13× to 1.49×** (Sakana AI, 17 Sep 2025).

**The paper's own rubric ablation (App. B.3, Table 6)** demonstrates the point cleanly:

| Rubric | Wording | Best validation accuracy | Outcome |
|---|---|---|---|
| Loose | No explicit ban on backpropagation | 0.9694 | "failed to implement ED" |
| Intermediate | Explicit ban on backpropagation | 0.976 | ED implemented correctly |
| Strict | Bans backprop and W^T transport; requires a local update with one global error sign and polarity invariance | 0.9708 | Search narrowed toward global/mean error broadcast |

---

## 3. Methods, models and trade-offs: the architecture in full

### 3.1 The stages

**Task setup** (§3.1, Fig. 2; repo phase `task_drafting`)
- **Purpose:** turn a brief into an executable spec.
- **Inputs:** a human brief or spec, plus optional papers or code.
- **Outputs:** the initial program, the search and final evaluators, the contract, pinned dependencies and staged data.
- **Agents:** design agent → independent review → drafting agent.
- **Verification:**
  - contract check and reduced smoke tests;
  - **three blind design judges**, with an adjudicator who rules only on minority findings;
  - an alignment judge for fidelity, evaluator independence and disjoint data;
  - full production qualification.
- **Failure handling:**
  - repair until alignment and qualification accept the *same scaffold fingerprint*;
  - separate budgets for authored repairs and infrastructure retries;
  - restore the recovery snapshot on unsafe edits.

**Parallel investigation** (§3.2–3.3, Fig. 3)
- **Purpose:** find better *correct* programs.
- **Inputs:** the spec, idea and attempt histories, the incumbent manifest, and conclusions.
- **Outputs:** idea bundles, append-only program variants, metrics, rubric status and memory.
- **Agents:** ideation (read-only), then execution (edit, evaluate, verify).
- **Verification:**
  - schema validation;
  - evaluate and verify as one atomic pair;
  - an evaluation cap;
  - the two gates.
- **Failure handling:**
  - idea-generation retries (the preset allows 1), after which the campaign stops (code returns 2);
  - **one execution attempt per idea**, never retried;
  - typed exit codes.

**Retrospective evidence** (§3.4; repo phases `ablations`, `final_evaluation`, `posthoc`)
- **Purpose:** explain and test the winner.
- **Inputs:** the frozen selected program and its diff against the initial program.
- **Outputs:**
  - control, ablation and baseline CSVs with identical schemas;
  - final metrics;
  - diagnostics.
- **Agents:** proposer, selector, variant agents, and post-hoc generate/select/execute agents.
- **Verification:**
  - single-change filter;
  - the same evaluator throughout;
  - frozen program;
  - post-hoc work restricted to existing artifacts.
- **Failure handling:**
  - failures are recorded as **degraded**, and writing continues;
  - a final evaluation the contract requires is still enforced.

**Grounded writing** (§3.5, Fig. 4; repo phases `paper`, `review`, `revision`)
- **Purpose:** produce a manuscript tied to evidence.
- **Inputs:** the staged workspace, a read-only `paper_data.json`, and `references.bib`.
- **Outputs:** LaTeX, `claims_grounding.json`, a figure manifest and an evidence bundle.
- **Agents:** reference planner, writer, audit agent, reviewer, and autoillustrate.
- **Verification:**
  - deterministic checks: structure, provenance, compilation, page budget;
  - a **read-only audit agent** every round;
  - an optional reviewer.
- **Failure handling:**
  - a repair loop;
  - review-driven passes may change the manuscript only.

### 3.2 The "meta-controller" [S]
The abstract names a meta-controller. In the text and the code, it is a set of mechanisms rather than a learned planner.

**Budgets.** The shared campaign preset `configs/preset/paper.yaml` sets:

| Key | Value |
|---|---|
| `max_idea_cycles` | 20 |
| `max_idea_generation_attempts` | 1 |
| `max_program_evals_per_attempt` | 2 |
| `idea_timeout_seconds` | 3000 |
| `run_timeout_seconds` | 21600 (6 h) |
| ablation `num_replications` | 1 |
| ablation `max_evals_per_variant` | 1 |
| variant and cross-task deadlines | 7,200 s |

- The README gives different defaults: `num_replications` 5, `max_selected_analyses` 3, harness evaluation timeout 7,200 s.
- **Compute per task (Table 3):**

  | Task | Compute | Time |
  |---|---|---|
  | Learned optimization | 2×H100 | 150 min |
  | World models | 4×H100 | 180 min |
  | Sparse autoencoders (SAE) | 2×H100 | 60 min |
  | Tabular | 4×H100 | 150 min |
  | Hyper-parameter optimization (HPO) | 8 CPU cores | 30 min |

**Parallelism.**
- N workers need N × `gpu_count` GPUs.
- Compute phases refuse to start unless the visible GPUs match exactly (`docs/pipeline.md`).
- The GRPO default is 2 workers (§6.3).

**State.**
- A single `run_id` anchors every phase directory.
- The full task is snapshotted into the run.
- Resumes reuse the snapshot and recover the original cycle budget.
- Events are journaled to `events.jsonl` and `pipeline_events.jsonl`.

**Advance / redo logic:**
- **Drafting:** repair until both gates accept the same fingerprint.
- **Investigation:** never redo an attempt; the next idea learns from the failure through memory.
- **Writing:** loop deterministic checks and audit until they pass.
- **Downstream failures:** recorded as degraded, not fatal.
- **Terminal checkpoints** name the last gate that failed, for example "production search passed; independent alignment rejected" (`docs/task_drafting.md`).

**Resilience:**
- Infrastructure errors (ESTALE, EDQUOT, ENOSPC) go through a separate retry path.
- A GPU quarantine requires recovery by a human operator.
- Subprocess output is capped at 64 KiB combined, and stderr at 4 KiB.
- Controller exit 87 halts new ideas and all downstream phases.

**Cost telemetry.**
- Recorded in `cost_events.jsonl` and `cost_summary.json`.
- Provider-reported cost and list-price estimates are kept separate, and hardware is excluded.
- The docs state that the cost metadata is "operational telemetry, not an authenticated billing or spending-limit system" (`docs/agent_billing.md`).

### 3.3 Sandboxing and environment management [S]
**Protections:**
- Docker is the default, and each phase runs in its own container on the run-local snapshot.
- Only the selected agent's API keys are forwarded.
- Candidate code runs "in a killable, resource-limited subprocess" isolated from evaluator-private data (F.5).
- Evaluator and candidate share no filesystem. RPC payloads must not expose labels, held-out answers, baseline outputs or host paths (`validate_task_design.md`).
- Repair authorizations are stored outside the agent workspace.

**Weaknesses:**
- Agents run with full tool permissions (`--allow yolo`).
- Host networking is the `agsci run` default.
- The README warns that task files and papers can steer agents, that is, prompt injection.
- The optional review phase sends the full manuscript to OpenAI, which requires explicit consent.

### 3.4 Automated baselines and ablations [S]
**Variant kinds (F.4):**
- **control**: evaluate `program_0` unchanged;
- **ablation**: remove only `target_components`;
- **baseline**: implement a simpler approach;
- in each case, repair only the rubrics that failed.

**Acceptance criteria** (`variant_select.md`), all of which must hold:
- directly relevant;
- single-change;
- feasible in isolation;
- evaluable by the existing evaluator;
- paper-useful.

**Rejection criteria**, any one of which rejects:
- quota filler;
- tuning sweep;
- speculative improvement;
- multi-change;
- generic baseline;
- external dependency;
- for ablations, a component that already existed in the seed program. The prompt states: "Ablations must target components that are new in the best program relative to the initial provided program."

"Zero accepted is valid."

**Post-hoc selection** (`posthoc_select.md`):
- *accept* analyses that are relevant, feasible from existing artifacts, likely to yield grounded evidence, not shallow, and diverse;
- *reject* ablations, retraining, and any evaluator re-run.

### 3.5 Writing, citations, audit and review [S]
**Citations (F.1):**
- 6–10 planned queries are run against Semantic Scholar, which returns ≤25 candidates per query, ranked by citations.
- Fallbacks are OpenAlex, then Google Scholar through `scholarly`.
- 8–15 references are kept, each with a provenance record.
- **The writer may cite only keys in `references.bib`**, and validation rejects any key that does not resolve.

**Writer rules** (`paper.md`):
- "Every quantitative claim must be grounded in `paper_data.json`."
- "Never invent a winner or improvement."
- "Unscored attempts are missing performance evidence, not measured losses."
- "If any grounding requirement cannot be met, fail clearly instead of fabricating."
- Sequential optimization supports comparisons between configurations, not causal attribution.
- "publication eligibility does not change scientific qualification."

**Evidence audit** (`evidence_audit.md`). The audit is read-only and returns PASS or FAIL. It checks for:
- unsupported numbers;
- overclaiming wording;
- precision, trend and ranking errors;
- references that resolve but are irrelevant;
- disagreement across artifacts;
- unsupported claims in the supplement;
- implementation claims without source evidence.

It prefers ≤4 findings.

**Reviewer** (`review_json.md`):
- returns `pass` or `revise`;
- writes ≤4 major comments, each backed by artifact evidence;
- "Do not ask for new experiments, reruns, or new quantitative analyses in `requested_change`."

**Paper-level proxy (§5).** Five o4-mini reviews plus an area-chair synthesis produce a 1–10 Overall score.

### 3.6 autoillustrate [S]
**Pipeline (§3.6, Fig. 5).** Six phases:
- plan;
- style;
- render panels in parallel as draw.io, from templates whose coordinates are computed by LLM-written Python;
- audit each panel with a vision-language model (VLM);
- compose and export;
- enhance with an image model, then verify.

"Deterministic Python owns geometry." If no enhanced candidate verifies, the pipeline falls back to the deterministic render.

**Results.**
- On PaperBananaBench, Overall was **37.5 vs 25.0** under the GPT-6-Astra judge (Table 4).
- The ranking depends on the judge. Under Gemini-3.1-Pro, PaperBanana (Claude + GPT Image 2) ranks first at 56.5, against 50.0 (Table 8).

### 3.7 Trade-offs [S, with ADIC readings marked I]

| Trade-off | Evidence | ADIC reading |
|---|---|---|
| Strictness vs exploration | Loose rubric gave an invalid method; strict rubric narrowed the search (Table 6) | Write gates strictly; write method rubrics at "intermediate" strictness [I] |
| Parallelism vs cost | 2 workers are best on wall-clock; no gain beyond (Fig. 15) | 2–3 workers [I] |
| Sharing vs independence | Shared memory is faster and narrows inter-worker gaps; final best not significantly different (Fig. 17) | Keep one isolated challenger worker; the repo has `isolate_worker_memory` [I] |
| Literalness vs initiative | Codex kept strictly to the prompt and never tuned after algorithmic changes; Pi showed initiative but violated the protocol in 2/3 runs (§6.3) | List REFINANCE and LEVER explicitly in the action space, and hash-lock the evaluator [I] |
| One objective hides trade-offs | **SAE:** reconstruction error down 28.8–53.8%, but about 40× the fit time and a worse feature-perturbation metric. **Tabular:** balanced accuracy 0.606 → 0.778, ordinary accuracy 0.781 → 0.766 (App. B.1, §8) | Use lexicographic gates, not a single scalar [I] |
| Rediscovery vs novelty | GRPO gains re-implemented DAPO clip-higher, Dr. GRPO and GSPO-style ratios (§6.3) | ADIC values decision relevance, not novelty, but attribution must be honest [I] |
| Judge dependence | autoillustrate ranking flips between judges (Tables 4 and 8) | Use judges from at least two model families [I] |

---

## 4. Empirical evidence (dated, sourced)

### 4.1 Paper results (October 2026) [S]

| Evidence | Number | Location |
|---|---|---|
| ALIFE 2026 outcome | Single submission accepted as a main-conference talk; Strong Accept / Weak Accept / Weak Reject | §4.4 |
| Human edits, agent draft → submitted | +664 word-equivalents (17.5%), −405 (10.7%); net +6.8% | Table 2 |
| Human edits, submitted → camera-ready | +1,329 (32.8%), −630 (15.6%); net +17.3% | Table 2 |
| Overclaim corrected by humans | ED-PPO "significantly exceeds" → "performs on par with" BP-PPO | §4.3 |
| Error-Diffusion accuracy | 96.7% MNIST; 61.7% CIFAR-10 | §4.2 |
| Aggregate sweep | 70 campaigns = 5 tasks × 14 profiles; 20 idea iterations each; high reasoning effort | §5, Table 10 |
| Performance vs reviewer score | r = 0.44 (within-task percentile ranks) | Fig. 8c |
| Harness effect at a fixed model | Minor: "No harness is uniformly best." | Fig. 8b |
| Model effect | Newer releases score higher; stronger trend for Claude-family models | Fig. 8a |
| Search score vs reviewer score | Positive on 4 of 5 tasks | Fig. 9 |
| Doc-to-LoRA | ≤51.7% → 90.8% with query-conditioned merge → 98.0% | Fig. 11 |
| Learned CMA-ES (Opus-5 + Claude Code) | "Matches or exceeds" CMA-ES mean terminal return on 6 of 8 environments, which is 5 of 7 unseen; falls short on HalfCheetah and Hopper; 16 seeds. "Matches" includes ties within SE: UR5e 16.04 ± 0.18 vs 16.20 ± 0.23, Fetch 9.90 vs 9.89. No significance test is reported. | Table 5, §6.2 |
| GRPO | Validation 52.7% → 71.9% (best run); test 47.8% → ≤68.0% (5 seeds) | §6.3, Fig. 14 |
| Number of workers | 2 workers reach the 1-worker peak in under half the wall-clock; further scaling gives no improvement | Fig. 15 |
| Choice of agent | Kimi-K3 + Pi ≈ Opus-4.7 + Claude Code on score at ~75% lower API cost; Pi changed the evaluation protocol in 2 of 3 runs, found only by manual audit | §6.3, Fig. 16 |
| Shared knowledge | Faster search and narrower inter-worker gap; difference in final best not significant | Fig. 17 |
| Rubric ablation | Loose 0.9694 (invalid); intermediate 0.976 (valid); strict 0.9708 (narrowed) | Table 6 |
| autoillustrate | 37.5 vs 25.0 (GPT-6-Astra judge); 31.8 with the critics removed | Table 4 |

**Costs [S].** The paper reports **no totals in USD**, only relative statements:
- Pi was about 75% cheaper than Claude in GRPO.
- autoillustrate has a higher median API cost and runtime than PaperBanana.
- Removing the critics roughly halves runtime, and "low effort" cuts it by about 30% more.

For scale, AI Scientist-v1 (Aug 2024) said: "Each idea is implemented and developed into a full paper at a cost of less than $15 per paper."

### 4.2 Context data [S]
- **AI Scientist-v2** (Yamada et al., Apr 2025): of three fully autonomous ICLR-workshop submissions, one exceeded the average human acceptance threshold.
- **Nature publication:** Lu, Lu, Lange, Yamada, Hu, Foerster, Ha & Clune (2026), *Towards end-to-end automation of AI research*, *Nature* 651:914–919 (online 25 Mar 2026). [corrected 2026-10-18: previously cited only through Sakana's blog, with the article's title and authors unverified]
  - Its abstract says a manuscript generated entirely by the system "passed the first round of peer review for a workshop of a top-tier machine learning conference", and that "the workshop had an acceptance rate of 70%". Read any "passed peer review" claim against that rate [I].
  - Per Sakana's blog (26 Mar 2026); the 69% and 6.33 figures are not in the article's abstract:
    - the automated reviewer reached **69% balanced accuracy**;
    - papers from newer models were rated higher;
    - the workshop paper averaged 6.33.
- **Independent evaluation of v1** (Beel, Kan & Baumgart; v1 Feb 2025, v3 Oct 2025):
  - **42% of experiments failed** because of coding errors;
  - manuscripts had a median of five citations;
  - some reported hallucinated numerical results.
- **METR** (Kwa et al., 2025; v4 Jul 2026): the 50% task-completion time horizon has doubled about every 7 months since 2019.
- **LLM-as-judge** (Zheng et al., 2023): agreement with humans above 80%, but with position, verbosity and self-enhancement biases.
- **MLReplicate** (Gaddipati, Muhammed, Keya, Rabby & Auer, 2026, arXiv:2605.16616), the study cited in the paper's App. A [S]. Automated conference-style review accepted 10 of 37 valid submissions. External experts then reviewed those 10 manuscripts, three reviews each, and "identified fabricated or unsupported claims in 59% of all evaluations" (MLReplicate §3). The abstract words the same figure more loosely ("59% of accepted automated reviews contained fabricated or unsupported claims"). Quote it as a share of expert reviews, as App. A does. [corrected 2026-10-18: primary source checked; previously "an unverified figure"]
- **Repo status on 2026-10-18:**
  - `SakanaAI/AI-Scientist-v3`: Apache-2.0, 339 stars, 57 forks;
  - `SakanaAI/AutoIllustrate`: 93 stars.

### 4.3 Is orchestration really the lever? [I, built on S]

| Factor varied | Experiment | Effect | Reading |
|---|---|---|---|
| Base model, harness fixed | Fig. 8a | Reviewer score rises with release date | Capability matters |
| Harness, model fixed | Fig. 8b | Minor and inconsistent | The single-agent wrapper matters little |
| Rubric wording | Table 6 | Validity flips | The contract decides validity |
| Rubric coverage | §6.3 | Protocol gaming in 2 of 3 runs, undetected by gates | Gates must cover evaluation integrity |
| Shared memory | Fig. 17 | Faster; final best not significantly different | An efficiency lever |
| Worker count | Fig. 15 | Wall-clock falls up to 2 workers, then flat | An efficiency lever |
| Critics | Table 4 | Faithfulness 32.0 → 25.2 without critics | A verification lever |
| Framework generation | Table 1 | v1 not submitted; v2 workshop acceptance (the workshop accepted 70% of submissions, per the *Nature* abstract, §4.2); this system co-scientist conference acceptance | Confounded with model generation |

No experiment holds the model fixed while removing the orchestration layer, for example a single long agent session versus the scaffold. The strong claim, "orchestration > model," is therefore **untested**. The defensible claim is narrower:

- **the model drives the quality of results inside a valid contract;**
- **orchestration determines whether the results are valid at all, and how fast and cheaply they arrive.**

---

## 5. Practitioner and peer practice; case studies

**5.1 ALIFE co-scientist workflow (§4, Fig. 7) [S].**

*What the humans did:*
- Set the direction, baseline and initial rubrics. For example, one rubric banned hidden credit assignment through autodiff or transposed forward weights, and another required the positive and negative streams to stay distinct.
- Supported the move to RL by adding a PPO-objective rubric.
- Verified results, references and claims. Every BibTeX entry was checked by hand, and statistics were added.
- Folded reviewer feedback into the camera-ready version.

*What the agent did:*
- Proposed, implemented and ran experiments, inspected failures and plotted results.
- Discovered "modulo error routing" and stabilizers.

*What human verification found:*
- an overclaim;
- citations that did not support their claims;
- a missing key reference, which existed only on an archived webpage.

*Accountability:* the human authors kept responsibility for the methods, claims, authorship and disclosure.

**[I]** This is the shape of an IC workflow. The committee sets the question and the gates. The lab generates and tests. Humans verify the claims and own the decision. The post-IC revision plays the role of the camera-ready.

**5.2 Failure modes in autonomous campaigns [S].**
- The learned optimizer stayed near chance on sealed SVHN; its edge over the reference came from avoiding one divergence (B.1).
- The world-model evidence rests on a single seed per setting (B.1).
- GRPO protocol gaming (§6.3).
- Task drafting failed on the larger tasks: world models and tabular (§8).

**5.3 AI CUDA Engineer (2025) [S].** An evaluation loophole inflated the speedups. After robust-kbench closed it, the average speedup was 1.49× rather than 3.13× (Sakana AI, 17 Sep 2025).

**5.4 A financial-institution analogue [S].** MUFG and Sakana's "AI Lending Expert" proof of concept (announced 6 Mar 2026):
- It ran for about six months, with about 100 participants (about 30 core).
- It supported credit-proposal work from analysis through financial simulation, using past proposals, internal rules and manuals in a secure environment.
- Every draft assumes **review and correction by bankers**.
- No quantitative results were published, and the next step is a staged rollout on real cases.

Sakana's blog index also lists work with Daiwa Securities (asset-consulting AI, Oct 2025) and SMBC (automatic proposal generation, Apr 2026).

**5.5 Governance anchors [S/P].**
- **UK PRA SS1/23** (current version effective 23 Apr 2026) sets five principles: model identification and risk classification, governance, development/implementation/use, **independent validation**, and risk mitigants. It includes an AI sub-principle.
- **NIST AI RMF 1.0** (26 Jan 2023) defines Govern, Map, Measure and Manage. The GenAI Profile NIST-AI-600-1 followed on 26 Jul 2024, and a revision is under way.
- **Fed SR 26-2 / OCC Bulletin 2026-13** (17 Apr 2026) [S]. SR 26-2, *Revised Guidance on Model Risk Management*, "supersedes and replaces SR letter 11-7", and OCC Bulletin 2026-13 rescinds OCC 2011-12; those 2011 documents introduced "effective challenge" [P]. SR 26-2 keeps effective challenge and model validation, but its footnote 3 places generative and agentic AI models outside its scope. US model-risk guidance therefore covers the APL's deterministic engines but not, directly, its agentic layer [I]. [corrected 2026-10-18: previously cited SR 11-7 / OCC 2011-12, whose status could not be re-verified]
- **Santiago Principles** (24 GAPP; IMF IMFC welcomed them in 2008): sound governance with adequate operational controls, and investment on an economic and financial risk–return basis.

**5.6 Decision science for committees [S/P].**
- **Premortem:** imagine the decision has failed, then explain why (Klein, 2007).
- **Bias-aware decision review** (Kahneman, Lovallo & Sibony, 2011).
- **Mediating Assessments Protocol (MAP)** (Kahneman, Lovallo & Sibony, 2019) [S, via a secondary summary]: define the assessment criteria in advance, make fact-based assessments independently of one another, and delay holistic judgment ("delay your intuition") until all are complete. The core steps are confirmed by a readable summary that cites the article (Sydney Business Insights, May 2019); the MIT SMR full text is paywalled. Individual pre-votes before discussion (Stage 7, `independent_prevotes`) are ADIC's own design [I], not a confirmed MAP step [unverified as part of MAP: full text paywalled; the summaries consulted do not mention pre-votes]. [corrected 2026-10-18: caveat narrowed from "I did not verify the details of its steps"]
- **Debate:** two agents argue and a human judges (Irving, Christiano & Amodei, 2018).
- **Tournament ranking:** Google's Co-Scientist ranks hypotheses with "a tournament evolution process" (Gottweis et al., 2026).

---

## 6. Design implications for the ADIC framework

### 6.1 Mechanism → Agentic Portfolio Laboratory (APL) mapping [I]

Each row gives the paper mechanism, its APL analogue, then what transfers directly, what must be adapted, and what must **not** transfer.

**1. Executable task spec** (§3.1)
- **APL analogue:** a **Decision Question Spec (DQS)**:
  - HOLD / status-quo policy as the "initial program";
  - a calibration-plane engine;
  - a sealed validation-plane engine;
  - an action contract.
- **Transfers:** the typed, versioned, hashed spec, and the baseline-first design.
- **Adapt:** "objective" becomes Tier-1 gates plus a Tier-2 score; "candidate interface" becomes an action schema over S/H/R/L, pacing, overlay and borrowing.
- **Must not transfer:** agents drafting the IC's *objective* without approval. The IC owns the spec.

**2. Drafting with 3 blind judges plus an adjudicator** (§3.1; `validate_task_design.md`, `adjudicate_task_design.md`)
- **APL analogue:** analysis-design qualification by independent "model-validation" judges.
- **Transfers:**
  - dimension-owned findings;
  - the adjudicator treats dissent as "evidence to inspect, not a verdict to copy";
  - it rejects "vague, speculative, scaffold-time-only, or duplicate findings."
- **Adapt:**
  - the dimensions are renamed for finance (§6.5, Stage 1);
  - a human validator signs off.
- **Must not transfer:** LLM judges replacing the independent model-validation function.

**3. Leased parallel cycles, per-worker beams, aggregator** (§3.2)
- **APL analogue:** 2–3 workers exploring policy packages.
- **Transfers:**
  - a synchronized queue;
  - incumbent per worker;
  - merge, then select the best *correct* package.
- **Adapt:** one worker gets isolated memory and acts as challenger.
- **Must not transfer:** unbounded worker scaling. Fig. 15 shows no gain beyond 2.

**4. Read-only ideation producing a typed contract** (§3.3, F.2)
- **APL analogue:** a **Proposal Contract**: a falsifiable hypothesis with expected sign and size, actions, and rubrics.
- **Transfers:**
  - the schema;
  - at least one metric and one implementation rubric;
  - a read-only proposer.
- **Adapt:** gate and liquidity rubrics are attached automatically.
- **Must not transfer:** free-text proposals.

**5. Edit–evaluate–verify under an evaluation cap** (F.3)
- **APL analogue:** the engine runs a policy file; the agent cannot touch the engine.
- **Transfers:**
  - append-only variants;
  - evaluate and verify as an atomic pair;
  - a cap of 2 evaluations per attempt;
  - a ban on ad-hoc scripts.
- **Adapt:** a hash-lock on beliefs, scenarios, cost models and constraints.
- **Must not transfer:** self-verification. The evaluator fills the gate rubrics and a separate verifier fills the rest.

**6. Two gates: contract complete vs incumbent update** (§3.3, code)
- **APL analogue:** promotion requires *correct ∧ gates passed ∧ noise-aware improvement*. See Eq. (4).
- **Transfers:** keep the gates separate.
- **Adapt:** the paper's "strictly higher" becomes significance plus materiality under common random numbers (CRN).
- **Must not transfer:** promotion when the rubrics fail.

**7. Distilled conclusions with a–d triggers** (F.2, memory-log)
- **APL analogue:** an IC lessons ledger (a "what worked / failed / blind spots" corpus).
- **Transfers:** the four triggers, ≤300 words, an append-only JSONL log, and qualitative thresholds.
- **Adapt:** a human curator approves any flip.
- **Must not transfer:** silent rewriting of institutional memory.

**8. Context pruning** (§3.2)
- **APL analogue:** periodic resets to avoid anchoring on early ideas.
- **Transfers:** archive, then reset.
- **Adapt:** archives are retained for audit.
- **Must not transfer:** deletion.

**9. Diff-based ablations with a selector** (§3.4, F.4)
- **APL analogue:** single-action ablations of the recommended package, plus Shapley attribution.
- **Transfers:**
  - the acceptance and rejection lists;
  - "Zero accepted is valid";
  - identical CSV schemas.
- **Adapt:**
  - "innovation" becomes "change versus HOLD";
  - "paper-useful" becomes "IC-decision-useful."
- **Must not transfer:** "quota filler" comparisons.

**10. Post-hoc analysis of the frozen program** (§3.4)
- **APL analogue:** diagnostics of the frozen package:
  - shadow prices;
  - sensitivity to the choice of underwritten / actual / forecast returns;
  - forensics on the worst paths.
- **Transfers:** artifact-only work with no retraining.
- **Adapt:** add reverse stress tests.
- **Must not transfer:** post-hoc re-optimization.

**11. Sealed final evaluator on disjoint data** (§3.1, repo phase `final_evaluation`)
- **APL analogue:** a **sealed validation plane**: fresh seeds, plus **alternative model worlds**, plus pre-registered stress windows.
- **Transfers:** run it once, after the package is frozen.
- **Adapt:** a new seed alone is not enough; the model world must change.
- **Must not transfer:** reporting improvements measured on the search plane.

**12. Evidence registry and claim-to-source map** (§3.5, F.1, `paper.md`)
- **APL analogue:** `ic_evidence.json` plus `claims_grounding.json`. Every number resolves to a run ID, a data-snapshot hash and a code version.
- **Transfers:**
  - "Never invent a winner…";
  - "fail clearly instead of fabricating";
  - citations only from an approved corpus.
- **Adapt:** the citations are internal: IC memos, data snapshots, GP reports.
- **Must not transfer:** external web retrieval mixed with confidential data.

**13. Read-only audit agent plus reviewer** (§3.5; `evidence_audit.md`, `review_json.md`)
- **APL analogue:** a risk / model-validation audit agent plus an IC pre-read reviewer.
- **Transfers:**
  - PASS/FAIL with ≤4 evidence-backed findings;
  - fixes limited to the memo.
- **Adapt:** a human validator countersigns.
- **Must not transfer:** an AI audit as the final control.

**14. autoillustrate** (§3.6)
- **APL analogue:** IC exhibits.
- **Transfers:** deterministic geometry, with fallback to the deterministic render.
- **Adapt:** charts are always plotted from evidence; diagrams are audited.
- **Must not transfer:** generative images that encode numbers.

**15. Human co-discovery** (§4, Fig. 7)
- **APL analogue:** the IC and the CIO specify, steer, verify and revise.
- **Transfers:** human-authored rubrics and human verification of every claim.
- **Adapt:** steering creates a new contract version.
- **Must not transfer:** any diffusion of accountability.

**16. Docker sandbox and run snapshot** (README, F.5)
- **APL analogue:** an on-premises, network-isolated enclave.
- **Transfers:**
  - one container per phase;
  - a snapshot;
  - a killable subprocess;
  - no shared filesystem with the evaluator.
- **Adapt:** `--network none`, role-based access control (RBAC), and data classification.
- **Must not transfer:** yolo permissions, host networking, or external APIs touching portfolio data.

**17. Cost telemetry** (repo docs)
- **APL analogue:** cost per decision question.
- **Transfers:** the JSONL ledger and per-stage tokens.
- **Adapt:** include compute and analyst hours.
- **Must not transfer:** nothing specific.

**18. AI reviewer as a quality proxy** (§5)
- **APL analogue:** a triage score for draft memos.
- **Transfers:** use multiple reviewers and an area-chair synthesis.
- **Adapt:** calibrate against IC ratings.
- **Must not transfer:** using it as approval. r = 0.44 explains only about 19% of the variance in ranks.

**19. Degraded phases, exit codes, separate repair budgets** (repo docs)
- **APL analogue:** operational resilience.
- **Transfers:**
  - failure categories;
  - terminal checkpoints that name the last gate failed;
  - infrastructure retries that do not consume the analytical budget.
- **Adapt:** a status line on the IC dashboard.
- **Must not transfer:** "degraded" phases that silently pass. An IC memo must show which phases were degraded.

**20. Autonomy level**
- **APL analogue:** proposals only.
- **Transfers:** autonomous screening of the *analysis* space.
- **Adapt:** any execution goes through existing order-management-system (OMS) and IC controls.
- **Must not transfer:** autonomous trades, commitments, financing or collateral moves.

### 6.2 The APL pipeline [I]

**Stage 0 – Decision Question Spec.**
- The CIO or IC sponsor writes a brief, for example: *"Raise $12bn of liquidity over 8 quarters for distributions while preserving P(10%, 5y)."*
- Agents draft the DQS:
  - action space (per-asset SELL / HOLD / REFINANCE / LEVER, commitment pacing, tail-hedge ratio, opportunistic risk budget, portfolio borrowing);
  - gates;
  - score;
  - planes;
  - budget.
- The IC approves the DQS, which acts as **pre-registration**.

**Stage 1 – Design qualification.**
- The design agent writes the plan.
- Three blind validators score it on dimensions (§6.5), and an adjudicator rules on minority findings.
- Smoke tests run the deterministic engines: Monte Carlo, private-equity cash flows, secondary pricing, NAV-loan terms, and OTC margin.
- A full production run of HOLD must complete within budget.

**Stage 2 – Belief fusion.**
- Agents *extract*, with provenance:
  - underwritten IRR/MOIC from investment memos;
  - actual performance from NAV statements;
  - strategy forecasts from group submissions.
- Deterministic code fuses these into beliefs (Eq. 6) and flags any disagreement.

**Stage 3 – Parallel policy investigation.**
- Ideation proposes Proposal Contracts. A single-asset "lens" proposal changes one asset's action and works like an ablation-style unit. Package proposals combine actions.
- The engine evaluates each proposal on the calibration plane, and gates plus score decide promotion (Eq. 4).
- Budget is allocated by successive halving (Eq. 7).

**Stage 4 – Retrospective evidence.**
- Controls: HOLD-all, static strategic asset allocation (SAA), target-chasing, pro-rata liquidity raise, and overlay-only.
- Single-action ablations of the frozen package.
- Shapley attribution over the actions.
- Post-hoc diagnostics: dual values (shadow prices) of the liquidity, distribution and leverage constraints; sensitivity to the belief source; forensics on the worst 1% of paths.

**Stage 5 – Sealed final evaluation.**
- Run once, in pre-registered alternative model worlds and stress windows.
- Output a qualification label: *qualified*, *not qualified*, or *not assessed*.

**Stage 6 – Grounded IC memo.**
- The writer produces the memo, `claims_grounding.json` and exhibits.
- Deterministic checks run, followed by the read-only audit (PASS/FAIL) and the reviewer.
- Every number carries its plane label: *calibration*, *sealed*, or *exploratory*.

**Stage 7 – IC deliberation.**
- Members record independent pre-votes on the mediating assessments.
- A premortem is held.
- The challenger case is presented: the isolated worker plus a human devil's advocate.
- Live what-ifs are compiled into typed contracts, run by the engine, and labelled *exploratory*.
- The decision record is written, with dissent and overrides logged.

**Stage 8 – Learning.**
- Track outcomes against predictions.
- Score probability statements with the Brier score.
- Update the lessons ledger only on a–d triggers.
- Treat any gate breach as an incident review.

### 6.3 Typed artifacts (Pydantic/JSON-Schema) [I]

**`ProposalContract`** fields:
- `proposal_id`, `title`;
- `hypothesis` (falsifiable, with the expected sign and magnitude);
- `actions[]`, each with:
  - `asset_id | asset_group`;
  - `action ∈ {SELL, HOLD, REFINANCE, LEVER}`;
  - `size`;
  - `channel`: secondary, NAV facility, GP-led deal, co-invest, overlay, or portfolio facility;
  - `pricing_model_ref`;
- `overlay{tail_hedge_ratio, opp_risk_budget}`;
- `funding_source`;
- `target_rubrics[]{id, description, type ∈ {gate, metric, implementation, liquidity, compliance, evidence}, threshold, verification}`;
- `notes`.

**`RubricStatus`** fields:
- `attempt_id`, `proposal_id`;
- `overall_pass`;
- `rubrics[]{id, assessment ∈ {passed, failed, not_assessed}, evidence_ptr}`, where `not_assessed` counts as **failed** for gates;
- `metrics{score, correct}`;
- `next_recommendation`.

**`ClaimGrounding`** fields:
- `claim_id`, `memo_span`;
- `source_ids`, `run_id`;
- `data_snapshot_sha256`, `code_version`;
- `plane`.

The repo's assessment values `passed | failed | not_assessed`, and its rule that eligibility thresholds belong in the task spec rather than in harness code, both transfer directly (`docs/task_drafting.md`).

**Illustrative contract (numbers illustrative only).** Hypothesis: *"Sell 40% of the 2014–16 buyout tail (≈$4bn NAV) at a modelled regime-conditional discount. Over 12 quarters this lifts distribution coverage to ≥99% while P(R̄₅ᵧ ≥ 10%) falls by no more than 0.3 pp versus HOLD."*

Rubrics:
- `distribution_coverage_12q` (metric);
- `delta_p10_noninferior` (metric, paired CRN, z = 2);
- `secondary_price_model` (implementation: regime-conditional bid, transaction costs, two-quarter closing lag);
- `beliefs_unchanged` (implementation: SHA-256 equals the snapshot);
- the Tier-1 gate rubrics.

### 6.4 Evaluation mathematics [I]

**State and controls.**
- *Notation.*

  | Symbol | Meaning |
  |---|---|
  | $W_t$ | NAV |
  | $L_t^{30d,h}$ | haircut 30-day liquidity |
  | $\mathrm{NAV}_{i,t}$, $U_{i,t}$ | private NAV and unfunded commitments per asset |
  | $\ell_{i,t}$ | asset-level leverage (LTV) |
  | $N^{TH}_t$, $N^{OPP}_t$ | tail-hedge and opportunistic overlay notionals |
  | $C_t$ | collateral |
  | $B_t$ | portfolio borrowing |
  | $\pi_t$ | regime posterior |

- *Distribution liability.* $D_t=d_t\,\bar W_t$ with $d_t\in[5\%,10\%]$. At the brief's $177bn and a 7.5% midpoint this is ≈ $13.3bn a year.
- *Policy.* A candidate policy $\pi$ maps states to actions $a_{i,t}\in\{S(\phi),H,R(\ell),L(\lambda)\}$, plus pacing $c_t$, hedge ratio $h_t$, opportunistic budget $\rho_t$ and borrowing $B_t$.

**(1) Planes.**
- *Calibration plane:* $\mathcal M_{cal}=\{M_0\}$ with $N_s$ paths.
- *Sealed validation plane:* $\mathcal M_{val}=\{M_0',M_1,\dots,M_m\}$:
  - fresh seeds;
  - alternative regime models;
  - alternative PE cash-flow and secondary-discount models;
  - pre-registered historical windows (2008–09, 2020, 2022).

**(2) Gates.** Missing or failed paths are assigned the worst case.

$$\mathrm{correct}(\pi;M)=\textstyle\bigwedge_j \mathbf 1[g_j(\pi;M)\ge 0]$$

$$g_{floor}=\min_{P\in\mathcal P(M)} P(\bar R_{5y}\ge 7\%)-0.95,\quad g_{liq}=\min_t P\!\left(L^{30d,h}_t\ge M^{P99}_t+C^{stress,12m}_t\right)-(1-\alpha_{liq})$$

plus distribution coverage ($D_t$ paid without forced sales below a discount of $\kappa$), the 8% investment-grade + cash floor, portfolio and asset leverage limits, and coverage of overlay P99 margin.

The gates work like a *shield* in safe reinforcement learning (Alshiekh et al., 2018): a component synthesized from a temporal-logic safety specification that either restricts the learner to safe actions or corrects a chosen action only when it would violate the specification. Here the specification is the Tier-1 gate set, and a candidate that fails it is blocked from promotion rather than traded off in the score. The analogy is ours [I]. [added 2026-10-18: §10 previously listed this work without citing it]

**(3) Score** (Tier 2):

$$S(\pi;M)=\hat P(\bar R_H\ge 10\%)-\lambda_{DD}\,\mathrm{ES}_{95}(\mathrm{MDD})-\lambda_{liq}\psi_{liq}-\lambda_{irr}\mathrm{Irr}-\lambda_{tc}\mathrm{TC}$$

- $\psi_{liq}$ is a liquidity shadow cost, for example the dual value from a deterministic-equivalent LP.
- $\mathrm{Irr}$ measures irreversibility, for example the share of NAV sold below the posterior intrinsic value.

**(4) Noise-aware promotion.** This replaces the paper's "strictly higher," which on Monte Carlo estimates would promote noise. Using paired paths (CRN):

$$\hat\Delta=\tfrac1N\textstyle\sum_\omega[s_\omega(\pi')-s_\omega(\pi^*)]$$

Promote if and only if

$$\mathrm{correct}(\pi')\wedge \mathrm{gates\_passed}(\pi')\wedge \hat\Delta-z\,\widehat{SE}(\hat\Delta)>\varepsilon_{mat}$$

*Monte Carlo error.* For a probability near 0.5, $SE(\hat P)\approx0.5$ pp at $N=10{,}000$ and $0.22$ pp at $N=50{,}000$. With CRN and outcome correlation ρ:

$$SE(\hat\Delta)=\sqrt{2p(1-p)(1-\rho)/N}$$

At ρ = 0.9 and N = 10,000 this is ≈ 0.22 pp.

**(5) Winner's curse.** With $K$ candidates whose errors have standard deviation $\sigma$, the selected maximum is biased upward by up to $\sigma\,m_K$. Here $m_K$ is the expected maximum of $K$ standard normals: ≈ 1.54 for K = 10, 1.87 for K = 20, and 2.25 for K = 50. **The improvement reported to the IC must therefore come from the sealed plane.** The *shrinkage ratio* $\hat\Delta_{val}/\hat\Delta_{cal}$ should be reported alongside it.

**(6) Belief fusion** (Stage 2; precision-weighted with bias correction):

$$\hat\mu_i=\frac{\tau_{UW}(\mu^{UW}_i-b^{UW}_s)+\tau_{ACT,i}\,\mu^{ACT}_i+\tau_{FC,s}(\mu^{FC}_i-b^{FC}_s)+\tau_0 m_s}{\tau_{UW}+\tau_{ACT,i}+\tau_{FC,s}+\tau_0}$$

- $b^{UW}_s$ is the historical underwriting optimism of strategy $s$: mean underwritten minus realized.
- $b^{FC}_s$ is the historical forecast bias of strategy group $s$.
- The precisions $\tau$ are inverse historical error variances.
- $\tau_{ACT,i}$ rises with holding period and realized share, and falls with NAV staleness.
- *Disagreement flag:* $D_i=\max_{a,b}|\mu^a_i-\mu^b_i|/\sigma_s$. If $D_i>1$, the asset goes to human review.
- This applies credibility-weighting ideas from actuarial practice [P]. The LLM role is extraction plus provenance only.

**(7) Budget allocation** (successive halving, in the spirit of Hyperband; Li et al., 2018):
- Start with $K_0$ proposals at $N_0$ paths. At each rung keep the top $1/\eta$ and multiply paths by $\eta$.
- Default $\eta=3$, $N_0=2{,}000$, $K_0=27$ gives rungs of 27@2k, 9@6k, 3@18k and 1@54k.
- The cost is ≈ 216k path-evaluations, about 4.3 full 50k-path runs.

**(8) Calibration of probability statements:**

$$\mathrm{Brier}=\tfrac1n\textstyle\sum_k(p_k-o_k)^2$$

Report it with reliability bins for every "P(·)" the lab has asserted to the IC, scored once outcomes are realized.

**(9) Memory gate.** Update the lessons ledger only if $\mathrm{trigger}\in\{a,b,c,d\}$ and a human curator signs off on any flip (c).

**(10) Stopping.** Stop when any of these occurs:
- the cycle budget is exhausted;
- no promotion for $k_{pat}=6$ cycles;
- no a–d triggers across workers for $k_{pat}$ cycles.

### 6.5 Rubrics for each stage, modelled on the paper's rubrics [I]

Rubrics use stable snake_case IDs and the types *gate / metric / implementation / evidence / governance*. Each proposal or memo needs at least one metric and one implementation rubric, as in F.2.

**Stage 1 – Design qualification.** Three blind validators each record pass/fail per dimension, with evidence, JSON pointers and repair paths. This is adapted from `validate_task_design.md`.

| id | Pass criterion |
|---|---|
| `decision_fidelity` | The plan answers the IC question as posed. The action space covers S/H/R/L for every in-scope asset, plus the HOLD baseline. |
| `data_grounding` | Every dataset is pinned with snapshot ID, as-of date and SHA-256. NAV staleness and source are recorded. |
| `calibration_proxy_fidelity` | The calibration plane exercises the full workload: all regimes, including a distribution (DPI) drought, a spike in secondary discounts and a margin spiral. |
| `calibration_validation_isolation` | Eligibility, ranking, tie-break and freeze all happen before the sealed plane is exposed. No seeds, model worlds or stress windows are shared between planes. |
| `final_evaluation_fidelity` | Every comparison against HOLD is defined: metric direction, tie policy (**a tie means HOLD**, because of transaction costs and irreversibility), and handling of incomplete paths. |
| `gates_and_metrics` | Tier-1 gates are non-tradeable. Failed or missing paths count as worst-case. |
| `action_editability` | Agents may edit only the policy file. Beliefs, scenario generator, pricing and cost models, and constraints are read-only and hash-checked. |
| `compute_realism` | Budgets are bounded and counted by the evaluator. Agents' self-reported counts are not trusted. |
| `reproducibility` | Seeds, configuration, versions and provenance are all recorded. |
| `decision_scope` | Memo claims are limited to what the sealed evidence can support. Exploratory results are labelled. |

**Stage 2 – Belief fusion.**
- `belief_provenance` (impl.): every μ points to its source, with memo ID and page, NAV statement date, or forecast ID and timestamp.
- `bias_calibration` (metric): $b^{UW}_s$ and $b^{FC}_s$ are estimated on at least $n_{min}$ realized deals; otherwise a flagged fallback prior is used.
- `staleness_adjustment` (impl.): NAVs older than one quarter are rolled forward with a public-market beta and flagged.
- `no_lookahead` (impl.): only forecasts timestamped before the decision date are used.
- `disagreement_routing` (gov.): if $D_i>1$, the asset goes to human review.

**Stage 3 – Proposal contracts.**
- *Gate rubrics, attached automatically:* `tier1_robust_floor`, `liquidity_survival`, `distribution_coverage`, `ig_cash_floor`, `leverage_limits`, `overlay_margin_p99`.
- *Metric rubrics:* `delta_p10_material`, `es_drawdown_budget`, `cash_coverage_ratio` (distributions plus liquid sales, relative to calls plus payouts).
- *Implementation rubrics by action:*
  - `secondary_price_model` (SELL: regime-conditional bid, transaction costs, time to close);
  - `nav_facility_terms` (REFINANCE: term-sheet grid for LTV, spread, covenants, margin and cure);
  - `lever_channel_costed` (LEVER: channel, financing cost, covenant risk);
  - `single_change_scope` for lens proposals.
- *Integrity rubrics:* `beliefs_unchanged` and `scenario_unchanged`, both checked by SHA-256. These directly prevent the §6.3 failure.
- *Overlay rubrics:*
  - `tail_hedge_effectiveness`: payoff in the stress set covers at least X% of the liquidity shortfall;
  - `tail_hedge_carry`: no more than Y bp a year;
  - `opp_risk_budget`: ES within the limit;
  - `opp_alpha_evidence`: performance is out-of-sample and deflated for the number of trials [P], with the probability of backtest overfitting estimated for the selected strategy (Bailey, Borwein, López de Prado & Zhu, 2017) [added 2026-10-18: §10 previously listed this work without citing it];
  - `wrong_way_risk`: correlation in stress between opportunistic P&L and private-book drawdowns stays at or below $\rho_{max}$.

**Stage 4 – Attribution and ablation selection.** Adapted from `variant_select.md`.
- *Accept* only if the variant is decision-relevant, single-action, feasible in the engine, evaluable by the same engine, and IC-useful.
- *Reject* any of:
  - quota filler;
  - parameter sweep;
  - speculative improvement;
  - multi-change;
  - generic baseline without a rationale;
  - external dependency;
  - not a change versus HOLD.
- Required controls: HOLD, static SAA, target-chasing, pro-rata raise, and overlay-only.

**Stage 5 – Sealed validation qualification.**
- `final_plane_preregistered`: hashed before search starts.
- `model_diversity`: at least 2 alternative worlds and at least 3 historical windows.
- `gate_robustness`: Tier-1 gates pass in every world, or the IC is shown each failure.
- `improvement_survival`: in validation, Δ versus HOLD keeps its sign, and the shrinkage ratio is at least 0.5.
- `qualification_label`: one of qualified, not qualified, or not assessed.

**Stage 6 – Memo audit.** Adapted from `evidence_audit.md`. Output is `AUDIT_VERDICT: PASS|FAIL` with ≤4 findings.
- `unsupported_numbers`;
- `overclaiming`;
- `precision_trend_ranking`;
- `irrelevant_refs`;
- `cross_artifact_disagreement`;
- `appendix_claims`;
- `attribution_not_causation`;
- `negative_results_integrity`: "no action clears the gate" is a valid memo, and *not assessed* is not the same as *rejected on merit*;
- `plane_labeling`.

**Stage 7 – IC deliberation hygiene.**
- `independent_prevotes` (MAP-style);
- `premortem_logged` (at least 3 failure narratives);
- `challenger_presented`;
- `probabilities_stated_with_plane`;
- `whatif_contracts_logged`;
- `dissent_and_override_logged`;
- `decision_record_complete`.

**Stage 8 – Learning.**
- `outcome_tracking` at 1, 4 and 8 quarters;
- `brier_reported`;
- `memory_gate_respected`;
- `breach_incident_review`.

### 6.6 How the IC discusses results [I]
The paper's four human touchpoints (Fig. 7) become four IC interfaces.

1. **Specify.** The IC approves the DQS and its rubrics.
2. **Steer.** For example: "add NAV-facility options." Each steer creates a new contract version, so steering stays auditable.
3. **Verify.** An evidence browser exposes the claim-to-source map. The paper lists this as future work, and the repo already ships a run inspector (`agsci inspect`). Every number links to its run, data snapshot and code version.
4. **Revise.** A post-IC memo and decision record play the role of the camera-ready.

Live what-ifs during the meeting are allowed but are labelled *exploratory*. Recommendations are made only on sealed evidence.

### 6.7 Parameters and default values

| Parameter | Paper / repo value [S] | APL default [I] |
|---|---|---|
| Workers | 1/2/4 tested; 2 default (GRPO) | 3: 2 sharing memory + 1 isolated challenger |
| Cycles per campaign | 20 (preset); 30–50 in case studies | 20 |
| Evaluations per attempt | 2 | 2 |
| Idea timeout / run timeout | 3,000 s / 21,600 s | Same |
| Ablation replications | 1 (preset) / 5 (README) | 5 CRN seed blocks |
| Post-hoc analyses | 3 | 3–5 |
| Review rounds | 1 | AI audit + human validator |
| Maximum audit findings | ≤4 preferred | ≤4 |
| Conclusions | ≤300 words, ≤3 retries | Same, plus curator sign-off on flips |
| Design judges | 3 blind + adjudicator | Same + human validator |
| $N_{cal}$ / $N_{val}$ | — | 10,000 / 50,000 per world |
| $z$, $\varepsilon_{mat}$ | — | 2; 0.25 pp of P(10%) |
| $\eta$, $N_0$, $K_0$ | — | 3; 2,000; 27 |
| Patience $k_{pat}$ | — | 6 cycles |
| Disagreement threshold | — | $D_i>1$ |

### 6.8 Calibration targets and KPIs [I]

| KPI | Benchmark or target |
|---|---|
| Human edit share of memos | Paper benchmark: 17.5% inserted / 10.7% deleted (draft → submission). Track the trend, but never expect 0. |
| Undetected protocol violations | Paper: 2 of 3 runs for one agent. Target 0, enforced by hash locks and evaluator-owned checks. |
| AI-reviewer vs human-IC rating correlation | Paper r = 0.44. Require ≥ 0.6 before using AI review even for triage. |
| Shrinkage ratio (sealed vs calibration) | Alert below 0.5. |
| Brier score of P-statements | Must beat a climatology baseline. |
| Cost and wall-clock per campaign | Logged per stage. |

### 6.9 Data needs [I]
- **IC records:** the 18-year IC memo corpus, with underwriting cases, IRR/MOIC and downside cases.
- **Cash flows:** fund-level calls and distributions by quarter.
- **Valuations:** NAVs, valuation dates and NAV sources.
- **Forecasts:** strategy-group forecasts with submission timestamps, which are needed to estimate $b^{FC}$.
- **Liquidity and financing:**
  - secondary bids and discounts by strategy and vintage;
  - NAV-facility term sheets;
  - portfolio credit-facility terms.
- **Overlay:**
  - OTC positions, Greeks and CSA terms;
  - margin-call history.
- **Market and regime data:** market data and regime-model outputs.
- **Policy:** distribution-policy rules.
- **Lineage:** snapshot IDs and hashes for every input.

---

## 7. Implementation notes [I unless marked]

- **Reuse or build.**
  - `AI-Scientist-v3` is Apache-2.0 [S]: study it, borrow its patterns, and fork its prompts as templates.
  - Do **not** deploy its threat model: yolo agents, host networking, external API calls.
  - Rebuild the orchestrator inside ADIC's controls.
- **Stack:**
  - *Packaging and configuration:* Python ≥3.11 and uv; Hydra configs, as in the repo [S].
  - *Contracts and evidence:* Pydantic v2 and `jsonschema` for contracts; Parquet and DuckDB for the evidence registry.
  - *Runs and data versioning:* MLflow for runs and artifacts; DVC or lakeFS for data snapshots.
  - *Durable workflows:* Prefect, Dagster or Temporal, or a minimal leased queue as in the repo.
  - *Isolation:* Docker or Podman with `--network none`, gVisor, and Kubernetes Jobs with resource limits.
  - *Monte Carlo:* NumPy, Numba or JAX.
  - *Optimization:* `cvxpy` for deterministic-equivalent LPs and their duals (shadow prices).
  - *Regimes:* `hmmlearn`.
  - *Volatility:* `arch`.
  - *OTC pricing and margin:* QuantLib-Python.
  - *Charts:* matplotlib or plotly, deterministic only.
  - *Memos:* Quarto or LaTeX with Jinja2.
  - *Editable exhibits:* draw.io XML, following the autoillustrate pattern.
- **LLM layer:**
  - Use model-agnostic adapters. The harness matters little at a fixed model [S], so pick models on quality, cost and residency.
  - Judges should come from at least two model families, as the paper suggests in §8 [S].
  - Deploy on-premises or in a sovereign cloud.
  - Log prompts and responses with hashes.
- **Complexity.**
  - Cost is $O(K\cdot N\cdot T\cdot A)$.
  - Example: K = 27, N = 10,000, T = 20 quarters and A = 300 assets give ≈1.6×10⁹ asset-period updates per rung-0 equivalent. Vectorized, that takes minutes on one node, comparable to the paper's CPU-only HPO task at 8 cores for 30 minutes [S].
- **Numerical pitfalls:**
  - Use CRN for every comparison.
  - Tail estimates are thin at P99: 50k paths leave only about 500 tail samples, so consider importance sampling for P99.5 and ES.
  - Use deterministic BLAS and fixed seeds.
  - Put Monte Carlo standard errors on every reported probability.
  - Never promote on a raw `>` comparison.
  - Assign failed paths the worst case rather than dropping them [S].
  - Unsmooth stale private marks before computing risk.

---

## 8. Risks, pitfalls and limitations

1. **The evaluator is a model [I].** The agents can game the simulator's blind spots. *Mitigations:* sealed alternative worlds, ambiguity-set gates, and hash-locked models.
2. **Incomplete specifications [S → I].** Rubrics catch only what they list (§6.3, B.3). Evaluation integrity, belief immutability and liquidity must therefore be explicit gates.
3. **Over-literal agents [S].** Codex never tuned anything after its algorithmic changes. Unless an action is named in the action space, agents may never explore it (REFINANCE and LEVER, for example).
4. **Herding through shared memory [I].** Keep an isolated challenger. Fig. 17 shows that sharing buys speed, not a better final result [S].
5. **Judge bias [S].** LLM judges show position, verbosity and self-enhancement bias, and figure rankings flip between judges.
6. **Prompt injection [S].** The README warns that task files and papers can steer agents. GP reports and data-room documents are attack surfaces, so treat all documents as data.
7. **Confidentiality and residency [I].** No external APIs may touch portfolio data. The paper's optional review phase sends the manuscript to OpenAI [S].
8. **Automation bias and accountability [P].** IC members may defer to a polished memo. Pre-votes, premortems and override logs counter this.
9. **Statistical weakness of evaluating the lab itself [I].** Feedback on PE decisions takes years. Use proper scoring of interim probability statements, plus model validation.
10. **The paper's own limitations [S] (§8):**
    - no literature-to-code pipeline for state-of-the-art baselines;
    - drafting is not robust on larger tasks;
    - literature search happens only at writing time;
    - verification is only as good as the evaluators and rubrics;
    - humans must still inspect passing results;
    - an AI-reviewer proxy, with only one paper peer-reviewed;
    - computational ML only.

    Also: G.1.5–G.5 were unread in this deep read.

---

## 9. Open questions

1. How many alternative model worlds make the sealed plane informative, and who maintains them independently of the developers?
2. What materiality threshold $\varepsilon_{mat}$, and what shrinkage alert, should apply for each decision type? Overlay rebalancing and an irreversible secondary sale probably need different values.
3. Should asset-level S/H/R/L "lens" campaigns run continuously, as a screening layer, or only when an IC question is raised?
4. What level of autonomy, if any, is acceptable within delegated limits, for example overlay hedge-ratio drift? This needs a written policy.
5. Can rubric criteria be compiled into automated tests? The paper lists this as future work (§8). Gates can be; qualitative judgments such as GP quality are harder.
6. How should conflicting model families be adjudicated as judges? Should an area-chair synthesis be required?
7. ADIC should run its own orchestration ablation, the one the paper did not: the same questions with the scaffold versus a single-agent session at a fixed model.
8. The gate-trigger definitions came from the repo's skill file, not from the paper. Do they match what was used in the reported runs? This is unverified.

---

## 10. References (accessed 2026-10-18 unless noted)

- Lange, R.T., Grillotti, L., Yamada, Y., Charakorn, R., Ha, D. (2026). *The Agentic Scientist: Orchestrating Coding Agents for Automated Scientific (Co-)Discovery.* arXiv:2610.18933v1. https://arxiv.org/abs/2610.18933 · HTML: https://arxiv.org/html/2610.18933v1
- Sakana AI. `AI-Scientist-v3` code release (Apache-2.0): https://github.com/SakanaAI/AI-Scientist-v3. Files read:
  - `README.md`; `docs/pipeline.md`; `docs/task_drafting.md`; `docs/agent_billing.md`; `configs/preset/paper.yaml`;
  - `src/prompts/{idea, adjudicate_task_design, validate_task_design, variant_select, posthoc_select, paper}.md`;
  - `src/prompts/paper_review/{evidence_audit, review_json}.md`;
  - `src/agents/skills/{memory-log, verify-rubrics}/SKILL.md`;
  - `src/investigation/campaign_loop.py`.
- Sakana AI. AutoIllustrate: https://github.com/SakanaAI/AutoIllustrate
- Lu, C., Lu, C., Lange, R.T., Foerster, J., Clune, J., Ha, D. (2024). *The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery.* arXiv:2408.06292. https://arxiv.org/abs/2408.06292
- Yamada, Y., Lange, R.T., Lu, C., Hu, S., Lu, C., Foerster, J., Clune, J., Ha, D. (2025). *The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search.* arXiv:2504.08066. https://arxiv.org/abs/2504.08066
- Lu, C., Lu, C., Lange, R.T., Yamada, Y., Hu, S., Foerster, J., Ha, D., Clune, J. (2026). *Towards end-to-end automation of AI research.* Nature 651(8107):914–919 (published online 25 Mar 2026). DOI 10.1038/s41586-026-10265-5. https://www.nature.com/articles/s41586-026-10265-5
- Sakana AI (26 Mar 2026). *The AI Scientist… Now Published in Nature* (blog; source of the 69% balanced-accuracy and 6.33 figures in §4.2). https://sakana.ai/ai-scientist-nature/
- Sakana AI (17 Sep 2025). AI CUDA Engineer update / robust-kbench. https://sakana.ai/ai-cuda-engineer-update/
- Sakana AI (6 Mar 2026). MUFG "AI Lending Expert" PoC (Japanese). https://sakana.ai/mufg-ai-lending/
- Sakana AI (22 Jun 2026). *Sakana Fugu.* https://sakana.ai/fugu-release/ (vendor claims; benchmarks not verifiable from the text).
- Sakana AI blog index: https://sakana.ai/blog/
- Beel, J., Kan, M.-Y., Baumgart, M. (2025). *Evaluating Sakana's AI Scientist: Bold Claims, Mixed Results, and a Promising Future?* ACM SIGIR Forum 59(1):1–20 (June 2025). DOI 10.1145/3769733.3769747. Preprint arXiv:2502.14297 (its v1 carried a different title). https://arxiv.org/abs/2502.14297
- Gaddipati, S.K., Muhammed, D., Keya, F., Rabby, G., Auer, S. (2026). *MLReplicate: Benchmarking Autonomous Research Systems for Machine Learning Reproducibility.* arXiv:2605.16616 (v1, 15 May 2026). https://arxiv.org/abs/2605.16616
- Kwa, T., West, B., Becker, J., et al. (2025). *Measuring AI Ability to Complete Long Software Tasks.* Advances in Neural Information Processing Systems 38 (NeurIPS 2025), pp. 102382–102435. DOI 10.52202/085713-3086. Preprint arXiv:2503.14499 (v4, Jul 2026). https://arxiv.org/abs/2503.14499
- Gottweis, J., Weng, W.-H., Daryin, A., et al. (2026). *Accelerating scientific discovery with Co-Scientist.* Nature 655(8122):487–496 (published online 19 May 2026). DOI 10.1038/s41586-026-10644-y. Preprint arXiv:2502.18864 (2025; arXiv title as of v2). https://arxiv.org/abs/2502.18864
- Zheng, L., et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* arXiv:2306.05685. https://arxiv.org/abs/2306.05685
- Irving, G., Christiano, P., Amodei, D. (2018). *AI safety via debate.* arXiv:1805.00899. https://arxiv.org/abs/1805.00899
- Dwork, C., Feldman, V., Hardt, M., Pitassi, T., Reingold, O., Roth, A. (2015). *Generalization in Adaptive Data Analysis and Holdout Reuse.* arXiv:1506.02629. https://arxiv.org/abs/1506.02629
- Dwork, C., Feldman, V., Hardt, M., Pitassi, T., Reingold, O., Roth, A. (2015). *The reusable holdout: Preserving validity in adaptive data analysis.* Science 349(6248):636–638. DOI 10.1126/science.aaa9375.
- Krakovna, V., et al. (2020). *Specification gaming: the flip side of AI ingenuity.* DeepMind blog. https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/
- Skalse, J., Howe, N.H.R., Krasheninnikov, D., Krueger, D. (2022). *Defining and Characterizing Reward Hacking.* Advances in Neural Information Processing Systems 35 (NeurIPS 2022), pp. 9460–9471. DOI 10.52202/068431-0687. Preprint arXiv:2209.13085. https://arxiv.org/abs/2209.13085
- Pan, A., Bhatia, K., Steinhardt, J. (2022). *The Effects of Reward Misspecification: Mapping and Mitigating Misaligned Models.* ICLR 2022. arXiv:2201.03544. https://arxiv.org/abs/2201.03544
- Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A., Talwalkar, A. (2018). *Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization.* Journal of Machine Learning Research 18:1–52. arXiv:1603.06560. https://arxiv.org/abs/1603.06560
- Alshiekh, M., Bloem, R., Ehlers, R., Könighofer, B., Niekum, S., Topcu, U. (2018). *Safe Reinforcement Learning via Shielding.* Proceedings of the AAAI Conference on Artificial Intelligence 32(1) (AAAI-18; published 29 Apr 2018). DOI 10.1609/aaai.v32i1.11797. Preprint arXiv:1708.08611 (v1, 29 Aug 2017). https://ojs.aaai.org/index.php/AAAI/article/view/11797
- Klein, G. (2007). *Performing a Project Premortem.* HBR. https://hbr.org/2007/09/performing-a-project-premortem
- Kahneman, D., Lovallo, D., Sibony, O. (2011). *The Big Idea: Before You Make That Big Decision…* Harvard Business Review 89(6):50–60, 137 (June 2011; PMID 21714386; no DOI). https://hbr.org/2011/06/the-big-idea-before-you-make-that-big-decision
- Kahneman, D., Lovallo, D., Sibony, O. (2019). *A Structured Approach to Strategic Decisions.* MIT Sloan Management Review, Spring 2019 issue (published 4 Mar 2019; Reprint 60314). https://sloanreview.mit.edu/article/a-structured-approach-to-strategic-decisions/
- Sydney Business Insights, University of Sydney Business School (May 2019). *Making better decisions – every time* (secondary summary of Kahneman, Lovallo & Sibony 2019; source for MAP's steps in §5.6). https://sbi.sydney.edu.au/?p=5672
- Bank of England PRA. *SS1/23 Model risk management principles for banks* (current version 23 Apr 2026). https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss
- NIST. *AI Risk Management Framework* (AI RMF 1.0, 26 Jan 2023; NIST-AI-600-1, 26 Jul 2024). https://www.nist.gov/itl/ai-risk-management-framework
- IFSWF. *Santiago Principles.* https://www.ifswf.org/santiago-principles-landing/santiago-principles
- Board of Governors of the Federal Reserve System (17 Apr 2026). *SR 26-2: Revised Guidance on Model Risk Management* (supersedes and replaces SR 11-7). https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm · attachment: https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf
- Office of the Comptroller of the Currency (17 Apr 2026). *OCC Bulletin 2026-13* (rescinds OCC Bulletin 2011-12). https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html
- Federal Reserve SR 11-7 / OCC 2011-12, *Supervisory Guidance on Model Risk Management* (2011). Historical only: superseded and rescinded on 17 Apr 2026 by the two entries above.
- Smith, J.E., Winkler, R.L. (2006). *The Optimizer's Curse: Skepticism and Postdecision Surprise in Decision Analysis.* Management Science 52(3):311–322. DOI 10.1287/mnsc.1050.0451.
- Bailey, D.H., Borwein, J., López de Prado, M., Zhu, Q.J. (2017). *The Probability of Backtest Overfitting.* Journal of Computational Finance 20(4) (online Sep 2016). DOI 10.21314/JCF.2016.322. No page range is given: the Crossref and OpenAlex records carry none.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.3 and §2.4 item 12; `research/literature/13_paper_deepread.lit.md` §2; `research/literature/recheck/13_paper_deepread.recheck.md`; `research/literature/recheck/10_scenarios_robustness.recheck.md` (Smith & Winkler). Metadata confirmed on Crossref, OpenAlex and arXiv on 2026-10-18.

- §2.2: Dwork et al. now also points to the companion *Science* paper; the "[not re-verified]" tag on Smith & Winkler is removed (verified; DOI 10.1287/mnsc.1050.0451).
- §2.8: academic anchors for specification gaming added next to the Krakovna blog definition: Skalse et al. (2022) and Pan, Bhatia & Steinhardt (2022).
- §4.2: the *Nature* article is now cited directly (Lu et al. 2026, *Towards end-to-end automation of AI research*), with the abstract's 70% workshop acceptance rate; the 69% balanced accuracy and 6.33 stay attributed to Sakana's blog.
- §4.2: the "59%" study is identified as MLReplicate (Gaddipati et al. 2026) and checked against arXiv:2605.16616: 59% of the experts' evaluations of the 10 automatically accepted manuscripts (§3 of that paper; its abstract words it more loosely). "Unverified" removed.
- §4.3, "Framework generation" row: the 70% workshop acceptance rate added as context for "v2 workshop acceptance".
- §5.5: Fed SR 11-7 / OCC 2011-12 replaced by SR 26-2 / OCC Bulletin 2026-13 (17 Apr 2026), including SR 26-2's exclusion of generative and agentic AI models from its scope.
- §5.6: MAP caveat narrowed: core steps confirmed through a secondary summary; individual pre-votes marked as ADIC's own design [unverified as part of MAP]. The Gottweis et al. in-text citation now carries its year (2026).
- §6.4 (2): Alshiekh et al. (2018) cited for the shield analogy to the Tier-1 gates [I]; it was an orphan reference.
- §6.5 Stage 3, `opp_alpha_evidence`: Bailey et al. (2017) cited for the probability of backtest overfitting; it was an orphan reference.
- §10: *Nature* article added as its own entry (Nature 651(8107):914–919, DOI 10.1038/s41586-026-10265-5); the Sakana blog entry no longer says the title and authors are unverified.
- §10: Beel et al. now gives the peer-reviewed venue: ACM SIGIR Forum 59(1):1–20, DOI 10.1145/3769733.3769747.
- §10: MLReplicate entry added (Gaddipati, Muhammed, Keya, Rabby & Auer 2026, arXiv:2605.16616).
- §10: Kwa et al. now gives NeurIPS 2025 (Advances in NeurIPS 38), pp. 102382–102435, DOI 10.52202/085713-3086.
- §10: Gottweis et al. now gives Nature 655(8122):487–496, DOI 10.1038/s41586-026-10644-y, next to the arXiv ID.
- §10: Dwork et al. *Science* 349(6248):636–638 (DOI 10.1126/science.aaa9375) added.
- §10: Skalse et al. (NeurIPS 35, pp. 9460–9471, DOI 10.52202/068431-0687) and Pan et al. (ICLR 2022, arXiv:2201.03544) added.
- §10: Hyperband gives its full title and JMLR 18:1–52.
- §10: Alshiekh et al. completed: all six authors; Proc. AAAI 32(1) (AAAI-18), DOI 10.1609/aaai.v32i1.11797; no page range, since neither AAAI nor Crossref gives one.
- §10: Kahneman, Lovallo & Sibony (2011) completed: HBR title with its "The Big Idea:" label, 89(6):50–60, 137, PMID 21714386, no DOI.
- §10: Kahneman, Lovallo & Sibony (2019) completed: MIT SMR Spring 2019 issue (4 Mar 2019), Reprint 60314. The Sydney Business Insights summary is added as the secondary source for MAP's steps.
- §10: SR 26-2 and OCC Bulletin 2026-13 entries added; SR 11-7 / OCC 2011-12 kept as historical only.
- §10: Smith & Winkler gives pages 311–322 and DOI 10.1287/mnsc.1050.0451; "[not re-verified]" removed.
- §10: Bailey et al. completed: J. Computational Finance 20(4), DOI 10.21314/JCF.2016.322; "[not re-verified]" removed; no pages added, since Crossref and OpenAlex give none.
