# Tree demo: independent mathematical verification (SYNTHETIC)

> **SYNTHETIC.** This note checks `tree_demo.py`, `params.json` and `results.json` in this folder (results.json sha256 `18b39990c618d79d…`). Every number in them, and here, is illustrative, not ADIC data and not a forecast. The checks were run on 2026-10-19.

## Verdict

**The core is what the demo says it is.** One linear program over a 40-node scenario tree turns the inputs and limits in `params.json` into three outputs: a decision at every node, a price of liquidity at every node and the probability of every outcome. No step inside the solve is a judgement call.

I rebuilt the program from its written description with my own code and a different solver. The rebuild reproduces:

- the author's optimum, to a relative 8 × 10⁻¹⁰;
- every node's decisions;
- every published dual, each checked by re-solving with extra cash at that node;
- λ and the state prices;
- the CVaR row and the piecewise-linear (PWL) utility;
- the naive-rule comparison and the no-revolver case;
- Phase I, both MPC re-solves, the time-consistency test and the four calibration re-solves.

**I found no mathematical error.**

**One medium caveat (issue 1).** The headline "P(PE fire sale) = 0.0% against 23.2% for the naive rule" is partly an end-of-horizon effect. The t = 3 leaves impose only the cash floor. So in a third crisis year the 3-year plan sells liquid assets far below the IC range instead of selling PE. If the tree gets one more year, or the IC range's lower edge also holds at t = 3, the optimizer itself sells PE at the crisis discount with probability 2.4–10.5%. That is still far below the naive rule (31.5% on the same 4-year tree). The other eight notes are low severity: wording, reporting and robustness (§8).

## 1. What was checked, and how

