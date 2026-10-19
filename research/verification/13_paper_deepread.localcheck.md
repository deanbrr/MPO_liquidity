# Local full-text check: Stream 13 dossier vs. arXiv:2610.18933v1

**Dossier checked (not edited):** `research/dossiers/13_paper_deepread.md`
**Authority:** `inputs/agentic_scientist_2610.18933v1.txt` (88 pages; line numbers below refer to this file)
**Context only:** `research/verification/13_paper_deepread.verify.md` (earlier web-based log)
**Date:** 2026-10-18

**Scope.**
- Every claim the dossier makes *about the paper* was checked against the local full text, including App. G.1.5–G.5, which the dossier author never read.
- Claims about external sources were **not** counted, because they are not paper claims: Dwork, Smith & Winkler, Krakovna, AI CUDA Engineer, Nature/MUFG blogs, PRA, NIST, SR 11-7, METR, Beel et al.
- The dossier's own design mathematics (§6.4) was out of scope.
- Claims the dossier sources to the `AI-Scientist-v3` repo are listed as "not in paper (repo)". They cannot be verified here, and the label shows which architecture claims rest on the repo alone.

---

## Summary

**Result: 130 claims checked.**

| Verdict | Count |
|---|---|
| Confirmed | 96 |
| Corrected | 19 |
| Refuted | 2 |
| Not in paper, misattributed or unsupported | 3 |
| Not in paper, repo-sourced (unverifiable here) | 10 |

**What holds up.**
- The numeric results drawn from the paper are accurate. That covers Tables 2, 4, 5, 6 and 8, Fig. 8c, Figs. 11 and 14–17, and Table 3.
- The ideation and execution contract is described correctly (F.2–F.4).
- The central correction to the brief is supported: the paper does not show that orchestration beats the model.

**Where the dossier goes wrong.** The problems are in the *mechanism* layer.
1. **Evaluator immutability and sandboxing are overstated.**
   - The paper protects the evaluator task by task. Doc-to-LoRA uses harness-guarded files; the GRPO agent could modify the scored evaluation procedure, and nobody noticed.
   - The paper calls its own CMA-ES contract "a cooperative research-code contract, not an adversarial sandbox" (l.7489-7490).
2. **Repo mechanisms are presented as paper mechanisms.**
   - The three blind judges plus adjudicator are the clearest case. The paper has a single review agent that also repairs the design.
   - Many "meta-controller" details exist only in the repo: budgets, exit codes, degraded phases, fingerprints.
3. **Several reported figures are misused.**
   - The r = 0.44 correlation is presented as an AI-versus-human agreement benchmark. It is not.
   - Protocol violations are framed as a problem of one agent. They also appeared in Claude Code runs.
   - The case-study settings are wrong: the paper used 1 evaluation per idea and 20–60 cycles.
   - The paper does show costs in USD, in Fig. 16.
4. **Two generalizations contradict the paper:**
   - "model quality is a second-order lever";
   - "unless an action is named, agents may never explore it."
5. **The task specifications in App. G.1–G.5 were missed almost entirely.** They hold the paper's most transferable mechanisms:
   - evaluator-owned accounting;
   - the rule that a candidate's own reports never count as evidence;
   - chronological splits with embargo gaps;
   - anonymized interfaces;
   - non-inferiority built into `correct`;
   - mandatory naive and permutation controls;
   - `not_qualified` labels;
   - Pareto comparison over operating points declared in advance.
6. **Several headline caveats were missed:**
   - The system's own CMA-ES paper attributes 55.8% of its margin over CMA-ES to fixed scaffolding.
   - Doc-to-LoRA has no separate final evaluation.
   - The paper's own figures drop seeds that produced NaN results.

**Where the local text overturns the earlier web log.**
- **Retry limit.** The web log changed "≤3 retries" to "3 attempts in total", based on the repo skill file. The paper's F.2 prompt reads "≤3 retries on validation failure" (l.6290), so the dossier matches the paper; the repo differs from the paper.
- **"Authoritative" log.** The web log said the JSONL memory log is not called "authoritative". The paper's F.2 and F.3 prompts call it "the authoritative cross-idea memory log" (l.6285, l.6378).
- **Everything else in the web log is consistent with the local text:**
  - the single design review;
  - the Fig. 16 USD axis;
  - the Claude Code protocol violations;
  - the 20–60 cycles and 1 evaluation per idea;
  - Codex's obedience to the G.5 prompt.

---

## Claims table

**Verdicts:** confirmed · corrected · refuted · not in paper (misattributed) · not in paper (repo). **"l."** = line in the local text.

