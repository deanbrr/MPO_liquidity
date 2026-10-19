# C1: Portfolio mathematics (optimization core, scenario and robustness layer, objective design)

*ADIC Robust Target-Attainment TPA Lab. Cluster synthesis of streams 01 (multi-period optimization), 10 (scenarios and robustness) and 11 (objective design). As of 2026-10-18. Version 1.1.*

*Inputs read in full: the context file `inputs/00_CONTEXT_AND_PRIOR_WORK.md`, dossiers 01, 10 and 11, and their three verification logs.*

**Evidence tags**

| Tag | Meaning |
|---|---|
| **[S]** | Sourced; confirmed by the stream verifier. |
| **[C]** | Corrected by the verifier. Only the corrected value is used. |
| **[I]** | Inference or own computation. Illustrative, not ADIC data. |
| **[I-new]** | Computed for this synthesis (scripts in §13). |
| **[U]** | Unverifiable. Never load-bearing. |

ADIC figures are assumptions taken from the client brief.

---

## 1. Executive summary

1. **The streams agree on the solution's shape and disagree only on labels.** Streams 01 and 11 both use "L1/L2/L3", for different pieces. This document replaces both schemes with six deterministic components named by function:

   | Component | Role |
   |---|---|
   | **E** | Regime-switching scenario engine, anchored to CMAs. |
   | **P** | Policy simulator. It tunes and certifies the interpretable *standing policy*. |
   | **H** | Here-and-now decision program (HDP): a 12-quarter stochastic MILP. It prices asset-level SELL/HOLD/REFINANCE/LEVER actions and yields liquidity shadow prices. |
   | **V** | Terminal values: regression now, Markov SDDP later. |
   | **R** | Robustness layer. It reweights one scenario matrix. |
   | **F** | Safety filter. It projects any proposal onto the Tier-1 safe set. |

2. **Each constraint lives where it can be computed.**
   - Short-horizon liquidity is enforced in H and F.
   - Long-horizon floors and payout reliability live in the 40-quarter simulator. H carries them only as tuned surrogates.
   - Probabilities are verified out of sample, never optimized.

   This resolves verifier findings 01-R2, 01-R3 and 11-R8.

3. **Never maximize P(10%).**
   - Maximizing a hit probability replicates a digital option (Browne 1999 [S]).
   - In a toy DP it lifts P(target) from ≈34% to ≈68% by pinning leverage whenever the fund is behind. That buys a ≈4.6% chance of a >40% loss [I].
   - Stream 10's Tier-2 P(10%) objective is therefore overruled.

   Tier 2 instead maximizes CRRA utility (γ = 3) on real *distribution-inclusive* wealth, minus an L2 shortfall against 10% target wealth. Payouts are accumulated at 10%, so the shortfall equals the owner-IRR shortfall: $\mathrm{IRR}\ge10\%\iff\widetilde W_T\ge W_0\,1.1^T$. The term is affine per scenario, which fixes 11-R5.

4. **The v8 Tier-1 floor is infeasible when read as a probability on realised returns.**
   - It would need ≈15.8–17.9% expected return.
   - The stylised 60%-private book shows P(5y<7%) ≈ 31–55% across fee-consistent CMAs [C].

   It is replaced by Tier 1A (the survival set) plus Tier 1B (the robust floor). Tier 1B has two tests:
   - the mixture median of the 10-year return ≥ 7%;
   - worst-model CVaR10% ≥ 0%.

   The second test binds near 14.3% vol for an 8.5% book and ≈17.5% for a 10.5% book [C; I-new]. Fragility k\* and breakdown divergence η\* are reported alongside.

5. **Reliability defaults:**
   - P(red event within 5 years) ≤ 1% in every model, where a red event is a forced PE secondary sale or a payout below the minimum;
   - planned payout honoured with 97.5% reliability over 12 months;
   - survival of a 24-month named stress without PE secondaries;
   - IG + cash ≥ 8% of NAV;
   - 30-day margin coverage.

   Gates use each model's Clopper–Pearson upper bound at 50k paths. KL worst cases at η = 0.10 are not used, because they flip on a single path [C].

6. **Model uncertainty dwarfs Monte Carlo error** [C].
   - P(5y≥10%) ranges ≈27–51% across fee-consistent providers.
   - Mean returns disperse by ≈3–4pp.
   - The Monte Carlo standard error is ≈0.2pp.

   Every probability shown to the IC leads with its ensemble range.

7. **Shadow prices are the common currency.**
   - The corrected REFINANCE hurdle is ρ > s, not ρ > r^f + s [C].
   - SELL, LEVER and the tail hedge are priced at the same cash duals.
   - Discrete actions use forced-action re-solves.

8. **Drawdown and payout.**
   - The risk-constrained-Kelly real-drawdown constraint is infeasible across the 5–10% payout band [C]. Drawdown becomes an appetite metric set by the IC.
   - Under current CMAs, the payout that preserves real NAV in the median is ≈5–6%, not ≈6.8% [C].

9. **Leverage widens outcomes but barely moves the floor** [C]. With ACWI futures at 1.3×, P(5y≥10%) rises from 39.1% to 45.8%, while P(5y<7%) only moves from 40.4% to 39.0%. Default: ≤ 1.3× economic leverage.

10. **The private book is in a distribution drought.**
    - Distributions run at 12–15% of NAV, against 20–27% historically [S].
    - Normal-era calibrations (Luxenberg-type) overstate private cash by ≈2.7–3.5× [C].
    - Distribution intensities are therefore keyed to an exit-activity factor.

11. **Build plan.**
    - Phase 1 is pure Python: numpy/scipy, JAX or numba, cvxpy with Clarabel/HiGHS, and Pyomo with mpi-sppy.
    - Phase 2 adds SDDP.
    - Every engine exposes typed outputs and rubric checks to the agentic layer.

---

## 2. Verification corrections applied

All rows are applied throughout. No original claim is repeated uncorrected. None of the three logs refuted a claim.

