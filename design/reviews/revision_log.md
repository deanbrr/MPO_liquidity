# Revision log: ARCHITECTURE.md and BUILD_SPEC.md, v1.0 → v1.1

**Date:** 2026-10-18 · **Author:** Chief Architect (design workflow, revision stage) · **Inputs:** `design/reviews/critique_quant.md` (QUANT-01 to QUANT-34) and `design/reviews/critique_build.md` (BUILD-01 to BUILD-41) · **Outputs:** `design/ARCHITECTURE.md` v1.1 (ARCH) and `design/BUILD_SPEC.md` v1.1 (SPEC).

> **SYNTHETIC – NOT ADIC DATA.** Every balance, probability, price, horizon, timing and count below comes from the synthetic working book, research prototypes or benchmark proxies.

## Summary

| Severity | Items | Fixed | Partially fixed | Rejected |
|---|---|---|---|---|
| Critical | 5 (QUANT-01, -02, -03; BUILD-01, -02) | 5 | 0 | 0 |
| High | 26 | 26 | 0 | 0 |
| Medium | 27 | 27 | 0 | 0 |
| Low | 17 | 17 | 0 | 0 |
| **Total** | **75** | **75** | **0** | **0** |

The revision ran in two passes. The first pass wrote ARCH v1.1 (ADR-37 to ADR-49, §8.12, the supersession table in §16) and SPEC's S-ADR-27 to S-ADR-44 and contracts (§0–§3). The second pass found that SPEC's module, H, data, agent, pack, plan and test sections (§4–§11) were still at v1.0 and contradicted those S-ADRs. It brought them into line, added SPEC §4.35 and the SPEC revision history, and made five small ARCH corrections. Every "Where changed" entry below refers to the final text. Where a fix was implemented differently from the critic's suggestion, the note says so; no suggestion was rejected outright.

One research figure was added in the second pass. `research/addenda/gap_02_calcs/gap02_results.json` stores M6's P99 facility-free gap ($7.37bn → θ = 0.58). Under the class-banded θ\* rule adopted for QUANT-08, the research fixture therefore gives θ\* ≈ 0.58, against 0.76 for the legacy worst-model rule. The first pass had said this value was not computed. SYNTHETIC: allocation v1, census v1.0, research conventions, gap_02's seed.

## Dispositions

ARCH = `design/ARCHITECTURE.md`; SPEC = `design/BUILD_SPEC.md`.

