# Proposal PA: Quant-rigor first

**Angle:** start from the mathematics. Every module is a consistent piece of one controlled stochastic system, and every approximation carries a certificate or a test. **Date:** 2026-10-18. **Status:** candidate architecture for the design judge panel.

> **SYNTHETIC.** Every ADIC balance, probability and cost below comes from the working allocation, census v1.0 or design defaults. None of it is ADIC data. Numbers tagged **[M]** were measured for this proposal on a *structural proxy* of the here-and-now program: random SYNTHETIC data with the production sparsity pattern (§4.8.3).

**Citation keys.**
- SYN = `research/00_SYNTHESIS.md` v1.1; GROUPS = `research/groups/01_GROUPS_SYNTHESIS.md`; gap_0k = `research/addenda/gap_0k.md`; C1 = `research/clusters/C1_portfolio_math.md`; LC = `research/verification/13_paper_deepread.localcheck.md`.
- ver/x and lit/x = `research/verification/x.verify.md` and `research/literature/x.lit.md`; "paper l.N" = line N of the Sakana full text; brief = `design/00_DESIGN_BRIEF.md`; BP = the user's blueprint.
- [I] marks a design inference.

---

## 1. Thesis

ADIC is one partially observed, controlled Markov system Σ: a state, admissible actions, an exogenous law, a transition, an observation map and a lexicographic objective. Each laboratory module is either a component of Σ or an approximate solver of it.
- **Components.** The scenario generator *is* the exogenous law. The group engines, ledger, debt and overlay *are* pieces of one transition operator. The Forward Belief Engine *is* the belief state.
- **Solvers.** The here-and-now tree program H, the standing policy P and the terminal values. Each approximation they make sits in an error ledger with a certificate or a test.

The liquidity price λ is derived, not designed. It is the KKT multiplier of unencumbered cash in the restored, feasible program, normalised to a per-quarter premium. Corporate Finance publishes it as the FTP curve, paired with quantity envelopes read from the same solution.

Four further rules follow:
- feasibility before prices (Phase I);
- chance constraints certified in an exact simulator, never optimised;
- robustness as verification across disjoint model worlds;
- exact attribution, with the residual reported.

Agents never touch Σ. They propose typed points in its policy and scenario spaces; an out-of-process evaluator prices, counts and gates them.

## 2. Requirements and principles trace

| Req | Where | How satisfied |
|---|---|---|
| R1 multi-period | §4.8 | Four Powell classes: PFA standing policy (40 quarters), DLA tree program H (12 quarters, re-solved each quarter as MPC), VFA terminal values, CFA buffers |
| R2 robust scenarios | §4.10 | Six CMA worlds, a held-out generator and a misspecification ensemble, hashed before search; KL and W∞ tilts; reverse stress |
| R3 probabilities | §4.8.8 | Clopper–Pearson certification on fresh 50k paths per world; every probability shown as value, world range and MC error |
| R4 distribution | §4.7 | Exogenous owner draw D_y = d_yB_y (Mode B); T1 is a hard row, T7 is certified; Modes A/H and the band priced on common random numbers (CRN) |
| R5 10% target | §4.1, §4.9 | 10-year geometric TWR; Tier-2 objective J; P(10%) reported, never optimised; a bridge per world |
| R6 leverage | §4.6–4.7 | Portfolio and asset LEVER columns; T5 rows; leverage monotone in the cushion |
| R7 private, DPI | §4.4 | Engines driven by the exit state e_t (drought posterior 0.87 at t₀), with two clocks |
| R8 lens | §4.6, §4.8.5 | Actions are exact LP columns; LEVER ≡ ADD + REFI is a unit test; cards come from reduced costs plus forced re-solves |
| R9 three marks | §4.5 | GLS/Benktander fusion plus a market-implied anchor; validated by simulation-based calibration (SBC) |
| R10 overlay | §4.7 | Position layer with Greeks, VM by CSA, SIMM-like IM; OV1–OV3 as rows |
| R11 agentic | §5 | Deterministic state machine; eight role types; three engine-owned gates |
| R12 IC | §6 | Pack, 12-seat shadow IC, blind pre-vote, what-ifs, decision log |
| R13 deck | §4.9, §4.11 | Two tiers rebuilt as a lexicographic program; F_t inside P; v8 attribution kept as `test_v8_replica` |
| R14 groups + CF | §3, §4.4–4.6, §4.8.6 | Group tag on every position; group engines and instruments; envelopes and FTP; CF owns the cash rows and λ |
| R15 synthetic | §7 | Sealed-truth generator; parameter recovery; tainting SYNTHETIC label |

| Principle | Enforcing mechanism |
|---|---|
| P1 | The evaluator is the only source of numbers; the claim validator rejects any unregistered number; no execution API exists; humans vote |
| P2 | Out-of-process evaluator with read-only, hashed engine, scenarios, beliefs, cost models and metric definitions; manifests; a guarded-file check; a stale cache stops evaluation (paper l.7210); agent self-reports are diagnostics only |
| P3 | Search plane and final plane (fresh seeds, held-out generator, misspecification ensemble) hashed at G0, with separate caches; search sees bounded aggregates only (paper l.6825); calibration windows embargoed |
| P4 | Typed PolicySpec and ScenarioSpec bundles with rubrics; every call counted by the engine, failures included; ≤ 3 retries (paper l.6290); DSR, PBO, α-investing |
| P5 | Gate 1 correct, Gate 2 selection (ties keep the incumbent), Gate 3 qualification → `not_qualified` (paper l.6932) |
| P6 | HOLD, static SAA, v8 rules, target-chasing and a shuffled-signal placebo at 3/5/10 years; exact switch-off null; single-change ablations; disjoint selection and reporting seeds |
| P7 | "Resolves" is a deterministic registry check; "supports" is judged by a family-B auditor with logs and diffs |
| P8 | IC/CIO sign the AnalysisContract; agents only draft amendments |
| P9 | Plain-Python state machine; 2 shared-memory workers plus 1 isolated; per-campaign memory; escalation channel |
| P10 | Auditor and red team on model family B; any same-family fallback is flagged |
| P11 | Counter-based RNG keyed by (seed, world, plane, path, month, source, slot); manifests; pinned solver versions |
| P12 | Engine packages never import agent code (a layering test); stub and replay LLM backends |
| P13 | Prompts carry aggregates and IDs only; holdings stay local |
| P14 | Every card shows binding rows, a one-sided dual interval, the reduced cost, attribution and flip thresholds |
| P15 | Type system forbids time-to-go, scenario IDs and regime labels; policies see lagged observables; filters run on simulated observables |

## 3. System decomposition

Every module is deterministic except L8 and the shadow-IC seats.

| ID | Module | Responsibility: inputs → outputs | Owner | Feeds |
|---|---|---|---|---|
| D1–D3 | `data` | ADIC feeds or SYN-ADIC-177 → bitemporal, hashed, taint-propagating snapshots | CIO office data team; MRM audits | all |
| E1 | `scen` | CMAs and market data → law P_m (factor and regime paths in six worlds); trees for H | CIO office TPA desk; MRM validates | T, C |
| E2 | `state` | Observables → F_t and regime, exit and shock posteriors; initial state frozen at G2 | Risk (CRO) | C1, C2, IC |
| E3 | `liab` | Fiscal state, Brent, Z → owner-draw paths; modes A/B/H; payout-rule library | Corporate Finance (CF) | T5, C4 |
| T1 | `priv` | Positions, beliefs, paths → private cash flows and NAVs (cohort and asset level) | Private groups calibrate; TPA desk codes | T5, A2 |
| T2 | `pub` | HF lots and terms τ → cash shares φ_i(h, S); long-only NAV and impact | Public Markets | T5 |
| T3 | `ovl` | Blotter or families, surfaces → P&L, VM by CSA, SIMM-like IM, OV1–OV3 | Overlay; CF owns collateral | T5, C4 |
| T4–T5 | `debt`, `ledger` | Flows and facilities → cash identity, HQLA, ladder LR1–LR8, CFP stage | CF | C1, C4, C5 |
| B1–B2 | `beliefs` | Marks u/a/f, bids, registry → (μ̂, Σ̂), group bias, WIS scores | CIO office; CRO validates | T1, C4 |
| A1–A2 | `actions` | Positions, consents, regimes → admissible actions; exact column cash-flow vectors | Each group; CF for portfolio REFI/LEVER | C4 |
| C1–C3 | `sim`, `policy` | Policy and paths → path metrics; DSL → kernels; tuned θ; certified gates | TPA desk; CRO certifies | lab |
| C4–C7 | `opt` | State, tree, columns → actions, duals, λ/FTP, envelopes, Γ; F-projected proposals; terminal values | TPA desk computes; CF publishes FTP; Risk owns module F | IC, groups |
| V1–V4 | `robust`, `attrib`, `bridge`, `stats` | Policy metrics → world ranges and tilts; attributions; bridge; CP, MMW, DSR, PBO | Risk; CIO office; MRM | IC |
| X1–X3 | `lab` | Typed requests → counted, gated, hashed results; registries | MRM | agents |
| L8 | `agents` | Evidence slices → typed proposals, claims and views (§5) | CIO office under AI governance | X1 only |
| I1–I3 | `ic` | Registry → pack with client-side entropy pooling; ballots; DecisionRecords | IC secretary | humans |

