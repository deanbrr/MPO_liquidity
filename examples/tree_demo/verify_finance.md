# Finance sanity review: multi-period tree demo (SYNTHETIC)

> **SYNTHETIC.** This review checks `results.json` and `RESULTS.md` in this folder. Every number here is computed from the demo's synthetic parameters (`params.json`) or from re-solves of the same program. None of it is ADIC data.

Reviewer stance: a sovereign-fund CIO and CRO reading the demo cold. Question asked: are the behaviours sensible and explainable, and is anything wrong, implausible, misleading or unexplained?

Method: I read the two outputs, `params.json`, `tree_demo.py`, ARCHITECTURE.md §4.8–4.10 and §5.1–5.7, inputs §1A, and the research syntheses. I reproduced the main and no-revolver cases exactly by importing `tree_demo.py`, without editing it. I then re-solved about 30 variants: parameter overrides, a 4-stage tree, horizon-node limits, rolling re-solves at every year-1 node, and naive-rule variants. No file in `examples/` was changed apart from this report. Section 7 lists the variants.

---

## 1. Verdict

**The mechanics pass. The finance narrative is not yet safe to show a CIO or CRO.**

What works:
- The LP is correct. Duals agree with finite differences, cash is conserved, and the owner draw is paid at every node.
- Several behaviours match intuition (section 2).

Six problems would be caught in the first IC question:

1. **End-of-horizon effects.** The REFINANCE and LEVER actions at t = 2 come from cutting the tree at year 3, and so does the "0% fire sale" headline.
2. **Wrong policy behind the probabilities.** The outcome probabilities describe the static 3-year plan, not the rolling policy the demo says it runs. The rolling policy sells PE in the 55% drought branch.
3. **The 27% IC range is doing the work.** Its lower edge is treated as hard, and it drives the no-revolver fire sale, the "consent-sensitive" PE card and the $0.75bn revolver value. At a 20% edge the revolver is worth less than its fee.
4. **The naive-rule gap is caused by the IC range.** The naive rule fire-sells PE only because it may not sell equities below the band. Allowed to, it beats the optimizer on certainty equivalent and on CVaR, with zero fire sales.
5. **Mislabelled actions.** Revolver draws that pay for equity purchases are labelled REFINANCE. By the user's definitions they are LEVER.
6. **Cash at the hard floor.** The plan holds Treasury at the 4% floor (CFP-Red) in 79% of t = 2 states and levers there. The 8% elastic target is not modelled.

## 2. What reads well (keep)

- **Root, drought.** The program sells $8.21bn of the liquid book and holds PE. Cash ends at 13.1% of NAV, which pre-funds next year's draw. The research's first-year liquid-book need from today's state is about $8.5bn. A 4-stage tree gives the same root decision, so this decision does not depend on the horizon.
- **Second crisis year (D>C>C).** Funding comes in cost order: revolver to its 50% crisis cap (SOFR + 85bp), then P2S, then the NAV loan (+440bp). No PE is sold. λ = 4.0% ≈ the NAV-loan spread, and $1 of extra revolver capacity is worth 3.5¢ (the spread gap). This matches the CFP-Red playbook (lines drawn, P2S, long-only sales before red sales).
- **λ arithmetic.** λ ≈ loan spread when a loan is the marginal dollar. It is ≈ d/(1 − d) when a PE sale is: 47.9% without the revolver.
- **Non-stress branches.** PE is held and pacing is kept in normal and drought branches of the main plan.
- **Disclosure.** RESULTS.md §6 and §10 already disclose the rolling-floor time inconsistency and the role of the IC range. The problem is that the headline sections do not carry those caveats.

## 3. Expected behaviours: scorecard

| Expected behaviour | Result | Comment |
|---|---|---|
| Normal branches: hold PE, keep pacing | Pass (static plan) | The rolling re-solve sells PE at D>D (H2) |
| Drought: sell liquid or draw the revolver before selling PE at a discount | Pass (static plan) | Fails under the rolling policy at D>D (p 0.55): $3.49bn PE sale at 15% |
| Crisis, oil weak, high draw: committed liquidity and REFINANCE before a 35% fire sale | Pass at D>C>C | In the first crisis year (D>C, D>N>C) the program sells equities at the bottom to de-risk, down to the band (M2) |
| LEVER only when liquidity is slack | **Fail** | LEVER at D>D>N, D>D>D, D>C>N with the floor binding; at D>D>D and D>C>N it is revolver-funded (H5, H6) |
| λ highest in crisis branches | **Partial** | 4.0% at D>C>C, but 0.0% at D>C and D>N>C, below drought nodes at 0.5% (M1) |
| No revolver raises λ and can flip a fund to SELL | Pass, wrong cause | λ 47.9% and root PE SELL 2.16, but the IC lower edge is the cause (H3) |
| No end-of-horizon artefacts | **Fail** | H1 |
| Parameters near the research | **Partial** | Owner draw, NAV-loan cap, PE terminal valuation, ψ = 0 (M3–M6) |
| SYNTHETIC label on all numbers | Partial | Banner only; no per-table tag (L4) |

