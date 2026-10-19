# The multi-period tree, worked through (SYNTHETIC)

> **SYNTHETIC: not ADIC data and not a forecast.** Every number below is read from [`results.json`](../../examples/tree_demo/results.json) (hash `eec513b66e7a1dfb…`) and [`RESULTS.md`](../../examples/tree_demo/RESULTS.md), which `tree_demo.py` computed from the illustrative inputs in `params.json`. Money is in $bn. A node id is the path of regimes that leads to it: `D>C>C` means "start in a drought, crisis in year 1, crisis again in year 2".

**Short answer.** The core of the design is one optimization. The documents read as complicated because they also specify the governance and evidence trail around it. Given today's balance sheet, a scenario tree and a set of limits, a linear program computes three things for every node of the tree: what to do, what a dollar of liquidity is worth there, and how likely the node is. Nothing in the solve is a judgement call, and the same inputs always give the same outputs. People set the inputs and limits in advance, each with a named owner, and approve the one decision that is executed now. Agents can propose, explain and challenge, but they cannot produce or change a number.

## 1. What the tree is (SYNTHETIC)

The demo starts from the $177bn of allocation v2:
- Treasury cash, $15.0bn (Corporate Finance);
- the liquid book, $56.0bn (Public Markets);
- the PE-like book, with $66.0bn of NAV and $18.0bn unfunded (PE funds, Secondaries, Co-investment);
- a $40.0bn yield book (Private Credit, Capital Solutions, Real Assets), held without decisions in this toy.

Steps are one year. Decisions are taken at t = 0 (today), 1 and 2, and outcomes are read at t = 3. Each year falls in one of three regimes, and the regime sets that year's numbers. Today reads as D.