The only outward interfaces are a typer CLI and an MCP server exposing X1's typed API.

## 4. Quant core

### 4.0 One system, one notation

| Element | Definition |
|---|---|
| Clock | Quarters t = 0…T; monthly engine sub-steps; daily overlay sub-steps in stress windows |
| State | S_t = (R_t, I_t, B_t): physical positions and ledger, prices and curves, beliefs (SYN §2.1) |
| Latent regime | ξ_t = (S_t, e_t, Z_t): macro × exit window × shock type; law P_m in world m |
| Observation | o_t, lagged: reported NAV one quarter, EBP and CPI one month |
| Beliefs | B_t = β(B_{t−1}, o_t): regime posterior, F_t, exit and shock posteriors, FBE posterior, group-bias posteriors |
| Policy | a_t = π_θ(o_{0:t}, B_t) ∈ A(S_t); no labels, no time-to-go (P15) |
| Transition | S_{t+1} = Φ(S_t, a_t, W_{t+1}), with Φ = Φ_ledger ∘ (Φ_priv ⊕ Φ_pub ⊕ Φ_ovl ⊕ Φ_debt ⊕ Φ_liab) |
| Objective | Lexicographic: feasibility, Tier 1A, Tier 1B, Tier 2 J (§4.9) |

**Module ↔ Σ ↔ test.**

| Module | Object in Σ | Test |
|---|---|---|
| E1 | P_m | 10-year compound return within 5bp of each world's CMA |
| E2 | β | Run on simulated observables; reliability |
| T1–T5, E3 | Pieces of Φ | Conservation to 1e-10 |
| B1 | Belief about μ_i | SBC |
| A1–A2 | A(S) | Homogeneity |
| C1 | Exact policy evaluation | The reference for everything else |
| C4 | Approximate t = 0 argmax | Certificate Γ, MMW gap |
| C5 | ∂V₀/∂cash | Finite differences |
| V1 | Alternative laws | Intersection–union test |
| V2 | Decomposition of J | Efficiency residual |

**Two structural properties carry the design.**
- **(P-H) Positive homogeneity.** Every position engine is homogeneous of degree 1 in the fraction held. A hedge-fund lot is homogeneous only while ADIC's request leaves the gate unchanged; otherwise it becomes a discrete column. Fractional SELL/REFI/LEVER columns therefore have exact linear coefficients: the engine's cash-flow vectors on CRN. Fixed actions enter the LP as right-hand-side updates.
- **(P-L) Linear ledger.** Cash, HQLA, NAV and encumbrance are linear in positions and flows. Nonlinearity lives only in four places, each handled in the error ledger (§4.12):
  - price impact (convex piecewise-linear cost);
  - covenants;
  - gates;
  - SIMM margin (a norm of sensitivities).

### 4.1 Time grid and the meaning of 10%

- **Grid.**
  - Decisions are quarterly and the engine monthly; overlay VM settles daily (T+1) in stress windows.
  - The owner sets an annual rate, paid in four instalments on opening-of-fiscal-year reported NAV, reset annually (SYN §4.7; gap_02 §1.1).
  - Simulation runs 40 quarters plus a terminal value; reporting windows are 3, 5 and 10 years; H looks 12 quarters ahead.
- **Target.** 10% nominal USD, measured as the 10-year rolling geometric TWR, gross of distributions and net of fees and financing:
  - Π_{t+1} = Π_t(W_{t+1} + d_t)/W_t;
  - R̄₁₀ = (Π₄₀/Π₀)^{1/10} − 1 (SYN §4.9, §9.3).
- **Also reported:** real TWR, NAV growth net of payouts, and owner IRR (accrued at 10%, report only).
- **Why J matches the target.** Tier 2 accrues distributions at the fund's own return, so W̃_T = W₀Π_T exactly and J is neutral to payout timing.
- **Arithmetic.**
  - Holding real NAV needs 7.9%, 10.8% or 13.9% at payouts of 5%, 7.5% or 10% (SYN §2.3a).
  - Evidence-central E[R] is 6.1–10.5% across worlds, 8.3% for the mixture (gap_05 §1).
  - 10% is therefore a target for reporting and for the bridge, never a constraint.

### 4.2 State representation and memory budget

| Block | Unit (census v1.0) | Floats per path |
|---|---|---|
| Fund interests | ≈90 cohorts (strategy × vintage bucket × region) × 6 states | 540 |
| Single companies | ≈130 assets × 4 states | 520 |
| Contractual claims | ≈55 cohorts or assets × 7 states | 385 |
| Hedge-fund lots | 40 lots × 8 machine states | 320 |
| Long-only, overlay, CSAs, ledger and debt | — | ≈85 |
| Beliefs | Regime, F_t, exit and shock posteriors, group bias, μ draws | ≈180 |

**Simulator footprint.**
- Each path carries ≈2,000 floats (16 KB). At 10,000 paths that is 160 MB of live state, plus 64 MB of outputs and ≈100 MB of factors, so peak memory stays under 1 GB. 50k-path runs go in 10k blocks.
- Work is ≈6×10¹⁰ flops plus the state machines: an estimated 10–30 s on 8 numba cores [I]. Benchmark gate B1 holds this to the brief's 60 s.

**Cohort exactness rule [I].**
- The fund engine is linear in (V, U) given cohort intensities. Aggregation is therefore exact when members share strategy, age bucket, region and β.
- Split a cohort until its first-order bound e_c = Σ_{i∈c} V_i(|∂cf/∂a|·|a_i − ā_c| + |∂cf/∂μ|·|μ̂_i − μ̄_c|) is ≤ 0.5% of the cohort's annual cash flow.
- Idiosyncratic shocks match the first two moments through σ_c = σ_id·√(Herfindahl of member weights).
- Asset detail is kept for actions (A2).

**Optimiser state.** Each H node carries ≈30 states: 10 cohort NAVs and 10 unfunded balances (5 groups × young/mature), cash, liquid book, revolver, NAV facility, wealth, synthetic beta, P2S, HF queue and the red-margin running maximum.

### 4.3 Scenario generator: the law P_m

- **Regimes and factors.**
  - Macro S ∈ {EXP, LATE, CRIS, RECV} follows a hidden semi-Markov model with negative-binomial dwell. The exit window e takes {O, N, D, F}; the shock type Z takes {N, B, SG, DB, SS, GW}.
  - About 20 monthly factors: f_t = c_S + Af_{t−1} + D_SL_Sε_t, with ε ~ t₅. Asset returns are r = a_S + b′f + σ_Su.
  - CMA anchoring is exact, world by world for M1–M6, plus a held-out block-bootstrap/FHS generator (SYN §4.1; C1 §5.10).
- **Oil and volatility.** Two-factor oil starts from the futures curve, and the Gulf-war dwell is conditioned on elapsed time. Implied-vol states include β(T) ≈ 0.94(T/30d)^−0.43, MOVE and OVX (gap_03 §3; gap_04 §6).
- **Owner demand.** The owner's fiscal state follows Brent and the shock type Z, and E3 maps it to the draw (§4.7). This is liability-side wrong-way risk, worst in demand busts.
- **Initial state, frozen at G2:** F_t = 0.10 against a 0.17 base rate; drought 0.87; Gulf war ≈0.85; 12-month draw $9.9–10.8bn (gap_04 §6).
- **CRN by construction [I].**
  - Every uniform is a pure function u = H(seed, world, plane, path, month, source, slot) of a counter-based generator. A policy change never shifts another draw; decision-dependent draws (sale success, gate hazards, CV offers) read pre-indexed slots.
  - HOLD serves as a control variate. Importance sampling on the regime chain covers p̂ < 0.5% (C1 §5.7).
