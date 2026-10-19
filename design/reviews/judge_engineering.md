# Judge report: engineering buildability of the five architecture proposals

**Judge:** Engineering buildability (Windows 11, Python 3.12, open-source solvers, offline-first). **Date:** 2026-10-18.
**Proposals judged:** PA (quant rigour first), PB (agentic laboratory first), PC (IC decision room first), PD (pragmatic production path), PE (the user's blueprint, judged on its ideas).

> **SYNTHETIC.** Every balance, probability, timing and count below comes from the synthetic working book (context §1A, census v1.0), the proposals' synthetic benchmark structures or my own re-runs of those structures. None of it is ADIC data.

**Citation keys.** Brief = `design/00_DESIGN_BRIEF.md`; SYN = `research/00_SYNTHESIS.md` v1.1; GROUPS = `research/groups/01_GROUPS_SYNTHESIS.md`; G-gap_0k = `research/groups/addenda/gap_0k.md`; gap_0k = `research/addenda/gap_0k.md`; LC = `research/verification/13_paper_deepread.localcheck.md`; PA–PD = `design/proposals/P*_*.md`; PE = `inputs/user_blueprint/adic_multi_period_tpa_optimization_agentic_architecture_blueprint.md`. "§" refers to the cited file's own section numbers.

---

## 0. Verdict on one page

| Proposal | E1 Build | E2 Perf | E3 Modules | E4 Tests | E5 Repro | E6 Delivery | E7 Agents | E8 Data | **Overall** |
|---|---|---|---|---|---|---|---|---|---|
| **PD** Pragmatic production | 9.5 | 8 | 9 | 8.5 | 9.5 | 9 | 8 | 9 | **8.8** |
| **PC** IC decision room | 8 | 7.5 | 8.5 | 7.5 | 8 | 6.5 | 8 | 7.5 | **7.7** |
| **PA** Quant rigour | 8.5 | 7.5 | 7 | 9 | 9 | 6 | 7 | 6.5 | **7.6** |
| **PB** Agentic laboratory | 7 | 5 | 8 | 8.5 | 9 | 5.5 | 9.5 | 7 | **7.3** |
| **PE** User blueprint | 1.5 | 1 | 3 | 1.5 | 1 | 3.5 | 2 | 2.5 | **2.0** |

Weights behind "Overall": E1, E2, E3, E4 and E6 at 15% each; E5 and E7 at 10%; E8 at 5%. The ranking is unchanged under equal weights.

**Recommended base: PD**, as an explicit composite.
- PD measures the most workloads on this laptop: the policy simulator, 50k-path certification, H at four sizes and warm re-solves. It also ports the research prototypes as regression fixtures, freezes typed `Protocol` interfaces in week 2 and ships a 10-week end-to-end slice with exit criteria (PD §1, §3, §4.15, §8).
- Graft onto it: PA's verification apparatus (error ledger, consistency contract, selection certificate Γ, counter-based CRN); PB's agent-integrity apparatus (rendered claims, anchored-residual DSL, integrity drills, typed failure taxonomy, planted-effect lab calibration); PC's decision-room spine (Decision Register and evidence compiler, computed shadow IC, interface shape contracts, draws outside parallel kernels); and four of PE's ideas (§7).

**No fatal flaw in PA–PD.** All four move integrality out of the scenario tree (an LP plus a small post-LP MILP), replace Gurobi's `feasRelax` with HiGHS, keep the owner's draw exogenous and use the user's REFINANCE/LEVER definitions. **PE is not adoptable as written**: it depends on Gurobi/MOSEK, PyMC, LangGraph/AutoGen and a neural-operator surrogate, makes the distribution a decision with its own utility, puts a P(CAGR ≥ 10%) indicator in a weighted objective and inverts the user's REFINANCE/LEVER definitions (§3.5).

**Top five must-fix items** (full list in §8):
1. Benchmark the here-and-now program at production fidelity in sprint 1 and choose the solver per tree shape: my re-runs show that the faster HiGHS algorithm flips between tree structures (§5.1).
2. Implement lexicographic Phase I as explicit elastic LPs in HiGHS, with crossover-based duals, and port both pinned-dual suites (gap_02 8/8, G-gap_01 18/18) as CI gates.
3. Fold in the groups addenda the proposals miss: census versioning (G-gap_02 census v1.1), the robust FBE-R and its optimizer-feedback covariates, the new κ definition, the deterministic O3 performance module and gate V24 (§5.3).
4. One determinism contract: counter-based or block-keyed RNG generated outside parallel kernels, single-threaded evaluator solves, pinned versions and golden manifests reproduced bit for bit.
5. Write down the package policy: everything in SYN §10's stack that is not installed (JAX, Pyomo/mpi-sppy, pycma, Optuna, QuantLib/ORE, chainladder, scoringrules, SDDP.jl) is replaced in-house or justified in writing.

---

## 1. Method and evidence

**What I read.** The brief in full; context in full; SYN §0–2 in full and §3, §4.1–4.12, §5, §6, §7.2, §8, §9, §10; GROUPS §0–2.4, §4–6; G-gap_01, G-gap_02 and G-gap_03 (answer sections and the parts that change engines); gap_01–gap_05 (answer sections; gap_02 in depth, including `test_no_pinned_duals.py` and `phase1_demo.py`); LC summary; all five proposals in full.

**What I verified on this machine** (Core Ultra 9 285HX, 24 cores, 95 GB RAM).
- *Environment.* The project venv holds 89 distributions, including highspy 1.15.1, clarabel 0.11.1, osqp 1.1.3, scs 3.3.1, ecos 2.0.14, numba 0.68, hmmlearn 0.3.3, arch 8.0, statsmodels 0.15, scikit-learn 1.9.1, pyarrow 26, pydantic 2.14, anthropic 1.15, mcp 2.3, opentelemetry-api, pyyaml, jsonschema and pywin32. **Absent:** jax, cma (pycma), optuna, pyomo, mpi-sppy, QuantLib, ORE, chainladder, scoringrules, pymc, numpyro, gurobipy and mosek. cvxpy reports CLARABEL, SCS, ECOS, ECOS_BB, OSQP, HIGHS and SCIPY.
- *Solver API.* `highspy.Highs` exposes `feasibilityRelaxation`, `getIis`, `writeIisModel`, `getRanging`, `setBasis`/`getBasis`, `getDualRay` and in-memory model edits, so PA's and PD's claims that Phase I, the IIS, ranging and warm starts need no Gurobi are correct.
- *Model IDs.* `claude-opus-5-5` and `claude-sonnet-5-5` both appear in the bundled SDK reference, so PB's Phase-0 "family B" model exists (it is the same provider, as PB discloses).
- *Benchmarks.* I read every proposal's benchmark script (PA `hbench/h_tree_bench.py`; PC `pc_bench/hn_lp_bench.py`, `sim_kernel_bench.py`; PD `pd_bench/bench_lp.py`, `bench_sim.py`, `bench_warm.py`) and their result files, and re-ran three configurations (§5.1, Appendix A).
- *Load caveat.* Throughout my session the CPU sat at 100%: the groups gap_04 Shapley job (`g04_run.py shapley`) occupied 22 worker processes. Every absolute time I measured is therefore pessimistic, by about 3–4.5× against the proposals' own (also loaded) runs. Ratios between solvers on the same structure hold under load only when both run single-threaded; HiGHS's IPM can be multi-threaded (§5.1).

---

## 2. Scores with justifications

### 2.1 PA: Quant rigour first (overall 7.6)

| Criterion | Score | Justification |
|---|---|---|
| E1 Buildability | 8.5 | Designs for the installed stack: matrices assembled in `scipy.sparse` and passed to `highspy`, with cvxpy kept for small problems (§4.8.3 "Engineering"); in-house numpy CMA-ES because `cma` is absent (§4.8.8); closed-form empirical Bayes because PyMC is absent (§10). Two pieces are expensive to build: belief-state trees with posterior-predictive children (§4.3) and the overnight resource-directive Benders for 2,000-leaf trees (§4.8.3, deferred to Phase 1). The client-side JavaScript entropy pooling (§6) has no test plan in an environment without Node |
| E2 Performance | 7.5 | The most faithful proxy of the three LP benchmarks: PWL CRRA tangents, the L2 shortfall, per-model CVaR rows, a running-max red margin and root rows (`h_tree_bench.py`). Measured default 1,200 leaves × 8 periods = 227k columns, 202k rows: **53 s** HiGHS IPX cold, CLARABEL 98 s (§4.8.3). My re-run reproduced the iteration count (94) and took 224 s on the saturated machine, with dual simplex at 399 s, so IPM is the right default for this tree. The whole quarterly run is budgeted at ≈1.5–2 min (§4.8.3), which sits on the edge of the target. PA honestly reports that 1,200 × 12 and 2,000 × 8 do not converge in 300 s (its `run_1200x12.json` and `run_2000x8.json` confirm the time-limit status), so the brief's upper corner needs Benders overnight. The 10k × 40 simulator is an estimate only (10–30 s on 8 numba cores [I], §4.2) |
| E3 Modules | 7 | Clear module IDs, owners and a dependency order (§3, §8), with parallel tracks against "a fake Φ fixture" and integration at weeks 4–6 (§8). But "one Φ generates both the simulator and H's rows" (§4.8.2 H1, §9 #1) makes every engine team deliver two artefacts, a simulation step and a node-row generator, which is the tightest coupling in any proposal. Interface contracts are named but not written out (§11 item 15) |
| E4 Testability | 9 | The best quant verification design. Error ledger A1–A16, each with a certificate or test, an acceptance level and a fallback (§4.12). Consistency contract in CI: conservation to 1e-10, H rows reproduce the simulator's cash path to 1e-9, duals inside finite-difference intervals, penalty invariance, μ − M > 0 at pricing nodes, H–P agreement, HiGHS–CLARABEL agreement, LEVER ≡ ADD + REFI, metamorphic rules (§4.12). The selection certificate Γ is checked on every run (§4.8.5). Test families include statistical CP-coverage tests and a layering test (§8) |
| E5 Reproducibility | 9 | Counter-based RNG: every uniform is a pure function of (seed, world, plane, path, month, source, slot), so CRN holds by construction and results cannot depend on thread count (§4.3, P11 row of §2). Manifests, pinned solver versions, hashed planes; stale caches stop evaluation (§2 P2) |
| E6 Delivery | 6 | An MVP is defined (§8: M1 + M6 + held-out, Level-1 overlay, FBE on planted biases, P with certification, H in the what-if configuration), with integration milestones at weeks 4–6. But it has no MVP completion date or exit test beyond the six questions, and it front-loads the full Φ-to-row machinery, column generation with the Farley certificate, the Level-B MILP and belief-state trees. Rigour is spent before an end-to-end slice exists |
| E7 Agent layer | 7 | Deliberately thin and sound: agents emit only typed objects the evaluator can price; a plain-Python state machine; engine-owned gates; `LLMBackend` with Anthropic, Replay (fails closed on a miss) and Stub; engine packages never import agent code (§5). Little on the failure taxonomy, the tool firewall or a cost model; cost control is the $50 / $200 caps and counted evaluations (§5 "Budgets") |
| E8 Data | 6.5 | Tables, bitemporal tags and an adapter flow "map → validate → bitemporal upsert → hash", with real and synthetic never mixed (§7). No quarantine for unknown fields, no adapter contract tests, no operator flag for holding-level prompt content beyond P13's one line |

### 2.2 PB: Agentic laboratory first (overall 7.3)

| Criterion | Score | Justification |
|---|---|---|
| E1 Buildability | 7 | The quant core uses the installed stack (HiGHS IPM on `scipy.sparse`, CLARABEL cross-check, in-house CMA-ES; §4.10, §5.4). The lab adds four OS processes, an MCP stdio relay, NTFS ACLs and a seal service under a separate CRO account holding a commit-reveal salt (§5.2 B1–B4). All of it is buildable with pywin32, but it is operationally heavy on a single-user laptop, which PB concedes (§10 risk 5). Search family F2, "a 3-regime MS-VAR with mixture innovations" (§4.3), has no library: statsmodels' Markov models are univariate, so it is a custom EM build |
| E2 Performance | 5 | Nothing is measured. The simulator budget is ≈52 s against the 60 s target (§4.2 [I]). The interactive H (3 models × 400 leaves, ≈244k variables, 1.2M nonzeros) is estimated at 30–90 s on HiGHS IPM (§4.10 [I]), optimistic against PC's measured 136 s for 261k variables. Phase I runs on the full tree, adding 20–60 s per tier (§4.10 table), and 10 SAA replications take 20–30 min. The quarterly baseline is therefore likely above 2 minutes. PB makes `bench_h.py` a month-1 exit criterion (§4.10), which is the right hedge |
| E3 Modules | 8 | Nine streams against frozen `contracts/` (arrays of shape (paths, quarters, entities), float32, US$m), with the evaluator, seal and claims built on mock engines in parallel with the engines (§8). The trust boundaries are explicit process boundaries (§3, §5.2) |
| E4 Testability | 8.5 | The best agent-layer test design: a CI drill for each observed failure mode, covering tampering, the budget cap, a final-store permission error, NaN paths scored worst-case, seeded overclaims, a fabricated-number memo, a planted leak that must fail to compile, caches, horizon references, memo-cites-memory and escalation (§5.16). Planted-effect campaigns (true gain, leak, null world) measure the lab's own power and false-qualification rate (§7). Quant-level tests are standard (§8) and lack PA's solver-consistency checks |
| E5 Reproducibility | 9 | SeedSequence and Philox streams keyed by (world, path, entity); manifests carrying every hash; a hash-chained ledger; ReplayBackend reproduces campaigns bit for bit; final seeds by HMAC(salt, world) with commit-reveal (§4.2, §5.2 B4–B5, §5.17) |
| E6 Delivery | 5.5 | The week-6 MVP is lab-centric: a reduced book (PE funds, Treasury, long-only, simple HF ladder), Gates 1–3 through the seal service, a 3-slot DSL and a minimal pack (§8). It lacks H, λ, envelopes and cards, so it cannot answer SYN §10's six MVP questions, which appear only as later exit criteria. Nine parallel streams in 12 weeks, with the heaviest infrastructure first |
| E7 Agent layer | 9.5 | The strongest. A deterministic FSM with checkpoints K0–K9 and per-state tool allowlists (§5.6); strict schemas with a `submit_<artifact>` tool re-validated by Pydantic; ≤ 3 retries; a typed failure taxonomy (INVALID_SPEC … BUDGET_EXHAUSTED distinct from EXECUTION_FAILED, §5.7); degraded phases; rendered placeholders, so no LLM writes a digit (§5.10); an anchored-residual DSL with identity at zero, which makes the switch-off null exact (§5.4); refusal-fallback handling with a family-collision check (§5.17); a costed campaign of ≈$35 with caching and Batch (§5.15) |
| E8 Data | 7 | `SourceAdapter.load(as_of) -> Snapshot`, with real and synthetic never in one snapshot (§7); a gateway redaction filter, extractors without outbound tools and data classes allowed in prompts declared in the contract (§2 P13, §5.3 `llm_policy`). Adapter validation and quarantine are not specified |

### 2.3 PC: IC decision room first (overall 7.7)

| Criterion | Score | Justification |
|---|---|---|
| E1 Buildability | 8 | Standard stack: HiGHS (benchmarked through `scipy.optimize.linprog`), CLARABEL through cvxpy, OSQP for module F, in-house CMA-ES (§4.11). `linprog` exposes no basis, warm start, ranging or IIS, so production must call `highspy` directly, as PA and PD do. Phase I by sequential HiGHS LPs with an IIS deletion filter over ≤ 30 aggregated rows, which avoids Gurobi (§4.11). The Register is a signed YAML catalogue compiled into Pydantic objects (§6.1). The in-browser golden self-test for JavaScript entropy pooling is the honest answer to "no Node" (§6.6). The evidence compiler (a content-hashed build DAG) is real software to write |
| E2 Performance | 7.5 | Measured on a proxy that includes the CVaR row: 500 leaves = 132k variables, **20.2 s** HiGHS IPM, against 109.5 s dual simplex and 80.8 s CLARABEL; 1,000 leaves 136 s IPM (§4.11; `hn_lp_bench_20x50.json` confirms 136.3 / 571.4 / 207.5 s). My re-run on a saturated machine gave 90.7 s IPM and 124.0 s dual simplex, so PC's IPM speed probably relies on HiGHS's parallel interior-point threads (§5.1). The design runs five 500-leaf SAA replications in parallel processes to stay inside 2 minutes and to produce dual bands (§4.11). Simulator: the numba kernel ran 10k paths × 400 cohorts × 120 months in 3.96 s on 8 threads, and the full engine is budgeted at 5–8× (§4.2). Caveat: its tree branches only at t = 1 (20 nodes) and then runs single-path fans from quarter 4 to 11, so 8 of 12 quarters are clairvoyant within each leaf path and quarter-1 prices rest on 20 nodes; PC neither measures nor discusses this |
| E3 Modules | 8.5 | Layers L0–L5 with downward-only dependencies, so the room never calls an engine directly (§3.1). The best interface table: ScenarioSet f32[N,M,F], CashflowCube f32[N,Q,K,4], LedgerPaths f32[N,M,R], BeliefSet, HNResult, ViewSpec, PolicySpec and RunManifest, with units (§3.3). Six streams, and the room is built on recorded fixtures from week 1 (§8) |
| E4 Testability | 7.5 | Room tests: every Register entry renders, incomplete briefs are rejected, seeded numbers are caught, recused votes are excluded, pre-votes are immutable, and JavaScript matches Python entropy pooling on golden cases (§8). There is an end-to-end test (`adic-tpa quarter --synthetic` < 30 min). Regression, recovery and metamorphic suites are present. Solver-level reconciliation (H–P agreement, dual sanity, cohort vs asset) is thin |
| E5 Reproducibility | 8 | SeedSequence keys per plane, model and path block. Crucially, draws are generated outside parallel kernels because PC's own bench gave thread-count-dependent results when drawing inside `prange` (§2.2 P11). Its JSON shows mean TWR 2.73838 at 8 threads against 2.73833 at 24. Manifests; replay cassettes keyed by SHA-256 (§5.5) |
| E6 Delivery | 6.5 | A full vertical slice in 10–12 weeks (Q1, Q2, Q4, Q5 and Q6 decisions; L0; W1; shadow IC on the stub; 500-leaf H-LP; P; module F; §8). Building the room on fixtures from week 1 lets the IC test the product early. The 23-entry Register, the evidence compiler and the computed shadow IC add scope that an engine-first slice would not carry |
| E7 Agent layer | 8 | Roles with typed MCP tools, strict schemas, `messages.parse`, auto tool choice, explicit effort and refusal fallback (§5.1–5.2); gates G0–G9 (§5.4); blocking escalation for high-tier roles (§5.5). Seats get their numbers only from `implied_actions` under declared (q_k, θ_k), which is the cleanest P1 treatment of the shadow IC (§6.5). Failure handling and cost control are generic |
| E8 Data | 7.5 | Table schema with keys (§7). `data_class ∈ {SYNTHETIC, REAL}`, with mixed data a hard error. Adapters validate against the same schemas. Holding-level prompts need an operator flag (§2.2 P13) |

### 2.4 PD: Pragmatic production path (overall 8.8)

| Criterion | Score | Justification |
|---|---|---|
| E1 Buildability | 9.5 | Every substitution is explicit. Negative-binomial dwell via a state-expanded `hmmlearn` HMM because no HSMM library exists (§4.3); `scipy.optimize.differential_evolution`, with `cma` added only if DE is ≥ 5bp CE worse under a pre-registered test (§4.11); `scipy.optimize.milp`/HiGHS for selection; cvxpy/OSQP for module F; HiGHS `feasibilityRelaxation` and `getIis` for Phase I (§4.11, §9 #5); in-house entropy pooling to avoid GPL (§4.13); a SQLite registry; concrete typer commands (§4.15). Increment 1 ports `hf_ladder.py`, `t1_engine` and `bridge.py` as regression fixtures (§4.4, §8) |
| E2 Performance | 8 | Measured on the target laptop: asset-level P at 10.9 s for 10k × 40 on one process and 5.9 s on four, with identical checksums; 50k paths per world in 16.8 s; H at 600 × 12 (177k variables) in **32 s** dual simplex, 1,000 × 12 in 90 s, 2,000 × 12 in 286 s overnight; warm re-solves in 0.04–0.06 s (§4.11, §4.15). Two caveats. The LP bench omits the CVaR, utility and T4′ rows, and the simulator bench is simplified (4-state HF machine, no FBE draws, no filter recomputation), hence PD's 2.5× reserve. My re-run with a binding CVaR row added (§5.1) shows that single-threaded dual simplex stays ≈3× faster than single-threaded IPM on PD's tree (78.5 s against 231.8 s), so the solver choice survives for this tree, but absolute times rose under load |
| E3 Modules | 9 | Concrete `Protocol` signatures: `AssetEngine.init/step`, `Ledger.apply/row_slacks` returning the same RowIds as H's rows, `Policy.act` without horizon or path id, `build_h`, `phase1`, `phase2` and `price` with `priced_on` (§3). Unit conventions are fixed ($bn float64 in the ledger and LP, float32 in cubes). Contracts freeze in week 2, and each stream builds against a golden 200-path mini-cube and mini FlowCube (§8). This is the easiest design to split among parallel agents |
| E4 Testability | 8.5 | The test matrix covers unit, property (ledger identity, dual signs, DSL rejects look-ahead), metamorphic (including penalties ×10 leave duals unchanged, measured 0.0), regression (golden manifests bit for bit, `test_v8_replica`, bridge, the gap_02 8/8 and G-gap_01 18/18 suites ported), reconciliation (H vs P replay to 1%, cohort vs asset, DVA sums, netting), parameter recovery, nightly performance assertions and agentic drills (§8). An H–P Kendall τ ≥ 0.8 ranking test guards the LP surrogate (§4.11). Missing, relative to PA and PB: certificates (Γ, MMW gap), dual finite-difference intervals and an integrity-drill suite |
| E5 Reproducibility | 9.5 | SeedSequence per path block, with an identical checksum at 1 and 4 workers (measured); solver and BLAS pinned to one thread in the evaluator; exogenous cubes regenerated and checksum-verified (2.3 s per 10k paths) rather than stored, with final-plane cubes materialised once and sealed; replay keyed by sha256(model, system, tools, messages, params) (§2 P11, §4.2, §5) |
| E6 Delivery | 9 | Increment 1 (weeks 0–10) has a concrete scope and exit criteria: the six MVP questions, both pinned-dual suites, exact identities, green performance assertions and a 100% labelling audit. v1 (months 3–6) and v2 (months 6–12) follow, sized to a team of four (§8). It reuses research code rather than rewriting it |
| E7 Agent layer | 8 | Agents have no file, shell, code or network tools; tools are served by a separate evaluator process over MCP stdio; the PolicySpec AST compiles to vectorised numpy and is never `eval`ed (§5). Meta-controller state persists in the registry; a separate final-plane evaluator instance has its own cache; budgets count evaluations, paths, CPU-seconds, tokens and dollars; escalation has severities; LLM settings are correct for anthropic 1.15 (§5). No rendered placeholders and no drill suite like PB's |
| E8 Data | 9 | Bitemporal entity table with keys and grains (§7). `SourceAdapter.read(raw) → pa.Table → validate(schema) → load(bitemporal)`; unknown fields or units go to quarantine; each adapter has fixture contract tests; adapters are ordered by data value; synthetic sets stay frozen and separate (§7). Holding-level prompt content needs an operator flag in live mode (§2 P13) |

### 2.5 PE: User blueprint (overall 2.0)

| Criterion | Score | Justification |
|---|---|---|
| E1 Buildability | 1.5 | Requires Gurobi/MOSEK MILP/MIQP (§3.1 item 3; §4 Phase 2), Stan/PyMC or NumPyro (§3.1 item 1; §4 Phase 1), LangGraph or AutoGen (§4 Phase 4) and a neural operator trained on 50,000+ pre-solved runs (§4 Phase 3). None is installed; there is no GPU; orchestration by LangGraph conflicts with P9 |
| E2 Performance | 1 | A max-min Wasserstein DRO over a sum containing a P(CAGR ≥ 10%) indicator, with discrete S/H/R/L per asset per epoch on 10,000 paths (§2.3, §2.5), is a non-convex mixed-integer program that will not solve at this scale. It gives no variable counts and answers live questions with a "<3 s" surrogate (§3.2 step 4) |
| E3 Modules | 3 | The modules are agents ("Asset Optionality Agent … MILP solver", §3.1), which blurs deterministic engines and LLM roles. No interface contracts |
| E4 Testability | 1.5 | One sentence: figures "must come from verified solver state outputs" (§4 Phase 4). No unit, recovery, regression or CI gates |
| E5 Reproducibility | 1 | Not addressed |
| E6 Delivery | 3.5 | A four-phase, 18-week roadmap (§4) is a useful framing (brief §6 graft 8), but it has no thin end-to-end slice, and Phase 3 trains a surrogate before the engine is validated |
| E7 Agent layer | 2 | LLM-driven orchestration; `Agent_Discovery` "autonomously" runs overnight experiments maximising P(return ≥ 10%) (§3.1 item 5, §4 Phase 3), with no evaluator boundary, planes, counting or gates |
| E8 Data | 2.5 | A schema linking each asset to its triplet, cash flows, debt and secondary benchmarks (§4 Phase 1); nothing on confidentiality or synthetic labelling |

---

## 3. Fatal flaws and serious risks

### 3.1 PA
- **No fatal flaw.**
- **Serious risk: the Φ-to-rows coupling** (§4.8.2 H1). Every engine must export node-level linear coefficients as well as simulate, and the nonlinear engines (HF gates, covenants, SIMM) need special handling (§4.0 P-H/P-L). This is the hardest interface in any proposal to build in parallel.
- **Serious risk: the quarterly run sits at the 2-minute edge** (≈1.5–2 min, §4.8.3), and the brief's 2,000-scenario corner needs a hand-built Benders (Phase 1).
- PA names dual stability as its biggest risk (§10 risk 1), correctly; λ rests on about a dozen tail leaves per world.

### 3.2 PB
- **No fatal flaw.**
- **Serious risk: H performance is unmeasured,** and Phase I runs on the full tree tier by tier (§4.10). A quarterly baseline above 2 minutes is likely until `bench_h.py` proves otherwise.
- **Serious risk: the infrastructure-first build order.** The seal service under a separate account, four processes and nine streams come before the quant slice that answers the IC's questions (§8). If the lab qualifies nothing (PB §10 risk 1, "zero yield"), the first months produce no decision support.
- The optimiser's own recommendation is only a candidate that must clear Gates 2–3 (§5.6). PB keeps baseline cards from BASELINE_PRICED, so the IC is not left empty-handed, but power shortfalls (NOT_ASSESSED, §10 risk 2) may be common.

### 3.3 PC
- **No fatal flaw.**
- **Serious risk: tree clairvoyance and coarse quarter-1 prices.** Single-path fans run from quarter 4 to 11 (§4.11), and the effect is not measured. Adopt PA's A9 test (out-of-sample root evaluation in P, a 1-leaf-fan variant).
- **Serious risk: the new hard row LM** (§4.11, §4.12 Tier 1A). "Liquid assets + unused committed facilities × canonical credit ≥ draws + calls − distributions + IM + CVaR₉₉(VM) over 12 months" overlaps T3 and T4′ and their canonical conventions (gap_02 §1.1). As a separate hard row it can double-count and push the book into recovery mode spuriously. PD's treatment, which hardens T3 with CVaR₉₉ VM and puts the stress-coverage ratio on the offset card, is the consistent one.
- **Scope risk: process burden** (PC §10's own top risk), which is a delivery risk too.

### 3.4 PD
- **No fatal flaw.**
- **Deviation to document: the quarterly private-engine clock** (§4.1), against SYN §2.1's monthly engine. It is defensible, because marks are quarterly and the T4′ ledger and VM stay monthly. It needs an error-ledger test showing that T6 and T3 do not move materially. PC's kernel bench shows that a monthly cohort clock is affordable anyway (§4.2: 8.3 ns per cohort-month).
- **Evidence gap: benchmarks below production fidelity.** The LP bench omits the CVaR, utility and T4′ rows, and the simulator bench is simplified (`bench_lp.py`, `bench_sim.py`). PD's 2.5× reserve (§4.15) and my CVaR re-run make this acceptable, provided the sprint-1 production benchmark is a gate.
- **Thinner agent integrity than PB:** no rendered placeholders and no drill suite. Fixed by grafts.

### 3.5 PE (not adoptable as written)
1. **The distribution is a decision variable with a utility term,** U(D_t) in the objective and D_t in the policy (§2.5). The user confirmed that the owner sets the draw as an exogenous liability (brief §6 item 6, user answers).
2. **REFINANCE and LEVER contradict the user's definitions.** REFINANCE is an asset-level dividend recap or debt repricing, which is a GP decision; LEVER is NAV lending or preferred equity, which is cash-out, i.e. the user's REFINANCE (§2.3 table; brief §6 cautions).
3. **A P(CAGR ≥ 10%) indicator sits in a weighted objective** (§2.5), and `Agent_Discovery` maximises P(return ≥ 10%) (§4 Phase 3). That rewards gambling for resurrection (SYN L9, §4.9).
4. **The live IC sees surrogate numbers** from a neural operator in under 3 s (§3.2 step 4; §4 Phase 3), against P1 and brief §6.
5. **Unbuildable dependencies:** Gurobi/MOSEK, PyMC/Stan, LangGraph/AutoGen, a GPU-scale surrogate (§3.1, §4).
6. **No evaluator integrity, planes, counting or gates.** It is ungovernable under P2–P5, which the paper's own failures make necessary (brief §2 P2; SYN L12).
7. **Illustrative numbers framed as outputs** ("+14.2%", "64% → 41%", §3.1 item 5, §3.2 step 2) and an ambiguous "nominal/real" target (§1); the brief says nominal USD (brief §6).

---

## 4. Best ideas worth grafting, by proposal

| Source | Idea (exact section) | Why it matters for engineering |
|---|---|---|
| PA §4.12 | Error ledger A1–A16 plus the consistency contract | Turns every approximation (cohorting, tree reduction, Taylor P&L, PWL utility, CVaR surrogates, client-side EP) into a CI test with an acceptance level and a fallback |
| PA §4.8.5 | Column generation with the Lagrangian (Farley) certificate Γ, accepted at ≤ 5bp CE, else "selection not certified" | A computable optimality gap for the selection MILP; cheap with exact column cash-flow vectors |
| PA §4.3 | Counter-based RNG u = H(seed, world, plane, path, month, source, slot) | CRN by construction, independent of thread count and policy; removes PC's observed `prange` non-determinism |
| PA §4.8.6 | One-sided duals by warm re-solves ("at a kink"), RHS ranging validity intervals, H–P agreement on λ^spot | Makes the FTP curve auditable; directly addresses dual instability |
| PA §4.8.3 | Direct `highspy` assembly from `scipy.sparse`, no cvxpy canonicalisation at 10⁶ nonzeros; money in W₀ = 1 units, penalties ≤ 10⁴ | Avoids measurable overhead and conditioning problems |
| PA §4.9 | Tolerance cascade: level-k metrics may degrade by at most one paired SE while optimising level k + 1 | A testable lexicographic rule |
| PA §4.12 A9 | Fan-clairvoyance test (root evaluated out of sample in P; 1-leaf-fan variant) | Needed by every tree design, PC's above all |
| PB §5.10 | Rendered claims: typed placeholders `{{m:<metric_id>\|<format>}}`, plus a validator that rejects literal digits | The strongest mechanical P1 enforcement; kills "tool bypass" |
| PB §5.4 | Anchored-residual PolicySpec DSL with identity at zero and type rules TR1–TR7 | Makes the switch-off null control exact by construction (brief P6) and keeps search inside a schema |
| PB §5.7 | Typed gate failure taxonomy (INVALID_SPEC, TIER1_FAIL, NI_FAIL, OV_FAIL, PINNED_DUAL, GAMBLING, BUDGET_EXHAUSTED ≠ EXECUTION_FAILED) | Engine-owned accounting the paper lacked (brief P5) |
| PB §5.16 | Integrity drill suite in CI (tamper, over-budget, final-store permission, NaN worst-case, seeded overclaim, fabricated number, planted leak, cache, horizon reference, memo cites memory, escalation) | Converts P2–P9 into regression tests |
| PB §7 | Planted-effect lab calibration (true gain, planted leak, null world) | Measures power and false qualification; sets ε_mat and budgets empirically |
| PB §5.2 B4–B5 | Commit-reveal final seeds (HMAC(salt, world)); hash-chained append-only ledger | Lightweight versions are cheap and make P3 auditable |
| PB §5.3 | `AnalysisContract` as a frozen, `extra="forbid"` Pydantic model with signoffs, planes, gates, budgets and hashes | A ready interface for the contract plane |
| PB §5.15 | Per-campaign token and cost model, with caching and Batch | Cost control with numbers |
| PC §6.1 | Decision Register plus the evidence compiler: `EvidenceSpec(metric, by, plane, max_age_days)`; a brief renders only if every spec resolves, else "EVIDENCE MISSING" | Traceability from IC decision to hashed run; no silent fill |
| PC §6.5 | Computed shadow IC: each seat's position is `implied_actions(q_k, θ_k)` with θ_k in an admissible set Θ (no indicator terms) | Grafts PE's opposing utilities without breaking P1 or L9 |
| PC §3.3 | Interface table with array shapes and units | Lets parallel agents build against fixed tensors |
| PC §2.2 P11 | Generate draws outside parallel kernels (thread-count dependence measured) | An empirical determinism finding |
| PC §4.11 | Parallel SAA replications as the standard design (dual bands within the time budget); IPM duals taken after crossover | Practical route to dual bands and to the basic solutions that pinned-dual detection needs |
| PC §6.6 / PD §6 | JavaScript entropy pooling with golden vectors and an in-browser self-test; any logged number recomputed by Python | The only way to test W1 without Node |
| PD §3 | `Protocol` interfaces (AssetEngine, Ledger, Policy, build_h, phase1, phase2, price), with `row_slacks` sharing RowIds with H | The base contract layer |
| PD §4.2 | Regenerate-and-verify cubes with checksums; seal final-plane cubes | Saves gigabytes and binds code to seeds |
| PD §4.11 | H–P Kendall τ ≥ 0.8 ranking test and replay-to-1% test; warm re-solves for the selection loop and penalty-invariance test | Cheap guards on the LP surrogate |
| PD §7 | Adapter pipeline with quarantine and fixture contract tests | Real-data onboarding without contaminating stores |
| PE §2.2 | Market-implied fourth signal (secondary bids → implied forward return) | Brief §6 graft 1; already in PA–PD's FBE |
| PE §3.1 item 1 | Zombie-NAV flag; P(forecast achieved within k quarters); catalyst milestones required for recovery forecasts | Brief §6 graft 2; cheap deterministic diagnostics |
| PE §2.4 | Liquidity-margin inequality with CVaR₉₉ of stressed VM; stress-coverage test | Brief §6 graft 3; adopt as PD does (harden T3; ratio on the offset card), not as a new hard row |
| PE §3.2 | Opposing institutional personas; archetypes A/B/C; NL what-if → typed overrides | Brief §6 grafts 4, 5, 7, implemented through PC §6.5 and PB/PD controls |
| PE §4 | Phased roadmap framing | Brief §6 graft 8 |

---

## 5. Cross-cutting engineering findings

### 5.1 Performance: what the benchmarks show (SYNTHETIC structures)

**Here-and-now LP.** Every PA–PD design rejects SYN §4.8's asset-level 12-quarter stochastic MILP (≈1.8M variables per 1,000-leaf tree, "tens of minutes on HiGHS"). Every one keeps integrality in a small post-LP selection MILP over ≤ 30 coupling rows (SYN §4.4), where HiGHS MIP is fast: ≤ 600 binaries (PD), ≈1,050 (PB), ≈1,600 (PC). This is the decisive engineering call, and all four make it.

| Configuration | Source | Size (columns / rows / nnz) | Reported | Judge re-run (machine at 100% load) |
|---|---|---|---|---|
| PA default, 1,200 leaves × 8 periods, PWL utility + CVaR + running max | PA §4.8.3 | 227k / 202k / 0.86M | 53 s IPX (cold); CLARABEL 98 s | **224.2 s IPM + crossover** (94 IPM iterations, as PA reports); **399.3 s dual simplex**; objectives equal |
| PA 1,200 × 12 and 2,000 × 8 | PA result files | 419k / 356k / 1.56M; 359k / 321k / 1.36M | not converged in 300 s | — (files confirm) |
| PC 500 leaves (fan), with CVaR row | PC §4.11 | 132k / 103k / 0.52M | 20.2 s IPM; 109.5 s dual simplex; 80.8 s CLARABEL | **90.7 s IPM; 124.0 s dual simplex**; both objectives −167.797, matching PC's |
| PC 1,000 leaves | `hn_lp_bench_20x50.json` | 261k / 204k / 1.02M | 136.3 s IPM; 571.4 s DS; 207.5 s CLARABEL | — |
| PD 600 × 12, no CVaR | PD §4.11 | 177k / 134k / 0.70M | 32 s dual simplex | **97.2 s DS; 173.0 s IPM + crossover** |
| PD 600 × 12 **plus a binding RU-CVaR row** on a signed leaf margin (T6 surrogate) | judge addition | 177k / 134k / 0.71M | — | **78.5 s DS; 231.8 s IPM + crossover**; CVaR dual −0.505 in both; objectives agree to 1e-9 |
| PB interactive, 3 × 400 leaves | PB §4.10 | ≈244k / 119k / 1.2M | 30–90 s IPM **[I], unmeasured** | — |

What follows:
1. **The faster algorithm depends on the tree's shape and on the thread policy.** On PD's branching tree, single-threaded dual simplex beats single-threaded IPM by 1.8–4× (PD's 500 × 8 runs and my 600 × 12 runs), with or without the CVaR row. On PA's tree (branching to Q4, short fans, PWL utility rows), IPM beats dual simplex by 1.8× (224 s against 399 s in my run). On PC's single-path-fan tree, IPM wins by 5.4× in PC's run but only 1.4× in mine (90.7 s against 124.0 s). The likely reason is that HiGHS 1.15.1's `ipm` can run the parallel HiPO interior-point code (the options include `hipo_parallel_type = both`, `threads = 0` auto). With free cores it is fast; on a saturated machine it is not, while dual simplex is serial either way. A design that fixes one algorithm in advance (PD prefers dual simplex, PC prefers IPM) is betting on its own tree and its own core count. Must-fix 1 (§8): benchmark the production tree under the evaluator's real thread policy and race the two algorithms (or use HiGHS's automatic choice), with crossover always on when duals are read.
   - *Determinism corollary.* A multi-threaded IPM on a degenerate LP can land on a different optimal vertex after crossover, and so return different duals, at different thread counts. PD pins the evaluator to one thread (§2 P11). PA and PC run with defaults. Evaluator solves must be single-threaded, or proven vertex-stable, with every solver option recorded in the manifest. Speed comes from parallel processes (SAA replications, models), not from threads inside one solve.
2. **The CVaR surrogate does not break PD's solver choice.** Adding the dense T6 row did not slow dual simplex on PD's structure; it was slightly faster (78.5 s against 97.2 s), possibly because the binding row prunes the feasible region.
3. **Absolute times are load-sensitive by 3–4.5×** (PA's IPM 53 → 224 s, PC's 20 → 91 s, PD's dual simplex 32 → 97 s on my saturated machine). The proposals' numbers were also taken under load. Expect ≈20–60 s for a 130–230k-column production H on an idle laptop. That fits the 2-minute target only if Phase I is cheap (deterministic root rows, as PA's Phase I-a and gap_02's linearised t₀ block), not tier-by-tier re-solves of the full tree (PB §4.10).
4. **The brief's 2,000-scenario × 20-quarter corner is not interactive on HiGHS in any design.** PD (286 s for 2,000 × 12) and PA (time limit) agree. Treat it as overnight, as PA and PD do.

**Policy simulator.** PD measured a simplified asset-level engine at 10.9 s per 10k × 40 on one process (5.9 s on four), and PC measured a cohort kernel at 3.96 s on 8 threads (`sim_kernel_bench.json`). With PD's 2.5× and PC's 5–8× fidelity reserves, the 60 s target is credible on 8 cores. PA (10–30 s) and PB (≈52 s) are estimates only. PB's estimate is the tightest and should be benchmarked first.

### 5.2 Environment conflicts inherited from the research
- SYN §4.8 says "Gurobi's `feasRelax` with `minrelax=True` implements both stages" of Phase I, and SYN §10's stack lists numba or JAX, chainladder, scoringrules, Pyomo with mpi-sppy, pycma, Optuna, QuantLib/ORE, SDDP.jl via juliacall and commercial MILP. Only numba and cvxpy/HiGHS/CLARABEL/OSQP are installed (§1). Each final-architecture module must name its in-house replacement: Benktander and Mack in numpy; WIS/CRPS in numpy; CMA-ES in numpy or scipy DE; SSVI, Black and Bachelier closed forms as pricing references in place of QuantLib (gap_03 §9 T1 references); SDDP deferred.
- gap_02's `phase1_demo.py` already implements lexicographic Phase I in cvxpy. The production version should be explicit elastic LPs per tier with previous-tier violations bounded (u_Tj ≤ u*_j + δ). HiGHS's `feasibilityRelaxation` minimises one weighted violation. PA §4.8.4 and PD §4.11 run it "per tier" without saying how earlier tiers' violations stay bounded when the next tier runs, and the function does not do that by itself.
- Opus 5.5 constraints (brief §3) are handled correctly by PB §5.17, PC §5.2 and PD §5: adaptive thinking always on, explicit effort, `tool_choice` auto, strict schemas, `messages.parse`.

### 5.3 Research updates the proposals do not carry (all four would need them)
G-gap_02 was written at 15:28, before or during proposal drafting. None of PA–PD reflects it (a search for "census v1.1", "V24" and "16.4" finds nothing):
- **Census v1.1** seals PE unfunded at $16.4bn rather than $27.4bn (total $27.0bn), pending user confirmation. It moves the T4 facility need, the drought cash map and L8 from 0.81 (breach) to 0.75 (G-gap_02 §0, §7). The generator must version censuses as hashed configs and carry both.
- **FBE-R replaces the production FBE.** The baseline FBE fails four pre-registered misspecification gates. FBE-R uses a Huber bias regression on [1, D, gap, flag], pooled across groups, whose covariates include the optimizer's own SELL flags and envelope status (G-gap_02 §3). This creates a **feedback edge from `core` to `beliefs`**. It must read the *previous* quarter's frozen outputs to keep the pipeline acyclic, and G2's freeze must hash them.
- **κ_g redefined** as the true/stated 80% width ratio, replacing κ_conf (G-gap_02 §5). PA–PD use κ_g already, so this is consistent, but the generator's q₁₀/q₉₀ formula changes.
- **O3 becomes `perf_module.py`,** deterministic with 17/17 golden tests (G-gap_02 §4). Port it as is.
- **Gate V24:** one EV draw per company per path keyed by `company_id` in the SeedSequence hierarchy; overlap bands; GP ≤ 5% on the graph, with 35% of sampled censuses breaching it (G-gap_02 §6). This affects the RNG design (PA's counter key needs a `company` slot) and the synthetic generator.
- G-gap_01 §0 item 2 puts θ\* at 0.79 pooled (facility need $14.6bn) rather than 0.76. Only PD notes this (§4.12).

### 5.4 Inconsistencies between proposals that the composite must settle
| Item | PA | PB | PC | PD | Recommendation |
|---|---|---|---|---|---|
| Money units | W₀ = 1 | US$m float32 | $bn | $bn float64 (ledger, LP), float32 (cubes) | PD's, with PA's W₀ scaling inside the LP for conditioning |
| Private clock | monthly | monthly gen, monthly ledger Q1–8 | monthly sub-steps | quarterly (pushback) | Monthly ledger for T3/T4′ in all cases; private engines quarterly only if an A1-style test passes |
| RNG | counter-based keyed tuple | Philox by (world, path, entity) | SeedSequence per block, draws outside `prange` | SeedSequence per path block | Counter-based keyed tuple incl. `company_id` (PA + G-gap_02 V24) |
| H tree | 24×4×2×2 + 3-leaf fans, 8 periods | 20×4×5 per model | 20 nodes + 25-leaf single-path fans | b₁ at Q1, b₄ at Q4, fan to 12 | Branching to Q4 (PA/PD); fan clairvoyance measured (PA A9) |
| LP algorithm | IPX + crossover | IPM | IPM after crossover | dual simplex, 1 thread | Race both; crossover on |
| Policy search | numpy CMA-ES | numpy CMA-ES | numpy CMA-ES | scipy DE (cma if justified) | Either; pre-registered |

---

## 6. Recommendation: base and composite

**Base: PD.** Keep its thesis ("ship a ledger, not an oracle"), the shared ledger kernel used forward (P), linearised (H) and on s\*(θ\*) (T4′), its Protocol layer, the measured performance budget, increments 1/v1/v2, the adapter pipeline and the research-code ports.

**Composite module map.**

| Layer | Take from | Notes |
|---|---|---|
| Contracts, units, Protocols | PD §3 + PC §3.3 shapes + PB §5.3 `AnalysisContract` | Frozen in week 2 |
| RNG and determinism | PA §4.3 counter-based key (+ `company_id`) + PD §4.2 regenerate-and-verify + PC §2.2 draws outside kernels | One determinism test suite |
| Engines (scen, priv, pub, overlay, liab, ledger) | PD §4.3–4.9, with SYN §4 and GROUPS §3 for content | Monthly ledger for T3/T4′ |
| H, Phase I/II, duals, selection | PD §4.11 + PA §4.8.4–4.8.6 (Γ certificate, one-sided duals, ranging, μ − M > 0) | Production benchmark gate in sprint 1 |
| Verification | PA §4.12 error ledger and consistency contract + PD §8 matrix | CI fixtures; nightly on the book |
| Lab and agents | PD §5 trust boundary + PB §5.4, §5.7, §5.10, §5.16, §7 (DSL, failure taxonomy, placeholders, drills, planted-effect calibration) | Seal service in a light form: commit-reveal file + separate evaluator instance |
| IC layer | PD §6 + PC §6.1 Register and evidence compiler (v1), §6.5 computed shadow IC, §6.6 W1 self-test | Register restricted to MVP decisions Q1, Q2, Q4, Q5, Q6 in increment 1 |
| Synthetic data | GROUPS §6 + G-gap_02 (census versions, FBE-R gates, O3, V24) | `data_class` hard error (PC §7) |

---

## 7. Prioritised graft list

1. **PA §4.12:** error ledger A1–A16 and the consistency contract, as CI fixtures and nightly book checks.
2. **PB §5.10:** rendered claims with typed placeholders and a digit-rejecting validator.
3. **PA §4.8.5–4.8.6:** the selection certificate Γ, one-sided duals ("at a kink"), RHS ranging and the μ − M > 0 test; publish an FTP band when duals are unstable.
4. **PA §4.3 + G-gap_02 §6:** a counter-based RNG keyed by (seed, world, plane, path, month, source, slot, company_id), so CRN, thread independence and V24 identity hold together.
5. **PB §5.16 and §5.7:** the integrity drill suite and the typed gate-failure taxonomy.
6. **PB §5.4:** the anchored-residual PolicySpec DSL with identity at zero (exact switch-off null).
7. **PC §6.1:** Decision Register plus evidence compiler ("EVIDENCE MISSING", never silent fill), starting with the five MVP decisions.
8. **PC §6.5:** computed shadow IC via `implied_actions(q_k, θ_k)` with θ_k in Θ; this is PE's opposing-utility idea (graft 4) made P1-safe.
9. **PB §7:** planted-effect lab calibration (true gain, leak, null world) to set ε_mat and budgets.
10. **PC §4.11:** parallel SAA replications for dual and envelope bands; crossover before reading duals.
11. **PC §6.6 / PD §6:** JavaScript entropy pooling with golden vectors, an in-browser self-test and Python recomputation of logged numbers.
12. **PA §4.12 A9:** fan-clairvoyance test on whatever tree is adopted.
13. **PB §5.2 B4–B5:** commit-reveal final seeds and a hash-chained ledger, in a light form on the laptop.
14. **PE §2.2, §3.1, §2.4, §3.2:** market-implied fourth signal; Zombie-NAV, P(forecast achieved within k quarters) and catalyst rule; CVaR₉₉ VM in T3 plus the stress-coverage ratio on the offset card; archetypes A/B/C as frozen controls; NL what-ifs as member-confirmed typed overrides.
15. **PB §5.15:** the per-campaign cost model, with caching and Batch for seat assessments.

---

## 8. Must-fix list (regardless of base)

| # | Must-fix | Why / evidence | Acceptance test |
|---|---|---|---|
| 1 | Production-fidelity H benchmark in sprint 1 (CVaR T6 surrogate, PWL utility, L2 shortfall, T4′ root rows, path-min headroom, ≈400 asset columns), with automatic algorithm choice (race IPM+crossover against dual simplex) and a fallback ladder (smaller tree → model-wise solves → overnight Benders) | The faster algorithm flips with tree shape (§5.1); PB is unmeasured; PD's bench omits rows | `tests/perf`: quarterly H ≤ 120 s on the reference laptop, nightly |
| 2 | Lexicographic Phase I as explicit elastic LPs per tier, with previous-tier bounds, on deterministic root rows first (Phase I-a), then CVaR rows only on failure; IIS by `getIis` or a row-family deletion filter; Phase-I duals labelled "infeasibility prices" only | L15; gap_02 §4; SYN §4.8 relies on Gurobi; `feasibilityRelaxation` alone does not chain tiers | gap_02's 8/8 and G-gap_01's 18/18 suites ported; Phase-I closed form; penalty ×10 invariance |
| 3 | Duals read only from a basic solution (crossover on); `priced_on` on every card, envelope and FTP point; envelopes refused from pinned or reverse-stress solves | Pinned-dual detection needs complementary slackness (PC §4.11); G-gap_01 §0 item 6 | CI fails any card with `priced_on` ≠ feasible/restored, or a dual within tolerance of a penalty tier |
| 4 | Dual-stability protocol: bootstrap bands across SAA replications, sign-flip flags, hysteresis, EWMA-published FTP, "at a kink" labels, H–P ranking test | PA §10 and PD §10 both rank it the top risk | Kendall τ ≥ 0.8 (PD §4.11); bands printed on every card |
| 5 | One determinism contract: counter-based keyed RNG (incl. `company_id`) or block-keyed draws generated outside parallel kernels; evaluator LP solves single-threaded (`threads = 1`, fixed `solver`, `random_seed`), or a proof that multi-threaded HiPO returns the same vertex after crossover; every solver option recorded in the manifest; pinned HiGHS, numba and numpy versions; golden manifests reproduced bit for bit | PC's measured `prange` non-determinism; HiGHS 1.15.1's parallel HiPO IPM (§5.1); brief P11 | Same checksum and same duals at 1, 4 and 8 workers; golden-manifest regression |
| 6 | Package policy in writing: no JAX, Pyomo/mpi-sppy, Optuna, QuantLib/ORE, chainladder, scoringrules, PyMC, SDDP.jl; `cma` only as a justified pure-Python addition; a licence note for the SIMM-like engine (SYN §4.6 "Licensing") | SYN §10 stack vs installed environment (§1) | `pip check` plus an import-allowlist test in CI |
| 7 | Fold in G-gap_02: census versioning (v1.0 and v1.1 as hashed configs, user to confirm), FBE-R with lagged optimizer covariates (acyclic pipeline), κ redefinition, the `perf_module.py` O3 port (17/17 tests), gate V24 | §5.3 | V1–V24 green on both censuses; DAG check that `beliefs` reads only frozen prior-quarter `core` outputs |
| 8 | Clock decision recorded: monthly ledger for T3/T4′ and VM in every design; a quarterly private clock only if an error-ledger test shows ΔP(red) ≤ max(0.1pp, 2 SE) | SYN §2.1 monthly engine vs PD §4.1 | A1-style test on 2,000 CRN paths |
| 9 | User-confirmed semantics encoded as schema enums and tests: REFINANCE = cash-out with exposure unchanged; LEVER = exposure-up (≡ ADD + REFI); in Mode B the draw is never an optimizer column; no indicator or P(10%) term in any objective (lint) | Brief §6 user answers; SYN L9 | Unit tests: an exposure-delta check per lens; an objective-term linter; LEVER ≡ ADD + REFI |
| 10 | Out-of-process evaluator as the only tool host (MCP stdio); agents with no file, shell, code or network tools; per-request hash checks; a separate final-plane instance and cache; engine-side counting including failures; Windows isolation limits disclosed | Brief P2–P4; PB §5.2; PD §5 | PB §5.16 drills in CI |
| 11 | Provider-agnostic `LLMBackend`: Anthropic default (`claude-opus-5-5`, explicit effort, strict tools, `messages.parse`, auto tool choice, refusal handling); Replay keyed by canonical-request SHA-256 that fails closed; Stub; engines never import agents | Brief P10, P12, §3 | Full offline campaign in CI on Replay; layering test (PA §8) |
| 12 | Synthetic labelling and taint in code: `SYN-` ids, `is_synthetic`, `data_class` (mixed = hard error), a footer on every chart and table, a claim-validator rule against attributing synthetic numbers to ADIC | Brief R15, P15; GROUPS §6 L1–L8 | 100% labelling audit in CI |
| 13 | Real-data adapters: schema validation, unit/currency/basis tags, bitemporal load, quarantine for unknowns, fixture contract tests; an operator flag before any holding-level content enters a prompt; in-region serving before real data | Brief P13; SYN §5.7, §7.2 | Adapter contract tests; a prompt-redaction test |
| 14 | Client-side W1 entropy pooling: JavaScript port with golden vectors, an in-browser self-test that disables W1 on mismatch > 10⁻⁶, and Python recomputation for any logged number | No Node in the environment (brief §3) | Golden-case test from the Python side |
| 15 | Reconcile any added Tier-1 rows (PC's LM) with T3/T4′ canonical conventions before adoption; no new hard row without recalibrating the recovery trigger | §3.3; gap_02 §1.1 | Phase-I result unchanged on the canonical fixture unless intended |

---

## Appendix A. Verification runs

All runs used the project venv (`.venv\Scripts\python.exe -I`) on the Core Ultra 9 285HX while the groups gap_04 Shapley job held the CPU at 100%. Scripts are in the session scratchpad folder `judge_eng`.

| Run | Command | Result |
|---|---|---|
| Environment inventory | `importlib.metadata` listing | 89 distributions; absences as in §1 |
| highspy API | `dir(highspy.Highs())` | `feasibilityRelaxation`, `getIis`, `writeIisModel`, `getRanging`, `setBasis`, `getDualRay` present |
| CVaR effect on PD's tree (`cvar_effect.py 600 12 30 600 45`) | PD `bench_lp.build()` unchanged, plus RU-CVaR at 99.4% on leaf margin C − 0.06W, bound set 45 below the unconstrained CVaR so it binds (a probe at S = 100 showed binding from 40) | Base: DS 97.2 s, IPM + crossover 173.0 s. With CVaR: DS 78.5 s, IPM + crossover 231.8 s; objective −56.168 in both; CVaR dual −0.505 in both |
| PC 500-leaf re-run (`hn_lp_bench` copy, `20 25 highs-ipm,highs-ds`) | PC's script unchanged, copied so as not to overwrite PC's JSON | IPM 90.7 s, dual simplex 124.0 s; both objectives −167.797 (matches PC's CLARABEL objective); all cash-row duals non-zero, no elastic cash used |
| PA default re-run (`pa_default_rerun.py 400`) | PA `h_tree_bench.build((25,4,2,2), 3, 4)` unchanged; IPM + crossover and dual simplex only | 5,526 nodes, 1,200 leaves, 227,098 × 202,041, 857k nonzeros. IPM + crossover 224.2 s (94 iterations), dual simplex 399.3 s (162,541 iterations); objective −0.113153 in both |

## Appendix B. Compliance with research findings and user definitions

| Requirement (source) | PA | PB | PC | PD | PE |
|---|---|---|---|---|---|
| λ from a feasible (restored) problem, with envelopes (L14, L15; gap_02 §4) | ✓ §4.8.4–4.8.6 | ✓ §4.9–4.10 | ✓ §4.10–4.11 | ✓ §4.10–4.11 | ✗ (Bellman λ only) |
| CI fails any card on a penalty-pinned dual (SYN §5.5) | ✓ extended | ✓ Gate 1(g) | ✓ | ✓ 8/8 + 18/18 | ✗ |
| Tier 1 first; ≤ 1% red event binding; P(10%) reported only (SYN §1, §4.9) | ✓ | ✓ | ✓ | ✓ | ✗ indicator in objective |
| Explicit return bridge (gap_05) | ✓ | ✓ | ✓ | ✓ | ✗ |
| T4′ = s\*(θ\*) with canonical conventions; T6 bands by model class (gap_02) | ✓ | ✓ | ✓ (LM row to reconcile) | ✓ (θ\* 0.79 noted) | ✗ |
| Overlay as a position layer, OV1–OV3 (gap_03) | ✓ | ✓ in `correct` | ✓ | ✓ | partial (Greeks named) |
| F_t distinct from k_MS (gap_04) | ✓ | ✓ | ✓ | ✓ | ✗ |
| Group layer: four groups carry PE; HF state machine; P2S; three marks + market anchor + credibility (GROUPS) | ✓ | ✓ | ✓ | ✓ | partial (strategy-group bias only) |
| REFINANCE = cash-out; LEVER = exposure-up (brief §6) | ✓ §4.6 | ✓ §4.6 | ✓ §4.6 | ✓ §4.6 | ✗ inverted |
| Owner-set distribution exogenous (brief §6) | ✓ §4.7 | ✓ §4.8 | ✓ §4.9 | ✓ §4.9 | ✗ decision with utility |
| No commercial solver; MILP kept out of the tree (brief §3) | ✓ | ✓ | ✓ | ✓ | ✗ |
| Synthetic labelled and generated from documented truth (R15) | ✓ | ✓ | ✓ | ✓ | ✗ |
| G-gap_02 updates (census v1.1, FBE-R, O3, V24) | ✗ | ✗ | ✗ | ✗ | ✗ |

*SYNTHETIC – NOT ADIC DATA (every timing, count and probability in this report).*