## 4. Findings

### High

**H1. End-of-horizon effects drive the REFINANCE and LEVER plans at t = 2 and the "0% fire sale" headline.**

The pattern: every REFINANCE and LEVER action in the tree sits at t = 2, the last decision stage. At t = 0 and t = 1 the program only trades the liquid book. Horizon nodes make the final year free of consequences:
- debt is netted at face value;
- the IC range, the 50% revolver availability in C and the NAV-loan LTV cut are not enforced;
- unfunded commitments carry no cost (ψ = 0);
- PE is valued at 100% of NAV.

Evidence:
- **3-stage plan.** Revolver draws at 6 of 9 t = 2 nodes (P 59.5%), LEVER at 3 (P 50.5%), none earlier.
- **4-stage tree, same parameters.**
  - The root is unchanged (SELL 8.21).
  - At t = 2, revolver draws fall to P 23.2% and LEVER to P 20.3%.
  - Both reappear at the new last stage (t = 3: revolver 44.0%, LEVER 23.9%).
  - PE fire sales at the 35% discount appear at t = 3 with P 6.5%; the 3-year plan reports 0.0%.
- **Horizon nodes.**
  - Settlement sales of up to $18.6bn push the liquid share below the 27% IC edge in 25.6% of terminal probability, and below 20% in 7.7%.
  - Worst leaf, D>C>C>C: liquid 10.4% of NAV; debt $8.8bn (revolver at its crisis cap plus the NAV loan); (PE + yield + unfunded)/NAV 1.11; NAV −46%.
- **IC lower edge also enforced at horizon nodes.**
  - The root becomes SELL 8.49 liquid + SELL 6.88 PE.
  - P(any PE sale) is 100% and P(fire sale) 2.4%.
  - LEVER disappears (0%), and CE falls by $1.70bn.

Why it matters: a CRO will read "lever in the drought on the revolver" and "never fire-sell PE" as policy. Both come from the 3-year cut-off. The plan ends in states from which year 4 needs PE sales.

Fix:
- Add terminal conditions at horizon nodes. Two options:
  - the Tier-1A rows plus the IC range, or a next-year coverage reserve (draw + net calls);
  - the leaf regime's revolver availability and LTV, with forced paydowns.
- Use a stated ψ > 0 and haircut PE in crisis leaves.
- Alternatively, extend the tree and report only actions at t ≤ H − 2 as policy.
- Report horizon-node balance sheets beside W~: liquid share, LR8, debt and NAV drawdown.
- State in RESULTS.md that actions at t = 2 depend on the horizon.

**H2. The outcome probabilities describe the static plan, not the rolling policy the demo says it executes.**

Evidence:
- RESULTS.md §1 says only the root is executed and the rest is re-optimized each year. Yet the key results and §3 report P(any PE sale) = 0.0% and P(fire sale) = 0.0% for the static plan.
- **Re-solve at D>D (p 0.55).** The rolling policy sells $3.49bn of PE at the 15% drought discount (a $0.52bn loss) while holding 12.6% of NAV in cash. It does so because the CVaR floor is re-imposed on the new window. Without the floor there is no root PE sale at D>D, but a 6% fire-sale probability remains in the new window.
- **Re-solve at D>C (p 0.15).** The floor cannot be met, so the program enters recovery mode and drops it. The re-solved tree then has a 21.3% conditional probability of a PE fire sale at the crisis discount within three years.
- So the policy that actually runs sells PE with probability of at least 55% in year 2.

Why it matters: the user asked for probabilities of outcomes, and these are not the outcomes of the policy that would run.

Fix:
- Simulate the closed-loop policy on the tree: re-solve at every t = 1 and t = 2 node on a rolling window and execute the first decision.
- Report its P(PE sale), P(fire sale), CE and CVaR next to the static plan.
- Put the D>D PE sale in the key results, or retitle the outcome table "static 3-year plan".

