# Finance review: MPO v2 prototype (SYNTHETIC)

> **SYNTHETIC – NOT ADIC DATA.** This review checks `RESULTS.md` and `results.json` in this folder. Every number below comes from the prototype's synthetic book, scenarios and sealed truth (`params.json`), or from re-runs of the prototype's own simulator on the same paths. None of it is ADIC data, and nothing here is a recommendation.

Reviewer stance: a sovereign-fund CIO and CRO reading the results cold.

Questions asked:
- Is the change list sensible and explainable, holding by holding?
- Is the value-add real out of sample, or does it come from in-sample optimism, end-of-horizon effects, hard limits or mislabelled actions?
- Does the max-P(goal) solution gamble, and does the bPOE solution avoid it?
- Are the parameters consistent with the research?
- What would an IC challenge first?

Method:
- **Read.** RESULTS.md, results.json, run_log.txt and params.json. The code that decides the answers: `model.py` (ledger and rows), `policy.py` (R1 labels, cards), `sim.py`, `optim.py` (switch-offs), `book.py` (truth), `prep.py` and `scenarios.py`. Research: SYN §4.4–4.6, §4.9 and L9; LIT §3.9; DSGO §5.5 and §6.5. Lessons: the tree demo's verify_finance.md.
- **Reproduced.** I rebuilt the headline world with the prototype's own modules and reconstructed O1's root decision from results.json. No project file was edited, bytecode writing was off and nothing was written into the project folder. The rebuild reproduces the published certification exactly: B0 42.91%, O1 (rule recourse) 46.90%, CVaR10 −8.25%, value at equal tail +2.85pp.
- **Static counterfactuals** on the same 10,000 certification paths: O1 with one line removed or reset, and the status quo with one line added. These measure what each line contributes to the policy that is actually certified. The published switch-offs re-solve the LP, which answers a different question.
- **Sharpe replays.** The certification was replayed with the opportunistic book's true Sharpe set to the prior mean (0.30) and to 0.
- **Replication books.** I re-solved and re-certified the four replication books and the placebo exactly as `tasks.run_book` does; their first 4,000 paths reproduce the published figures exactly. I then extended each to 10,000 paths and ran three opportunistic Sharpes: the book's own draw, 0.30 and 0.
- **Other checks.** A per-world split (M1/M2/M6), distribution shape, the fund's equity beta and an overlay stress check.

---

## 1. Verdict

**The core of the t0 change list is explainable and adds a real but modest amount out of sample. The headline would not survive an IC:**
- About 40% of the +2.9pp value at equal tail comes from a lucky synthetic draw that sizes one capped line.
- The multi-period plan adds nothing.
- The tail guard holds only inside the LP's own ledger.
- Eleven of the 24 rows add nothing measurable out of sample.

What holds:
- O1 beats the status quo out of sample in every book and every CMA world: +2.0 to +4.0pp of P(goal) across five books, and +3.9 to +4.2pp in each of M1, M2 and M6.
- With the opportunistic draw neutralized (Sharpe 0.30), value at equal tail is about **+1.2pp** across five books (range +0.5 to +1.7pp; clustered p = 0.002 against zero). That is value that synthetic beta alone cannot buy.
- That value comes from a few t0 trades that can be explained: hedge-fund redemptions recycled into beta and long-only, and the RA-02 redemption.

What an IC would catch:
1. **The headline value at equal tail rests on one line and one draw (critical, F1).**
   - Raising opportunistic IM from $1.0bn to its $1.5bn cap contributes 1.46pp of the 2.85pp in the headline book.
   - That figure is scored against a sealed truth whose opportunistic Sharpe (0.67) is 1.5 sd above the prior (0.30).
   - The placebo book reuses the same seed and draws the same Sharpe, which is why H7 fails.
   - Tested as pre-registered (clustered by book), H6 is not established at its +1pp margin.
2. **Pacing is worth nothing, and its −11.9pp attribution is a Phase I artefact (high, F2).**
   - Holding every commitment budget at plan changes O1's out-of-sample P(goal) by −0.02pp.
   - The plan raises PE above plan and cuts Secondaries and Capital Solutions in Amber. The research rule does the opposite.
3. **The year-1 contingent plans destroy value and carry a gambling signature (high, F3).**
   - With its own playbook, O1 scores 44.4% against 46.9% when held static. Its value at equal tail averages −0.2pp across books (range −0.7 to +0.6pp).
   - Leverage rises after a loss in 2.7% of path-years, above A14's 1% threshold. A14 was run only on the static variant.
4. **The tail guard holds only in the LP's ledger (high, F4).**
   - On the same 210 tree paths, the quarterly simulator puts O1's CVaR10 1.0–1.4pp below B0's. Out of sample it is 1.5pp below, and CVaR1 is 4.2pp below.
   - The LP accrues owner draws at the status quo's return. That flatters a levered plan's bad leaves.
5. **The opportunistic book is the largest new tail risk and breaks the research's overlay rules (high, F5).**
   - In the worst 1% of equity years it loses $9.1bn on average at $1.5bn IM, while the tail ladder pays $1.0bn.
6. **The $13.9bn of hedge-fund redemptions rests on a prior the research calls incomplete (high, F6).**
   - The model has zero alpha and no put-writing baseline. Every redemption sits within 0.26–0.58pp of its hurdle.
7. **Eleven rows add nothing, and most large rows are corner solutions (medium, F7 and F8).**
   - The five PACE rows, the two TRS and the term loan are worth nothing. The three Private Credit rows are worth about zero: removing them changes P(goal) by +0.04pp.
   - A four-line rule reaches 94% of O1's raw uplift and 88% of its value at equal tail.

**The headline, restated** (SYNTHETIC; 10,000 paths per book unless noted):