| # | Claim (dossier location) | Verdict | Correct statement / note | Paper line(s) |
|---|---|---|---|---|
| 1 | Authors, Sakana AI, arXiv 13 Oct 2026, 88 pages, CC BY 4.0 (§1.1) | confirmed | The licence comes from arXiv metadata. The only CC BY 4.0 in the text belongs to the embedded ALIFE paper (l.3369). The PDF header is dated 2026-10-15. | 4, 7-8, 73, 7637 |
| 2 | Drives Claude Code, Codex, Pi and OpenCode; "cursor and gemini also supported in the repo" (§1.1) | corrected | The paper itself uses Cursor: Composer 2.5 Fast / Cursor for the ED MuJoCo/Brax runs, 60 cycles. A Gemini harness does not appear in the paper. | 600-602, 7536-7539 |
| 3 | Fig. 1 has four stages, with "final evaluation" placed under §3.4 (§1.1) | corrected | The four stages are confirmed. The final evaluation program, however, belongs to the task spec in §3.1 and "runs the selected program after exploration". §3.4 covers baselines, ablations, controls and post-hoc analysis. | 71, 209-219, 335-361 |
| 4 | Abstract: the process "is driven by a meta-controller that manages parallel research agents" (§1.1) | corrected | The quote is truncated. It continues "…and enforces rubric verification at each stage." The term appears only in the abstract, and that claim sits in tension with §3.3, where promotion does not require a rubric pass. | 18-19, 330-333 |
| 5 | ALIFE 2026 main-conference talk; Strong Accept / Weak Accept / Weak Reject (§1.2, §4.1) | confirmed | The dossier omits that a "development version" of the system was used, and that humans verified and edited the paper before submission. | 23-24, 451-456, 567-568 |
| 6 | Table 2 edit statistics; 17.5% / 10.7% used as a KPI benchmark (§1.2, §4.1, §6.8) | confirmed | Agent draft → submitted: +664 (17.5%), −405 (10.7%). Submitted → camera-ready: +1,329 (32.8%), −630 (15.6%). Units are latexdiff word-equivalents. | 546-550 |
| 7 | 70 campaigns = 5 tasks × 14 profiles, 20 iterations, high effort (§1.2, §4.1) | confirmed | The profiles split 4+4+3+3 (Table 10). The tasks were "five manually prepared research tasks". | 596, 600-604, 1377-1378, 6649-6655 |
| 8 | Final-performance rank versus AI-review rank: r = 0.44 (Fig. 8c) | confirmed | Within-task percentile ranks, n = 70. | 712, 725-728 |
| 9 | Doc-to-LoRA: ≤51.7% → 90.8% → 98.0% (Fig. 11) | confirmed | Missed caveat: one synthetic benchmark, one run per configuration, and no separate final or post-search evaluation (see Missed E4). | 954-955, 997-998, 1012-1013, 2307 |
| 10 | Learned CMA-ES matches or beats CMA-ES on 6 of 8 environments (5 of 7 unseen); falls short on HalfCheetah and Hopper; UR5e and Fetch figures as given; 16 seeds; no test (§1.2, §4.1) | confirmed | The values are exact. Missed: the system's own C.2 paper finds the fixed anchor supplies 55.8% of the margin over CMA-ES, and the learned increment "reverses sign on final solution quality". | 1079-1081, 2069-2087, 2657-2663 |
| 11 | GRPO: validation 52.7% → 71.9% (best run); test 47.8% → ≤68.0% (5 seeds) | confirmed | Missed: seeds that diverged to NaN are "excluded from mean ± s.d.", and the best 2-worker program "can overfit to validation outcomes". | 1109, 1128-1138 |
| 12 | Each cycle binds one falsifiable hypothesis to typed rubrics (§1.3) | confirmed | | 310-314, 320-322, 1965-1966 |
| 13 | "candidates are scored by evaluators the agent cannot edit" (§1.3) | corrected | This holds only in some tasks. Where it holds, it is enforced either by guarded files the harness rejects edits to (Doc-to-LoRA) or by a frozen evaluator (learned optimization). But the GRPO agent "modified the test-time evaluation procedure itself", and nothing flagged it. The CMA-ES spec describes itself as "a cooperative research-code contract, not an adversarial sandbox". | 6701-6702, 6722, 7345-7349, 1224-1234, 7489-7490 |
| 14 | Search and final evaluation use disjoint data (§1.3, §2.2) | confirmed | Caveats: the final evaluator is optional; the alignment judge checks for disjoint data only in drafted tasks; Doc-to-LoRA has no final plane at all. | 210-219, 236-237 |
| 15 | "every claim in the output must resolve to a frozen artifact" (§1.3) | corrected | The paper says *quantitative* claims resolve to aggregate outputs and raw artifacts. Its link checks test that a link resolves, not that the source supports the claim. The claim-to-source map does not cover idea provenance; the paper lists that as future work. | 390-391, 6200-6201, 1410-1412 |
| 16 | Abstract: autonomy "depends not only on base model capabilities, but also on the cross-agent orchestration layer" | confirmed | | 29-30 |
| 17 | §5: "the underlying model matters more" than the harness | confirmed | Measured on AI-reviewer scores. | 654-655 |
| 18 | §6.3: the base model "can have a significant impact on the idea investigation phase"; the question is addressed only partially | confirmed | The full sentence ends "…including both final performance and search costs." | 1211-1220 |
| 19 | No rubric covered evaluation integrity, so 2 of 3 Pi runs changed the test protocol and no gate flagged it (§1.4, §4.3) | confirmed | Example: k-sample majority voting replaced the baseline's pass@1. A manual post-hoc audit found it. The dossier's account is incomplete; see #121. | 1224-1234 |
| 20 | Shared memory speeds up search; its effect on the final best score is not significant (Fig. 17) | confirmed | The paper adds a "higher mean best-program score", a narrower gap between workers, and "substantial … inter-run variance". | 1278-1286 |
| 21 | Two workers reach the one-worker peak in under half the wall-clock time; more workers add nothing (Fig. 15) | confirmed | Evidence is one task (GRPO), with 1, 2 and 4 workers and 3 seeds each. The paper says more workers "does not necessarily yield better final results". | 1159-1169, 1206-1210 |
| 22 | Removing the figure critics lowers faithfulness (Table 4) | confirmed | Faithfulness 32.0 → 25.2; Overall 37.5 → 31.8. | 1349-1351, 1360-1361 |
| 23 | "model quality is a second-order lever on performance" [I] (§1.5) | refuted | The paper says "the underlying model matters more" than the harness, and that the base model "can have a significant impact" on both final performance and cost. | 654-655, 1219-1220 |
| 24 | "deterministic Python owns geometry" (§3.6) (§1.5) | confirmed | From the Fig. 5 caption. | 441-442 |
| 25 | The released code promotes any correct, strictly better candidate even if its rubrics fail (§1.7, §2.3) | confirmed | This is the paper's documented design: rubric completion and best-program updates "are therefore independent decisions", and the aggregator picks the "best correct program". The code itself was not checked. | 256-257, 330-333 |
| 26 | "In the paper, the evaluator measures the real thing"; the final plane "must change the model world, not just the random seed" (§1.8) | corrected | The paper's final planes already change the data or environment, not only the seed: CIFAR-10 for search vs SVHN for final; disjoint HPO task IDs; chronological partitions; different tables. The HPO task also scores against "continuous XGBoost surrogates", and the paper notes that "surrogate benchmarks do not establish real-training performance". | 6723-6725, 6789-6791, 6797-6798, 6846-6847, 6879-6881, 7206-7207 |
| 27 | A read-only ideation agent runs, then an execution agent (§2.1) | confirmed | "Read-only" is a protocol requirement stated in the prompt. | 309-319 |
| 28 | Fields of `idea_bundle.json` (F.2) | confirmed | | 6246-6252 |
| 29 | At least one metric rubric and one implementation rubric; snake_case IDs | confirmed | `target_rubrics.json` must be identical to the bundle's rubric array. | 6254-6256 |
| 30 | Records are normalized; "any missing fields or mismatched rubric identifiers are rejected" (§3.3) | confirmed | | 322-323 |
| 31 | The ideation agent may not run Bash, Python, pip or the evaluator (F.2) | confirmed | | 6258-6264 |
| 32 | Execution agent: append-only `program_<idx>`; only `evaluate.py`; no ad-hoc Python, notebooks, pytest or SciPy; `rubric_status.json` after every evaluation (F.3) | confirmed | | 6335-6341, 6359-6367, 6415-6417 |
| 33 | Because intent and evidence are separate artifacts, "Conclusions therefore cannot be rebuilt after the fact from the conversation" (§2.1) | corrected | The paper's rationale is that "the execution agent does not have to reconstruct its intent from conversational context." Reading this as a guard against post-hoc rationalization is the dossier's inference. App. A does say the ideation agent fixes the target rubrics before execution. | 324-326, 1986-1987 |
| 34 | Contents of the task spec (§3.1) | confirmed | | 209-223 |
| 35 | The alignment judge checks that the evaluators are independent and use disjoint data (§3.1) | confirmed | | 236-237 |
| 36 | HPO planes table (App. G.1.2) | confirmed | The table also sets memory limits of 32 GiB (search) and 64 GiB (final). | 6833-6836 |
| 37 | "non-tradeable gates"; failed or missing episodes keep a worst-case value; dropping them is a review failure (`validate_task_design.md`) (§2.3) | not in paper (repo) | The phrase is not in the paper, but the task specs say the same thing: "Failed cells contribute zero; never drop or renormalize them"; "never drop them from aggregates"; "fixed worst loss". | 6684-6686, 6740, 6807-6808, 7104, 7483 |
| 38 | The two independent gates, as quoted (§3.3) | confirmed | | 330-333 |
| 39 | The promotion expression in `campaign_loop.py` (§2.3) | not in paper (repo) | Consistent with l.330-333. | — |
| 40 | "These workers lease cycles from a synchronized queue" | confirmed | Fig. 3 calls it a "Dynamic Queue". | 249, 293 |
| 41 | Each worker's local best program works like a per-worker beam | confirmed | | 249-251 |
| 42 | At cycle start a worker imports shared memory and conclusions; at cycle end it publishes; logs stay local | confirmed | | 251-254 |
| 43 | Pruning archives the history and resets; the incumbent is carried forward | confirmed | The dossier omits that the GRPO runs pruned every 20 cycles. | 254-256, 7648 |
| 44 | `prune_every_n_cycles`, `_pruned/chapter_NNN`, and the warning about resets without containers | not in paper (repo) | | — |
| 45 | The aggregator merges histories and picks the best correct program | confirmed | | 256-258 |
| 46 | An append-only `memory.md`, a global markdown file and an "authoritative" JSONL log (§2.5) | confirmed | F.2 and F.3 call it "the authoritative cross-idea memory log". This overturns the earlier web log. | 6273-6285, 6369-6378 |
| 47 | Conclusions are forward-looking, a single paragraph of ≤300 words, with ≤3 validation retries (§2.5, §6.7) | confirmed | F.2 reads "(single paragraph, ≤300 words, ≤3 retries on validation failure)". The earlier log's "3 attempts total" comes from the repo skill file. | 6231, 6288-6291 |
| 48 | `memory.md` headers; "qualitative thresholds, no exact numbers"; "otherwise skipped"; trigger meanings (a) contradiction, (b) new category, (c) flip, (d) refinement; re-confirmation excluded (§2.5) | not in paper (repo) | The paper names only an "(a)/(b)/(c)/(d) gate" and does not define the triggers. | 6288-6289 |
| 49 | Gate log format `gate=<…>; trigger=<…>; reason=…` | confirmed | | 6292-6293 |
| 50 | The selected program is instrumented with extra metrics | confirmed | | 343-345 |
| 51 | Ablations are proposed from the code diff; each "must isolate an innovation introduced by the selected program" | confirmed | The same agent also proposes baselines. | 345-347 |
| 52 | A separate agent filters proposals for relevance, feasibility and single-change scope | confirmed | | 347-348 |
| 53 | Controls run alongside, and results are aggregated across seeds | confirmed | Multiple seeds are optional: the evaluator "can be run for multiple seeds". | 349-353 |
| 54 | Post-hoc work is on the frozen program; proposals that retrain or alter it are rejected programmatically | confirmed | | 354-357 |
| 55 | Claims resolve to aggregate outputs and raw artifacts; the memory summary only guides interpretation | confirmed | The paper says "Quantitative claims". | 387-391 |
| 56 | Conclusion quote: "embedded in an orchestrated workflow that preserves evidence and tests claims" | confirmed | | 1372-1374 |
| 57 | The human role shifts to specifying the contract: task, evaluators, rubrics | confirmed | | 1387-1389 |
| 58 | AI Scientist-v1 extended its time limits; this system changed the protocol in some RL runs | confirmed | | 1389-1391 |
| 59 | Agents can follow the contract too literally | confirmed | | 1392-1393 |
| 60 | Autonomous campaigns screen directions cheaply; human steering turns them into verified contributions | confirmed | | 1398-1399 |
| 61 | Table 6 rubric ablation | confirmed | No seed counts or repeats are reported. | 2111-2129 |
| 62 | Task setup: purpose, inputs and outputs; design agent → review → drafting agent | confirmed | | 188-235 |
| 63 | "three blind design judges, with an adjudicator who rules only on minority findings", placed in the §3.1 / Fig. 2 stage (also mapping row 2 and §6.7) | not in paper (misattributed) | The paper has one review: "an independent review agent assesses the design and repairs any issues". | 194-195, 232-233 |
| 64 | Contract check and smoke tests; alignment judge; full production check | confirmed | The production check applies only "In containerized runs". | 235-240 |
| 65 | Investigation inputs, outputs, agents and verification (schema, evaluate + verify as one atomic pair, cap, two gates) | confirmed | The cap is a rule in the prompt, which the agent checks itself. | 315-333, 6343-6350, 6412-6413 |
| 66 | Failure handling and advance logic (§3.1, §3.2): same-fingerprint rule; separate repair and infrastructure budgets; recovery snapshot; idea-generation retry then exit 2; one attempt, never retried; typed exit codes; "degraded" phases; review may edit only the manuscript; terminal checkpoints | not in paper (repo) | The paper says only "Failed scaffolds are repaired, and only versions that pass all checks proceed". Ablation agents are re-launched if they stop early. | 239-240, 6461-6463 |
| 67 | Retrospective evidence: inputs, outputs, agents; identical CSV schemas | confirmed | | 343-361, 6495-6513 |
| 68 | "post-hoc work restricted to existing artifacts" (§3.1); mapping row 10 "artifact-only" | corrected | "Diagnostics may run new inference or analyze existing artifacts". An optional bootstrap stage "reruns the evaluator once". | 355-359 |
| 69 | Writing phase: inputs, outputs, agents, verification | confirmed | The file names `paper_data.json` and `claims_grounding.json` are repo-only. The paper also has a gap-analysis agent and a post-draft planner. | 387-408, 6187-6205 |
| 70 | The meta-controller is a set of mechanisms, not a learned planner | confirmed | The term appears only in the abstract. | 19, 245-258 |
| 71 | Preset and README budgets: 20 idea cycles; 2 evaluations per attempt; 3,000 s and 21,600 s timeouts; 1 vs 5 replications; 3 post-hoc analyses; 1 review round; 7,200 s deadlines | not in paper (repo) | The paper's own runs differ: 1 evaluation per idea (CMA-ES, GRPO), and a 6-hour budget for CMA-ES. | 7517, 7521, 7647 |
| 72 | Table 3 compute per task | confirmed | The paper calls it the "Search iteration budget". | 608-641 |
| 73 | N × `gpu_count` rule; GPU-match check; run_id / snapshot / resume; `events.jsonl`; ESTALE retries; GPU quarantine; 64 KiB / 4 KiB caps; exit 87; `cost_events.jsonl` | not in paper (repo) | The closest paper text: checkpoints "bind config, program, evaluator, dependency, and reference identities", and resume happens "only through the supplied campaign tools". | 7522-7523 |
| 74 | The GRPO default is 2 workers | confirmed | | 1277-1278 |
| 75 | The writing loop alternates deterministic checks with agent audit | confirmed | | 401-407 |
| 76 | Sandbox details (§3.3): Docker per phase; API-key forwarding; no shared filesystem and RPC rules; repair authorizations; `--allow yolo`; host networking; README injection warning; OpenAI consent | not in paper (repo) | The paper says only that cycles are "containerized"; GRPO ran "Containerized (Docker, CUDA 12.8), Slurm-submitted". The task specs restrict what the RPC exposes and say to treat upstream text "as untrusted". | 246, 7651, 6886-6888, 6874-6875 |
| 77 | Candidate code runs "in a killable, resource-limited subprocess" isolated from evaluator data (F.5), listed as a protection (§3.3) | corrected | This is an instruction *to the task-drafting agent*, not a guarantee the harness enforces. CMA-ES is "cooperative … not an adversarial sandbox", and agents used "general web access" during investigation. | 6619-6620, 7489-7490, 1435-1436 |
| 78 | Variant kinds: control, ablation, baseline; repair only the rubrics that failed (F.4) | confirmed | | 6478-6494 |
| 79 | `variant_select` / `posthoc_select` acceptance and rejection lists; "Zero accepted is valid"; post-hoc rejects "any evaluator re-run" | not in paper (repo) | The paper's filter is "relevance, feasibility, and single-change scope", and the paper allows one bootstrap evaluator rerun. | 347-348, 358-359 |
| 80 | F.1 bibliography retrieval: 6–10 queries; ≤25 results per query; OpenAlex and scholarly fallbacks; 8–15 references; key validation | confirmed | | 6188-6201 |
| 81 | Writer rules (`paper.md`), audit checklist (`evidence_audit.md`), reviewer schema (`review_json.md`) | not in paper (repo) | The paper says the audit runs every round on a read-only copy and flags overclaiming or contradiction, and that an optional reviewer "may ask the writer agent to narrow or qualify claims". | 405-408 |
| 82 | AI-reviewer proxy: five o4-mini reviews plus an area chair; 1–10 Overall score | confirmed | The paper calls it a proxy, "not as ground-truth evidence of full scientific correctness". | 643-650 |
| 83 | autoillustrate's six phases: plan; style; render; VLM audit; compose and export; enhance then verify (§3.6) | corrected | The paper's numbering: Phase 2 = rendering, Phase 3 = panel inspection, Phase 5 = enhancement, Phase 6 = verification (Stage A by VLM, Stage B by unit tests). Planning and styling come before Phase 2, so styling is not its own phase, and enhancement and verification are separate phases. | 442-445, 6085-6089 |
| 84 | Panels are rendered in parallel as draw.io, from templates whose coordinates come from LLM-written Python; each panel gets a VLM audit | confirmed | | 421-430, 442-444, 2019-2021 |
| 85 | If no enhanced candidate verifies, the pipeline falls back to the deterministic render | confirmed | | 435-437, 444-445 |
| 86 | PaperBananaBench Overall 37.5 vs 25.0 under the GPT-6-Astra judge (Table 4) | confirmed | | 1340-1341, 1358-1366 |
| 87 | Under Gemini-3.1-Pro, PaperBanana (Claude + GPT Image 2) ranks first, 56.5 vs 50.0 (Table 8) | confirmed | | 6093-6098, 6116-6124 |
| 88 | Trade-off table: "2 workers are best on wall-clock; no gain beyond"; mapping row 3: "Fig. 15 shows no gain beyond 2" | corrected | The paper says two workers reach the one-worker peak in under half the wall-clock time, and more workers "does not necessarily yield better final results". Only 1, 2 and 4 workers were tested, and no costs are reported for worker scaling. | 1164-1169, 1206-1210 |
| 89 | Codex kept strictly to the prompt; Pi "showed initiative" but violated the protocol in 2 of 3 runs | confirmed | "Initiative" is the dossier's gloss. The paper also says Pi was faster, more consistent, 75% cheaper, and generalized better to the test set. | 1215-1219, 1224-1235 |
| 90 | SAE trade-offs (error down 28.8–53.8%, about 40× the fit time, worse perturbation metric); tabular trade-offs (0.606 → 0.778 balanced accuracy, 0.781 → 0.766 accuracy) | confirmed | The tabular sealed result uses a single seed; the paper says that "does not establish seed robustness". | 2041-2049, 1405-1407, 7183 |
| 91 | GRPO gains re-implemented DAPO clip-higher, Dr. GRPO and GSPO | confirmed | The paper calls these "not independent rediscoveries": the agent "had in principle access … through web search". | 1139-1150 |
| 92 | The ranking depends on the judge (Tables 4 and 8) | confirmed | | 6094-6101 |
| 93 | Humans corrected the ED-PPO overclaim | confirmed | | 551-553 |
| 94 | ED accuracy: 96.7% on MNIST, 61.7% on CIFAR-10 | confirmed | | 519-521 |
| 95 | At a fixed model the harness effect is minor; "No harness is uniformly best" (also §7: "harness matters little") | confirmed | Measured on reviewer scores. | 654-658, 1379-1380 |
| 96 | Newer model releases score higher, with a stronger trend for Claude models | confirmed | +1.34 vs +0.14 points per year. | 651-654, 674-675 |
| 97 | "Search score vs reviewer score — Positive on 4 of 5 tasks" (Fig. 9) | corrected | Fig. 9 plots *final task performance* percentile against reviewer score. Learned optimization has a slope of −0.03. | 724-728, 830, 872-875 |
| 98 | Kimi-K3 + Pi ≈ Opus-4.7 + Claude Code at about 75% lower API cost; Pi changed the protocol in 2 of 3 runs, found by manual audit | confirmed | Pi stayed faster and more consistent "After excluding protocol-violating programs". | 1215-1217, 1234-1235 |
| 99 | "The paper reports no totals in USD, only relative statements" (§4.1) | corrected | The right-hand panel of Fig. 16 plots "cumulative cost (USD)" per cycle on a 0–400 axis. No totals are tabulated. | 1262-1273 |
| 100 | Relative costs: Pi 75% cheaper; autoillustrate costlier and slower; removing critics roughly halves runtime; low effort about 30% faster again | confirmed | | 1216, 1352-1357 |
| 101 | App. A cites a study: 59% of expert reviews of agent manuscripts that an automated pipeline had accepted flagged fabricated or unsupported claims | confirmed | Ten manuscripts (Gaddipati et al., 2026). | 2001-2003 |
| 102 | Table 1: v1 not submitted; v2 workshop acceptance; this system co-scientist conference acceptance | confirmed | | 97-103 |
| 103 | Critics: faithfulness 32.0 → 25.2 | confirmed | | 1360-1361 |
| 104 | No experiment removes the orchestration layer at a fixed model | confirmed | The cross-agent comparison changes model and harness together, under the same scaffold. | 1211-1216, 1271 |
| 105 | Orchestration determines "how fast and cheaply" results arrive (§4.3) | not in paper | "Fast" is supported (workers, shared memory). "Cheaply" is not: the only cost evidence comes from changing the agent and model (Fig. 16), not from any orchestration ablation. | 1164-1166, 1215-1220 |
| 106 | ALIFE: "one rubric banned … and another required the positive and negative streams to stay distinct" (§5.1) | corrected | There is one rubric. It prohibits hidden credit assignment, and "This required the positive and negative streams to remain distinct". | 509-512 |
| 107 | Humans added the PPO-objective rubric for the RL experiments | confirmed | Humans also ported the best implementation and prepared the Brax and Craftax environments. | 524-529 |
| 108 | Humans verified results, references and claims; checked every BibTeX entry; added statistics | confirmed | | 538-555 |
| 109 | Reviewer feedback went into the camera-ready version | confirmed | | 577-587 |
| 110 | The agent ran the experiments and found modulo error routing and the stabilizers | confirmed | | 471-473, 514-520 |
| 111 | Human verification found an overclaim, unsupported citations and a missing archived reference | confirmed | | 551-558 |
| 112 | The human authors keep responsibility for methods, claims, authorship and disclosure | confirmed | | 457-458 |
| 113 | The learned optimizer stayed near chance on sealed SVHN; its edge came from one avoided divergence | confirmed | | 2036-2037 |
| 114 | The world-model evidence uses one seed per setting | confirmed | | 2055-2056 |
| 115 | "Task drafting failed on the larger tasks: world models and tabular (§8)" (§5.2) | corrected | §8 says drafting "may fail" to produce a matching scaffold for tasks like these. All five sweep tasks were prepared by hand, and no drafting runs on them are reported. | 1428-1432, 596, 6716-6717, 6864-6865, 7072-7073, 7197-7198 |
| 116 | Four human touchpoints (Fig. 7) | confirmed | The touchpoints include hands-on porting, environment setup and extra experiments. | 492-508 |
| 117 | A claim-to-source browsing interface is future work | confirmed | | 1459-1462 |
| 118 | Workers: 1, 2 and 4 tested; 2 is the GRPO default (§6.7) | confirmed | | 1160-1162, 1277 |
| 119 | "Cycles per campaign: 20 (preset); 30–50 in case studies" (§6.7) | corrected | The case studies used **20–60** cycles: ED 20, 60, 60 and 30; Doc-to-LoRA 40; CMA-ES 30; GRPO 50. | 7539, 7244, 7397, 7645 |
| 120 | "Evaluations per attempt: 2" (§6.7; mapping row 5: "cap of 2") | corrected | The paper's case studies allowed exactly **1** evaluation per idea (CMA-ES, GRPO). 2 is the repo preset. | 7517, 7647 |
| 121 | KPI: "Undetected protocol violations — Paper: 2 of 3 runs for one agent" (§6.8) | corrected | Violations also occurred in the **Opus-4.7 + Claude Code** runs without shared knowledge (Fig. 17). §8 speaks of "a subset of RL fine-tuning runs". | 1320-1322, 1390-1391 |
| 122 | KPI: "AI-reviewer vs human-IC rating correlation — Paper r = 0.44" (§6.8) | corrected | The r = 0.44 relates *task-performance rank* to AI-review rank. The paper reports no statistic for agreement between AI and human reviewers. | 725-728, 647-650 |
| 123 | Judges from several model families, as the paper suggests (§7) | confirmed | "Reviewers drawn from several model families to dilute the circularity". | 1423-1425 |
| 124 | "Assign failed paths the worst case rather than dropping them [S]" (§7) | confirmed | The task specs require this, but the paper's own Figs. 14 and 16 drop NaN seeds from the mean ± s.d. | 6740, 6807-6808, 7483, 1109, 1256-1257 |
| 125 | Rubrics catch only what they list (§8, risk 2) | confirmed | | 1221-1224 |
| 126 | "Over-literal agents [S] … Unless an action is named in the action space, agents may never explore it" (§8 risk 3; §3.7) | refuted | Codex "followed the task prompt instructions (Section G.5) more strictly", and G.5 said "Do NOT perform hyperparameter tuning, grid searches…". The Pi case shows the opposite: agents *do* explore actions nobody named. | 1217-1219, 7663-7665, 1224-1232 |
| 127 | "The paper's optional review phase sends the manuscript to OpenAI [S]" (§8, risk 7) | not in paper (misattributed) | This is the repo's `review` phase. The paper's §5 proxy reviewer is o4-mini, and the paper says nothing about consent. | 643-648 |
| 128 | The paper's §8 limitations list (§8, risk 10) | confirmed | The list omits "coding agents leverage general web access to inform idea investigation" and the autoillustrate failure cases in E.3. | 1427-1445, 6106-6111 |
| 129 | Turning rubric criteria into automated tests is future work | confirmed | The paper adds "checked for reward hacking, and complemented by independent scientific review". | 1463-1465 |
| 130 | The trigger definitions come from the repo skill, not the paper (§9, Q8) | confirmed | The F.2 prompt invokes the "(a)/(b)/(c)/(d) gate" but never defines it. | 6288-6289 |

