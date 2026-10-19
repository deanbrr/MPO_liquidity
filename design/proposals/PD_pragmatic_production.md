# Proposal PD: Pragmatic production path

**Angle:** what a small quant team can build, test and operate on a Windows laptop (Python 3.12, HiGHS/CLARABEL, offline-first), in increments, meeting R1–R15 and P1–P15. **Date:** 2026-10-18.

> **SYNTHETIC – NOT ADIC DATA.** Every balance, probability, price and timing below is computed on the synthetic working book (context §1A, census v1.0) or on a synthetic benchmark structure. None of it is ADIC data.

**Citation key.** `Brief` = design/00_DESIGN_BRIEF.md; `00_SYNTHESIS` = research/00_SYNTHESIS.md; `GROUPS` = research/groups/01_GROUPS_SYNTHESIS.md; `gap_0x` = research/addenda/gap_0x.md; `GROUPS gap_0x` = research/groups/addenda/gap_0x.md; `Paper l.` = paper line as quoted in Brief §2. **[PD-bench]** = timings measured for this proposal on the target laptop (Core Ultra 9 285HX, 24 cores, 95.5 GB), single-threaded unless stated, with other workloads running, so conservative. Scripts are in the session scratchpad (`...\scratchpad\pd_bench\bench_lp.py`, `bench_warm.py`, `bench_clarabel.py`, `bench_sim.py`); increment 1 re-homes them as `tests/perf/`.

---

## 1. Thesis

**Ship a ledger, not an oracle.** The organizing idea is one deterministic liquidity-and-collateral **ledger kernel**. Every engine feeds it through one typed flow contract, and it is used three ways:
- **Forward on 10,000–50,000 paths**, it is the policy simulator P, which produces probabilities and Tier-1 certificates.
- **Linearized on a reduced scenario tree**, it is the here-and-now LP H. H's Phase-II duals give λ, Corporate Finance's FTP curve and the group envelopes.
- **On the canonical stress s\*(θ\*)**, it gives T4′ survival and the CFP stage.

P, H and the stress test share ledger rows, the scenario cube (common random numbers) and the action catalogue, so they reconcile through identity tests, and real data enters only through adapters that emit the same contracts. Beliefs, the overlay, agents and the IC pack plug in behind typed interfaces; agents can only submit typed specs to an out-of-process, content-hashed evaluator.

The design is sized to the laptop by measurement:
- asset-level simulation of the ≈390-unit synthetic book runs 10,000 paths × 40 quarters in **10.9 s** on one core;
- the default 600-leaf × 12-quarter LP solves in **32 s** with HiGHS dual simplex [PD-bench].

Headroom is spent on fidelity and replications, not on solvers the environment lacks. Increment 1 runs a thin end-to-end SYNTHETIC slice; v1 and v2 deepen modules behind unchanged interfaces.

---

## 2. Requirements and principles trace

**Requirements.**

| R | Where | How |
|---|---|---|
| R1 multi-period | `core.sim` (P), `core.h` (H) | 40-quarter policy simulation; 12-quarter LP re-solved quarterly (MPC); parametric policy search (§4.11) |
| R2 robust scenarios | `scen`, `robust` | Six-model ensemble plus bootstrap families (00_SYNTHESIS §4.1); KL/W∞, k_MS, reverse stress; search, final and misspecification planes |
| R3 probabilities | `core.certify`, `ic` | Every probability shows mixture value, model range, Monte Carlo error and scenario hash; gates use Clopper–Pearson bounds (00_SYNTHESIS §6.7) |
| R4 5–10% payout | `owner`, `ledger` | Stochastic owner draw on an opening-NAV basis; rows T1 and T7; mandate switch A/B/H (00_SYNTHESIS §4.7) |
| R5 10% target | §4.1, `bridge` | Defined as a 10-year geometric TWR; what-you-need-to-believe (WYNTB) bridge per model; P(10%) reported, never optimized (gap_05) |
| R6 leverage | `ledger`, `core.h` | Facilities as Corporate Finance variables in H; asset-level LEVER columns; limits in T5 (00_SYNTHESIS §4.5) |
| R7 60% private, declining DPI | `priv` | Exit-window state e_t, effective-age clock, structural scalar Φ; pacing is a decision |
| R8 S/H/R/L lens | `core.actions` | Per-group action catalogue; Lagrangian scores; decision cards; test that LEVER ≡ ADD + REFI |
| R9 three return series | `beliefs` | Forward Belief Engine (FBE) with a fourth market-implied anchor; group credibility |
| R10 overlay | `overlay` | Position layer with three books, VM by CSA, SIMM-like IM and limits OV1–OV3 (gap_03) |
| R11 agentic | `lab`, `agents`, `evaluator` | Deterministic meta-controller; typed tools; gates G0–G9; stub/replay backends |
| R12 IC discussion | `ic` | Quarterly pack, 12-seat shadow IC, grounded Q&A, two-channel view conditioning, decision log |
| R13 build on deck | `core`, `attrib`, `ic` | Two tiers become Tier 1A/1B/2; v8's eight lights become a 12-row state panel (gap_04); `test_v8_replica` |
| R14 seven groups + Corporate Finance | schema, `priv`/`pub`/`overlay`, `core.h` | `group` key on every row; envelopes and FTP; Corporate Finance owns the ledger and λ; IC agenda by group |
| R15 synthetic data | `synth` | SYN-ADIC-177 with world, sealed-truth and observation layers; `is_synthetic` taint; simulation-based calibration (SBC) and parameter-recovery gates |

**Principles.**

| P | Enforced by |
|---|---|
| P1 tools own numbers | Agents have no compute, file or shell tools. The claim validator rejects any number not resolving to a registry `metric_id`. No execution adapter exists |
| P2 evaluator integrity | Separate evaluator process checks sha256 of engine source, config, seeds and cube checksums, and data snapshot on every request; engine-side counting and rejection; missing or mismatched cache → refuse (Paper l.7210); spec schemas have no field for self-reported results |
| P3 planes | Final and misspecification seeds and checksums frozen at G1/G2; separate final-plane evaluator instance and cache; search sees bounded aggregates only (Paper l.6825); embargoed windows |
| P4 bundles and budgets | `IdeaBundle` schema; ≤ 3 retries; counter includes failures; counts feed the deflated Sharpe ratio (DSR) and the probability of backtest overfitting (PBO) |
| P5 gates | G1 `correct` (engine-owned) includes non-inferiority versus HOLD in every world, aggregated on the worst world. G2: strict improvement; a tie keeps the incumbent. G3: paired common-random-number test on the final plane, else `not_qualified` |
| P6 controls | Contract-fixed comparators at 3/5/10 years; shuffled-signal placebo; switch-off null control; single-change ablations; disjoint seeds |
| P7 claims | "Resolves" checked deterministically; "supports" judged by a cross-family auditor on logs and diffs; idea-provenance map |
| P8 humans own the contract | `AnalysisContract` takes a CIO/CRO signature at G0; agents may draft amendments only |
| P9 deterministic orchestration | Plain-Python state machine; 2 workers by default, configurable to 4; memory is a search heuristic only |
| P10 cross-family review | Auditor and Red Team run on a different model (and provider once approved); family count disclosed |
| P11 reproducibility | SeedSequence spawned per path block. Identical checksum at 1 and 4 workers [PD-bench]. Solver and BLAS pinned to one thread in the evaluator |
| P12 offline | Engine and tests need no network; `TPA_LLM_MODE=offline\|replay\|live` |
| P13 confidentiality | Prompts carry aggregates and IDs; holding-level content needs an operator flag in live mode; quarantined extractors; data stays on the machine |
| P14 explainability | Cards carry binding rows, duals, marginal value, attribution, flip thresholds and `priced_on` |
| P15 anonymized, horizon-free | DSL has no time-to-go or scenario-identity variable; path ids are random; observation lags are type-checked |

---

## 3. System decomposition

```
L9 IC        ic (pack, console, shadow IC, decision log) · cli · mcp_server
L8 Lab       lab (meta-controller) · agents (roles, LLM backends, validator) · evaluator (separate process)
L7 Explain   robust (ensemble, KL/W∞, entropy pooling, reverse stress) · attrib (Shapley on CRN, DVA)
L6 Decide    core.sim (P) · core.h (tree LP, Phase I/II, duals) · core.actions · core.safety (module F)
L5 Ledger    ledger (cash/HQLA/IG/encumbrance/facilities/payout; LR1–LR8; T4′ replica; CFP)
L4 Beliefs   beliefs (FBE, registry, credibility) · bridge (WYNTB)
L3 Assets    priv (funds | companies | claims) · pub (HF state machine, long-only) · overlay
L2 World     scen (regimes, factors, vol states, oil/fiscal, F_t, initial state, trees) · owner
L1 Data      data (schemas, bitemporal store, adapters, freeze) · synth (SYN-ADIC-177)
L0 Contracts contracts (pydantic models, array specs, units) · registry (SQLite, manifests, hashes)
```