| ID | Original claim | Correction applied | Design effect |
|---|---|---|---|
| 01-1 | REFINANCE wins if ρ > r^f + s | ρ is already net of r^f, so the test is **ρ > s**. The old hurdle was ≈389bp too high at SOFR 3.89%. Quarterly units throughout. | §5.9 |
| 01-2 | 5-year NPV floor C7 inside a 12-quarter tree | Cannot be computed scenario-wise; L2 cuts give expectations, not NAV distributions. | Floors move to P; H gets a tuned surrogate (D4, D5) |
| 01-3 | Scenario approach certifies L3 (≈1,000 / ≈60,000 scenarios) | Campi–Garatti needs a convex program with the constraint enforced on all samples, and a CMA-ES-tuned policy has neither. The exact bound would give 631 / 31,785 (ε 5%, β 1%). Certify the fixed policy out of sample instead: zero failures in ⌈ln(1/β)/ε⌉ fresh paths (93 at 5%/1%), or Clopper–Pearson. | D13, §5.7 |
| 01-4 | Luxenberg λ1 0.26, λ0 0.128, δ 0.33 "from 2021 buyout assumptions"; overstatement 2–2.5× | The intensities are from eFront buyout data; only the 15.8% return is BlackRock's 2021 CMA. The stated means do not reproduce the reported gains (α_K 2.491, α_I 3.685, α_D 1.804). The gains match eq. (8) means of E[λ1] ≈ 0.334, E[λ0] ≈ 0.167, E[δ] ≈ 0.402, E[R] ≈ 1.218. Since D = δRV, the like-for-like overstatement against Bain's 14% is **≈2.7–3.5×**, and drought δ ≈ **0.12–0.13**. State the quarterly conversion explicitly. | §5.10, §6, §7 |
| 01-5 | Constraint set C1–C8 | CVaR on a non-negative shortfall forces zero breach, so use signed margins. A hard C3 contradicts C8's 1% budget. Without relatively complete recourse, deep-stress leaves become infeasible. Fix: hard 30-day rows, probabilistic longer horizons, elastic slacks with lexicographic penalties. | §5.4 |
| 01-6 | Small Shapley–Folkman gap for price decomposition | The bound scales with the ≈8,100 coupling rows, so it is vacuous. Heuristic only; validate against the extensive form. | §5.6 |
| 01-7 | WS ≥ RP ≥ EEV as invariants | Holds for risk-neutral recourse only; EEV can be −∞ under CVaR rows. Compute on a risk-neutral penalized surrogate. Monotonicity applies to the optimized objective, within SAA tolerance. | §8 |
| 01-8 | Information-relaxation "optimality gap" | Restate as "gap vs the best policy under model m, risk-neutral surrogate". It says nothing about model risk. | §8 |
| 01-9 | Action modelling | REFINANCE proceeds were missing from the cash and NAV transitions. The opportunistic sleeve had no P&L mapping. LEVER semantics were ambiguous. | §5.3, §12 |
| 01-10, 01-11 | SELL value; cash equation | The fixed cost scales with μ0. The terminal multiplier is dimensionless. Facility interest accrues on the post-draw balance. One symbol per object. | §5.3, §5.9 |
| 01-12, 01-13 | L1 sizing; ADIC gap of USD 4–13bn | Sizing is unbenchmarked and ignores the model multiplier (≥3×). The gap omits new-commitment calls and depends on how unfunded is scaled: USD 7–16bn with ≈USD 50bn unfunded. Show it as a range. | §7, §8 |
| 01-14 | Floor "IRR ≥ 7%, rolling 5y, CVaR95" attributed to the deck | Inference, not deck content. The deck specified a worst-case 5-year return with ≤5% breach. | D5 |
| 01-15 | Literature | **Boyd 2017:** the <0.5 s / 80k-problem timings are projections; the measured run was 410 back-tests (≈0.5M problems) in ≈30 min on 32 cores. **Luxenberg:** over 20 periods, MPC *and* a simple heuristic are "extremely close" to the liquid ceiling. **Dulac-Arnold:** 8 of 9 challenges apply. **Powell's** "vast majority" is stated as belief. **Boyd 2014:** no guarantee. **Dowson:** end effects removed on one model only. **Dropped [U]:** "SDDP.jl 30% slower"; Towers Perrin "10–40 years". | Throughout |
| 10-1 | Book 6.2% / 8.0% / 11.4%; P(5y≥10%) 27–59%; KL 0.04–0.15; dispersion ≈5pp | BlackRock is gross of fees. JPM alternatives are net of fees; AQR's buyout figure is net of a 3.5% fee. Fee-consistent BlackRock: **9.2–10.2%**. Corrected: P(5y≥10%) **27–51%**; P(5y<7%) **31–55%**; KL vs JPM **0.02–0.06**; AQR–BlackRock **0.12–0.20**; detection error **25–38%**; dispersion **3–4pp**. Use unlevered DL (9.31%). | D11; η re-derived to 0.05 |
| 10-2 | KL-robust "≤1%" gates at η = 0.10 | Knife-edge. One failing path in 50k gives 1.73% (fail); zero failing paths always pass. The largest nominal p that keeps the 1% cap is 1.7×10⁻⁷ / 2.5×10⁻⁵ / 5.3×10⁻⁴ / 1.6×10⁻³ at η = 0.10 / 0.05 / 0.02 / 0.01. | D12 |
| 10-3 | W1 worst-case P(5y<7%) of 57.5 / 64.5 / 74.2%, read as an average shift | Indicators are not Lipschitz. A uniform shift gives ≈42.3 / 43.7 / 46.5%. Use W∞ for probabilities; W1 for mean and CVaR only. | §5.11 |
| 10-4, 10-5 | ENS gates; multiplier formula | Under uniform weights ENS/N = e^{−KL}, so the gates never fire; use Kish ESS and maximum weight. The ENS diagnostic is Meucci (2012), *Effective Number of Scenarios in Fully Flexible Probabilities*, which the stream used without citing it [corrected 2026-10-18]. The robust multiplier form is max_q E_q[ℓ] − θKL = θ ln E_p[e^{ℓ/θ}]. | §5.11 |
| 10-6 | Leverage by scaling the book | An overlay cannot earn PE premia. With ACWI futures, P(5y≥10%) / P(5y<7%) are 43.0% / 39.4% at 1.15× and 45.8% / 39.0% at 1.30×, against 39.1% / 40.4% unlevered. | D18 |
| 10-7, 10-8 | Return conventions; "Tier 1 infeasible" | Consistent lognormal for the stylised book: arithmetic 9.17%, vol 13.08%, geometric 8.39%; P(5y<7%) **40.4%**, P(5y≥10%) **39.1%**. Infeasibility holds only under reading (a), realised returns (centre 15.8–17.9%; 5-year σ ≈ 5.3%). Reading (b), a model-uncertainty test on expected return, is feasible. | D5, §7 |
| 10-9 | SDDP "one-to-one"; scenario sizes | Needs convexity and an observed Markov state, but the regime is latent and the actions are discrete. Exact Campi–Garatti minima at β = 10⁻³: 447 / 986 / 2,658 for d = 10 / 30 / 100, and 4,970 for d = 30 at ε = 1%. | D3, D13 |
| 10-10 | Smaller points | η = 0.10 was the author's choice. The Gaussian translation of η\* is tautological. A full covariance per regime has 840 parameters. The W1 greedy formula assumes equal weights. The prototype drew regimes i.i.d., so its robust numbers are illustrative. Use Meucci's *linear* blend. Classification is 62–82% correct at 20 years, so "undetectable for decades" overstates. Lange et al.: base models and orchestration act *jointly*. BlackRock vols are higher (buyout 26.06% vs 19.78%), so mean-only KL understates tail ambiguity. | §5.10–5.12 |
| 11-1, 11-2 | RCK real-drawdown constraint (λ = 8.4, G net of payout); "drawdown ≤ 30%" | Infeasible across 5–10%: it needs E ln G ≥ ≈5.1%/yr, while E ln G is −0.05 / −2.72 / −5.46%/yr at d = 5 / 7.5 / 10%. P(real NAV < 0.7 W0 within 10y) is 23.6% / 49.7% at d = 5 / 7.5%. It bounds falls below the starting value, not peak-to-trough (35.3% at d = 5%). | D8 |
| 11-3, 11-4 | "60/40 ≈ 8.5–9% arithmetic"; sustainable payout ≈6.8% | JPM figures are compound: ≈8.9% compound ≈ 10.5% arithmetic. 60% PE / 40% ACWI: vol ≈17.7%, median ≈9.1%, P(10y≥10%) ≈43%, P(5y<7%) ≈39.5%. Payout preserving real NAV: median ≈5–6%, mean ≈5.5–7.2%. | §7 |
| 11-5, 11-6 | Conic program; Euler contributions | The TWR shortfall is not conic, so use an affine gross-wealth proxy. The path-max deficit is not homogeneous: report marginal contributions and the liability block separately. | D6, §5.9 |
| 11-7, 11-8 | Yale rule; scenario table | Yale's formal rule: 80/20 with 5.25%, inflation-adjusted, collared at 4.0–6.5%. The table's N values assume β = 10⁻⁶; L2 would need 15,464–115,679 scenarios, so no certificate is claimed. | §7, D13 |
| 11-9 | C4 as a loose backstop | Binds at σ ≈ 14.3% for an 8.5% book and **≈17.5% for a 10.5% book** [I-new]. | D5 |
| 11-10 to 11-12 | Overclaims, toy details, citations | P(target) is the α = 0 boundary, not "the most risk-seeking criterion". The payout identity is deterministic. Rolling MPC alone does not stop leverage pinning under an indicator objective. The secondary-discount range in the no-sale stress is inert and is removed. The toy base (≈15.2% distributions) is optimistic, so use the drought variant. Closed-form 10y P(≥10%) at 1.0× is 28.5%. Add Föllmer & Leukert (2000); "Mohajerin Esfahani"; pages for R&U 2000 and Das et al. 2020. CPP 85/15, 55/45 and the triennial review are now confirmed. | §5.4, §7, §13 |

---

## 3. Decision register

| # | Question | Recommendation | Rationale |
|---|---|---|---|
| D1 | Architecture | E, P, H, V, R, F, run on a quarterly cycle (§4). | Streams 01 and 11 describe the same pieces under swapped labels; stream 10 supplies E and R. |
| D2 | Policy the IC adopts | The tuned interpretable policy from P is the standing policy (≈20 parameters, monotone in the cushion). H sets this quarter's asset actions and the prices. Any disagreement between the two is explained. Deep RL is used only as an R&D challenger, with its structure distilled into rules. | Powell's view [S, stated as belief]. A simple heuristic matches MPC over 20 periods [C]. 8 of 9 RL challenges apply [C]. |
| D3 | Strategic values | **Phase 1:** regression terminal values ω, ψ. **Phase 2:** Markov SDDP on ≤20 states and ≤8 Markov states, with the regime observed in the lookahead and no integers. | Verifier 10-R9; SDDP is optional in stream 11. |
| D4 | Tier-1 survival set | **Hard:** margin coverage, IG + cash, structural limits, 24-month named stress. **Per-model probabilistic:** red event ≤ 1% over 5 years; planned payout ≥ 97.5% over 12 months. **Elastic** penalties throughout. | Merges stream 01's C1–C8 (fixed), stream 10's T1-L (no longer knife-edge) and stream 11's C1/C2/C5. One red-event definition replaces two near-duplicates. |
| D5 | Robust floor | **Reading (b):** median of the 10-year TWR under the model mixture ≥ 7%, and worst-model CVaR10% ≥ 0% (potentially binding). P(5y<7%) and P(10y<7%) are reported as ranges, with k\* and η\*. Recovery mode if the floor fails. | The realised-return 5% reading is infeasible in all three streams. Combines stream 10's mixture-plus-fragility with stream 11's C4-plus-median. |
| D6 | Tier-2 objective | Maximize mixture E[U₃(real W̃)] − λ_T‖(1 − W̃/W̃\*)₊‖₂. No indicator terms; P(10%) is reported only. Log utility as a cross-check. | Stream 10's P(10%) objective is overruled by Browne and the DP evidence. Stream 01's risk-neutral NPV objective hugs boundaries. |
| D7 | Target metric | **Report:** 10-year rolling geometric TWR, nominal, gross of distributions; 5 years as secondary. **Optimize:** owner NPV / distribution-inclusive wealth. | Peer comparability; IRR⇔NPV linearity; 11-R5. |
| D8 | Drawdown | Not in Tier 1. Report investment drawdown and real NAV against a payout-implied glide path. The IC sets the appetite from the feasible (d, α, β) region. Provisional capacity: P(10y investment max DD > 40%) ≤ 10%. | 11-R1/R2. The CDaR95 ≤ 25% fallback is infeasible even for an i.i.d. book at 12% vol (≈34%) [I-new]. |
| D9 | Priorities | Lexicographic penalties for feasibility; ε-constraint sweeps for the price of safety; capacity / tolerance / appetite bands with hysteresis. | Stream 01 (Russell–Yasuda), stream 11, verifier 01-R6. |
| D10 | Scenario engine | Monthly regime factor model: K = 4 plus a persistent exit factor, t₅ innovations, ergodic CMA anchoring, 50k × 120 months per model. | Stream 10's primary engine. Stream 01's low-DPI state is represented through the exit factor. |
| D11 | Ambiguity set | Six fee- and leverage-consistent models with their own vols, plus one held-out generator. KL η = 0.05 for reporting. W∞ 0.5pp for probabilities; W1 0.5pp for Lipschitz metrics. | 10-1, 10-3, 10-10; η re-derived from the fee-consistent KL range of 0.02–0.06. |
| D12 | Rare-event gates | Per-model one-sided 95% Clopper–Pearson upper bound ≤ ε at 50k paths, with importance sampling below 0.5%, plus the named stress. KL at η_L = 0.01 is reported. An optional KL gate pairs η_L = 0.01 with a 2.5% cap (≈ nominal 0.88%). | 10-2 and [I-new]. |
| D13 | Certification | Out of sample on held-out seeds and a held-out generator; optimism gap; data-snooping log; Smith–Winkler shrinkage. Campi–Garatti only for convex sub-programs, with β stated. | 01-3, 10-9, 11-8. |
| D14 | Views and pooling | Entropy pooling with Meucci's linear blend; linear opinion pool, with the log pool as a sensitivity; Jensen–Shannon disagreement; decision-relevance test. LLMs draft constraint tables; humans supply the numbers. | Stream 10, corrected. The linear pool preserves event probabilities and gives no member a veto. |
| D15 | Fragility | KL fragility k\* (Aumann–Serrano) as the IC index. η\* translated into a detection-error probability. GKK and Pesenti for narratives. Wasserstein satisficing for per-asset radii. | Streams 10 and 11 reconciled; 10-10. |
| D16 | Action pricing | Cash duals → ρ; corrected SELL / REFINANCE / LEVER values; reduced cost r_j; forced-action re-solves. Approve only if r_j > 0 in every model and F passes. | Stream 01 §6.7 (corrected) is the cash-dual special case of stream 11 §6.6. |
| D17 | Time consistency | Re-solve quarterly; per-period constraints; the IC pre-commits parameters per annual cycle, with a deeper triennial review; recovery mode. | Shapiro (2009) [S]; CPP's triennial review [S]. |
| D18 | Leverage | Economic leverage through liquid assets and futures; debt tracked separately; ≤ 1.3× economic; debt ≤ 10% of NAV as a placeholder until stream 06 reports. | 10-6; stream 11 toy. |
| D19 | Stack | Python first. In-house entropy-pooling solver (fortitudo.tech is GPL-3.0). Commercial MILP/MISOCP in production. Julia only in Phase 2. | Implementation notes from all three streams. |
| D20 | Conventions | Tag returns arithmetic or geometric and gross or net of fees. Store rates annually and convert quarterly; intensities via 1 − (1 − x)^{1/4}. Scale by NAV. Hash every scenario set. | Four corrections were convention errors. |