| Measure | As published | Restated by this review |
|---|---|---|
| P(goal) uplift vs status quo | +4.0pp (headline book) | +2.0 to +4.0pp across five books, mean +2.9pp |
| Value at equal tail (H6) | +2.9pp, ESTABLISHED | +1.4pp mean over five books at their own draws (p = 0.21 vs the +1pp margin); **+1.2pp** with the opportunistic Sharpe at its prior mean (p = 0.17 vs +1pp; p = 0.002 vs 0); about +0.9pp without the opportunistic upsizing |
| Where the value comes from | PACE −11.9pp, HEDGE −2.8, REBALANCE −2.2, REDEEM −0.8 | Opportunistic upsizing: +1.9pp raw, +1.5pp at equal tail at the headline draw, about +0.3pp at the prior. Hedge-fund redemptions and long-only adds: about +1.6pp raw, about +0.8pp at equal tail. RA-02: +0.2pp. Pacing, TRS, term loan and PC trades: about 0 |
| Multi-period plan | Year-1 contingent plans in §3 | Value at equal tail −0.2pp on average across books; leverage rises after a loss in 2.7% of path-years, above the 1% A14 threshold |
| Tail vs status quo | Depth guard holds (CVaR10 −6.2% vs −7.1%) | Out of sample CVaR10 −8.25% vs −6.79%; CVaR1 −20.9% vs −16.6%; P95 drawdown 53.8% vs 48.9% |
| Optimism gap (O1) | −0.2pp | +2.3pp like for like (tree 46.7% vs its own playbook 44.4%); mean TWR uplift +1.18pp in the tree vs +0.52pp out of sample |

---

## 2. What reads well (keep)

**Most of the tree demo's lessons were absorbed.**
- Owner draw: the 2027 draw is 5.75%, about $10.2bn, inside the research's $9.9–10.8bn.
- Crisis dwell is 10 months.
- The NAV facility is capped at 20% of private NAV.
- Facility parity holds for every baseline.
- Fan years are constraint nodes, with terminal liquidity enforced (H15).
- Stage-2 decisions are recourse only.
- Root red-tier sales are held at zero under ADR-39 and shown only by forced re-solve.
- Regime equity shifts are centred, so there is nothing to time.
- The pacing range is wide rather than a hard IC band.

**The measurement design is the right one.** It has:
- a risk-matched beta line (B4) and value at equal tail;
- a placebo book and replication books;
- separate selection and certification path sets;
- Holm adjustment;
- an error ledger;
- determinism that I could reproduce exactly.

**Some disclosures are honest:**
- "Beta is risk budget, not value".
- H3 and H4 are reported as not met.
- The PACE row is flagged as needing a Phase I allowance.

**Holding-level logic that holds up:**
- RA-02 redemption: fused μ 3.4% is below cash, and the open-end queue beats a 0.667 secondary bid. Worth +0.2pp out of sample.
- Hedge funds recycled into beta and long-only: coherent inside the model, and worth +0.8pp out of sample within O1.
- LO-04 add: Treasuries and IG serve as the liquidity reserve while Treasury cash falls from $15bn to $5.1bn.
- The tail ladder sits at its research floor.
- The red-tier forced cards are presented correctly.

**Other behaviour that is right:**
- The bPOE objective avoids the threading the MILP shows in the tree: pile-up at the goal is 1.4% against 6.0%.
- REFINANCE is correctly unused at today's liquidity: ℓ is 1.8% and the red margin is a −$28.9bn cushion.

---

## 3. Scorecard

| Question | Answer | Where |
|---|---|---|
| Change list sensible, explainable holding by holding? | **Partly.** Ten rows can be explained and add value out of sample: five hedge-fund redemptions, four long-only adds, RA-02. Eight rows are worth about 0 or are unsupported: five PACE, two TRS, TERM. The three Private Credit rows are worth about 0, and PC-05 rests on a fusion artefact. Synthetic beta is risk budget. The largest value line (opportunistic) depends on a draw | §4, F2, F7, F12 |
| Value-add real out of sample? | **Yes, but about +1pp at equal tail, not +2.9pp.** It sits in the t0 trades, not the multi-period plan | F1, F3 |
| In-sample optimism? | **Yes, for the LP's own policy:** +2.3pp on P(goal), and the mean TWR uplift halves out of sample. Hidden by comparing the tree with a different policy (the rule) | F3 |
| End-of-horizon effects? | **Mostly fixed.** Three remain: pacing is set by tree constraints with no in-horizon value; draws are accrued at the status quo's return; no 10-year run (A10) | F2, F4 |
| Hard limits doing the work? | **Yes.** The binding limits are the opportunistic cap, the class cap, the per-unit trade caps, the TRS caps, the pacing floor and the $0.05bn red-sale threshold. A20 tested none of them | F8 |
| Mislabelled actions? | **Partly.** REFINANCE and LEVER follow R1. But the TRS is labelled "portable alpha", LEVER is reported gross of redemptions in flight, and node netting hides a fully drawn revolver in a crisis | F7, F11 |
| Does max-P(goal) gamble? | **In the tree, yes:** threading, with pile-up 6.0% and mean wealth $6.4bn lower. Out of sample the gamble shows up as overfitting (41.8–44.0%), not as a bimodal distribution. O2 is a heuristic with a 79% gap, not the maximizer | F10 |
| Does bPOE avoid it? | **It avoids threading, not risk-seeking.** At Φ = 0.957 the objective is close to the mean of the worst 95.7% of outcomes. The CRRA tie-break and the guards carry the safety, and the main guard leaks | F4, F10 |
| Parameters consistent with research? | **Mostly.** Five exceptions: the hedge-fund baseline, the opportunistic book, the pacing direction, the use of term debt, and draw accrual | §7 |

---

## 4. The change list, row by row

"OOS effect" is the change in O1's out-of-sample P(goal) when the row is removed (static, same paths, sealed truth). A negative number means the row helps. ±x is the 95% half-width.

