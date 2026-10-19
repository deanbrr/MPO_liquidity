# Design review: Quant / CRO judge

**Panel:** ADIC Agentic Total-Portfolio Laboratory, architecture selection. **Judge:** Quant / CRO. **Date:** 2026-10-18.
**Proposals judged:** PA (quant rigor), PB (agentic lab), PC (IC decision room), PD (pragmatic production), PE (the user's blueprint, judged on its ideas).

> **SYNTHETIC.** Every ADIC balance, probability, price and solve time quoted below comes from the synthetic working book (context §1A, census v1.0 or v1.1), the research prototypes, or random-coefficient *structural proxies* of the optimizer. None of it is ADIC data.

**Citation keys.** 00_SYNTHESIS = `research/00_SYNTHESIS.md` v1.1; GROUPS = `research/groups/01_GROUPS_SYNTHESIS.md`; GROUPS gap_0k = `research/groups/addenda/gap_0k.md`; gap_0k = `research/addenda/gap_0k.md`; brief = `design/00_DESIGN_BRIEF.md`; paper l.N = line N of `inputs/agentic_scientist_2610.18933v1.txt`. Proposal sections are cited as "PA §4.8.4" and so on.

---

## 1. Verdict in brief

| Rank | Proposal | Overall (1–10) | One-line verdict |
|---|---|---|---|
| 1 | **PA** quant rigor | **8.1** | The most coherent multi-period formulation and the only one that prices the binding T6 gate in every model class. Thin agent layer; misses the three groups addenda; searches on one generator family |
| 2 | **PD** pragmatic production | **7.8** | The best engineering, the best liquidity and overlay realism, and the only proposal current with GROUPS gap_01 and gap_03. Its H runs on M1–M3 only, so λ omits the worlds where T6 binds |
| 3 | **PB** agentic lab | **7.1** | Best-in-class verification infrastructure: seal service, commit-reveal seeds, anchored-residual DSL, planted-effect lab calibration. Its quant core is the synthesis transcribed, with H on M1–M3 and a payout slot in the DSL |
| 4 | **PC** IC decision room | **6.9** | The best IC and Treasury operating model: Decision Register, computed shadow IC, owner-draw *response* decision. H uses a risk-neutral terminal objective, and M4–M6 sit outside search |
| 5 | **PE** user blueprint | **2.5** | Right instincts but a mathematically incoherent objective that maximizes P(10%), makes the payout a decision and inverts REFINANCE/LEVER. It is a source of grafts, not a base |

**Recommendation: an explicit composite on PA's quant core.** Take PA's formulation, Phase I, certificates and error ledger as the base. Build them on PD's ledger kernel, package skeleton, increment plan and groups-addenda content. Wrap them in PB's evaluator, seal service and anchored-residual DSL. Put PC's Decision Register and computed shadow IC in front. Then close the fourteen must-fix items in §8 whichever base is chosen. Three of them are shared defects of all four generated proposals:
- the binding stressed worlds (M4–M6) must be inside H's tree and the search plane;
- model identity must not be learnable inside the tree;
- the GROUPS gap_02 corrections (census v1.1, FBE-R, misspecification gates) are missing everywhere.

---

## 2. How I scored

**Criteria.** Q1–Q8 as set by the panel. **Weights for the overall score** (my CRO weighting; the overall is a judgement, and the weighted mean is shown for transparency):

| Q1 formulation | Q2 research faithfulness | Q3 liquidity & funding | Q4 private markets & fusion | Q5 overlay | Q6 robustness & verification | Q7 synthetic truth | Q8 model risk |
|---|---|---|---|---|---|---|---|
| 0.18 | 0.18 | 0.15 | 0.10 | 0.10 | 0.10 | 0.07 | 0.12 |

**What I checked beyond reading.**
- **Benchmark artifacts.** The solve times the proposals quote come from scripts in the session scratchpad (`...\scratchpad\hbench\`, `pc_bench\`, `pd_bench\`). Their saved JSON outputs match the quoted figures:

  | Artifact | What it shows | Matches |
  |---|---|---|
  | `hbench/run_1200x12.json` | 419,098 columns; HiGHS IPX stops at the 300 s limit | PA §4.8.3 "not converged in 300 s" |
  | `hbench/run_2000x8.json` | 359,098 columns; stops at 300 s | PA §4.8.3 |
  | `pc_bench/hn_lp_bench_20x50.json` | 1,000 leaves: IPM 136.3 s, dual simplex 571.4 s, CLARABEL 207.5 s | PC §4.11. PC's 500-leaf IPM figure (20.2 s) is not in the saved JSON; only the CLARABEL run (80.8 s) is |
  | `pc_bench/sim_kernel_bench.json` | 10k paths × 400 cohorts × 120 months in 3.96 s on 8 threads | PC §4.2 |
  | `pd_bench/lp_1000_12_simplex.json`, `lp_2000_12_simplex.json` | Dual simplex 90.4 s and 286.1 s | PD §4.11 |

  PA's default (1,200 × 8, 53 s) and PD's default (600 × 12, 32 s) were not saved as JSON, although the scripts exist. PB's times are estimates [I]. All of these are random-coefficient proxies, so production timing must be re-benchmarked (must-fix 11). *SYNTHETIC proxy.*
- **Environment.**
  - The project venv's HiGHS 1.15.1 (highspy) exposes `feasibilityRelaxation`, `getIis` and `getRanging`, so gap_02's Gurobi `feasRelax` has a native replacement.
  - cvxpy's installed solvers are CLARABEL, SCS, ECOS, SCIPY, HIGHS, ECOS_BB and OSQP.
  - **Not installed:** `cma`, `optuna`, `pymc`, `numpyro`, `jax`, `QuantLib`, `chainladder`, `scoringrules`, `pyomo`, `mpisppy`, `SALib`. Several of these are named in 00_SYNTHESIS §8 and §10.
- **Paper mechanism.** PB's anchored-residual DSL claims to reproduce the paper's exact switch-off null. The paper's construction is a zero-initialised bounded multiplicative residual, g(v) = 2tanh(3v) ∈ [½, 2], on a CMA-ES core; forcing every gate to 1 recovers the classical algorithm (paper l.2687–2700). PB §5.4 TR5 is a faithful transplant.

---

## 3. Score table

| Criterion | PA | PB | PC | PD | PE |
|---|---|---|---|---|---|
| Q1 Multi-period formulation | **9** | 6.5 | 6 | 7.5 | 2 |
| Q2 Faithfulness to research | **7.5** | 6 | 6 | 7 | 2 |
| Q3 Liquidity & funding realism | 8 | 7 | 8 | **8.5** | 3 |
| Q4 Private markets & fusion | 7.5 | 7.5 | **8** | **8** | 4 |
| Q5 Overlay realism | 8 | 7 | 7 | **9** | 4 |
| Q6 Robustness & verification | 8 | **8.5** | 7 | 7.5 | 2 |
| Q7 Synthetic data & recovery | 7 | **8** | 7.5 | 7.5 | 1 |
| Q8 Model risk & failure modes | **9** | 7.5 | 6.5 | 8 | 2 |
| Weighted mean | 8.09 | 7.06 | 6.87 | 7.82 | 2.48 |
| **Overall (judgement)** | **8.1** | **7.1** | **6.9** | **7.8** | **2.5** |

### 3.1 Research-findings checklist

✓ = done; ~ = partial or inconsistent; ✗ = missing or contradicted.

| Finding (source) | PA | PB | PC | PD | PE |
|---|---|---|---|---|---|
| λ and quantity envelopes from one solve (L14; GROUPS §4.3–4.4) | ✓ §4.8.6 | ✓ §4.9 | ✓ §4.10 | ✓ §4.10 | ✗ |
| Feasibility before prices; duals only from the restored problem (L15; gap_02 §4) | ✓ §4.8.4 | ✓ §4.10a | ✓ §4.11 | ✓ §4.11 | ✗ soft penalty |
| Pinned-dual guard extended to the T6 CVaR surrogate (GROUPS gap_01 §6 item 5) | ✓ Phase I-b | ✗ | ✗ | ✗ | ✗ |
| T4′ = s\*(θ\*) with hashed canonical conventions (00_SYNTHESIS §2.3(d), §4.9) | ✓ | ✓ | ✓ | ✓ (+ pooled θ\* 0.79) | ✗ |
| T6 bands by model class (gap_02 §3) | ✓ | ✓ | ✓ | ✓ | ✗ |
| **Worlds where T6 binds (M4–M6) inside H and search** | ✓ all six | ✗ H on M1–M3 | ✗/? search M1, M3; H unspecified | ✗ H on M1–M3; M4, M6 never searched | ✗ |
| ≥ 2 generator families in search (00_SYNTHESIS §4.1, §5.1 item 4) | ✗ E only | ✓ F1 + F2 | ✓ VAR-bootstrap | ✓ embargoed B1 | ✗ |
| P(10%) reported, never optimized (L9) | ✓ | ✓ (gambling signature is a Gate-1 failure) | ✓ (Θ forbids indicators) | ✓ | ✗ |
| Explicit return bridge (gap_05; 00_SYNTHESIS §4.12) | ✓ | ✓ | ✓ | ✓ | ✗ |
| Overlay position layer with OV1–OV3 (gap_03) | ✓ (OV1/OV2 are rows in H) | ✓ (in `correct`) | ✓ | ✓ | ✗ |
| Overlay group accounting: three books, services, ex-ante tail credit, sizing (GROUPS gap_03) | ✗ | ✗ | ✗ | ✓ | ✗ |
| F_t defined as a calibrated 3-month stress probability, distinct from k_MS (gap_04) | ✓ | ✓ | ✓ | ✓ | ✗ |
| Tier-2 accrual at the fund's own return (00_SYNTHESIS §4.9) | ✓ | ✓ | ✓ | ✓ | ✗ U(D_t) |
| Owner draw exogenous; no payout lever in the base policy (brief §6; context §1A) | ~ de Finetti top-up | ~ `payout_topup` slot | ~ "top-up rule" | ✓ | ✗ |
| REFINANCE = cash-out; LEVER = exposure-up (brief R8) | ✓ | ✓ | ✓ | ✓ | ✗ inverted |
| Hedge-fund term state machine; φ(h,S) is the only ladder interface (gap_01 §5) | ✓ | ✓ | ✓ | ✓ | ✗ |
| IG 8% elastic / 4% hard; facilities at 0% in 30-day rows | ✓ | ✓ | ✓ | ✓ (+ CVaR₉₉ VM) | ✗ |
| Readiness-Red vs event-Red (GROUPS gap_01 §1.3) | ✗ | ✗ | ✗ | ✗ | ✗ |
| Execution vs structural recovery; KKT cap at the cheapest spare lever (GROUPS gap_01 §2) | ✗ | ✗ | ✗ | ✓ | ✗ |
| NAV facility demoted (pledge cap ≈ $2.1bn; GROUPS gap_01 §0 item 7) | ✗ | ~ | ~ | ✓ | ✗ |
| Census v1.1, FBE-R, misspecification gates G-A–G-E (GROUPS gap_02) | ✗ | ✗ | ✗ | ✗ | ✗ |
| H objective is a piecewise-linear proxy of J, with an H–P consistency test | ✓ | ~ (shared objective, no test) | ✗ risk-neutral | ✓ Kendall τ | ✗ |
| Solve times measured on HiGHS/CLARABEL | ✓ [M] | ✗ [I] | ✓ bench | ✓ bench | ✗ (Gurobi) |

---

## 4. Proposal-by-proposal justification

### 4.1 PA: quant rigor first (overall 8.1)

| Q | Score | Justification |
|---|---|---|
| Q1 | 9 | One transition operator Φ generates both the simulator and H's rows, with conservation to 1e-10 and H's cash path reproducing the simulator's to 1e-9 (§4.0, §4.8.2 H1, §4.12). It uses all four Powell classes with distinct jobs (§4.8.1). Phase I-a and I-b use highspy `feasibilityRelaxation` and `getIis`, and store a Farkas certificate (§4.8.4). ℓ_n = M_n/(μ_n − M_n) is *derived* from cash stationarity (§4.8.6). Column generation carries a Farley bound Γ, and the Level-B MILP carries an (m + 1)·max ρ gap bound (§4.8.5). **Deduction:** the stage-1 nodes are "6 worlds × 4 strata" (§4.3), so recourse can condition on model identity after one quarter. That contradicts PA's own rule that "a node carries only observable information". The tail stratum is also defined on a 24-month forward statistic, G\* |
| Q2 | 7.5 | Implements L1, L14 and L15, T4′, T6 bands by world class inside H (§4.8.2 H4), report-only P(10%), the bridge, OV1–OV3, F_t and the own-return accrual (§4.1, §4.9). **Misses:** GROUPS gap_01 (readiness- vs event-Red; execution recovery; the spare-lever cap), gap_02 and gap_03. Search runs on a single generator family (§4.10; 00_SYNTHESIS §5.1 item 4 asks for ≥ 2). A de Finetti payout top-up sits in the standing policy (§4.8.1) without a Mode A/H restriction |
| Q3 | 8 | CF owns the cash rows, λ, FTP, and envelopes priced only inside their ranging interval (§4.8.6). Ladder, CFP stage, the HF φ interface, IG 8/4, facilities at 0% in 30-day rows and canonical T4′ rows are all present (§4.7, §4.8.2 H6). **Missing:** readiness- vs event-Red, and the spare-lever KKT cap. The LP-portfolio NAV facility stays a REFINANCE lever (§4.6) despite its pledge cap |
| Q4 | 7.5 | Group engines and the lens table follow GROUPS §3 (§4.4, §4.6). The market anchor is the best specified of the five: the IRR is solved on buyer cash flows, with the buyer–seller PME gap by fund age as its bias (§4.5). A cohort-exactness rule controls aggregation error (§4.2). **Missing:** FBE-R and its misspecification gates (GROUPS gap_02 §3), and the Zombie-NAV and catalyst diagnostics (brief §6 graft 2) |
| Q5 | 8 | OV1 and OV2 enter H as linear rows built from precomputed stress revaluations. SIMM IM and OV3 are linearised conservatively in H and re-checked exactly in module F (§4.7). This is the only proposal in which net-vega governance is enforced *inside* the optimizer. **Missing:** GROUPS gap_03's three-book lens, services ledger, ex-ante tail credit and reconciled sizing |
| Q6 | 8 | Search on six worlds; final plane of fresh seeds, held-out generator and misspecification ensemble; qualification by an intersection–union test with Holm and pre-declared materiality (§4.10). Switch-off null, single-change ablations, shuffled-signal placebo, DSR/PBO/α-investing (§2 P4–P6), and a tolerance cascade (§4.9). **Deduction:** no second generator family in search |
| Q7 | 7 | SYN-ADIC-177 in three layers, SBC, ±5pp recovery and taint (§7). It builds on census v1.0, which GROUPS gap_02 §1 shows fails V6, and has no estimator-misspecification gates |
| Q8 | 9 | The error ledger A1–A16 gives each approximation a certificate or test, an acceptance level and a fallback (§4.12). A consistency contract runs in CI. Dual instability is named as the top risk, with a stated fallback: publish FTP as a band and decide by forced re-solves (§10) |

- **Fatal flaws:** none.
- **Serious, must be fixed:** model-world branching in the tree; one search generator family; missing groups addenda; the payout top-up; the NAV facility. Lesser: three workers (2 shared + 1 isolated) against brief P9's default of 2.
- **Best ideas:**
  - Phase I-a/I-b with IIS and a Farkas certificate, plus the extended pinned-dual test μ_n − M_n > 0 (§4.8.4);
  - the column-generation certificate Γ ≤ 5bp CE and the Level-B gap bound (§4.8.5);
  - λ derived from KKT; one-sided dual intervals at kinks; RHS ranging; H–P agreement on ∂J/∂cash₀ (§4.8.6);
  - OV rows inside H (§4.7);
  - the error ledger and consistency contract (§4.12);
  - the tolerance cascade, under which Tier-2 gains may not come from Tier-1 erosion within one paired SE (§4.9);
  - counter-based CRN keyed by (seed, world, plane, path, month, source, slot) (§4.3);
  - the Aumann–Shapley "what moved H" path integral (§4.11);
  - the horizon-invariance test T_H = 8/12/16 (§4.9);
  - HiGHS–CLARABEL agreement as a CI check (§4.12).

### 4.2 PB: agentic laboratory first (overall 7.1)

| Q | Score | Justification |
|---|---|---|
| Q1 | 6.5 | Phase I per tier on HiGHS with an IIS, a restored LP, a selection MILP outside the tree (§4.10a–c), and P0 plus anchored residuals as a clean, searchable PFA class (§5.4). **But** H runs on M1–M3 only: "3 × 400 (M1–M3)" and "M4–M6 discipline H through the gates" (§4.10). λ therefore never sees the worlds where T6 binds. Duals come from IPM `marginals` with no stated crossover, terminal values are unspecified, and solve times are estimates |
| Q2 | 6 | Faithful on L14 and L15, T4′, T6 bands, report-only P(10%), OV1–OV3, F_t and the accrual. It states outright that "payout is not a decision variable" (§4.8). **But** M4–M6 are excluded from search (§4.3), and the DSL exposes a `payout_topup` slot (§5.4) through which search could optimize the owner's payout. No groups addenda |
| Q3 | 7 | CF runs as the internal bank: two price sets, vintage locking, the contingent-liquidity charge (§4.9), ledger rows LR1–LR8 and CFP stages. The first campaign "starts in CFP stage Red" (§5.14) with no readiness/event distinction, so the event-Red playbook (line draws, P2S, amber sales) would fire on a hypothetical-stress indicator |
| Q4 | 7.5 | Group lens table (§4.6). Market anchor y^MKT = (1 + y_B)p^{1/D} − 1 (§4.5); I checked it: 91%, D = 3.4 and a 12% hurdle give ≈8.9%. Zombie-NAV, half precision for recovery forecasts without catalysts, and P(forecast achieved within k quarters). **Missing:** a buyer–seller bias correction on the anchor, and FBE-R |
| Q5 | 7 | Standard position layer. OV1–OV3, surface no-arbitrage checks and the ≥ 3-quote rule for hybrids are part of `correct` (§4.7); OverlayStructure is an idea type. No GROUPS gap_03 accounting |
| Q6 | 8.5 | The strongest verification infrastructure:<br>• a CRO-owned seal service with commit-reveal HMAC seeds (§5.2 B4);<br>• 15 sealed worlds, including a second family F2 and engine-level misspecification MS1–MS6 (§4.3);<br>• an MDE ≤ ε_mat gate and NOT_ASSESSED as an outcome (§5.7);<br>• an exact null control by construction (TR5);<br>• integrity drills (§5.16).<br>**Deduction:** the binding worlds are first seen in the run-once sealed plane, where failures can no longer inform search |
| Q7 | 8 | Planted-effect campaigns (a true gain, a leak and a null world) calibrate the lab's power and false-qualification rate (§7). Only `synth/` may create data (§5.2 B8). Census v1.0; no FBE misspecification gates |
| Q8 | 7.5 | Names the right top risk, that the lab certifies a misspecification shared by every world, and gives mitigations. Also covers zero yield, statistical power, isolation and meta-adaptivity (§10). Less on quantitative approximation error |

- **Fatal flaws as written:**
  1. λ, FTP and envelopes come from an H solved on M1–M3 only, so the binding T6 price is absent from the published curve.
  2. The `payout_topup` DSL slot lets search optimize the owner's distribution.

  Both are easy to fix.
- **Best ideas:**
  - the seal service with commit-reveal final seeds and a 4-process trust boundary (§5.2);
  - the anchored-residual PolicySpec with identity at zero, which makes the switch-off null exact (§5.4, TR5; paper l.2687–2700);
  - planted-effect lab calibration (§7);
  - the MDE ≤ ε_mat gate and the NOT_ASSESSED label (§5.7);
  - claims rendered from typed placeholders by a validator that rejects literal digits (§5.10);
  - the integrity-drill table (§5.16);
  - the optimizer's own output treated as a candidate, C_H (§5.6);
  - blueprint archetypes A/B/C as frozen controls (§5.9);
  - a `predicted_effect` field in each IdeaBundle, scored later (§5.4).

### 4.3 PC: IC decision room first (overall 6.9)

| Q | Score | Justification |
|---|---|---|
| Q1 | 6 | Phase I runs as sequential HiGHS LPs with a deletion-filter IIS. The H-LP is benchmarked, and duals are taken *after crossover*, which pinned-dual detection needs (§4.11). **But** H's objective is risk-neutral: linear terminal value, ω·NAV − ψ·U + L − Debt, less a linear shortfall (§4.11). 00_SYNTHESIS §4.8 rejects a risk-neutral objective because it hugs constraint boundaries, and it misaligns H's prices with Tier-2 J. There is no H–P ranking test, and the worlds in H are unspecified |
| Q2 | 6 | L14 and L15, T4′, T6 bands, report-only P(10%) (the value set Θ forbids indicators; §4.12), the bridge and the accrual are all present. **But** M4–M6 are confined to the misspecification plane (§4.3), G4 checks non-inferiority only in search worlds (§5.4), the standing policy keeps a "top-up rule" (§4.11), and there are no groups addenda |
| Q3 | 8 | The best operational framing of Corporate Finance. Register entries cover:<br>• Q2, the owner-draw *response*: funding the next four instalments;<br>• Q3, buffer, funding and leverage;<br>• E3, the CFP stage-change playbook;<br>• E4, owner overrides (§6.1).<br>The liquidity-margin row LM (blueprint graft 3) uses canonical facility credit (§4.11), and there is an FTP dispute committee with mismatch P&L (§6.8). **Missing:** readiness- vs event-Red |
| Q4 | 8 | The market anchor carries its own bias prior, a precision set by bid dispersion, and a second source; I checked its inversion against GROUPS §3.2 (≈9.0%) (§4.5). Zombie-NAV and no-catalyst flags are made operational. Credibility is shown as information value in dollars, with a route to contest it (§6.8). Group seats hold their own forecasts at face value, so the political wedge becomes measurable (§6.5). **Missing:** FBE-R |
| Q5 | 7 | Position layer and OV1–OV3. The stress-coverage ratio (graft 3) sits on the offset card; the contingent-liquidity charge and LSMC monetization are included (§4.8). No GROUPS gap_03 |
| Q6 | 7 | Planes, gates G4–G6, placebo, archetypes and the null control (§5.4; §2.2 P6), plus offline evaluation suites for the room (§6.9). Search covers only M1, M3 and a hybrid generator |
| Q7 | 7.5 | The standard generator plus planted-bias recovery of b^u, b^f and κ_g per group, and recovery tests for the F_t calibration and the owner model (§7, §8). Census v1.0 |
| Q8 | 6.5 | The risk table centres on process burden; it acknowledges shared misspecification and LP scale (§10) but says little on quantitative approximation error |

- **Fatal flaws:** none strictly. Two serious defects:
  1. the risk-neutral H objective, with no H–P consistency test;
  2. M4–M6 excluded from search, with H's world coverage unspecified. This becomes fatal if H runs on the search worlds.
- **Best ideas:**
  - the Decision Register and evidence compiler, which never fills a missing metric silently (§6.1);
  - the computed shadow IC: seats are (q_k, θ_k) pairs inside an admissible set Θ, and their implied actions come from the optimizer, so the seats are P1-compliant (§6.5);
  - recusal enforced in software;
  - Q2 framed as how to fund the exogenous draw, not what the draw is;
  - the LM row with canonical credit (§4.11);
  - the consent agenda and a 180-minute attention budget (§6.6);
  - signposts with root-found flip values, plus commitment plans (§6.7);
  - duals taken after crossover (§4.11).

### 4.4 PD: pragmatic production path (overall 7.8)

| Q | Score | Justification |
|---|---|---|
| Q1 | 7.5 | One ledger kernel serves three uses: forward (P), linearised (H) and on s\* (§1, §3 interfaces). H uses PWL CRRA and a CVaR₉₉.₄ on signed margins resting on ≥ 30 tail leaves through oversampling and reweighting (§4.11). Phase I uses highspy `feasibilityRelaxation` and `getIis`. H–P consistency is tested by a Kendall-τ ranking test and a replay test (§4.11). **Deduction:** H runs on M1–M3 only (§4.15, nightly batch); the T6 surrogate has no pinned-dual guard; there is no selection certificate |
| Q2 | 7 | The only proposal that folds in GROUPS gap_01: execution recovery with d₀ = $11.3bn and u\* = 0, the spare-lever KKT cap, and the pooled θ\* of 0.79 (§4.10, §4.12). It also folds in GROUPS gap_03 (§4.8). **But** M4 and M6 are "never searched" (§4.3) and H excludes M4–M6, so λ omits the binding T6 worlds. No GROUPS gap_02 |
| Q3 | 8.5 | CF owns the ledger and λ. T3 is hardened from P99 to CVaR₉₉ stressed VM (§4.12). The spare-lever cap comes with a regression test for revolver-signed μ ≈ 0.0113 against 0.243 without it (§4.10; SYNTHETIC). Execution recovery is exercised from increment 1, and the NAV facility is pledge-capped. **Missing:** readiness- vs event-Red |
| Q4 | 8 | Group lens table (§4.6). The market anchor covers SELL (Secondaries bids) and REFINANCE (Capital Solutions reserve quotes), both conflict-flagged. Zombie-NAV and catalyst halving are included (§4.5), and asset-level simulation keeps holding detail (§4.2). **Missing:** FBE-R |
| Q5 | 9 | Three books, each with an S/H/R/L lens; REFINANCE is allowed only if OV1–OV3 hold before *and* after (§4.6). The floor ladder is sized from the budget: $7.1bn at 0.15% and 3.74% a year (SYNTHETIC). Tail credit is booked ex ante, with the IC policy residual; there is a services ledger and a fatigue tracker (§4.8, §6). Acceptance requires reproducing the SIMM worked example: $609.7m → $418.9m and an offset ratio of 1.77 (§4.8) |
| Q6 | 7.5 | Two families in search, including the embargoed bootstrap B1, and a time-disjoint B2 in the final plane (§4.3). Gates G1–G3 (§5). Reconciliation tests: H vs P replay, cohort vs asset, DVA sums. Cubes are regenerated and verified by checksum (§4.2), and penalty-×10 invariance is measured. **Deduction:** M4 and M6 are not searched |
| Q7 | 7.5 | SBC on the FBE, the regime HMM and the draw model; MRM holds the sealed truth (§3, §8). Census v1.0 |
| Q8 | 8 | Dual instability is ranked most severe, with concrete mitigations. Cards fall back to "select on P" when the H–P test fails. SDDP-lite is built only if that test fails. Failures stop the run loudly (§10, §4.15) |

- **Fatal flaw as written:** H runs on M1–M3 and M4/M6 are never searched, so λ, FTP and envelopes omit the worlds where T6 binds. In gap_02's Mix A, the binding Clopper–Pearson bound of 0.98% is in M5, and the M6 class breaches capacity without the band (SYNTHETIC). Easy to fix.
- **Best ideas:**
  - the ledger kernel shared by P, H and the stress test (§1);
  - performance measured on the target laptop (§4.15);
  - asset-level simulation, with cohorts only above 1,500 units behind a KS reconciliation (§4.2);
  - the spare-lever cap and execution-recovery semantics (§4.10, §4.12);
  - the H–P Kendall-τ and replay tests (§4.11);
  - GROUPS gap_03 overlay accounting (§4.8);
  - T3 hardened to CVaR₉₉ VM (§4.12);
  - chronologically disjoint bootstrap families B1 and B2 with an embargo (§4.3);
  - porting `hf_ladder.py`, `t1_engine` and `bridge.py` as regression fixtures;
  - the increment plan and team sizing (§8).

### 4.5 PE: the user's blueprint (overall 2.5)

| Q | Score | Justification |
|---|---|---|
| Q1 | 2 | The objective (§2.5) is incoherent:<br>• a distribution utility U(D_t);<br>• an indicator 𝟙(CAGR₀→T ≥ 10%), a terminal event placed inside a per-period discounted sum;<br>• a per-period CVaR term inside an expectation;<br>• a soft liquidity-breach penalty, all under a Wasserstein min.<br>There is no feasibility step, so the penalty prices pin (L15). There is no policy-class structure beyond "MPC/SDDP" |
| Q2 | 2 | It contradicts:<br>• L9: P(10%) sits in the objective, and the discovery agent maximizes P(Return ≥ 10%) (§4 Phase 3);<br>• L15;<br>• the owner-set payout: D_t is part of the policy π (§2.5);<br>• the user-confirmed definitions: NAV lending and preferred equity are labelled LEVER, and an asset-level recap, a GP decision, is labelled REFINANCE (§2.3).<br>It has no T4′, no T6 and no bridge |
| Q3 | 3 | The liquidity-margin row (§2.4) is a useful idea, but it counts unused facilities and all public holdings at 100%. Treating the tail hedge as liquidity that pays when λ peaks is right in spirit. There is no CF internal bank, no hedge-fund terms and no CFP |
| Q4 | 4 | Good ideas: a market-implied fourth signal, Zombie-NAV, a catalyst requirement and hierarchical shrinkage (§2.2, §3.1). But the posterior is ad hoc and uses "ActMomentum", whereas the research ignores actuals before year 3 and shrinks them for persistence. There are no group-specific translations |
| Q5 | 4 | It sees the VM/IM coupling and proposes a stress-coverage test (§2.4; §3.1, agent 4). There is no Greek layer, no SIMM and no net-vega limits, and the opportunistic book is cast as the gap-closer to 10% |
| Q6 | 2 | The discovery agent "logs proven structural insights" with no sealed plane, no counting and no deflation; its illustrative "+14.2%" carries spurious precision |
| Q7 | 1 | No synthetic ground truth and no parameter recovery |
| Q8 | 2 | No failure-mode analysis. It claims robustness "even if macroeconomic correlations break down" |

- **Fatal flaws:**
  1. A P(CAGR ≥ 10%) indicator in a weighted objective, and as the discovery agent's fitness. This rewards gambling for resurrection (L9).
  2. The distribution as a decision with its own utility, contradicting the owner-set exogenous liability.
  3. REFINANCE and LEVER mislabelled against the user's confirmed definitions.
  4. Liquidity breach as a soft penalty, with no Phase I, so prices pin.
  5. A neural-operator surrogate as the live IC answer engine, which conflicts with P1.
  6. A stack that cannot run here: Gurobi/MOSEK, Stan/PyMC, LangGraph/AutoGen.
- **Best ideas (graftable):**
  - the market-implied fourth signal (§2.2);
  - Zombie-NAV, P(forecast achieved within k quarters) and catalyst milestones (§3.1);
  - the liquidity-margin row and the stress-coverage test (§2.4);
  - opposing institutional utilities, recast as an admissible Θ (§3.2);
  - archetypes A/B/C (§3.2);
  - natural-language what-ifs translated into typed overrides (§3.2);
  - the phased roadmap (§4);
  - the tail hedge as liquidity that pays when λ peaks (§2.4).

---

## 5. Cross-cutting defects (shared by the generated proposals)

1. **The binding worlds are outside the program that sets prices.**
   - PB (H on M1–M3), PD (H on M1–M3; M4 and M6 never searched) and PC (M4–M6 only in the misspecification plane) all separate the worlds that carry the binding Tier-1 gate from the program whose duals become Corporate Finance's FTP.
   - 00_SYNTHESIS L15 and GROUPS gap_01 §3 say that once T4′ is slack under a certified mix, "the binding price becomes T6's", carried by H's CVaR surrogate.
   - gap_02 §2.3 puts the binding CP bound for Mix A in M5 (0.98%), and gap_02 §3 puts the M6 class above its capacity band without the owner band (SYNTHETIC).
   - An FTP curve computed without those worlds is too low exactly where it matters.
   - Only PA puts all six worlds in search and in H (PA §4.3, §4.10).
2. **Model identity can be learned inside the tree.**
   - PA's stage-1 nodes are world-labelled (§4.3). PB and PD use per-model trees with a shared root; the synthesis itself puts "three models in the tree" (00_SYNTHESIS §4.8).
   - World-specific recourse after one quarter assumes the fund learns which CMA world it is in. That overstates flexibility, understates the cost of the M6-class constraint, and biases root actions and λ toward too little conservatism.
   - Note: 00_SYNTHESIS L11 reports that a detection test confuses providers 25–38% of the time even with 20 years of data.
3. **The groups addenda are only partly absorbed.**
   - No proposal adopts GROUPS gap_02:
     - census v1.1 seals PE unfunded at $16.4bn instead of $27.4bn, which v1.0 reaches only through histories that fail V6;
     - FBE-R is the production fusion;
     - the misspecification gates G-A–G-E;
     - the deterministic O3 performance module;
     - the overlap graph with gate V24.
   - No proposal implements readiness- vs event-Red (GROUPS gap_01 §1.3).
   - Only PD carries GROUPS gap_01's execution-recovery and KKT-cap corrections and GROUPS gap_03's overlay accounting.
4. **Payout levers have crept back in** as PA's de Finetti top-up (§4.8.1), PB's `payout_topup` slot (§5.4) and PC's "top-up rule" (§4.11). Under the user-confirmed Mode B they are admissible only in the Mode A/H counterfactual used to price the mandate (00_SYNTHESIS §4.9: "In Mode B the draw is exogenous").
5. **Dependencies missing from the environment.** 00_SYNTHESIS §8 and §10 name QuantLib/ORE pricing references, SALib, pycma/Optuna, chainladder, scoringrules and Pyomo/mpi-sppy; none is installed. Only PA, PC and PD handle part of this (in-house CMA-ES, DE, closed-form empirical Bayes).

---

## 6. Recommended base: an explicit composite

**Base: PA's quant core**, chosen for Q1 and Q8. It is the only formulation in which:
- λ is derived from the KKT conditions;
- Phase I covers the T6 surrogate as well as the deterministic rows;
- asset selection carries a certificate;
- every approximation sits in an error ledger with a test and a fallback.

It is assembled as follows.

| Layer | Take from | Notes |
|---|---|---|
| Formulation, Phase I-a/I-b, duals, certificates, error ledger, tolerance cascade | **PA** §4.8–4.12 | Apply must-fix 1–3 to PA's tree |
| Ledger kernel, package skeleton, increments, performance budget, asset-level simulation | **PD** §1, §3, §4.2, §4.15, §8 | PA's cohort-exactness rule stays as the fallback above 1,500 units |
| Liquidity semantics: execution vs structural recovery, spare-lever cap, T3+ CVaR₉₉ VM | **PD** §4.10, §4.12, plus GROUPS gap_01 | Add readiness- vs event-Red (must-fix 4) |
| Overlay: OV rows in H (PA §4.7), with three-book accounting, services ledger, ex-ante credit and sizing | **PA + PD** §4.8, plus GROUPS gap_03 | |
| Evaluator, seal service, anchored-residual DSL, planted-effect calibration, drills, placeholders | **PB** §5.2–5.10, §5.16, §7 | Remove `payout_topup` |
| Decision Register, computed shadow IC (Θ), owner-draw response, LM row, consent agenda | **PC** §4.11, §6.1–6.7 | |
| Beliefs | PA §4.5 (anchor), PD §4.5 (anchor for REFINANCE), PB/PC/PD flags, **plus GROUPS gap_02 FBE-R** | Must-fix 7 |

**Contested choices, resolved.**

| Choice | Resolution | Basis |
|---|---|---|
| Cohorts or asset level in P | Asset level at ADIC's size; cohorts only above 1,500 units, behind PA's exactness bound and PD's KS test | PD §4.2 (10.9 s per 10k × 40, measured); PA §4.2 |
| Asset columns in H | Put them directly in the root while they fit (PD); otherwise column generation (PA). **Always report Γ** | PA §4.8.5; PD §4.11 |
| Solver | Choose per structure by a benchmark registered in advance (PA measured IPX fastest on its tree, PD dual simplex on its); always take duals after crossover | PC §4.11; PD §4.11; PA §4.8.3 |
| Clock for private engines | Quarterly is acceptable (PD's pushback) if PA's error-ledger row A1 passes (30-day need within 5%); keep a monthly T4′ ledger and monthly HF/VM clocks | PD §4.1; PA §4.12 |
| Planes | Search: E × {M1–M6} plus a second family. Final: fresh seeds, held-out FHS and misspecification variants | Must-fix 1 |
| Workers | 2 by default (brief P9), with an isolated challenger as an ablation only | PD §5; PB §5 |

---

## 7. Graft list, in priority order

1. **PA §4.8.2–4.8.4.** The node-wise sparse tree LP assembled in `scipy.sparse` and passed to `highspy`, with transition rows generated by the simulator's own Φ. Phase I-a on deterministic rows and Phase I-b on the T6/Tier-1B CVaR rows, via `feasibilityRelaxation` per tier, `getIis` and a Farkas certificate. The extended `test_no_pinned_duals` asserting μ_n − M_n > 0.
2. **PA §4.8.5–4.8.7.** Column generation with the Farley bound Γ (accept at ≤ 5bp CE); a Level-B MILP with an (m + 1)·max ρ gap and the marginal-asset agenda; forced re-solves for the top-20 cards; ℓ_n = M_n/(μ_n − M_n) from KKT; one-sided dual intervals at kinks; RHS ranging validity on envelope pricing.
3. **PD §4.10–4.12, with GROUPS gap_01.** The KKT cap at the cheapest spare lever, regression-tested on revolver-signed μ ≈ 0.0113 against 0.243 (SYNTHETIC). Execution recovery (d₀) kept separate from structural recovery (u\*), with group delivery shares φ_g. The 8 + 18 pinned-dual tests ported. The H–P Kendall-τ ≥ 0.8 ranking test and the replay test, with "select on P" as the fallback.
4. **PD §1, §3, §4.2, §4.15.** The ledger kernel as the single source of P, H and T4′ rows; the AssetEngine/Ledger/Policy protocols; asset-level simulation; regenerate-and-verify scenario cubes; performance budgets asserted nightly.
5. **PA §4.7 with PD §4.6/§4.8 (GROUPS gap_03).** OV1/OV2 as rows in H, with SIMM and OV3 linearised and re-checked in module F. Three books with S/H/R/L, REFINANCE only if OV1–OV3 hold before and after. The floor ladder sized from the budget. Ex-ante kernel tail credit with the IC policy residual. The services ledger, with gate V2 run on DVA ledgers. The fatigue tracker. The SIMM worked example as an acceptance test.
6. **PB §5.2, §5.4, §5.7, §5.10, §5.16.** The seal service with commit-reveal HMAC final seeds; the 4-process boundary with a tool firewall and per-request hash checks; the hash-chained ledger; the anchored-residual DSL with identity at zero (exact switch-off null); the MDE ≤ ε_mat gate and NOT_ASSESSED; rendered placeholders with a validator that rejects literal digits; integrity drills in CI.
7. **PB §7.** Planted-effect campaigns (true gain, planted leak, null world) to measure the lab's power, false-qualification rate and leak detection before the lab's thresholds (ε_mat, budgets) are trusted.
8. **PC §6.1, §4.12 and §6.5.** The Decision Register with evidence contracts, where a missing metric shows "EVIDENCE MISSING" and is never filled silently. The computed shadow IC: seats as (q_k, θ_k) inside Θ (γ ∈ [2, 6], λ_T ∈ [0, 2], shortfall exponent ≥ 1, a T6 limit no looser than the IC's tolerance, no indicators), with implied actions computed by the engine, recusal in software and the belief/value split. Q2, the owner-draw response, as the Treasurer's standing decision.
9. **PC §4.11 and PD §4.12.** The liquidity-margin row LM (blueprint graft 3) with canonical facility credit; T3 hardened from P99 to CVaR₉₉ stressed VM; the stress-coverage ratio shown on the offset card and hard only through OV2.
10. **PD §4.3.** A second generator family in search: an embargoed block bootstrap B1 fitted to data ending in 2015. A chronologically disjoint FHS family B2 (2017–2026) in the final plane (paper l.6879–6882).
11. **PA §4.5 with PD §4.5 and PB/PC flags.** A market anchor solved on buyer cash flows, with the buyer–seller PME gap by fund age as its bias; anchors for SELL (Secondaries) and REFINANCE (Capital Solutions reserve quotes), conflict-flagged; Zombie-NAV; half precision for recovery forecasts without catalysts.
12. **PA §4.9, §4.12.** The tolerance cascade; the horizon-invariance test (T_H = 8/12/16); HiGHS–CLARABEL agreement; the full error ledger A1–A16 as the MRM validation plan.
13. **PE (blueprint).** Archetypes A/B/C as frozen controls; natural-language what-ifs as typed, member-confirmed overrides; the Liquidity Guardian vs Total Return Architect tension expressed through Θ (never P(10%)); the phased roadmap framing.

---

## 8. Must-fix list (whatever the base)

| # | Item | Specification and test |
|---|---|---|
| 1 | **Every banded world inside H and the search plane** | Search: E × {M1–M6} plus a structurally different second family (B1 or F2). H's tree must include every model class that carries a T6 band, with per-class CVaR rows (M1–M5 and the mixture at 0.5/1/2%; M6 class —/2.5/5%). Final (run once): fresh seeds on M1–M6, the held-out FHS generator and misspecification variants. **Test** `test_binding_world_priced`: any class whose CP bound is ≥ 0.9 × tolerance must have a priced row in H, and every card's `priced_on` lists the classes it covers (00_SYNTHESIS §4.9, §5.1; gap_02 §2.3; GROUPS gap_01 §3) |
| 2 | **Non-anticipativity across model worlds** | Recourse at stage-1 and stage-2 nodes may depend only on observable history. Either impose y_n = y_{n′} for nodes with the same observable signature in different worlds, or build world-mixture nodes with world-tagged leaves for the per-class CVaR rows. Tail strata must be defined on information available at the node, with likelihood-ratio weights. Report the "model-learning optimism" gap between the pooled and world-separated trees (00_SYNTHESIS L11; PA A9) |
| 3 | **Pinned-dual guard on the T6 surrogate and Tier-1B rows** | Phase I-b as in PA §4.8.4; a glide path on CVaR rows; penalty-×10 invariance of the T6 dual; no card priced off an infeasible CVaR row (GROUPS gap_01 §6 item 5) |
| 4 | **Readiness-Red vs event-Red** | Event-Red comes only from T3 coverage, Treasury ÷ NAV, liquid share and LaR99 ÷ CBC_TP. A forward T4′ survival indicator alone triggers the Phase-II plan (pacing rule, revolver request, band request), never line draws, P2S, amber sales or hedge monetization (GROUPS gap_01 §1.3). The synthetic book starts in readiness-Red (17 months SH_TP; SYNTHETIC) |
| 5 | **Recovery semantics** | Separate the structural deficit u\* (Board and owner) from the execution deficit d₀ (glide path, group delivery shares φ_g, a quarterly progress test). Cap the KKT dual at the cheapest spare lever, not buffer carry. Show signposts such as the cap-binding θ (0.82) and revolver spare capacity (GROUPS gap_01 §2.2–2.3, §3) |
| 6 | **The owner's distribution stays exogenous** | Mode B contracts admit no payout variable: PB's `payout_topup` and PA's and PC's top-ups are compile errors under Mode B. Payout rules live only in the Mode A/H counterfactual that prices J\*_A − J\*_B and in proposals to the owner. The owner band is an owner/Board decision, modelled as Mode H, never an ADIC lever (brief §6; 00_SYNTHESIS §4.7, §4.9) |
| 7 | **Adopt GROUPS gap_02** | Version the census: v1.1 (PE unfunded $16.4bn) pending user confirmation, with v1.0 and the other histories as truth variants. Estimators must recover pace and unfunded by vintage under every variant. Use FBE-R (a Huber bias regression on [1, D, gap, flag] with slopes pooled across groups, and the optimizer's SELL flags and envelope status as covariates) as the production fusion. Freeze and hash gates G-A–G-E before the first scored release. Make the pay remedy (G-E) a precondition for granting forecast precision. Add the O3 performance module and the overlap graph with V24 (one EV draw per company across all claims; GP ≤ 5% computed on the graph) |
| 8 | **Adopt GROUPS gap_03 overlay accounting** | Three books with S/H/R/L; services booked to clients at FTP (the client bears exposure and liquidity, the Overlay bears execution and basis, CF bears funding); ex-ante tail credit with the IC policy residual; reconciled stress use (−$4.0bn instead of −$6.0bn; SYNTHETIC); the opportunistic default is SELL in Red; the tail budget and the opportunistic book are one decision through OV1/OV2 |
| 9 | **Fit the stack to the environment** | Gurobi `feasRelax` → highspy `feasibilityRelaxation` + `getIis` (both verified present). QuantLib/ORE references → in-house Black-76/Bachelier/SSVI with golden values, arbitrage checks and put–call parity. pycma/Optuna → in-house CMA-ES or scipy DE. SALib → in-house Saltelli/Morris, or a justified pure-Python addition. SDDP.jl → deferred. A licensed SIMM reconciliation → a production item. Any PyPI addition must be justified in writing |
| 10 | **Demote the NAV facility; condition revolver credit** | Keep the LP-portfolio NAV facility only as a capacity-capped column (≈ $2.1bn at 10% LTV, $1.1bn credited at the stressed 5%; ≈ 6× the revolver's cost per credited dollar; SYNTHETIC). Credit the revolver at 80% only from month 2, with covenant headroom under s\*, ≥ 10 banks, none above 12.5%, and a yearly test draw (GROUPS gap_01 §0 item 7; gap_02 §1.1) |
| 11 | **Performance acceptance on the real assembled model** | Re-benchmark in sprint 1 on the true row structure: 24 monthly T4′ rows, per-class CVaR rows, OV rows, LM and encumbrance. B1: P ≤ 60 s. B2: H ≤ 2 min including Phase I/II and selection re-solves. Duals after crossover. Fallbacks: the what-if tree size, then Benders overnight (PA §4.8.3; PD §4.11) |
| 12 | **H–P alignment** | H's objective is the PWL CRRA(3) plus L2 shortfall proxy of J, with λ^H_T tuned until H and P rank actions alike. A risk-neutral terminal objective (PC §4.11) is rejected. Kendall τ ≥ 0.8 on the top-30 candidates; otherwise flag the card and select on P (00_SYNTHESIS §4.8–4.9; PD §4.11) |
| 13 | **Liquidity-margin row on canonical conventions** | The blueprint row is admissible only with haircut HQLA, HF cash through φ(h,S), facilities at 0% in 30-day rows and canonical credit beyond, encumbered IM excluded, and CVaR₉₉ stressed VM. "Unused facility" at 100% is rejected (brief §6 graft 3; gap_02 §1.1) |
| 14 | **P(10%) never in any objective or fitness** | This covers agent "discovery" fitness and seat utilities. The gambling signatures (risk rising after losses outside the cushion channel; leverage at the cap while behind target) are Gate-1 failures (PB §4.11 item 4). Every probability leads with its model range and MC error (00_SYNTHESIS L9, §6.7) |

---

## 9. Notes for the chief architect

- **Data that decides the results** (all proposals agree; 00_SYNTHESIS §7.2): hedge-fund terms τ, PE unfunded by vintage (now doubly decisive, given census v1.1 against v1.0), the overlay blotter and CSAs, and the owner-draw convention. Until they arrive, every card stays labelled SYNTHETIC, and the IC pack should show census-variant sensitivity next to each liquidity metric.
- **The CRO's binding question is T6 in the M6 class.** Without the owner band, M6 breaches its 5% capacity band (5.2–5.8%), and the book is in recovery today (gap_02 §3; SYNTHETIC).
  - The architecture must make that visible on day one: SIGNED_IN_RECOVERY, u\*, the IIS, and infeasibility prices on the Treasurer's panel, never on cards.
  - That is only possible if M6 is inside H and the search plane (must-fix 1).