- **Planes.** Search runs on M1–M6 with search seeds. The final plane holds fresh seeds, the held-out generator and the misspecification ensemble (§4.10). Calibration windows carry a 3-month embargo.
- **Belief-state trees for H [I].**
  - Stage 1 has 24 nodes: 6 worlds × 4 strata (benign, drought, crisis entry, and a tail stratum holding the top 2% of the facility-free funding gap G*), with exact stratum probabilities.
  - Children are drawn from the posterior predictive Σ_sπ_n(s)P(·|s), not from the regime that generated the path, so a node carries only observable information. Partially observed programs need a belief state (lit/10 backfill 3).
  - Reduction respects the filtration distance (backfill 4) and must pass out-of-sample A/B tests (lit/01_mpo §5).

### 4.4 Private engines per group

| Group | Engine | Mechanics and defaults |
|---|---|---|
| PE | Fund-interest RFT-TA v2, cohorts | Effective age advances at κ(e) = 1.2/1.0/0.6/0.5. Calls (1 − e^{−λΔ})U with λ = λ̄(a)m^C(e). Distributions (1 − e^{−δΔ})Ve^rζ with δ = δ̄(a^e)exp(κ^DX − θ_GG). Reported-NAV AC1 0.66–0.71. m^D 1.25/1.0/0.45–0.50/0.30–0.35. Stressed calls λ(U − B^SL) + c^SL·B^SL (SYN §4.2) |
| Secondaries | Three templates | LP interest with V₀ = θN^ref; secondary-fund layer (calls 45% a year, NAV peak ≈65%); CV stake on the EV engine. Deferred payables count as debt (GROUPS §3.2) |
| Co-investment | EV per company | E = max(V − D, 0); write-off at V ≤ κD; Weibull exits (k 1.447, η 7.70 years) × 1.3/1.0/0.5/0.3; P(MOIC < 1) 0.35–0.40 (GROUPS §3.4) |
| Capital Solutions | Claim state machine | Accrual C ← C + qa; NAV loan B′ = B + (I − D)⁺ − σ(ℓ)(D − I)⁺; PIK share 15/30/60–80/20%; default 1.0/2.5/6–8/1.5% (GROUPS §3.3) |
| Private Credit | Competing-risk cohorts plus wrappers | h^def = φΦ(−ln ICR̄/σ)ξe^{β′x}; separate PIK and extension hazards; DDTL draws; LGD 0.67, PD_N 1.1% (GC1 pair kept as a truth variant; GROUPS §3.6) |
| Public Markets | Factor model plus state machine | States LOCK…TRS_TERM. The P5 cash share φ_i(h, S) is the only interface to the ladder. Long-only impact Yσ√(Q/V) (GROUPS §3.5) |

Fused beliefs enter as per-path draws of ᾱ_i plus a common group-bias shock. Kalman learning inside the simulation gives HOLD its information value (SYN §4.3).

### 4.5 Belief fusion: three marks plus a market anchor

- **Basis.** The forward log return on nowcast economic NAV, net of fees. Since-inception IRR is sunk and shown greyed out (SYN §4.3).
- **Signals.** Each signal reads s_{ij} = α_{j,g} + μ_i + ε_{ij}, with ε_i ~ N(0, Ω̃_g) and a shared outcome-noise term:
  - f, the group forecast;
  - u, underwriting (single deals only; it expires after T_u + 1);
  - a, the actual (shrunk; ignored before year 3);
  - m, market-implied.
- **Posterior (GLS).**
  - μ̂_i = Λ_i^{−1}(m_kσ_k^{−2} + 1′Ω̃^{−1}(s_i − α̂)), with Λ_i = σ_k^{−2} + 1′Ω̃^{−1}1 and non-negative weights.
  - Fund interests use Benktander credibility instead: c*U_CL + (1 − c*)U_BF, with a prior frozen at inception and fused with the forecast only.
- **Market-implied anchor (BP graft 1).**
  - From an external bid p, solve pN^ref = Σ_t E_b[CF_t](1 + y)^{−t} on buyer cash flows.
  - Its bias is the buyer–seller PME gap by fund age: +24.5 / +3.0 / −0.8pp (SYN §7.1).
  - The Secondaries desk contributes only scored distributions of *external* prices, never quotes where it may bid (GROUPS §4.2).
- **Credibility per group.** Forecast precision is 1/(κ_g²σ̂²), with κ ~ lognormal (median 1.75) until scored. Bias priors b^f are PE +3.0, Co-investment +3.5 and hedge funds +2.0pp. A forecast enters once (GROUPS §5).
- **Use.** Tier 2 takes posterior means; Tier 1 takes P10 with group bias at +2 sd.
- **Validation.** SBC and parameter recovery within ±5pp (V16–V18). The prototype SBC already caught a fusion that ignored correlated errors: χ²₁₉ = 207 against 30.1 (GROUPS §6).

### 4.6 Action economics per group

Actions combine two primitives, exposure and financing; LEVER ≡ ADD + REFI is a unit test (SYN §4.4). REFINANCE means cash-out and LEVER means exposure-up, as the user confirmed.

| Group | SELL | HOLD | REFINANCE | LEVER / ADD | Lag; availability |
|---|---|---|---|---|---|
| PE | LP sale at a hedonic price: buyout 91%; crisis 0.80–0.84 of economic NAV | GP-triggered CV offer (exogenous) | LP-portfolio NAV facility (CF) at SOFR + 300bp, LTV 10–20%; preferred at 12% | Re-ups; pacing corridor (Green 0.75–1.25×, Amber 0.25–0.5×) | 3–6 months; success 0.75–0.85 / 0.6 / 0.4–0.5 by regime |
| Secondaries | Tertiary or CV-stake sale | Deferred payables count as debt | LP-level facility; CFO | Buy iff b* ≥ p^ce after a 4.2–5.1% winner's curse; contingent budget only | ≤ 12 months |
| Co-investment | Buyer-model bid: 71–79% normal, 56–65% drought | Hold | Pool facility at SOFR + 450–750bp; single-asset REFI inadmissible | Holdco PIK in benign states only (wipe-out risk 7.0% → 22.8%) | 3–9 months |
| Capital Solutions | Syndication; secondaries at the yield mark less 8–12% (normal) or 20–30% (crisis) | Amendment policy | Back-leverage D/E ≤ 0.5, with a cash-carry row; CFO | Contingent new money | Close to 6 months; thin in crisis |
| Private Credit | Loans at 0.99 / 0.96 / 0.85 of par; prorated tenders | SMA run-off (≈$0.8–0.9bn in year 1) | SMA back-leverage at S + 200–275bp | Only if EL < y_A − c_B | Days to 4 months |
| Public Markets | Redemption as a queued, irrevocable SELL; HF secondaries at 15–50% discount | Hold | Long-only P2S: 0.40–0.70% a year per $ freed (2.2–3.3% in stress); $1.65bn VM per $5bn in a −33% month | Portable alpha; HF-TRS (≈2 survival months) | Long-only 1–7 days; HF 3–24 months |
| Overlay | Monetise iff V(1 − ba) + λ^wΔL ≥ continuation | — | — | Synthetic beta ≤ 1.30× | 1–7 days |
| CF | — | — | Revolver at SOFR + 85bp drawn, 15bp undrawn; 0% credit in 30-day rows | Facilities, repo | ≤ 3 months |

Sources: gap_01 §3; GROUPS §3.

**Admissibility A(S_t).**
- Each action carries a consent probability and a lead time.
- At most one lens action per asset per quarter.
- HF notices only on notice dates.
- LP-accessible instruments only (gate V23).
- Intra-ADIC transfers raise zero liquidity and are never optimiser variables (GROUPS §4.1).

One kernel prices every column.

### 4.7 Leverage, overlay and liabilities

- **Leverage.** Hard rows:
  - recourse debt ≤ 10% (target) / 15% (hard);
  - economic exposure ≤ 1.30×;
  - encumbrance ≤ 15/20%;
  - pledges ≤ 20% of private NAV;
  - ≤ 20% of debt maturing in any 12 months.
  Covenant probabilities are certified in P. Portfolio LEVER needs Tier 1 to pass with the debt included (SYN §4.5).
