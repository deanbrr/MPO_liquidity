# Checkpoint: ADIC Agentic Total-Portfolio Lab

Checkpoint taken 2026-10-18 at about 12:35 local time, because the session may stop. **Updated 15:30:** main research finished, design workflow launched (§3).

`orchestration/STATE_AT_CHECKPOINT.txt` is an auto-generated list of every research file that existed at checkpoint time.

## 1. How to resume in a new session
1. Read these, in order:
   - this file
   - `inputs/00_CONTEXT_AND_PRIOR_WORK.md`: client facts, the seven groups (§1A), the prior deck
   - `design/00_DESIGN_BRIEF.md`: R1–R15, P1–P15, design decisions 1–21
2. Re-list `research/` and compare it with `orchestration/STATE_AT_CHECKPOINT.txt` to see what finished after the checkpoint.
3. **Workflow runs cannot be resumed by run ID from a new session**: resume works only within the same session. Relaunch only the unfinished stages.
   - Use the scripts in `orchestration/workflows/`.
   - Change their orchestration to skip any stage whose output file already exists and is complete. Every stage writes to a fixed path, listed in §3.
4. **Consensus** (academic search; the user has a paid account): if `mcp__claude_ai_Consensus__search` is not available, ask the user to run `/mcp` and select "claude.ai Consensus". Rules:
   - run at most 3 searches at a time
   - apply no filters unless the user asks
   - cite the paper URLs exactly as returned
5. **Environment:** uv and Git are **not on PATH**, so call them by full path (see §5).

## 2. Requirements and user confirmations (all 2026-10-18)
- **ADIC:**
  - endowment-model fund, about $177bn
  - must distribute 5–10% of the fund a year to its sovereign owner
  - 10% nominal USD return target
  - leverage allowed
  - about 60% private, mostly PE, with declining DPI
  - large OTC derivatives overlay with two strategies: a tail-protection hedge and an opportunistic trading strategy
- **What to build:** a multi-period optimization framework that provides:
  - robust scenario analysis and probabilities of outcomes
  - a SELL / HOLD / REFINANCE / LEVER lens per strategy and asset
  - fusion of three return series per asset: underwritten, current actual, and the group's forecast
  - an agentic architecture inspired by *The Agentic Scientist* (arXiv 2610.18933)
  - IC discussion of the results
- **Eight investment groups.** Groups own holdings, forecasts, actions and budgets; decisions are judged at total-portfolio level. The user added **Real Assets** at about 17:40, after the seven-group research had finished.
  - **Confirmed by the user (2026-10-18):**
    - sectors: real estate, infrastructure, and energy & natural resources; not agriculture or timber;
    - access: funds plus co-investments and direct assets or JVs;
    - size: part of the ~60% private allocation.
    - The user also chose PE unfunded census v1.1 ($16.4bn). It was sealed for a $52bn PE bucket, so re-runs also report it rescaled to about $10.9bn.
  - No size was given. Working allocation v2 (context §1A) carves Real Assets ($18bn) out of PE funds ($52bn → $34bn).
  - Design brief §8 sets the interim rules.
  - Once Real Assets research lands, its integration memo must be applied to the group report, the main report and the design documents.
  1. PE: allocates to funds.
  2. Secondaries: a **hybrid of fund and direct investments** (confirmed).
  3. Capital Solutions: preferred and structured equity, NAV and fund finance, GP solutions, special situations (confirmed).
  4. Co-investment.
  5. Public Markets: hedge funds and long-only managers.
  6. Private Credit.
  7. Overlay.
- **Corporate Finance owns Treasury.** It is the internal bank and runs the whole funding and liability side (all confirmed):
  - liquidity buffer
  - portfolio borrowing and leverage facilities
  - overlay collateral (VM/IM)
  - distribution payments to the owner
  - liquidity gate, contingency funding plan and internal transfer pricing

  The seven groups run the asset side.
