# Framework description v1.0: mathematics and specification review (§3–§6, §10)

> **SYNTHETIC – NOT ADIC DATA.** This review checks `design/FRAMEWORK_DESCRIPTION.md` v1.0 (draft). Every number below comes from the synthetic book SYN-ADIC-177, from `examples/mpo_v2/params.json` as committed in `2aafbad`, from the prototype's own run artefacts at that commit, or from independent synthetic re-derivations. Nothing is ADIC data.

**Scope.** Sections 3 (multi-period approach), 4 (optimization mathematics), 5 (data and three-return fusion), 6 (simulator and certification) and 10 (glossary), line by line.

**Sources.**
- `design/DECISION_SPACE_AND_GOAL_OBJECTIVE.md` v1.1 ("DSGO"), including its "Review changes".
- `design/SLIM_ARCHITECTURE.md` ("SLIM").
- The prototype as committed in `2aafbad`: model.py, optim.py, tree.py, scenarios.py, prep.py, fusion.py, book.py, sim.py, policy.py, tasks.py, world.py, common.py, mpo_v2.py, params.json, run_log.txt and results.json. Every file was read through `git show 2aafbad:…` into a scratch snapshot, so the parallel fix could not change what was checked. The document itself is byte-identical to its `2aafbad` version.
- The fix lists in `examples/mpo_v2/verify_math.md` §9 (issues #1–#11) and `verify_finance.md` §5 (F1–F13, L1–L5).

**Method.**
1. Every equation in scope was re-derived by hand.
2. An independent script with no prototype imports re-derives the bPOE/CVaR link, GBO's STRETCH form, the Charnes–Cooper LP, the fixed-point iteration, DSGO's degeneracy table and pure gamble, the Gaussian optimal-transport map and the owner-draw projection, and counts the LP columns. It is `fd_math_checks.py` in this session's scratchpad; Appendix A reproduces its output.
3. Every symbol, unit, parameter value and tree dimension was compared with `params.json` and with the code that reads it.

**Classification.**
- **fix-now:** the document is wrong, internally inconsistent, or silent on a deviation, measured against DSGO/SLIM or the `2aafbad` code, and no pending fix covers the point. It can be corrected today.
- **sync-later:** the document matches `2aafbad` (or the spec), but the item is on the `verify_math` §9 or `verify_finance` §5 fix list. Re-check the text against the fixed code; do not edit it now.

---

## Verdict

**The mathematics is sound and the description of the prototype is close.** In the four sections and the glossary I found no arithmetic error in the optimization core. These all hold, re-derived or matched to code:
- bPOE and its CVaR link, Propositions 1–3 and Remark 1;
- GBO's two regimes and its STRETCH closed form;
- the Charnes–Cooper LP and its τ-scaled CVaR rows;
- the fixed-point iteration and its certificate;
- the MILP indicator row;
- CRRA(3) + L2 and Phase I;
- the dual-based liquidity premium, the reservation price, hurdle and break-even algebra, and the SELL reading rule;
- the tree dimensions and model size;
- all six factor equations, every ledger row and constraint form, and the fusion equations;
- the simulator mechanics.

**Nine passages need correcting before the verified version (medium):**
1. The owner-draw equation places the projection so that the override cannot bite at today's Brent (FN-01).
2. §5.6 states a −½σ²_sys term the prototype does not have and the log basis does not need (FN-02).
3. §5.6's belief-risk rationale overstates what one common driver does (FN-03).
4. "Above the mean, probability can rise only through dispersion" contradicts Proposition 3 (FN-04).
5. §3.6 states the catch-up rationale backwards (FN-05).
6. §3.7 says the red margin is hard at fan years, which neither the code nor §4.3 does (FN-06).
7. §4.11's prose gives REFINANCE priority, but R1's formula gives LEVER priority (FN-07).
8. §6.2 says the headline truth uses 0.5× or 1.5× alpha dispersion, but it uses 1.0× (FN-08).
9. Twenty-odd symbols collide across sections, including g_ℓ, τ, H1–H7, X, y and Φ (FN-09).

Sixteen low fix-now items follow (FN-10 to FN-25). Fourteen items are sync-later (SL-01 to SL-14); four of them are medium: H16, H9, O2's label and draw accrual.

---

## 1. What was re-derived, and the result

| Item | Where | Check | Result |
|---|---|---|---|
| bPOE₀(X) ≤ p ⇔ CVaR₁₋ₚ(X) ≤ 0, via a = −1/η | §4.5 l.515–518 | 400 random discrete distributions × 25 levels | 0 mismatches |
| Proposition 1 (icx monotone) | l.522 | each (ax+1)⁺ convex, non-decreasing for a ≥ 0; min preserves order | holds (heading: FN-13) |
| Remark 1: E[(aX+1)⁺] = (a/W₀)E[(W^b − W̃)⁺], W^b = W* + W₀/a | l.526 | algebra | holds |
| Proposition 2 | l.529 | E[(aX+1)⁺] ≥ aE[X] + 1; Jensen for concave ψ ≤ 𝟙 | holds (wording: FN-11, FN-04) |
| Proposition 3 | l.530–532 | PLAN: both depend on (m − W*)/s. STRETCH: on ρ = −m + s·r_Z = c, (W* − m)/(c + m) falls in m | holds |
| GBO STRETCH: Φ = 1 + E[X]/c_max | l.553, 566 | 300 random distributions with E[X] ≥ 0 and X ≥ −c_max | exact (0 violations); continuity at 1 holds |
| Charnes–Cooper LP, x* = y*/τ* | l.557–563 | 25 random LPs against a grid over a | LP ≤ grid minimum; gap ≤ 3.4e-4 (grid step) |
| CVaR auxiliaries scaled by τ | l.563 | substitute η̃ = τη, z̃ = τz; H10's right side becomes τ·(CVaR^B0 + δ) | holds |
| Fixed-point iteration | l.567 | 20 random LPs | monotone in every case; reaches the perspective-LP optimum to 3.6e-14 |
| Tie-break rows | l.568 | optim.gbo: CVaR row coefficient Φ* + 0.005; mean row E* − 0.005·c_max·W₀ | matches |
| MILP row: W̃ ≥ (W* + ε_gW₀)g with L = 0 | l.575–578 | algebra; optim.milp | matches (justification: SL-06) |
| "round" incumbent | l.582–584 | optim.milp_round | matches (label: SL-03) |
| CRRA(3) + L2 | l.590–595 | U₃ = −1/(2w²); min of 32 tangents ≥ U (outer); max of 16 secants = interpolant; real wealth /(W₀·1.025⁵) | holds; matches params |
| Phase I | l.612 | optim.phase1; tasks.run_gbo re-runs it for infeasible variants | matches |
| ℓ_n = λ_n/(e^{r_f}Σλ_c) − 1 = 𝓜/(π^H − 𝓜) | l.620–626 | stationarity in C_n (cash rows n and children, W, NR, LQ rows) | holds; policy.liquidity_premia matches |
| p*, h, μ^BE; SELL ⇔ p^ce > p* ⇔ μ̂ < μ^BE | l.630–637 | μ^BE − μ̂ = ln(p^ce/p*)/D | exact equivalence; policy.cards matches (caveats: FN-14, FN-15) |
| ADD rule against p* | l.648 | buy iff p^buy < θe^{(μ̂−h)D} | consistent with SELL |
| R1 formula | l.658–662 | policy.r1_labels | matches (prose: FN-07) |
| Model size | l.668–673 | 81 × 251 + 711 × 51 + 210 × 10 + 8 | 58,700 columns exactly; run_log: 59,667 rows, 635,380 nonzeros |
| Solver settings | l.675 | model.highs / run | IPM + crossover, 1 thread, seed 0, tolerances 1e-7: matches |
| Tree shape | l.313–320 | tree.py; results.json | strata 1/1/2/3/3; 10 × 7 × 3; 81 / 210 / 711; rank rule 10 ≥ 7, 7 ≥ 7, 3 ≥ 3 |
| OT map A = S^½(S^½S_cS^½)^−½S^½ | l.318 | 50 random covariance pairs | AS_cA' = S to 1.4e-13; equals S_c^−½(S_c^½SS_c^½)^½S_c^−½ |
| Factor equations (six) | l.274–283 | scenarios.Generator.step | all match, including E_t on start-of-quarter state |
| Unit engine | l.302–306 | UnitEngine.step | matches (precision: FN-22) |
| §4.2 ledger rows | l.400–445 | model.py | x-balance, cash row (all six lines), W, E, LQ, B, Q and m^red match |
| §4.3 row forms | l.453–491 | model.py | match (H16: SL-01; H9: SL-02; H4: SL-14) |
| W̃_ℓ | l.498 | Wt row; prep.acc | matches (accrual: SL-04) |
| Fusion | §5.2–5.4 | fusion.fuse | translations, Benktander, Bühlmann, κ, weights, σ_post, σ̂, Student-t quantiles and α̂ match |
| Degeneracy table | l.536–541 | exact lognormal | bPOE 1.000 / 0.969 / 0.910 / 0.820 exact; three entries off in the third digit (FN-12) |
| Pure gamble, M2 row | l.543 | quadrature | 52.6% → 54.3%; 0.910 → 0.913: matches |
| Simulator | §6.1–6.4 | sim.py, tasks.py, mpo_v2.py | CRN by (seed, chunk), seeds 21 and 31, 4,000 / 10,000 paths, draw ÷ 4, waterfall order, B0–B4, metrics and Holm set match (FN-19 to FN-21) |
| Constants | various | — | 2.563 = 2 × 1.2816; coverage at κ 2.2 = 44.0%; tail cap 0.922 × 0.18 = 0.166; c_max = 3.221; 1/210 = 0.48% |

---

## 2. Fix now

### Medium

**FN-01. §3.2, l.293: the owner-draw projection is in the wrong place.**
- **Document:** d^tgt_y = Π[5%,10%](5% + 5%·(67 − P)/(67 − 23) + 2%·𝟙[override]).
- **Code** (`scenarios.Generator.draw_rate`): the oil-linked target is clipped first, then the override is added and the result clipped again.
- **Effect:** by the document's formula, the override adds nothing whenever Brent exceeds $84.6, because 5% + 5%(67 − P)/44 + 2% < 5% there. That includes today's $126.55 Gulf-war state, where the override probability is highest (2% a year). Between $67 and $84.6 it adds less than 2pp.
- **Recomputed** (Appendix A §8), target with an override:

  | Brent | Document | Code |
  |---|---|---|
  | $126.55 | 5.00% | 7.00% |
  | $90 | 5.00% | 7.00% |
  | $50 | 8.93% | 8.93% |

- §7.5 ("a 2% a year override probability adding 2pp") agrees with the code, not with §3.2.
- **Fix:** d^tgt_y = Π[5%,10%]( Π[5%,10%](5% + 5%·(67 − P_y)/44) + 2%·𝟙[override_y] ). P_y is Brent at the start of the fiscal year, and the override probability is keyed to the oil state Z at that date.

**FN-02. §5.6, l.748: the tree's belief equation has a −½σ²_sys term the prototype does not apply.**
- **Document:** R_{i,c} = μ̂_i − ½σ²_sys,i + b_i'(f_c − Ef) + σ_post,i·(5/3)e_ℓ (fan years only).
- **Code:** holdings move along the tree through the shared unit engine (prep.prepare → tree.propagate → UnitEngine.step: r = r_f/4 + f·b + α/4), with α̂_i = μ̂_i − (r_f + b_i'f̄). So the annual log return is R = μ̂_i + b_i'(f_n − f̄) + (5/3)σ_post,i·e_ℓ·𝟙[t ≥ 3]. No −½σ²_sys term exists anywhere in the prototype.
- **Math:** §2.5 defines μ̂ as an annualized forward *log* return, and b'(f − f̄) has mean zero, so E[R] = μ̂ needs no convexity correction. With the term, the tree would sit ½σ²_sys below the belief: about 1.3pp a year for a beta-1 equity holding at 16% volatility, a systematic penalty on high-beta holdings. DSGO §3.3 carries the same term; it is right only if μ̂ is an arithmetic mean.
- **Fix:**
  - Write R_{i,n} = μ̂_i + b_i'(f_n − f̄) + (5/3)σ_post,i·e_ℓ·𝟙[t(n) ≥ 3].
  - Index by node n; the current form mixes branch c and leaf ℓ.
  - Tag DSGO's −½σ²_sys as not applied, with the reason, and raise it against DSGO.

**FN-03. §5.6, l.751: one common belief driver does not remove riskless spreads.**
- **Document:** "Without it, two holdings with the same loadings but different μ̂ would form a riskless spread, and the LP would push belief-versus-bid swaps to their caps."
- **Code** (prep.py: `a_hat + e[ids]·s_post`): there is one draw e_ℓ per fan path. Every holding shares it, scaled by its own σ_post.
- **Effect on a long/short pair with equal loadings:** belief risk is (5/3)·|σ_post,1 − σ_post,2|·e_ℓ.
  - It is zero when the two σ_post are equal.
  - It is far below the independent-error value otherwise. At 3% against 1.5%, it is 2.5pp a year, against 5.6pp with independent errors (Appendix A §10).
- So the driver penalizes a tilt toward weakly evidenced holdings as a whole, but leaves most spreads nearly riskless. The per-unit trade cap is what actually bounds the swaps.
- **Fix:** say so. DSGO's group component ρ_g (Planned) adds cross-group spread risk; idiosyncratic belief errors are not in the tree.

**FN-04. §4.5, l.529: "Above the mean, probability can rise only through dispersion, which is gambling."**
- **Math:** for W̃ = m + sZ with m < W*, P(goal) = 1 − F_Z((W* − m)/s) rises with m as well as with s.
- Proposition 3, two lines later, concludes that the P(goal)-optimal point at a binding tail limit is the *mean*-maximizing point. DSGO §0 finding 3 says P(goal) "is bought with tail risk or with drift". The sentence, carried over from SLIM §3.3, contradicts both.
- Jensen shows something narrower: a concave or buffered *surrogate* cannot certify any probability above the mean.
- **Fix:** "Above the mean, no concave surrogate can certify a positive probability. The exact P(goal) rises through drift or through dispersion, and dispersion alone is gambling."

**FN-05. §3.6, l.354: the catch-up rationale is backwards.**
- **Document:** the plan is "re-solved against the original goal path W₀·1.10^t rather than a reset goal, so that losses do not trigger catch-up risk."
- Keeping the original path after a loss leaves the book behind it. A re-solve is then STRETCH and levers unless G5 binds (DSGO §5.5). SLIM §3.5 says: "Guards G3 and G5 police the catch-up incentive after losses."
- A reset goal would remove the catch-up pressure, at the cost of time consistency. The original path is chosen for pre-commitment (Forsyth 2020), and its catch-up incentive is exactly what G4/G5 and certification guard against.
- **Fix:** "…rather than a reset goal, so that the plan stays pre-committed (Forsyth 2020). After losses this makes a re-solve STRETCH and creates a catch-up incentive, which G4 and G5 restrain and certification flags (DSGO §5.5)."

**FN-06. §3.7, l.367 and §4.3, l.469 disagree: is the red margin a hard row at fan years?**
- **§3.7:** "Hard rows (floors, leverage, and a red margin ≤ 0, meaning non-red liquidity covers next year's needs) hold at every leaf and fan year."
- **Code:**
  - Floors and leverage hold at every time node (`floor4`, `floor8` and `lev` rows).
  - The red margin is bounded hard only at leaves: H15, `M[leaf] − SL15 ≤ 0`.
  - At fan years 3–4 the margin enters only H9's CVaR surrogate (the `H9m` hinge rows).
- §4.3's H15 row says "at leaves", which matches the code. DSGO RV-07 likewise puts fan-year margins into H9, not into a hard row.
- **Fix:** "Floors and leverage hold at every fan year and leaf. Non-red liquidity covers next year's needs at the leaves (H15). Fan-year margins enter the red-event surrogate H9."

**FN-07. §4.11, l.664: the prose gives the opposite priority to R1's formula.**
- **Document:** "Borrowing therefore first counts as REFINANCE, funding the draw, existing calls and debt service; only the remainder that funds new exposure is LEVER."
- **Formula:** LEVER_n = min(ΔB⁺, ΔE^disc⁺) assigns borrowing to net new exposure first. Only the excess over ΔE^disc is REFINANCE.
- The two readings agree only when the node's cash and reserves are unchanged.
- **Counterexample:** borrow $5bn, add $5bn of liquid exposure, pay a $5bn draw out of Treasury.
  - The formula, and `policy.r1_labels`, give LEVER 5 and REFINANCE 0.
  - The sentence gives REFINANCE 5 and LEVER 0.
- DSGO §1.2 has the same sentence. This is the split the user defined, so the words must match the rule.
- **Fix:** "Borrowing counts as LEVER up to the node's net discretionary exposure added; any excess is REFINANCE. When cash and reserves are unchanged this is the same as 'borrowing first funds the draw, calls and debt service'." Raise the same correction against DSGO §1.2.

**FN-08. §6.2, l.768: the headline truth does not differ from the beliefs in alpha dispersion.**
- **Document:** the truth "deliberately differs from the model the fusion assumes: true alpha dispersion is 0.5× or 1.5× the prior's".
- **Code:** the headline book uses `truth_model.alpha_dispersion_main` = 1.0 (`world.headline_variant`; `book.make_book`: α_true = α* + disp·sd_prior·z). Its true alphas therefore have the prior's dispersion. The 0.5× and 1.5× variants apply only to the four replication books (`mpo_v2.py`, `rep_specs`).
- The headline truth differs from the belief model through the other four channels:
  - the bias shift (+1 prior sd);
  - the +1pp drought optimism;
  - 44% range coverage;
  - half bid pass-through.
- **Fix:** say so. If the books fix (verify_finance F1) changes the headline variant, re-check.

**FN-09. §3–§6 and §10: symbols collide across sections.**

Several symbols carry two or more meanings within a few lines. A reference for the quant lead should rename the in-section clashes and extend the glossary. In order of how much they mislead:

| Symbol | Meanings |
|---|---|
| g_ℓ | the leaf's decision-coefficient vector (§4.5 l.557) and the MILP goal indicator (§4.6, §10); also g = group and ĝ*(p) |
| τ | the Charnes–Cooper scale (§4.5) and the rounding threshold (§4.6 l.584) |
| H1–H7 | hard rows and pre-registered hypotheses (§6.5). §4.8 l.604's "for the comparison H2" means the hypothesis, while H2 is also the cash floor |
| X | the miss X_ℓ (§4.3–4.5) and the exit factor X_t (§3.2) |
| y | template dollars y_{n,k}; the 10-year yield y_t (§3.2); the Charnes–Cooper variable (§4.5); the buyer return y_b (§5.2) |
| e | the exit window e_t and the belief-error driver e_ℓ (both in §10) |
| Z | the oil state Z_t, the credibility weight Z_g (both in §10) and the standardized variable in Proposition 3 |
| Φ | the GBO value and the normal CDF (§5.3 κ^arch; §2.5) |
| η | CVaR thresholds (H9, H10, §4.5) and the VIX noise η_{t+1} (§3.2) |
| s | sold fraction, sleeve index (both in the x-balance l.400, and both in §10), credit spread s_t, call stress s(S), signals s_j and s_f, spread s_B |
| v, u | P2S decrease v_n and VIX level v_t; P2S increase u_n and the LP auxiliaries u_ℓ, u_{ℓ,k} and u* |
| r | redeemed fraction r_{n,i} and the returns r_{i,t}, r_f, r^B, r^SAA |
| m | CMA world, ancestor or start node (T_{m→n}, y_{m,k}, m ∈ 𝒟(ℓ)), exit multipliers m^D and m^C, location m(x) |
| k | template, the node index in §4.4's product ∏_{k≻n}, the CVaR-level index (α_k, η_k), intensities k^eq and k^D, and the prior μ_k |
| a | added fraction, the bPOE multiplier, the holding's age (§5.2), a₂(ℓ) and the "actual a" signal |
| p | leaf probability, parent p(n), the bid p and the realized share p (both in §5.2), the iterate p_k |
| D, G, λ | duration D_i, draws D_t (§4.4) and the set 𝒟(ℓ); gross returns G_{n,i} and G^eq, compounding G_{t→T}, guards G4 and G5; cash dual λ_n, λ_T and λ_Lev |
| S, M, ε | macro regime S_t and the covariances S, S_c (§3.3); big-M, MOIC M and worlds M1–M6; ε_R, ε_g and the shocks ε^{1..5} |

### Low

**FN-10. Symbols used without definition, and glossary gaps.**
- **Undefined at first use:**
  - §3.3 l.318: S and S_c.
  - §4.1 l.392: R^eq_n.
  - §4.2: V^sl, the sleeve bid, c^tail, f^u, f^β(n), f^P2S(n), f^TRS, tc, oid_j, T^Dist and T^Call.
  - §4.3: av(n) and w_g.
  - §4.5: c_ℓ and g_ℓ (DSGO P5: c_ℓ = (W* − W̃_ℓ(0))/W₀).
  - §4.10: D_i, defined only later in §5.2; and the table's s_B, f, T, λ_Lev, T*, μ̂^new, p^buy, h^new, α̂^net, κ^reentry and T^cash.
  - §5.6: σ_sys.
- **Missing from §10:** τ, a, a_min, η, z_ℓ, u_{ℓ,k}, E*, Φ*, H, D, V*, κ^G, r^SAA, G^eq, tail_n, oppret_n; the hypothesis, error-ledger and acceptance labels (H1–H7, E1–E5, A-checks); F_t.
- **One convention to state:** CVaR₁₀ in §6.4 and §8 is the mean of the worst 10% of TWR, a return. CVaR_α in §4 and §10 is the upper tail of a loss.

**FN-11. §4.5, l.529: "so bPOE = 1 for every plan".** The inequality holds plan by plan. Fix: "…so bPOE = 1 for that plan; if E[W̃(x)] ≤ W* for every feasible x, bPOE = 1 for every plan (STRETCH)."

**FN-12. §4.5, l.534–543: the degeneracy table is Monte Carlo, not analytic.**
- The document calls it "the spec's analytic check", but the values are DSGO's 300,000-path Monte Carlo. Three entries differ from the exact lognormal values in the third digit.
- Exact values come from E[W̃]/W* = ((1 + m_L)/1.1)⁵, with m_L = m + (L − 1)(m − r_f − 0.30%) and log volatility L·σ:

  | Row | E[W̃]/W*, exact | Document | P(goal), exact | Document |
  |---|---|---|---|---|
  | 8.30%, 1.00× | 0.974 | 0.974 | 40.4% | 40.4% |
  | 8.30%, 1.30× | 1.046 | **1.047** | 46.0% | 46.0% |
  | 10.47%, 1.00× | 1.076 | **1.075** | 52.6% | 52.6% |
  | 10.47%, 1.30× | 1.188 | 1.188 | 58.0% | **57.9%** |

- bPOE and the pure gamble match.
- **Fix:** print the exact values, or call it a Monte Carlo check.

**FN-13. §4.5, l.522: the heading "Why it cannot be gamed" overclaims.** Remark 1 shows that mean-increasing skewed payoffs can be rewarded, and DSGO RV-03 narrowed the claim. Fix: "Why mean-preserving gambles are not rewarded (Proposition 1)".

**FN-14. §4.10, l.637: the interior-sale reading ignores shared rows.**
- The zero reduced cost of s_{0,i} includes the duals of every row that contains it:
  - the PE/Secondaries LP-depth row;
  - the CO, RA, CS, PC and HF group-depth rows;
  - RS_n when the sale is a red event.
- λ₀·bid = ν_i holds only when none of them binds.
- With a binding group cap, p^ce > p* even at an interior sale, and a group member left at s = 0 can show p^ce > p*. A23's hold test (p^ce ≤ p* + 2e-3) would then report a false mismatch.
- **Fix:** add the qualification, and soften "A card therefore cannot contradict its decision" (l.618) to "agrees in sign, up to binding shared caps".

**FN-15. §4.10, l.623–640: caveats on h and ℓ̄.**
1. The closed form p* = θe^{(μ̂−h)D} omits DSGO's unfunded term u_iψ_i and the charges. The LP's p* covers the whole position including its unfunded, so the backed-out h absorbs the unfunded value. That is material where U/N is large: PE-12 has U/N = 1.3.
2. h also bundles r_f (DSGO: h = r_f + ℓ̄ + κ^G), not only the liquidity premium and κ^G.
3. The code floors D at 0.5 years.
4. ℓ̄ is one unweighted average, ½ℓ₀ + ½·mean of the ten stage-1 ℓ_n, used for every holding. DSGO's ℓ̄_i(D_i) is a term average over each holding's duration.

Tag items 1 and 4 as Spec ≠ code. verify_finance L2 (unstable hurdles at D ≈ 1) touches the same cards.

**FN-16. §3.4, l.331: fan-year funding moves do condition on the belief error.** Path-specific sleeve sales, revolver use and beta cuts in fan years see e_ℓ; this is error-ledger row E2. Fix: "no discretionary decision (root, stage 1, stage 2) conditions on the realized alpha error".

**FN-17. §3.6, l.356: the static variant is not a proxy for rolling MPC.** With no recourse it uses less information than the playbook; MPC uses more. It brackets the playbook from below and says nothing about E3 (playbook against MPC). Fix: "The static variant (no year-1 recourse) is certified beside the playbook, and the selection set chooses between them; neither measures E3."

**FN-18. §5.1, l.690 and §5.5, l.740–743: non-external bids act as prices and beliefs.**
- `book.make_book` gives every non-liquid holding with a bid key a synthetic unit bid with alpha pass-through. That includes the holdings flagged `bid_external = false` (source "segment"): CS-01 to CS-05, PC-01, PC-02, PC-05, RA-02, RA-04 and RA-08.
- `prep.prepare` turns each such bid into a price premium on sale proceeds. `fusion.fuse` turns it into a market-anchor signal (μ̂^bid and the disagreement flag).
- In `2aafbad`, PC-02 and PC-05 are sold at such bids.
- **Fix:** disclose this beside "external secondary bids" and "in-house desk quotes are never prices", or restrict both channels to external bids.

**FN-19. §6.1, l.759–761: not every reported number uses the certification set.** The replication and placebo books are certified on their own path set (in `2aafbad`: 4,000 paths, seed 1031, chunks of 2,000), and the selection set runs in chunks of 1,000, not 1,250. Fix: write "every reported headline-book number", and give the book sets' sizes and seeds once SL-07 lands.

**FN-20. §6.3, l.781–793: two simulator details.**
1. Redemption cash arrives at year ends, not every quarter: the queued remainder is paid and new notices pay at the class pass-through. The tail-ladder payoff also pays at year ends. Only the claims' accrual is quarterly.
2. Optimized policies are cut to the class and behind caps; B0–B3 to the flat 1.30× cap; B4 is uncapped. "Baselines share the flows, limits…" (l.793) should say so.

**FN-21. §6.2, l.776: belief mode is not DSGO's posterior-draw mode.** It uses α = α̂ (point beliefs), the prior opportunistic Sharpe and no idiosyncratic noise (`tasks.run_sim` with truth = None). DSGO §5.5 draws α ~ N(μ̂, σ²_post). Tag as Spec ≠ code.

**FN-22. §3.2: untagged deviations and precision.**
1. **Untagged deviations:**
   - Regimes are first-order Markov; DSGO §5.1 has a semi-Markov crisis dwell of 6–18 months.
   - Factors have no VAR(1) term; DSGO has f_t = c_S + Af_{t−1} + D_SL_Sε_t.
   - Brent starts from spot; DSGO uses the futures strip and Gulf-war dwell conditioning, which §9.3 lists as production adds.
2. **l.272, "nothing is predictable to time":** true for equity. The credit factor's expected return varies with the spread level (the ¼s_t carry) and with the regime's expected default loss.
3. **Small items:**
   - l.302's "(·)" stands for V_ie^r − ¼yld_iV_ie^r.
   - Reported NAV also adds calls: N' = N·e^{r^N}·(1 − Dist/(Ve^r)) + Call.
   - η in the VIX equation is standard normal, not Student-t.

**FN-23. §3.3: precision.**
1. The first clustering feature is the year's equity log excess return Σf^eq, not "the year equity return".
2. Stage 2 is allocated by class only, not by shock type.
3. Add to Spec ≠ code: DSGO matches 8, 7 and 7 drivers, including the draw rate, and moment-matches the fans. The prototype matches 6 and 6, and at the fans only the fan return and e. The draw rate is never matched (it is a function of Brent).

**FN-24. §4.2–§4.3, §4.7: formula precision.**
1. L^up is credited from year 1 only: H3, m^red and the revolver cap use L^s at the root. The §4.3 forms show L^s + L^up everywhere.
2. In fan years, the cash row, IM, E and m^red use the stage-2 ancestor's p2s, trs, hed and opp. Written as hed_n, p2s_p and so on, they are undefined at fan nodes.
3. W̃'s draw sum (l.498) runs over path(ℓ) without the root.
4. The TRS ≤ 50%-of-lot cap is imposed only at the root and stage-1 nodes.
5. In model.py the first STR node keeps its parent's class cap ("met within four quarters"). §4.3's G5 row omits this; only §7.2 hints at it.
6. §4.7 and §2.4 use 32 geometric tangents where DSGO §4.5 has 48 adaptive ones. params.json records the deviation; the document should tag it.

**FN-25. §5.2: precision.**
1. "D its duration (a share of H)": D is in years, D = share × H.
2. "DPI distributions to date" is a dollar amount, but DPI usually denotes the ratio. Rename it, for example Dist_td.
3. Fund interests also blend the error, σ_f ← √((c*σ_f)² + ((1 − c*)σ_k)²), before the horizon scaling.
4. D is floored at 0.5 years in ρ_m and in its 0.05/D error.
5. For fund interests the prior enters through the Benktander channel, not as a separate signal; the table says "every holding".

---

## 3. Sync later

Re-check each against the fixed code. Nothing here should be edited before the fix lands.

| Id | Sev. | Where | What the document says now (matches `2aafbad`) | Pending fix | Re-check |
|---|---|---|---|---|---|
| SL-01 | medium | §4.3 H16 l.470; §3.5 l.340 | H16's right side includes +0.08W_n + Δ⁻_n (repayments); "need-based funding" | verify_math #1: the cap is vacuous through same-node draw-and-repay (102 node-instrument pairs); fix caps repayments by the parent balance and replaces 0.08W by the floor shortfall. #11: the sleeve cut is an equal fraction of each member's *original* position | New H16 formula; any "bounds clairvoyance (E2)" wording; document the sleeve cut in §4.2 |
| SL-02 | medium | §4.3 H9 l.477–483; ε_R = 0.6% (§2.4, §4.8) | CVaR surrogate with a $0.05bn allowance; "tree buffer of 0.6% is tighter than the certified 1%" | verify_math #2: degenerate (R = 0 on 67% of mass; ε inert at 0.3–1.2%); #4: ADR-39 (ii), first node after STR, is absent. verify_finance F2, F8, F9: recalibrate. Also, DSGO RV-22's tuning of ε_R to certify P(red) ≤ 1% is neither built nor tagged | Rewrite H9 and the ε_R rationale; tag the tuning |
| SL-03 | medium | §4.6 l.572–586; §10 (O2); §6.5 H5 | "The exact maximum-probability MILP"; the relaxation is "a valid upper bound"; variant A is "the in-sample ceiling" | verify_math #3, verify_finance F10: label O2 an LP-rounding incumbent (46.31% against a proven 48.65% on the reduced instance). The bound is max E[min(1, W̃/M)] on the ε_g-margin problem, so not strictly a bound on the reported P(goal) | Labels, the "ceiling" sentence and H5's basis |
| SL-04 | medium | §4.4 l.498, l.508; §3.8 l.378 | Draws accrue at r^SAA; own-return accrual "Planned" | verify_finance F4: accrue at each policy's own node returns (fixed point) | W̃ formula, E1 and the Known-bias paragraph |
| SL-05 | low | §4.12 l.675; §4.5 l.567–568 | "The GBO value is checked against the exact bPOE function to 10⁻⁶ (A5)" | verify_math #5: A5 compares the function with itself and is hard-coded to pass, as are A7 and A8. DSGO §4.3 step 4 is not run. Φ* is the minimum bPOE, while O1's own bPOE is Φ* + 0.005. The PLAN loop minimizes plain bPOE (a ≥ 0), which equals Φ only if a* ≥ a_min | A5 and A7 text; report Φ* and bPOE(O1) |
| SL-06 | low | §4.6 l.578 | "L_ℓ = 0 is valid because H5 holds at every node, keeping leaf wealth non-negative" | verify_math #6: H5 bounds W, not W̃ = W − ψU ± pacing − range charges + accrued draws. BRK is unbounded, so min W̃ over the feasible set is −$193bn on the reduced instance | Once BRK is bounded: W ≥ 0 by H5; W̃ ≥ 0 because accrued draws exceed ψU, the pacing debit and the bounded range charges |
| SL-07 | low | §6.1–6.2; §6.5 l.822–832 | Books "regenerated, re-fused, re-solved and re-certified"; hypotheses as in DSGO | verify_math #8, verify_finance F1: one path set (seed 1031) for every book; colliding template seeds; the placebo shares the headline seed and so the opportunistic Sharpe draw. H1 is tested without its P(red) ≤ 1% clause and unclustered; H6 on the headline book only; H7 as \|ΔP\| < 1pp plus O1's value at equal tail ≤ 0.5pp, not "one SE" | Book description; the prototype's test definitions beside the DSGO table |
| SL-08 | low | §6.3 l.791 | "Surplus above 9% repays the revolver, except in playbook years" | verify_math #11: `2aafbad` skips the repayment in years 1–2 for every plan policy, static included; the fix makes it playbook-only, which is what the document says | Confirm against the fixed sim.py |
| SL-09 | low | §4.1 l.392; §3.2 l.281, l.287; §6.2 l.773; §5.2 prior row | Opportunistic return per $ of IM; zero-mean vol factor; hedge-fund α* = 0 | verify_finance F5 (the tree carries only the factor part at the prior Sharpe; 60% is idiosyncratic in the simulator) and F6 (no put-writing premium) | oppret_n, f^vol, the "not next quarter's expected return" note and the hedge-fund prior |
| SL-10 | low | §6.4 l.813; §6.5 H4 | G6 signatures, Sarle flag above 0.555 | verify_finance F3 (A14 run only on the selected variant), F10 (Sarle falls with kurtosis) | Metric list; which variants are tested |
| SL-11 | low | §5.2 l.701 | Underwritten row: required-return target, "expires after T_u + 1" | verify_finance F12 reworks the signal. Today the code uses it for deals only while T_u − a ≥ 1, so it expires after T_u − 1; liquid mandates use ln M_u/(T_u·share) | The row once the signal is rebuilt |
| SL-12 | low | §4.11 l.661–664; §4.2 l.432 | R1 inputs; W_n as the economic NAV of the whole book | verify_finance F7, F11: R1 is reported gross of redemptions in flight; node netting hides revolver use; the TRS is labelled portable alpha; TERM is a bridge. At the notice node W_n excludes the redemption receivable: redeemed units leave Σx̄V at p, and Q appears only at the child | R1 reporting text; W's definition at redemption nodes |
| SL-13 | low | §4.4 l.498; §3.7 l.364 | c^PACE terms and values; the 0.25–1.25× pacing range | verify_finance F2: pacing is worth about 0 in the horizon; non-PE c^PACE values are assumed; the Amber corridor is not imposed | Pacing terms if the treatment changes |
| SL-14 | low | §4.3 H4 l.458 | "revolver at 50%" | verify_math #10: H4 credits 0.5·L^s without netting a root draw (latent) | "50% of the undrawn signed revolver" |

---

## 4. Section ledger

| Section | Lines | Status | Issues |
|---|---|---|---|
| §3.1 Stages | 255–263 | correct | — |
| §3.2 Generator | 265–307 | factor equations correct; owner draw wrong | FN-01, FN-22, SL-09 |
| §3.3 Tree | 309–324 | correct | FN-23, FN-09 (S), FN-10 |
| §3.4 Non-anticipativity | 326–331 | one overstatement | FN-16 |
| §3.5 Recourse | 333–350 | correct | SL-01, SL-08 |
| §3.6 MPC | 352–356 | rationale reversed | FN-05, FN-17 |
| §3.7 Terminal values | 358–371 | fan-year claim wrong | FN-06, SL-13 |
| §3.8 Tree and simulator | 373–380 | correct | SL-04 |
| §4.1 Data on the tree | 386–393 | correct | FN-10, SL-09 |
| §4.2 Ledger | 395–447 | correct | FN-24, SL-12 |
| §4.3 Constraints | 449–491 | correct | FN-24, SL-01, SL-02, SL-14 |
| §4.4 Wealth and miss | 493–508 | correct | FN-24, SL-04, SL-13 |
| §4.5 GBO and bPOE | 510–570 | correct mathematics; wording and table | FN-04, FN-11, FN-12, FN-13, FN-09, SL-05 |
| §4.6 MILP | 572–586 | correct row | SL-03, SL-06 |
| §4.7 CRRA + L2 | 588–596 | correct | FN-24 |
| §4.8 Selection | 598–606 | correct | FN-09 (H2) |
| §4.9 Phase I | 608–614 | correct | — |
| §4.10 Duals and cards | 616–651 | correct algebra; caveats | FN-14, FN-15, FN-10 |
| §4.11 R1 | 653–664 | formula correct; prose reversed | FN-07, SL-12 |
| §4.12 Size and solver | 666–677 | correct sizes | SL-05 |
| §5.1–5.5 Fusion | 683–743 | equations correct | FN-18, FN-25, SL-11 |
| §5.6 Beliefs in the tree | 745–751 | equation and rationale wrong | FN-02, FN-03 |
| §6.1 Paths | 757–763 | correct for the headline book | FN-19, SL-07 |
| §6.2 Truth | 765–777 | headline dispersion wrong | FN-08, FN-21, SL-07, SL-09 |
| §6.3 Policies | 779–803 | correct, two timing details | FN-20, SL-08 |
| §6.4 Metrics | 805–816 | correct | FN-10 (CVaR₁₀), SL-10 |
| §6.5 Tests | 818–832 | DSGO hypotheses, not the prototype's tests | SL-07, FN-09 |
| §10 Glossary | 1090–1130 | entries correct; collisions and gaps | FN-09, FN-10, SL-03 |

---

## 5. Code observations outside this review's scope

These are not document findings, and neither fix list covers them. They are recorded for the prototype owner.

1. **The static (rule) variant never receives the revolver upsize.** `sim.run_policy` sets L = L^s + L^up only inside the playbook branch at t = 1. The static variant pays the 15bp upfront fee at t0, but its waterfall capacity and undrawn fee stay on $10bn. This is latent in `2aafbad`: O1 has no upsize.
2. **`policy.r1_labels` compares unlike bases at the root.**
   - syn_prev is the gross status-quo beta ($10bn), while syn_now is net of posted margin. Root ΔB is understated by im·$10bn: $0.6bn at DRT.
   - PIK accrual counts as new financing in ΔB.
3. **Forced re-solves are ordered by |size| in $bn.** `params.report.n_forced` says "largest goal value". Rows with no fixable column (the revolver upsize) are skipped, so fewer than six may run.
4. **`optim.gbo` stops the PLAN loop after 12 iterations.** If it has not converged by then, no certificate runs and no flag is raised.

---

## Appendix A. Re-derivation output (SYNTHETIC)

The script `fd_math_checks.py` is in this session's scratchpad. It imports numpy and scipy only; no prototype module.

```
== 1. bPOE_0(X) <= p  <=>  CVaR_{1-p}(X) <= 0 (random discrete distributions)
   mismatches: 0 (0 expected)
== 2. GBO STRETCH closed form: Phi = 1 + E[X]/c_max when E[X] >= 0 and max W~ <= W* + c_max W0
   violations: 0 (0 expected); c_max = 3.221
== 3. Charnes-Cooper / perspective LP equals min_{x in P, a >= a_min} E[(aX(x)+1)+]
   max (grid minimum - perspective LP): 3.41e-04 (>= 0 and small expected: the LP is exact)
== 4. Fixed-point iteration p_{k+1} = bPOE(X(argmin_x CVaR_{1-p_k})) is non-increasing and reaches min bPOE
   monotone in all trials: True ; max |fixed point - perspective|: 3.55e-14
== 5. Degeneracy table (bridge model: m_L = m + (L-1)(m - rf - f), log vol L*sigma; quadrature)
   0.0830 1.00x  E/W* 0.9743 (doc 0.974)  P(goal) 0.4044 (doc 0.404)  bPOE 1.0000 (doc 1.0)  c* None
   0.0830 1.30x  E/W* 1.0463 (doc 1.047)  P(goal) 0.4597 (doc 0.46)  bPOE 0.9690 (doc 0.969)  c* 1.761
   0.1047 1.00x  E/W* 1.0759 (doc 1.075)  P(goal) 0.5264 (doc 0.526)  bPOE 0.9099 (doc 0.91)  c* 0.923
   0.1047 1.30x  E/W* 1.1877 (doc 1.188)  P(goal) 0.5799 (doc 0.579)  bPOE 0.8201 (doc 0.82)  c* 0.961
== 6. Pure gamble on the M2 row: -1.0 W0 with prob 5%, +0.05/0.95 W0 otherwise (mean unchanged)
   P(goal) 0.5264 -> 0.5430 (doc 52.6% -> 54.3%); bPOE 0.9099 -> 0.9129 (doc 0.910 -> 0.913)
== 7. Gaussian OT matching map A = S^1/2 (S^1/2 Sc S^1/2)^-1/2 S^1/2
   max |A Sc A' - S| 1.4e-13; max |A - Sc^-1/2 (Sc^1/2 S Sc^1/2)^1/2 Sc^-1/2| 3.9e-13; symmetric: True
== 8. Owner-draw projection: document formula vs code (draw_rate in scenarios.py)
   Brent  126.55: no override doc 0.0500 code 0.0500 | override doc 0.0500 code 0.0700
   Brent  110.00: no override doc 0.0500 code 0.0500 | override doc 0.0500 code 0.0700
   Brent   90.00: no override doc 0.0500 code 0.0500 | override doc 0.0500 code 0.0700
   Brent   84.60: no override doc 0.0500 code 0.0500 | override doc 0.0500 code 0.0700
   Brent   67.00: no override doc 0.0500 code 0.0500 | override doc 0.0700 code 0.0700
   Brent   50.00: no override doc 0.0693 code 0.0693 | override doc 0.0893 code 0.0893
   Brent   30.00: no override doc 0.0920 code 0.0920 | override doc 0.1000 code 0.1000
   Brent   23.00: no override doc 0.1000 code 0.1000 | override doc 0.1000 code 0.1000
== 9. Small constants
   2 x 1.2816 = 2.5631 ; coverage at kappa 2.2 = 0.4398 ; kappa_arch(0.44) = 2.1988
   tail max payoff 0.922 x 0.18 = 0.166 ; 1/210 = 0.00476 ; c_max = 2 x 1.1^5 = 3.221
   CRRA(3): U(w) = w^(1-3)/(1-3) = -1/(2 w^2); tangent envelope >= U (outer approx): True
   decision nodes 1+10+70 = 81 ; leaves 70x3 = 210 ; time nodes 81 + 210x3 = 711
   columns 81x251 + 711x51 + 210x10 + 8 = 58700
== 10. One common belief-error driver: spread risk of a long/short pair
   equal sigma_post 0.02: spread belief sd = |s1 - s2| x 5/3 = 0.0000 (riskless)
   sigma_post 3% vs 1.5%: common driver 0.0250/yr; independent drivers 0.0559/yr
== 11. Liquidity premium identity ell = lam/(e^rf sum lam_c) - 1 = M/(lam - M)
    0.181034 == 0.181034
```

Exact closed forms behind §5: E[W̃]/W* = ((1 + m_L)/1.1)⁵, giving 0.97430, 1.04630, 1.07590 and 1.18772. P(goal) = Φ((5μ_L − 5 ln 1.1)/(σ_L√5)), giving 0.4045, 0.4597, 0.5264 and 0.5799.

*SYNTHETIC – NOT ADIC DATA.*