- **Overlay.**
  - *Instruments and margin.* Level-1 family exposures in the MVP; Level-2 templates on arbitrage-free surfaces later (equity SSVI first). The Taylor P&L is used only where the explain test passes (Spearman > 0.80, KS < 0.09). VM by CSA follows C* = sgn(V)(|V| − H)⁺. SIMM-like IM comes from the same sensitivities, with a deferred step after stresses (gap_03 §2, §7).
  - *Inside H.* Overlay positions are root columns, and their VM/IM coefficients at each node come from the position layer. OV1 (NV^eq_overlay(s) ≥ 0.75·NV^eq_tail(s)) and OV2 (−P&L_opp(s) ≤ 0.25·P&L_tail(s)) are linear rows given pre-computed stress revaluations. Exact SIMM IM and OV3 are norms: H linearises them conservatively, and module F re-checks them exactly (gap_03 §8).
  - *Valuation.* Opportunistic α is credited only if DSR ≥ 0.95. The tail hedge is valued as carry plus liquidity value E[Σδλ^wΔL] plus enabling value Σ_kη_kΔslack_k (SYN L5).
- **Liabilities.**
  - Draw rule: d^tgt = Π_[5%,10%](7.5% + 0.625·FN); smoothed d_y = Π(0.5·d_{y−1} + 0.5·d^tgt).
  - Owner overrides occur 0.25–2% a year; the draw base is opening reported NAV (SYN §4.7).
  - Mode B is the default. The owner band activates in 12–22% of paths and cuts the premium of the cheapest certified mix from 62bp to 21bp (gap_02 §2.3).

### 4.8 Optimiser

#### 4.8.1 Policy classes

| Class | Instance | Role |
|---|---|---|
| PFA | Standing policy π_θ, ≈20 parameters, cushion-monotone; v8's rules frozen as a comparator | Simulable 40-quarter policy, certified in P |
| CFA | H with tuned CVaR buffers b^red, b^floor | Makes H's decisions pass T6 and Tier 1B in P |
| DLA | Tree program H, re-solved quarterly (MPC) | This quarter's actions, λ and envelopes |
| VFA | Terminal values ω_c, ψ_c (regress-later); SDDP in Phase 2 | Removes the horizon |

**Standing-policy rules** (gap_04 §4.3):
- reserve: HQLA*/W = θ₁ + θ₂P(e ∈ {D, F}) + θ₃F_t;
- leverage: clip(θ₉ + θ₁₀c_t − θ₁₁F_t, 1, 1.3);
- hedge ratio: clip(θ₁₂ + θ₁₃F_t − θ₁₄c_t, 0, H^max);
- pacing with a stage cut; a fixed waterfall; a de Finetti top-up.

The cushion is c_t = min_{h≤24}[CBC^{TPF}_{s*}(h) − NCO_{s*}(h) − 0.04W(h) + g_t]/W_t (gap_02 §4).

#### 4.8.2 The here-and-now program H

H is written node-wise on a tree: nodes n with parent p(n) and probability p_n, leaves ℓ, worlds m.
- Root actions x₀ set the post-action state σ₀ = σ̄ − A₀x₀.
- Each node carries recourse y_n (sales by cohort and tier, draw/repay, long-only trades, monetisation, pacing), a state σ_n and a running maximum R_n.

**Objective:** max Σ_ℓ p_ℓ[Û(W̃^real_ℓ/W₀) − λ^H_Tψ̂(1 − W̃_ℓ/W̃*)] − Σ_n p_nκ_n′y_n, subject to:

- **(H1) Transition.** σ_n = Φ_nσ_{p(n)} + B_ny_n + c_n + Δ_n. The rows are generated by the simulator's own Φ code. Δ_n holds the exact cash flows of asset actions already fixed.
- **(H2) Node limits.** G_nσ_n + K_ny_n ≤ g_n − g^rec_n: the 4% IG floor, leverage, encumbrance, LTV by regime and depth caps. g^rec is the Phase-I glide path.
- **(H3) Red margin.** R_n ≥ R_{p(n)} and R_n ≥ g^red(σ_n), a sparse running maximum.
- **(H4) T6 surrogate per world class.** η_m + (1/ε′)Σ_{ℓ∈m}p_{ℓ|m}z_ℓ ≤ b^red_m, with z_ℓ ≥ R_ℓ − η_m, z ≥ 0 and ε′ = 1 − (1 − ε)^{12/20}, i.e. 0.60% at ε = 1% (C1 §5.4). CVaR is taken on the *signed* margin (ver/01_mpo R5).
- **(H5) Tier-1B surrogate.** CVaR₁₀%(−NPV_{12q}) ≤ b^floor in the worst world.
- **(H6) Root rows.**
  - T3 30-day coverage, with facilities credited at 0%.
  - T4′ ladder at 3, 12 and 24 months under s*(0.76) with hashed conventions. The coefficients are finite differences of the deterministic ladder, re-verified exactly at the solution.
  - T5, T8, LR4 and LR8, OV1 and OV2.
- **(H7) Non-anticipativity** holds by construction: one decision per node.

**Default tree.** Branching 24 × 4 × 2 × 2 is exact through Q4, with 384 Q4 nodes. Each Q4 node ends in a 3-leaf fan covering Q5–Q12 in four semiannual periods. That gives 1,152 leaves, 8 periods and ≈5,300 nodes. The only clairvoyance left sits inside the year-2–3 fans, and A9 measures it.

#### 4.8.3 Counts and measured solve times

H is kept sparse on purpose:
- the only dense rows are one CVaR row per world, which interior-point methods absorb cheaply;
- every other row is node-local;
- no column links all scenarios.

A "fan" formulation was also measured. Its dense linking columns (scenario-specific root cash-flow vectors, shared decision-rule slopes) made it slower at half the size **[M]**.

| Configuration | Leaves × periods | Columns | Rows | Non-zeros | HiGHS IPX, cold | CLARABEL | Warm dual simplex |
|---|---|---|---|---|---|---|---|
| Dense-column fan (rejected) | 300 × 8 | 48k | 61k | 0.84M | 26 s (simplex > 300 s) | — | — |
| What-if | 400 × 8 | 95k | 83k | 0.36M | 9–53 s | 11 s | 2.8–4.8 s after re-fixing 10–30 root decisions (cold: 46–52 s) |
| **Quarterly (default)** | 1,200 × 8 | 227k | 202k | 0.86M | **53 s** (94 iterations; 97 s with explicit path-max rows) | 98 s | ≈5 s [estimate] |
| Extensive form, large | 1,200 × 12 | 419k | 356k | 1.56M | Not converged in 300 s | — | — |
| Extensive form, large | 2,000 × 8 | 359k | 321k | 1.36M | Not converged in 300 s | — | — |
| One stage-1 subtree | 48 × 12 | 17k | 14k | 62k | 1.2 s (simplex 2.3 s) | — | — |

*Notes.* SYNTHETIC proxy; HiGHS 1.15.1 via `highspy`, CLARABEL 0.11.1. The machine (Core Ultra 9 285HX, 24 cores) was ≈100% loaded by unrelated jobs, so times are noisy and pessimistic; a smaller laptop may be 1.5–3× slower. Production adds ≈20–25% columns.

Counts scale as:
- columns ≈ |𝒩|(n_σ + n_y + n_u) + 5|ℒ| + n₀;
- rows ≈ |𝒩|(n_Φ + n_G + 2) + 20|ℒ| + |M| + n_root.

**Quarterly run budget** [M + I]:

| Step | Time |
|---|---|
| Phase I-a | < 1 s |
| Phase II, cold IPX plus crossover | ≈1 min |
| 2–4 warm selection re-solves | ≈5 s each |
| 4 warm finite-difference re-solves | ≈5 s each |
| **Total** | **≈1.5–2 min**, within the brief's target |

**Larger trees.** Beyond ≈1,200 × 8 the extensive form does not converge in 300 s. So the 2,000-leaf × 12-quarter configuration runs overnight, by resource-directive Benders over the 24 stage-1 subtrees:
- the master allocates each world's CVaR budget across subtrees, which is exact for LPs;
- subproblems take ≈1–2 s and run in parallel;
- estimated total: 1–3 minutes on 8 processes [I, extrapolated].
This is a Phase 1 deliverable.

**Engineering.**
- Matrices are assembled in scipy.sparse and passed to `highspy`. Its build provides IPX, crossover, `setBasis`, `getRanging`, `feasibilityRelaxation` and `getIis` **[M]**.
- cvxpy is kept for small problems; canonicalising 10⁶ non-zeros through it would be avoidable overhead.
- Money is expressed in W₀ = 1 units, and penalties stay ≤ 10⁴.

#### 4.8.4 Phase I: feasibility before prices

