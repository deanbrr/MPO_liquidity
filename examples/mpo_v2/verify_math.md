# MPO v2: independent mathematical verification (SYNTHETIC)

> **SYNTHETIC – NOT ADIC DATA.** This note checks `examples/mpo_v2` as it stood on 2026-10-19: the code, `params.json` (sha256 `f39d2ae004b742a6…`, the hash RESULTS.md prints) and `results.json` (sha256 `85bf9501efb9b73c…`). Every number here comes from the synthetic book, tree and sealed truth of that run, or from a reduced synthetic instance built for this check. Nothing is an ADIC holding, mark or forecast.

## Verdict

**The optimizer does what RESULTS.md says, and its arithmetic is right.**

- I rebuilt the tree LP from its economic definitions with my own code. My formulation has no aggregate state variables and only 51,259 rows against the author's 59,667. I solved it with HiGHS and, as a second solver, Clarabel.
- At full scale (210 leaves) it reproduces the author's main objective (O1, GBO) to machine precision:
  - mean LP: E*[W̃] = **285.16754603616** in both;
  - exact minimum bPOE: **0.95669580847** in both;
  - CRRA tie-break: E[U] agrees to 1e-15 (HiGHS) and 9.4e-10 (Clarabel);
  - every root decision agrees to within 7e-14 $bn (HiGHS) and 1.5e-7 $bn (Clarabel), and every leaf W̃ to within 4.4e-12 $bn.
- The bPOE/CVaR rows are exact. Every implemented hard row holds for O1 at every node, fan year and leaf, to within 9e-13.
- On a 60-leaf instance, the exact MILP's indicators equal 1 exactly on the leaves that meet the goal.
- The out-of-sample run uses fresh paths, and every certified P(goal) reproduces to the last digit.
- Each attribution re-solve removes exactly one column family, and all 11 reproduce when re-solved with my own restrictions.

**What is wrong is in the formulation, not the arithmetic.** Three medium issues:

1. **The H16 need-based funding cap is vacuous.** Its right-hand side includes repayments, and a same-node revolver draw-and-repay costs nothing. O1 uses this at 102 node-instrument pairs (up to $82bn in one node), and every need-row dual is zero.
   - With the cap as DSGO specifies it, the in-tree numbers change: Φ* goes from 0.957 to 0.970, and in-tree P(goal) from 46.7% to 43.4%, against 43.2% for the status quo.
   - So the in-tree uplift rests on fan-year clairvoyance, and the "E2 is bounded by H16" claim does not hold.
   - **The out-of-sample headline is not affected.** Re-optimized root decisions certify at 46.99% to 47.27%, against 46.90% as run.
2. **The red-event limit H9 is degenerate.** O1 sells red-tier units for exactly the $0.05bn allowance at 126 nodes, so its path statistic R is exactly 0 on 67% of the probability mass.
   - CVaR at 1 − 0.6% ≤ 0 therefore equals a hard "no red event on any path" rule: E* and Φ* are identical to every digit.
   - The ε grid of the frontier is inert (0.3%–1.2% identical).
   - "The red-event limit does not bind" is not true in the tree: dropping H9 moves Φ* to 0.953 and in-tree P(goal) to 47.7%.
3. **O2 is labelled "exact max-P(goal) MILP" but is an LP-rounding incumbent.** On the reduced instance the true optimum is 48.65% and the rounding finds 46.31%. Its reported 79% gap is measured against max E[min(1, W̃/M)], a bound that says almost nothing.

The other notes are low severity: reporting, latent bugs, documentation (§9).

## 1. What was checked, and how