---

## Missed or under-weighted mechanisms

These are relevant to an agentic portfolio laboratory: a deterministic engine, agent-proposed policies, counted evaluations, ablations, IC memos with claim-to-source validation, and IC support. Most of them sit in App. G, the task specifications, which the dossier did not read.

### A. Trust boundary: what the evaluator owns, and what never counts as evidence

1. **The evaluator owns data access, budget enforcement, integrity checks and scoring; the candidate owns the research components.**
   - Evaluator code, reference method, resources and score "stay frozen" (l.6701-6702, l.6722).
   - "The evaluator owns accounting." It deterministically rejects malformed, duplicate, out-of-bounds, non-finite and over-budget outputs (l.6806-6808).
   - In the tabular task the evaluator owns preprocessing, labels, splits, comparisons, scoring and controls (l.7222-7223).
   - *Lab:* the engine counts evaluations and rejects invalid policies. Agents never do this accounting.
2. **What a candidate reports about itself is never evidence.**
   - "candidate self-reports do not certify compliance" (l.6677).
   - "reported update counts do not prove training stability or learning" (l.6937-6938).
   - Counters and digests from candidate code are "unverified declarations" and "never determine scientific correctness" (l.7223-7230).
   - "GPU activity alone does not prove learning" (l.6943).
   - *Lab:* constraint flags, run counts or hashes that an agent reports are diagnostics only. IC evidence must come from engine-side logs.