- **Phase I-a (seconds).** A lexicographic minimum violation of the hard deterministic rows (T1 over the s* ladder, T2 at 4%, T3, T4′, T8):
  - u*_k = min Σ_{r∈𝒯_k}w_ru_r s.t. Ax + u ≥ b, x ∈ 𝒳_rev, u_{𝒯_j} ≤ u*_j + δ for j < k.
  - 𝒳_rev is the set of reversible levers: facilities, pacing, a band request, the reserve, amber sales and HF notices. PE sales are excluded; T5 and legal rows stay hard (gap_02 §4).
  - It is implemented with `feasibilityRelaxation` per tier (rows relaxable, column bounds hard). `getIis` gives the irreducible infeasible subsystem; the Farkas ray is stored as the infeasibility certificate.
- **Phase I-b.** The same on (H4)–(H5), run only when a screen fails: the CVaR rows at HOLD with every reversible lever at capacity.
- **Phase II.** The restored problem uses the glide path g_{r,t} = u*_r(1 − t/T_rec)⁺, with T_rec = 4 quarters (8 with the Board).
  - λ is read only from Phase II.
  - Phase-I duals are shown as "infeasibility prices" and never reach the FTP curve or a card.
  - The contract is signed in RECOVERY.
- **`test_no_pinned_duals`, extended** from gap_02 §5:
  - no pricing row slack and no penalty-pinned dual;
  - duals invariant to ×10 penalties;
  - a reservation-price floor;
  - cushion ≥ 0;
  - the Phase-I closed form;
  - new: μ_n − M_n > 0 at every pricing node (§4.8.6).
- **Why.** A pinned dual of 100 prices every fund as a SELL at 0.9% of NAV. After restoration the dual is 0.237 and the reservation price 76.8% (gap_02 §4).

#### 4.8.5 Asset decisions: column generation with a certified gap

- **Restricted master.** H with cohort pro-rata root columns. These are convex combinations of asset columns, so the master is a restriction of the asset-fraction LP.
- **Pricing.**
  - For each candidate column j (asset, action, size), A2 computes its exact node cash-flow vector on the tree with CRN.
  - Its reduced cost is r_j = c_j − y′A_j. Duals apply to the column's direct coefficients only (SYN §4.4).
- **Level B (integer restoration).**
  - Maximise Σr_jx_j over semicontinuous asset actions (minimum tickets, consents, at most one action per asset).
  - Subject to ≤ 30 aggregated coupling rows: Q1–Q8 liquidity, T4′, leverage, encumbrance, pledges, envelopes, depth.
  - HiGHS MIP solves it in seconds.
  - Its LP relaxation splits at most one asset per binding row, with gap ≤ (m + 1)·max_iρ_i (ver/01_mpo R7; dossier 08). The split assets form the IC's marginal-asset agenda.
- **Fix and re-solve.** Selected actions enter H as exact right-hand-side updates, which add no density. Warm dual simplex; at most 5 iterations with dual damping 0.5.
- **Certificate on every run.**
  - Γ = [z_RMP + Σ_ju_j(r_j)⁺] − z_fixed ≥ z*_MILP − z_fixed ≥ 0. This is the Lagrangian (Farley) bound of column generation.
  - Accept if Γ ≤ 5bp CE; otherwise label the cards "selection not certified".
  - Prices alone are not enough: in a 40-asset test they matched 36 of 40 decisions but cost $24.7m (SYN §4.4).

#### 4.8.6 Duals → kernel → λ, FTP and envelopes (Corporate Finance as the internal bank)

- **λ from the KKT conditions.**
  - Stationarity of node cash gives μ_n = (1 + r_f)Σ_{c∈ch(n)}μ_c + M_n. Here M_n = Σ_{r∈ℛ_c}a_{r,C_n}y_r is the dual mass of the liquidity rows that contain cash (IG, coverage, survival, red margin, ladder).
  - So ℓ_n = M_n/(μ_n − M_n). This is SYN §4.4's ℓ = M/(π^H − M) with π^H ≡ μ_n, now derived rather than asserted. It does not read zero when only the IG floor binds.
- **Kernel.** π_n = p_nm_n∏_{k∈path(n)}(1 + ℓ_k)^{−1}, where m prices the α* funding basket at par. Without m, a worked SELL flips by $72m (SYN L1).
- **Published prices.**
  - λ^spot is ℓ at the Q1 nodes, by regime class.
  - FTP(h) = (E_π̂[∏_{k≤h}(1 + ℓ_k)])^{1/h} − 1.
  - The one-off premium L = π₀/π̄ − 1 applies to deal NPVs (17.5–23.7%).
  - Decisions use undamped duals. The published curve is an EWMA with a ±50% collar; performance charges are vintage-locked, and CF holds the mismatch (GROUPS §4.3).
- **Dual quality.**
  - One-sided derivatives V′(b ± δ) by warm re-solves. If they differ, the cards show the interval and the label "at a kink".
  - RHS ranging gives each price's validity interval.
  - Bootstrap bands over ≥ 5 trees.
  - H–P agreement: ∂J/∂cash₀ in P against λ^spot.
- **Envelopes.**
  - Λ^k_g = Σ_{i∈g}a^k_i(x*) for each coupling row, with ranges across trees.
  - Why prices alone fail (the rigorous form of L14): at an LP optimum each group's Lagrangian subproblem usually has a face of maximisers, so prices cannot select the optimal vertex (Baumol–Fabian). The envelope selects it.
  - A request above the envelope is priced at λ_k only inside the ranging interval, with Σ_ga^k_gδ⁺_g ≤ slack_k. Beyond it the TPC re-solves (GROUPS §4.4).

#### 4.8.7 Lagrangian action scoring and decision cards

**Score.** Score(i, a) = r_j − κ^irr − κ^GP − κ^tc. The reading rules (GROUPS §3.0):
- SELL iff p^ce > (LAPV(HOLD + best REFI) + charges − relief)/NAV;
- REFI iff s_B + f/T + λ_Lev + the covenant charge < ℓ̄_[0,T] (the test is ρ > s, not ρ > r_f + s);
- LEVER iff ADD and REFI both pass.

**Cards show** the reduced cost with its dual interval; flip thresholds (reservation price, break-even return, break-even ℓ); P(best) and regret across trees and worlds; the belief card; consents; envelope use; and `priced_on`.

**Forced re-solves.** The top 20 cards and every marginal-agenda asset get a forced-action re-solve. If it differs from r_j by more than 2bp CE, the card is flagged "second-order effects material".

#### 4.8.8 MPC, module F, policy search and certification

- **Quarterly MPC.** Freeze the state (G2), then run Phase I, H, Level B and the certificates. Finish with module F: a^safe = argmin‖a − a^prop‖²_Q s.t. ĝ_k(S, a) ≤ −δ_k.
  - Module F's gradients come from duals, checked by finite differences, with exact SIMM and OV3 re-checks.
  - Every proposal (optimiser, agent or IC) passes through F, which records what changed (C1 §5.13).
  - Between quarters, the CFP playbook and the standing policy act.
- **Policy search.** CMA-ES, implemented in-house in numpy (`cma` is not installed), on 10k CRN paths per world.
  - Tier 1 enters through an augmented Lagrangian.
  - Type rules are sign constraints: ∂f/∂c ≥ 0, and no size rule may increase in past losses except through c_t.
  - Successive halving saves ≈3.9× (SYN §5.4).
- **Certification.** Freeze θ and run fresh 50k paths per world plus the held-out generator.
  - A gate passes iff the one-sided 95% Clopper–Pearson bound is ≤ the class band. At 50k paths, p̂ = 0.90% passes a 1% gate and 1.00% fails (C1 §5.7).
  - Importance sampling below 0.5%.
  - The optimism gap and the number of policies tried are reported.
  - HDP-in-the-loop on 200–500 paths measures the PFA–MPC gap.

### 4.9 Objective and constraints: the two tiers as a lexicographic program

| Level | Content |
|---|---|
| 0 | Feasibility: u* = 0, or RECOVERY on a glide path |
| 1 (Tier 1A) | T1 payout (instalment ≥ max(5%B_y, owner call), annual ≤ 10%B_y). T2 IG + cash 8% elastic / 4% hard. T3 30-day coverage (ADIC-LCR 2.10×). T4′ = s*(0.76) survival for 24 months. T5. T6 red event ≤ 0.5/1/2% (M1–M5 and the mixture) and —/2.5/5% (M6 class). T7 ≤ 2.5%. T8. T9 (SYN §4.9; gap_02 §3) |
| 2 (Tier 1B) | Mixture median R̄₁₀ ≥ 7% and worst-world CVaR₁₀% ≥ 0% |
| 3 (Tier 2) | J = Σ_mw_m{E_m[U₃(W̃^real₄₀/W₀)] − λ_T(E_m[(1 − W̃₄₀/W̃*)²₊])^{1/2}}, with γ = 3, λ_T = 1 (swept 0–2), W̃* = W₀·1.10¹⁰ |