| ID | Severity | Action | Where changed | Note (what was done; reason if not as suggested) |
|---|---|---|---|---|
| QUANT-01 | critical | fixed | ARCH §5.2 (Tier 1B bands), §5.5, ADR-37; SPEC S-ADR-06 (amended), S-ADR-31, §3.14 `FloorSpec`, §3.18 `T6Screen`, §4.19 `test_tier1b_floor`, §4.20 `t6_screen`/`recovery_mode`, §4.27 Gate 1, §5.9 | The 10-year window is kept and re-certified at each quarterly re-solve on [t, t + 40]. CVaR₁₀% is banded by model class: +1/0/−2% for M1–M5 and MIX, —/−2.5/−5% for M6, misspecification report-only, all [I] for A1. Only capacity breaches trigger Phase I-b. Adds a regression test of SYN §4.9's binding at ≈14.3% vol |
| QUANT-02 | critical | fixed | ARCH §3.5, §4.4, §4.7, ADR-40; SPEC S-ADR-28, §3.10 `BeliefSet.alpha_a`, `BeliefDraws`, §3.17 `init(…, draws, world)`, §4.11–§4.12 engine equations, §4.15 `draw_paths(…, world)`, §6.9 | Beliefs enter as benchmark-relative α drawn per world and quarter, and engines add only α to the world's beta return. `test_engine_mean_log_return_by_world` checks this, and the 7.7% stylized fact on M1 gates the wiring |
| QUANT-03 | critical | fixed | ARCH §5.2 (red event), §5.10, ADR-39; SPEC S-ADR-05/-13 (amended), S-ADR-30, §3.1 `SaleReason`, §3.11 `RecourseOrder`, §4.14 `red_test`, §4.18 `t6_consuming`, §4.19 gambling detector, §4.27 Gate 2, §7.13 drill | A sale is red by economic substance: it is inside the forced waterfall, or the event stage is ≥ Amber, or IG + cash is below 8%, or the bid is more than δ_max below normal. The preemptive rung leaves `recourse_cover`. Adds a relabelling metamorphic test, a drill and the relabelling signature |
| QUANT-04 | high | fixed | ARCH §5.4, ADR-42, A19; SPEC S-ADR-33, §3.7 `GroupRates.u_per_nav`/`nav_share`, §5.2 (sales by age), §5.3 H1-cash/H1-NAV, §5.14 identity test with fixed SELLs | The buyer assumes κ^U of unfunded per $ sold. The age split of group sales is a contract field (`sale_age_allocation`: pro-rata default, mature-first alternative) |
| QUANT-05 | high | fixed | ARCH §5.4 TERMINAL, ADR-42, A24; SPEC §5.2 (`D^RA`, `IM`, `K`, `W_n`), §5.3 H1-W, H2f, TERMINAL, §5.14 cost-neutrality test | Real Assets sit at gross value with explicit debt and its transition. IM and residual overlay MTM are in W̃ and in the new W_n definition row. Adds a zero-NPV refinancing test |
| QUANT-06 | high | fixed | ARCH §5.4 H3; SPEC §3.18 `NodeCoefficients` (exogenous amounts removed), §5.3 H3, §5.14 conversion-invariance test | Every H3 term is linear in the node's state, so converting a non-red resource into cash leaves the row unchanged |
| QUANT-07 | high | fixed | ARCH §4.8, §4.10, §5.4, §5.6, §5.7 item 2, ADR-42; SPEC §4.18 `score`, §4.26 `kkt_interlock`, §5.3 H1-cash, §5.4, §5.8 KKT cap, §5.14 round-trip test | Every cost is charged once, in cash: the convex excess through segment variables, κ^GP through the charge state K. The objective has no money term, and the operational score is r_j − κ^irr. This differs from the critic's suggestion (keep the convex excess in κ, scaled by ū′) but meets the same test and removes the unit mismatch entirely |
| QUANT-08 | high | fixed | ARCH §4.9 θ\* rule, ADR-38, §5.5; SPEC S-ADR-32, §3.14 `Tier1Spec.theta_rule`/`theta_star`, §4.14 θ\* rule and tests, B13 | θ\* is class-banded: each class's quantile at its own tolerance share. The M6-at-1% rule survives as a prudence-overlay sensitivity, printed with its facility ask and the cap-binding θ signpost, and θ\* is recalibrated at G0. Research value ≈ 0.58 vs 0.76 (see Summary) |
| QUANT-09 | high | fixed | ARCH §5.2 T4′ appetite, ADR-29, ADR-38; SPEC S-ADR-32, §3.9 `StressReport`, §4.14, §5.2 `e^app`, §5.3 H6f | Appetite is ≥ 24 months on Treasury + Public Markets with no facility credit (G-gap_04 §5); the 36-month row is removed |
| QUANT-10 | high | fixed | ARCH §3.3, §8.5, ADR-21, ADR-46; SPEC S-ADR-36, §3.16 (draft models; `agent_judgment_probs` removed), §4.28 validator, §4.31 `minority_trigger`, §8.8 linter, §7.13 drill | No LLM-originated number is rendered, pooled or compared. Δp, dispersion and the influence cap are defined on engine outputs. Extracted numbers need 100% human verification, or dual extraction plus a sampled error-rate gate |
| QUANT-11 | high | fixed | ARCH §2.2, §4.7, ADR-43, §9.3–9.4; SPEC S-ADR-27, §3.5 `Mark`/`ForecastRecord`/`CaseMap`, §4.15 `irr_translation`, §4.17, §6.5 O2/O4, §6.9, WP-05 | Brief §9 adopted: the archive exists. IRR/MOIC marks with cases translate to the forward basis via cash-flow history, mean-path profile and exit prior. Strategic covariates are 0 with an indicator before go-live. The synthetic archive takes ADIC's shape, and SBC and recovery run through the translation |
| QUANT-12 | high | fixed | ARCH §4.9 (readiness inside P), §11.5 B1, A20, ADR-48; SPEC S-ADR-38, §4.14 `readiness_reading`, §4.19 loop and performance, §10.1 B1 lines | Readiness comes from linear response vectors (≤ 0.1 s per 10k paths per quarter), with the full replica only on band exits. B1 is the sum of nine tested lines, 35.5 s |
| QUANT-13 | medium | fixed | ARCH §4.7 credibility, ADR-43; SPEC S-ADR-10 (amended), S-ADR-27, §4.15 `credibility`, `forecast_precision`, tests | κ_g uses the full archive; forecast precision is capped as × min(1, 8/h) |
| QUANT-14 | medium | fixed | ARCH §4.8 CF row, §4.9 conventions, ADR-35, ADR-38; SPEC S-ADR-12/-20 (amended), S-ADR-32, §3.2 `fund_distribution_stress`, §3.3 `Facility.credit_stress`, §3.9 `ConventionSets`, `RAStressConvention`, §4.14, §5.9, §6.6 | The lab prices on the internally consistent set: ≤ 50% revolver credit in s\*, OV2-consistent opportunistic loss, lag 2, Real Assets stressed income. The research set prints as a sensitivity until A1, and `dist_mult` is decoupled from red-tier membership |
| QUANT-15 | medium | fixed | ARCH §5.4 H1; SPEC §3.7 `GroupRates` (simple returns, overlay coefficients) and fan compounding, §3.18 `NodeCoefficients`, §5.3 H1-cash/H1-NAV, §5.14 semiannual identity fixture | Premium, opportunistic P&L (incl. VM), opex and undrawn fees now sit in the cash row. Adds simple returns, compounded fan coefficients and lags mapped by period length |
| QUANT-16 | medium | fixed | ARCH §6.8; SPEC §4.13 `test_services_entity_pnl_sums_to_external` | The external-interest row is restored; a test checks that entity P&Ls sum to external P&L |
| QUANT-17 | medium | fixed | ARCH §4.8 reading rules, ADR-49, ADR-36; SPEC §3.13 `lever_breakeven_financing_a`, `lever_legs`, §4.18 rule and `test_lever_additive_rule` | LEVER is read additively: it pays iff α\* − risk exceeds the all-in financing cost. Cards show both legs |
| QUANT-18 | medium | fixed | ARCH §5.4, §5.7 item 5, A8; SPEC §3.12 `exact_objective`, §3.14 `h_utility_tangents = 48`, §4.3, §4.21, §5.3 UTILITY, §5.6, §5.11, §5.14 `test_a8_decision` | A8 is stated on decision-relevant error, with exact utility at the solution and the top-k alternatives. Adds 48 adaptive tangents and a nightly CLARABEL power-cone reference; Γ and forced re-solves are judged on exact utility |
| QUANT-19 | medium | fixed | ARCH §4.1, §7.5–7.6, ADR-45; SPEC S-ADR-35, §3.14 `PlaneSpec.b2_mode`, §4.10 B2, §4.27 Gate 3 | B2 is labelled a model-family hold-out by default. The out-of-time variant requires E, the filter and F_t calibrated through 2015 |
| QUANT-20 | medium | fixed | ARCH §5.2, §7.6; SPEC §3.6 `WorldSpec.t6_class`, §3.14 `GateSpec.pbo_source`/`ni_worlds_*`, §4.27 Gates | PBO is computed on the search ledger. B1 and B2 join the M1–M5 class; misspecification worlds join the M6 class (report-only for Tier 1B and non-inferiority). The NI world sets are now defined |
| QUANT-21 | medium | fixed | ARCH §4.1, ADR-45; SPEC S-ADR-35, §3.6 `FactorModelParams.df`, §4.2 `student_t(standardize=True)`, §4.10 algorithm and tests | t innovations are standardized, with vol and correlation tests. The anchor is E[Σ log(1 + r)] |
| QUANT-22 | medium | fixed | ARCH §5.4, §5.6, §11.5 B2, ADR-48; SPEC S-ADR-38, §3.12 `DualQuality.method`, `resolve_counts`, §4.20 `dual_quality`, §5.8 rule (3), §5.14 B2 | Dual quality comes from ranging, with ≤ 10 FD rows on the quarterly path and full FD nightly. `test_b2` runs every mandated re-solve against per-step budgets: ≈ 113 s, ≤ 2 s per re-solve |
| QUANT-23 | medium | fixed | ARCH header, §1.1 (R16), §15 (Q2 closed), §16 supersession table; SPEC §0.2 | ARCH v1.1 adopts S-ADR-01 to S-ADR-44, and the supersession table lists every v1.0 statement that changed |
| QUANT-24 | medium | fixed | ARCH §4.7 fusion; SPEC S-ADR-10 (amended), S-ADR-27, §4.15 algorithms and `test_equal_weights_default` | Equal or screened weights by default, with Ω̃ in the variance only. GLS is a variant gated out of sample on the archive |
| QUANT-25 | medium | fixed | ARCH §5.2 T1, §5.5; SPEC §3.18 `contracts.rules.instalment_bn`, §4.1 `test_rules`, §4.8, §5.9 | The payout floor is annual; each instalment is the remaining amount ÷ instalments left |
| QUANT-26 | low | fixed | ARCH §5.6; SPEC §5.8, §5.14 `test_kernel_two_node` | The kernel product runs over strict ancestors |
| QUANT-27 | low | fixed | ARCH §4.12; SPEC §4.25 `k_ms` and golden test | Loss sign: f = −R̄, τ = −7% |
| QUANT-28 | low | fixed | ARCH §4.4; SPEC §3.2 couplings, §4.11 | 20-quarter kernel with yearly weights; time unit set in config |
| QUANT-29 | low | fixed | ARCH §4.1; SPEC §4.10 `monthly_shock_matrix` and test | Principal 12th root with non-negativity repair |
| QUANT-30 | low | fixed | ARCH §4.8 instrument table; SPEC §4.18 classification and `test_exposure_delta_every_instrument` | A lower-strike sale is a partial SELL; CF liquidity borrowing is REFINANCE |
| QUANT-31 | low | fixed | ARCH §4.0, §5.13 A1; SPEC §4.19 A1 test | ≥ 20,000 CRN paths (or importance sampling) with a fixed 0.1pp bound |
| QUANT-32 | low | fixed | ARCH §4.12, §8.7, A15; SPEC §4.25, §8.4, §4.35 | One rule: ESS warns at 0.5N and blocks at 0.2N; KL gates at 0.05/0.20/0.35/0.80, since ESS/N = e^{−2KL}. CHAT_ANALYST still repeats the old gates; SPEC §4.35 overrides them (see below) |
| QUANT-33 | low | fixed | ARCH §5.10; SPEC §4.24 `successive_halving`, §7.7 | Rungs of 2,000/6,000/10,000 paths give 138k vs 270k path-evaluations, a 1.96× saving |
| QUANT-34 | low | fixed | ARCH §5.4 H5; SPEC §5.3 H5 | H5 uses (1 + r_{f,q})^{12} |
| BUILD-01 | critical | fixed | ARCH §3.5, §4.9, ADR-41; SPEC §1.3, S-ADR-29, §3.8 (`sale_red` deleted; `by_recourse_unit`), §3.17, §3.18 `RecourseAvailability`/`RecourseOutcome`, §4.11–§4.12, §4.14, §4.19 loop and tests | Three-phase protocol: engines quote; the ledger executes and books proceeds once; engines apply the outcome before t + 1. Tests cover zero post-sale flows, conservation, and H–P agreement on the first red month |
| BUILD-02 | critical | fixed | ARCH §4.1, §11.6, ADR-45, Q10; SPEC S-ADR-35, §2 `data_public/`, §3.6 `BootstrapParams`, §3.7 `CubeMeta.proxy_factors`, §4.10, WP-41 | B1 and B2 run on the panel's columns, with E-conditional fills labelled PROXY. Parameters without data ship as [I] "set and verified". WP-41 (a human with network access) snapshots the missing series |
| BUILD-03 | high | fixed | SPEC S-ADR-39, §1.11, §3 preamble, §4.1 `load_yaml`/`load_json_payload`, `test_config_roundtrip` | External data is validated in JSON mode, and models are never used as set members |
| BUILD-04 | high | fixed | ARCH §3.5, ADR-40; SPEC S-ADR-28, §3.10 `BeliefDraws`, `alpha_a`, §3.17, §4.0, §4.15, `test_draws_per_world` | Same fix as QUANT-02, plus shared GP effects and the `_a` suffix |
| BUILD-05 | high | fixed | ARCH §3.5, §11.5 B1, ADR-48; SPEC §1.7, S-ADR-25 (amended), S-ADR-38, §4.2, §4.10–§4.14 performance lines, §10.1 B1 table, `test_b1_profile` | Nine-line allocation summing to 35.5 s. Adds four-lane Philox with cached keys, tabulated inverse CDFs, the linear readiness reading, and group rates over 12 quarters only |
| BUILD-06 | high | fixed | As QUANT-22 | — |
| BUILD-07 | high | fixed | ARCH §11.5 B12–B17; SPEC §4.31 `implied_actions`, §6.9 blocking policy, §9.3, §10.1 B12 stage table and B13–B17 | B12 is budgeted by stage (≈ 28 min). Implied actions re-weight cached paths; controls run at the race count; V16–V18 become release jobs; column construction has its own line |
| BUILD-08 | high | fixed | ARCH §8.12, ADR-44, §11.3–11.4; SPEC S-ADR-34, §2, §3.18 `contracts/analyst.py`, §4.0, §4.35 (new), §7.4, §7.11–§7.12, §8.1, WP-39/40, §9.4 #12, §10.1 B18 | The analyst is built: a thin slice in increment 1, the rest in v1. It is reconciled with `design/addenda/CHAT_ANALYST.md` v1.0, which appeared after the critiques. Its proposed S-ADRs become S-ADR-34(a)–(c), its WP-CHAT-01..11 map into WP-01/39/40, and two values it repeats from v1.0 are overridden |
| BUILD-09 | high | fixed | As QUANT-11; marks-archive adapter schema and contract test frozen in WP-05 (wave 1) | — |
| BUILD-10 | high | fixed | ARCH §11.2, ADR-46; SPEC S-ADR-36, §3.16 draft models, §4.29 `check_llm_schema`, §7.2, §7.4, §7.5, `test_llm_schemas_transform` | LLM roles emit draft models only, using `KeyValue` lists and named sub-models; CI checks the strict-schema transform |
| BUILD-11 | high | fixed | SPEC S-ADR-29, §3.18 (contexts and types with fields), §4.5 walking skeleton, §4.20 `t6_screen`, §4.27 `optimize_h -> HSummary`, §7.4 `compile_spec` (spec stored by hash), §9.1 wave-0 gate | The walking skeleton gates the contract freeze |
| BUILD-12 | high | fixed | ARCH §3.5; SPEC S-ADR-29, §4.20–§4.22 | Amended `select`, `price`, `phase2` and `project` signatures, recorded by S-ADR |
| BUILD-13 | high | fixed | ARCH §5.3; SPEC S-ADR-44, §3.14 buffer defaults, §4.23 `calibrate_buffers`, B17 | The outer calibration loop now has an owner, a stop rule, a cap and a budget |
| BUILD-14 | high | fixed | ARCH §4.1–4.2, ADR-45; SPEC S-ADR-35, §4.9 `simulate_filter` and test, §4.10 factors (`log_rv`, `short_rate`) | The filter's observables are in the cube; `simulate_filter` reproduces `forward_filter` on the panel |
| BUILD-15 | high | fixed | ARCH §5.11, A21; SPEC §3.11 `Observables.unit_values`/`group_values`, §4.19 producers and test | Producers added for the exit and shock posteriors, the ℓ_t lookup and per-unit observables |
| BUILD-16 | high | fixed | ARCH §3.5, §7.5; SPEC S-ADR-43, §3.6 `MisspecOverride`, §3.14 `book_variants`, §3.17 `EngineFactory`, §4.19 factory and test | Misspecification members are typed overrides applied by the engine factory |
| BUILD-17 | high | fixed | ARCH §11.6, ADR-47; SPEC S-ADR-37, §4.10 (8 factors), §6.9 blocking policy, §9.3 | ARCH §11.6 increment-1 fidelity is restored. Blocking gates are named, n/a gates don't block, and the census rule uses V6 + V1–V2 |
| BUILD-18 | high | fixed | ARCH §7.2, §11.7, ADR-47; SPEC S-ADR-37, §3.1 `RunMode`, §3.14 validators, §4.5 `synthetic_committee`, §4.27 `new_salt`, §4.31 `RoomService`, §4.34, §7.6, §9.4 #11 | New DEV/SYNTHETIC mode, refused in REAL mode; ACL drills are marked `requires_accounts` |
| BUILD-19 | high | fixed | As QUANT-18 | — |
| BUILD-20 | medium | fixed | ARCH §7.7; SPEC §4.4 `expected_max_z`, `max_z_quantile`, `deflated_improvement`, §7.7 | The two functions are split and the deflation formula uses the quantile; tests check 2.746 and 3.474 |
| BUILD-21 | medium | fixed | SPEC §2, §3.18 `FBEValidationSet`, §4.5 fixtures and fakes, §4.15 `fbe_variant`, §4.17, §6.9, WP-03/14 | The generators moved to `beliefs.validation`, one of the critic's two options, so `beliefs` needs no `testing` import; the gates config moved under `config/beliefs/`; WP-03 adds the fixture H and the fakes |
| BUILD-22 | medium | fixed | ARCH §5.7 item 2; SPEC §3.12 `Column`, §3.18 `RowIndex`, §4.18 `build_columns`, §4.20 `row_index`, §5.5 | Columns are keyed by RowKey, and the call order is stated |
| BUILD-23 | medium | fixed | As QUANT-04 (fixed pro-rata age split; counts updated in §5.2) | — |
| BUILD-24 | medium | fixed | SPEC §3.8 `UnitFinancing`, §3.9 `LedgerState.unit_debt_bn`, §4.11 `UnitFinancingBook`, §5.2, §5.3 H2d | The engine that owns a unit owns its financing. Flows, covenants and look-through leverage are covered, and H mirrors the financing through column coefficients |
| BUILD-25 | medium | fixed | SPEC §2 (`priv.profiles` removed), §3.18 `contracts.rules`, §4.0, §4.8, §4.14 | The instalment rule and the intra-quarter profiles now exist once |
| BUILD-26 | medium | fixed | SPEC S-ADR-42, §2, §4.27 `make_server`, §4.33, §10.6 owners | One metric file per WP, an engine registry and a single server factory; cross-module test owners are named |
| BUILD-27 | medium | fixed | SPEC §3.15, §4.1 `VOLATILE_FIELDS`/`canonical_artifact_hash`, §9.4 #4, #9, #10, §10.5 | The MVP questions are operational, artifacts compare by canonical hash, and the socket fixture allows loopback |
| BUILD-28 | medium | fixed | SPEC S-ADR-42, §1.13, §4.20 `solve_replications` | Worker functions are top-level and picklable, the numba cache is per plane, cubes regenerate inside workers, and start-up time counts in B2/B5 |
| BUILD-29 | medium | fixed | ARCH §11.7–11.8; SPEC S-ADR-40, §1.1 (`cryptography` allowlisted), §3.14 `SignOff`, §4.1 `signing`, §4.31 | Ed25519 signatures with DPAPI-protected keys and a signed roster; DEV mode uses a test key |
| BUILD-30 | medium | fixed | ARCH §5.10, §7.7, §11.5 B8; SPEC §3.14 `PlaneSpec.paths`, §4.24, §4.27 Gate 1, §7.7 evaluation-kind table, §10.1 B8 | Evaluations are charged by kind; the lab costs ≈ 16 core-hours (races ≈ 9, confirmations ≈ 7) against the 20 core-hour cap |
| BUILD-31 | medium | fixed | ARCH §11.5 B7; SPEC §4.26 `group_shapley`, WP-36, §10.1 B7, §10.2 weekly | The group game runs weekly with 32 antithetic permutations, ≈ 21 core-hours at the 36 s design budget (the exact game would cost ≈ 61; ≈ 102 at the 60 s target) |
| BUILD-32 | medium | fixed | ARCH A22; SPEC §5.14 B6 | Re-fusion is a first-order coefficient adjustment with a nightly exact check; failing that, FBE what-ifs go to W3 |
| BUILD-33 | medium | fixed | ARCH §7.13; SPEC S-ADR-41, §1.10 `ReplayDrift`, §4.29, §7.1 | Two-tier Replay keys; integrity drills gate on exact digests |
| BUILD-34 | low | fixed | SPEC §4.29 `LLMRequest`, §4.19 `SimResult`, §3.9 `credit_cash_a`, §3.18/§7.4 `dp_red_bucket` | All four defects fixed |
| BUILD-35 | low | fixed | SPEC S-ADR-42, §2 `.gitattributes`, §4.1 LF hashing and test, §10.5 | Text is hashed with LF line endings |
| BUILD-36 | low | fixed | SPEC §4.14 θ\* grid test, §4.15 FBE gate test, §10.4 | θ\* is tested by interpolation on the ported grid (0.58 class-banded, 0.76 overlay). FBE gate outcomes are re-derived under the S-ADR-10/27 estimator before the first scored release; until then the tests check mechanisms |
| BUILD-37 | low | fixed | SPEC §1.2, §3.6 `factor_kinds`, `StateSnapshot.factor_levels0`, §3.7 `CubeMeta`, §4.10 | Factor kinds are declared, spreads are stored as levels, and vol states exist in one copy |
| BUILD-38 | low | fixed | SPEC §3.7 `TreeSpec.worlds` (no default), §3.14 `model_weights`, §4.24, §4.27 | World sets and weights come only from the contract template. B1 enters Gate 1, never Ψ_τ |
| BUILD-39 | low | fixed | SPEC S-ADR-41, §4.30 `ToolFirewall` | Tool lists are fixed per transcript; allowlists are enforced with `is_error` results |
| BUILD-40 | low | fixed | SPEC S-ADR-13, §3.7 `crowding_index`, `GroupRates.hf_phi`, §4.10, §4.12 | The crowding index is exogenous, and `hf_phi` is a table lookup |
| BUILD-41 | low | fixed | SPEC S-ADR-38, §3.8 `FlowCube` | Column cubes carry only the affected units |

