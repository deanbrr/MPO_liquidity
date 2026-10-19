# Quant review: Decision Space and Goal-Seeking Objective

*Adversarial review of `design/DECISION_SPACE_AND_GOAL_OBJECTIVE.md` (DSGO) v1.0, and its consistency with `design/SLIM_ARCHITECTURE.md` (SLIM) v1.0. 19 October 2026. The fixes are applied in place to DSGO, now v1.1, and listed in its "Review changes" section; each one is tagged [RV-nn] where it occurs.*

> **SYNTHETIC – NOT ADIC DATA.** Every number in this review comes from synthetic checks (`review_checks/`), the research syntheses or the design documents. None of it is ADIC data.

---

## 1. Verdict

**The mathematical core is right. The spec could not be built as written, and its value-add demonstration could have been faked in four ways. v1.1 fixes both.**

**What is right.**
- The bPOE identity and its sign conventions. The miss X = (W\* − W̃)/W₀ is loss-type, and the buffered tail is the upper tail of X.
- The CVaR link {bPOE ≤ p} = {CVaR₁₋ₚ(X) ≤ 0}, and the Charnes–Cooper LP.
- Propositions 1–3 and the big-M construction.
- The §4.2 lognormal table. I re-derived it analytically: 40.4%, 46.0%, 52.6%; bPOE 0.969 and 0.910; c\* 1.76 and 0.92.

**What breaks.**
1. **The tree cannot be built as specified.** Moment matching six drivers with 5 children (and 4 fan paths) cannot reach the stated tolerances, and the no-arbitrage test cannot pass for alpha-bearing units.
2. **Beta can masquerade as value-add.** In the pilot, the mean-LP root decision beat the status quo by **+6.9pp** of out-of-sample P(goal), but only **+0.8pp** at equal tail risk. The goal MILP's root decision was **−1.3pp** at equal tail.
3. **The "sealed truth" can confirm the beliefs.** If the synthetic truth is drawn from the fusion's own priors, the sealed-truth test passes by construction, and one synthetic book is one lucky draw.
4. **Alpha and crisis discounts are free lunches in the tree.** Alpha differences are riskless there. The crisis-purchase edge is an assumption about θ.

**Safety claims to narrow.**
- GBO cannot be gamed by *mean-preserving* spreads. But it is a linear hinge: in a complete synthetic market its optimum is all-or-nothing, with wealth at zero in 13–26% of states.
- The guards, not the objective, carry the safety.
- v1.0's guards had gaps: class leverage caps that A14 would itself flag, G4 in dollar terms, a single-level depth guard, and fan years with no rows.
- The red-event rule had dropped ADR-39's stage test.

**Can the MILP run in minutes?** Yes, with caveats. The pilot (200 goal binaries, 9.6k columns) closed in 65 s. R4's "exact in the MILP" would have added about 12,000 binaries and is removed.

**Severity counts.** 24 issues: 3 critical, 7 high, 12 medium, 2 low.

---

## 2. What was checked, and how

| Question asked by the task | Method | Evidence |
|---|---|---|
| bPOE formulation, LP form, threshold variable, CVaR link, what it optimizes | Re-derivation; analytic recomputation of §4.2; complete-market LP | §4 C1; `check_objective.py` |
| Is the MILP valid and small enough for HiGHS in minutes? | Big-M validity proof; HiGHS MIP pilot on a 10 × 5 × 4 tree | `milp_pilot.py`, `milp_pilot_output.txt` |
| Action economics against the research and the user's REFINANCE/LEVER definitions | Line-by-line check of §2 against SYN §4.4–4.6, GROUPS §3, RA §7, ARCH ADR-39/42/49 | §3 RV-09, RV-10, RV-12 |
| Is the tree rich enough? Is the out-of-sample evaluation sound? | Rank argument; low-rank approximation of a synthetic driver correlation; root-decision optimism check on fresh paths | `check_objective.py` C3; `optimism_check.py` |
| Do the anti-gambling guards bind where needed? | Guard-by-guard against ARCH §5.2's hard signatures and SYN §4.8's cushion rule | §3 RV-03, RV-05, RV-11 |
| Can the value-add demonstration be faked (end-of-horizon effects, in-sample optimism, hard limits, mislabels)? | Risk-matched control in the pilot; end-of-horizon audit of fans and leaves; limit audit | §4 C2 and P2; RV-02, RV-04, RV-07, RV-19 |