| Set by the regime (year 1, from today's drought) | N normal | D PE drought | C crisis with oil shock |
|---|---|---|---|
| Probability | 0.30 | 0.55 | 0.15 |
| Liquid book return | +14.3% | +9.3% | −14.7% |
| PE NAV return (reported) | +17.1% | +10.1% | −7.0% |
| PE distributions (% of NAV) / calls (% of unfunded) | 18% / 30% | 9% / 28% | 4% / 35% |
| Owner's draw (% of NAV) | 5.8% | 5.8% | 7.5% |
| Secondary bid for PE (% of NAV) | 92% | 85% | 65% |
| Revolver available (% of its $15bn) | 100% | 100% | 50% |

The owner's draw follows oil, not PE exits. Returns also depend on the previous year's regime. They are set so that next year's expected return and volatility are the same from every regime, so the tree gives the program nothing to time.

Each node has three children, with probabilities from a transition matrix. From D the next year is N, D or C with probability 0.30 / 0.55 / 0.15; from N, 0.70 / 0.20 / 0.10; from C, 0.30 / 0.40 / 0.30. A node's probability is the product along its path, so `D>C>C` = 0.15 × 0.30 = 0.045. That gives 13 decision nodes and 27 outcomes, with probabilities from 0.45% to 16.6%. Here is the decision part of the tree, with the plan at each node:

```text
t=0         t=1 (year 1 known)          t=2 (year 2 known)
                                        +-- D>N>N  p 0.210  P2S 0.64
            +-- D>N  p 0.30  SELL 1.15 -+-- D>N>D  p 0.060  SELL 6.25
            |                           +-- D>N>C  p 0.030  SELL 5.99
            |                           +-- D>D>N  p 0.165  P2S 0.44
D  p 1.00 --+-- D>D  p 0.55  SELL 6.45 -+-- D>D>D  p 0.302  SELL 6.21
BUY 0.84    |                           +-- D>D>C  p 0.083  SELL 6.18
            |                           +-- D>C>N  p 0.045  SELL 7.81, P2S 5.00, repay 6.28
            +-- D>C  p 0.15  REV 6.28 --+-- D>C>D  p 0.060  SELL 11.43, P2S 5.00, repay 6.28
                                        +-- D>C>C  p 0.045  SELL 12.71, repay 0.58

Each t=2 node branches again into N / D / C: 27 outcomes at t=3.
```

SELL and BUY trade the liquid book. P2S (physical to synthetic) is a REFINANCE: holdings are swapped for futures, which raises cash and keeps the exposure. REV and repay are Corporate Finance drawing and repaying its revolver. The PE book is HOLD at every node.

## 2. What is decided at each node, and why the rest is a contingent plan

At each of the 13 decision nodes the program sets dollar amounts for:
- **The liquid book:** SELL, BUY, or REFINANCE by P2S (up to $5bn). Synthetic LEVER is fixed at zero by the leverage doctrine, because borrowing to add beta cannot pass the LEVER test.
- **The PE book:** SELL at the regime's bid; REFINANCE with a NAV loan (10% LTV on 20% of private NAV, 5% in a crisis); or PACE-CUT, up to 75% of the year's $5bn of commitments.
- **Corporate Finance:** draw or repay the $15bn revolver, if it is signed. A draw that pays the fund's bills is REFINANCE; a draw that pays for purchases is LEVER.
- **The appetite limits:** how far to sit below the 8% Treasury target and below the 27% lower edge of the IC range for public markets. Each dollar of shortfall costs 2 cents a year, and nothing in a crisis year.

The 27 leaves only settle: they repay, rebalance and restore limits, with no new borrowing.

**Only the root decision is executed now: buy $0.84bn of the liquid book.** Treasury holds $15.0bn, 8.5% of NAV. The program keeps exactly the 8% target ($14.16bn) and invests the rest. The other 12 decision nodes are the plan for each branch: "if year 1 looks like this, do that". They matter today because a decision is only right if every branch after it can be handled. Buying $0.84bn is safe because the plan already holds an answer for a crisis year (`D>C`, p = 0.15). That answer pays the owner $13.3bn and keeps the 4% cash floor without selling PE. A one-period optimizer cannot see that.

**Re-solving as reality unfolds.** A year later (a quarter, in production) the regime is known and the balance sheet is measured. The program is then solved again on a fresh tree. This is model predictive control (MPC). The demo runs it at all 12 nodes of years 1 and 2 (RESULTS.md §5). The re-solves differ from the plan only because the window has moved a year further:
- at `D>D` the plan says SELL 6.45, and the re-solve says SELL 4.46 plus P2S 2.09;
- at `D>C` both draw $6.28bn on the revolver.

The rolling policy's certainty equivalent is within $0.002bn of the plan's. Re-solving a year-1 subtree over the same horizon reproduces the plan exactly, so the program is time-consistent. The root decision is the same in a 2-, 3- or 4-year tree (RESULTS.md §6). Plans further out are softer: where two funding mixes are worth the same, as at `D>C>N`, the plan can switch between them. That is one more reason to execute only the root.

## 3. The optimization in words and equations

**In words.** Choose the decisions at all 13 nodes to maximize the expected utility of terminal wealth over the 27 outcomes, subject to five conditions:
- the balance sheet rolls forward exactly;
- the owner is paid in full every year;
- hard limits hold at every node;
- appetite limits are breached only at their stated price;
- if the IC sets one, a CVaR floor on bad outcomes holds.

```text
States at node n, after its decisions:
  C cash   L liquid book   X synthetic (P2S)   P PE NAV   U unfunded   Y yield book   BR revolver   BN NAV loan
Transition from the parent p (n's regime sets the year's rates):
  L_n = (1 + rL_n) L_p − sell_n + buy_n − p2s_n + unwind_n
  X_n = X_p + p2s_n − unwind_n
  P_n = (1 + rP_n − δ_n) P_p + q_n U_p − sellPE_n
  U_n = (1 − q_n) U_p + (5 − cut_p) − 0.27 sellPE_n
Cash balance (the owner's draw d_n NAV_p is a fixed outflow; no variable can reduce it):
  C_n = (1 + r) C_p + δ_n P_p − q_n U_p + y_n Y_p − d_n NAV_p − interest, fees and margin on BR, BN, X
        + (1 − τ)(sell_n + p2s_n) − (1 + τ)(buy_n + unwind_n) + (1 − disc_n) sellPE_n + ΔBR_n + ΔBN_n
Hard limits, every node:
  C_n ≥ 0.04 NAV_n    BR_n ≤ avail_n × 15    BN_n ≤ LTV_n × 0.20 × private NAV_n
  L_n + X_n ≤ 0.37 NAV_n    gross exposure ≤ 1.30 NAV_n    X_n ≤ 5    cut_n ≤ 3.75
Appetite limits, 2¢ per $ of shortfall per year (0 in a crisis year):
  C_n − BR_n − BN_n + s8_n ≥ 0.08 NAV_n        L_n + X_n + sb_n ≥ 0.27 NAV_n        s8_n, sb_n ≥ 0
CVaR10% floor on terminal wealth, if the IC sets one:
  η − 10 Σ_ℓ p_ℓ z_ℓ ≥ floor        z_ℓ ≥ η − W~_ℓ        z_ℓ ≥ 0
Terminal wealth at leaf ℓ (ω = 0.90 after a crisis year, else 1):
  W~_ℓ = C + L + ω P + Y − BR − BN − 0.02 U − pacing and appetite charges + owner's draws paid
Objective (10 tangent lines a_k + b_k w to the CRRA(3) utility):
  maximize Σ_ℓ p_ℓ u_ℓ    subject to    u_ℓ ≤ a_k + b_k W~_ℓ / 177    for k = 1..10
```

Five points matter:
- **The owner's draw is a liability, not a choice.** The draw is 5.8% of last year's NAV, or 7.5% in a crisis year. It sits in every cash row, and no variable can reduce it, so it is paid in full on every path: $32.7bn expected over three years.
- **The utility is concave.** CRRA with risk aversion 3 prefers a narrower spread of outcomes to a wider one with the same mean. Replacing the curve by 10 tangent lines keeps the problem linear. With 48 tangents the root decision does not move.
- **CVaR is linear** in the Rockafellar–Uryasev form: η is the 10% quantile of terminal wealth and z_ℓ the shortfall below it. The main case sets no floor, because the architecture's floors apply to 10-year windows, which a 3-year tree cannot test. (The demo's first version set a floor just above the tail so that it would bind, and review caught it.) RESULTS.md §7 shows what a floor would do if the IC set one. At −1.5% a year it costs $0.04bn of certainty equivalent. At 0% it costs $2.87bn and brings PE sales on 4.5% of paths.
- **It is an LP.** Every state is linear in the decisions, every limit is linear, and every variable is continuous. The demo has 559 columns and 816 rows and solves in milliseconds on HiGHS dual simplex. The solution is a basis, so it also gives exact duals, which are the source of λ.
- **Non-anticipativity holds by construction.** There is one decision per node, shared by every scenario that passes through it. Standing at `D>C`, the fund cannot know which year 2 is coming.