**H3. The hard 27% IC lower edge, not liquidity, drives the no-revolver fire sale, the Phase I deficit and the $0.75bn revolver value.**

Evidence:
- A band edge binds at 11 of 13 decision nodes.
- **No-revolver D>C>C.** PE is sold at a 35% discount while $26.7bn of physical equities plus $5bn of synthetic exposure remain. The largest shadow price at the node is the IC lower edge (36¢ per $1), above the cash floor (34¢).
- **Phase I (no revolver).** u* = $0.247bn with the band, and u* = 0 without its lower edge: no PE sale is needed.
- **Revolver value in certainty equivalent (CE):**

  | IC lower edge | Revolver CE value | P(PE fire sale), no revolver |
  |---|---|---|
  | 27% (demo) | $0.755bn | 6% |
  | 24% | $0.089bn | 6% |
  | 20% | −$0.063bn | 0% |
  | Waived in crisis nodes | −$0.052bn (only the undrawn fee remains) | 0% |

- The research's CFP playbook (GROUPS §2.4; ARCHITECTURE §4.9) puts "lines drawn; P2S and long-only sales; amber sales" at event-Red and red-tier (PE) sales only at Black. The hard band reverses that order.

Why it matters: the consent story ("sign the revolver or fire-sell PE"; "the PE card is consent-sensitive") is a property of a synthetic allocation band, not of the fund's liquidity. A CIO would breach a soft IC range before selling PE at 35%.

Fix:
- Make the range elastic: a priced breach, or waived in event-Red and crisis nodes as the playbook does.
- Remove its cause, the market timing in M2.
- Show the headline numbers at 27%, 24% and 20%.
- In Phase I, report IC-range shortfalls separately from Tier-1A rows. The architecture's Phase I tiers contain no allocation range.

**H4. The naive-rule comparison misattributes the fire sales. A naive rule allowed to sell equities below the band beats the optimizer.**