| Module | Responsibility | In → Out | D/A | Owner | Interfaces |
|---|---|---|---|---|---|
| `contracts` | Schemas, array shapes, units, enums | — → models | D | CIO office (TPA desk) | All |
| `registry` | Append-only run, metric, claim, forecast and decision store; hash chain | records → ids | D | MRM | All |
| `data` | Bitemporal store; adapters; freeze and hash | raw files → `BookSnapshot` | D | CIO office; Corporate Finance (funding, collateral) | synth, beliefs, ledger |
| `synth` | SYN-ADIC-177 | seeds → census, marks, quotes, terms | D | MRM (holds the sealed truth) | data, tests |
| `scen` | Scenario engine E; stress filter and F_t; initial state; tree reduction | CMAs, market data → `ScenarioCube`, `Tree` | D | Risk (CRO office) | owner, engines, core |
| `owner` | Draw engine; mandate switch; payout library | cube → `DrawCube` | D | Corporate Finance | ledger |
| `priv` | Fund-interest, single-company and contractual-claim engines with group templates | book, beliefs, cube, actions → `FlowCube` | D | Five private groups own parameters; TPA desk owns code | ledger |
| `pub` | Hedge-fund liquidity-term state machine; long-only | terms τ, notices → `FlowCube` | D | Public Markets | ledger |
| `overlay` | Templates, surfaces, Greeks, VM by CSA, SIMM-like IM, OV1–OV3, monetization | blotter or family exposures → `FlowCube`, Greeks | D | Overlay; collateral by Corporate Finance | ledger, ic |
| `beliefs` | FBE; forecast registry; WIS scoring; credibility; flags | marks, quotes, forecasts → `BeliefSet` | D | Risk (validation); groups file forecasts | priv, bridge, core |
| `bridge` | WYNTB card per model | CMAs, lever priors → `BridgeCard` | D | CIO office | ic |
| `ledger` | Cash identities, ladder, T4′ replica, survival, CFP stage | flows, draws → `LedgerState`, `StressReport` | D | Corporate Finance (Treasurer) | core, ic |
| `core.sim` | Policy-in-the-loop P; certification | cubes, policy → `PathMetrics`, `Certificate` | D | CIO office; Risk certifies | evaluator |
| `core.h` | Tree LP, Phase I/II, kernel, λ, envelopes, FTP, selection MILP | tree, state, catalogue → `Solution`, `Duals` | D | CIO office (decision prices); Corporate Finance publishes FTP | actions, ic |
| `core.actions` | Catalogue, scores, cards, flip thresholds | duals, beliefs → `ActionCard`s | D | Groups propose; CIO office scores | ic |
| `core.safety` | Module F projection | proposal → safe action + diff | D | Risk | lab, ic |
| `robust` | Ranges, KL/W∞, k_MS, η\*, entropy pooling, reverse stress | path metrics → `RobustCard` | D | Risk | ic, lab |
| `attrib` | Prices-first explanation, Shapley, DVA, ablations | solutions → `AttributionCard` | D | CIO office; Corporate Finance for FTP lines | ic |
| `evaluator` | Hashing, counting, planes, gate statistics | typed specs → `RunRecord` | D | MRM | lab, mcp |
| `lab` | Meta-controller, budgets, gates, memory, escalation | contract → campaign state | D | CIO office; MRM oversight | agents, evaluator |
| `agents` | LLM roles, strict tool schemas, backends, claim validator | evidence slices → typed proposals, memos, flags | A (validator D) | CIO office; AI governance in Risk | lab, ic |
| `ic` | Pack (HTML+JSON), console, shadow IC, ballots, decision log | registry → pack, `DecisionRecord` | D + A | IC secretariat | humans |

**Core interfaces.** Dollar amounts are $bn as float64 in the ledger and LP, and float32 in cubes. Time indices: q = 0..40 quarter-ends, m = 0..120 months. Rates are per period.

```python
class AssetEngine(Protocol):                      # priv.*, pub.*, overlay
    engine_id: str; groups: tuple[GroupId, ...]
    def init(self, book: BookSnapshot, beliefs: BeliefSet, n_paths: int) -> EngineState: ...
    def step(self, q: int, st: EngineState, world: WorldSlice, act: ActionSlice,
             noise: NoiseSlice) -> FlowSlice: ...  # f32[P, n_flow_types], typed by FlowType x GroupId
class Ledger(Protocol):
    def apply(self, q: int, ls: LedgerState, flows: Sequence[FlowSlice], draw: f32[P]) -> LedgerState: ...
    def row_slacks(self, ls: LedgerState) -> dict[RowId, f32[P]]   # same RowIds as H's rows
class Policy(Protocol):                           # compiled PolicySpec or hand rule
    def act(self, q: int, obs: Observables) -> ActionSlice          # obs lagged; no horizon, no path id
def build_h(tree: Tree, ls0: LedgerState, cat: ActionCatalogue, c: AnalysisContract) -> LPModel
def phase1(lp: LPModel, tiers: Sequence[RowTier], reversible: ColMask) -> Phase1Result  # u*, IIS, levers at cap
def phase2(lp: LPModel, p1: Phase1Result, T_rec: int = 4) -> Solution                  # duals only from here
def price(sol: Solution) -> tuple[Kernel, FTPCurve, EnvelopeSet]                        # each carries priced_on
```

---

## 4. Quant core

### 4.1 Time grid and the meaning of 10%

| Item | Decision |
|---|---|
| Clocks | Quarterly: decisions, private engines, ledger. Monthly: market factors, hedge-fund dealing, overlay VM. Daily sub-steps only in the overlay stress module (named stresses, 2008/2020/2022 replays) and a flagged 2,000-path stress subsample. Pushback on 00_SYNTHESIS §2.1's monthly engine: private statements and marks are quarterly, so a monthly private clock triples the largest cost for little information; intra-quarter timing still enters via the monthly T4′ ledger and VM |
| Horizons | P: 40 quarters, reported at 3/5/10 years. H: 12 quarters (8–20 configurable; quarters 9–20 can be taken in 4-quarter steps). T4′: 24 months, monthly. T6: 5 years in P |
| 10% target | **Primary:** rolling 10-year geometric TWR, nominal USD, net of fees and costs, gross of distributions. Distributions accrue at the fund's own return, so distribution-inclusive wealth equals TWR wealth (00_SYNTHESIS §4.9, §9.3 item 2). **Also reported:** 3- and 5-year windows; real TWR; owner IRR at a 10% accrual (reported, never optimized); NAV growth net of distributions (real NAV holds at 8.3% only at a ≈5.3% payout, gap_05). P(10%) carries its model range and is never in an objective |

### 4.2 State representation and memory budget

At ADIC's size cohorting is unnecessary: unit-level simulation takes 10.9 s per 10,000 paths × 40 quarters single-process and 5.9 s on 4 processes, with an identical checksum [PD-bench]. Cohorting (strategy × vintage × region) switches on only above 1,500 units, behind a reconciliation test against unit-level flow distributions (KS < 0.05).

| Unit (synthetic census, GROUPS §6) | Count | Per-path state | Floats |
|---|---|---|---|
| Fund interests (PE, secondary funds) | 160 | V, reported N, unfunded U, effective age, NAV-loan balance, flags | 960 |
| Single companies | 90 | EV, debt, alive | 270 |
| Capital Solutions claims | 40 | accreted claim, credit state | 80 |
| Private-credit cohorts | 20 | 5 state shares, par | 120 |
| Hedge-fund lots | 40 | NAV, request, state, months queued, times gated, holdback | 240 |
| Long-only; overlay buckets; CSAs | 24; 15; 12 | NAV; Δ/Γ/ν/Θ; MTM, collateral, IM | 120 |
| Ledger; world | 1; 1 | cash/HQLA, IG, 3 facilities, encumbrance, payout YTD, B_y, TWR peak, CFP stage, cushion; S, e, Z, filter posterior, F_t, oil, vol states | 30 |

That is ≈1,820 float64, or 14.6 KB per path: 29 MB per 2,000-path block. Outputs are 48 float32 summaries per path-quarter (77 MB per 10,000 paths), streamed per block to Parquet.