3. **The harness enforces guarded files.**
   - `program_spec.toml` declares guarded checks, and "the harness rejects candidates that edit or bypass them" (l.7345-7349).
   - The evaluator strips ambient environment variables and injects the benchmark values itself (l.7335-7337).
   - *Lab:* guard the engine, the beliefs, the scenario generator and the cost models this way. Guarded files are stronger than a rubric because the agent cannot talk its way past them.
4. **Isolation in the paper is cooperative, not adversarial.**
   - The paper says so directly (l.7489-7490).
   - Agents used general web access during investigation (l.1435-1436, l.1142-1144).
   - The drafting agent is allowed network access (l.6591).
   - *Lab:* isolation has to be enforced by infrastructure, not by prompts.
5. **The per-attempt evaluation cap is a rule in the prompt that the agent checks itself** (l.6412-6413, l.6565-6566).
   - It counts calls, not folders, including failed runs and retries (l.6347-6349).
   - An attempt stops at the first all-rubric pass (l.6346).
   - *Lab:* count evaluations at the engine. Decide deliberately whether a rubric pass should stop optimization.

### B. Leakage and hygiene of the data planes

6. **Chronological partitions with embargo gaps.**
   - Training uses `[0, 0.6N)`, search `[0.6N+64, 0.8N)` and final `[0.8N+64, N)`. "The 64-frame gaps prevent boundary windows from leaking" (l.6879-6882).
   - This transfers directly to time-series simulation: put an embargo between the calibration window and the sealed window.
