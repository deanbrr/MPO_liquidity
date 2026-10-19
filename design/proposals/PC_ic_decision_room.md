# Proposal PC: IC decision-room first

**Angle.** Start from the decisions the human IC, the CIO, the CRO, the Treasurer (Corporate Finance, CF) and the seven group heads must take. Work back from them to the evidence, the engines and the agents. **Date:** 2026-10-18.

**Tags** as in 00_SYNTHESIS §0, plus [I-calc] for computations made for this proposal. Every ADIC figure is an assumption; every computed number is *SYNTHETIC – NOT ADIC DATA*. "Bench" means two structural benchmarks run on this laptop: `hn_lp_bench.py` and `sim_kernel_bench.py` in `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\pc_bench\` (session scratchpad, not part of the repository).

---

## 1. Thesis

The organizing idea is a **Decision Register**. It is a typed catalogue, owned by humans, of the 23 recurring and event-driven decisions that the IC, CIO, CRO, Treasurer and seven group heads take each quarter and year: pacing, envelopes, SELL/HOLD/REFINANCE/LEVER cards, leverage, overlay budgets, the liquidity buffer and the response to the owner's draw. Each entry declares who proposes and who decides, its variables and deadline, and the options it must always show (status quo, DEFER, the recommendation, the archetypes). It also declares an **evidence contract**: the registry metrics, planes and freshness the decision needs. A deterministic compiler turns each quarter's agenda into an evidence build graph that schedules the engines. Every engine therefore exists because a decision consumes it, and every number in the room traces to a hashed run. The quant core gives the room one currency: a liquidity price λ, read only from a feasible problem, published as CF's funds-transfer-pricing (FTP) curve and paired with quantity envelopes from the same solve. The shadow IC is a computed sensitivity analysis, not a persona debate. Each seat's position is the optimizer's implied action under that seat's declared beliefs and an admissible utility; LLMs argue around those numbers but never produce them. Humans pre-vote blind and decide by ballot, and their decisions, dissents and signposts are logged and scored like every other forecast.

## 2. Requirements and principles trace

### 2.1 Requirements R1–R15

| # | Where | How satisfied |
|---|---|---|
| R1 Multi-period | §4.11 | 12-quarter here-and-now LP on a scenario tree; certified 40-quarter standing policy; quarterly MPC (00_SYNTHESIS §4.8) |
| R2 Robust scenarios | §4.3, §4.13 | Six fee-consistent CMA models, a held-out generator and a misspecification ensemble; KL/W∞ metrics, k_MS, reverse stress; entropy-pooling views |
| R3 Probabilities | §4.12, §6.3 | Each probability shown with model range and MC error; Clopper–Pearson certification; ICD-203 words; Brier scores at 1, 4 and 8 quarters |
| R4 5–10% distribution | §4.9; Q2, A6 | Owner-draw engine $D_y=d_yB_y$ on the oil/fiscal state; mandate switch; T1/T7/T8; a quarterly owner-response decision |
| R5 10% target | §4.1, §4.12 | 10-year geometric TWR, distribution-inclusive; "what you need to believe" (WYNTB) bridge per model; P(10%) reported, never optimized (gap_05) |
| R6 Leverage | §4.7; Q3, Q6, A5 | Portfolio LEVER is a CF decision; asset-level LEVER ≡ ADD + REFI; limits and doctrine (00_SYNTHESIS §4.5) |
| R7 Private book, DPI decline | §4.4; Q5 | Three private engines with exit window $e_t$ and an effective-age clock; drought start (D 0.87) |
| R8 Lens per asset | §4.6; Q6 | One pricing kernel; group instrument library; decision cards carrying `priced_on` |
| R9 Three return series | §4.5 | The Forward Belief Engine (FBE) fuses u/a/f plus a market-implied anchor; group bias model; forecast registry |
| R10 Overlay | §4.8; Q7, A7 | Position layer, net-vega limits OV1–OV3, VM/IM by CSA (gap_03) |
| R11 Agentic | §5 | Deterministic meta-controller, typed tools, gates G0–G9, planes, counted evaluations |
| R12 IC discussion | §6 | Register, pack, computed shadow IC, blind pre-vote, console, decision log, signposts |
| R13 Prior deck | §4.12, §4.14 | Two tiers → Tier 1A/1B + Tier 2; state engine → 12-row panel with F_t; `test_v8_replica`; motto enforced as P1 |
| R14 Seven groups + CF | §3, §4.10, §6 | Every decision has a group or CF owner; envelopes + FTP; group blocks on the agenda; CF as internal bank |
| R15 Synthetic data | §7 | SYN-ADIC-177 three-layer generator; SBC and parameter recovery; taint-propagating labels |

### 2.2 Principles P1–P15

| P | Enforcement mechanism |
|---|---|
| P1 | `validate_claims` blocks any number that does not resolve to a run-registry metric. Seats get numbers only from `implied_actions`. No execution adapter exists. AI seats never vote |
| P2 | Out-of-process evaluator with read-only engine, scenario and belief mounts. RunManifest hashes source, config, scenarios and beliefs. Guarded files; counting on the engine side; a stale cache stops the run (brief l.7210) |
| P3 | Plane registry: search, final and misspecification sets hashed at G0, before search. Separate caches. Search sees bounded aggregates. Embargoed historical windows |
| P4 | `IdeaBundle` with hypothesis, plan, ≥1 metric rubric and ≥1 constraint rubric. ≤3 retries. Every call counted, failures included. DSR/PBO deflation printed |
| P5 | G4 `correct` is engine-owned, including non-inferiority vs HOLD in every world (worst world aggregated). G5 strict, ties keep the incumbent. G6 paired CRN with pre-declared materiality, else `not_qualified` |
| P6 | Every package brief shows HOLD, static SAA, v8 rules, target-chasing, a placebo and archetypes A/B/C. Switch-off null control; single-change ablations; disjoint seeds |
| P7 | A validator checks that sources resolve; a family-B auditor reads logs and engine diffs to check that they support the claim. Both verdicts printed |
| P8 | Register and AnalysisContract written by humans, signed at G0/G1. Agents draft amendments; humans adopt them |
| P9 | Plain-Python state machine. 2 workers. Campaign memory is a heuristic only. Escalation channel and assumption log |
| P10 | Auditor and Red Team on family B; ≤40% of seats per family; provider-agnostic `LLMBackend` |
| P11 | `SeedSequence` keys per plane, model and path block. Draws generated *outside* parallel kernels: the bench gave thread-count-dependent results when drawing inside `prange` |
| P12 | Engines and tests run without an LLM; `StubBackend`/`ReplayBackend`; live mode needs only a key |
| P13 | Prompts carry aggregates and IDs. Extractors are quarantined. Holding-level prompts need an operator flag |
| P14 | `DecisionBrief` requires binding constraints, shadow prices, marginal value per action, attribution and flip thresholds; incomplete briefs are rejected |
| P15 | The PolicySpec checker forbids identity, horizon and budget features. Scenarios are anonymized. Terminal values remove end effects. `is_synthetic` taint |

## 3. System decomposition

### 3.1 Layers

```
L5 Decision room   idm/ pack/    Register · evidence compiler · briefs and pack · console (Q&A, W1–W3) · shadow IC
                                 · ballots · decision log · signpost monitor · forecast registry
L4 Agentic         lab/ agents/  deterministic meta-controller · LLM roles behind typed MCP tools · gates · budgets
L3 Evidence plane  lab/          evaluator process · run and metric registries · plane registry · content-addressed caches
L2 Decision engines core/ icm/ robust/ bridge/ attrib/   Phase I · H-LP + duals · scoring + selection MILP
                                 · simulator P + policy search · module F · envelopes/FTP · robustness · bridge · attribution