**Improvements over v8 and v1.1.**
1. **Tolerance cascade.** While optimising level k + 1, level-k metrics may degrade by at most one paired standard error. Tier-2 gains therefore never come from statistically invisible Tier-1 erosion, and ties keep the incumbent (paper l.6823–6824).
2. **Probabilities are certified, never optimised.** H carries conservative CVaR surrogates: CVaR_{1−ε}(g) ≤ 0 implies P(g > 0) ≤ ε (Nemirovski–Shapiro; dossier 01_mpo). Their buffers are tuned until H passes in P.
3. **No gambling.** No indicator terms; shortfall exponent 2; cushion-monotone type rules; the gambling detector G1–G4 (C1 §5.7).
4. **Time consistency disclosed.** Quarterly re-solves drift effective risk aversion (lit/01_mpo §4.5). A horizon-invariance test (T_H = 8/12/16) checks root actions and λ.
5. **Robust-satisficing reading.** "The floor holds within δ nats of the mixture, losing k_MS·δ" (lit/10 backfill 1).

v8's floor needs a 15.8–17.9% expected return, so it is retired. Maximising P(10%) buys a toy 4.6% chance of a loss above 40% (SYN §4.9, L9).

### 4.10 Robustness as verification across model worlds

- **Worlds, hashed at G0.**
  - Search: M1–M6 (JPM 2027, BlackRock fee-adjusted, AQR, JPM drought, JPM stagflation, BlackRock risk-premia-rise).
  - Final: fresh seeds and the held-out generator, plus a misspecification ensemble: K = 3/5 or jump regime models; Φ = 0.75; GC1's PD/LGD pair; adverse HF terms τ; a log fiscal map; and fixed-USD draws.
- **Qualification is an intersection–union test.** A recommendation qualifies only if all three hold:
  1. Tier 1 passes in every world under its band.
  2. It is non-inferior to HOLD in every world, aggregated on the worst.
  3. The one-sided 95% paired lower bound on ΔJ exceeds the pre-declared materiality (overlay 3, pacing 5, REFI/LEVER 10, SELL 15bp CE) for the mixture and is positive in ≥ 2 worlds, Holm-adjusted across finalists.

  Anything else is NOT_QUALIFIED (SYN §5.4; paper l.6926–6933).
- **Tilt layer: one exponential family (SYN L11).**
  - KL worst cases at η = 0.05 (0.01 for rare events).
  - W∞ shifts of 0.5pp for fee and smoothing bias.
  - Breakdown divergence η* and k_MS.
  - Reverse stress: the minimum-KL tilt to failure, plus red-team ScenarioSpecs that must beat GW → SG → DB.
  - IC views use the same solver, gated by KL flags (0.05 / 0.25 / 1.20 / 2.30 nats) and Kish ESS ≥ 5,000 (SYN §6.4).
- **No DRO inside H.** Its radius cannot be elicited, and providers are confused 25–38% of the time. Model dispersion (3–4pp) dwarfs Monte Carlo error (0.2pp), so the ensemble is the first-order layer (SYN §4.10, L11).

### 4.11 Exact attribution

1. **Components.** Exact Shapley values over ≤ 6 components (64 coalitions) on CRN, with 50k paths. Efficiency Σφ_c = v(N) − v(∅) holds by construction. Each value is reported with its Monte Carlo SE and an anticipation audit (gap_05 §8).
2. **Switch-off null control.** In the paper, scaffolding supplied 55.8% of the margin and the learned increment reversed sign (paper l.2657–2663). Ablations change only the declared component (paper l.6561).
3. **Group dollars.** DVA_g = Σ_{i∈g}NAV_i(r_i − r^FB_i) − FTP^vint_g − λ_RRC_g + CR_g, summing to NAV₀(R_P − R_RP) with the residual reported (GROUPS §4.3).
4. **What moved H.** An Aumann–Shapley path integral of duals from last quarter's inputs to this quarter's: ΔV = Σ_k∫₀¹∂V/∂θ_k(θ₀ + τΔθ)Δθ_kdτ, on 16 warm re-solves. The LP value is piecewise linear, so only grid error remains, and it is reported.
5. **Hedges.** Carry, liquidity value, enabling value and a residual.

v8's +3.5pp survives only as `test_v8_replica`; in the new engine it is +0.35–0.61pp.

### 4.12 Error ledger and consistency contract

| # | Approximation | Certificate or test | Acceptance | If it fails |
|---|---|---|---|---|
| A1 | Monthly engine | Daily VM sub-steps; 2008/2020/2022 replays | 30-day need within 5% | Daily steps on stress paths |
| A2 | Cohorting | First-order bound; asset vs cohort on 2,000 CRN paths | ΔP(red) ≤ max(0.1pp, 2 SE); ΔCE ≤ 2bp | Split cohorts |
| A3 | Taylor overlay P&L | Explain test | Spearman > 0.80, KS < 0.09 | Full revaluation |
| A4 | Tree reduction | Mak–Morton–Wood gap over ≥ 5 trees; A/B stability | ≤ 10bp CE; root actions stable in 4 of 5 trees | More leaves |
| A5 | Semiannual years 2–3 | Quarterly 12-period overnight solve | Same root actions; Δλ^spot ≤ 10% | Quarterly grid |
| A6–A7 | Cohort master; integer restoration | Γ; (m + 1)·max ρ_i | Γ ≤ 5bp CE | More columns or iterations |
| A8 | PWL utility | Tangent bound h²·max\|U″\|/8; exact U at the solution | ≤ 0.5bp CE | More tangents or a power cone |
| A9 | Fan clairvoyance | H's root evaluated out of sample in P; 1-leaf-fan variant | Root unchanged; optimism gap reported | Deeper tree |
| A10 | CVaR for chance constraints | Conservative; CP certification in P | P passes | Raise buffers |
| A11 | Terminal values | Horizon invariance; out-of-sample R² | Root stable | Longer horizon or SDDP |
| A12 | PFA class | HDP-in-the-loop | Gap ≤ 10bp CE | Enrich the DSL |
| A13 | Filters | Frozen filter on simulated data; reliability | Within bands | Recalibrate |
| A14 | Module F | Finite-difference gradients; exact re-check | Zero violations | Iterate |
| A15 | Client-side EP | ESS and KL gates | ESS ≥ 5,000 | Re-simulate |
| A16 | Monte Carlo | CP intervals, paired SEs, importance sampling | Every number carries its SE | More paths |

**Consistency contract** (CI on fixtures; nightly on the book):
- conservation to 1e-10, and intra-ADIC netting = 0;
- homogeneity;
- H's rows reproduce the simulator's cash path to 1e-9;
- duals lie inside their finite-difference interval;
- penalty invariance;
- μ − M > 0;
- H–P agreement on λ^spot and on action rankings;
- HiGHS–CLARABEL agreement;
- LEVER ≡ ADD + REFI;
- metamorphic tests: a wider discount gives no more SELL when liquidity is slack; a costlier facility gives no more REFI; a tighter band never enlarges the feasible set (SYN §5.5).

## 5. Agentic layer (minimal, in service of the mathematics)

An agent may emit only a typed object the evaluator can price:
- a column (PolicySpec or ColumnSpec);
- an alternative law (ScenarioSpec);
- a moment constraint (ViewSpec);
- a draft contract amendment;
- a claim bound to registry IDs.

| Role | Output | Tools | Gate | Model family |
|---|---|---|---|---|
| Column proposers ×2, plus 1 isolated challenger | Bundles: hypothesis, plan, ≥ 1 metric and ≥ 1 constraint rubric (paper F.2) | `price_columns`, `evaluate_policy` (search plane) | Screening | A (challenger B) |
| Scenario adversary | ScenarioSpecs with KL ≤ η_max | `scenario_impact`, `reverse_stress` | Audit | B |
| Quarantined extractor | τ, covenant and GP-notice records; no outbound tools | — | Schema check plus human samples | A |
| View translator | ViewSpecs; the member confirms the *effective* view | `ep_condition` | Human | A |
| Memo writer | Claims citing metric IDs | `get_metric`, `validate_claims` | Coverage = 1 | A |
| Auditor | Verdicts on whether evidence *supports* each claim | Read-only logs, diffs, registries | ≤ 4 findings | B |
| Shadow-IC seats ×12 | Assessments, minority reports | Evidence slices | Flag, never vote | ≥ 3 families |
| Contract drafter | Amendment drafts | Phase-I checker | Human signature | A |