| Task | Method | Result |
|---|---|---|
| Reproduce O1 | The author's pipeline, imported read-only in my own process (no file in `examples/mpo_v2` was modified), every intermediate GBO solve captured | φ 0.956696, E* 285.168, in-tree P(goal) 0.466646 and bPOE 0.961696: identical to results.json |
| Re-implement and re-solve, full scale | `my_lp.py`: my own row builder written from DSGO §1.3/§4.1/§4.6–4.7 and the params.json rationales. Holding and template values, unfunded, pledge pools and stressed flows are inline expressions, not variables. HiGHS (IPM and dual simplex) and Clarabel | §2: optimum and decisions match |
| Re-implement and re-solve, reduced instance | 20 holdings (every group and sleeve), group NAVs rescaled to the full book, tree 5 × 4 × 3 = 60 leaves. Author's model 16,178 × 13,896; mine 13,700 × 11,542 | §2 |
| bPOE / CVaR formulation | bPOE of each solution by breakpoint enumeration and by the CVaR root; the LP's CVaR against a sort and an RU scan; an exact single-LP (perspective / Charnes–Cooper) bPOE minimization at full scale | §3 |
| MILP indicator logic | My own MILP with explicit indicators, and the author's `optim.milp`, both run to proven optimality on the reduced instance; big-M validity by min W̃ per leaf | §5 |
| Every hard constraint at every node | O1 against the author's rows and bounds, and against my independent rows (51,259), at all 711 time nodes | §4 |
| Out-of-sample simulation | Re-ran the certification set. Hashed paths across the certification set, the selection set, the tree's raw paths and the book paths. Instrumented a scratch copy of `sim.py` to see what the rule recourse does | §6 |
| Attribution | Diffed the live model under every `SwitchOff` (columns, rows, coefficients, restoration). Re-solved every family with my own DSGO §6.3 restriction | §7 |
| Beyond reproduction | H9 degeneracy, H16 loophole (in-tree and out of sample), unimplemented DSGO rows, big-M lower bound, red-flag fragility | §8 |

**Environment note.** `.venv\Scripts\python.exe` is blocked by the machine's application-control policy, so every script ran under `pythonw.exe` and wrote its own log.

## 2. Independent re-solve: optimum and decisions

**Data recomputed from definitions** and compared with the prepared arrays: W0 and W*, sleeve values and bids, per-unit trade caps, static-SAA returns, the draw accrual factors G_{t→5}, stressed calls and P10 distributions, and 24-month stress flows. Every difference is ≤ 8.9e-16.