L1 World and book  scen state priv pub overlay liab beliefs ledger
L0 Data            data/ synth/  bitemporal store · schemas · adapters · SYN-ADIC-177 · labels and taint
```

Dependencies point downward only. L5 never calls an engine: it asks the compiler, which asks the evaluator.

### 3.2 Modules

D = deterministic, A = agentic. "Serves" lists Register entries (§6.1).

| Module | Responsibility | In → out | D/A | Owner | Serves |
|---|---|---|---|---|---|
| `data`, `synth` | Schemas, store, adapters, taint; SYN-ADIC-177 | files/seeds → Parquet | D | Data office (CIO) | all |
| `scen` | Regime-switching factor model; six CMA models + held-out generator; vol and oil/fiscal states | CMAs, market data → ScenarioSet | D | Risk (CRO office) | Q1–Q7, A1–A2 |
| `state` | Stress filter F_t; initial π0, e0, Z0; 12-month draw | snapshot → StateSnapshot | D | Risk | Q1, Q2, Q10 |
| `priv` | Engines for fund interests, single companies, contractual claims | positions, beliefs → CashflowCube | D | TPA desk + group quants | Q1, Q5, Q6 |
| `pub` | Hedge-fund liquidity-term state machine; long-only | terms τ → φ_i(h,S) | D | Public Markets + TPA | Q8 |
| `overlay` | Templates, surfaces, VM by CSA, SIMM-like IM, OV1–OV3 | blotter → P&L, VM/IM, offset card | D | Overlay + Risk | Q7, A7 |
| `liab` | Owner draws, mandate switch, rule library | fiscal state → draw paths | D | CF | Q2, A6, E4 |
| `beliefs` | FBE (four signals), bias model, registry scoring | marks, quotes → BeliefSet | D | CRO office (validator) | Q5, Q6, A8 |
| `ledger` | Liquidity ledger, ladder LR1–LR8, CFP stage, survival | flows → LedgerPaths | D | CF | Q1–Q3, E3 |
| `actions` | Instrument library; action cash-flow deltas on CRN; cards | kernel → DecisionCard | D | TPA desk | Q6, Q9, E1–E2 |
| `core` | Phase I; H-LP and duals; scoring and selection; simulator P, CMA-ES search; module F | contract, tree → HNResult, Tier-1 bounds | D | TPA desk; CRO signs Phase I and module F | Q1–Q7, A1 |
| `icm` | Envelopes, decision prices, published FTP, vintage ledger | duals → EnvelopeSet, FTPCurve | D | CF (FTP) + TPA (envelopes) | Q4, A3 |
| `robust`, `bridge`, `attrib` | Entropy pooling, R1–R8, reverse stress; WYNTB; attribution | weights, CMAs → cards | D | Risk; CIO office | Q1, A2, all briefs |
| `lab` | Evaluator, registries, planes, gates, meta-controller | contracts → manifests | D | TPA desk under MRM | all |
| `agents` | LLM roles, backends, prompts | typed tool calls → typed outputs | A | CIO data science (AI management system) | briefs, console, seats |
| `idm`, `pack` | Register, compiler, briefs, shadow-IC protocol, ballots, log, signposts; HTML pack and console | runs → pack, records | D (seats A) | IC secretariat (CIO office); registry by CRO office | all |

### 3.3 Interface contracts (Pydantic v2; arrays as Arrow tensors)

| Contract | Shape / fields | Units |
|---|---|---|
| ScenarioSet | factors f32[N, M, F]; regimes i8[N, M, 3]; vol f32[N, M, V]; draw rate f32[N, Y] | monthly log returns |
| CashflowCube | f32[N, Q, K, 4]: calls, distributions, economic NAV, reported NAV | $bn per quarter |
| LedgerPaths | f32[N, M, R]: LR1–LR8, CBC, NCO | $bn |
| BeliefSet | μ̂, σ̂, band, flags per position; group-bias draws | forward log return on nowcast NAV |
| HNResult | actions; duals μ[n,t], φ, λ_R, λ_Lev, ρ; ℓ^q; envelopes; `priced_on` | per $ |
| ViewSpec | metric, operator, value, confidence c, channel ∈ {FBE, EP} | metric units |
| PolicySpec | AST of ≤25 nodes and ≤8 parameters; variables with observation lags | — |
| RunManifest | hashes (engine, config, scenarios, beliefs, data); seeds; plane; LLM call records | — |

## 4. Quant core

### 4.1 Time grid and the 10% target

- **Clock.** Quarterly decisions, t = 0…39. Monthly sub-steps for the ledger and hedge-fund dealing. Daily overlay sub-steps inside stress windows only. Reporting windows are 3, 5 and 10 years.
- **Target.** 10% means the 10-year geometric TWR, nominal USD and distribution-inclusive: $\widetilde W_T=W_0\prod_k(1+r^p_k)$. Payouts therefore move it only through what they cost (00_SYNTHESIS §4.9, §9.3).
- **Also reported:** real TWR; NAV growth net of payouts; the real-preserving payout (≈5.3% at the 8.3% mixture return, gap_05); owner IRR at a 10% accrual (reported only).

### 4.2 State representation and memory budget

Path simulation runs on cohorts; action analysis runs on holdings with CRN (00_SYNTHESIS §4.2).

| Block | Floats per path |
|---|---|
| ≈300 fund-interest cohorts × (V, N, U, a^e, NAV-loan balance, deferred payable) | 1,800 |
| ≈120 companies × 4; ≈100 claim cohorts × 3; 40 hedge-fund lots × 6 | 1,020 |
| Overlay (15 families × 3, 12 CSAs × 2); ledger (12); world state (S, e, Z, V, ≈20 factors, F_t) | 110 |
| Beliefs: μ_i drawn once per path + 7 group-bias shocks | 407 |
| **Total ≈3,340 floats = 13.4 KB (float32)** | |

**Memory.** 10,000 paths hold 134 MB of live state plus 100 MB of path metrics (64 metrics × 40 quarters).

**Bench.** A numba cohort kernel (two clocks, smoothing, ledger, recourse) ran 10,000 paths × 400 cohorts × 120 months in **3.96 s on 8 threads**, or 8.3 ns per cohort-month (2.28 s on 24 threads) [I-calc]. The full engine is budgeted at 5–8× the kernel, which gives ≈20–35 s per model on 8 cores, inside the 60 s target. The six models run in parallel processes.

### 4.3 Scenario generator

Adopt 00_SYNTHESIS §4.1.
- **Model.** Monthly regime switching: $f_t=c_{S_t}+Af_{t-1}+D_{S_t}L_{S_t}\varepsilon_t$, with $\varepsilon\sim t_5$. Three coupled chains: macro $S_t$, exit window $e_t\in\{O,N,D,F\}$, and oil/fiscal shock $Z_t\in\{N,B,SG,DB,SS,GW\}$.
- **Factors.** About 20, including Brent (started from the futures curve), USD, spreads, CPI, rates, VIX/MOVE/OVX, exit activity, secondary discount and NAV-loan spread.
- **Implied volatility** moves across tenors by $\beta(T)\approx0.94(T/30d)^{-0.43}$ (gap_03 §3).
- **Anchoring.** Each model is anchored to its CMA's 10-year compound returns.
- **Planes,** hashed at G0:
  - *search:* M1 and M3 plus a second generator family (a VAR-bootstrap hybrid);
  - *final:* fresh seeds on M1–M6, the held-out block-bootstrap/FHS generator, and the 2008–09, 2020 and 2022 windows (sign and Tier-1 checks only);
  - *misspecification:* M4–M6, Φ = 0.75, GC1's private-credit loss pair, adverse hedge-fund terms, the log fiscal map.
- **Owner demand:** $d_y=\Pi_{[5,10\%]}(0.5d_{y-1}+0.5\,\Pi(7.5\%+0.625FN_y))$, with overrides 0.25–2% by Z (00_SYNTHESIS §4.7). From today: $9.9–10.8bn over 12 months.
- **Initial state,** frozen at G2: calm ≥ 0.99; F_t = 0.10 (base rate 0.17); drought 0.87; Gulf war ≈0.85 (gap_04).

### 4.4 Private engines by group

Three engines share one pricing kernel (GROUPS §1).
- **Fund interests** (PE, secondary funds, closed-end credit):
  - calls $C=(1-e^{-\lambda\Delta})U$;
  - distributions $D=(1-e^{-\delta\Delta})Ve^r\zeta$, where δ runs on effective age $a^e_{t+1}=a^e_t+\kappa(e)\Delta$ with κ = 1.2 / 1.0 / 0.6 / 0.5;
  - reported NAV is smoothed to AC1 0.66–0.71;
  - stressed calls are $\lambda(U-B^{SL})+c^{SL}B^{SL}$.
- **Single companies** (co-investments, CV stakes, kickers): EV jump-diffusion with $E=\max(V-D,0)$, Weibull exits scaled ×1.3 / 1.0 / 0.5 / 0.3 by regime, one draw per company per path.
- **Contractual claims** (Capital Solutions, Private Credit): competing risks with separate PIK, extension and default hazards; LGD 0.67, PD_N 1.1% (GROUPS R1).
- **Public Markets:** a hedge-fund liquidity-term state machine, connected to the ladder only through φ_i(h,S); long-only with net IR −0.05.
- **Beliefs** enter as $\bar\alpha_i$. Each μ_i is drawn once per path with a group-bias shock, then Kalman-updated, which gives HOLD its information value.

### 4.5 Belief fusion: three marks plus a market anchor

All signals are put on one basis: the forward log return on nowcast economic NAV, net of fees.
- **Fusion.** $s_j=\alpha_{j,g}+\beta_j\mu+\varepsilon_j$ for $j\in\{u,a,f,m\}$, and $\hat\mu=\Lambda^{-1}(m\sigma_k^{-2}+\mathbf1'\tilde\Omega^{-1}\tilde s)$, with correlated errors and non-negative weights (00_SYNTHESIS §4.3).
- **Fund interests** use Benktander credibility with a prior frozen at inception.
- **Group forecasts** enter once, at precision $1/(\kappa_g^2\hat\sigma^2)$, with median κ_g = 1.75 (GROUPS §5).
- **Market anchor** (blueprint graft 1):
  - $y^{MKT}=(1+y_b)(p/\theta)^{1/D}-1$; with p = 0.87, θ = 0.95, D = 3.4 and y_b = 11.9%, it gives ≈9.0% (GROUPS §3.2, inverted);
  - it carries its own bias prior and a precision set by bid dispersion;
  - desk bids enter only through the pricing committee, with an external second source.
- **Outputs:**
  - μ̂, σ̂ and an 80% band;
  - P(forecast achieved within k quarters);
  - flags F1–F10;
  - a **Zombie-NAV** flag: mark ≥ reference while exit velocity sits below the reference P25 for 4+ quarters;
  - a **no-catalyst** flag on recovery forecasts without dated milestones (brief §6 graft 2).

Tier 2 uses posterior means; Tier 1 uses the P10 with group bias stressed by +2 sd.

### 4.6 Action economics by group

SELL, HOLD, REFINANCE and LEVER reduce to two primitives, exposure and financing. LEVER ≡ ADD + REFI is checked by a reconciliation test.

Every action is scored on one kernel:
- $\mathrm{Score}(i,a)=\sum\pi\,\mathbb E_b[\Delta CF]+\sum\tilde\mu(h\Delta HQLA-\Delta SC)+\sum\tilde\phi(\Delta IGC-0.08\Delta NAV)-\lambda_R\Delta\mathrm{CVaR}-\lambda_{Lev}\Delta Lev-\lambda_{Enc}\Delta Enc-\sum\rho_k\Delta\mathrm{Floor}_k-\kappa$
- where $\pi_{s,t}=p_sm_{s,t}\prod_{k<t}(1+\ell^q_{s,k})^{-1}$ (00_SYNTHESIS §4.4).

Transfers between ADIC groups raise zero liquidity.

| Group | SELL | HOLD | REFINANCE (cash-out) | LEVER (exposure-up) | Lag / availability |
|---|---|---|---|---|---|
| PE | LP sale/strip at hedonic price (buyout 91%; crisis 0.80–0.84 of economic NAV) | CV election | LP-portfolio NAV facility (CF; SOFR+300bp, LTV 10–20%); preferred 12% | Re-ups; **pacing** corridor | 3–6 months; success 0.75–0.85 / 0.6 / 0.4–0.5 |
| Secondaries | Tertiary sale | Deferred payables count as debt | LP-level facility; CFO | Buy iff $b^*\ge p^{ce}$ after a 4.2–5.1% curse haircut; contingent budget | ≤12 months |
| Co-investment | Buyer-model bid: 71–79% normal, 56–65% drought | LAPV less concentration | Pool facility only | Holdco PIK rarely (wipe-out 7.0% → 22.8%) | 3–9 months |
| Capital Solutions | Syndication; credit secondaries −8–12% | Amendment policy | Back-leverage D/E ≤ 0.5; CFO | ADD iff IRR > $(1+r_h)(1+\bar\ell)-1$ | Benign regimes |
| Private Credit | SMA loans 0.99 / 0.96 / 0.85; evergreen ≈38% filled | Run-off switch (+$0.8–0.9bn in year 1) | SMA back-leverage | SMAs only, EL < ≈4% | Days to 4 months |
| Public Markets | Queued HF redemption iff $\hat\alpha+\kappa^{re}<\bar\ell(T^{cash})$ | NAV + PV(α) − value of terms | **P2S**: 0.40–0.70% per $ freed (normal), 2.2–3.3% (stress) | Portable alpha; HF-TRS (≈2 survival months) | φ: 19 / 55 / 66% by month 3 / 6 / 12 |
| Overlay | Tail monetization iff $V(1-ba)+\lambda^w\Delta L\ge$ continuation | Hedge ratio | IM release | Synthetic beta within 1.0–1.3× | 1–7 days |
| CF | — | — | Revolver SOFR+85bp (0% credit in 30-day rows), repo, term debt | Borrow only against the cyclical shortfall | ≤3 months |

Sources: 00_SYNTHESIS §4.4; GROUPS §3; gap_01 §3.

### 4.7 Leverage

- **Limits:** recourse debt ≤ 10% / 15%; economic exposure ≤ 1.30×; encumbrance ≤ 15% / 20%; covenant P(trigger within 12 months) ≤ 2%; 30-day coverage ≥ 1.0 with facilities at 0% (00_SYNTHESIS §4.5).
- **Doctrine.** Portfolio LEVER needs all of: Tier 1 passing with the debt; α\* above shadow costs; ΔP(10%)/ΔP(breach) above the IC's elicited rate; rating proxies at ≥ 95%. Leverage at the cap while the fund is behind target is flagged.

### 4.8 Overlay as a position layer

- **Books.** Three books (synthetic beta, the defensive stack, opportunistic) settle through one collateral ledger.
- **Templates.** Trades map to ≈15 templates priced on regime-driven surfaces.
- **One sensitivity set** feeds P&L, VM by CSA ($C^*=\mathrm{sgn}(V)(|V|-H)^+$, MTA, T+1), SIMM-like IM, the net-Greek limits and the ledger (gap_03 §2).
- **Limits:**
  - OV1 economic net vega $NV^{eq}_{overlay}(s)\ge0.75NV^{eq}_{tail}(s)$;
  - OV2 offset ratio ≤ 25% in every named stress;
  - OV3 a short-dated gamma budget.
- **Opportunistic credit.** Only residual α is credited, and only if DSR ≥ 0.95.
- **Stress-coverage ratio** (blueprint graft 3), printed on the offset card for each named stress: tail-hedge inflows ÷ (opportunistic VM + the private-distribution shortfall). Below 1.0 it shows amber.
- **Hedge value** = carry + liquidity value + enabling value. Monetization is decided by least-squares Monte Carlo.
- **Collateral.** CF's pool funds collateral. The overlay pays the contingent-liquidity charge (CLC) and is credited for crisis payoffs.

### 4.9 Liabilities

- **Mode B (owner call) is the default.** Modes A and H are priced by $J^*_A-J^*_B$ on CRN.
- **Draw basis.** $B_y$ is opening-of-fiscal-year reported NAV, reset annually (gap_02 §1.1).
- **The owner band.** Pre-agreed 5% draws in CFP Red: active in 12–22% of paths within a year, withholding $3–7bn over five years (L4).
- **Reserve** = 12 months of draws + the 30-day collateral need + stressed net calls.

### 4.10 Internal capital market: CF as the internal bank

- **Kernel.** $\ell^q_{s,t}=M_{s,t}/(\pi^H_{s,t}-M_{s,t})$, with $M=\mu+0.92\phi+\sum a_ry_r$ over every cash row of the *restored* H problem.
- **Envelopes.** $\Lambda^k_g=\sum_{i\in g}a^k_i(x^*)$, pooled across SAA replications.
  - Releasing capacity is free.
  - Increases on binding rows are priced at the dual, with $\sum_ga^k_g\delta^+_g\le\text{slack}_k$.
  - Up to +20% is Tier B; no ratchet (GROUPS §4.4).
- **Two price sets.**
  - Decision prices: undamped robust duals, with no floor.
  - Published FTP: an EWMA with a 2-quarter half-life and a ±50% collar, charged on liquidity tenor.
  - Performance charges are vintage-locked; CF holds the mismatch (GROUPS §4.3).
- **State-contingent pacing.** $P_{g,t}=P^*_g\Pi(1-\eta_g(\ell_t-\bar\ell)/\bar\ell)$, with η > 0 for PE and Co-investment and η < 0 for Secondaries and Capital Solutions.
- **`priced_on`.** Every card and FTP point records it. Phase-I duals are "infeasibility prices" only (gap_02 §4).

### 4.11 Optimizer

**Phase I.** Find the minimum violation, tier by tier:
$$u^*_k=\min\sum_{r\in\mathcal T_k}w_ru_r\ \text{ s.t. } Ax+u\ge b,\ x\in\mathcal X_{rev},\ \text{T5/legal rows hard},\ u_{\mathcal T_j}\le u^*_j+\delta\ (j<k)$$
- **Reversible levers only.** $\mathcal X_{rev}$ holds facilities, pacing, a band request, the reserve, amber sales and HF notices. PE sales are excluded.
- **Solver.** Sequential HiGHS LPs stand in for Gurobi's `feasRelax`. The IIS comes from a deletion filter over ≤30 aggregated rows.
- **Recovery.** If u\* > 0, the contract signs in RECOVERY with glide path $g_{r,t}=u^*_r(1-t/T_{rec})^+$ and T_rec = 4 quarters.

**Phase II: the here-and-now LP (H-LP).**
- **Tree.** Root (t = 0, asset-level first stage) → 20 regime-stratified nodes (t = 1–3) → L leaves each (t = 4–11).
- **Objective.** $\max\sum_sp_s[\sum_g\omega_gNAV_{g,T}-\psi_gU_{g,T}+L_T-Debt_T]-\lambda^H_T\sum_sp_s\,short_s$, less financing costs.
- **Rows per node-quarter:**
  - cash balance, NAV and unfunded transitions, debt;
  - IG + cash at 4% hard; the 8% appetite row is elastic and leaves the kernel when its slack is positive;
  - T3; leverage, exposure and encumbrance;
  - LR8 on the glide path; LR4 group budgets;
  - sale and P2S capacity by regime.
- **Global rows:**
  - a CVaR₀.₉₉₄ row on signed 12-quarter margins (the T6 surrogate);
  - T4′ robust rows on first-stage actions;
  - the blueprint's **liquidity-margin row LM** (graft 3): liquid assets + unused committed facilities × canonical credit ≥ draws + calls − distributions + IM + CVaR₉₉(VM) over 12 months.
- **Terminal values** ω and ψ come from regression, which removes end effects.

**Size and measured solve time** (bench: a structural proxy with random coefficients; another agent's benchmark was running at the same time) [I-calc]:

| Leaves | Variables | Rows | Nonzeros | HiGHS IPM | HiGHS dual simplex | CLARABEL |
|---|---|---|---|---|---|---|
| 500 (standard) | 132,153 | 102,523 | 0.52M | **20.2 s** | 109.5 s | 80.8 s |
| 1,000 | 261,153 | 203,523 | 1.02M | 136.3 s | 571.4 s | 207.5 s |

All three solvers reach the same objective (relative difference below 10⁻⁷). The cash-row duals are non-zero at every node-quarter, so λ can be extracted.

- **Production size.** Production adds about 25–35% more rows, so a 500-leaf solve should take ≈30–45 s.
- **Standard design: five independent 500-leaf SAA replications in parallel processes.**
  - This meets the 2-minute target and yields the dual and envelope bands.
  - It beats one 1,000-leaf tree, whose IPM time grew 6.7× for twice the size; that tree runs overnight as a stability check.
  - IPM duals are taken after crossover, because pinned-dual detection needs complementary slackness.

**Selection loop (Lagrangian scoring).**
1. Take the duals.
2. Score every holding-action on 1,000 CRN paths (seconds in numpy).
3. Solve a HiGHS selection MILP over ≤30 aggregated coupling rows, one action per asset (≈1,600 binaries, seconds).
4. Fix the selection and warm-start a re-solve; repeat 2–5 times with damping.
5. Bootstrap dual bands across replications (00_SYNTHESIS §4.4).

The LP splits at most one asset per binding row. Those assets form the **marginal-asset agenda** that orders the IC's group blocks.

**MPC, policy search, module F.**
- **MPC.** Root actions, after module F, become this quarter's recommendations.
- **Standing policy.** Between meetings and in simulation, a cushion-monotone policy of ≈20 parameters governs. It covers the reserve, pacing with a drought brake, leverage clip(θ9 + θ10·c_t − θ11·F_t, 1, 1.3), the hedge ratio, the recourse waterfall, a SELL screen and a top-up rule.
- **Tuning.** The policy is tuned by an in-house CMA-ES (no `cma` package) with racing on 10k CRN paths, then certified on the final plane.
- **Module F** is a QP of ≤150 variables (OSQP/CLARABEL, milliseconds). Every proposal, from the optimizer, an agent or the IC, passes through it onto the Tier-1 set, and the changes are logged.

### 4.12 Objective and constraints: the two tiers, made governable

The lexicographic structure stays (00_SYNTHESIS §4.9):
- **Tier 1A:** T1–T9 plus LM.
- **Tier 1B:** mixture median 10-year TWR ≥ 7%, and worst-model CVaR10% ≥ 0%.
- **Tier 2:** $J(\theta)=\sum_mw_m\{\mathbb E[U_3(\widetilde W^{real}/W_0)]-\lambda_T(\mathbb E[(1-\widetilde W/\widetilde W^\star)^2_+])^{1/2}\}$, with payouts accruing at the fund's own return.

Three changes make it governable:
1. **Bands are governance objects.**
   - T6 is banded by model class: 0.5 / 1 / 2% for M1–M5, and — / 2.5 / 5% for M6 (gap_02 §3).
   - A tolerance breach triggers the CFP Amber playbook; a capacity breach triggers recovery and a Board item.
   - The IC ratifies bands and model weights each year (A1, A2), and the pack prices them: at ε_R = 1%, 21bp a year with the owner band vs 62bp without.
2. **An admissible value set Θ** constrains seat utilities: γ ∈ [2, 6]; λ_T ∈ [0, 2]; shortfall exponent ≥ 1; a T6 limit no looser than the IC's tolerance; extra costs only on engine metrics. No indicator terms are allowed (L9).
3. **Rule by reversibility.** Reversible actions take the pooled-belief optimum. Irreversible ones take minimax regret over the finite credal set. Max-min is a diagnostic only (C4 §6.6).

Anti-target-chasing safeguards: no indicator terms; a cushion-monotone type rule; a gambling detector.

### 4.13 Robustness

- **Layering.** Model ensemble → KL/W∞ balls (η = 0.05, anchored on the 0.02–0.06 nat cross-provider divergence; η_L = 0.01 for rare events) → reverse stress.
- **Metrics.** R1–R8, including k_MS (bp of floor per 0.01 nat) and the breakdown divergence η\*.
- **Reverse stress** is the minimum-KL tilt to failure with a Pesenti ranking. The Red Team must beat the GW → SG → DB benchmark (00_SYNTHESIS §4.10).

### 4.14 Attribution

- **Order.** Prices first (λ with bands, reduced costs), then counterfactuals (forced re-solves, capability values, price of safety), then exact Shapley over ≤6 action groups on CRN.
- **Group value added:** $DVA_g=\sum NAV_i(r_i-r^{FB}_i)-FTP^{vint}_g-\lambda_RRC_g+CR_g$.
- **Anticipation audit** on every attribution. v8's +3.5pp survives only as `test_v8_replica`; the new engine gives +0.35–0.61pp (gap_05 §8).

## 5. Agentic layer

### 5.1 Roles

| Role | Does (tools) | Output | Gate | Family |
|---|---|---|---|---|
| Contract Drafter | Drafts contracts and Register amendments (`phase1_restore`) | ContractDraft | G0, human signs | A |
| Design Reviewer + Alignment Judge | Assesses and repairs the design; checks evaluator independence (paper: one reviewer, l.194–195) | DesignReview | G1 | A + B |
| Quarantined Extractors ×2 | Dual extraction from memos and GP notices; no outbound tools | ExtractRecord | schema + human sample | A |
| Ideators ×2 | Propose packages and PolicySpecs as columns (`evaluate_policy`, search plane) | IdeaBundle | G3–G5 | A |
| Red Team | Reverse stress; objective devil's advocate (`ep_condition`) | RedTeamReport | disclosed at G8 | B |
| Brief Composer | Writes briefs from registry metrics (`get_metric`, `validate_claims`) | BriefText | G7 | A |
| Auditor | Checks that sources support claims, using logs and engine diffs | AuditReport | G8 | B |
| Shadow-IC seats ×12 | Assess, argue, file minority reports (`implied_actions`, own evidence slice) | SeatAssessment | rubric | ≥3 families (target) |
| Facilitator | Runs the protocol; introduces no claims | — | — | A |
| Translator | Turns natural-language what-ifs into ViewSpecs, confirmed with the member | ViewSpec | human confirms | A |
| Q&A Answerer | Grounded answers, each labelled model output / agent judgment / assumption | Answer | claim validator | A |
| Minutes Drafter | Drafts minutes; dissent recorded verbatim | Minutes | secretary approves | A |

### 5.2 Typed tools

**MCP tools:** `state_snapshot`, `phase1_restore`, `optimize_hn`, `price_action`, `evaluate_policy` (bounded aggregates only), `implied_actions(seat, views, theta)`, `ep_condition`, `evsi_crossfit`, `flip_thresholds`, `bridge_card`, `group_envelopes`, `overlay_offset_card`, `robustness_card`, `attribute`, `get_metric`, `validate_claims`, `register_forecast`, `log_assumption`, `escalate`.

**Schemas and calls.**
- Each tool is a pair of Pydantic models with `additionalProperties: false` and `strict: true`.
- Typed outputs come from `client.messages.parse(output_format=Model)`.
- `tool_choice="auto"`, because Opus 5.5 rejects forced tool choice.
- Effort is set explicitly per role (the default is `medium`).
- Refusal fallback: `betas=["server-side-fallback-2026-07-01"]`, `fallbacks="default"`.

### 5.3 Meta-controller (plain Python)

SNAPSHOT → BELIEFS_FROZEN (G2) → CONTRACT_CHECK (G0; SIGNED or SIGNED_IN_RECOVERY) → EVIDENCE_BUILD → OPTIMIZE → [IDEATION ⇄ SCREENING (G3–G5)]\* → SEALED (G6, once) → RETROSPECTIVE → BRIEFS (G7) → AUDIT (G8) → SHADOW_IC → PREVOTE_LOCK → IC → RECORD (G9) → MONITOR.

ESCALATE is reachable from every state. The loop stops when the budget is spent, after 6 cycles without a promotion, or when no column has a positive robust reduced cost.

**Planes.** Four planes are separated:
- *human decisions:* sponsors sign, MRM validates, the IC decides;
- *control:* the meta-controller, with no LLM in its control flow;
- *LLM roles:* no write access to engines, evaluators, beliefs or scenarios;
- *engines:* hashed, behind the evaluator.

The data planes (search, final, misspecification; §4.3) keep separate caches, and the final plane is run once.

### 5.4 Gates

| Gate | Pass condition (all checks engine-owned unless stated) |
|---|---|
| G0 contract | Phase-I u\* = 0, or signed in RECOVERY with u\*, the IIS, the glide path and Board sign-off |
| G1 design | Reviewer, judge and human agree: evaluator independent, planes disjoint, controls declared |
| G2 freeze | State and beliefs hashed; flagged assets reviewed |
| G3 admissibility | DSL checks: observation lags; cushion- and loss-monotonicity; no identity or horizon features |
| G4 `correct` | Hard constraints, budgets, no leakage, non-inferiority vs HOLD in every search world (worst world aggregated); failed paths scored as worst case |
| G5 selection | Paired CRN lower bound of ΔΨ > ε_mat (3 / 5 / 10 / 15bp for overlay / pacing / REFI-LEVER / SELL); ties keep the incumbent |
| G6 qualification | Intersection–union test across disjoint worlds; Holm; CP bounds vs T6 bands; PBO ≤ 0.20; 3.47σ deflation at N = 200. Otherwise NOT ESTABLISHED (`not_qualified`) |
| G7 brief | Claim coverage = 1; plane labels; ICD-203; required P14 fields |
| G8 audit | Family-B auditor PASS with ≤4 findings; both verdicts printed |
| G9 record | Pre-votes locked; ballot, dissent, overrides with reason codes, signposts, review date |

Rubrics that agents check themselves are diagnostics only (brief P5).

### 5.5 Budgets, memory, escalation, review, offline mode

- **Budgets.** The evaluator counts every evaluation, failures and retries included. LLM spend is capped at $50 soft / $200 hard per cycle. α-investing runs with W₀ = 0.05, and wall clock is bounded. IC attention (§6.6) is a budget the compiler enforces.
- **Memory.** An append-only log plus ≤300 words of conclusions per campaign; a curator signs flips. It is never evidence, never crosses campaigns and never sees the final plane. Institutional memory lives only in the forecast registry and the decision log.
- **Escalation.** `escalate()` blocks High-tier roles until a human answers. `log_assumption()` is mandatory, and open assumptions print in every brief. The paper's agents assume rather than ask (l.6406–6408).
- **Cross-family review** runs through `LLMBackend` (Anthropic default; Bedrock, Vertex and Foundry clients). Without a second approved family, isolated same-family review is labelled "correlated".
- **Offline.** `StubBackend` returns deterministic, schema-valid outputs. `ReplayBackend` replays cassettes keyed by the SHA-256 of role, prompt version and inputs. Opus 5.5 has no sampling controls, so replay is the only way to get deterministic agent tests.

## 6. IC layer

### 6.1 The Decision Register

The Register is a signed YAML catalogue compiled into typed objects:

```python
class EvidenceSpec(BaseModel, frozen=True):
    metric: str                     # registry id, e.g. "tier1.T6.cp_upper"
    by: tuple[str, ...] = ()        # ("model",), ("group",)
    plane: Literal["final", "search", "exploratory"] = "final"
    max_age_days: int = 31
