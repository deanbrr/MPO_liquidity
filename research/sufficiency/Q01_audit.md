# Q01 audit: is there a sound, buildable multi-period optimizer, solvable on HiGHS/CLARABEL within target?

*Research-sufficiency audit, 2026-10-18. Design-stage files were not audited. Every [I-calc] number is SYNTHETIC, not ADIC data. [audit-calc] marks this audit's own arithmetic on corpus inputs.*

**Verdict: PARTIAL.** Design-ready and buildable at Phase-0 scale. Whether it runs within the performance targets is not established, and the research's own estimates contradict the 2-minute HiGHS target for the program as specified.

## 1. Answer today

**Formulation: yes.** The research combines Powell's policy classes into one core (synthesis §4.8, L10; C1 §5):
- **P**, a ≈20-parameter, cushion-monotone standing policy. It is tuned by CMA-ES or Bayesian optimization on 10k common-random-number paths per model, then certified on fresh 50k paths with one-sided Clopper–Pearson bounds: p̂ = 0.90% passes a 1% gate, 1.00% fails [I-calc, C1 §5.7].
- **H**, a 12-quarter here-and-now stochastic MILP. Stage 1 is at asset level; recourse is at group level under linear decision rules. Rows are elastic, with penalty tiers 10⁴ > 10³ > 10² > 50 > 10, and CVaR is applied to signed margins. Its cash-row duals form one kernel that prices SELL/HOLD/REFINANCE/LEVER (synthesis §4.4).
- **Phase I/II:** duals are read only from a restored, feasible problem (gap_02 §4).
- **V** (regression terminal values now, SDDP later) and **F** (a QP safety filter).
- **Benchmarks:** certainty-equivalent MPC over 8 quarters, and HDP-in-the-loop.

All of this design content is [I]; the duality results are exact (synthesis L15).

**What has actually run** (all SYNTHETIC, all small):
- **Phase I/II on HiGHS (cvxpy).** A penalty-pinned dual of 100 prices a fund at 0.9% of NAV; the restored dual, 0.237, prices it at 76.8% [I-calc, gap_02 §4]. The pinned-dual tests pass 8/8 and 18/18 (gap_02 §5; groups synthesis §4.8; not re-run here).
- **A reduced H on HiGHS.** A one-year two-stage SAA LP over 10 × 1,000 paths, ≈3,000 variables [audit-calc, g04_run.py], yields envelopes and FTP: the T4′ dual is 0.046–0.051 at appetite and 0 at tolerance [I-calc, groups gap_04 §5]. It is "a one-year LP, not H itself" (§9).
- **A 40-asset HiGHS MILP.** Three prices reproduce 36 of 40 exact decisions; a price-only rule is $24.7m worse (dossier 08 §6.13, synthetic).
- **The only measured solver times.** A HiGHS MILP with 1,500 binaries × 30 rows at a 1e-6 gap took 1.7, 9.3 and 39 s; with 3,000 binaries, 4.4 s (08 verify R10).

**Solvability within targets: not established.**
- **H's size.** ≈1.8M variables per 1,000-leaf model tree and ≈5.4M for three models, solved decomposed overnight. What-if mode (2 models × 200 scenarios, ≈0.8M variables) takes "tens of minutes with HiGHS" [I, unbenchmarked; C1 §8; synthesis §4.8].
- **The targets.** The brief asks for a 500–2,000-scenario × 8–20-quarter LP in under ~2 minutes, and for ≥10k paths × 40 quarters × ~300 holdings in under ~60 s. Both are "to be confirmed in design" (brief §3).
- **Target versus estimate.** At the corpus's ≈150 recourse variables per node (01_mpo §4.2 [I]), the target LP has ≈0.6M–6M variables [audit-calc]. That is the size the research expects to take tens of minutes on HiGHS.
- **A smaller alternative, untimed.** Dossier 11 §7 calls a path-based LP with affine recourse "tractable for HiGHS or Clarabel" [I], but nobody has timed it.
- **P's runtime.** The only timing is 512 coalitions × 6 models × 10k paths in 54 minutes on 22 cores, on a 20-quarter group- and cohort-level engine [I-calc, groups gap_04 §6]. That is ≈23 core-seconds per evaluation [audit-calc], so the 60 s target is plausible but unproven at 40 quarters and 300 holdings.
- **MPC in the loop.** Certainty-equivalent MPC inside the simulator needs ≈400k solves, or 1–6 CPU-hours (01_mpo §4.2 [I]). Only rule policies can meet a 60 s budget.

**Plain answer:** the formulation is sound and buildable. H as written probably misses the HiGHS target; a reduced or path-based LP probably meets it. Neither is measured.

## 2. Evidence

**Strongest sources.**
- Dossier 01's verification log: 34 claims, 27 confirmed, 5 corrected, 0 refuted; overall MEDIUM, design formulas medium-to-low until fixed (fixes applied in C1 §2).
- The 01 literature check: 37 citations, none mismatched; "None of these overturns the three-layer architecture". The verdict on the optimization core is "Refined" (lit synthesis §4.9).
- Verifier fixes adopted in C1 §2 and synthesis §4.8, all [C]:
  - long-horizon floors move into P;
  - Clopper–Pearson replaces the scenario approach, whose exact bound is 631 / 31,785, not ≈1,000 / 60,000;
  - CVaR on signed margins, with elastic rows;
  - Shapley–Folkman is vacuous at ≈8,100 coupling rows, so price decomposition is only a heuristic;
  - VSS and EVPI only on a risk-neutral surrogate;
  - Boyd's timings are projections; the measured run was ≈0.5M problems in ≈30 minutes on 32 cores;
  - in Luxenberg, MPC and a simple heuristic are both "extremely close" to the fully liquid benchmark.