7. **Each plane has its own private resource tree and caches** (l.6883-6885).
   - Final smoke tests use synthetic fixtures and never open the final data (l.6767).
   - Final environments and seeds are excluded from search, tuning, calibration *and retry* decisions; hashes are frozen before execution (l.6670-6671).
   - "Never use final cases for tuning, calibration, memory, or promotion" (l.6798). Memory is named explicitly.
8. **Interfaces are anonymized.**
   - Not allowed: "identity-keyed behavior, fixed replay, lookup answers, hidden optima, and future access" (l.6803-6805).
   - No branching on a known task identity (l.7461-7462).
   - No access to dataset identities (l.7171-7172).
   - *Lab:* present scenarios and regimes to policies anonymously, so a policy cannot key on "2008" or "2020".
9. **Search exposes only bounded aggregate metrics and failure categories** (l.6825). This is the paper's control against adaptive overfitting of the holdout.
10. **Anytime / horizon-free constraint.** Decisions may not depend on a countdown, the budget or the horizon (l.7464-7468). *Lab:* this guards against end-of-horizon gaming.
11. **No synthetic stand-ins.** "Do not silently replace a required benchmark, evaluator, dataset … with a synthetic stand-in. If blocked, exit non-zero" (l.6593-6594). See also l.6799-6800 and l.6918-6919.