Evidence:
- The naive rule may not sell liquid below 27% of NAV, so whenever the band blocks it, it sells PE: D>C 1.47, D>D>C 6.26, D>C>D 1.81, D>C>C 19.60.
- Re-run with the lower edge waived (upper edge kept, same 8.47% cash target, still never borrows):

  | | Naive, lower edge waived | Optimizer (demo) |
  |---|---|---|
  | CE | $210.62bn | $210.46bn |
  | CVaR10% | −3.64%/yr | −3.90%/yr |
  | P(fire sale) | 0% | 0% (the demo's naive rule: 23.2%) |

  The waived rule sits below the lower edge on 6 crisis-path nodes (P 26.3%).
- About half of the headline +$1.57bn is revolver access that the naive rule cannot use: R1 − R0 = $0.76bn.

Why it matters: the key-results line "The naive rule (sell liquid first, never borrow) fire-sells PE with probability 23.2%" implies the fire sales come from not borrowing and having no foresight. They come from the hard band. A CIO who tests the simple rule will find it is better.

Fix:
- Add a soft-band naive column and a "naive + revolver first" column.
- Decompose +$1.57bn into revolver access (≈ $0.76bn) and optimization (≈ $0.81bn).
- Rewrite the bullet.

**H5. Revolver draws that fund equity purchases are labelled REFINANCE. By the user's definitions they are LEVER.**

Evidence:
- `labels_for()` labels every revolver draw "REFINANCE (revolver)", whatever it pays for.
- **D>D>D (p 0.30).** Opening cash is $8.90bn, posted margin $0.25bn and the floor $7.03bn. Without the $3.00bn purchase, no draw would be needed, so the $1.38bn draw pays for the purchase.
- **D>C>N.** $6.31bn of the $6.35bn draw pays for the $6.30bn purchase.
- User-confirmed definitions (inputs §1A; ARCHITECTURE §4.8): REFINANCE raises cash against a holding without selling it; LEVER borrows to add exposure; "Only borrowing that funds new exposure is LEVER".

Why it matters: this is the user's own vocabulary, and the tree contradicts it at the node with the highest t = 2 probability.

Fix:
- In `labels_for()`, split each draw into a purchase-funding part (LEVER) and a part that funds the floor or the draw (REFINANCE).
- Add the exposure-delta test the architecture requires (§4.8, JE-MF9).

**H6. The plan runs Treasury at the 4% hard floor in most t = 2 states and levers there. The 8% elastic target and the CFP stages are missing.**

Evidence:
- **Treasury/NAV after decisions.**
  - 4.0–4.4% at every t = 2 node except D>N>N (79% of t = 2 probability).
  - 4.5% at D>N, the normal year-1 branch, where the program spends the root's buffer on $14.77bn of equities.
- On the architecture's CFP event indicator these readings are Red, at the Black threshold. The bands are: Green ≥ 8%, Amber 6–8%, Red 4–6%, Black < 4%.
- **LEVER while cash is tight.** LEVER happens at D>D>N, D>D>D and D>C>N with the floor binding. At D>D>D and D>C>N the revolver is also drawn.
- RESULTS.md says "a binding cash floor alone is not a stress signal".
- **What the architecture says.**
  - T2 is 8% elastic / 4% hard, restored within 4 quarters (§5.2).
  - §4.10: leverage is "a liquidity and implementation tool, not a route to 10%", and the aggregate book's α* = r_f − c < 0.
  - Levering to the $5bn synthetic cap in a drought while behind target resembles the gambling-detector signature (§5.2).

Fix:
- Model the 8% elastic target as a priced shortfall.
- Print Treasury/NAV and the CFP band at every node.
- Block LEVER and borrowed purchases below Amber, then re-check the "LEVER only when slack" behaviour.

### Medium

**M1. λ is not highest in the crisis branches, and λ = 0 in the first crisis year is unexplained.**

Evidence:
- λ = 0.0% at D>C (p 0.15) and at D>N>C, while drought nodes read about 0.5%.
- At D>C the floor is slack by only $0.08bn, because the IC lower edge, not cash, sets the sale (band shadow 5.9¢).
- The stress shows up in the state price m instead: 1.81 at D>C, 1.45 at D>N>C.
- Without the revolver, λ = 0 at D>C, D>N>C and D>C>D.
- A crisis draw of 10.1% instead of 10% makes the floor bind at D>C, draws $0.04bn on the revolver and moves λ to 0.66%.

Fix:
- Explain λ versus m in RESULTS.md.
- Flag readings within $0.5bn of a kink.
- Consider reporting the full liquidity dual mass.

**M2. The liquid book times regimes between the band edges and sells at the bottom.**

Evidence:
- At every crisis node the program sells down to the lower edge and would sell more (band shadow 5.4–7.7¢).
- D>N buys $14.77bn; D>N>C then sells $18.08bn after a −15% year.
- With the lower edge removed, it sells 100% of the liquid book at D>C ($50.8bn) and buys $31–46bn back at D>C>D and D>C>N. The demo's own calibration check shows $47.6bn.
- `params.json` says the +10% post-crisis rebound stops selling at the bottom. It does not; the band does.
- Cause:
  - next-year liquid returns depend strongly on the current regime (10.1% from N, 6.9% from D, 6.65% from C with σ 17.8%);
  - crises persist 40% of the time.
  This gives the LP a timing signal that the research finds absent out of sample (CAPE timing R² −5% to −56%).

Fix:
- Let regimes move volatility and tails more than means.
- Add scenarios per node.
- Report turnover and band-edge flags.
- Correct the rebound rationale.

**M3. The owner-draw calibration is far from the research and drives the revolver's value.**

Evidence:
- **Demo.** A 7.5% draw in D gives an expected year-1 draw of $13.1bn. There is a 15% chance of a 10% draw in year 1, and 16.8% of years draw 10% in the long run.
- **Research.**
  - 12-month draw: $9.9–10.8bn (5.6–6.1% of NAV).
  - P(2027 draw rate ≥ 9.5%) ≈ 1.2%.
  - Draw at the 5% floor above about $67 Brent and at the 10% cap only below about $23.
  - Brent is $126.55 today, with a Gulf-war state at about 0.85.
- Tying the draw to the PE exit regime (D) inverts today's configuration: an exit drought with strong oil.
- At draws of 5.5/6/8% (N/D/C), the revolver is worth $0.07bn instead of $0.755bn, and P(revolver drawn) falls to 24%.

Fix:
- Decouple the draw from the exit regime.
- Calibrate year 1 to $9.9–10.8bn.
- Model the 10% draw as an oil-collapse state with a research-consistent probability.
- Show the sensitivity.

**M4. NAV-loan capacity is 2.5–3 times the architecture's cap, and the "0% fire sale" result depends on it.**

Evidence:
- The demo allows LTV of 10% / 10% / 5% on the whole $66bn PE-like book ($6.6bn / $3.3bn). That includes $18bn of co-investment, for which single-asset REFINANCE is inadmissible (§4.8).
- The architecture caps the pledge pool at 20% of private NAV: about $2.1bn at 10% LTV, and $1.1bn credited at a 5% stressed LTV.
- With that cap, the revolver-signed plan also fire-sells PE at D>C>C (P 6%, λ 45%).
- `params.json` notes the gap; RESULTS.md does not.

Fix: use the architecture's cap, or show both results.

**M5. PE valuation is inconsistent in crisis states and flatters the tail.**

Evidence:
- **Inconsistent marks.** In a crisis year PE is marked −10% against −15% for the liquid book, because NAVs are smoothed. A buyer pays 65% of that mark. Yet horizon nodes value PE at 100% of the smoothed mark in every leaf, including the C>C leaves.
- **What the research says.** Research §4.2: risk and value use economic NAV; reported NAV is only for covenants and bids. In the demo, CVaR10% (−3.9%/yr) and the worst outcomes use stale marks.
- **Effect on behaviour.** Equities, marked to market, look riskier than PE, which favours "sell liquid, hold PE" in crises.
- **The 35% crisis discount.**
  - It is plausible for a blend that includes co-investment.
  - It is at the punitive end for fund interests: the research has 83.5% market-adjusted bids and the architecture a crisis residual of 0.80–0.84. In the demo the crisis sale price is 58.5% of pre-crisis NAV, or 68.8% market-adjusted.
  - At a 25% discount the revolver's value roughly halves, to $0.40bn.

Fix:
- Value PE on economic (de-smoothed) NAV for W~ and CVaR, or haircut PE in crisis leaves; keep reported NAV for bids.
- Label 35% as a stress case and show the 25% result.

**M6. "PACE-CUT is never chosen" comes from ψ = 0 and the 3-year window, and contradicts the research.**

Evidence:
- **With a terminal charge on unfunded commitments (ψ):**

  | ψ | Pacing cut | Root PE decision |
  |---|---|---|
  | 0 (demo) | none | HOLD |
  | 0.05 | none | SELL $1.34bn |
  | 0.10 | 100% of the $5bn plan at all 9 t = 2 nodes | SELL $5.42bn |
  | 0.20 | 100% at all 13 decision nodes | SELL |

- Cuts are all-or-nothing. The research corridor is Amber 0.25–0.5× with a protected 25% core sleeve.
- The research calls pacing the most effective single lever on the red event and says it must move first and early. RESULTS.md says pacing "would only enter if the franchise cost were below" 0.5¢.

Fix:
- Estimate ψ, or state a value with a sensitivity.
- Add the corridor with its core sleeve.
- Rewrite the PACE-CUT paragraph.

**M7. The CVaR floor was tuned to bind for display, and it drives PE sales when tightened or rolled.**

Evidence:
- The floor sits just above the unconstrained tail: −3.9% against −4.13%.
- After one crisis year (p 0.15) it cannot be met (best −6.9%), and the re-solve enters structural recovery.
- At −3.0% it forces a $29.9bn PE sale at the root, 45% of the PE book.
- Rolled forward at D>D, it forces a $3.49bn PE sale while cash is 12.6% of NAV.
- Because the band blocks equity sales, PE becomes the de-risking lever.
- Calling it "Tier 1B style" invites comparison with the architecture's 10-year bands (+1% / 0% / −2%), which do not apply.

Fix:
- Present the floor as a sensitivity, not a binding limit.
- Never meet a tail row with red-tier sales without the T6 forced re-solve.
- Drop the "Tier 1B" label or explain it.

**M8. The red-event test (ADR-39) is not applied, so PE-sale risk is understated.**

Evidence:
- The demo counts a "fire sale" only when it happens in a crisis-regime node.
- Under ADR-39, a red-tier sale is a red event if any of these holds:
  - the event stage is Amber or worse;
  - IG + cash is below 8%;
  - the bid is below 0.9 times the normal bid.
- Today is event-Amber (§4.9). So the no-revolver root sale (P 100%) and the D>D re-solve sale are red events. The no-revolver column's "6.0%" would read 100% as a red-event probability.
- §5.4 holds root red-tier SELL columns at zero in Phase II and prices them only by forced re-solve.

Fix:
- Add P(red event) to the outcome table.
- Hold root red-tier SELL at zero and show its forced re-solve.

**M9. The headline numbers are single points and fragile, and there is no sensitivity table.**

Evidence (section 5):
- The revolver's value ranges from −$0.17bn to $0.97bn across the variants.
- The root decision flips to HOLD (crisis persistence 0.25, or a 20% band) or to a $13.6bn PE sale (no post-crisis rebound).
- The "0% fire sale" result flips with the NAV-loan cap or a 4-year tree.

This is the direct answer to the user's worry about subjectivity. The solve is objective, but the answer moves with a handful of human-set inputs, and the page should name them.

Fix: put the section 5 table in RESULTS.md, with the owner of each input.

### Low

- **L1. Crisis persistence.** 0.40 (a mean spell of 20 months) is above the research's 6–18-month crisis dwell. At 0.25 the root holds instead of selling, CVaR improves to −2.2%/yr, and the revolver is worth $0.33bn.
- **L2. Yield book has no levers.** The $40bn yield book is held with no decisions. The recourse waterfall skips amber sales (private credit loans at 0.85–0.99 of par, LP interests at 89%, evergreen tenders about 38% filled) and the SMA run-off (about $0.8–0.9bn a year), and goes straight from loans to PE.
- **L3. Terminal risk metrics are missing.** Only W~ is shown, and it counts the draws paid. Balance-sheet NAV ends below 80% of $177bn with P 16.2% (worst −46%). (Private NAV + unfunded)/NAV exceeds 0.80 (the architecture's LR8 default) in 25.6% of terminal probability. Neither is reported.
- **L4. SYNTHETIC labelling.** The label sits only at the top of RESULTS.md and in `results.json` meta. Tables and headline sentences ($0.75bn, $1.57bn, 32.2%) carry no tag. The research tags every table "SYNTHETIC – NOT ADIC DATA".
- **L5. P(≥ 10%/yr) is coarse.** It is 32.2% in every policy column because, on 27 leaves, the regime path alone decides it. Leaf masses range from 0.4% to 16.6%, so probabilities are coarse. RESULTS.md should say so.
- **L6. Naive 4% column breaches the band.** It breaches the IC upper edge at D>N (38.0%) and D>N>N (40.0%). The text says the naive rule has "0 breaches", which holds only for the 8.5% column.
- **L7. Flat synthetic financing and covenant risk.** Synthetic financing is 60bp in every regime, whereas the research has about 30bp on average, 81bp at the June-2026 roll and 175bp in stress. Crisis P2S and LEVER are therefore under-costed. Revolver availability at D>C>C also assumes covenant headroom after a 33% NAV fall; in 2008–09 about a third of loans breached a covenant.

## 5. Sensitivity of the headline numbers (re-solves, SYNTHETIC)

R1 = revolver signed; R0 = no revolver. CE values are exact CRRA(3) certainty equivalents, in $bn.

| Variant (one change from the demo) | Revolver CE value | R1: P(PE sale) / P(fire sale) | R0: P(PE sale) / P(fire sale) | R1 root decision |
|---|---|---|---|---|
| Demo as published | 0.755 | 0% / 0% | 100% / 6% | SELL 8.21 liquid |
| IC lower edge 24% | 0.089 | 0% / 0% | 6% / 6% | SELL 2.41 liquid |
| IC lower edge 20% | −0.063 | 0% / 0% | 0% / 0% | HOLD |
| IC lower edge waived in crisis nodes | −0.052 | 0% / 0% | 0% / 0% | BUY 4.39 liquid, then sells 100% of liquid in crisis nodes |
| IC lower edge also at horizon nodes | n/a | 100% / 2.4% | n/a | SELL 8.49 liquid + SELL 6.88 PE |
| 4-stage tree (floor slack) | n/a | 6.5% / 6.5% by t = 3 | n/a | SELL 8.21 liquid |
| Owner draw D at 6% (C 10%) | 0.713 | 0% / 0% | 100% / 6% | SELL 8.21 |
| Owner draw 5.5 / 6 / 8% | 0.072 | 0% / 0% | 6% / 6% | SELL 6.37 |
| Crisis discount 25% | 0.400 | 0% / 0% | 15% / 15% | SELL 8.21 |
| Drought discount 11% | 0.568 | 0% / 0% | 100% / 6% | SELL 8.21 |
| Crisis persistence 0.25 | 0.332 | 0% / 0% | 3.7% / 3.7% | HOLD |
| NAV-loan capacity at the architecture cap | 0.970 | 6% / 6% | 100% / 6% | SELL 8.21 |
| No post-crisis rebound | −0.170 | 100% / 0% | 100% / 0% | SELL 8.76 liquid + SELL 13.59 PE |
| ψ = 0.10 | n/a | 100% / 0% (+ PACE-CUT 100% at t = 2) | 100% | SELL 8.43 liquid + SELL 5.42 PE |
| No CVaR floor | 0.384 | 0% / 0% | 6% / 6% | SELL 4.41 |
| Naive rule, lower edge waived | n/a | CE 210.62 vs optimizer 210.46; CVaR −3.64% vs −3.90%; P(fire) 0% | | |

## 6. Parameters against the research

| Parameter | Demo | Research or architecture | Reading |
|---|---|---|---|
| Owner draw D / C | 7.5% / 10% | 12-month draw 5.6–6.1% ($9.9–10.8bn); P(2027 ≥ 9.5%) ≈ 1.2%; 10% only below ≈ $23 Brent | Far (M3) |
| D → C | 15% | P(stress within 12 months) 13–35% | In range for market stress, not for oil-weak 10% draws |
| C → C | 40% (mean 20 months) | Crisis dwell 6–18 months | Slightly long (L1) |
| PE distributions N / D / C | 18 / 9 / 4% | 17–24% (2017–20); 9% (H1-2026) | OK; crisis milder than T4′ |
| PE calls N / D / C | 30 / 28 / 35% | 28% base; ×1.29–1.38 under stress | OK |
| Secondary discount N / D / C | 8 / 15 / 35% | H1-2026 (a drought): LP portfolios 87%, buyout 91%; co-investment 71–79% / 56–65%; crisis 61% of stale NAV, 83.5% market-adjusted; crisis residual 0.80–0.84 | N low for a blend; D OK for a blend; C punitive for funds (M5) |
| NAV loan | 10 / 10 / 5% of $66bn; +300 / 350 / 440bp | +300bp (250–400), +140bp in stress; pledge pool ≤ 20% of private NAV (≈ $2.1bn / $1.1bn) | Spread OK; capacity 2.5–3× (M4) |
| Revolver | $15bn; +85bp drawn; 15bp undrawn; 50% in C | PIF $15bn precedent; +85bp; ≤ 50% credit under the joint stress | OK |
| Synthetic financing | 60bp flat | ≈ 30bp average; 81bp (June 2026); 175bp stress | Flat (L7) |
| Pacing plan / c^PACE | $5bn / 8.6¢ | $5.34bn sealed pace / 8.6¢ (5.6–12.3¢) | OK, but ψ = 0 (M6) |
| Unfunded | $18bn | Census v1.1 PE $16.4bn, plus secondaries and co-investment | OK |
| Cash floor | 4% hard | T2: 8% elastic, 4% hard | 8% missing (H6) |
| CVaR floor | −3.9%/yr over 3 years | Tier-1B bands on the 10-year TWR: +1 / 0 / −2% | Display device (M7) |
| Returns | Liquid 14 / 9 / −15 (+10 rebound); PE 14 / 7 / −10 (+5) | CMAs: ACWI 7.5%, PE 9.6%, HF 6.7% | Long-run means (≈ 7.4% / 7.6%) OK; regime predictability strong (M2) |

## 7. How the checks were run

- `tree_demo.py` was imported unchanged, and its own `build_tree`, `build_lp`, `extract`, `summarize`, `simulate_naive` and `run_phase1` were used. HiGHS dual simplex was the solver.
- The main and no-revolver cases reproduce `results.json` exactly (CE 210.456 and 209.702).
- **Variants.** Each changes one value in `params.json` (as listed in section 5), plus four structural changes:
  - a 4-stage tree (`decision_stages` = 4);
  - the IC lower edge added at horizon nodes;
  - the IC lower edge released in crisis-regime nodes;
  - rolling 3-year re-solves at D>N, D>D and D>C, with and without the floor.
- **Naive variants.** `simulate_naive` was run with the lower edge set to `None` and the upper edge kept.
- The scripts are in the session scratchpad and may not persist:
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\analyze2.py`
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\analyze3.py`
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\analyze4.py`
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\analyze5.py`
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\analyze6.py`

  The variant list above is enough to rebuild them.