## 4. Three branches, node by node (SYNTHETIC)

How to read the tables:
- **Binding** lists the limits that bind at the node, with the price of $1 of relief.
- **λ** is the liquidity price (§5).
- **m** is the state price: today's value of $1 at the node, per unit of probability.
- **CFP stage** is the contingency-funding-plan stage: the worse of the Treasury/NAV reading and the liquid-share reading.

**Best: `D>N>N>N`, p = 0.147, +12.0% a year.**

| Node | p | Draw | Decision | Treasury / NAV, CFP stage | Binding | λ | m |
|---|---|---|---|---|---|---|---|
| D | 1.000 | – | Liquid BUY 0.84 | 8.0%, Green | 8% target, 0.7¢ | 0.68% | 1.00 |
| D>N | 0.300 | 10.3 | Liquid SELL 1.15 | 8.0%, Green | 8% target, 0.4¢ | 0.34% | 0.76 |
| D>N>N | 0.210 | 11.1 | Liquid REFINANCE 0.64 (P2S) | 8.0%, Green | 8% target, 0.3¢ | 0.28% | 0.60 |
| D>N>N>N | 0.147 | 11.7 | Settle: close the P2S, SELL 0.62 | 8.0%, Green | – | – | – |

In normal years distributions and yield roughly cover the owner's draw. The 8% target grows with NAV, though, so the program tops up Treasury every year. Here a sale and a P2S cost about the same, and the re-solves in §2 swap them at both nodes. Outcome: $248.7bn of terminal wealth with draws counted, NAV up 20%, CFP Green.

**Drought persists: `D>D>D>D`, p = 0.166 (the most likely single outcome), +8.6% a year.**

| Node | p | Draw | Decision | Treasury / NAV, CFP stage | Binding | λ | m |
|---|---|---|---|---|---|---|---|
| D>D | 0.550 | 10.3 | Liquid SELL 6.45 | 8.0%, Green | 8% target, 1.0¢ | 0.96% | 0.92 |
| D>D>D | 0.302 | 10.6 | Liquid SELL 6.21 | 8.0%, Green | 8% target, 0.4¢ | 0.40% | 0.82 |
| D>D>D>D | 0.166 | 10.9 | Settle: SELL 5.98 | 8.0%, Amber | – | – | – |