- **Synthetic returns are allowed.** They must always be labeled SYNTHETIC and generated from a known ground-truth process.
- **Action definitions (confirmed):**
  - REFINANCE = raise cash against a holding without selling it (NAV loan, preferred equity, recap).
  - LEVER = borrow to add exposure.
- **Distributions (confirmed):** the owner sets the annual rate within 5–10%, likely higher when oil is weak. It is an exogenous, stochastic liability, not a decision variable.
- **User-supplied blueprint** (`inputs/user_blueprint/`): treat it as a fifth design proposal. Design brief §6 has the assessment.
- **Governing motto (from the user's deck):** "LLMs accelerate evidence; deterministic models own numbers; humans own decisions."

## 3. State of the work
### Finished (committed)
- **Main research, 14 streams:**
  - dossiers: `research/dossiers/NN_key.md`
  - adversarial verification logs: `research/verification/NN_key.verify.md`
  - 4 cluster syntheses: `research/clusters/C1..C4*.md`
  - master synthesis: `research/00_SYNTHESIS.md` **v1.1** (256 KB, written 15:08, sections 0–11 complete). It integrates the group layer, the five gap addenda and fixes for all 13 critic contradictions. A v1.0 backup is in the session scratchpad.
  - critic → 5 gap addenda: `research/addenda/gap_01.md`–`gap_05.md`, plus `gap_NN_calcs/`:
    - 01: HF liquidity ladder / swap
    - 02: Tier-1 feasibility, Phase I, `test_no_pinned_duals.py`
    - 03: overlay position and Greek layer
    - 04: F_t stress filter and initial state
    - 05: return bridge and v8 rerun
  - `gap_02_calcs/gap02_grid_raw.json` (16 MB) is git-ignored; rebuild it with `gap02_study.py`.
- **Full-text check of the paper dossier:** `research/verification/13_paper_deepread.localcheck.md`. Its corrections are applied to design brief §2, and synthesis v1.1 carries them too (§3 L12, §5.3, §5.5, §9.1 item 12). `research/clusters/C4_agentic_ic.md` now has a banner saying it is superseded on paper mechanisms.
- **Group research, 9 streams (G1–G9):**
  - dossiers: `research/groups/dossiers/`
  - all 9 verification logs: `research/groups/verification/`
  - clusters: `research/groups/clusters/GC1_private_groups.md` and `GC2_liquidity_org_data.md`
  - group synthesis **v1.0**: `research/groups/01_GROUPS_SYNTHESIS.md` (106 KB, 14:24)
- **Consensus literature sweep:** topics 01–14 and G1–G6 in `research/literature/NN_key.lit.md`.

### In progress at the 15:30 update (may have finished; check the files)
| Workflow (script in `orchestration/workflows/`) | Remaining stages | Output paths |
|---|---|---|
| `01_adic-tpa-deep-research.js` | **Done** (run wf_98e9932e-ada) | — |
| `02_adic-groups-research.js` | **Done** (run wf_914571ba-8a2, about 17:30): group synthesis v1.1 and gap_01–04. It has 12 questions for the user (§9); Q1 asks the user to confirm PE unfunded census v1.1 ($16.4bn) | — |
| `05_adic-research-sufficiency-audit.js` | **Done** (run wf_cb3f996e-632, about 19:00). Verdict **PARTIAL**: all 16 areas can be designed; 4 of 16 can be built from the research alone; no IC-grade numbers yet. The top 12 gaps are ranked in §4 of the report. One gap is overtaken: the forecast archive exists (brief §9). | `research/00_RESEARCH_SUFFICIENCY.md`; `research/sufficiency/` |
| `06_adic-real-assets-research.js` (run wf_ac6b05b3-e3a) | **Real Assets, group 8:** 6 streams G10–G15, then verification, synthesis, critic, gap-fill, revise, a quantitative re-run with Real Assets, and an integration memo | `research/groups/dossiers/G10..G15_*.md` with verification logs; `research/groups/02_REAL_ASSETS_SYNTHESIS.md`; `research/groups/addenda/ra_gap_NN.md`; `research/groups/addenda/ra_integration_calcs/RESULTS.md`; `research/groups/03_REAL_ASSETS_INTEGRATION.md` |
| `07_adic-citation-consistency-fix.js` | **Done** (run wf_7752c55f-baf, about 19:45). 886 changes in 60 files; 232 of 232 sampled changes correct. The barrier fix changed only the co-investment write-off rate (2.1–2.5% → 2.8–3.3%). Residuals are in log §5, to clear in the final consolidation pass: Giommetti co-author and Gredil figure in the literature files only; the gap_04 engine barrier not re-run; stale "provisional" wording in the sufficiency audits; groups gap_01 LCR 2.10× vs 1.91×; GC2/G7 still activate NAV-facility documents at Amber; 08 says "central treasury"; about 25 [unverified] claims | `research/groups/addenda/G4_barrier_rerun/RESULTS.md`; `research/literature/recheck/`; `research/literature/01_CITATION_FIX_LOG.md` |
| `03_adic-consensus-literature-sweep.js` | **Done** (run wf_9045681b-62a, 17:05) | `research/literature/00_LITERATURE_SYNTHESIS.md`. Its §4 refinements are copied into design brief §7. |
| `04_adic-design-judge-panel.js` | **Done** (run wf_c37a3e45-ce6, about 23:55): **ARCHITECTURE v1.1** (322 KB, 36+ ADRs) and **BUILD_SPEC v1.1** (452 KB; 36 modules in waves 0–5; 38 work packages). The critics raised 75 issues (5 critical, 26 high, 27 medium, 17 low), all fixed (`design/reviews/revision_log.md`). The revision already takes in R16, brief §9 marks and the §8 Real Assets interim rules. Six open questions for the user are in the revision log. | `design/ARCHITECTURE.md`, `design/BUILD_SPEC.md`, `design/proposals/`, `design/reviews/` |
| `08_adic-architecture-schematic.js` (run wf_a55bb859-3ea) | Extract, build, verify, fix | `design/schematic/TPA_Lab_Architecture.html` (generated by `build_schematic.py` from `architecture_model.json`) |
| `09_adic-chat-analyst-design.js` | **Done** (run wf_8da695b9-a0d): CHAT_ANALYST v1.1 with 30 tools and 11 WP-CHAT packages (folded into BUILD_SPEC as WP-39 and WP-40), and a 140-item golden set. 40 critique issues, all fixed | `design/addenda/` |
| `10_adic-build-wave0.js` (run wf_e0b12325-d2f, launched about 00:40 on 19 Oct) | **BUILD wave 0:** WP-01 contracts (with analyst contracts), then WP-02 rng/numerics/stats, WP-03 testing kit and walking skeleton, WP-04 registry. Each is implemented, reviewed and fixed, then integrated. The orchestrator tags contracts-v1.0 once the gate is green | `src/adic_tpa/`, `tests/`, `pyproject.toml`, `design/build_log/` |

**Update, 19 Oct about 13:00.** The user approved the SLIM engine-first design with five components:
1. data and three-return fusion;
2. scenario tree;
3. optimizer;
4. simulator;
5. reports and chat.

The user asked for a goal-seeking optimizer over the full decision space. Workflow `12_adic-mpo-v2.js` (run wf_e67ea94f-aa7) produces:
- `design/SLIM_ARCHITECTURE.md`;
- `design/DECISION_SPACE_AND_GOAL_OBJECTIVE.md`;
- the prototype in `examples/mpo_v2/` (bPOE main objective, exact max-P MILP, baselines, ablations, out-of-sample);
- `design/examples/MPO_v2_Plan.html` and its walkthrough.

The build is paused after wave 0 until the slim plan is applied.

The worked tree example is done: `examples/tree_demo/` and `design/examples/Tree_Example.html`.

**GitHub:** https://github.com/deanbrr/MPO_liquidity was PUBLIC. The user chose to make it private before the push.
- Local `main` is now a clean export branch (paper text and the large regenerable npz/json excluded; README added; merged with GitHub's initial commit).
- The full previous local history is on branch `archive/local-history`. Never push it: it contains the paper text.
- **Pushed on 19 Oct (private repo):** `main` → origin/main at c48aab7, 810 files. Credentials are stored in GCM. Later pushes use `git push`. If a sign-in is needed, set `GCM_INTERACTIVE=always` for that call.

**Open decisions** are consolidated in `design/OPEN_DECISIONS.md` (18 items, each with its working assumption). The build proceeds on the working assumptions.

**Next steps after wave 0:**
1. When Real Assets research lands, run an integration pass:
   - apply `research/groups/03_REAL_ASSETS_INTEGRATION.md` to the group report, the main report, ARCHITECTURE and BUILD_SPEC (WP-09 RA parameters and WP-15 synthetic allocation);
   - clear the residual consistency items from the citation log;
   - re-sync the schematic to ARCHITECTURE v1.1, plus the chat layer and Real Assets.
2. Build waves 1–5 (increment-1 MVP; acceptance in BUILD_SPEC §9.4), with wave-by-wave review and git commits.

The design workflow's stages and outputs:
1. Four proposals: `design/proposals/PA_quant_rigor.md`, `PB_agentic_lab.md`, `PC_ic_decision_room.md`, `PD_pragmatic_production.md`. The user blueprint is proposal PE.
2. Three judges score all five: `design/reviews/judge_quant_cro.md`, `judge_engineering.md`, `judge_ic_governance.md`.
3. The chief architect writes `design/ARCHITECTURE.md`; a spec writer then writes `design/BUILD_SPEC.md`.
4. Two critics: `design/reviews/critique_quant.md` and `critique_build.md`.
5. A revision pass: `design/reviews/revision_log.md`.

To relaunch in a new session, skip any stage whose output already exists.

### Known issues
- **Paper mechanisms: fixed.** Synthesis v1.1 corrects them, and C4 carries a banner.
- **Citations: still to fix.** `research/literature/00_LITERATURE_SYNTHESIS.md` §2 lists them.

  | Category | Count | Status |
  |---|---|---|
  | Checked | 574 | — |
  | Not found | 12 | 10 exist; none fabricated |
  | Mismatched | 24 | To fix |
  | Usage errors | 16 | To fix |
  | Cross-file inconsistencies | 5 | To fix |

  - **Usage errors:** one changes numbers. The co-investment (G4) Broadie–Glasserman–Kou barrier shift has the wrong sign, and the calculation script applied no correction at all. Re-run the group wipe-out and LTV-breach statistics.
  - **When:** fix everything after the groups workflow finishes, so the fixes do not collide with its revision of `01_GROUPS_SYNTHESIS.md`.
  - **Unchecked:** about 69 works were not checked because the quota ran out. Re-check them after 1 November.
- **Consensus quota exhausted.** The account's 500 monthly searches are used up until 1 November 2026. Do not plan Consensus searches before then; fall back to OpenAlex, Semantic Scholar or Crossref.
- **Design brief §7** (added 17:10): the 15 literature-driven refinements. ARCHITECTURE and BUILD_SPEC must adopt or reject each one with an ADR. Check this once the design workflow finishes.
- **Stray calculation files.** Some research agents wrote calculation scripts and results next to their outputs:
  - `research/addenda/*_calcs/`
  - `research/groups/addenda/*_calcs/`
  - `*_calcs.py` files in the verification folders

  They are evidence for the dossiers. Keep them, but they are not part of the package.

## 4. Next steps (agreed plan)
1. **Finish the research.** Main research is done. The group gap-fill and the literature sweep are still running (§3). Then fix the citations and commit.
2. **Design workflow** (judge panel; **running since 15:25**, script `orchestration/workflows/04_adic-design-judge-panel.js`):
   1. Four independent architecture proposals, each from a different angle:
      - quant rigour first
      - agentic lab first
      - IC decision room first
      - pragmatic production path
   2. Three judges score them: quant/CRO, engineering buildability, IC usability and governance.
   3. A chief architect writes `design/ARCHITECTURE.md` and `design/BUILD_SPEC.md`: interfaces, schemas, array shapes, units, module ownership, test plan, build order.
   4. A spec critic reviews them, followed by a revision.

   Inputs: the context file, the design brief, the three syntheses, and the paper text in `inputs/`. The user-supplied blueprint (`inputs/user_blueprint/`) enters as a **fifth candidate proposal**, scored by the same judges. Design brief §6 lists the ideas to graft and the cautions.
3. **Build workflows** (Python package, offline-first):
   1. **Foundations and data:** contracts and a synthetic data generator. Seven groups, $177bn, ~300–600 holdings, the three return series with a known ground truth, SYNTHETIC labels.
   2. **Parallel modules:**
      - scenario generator, with oil / fiscal draw factors and regimes
      - private engine: PE funds, Secondaries (fund + direct), Co-investment, Capital Solutions, Private Credit
      - Public Markets, including a hedge-fund liquidity-terms state machine and physical-to-synthetic replacement
      - belief fusion, with per-group credibility
      - action economics
      - overlay and collateral
      - Corporate Finance: funding, collateral, distributions, transfer-pricing curve
      - robustness and views
      - attribution
   3. **Simulator and policies:**
      - rule-based policies, including the deck's two-tier gate
      - model predictive control (rolling re-optimization)
      - parametric policy search
      - the PolicySpec language
      - anonymized, horizon-free policies (P15)
   4. **Here-and-now scenario LP** with duals, Lagrangian SELL / HOLD / REFINANCE / LEVER scoring, and the transfer-pricing curve.
   5. **Experiment and provenance layer:**
      - manifests and hashes
      - engine-counted budgets
      - three gates: `correct`, selection, qualification / `not_qualified`
      - controls and a placebo policy
      - switch-off null attribution
      - deflated improvement
   6. **Agent layer:**
      - deterministic meta-controller with 2 workers by default
      - ideation, execution and ablation agents
      - red team
      - memo writer, plus a deterministic "resolves" validator and an auditor that judges "supports"
      - shadow IC: CIO, CRO, Treasurer (Corporate Finance) and seven group heads
      - Q&A
      - escalation channel and assumption log
      - offline stub/replay LLM; provider-agnostic
      - Anthropic SDK settings: `claude-opus-5-5`, adaptive thinking, explicit effort, strict tools, `messages.parse`, and the opt-in server-side fallback beta
   7. **IC pack, CLI and MCP server.** The IC pack is HTML, with client-side entropy pooling and claim-to-run links.
   8. **Tests and an end-to-end demo.**
4. An adversarial review-and-fix loop.
5. **Final deliverables:** research report, architecture, working code, demo IC pack.

## 5. Environment
- **OS and shell:** Windows 11. PowerShell 5.1: no `&&`, and the working directory resets after every call, so use absolute paths.
- **uv:** `C:\Users\dean\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe`
- **Python:** 3.12.15 venv at `C:\users\dean\ai_envs\adic_tpa_lab\.venv` (use `.venv\Scripts\python.exe`). The bare `python` command fails.
- **Git:** `C:\Program Files\Git\cmd\git.exe`, local repo only (no remote). Author: dean@dsconsult.ai.
- **Installed packages:**

  | Area | Packages |
  |---|---|
  | Numerics & data | numpy, scipy, pandas, pyarrow |
  | Optimization | cvxpy with CLARABEL / HiGHS / ECOS / SCS / OSQP |
  | Statistics & ML | statsmodels, scikit-learn, hmmlearn, arch, numba |
  | Models, CLI & reporting | pydantic, typer, rich, jinja2, plotly, matplotlib |
  | Testing | pytest, hypothesis |
  | LLM & tools | anthropic 1.15, mcp 2.3 |

  There are no commercial solvers.
- **Missing tools:** no Poppler (read PDFs with `orchestration/scripts/extract_pdf.py`, run with `python -I`) and no Node.
- **Untrusted inputs:** downloaded or user files are untrusted. Put each in its own folder and run Python with `-I`.