| Row(s) | Verdict | OOS effect of removing it | Comment |
|---|---|---|---|
| HF-01, -02 (26%), -04, -05, -06 redeem ($13.9bn) | Explainable in the model; **prior-dependent** | −0.83pp ±0.20 (value at equal tail −0.64pp) | Each redemption is 0.26–0.58pp below its goal hurdle, and the model has no put-writing baseline (F6). The plan spends $10bn of Treasury cash at t0 against $13.2bn of hedge-fund proceeds expected within 12 months |
| LO-01 +3.95, LO-02 +1.48, LO-03 +3.36 ($8.8bn of equity) | Explainable as recycling the redemptions into beta; **mostly beta** | All four long-only adds together: −0.78pp ±0.20 (value at equal tail only −0.20pp) | LO-01 sits at its per-unit trade cap with p\* = 1.10, so it is cap-bound. Flagged `goal_driven`: the add would fail the CMA utility hurdle |
| LO-04 +3.95 (Treasuries and IG) | Sensible: a liquidity reserve | Included above | At its trade cap (p\* 1.013) |
| RA-02 redeem ($2.35bn) | **Sensible** | −0.20pp ±0.08 | Fused μ 3.4% is below SOFR. The LP pays the redemption at economic value, which is conservative; the card says "at NAV" |
| PC-02 sell ($0.74bn) | Marginal | PC trades together: +0.04pp ±0.04 | Bid 0.949 against p\* 0.943, a 0.6% edge. The card's 9.92% hurdle is a short-duration artefact (D = 1.4 years) |
| PC-05 sell ($0.74bn) | **Artefact** | (included above) | A −17.1% forward "underwritten" signal pulls fused μ from about 8.4% to 5.2%. It comes from restating an evergreen fund's since-inception underwritten IRR (F12) |
| PC_NEW buy $1.2bn | Explainable | (included above) | New loans at DRT spreads, while the PC fund commitment is cut 75%. The pair needs one sentence of explanation |
| COMMIT_PE +10%; COMMIT_SEC, CS, PC, RA −75% | **Unsupported** | Pacing at plan: −0.02pp ±0.09 | Four programmes sit at the 0.25× floor. PE above plan in Amber, and SEC and CS cut, contradict the research rule. Removing the rows is worth about 0 in the horizon; their value beyond it is assumed (F2) |
| SYNTH_BETA +$12.2bn | Risk budget (as reported) | −1.02pp ±0.22 raw; value at equal tail −0.10pp | Lowers mean TWR in M6 (F13). It is LEVER |
| TRS:HF-03 1.75, TRS:HF-02 1.30 | **Remove or relabel** | +0.08pp ±0.10 (removing helps) | Levered hedge-fund exposure, not portable alpha. HF-03 carry is negative. HF-02 is redeemed and re-bought synthetically (F7) |
| TERM borrow $6.0bn | **Remove or relabel as a bridge** | −0.09pp ±0.11 raw; value at equal tail +0.09pp | In the LP it bridges the redemption cash for one year. The certified rule holds it for five years. Against research doctrine (F7) |
| TAIL_LADDER $6.15bn (floor) | Fine | Not tested | Small next to the opportunistic book's crash loss (F5) |
| OPPORTUNISTIC +$0.5bn IM (to the $1.5bn cap) | **Largest value line; draw-dependent; breaches overlay rules** | At Sharpe 0.67: −1.87pp ±0.27 (value at equal tail −1.46pp). At 0.30: −0.87pp (−0.22pp). At 0: removing it still costs 0.30pp ±0.18 of P(goal) but gains 0.61pp at equal tail | A zero-skill short-volatility book still lifts P(goal) through dispersion, because the goal sits above the median (F1, F5, F10) |

---

## 5. Findings

### Critical

**F1. The headline value at equal tail (+2.9pp, H6 ESTABLISHED) rests on the opportunistic book and one synthetic draw. Tested as pre-registered, it is not established at the +1pp margin.**

Evidence:
- **Switch-offs.** The published HEDGE switch-off (an LP re-solve with opportunistic IM held at $1.0bn) removes 2.41pp of the 2.85pp. My static check, O1 with IM back at $1.0bn, gives:
  - P(goal) −1.87pp [−2.14, −1.60];
  - value at equal tail 2.85 → 1.39pp.

  The status quo with only the IM increase gains +1.65pp [+1.39, +1.91] of P(goal) and +1.47pp at equal tail.
- **The draw.** The headline truth draws the opportunistic Sharpe at 0.672. The prior is N(0.30, 0.25²), so that is +1.5 sd. Replayed on the same paths:
  - at 0.30, O1's value at equal tail is +1.65pp;
  - at 0, it is +1.02pp. O1 with IM at $1.0bn is then better, at +1.63pp: with no skill, the upsizing destroys value.
- **The placebo.** The placebo book reuses the headline seed (20261019), and `make_book` keeps the random stream aligned across variants. So it draws the same Sharpe, 0.672. That, not "levers that do not use the marks" in general, is the main reason H7 fails: at 0.30 the placebo's value at equal tail falls from +2.39 to +1.55pp.
- **Across books, value at equal tail tracks the opportunistic draw.** The correlation is 0.86 at 10,000 paths. The published 4,000-path values rank-correlate 0.94 with the draws.

  | Book | Sharpe draw | Value at equal tail (published, 4k paths) |
  |---|---|---|
  | 7104 | 0.150 | −0.30 |
  | 7102 | 0.181 | +0.98 |
  | 7101 | 0.417 | +1.11 |
  | 7103 | 0.558 | +1.28 |
  | Placebo | 0.672 | +2.13 |
  | Headline | 0.672 | +2.85 |
- **The pre-registered test was not run as specified.** DSGO §5.5 pre-registered H6 across K ≥ 8 books with intervals clustered by book, "so one lucky draw … cannot carry the result". The prototype tested H6 on the headline book only. Clustered over the five non-placebo books (10,000 paths each):
  - at their own draws: +1.41pp, one-sided p = 0.21 against +1pp;
  - at Sharpe 0.30: +1.24pp, p = 0.17;
  - both are positive against zero (p = 0.019 and 0.002).

Why it matters: the IC would be asked to approve a short-volatility upsizing (F5) on a number that is about 40% luck. The defensible figure is about +1.2pp, or about +0.9pp without the upsizing.

Fix:
- Test H6 as pre-registered: clustered over at least eight books, with the opportunistic Sharpe integrated over its prior or fixed at 0.30.
- Give the placebo its own seed for the opportunistic draw.
- Restate the headline and §10.
- Report the opportunistic line separately, as a risk-appetite choice with its crash loss.

### High

**F2. Pacing is worth nothing out of sample. Its −11.9pp attribution is a Phase I artefact, and the direction contradicts the research.**

Evidence:
- **Why the switch-off reads −11.9pp.** PACE is the only switch-off that is infeasible as stated. At plan pacing the tree's H9 row cannot be met, so Phase I adds an allowance and the re-solve falls back to a conservative STRETCH solution. That solution has CVaR10 −4.4%, mean TWR 7.6% and P(goal) 35.0%, which is 7.9pp below the status quo, and the status quo also paces at plan.
- **Static checks:**
  - O1 with every commitment budget at plan: −0.02pp [−0.11, +0.07].
  - Status quo with O1's pacing: −0.06pp [−0.16, +0.04].
  - With the assumed post-horizon credits (c_pace) removed from terminal wealth, O1's pacing is worth at most +0.14pp.