---

## 4. Architecture of the portfolio-math core

```
 +------------------------ (E) Scenario engine, one run per model m in M -----------------------+
 | regimes + factors + CMA anchoring | private cash flows (04) | owner demand (03) | overlay (09) |
 | common random numbers | versioned scenario matrix + hash                                      |
 +-----------+-------------------------------+--------------------------------+-----------------+
             | 50k paths per model           | reduced tree                   | aggregated Markov
             v                               v (regime-stratified k-medoids)   v model (Phase 2)
 (P) Policy simulator and tuner      (H) Here-and-now program (HDP)     (V) Strategic values
 PFA/CFA via CMA-ES on CRN; Tier 1   12-quarter MILP, asset-level       Phase 1: regression omega,
 verified out of sample; long-       stage 1, LDR recourse, CVaR on     psi. Phase 2: SDDP cuts
 horizon floors; exact J             signed margins -> mu, rho, r_j     ("liquidity water values")
       | tuned CFA buffers ---------------->|<------------- terminal value --------------|
       |<---- distilled thresholds (rho-hat, SELL screen, reserve targets)
       v                                    v
 (R) Robustness: ensemble ranges, KL / W-inf / W1, k*, eta*, reverse stress, views, pools (O(N))
       v
 (F) Safety filter: projects every proposal onto the Tier-1 safe set and logs the change
       v
 IC portfolio-math pack -> approve / resize / defer -> override log -> outcome feedback
```

**Quarterly cycle.** A re-solve is also triggered when a state-engine light changes colour.
1. **E:** refresh the data and the regime posterior; regenerate paths; reduce them to the tree and check it for arbitrage.
2. **V:** refresh the terminal values.
3. **H:** solve across 10 SAA replications. Outputs: actions, duals, ε-sweeps, capability values, stability.
4. **P:** certify every Tier-1 probability. Compare these policies:
   - the tuned policy;
   - the HDP-in-the-loop policy;
   - certainty-equivalent MPC (H = 8);
   - the v8 comparators;
   - ablations (no overlay, no facility, no secondaries).
5. **R:** produce ensemble ranges, worst cases, k\*, η\*, reverse-stress worlds and view posteriors.
6. **Rubrics** (§8): any failure blocks the pack.
7. **F, then the IC pack.** Live what-ifs run as warm-started H re-solves.

**What lives where**

| Object | Enforced or estimated | Verified | Reported as |
|---|---|---|---|
| Margin coverage, IG + cash, structural limits | H (elastic hard rows); F | P (frequency) | status, slack |
| 24-month named stress | H (linear robust counterpart); F | deterministic | survival horizon |
| Red event ≤ 1% over 5y | H: 12-quarter CVaR on a signed margin (ε′ 0.60%) plus a severity budget | P: per-model Clopper–Pearson | range, upper bound, KL(0.01) |
| Planned payout 97.5% over 12m | H: penalty tier | P | range |
| Robust floor (10y) | P (constraint on θ); H: tuned surrogate | P + held-out generator | median range, CVaR10, k\*, η\* |
| Objective J | P exactly; H as a PWL surrogate + terminal value | agreement rubric | CE return, frontiers |
| Action values | H duals + forced re-solves | P (A/B on common paths) | decision cards |

---

## 5. Model formulations

### 5.1 Conventions and notation

**Time and scaling**
- Decisions are quarterly, t = 0, …, T. The scenario engine is monthly, and margin uses monthly sub-steps.
- Solver money is in units of W₀ = 1. Reports use USD bn.

**Rates and returns**
- Compounding rates: $r_q=(1+r_a)^{1/4}-1$.
- Loan spreads: $s_q=s_a/4$.
- Proportional intensities: $x_q=1-(1-x_a)^{1/4}$. For example, 0.14 → 0.0370, 0.26 → 0.0725 and 0.334 → 0.0966 [I-new].
- Luxenberg's λ0 does not convert this way. Model new commitments as new positions on the age-dependent call curve instead.
- Returns are gross factors R = 1 + r, each tagged arithmetic or geometric, with its fee basis and leverage basis.

| Symbol | Meaning |
|---|---|
| $W_t,\ C_t,\ h_{k,t}$ | NAV net of all debt; cash and cash-like HQLA; liquid sleeve k |
| $V_{i,t},\ U_{i,t},\ a_{i,t}$ | private position i (group g): NAV, unfunded, age |
| $N_{i,t},\ B_t,\ Q_t$ | ADIC-level NAV loan on i; fund facility; term debt |
| $H_{b,t},\ X_t,\ e_t,\ \mathrm{IM}_t$ | hedge notional in bucket b; signed futures notional; opportunistic budget; initial margin |
| $d_t,\ d^{\min}_t,\ d^{\text{plan}}_t$ | payout to owner; minimum; planned |
| $\mathrm{Cal},\ \mathrm{Dis},\ \lambda^{\text{call}}_g,\ \lambda^{\text{dis}}_g$ | calls; GP distributions; quarterly intensities |
| $\delta^{\text{sec}},\ s^B,\ s^Q,\ s^N,\ \eta_{k,j}$ | secondary discount; spreads over SOFR; liquidity haircuts |
| $S_t,\ x^{\text{exit}}_t,\ \boldsymbol\pi_t,\ \iota_t$ | regime; exit factor; regime posterior; CPI index |
| $\mu_n,\ \rho_n$ | probability-normalized cash dual; implied liquidity premium |
| $m\in\mathcal M,\ w_m,\ p_s,\ q_s$ | models and weights; nominal and tilted scenario weights |

### 5.2 State, decisions, exogenous information

The state follows Powell's split, $\mathcal S_t=(R_t,I_t,B_t)$.

**Physical, $R_t$**
- $C_t$ and $h_t$;
- per private position: $V_{i,t}$, $U_{i,t}$, $N_{i,t}$, $a_{i,t}$ and a pledged flag;
- $B_t$ and $Q_t$, with maturities;
- the hedge book, $X_t$, $e_t$ and $\mathrm{IM}_t$;
- year-to-date and last payout;
- the peak of the TWR index.

**Information, $I_t$:** prices, curves and vol surfaces; spreads; secondary discounts; NAV-loan terms; SOFR; oil.

**Beliefs, $B_t$:** $\boldsymbol\pi_t$; fused return beliefs $(\mu_{i,t},\sigma_{i,t})$ from the underwritten, actual and forecast marks (stream 07); model weights; ambiguity radii.

**Decisions, $a_t$**
- trades $z^{\pm}$;
- commitments $k_{g,t}$;
- per asset: SELL fraction $\phi_{i,t}$, REFINANCE draw $n_{i,t}$ and LEVER add-on $\ell_{i,t}$, with binaries $y^a_i$ and $\sum_ay^a_i\le1$ in stage 1;
- facility and debt moves $\Delta B^{\pm}$, $\Delta Q$;
- overlay: $H_{b,t}$, $X_t$, $e_t$;
- $d_t$, but only if the payout rule leaves discretion.

**Exogenous, $W_{t+1}$:** returns; intensities; discounts; spreads and LTV caps; overlay cash flows per unit; opportunistic return; owner demand; regime transition.

### 5.3 Transition model (shared by P and H)

Actions happen at the beginning of the quarter; flows realise during it.

**Private positions**

$$V^+_{i,t}=(1-\phi_{i,t})V_{i,t}+\ell_{i,t},\qquad U^+_{i,t}=(1-\phi_{i,t})U_{i,t},\qquad N^+_{i,t}=(1-\phi_{i,t})N_{i,t}+n_{i,t}$$

$$\mathrm{Cal}_{i,t+1}=\lambda^{\text{call}}_g(S_t,a_{i,t})\,U^+_{i,t},\qquad \mathrm{Dis}_{i,t+1}=\lambda^{\text{dis}}_g(S_{t+1},x^{\text{exit}}_{t+1},a_{i,t})\,R_{i,t+1}V^+_{i,t}$$

$$V_{i,t+1}=R_{i,t+1}V^+_{i,t}+\mathrm{Cal}_{i,t+1}-\mathrm{Dis}_{i,t+1},\qquad U_{i,t+1}=U^+_{i,t}-\mathrm{Cal}_{i,t+1},\qquad N_{i,t+1}=N^+_{i,t}$$

- A sale repays the attached loan pro rata, and the buyer assumes the unfunded commitment.
- A new commitment opens a position with V = 0 and U = $k_{g,t}$.

**Liquid sleeves and debt:** $h_{k,t+1}=R^L_{k,t+1}(h_{k,t}+z^+_{k,t}-z^-_{k,t})$; $B^+_t=B_t+\Delta B^+_t-\Delta B^-_t$; $Q^+_t=Q_t+\Delta Q_t$.

**Cash** (quarterly rates)

$$\begin{aligned}C^+_t={}&C_t-\textstyle\sum_k[(1+\tau^+_k)z^+_{k,t}-(1-\tau^-_k)z^-_{k,t}]-\sum_i\ell_{i,t}+\sum_i[(1-\delta^{\text{sec}}_{i,t})\phi_{i,t}V_{i,t}-\phi_{i,t}N_{i,t}]\\&+\textstyle\sum_in_{i,t}+\Delta B^+_t-\Delta B^-_t+\Delta Q_t-d_t-\sum_b\varpi_{b,t}H_{b,t}-\sum_{i,a}\Phi^a_iy^a_i\end{aligned}$$

$$\begin{aligned}C_{t+1}={}&(1+r^f_t)C^+_t+\textstyle\sum_i(\mathrm{Dis}_{i,t+1}-\mathrm{Cal}_{i,t+1})-(r^f_t+s^B)B^+_t-(r^f_t+s^Q)Q^+_t-\sum_i(r^f_t+s^N_t)N^+_{i,t}\\&+\textstyle\sum_bH_{b,t}\kappa_{b,t+1}+X_t(R^{\text{fut}}_{t+1}-1-r^f_t)+e_t\,r^{\text{opp}}_{t+1}\end{aligned}$$

- $\varpi_b$ is the premium per unit of notional.
- $\kappa_b$ is the hedge cash flow per unit of notional (payoff or collateralised MTM change), supplied by stream 09.
- $r^{\text{opp}}$ is the opportunistic P&L per unit of budget, settled through variation margin.

This fixes 01-R10 and 01-R12.

**NAV, HQLA and margin**

$$W_t=C_t+\textstyle\sum_kh_{k,t}+\sum_iV_{i,t}+\mathrm{MTM}^{\text{ovl}}_t-B_t-Q_t-\sum_iN_{i,t},\qquad \mathrm{HQLA}_t=C_t+\sum_k(1-\eta_{k,S_t})h_{k,t}-\mathrm{IM}_t$$

