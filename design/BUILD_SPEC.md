# ADIC Agentic Total-Portfolio Laboratory: Build Specification

**Version:** 1.1 · **Date:** 2026-10-18 · **Author:** Lead Engineer (design workflow, stage 3b), revised by the Chief Architect after the quant-consistency and buildability critiques · **Status:** binding on the build. It refines `design/ARCHITECTURE.md` v1.1 (ARCH) into names, signatures, shapes, units, work packages and tests. Where it changes ARCH, a spec-level ADR in §0.3 records why; ARCH v1.1 has adopted S-ADR-01 to S-ADR-44. Dispositions of all 75 critique items are in `design/reviews/revision_log.md`.

> **SYNTHETIC – NOT ADIC DATA.** Every balance, probability, price, horizon, timing and count in this document comes from the synthetic working book (context §1A, allocation v1 or v2, census v1.0, v1.1 or v1.1r), research prototypes or benchmark proxies. [I] marks a design default to be calibrated; [I-calc] a research computation; [M] a measured benchmark on a synthetic structure.

**Citation keys** (as ARCH, plus): ARCH = `design/ARCHITECTURE.md`; brief §7 / §8 = `design/00_DESIGN_BRIEF.md` §7 (literature refinements) and §8 (Real Assets); CTX §1A v2 = the context file's working allocation v2; GROUPS, G-gap_0k, gap_0k, SYN, LC, PA–PE, JQ/JE/JG as in ARCH's key table.

---

## 0. How to use this document; precedence; spec-level ADRs

### 0.1 For the coding agent of a work package

1. Read §1 (conventions) and §3 (contracts) in full; read your module's §4 entry and its row in the import table (§4.0).
2. Import only the modules your row allows. The layering test (`tests/layering/test_imports.py`) fails the build otherwise.
3. Build against the frozen contracts (`adic_tpa.contracts`) and the fixtures in `adic_tpa.testing`, not against other WPs' unfinished code. Contracts freeze at the end of Wave 0, and only after the **walking skeleton** (`tests/skeleton/test_walking_skeleton.py`, WP-03) has called every Protocol and every cross-WP function in §4 once, end to end, on `mini_book` with fakes; changing a frozen signature needs a contract-change note signed by the WP-01 owner and every consumer WP.
4. Your WP is done only when its Definition of Done (§9.2) and its §4 tests pass in CI, offline.

### 0.2 Precedence

- **Intent:** brief > ARCH > this spec. **Names, signatures, shapes, units and tests:** this spec > ARCH (refinements). A refinement may add fields, parameters with defaults, or modules; it may not change a meaning in ARCH without an S-ADR below. ARCH v1.1 adopts every S-ADR in §0.3, so a coding agent reading ARCH "for the reasons" meets no contradiction; ARCH §16 lists the v1.0 statements that were superseded.
- Research numbers quoted here are SYNTHETIC calibration targets, never acceptance values, unless a test names them explicitly (e.g., the ported regression suites).

### 0.3 Spec-level ADRs

ARCH v1.0 predated brief §7 (literature refinements, added 17:10), brief §8 (Real Assets, added 17:40), brief §9 (the three return series, about 18:40) and R16 (chat). The brief requires the build to adopt or reject each item by ADR. S-ADR-01 to S-ADR-26 did that for §7–§8; S-ADR-27 to S-ADR-44 (v1.1) adopt §9 and R16 and close the critique items, amending earlier S-ADRs where the critiques found them wrong (each amended row says so). Format: decision; consequence; evidence.

| ID | Decision | Consequence | Evidence |
|---|---|---|---|
| **S-ADR-01** Taxonomy is configuration | `GroupId` is a validated string, never a closed enum. `config/taxonomy/groups_v2.yaml` (default) lists eight investment groups `PE, SECONDARIES, CAPSOL, COINVEST, PUBLIC, PRIVCREDIT, OVERLAY, REALASSETS`, plus non-investment owners `CF` and `TPA`. `groups_v1.yaml` (seven groups) reproduces research fixtures. Engine code reads group *capabilities* (`GroupSpec` flags), never group names | Seats = n_groups + 5; group Shapley players = n_groups + 2; H's private blocks loop over `private` groups; `test_no_hardcoded_group_ids` scans `src/` | brief §8 rule 1; CTX §1A |
| **S-ADR-02** Real Assets interim engine and lenses | `priv.realassets`: closed-end funds reuse the fund engine with RA templates (earlier income); core, open-end and direct assets use NOI/cap-rate value with Geltner-smoothed appraisal NAV, capex and development calls, non-recourse asset debt (LTV, DSCR, maturity wall, refinancing, rate hedge) and an open-end redemption queue (`pub.queue`). Forced RA asset or LP-interest sales are red tier; open-end redemptions amber; cash-out refinancing of asset debt is a reversible R0x lever outside CF facilities that counts in look-through leverage | Parameters are config (`config/groups/realassets.yaml`), so the RA integration memo replaces them without interface change | brief §8 rules 2–5, 7 |
| **S-ADR-03** Allocation v2 default; census rule | Book configs: allocation `v1` (PE $52bn, seven groups) and `v2` (PE $34bn, RA $18bn, eight groups; default). Census ids: `v1.0` (PE unfunded $27.4bn), `v1.1` ($16.4bn, the user's choice) and `v1.1r` (the sealed v1.1 vintage history rescaled to the allocation's PE bucket: $10.7bn under v2 by exact rescaling — the brief's "about $10.9bn" uses the rounded U/NAV of 0.32 — and identical to v1.1 under v1). **Decision census:** `v1.1` if a V6-compliant history fits the active allocation's PE bucket and V1–V2 pass at build (V6 is the decisive gate, G-gap_02 §1; v1.1 amendment by S-ADR-37, because "passes V1–V24" was undefined while V15 and V18 are n/a); otherwise `v1.1r`, with the substitution recorded in the manifest and printed on L0 (never silent). Every liquidity metric is shown for the decision census and the side-by-side census (`v1.1` vs `v1.1r` under v2; `v1.1` vs `v1.0` under v1). Research regression fixtures run on allocation v1 + census v1.0 | ARCH ADR-25 extended; Q2 closed by brief §8 (the user chose v1.1) | brief §8 "PE unfunded"; CTX §1A v2; G-gap_02 §1 |
| **S-ADR-04** One money unit | USD bn at every interface and in every file (Parquet, JSON, YAML). ARCH §9.4's "US$m internally" is superseded for files; the LP scales by W₀ internally only | No unit conversions between modules | ARCH §0.5 |
| **S-ADR-05** Red event generalized (**amended by S-ADR-30**) | Red-tier membership comes from the taxonomy (`red_tier: true`: PE, SECONDARIES, COINVEST, REALASSETS by default), so T6 is computable for any taxonomy. v1.0's rule "a sale tagged `SaleReason.RECOURSE_RED`; discretionary SELLs are never red" is withdrawn: whether a red-tier sale is a red event is decided by economic substance (S-ADR-30), whatever its label or code path | T6 is computable for any taxonomy and cannot be gamed by relabelling | ARCH §5.2 T6, ADR-39; brief §8; QUANT-03 |
| **S-ADR-06** Objective refinements | Shortfall exponent **strictly > 1** in Θ and in every fitness (linter rejects p ≤ 1). J is pre-committed: `ObjectiveSpec.target_mode = "precommitted"` anchors the target path at the A1 contract date and quarterly re-solves use the induced target on that path, never re-anchoring (Forsyth 2020). Tier-1B re-imposition (Cuoco–He–Isaenko 2008) is **amended by S-ADR-31**: v1.0 certified 5-year windows starting at years 0–5, which silently shortened the 10-year floor; v1.1 re-certifies the forward 10-year floor at every quarterly re-solve and bands it by model class | ARCH §5.2 "≥ 1" tightened | brief §7 item 4; QUANT-01 |
| **S-ADR-07** T6 surrogates, bPOE, reaching for yield | `T6SurrogateKind ∈ {CVAR_CLASS (default), WORST_CASE_CVAR, ALSO_X}`; the nightly experiment compares certified P(red) and cost. Buffered probability of exceedance is reported beside every P(red) and on the red margin. A reaching-for-yield (RFY) signature joins the gambling detector as a *flag* | No change to the default H rows | brief §7 item 4 |
| **S-ADR-08** Robustness | DRO and robust satisficing shown as one frontier; ambiguity on regime persistence by exact path likelihood ratios under alternative transition matrices (`robust.persistence`); ambiguity sets never stacked (ensemble range and KL tilt reported separately); regime-conditional radii η_s | New figure and metrics | brief §7 item 5 |
| **S-ADR-09** Optimization core | Tree reducers behind one interface: `kmeans_observable` (default, ARCH §5.4) and `forward_filtration` (Heitsch–Römisch forward selection), A/B by error-ledger row A4. An information-relaxation dual bound (Brown–Smith) on the standing policy runs nightly on 500 paths and its gap prints in every release. Belief-state SDDP stays deferred (ADR-36); terminal-value regressions include the regime posterior as a feature. The DSL gains a lifted piecewise-linear transform `hinge(k)` | New module `core.irb`; DSL grammar extended | brief §7 item 6 |
| **S-ADR-10** Forward Belief Engine (**amended by S-ADR-27**) | Mean fusion weights are equal (or screened) by default; covariances Ω̃ enter the predictive variance only; constrained GLS weights are a variant retained only if they beat equal-weight and screened averages out of sample on the point-in-time archive (decided on real data; synthetic data tests correctness only, never selects variants); every linear pool is recalibrated by a beta-transformed linear pool; κ_g is estimated on the full archive (optional time decay) and forecast precision is capped beyond 8 quarters ahead (× min(1, 8/h)); no "best forecaster" recognition outside the incentive-compatible WIS points in pay. v1.0's "w = (1 − s)·w_GLS + s·w_eq" default put Ω̃ back into the weights, and its "last 8 resolved quarters" read the literature's horizon cap as an estimation window | ARCH §4.7 refined | brief §7 items 7, 13; literature §4.10; QUANT-13, QUANT-24 |
| **S-ADR-11** Group priors | Hedge-fund α prior mean 0 with α = 0 a mandatory sensitivity and a put-writing baseline in hedge-fund attribution; long-only sleeve-specific IR priors; Private Credit fund-age prior with a downside-beta charge, LGD by collateral type, evergreen units at 0 Tier-1 liquidity; PE weights GP access over selection skill and applies a fund-size penalty to up-sizes; Secondaries CV elections are exogenous events | Config changes in `config/groups/*.yaml` and `config/beliefs/priors.yaml` | brief §7 item 8 |
| **S-ADR-12** Facilities and financing window (**convention roles reversed by S-ADR-32**) | Revolver availability multiplier ≤ 0.5 in the joint oil–crisis state (S = CRIS ∧ Z ∈ {DB, SG, GW}) in P and H; unsigned facilities count zero. Because s\* represents that joint state, the synthetic lab now prices T4′ with the ≤ 50% credit and prints the research's 80% as the "as ratified" sensitivity row until A1 decides (v1.0 had the roles the other way round, so the hard row contradicted H2h in the same LP). A financing-window state f ∈ {OPEN, TIGHT, CLOSED}, derived from E's credit and EBP factors, drives availability and spreads; a 110bp [I] tightening premium enters REFINANCE and LEVER hurdles in TIGHT and CLOSED. Pre-funded term cash is a CF lever column and a capability counterfactual. Effective debt maturity and rollover risk sit on the Treasurer panel | New enum `FinWindow`; new lever `cf_term_prefund` | brief §7 item 2 |
| **S-ADR-13** Recourse waterfall (**amended by S-ADR-30**) | P0's recourse order is a tuned, state-dependent `RecourseOrder` (a permutation of reserve, P2S, liquid, facility, amber and red rungs, chosen from a declared set, switched on planning stage and drought posterior), with a crowding haircut on sale prices that rises with a market-wide forced-selling index; the index is an exogenous cube variable built from `sec_discount` and `hy_spread`, never a cross-path statistic (which would depend on block size). LIQUID_FIRST, CASH_LAST and PRO_RATA run as standing ablation controls. A drought early-raise slot `preemptive_raise` (planned tail-end and LP-interest sales within depth caps, term funding) executes at quarter start **outside** `recourse_cover`; its red-tier sales are red events whenever the economic-substance test holds (S-ADR-30) | P0 parameters +2; controls +2 | brief §7 item 1; QUANT-03; BUILD-40 |
| **S-ADR-14** Owner band, Mode H only | The band is priced at the owner's cost (peaking in demand busts); owner acceptance in DB states is stochastic, p_acc = 0.3 [I]; owner-directed domestic investments are an obligation stream inside the band; band policies need a written owner `SignOff`; Mix A (no band) is the default | Only in OWNER_PROPOSAL runs | brief §7 item 3; ARCH ADR-09 |
| **S-ADR-15** Overlay | Any convex-sleeve increase must beat an equal-cost CF cash buffer (Gamba–Triantis test in `attrib.counterfactual`); P0's convex trigger keys on a left-tail-premium percentile `ltp_pctile` instead of low VRP (`vrp_pctile` stays a feature); the trend template's crisis beta decays after crises; VM receipts arrive with a delay (1 business day normal, 3 in stress [I]) that the monthly ledger and T3 see; DSR severity by provenance (live ≥ 0.95; backtest-only ≥ 0.99) | DSL variable added | brief §7 item 9 |
| **S-ADR-16** Internal capital market | λ is published decomposed by binding row; risk charges come from H's CVaR-row duals (owner-loss-consistent), never Euler CVaR splits; prices are conditioned on the financing window; the Γ gap is reported against the group count; summed group risk budgets carry a diversification haircut h_div = 10% [I]; envelope changes are collared at ±25% a quarter outside ranging validity; no single hurdle | `icm` additions | brief §7 item 10 |
| **S-ADR-17** IC refinements | Adopted as already in ARCH §8 (commitment plans, authentic dissent first, objective devil's advocacy aimed at the model recommendation, decision accuracy and under-reliance KPIs) | None | brief §7 item 11 |
| **S-ADR-18** Lab | Canary tokens are planted in final-plane manifests and in the sealed truth store; a canary in any agent-visible channel is a SEAL_BREACH → ABORTED. An mFDR ledger runs across contracts in the registry (Holm within a contract, mFDR across); judge admission tests; re-qualification after any model upgrade | `seal.canary`, `registry.mfdr` | brief §7 item 12 |
| **S-ADR-19** Synthetic data | Generator variants pre-registered (misspecification ensemble hashed); semi-synthetic release R3 (ADIC observation structure, synthetic truth) planned for when data arrive; SYN-ADIC-177 tests correctness and robustness, never selects estimator variants | `synth.releases` reserves R3 | brief §7 item 13 |
| **S-ADR-20** Pacing | A commitment cut earns no liquidity credit for 2 quarters (calls unchanged until t + 2) in H, P and T4′; the corridor's option value is reported (attrib); commitment-inclusive leverage (recourse debt + unfunded) ÷ NAV joins the T5 metrics | `CanonicalConventions.pacing_credit_lag_q = 2` is a Tier-1 convention change proposed at A1 (JG-MF13). v1.1 (S-ADR-32): because P and H already use lag 2, the synthetic lab prices T4′ with lag 2 as well and prints lag 0 as the sensitivity; only the ported research fixtures run with lag 0; `ledger.leverage` metric | brief §7 item 14; QUANT-14 |
| **S-ADR-21** Provisional research numbers | Co-investment wipe-out and LTV-breach statistics (G4, barrier-sign error) are provisional: no test uses them as acceptance values; tests check mechanisms (monotonicity, inadmissibility flags) | — | brief §7 item 15 |
| **S-ADR-22** Thirteen shadow-IC seats under v2 | Seats are generated from the taxonomy: CIO, CRO, Treasurer, one seat per investment group (8), Outside-View Forecaster, Red Team; the Overlay seat keeps its two briefs | ARCH "twelve" becomes n_groups + 5 | S-ADR-01; brief §8 rule 1 |
| **S-ADR-23** Anthropic call surface | First-party calls use `client.beta.messages.parse(..., output_format=Model, betas=["server-side-fallback-2026-07-01"], fallbacks="default")`; Batches requests omit `fallbacks` (rejected there) and handle refusals by synchronous re-route; Bedrock, Vertex and Foundry use `BetaRefusalFallbackMiddleware` | ARCH §11.2 refined | bundled claude-api skill (Python README, refusal section) |
| **S-ADR-24** Composition root | A new top-level package `pipeline` wires `lab` and `idm` through `contracts.ports.RoomPort`, so imports stay downward | ARCH §3.2 does not name it | ARCH §3.2 rule "dependencies point downward" |
| **S-ADR-25** Seeds (**key layout amended by S-ADR-38**) | numpy `SeedSequence` spawn tree at the (plane, world) level; below it SHA-256-keyed Philox4x64-10 per (source, entity) with counter (path, month, ⌊slot/4⌋, 0) and output lane slot mod 4, so all four Philox lanes are used (v1.0 keyed per slot, which forced one lane per stream and capped generation at ≈31.5M uniforms/s) | Reconciles brief P11 with ARCH §3.5 | ARCH ADR-15; BUILD-05 |
| **S-ADR-26** Calendar | As-of instant q = 0 is 2026-09-30 (census date); fiscal year = calendar year; owner instalments at calendar quarter ends | Fixes ARCH's open calendar | G-gap_02 §1 (census date) |
| **S-ADR-27** Brief §9 adopted; literature item 7 corrected | ADIC's quarterly point-in-time archive exists; FBE-R, κ_g and registry scoring are estimated from it from the first release. The `marks_archive` adapter's schema and contract test are frozen in WP-05 (wave 1). `ForecastRecord.target` gains `irr_si` and `moic_si`, plus `case_map` (down/base/up → p10/p50/p90 by default, per-group overrides) and `exit_horizon_q`. `beliefs.signal_returns` receives the unit's cash-flow table and implements the translation of §4.15 (remaining value from the stated MOIC or IRR on the fund engine's mean-path profile; cash-weighted remaining life; nowcast). Strategic covariates are 0 with a `history_indicator` before go-live. O2/O4 emit since-inception net IRR/MOIC with cases and a 2008-to-as-of archive in R0. Amends S-ADR-10 (equal/screened weights by default; κ_g on the full archive with a horizon cap) | Real-data calibration from day one; the synthetic tests exercise the translation | brief §9, §7 item 7; ARCH ADR-43; QUANT-11, -13, -24; BUILD-09 |
| **S-ADR-28** Belief draws | `BeliefSet.mu_hat` is replaced by `alpha_a` (forward log excess return over the unit's benchmark at the as-of), `benchmark_id`, `beta_hat` and `bench_ref_a`, with `mu_total_a = bench_ref_a + alpha_a` for display. New `contracts.beliefs.BeliefDraws`; `beliefs.draw_paths(bs, base, paths, graph, tax, world) -> BeliefDraws` per world and block; `AssetEngine.init(book, beliefs, n_paths, *, draws, world)`. Engines add only α to the world's beta return | No double-counted beta; worlds move returns | ARCH ADR-40; SYN §4.2; QUANT-02; BUILD-04 |
| **S-ADR-29** Interface amendments before the freeze | ARCH §3.5 amended (adopted in ARCH v1.1): `AssetEngine.init(..., *, draws, world)`, `AssetEngine.recourse_quotes`, `AssetEngine.apply_recourse`, `Ledger.apply(..., quotes) -> (LedgerState, RecourseOutcome)`, `phase2(lp, p1, glide, tree)`, `price(sol, lp, tree, tax)`, `select(lp, sol, cols, *, basis)`, `project(prop, state, *, ls0, rows, exact_check)`, and the `EngineFactory` Protocol. `SimContext`, `PolicyContext`, `EngineContext`, `RecourseAvailability`, `RecourseOutcome`, `T6Screen`, `LinearizedTier1`, `ExactCheck`, `FBEValidationSet` and `GroupRatesMeta` move into `contracts` with fields (§3.18); `OptimizeHOut` is replaced by `HSummary`; `core.h.t6_screen` produces `T6Screen` | No consumer invents a shape after the freeze | ARCH ADR-41; BUILD-01, -11, -12, -16 |
| **S-ADR-30** Red event by economic substance (amends S-ADR-05, -13) | `ledger.red_test` marks a red-tier sale red if (i) `recourse_cover` executed it, whatever the rung; (ii) event stage ≥ AMBER or unencumbered IG + cash < `ig_target`·W at execution; or (iii) its cash-equivalent bid < (1 − `Tier1Spec.red_discount_max`) × the unit's normal-regime hedonic bid (`red_discount_max = 0.10` [I], A1 field). `SaleReason` labels are reporting-only; PLANNED requires event GREEN, IG + cash ≥ target and no (iii). `RecourseOrder` has no "preemptive" rung. In H, root red-tier SELL columns are T6-consuming when the frozen state meets (ii) or the bid meets (iii): column bound 0 in Phase II, priced by forced re-solve | Relabelling cannot move P(red); Gate 2 flags the relabelling signature | ARCH ADR-39; QUANT-03 |
| **S-ADR-31** Tier-1B floor (amends S-ADR-06) | `FloorSpec`: 10-year forward windows re-certified at every quarterly re-solve on [t, t + 40]; CVaR₁₀% bands by class (M1–M5 and MIX: +1% / 0% / −2%; M6 class: — / −2.5% / −5%; misspecification report-only; [I]); mixture median ≥ 7% (capacity 6% [I]); only capacity breaches enter Phase I-b | The floor keeps its meaning without a structural veto | ARCH ADR-37; SYN §4.9; QUANT-01 |
| **S-ADR-32** θ\*, T4′ appetite and canonical conventions (amends S-ADR-12, -20) | `Tier1Spec.theta_rule = "class_banded"`: G\* = max over T6 classes of the class quantile at its own tolerance share (0.40% for M1–M5 and MIX, 1.01% for M6); on the research fixture this gives θ\* ≈ 0.58, set by the M6 class (M6's P99 gap $7.37bn; the mixture alone gives 0.42, the worst of M1–M5 0.35) against 0.76 for the legacy rule [I-calc: `research/addenda/gap_02_calcs/gap02_results.json` `calibration.targets` and `theta_for`; allocation v1, census v1.0, research conventions; SYNTHETIC]; `theta_star` has no code default and is set at G0 (B13) on the decision census, allocation and pricing conventions; the legacy worst-model value is the `prudence_overlay` sensitivity. APPETITE rows use T4′ survival ≥ 24 months on TP with no facility credit. Canonical defaults: revolver credit 0.5 in s\*, opportunistic loss `ov2_consistent`, pacing lag 2, Real Assets stressed income; `conventions_research` printed as a sensitivity. `StressSpec.dist_mult` applies to groups flagged `fund_distribution_stress`, not to `red_tier` groups | T4′ and T6 agree class by class; one internally consistent pricing set | ARCH ADR-38; gap_02 §1.2; G-gap_04 §5; G-gap_03 §5; QUANT-08, -09, -14 |
| **S-ADR-33** H accounting | §5 rewritten per ARCH ADR-42: buyer-assumed unfunded κ^U and a fixed age split ω of group sales (`sale_age_allocation ∈ {pro_rata_ref, mature_first}`); RA at gross value with D^RA and its transition; W_n definition row; TERMINAL with IM, residual overlay MTM, D^RA and accumulated charges K; H3 capacities linear in the state; every cost once in cash (segments at pricing nodes; K for κ^GP); no money term in the objective; simple returns; compounded fan coefficients; lags mapped by period length; H5 at (1 + r_{f,q})^12; kernel over strict ancestors; column coefficients keyed by `RowKey`; per-unit `UnitFinancing` | Prices and feasibility verdicts free of the v1.0 accounting errors | ARCH ADR-42; QUANT-04 to -07, -15, -26, -34; BUILD-22 to -24 |
| **S-ADR-34** Conversational analyst | New package `analyst` and `contracts/analyst.py`, specified in full by `design/addenda/CHAT_ANALYST.md` v1.0, which is binding for R16 and refines this spec's analyst names, schemas, 30-tool catalogue, surfaces, confirmation protocol, access matrix, logging and evaluation (§4.35). The addendum's proposed "S-ADR-27/28/29" (analyst package; grounding forms; process topology) are adopted here as S-ADR-34(a)–(c), renumbered because S-ADR-27–29 were already assigned. Work packages: the addendum's WP-CHAT-01 is delivered by WP-01 (contracts, wave 0); WP-CHAT-02–04, 06, 07, 09, the W1/W2 part of WP-CHAT-05 and the Stub/Replay part of WP-CHAT-10 form **WP-39** (increment 1, waves 4–5); the W3 part of 05, 08, the live part of 10 and 11 form **WP-40** (v1, waves 6–7). Two v1.1 rules override values the addendum repeats from v1.0: the unified W1 KL and ESS gates (§8.4; QUANT-32) and two-tier Replay keys (S-ADR-41). Surfaces: `tpa chat`, the read-only analyst MCP server, and the pack's Ask panel (hand-off to `tpa chat` in increment 1; the loopback `tpa ask serve` in v1). Acceptance: the 140-question golden set, ≥ 300 items in v1 | R16 is built, not deferred | brief R16; ARCH §8.12, ADR-44; CHAT_ANALYST §14; BUILD-08 |
| **S-ADR-35** Market data, factor set, B1/B2 | v1 factor set of 20 (§4.10), including `log_rv` and `short_rate`; implied vols only in `ScenarioCube.vol`; each factor's kind (`logret`, `level`, `change`) declared in `scen/factors.yaml` and `CubeMeta`; spreads stored as levels and their t₀ levels in `StateSnapshot`; ε = √((ν − 2)/ν)·t_ν; P^Z_m the principal 12th root; anchor on E[Σ log(1 + r)]. Increment 1: an 8-factor subset. B1/B2 resample the gap_04 panel's columns and fill the rest from E's conditional model, labelled PROXY. WP-41 (wave 6, a human with network access) snapshots the missing public series. `calibrate_world` fits only factors with history and otherwise verifies [I] configuration. `PlaneSpec.b2_mode ∈ {family_holdout, out_of_time}` | B1/B2 buildable now; F_t computable on simulated paths | ARCH ADR-45; BUILD-02, -14, -37; QUANT-19, -21, -29 |
| **S-ADR-36** LLM draft models and numeric fields | Role outputs are draft models (§3.16): `SeatArgumentDraft`, `MemoDraft`, `AnswerDraft`, `ViewSpecDraft`, `ScenarioSpecDraft`, `AuditDraft`; deterministic code assembles `SeatAssessment`, `RenderedDocument`, `AnswerCard`, `ViewSpec`, `ScenarioSpec` and `AuditReport`. LLM-facing schemas use `KeyValue` lists and named sub-models, never dicts or fixed tuples (`tests/agents/test_llm_schemas_transform.py` runs the SDK's strict-schema transform on each). `SeatAssessment.agent_judgment_probs` is removed; `IdeaBundle.predicted_effect` and `ExtractionRecord.confidence` are diagnostics never rendered or aggregated; extracted numbers reach engines only after 100% human verification or dual-extraction agreement plus a sampled check under an error-rate gate | P1 holds in the schemas themselves | ARCH ADR-46; QUANT-10; BUILD-10 |
| **S-ADR-37** Increment-1 fidelity, blocking gates, DEV/SYNTHETIC mode | Increment 1 restores ARCH §11.6: 8 factors, simplified private engines, allocation v2 with censuses v1.1/v1.1r (allocation v1 + v1.0 only as research fixtures), computed seats in v1. Blocking V-gates in increment 1: V1–V2, V5–V9, V12, V20, V22–V24; n/a gates are non-blocking; V16–V18 are release-validation jobs whose hashed reports the pipeline reads. `AnalysisContract.run_mode ∈ {DEV_SYNTHETIC, REAL}`: DEV allows a single-account software seal (salt under `runs/<run_id>/seal/`, commit–reveal checked in code), the test signer key and the `testing.synthetic_committee` fixture (seeded pre-votes and ballots labelled SYNTHETIC); REAL refuses all three; L0 prints the mode; ACL drills are marked `requires_accounts` | The 10-week MVP is reachable and the demo reaches CLOSED unattended | ARCH ADR-47; BUILD-17, -18 |
| **S-ADR-38** Performance re-baseline, RNG lanes, samplers | B1 is the sum of nine tested component lines (§10.1, ≈ 36 s); RNG keys per (source, entity), counters (path, month, ⌊slot/4⌋, 0), lane = slot mod 4, keys cached per block; t_ν and gamma by tabulated inverse CDFs in numba (abs error < 1e-7) instead of `stdtrit`/`gammaincinv`; the readiness reading in P from linear response vectors with the full replica on band exits (A20); dual quality from ranging with ≤ 10 finite-difference rows on the quarterly path; per-step B2 and per-stage B12 budgets; a per-kind evaluation table for the lab; group Shapley weekly with P = 32 permutations; column `FlowCube`s carry only the affected units | Budgets add up and are tested | ARCH ADR-48; QUANT-12, -22, -33; BUILD-05, -06, -07, -30, -31, -41 |
| **S-ADR-39** External data in Pydantic JSON mode | Models keep `strict=True`, so every external payload is validated in JSON mode: `load_yaml` = `model.model_validate_json(json.dumps(yaml.safe_load(f), default=iso))`; MCP payloads and registry rows use `model_validate_json`; no model is used as a set member or dict key (caches key on `content_hash`) | Config and tool I/O load on day 1 | BUILD-03 (pydantic 2.14.1 checked) |
| **S-ADR-40** Signatures | `SignOff.signature` is an Ed25519 signature (`cryptography` 50.0.2, added to the allowlist with this justification) over canonical JSON {object_hash, role, signer_hash, signed_at}; private keys per person, protected by DPAPI (`win32crypt`); public keys in `config/room/signers_roster.yaml`, signed by the CRO office and MRM; `contracts.signing.verify`; DEV mode uses a fixed test key labelled SYNTHETIC | Third-party-verifiable sign-offs | BUILD-29 |
| **S-ADR-41** Replay keys; fixed tool lists | Two-tier Replay keys: a structural key (role, state, prompt hash, tool-schema hash, turn index) selects the cassette; the full request digest is then compared and a mismatch raises `REPLAY_DRIFT` (Stub fallback in non-gating tests; integrity drills gate on exact Replay); re-recording is scheduled. Each role's tool list is fixed for the life of a transcript; a state change starts a new transcript; the firewall enforces allowlists by returning `is_error` tool results | The agent suite stays green across engine changes; prompt caching survives | BUILD-33, -39 |
| **S-ADR-42** Build hygiene | Worker functions are top-level and picklable with explicit arguments (contract hash, seeds); `@njit(cache=True)` with `NUMBA_CACHE_DIR` per plane, warmed at evaluator start outside the hash checks; cubes regenerated inside workers; process start-up counted in B2/B5. Text files are hashed with LF-normalized line endings and `.gitattributes` sets `* text eol=lf`. One metric file per WP (`config/metrics/wp-NN.yaml`, merged with a duplicate-id check); engines registered in `config/engines.yaml`, not in a package `__init__`; one evaluator server factory in `evaluator/server.py`, `mcp_server.py` only dispatches; every cross-module test has a named owner WP (§10.6) | No parallel-agent collisions; bit-for-bit hashes across machines | BUILD-26, -28, -35 |
| **S-ADR-43** Misspecification ensemble as typed overrides | `MisspecOverride{target_module, param_path, op ∈ {set, mult}, value}`; `WorldSpec.overrides`; `EngineFactory.build(book, world)` applies them; book variants become `PlaneSpec.book_variants`; effective configs hashed into the manifest | The final plane can run the ensemble behind the 7% floor claim | ARCH §7.5; BUILD-16 |
| **S-ADR-44** Outer calibration loop | `core.mpc.calibrate_buffers` tunes `b_red`, `b_floor` and `lambda_T_H`: bisection on a buffer multiplier per class, ≤ 4 warm-started iterations, stop when every class's CP bound ≤ tolerance and Kendall τ ≥ 0.8; defaults from last quarter, zero buffers in the first quarter; at the cap, Phase I-b decides structural recovery on the CVaR rows, otherwise cards carry `calibration_capped` | The CFA class has an owner, a stop rule and a budget (B17) | ARCH §5.3; BUILD-13 |

---

## 1. Global conventions

### 1.1 Package, interpreter and installation

| Item | Rule |
|---|---|
| Package | `src/adic_tpa/` (src layout), import name `adic_tpa`, CLI `tpa` (typer app `adic_tpa.cli:app`; also `python -m adic_tpa`) |
| Interpreter | `C:\users\dean\ai_envs\adic_tpa_lab\.venv\Scripts\python.exe` (CPython 3.12.15). Bare `python` is never used in scripts or docs |
| Installation | Offline "dev install": `tools/dev_install.py` writes `adic_tpa_dev.pth` (one line: the absolute path of `src`) into the venv's `Lib\site-packages`. This works with `python -I` (isolated mode still processes site-packages `.pth` files), which the evaluator and seal processes require. `pyproject.toml` declares hatchling for later packaging but nothing in development needs a build backend |
| Pinned stack | numpy 2.5, scipy 1.18, pandas 3.0, pyarrow 26, cvxpy 1.9.3, highspy 1.15.1, clarabel 0.11.1, osqp 1.1.3, scs 3.3.1, statsmodels 0.15, scikit-learn 1.9.1, hmmlearn 0.3.3, arch 8.0, numba 0.68, pydantic 2.14, typer, rich, jinja2, plotly, matplotlib, pytest, hypothesis, anthropic 1.15, mcp 2.3, opentelemetry-api, pyyaml, jsonschema, pywin32 (JE §1), and `cryptography` 50.0.2 (installed; justified by S-ADR-40 for verifiable signatures). The import-allowlist test (`tests/layering/test_allowlist.py`) fails on any other third-party import. No PyPI addition without a written justification and an ADR (ARCH §11.8) |
| Shell | PowerShell 5.1: no `&&`; absolute paths only; the cwd resets between calls |
| Style | `from __future__ import annotations` in every module; full type hints on public functions; NumPy-style docstrings with a `Units:` line for every money or rate argument; no module-level mutable state; no `eval`/`exec`; no network imports in any engine module (L0–L7); at L8 only the evaluator's MCP stdio layer imports `mcp` |

### 1.2 Units

| Quantity | Unit at interfaces | Storage dtype | Notes |
|---|---|---|---|
| Money (NAV, cash, flows, notional, debt, IM, VM) | **USD bn** | float64 in ledger, LP inputs, beliefs, cards; float32 in path cubes | Suffix `_bn` on scalar fields; cubes declare units in their spec |
| Money inside an LP | W₀ units (opening NAV, $177bn = 1.0) | float64 | `LPModel.scale_bn` stores W₀; only `core.h`/`core.solver` see W₀ units |
| Rates and returns | **decimal per period** of the producing clock (monthly engines: per month; quarterly engines and the LP: per quarter) | float64 / float32 | Annual values only in config and display, suffix `_a` (e.g., `sofr_a = 0.0389`). Conversions in `contracts.units`: `q_rate(r_a) = (1+r_a)**0.25 - 1`; `m_rate(r_a) = (1+r_a)**(1/12) - 1`; intensities `q_intensity(x_a) = 1-(1-x_a)**0.25` (SYN §0) |
| Factors in `ScenarioCube` | per the factor's declared kind (S-ADR-35): `logret` = monthly log return (equities, USD, Brent, inflation); `level` = end-of-month level in decimal (rates, spreads, log realized vol, exit factor, secondary discount, cap rates); `change` only where declared | float32 | Kinds live in `scen/factors.yaml` and `CubeMeta.factor_kinds`; spreads are always levels, and `StateSnapshot.factor_levels0` holds their t₀ levels; implied-vol indices live only in `ScenarioCube.vol` |
| Spreads | decimal (0.0085 = 85bp) | float64 | Display in bp via `contracts.units.to_bp` |
| Probabilities | decimal in [0, 1] | float64 | Display rules in §8.3 |
| CE metrics | **bp a year** of certainty-equivalent return (`stats.ce`) | float64 | Display adds "≈ $X m a year" with 1bp a year ≈ $17.7m a year at W₀ = $177bn (ARCH §5.2) |
| Time | quarter index `t`, month index `m` (§1.3) | int16/int32 | Years only in reporting windows |
| Return tags | `ReturnBasis` (kind arith / geom / log; fees gross / net) on every return field | — | ARCH §0.5 |

### 1.3 Time index and calendar

- **Instants and periods.** A *stock* array (NAV, cash, state) has length T + 1, index i = the instant at the end of period i (i = 0 is the as-of instant). A *flow* array (returns, cash flows) has length T, index i = the period from instant i to instant i + 1. Quarters: T_q = 40; months: T_m = 120. Month period m lies in quarter period ⌊m/3⌋.
- **As-of.** `Calendar.asof_instant = 2026-09-30` (S-ADR-26). Quarter period 0 = Q4-2026; month period 0 = October 2026. The R0 snapshot is dated 2026-10-18 and its market data run to the last close; the simulation clock starts at the census instant.
- **Fiscal year** = calendar year. `Calendar.fiscal_year(t)` returns 2026 for t = 0, 2027 for t = 1…4, and so on. FY2026 has one instalment left in the horizon. Draw-rate arrays have Y = 11 columns (FY2026–FY2036).
- **Owner instalments** fall at the end of each calendar quarter (month index 3t + 2). D_y = d_y·B_y, with B_y the reported NAV at the opening instant of FY y, reset annually (canonical; ARCH §4.3).
- **Decision timing inside a quarter:** (1) the policy acts at instant t; (2) every engine publishes `RecourseAvailability` for its recourse-eligible units (`recourse_quotes`, S-ADR-29); (3) quarterly engines step over period t, monthly engines step over months 3t…3t+2; (4) the ledger applies monthly flows, including the owner instalment in month 3t + 2, and runs the recourse waterfall in any month in which unencumbered HQLA falls below the hard floor, returning a `RecourseOutcome`; (5) engines apply the outcome (`apply_recourse`) before period t + 1.

### 1.4 Cash-flow sign convention

From ADIC's point of view: **inflow to ADIC positive, outflow negative**, in every `FlowSlice`, `FlowCube`, ledger identity and column vector. Calls, fees, premiums, VM paid, ΔIM posted, owner instalments, debt service and capex are negative; distributions, coupons, sale proceeds, redemption payouts, VM received, monetization and debt draws are positive. Stocks are non-negative magnitudes: NAV, unfunded commitment, debt balance, posted IM, encumbrance. `FlowType` declares an expected sign and `FlowSlice.validate()` rejects violations beyond 1e-12. The ledger identity is therefore L_{m+1} = L_m + Σ flows (ARCH §4.9 with signed flows).

### 1.5 Arrays

| Rule | Value |
|---|---|
| Axis order | **[path, time, entity, type]** — paths first, then time (month or quarter), then entity (unit, group, factor, row, CSA), then type (flow type, state component) |
| dtypes | float32 path cubes; float64 ledger states, LP data, beliefs and every reported statistic; int8 discrete states (regimes, lot states, stages); int16 time indices; int32 entity indices; uint64 RNG keys; bool masks |
| Layout | C-contiguous; containers own their arrays; `validate()` checks shape, dtype, finiteness and declared invariants |
| Blocking | Path simulations run in blocks of 2,000 paths; no array holds more than one block × full horizon of unit-level data |
| Missing values | NaN is illegal in engine arrays (failed paths are flagged and scored worst-case, never NaN-dropped; brief P5) |

### 1.6 Currency

USD only. Non-USD exposures exist only through overlay templates and, for real data, through adapters that convert at a recorded rate (`fx_rate`, `fx_source`, `fx_asof` columns). The synthetic book is USD throughout.

### 1.7 Seeds and random numbers (S-ADR-25; ARCH §3.5)

```
root_seed            : int (128-bit), a contract field
base(plane, world)   : SeedSequence(entropy=root_seed,
                         spawn_key=(PLANE_CODE[plane], WORLD_CODE[world])).generate_state(4, uint32) -> 16 bytes
base(final, world)   : HMAC-SHA256(salt, world_id.encode())[:16]       # salt held by the seal service
stream key           : SHA-256(base ‖ source ‖ u64 entity_key)[:16] -> Philox key (2 × u64)    # cached per block (S-ADR-38)
counter              : (u64 path, u64 month, u64 ⌊slot/4⌋, 0)
lane                 : slot mod 4                                     # all four Philox outputs used
entity_key(id)       : first 8 bytes of SHA-256(id) as u64; 0 when no entity
uniform              : (x >> 11) · 2^-53 from the 64-bit Philox4x64-10 output in the slot's lane
```

- PLANE_CODE = {calibration 0, search 1, final 2, historical 3, exploration 4}. WORLD_CODE = {M1–M6: 1–6, B1: 11, B2: 12, misspecification worlds: 100 + index in the contract's list}.
- Every variate uses inverse-CDF sampling from exactly one uniform per draw, so slot accounting is exact; decision-dependent draws (sale success, gate hazards, CV offers) read pre-indexed slots whether or not the event occurs.
- Draws are generated by `rng.draw_block` *before* the engine kernels of a step and passed in as `NoiseSlice`; no kernel holds RNG state. Results cannot depend on thread count, block size or entity order.
- Company draws use `entity_key(company_id)` so every ADIC claim on a company reads one EV draw per path (gate V24a).

### 1.8 Identifiers

| ID | Format | Example |
|---|---|---|
| Synthetic holding | `SYN-<GROUPCODE>-<4 digits>` (group codes from the taxonomy) | `SYN-PE-0042`, `SYN-RA-0007` |
| Real holding | adapter-assigned, never `SYN-` | — |
| Company / sponsor (GP) | `SYN-CMP-<6 digits>` / `SYN-GP-<4 digits>` (distinct from the group code CO) | `SYN-CMP-000417`, `SYN-GP-0031` |
| Overlay trade / CSA / facility | `SYN-TR-<5>` / `SYN-CSA-<2>` / `SYN-FAC-<2>` | — |
| Content hash | `sha256:<64 hex>` of canonical JSON or array bytes | — |
| Run | `run-<UTC yyyymmddThhmmssZ>-<first 8 hex of manifest hash>` | `run-20261018T091500Z-3f2a9c1d` |
| Artifact reference | `<run_id>:<artifact>:<json-pointer>` | `run-…:tier1_board:/rows/T6/M6/cp_upper` |
| Metric | dotted lowercase, versioned: `<family>.<name>[.<qualifier>]@v<k>` | `tier1.t6.cp_upper@v1` |
| Row key | `<FAMILY>:<k=v>[:<k=v>…]` (§3.12) | `T4P:h=07`, `LR4:g=PE:h=24` |
| Campaign / contract / decision | `cmp-<quarter>-<n>` / `ctr-<quarter>-v<n>` / `dec-<register_id>-<quarter>-<n>` | `ctr-2026Q4-v1` |

### 1.9 Logging and tracing

Standard-library `logging` with `adic_tpa.contracts.logjson.JsonFormatter`: one JSON object per line with `ts` (UTC ISO-8601), `level`, `module`, `event`, `run_id`, `campaign_id`, `plane`, `world`, and event-specific keys. No free-text numbers in log messages that claims could cite. OpenTelemetry spans (opentelemetry-api, no-op tracer by default) wrap evaluator requests, solver calls and LLM calls; span attributes mirror manifest fields. Logs go to `runs/<run_id>/logs/*.jsonl`.

### 1.10 Errors

All exceptions derive from `adic_tpa.contracts.errors.TPAError(code: str, message: str, context: dict)`. `code` is stable and used by gates and the failure taxonomy.

| Class | `code` | Raised when |
|---|---|---|
| `SchemaError` | `SCHEMA` | Pydantic or array-spec validation fails |
| `UnitError` | `UNIT` | A unit or sign tag is wrong |
| `DataClassMixError` | `DATA_CLASS_MIX` | SYNTHETIC and REAL data meet (TB7) |
| `HashMismatch` | `HASH_MISMATCH` | Any engine/config/scenario/belief/snapshot hash differs from the contract |
| `CacheMiss` | `CACHE_MISS` | A required cache entry is missing or stale (never recompute silently; paper l.7210) |
| `SolverError` | `SOLVER_NONOPTIMAL` | Any LP/MILP/QP status other than optimal |
| `InfeasibleError` | `INFEASIBLE` | A hard problem is infeasible where feasibility is required (carries the IIS) |
| `PinnedDualError` | `PINNED_DUAL` | A pricing dual equals a penalty tier, fails ×10 invariance or μ − M ≤ 0 |
| `PricingRefused` | `PRICING_REFUSED` | Prices or envelopes requested from a reverse stress, a pinned solve or an unsigned consent scenario |
| `EvidenceMissing` | `EVIDENCE_MISSING` | An EvidenceSpec does not resolve |
| `BudgetExhausted` | `BUDGET_EXHAUSTED` | Any counted budget is spent |
| `ExecutionFailed` | `EXECUTION_FAILED` | An engine fault (distinct from budget exhaustion; paper l.6685) |
| `SealBreach` | `SEAL_BREACH` | Final-plane access outside the seal runner, or a canary seen |
| `ReplayMiss` | `REPLAY_MISS` | Replay backend has no cassette for a request's structural key |
| `ReplayDrift` | `REPLAY_DRIFT` | A cassette matches the structural key but not the full request digest (S-ADR-41) |
| `EntitlementDenied` | `ENTITLEMENT` | An analyst tool call exceeds the principal's entitlements; the refusal names the rule (S-ADR-34) |
| `RunModeRefused` | `RUN_MODE` | A DEV/SYNTHETIC-only facility (software seal, test signer, synthetic committee) is requested in REAL mode (S-ADR-37) |
| `LLMRefusal` | `LLM_REFUSAL` | The whole fallback chain refused |
| `DSLCompileError` | `INVALID_SPEC/TR1`…`TR8` | A PolicySpec breaks a type rule |
| `CensusInfeasible` | `CENSUS_INFEASIBLE` | No plan-consistent PE history meets the census targets |
| `GateFailure` | `GATE/<id>` | A validation gate (V1–V24, G-A–G-E) fails |
| `LayeringViolation` | `LAYERING` | Raised by the layering test harness |

### 1.11 Configuration

- Human-edited configuration is **YAML** (`yaml.safe_load`) validated into Pydantic models with `extra="forbid"` and `frozen=True` by `contracts.config.load_yaml(path, model)`, which validates in **JSON mode** (`model.model_validate_json(json.dumps(raw, default=iso))`), because strict mode rejects enum strings and YAML lists for tuple fields when given Python objects (S-ADR-39); TOML is used only for `pyproject.toml`. `tests/unit/test_config_roundtrip.py` loads every file under `config/` through its model.
- Package configuration lives in `src/adic_tpa/config/` and is hashed as a whole into `config_hash` (sorted relative paths + file bytes). Quarter-specific inputs (signed contracts, registers, campaign settings) live in `runs/<quarter>/` and are hashed into the contract.
- Every numeric default is in config with an `# [I]`, `# [S: source]` or `# [I-calc: source]` comment; code holds no calibrated numbers.

### 1.12 SYNTHETIC labelling rule (ARCH §9.5; R15)

1. Every data row carries `is_synthetic: bool` and `data_class ∈ {SYNTHETIC, REAL}`; synthetic ids carry `SYN-`.
2. Only `synth` creates data; everything computed from a synthetic input is synthetic (`data.taint`); `RunManifest.data_class` is the taint of all inputs; SYNTHETIC and REAL together raise `DataClassMixError`.
3. Every chart, table, page, JSON artifact and CLI summary built from a SYNTHETIC run carries the footer **"SYNTHETIC – NOT ADIC DATA"** (`contracts.SYNTHETIC_FOOTER`).
4. The claim validator rejects text attributing synthetic numbers to ADIC.
5. `tpa audit labels` must report 100% coverage in CI.

### 1.13 Determinism and threads

- Evaluator processes set `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1` before importing numpy, run HiGHS with `threads=1`, and record every solver option in the manifest (ARCH §3.5; JE-MF5).
- numba kernels use `parallel=True` only over paths, never with RNG state; `NUMBA_NUM_THREADS` is recorded; every kernel is `@njit(cache=True)` with `NUMBA_CACHE_DIR` set per plane and warmed at evaluator start, outside the hash checks (S-ADR-42).
- Speed comes from processes (worlds, SAA replications, path blocks), never from threads inside one LP solve. Windows uses spawn, so worker functions are top-level and picklable, take explicit arguments (contract hash, seeds, path offsets), regenerate their cubes inside the worker instead of receiving pickled cubes, and process start-up is included in the B2 and B5 measurements.

---

## 2. Package layout

Every file lists its owner work package (WP-nn, §9.2). A directory line with a WP covers every file under it unless a file says otherwise.

```text
adic_tpa_lab/
├── pyproject.toml                         WP-01  project metadata; [tool.pytest.ini_options] pythonpath=["src"], markers (incl. requires_accounts)
├── .gitattributes                         WP-01  "* text eol=lf" so text hashes agree across checkouts (S-ADR-42)
├── tools/dev_install.py                   WP-01  writes adic_tpa_dev.pth into the venv
├── tools/port_research.py                 WP-03  copies research fixtures (read-only) into tests/regression/fixtures with SHA-256
├── tools/coverage_lite.py                 WP-03  line coverage via sys.monitoring (coverage.py is not installed; §10.3)
├── src/adic_tpa/
│   ├── __init__.py                        WP-01  __version__, SYNTHETIC_FOOTER
│   ├── __main__.py                        WP-29  python -m adic_tpa -> cli.app
│   ├── py.typed                           WP-01
│   ├── config/                                   package data, hashed into config_hash
│   │   ├── taxonomy/groups_v1.yaml, groups_v2.yaml                       WP-01
│   │   ├── metrics/wp-NN.yaml                                            one file per WP (owner = that WP); merged by registry.metrics with a duplicate-id check (S-ADR-42)
│   │   ├── engines.yaml                                                  WP-17  engine_id → import path (engine registry; no package __init__ registration)
│   │   ├── worlds/{M1,M6,B1}.yaml                                        WP-06
│   │   ├── worlds/{M2,M3,M4,M5,B2}.yaml, worlds/misspec/*.yaml           WP-31
│   │   ├── scen/{factors.yaml, panel_map.yaml, asset_classes.yaml}       WP-06
│   │   ├── state/{stress_filter.yaml, initial_state.yaml, panel.yaml}    WP-07
│   │   ├── owner.yaml                                                    WP-08
│   │   ├── groups/{pe.yaml, secondaries.yaml, realassets.yaml}           WP-09
│   │   ├── groups/{coinvest.yaml, capsol.yaml, privcredit.yaml}          WP-10
│   │   ├── groups/public.yaml                                            WP-11
│   │   ├── groups/overlay.yaml, overlay/{level1.yaml, csa_archetypes.yaml, named_stresses.yaml, simm_v2_8_2512.yaml}  WP-12
│   │   ├── overlay/templates_level2.yaml                                 WP-32
│   │   ├── ledger/{t4prime_canonical_v1.yaml, cfp_stages.yaml, facilities.yaml, ladder.yaml}  WP-13
│   │   ├── beliefs/{priors.yaml, flags.yaml, misspec_gates.yaml, translation.yaml}, bridge/levers.yaml   WP-14
│   │   ├── synth/{allocation_v1.yaml, allocation_v2.yaml, census_v1.0.yaml, census_v1.1.yaml, census_v1.1r.yaml, truth_variants.yaml, overlap.yaml}  WP-15
│   │   ├── actions/instruments.yaml                                      WP-16
│   │   ├── policy/{p0.yaml, controls.yaml, archetypes.yaml}              WP-17
│   │   ├── core/{h_presets.yaml, solver_policy.yaml, tree.yaml}          WP-18
│   │   ├── core/dsl_variables.yaml, core/search.yaml                     WP-21
│   │   ├── icm/{ftp.yaml, envelopes.yaml}                                WP-20
│   │   ├── robust/robust.yaml                                            WP-22
│   │   ├── evaluator/{gates.yaml, planes.yaml}, contract_templates/decision_quarter.yaml  WP-24
│   │   ├── llm/roles.yaml                                                WP-25
│   │   ├── lab/budgets.yaml                                              WP-26
│   │   ├── room/{register_v1.yaml, seats_theta.yaml, agenda.yaml, signers_roster.yaml}   WP-27
│   │   ├── analyst/{role_map.yaml, walls.yaml, tools.yaml, budgets.yaml}, methodology/   WP-39 (CHAT_ANALYST §9, §14.1)
│   │   └── pack/theme.yaml                                               WP-28
│   ├── data_public/                       WP-06  monthly_panel_v1.csv (copied unedited from research/addenda/gap_04_calcs/monthly_panel.csv) + .sha256; brent_quarterly_v1.csv (from research/groups/addenda/G15_calcs/data/) + .sha256; cma/*.yaml (provider anchors, as-of dated);
│   │                                             WP-41 adds the snapshotted public series (REAL public data, source and as-of per file, SHA-256)
│   ├── contracts/                         WP-01
│   │   ├── __init__.py ids.py enums.py units.py calendar.py hashing.py errors.py config.py logjson.py signing.py
│   │   ├── taxonomy.py arrays.py book.py marks.py overlay.py world.py engine_io.py ledger.py beliefs.py rules.py
│   │   └── policy.py optimizer.py actions.py contract.py evidence.py lab.py claims.py room.py tools.py ports.py analyst.py
│   ├── rng/                               WP-02  __init__.py keys.py philox.py samplers.py streams.py
│   ├── numerics/                          WP-02  __init__.py pwl.py roots.py linalg.py lse.py numba_utils.py
│   ├── stats/                             WP-02  __init__.py cp.py bootstrap.py multiple.py dsr.py pbo.py mde.py bpoe.py ce.py
│   ├── testing/                           WP-03  __init__.py fixtures.py fakes.py trees.py golden.py fixture_h.py committee.py   (FBE generators: beliefs/validation.py)
│   ├── registry/                          WP-04  __init__.py store.py chain.py artifacts.py metrics.py provenance.py mfdr.py schema.sql
│   ├── data/                              WP-05  __init__.py schemas.py store.py freeze.py taint.py quarantine.py
│   │   └── adapters/__init__.py base.py marks_archive.py   WP-05 (schema + contract test, wave 1);  hf_terms.py pe_unfunded.py overlay_crif.py csa.py facility.py owner_draw.py loan_tape.py  WP-37
│   ├── synth/                             WP-15  __init__.py config.py census.py history.py book.py truth.py observation.py quotes.py overlap.py overlay_book.py realassets.py releases.py gates.py misspec.py sealed.py
│   ├── scen/                              WP-06  __init__.py regimes.py factors.py cma.py oil.py vol.py ensemble.py bootstrap.py cube.py assets.py calibrate.py
│   ├── state/                             WP-07  __init__.py filter.py fragility.py exitfilter.py nowcast.py initial.py panel.py harness.py
│   ├── owner/                             WP-08  __init__.py fiscal.py draw.py modes.py payout_library.py
│   ├── priv/                              WP-09  __init__.py fund.py realassets.py templates.py financing.py   (intra-quarter profiles live in contracts/rules.py)
│   │   ├── company.py claims.py credit.py overlap.py                     WP-10
│   ├── pub/                               WP-11  __init__.py hf.py queue.py longonly.py p2s.py
│   ├── overlay/                           WP-12  __init__.py books.py level1.py pricers.py surfaces.py greeks.py crif.py vm.py simm.py limits.py monetize.py services.py valuation.py engine.py
│   │   └── templates.py                   WP-32 (Level-2 templates; surfaces.py extended by WP-32)
│   ├── beliefs/                           WP-14  __init__.py marks.py irr_translation.py fbe.py translations.py market_implied.py credibility.py diagnostics.py scoring.py blp.py perf.py draws.py validation.py
│   ├── bridge/                            WP-14  __init__.py wyntb.py
│   ├── ledger/                            WP-13  __init__.py kernel.py rows.py recourse.py redtest.py ladder.py stress.py readiness.py cfp.py facilities.py covenants.py leverage.py linear.py
│   ├── actions/                           WP-16  __init__.py library.py admissibility.py columns.py scores.py cards.py flips.py
│   ├── core/
│   │   ├── __init__.py observables.py sim.py factory.py policy.py terminal.py certify.py   WP-17
│   │   ├── tree.py h.py solver.py phase1.py phase2.py duals.py kernel.py              WP-18
│   │   ├── colgen.py levelb.py safety.py                                              WP-19
│   │   ├── mpc.py                                                                     WP-20
│   │   ├── dsl.py search.py                                                           WP-21
│   │   └── irb.py                                                                     WP-23
│   ├── icm/                               WP-20  __init__.py pricing.py envelopes.py ftp.py charges.py recovery.py contingent.py pacing.py transfers.py services.py
│   ├── robust/                            WP-22  __init__.py ensemble.py tilts.py kms.py ep.py reverse.py persistence.py frontier.py
│   ├── attrib/                            WP-23  __init__.py prices.py counterfactual.py shapley.py null.py dva.py moved.py
│   ├── evaluator/                         WP-24  __init__.py service.py server.py client.py tools.py planes.py cache.py counting.py gates.py hashcheck.py failures.py finalists.py
│   ├── seal/                              WP-24  __init__.py salt.py commit.py runner.py
│   │   └── canary.py                      WP-38
│   ├── claims/                            WP-25  __init__.py placeholders.py render.py validator.py icd203.py provenance.py
│   ├── agents/                            WP-25  __init__.py gateway.py roles.py loop.py tools.py cost.py
│   │   ├── backends/__init__.py base.py anthropic_backend.py replay.py stub.py
│   │   └── prompts/*.md                   (one frozen prompt per role; hashed into llm_policy)
│   ├── lab/                               WP-26  __init__.py fsm.py campaign.py budgets.py memory.py archive.py escalation.py firewall.py
│   │   └── calibration.py                 WP-38
│   ├── idm/                               WP-27  __init__.py register.py compiler.py briefs.py seats.py protocol.py ballots.py decision_log.py signposts.py consent.py evsi.py politics.py room_service.py
│   ├── pack/                              WP-28  __init__.py build.py payload.py figures.py theme.py linter.py
│   │   ├── templates/base.html.j2 l0.html.j2 l1_brief.html.j2 l2_drill.html.j2 console.html.j2
│   │   └── static/ep.js pack.css
│   ├── analyst/                           WP-39  __init__.py principal.py policy.py service.py tools_read.py sessions.py overrides.py backtranslate.py runs.py
│   │                                             chat.py turn.py stub_grammar.py replay_runner.py audit.py eval.py server.py   (names per CHAT_ANALYST §14.1)
│   │                                      WP-40  ask_http.py (loopback `tpa ask serve`), W3 runs, live evaluation
│   ├── pipeline/                          WP-30  __init__.py quarter.py cycle.py
│   ├── cli.py                             WP-29
│   └── mcp_server.py                      WP-29  dispatch only: evaluator.server and analyst.server own the server factories (S-ADR-42)
├── tests/                                 (owner WP per test file = owner of the module under test; cross-module tests have a named owner in §10.6)
│   ├── unit/ property/ metamorphic/ regression/ reconciliation/ solver/ statistical/ recovery/ skeleton/ agents/ analyst/
│   ├── overlay/ determinism/ layering/ drills/ room/ labelling/ perf/ e2e/
│   ├── regression/fixtures/               WP-03  ported research inputs and frozen JSON outputs (read-only copies + SHA-256)
│   ├── golden/                            WP-03  golden mini-cube, mini FlowCube, fixture tree, golden manifests, EP golden cases
│   └── cassettes/<role>/<key>.json        WP-25  recorded LLM responses for the Replay backend
├── runs/                                  outputs (git-ignored): runs/<quarter>/contract.yaml, runs/<run_id>/{manifest.json, artifacts/, logs/, pack/}
└── stores/                                stores/data/SYNTHETIC/ (bitemporal Parquet), stores/data/REAL/ (empty until in-region serving), stores/truth/ (sealed; ACL),
                                           stores/seal/ (per-campaign salts; CRO-only ACL; REAL mode), stores/registry.sqlite;
                                           DEV/SYNTHETIC mode keeps the software seal's salt under runs/<run_id>/seal/ (S-ADR-37)
```

---

## 3. Data contracts

All models live in `adic_tpa.contracts` (WP-01). Pydantic models use `model_config = ConfigDict(frozen=True, extra="forbid", strict=True)` unless marked mutable; external data (YAML, JSON, MCP payloads, registry rows) is always validated in JSON mode (`model_validate_json`, S-ADR-39); models are never used as set members or dict keys (a frozen model with a dict field is unhashable; caches key on `content_hash`); anything holding numpy arrays is a frozen dataclass, never a Pydantic model. **Array containers** are `@dataclass(frozen=True, slots=True)` subclasses of `contracts.arrays.ArrayContainer`; they hold numpy arrays plus a Pydantic `meta`, and `validate()` checks them against `contracts.arrays.ARRAY_SPECS` (§3.17). Units follow §1.2; field suffixes `_bn` (USD bn), `_a` (annual decimal), `_q` (per quarter), `_m` (per month).

### 3.1 Enumerations (`contracts/enums.py`)

```python
class Lens(StrEnum):            SELL, HOLD, REFINANCE, LEVER, ADD, PACE   # REFINANCE = cash-out; LEVER = exposure-up ≡ ADD + REFI
class Plane(StrEnum):           CALIBRATION, SEARCH, FINAL, HISTORICAL, EXPLORATION
class MandateMode(StrEnum):     B_OWNER_CALL = "B"; H_HYBRID = "H"; A_ADIC_RULE = "A"
class ContractMode(StrEnum):    NORMAL = "NORMAL"; EXECUTION_RECOVERY = "EXEC_RECOVERY"; STRUCTURAL_RECOVERY = "STRUCT_RECOVERY"
class ConsentScenario(StrEnum): R0X = "R0x"; R0 = "R0"; R1 = "R1"; R2 = "R2"      # ordered R0x < R0 < R1 < R2
class CFPStage(IntEnum):        GREEN = 0; AMBER = 1; RED = 2; BLACK = 3
class RecourseTier(StrEnum):    T, TP, TPF, TPFA, ALL                              # nested (GROUPS §2.4)
class MacroRegime(IntEnum):     EXP = 0; LATE = 1; CRIS = 2; RECV = 3
class ExitWindow(IntEnum):      O = 0; N = 1; D = 2; F = 3
class ShockType(IntEnum):       N = 0; B = 1; SG = 2; DB = 3; SS = 4; GW = 5
class StressState(IntEnum):     CALM = 0; ELEVATED = 1; CRISIS = 2
class FinWindow(IntEnum):       OPEN = 0; TIGHT = 1; CLOSED = 2                    # S-ADR-12
class Clock(StrEnum):           MONTHLY, QUARTERLY
class FlowType(IntEnum):        # (expected sign, cash?)  F = 18
    CALL=0 (−,cash); DISTRIBUTION=1 (+); INCOME_CASH=2 (+); PIK_ACCRUAL=3 (+, NON-CASH); SALE_PROCEEDS=4 (+); FEES=5 (−)
    VM=6 (±); DELTA_IM=7 (±); PREMIUM=8 (−); MONETIZATION=9 (+); REDEMPTION_PAY=10 (+); DEBT_DRAW=11 (+)
    DEBT_REPAY=12 (−); DEBT_SERVICE=13 (−); CAPEX=14 (−); OWNER_DRAW=15 (−); OPEX=16 (−); INTEREST_ON_CASH=17 (±)
class Counterparty(StrEnum):    EXTERNAL, INTRA_ADIC
class SaleReason(IntEnum):      NONE=0; DISCRETIONARY=1; PLANNED=2; RECOURSE_LIQUID=3; RECOURSE_AMBER=4; RECOURSE_RED=5   # reporting labels only:
                                # whether a sale is a T6 red event is decided by ledger.red_test on economic substance (S-ADR-30)
class RunMode(StrEnum):         DEV_SYNTHETIC, REAL                                 # S-ADR-37
class FactorKind(StrEnum):      LOGRET, LEVEL, CHANGE                               # S-ADR-35
class AnswerStatus(IntEnum):    EXPLORATORY = 0; BASELINE = 1; SEARCH = 2; SEALED_NOT_QUALIFIED = 3; QUALIFIED = 4   # S-ADR-34; an answer takes the minimum used
class DataClass(StrEnum):       SYNTHETIC, REAL
class PricedOn(StrEnum):        FEASIBLE = "feasible"; RESTORED = "restored_problem"
class EvidencePlane(StrEnum):   SEALED = "sealed"; SEARCH = "search"; EXPLORATORY = "exploratory"
class MarkType(StrEnum):        UNDERWRITTEN, ACTUAL, FORECAST, MARKET_IMPLIED
class Book(StrEnum):            TAIL, OPP, BETA
class HFLotState(IntEnum):      LOCK, SOFT, OPEN, NOTICE, QUEUE, SUSP, PAY, SP, LIQ, DONE, TRS_TERM
class CreditState(IntEnum):     PERFORMING, PIK, AMENDED, EXTENDED, NONACCRUAL, DEFAULT, WORKOUT, RESOLVED, REPAID
class RowFamily(StrEnum):       TRANSITION, T1_PAYOUT, T2_IG_HARD, T2_IG_TARGET, T3_COV30, T4P, T4P_APPETITE, T5_DEBT, T5_EXPOSURE, T5_ENCUMBRANCE,
                                T5_PLEDGE, T5_MATURITY, T8_DCR, LR4, LR8, NAVF_LTV, RA_LTV, SALE_DEPTH, HF_NOTICE, P2S_CAP, FAC_AVAIL,
                                RED_MARGIN, T6_CVAR, FLOOR_CVAR, UTILITY, SHORTFALL, OV1, OV2, OV3, DEALER, TAIL_BUDGET, LEVEL_B
class RowRole(IntEnum):         DEFINITION=0; PRICING=1; APPETITE=2; STRUCTURAL=3      # only PRICING rows feed λ, cards, envelopes
class GateLabel(StrEnum):       CORRECT, PROMOTED, NOT_PROMOTED, QUALIFIED, NOT_QUALIFIED, NOT_CORRECT, NOT_ASSESSED
class FailureLabel(StrEnum):    INVALID_SPEC, TIER1_FAIL, FLOOR_FAIL, NI_FAIL, OV_FAIL, PINNED_DUAL, GAMBLING, BUDGET_EXHAUSTED, EXECUTION_FAILED
class OptionKind(StrEnum):      STATUS_QUO, DEFER, RECOMMENDED, ALTERNATIVE, ARCH_A, ARCH_B, ARCH_C
class Tier(StrEnum):            A, B, C, BOARD
class RoleId(StrEnum):          CONTRACT_DRAFTER, DESIGN_REVIEWER, IDEATOR, EXECUTOR, ABLATION_PROPOSER, ABLATION_FILTER, RED_TEAM,
                                MEMO_WRITER, AUDITOR, TRANSLATOR, QA_ANSWERER, SEAT_NARRATOR, FACILITATOR, AI_VALIDATOR,
                                MINUTES_DRAFTER, EXTRACTOR
class ModelFamily(StrEnum):     A, B, C
class LLMMode(StrEnum):         OFFLINE, REPLAY, LIVE
class CampaignState(StrEnum):   DRAFT, FROZEN, SIGNED, SIGNED_IN_RECOVERY, DESIGN_REVIEWED, BASELINE_PRICED, IDEATION, SCREENING,
                                SELECTION, SEALED, RETROSPECTIVE, MEMO, REVIEW, SHADOW_IC, PREVOTE_LOCK, IC, CLOSED, ABORTED
class T6SurrogateKind(StrEnum): CVAR_CLASS, WORST_CASE_CVAR, ALSO_X
class TargetMode(StrEnum):      PRECOMMITTED, ROLLING
CensusId = Literal["v1.0", "v1.1", "v1.1r"];  AllocationId = Literal["v1", "v2"]
WorldId = str   # "M1".."M6", "B1", "B2", "MS:<name>"; validated by contracts.world.validate_world_id
class ReturnBasis(BaseModel): kind: Literal["arith", "geom", "log"]; fees: Literal["gross", "net"]
# contracts/ids.py — NewType(str) aliases with the §1.8 formats validated on construction:
#   GroupId, HoldingId, UnitId (holding id or cohort id), CompanyId, SponsorId, TradeId, CsaId, FacilityId,
#   RunId, MetricId, DecisionId, ContractId, CampaignId, ArtifactRef ("<run_id>:<artifact>:<json-pointer>")
# contracts/arrays.py — dtype aliases: F32, F64 = npt.NDArray[np.float32 | np.float64]; I8, I16, I32; U32, U64; B (bool)
```

`FlowType.sign(ft) -> int` and `FlowType.is_cash(ft) -> bool` are table lookups; the ledger ignores non-cash types for liquidity.

### 3.2 Taxonomy (`contracts/taxonomy.py`)

```python
class GroupSpec(BaseModel):
    group_id: GroupId                 # "PE"
    code: str                         # SYN id code: PE, SEC, CS, CO, PM, PC, OVL, RA, CF, TPA
    display_name: str
    kind: Literal["private", "public", "overlay", "funding", "attribution"]
    engines: tuple[Literal["fund", "company", "claims", "credit", "realassets", "hf", "longonly", "overlay", "treasury"], ...]
    recourse_tier: RecourseTier | None   # tier where its SALES enter: PUBLIC→TP, PRIVCREDIT/CAPSOL→TPFA, PE/SEC/CO/RA→ALL
    red_tier: bool                       # forced sale = T6 red event (S-ADR-05)
    amber_tier: bool
    has_unfunded: bool
    age_buckets: tuple[str, ...] = ("young", "mature")
    young_max_age_years: float = 4.0
    lenses: tuple[Lens, ...]
    forecast_basis: Literal["gp_projection", "deal_model", "contract_yield", "loss_adjusted_yield", "net_alpha",
                            "benchmark_ir", "strategy_pnl", "business_plan"]
    fbe_path: Literal["fund", "single_deal", "cohort", "hierarchical_factor", "benchmark", "scenario"]
    seat: bool
    commitment_split: float = 0.0        # canonical new-commitment split (sum = 1 over groups)
    pacing_eta_sign: Literal[-1, 0, 1] = 0
    contingent_budget: bool = False
    in_envelopes: bool = True
    fund_distribution_stress: bool = False   # s* applies 0.45(1 − θ) × drought rates to its fund distributions (PE, SEC, CO);
                                             # decoupled from red_tier: RA follows the stressed-income convention (S-ADR-32)

class CouplingSpec(BaseModel):
    kind: Literal["offered_flow", "shared_gp_effect", "recap_netting"]
    source: GroupId; target: GroupId; params: dict[str, float | list[float] | str]   # incl. time_unit ("quarter")

class TaxonomyConfig(BaseModel):
    version: Literal["v1", "v2"]; groups: tuple[GroupSpec, ...]
    strategies: dict[GroupId, tuple[str, ...]]; couplings: tuple[CouplingSpec, ...]

class GroupRegistry:                    # immutable runtime view
    @classmethod
    def load(cls, path: Path | None = None) -> "GroupRegistry": ...   # default config/taxonomy/groups_v2.yaml
    def ids(self, kind: str | None = None) -> tuple[GroupId, ...]: ...  # taxonomy order; stable
    def spec(self, g: GroupId) -> GroupSpec: ...                        # raises SchemaError on unknown id
    def private(self) -> tuple[GroupId, ...]: ...
    def red_tier(self) -> tuple[GroupId, ...]: ...
    def index(self, g: GroupId) -> int: ...                             # column index in [.., G, ..] arrays
    @property
    def hash(self) -> str: ...
```

`groups_v2.yaml` content (normative; S-ADR-01/02):

| group_id | code | kind | engines | recourse_tier | red | amber | seat | split | η sign | contingent |
|---|---|---|---|---|---|---|---|---|---|---|
| PE | PE | private | fund | ALL | ✓ | | ✓ | 0.50 | +1 | |
| SECONDARIES | SEC | private | fund, company | ALL | ✓ | | ✓ | 0.10 | −1 | ✓ |
| CAPSOL | CS | private | claims, company | TPFA | | ✓ | ✓ | 0.10 | −1 | ✓ |
| COINVEST | CO | private | company | ALL | ✓ | | ✓ | 0.10 | +1 | |
| PUBLIC | PM | public | hf, longonly | TP | | | ✓ | 0 | 0 | |
| PRIVCREDIT | PC | private | credit, fund | TPFA | | ✓ | ✓ | 0.10 | 0 | ✓ |
| OVERLAY | OVL | overlay | overlay | — | | | ✓ | 0 | 0 | |
| REALASSETS | RA | private | realassets, fund | ALL (open-end redemptions: amber) | ✓ | ✓ | ✓ | 0.10 | +1 | |
| CF | CF | funding | treasury | T | | | (Treasurer seat) | 0 | 0 | |
| TPA | TPA | attribution | — | — | | | | 0 | 0 | |

`fund_distribution_stress` is true for PE, SECONDARIES and COINVEST only. `groups_v1.yaml` drops REALASSETS and sets the PE split to 0.60 (GROUPS §2.2 convention 60/10/10/10/10). Couplings in both: `offered_flow` PE → COINVEST over a 20-quarter kernel with yearly weights, O_t = θ Σ_{j=0}^{19} ¼ d_{⌊j/4⌋} C^PE_{t−j} (`params: {theta: 0.33, d_per_year: [0.15, 0.25, 0.25, 0.20, 0.15], acceptance: [0.3, 0.6], time_unit: quarter}`; G-gap_04 §1.2), `shared_gp_effect` among PE, COINVEST, SECONDARIES (ρ_GP = 0.6), `recap_netting` COINVEST ↔ PRIVCREDIT.

### 3.3 Book (`contracts/book.py`)

```python
class Holding(BaseModel):
    holding_id: HoldingId; group: GroupId; strategy: str; sub_strategy: str | None = None
    unit_kind: Literal["fund", "company", "claim", "loan_cohort", "hf_lot", "longonly", "treasury",
                       "ra_asset", "ra_open_end", "overlay_bucket"]
    gp_id: SponsorId | None = None; company_ids: tuple[CompanyId, ...] = ()
    vintage: int | None = None; region: Literal["US", "EUROPE", "ASIA", "GCC", "EM", "GLOBAL"]; sector: str | None = None
    commitment_bn: float | None = None; unfunded_bn: float = 0.0            # >= 0, <= commitment
    nav_reported_bn: float                                                  # >= 0
    nav_reference_date: date
    wrapper: Literal["SMA", "CEF", "EVERGREEN", "BDC", "COMMINGLED", "MANAGED_ACCOUNT", "DIRECT", "JV",
                     "OPEN_END", "CLOSED_END", "LISTED", "TREASURY"] | None = None
    consent_transfer: bool = True; consent_pledge: bool = True; rofr: bool = False
    pledged_bn: float = 0.0; encumbered_bn: float = 0.0
    terms: (PrivateFundTerms | CompanyTerms | ClaimTerms | LoanCohortTerms | HFTerms | LongOnlyTerms
            | TreasuryTerms | RealAssetTerms | None) = Field(discriminator="kind")
    is_synthetic: bool; data_class: DataClass; source: str
    # validators: is_synthetic == (data_class == SYNTHETIC) == holding_id.startswith("SYN-"); unfunded <= commitment;
    #             terms.kind matches unit_kind
```

| Terms model | Fields (units) |
|---|---|
| `PrivateFundTerms` (kind="fund") | strategy_class ∈ {buyout_large, buyout_mid, growth, vc, sector, special_sits, secondary_fund, credit_fund, ra_closed}; age_years; effective_age_years; fee_rate_a; carry; hurdle_a; lpa_term_years; extensions_used; subscription_line_bn; gp_navloan_bn; recallable_bn; recycling_cap = 1.10; sec_template ∈ {S1…S6} \| None; theta_true_over_ref (Secondaries) \| None |
| `CompanyTerms` | ownership; ev_bn; net_debt_bn; ebitda_bn; entry_ev_ebitda; icr; software_flag; spv_debt_bn; beta_asset; sigma_id_a; exit_route |
| `ClaimTerms` (Capital Solutions) | family ∈ {A…G}; claim_bn; coupon_a; pik_share_cap; pik_window_q; step_up_a; make_whole; moic_floor; warrants (n_w, strike_bn, expiry) \| None; seniority; ltv; icr; negative_ebitda; status: CreditState; syndication_share |
| `LoanCohortTerms` (Private Credit) | segment ∈ {DL, ABF, MEZZ, OPP}; vehicle_id; wrapper; n_loans; par_bn (incl. PIK); spread_a; floor_a; oid; wam_years; undrawn_bn; sponsored_share; software_share; state_shares: dict[CreditState, float] (sum 1); collateral_type (LGD key, S-ADR-11); evergreen_cap_q |
| `HFTerms` (τ) | strategy; dealing ∈ {monthly, quarterly, semiannual, annual}; notice_days; notice_revocable = False; lockup_end \| None; soft_lock_fee; gate_type ∈ {none, investor, fund}; gate_level; holdback; payment_lag_days; side_pocket_cap; suspension_allowed; transfer_consent; pledge_consent; beta_eq_normal; beta_eq_crisis; alpha_net_a; alpha_sd_a; crisis_gate_hazard_q; leverage_navw; smoothing_theta; adic_share_of_fund |
| `LongOnlyTerms` | sleeve ∈ {DM_EQ, EM_EQ, FI}; benchmark; beta; te_a; ir_prior; adv_bn; vehicle ∈ {SMA, COMMINGLED}; tax_rate; credit_beta |
| `TreasuryTerms` | sleeve ∈ {CASH, UST, IG}; haircut; hqla_level ∈ {L1, L2A, L2B}; cf_controlled; duration_years |
| `RealAssetTerms` | sector ∈ {REAL_ESTATE, INFRASTRUCTURE, ENERGY_NATRES}; access ∈ {CLOSED_END_FUND, OPEN_END_FUND, COINVEST, DIRECT, JV}; noi_bn; cap_rate; inflation_passthrough; oil_beta; capex_reserve_rate_a; development: DevelopmentPlan \| None (committed_bn, s_curve_quarters); debt: AssetDebt \| None; open_end: OpenEndTerms \| None (dealing, notice_days, gate_pct_nav_q); appraisal_lambda; report_lag_q |
| `AssetDebt` | balance_bn; rate_type ∈ {FIXED, FLOATING}; spread_a; hedge_ratio; maturity; ltv_max; dscr_covenant; amort_q; recourse: Literal[False] = False |

```python
class SponsorNode(BaseModel): sponsor_id: SponsorId; tier: Literal["elite", "core", "other"]
class CompanyNode(BaseModel): company_id: CompanyId; sponsor_id: SponsorId | None; sector: str; ev_bn: float
                              net_debt_bn: float; ebitda_bn: float; icr: float; software_flag: bool
class ClaimEdge(BaseModel):   holder_id: HoldingId; company_id: CompanyId; share: float; seniority: int
                              claim_kind: Literal["pe_lookthrough", "coinvest_equity", "cs_claim", "pc_loan", "sec_cv"]
class OverlapGraph(BaseModel):
    sponsors: tuple[SponsorNode, ...]; companies: tuple[CompanyNode, ...]; edges: tuple[ClaimEdge, ...]
    def gp_concentration(self, book: "BookSnapshot") -> dict[SponsorId, float]: ...   # share of private NAV + unfunded

class Facility(BaseModel):
    facility_id: FacilityId; kind: Literal["revolver", "nav_facility", "repo", "term_debt", "cf_term_prefund"]
    status: Literal["signed", "requested", "indicative"]; committed: bool
    size_bn: float; drawn_bn: float = 0.0; spread_drawn_a: float; fee_undrawn_a: float; fee_upfront: float
    maturity: date; n_banks: int | None = None; max_bank_share: float | None = None
    covenant_headroom_test: bool = True; test_draw_annual: bool = True
    credit_30d: Literal[0.0] = 0.0          # facilities never count in 30-day rows
    credit_stress: float                     # canonical credit in T4′ rows: revolver 0.5 from month 2 in s* (pricing set; 0.8 in the research set, S-ADR-32)
    available_from_month: int = 2
    pledge_pool_cap_share: float | None = None   # NAV facility: 0.20 of private NAV
    ltv_normal: float | None = None; ltv_stressed: float | None = None
    lead_time_q: int = 0
    consent_scenario: ConsentScenario        # lowest scenario in which it may be priced

class CSA(BaseModel):
    csa_id: CsaId; dealer_id: str; threshold_bn: float; mta_bn: float; ia_bn: float
    eligible_collateral: tuple[Literal["cash", "ust", "ig"], ...]; reuse_right: bool
    im_regime: Literal["two_way_simm", "ia_only", "cleared"]
    phi_recognition: float                   # 1.0 cash VM, 0.7 OTC collateral with reuse, 0.0 pledged
    gcc_dealer: bool = False; settlement_lag_bd: int = 1; stress_delay_bd: int = 3   # S-ADR-15

class OwnerDrawHistory(BaseModel):
    convention: Literal["opening_fy_reported_nav", "fixed_usd", "current_nav"]
    history: tuple[tuple[int, float], ...]   # (fiscal year, rate)
    d_prev: float                            # FY2026 actual rate (client data; SYNTHETIC 0.058)
    band_agreement: SignOff | None = None    # Mode H only (S-ADR-14)

class BookSnapshot(BaseModel):
    snapshot_id: str; asof: date; known_at: datetime
    taxonomy_version: Literal["v1", "v2"]; allocation: AllocationId | None; census_id: CensusId | None
    holdings: tuple[Holding, ...]; overlap: OverlapGraph; facilities: tuple[Facility, ...]
    overlay: "OverlayBook"; owner: OwnerDrawHistory
    nav_total_reported_bn: float; data_class: DataClass; content_hash: str
    def by_group(self) -> dict[GroupId, tuple[Holding, ...]]: ...
    def unit_index(self) -> "UnitIndex": ...   # stable order: taxonomy group order, then holding_id
    # validators: Σ nav_reported == nav_total (1e-9); every group in the taxonomy; one data_class
```

`UnitIndex` (array container): `unit_ids: tuple[UnitId, ...]`, `group_of: I32[U]`, `engine_of: tuple[str, ...]`, `age_bucket: I8[U]`, `red_tier: B[U]`.

### 3.4 Overlay contracts (`contracts/overlay.py`)

```python
class OverlayTrade(BaseModel):
    trade_id: TradeId; book: Book; template: str; client_group: GroupId | None = None; service_id: str | None = None
    underlying: str; strike_rel: float | None = None; strike2_rel: float | None = None; expiry: date | None = None
    notional_bn: float; premium_bn: float; venue: Literal["listed", "cleared", "bilateral"]; csa_id: CsaId | None = None
    rung: Literal["3M", "6M", "12M"] | None = None; s_lock_a: float | None = None; trigger_state: str | None = None
    is_synthetic: bool; data_class: DataClass

class CRIFRow(BaseModel):                       # ISDA Risk Data Standards keys (GROUPS §3.7)
    trade_id: TradeId; portfolio_id: str; product_class: Literal["RatesFX", "Credit", "Equity", "Commodity"]
    risk_type: str; qualifier: str; bucket: str; label1: str | None; label2: str | None
    amount_usd_bn: float; im_model: Literal["SIMM", "Schedule"]; end_date: date | None
    post_regulations: str | None; collect_regulations: str | None

class ServiceContract(BaseModel):
    service_id: str; client_group: GroupId
    kind: Literal["completion_beta", "p2s", "pe_beta_rebuild", "group_hedge", "portable_alpha_collateral"]
    notional_bn: float; reference_index: str; s_lock_a: float; clc_basis_bn: float

class OverlayPolicy(BaseModel):
    tail_budget_a: float = 0.0015            # IC floor 0.15% of NAV a year; cap 0.50% (GROUPS §3.7)
    tail_budget_cap_a: float = 0.0050
    ladder_weights: tuple[float, float, float] = (0.25, 0.50, 0.25)   # 3M/6M/12M rungs, 90/72 put spreads
    opp_vol_target_a: float = 0.011; opp_im_budget_bn: float = 1.5; completion_beta_bn: float = 10.0
    ov1_ratio: float = 0.75; ov2_max: float = 0.25; ov3_share: float = 0.5   # [I] IC-set
    dealer_max_share_nav: float = 0.005; min_dealers: int = 5

class OverlayBook(BaseModel):
    trades: tuple[OverlayTrade, ...]; csas: tuple[CSA, ...]; services: tuple[ServiceContract, ...]
    policy: OverlayPolicy; fixture: bool = False   # True for the ≈250-trade engine-test blotter
```

`OverlayGreeks` (array container): `delta F64[B, K]`, `gamma_diag F64[B, K]`, `vega F64[B, J]` (by expiry bucket), `vanna F64[B, J]`, `volga F64[B, J]`, `theta F64[B]`, `nv_eq F64[S]` (economic net VIX-equivalent vega per named stress), `pnl_stress F64[B, S]`; B = 3 books, K factors, J vega buckets, S named stresses.

### 3.5 Marks and forecasts (`contracts/marks.py`)

```python
class CaseMap(BaseModel):                       # brief §9: cases read as nominal quantiles unless the group states otherwise
    down: Literal["p05", "p10", "p25"] = "p10"; base: Literal["p50"] = "p50"; up: Literal["p75", "p90", "p95"] = "p90"
class Mark(BaseModel):
    holding_id: HoldingId; mark_type: MarkType; as_of: date; recorded_at: datetime
    basis: Literal["IRR", "MOIC", "TVPI", "YIELD", "YIELD_ON_COST", "EXIT_CAP_RATE", "NAV", "PRICE"]; gross_net: Literal["gross", "net"]
    since_inception: bool = True                 # ADIC's IRR/MOIC marks are since inception (shown as sunk)
    value: float; horizon_years: float | None = None; exit_date: date | None = None; author: str; revision_id: int
    case_down: float | None = None; case_base: float | None = None; case_up: float | None = None
    case_map: CaseMap = CaseMap()                # per-group override from config/beliefs/translation.yaml
    is_synthetic: bool; data_class: DataClass

class ForecastSnapshot(BaseModel): u: float | None; a: float | None; nav_bn: float; regime: MacroRegime; exit: ExitWindow
class ForecastRecord(BaseModel):
    record_id: str; group: GroupId; holding_id: HoldingId | None; author: str; as_of: date; recorded_at: datetime
    horizon_q: int; exit_horizon_q: int | None = None       # forecast exit timing (IRR/MOIC targets)
    target: Literal["irr_si", "moic_si", "fwd_return_a", "distributions_bn", "calls_bn", "exit_quarter", "net_alpha_a",
                    "tvpi", "lay_a", "pnl_bn"]              # irr_si / moic_si: since-inception net, as ADIC files them (S-ADR-27)
    case_map: CaseMap = CaseMap()
    quantiles: dict[Literal["p05", "p10", "p25", "p50", "p75", "p90", "p95"], float]   # from the cases via case_map; p10 < p50 < p90
    cashflow_ref: ArtifactRef | None = None                 # the unit's cash-flow history used by the translation
    cashflows_4q: tuple[float, ...] | None = None; cashflows_8q: tuple[float, ...] | None = None
    snapshot: ForecastSnapshot; decision_link: DecisionId | None = None; shadow_id: str | None = None   # declined deals
    resolved_value: float | None = None; resolved_at: date | None = None
    is_synthetic: bool; data_class: DataClass

class Quote(BaseModel):
    quote_id: str; holding_id: HoldingId; as_of: date; kind: Literal["secondary_bid", "financing_reserve", "dealer_hybrid"]
    bid_pct_ref_nav: float; ref_nav_date: date; deferral_share: float = 0.0; deferral_months: int = 0
    source: Literal["external", "in_house"]; desk: GroupId | None = None; counterparty_class: str
    conflict_flag: bool; second_source_id: str | None = None   # validator: in_house ⇒ conflict_flag
    is_synthetic: bool; data_class: DataClass

class Milestone(BaseModel):
    holding_id: HoldingId; milestone_id: str; description: str; due: date
    verification_source: str; status: Literal["pending", "met", "missed"]
```

### 3.6 World and state (`contracts/world.py`)

```python
class CMALine(BaseModel):
    asset_class: str; arith_mean_a: float; vol_a: float; basis: ReturnBasis; benchmark: str
    fee_adjusted: bool; selection_included: bool; levered: bool = False
class RegimeParams(BaseModel):
    n_macro: Literal[3, 4, 5] = 4; dwell_substates: int = 3            # state-expanded HMM for NB dwell (PD §4.3)
    P_macro: list[list[float]]; P_exit: list[list[float]]; P_shock_annual: list[list[float]]; kappa_shock_macro: list[list[float]]
    gw_dwell_by_elapsed: list[float]
class FactorModelParams(BaseModel):
    factor_names: tuple[str, ...]; factor_kinds: tuple[FactorKind, ...]          # S-ADR-35
    c: dict[str, list[float]]; A: list[list[float]]; D: dict[str, list[float]]
    R0: list[list[float]]; R_crisis: list[list[float]]; omega: dict[str, float]
    df: int = 5                                  # innovations ε = sqrt((df − 2)/df) · t_df (unit variance)
    provenance: dict[str, Literal["fitted", "set_and_verified"]]                  # per factor; set_and_verified until data exist
    asset_loadings: dict[str, list[float]]; asset_alpha: dict[str, dict[str, float]]; asset_sigma: dict[str, dict[str, float]]
class OilParams(BaseModel):  mean_level: float = 70.0; kappa: dict[str, float]; vol: dict[str, float]; rho_eq: dict[str, float]; gw_jump: dict[str, float]
class VolParams(BaseModel):  beta_T_coef: float = 0.94; beta_T_exp: float = -0.43; spot_vol_slope: tuple[float, float] = (-1.35, -0.94)
                             move: dict[str, float]; ovx: dict[str, float]
class BootstrapParams(BaseModel): panel_start: date; panel_end: date; block_months: tuple[int, int] = (12, 24); embargo_months: int = 12
                                  method: Literal["stationary_block", "fhs"]
                                  observed_factors: tuple[str, ...]             # resampled from data_public panels
                                  fill: Literal["conditional_e"] = "conditional_e"   # other factors from E given the block; labelled PROXY
class MisspecOverride(BaseModel):                # S-ADR-43
    target_module: Literal["priv", "pub", "overlay", "owner", "ledger", "policy", "scen"]
    param_path: str                              # dotted path into the target's config model
    op: Literal["set", "mult"]; value: float | str | bool
class WorldSpec(BaseModel):
    world_id: WorldId; family: Literal["E", "B1", "B2"]; provider: str; cma_asof: date
    cma: dict[str, CMALine]; regime: RegimeParams | None; factors: FactorModelParams | None
    oil: OilParams; vol: VolParams; bootstrap: BootstrapParams | None = None
    misspec_tags: tuple[str, ...] = (); overrides: tuple[MisspecOverride, ...] = ()
    t6_class: Literal["M1_M5", "M6", "REPORT_ONLY"]  # B1/B2 → M1_M5; misspecification worlds → M6 for T6, report-only for Tier 1B
    content_hash: str

class OilState(BaseModel): spot: float; front: float; chi0: float; xi0: float   # χ0 = ln spot − ln front (gap_04 §6.1 step 6)
class StateSnapshot(BaseModel):
    asof: date; data_timestamps: dict[str, datetime]
    pi0_macro: tuple[float, ...]; pi0_range: tuple[tuple[float, float], ...]
    stress_post: tuple[float, float, float]; F_t: float; F_base_rate: float; F_ab: tuple[float, float]
    e0: tuple[float, float, float, float]; z0: tuple[float, ...]; z_disagreement: bool
    oil: OilState; gw_elapsed_months: int
    draw_12m_bn: tuple[float, float]; draw_p90_bn: float; d_prev: float
    factor_levels0: dict[str, float]             # t0 levels of every LEVEL-kind factor (rates, spreads, log RV, ...)
    filter_version_hash: str; content_hash: str
class PanelRow(BaseModel): index: int; light: str; metric_id: MetricId; status: CFPStage | Literal["INFO"]; policy_link: str
class StatePanel(BaseModel): rows: tuple[PanelRow, ...]   # exactly 12 (gap_04 §8)
```

### 3.7 Path cubes and trees (`contracts/arrays.py`, `contracts/world.py`)

```python
class CubeMeta(BaseModel):
    world_id: WorldId; plane: Plane; base_entropy_hex: str; generator_hash: str; asof: date
    n_paths: int; path_offset: int; months: int = 120; factor_names: tuple[str, ...]; factor_kinds: tuple[FactorKind, ...]
    proxy_factors: tuple[str, ...] = ()          # B1/B2 factors filled from E's conditional model (labelled PROXY in claims)
    asset_names: tuple[str, ...]
    vol_names: tuple[str, ...] = ("log_vix30", "log_move", "ovx"); is_synthetic: bool; data_class: DataClass; checksum: str

@dataclass(frozen=True, slots=True)
class ScenarioCube(ArrayContainer):
    meta: CubeMeta
    factors: F32          # [P, M, K]  monthly log returns / decimal changes
    regimes: I8           # [P, M, 3]  (MacroRegime, ExitWindow, ShockType) in month period m
    stress_post: F32      # [P, M, 3]  stress-filter posterior after month m (state.simulate_filter)
    vol: F32              # [P, M, V]
    fin_window: I8        # [P, M]     FinWindow (S-ADR-12)
    crowding_index: F32   # [P, M]     exogenous forced-selling index from sec_discount and hy_spread (S-ADR-13)
    asset_returns: F32    # [P, M, A]  monthly log returns per asset class
    brent: F32            # [P, M]     USD/bbl at month end
    draw_rate: F32 | None = None      # [P, Y]  attached by owner.attach_draws (Y = 11)
    draw_override: B | None = None    # [P, Y]
    group_rates: "GroupRates | None" = None   # attached by core.sim.record_group_rates (tree building only)
```

Path index stored in the RNG counter is `path_offset + local index`, so a 2,000-path block regenerates identically wherever it runs.

```python
@dataclass(frozen=True, slots=True)
class GroupRates(ArrayContainer):        # recorded under HOLD + plan pacing over the tree's 12 quarters (Q = 12); private groups × age
    meta: GroupRatesMeta                 # contracts (§3.18): groups, age_buckets, policy_ref, cube checksum, rate_kind = "simple"
    delta: F32      # [P, Q, Gp, 2]  distributions ÷ opening economic NAV, per quarter
    qcall: F32      # [P, Q, Gp, 2]  calls ÷ opening unfunded, per quarter
    ret_simple: F32 # [P, Q, Gp, 2]  economic NAV SIMPLE return per quarter, e^r − 1 (H's NAV rows are linear in simple returns)
    bid: F32        # [P, Q, Gp, 2]  cash-equivalent secondary bid ÷ economic NAV
    income: F32     # [P, Q, Gp, 2]  contractual cash income ÷ NAV (credit, Capital Solutions; RA on gross value, before asset-debt service)
    u_per_nav: F32  # [P, Q, Gp, 2]  unfunded per $ of economic NAV (κ^U; the buyer assumes it on a sale)
    nav_share: F32  # [P, Q, Gp, 2]  bucket share of the group's economic NAV (ω; default age split of group sales)
    call_stress_12m: F32  # [P, Q, Gp, 2]  stressed 12-month call rate on unfunded (H3 required outflows)
    lo_ret: F32; hf_ret: F32          # [P, Q]  simple returns
    hf_phi: F32     # [P, Q, 4]   lookup of pub.phi_table by the path's regime at quarter start (3/6/12/24 months; no nested simulation)
    vm_per_beta: F32                  # [P, Q]  VM per $1 of synthetic-beta notional
    cash_rate: F32; fac_rate: F32     # [P, Q]  per quarter
    ra_debt_rate: F32; ra_amort: F32; ra_direct_share: F32   # [P, Q]  RA asset-debt cost and amortization per quarter; directs' share of RA value
    tail_prem_rate: F32; tail_value: F32; opp_pnl_rate: F32; delta_im_rate: F32   # [P, Q]  overlay per-unit coefficients (OverlayStressCoeffs basis)
    draw_rate_q: F32                  # [P, Q]  instalment ÷ B_y
    stress_class: I8                  # [P, Q]  StressState of the stress filter at quarter end
    obs: F32        # [P, Q, n_obs]   observable features for tree clustering (TreeSpec.features)

class TreeSpec(BaseModel):
    k1: int = 24; k4: int = 4; fan_leaves: int = 6; fan_ends_q: tuple[int, ...] = (6, 8, 10, 12)
    paths_per_world: int = 2000; worlds: tuple[WorldId, ...]   # no code default: from the contract template (M1, M6 in increment 1;
                                                                # M1–M6 in v1), because M2–M5 have no configs before WP-31 (BUILD-38)
    tail_quantile: float = 0.02; min_tail_leaves_per_world: int = 30
    reducer: Literal["kmeans_observable", "forward_filtration"] = "kmeans_observable"
    features: tuple[str, ...] = ("F_t", "stress_post_crisis", "p_exit_DF", "p_shock_DB_GW_SG", "cum_eq_ret",
                                 "hy_spread", "draw_rate_realized", "override_flag", "pe_dist_rate")
    seed: int = 0

@dataclass(frozen=True, slots=True)
class Tree(ArrayContainer):
    spec: TreeSpec; tree_hash: str; pooled_worlds: tuple[WorldId, ...]
    parent: I32       # [N]  (−1 for root)
    t_end: I16        # [N]  quarter instant at node end (0 for root)
    period_q: I8      # [N]  1 (Q1–Q4) or 2 (fan periods)
    stage: I8         # [N]  0 root; 1–4 quarterly; 5–8 fan
    p: F64            # [N]  Σ_m w_m p_{n|m}
    p_world: F64      # [N, W], W = len(spec.worlds): 6 in v1, 2 (M1, M6) in the MVP
    is_leaf: B        # [N]
    leaf_world: I8    # [N]  world index for leaves, −1 otherwise
    lr_weight: F64    # [N]  likelihood-ratio weights for tail-stratum leaves (1.0 otherwise)
    member_ptr: I32   # [N + 1]  CSR pointers into member_idx
    member_idx: I32   # [nnz]    pooled path indices
    coef: "NodeCoefficients"   # the GroupRates fields aggregated per node: [N, ...]
    obs_centroid: F64 # [N, n_obs]
    regime_class: I8  # [N]  StressState of the node centroid
```

Default sizes (v2): N = 1 + 24 + 24 + 24 + 96 + 576 × 4 = **2,473 nodes**, **576 leaves**, 8 periods. Node coefficients are probability-weighted means over member paths for linear quantities and the medoid path's values for nonlinear ones (ARCH §5.4). Coefficients of a two-quarter fan period are compounded from its quarters on each member path before averaging: intensities 1 − (1 − q₁)(1 − q₂), returns and cash rates (1 + r₁)(1 + r₂) − 1, distributions and income measured on the in-period NAV path, so they are exact for HOLD (S-ADR-33).

### 3.8 Engine I/O (`contracts/engine_io.py`)

```python
class NoiseRequest(BaseModel):
    source: str                         # e.g. "priv.fund.idio", "priv.company.ev", "pub.hf.gate", "sale.success"
    slots: int                          # uniforms per (path, month, entity)
    entity_ids: tuple[str, ...] | None  # None -> one stream with entity_key 0
    months: tuple[int, ...]             # month periods covered

@dataclass(frozen=True, slots=True)
class NoiseSlice(ArrayContainer):
    requests: tuple[NoiseRequest, ...]
    u: dict[str, F64]                   # u[source]: [P, n_months, n_entities, slots], uniforms in [0, 1)

@dataclass(frozen=True, slots=True)
class WorldSlice(ArrayContainer):
    clock: Clock; t: int; months: tuple[int, ...]
    factors: F32; regimes: I8; stress_post: F32; vol: F32; fin_window: I8; asset_returns: F32; brent: F32   # [P, nm, ...]

@dataclass(slots=True)                  # mutable: the simulator fills it from Policy.act
class ActionSlice(ArrayContainer):
    t: int
    sell_frac: F32          # [P, U]  fraction of current position sold this quarter (discretionary and planned; recourse sales are ledger-decided)
    sell_reason: I8         # [P, U]  SaleReason (reporting label; red status comes from ledger.red_test)
    refi_draw_bn: F32       # [P, U]  cash raised against the unit (REFINANCE)
    add_bn: F32             # [P, U]  exposure added (ADD; LEVER = ADD + refi_draw on the same unit)
    commit_bn: F32          # [P, G]  new commitments this quarter
    contingent_bn: F32      # [P, G]  contingent-budget deployment
    hf_notice_frac: F32     # [P, L]  share of each HF lot noticed (notice dates only)
    sma_runoff: F32         # [P]     ρ ∈ [0, 1], 1 = reinvest, 0 = run off
    p2s_bn: F32; beta_add_bn: F32; tail_notional_bn: F32; opp_scale: F32; monetize_frac: F32   # [P]
    fac_draw_bn: F32; fac_repay_bn: F32     # [P, NF]
    reserve_target: F32     # [P]     HQLA* ÷ W
    recourse_order: I8      # [P, 6]  permutation of the rungs reserve, p2s, liquid, facility, amber, red (S-ADR-13; no preemptive rung)
    preemptive_raise_bn: F32  # [P]   executed at quarter start, outside recourse_cover; red-tested by substance (S-ADR-30)

@dataclass(frozen=True, slots=True)
class FlowSlice(ArrayContainer):
    engine_id: str; clock: Clock; t: int
    by_group: F32           # [P, G, F]   signed $bn, EXTERNAL counterparty only
    intra: F32              # [P, G, F]   INTRA_ADIC flows; Σ over groups == 0 (1e-9)
    by_unit: F32 | None     # [P, U_e, F] when keep_units=True
    recourse_unit_ids: tuple[UnitId, ...]   # this engine's recourse-eligible units (red and amber tiers, long-only, HF lots)
    by_recourse_unit: F32   # [P, U_r, F] always emitted: the ledger scales a sold fraction out of the remaining intra-quarter flows
    nav_econ: F32; nav_rep: F32; unfunded: F32; encumbered: F32   # [P, U_e] stocks at period end
    hqla_contrib_bn: F32    # [P]         treasury and public sleeves only
    # v1.0's sale_red field is deleted: red sales are ledger facts (RecourseOutcome + ledger.red_test; S-ADR-29/30)

@dataclass(slots=True)
class UnitFinancing(ArrayContainer):    # per-unit debt created by REFINANCE/LEVER, owned by the engine that owns the unit (BUILD-24)
    unit_ids: tuple[UnitId, ...]; instrument_ids: tuple[str, ...]
    balance_bn: F64         # [P, U_f]
    rate_q: F64; amort_q: F64; ltv_covenant: F64   # [U_f]  per-quarter cost and amortization; covenant LTV on reported NAV
    breached: B             # [P, U_f]  forced paydown triggered this quarter
    # emits DEBT_DRAW / DEBT_SERVICE / DEBT_REPAY flows; the ledger adds balances to look-through leverage

class EngineState:                      # base class; subclasses hold numpy arrays, mutated in place by step() and apply_recourse()
    unit_ids: tuple[UnitId, ...]
    financing: UnitFinancing | None
    def stocks(self) -> tuple[F32, F32, F32]: ...   # nav_econ, nav_rep, unfunded  [P, U_e]

class FlowCubeMeta(BaseModel):
    unit_ids: tuple[UnitId, ...]; group_of: tuple[GroupId, ...]; quarters: int = 40
    cube_checksum: str; action: "LensAction | None" = None    # set for column flows (Δ vs HOLD on CRN)
@dataclass(frozen=True, slots=True)
class FlowCube(ArrayContainer):
    meta: FlowCubeMeta
    values: F32             # [P, Q, U, 18] signed $bn per quarter; at most one 2,000-path block
    # column cubes (meta.action set) carry only the affected units, U = 1–3; full-book cubes are stored per unit kind's
    # flow-type subset and materialized only on request (one full 600-unit float32 block would be ≈3.5 GB; S-ADR-38)
```

### 3.9 Ledger contracts (`contracts/ledger.py`)

```python
@dataclass(slots=True)
class LedgerState(ArrayContainer):      # one path block; instant m
    m: int; fy: int
    hqla_unenc_bn: F64      # [P] unencumbered, haircut HQLA under CF control
    treasury_bn: F64        # [P, 3] cash, UST, IG (market value)
    posted_im_bn: F64; vm_balance_bn: F64; vm_in_transit_bn: F64          # [P]
    fac_drawn_bn: F64; fac_limit_bn: F64                                  # [P, NF]
    asset_debt_bn: F64      # [P] RA non-recourse (look-through only)
    unit_debt_bn: F64       # [P] Σ UnitFinancing balances reported by engines (look-through leverage; BUILD-24)
    encumbrance_bn: F64; nav_econ_bn: F64; nav_rep_bn: F64; liquid_bn: F64   # [P]
    nav_group_econ: F64; nav_group_rep: F64; unfunded_group: F64          # [P, G]
    draw_basis_bn: F64; draw_rate: F64; payout_ytd_bn: F64                # [P]
    twr_index: F64; twr_peak: F64; cushion: F64                           # [P]
    readiness: I8; event: I8; planning: I8; playbook: I8                  # [P] CFPStage
    event_hist: I8          # [P, 2] last two event readings (hysteresis)
    red_event: B; payout_short: B; failed: B                              # [P]
    red_month: I16          # [P] first red month, −1 if none

@dataclass(frozen=True, slots=True)
class LedgerPaths(ArrayContainer):
    row_keys: tuple[RowKey, ...]
    rows: F32               # [P, M + 1, R] row slacks at monthly instants ($bn; ≥ 0 means satisfied)
    stages: I8              # [P, M + 1, 4] readiness, event, planning, playbook

class OverlayStressConvention(BaseModel):
    beta_notional_bn: float = 10.0; im_from: float = 0.04; im_to: float = 0.10
    tail_monetization: bool = True
    opp_loss: Literal["ov2_consistent", "pct_nav"] = "ov2_consistent"   # S-ADR-32: OV2 cap × tail payoff in the stress
    opp_loss_pct_nav: float = 0.015                    # used only by the research ("as ratified") sensitivity set

class RAStressConvention(BaseModel):                   # S-ADR-32; replaces the PE distribution multiplier for Real Assets
    noi_yield_mult: float; development_calls: bool = True; refinancing_wall: bool = True
    refi_spread_stress_a: float; refi_ltv_cap: float   # values [I] in config/ledger/t4prime_canonical_v1.yaml

class CanonicalConventions(BaseModel):       # hashed contract fields (ARCH §4.9 table); defaults are the lab's consistent set
    draw_basis: Literal["opening_fy_reported_nav", "fixed_usd", "current_nav"] = "opening_fy_reported_nav"
    draw_rate_in_stress: float = 0.10; draw_years_capped: int = 2
    revolver_credit: float = 0.50; revolver_from_month: int = 2   # s* is the joint oil–crisis state (S-ADR-12/32); 0.80 in the research set
    nav_facility_ltv_stressed: float = 0.05; pledge_pool_cap: float = 0.20
    ig_target: float = 0.08; ig_hard: float = 0.04; ig_restore_quarters: int = 4
    credit_cash_a: dict[GroupId, float]                # no code default: PRIVCREDIT 0.10, CAPSOL 0.07 live in config (group-id lint)
    hf_whole_book_noticed: bool = True; hf_pass_through: float = 0.83
    new_commitments_bn_a: float = 12.0; commitment_split: dict[GroupId, float]
    overlay: OverlayStressConvention = OverlayStressConvention()
    real_assets: RAStressConvention
    shock_timing: Literal["vertex_t0"] = "vertex_t0"
    pacing_credit_lag_q: int = 2                       # S-ADR-20/32; 0 only in the ported research fixtures

class ConventionSets(BaseModel):                       # what prices and what prints as a sensitivity until A1 (S-ADR-32)
    pricing: CanonicalConventions                      # the internally consistent set (defaults above)
    research: CanonicalConventions                     # "as ratified" research set: revolver 0.80, opp loss 1.5% NAV, lag 0, RA via dist_mult

class StressSpec(BaseModel):
    name: str; theta: float; months: int = 24
    equity_shock: float          # −(0.30 + 0.10 θ)
    dist_mult: float             # 0.45 (1 − θ) × drought rates, groups with fund_distribution_stress (PE, SEC, CO); never RA
    call_mult: float             # 1 + 0.5 θ
    base_call_rate_a: float = 0.28
    conventions: CanonicalConventions
    role: Literal["pricing", "reverse"]          # reverse stresses never price (PricingRefused)
    @classmethod
    def s_star(cls, theta: float, conv: CanonicalConventions) -> "StressSpec": ...

@dataclass(frozen=True, slots=True)
class StressReport(ArrayContainer):
    spec_hash: str
    headroom_bn: F64        # [P, 24]  hd_h on T + P + F (facility-inclusive)
    nco_bn: F64             # [P, 24]
    cbc_bn: dict[RecourseTier, F64]       # each [P, 24]
    survival_months: dict[RecourseTier, I16]   # each [P]; 25 means "> 24"; APPETITE reads survival_months[TP] ≥ 24 (no facilities)
    gap_bn: F64             # [P]  G* = max_h [NCO(h) + 0.04 W(h) − CBC_TP(h)]
    d0_bn: F64              # [P]  max(0, −min_h hd_h)

class CFPReading(BaseModel):
    readiness: CFPStage; event: CFPStage; planning: CFPStage; playbook: CFPStage
    indicators: dict[Literal["sh_tp_months", "lcr30", "treasury_share", "liquid_share", "lar99_over_cbc"], float]
    triggers: tuple[str, ...]
    # validator (ARCH §4.9 invariant): playbook in {RED, BLACK} only if event >= RED
```

### 3.10 Beliefs and bridge (`contracts/beliefs.py`)

```python
class BeliefMeta(BaseModel):
    asof: date; fbe_version: str; prior_hash: str; inputs_hash: str
    frozen_optimizer_outputs_hash: str          # previous quarter's SELL flags and envelope status (acyclic; JE §5.3)
    data_class: DataClass; content_hash: str

@dataclass(frozen=True, slots=True)
class BeliefSet(ArrayContainer):
    meta: BeliefMeta; unit_ids: tuple[UnitId, ...]
    alpha_a: F64            # [U] fused forward log return in EXCESS of the unit's benchmark at the as-of, a year, net (S-ADR-28)
    benchmark_id: tuple[str, ...]   # [U] CMA asset class of the unit's benchmark (scen.asset_class_map)
    beta_hat: F64           # [U] beta to the benchmark's market factor at the as-of
    bench_ref_a: F64        # [U] benchmark expected log return used in the decomposition: r_f + β̂·ERP_ref (mixture CMA, as-of)
    mu_total_a: F64         # [U] = bench_ref_a + alpha_a; display, cards and Tier-1 views only, never fed to an engine
    sigma_hat: F64          # [U]
    band80: F64             # [U, 2]  on mu_total_a
    mu_p10: F64             # [U] Tier-1 view: posterior P10 of mu_total_a with group bias at +2 sd
    weights: F64            # [U, 4] fusion weights on (f, u, a, m); 0 where absent
    market_anchor: F64; has_market: B          # [U]
    nowcast_nav_bn: F64     # [U]
    flags: U32              # [U] bitmask: F1..F10 = bits 0–9, ZOMBIE = 10, CATALYST_MISSING = 11
    p_achieved: F64         # [U, 2] P(forecast achieved within 4, 8 quarters)
    group_bias_mean: F64; group_bias_sd: F64; kappa: F64       # [G]
    info_value_usd_m: F64 | None = None        # [G] information value of each group's forecast (W2)
    # validators: mu_total_a == bench_ref_a + alpha_a (1e-12); band80[:,0] < mu_total_a < band80[:,1]

@dataclass(frozen=True, slots=True)
class BeliefDraws(ArrayContainer):               # produced by beliefs.draw_paths per world and block; consumed via AssetEngine.init
    world_id: WorldId; path_offset: int; unit_ids: tuple[UnitId, ...]; gp_ids: tuple[SponsorId, ...]
    alpha0_q: F32           # [P, U]   initial per-path α per quarter = posterior draw + group bias + GP effect, shifted to the
                            #          world's CMA-line basis (bridge double-counting guard: selection/fee/leverage conventions)
    group_bias_q: F32       # [P, G]   shared group-bias shock per quarter (reported separately for attribution)
    gp_effect_q: F32        # [P, n_gp] shared GP effect per quarter (one draw per GP per path; V24d)
    m_q: F64; phi: F64; eta_sd_q: F64   # [U]  learning: α_{t+1} = m + φ(α_t − m) + η_t
    # invariant: draws frozen at α̂ (eta_sd = 0, bias = 0) reproduce the no-learning variant exactly

class UnitBelief(BaseModel):                    # card view
    unit_id: UnitId; raw: dict[MarkType, float | None]; fused_mu_a: float; alpha_a: float; benchmark_id: str
    sigma_a: float; band80: tuple[float, float]
    market_anchor_a: float | None; flags: tuple[str, ...]; p_achieved_4q: float; p_achieved_8q: float
    weights: dict[MarkType, float]

class LeverLine(BaseModel): name: str; weight: float; alpha_star_a: float; sd_a: float; benchmark: str
class BridgeCard(BaseModel):
    world_id: WorldId; beta_return_a: float; levers: tuple[LeverLine, ...]; overlay_sr: float; overlay_sigma_a: float
    leverage: float; drags: dict[str, float]; arith_mean_a: float; geom_mean_a: float
    gap_to_target_pp: float; p_mu_ge_target: tuple[float, float]   # (independent, comonotone levers)
    p_10y_ge_target: float; break_evens: dict[str, float]
    verdict: Literal["Plan", "Stretch", "Aspiration"]; data_class: DataClass
```

### 3.11 Policies (`contracts/policy.py`)

```python
class PolicyRef(BaseModel):
    kind: Literal["native", "spec"]
    name: str          # native: HOLD, STATIC_SAA, DECK_RULES, TARGET_CHASING, PLACEBO, PRO_RATA, OVERLAY_ONLY,
                       #         LIQUID_FIRST, CASH_LAST, ARCH_A, ARCH_B, ARCH_C, P0, C_H
    params_hash: str; spec_hash: str | None = None

class FeatureExpr(BaseModel):
    var: str                                     # registry variable (config/core/dsl_variables.yaml)
    lag: int                                     # quarters; >= registry minimum (TR1)
    xforms: tuple[Literal["logit", "zscore_frozen", "diff", "min", "max", "hinge"], ...] = ()
    xform_args: tuple[float, ...] = ()

class ResidualSpec(BaseModel):
    slot: str                                    # reserve_target | pacing_mult[g] | econ_leverage | tail_hedge_ratio | opp_budget
                                                 # | sell_screen[g] | refi_hurdle[g] | hf_notice_share | p2s_share | recourse_order
                                                 # | preemptive_raise | payout_topup (Mode A/H only, TR8)
    form: Literal["mult_tanh", "add_clip", "switch_hyst"]
    rho: float | None = None; lo: float | None = None; hi: float | None = None; on: float | None = None; off: float | None = None
    features: tuple[FeatureExpr, ...]            # 1..3
    box: tuple[tuple[float, float], ...]         # one box per weight; must contain 0 (TR5)
    gate_id: str

class PackageItem(BaseModel):
    target: HoldingId | GroupId; lens: Lens; instrument: str
    size_bn: float | None = None; size_frac: float | None = None
    trigger: FeatureExpr | None = None; window_q: int = 1
class ActionPackage(BaseModel): items: tuple[PackageItem, ...]           # <= 12, <= 1 lens per asset per quarter
class OverlayLeg(BaseModel):    template: str; strike_rel: float | None; expiry_months: int; notional_bn: float; side: Literal["long", "short"]
class OverlayStructure(BaseModel): template: str; legs: tuple[OverlayLeg, ...]; sleeve: Book
                                   monetization_trigger: FeatureExpr | None = None

class PolicySpec(BaseModel):
    anchor: str                                  # "P0@sha256:..."
    residuals: tuple[ResidualSpec, ...] = ()     # 0..6
    packages: tuple[ActionPackage, ...] = ()     # 0..3
    overlays: tuple[OverlayStructure, ...] = ()  # 0..3
    mandate_mode: MandateMode = MandateMode.B_OWNER_CALL
    @computed_field
    def spec_hash(self) -> str: ...

class RecourseOrder(BaseModel):
    rungs: tuple[Literal["reserve", "p2s", "liquid", "facility", "amber", "red"], ...]   # no "preemptive" rung (S-ADR-30)
    switch_on: Literal["planning_stage", "drought"] | None = None
    alt_rungs: tuple[str, ...] | None = None; switch_threshold: float | None = None
    crowding_haircut_coef: float = 0.0           # discount per unit of ScenarioCube.crowding_index (S-ADR-13)

@dataclass(frozen=True, slots=True)
class Observables(ArrayContainer):
    t: int
    values: dict[str, F32]                       # DSL variables already lagged, each [P]
    unit_values: dict[str, F32]                  # per-unit observables, each [P, U]: bid_ce, reservation_price, rho_hat (lagged per registry)
    group_values: dict[str, F32]                 # per-group observables, each [P, G]: envelope use, unfunded share, pacing multiplier
    world_hidden: Literal[True] = True           # marker: no world id, path id, horizon or budget is present (TR2)
```

### 3.12 Optimizer contracts (`contracts/optimizer.py`)

```python
class RowKey(BaseModel):
    family: RowFamily; idx: tuple[tuple[str, str | int], ...] = ()
    def __str__(self) -> str: ...                 # "T4P:h=07", "LR4:g=PE:h=24", "TRANSITION:s=C:n=113"
    @classmethod
    def parse(cls, s: str) -> "RowKey": ...
class ColKey(BaseModel):
    family: Literal["state", "decision", "lens", "aux", "elastic"]; name: str; node: int | None = None
    idx: tuple[tuple[str, str | int], ...] = ()

class LPMeta(BaseModel):
    tree_hash: str; contract_hash: str; catalogue_hash: str; ledger_hash: str; builder_version: str
    consent_scenario: ConsentScenario; pricing_level: Literal["tolerance", "appetite"]; replication: int

@dataclass(frozen=True, slots=True)
class LPModel(ArrayContainer):
    name: str; meta: LPMeta
    c: F64                    # [n]  objective coefficients; sense is always MAXIMIZE
    A: "scipy.sparse.csc_array"   # [m, n]
    row_lo: F64; row_hi: F64  # [m]  (−inf / +inf allowed)
    col_lo: F64; col_hi: F64  # [n]
    integrality: I8 | None    # [n]  Level B only
    row_keys: tuple[RowKey, ...]; col_keys: tuple[ColKey, ...]
    row_role: I8              # [m]  RowRole
    row_tier: I8              # [m]  Phase-I tier (0 = not tiered)
    node_of_row: I32; node_of_col: I32
    scale_bn: float           # W₀ in $bn (177.0 at the SYNTHETIC as-of)

class RowTier(BaseModel): tier: int; name: str; families: tuple[RowFamily, ...]; weight: float = 1.0
class Lever(BaseModel):
    lever_id: str; owner_group: GroupId; reversible: bool; consent_scenario: ConsentScenario
    cap_bn: float; cost: float                    # PV cost per $bn used
    slope: tuple[float, ...]                      # 24 values: month-h T4′ headroom relief per $bn
    ig_effect: float = 0.0; lag_q: int = 0; shares_sleeve_with: str | None = None
class LeverSet(BaseModel):
    levers: tuple[Lever, ...]
    def available(self, scenario: ConsentScenario) -> tuple[Lever, ...]: ...

class TierResult(BaseModel):
    tier: int; u_star_bn: float; violations_bn: dict[str, float]; iis: tuple[str, ...]
    farkas_ray_ref: ArtifactRef | None; levers_at_cap: tuple[str, ...]; solver: "SolverRecord"
class Phase1Result(BaseModel):
    by_scenario: dict[ConsentScenario, tuple[TierResult, ...]]
    d0_bn: float; mode: ContractMode; pricing_scenario: ConsentScenario
    infeasibility_prices: dict[str, float]        # Treasurer panel only; never on cards, envelopes or FTP
    recovery_hash: str | None
class GlidePath(BaseModel):
    kind: Literal["none", "execution", "structural"]; t_rec_q: int = 4
    d0_bn: float = 0.0; u_star_by_row: dict[str, float] = {}
    g_bn: tuple[float, ...]                       # per quarter t = 0..T_rec: g_t = d0 (1 − t/T_rec)+
    phi_g: dict[GroupId, tuple[float, ...]] = {}  # delivery shares per quarter (ARCH §6.4)
    recovery_hash: str
class RecoveryPlan(BaseModel):
    mode: ContractMode; u_star_bn: float; d0_bn: float; iis: tuple[str, ...]; glide: GlidePath
    board_signoff_required: bool; owner_signoff_required: bool

class DualQuality(BaseModel):
    one_sided: tuple[float, float]; at_kink: bool; ranging: tuple[float, float]
    band: tuple[float, float, float]              # min, median, max across SAA replications
    sign_flip: bool; pinned: bool
    method: Literal["ranging", "parametric_step", "finite_difference"]   # FD only on the capped set of ≤ 10 rows (S-ADR-38)
@dataclass(frozen=True, slots=True)
class DualSet(ArrayContainer):
    pi_row: F64        # [m]  normalized shadow prices (§5.8): ≥ 0 for binding ≥-resource rows
    mu_cash: F64       # [N]  value of an exogenous $ (W₀ unit) of cash at node n
    M_cash: F64        # [N]  dual mass of PRICING liquidity rows containing C_n
    ell: F64           # [N]  ℓ_n = M_n / (μ_n − M_n), per period
    quality: dict[str, DualQuality]               # keyed by str(RowKey), PRICING rows shown on cards

@dataclass(frozen=True, slots=True)
class HSolution(ArrayContainer):
    meta: LPMeta; status: str; objective: float; x: F64; duals: DualSet
    root_values: dict[str, float]                 # str(ColKey) -> value, root decisions and lens columns
    marginal_utility_wealth: float                # ū′ = Σ_ℓ p_ℓ ∂obj/∂W̃_ℓ at the solution (CE conversion, §5.11)
    priced_on: PricedOn; consent_scenario: ConsentScenario; pricing_level: Literal["tolerance", "appetite"]
    recovery_hash: str | None; replication: int; solver: "SolverRecord"
    resolve_counts: dict[Literal["selection", "finite_difference", "parametric", "forced"], int] = {}   # logged in the manifest
    exact_objective: float | None = None          # exact CRRA/shortfall at the solution's leaf wealth (A8; Γ and ε_mat use it)

class Kernel(BaseModel):
    pi: tuple[float, ...]; ell: tuple[float, ...]; deflator: tuple[float, ...]; esscher_gamma: float
    lambda_spot: dict[StressState, float]; one_off_premium: float; priced_on: PricedOn; recovery_hash: str | None
class FTPPoint(BaseModel):
    tenor_q: int; decision_q: float; published_q: float; band_q: tuple[float, float]
    components: dict[RowFamily, float]            # λ decomposition by binding row (S-ADR-16)
    fin_window: FinWindow | None = None; priced_on: PricedOn; recovery_hash: str | None
class FTPCurves(BaseModel):
    asof: date; tolerance: tuple[FTPPoint, ...]; appetite: tuple[FTPPoint, ...] | None
    ewma_halflife_q: int = 2; collar: float = 0.5
class Envelope(BaseModel):
    group: GroupId; row: str; value_bn: float; range_bn: tuple[float, float]; dual: float
    ranging_bn: tuple[float, float]; elasticity_bn_per_100bp: float; delivery_share: float | None
    priced_on: PricedOn; recovery_hash: str | None
class EnvelopeSet(BaseModel):
    envelopes: tuple[Envelope, ...]; pool_bn: dict[str, float]; slack_bn: dict[str, float]
    risk_haircut: float = 0.10                    # S-ADR-16

class Column(BaseModel):
    col_id: str; unit_id: UnitId | None; group: GroupId; action: "LensAction"
    node_coeffs_ref: ArtifactRef                  # sparse vector keyed by str(RowKey), not row number, so columns can be built
                                                  # before H is assembled; core.h.row_index(lp) maps keys to rows at pricing time
    cost: float; consent_p: float; lag_q: int; min_ticket_bn: float; irreversible: bool
    t6_consuming: bool = False                    # red-tier SELL in a state that meets ledger.red_test (ii)/(iii): bound 0 in Phase II
class ColumnPool(BaseModel): columns: tuple[Column, ...]; tree_hash: str
class Selection(BaseModel):
    chosen: tuple[str, ...]; x: dict[str, float]; split_assets: tuple[UnitId, ...]   # marginal-asset agenda
    gamma_bp: float; gamma_bp_exact: float; certified: bool; iterations: int   # Γ judged on exact utility (A8)
    forced_resolve_flags: dict[str, bool]; calibration_capped: bool = False    # S-ADR-44
class WhatChanged(BaseModel): field: str; before: float; after: float; reason_row: str
class SafeAction(BaseModel):
    action: "ActionProposal"; changed: tuple[WhatChanged, ...]; binding_rows: tuple[str, ...]
    projected: bool; tier1_override_needed: bool; exact_recheck_passed: bool
class ActionProposal(BaseModel):          # ARCH §3.5 calls this type `ActionSet`; `ActionSet = ActionProposal` is exported as an alias
    source: Literal["optimizer", "agent", "ic_amendment", "archetype", "standing_policy"]
    root_values: dict[str, float]; lens_actions: tuple["LensAction", ...]
```

### 3.13 Actions and cards (`contracts/actions.py`)

```python
class LensAction(BaseModel):
    unit_id: UnitId | None; group: GroupId; lens: Lens; instrument: str
    size_bn: float; exposure_delta_bn: float; financing_delta_bn: float; cash_out_bn: float
    # validators (JE-MF9): SELL ⇒ exposure_delta < 0; HOLD ⇒ both deltas 0;
    #   REFINANCE ⇒ exposure_delta == 0 ∧ financing_delta > 0 ∧ cash_out > 0;
    #   ADD ⇒ exposure_delta > 0 ∧ financing_delta == 0; LEVER ⇒ exposure_delta > 0 ∧ financing_delta > 0;
    #   PACE ⇒ unit_id is None
class InstrumentSpec(BaseModel):
    instrument_id: str; group: GroupId; lens: Lens; description: str; price_model: str
    availability: dict[MacroRegime, float]; fin_window_mult: dict[FinWindow, float]
    lag_q: int; consent_required: bool; external_only: Literal[True] = True; params: dict[str, float]
class ActionCatalogue(BaseModel):
    instruments: tuple[InstrumentSpec, ...]; columns: ColumnPool
    overlay_stress_ref: ArtifactRef                # NV^eq and P&L per named stress per overlay column (OV1/OV2 rows)
    hash: str
class FlipThresholds(BaseModel):
    reservation_price: float | None; breakeven_fwd_return_a: float | None
    breakeven_ell_a: float | None; one_off_premium: float | None
    lever_breakeven_financing_a: float | None = None   # LEVER flips where α* − risk charge = all-in financing cost (ADR-49)
class WaterfallItem(BaseModel): label: str; value_usd_m: float
class BeliefCard(BaseModel):
    raw_marks: dict[MarkType, float | None]; fused_mu_a: float; sigma_a: float; band80: tuple[float, float]
    market_anchor_a: float | None; flags: tuple[str, ...]; zombie: bool
    catalyst_status: Literal["ok", "missing", "overdue", "n/a"]; p_achieved_4q: float; p_achieved_8q: float
    info_value_usd_m: float | None
class DecisionCard(BaseModel):
    card_id: str; unit_id: UnitId | None; group: GroupId; asof: date; action: LensAction
    reduced_cost_bp: float; dual_interval_bp: tuple[float, float]; at_kink: bool; value_usd_m: float
    p_best: float; regret_bp: tuple[float, float]; lapv_waterfall: tuple[WaterfallItem, ...]
    flips: FlipThresholds; belief: BeliefCard; consents: tuple[str, ...]; rofr: bool
    envelope_use_bn: float; alpha_star_a: float; drag_a: float
    priced_on: PricedOn; consent_scenario: ConsentScenario; recovery_hash: str | None
    gamma_status: Literal["certified", "selection_not_certified"]
    consent_sensitive: bool; second_order_material: bool; tree_sensitive: bool; hp_rank_flag: bool
    t6_consuming: bool                           # "counts as a T6 red event in the current state" (S-ADR-30)
    lever_legs: tuple[WaterfallItem, ...] | None = None   # ADD and REFI legs of a LEVER, shown separately (ADR-49)
    binding_rows: tuple[str, ...]; shadow_prices: dict[str, tuple[float, float, float]]   # value, one-sided lo, hi
    plane: EvidencePlane; run_ref: ArtifactRef; data_class: DataClass
```

### 3.14 Contract and governance (`contracts/contract.py`)

```python
class SignOff(BaseModel):
    role: Literal["CIO", "CRO", "TREASURER", "BOARD", "OWNER", "SECRETARY"]; signer_hash: str
    signed_at: datetime; object_hash: str; method: Literal["ed25519_dpapi", "hardware_token", "dev_test_key"]
    signature: str                               # Ed25519 over canonical_json({object_hash, role, signer_hash, signed_at}) (S-ADR-40)
    # created only by tpa room/seal sign commands under an authenticated Windows account; no agent tool returns SignOff;
    # verified by contracts.signing.verify against config/room/signers_roster.yaml; dev_test_key is refused in REAL mode

class ObjectiveSpec(BaseModel):
    gamma: float = 3.0; lambda_T: float = 1.0; shortfall_exponent: float = 2.0   # > 1 strictly (S-ADR-06)
    target_annual: float = 0.10; horizon_years: int = 10; accrual: Literal["own_return"] = "own_return"
    target_mode: TargetMode = TargetMode.PRECOMMITTED; target_anchor_date: date; target_anchor_wealth_bn: float
    psi_tau_pp: float = 0.5; model_weights: dict[WorldId, float]          # no code default: set in the contract template (1/6 each
                                                                          # M1–M6, Q8); B1/B2 never enter Ψ_τ (BUILD-38)
    h_utility_tangents: int = 48                 # adaptive: placed by leaf-mass quantiles on the previous solve's leaf-wealth P1–P99
    h_utility_tangents_fallback: int = 32        # B2 fallback ladder, allowed only if the A8 decision test passes (S-ADR-38)
    h_shortfall_breaks: tuple[float, ...] = (0.0, 0.05, 0.10, 0.20, 0.35, 0.50)
    lambda_T_H: float = 1.0                                               # tuned by core.mpc.calibrate_buffers (S-ADR-44)
class Tier1Spec(BaseModel):
    t6_bands: dict[str, tuple[float | None, float, float]]   # appetite, tolerance, capacity:
                                                              # M1..M5, MIX: (0.005, 0.01, 0.02); M6: (None, 0.025, 0.05)
    t6_window_years: int = 5; t7_limit: float = 0.025; t8_shock_types: tuple[ShockType, ...] = (DB, GW, SG)
    t8_hard: float = 1.0; t8_green: float = 1.25; t9_trigger_12m: float = 0.02; t9_default_life: float = 0.01
    red_discount_max: float = 0.10               # δ_max of the economic-substance red test (S-ADR-30) [I], A1 field
    theta_rule: Literal["class_banded", "prudence_overlay"] = "class_banded"   # S-ADR-32; prudence_overlay = M6 at 1% (legacy)
    theta_star: float                            # no code default: set by ledger.calibrate_theta_star at G0 (B13) and hashed
    theta_star_overlay: float | None = None      # the prudence-overlay value, printed as a sensitivity with its facility ask
    t3_vm_stat: Literal["P99", "CVaR99"] = "P99"; conventions: ConventionSets
    t6_surrogate: T6SurrogateKind = T6SurrogateKind.CVAR_CLASS
    b_red: dict[str, float] = {}; b_floor: dict[WorldId, float] = {}    # CFA buffers from core.mpc.calibrate_buffers; {} means
                                                                         # "last quarter's values", and zero buffers in the first quarter
    t5: dict[str, float]          # recourse_debt_target 0.10, hard 0.15, exposure 1.30, encumbrance 0.15/0.20, pledge 0.20,
                                  # maturity_12m 0.20, lr8 0.80, gross_overlay 0.30
class FloorSpec(BaseModel):                     # S-ADR-31 (replaces v1.0's 5-year rolling windows)
    window_years: int = 10; recertify_each_quarter: bool = True          # forward window [t, t + 40] at every re-solve
    median_10y_min: float = 0.07; median_10y_capacity: float = 0.06      # mixture median: tolerance / capacity [I]
    cvar10_bands: dict[Literal["M1_M5", "MIX", "M6"], tuple[float | None, float, float]] = {
        "M1_M5": (0.01, 0.0, -0.02), "MIX": (0.01, 0.0, -0.02), "M6": (None, -0.025, -0.05)}   # appetite, tolerance, capacity [I]
    misspec_report_only: bool = True             # misspecification worlds: reported, never gating
class ActionSpace(BaseModel):
    lenses_by_group: dict[GroupId, tuple[Lens, ...]]; instrument_whitelist: tuple[str, ...]
    idea_kinds: tuple[Literal["policy_residual", "action_package", "overlay_structure"], ...]; max_lens_per_asset_q: int = 1
class PlaneSpec(BaseModel):
    search_worlds: tuple[WorldId, ...]; final_worlds: tuple[WorldId, ...]; misspec: tuple[str, ...]
    book_variants: tuple[CensusId, ...] = ()     # misspecification members that are another book (S-ADR-43)
    b2_mode: Literal["family_holdout", "out_of_time"] = "family_holdout"   # out_of_time: E, filter and F_t calibrated through 2015
    seal_commitment: str                          # SHA256(salt ‖ contract_hash) written at signing
    windows: dict[str, tuple[date, date]]; embargo_months_bootstrap: int = 12; embargo_months_calibration: int = 3
    paths: dict[Literal["race", "confirm", "final", "tail"], int] = {"race": 2000, "confirm": 10000, "final": 50000, "tail": 250000}
    # evaluation-kind table (§7.7): race = screening; confirm = Gate-1 confirmation of promotion candidates only
class GateSpec(BaseModel):
    eps_ni_bp: float = 5.0; eps_mat_bp: dict[Literal["overlay", "pacing", "refi_lever", "sell", "other"], float]
    lcb_level: float = 0.95; holm: bool = True; pbo_max: float = 0.20; cscv_blocks: int = 8; mde_max_bp: float
    pbo_source: Literal["search_ledger"] = "search_ledger"   # CSCV on the counted search evaluations, never the sealed plane
    ni_worlds_search: tuple[WorldId, ...]; ni_worlds_final: tuple[WorldId, ...]   # {M1..M6, B1} / {M1..M6, B2}; misspec report-only
    ni_comparator: Literal["HOLD", "RESTORED_BASELINE"]; miss_fd_cost_ratio: float; search_t6_factor: float = 0.8
class BudgetSpec(BaseModel):
    cycles: int = 24; cycles_per_worker: int = 12; evals: int = 650; evals_per_attempt: int = 2; tuning_evals: int = 24
    usd_soft: float = 50.0; usd_hard: float = 200.0; core_hours: float = 20.0; alpha_wealth0: float = 0.05
    wall_clock_hours: float = 48.0; validation_retries: int = 3; workers: int = 2           # configurable to 4 (ADR-17)
class RoleLLMSpec(BaseModel):
    role: RoleId; family: ModelFamily; model: str; effort: Literal["low", "medium", "high", "xhigh", "max"]
    max_tokens: int = 16000; prompt_hash: str; tools: tuple[str, ...]; data_classes_allowed: tuple[DataClass, ...]
    materiality: Literal["high", "medium", "low"]; blocking_escalation: bool
class LLMSpec(BaseModel):
    mode: LLMMode; provider: Literal["anthropic", "bedrock", "vertex", "foundry"]; roles: tuple[RoleLLMSpec, ...]
    fallback: Literal["server_default", "client_middleware", "none"] = "server_default"
    holding_level_content_allowed: bool = False   # operator flag (P13)
class RACI(BaseModel): owners: dict[str, str]
class RiskBudget(BaseModel): name: str; t6_eps: float; floor: float; tail_budget_a: float; leverage_max: float
class FrozenQuestion(BaseModel): qid: str; item_id: str; text: str; resolves_by: date; metric_id: MetricId | None = None

class AnalysisContract(BaseModel):              # ARCH §10.1 fields, plus the five marked NEW
    contract_id: ContractId; version: int; quarter: str; data_class: DataClass
    census_id: CensusId | None; purpose: Literal["DECISION", "OWNER_PROPOSAL"] = "DECISION"
    allocation: AllocationId = "v2"                                  # NEW (S-ADR-03)
    census_side_by_side: CensusId | None = None                      # NEW
    mandate_mode: MandateMode = MandateMode.B_OWNER_CALL; owner_signoff: SignOff | None = None
    mode: ContractMode; recovery: RecoveryPlan | None
    pricing_scenario: ConsentScenario; pricing_level: Literal["tolerance", "appetite"] = "tolerance"
    signoffs: tuple[SignOff, ...]; frozen_questions: tuple[FrozenQuestion, ...]
    objective: ObjectiveSpec; tier1: Tier1Spec; floor: FloorSpec; actions: ActionSpace
    anchor: PolicyRef; controls: tuple[PolicyRef, ...]; planes: PlaneSpec; gates: GateSpec; budgets: BudgetSpec
    horizons_q: tuple[int, ...] = (12, 20, 40); operating_points: tuple[RiskBudget, ...]
    llm_policy: LLMSpec; raci: RACI
    root_seed: int                                                   # NEW (S-ADR-25)
    canary_commitment: str | None = None                             # NEW (S-ADR-18)
    run_mode: RunMode                                                # NEW (S-ADR-37)
    engine_hash: str; config_hash: str; snapshot_hash: str; scenario_hashes: dict[str, str]; taxonomy_hash: str
    # validators (ARCH §10.1): owner_signoff required iff mandate_mode != B; purpose == OWNER_PROPOSAL outputs never reach
    # cards/envelopes/FTP; STRUCTURAL_RECOVERY requires a BOARD SignOff; gates.ni_comparator == RESTORED_BASELINE iff mode != NORMAL;
    # pricing_scenario <= highest scenario whose levers carry SignOffs (R1 needs a signed revolver, R2 an owner band agreement);
    # objective.shortfall_exponent > 1; Σ model_weights == 1; tier1.theta_star is set (G0); run_mode == REAL forbids
    # dev_test_key SignOffs, the software seal and the synthetic committee; data_class == REAL forbids run_mode == DEV_SYNTHETIC
```

### 3.15 Evidence and evaluator contracts (`contracts/evidence.py`)

```python
class SolverRecord(BaseModel):
    solver: Literal["highs", "highs_mip", "clarabel", "osqp"]; version: str; algorithm: str
    options: dict[str, str | int | float | bool]; threads: int; status: str; iterations: int; time_s: float
    objective: float; primal_infeas: float; dual_infeas: float; crossover: bool
class LLMCallRecord(BaseModel):
    call_id: str; role: RoleId; requested_model: str; served_model: str; fallback_event: bool
    prompt_hash: str; response_hash: str; input_tokens: int; output_tokens: int; cache_read_tokens: int
    cost_usd: float; stop_reason: str; latency_s: float; replay_key: str
class RunManifest(BaseModel):
    run_id: RunId; kind: str; created_at: datetime; engine_git_sha: str; engine_tree_hash: str; config_hash: str
    contract_hash: str | None; snapshot_hash: str; census_hash: str | None; belief_hash: str | None
    scenario_hashes: dict[str, str]          # "plane:world" -> cube checksum
    seed_spawn: dict[str, str]               # "plane:world" -> base entropy hex, or "HMAC" on the final plane
    plane: Plane; cache_keys: tuple[str, ...]; solver_records: tuple[SolverRecord, ...]
    versions: dict[str, str]; env: dict[str, str]; llm_calls: tuple[str, ...]
    data_class: DataClass; run_mode: RunMode; parent_runs: tuple[RunId, ...] = (); status: Literal["STARTED", "OK", "FAILED", "ABORTED"]
    effective_config_hashes: dict[str, str] = {}   # per module after misspecification overrides (S-ADR-43)
    canonical_artifact_hashes: dict[str, str] = {} # contracts.hashing.canonical_artifact_hash (volatile fields normalized; §9.4 #9)
class MetricDef(BaseModel):
    metric_id: MetricId; description: str; unit: str; aggregation: str
    ci_method: Literal["clopper_pearson", "paired_bootstrap", "mc_se", "none"]
    range_method: Literal["model_min_max", "none"]; icd203: bool; owner_role: str; code_ref: str; code_hash: str
class MetricInstance(BaseModel):
    metric_id: MetricId; run_id: RunId; value: float; unit: str; plane: EvidencePlane
    ci: tuple[float, float] | None = None; model_range: tuple[float, float] | None = None; mc_se: float | None = None
    scenario_hash: str; by: dict[str, str] = {}; data_class: DataClass
class TuningJob(BaseModel): box: dict[str, tuple[float, float]]; max_evals: int = 24; method: Literal["cmaes"] = "cmaes"
class EvalRequest(BaseModel):                # NO fields for metrics, seeds, worlds or path counts (ARCH §10.4)
    request_id: str; campaign_id: CampaignId; attempt_id: str; spec_hash: str
    kind: Literal["evaluate", "tune", "ablation", "price_package", "scenario"]; tuning_job: TuningJob | None = None
class EvalResultAgentView(BaseModel):
    request_id: str; correct: bool
    delta_psi_bucket: Literal["<-10", "-10..-3", "-3..0", "0..3", "3..10", ">10"]     # CE bp a year
    gate_categories: tuple[FailureLabel, ...]; promotable: bool; budget_left: int
class GateOutcome(BaseModel):
    gate: Literal["G1_correct", "G2_selection", "G3_qualification"]; passed: bool; label: GateLabel | None
    failures: tuple[FailureLabel, ...]; details: dict[str, float]
class EvalRecord(BaseModel):                 # full record: humans and the auditor only
    request: EvalRequest; agent_view: EvalResultAgentView; gates: tuple[GateOutcome, ...]
    metrics: dict[MetricId, MetricInstance]; run_id: RunId; counted: bool; cpu_s: float
class Certificate(BaseModel):
    gate: str; world: WorldId; k: int; n: int; p_hat: float; cp_upper: float; band: tuple[float | None, float, float]
    passed: bool; importance_sampled: bool; bpoe: float | None = None
```

### 3.16 Lab, claims and room (`contracts/lab.py`, `claims.py`, `room.py`)

```python
class KeyValue(BaseModel): key: str; value: float | str    # LLM-facing replacement for dict fields (S-ADR-36)
class Interval(BaseModel): lo: float; hi: float              # LLM-facing replacement for fixed-length tuples
class Rubric(BaseModel): kind: Literal["metric", "constraint", "implementation"]; text: str
                         metric_id: MetricId | None = None; threshold: float | None = None
class EffectForecast(BaseModel): metric_id: MetricId; direction: Literal["up", "down"]; size_bp: float; interval_bp: Interval
                                 # a search diagnostic only: never rendered, pooled or compared with engine numbers (S-ADR-36)
class IdeaBundle(BaseModel):                 # paper App. F.2; PB §5.4 (LLM-authored: its PolicySpec boxes use Interval sub-models)
    idea_id: str; title: str; worker: int; cycle: int
    kind: Literal["policy_residual", "action_package", "overlay_structure"]
    hypothesis: str; mechanism_refs: tuple[ArtifactRef, ...]; implementation_plan: tuple[str, ...]
    spec: PolicySpec; target_rubrics: tuple[Rubric, ...]   # >= 1 metric and >= 1 constraint/implementation
    predicted_effect: EffectForecast; assumptions: tuple[str, ...]
class AmendmentDraft(BaseModel): draft_id: str; target_field: str; proposed_value: str; rationale: str; author_role: RoleId
class Escalation(BaseModel):
    escalation_id: str; kind: str; question: str; blocking: bool; proposed_assumption: str | None
    severity: Literal["low", "medium", "high"]; worker: int | None; state: CampaignState; raised_at: datetime
    resolved_by: str | None = None; resolution: str | None = None
class AssumptionEntry(BaseModel): assumption_id: str; text: str; origin: str; tagged_artifacts: tuple[ArtifactRef, ...]
class MemoryEvent(BaseModel): worker: int; cycle: int; kind: Literal["event", "conclusion_update"]; text: str; reason: str | None

PLACEHOLDER_RE = r"\{\{m:(?P<metric>[a-z0-9_.@:-]+)\|(?P<fmt>pct|pp|bp|usd_bn|usd_m|x|months|int|prob|ratio)\}\}"
class ValidationError_(BaseModel):
    code: Literal["LITERAL_DIGIT", "UNKNOWN_METRIC", "WRONG_PLANE", "IMPROVEMENT_VERB_UNQUALIFIED", "PROB_WITHOUT_RANGE",
                  "CITES_MEMORY", "SYNTHETIC_AS_ADIC", "LOW_COVERAGE", "LEAGUE_TABLE", "NAMED_PERSON_REGRET",
                  "BLUEPRINT_FIGURE", "MISSING_P14_FIELD",
                  "LLM_NUMBER_RENDERED",      # an LLM-originated numeric field reached a rendered or aggregated output (S-ADR-36)
                  "UNFETCHED_REF"]            # analyst answer cites a reference not fetched in this turn under its context (S-ADR-34)
    span: tuple[int, int]; detail: str
class ValidationReport(BaseModel): passed: bool; coverage: float; errors: tuple[ValidationError_, ...]
class ClaimRecord(BaseModel):
    claim_id: str; doc_id: str; sentence_index: int; placeholders: tuple[MetricId, ...]; verbs: tuple[str, ...]
    supports_verdict: Literal["supports", "partial", "not_supported", "unaudited"] = "unaudited"
    auditor_family: ModelFamily | None = None; human_countersign: SignOff | None = None
class RenderedDocument(BaseModel):           # assembled by claims.render; never an LLM output model
    doc_id: str; kind: Literal["memo", "brief", "minutes", "answer", "seat_argument", "minority_report"]
    template_text: str; rendered_html: str; claims: tuple[ClaimRecord, ...]; validation: ValidationReport
    provenance_root: ArtifactRef; data_class: DataClass
class AuditFinding(BaseModel): claim_id: str; severity: Literal["minor", "major"]; text: str
class AuditCheck(BaseModel): check: Literal["recompute", "contract", "references", "bundle_alignment"]; result: Literal["pass", "fail"]
class AuditReport(BaseModel):                 # assembled by deterministic code from an AuditDraft
    doc_id: str; checks: tuple[AuditCheck, ...]
    findings: tuple[AuditFinding, ...]; verdict: Literal["PASS", "FAIL"]; family: ModelFamily; correlated: bool

# LLM draft models (S-ADR-36): the only output models a role may submit. No engine-owned, validator-owned or human-owned field.
class MemoDraft(BaseModel): doc_kind: Literal["memo", "brief", "minutes", "answer", "minority_report"]; template_text: str
class SeatArgumentDraft(BaseModel): seat_id: str; item_id: str; cruxes: tuple[str, ...]; template_text: str
                                    view_proposals: tuple["ViewSpecDraft", ...] = ()   # beliefs change only through typed views
class AuditDraft(BaseModel): doc_id: str; checks: tuple[AuditCheck, ...]; findings: tuple[AuditFinding, ...]; verdict: Literal["PASS", "FAIL"]
class AnswerDraft(BaseModel): context_id: str; statements: tuple["StatementDraft", ...]; not_answered: tuple[str, ...] = ()
class StatementDraft(BaseModel): text: str; kind: Literal["model_output", "agent_judgment", "assumption"]; refs: tuple[ArtifactRef, ...]
class ProvenanceNode(BaseModel): ref: ArtifactRef; kind: str; parents: tuple[ArtifactRef, ...]; hash: str

class EvidenceSpec(BaseModel): metric: MetricId; by: tuple[str, ...] = (); plane: EvidencePlane = EvidencePlane.SEALED; max_age_days: int = 31
class DecisionVariable(BaseModel): name: str; unit: str; bounds: tuple[float, float] | None = None
class SignpostRule(BaseModel): count_min: int = 3; count_max: int = 6; alarm_sigma: float = 0.5; rearm_sigma: float = 0.25
class DecisionType(BaseModel):
    id: str; title: str; proposer: str; decider: str; tier: Tier | None
    cadence: Literal["quarterly", "annual", "event", "monthly", "dealing_dates", "budget_cycle"]
    deadline_rule: str; variables: tuple[DecisionVariable, ...]
    always_show: tuple[OptionKind, ...] = (OptionKind.STATUS_QUO, OptionKind.DEFER, OptionKind.RECOMMENDED)
    evidence: tuple[EvidenceSpec, ...]; signposts: SignpostRule; increment: Literal["1", "v1"]
class Register(BaseModel): version: str; entries: tuple[DecisionType, ...]; signoffs: tuple[SignOff, ...]; hash: str
class RunSpec(BaseModel): tool: str; args: dict[str, Any]; plane: Plane; spec_hash: str
class EvidencePlan(BaseModel): specs: tuple[RunSpec, ...]; edges: tuple[tuple[str, str], ...]
                               by_decision: dict[str, tuple[str, ...]]; hash: str
class Theta(BaseModel):                      # admissible value set Θ (ARCH §8.5; S-ADR-06)
    gamma: float          # [2, 6]
    lambda_T: float       # [0, 2]
    shortfall_exponent: float   # (1, 3]
    t6_limit: float       # <= the IC tolerance band
    extra_costs: dict[MetricId, float] = {}  # engine metrics only; no indicator or probability terms
class SeatSpec(BaseModel):
    seat_id: str; mandate: str                # "PE mandate (AI seat)" — never a person's name
    belief_channel: Literal["base_mixture", "worst_class", "base_plus_owner_stress", "group_forecasts",
                            "reference_class", "min_kl_failure"]
    group: GroupId | None; theta: Theta | None; family: ModelFamily; recuse_on: tuple[GroupId, ...] = ()
class SeatAssessment(BaseModel):              # assembled by idm.seats from engine outputs + a SeatArgumentDraft; never an LLM output
    seat_id: str; item_id: str; implied_action_ref: ArtifactRef; regret_bp: dict[str, float]   # engine numbers (implied_actions)
    belief_value_split: tuple[float, float]; event_probs_ref: ArtifactRef   # engine probabilities of the frozen-question events
    cruxes: tuple[str, ...]; argument: RenderedDocument
    hash: str                                   # v1.0's agent_judgment_probs field is removed (S-ADR-36; QUANT-10)
class MinorityReport(BaseModel):
    author: str; item_id: str; document: RenderedDocument; authentic: bool   # Red Team: authentic=False ("assigned dissent")
    trigger: Literal["dp15", "regret10", "member"]; hash: str
class PreVote(BaseModel):
    member_hash: str; item_id: str; choice: Literal["approve", "resize", "defer", "reject"]
    probabilities: dict[str, float]; rationale: str; locked_at: datetime; hash: str
class Ballot(BaseModel):
    member_hash: str; item_id: str; choice: Literal["approve", "resize", "defer", "reject"]
    probabilities: dict[str, float]; rationale: str; what_would_change: str
    recused: bool; second_chance_ack: bool; how_could_be_wrong: str | None; cast_at: datetime; hash: str
class OptionSummary(BaseModel):
    kind: OptionKind; label: str; policy_ref: PolicyRef | None
    delta_ce_bp: MetricId; p_red_by_class: dict[str, MetricId]; p10_target: MetricId; delta_survival_months: MetricId
class Signpost(BaseModel):
    indicator: MetricId; flip_value: float; alarm_value: float; rearm_band: float; sigma: float; owner: str
    state: Literal["armed", "alarm", "flipped", "rearmed"] = "armed"
class ContingentAction(BaseModel): condition: str; action: str; tier: Tier
class OutcomeScore(BaseModel): horizon: Literal["q1", "q4", "q8"]; brier: float; resolved_at: date; detail: dict[str, float]
class DecisionRecord(BaseModel):              # ARCH §8.9 verbatim, plus data_class and the hash chain
    decision_id: DecisionId; register_id: str; as_of: date; tier: Literal["A", "B", "C", "Board"]
    options: tuple[OptionSummary, ...]; engine_recommendation: str
    evidence_plane: Literal["sealed", "search", "exploratory"]; run_manifests: tuple[RunId, ...]
    priced_on: PricedOn; consent_scenario: ConsentScenario; recovery_hash: str | None
    prevote_hashes: tuple[str, ...]; ballots: tuple[Ballot, ...]; decision: str
    override: Literal["belief", "value", "info_outside_model", "implementation", "legal_consent", "relationship", "other"] | None
    rationale: str; minority_reports: tuple[str, ...]; signposts: tuple[Signpost, ...]
    commitment_plan: tuple[ContingentAction, ...]; review_date: date
    outcomes: dict[Literal["q1", "q4", "q8"], OutcomeScore] = {}
    data_class: DataClass; prev_hash: str; record_hash: str
class ViewSpecDraft(BaseModel):               # what the Translator, a seat narrator or the analyst may emit
    channel: Literal["FBE", "EP"]; metric: str; operator: Literal["eq", "le", "ge"]; value: float
    confidence_c: float = 0.6; horizon_q: int | None = None
class ViewSpec(BaseModel):                    # assembled by code; confirmed and author_hash are set only by a human confirmation step
    view_id: str; draft: ViewSpecDraft; author_hash: str; confirmed: bool = False; confirmed_by: str | None = None
    confirmation_surface: Literal["tpa_chat", "ask_service", "room_console", "mcp_client_attested"] | None = None
class ScenarioSpecDraft(BaseModel):           # LLM-facing (red team): targets as a KeyValue list, not a dict
    kind: Literal["tilt", "param_shift", "named"]; targets: tuple[KeyValue, ...]; kl_bound: float
class ScenarioSpec(BaseModel):
    spec_id: str; kind: Literal["tilt", "param_shift", "named"]; targets: dict[str, float]; kl_bound: float; author_role: RoleId
class EPResult(BaseModel):
    weights_ref: ArtifactRef; kl: float; ess: float; max_ratio: float
    effective_views: tuple[ViewSpec, ...]; flags: tuple[Literal["inform", "warn", "amber", "red", "ess_block"], ...]
```

### 3.17 Ports (`contracts/ports.py`) and array contracts (`contracts/arrays.py`)

```python
class AssetEngine(Protocol):                       # priv.*, pub.*, overlay (ARCH §3.5 v1.1; S-ADR-28/29)
    engine_id: str; groups: tuple[GroupId, ...]; clock: Clock
    def init(self, book: BookSnapshot, beliefs: BeliefSet, n_paths: int, *, draws: BeliefDraws, world: WorldSpec) -> EngineState: ...
    def noise_requests(self, t: int) -> Sequence[NoiseRequest]: ...
    def recourse_quotes(self, t: int, st: EngineState, world: WorldSlice) -> RecourseAvailability: ...   # phase 1, quarter start
    def step(self, t: int, st: EngineState, world: WorldSlice, act: ActionSlice, noise: NoiseSlice) -> FlowSlice: ...
    def apply_recourse(self, st: EngineState, outcome: RecourseOutcome) -> None: ...   # phase 3: scale sold units before t + 1
    def column_flows(self, unit_id: UnitId, action: LensAction, cube: ScenarioCube) -> "FlowCube": ...
class Ledger(Protocol):
    def apply(self, m: int, ls: LedgerState, flows: Sequence[FlowSlice], draw: F32,
              quotes: RecourseAvailability) -> tuple[LedgerState, RecourseOutcome]: ...   # phase 2; books proceeds once
    def row_slacks(self, ls: LedgerState) -> dict[RowKey, F32]: ...
    def stress_replica(self, ls0: LedgerState, stress: StressSpec) -> StressReport: ...
class EngineFactory(Protocol):                     # implemented by core.sim.factory.DefaultEngineFactory (S-ADR-43)
    def build(self, book: BookSnapshot, world: WorldSpec) -> "EngineBundle": ...   # applies world.overrides; hashes effective configs
@dataclass(frozen=True)
class EngineBundle:
    engines: tuple[AssetEngine, ...]; ledger: Ledger; owner_cfg: OwnerConfig
    policy_wrappers: tuple[Callable[[Policy], Policy], ...]   # e.g. playbook slippage (one-quarter delay, 50% fills)
    effective_config_hashes: Mapping[str, str]
class Policy(Protocol):
    policy_ref: PolicyRef
    def act(self, q: int, obs: Observables) -> ActionSlice: ...   # obs lagged; no horizon, path id or world id
class LLMBackend(Protocol):
    family: ModelFamily
    def parse(self, req: "LLMRequest", output_model: type[BaseModel]) -> "LLMResponse": ...
    def run_tools(self, req: "LLMRequest", tools: Sequence["ToolDef"], executor: "ToolExecutor") -> "LLMResponse": ...
class EvaluatorPort(Protocol): ...                 # one typed method per evaluator tool (§7.4); in-process or MCP client
class RoomPort(Protocol):                          # implemented by idm.room_service.RoomService; injected by pipeline
    def compile_agenda(self, quarter: str, snapshot_hash: str) -> EvidencePlan: ...
    def build_briefs(self, plan: EvidencePlan) -> tuple[RenderedDocument, ...]: ...
    def run_shadow_ic(self, items: Sequence[str]) -> tuple[SeatAssessment, ...]: ...
    def lock_prevotes(self, quarter: str) -> tuple[str, ...]: ...
    def record_decisions(self, quarter: str) -> tuple[DecisionRecord, ...]: ...
```

**Array contracts** (`ARRAY_SPECS`; checked by `validate()`):

| Name | Shape (axis order) | dtype | Units | Invariants |
|---|---|---|---|---|
| `ScenarioCube.factors` | [P, 120, K] | f32 | per `meta.factor_kinds` (log return, level or change) | finite; checksum matches `meta.checksum` |
| `ScenarioCube.regimes` | [P, 120, 3] | i8 | enum codes (S, e, Z) | values in enum ranges |
| `ScenarioCube.stress_post` | [P, 120, 3] | f32 | probability | rows sum to 1 ± 1e-5 |
| `ScenarioCube.asset_returns` | [P, 120, A] | f32 | monthly log return | expected 10-year log return E[Σ log(1 + r)] within 5bp of the CMA geometric mean (converted from `arith_mean_a` and `vol_a`); annualized vols and correlations within tolerance of the world's CMA (scen test) |
| `ScenarioCube.draw_rate` | [P, 11] | f32 | decimal a year | in [0.05, 0.10] except flagged overrides |
| `GroupRates.*` | [P, 12, Gp, 2] (or [P, 12]) | f32 | per quarter; returns simple | delta, qcall ∈ [0, 1]; bid ∈ (0, 1.2]; nav_share sums to 1 over age buckets |
| `Tree.p` | [N] | f64 | probability | children's p sum to parent's p (1e-12); leaves sum to 1 |
| `Tree.p_world` | [N, W] | f64 | probability | per world, leaves sum to 1 |
| `NoiseSlice.u[source]` | [P, nm, n_ent, slots] | f64 | uniform | in [0, 1) |
| `ActionSlice.sell_frac` | [P, U] | f32 | fraction | in [0, 1] |
| `FlowSlice.by_group` | [P, G, 18] | f32 | $bn per period, signed | signs per `FlowType`; non-cash columns excluded from liquidity |
| `FlowSlice.intra` | [P, G, 18] | f32 | $bn | Σ_g = 0 (1e-9 × scale) |
| `FlowSlice.by_recourse_unit` | [P, U_r, 18] | f32 | $bn per period, signed | units listed in `recourse_unit_ids`; Σ over units ≤ `by_group` per group |
| `FlowCube.values` | [P, 40, U, 18] | f32 | $bn per quarter | one block at most; unit→group map in meta; column cubes carry only affected units |
| `RecourseAvailability.*` | [P, U_r] | f32 / i8 | fraction of economic NAV; months | bid ∈ (0, 1.2]; depth ∈ [0, 1] |
| `RecourseOutcome.sold_frac` | [P, U_r] | f32 | fraction | in [0, depth]; month ∈ [−1, 119]; red only where tier = red |
| `BeliefDraws.alpha0_q` | [P, U] | f32 | log return per quarter | finite; with zero posterior noise, bias, GP effect and basis shift it equals `BeliefSet.alpha_a`/4 exactly |
| `LedgerState.*` | [P] or [P, k] | f64 | $bn / stage codes | conservation Δcash = Σ cash flows (1e-10); NAV ≥ 0 |
| `LedgerPaths.rows` | [P, 121, R] | f32 | $bn slack | row_keys length R |
| `StressReport.headroom_bn` | [P, 24] | f64 | $bn | d0 = max(0, −min_h) |
| `BeliefSet.alpha_a`, `mu_total_a` | [U] | f64 | annual log return | finite; mu_total_a = bench_ref_a + alpha_a; band80[:,0] < mu_total_a < band80[:,1] |
| `PathMetrics.quarterly` | [P, 41, Kq ≤ 48] | f32 | per series meta | streamed per block to Parquet |
| `PathMetrics.terminal` | [P, Kt] | f64 | per series meta | red flag ∈ {0, 1}; failed paths carry worst-case values |
| `LPModel.A` | [m, n] sparse CSC | f64 | W₀ units | finite; ‖coef‖ ≤ 1e4; penalties ≤ 1e4 |
| `DualSet.ell` | [N] | f64 | per period | finite; ≥ 0 at pricing nodes when μ − M > 0 |
| `PathMetrics` payload for W1 | [10,000, ≤ 40] | f16 (embedded) | metric units | §8.4 |

`PathMetrics` (array container, `contracts/evidence.py`): `meta` (world, plane, policy_ref, cube checksum, series names), `quarterly F32[P, 41, Kq]`, `terminal F64[P, Kt]` with Kt series at least: `w_tilde_40` (own-return accrued, W₀ units), `w_tilde_real_40`, `twr_3y`, `twr_5y`, `twr_10y`, `red_event`, `red_quarter`, `payout_short`, `t7_shortfall_12m`, `t9_trigger_12m`, `max_dd_10y`, `failed`.

### 3.18 Shared helper types and the type-ownership rule

**Rule.** Every type named in a §4 signature has exactly one defining module. Types that cross a WP boundary as *inputs* live in `contracts`; result types live in the module that returns them and may be imported by any module the import table (§4.0) allows. A type not listed here or in §3.1–3.17 is defined by the module whose signature returns it.

```python
# contracts/world.py (moved here because several WPs consume them)
class StressFilterParams(BaseModel):          # produced by state (WP-07); consumed by scen, core.sim
    means: list[list[float]]; covs: list[list[list[float]]]; transmat: list[list[float]]; startprob: list[float]
    fitted_through: date; ab: tuple[float, float]; base_rate: float; version_hash: str
class OwnerConfig(BaseModel): ...             # fields as listed in §4.8; produced from config/owner.yaml; consumed by owner, state, core.sim

# contracts/world.py (continued)
class GroupRatesMeta(BaseModel):              # BUILD-11: was referenced but undefined
    groups: tuple[GroupId, ...]; age_buckets: tuple[str, ...]; policy_ref: PolicyRef; world_id: WorldId
    cube_checksum: str; quarters: int = 12; rate_kind: Literal["simple"] = "simple"

# contracts/optimizer.py (shared by ledger.linear (WP-13), core.tree/core.h (WP-18), actions (WP-16))
@dataclass(frozen=True, slots=True)
class NodeCoefficients(ArrayContainer):       # GroupRates fields aggregated per node (fan periods compounded); RATES only, never amounts
    delta: F64; qcall: F64; ret_simple: F64; bid: F64; income: F64                 # [N, Gp, 2]
    u_per_nav: F64; nav_share: F64; call_stress_12m: F64                           # [N, Gp, 2]  κ^U, ω, H3 outflow rate
    lo_ret: F64; hf_ret: F64; vm_per_beta: F64; cash_rate: F64; fac_rate: F64; draw_rate_q: F64; tau_lo: F64; h_im: F64   # [N]
    ra_debt_rate: F64; ra_amort: F64; ra_direct_share: F64                         # [N]
    tail_prem_rate: F64; tail_value: F64; opp_pnl_rate: F64; delta_im_rate: F64; opex_rate: F64   # [N]
    hf_phi: F64                                                       # [N, 4]
    fac_avail: F64                                                    # [N, NF]  availability multipliers (≤ 0.5 in the joint oil–crisis state)
    amber_depth: F64                                                  # [N, Ga]  depth fraction per amber group
    # v1.0's outflows_next, liq_cap, amber_cap and fac_cap (exogenous W₀ amounts) are removed: H3 builds them from the
    # node's state with these rates, so converting a non-red resource into cash leaves H3 unchanged (S-ADR-33; QUANT-06)

class T6Screen(BaseModel):                    # produced by core.h.t6_screen; consumed by core.h.recovery_mode (BUILD-11)
    scenario: ConsentScenario; levers_at_cap: tuple[str, ...]
    t6_cvar_at_hold: dict[str, float]         # per class, CVaR row value at HOLD with every reversible lever at cap (W₀ units)
    floor_cvar_at_hold: dict[str, float]      # per world (Tier 1B)
    breach: dict[str, Literal["none", "tolerance", "capacity"]]   # only "capacity" triggers Phase I-b (S-ADR-31)
@dataclass(frozen=True, slots=True)
class LinearizedTier1(ArrayContainer):        # module F's linearized Tier-1 rows (core.select.safety)
    row_keys: tuple[RowKey, ...]; action_names: tuple[str, ...]
    G: F64            # [m_F, n_a]  row Jacobian with respect to the action vector (from duals, FD-checked)
    g0: F64; delta: F64   # [m_F]  row values at the proposal; amber buffers δ_k
    fd_checked: bool
class ExactCheck(BaseModel):
    passed: bool; violations: dict[str, float]; simm_im_bn: float; ov3_share: float; recomputed_rows: tuple[str, ...]
@dataclass(frozen=True, slots=True)
class VarIndex(ArrayContainer):
    state_names: tuple[str, ...]; decision_names: tuple[str, ...]
    state_cols: I32; decision_cols: I32       # [N, n_state], [N, n_dec]; −1 where a decision does not exist at a node
    root_cols: dict[str, int]; leaf_cols: dict[str, I32]   # leaf auxiliaries: u, psi, w_tilde, z_<class>, z_floor
@dataclass(frozen=True, slots=True)
class RowBlock(ArrayContainer):               # COO triplets for a batch of rows
    row_keys: tuple[RowKey, ...]; i: I32; j: I32; v: F64; lo: F64; hi: F64; role: I8; tier: I8
@dataclass(frozen=True, slots=True)
class RowIndex(ArrayContainer):               # produced by core.h.row_index(lp) AFTER build_h; used only at pricing time (BUILD-22)
    row_of: dict[str, int]                    # str(RowKey) -> row number in the assembled LPModel

# contracts/ledger.py (continued; S-ADR-29, BUILD-01): the recourse protocol
@dataclass(frozen=True, slots=True)
class RecourseAvailability(ArrayContainer):   # produced by every AssetEngine.recourse_quotes at quarter start
    engine_id: str; unit_ids: tuple[UnitId, ...]; group_of: tuple[GroupId, ...]
    bid_frac: F32           # [P, U_r]  cash-equivalent bid ÷ economic NAV this quarter (incl. crowding haircut)
    normal_bid_frac: F32    # [U_r]     normal-regime hedonic bid for the unit's age and size (red test (iii))
    depth_frac: F32         # [P, U_r]  maximum fraction saleable this quarter
    lag_m: I8               # [P, U_r]  settlement lag in months
    tier: I8                # [U_r]     1 = amber, 2 = red (from the taxonomy)
@dataclass(frozen=True, slots=True)
class RecourseOutcome(ArrayContainer):        # returned by Ledger.apply; consumed by AssetEngine.apply_recourse and metrics
    unit_ids: tuple[UnitId, ...]
    sold_frac: F32          # [P, U_r]  fraction of the position sold by recourse_cover this quarter
    month: I16              # [P, U_r]  month of the sale, −1 if none
    proceeds_bn: F64        # [P, U_r]  booked by the ledger after the lag (engines never book recourse proceeds)
    red: B                  # [P, U_r]  ledger.red_test result (S-ADR-30)
    reason: I8              # [P, U_r]  SaleReason label (reporting only)

# contracts/rules.py (pure functions; one copy shared by owner, ledger, priv and H; BUILD-25)
def instalment_bn(draw_rate: F64, basis_bn: F64, instalments_left: int, paid_ytd_bn: F64) -> F64: ...   # ≤ 0; remaining ÷ left
def intra_quarter_profile(flow_type: FlowType, clock: Clock) -> F64: ...   # [3] month weights; A1 governs its use

# contracts/ports.py (continued): contexts that cross WP boundaries (BUILD-11)
@dataclass(frozen=True)
class PolicyContext:
    idx: UnitIndex; tax: GroupRegistry; p0_theta: Mapping[str, float]; recourse: RecourseOrder
    mandate_mode: MandateMode; archetype_params: Mapping[str, Mapping[str, float]]; contract_hash: str
@dataclass(frozen=True)
class SimContext:
    factory: EngineFactory; book: BookSnapshot; beliefs: BeliefSet; state0: StateSnapshot; worlds: Mapping[WorldId, WorldSpec]
    owner_cfg: OwnerConfig; filter_params: StressFilterParams; root_seed: int; plane: Plane; salt: bytes | None
    policy_ctx: PolicyContext; contract_hash: str
@dataclass(frozen=True)
class EngineContext:                          # what core.mpc needs beyond the contract and snapshot
    sim: SimContext; tree_spec: TreeSpec; catalogue_cfg: Mapping[str, Any]; solver_policy: Mapping[str, str]; processes: int = 5

# contracts/evidence.py (continued)
class FBEValidationSet(BaseModel):            # produced by beliefs.validation.fbe_variant (pure functions of seeds and variant parameters); no synth import (BUILD-21)
    variant: str; n_worlds: int; root_seed: int; config_hash: str
    forecasts_ref: ArtifactRef; truth_ref: ArtifactRef; oracle_ref: ArtifactRef

# contracts/overlay.py (shared by overlay (WP-12), actions (WP-16), core.h (WP-18))
@dataclass(frozen=True, slots=True)
class OverlayStressCoeffs(ArrayContainer):
    stresses: tuple[str, ...]; col_ids: tuple[str, ...]
    nv_eq_tail: F64; nv_eq_ovl: F64; pnl_tail: F64; pnl_opp: F64     # [S, n_cols] per unit of each overlay column
    base_nv_eq_tail: F64; base_nv_eq_ovl: F64; base_pnl_tail: F64; base_pnl_opp: F64   # [S] for the current book

# contracts/evidence.py
class GateReport(BaseModel):                  # produced by priv.check_v24, synth.run_gates, beliefs.validate_fbe
    subject: str; gates: dict[str, Literal["pass", "fail", "n/a"]]; details: dict[str, dict[str, float]]; blocking: bool

# contracts/tools.py — evaluator and lab tool I/O (strict schemas, additionalProperties: false)
class StateSnapshotIn(BaseModel): pass
class StateCard(BaseModel): cfp: CFPReading; F_t: float; e0: tuple[float, ...]; z0: tuple[float, ...]
                            draw_12m_bn: tuple[float, float]; t4p_survival_months: dict[RecourseTier, int]
                            lambda_spot: dict[StressState, float]; plane: EvidencePlane; refs: tuple[ArtifactRef, ...]
class Phase1In(BaseModel): scenario: ConsentScenario | None = None
class TierSummary(BaseModel): tier: int; u_star_bn: float; iis: tuple[str, ...]; levers_at_cap: tuple[str, ...]
class Phase1Card(BaseModel): by_scenario: dict[ConsentScenario, tuple[TierSummary, ...]]; mode: ContractMode
                             d0_bn: float; glide: GlidePath | None; pricing_scenario: ConsentScenario
class TypedOverride(BaseModel): target: str; field: str; value: float; unit: str; source_view_id: str
class OptimizeHIn(BaseModel): preset: Literal["whatif"] = "whatif"; views: tuple[ViewSpec, ...] = (); overrides: tuple[TypedOverride, ...] = ()
                              # views must carry confirmed = True; the tool returns HSummary (v1.0's OptimizeHOut is removed)
class HSummary(BaseModel): root_actions: tuple[LensAction, ...]; lambda_spot: dict[StressState, float]
                           ftp: tuple[FTPPoint, ...]; envelopes: tuple[Envelope, ...]
                           gamma_status: Literal["certified", "selection_not_certified"]; priced_on: PricedOn
                           plane: Literal["exploratory"] = "exploratory"; run_ref: ArtifactRef
class PackagePrice(BaseModel): robust_rc_bucket: str; dominated: bool
class ScenarioResult(BaseModel): dp_red_bucket: str; binding_rows: tuple[str, ...]; kl: float
class ReverseStressIn(BaseModel): metric: MetricId; threshold: float
class ReverseStressResult(BaseModel): kl: float; tilt_ref: ArtifactRef; ranking: tuple[tuple[str, float], ...]
class ImpliedIn(BaseModel): seat_id: str; item_id: str
class ImpliedActionCard(BaseModel): seat_id: str; item_id: str; action: str; regret_bp_by_option: dict[str, float]; ref: ArtifactRef
class EPIn(BaseModel): views: tuple[ViewSpec, ...]
class EVSIIn(BaseModel): item_id: str
class EVSIResult(BaseModel): lb80_usd_m: float; mean_usd_m: float; folds: int; cost_of_delay_usd_m: float
class FlipIn(BaseModel): card_id: str
class AttributeIn(BaseModel): run_id: RunId; kind: Literal["shapley6", "group", "null", "what_moved"]
class AttributionCard(BaseModel): kind: str; components: dict[str, tuple[float, float]]; residual: float
                                  established: dict[str, bool]; ref: ArtifactRef
class EnvelopeSummary(BaseModel): envelopes: tuple[Envelope, ...]; pool_bn: dict[str, float]
class OffsetRow(BaseModel): stress: str; pnl_tail_bn: float; pnl_opp_bn: float; offset_ratio: float
                            nv_eq_economic: float; nv_simm: float; im_by_csa_bn: dict[CsaId, float]; im_saving_priced_bn: float
class OffsetCard(BaseModel): rows: tuple[OffsetRow, ...]; stress_coverage_ratio: float
class TradePrice(BaseModel): value_bn: float; greeks_ref: ArtifactRef
class HybridCheck(BaseModel): implied_corr_spread: float; q_vs_p_pass: bool; accepted: bool
class TypeReport(BaseModel): passed: bool; errors: tuple[tuple[str, str], ...]     # (code, detail), codes INVALID_SPEC/TR1..TR8
class ReviewFindings(BaseModel): findings: tuple[str, ...]; severity: tuple[Literal["minor", "major"], ...]
class VariantSet(BaseModel): variants: tuple[PolicySpec, ...]; rationale: tuple[str, ...]
class ExtractionRecord(BaseModel): doc_hash: str; fields: tuple[KeyValue, ...]; confidence: float; extractor_family: ModelFamily
                                   # confidence is a QA diagnostic only; fields reach engines only after verification (S-ADR-36)

# contracts/analyst.py (S-ADR-34; frozen by WP-01 with contracts-v1.0). The models below are the minimum set; CHAT_ANALYST §5.1, §5.3 and §6.3
#   are binding and add Fact, QuoteRef, TableSpec, ToolResult[P], ToolError/ToolErrorCode, the 30 tools' input and payload models,
#   OverrideConfirmation and ConfirmToken. Where a name differs (WhatIfDraft ≈ OverrideDraftView, WhatIfConfirmation ≈ OverrideConfirmation),
#   the addendum's name and fields win; the evaluator checks OverrideConfirmation and ignores ViewSpec.confirmed on analyst runs.
class Principal(BaseModel): user_hash: str; roles: tuple[str, ...]; groups: tuple[GroupId, ...]; recusals: tuple[GroupId, ...]
                            barriers: tuple[str, ...]; prevote_locked_items: tuple[str, ...]
class ContextHandle(BaseModel): context_id: str; asof: date; contract_hash: str; census_id: CensusId | None
                                allocation: AllocationId; plane: EvidencePlane; data_class: DataClass; run_ids: tuple[RunId, ...]
class Statement(BaseModel): text: str; kind: Literal["model_output", "agent_judgment", "assumption"]; refs: tuple[ArtifactRef, ...]
class AnswerCard(BaseModel):                  # assembled from an AnswerDraft by analyst.answers; rendered by claims.render
    context_id: str; statements: tuple[Statement, ...]; status: AnswerStatus; synthetic: bool; interim: bool
    rendered: RenderedDocument; not_answered: tuple[str, ...] = ()
class WhatIfDraft(BaseModel): draft_hash: str; kind: Literal["belief_view", "scenario_view", "lever_change"]
                              view: ViewSpecDraft | None; lever: TypedOverride | None; back_translation: str
                              effective_value: float | None; kl: float | None; ess: float | None; recompute: tuple[str, ...]
                              tier: Literal["W1", "W2", "W3"]
class WhatIfConfirmation(BaseModel): draft_hash: str; principal: Principal; surface: Literal["tpa_chat", "ask_service", "mcp_client_attested"]
                                     confirmed_at: datetime; single_use_token: str
class ChatTurnRecord(BaseModel): session_id: str; turn: int; principal_hash: str; surface: str; question_hash: str
                                 tool_calls: tuple[str, ...]; answer_ref: ArtifactRef; validator_passed: bool; status: AnswerStatus
                                 served_model: str; tokens: int; cost_usd: float; prev_hash: str; record_hash: str
```

| Result types defined outside `contracts` | Defining module | Consumers |
|---|---|---|
| `SimResult` (a frozen dataclass: it holds arrays), `JResult`, `Tier1Board`, `CertificationReport`, `GamblingReport`, `TerminalValues`, `ObservableHistory`, `ObsVarSpec`, `DefaultEngineFactory` | `core.sim` (`sim.py`, `factory.py`, `policy.py`, `observables.py`, `certify.py`, `terminal.py`) | core.h, core.select, core.dsl, core.mpc, attrib, evaluator |
| `LPResult`, `Basis` | `core.h` (`solver.py`, `phase1.py`) | core.select, core.mpc, attrib |
| `HPTestResult`, `BufferCalibration` | `core.select`, `core.mpc` | core.mpc, evaluator |
| `MPCResult` | `core.mpc` | evaluator |
| `PricedSet`, `RequestPrice`, `ChargesReport`, `DVAReport`, `TransferVerdict`, `ServicesLedger`, `GroupReturns`, `InternalTransfer`, `ChargeConfig` | `icm` | core.mpc, attrib, evaluator |
| `VariableRegistry` | `core.dsl` | evaluator |
| `EPSolution`, `FrontierTable`, `RobustnessCard`, `RobustConfig` | `robust` | attrib, evaluator |
| `NullControl`, `IRBResult`, `GTResult`, `OwnerProposalReport`, `SafetyPriceTable`, `V8Fixture` | `attrib`, `core.irb` | evaluator |
| `SimmParams`, `SimmResult`, `OVReport`, `LadderSpec`, `MarketState`, `NamedStress`, `OverlayState` | `overlay` | actions, core.h, core.select, evaluator |
| `CFPConfig`, `LadderConfig`, `LadderReport`, `RowFamilySpec`, `LedgerConfig`, `ReadinessModel`, `GStarGrid` | `ledger` | core.sim, core.h, evaluator |
| `SyntheticCommittee` (DEV_SYNTHETIC only) | `testing` (`committee.py`) | pipeline, tests |
| `SignalSet`, `BiasModel`, `KappaPosterior`, `FrozenOptimizerOutputs`, `FittedHazards`, `NowcastConfig`, `BiasConfig`, `FuseConfig`, `FlagConfig` | `beliefs` | evaluator, pipeline |
| `PrivTemplates`, `MeanPathFlows`, `OverlapParams` | `priv` | synth, actions |
| `InitialStateInputs`, `ShockNowcastInputs`, `HarnessConfig`, `HarnessReport` | `state` | evaluator, pipeline |
| `AnchorReport`, `CalibConfig` | `scen` | evaluator |
| `PayoutRule`, `OwnerRuleState` | `owner` | attrib |
| `AdmissibilityState`, `AdmissibilityResult`, `ScoreBreakdown`, `CatalogueConfig` | `actions` | core.h, core.select, evaluator |
| `SynthConfig`, `SynthBook`, `ObservationSet`, `ReleaseManifest`, `HistoryRule`, `PEHistory`, `MRMToken`, `TruthReader` | `synth` | pipeline, cli (`FBEValidationSet` now lives in `contracts.evidence`) |
| `AnalystService`, `EntitlementRule`, `ChatSession` | `analyst` | cli, mcp_server, pipeline |
| `StorePaths`, `RequestContext`, `SealedResult`, `PlaneCache` | `evaluator`, `seal` | lab, pipeline |
| `SealClient`, `LabConfig`, `CampaignStatus`, `CampaignHistory`, `BudgetLedger` | `lab` | pipeline, cli |
| `EvidenceStatus`, `RegretTable`, `TallyResult`, `RoomService` | `idm` | pack, pipeline |
| `PackManifest`, `EPPayload`, `EPGolden`, `FigureSpec`, `PackTheme` | `pack` | pipeline, cli |
| `LLMRequest`, `LLMResponse`, `ToolDef`, `ToolExecutor`, `ToolRegistry` | `agents` (`LLMRequest`/`LLMResponse` re-exported by `contracts.ports` for the `LLMBackend` Protocol) | lab, idm |
| `Placeholder` | `claims` | agents, idm, pack |
| `ChainReport`, `MFDRLedger` | `registry` | cli, lab |
| `AdapterValidation`, `AdapterReport` | `data` | cli |
| `QuarterResult` | `pipeline` | cli |

---

## 4. Module specifications

### 4.0 Import table (authoritative; enforced by `tests/layering/test_imports.py`)

The test parses every module's AST and fails on any `adic_tpa.*` import not listed. Engine modules (everything above `evaluator`) never import `lab`, `agents`, `claims`, `idm`, `pack`, `analyst`, `pipeline` or any networking module (`socket`, `http`, `urllib`, `requests`, `httpx`, `anthropic`, `mcp`). The asset engines (`priv`, `pub`, `overlay`) never import `beliefs` either: belief draws arrive through `AssetEngine.init(…, draws=…)`, produced by `beliefs.draw_paths` and passed by `core.sim` (S-ADR-28). The owner instalment rule and the intra-quarter profiles exist once, in `contracts.rules` (BUILD-25).

| Module (package path under `src/adic_tpa/`) | May import (adic_tpa) | Wave | WP |
|---|---|---|---|
| `contracts` | — | 0 | 01 |
| `numerics` | contracts | 0 | 02 |
| `rng` | contracts, numerics | 0 | 02 |
| `stats` | contracts, numerics | 0 | 02 |
| `testing` | contracts, rng, numerics | 0 | 03 |
| `registry` | contracts | 0 | 04 |
| `data` | contracts | 1 | 05 |
| `owner` | contracts, rng, numerics | 1 | 08 |
| `state` | contracts, rng, numerics, stats, data, owner | 1 | 07 |
| `scen` | contracts, rng, numerics, data, state | 1 | 06 |
| `pub` | contracts, rng, numerics | 1 | 11 |
| `priv` | contracts, rng, numerics, pub | 1 | 09, 10 |
| `overlay` | contracts, rng, numerics | 1 | 12 |
| `ledger` | contracts, numerics | 1 | 13 |
| `beliefs` | contracts, rng, numerics, stats, data | 1 | 14 |
| `bridge` | contracts, numerics, stats, data | 1 | 14 |
| `synth` | contracts, rng, numerics, data, owner, state, scen, pub, priv, overlay | 2 | 15 |
| `actions` | contracts, rng, numerics, pub, priv, overlay, ledger, beliefs | 2 | 16 |
| `core.sim` (`observables`, `sim`, `factory`, `policy`, `terminal`, `certify`) | contracts, rng, numerics, stats, owner, state, scen, pub, priv, overlay, ledger, beliefs | 2 | 17 |
| `core.h` (`tree`, `h`, `solver`, `phase1`, `phase2`, `duals`, `kernel`) | contracts, rng, numerics, ledger, overlay, actions, core.sim | 2 | 18 |
| `core.select` (`colgen`, `levelb`, `safety`) | contracts, numerics, stats, ledger, overlay, actions, core.sim, core.h | 2 | 19 |
| `icm` | contracts, numerics, ledger, core.h | 3 | 20 |
| `core.mpc` | contracts, numerics, stats, state, beliefs, actions, core.sim, core.h, core.select, icm | 3 | 20 |
| `core.dsl` (`dsl`, `search`) | contracts, rng, numerics, core.sim | 3 | 21 |
| `robust` | contracts, numerics, stats | 3 | 22 |
| `attrib` (+ `core.irb`) | contracts, numerics, stats, owner, core.sim, core.h, core.select, core.dsl, icm, robust | 3 | 23 |
| `evaluator` | contracts, registry, rng, numerics, stats, data, owner, state, scen, pub, priv, overlay, ledger, beliefs, bridge, actions, core.*, icm, robust, attrib | 3 | 24 |
| `seal` | contracts, registry, evaluator (client and runner only) | 3 | 24 |
| `claims` | contracts, registry | 4 | 25 |
| `agents` | contracts, registry, claims | 4 | 25 |
| `lab` | contracts, registry, claims, agents, evaluator.client, seal | 4 | 26 |
| `idm` | contracts, registry, claims, agents, evaluator.client | 4 | 27 |
| `pack` | contracts, registry, claims, idm | 4 | 28 |
| `analyst` | contracts, registry, claims, agents, evaluator.client | 4 (thin slice), 6 (v1) | 39, 40 |
| `mcp_server` | contracts, registry, evaluator.server, analyst.server (dispatch only) | 4 | 29 |
| `cli` | any (lazy imports inside commands) | 4 | 29 |
| `pipeline` | any | 5 | 30 |

Each entry below gives purpose, public API (exact signatures), algorithms, invariants, performance, errors, and tests with acceptance criteria. "Golden" means a frozen JSON in `tests/golden/` or `tests/regression/fixtures/`.

---

### 4.1 `contracts` (WP-01, wave 0)

**Purpose.** The frozen vocabulary: models (§3), enums, units, calendar, hashing, taxonomy registry, errors, config loading, array specs and Protocols.

```python
# hashing.py
def canonical_json(obj: Any) -> bytes             # sorted keys; separators (",", ":"); floats by repr(); NaN/inf forbidden;
                                                  # datetimes ISO-8601 UTC "Z"; enums by value; arrays by array_checksum; pydantic via model_dump(mode="json")
def content_hash(obj: Any) -> str                 # "sha256:<hex>"
def array_checksum(*arrays: np.ndarray) -> str    # sha256 over (dtype.str, shape, C-order bytes) of each array in order
def file_tree_hash(root: Path, patterns: Sequence[str] = ("**/*.py", "**/*.yaml", "**/*.csv", "**/*.md", "**/*.j2", "**/*.js")) -> str
                                                  # text files hashed with CRLF→LF normalized (core.autocrlf-proof; S-ADR-42)
def engine_tree_hash() -> str                     # file_tree_hash(src/adic_tpa)
def config_hash() -> str                          # file_tree_hash(src/adic_tpa/config)
VOLATILE_FIELDS: Final[frozenset[str]]            # run_id, created_at, recorded_at, cast_at, locked_at, prev_hash, record_hash,
                                                  # chain hashes, absolute paths; ArtifactRef run-id prefixes normalized to "<run>"
def canonical_artifact_hash(obj: Any) -> str      # content_hash after normalizing VOLATILE_FIELDS (e2e #9; BUILD-27)
# signing.py (S-ADR-40)
def sign(payload: bytes, key_ref: str) -> str; def verify(signoff: SignOff, roster: Mapping[str, bytes]) -> bool
# units.py
def q_rate(r_a: float | F64) -> float | F64; def m_rate(r_a): ...; def a_from_q(r_q): ...; def q_intensity(x_a): ...
def to_bp(x: float) -> float; BP: float = 1e-4
# calendar.py
class Calendar(BaseModel):
    asof_instant: date = date(2026, 9, 30); n_quarters: int = 40
    def quarter_end(self, t: int) -> date: ...    # instant t
    def month_end(self, m: int) -> date: ...
    def fiscal_year(self, t: int) -> int: ...     # of quarter period t
    def instalment_month(self, t: int) -> int: ...   # 3t + 2
    def fy_open_quarter(self, fy: int) -> int: ...   # quarter instant at which FY fy opens (0 for FY2026's in-horizon remainder)
# config.py
def load_yaml(path: Path, model: type[T]) -> T    # yaml.safe_load → json.dumps(default=iso) → model.model_validate_json (strict, JSON mode;
                                                  # S-ADR-39) + records file hash in a process-level audit list
def load_json_payload(raw: str | bytes, model: type[T]) -> T   # MCP tool I/O and registry rows: model_validate_json
# arrays.py
class ArrayContainer:
    def validate(self) -> None: ...               # against ARRAY_SPECS[type(self).__name__]
    def checksum(self) -> str: ...
    def to_npz(self, path: Path) -> str: ...      # returns checksum
    @classmethod
    def from_npz(cls, path: Path, expected_checksum: str | None = None) -> Self: ...
ARRAY_SPECS: Mapping[str, Mapping[str, ArraySpec]]   # ArraySpec(shape_symbols, dtype, units, invariants: tuple[str, ...])
SYNTHETIC_FOOTER: Final = "SYNTHETIC – NOT ADIC DATA"
```

**Invariants.** `content_hash` is stable across processes, machines and Python hash seeds (golden values). All models are frozen; mutation raises.
**Performance.** `content_hash(BookSnapshot)` for 500 holdings + 1,500 loans < 0.5 s.
**Tests.** `unit/test_hashing.py` (golden hashes for 10 objects; float repr round trip; NaN rejected); `unit/test_models_strict.py` (extra field rejected for every model; frozen); `unit/test_lens_action_rules.py` (each Lens rule, JE-MF9); `unit/test_contract_validators.py` (each ARCH §10.1 rule: missing owner_signoff in Mode H fails; OWNER_PROPOSAL cannot feed cards; STRUCT_RECOVERY without BOARD fails; ni_comparator mismatch fails; R1 pricing without a signed revolver fails; shortfall_exponent = 1.0 fails); `unit/test_cfp_invariant.py`; `layering/test_no_hardcoded_group_ids.py` (regex over `src/` excluding `config/`, `testing/` and `contracts/taxonomy.py`: no string literal equal to a configured group id or code; `CanonicalConventions.credit_cash_a` therefore has no code default); `unit/test_config_roundtrip.py` (every file under `config/` loads through its model in JSON mode; an enum string and a YAML list for a tuple field both validate); `unit/test_text_hash_lf.py` (CRLF and LF copies of a file hash equal); `unit/test_canonical_artifact_hash.py` (two runs differing only in run ids and timestamps hash equal); `unit/test_signing.py` (Ed25519 round trip; tampered payload fails; dev key refused in REAL mode); `unit/test_rules.py` (instalment = remaining ÷ instalments left; annual floor 5% of B_y, never 20%).

---

### 4.2 `rng` (WP-02, wave 0)

**Purpose.** Counter-based keyed random numbers (§1.7): CRN by construction, thread- and order-independent.

```python
PLANE_CODE: Mapping[Plane, int]; WORLD_CODE: Mapping[str, int]
def base_entropy(root_seed: int, plane: Plane, world: WorldId, *, salt: bytes | None = None,
                 misspec_index: int | None = None) -> bytes                     # 16 bytes; FINAL requires salt (HMAC)
def entity_key(entity_id: str | None) -> np.uint64
def stream_key(base: bytes, source: str, entity: np.uint64) -> np.ndarray      # uint64[2]; the slot is not in the key (S-ADR-38)
def philox4x64_10(counters: np.ndarray, key: np.ndarray) -> np.ndarray          # numba njit(parallel=True); U64[N,4] -> U64[N,4]
def uniforms(base: bytes, source: str, entity_ids: Sequence[str | None], paths: np.ndarray,
             months: np.ndarray, slots: int) -> F64                             # [len(paths), len(months), len(entity_ids), slots]
                                                                                # counter (path, month, ⌊slot/4⌋, 0), lane = slot mod 4
def draw_block(base: bytes, requests: Sequence[NoiseRequest], paths: np.ndarray) -> NoiseSlice   # stream keys cached per block
# samplers.py — vectorized inverse-CDF, one uniform per variate
def normal(u: F64) -> F64                                   # scipy.special.ndtri (7.5 ns per variate [M])
def student_t(u: F64, df: float, *, standardize: bool = True) -> F64   # tabulated inverse CDF in numba (abs error < 1e-7), tails
                                                            # by the asymptotic expansion; standardize → sqrt((df−2)/df)·t (unit variance)
def truncated_t(u: F64, df: float, lo: float, hi: float) -> F64
def gamma(u: F64, shape: float, scale: float = 1.0) -> F64  # tabulated inverse CDF per shape in numba (abs error < 1e-7);
                                                            # scipy stdtrit/gammaincinv (≈180–200 ns per variate [M]) only in tests
def exponential(u: F64, rate: F64) -> F64
def bernoulli(u: F64, p: F64) -> B
def categorical(u: F64, cum_probs: F64) -> I8               # cum_probs [..., k], last == 1
def kou_jump(u_occ: F64, u_size: F64, u_sign: F64, lam: float, eta_up: float, eta_dn: float, p_up: float) -> F64
```

**Algorithm.** Philox4x64-10 (Salmon et al. 2011): ten rounds with multipliers `0xD2E7470EE14C6C93`, `0xCA5A826395121157` and Weyl increments `0x9E3779B97F4A7C15`, `0xBB67AE8584CAA73B`. Uniform = `(x >> 11) * 2**-53`.
**Invariants.** Pure function of (base, source, slot, entity, path, month, j); identical output at 1, 4 and 8 numba threads, for any block size and any entity order.
**Performance.** ≥ 100M uniforms/s single-threaded with all four lanes (126M/s measured for numba Philox4x64-10 [M]); one quarter of draws for a 2,000-path block of the v2 book ≤ 0.02 s, so ≤ 4 s per 10,000 paths × 40 quarters (B1 line).
**Errors.** `SchemaError` (bad request), `SealBreach` (FINAL without salt).
**Tests.** `unit/test_philox_numpy_equivalence.py` (output equals `numpy.random.Philox(counter=c, key=k).random_raw()` for 20 pinned (c, k); the WP pins numpy's counter-advance convention in the test); `unit/test_sampler_tables.py` (tabulated t and gamma inverse CDFs within 1e-7 of scipy on a dense grid incl. tails; standardized t₅ variance 1 ± 0.005 on 1e6 draws); `determinism/test_rng_threads.py`; `statistical/test_uniformity.py` (KS p > 0.01 on 1e6 draws; |corr| < 0.005 across adjacent slots and entities); `unit/test_entity_order_invariance.py`; `unit/test_company_key_identity.py` (two claims on one company read identical EV draws: V24a).

---

### 4.3 `numerics` (WP-02, wave 0)

```python
def crra_tangents(points: Sequence[float], gamma: float) -> tuple[F64, F64]   # (slopes, intercepts) of tangent cuts u ≤ a_k x + b_k
def adaptive_tangent_points(leaf_wealth: F64, weights: F64, n: int = 48, lo_q: float = 0.01, hi_q: float = 0.99) -> F64
                                                                              # weighted-quantile placement on the previous solve's leaves
def pwl_power(breaks: Sequence[float], p: float) -> tuple[F64, F64]           # convex PWL of x**p (shortfall), secant form
def tangent_error_bound(points: Sequence[float], gamma: float) -> float       # h² max|U″| / 8: reported beside Γ, never a gate (A8)
def exact_objective(w_tilde: F64, w_tilde_real: F64, p: F64, gamma: float, lam_T: float, w_star: F64, p_exp: float) -> float
def brentq(f: Callable[[float], float], lo: float, hi: float, *, xtol: float = 1e-12, maxiter: int = 200) -> float   # raises SolverError
def nearest_correlation(C: F64, *, tol: float = 1e-10, maxiter: int = 500) -> F64   # Higham alternating projections
def logsumexp_weights(logw: F64) -> F64                                       # normalized weights
def weighted_quantile(x: F64, w: F64, q: float | F64) -> F64
def kish_ess(w: F64) -> float                                                 # (Σw)² / Σw²
```

**Tests.** Tangent cuts lie above U and touch at the points; `adaptive_tangent_points` places ≥ 60% of points inside the weighted P10–P90 of the leaf wealth; `exact_objective` equals the CRRA/shortfall formula to 1e-12; nearest_correlation returns PSD with unit diagonal; weighted_quantile equals `numpy.quantile` for equal weights. (v1.0's "`tangent_error_bound` ≤ 0.5bp CE at eight points" could never pass: the bound is 12–84bp a year; A8 is now the decision test of §5.14.)

---

### 4.4 `stats` (WP-02, wave 0)

```python
def clopper_pearson(k: int, n: int, alpha: float = 0.05, side: Literal["upper", "two"] = "upper") -> float | tuple[float, float]
def is_cp_upper(weights: F64, events: B, alpha: float = 0.05) -> float        # importance-sampled; Kish-effective n
@dataclass class BootstrapResult: mean: float; se: float; lcb: float; ucb: float
def paired_bootstrap(diff: F64, *, n_boot: int = 2000, block: int | None = None, level: float = 0.95, seed: int = 0) -> BootstrapResult
def holm(pvalues: Sequence[float], alpha: float) -> tuple[bool, ...]
class AlphaInvesting:                                  # decaying-memory generalized α-investing (ARCH §7.7)
    def __init__(self, w0: float = 0.05, payout: float = 0.05, decay: float = 0.9) -> None: ...
    def test(self, p: float) -> bool: ...
    @property
    def wealth(self) -> float: ...
def expected_max_z(n_eff: int) -> float                # E[max of n iid N(0,1)] ≈ 2.746 at N = 200 (BLdP approximation 2.766); feeds DSR's SR₀
def max_z_quantile(n_eff: int, q: float = 0.95) -> float   # q-quantile of that maximum ≈ 3.474 at N = 200: the deflation hurdle (SYN §5.4)
def deflated_sharpe(sr: float, n_eff: int, t_obs: int, skew: float, kurt: float) -> float   # uses expected_max_z
def pbo_cscv(perf: F64, n_blocks: int = 8) -> float    # perf [n_trials, n_obs]
def mde(se: float, alpha: float = 0.05, power: float = 0.8) -> float
def deflated_improvement(delta_psi: float, se: float, n_eff: int, q: float = 0.95) -> float   # ΔΨ̂ − SE·max_z_quantile(n_eff, q)
def cvar(x: F64, alpha: float, w: F64 | None = None) -> float
def bpoe(x: F64, threshold: float, w: F64 | None = None) -> float   # buffered probability of exceedance (S-ADR-07)
# ce.py (§1.2)
def j_to_ce_wealth(J: float, gamma: float, lambda_T: float, shortfall_exponent: float, target_rel: float) -> float
def delta_ce_bp(J1: float, J0: float, obj: "ObjectiveSpec", years: int = 10) -> float
def h_delta_ce_bp(delta_obj: float, marginal_utility_wealth: float, years: float = 3.0) -> float
def usd_m_per_bp_year(w0_bn: float) -> float           # 17.7 at W₀ = 177
```

**Tests.** `statistical/test_cp_coverage.py` (nominal ≥ 95% coverage on Bernoulli(p) for p ∈ {0.005, 0.01, 0.02}, n = 50k; at n = 50k, p̂ = 0.90% passes a 1% gate and 1.00% fails: ARCH §5.10); Holm and α-investing control FWER/mFDR ≤ nominal on 2,000 synthetic null campaigns; `expected_max_z(200)` within 0.02 of 2.746 and `max_z_quantile(200)` within 0.02 of 3.474 (BUILD-20); bPOE ≥ POE and bPOE(CVaR_α threshold) = 1 − α (property); `j_to_ce_wealth` inverts the objective to 1e-10.

---

### 4.5 `testing` (WP-03, wave 0)

**Purpose.** Fixtures and fakes so every stream builds against frozen tensors before the real engines exist (ARCH §3.4).

```python
def mini_book(allocation: AllocationId = "v2", *, seed: int = 7) -> BookSnapshot   # one unit per private group × age bucket, 3 HF lots,
                                                                                    # 2 long-only, 3 treasury sleeves, small overlay policy book; SYNTHETIC
def mini_cube(n_paths: int = 200, world: WorldId = "M1", *, seed: int = 7) -> ScenarioCube   # 2-regime Gaussian factors, real factor names; not scen
def mini_flowcube(book: BookSnapshot, cube: ScenarioCube) -> FlowCube
def fixture_tree(branching: tuple[int, ...] = (2, 2, 2), *, unreduced: bool = True) -> Tree   # one path per node
def fake_engines(book: BookSnapshot) -> list[AssetEngine]      # deterministic linear engines with closed-form flows
class FakeLedger(Ledger): ...                                  # honours the Protocol; identity-exact
def fake_beliefs(book: BookSnapshot) -> BeliefSet
def golden(name: str) -> Any
def assert_manifest_reproduces(manifest_path: Path) -> None    # re-runs a manifest, compares canonical artifact hashes (§4.1)
def fixture_h() -> tuple[LPModel, HSolution, DualSet, Tree]    # fixture_h.py: from the gap_02 coefficient export, so WP-16/19/20/23 test
                                                               # against H outputs before WP-18 lands (BUILD-21)
def fake_filter(params: StressFilterParams | None = None) -> Callable[..., F32]   # stand-in for state.simulate_filter (WP-06 before WP-07)
def fake_owner_draws(cube: ScenarioCube, rate: float = 0.075) -> ScenarioCube   # stand-in for owner.attach_draws
def fake_belief_draws(bs: BeliefSet, world: WorldSpec, n_paths: int) -> BeliefDraws   # α frozen at α̂ (the no-learning variant)
def synthetic_committee(register: Register, seed: int) -> "SyntheticCommittee"   # committee.py: seeded pre-votes and ballots labelled
                                                               # SYNTHETIC; refused in REAL mode (RunModeRefused; S-ADR-37)
```

**Walking skeleton** (`tests/skeleton/test_walking_skeleton.py`, owner WP-03; the gate for tagging `contracts-v1.0`, BUILD-11): calls every Protocol method of §3.17 and every cross-WP function named in §4 once, end to end on `mini_book` with the fakes above: engine `init` with `BeliefDraws` → `recourse_quotes` → `step` → `Ledger.apply` → `apply_recourse` → P on 200 paths → tree → `fixture_h` → `phase2` → `price` → `select` → `project` → evaluator client → `RoomPort`; it asserts types, shapes and units against `ARRAY_SPECS` and fails on any signature drift.

**Definition of done.** Golden checksums of `mini_cube()`, `mini_flowcube(mini_book(), mini_cube())` and `fixture_tree()` committed in `tests/golden/frozen_fixtures.json` at the end of Wave 0; the walking skeleton green; any later change requires the contract-change note (§0.1).

---

### 4.6 `registry` (WP-04, wave 0)

**Purpose.** Append-only, hash-chained run/metric/claim/forecast-score/decision store (SQLite in WAL mode + Parquet/NPZ artifacts under `runs/`).

```python
class Registry:
    def __init__(self, db_path: Path, artifact_root: Path, *, readonly: bool = False) -> None: ...
    def begin_run(self, manifest: RunManifest) -> RunId: ...
    def end_run(self, run_id: RunId, status: Literal["OK", "FAILED", "ABORTED"], error: str | None = None) -> None: ...
    def put_artifact(self, run_id: RunId, name: str, obj: BaseModel | ArrayContainer | pa.Table | bytes) -> ArtifactRef: ...
    def get_artifact(self, ref: ArtifactRef | str) -> Any: ...
    def define_metric(self, d: MetricDef) -> None: ...            # new id on any definition change; MRM approval flag
    def put_metrics(self, ms: Sequence[MetricInstance]) -> None: ...
    def get_metric(self, metric_id: MetricId, *, run_id: RunId | None = None, plane: EvidencePlane | None = None,
                   by: Mapping[str, str] | None = None) -> MetricInstance: ...
    def list_metrics(self, *, run_id: RunId | None = None, prefix: str | None = None) -> list[MetricInstance]: ...
    def append_ledger(self, kind: Literal["eval_request", "eval_record", "llm_call", "budget", "escalation",
                                          "assumption", "seal", "drill"], payload: BaseModel) -> str: ...   # returns row hash
    def verify_chain(self) -> "ChainReport": ...
    def put_claim(self, c: ClaimRecord) -> None: ...
    def append_decision(self, d: DecisionRecord) -> None: ...      # validates prev_hash / record_hash
    def get_provenance(self, ref: ArtifactRef) -> ProvenanceNode: ...
    def mfdr(self) -> "MFDRLedger": ...                            # S-ADR-18
```

**Algorithm.** Each ledger row stores `prev_hash` and `row_hash = sha256(prev_hash ‖ canonical_json(payload))`; SQLite triggers raise on UPDATE or DELETE of any registry table. One writer per process (file lock); readers unlimited.
**Performance.** `put_metrics` ≥ 10,000 rows/s; `verify_chain` on 1M rows < 60 s.
**Tests.** Tamper drill (edit a row with sqlite3 → `verify_chain` reports the first bad row); UPDATE/DELETE rejected; artifact round trip with checksum; metric definition change creates a new id; decision chain broken → error.

---

### 4.7 `data` (WP-05, wave 1)

**Purpose.** Bitemporal store, schemas, freeze-and-hash, taint, quarantine, adapter base (real-data adapters are WP-37).

```python
SCHEMAS: Mapping[TableName, pa.Schema]   # derived from contracts models; metadata: unit, data_class, is_synthetic, version
TableName = Literal["holding", "cashflow", "mark", "milestone", "forecast", "quote", "hf_terms", "loan", "facility",
                    "owner_draw", "overlay_trade", "crif_row", "csa", "service", "company", "sponsor", "claim_edge"]
class BitemporalStore:
    def __init__(self, root: Path, data_class: DataClass) -> None: ...   # one store per data class
    def upsert(self, table: TableName, rows: pa.Table, *, recorded_at: datetime) -> int: ...
    def as_of(self, table: TableName, valid_at: date, known_at: datetime) -> pa.Table: ...
    def tables(self) -> tuple[TableName, ...]: ...
def freeze(store: BitemporalStore, asof: date, known_at: datetime, tax: GroupRegistry, *,
           allocation: AllocationId | None, census_id: CensusId | None) -> BookSnapshot
def save_snapshot(snap: BookSnapshot, path: Path) -> str; def load_snapshot(path: Path, expected_hash: str | None = None) -> BookSnapshot
def taint(*classes: DataClass) -> DataClass                               # raises DataClassMixError on a mix
class SourceAdapter(Protocol):
    source_id: str; table: TableName
    def read(self, raw: Path) -> pa.Table: ...
    def validate(self, t: pa.Table) -> "AdapterValidation": ...            # unknown fields or units -> quarantine rows
def run_adapter(adapter: SourceAdapter, raw: Path, store: BitemporalStore, quarantine_root: Path) -> "AdapterReport"
```

**Semantics.** A row is visible at (valid_at, known_at) iff valid_from ≤ valid_at < valid_to (open-ended if null) and recorded_at ≤ known_at; the latest recorded version per key wins.
**Invariants.** A store never accepts rows of the other data class; snapshots record the store's data class; `freeze` output hashes identically for identical inputs.
**Tests.** Property test of as-of semantics (hypothesis over random version histories); mixing raises; quarantine on an unknown column or unit; snapshot round trip; taint truth table.

---

### 4.8 `owner` (WP-08, wave 1)

**Purpose.** The exogenous owner draw (Mode B) and owner-proposal machinery (Modes A/H) (ARCH §4.3; S-ADR-14).

```python
class OwnerConfig(BaseModel):                      # defined in contracts.world (§3.18); fields normative here
    c: float = 0.075; b: float = 0.625; rho_d: float = 0.5
    override_p_a: dict[ShockType, float]           # 0.0025 (N, B, SS), 0.01 (SG, DB), 0.02 (GW)
    hydro_share: tuple[float, float] = (0.113, 0.091); breakeven_median: float = 55.0; breakeven_p05_p95: tuple[float, float] = (45.0, 70.0)
    gw_wedge_pp: tuple[float, float] = (-5.0, 2.0); fiscal_noise_sd_pp: float; ref_price: float
    basis: Literal["opening_fy_reported_nav", "fixed_usd", "current_nav"] = "opening_fy_reported_nav"
    mode: MandateMode = MandateMode.B_OWNER_CALL
    band_floor: float = 0.05; p_accept_band: dict[ShockType, float]   # DB: 0.30 [I], others 1.0 (Mode H only)
    domestic_obligation_bn_a: tuple[float, float] | None = None       # Mode H only
def fiscal_need(cube: ScenarioCube, cfg: OwnerConfig, base: bytes) -> F32                 # [P, Y] FN_y in pp
def draw_rates(fn: F32, cube: ScenarioCube, cfg: OwnerConfig, d_prev: float, base: bytes) -> tuple[F32, B]   # rates, override flags
def attach_draws(cube: ScenarioCube, cfg: OwnerConfig, d_prev: float, base: bytes) -> ScenarioCube   # new cube with draw_rate set
# instalment_bn is contracts.rules.instalment_bn (one copy for owner, ledger, priv and H; BUILD-25): the annual payout is ≥ max(5% of B_y,
#   owner call) and ≤ 10% of B_y, and each quarterly instalment is the remaining annual amount ÷ instalments left (QUANT-25)
def kink_pairs(cfg: OwnerConfig) -> dict[Literal["linear", "log"], tuple[float, float]]               # Brent at the 5% and 10% kinks
class PayoutRule(Protocol):
    name: str
    def rate(self, state: "OwnerRuleState") -> F64: ...
PAYOUT_LIBRARY: Mapping[str, PayoutRule]   # R12_PAYOUT_MATCHED, POMV, YALE_80_20, TWO_KEY, SURPLUS_BARRIER (OWNER_PROPOSAL only)
```

**Algorithm.** FB^pre_y = 100 h_y (P̄^eff_y q̄_y − P^BE_y)/P^ref + w_{Z_y} + ε_y; FN_y = −FB^pre_y; d^tgt_y = Π_[5%,10%](c + b·FN_y); d_y = Π(ρ_d d_{y−1} + (1 − ρ_d) d^tgt_y); an override (annual probability by Z) resets the year's remaining instalments to 10% [I]. Mode H: in event-stage Red or macro crisis the band floor of 5% applies if accepted (Bernoulli p_accept_band[Z]).
**Invariants.** Mode B exposes no decision variable (there is no function that takes an action and returns a draw); rates in [5%, 10%].
**Tests.** Kink pairs ≈ $67/$23 (linear) and $64/$31 (log) within $1 (golden, SYN §4.7); 12-month draw at the SYNTHETIC as-of in $9.9–10.8bn and P(2027 rate ≥ 9.5%) = 1.2% ± 0.5pp on 50k paths (regression, gap_04 §6.2); recovery of (c, b, ρ_d) within V17 bands from 200 synthetic histories; `unit/test_mode_b_has_no_payout_lever.py`.

---

### 4.9 `state` (WP-07, wave 1)

**Purpose.** Stress filter, F_t, exit and shock nowcasts, the frozen initial state, the 12-row panel and the walk-forward harness (ARCH §4.2; gap_04).

```python
# StressFilterParams is defined in contracts.world (§3.18); state produces it
def fit_stress_filter(panel: pd.DataFrame, end: date) -> StressFilterParams        # hmmlearn GaussianHMM(3, "full"); labels anchored on crisis vol
def forward_filter(params: StressFilterParams, x: F64) -> F64                      # [T, 3]; forward recursion only
def fit_fragility(post_crisis: F64, dd3: B, *, purge_months: int = 3, embargo_months: int = 3) -> tuple[float, float]
def fragility(post_crisis: F64, ab: tuple[float, float]) -> F64                   # F = σ(a + b·logit π̂^c)
def simulate_filter(factors: F32, factor_names: Sequence[str], params: StressFilterParams, panel_tail: F64) -> F32   # [P, M, 3]; reads
                                                                                    # the filter's own observables from the cube: us_eq − short_rate,
                                                                                    # log_rv, ebp lagged one month, Δust10y (S-ADR-35; BUILD-14)
def exit_filter(dist_rates_a: F64, prior: F64, sigma: float = 0.15) -> F64         # interim e0 filter (4 states)
def nowcast_shock(inputs: "ShockNowcastInputs", prior: F64) -> tuple[F64, bool]     # Z0 posterior, disagreement alarm
def initial_state(inp: "InitialStateInputs", params: StressFilterParams, owner_cfg: OwnerConfig) -> StateSnapshot   # 7-step procedure
def build_panel(state: StateSnapshot, cfp: CFPReading, metrics: Mapping[MetricId, MetricInstance]) -> StatePanel
def harness(panel: pd.DataFrame, signals: Sequence[str], targets: Sequence[str], cfg: "HarnessConfig") -> "HarnessReport"   # Holm, both halves
```

**Invariants.** No look-ahead: appending future rows never changes past posteriors (metamorphic test). P recomputes F_t from simulated observables with the frozen filter; nothing reads the true S_t.
**Tests.** On the copied public panel (`data_public/monthly_panel_v1.csv`): F_t at end-Sep 2026 = 0.10 ± 0.02 against a 0.17 base rate; e0[D] = 0.87 ± 0.03 (regression, gap_04 §4.2, §6.2); reliability bins reported; harness reproduces gap_04's Holm decisions on its 12 primary tests; `simulate_filter` is deterministic and, fed the historical panel's own columns, reproduces `forward_filter` to 1e-12 (BUILD-14); `exit_filter` run per path on simulated PE distribution rates equals the interim e₀ filter on the same inputs (the observables producer of §4.19).

---

### 4.10 `scen` (WP-06, wave 1; M2–M5, B2, misspecification in WP-31)

**Purpose.** Engine E and the second families (ARCH §4.1).

```python
def load_world(world_id: WorldId, config_dir: Path | None = None) -> WorldSpec
def build_cube(world: WorldSpec, state0: StateSnapshot, n_paths: int, plane: Plane, base: bytes, *,
               filter_params: StressFilterParams, path_offset: int = 0, months: int = 120) -> ScenarioCube
def regenerate(meta: CubeMeta, world: WorldSpec, state0: StateSnapshot, filter_params: StressFilterParams) -> ScenarioCube
def verify_cube(cube: ScenarioCube, expected_checksum: str) -> None                 # HashMismatch
def anchor_check(world: WorldSpec, n_paths: int = 50_000, root_seed: int = 0) -> "AnchorReport"   # E[Σ log(1 + r)] over 10 years within 5bp;
                                                                                    # annualized vols and correlations vs the world's CMA
def calibrate_world(panel: pd.DataFrame, cma: Mapping[str, CMALine], cfg: "CalibConfig") -> WorldSpec   # offline; fits the factors that have
                                                                                    # history, verifies the rest ("set_and_verified"); YAML + report
def monthly_shock_matrix(P_annual: F64) -> tuple[F64, float]                        # principal 12th root with repair; (P_m, repair error)
def asset_class_map(book: BookSnapshot) -> dict[UnitId, str]
```

**Algorithm (E).** (1) Regimes: macro S as a state-expanded HMM (k dwell sub-states per regime: negative-binomial dwell), exit e semi-Markov, shock Z with the monthly matrix P^Z_m = the principal 12th root of the annual P^Z_a (`monthly_shock_matrix`: `scipy.linalg.fractional_matrix_power`, negative entries clipped, rows renormalized, repair error logged; v1.0's linearization I + (P^Z_a − I)/12 kept the stationary shares but overstated 12-month persistence by up to 15pp, QUANT-29), coupled to S by κ; initial states sampled from π₀, e₀, z₀ (source `scen.init`); GW dwell conditioned on elapsed duration. (2) Factors f_t = c_S + A f_{t−1} + D_S L_S ε_t with ε = √((ν − 2)/ν)·t_ν, ν = 5, unit variance (`rng.samplers.student_t(standardize=True)`; unscaled t₅ variates have variance 5/3 and inflated every factor vol by 29%, QUANT-21); R_s = (1 − ω_s)R₀ + ω_s R_crisis repaired by `nearest_correlation`; LEVEL factors evolve from `StateSnapshot.factor_levels0`. (3) CMA anchoring of intercepts precomputed in `WorldSpec`, root-found so each asset's expected 10-year log return E[Σ log(1 + r)] matches the CMA geometric mean converted from `arith_mean_a` and `vol_a` (lognormal conversion) within 5bp; E[exp Σ r] is never the anchor, because it is undefined under t₅ log returns. (4) Asset returns r_a = a_{a,S} + b_a′f + σ_{a,S}u. (5) Two-factor oil from the futures curve (χ₀ = ln spot − ln front). (6) Vol states (β(T) = 0.94(T/30d)^−0.43; MOVE; OVX by Z) live only in `ScenarioCube.vol`; the factor `log_rv` follows a regime-dependent log-vol AR(1) linked to `log_vix30` by a VIX–realized spread. (7) `fin_window` from the HY-spread and EBP levels (config thresholds). (8) `crowding_index` from `sec_discount` and `hy_spread` (S-ADR-13). (9) `stress_post` by `state.simulate_filter` on the cube's own `us_eq`, `short_rate`, `log_rv`, `ebp` and `ust10y`, the observables the frozen filter was fitted on (BUILD-14).
**Calibration provenance** (S-ADR-35; BUILD-02). The only monthly market history on disk is the 23-column gap_04 panel (1963-07 to 2026-08: US equity excess return, rf, log realized vol, 10-year yield, EBP and derived series) plus quarterly Brent from 2002. `calibrate_world` fits c, A, D, R₀ and R_crisis only for factors with history there; every other parameter ships as [I] configuration with `provenance = "set_and_verified"`, checked against the SYN §7.1 targets, and no claim calls it "fitted".
**B1:** stationary block bootstrap (12–24-month blocks) of the panel 1990–2015 with a 12-month embargo, resampling the panel's observed columns (`BootstrapParams.observed_factors`); every other factor is drawn from E's conditional model given the resampled block (`fill = "conditional_e"`), listed in `CubeMeta.proxy_factors` and labelled PROXY wherever a claim uses it; latent chains are replaced by frozen filters' posteriors on the resampled observables. **B2:** filtered historical simulation on 2017–2026 with the same fill rule; constructible only with `plane == FINAL` (else `SealBreach`). E, the stress filter and F_t are calibrated on data through 2026, so by default (`PlaneSpec.b2_mode = "family_holdout"`) Gate 3 and every claim call B2 a **model-family hold-out**, not out-of-time evidence; `"out_of_time"` requires E's dynamics, the filter and F_t recalibrated through 2015 with the 12-month embargo (QUANT-19). WP-41 (wave 6; a human with network access) snapshots the missing public series, after which B1 and B2 drop their fills.
**Factors** (`scen/factors.yaml`; each factor declares its kind, mirrored in `CubeMeta.factor_kinds`; BUILD-37). **v1, K = 20:** `logret`: us_eq, intl_eq, em_eq, usd, cpi, brent_log; `level`: short_rate, ust2y, ust10y, ig_spread, hy_spread, ebp, log_rv, brent_slope, exit_X, sec_discount, navloan_spread, pc_loss_index, ra_caprate, infra_discount. Implied vols (`log_vix30`, `log_move`, `ovx`) are not factors; they live once, in `ScenarioCube.vol`. **Increment 1, K = 8:** us_eq, short_rate, ust10y, hy_spread, ebp, log_rv, brent_log, exit_X (the filter's observables plus the drivers of the financing window, oil and the exit chain); the other twelve are deterministic CMA-mean paths flagged in `CubeMeta` until WP-31 (S-ADR-37).
**Performance.** ≤ 2.5 s per 10,000 paths × 120 months on one process with the tabulated inverse CDFs of §4.2 (PD measured 2.3 s [M]; `scipy.special.stdtrit` alone would take 4.6 s per cube [M]): B9 and the B1 "scenario cube" line.
**Tests.** `anchor_check` within 5bp on E[Σ log(1 + r)] for every CMA line of M1 and M6 (MVP) and M1–M6 (v1); annualized vols within ±0.5pp and correlations within ±0.05 of each world's CMA (QUANT-21); `test_monthly_shock_matrix` (P^Z_m to the 12th power reproduces P^Z_a to 1e-6 where the principal root is non-negative, otherwise the logged repair error is ≤ 0.01; QUANT-29); drought-persistence share of paths with e ∈ {D, F} for ≥ 4 years in 12–15% ± 3pp (SYN §7.1); dwell medians inside 6–18 months (crisis) and 36–60 (expansion); oil–equity correlation signs by era; every factor's stored kind matches `factors.yaml` and spreads stay levels (BUILD-37); cube checksum reproducible across blocks and processes; B1 draws no month inside the embargo and lists its PROXY factors in `CubeMeta`; B2 on SEARCH raises; `calibrate_world` marks every unfitted parameter `set_and_verified` (BUILD-02).

---

### 4.11 `priv` (WP-09 fund + real assets; WP-10 company, claims, credit, overlap; wave 1)

**Purpose.** Cash flows, economic and reported NAV, unfunded balances and credit states for every private unit, with exact per-action counterfactual flows on CRN (ARCH §4.4; GROUPS §3).

```python
class FundEngine:        engine_id = "priv.fund";       clock = Clock.QUARTERLY   # implements AssetEngine
class CompanyEngine:     engine_id = "priv.company";    clock = Clock.QUARTERLY
class ClaimsEngine:      engine_id = "priv.claims";     clock = Clock.QUARTERLY   # Capital Solutions families A–G
class CreditEngine:      engine_id = "priv.credit";     clock = Clock.QUARTERLY   # Private Credit loan cohorts + wrappers
class RealAssetsEngine:  engine_id = "priv.realassets"; clock = Clock.QUARTERLY   # interim (S-ADR-02)
def load_templates(tax: GroupRegistry, config_dir: Path | None = None) -> "PrivTemplates"
def bid_fraction(group: GroupId, unit_kind: str, age_years: float, regime: MacroRegime, exit: ExitWindow,
                 size_bn: float, templates: "PrivTemplates") -> float          # hedonic cash-equivalent bid ÷ economic NAV
FundEngine.mean_path(self, unit: Holding, exit_path: Sequence[ExitWindow], quarters: int) -> "MeanPathFlows"   # history fit, Phase-I slopes
def build_overlap(params: "OverlapParams", tax: GroupRegistry, base: bytes) -> OverlapGraph
def check_v24(graph: OverlapGraph, book: BookSnapshot, params: "OverlapParams") -> "GateReport"
# Every engine implements AssetEngine (§3.17), including recourse_quotes and apply_recourse (S-ADR-29).
class UnitFinancingBook:                                   # priv/financing.py; owns every unit's UnitFinancing (BUILD-24)
    def draw(self, st: EngineState, unit_ids: Sequence[UnitId], amounts_bn: F64, instrument_ids: Sequence[str]) -> None: ...
    def step(self, st: EngineState, t: int, nav_rep: F32) -> F32: ...   # [P, U_f, 3]: DEBT_SERVICE, DEBT_REPAY (incl. forced paydowns), breach flag
```

**Algorithms** (defaults [I] in `config/groups/*.yaml`, sources as cited):

| Engine | Equations |
|---|---|
| Fund (RFT-TA v2) | Economic NAV log return per quarter: r_f,q + β_i(R^eq_q − r_f,q) + γ_iΔcs_q + α_{i,path,q} − ½σ_id²Δ + σ_id√Δ z_i + J_i, with α from `BeliefDraws.alpha0_q` (received through `init`; the engine adds only the benchmark-relative α to the world's beta return, never a total return, S-ADR-28), updated by α_{t+1} = m + φ(α_t − m) + η_t (SYN §4.3). Effective age a^e_{t+1} = a^e_t + κ(e_t)Δ, κ = 1.2/1.0/0.6/0.5. Calls C = (1 − e^{−λΔ})U, λ = λ̄_s(a)·m^C(e)·e^{u}, λ̄ from the 20/25/30/35/40% schedule, m^C = 1.3/1.0/0.975/0.8; stressed calls λ(U − B^SL) + c^SL B^SL. Distributions D = (1 − e^{−δΔ})Ve^{r}ζ, δ = δ̄_s(a^e)·m^D(e)·Φ·exp(κ^D X_t + ς_s(q) − θ_G G + u), m^D = 1.25/1.0/0.475/0.325, G = ln N − ln V. Reported NAV r^N_t = (1 − λ_s)r_{t−ℓ} + λ_s r^N_{t−1} + η_t (buyout AC1 0.66–0.71). G1 mechanics: subscription lines, GP NAV loans, GP-triggered CV offers (exogenous events), extensions with fee step, buyer assumes unfunded, recycling ≤ 110%, fees inside net flows. Secondaries templates S1 (calls 45% a year of remaining unfunded for 4 years), S3 (V₀ = θN^ref), S4/S5 on the company engine. RA closed-end: RA template with income distributions y_inc·V each quarter plus exit distributions |
| Company (EV) | ln(V_{t+Δ}/V_t) = (α − ½σ²)Δ + β_A r_m + σ√Δ ε + ΣJ (Kou); E = max(V − D, 0); write-off at V ≤ κD; hazard h₀e^{b(ICR* − ICR)+}; Weibull exits (k 1.447, η 7.70 y) × 1.3/1.0/0.5/0.3; GP-triggered recaps (post-recap distress ×2.0); marks M_{t+Δ} = λM_t + (1 − λ)E_{t−Δ} + b_g + e_t. EV draws keyed by `company_id` (source `priv.company.ev`) for every company with a direct ADIC equity or claim position (co-investments, Secondaries CV stakes, Capital Solutions C/D/E, and Private Credit loans in the recap-netting set) |
| Claims (Capital Solutions) | States {PERFORMING, PIK, AMENDED, EXTENDED, DEFAULT, WORKOUT, REPAID}; accrual q = CrΔ, cash q(1 − a), C ← C + qa, a ≤ ā(age); NAV loans B_{t+1} = B_t + (I_t − D_t)+ − σ(ℓ_t)(D_t − I_t)+ on the borrower's reported NAV; redemption max{κC, m_min I₀ − Σcash, MW}; PIK share 15/30/60–80/20%, default 1.0/2.5/6–8/1.5%, recovery ×1.0/0.9/0.7/1.0 (EXP/LATE×D/CRIS/RECV); kickers via the company payoff |
| Credit (Private Credit) | Cohort shares over {PERFORMING (cash-pay), PIK, NONACCRUAL, RESOLVED, REPAID}; h^def = φΦ(−ln ICR̄/σ_ICR)ξ_t e^{β′x}; separate PIK, extension (0.2/0.3/0.5/0.6) and loss hazards; stochastic CPR; DDTL draws 15/20/30/60%; evergreen proceeds E[min(1, c̄ NAV/ΣR)]R_ADIC; LGD 0.67, PD_N 1.1% (×1.5 drought, ×3 crisis), GC1 pair as a truth variant; PIK-cohort hazard ×1.3–1.7; LGD by collateral type and evergreen units at 0 Tier-1 liquidity (S-ADR-11); SMA run-off switch ρ |
| Real assets (interim) | Core/open-end/direct: ln V_{t+Δ} − ln V_t = Δln NOI − Δln k_t + ε_i, Δln NOI = (g₀ + π_pass·π_t)Δ + β_oil·Δln Brent·1{sector = ENERGY_NATRES} + σ_NOI√Δ z, k_t = k̄_sector + β_k(ra_caprate_t − mean); cash income = k_t V_tΔ − maintenance capex − debt service; reported NAV Geltner N_t = (1 − λ_G)V_{t−ℓ} + λ_G N_{t−1}; development calls on an S-curve over committed capex; asset debt: DSCR = NOI/debt service, cash sweep below the covenant, refinancing at maturity at the regime spread and LTV cap, cash-in cure or (non-recourse) hand-back if LTV_max·V < D; open-end units run `pub.queue.RedemptionQueue`. Closed-end RA funds run on FundEngine with the RA template |

**Couplings** (G-gap_04 §1.2): co-investment offered flow O_t = θ Σ_{j=0}^{19} ¼ d_{⌊j/4⌋} C^PE_{t−j}, with d per year over 20 quarters (§3.2; v1.0's five-quarter kernel compressed the PE → co-investment lag four-fold, QUANT-28), computed on simulated PE commitments; one GP effect per path shared by PE funds, co-investments and Secondaries with the same GP (`BeliefDraws.gp_effect_q`, ρ_GP = 0.6, only along graph edges: V24d).
**Recourse and unit financing** (S-ADR-29; BUILD-01, BUILD-24). `recourse_quotes(t, …)` publishes for every recourse-eligible unit the cash-equivalent bid (`bid_fraction` with the crowding haircut on `ScenarioCube.crowding_index`), the normal-regime hedonic bid (red test (iii)), the depth cap, the settlement lag and the tier. `apply_recourse` scales the sold fraction out of the unit's NAV, unfunded commitment (the buyer assumes it) and financing balance before t + 1. Engines never book recourse proceeds and never set a red flag; the ledger does both. `UnitFinancingBook` carries the balances that REFINANCE and LEVER create: accrual, debt service and amortization each quarter, an LTV covenant on lagged reported NAV, and a forced paydown when it breaches, emitted as DEBT_DRAW, DEBT_SERVICE and DEBT_REPAY flows; the ledger adds the balances to look-through leverage.
**Invariants.** (P-H) flows are positively homogeneous of degree 1 in the fraction held; economic NAV roll-forward V_{t+1} = V_t e^{r} − calls·(−1) − distributions holds to 1e-10 per unit; equity ≥ 0 on non-recourse RA assets; `column_flows(unit, HOLD)` equals the baseline unit flows bit for bit; a fraction sold by `recourse_cover` produces no later flow and conservation holds across the sale.
**Performance.** All private engines ≤ 12 s per 10,000 paths × 40 quarters at asset level on one process (v2 book ≈ 375 private units + ≈130 company paths).
**Tests.** Call schedule reaches ≈90% called by year 6 in N (±3pp); V5 DPI by age, V6 distribution/contribution rates vs MSCI ±2pp on the decision census, V7 exits above prior mark 0.70–0.80, V8 buyout AR(1) 0.66–0.71, V12 Private Credit regime-weighted loss 0.8–1.2%, co-investment P(MOIC < 1) 0.35–0.40 (all `regression/test_priv_stylized.py`); homogeneity and roll-forward (property); `test_company_draw_identity_v24a`; RA: Geltner AC1 within ±0.05 of λ_G, LTV-breach path produces a cure outflow or hand-back with equity floored at 0, oil beta sign in ENERGY_NATRES; per-lens `test_lever_equals_add_plus_refi` hooks via `column_flows`; `test_engine_mean_log_return_by_world` (for every world, each engine's mean log return per unit equals r_f + β·ERP_world + ᾱ − ½σ² within MC error on 50k paths, so beta is never counted twice and the six worlds move asset returns; QUANT-02); `test_recourse_sold_unit_flows_zero` (after `apply_recourse` a sold fraction's distributions, calls and NAV are zero; BUILD-01); `test_unit_financing_breach_paydown` (an LTV breach forces a paydown; balances reach the ledger's look-through leverage; BUILD-24). The SYN §7.1 stylized fact "central path ≈ 7.7% ten-year endowment outcome" on M1 (§6.9) is the integration gate for the belief wiring.

---

### 4.12 `pub` (WP-11, wave 1)

**Purpose.** Hedge-fund liquidity-term state machine, long-only sleeves, P2S economics and the generic redemption queue (ARCH §4.5; gap_01 §5).

```python
class HFEngine:        engine_id = "pub.hf";       clock = Clock.MONTHLY
class LongOnlyEngine:  engine_id = "pub.longonly"; clock = Clock.MONTHLY
class RedemptionQueue:                                     # generic; also used by RA open-end funds
    def __init__(self, terms: Sequence[HFTerms | "OpenEndTerms"], n_paths: int) -> None: ...
    def step(self, m: int, notices: F32, nav: F32, regime: I8, u: Mapping[str, F64]) -> tuple[F32, F32]: ...   # (cash paid, holdback)
def phi_table(lots: Sequence[Holding], regime: MacroRegime, base: bytes, *, horizons_m: Sequence[int] = (3, 6, 12, 24),
              n_sims: int = 2000, quantile: float = 0.05) -> F64                     # [L, H] P5 cash share; the only ladder interface;
                                                                                     # GroupRates.hf_phi is a lookup of this table by the path's
                                                                                     # regime, never a nested simulation (BUILD-40)
def impact_cost(q_bn: F64, adv_bn: F64, sigma_d: F64, *, Y: float, half_spread: float, tax: float) -> F64
def p2s_cost_a(regime: MacroRegime, fin_window: FinWindow) -> float               # per $ freed a year (0.40–0.70% normal …)
```

**Algorithm.** Lot states {LOCK, SOFT, OPEN, NOTICE, QUEUE, SUSP, PAY, SP, LIQ, DONE, TRS_TERM}. At each dealing date: other investors' requests R^oth = NAV·clip(ρ_S + ρ₁[−r^rel]+ + ρ₂1{p̂^gate > p*}); a gate if requests exceed gNAV (always if mandatory, else a logit hazard on regime, drawdown, flows, mismatch, leverage); payout min(1, gNAV/R) only when gated; liquidation 50/30/20% by months 3/12/36; cash (1 − h)·Pay after the payment lag. ADIC notices only on notice dates, irrevocable unless `notice_revocable`. HF returns: r = r_f + β_S′F + γP + α + σ_Sε + J with fund-level smoothing θ₀ ≥ 0.5. Long-only: r = r_b + (β − 1)(r_b − r_f) + α + TE·ε. In both, α is the unit's benchmark-relative draw from `BeliefDraws.alpha0_q` (S-ADR-28). Long-only sleeves (impact-cost bids) and HF lots (queue payouts through φ) publish `RecourseAvailability` for the liquid rung; RA open-end units publish theirs for the amber rung through `RedemptionQueue`.
**Performance.** HF machine, long-only sleeves and queues ≤ 3 s per 10,000 paths × 120 months on one process (the B1 "public" line).
**Tests.** Port of `research/addenda/gap_01_calcs/hf_ladder.py` fixtures: ≈$4.9bn of HF cash within 90 days (static buckets) and $10.7bn by month 6 under the machine on the allocation-v1 fixture book (±$0.1bn); P5 and P50 differ by ≤ 1 month; notices on non-dealing dates rejected; gate payout identity; impact cost golden values.

---

### 4.13 `overlay` (WP-12 Level 1, VM, SIMM-like core, limits; WP-32 Level 2; wave 1)

**Purpose.** The position layer for the tail, opportunistic and synthetic-beta books (ARCH §4.6; gap_03; G-gap_03).

```python
class OverlayEngine:  engine_id = "overlay"; clock = Clock.MONTHLY      # implements AssetEngine
def price_trade(trade: OverlayTrade, mkt: "MarketState") -> float        # $bn; Black-76, Bachelier, SSVI closed forms (backs the `price_trade` tool)
def greeks(trades: Sequence[OverlayTrade], mkt: "MarketState") -> OverlayGreeks
def crif(trades: Sequence[OverlayTrade], mkt: "MarketState") -> tuple[CRIFRow, ...]
def vm_by_csa(mtm_bn: F64, csas: Sequence[CSA], prev_collateral_bn: F64, stress: B) -> tuple[F64, F64, F64]   # transfer, collateral, in-transit
def simm_like(rows: Sequence[CRIFRow], params: "SimmParams", csa_id: CsaId) -> "SimmResult"   # delta, vega, curvature by product/risk class
def nv_eq(vega_by_bucket: F64, expiries_days: F64, beta_coef: float = 0.94, beta_exp: float = -0.43) -> float
def check_ov(state: "OverlayState", stresses: Sequence["NamedStress"], policy: OverlayPolicy) -> "OVReport"   # OV1, OV2, OV3
def floor_ladder(budget_a: float, nav_bn: float, mkt: "MarketState", policy: OverlayPolicy) -> "LadderSpec"
def monetize_decision(value_bn: F64, delta: F64, premium_bn: F64, stress_label: B, vix: F64, lambda_w: F64, cont_value: F64) -> F64
def services_ledger(services: Sequence[ServiceContract], flows: F64, ftp_a: float, c_buf: float = 0.015) -> "ServicesLedger"
def tail_dva_ex_ante(trades: Sequence[OverlayTrade], kernel_values: F64) -> float
def stress_coefficients(book: OverlayBook, stresses: Sequence["NamedStress"], mkt: "MarketState") -> "OverlayStressCoeffs"   # OV1/OV2 rows in H
```

**Algorithms.** VM: C*_c = sgn(V_c)(|V_c| − H_c)+, transfer if ≥ MTA_c, T+1 (stress delay per CSA, S-ADR-15); recognition φ; posted IM encumbered. SIMM-like per CSA and product class with SIMM v2.8+2512 tables (`config/overlay/simm_v2_8_2512.yaml`): WS_k = RW_k s_k CR_k; within-bucket and cross-bucket aggregation; vega and curvature (SF(t) = 0.5 min(1, 14/t)); deferred IM step after each post-stress recalibration. Level 1: opportunistic families as exposure rules on E's observables (trend, carry, RV, short vol) with residual skill α^f = SR^post_f σ_f − E[factor P&L_f], shrunk from N(0.3, 0.25²) and DSR-gated (live ≥ 0.95, backtest-only ≥ 0.99); trend crisis beta decays after crises (S-ADR-15). Taylor P&L outside stress windows; full revaluation monthly, in daily stress sub-steps and at triggers.
**Performance.** Monthly full revaluation of the policy book, VM by CSA and SIMM-like IM ≤ 5 s per 10,000 paths × 120 months on one process (the B1 "overlay" line); Taylor P&L between revaluations (A3).
**Tests.** T1 pricing within 0.5% of vega (or 1bp) of closed-form references and put–call parity; T2 analytic vs bump Greeks within 1%; T3 explain test (Spearman > 0.80, KS < 0.09); T5 the gap_03 §7.4 position planted in one CSA breaches OV1 and OV2 while SIMM vega ≈ 0; SIMM worked example $609.7m → $418.9m (±0.5%) and offset ratio 1.77 (±0.02); 90/72 ladder cost 3.74% of notional a year (±0.10pp) at the 16-Oct-2026 market state, so the 0.15% floor buys ≈$7.1bn (±$0.4bn); reconciled S1 overlay use −$4.0bn (±$0.2bn) on the reconciled policy book (GROUPS §2.2; all SYNTHETIC); VM threshold/MTA cases; services ledger nets to zero across client/overlay/CF on DVA ledgers (V2); `test_services_entity_pnl_sums_to_external` (Σ entity P&L = external P&L for funded and unfunded services on the benign path and on S1, with CF's "external interest on collateral cash" row +r_f·C_t and C_t = N for funded services; QUANT-16).

---

### 4.14 `ledger` (WP-13, wave 1)

**Purpose.** The single kernel of cash, HQLA, IG + cash, encumbrance, facilities and payout identities shared by P, H and the T4′ stress; ladder LR1–LR8; CFP readiness/event stages (ARCH §4.9; GROUPS §2.4).

```python
class LedgerConfig(BaseModel): conventions: CanonicalConventions; cfp: "CFPConfig"; ladder: "LadderConfig"; t3_vm_stat: Literal["P99", "CVaR99"]
class LedgerKernel:                                             # implements Ledger
    def __init__(self, tax: GroupRegistry, facilities: Sequence[Facility], csas: Sequence[CSA],
                 cfg: LedgerConfig, cal: Calendar) -> None: ...
    def init_state(self, book: BookSnapshot, n_paths: int) -> LedgerState: ...
    def apply(self, m: int, ls: LedgerState, flows: Sequence[FlowSlice], draw: F32,
              quotes: RecourseAvailability) -> tuple[LedgerState, RecourseOutcome]: ...   # phase 2 of recourse; books proceeds once
    def row_slacks(self, ls: LedgerState) -> dict[RowKey, F32]: ...
    def stress_replica(self, ls0: LedgerState, stress: StressSpec) -> StressReport: ...
def instalment_draw(ls: LedgerState, draw_rate_y: F32, m: int, cal: Calendar) -> F32        # [P] ≤ 0 in instalment months; wraps
                                                                                            # contracts.rules.instalment_bn (BUILD-25)
def recourse_cover(ls: LedgerState, shortfall_bn: F64, order: I8, quotes: RecourseAvailability, m: int) -> RecourseOutcome
def red_test(sold_frac: F32, quotes: RecourseAvailability, ls: LedgerState, m: int, *, in_recourse: bool,
             red_discount_max: float, ig_target: float) -> B                               # S-ADR-30: economic substance, never the label
def build_readiness_model(ls0: LedgerState, stress: StressSpec) -> "ReadinessModel"        # per-unit-of-stock monthly NCO/CBC response vectors
def readiness_reading(ls: LedgerState, model: "ReadinessModel") -> tuple[I16, F64]          # [P] SH_TP months, min 24-month headroom (A20)
def cfp_reading(ls: LedgerState, report: StressReport | tuple[I16, F64], cfg: "CFPConfig") -> tuple[I8, I8, I8, I8]   # readiness, event, planning, playbook
def ladder_report(ls0: LedgerState, stress: StressSpec) -> "LadderReport"                    # LR1–LR8 at t0 (Treasurer panel)
def calibrate_theta_star(gap_samples: Mapping[WorldId, F64], t6_class: Mapping[WorldId, str], tolerance: Mapping[str, float],
                         grid: "GStarGrid", *, horizon_share: float = 8 / 20,
                         rule: Literal["class_banded", "prudence_overlay"] = "class_banded") -> float   # S-ADR-32
def theta_from_grid(grid: "GStarGrid", target_gap_bn: float) -> float                      # inverse of the G*(θ) grid, monotone interpolation
def leverage_metrics(ls: LedgerState, book: BookSnapshot) -> dict[str, F64]   # DBRS, repo-incl., Moody's-style, delta-adjusted, look-through
                                                                              # (incl. RA asset debt), commitment-inclusive (S-ADR-20)
# linear.py — the SAME coefficient definitions used by apply(), exported for H
def node_transition_rows(coef: "NodeCoefficients", n: int, parent: int, vidx: "VarIndex") -> "RowBlock"
def t4p_root_rows(ls0: LedgerState, stress: StressSpec, root_cols: Sequence[ColKey], fd_step_bn: float = 0.1) -> "RowBlock"
ROW_FAMILIES: Mapping[RowFamily, "RowFamilySpec"]   # role (RowRole), Phase-I tier, sign convention
```

**Algorithms.**
- *Identity* (signed flows, §1.4): L_{m+1} = L_m + Σ_external cash flows + facility draws − repayments − interest + VM received (φ-recognized, after delay) + VM paid + ΔIM + owner instalment. Intra-ADIC flows contribute zero to liquidity and must sum to zero across groups.
- *Monthly recourse (S-ADR-29; BUILD-01):* if unencumbered HQLA < max(ig_hard·W, payout due), `recourse_cover` runs the path's `recourse_order`, a permutation of the rungs reserve, P2S, liquid sales, facility (available credit only: signed, from month 2, covenant headroom, × the joint oil–crisis cap), amber sales (PC, CS, RA open-end) and red sales (PE, SEC, CO, RA; depth-capped), selling fractions of units at the bids the engines published in `RecourseAvailability` at quarter start; the ledger books the proceeds after the settlement lag, scales the sold fractions out of the units' remaining intra-quarter flows (`FlowSlice.by_recourse_unit`, exact by positive homogeneity) and returns them in `RecourseOutcome`, which the engines apply before t + 1; if still short, `payout_short`. There is **no preemptive rung**: `preemptive_raise` executes at quarter start through the policy's `ActionSlice`, outside `recourse_cover` (S-ADR-13).
- *Red test (S-ADR-30; QUANT-03):* `red_test` runs on every red-tier sale, discretionary, planned or forced, and marks it red if (i) `recourse_cover` executed it, whatever the rung; (ii) at execution the event stage ≥ AMBER or unencumbered IG + cash < `ig_target`·W; or (iii) its cash-equivalent bid < (1 − `red_discount_max`) × the unit's normal-regime bid. `red_event` and `red_month` derive from `red_test` and `payout_short` alone; `SaleReason` is a reporting label.
- *T3:* coverage = CF-controlled, Basel-capped haircut HQLA ÷ [max(look-back P95 of 30-day net collateral flows, VM statistic + ΔIM) + draws due ≤ 30 days + stressed calls − P10 distributions + debt service], facilities at 0%; the VM statistic is P99 or CVaR99 per contract (ADR-12).
- *T4′ replica:* s*(θ*) with the pricing convention set (`ConventionSets.pricing`: revolver credit 0.5 from month 2, the OV2-consistent opportunistic loss, pacing lag 2, Real Assets on `RAStressConvention`, `dist_mult` only on groups flagged `fund_distribution_stress`); the research ("as ratified") set prints as a sensitivity row (S-ADR-32; QUANT-14). NCO, CBC by tier (T ⊂ TP ⊂ TPF ⊂ TPFA ⊂ ALL), survival SH^R = min{h: NCO(h) > CBC^R(h)}, headroom hd_h on T + P + F, d₀ = max(0, −min hd_h). The APPETITE reading is `survival_months[TP] ≥ 24` with no facility credit (S-ADR-32; QUANT-09).
- *Readiness inside P (QUANT-12; A20):* under s* the stressed NCO and CBC are linear in the stocks, so `readiness_reading` computes SH_TP and the minimum headroom from `ReadinessModel` response vectors on group aggregates; the full `stress_replica` runs only for paths that leave their hysteresis band, and a nightly test compares the two.
- *CFP stages:* thresholds in `ledger/cfp_stages.yaml` (ARCH §4.9 table); planning = max(readiness, event); playbook from the event stage only; any hard trigger escalates; de-escalation needs two consecutive better readings; readiness-Red without event-Red sets the PHASE2_PLAN flag.
- *θ\* rule (S-ADR-32; QUANT-08):* θ* solves G*(θ) = the largest over T6 classes of the class's quantile of the facility-free 24-month gap at its own tolerance share: 1 − (1 − 0.01)^{8/20} = 0.40% (P99.6) for each of M1–M5 and for MIX, 1 − (1 − 0.025)^{8/20} ≈ 1.01% (≈ P99.0) for the M6 class, on pooled SAA replications (≥ 10 × 50k paths) of the decision census and allocation under the pricing conventions (B13). `rule = "prudence_overlay"` reproduces the legacy worst-model rule (M6 at 0.40%), printed with its facility ask and the cap-binding θ signpost.

**Invariants.** Conservation Δcash = Σ cash flows to 1e-10 per path-month, including across recourse sales; recourse proceeds are booked once, by the ledger; NAV ≥ 0; `playbook ∈ {RED, BLACK}` ⇒ `event ≥ RED`; `red_event` derives only from `red_test` and `payout_short`; row_slacks share RowKeys with H.
**Performance.** `apply` including recourse ≤ 2 s per 10,000 paths × 120 months (numba; the B1 "ledger and recourse" line); `readiness_reading` ≤ 0.1 s per 10,000 paths per quarter, so readiness plus `cfp_reading` stay ≤ 4 s per 10,000 paths × 40 quarters including full replicas on band exits (the B1 "readiness" line; v1.0 ran the full replica every quarter, 80 s, QUANT-12); `stress_replica` ≤ 2 s per 10,000 paths per call (t₀ ladder, θ* recalibration, band exits).
**Tests.** Port of `research/addenda/gap_02_calcs/t1_engine.py` `ladder` fixtures on the research convention set (`ConventionSets.research`): do-nothing SH_TP 17 months, minimum 24-month headroom −$11.1bn, facility need $13.9bn under s*(0.76) on gap_02's unfunded split (exact to $0.01bn / 1 month); groups gap_01 group-resolved replica: 6 readings × 8 policies exact (GROUPS §2.4); `test_readiness_red_never_fires_red_playbook`; hysteresis; VM delay reduces T3 coverage in a stress month; θ* (BUILD-36): the pooled gap samples behind 0.79 were not kept, so the test ports the 61-point G*(θ) grid and the per-model gap quantiles of `research/addenda/gap_02_calcs/gap02_results.json` and checks that `theta_from_grid` reproduces its `theta_for` values to ±0.005 (mixture P99.6 0.42; worst of M1–M5 at P99.6 0.35; M6 P99 0.58; worst model P99.6 0.76), so the class-banded rule returns ≈ 0.58 and the prudence overlay ≈ 0.76 on the fixture (SYNTHETIC); the pooled 10 × 50k recalibration is a G0 job (B13), not a unit test; `test_red_test_substance` (a red-tier sale inside `recourse_cover`, in event-Amber, below the 8% target or at a bid more than δ_max below its normal-regime bid is red whatever its label; an event-Green sale above target at a normal bid is not); `metamorphic/test_relabel_sale_reason_leaves_p_red` (permuting `SaleReason` labels leaves P(red) unchanged; QUANT-03); `test_recourse_protocol` (proceeds booked once; a sold fraction's later flows are zero; on the unreduced fixture tree H's red-margin rows and P agree on the first red month; BUILD-01); `test_readiness_linear_vs_replica` (|ΔSH_TP| ≤ 0.5 month and |Δheadroom| ≤ $0.1bn on 2,000 paths; A20); `test_appetite_reads_tp_24m` (QUANT-09); `test_pricing_conventions` (revolver 0.5 in s*, OV2-consistent opportunistic loss, lag 2, RA stressed income; `dist_mult` never applies to RA; QUANT-14); LR8 = 0.814 fails on census v1.0 and 0.752 passes on v1.1 under allocation v1 (G-gap_02 §2); property test of conservation over random flows (hypothesis).

---

### 4.15 `beliefs` (WP-14, wave 1)

**Purpose.** The Forward Belief Engine FBE-R: four marks to calibrated forward beliefs, credibility, diagnostics, forecast scoring and the deterministic performance module O3 (ARCH §4.7; G-gap_02 §3–5; S-ADR-10, S-ADR-11).

```python
def nowcast_nav(unit: Holding, marks: Sequence[Mark], index_log_returns: F64, cfg: "NowcastConfig") -> float   # V* = N e^{β̃Δm − ψ}
def irr_translation(unit: Holding, rec: ForecastRecord | Mark, cashflows: pa.Table, nowcast_bn: float, profile_q: F64,
                    exit_prior_q: tuple[float, float]) -> tuple[F64, float]   # forward-basis (p10, p50, p90) and remaining life H_f (S-ADR-27);
                                                                            # profile_q: the unit's mean-path distribution profile per unit of
                                                                            # remaining value (priv.FundEngine.mean_path, passed in as data)
def signal_returns(unit: Holding, marks: Sequence[Mark], quotes: Sequence[Quote], nowcast_bn: float, cashflows: pa.Table,
                   profile_q: F64, cfg: "SignalConfig") -> "SignalSet"     # all four marks on the forward basis
def market_implied_return(quote: Quote, buyer_cf_bn: F64, ref_nav_bn: float) -> float                          # p N^ref = Σ E_b[CF](1+y)^−t
def fit_bias_model(forecasts: pa.Table, frozen: "FrozenOptimizerOutputs", cfg: "BiasConfig") -> "BiasModel"      # Huber (statsmodels RLM, HuberT)
def credibility(scored: pa.Table, *, prior: tuple[float, float] = (math.log(1.75), 0.25),
                decay_halflife_q: int | None = None) -> dict[GroupId, "KappaPosterior"]   # the full point-in-time archive (S-ADR-27)
def forecast_precision(kappa: float, sigma_hat: float, horizon_q: int, cap_q: int = 8) -> float   # min(1, cap_q/h)/(κ²σ̂²) (QUANT-13)
def translate(group: GroupId, signals: "SignalSet", unit: Holding, tax: GroupRegistry) -> "SignalSet"
def fuse(units: Sequence[Holding], signals: Mapping[UnitId, "SignalSet"], bias: "BiasModel",
         kappa: Mapping[GroupId, "KappaPosterior"], cfg: "FuseConfig") -> BeliefSet
def diagnostics(unit: Holding, marks: Sequence[Mark], milestones: Sequence[Milestone], belief_row: "UnitBelief",
                hazards: "FittedHazards", cfg: "FlagConfig") -> tuple[int, float, float]   # flags bitmask, p_achieved_4q, p_achieved_8q
def draw_paths(bs: BeliefSet, base: bytes, paths: np.ndarray, graph: OverlapGraph, tax: GroupRegistry,
               world: WorldSpec) -> BeliefDraws                              # per world and block, per quarter (S-ADR-28)
def wis(y: F64, q10: F64, q50: F64, q90: F64) -> F64      # (1/1.5)[½|y − q50| + 0.1·IS_0.2]
def crps_gaussian(y: F64, mu: F64, sigma: F64) -> F64; def coverage80(y: F64, q10: F64, q90: F64) -> float
def blp_fit(pit_values: F64) -> tuple[float, float]; def blp_apply(cdf_values: F64, ab: tuple[float, float]) -> F64   # beta-transformed linear pool
# perf.py — port of perf_module.py (perf-0.1.0), 17/17 golden tests
def xirr(dates: Sequence[date], cfs_bn: F64) -> float | None
def tvpi_dpi_rvpi(contribs_bn: F64, dists_bn: F64, nav_bn: float) -> tuple[float, float, float]
def ks_pme(dates: Sequence[date], contribs_bn: F64, dists_bn: F64, nav_bn: float, index: F64) -> float
def direct_alpha(dates: Sequence[date], cfs_bn: F64, nav_bn: float, index: F64) -> float
def modified_dietz_twr(values_bn: F64, flows_bn: F64, flow_weights: F64) -> float
def credit_yields(cash_interest_bn: F64, fees_bn: F64, par_bn: F64, chargeoffs_bn: F64, recoveries_bn: F64, dt: F64) -> dict[str, float]
def overlay_book_pnl(d_mtm_bn: F64, cash_bn: F64, ftp_a: float, im_bn: F64, dt: F64) -> float
# validation.py
def fbe_variant(variant: str, n_worlds: int, root_seed: int) -> FBEValidationSet   # pure generator of a misspecification variant (BUILD-21)
def validate_fbe(variants: Sequence[str] = ("M0", "M1", "M2", "M3", "M4", "M5", "M5s", "M6", "MALL"),
                 n_worlds: int = 2000, root_seed: int = 0) -> "GateReport"   # G-A … G-E on fbe_variant sets; thresholds in config/beliefs/misspec_gates.yaml
```

**Algorithms.** One basis: annualized forward log return on nowcast economic NAV, net. **Translation from ADIC's marks** (brief §9; S-ADR-27; ARCH §4.7; QUANT-11, BUILD-09): a since-inception net MOIC or IRR mark or forecast with down/base/up cases is read as quantiles through its `case_map` (P10/P50/P90 by default; the map is monotone, so the quantiles carry through). For each case the remaining value R_f is the scale k of the unit's mean-path distribution profile (conditional on the current exit-window posterior) such that the cash-flow history plus k × profile reproduces the stated MOIC (R_f = MOIC_f·PaidIn − Dist) or IRR (root-found with `numerics.brentq`, sign change checked); H_f is the profile's cash-weighted remaining life and ρ_f = H_f⁻¹ ln(R_f e^{β̃Δm}/V*_t); exit-timing uncertainty around `exit_horizon_q` widens σ̂. Single deals use one terminal flow at the forecast exit date; Real Assets translate yield-on-cost and exit cap rate through a direct-capitalization model; credit and Capital Solutions use contractual yield less expected loss. The fused total return is split into the unit's benchmark expectation at the as-of, r_f + β̂·ERP_ref on the mixture CMA, and α̂ (S-ADR-28). **Fusion.** Fund interests: Benktander U = c*U_CL + (1 − c*)U_BF, c* = p/(p + t), prior frozen at inception, fused with the forecast only. Single deals: **equal (or screened) weights** on the debiased signals by default, with Ω̃ entering the predictive variance only; constrained GLS weights μ̂ = Λ⁻¹(mσ_k⁻² + 1′Ω̃⁻¹s̃) with weights ≥ 0 are the variant `FuseConfig.weights = "gls"`, retained only if they beat the equal and screened averages out of sample on ADIC's archive; synthetic data never select it (S-ADR-10 as amended by S-ADR-27; v1.0's w = (1 − s)w_GLS + s·w_eq put Ω̃ back into the weights, QUANT-24). Every linear pool is recalibrated by a beta-transformed linear pool. FBE-R: y_j − q50_j = β₀ + β_D1{D} + β_gap(u_j − a_j)+ + β_flag1{SELL_{i,t−1}} + β_env·env_binding_{g,t−1} + β_hist·history_indicator_j + ε_j, slopes pooled, intercepts by group/strategy/age, inverse-propensity weights for declined deals; the strategic covariates come from the *previous* quarter's frozen optimizer outputs and are 0 with `history_indicator = 1` on the pre-go-live archive, so their slopes are estimated from go-live data only. **Credibility:** κ_g on the full point-in-time archive (optional time decay), prior LN(ln 1.75, 0.25²); a forecast enters once, at precision `forecast_precision` = min(1, 8/h)/(κ_g²σ̂²) for a horizon of h quarters, so precision is capped beyond 8 quarters ahead (v1.0 read the literature's horizon cap as an 8-quarter estimation window, QUANT-13); σ̂ = (q90 − q10)/2.563 from the case quantiles; ε ~ t_ν(0, κ_g σ̂ c_ν); gate G-E caps κ_g at 2.74 until the pay remedy holds. **Draws** (S-ADR-28): `draw_paths` returns, per world and block, α₀ = posterior draw + shared group-bias shock + GP effect (one draw per GP per path), shifted to the world's CMA-line basis (selection, fee and leverage conventions: the bridge's double-counting guard), with learning parameters (m, φ, η) per unit. Diagnostics: Zombie-NAV (reported NAV ≥ cost or prior-year mark while the fitted exit hazard < P25 of its reference class in the same exit regime for ≥ 4 quarters); catalyst rule halves precision of an unmilestoned recovery forecast; flags F1 hockey-stick, F2 stale NAV, F3 fundraising window, F4 market disagreement > 400bp, F5 exit multiple > entry, F6 leverage > 6× or ICR < 2.0, F7 near-term exit at < 15% regime probability, F8 PIK at face, F9 accretion booked as return, F10 targets used as expectations. Tier 2 uses posterior means; Tier 1 the posterior P10 with group bias at +2 sd.
**Invariants.** The pipeline is acyclic: `fuse` reads only frozen prior-quarter optimizer outputs (hash checked at G2). Synthetic data never selects between FBE variants (S-ADR-19).
**Tests.** `regression/test_perf_golden.py` 17/17 (e.g., XIRR of −100 then +121 over 730 days = 10%; KS-PME = TVPI on a flat index; tracker direct alpha 0); `recovery/test_fbe_sbc.py` (rank uniformity χ² p > 0.01; a fusion ignoring correlated u–f errors must fail, reproducing χ²₁₉ ≫ 30.1); ±5pp recovery of b^u, b^f and κ_g per group (V17), run through the IRR/MOIC translation on the synthetic archive (QUANT-11); `unit/test_irr_translation.py` (a MOIC or IRR forecast generated from a known forward return on the mean-path profile translates back within 1bp; cases map monotonically to P10/P50/P90; a later exit horizon lowers ρ_f at a fixed MOIC); `recovery/test_fbe_gates.py` (G-A–G-E with the thresholds of `config/beliefs/misspec_gates.yaml` on `fbe_variant` sets; it tests mechanisms only until the gate outcomes are re-derived under the S-ADR-10/27 estimator (equal-weight default, BLP recalibration, full-archive κ_g with the horizon cap) and frozen again before the first scored release, because v1.0 pinned G-gap_02 Table 5 outcomes obtained with the old estimator; BUILD-36); `test_forecast_precision_horizon_cap` (QUANT-13); `test_equal_weights_default` (Ω̃ changes the predictive variance, never the default mean weights; QUANT-24); `test_draws_per_world` (draws frozen at α̂ reproduce the no-learning variant; two engines with claims on one GP read the same `gp_effect_q`; `alpha0_q` differs across worlds only by the basis shift; BUILD-04); WIS golden (12/20/26% vs 7% → 0.086); market-implied solver round trip; BLP improves PIT uniformity on a miscalibrated pool.

---

### 4.16 `bridge` (WP-14, wave 1)

**Purpose.** "What you need to believe" per model world (ARCH §4.11; gap_05).

```python
def bridge_card(world: WorldSpec, saa_weights: Mapping[str, float], levers: Sequence[LeverLine], overlay_sr: float,
                overlay_sigma_a: float, leverage: float, financing_spread_a: float, drags: Mapping[str, float],
                *, target_a: float = 0.10, horizon_years: int = 10, vol_a: float | None = None) -> BridgeCard
def p_mu_ge(target_a: float, mean_a: float, tau: float) -> float
def p_horizon_ge(target_a: float, mean_a: float, sigma_log: float, tau: float, years: int) -> float   # σ²_log/H + τ²
def verdict(p_mu_central: float, p_mu_at_cap: float) -> Literal["Plan", "Stretch", "Aspiration"]   # ≥ 50% central; ≥ 10% at 1.30× cap
```

**Algorithm.** m_m = w′a_m + Σ_jω_jα*_j + SR·σ_O + (L − 1)(a_{m,EQ} − r_{f,m} − s) − Σ_k D_{k,m}; α* against each CMA line's own benchmark (double-counting guard); M2's PE selection α* capped at 0.25pp; τ² = Σ(ω_j sd_j)² + (sd_SR σ_O)²; geometric conversion with a consistent lognormal.
**Tests.** Port of `research/addenda/gap_05_calcs/bridge.py`: verifier-10 stylized-book figures reproduced exactly; working-book evidence-central 10-year geometric E[R] M1 8.84%, M2 10.47%, M3 6.82%, M4 8.61%, M5 8.86%, M6 6.06% within 1bp on the allocation-v1 fixture, verdicts Stretch/Plan/Aspiration/Stretch/Stretch/Aspiration (regression, SYNTHETIC); P(μ ≥ x) uses τ only (property).

---

### 4.17 `synth` (WP-15, wave 2)

**Purpose.** SYN-ADIC-177: structural generator with world, sealed-truth and observation layers; censuses; releases; gates V1–V24; misspecification generators for FBE validation (ARCH §9.4; GROUPS §6; G-gap_02; full specification in §6).

```python
class SynthConfig(BaseModel):
    allocation: AllocationId = "v2"; census_id: CensusId = "v1.1"; release: Literal["R0", "R1", "R2", "R3"] = "R0"
    root_seed: int; truth_variant: Literal["sealed", "mature", "flat10", "growth20", "v1.0_repro"] = "sealed"
    pc_loss_pair: Literal["severity", "incidence"] = "severity"; hf_trs_scenario: bool = False; overlay_fixture: bool = False
def decision_census(allocation: AllocationId, tax: GroupRegistry, root_seed: int) -> tuple[CensusId, str]   # S-ADR-03 rule and reason
def fit_pe_history(nav_target_bn: float, unfunded_target_bn: float, rule: "HistoryRule") -> "PEHistory"      # LP on FundEngine.mean_path
def build_book(cfg: SynthConfig, tax: GroupRegistry) -> "SynthBook"            # observation-layer BookSnapshot + truth handles
def generate_observations(book: "SynthBook", world: WorldSpec, cfg: SynthConfig) -> "ObservationSet"   # O1–O4 (O2/O4 as since-inception net
                                                                                    # IRR/MOIC with cases, S-ADR-27), quotes, tapes, 2008→as-of archive
def write_release(book: "SynthBook", obs: "ObservationSet", store: BitemporalStore, truth: "SealedTruthStore") -> "ReleaseManifest"
def run_gates(release: "ReleaseManifest", gates: Sequence[str] | None = None) -> "GateReport"   # V1–V24, VR1–VR3 (§6.9)
def book_variant(census: CensusId, cfg: SynthConfig, tax: GroupRegistry) -> "SynthBook"   # misspecification-ensemble book variants
                                                                                    # (PlaneSpec.book_variants, S-ADR-43); the FBE generators live in
                                                                                    # beliefs.validation.fbe_variant (BUILD-21)
class SealedTruthStore:
    def __init__(self, root: Path) -> None: ...
    def write(self, key: str, obj: Any) -> str: ...
    def open_for_validation(self, token: "MRMToken") -> "TruthReader": ...    # ACL-checked; agents and estimators cannot open (TB8)
```

**Invariants.** Only `synth` writes to a SYNTHETIC store; every row is labelled; same config + seed → same release hash; the truth store is never imported by `beliefs`, `core`, `lab` or `agents` (layering test).
**Tests.** The blocking V-gates green on the decision census (increment 1: V1–V2, V5–V9, V12, V20, V22–V24; v1: every applicable gate; a gate that cannot run, e.g. V15 before ADIC data or V18 before R2, is n/a and never blocks; S-ADR-37); S-ADR-03 rule (`v1.1` under v2 is replaced by `v1.1r` iff no V6-compliant history fits the PE bucket or V1–V2 fail, with the reason recorded); `test_archive_shape` (O2/O4 emit since-inception net IRR or MOIC with down/base/up cases, quarterly from 2008 with bitemporal `recorded_at`; strategic covariates exist only after the synthetic go-live date; QUANT-11, BUILD-09); release reproducibility; labelling 100%; R1 uses CRN across SELL / HOLD / REFINANCE / LEVER (column flows on identical draws); V16–V18 run as release-validation jobs whose hashed reports the pipeline reads (B14), never inside B12.

---

### 4.18 `actions` (WP-16, wave 2)

**Purpose.** Instrument library, admissibility, exact column cash flows on CRN, Lagrangian scores, decision cards and flip thresholds (ARCH §4.8).

```python
def load_library(tax: GroupRegistry, config_dir: Path | None = None) -> tuple[InstrumentSpec, ...]
def admissible(unit: Holding, action: LensAction, inst: InstrumentSpec, state: "AdmissibilityState") -> "AdmissibilityResult"
def candidate_actions(book: BookSnapshot, lib: Sequence[InstrumentSpec], state: "AdmissibilityState",
                      sizes: Sequence[float] = (0.25, 0.5, 1.0)) -> tuple[LensAction, ...]
def column_flows(engines: Mapping[str, AssetEngine], action: LensAction, cube: ScenarioCube) -> FlowCube   # Δ vs HOLD on CRN
def build_columns(actions: Sequence[LensAction], tree: Tree, engines: Mapping[str, AssetEngine],
                  cubes: Mapping[WorldId, ScenarioCube]) -> ColumnPool         # coefficients keyed by RowKey, so columns can be built
                                                                              # before H is assembled; core.h.row_index maps them (BUILD-22)
def build_catalogue(book: BookSnapshot, tree: Tree, engines: Mapping[str, AssetEngine], cubes: Mapping[WorldId, ScenarioCube],
                    overlay_stress: "OverlayStressCoeffs", lib: Sequence[InstrumentSpec], cfg: "CatalogueConfig") -> ActionCatalogue
def score(col: Column, sol: HSolution) -> "ScoreBreakdown"          # r_j − κ^irr; r_j already carries κ^tc (cash rows), the convex excess
                                                                    # (segments) and κ^GP (state K), so they are not subtracted again (QUANT-07)
def reservation_price(unit: Holding, sol: HSolution, belief: UnitBelief, best_refi: Column | None) -> float
def flip_thresholds(unit: Holding, col: Column, sol: HSolution, belief: UnitBelief) -> FlipThresholds
def make_card(col: Column, sol: HSolution, sel: Selection, belief: UnitBelief, env: EnvelopeSet,
              quality: Mapping[str, DualQuality], run_ref: ArtifactRef) -> DecisionCard
def lever_identity_gap(engines: Mapping[str, AssetEngine], unit_id: UnitId, add_bn: float, refi_bn: float, cube: ScenarioCube) -> float
```

**Algorithms.** Score(i, a) = Σπ E_b[ΔCF] + Σμ̃(hΔHQLA − ΔSC) + Σφ̃(ΔIGC − 0.08ΔNAV) − λ_RΔCVaR − λ_LevΔLev − λ_EncΔEnc − Σρ_kΔFloor_k − κ^irr − κ^GP − κ^tc (SYN §4.4), evaluated as r_j − κ^irr with r_j = c_j − y′A_j on the restored H: A_j already carries κ^tc in the cash rows, the convex excess through segment variables and κ^GP through the accumulated-charge state K, so neither is subtracted twice (ADR-42; QUANT-07). Reading rules: SELL iff the cash-equivalent bid > p* = [E LAPV(HOLD + best REFI) + κ^GP + κ^irr − relief]/NAV; REFI iff s_B + f/T + λ_Lev + covenant charge + tightening premium (TIGHT/CLOSED, S-ADR-12) < ℓ̄_[0,T]; ADD iff α* − ℓ̄_[0,D] − risk charge > 0; LEVER (≡ ADD + REFI, cash-neutral, so ℓ̄ cancels) iff α* − risk charge − (s_B + f/T + λ_Lev + covenant charge + tightening premium) > 0, with the ADD and REFI legs shown separately (`DecisionCard.lever_legs`) and the flip threshold α* − risk charge = all-in financing cost (`FlipThresholds.lever_breakeven_financing_a`; ADR-49; v1.0's conjunctive rule rejected profitable LEVERs, QUANT-17). Lens classification follows the exposure delta: a lower-strike sale against a held put is a partial SELL; Corporate Finance borrowing for liquidity is REFINANCE; only borrowing that funds new exposure is LEVER (QUANT-30). A red-tier SELL column is `t6_consuming` when the frozen state meets `ledger.red_test` (ii) or its bid meets (iii) (S-ADR-30). Deal NPVs use the one-off premium L_s = π_{s,0}/π̄ − 1. Admissibility: ≤ 1 lens per asset per quarter; consent probabilities and lead times; HF notices on notice dates; LP-accessible instruments only (V23); inadmissible: call default, excuse-right abuse, non-consented transfers or pledges, refusing contractual DDTL draws, MNPI flows, counting intra-ADIC transfers as liquidity, single-asset co-investment REFINANCE.
**Tests.** `test_lever_equals_add_plus_refi` (every group's LEVER instrument: |CF(LEVER) − CF(ADD) − CF(REFI)| ≤ 1e-9 $bn per path-quarter) with an exposure-delta check per lens; `test_exposure_delta_every_instrument` (every library instrument satisfies its lens's `LensAction` sign rules; lower-strike sales classify as SELL and CF liquidity borrowing as REFINANCE; QUANT-30); `test_lever_additive_rule` (α* 3%, risk charge 0.5%, all-in financing 2.4%: LEVER pays at ℓ̄ = 0.5%, 1.5% and 4%, and the card shows both legs; QUANT-17); `test_columns_keyed_by_rowkey` (columns built before `build_h` map to the same rows as columns built after it; BUILD-22); `test_t6_consuming_sell_flag` (in an event-Amber state every red-tier SELL column is `t6_consuming`, held at zero in Phase II and priced by forced re-solve; S-ADR-30); HOLD columns are zero; inadmissible list rejected; worked values on the gap_02 / G-gap_01 fixtures (allocation v1, census v1.0): 2018 buyout fund bid 88% → reservation price 87.7% with T4′ met by a $13.4bn revolver; 0.9% when priced on the pinned dual; 76.8% after restoration; 70.6% before the revolver is signed vs 90.7% after (±0.1pp); metamorphic: a wider discount never raises discretionary SELL proceeds when liquidity is slack; a costlier facility never raises REFI volume.

---

### 4.19 `core.sim` — `observables`, `sim`, `factory`, `policy`, `terminal`, `certify` (WP-17, wave 2)

**Purpose.** The policy simulator P on the shared ledger kernel; the standing policy P0, controls and archetypes as native policies; terminal values; certification (ARCH §5.3, §5.9–5.12).

```python
# observables.py — every DSL and policy variable has a producer inside P, with no H solve per path (BUILD-15)
OBS_VARS: Mapping[str, "ObsVarSpec"]          # config/core/dsl_variables.yaml: name, min_lag_q, unit, source, kind ∈ {path, unit, group}
def build_observables(t: int, hist: "ObservableHistory", *, lags: Mapping[str, int]) -> Observables
def exit_posterior(dist_rates_q: F32, prior: F64, sigma: float = 0.15) -> F32     # [P, 4] per-path state.exit_filter on simulated PE distribution rates
def shock_posterior(brent: F32, draw_rate: F32, prior: F64) -> F32                # [P, 6] nowcast on simulated oil and fiscal observables
def ell_lookup(stress_class: I8, kern: Kernel) -> F32                             # [P] ℓ_t and ftp_published from λ^spot by simulated stress class (A21)
def unit_observables(states: Sequence[EngineState], quotes: Sequence[RecourseAvailability],
                     price_table: "ReservationTable") -> dict[str, F32]           # [P, U] bid_ce, reservation_price (table by stress class), rho_hat
                                                                                  # (per-path filter of lagged reported returns)
# policy.py
class P0Policy:                               # implements Policy; θ in config/policy/p0.yaml (22 parameters)
    def __init__(self, theta: Mapping[str, float], idx: UnitIndex, tax: GroupRegistry, recourse: RecourseOrder,
                 mandate_mode: MandateMode = MandateMode.B_OWNER_CALL) -> None: ...
    def act(self, q: int, obs: Observables) -> ActionSlice: ...
NATIVE_POLICIES: Mapping[str, Callable[["PolicyContext"], Policy]]   # HOLD, STATIC_SAA, DECK_RULES, TARGET_CHASING, PLACEBO,
                                                                       # PRO_RATA, OVERLAY_ONLY, LIQUID_FIRST, CASH_LAST, ARCH_A, ARCH_B, ARCH_C
class ChPolicy:                               # C_H: H's quarter-1 package, then P0
    def __init__(self, root_actions: ActionProposal, p0: P0Policy) -> None: ...
def make_policy(ref: PolicyRef, ctx: "PolicyContext") -> Policy
# sim.py
class SimConfig(BaseModel):
    n_paths: int; block: int = 2000; plane: Plane; quarters: int = 40
    record: tuple[Literal["ledger_paths", "group_rates", "flows_by_unit"], ...] = (); keep_units: bool = False
    private_clock: Clock = Clock.QUARTERLY; processes: int = 1; numba_threads: int = 8
@dataclass(frozen=True)
class SimResult: metrics: PathMetrics; ledger_paths_ref: ArtifactRef | None; group_rates: GroupRates | None; manifest: RunManifest
                                              # a frozen dataclass, not a Pydantic model, because it holds arrays (BUILD-34)
def simulate(book: BookSnapshot, beliefs: BeliefSet, policy: Policy, world: WorldSpec, state0: StateSnapshot, cfg: SimConfig,
             *, root_seed: int, owner_cfg: OwnerConfig, filter_params: StressFilterParams, salt: bytes | None = None,
             factory: EngineFactory | None = None) -> SimResult           # engines, ledger, owner config and policy wrappers come from
                                                                          # factory.build(book, world), which applies world.overrides (S-ADR-43)
def record_group_rates(book: BookSnapshot, beliefs: BeliefSet, world: WorldSpec, state0: StateSnapshot, n_paths: int,
                       plane: Plane, *, root_seed: int, owner_cfg: OwnerConfig, filter_params: StressFilterParams,
                       quarters: int = 12) -> GroupRates                   # the tree's 12 quarters only (B10; BUILD-05)
# factory.py
class DefaultEngineFactory:                  # implements EngineFactory; engine registry in config/engines.yaml; effective configs hashed (S-ADR-43)
    def build(self, book: BookSnapshot, world: WorldSpec) -> EngineBundle: ...
def j_value(pm: Mapping[WorldId, PathMetrics], obj: ObjectiveSpec) -> "JResult"          # J per world, mixture, Ψ_τ, CE bp a year
def tier1_board(pm: Mapping[WorldId, PathMetrics], tier1: Tier1Spec, floor: FloorSpec) -> "Tier1Board"
def gambling_signatures(pm: PathMetrics, quarterly_series: Sequence[str]) -> "GamblingReport"   # G1/G2 failures; RFY + bimodality flags
# terminal.py
def fit_terminal_values(sim: SimResult, tax: GroupRegistry, *, regressors: Sequence[str]) -> "TerminalValues"   # ω_g, ψ_g; R² out of sample
# certify.py
def certify(ref: PolicyRef, ctx: "SimContext", contract: AnalysisContract, plane: Plane, worlds: Sequence[WorldId],
            *, n_paths: int = 50_000, salt: bytes | None = None) -> "CertificationReport"   # Certificates per gate × class band
```

**Simulation loop** (per 2,000-path block; §1.3): `factory.build(book, world)` → regenerate and verify the cube block (scen + owner) → `beliefs.draw_paths(…, world)` → engines `init(…, draws=…, world=…)` → for t in 0…39: build observables (lagged; producers above) → `policy.act` (including `preemptive_raise`, executed at quarter start) → every engine's `recourse_quotes(t)` → `rng.draw_block` for every engine's `noise_requests(t)` (outside kernels) → quarterly engines step; monthly engines step three times → `ledger.apply` for months 3t…3t+2 with the quotes (quarterly flows spread by `contracts.rules.intra_quarter_profile`; instalment in month 3t + 2), returning `RecourseOutcome` → every engine's `apply_recourse` → `ledger.readiness_reading` and `cfp_reading` at quarter end (the full `stress_replica` only for paths leaving their hysteresis band; A20) → record metrics, with red events from `red_test`. Failed paths (engine fault) are flagged `failed` and scored worst-case; never dropped.
**P0** (θ in config; SYN §4.8 amended by gap_02/gap_04 and S-ADR-13/15): reserve HQLA*/W = θ1 + θ2·P(e ∈ {D, F}) + θ3·F_t; pacing with drought brake θ4, overcommitment term θ5, gap-closing speed θ6 (25–50% a quarter) and stage multipliers θ7/θ8 keyed to the planning stage; a cut earns no liquidity credit for 2 quarters (S-ADR-20); economic leverage clip(θ9 + θ10·c_t − θ11·F_t, 1, 1.3); tail ratio clip(θ12 + θ13·F_t − θ14·c_t, 0, H_max) with the convex sleeve rising only when `ltp_pctile` ≥ θ21 (S-ADR-15); opportunistic budget falling with margin use (θ15); SELL screen on fitted ρ̂ (θ16); HF notice share at event-Amber (θ17); recourse order switch (θ18) and crowding haircut (θ22); `preemptive_raise` at P(e ∈ {D, F}) ≥ θ19; P2S share at event-Red (θ20). No payout rung and no top-up in Mode B (TR8).
**Archetypes** (ARCH §5.10): A sells PE/SEC/CO interests bidding ≥ reservation price − 5pp within depth caps until the liquid share reaches 28%; B uses the revolver if signed, the capacity-capped NAV facility, CS back-leverage within D/E ≤ 0.5, P2S up to $10bn and tail monetization at 2× premium, with no private sales; C scales the opportunistic book to its 1.5%-of-NAV vol cap and IM budget and raises economic leverage along the cushion-monotone rule to its maximum within OV1–OV3. Each passes through module F; a materially projected archetype is labelled "Tier-1 infeasible as specified".
**Gambling detector.** G1 (failure): regression of exposure change on lagged loss with the cushion as control has a positive loss coefficient (p < 0.05); G2 (failure): > 5% of path-quarters at leverage ≥ 1.29 while W̃ is below the target path. Flags: bimodality coefficient of terminal wealth > 0.555; P(10%) rising with a flat median; RFY (carry, short-vol and illiquidity exposure rising as the cushion falls; S-ADR-07); the relabelling signature (red-tier sales tested non-red rising while P(red) falls against the incumbent; sent to the auditor; QUANT-03).
**Performance.** B1: 10,000 paths × 40 quarters, asset level, policy in the loop ≤ 60 s; design budget ≈ 36 s, the sum of nine component lines that `tests/perf/test_b1_profile.py` asserts separately: scenario cube 2.5, RNG 4, private engines 12, public 3, overlay 5, ledger and recourse 2, readiness and CFP 4, policy and observables 2, metrics 1 (§10.1; v1.0's lines summed to 95–125 s before HF, overlay and policy; QUANT-12, BUILD-05); PD measured 10.9 s on one process for a simplified engine [M]. B5: 50,000 paths per world ≤ 60 s on 4 processes including process start-up (5 × 36 s ÷ 4 ≈ 45 s).
**Tests.** A1 (`reconciliation/test_a1_private_clock.py`): |ΔP(red)| between quarterly and monthly private clocks ≤ 0.1pp (a fixed bound) on ≥ 20,000 CRN paths, or on importance-sampled stressed paths with an equivalent paired SE, else the WP switches the default to monthly (v1.0's max(0.1pp, 2 SE) on 2,000 paths let clock errors up to ≈ 0.3pp pass; QUANT-31); `determinism/test_sim_workers.py` (same checksum at 1, 4, 8 workers and any block size); `drills/test_failed_paths_worst_case.py`; `layering/test_no_horizon_reference.py` (Observables carry only registry variables; no t-to-go, world id or path id); `test_observable_producers` (every `OBS_VARS` entry has a producer and a lag rule; `ell_lookup` agrees with H's node ℓ on the tree's paths for ≥ 95% of pacing and SELL decisions, A21; BUILD-15); `test_factory_overrides` (each `MisspecOverride` changes only its target module's effective config hash; BUILD-16); `test_tier1b_floor` (`tier1_board` re-certifies the forward 10-year floor and applies the class bands; regression: an i.i.d. lognormal book with an 8.5% arithmetic mean breaches CVaR₁₀% ≥ 0 at ≈ 14.3% vol, SYN §4.9; QUANT-01); J neutrality identity W̃_T = W₀Π_T to 1e-9; archetype behaviour tests; certification CP coverage.

---

### 4.20 `core.h` — `tree`, `h`, `solver`, `phase1`, `phase2`, `duals`, `kernel` (WP-18, wave 2)

**Purpose.** The here-and-now program: pooled-observable tree, H assembly from the ledger's linear rows, solver wrappers, lexicographic Phase I with consent scenarios, restored Phase II, dual extraction, kernel and FTP. Formulation, settings and acceptance are in §5; this entry fixes the API.

```python
def attach_group_rates(cubes: Mapping[WorldId, ScenarioCube], rates: Mapping[WorldId, GroupRates]) -> dict[WorldId, ScenarioCube]
def build_tree(cubes: Mapping[WorldId, ScenarioCube], spec: TreeSpec) -> Tree           # ARCH §3.5 signature; cubes must carry group_rates
def build_h(tree: Tree, ls0: LedgerState, cat: ActionCatalogue, c: AnalysisContract, *,
            preset: Literal["whatif", "default", "signoff", "overnight"] = "default", appetite: bool = False,
            glide: GlidePath | None = None, replication: int = 0) -> LPModel             # ARCH signature + keyword refinements
def solve_lp(lp: LPModel, *, solver: Literal["highs", "clarabel"] = "highs", algorithm: Literal["ipm", "simplex"] | None = None,
             basis: "Basis | None" = None, time_limit_s: float = 110.0) -> "LPResult"   # algorithm None -> contract solver_policy
def check_highs_options() -> dict[str, Any]                                              # asserts option names; recorded in manifest
def build_t0_block(ls0: LedgerState, stress: StressSpec, levers: LeverSet, c: AnalysisContract) -> LPModel
def phase1(lp: LPModel, tiers: Sequence[RowTier], levers: LeverSet, scenarios: Sequence[ConsentScenario]) -> Phase1Result   # ARCH signature
def phase1b_cvar(h: LPModel, p1a: Phase1Result, levers: LeverSet) -> Phase1Result
def t6_screen(lp: LPModel, levers: LeverSet, scenario: ConsentScenario) -> T6Screen     # CVaR rows at HOLD, reversible levers at cap (BUILD-11)
def recovery_mode(p1: Phase1Result, t6_screen: T6Screen, c: AnalysisContract) -> tuple[ContractMode, GlidePath]   # capacity breaches only (S-ADR-31)
def phase2(lp: LPModel, p1: Phase1Result, glide: GlidePath, tree: Tree) -> HSolution     # ARCH §3.5 v1.1 (S-ADR-29); duals only from here
def row_index(lp: LPModel) -> RowIndex                                                 # str(RowKey) → row number, after build_h (BUILD-22)
def extract_duals(lp: LPModel, res: "LPResult", tree: Tree) -> DualSet
def dual_quality(lp: LPModel, sol: HSolution, rows: Sequence[RowKey], *, basis: "Basis", fd_rows: Sequence[RowKey] = (),
                 step: float = 1e-4) -> dict[str, DualQuality]   # ranging from the basis; one parametric step where degenerate;
                                                                 # finite differences only on fd_rows (≤ 10 on the quarterly path; S-ADR-38)
def assert_no_pinned_duals(lp: LPModel, sol: HSolution, *, elastic_penalties: Sequence[float]) -> None   # PinnedDualError
def kernel(sol: HSolution, tree: Tree) -> Kernel
def ftp_points(sol: HSolution, tree: Tree, kern: Kernel, tenors_q: Sequence[int] = (1, 2, 4, 8, 12)) -> tuple[FTPPoint, ...]
def solve_replications(c: AnalysisContract, ls0: LedgerState, *, cube_metas: Mapping[WorldId, CubeMeta], catalogue_cfg_hash: str,
                       n_rep: int = 5, processes: int = 5) -> tuple[HSolution, ...]    # one top-level, picklable worker per replication,
                                                                                       # single-threaded; each worker regenerates its cubes and
                                                                                       # catalogue from hashes and seeds, never from closures (BUILD-28)
```

---

### 4.21 `core.select` — `colgen`, `levelb`, `safety` (WP-19, wave 2)

```python
def price_columns(pool: ColumnPool, sol: HSolution) -> dict[str, float]           # r_j = c_j − y′A_j, direct coefficients only
def gamma_certificate(z_rmp: float, rc: Mapping[str, float], caps: Mapping[str, float], z_fixed: float) -> float   # Γ = z_RMP + Σu_j r_j⁺ − z_fixed
def select(lp: LPModel, sol: HSolution, cols: ColumnPool, *, basis: "Basis") -> Selection   # ARCH §3.5 v1.1: Level-B MILP + warm fix-and-resolve + Γ
def forced_resolves(lp: LPModel, sol: HSolution, cols: Sequence[Column], *, cap: int = 20) -> dict[str, float]   # Δ exact objective, CE bp;
                                                                                  # flag > 2bp; selected replication only
def hp_ranking_test(cands: Sequence[Column], h_scores: Mapping[str, float], p_scores: Mapping[str, float],
                    replay_cash_gap: float) -> "HPTestResult"                     # Kendall τ ≥ 0.8; replay within 1%
def project(prop: ActionProposal, state: StateSnapshot, *, ls0: LedgerState, rows: "LinearizedTier1",
            exact_check: Callable[[ActionProposal], "ExactCheck"], q_weights: Mapping[str, float]) -> SafeAction   # module F
```

**Level B.** max Σ_j r_j x_j over semicontinuous asset actions (minimum tickets, consents, ≤ 1 action per asset per quarter) subject to ≤ 30 aggregated coupling rows (Q1–Q8 liquidity, T4′, leverage, encumbrance, pledges, envelopes, depth); HiGHS MIP (≤ 1,600 binaries; `mip_rel_gap = 1e-6`, threads 1). Selected actions enter H as exact RHS updates Δ_n; warm dual simplex; ≤ 5 iterations with dual damping 0.5. The LP relaxation splits at most one asset per binding row; split assets form the marginal-asset agenda. Γ is judged on exact utility (`HSolution.exact_objective`, A8) and accepted at ≤ 5bp CE (`stats.h_delta_ce_bp`), with the PWL bound shown beside it; otherwise cards say "selection not certified". Forced re-solves run on the selected replication only, capped at 20: the top cards by |r_j| near the flip point, every marginal-agenda asset and every T6-consuming SELL (S-ADR-38).
**Module F.** a^safe = argmin‖a − a^prop‖²_Q s.t. ĝ_k(S, a) ≤ −δ_k on linearized Tier-1 rows with amber buffers δ_k; cvxpy + OSQP (`eps_abs = eps_rel = 1e-8`, `polish = True`; CLARABEL fallback); ≤ 600 variables; up to 5 iterations of exact re-checks of SIMM IM and OV3; in recovery it projects onto the restored set including the glide path; returns `WhatChanged` records. Every proposal (optimizer, agent package, IC amendment, archetype, standing policy) passes through it.
**Performance.** B3 Level B ≤ 10 s; module F ≤ 1 s per proposal.
**Tests.** Γ ≥ 0 always; on a 40-asset fixture, Level B matches brute-force enumeration and a price-only rule is worse (SYN §4.4 example); `test_split_assets_at_most_one_per_binding_row`; module F: zero violations after projection (A14), finite-difference gradients within 1e-6, `WhatChanged` populated, a Tier-1-violating IC amendment yields `tier1_override_needed`.

---

### 4.22 `icm` (WP-20, wave 3)

**Purpose.** Corporate Finance as internal bank: decision and published FTP at tolerance and appetite, envelopes, requests, recovery envelopes and delivery shares, charges, DVA, transfers, services, pacing and contingent budgets (ARCH §6; S-ADR-16).

```python
def price(sol: HSolution, lp: LPModel, tree: Tree, tax: GroupRegistry) -> tuple[Kernel, FTPCurves, EnvelopeSet]   # ARCH §3.5 v1.1 (S-ADR-29);
                                                                                # PricingRefused on pinned, reverse or unsigned
def price_replications(sols: Sequence[HSolution], tree_by_rep: Sequence[Tree]) -> "PricedSet"   # medians, min–max bands, tree-sensitive flags
def published_ftp(decision: FTPCurves, history: Sequence[FTPCurves], *, halflife_q: int = 2, collar: float = 0.5) -> FTPCurves
def envelopes(sol: HSolution, lp: LPModel, tax: GroupRegistry, coupling_rows: Sequence[RowKey]) -> EnvelopeSet   # Λ^k_g = Σ_{i∈g} a^k_i(x*), LP coefficients
def price_request(env: Envelope, delta_bn: float) -> "RequestPrice"              # dual inside ranging only; else "TPC re-solve"
def delivery_shares(levers: LeverSet, glide: GlidePath, scenario: ConsentScenario) -> dict[GroupId, tuple[float, ...]]
def recovery_envelopes(env: EnvelopeSet, glide: GlidePath, shares: Mapping[GroupId, Sequence[float]]) -> EnvelopeSet   # B^rec = Λ + φ g_t
def charges(book: BookSnapshot, kern: Kernel, ftp: FTPCurves, env: EnvelopeSet, sol: HSolution, cfg: "ChargeConfig") -> "ChargesReport"
def dva(groups: Mapping[GroupId, "GroupReturns"], ftp_vintage: Mapping[GroupId, float], risk_charges: Mapping[GroupId, float],
        credits: Mapping[GroupId, float]) -> "DVAReport"                          # sums to NAV₀(R_P − R_RP) + residual
def pacing_rule(ell: float, ell_bar: float, plan_bn: Mapping[GroupId, float], tax: GroupRegistry, stage: CFPStage) -> dict[GroupId, float]
def cost_of_cut(alpha_star: Mapping[GroupId, float], ftp: Mapping[GroupId, float], durations: Mapping[GroupId, float],
                kappa_gp: float, theta_a: float = 0.149) -> float                 # c^PACE (G-gap_04 §7)
def contingent_gate(dhat: float, confirmed: bool, tier1_green: bool, event_stage: CFPStage) -> bool   # d̂ > 20%, confirmed, Tier 1 green, not Black
def transfer_check(t: "InternalTransfer") -> "TransferVerdict"                   # zero liquidity; fair value both legs; wedge to centre line
def services_charges(services: Sequence[ServiceContract], ftp: FTPCurves, c_buf: float = 0.015) -> "ServicesLedger"
```

**Algorithms.** Decision prices = undamped restored duals (no floor; c_buf = 1.5% is a ceiling); published FTP = EWMA (2-quarter half-life) with a ±50% collar, charged on each asset's liquidity tenor, vintage-locked, CF holds the mismatch (DVA_CF); nightly solves at tolerance and appetite (ADR-29); λ published with its decomposition by binding row; risk charges = H's CVaR-row duals × the action's coefficients (S-ADR-16); summed group risk budgets haircut by h_div; envelope changes collared at ±25% a quarter outside ranging; delivery shares φ_{g,t} = Σ_{ℓ∈L_g}s_{ℓ,24}x^{(t)}_ℓ / Σ_ℓ s_{ℓ,24}x^{(t)}_ℓ over the least-cost reversible lever mix; pacing P_{g,t} = P*_g Π_[m_lo,m_hi](1 − η_g(ℓ_t − ℓ̄)/ℓ̄) with η sign from the taxonomy and the planning-stage corridor (Green 0.75–1.25×, Amber 0.25–0.5× with ≥ 25% protected core, Red protected re-ups only).
**Tests.** `regression/test_kkt_cap_cheapest_spare_lever.py` (port of `test_no_pinned_duals_groups.py` on its research fixture LP, whose objective carries c_ℓ: revolver-signed μ ≈ 0.0113 vs 0.243 without; Σ_h μ_h s_{ℓh} + y_IG ι_ℓ ≤ c_ℓ for every lever below cap; in production H, where every cost sits in the cash rows, the same check is the lever column's reduced cost ≤ 1e-7, ARCH §5.6); `test_recovery_envelopes_sum_and_glide_shares` (Σφ = 1; envelopes + draws + opex + fees = NCO(24) to 1e-9; R1 glide share of CF > 0.9); EWMA and collar; request priced only inside ranging; `PricingRefused` for reverse stresses and unsigned scenarios; c^PACE = 8.6¢ per PE $ forgone (±0.2¢) on the M1 fixture (G-gap_04 §7); transfers count zero liquidity and net to zero on DVA ledgers (V2).

---

### 4.23 `core.mpc` (WP-20, wave 3)

```python
class MPCResult(BaseModel):
    phase1: Phase1Result; mode: ContractMode; glide: GlidePath; solutions: tuple[ArtifactRef, ...]   # 5 replications
    selection: Selection; priced: "PricedSet"; cards: tuple[DecisionCard, ...]; safe: SafeAction
    c_h: PolicyRef; certification: "CertificationReport"; tier1: "Tier1Board"; hp_test: "HPTestResult"; calibration: "BufferCalibration"
def run_quarter_mpc(contract: AnalysisContract, snapshot: BookSnapshot, state0: StateSnapshot, beliefs: BeliefSet,
                    ctx: EngineContext) -> MPCResult
def calibrate_buffers(contract: AnalysisContract, ctx: EngineContext, sol0: HSolution, *, max_iter: int = 4) -> "BufferCalibration"
    # S-ADR-44 (BUILD-13): bisection on one buffer multiplier per T6 class and Tier-1B world, warm-started; stops when every class's
    # CP upper bound in P is within its tolerance and Kendall τ(H, P) ≥ 0.8; returns b_red, b_floor, lambda_T_H and the history (B17 ≤ 5 min)
```

Order (ARCH §5.9): freeze (G2) → Phase I per consent scenario and recovery mode (G0) → H on 5 SAA replications in parallel processes → selection and Γ per replication → replication selection in P (2,000-path race per world, 10,000 only on a near tie; B16) → finite-difference dual checks (≤ 10 rows) and forced re-solves (≤ 20) on the selected replication → H–P test → module F → P certification of C_H = (H's quarter-1 actions, then P0) on the search plane → if a class fails, `calibrate_buffers` and repeat from H with warm starts (≤ 4 iterations); at the cap, Phase I-b decides structural recovery on the CVaR rows, otherwise cards carry `calibration_capped` → artifacts for the sealed run. Defaults: last quarter's calibration, zero buffers in the first quarter.

---

### 4.24 `core.dsl` — `dsl`, `search` (WP-21, wave 3)

```python
def parse_spec(obj: Mapping[str, Any] | str) -> PolicySpec
def type_check(spec: PolicySpec, registry: "VariableRegistry", contract: AnalysisContract) -> "TypeReport"   # TR1–TR8
def compile_spec(spec: PolicySpec, anchor: P0Policy, ctx: "PolicyContext") -> Policy        # vectorized numpy closures; never eval
def identity_check(spec: PolicySpec, anchor: P0Policy, obs_samples: Sequence[Observables]) -> bool   # TR5: w = 0 reproduces P0 exactly
class CMAES:                                       # in-house numpy (no `cma` dependency)
    def __init__(self, x0: F64, sigma0: float, bounds: F64, seed: int, popsize: int | None = None) -> None: ...
    def ask(self) -> F64: ...
    def tell(self, x: F64, f: F64) -> None: ...
    def stop(self) -> bool: ...
def successive_halving(n_candidates: int, evaluate: Callable[[int, int], float], *, eta: int = 3,
                       rung_paths: tuple[int, ...] = (2000, 6000, 10000)) -> list[int]   # 27 → 9 → 3 candidates; ≈ 2× saving (QUANT-33)
def augmented_lagrangian(fitness_j: float, violations: F64, mu: F64, rho: float) -> float
```

**Grammar** (ARCH §5.11, extended by S-ADR-09/12/15): `PolicySpec := anchor "P0@"HASH residual{0..6} package{0..3} overlay{0..3}`; `form := mult_tanh(ρ<1) | add_clip(lo, hi) | switch_hyst(on, off)`; `xform := logit | zscore_frozen | diff(k) | min | max | hinge(k)`; `VAR := c_t | F_t@hash | P(e in {D,F}) | P(Z in {DB,GW,SG}) | planning_stage | event_stage | ftp_published | nav_reported | liquid_share | twr_drawdown | owner_draw_12m | sec_bid_index | facility_headroom | im_util | vrp_pctile | ltp_pctile | fin_window`. Minimum lags: nav_reported 1 quarter, sec_bid_index 1 quarter, others 0 (F_t's EBP input is lagged one month inside the filter).
**Type rules.** TR1 lags ≥ registry minimum; TR2 no scenario token, world id, date, quarters left, budget, true regime, economic NAV or final-plane quantity; TR3 cushion-monotone sizes (anchor monotone, ρ < 1, box(w_c) ⊂ [0, ∞)); TR4 no size increasing in past losses except through c_t; TR5 box contains 0 and the gate forces the identity; TR6 ≤ 25 nodes, ≤ 8 parameters, 0.5bp fitness penalty per parameter; TR7 admissible instruments and consents, internal transfers count zero; TR8 `payout_topup` compiles only in Mode A/H with `owner_signoff`. Failures raise `DSLCompileError(code="INVALID_SPEC/TRk")`; the executor gets ≤ 3 retries.
**Search.** CMA-ES on CRN paths per search world (M1–M6, B1), racing at 2,000 paths and confirming only promotion candidates at 10,000 (the per-kind table of §7.7; BUILD-30), Tier 1 through an augmented Lagrangian, type rules as sign constraints, successive halving with rungs of 2,000 / 6,000 / 10,000 paths per world (27 → 9 → 3 candidates, η = 3): 27 × 2,000 + 9 × 6,000 + 3 × 10,000 = 138k path-evaluations per world against 270k for 27 × 10,000, a ≈ 2× saving that sizes B8 (v1.0 claimed 3.9×; QUANT-33); scipy differential evolution is the pre-registered comparator. Fitness = Ψ_τ (no indicator or probability terms), computed on M1–M6 with the contract's model weights; B1 enters Gate 1's every-world clauses (T6 in the M1–M5 class band; non-inferiority) but never Ψ_τ (BUILD-38).
**Tests.** Planted leak fails to compile (TR1/TR2 drill); `test_no_payout_lever_in_mode_B`; `test_no_indicator_terms` (AST linter over `core/`, `idm/seats.py` and configs: fitness, objective and Θ may reference only J/Ψ/CE and engine cost metrics); `identity_check` true for every compiled residual at w = 0; CMA-ES solves sphere/Rosenbrock to 1e-8; successive halving keeps a planted best candidate in ≥ 95% of seeded runs.

---

### 4.25 `robust` (WP-22, wave 3)

```python
def ensemble_range(metric_by_world: Mapping[WorldId, float], weights: Mapping[WorldId, float]) -> tuple[float, float, float]
def kl_worst_prob(events: B, p: F64, eta: float) -> float
def kl_worst_expectation(loss: F64, p: F64, eta: float) -> float           # inf_ϑ ϑη + ϑ ln Σ p e^{ℓ/ϑ}
def kl_worst_cvar(loss: F64, p: F64, eta: float, alpha: float) -> float
def winf_threshold_prob(x: F64, threshold: float, shift: float, p: F64) -> float
def breakdown_eta(metric: Callable[[F64], float], threshold: float, p: F64) -> float
def k_ms(loss: F64, tau: float, p: F64) -> float                          # inf{k > 0: Σ p e^{(f − τ)/k} ≤ 1} for a LOSS f with target τ;
                                                                          # the 7% floor is k_ms(−R̄, −0.07, p) (QUANT-27)
def entropy_pool(G: F64, v: F64, ops: Sequence[Literal["eq", "le", "ge"]], p: F64, *, max_iter: int = 50, tol: float = 1e-10) -> "EPSolution"
def shrink_targets(G: F64, v: F64, p: F64, c: float = 0.6) -> F64          # v_eff = E_p[g] + c (v − E_p[g])
def reverse_stress(loss: F64, threshold: float, p: F64, features: F64) -> "ReverseStressResult"   # min-KL tilt to failure + Pesenti ranking
def persistence_tilt(regimes: I8, P_base: F64, P_alt: F64) -> F64         # path likelihood ratios (S-ADR-08)
def dro_rs_frontier(metric_paths: F64, p: F64, etas: Sequence[float], taus: Sequence[float]) -> "FrontierTable"
def robustness_card(pm: Mapping[WorldId, PathMetrics], metric_ids: Sequence[MetricId], cfg: "RobustConfig") -> "RobustnessCard"
```

**Algorithms.** Ensemble first (min, mixture, max over M1–M6), then KL balls (η = 0.05 swept 0.02–0.10; η_L = 0.01 for rare events; regime-conditional radii), W∞ (0.5pp), breakdown η*, k_MS (bp of floor per 0.01 nat); never stacked. Entropy pooling: minimize KL(q‖p) s.t. E_q[g_k] {=, ≤, ≥} v_k by Newton on the dual min_λ ln Σ_i p_i e^{λ′g_i} − λ′v (gradient E_q[g] − v, Hessian Cov_q[g]) with backtracking; inequality views by projected Newton on sign-constrained λ; stop at ‖grad‖∞ ≤ 1e-10·scale or 50 iterations. One ESS and KL rule, shared with the pack's W1 (§8.4; QUANT-32): Kish ESS warns below 0.5N and blocks below 0.2N; KL flags inform > 0.05, warn > 0.20, amber > 0.35 and red > 0.80 nats, consistent with the ESS floor because ESS/N = e^{−2KL} for a Gaussian tilt (≈ 0.5 at 0.35; ≈ 0.2 at 0.80, which forces W3); weight ratio ≤ 50.
**Performance.** B4 reference: `entropy_pool` < 1 s on 50,000 scenarios × 20 views.
**Tests.** EP views satisfied to 1e-10 and KL equal to the closed form for one Gaussian mean view; persistence weights average 1 (property); `robustness_card` reports ensemble range and KL tilt separately (no stacking); k_MS golden on the prototype vector with the loss sign, Σ p e^{(0.07 − R̄_i)/k} ≤ 1 (finite whenever some R̄_i < 7%; QUANT-27); the ESS and KL flags fire at the shared thresholds (QUANT-32).

---

### 4.26 `attrib` and `core.irb` (WP-23, wave 3)

```python
def kkt_interlock(sol: HSolution, col: Column) -> dict[str, float]          # ℓ̄ − s_B − f/T = λ_Lev + η − ζ, read on the column's reduced cost,
                                                                            # because every financing cost sits in the cash rows (ADR-42; QUANT-07)
def capability_values(lp: LPModel, sol: HSolution, capabilities: Sequence[str]) -> dict[str, float]   # re-solve without each capability
def price_of_safety(lp: LPModel, sol: HSolution, rows: Sequence[RowKey], eps_grid: Sequence[float]) -> "SafetyPriceTable"
def shapley_exact(value: Callable[[frozenset[str]], float], players: Sequence[str]) -> dict[str, float]          # ≤ 10 players
def shapley_permutation(value: Callable[[frozenset[str]], float], players: Sequence[str], *, n_perm: int = 32,
                        seed: int = 0) -> dict[str, tuple[float, float]]    # value, SE (path ⊕ permutation)
def group_shapley(ctx: SimContext, policy: PolicyRef, baseline: PolicyRef, tax: GroupRegistry, *, n_perm: int = 32,
                  paths: int = 10_000) -> dict[str, tuple[float, float]]   # n_groups + 2 players; exact only if 2ⁿ × cost fits the weekly budget,
                                                                          # else antithetic permutations with path ⊕ permutation SEs (BUILD-31)
def null_control(j_pi: float, j_p0: float, j_hold: float) -> "NullControl"  # scaffolding vs searched share (exact)
def what_moved_h(lp_prev: LPModel, lp_now: LPModel, *, n_steps: int = 16) -> dict[str, float]   # Aumann–Shapley path integral; grid error
def corridor_option_value(ctx: "SimContext", p0: PolicyRef) -> float      # S-ADR-20
def cash_buffer_test(ctx: "SimContext", tail_increment_a: float) -> "GTResult"   # S-ADR-15 (Gamba–Triantis)
def owner_mode_values(contract: AnalysisContract, ctx: "SimContext") -> "OwnerProposalReport"   # J*_A − J*_B, J*_H − J*_B (OWNER_PROPOSAL only)
def v8_replica(fixture: "V8Fixture") -> dict[str, float]                   # test_v8_replica
# core/irb.py
def info_relaxation_bound(policy: Policy, ctx: "SimContext", *, n_paths: int = 500,
                          penalty: Literal["zero", "terminal_value"] = "terminal_value") -> "IRBResult"   # upper, policy value, gap, SE
```

**Rules.** Prices first, counterfactuals second, decompositions third; always on CRN; attributions non-anticipative, ex ante across worlds, costed and Tier-1 filtered, with an anticipation audit; a component claim needs an ex-ante Shapley lower 95% bound ≥ 5bp a year in ≥ 2 worlds, else NOT ESTABLISHED; stand-alone attribution never shown alone.
**Tests.** Shapley efficiency exact; `regression/test_v8_replica.py` (±0.05pp per row; gap_05 §8) and the new-engine uplift in +0.35–0.61pp (SYNTHETIC); what-moved-H grid error reported and ≤ 1bp on the fixture; IRB upper ≥ policy value (property); null control decomposition exact.

---

### 4.27 `evaluator` and `seal` (WP-24, wave 3)

**Purpose.** The only tool host: an out-of-process evaluator per plane that verifies hashes, counts every call, runs engines, applies Gates 1–3 and writes the hash-chained ledger; the seal service holding the final-plane salt (ARCH §7.2, §7.5–7.6, §10.4; tool catalogue in §7.4).

```python
class EvaluatorService:                                     # implements EvaluatorPort
    def __init__(self, plane: Plane, contract: AnalysisContract, registry: Registry, stores: "StorePaths", *,
                 final_spawn: Mapping[WorldId, bytes] | None = None) -> None: ...
    # one typed method per tool in §7.4, e.g.:
    def evaluate_policy(self, req: EvalRequest) -> EvalResultAgentView: ...      # counted; full EvalRecord to the ledger
    def optimize_h(self, req: OptimizeHIn) -> HSummary: ...                     # v1.0's OptimizeHOut is removed (BUILD-11)
def make_server(plane: Plane, contract_path: Path) -> "MCPServer"   # evaluator/server.py: the one server factory; mcp_server.py dispatches (S-ADR-42)
def serve(plane: Plane, contract_path: Path) -> None        # MCP 2.3 stdio server; process started as `python -I -m adic_tpa evaluator serve`
class EvaluatorClient:                                      # implements EvaluatorPort over MCP stdio
    def __init__(self, plane: Plane, contract_path: Path, *, spawn: bool = True) -> None: ...
def check_hashes(ctx: "RequestContext", contract: AnalysisContract) -> None   # HashMismatch -> campaign ABORTED
class PlaneCache:                                           # key = sha256(source, snapshot, runtime, plane)
    def get(self, key: str) -> Any: ...                     # CacheMiss on miss or stale; never recompute silently
    def put(self, key: str, value: Any) -> None: ...
def gate1_correct(rec: EvalRecord, contract: AnalysisContract) -> GateOutcome
def gate2_selection(rec: EvalRecord, incumbent: EvalRecord, contract: AnalysisContract) -> GateOutcome
def gate3_qualification(finalists: Sequence[EvalRecord], comparator: EvalRecord, contract: AnalysisContract) -> tuple[GateOutcome, ...]
def bucket_delta_psi(delta_bp: float) -> str                # agent view rounding
# seal
def new_salt(campaign_id: CampaignId, salt_dir: Path, *, run_mode: RunMode) -> Path   # 256-bit; REAL: NTFS ACL to the CRO account;
                                                                       # DEV_SYNTHETIC: single-account software seal under runs/<run_id>/seal/,
                                                                       # commit–reveal still checked in code (S-ADR-37)
def commit(salt: bytes, contract_hash: str) -> str                     # SHA256(salt ‖ contract_hash)
def run_sealed(campaign_id: CampaignId, finalists: Sequence[PolicyRef], contract_path: Path) -> "SealedResult"   # spawns the FINAL evaluator once
def reveal(campaign_id: CampaignId) -> bytes
def verify_commit(salt: bytes, contract_hash: str, commitment: str) -> bool
```

**Gates.** Gate 1 `correct` (search and final): TR1–TR8; hard rows T1–T5 and T8 on every path (or on the glide path in recovery; failed paths worst-case); T6, T7, T9 within class bands (search: point estimate ≤ 0.8 × tolerance, screened at the 2,000-path race count and confirmed at 10,000 paths only for promotion candidates, per the evaluation kinds of §7.7; final: one-sided 95% CP bound ≤ tolerance); the Tier-1B floor on forward 10-year windows within its class bands (S-ADR-31); non-inferiority min_m[J_m(π) − J_m(comparator)] ≥ −5bp CE over `GateSpec.ni_worlds_search` = {M1–M6, B1} or `ni_worlds_final` = {M1–M6, B2}, with the comparator HOLD, or the restored Phase-II baseline in recovery; OV1–OV3; no pinned dual; no gambling signature; within budget. **Class membership** (QUANT-20): B1 and B2 belong to the M1–M5 class for T6, T7 and T9; misspecification worlds belong to the M6 class for T6 and are report-only for Tier 1B and non-inferiority. Gate 2: correct and ΔΨ̂ − 2·SE_boot > ε_mat vs the incumbent on paired CRN, Ψ_τ = −τ ln Σ_m w_m e^{−Ĵ_m/τ} over M1–M6, τ = 0.5pp, ε_mat = 3/5/10/15bp (overlay/pacing/REFI–LEVER/SELL); ties keep the incumbent; the relabelling signature is flagged to the auditor. Gate 3 (final, once): correct on the final plane; Holm-adjusted LCB95(ΔΨ vs comparator) > ε_mat; LCB95(ΔJ_m) > −5bp in every world; > 0 in ≥ 2 worlds, one of them B2, which claims call a **model-family hold-out** unless `PlaneSpec.b2_mode = "out_of_time"` (QUANT-19); PBO ≤ 0.20, computed by CSCV (≥ 8 blocks) on the **search ledger** (every counted search evaluation on common blocks) and reported at Gate 3, never computed on the sealed plane (`GateSpec.pbo_source`; QUANT-20); MDE ≤ ε_mat → QUALIFIED / NOT_QUALIFIED / NOT_CORRECT / NOT_ASSESSED. Increment 1 has no B2 (it arrives with WP-31): the sealed run uses fresh M1/M6 seeds, the held-out-family clause cannot be met, and the best attainable label is NOT_ASSESSED, which the pack shows as such ("zero qualified" is a valid outcome; ARCH §7.12).
**Process.** `python -I`, thread env vars set to 1, no network imports; read-only engine/config/store mounts; every request verifies engine, config, scenario, belief and snapshot hashes; each plane has its own cache directory; agents receive `EvalResultAgentView` only. Final-plane spawn keys exist only inside the process started by `run_sealed`. **Import hygiene:** `evaluator/__init__.py` imports nothing that pulls in engines; `evaluator/client.py` imports only `contracts`, `registry` and `mcp`, so `lab` and `idm` can use the client without loading engine code (layering test).
**Tests.** Drills (§7.13): tamper → ABORTED; over-budget → BUDGET_EXHAUSTED; search process opening the final store → permission error; cache drill; hash check at SEALED; commit/reveal round trip; `test_ni_comparator_restored_in_recovery`; agent view contains no metric values beyond the bucket.

---

### 4.28 `claims` (WP-25, wave 4)

```python
def extract_placeholders(text: str) -> tuple["Placeholder", ...]           # PLACEHOLDER_RE
def render(text: str, registry: Registry, scope: Sequence[RunId], *, plane_policy: Mapping[str, EvidencePlane]) -> RenderedDocument
def format_metric(m: MetricInstance, fmt: str) -> str                      # §8.3 grammar
def icd203_word(p: float) -> str | None
def validate(doc: RenderedDocument, registry: Registry, labels: Mapping[str, GateLabel], *, memory_refs: frozenset[str]) -> ValidationReport
def provenance_dag(ref: ArtifactRef, registry: Registry) -> ProvenanceNode
IMPROVEMENT_VERBS: frozenset[str]   # improves, improve, improved, beats, outperforms, significantly, superior, better than, raises, increases
DIGIT_WHITELIST: tuple[re.Pattern, ...]   # ISO dates, Qn-YYYY, years 1990–2040, § refs, register ids (Q1–Q10, A1–A9, E1–E4),
                                          # labels T1–T9, LR1–LR8, OV1–OV3, M1–M6, B1, B2, S-ADR-nn, WP-nn
```

**Validator rejects** (ARCH §10.6): literal digits outside the whitelist; unknown or wrong-plane metrics; improvement verbs on NOT_QUALIFIED or NOT_ASSESSED results or within MC error (|Δ| < 2 paired SE); probabilities without a range; citations to memory; synthetic numbers attributed to ADIC ("ADIC's …" next to a SYNTHETIC metric); claim coverage < 1; league tables; named-person regret; blueprint illustrative figures (+14.2%, 64% → 41%); briefs missing a P14 field; any LLM-originated numeric field (an `EffectForecast`, extraction confidence or extracted value not yet verified) rendered or aggregated (`LLM_NUMBER_RENDERED`; S-ADR-36); an analyst answer citing a reference not fetched in this turn under its context handle (`UNFETCHED_REF`; S-ADR-34).
**Tests.** Seeded fabricated-number memo fails; seeded overclaim fails; memo citing memory fails; ICD-203 bin edges; rendering golden for each format.

---

### 4.29 `agents` (WP-25, wave 4) — full specification in §7

```python
@dataclass(frozen=True) class LLMRequest: role: RoleId; model: str; system: str; messages: tuple[dict, ...]; tools: tuple["ToolDef", ...]
                                          effort: str; max_tokens: int = 16000
                                          thinking: Mapping[str, str] = field(default_factory=lambda: {"type": "adaptive"})   # BUILD-34
@dataclass(frozen=True) class LLMResponse: content: tuple[dict, ...]; parsed: BaseModel | None; stop_reason: str; served_model: str
                                           usage: Mapping[str, int]; record: LLMCallRecord
class AnthropicBackend: ...   # implements LLMBackend; §7.2
class ReplayBackend:   ...    # two-tier keys (S-ADR-41): structural_key selects the cassette (miss → ReplayMiss, fails closed); then the
                              # full request_digest is compared (mismatch → ReplayDrift; Stub fallback only in non-gating tests)
class StubBackend:     ...    # seeded, schema-valid, rule-based outputs (e.g., DSL-grammar sampling)
def structural_key(req: LLMRequest, state: CampaignState, turn: int) -> str        # role, state, prompt hash, tool-schema hash, turn index
def request_digest(req: LLMRequest, output_model: type[BaseModel] | None = None) -> str   # SHA-256 of the canonical request as sent
def check_llm_schema(model: type[BaseModel]) -> None   # runs the SDK's strict-schema transform; rejects empty-object and prefixItems fields (S-ADR-36)
def make_backend(spec: LLMSpec, role: RoleLLMSpec, registry: Registry) -> LLMBackend    # TPA_LLM_MODE ∈ {offline, replay, live}
class Gateway:
    def redact(self, req: LLMRequest, spec: LLMSpec) -> LLMRequest: ...  # tokenizes owner fiscal items, counterparties, GP names
    def send(self, req: LLMRequest, backend: LLMBackend, output_model: type[BaseModel] | None) -> LLMResponse: ...
def run_role(role: RoleId, state: CampaignState, inputs: BaseModel, backend: LLMBackend, tools: "ToolRegistry",
             *, max_retries: int = 3) -> BaseModel                         # manual tool loop; submit_<artifact> re-validated by pydantic
```

---

### 4.30 `lab` (WP-26, wave 4) — states and budgets in §7.6–7.9

```python
class MetaController:
    def __init__(self, contract: AnalysisContract, registry: Registry, evaluator: EvaluatorPort, room: RoomPort,
                 backends: Mapping[ModelFamily, LLMBackend], seal: "SealClient", cfg: "LabConfig") -> None: ...
    def run(self, *, until: CampaignState = CampaignState.CLOSED, campaign_enabled: bool = True) -> CampaignState: ...
    def step(self) -> CampaignState: ...
    def escalate(self, e: Escalation) -> None: ...
    def resolve(self, escalation_id: str, resolution: str, signer: SignOff) -> None: ...
    def status(self) -> "CampaignStatus": ...
class BudgetLedger:   def charge(self, kind: Literal["eval", "tuning_eval", "usd", "core_s", "cycle"], amount: float) -> None: ...   # BudgetExhausted
class CampaignMemory: def append(self, ev: MemoryEvent) -> None: ...; def conclusions(self, worker: int) -> str: ...; def close(self) -> None: ...
class MapElitesArchive: def add(self, bundle: IdeaBundle, descriptor: tuple[float, ...], score: float) -> bool: ...; def underfilled(self) -> list[tuple[int, ...]]: ...
class ToolFirewall:   def allowed(self, role: RoleId, state: CampaignState, tool: str) -> bool: ...   # a disallowed call gets an is_error tool
                      # result; each role's tool list stays fixed for the life of a transcript and a state change starts a new transcript,
                      # so prompt caching and preserved thinking survive (S-ADR-41; BUILD-39)
def stop_rule(history: "CampaignHistory") -> bool    # budget spent, 6 cycles without promotion, or no positive robust reduced cost
```

---

### 4.31 `idm` (WP-27, wave 4) — room protocol in §8

```python
def load_register(path: Path) -> Register                                   # signed YAML; Ed25519 signatures verified against the roster (S-ADR-40)
def compile_agenda(reg: Register, quarter: str, snapshot_hash: str, contract: AnalysisContract) -> EvidencePlan
def resolve_evidence(plan: EvidencePlan, evaluator: EvaluatorPort, registry: Registry) -> "EvidenceStatus"
def build_brief(item: DecisionType, status: "EvidenceStatus", writer: Callable[..., RenderedDocument]) -> RenderedDocument   # "EVIDENCE MISSING: <metric>"
def make_seats(tax: GroupRegistry, theta_path: Path) -> tuple[SeatSpec, ...]   # n_groups + 5 (S-ADR-22)
def implied_actions(seat: SeatSpec, item_id: str, evaluator: EvaluatorPort) -> ArtifactRef   # the only source of seat numbers: J under the seat's
                                                                            # (q_k, θ_k) over the item's finite option set by exact re-weighting of cached
                                                                            # CRN paths; an H re-solve only when the seat's belief channel needs re-fusion
                                                                            # (BUILD-07)
def regret_table(seats: Sequence[SeatSpec], options: Sequence[OptionSummary], evaluator: EvaluatorPort) -> "RegretTable"
def belief_value_split(seat: SeatSpec, option: OptionSummary, evaluator: EvaluatorPort) -> tuple[float, float]
def minority_trigger(dp_pp: float, regret_bp: float) -> bool               # |Δp| ≥ 15pp or regret ≥ 10bp CE; Δp is the difference between ENGINE
                                                                            # probabilities of a frozen-question event under the seat's beliefs and under
                                                                            # the base mixture, never an LLM-stated number (S-ADR-36; QUANT-10)
def diversity_alarm(rank_corr: F64) -> bool                                 # any pairwise > 0.9
def lock_prevote(pv: PreVote, registry: Registry) -> str
def tally(ballots: Sequence[Ballot], recusals: Mapping[str, Sequence[GroupId]], item_group: GroupId | None) -> "TallyResult"   # recused votes recorded, not tallied
def consent_eligible(item: DecisionType, evidence: "EvidenceStatus") -> bool
def evsi_crossfit(item_id: str, evaluator: EvaluatorPort, *, folds: int = 2) -> "EVSIResult"
def defer_allowed(evsi_lb80: float, cost_of_delay: float, staged_dominates: bool, prior_deferrals: int) -> bool
def find_signposts(decision_id: str, evaluator: EvaluatorPort, k: int = 4) -> tuple[Signpost, ...]   # root-finding on the flip condition
def append_decision(rec: DecisionRecord, registry: Registry) -> None
class RoomService: ...                                                       # implements RoomPort; pre-votes and ballots come from an injected
                                                                             # ballot source: humans in REAL mode, testing.synthetic_committee
                                                                             # (labelled SYNTHETIC) in DEV_SYNTHETIC mode (S-ADR-37)
```

---

### 4.32 `pack` (WP-28, wave 4) — sections and payload in §8

```python
def build_pack(quarter: str, registry: Registry, run_ids: Sequence[RunId], out_dir: Path, *, theme: "PackTheme | None" = None) -> "PackManifest"
def ep_payload(pm: Mapping[WorldId, PathMetrics], metric_ids: Sequence[MetricId], *, n_paths: int = 10_000, seed: int = 0) -> "EPPayload"
def golden_ep_cases(payload: "EPPayload", views: Sequence[Sequence[ViewSpec]]) -> tuple["EPGolden", ...]   # via robust.entropy_pool artifacts
def figure_html(spec: "FigureSpec", data: Mapping[str, Any], theme: "PackTheme") -> str
def lint_pack(html: str, payload: Mapping[str, Any]) -> ValidationReport
```

---

### 4.33 `cli` and `mcp_server` (WP-29, wave 4) — command list in §7.12, servers in §7.11

```python
app: typer.Typer                                                          # cli.py; JSON logs; non-zero exit on any TPAError
def serve(server: Literal["evaluator", "analyst"], plane: Plane, contract_path: Path, *, quarter: str | None = None) -> None
                                                                          # mcp_server.py dispatches only: evaluator.server.make_server and
                                                                          # analyst.server.make_server own the factories (S-ADR-42)
```

---

### 4.34 `pipeline` (WP-30, wave 5)

```python
class QuarterResult(BaseModel): campaign_id: CampaignId; final_state: CampaignState; pack_path: Path; manifests: tuple[RunId, ...]; labels_audit: float
def run_quarter(asof: date, *, synthetic: bool = True, llm_mode: LLMMode = LLMMode.OFFLINE, campaign: bool = False,
                allocation: AllocationId = "v2", census: CensusId | None = None, root_seed: int = 20261018,
                out_root: Path = Path("runs")) -> QuarterResult                      # quarter.py
class MonthlyResult(BaseModel): asof: date; cfp: CFPReading; signpost_alarms: tuple[str, ...]; event_decisions: tuple[DecisionId, ...]
def run_monthly(asof: date, *, synthetic: bool = True, llm_mode: LLMMode = LLMMode.OFFLINE) -> MonthlyResult   # cycle.py: CFP readings,
                                                                                    # signpost monitor, E1–E4 via the compressed protocol (W2, EXPLORATORY)
```

Composition root: builds the synthetic release (or freezes real data), the snapshot and state, drafts the contract from `contract_templates/decision_quarter.yaml`, starts the search evaluator process, wires `lab.MetaController` with `idm.RoomService`, runs to CLOSED, and builds the pack. In `run_mode = DEV_SYNTHETIC` (S-ADR-37; BUILD-18) it signs with the fixed test key labelled SYNTHETIC (S-ADR-40), seals with the single-account software seal and injects `testing.synthetic_committee` as the room's pre-vote and ballot source, so the FSM reaches CLOSED unattended on one Windows account; L0 prints the mode. REAL mode refuses all three (`RunModeRefused`); ACL drills that need separate accounts are marked `requires_accounts` and run only where those accounts exist.

---

### 4.35 `analyst` (WP-39 increment 1; WP-40 v1) — full design in `design/addenda/CHAT_ANALYST.md`

**Purpose.** The conversational analyst of brief R16 (ARCH §8.12; S-ADR-34): one deterministic `AnalystService` behind three thin surfaces (`tpa chat`, the read-only analyst MCP server, the pack's Ask panel). The LLM chooses tools and writes connective prose around placeholders; it never computes a number.

**Binding source.** CHAT_ANALYST v1.0 specifies the tool contract (§5.1), the 30-tool catalogue (§5.2), the input and payload models (§5.3), the what-if protocol with `OverrideConfirmation` and `ConfirmToken` (§6), explanations (§7), sessions and context handles (§8), the access matrix AR-1 to AR-11 and information barriers (§9), security (§10), logging with the ledger kinds `chat_session`, `chat_turn`, `override_draft`, `override_confirmation`, `whatif_run`, `access_denial` and `decision_link` (§11), evaluation (§12) and budgets (§13). This spec adds only the following.
- **Overrides by v1.1 rules:** W1 previews use the shared ESS and KL rule of §8.4 and §4.25 (ESS warn < 0.5N, block < 0.2N; KL 0.05 / 0.20 / 0.35 / 0.80), not the addendum's 1.20 and 2.30 nats; Replay uses the two-tier keys of S-ADR-41.
- **Imports:** `analyst` may import `contracts`, `registry`, `claims`, `agents` and `evaluator.client` (§4.0); it reads through `Registry(readonly=True)` and runs confirmed what-ifs only on the exploration plane.
- **Forecast intake** moves off every LLM-facing surface to the human command `tpa forecast register` (operator token).
- **Work packages:** WP-CHAT-01 in WP-01 (wave 0); WP-CHAT-02–04, 06, 07, 09, the W1/W2 part of 05 and the Stub/Replay part of 10 in WP-39 (waves 4–5); the W3 part of 05, 08 (Ask service), the live part of 10 and 11 in WP-40 (waves 6–7).

**Performance.** B18: cached answer ≤ 5 s (tool P95 ≤ 300 ms); W1 < 1 s; W2 ≤ 60 s with progress and cancel; W3 returns a run handle within 2 s.
**Tests.** The 140-item golden set (`design/addenda/chat_golden_questions.json`) on Stub in `pr` and on Replay nightly, with 100% number provenance, label correctness and zero access violations (CHAT_ANALYST §12.2); `run_whatif` never succeeds before a human confirmation (fuzzed); a W1 chat number equals `robust.entropy_pool` to 1e-12; the read-only drill (every write path from the analyst process is refused); CLI–MCP parity; ≥ 300 items in v1 with pass³ ≥ 0.9 on what-if translation.

---

## 5. The here-and-now program H

H is a node-wise sparse tree LP built from the ledger kernel's linear rows (ADR-02, ADR-03), solved on HiGHS through `highspy` from `scipy.sparse` matrices (cvxpy only for fixture-size reference models), in W₀ units, maximizing a PWL proxy of J subject to Tier-1 rows, after a lexicographic Phase I. Sizes below are for the **quarterly default preset** (576 leaves × 8 periods) on the v2 taxonomy; v1 figures in parentheses. ARCH §5.4 quotes this recount; the B2 benchmark (§5.14) governs. The v1.1 accounting (S-ADR-33; ARCH ADR-42) corrects six v1.0 errors: unfunded commitments now transfer to the buyer on a sale (QUANT-04); terminal wealth and W_n carry Real Assets debt, posted IM and residual overlay value (QUANT-05); red-margin capacities are linear in the state (QUANT-06); every cost is charged once, in cash, with no money term in the objective (QUANT-07); NAV rows use simple returns with compounded fan coefficients and period-length lag mapping (QUANT-15); and H5 uses a quarterly rate (QUANT-34).

### 5.1 Index sets

| Set | Meaning | Size v2 (v1) |
|---|---|---|
| 𝒩 | tree nodes: root, 24 Q1, 24 Q2 (pass-through), 24 Q3 (pass-through), 96 Q4, 576 × 4 fan nodes (Q6, Q8, Q10, Q12) | 2,473 |
| 𝒩_P ⊂ 𝒩 | pricing nodes: root and Q1–Q4 nodes | 169 |
| ℒ ⊂ 𝒩 | leaves (Q12 fan nodes), each tagged with one world | 576 |
| 𝒢_p | private groups (`GroupRegistry.private()`): PE, SECONDARIES, CAPSOL, COINVEST, PRIVCREDIT, REALASSETS | 6 (5) |
| 𝒜 | age buckets {young, mature} | 2 |
| 𝒞 | T6 classes {M1, …, M6, MIX} | 7 (3 in the MVP: M1, M6, MIX) |
| 𝓜 | worlds M1–M6 | 6 (2 in the MVP) |
| 𝓗 | months 1–24 for T4′ root rows | 24 |
| 𝓢 | named overlay stresses (1987-type, 2018-type, 2020-type, V3 entry) | 4 |
| 𝓩 | T8 shock types {DB, GW, SG + peg} | 3 |
| 𝓡 | root lens columns (cohort pro-rata SELL by group × age, REFINANCE by instrument, LEVER/ADD by instrument, facility sizing, tail-ladder notional, opportunistic budget) | ≈ 34 (30) |
| 𝓕 | facilities in the model: revolver (priced only in R1 and above), NAV facility (capacity-capped), repo, term pre-funding (S-ADR-12) | 4 |
| 𝒥 | convex-cost segments at pricing nodes, for the eight sale variables (long-only, 3 amber, 4 red) and the revolver and NAV-facility balances | 3 |

### 5.2 Variable inventory

All money variables are in W₀ units (W₀ = opening NAV, $177bn SYNTHETIC). Decisions at node p act during the periods of p's children.

| Symbol | Meaning | Index | Per node v2 (v1) | Bounds |
|---|---|---|---|---|
| C_n | unencumbered haircut cash + HQLA (CF-controlled; posted IM excluded) | n ∈ 𝒩 | 1 | ≥ 0 |
| V_{g,a,n}, U_{g,a,n} | economic NAV (Real Assets directs and JVs at gross asset value) and unfunded by private group × age | g ∈ 𝒢_p, a ∈ 𝒜 | 12 + 12 (10 + 10) | ≥ 0 |
| D^RA_n | RA non-recourse asset debt (look-through); D^RA_n = (1 − amort_n)D^RA_p + x^ra_p | n | 1 (0) | ≥ 0 |
| LO_n, HF_n, Q_n | long-only NAV, un-noticed HF NAV, HF queue | n | 3 | ≥ 0 |
| F^rev_n, F^nav_n, F^repo_n, F^term_n | facility balances | n | 4 | [0, limit × availability] |
| B^p2s_n, B^β_n | P2S notional; other synthetic-beta notional | n | 2 | ≥ 0 |
| N^tail_n, O_n | tail-ladder notional; opportunistic risk scale | n | 2 | ≥ 0 |
| IM_n | posted initial margin (encumbered, still ADIC's asset) | n | 1 | ≥ 0 |
| K_n | accumulated non-cash charges: K_n = K_p + Σ_g κ^GP_g s^red_{g,p} | n | 1 | ≥ 0 |
| W_n | wealth, defined by its own row H1-W (v1.0 had no definition row) | n | 1 | free |
| B_n | draw basis: reported NAV at the opening of node n's fiscal year (carried; reset by a linear NAV proxy at FY-open nodes) | n | 1 | ≥ 0 |
| R_n | red-margin running maximum | n | 1 | free |
| s^LO_n | long-only sales | n | 1 | [0, LO] |
| ν_n | HF notices (non-zero only at notice-date nodes) | n | 1 | [0, HF] |
| y^p2s_n, y^add_n | P2S conversion; beta addition (separate variables) | n | 2 | ≥ 0 |
| f^±_{k,n} | draw / repay per facility | k ∈ 𝓕 | 8 | ≥ 0 |
| k_{g,n} | new commitments (enter U with a 2-quarter lag, S-ADR-20) | g ∈ 𝒢_p | 6 (5) | [0, corridor × plan] |
| s^amb_{g,n} | amber sales / redemptions: PRIVCREDIT, CAPSOL, RA open-end | | 3 (2) | [0, depth] |
| s^red_{g,n} | red sales: PE, SECONDARIES, COINVEST, REALASSETS | | 4 (3) | [0, depth] |
| ρ_n | SMA run-off share | n | 1 | [0, 1] |
| μ^tail_n, o_n | tail notional monetized; opportunistic scale-down (both in notional, so the cash row stays linear) | n | 2 | [0, N^tail], [0, O] |
| d^cb_{g,n} | contingent-budget deployment (SECONDARIES, CAPSOL, PRIVCREDIT) | | 3 | [0, budget] |
| r^top_n | Treasury top-up from DM equities (CF authority, R0) | n | 1 | ≥ 0 |
| x^ra_n | RA cash-out refinancing (R0x, S-ADR-02) | n | 1 (0) | [0, LTV headroom] |
| σ_{v,j,n} | convex-cost segments j ∈ 𝒥 of the eight sale variables and of F^rev, F^nav; each parent variable equals the sum of its segments (row SEG) | n ∈ 𝒩_P | 30 (24) | [0, segment width] |
| e^app | elastics on APPETITE rows only: T2 8% at pricing nodes; T4′ on Treasury + Public Markets at the root (24 months, no facility credit; S-ADR-32) | 𝒩_P; h ∈ 𝓗 | 169 + 24 | ≥ 0 |
| x_r | root lens columns (convex combinations of asset columns) | r ∈ 𝓡 | root only | [0, 1] |
| u_ℓ, ψ_ℓ, W̃_ℓ | utility hypograph, shortfall epigraph, terminal wealth | ℓ ∈ ℒ | 3 per leaf | free / ≥ 0 / free |
| η_c, z_{c,ℓ} | T6 CVaR auxiliaries (world classes use their leaves; MIX uses all) | c ∈ 𝒞 | 7 + 1,152 | free / ≥ 0 |
| η′_m, z′_ℓ | Tier-1B CVaR auxiliaries | m ∈ 𝓜 | 6 + 576 | free / ≥ 0 |

**Sales by age** (S-ADR-33; QUANT-04, BUILD-23). Node sale variables are by group. A group sale s_{g,n} is split across age buckets by the fixed contract rule `sale_age_allocation` (default `pro_rata_ref`: the node's reference NAV shares w^age_{g,a,n} = `NodeCoefficients.nav_share`; `mature_first` is the alternative), so no per-age sale variables exist; the buyer assumes κ^U_{g,a,n} of unfunded per $ of NAV sold (`NodeCoefficients.u_per_nav`; 0.53 for PE on the research book, G-gap_01 §2.3), exact under positive homogeneity for pro-rata sales (error-ledger A19). **Unit financing** (BUILD-24): REFINANCE and LEVER balances created by root lens columns enter H through the columns' exact node cash-flow vectors (draw, service, amortization and forced paydowns, computed by the owning engine's `UnitFinancing` on the tree's paths) and, once an action is fixed, through Δ_n; the recourse-debt row (H2d) reads the balances as column coefficients.

**Count:** per node 42 states + 33 decisions in v2 (37 + 29 in v1); 2,473 × 75 = 185,475 (163,218) + 5,070 (4,056) segment columns at the 169 pricing nodes + 34 (30) root + 1,728 leaf + 1,159 T6 and 582 Tier-1B CVaR columns + 193 appetite elastics ≈ **194k columns (171k)**.

### 5.3 Constraint inventory

| ID | Family (RowFamily, RowRole) | Form (W₀ units) | Index | Count v2 |
|---|---|---|---|---|
| H1 | TRANSITION (DEFINITION) | σ_n = Φ_n σ_{p(n)} + B_n y_{p(n)} + c_n + Δ_n, one equality per carried state (every state but W and R); coefficients from `ledger.linear.node_transition_rows` on the tree's node coefficients: simple returns, fan-period coefficients compounded over their two quarters (§3.7), lags mapped to node ancestry by period length | n ≠ root, 40 states | 2,472 × 40 = 98,880 |
| H1-cash | (the cash row of H1) | C_n = (1 + r^c_n)C_p + Σ_{g,a}(δ + inc)_{g,a,n}(V_{g,a,p} − w^age_{g,a,p}s_{g,p}) − Σ_{g,a} q_{g,a,n}(U_{g,a,p} − κ^U_{g,a,p}w^age_{g,a,p}s_{g,p}) + Σ_g b_{g,n}s_{g,p} − Σ_{v,j} c^seg_{v,j}σ_{v,j,p} + (1 − τ^LO_n)s^LO_p + φ^HF_n ν_{p′} + (1 − h^IM)y^p2s_p + r^top_p + x^ra_p + Σ_k(f^+_{k,p} − f^−_{k,p}) − Σ_k r^F_{k,n}F_{k,p} − Σ_{k,j} c^F_{k,j}σ_{k,j,p} − Σ_k fee_k(limit_k − F_{k,p}) − (ra_debt_rate + ra_amort)_n D^RA_p − d_nB_n − vm_n(B^p2s_p + B^β_p) − ΔIM_n − prem_n N^tail_p + v^tail_n μ^tail_p + opp_n O_p − opex_n W_p + Δ_n, where s_{g,p} is the group's amber or red sale, r^F includes the base rate, spread and the S-ADR-12 tightening premium, c^seg and c^F are the convex excess per segment (pricing nodes; fan nodes use the top segment's rate, A23), d_n B_n is the node's owner instalment, and prem, v^tail and opp are the per-unit overlay coefficients of `OverlayStressCoeffs`' basis (premium, payoff at monetization, opportunistic P&L incl. its VM; QUANT-15) | | |
| H1-NAV | | V_{g,a,n} = (1 + R_{g,a,n} − δ_{g,a,n})(V_{g,a,p} − w^age_{g,a,p}s_{g,p}) + q_{g,a,n}(U_{g,a,p} − κ^U_{g,a,p}w^age_{g,a,p}s_{g,p}) + age migration, with R the **simple** return e^r − 1 (QUANT-15); U_{g,a,n} = (1 − q_{g,a,n})(U_{g,a,p} − κ^U_{g,a,p}w^age_{g,a,p}s_{g,p}) + k_{g,lag(n)} for the young bucket, lag(n) = the ancestor two quarters back (the grandparent at quarterly nodes, the parent at semiannual fan nodes); K_n = K_p + Σ_g κ^GP_g s^red_{g,p}; D^RA_n = (1 − ra_amort_n)D^RA_p + x^ra_p | | |
| H1-W | WEALTH (DEFINITION) | W_n = C_n + IM_n + LO_n + HF_n + Q_n + Σ_{g,a}V_{g,a,n} − D^RA_n − Σ_k F_{k,n} + v^tail_n N^tail_n (QUANT-05) | n | 2,473 |
| SEG | SEGMENT (DEFINITION) | each segmented variable equals the sum of its segments | n ∈ 𝒩_P, 10 per node | 1,690 |
| H2a | T2_IG_HARD (PRICING) | C_n ≥ 0.04 W_n (C is unencumbered, so posted IM is already excluded) | n ∈ 𝒩 | 2,473 |
| H2b | T2_IG_TARGET (APPETITE) | C_n + e^app_n ≥ 0.08 W_n; dual excluded from λ and cards | n ∈ 𝒩_P | 169 |
| H2c | T3_COV30 (PRICING) | haircut HQLA ≥ 30-day need (VM statistic per `t3_vm_stat`, facilities 0%) | root, Q1 | 25 |
| H2d | T5_EXPOSURE, T5_DEBT, T5_ENCUMBRANCE (STRUCTURAL) | exposure ≤ 1.30 W; recourse debt (facilities + unit financing) ≤ 0.15 W (0.10 target as appetite); encumbrance (incl. IM) ≤ 0.20 assets | n | 3 × 2,473 |
| H2e | LR8 (STRUCTURAL) | Σ(V + U) ≤ 0.80 W (ADIC limit pending) | n | 2,473 |
| H2f | NAVF_LTV, RA_LTV (STRUCTURAL) | F^nav ≤ LTV_stressed × pledged reported NAV; D^RA ≤ LTV_max × ra_direct_share × V^RA (the gross value of the levered directs and JVs) | n | 2 × 2,473 |
| H2g | SALE_DEPTH (STRUCTURAL) | s^amb_g, s^red_g ≤ depth_{g,n} Σ_a V_{g,a,n} (5% of strategy depth per half-year at regime success rates) | n, 7 groups | 7 × 2,473 |
| H2h | HF_NOTICE, P2S_CAP, FAC_AVAIL (STRUCTURAL) | ν ≤ notice capacity; B^p2s ≤ cap (0.30 W gross overlay incl. P2S, Q5); F_k ≤ size × availability(S, Z, f) (≤ 0.5 in joint oil–crisis, S-ADR-12) | n | 4 × 2,473 |
| H3 | RED_MARGIN (PRICING) | R_n ≥ R_{p(n)}; R_n ≥ g^red_n(σ_n) = O^next_n − [C_n − 0.04W_n + LiqCap_n + FacCap_n + AmberCap_n], the signed shortfall of non-red resources, every term linear in the node's state (S-ADR-33; QUANT-06): O^next_n = Σ_{g,a} call_stress_12m_{g,a,n}U_{g,a,n} + 4d_nB_n + 4Σ_k(r^F + amort)_{k,n}F_{k,n} + 4(ra_debt_rate + ra_amort)_n D^RA_n + 4 opex_n W_n; LiqCap_n = (1 − τ^LO_n)LO_n + φ^{12m}_n HF_n; FacCap_n = Σ_{k signed}(fac_avail_{k,n} limit_k − F_{k,n}); AmberCap_n = Σ_{g amber} amber_depth_{g,n} b_{g,n} Σ_a V_{g,a,n}. Converting $1 of a non-red resource into cash therefore leaves the row unchanged | n | 2 × 2,473 |
| H4 | T6_CVAR (PRICING) | η_c + (1/ε′_c) Σ_{ℓ∈c} p_{ℓ\|c} w^lr_ℓ z_{c,ℓ} ≤ b^red_c; z_{c,ℓ} ≥ R_ℓ − η_c; ε′_c = 1 − (1 − ε_c)^{12/20} (0.60% at 1%; 1.51% at M6's 2.5%) | c ∈ 𝒞 | 7 + 1,152 |
| H5 | FLOOR_CVAR (PRICING) | η′_m + 10 Σ_{ℓ∈m} p_{ℓ\|m} z′_ℓ ≤ b^floor_m; z′_ℓ ≥ −NPV_ℓ − η′_m with NPV_ℓ = W̃_ℓ − (1 + r_{f,q})^{12}·1 (the quarterly rate over the tree's 12 quarters; QUANT-34) | m ∈ 𝓜 | 6 + 576 |
| H6a | T4P (PRICING) | hd_h(0) + Σ_{r∈𝓡} s_{r,h} x_r + Σ_ℓ s^lev_{ℓ,h} y^root_ℓ ≥ −g_h (slopes by finite differences on `ledger.stress_replica` under the pricing conventions, step $0.1bn; re-verified exactly at the solution, re-linearized ≤ 3 times) | h ∈ 𝓗 | 24 |
| H6b | T8_DCR (PRICING) | stressed 12-month resources_z(x₀) ≥ 1.0 × outflows_z | z ∈ 𝓩 | 3 |
| H6c | LR4 (PRICING at 24m; reported at 12m) | per horizon: one pool row Σ_g B_{g,h} + B_{OVL,h} ≤ Pool_h(x₀) and one budget row LC_g ≤ B_{g,h} per private group and the Overlay | h ∈ {12, 24} | 2 × (6 + 2) = 16 (14) |
| H6d | OV1, OV2 (STRUCTURAL) | NV^eq_ovl(s) − 0.75 NV^eq_tail(s) ≥ 0; −P&L_opp(s) − 0.25 P&L_tail(s) ≤ 0 (linear in root overlay columns, given precomputed revaluations) | s ∈ 𝓢 | 8 |
| H6e | DEALER, TAIL_BUDGET, T5 at root | dealer ≤ 0.5% NAV; 0.15% ≤ tail premium ≤ 0.50% NAV a year; ≤ 20% of debt maturing in 12 months | root | ≈ 10 |
| H6f | T4P_APPETITE (APPETITE) | hd^TP_h(x₀) + e^app_h ≥ 0: survival for 24 months on Treasury + Public Markets alone, no facility credit (S-ADR-32; v1.0 carried a 36-month row the 24-month replica could not evaluate, QUANT-09) | h ∈ 𝓗 | 24 |
| H7 | non-anticipativity | by construction: one decision vector per node, nodes built on pooled observables | — | — |
| UTILITY | (DEFINITION) | u_ℓ ≤ a_k(W̃^real_ℓ) + b_k, k = 1…48 tangents of U₃(x) = x^{1−γ}/(1−γ), placed by `numerics.adaptive_tangent_points` at weighted quantiles of the previous solve's leaf wealth (P1–P99; first solve: HOLD's simulated leaf wealth); v1.0's 8 tangents carried a PWL error of 12–84bp a year of CE (QUANT-18, BUILD-19) | ℓ | 48 × 576 = 27,648 |
| SHORTFALL | (DEFINITION) | ψ_ℓ ≥ secant pieces of ((1 − W̃_ℓ/W̃*_ℓ)+)^p, p = 2, breaks (0, 0.05, 0.10, 0.20, 0.35, 0.50); W̃*_ℓ from the pre-committed target path (S-ADR-06) | ℓ | 3,456 |
| TERMINAL | (DEFINITION) | W̃_ℓ = C + IM + LO + HF + Q + Σ_g ω^T_g V_g − Σ_g ψ^T_g U_g − Σ_k F_k − D^RA + v^tail_ℓ N^tail + m^opp_ℓ O − K_ℓ + A_ℓ, with ω^T, ψ^T the regression terminal values (§5.12), posted IM (still ADIC's asset), the residual MTM of the tail and opportunistic books (VM-settled positions are already in cash), the accumulated charges K, and A_ℓ the distributions accrued at the leaf's exogenous static-SAA return, so the objective stays affine (S-ADR-33; QUANT-05) | ℓ | 576 |

**Count:** 98,880 (H1) + 2,473 (H1-W) + 1,690 (SEG) + 44,708 (H2a–H2h) + 4,946 (H3) + 1,159 (H4) + 582 (H5) + 85 (H6a–H6f) + 27,648 (UTILITY) + 3,456 (SHORTFALL) + 576 (TERMINAL) = 186,203 ≈ **186k rows (166k)**, ≈ 1.0M non-zeros. v1.0 counted 157k rows; the increase comes from the 48 utility tangents (+23k), three more carried states, the W_n definition rows and the segment rows. ARCH §5.4 quotes this recount.

### 5.4 Objective

max Σ_{ℓ∈ℒ} p_ℓ [u_ℓ − λ^H_T ψ_ℓ]

**There is no money term in the objective** (S-ADR-33; ARCH ADR-42; QUANT-07). Every cost is charged once, in money that flows into W̃: the base rate, spread, linear impact τ, fees and the S-ADR-12 tightening premium (TIGHT/CLOSED windows) in the cash rows; the convex excess of price impact and of the funding curves c_k(B, z) = r_t + σ_k(z) + η_k(z)(B/B̄_k)² through segment variables with rising unit costs at pricing nodes (fan nodes use the top segment's linear rate, error-ledger A23); κ^GP relationship charges on red sales through the accumulated-charge state K, which TERMINAL subtracts. v1.0 charged financing and impact in the cash rows and again as an objective penalty, and added money to utility without ū′ scaling. λ^H_T is tuned by `core.mpc.calibrate_buffers` until the H–P ranking test passes (Kendall τ ≥ 0.8). A risk-neutral terminal objective is rejected (JQ-MF12).

### 5.5 Assembly (`core.h.build_h`)

1. `VarIndex`: root columns first, then nodes in depth-first order (block locality); every column gets a `ColKey`. Lens columns arrive from `actions.build_columns` with coefficients keyed by `RowKey` and are mapped by `core.h.row_index(lp)`; call order: tree → root coefficients → `build_h` → columns → price → select (BUILD-22).
2. For each node: H1 rows from `ledger.linear.node_transition_rows(tree.coef, n, parent, vidx)`; H1-W; SEG rows at pricing nodes; H2 limits; H3 red-margin rows built from the node's state.
3. For each leaf: TERMINAL, UTILITY (48 adaptive tangents), SHORTFALL, H4/H5 auxiliaries.
4. Root rows: H2c, H6a–H6f (`ledger.linear.t4p_root_rows` under the pricing conventions, `actions` catalogue coefficients, `overlay.stress_coefficients`).
5. Scaling: all money in W₀ units; assert max |a_ij| ≤ 1e4 and every penalty ≤ 1e4; warn on coefficients < 1e-9.
6. Roles and Phase-I tiers from `ledger.ROW_FAMILIES`; `LPModel.meta` records tree, contract, catalogue and ledger hashes.
7. In recovery, hard-row bounds are shifted by the glide path g^rec; **no elastic variable is ever attached to a hard row in a Phase-II model** (checked by `assert_no_pinned_duals`). T6-consuming root SELL columns (S-ADR-30) get upper bound 0 in Phase II and are priced by forced re-solve.

### 5.6 cvxpy reference formulation (fixture trees only)

Used by `tests/solver/test_cvxpy_reference.py` on trees of ≤ 50 leaves to cross-check `build_h` row by row, and nowhere in production (canonicalizing 10⁶ non-zeros through cvxpy is avoidable overhead; PA §4.8.3).

```python
def reference_h(tree: Tree, ls0: LedgerState, cat: ActionCatalogue, c: AnalysisContract) -> cp.Problem:
    S = cp.Variable((N, n_state)); Y = cp.Variable((N, n_dec), nonneg=True); X = cp.Variable(n_root, nonneg=True)
    u = cp.Variable(L); psi = cp.Variable(L, nonneg=True); Wt = cp.Variable(L)
    eta = cp.Variable(n_class); z = cp.Variable((n_class, L), nonneg=True)
    cons = []
    for n in nonroot:                                         # H1
        cons += [S[n] == Phi[n] @ S[parent[n]] + B[n] @ Y[parent[n]] + cvec[n] + Delta[n]]
    cons += [G[n] @ S[n] + K[n] @ Y[n] <= g[n] - g_rec[n] for n in nodes]          # H2
    cons += [R(n) >= R(parent[n]) for n in nonroot] + [R(n) >= gred_a[n] @ S[n] + gred_b[n] for n in nodes]   # H3
    for c_ in classes:                                        # H4
        cons += [eta[c_] + (1 / eps_p[c_]) * cp.sum(cp.multiply(p_cl[c_] * lr, z[c_])) <= b_red[c_],
                 z[c_] >= R_leaf - eta[c_]]
    cons += [Wn[n] == w_coef[n] @ S[n] for n in nodes]                            # H1-W
    cons += [Y[n, seg_parent] == cp.sum(Seg[n], axis=1) for n in pricing_nodes]   # SEG (convex excess priced in the cash rows)
    cons += [u <= a_k[k] * Wt_real + b_k[k] for k in range(48)]                    # UTILITY: 48 adaptive tangents
    cons += [psi >= s_j[j] * (1 - Wt / Wstar) + t_j[j] for j in range(n_breaks)]   # SHORTFALL
    cons += [Wt == term_coef @ S_leaf + A_leaf]                                    # TERMINAL: + IM + overlay MTM − D^RA − K
    cons += [hd0 + Slope @ X >= -g_h]                                              # H6a; other root rows similarly
    obj = cp.Maximize(p_leaf @ (u - lam_T * psi))                                  # no money term (S-ADR-33)
    return cp.Problem(obj, cons)
# acceptance: |z_cvxpy(CLARABEL) − z_highs(build_h)| ≤ 1e-7·max(1, |z|); row-by-row coefficient equality to 1e-12
# nightly exact-utility reference (A8): the same fixture with u_ℓ ≤ U₃(W̃^real_ℓ) as a CLARABEL power cone
```

### 5.7 Solver settings

**HiGHS (`highspy` 1.15.1)** — set through `Highs.setOptionValue`; `check_highs_options()` asserts every name exists and records all values in the manifest:

| Option | Value |
|---|---|
| `presolve` | `"on"` |
| `solver` | per `config/core/solver_policy.yaml` and the contract: `"ipm"` (with `run_crossover = "on"`) or `"simplex"` (with `simplex_strategy = 1`, dual) — chosen by the sprint-1 race per preset (JE-MF1) |
| `threads` | 1 (evaluator policy; speed from processes) |
| `parallel` | `"off"` |
| `random_seed` | 0 |
| `time_limit` | 110 s per replication (default preset); 600 s nightly; 21,600 s overnight |
| `primal_feasibility_tolerance` / `dual_feasibility_tolerance` | 1e-7 / 1e-7 |
| `ipm_optimality_tolerance` | 1e-8 |
| `mip_rel_gap` / `mip_feasibility_tolerance` | 1e-6 / 1e-7 (Level B only) |
| `output_flag`, `log_to_console` | False (the HiGHS log is captured to `runs/<run_id>/logs/highs.log`) |

Acceptance of a solve: model status optimal; for any solve whose duals are read, a valid basis (`basis_validity` = valid after crossover); otherwise `SolverError`.

**CLARABEL (0.11.1)**, called directly on the cone form (L ≤ Ax ≤ U split into two non-negative cones, equalities as the zero cone): `tol_gap_abs = tol_gap_rel = 1e-8`, `tol_feas = 1e-8`, `max_iter = 500`, `equilibrate_enable = True`, `presolve_enable = True`, `verbose = False`. Nightly agreement: |z_HiGHS − z_CLARABEL| ≤ 1e-6·|z| + 1e-8, and pricing duals within 1e-4 relative on rows whose HiGHS ranging interval is non-degenerate.

**OSQP** (module F): `eps_abs = eps_rel = 1e-8`, `polish = True`, `max_iter = 20,000`; CLARABEL fallback on non-convergence.

### 5.8 Dual extraction and sign conventions

Solver-independent definitions (z* = optimal maximized objective; rows written l_r ≤ a_r′x ≤ u_r):

| Quantity | Definition | Sign |
|---|---|---|
| π_r (inequality row) | lower bound binding: π_r = −∂z*/∂l_r; upper bound binding: π_r = ∂z*/∂u_r; slack: 0 | ≥ 0: the value of relaxing the row by one W₀ unit |
| μ_n (cash transition) | μ_n = ∂z*/∂e_n, e_n an exogenous cash injection added to the right side of node n's cash row | ≥ 0 normally |
| M_n | Σ_{r ∈ PRICING rows containing C_n} a_{r,C_n}·π_r, with a_{r,C_n} the coefficient in the row's requirement orientation (positive when cash helps satisfy it) | ≥ 0 |
| ℓ_n | M_n/(μ_n − M_n) per period of node n; fan nodes converted to per quarter by (1 + ℓ)^{1/2} − 1 | ≥ 0 when μ_n − M_n > 0 |

Implementation rules: (1) solve with `ObjSense.kMaximize`; (2) map HiGHS `row_dual` values to π and μ with the sign rule pinned by `solver/test_dual_sign_toy.py` — a 2-variable, 3-row LP with analytically known duals for ≥, ≤ and = rows under both senses; (3) one-sided derivatives come from the optimal basis (`Highs.getRanging`), with one parametric warm step only where ranging shows degeneracy; on the quarterly path, finite-difference warm re-solves run only on the capped, pre-declared set of ≤ 10 pricing rows that price cards, envelopes and FTP tenors, on the selected replication; full finite-difference verification of the Q1 cash rows and every T4P row runs nightly on the sign-off preset; re-solve counts go to `HSolution.resolve_counts` and the manifest (S-ADR-38; QUANT-22, BUILD-06); a mismatch outside the dual-quality interval raises `SolverError`.

Derived prices (ARCH §5.6; SYN L1): kernel π_n = p_n m_n ∏_{k ≺ n}(1 + ℓ_k)^{−1}, the product over n's strict ancestors (from μ_n = (1 + r)(1 + ℓ_n)Σμ_c a dollar at n is discounted by its ancestors' premia; including k = n would discount stressed nodes twice; `solver/test_kernel_two_node.py` pins it analytically; QUANT-26), with the Esscher deflator m_c = exp(−γ_m R^b_c)/E_{p(·|n)}[exp(−γ_m R^b)] on the α* funding-basket return and one γ_m per tree root-found so that E_{p(·|n)}[m(1 + R^b)] = 1 + r_f; λ^spot(s) = probability-weighted mean ℓ over Q1 nodes of regime class s; FTP(h) = (E_π̂[∏_{k≤h}(1 + ℓ_k)])^{1/h} − 1 per quarter (annualized only for display); one-off premium L = π₀/π̄ − 1; λ decomposition by binding row: component_f = ℓ_n·M_{n,f}/M_n (S-ADR-16). Dual quality: one-sided derivatives V′(b ± δ) from ranging (finite differences with δ = 1e-4 W₀ only on the capped set of rule (3)) — "at a kink" if |V′₊ − V′₋| > 1e-6 + 1e-3|V′|; validity interval from `Highs.getRanging()`; min/median/max band across the five replications; sign flips change the published sign only after two consecutive quarters or when |value| exceeds twice the band width (hysteresis). The KKT cap check runs on every solve: every lever below its cap has reduced cost ≤ 1e-7, i.e. Σ_h μ_h s_{ℓh} + y_IG ι_ℓ ≤ c_ℓ with c_ℓ the lever's cash-row cost valued at the cash duals (ARCH §5.6).

### 5.9 Phase I (lexicographic, explicit elastic LPs; ADR-06)

**Phase I-a** (`build_t0_block` + `phase1`) runs on the linearized t₀ block per consent scenario, in seconds:

- Columns: reversible levers x_ℓ ∈ [0, cap_ℓ(scenario)] — R0x: pacing cuts by group (no credit for 2 quarters), co-investment pause, SMA run-off and SMA sale (one shared $5.6bn sleeve), Capital Solutions syndication, contingent budgets off, opportunistic de-risking (IM release), P2S (no T4′ credit), RA cash-out refinancing; R0: + Treasury top-up from DM equities; R1: + committed revolver up to $15bn (credit 0.5 from month 2 in s*, the pricing convention set; 0.8 only in the research sensitivity; S-ADR-32); R2: + owner band (Mode H, owner SignOff). PE, Secondaries, Co-investment and RA asset sales are excluded, so recovery never presumes a fire sale (G-gap_01 §2).
- Rows: 24 monthly T4′ headroom rows; T1 over the s* ladder as an annual floor, payout ≥ max(5% of B_y, owner call) and ≤ 10% of B_y, with each instalment the remaining annual amount ÷ instalments left (`contracts.rules.instalment_bn`; a quarterly 5% floor would be 20% a year and pin duals, QUANT-25); T2 at 4%; T3; T8 per shock type; LR8; T5 and legal rows hard; elastic u_r ≥ 0 on tiered rows.
- Tiers: 𝒯₁ = {T1, T3}; 𝒯₂ = {T4′}; 𝒯₃ = {T2 hard, T8}. For k = 1, 2, 3: u*_k = min Σ_{r∈𝒯_k} u_r subject to the rows, the scenario's lever caps, and Σ_{r∈𝒯_j} u_r ≤ u*_j + δ for j < k, δ = 1e-6 W₀ (highspy `feasibilityRelaxation` is not used because it does not chain tiers; JE §5.2).
- If u*_k > 0: the IIS of the hard system (levers at caps, earlier tiers at their u*) from `Highs.getIis` where available, else a deletion filter over ≈ 30 row families; the Farkas ray from `Highs.getDualRay` stored as an artifact; levers at cap named with their owning group.
- Outputs: `Phase1Result.by_scenario[R0x…R2]`, d₀ = max(0, −min_h hd_h(0)), infeasibility prices (Phase-I duals; Treasurer panel only).

**Mode** (`recovery_mode`): pricing scenario = highest scenario whose levers are signed. u* > 0 on a hard tier under it → STRUCTURAL_RECOVERY (g_{r,t} = u*_r(1 − t/T_rec)+, T_rec = 4, 8 with Board approval). Else d₀ > 0 (or a hard row fails at x = 0) → EXECUTION_RECOVERY (g_t = d₀(1 − t/T_rec)+, delivery shares φ_{g,t}). The T6 screen (`t6_screen`: T6 and Tier-1B CVaR rows at HOLD with every reversible lever at capacity) breaching a class's **capacity** level triggers **Phase I-b** (tolerance breaches feed the Amber planning response and the CFA buffers, never recovery; S-ADR-31): the same lexicographic program on the full H with H4–H5 elastic (tier 𝒯₄) and the hard rows on their glide path; u*_CVaR > 0 → STRUCTURAL_RECOVERY with glide on the buffers. Otherwise NORMAL. Recovery status is always computed at G0 on the integrated engine, never assumed (ADR-11).

### 5.10 Phase II

The restored problem: hard rows with right-hand sides relaxed by the glide path, no elastic on hard rows, appetite rows elastic at a fixed contract penalty (excluded from pricing). `HSolution.priced_on = FEASIBLE` in NORMAL, `RESTORED` otherwise, with `recovery_hash = content_hash(GlidePath)`. The recovery cushion c_t = min_{h≤24}[CBC^TPF_{s*}(h) − NCO_{s*}(h) − 0.04W(h) + g_t]/W_t is ≥ 0 on the glide path, so cushion-monotone rules stay interior. Duals are read only from Phase II.

### 5.11 CE conversion, selection and certificates

ū′ = Σ_ℓ p_ℓ(∂u_ℓ/∂W̃_ℓ − λ^H_T ∂ψ_ℓ/∂W̃_ℓ) from the active PWL pieces; ΔCE_bp/yr = 1e4·Δobj/(ū′·3) (`stats.h_delta_ce_bp`). Column generation, Level B, Γ = [z_RMP + Σ_j u_j(r_j)⁺] − z_fixed ≥ z*_MILP − z_fixed ≥ 0 accepted at ≤ 5bp CE and forced re-solves flagged above 2bp, both judged on exact utility re-evaluated at the leaves' wealth (`HSolution.exact_objective`, A8) with the PWL bound beside them, and the H–P test (Kendall τ ≥ 0.8 on the top 30; replayed cash within 1%) are specified in §4.21. Each of the 5 SAA replications selects; their root actions are evaluated in P on an independent search set at the 2,000-path race count per world, escalating to 10,000 paths only when the top two are within 2 paired SE (B16), and the best Ψ is chosen (ties keep the replication with median duals); finite-difference dual checks and forced re-solves then run on the selected replication only; duals and envelopes publish as the median with min–max bands; root actions stable in fewer than 4 of 5 replications are "tree-sensitive".

### 5.12 Tree construction (`core.tree.build_tree`)

1. `core.sim.record_group_rates` on 2,000 search-plane paths per world for M1–M6 (12,000 pooled, CRN), HOLD + plan pacing, over the tree's 12 quarters only (B10); observable features per TreeSpec, each with a producer inside P (§4.19).
2. Stage 1: K₁ = 24 Q1 nodes by seeded, regime-stratified k-means (scikit-learn `KMeans(n_init=10, random_state=spec.seed)`) on standardized pooled Q1 features. Q2, Q3: pass-through nodes on the cluster's medoid path, decisions shared by the cluster.
3. Stage 2: within each Q1 node, K₄ = 4 Q4 children on Q4 features.
4. Fans: each Q4 node ends in L = 6 world-tagged leaf paths drawn from its members, stratified by world in proportion to w_m p_{n|m} and by a tail stratum on information available at Q4 (top `tail_quantile` of the facility-free funding gap), with likelihood-ratio weights so each world's CVaR row rests on ≥ 30 tail leaves; fan periods semiannual (Q6, Q8, Q10, Q12).
5. Node probabilities p_n = Σ_m w_m p_{n|m}; leaf world-conditional probabilities normalize within each world; coefficients are probability-weighted member means (linear quantities) or medoid values (nonlinear).
6. `forward_filtration` reducer (S-ADR-09) replaces steps 2–3 with Heitsch–Römisch forward selection under a stagewise transport distance; selected only by error-ledger row A4.

**Presets** (`config/core/h_presets.yaml`; ARCH §5.4 table):

| Preset | K₁ × K₄ × fan leaves | Leaves × periods | Fan periods | Use |
|---|---|---|---|---|
| `whatif` | 20 × 4 × 5 | 400 × 8 | semiannual Q6–Q12 | W2 what-ifs; MVP decisions |
| `default` | 24 × 4 × 6 | 576 × 8 | semiannual Q6–Q12 | quarterly decisions, λ, envelopes (5 replications) |
| `signoff` | 25 × 4 × 10 | 1,000 × 12 | quarterly Q5–Q12 | nightly stability (A4, A5) and published bands |
| `overnight` | 25 × 8 × 10 | 2,000 × 12 | quarterly; 20-quarter variant in 4-quarter steps beyond Q8 | brief's large corner; tree-sensitivity flag |

**Tests.** `test_no_world_identity_in_nodes` (permuting world labels within pooled clusters leaves Q1–Q4 nodes, coefficients and decisions unchanged); probability conservation; ≥ 30 tail leaves per world; deterministic tree hash for a fixed seed.

### 5.13 The no-pinned-duals CI test

| File | Content | Acceptance |
|---|---|---|
| `tests/regression/test_no_pinned_duals.py` | Port of gap_02's suite (8 tests): research coefficients exported once to `tests/regression/fixtures/gap02/coefs.json` by `tools/port_research.py`; the tests run **production** `core.phase1`, `core.phase2`, `core.duals`, `actions.make_card` on them | 8/8: the critic reading pins the T4 dual at the penalty tier and scales ×10 with it; the guard fires; every test fund reads SELL below a 2% reservation price on the pinned solve; restored prices are finite and ×10-invariant; restored reservation prices > 0.60; cushion on the glide path ≥ 0; Phase-I closed form u* = max(0, −(h₀ + max relief)) with "T4 row" in the IIS |
| `tests/regression/test_no_pinned_duals_groups.py` | Port of G-gap_01's suite (18 tests) on its group-resolved fixture | 18/18 incl. `test_kkt_cap_cheapest_spare_lever`, Phase-I group closed form per consent scenario with IIS naming PE and Private Credit levers, canonical s*(0.76) restorable with u* = 0 in R0x–R2, envelopes sum to NCO(24), glide shares sum to 1, interim glide path feasible without sales |
| `tests/solver/test_no_pinned_duals_h.py` | Extended test on production H (fixture tree in CI; default tree nightly) | (a) no PRICING dual within 1e-6·M of any elastic penalty value M in the model; (b) ×10 invariance: re-solves with diagnostic elastics on all hard rows at M and 10M give pricing duals equal to 1e-6 relative and identical card actions; (c) μ_n − M_n > 0 at every pricing node; (d) every card, envelope and FTP point carries `priced_on` ∈ {feasible, restored_problem}, and restored ⇒ recovery_hash equals the contract's; (e) no hard-row elastic column exists in a Phase-II `LPModel`; (f) `PricingRefused` for reverse-stress and unsigned-consent solves; (g) all fixture SELL reservation prices > 0.60; (h) T6/Tier-1B rows: Phase I-b and ×10 invariance (`test_t6_surrogate_guard`) |

A failure in any of the three files blocks merge (CI) and blocks pack publication (nightly gate G-pinned).

### 5.14 Scale test and timing acceptance

| Test | Workload | Acceptance |
|---|---|---|
| `tests/perf/test_b2_h_quarterly.py` | Default tree (576 × 8) from 6 × 2,000 pooled search paths on the v2 book, with **every mandated solve and re-solve**: Phase I-a for R0x–R2; assembly of 5 replications in 5 single-threaded worker processes (start-up included); Phase II on each; ranging, kernel and FTP; Level B with ≤ 4 warm selection re-solves per replication; finite-difference checks on ≤ 10 pricing rows and ≤ 20 forced re-solves on the selected replication | **≤ 120 s wall clock** on the reference laptop (Core Ultra 9 285HX, idle) against per-step budgets that `test_b2_profile` asserts: Phase I-a 5 s; assembly 15 s; Phase II 60 s; ranging, kernel and FTP 5 s; Level B and selection re-solves 13 s; finite-difference checks 5 s; forced re-solves 10 s (≈ 113 s; ≤ 2 s per warm re-solve [I]); re-solve counts in the manifest; nightly fails above 132 s; if a re-solve exceeds its budget, the finite-difference checks move to the nightly job and cards show ranging intervals (S-ADR-38; QUANT-22, BUILD-06) |
| `tests/perf/test_h_size.py` | Column, row and non-zero counts | within ±15% of §5.2–5.3 (detects accidental density) |
| Sprint-1 production benchmark (WP-18 DoD; JE-MF1) | IPM + crossover vs dual simplex, single-threaded, on the production row structure at the default and what-if presets | winner recorded per preset in `solver_policy.yaml` and the contract; fallback ladder if B2 fails: K₁ 24 → 16, then the what-if size (400 × 8) for decisions with the default tree overnight |
| `tests/perf/test_b6_whatif.py` | W2: 400 × 8 on cached paths; an FBE view is applied by a first-order adjustment of the node coefficients (Δret = Δα per quarter on the affected group buckets; distributions through the fund engine's linear sensitivities), never by re-recording group rates (A22; BUILD-32) | ≤ 60 s; a nightly exact re-record keeps the coefficients within 2% and the root actions unchanged, else FBE what-ifs route to W3 |
| Nightly sign-off | 1,000 × 12 quarterly + 10 replications | ≤ 15 min; feeds A4/A5 |
| Overnight | 2,000 × 12; 20-quarter horizon in 4-quarter steps beyond Q8 | completes ≤ 6 h; tree-sensitivity flag (documented deviation, ADR-05) |
| `tests/reconciliation/test_h_identity_unreduced.py` | Unreduced fixture trees (one path per node), quarterly **and** semiannual, with fixed actions including fixed SELL actions (buyer-assumed unfunded) and fixed REFINANCE draws | H rows reproduce the simulator's cash path to **1e-9** (ADR-02; QUANT-04, QUANT-15) |
| `tests/reconciliation/test_h_replay.py` | Reduced tree: H's first-stage actions replayed through P on the tree's paths | projected cash within 1% |
| `tests/metamorphic/test_h3_conversion_invariance.py` | Convert $1 of long-only into cash at zero impact; draw $1 of the revolver | every H3 row unchanged (QUANT-06) |
| `tests/metamorphic/test_h_cost_neutrality.py` | A zero-NPV RA refinancing; a cost-neutral financing round trip | the objective changes only by the PWL error (QUANT-05, QUANT-07) |
| `tests/solver/test_kernel_two_node.py` | A 2-node tree with analytic duals | π discounts over strict ancestors exactly (QUANT-26) |
| `tests/solver/test_a8_decision.py` | Exact CRRA at the solution and at the top-k alternative actions; nightly CLARABEL power-cone reference on the fixture tree | ranking unchanged and \|ΔJ_exact − ΔJ_PWL\| ≤ 0.5bp CE between them; the absolute PWL bound is reported, not gated (A8; QUANT-18, BUILD-19) |
| Error-ledger rows in H | A4 MMW gap ≤ 10bp CE over ≥ 5 trees and root stable in 4 of 5; A5 same root actions and Δλ^spot ≤ 10% vs the quarterly 12-period solve; A8 by the decision test above; A9 root evaluated out of sample in P plus the policy-fan variant; A17 pooled vs world-separated optimism gap reported; horizon invariance T_H = 8/12/16; `test_binding_world_priced` (every banded class has an H4 row; the binding class carries a non-zero dual on the fixture where it binds) | as stated (ARCH §5.13) |

---

## 6. Synthetic data specification: SYN-ADIC-177

> **SYNTHETIC – NOT ADIC DATA.** Everything in this section is a documented ground-truth process for testing estimators and engines. Parameters marked [I] are design defaults; sourced values cite GROUPS or SYN.

### 6.1 Layers, releases and storage

| Layer | Content | Readable by |
|---|---|---|
| World | Regime chains (S, e, Z), factor paths, exit factor X_t, valuation gap z_t, oil and fiscal paths (generated by `scen` + `owner` on the history window 2008 → as-of and forward) | everyone (it is synthetic market history) |
| Sealed truth | Skill draws (vintage, GP, idiosyncratic), economic NAV, true μ, bias draws, κ_g, overlap graph truth, outcomes | `SealedTruthStore` via MRM validation tokens only (TB8) |
| Observation | Holdings, reported NAV, cash flows, four marks, forecasts, quotes, HF terms τ, loan tapes, overlay trades, CRIF, CSAs, facilities, owner draw history | engines, estimators, agents (aggregates) |

Releases (ARCH §9.4): **R0** — the 2026-10-18 snapshot with history from 2008; **R1** — 1,000 worlds × 40 quarters on CRN across SELL / HOLD / REFINANCE / LEVER (column flows on identical draws); **R2** — 200 history worlds (2000–2040) for time-travel scoring; **R3** — reserved for the semi-synthetic release (S-ADR-19). Storage: bitemporal Parquet in `stores/data/SYNTHETIC/` (USD bn, S-ADR-04), truth in `stores/truth/`, release manifest (config hash, seeds, census, allocation, gate report) in the registry.

### 6.2 Allocations, positions and unfunded commitments

All books total **$177bn of reported NAV** (CTX §1A). Allocation v2 is the default (S-ADR-03).

| Group | Positions | NAV v1 ($bn) | NAV v2 ($bn) | Unfunded ($bn): census v1.0 / v1.1 / v1.1r (v2) | Size law; mix |
|---|---|---|---|---|---|
| PE | 120 interests on ≈70 GPs | 52 | **34** | 27.4 / 16.4 / 10.7 | lognormal σ 1.0; large buyout 40%, mid buyout 25, growth 12, VC 8, sector 10, special situations 5; US 60, Europe 28, Asia 12; GP tiers elite 10% of GPs (20% of NAV), core 50% (60%), other 40% (20%) (GROUPS §3.1) |
| Secondaries | 40 | 14 | 14 | 3.9 (incl. 0.4 deferred payables) | σ 0.8; S1 5.6 (10 funds, vintages 2017–25), S3 4.6, S4 2.0, S5 1.4, S6 0.4 (GROUPS §3.2) |
| Co-investment | 90 | 18 | 18 | 1.5 | σ 0.8; effective N ≈ 45; largest $1.2bn; deals from BJS quartiles (≈10% zero returns); starts in D (GROUPS §3.4) |
| Capital Solutions | 40 | 8 | 8 | 1.2 | median $150m ($50–600m); families A 30%, B 10, C 20, D 15, E 10, F 15; vintages 2019–26; 3 positions in PIK or amendment, 1 in workout (GROUPS §3.3) |
| Private Credit | 35 vehicles; ≈1,500 loans in ≈20 cohorts | 14 | 14 | 4.0 (1.0 DDTL/revolver + 3.0 fund unfunded) | DL 60% (S+550), ABF 15, mezzanine 10 (⅓ PIK), opportunistic 15; wrappers SMA 40, CEF 45, evergreen 10, BDC 5; 75% sponsored; starts in T (GROUPS §3.6) |
| Real Assets (v2 only) | 50: 22 closed-end funds, 6 open-end funds, 22 co-investments/directs/JVs | — | **18** | — / ≈4.0 / ≈4.0 (closed-end 3.0, development 1.0) | real estate 45%, infrastructure 35%, energy & natural resources 20% [I]; σ 0.8; asset debt on directs/JVs at LTV 45–55% [I] (brief §8 rule 6) |
| Public Markets: hedge funds | 40 lots | 20 | 20 | — | σ 0.6; multi-strategy 30%, equity L/S 15, event 10, credit 15, RV 10, macro 10, trend 10, with the GROUPS §3.5 terms table |
| Public Markets: long-only | 24 mandates | 36 | 36 | — | DM equity 22, EM equity 6, fixed income 8 |
| Treasury (CF) | 6 sleeves | 15 | 15 | — | cash 6, UST 4, IG 5 |
| **Total** | **395 (v1) / 445 (v2)** + loans + trades | **177** | **177** | v1: 38.0 / 27.0 / 27.0; v2: — / 31.0 / 25.3 | |

Census v1.1r rescales the sealed v1.1 vintage history by 34/52, giving $10.7bn under v2 (the brief quotes "about $10.9bn" from the rounded U/NAV of 0.32; the build uses the exact rescaling and prints both). Census v1.0 is not defined on allocation v2.

### 6.3 PE vintage history and the census rule

`synth.history.fit_pe_history` ports `research/groups/addenda/gap_02_calcs/seal_history.py`: census quantities are linear in vintage commitments, so the history is a linear program on `FundEngine.mean_path` rates — maximize unfunded subject to PE NAV = target, both MSCI H1-2026 rates inside V6's ±2pp band (distribution 9.0%, contribution ≥ 29.0%) and a growth corridor on commitments; choose the plan-consistent member with exactly 9.0% distributions and the largest unfunded (G-gap_02 §1). Sealed v1.1 (allocation v1): commitments +1.44% a year 2010–20 ($3.80bn → $4.39bn), 1.5× in 2021–22 ($6.67bn, $6.77bn), −5.75% a year 2023–26 ($6.38bn → $5.34bn); NAV $52.0bn by vintage 2010–15 7.3 / 2016–20 22.5 / 2021–22 12.8 / 2023–26 9.5; unfunded $16.4bn (pre-2021 0.6; 2021–22 2.5; 2023–24 5.6; 2025–26 7.7); SHA-256 of the research file `sealed_pe_history_v1_1.csv` = `4346dc249e83bff8d952588715a69ec038b9725ab436e0b24b8bb4227f2f54a9` (the regression test verifies the copied fixture's hash and reproduces its commitments by vintage and strategy and its unfunded by vintage within $0.01bn). Truth variants: mature $13.9bn, 10%-then-flat $18.4bn, 20% growth $31.9bn (fails V6 by construction; stress truth), v1.0 reproduction $27.4bn.

**Decision census (S-ADR-03).** Under v2 the builder first attempts `v1.1` (PE unfunded $16.4bn on PE NAV $34bn): it fits a plan-consistent history to those targets; if no V6-compliant history exists (`CensusInfeasible`) or V1–V2 fail at build, the decision census is `v1.1r` (V6 is the decisive gate, G-gap_02 §1; a gate that is n/a never triggers the substitution; S-ADR-37), and the release manifest and L0 state "census v1.1 requested; v1.1r used because <gate>". Both censuses are generated, and every liquidity metric is reported for both.

### 6.4 Ground-truth processes (sealed)

| Component | Truth process |
|---|---|
| PE skill | a_v = −0.05 z_v + u_v a year (vintage SD ≈ 1%), GP effect 3%, idiosyncratic 2.5% (σ_α ≈ 4%); α net of ≈1% a year write-down jumps; calibrated within each world (pooling worlds gave a vintage ICC of 0.78 vs 0.12 empirically) (GROUPS §6) |
| PE NAV shocks | truncated t₅ (E[e^{t₅}] is infinite) or NIG; economic NAV via FundEngine with true μ |
| Co-investment deals | gross PME quartiles P25 0.26, median 1.16, P75 2.45 (BJS 2020); P(MOIC < 1) 0.35–0.40; GP effect shared with PE funds of the same GP (ρ_GP 0.6 along graph edges) |
| Capital Solutions | competing-risk truth per family; default and PIK rates by regime as §4.11 |
| Private Credit | severity-anchored pair LGD 0.67, PD_N 1.1% (×1.5 D, ×3 C) as default truth; incidence-anchored GC1 pair (PD 1.1/1.5/2.4/6.0%, LGD 0.45/0.50/0.55/0.65) as variant; estimators must pass SBC on both (GROUPS §3.6 R1) |
| Hedge funds | τ drawn so that book-level notice capacity matches Form PF on its own definition: 8.4 / 27.3 / 23.0 / 41.4% at ≤ 7d / 8–90d / 91–365d / > 365d; crisis gate hazards per strategy; optional HF-TRS scenario (TRS_TERM branch) |
| Real assets [I] | NOI growth g₀ = 1.5% real a year plus partial inflation pass-through (RE 0.5, infra 0.7, ENR 0.3); cap rates RE 5.5%, infra 6.0%, ENR 8.0% loading on `ra_caprate`; ENR oil beta 0.6 on Brent (wrong-way with the owner draw, brief §8 rule 5); value-add α ~ N(1%, 2%) a year; development S-curves over 8–12 quarters |
| Overlay | positions only (no skill truth beyond the opportunistic residual α ~ N(0.3 SR, 0.25²) prior) |
| Overlap graph | sampled with s_PC = 0.75, p_co/h_co = 0.70/0.90, h ≈ 0.6, p_csA = p_csC = 0.50; rejects draws breaching GP ≤ 5% unless labelled a concentration stress (G-gap_02 §6) |

### 6.5 Observation layer: the four marks and their biases

- **O1 reported NAV:** smoothing 0.5 (buyout), 0.6 (VC), 0.5–0.7 (private credit), 0.5 (Capital Solutions, co-investment), Geltner λ_G 0.6 (real assets [I]); 1-quarter lag; noise N(0, 0.04²); BGK-type peer reversion ≈ 2.6pp per SD plus ≈ +5pp at 2 SD below peers after five years without a new fund; exit uplift N(0.10, 0.15²).
- **O2 underwritten:** the sealed forward-basis value u = μ̄ + 0.3(α − α_s) + b^u + γ′x (+2pp each for leverage > 6× and multiple-expansion share > 50%), expiring after T_u + 1, is **emitted as ADIC files it**: an underwriting net IRR or MOIC with down/base/up cases, its image under the unit's planned cash-flow profile (brief §9; S-ADR-27). Real assets: yield-on-cost, IRR and exit cap rate.
- **O3 actual:** `beliefs.perf` on observation data only (so actuals inherit O1 biases); since-inception net IRR and MOIC per holding, shown as sunk.
- **O4 forecast:** the sealed forward-basis process f_t = 0.6 f_{t−1} + 0.4[w_u u + w_a a + (1 − w_u − w_a) f* + b^f] + η, with timing optimism for 5 quarters after a high-yield spread shock above +150bp, stated intervals q₁₀, q₉₀ = f ∓ 1.2816·σ_true/κ_g and strategic bias b^f_{i,t} = b^f_g + b_g Z_{g,t−1} B′_{g,t}/(2 s_g) + u_def 1{SELL_{i,t−1}} with u_def = +2pp (G-gap_02 §3), is **emitted in ADIC's shape** (S-ADR-27; QUANT-11, BUILD-09): a since-inception net IRR or MOIC (by group convention) with down/base/up cases at the stated q₁₀/q₅₀/q₉₀, obtained by pushing each forward-basis quantile through the unit's cash-flow history and the fund engine's mean-path profile to the stated exit horizon (`exit_horizon_q`), quarterly from 2008 to the as-of with bitemporal `recorded_at`. Estimators therefore see only IRR/MOIC with cases, and parameter recovery runs through `beliefs.irr_translation`. The strategic covariates (prior-quarter SELL flags, envelope status) exist only after the synthetic go-live date; before it they are 0 with `history_indicator = 1`, as on ADIC's pre-lab archive.
- **Market-implied (m):** external secondary bids from the hedonic model with desk noise; in-house desk quotes flagged `conflict_flag = True`; Capital Solutions reserve quotes as financing anchors; real assets use listed REIT/infrastructure NAV discounts and secondary pricing.

| Group | b^u / b^f (pp a year) | κ_g (coverage of a stated 80% interval) | Specific planted biases |
|---|---|---|---|
| PE | +5.0 / +3.0 (+4.0 after age 8) | 2.00 (48%) | timing slip +2–4 quarters (normal), +4–8 (drought); fundraising-window marks |
| Secondaries | +2.0 / +1.5 | 1.67 (56%) | accretion booked as return; targets used as expectations; winner's curse |
| Capital Solutions | +2.0 / +1.5 | 2.00 (48%) | PD understated ×0.7; PIK at face; kicker optimism; WAL too short |
| Co-investment | +6.0 / +3.5 | 2.22 (44%) | exit multiple = entry in 16% of models; EBITDA growth above reference P75 |
| Private Credit | +0.75 / +0.75 | 1.67 (56%) | syndicated (not direct) recoveries; default definition |
| Hedge funds | +3.0 / +2.0 | 1.67 (56%) | selection on past returns; smoothing; contractual liquidity assumed |
| Long-only | +1.0 / +0.75 | 1.43 (63%) | — |
| Overlay | carry −30%, crisis payoff +20%; Sharpe +0.6 / +0.4 | — | trials under-reported unless counted |
| Real assets [I] | +2.5 / +2.0 | 2.00 (48%) | cap-rate compression and NOI-growth optimism in business plans |

(GROUPS §5 table; κ_g = 1/κ_conf, G-gap_02 §5.) SBC mode draws κ_g from LN(ln 1.75, 0.25²); recovery mode pins the table values.

### 6.6 Facilities, debt and collateral (synthetic)

| ID | Kind | Status (consent) | Size | Pricing | Stress credit |
|---|---|---|---|---|---|
| SYN-FAC-01 | committed unsecured revolver | requested, unsigned (R1) | $15bn | SOFR + 85bp drawn, 15bp undrawn, 15bp upfront per 3 years; ≥ 10 banks, none > 12.5%; yearly test draw | 0 in 30-day rows; from month 2 with covenant headroom: 0.5 in s* and in the joint oil–crisis state (pricing set), 0.8 in the research sensitivity (S-ADR-12, S-ADR-32) |
| SYN-FAC-02 | LP-portfolio NAV facility | available (R0x) | capacity-capped: pledge pool ≤ 20% of private NAV → ≈ $2.1bn at 10% LTV | SOFR + 300bp (250–400) + 1–2% OID; +140bp in stress | 5% stressed LTV (≈ $1.1bn credited); forced paydowns in stress |
| SYN-FAC-03 | repo against UST | uncommitted (R0x) | $5bn | SOFR + 20bp [I] | 0 in stress rows (repo is a route, not a source) |
| SYN-FAC-04 | term pre-funding | indicative (R1) | up to $5bn, 3 years | SOFR + 120bp [I] | counts as cash once drawn (S-ADR-12) |

Recourse debt at t₀ is zero; economic exposure ≈ 0.97× with the $10bn completion beta. Twelve CSA archetypes (§6.7) carry thresholds, MTAs, eligible collateral, reuse rights and IM regimes.

### 6.7 Overlay book

- **Policy book (decision runs; G-gap_03 §5):** 90/72 put-spread floor ladder on SPX at the 0.15% budget, $7.1bn notional (3M $1.6bn, 6M $3.4bn, 12M $2.1bn; listed); $10bn completion beta (index futures, client TPA); opportunistic Level-1 exposures (trend, carry, RV, short vol) at vol ≈ 1.0–1.2% of NAV and IM $1.0bn within a $1.5bn budget.
- **Engine-test fixture (`overlay_fixture=True`; tests only):** ≈ 250 trades on 12 CSAs: tail stack ≈ 70 trades, ≈ $25bn (SPX/SX5E put spreads, VIX calls, CDX HY payers, CDX IG protection, Brent put spreads, 3–5 hybrid shells); opportunistic ≈ 150 trades, ≈ $45bn notional (trend futures, FX carry, IRS and swaption RV, CDX carry, short strangles and variance swaps); synthetic beta ≈ 30 trades. CSA archetypes cover both IM regimes (two-way SIMM; IA-only for sovereign-exempt status), zero and non-zero thresholds, MTAs $0.5–5m, cash-only vs UST-eligible collateral, reuse vs pledge, rating triggers and two GCC dealers (wrong-way in GW); at least four dealers face both books. Its tail premium (≈ 0.53% of NAV, above the cap) is rescaled to the budget in decision runs.
- **Market state (16 Oct 2026, Cboe):** SPX 7,659.44; VIX 19.99; VIX3M 20.50; VIX6M 21.67; VIX1Y 22.61; SKEW 168.59 (GROUPS §8).

### 6.8 Owner distribution process

`owner` with `config/owner.yaml` (§4.8): fiscal map with hydrocarbon share 11.3% → 9.1%, breakeven lognormal median $55 (90% $45–70), Gulf-war wedge N(−5, 2²)pp; reduced-form draw c = 7.5%, b = 0.625, ρ_d = 0.5; overrides 0.25% (N, B, SS), 1% (SG, DB), 2% (GW) a year; instalments at quarter ends on the opening-of-fiscal-year reported NAV. Synthetic client data: FY2026 rate d₂₀₂₆ = 5.8%; draw history 2008–2025 generated by the same process on the history window. B₂₀₂₆ is the R0 history's reported NAV at 2025-12-31, calibrated so that the 12-month draw (Q4-2026 instalment plus three 2027 instalments) lands in $9.9–10.8bn (gap_04 §6.2).

### 6.9 Validation gates (block the pack on the decision census, by increment; S-ADR-37)

**Blocking policy** (BUILD-17). Increment 1 blocks the pack on V1–V2, V5–V9, V12, V20 and V22–V24; v1 blocks on every applicable gate. A gate that cannot run (V15 before ADIC data; V18 before release R2) is n/a and never blocks. V16–V18 are release-validation jobs (B14) whose hashed reports the pipeline reads; they never run inside the quarterly cycle (B12).

| Gate | Check | Tolerance |
|---|---|---|
| V1 | Accounting identities (NAV roll-forward, cash, unfunded) | 1e-10 |
| V2 | Group totals equal the allocation; intra-ADIC flows net to zero on cash **and** DVA ledgers | 1e-9 $bn |
| V3 | PE dispersion vs BGK (USD sample) | SD within ±20% |
| V4 | Vintage component share of PE return variance | 0.10–0.18 |
| V5 | DPI by fund age vs reference bands | ±0.10× |
| V6 | Distribution and contribution rates vs MSCI H1-2026 (9.0% / 29–31%) | ±2pp |
| V7 | Share of exits above the prior mark | 0.70–0.80 |
| V8 | Buyout reported-NAV AR(1) | 0.66–0.71 |
| V9 | Secondary prices vs Jefferies (all 87%, buyout 91%) | ±3pp |
| V10 | HF smoothing at fund level | θ₀ ≥ 0.5 |
| V11 | HF liquidity vs Form PF on its own definition | ±5pp per bucket |
| V12 | Private Credit regime-weighted loss | 0.8–1.2% a year |
| V13 | VIX and MOVE quantiles | ±10% |
| V14 | Bias realism: planted biases inside the prior bands | 100% of groups |
| V15 | Two-sample classifier AUC (real vs synthetic; activates with ADIC data) | ≤ 0.60 |
| V16 | Simulation-based calibration (FBE-R, regime filter, owner model, census pace) | rank χ² p > 0.01 |
| V17 | Parameter recovery incl. PE pace and unfunded by vintage under every truth variant | 80% intervals cover truth; point error ≤ 5pp |
| V18 | Time-travel CRPS skill (R2) | > 0 |
| V19 | Regret vs oracle per group | reported |
| V20 | Labelling | 100% |
| V21 | Census and NAV-weighted leverage vs OFR | ±20% |
| V22 | Basel caps in every coverage ratio | all |
| V23 | No LP-inaccessible SELL or REFINANCE instrument | 0 |
| V24 | Overlap: (a) one EV draw per company per path, same-quarter defaults and recaps with waterfall-consistent payoffs, intra-ADIC recap flows net to zero; (b) overlap shares in binomial 90% bands (Co-investment ∩ PE 0.59–0.76; PC ∩ PE 0.115–0.143; CS C/D/E ∩ PE 0.15–0.51; CS A → ADIC funds 0.26–0.74; co-investments with an ADIC PC loan 0.03–0.13); (c) GP ≤ 5% on the graph; (d) ρ_GP only along shared-GP edges | as stated |
| VR1–VR3 (interim, S-ADR-02) | RA reported-NAV AC1; core income yield; open-end queue in stress | 0.5–0.7; 3.5–6% a year; requests ≥ 2× the cap in CRIS |

**Stylized facts** (SYN §7.1, checked on R1 under M1): drought distribution yields 12–15% of NAV persisting ≥ 4 years in the drought share of paths; ≈ 7-year average holds; crisis secondary bids ≥ 61% of NAV (H2-2008 upper bound); a central path consistent with ≈ 7.7% ten-year endowment outcomes (±1pp), which is also the integration gate for the belief-to-engine wiring (a doubled beta would push it several points higher; QUANT-02).

**Misspecification gates for estimators** (frozen and hashed in `config/beliefs/misspec_gates.yaml`, owned by WP-14, before the first scored release; no tuning on release data; generated by `beliefs.validation.fbe_variant`; G-gap_02 §3): variants M0, M1 (regime-dependent optimism), M2 (nonlinear anchoring), M3 (t₃ tails), M4 (correlated u–f errors, ρ = 0.6), M5/M5s (strategic bias under designed/status-quo pay), M6 (prior shift), MALL. Metrics against a variant-aware oracle. **G-A** (M0): SBC passes, 80% coverage 0.75–0.85, excess CRPS ≤ 15%. **G-B** (each of M1–M6): excess CRPS ≤ 15%, coverage 0.72–0.88, SELL bias ≤ 1.5pp, excess regret ≤ 35%. **G-C** (MALL): ≤ 25%, ≥ 0.70, ≤ 2.0pp, ≤ 50%. **G-D**: detection power ≥ 0.70 with false positives ≤ 0.05. **G-E**: a group failing G-B under M5s gets non-trivial forecast precision only after the pay remedy (b ≤ 0.005, s ≥ 50, nothing scaling with budget); otherwise κ_g is capped at 2.74.

**Parameter-recovery suite** (`tests/recovery/`): FBE-R biases and κ_g per group (±5pp; κ within its 80% posterior interval), estimated from the emitted IRR/MOIC archive through the translation (QUANT-11); regime transition probabilities from simulated observables (±5pp); owner (c, b, ρ_d); census pace and unfunded by vintage under every truth variant (V17); F_t calibration (a, b) reliability within bins.

### 6.10 Labelling

`SYN-` identifiers; `is_synthetic = true` and `data_class = SYNTHETIC` on every row; Parquet schema metadata `{"data_class": "SYNTHETIC", "generator": "SYN-ADIC-177", "release": ..., "census": ..., "allocation": ...}`; the footer on every output; taint propagation; the truth store sealed from agents and estimators; synthetic sets frozen and kept separate once ADIC data arrive.

---

## 7. Agent layer specification

LLMs propose, extract, argue and narrate; they never produce a number, never touch engine code and never vote (P1; ARCH §7). Every number reaches text through a rendered placeholder.

### 7.1 LLM provider interface (`agents/backends`)

| Backend | Behaviour |
|---|---|
| `AnthropicBackend` | Live; needs only credentials resolved by the SDK. Providers: first-party `anthropic.Anthropic`, `AnthropicBedrockMantle(aws_region=…)` (model `anthropic.claude-opus-5-5`), `AnthropicVertex(project_id=…, region=…)`, `AnthropicFoundry(api_key=…, resource=…)` — channels, not model families (ADR-30) |
| `ReplayBackend` | Serves recorded responses from `tests/cassettes/<role>/<structural key>.json` with two-tier keys (S-ADR-41; BUILD-33): the **structural key** (role, campaign state, frozen-prompt hash, tool-schema hash, turn index) selects the cassette, and a miss raises `ReplayMiss` (fails closed); the **request digest** (SHA-256 of canonical JSON {model, system, tools, messages as sent with thinking blocks, max_tokens, effort, thinking, output-model schema hash, betas, fallbacks}) is then compared, and a mismatch raises `ReplayDrift`. Integrity drills gate on exact digests; other agent tests may fall back to Stub on drift and report it; re-recording is scheduled after engine or prompt changes, so engine changes do not turn the agent suite red |
| `StubBackend` | Seeded, schema-valid, rule-based outputs per role (e.g., IdeaBundles sampled from the DSL grammar inside declared boxes; memos assembled from placeholder templates; seat arguments listing the engine's cruxes) |

Selection: environment variable `TPA_LLM_MODE ∈ {offline, replay, live}` → Stub / Replay / Anthropic for every role (`make_backend`). `tpa replay record` runs a campaign live and writes cassettes. Opus 5.5 accepts no sampling parameters, so Replay is the only route to deterministic agent tests (ARCH §7.13).

### 7.2 Anthropic call shape (anthropic 1.15; S-ADR-23)

```python
client = anthropic.Anthropic(max_retries=2, timeout=600.0)
resp = client.beta.messages.parse(
    model=role.model,                        # family A "claude-opus-5-5"; family B (Phase 0) "claude-sonnet-5-5", labelled correlated
    max_tokens=role.max_tokens,              # 16000 default; messages.stream(...).get_final_message() for long outputs
    thinking={"type": "adaptive"},           # cannot be disabled on Opus 5.5
    output_config={"effort": role.effort},   # always explicit (Opus 5.5 defaults to "medium")
    system=[{"type": "text", "text": frozen_prompt, "cache_control": {"type": "ephemeral"}}],
    messages=transcript,                     # append-only; thinking blocks passed back unchanged
    tools=tool_defs,                         # each with "strict": True, additionalProperties: false, required
    tool_choice={"type": "auto"},            # forced tool choice returns 400 on Opus 5.5; the prompt names the submit tool
    output_format=role.output_model,         # an LLM draft model (§3.16; S-ADR-36), checked by check_llm_schema; read resp.parsed_output
    betas=["server-side-fallback-2026-07-01"], fallbacks="default",
)
```

Rules: no temperature/top_p/top_k and no assistant prefill (both 400); check `stop_reason == "refusal"` (and `stop_details.category`) before reading content; a refusal of the whole chain raises `LLMRefusal` and the role escalates; `max_tokens` → one retry with streaming at twice the cap; parallel tool results go back in one user message; failed tools return `is_error: true`; errors are caught most-specific-first (NotFound → RateLimit → APIStatus → APIConnection). Batches (50% price) serve non-urgent S1 seat assessments and omit `fallbacks` (rejected there); refused batch items re-run synchronously. On Bedrock, Vertex and Foundry the SDK's `BetaRefusalFallbackMiddleware` replaces the server parameter. WP-25 verifies in one recorded live call that `parse` forwards `betas`/`fallbacks`; if it does not, the backend calls `client.beta.messages.create(..., output_config={"effort": ..., "format": {...}})` and validates with the Pydantic model. Every call writes an `LLMCallRecord` (requested vs served model from `resp.model` and `usage.iterations`, tokens incl. `cache_read_input_tokens`, cost from the `config/llm/roles.yaml` price table: Opus 5.5 $4 / $20 per MTok, cache reads $0.20; Sonnet 5.5 $2 / $10). A fallback that puts author and reviewer in one family triggers re-routing of the review (ADR-30).

### 7.3 Gateway, egress and redaction

Only the `tpa lab` process has network egress; agents hold no file, shell, code or network tool; tools are typed and served by the lab firewall or the evaluator. `Gateway.redact` tokenizes owner fiscal items, counterparties and GP names with stable per-campaign tokens; holding-level content enters a prompt only if `llm_policy.holding_level_content_allowed` (operator flag) and the role's `data_classes_allowed` include the run's data class; REAL data additionally requires the in-region-serving confirmation recorded in the contract (P13; ARCH §9.7). Untrusted documents reach only quarantined extractors (no outbound tools, dual extraction, human sampling) and are treated as data, never instructions (TB6).

### 7.4 Typed tools

Each tool is a pair of strict Pydantic models in `contracts.tools` (JSON Schema with `additionalProperties: false`, all fields required or defaulted). **Evaluator tools** run in the evaluator process (MCP 2.3 stdio); **lab tools** run in the lab firewall and read or write only the registry and campaign memory. Counted calls charge the evaluator's budget, failures included.

| Tool | Input → output (models) | Server / planes | Counted | Roles (state-dependent allowlist) |
|---|---|---|---|---|
| `state_snapshot` | `StateSnapshotIn{}` → `StateCard` (stages, F_t, e₀, Z₀, draw fan, T4′ survival, λ summary; aggregates only) | evaluator; search, exploration | no | drafter, ideators, writer, Q&A, seats |
| `phase1_restore` | `Phase1In{scenario}` → `Phase1Card` (u*, d₀, IIS names, glide path, levers at cap; infeasibility prices only in the Treasurer view) | evaluator; search | no | drafter |
| `compile_spec` | `PolicySpec` → `TypeReport` (TR1–TR8; ≤ 3 retries per attempt); a spec that compiles is stored by `spec_hash` in the plane store, from which `evaluate_policy` reads it (an unknown hash raises `CacheMiss`; BUILD-11) | evaluator; search | no | executors |
| `evaluate_policy` | `EvalRequest` → `EvalResultAgentView` | evaluator; search | **yes** | executors |
| `price_actions` | `ActionPackage` → `PackagePrice{robust_rc_bucket, dominated}` | evaluator; search | **yes** | ideators, executors |
| `optimize_h` | `OptimizeHIn{preset="whatif", views: list[ViewSpec] (confirmed), overrides: list[TypedOverride]}` → `HSummary` (EXPLORATORY) | evaluator; exploration | yes (exploration budget) | translator, room |
| `evaluate_scenario` | `ScenarioSpecDraft` (KL-bounded; targets as a `KeyValue` list; the firewall assembles the `ScenarioSpec`) → `ScenarioResult{dp_red_bucket, binding_rows, kl}` | evaluator; exploration | **yes** | red team |
| `reverse_stress` | `ReverseStressIn{metric, threshold}` → `ReverseStressResult` | evaluator; exploration | **yes** | red team |
| `implied_actions` | `ImpliedIn{seat_id, item_id}` → `ImpliedActionCard{action, regret_bp_by_option}` (engine numbers: exact re-weighting of cached CRN paths over the item's options; BUILD-07) | evaluator; exploration | no (room budget) | seat narrators (read only) |
| `ep_condition` | `EPIn{views}` → `EPResult` | evaluator; exploration | no | translator |
| `evsi_crossfit` | `EVSIIn{item_id}` → `EVSIResult` | evaluator; exploration | yes | room (deterministic) |
| `flip_thresholds` | `FlipIn{card_id}` → `FlipThresholds` | evaluator; search | no | writer, Q&A |
| `robustness_card`, `bridge_card`, `group_envelopes`, `overlay_offset_card` | `{ids}` → `RobustnessCard` / `BridgeCard` / `EnvelopeSummary` / `OffsetCard` | evaluator; search | no | writer, seats |
| `attribute` | `AttributeIn{run_id, kind ∈ {shapley6, group, null, what_moved}}` → `AttributionCard` | evaluator; search | yes | writer, auditor |
| `price_trade`, `crif_sensitivities`, `simm_like`, `greek_offsets`, `hybrid_quote_check` | overlay structures → `TradePrice` / CRIF aggregates / `SimmResult` / `OVReport` / `HybridCheck` | evaluator; exploration | no | ideators (overlay structures) |
| `get_metric`, `list_metrics`, `get_provenance` | registry reads → `MetricInstance` / ids / `ProvenanceNode` | evaluator; all but final | no | writer, Q&A, auditor |
| `validate_claims` | `{doc_id}` → `ValidationReport` | evaluator | no | writer |
| (forecast intake) | `ForecastRecord` + operator token → ack, through the human command `tpa forecast register` only; no LLM-facing surface exposes it (S-ADR-34) | CLI | no | — |
| `log_assumption`, `escalate` | `AssumptionEntry` / `Escalation` → ack (ledger writes) | evaluator | no | all roles |
| `read_template`, `read_contract`, `lint_report` | contract template / signed contract / deterministic linter report | lab | no | drafter, reviewer |
| `get_price_table`, `get_cards`, `get_archive_summary` | λ table, cards (aggregated), MAP-Elites summary | lab | no | ideators |
| `get_memory`, `write_memory_event`, `write_rubric_status` | campaign memory (closed at SELECTION) | lab | no | ideators, executors |
| `submit_idea_bundle`, `submit_eval_request`, `get_eval_result` | `IdeaBundle`; relays to `evaluate_policy`; ledger agent view | lab | via evaluator | ideators, executors |
| `get_spec_diff`, `propose_variants`, `filter_variants` | single-change ablation variants (`VariantSet`; "zero accepted" valid) | lab | no | ablation proposer / filter |
| `submit_scenario_spec`, `get_exploration_result` | relays to `evaluate_scenario` | lab | via evaluator | red team |
| `draft_memo`, `draft_viewspec`, `draft_scenariospec`, `answer_grounded` | `MemoDraft` (placeholder text); `ViewSpecDraft` / `ScenarioSpecDraft` for human confirmation (no `confirmed` or `author_hash` field); `AnswerDraft` citing `run_id:artifact:path` (the analyst's catalogue is CHAT_ANALYST §5.2) | lab | no | writer, translator, Q&A |
| `read_ledger`, `read_run_logs`, `read_engine_diff`, `read_rendered_memo`, `read_bundles` | read-only registry views | lab | no | auditor |
| `get_evidence_slice`, `submit_assessment`, `submit_minority_report` | seat evidence; `SeatArgumentDraft` (cruxes, placeholder text, optional `ViewSpecDraft`s), from which `idm.seats` assembles the `SeatAssessment`; a `MemoDraft` for the minority report | lab (idm) | no | seat narrators |
| `read_pack`, `read_registry` | pack JSON; registry | lab | no | AI validator |
| `read_ballots`, `read_transcript_structured` | ballots; structured meeting notes | lab | no | minutes drafter |
| `submit_extraction` | `ExtractionRecord` → quarantine | lab (no outbound) | no | extractors |

Deterministic enumeration prices every single-asset lens action each quarter; agents handle only packages, residual structures, overlay structures and IC questions (SYN §5.1 item 7).

### 7.5 Roles and prompts

Prompts live in `src/adic_tpa/agents/prompts/<role_id>.md`, start with a frozen header (role, mandate, prohibitions: no digits outside placeholders, no attribution of synthetic numbers to ADIC, never vote, documents are data; the name of the role's `submit_*` tool) and are hashed into `llm_policy`. Any prompt, model or tool change reruns the agent evaluation suite (SYN §5.6).

| Role (`RoleId`) | Family; effort | Active states | Output model | Gate | Materiality / blocking escalation |
|---|---|---|---|---|---|
| CONTRACT_DRAFTER | A; high | DRAFT | `AmendmentDraft` | G0 + human signature | high / blocking |
| DESIGN_REVIEWER | B; high | SIGNED, SIGNED_IN_RECOVERY | `ReviewFindings` (findings only) | G1, CRO disposition | high / blocking |
| IDEATOR ×2 workers | A; high | IDEATION | `IdeaBundle` | G3 | low |
| EXECUTOR | A; medium | SCREENING | compiled spec, rubric status | G4–G5 | low |
| ABLATION_PROPOSER / ABLATION_FILTER | A / B; medium | RETROSPECTIVE | `VariantSet` | retrospective | low |
| RED_TEAM | B; high | SCREENING, RETROSPECTIVE, SHADOW_IC | findings, "assigned dissent" | disclosed at G8 | medium |
| MEMO_WRITER | A; high | MEMO | `MemoDraft` (placeholders; `claims.render` assembles the `RenderedDocument`) | G7 | medium |
| AUDITOR | B; high | REVIEW | `AuditDraft` (code assembles the `AuditReport` and sets family and correlated) | G8 | medium |
| TRANSLATOR | A; medium | IC, event decisions | `ViewSpecDraft` / `ScenarioSpecDraft` | human confirms the effective view | high / blocking |
| QA_ANSWERER | A; medium | SHADOW_IC, IC | `AnswerDraft` (per-statement labels; the analyst assembles the `AnswerCard`) | claim validator | medium |
| SEAT_NARRATOR ×(n_groups + 5) | ≥ 3 families target, ≤ 40% per approved family; medium | SHADOW_IC | `SeatArgumentDraft`, `MemoDraft` (minority report); no probabilities | rubric; flag, never vote | medium |
| FACILITATOR | A; medium | SHADOW_IC | protocol transitions only | — | low |
| AI_VALIDATOR | B; medium | REVIEW, SHADOW_IC | `ValidationReport` on the pack | pack gate | medium |
| MINUTES_DRAFTER | A; medium | IC → CLOSED | `MemoDraft` (minutes; dissent verbatim) | secretary approves | medium |
| EXTRACTOR ×2 (real-data phase) | A; low | outside campaigns | `ExtractionRecord` | schema + human sample | medium |

Every role ends by calling its `submit_<artifact>` tool; the meta-controller re-validates the payload with Pydantic, allowing ≤ 3 retries on validation failure (paper l.6290). Every output model is an LLM draft model with no engine-, validator- or human-owned field; dict fields are `KeyValue` lists and fixed tuples are named sub-models, and `tests/agents/test_llm_schemas_transform.py` runs `check_llm_schema` on each (S-ADR-36; BUILD-10).

### 7.6 Meta-controller states and transitions (`lab.fsm`)

| State | Entry gate (engine-side inputs only) | Actions | Next |
|---|---|---|---|
| DRAFT | — | contract from template; drafter proposes amendments; data cut-off | FROZEN |
| FROZEN | **G2**: snapshot, initial state, FBE-R (using prior-quarter frozen optimizer outputs) hashed; flagged assets reviewed by humans | — | SIGNED or SIGNED_IN_RECOVERY |
| SIGNED / SIGNED_IN_RECOVERY | **G0**: Phase I for R0x–R2, recovery mode, plane hashes, salt commitment, CIO + CRO SignOffs (+ Board, + owner if structural/band) | — | DESIGN_REVIEWED |
| DESIGN_REVIEWED | **G1**: family-B review + deterministic linter; CRO dispositions every finding | — | BASELINE_PRICED |
| BASELINE_PRICED | H on 5 replications at the default preset (increment 1: what-if preset); no pinned duals; Level B with Γ; cards for every holding; envelopes; draft FTP; module F; C_H defined | — | IDEATION (campaign enabled) or SELECTION |
| IDEATION | budget left | ideators submit bundles (MAP-Elites quota: every third cycle a worker targets an under-filled cell) | SCREENING |
| SCREENING | **G3** schema and DSL compile | executors evaluate; **G4** `correct`, **G5** selection | IDEATION, or SELECTION on the stop rule |
| SELECTION | — | finalists frozen (incumbent, ≤ 3 archive cells, C_H always; ≤ 4); memory writes close | SEALED |
| SEALED | commitment verified (REAL: CRO-account salt; DEV_SYNTHETIC: the single-account software seal, commit–reveal checked in code) | seal service runs the final plane once; **G6** labels | RETROSPECTIVE |
| RETROSPECTIVE | — | controls at 3/5/10 years, switch-off null, single-change ablations (no tuning), red team, one bootstrap rerun | MEMO |
| MEMO | — | writer drafts with placeholders; renderer fills | REVIEW |
| REVIEW | **G7**: claim coverage = 1, validator pass, plane labels, ICD-203 words, P14 fields | auditor; human countersignature (**G8**: family-B PASS with ≤ 4 findings) | SHADOW_IC |
| SHADOW_IC | — | `RoomPort.run_shadow_ic` (S0–S7) | PREVOTE_LOCK |
| PREVOTE_LOCK | — | human blind pre-votes locked (T−1); in DEV_SYNTHETIC the seeded `testing.synthetic_committee` casts them, labelled SYNTHETIC (S-ADR-37) | IC |
| IC | — | H1–H6; ballots (synthetic committee in DEV_SYNTHETIC) | CLOSED (**G9**: pre-votes locked, ballot, dissent, overrides with reason codes, signposts, review date) |
| ABORTED | hash mismatch, seal breach or canary, hard budget cap, human stop | campaign frozen; incident record | — |

ESCALATE is a per-worker overlay reachable from every state; it pauses only the requesting worker (blocking roles) and never the deterministic baseline. The freeze precedes the contract check because Phase I needs the frozen state. **Stop rule:** budget spent, 6 cycles without a promotion, or no column with a positive robust reduced cost. Engine faults retry under their own budget as degraded phases, shown and never passed silently; candidate-caused failures count as evaluations. FSM state persists in the registry, so `tpa lab status` and restarts are exact.

### 7.7 Budgets, counting and the overfitting adjustment

Defaults from `BudgetSpec` (ARCH §7.7; calibrated by §7.14): 24 idea cycles (12 per worker), ≤ 650 counted search evaluations, ≤ 2 EvalRequests per attempt, tuning jobs ≤ 24 counted CMA-ES evaluations, LLM spend $50 soft / $200 hard per cycle (expected ≈ $35 per campaign), ≈ 20 core-hours, 2 workers (configurable to 4). The evaluator counts every call, failures and retries included; BUDGET_EXHAUSTED is distinct from EXECUTION_FAILED. Error control: decaying-memory generalized α-investing across cycles (W₀ = 0.05, payout 0.05, escalate below 0.005), Holm within a cycle, mFDR across contracts (S-ADR-18). Reported to the IC: N_eval (incl. failures), clustered N_eff, the deflated improvement ΔΨ̂ − SE·q_{0.95}(max_{N_eff} Z) (`stats.deflated_improvement`; the 95% null quantile of the maximum, ≈ 3.47 at N = 200), DSR with its benchmark Sharpe from the expected maximum (`stats.expected_max_z`, ≈ 2.75 at N = 200) and its non-normality term (v1.0 used the expectation where the quantile belongs; BUILD-20), the search-to-final optimism gap and PBO from the search ledger.

**Evaluation kinds** (BUILD-30; B8). Every evaluation is charged in measured core-seconds to `BudgetLedger`; the expected charge follows from B1's ≈ 36 core-seconds per 10,000 paths per world:

| Kind | Worlds | Paths per world | Expected charge (core-s) | Budget use |
|---|---|---|---|---|
| `race` (screening; `evaluate_policy`, successive-halving rungs) | 7 search worlds (M1–M6, B1) | 2,000 | ≈ 50 | 650 evaluations ≈ 9 core-hours |
| `confirm` (Gate-1 confirmation of promotion candidates only) | 7 | 10,000 | ≈ 250 | ≈ 100 candidates ≈ 7 core-hours |
| `tune` (CMA-ES inside a declared box) | 7 | 2,000 | ≈ 50 per counted evaluation | inside the 24-evaluation tuning cap |
| `price_package` | tree only (warm H re-solve) | — | ≈ 20 | counted |
| `scenario`, `reverse_stress` (exploration) | 1–3 | 10,000 | 36–110 | exploration budget |
| `final` (sealed, once) | final worlds + B2 + misspecification | 50,000 | ≈ 180 per world | outside the lab budget |

The lab budget is therefore ≈ 16 core-hours against the 20 core-hour cap (v1.0 implied 76 core-hours by confirming every evaluation at 10,000 paths).

### 7.8 Logs, escalation and the assumption log

Ledger kinds (`registry.append_ledger`): `eval_request`, `eval_record`, `llm_call`, `budget`, `escalation`, `assumption`, `seal`, `drill`. `escalate(kind, question, blocking, proposed_assumption, severity)` routes to the RACI owner in the contract; a blocking call pauses the worker (high-materiality roles always block); a non-blocking call proceeds under a logged assumption that tags every downstream artifact and prints in the memo and the pack appendix. "Data insufficient" is an admissible output (reversing paper l.6406-6408).

### 7.9 Memory

An append-only event log plus a per-worker conclusions paragraph of ≤ 300 words, changed only on a contradiction, a new category, a Do/Don't flip or a named refinement, with logged decisions; shared at cycle boundaries; pruned every 8 cycles [I]; writes close at SELECTION (before any final result exists; paper l.6798); archived read-only at CLOSED and never loaded into another campaign (LC M4). The writer, the auditor and the seats cannot read it; the validator rejects any document citing it.

### 7.10 Cross-family review and admission tests

Reviewer, ablation filter, red team, auditor and AI validator run on family B. In Phase 0 family B is `claude-sonnet-5-5` with a disjoint context and role prompt, and every such review is labelled "correlated", never extremized; the ≤ 40%-per-family seat rule applies only across approved families (ADR-30). Admission tests before a role is trusted (run on Replay cassettes recorded live): judges κ ≥ 0.6 on ≥ 50 golden items; auditor ≥ 90% recall on seeded semantic errors; translator pass³ ≥ 0.9; sycophancy < 10% unjustified flips; re-run after any model upgrade (S-ADR-18).

### 7.11 MCP servers (`mcp_server.py`, mcp 2.3, stdio)

| Server | Tools | Restrictions |
|---|---|---|
| **evaluator** (`tpa mcp serve --server evaluator --plane {search,exploration}`) | every evaluator tool of §7.4 | never the final plane (only `seal.run_sealed` spawns a final instance), never the sealed truth, no write path to engines, beliefs or scenarios; per-request hash checks; counting |
| **analyst** `adic-tpa-analyst` (read-only; any authorized principal's MCP client; `tpa mcp serve --server analyst --quarter 2026Q4`) | the role-filtered 30-tool catalogue of CHAT_ANALYST §5.2: reads, draft previews and `run_whatif` after confirmation; no direct `optimize_h`; no forecast intake (S-ADR-34; BUILD-08) | same restrictions; exploration grade and SYNTHETIC-only until Q6; tool results are pre-rendered cards; long simulations return a run handle polled through `get_run_status` |

### 7.12 CLI (`tpa`, typer)

| Command | Purpose |
|---|---|
| `tpa data freeze --asof DATE [--store PATH]` | bitemporal freeze → `BookSnapshot` + hash |
| `tpa data adapt --source ID --raw PATH` | run a real-data adapter (WP-37) with quarantine |
| `tpa synth build [--allocation v2] [--census v1.1] [--release R0] [--seed N]` | build a SYN-ADIC-177 release |
| `tpa synth gates --release PATH` | V1–V24 (+ VR1–VR3) report |
| `tpa scen build --world M1 --plane search --paths 10000` | build and checksum a cube |
| `tpa state snapshot --asof DATE` | initial state + panel |
| `tpa run quarter --asof DATE [--synthetic] [--offline\|--replay\|--live] [--campaign/--no-campaign] [--allocation v2] [--census ID]` | the full quarterly cycle (pipeline) |
| `tpa phase1 [--scenario R0x…R2]` | Phase I report |
| `tpa h solve --preset {whatif,default,signoff,overnight} [--replications 5]` | H with duals |
| `tpa p certify --policy REF --plane {search,final}` | certification (final only through the seal) |
| `tpa evaluator serve --plane {search,exploration,final}` | evaluator process (`final` refuses unless spawned by the seal runner) |
| `tpa seal commit\|run\|reveal --campaign ID` | commit-reveal and the once-only final run (REAL: CRO account; DEV_SYNTHETIC: single-account software seal) |
| `tpa lab start\|status\|escalations\|resolve\|stop` | meta-controller control |
| `tpa room compile\|pack\|prevote\|ballot\|record\|sign` | decision room; `sign` creates `SignOff` objects for an authenticated human |
| `tpa mcp serve --server {evaluator,analyst} [--quarter Q]` | MCP servers |
| `tpa chat [--offline\|--replay\|--live] [--quarter Q] [--via-mcp]` | the conversational analyst REPL (§4.35; CHAT_ANALYST §3.3) |
| `tpa chat eval --golden PATH --backend {stub,replay,live}` | golden-set evaluation of the analyst |
| `tpa ask serve [--quarter Q]` | v1: loopback (127.0.0.1) Ask service for the pack's live view |
| `tpa analyst confirm\|runs\|transcripts` | human confirmation of an MCP-drafted what-if; own runs; transcripts (user and GOV only) |
| `tpa forecast register --file PATH` | human forecast intake (operator token) |
| `tpa replay record --campaign ID` | record live LLM responses into cassettes |
| `tpa bench [--suite B1…B12]` | benchmarks |
| `tpa audit labels\|chain\|layering\|allowlist` | labelling audit, registry chain, import rules |
| `tpa config show\|hash` | configuration and hashes |

All commands log JSON; every `TPAError` exits non-zero with its `code` (hash mismatch, non-optimal solve, pinned dual, missing cache, unmet evidence contract all stop loudly).

### 7.13 Integrity drills (CI, `tests/drills/`)

| Drill | Expected failure |
|---|---|
| `test_tamper_engine_hash` (edit an engine file between signing and a request) | ABORTED with HASH_MISMATCH |
| `test_chain_verification` (edit a ledger row) | `verify_chain` names the row |
| `test_over_budget` | BUDGET_EXHAUSTED; no further evaluation |
| `test_search_opens_final_store` | permission error / `SealBreach` |
| `test_world_list_hash_at_sealed` | mismatch → ABORTED |
| `test_failed_paths_worst_case` | failed paths scored worst-case, never dropped |
| `test_seeded_overclaim_flagged` | auditor flags; validator blocks improvement verbs on NOT_QUALIFIED |
| `test_fabricated_number_memo` | LITERAL_DIGIT rejection |
| `test_planted_leak_fails_compile` | INVALID_SPEC/TR1 or TR2 |
| `test_fabricated_data` (an agent output claiming new holdings) | rejected: only `synth` creates data |
| `test_no_horizon_reference` | compile error |
| `test_cache_mismatch_stops` | CACHE_MISS, no recomputation |
| `test_memo_cannot_cite_memory` | CITES_MEMORY |
| `test_escalation_pauses_worker` | worker paused; assumption tags on artifacts |
| `test_no_payout_lever_in_mode_B` | INVALID_SPEC/TR8 |
| `test_canary_in_agent_channel` (S-ADR-18) | SEAL_BREACH → ABORTED |
| `test_relabel_sale_reason_leaves_p_red` (QUANT-03) | P(red) unchanged under any permutation of `SaleReason` labels |
| `test_llm_number_not_rendered` (S-ADR-36) | an `EffectForecast` or extraction confidence reaching a rendered or aggregated output → LLM_NUMBER_RENDERED |
| `test_dev_mode_refused_in_real` (S-ADR-37) | software seal, test key or synthetic committee requested in REAL mode → RUN_MODE |
| `test_analyst_read_only` (S-ADR-34) | every write path from the analyst process refused; `run_whatif` refused before confirmation |

### 7.14 Lab calibration with planted effects (WP-38; ARCH §7.12)

Campaigns on SYN-ADIC-177 worlds with (i) a planted true gain of known size, (ii) a planted leak, (iii) a null world measure power, false-qualification rate and leak detection; ε_mat and budgets are set so power ≥ 0.8 at the planted effect and false qualification ≤ 5% [I]. The contract states the miss-to-false-discovery cost ratio and the sealed test's MDE. "Zero qualified" is a valid campaign outcome; the deterministic baseline (cards, C_H's sealed verdict) still carries the IC.

---

## 8. IC pack specification

### 8.1 Build and packaging (`pack.build_pack`; `tpa room pack`)

| Output | Content |
|---|---|
| `runs/<quarter>/pack/index.html` | **One self-contained file**: inline CSS (`static/pack.css`), the plotly.js bundle shipped inside the installed `plotly` package (inlined once), inline `static/ep.js`, and JSON payloads in `<script type="application/json">` blocks (float16 matrices base64-encoded). A `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'">` forbids any network request. Target size ≤ 15 MB |
| `runs/<quarter>/pack/pack_manifest.json` | run ids, artifact refs, metric ids used, pack hash, theme hash, payload checksum, data class |
| `runs/<quarter>/pack/decision_log.jsonl` | §8.7 |

Templates (jinja2, `pack/templates/`): `base.html.j2` (shell, theme tokens, footer), `l0.html.j2`, `l1_brief.html.j2`, `l2_drill.html.j2`, `console.html.j2` (W1 view conditioning and the Ask panel). The static `index.html` keeps `connect-src 'none'`, so in increment 1 the Ask panel hands off: it shows the `tpa chat --quarter <q>` command with the pack's context handle, and W1 still works from `file://`. In v1, `tpa ask serve` (WP-40) serves a second build, `index_live.html`, from 127.0.0.1 with `connect-src 'self'`, a per-launch token, cookie, Host, Origin and CSRF checks and no CORS: the one documented exception to the no-network rule (CHAT_ANALYST §3.4; S-ADR-34). Figures are plotly divs produced by `figure_html` with `include_plotlyjs=False` (the bundle is inlined once in `base`). Every narrative paragraph comes from a `RenderedDocument`; templates contain no numbers.

### 8.2 Sections and figures

| Section | Content | Form (one axis; table view for every chart) |
|---|---|---|
| **L0-1** CFP and survival | readiness, event and planning stages; T4′ survival months (T and TP); in recovery: mode, u*, d₀, IIS, glide path, priced consent scenario | stat tiles with status icon + label |
| **L0-2** Tier-1 board | rows T1–T9 and Tier-1B; columns M1–M6, MIX; cell "p̂ [CP upper]" with band status (appetite/tolerance/capacity); P(10%) row printed beside P(red), labelled "reported, never optimized" | table |
| **L0-3** Owner draw | next 4 instalments with P10–P90; funding waterfall in the binding state ("Can we pay the next four instalments without a red sale?") | single-series bar chart + table |
| **L0-4** λ and FTP | decision FTP by tenor (1–12 quarters) at tolerance and appetite, min–max band across replications; published curve; change vs last quarter; λ^spot by regime; λ decomposition by binding row | line chart (2 series) + table |
| **L0-5** WYNTB bridge | per world: beta, levers, drags, gap to 10%, P(μ ≥ 10%) range, verdict | small multiples (one waterfall per world) + verdict tiles |
| **L0-6** Package vs controls and archetypes | status quo (or restored baseline in recovery), DEFER, recommendation, archetypes A/B/C; ΔCE bp ± SE; P(red) by class; Δsurvival months; P(10%) beside P(red); gate label | dot plot of ΔCE with CI whiskers; separate dot plot of P(red) by class; table |
| **L0-7** Decisions this quarter | Register items, decider, tier, deadline, consent-agenda eligibility | table |
| **L0-8** State panel | the 12 rows of gap_04 §8 with readiness and event stages shown separately on the liquidity-gate row | table with status icon + label |
| **L0-9** Lab block | what was tried, what qualified, what did not; N_eval, N_eff, deflated improvement, optimism gap, PBO; scaffolding vs searched share | table |
| **L1 brief** (per Register item; ≤ 1 page, ≤ 6 for Tier A) | (1) question, deadline, decider, recusals; (2) options; (3) consequences: ΔTier-1 by class with CP bounds, ΔJ in bp and $, Δsurvival, ΔP(10%) reported only; (4) economics: λ-priced waterfall, binding rows, shadow prices with one-sided intervals, marginal value per action, envelope use, `priced_on`, Γ; (5) beliefs: raw vs fused marks, market anchor, information value, flags; (6) disagreement: implied-action map (seat × option regret), belief/value split, minority reports (authentic first; Red Team labelled "assigned dissent"); (7) what would change it: flip thresholds, signposts, cross-fitted EVSI when DEFER is live | horizontal bar waterfall; tables; regret heat table (sequential blue ramp) |
| **Group blocks** (one per group, taxonomy order) | envelope use and priced requests (inside ranging), decision cards, hurdle, FTP, delivery share φ_g in recovery, own information value (only at n_eff ≥ 20), DVA | small multiples by group; card tables |
| **Treasurer view** | LR1–LR8, CFP readings, facility and covenant headroom, effective maturity and rollover (S-ADR-12), VM/IM by CSA, draw fan, decision vs published FTP, mismatch P&L, infeasibility prices (labelled; never on cards) | tables; T4′ headroom fan (line + band) |
| **CRO view** | Tier-1 board detail, CP bounds, class bands, recovery status, k_MS, η*, bPOE, gambling and RFY flags, OV1–OV3 | tables |
| **Overlay view** | offset card per named stress (tail and opportunistic P&L, offset ratio, economic vs SIMM net vega, IM by CSA, λ-priced IM saving, stress-coverage ratio), convex budget and carry, fatigue tracker, ex-ante tail credit, services ledger | tables |
| **L2 drill-down** | for every number: metric definition, CI method, model range, MC error, scenario hash, run manifest summary (engine SHA, config hash, seed spawn, solver record); raw artifact excerpt | drawer panel (≤ 2 clicks from any number) |
| **Appendix** | assumption log, escalations, controls at 3/5/10 years (static SAA, deck rules, target-chasing labelled "gambling control", placebo, pro-rata, overlay-only, liquid-first, cash-last), census side by side (S-ADR-03), model weights, open questions | tables |

### 8.3 Visual grammar and theme (`pack/theme.py`, `config/pack/theme.yaml`)

- **Probabilities** render as "37% [26–38%] ± 0.2pp" = central [model range] ± MC error, followed by a short scenario hash, an ICD-203 word and a plane badge (SEALED / SEARCH / EXPLORATORY). ICD-203 bins (half-open): [1%, 5%) almost no chance; [5%, 20%) very unlikely; [20%, 45%) unlikely; [45%, 55%) roughly even chance; [55%, 80%) likely; [80%, 95%) very likely; [95%, 99%] almost certain; outside 1–99% only the number (ARCH §8.4).
- A difference with |Δ| < 2 paired SE is greyed; P(10%) always sits beside worst-model P(red); CE values carry "≈ $X m a year".
- **Palette** — the dataviz reference instance, used unchanged (validated by its authors; any change must be re-validated by loading `validate_palette.js` as a module in a dev page, since no Node is installed). Categorical slots in fixed order: worlds M1–M6 → slots 1–6, light `#2a78d6, #eb6834, #1baf7a, #eda100, #e87ba4, #008300`, dark `#3987e5, #d95926, #199e70, #c98500, #d55181, #008300`. Line and bar charts may carry up to six world series (adjacent-pair gates pass); scatter-type forms carry at most three series, otherwise small multiples. Groups never get color identity: group charts use small multiples or single-hue bars with labels (identity by label, not color).
- **Status colors** (reserved, always icon + text label): Green → good `#0ca30c`; Amber → warning `#fab219`; Red → critical `#d03b3b`; Black → primary ink (`#0b0b0b` light / `#f0efec` dark) with a "■ BLACK" label; serious `#ec835a` marks "watch" annotations only.
- Sequential (regret heat tables): blue ramp steps 250–700 for ordinal cells; diverging (Δ vs status quo): blue ↔ red with a gray midpoint (`#f0efec` light / `#383835` dark).
- Chrome: surfaces `#fcfcfb` / `#1a1a19`; ink `#0b0b0b` / `#f0efec`; secondary `#52514e` / `#c3c2b7`; gridlines `#e1e0d9` / `#2c2c2a`. Colors are CSS custom properties on a `.viz-root`, redefined under `prefers-color-scheme: dark` (guarded by `:not([data-theme="light"])`) and under `[data-theme="dark"]`.
- Rules: one y-axis per chart (never dual axes); a legend for ≥ 2 series plus direct labels when ≤ 4; numbers and labels in ink tokens, never series colors; hover tooltips on every mark; system sans font; tabular figures in tables; the SYNTHETIC footer in every section.

### 8.4 Client-side view conditioning (W1)

**Payload** (`pack.ep_payload`, embedded as `<script type="application/json" id="ep-payload">`):

```json
{"version": 1, "n_paths": 10000, "data_class": "SYNTHETIC", "checksum": "sha256:…",
 "metrics": [{"id": "terminal.twr_10y", "label": "10-year TWR", "unit": "decimal a year", "kind": "terminal"}, "… ≤ 40"],
 "matrix_f16_b64": "<row-major float16 [10000 × K]>", "world_of_path_i8_b64": "<int8 [10000]>",
 "prior_f32_b64": null,
 "view_library": [{"id": "pe_dist_rate_2027", "metric": "…", "ops": ["eq", "le", "ge"], "default_c": 0.6}],
 "golden": [{"views": [{"metric": "…", "op": "eq", "value": 0.0, "c": 0.6}],
             "expected": {"kl": 0.0, "ess": 0.0, "means": {"…": 0.0}, "probs": {"…": 0.0}}}]}
```

Paths are drawn from the certification run stratified by world in proportion to w_m (seeded); the golden cases are computed by Python `robust.entropy_pool` **on the float16-decoded matrix**, so JS and Python see identical inputs.

**Algorithm** (`static/ep.js`, ≤ 150 lines of vanilla JS, no dependencies): decode float16 to `Float64Array`; target shrinkage v_eff = E_p[g] + c(v − E_p[g]); Newton on the dual f(λ) = ln Σ_i p_i e^{λ′g_i} − λ′v_eff with gradient E_q[g] − v_eff and Hessian Cov_q[g] + 1e-12·I, Armijo backtracking (β = 0.5); inequality views by projected Newton with sign-constrained λ and an active set; stop when max|grad| ≤ 1e-10·(1 + |v|) or after 50 iterations; outputs q, KL = Σ q ln(q/p), Kish ESS = 1/Σq², and max q/p. **Gates** (one rule with `robust`, §4.25; QUANT-32): KL > 0.05 inform, > 0.20 warn, > 0.35 amber, > 0.80 red (forces W3; further W1 disabled), consistent with the ESS floor because ESS/N = e^{−2KL} for a Gaussian tilt; Kish ESS warns below 0.5N (5,000 of the payload's 10,000 paths) and blocks below 0.2N (2,000); ratio > 50 warns. (v1.0's amber and red gates at 1.20 and 2.30 nats could never be reached under its own ESS ≥ 5,000 block.) Recomputed headline metrics (P(red) by class, P(10%), median TWR, CE) are labelled EXPLORATORY.

**Self-test on load:** every golden case runs; KL, ESS, means and probabilities must match to 1e-6 (absolute for probabilities, relative for means); any mismatch disables W1 behind a red banner. **Logging:** any W1 number entering a DecisionRecord is recomputed by Python (`tpa room record` calls `robust.entropy_pool` with the logged views); the logged value is the Python one (ARCH §8.7; JE-MF14).

### 8.5 Claim-to-run links

The renderer wraps each value as `<span class="m" data-metric="<metric_id>" data-ref="<run_id>:<artifact>:<json-pointer>" data-plane="SEALED">…</span>`. Click 1 opens the L2 drawer (definition, CI method, model range, MC error, scenario hash, manifest summary); click 2 shows the embedded artifact excerpt and the full manifest JSON. Analyst answers (`AnswerCard`, §4.35) cite `run_id:artifact:path` and label each statement "model output", "agent judgment" or "assumption"; an "agent judgment" statement carries no number (S-ADR-36).

### 8.6 Archetypes and controls

Every recommendation table shows status quo, DEFER, the recommendation (C_H or a QUALIFIED finalist) and archetypes A/B/C (§4.19), all on CRN with ΔCE, P(red) by class, Δsurvival and P(10%) beside P(red). In recovery the comparator row is the restored Phase-II baseline and HOLD is shown as "control, Tier-1 infeasible" (ADR-31). A materially projected archetype is labelled "Tier-1 infeasible as specified". NOT_QUALIFIED and NOT_ASSESSED rows carry their labels and the validator blocks improvement verbs. A QUALIFIED label never substitutes for the ballot.

### 8.7 Decision log format

`decision_log.jsonl`: one canonical-JSON `DecisionRecord` per line with `prev_hash` and `record_hash = sha256(prev_hash ‖ canonical_json(record without record_hash))`; the first record's `prev_hash` is `sha256:` followed by 64 zeros. Outcomes (Brier scores at 1, 4 and 8 quarters) are appended as new `outcome` records referencing the `decision_id`; nothing is edited. The registry mirrors the chain; `tpa audit chain` verifies both. Signposts are monitored monthly by `idm.find_signposts` outputs: alarm at 0.5σ on the safe side, re-arm after a 0.25σ retreat; an alarm triggers a Tier-B review, a flip a Tier-A re-decision.

### 8.8 Pack linter (`pack.lint_pack`; runs before publication)

Rejects: a missing SYNTHETIC footer on any tainted section; cross-group league tables (any table ranking groups by forecast skill, credibility, DVA or regret); named-person regret ("regret of the PE head"); blueprint illustrative figures; a probability without its range; any number element without a resolving `data-ref`; any network reference (the loopback `index_live.html` build excepted); any LLM-originated number rendered or aggregated, including seat probabilities, `EffectForecast`s and extraction confidences (`LLM_NUMBER_RENDERED`; v1.0 allowed seat probabilities labelled "agent judgment"; S-ADR-36, QUANT-10); credibility shown below n_eff = 20; P(10%) without an adjacent P(red); a card without `priced_on`; an envelope or FTP point derived from a reverse stress.

### 8.9 Usability acceptance (`tests/room/` plus IC user testing)

L0 readable in ≤ 5 minutes (≤ 250 words of narrative; each block within one screen height); every number ≤ 2 clicks from its manifest; W1 < 1 s for 10,000 paths and ≤ 20 views; pack published by T−7; no item reaches the ballot with an unmet evidence contract; every Register entry renders; incomplete briefs rejected; seeded numbers caught; recused votes excluded from the tally; pre-votes immutable after lock.

---

## 9. Build plan

### 9.1 Waves

Waves 0–5 deliver **increment 1, the MVP slice** (ARCH §11.6): a thin end-to-end path through every layer, at reduced fidelity, behind the final interfaces. Waves 6–7 deliver **v1** by deepening modules behind unchanged interfaces (ADR-34). Every WP in a wave can run in parallel once its dependencies' *interfaces* exist; WPs build against `adic_tpa.testing` fixtures and fakes until upstream code lands.

| Wave | WPs | Theme | Gate to leave the wave |
|---|---|---|---|
| 0 | 01, 02, 03, 04 | Contracts, RNG/numerics/stats, testing kit, registry | the walking skeleton green (§4.5), then `contracts-v1.0` tagged (end of week 2); frozen fixture checksums committed; layering and allowlist tests active |
| 1 | 05–14 | Data, world and asset engines, ledger, beliefs, bridge | each WP's DoD; Protocol conformance tests pass against the frozen fixtures |
| 2 | 15–19 | Synthetic book, actions, simulator P, H with Phase I/II and duals, selection and module F | ledger–simulator integration (week 4), simulator on the real engines (week 5), H on real coefficients (week 6); sprint-1 production H benchmark recorded |
| 3 | 20–24 | ICM and MPC, DSL and search, robustness, attribution, evaluator and seal | evaluator runs as a separate process with hash checks, counting and Gates 1–3 |
| 4 | 25–29, 39 | Claims and agents, lab, decision room, pack, CLI and MCP, analyst thin slice | FSM reaches CLOSED offline in DEV_SYNTHETIC mode; pack v0 builds; the analyst golden set runs on Stub |
| 5 | 30 (+ 39 completion) | Pipeline, integration, end-to-end demo | **increment-1 exit (week 10):** §9.4 passes |
| 6 | 31, 32, 33, 35, 37, 40, 41 | v1 part 1: worlds and families, Level-2 overlay, production H, full room, real-data adapters, analyst v1, public market data | each WP's DoD |
| 7 | 34, 36, 38 | v1 part 2: search and sealed certification, full attribution, lab calibration | v1 exit (ARCH §11.6): V1–V24 (n/a gates excepted) and G-A–G-E green; sealed plane run once; room and analyst offline suites pass (≥ 300 golden items) |

### 9.2 Work packages

| WP | Wave | Module(s) | Depends on | Deliverables | Definition of done (all tests offline, CI green) | Parallel with |
|---|---|---|---|---|---|---|
| **WP-01** | 0 | `contracts`, `pyproject.toml`, `.gitattributes`, `tools/dev_install.py`, `config/taxonomy/*` | — | every §3 model and enum (incl. the recourse protocol, `BeliefDraws`, the contexts, the LLM draft models and `contracts/analyst.py` per CHAT_ANALYST §5, i.e. WP-CHAT-01), units, calendar, hashing incl. `canonical_artifact_hash`, signing, `contracts.rules`, errors, the JSON-mode config loader, `ARRAY_SPECS`, Protocols, taxonomy v1/v2 | §4.1 tests incl. config round trip, LF hashing and signing; contracts tagged only after the walking skeleton (WP-03) is green; `test_no_hardcoded_group_ids` and allowlist harness in place | 02–04 after day 5 |
| **WP-02** | 0 | `rng`, `numerics`, `stats` | 01 | keyed Philox, samplers, PWL/roots/linalg, CP/bootstrap/Holm/α-investing/DSR/PBO/MDE/bPOE/CE | §4.2–4.4 tests; numpy-Philox equivalence; ≥ 50M uniforms/s | 03, 04 |
| **WP-03** | 0 | `testing`, `tools/port_research.py`, `tests/golden`, `tests/regression/fixtures` | 01 | mini book (v1, v2), mini cube, mini FlowCube, fixture tree, fake engines and ledger, fixture H (`LPModel`, `HSolution`, `DualSet`, `Tree` from the gap_02 export), fakes for the stress filter, owner draws and belief draws, the synthetic committee, golden loader, the walking skeleton; research fixtures copied read-only with SHA-256 (hf_ladder, t1_engine ladder readings, gap_02 and G-gap_01 coefficient exports, the gap_02 G*(θ) grid and per-model gap quantiles, perf golden cases, bridge, v8 replica, SIMM example, sealed PE history) | frozen checksums committed; the walking skeleton green on `mini_book` (the gate for tagging contracts); fakes pass Protocol conformance; port manifest lists every source file and hash | 02, 04 |
| **WP-04** | 0 | `registry` | 01 | SQLite + artifacts, hash chain, metric registry, provenance, mFDR table | §4.6 tests incl. tamper drill | 02, 03 |
| **WP-05** | 1 | `data` (store, schemas, freeze, taint, quarantine, adapter base, `adapters/marks_archive.py` schema) | 01, 04 | bitemporal store; snapshot freeze/hash; the marks-archive adapter's schema and contract test (since-inception net IRR/MOIC with cases; as-of mapping to holding and quarter; S-ADR-27) | §4.7 tests; marks-archive contract test on a fixture archive | 06–14 |
| **WP-06** | 1 | `scen` (M1, M6, B1 on the 8-factor subset), `data_public/` | 01, 02, 03 (fake filter), 07 (interfaces) | engine E (standardized t₅, principal 12th root, expected-log anchor, declared factor kinds), oil, vol states, fin window, crowding index, B1 on the panel's columns with labelled fills, cube build/verify/regenerate | anchors ≤ 5bp and vol/correlation checks (M1, M6); provenance flags; checksum reproducibility; ≤ 2.5 s per 10k paths with tabulated samplers | 05, 07–14 |
| **WP-07** | 1 | `state` | 01, 02, 05, 08 (interfaces) | stress filter, F_t, exit and shock nowcasts, initial state, panel, harness | F_t 0.10 ± 0.02 and e₀[D] 0.87 ± 0.03 on the copied panel; `simulate_filter` reproduces `forward_filter` on the panel's columns; no-look-ahead metamorphic test | 05, 06, 08–14 |
| **WP-08** | 1 | `owner` | 01, 02 | fiscal map, draw engine, modes, payout library | kink pairs; 12-month draw band; recovery; no Mode-B lever | 05–07, 09–14 |
| **WP-09** | 1 | `priv.fund`, `priv.realassets`, `priv.templates`, `priv.financing`, `config/groups/{pe,secondaries,realassets}.yaml` | 01, 02, 03, 11 (queue interface) | RFT-TA v2 (core mechanics in increment 1; G1 mechanics, recaps and extension hazards in v1) with Secondaries templates; RA interim engine; `mean_path`; `bid_fraction`; `recourse_quotes` and `apply_recourse`; `UnitFinancingBook` (the intra-quarter profiles live in `contracts.rules`) | §4.11 fund and RA tests incl. the per-world expectation, recourse and financing tests; homogeneity; roll-forward identity | 05–08, 10–14 |
| **WP-10** | 1 | `priv.company`, `priv.claims`, `priv.credit`, `priv.overlap`, `config/groups/{coinvest,capsol,privcredit}.yaml` | 01, 02, 03 | EV engine keyed by company, Capital Solutions claims, Private Credit cohorts and wrappers, overlap graph and V24 check | V24a identity; V12; co-investment P(MOIC < 1) band | 05–09, 11–14 |
| **WP-11** | 1 | `pub`, `config/groups/public.yaml` | 01, 02, 03 | HF state machine, `phi_table`, long-only, P2S, generic queue | hf_ladder port fixtures (±$0.1bn); notice-date and gate tests | 05–10, 12–14 |
| **WP-12** | 1 | `overlay` (Level 1, pricers, Greeks, CRIF, VM, SIMM-like, OV1–OV3, ladder, monetization, services, valuation), `config/overlay/*` | 01, 02, 03 | position layer for the policy book and the fixture blotter | SIMM worked example; ladder cost; seeded offset (T5); reconciled S1 use; T1–T3 | 05–11, 13, 14 |
| **WP-13** | 1 | `ledger`, `config/ledger/*` | 01, 02, 03 | kernel, row families, the recourse protocol and `red_test`, ladder, T4′ replica with the pricing and research convention sets, readiness model, CFP stages, facilities, covenants, leverage metrics incl. unit debt, linear rows | t1_engine port exact (research set); groups replica exact; readiness/event invariant; θ* by grid interpolation (≈ 0.58 class-banded, ≈ 0.76 overlay on the fixture); red-test, relabelling and recourse-protocol tests; conservation property | 05–12, 14 |
| **WP-14** | 1 | `beliefs`, `bridge`, `config/beliefs/*` (incl. `misspec_gates.yaml`, `translation.yaml`), `config/bridge/*` | 01, 02, 05 | FBE-R, the IRR/MOIC translation, group translations, market-implied mark, credibility on the full archive with the horizon cap, diagnostics, scoring, BLP, perf O3, `draw_paths` per world, `fbe_variant` generators and the validation harness; WYNTB | perf 17/17; translation round trip; SBC; G-A–G-E mechanisms (outcomes re-derived before the first scored release); draws tests; bridge regression | 05–13 |
| **WP-15** | 2 | `synth`, `config/synth/*` | 05–12 | SYN-ADIC-177 R0 on allocation v2 with censuses v1.1/v1.1r (allocation v1 + census v1.0 for the research fixtures); truth store; observation layer emitting since-inception net IRR/MOIC with cases and the 2008→as-of archive; overlay book; history fit; gates; book variants | the increment-1 blocking V-gates (+ VR1–VR3) on the decision census; census rule (V6 + V1–V2) tested; archive-shape test; sealed v1.1 history reproduced within $0.01bn; labelling 100% | 16–19 |
| **WP-16** | 2 | `actions`, `config/actions/instruments.yaml` | 03 (fixture H), 09–14 | library, admissibility, RowKey-keyed column flows, catalogue, scores (r_j − κ^irr), cards with LEVER legs and the T6-consuming flag, flips | LEVER ≡ ADD + REFI and the exposure-delta rules per instrument; additive LEVER rule; worked values; metamorphic rules | 15, 17–19 |
| **WP-17** | 2 | `core.observables`, `core.sim`, `core.factory`, `core.policy`, `core.terminal`, `core.certify`, `config/policy/*`, `config/engines.yaml` | 06–14 | P with P0, controls and archetypes as native policies; the engine factory with typed overrides; observable producers; the recourse-protocol loop; group-rate recording over 12 quarters; J and Tier-1 board; gambling, RFY and relabelling detector; certification | B1 ≤ 60 s and `test_b1_profile` per line; A1 on ≥ 20,000 CRN paths; determinism at 1/4/8 workers; failed-paths drill; certification CP coverage | 15, 16, 18, 19 |
| **WP-18** | 2 | `core.tree`, `core.h`, `core.solver`, `core.phase1`, `core.phase2`, `core.duals`, `core.kernel`, `config/core/{h_presets,solver_policy,tree}.yaml` | 13, 16 (interfaces), 17 (group rates) | §5 v1.1 in full at the what-if and default presets, with the amended `phase2`, `t6_screen` and `row_index` | pinned-dual suites 8/8 and 18/18 and the extended H test; identity 1e-9 on unreduced quarterly and semiannual trees incl. fixed SELLs; H3 and cost-neutrality metamorphic tests; kernel two-node test; A8 decision test; dual sign toy; Phase-I closed forms; **sprint-1 production benchmark recorded**; B2 per-step profile measured | 15–17, 19 |
| **WP-19** | 2 | `core.colgen`, `core.levelb`, `core.safety` | 16, 18 (interfaces) | column pricing, Level-B MILP, Γ, forced re-solves, H–P test, module F | Γ ≥ 0; 40-asset brute-force check; module F zero violations; B3 ≤ 10 s | 15–18 |
| **WP-20** | 3 | `icm`, `core.mpc`, `config/icm/*` | 17–19 | pricing, published FTP, envelopes, requests, delivery shares, recovery envelopes, charges, DVA, pacing, contingent gate, transfers, services; MPC loop with `calibrate_buffers` | KKT-cap test; recovery-envelope test; EWMA/collar; c^PACE; buffer calibration within 4 iterations on the fixture; MPC end to end on the v2 book | 21–24 |
| **WP-21** | 3 | `core.dsl`, `core.search`, `config/core/{dsl_variables,search}.yaml` | 17 | DSL parser, type rules TR1–TR8 (+ hinge, new variables), compiler, identity check; CMA-ES; successive halving on the 2,000 / 6,000 / 10,000-path rung schedule | leak drill; TR8 drill; indicator-term linter; identity at zero | 20, 22–24 |
| **WP-22** | 3 | `robust` | 02 | ensemble, KL/W∞, k_MS, η*, entropy pooling, reverse stress, persistence tilts, DRO–RS frontier, robustness card | EP exactness; perf < 1 s at 50k × 20; no-stacking test | 20, 21, 23, 24 |
| **WP-23** | 3 | `attrib` (MVP: prices, KKT interlock, capability values, null control, DVA), `core.irb` | 17–22 | explanation by prices and counterfactuals; IRB | null-control identity; IRB ≥ policy value; capability values on the fixture | 20–22, 24 |
| **WP-24** | 3 | `evaluator`, `seal` (no canary), `config/evaluator/*`, contract template | 04, 05–23 (interfaces) | evaluator service, the one MCP server factory and the client, planes, caches, counting by evaluation kind, hash checks, Gates 1–3 (class membership; PBO on the search ledger), failure taxonomy, finalists; salt, commit, sealed runner, reveal, in REAL and DEV_SYNTHETIC modes | drills: tamper, over-budget, final-store permission (`requires_accounts` in REAL), cache, world-list hash, DEV-mode refusal in REAL; agent view minimality; commit/reveal round trip | 20–23 |
| **WP-25** | 4 | `claims`, `agents`, prompts, `config/llm/roles.yaml` | 04, 24 (tool schemas) | renderer, validator (incl. LLM_NUMBER_RENDERED, UNFETCHED_REF), ICD-203, provenance; LLM backends with two-tier Replay keys, gateway, role registry with draft output models, tool loop, cost records | validator drills; `test_llm_schemas_transform`; Replay fails closed on a structural miss and reports drift; one recorded live cassette per role (or Stub-only until credentials exist, flagged); redaction test | 26–29, 39 |
| **WP-26** | 4 | `lab` (no calibration), `config/lab/budgets.yaml` | 24, 25 | FSM, budgets charged in core-seconds by evaluation kind, memory, MAP-Elites archive, escalation, firewall with fixed tool lists | FSM reaches CLOSED offline in DEV_SYNTHETIC mode with campaign off and on (Stub); budget and escalation drills; memory closes at SELECTION | 25, 27–29 |
| **WP-27** | 4 | `idm`, `config/room/*` | 24, 25 | Register (MVP entries Q1, Q2, Q4, Q5, Q6), compiler, briefs, ballots with an injected ballot source (humans; the synthetic committee in DEV_SYNTHETIC), recusal, decision log, signposts, politics linters, `RoomService`; seat specs and the `implied_actions` interface (computed seats run from v1, WP-35) | every MVP entry renders; EVIDENCE MISSING path; seat numbers only from `implied_actions` (interface test); recused votes not tallied; chain verifies | 25, 26, 28, 29 |
| **WP-28** | 4 | `pack` | 25, 27 | templates, figures, theme, EP payload and `ep.js`, linter | self-contained HTML (no network); JS = Python on golden EP cases; linter rules; ≤ 2-click links | 25–27, 29 |
| **WP-29** | 4 | `cli`, `mcp_server` (dispatch only), `__main__` | 24–28, 39 | all §7.12 commands (the analyst commands call WP-39's service) | command smoke tests; both servers answer typed calls through their factories; JSON logs | 25–28 |
| **WP-30** | 5 | `pipeline`; integration | all of 01–29 | composition root; the quarterly cycle offline; demo artifacts | **§9.4 end-to-end acceptance**; increment-1 exit criteria (ARCH §11.6) | — |
| **WP-31** | 6 | `scen` v1 (M2–M5, B2, misspecification worlds), `state` harness v1 | 06, 07, 15 | six worlds, held-out FHS family, misspecification ensemble configs (hashed), production F_t harness, optional HSMM state expansion | anchors ≤ 5bp all worlds; B2 final-plane-only; misspec configs hashed before search | 32, 33, 35, 37 |
| **WP-32** | 6 | `overlay` v1 (`templates.py`, surfaces SSVI / normal SABR / Brent SVI, full SIMM-like per CSA and product class, P&L explain, OV rows wired into H, 2020 replay) | 12, 18 | Level-2 position layer | gap_03 T1–T6; explain test; OV rows priced in H | 31, 33, 35, 37 |
| **WP-33** | 6 | `core.h` v1 | 18–20 | default preset with 5 replications in processes; nightly sign-off and overnight presets; A4, A5, A9, A17, horizon invariance; full dual-quality protocol; `forward_filtration` reducer; T6 surrogate variants; tolerance and appetite FTP nightly | B2 ≤ 120 s on the default preset; error-ledger rows green | 31, 32, 35, 37 |
| **WP-34** | 7 | `core.search` v1 + `core.certify` v1 + `seal` v1 | 21, 24, 31 | CMA-ES on M1–M6 + B1 with racing; sealed certification with B2, misspecification and slippage stresses; importance sampling; HDP-in-the-loop; nightly IRB | sealed plane run once; B5; A12, A16, A18 | 36, 38 |
| **WP-35** | 6 | `idm` v1 + `pack` v1 | 27, 28 | full Register (Q3, Q7–Q10, A1–A9, E1–E4); computed shadow IC protocol S0–S7 and H0–H6; consent agenda; DEFER with cross-fitted EVSI; root-found signposts; commitment plans; hidden-profile decision-accuracy suite | room offline suite passes; diversity alarm; minority-report triggers | 31–33, 37 |
| **WP-36** | 7 | `attrib` v1 | 23, 31 | exact 6-component Shapley; the (n_groups + 2)-player group game as a weekly job with 32 antithetic permutations and path ⊕ permutation SEs (≈ 21 core-hours at B1's 36-s design budget, against ≈ 61 for the exact 2¹⁰-coalition game, or ≈ 102 at the 60-s target as the critique computed; BUILD-31); `test_v8_replica`; what-moved-H; corridor option value; Gamba–Triantis test; owner mode values (owner packs) | Shapley efficiency; v8 replica ±0.05pp; component-claim rule | 34, 38 |
| **WP-37** | 6 | `data.adapters` (τ, PE unfunded by vintage, overlay CRIF, CSA, facility, owner draw, loan tapes; ingestion of real marks-archive files, whose schema WP-05 froze) | 05 | adapters with quarantine and fixture contract tests | contract tests; unknown fields quarantined; redaction test on REAL-class fixtures | 31–33, 35 |
| **WP-38** | 7 | `lab.calibration`, `seal.canary`, `registry.mfdr` wiring, admission tests | 26, 34 | planted-effect campaigns; canaries; mFDR ledger; judge/auditor/translator admission harness | power ≥ 0.8 and false qualification ≤ 5% at the calibrated ε_mat; canary drill | 34, 36 |

| **WP-39** | 4–5 | `analyst` (thin slice), `config/analyst/*`, `config/methodology/` | 01, 04, 24, 25, 27, 28 | CHAT_ANALYST WP-CHAT-02–04, 06, 07, 09, the W1/W2 part of 05 and the Stub/Replay part of 10: grounding forms, principals and walls, read tools and context handles, the analyst MCP server, `tpa chat`, transcripts and audit, W1/W2 what-ifs with human confirmation | the 140-item golden set on Stub (100% number provenance and labels, zero access violations); Replay fails closed; read-only drill; no run before confirmation; CLI–MCP parity | 25–30 |
| **WP-40** | 6–7 | `analyst` v1 (`ask_http.py`, W3 runs, live evaluation, human evaluation) | 28, 35, 38, 39 | CHAT_ANALYST WP-CHAT-05 (W3), 08 (loopback Ask service and `index_live.html`), the live part of 10, and 11 | ≥ 300 golden items; pass³ ≥ 0.9 live; DNS-rebinding, CSRF and non-loopback tests | 31–38 |
| **WP-41** | 6 | `data_public/` snapshot, run by a human with network access | 06 | the missing monthly public series (international and EM equity, 2-year yield, IG/HY spreads, USD, monthly Brent, secondary discounts and the other cube factors), each with source, licence, as-of and SHA-256, labelled REAL public market data; `calibrate_world` refit; the B1/B2 fills removed (S-ADR-35) | provenance flags flip to `fitted`; anchors and vol checks re-pass; B1/B2 lose their PROXY labels | 31–33 |

**Work-package count: 41** (31 in increment 1: WP-01 to WP-30 and WP-39; 10 in v1: WP-31 to WP-38, WP-40 and WP-41).

### 9.3 The MVP slice (increment 1)

Increment 1 restores ARCH §11.6's fidelity (S-ADR-37; v1.0 of this spec widened it without an ADR, BUILD-17) and implements, behind the final interfaces: the Wave-0 walking skeleton; SYN-ADIC-177 R0 on allocation v2 with censuses v1.1 and v1.1r and the marks archive in ADIC's shape (allocation v1 and census v1.0 only for the research fixtures); E with M1 and M6 plus B1 on the 8-factor subset, B1 on the panel's columns with labelled fills; simplified private engines (core mechanics; G1 mechanics, recaps, Kou jumps, amendments and extension hazards in v1) plus the RA interim engine, with the recourse protocol; the HF machine; the Level-1 overlay with the floor ladder; the reduced-form draw; the full ledger with the T4′ replica (pricing and research convention sets), the readiness model and readiness/event CFP; P with P0, controls and archetypes at 10k paths (controls at the 2,000-path race count inside B12); H at the what-if preset for decisions, with Phase I-a, consent scenarios, λ, envelopes, the top-20 cards with Γ and module F (the default preset benchmarked); FBE-R with the IRR/MOIC translation on the synthetic archive; the bridge; the evaluator as a separate process; the seal service in DEV_SYNTHETIC mode; the Memo Writer and claim validator on Replay/Stub; Register entries Q1, Q2, Q4, Q5, Q6 with the synthetic committee; pack v0 with W1, archetypes and the Ask hand-off; the analyst thin slice (WP-39). Computed seats arrive in v1. Exit: the six MVP questions answered end to end with their listed artifacts and metric ids (§9.4 #4); pinned-dual suites 8/8 and 18/18 and the must-fix pins green; identities exact; the increment-1 blocking V-gates green (§6.9); performance assertions green; sprint-1 production H benchmark passed; the analyst golden set green on Stub; 100% labelling audit.

### 9.4 End-to-end demo acceptance test (`tests/e2e/test_quarter_demo.py`)

Command: `C:\users\dean\ai_envs\adic_tpa_lab\.venv\Scripts\python.exe -m adic_tpa run quarter --asof 2026-10-18 --synthetic --offline --no-campaign` (increment 1); v1 adds the same with `--campaign` on Stub and on Replay cassettes.

| # | Acceptance criterion |
|---|---|
| 1 | Exit code 0 in ≤ 30 minutes on the reference laptop, with every B12 stage inside its budget (§10.1) |
| 2 | Produces `runs/2026Q4/pack/index.html`, `pack_manifest.json` and `decision_log.jsonl`; `tpa audit chain` verifies the registry and the decision log |
| 3 | L0 has all nine blocks; briefs for Q1, Q2, Q4, Q5 and Q6 render with no EVIDENCE MISSING (a negative variant deletes one metric and must show "EVIDENCE MISSING: <metric>") |
| 4 | The six MVP questions (SYN §10) are answered, each by the artifacts and metric ids that `tests/e2e/mvp_questions.yaml` lists and the test resolves in the registry (BUILD-27): (1) Phase-I status, the `phase1_card` artifact with u*, d₀, IIS and glide path for R0x–R2; (2) survival, the `stress_report` and `cfp_reading` artifacts (T4′ survival months by tier, readiness and event stages) under T4′ and the reverse stresses, labelled reverse and never priced; (3) the λ curve, the `kernel` and `ftp_curves` artifacts (decision FTP by tenor with bands, λ^spot by regime); (4) the top-20 `decision_card` artifacts by group with envelopes, `priced_on` and Γ status; (5) the `tier1_board` artifact with model ranges and the priced ε_R frontier, Mix A vs Mix B (e.g. `tier1.t6.cp_upper@v1` by class); (6) the `bridge_card` artifacts by world |
| 5 | Every number has a resolving `data-ref`; claim coverage = 1; no literal digits outside placeholders in any narrative |
| 6 | Labelling audit 100%; the SYNTHETIC footer in every section; the decision census and side-by-side census stated on L0 (S-ADR-03) |
| 7 | The contract mode is computed at G0 (NORMAL, EXECUTION_RECOVERY or STRUCTURAL_RECOVERY), never asserted, and every card's `priced_on` agrees with it |
| 8 | The pinned-dual suites and the must-fix pins pass in the same CI run |
| 9 | A second run with the same seed reproduces every artifact's canonical hash bit for bit (`contracts.hashing.canonical_artifact_hash`, which normalizes run ids, datetimes and chain hashes, the declared `VOLATILE_FIELDS`); array and cube checksums are compared raw (BUILD-27) |
| 10 | No process other than `tpa lab`/gateway makes a non-loopback connection: the fixture patches `socket.connect`, `sendto` and DNS resolution to fail for non-loopback addresses and allows loopback socket pairs (one Windows ProactorEventLoop, which the MCP stdio layer uses, opens three AF_INET loopback sockets); the run works with networking disabled (BUILD-27) |
| 11 | The run is in DEV_SYNTHETIC mode, says so on L0 and reaches CLOSED unattended on one Windows account (software seal, test signer, synthetic committee); the same command with `run_mode = REAL` refuses all three (S-ADR-37) |
| 12 | The analyst golden set passes on Stub against this run's quarter (S-ADR-34) |

---

## 10. Performance and test plan

### 10.1 Benchmarks (asserted nightly in `tests/perf/`; reference laptop Core Ultra 9 285HX, idle; loaded-machine numbers are 3–4.5× pessimistic, JE §5.1)

| ID | Workload | Target | Evidence / owner |
|---|---|---|---|
| B1 | P: 10,000 paths × 40 quarters, asset level, policy in the loop (v2 book) | ≤ 60 s; design ≈ 36 s = the nine component lines below, each asserted by `tests/perf/test_b1_profile.py` | PD 10.9 s on 1 process [M]; WP-17 |
| B2 | Quarterly H: Phase I-a, assembly, Phase II on 5 replications, ranging, Level B with ≤ 4 re-solves, ≤ 10 finite-difference rows and ≤ 20 forced re-solves on the selected replication | ≤ 120 s wall clock; per-step budgets in §5.14 (≈ 113 s) | §5.14; WP-18 (benchmark), WP-33 (production) |
| B3 | Level-B MILP | ≤ 10 s | WP-19 |
| B4 | W1 entropy pooling in the browser (10k paths, ≤ 20 views) | < 1 s | in-browser self-test timing; CI checks ≤ 50 Newton iterations on the golden cases; WP-28 |
| B5 | Certification, 50k paths per world | ≤ 60 s per world on 4 processes including process start-up (5 × 36 s ÷ 4 ≈ 45 s); 7 final worlds ≤ 7 min | PD 16.8 s per world [M]; WP-17/34 |
| B6 | W2 what-if (400 × 8 on cached paths; FBE views by first-order coefficient adjustment, A22) | ≤ 60 s | WP-18/33 |
| B7 | Nightly batch (P on all worlds, sign-off tree with full finite-difference dual verification, bands, robustness, pack); the group Shapley game is a weekly job (≈ 21 core-hours, ≈ 1 h on 22 cores) | < 1 hour | WP-30/33/36 |
| B8 | Lab campaign | ≈ 16 core-hours (races ≈ 9, confirmations ≈ 7; §7.7) within the 20 core-hour budget | WP-26/38 |
| B9 | Cube generation with tabulated inverse CDFs | ≤ 2.5 s per 10,000 paths × 120 months | WP-06 |
| B10 | Tree build (12,000 pooled paths → 576 leaves, incl. group-rate recording over the tree's 12 quarters) | ≤ 30 s | WP-18 |
| B11 | Phase I-a, all four consent scenarios | ≤ 5 s | WP-18 |
| B12 | End-to-end offline quarter, increment 1 (§9.4) | ≤ 30 min, by stage (table below) | WP-30 |
| B13 | θ* recalibration (10 × 50k pooled paths; annual, or on a census, allocation or book change) | ≤ 5 min | WP-13 |
| B14 | Synthetic release build and V-gates incl. V16–V18 (a release job outside B12) | ≤ 30 min | WP-15 |
| B15 | Column construction for the catalogue | ≤ 3 min | WP-16 |
| B16 | Replication selection in P (2,000-path race per world; 10,000 on a near tie) | ≤ 60 s on 4 processes | WP-20 |
| B17 | Buffer and λ^H_T calibration (≤ 4 warm iterations) | ≤ 5 min | WP-20 |
| B18 | Analyst latency | cached answer ≤ 5 s; W1 < 1 s; W2 ≤ 60 s with progress and cancel; W3 handle ≤ 2 s | WP-39/40 |

**B1 component lines** (seconds per 10,000 paths × 40 quarters on one process; S-ADR-38; v1.0's lines summed to 95–125 s before HF, overlay and policy, mostly from a full stress replica every quarter and one-lane RNG; QUANT-12, BUILD-05):

| Line | Budget (s) | Module |
|---|---|---|
| Scenario cube (B9) | 2.5 | scen |
| RNG (four-lane Philox, keys cached per block; ≤ 0.02 s per 2,000-path block-quarter) | 4 | rng |
| Private engines | 12 | priv |
| Public Markets (HF machine, long-only, queues) | 3 | pub |
| Overlay (monthly revaluation, VM by CSA, SIMM-like IM) | 5 | overlay |
| Ledger and recourse | 2 | ledger |
| Readiness reading and CFP (linear response; full replica on band exits) | 4 | ledger |
| Policy and observables | 2 | core.sim |
| Metrics | 1 | core.sim |
| **Total** | **35.5** | |

**B12 stages** (increment 1; synthetic, offline, campaign off; BUILD-07):

| Stage | Budget |
|---|---|
| Snapshot freeze, initial state and FBE-R on the pre-built R0 release (B14 builds it) | 2 min |
| Cubes for M1, M6 and B1 with owner draws (B9) | 1 min |
| Phase I-a and recovery mode (B11) | 0.1 min |
| Group rates and tree (B10) | 0.5 min |
| Column construction (B15) | 3 min |
| H at the what-if preset on 5 replications, selection, Γ, dual checks | 2 min |
| Replication selection in P (B16) | 1 min |
| Buffer calibration (B17) | 5 min |
| Certification of C_H on M1, M6 and B1 at 50k paths (B5) | 3 min |
| Sealed run: ≤ 2 finalists × fresh M1/M6 seeds at 50k paths | 4 min |
| Controls and archetypes: 12 policies × 3 worlds at the 2,000-path race count | 2 min |
| Bridge, robustness and MVP attribution | 1 min |
| Memo on Stub/Replay, rendering, validation and pack build | 2 min |
| Room: Register, briefs, synthetic committee, decision log | 1 min |
| **Total** | **≈ 28 min** |

Computed seats (v1) evaluate `implied_actions` by re-weighting cached paths and get their own line in v1's B12; V16–V18 run in B14, never in B12.

A benchmark more than 10% over target fails the nightly; regressions over 20% between nightlies are flagged even under target.

### 10.2 CI suites

| Suite | Trigger | Content | Budget |
|---|---|---|---|
| `pr` (`pytest -m "not slow and not perf"`) | every change | the walking skeleton; unit, property (hypothesis `max_examples=100`), metamorphic, regression on fixtures, reconciliation on fixture trees, solver on fixture LPs, drills, room, labelling, layering and allowlist; the analyst golden set on Stub (140 items) and access drills | ≤ 15 min |
| `nightly` | daily | everything in `pr` + perf B1–B7, B9–B18 with the B1 and B2 profiles; default and sign-off trees with full finite-difference dual verification; the A8 power-cone reference; statistical suites; recovery with reduced worlds (200); determinism at 1/4/8 workers; HiGHS–CLARABEL agreement; golden-manifest reproduction by canonical hash; the e2e demo; the analyst on Replay with CLI–MCP parity | ≤ 3 h |
| `weekly` | weekly | full recovery suites (2,000 worlds); overnight tree; G-A–G-E; the group Shapley game (32 permutations); lab calibration campaign (v1); admission tests on cassettes; scheduled cassette re-recording | ≤ 12 h |

### 10.3 Coverage expectations

coverage.py is not installed, so `tools/coverage_lite.py` (WP-03) collects line coverage with Python 3.12's `sys.monitoring` LINE events during the `pr` suite. Targets: ≥ 85% of lines in every engine package; ≥ 90% in `contracts`, `ledger`, `core.phase1`, `core.phase2`, `core.duals`, `claims.validator`, `evaluator.gates` and `seal`; 100% of public functions (names in each module's `__all__`) called by at least one test (checked by the same tool). Coverage is reported per WP in the CI summary; falling below target fails the WP's DoD.

### 10.4 Golden files

| Golden | Location | Producer |
|---|---|---|
| Frozen fixtures (mini book v1/v2, mini cube, mini FlowCube, fixture tree) | `tests/golden/frozen_fixtures.json` | WP-03 |
| Research ports (read-only copies + SHA-256): `hf_ladder.py` results; `t1_engine.ladder` readings; the gap_02 G*(θ) grid and per-model gap quantiles (`gap02_results.json`, BUILD-36); gap_02 coefficient export and expected outcomes; G-gap_01 coefficient export and expected outcomes; `perf_module.py` golden cases; `bridge.py` verifier-10 figures; `v8_rerun` replica rows; SIMM worked example; `sealed_pe_history_v1_1.csv` | `tests/regression/fixtures/<source>/` | WP-03 (`tools/port_research.py`) |
| Golden manifests: (1) MVP offline quarter; (2) H what-if solve on the fixture tree; (3) certification on the mini world | `tests/golden/manifests/` | WP-30, WP-18, WP-17 |
| EP golden cases | inside the pack payload and `tests/golden/ep_cases.json` | WP-28 |
| Pack structure snapshot (section ids, block order; not bytes) | `tests/golden/pack_structure.json` | WP-28 |

Updating a golden requires `pytest --update-golden`, a contract-change note naming the reason, and review by the module owner and MRM.

### 10.5 Tolerance policy for reproducibility

| Situation | Rule |
|---|---|
| Same machine, pinned versions, recorded thread settings | **Bit for bit**: cube checksums, path metrics, single-threaded HiGHS solutions and duals, and registry artifacts compared by canonical artifact hash (volatile fields normalized, §4.1); text files hashed with LF line endings, so checkouts with different `core.autocrlf` agree (S-ADR-42) |
| Different machine or BLAS build | identities ≤ 1e-10 $bn; LP objective ≤ 1e-9 relative; duals ≤ 1e-7 relative on non-degenerate rows (degenerate rows compared by overlap of ranging intervals); Monte Carlo metrics identical because Philox draws are pure functions — a numba/numpy upgrade that changes floating-point results is re-baselined through the golden-update path with differences ≤ 1e-6 relative on aggregates |
| Statistical tests | fixed seeds; every tolerance with sampling error states its basis (e.g., ± 2 SE, CP 95%) |
| Multi-threaded IPM | never used in evaluator solves; allowed only in exploratory benchmarks, labelled |

### 10.6 Test inventory by family (named suites; ARCH §10.7)

| Family | Directory | Named suites (acceptance as in §4–§5) |
|---|---|---|
| Unit | `tests/unit/` | engine equations; pricers vs closed forms and put–call parity; VM by CSA; WIS/CRPS; Benktander; EP dual; perf 17/17; hashing; contract validators; dual sign toy |
| Property | `tests/property/` | ledger identity; NAV ≥ 0; homogeneity; dual signs; envelopes within slack; netting = 0; DSL rejects look-ahead and horizon variables |
| Metamorphic | `tests/metamorphic/` | wider discount ⇒ no more discretionary SELL when slack; costlier facility ⇒ no more REFI; tighter band ⇒ smaller feasible set; NAV scaling and relabelling; relabelling a sale reason leaves P(red) unchanged; converting a non-red resource into cash leaves H3 unchanged; a zero-NPV refinancing and a cost-neutral financing round trip change the objective only by the PWL error; penalties ×10 leave duals unchanged; a dominated option leaves the recommendation unchanged; filter no-look-ahead |
| Regression | `tests/regression/` | `test_no_pinned_duals` (8/8); `test_no_pinned_duals_groups` (18/18); `test_kkt_cap_cheapest_spare_lever`; `test_v8_replica`; bridge vs verifier 10; gap_01 group table and census cash map to $0.01bn; hf_ladder, t1_engine, bridge ports; SIMM example; sealed v1.1 history (fixture hash + $0.01bn reproduction) |
| Must-fix pins | `tests/regression/must_fix/` | `test_binding_world_priced`; `test_no_world_identity_in_nodes`; `test_t6_surrogate_guard`; `test_readiness_red_never_fires_red_playbook`; `test_recovery_envelopes_sum_and_glide_shares`; `test_no_payout_lever_in_mode_B`; `test_phase1_reports_all_consent_scenarios`; `test_ni_comparator_restored_in_recovery`; `test_seat_numbers_only_from_implied_actions`; `test_no_named_person_regret_in_pack`; `test_credibility_hidden_below_neff_20`; `test_no_league_table`; `test_no_indicator_terms`; `test_lever_equals_add_plus_refi` |
| Reconciliation | `tests/reconciliation/` | H vs P replay ≤ 1%; unreduced-tree identity 1e-9 on quarterly and semiannual fixtures with fixed SELLs; recourse protocol (a sold unit's flows stop; H and P agree on the first red month); A1 clock on ≥ 20,000 CRN paths; cohort vs asset (A2, only if cohorting is enabled); DVA sums; services ledger nets to zero on DVA ledgers and entity P&Ls sum to external P&L |
| Solver | `tests/solver/` | dual intervals (ranging; finite differences on the capped set); penalty invariance; HiGHS–CLARABEL agreement; Γ ≥ 0 on exact utility; the A8 decision test; the kernel two-node test; Phase-I closed forms; H–P Kendall τ ≥ 0.8; cvxpy reference cross-check; extended pinned-dual test |
| Skeleton | `tests/skeleton/` | the Wave-0 walking skeleton (WP-03) |
| Analyst | `tests/analyst/` | golden set on Stub and Replay; access, read-only and confirmation drills; CLI–MCP parity (WP-39/40) |
| Statistical | `tests/statistical/` | CP coverage; paired-bootstrap calibration; Holm and α-investing on synthetic nulls; uniformity of the RNG |
| Recovery | `tests/recovery/` | SBC; ±5pp recovery for FBE-R, regime filters, owner model and census pace under every truth variant; G-A–G-E |
| Overlay | `tests/overlay/` | T1–T6 (T4 licensed-SIMM reconciliation is a production item) |
| Determinism | `tests/determinism/` | same checksums and duals at 1, 4, 8 workers; draws outside kernels; block-size invariance |
| Layering and packaging | `tests/layering/` | import table (§4.0); allowlist; no hard-coded group ids; engines never import agents or networking |
| Drills | `tests/drills/` | §7.13 |
| Room | `tests/room/` | §8.9; JS = Python EP on golden cases |
| Labelling | `tests/labelling/` | 100% audit of `is_synthetic`, `data_class`, footers, taint |
| Performance | `tests/perf/` | B1–B18, with the B1 and B2 profiles per line |
| End to end | `tests/e2e/` | §9.4 |

**Owners of cross-module tests** (S-ADR-42; BUILD-26). Reconciliation: H identity and replay → WP-18; A1 and H–P agreement → WP-17; the recourse protocol (ledger–engine) → WP-13; services and DVA netting → WP-20. Must-fix pins: the WP of the module each pins, named in the file header. The walking skeleton → WP-03; the e2e demo → WP-30; each B1 and B2 profile line → the WP owning the module on that line.

---

## 11. Traceability

| ARCH section / ADR | Implemented in (modules) | Verified by (tests / gates) |
|---|---|---|
| §0.3 rule 1, ADR-02 one ledger kernel for P, H, T4′ | `ledger` (kernel, linear, stress), `core.sim`, `core.h` | unreduced-tree identity 1e-9; H–P replay ≤ 1%; t1_engine port |
| §0.3 rule 2, ADR-07 one price λ from KKT | `core.duals`, `core.kernel`, `icm` | dual sign toy; μ − M > 0; KKT-cap test; dual-quality intervals |
| §0.3 rule 3, ADR-04 every banded world in H on a pooled-observable tree | `core.tree`, `core.h` (H4 per class) | `test_binding_world_priced`; `test_no_world_identity_in_nodes`; A17 |
| §0.3 rule 4, ADR-10, ADR-11 safety first; T6 bands by class | `core.h` (H3–H5), `core.certify`, `core.phase1` | CP certification; `test_t6_surrogate_guard`; Gate 1(c) |
| §0.3 rule 5, ADR-09 owner draw exogenous | `owner`, `core.dsl` (TR8), `contracts` validators | `test_no_payout_lever_in_mode_B`; Mode-B API test |
| §0.3 rule 6, ADR-08 readiness-Red ≠ event-Red | `ledger.cfp` | `test_readiness_red_never_fires_red_playbook`; CFPReading validator |
| §0.3 rule 7, ADR-19 integrity by infrastructure | `evaluator`, `seal`, `registry`, `claims` | drills §7.13; chain verification |
| §0.3 rule 8, ADR-21 humans own contract and vote; computed seats | `contracts.SignOff`, `idm.seats`, `idm.ballots` | `test_seat_numbers_only_from_implied_actions`; recusal tally test |
| §0.3 rule 9, ADR-15 offline first, determinism | `agents.backends`, `rng`, `core.solver` | offline e2e; Replay fail-closed; determinism suite |
| §0.3 rule 10 synthetic labelled, sealed truth, recovery | `synth`, `data.taint`, `pack.lint_pack` | labelling audit 100%; V16–V18; truth-store layering test |
| §3.4 package layout and ownership | §2 tree; §9.2 WPs | layering test |
| §3.5 frozen interfaces | `contracts.ports`, §4 signatures | Protocol conformance tests (WP-03) |
| §3.6 quarterly data flow | `pipeline`, `lab.fsm`, `idm` | e2e demo; FSM tests |
| §4.0 time grid, meaning of 10% | `contracts.calendar`, `core.sim.j_value`, `bridge` | J neutrality identity; calendar tests |
| §4.1 scen; ADR-16 second families | `scen` (E, B1, B2) | anchor ≤ 5bp; B2 final-only; embargo test |
| §4.2 state, F_t | `state` | F_t and e₀ regressions; no-look-ahead |
| §4.3 owner | `owner` | kinks; draw band; recovery |
| §4.4 private engines; ADR-14 clock | `priv` | stylized facts V3–V13; V24a; A1 |
| §4.5 Public Markets | `pub` | hf_ladder port |
| §4.6 overlay; ADR-13 | `overlay` | T1–T6; SIMM example; reconciled S1 use |
| §4.7 beliefs; ADR-24 FBE-R + fourth mark | `beliefs` | SBC; G-A–G-E; perf 17/17 |
| §4.8 actions; REFINANCE/LEVER semantics | `actions`, `contracts.LensAction` | `test_lever_equals_add_plus_refi`; worked values |
| §4.9 ledger, ladder, T4′, CFP | `ledger` | ports; θ* rule; LR8 |
| §4.10 leverage; ADR-35 NAV facility demoted | `ledger.leverage`, `ledger.facilities`, `synth` facility table | facility credit tests; R1-only revolver pricing |
| §4.11 bridge | `bridge` | verifier-10 regression |
| §4.12 robust; no DRO in H | `robust` | EP exactness; no-stacking test |
| §4.13 attribution | `attrib`, `core.irb` | Shapley efficiency; v8 replica; null control |
| §5.2 objective and tiers; ADR-10 | `core.h` objective, `core.sim.j_value`, `core.dsl` linter | `test_no_indicator_terms`; tolerance-cascade checks in Gate 2 |
| §5.4 H; ADR-03, ADR-05 | `core.tree`, `core.h`, `core.solver` | §5.14 B2, sizes, presets |
| §5.5 Phase I, consent scenarios; ADR-06 | `core.phase1`, `core.phase2` | pinned-dual suites; `test_phase1_reports_all_consent_scenarios` |
| §5.6 duals, kernel, λ | `core.duals`, `core.kernel` | dual-quality tests; KKT cap |
| §5.7 selection, Γ | `core.colgen`, `core.levelb` | Γ ≥ 0; brute-force check; forced re-solves |
| §5.8 module F; ADR-32 | `core.safety` | zero violations; `tier1_override_needed` |
| §5.9 MPC loop | `core.mpc` | MPC e2e on the v2 book |
| §5.10 P0, controls, archetypes; ADR-26 | `core.policy` | archetype behaviour tests; F projection labels |
| §5.11 DSL; ADR-18 | `core.dsl` | TR1–TR8 drills; identity at zero |
| §5.12 terminal values | `core.terminal` | horizon invariance; out-of-sample R² |
| §5.13 error ledger A1–A18 and consistency contract | `core.*`, `overlay`, `robust`, `pack` | A-row tests listed in §5.14 and §10.6 |
| §6.1–6.3 FTP, envelopes, requests; ADR-29 | `icm` | EWMA/collar; ranging-only requests; appetite vs tolerance nightly |
| §6.4 recovery envelopes and delivery shares | `icm.recovery`, `icm.delivery_shares` | `test_recovery_envelopes_sum_and_glide_shares` |
| §6.5 pacing and c^PACE | `icm.pacing`, `core.policy` | c^PACE regression; 2-quarter credit lag (S-ADR-20) |
| §6.6 in-house desks and conflict controls | `data` (quote conflict flag), `beliefs.market_implied`, `idm.politics` | conflicted-quote second-source test |
| §6.7 contingent budgets; ADR-28 | `icm.contingent` | gate truth table |
| §6.8 internal transfers and services | `icm.transfers`, `icm.services`, `overlay.services` | V2 on DVA ledgers; services netting |
| §6.9 charges, DVA, pay, disputes | `icm.charges`, `icm.dva`, `idm.politics` | DVA sums; visibility test |
| §7.1–7.4 lab mechanisms, processes, roles, tools | `lab`, `agents`, `evaluator` | FSM tests; tool schema strictness; firewall tests |
| §7.5 planes; ADR-16 | `evaluator.planes`, `seal`, `scen` | final-store drill; HMAC seeds; world-list hash |
| §7.6 gates and failure taxonomy | `evaluator.gates`, `evaluator.failures` | gate unit tests; `test_ni_comparator_restored_in_recovery` |
| §7.7 budgets and deflation | `lab.budgets`, `stats` | over-budget drill; DSR/PBO tests |
| §7.8 memory; ADR-33 | `lab.memory` | memory closes at SELECTION; `test_memo_cannot_cite_memory` |
| §7.9 escalation and assumptions | `lab.escalation` | escalation drill |
| §7.10 cross-family review; ADR-30 | `agents`, `config/llm/roles.yaml` | correlated-label test; admission tests |
| §7.11 drills | `tests/drills/` | each drill |
| §7.12 planted-effect calibration | `lab.calibration` | WP-38 DoD |
| §7.13 offline mode | `agents.backends` | Replay fail-closed; offline e2e |
| §8.1 decision rights | `idm.ballots`, `idm.protocol`, `contracts` tiers | recusal; irreversibility check; tier routing tests |
| §8.2 Decision Register; ADR-22 | `idm.register`, `idm.compiler` | every entry renders; EVIDENCE MISSING |
| §8.4 pack | `pack` | §8.8–8.9 |
| §8.5 shadow IC | `idm.seats` | seat-numbers test; diversity alarm; minority triggers |
| §8.6 human meeting | `idm.protocol`, `idm.consent`, `idm.evsi` | pre-vote immutability; DEFER rule test |
| §8.7 Q&A, what-ifs; ADR-23 | `pack/static/ep.js`, `robust.ep`, `core.h` (W2) | JS = Python; Python recomputation of logged W1 numbers |
| §8.9 decision log and signposts | `idm.decision_log`, `idm.signposts` | chain verification; signpost root-finding test |
| §8.10 politics rules | `idm.politics`, `pack.lint_pack` | league-table, n_eff, named-regret tests |
| §8.11 evaluating the room | WP-35 suites | hidden-profile decision accuracy baseline |
| §9.1–9.3 data hierarchy, tables, marks | `contracts`, `data` | schema tests; bitemporal property tests |
| §9.4–9.5 SYN-ADIC-177; ADR-25 | `synth` | V1–V24; census rule (S-ADR-03) |
| §9.6 adapters | `data.adapters` (WP-37) | contract tests; quarantine |
| §9.7 confidentiality | `agents.gateway` | redaction test |
| §10.1 AnalysisContract | `contracts.contract` | validator tests |
| §10.2 manifests | `registry`, `contracts.hashing` | golden manifests bit for bit |
| §10.3 metric registry | `registry.metrics` | definition-change test |
| §10.4 evaluator contracts | `contracts.evidence`, `evaluator` | agent-view minimality |
| §10.5 controls, null, ablations | `core.policy`, `attrib.null_control`, `evaluator` (no tuning for ablations) | null identity; ablation refusal test |
| §10.6 claims and provenance; ADR-20 | `claims` | validator drills; provenance DAG test |
| §11.1–11.3 offline, LLM config, MCP | `agents`, `mcp_server` | offline e2e; server tests |
| §11.4 CLI | `cli` | command smoke tests |
| §11.5 budgets | `tests/perf/` | B1–B12 |
| §11.6 increments; ADR-34 | §9 waves | wave gates |
| §11.8 package policy; ADR-27 | allowlist test | `tpa audit allowlist` |
| ADR-01 layered composite | whole layout | — |
| ADR-12 liquidity margin as T3 option, diagnostic, ratio | `ledger` (`t3_vm_stat`), `overlay` (stress-coverage ratio) | T3 statistic switch test |
| ADR-17 two workers | `contracts.BudgetSpec.workers`, `lab` | FSM with 2 and 4 workers |
| ADR-31 comparator in recovery | `evaluator.gates` | `test_ni_comparator_restored_in_recovery` |
| ADR-36 deferred / rejected | not built (SDDP, neural surrogates, DRO in H, payout as decision, MILP in tree) | linters (`test_no_indicator_terms`, TR8) |
| S-ADR-01, -22 taxonomy as config; 13 seats | `contracts.taxonomy`, `idm.seats`, `attrib.group_shapley` | `test_no_hardcoded_group_ids`; seat count = n_groups + 5 |
| S-ADR-02 Real Assets interim | `priv.realassets`, `pub.queue`, `synth.realassets`, `actions` library | RA tests (§4.11); VR1–VR3 |
| S-ADR-03 allocation and census rule | `synth.census`, `synth.decision_census`, `pack` L0 | census-rule test; L0 disclosure (e2e #6) |
| S-ADR-05, -30 red event by economic substance | `ledger.redtest`, `ledger.recourse`, `core.sim` | `test_red_test_substance`; relabelling metamorphic test and drill |
| S-ADR-06, -31 objective refinements; Tier-1B floor | `contracts.ObjectiveSpec`, `contracts.FloorSpec`, `core.h`, `core.certify` | shortfall-exponent validator; forward 10-year floor and class-band tests; the SYN §4.9 14.3%-vol regression |
| S-ADR-07 T6 surrogate variants, bPOE, RFY | `core.h`, `stats.bpoe`, `core.sim.gambling_signatures` | WP-33 experiment; bPOE properties |
| S-ADR-08 robustness refinements | `robust.persistence`, `robust.frontier` | persistence weights; frontier test |
| S-ADR-09 optimization refinements | `core.tree` (forward filtration), `core.irb`, `core.dsl` (hinge) | A4 A/B; IRB property |
| S-ADR-10, -11, -27 FBE, the marks archive and group priors | `beliefs`, `config/beliefs`, `config/groups`, `data.adapters.marks_archive` | equal-weight default and horizon-cap tests; IRR/MOIC translation round trip; archive contract test; prior config tests |
| S-ADR-12, -32 facilities, financing window, θ* and conventions | `scen` (fin_window), `ledger.facilities`, `ledger.stress`, `actions` (tightening premium) | availability cap test; θ* grid test; pricing-conventions test; research sensitivity row |
| S-ADR-13 recourse waterfall | `core.policy`, `ledger.recourse` | liquid-first/cash-last/pro-rata ablation controls run; `RecourseOrder` has no preemptive rung |
| S-ADR-14 owner band (Mode H) | `owner.modes` | band acceptance test (OWNER_PROPOSAL only) |
| S-ADR-15 overlay refinements | `overlay`, `attrib.cash_buffer_test`, `core.dsl` (`ltp_pctile`) | VM-delay T3 test; Gamba–Triantis test |
| S-ADR-16 ICM refinements | `icm` | λ decomposition sums to ℓ; risk charges from CVaR duals; envelope collar |
| S-ADR-18 lab refinements | `seal.canary`, `registry.mfdr`, admission tests | canary drill; mFDR control |
| S-ADR-19 synthetic data refinements | `synth.releases` | pre-registration hashes |
| S-ADR-20 pacing refinements | `ledger.linear`, `core.policy`, `attrib.corridor_option_value` | 2-quarter lag test; commitment-inclusive leverage metric |
| S-ADR-21 provisional numbers | test design | no test pins G4 wipe-out / LTV-breach values |
| S-ADR-23 Anthropic call surface | `agents.backends.anthropic_backend` | recorded cassette; refusal path test |
| S-ADR-24 composition root | `pipeline`, `contracts.ports.RoomPort` | layering test |
| S-ADR-25, -38 seeds and four-lane keys | `rng` | Philox equivalence; spawn-tree test; sampler-table test |
| S-ADR-26 calendar | `contracts.calendar` | calendar tests |
| S-ADR-28; ARCH ADR-40 belief draws per world | `beliefs.draws`, `contracts.BeliefDraws`, `priv`, `pub` | `test_engine_mean_log_return_by_world`; `test_draws_per_world`; the 7.7% stylized-fact gate |
| S-ADR-29; ARCH ADR-41 interfaces and the recourse protocol | `contracts.ports`, `ledger.recourse`, engines, `core.sim`, `core.h`, `core.select`, `icm` | walking skeleton; `test_recourse_protocol`; `test_recourse_sold_unit_flows_zero` |
| S-ADR-33; ARCH ADR-42 H accounting | `core.h`, `ledger.linear`, `actions` | identity tests (fixed SELLs; semiannual); H3 and cost-neutrality metamorphic tests; kernel two-node test; `test_h_size` |
| S-ADR-34; ARCH ADR-44 conversational analyst | `analyst`, `contracts.analyst`, `mcp_server`, `cli` | golden set; access, read-only and confirmation drills; CLI–MCP parity |
| S-ADR-35; ARCH ADR-45 market data and the factor set | `scen`, `state`, `data_public` | anchor, vol and correlation checks; shock-matrix test; filter reproduction; provenance flags |
| S-ADR-36; ARCH ADR-46 LLM draft models | `contracts` (§3.16), `agents`, `claims`, `pack.lint_pack` | `test_llm_schemas_transform`; LLM_NUMBER_RENDERED drill; pack linter |
| S-ADR-37; ARCH ADR-47 increment-1 fidelity and DEV/SYNTHETIC mode | `pipeline`, `seal`, `testing.committee`, `contracts.signing` | e2e #11; `test_dev_mode_refused_in_real` |
| S-ADR-38; ARCH ADR-48 performance budgets | `tests/perf/` | B1 and B2 profiles; B12 stage budgets |
| S-ADR-39 JSON-mode validation | `contracts.config` | `test_config_roundtrip` |
| S-ADR-40 signatures | `contracts.signing`, `idm` | `test_signing` |
| S-ADR-41 Replay keys; fixed tool lists | `agents.backends.replay`, `lab.firewall` | Replay drift test; firewall tests |
| S-ADR-42 build hygiene | layout, `contracts.hashing`, `registry.metrics` | LF hash test; duplicate metric-id check; worker picklability |
| S-ADR-43 misspecification overrides | `core.factory`, `contracts.MisspecOverride` | `test_factory_overrides` |
| S-ADR-44 outer calibration loop | `core.mpc.calibrate_buffers` | convergence test; B17 |
| ARCH ADR-37 to ADR-39, ADR-43, ADR-49 | see S-ADR-31, -32, -30, -27; `actions` (additive LEVER) | as above; `test_lever_additive_rule` |

---

## 12. Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-18 | First issue (design workflow, stage 3b) |
| 1.1 | 2026-10-18 | Revised against `design/reviews/critique_quant.md` (QUANT-01 to QUANT-34) and `design/reviews/critique_build.md` (BUILD-01 to BUILD-41). First pass: S-ADR-27 to S-ADR-44 (§0.3) and the contracts (§1–§3). Second pass, completing the revision: every module entry (§4.2–§4.34) brought into line with those S-ADRs, the new §4.35 `analyst` (reconciled with `design/addenda/CHAT_ANALYST.md` v1.0, which appeared after the critiques), the H accounting of §5 (≈194k columns × 186k rows), §6 (IRR/MOIC observation layer, blocking-gate policy), §7 (draft models, two-tier Replay, evaluation-kind table), §8 (W1 gates, Ask hand-off), §9 (41 work packages, restored increment 1, operational e2e criteria), §10 (benchmarks as sums of tested lines) and §11. One research figure was added: the class-banded θ\* is ≈ 0.58 on the research fixture (`gap02_results.json`). Every disposition is in `design/reviews/revision_log.md` |

*SYNTHETIC – NOT ADIC DATA (every balance, probability, price, horizon, timing and count in this document).*