---

## 3. Issues and fixes

Severity reflects what happens if the issue ships unfixed.
- **Critical:** the build cannot be done as written, or its headline can be wrong.
- **High:** a guard, label or result is materially misleading.
- **Medium:** consistency, power or robustness.
- **Low:** presentation.

| RV | Severity | Issue | Fix applied in DSGO v1.1 |
|---|---|---|---|
| 02 | critical | **Belief-confirming truth, single draw.** If the synthetic generator draws true α, marks and bids from the FBE's own priors, sealed-truth mode is statistically posterior mode and H3 passes by construction. One synthetic book gives one draw of selection luck that path-level intervals ignore | Truth model ≠ belief model (α dispersion ×0.5 and ×1.5, bias +1 sd with a regime component, ranges covering 36–52%, bid informativeness 1.0 and 0.5). K ≥ 8 regenerated books, intervals clustered by book. Null-information placebo book (H7, A19, A21). Posterior mode is never the headline (§5.1, §5.5, §6.5) |
| 04 | critical | **Value-add fakeable by beta.** In STRETCH, GBO is max-mean, so P(goal) rises with risk; selection then picks the riskiest candidate. Baselines had no risk-matched control, and F4 mixed beta with alpha-funded leverage. Families that free tail budget (FUND, HEDGE) look valuable because the budget is respent on beta | New B4 risk-matched line (B0 + synthetic beta, 1.00–1.60×); headline "value at equal tail"; F4 split into BETA and LEVER; new H6 (≥ +1pp at equal tail). Every family is reported raw and at equal tail. SLIM's P0 and archetypes A–C are added as baselines (§4.8, §5.5, §6.1, §6.3) |
| 06 | critical | **Rank-deficient tree.** A branching with K children matches a covariance of rank ≤ K − 1. Stage 2 (5 children) and the fans (4 paths) cannot match a 6-driver covariance. The unmatched directions are riskless in the tree, so stage-1/2 decisions hedge the specific children | 10 × 8 × 8 = 640 leaves under the rule K ≥ d + 1 (d = 8 at stage 1, 7 later). Stage 1 stratified by shock type. Kaut–Wallace out-of-sample stability and the MMW gap added (§5.2, A11, A22) |
| 01 | high | **Alpha riskless in the tree.** Tree returns carry only factor risk, so equal-loading units with different μ̂ form riskless spreads. The LP pushes selection swaps to their caps; the positive state-price test fails by construction | One belief-error driver (with a group component) drawn at stage 1 and held to the leaves; per-unit trade caps scaled by posterior precision; no-arbitrage tested on factor and benchmark assets only (§3.3, §5.2) |
| 03 | high | **"Cannot gamble" overstated.** For fixed a, GBO is a *linear* shortfall below W\* + W₀/a, the exponent-1 class that LIT §4.7 (Krabichler et al.) says reproduces probability maximization. It rewards mean-increasing skewed payoffs. G3 ("exponent > 1 wherever a shortfall penalty is used") contradicted GBO itself, and ARCH §5.2's exponent rule was overridden silently. The single-level depth guard lets loss migrate to the 1% tail | Remark 1 with the complete-market check; P2 restated; multi-level H10(a) (CVaR₉₀/₉₅/₉₉); G1 and G3 restated with the override disclosed; mandatory CRRA tie-break (§4.2, §4.3, §4.6, §4.7) |
| 05 | high | **H1 and H4 inconsistent.** At δ = 0.01·W₀ with H10(a) binding, O1's worst-decile mean wealth is below B0's, so O1 cannot second-order dominate B0, and H4 fails by construction | Recommendation O1 at δ = 0, multi-level (approximately SSD at three levels). δ > 0 points become IC-chosen frontier points. H1 and H4 sit at the same point (§4.7 G7, §6.2, §6.5) |
| 07 | high | **End-of-horizon leakage.** (a) H2/H5/H6 hold "at nodes and leaves" and H9 takes the max over "the path's nodes", but fan years t = 3, 4 are neither. (b) Leaves deduct debt at face only, so preferred equity (12% pref, 1.3× floor), CFO notes, deferred payables, PIK accruals and leaseback rents look free. (c) Fan funding is clairvoyant per path | Fan years are constraint nodes for every row, including H9's red margin. Every financing claim is deducted at fair value. New H16 (need-based fan funding, buy-and-hold fans, forced deleveraging only) (§1.1, §4.1, §4.6, §5.2) |
| 08 | high | **Cards contradict the LP.** h = r_f + RP + ℓ̄ + κ^R counts risk twice: the CMA premium plus the goal-tail charge, while the LP prices risk only through its own kernel. Synthetic beta reads LEVER = FAIL on the card (μ̂ − r_f − RP = 0) while the LP takes it, and §2.6's own rule says ERP − f > charges | Goal-basis hurdle h = r_f + ℓ̄ + κ^G from the LP's kernel; the CMA version is kept as a "utility view" line. LEVER read additively per ADR-49 against κ^G. Flip thresholds from parametric re-solves. A23 card–LP sign consistency (§3.4) |
| 09 | high | **Red event narrower than ADR-39.** H9 counted red-tier sales only at STR nodes or below 0.9 × the normal bid. ADR-39 also counts any red-tier sale in an Amber+ stage or with IG + cash < 8%, and today is Amber. v1.0 would have planned PE and RA sales at DRT nodes and at the root that ARCH and SLIM G2 count as red events | ADR-39 adopted in full with exogenous proxies; root red-tier SELL held at zero and shown by forced re-solve; "ADR-39 relaxed in Amber" made an IC sensitivity (likely the largest driver of t0 SELL value) (§4.6, §3.4, §6.4, §4.8) |
| 10 | high | **Crisis-purchase value is a θ assumption.** Offer discounts (10 / 15–20 / 25–35% on reported NAV) were set independently of θ, fixed at 0.92, so a 30% STR discount books ≈ +31% accretion. GRP: θ is state-dependent (tail-end 0.65–0.70 frozen), and the dry-powder value falls from 15–22¢ to 0.5–9¢ per $ at θ = 0.75 | One primitive: price = ρ × θ_n, with ρ the buyer residual on economic NAV (≈1.0 at BEN and DRT, 0.80–0.84 at STR); discounts derived; θ_n path-dependent; zero-edge placebo and θ = 0.75 sensitivity (§2.2, §5.1) |
| 11 | medium | **Class caps, not cushion caps.** G5 allowed 1.30× at *behind* BEN nodes, so STRETCH sits at the cap while behind, ARCH's hard signature, and A14 blocks its own change list. G4 in dollar terms lets leverage rise after a loss | G5: class caps, a behind cap of 1 + ½(L^class − 1), and borrowed exposure ≤ the B0 liquidity cushion (exogenous, linear, never negative). G4 in ratio form E_n ≤ E_parent·W^{B0}_n/W^{B0}_parent, triggered by "behind" alone (§4.7) |
| 12 | medium | **Mislabels against R1 and the user's definitions.** Deferred-payment purchase labelled "ADD with FUND" (it is LEVER: seller-financed exposure); holdco PIK labelled LEVER by instrument; SMA run-off labelled HOLD (ΔE < 0, cash + is SELL); FUND shown with ΔB +. A4's "LEVER ΔB > 0" fails for futures, TRS and P2S unless B includes embedded financing | R1 in closed form, LEVER = min(ΔB⁺, ΔE^disc⁺); B = recourse + secured + seller + embedded derivative financing; relabels; FUND = capacity only (§1.1, §1.2, §2) |
| 13 | medium | **MILP integers and strength.** R4 "exact in the MILP" adds ≈40 × 61 × 5 ≈ 12,000 binaries for a rule meaningless at cohort level. A8 is satisfied by the MIP start, so it tests nothing about optimality | Goal binaries only; big-M default L_ℓ = 0 with a validity check; LP-tightened bounds optional (pilot: 514 s of bound LPs for a slower MIP); subtree fallback; free-binary count reported (§1.2, §4.4) |
| 14 | medium | **World set inconsistent.** §0 and §4.2 reason on the six-world 8.3% mixture, §5.1 on M1 with M2/M6 "as worlds", §5.5 on M2/M6 as misspecification worlds; SLIM pools six worlds. The PLAN/STRETCH label depends on which | Prototype tree pools M1, M2, M6 (IC weights, default equal, ≈8.5%), clustered on observables; labels per world and pooled; misspecification worlds separate (§5.1) |
| 15 | medium | **Wrong policy behind the probabilities (the toy's H2 again).** Certified numbers describe the playbook, while the process re-solves; a time-inconsistent re-solve at a behind node is STRETCH and levers. The 500-path MPC check gives ±4.4pp | Playbook and rolling MPC both certified, MPC on ≥ 2,000 paired paths; re-solves keep the original goal path; flags at 2pp (§4.3, §5.5) |
| 16 | medium | **Tie-break tolerance undefined.** "Goal value within 0.5pp" means different things in PLAN (a probability), STRETCH (Φ − 1 = E[X]/c_max, so 0.016·W₀) and ĝ\*(p) (a return) | Defined per case (§4.3) |
| 17 | medium | **GBO conditions and tolerances.** P3's equality needs max_ℓ W̃_ℓ ≤ W\* + c_max·W₀; c_ℓ and g_ℓ undefined in P5; A7's 10⁻⁶ against a 0.1% bisection; SLIM's 10⁻⁹ below HiGHS's 10⁻⁷ feasibility tolerance; A6's ‖x − x_mean‖ invalid under LP degeneracy; ℓ formula used μ for π^H | One leaf condition for exactness; notation defined; tolerances consistent; A6 compares objectives (§4.3, §7.2) |
| 18 | medium | **Valuation basis.** Goal NAV basis undefined: on reported NAV, smoothing after a crisis flatters illiquid plans. ω = 0.90 after a crisis on *economic* NAV counted the crisis twice. c^PACE was charged in cash while the tree also models the forgone returns | Goal on economic NAV, reported-NAV P(goal) shown, flag at 2pp; ω = 1 by default (liquidation basis as sensitivity) in both engines; c^PACE post-horizon only (§4.1, A24) |
| 19 | medium | **Hard limits may do the work (the toy's H3 again).** IC ranges were wide but hard (SLIM §5.4 says elastic and priced); H11 bound from stage 1, even at STR nodes; no test relaxes IC limits | Ranges elastic and priced (waived at STR); H11 glide path; A20 relaxes each IC limit one at a time and flags `limit_driven` actions; cap scale added to the frontier (§2.10, §4.6, §4.8, §6.4) |
| 20 | medium | **No volatility driver.** The opportunistic book (short-vol templates) and the tail ladder were priced on a tree with no implied-vol state. A risk-neutral STRETCH objective would see the variance-premium carry without its tail | Implied volatility added as a driver (§5.1, §5.2) |
| 21 | medium | **Facility parity.** B0 and B2 waterfalls omitted signed facilities. In the toy, about half of the uplift was revolver access | Every baseline uses the same signed facilities before red sales and pays the same fees (§6.1) |
| 22 | medium | **ε_R in the tree equals the certified level (1%).** The research carries a tighter surrogate (0.60%) because in-sample bounds slip out of sample | Tree ε_R is a tuned buffer (default 0.60%), certified to 1% (H9) |
| 23 | low | **SLIM consistency.** Guard numbering differs (SLIM G1–G9 vs DSGO G1–G7, different meanings); paths (SLIM 10k + 50k per world vs 10k + 10k); scale (≈450 positions and 500–1,000 leaves vs ≈250 units and 200 leaves); recourse (SLIM group-level vs DSGO per unit); consent "R2" undefined | Mapping table; paths per world; counts aligned; group-level recourse in linear form (fixed t0 cohort baskets); R2 = revolver + owner band (§4.7, §5.3, §5.5, §6.2, §7.1) |
| 24 | low | **Multiplicity.** 5 hypotheses × worlds × consent scenarios with no adjustment | H1 primary; H1–H7 Holm-adjusted; per-world results descriptive (§5.5, §6.5) |

---

## 4. Evidence

All checks are SYNTHETIC. The scripts and outputs are in `examples/mpo_v2/review_checks/`.

### C1. The bPOE optimum in a complete market is all-or-nothing (RV-03)

**Set-up.** A lognormal market: 5 years, 400 equiprobable states, 14.4% log volatility, SOFR 3.89%, and the lognormal pricing kernel. Minimize bPOE₀ of the miss over all payoffs W ≥ 0 with E[ξW] = W₀, using the perspective LP.

| Mixture (geometric) | Optimal payoff | Mass at zero | P(goal) | bPOE | Squared-shortfall optimum |
|---|---|---|---|---|---|
| 8.30% | {0, 2.77·W₀} | 26% | 74% | 0.62 | 400 distinct values; zero only in the worst state (0.25%) |
| 10.47% (M2) | {0, 2.40·W₀} | 13% | 87% | 0.40 | 400 distinct values; zero only in the worst state (0.25%) |

**Reading.**
- Proposition 1 (icx-monotonicity) is correct, but it only excludes *mean-preserving* spreads.
- With a kernel, sacrificing expensive bad states to buy cheap good states raises the physical mean, so a linear hinge rewards it. That is the Krabichler result that LIT §4.7 already cites.
- SLIM §3.3's sentence "a plan cannot buy P̄ by sacrificing bad states" is therefore too strong (§7 below).

### C2. Beta alone moves P(goal) a lot (RV-04)

**Set-up.** The bridge model of SYN §4.12: arithmetic m_L = m + (L − 1)(m − r_f − 30bp), log volatility L·14.4%, i.i.d. lognormal, 400,000 paths.

| Mixture 8.3% | P(goal) gain | Worst-decile mean W̃ given up |
|---|---|---|
| 1.02× | +0.49pp | 0.007·W₀ |
| 1.05× | +1.22pp | 0.018·W₀ |
| 1.10× | +2.29pp | 0.035·W₀ |
| 1.15× (DRT cap) | +3.23pp | 0.052·W₀ |
| 1.30× | +5.49pp | 0.103·W₀ |

**Reading.**
- By interpolation, δ = 0.01·W₀ buys ≈+0.7pp, δ = 0.04·W₀ ≈+2.6pp, and the DRT cap ≈+3.2pp.
- So at v1.0's δ, H1's +2pp could not be met by beta *alone*.
- But the optimizer can free tail budget cheaply, for example by pre-arranging the revolver to avoid B0's forced sales, and respend it on beta.
- The δ ≥ 0.02 frontier points would have shown beta as "uplift".

### C3. Moment matching with 5 children or 4 paths cannot meet the tolerances (RV-06)

- **Rank argument.** With K branches and probabilities p, the centred covariance Σp_c(x_c − x̄)(x_c − x̄)′ has rank ≤ K − 1.
- **Synthetic correlation** of (equity, credit, rates, Brent, exit, draw), with eigenvalues 2.56, 1.45, 0.99, 0.46, 0.36 and 0.19:
  - the best rank-4 approximation (5 children) misses vols by up to **12.5%** and correlations by up to **0.25**;
  - rank 3 (4 fan paths) misses by **15.5%** and **0.41**.
  - v1.0's tolerances were 2% and 0.05.

### P1. MILP sizing pilot (RV-13)

**Set-up.**
- Tree: 10 × 5 × 4 (61 decision nodes, 200 leaves).
- Assets: 40 cohorts (16 liquid; 24 illiquid with 10% sale caps), 5 factors, no idiosyncratic risk.
- Constraints: cash floor 4%, exposure ≤ 1.30W at every node and fan year, owner draw 6%, relative CVaR₉₀ depth guard (δ = 0.01·W₀).
- Size: 9,643 columns, 8,328 rows, 110k nonzeros.

**Results.** HiGHS 1.15.1, single thread, gap 0.5%:

| Step | Result |
|---|---|
| Status-quo LP; mean LP (GBO in STRETCH) | 0.2 s; 1.3 s |
| 400 leaf-bound LPs (L_ℓ, U_ℓ), warm-started | 514 s; fixed 54 binaries to 0, none to 1 |
| Goal MILP, LP-tightened M, no fixing | **Optimal in 65 s, 441 nodes** |
| Goal MILP, with fixing | Optimal in 95 s, 430 nodes |
| Goal MILP, loose M = W\* + ε + W₀ | Optimal in ≈ 70 s |
| In-tree P(goal): status quo / mean LP / MILP | 39.5% / 49.5% / 67.0% |

**Reading.**
- The cohort-level MILP is tractable.
- Leaf-bound LPs are not worth their cost, so v1.1 makes L_ℓ = 0 the default after a validity check.
- At full scale (640 binaries, ≈80k columns) expect 30–90 minutes. The stratified subtree is the fallback.

### P2. Out-of-sample optimism and the risk-matched control (RV-01, RV-02, RV-04, RV-06)

**Set-up.**
- Take the *root* decision of each policy and freeze it: buy-and-hold, with draws paid from cash, then pro-rata liquid sales, then debt.
- Evaluate it on the tree's own 200 leaves and on 20,000 fresh paths, under two truths:
  - truth = belief;
  - truth ≠ belief: one draw of α_true = α̂ + N(0, 1.5%), plus idiosyncratic noise of 5% (liquid) and 12% (illiquid).

| Root decision | Exposure/W | P(goal): tree | Fresh, truth = belief | Fresh, truth ≠ belief | Worst-decile mean W̃ (fresh, ≠) |
|---|---|---|---|---|---|
| Status quo | 0.92 | 41.0% | 34.0% | 34.3% | 0.665·W₀ |
| Mean LP (GBO, STRETCH) | 1.30 | 48.0% | 42.1% | 41.2% | 0.374·W₀ |
| Goal MILP | 1.30 | 45.0% | 38.3% | 36.8% | 0.503·W₀ |

**Value at equal tail.** B4, the status quo with debt-financed scaling of the liquid book matched to the same worst-decile mean on the same paths:
- mean LP: 41.2% vs B4 40.4%, so **+0.8pp**, against **+6.9pp** over the status quo;
- MILP: 36.8% vs B4 38.2%, so **−1.3pp**.

**Reading.**
1. Both optimized roots lever to the 1.30× cap, and most of their uplift is beta.
2. The in-tree depth guard (δ = 0.01·W₀) is met only through stage-1/2 recourse that sees its 5 children. The root alone gives up 0.29·W₀ of worst-decile wealth out of sample.
3. The tree's sampling error alone is about 7pp on P(goal): the status quo reads 41.0% in the tree and 34.0% fresh. That is why v1.1 enlarges the tree and moment-matches it.
4. The exact maximizer's root is worse than plain beta at equal tail, consistent with H5.

**Caveats.** One random tree, no moment matching, one truth draw. Root illiquid sales were uncapped in the pilot, which let the MILP sell 98% of illiquids at the root. The numbers illustrate the failure modes; they are not ADIC estimates.

---

## 5. Notes on the remaining checks

**bPOE, the threshold variable and the CVaR link.**
- bPOE₀(X) = min_{a≥0} E[(aX + 1)⁺]. The threshold variable a is the reciprocal of the buffer c = (W̃_q − W\*)/W₀, where W̃_q is the bPOE-quantile of W̃.
- At the optimum, c\* = −VaR at level 1 − bPOE.
- On a finite tree, the minimum is attained at a breakpoint a = −1/X_ℓ, so c\* ≤ (max W̃ − W\*)/W₀. That gives v1.1's single exactness condition for GBO.
- What bPOE optimizes in PLAN: the tail fraction whose mean just reaches the goal, i.e. Roy's safety-first criterion under location–scale (Proposition 3).
- In STRETCH, GBO is a_min·E[(X + c_max)⁺], i.e. it maximizes E[min(W̃, W\* + c_max·W₀)]. That is risk-neutral up to the cap, which is why the guards must carry the safety.

**MILP validity.** M_ℓ = W\* + ε_g·W₀ − L_ℓ is valid for any lower bound L_ℓ: with g_ℓ = 0 the row reads W̃_ℓ ≥ L_ℓ. ε_g = 0.001 makes the MILP slightly conservative against the out-of-sample event W̃ ≥ W\*, which is acceptable.

**REFINANCE and LEVER economics.**
- The NAV-facility capacity (≈$2.1bn, $1.1bn credited), the revolver terms, P2S costs, Capital Solutions back-leverage, SMA leverage and the RA rows match SYN §4.4–4.5, GROUPS §3 and RA §7.
- The LEVER card's additive form matches ADR-49 once the risk charge is κ^G (RV-08).
- The REFINANCE horizon T\* reproduces L6's "≈2 years" only by ignoring the asset's carry, so it is now labelled a display aid.

**Anti-gambling guards, binding where needed.**
- After v1.1, the binding guard in STRETCH is the multi-level H10(a) (δ = 0) or the behind and cushion caps.
- Leverage at the cap while behind is impossible by construction (G5).
- Risk cannot rise after a loss year (G4 in ratio form).
- Tail risk cannot migrate below the 1% level (H10 multi-level, with ≥ 6 leaves in the 1% tail).
- Red events in fan years count (H9).

**Selection and certification split.** Sound as specified: selection and certification use disjoint path sets. v1.1 adds clustering by synthetic book, Smith–Winkler shrinkage and the count of policies tried.

---

## 6. Verified correct and left unchanged

- §4.2: Propositions 1–3; the degeneracy argument (E[X] ≥ 0 ⇒ bPOE = 1; Jensen for concave lower bounds); the pure-gamble example (P(goal) 52.6% → 54.3%; bPOE 0.910 → 0.913, re-derived); and the drift sensitivity (+0.1pp a year ≈ +0.6pp of 5-year P(goal)).
- The c_max choice (2W\*/W₀ ≈ 3.22 at 5 years, 5.19 at 10).
- The bisection's monotonicity: min_x CVaR₁₋ₚ is non-increasing in p.
- The goal accounting W₀∏(1 + r_t) = W_T + ΣD_t·G_{t→T}, with exogenous static-SAA accrual in the tree (error ledger E1).
- The H4/T4′ stress interpolation: equity −(30 + 10θ)%, distributions (0.45 − 0.45θ) × drought, calls 1 + 0.5θ, consistent at θ\* = 0.58, 0.76 and literal T4 (θ = 1).
- The PE, Secondaries, Co-investment, Capital Solutions, Private Credit, Public Markets, Real Assets, Overlay and Corporate Finance rows, apart from the relabels and the θ fix.

---

## 7. SLIM follow-ups (recommended; SLIM not edited here)

1. **§3.3 "Depth-aware".** Replace "so a plan cannot buy P̄ by sacrificing bad states" with "a plan cannot buy P̄ with a mean-preserving spread; mean-increasing skewed payoffs can raise P̄ (DSGO Remark 1), so G3 and G5 are hard". C1 is the counterexample.
2. **§3.3 candidates.** Add the p → 0 candidate (the mean LP), which is GBO's STRETCH solution. Define the tie-break tolerance per case (DSGO §4.3).
3. **§1.6 Done when.** Change "equals `stats.bpoe` … (1e-9)" to 10⁻⁶, consistent with HiGHS's default feasibility tolerance of 10⁻⁷.
4. **§1.6 Scale and §1.7 paths.** Align with DSGO v1.1: 640 leaves under the rank rule; per-unit root and stage-1 columns with cohort-basket recourse; ≥ 10k certification paths per world (50k in production); K ≥ 8 synthetic books.
5. **§1.7 baselines and §5.5 acceptance item 6.** Add the risk-matched control and "value at equal tail" to the uplift report, beside ΔP(10%).
6. **§3.5 G5.** Use the cushion-monotone form: class caps, the behind cap, and the B0 liquidity cushion. Phrase "exposure may not exceed the parent's" as a share of wealth.
7. **§3.5 G2.** State the ADR-39 stage test explicitly: today is Amber, so root red-tier sales are priced only by forced re-solve.

---

## 8. Residual risks the build must still retire

- **Likely NOT ESTABLISHED.** At δ = 0, with root red-tier sales held out by ADR-39 and beta excluded from value, the realistic sources of uplift are planned BEN-node sales, avoided forced sales, STR-node purchases, pacing and yield-book levers. +2pp (H1) may not be reached. The report must be ready to say so; that is a finding, not a failure.
- **Belief risk in the tree is one driver.** Error-ledger row E5 measures how much the simulator's full idiosyncratic and belief noise changes the root. If the root changes, the tree needs group-level belief drivers (more stage-1 branches).
- **Full-scale MILP time.** It is unproven at 640 binaries and ≈80k columns. The subtree fallback keeps the comparison like-for-like.
- **Rank-rule tree size.** The LP grows to ≈70–90k columns. If 10–90 s per LP is missed, cohort-basket recourse at stage 1 is the next reduction.
- **ADR-39 governance.** Whether planned red-tier sales in Amber are allowed is an IC choice. The frontier shows its value; the model must not decide it.

---

## 9. Reproduction

All in `examples/mpo_v2/review_checks/`. SYNTHETIC; Python at `.venv\Scripts\python.exe`.
- `check_objective.py`: C1, C2 and C3, in about 30 s. Output in `check_objective_output.txt`.
- `milp_pilot.py [time_limit_s]`: P1, about 12 minutes including the 400 bound LPs. Output in `milp_pilot_output.txt`.
- `optimism_check.py`: P2, about 2 minutes. It imports `milp_pilot.py` from the same folder. Output in `optimism_check_output.txt`.