| Task | Method | Result |
|---|---|---|
| 1. Re-solve the LP | My own model written from `params.json` and RESULTS.md §9 (depth-first tree keyed by path, every row a cvxpy expression, objective E[Û] unscaled). Solved with **CLARABEL** (interior point), and with cvxpy → HiGHS for vertex solutions. The author used highspy dual simplex on a hand-built sparse matrix. | Objective relative difference ≤ 8.4 × 10⁻¹⁰ in all four cases; decisions agree to ≤ $24k (vertex) |
| 2. Every row at every node | My own flow equations applied to (a) results.json as exported and (b) the author's unrounded values (scratch copy of the script) | (a) closes to the 8-significant-digit rounding; (b) cash balances close to 4.4 × 10⁻¹⁴ $bn, i.e. to the cent. All limits hold. |
| 3. Duals | Re-solve with ±$0.01bn and ±$0.0001bn of cash at **all 40** cash rows (5 of them also with CLARABEL). Separate re-solves for floor relief, carry, the CVaR floor, 8 binding limits and the pacing break-even. | Every reported value reproduced, relative error ≤ 1.1 × 10⁻⁷ (the export's rounding) |
| 4. CVaR, PWL, naive rule | CVaR by sorting, by Rockafellar–Uryasev and from the LP's own η and z; tangent algebra on a fine grid; naive rule re-coded from its description | Exact match |
| 5. No revolver, MPC | My own re-solves, including the max-CVaR capacity check and Phase I | Exact match |
| Beyond reproduction | Horizon test at H = 2, 3, 4; IC range enforced at t = 3; draw basis; recovery-mode alternatives; λ decomposition | §7 |

Determinism: re-running a scratch copy of `tree_demo.py` reproduces `results.json` and `RESULTS.md` byte for byte (sha256 `18B39990…` and `427FCA5E…`).

## 2. Independent re-solve: objective and decisions

My model has 387 variables and 616 constraints, the same size as the author's LP. Every row of RESULTS.md §9 was confirmed term by term, because a single wrong coefficient would have moved the optimum.

| Case | Author: E[Û] (highspy) | Mine, CLARABEL | Mine, HiGHS via cvxpy | Relative difference |
|---|---|---|---|---|
| Revolver signed, CVaR floor (main) | −0.353049874751 | −0.353049875025 | −0.353049874775 | 7.8e-10 / 6.8e-11 |
| No revolver, CVaR floor | −0.355598633926 | −0.355598634172 | −0.355598633929 | 6.9e-10 / 6.9e-12 |
| Revolver, no floor | −0.352856075614 | −0.352856075705 | – | 2.6e-10 |
| No revolver, no floor | −0.354215133970 | −0.354215134021 | – | 1.4e-10 |

- **Tangents:** my own two-pass placement (first pass on 0.60–1.70; second pass on 0.97 × min to 1.03 × max of the first solve's leaf wealth) reproduces the author's 10 tangent points to ≤ 1.3 × 10⁻⁹ relative in every case.
- **Decisions:** I compared 11 quantities at all 40 nodes (sell / buy liquid, sell PE, revolver, NAV loan, synthetic notional, pacing cut, closing C, L, P, U).
  - Revolver case: the largest difference is $2.4 × 10⁻⁵bn (D>D>D, HiGHS vertex), on a direction where the two objectives agree to 2 × 10⁻¹¹. With CLARABEL it is 8.5 × 10⁻⁴bn, at a leaf, which is interior-point tolerance.
  - No-revolver case: 5.0 × 10⁻⁷bn.

## 3. Every node: cash balances, owner draw, limits, probabilities, non-anticipativity

**Identities, recomputed with my own flow equations from the author's unrounded node values ($bn):**

| Identity | Max residual |
|---|---|
| opening cash = parent's closing cash + nine named flows (draw, distributions, calls, yield cash, interest, margin returned, variation margin, revolver interest and fees, NAV-loan interest) | 4.0e-15 |
| closing cash = opening cash + (1−τ)·sell − (1+τ)·buy + (1−disc)·PE sale + Δrevolver + ΔNAV loan − initial margin | 3.3e-14 (4.4e-14 without revolver) |
| liquid, PE NAV and unfunded roll-forwards | ≤ 1.4e-14 |
| owner draw = regime draw rate × parent's post-decision NAV | exact (relative 1e-17) |
| W̃ = terminal NAV − pacing charges + draws accrued at the static-allocation return | 2.8e-14 |
| W̃ recomputed vs the LP's W column | 8.5e-14 |

From the exported `results.json`, which is rounded to 8 significant digits, the same identities close only to the rounding: ≤ 8.7 × 10⁻⁷ for cash and ≤ 5.4 × 10⁻⁶ for W̃. Two apparent IC-range "violations" of 2 × 10⁻⁷ are that rounding on binding rows (unrounded slack −7 × 10⁻¹⁵).

**Owner draw is paid in full at every node.** The draw is a constant share of the opening NAV inside every child's cash equality. No variable can reduce it. After it is paid, cash is ≥ 0 and ≥ 4% of NAV at all 40 nodes (minimum slack −1.8 × 10⁻¹⁵).

**Limits at the 13 decision nodes, both consent scenarios, unrounded values:** every limit holds.

- The cash floor, revolver availability (D>C>C: 7.5 = 50% of 15), the IC range and the $5bn synthetic budget bind where RESULTS.md §2 says, and are never exceeded.
- NAV-loan LTV slack is ≥ $1.69bn with the revolver and binds at D>C>C without it.
- Exposure ≤ 1.30× has ≥ $27bn of slack.
- No node cuts pacing, and no node buys and sells liquid at once.
- Every stock and trade is ≥ 0.

**Probabilities:**

- Each stage sums to 1 (to 2 × 10⁻¹⁶).
- Each node's probability is its parent's times the branch probability (exact).
- Branch probabilities equal the rows of the transition matrix (exact).
- The 39 edges in results.json match the node flows exactly.

**Non-anticipativity holds by construction.** Both formulations carry exactly one decision vector per node. Each node's opening state is recomputed from its parent's closing state and its own year's rates alone (residual ≤ 4 × 10⁻¹⁵). So a decision can depend only on the path observed so far, and there are no scenario copies to tie together.

**Horizon nodes.** As documented, the t = 3 nodes impose only the cash floor. They do not impose the IC range, the LTV cap or revolver availability. Without the revolver, leaf D>C>C>C carries a NAV loan of 2.64 against a 5% crisis LTV cap of 2.52, i.e. $0.12bn above the cap. The consequences are in §7 and issue 1.

## 4. Duals, state prices and λ

**Conventions (checked).**

- HiGHS reports a row dual as ∂(objective)/∂(row bound) in the maximize sense.
- The LP objective is 1000 × E[Û], and the report divides by 1000.
- A ≥ row at its bound has a dual ≤ 0, which the author negates to get "value of relief".
- The cash-row dual μ is positive at every node (minimum 2.7 × 10⁻⁵ at D>N>C>N).

My re-solves measure the derivatives directly, so they do not depend on any sign convention.

**Cash-row duals, re-solved with ±$0.01bn of extra cash:**

| Node | p | μ reported (E[U] per $bn) | HiGHS re-solve, right = left | rel. err | CLARABEL re-solve, right / left | rel. err | State price m |
|---|---|---|---|---|---|---|---|
| D | 1.000 | 4.2545581e-3 | 4.2545581e-3 | 9e-10 | 4.254546e-3 / 4.254531e-3 | 3e-6 | 1.000 |
| D>C | 0.150 | 1.1567215e-3 | 1.1567215e-3 | 1e-8 | 1.156729e-3 / 1.156732e-3 | 7e-6 | 1.813 |
| D>N>D | 0.060 | 1.8382861e-4 | 1.8382861e-4 | 3e-8 | 1.838286e-4 / 1.838286e-4 | 2e-7 | 0.720 |
| D>C>C | 0.060 | 7.2530076e-4 | 7.2530076e-4 | 1e-8 | 7.253104e-4 / 7.253060e-4 | 7e-6 | 2.841 |
| D>C>C>C | 0.024 | 3.9671115e-4 | 3.9671115e-4 | 1e-8 | 3.967118e-4 / 3.967104e-4 | 2e-6 | 3.885 |

All 40 nodes (HiGHS): the largest relative error is 1.1 × 10⁻⁷ at ±$0.01bn and 9.5 × 10⁻⁸ at ±$0.0001bn. The right and left derivatives agree at every node, so no node sits at a kink within $10m. My own CLARABEL duals for these rows equal the reported values to 8 digits. State prices m = μₙ/(pₙ μ₀) are reproduced at all 40 nodes.

**λ normalization.** The definition is λₙ = Mₙ/(μₙ − Mₙ), where Mₙ = (1 − f) × (value of $1 of relief on node n's cash-floor row). I checked it three ways:

- (a) from my own duals;
- (b) from re-solves of the floor row and the cash row;
- (c) directly as (μ − carry)/carry, where carry is the value of $1 injected at n with the floor tightened by $(1 − f), i.e. a dollar that cannot relieve the floor.

| Node | λ reported | (a) my duals | (b) / (c) re-solves |
|---|---|---|---|
| D>N>D | 0.508% | 0.508% | 0.51% / 0.51% |
| D>D>N | 0.269% | 0.269% | 0.27% / 0.27% |
| D>D>D | 0.546% | 0.546% | 0.55% / 0.55% |
| D>D>C | 0.536% | 0.536% | 0.54% / 0.54% |
| D>C>N | 0.585% | 0.585% | 0.58% / 0.58% |
| D>C>D | 0.540% | 0.540% | 0.54% / 0.54% |
| D>C>C | 4.030% | 4.030% | 4.03% / 4.03% |
| the other 6 decision nodes | 0 | 0 | 0 / 0 |
| D>C>C, no revolver | 47.907% | – | 47.907% / 47.907% |

ARCHITECTURE.md §5.6's identity μₙ = (1 + r) Σ μ_child + Mₙ holds here to within ±2.1% (carry ÷ (1 + r)Σμ_child lies between 0.979 and 1.015). The residual comes from the NAV-linked draw and from the IC-range rows, which also contain cash through NAV.

**Other prices.**

- **CVaR row:** ∂E[Û]/∂F = −2.7214765 × 10⁻⁴ per $bn on both sides, i.e. **$0.0640 of today's cash per $1 of floor** (reported 0.063966137).
- **Binding limits, in ¢ per $1 of relief at the node** (re-solve vs reported):
  - IC range: D 0.501 vs 0.501; D>C 5.867 vs 5.867; D>C>C 7.736 vs 7.736.
  - Revolver cap at D>C>C: 3.498 vs 3.498.
  - Synthetic budget: D>C>C 3.035 vs 3.035; D>D>D 0.219 vs 0.219.
  - Cash floor: D>C>C 4.036 vs 4.036; D>N>D 0.526 vs 0.526.
- **Pacing break-even:** with the revolver the root's reported value is 0.547¢ per $. A cutting cost 0.02¢ below it makes the root cut $3.74bn; 0.02¢ above it makes the root cut nothing. Without the revolver the reported value is 4.487¢: 0.02¢ below cuts the full $5bn plan; 0.02¢ above cuts nothing.

## 5. CVaR, PWL utility and the naive rule

**CVaR.** The coded rows are the Rockafellar–Uryasev form for the lower tail of W̃:

- z_ℓ ≥ η − W̃_ℓ, z_ℓ ≥ 0, η − Σ p_ℓ z_ℓ / 0.10 ≥ F.

On the exported terminal distribution:

- CVaR₁₀% computed by sorting = Rockafellar–Uryasev = **157.08815 = F**, so the row binds.
- The 10% quantile falls inside the atom D>C>N>C (cumulative probability 0.0979 → 0.1016).
- In my LP, η = 173.103 = W̃(D>C>N>C), and z equals (η − W̃)⁺ exactly.
- Without the row the tail is −4.129% a year with the revolver and −4.260% without, as params.json states.

**PWL utility.**

- The 10 tangents run from 0.7428 to 1.4581 (geometric ratio 1.078).
- Slopes w⁻³ fall strictly, so the envelope is concave (largest second difference 9 × 10⁻¹⁶).
- On a 30,000-point grid over [0.5, 2] the envelope never lies below CRRA(3) (minimum gap +1 × 10⁻¹²) and touches it at every tangent point.
- Leaf wealth (0.766–1.416 × W₀) lies inside the tangent range.
- The largest error at the leaves is 2.497 × 10⁻³ and the level bias in certainty equivalent is $0.183bn, both as reported.
- With 48 tangents: CE 210.45733 against 210.45648, and the root decision moves by 8.6 × 10⁻⁸ $bn.

**Naive rule.** I re-coded it from its description in params.json and ran it on the same tree with the same flow equations. It reproduces every reported number:

- E[W̃] 216.41621, CE 208.88899, CVaR 152.76257, P(fire sale) 23.25%;
- PE sales at D>C 1.47, D>C>C 19.60, D>D>C 6.26 and D>C>D 1.81;
- decisions within 4 × 10⁻⁷, and 0 IC-range breaches.

The 4% variant also matches (CE 208.87808, CVaR 151.09664). It **breaches the IC range's upper edge** at D>N (38.0%, p = 0.30) and D>N>N (40.0%, p = 0.21) (issue 5).

The flows are the same except one item: the naive rule pays no revolver undrawn fee, while the optimizer with the revolver does. Charging the naive rule the fee lowers its CE by $0.079bn, so the reported +$1.57bn advantage is slightly conservative.

## 6. No-revolver case, Phase I, MPC re-solves, time consistency, calibration

| Claim | Reported | Re-solved here |
|---|---|---|
| No revolver: root PE sale; D>C>C PE sale + NAV loan; λ(D>C>C) | SELL 2.16; SELL 5.30 + 2.64; 47.9% | same (decisions within 5 × 10⁻⁷); 47.907% |
| Root PE sale without a revolver is caused by the CVaR floor | yes | yes: without the floor, P(any PE sale) = 6% (only D>C>C) |
| Value of the signed revolver | $0.75bn CE (13bp a year) | $0.755bn (12.7bp a year); $0.873bn on a 4-year tree |
| Phase I with revolver | u* = 0 | u* = 0 |
| Phase I without revolver | u* = 0.2468, short at D>C>C by $4.113bn | u* = 0.24680, D>C>C $4.1133bn |
| MPC from D>C: CVaR floor attainable? | no; best −6.86% a year; shortfall $11.6bn | infeasible with both solvers; max-CVaR 117.960 (−6.862% a year); shortfall $11.616bn |
| MPC from D>C: Phase I without PE sales | u* = 1.29, short at D>C>C>C $8.1bn | u* = 1.2925, D>C>C>C $8.078bn |
| MPC from D>C: recovery re-solve | SELL 1.20 liquid; CE 165.14; CVaR −7.89% a year | SELL 1.19891; CE 165.1396; CVaR −7.893% a year |
| MPC from D>D | SELL 4.63 liquid + SELL 3.49 PE | SELL 4.62594 + 3.49358 (within 2.5 × 10⁻⁷). Cause: the re-imposed floor (a 3-year window without the floor sells 4.48 liquid and no PE). |
| Time consistency without the CVaR row | max decision difference 2.5e-13 | 1.4e-14 (D>C), 2.2e-13 (D>D) |
| Calibration re-solves (4 variants) | e.g. a −3% floor sells $29.9bn PE at the root | all four reproduced to 7 digits (56.0 liquid; 35.553 PE; 47.6 and 67.29; 29.926 PE) |
| All 23 summary statistics, 4 cases | – | largest difference 4.8 × 10⁻⁶ |

## 7. Beyond reproduction: how robust are the headline numbers?

These tests change one modelling choice at a time. They are sensitivities, not corrections.

**Horizon test**, as ARCHITECTURE.md §5.2 asks for: same parameters, revolver signed, trees of 2, 3 and 4 years.

| Horizon | Root decision without floor | Root decision with the −3.9% a year floor | Optimizer P(PE fire sale) | Naive P(PE fire sale) |
|---|---|---|---|---|
| 2 years | BUY 4.10 liquid | SELL 10.76 liquid + **SELL 62.74 PE** | 0% | 15.0% |
| 3 years (the demo) | SELL 4.41 | SELL 8.21 | **0%** | 23.25% |
| 4 years (floor slack, CVaR −2.77% a year) | SELL 8.21 | SELL 8.21 | **6.49% by t = 3** (D>C>C>C $13.7bn, D>D>C>C $2.7bn, D>C>D>C $0.2bn) | 31.5% by t = 3 |

- **Why the 3-year plan shows 0%.** At t = 3 only the cash floor is imposed. 68% of leaves (by probability) sell liquid assets to restore it, up to $18.6bn. 13 of the 27 leaves (p = 25.6%) end with public-markets exposure below the 27% IC edge, the lowest being D>C>C>C at 10.4% of NAV. That leaf also ends with the revolver at its 50% crisis cap and cash at the floor. Nothing values the liquidity used up, because ψ = 0 and there is no terminal liquidity row.
- **Same model with the IC edge held at t = 3.** With the floor, P(fire sale) = 2.4%, and the root adds a $6.88bn PE sale at the drought discount (CE 208.76 against 210.46). Without the floor, P(fire sale) = 10.5%.
- **MPC from D>C shows the same effect.** Its recovery plan sells PE at the crisis discount with probability 21% inside its new window (results.json reports this; RESULTS.md does not).
- **The root decision is fairly robust; the contingent plans and the fire-sale statistic are not.**
  - SELL 8.21 recurs at H = 4. It sits exactly at the IC range's lower edge, a human-set limit.
  - It changes if the IC edge is held at t = 3, or if the horizon is 2 years.

**Recovery mode from D>C.** The author drops the Tier-1B row once it is unattainable. Keeping the row at the attainable level instead gives:

| Rule | Root decision | CE | CVaR (a year) | P(fire sale), new window |
|---|---|---|---|---|
| Drop the row (author) | SELL 1.20 liquid | 165.14 | −7.89% | 21.3% |
| CVaR ≥ best attainable − $0.01bn | SELL 2.51 liquid + **13.90 PE at 35% off** | 161.53 | −6.86% | 100% |
| CVaR ≥ best attainable − $1bn | SELL 1.69 + 5.18 PE | 163.97 | −7.13% | 100% |

Keeping the row costs up to $3.6bn of CE and forces a crisis fire sale today, to gain at most 1.0pp a year of tail. The author's rule is defensible, but it is a policy choice (issue 3).

**The draw basis is immaterial.** Basing the owner's draw on the parent's pre-decision NAV instead of its post-decision NAV moves decisions by at most $2.7m (D>D) and λ(D>C>C) by 5 × 10⁻⁶.

**What λ actually measures at revolver-funded nodes.** There λ is 0.51–0.58%, not "about" the 0.85% drawn spread. Approximately:

- λ ≈ (1 − f)/(1 + r) × (0.85% drawn spread − 0.15% undrawn fee a drawn dollar saves − the t = 3 settlement cost of carrying less cash, about 0.14% where the leaf floors bind).

The node-by-node variation follows the share of children that settle at t = 3. Setting the undrawn fee to zero raises λ by exactly 0.139pp at D>D>D and D>C>N (where the revolver stays marginal), which is (1 − f)/(1 + r) × 0.15%. At D>C>C the same formula with the 4.4% NAV-loan spread gives 4.07% against 4.03%.

## 8. Issues

| # | Severity | Issue | Fix |
|---|---|---|---|
| 1 | medium | **End-of-horizon effect behind the 0% fire-sale headline.** t = 3 leaves impose only the cash floor. 13 of 27 leaves (p = 25.6%) end below the 27% IC edge after settlement sales of up to $18.6bn. Crisis paths end with the revolver at its cap. Without the revolver, D>C>C>C ends $0.12bn above the 5% LTV cap. ψ = 0. So "P(PE fire sale) = 0.0%" and the 23.2pp gap to the naive rule are horizon results: with H = 4 they become 6.5% vs 31.5%; with the IC edge held at t = 3, 2.4% (and a $6.9bn root PE sale) or 10.5% without the floor. | Impose the IC range, LTV and availability at t = 3, or add a terminal liquidity row or terminal values (ω, ψ). Report the horizon-invariance test (§5.2) next to the headline and caveat it in RESULTS.md. |
| 2 | low | λ reading in RESULTS.md §2: "about the spread of the loan (0.85% revolver)". Computed λ at revolver-funded nodes is 0.51–0.58%. The gap comes mostly from the 0.15% undrawn fee saved and the ~0.14% t = 3 settlement cost, not the NAV-linked draw (the draw basis changes λ by < 0.001pp). For the PE sale it is 47.9% against d/(1−d) = 54%. | State λ ≈ (1−f)/(1+r) × net cost of the marginal source, and give the revolver's net cost (≈0.56%). |
| 3 | low | Recovery mode (MPC from D>C) drops the Tier-1B row entirely. The re-solved tail (−7.89% a year) is 1pp a year worse than attainable (−6.86%). The plan still sells PE at the crisis discount with probability 21% in the new window. The capacity check includes PE sales, whereas §5.5 defines Phase I over reversible levers only. The rule is hard-coded, not in params.json. | Show the §7 trade-off table in RESULTS.md. Make the recovery rule a parameter (drop / glide path). Reword "does not fire-sell PE" to note the contingent sales. |
| 4 | low | The headline root decision (SELL 8.21) is a corner of two human-set, tuned limits: the IC lower edge, and a −3.9% CVaR floor set just above the unconstrained −4.13%. The same floor forces a $62.7bn root PE sale at H = 2 and is slack at H = 4. All of this is disclosed, but "nothing inside the solve is a judgement call" invites the reading that the decision is limit-free. | Add a small table of how the root decision moves with the floor level, the IC range and the horizon. |
| 5 | low | RESULTS.md §3 shows "Naive rule at the 4% floor" without saying it breaches the IC range (D>N 38.0%, D>N>N 40.0%; results.json lists both). results.json's `limit_breaches.note` says the naive rule "only respects the cash floor", which contradicts RESULTS.md and params.json ("inside the IC range"). The naive rule pays no undrawn fee; including it would raise the optimizer's lead to $1.65bn. | Footnote the column, align the note, and mention the fee asymmetry. |
| 6 | low | The check "reduced cost on every cash column 2.9e-18, so μ = carry + M holds exactly" is circular. Simplex zeroes the reduced cost of basic columns, and "carry" is defined as μ − M, so the check cannot catch a wrong λ. | Replace it with the direct carry re-solve used here (inject δ, tighten the floor by (1−f)δ). It reproduces λ to 1e-8. |
| 7 | low | results.json rounds every value to 8 significant digits, so the published cash balances re-add only to ~$1–5k; the to-the-cent check needs the unrounded run. Minor: RESULTS.md prints the floor's cost as "1bp a year" for 0.57bp. | Export flows to an absolute precision (e.g. 1e-9 $bn) or add per-node residuals. Print one decimal in bp. |
| 8 | low | params.json says "nothing is hard-coded in the script except solver settings and report formatting". Yet these are hard-coded: the tangent re-placement margins (0.97 / 1.03); the $5m action threshold, which drives every P(...) statistic; the binding tolerance; and the recovery rule. | Move them into params.json. |
| 9 | low | LEVER / P2S labels read the post-decision synthetic notional X (a stock) as the node's trade. Harmless here, because no node inherits X > 0 from its parent (checked), but a carried position would be re-labelled as a new LEVER. | Label the change in X relative to the parent. |

## 9. Reproducing this check

The scripts are in the session scratchpad: `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\verify\`. They run with `.venv\Scripts\python.exe` and read `params.json` and `results.json` from this folder.

| Script | What it does |
|---|---|
| `indep.py` | The independent model (tree, rows, CLARABEL / HiGHS solve, two-pass tangents) |
| `step1_solve.py` | Objectives, tangents and decisions |
| `step2_constraints.py` | Every identity and limit at every node |
| `step3_duals.py` | Duals, λ, state prices, CVaR and binding-limit prices by re-solving |
| `step4_cvar_pwl_naive.py` | CVaR, PWL, the 48-tangent test, the naive rule and the pacing break-even |
| `step5_mpc_phase1.py` | Phase I, MPC, time consistency and calibration |
| `step6_extra.py` – `step10_lambda_decomp.py` | Summary statistics, recovery alternatives, draw basis, horizon test, IC edge at t = 3, λ decomposition |
| `author_obj.py` | Runs the author's code, in a scratch copy only, to read its full-precision objectives as comparison targets |