Exogenous cubes are **regenerated and verified**, not stored. Regeneration costs ≈2.3 s per 10,000 paths, and a checksum mismatch stops the run. Final-plane cubes are materialized once and sealed.

### 4.3 Scenario generator

- **Structure.** Follows 00_SYNTHESIS §4.1: a monthly regime-switching, CMA-anchored factor model with about 20 factors and t₅ innovations. Factors: macro and rates, two-factor Brent, USD, spreads and EBP, equity, log VIX with β(T), MOVE, OVX, exit factor X, secondary discount, NAV-loan spread, private-credit loss index. Coupled chains: macro regime S, exit window e ∈ {O,N,D,F}, oil/fiscal shock type Z ∈ {N,B,SG,DB,SS,GW}.
- **Substitutions.**
  - No HSMM library is installed. Dwell times use a state-expanded HMM: negative-binomial dwell via k sub-states, fitted with hmmlearn, or a numpy jump-penalized estimator.
  - The 3-state stress filter is hmmlearn `GaussianHMM`, forward-filtered only, giving $F_t=\sigma(a+b\,\mathrm{logit}\,\hat\pi^c_t)$ (gap_04 §4.2).
  - In simulation, P recomputes F_t on simulated factors with the frozen filter.
- **Initial state.** gap_04's seven-step procedure, hashed at G2: oil from the futures curve, Gulf-war dwell conditioned on elapsed duration, draw expectation.
- **Ensemble.** M1 J.P. Morgan 2027, M2 BlackRock fee-adjusted, M3 AQR, M4 drought, M5 stagflation, M6 "risk premia rise", plus bootstrap families.

| Plane | Contents | Frozen at |
|---|---|---|
| Search | Two generator families (00_SYNTHESIS §5.1): regime-switching on M1, M2, M3, M5, and block bootstrap B1 fitted to data ending 2015 with a 12-month embargo. Seeds S_search; 2,000–10,000 paths per world | G1 |
| Final (sealed) | Fresh seeds on M1–M6, plus worlds never searched: M4, M6, held-out FHS generator B2 (2017–2026). 50,000 paths per world; ≥ 3 pre-registered historical windows with embargo | G1 (hashes), run once |
| Misspecification (judged with the final plane, never searched) | Drought persistence 0.95, Φ = 0.75, adverse hedge-fund terms, PD/LGD truth variant, milder M6 | G1 |

- **Calibration targets** are those of 00_SYNTHESIS §7.1, for example drought distribution yields of 12–15% persisting ≥ 4 years.
- **Output contract.** `ScenarioCube{meta: model_id, plane, seed_key, generator_hash, asof, is_synthetic; factors f32[P,M,K]; regime/exit/shock i8[P,M]; stress_post f32[P,M,3]}`.

### 4.4 Private engines per group

Three engines serve seven groups (00_SYNTHESIS §4.2; GROUPS §3). Every action is scored on one deflator; group P&L is attribution only.

| Engine | Groups | Core equations and defaults (all [I] unless sourced there) |
|---|---|---|
| Fund interests (RFT-TA v2) | PE; secondary funds; closed-end credit funds | Calls $C=(1-e^{-\lambda\Delta})U$ with $\lambda=\bar\lambda_s(a)m^C(e)$. Distributions on effective age, $a^e_{t+1}=a^e_t+\kappa(e)\Delta$ with κ = 1.2/1.0/0.6/0.5. Reported-NAV AC1 0.66–0.71. Stressed calls λ(U − B^SL) + c^SL·B^SL |
| Single companies | Co-investment, CV stakes, Capital Solutions kickers | EV jump-diffusion, E = max(V − D, 0); Weibull exits (k 1.447, η 7.70 years) × 1.3/1.0/0.5/0.3 by exit regime; P(MOIC < 1) ≈ 0.35–0.40 |
| Contractual claims | Capital Solutions; Private Credit | Credit state machine; PIK share 15/30/60–80/20% by regime; separate PIK and extension hazards; LGD 0.67, PD_N 1.1%; delayed-draw draws 15/20/30/60% |
| Factor model + state machine | Public Markets | Hedge-fund lots in states LOCK … TRS_TERM; the P5 cash share φ_i(h,S) is the only ladder interface (gap_01 §5). Long-only: benchmark + tracking error |

- **Economic vs reported NAV.** Risk and value use economic NAV; covenants, bids and the draw basis use reported NAV.
- **DPI drought.** The exit-window state e (m^D 0.45–0.50 in D), the slower effective-age clock and the structural scalar Φ ∈ [0.75, 1].
- **How beliefs enter.** Each path draws $\bar\alpha_i$ once from the FBE posterior plus a common group-bias shock, so forecast risk does not diversify away (00_SYNTHESIS §4.3).
- **Code reuse.** Increment 1 ports `hf_ladder.py` (gap_01) and `t1_engine` (gap_02) as regression fixtures.

### 4.5 Belief fusion