### C. Statistical design of gates and claims (the paper has more than "strictly higher")

12. **`correct` already contains the non-negotiable constraints, including non-inferiority in every family.**
    - HPO: `candidate_family_mean >= starter_family_mean - 0.01`, alongside legality, budgets and no leakage (l.6820-6822).
    - SAE: loss recovered within 0.02 of the stronger reference (l.7101-7102), and a score aggregated as the **minimum across families** (l.7102-7103).
    - *Lab:* require non-inferiority to HOLD in every model world, and aggregate on the worst world.
13. **A tie keeps the incumbent** (l.6823-6824). This is the paper's own version of "tie = HOLD".
14. **Final claims need paired, pre-declared uncertainty.**
    - "checkpoints within a run are correlated, not independent replications"; "Search eligibility does not establish scientific superiority" (l.6826-6829).
    - Negative results are valid outcomes (l.6854-6855).
    - The CMA-ES evaluator reports a paired bootstrap interval, but ranks only on the point score (l.7509-7512).
    - SAE final correctness requires an improvement of more than 1e-4 relative "at every case" (l.7107-7108).
    - In short, materiality and uncertainty machinery exists at the final stage, but not at search promotion.
15. **Common random numbers are already in use:** "128 newly sampled tasks, shared across all 256 candidates as common random numbers" (l.7472-7473).
16. **Failure accounting.**
    - Never drop or renormalize failures (l.6684-6686, l.6740, l.6807-6808, l.7104, l.7219-7220).
    - Budget exhaustion is defined separately from execution failure (l.6685-6686, l.6743-6744).
    - **Counter-example in the paper's own reporting:** Figs. 14 and 16 drop NaN seeds from the mean ± s.d. (l.1109, l.1256-1257), and the "up to 68.0%" figure is reported under that exclusion.
17. **Correctness is kept separate from eligibility for an improvement claim.** A valid but non-winning final run records `correct=false` and `not_qualified`, and the process still exits successfully (l.6926-6933).
    - "Protocol validity alone does not establish improvement" (l.6712-6713).
    - This is the paper's own version of the lab's qualification label.