Each drought year drains about $6bn from Treasury. At `D>D` the owner draws 10.3 and PE calls 5.0, against distributions of 5.9, yield of 2.8 and interest of 0.6. The program refills Treasury from the liquid book. It sells no PE: at an 85% bid a sale loses 15 cents per dollar of NAV, against a liquidity price under 1 cent. The cost shows in the mix. The liquid share falls from 32.1% to 30.6%, 29.2% and then 27.9%. That is CFP Amber, just above the IC range's 27% edge. Outcome: $226.6bn, NAV up 8.8%.

**Crisis with an oil shock, three years running: `D>C>C>C`, p = 0.0135 (the worst outcome), −6.0% a year.**

| Node | p | Draw | Decision | Treasury / NAV, CFP stage | Binding | λ | m |
|---|---|---|---|---|---|---|---|
| D>C | 0.150 | 13.3 | CF REFINANCE 6.28 (revolver); liquid and PE HOLD | 4.0%, Red | cash floor, 0.7¢ | 0.65% | 1.47 |
| D>C>C | 0.045 | 11.3 | Liquid SELL 12.71; repay revolver 0.58 | 4.0%, Red | cash floor, 0.6¢ | 0.54% | 1.95 |
| D>C>C>C | 0.0135 | 10.1 | Settle: SELL 10.73 | 4.0%, Black | – | – | – |

Year 1 takes $14.4bn out of a Treasury that holds $14.2bn:
- liquid assets fall 14.7%;
- the owner draws $13.3bn, because oil is weak;
- PE calls $6.3bn and distributes only $2.6bn.

Before any action, cash is −$0.25bn. The program draws $6.28bn on the revolver, exactly enough to restore the 4% floor, and sells nothing at the bottom. The 8% target is free in a crisis year, so rebuilding it waits. In year 2 the program sells $12.71bn of liquid assets and trims the revolver by $0.58bn.

At the horizon the fund is in CFP Black. The liquid share is 16.0%, $5.7bn is still drawn, NAV is down 31.7% and terminal wealth is $146.9bn. The IC range is $13.3bn short, and that shortfall is charged. Yet every hard limit holds, the owner receives all $34.7bn of draws, and no PE is sold at the 65% crisis bid. Phase I shows that no mix of reversible levers could hold the IC range here: the minimum shortfall is $5.8bn.

## 5. The liquidity price λ (SYNTHETIC)

**What it is.** Each node has a cash-balance row, and its dual μ is the value of one more dollar of cash there. Part of μ, call it M, comes from the node's liquidity rows (the 4% floor and the 8% target). The rest is the value of carrying the dollar into next year. λ = M / (μ − M) is the premium of cash over its carry value: the cost of the marginal dollar of liquidity at that node.

**In dollars.** At the root λ = 0.68%, so an extra $0.5bn of Treasury cash is worth about $3.4m for the year. That is what producing it from the cheapest source left would cost: the liquid book's 0.15% trading cost, plus the return given up by holding cash instead.

At `D>C`, λ = 0.65% can be checked by hand:
- the revolver's spread is 85bp, less the 15bp undrawn fee that drawing saves: 0.70%, paid a year later;
- each extra dollar of NAV needs 4 more cents of floor;
- so λ = 0.70% × 0.96 / 1.0389 = 0.65%.

Re-solves with small cash injections confirm every node's price, to a relative error of 4.1e-10. Each price holds for at least ±$0.5bn of cash.

**Why λ does not spike in the crisis branches here, and when it does.** With the revolver signed, crisis λ is only 0.01–0.65%, because the facility caps the marginal dollar at its net cost. The crisis shows in the state price m instead: 0.60 at `D>N>N`, 1.47 at `D>C` and 1.95 at `D>C>C`. A dollar is worth most where the fund is poorest.

λ peaks at 1.76% at `D>C>D`, the drought after a crisis. There the program repays the revolver and rebuilds Treasury against three binding limits: the 8% target, the $5bn P2S budget and the IC range edge. λ sits at the cap set by the IC's own 2-cent target price.

So λ spikes when the cheapest remaining source is expensive. Suppose the IC range's lower edge were hard even in a crisis. Without the revolver, λ at `D>C>C` would then reach 23.0% (RESULTS.md §7).

**Corporate Finance's transfer price.** λ is what the internal bank should charge a group that uses liquidity in that state, and credit a group that supplies it. An extra $0.5bn for the coming year would cost:
- about $3.4m at today's price;
- $4.8m if the drought persists (`D>D`);
- $8.8m in the drought after a crisis (`D>C>D`).