**Contradictions.**
1. **Target vs estimate.** Brief §3: under 2 minutes. C1 §8 and synthesis §4.8: tens of minutes on HiGHS. Dossier 01 §4.2: "seconds to about a minute" for 0.4M variables, solver unstated (all [I]). Only commercial solvers are credited with seconds-to-minutes (synthesis §4.8), and production plans commercial MILP (C1 D19; synthesis §10); the brief excludes them.
2. **H's role.** Synthesis §4.8 and C1 §5.6 make H a full asset-level MILP. The selection loop (synthesis §4.4; C2 §4.4; 08 §7) uses H only for duals: a separate MILP over ≤20–30 aggregated rows, then H re-solved with actions fixed, 2–5 times. 01_mpo §7 [S] lists CLARABEL for LP/QP/conic and HiGHS for MIP, so only HiGHS takes the MILP; its duals need fix-and-price (G8 dossier §7).
3. **Waterfall.** The literature "contradicts" P's fixed recourse waterfall (synthesis §4.8; lit §4.4). Brief §7.1 requires a tuned, state-dependent order.
4. **Dual bounds.** Brief §7.6 requires information-relaxation bounds for P. 01 verify R9 says a valid bound under Tier-1 CVaR and chance rows needs a constrained extension; 01 lit §4.2 names a candidate (abstract-level) but nothing specifies it.
5. **Decision rules.** Synthesis §4.8 uses linear decision rules inside the fans. The literature says they "can be inadequate" and recommends lifted rules (lit §4.9).
6. **Parameter cap.** The PolicySpec DSL allows ≤ 8 parameters (synthesis §5.5; C4 §5.3), but P has ≈20.
7. **Accrual.** C1 §5.5 still accrues payouts at 10%. Synthesis §4.9 (v1.1) accrues them at the fund's own return, and the synthesis governs.
8. **T6 pricing.** Once T4′ is slack, the binding price is T6's, carried by H's CVaR surrogate (ε′ = 0.60%). The groups synthesis (§4.4) calls this "an open item".

**Citation-audit errors that touch Q01.**
- Dossier 10 applies Heitsch–Römisch (2003), a two-stage method, to multistage trees. The fix is their 2009 filtration-distance method (lit §2.4 item 13).
- Klaassen (2002) is missing from dossier 01's reference list (lit §2.5).
- Synthesis §4.4 tags the synthetic 40-asset test [S]. It should be [I] (08 §8: "Example 3 is synthetic").

## 3. Readiness

| Level | Ready | Reason |
|---|---|---|
| DESIGN | Yes | Components, equations (C1 §5.3–5.9), dual kernel, Phase I/II, certification and rubric tests specified; verifier corrections applied |
| BUILD | Yes, at Phase-0 scale | Equations, interfaces (08 §7 `ActionBundle` / `DualSet`), Phase-I code and tests exist; synthesis §10 scopes H to 200–400 leaves. Open: production H form, tree method, libraries |
| IC ANSWER | No | "Sound formulation" is defensible. "Within targets" rests on unbenchmarked [I] estimates that conflict with the target |
| NEEDS ADIC DATA | No (for this question) | Formulation and benchmarks can run on SYN-ADIC-177; ADIC data only fixes production sizing (holdings, consents, facilities) and dual levels |

## 4. Gaps

| # | Gap | Impact | Close by |
|---|---|---|---|
| 1 | No here-and-now LP of 500–2,000 scenarios × 8–20 quarters has been timed on HiGHS or CLARABEL. Benchmark the full-tree H, the LP + aggregated-MILP loop and a path-based affine LP | High | build_experiment |
| 2 | Decide which H variant must meet the interactive target and which runs overnight, and confirm the provisional targets | High | user_decision |
| 3 | Recommended libraries are absent from the venv: Pyomo, mpi-sppy, pycma, Optuna, BoTorch, JAX. Present: cvxpy 1.9.3, highspy 1.15.1, clarabel 0.11.1, numba, scipy [audit check]. Decomposition and CMA-ES must be hand-built or installed; SDDP needs Julia or Gurobi | Medium | user_decision |
| 4 | No compute budget for the quarterly cycle, which stacks 10 SAA replications, 2–5 damping passes, ~300 forced-action re-solves, 20 bootstrap subsets and 3–6 models; none for HDP-in-the-loop (500–2,000 paths × 40 re-solves) | Medium | build_experiment |
| 5 | The chain duals → kernel → scores → MILP → re-solve has never run end to end on multi-period H duals (08 uses a deterministic ℓ; Phase-I demos a linearised t0 block; the reduced H stops at FTP) | Medium | build_experiment |
| 6 | T6 pricing through the CVaR surrogate is unresolved; test worst-case CVaR and ALSO-X (brief §7.4) | Medium | build_experiment |
| 7 | No constrained information-relaxation bound for P is specified | Medium | more_research |
| 8 | Filtration-distance tree reduction and lifted decision rules are not specified to code level | Medium | more_research |
| 9 | The H↔P agreement loop (λ^H_T, b^red, b^floor) has no convergence rule | Medium | build_experiment |
| 10 | The 60 s policy-evaluation target is unmeasured at 40 quarters × ~300 holdings | Medium | build_experiment |
| 11 | Decide whether the waterfall becomes a tuned parameter, and reconcile the PolicySpec cap with P's ≈20 parameters | Low | user_decision |
| 12 | Dual stability at scale is undemonstrated (Clarabel central duals, HiGHS ranging). The Phase-I "IIS" is a levers-at-capacity list, not a solver IIS (phase1_demo.py) | Low | build_experiment |