## Fixes whose adequacy is confirmed at build time

Each is a design rule with a stated test and fallback; the design does not assume the outcome.

| Item | Test that decides | Fallback |
|---|---|---|
| Decision θ\* (QUANT-08) | G0 recalibration on the decision census, allocation v2 and pricing conventions (B13) | The prudence overlay stays printed as a sensitivity |
| 48 adaptive tangents (QUANT-18, BUILD-19) | `test_a8_decision` and the nightly power-cone reference | More tangents |
| Linear readiness reading (QUANT-12) | A20 nightly comparison (≤ 0.5 month, ≤ $0.1bn) | Full replica every quarter (B1 grows) |
| B2 re-solve budget (QUANT-22) | `test_b2_profile` (≤ 2 s per warm re-solve) | Finite-difference checks move to the nightly job |
| FBE gate outcomes (BUILD-36) | Re-derivation under the S-ADR-10/27 estimator before the first scored release | Mechanism tests only |
| Missing market series (BUILD-02) | WP-41, after user approval (question 3 below) | Labelled conditional fills remain |

## Cross-document notes (outside this revision's write scope)

- `design/addenda/CHAT_ANALYST.md` v1.0 has four conflicts with this revision, which SPEC S-ADR-34 and §4.35 resolve in favour of v1.1:
  - it repeats the v1.0 W1 gates (amber 1.20, red 2.30 nats; ESS ≥ 5,000), superseded by QUANT-32;
  - it uses single-tier Replay keys, superseded by S-ADR-41;
  - it numbers its proposed spec ADRs S-ADR-27–29, which collides with SPEC v1.1;
  - it proposes WP-39 to WP-49.

  The addendum's owner should align it with v1.1.