class DecisionType(BaseModel, frozen=True):
    id: str; proposer: Role; decider: Tier; cadence: Cadence; deadline_rule: str
    variables: tuple[DecisionVariable, ...]
    always_show: tuple[OptionKind, ...] = ("status_quo", "defer", "recommended")
    evidence: tuple[EvidenceSpec, ...]; signposts: SignpostRule
def compile_agenda(reg: Register, q: Quarter, snap: StateSnapshot) -> EvidencePlan: ...
```

The EvidencePlan is a DAG of RunSpecs keyed by content hash and deduplicated across decisions. A brief renders only if every EvidenceSpec resolves. Otherwise it shows "EVIDENCE MISSING: ⟨metric⟩" and is never silently filled.

| ID | Decision (variables) | Proposer → decider | Cadence / deadline | Minimum evidence | Engines |
|---|---|---|---|---|---|
| Q1 | Fund state: CFP stage, Tier-1 status, recovery path | CRO + Treasurer → IC (Board if amber/red or in recovery) | Quarterly; on stage change | State panel; Tier-1 board; survival under T4′; Phase-I u\*, IIS, infeasibility prices | state, ledger, core |
| Q2 | Owner-draw response: funding of the next 4 instalments, reserve top-up, band trigger | Treasurer (owner's advocate) → IC; band → Board + owner | Quarterly; 10 days before an instalment | Draw fan by Z; recourse waterfall and marginal cost of liquidity; T8 by shock type; $J^*_A-J^*_B$ | liab, ledger, core |
| Q3 | Buffer, funding, portfolio leverage (HQLA target, revolver, facility programme, exposure 1.0–1.3×) | Treasurer decides funding; CIO proposes exposure → IC if outside band | Quarterly; lead time 6–12 weeks | LR1–LR8; λ by regime and horizon; covenant P(trigger); cushion c_t; doctrine tests | ledger, core, overlay |
| Q4 | Envelopes and FTP; contingent budgets | TPA + CF → TPC/IC (heads recuse) | Quarterly | Envelopes with SAA ranges; itemized charges; elasticity; priced requests | icm, core |
| Q5 | Pacing by group within the corridor | Group heads → group (Green), CIO (Amber), IC (Tier A) | Quarterly | Pacing MPC; unfunded by vintage; cut cash profile; forgone α\*; co-investment flow | priv, core, icm |
| Q6 | SELL/HOLD/REFI/LEVER cards (marginal-asset agenda) | Groups (CF for facilities) → group / CIO+CRO / IC | Quarterly; on events | DecisionCard with `priced_on` | actions, beliefs, core |
| Q7 | Overlay: tail budget, monetization triggers, opportunistic budget, synthetic beta | Overlay head → IC (Tier A if tail change > 10bp/yr) | Quarterly | Offset card; hedge decomposition; DSR; IM by CSA; carry tracker | overlay, ledger |
| Q8 | HF notices (irrevocable) and P2S conversions | Public Markets → CIO+CRO; pre-approved at Amber | Dealing dates | φ_i(h,S); redemption rule; P2S VM in a −33% month | pub, overlay |
| Q9 | Internal transfers; conflicted quotes; contingent-budget releases | Groups → pricing committee → Tier B/A | As they arise | Zero liquidity; fair value on both legs; ≥2 external bids or a 20% strip | icm, actions |
| Q10 | Signpost reviews | Monitor → Tier B (alarm) / Tier A (flip) | Monthly | Distance to flip | idm, state |
| A1 | Tier-1 contract: θ\*, T6 bands, ε_R, floor, T_rec | CRO → IC → Board | Annual | ε_R–cost frontier; price of safety per row | core, robust |
| A2 | Model weights and the bridge | CIO → IC vote | Annual | WYNTB per model; P(μ ≥ 10%) | bridge |
| A3 | FTP and envelope methodology; c_buf | CF → IC → Board | Annual | Decentralization test; mismatch P&L | icm |
| A4 | Pacing plan P\*_g, core sleeve, overcommitment limit | CIO → IC | Annual | Pacing MPC; LR8 path | priv, core |
| A5 | Leverage limits and facility programme | Treasurer → IC → Board | Annual | Doctrine; facility need under T4′ | ledger, core |
| A6 | Mandate proposal to the owner (band, draw convention, payout rule) | Treasurer → IC → Board + owner | Budget cycle | $J^*_A-J^*_B$; four owner dimensions | liab, core |
| A7 | Convex budget; opportunistic limits; OV thresholds | Overlay head → IC | Annual | Hedge valuation; DSR | overlay |
| A8 | Credibility release; pay KPIs | CRO office → IC informed | Annual | WIS, bias, κ, information value | beliefs, idm |
| A9 | Model revalidation, including the room itself | MRM | Annual | Harness results | all |
| E1 | GP-triggered events (CV elections, LPAC votes, recaps) | Group → by size tier | ≥30 days | Card | actions |
| E2 | Expiring bids and financing windows: letting one lapse is a decision | Group/CF → CRO if loss > 0.25% of NAV | Expiry | Card + irreversibility check | actions |
| E3 | CFP stage change → pre-approved playbook | Treasurer (Green), CIO (Amber), IC weekly (Red), Board + owner (Black) | Immediate | Stage triggers | ledger |
| E4 | Owner override or unscheduled draw | Treasurer → IC | Immediate | Draw and coverage | liab, ledger |

Tier A covers actions ≥ 0.25% of NAV (≈$0.44bn), secondary discounts > 10%, LTV up > 5pp, or a tail-budget change > 10bp a year (00_SYNTHESIS §6.1; GROUPS §7.3).

### 6.2 Cycles

**Quarterly cycle.** T−21 snapshot and G2 freeze. T−18 group forecasts, proposals and quotes. T−14 evidence build, Phase I, H-LP, sealed runs. T−10 S0. T−7 pack published, S1. T−1 human pre-vote locks. T meeting. T+5 log closed, signposts armed. A1–A9 run in Q4. Event decisions run a compressed protocol (S1, S5, H0, H4).

### 6.3 The IC pack

- **L0 "Fund on a page":**
  - CFP stage and survival under T4′;
  - Tier-1 summary by model-class band;
  - the owner draw for the next 4 quarters and its funding;
  - λ and the FTP change;
  - the WYNTB verdict by model;
  - the package vs controls and archetypes A/B/C (ΔCE, P(red) by class, P(10%) reported);
  - this quarter's decisions with deadlines;
  - the 12-row state panel (gap_04 §8).
- **L1 briefs** (one page each; ≤6 pages per Tier-A item) follow a fixed anatomy:
  1. question, deadline, decider, recusals;
  2. options: status quo, DEFER, recommendation, alternatives;
  3. consequences: ΔTier-1 by class with CP bounds; ΔJ in bp and $ (1bp ≈ $17.7m a year); Δsurvival months; ΔP(10%) reported only;
  4. economics: λ-priced waterfall, binding constraints, shadow prices, marginal value per action, envelope use, `priced_on`;
  5. beliefs: raw vs fused, market anchor, information value, flags;
  6. disagreement: implied-action map, belief/value split, minority reports with authentic ones first;
  7. what would change it: flip thresholds, signposts, cross-fitted EVSI when DEFER is live.
- **L2 drill-down.** Every number is two clicks from `run_id:artifact:path`.
- **Visual grammar:**
  - "37% [26–38%] ± 0.2pp" with the scenario hash;
  - ICD-203 words;
  - greyed if |Δ| < 2 paired SE;
  - P(10%) always shown beside P(red);
  - SYNTHETIC footer when tainted;
  - a linter rejects cross-group league tables.
- **Usability acceptance** (tested in `tests/room` and by IC user testing):
  - L0 can be read in ≤ 5 minutes;
  - every number is ≤ 2 clicks from its manifest;
  - W1 answers in < 1 s;
  - the pack is published by T−7;
  - no item reaches the ballot with an unmet evidence contract.

### 6.4 What each seat sees each quarter

| Seat | First screen | Standing question |
|---|---|---|
| Every IC member | L0; ballot list; own pre-vote history and private Brier score | What must we decide, by when, and what would change it? |
| CIO | Bridge by model; package vs archetypes; envelope coherence; net α\* after charges | Does the package earn its Tier-1 cost? |
| CRO | Tier-1 board, CP bounds, class bands; recovery; k_MS, η\*; gambling flags; OV1–OV3 | Which gate binds, in which model class? |
| Treasurer | LR1–LR8; CFP triggers; facility and covenant headroom; VM/IM by CSA; draw fan; FTP (decision vs published); mismatch P&L | Can we pay the next four instalments in the binding state without a red sale? |
| PE | Corridor; unfunded by vintage; marginal-fund cards; pending CVs; information value | Is the cut priced as forgone α\* and lost co-investment flow? |
| Secondaries | Contingent-budget triggers; desk score vs consensus; deferred payables | Is θ/p > 1 after staleness, with both triggers on? |
| Co-investment | Accepted vs needed flow; single-asset cards; effective N | Which growth and exit multiple must hold? |
| Capital Solutions | Break-even IRR at ℓ̄; PIK book; reserve-price record; cash-carry row | Does the deal clear $(1+r_h)(1+\bar\ell)-1$ on drought cash? |
| Private Credit | Run-off value; sale vs run-off break-even ℓ̄; LGD pair per card | Which sleeves run off at Amber? |
| Public Markets | Terms τ, φ(h); notice calendar; P2S cards with VM in a −33% month | Which notices go in at Amber? |
| Overlay | Offset card; convex budget and carry; triggers; DSR; IM by CSA | Do OV1–OV3 hold, and what does the hedge buy in λ? |

### 6.5 The shadow IC: computed opposing utilities

Twelve mandate seats (GROUPS §7.1), each a declared pair (q_k, θ_k) with θ_k ∈ Θ. The blueprint's opposing utilities survive (graft 4), but no seat maximizes P(10%).

| Seat | Belief channel q_k | Values: γ, λ_T, T6 limit, extra costs |
|---|---|---|
| CIO (return architect) | IC base mixture | 2, 2, 1%, — |
| CRO | Worst model class | 3, 1, 0.5%, k_MS |
| Treasurer (liquidity guardian; owner's advocate) | Base + owner stress (draw at P90) | 5, 0.5, 0.5%, owner financing cost ×2, T7 shortfall |
| Seven group heads | Own group's forecasts at face value | 3, 1, 1%, plus the mandate's loss term (κ^GP; dry-powder option value; concentration; PIK/kicker; LGD ambiguity; adverse selection; hedge fatigue and hidden short volatility) |
| Outside-View Forecaster | Reference-class priors only | 3, 1, 1% |
| Red Team (objective DA) | Minimum-KL failure world against the recommendation | — |

- **Implied action and regret.** $a^*_k=\arg\max_{a\in\mathcal A_{T1}}J(a;q_k,\theta_k)$, computed by `implied_actions` (W2 on cached paths). Regret is $R_k(a)=J(a^*_k)-J(a)$ under seat k's beliefs and values.
- **Two kinds of disagreement.** A two-factor Shapley split separates belief from value. Belief splits go to diligence; value splits go up the delegation chain.
- **Minority reports** trigger at |Δp| ≥ 15pp or a regret ≥ 10bp (00_SYNTHESIS §6.5).
- **The politics become measurable.** Group seats hold their forecasts at face value. The belief part of a head's disagreement is therefore the decision value of the gap between their forecast and the fused belief; the value part is the mandate's loss emphasis.
- **Recusal.** A head's implied actions on their own envelope are shown but excluded from the pool.
- **Diversity alarm** if the pairwise rank correlation between seats exceeds 0.9.

**Protocol** (00_SYNTHESIS §6.3, updated by 14 lit check §4–5):
- **S0:** 8–15 frozen questions per Tier-A item.
- **S1:** blind seat pre-votes (probabilities, MAP scores, implied action, top artifacts, "what would change my mind"), hashed.
- **S2:** reveal; cruxes ranked by value of information.
- **S3:** **one** debate round by default. A move > 5pp needs a new validated artifact. An influence cap applies, and conflicted quotes need a second source.
- **S4:** pre-mortem; competing hypotheses on whether the DPI decline is cyclical or structural.
- **S5–S7:** minority reports, questions, package.
- **Dissent order.** Authentic minority reports come first. The Red Team's output is labelled *assigned dissent* and targets the recommendation and, after H1, the human majority (Schwenk 1990; Nemeth 2001; Schulz-Hardt 2002).

### 6.6 The human meeting, Q&A and view conditioning

**Flow (H0–H6):**
- **H0, blind pre-vote** on the fact pack (no AI narrative, shadow map or minority reports). It locks at T−1.
- **H1, reveal:** human dispersion → model baseline → shadow map → minority reports.
- **H2, cruxes** on the console, plus an integration step: which facts held by one person change a score?
- **H3, pre-mortem** led by a rotating human devil's advocate.
- **H4, simultaneous ballot:** approve / resize / defer / reject, with probabilities, rationale and "what would change my mind", then a second-chance check.
- **H5, minutes** drafted by AI, approved by the secretary, dissent verbatim.
- **H6:** signposts armed.

**Agenda and attention budget (180 min):**
- A. Total portfolio, 40 min (Q1–Q4).
- B. Group blocks, 90 min, ordered by decision value at stake (minimax regret in $ + EVSI).
- C. Cross-group, 20 min (Q9, offset card, collateral).
- D. Ballot, 30 min.

**Consent agenda.** An item goes there only if P(best) ≥ 0.8 in every model class, no minority report triggers, minimax regret ≤ materiality and no Board trigger applies. Any member can pull an item, with a logged reason. At most 4 Tier-A items per meeting.

**Decision rules:**
- **DEFER** only if the 80% lower bound of cross-fitted EVSI exceeds the cost of delay, no staged action dominates and there are < 2 prior deferrals.
- **Symmetric irreversibility.** Forfeiting an option worth > 0.25% of NAV, including letting a window lapse, needs a second-chance check and CRO sign-off.
- **Recusal is enforced in software:** the vote is recorded but not tallied.
- Heads challenge but never veto.

**Q&A and what-ifs.**

| Mode | What | Latency | Label |
|---|---|---|---|
| Ask | Grounded Q&A citing `run_id:artifact:path`; "not in the artifacts" is allowed | seconds | model output / agent judgment / assumption |
| W1 | Entropy-pooling re-weighting inside the pack | < 1 s | exploratory |
| W2 | Re-fusion and re-optimization on cached CRN paths | 1–5 min | exploratory |
| W3 | Re-simulation with a tilted sampler (MCP Task) | overnight | confirmatory if sealed |

**View conditioning** has two channels (00_SYNTHESIS §6.4):
- **Asset-return views** become FBE signals, with ω = (P90 − P10)/2.563 until the member has been scored.
- **Scenario, cash-flow and regime views** go through entropy pooling. The target is shrunk first, $v^{eff}=\mathbb E_p[g]+c(v-\mathbb E_p[g])$, then solved exactly by minimum KL. The member confirms the *effective* view: at c = 0.6, "30% below" becomes 18% below.
- **Flags:** KL > 0.05 inform, > 0.25 warn, > 1.20 amber, > 2.30 forces W3. Effective sample size must stay ≥ 5,000.

**Worked example** (graft 7): "Buyout forecast 16% realizes at 8%, spreads +250bp".
- The Translator emits an FBE ViewSpec (PE buyout forecast = 8%) and an EP ViewSpec (HY spread +250bp over 4 quarters).
- It shows the effective views, KL and ESS.
- Once confirmed, W2 re-scores the cards and W1 re-weights the paths.
- An irreversible Tier-A action decided on exploratory evidence needs a confirmatory sealed run before execution.

**Client-side entropy pooling** (brief decision 14):
- The pack embeds 10,000 paths × ≈40 metrics in float16 (≈0.8 MB), about 30 view functions and a ≤150-line JS dual-Newton solver.
- On opening, it runs golden cases against Python reference outputs and disables W1 on any mismatch > 10⁻⁶. With no Node in the environment, this in-browser self-test is the check.
- There is no neural surrogate (brief §6).

### 6.7 Decision log and signposts

```python
class DecisionRecord(BaseModel):     # append-only, bitemporal, hashed
    decision_id: str; register_id: str; as_of: date; tier: Literal["A", "B", "C", "Board"]
    options: list[OptionSummary]; engine_recommendation: str; evidence_plane: Literal["final", "exploratory"]
    run_manifests: list[str]; prevote_hashes: list[str]; ballots: list[Ballot]; decision: str
    override: Literal["belief", "value", "info_outside_model", "implementation", "legal_consent",
                      "relationship", "other"] | None
    rationale: str; minority_reports: list[str]                  # hashes; text verbatim
    signposts: list[Signpost]; commitment_plan: list[ContingentAction]; review_date: date
    outcomes: dict[Literal["q1", "q4", "q8"], OutcomeScore] = {}