$\mathrm{IM}_t=\sum_bm_bH_{b,t}+m_X(X^+_t+X^-_t)+m_ee_t$. The TWR index is $\Pi_{t+1}=\Pi_t(W_{t+1}+d_t)/W_t$.

**Keeping H linear.** Every term is linear per scenario except $\phi V$ when V is a variable.
- Asset-level fractions act only at the root, where $V_{i,0}$ is data.
- Recourse nodes sell dollars by group, $s_{g,t}$, and transfer $\bar u_{g,t}s_{g,t}$ of unfunded, using a projected ratio $\bar u$.
- Price impact is convex piecewise-linear: $\sum_\ell(1-\delta^{\text{sec}}_{g,\ell})s^\ell_{g,t}$ with $s^\ell\le\text{cap}_\ell$.

### 5.4 Tier-1 safe set

**Hard at every decision date.** Each constraint has an elastic slack $u\ge0$, penalized in every optimization.

- **T1.1 Payout.**
  - Floor: $d_t\ge d^{\min}_t-u^{\text{crit}}_t$, where $d^{\min}_t$ is the quarterly instalment of $\max(5\%\bar W_y,d^{\text{own}}_t)$.
  - Band: $\sum_{t\in y}d_t\le10\%\bar W_y$.
- **T1.2 IG + cash.** $C_t+h^{\text{IG}}_t\ge0.08W_t-u^{\text{IG}}_t$.
- **T1.3 Margin coverage.** $\mathrm{HQLA}_t\ge\sum_bv_{b,S}H_{b,t}+v_{X,S}(X^+_t+X^-_t)+v_{e,S}e_t+O^{30d}_t-u^M_t$. The v terms are per-unit P99 30-day variation-margin rates (stream 09); $O^{30d}$ are scheduled outflows.
- **T1.4 24-month named stress.** A linear robust counterpart whose worst case is at a vertex of the stress set:

  $$\mathrm{HQLA}^{\text{str}}_t+0.5\bar B_t-B_t\ge\textstyle\sum_{\tau=1}^{8}[d^{\min}_{t+\tau}+1.5\overline{\mathrm{Cal}}_{t+\tau}+\mathrm{DS}_{t+\tau}]+\mathrm{VM}^{24m}_{99.5}-u^S_t$$

  The stress applies a −40% equity shock, 0% PE distributions, 50% facility availability and no PE secondary sales. The inert secondary-discount parameter is removed.
- **T1.5 Structural limits.**
  - Economic leverage: $(\sum_kh_k+\sum_iV_i+X^+)/W\le1.3$.
  - Debt: $(B+Q+\sum N)/W\le10\%$ (placeholder).
  - Facility LTV: $B\le\mathrm{LTV}^B_S\sum_{\text{pledged}}V_i$.
  - NAV-loan LTV: $N_i\le\mathrm{LTV}^N_SV_i$, with ≤15% per fund and $\sum N\le5\%W$.
  - Overcommitment: $\sum(V+U)\le0.80W$.
  - Overlay: $X^++X^-\le0.30W$; a premium budget; $\mathrm{ES}_{97.5}(e\,r^{\text{opp}})\le B^{\text{opp}}W$.

  Because LTV caps depend on the regime, stress forces repayment exactly when cash is dearest. That is REFINANCE's wrong-way cost.

**Probabilistic, per model.** Verified in P.
- **T1.6 Red event.** $P_m(\exists t\le20:\text{forced PE secondary or }u^{\text{crit}}_t>0)\le\varepsilon_R=1\%$.
- **T1.7 Planned payout.** $P_m(\exists t\le4:d_t<d^{\text{plan}}_t)\le2.5\%$.
- **T1.8 Robust floor.** With $\bar R_{10}=(\Pi_{40}/\Pi_0)^{1/10}-1$ and the mixture $\bar P=\sum_mw_mP_m$:

  $$\mathrm{Med}_{\bar P}(\bar R_{10})\ge7\%\quad\text{and}\quad\min_m\mathrm{CVaR}^{P_m}_{10\%}(\bar R_{10})\ge0\%$$

