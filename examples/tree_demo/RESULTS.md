# Multi-period tree: worked example (SYNTHETIC)

> **SYNTHETIC. Not ADIC data and not a forecast.** Every number here is computed by `tree_demo.py` from the illustrative inputs in `params.json` and read from `results.json`. Version 2: the corrections from `verify_math.md` and `verify_finance.md` are applied (section 10 lists each one).

## What this shows

One linear program turns inputs and limits into decisions. People set the inputs (scenario probabilities, returns, bids, the owner's draw rule) and the limits (the 4% cash floor, facility and leverage caps, the IC range, the prices of the two appetite limits) and approve the result. Nothing inside the solve is a judgement call. For every node of a 40-node scenario tree the program returns:

1. **what to do** with each book (SELL / HOLD / REFINANCE / LEVER / PACE-CUT, with amounts);
2. **the price of liquidity** at that node (λ, read from the LP duals);
3. **the probability** of reaching it, and so the probability of every outcome.

Start: the $177bn book (allocation v2), today read as a PE distribution **drought (D)**. Each year moves to N (normal), D (drought) or C (crisis with an oil shock, when the owner draws more). Decisions at t = 0, 1, 2; outcomes at t = 3; 1 + 3 + 9 + 27 = 40 nodes. The LP has 559 columns and 816 rows and solves in milliseconds with HiGHS. The whole run, with every check below, takes a few seconds.

**Key results (revolver signed unless stated; SYNTHETIC):**

- **Today (root, drought):** Liquid BUY 0.84. Treasury closes at 8.0% of NAV (CFP Green); λ = 0.68%. The program holds exactly the 8% own-liquidity target and puts the cash above it into the liquid book. The same root decision comes out of a 2-, 3- and 4-year tree (section 6).
- **First crisis year (D>C, p = 0.15):** CF REFINANCE 6.28 (revolver); Treasury 4.0% of NAV (CFP Red); λ = 0.65%; state price m = 1.47. It sells no equities at the bottom and no PE. Without the revolver: Liquid SELL 6.27.
- **Drought persists (D>D, p = 0.55):** Liquid SELL 6.45, restoring the 8% target; λ = 0.96%.
- **Outcomes of the plan:** expected return 7.4% a year (owner draws counted), P(≥ 10% a year) = 41.3%, CVaR10% = -1.7% a year, P(any PE sale) = 0.0%, P(red event) = 0.0%. **The rolling policy** (re-solved at all 12 nodes of years 1 and 2) reaches a certainty equivalent within $0.002bn of the static plan, with P(any PE sale) = 0.0%.
- **The signed revolver** is worth −$0.066bn of certainty equivalent here, against $0.068bn of undrawn fees over 3 years. With research-calibrated draws the fund can meet its crisis needs by selling liquid assets, so the facility does not pay for itself in this example. With v1's hard IC range it would be worth +$0.47bn (section 7). v1's $0.75bn also reflected its larger crisis draws and its downside floor.
- **Against a simple rule** (hold 8% by selling liquid first and PE last, never borrow): the program beats it by +$0.036bn when neither has a revolver (the program can also use P2S and the NAV loan), and beats the same rule with the revolver by +$0.043bn. The gaps are small because liquidity is cheap in this calibration. Here the program's value is that it finds the plan without a hand-written rule and prices liquidity at every node.

## 1. The tree and the decision at every node (revolver signed)

Each line: path (regime of each year), probability of reaching the node, opening cash / liquid / PE NAV ($bn) after that year's flows, the owner's draw paid that year, the decision (amounts in $bn; CF = Corporate Finance), Treasury / NAV after the decision with its CFP stage, λ (liquidity premium) and m (state price: today's value of $1 at that node per unit of probability). Under each year-2 node: its three outcomes at t = 3 as annualized returns, with the settlement trade if there is one.

```text
D        p=1.000 | cash  15.0 liq  56.0 PE  66.0 | Liquid BUY 0.84 | T/NAV 8.0% Green | λ 0.68% m 1.00
    D>N      p=0.300 | cash  14.1 liq  65.0 PE  70.8 | draw 10.3 | Liquid SELL 1.15 | T/NAV 8.0% Green | λ 0.34% m 0.76
    D>D      p=0.550 | cash   8.1 liq  62.1 PE  71.7 | draw 10.3 | Liquid SELL 6.45 | T/NAV 8.0% Green | λ 0.96% m 0.92
    D>C      p=0.150 | cash  -0.2 liq  48.5 PE  65.1 | draw 13.3 | CF REFINANCE 6.28 (revolver) | T/NAV 4.0% Red | λ 0.65% m 1.47
        D>N>N    p=0.210 | cash  15.5 liq  71.1 PE  72.9 | draw 11.1 | Liquid REFINANCE 0.64 (P2S) | T/NAV 8.0% Green | λ 0.28% m 0.60
            t=3 -> N: 12.0%/yr p=0.147 sells liq 0.6 | D: 10.2%/yr p=0.042 sells liq 6.5 | C: 2.6%/yr p=0.021 sells liq 12.0
        D>N>D    p=0.060 | cash   9.1 liq  67.6 PE  73.8 | draw 11.1 | Liquid SELL 6.25 | T/NAV 8.0% Green | λ 0.37% m 0.82
            t=3 -> N: 11.0%/yr p=0.018 sells liq 0.5 | D: 9.3%/yr p=0.033 sells liq 6.4 | C: 2.4%/yr p=0.009 sells liq 8.4
        D>N>C    p=0.030 | cash   0.2 liq  50.8 PE  66.0 | draw 14.3 | Liquid SELL 5.99 | T/NAV 4.0% Red | λ 0.01% m 1.36
            t=3 -> N: 4.9%/yr p=0.009 sells liq 6.1 | D: 3.6%/yr p=0.012 sells liq 6.2 | C: -2.0%/yr p=0.009 sells liq 12.0
        D>D>N    p=0.165 | cash  15.3 liq  63.6 PE  76.4 | draw 10.6 | Liquid REFINANCE 0.44 (P2S) | T/NAV 8.0% Green | λ 0.37% m 0.74
            t=3 -> N: 11.1%/yr p=0.116 | D: 9.3%/yr p=0.033 sells liq 6.0 | C: 1.8%/yr p=0.017 sells liq 7.1
        D>D>D    p=0.302 | cash   8.8 liq  60.9 PE  77.5 | draw 10.6 | Liquid SELL 6.21 | T/NAV 8.0% Green | λ 0.40% m 0.82
            t=3 -> N: 10.2%/yr p=0.091 | D: 8.6%/yr p=0.166 sells liq 6.0 | C: 1.7%/yr p=0.045 sells liq 6.1
        D>D>C    p=0.083 | cash   0.0 liq  47.5 PE  70.2 | draw 13.6 | Liquid SELL 6.18 | T/NAV 4.0% Red | λ 0.04% m 1.37
            t=3 -> N: 4.8%/yr p=0.025 sells liq 2.1 | D: 3.5%/yr p=0.033 sells liq 4.8 | C: -2.1%/yr p=0.025 sells liq 12.0
        D>C>N    p=0.045 | cash   6.9 liq  56.0 PE  69.8 | draw  8.8 | Liquid SELL 7.81 + REFINANCE 5.00 (P2S); CF REPAY revolver 6.28 | T/NAV 8.0% Amber | λ 0.41% m 1.09
            t=3 -> N: 5.9%/yr p=0.032 | D: 4.1%/yr p=0.009 sells liq 1.1 | C: -3.1%/yr p=0.004 sells liq 6.2
        D>C>D    p=0.060 | cash   1.0 liq  54.1 PE  71.7 | draw  8.8 | Liquid SELL 11.43 + REFINANCE 5.00 (P2S); CF REPAY revolver 6.28 | T/NAV 6.9% Red | λ 1.76% m 1.24
            t=3 -> N: 5.3%/yr p=0.018 | D: 3.6%/yr p=0.033 | C: -3.2%/yr p=0.009 sells liq 7.9
        D>C>C    p=0.045 | cash  -6.7 liq  45.1 PE  67.4 | draw 11.3 | Liquid SELL 12.71; CF REPAY revolver 0.58 | T/NAV 4.0% Red | λ 0.54% m 1.95
            t=3 -> N: 1.0%/yr p=0.013 | D: -0.4%/yr p=0.018 sells liq 4.1 | C: -6.0%/yr p=0.013 sells liq 10.7
```

Read across a row: the program's plan for that state of the world. Only the root's decision is executed now; the rest are contingency plans, re-solved when the year's regime is known (section 5 runs that rolling policy). Opening cash can be negative: it is cash after the year's flows (draw, calls, distributions, yield, interest) and before the node's actions. With annual steps the sales and drawings a treasurer would make during the year are booked at the node, and after them every hard limit holds at every node.

## 2. Decisions, binding limits and prices by node

| Path | p | Draw paid | Liquid | PE book | Corporate Finance | Treasury / NAV (CFP) | Binding limits (¢ per $1 of relief, at the node) | λ | m |
|---|---|---|---|---|---|---|---|---|---|
| D | 1.000 | - | BUY 0.84 | HOLD | NONE | 8.0% (Green) | 8% target (0.7¢) | 0.68% | 1.00 |
| D>N | 0.300 | 10.3 | SELL 1.15 | HOLD | NONE | 8.0% (Green) | 8% target (0.4¢) | 0.34% | 0.76 |
| D>D | 0.550 | 10.3 | SELL 6.45 | HOLD | NONE | 8.0% (Green) | 8% target (1.0¢) | 0.96% | 0.92 |
| D>C | 0.150 | 13.3 | HOLD | HOLD | REFINANCE 6.28 (revolver) | 4.0% (Red) | cash floor (0.7¢) | 0.65% | 1.47 |
| D>N>N | 0.210 | 11.1 | REFINANCE 0.64 (P2S) | HOLD | NONE | 8.0% (Green) | 8% target (0.3¢) | 0.28% | 0.60 |
| D>N>D | 0.060 | 11.1 | SELL 6.25 | HOLD | NONE | 8.0% (Green) | 8% target (0.4¢) | 0.37% | 0.82 |
| D>N>C | 0.030 | 14.3 | SELL 5.99 | HOLD | NONE | 4.0% (Red) | cash floor (0.0¢) | 0.01% | 1.36 |
| D>D>N | 0.165 | 10.6 | REFINANCE 0.44 (P2S) | HOLD | NONE | 8.0% (Green) | 8% target (0.4¢) | 0.37% | 0.74 |
| D>D>D | 0.302 | 10.6 | SELL 6.21 | HOLD | NONE | 8.0% (Green) | 8% target (0.4¢) | 0.40% | 0.82 |
| D>D>C | 0.083 | 13.6 | SELL 6.18 | HOLD | NONE | 4.0% (Red) | cash floor (0.0¢) | 0.04% | 1.37 |
| D>C>N | 0.045 | 8.8 | SELL 7.81 + REFINANCE 5.00 (P2S) | HOLD | REPAY revolver 6.28 | 8.0% (Amber) | 8% target (0.4¢); synthetic budget (0.0¢) | 0.41% | 1.09 |
| D>C>D | 0.060 | 8.8 | SELL 11.43 + REFINANCE 5.00 (P2S) | HOLD | REPAY revolver 6.28 | 6.9% (Red) | 8% target (1.9¢); synthetic budget (0.9¢); IC range (lower) (1.3¢) | 1.76% | 1.24 |
| D>C>C | 0.045 | 11.3 | SELL 12.71 | HOLD | REPAY revolver 0.58 | 4.0% (Red) | cash floor (0.6¢) | 0.54% | 1.95 |

**How to read λ and m.** λ = M/(μ − M): μ is the dual of the node's cash-balance row and M the part that comes from the node's liquidity rows (the 4% floor and the 8% target; ARCHITECTURE.md §5.6). It is the cost of the marginal dollar of liquidity at that node, roughly (1 − f)/(1 + r) × the net cost of the cheapest source still available. Where the 8% target binds and is met, the marginal dollar comes from a liquid sale: the 0.15% trading cost plus the return given up by holding cash instead of the liquid book (λ 0.28%–1.76% here, capped by the target's 2¢ price). Where a crisis year draws the revolver, it is the revolver's 85bp spread less the 15bp undrawn fee the draw saves (λ 0.65%–0.65%). The highest λ in the tree is 1.76% at D>C>D (binding there: 8% target, synthetic budget, IC range (lower)).

So λ is **not** highest in the crisis branches (crisis nodes: 0.01%–0.65%): with a signed revolver, a crisis dollar is cheap at the margin. The stress shows in m instead. m is today's value of a dollar at that node, and it is highest where wealth is lowest (D>C 1.47, D>C>C 1.95). Without the revolver, crisis λ rises (section 4). Every decision node's cash price was also measured at ± $0.5bn of cash. None sits within that distance of a kink, so each λ holds for at least that much cash.

**PACE-CUT** is available at every node, capped at 75% of the year's plan (a protected core sleeve), but it is not chosen here. Its franchise cost is 8.6¢ per $ cut, and its liquidity only arrives two quarters later. The cut column's reduced cost gives the break-even cost: the most valuable cut in the tree is at D>C, worth 3.0¢ per $. Unfunded commitments left at t = 3 carry a stated burden of 2¢ per $ (v1 used 0). With a terminal burden of 10¢ per $ of unfunded (section 7), the program cuts the maximum 75% of the plan in the second crisis year (D>C>C: PACE-CUT 3.75).

## 3. Outcomes and their probabilities (SYNTHETIC)

| Metric | Plan, revolver | Rolling policy, revolver | Plan, no revolver | Rolling, no revolver | Naive 8% | Naive 8% + revolver | Naive 4% |
|---|---|---|---|---|---|---|---|
| Certainty equivalent of W~ ($bn, exact CRRA 3) | 214.95 | 214.94 | 215.01 | 215.01 | 214.98 | 214.90 | 214.72 |
| Expected W~ ($bn, draws counted) | 220.36 | 220.45 | 220.38 | 220.51 | 220.31 | 220.24 | 220.56 |
| Expected annualized return | 7.4% | 7.4% | 7.4% | 7.4% | 7.4% | 7.4% | 7.4% |
| Median annualized return | 8.6% | 8.6% | 8.6% | 8.6% | 8.6% | 8.6% | 8.7% |
| CVaR10% as annualized return | -1.7% | -1.8% | -1.7% | -1.7% | -1.6% | -1.6% | -1.9% |
| P(annualized return ≥ 10%) | 41.3% | 41.3% | 41.3% | 41.3% | 41.3% | 41.3% | 41.3% |
| P(annualized return < 0) | 7.9% | 7.9% | 7.9% | 7.9% | 7.9% | 7.9% | 7.9% |
| P(any PE sale) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| P(PE fire sale at the crisis discount) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| P(red event: ADR-39 test) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| P(revolver drawn somewhere) | 15.0% | 26.2% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| P(NAV loan used somewhere) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| P(P2S used somewhere) | 48.0% | 95.5% | 27.0% | 95.5% | 0.0% | 0.0% | 0.0% |
| P(LEVER: synthetic, or a draw that pays for purchases) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| P(below the 8% target somewhere) | 35.4% | 35.4% | 35.4% | 35.4% | 27.6% | 27.6% | 100.0% |
| P(CFP Red or Black somewhere) | 33.3% | 33.3% | 33.3% | 33.3% | 32.4% | 32.4% | 100.0% |
| P(pacing cut somewhere) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| At t = 3: P(liquid share < 27%) | 22.2% | 18.9% | 22.2% | 22.2% | 24.9% | 24.9% | 20.4% |
| At t = 3: P(private NAV + unfunded > 80% of NAV, LR8) | 20.4% | 20.4% | 20.4% | 20.4% | 20.4% | 20.4% | 20.4% |
| At t = 3: P(NAV < 80% of today's) | 7.9% | 7.9% | 7.9% | 7.9% | 6.1% | 6.1% | 7.9% |
| Expected owner draws paid over 3 years ($bn) | 32.70 | 32.70 | 32.70 | 32.70 | 32.70 | 32.70 | 32.74 |

Columns: the **plan** is the static 3-year solution. The **rolling policy** executes only each node's first decision and re-solves a fresh 3-year tree at every node of years 1 and 2 (section 5); its probabilities are those of the policy that would actually run. The **naive rules** face the same flows, limits and charges: hold the target by selling liquid inside the IC range, sell liquid below the range before any PE if the 4% floor would fail, and never use a NAV loan, P2S, LEVER or a pacing cut. The revolver variant draws only for the floor ('lines drawn') and pays the undrawn fee. The owner's draw is paid in full at every node in every column: it is a fixed outflow in every cash row, not a choice.

Decomposition of the program's lead in certainty equivalent ($bn): program with revolver minus naive 8% -0.030 = value of the revolver to the program -0.066 + optimizing without it +0.036. With the revolver on both sides, the program leads by +0.043. Probabilities are coarse: 27 leaves whose masses run from 0.45% to 16.6%, so P(≥ 10% a year) moves in leaf-sized steps and is the same in every column (the regime path decides it).

Terminal distribution of the plan (revolver signed), worst to best, with the horizon balance sheet:

| Path | p | Cum. p | W~ ($bn) | Annualized | Treasury / NAV | Liquid share | LR8 | Debt ($bn) | NAV vs today | CFP |
|---|---|---|---|---|---|---|---|---|---|---|
| D>C>C>C | 0.0135 | 0.013 | 146.9 | -6.0% | 4.0% | 16.0% | 0.97 | 5.7 | -31.7% | Black |
| D>C>D>C | 0.0090 | 0.022 | 160.7 | -3.2% | 4.0% | 18.0% | 0.90 | 0.0 | -23.8% | Black |
| D>C>N>C | 0.0045 | 0.027 | 161.0 | -3.1% | 4.0% | 21.0% | 0.87 | 0.0 | -24.1% | Red |
| D>D>C>C | 0.0248 | 0.052 | 165.9 | -2.1% | 4.0% | 18.9% | 0.88 | 0.0 | -21.2% | Black |
| D>N>C>C | 0.0090 | 0.061 | 166.5 | -2.0% | 4.0% | 21.3% | 0.86 | 0.0 | -21.3% | Red |
| D>C>C>D | 0.0180 | 0.079 | 175.0 | -0.4% | 4.0% | 22.7% | 0.89 | 5.7 | -20.3% | Red |
| D>C>C>N | 0.0135 | 0.092 | 182.1 | 1.0% | 4.0% | 25.4% | 0.84 | 3.9 | -16.8% | Red |
| D>D>D>C | 0.0454 | 0.138 | 186.0 | 1.7% | 4.0% | 25.4% | 0.81 | 0.0 | -9.7% | Red |
| D>D>N>C | 0.0165 | 0.154 | 186.8 | 1.8% | 4.7% | 27.0% | 0.79 | 0.0 | -9.7% | Red |
| D>N>D>C | 0.0090 | 0.163 | 190.0 | 2.4% | 5.3% | 27.0% | 0.78 | 0.0 | -8.0% | Red |
| D>N>N>C | 0.0210 | 0.184 | 191.4 | 2.6% | 7.6% | 27.0% | 0.75 | 0.0 | -7.7% | Amber |
| D>D>C>D | 0.0330 | 0.217 | 196.3 | 3.5% | 4.0% | 25.5% | 0.81 | 0.0 | -8.3% | Red |
| D>N>C>D | 0.0120 | 0.229 | 196.7 | 3.6% | 4.7% | 27.0% | 0.79 | 0.0 | -8.3% | Red |
| D>C>D>D | 0.0330 | 0.262 | 196.9 | 3.6% | 4.3% | 25.3% | 0.81 | 0.0 | -7.9% | Red |
| D>C>N>D | 0.0090 | 0.271 | 199.9 | 4.1% | 6.0% | 27.0% | 0.77 | 0.0 | -6.5% | Red |
| D>D>C>N | 0.0248 | 0.296 | 204.0 | 4.8% | 6.0% | 27.0% | 0.77 | 0.0 | -4.5% | Amber |
| D>N>C>N | 0.0090 | 0.305 | 204.3 | 4.9% | 8.0% | 27.0% | 0.75 | 0.0 | -4.6% | Amber |
| D>C>D>N | 0.0180 | 0.323 | 206.5 | 5.3% | 8.0% | 25.2% | 0.77 | 0.0 | -3.3% | Amber |
| D>C>N>N | 0.0315 | 0.354 | 210.1 | 5.9% | 8.8% | 27.6% | 0.73 | 0.0 | -1.5% | Amber |
| D>D>D>D | 0.1664 | 0.521 | 226.6 | 8.6% | 8.0% | 27.9% | 0.73 | 0.0 | 8.8% | Amber |
| D>N>D>D | 0.0330 | 0.554 | 231.3 | 9.3% | 8.0% | 30.8% | 0.70 | 0.0 | 11.1% | Green |
| D>D>N>D | 0.0330 | 0.587 | 231.4 | 9.3% | 8.0% | 31.0% | 0.70 | 0.0 | 11.2% | Green |
| D>N>N>D | 0.0420 | 0.629 | 237.0 | 10.2% | 8.0% | 33.8% | 0.67 | 0.0 | 14.0% | Green |
| D>D>D>N | 0.0907 | 0.720 | 237.0 | 10.2% | 8.1% | 30.9% | 0.70 | 0.0 | 14.1% | Green |
| D>N>D>N | 0.0180 | 0.738 | 241.8 | 11.0% | 8.0% | 33.8% | 0.67 | 0.0 | 16.5% | Green |
| D>D>N>N | 0.1155 | 0.853 | 242.9 | 11.1% | 8.1% | 34.0% | 0.66 | 0.0 | 17.0% | Green |
| D>N>N>N | 0.1470 | 1.000 | 248.7 | 12.0% | 8.0% | 36.7% | 0.63 | 0.0 | 20.0% | Green |

At t = 3 every hard row still holds: the 4% floor, the NAV-loan cap and revolver availability of the leaf's regime (with forced paydowns). Debt can be repaid there but not drawn, because a draw at the horizon would cost nothing inside the tree. Shortfalls below the 8% target and the IC range are charged, so the plan cannot end in a state that the next year would have to repair for free. PE is valued at economic NAV (90% of the mark after a crisis year), and unfunded commitments carry a burden. LR8 is (private NAV + unfunded) / NAV; the architecture's default limit is 0.80.

## 4. Revolver signed or not (consent scenarios R1 and R0) and Phase I

Phase I asks whether every hard row can be met with reversible levers only, i.e. with no PE sale (ARCHITECTURE.md §5.5). Tier A is the 4% cash floor at every node. The IC range is not a Tier-1A row, so its shortfall is reported separately as tier B. With the revolver: the cash floor can be met without PE sales, but the IC range's lower edge cannot everywhere; tier A u* = 0.000bn, IC-range shortfall u* = 0.079bn (D>C>C>C ($5.82bn)). Without it: the cash floor can be met without PE sales, but the IC range's lower edge cannot everywhere; tier A u* = 0.000bn, IC-range shortfall u* = 0.593bn, all at t = 3 after crisis years (D>N>C>C ($2.07bn), D>D>C>C ($6.30bn), D>C>N>C ($2.64bn), D>C>D>C ($7.09bn), D>C>C>N ($0.30bn), D>C>C>D ($5.90bn), D>C>C>C ($13.22bn)). The IC range is elastic, so its shortfalls are priced, not forced, and they never trigger a PE sale.

| Path | p | λ with revolver | λ without | m with / without | Closing cash with / without | What changes |
|---|---|---|---|---|---|---|
| D | 1.000 | 0.68% | 0.67% | 1.00 / 1.00 | 14.2 / 14.2 | same actions |
| D>N | 0.300 | 0.34% | 0.24% | 0.76 / 0.76 | 15.3 / 15.3 | liquid book: SELL 1.15 -> SELL 1.13 |
| D>D | 0.550 | 0.96% | 0.82% | 0.92 / 0.92 | 14.6 / 14.6 | liquid book: SELL 6.45 -> SELL 6.42 |
| D>C | 0.150 | 0.65% | 0.71% | 1.47 / 1.47 | 6.0 / 6.0 | liquid book: HOLD -> SELL 6.27; corporate finance: REFINANCE 6.28 (revolver) -> NONE |
| D>N>N | 0.210 | 0.28% | 0.00% | 0.60 / 0.61 | 16.1 / 18.0 | liquid book: REFINANCE 0.64 (P2S) -> SELL 2.51 |
| D>N>D | 0.060 | 0.37% | 0.43% | 0.82 / 0.82 | 15.3 / 15.3 | liquid book: SELL 6.25 -> SELL 6.23 |
| D>N>C | 0.030 | 0.01% | 0.52% | 1.36 / 1.40 | 6.2 / 6.2 | liquid book: SELL 5.99 -> SELL 5.97 |
| D>D>N | 0.165 | 0.37% | 0.37% | 0.74 / 0.73 | 15.7 / 15.7 | liquid book: REFINANCE 0.44 (P2S) -> REFINANCE 0.42 (P2S) |
| D>D>D | 0.302 | 0.40% | 0.45% | 0.82 / 0.82 | 15.0 / 15.0 | liquid book: SELL 6.21 -> SELL 6.19 |
| D>D>C | 0.083 | 0.04% | 0.55% | 1.37 / 1.41 | 6.2 / 6.2 | liquid book: SELL 6.18 -> SELL 6.16 |
| D>C>N | 0.045 | 0.41% | 0.47% | 1.09 / 1.08 | 13.2 / 13.1 | liquid book: SELL 7.81 + REFINANCE 5.00 (P2S) -> SELL 1.16 + REFINANCE 5.00 (P2S); corporate finance: REPAY revolver 6.28 -> NONE |
| D>C>D | 0.060 | 1.76% | 1.76% | 1.24 / 1.22 | 10.9 / 10.6 | liquid book: SELL 11.43 + REFINANCE 5.00 (P2S) -> SELL 4.54 + REFINANCE 5.00 (P2S); corporate finance: REPAY revolver 6.28 -> NONE |
| D>C>C | 0.045 | 0.54% | 0.13% | 1.95 / 1.97 | 5.4 / 5.4 | liquid book: SELL 12.71 -> SELL 11.85; corporate finance: REPAY revolver 0.58 -> NONE |

Value of the signed revolver: −$0.066bn of certainty equivalent against $0.068bn of undrawn fees over 3 years. No root decision changes between R1 and R0, so no card here is consent-sensitive. Section 7 shows when the facility becomes valuable: with v1's hard IC range it is worth +$0.47bn, because without it the fund would have to sell PE.

## 5. The rolling policy (MPC): re-solving at every node of years 1 and 2

Only the root decision is executed. A year later the realized regime is known, the state is measured, and the same program is solved again on a fresh 3-year tree from there, with the same rules. A re-solve whose opening event stage is Amber or worse holds any PE sale at its own root at zero and prices it with a forced re-solve (ARCHITECTURE.md §5.4). The opening stage is read before the node's actions, on cash after the year's flows, which is why it is often Red or Black. At t = 3 each path settles with the same horizon rows as the plan. That is done at all 3 + 9 = 12 nodes, so every probability in the rolling columns of section 3 is that of the policy that would run.

| Node | p | Opening event stage | Plan made at t = 0 | Re-solved | Treasury / NAV | λ |
|---|---|---|---|---|---|---|
| D>N | 0.300 | Amber | Liquid SELL 1.15 | Liquid REFINANCE 1.21 (P2S) | 8.0% | 0.38% |
| D>D | 0.550 | Red | Liquid SELL 6.45 | Liquid SELL 4.46 + REFINANCE 2.09 (P2S) | 8.0% | 0.95% |
| D>C | 0.150 | Black | CF REFINANCE 6.28 (revolver) | CF REFINANCE 6.28 (revolver) | 4.0% | 0.65% |
| D>N>N | 0.210 | Amber | Liquid REFINANCE 0.64 (P2S) | Liquid SELL 0.52 | 8.0% | 0.46% |
| D>N>D | 0.060 | Red | Liquid SELL 6.25 | Liquid SELL 5.44 + REFINANCE 0.82 (P2S) | 8.0% | 0.94% |
| D>N>C | 0.030 | Black | Liquid SELL 5.99 | Liquid UNWIND P2S 1.21; CF REFINANCE 7.42 (revolver) | 4.0% | 0.65% |
| D>D>N | 0.165 | Amber | Liquid REFINANCE 0.44 (P2S) | Liquid REFINANCE 0.24 (P2S) | 8.0% | 0.55% |
| D>D>D | 0.302 | Red | Liquid SELL 6.21 | Liquid SELL 5.74 + REFINANCE 0.40 (P2S) | 8.0% | 0.95% |
| D>D>C | 0.083 | Black | Liquid SELL 6.18 | Liquid SELL 1.05 + UNWIND P2S 2.09; CF REFINANCE 7.50 (revolver) | 4.0% | 0.81% |
| D>C>N | 0.045 | Red | Liquid SELL 7.81 + REFINANCE 5.00 (P2S); CF REPAY revolver 6.28 | Liquid SELL 7.81 + REFINANCE 5.00 (P2S); CF REPAY revolver 6.28 | 8.0% | 0.73% |
| D>C>D | 0.060 | Black | Liquid SELL 11.43 + REFINANCE 5.00 (P2S); CF REPAY revolver 6.28 | Liquid SELL 11.43 + REFINANCE 5.00 (P2S); CF REPAY revolver 6.28 | 6.9% | 1.59% |
| D>C>C | 0.045 | Black | Liquid SELL 12.71; CF REPAY revolver 0.58 | Liquid SELL 10.91; CF REFINANCE 1.22 (revolver) | 4.0% | 0.91% |

The re-solved decisions differ from the plan only where the 3-year window has moved, so the horizon now sees one more year. The rolling policy's certainty equivalent is 214.944 against 214.946 for the plan. Forced re-solves that allow a PE sale at a re-solve's root would add at most $0.000bn. Check: re-solving the remaining subtree with the same horizon reproduces the plan exactly (max decision difference D>N: $8e-15bn, D>D: $8e-15bn, D>C: $9e-14bn). The program is time consistent; only the moving window changes decisions. v1's rolling CVaR floor was not time consistent and made the rolling policy sell PE at D>D. There is no floor in the main case now (section 7).

## 6. Horizon test: does the answer depend on where the tree stops?

Same inputs and rules, with the tree cut after 2, 3 and 4 years (ARCHITECTURE.md §5.2):

| Tree | Nodes | Root decision | Root λ | Plan at D>C (first crisis year) | CE (annualized) | P(any PE sale) R1 / R0 | P(red event) R1 / R0 | P(revolver drawn, years 1-2) |
|---|---|---|---|---|---|---|---|---|
| 2 years | 13 | Liquid BUY 0.84 | 0.80% | CF REFINANCE 6.28 (revolver) | 6.4% | 0.0% / 0.0% | 0.0% / 0.0% | 15.0% |
| 3 years | 40 | Liquid BUY 0.84 | 0.68% | CF REFINANCE 6.28 (revolver) | 6.7% | 0.0% / 0.0% | 0.0% / 0.0% | 15.0% |
| 4 years | 121 | Liquid BUY 0.84 | 0.81% | CF REFINANCE 6.28 (revolver) | 6.8% | 0.0% / 0.0% | 0.0% / 0.0% | 26.2% |

The root decision does not depend on the horizon, and neither does the first-crisis-year response. Plans further out shift a little with the cut, because the last decision year always looks one year ahead, so they are contingency plans, not policy. In v1 the 0% fire-sale headline and the LEVER and REFINANCE plans at t = 2 came from the cut. Horizon rows now hold every limit at t = 3 and price what is left to repair.

## 7. What moves the answer: the human-set inputs and their owners (SYNTHETIC)

The solve is objective, but its answer moves with a handful of inputs that people own. Each row changes one input in `params.json` and re-solves with and without the revolver. CE change is against the main case ($214.95bn).

| Input changed | Owner | Root decision (R1) | First crisis year D>C (R1) | CE change ($bn) | Revolver value ($bn) | P(PE sale) R1 / R0 | P(fire sale) R1 / R0 | P(red event) R1 / R0 | Max λ R1 / R0 |
|---|---|---|---|---|---|---|---|---|---|
| Main case | - | Liquid BUY 0.84 | CF REFINANCE 6.28 (revolver) | - | -0.066 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| IC range lower edge 24% (not 27%) | IC | Liquid BUY 0.84 | CF REFINANCE 6.28 (revolver) | +0.043 | -0.067 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.0% / 0.8% |
| IC range lower edge 20% | IC | Liquid BUY 0.84 | CF REFINANCE 6.28 (revolver) | +0.076 | -0.067 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.0% / 0.9% |
| IC lower edge hard everywhere, crisis years included (v1) | IC | Liquid BUY 0.84 | Liquid SELL 6.29 | -0.267 | +0.471 | 6.5% / 22.2% | 4.7% / 13.8% | 6.5% / 22.2% | 1.8% / 23.0% |
| Appetite prices 1% (not 2%) for the target and the range | IC (liquidity appetite) | Liquid BUY 0.84 | CF REFINANCE 6.28 (revolver) | +0.056 | -0.065 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.9% / 0.9% |
| Appetite prices 0.75% for the target and the range | IC (liquidity appetite) | Liquid BUY 7.91 | Liquid SELL 6.09; CF REFINANCE 7.50 (revolver) | +0.081 | -0.066 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.8% / 0.9% |
| Owner draw 10% in a crisis (Brent below $23) | Owner (Corporate Finance forecasts) | Liquid BUY 0.84 | Liquid SELL 3.04; CF REFINANCE 7.50 (revolver) | -0.013 | -0.064 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| Owner draw 6 / 7.5 / 10% by regime (v1) | Owner (Corporate Finance forecasts) | Liquid BUY 0.84 | Liquid SELL 3.04; CF REFINANCE 7.50 (revolver) | +0.017 | -0.064 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 2.2% / 2.3% |
| Crisis persistence 40% (v1) | Scenario engine (CRO validates) | Liquid BUY 0.84 | Liquid SELL 0.87; CF REFINANCE 5.41 (revolver) | -0.501 | -0.066 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.7% |
| Crisis secondary discount 25% (not 35%) | Market data (Secondaries) | Liquid BUY 0.84 | CF REFINANCE 6.28 (revolver) | +0.000 | -0.066 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| NAV loan against the whole PE book (v1 capacity) | Corporate Finance | Liquid BUY 0.84 | CF REFINANCE 6.28 (revolver) | +0.000 | -0.066 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| No terminal burden on unfunded (psi = 0, v1) | TPA (terminal values) | Liquid BUY 0.84 | CF REFINANCE 6.28 (revolver) | +0.349 | -0.066 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| Terminal burden on unfunded psi = 0.10 | TPA (terminal values) | Liquid BUY 0.84 | CF REFINANCE 6.28 (revolver) | -1.342 | -0.067 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| PE in crisis leaves at the reported mark (omega = 1, v1) | TPA (valuation) | Liquid REFINANCE 0.52 (P2S) + BUY 1.33 | Liquid UNWIND P2S 0.52; CF REFINANCE 6.88 (revolver) | +1.960 | -0.046 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| No price on the 8% cash target (4% floor only, v1) | IC (liquidity appetite) | Liquid BUY 7.91 | Liquid SELL 8.78; CF REFINANCE 4.82 (revolver) | +0.222 | -0.028 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.6% / 0.8% |
| 8% target counted gross of facility draws | IC (liquidity appetite) | Liquid BUY 5.04; CF LEVER 4.21 (revolver pays for purchases) | Liquid SELL 4.35; CF REFINANCE 2.10 (revolver) | +0.071 | +0.004 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.6% / 1.8% |
| Synthetic LEVER of the liquid book allowed | IC (leverage doctrine) | Liquid BUY 0.78 + LEVER 1.14 (synthetic) | Liquid SELL 0.08 + UNWIND P2S 1.14; CF REFINANCE 7.50 (revolver) | +0.002 | -0.064 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| Regimes move volatility (equal means only) | Scenario engine (CRO validates) | Liquid BUY 0.84 | Liquid SELL 6.29 | -0.223 | -0.073 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.8% / 1.8% |
| Regimes predict returns (v1 means with post-crisis rebound) | Scenario engine (CRO validates) | Liquid BUY 0.84 | Liquid SELL 7.92 | -4.380 | -0.070 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 2.1% / 2.2% |
| Risk aversion 5 (not 3) | IC and Board | Liquid SELL 8.21 | Liquid SELL 18.07 | n/a (other utility) | -0.066 | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |

What the table says:

- **A hard IC range brings back every v1 problem.** If the lower edge also binds in crisis years, the program fire-sells PE (P = 4.7% with the revolver, 13.8% without), λ reaches 23.0% without the revolver, and the revolver is worth +$0.47bn. A CIO would breach a soft range before selling PE at 35% (verify_finance.md H3); the elastic range does exactly that.
- **Regime-predictable volatility makes the program time the market.** With equal means only, the first crisis year's plan becomes 'Liquid SELL 6.29' with λ = 0.02%, and the revolver is never drawn: the sale pays for itself through the risk it removes, so it sells at the bottom for risk, not for cash. With v1's regime means, CE falls by $4.38bn and D>C becomes 'Liquid SELL 7.92'. The main case gives the program nothing to time.
- **Without a price on the 8% target** the root becomes 'Liquid BUY 7.91' and the revolver is drawn on 73.0% of paths: the fund spends its buffer on equities (Treasury 4.0% of NAV today) and leans on the revolver later. That is v1's 'Treasury at the floor, levering there' (verify_finance.md H6).
- **With the target counted gross of facility draws** the root becomes 'Liquid BUY 5.04; CF LEVER 4.21 (revolver pays for purchases)' and the revolver is drawn on 100.0% of paths: the fund borrows to buy equities. That is v1's 'Treasury at the floor, levering there' (verify_finance.md H6).
- **The appetite prices need to clear about 1%.** At 1% today's decision is 'Liquid BUY 0.84' (Treasury 8.0%), as at 2%; at 0.75% it becomes 'Liquid BUY 7.91' and Treasury falls to 4.0% of NAV, because a cheaper target is worth breaching for the return on equities. Any price above that threshold gives the same plan, so the exact number matters less than the IC's choice to treat 8% as a target.
- **The terminal burden on unfunded commitments (ψ) is the one input that turns PACE-CUT on**: at ψ = 0.10 the second crisis year reads 'Liquid SELL 12.88; PE PACE-CUT 3.75; CF REPAY revolver 0.75'. CE changes by −$1.34bn, so ψ deserves the estimation the architecture plans for it (§5.12).
- **Valuing crisis-leaf PE at the reported mark** (v1) adds +$1.96bn of certainty equivalent that does not exist (verify_finance.md M5).
- **Risk aversion** is the input that moves today's decision most: at γ = 5 the root becomes Liquid SELL 8.21.
- **Inputs that leave today's decision unchanged and cause no PE sale** (they still move the certainty equivalent and the contingent plans): IC range lower edge 24% (not 27%); IC range lower edge 20%; Appetite prices 1% (not 2%) for the target and the range; Owner draw 10% in a crisis (Brent below $23); Owner draw 6 / 7.5 / 10% by regime (v1); Crisis persistence 40% (v1); Crisis secondary discount 25% (not 35%); NAV loan against the whole PE book (v1 capacity); No terminal burden on unfunded (psi = 0, v1); Terminal burden on unfunded psi = 0.10; Regimes move volatility (equal means only); Regimes predict returns (v1 means with post-crisis rebound).

**Downside floors (a sensitivity, not part of the main case).** The architecture's Tier-1B floors apply to 10-year windows, which a 3-year tree that starts in a drought cannot test. A 3-year floor would be a new limit for the IC to set. Without one, the plan's CVaR10% is -1.7% a year, and the best any policy can reach is 0.9% a year. In every row a PE sale at the root is held at zero and priced by a forced re-solve, so a tail row is never met with a red-tier sale without the IC seeing it:

| CVaR10% floor (a year) | Binds? | Price of $1 of floor (today's $) | CE cost ($bn) | Root decision | P(any PE sale) | P(red event) | Forced re-solve with a root PE sale |
|---|---|---|---|---|---|---|---|
| -4.0% | no | 0.000 | 0.00 | Liquid BUY 0.84 | 0.0% | 0.0% | adds nothing (no root PE sale wanted) |
| -1.5% | yes | 0.037 | 0.04 | Liquid BUY 0.84 | 0.0% | 0.0% | adds nothing (no root PE sale wanted) |
| -1.0% | yes | 0.127 | 0.38 | Liquid SELL 6.01 | 0.0% | 0.0% | adds nothing (no root PE sale wanted) |
| -0.5% | yes | 0.302 | 1.22 | Liquid SELL 8.21 | 0.0% | 0.0% | adds nothing (no root PE sale wanted) |
| 0.0% | yes | 0.382 | 2.87 | Liquid SELL 16.88 | 4.5% | 4.5% | adds nothing (no root PE sale wanted) |
| 0.5% | yes | 0.612 | 6.00 | Liquid SELL 46.17 | 34.5% | 34.5% | adds nothing (no root PE sale wanted) |

v1's floor of −3.9% a year was set just above the unconstrained tail so that it would bind. Here it would be slack. A floor that binds is cheap at first and then expensive: near the best attainable tail the program sells the liquid book far below the IC range, and contingent PE sales (red events) appear.

## 8. What people set, what the program computes

| Set by people (inputs and limits, in params.json, each with an owner) | Computed by the program (no judgement) |
|---|---|
| Regime probabilities, regime returns and the CMA mean and volatility (scenario engine; CRO validates) | Every decision at every node |
| Secondary discounts, loan spreads, LTV and pledge caps, facility availability (market data; Corporate Finance) | λ and the state price at every node |
| Owner draw rule: 5-10% of NAV, higher when oil is weak (owner; Corporate Finance forecasts) | Which limits bind, and what each costs |
| Hard limits: 4% floor, 1.30x exposure, synthetic budget, IC range edges (IC) | Probabilities of every outcome, CE, CVaR, P(red event) |
| Appetite prices: 8% target and IC range shortfalls (IC); terminal PE value and unfunded burden (TPA) | The rolling policy, the horizon test and every sensitivity |
| Which facilities are signed (consent scenarios: Corporate Finance, banks, owner) | How decisions and prices change if a facility is not signed |
| Approval of the root decision, and of any red-tier sale (forced re-solve) | The forced re-solve that prices a held red-tier sale |

## 9. The program, written out

Per decision node n (13 nodes): post-decision states C (unencumbered cash), L (physical liquid), P (PE NAV, reported), U (unfunded), BR (revolver), BN (NAV loan), X (synthetic notional); trades sL, bL (sell / buy liquid), cv (P2S: physical to synthetic), uw (unwind), lev (synthetic LEVER, fixed at 0 by the doctrine), sP (sell PE), cut (pacing cut); s8 and sb (priced shortfalls below the 8% target and the IC range). Per leaf ℓ (27): settlement trades sL, bL, sP, facility moves, s8, sb, and terminal wealth W~.

```text
max  Σ_ℓ p_ℓ u_ℓ,   u_ℓ ≤ U(w_k) + U'(w_k)(W~_ℓ/W0 − w_k)              k = 1..10 tangents of CRRA(3)
cash  C_n = (1+r)C_p + (1+r)h_p X_p + (rL_n − r − s_X,p)X_p + δ_n P_p − q_n U_p + y_n Y_p − d_n·NAV_p
            − (r+s_R)BR_p − f_R(Lim−BR_p) − (r+s_N,p)BN_p
            + (1−τ)(sL_n + cv_n) − (1+τ)(bL_n + uw_n) + (1−disc_n)sP_n + (BR_n−BR_p) + (BN_n−BN_p) − h_n X_n
liq   L_n = (1+rL_n)L_p − sL_n + bL_n − cv_n + uw_n;      X_n = X_p + cv_n − uw_n + lev_n,  uw_n ≤ X_p
PE    P_n = (1+rP_n−δ_n)P_p + q_n U_p − sP_n;              U_n = (1−q_n)U_p + (plan − cut_p) − κ_U sP_n
hard  C_n ≥ 0.04·NAV_n   (NAV_n = C + hX + L + P + Y − BR − BN)                      every node, t = 3 too
      BN_n ≤ LTV_n·0.20·(P_n + Y_n);  BR_n ≤ avail_n·Lim;  L+X ≤ 0.37·NAV_n                    every node, t = 3 too
      L+P+Y+X ≤ 1.30·NAV_n;  X_n ≤ 5;  cut_n ≤ 0.75·plan                       decision nodes
      BR_ℓ ≤ BR_p;  BN_ℓ ≤ BN_p   (debt can be repaid at t = 3, not drawn)                  leaves
appetite  C_n − BR_n − BN_n + s8_n ≥ 0.08·NAV_n;   L_n + X_n + sb_n ≥ 0.27·NAV_n          every node, priced in W~
W~_ℓ = C + L + ω_ℓ·P + Y − BR − BN − ψ·U − c_PACE·Σcut − Σ_k π_k(s8_k + sb_k) + Σ_t d_t·NAV_{t−1}·G_{t→3}
```

p = parent node, n = the node (its regime sets the year's rates). π_k = 2¢ a year at N and D nodes and at t = 3, 0 in a crisis year; ω = 1 except 0.90 after a crisis year; ψ = 0.02. The owner draw d_n·NAV_p is a fixed liability of the year. No variable can skip it, so it is paid in full by construction.

Returns by (previous regime → this year's regime), computed from params.json so that next year's mean and volatility are the same from every regime (liquid book CMA 7.2%, PE 9.6%):

| Previous year | Liquid: to N | to D | to C | PE NAV: to N | to D | to C |
|---|---|---|---|---|---|---|
| N | 11.5% | 6.0% | -20.4% | 13.6% | 6.3% | -11.5% |
| D | 14.3% | 9.3% | -14.7% | 17.1% | 10.1% | -7.0% |
| C | 15.5% | 11.6% | -7.0% | 17.5% | 12.0% | -1.5% |

So a crisis after a calm year is a deeper loss than a crisis after a crisis, and nothing in the tree lets the program forecast a better or calmer year from today's regime.

## 10. What changed in version 2, and why

Every critical and high finding of `verify_finance.md` and `verify_math.md` is addressed, and so are the medium ones. The low ones are addressed where the fix was cheap; the rest are listed as open.

| Finding | Change in v2 | Where to see it |
|---|---|---|
| Horizon effects drive the t = 2 plans and the 0% fire-sale headline (finance H1, math 1) | Horizon nodes keep every hard row (4% floor, LTV and availability of the leaf's regime with forced paydowns), allow no new borrowing, and price what is left below the 8% target and the IC range; PE at economic value (ω), unfunded burden ψ > 0; horizon-node balance sheets reported; 2/3/4-year horizon test | §§1, 3, 6 |
| Probabilities describe the static plan, not the rolling policy (H2) | The rolling policy is simulated: re-solve at all 12 nodes of years 1-2, execute the first decision, settle at t = 3; its statistics sit beside the plan's | §§3, 5 |
| A hard 27% IC edge drives fire sales, the Phase I deficit and the revolver value (H3) | The IC lower edge is elastic (2¢ a year per $ below it, free in a crisis year); Phase I reports IC-range shortfalls apart from Tier 1A; the cause of the timing it masked is removed (M2); 27 / 24 / 20% and v1's hard edge in §7 | §§4, 7 |
| The naive-rule gap is caused by the band (H4) | Naive rules face the same flows, limits and charges and sell liquid below the range before any PE; a revolver variant; the lead is decomposed into revolver access and optimization | §3 |
| Revolver draws that fund purchases are labelled REFINANCE (H5) | P2S, unwind and synthetic LEVER are separate columns; a draw that pays for purchases is labelled LEVER; the exposure change is read against the parent's position | §§1, 2 |
| Treasury at the 4% floor in most t = 2 states, levering there; no 8% target or CFP stages (H6) | 8% own-liquidity target (net of facility draws), elastic and priced; CFP stage at every node; the doctrine (beta has α* < 0) keeps synthetic LEVER at zero; no liquid-book purchases in a crisis year (the CFP Red playbook adds no risk), and the target makes borrowed purchases costly elsewhere; P(LEVER while CFP Red or Black) is reported | §§1-3, 7 |
| λ not highest in crisis, unexplained (M1) | λ against m explained; λ uses the full liquidity dual mass (floor and target); one-sided prices probed at ± $0.5bn for kinks | §2 |
| The liquid book times regimes and sells at the bottom (M2) | Next year's expected return and volatility are the same from every regime (CMA mean, start-regime volatility); turnover and binding edges reported; the rebound rationale removed | §§7, 9 |
| Owner draw far from the research (M3) | N and D draw 5.8% ($10.3bn, inside the research's $9.9-10.8bn); a crisis with an oil shock 7.5%; the 10% cap and v1's draws as sensitivities | §7 |
| NAV-loan capacity 2.5-3x the architecture's cap (M4) | Pledge pool capped at 20% of private NAV: $2.1bn at 10% LTV, $1.1bn at 5%; v1's capacity as a sensitivity | §7 |
| PE valued at stale marks in crisis leaves (M5) | Economic value 90% of the mark after a crisis year; the 35% crisis discount labelled a stress case and 25% shown | §§3, 7 |
| PACE-CUT never chosen because ψ = 0 (M6) | ψ = 2¢ stated with a sensitivity (0 and 10¢); corridor with a 25% protected core sleeve; break-even printed | §§2, 7 |
| CVaR floor tuned to bind (M7); root decision a corner of two tuned limits (math 4) | No floor in the main case; floors from −4% to +0.5% a year as a sensitivity, with root PE sales held at zero and priced by forced re-solve; 'Tier 1B' label dropped; today's decision now sits at the 8% target, and §7 shows how it moves with every input | §7 |
| Math 2 and 3: λ read as 'about the loan spread'; recovery mode drops the floor by a hard-coded rule | λ ≈ (1 − f)/(1 + r) × net cost of the marginal source, with the ranges read from this run; no floor in the main case or the rolling policy, so no recovery mode is triggered, and an unattainable floor in §7 is reported with its forced re-solve | §§2, 5, 7 |
| Red-event test (ADR-39) not applied (M8) | P(red event) in every outcome column; the root red-tier SELL rule (today's stage is computed: Green); re-solves at Amber or worse hold root PE sales at zero | §§3, 5 |
| No sensitivity table (M9) | One-at-a-time table with the owner of each input | §7 |
| Low: crisis persistence 40% (L1) | 30% (17-month mean spell); 40% as a sensitivity | §7 |
| Low: terminal risk metrics missing (L3) | LR8, NAV drawdown, Treasury, liquid share and debt per leaf | §3 |
| Low: SYNTHETIC labels (L4); coarse probabilities (L5); naive breaches (L6, math 5) | Tagged headings; coarseness stated; naive rules trim to the upper edge and report breaches | §3 |
| Low: flat synthetic financing (L7) | 30 / 81 / 175bp by regime | params.json |
| Math: circular stationarity check (6); 8-digit rounding (7); hard-coded settings (8); LEVER label on the stock (9) | Direct carry re-solve; 12 significant digits and per-node residuals; thresholds moved to params.json 'settings'; labels read changes against the parent | §11; results.json |

**Still open (stated, not fixed):**

- The yield book ($40bn) still has no levers (verify_finance.md L2): amber sales of private credit and the SMA run-off are not modelled, so the waterfall goes from liquid assets and facilities straight to PE.
- Covenant risk on the revolver after a large NAV fall is not modelled (L7).
- Three branches a year are coarse: the tree's volatility is set to the start regime's (9.5% liquid, 7.6% reported PE), below a real blended book's. Results that depend on tails (CVaR, P(red event)) should be read as illustrations. More scenarios per node (M2's second fix) would cost the 40-node picture.
- ψ, ω and the two appetite prices are stated values with sensitivities. The architecture estimates terminal values by regression on simulated paths (§5.12), which this toy does not have.
- Contingent plans at t ≥ 1 are not unique where two funding mixes are worth the same (section 11). Only the root decision is executed, and it is unique and horizon-invariant here.

## 11. Checks run by tree_demo.py

- Probabilities sum to 1 at every stage: {'0': 1.0, '1': 1.0, '2': 1.0, '3': 1.0}.
- Every identity, recomputed from the reported states (not the LP rows): opening stocks from the parent's closing stocks and the year's rates; closing stocks from the opening stocks and the trades; the owner draw = draw rate × the parent's closing NAV. The largest residual is 6.0e-14bn. Terminal wealth: LP against recomputed 5.7e-14bn.
- Every limit at every node, both consent scenarios: all hold = True (smallest slack by family, revolver case: cash floor (4%) -4.4e-15; 8% target incl. priced shortfall -3.6e-15; NAV-loan capacity 1.0e+00; revolver availability 1.2e+00; IC range upper edge 5.6e-01; IC range lower edge incl. priced shortfall -7.1e-15; exposure cap 4.0e+01; synthetic budget 0.0e+00; pacing cut <= 75% of plan 3.8e+00; non-negative stocks 0.0e+00).
- Duals: finite-difference re-solves on 41 rows (every decision node's cash row, binding limits, some leaves) agree with the LP duals to a relative 2.2e-06. λ was also recomputed with a direct carry re-solve at every decision node (inject $1 and tighten the floor and the target so it cannot relieve them). That replaces v1's circular reduced-cost check, and it agrees to 3.3e-10. Kink probes at ± $0.5bn: none near a kink.
- Piecewise-linear utility: largest error at the leaves 2.3e-03 (a level bias of $0.11bn in certainty equivalent; every comparison uses the exact CRRA). Re-solved with 48 tangents: certainty equivalent 214.947 against 214.946. The root decision moves by $0.00bn. The largest move anywhere is $3.91bn at D>C>N (Liquid SELL 7.81 + REFINANCE 5.00 (P2S); CF REPAY revolver 6.28 against Liquid SELL 11.53 + REFINANCE 1.09 (P2S); CF REPAY revolver 6.28), a node where the two funding mixes are worth the same to within the certainty-equivalent difference above.
- Time consistency: re-solving each year-1 subtree reproduces the plan to 9.4e-14bn.
- Deterministic: single-threaded dual simplex, fixed seed, no sampling; results.json hash `eec513b66e7a1dfb…`.

## Verification (independent re-implementation)

`verify_independent.py` re-implements the program from section 9 and `params.json` without calling `tree_demo.py`'s model code. The tree is built depth-first and keyed by path, every row is a cvxpy expression, and the program is solved with CLARABEL (interior point) and with HiGHS through cvxpy. It checked results.json `eec513b66e7a1dfb…` on 2026-10-19. **Result: all three checks pass.**

| Check | What was compared | Result |
|---|---|---|
| 1. Objective agreement, revolver signed | E[Û]: author -0.338692698011; independent HiGHS -0.338692698011, CLARABEL -0.338692698041 (each with its own two-pass tangents) | relative difference 6.0e-13 / 9.0e-11; tangents agree to 3.9e-12 |
| 1. Objective agreement, no revolver | author -0.338499473967; HiGHS -0.338499473967, CLARABEL -0.338499474097 | relative difference 3.9e-13 / 3.8e-10 |
| 1. Decisions and states at all 40 nodes | sells, buys, PE sales, P2S, closing C, L, P, U, BR, BN, X (HiGHS vertex, author's tangents) | largest difference $9.9e-11bn (D>C>C>N L); no revolver $2.5e-09bn |
| 2. Identities at every node, from the published values | opening stocks from the parent's closing stocks and the year's rates; closing stocks from the trades; owner draw = rate × parent's NAV; probabilities | largest residual 5.6e-10 (revolver) / 5.6e-10 (no revolver) |
| 2. Limits at every node, from the published values | 4% floor, 8% target with its priced shortfall, NAV-loan capacity, revolver availability, IC range edges, exposure cap, synthetic budget, pacing cap, non-negative stocks | smallest slack -4.8e-11 / -8.5e-11 (≥ 0 holds) |
| 3. Cash price at all 13 decision nodes | μ published against ± $0.001bn re-solves (HiGHS) | largest relative error 4.1e-10; right and left slopes agree to 2.7e-09 |
| 3. λ at all 13 decision nodes | λ published against a carry re-solve (inject $1, tighten the floor and target by (1 − f) and (1 − 0.08)) | largest absolute difference 2.1e-09 |
| Uniqueness of the decisions that matter | the range of each decision at t = 0 and t = 1 over the whole optimal face (objective held at its optimum) | root: $2.0e-05bn; year 1: $6.4e-04bn (D>D cv) |

What this does and does not show: an independently written program with the same inputs reaches the same optimum, decisions and prices, and the published numbers satisfy every row. It does not test whether the inputs are right. That is what the sensitivities in section 7 are for. Details are in `verification.json`.