**Mechanics.**
- **Tools.** Strict schemas on the MCP server, executed by X1. Besides those above: `robustness_card`, `flip_thresholds`, `phase1_restore`, `group_envelopes`, `bridge_card`, `register_forecast`, `escalate` and `log_assumption`.
- **Meta-controller.** A plain Python state machine:
  - DRAFT → SIGNED or SIGNED_IN_RECOVERY (G0, Phase I) → DESIGN_QUALIFIED (G1) → STATE_FROZEN (G2) → (PROPOSE → SCREEN)* → SELECT → SEAL (run once) → RETRO → MEMO → AUDIT → IC → CLOSED.
  - ESCALATE is reachable from any state.
  - It stops on budget exhaustion, after 6 cycles without promotion, or when no column has a positive robust reduced cost.
- **Planes.** Search exposes only bounded aggregates (paper l.6825). The final plane is sealed and run once; each plane has its own caches.
- **Gates** (engine-owned):
  - Gate 1 checks type rules, Tier 1 in every search world, non-inferiority to HOLD in every world, budgets and guarded files. Failures score worst-case.
  - Gate 2 promotes only if ΔΨ_τ − 2·SE > ε_mat, using an entropic aggregator across worlds; ties keep the incumbent.
  - Gate 3 applies the §4.10 test and returns QUALIFIED, NOT_QUALIFIED or NOT_ASSESSED.
- **Budgets.** X1 counts every evaluation, failures included. α-investing with W₀ = 0.05; $50 soft / $200 hard per cycle; a DSR hurdle of ≈3.47σ at N = 200; PBO ≤ 0.20 (SYN §5.4, §5.7).
- **Memory.** An append-only log plus a conclusions note of ≤ 300 words, used as a search heuristic only: never evidence, never carried across campaigns, never exposed to the final plane.
- **Escalation.** `escalate` pauses the state machine when blocking. Assumptions are logged, versioned and printed in the memo and the pack. The paper's agents are told never to ask (paper l.6407); ADIC reverses that.
- **Cross-family review.** The auditor and red team run on family B. If only one family is configured, the record says "same-family review" and a human countersigns.
- **Offline mode.** An `LLMBackend` protocol with three implementations: Anthropic (claude-opus-5-5, explicit effort, strict tools, `messages.parse`), Replay (keyed by prompt hash, failing closed on a miss) and Stub. Engine packages never import `agents`.

## 6. IC layer

| Audience | Sees each quarter |
|---|---|
| IC | CFP stage; the Tier-1 board (value, world range, CP bound, KL worst case, band; in recovery also u*, the IIS, the glide path and infeasibility prices); the λ curve with intervals and FTP; certificates Γ and the MMW gap; the bridge per world; P(10y ≥ 10%) against worst-world P(red); the ε_R–cost frontier; k_MS and reverse stress; the 12-light state panel |
| Group heads | Envelope use and priced requests within their ranging validity; decision cards in marginal-agenda order; net α* after charges; forecast information value against the group's own reference class (n_eff ≥ 20); DVA |
| Treasurer / CF | Ladder; survival fans under T4′; facility and covenant paths; collateral ladders by CSA; owner-draw paths; FTP publication; band pricing |

- **Shadow IC.** Twelve mandate seats: CIO, CRO, the Treasurer as the owner's advocate, five private-group heads, Public Markets, Overlay, an outside-view forecaster and a red team. AI seats flag but never vote. Group heads recuse on their own envelopes and are scored on total-portfolio regret (GROUPS §7.1). The blueprint's opposing personas become the Treasurer's and the CIO's mandates.
- **Protocol** (SYN §6.3):
  - frozen questions;
  - independent assessments;
  - a reveal, with cruxes ranked by value of information;
  - a debate on at most 3 cruxes;
  - a pre-mortem and minority reports;
  - a locked blind human pre-vote;
  - a ballot with probabilities;
  - minutes and signposts.
- **Discussion order.** Total portfolio, then group blocks, then cross-group items (internal transfers, desk quotes, collateral, the overlay offset card), then the ballot.
- **Q&A.** Answers cite `run_id:artifact:path` and label each statement as model output, agent judgment or assumption.
- **View conditioning.**
  - W1 is client-side entropy pooling in the HTML pack: an embedded 10k × ~40 matrix (≈1.6 MB) and Newton in plain JavaScript. Reweighting is exact and labelled exploratory.
  - W2 re-optimises on cached trees; W3 re-simulates.
  - Natural-language what-ifs become typed overrides the member confirms; no surrogate number is ever shown (brief §6).
  - An irreversible Tier-A action needs a sealed confirmatory run.
- **Decision log.** Append-only DecisionRecords: ballots, overrides with reason codes, verbatim dissent, signposts with flip values. Every IC probability is Brier-scored at 1, 4 and 8 quarters.

## 7. Data and synthetic generator

- **Schema.** holding → group (7 + CF) → strategy → sub-strategy.
  - Tables: `position`, `cashflow`, `mark` (u/a/f with basis, as-of, recorded-at, author, revision), `quote` (with a conflict flag), `hf_terms`, `facility`, `overlay_trade` (with CRIF), `csa`, `owner_draw`, `forecast`, `decision`, `assumption`.
  - Every fact is bitemporal and tagged with unit, currency, gross/net, arithmetic/geometric and frequency.
- **Biased observations** (GROUPS §6).
  - Reported NAV is smoothed at 0.5–0.7, lagged and manipulated BGK-style.
  - Underwriting follows u = μ̄ + 0.3(α − α_s) + b^u + γ′x, with +2pp for leverage above 6× or heavy multiple expansion.
  - Forecasts follow f_t = 0.6f_{t−1} + 0.4[w_uu + w_aa + (1 − w_u − w_a)f* + b^f] + η, with timing optimism after high-yield shocks.
- **Sealed truth.**
  - Vintage skill a_v = −0.05z_v + u_v; GP effect 3%; idiosyncratic 2.5%.
  - Truncated or NIG shocks; both PD/LGD pairs; τ calibrated to Form PF.
  - Releases: R0; R1 with 1,000 worlds × 40 quarters on CRN across lens actions; R2 with 200 history worlds. Census: ≈395 positions, ≈1,500 loans, ≈250 trades, $177bn NAV, $38bn unfunded.
- **Checks.** V1–V23, among them identities, netting, DPI by age, distribution rates, exit uplift, secondary prices, HF liquidity, the PC loss band, SBC, parameter recovery within ±5pp, time-travel CRPS, regret against an oracle, 100% labelling and LP-accessible actions only.
- **Labelling.**
  - `SYN-` IDs, `is_synthetic`, Parquet metadata and a "SYNTHETIC – NOT ADIC DATA" footer.
  - Taint propagation: any output computed from synthetic input is synthetic.
  - Truth tables are sealed from agents and estimators.
  - The claim validator rejects attributing synthetic numbers to ADIC.
- **Adapters.** map → validate → bitemporal upsert → hash; real and synthetic data are never mixed. First requests: τ, PE unfunded by vintage, the blotter and CSAs, the draw convention.

## 8. Package layout and build order

```
adic_tpa/
  core/     types, units (W0), ids, hashing, manifests, counter-based rng
  data/     schemas, store, adapters/, synth/
  scen/ state/ liab/            priv/ pub/ ovl/ debt/ ledger/
  beliefs/  actions/  sim/  policy/ (dsl, standing, cmaes, certify)
  opt/      assemble, highs_io, phase1, colgen, levelb, duals, kernel, envelopes, filter_f, vfa
  robust/ attrib/ bridge/ stats/   lab/ (evaluator, metacontroller, gates, registries)
  agents/   backends (anthropic, replay, stub), roles, tools, mcp_server
  ic/       pack (jinja2 + plotly + client EP), shadow_ic, decision_log      cli/
tests/ unit property metamorphic regression recovery solver statistical perf layering
```

- **Dependency order.** core → data → scen/state/liab → priv/pub/ovl/debt → ledger → beliefs → actions → sim → policy → opt → robust/attrib/bridge/stats → lab → agents/ic → cli.
- **Parallel tracks, after a shared core in weeks 0–2:**
  - scenarios;
  - private and public engines;
  - overlay;
  - beliefs with recovery tests;
  - opt against a fake Φ fixture;
  - lab and agents on the stub backend.

  They integrate at the ledger (week 4), the simulator (week 5) and H on the real Φ (week 6).