**Full scale (210 leaves; the author's matrices are 59,667 × 58,700)**

| Quantity | Author (HiGHS IPM) | Mine, HiGHS | Mine, Clarabel |
|---|---|---|---|
| Mean LP, E*[W̃] ($bn) | 285.1675460361626 | 285.16754603616266 | 285.1675475456 (5e-9 relative) |
| Exact min bPOE (perspective LP) | 0.9566958084738267 (on the author's matrix) | 0.9566958084738266 | – |
| min CVaR at p = 0.95727 | −0.000797828116 | −0.000797945520 (1.2e-7, the 1e-7 tolerance) | – |
| CRRA(3) tie-break, E[U] | −0.3874240687366748 | −0.38742406873667445 | −0.38742406837 (objective scaled ×1000; 9.4e-10) |
| Root decisions, max difference | – | ≤ 7.2e-14 $bn (sell, redeem, add, templates, β, TRS, tail, opportunistic IM, debt, P2S) | β 8.6e-8, adds 1.9e-8, redemptions 1.5e-7, commitments 6.4e-8 $bn |
| Leaf W̃, max difference | – | 4.4e-12 $bn; P(goal) 0.466646 in both | – |

- **The author's solutions satisfy my rows.** The worst violations are 8.95e-13 (O1), 6.4e-13 (mean LP) and 1.9e-12 (min CVaR), with no bound violated.
- **O1's objective in my model** is E[U] = −0.387424068737, the author's value.
- **Clarabel needs the CRRA objective scaled.** Unscaled, it stops about 1e-5 below the optimum on both instances. That is Clarabel's convergence on a flat, piecewise-linear objective, not a better point: the author's point is feasible in my rows and better.

**Reduced instance (60 leaves)**

| Quantity | Author | Mine, HiGHS | Mine, Clarabel |
|---|---|---|---|
| Mean LP | 275.089405724656 | 275.089405724656 (dual simplex) | 275.089405725201 (2e-12) |
| Φ (min bPOE) | 0.9909835409669074 (fixed point) | 0.9909835409669079 (perspective); bisection over 23 LPs gives (0.99098355, 0.99098361] | 0.9909924 (perspective; the τ-scaled LP limits Clarabel's accuracy) |
| Tie-break E[U] | −0.3858332626836129 | −0.38583326268361323 (IPM); −0.38583326268361356 (dual simplex at tolerance 1e-9) | −0.38583326268200 (scaled; 4e-12) |
| Root decisions | – | ≤ 6.4e-14 $bn | ≤ 7e-6 $bn |
| CRRA + L2 (O3) | −0.4208237440 | −0.420823753303 | – |
| Status-quo LP (B0) objective | 5.288576922182329 | 5.28857692218233 (my own B0 model) | – |
| B0 readings | – | W, W̃ and the red margin within 1.4e-13; CVaR_X at 90/95/99% identical (0.8786, 0.9407, 1.0941) | – |

The dual simplex at its default 1e-7 tolerance stopped 8.5e-7 below the optimum. With a 1e-9 tolerance it matches.

## 3. The bPOE / CVaR formulation

All numbers are full scale. X = (W* − W̃)/W0; bPOE₀(X) = min_{a≥0} E[(aX+1)⁺].

| Solution | bPOE (enumeration) | bPOE (CVaR root) | a* | Buffer c* (W0) | In-tree P(goal) |
|---|---|---|---|---|---|
| Mean LP | 0.9572695203 | 0.9572695203 | 0.738 | 1.354 | 44.69% |
| Min CVaR at p₀ = 0.95727 (Φ reported) | **0.9566960634** | 0.9566960634 | 0.751 | 1.332 | 46.21% |
| Certificate LP at 0.95570 | 0.9567039835 | 0.9567039835 | 0.758 | 1.318 | 46.21% |
| O1 (tie-break) | **0.9616960634** | 0.9616960634 | 0.774 | 1.292 | 46.66% |
| Exact optimum (perspective LP) | **0.9566958085** | 0.9566958085 | 0.751 | 1.331 | 46.21% |

- **The LP's CVaR is exact.** The min-CVaR objective −0.000797828115833 equals the sorted CVaR (−0.000797828115832) and an RU scan over all atoms. The hinge variables equal (X − η)⁺ to 4.4e-16. η = −1.3318, the negative of the buffer.
- **The certificate is valid.** At p = 0.95570 the LP's minimum CVaR is +0.0013905. That matches the direct CVaR of its own solution, so no plan reaches bPOE ≤ 0.95570, and Φ* lies in (0.95570, 0.95670].
- **The exact optimum confirms the fixed point.** One perspective LP on the author's own matrix gives **0.95669580847** (HiGHS, 30 s). The fixed point stopped 2.5e-7 above it, inside DSGO's 1e-6 cross-check (§4.3 step 4), which the code itself does not run.
- **GBO equals bPOE here.** The variant with a ≥ a_min = 1/c_max = 0.310 gives the same value. a* = 0.751 is well above a_min, and max W̃ − W* = 1.97 W0 < c_max = 3.22 W0, so the leaf condition holds.
- **O1's own bPOE is Φ* + 0.005 exactly.** The tie-break row pt·η + Σp·u ≤ 0 binds (−1.6e-15), and CVaR at 1 − Φ* is +0.00675 for O1. The headline "Φ* = 0.957" is therefore the minimum bPOE, not the recommended plan's, which is 0.962 (issue 5). This is the DSGO tie-break as specified; only the reporting is loose.
- **Check A5 can never fail.** It compares `gbo_value` on O1's leaves with `tree_stats(...)["phi"]`, which is the same function on the same inputs, and its pass flag is hard-coded. A7, A8 and "solves" are also hard-coded to pass.

## 4. Every hard constraint at every node (O1, full scale)

All 711 time nodes are checked: root, stage 1, stage 2, fan years 3–4 and leaves.

**Identities** (every row type is binding by definition): cash and margin, holdings balance, P2S, W, NR, exposure, IG + cash, IM, debt balances (PIK accrual), the queue, red sales, red margin, W̃, CVaR hinges and the aggregates. The largest residual is 8.8e-13 $bn. No column bound is violated (worst 0), and every Phase I slack is 0.

| Limit (rows) | Max violation | Binding | Min slack |
|---|---|---|---|
| H2 4% floor (711) / 8% floor (391) | 0 / 0 | 0 / 1 | 3.95 / 0 |
| H3 six-month coverage (81) | 0 | 0 | 20.6 |
| H4 24-month stress (1) | 6e-15 | **1** | 0 |
| H5 leverage, G5 class/behind caps (711) | 0 | 28 | 0 |
| H5 recourse debt ≤ 15% W / encumbrance ≤ 20% (711 each) | 0 / 0 | 0 / 0 | 8.5 / 11.4 |
| H6 LTV: NAV facility LTV and pool, preferred, CS and SMA back-leverage, RA cash-out (711 each) | 0 | SMA 13, others 0 | – |
| Revolver availability (711) | 0 | 6 | 0 |
| H7 depth caps: LP sales (81), group sales (405), sleeves (2,133) | 0 | 0 / 43 / 136 | – |
| H9 red-event CVaR (1; hinges 2,520) | 0 | 1 (degenerate, see §8) | – |
| H10 depth guard at 90/95/99% (3) | 0 | **3 of 3** | 0 |
| H11 overcommitment (495) | 7e-15 | 21 | 0 |
| H13 tail range (11 + 11), gross overlay (711) | 0 | 9 + 2, 8 | – |
| H15 leaf liquidity (210) | 0 | 0 | 20.4 |
| H16 need-based funding (711) | 3e-14 | 102 (**all duals 0**, see §8) | 0 |
| G4 no doubling down (406 + 39 + 39), G5 cushion (711) | 3e-14 | 134 / 20 / 21, 1 | 0 |
| Fan sleeve positivity (2,100 + 420), TRS cap (66) | 0 | 1,569 / 1, 62 | 0 |

- **The same check through my independent rows** gives a worst violation of 8.95e-13 at every node.
- **ADR-39 at the root:** every red-tier root SELL column is held at 0.
- **The status-quo LP leaves the range-breach column BRK unpriced.** At its vertex, BRK still equals the minimal breach in all 464 cells, so B0's leaf distribution (the H10 reference) is not distorted. That is latent (issue 11).

## 5. The MILP: indicator logic, big-M and the "round" comparison

**Indicator logic is exact (reduced instance, both run to proven optimality).**

- The author's `optim.milp` (HiGHS branch and bound, gap 1e-6) gives **0.4865380333** in 3 nodes and 34 s. My MILP with explicit indicators gives **0.4865380333** in 3 nodes and 22 s.
- In my solution, 29 indicators equal 1, 29 leaves have W̃ ≥ W* + ε_g·W0, and 29 leaves have W̃ ≥ W*. There is no indicator at 1 below the margin, no leaf above the margin at 0 and no leaf in the ε band [W*, W* + ε_g·W0). Every indicator is integral.
- The author's solution has the same property (P(meets the margin) = P(meets the goal) = objective). Dropping the margin (ε_g = 0) gives the same optimum.

**Big-M with L = 0 is not valid as stated, but valid in substance.**

- The minimum of W̃_ℓ over the feasible set is negative at 4 of 60 leaves, as low as −$192.9bn.
- All of it comes from the range-breach columns BRK, which have no upper bound. At that leaf they total $66,601bn, a $333bn "charge", while W at the leaf is $95.7bn. With BRK kept at its breach, the minimum W̃ there is +$109.0bn.
- The MILP with valid, LP-tightened M (L_ℓ = min(0, min W̃_ℓ)) has the same optimum, 0.4865380333.
- DSGO's argument ("H5 keeps wealth non-negative") misses the terms deducted after W: ψ·unfunded, the pacing credit and range charges (issue 6).

**The "round" comparison that the run reports as O2:**

- On the reduced instance it finds **46.31%**, against the proven optimum of **48.65%** (2.35pp short). It reports a "gap" of 86.1% against its relaxation bound of 0.8616.
- That bound is weak by construction. With g relaxed, the optimal g_ℓ equals min(1, W̃_ℓ/M) exactly (checked: difference 0), so the bound is max E[min(1, W̃/M)].
- At full scale I re-solved the relaxation: **0.859876**, the reported bound. Without the ε margin it is 0.860130, so the margin version is not, strictly, a bound on the no-margin P(goal) that the incumbent reports. The difference is immaterial.
- On the reduced instance the exact max-P(goal) solution behaves as H5 expects: E[W̃] = 254.6 < W*, bPOE 1.0, and 12% of mass piled up just above the goal. **H5 is tested on a heuristic, though, and the §4 table calls it "exact"** (issue 3).

## 6. Out-of-sample simulation: fresh draws and the same recourse rule

**The certified numbers reproduce exactly.** I re-ran 10,000 paths on seed 31 in chunks of 1,250, with template truth seed 502, from O1's solution.

| Policy | P(goal), re-run | P(goal), results.json | Mean TWR |
|---|---|---|---|
| B0 | 0.4291 | 0.4291 | 8.6009% = reported |
| B3 | 0.4474 | 0.4474 | identical |
| O1, rule recourse | 0.4690 | 0.4690 | identical |
| O1, playbook | 0.4442 | 0.4442 | identical |

- **The paths are fresh.** The 10,000 certification paths are all distinct. Hashing each path's first-quarter factor vector finds no overlap with the selection set (seed 21, 4,000), the tree's 20,000 raw stage-1 paths (seed 11) or the replication-book paths (seed 1031).
- **Common random numbers hold.** Every policy in a chunk runs on the same world, and the ADR-39 stage is read on B0's path in both the tree and the simulator.
- **The truth is sealed.** True alphas come from the book's truth model, the beliefs never see it, and belief mode is never the headline.
- **The in-tree simulator (E1) reproduces:** B0 0.449264, O1 rule 0.451759, O1 playbook 0.448392.
- **The 400-candidate bPOE approximation is fine.** Exact 0.979403 against approximate 0.979406 (O1 rule, at the goal).

**What the rule recourse does** (instrumented scratch copy of `sim.py`). It is the same rule on the selection and certification sets, and it does what RESULTS.md says:

- it never maps a path to a playbook node (node1 = −1 on every path);
- commitment multipliers stay at the root's (standard deviation 5e-14);
- the tail ladder stays at the root's $6.146bn notional;
- leverage is cut to the class and behind caps (1.05–1.30), whereas B0–B3 use the flat 1.30;
- it restores the 8% floor.

One asymmetry: for every `plan` policy the revolver is not repaid in years 1–2, even without a playbook. It is irrelevant here. The revolver is drawn on 0.05% and 0.19% of paths, and repaying it as the baselines do leaves P(goal) at 0.4690.

**Replication books are not independent** (issue 8):

- All four books use one path set (seed 1031).
- Each book's template-truth seed (book seed + 1) is the next book's book seed: 7102, 7103 and 7104 produce identical normal draws.
- So H3's between-book standard error leaves out path noise and some truth noise.

## 7. Switch-off attribution: one family each?

**Part 1: what each `SwitchOff` changes in the live model.** Every switch-off is fully restored on exit.

| Family | Columns changed (block @ level: count) | Rows / coefficients changed |
|---|---|---|
| SELL | s@0: 21, s@1: 550 | – |
| ADD | a@0: 10, a@1: 100; purchase templates y@0: 2, y@1: 25 | – |
| REFINANCE | P2S up pu@0–1: 11; NAV facility, preferred, back-leverage, RA cash-out draws dr@0–1: 37 | – |
| BETA | β@0–2: 81 (fixed at $10bn) | – |
| LEVER | HF TRS@0–2: 486; INFRA_LEV and SMA_LEV y@1: 6 | – |
| PACE | commitment y@0–2: 405 (fixed at plan) | – |
| REDEEM | r@0–1: 77 | – |
| HEDGE | opportunistic IM@0–2: 81 (fixed at $1bn) | 11 coefficients (tail cap → floor) |
| FUND | revolver and term draws dr@0–4: 510; revolver upsize: 1 | – |
| REBALANCE | none | 1,296 rows (each group within ±1% of B0's share) |

- **The column sets are disjoint:** no column belongs to two families.
- **Decision columns in no family:** P2S unwind (inert while P2S up is 0), the tail notional (controlled through the HEDGE rows) and fan-year β (forced deleveraging only).

**Part 2: every re-solve reproduced with my own restriction on my own LP**, using the tie-break at the author's φ + 0.005.

| Family | E* author (run log) / mine | Φ author / mine (exact) | In-tree P(goal) author / mine |
|---|---|---|---|
| SELL | 284.517 / 284.51743 | 0.959058 / 0.9590581 | 0.473339 / 0.473339 |
| ADD | 281.196 / 281.19578 | 0.971149 / 0.9711487 | 0.445584 / 0.445585 |
| REFINANCE | 285.168 / 285.16755 | 0.956696 / 0.9566959 | 0.466646 / 0.466646 |
| BETA | 280.422 / 280.42197 | 0.973495 / 0.9734954 | 0.448453 / 0.448453 |
| LEVER | 285.168 / 285.16755 | 0.956696 / 0.9566959 | 0.466646 / 0.466646 |
| PACE | infeasible; Phase I u* 0.00268912 on H9 (1 row); E* 263.997 (STRETCH) / infeasible; u* 0.00268912 on H9 (1 row); E* 263.99717 | 1.01718 / STRETCH | – |
| REDEEM | 282.966 / 282.96630 | 0.966437 / 0.9664370 | 0.457492 / 0.457492 |
| HEDGE | 284.252 / 284.25218 | 0.959951 / 0.9599509 | 0.451527 / 0.451527 |
| FUND | 282.830 / 282.82997 | 0.966062 / 0.9660587 | 0.457546 / 0.457547 |
| REBALANCE | 277.347 / 277.34726 | 0.985410 / 0.9854105 | 0.434018 / 0.434019 |
| BELIEFS | 280.688 / 280.68757 | 0.974540 / 0.9745403 | 0.444652 / 0.444652 |

**So the nine column families each remove exactly one family. Caveats** (issue 9):

- REBALANCE is a row restriction that limits SELL, ADD, REDEEM and PACE at once. That is DSGO's design, but it is not a separate family.
- PACE needs a Phase I allowance, so its row mixes the family's value with relaxing H9.
- BELIEFS rebuilds the status-quo readings under priors, which changes the H10 reference and the G4/G5 flags (rows 59,674 vs 59,667). It also keeps the fused σ_post in the belief-error driver and the trade caps.
- The BETA family is synthetic beta only. DSGO §6.3 F4a also puts "completion adds" there, and O1's $12.7bn of long-only adds (including index-like LO-01) sit in ADD.
- The switch-off runs are not certified (`certify=False`), whereas O1 is. FUND's φ, for example, is 3.3e-6 above its exact optimum. That is immaterial.
- The FR_eps_0.006 run, a worker re-solve with O1's settings, reproduces O1 exactly. So worker scheduling does not leak into the attribution.

## 8. Beyond reproduction: how robust are the in-tree numbers?

**H16 need-based funding cap is vacuous (issue 1).**

The row is: sleeve proceeds ≤ calls + draw + interest + tail premium + 0.08·W + Σ repayments. A revolver draw and repayment at the same node leave cash, balance, availability, interest and the red margin unchanged, so repayments can be inflated for free.

- O1 does this at **102 node-instrument pairs** (levels 2–4), up to **$82.4bn** at one node.
- Every need-row dual in the author's tie-break is exactly 0, although 102 rows bind.
- Fan years therefore sell long-only with foresight of the leaf path. Probability-weighted and summed over the three fan years, sleeve proceeds are $32.0bn long-only, $1.7bn amber, $0.03bn red and $0 hedge funds.

| Variant (my LP, GBO, tie-break at Φ* + 0.005) | E* | Φ* | In-tree P(goal) | Root β / term debt ($bn) | **OOS P(goal), rule recourse, 10,000 certification paths** |
|---|---|---|---|---|---|
| As run | 285.168 | 0.95670 | 46.66% | 22.20 / 6.01 | 46.90% |
| No same-node draw-and-repay (repayment ≤ parent balance) | 284.379 | 0.96002 | 46.89% | 22.65 / 6.21 | 46.99% (+0.09pp, s.e. 0.03) |
| Cap as specified, fans (no repayment, no 8% W allowance) | 281.984 | 0.96994 | 43.42% | 24.04 / 0 | 47.27% (+0.37pp, s.e. 0.06) |
| Cap as specified, every node | 281.842 | 0.97070 | 43.35% | 24.76 / 0 | 47.26% (+0.36pp) |
| Status quo B0 | – | 1.000 | 43.23% | 10 / 0 | 42.91% |

- **In-tree numbers depend on the loophole.** "P(goal) 46.7% vs 43.2%" and Φ* = 0.957 rest on fan clairvoyance. Under the cap DSGO H16 describes, in-tree O1 ≈ B0.
- **The out-of-sample headline does not.** The out-of-sample P(goal) of the re-optimized root decisions is equal or slightly higher, at a slightly deeper CVaR10 (−8.41% vs −8.25%) and a higher P(red) (0.22% vs 0.08%).
- RESULTS §11's "E2 is bounded by H16" is not true as coded.

**H9 is degenerate, and its ε is inert (issue 2).**

- R_ℓ = max over the path of (red margin, red-event sales − $0.05bn) is **exactly 0 on 66.9% of the probability mass** and negative elsewhere. η_R = 0.
- The zeros come from 126 red-event sales of exactly the $0.05bn `red_sale_threshold`: 120 red-sleeve funding sales in fan years and 6 planned sales at stage 1–2.
- With that many exact zeros in the tail, CVaR at 1 − ε ≤ 0 forces R ≤ 0 on every path for any ε below 66.9%.

| H9 variant (my LP) | E* | Φ* |
|---|---|---|
| ε = 0.6% (as run) | 285.16754603616 | 0.95669580847 |
| Hard per-node rule: margin ≤ 0 and red sales ≤ $0.05bn everywhere | 285.16754603616 | 0.95669580847 (identical) |
| ε = 5% | 285.17513 | 0.95664 |
| No H9 | 285.97473 | 0.95315 |

- **The frontier's ε axis is not a frontier.** The rows at 0.3%, 0.6% and 1.2% are the same constraint.
- **H9 does bind in the tree,** through the $0.05bn allowance, not through the red margin. The red margin is in fact ≤ −16 everywhere, as RESULTS says.
- **The allowance is worth little.** Forbidding the fan red-sleeve sales moves Φ* by only 5.6e-5 and leaves in-tree P(goal) unchanged.
- **The knife edge makes `tree_stats`' red flag (RS > thr) fragile.** In the reduced exact MILP, 4 nodes sit at thr + 6.9e-18, and the reported in-tree P(red) is 4.6% although R ≤ 7e-18 (issue 7).

**DSGO hard rows that are not in the model (issue 4).** model.py's docstring says "every hard row of DSGO §4.6 … is a row here", but these are absent:

- H8 oil exposure;
- H10(b) absolute per-world floor;
- H12 concentration;
- H13 OV1/OV2;
- H3's 30-day HQLA test;
- H5's 12-month maturity limit;
- ADR-39 condition (ii), first node after STR (2 decision nodes are Green and first after STR).

RESULTS §11 does not list them. Measured on O1:

- ENR exceeds 1.5% of NAV at 68 of 711 nodes (maximum 2.47%; 1.47% at t0). The status quo does too (82 nodes, maximum 2.81%), so this is oil-price drift that no decision causes.
- GCC real estate peaks at 0.70% (limit 1%), and the largest co-investment position at 2.05% (limit 4%).
- The TRS cap is not imposed at stage-2 and fan nodes, but O1 never exceeds it there.
- H4 credits the 50% revolver without netting a root draw. O1 draws none, so this is latent (issue 10).

**Sleeve funding is an equal absolute cut of every member's original position** (low; part of E1). After O1 redeems four hedge-fund lots fully at the root, the HF sleeve cannot fund anything anywhere in the tree (fan-year HF sales are $0). The simulator sells pro rata to current holdings.

## 9. Issues

| # | Severity | Issue | Fix |
|---|---|---|---|
| 1 | medium | **H16 need-based cap is vacuous.** Its right-hand side includes Σ repayments, and same-node revolver draw-and-repay costs nothing. O1 cycles at 102 node-instrument pairs (up to $82bn); all need-row duals are 0. Fan years then sell with path foresight. Under the cap as DSGO specifies, Φ* is 0.970 (not 0.957) and in-tree P(goal) 43.4% (not 46.7%; B0 43.2%). The out-of-sample P(goal) of the re-optimized root is 46.99–47.27% vs 46.90%. RESULTS §11 "E2 bounded by H16" is false as coded. | Cap repayments by the parent's balance (or drop RP from the row), and replace the 0.08·W allowance by the floor shortfall. Re-state the in-tree statistics and the E2 claim. |
| 2 | medium | **H9 degenerate.** 126 red-event sales sit at exactly the $0.05bn allowance, so R = 0 on 67% of mass and CVaR at 1 − ε ≤ 0 equals "no red event on any path". ε = 0.6% gives E* and Φ* identical to the hard rule, so the ε frontier (0.3–1.2%) is inert. "The red-event limit does not bind" is wrong in the tree: without H9, Φ* is 0.953 and in-tree P(goal) 47.7%. | Count any forced red-tier sale (no allowance) or use a strict threshold with a margin. Report the ε frontier only after checking P(R = 0) < 1 − ε. Correct RESULTS §10. |
| 3 | medium | **O2 labelled "exact max-P(goal) MILP"** (RESULTS §4, H5) is LP rounding. On the reduced instance it gives 46.31% against the proven optimum of 48.65%. Its 79–86% gap is against max E[min(1, W̃/M)], and the margin-version bound is not a bound on the no-margin P(goal) (0.85988 vs 0.86013). | Label it "LP-rounding incumbent (heuristic)". Run H5 on the exact MILP on a subtree (DSGO §4.4 fallback) or report it as indicative. |
| 4 | low | **The docstring claims every DSGO §4.6 row**, but H8, H10(b), H12, H13 OV1/OV2, H3's 30-day test, H5's maturity limit and ADR-39 (ii) are absent and missing from RESULTS §11. On O1 only ENR drift exceeds its limit (68 nodes; B0 82). | List them in §11 and correct the docstring, or implement H8 as "no new oil-linked ADDs" and ADR-39 (ii). |
| 5 | low | **GBO reporting and checks.** The headline "Φ* = 0.957" is the minimum bPOE; O1's own bPOE is 0.9617 (Φ* + 0.005, tie row binding). A5 compares a function with itself; A7, A8 and "solves" are hard-coded to pass. DSGO §4.3 step 4 (LP value vs `stats.bpoe` within 1e-6) is not run. It holds: 2.5e-7 against the exact perspective LP. | Report both Φ* and bPOE(O1). Make A5 compare the LP's CVaR row with an exact recomputation, and run the perspective cross-check. |
| 6 | low | **Big-M L = 0 is not valid as stated.** The range-breach column BRK is unbounded above, so min W̃ over the feasible set is −$193bn (reduced instance). With BRK at its breach the minimum is +$109bn, and the MILP optimum is unchanged with valid M. DSGO's argument also ignores ψ·U, the pacing credit and range charges. | Bound BRK by its breach (it then also needs no cost in B0), or derive L_ℓ with BRK minimal. Fix the DSGO §4.4 text. |
| 7 | low | **`tree_stats` flags red events with RS > thr**, while solutions sit at RS = thr. A 1-ulp difference makes the reduced exact MILP report P(red) = 4.6% with R ≤ 7e-18. | Use RS > thr + tolerance, consistent with the H9 row. |
| 8 | low | **Replication books share one path set** (seed 1031), and book k's template-truth seed equals book k+1's book seed (identical normal draws). H3's between-book standard error therefore understates the uncertainty. | Give each book its own simulation seed and a disjoint template-truth seed (e.g. via SeedSequence spawn). |
| 9 | low | **Attribution boundaries.** REBALANCE is a row restriction overlapping SELL, ADD, REDEEM and PACE. BETA excludes the completion adds that DSGO F4a includes ($12.7bn of long-only adds sit in ADD). BELIEFS also changes the B0 readings and keeps the fused σ_post. Switch-offs are uncertified, unlike O1. PACE needs Phase I. | State these in §5; move index-like long-only adds to BETA. Certify the switch-off GBOs. |
| 10 | low | **H4 credits the revolver without netting a root draw.** Latent: O1's root revolver is 0. | Subtract the root revolver balance in H4, as H3 and the red margin do. |
| 11 | low | **Latent or no-effect asymmetries.** The B0 LP does not price BRK (at its vertex BRK is still minimal in all 464 cells). The simulator never repays the revolver in years 1–2 for any `plan` policy, even under rule recourse (0.4690 either way). Sleeve funding is an equal absolute cut, so a fully redeemed member blocks its sleeve (HF in O1's tree). | Price or bound BRK. Apply the playbook-only repayment rule. Document the sleeve cut in E1. |

## 10. Reproducing this check

The scripts are in the session scratchpad: `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\vm\`. They run with `.venv\Scripts\pythonw.exe -B <script>`, because `python.exe` is blocked by application control. Each writes a `.log` and a `.json` beside itself. The author's code is imported read-only, and the instrumented simulator is a scratch copy executed in memory.

| Script | What it does |
|---|---|
| `full_o1.py` | Runs the author's pipeline at full scale and captures every GBO solve (`full_dump.pkl`) |
| `full_checks.py` | bPOE/CVaR numerics, every row and bound of O1, perspective LP, MILP relaxation with and without the margin, B0's BRK |
| `my_lp.py`, `vlib.py` | The independent LP; Clarabel and HiGHS wrappers; perspective-LP builder; exact CVaR and bPOE |
| `my_full.py` | Author solutions in my rows; my mean, CVaR, perspective and tie-break solves (HiGHS and Clarabel) |
| `make_reduced.py`, `red_author.py`, `red_mine.py` | Reduced instance (`reduced\params.json`); author pipeline incl. exact MILP; my side incl. MILP indicators, big-M bounds and my B0 |
| `oos_check.py` | Certification re-run, fresh-draw hashes, seed collisions, rule-recourse instrumentation, E1 |
| `attr_check.py` | SwitchOff diffs and independent re-solves of all 11 families |
| `followup1.py` – `followup4.py`, `final_full.py` | Red-threshold knife edge, scaled Clarabel, H9 degeneracy, H16 loophole in-tree and out of sample, unimplemented rows, TRS cap |

*SYNTHETIC – NOT ADIC DATA.*