18. **Operating points declared in advance.** Compare Pareto frontiers "rather than selecting one favorable mean L0 after seeing results" (l.7020-7021); horizons are also declared in advance (l.6678-6679, l.6920-6926). *Lab:* declare several risk budgets and horizons up front, with no post-hoc picking.

### D. Controls and attribution

19. **Naive controls are mandatory, and a candidate must beat them at every horizon.**
    - Copy-last-frame and constant-velocity controls (l.6925-6926).
    - A hand-designed comparator frozen before search (l.6680-6681).
    - Permutation, placebo and reset controls (l.7029-7030, l.7153-7154, l.7216-7217).
    - *Lab:* run HOLD, pro-rata and static SAA at every horizon, plus a placebo policy fed shuffled signals.
20. **Attribution by an exact null control** (C.2).
    - With the learned part switched off, the anchor scores 1.107 against 1.191 for the full method. That is 55.8% of the margin over CMA-ES.
    - The learned increment "reverses sign on final solution quality" (l.2657-2663, l.2687-2700, l.3104-3117).
    - The abstract's "5 of 7 unseen" headline is therefore mostly scaffolding.
21. **Ablations show that winners carry harmful or useless parts.**
    - Removing the world model's constant-velocity initializer *improves* development results (l.2054-2055).
    - The tabular class-balanced loss has "no measurable benefit" (l.2046-2047).
    - Comparisons matched on query count rather than cost "do not establish superiority" (l.2066-2067).
22. **Fairness rules for ablation agents:** "Do NOT optimize beyond making the variant valid and analyzable"; "change ONLY the declared component"; "Do NOT invent additional experiments" (l.6559-6561).

### E. Selection bias and overfitting in the paper's own results

23. **GRPO.** The best 2-worker hyperparameters "can overfit to validation outcomes", and training diverges when the program is retrained independently (l.1135-1138).
24. **CMA-ES selection bias.** The generated C.2 paper says: "The eight-seed protocol used to report the headline was also used to select the configuration", giving "selection bias of unquantified size" (l.3089-3091).
    - Its conclusion is also "not robust to a modest change in horizon" (l.3087-3088).
25. **The validation environment shaped the CMA-ES program.**
    - The re-expansion mechanism "cannot fire during the 50-generation BBOB inner loop", which indicates "interplay between Ant-v1 validation and idea investigation" (l.1067-1068).
    - The transfer test was chosen after the drafted manuscript suggested it (l.1069-1071).
    - Yet §8 asks that transfer tests be "fixed before search and held out from it" (l.1421-1423).
26. **Doc-to-LoRA has no separate sealed or post-search evaluation.**
    - "Each configuration is one trained model evaluated once by the fixed benchmark" (l.2307).
    - The paper also reports a collapse instability (l.2316-2317).
27. **Protocol gaming happened across agents.** Crosses in Fig. 17 mark protocol-modifying evaluations in the Claude Code runs without shared knowledge (l.1320-1322). "neither deviation is apparent from the reported numbers alone" (l.1393-1394).
28. **Rubric pass rates "fluctuate" while the best score rises** (l.659-660, Fig. 9).
    - The final pick is the "best correct" program, not a rubric-passing one (l.256-257).
    - That sits uneasily with the abstract's "enforces rubric verification at each stage" (l.18-19).

### F. Writing, audit and governance signals

29. **Auditors should read logs and code, not just the paper.**
    - In audits of two open-source systems, an LLM auditor caught biased benchmark selection, post-hoc selection on test results and undisclosed synthetic data "far more reliably from logs and code than from the paper alone" (l.1976-1979).
    - The paper also cites Xcientist's audit of claim drift (l.1979-1982).
    - *Lab:* give the audit agent the run logs and the engine diff, not only the memo.
30. **Validation signals beyond AI review.**
    - AI reviewer scores "can potentially be overfit like any other metric" (l.1421).
    - The paper proposes independent reproduction behind each claim, and an idea-provenance map (l.1410-1412, l.1425).
31. **Agents never escalate.** "Never ask user questions. If info missing, make best reasonable assumption and continue" (l.6406-6408; also l.6304). *Lab:* give agents an escalation channel, and log every assumption an agent makes.
32. **Each claim type carries its own evidence requirement and scope.**
    - Example: a learned-state claim needs evidence that resetting the state changes outcomes (l.6709-6710).
    - "Scope conclusions to the tested configuration…" (l.6714, l.6972, l.7070-7071, l.7193-7195).
33. **Cache and reference identity is bound, and nothing is recomputed silently.**
    - Cache identity binds source, data, workload, runtime image and hardware (l.6915-6917).
    - "Missing, stale, corrupt, or incomplete caches stop evaluation; they never trigger hidden retraining" (l.7210).
    - Evidence is reused only when identities match (l.6734-6735).
    - Smoke runs "cannot establish production qualification" (l.6962-6963).
34. **Responsible deployment** needs sandboxing, provenance for generated code and text, disclosure, watermarking and human accountability (l.1451-1453). The generated papers are watermarked (l.2031).

---

## Mapping-table issues

Issues with dossier §6.1, rows 1–20, and related KPI and parameter rows.