- **One forward basis.** The forward log return on nowcast economic NAV, net of fees (00_SYNTHESIS §4.3).
- **Fund interests.** Benktander credibility $U=c^*U_{CL}+(1-c^*)U_{BF}$, with the prior frozen at inception and fused with the forecast only.
- **Single deals.** Constrained GLS, $\hat\mu=\Lambda^{-1}(m\sigma_k^{-2}+\mathbf1'\tilde\Omega^{-1}\tilde s)$, with correlated errors and weights ≥ 0.
- **Market-implied anchor (blueprint graft 1, Brief §6).**
  - Secondaries desk bids give a buyer-implied return through $(1+y_P)\approx(1+y_V)(\theta/p)^{1/D}$; Capital Solutions reserve quotes do the same for REFINANCE.
  - Each enters as a fourth signal with its own bias prior and precision.
  - Only external prints get full weight; desk quotes carry the conflict flag, and a desk never quotes where it may bid (GROUPS §4.2).
- **Credibility.** A group forecast enters once at precision $1/(\kappa_g^2\hat\sigma^2)$, with κ lognormal, median 1.75 (1.2–2.7), and per-group bias priors b^u/b^f (GROUPS §5). All closed-form numpy; no MCMC.
- **Outputs.** μ̂, σ̂, an 80% band and flags F1–F10, plus three blueprint diagnostics:
  - a **Zombie-NAV** flag: reported mark ≥ cost while the fitted exit hazard has been below its regime median for ≥ 4 quarters;
  - P(forecast achieved within k quarters);
  - a catalyst requirement: a recovery forecast with no dated milestone has its precision halved.
- **Tier usage.** Tier 2 uses posterior means; Tier 1 uses the posterior P10 with group bias at +2 sd.

### 4.6 Action economics per group

Every action is a bundle of state-contingent cash flows and resource uses, and LEVER ≡ ADD + REFI (00_SYNTHESIS §4.4; gap_01 §3; GROUPS gap_03 §2.3). Only external counterparties raise liquidity.

| Group | SELL | HOLD | REFINANCE (cash-out) | LEVER (exposure-up) | Lag; regime availability |
|---|---|---|---|---|---|
| PE | LP-led sale or strip at a hedonic price on economic NAV (buyout 91%; crisis 0.80–0.84) | Fund calls; CV elections are GP-triggered | LP-portfolio NAV facility (Corporate Finance) at SOFR + 300bp, LTV 10–20%, pledge-capped near $2bn (GROUPS gap_01); preferred at 12% | Up-sized re-ups; **pacing corridor** Green 0.75–1.25×, Amber 0.25–0.5× | Sale 3–6 months, success 0.75–0.85 / 0.6 / 0.4–0.5; pacing 1–4 quarters |
| Secondaries | Tertiary sale or strip; external buyer only | Carry deferred payables, which count as debt and a hard outflow | LP-level facility on S1/S3; CFO on a seasoned pool | ADD by discount purchase iff b\* ≥ p^ce after a 4.2–5.1% winner's-curse haircut. Buyer deferral is a vendor loan, counted as debt ≤ 10% of group NAV. Contingent on discount > 20%, Tier 1 green and stage Green/Amber | ≤ 12 months; 3–5% of segment volume |
| Co-investment | Single-asset sale at a buyer-model bid (71–79% normal, 56–65% drought) | LAPV less concentration CVaR | Pool facility only; **single-asset REFINANCE inadmissible** | Holdco PIK in benign regimes only | 3–9 months; bid cut in drought |
| Capital Solutions | Syndication; secondaries at yield mark −8–12% (crisis −20–30%) | Amendment policy by least-squares Monte Carlo | Back-leverage D/E ≤ 0.5 with a cash-carry row; CFO | Same, cash-pay families only | Back-leverage arranged in benign/normal; CFO 6–12 months |
| Private Credit | Loans 0.99/0.96/0.85; LP interests 89%; evergreen tender ≈38% filled | SMA run-off switch, ≈$0.8–0.9bn in year 1 | SMA back-leverage, LTV ≤ 40–45% | SMAs only, if EL < y_A − c_B ≈ 4.0% | Days to 4 months; queues in crisis |
| Public Markets, hedge funds | Redemption as a queued SELL; notices only on notice dates, irrevocable unless τ says otherwise | NAV + PV(α) − terms value | Unit loans at 20–50% LTV with consent | Portable alpha, HF-TRS (TRS_TERM branch) | φ(P5): 19% by month 3, 55% by 6, 66% by 12 |
| Public Markets, long-only | Sale at impact Yσ√(Q/V) | — | **Physical-to-synthetic (P2S)** at 0.40–0.70% a year per $ freed in normal markets, 2.2–3.3% in stress; VM liability | Exposure ≤ 1.30× | 1–7 days |
| Overlay | Tail monetization if V(1 − ba) + λ^wΔL ≥ continuation value; cut the opportunistic book | Roll the floor ladder | Compression, novation, CSA reallocation, UST as IM, only if OV1–OV3 hold before and after | Add tail layers within the 0.5% cap; scale the opportunistic book only if DSR ≥ 0.95 | T+0 listed; days OTC |
| Corporate Finance | — | — | Revolver SOFR + 85bp, 0% credit in 30-day rows; repo; term debt | Portfolio facilities (H variables) | ≤ 3 months |

### 4.7 Leverage

- **Limits** (00_SYNTHESIS §4.5): recourse debt ≤ 10% target / 15% hard; economic exposure ≤ 1.30×; encumbrance ≤ 15/20%; covenant P(trigger, 12 months) ≤ 2%; ≤ 20% of debt maturing in any 12 months; NSFR-style stable funding.
- **Funding curves** are piecewise-linear in H.
- **Doctrine.** Portfolio LEVER passes only if Tier 1 holds with the debt included and the use's α\* exceeds its shadow costs. Leverage moves only through the cushion-monotone rule, never sized to the gap to target.

### 4.8 Overlay: a position layer

- **Books.** Three: tail, opportunistic, synthetic beta. One sensitivity set (SIMM definitions) feeds P&L, VM by CSA, IM, net-Greek limits and the ledger (gap_03 §2).
- **Increment 1 (Level 1).**
  - Families are factor exposures.
  - The floor ladder is 90/72 put spreads on 3/6/12-month rungs, priced on equity SSVI anchored to VIX via β(T).
  - At the 0.15% floor it buys ≈$7.1bn of notional, at a cost of 3.74% of notional a year (GROUPS gap_03 §5, SYNTHETIC).
- **Increment v1 (Level 2).** About 15 templates and a SIMM-like engine (delta, vega, curvature; versioned parameter tables). Acceptance: reproduce gap_03's worked example, $609.7m of separate-CSA IM falling to $418.9m on one CSA, and the 1.77 offset ratio.
- **Simulation.** Monthly delta-gamma-vega-theta expansion with monthly full revaluation of option buckets. A P&L-explain test (Spearman > 0.80, KS < 0.09) decides where the Taylor form is allowed.
- **Limits OV1–OV3** are computed by full revaluation in named stresses, where they are defined.
- **Collateral.** Corporate Finance's pool funds VM and IM. Recognition φ is 1 for cash, 0.7 for OTC collateral with reuse rights, 0 for pledged. Posted IM is encumbered and excluded from T2. A deferred IM step follows each SIMM recalibration after a stress (00_SYNTHESIS §4.6).
- **Tail credit** is booked ex ante at kernel value, with the policy residual on the IC line (GROUPS gap_03 §4).

### 4.9 Liabilities

- **Draw (Phase 1 reduced form).** $d^{tgt}_y=\Pi_{[5\%,10\%]}(c+b\,FN_y)$ and $d_y=\Pi(\rho d_{y-1}+(1-\rho)d^{tgt}_y)$, with c = 7.5%, b = 0.625, ρ = 0.5, and override probabilities by Z.
- **Basis.** $D_y=d_yB_y$ on opening-of-year reported NAV, reset annually; fixed-USD and current-NAV conventions are sensitivities. Paid quarterly (00_SYNTHESIS §4.7).
- **Mandate switch.** Mode B (owner call) is the default; the owner band (5% in CFP Red or crisis) is a priced option. The payout-rule library is used only for proposals to the owner. The structural fiscal model waits for v2.

### 4.10 Internal capital market

H's Phase-II duals on every row containing cash give a quarterly liquidity premium and the kernel

$$\pi_{s,t}=p_sm_{s,t}\prod_{k<t}(1+\ell^q_{s,k})^{-1},\qquad \ell^q=M/(\pi^H-M),\qquad M=\mu+0.92\phi+\textstyle\sum_r a_ry_r$$

(00_SYNTHESIS L1, §4.4).

- **Envelopes.** $\Lambda^k_g=\sum_{i\in g}a^k_i(x^\*)$ for each coupling row, pooled over 10 SAA tree replications and reported with ranges. Releases are free; increases on binding rows pay the dual (L14).
- **Decision prices.** Undamped duals with no floor. The KKT cap is the cheapest *spare* lever per unit of headroom, not buffer carry (GROUPS gap_01 §2.3). Increment 1's sanity check reproduces revolver-signed μ ≈ 0.0113 (≈1.1% PV per $ of month-24 headroom) and 0.243 without the revolver (SYNTHETIC).
- **Corporate Finance as internal bank.** Publishes the FTP curve as an EWMA of decision duals (2-quarter half-life, ±50% collar); holds the mismatch from vintage-locked performance charges; charges the contingent-liquidity charge once (c_buf = 1.5%); credits contractual inflows and crisis payoffs.
- **Guard.** Every card and envelope carries `priced_on ∈ {feasible, restored_problem}` plus a recovery hash. A card priced on a pinned dual fails CI.

### 4.11 Optimizer

**H: here-and-now LP.** The tree is built from the P cube by forward clustering: regime-stratified k-means with a fixed seed, b₁ branches at quarter 1, b₄ per node at quarter 4, then a fan. Tail leaves are oversampled by regime and draw state and reweighted, so the 0.6% CVaR rests on ≥ 30 leaves.

- **Per node (32 columns).** State: cash/HQLA C, facility F, 7 group NAVs V_g, 5 unfunded U_g, 3 elastic slacks used only in Phase I. Decisions: long-only sales, hedge-fund notice proceeds, P2S, 5 commitments k_g, 5 group sales s_g, ΔF.
- **Dynamics (equalities).**

$$C_n=(1+r^c_n)C_p+\textstyle\sum_g\delta_{g,n}(V_{g,p}-s_{g,p})-\sum_gq_{g,n}U_{g,p}+\sum_gb_{g,n}s_{g,p}+s^{LO}_p+s^{HF}_p+(1-m)y^{p2s}_p+\Delta F_p-r^F_nF_p-D_n-VM_n$$

  Here δ is the distribution rate, q the call rate and b the bid as a fraction of NAV, all scenario-specific. The V_g, U_g and F transitions follow the same pattern.
- **Rows per node (≈25).** 14 transition equalities (cash, 7 NAV, 5 unfunded, facility). Inequalities: IG at 8% elastic / 4% hard; T3 30-day coverage with facilities at 0%; LR8; leverage; encumbrance; 5 sale-depth rows; hedge-fund notice capacity φ(h,S); P2S cap.
- **Root.**
  - 24 monthly T4′ headroom rows $hd_h(x)\ge-g_h$, with slopes from finite differences on the `ledger` stress replica (GROUPS gap_01 §2.1).
  - ≈400 asset-action columns z_{i,a} ∈ [0, 1] with lags and consent probabilities.
- **Leaves.** Regression terminal values ω_g, ψ; an 8-segment piecewise-linear CRRA utility; path-minimum headroom m_ℓ; a Rockafellar–Uryasev CVaR at 99.4% on signed margins (the T6 surrogate, 00_SYNTHESIS §4.9).

**Measured size and time** (benchmark structure with the per-node and root layout above, HiGHS 1.15.1, one thread) [PD-bench]:

| Tree (leaves × quarters) | Nodes | Variables | Rows | Nonzeros | Dual simplex | Use |
|---|---|---|---|---|---|---|
| 500 × 8 | 2,561 | 82,852 | 61,007 | 0.33M | 12.6–14.1 s (IPM 41–51 s; CLARABEL 62 s; PDLP 594 s) | W2 what-ifs |
| **600 × 12** | 5,491 | 176,712 | 133,657 | 0.70M | **32 s** | Quarterly default |
| 1,000 × 12 | 9,121 | 293,272 | 222,007 | 1.16M | 90 s | Sign-off |
| 2,000 × 12 | 18,121 | 582,272 | 441,007 | 2.27M | 286 s | Overnight only |
| Warm re-solve (fix 20 columns; penalties ×10) | — | — | — | — | 0.04–0.06 s | Selection loop, tests |

Solve time grows roughly as n^1.6. Production adds T4′, CVaR, utility and encumbrance rows (≈+10%), so the default is estimated at 35–50 s.

The 2-minute target holds up to ≈300k variables. A 20-quarter horizon stays inside it by taking quarters 9–20 in 4-quarter steps: 1,000 leaves × 11 stages is ≈261k variables, ≈75 s by interpolation. The 2,000-scenario corner runs overnight.

**Pushback.** 00_SYNTHESIS §4.8 budgets ≈1.8M variables per 1,000-leaf tree as a stochastic MILP, "tens of minutes on HiGHS". This design keeps recourse at group level and integers out of the tree. Parallel dual simplex was slower (20.2 s against 12.6 s on 4 threads), so parallelism runs across models and SAA replications in separate processes.

**Phase I / Phase II** (gap_02 §4; L15):
- **Phase I.** HiGHS `feasibilityRelaxation`, present in highspy 1.15.1, run per tier lexicographically. Only reversible levers are free: facilities, pacing, a band request, reserve, amber sales, hedge-fund notices. PE, Secondaries and Co-investment sales are fixed at 0. IIS via `getIis`, with a deletion filter over ≈30 row families as the fallback.
- **Phase II.** The restored problem, with glide path $g_{r,t}=u^\*_r(1-t/T_{rec})^+$ and T_rec = 4 quarters. Only Phase-II duals become λ. The semantics are pinned by porting gap_02's 8 and GROUPS gap_01's 18 pinned-dual tests.

**Selection loop** (00_SYNTHESIS §4.4):
1. Solve the LP.
2. Score every candidate by its reduced cost against the duals: $\mathrm{Score}(i,a)=\sum\pi\Delta CF+\sum\tilde\mu(h\Delta HQLA-\Delta SC)+\sum\tilde\phi(\Delta IGC-0.08\Delta NAV)-\lambda_R\Delta\mathrm{CVaR}-\lambda_{Lev}\Delta Lev-\lambda_{Enc}\Delta Enc-\sum\rho_k\Delta\mathrm{Floor}_k-\kappa^{irr}-\kappa^{GP}-\kappa^{tc}$.
3. Solve a small MILP (`scipy.optimize.milp`/HiGHS) over ≤ 600 binaries, at most one action per asset, and ≤ 30 aggregated coupling rows.
4. Fix and warm re-solve; 2–5 damped iterations.
5. Take dual bands from 10 SAA replications (≈90 s on 4 processes); flag sign flips; apply hysteresis.

The MILP stays because a price-only rule was $24.7m worse in the 40-asset test (00_SYNTHESIS §4.4). LP-split assets form the IC's marginal-asset agenda.

**MPC and P.**
- **MPC.** H re-solves each quarter from the frozen state.
- **Standing policy.** The cushion-monotone rule set of 00_SYNTHESIS §4.8 (reserve, pacing with stage cut, leverage, hedge ratio, waterfall), about 20 θ.
- **Search.** Seeded `scipy.optimize.differential_evolution`. v1 adds `cma` (pure-Python, BSD-3) only if DE is ≥ 5bp CE worse than a reference at equal budget (pre-registered). Racing by successive halving (27 candidates, η = 3, 2,000 paths per model). One evaluation (2,000 paths × 3 models) takes ≈6.5 s, so 480 evaluations take ≈13 minutes on 4 processes [PD-bench scaling].
- **Certification.** Fresh 50,000 paths per world, ≈17 s each on 4 processes [PD-bench]; one-sided 95% Clopper–Pearson bounds; importance sampling below 0.5%.
- **Consistency checks.**
  - Terminal values ω, ψ are regressed on P paths each quarter.
  - H–P ranking test: Kendall τ ≥ 0.8 between H's and P's ranking of the top 30 candidates; else flag the card and select on P.
  - Replay test: H's first-stage actions replayed through P on the tree's paths must match the LP's projected cash to within 1%.
- **Module F.** A ≤ 600-variable QP in cvxpy/OSQP that projects every proposal (optimizer, agent or IC) onto the linearized Tier-1 set with amber buffers, and logs "what changed".

### 4.12 Objective and constraints: improving the two tiers

Lexicographic, implemented as Phase I → Tier 1B check → Tier 2, never through penalty prices (gap_02).

| Row | Form (00_SYNTHESIS §4.9) | Single computational home |
|---|---|---|
| T1 payout | Instalment ≥ max(5% of B_y, owner call) | ledger, H, F |
| T2 IG + cash | 8% elastic, 4% hard, net of encumbered IM | ledger, H, F |
| T3+ 30-day coverage | Unencumbered HQLA ≥ max(look-back, **CVaR₉₉ stressed VM** + ΔIM) + draws + stressed calls − P10 distributions + debt service; facilities 0%. This hardens P99 to CVaR₉₉ (blueprint graft 3) | ledger, H, F |
| T4′ | s\*(θ\*), θ\* = 0.76 (0.79 pooled; GROUPS gap_01); survival on Treasury + Public Markets + facilities ≥ 24 months; canonical conventions hashed | ledger replica; root rows in H; F |
| T5 | Leverage, encumbrance, LR8, dealer and overlay limits | H, F |
| T6 red event | P(forced PE sale or payout below minimum, 5 years); bands 0.5/1/2% (M1–M5, mixture), —/2.5/5% (M6 class) | P (Clopper–Pearson); H carries the CVaR surrogate |
| T7, T8, T9 | Plan shortfall ≤ 2.5%; stressed coverage ≥ 1.0 per shock type; covenants 2%/1% | P; ledger |
| Tier 1B | Mixture median 10-year TWR ≥ 7%; worst-model CVaR₁₀ ≥ 0 | P across worlds |
| Tier 2 | $J=\sum_mw_m\{\mathbb E[U_3(\widetilde W^{real}_{40}/W_0)]-\lambda_T(\mathbb E[(1-\widetilde W_{40}/\widetilde W^\star_{40})_+^2])^{1/2}\}$, γ = 3 | P exactly; H uses a piecewise-linear proxy with λ_T^H tuned so H and P rank alike |

**Improvements.**
1. Every row has one home and one test.
2. The blueprint's stress-coverage test (tail inflows ≥ opportunistic VM + private shortfall) is a reported ratio on the offset card, hard only through OV2 (≤ 25%).
3. The gambling detector and the cushion- and loss-monotone type rules run in CI.
4. The recovery cushion (gap_02 §4) keeps rules interior.

The synthetic book is in execution recovery today: d₀ = $11.3bn against T4′, with structural u\* = 0 (GROUPS gap_01 §2). So increment 1 must exercise `priced_on: restored_problem` from the first run.

### 4.13 Robustness

- **Ensemble first.** Min/max/mixture across M1–M6 (R8) leads every metric.
- **Divergence measures.** All are reweightings of one cube: KL worst case at η = 0.05 (0.01 for rare events), W∞ shift of 0.5pp, breakdown divergence η\* and k_MS (00_SYNTHESIS §4.10).
- **Entropy pooling.** In-house, because the open package is GPL-3.0: Newton on the dual of the minimum-KL problem with ≤ 20 linear views. Estimated < 1 s on 50,000 scenarios.
- **Reverse stress.** Minimum-KL tilt to failure, with a Pesenti ranking. Red-team `ScenarioSpec`s stay inside declared parameter bounds.

### 4.14 Attribution

- **Order.** Prices first (λ, reduced costs, the KKT interlock); then capability values from forced warm re-solves; then exact Shapley over ≤ 6 action groups (64 coalitions) on common random numbers.
- **Group DVA in dollars.** $\mathrm{DVA}_g=\sum\mathrm{NAV}_i(r_i-r^{FB}_i)-\mathrm{FTP}^{vint}_g-\lambda_R\mathrm{RC}_g+\mathrm{CR}_g$, reconciled to the total. Intra-ADIC transfers net to zero (gate V2, on DVA ledgers).
- **Audits.** An anticipation audit on every attribution. `test_v8_replica` holds ±0.05pp per row (gap_05).

### 4.15 Performance budget and operability

| Workload | Target (Brief §3) | Measured [PD-bench] | Budget kept |
|---|---|---|---|
| P: 10,000 paths × 40 quarters, asset level, policy in loop | < 60 s | 10.9 s (1 process); 5.9 s (4); one-off JIT 4.9 s, cached 0.6 s | ≤ 30 s at full fidelity (2.5× reserve for Level-2 overlay, 20 factors) |
| P: 50,000 paths, per world | — | 16.8 s (4 processes) | ≤ 60 s; sealed 7 worlds ≤ 7 minutes |
| H: 500–1,000 leaves × 8–12 quarters | < 2 minutes | 13–90 s | Default 600 × 12; 2,000 leaves overnight |
| Nightly batch | — | — | P on 6 worlds, H on M1–M3 in parallel, SAA bands, robustness, attribution, pack: < 1 hour |

**Operations.** CLI (typer): `tpa data freeze`, `tpa scen build`, `tpa run quarter --asof`, `tpa h solve --preset default`, `tpa p certify`, `tpa pack build`, `tpa lab start|status|escalations`, `tpa evaluator serve`, `tpa mcp serve`. Structured JSON logs. Every failure stops loudly: hash mismatch, non-optimal solve, pinned dual, missing cache. Compute cost is zero marginal; LLM spend is in §5.

---

## 5. Agentic layer

Workflow first: agents act only where options cannot be enumerated (00_SYNTHESIS §5.1). Every single-asset lens action is priced deterministically each quarter. Agents propose *packages* and new structures as columns, and the duals referee them.

| Role | Does | Typed tools | Model, effort | Gate |
|---|---|---|---|---|
| Contract Drafter | Drafts `AnalysisContract` amendments; never adopts | `check_contract` (gate feasibility, Phase I) | A, high | G0 human signature |
| Quarantined Extractor | GP notices, memos, covenants → typed records; dual extraction | `submit_extraction` only; no outbound tools | A, medium | Schema; human sample |
| Ideators ×2 (isolated challenger only as an ablation) | `IdeaBundle`: hypothesis, `PolicySpec` or package, plan, ≥ 1 metric and ≥ 1 constraint rubric | `search_metrics` (bounded aggregates), `evaluate_policy` (counted), `price_actions` | A, high | G3–G5 |
| Red Team | Bounded `ScenarioSpec`s; reverse stress; unnamed OV2 breaches | `evaluate_scenario` | B, high | Disclosed at G8 |
| Memo Writer | IC memo citing metric ids only | `get_metric`, `validate_claims` | A, medium | G7 |
| Auditor | "Supports" verdicts from logs, manifests and engine diffs | Read-only registry | B, high | G8 |
| Translator | Natural language → `ViewSpec`/`ScenarioSpec`, confirmed over multiple turns | `draft_view`, `ep_condition` | A, medium | Human confirmation |
| Shadow-IC seats ×12 | Assessments, cruxes, minority reports | Evidence-slice tools | A + B, high | Rubric; flag, never vote |

- **Trust boundary.**
  - Tools are served by `tpa evaluator serve`, a separate process exposing MCP (mcp 2.3) over stdio. Agents hold no file, shell, code or network tool, so "no exploratory evaluation outside the evaluator" is structural (Brief P4).
  - `PolicySpec` is a pydantic AST with ≤ 25 nodes and ≤ 8 parameters, with typed observation lags and cushion- and loss-monotonicity rules. It compiles to vectorized numpy, never `eval`.
- **Meta-controller.** Plain Python, with state persisted in the registry:
  - DRAFT → SIGNED | SIGNED_IN_RECOVERY → QUALIFIED → BELIEFS_FROZEN (G2) → (IDEATION ⇄ SCREENING)\* → SELECTION → SEALED (G6) → RETROSPECTIVE (G7) → MEMO → REVIEW (G8) → IC (G9) → CLOSED, with ESCALATE reachable from any state.
  - It stops on budget exhaustion, after 6 cycles without promotion, or when no column has a positive robust reduced cost.
- **Gates.** Evaluator-owned.
  - **G1 `correct`:** hard rows satisfied (or on the glide path); T6/T7/T9 bounds within their bands; the DSL compiled; budgets respected; non-inferiority $\min_m\Delta\hat\Psi_m\ge-\varepsilon_{ni}$.
  - **G2:** $\Delta\hat\Psi-2\,\mathrm{SE}>\varepsilon_{mat}$, with materiality 3/5/10/15bp by action class; a tie keeps the incumbent.
  - **G3:** sealed final plane; paired common random numbers; intersection–union across worlds; Holm; PBO ≤ 0.20. Labels: QUALIFIED, `not_qualified` or NOT ASSESSED.
  - Rubrics are diagnostics and stopping rules only (00_SYNTHESIS §5.4; Paper l.6926-6933).
- **Planes.** The search evaluator sees only the search plane and returns bounded aggregates and failure categories. The final-plane evaluator is a second instance with its own cache and the sealed seeds, called once per campaign at SEALED. Final cases never feed tuning, memory or promotion (Paper l.6798).
- **Budgets.** Counted in the engine: evaluations (failures included), paths, CPU-seconds, tokens and dollars from call records, and α-wealth (W₀ = 0.05). The counts drive DSR and PBO.
- **Memory.** An append-only log plus a ≤ 300-word conclusions paragraph. It is search-only, reset per campaign, never sees the final plane and never reaches the IC (Brief P9).
- **Escalation and assumptions.** `escalate(kind, question, proposed_assumption, severity)`: low severity logs the assumption and continues; high severity pauses the worker until a human replies. All assumptions appear in the pack appendix.
- **Cross-family review.** Author A is `claude-opus-5-5`. Reviewer B is a different model with an independent context (logs and diffs only) until ADIC approves a second provider, whose SDK is then a justified addition. The pack discloses the family count; same-family seats are treated as correlated and never extremized (00_SYNTHESIS §6.2).
- **LLM settings** (anthropic 1.15). Typed outputs via `client.messages.parse(output_format=Model)`. Tools use `strict: True` and `additionalProperties: false`. `tool_choice` is auto plus a prompt instruction, since forced choice is rejected on Opus 5.5. Adaptive thinking with explicit `output_config={"effort": ...}` (the default is medium). Refusal fallback is opt-in and `stop_reason == "refusal"` is handled. Prompt caching on frozen prefixes; the Batches API (50% price) for non-urgent seat assessments; Bedrock, Vertex and Foundry clients behind the same backend.
- **Offline mode.** `ReplayBackend` replays recorded responses keyed by sha256(model, system, tools, messages, params); `StubBackend` gives seeded rule-based outputs (e.g., DSL-grammar sampling). CI runs replay. Without LLM access only narrative is lost; numbers are unaffected.
- **Cost.** Opus 5.5 lists at $4 / $20 per million tokens; a lab cycle costs ≈$9–16, budgeted at $50 soft / $200 hard (00_SYNTHESIS §5.7). A Tier-A shadow-IC round is ≈$5–10 [I]; total ≈$1–3k a quarter [I].

---

## 6. IC layer

| Audience | Sees each quarter |
|---|---|
| Whole IC (Block A) | CFP stage; Tier-1 board (nominal, model range, Clopper–Pearson bound, KL(0.01) worst case, band); T4′ survival fans; λ by regime with the marginal-cost-of-liquidity curve; WYNTB bridge; P(10y ≥ 10%) against worst-model P(red); ε_R–cost frontier (Mix A vs B); 12-row state panel (gap_04 §8); comparators and archetypes A/B/C (blueprint graft 5); gambling flags |
| Each group head (Block B) | Envelope use and priced requests above it; decision cards (P(best), regret both ways, LAPV waterfall, flip thresholds, consents); belief card with the forecast's information value against its own reference class, only when n_eff ≥ 20; net α\* after charges; hurdle; FTP; RECOVERY delivery share φ_g |
| Treasurer (Corporate Finance) | Ledger and ladder LR1–LR8; facility and covenant paths; collateral ladder by CSA; Phase-I infeasibility prices (never on cards); FTP curve; owner-draw paths, band activation, J\*_A − J\*_B |
| CRO / CIO / Overlay head | T6 bands, k_MS, η\*, reverse stress / envelope coherence, bridge model weights, marginal-asset agenda / offset card (OV1–OV3), fatigue tracker, ex-ante tail credit, services ledger |

- **Shadow IC.** Twelve seats defined by mandate: CIO, CRO, Treasurer (also the owner's advocate), five private-group heads, the Public Markets head, the Overlay head, an Outside-View Forecaster and a Red Team. A Facilitator and an AI Validator sit outside the twelve. Seats flag, never vote. Group heads recuse on their own envelopes and are scored on total-portfolio regret (00_SYNTHESIS §6.2; GROUPS §7).
- **Protocol** (00_SYNTHESIS §6.3). S0–S7 at T−10 to T−2: frozen questions, independent assessments, reveal, ≤ 3 cruxes, pre-mortem, minority reports. **H0: blind human pre-vote at T−1**, locked on submission. H1–H4 at T: staged reveal and ballot. H5–H6: minutes, dissent verbatim, signposts.
- **Agenda.** A total portfolio → B group blocks, ordered by the marginal-asset agenda → C cross-group items (internal transfers at zero liquidity, desk quotes through the pricing committee, P2S/HF-TRS collateral) → D ballot.
- **Q&A.** Answers cite `run_id:artifact:path` and label each statement as model output, agent judgment or assumption; "not in the artifacts" is valid. What-ifs: W1 entropy pooling (< 1 s); W2 H at 500 × 8 on cached paths (≈15 s); W3 re-simulation (minutes). An irreversible Tier-A action decided on exploratory evidence needs a sealed confirmatory run.
- **View conditioning.** Two channels: asset and lever views become FBE signals (ω = (P90 − P10)/2.563), and scenario views go through entropy pooling with target shrinkage $v^{eff}=E_p[g]+c(v-E_p[g])$, KL flags at 0.05/0.25/1.20/2.30 and ESS ≥ 5,000 (00_SYNTHESIS §6.4).
  - The pack embeds a ≈150-line vanilla-JS port of the Python EP solver with golden vectors. It runs a self-test on load and shows a red banner on any deviation above 10⁻⁶; no Node is needed.
  - W1 numbers are labelled exploratory. Any number entering the decision log is recomputed by the Python engine.
- **Decision log.** Append-only `DecisionRecord`: ballot, rationale, override against the model recommendation with a reason code, dissent, 3–6 signposts with flip values, and a review date. Every probability shown is Brier-scored at 1, 4 and 8 quarters.

---

## 7. Data and synthetic generator

| Entity (bitemporal: valid_from/to, recorded_at) | Key; grain | Required fields (00_SYNTHESIS §7.2; GROUPS §3) |
|---|---|---|
| `holding` | holding_id | group, strategy, sub_strategy, GP/company ids, vintage, region, commitment, wrapper, consent flags, `is_synthetic`, `source` |
| `cashflow` | holding × date | type (call, distribution, recallable, in-kind, coupon, PIK accrual), amount, currency |
| `mark` | holding × mark_type × as_of × recorded_at | mark_type ∈ {underwritten, actual, forecast, market_implied}; basis (IRR/MOIC/TVPI; gross/net); horizon; author; revision; base/down/up cases |
| `quote` | event | bid % of reference NAV, reference date, deferral, counterparty class, `conflict_flag`, external/internal |
| `hf_terms` (τ) | lot | notice, revocability, gates, dealing, lag, holdback, lock-up, side pocket, consents |
| `facility`, `owner_draw`, `forecast` | id; event | Covenants and syndicate; draw convention; P10/P50/P90 and the snapshot of u, a, NAV, regime |
| `overlay_trade`, `crif_row`, `csa` | trade; risk factor; CSA | Template, book, client, CRIF keys; threshold, MTA, IA, reuse, IM regime |

- **Hierarchy.** holding → group (PE, SECONDARIES, CAPSOL, COINVEST, PUBLIC, PRIVCREDIT, OVERLAY, plus CF as non-investment) → strategy → sub-strategy. Group roll-ups are views. Internal transfers carry `counterparty=intra_adic` and count zero toward liquidity raised, with fair value on both legs (GROUPS §4.1).
- **Generator SYN-ADIC-177** (GROUPS §6; gap_01 §8). Three layers:
  - **World:** regimes, factors, exit factor.
  - **Sealed truth:** skill $a_v=-0.05z_v+u_v$, GP effect, economic NAV, true μ, bias draws.
  - **Observation:** smoothed reported NAV; manipulation of the Barber–Gredil–Kaplan (BGK) type; underwriting $u=\bar\mu+0.3(\alpha-\alpha_s)+b^u+\gamma'x$; anchored forecasts $f_t=0.6f_{t-1}+0.4[\cdot]+b^f$; timing optimism after HY shocks; market-implied bids from the hedonic model with desk noise.
  - Census v1.0: ≈395 positions, ≈1,500 loans, ≈250 trades on 12 CSAs, $177bn. Releases R0 / R1 (1,000 worlds × 40 quarters on CRN) / R2 (200 history worlds).
- **Checks.** Gates V1–V23. Parameter recovery ±5pp. SBC rank uniformity: the prototype caught a fusion bug at χ²₁₉ = 207 against a critical value of 30.1 (GROUPS §6). Stylized facts: distribution rates within ±2pp of MSCI, AC1, secondary prices within ±3pp of Jefferies, private-credit loss 0.8–1.2%.
- **Labelling L1–L8 in code.** `SYN-` ids, `is_synthetic`, Parquet metadata, a footer on every chart and table, taint propagation, sealed truth, and a validator rule against attributing synthetic numbers to ADIC.
- **Adapters for real data.** `SourceAdapter.read(raw) → pa.Table → validate(schema) → load(bitemporal)`; unknown fields or units go to quarantine; each adapter has fixture contract tests. Order by data value: hedge-fund τ, PE unfunded by vintage, overlay blotter (CRIF), CSA terms, marks archive, facility documents, draw history. Synthetic sets stay frozen and separate once real data arrives (Brief §4).

---

## 8. Package layout and build order

`src/tpa/{contracts, registry, data, synth, scen, owner, priv, pub, overlay, beliefs, bridge, ledger, core/{sim, policy, certify, tree, h, phase1, duals, actions, safety, terminal}, robust, attrib, evaluator, lab, agents, ic}`, plus `cli.py` and `mcp_server.py`.

**Dependency order.** contracts → registry → data → {scen, beliefs, ledger} → {owner, priv, pub, overlay, bridge} → core → {robust, attrib} → evaluator → {lab, agents} → ic. Contracts freeze in week 2. Each stream builds against a golden mini-cube (200 paths) and a mini `FlowCube`.

**Parallel streams** (team of 4 [I]: 2 quant developers, 1 data/platform engineer, 1 validation quant at 50%): A data, synth, beliefs · B scen, owner, priv, pub · C ledger, core, robust · D evaluator, lab, agents, ic, overlay.

| Increment | Scope | Exit criterion |
|---|---|---|
| **1 · MVP slice (weeks 0–10)** | R0 census; E with M1 + M6 proxies (8 factors, 3 chains); simplified three engines; HF state machine (`hf_ladder.py` port); Level-1 overlay; reduced-form draw; full ledger with T4′ replica (`t1_engine` port) and CFP; P with the fixed rule policy at 10,000 paths; H at 500 × 8 with Phase I/II; λ, envelopes, 20 decision cards, module F; FBE on planted biases; bridge (`bridge.py` port); HTML pack v0; evaluator as a separate process; Memo Writer and claim validator on `ReplayBackend` | Six MVP questions answered end to end (00_SYNTHESIS §10); pinned-dual suites 8/8 and 18/18 ported; identities exact; perf assertions green; 100% labelling audit |
| **v1 (months 3–6)** | M1–M6 + held-out generator; production F_t harness; Level-2 overlay, SIMM-like engine, OV1–OV3, 2020 replay; robust + entropy pooling + reverse stress; DE/CMA-ES search + sealed certification; G0–G9 with live backends; 12-seat shadow IC; Shapley + `test_v8_replica`; H default 600 × 12; adapters for τ, unfunded by vintage, blotter | Gates V1–V23; SBC passes; sealed plane run once; shadow-IC offline suite passes (hidden-profile ≥ 80%) |
| **v2 (months 6–12)** | ADIC data in shadow mode; MRM validation; structural owner model; SDDP-lite on 24 Markov nodes only if the H–P ranking test fails; second model family if approved | Shadow recommendations logged against decisions; no unexplained gate breach |

**Test strategy.**

| Kind | Examples |
|---|---|
| Unit | Pricers against closed forms, put–call parity; WIS/CRPS; Benktander; SIMM worked example |
| Property (hypothesis) | Ledger identity Σ flows = Δcash for random flows; dual signs; DSL type rules reject look-ahead and horizon variables |
| Metamorphic | Wider discount must not raise discretionary SELL proceeds when liquidity is slack; costlier facility must not raise REFI volume; tighter band must not expand the feasible set; NAV scaling and relabelling invariance; penalties ×10 leave duals unchanged (0.0 change measured) |
| Regression | Golden manifests reproduce bit-for-bit; `test_v8_replica`; bridge reproduces verifier 10; gap_02 and GROUPS gap_01 fixtures |
| Reconciliation | H vs P replay; cohort vs asset; DVA sums to total; intra-ADIC transfers net to zero |
| Parameter recovery | SBC on the FBE, the regime HMM and the draw model; ±5pp recovery on SYN-ADIC-177 |
| Performance | §4.15 budgets asserted nightly |
| Agentic | Replay determinism; seeded-error drills; prompt-injection documents; admission κ ≥ 0.6 on ≥ 50 golden items |

---

## 9. Key choices versus alternatives

| # | Choice | Rejected alternative | Evidence |
|---|---|---|---|
| 1 | One ledger kernel shared by P, H and the stress test | Separate models per tool | "One model shared by simulator and optimizer" (00_SYNTHESIS §2.1); reconciliation tests (00_SYNTHESIS §8) |
| 2 | Group-recourse LP + small post-LP MILP | 12-quarter stochastic MILP, ≈1.8M variables, decomposed | "Tens of minutes on HiGHS" (00_SYNTHESIS §4.8); 1,000 × 12 LP in 90 s [PD-bench]; price-only rule $24.7m worse, so keep the MILP (00_SYNTHESIS §4.4) |
| 3 | HiGHS dual simplex, single thread, warm starts | IPM, CLARABEL, PDLP, parallel simplex | 12.6 s vs 41–51 / 62 / 594 / 20 s on the same LP; warm re-solve 0.05 s [PD-bench] |
| 4 | Asset-level simulation | Cohorts as the default | 10.9 s per 10,000 × 40 [PD-bench]; asset detail needed for cards (Brief §3) |
| 5 | HiGHS `feasibilityRelaxation` + `getIis` | Gurobi `feasRelax` | gap_02 §4 specifies feasRelax; HiGHS 1.15.1 provides both functions; closed-form tests ported |
| 6 | Regression terminal values + H–P ranking test | Markov SDDP (SDDP.jl) | No Julia (Brief §3); SDDP is Phase 2 in 00_SYNTHESIS §4.8 |
| 7 | Exact entropy pooling (JS console + Python twin) | Neural-operator surrogate | Conflicts with P1 (Brief §6); EP is exact (00_SYNTHESIS L11) |
| 8 | Closed-form/GLS FBE, SBC-validated | PyMC hierarchical model | PyMC not installed (Brief §6); SBC caught a GLS bug (GROUPS §6) |
| 9 | Out-of-process evaluator; typed tools only | Prompt rules or containers | Paper's isolation was "cooperative… not an adversarial sandbox" (Paper l.7489-7490); no Docker assumed |
| 10 | Monthly Taylor overlay; daily sub-steps in the stress module | Daily sub-steps on all paths | OV1–OV3 are defined in named stresses (gap_03 §8); P&L-explain gate (§9) |
| 11 | 2 workers, isolated challenger as an ablation only | 3 workers | Brief P9; 3 workers untested in the paper (13_paper_deepread.localcheck M5) |
| 12 | Regenerate-and-verify cubes; seal the final plane | Store every cube | 2.3 s per 10,000 paths; checksums bind code and seeds (Paper l.6915-6917) |
| 13 | Tail-oversampled 600-leaf tree; T6 certified in P | 2,000-leaf interactive trees | 286 s [PD-bench]; T6 is certified in P (00_SYNTHESIS §4.9) |

---

## 10. Risks, and what this proposal leaves out or defers

| Risk (most severe first) | Mitigation |
|---|---|
| **Dual instability from tree reduction and LP degeneracy.** λ is a vertex dual of a degenerate 600-leaf LP with group-level recourse, so FTP, hurdles and envelopes can jump between quarters or replications, which undermines L14 | Dual bands over 10 SAA replications; sign-flip flags; hysteresis; EWMA-published FTP; overnight 1,000/2,000-leaf cross-checks; H–P ranking and replay tests; unstable cards flagged, not hidden |
| Data dependency (τ, unfunded by vintage, marks archive) | Adapters ordered by value; the archive starts in increment 1; cards stay labelled SYNTHETIC until the data arrives |
| Shared misspecification across the six models | Held-out bootstrap generator; misspecification plane; model ranges lead every probability |
| Single model family at launch | Different-model reviewer; disclosure; correlated-seat treatment |
| Windows process isolation is weaker than containers | No file, shell or code tools for agents; per-request hash checks; read-only ACLs on engine and data |
| Performance creep as engines deepen | 2.5× reserve; nightly budget assertions |
| JS entropy pooling outside CI | In-browser golden self-test; engine recomputation for any logged number |

**Deferred.** SDDP; Benders for interactive 2,000 × 20 trees; licensed-SIMM and QuantLib reconciliation (v2); FX/CDX surfaces and hybrid copulas (data missing, gap_03 §10); structural owner model; deep-RL challengers; full HSMM; online IC trials (shadow mode only, 00_SYNTHESIS §6.6).

---

## 11. Brief section 5 decisions 1–21

1. **Time grid (§4.1).** Quarterly decisions and private engines; monthly market, hedge-fund and VM clock; P 40 quarters; H 12 (8–20). 10% = 10-year geometric TWR, nominal, gross of distributions; real, owner-IRR and 3/5-year views reported.
2. **State (§4.2).** Asset level, ≈390 units, 14.6 KB per path; cohorts only above 1,500 units.
3. **Scenarios (§4.3).** About 20 monthly factors; chains S, e, Z; M1–M6 plus two bootstrap families; planes frozen at G1.
4. **Private engine (§4.4).** RFT-TA v2, EV and competing-risks engines; economic vs reported NAV; drought via e, κ(e), Φ; beliefs as per-path $\bar\alpha_i$ plus a group-bias shock.
5. **Instruments (§4.6).** Kernel-priced; availability by regime; liquidity cost via break-even ℓ and the one-off premium $L_s$.
6. **Overlay (§4.8).** 90/72 floor ladder at 0.15–0.5% of NAV; exposure templates with DSR-gated α; VM by CSA; SIMM-like IM; OV1–OV3.
7. **Liabilities (§4.9).** Reduced-form draw on an opening-NAV basis; Mode B default; owner band as a priced option.
8. **Optimizer (§4.11).** Tree LP with Phase I/II, λ from Phase II only; Lagrangian scores; small MILP; module F.
9. **Policies.** Cushion-monotone rules (the deck's gate and hedge/amplify rules rewritten through c_t, F_t); MPC via H; DE/CMA-ES search; `PolicySpec` DSL.
10. **Objective (§4.12).** Lexicographic Tier 1A/1B, then J. T6 bands 0.5/1/2% and 2.5/5%; T7 2.5%; T9 2%/1%.
11. **Robustness (§4.13).** Ensemble first; KL η = 0.05 (0.01 for rare events); W∞ 0.5pp; reverse stress; in-house entropy pooling.
12. **Experiment layer (§5).** Hashed `RunManifest`; append-only registry; engine-side counting; DSR, PBO.
13. **Agents (§5).** Eight roles; strict typed tools; G0–G9; plain-Python state machine; search-only memory.
14. **IC module (§6).** Blind pre-vote protocol; grounded Q&A; client-side entropy pooling with an engine twin; decision log.
15. **Package (§8).** Layered DAG; frozen contracts; four streams; test matrix; exit criteria.
16. **Taxonomy (§7).** holding → group → strategy → sub-strategy; intra-ADIC transfers count zero; DVA by group; decisions at total-portfolio level.
17. **Group actions (§4.6).** Hedge-fund queues, P2S, private-credit back-leverage, single-asset co-investment sales, the PE corridor.
18. **Internal capital market (§4.10).** Pooled-SAA envelopes; undamped decision duals; EWMA FTP; desk quotes as evidence; contingent dry-powder budgets.
19. **Credibility (§4.5).** WIS registry; bias model with κ_g; information value only against the group's own class, at n_eff ≥ 20; pay decoupled from budget.
20. **Shadow IC (§6).** Twelve mandate seats plus Facilitator and AI Validator; A/B/C/D agenda.
21. **Synthetic data (§7).** SYN-ADIC-177 with three layers; planted mark biases plus a market anchor; V1–V23; SBC; taint labelling.

*SYNTHETIC – NOT ADIC DATA (all [I-calc] and [PD-bench] figures).*
