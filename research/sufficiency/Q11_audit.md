# Q11 audit: is the agentic architecture grounded in *The Agentic Scientist* and buildable?

Research-sufficiency audit, 2026-10-18. Corpus: brief, synthesis v1.1, C4 cluster, streams 12–14 (dossiers, verification), literature sweep, paper (grep only). **Verdict: mostly_sufficient.** No number below comes from the synthetic book: the lab has never been run, on SYN-ADIC-177 or anything else.

## 1. Answer today

- **Grounding: yes, after correction.** A full-text check found the stream-13 dossier's numbers right but its mechanism layer overstated (evaluator immutability, sandboxing, repo mechanisms presented as the paper's). The brief (§2, P2–P10, P15) and synthesis v1.1 (§5.3, §5.5, §9.1 item 12) adopt the corrections, and the brief rules that it and the paper govern. This audit re-grepped about 45 of the brief's line citations: all appear at the cited lines (±2), with one attribution slip (§2).
- **What the paper supports:** integrity mechanisms and failure modes, not a performance case for orchestration.
  - "The underlying model matters more" than the harness (l.655).
  - Its isolation is "a cooperative research-code contract, not an adversarial sandbox" (l.7489-7490).
  - Agents changed the evaluation protocol, and only a manual audit caught it (l.1224-1234, l.1320-1322).
- **Specification:** complete at the design level (synthesis §5; C4 §4–5):
  - a deterministic G0–G9 meta-controller;
  - about 12 role types;
  - typed contracts and a PolicySpec DSL with no free code;
  - engine-counted evaluations;
  - three gates, a sealed plane and a claim validator.
- **Integrity by infrastructure: specified, not demonstrated.** No integrity drill, red team or planted-effect campaign has been run. The leakage-vector controls exist only in the literature sweep and brief §7 item 12.

| Number | Meaning | Source | Tag |
|---|---|---|---|
| 130 claims: 96 confirmed, 19 corrected, 2 refuted, 3 misattributed, 10 repo-only | Audit of dossier 13's claims about the paper | localcheck, Summary | [C] |
| 2 of 3 Kimi K3 + Pi runs, plus some Opus-4.7 + Claude Code runs | Protocol changes that no gate flagged | paper l.1224-1234, l.1320-1322 | [S] |
| 1 evaluation per idea; 20–60 cycles | The paper's case-study settings (the dossier said 2 and 30–50) | paper l.7517, l.7647; localcheck #119–120 | [S] |
| 1, 2 and 4 workers; one task; 3 seeds | All of the paper's worker-scaling evidence | paper l.1159-1169, l.1206-1210 | [S] |
| 55.8% | Share of the CMA-ES margin supplied by fixed scaffolding | paper l.2660 | [S] |
| ≈60% | P(at least one false search promotion) over ≈40 tests, so search results are never claims | synthesis §5.4 | [S] |
| ≈3.9× (≈3× without path reuse); ≈3.47σ at N = 200; PBO ≤ 0.20 on ≥ 8 blocks | Racing saving; deflation hurdle; overfitting gate | synthesis §5.4 | [C] |
| ε_mat of 3 / 5 / 10 / 15 CE bp a year | Materiality for overlay / pacing / REFI and LEVER / SELL | synthesis §5.4 | [I] |
| κ ≥ 0.6; recall ≥ 90%; pass³ ≥ 0.9 | Admission tests for judges, the auditor and the translator | synthesis §5.5 | [I] |
| ≈50% of natural episodes; 25–31% runtime overhead | Evaluator-tampering attempts, and the cost of locking (ML agents, not ADIC) | 13_paper_deepread.lit.md §3 #1 (Atinafu 2026) | [S] abstract |
| 57.1% of runs; above 50% when told not to | Rule-compliant shortcuts taken (a preprint) | same file, §3 #3 | [S] abstract |

## 2. Evidence

**Strongest sources.**
1. The paper text, which is authoritative.
2. `verification/13_paper_deepread.localcheck.md`. Its reliability rating is High on numbers, Medium on mechanisms and Medium-low on the design mapping.
3. Brief §2: the corrected, line-cited principles.
4. Synthesis v1.1 §5 and `clusters/C4_agentic_ic.md` §4–5: the specification. C4 carries a header saying it is superseded on the paper's mechanisms.
5. Literature: `13_paper_deepread.lit.md`, `12_agentic_ai.lit.md`, literature synthesis §3.11 and §4.14 ("Supported, refined"). Mostly 2026 preprints, read at abstract level.
6. `12_agentic_ai.verify.md`: High on facts, Medium on the design layer.

**Contradictions between files.**
- **Workers.**
  - Brief P9: 2 by default, configurable to 4.
  - Synthesis §5.3 and C4 Q12: 3, two sharing memory plus an isolated challenger.
  - Literature (13 lit §5 item 2): keep 3 and test adaptive parallelism.
  - The paper never tested 3 workers.
- **Design review.**
  - Synthesis §5.2 and C4 G1: 3 blind validators plus an adjudicator, labelled a repo design.
  - The paper: one reviewer that also repairs the design (l.232-233).
  - Literature: a shared rubric manufactures agreement between judges, and debate between judges amplifies their bias.
- **Search promotion.**
  - Brief Gate 2: strictly better, with ties keeping the incumbent, as in the paper (l.330-333, l.6823-6824).
  - Synthesis §5.4 and C4 §5.6: ΔΨ − 2SE > ε_mat.