class Signpost(BaseModel):
    indicator: str; flip_value: float; alarm_value: float; rearm_band: float   # alarm 0.5σ safe side; re-arm 0.25σ
    owner: Role   # alarm -> Tier-B review; flip -> Tier-A re-decision
```

- **Signposts.** 3–6 per decision, drawn from the pre-mortem. Each flip value comes from root-finding on $J(a_c;q(z))=\max_{a\neq a_c}J(a;q(z))$. They are monitored monthly.
- **Commitment plan.** Pre-committed contingent actions guard against committee dynamic inconsistency. The log tracks plan consistency and DEFER frequency (Garlappi 2017, via 14 lit check §4.2).
- **Scoring.** Every ballot probability is Brier-scored at 1, 4 and 8 quarters. Overrides carry reason codes.

### 6.8 Politics: forecast credibility and transfer pricing

| Credibility rule | Mechanism | Basis |
|---|---|---|
| A weight on information, not a grade | Show **information value** in $: decision value with vs without the group's forecast (W2), and the share of actions it changed | G8 §6.6; GROUPS §7.4 |
| Own reference class only | Shown only at n_eff ≥ 20 (SE ±8.9pp at n = 20) | GROUPS §5 |
| No league tables | Enforced by linter; individual scores private | GROUPS §7.4 |
| Symmetric | WIS penalizes sandbagging (width) like optimism (coverage) | GROUPS §5 |
| A forecast cannot buy budget | Budgets move only through envelopes and duals; elasticity shown ("+100bp of credible α\* buys $X bn") | L14; G8 §6.3 |
| Pay decoupled from budget | Linear in vintage-FTP DVA, with ≤10 points for WIS | L8; G8 §6.8 |
| Recovery needs catalysts | Milestones; P(achieved within k quarters); Zombie-NAV flag | graft 2 |
| A route to contest | Groups file evidence against their bias estimate with the validator; decided within the quarter, logged; the IC does not adjudicate | [I] |

| Transfer-pricing item | Rule |
|---|---|
| Decision prices | Undamped restored duals; no floor; c_buf = 1.5% is a ceiling (GROUPS §4.3; G8-R2–R5) |
| Published curve | EWMA, 2-quarter half-life, ±50% collar, on liquidity tenor |
| Performance charges | Vintage-locked; CF books the mismatch as DVA_CF |
| Contingent liquidity | $CLC_g=c_{buf}\sum_h\omega_hO^{stress}_{g,h}$ ≈ $0.2bn a year, charged once; contractual inflows and crisis payoffs credited |
| Disputes | Transfer-pricing committee (CRO office), 10-business-day SLA; methodology approved by the Board annually |
| Transparency | Own itemized charges; peers' charges only in aggregate |
| Recovery | Infeasibility prices never posted; CI fails pinned-dual cards |

### 6.9 Evaluating the room

An online trial is infeasible: it needs ≈6,300 effective forecasts per arm (00_SYNTHESIS §6.6). Evidence comes instead from:
- **Shadow mode** for 6–12 months.
- **Offline suites:** hidden-profile decision accuracy; seeded errors, including for senior members; sycophancy tests.
- **KPIs:** reliance split by whether the model was right (over- and under-reliance); override accuracy; dissent rate; DEFER frequency; anti-portfolio returns; an annual legitimacy survey (14 lit check §4.5).

## 7. Data and synthetic generator

**Schemas.** Parquet + Pydantic; every row carries `is_synthetic`, provenance, units and basis tags. The hierarchy is `taxonomy(group → strategy → sub_strategy)` with holdings at the leaves.

| Table | Key | Notable fields |
|---|---|---|
| holdings | holding_id, quarter | group, strategy, sub-strategy, vintage, GP, unfunded by vintage, NAV + date, consent/ROFR/pledge flags, wrapper |
| marks | holding × {u, a, f, m} × valid time × recorded time | value, basis, horizon, author, revision, milestones |
| cash_flows | holding × date | type, amount |
| quotes | event | bid % NAV, deferral, source, `conflict_flag`, second source |
| hf_terms | lot | τ: notice, revocability, gates, dealing, lag, holdback, side pocket, consents |
| overlay | trade, day | template, CSA, CRIF sensitivities, VM/IM |
| funding, owner | facility; year | terms and covenants; rule, draw convention, draws |
| forecast_registry, decision_log | record | quantiles, snapshot, decision link; §6.7 |

**Roll-ups.** Group roll-ups are views. Intra-ADIC transfers are flagged, netted at zero liquidity and booked at fair value on both legs (gate V2).

**Ground truth** (GROUPS §6). Three layers: world, sealed truth, observation.
- **Census v1.0:** ≈395 positions, ≈1,500 loans and ≈250 trades; $177bn NAV; $38bn unfunded.
- **Truth:** skill $a_v=-0.05z_v+u_v$ (GP effect 3%, idiosyncratic 2.5%); NIG shocks; co-investments drawn from BJS quartiles; both private-credit loss pairs.
- **Observation biases:**
  - Smoothing of 0.5 (buyout), 0.6 (VC) and 0.5–0.7 (private credit); 1-quarter lag; BGK manipulation of 2.6pp per SD.
  - Underwriting $u=\bar\mu+0.3(\alpha-\alpha_s)+b^u+\gamma'x$, with +2pp for leverage > 6×.
  - Forecasts $f_t=0.6f_{t-1}+0.4[w_uu+w_aa+(1-w_u-w_a)f^*+b^f]+\eta$, with timing optimism after spread shocks.
  - Market bids from the hedonic model.

**Checks:**
- V1–V23. Identities and netting. Stylized facts (V3–V13): distribution rates vs MSCI ±2pp, AC1, secondary prices vs Jefferies ±3pp, private-credit loss 0.8–1.2%. Estimators: SBC, parameter recovery ±5pp, CRPS skill > 0, regret vs oracle. Labelling at 100%.
- Planted-bias recovery of b^u, b^f and κ_g per group.
- Truth is sealed from agents and estimators.

**Labelling** (L1–L8): `SYN-` ids; a footer on every page; taint propagation; the validator rejects any text attributing synthetic numbers to ADIC; `data_class ∈ {SYNTHETIC, REAL}`, with mixed data a hard error.

**Adapters** validate against the same schemas. First requests: hedge-fund terms τ, PE unfunded by vintage, the overlay blotter and CSAs, and the owner draw convention (00_SYNTHESIS §7.2).

## 8. Package layout and build order

```
adic_tpa/
  contracts/ data/ synth/ scen/ state/ priv/ pub/ overlay/ liab/ beliefs/ ledger/
  actions/ icm/ core/{phase1,hn,select,sim,search,filter,mpc}.py robust/ bridge/ attrib/
  lab/ agents/ idm/ (register.yaml, compiler, briefs, shadow, ballot, log, signposts) pack/ (jinja2, plotly, ep.js)
  cli/ mcp_server/