In production, these node prices, compounded into a curve by tenor, are the decision prices. Corporate Finance publishes a smoothed version each quarter as the FTP curve (ARCHITECTURE.md §6.1). Groups pay the number that steers the optimizer.

**SELL or HOLD for a fund.** A fund is sold when its bid beats its reservation price. The reservation price is the fund's value to ADIC if held or refinanced, net of what the cash from a sale is worth (ARCHITECTURE.md §4.8). λ links the two: a sale at bid b brings in b(1 + λ). With λ at most 1.76%, a bid must come within about 2% of the fund's held value to clear, to first order. The best bid in the tree is 92% of NAV, so PE is held everywhere.

When λ jumps, the reservation price falls and SELL can win. In the hard-range stress:

| `D>C>C`, hard-range stress | Without the revolver | With the revolver signed |
|---|---|---|
| λ at the node | 23.0% | 1.83% |
| PE book | SELL 7.19 at the 65% crisis bid | REFINANCE 1.03 (NAV loan) |
| Corporate Finance | – | REFINANCE 7.50 (revolver) |
| P(any PE sale) / P(fire sale), whole tree | 22.2% / 13.8% | 6.5% / 4.7% |

The node and the bid are the same, and the answer is the opposite. In this stress the signed facility is worth +$0.47bn. A fund whose bid lies between the two reservation prices is what the design labels consent-sensitive.

In the main case the revolver changes only the liquid side. At `D>C` the program draws $6.28bn with the revolver, or sells $6.27bn without it. The facility is worth −$0.066bn against $0.068bn of fees, so on these inputs it does not pay for itself.

## 6. Probabilities of outcomes (SYNTHETIC)