- **MVP ("Liquidity & Actions"; offline, synthetic).** It answers SYN §10's six questions:
  - Phase-I status;
  - survival and the CFP stage under T4′;
  - λ and the MCL;
  - the top-20 cards with envelopes and Γ;
  - the Tier-1 board with world ranges and the ε_R frontier;
  - the bridge.

  Scope: worlds M1 and M6 plus held-out; a Level-1 overlay; the FBE on planted biases; P with certification; H in the what-if configuration; a replay-backend memo writer.
- **Gates.** B1: simulator ≤ 60 s. B2: quarterly H ≤ 2 min. B3: Level B ≤ 10 s. B4: W1 ≤ 1 s.
- **Tests.**
  - Unit: identities and units.
  - Property (hypothesis): homogeneity, monotonicity, conservation.
  - Metamorphic.
  - Regression: `test_no_pinned_duals`, `test_v8_replica`, the bridge against verifier 10, the gap_01 table to $0.01bn.
  - Recovery and SBC.
  - Solver: finite differences, penalty invariance, two-solver agreement, Γ ≥ 0.
  - Statistical: CP coverage on events of known probability.
  - Performance and layering.

## 9. Key choices versus alternatives

| # | Choice | Rejected | Evidence |
|---|---|---|---|
| 1 | One Φ generates both the simulator and H's rows | A separate optimisation model | Rules out H/P disagreement (C1 §5.3) |
| 2 | Phase I, then the restored problem | Penalty weights as prices | Dual 100 → 0.237; reservation price 0.9% → 76.8% (gap_02 §4) |
| 3 | Node-wise tree LP plus column generation with the Farley certificate | Asset-level extensive MILP; dense fans with decision rules | Shapley–Folkman bound vacuous at ≈8,100 rows (ver/01_mpo R7); density penalty [M]; decision rules can go infeasible (lit/01_mpo §4.4) |
| 4 | Belief-state trees | Trees built on true regimes | Latent regimes need a belief state (lit/10); P15 |
| 5 | CVaR in H; Clopper–Pearson in P | The scenario approach; optimising probabilities | Scenario approach misapplied to tuned policies (ver/01_mpo R3) |
| 6 | λ from cash KKT, with envelopes | Hand-set hurdles; prices alone | Baumol–Fabian; 36/40 decisions but $24.7m worse (SYN §4.4) |
| 7 | Kernel with a market-risk deflator | Liquidity-only discounting | $72m flip (SYN L1) |
| 8 | Verification across worlds plus tilts | A DRO ball inside H | Radius not elicitable; 3–4pp model dispersion vs 0.2pp MC error (SYN §4.10) |
| 9 | Exact Shapley plus a null control | Attribution by sequential re-optimisation | v8's +3.5pp → +0.35–0.61pp (gap_05 §8); 55.8% was scaffolding (paper l.2657) |
| 10 | Cohorts under an exactness rule; asset-level nonlinear engines | Full asset-level simulation; asset classes | 60 s target; a single private rate hides the PE drain (SYN §4.2) |
| 11 | Agents only as column and scenario generators | Agent-orchestrated analysis | Protocol gaming in 2 of 3 runs; "cooperative … not an adversarial sandbox" (paper l.1224–1234, l.7489) |
| 12 | `highspy` on assembled sparse matrices | cvxpy at scale; Gurobi `feasRelax` | Feasibility relaxation, IIS, ranging and warm starts are all available [M] |

## 10. Risks, and what is deliberately left out

**Risks.**
1. **Dual stability, the biggest risk.** CVaR-row duals rest on about a dozen tail leaves per world, so λ may swing across trees and flip marginal assets.
   - *Mitigations:* tail strata, bootstrap bands, one-sided intervals, hysteresis and forced re-solves.
   - *Fallback:* publish FTP as a band and decide by forced re-solves.
2. **Solve time.** Real assemblies may be slower than the proxy. Fallbacks: the 400-leaf configuration, and Benders overnight.
3. **Shared factor architecture.** Verification cannot detect a misspecification common to all worlds (SYN §9.2).
4. **Data.** τ, PE unfunded by vintage and the overlay blotter decide the results.
5. **Mandate.** Without the owner band, the M6 class breaches its capacity level, which puts the book into recovery (gap_02 §3).
6. **Complexity.** The design needs MRM capacity; the consistency contract mitigates it.
7. **A thin agent layer** may disappoint R11 expectations. This is deliberate.

**Deferred or excluded.**
- SDDP and belief-state SDDP; deep-RL challengers.
- Neural surrogates (they conflict with P1).
- MCMC: PyMC is absent, so closed-form empirical Bayes is used.
- Level-2 overlay beyond SSVI; the structural owner model.
- Benders beyond 2,000 leaves.
- Cross-campaign memory; persuasion optimisation.

Nothing executes.

## 11. Brief §5 decisions

1. **Time grid.** Quarterly decisions, monthly engine, daily stress sub-steps; 40 quarters with 3/5/10-year windows. 10% means the 10-year rolling geometric TWR, nominal, gross of distributions; real, net-of-payout and owner-IRR measures are also reported.
2. **State.** Cohorts for linear engines, assets for nonlinear ones (≈130 companies, 40 HF lots); ≈2,000 floats per path, under 1 GB at 10k paths; ≈30 states per H node.
3. **Scenario generator.** ≈20 factors; macro × exit × shock chains; t₅ innovations; six CMA worlds plus held-out and misspecification sets, hashed at G0; belief-state trees for H.
4. **Private engine.** RFT-TA v2 cohorts plus EV and claims engines. Economic NAV drives value; reported NAV drives covenants and bids. The drought enters through e_t multipliers and effective age; fused μ_i enters as drift plus a group-bias shock.
5. **Instruments.** Hedonic secondary prices with size impact; NAV facility at SOFR + 300bp (+140bp in stress); preferred equity at 12–14%; CV elections as GP offer events; CFOs with a 6–12-month lead. Each instrument's implied cost of liquidity is its reduced cost at the kernel.
6. **Overlay.** A position layer: tail ladder monetised at λ^w; opportunistic exposure rules with DSR-gated α; VM by CSA; SIMM-like IM; OV1–OV3; collateral charged and credited by CF.
7. **Liabilities.** A smoothed, clipped, fiscal-driven owner draw on opening NAV; Mode B by default; the band priced on CRN.
8. **Optimiser.** A node-wise 12-quarter tree LP with ≈1,150 leaves; Phase I then II; column generation plus a Level-B MILP with certificate Γ; ℓ = M/(μ − M) feeding the kernel; Lagrangian scoring.
9. **Policy classes.** PFA standing policy, CFA buffers, DLA/MPC (H), VFA terminal values; a PolicySpec DSL (≤ 25 nodes, ≤ 8 parameters, typed lags; SYN §5.5) through which agents propose policies.
10. **Objective.** Lexicographic levels 0–3 with a tolerance cascade; T6 bands by model class; floor reading (b); J = CRRA(3) with an L2 shortfall.
11. **Robustness.** Ensemble first, then KL/W∞ tilts, then reverse stress; views through the same tilts; qualification by intersection–union test.
12. **Experiment layer.** Hashed manifests; a metric registry; engine-counted budgets; DSR, PBO, α-investing.
13. **Agent roster.** Eight roles emitting typed mathematical objects; a state machine; three gates.
14. **IC module.** 12 seats; a blind pre-vote; W1/W2/W3 what-ifs; DecisionRecords with Brier scoring.
15. **Package layout.** As in §8; pydantic contracts carrying units and array shapes [path, t, k]; benchmark gates B1–B4.
16. **Group taxonomy.** holding → group → strategy → sub-strategy; intra-ADIC netting at zero; group DVA alongside total-portfolio decisions.
17. **Group actions.** As in the §4.6 table.
18. **Internal capital market.** Envelopes and λ from one solve; FTP published by CF; firewalled desk quotes as evidence; dry powder held as contingent columns.
19. **Forecast credibility.** Registry, WIS and bias model; κ_g as precision; shown only against each group's own reference class; pay decoupled from budget size.
20. **Shadow-IC roster.** Twelve mandate seats, organised by total portfolio and by group.
21. **Synthetic generator.** SYN-ADIC-177: three layers, census v1.0, V1–V23, SBC, labelled throughout.