tests/ unit/ property/ metamorphic/ regression/ recovery/ room/ e2e/
```

| Stream | Modules | Depends on | Starts |
|---|---|---|---|
| S1 Contracts & data | contracts, data, synth | — | week 0 |
| S2 World | scen, state, liab | S1 | week 1 |
| S3 Book engines | priv, pub, overlay, beliefs | S1 | week 1 |
| S4 Ledger & decisions | ledger, actions, core, icm | S2–S3 interfaces | week 2 |
| S5 Evidence | lab, robust, bridge, attrib | S1 | week 1 |
| S6 Decision room | idm, pack, agents, cli, mcp_server | S1, S5 | **week 1, on fixtures** |

The IC-first payoff: the room is usable on recorded fixtures before the engines are finished.

**MVP: the decision-room MVP** (10–12 weeks). One quarter's pack runs end to end, offline, on SYN-ADIC-177.
- **Decisions:** Q1 (with Phase I), Q2, Q4, Q5 (PE) and Q6 (top-20 cards by group).
- **Room features:** L0 with archetypes A/B/C; W1; the shadow IC on `StubBackend`; pre-vote, log and signposts.
- **Engines:** M1, M6 and the held-out generator; the fund-interest and claim engines; the HF machine; Level-1 overlay; ledger; FBE with planted biases; the 500-leaf H-LP; P; module F.
- **Exit test:** it answers the six MVP questions of 00_SYNTHESIS §10.

| Tests | Examples |
|---|---|
| Unit | Engine equations; VM by CSA; WIS; entropy-pooling dual |
| Property | Cash identity; NAV ≥ 0; LEVER ≡ ADD + REFI; envelopes within slack; netting = 0 |
| Metamorphic | Wider discount ⇒ no more discretionary SELL; costlier facility ⇒ no more REFI; tighter band ⇒ smaller feasible set; scaling invariance; a dominated option leaves the recommendation unchanged |
| Regression | `test_no_pinned_duals.py` (8/8); `test_v8_replica` (±0.05pp); bridge vs verifier 10 |
| Recovery | FBE biases, κ_g, F_t calibration and the owner model on SYN truth with SBC |
| Room | Every Register entry renders; incomplete briefs rejected; seeded numbers caught; recused votes excluded; pre-votes immutable; JS = Python entropy pooling on golden cases |
| End-to-end | `adic-tpa quarter --synthetic` builds the pack offline in < 30 min |

## 9. Key choices versus alternatives

| # | Choice | Rejected alternative | Evidence |
|---|---|---|---|
| 1 | The Register compiles the evidence graph | An engine-first pipeline feeding a dashboard | The paper validated only hand-prepared contracts (brief P8); IC attention is scarcer than tokens (00_SYNTHESIS §5.7) |
| 2 | Seats' numbers come from `implied_actions` | LLM personas producing numbers (blueprint §3.2) | P1; caricature risk (GROUPS §7.1); persuasion gains came with accuracy losses (00_SYNTHESIS §6.6) |
| 3 | Opposing utilities confined to Θ | A "Total Return Architect" maximizing P(CAGR ≥ 10%) | Digital option: P(target) 34% → 68% with a 4.6% chance of a > 40% loss (L9) |
| 4 | Objective devil's advocate; authentic dissent first | A standing assigned devil's advocate plus dialectical inquiry everywhere | Schwenk 1990; Nemeth 2001; Schulz-Hardt 2002 (14 lit check §5) |
| 5 | Pooled beliefs for reversible actions, minimax regret for irreversible ones; symmetric irreversibility | Max-min; a ⅔ supermajority | Max-min gives the most pessimistic member a veto; a supermajority tilts toward HOLD (C4 §6.1, §6.6) |
| 6 | W1 entropy pooling plus engine reruns | A neural-operator surrogate | Brief §6; P1 |
| 7 | Five parallel 500-leaf LP replications with Lagrangian scoring and a small MILP | An asset-level stochastic MILP (≈1.8M variables, 00_SYNTHESIS §4.8) | No commercial MILP; bench 20.2 s vs 136 s; three prices reproduced 36 of 40 exact decisions (00_SYNTHESIS §4.4) |
| 8 | Credibility as information value, own class, n_eff ≥ 20, pay decoupled | League tables; credibility-weighted budgets | δ\* = bZB′/(2s) (L8; Boutilier 2011) |
| 9 | Two FTP price sets; CF holds the mismatch | One curve; a price floor | G8 R2–R5; CEBS vintage locking |
| 10 | Blind human pre-vote; under-reliance tracked | AI view first | Human–AI teams g −0.23 (L13); Kokje 2026 |
| 11 | Market-implied fourth signal via pricing committee + second source | Desk quotes as prices | Graft 1; quotes are evidence, not prices (00_SYNTHESIS §2.2) |

## 10. Risks, and what this proposal leaves out or defers

| Risk | Effect | Mitigation |
|---|---|---|
| **Process burden and legitimacy (the biggest risk)** | The room becomes ritual; decisions route around it; heads resist credibility scores and FTP | Attention caps; consent agenda; pilot on Tier-B first; shadow mode; private scores; legitimacy survey; CIO owns the Register |
| A simulator that verifies itself | False precision on a shared misspecification | Model ranges lead every number; held-out generator; k_MS; NOT ESTABLISHED |
| LP scale on real data | IPM time superlinear in size | 500-leaf replications; warm starts; decomposition by subtree; benchmark gate in sprint 1 |
| Seats too similar | Shadow IC adds noise | Diversity alarm; spread across Θ; seat ablation |
| Conflicted quotes; lobbying | Anchoring; capacity won by persuasion | Firewall; second source; envelopes priced at the dual |
| Owner refuses the band | M6 breaches capacity → recovery | Recovery mode built in; Mix A path (gap_02) |
| Client-side entropy pooling not testable in CI | Wrong W1 numbers | Golden self-test; W1 labelled exploratory; Python reference |

**Deferred.** SDDP water values and the structural owner model (Phase 2). Level-2 overlay pricers and Benders decomposition (Phase 1). Deep RL (R&D). Surrogates. Verbatim transcripts (restricted). More than two model families until approved.

**Excluded.** Any execution.

## 11. Brief §5 decisions 1–21

1. **Time grid.** Quarterly decisions; monthly ledger/HF and daily stress sub-steps; 40 quarters; 3/5/10-year windows. 10% = 10-year geometric TWR, nominal, distribution-inclusive.
2. **State.** Cohorts in P (≈3,340 float32 per path, ≈0.5 GB for 10k paths); holdings with CRN for cards. Kernel bench: 3.96 s.
3. **Scenarios.** Regime-switching factor model (S/e/Z chains, ≈20 factors, vol states); six CMA-anchored models + held-out bootstrap; planes hashed at G0.
4. **Private engine.** RFT-TA v2 on two clocks; economic vs reported NAV; drought via e_t (D 0.87) and Φ; beliefs as per-path $\bar\alpha_i$.
5. **Instruments.** §4.6: hedonic secondaries; NAV loans (SOFR+300bp, pledge cap ≈$2bn); preferred 12–14%; GP-triggered CVs; CFOs. Each has regime availability and a one-off premium L_s ≈ 17.5–23.7%.
6. **Overlay.** Position layer; OV1–OV3; VM by CSA; SIMM-like IM; LSMC monetization; opportunistic = templates + DSR-gated α.
7. **Liabilities.** Mode B, $D_y=d_yB_y$, opening-NAV basis; band priced; rule library for A6.
8. **Optimizer.** Phase I → restored 500-leaf H-LP (×5) → duals, π, λ → Lagrangian scoring → selection MILP → re-solve.
9. **Policy classes.** Cushion-monotone standing policy (v8 rules as controls); MPC; CMA-ES; agents propose via the PolicySpec DSL.
10. **Objective.** Tier 1A (T1–T9 + LM) / 1B floor / Tier 2 CRRA γ = 3 with L2 shortfall; T6 bands by model class; seats confined to Θ.
11. **Robustness.** Ensemble; KL/W∞ balls; k_MS and η\*; minimum-KL reverse stress; views on the same matrix.
12. **Experiment layer.** Hashed manifests; registries; accounting owned by the evaluator; DSR, PBO, α-investing.
13. **Agent roster.** 12 role types; typed tools; plain-Python meta-controller; gates G0–G9; family-B auditor.
14. **IC module.** Register → compiler → pack; computed shadow IC; blind pre-vote; self-tested client-side W1; append-only log with signposts.
15. **Package layout.** §8: contracts first; six streams; the room built on fixtures from week 1.
16. **Taxonomy.** Holding → group → strategy → sub-strategy; intra-ADIC netting at zero liquidity; DVA_g; decisions judged at total-portfolio level.
17. **Group actions.** §4.6: HF state machine; P2S via the overlay; SMA-only credit leverage; buyer-model co-investment bids; PE pacing corridor.
18. **Internal capital market.** Envelopes and decision prices from restored duals; smoothed published FTP; vintage locking; firewalled desks; dry powder as contingent budgets.
19. **Forecast credibility.** WIS registry; selection-weighted bias model; information value against the group's own class at n_eff ≥ 20; a contest route; pay decoupled from budget.
20. **Shadow IC.** 12 mandate seats with (q_k, θ_k); Red Team as objective DA. Agenda: total portfolio → group blocks by decision value → cross-group → ballot.
21. **Synthetic data.** SYN-ADIC-177 census v1.0; planted u/a/f/m biases; V1–V23; SBC; SYNTHETIC taint.