Every leaf has a probability, so the plan comes with a full outcome table (RESULTS.md §3; returns count the owner's draws):

| Expected return | Median | P(≥ 10% a year) | P(< 0) | CVaR10% | P(PE sale) | P(red event) | P(revolver drawn) | P(CFP Red or Black) |
|---|---|---|---|---|---|---|---|---|
| 7.4% a year | 8.6% | 41.3% | 7.9% | −1.7% a year | 0.0% | 0.0% | 15.0% | 33.3% |

Treat these as illustrations, for three reasons the demo states itself:
1. **Coarse.** 27 leaves from 0.45% to 16.6% move probabilities in leaf-sized steps. P(≥ 10%) is 41.3% in all seven columns of RESULTS.md §3, because the regime path alone decides it.
2. **Thin tails.** Three branches a year understate a real book's volatility, which flatters CVaR and P(red event).
3. **Plan, not policy.** The numbers describe the static plan. The rolling policy of §2 draws the revolver on 26.2% of paths, not 15.0%.

So the production design splits the work. The tree program H gives decisions and prices. The policy simulator P runs the same ledger forward on 10,000–50,000 paths per model world, with 250,000 or importance sampling for tails below 0.5%. It runs the policy that would actually be executed: this quarter's decisions from H, then the standing policy (ARCHITECTURE.md §3.1, §4.1, §5.9). At 50,000 paths, the standard error of a 1% probability is 0.04 percentage points, against the tree's 0.45% steps.

Probabilities are certified in P, never optimized. No probability term may enter an objective, because maximizing P(≥ 10%) rewards gambling. H carries CVaR rows, whose buffers are tuned until P certifies the limits.

## 7. Optimized versus a naive rule (SYNTHETIC)

The naive rule faces the same flows, limits and charges:
- it holds the 8% target by selling liquid assets inside the IC range;
- if the floor would fail, it sells liquid assets below the range before any PE;
- it never uses a NAV loan, P2S, LEVER or a pacing cut.

| Certainty equivalent ($bn, exact CRRA 3) | No revolver | Revolver signed |
|---|---|---|
| Program | 215.012 | 214.946 |
| Naive rule at the 8% target | 214.976 | 214.903 |
| **Program's lead** | **+0.036** | **+0.043** |
| Naive rule at the 4% floor | 214.721 | – |

The program adds $36–43m of certainty equivalent over three years, about 0.6–0.7bp a year. That is small, for a clear reason. In this calibration liquidity is cheap (λ never above 1.8%), PE is never sold, and "sell liquid first, never borrow" is close to optimal.

The behaviour differs where it matters. In the first crisis year the naive rule sells $12.3bn of liquid assets at the bottom to restore 8%. The program sells $6.27bn without the revolver and nothing with it, and rebuilds after the crisis. The biggest number in the table is the buffer itself: the same rule run at the 4% floor loses $0.25bn.

The program's other gains do not show in dollars:
- its plan follows from the limits, so it changes when they do, with no rule to rewrite;
- it prices liquidity at every node;
- it values the facility (here, negatively);
- it shows which inputs would move today's decision (§9).

The naive rule was not run on the stress cases, so the demo gives no dollar figure for when liquidity is expensive.

## 8. How this scales to the production design

| | Demo | Production (ARCHITECTURE.md §5.4) |
|---|---|---|
| Time steps | 3 annual decision stages | 8 periods: four quarters, then four half-years |
| Tree | 40 nodes, 27 leaves | 24 first-quarter nodes × 4 year-end children × 6 leaf paths = 576 leaves |
| Scenarios | One transition matrix, three regimes | 12,000 simulated paths, 2,000 from each of six model worlds, pooled; nodes defined on observable features only |
| Book | 5 blocks | Eight groups, private books split young and mature: ≈42 states and ≈33 decisions per node |
| Actions | Book-level SELL / HOLD / REFINANCE / LEVER | The same, plus a card for every holding priced by its reduced cost, and a small MILP for ticket sizes |
| Limits | 4% floor, 8% target, IC range, facility caps | The same, plus 30-day coverage, 24-month survival, red-event CVaR rows by model class and 10-year floors |
| Size and time | 559 columns, milliseconds | ≈194k columns, ≈186k rows; quarterly re-solve within 120 seconds on HiGHS |
| Probabilities | From the tree | Certified in P on 10,000–50,000 paths per world |

These parts carry over unchanged:
- the transition and the cash row, with the owner's draw as a fixed outflow;
- hard limits and priced appetite limits;
- a concave utility made linear (48 tangents in production, plus a shortfall term against 10% a year);
- non-anticipativity;
- λ from the duals;
- Phase I for each consent scenario;
- red-tier sales held at zero and priced by forced re-solve;
- MPC.

Production adds size and detail, not a different method.

## 9. Where humans and AI agents come in

| People set, in advance, each with an owner | The program computes, with no judgement |
|---|---|
| Scenario models and regime probabilities (scenario engine; CRO validates) | Every decision at every node |
| Bids, spreads, LTVs and facility terms (market data; Corporate Finance) | λ and the state price at every node |
| The owner's draw rule (owner; Corporate Finance forecasts) | Which limits bind, and what each costs |
| Hard limits and appetite prices (IC); risk aversion (IC and Board) | The probability of every outcome |
| Which facilities are signed (Corporate Finance, banks, owner) | How decisions and prices change without them |
| Approval of the executed decision and of any red-tier sale | The forced re-solve that prices a sale held for approval |

**Agents never produce numbers.** An LLM may propose an idea, such as a policy rule or a stress scenario, draft text, or argue a case in the IC room. Every candidate goes to the same deterministic evaluator. A validator rejects any number an LLM writes outside an engine-filled placeholder, and AI seats state no probabilities (ARCHITECTURE.md §3.3). The agent campaign can be switched off; the quarterly loop still prices H's recommendation for the IC (§7.4).

**The same inputs give the same outputs.** The demo uses single-threaded dual simplex, a fixed seed and no sampling. A separate program written from the equations was solved with HiGHS and with CLARABEL. It reproduces the objective to 1 part in 10^10 and every decision at all 40 nodes to within a few dollars.

**On "subjective".** You are partly right. People are in the loop by design, and some inputs are judgements, not facts: risk aversion, the limits, the appetite prices and the choice of scenario models. Every optimizer needs inputs like these. This design keeps them out of the computation, makes each one explicit, gives it an owner and shows what it does.

RESULTS.md §7 changes 19 human-set inputs one at a time. Thirteen leave today's decision unchanged. The six that move it are all explicit choices of policy or valuation:
- risk aversion 5 instead of 3 (BUY 0.84 becomes SELL 8.21);
- an appetite price below 1%;
- no price on the 8% target;
- counting the target gross of facility draws;
- allowing synthetic LEVER;
- valuing crisis PE at its reported mark.

People set limits before the solve and approve after it. They cannot edit what the solve produces. Between quarters nothing executes itself: rules approved by the IC are carried out by named people.

*All figures SYNTHETIC. Sources: `examples/tree_demo/results.json`; `examples/tree_demo/RESULTS.md` §§1–8 and "Verification"; `design/ARCHITECTURE.md` §§3.1, 3.3, 4.8, 5.1–5.9, 6.1, 7.4.*