**H surrogates on the 12-quarter horizon**
- **Signed red margin.** $g^{\text{red}}_c=C^{\text{floor}}_c-[\mathrm{HQLA}_c+(\bar B_{S_c}-B_c)-\mathrm{Proc}^{\text{sec}}_{a(c)}]$. It measures need *before* red recourse. The constraint is $\mathrm{CVaR}^{(m)}_{1-\varepsilon'_R}(\max_{t\le12}g^{\text{red}})\le0$, with $\varepsilon'_R=1-(1-\varepsilon_R)^{12/20}=0.60\%$ [I-new]. It is built from Rockafellar–Uryasev rows plus one max variable per scenario.
- **Severity budget.** $\mathrm{CVaR}^{(m)}_{1-\varepsilon'_R}(\sum_t\mathrm{Proc}^{\text{sec}}_t+u^{\text{crit}}_t)\le b^{\text{red}}$, a Gerber–Shiu-style dollar budget.
- **Floor surrogate.** $\mathrm{CVaR}^{(m)}_{10\%}(-\mathrm{NPV}_{0\%,12q})\le b^{\text{floor}}$, where $\mathrm{NPV}_{0\%,12q}=-W_0+\sum_{t\le12}d_t+W^{\text{term}}_{12}$.
- Both $b^{\text{red}}$ and $b^{\text{floor}}$ are CFA buffers, tuned in P until the decisions H implements satisfy T1.6 and T1.8 in simulation.

**Penalty tiers.** Normalized defaults are $M^M=10^4>M^{\text{crit}}=10^3>M^S=10^2>M^{\text{red}}=50>M^{\text{IG}}=10$, all far above the marginal utility of wealth (≈1).
- The red tier charges secondary proceeds on top of their economic discount.
- Penalty usage is reported as breach evidence.
- Duals are reported only for rows with zero slack.

**Governance bands** (stream 11). Each metric gets three levels, with hysteresis between them. For ε_R:
- capacity (hard): 2%;
- tolerance (amber): 1%;
- appetite (target): 0.5%.

**Recovery mode.** If T1.6 or T1.8 is already infeasible at t = 0, first minimize the violated metric, then maximize J without worsening it. The IC is told.

### 5.5 Tier-2 objective

**Distribution-inclusive wealth**

$$\widetilde W_T=W^{\text{term}}_T+\textstyle\sum_{t\le T}d_t(1.10)^{(T-t)/4},\qquad\mathrm{IRR}\ge10\%\iff\mathrm{NPV}_{10\%}\ge0\iff\widetilde W_T\ge W_0(1.10)^{T/4}$$

The equivalence holds because the owner's flows are one outflow followed by non-negative inflows [I, stream 01].

**Simulator objective** (exact, 40 quarters)

$$J(\theta)=\sum_mw_m\Big\{\mathbb E_{P_m}[U_\gamma(\widetilde W^{\text{real}}_{40}/W_0)]-\lambda_T\big(\mathbb E_{P_m}[(1-\widetilde W_{40}/\widetilde W^\star_{40})_+^2]\big)^{1/2}\Big\}$$

- $U_\gamma(w)=(w^{1-\gamma}-1)/(1-\gamma)$ with γ = 3.
- $\widetilde W^{\text{real}}=\widetilde W/\iota$ and $\widetilde W^\star_{40}=W_0\,1.10^{10}$.
- λ_T = 1, swept over 0–2 [I-new]. Since U₃′(1) = 1, λ_T = 1 roughly doubles the felt cost of a shortfall.

**H objective** (LP/MILP surrogate)

$$\max\sum_mw_m\sum_{s}p_s\big[\hat U(\widetilde W^{\text{real}}_s/W_0)-\lambda^H_T\hat\psi(1-\widetilde W_s/\widetilde W^\star_{12})\big]-\sum_np_n\big[\mathrm{TC}_n+\textstyle\sum M^{\text{tier}}u^{\text{tier}}_n\big]-\kappa^u\sum_i\sigma_i\ell_{i,0}$$

- $\hat U$: 12 tangents of U₃ on [0.3, 3].
- $\hat\psi$: 6 PWL segments of $x_+^2$ on [0, 0.6], or the exact second-order cone with an MISOCP solver.
- $\lambda^H_T$ is tuned until H and P rank actions the same way.
- $\kappa^u\sigma_i\ell_i$ is the LEVER uncertainty haircut, with κ^u ≈ 0.5–1 and σ_i from stream 07.

**Terminal value** (Phase 1)

$$W^{\text{term}}=C+\textstyle\sum_kh_k+\sum_g\omega_{g,j}V_g-\sum_g\psi_{g,j}U_g+\mathrm{MTM}^{\text{ovl}}-B-Q-\sum N$$

- ω (value per USD of group NAV, floored at $1-\delta^{\text{sec}}$) and ψ (burden per USD of unfunded) come from regressing P's discounted continuation values on the aggregated state (Brandt et al. [S]).
- Phase 2 replaces them with SDDP cuts.

**Rules against target-chasing** (stream 11)
- No indicator terms.
- Shortfall exponent α ≥ 1 (default 2).
- Leverage, risk budget and pacing monotone in the cushion.
- Rolling horizon with a terminal value.
- Constraints hold in every model.
- A gambling detector (§5.7).

### 5.6 HDP specifics

**Tree, per model**
- Root at t = 0.
- 40 regime-stratified branches over Q1, sampled from $\boldsymbol\pi_0$.
- 25 branches per node at t = 4.
- A fan to t = 12.
- 1,000 leaves per model. Three models sit in the tree: base, worst-liquidity, worst-return. All six run decomposed overnight.

**Decision levels**
- Stage 1 is at asset level: ≈300 positions, ≈1,500 continuous variables and ≈900 binaries [I].
- Recourse is at group level.
- Sizes are semi-continuous with NAV-tight bounds. Without GP consent, $y^a_i=0$.

**Within fans**, recourse follows linear decision rules $y_t=y^0_t+Y_t\xi_{[t]}$, with coefficients shared across each stage-2 node. This removes clairvoyance.

**Solution ladder:** extensive-form MILP → Benders with an integer master → relax-and-fix → price decomposition (heuristic, validated).

**Scenario reduction:** regime-stratified k-medoids plus Høyland–Wallace moment matching, a no-arbitrage check (Klaassen 2002 [S]), and a stability test (solve on tree A, evaluate on paths B).

**Outputs:**
- actions;
- a regime playbook;
- duals;
- ε-sweeps;
- capability values (re-solves without the facility, the overlay, secondaries or the opportunistic sleeve);
- stability across replications;
- VSS and EVPI on the risk-neutral penalized surrogate.

### 5.7 Policy family, tuning and certification

**Policy rules** (≈20 parameters)

| Rule | Form | Constraint on θ |
|---|---|---|
| Reserve | $\mathrm{HQLA}^\star_t/W_t=\theta_1+\theta_2\mathbb 1\{\text{drought}\}+\theta_3F_t$ | θ₁…₃ ≥ 0 |
| Pacing | $k_{g,t}=[\theta_{4,g}+\theta_5c_t-\theta_6\mathbb 1\{\text{drought}\}-\theta_7(\text{overcommit}_t-\theta_8)^+]^+W_t$, closing 0.25–0.5 of the gap per quarter | θ₅ ≥ 0 |
| Economic leverage | $L_t=\mathrm{clip}(\theta_9+\theta_{10}c_t-\theta_{11}F_t,1,1.3)$ | θ₁₀ ≥ 0 |
| Tail hedge | $H_t/W_t=\mathrm{clip}(\theta_{12}+\theta_{13}F_t-\theta_{14}c_t,0,H^{\max})$ | θ₁₄ ≥ 0 |
| Opportunistic | $e_t/W_t=\mathrm{clip}(\theta_{15}-\theta_{16}\,\text{margin use}_t,0,e^{\max})$ | — |
| Waterfall | reserve → liquid sales → facility (if gap > θ₁₇) → PE secondary only if gap > θ₁₈ and $\delta^{\text{sec}}<\delta^{\max}$ → payout to minimum | fixed order |
| SELL screen | sell if $\hat\rho_t-\text{hold premium}_i>\theta_{19}$, where $\hat\rho_t$ is fitted to H's duals | — |
| Payout top-up | pay above the minimum only if $c_t\ge\theta_{20}$ (a de Finetti-style barrier on the top-up only; the classic barrier strategy has no minimum payout, so the always-paid minimum is ADIC's adaptation [I]) | — |

- $F_t$ is the state-engine fragility index.
- $c_t$ is the liquidity cushion: the T1.4 slack divided by NAV.

**Tuning**
- Maximize $\hat J(\theta)$ on 10k paths per model with common random numbers.
- Handle T1.6–T1.8 with augmented-Lagrangian penalties.
- Optimize with CMA-ES, or Bayesian optimization for ≤20 dimensions (Frazier [S]).
- Benchmark against HDP-in-the-loop (500–2,000 paths) and certainty-equivalent MPC (H = 8).

**Certification**
1. Freeze θ.
2. Run fresh 50k paths per model plus a held-out bootstrap/FHS generator.
3. Report $\hat p_m$ and its one-sided 95% Clopper–Pearson upper bound. Pass if the bound is ≤ ε.

At 50k paths [I-new]:
- $\hat p$ = 0.90% gives a bound of 0.97% (pass for ε = 1%).
- $\hat p$ = 1.00% gives 1.08% (fail).
- The relative standard error is 4.5% at p = 1% and 10% at p = 0.2%.
- Zero-failure shortcut: N = ⌈ln(1/β)/ε⌉, i.e. 93 at (5%, 1%) and 461 at (1%, 1%).
- Use importance sampling on the regime chain whenever $\hat p$ < 0.5%.

Also report the optimism gap and the number of policies tried, and shrink the selected advantage (Smith–Winkler [S]).

**Gambling detector**
- **G1:** risk rises after losses.
- **G2:** bimodal terminal distribution.
- **G3:** P(10%) rises while the median is flat and CVaR worsens. In the toy, policy C vs B gives +3.5pp of P(10%) for +10.7pp of hard-breach probability at an equal median [I; toy not re-run; optimistic base].
- **G4:** leverage at its cap whenever the fund is behind the target path, the signature of a P-max policy.

### 5.8 Strategic value layer (Phase 2)

| Element | Specification |
|---|---|
| Method | Markov SDDP |
| State | ≈20 aggregated variables (liquid, cash, debt, NAV and unfunded for ≈6 groups, hedge) |
| Markov states | 4 regimes × 2 exit buckets |
| Stages | 40 quarterly stages plus a cyclic node (Dowson's policy graph) |
| Regime | Observed in the lookahead |
| Integers | None |
| Risk measure | Expectation; EAVaR sparingly |

**Caveats**
- The SDDP.jl lower bound is invalid under non-expectation risk measures [S].
- Risk-averse upper bounds need Kozmík–Morton estimators [S].
- Belief-state SDDP and SDDiP are research options [U].

The cut slopes per Markov state are the "liquidity water values" that feed H.

### 5.9 Action pricing: SELL / HOLD / REFINANCE / LEVER

$\mu_n$ is the cash dual divided by the node probability; dividing by $\mu_0$ gives root dollars.

**Implied quarterly liquidity premium.** $\rho_n=\mu_n/\mathbb E[\mu_c\mid n]-(1+r^f_n)$. It is ≈0 when cash is slack and spikes in stress.

**Continuation value of position i** (root USD)

$$\mathrm{CV}_i=\tfrac1{\mu_0}\mathbb E\Big[\textstyle\sum_{t=1}^{T_1}\mu_t\big(\mathrm{Dis}_{i,t}-\mathrm{Cal}_{i,t}-(r^f_{t-1}+s^N)N_{i,t}\big)+\mu_{T_1}\omega_{g,S_{T_1}}(V_{i,T_1}-N_{i,T_1})\Big]$$

**Action values** (root USD)
- **SELL:** $v^S_i=(1-\delta^{\text{sec}}_i)V_i-N_i-\Phi^S_i-\mathrm{CV}_i$. Relief from future calls is inside CV.
- **REFINANCE** (USD 1 repaid at τ): $v^R=1-\tfrac1{\mu_0}\mathbb E[\sum_{t\le\tau}\mu_t(r^f_{t-1}+s^N)+\mu_\tau]$.
  - For τ = 1 this is $v^R=\tfrac{\mathbb E[\mu_1]}{\mu_0}(\rho_0-s^N)$, so it pays **iff ρ > s^N** [C].
  - Covenant-forced repayment in stress is captured only by forced-action re-solves.
- **LEVER:** $v^L_i=\Delta[-1+\mathrm{cv}_i-\kappa^u\sigma_i]-\Phi^L_i$, where cv_i is the per-dollar continuation value under fused, shrunk beliefs, including any new unfunded.
- **HOLD:** zero.

**General reduced cost** (stream 11): $r_j=\Delta J_j-\sum_k\lambda_k\Delta g_{k,j}-c_j$.
- Approve only if $r_j>0$ in every model and F passes.
- Rank by $r_j$ per unit of irreversibility (SELL > REFINANCE > LEVER > HOLD).
- Discrete actions use warm-started forced-action re-solves, reported as ranges over replications × models.
- Tail-constraint contributions are reported as marginal contributions plus the liability block. There is no Euler split [C].

**Liquidity merit order:** buffer → liquid rebalancing → overlay de-risking (releases collateral) → NAV facility → LP secondary → GP-led solution. The marginal source sets ρ.

**Overlay at shadow prices**
- **Tail hedge:** $v^H=\mathbb E[\mu P^H]/\mu_0-\text{premium}$. It exceeds the discounted expected payoff because the hedge pays when μ spikes.
- Its value appears in the duals of T1.3 and T1.6, not in expected return. In the toy it cut red-breach probability from 10.7% to 4.1% [I].
- **Opportunistic sleeve:** charged when its losses cluster in high-μ states.

### 5.10 Scenario engine (E)

**Regimes**
- Hidden semi-Markov $S_t\in\{$expansion, inflationary late-cycle, crisis, recovery$\}$, following Guidolin–Timmermann [S].
- Negative-binomial dwell, or jump-penalized estimation. Jump models were more persistent out of sample in Shu, Yu & Mulvey (2024), *J. Asset Management* 25(5):493–507, DOI 10.1057/s41260-024-00376-x, the published version of the arXiv:2402.05272 preprint the stream cited [S].
- K ∈ {3, 4, 5} chosen by out-of-sample log score.
- Regimes are anchored by crisis vol to prevent label switching.

**Exit factor:** $x^{\text{exit}}_{t+1}=\mu_x(S_t)+\phi_x(x^{\text{exit}}_t-\mu_x(S_t))+\sigma_x\varepsilon^x$, highly persistent and bucketed into drought and normal for H and V. It starts in drought. MSCI reports series-high exit multiples alongside 12% distribution rates, and expects the drought not to end merely because exit conditions improve [S].

**Factors.** About 20 monthly series: growth, CPI, policy rate, 10y, 2s10s, Brent, USD, IG/HY OAS, private-credit losses, ACWI/EM excess returns, log VIX, skew, term slope, exit activity, secondary discount, NAV-loan spread.

$$f_t=c_{S_t}+Af_{t-1}+D_{S_t}L_{S_t}\varepsilon_t,\quad\varepsilon_t\sim t_5,\quad R_s=(1-\omega_s)R_0+\omega_sR_{\text{crisis}}$$

Regimes move intercepts, block vol multipliers and the blend weight. A full covariance per regime would be 840 parameters [C].

**Assets:** $r_{a,t}=a_{a,S_t}+b_a^\top f_t+\sigma_{a,S_t}u_{a,t}$. The stock–bond correlation is regime-dependent; JPM 2026 has ACWI–Agg at +0.33 [S].

**Private assets**
- True return: $r^*_{g,t}=\alpha_g+\beta_g^\top f_t+e_{g,t}$.
- Reported return: $r^{\text{rep}}_{g,t}=\sum_k\vartheta_{gk}r^*_{g,t-k}$ with $\sum\vartheta=1$ (GLM [S]).
- Idiosyncratic spread is calibrated to the ≈1,960bp manager dispersion [S].
- Risk uses de-smoothed returns; covenants use reported NAV.

**Cash flows** (stream 04): $\lambda^{\text{call}}_g(S,\text{age})$ and $\lambda^{\text{dis}}_g(S,x^{\text{exit}},\text{age})$.

**Liquidity drivers** (stream 05 calibrates; no defaults asserted here):
- $\delta^{\text{sec}}=\delta_0+\delta_1\mathbb 1\{\text{crisis}\}+\delta_2(-r^{\text{eq}}_{t-3:t})^++\text{quality/age}+\text{size impact}$.
- NAV-loan rate = SOFR + $s_0$ + $s_1$·HY OAS, with LTV(S).

**Owner demand** (stream 03 hypothesis): $d^{\text{own}}_t=\mathrm{clip}(\bar d+\kappa_{\text{oil}}(\ln\bar O-\ln O_t)+\kappa_f\xi_t,5\%,10\%)\bar W_t$. This is wrong-way risk.

**Overlay drivers** (stream 09): an AR(1) for ATM vol with a negative equity link and jumps; SVI surface slices; Q-valuation on P-paths; a variance risk premium; VM = −ΔMTM.

**Calibration**
1. Fit on monthly data from 1990 to 2026 (1970s for inflation).
2. Ergodic matching: $c_s\leftarrow c_s+(I-A)(m^{\text{CMA}}-\bar m)$ with $\bar m=(I-A)^{-1}\sum_s\bar\pi_sc_s$. This is exact [verifier-checked].
3. 1-D intercept roots so each 10-year *compound* return equals its CMA.
4. Vol scaling plus a Higham repair. The JPM 2026 matrix has minimum eigenvalue −0.0161, and the repair changes no entry by more than 0.0066 [S].
5. Fit desmoothing and cash flows on ADIC data.
6. Run every model with common random numbers.

**Ensemble.** Providers are normalized to net-of-fee before mixing. BlackRock haircuts:

| Asset | Haircut |
|---|---|
| PE | 2.5–4.5pp (centre 3.5pp, equal to AQR's fee) |
| Direct lending | 1.5–2.5pp (use the unlevered figure) |
| Infrastructure | 1.5–2.5pp |
| Hedge funds | 2–3pp |
| Core real estate | 0.75–1.25pp |

Each provider keeps its own vols.

| Model | CMA anchor | Structure |
|---|---|---|
| M1 | JPM 2027 (2026 values where silent) | base |
| M2 | BlackRock, fee-adjusted | base |
| M3 | AQR, nominal (real + 2.4%) | base |
| M4 | JPM | persistent drought |
| M5 | JPM | stagflation-heavy |
| M6 | BlackRock "risk premia rise", fee-adjusted | drought + overlay stress |

A held-out bootstrap generator is used only for validation. GMO and Research Affiliates are to be added once verified [U].

**Paths**
- 50k × 120 months per model; store features in float32 (≈0.6 GB per 50k × 120 × 25 block).
- Common random numbers across policies and models.
- 250k paths or importance sampling for tail sign-off.
- 2–10k reduced scenarios for H.
- An independent 50k test set.
- Regression-based nested simulation for future-node risk, with few inner draws per outer scenario (Broadie, Du & Moallemi 2015, *OR* 63(5):1077–1097, DOI 10.1287/opre.2015.1419 [S]). [corrected 2026-10-18: the paper presents "a regression-based nested Monte Carlo simulation method", so the earlier "not nested simulation" misstated it.]

### 5.11 Robustness layer (R)

Notation: y outcome, ℓ loss, A failure event, p nominal weights. Metrics are computed per policy and per model.

| ID | Metric | Formula and notes |
|---|---|---|
| R1 | KL worst-case probability | $\max\{q\ge p_A:\mathrm{kl}(q\,\Vert\,p_A)\le\eta\}$. Exact; bisection. |
| R2 | KL worst-case expectation | $\inf_{\vartheta>0}\vartheta\eta+\vartheta\ln\sum_ip_ie^{\ell_i/\vartheta}$ |
| R3 | KL worst-case CVaR (tail α) | $\min_t\{t+\alpha^{-1}\mathrm{R2}[(\ell-t)^+]\}$ |
| R4 | **W∞** threshold probability | $P(y<\tau+\varepsilon_W)$: the uniform-shift reading of fee, smoothing and measurement bias [C] |
| R5 | W1, Lipschitz metrics only | worst mean = E[y] − ε; worst CVaR_α = CVaR_α + ε/α. Any W1 threshold probability is labelled "concentrated transport" and uses the weights q. |
| R6 | Breakdown divergence | $\eta^\star=\min\mathrm{KL}(q\,\Vert\,p)$ s.t. $\mathbb E_q[y]\le\tau$, with $q^\star\propto pe^{-\vartheta y}$. Report tilted factor means, regime occupancy and detection error [C]. |
| R7 | Fragility | $k^\star=\inf\{k>0:\sum_ip_ie^{(f_i-\tau)/k}\le1\}$, requiring $\mathbb E_p[f]<\tau$. Equals Aumann–Serrano riskiness [S]; ≈σ²/(2(τ−μ)). |
| R8 | Structured layer | min, max and mixture over 𝓜 |
| — | Multiplier robustness | $\max_q\mathbb E_q[\ell]-\vartheta\mathrm{KL}=\vartheta\ln\mathbb E_p[e^{\ell/\vartheta}]$ (sign corrected) |
| — | Diagnostics | Kish ESS = 1/Σq² (warn < 0.10N, block < 0.02N); maximum weight ratio; tail ESS; KL as "distance moved" |

**How the IC reads k\*** [I]. For any model P, $\mathbb E_P[\bar R]\ge7\%-k^\star\,\mathrm{KL}(P\,\Vert\,\hat P)$. In the prototype, k\* = 0.152, so every 0.05 nats of misspecification costs 76bp of guaranteed floor (illustrative).

**Rare-event calibration** [I-new]

| Nominal event probability | η = 0.01 | η = 0.02 | η = 0.05 | η = 0.10 |
|---|---|---|---|---|
| 1% | 2.70% | 3.57% | 5.51% | 8.05% |
| 0.2% | 1.11% | 1.63% | 2.87% | 4.56% |

- A 2.5% cap at η = 0.01 needs a nominal ≤ 0.88% (≈441 failing paths in 50k). That can be checked by simulation.
- A 1% cap at η = 0.10 needs a nominal ≤ 1.7×10⁻⁷, which cannot.

**Defaults**
- η = **0.05** for reporting (sweep 0.02 / 0.05 / 0.10).
- η_L = 0.01 for rare events.
- ε_W = 0.5pp.
- W1 radius = 0.5pp.

### 5.12 Views and IC pooling

**Entropy pooling:** $\min_q\sum_iq_i\ln(q_i/p_i)$ s.t. $Gq=b$, $Hq\le c$, $\mathbf 1^\top q=1$. The dual is solved by Newton or BFGS; its dimension equals the number of views.

**Confidence:** $q_c=(1-c)p+cq^\star$ (Meucci's linear blend) [C].

**Pooling**
- The default is the linear pool $\sum_mw_mq^{(m)}$. It preserves event probabilities and gives no member a veto.
- The log pool is a sensitivity. For views on common features, it equals a tilt by the weighted-average multipliers.

**Disagreement and decision relevance**
- Disagreement is the Jensen–Shannon divergence between members' posteriors.
- Decision relevance asks whether the action ranking changes under any member's posterior.

**Gates:** an LP feasibility check before solving; a warning above KL 0.25 nats; the Kish ESS gates; regeneration by importance sampling when blocked.

**Supported views:** factor means; event and regime-path probabilities; quantiles; rankings; cash-flow views (e.g. P(distributions/NAV < 12% for 2 years)); vol and correlation via sequential entropy pooling. A structural change requires re-simulation, not a view.

### 5.13 Safety filter (F)

$$a^{\text{safe}}=\arg\min_a\|a-a^{\text{prop}}\|_Q^2\quad\text{s.t.}\quad\hat g_k(\mathcal S_t,a)\le-\delta_k\ \forall k$$

- $\hat g_k$ linearizes T1.1–T1.5 and the H surrogates of T1.6–T1.8 around the latest H solution. Gradients come from duals and are checked by finite differences.
- $\delta_k$ are the amber buffers.
- It is a small QP (OSQP).
- It returns the projected action plus a "what changed and why" record.
- Probabilistic reachability (Abate et al. 2008 [S]) supplies a "probability of remaining viable" KPI.

---

## 6. Default parameters

| Parameter | Default | Range | Source |
|---|---|---|---|
| Steps | quarterly decisions; monthly engine and margin | — | [I] 01/10 |
| Simulator horizon | 40 quarters + terminal value | 20–60 | [I] 11 |
| HDP tree | 12 quarters; 1 × 40 × 25 per model; LDR in fans | 8–20 quarters | [I] 01 |
| Models | 6 + 1 held-out; equal weights, then IC-set | 4–8 | [I] |
| Paths | 10k (tuning); 50k (reporting); fresh 50k (test); 250k / importance sampling (tails) | — | [S] stream 10 SE table |
| SAA replications | 10 | 5–20 | [I] 01 |
| CRRA γ; shortfall α; λ_T | 3; 2; 1 | 2–5; 1–3; 0–2 | [I] 11; Fishburn [S]; [I-new] |
| Target | 10% nominal; 10-year rolling geometric TWR gross of distributions; W̃ accumulated at 10% | 5y secondary | [I]; ADIC to confirm |
| ε_R red event, 5y, per model | 1% (≈0.2%/yr); H share 0.60% | 0.5–5% | [I] 11; [I-new] |
| Planned payout (12m) | 97.5% | 95–99% | [I] 11; FTK [S] |
| Named stress | 24 months; PE distributions 0%; calls 1.5×; equity −40%; VM P99.5; 50% facility; no secondaries | 18–36 months | [I] 11, corrected |
| IG + cash | ≥ 8% of NAV | — | [S] deck |
| Economic leverage; debt | ≤ 1.3×; ≤ 10% of NAV (placeholder) | 1.0–1.5×; 0–15% | [I] 11/01; stream 06 |
| NAV-loan LTV | ≤ 15% per fund; ≤ 5% of NAV total | — | [I] 11; streams 05/06 |
| Beta overlay; overcommitment | ≤ 30% of NAV; V + U ≤ 80% of NAV | —; 70–90% | [I] 11; stream 09 |
| Robust floor | mixture median R̄₁₀ ≥ 7%; worst-model CVaR10% ≥ 0% | backstop −2% to +3% | [I]; potentially binding |
| KL η; η_L | 0.05; 0.01 | 0.02–0.10; 0.01–0.02 | [I] re-derived; [C] |
| W∞ ε_W; W1 radius | 0.5pp; 0.5pp | 0.25–1.0 | [I] 10, relabelled |
| ESS gates; view KL warning | 0.10N / 0.02N; 0.25 nats | — | [I] |
| Penalty tiers | 10⁴ / 10³ / 10² / 50 / 10 | orders of magnitude | [I-new] |
| κ^u; pacing gap closure | 0.5–1; 0.25–0.5 per quarter | tuned | [I] 01 |
| Drawdown | reported; provisional P(10y investment DD > 40%) ≤ 10% | IC-set | [I-new] |
| Funding base | SOFR 3.89% (2026-10-15) + spreads | curve | [S] FRED |
| Distribution yield (annual, on NAV) | drought 12–14%; normal 20–25%; crisis 5–10% | calibrate | [S] Bain/MSCI; crisis [I] |
| δ in D = δRV | drought ≈ 0.12–0.13 | — | [C] |
| Call intensity (annual, on unfunded) | 0.26–0.33; regime range 0.20–0.35 | ADIC data | [C] Luxenberg |
| Secondary discount | placeholder: normal 5–15%, stress 20–35%, plus size impact | — | [I]; stream 05 |
| Regimes; innovations; dwell | K = 4 + exit factor; t₅; crisis 6–18 months, expansion 36–60 months | K ∈ {3, 4, 5} | [S] G–T; [I] 10 |

---

## 7. Calibration targets

| Target | Value | As of | Source | Confidence |
|---|---|---|---|---|
| Buyout distributions / NAV | ≈14% (Q4-24 to Q3-25); below 15% for 4 years; lowest since 2008–09 | 2026-02-22 | Bain GPER 2026 (Fig. 19, MSCI data) | High [S] |
| Closed-end PE distributions | 12% of asset value in 2025, vs ≈20% 20-year average | 2026-06-11 | MSCI | High [S] |
| Buyout distribution rate | 12% H1-26 (15% in 2025) vs ≈27% historical; top-quartile exit 18.2× EBITDA; net cash flow +USD 21bn | 2026-10-13 | MSCI | High [S] |
| Holding period; overhang; secondaries | ≈7 years; ≈32,000 companies worth USD 3.8tn; secondaries +41%; continuation vehicles +62% but < 10% of exits | 2026-02 | Bain | High [S] |
| LP constraint; LBO funding | 53% say undrawn commitments limit new ones; 8–9% at 30–40% leverage vs 6–7% at ≈50% in 2015 | 2026-02 | Bain / PEI | High [S] |
| SOFR | 3.89% | 2026-10-15 | FRED | High [S] |
| JPM 2026 (compound; arithmetic / vol) | ACWI 7.0% (8.28 / 16.78); PE 10.2% (11.91 / 19.78); IG 5.2%; cash 3.1%; inflation 2.5%; PE–ACWI 0.81; ACWI–Agg +0.33; alternatives net of fees | 2025-09-30 | JPM LTCMA | High [S] |
| JPM 2027 | 60/40 7.0%; with alternatives 7.5%; US LC 7.5%; large-cap PE median manager 9.6% | 2026-09-30 | JPM | High (headlines) [S] |
| BlackRock (10y, gross) | US LC 8.97%; buyout 15.89% (σ 26.06); DL 9.31% unlevered; risk-premia-rise PE 9.36% | 2026-06-30 | workbook | High for the numbers; fee-adjust [S] |
| AQR (local real) | US LC 3.9%; buyout 4.2% net of a 3.5% fee; ±3% error at 50% | 2025-12-31 | AQR | High [S] |
| Fee-consistent ensemble | book 6.2–9.7%; P(5y≥10%) 27–51%; P(5y<7%) 31–55%; KL 0.02–0.06 | 2026-10 | stream 10 + verifier | Medium [C] |
| 60% PE / 40% ACWI (JPM-consistent) | ≈10.5% arithmetic; ≈17.7% vol; median ≈9.1%; P(10y≥10%) ≈43%; P(5y<7%) ≈39.5% | 2026-10 | verifier 11 | Medium [C] |
| Manager dispersion | ≈1,960bp PE vs ≈200bp public equity | 2025 | JPM | High [S] |
| MC precision (t₅, 13% vol, 50k) | SE(VaR99) ≈0.41pp; SE(ES99) ≈0.8pp; SE of a 5% probability ≈0.10pp | 2026-10 | stream 10 + verifier | High [I] |
| Detection error (20 years) | JPM–AQR ≈38%; BlackRock (fee-adjusted)–AQR ≈25–30% | 2026-10 | verifier 10 | Medium [C] |
| Endowment outcomes | NACUBO FY2025 10.9%; 10-year 7.7% (6.8% FY24); USD 5bn+ cohort 11.8% | 2026-02 | NACUBO-Commonfund, TIFF | High [S] |
| Sustainable payout | median-preserving ≈5–6%; mean-preserving ≈5.5–7.2% | 2026-10 | verifier 11 | Medium [C] |
| Reliability anchors | Solvency II 99.5% / 1y; LCR 30 days; FTK 97.5% | — | EIOPA, BIS, IPE | High [S] |
| Payout precedents | Alaska POMV 5% of 5-of-6-year average (FY28 USD 4.1bn); Yale collar 4.0–6.5% | 2026 | APFC, Yale | High [S] |
| Stress precedent | Harvard ≈USD 1bn PE secondary talks; USD 1.2bn contingency bonds | Apr 2025 | Crimson | High [S] |
| Luxenberg buyout model | steady-state D/I ≈ 0.49/yr (≈3.5× Bain); upper reference only | 2022 | Luxenberg et al., ICAIF '22, DOI 10.1145/3533271.3561769 (preprint arXiv:2207.07767) | Medium [C] |
| Illiquidity cost | ≈2% of wealth to hedge once-a-decade crises | 2014 | Ang et al. | High [S] |
| ADIC payout gap (illustrative) | **Unfunded USD 37bn**, calls 26%: USD 3.6–12.5bn/yr (14% distributions); USD 5.7–14.6bn (12%). **Unfunded USD 50bn:** USD 7.0–15.8bn; USD 9.1–18.0bn. Calls at 33% add ≈USD 2.7–3.7bn. Before new-commitment calls; liquid book ≈USD 71bn. | 2026-10 | stream 01 + verifier; [I-new] | Low; ADIC data needed |

**The model must reproduce:**
- drought distribution yields of 12–15% persisting ≥4 years, with 20–27% in normal and recovery states;
- ≈7-year holding periods;
- crisis secondary discounts and NAV-loan spreads (stream 05);
- a central path consistent with ≈7.7% 10-year endowment outcomes;
- the v8 stylised outputs (static SAA 7.3%, P(≥10%) 31.7%), as **code regression tests only**.

---

## 8. Computation, software and machine-checkable rubrics

**Sizing** [I, unbenchmarked]
- **H, full solve:** ≈1.8M variables per 1,000-leaf model tree, ≈5.4M for three models. Run it decomposed (Benders, or progressive hedging via mpi-sppy), or with 300–400 leaves per model.
- **H, what-if mode:** 2 models × 200 scenarios, warm-started (≈0.8M variables). Seconds to minutes with a commercial solver; tens of minutes with HiGHS.
- **P:** vectorized (50k × 40 × 300 per model); CMA-ES runs ≈200 iterations.
- **SDDP:** 10³–10⁴ iterations.

**Literature anchors**
- Boyd et al.'s measured run: ≈0.5M problems in 30 min on 32 cores [C].
- mpi-sppy reached tight gaps on the largest stochastic unit-commitment MIPs within minutes [S].
- Valladão et al. solved a Markov SDDP with 100 assets [S].

**Stack**
- numpy/scipy; JAX or numba.
- cvxpy with Clarabel, HiGHS and OSQP (present in the venv).
- Pyomo with mpi-sppy.
- pycma, Optuna, BoTorch.
- statsmodels, hmmlearn, arch.
- An in-house entropy-pooling solver.
- Phase 2: SDDP.jl via juliacall, or msppy (needs Gurobi).

Use interior-point duals without crossover, checked by finite differences.

**Rubric checks.** Any failure blocks the pack; each check is an Agentic-Scientist stage gate.

| Engine | Checks |
|---|---|
| E | stylised facts; CMA reproduction; PSD; fee and leverage flag per model; MC SE; seeds and hash |
| H | solver status; dual signs; penalty usage; Mak–Morton–Wood bounds; stability across replications; VSS/EVPI ≥ 0 on the surrogate; objective monotone in constraint tightness (within SAA tolerance); tree A/B stability |
| P | per-model Clopper–Pearson; held-out generator; optimism gap; count of policies tried; flags G1–G4; monotonicity in the cushion; seed stability; union-bound vs joint estimates |
| Consistency | H actions fall inside the tuned policy region, or the difference is explained; H surrogates agree with P metrics; view KL and ESS gates |

---

## 9. Cross-disciplinary insights inside the cluster

1. **Hydro water values are liquidity values** (01). SDDP cuts and cash duals price a marginal dollar by regime. Power-dispatch merit order becomes the liquidity merit order, and bank funds-transfer pricing becomes per-group liquidity hurdles.
2. **A digital option explains target-chasing** (11). The same pathology appears in quantile hedging and in VaR-constrained managers (Föllmer–Leukert; Basak–Shapiro). Hence no indicators in objectives, and α ≥ 1.
3. **Control engineering supplies the gate** (11). A safety filter (barrier-function logic), probabilistic reachability as a viability KPI, and hysteresis bands.
4. **Actuarial ruin theory supplies the payout and breach logic** (11). The de Finetti barrier gives the payout band. De Finetti's criterion (expected discounted payouts until ruin) does not bound ruin by itself, so Gerber–Shiu timing-and-severity penalties are added to give severity budgets. Browne's danger zone justifies risk that is monotone in the cushion.
5. **One exponential tilt** unifies entropy pooling, Breuer–Csiszár worst cases, Pesenti reverse stress and Hansen–Sargent robustness (10). Views, stresses and robustness checks are all probability vectors on one scenario matrix.
6. **Ambiguity has an operational definition** (10, 11). Detection error separates ambiguity from risk: providers are misclassified 25–38% of the time even with 20 years of data. Robust satisficing asks the IC for a target rather than a radius; under KL, fragility equals Aumann–Serrano riskiness.
7. **HOLD vs SELL is an American option** on a liquidity-adjusted payoff (01). The Longstaff–Schwartz / Brandt regression yields both continuation values and the Phase-1 terminal value.
8. **IRR⇔NPV plus distribution-inclusive wealth** makes owner-return targets affine. This removes the TWR non-convexity while keeping TWR for reporting (synthesis of 01 and 11).
9. **Bank and insurance supervision supply the reliability language** (01, 11). LCR and the contingency funding plan become the ADIC-LCR and the named-stress test; ORSA's appetite / tolerance / capacity become the bands; Solvency II and FTK anchor ε.
10. **Prospect theory warns about IC framing** (11). "On track for 10%?" invites risk-seeking after losses, so the pack leads with cushions, survival and the price of safety.
11. **The optimizer's curse applies to agents** (10). Use a locked test set, count the policies tried, and shrink the selected advantage.
12. **Illiquidity economics** (01). Ang–Papanikolaou–Westerfield and Dimmock–Wang–Yang imply no-trade bands that widen with secondary discounts, and staggered vintages valued as a liquidity asset.

**Insights from the synthesis itself:** constraints live where they can be computed; probabilities are verified, never optimized; DPI follows exit *volume*, not valuation; and units discipline is a rubric check, because four verifier corrections were convention errors.

---

## 10. Interfaces to the other clusters

| Cluster | What C1 needs | What C1 provides |
|---|---|---|
| **Private book, liquidity tools, leverage, action economics, return fusion** (04–08) | **04:** λ^call(S, age) and λ^dis(S, x^exit, age); desmoothing; vintages; drought calibration. **05:** δ^sec with size impact and capacity; NAV-loan and facility terms (spread, LTV(S), covenants); GP-led options; consent rules. **06:** leverage and debt caps; funding sources. **07:** fused (μ_i, σ_i) with bias calibration; ambiguity radii from mark disagreement. **08:** semantics, fixed costs, minimum sizes and delays for each action. | μ and ρ by regime; CV_i; v^S, v^R, v^L; forced-action ranges; merit order; price of safety; terminal values ω and ψ |
| **Distribution policy, sovereign liabilities, peers/TPA, overlay** (02, 03, 09) | **02:** payout-rule family (fixed %, Yale formal, POMV, barrier); TPA reference-portfolio convention. **03:** joint law of owner demand with oil and the scenario factors; NAV basis; deferral and injection options. **09:** κ_b, ϖ_b; VM/IM model; P99 30-day VM rates by regime; opportunistic P&L law; CSA; monetization rules. | Price of payout (+1pp → X bp, Y pp); sustainable-payout curves by CMA; hedge value at shadow prices and its constraint-dual value; liquidity charge on opportunistic losses in high-μ states |
| **Agentic architecture and IC deliberation** (12–14) | Cycle orchestration; LLM agents for drafting views, narrative and challenge; the elicitation protocol; override and outcome logs | Typed tools (`simulate`, `solve_hdp`, `robustness_card`, `ep_views`, `safety_filter`, `price_action`); an objective-report schema; rubric gates; scenario hashes; a data-snooping log; live what-ifs |

**Governance boundary** (from v8)
- LLMs extract, draft and challenge. Deterministic code owns the numbers, and the IC owns decisions.
- SR 26-2 (17 Apr 2026) supersedes SR 11-7 and excludes generative and agentic AI [S]. C1's engines fall under model-risk management; agents need a separate track (e.g. NIST AI 600-1 [S]).
- *The Agentic Scientist* credits base models and orchestration jointly [C]. C1's rubrics are the orchestration-side contribution.

---

## 11. What the IC sees (portfolio-math pack)

Every probability is shown with its central value, model range and MC standard error, e.g. "37% [26–38%] ± 0.2pp". Every number carries the scenario hash and the model version.

1. **Actions**, each with a stability score: the share of replications × models that select it.
2. **Tier-1 board:** nominal value, model range, Clopper–Pearson bound, KL(0.01) worst case, band and penalty usage.
3. **Frontier A:** P(10y ≥ 10%) vs worst-model P(red event over 5y). Colour shows payout; markers show robust feasibility; the marginal rate of substitution is annotated.
4. **Frontier B:** robust floor vs P(10%).
5. **Sustainability frontier:** real NAV₁₀ vs payout, with mean- and median-preserving lines per CMA.
6. **Liquidity panel:** survival-horizon and ADIC-LCR fans; margin coverage; μ_t by regime; ρ vs the facility spread.
7. **Price of safety:** from ε-sweeps and duals, in bp of CE return and pp of P(10%).
8. **Fragility and reverse stress:** k\*; η\* with its detection-error translation; the most plausible failure world; the Pesenti sensitivity ranking.
9. **Views:** member and pooled posteriors; Jensen–Shannon disagreement; decision-relevance flag.
10. **Decision cards** per proposal: ΔJ in root USD; Δ slack; r_j; Δk\*; reversibility; safety-filter adjustment; model range.
11. **Capability values** and VSS/EVPI, both on the surrogate.
12. **Gambling-detector flags.**

---

## 12. Open questions and data ADIC must supply

**Open questions.** Each gives the working assumption used until it is answered.

1. **Floor.** Confirm reading (b), the 10-year horizon, nominal vs real, and gross vs net of distributions. *Assumed:* D5.
2. **Target.** TWR or IRR? Over what horizon? Net of leverage cost? *Assumed:* 10-year geometric TWR, gross of distributions.
3. **Payout.** Who chooses within 5–10%? On what NAV basis? Can timing or the 5% minimum flex? Does owner demand co-move with oil? Are injections possible? *Assumed:* a hard 5% minimum on beginning-of-year NAV, with stochastic owner demand.
4. **Breach tiers.** Which recourse is amber, red or critical? *Assumed:* liquid sales and the facility are amber; PE secondaries are red; a payout below the minimum is critical.
5. **Action semantics** (01-R10). Does LEVER mean adding exposure, borrowing against the asset, or GP-level leverage? Does REFINANCE mean an ADIC-level NAV loan or a GP-level recap? What consents and delays apply? *Assumed:* add exposure; ADIC-level loan or facility.
6. **Leverage.** Economic cap, debt/NAV, sovereign or rating limits, facility and CSA terms. *Assumed:* the §6 placeholders.
7. **IC parameters.** Sign-off on ε_R, 97.5%, 24 months, the bands and the review cadence.
8. **Ambiguity set.** Membership, weights, η and the approver; whether to add GMO and RA.
9. **Drawdown appetite.** To be set after the IC sees the (d, α, β) frontier.
10. **Secondary capacity.** Annual volume by strategy and regime that can be sold without extra discount.
11. **Tooling.** Is Julia acceptable? Are commercial MILP/MISOCP licences available?
12. **Currency.** Confirm the USD base, and whether a non-USD liability view is needed.
13. **Elicitation.** How formal (SHELF-style), and should members be calibration-scored?
14. **Hedge monetization.** Does hedge P&L arrive as cash in stress, and how fast?

**Data requests**
- **Asset level:** quarterly NAV, calls, distributions and unfunded; vintage, strategy, GP; leverage, NAV-loan terms, pledge status; the three return marks with forecast dates; secondary indications; consent rights.
- **Portfolio:** liquid sleeves with haircuts; cash; facility and bond terms; CSA/IM; overlay positions; opportunistic P&L and margin history.
- **Owner:** payout rule, history, NAV basis and timing; fiscal and oil linkage; injections.
- **Market:** SOFR curve; vol surfaces; secondary price history; NAV-loan spreads; provider CMA files versioned by as-of date.
- **Governance:** IC parameter choices, model weights, override and outcome logs.

---

## 13. Provenance

**New computations.** Both ran in the project venv, isolated with `-I`.

- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\c1\c1_checks.py`. Computes:
  - the KL worst-case tables (they reproduce verifier 10's η_L table exactly);
  - the binding volatility for C4;
  - Clopper–Pearson and zero-failure sizes;
  - quarterly conversions and joint-to-period reliability;
  - the ADIC gap grid;
  - the k\* reading.
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\c1\c1_drawdown.py`. Computes i.i.d. lognormal 10-year investment drawdowns:

  | Mean / vol | CDaR95 | P(max DD > 40%) | P(10y ≥ 10%) |
  |---|---|---|---|
  | 8.5% / 12% | ≈33.6% | ≈0.5% | — |
  | 9% / 15% | ≈43.5% | ≈3.5% | — |
  | 10.5% / 17.7% | ≈48.8% | ≈7.6% | ≈43.7% |

  These are lower bounds, because regime persistence raises drawdowns. The script's crude two-regime variant is unmatched and not used.

**Key references** (full lists in the dossiers): Powell (2019); Pereira & Pinto (1991); Philpott & de Matos (2012); Dowson (2020); Klaassen (2002), *Management Science* 48(11):1512–1516, DOI 10.1287/mnsc.48.11.1512.261; Boyd et al. (2017) [C]; Luxenberg et al. (2022, ICAIF '22, DOI 10.1145/3533271.3561769) [C]; Nystrup et al. (2019); Campi & Garatti (2008); Rockafellar & Uryasev (2000, *J. Risk* 2(3):21–41); Brown, Smith & Sun (2010); Long, Sim & Zhou (2023); Aumann & Serrano (2008); Hansen & Sargent (2022); Breuer & Csiszár (2013); Glasserman & Xu (2014); Pesenti et al. (2019); Mohajerin Esfahani & Kuhn (2018); Browne (1999); Föllmer & Leukert (1999, 2000); Basak & Shapiro (2001); Chen & Sim (2009); Dybvig (1999); Busseti, Ryu & Boyd (2016; i.i.d., infinite horizon); Guidolin & Timmermann (2007); Bain GPER 2026; MSCI (2026-06-11, 2026-10-13); JPM LTCMA 2026/2027; BlackRock CMA (Aug 2026); AQR 2026; NACUBO-Commonfund FY2025; SR 26-2.

**Unverified [U] and never load-bearing:** GMO and RA CMAs; the SDDP.jl speed claim (dropped); the Towers Perrin horizon.

**Verified by the literature audit, so no longer [U]** [corrected 2026-10-18]:
- Meucci (2008), "Fully flexible views: theory and practice", *Risk* 21(10); arXiv:1012.2848.
- Rebonato & Denev (2014), *Portfolio Management under Stress*, Cambridge University Press.
- Pflug (2001), *Math. Programming* 89, DOI 10.1007/pl00011398.
- Pflug & Pichler (2012), "A distance for multistage stochastic optimization models", *SIAM J. Optim.* 22, DOI 10.1137/110825054.
- Campbell & Viceira (2002), *Strategic Asset Allocation*, Oxford University Press, DOI 10.1093/0198296940.001.0001.
- Bailey, Borwein, López de Prado & Zhu (2017), "The probability of backtest overfitting", *J. Computational Finance* 20(4), DOI 10.21314/JCF.2016.322. Crossref holds the record but gives no volume, issue or pages; 20(4) comes from the audit's web check.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2; the citation-integrity tables in `research/literature/01_mpo.lit.md`, `10_scenarios_robustness.lit.md` and `11_objectives.lit.md`; and `research/literature/recheck/10_scenarios_robustness.recheck.md` and `11_objectives.recheck.md`.

- §2, row 10-4/10-5: credited the ENS diagnostic to Meucci (2012), which the stream used without citing it.
- §5.7, payout top-up rule: marked the always-paid minimum as ADIC's adaptation, since a classic de Finetti barrier strategy has no minimum payout (11 re-check, Avanzi note).
- §5.10, regimes: cited Shu, Yu & Mulvey to the published *J. Asset Management* 25(5):493–507 (2024), DOI 10.1057/s41260-024-00376-x, not the arXiv preprint (synthesis §2.3).
- §5.10, paths: replaced "regression proxies … not nested simulation" with "regression-based nested simulation (few inner draws per outer scenario)" and added DOI 10.1287/opre.2015.1419 (10 re-check).
- §7, Luxenberg row: cited the ICAIF '22 proceedings version, DOI 10.1145/3533271.3561769, alongside the preprint (synthesis §2.3; 01 table).
- §9, item 4: added that de Finetti's criterion does not bound ruin by itself, which is why the Gerber–Shiu penalties are needed (11 re-check, Avanzi note).
- §13, key references: added the missing Klaassen (2002) entry, *Management Science* 48(11):1512–1516, DOI 10.1287/mnsc.48.11.1512.261 (synthesis §2.5; metadata confirmed via OpenAlex), and the Luxenberg venue.
- §13, [U] list: moved Meucci (2008), Rebonato & Denev (2014), Pflug (2001), Pflug & Pichler (2012), Campbell & Viceira (2002) and Bailey et al. (2017) to verified (01 and 10 tables; synthesis §2.5 for the Bailey et al. venue).
- Checked and left unchanged:
  - the Campi–Garatti minima, β and convexity caveat (rows 10-9 and 11-7/11-8 already match the re-checks);
  - Lange et al. (row 10-10 and §10 already say base model and orchestration act jointly);
  - the Mohajerin Esfahani spelling, and Rockafellar & Uryasev 2(3):21–41 (confirmed by the 10 re-check).
- Not applicable: no barrier-monitoring statistic from the G4 barrier re-run (`research/groups/addenda/G4_barrier_rerun/RESULTS.md`) appears in this file.