- **Direction against the research.** Four of five programmes sit at the 0.25× floor, and PE goes to 1.10× plan.
  - SYN §4.4 sets the Amber corridor (today's stage) at 0.25–0.5×, with a protected core sleeve.
  - Its state-contingent rule has η > 0 for PE and η < 0 for Secondaries and Capital Solutions: cut PE and add SEC and CS when liquidity is tight. The plan does the reverse.
  - The change list does not flag PE as outside the Amber corridor.
- **Unpriced beyond the horizon.**
  - The post-horizon values for SEC, RA, PC and CS (5, 3, 1 and 1c per $) are assumptions [A].
  - A10, the 10-year horizon run, was not done.
  - The certified rule holds the cut for five years, so commitments are $13.2bn lower: $4.86bn a year against $7.5bn.
- **The tree's red-event row is much harsher than the simulator.**
  - B0's tree p_red is 1.24%, above the 0.6% buffer and the 1% limit, yet its out-of-sample P(red) is 0.10%.
  - With H9 unbounded, O1's tree p_red is 67.5%, against 0.09% out of sample.
  - The tree's red-event surrogate is what makes plan pacing "infeasible".

Why it matters: pacing is the largest strategic change in the list, and §10 presents it as the main source of value. In fact it is a device for meeting tree constraints (H9, and H11 binds PE). It is worth nothing within the horizon and unpriced beyond it.

Fix:
- Drop the "where the value comes from: PACE" narrative.
- Mark the pacing rows `limit_driven`.
- Impose, or at least flag, the Amber corridor and the η signs.
- Run A10 before any pacing change.
- Source the non-PE c_pace values.
- Recalibrate the tree's H9 surrogate to the simulator's measured red events.

**F3. The multi-period part adds no value out of sample, and the year-1 contingent plans carry a gambling signature above A14's threshold.**

Evidence:
- **The playbook loses.** O1 with its own year-1 playbook scores 44.4% out of sample, against 46.9% held static. Its value at equal tail is −0.17pp in the headline book and −0.43, +0.56, −0.23 and −0.71pp in the replication books, a mean of −0.20pp. The headline policy is the t0 change list held static.
- **The optimism gap is understated.**
  - Like for like, the LP's own policy has a +2.3pp gap: tree 46.7% against 44.4% for its playbook out of sample.
  - The reported O1 gap (−0.2pp), which H5 also uses, compares the tree with a different policy, the rule.
  - The mean TWR uplift is +1.18pp in the tree and +0.52pp out of sample.
- **A14 was run on the wrong variant.**
  - The playbook raises leverage after a loss year in 2.74% of path-years, above the 1% threshold that "blocks the change list".
  - A14 was run only on the rule variant, at 0.02%. O2's playbook is at 1.73%.
- **The playbook behaves like CPPI.**
  - Synthetic beta goes to zero in both STR branches, after equity years of −13% and −29% (log excess).
  - It rises to $51–62bn in the rally branches, which is the 30% gross-overlay cap.
  - It levers into oil-weak branches: at nodes 5 and 9 (Brent $37 and $44, next draw 7.1% and 6.7%), LEVER is $19.8bn and $26.9bn.
- **On the tree's own paths, O1 barely beats B0.** Run through the quarterly simulator, O1 is +0.3pp (rule) and −0.1pp (playbook) above B0, against +3.4pp in the LP's ledger (E1). With 210 leaves this comparison is noisy, but it is the same paths.

Why it matters: §3 shows these plans as the year-1 contingencies, and the request was for a multi-period optimizer. Out of sample, the multi-period plans add nothing; the value sits in the t0 list.

Fix:
- Present §3 as non-binding guidance, or drop it.
- Run A14 on every variant shown.
- Report the like-for-like optimism gap.
- Run the rolling MPC check (E3) before claiming multi-period value.
- Consider one t0 decision plus a cushion-monotone standing rule (SYN L10).

**F4. The tail guard holds only in the LP's ledger. On identical paths and out of sample, the plan's tail is worse than the status quo's.**

Evidence:
- **LP ledger.** O1 CVaR10 −6.2% against B0 −7.1%, so the depth guard at δ = 0 holds.
- **Same 210 tree paths, quarterly simulator.** O1 −9.0% (rule) and −8.7% (playbook) against B0 −7.7%.
- **Out of sample:**

  | Measure | O1 | B0 |
  |---|---|---|
  | CVaR10 | −8.25% | −6.79% |
  | CVaR1 | −20.85% | −16.62% |
  | P95 max drawdown | 53.8% | 48.9% |
  | Excess kurtosis | 5.4 | 1.4 |
  | Skew | −0.43 | +0.05 |

  The worst 1% of five-year outcomes ends roughly $15bn lower under O1 (approximate).
- **Cause 1: draw accrual.** W̃ accrues owner draws at the static-SAA return (the Wt row in `model.py`; error E1). For a riskier plan this overstates wealth in bad leaves and understates it in good ones. A guard that compares O1's tail with B0's is therefore biased toward O1. Research L9 requires payouts to accrue at the fund's own return.
- **Cause 2: the tree carries too little tail.**
  - It carries only the factor part of the opportunistic book; 60% of the book's variance (`opp_idio_share`) exists only in the simulator.
  - Only 4 leaves sit in the 1% tail, below the 6 that A22 requires.
- RESULTS reports the SSD failure (H4) but describes it as protection that "does not fully carry". In fact the guard is not doing its job.

Why it matters: the CRO's first protection, "no worse than today in the tail", is not true of the certified plan.

Fix:
- Accrue draws at each policy's own node returns, with a fixed-point re-solve.
- Carry the opportunistic book's full variance in the tree.
- Meet A22.
- Make out-of-sample CVaR at three levels against B0 a certification gate, not just a tree row.

**F5. The opportunistic book is mis-specified against the research and is the plan's largest new tail risk.**

Evidence:
- **Modelled as a strategy-level Sharpe process.** P&L = 1.77 × IM × (Sharpe + loading 0.3 on equity surprises and −0.6 on implied-vol surprises + 60% idiosyncratic).
- **What SYN §4.6 says instead:**
  - It rejects a strategy-level Sharpe process.
  - Premia belong in the scenario engine (E), and skill is credited only if the deflated Sharpe ratio is at least 0.95.
  - It rejects P(10%) in the overlay objective.

  The LP sizes the book on the goal objective and credits the 0.30 prior with no evidence test.
- **The OV1–OV3 limits are absent.** Over 50,000 certification path-years, with IM at $1.5bn:

  | Equity years | Equity return (mean) | Opportunistic P&L, mean (P5) | Tail ladder payoff | Loss ÷ payoff |
  |---|---|---|---|---|
  | Worst 5% | about −38% | −$5.5bn (−$11.1bn) | +$1.0bn | 5.6× |
  | Worst 1% | about −52% | −$9.1bn (−$15.3bn) | +$1.0bn | 8.9× |

  OV2 caps the loss at 25% of the tail payoff.
- **It is the line that fattens O1's left tail.** With IM back at $1.0bn, excess kurtosis falls from 5.4 to 1.1 and CVaR1 improves from −20.9% to −17.7%.
- **P(goal) rewards it even with no skill.** At a true Sharpe of zero, the upsizing still raises P(goal) by 0.30pp [+0.12, +0.48], because the goal sits above the median and dispersion helps. Meanwhile it cuts value at equal tail by 0.61pp. This is the gambling incentive the research warns about (L9).
- IM sits at its cap in all six books.

Fix:
- Implement the research design: exposure templates, the variance risk premium in E, the deflated-Sharpe gate and OV1–OV3.
- Size the book outside the goal objective.
- Until then, keep IM at $1.0bn and show any upsizing as an IC risk choice, with its crash loss.

**F6. The hedge-fund redemptions ($13.9bn, the largest real value source) rest on a prior the research calls incomplete. The sealed truth cannot test it.**

Evidence:
- **No premium for hedge funds' short-volatility exposure.** Hedge-fund alpha priors are zero ("Jurek–Stafford"). The scenario engine's vol factor is a pure zero-mean surprise (`scenarios.py`, `step`). So the hedge funds' negative vol loadings (−0.15 to −0.25) carry crash risk with no premium.
- **What the research prescribes.** LIT §3.9 calls for a near-zero alpha *and a put-writing baseline*.
- **The treatment is asymmetric.** The short-vol opportunistic book earns a 0.30 Sharpe.
- **The model's returns are low against the research CMA.** Model hedge-fund expected returns are 4.0–6.0%, about +1.1pp over SOFR on average. J.P. Morgan 2027 has hedge funds at 6.7% with cash at 3.1%, so +3.6pp.
- **Every redemption is close to its hurdle (0.26–0.58pp):**
  - HF-01: 4.44% vs 4.97%
  - HF-02: 5.78% vs 6.04%
  - HF-04: 5.86% vs 6.26%
  - HF-05: 5.21% vs 5.79%
  - HF-06: 4.43% vs 4.92%

  A put-writing baseline of about 1pp would likely flip all five.
- **The sealed truth cannot test this.** It perturbs only alphas, biases, ranges, bids and the opportunistic Sharpe. It shares the factor model and the premia. The out-of-sample gain from redeeming is the model agreeing with itself, not evidence.
- **Liquidity.** Five full redemptions at once are assumed to pass through 95% within 12 months (66% in STR), with no gates or holdbacks.

Fix:
- Put the put-writing (variance) premium in E for every short-volatility exposure, hedge funds and the opportunistic book alike, and re-solve.
- Show how the redemptions change with the hedge-fund premium.
- Model the hedge-fund state machine for full-lot redemptions.

### Medium

**F7. The TRS and term-loan lines are worth nothing, the TRS is mislabelled, and both contradict research doctrine.**

Evidence:
- **Worth nothing out of sample:**

  | Removed from O1 | Change in P(goal) | Change in value at equal tail |
  |---|---|---|
  | $3.05bn hedge-fund TRS | +0.08pp [−0.02, +0.18] | — |
  | $6.0bn term loan | −0.09pp [−0.20, +0.02] | +0.09pp |
  | TRS, term loan and pacing change together | −0.04pp | — |
- **The "portable alpha" label is wrong.** The cash row pays (hedge-fund return − SOFR − 100bp) on the notional, so the TRS is levered hedge-fund exposure.
  - The HF-03 TRS has negative carry: 4.05% against 4.89%.
  - HF-02 is redeemed 26% while a TRS re-adds 37% of its original NAV at a higher cost. Net exposure rises from $3.5bn to $3.9bn.
  - HF-03 (4.05% against its 4.33% hurdle) appears to be held mainly as the TRS reference, because the TRS cap is 50% of the lot held.
- **The term loan is a bridge.** In the LP it bridges the redemption cash: it is repaid at 8 of the 10 year-1 nodes. The certified rule holds it for five years.
- **Research doctrine (SYN §4.5):**
  - "Use term debt only to fund a reserve against the cyclical part of the shortfall."
  - A hedge-fund TRS sleeve "adds no redemption liquidity and costs ≈2 months of survival".

Fix: remove both lines, or relabel them. The TRS is LEVER into hedge funds. TERM is a bridge to redemption receipts, with a repayment rule.

**F8. The large rows are corner solutions, not holding-level insights, and a four-line rule gets most of the value.**

Evidence:
- **The same corners in every book.** In all six books, O1 lands on the same corners whatever the marks say:
  - opportunistic IM at its 1.5 cap;
  - E/W at the 1.150 DRT class cap;
  - synthetic beta of $21.5–23.9bn;
  - term debt of $5.9–7.0bn;
  - SEC, RA, PC and CS pacing at the 0.25× floor.

  LO-01 and LO-04 adds sit at per-unit trade caps (p\* 1.10 and 1.013), and the TRS sits at 50%-of-lot caps.
- **The year-1 plans use the red-event threshold as an allowance.** They sell exactly $0.05bn of red-tier assets at six nodes:
  - PE at nodes 1, 3, 4, 5 and 7 (node 1 is the demand-bust crisis);
  - RA at node 6.

  $0.05bn is `red_sale_threshold` [A]; below it a sale is not a red event.
- **A20 missed the binding limits.** It relaxed only floor8, the class caps and H11, and none of those moved P(goal) by more than 0.2pp. None of the binding caps was tested, and no row is flagged `limit_driven`.
- **A four-line rule matches O1.** The rule: redeem the five hedge funds, lift synthetic beta to $22bn, buy the long-only adds, raise opportunistic IM to $1.5bn. It reaches 46.67%, 0.23pp below O1, giving 94% of the raw uplift and 88% of the value at equal tail (78% at Sharpe 0.30). The three-mark fusion adds +0.3pp.

Fix:
- Run A20 on the binding caps: the opportunistic cap, the k_sel trade caps, the TRS cap, the pacing floor, the red-sale threshold and the gross overlay.
- Add the four-line rule as a baseline; it is the bar the optimizer has to clear.
- Price sub-threshold red-tier sales, or drop the threshold.

**F9. The red-event frontier (§6) cannot show what the limit costs.**

Evidence:
- **Why every GBO point looks the same.** Every GBO frontier point is certified with the rule recourse, which discards the stage-1 and stage-2 decisions that the red limit changes. The simulator also skips planned red-tier sales. Root decisions barely move, so out-of-sample P(goal) is 46.9% at every point, while tree p_red runs from 0% to 67.5%.
- **The MILP column mixes recourse variants for the same solution.** It shows 41.8% at the 0.3% limit (rule) and 44.0% at 0.6% and 1.2% (playbook) for one O2 solution.

Fix:
- Certify each frontier point with its own playbook, with red-tier sales executed and counted.
- Use one recourse variant per column.
- Recalibrate the tree's H9 surrogate (F2).

**F10. The max-P(goal) comparison is not a maximizer, and the gambling detectors cannot see the pattern they are meant to catch.**

Evidence:
- **O2 is a heuristic.** It is a root-only MILP relaxation plus LP rounding, started from the GBO solution, with a 79% gap and a relaxation bound of 86%.
- **It shows the in-tree gambling signature:**
  - pile-up mass just above the goal of 6.0%, against 1.4% for GBO;
  - E[W̃] $6.4bn lower;
  - P(goal) 48.0% against 46.7%.

  Out of sample the threading evaporates: pile-up is 0.5–0.7% and P(goal) 41.8–44.0%. The gamble shows up as overfitting, not as a bimodal outcome.
- **Sarle's coefficient falls with kurtosis.** O1's lower "bimodality" (0.140 against B0's 0.229) reflects fatter tails (excess kurtosis 5.4), not less gambling, yet RESULTS presents it as reassurance.
- **No concentration measure is reported.** The fund's equity beta rises:
  - static: from 0.75 to 0.85 of W0;
  - realized five-year: from 0.86 to 1.04.

  Public equity beta, physical plus synthetic, goes from 22% to 35% of W0.
- **bPOE is close to risk-neutral at Φ = 0.957.** It minimizes CVaR at the 4.3% level, which is close to the mean of the worst 95.7% of outcomes. The CRRA(3) tie-break, held within 0.005 of Φ, and the guards do the risk control.

Fix:
- Label O2 a heuristic.
- Report the in-tree pile-up and the lower mean as the gambling evidence.
- Replace Sarle with explicit checks: left-tail mass, skew and kurtosis against B0, and "P(goal) up with the median flat".
- Add factor and equity-beta concentration.
- State that bPOE avoids threading, not risk-seeking.

**F11. The labels are right by rule but hide what a CRO wants to see.**

Evidence:
- **LEVER is reported gross of redemptions in flight.** The root R1 lens treats the $16.25bn of in-flight redemptions as no exposure reduction. LEVER is $19.6bn during the notice year. Net of redemptions it would be $11.5bn, and the remaining $8.2bn is bridge financing against redemption receipts.
- **E/W is reported on one basis only.** The root E/W of 1.150 uses a W that excludes the redemption receivables. Economic exposure in year 1 is about 1.14×, and about 1.04× once the redemptions settle. The simulator's leverage metrics use 1.04, so they understate year-1 exposure.
- **Node netting hides the revolver.** At the demand-bust node, the revolver is drawn to its full 50% STR availability ($5bn) with $3.1bn of term debt still outstanding, and equities are bought. The node's R1 reads LEVER 0, REFINANCE 0, because the synthetic beta cut nets against the draw.
- **REFINANCE is zero at every node.** That is correct at today's liquidity, but the user asked to see this decision dimension.

Fix:
- Report LEVER gross and net of redemptions in flight.
- Report E/W on both bases.
- Flag instrument-level revolver use in stress.
- Add one scenario that shows when REFINANCE activates (for example STR under ADR-39, or the Black stage).

**F12. The PC-05 sale comes from a fusion artefact.**

Evidence:
- **How the signal is built.** `fusion.py` defines the underwritten signal as the return needed to land exactly on the underwritten MOIC: (ln M_u − ln M_t)/(T_u − age). For a holding that has already beaten its underwriting, that is a large negative "forecast".
- **PC-05.** It is an evergreen fund given a 4-year life, so it has one year left. It has earned 16.3% against a 5.2% underwriting, so the signal is −16.5% a year (−17.1% after debiasing).
- **Effect.** The signal carries 13% weight and pulls fused μ from about 8.4% to 5.2%, below the 5.8% hurdle, which triggers the sale.
- The bid (0.997) is near NAV, so the sale costs little, but the stated reason is wrong.

Fix: treat the underwritten case as a level prior on total return rather than a required-return target. Drop it for evergreen vehicles and for holdings already past their underwritten MOIC, and add a flag.

**F13. The headline hides the goal basis and how much the CMA world matters.**

Evidence:
- **Goal basis.** P(goal) is measured on economic NAV. On reported NAV, likely the owner's basis, it is 42.2% for O1 against 38.3% for B0.
- **World dispersion.** By world, P(goal) is 35.0–38.9% in M6, 43.7–47.9% in M1 and 50.0–53.9% in M2. The CMA world moves P(goal) by about 15pp; the plan moves it by about 4pp.
- **Beta in the pessimistic world.** The synthetic-beta increment lowers mean TWR in M6 (−0.07pp), as research L9 predicts ("leverage … destroys value in the most pessimistic model").

Fix: put both NAV bases and the per-world results in the headline.

### Low

- **L1. Sign conventions conflict.** In the change list, "dP(goal) forced" is positive when removing the row hurts. In the switch-off table, negative means removing the family hurts. In the red cards, positive means forcing the sale helps. Use one convention.
- **L2. Card artefacts.** Goal hurdles of 18–30% for short-duration holdings (RA-03, RA-07, PC-03) are numerically unstable, because h divides by D of about 1 year. The cards say "redeem at NAV", but the LP pays economic value.
- **L3. Synthetic financing.** The DRT synthetic financing spread is 60bp, against 81bp at the June-2026 roll (SYN §4.5).
- **L4. Signature checks understate year-1 leverage.** The simulator's leverage excludes queued hedge-fund claims that still earn hedge-fund returns, so the G6 signatures understate year-1 exposure (see F11).
- **L5. The "solves" check cannot fail.** It passes with 16 Infeasible statuses. These are expected (rounding probes and the OFF_PACE Phase I), but the check should say so.

---

## 6. Decomposition and replication tables (SYNTHETIC)

### 6.1 Headline book, line by line

Same 10,000 certification paths and sealed truth (opportunistic Sharpe 0.672). Variants are static: the root is changed and then held, as in the certified rule recourse. "dP vs O1" is paired, with its 95% CI. Value at equal tail (VET) is measured against the published B4 line.

| Variant | P(goal) | dP vs O1 | Mean TWR | CVaR10 | CVaR1 | VET |
|---|---|---|---|---|---|---|
| Status quo B0 | 42.91% | −3.99 [−4.38, −3.60] | 8.60% | −6.79% | −16.62% | 0.00 |
| **O1, as published** | **46.90%** | — | 9.12% | −8.25% | −20.85% | **+2.85** |
| O1, opportunistic IM back to $1.0bn | 45.03% | −1.87 [−2.14, −1.60] | 8.89% | −7.75% | −17.72% | +1.39 |
| O1, synthetic beta back to $10bn | 45.88% | −1.02 [−1.24, −0.80] | 9.09% | −7.11% | −17.80% | +2.75 |
| O1, no hedge-fund redemptions | 46.07% | −0.83 [−1.03, −0.63] | 9.04% | −8.02% | −20.07% | +2.21 |
| O1, no long-only adds | 46.12% | −0.78 [−0.98, −0.58] | 9.01% | −7.54% | −19.11% | +2.65 |
| O1, no RA-02 redemption | 46.70% | −0.20 [−0.28, −0.12] | 9.07% | −8.31% | −20.87% | +2.60 |
| O1, term loan removed | 46.81% | −0.09 [−0.20, +0.02] | 9.11% | −8.03% | −20.05% | +2.94 |
| O1, pacing at plan | 46.88% | −0.02 [−0.11, +0.07] | 9.10% | −8.36% | −21.10% | +2.74 |
| O1, no PC trades (sales, PC_NEW) | 46.94% | +0.04 [0.00, +0.08] | 9.12% | −8.24% | −20.84% | +2.90 |
| O1, no hedge-fund TRS | 46.98% | +0.08 [−0.02, +0.18] | 9.12% | −8.32% | −20.48% | +2.88 |
| O1 without TRS, term loan and pacing change | 46.86% | −0.04 [−0.16, +0.08] | 9.09% | −8.30% | −20.96% | +2.77 |
| Status quo + opportunistic IM $1.5bn only | 44.56% | B0 +1.65 [+1.39, +1.91] | 8.84% | −7.06% | −18.07% | +1.47 |
| Status quo + hedge-fund redemptions + beta $22.2bn | 44.19% | B0 +1.28 [+1.06, +1.50] | 8.72% | −7.59% | −18.46% | +0.67 |
| Status quo + O1 pacing only | 42.85% | B0 −0.06 [−0.16, +0.04] | 8.62% | −6.58% | −15.88% | −0.06 |
| Four-line rule (redemptions + beta, long-only adds, opportunistic IM $1.5bn) | 46.67% | −0.23 [−0.37, −0.09] | 9.04% | −8.39% | −21.09% | +2.51 |
| Same rule with IM $1.0bn | 44.91% | −1.99 [−2.26, −1.72] | 8.81% | −8.07% | −19.17% | +1.00 |

### 6.2 Opportunistic Sharpe replays (same paths; only the book's true Sharpe changes)

| Policy | P(goal) at Sharpe 0.672 / 0.30 / 0 | Value at equal tail at 0.672 / 0.30 / 0 |
|---|---|---|
| B0 | 42.91% / 41.29% / 39.79% | 0 / 0 / 0 |
| O1 | 46.90% / 44.32% / 42.48% | +2.85 / +1.65 / +1.02 |
| O1, IM $1.0bn | 45.03% / 43.45% / 42.18% | +1.39 / +1.43 / +1.63 |
| Status quo + IM $1.5bn | 44.56% / 42.13% / — | +1.47 / +0.34 / — |
| Four-line rule | 46.67% / 44.09% / — | +2.51 / +1.28 / — |

### 6.3 Replication books (re-solved as published; 10,000 paths on seed 1031)

The first 4,000 paths reproduce the published values exactly (for example, BOOK_7101: B0 43.45%, O1 rule 45.95%, VET +1.11). Values are pp; VET is value at equal tail.

| Book | True opportunistic Sharpe | O1 − B0 | VET, own draw | VET, Sharpe 0.30 | VET, Sharpe 0 | VET at Sharpe 0.30 with IM $1.0bn | Playbook VET, own draw |
|---|---|---|---|---|---|---|---|
| Headline (cert seed 31) | 0.672 | +3.99 | +2.85 | +1.65 | +1.02 | +1.43 | −0.17 |
| BOOK_7101 | 0.417 | +2.79 | +1.34 | +1.20 | +0.30 | +0.86 | −0.43 |
| BOOK_7102 | 0.181 | +2.99 | +1.36 | +1.67 | +0.90 | +1.35 | +0.56 |
| BOOK_7103 | 0.558 | +2.98 | +1.53 | +1.20 | +0.17 | +0.79 | −0.23 |
| BOOK_7104 | 0.150 | +1.97 | −0.05 | +0.46 | −0.39 | +0.20 | −0.71 |
| **Mean of five (clustered)** | — | **+2.94** | **+1.41** (p vs +1pp 0.21) | **+1.24** (p vs +1pp 0.17; vs 0: 0.002) | +0.40 | +0.93 | −0.20 |
| Placebo (same seed as headline) | 0.672 | +3.52 | +2.39 | +1.55 | +0.63 | +1.28 | +0.18 |

All six books put opportunistic IM at 1.500 and E/W at 1.150 at the root.

### 6.4 By CMA world (headline certification paths)

| World | B0 P(goal) | O1 P(goal) | dP | dMean TWR | O1 VET (own-world line) | Beta increment's effect on mean TWR |
|---|---|---|---|---|---|---|
| M1 | 43.71% | 47.88% | +4.17 | +0.56 | +3.22 | +0.05 |
| M2 | 50.03% | 53.92% | +3.89 | +0.62 | +2.52 | +0.10 |
| M6 | 35.00% | 38.91% | +3.92 | +0.37 | +2.81 | −0.07 |

### 6.5 Distribution shape and exposure

| Policy | Skew of TWR | Excess kurtosis | Sarle coefficient | 5-year equity beta | P(TWR < 0) |
|---|---|---|---|---|---|
| B0 | +0.05 | 1.37 | 0.229 | 0.86 | 14.9% |
| O1 | −0.43 | 5.43 | 0.140 | 1.04 | 15.8% |
| O1, IM $1.0bn | +0.04 | 1.06 | 0.246 | 0.93 | 16.2% |

**Static exposures at t0** (economic $bn, status quo → O1):

| Line | Status quo | O1 |
|---|---|---|
| Long-only | 36.0 | 48.8 |
| Hedge funds | 20.0 | 6.1 (+$3.05bn TRS notional) |
| Private Credit | 13.8 | 12.3 |
| Real Assets | 16.8 | 14.5 |
| Synthetic beta | 10.0 | 22.2 |
| Treasury cash | 15.0 | 5.1 |
| Equity-beta dollars | 127.5 | 143.8 |
| Commitments a year | 7.5 | 4.86 |

---

## 7. Parameters against the research

| Parameter | Prototype | Research | Reading |
|---|---|---|---|
| Owner draw, 2027 | 6.5% prior, smoothing 0.5 → 5.75% (about $10.2bn) | $9.9–10.8bn; kinks at $67 and $23 | OK (the demo's M3 is fixed) |
| Crisis dwell | 0.70 a quarter (10 months) | 6–18 months | OK |
| NAV facility | 10% LTV (5% in STR) on ≤ 20% of private NAV; S+300 (S+440 in STR) | Same | OK (the demo's M4 is fixed) |
| Revolver | $10bn signed, +$5bn upsize; S+85; 50% available in STR | Mix B $10bn; S+85; ≤ 50% | OK |
| Synthetic financing | 30 / 60 / 175bp (BEN / DRT / STR) | ≈30bp average; 81bp at the June-2026 roll; 175bp in stress | DRT slightly low (L3) |
| Tail ladder | 90/72 put spread, 3.74% a year, floor 0.15% of NAV | Floor 0.15%, rising toward 0.5% only under conditions | OK |
| Opportunistic book | Strategy-level Sharpe; 0.30 credited; sized on the goal objective; no OV limits; idiosyncratic part missing from the tree | Templates; premia in E; skill only if DSR ≥ 0.95; P(10%) rejected for the overlay; OV1–OV3; vol budget 1.0–1.5% of NAV | **Inconsistent (F5)** |
| Hedge-fund priors | α = 0; factor betas only; vol factor has zero mean | Near-zero α plus a put-writing baseline (LIT §3.9); J.P. Morgan 2027: hedge funds 6.7%, cash 3.1% | **Baseline missing (F6)** |
| Pacing range | 0.25–1.25× in every stage | Green 0.75–1.25×; Amber 0.25–0.5× with a protected core; η > 0 for PE and CO, η < 0 for SEC and CS | **PE at 1.10× in Amber; SEC and CS move the wrong way (F2)** |
| c_pace | PE 8.6c (sourced); SEC 5c, RA 3c, PC 1c, CS 1c [A] | PE 8.6c (range 5.6–12.3c) | Non-PE values unsourced (F2) |
| Unfunded charge ψ | 3c | $0.02–0.05 | OK |
| Term debt | $6bn LEVER funding liquid purchases | Only to fund a reserve against the cyclical shortfall (SYN §4.5) | **Inconsistent (F7)** |
| Hedge-fund TRS | Receive the hedge-fund return, pay S+100, 10% independent amount, labelled portable alpha | Counts inside 1.30×; adds no redemption liquidity; costs ≈2 months of survival | Label and use (F7) |
| Leverage caps | 1.30 / 1.15 / 1.10 by class; behind cap 1 + ½(L − 1) | Economic exposure ≤ 1.30×; cushion-monotone | OK; binding at the root (F8) |
| Distribution-inclusive wealth | Draws accrued at the static-SAA return | Accrue payouts at the fund's own return (L9) | **Inconsistent (F4)** |
| Red-event threshold | $0.05bn per node [A] | ADR-39 counts any red-tier sale in Amber or worse | Gamed at stage 1 (F8) |
| CMA worlds | M1 / M2 / M6, equal weights; pooled about 8.5% | Bridge 8.84 / 10.47 / 6.06% | OK; show the per-world results (F13) |
| Hedge-fund pass-through | 1.00 / 0.95 / 0.66 within 12 months, static | State machine with gates; "notice capacity is not cash" | Simplification; five full redemptions at once (F6) |

---

## 8. What the IC will challenge first

1. **"Half your headline is one short-volatility line on a lucky draw."**
   - Prepare: value at equal tail at a neutral Sharpe across books (about +1.2pp), and without the upsizing (about +0.9pp).
   - Prepare: the crash-loss table ($9.1bn in a 1-in-100 equity year against a $1.0bn ladder payoff).
2. **"You want to shrink four private programmes to a quarter of plan for five years, and raise PE in Amber. What is that worth?"**
   - Answer: nothing within five years (−0.02pp). Beyond five years it is unpriced.
3. **"Your year-1 plans lose to holding still and lever up after losses."**
   - Prepare: drop §3 as a plan, or show the rolling MPC.
4. **"The plan's tail is worse than today's out of sample, despite your depth guard."**
   - Prepare: the draw-accrual fix and an out-of-sample tail gate.
5. **"You redeem $14bn of hedge funds on a prior with no put-writing premium, and each redemption is within 0.6pp of its hurdle."**
   - Prepare: the hedge-fund premium sensitivity.
6. **"A four-line rule gets 94% of this. What is the optimizer for?"**
   - Prepare: the optimizer's margin over the four-line rule, about +0.2pp of P(goal) and +0.3pp at equal tail (mostly the RA-02 redemption and which hedge funds to keep).
   - Also state honestly that the multi-period part currently adds nothing out of sample, and that the rule borrows O1's choice of which hedge funds to redeem.

---

## 9. How the checks were run

- **Rebuild.** The prototype's modules were imported unchanged: `world.base`, `prep.prepare`, `sim.Sim` / `run_policy`, `book.make_book` and `tasks.run_gbo`. Bytecode writing was disabled, and the project folder's file count was unchanged before and after. O1's root was reconstructed from `results.json` (`cards`, `root`, `change_list`) and reproduces the published certification exactly.
- **Scripts** (session scratchpad; they may not persist):
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\mpo2_fin\fin_sim.py`: headline decomposition, Sharpe replays, c_pace off, overlay stress, distribution shape, equity beta. Output in `fin_sim_full.txt`.
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\mpo2_fin\fin_sim2.py`: further removals and the four-line rule. Output in `fin_sim2.txt`.
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\mpo2_fin\fin_sim3.py`: the per-world split. Output in `fin_sim3.txt`.
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\mpo2_fin\fin_books.py`: replication books re-solved and certified at three Sharpes. Output in `book_<id>.txt` and `.json`.
- **Runtime.** About 45 s per headline script. About 100 s per book: three GBO LPs plus three 10,000-path certifications. The five books ran in parallel.
- **Run with** `.venv\Scripts\pythonw.exe`; `python.exe` is blocked by the machine's application-control policy.

*SYNTHETIC – NOT ADIC DATA.*