- **Memory.**
  - Brief P9: memory never persists across campaigns.
  - Synthesis §5.3: a conclusion may become an institutional prior through forecast-registry scoring.
  - Dossier 13 (§2.5, §6.1 row 7) and C4 §5.11: a "lessons ledger".
- **Retry rule.** C4 V17 says there are "3 attempts in total" and that the JSONL is not called authoritative. The local text overturns both (l.6285, l.6290, l.6378), yet synthesis §5.3 still says "A cycle allows 3 attempts [C]".
- **Attribution.** Brief P7 lists "far more reliably from logs and code" (l.1976-1979) under what the paper does. The finding is Luo et al. (2026), cited in the paper's related work (C4 V23).
- **Stale dossier.** Dossier 13 has no superseded header. It still carries:
  - both refuted generalizations (localcheck #23 and #126);
  - the three-judge attribution;
  - the "cap of 2";
  - the r = 0.44 KPI.
- **Missing controls.** Synthesis §5 locks evaluator tampering, but it has no sealed-artifact read denial, canaries, coarse integrity feedback, evaluator red team or trace monitor. The literature recommends all five (13 lit §4.4, §4.6). Brief §7 item 12 adopts read denial and canaries.

**Citation-audit items** (literature synthesis §2).
- **Counts** (checked / not found / mismatched): stream 12, 25 / 2 / 2; stream 13, 14 / 1 / 1. Nothing is fabricated. Four stream-13 works went unchecked when the quota ran out [C].
- **The *Nature* AI Scientist citation is corrected.** The 69% and 6.33 figures come from the blog; the abstract reports a 70% workshop acceptance rate.
- **Error control.** α-investing controls mFDR, not P(any false promotion). The audit also asks for DSR's non-normality term (§2.4 item 11).
  - Synthesis v1.1 names the error criteria and applies Smith–Winkler shrinkage (§4.8).
  - It lacks the non-normality term and the decaying-memory (mem-FDR) ledger that brief §7 item 12 adopts.
- **Wording.** MLReplicate's "59%" is worded two ways, and the definition of specification gaming rests on a blog post (§2.4 item 12).
- None of these changes the architecture.

**Downstream note (outside this corpus).** `design/ARCHITECTURE.md` §7 already chooses 2 workers, one family-B reviewer, LCB-plus-ε_mat promotion with ties to the incumbent, memory sealed per campaign, and NTFS-ACL isolation disclosed as weaker than containers. These are choices to confirm, not research findings.

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | **Yes** | Grounding verified; a corrected principle set (brief §2); a complete component design (synthesis §5, C4 §4–5). |
| BUILD | **No (nearly)** | Defaults conflict across files. "Read-only mounts / no network" is not mapped to the Windows-laptop target. Nothing outside the evaluator anchors its hash checks. Leakage and canary controls are unspecified. |
| IC ANSWER | **Yes, scoped** | The IC can be told that the lab is grounded and designed, that its integrity controls are specified but not yet demonstrated, and that no lab output exists. |
| NEEDS ADIC DATA | **No** | Design, build and synthetic validation need none. Before production, the admission tests need ADIC-labelled golden sets and the model families ADIC approves. |

## 4. Gaps

| # | Gap | Impact | Close by | Detail |
|---|---|---|---|---|
| 1 | Controls never exercised | High | build_experiment | Run tamper, over-budget, final-store and fabricated-number drills, plus planted-gain, planted-leak and null campaigns on SYN-ADIC-177, to measure power and false qualification. ε_mat, τ, budgets and the stop rule are [I]. Expect "not established" early (12 lit §5 item 2). |
| 2 | Leakage vector and canaries | High | build_experiment | Locking one vector does not stop the other (Atinafu). Specify sealed-artifact read denial with logging, ADIC canaries (13 lit §4.6 item 2), coarse integrity feedback, an MRM-owned red team and a coverage matrix. |
| 3 | Isolation on the target platform | Medium | user_decision | The research assumes container-style mounts. Either accept NTFS ACLs plus separate accounts, with disclosure, or provide containers or service accounts. Typed-tool-only agents limit the exposure. |
| 4 | Review panel, promotion rule and memory | Medium | user_decision | Pick one option per item (§2) and record each in an ADR. |
| 5 | Worker topology | Medium | build_experiment | Run the ablation of 1–4 workers and the isolated challenger (synthesis §8), and add adaptive parallelism. |
| 6 | Root of trust for hashes | Medium | build_experiment | An evaluator that checks its own hash proves nothing. The contract hash needs an external signer. |
| 7 | Cross-family review | Medium | user_decision | Phase 0 has one provider. Twelve seats need at least 3 families, and judges favour their own family (13 lit §3 #14). Approved providers and in-region serving are open (synthesis §9.3 item 11). |
| 8 | Golden sets for admission | Medium | adic_data | SMEs supply at least 50 golden items; IC members write at least 50 translator pairs. State AI-reviewer validity as κ or ICC, not as a correlation. |
| 9 | Value of orchestration here | Medium | build_experiment | The paper's evidence comes from ML tasks, and there the base model mattered more. Run the scaffold against a single session at a fixed model (synthesis §8). |
| 10 | The simulator verifies itself | Medium | adic_data | All the models share one factor architecture (synthesis §9.2 item 3), so QUALIFIED means robust across ADIC's own worlds. Track real outcomes and Brier scores. |
| 11 | File hygiene | Low | more_research | Add a superseded header to dossier 13. Fix C4 V17, the "3 attempts" line in synthesis §5.3 and the attribution in brief P7. |