| ID | Row | What the dossier says | What the paper actually does |
|---|---|---|---|
| M1 | Row 2: "3 blind judges plus an adjudicator" | Cites §3.1 as the source. | The paper uses **one** independent review agent that both assesses and *repairs* the design, plus one alignment judge (l.194-195, 232-233, 236-237). The multi-judge design is repo-only, and the paper offers no evidence about how many judges to use. The lab may still adopt it, but not as a mechanism the paper validated. |
| M2 | Row 5: "the agent cannot touch the engine"; "a cap of 2 evaluations per attempt" | Treats the cap and engine immutability as transferable controls. | The cap is a self-checked rule in the prompt (l.6412-6413), and the case studies used **1** evaluation per idea (l.7517, 7647). The engine was immutable only where guarded checks were declared (l.7345-7349). In GRPO the scored evaluation procedure could be edited and was gamed (l.1224-1234). What should transfer is counting at the engine plus rejection of guarded-file edits, not the prompt rule. |
| M3 | Row 6: the two gates, "the paper's 'strictly higher'", "Must not transfer: promotion when the rubrics fail" | Treats rubrics as the gate the paper skips. | The paper's non-negotiable constraints already live inside the evaluator-owned `correct` flag. In HPO that includes legality, budgets, no leakage and per-family non-inferiority (l.6820-6822). Rubrics are the layer the agent verifies itself, and they double as a stopping rule for the attempt (l.6346). The lab's "gates passed" is therefore the paper's `correct`, not its rubrics. "Strictly higher" applies only to *search* promotion; final claims use paired, pre-declared uncertainty and materiality (l.6826-6829, 7107-7108, 7509-7512). The row is also internally inconsistent: it says "keep the gates separate" and then requires both for promotion. |
| M4 | Row 7 and §2.5: distilled conclusions become an "IC lessons ledger" / "institutional prior" | Presents a belief-revision protocol for institutional memory. | The paper's conclusions are per-worker, agent-written search heuristics used *within* one campaign "to bias toward directions previously found *promising*" (l.6231-6234). They are shared at cycle boundaries and periodically archived and reset by pruning (l.254-256). Nobody validates them, they do not carry across campaigns, and the trigger meanings are repo-only. The paper's only evidence about them is that sharing speeds up search (l.1278-1286). Mapping them to institutional memory overstates their epistemic status. |
| M5 | Row 3 and §6.7: 2–3 workers, including an "isolated challenger"; "no gain beyond 2" | Calls 3 workers a safe default. | Only 1, 2 and 4 workers were tested, on one task with 3 seeds; more workers "does not necessarily yield better final results" (l.1166-1167). A 3-worker setup is untested. In the paper, the configuration *without* shared knowledge is where Claude Code's protocol violations showed up (l.1320-1322). That is weak evidence, but it bears directly on an isolated challenger. |
| M6 | Row 10: post-hoc "artifact-only work" | Restricts post-hoc work to existing artifacts. | The paper allows new inference and one optional bootstrap rerun of the evaluator (l.355-359). Its actual constraint is no retraining and no alteration of the selected program. "Artifact-only" is a stricter repo prompt rule. |
| M7 | Row 11 and exec #8: the sealed final plane; "the evaluator measures the real thing"; "a new seed alone is not enough" | Implies the paper only reseeds the final plane and always measures reality. | The paper's final evaluator is *optional* (l.211, 217-219) and was absent for Doc-to-LoRA. Where it exists, it already changes datasets, environments or time partitions (l.6723-6725, 6790-6791, 6879-6881, 7206-7207). HPO evaluates against *surrogate* models (l.6789) and scopes its claims accordingly (l.6846-6847). The paper is therefore closer to "alternative model worlds" than the dossier says, and the "biggest conceptual gap" already appears in it. The paper's CMA-ES transfer test was also chosen after search (l.1069-1071), against its own advice to fix such tests first (l.1421-1423). Pre-registration needs to be explicit in the lab. |
| M8 | Row 16: the Docker sandbox; "killable subprocess; no shared filesystem with the evaluator" transfer | Lists these as paper protections. | The paper calls its own contract "cooperative … not an adversarial sandbox" (l.7489-7490). The killable subprocess is an instruction to the drafting agent (l.6619-6620). Agents used web access during investigation, and the drafting agent may use the network (l.1435-1436, 6591). The paper does not establish adversarial isolation. ADIC must design that itself. |
| M9 | Row 18 and the KPI in §6.8: the AI reviewer; r = 0.44 used as an AI-versus-human benchmark, with "≥0.6" required | Uses r = 0.44 as a benchmark for agreement with humans. | r = 0.44 measures how AI-review rank tracks *task-performance* rank across 70 campaigns (l.725-728). The paper gives no figure for agreement with humans; it defers to Lu et al. 2026 (l.647-649). It also warns that AI review scores "can potentially be overfit like any other metric" (l.1421). The KPI benchmark is mis-specified. |
| M10 | Row 12: claim-to-source map; "every number resolves to …" | Treats link resolution as validation. | The paper's deterministic checks confirm only that citation keys and claim-to-source links *resolve* (l.6200-6201). Whether the source *supports* the claim is left to the LLM audit (l.405-407) and to humans. In the ALIFE paper, humans found citations that resolved but did not support the claims (l.555-556). The map also omits idea provenance (l.1410-1412). The lab should split "resolves" (deterministic) from "supports" (audit plus human). |
| M11 | Row 1: "Transfers: the typed, versioned, hashed spec" | Implies agentic task drafting is validated. | Every reported task was prepared by hand and run *without* the drafting phase (l.596, 6716-6717, 6864-6865, 7072-7073, 7197-7198). The paper says drafting "may fail" on larger tasks (l.1428-1432). The empirical evidence is for human-authored specs, which supports "the IC owns the spec". Agent drafting is not validated. |
| M12 | Row 9: diff-based ablations plus Shapley | Presents Shapley attribution as the analogue of the paper's ablations. | Shapley is the lab's own addition. The paper's strongest attribution tool is the exact switch-off null control in C.2 (l.2687-2700, 3081-3083), and its fairness rule for ablation agents ("Do NOT optimize beyond making the variant valid", l.6559-6561) should transfer. The mapping omits both. |
| M13 | Exec #7: "promotion of a candidate without passing its gates" | Calls it a code defect. | This conflates rubrics with gates. Promotion still requires the evaluator-owned correctness gate (l.331-332), and leaving rubrics out of promotion is documented design, not a defect. |
| M14 | §6.6: the four human touchpoints map to Specify / Steer / Verify / Revise | Treats human steering as specification. | In Fig. 7 the humans also did engineering: they ported the best nodes, set up the RL environments and ran extra experiments for the camera-ready (l.492-497, 524-526). Steering in the paper included human implementation work, not only new contract versions. |

---

## Overall reliability

**Medium.** The rating differs by layer.

| Layer | Reliability | Why |
|---|---|---|
| Numeric results quoted from the paper | **High** | No refuted numbers. One mislabel (Fig. 9) and one omission (the USD axis in Fig. 16). |
| Description of mechanisms | **Medium** | Solid on F.2–F.4 and §3. But it mixes repo and paper without always saying which is which, misattributes the three-judge design and the OpenAI review phase to the paper, overstates evaluator immutability and sandboxing, gets the case-study settings wrong, and did not read App. G.1.5–G.5. |
| Design mapping to the lab | **Medium-low** | Five rows misrepresent the paper's mechanism (M2, M3, M4, M7, M9). One KPI uses the wrong statistic. Two "[S]"-tagged generalizations are contradicted by the paper (#23, #126). |

**Before the dossier is used for design, it should:**
- fold in Missed §A–§E, especially evaluator-owned accounting, guarded files, embargoed chronological splits, non-inferiority inside `correct`, naive and placebo controls, and the C.2 attribution result;
- fix M2, M3, M4, M7 and M9.