- `design/schematic/` (`architecture_model.json`, `TPA_Lab_Architecture.html`) was generated from earlier text and should be regenerated from v1.1.

## Questions only the user can answer

| # | Question | Working assumption until answered |
|---|---|---|
| 1 | **Tier-1 ratification (A1).** Should T4′ be calibrated class by class (θ\* ≈ 0.58 on the research fixture), or with M6 held at 1% as a Board-ratified prudence overlay (θ\* ≈ 0.76–0.79, with its $13.9–14.6bn facility ask)? Do you accept the Tier-1B bands, the economic-substance red event (δ_max, red-tier sales in event-Amber count as red) and the stress conventions: ≤ 50% revolver credit in s\* (vs 80%), an OV2-consistent opportunistic loss (vs 1.5% of NAV), a 2-quarter pacing-credit lag and stressed Real Assets income? | Class-banded θ\*, recalibrated at G0. Tier-1B bands +1/0/−2% (M1–M5, MIX) and —/−2.5/−5% (M6). δ_max = 10%, and event-Amber red-tier sales count as red. Pricing on the internally consistent conventions, with the research set shown as a sensitivity (ARCH Q3) |
| 2 | **Marks archive (brief §9).** From which quarter does the point-in-time archive start? Does it hold each holding's cash-flow history and the forecast's exit date or horizon? Which groups file IRR and which MOIC, and does any group state cases other than P10/P50/P90? | Quarterly from 2008; cash flows and exit timing available per holding; cases read as P10/P50/P90; the synthetic archive mirrors that shape (ARCH Q9) |
| 3 | **Public market data.** May a human with network access snapshot the missing monthly series into `data_public/` (WP-41), and from which licensed or public sources? | Increment 1 runs on the 23-column panel with labelled conditional fills; WP-41 lands in v1 (ARCH Q10) |
| 4 | **Analyst access (R16).** Which roles may use the analyst, and with what visibility of peer groups? How long are transcripts kept, and who may read them? May Claude Code or Desktop be used beyond synthetic data? May a chat what-if be cited in a DecisionRecord? | All IC members, the CIO, CRO, Treasurer, group heads and TPA analysts; group heads see peers in aggregate. Transcripts are kept for the decision-record retention period (7 years [I]) and read by the user, the CRO office and MRM. External MCP clients run on synthetic data only, at exploration grade. A chat what-if is cited only after confirmation on an ADIC surface and an exact recompute (ARCH Q11; CHAT_ANALYST Q1, Q5) |
| 5 | **Model weights and the target.** Which CMA model weights w_m should J, Ψ_τ, the mixture class (which enters the θ\* rule) and the bridge use? Is the 10% target gross or net of distributions, and over which horizon? | Equal weights (1/6) across M1–M6 until the A2 vote; nominal geometric 10-year TWR, gross of distributions (ARCH Q8) |
| 6 | **Increment-1 scope.** Is a 10-week MVP at ARCH §11.6 fidelity acceptable (8 factors, simplified private engines, allocation v2 only, computed seats in v1)? Or would you rather have the wider increment 1 that SPEC v1.0 described, on a longer schedule? | The 10-week MVP at ARCH §11.6 fidelity (S-ADR-37), with the analyst thin slice included |

*SYNTHETIC – NOT ADIC DATA.*
